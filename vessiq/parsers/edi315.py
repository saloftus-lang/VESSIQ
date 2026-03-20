"""
EDI X12 315 Parser
------------------
Parses raw EDI 315 (Ocean Shipment Status) messages into structured dicts.

EDI 315 is the standard transaction set carriers use to communicate vessel
and container status events. Common senders: Maersk, MSC, CMA CGM, ONE.

Segment structure (key segments we extract):
  ISA  — Interchange header (sender/receiver IDs)
  GS   — Functional group header
  ST   — Transaction set header (315)
  B4   — Beginning: status code, date, time, container/voyage refs
  N9   — Reference numbers (BOL, booking, container)
  Q2   — Vessel details (name, voyage, dates)
  R4   — Port/location (UN/LOCODE)
  DTM  — Date/time qualifiers (ETA, ETD, actual)
  SE   — Transaction set trailer

EDI 315 Status Codes → EventType mapping is in edi315.yaml config.
"""

from __future__ import annotations

import re
from typing import Any


def parse(raw_edi: str) -> list[dict[str, Any]]:
    """
    Parse a raw EDI 315 string (may contain multiple transaction sets).
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
    # Sub-element separator is at position 104 of ISA (the repetition separator or component)
    # Segment terminator is right after ISA[105] = position 106
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
    Extract relevant fields from a single 315 transaction set.
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

        elif tag == "B4":
            # B401: Special Handling Code (often empty)
            # B402: Shipment Status Code  ← the event type code (VE, UV, AV, etc.)
            # B403: Status Date (CCYYMMDD or YYMMDD)
            # B404: Status Time (HHMM)
            # B405: Time Code
            # B406: Voyage Number
            # B407: Equipment Initial (container prefix)
            # B408: Equipment Number
            # B409: Equipment Type
            data["status_code"] = _get(el, 2)   # position 2, not 1
            data["status_date"] = _get(el, 3)
            data["status_time"] = _get(el, 4)
            data["time_code"] = _get(el, 5)
            data["voyage_number"] = data.get("voyage_number") or _get(el, 6)
            data["equipment_initial"] = _get(el, 7)
            data["equipment_number"] = _get(el, 8)
            # Container number = initial + number
            init = data.get("equipment_initial", "") or ""
            num = data.get("equipment_number", "") or ""
            if init or num:
                data["container_number"] = (init + num).strip()

        elif tag == "N9":
            # N901: Reference qualifier (BM=BOL, BK=Booking, CN=Container)
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

        elif tag == "Q2":
            # Q201: Vessel name
            # Q202: Country code
            # Q203: Date (vessel departure from origin)
            # Q204: Date (vessel arrival at destination)
            # Q205: Date (vessel departure from last port)
            # Q206: Vessel code qualifier
            # Q207: Voyage number
            # Q208: Vessel IMO / reference
            data["vessel_name"] = _get(el, 1)
            data["vessel_eta_raw"] = _get(el, 4)   # Arrival date at destination
            data["vessel_etd_raw"] = _get(el, 3)   # Departure date
            data["voyage_number"] = _get(el, 7) or data.get("voyage_number")
            data["vessel_imo"] = _get(el, 8)

        elif tag == "R4":
            # R401: Port function code (L=loading, D=discharge, R=origin, E=destination)
            # R402: Location qualifier (UN=UN/LOCODE, W=SPLC)
            # R403: Location ID
            # R404: Location name
            # R405: Country code
            func = _get(el, 1)
            qualifier = _get(el, 2)
            location_id = _get(el, 3)
            location_name = _get(el, 4)

            # Prefer discharge/destination port as the "event port"
            if func in ("D", "E") or not data.get("port_locode"):
                if qualifier == "UN" and location_id:
                    data["port_locode"] = location_id
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

    return data


def _get(elements: list[str], index: int) -> str | None:
    """Safe element access — returns None if missing or empty."""
    if index < len(elements):
        val = elements[index].strip()
        return val if val else None
    return None
