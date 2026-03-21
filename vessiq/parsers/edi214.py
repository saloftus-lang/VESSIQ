"""
EDI X12 214 Parser
------------------
Parses raw EDI 214 (Transportation Carrier Shipment Status Message) into
structured dicts.

EDI 214 is the standard transaction set used by motor carriers and intermodal
providers to communicate shipment status updates to shippers and consignees.
Common senders: J.B. Hunt, Schneider, XPO Logistics, BNSF, Union Pacific.

Segment structure (key segments we extract):
  ISA  — Interchange header (sender/receiver IDs)
  GS   — Functional group header
  ST   — Transaction set header (214)
  B10  — Shipment identification (BOL, shipment ID, carrier SCAC)
  L11  — Business reference numbers (reference number, qualifier)
  MS1  — Equipment/shipment location (city, state, country)
  MS2  — Equipment status (SCAC, event code, event date)
  AT7  — Shipment status detail (status code, reason code, date, time)
  AT8  — Shipment weight/pieces
  SE   — Transaction set trailer

AT7 Status Codes → EventType mapping is in edi214.yaml config.
"""

from __future__ import annotations

from typing import Any


def parse(raw_edi: str) -> list[dict[str, Any]]:
    """
    Parse a raw EDI 214 string (may contain multiple transaction sets).
    Returns a list of raw event dicts — one per ST/SE transaction.
    """
    raw_edi = _normalize_line_endings(raw_edi)
    segment_terminator, element_separator, sub_separator = _detect_delimiters(raw_edi)
    segments = _split_segments(raw_edi, segment_terminator)
    transactions = _split_transactions(segments)

    results = []
    for txn_segments in transactions:
        parsed = _parse_transaction(txn_segments, element_separator, sub_separator)
        if parsed:
            results.append(parsed)
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalize_line_endings(raw: str) -> str:
    return raw.replace("\r\n", "\n").replace("\r", "\n")


def _detect_delimiters(raw: str) -> tuple[str, str, str]:
    """
    EDI delimiters are defined in the ISA segment (fixed-width header).
    ISA is always 106 characters. The element separator is ISA[3],
    the segment terminator is the character after ISA[105].
    """
    isa_start = raw.find("ISA")
    if isa_start == -1:
        # Fallback to common defaults
        return "~", "*", ":"

    isa = raw[isa_start:]
    element_sep = isa[3]         # character at position 3
    # Sub-element separator is at position 104 of ISA
    sub_sep = ":"
    if len(isa) > 104:
        sub_sep = isa[104]
    seg_term = "~"
    if len(isa) > 105:
        candidate = isa[105]
        if candidate.strip():
            seg_term = candidate
        elif len(isa) > 106:
            seg_term = isa[106]

    return seg_term, element_sep, sub_sep


def _split_segments(raw: str, terminator: str) -> list[str]:
    segments = []
    for seg in raw.split(terminator):
        seg = seg.strip()
        if seg:
            segments.append(seg)
    return segments


def _split_transactions(segments: list[str]) -> list[list[str]]:
    """Group segments into individual ST/SE transaction sets."""
    transactions: list[list[str]] = []
    current: list[str] = []
    in_txn = False

    for seg in segments:
        tag = seg.split("*")[0] if "*" in seg else seg[:3]
        if tag == "ST":
            in_txn = True
            current = [seg]
        elif tag == "SE":
            if in_txn:
                current.append(seg)
                transactions.append(current)
                current = []
                in_txn = False
        elif in_txn:
            current.append(seg)

    return transactions


def _elements(segment: str, sep: str) -> list[str]:
    """Split a segment string into elements, padding empties."""
    parts = segment.split(sep)
    return parts


def _parse_transaction(segments: list[str], elem_sep: str, sub_sep: str) -> dict[str, Any]:
    """
    Extract relevant fields from a single 214 transaction set.
    Returns a flat dict of raw parsed values.
    """
    data: dict[str, Any] = {
        "segment_tags_seen": [],
        "references": {},   # L11 refs keyed by qualifier
    }

    for seg in segments:
        el = _elements(seg, elem_sep)
        tag = el[0]
        data["segment_tags_seen"].append(tag)

        if tag == "ISA":
            data["isa_sender_id"] = _get(el, 6)
            data["isa_receiver_id"] = _get(el, 8)
            data["isa_date"] = _get(el, 9)

        elif tag == "B10":
            # B1001: Reference Identification (Shipment ID)
            # B1002: Shipment Identification Number / BOL Number
            # B1003: Standard Carrier Alpha Code (SCAC)
            data["shipment_id"] = _get(el, 1)
            data["bill_of_lading"] = _get(el, 2)
            data["carrier_scac"] = _get(el, 3)

        elif tag == "L11":
            # L1101: Reference Identification (reference number)
            # L1102: Reference Identification Qualifier
            #   BM = BOL, BK = Booking, CN = Container, SI = Shipper ID,
            #   CR = Customer Reference, PO = Purchase Order
            ref_value = _get(el, 1)
            qualifier = _get(el, 2)
            if qualifier and ref_value:
                data["references"][qualifier] = ref_value
                if qualifier == "BM":
                    data["bill_of_lading"] = data.get("bill_of_lading") or ref_value
                elif qualifier == "BK":
                    data["booking_number"] = ref_value
                elif qualifier in ("CN", "EQ"):
                    data["container_number"] = data.get("container_number") or ref_value
                elif qualifier == "SI":
                    data["shipper_id"] = ref_value
                elif qualifier == "CR":
                    data["customer_reference"] = ref_value
                elif qualifier == "PO":
                    data["purchase_order"] = ref_value
                elif qualifier == "VN":
                    data["voyage_number"] = ref_value

        elif tag == "MS1":
            # MS101: City Name
            # MS102: State/Province Code
            # MS103: Country Code
            city = _get(el, 1)
            state = _get(el, 2)
            country = _get(el, 3)
            data["location_city"] = city
            data["location_state"] = state
            data["location_country"] = country
            # Build a port_name from city + state
            parts = [p for p in [city, state] if p]
            if parts:
                data["port_name"] = ", ".join(parts)

        elif tag == "MS2":
            # MS201: Standard Carrier Alpha Code (SCAC)
            # MS202: Equipment Number
            # MS203: Equipment Description Code
            # MS204: Equipment Initial (container prefix)
            data["carrier_scac"] = _get(el, 1) or data.get("carrier_scac")
            equip_num = _get(el, 2)
            equip_init = _get(el, 4)
            if equip_init or equip_num:
                init = equip_init or ""
                num = equip_num or ""
                data["container_number"] = data.get("container_number") or (init + num).strip()

        elif tag == "AT7":
            # AT701: Shipment Status Code
            #   X1=Arrived, X3=Departed, X6=En Route, AF=Carrier Departed,
            #   AG=Estimated Delivery, D1=Completed Delivery, etc.
            # AT702: Shipment Status/Reason Code (reason for status)
            # AT703: Shipment Appointment Status Code
            # AT704: Shipment Status Code (secondary)
            # AT705: Date (CCYYMMDD)
            # AT706: Time (HHMM)
            # AT707: Time Code (LT=Local Time, ET=Eastern, CT=Central, etc.)
            data["status_code"] = _get(el, 1)
            data["status_reason_code"] = _get(el, 2)
            data["appointment_status"] = _get(el, 3)
            data["status_date"] = _get(el, 5)
            data["status_time"] = _get(el, 6)
            data["time_code"] = _get(el, 7)

        elif tag == "AT8":
            # AT801: Weight Qualifier (G=Gross, N=Net)
            # AT802: Weight Unit Code (L=Pounds, K=Kilograms)
            # AT803: Weight
            # AT804: Lading Quantity (number of pieces)
            data["weight_qualifier"] = _get(el, 1)
            data["weight_unit"] = _get(el, 2)
            data["weight"] = _get(el, 3)
            data["lading_quantity"] = _get(el, 4)

    return data


def _get(elements: list[str], index: int) -> str | None:
    """Safe element access — returns None if missing or empty."""
    if index < len(elements):
        val = elements[index].strip()
        return val if val else None
    return None
