"""
EDI X12 322 Parser
------------------
Parses raw EDI 322 (Terminal Operations and Intermodal Container Status)
messages into structured dicts.

EDI 322 is the standard transaction set used by railroads and container yards
to communicate container status updates. Common senders: BNSF, Union Pacific,
CSX, Norfolk Southern.

Segment structure (key segments we extract):
  ISA  — Interchange header (sender/receiver IDs)
  GS   — Functional group header
  ST   — Transaction set header (322)
  Q5   — Status details (status code, date, time, timezone)
  N7   — Equipment details (container number, equipment type)
  R4   — Port/location (qualifier, LOCODE, city)
  DTM  — Date/time references
  N9   — Reference numbers (BOL, booking)
  V1   — Vessel identification (name, IMO, voyage)
  SE   — Transaction set trailer

EDI 322 Q5 Status Codes → EventType mapping is in edi322.yaml config.
"""

from __future__ import annotations

from typing import Any


def parse(raw_edi: str) -> list[dict[str, Any]]:
    """
    Parse a raw EDI 322 string (may contain multiple transaction sets).
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
    Extract relevant fields from a single 322 transaction set.
    Returns a flat dict of raw parsed values.
    """
    data: dict[str, Any] = {
        "segment_tags_seen": [],
        "references": {},   # N9 refs keyed by qualifier
    }

    for seg in segments:
        el = _elements(seg, elem_sep)
        tag = el[0]
        data["segment_tags_seen"].append(tag)

        if tag == "ISA":
            data["isa_sender_id"] = el[6].strip() if len(el) > 6 else None
            data["isa_receiver_id"] = el[8].strip() if len(el) > 8 else None
            data["isa_date"] = el[9].strip() if len(el) > 9 else None

        elif tag == "Q5":
            # Q501: Status Code (AE, AL, UA, LR, OA, CD, etc.)
            # Q502: Status Date (CCYYMMDD)
            # Q503: Status Time (HHMM)
            # Q504: Time Code (timezone: LT, ET, CT, MT, PT)
            # Q505: Status Reason Code (optional)
            data["status_code"] = _get(el, 1)
            data["status_date"] = _get(el, 2)
            data["status_time"] = _get(el, 3)
            data["time_code"] = _get(el, 4)
            data["status_reason"] = _get(el, 5)

        elif tag == "N7":
            # N701: Equipment Initial (container prefix, e.g. MSCU)
            # N702: Equipment Number (numeric portion)
            # N703: Weight (optional)
            # N704: Weight Qualifier (optional)
            # N705: Equipment Description Code
            # N706: Equipment Length (optional)
            # N707: Height (optional)
            # N708: Width (optional)
            # N709: Equipment Type (e.g. CN=Container, TL=Trailer)
            data["equipment_initial"] = _get(el, 1)
            data["equipment_number"] = _get(el, 2)
            data["equipment_type_code"] = _get(el, 5) if len(el) > 5 else None
            init = (data.get("equipment_initial") or "").strip()
            num = (data.get("equipment_number") or "").strip()
            if init or num:
                data["container_number"] = (init + num).strip()

        elif tag == "V1":
            # V101: Vessel Code / IMO (ocean vessel code)
            # V102: Vessel Name
            # V103: Country Code
            # V104: Flight/Voyage Number
            # V105: Vessel Code Qualifier (L=Lloyds)
            data["vessel_imo"] = _get(el, 1)
            data["vessel_name"] = _get(el, 2)
            data["vessel_country"] = _get(el, 3)
            data["voyage_number"] = _get(el, 4)

        elif tag == "N9":
            # N901: Reference qualifier (BM=BOL, BK=Booking, CN=Container, WO=Work Order)
            # N902: Reference value
            qualifier = _get(el, 1)
            value = _get(el, 2)
            if qualifier and value:
                data["references"][qualifier] = value
                if qualifier == "BM":
                    data["bill_of_lading"] = value
                elif qualifier == "BK":
                    data["booking_number"] = value
                elif qualifier in ("CN", "EQ"):
                    data["container_number"] = data.get("container_number") or value

        elif tag == "R4":
            # R401: Port/terminal function code
            #   K=Port of Loading, L=Port of Discharge, R=Origin, E=Destination
            #   5=Ramp/Intermodal, I=Interchange Point, Y=Container Yard
            # R402: Location qualifier (UN=UN/LOCODE, CI=City, ZZ=Mutually Defined)
            # R403: Location ID
            # R404: Location name (city/port name)
            # R405: Country code
            func = _get(el, 1)
            qualifier = _get(el, 2)
            location_id = _get(el, 3)
            location_name = _get(el, 4)

            # Store terminal/yard info separately from port
            if func in ("Y", "5", "I"):
                # Container yard, ramp, or interchange point
                data["terminal_code"] = location_id
                data["terminal_name"] = location_name
            # Prefer destination/discharge location as the event port
            if func in ("E", "L") or not data.get("port_locode"):
                if qualifier == "UN" and location_id:
                    data["port_locode"] = location_id
                elif qualifier in ("CI", "ZZ") and location_id:
                    # Non-LOCODE location — store ID as-is
                    data["port_locode"] = data.get("port_locode") or location_id
                data["port_name"] = location_name

        elif tag == "DTM":
            # DTM01: Date/time qualifier
            # DTM02: Date (CCYYMMDD)
            # DTM03: Time (HHMM)
            qualifier = _get(el, 1)
            date_val = _get(el, 2)
            time_val = _get(el, 3)

            if qualifier == "140":  # Estimated arrival
                data["eta_date"] = date_val
                data["eta_time"] = time_val
            elif qualifier == "139":  # Estimated departure
                data["etd_date"] = date_val
                data["etd_time"] = time_val
            elif qualifier == "137":  # Transaction creation date
                data["transaction_date"] = date_val
            elif qualifier == "036":  # Expiration date
                data["expiration_date"] = date_val
            elif qualifier == "050":  # Received date
                data["received_date"] = date_val
                data["received_time"] = time_val

    return data


def _get(elements: list[str], index: int) -> str | None:
    """Safe element access — returns None if missing or empty."""
    if index < len(elements):
        val = elements[index].strip()
        return val if val else None
    return None
