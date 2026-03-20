"""
VESSIQ Normalization Engine
----------------------------
Takes raw parsed dicts (from any parser) and maps them to the unified
VesselEvent schema using YAML config files.

This is the core of VESSIQ: a config-driven translation layer that converts
messy, source-specific field names and codes into a clean, consistent schema.

Adding a new data source = add a parser + add a YAML mapping. No engine changes.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

from vessiq.schema import EventType, SourceFormat, VesselEvent

logger = logging.getLogger(__name__)

# Path to the mappings directory
_MAPPINGS_DIR = Path(__file__).parent.parent / "config" / "mappings"


def _load_mapping(format_key: str) -> dict:
    """Load the YAML mapping config for a given format (e.g. 'edi315')."""
    path = _MAPPINGS_DIR / f"{format_key}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No mapping config found at {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def normalize_edi315(
    raw_events: list[dict[str, Any]],
    source_name: str = "EDI_SOURCE",
) -> tuple[list[VesselEvent], list[str]]:
    """
    Normalize a list of raw EDI 315 parsed dicts into VesselEvent objects.

    Returns:
        (events, errors) — successfully normalized events + list of error strings
    """
    config = _load_mapping("edi315")
    events: list[VesselEvent] = []
    errors: list[str] = []

    for i, raw in enumerate(raw_events):
        try:
            event = _normalize_edi315_record(raw, config, source_name)
            events.append(event)
        except Exception as e:
            msg = f"EDI 315 record {i}: {e}"
            logger.warning(msg)
            errors.append(msg)

    return events, errors


def normalize_csv_terminal(
    raw_rows: list[dict[str, Any]],
    source_name: str = "CSV_TERMINAL",
) -> tuple[list[VesselEvent], list[str]]:
    """
    Normalize a list of raw CSV terminal row dicts into VesselEvent objects.

    Returns:
        (events, errors) — successfully normalized events + list of error strings
    """
    config = _load_mapping("csv_terminal")
    events: list[VesselEvent] = []
    errors: list[str] = []

    for i, raw in enumerate(raw_rows):
        try:
            event = _normalize_csv_record(raw, config, source_name)
            events.append(event)
        except Exception as e:
            row_idx = raw.get("_row_index", i)
            msg = f"CSV row {row_idx}: {e}"
            logger.warning(msg)
            errors.append(msg)

    return events, errors


# ---------------------------------------------------------------------------
# EDI 315 record normalizer
# ---------------------------------------------------------------------------

def _normalize_edi315_record(
    raw: dict[str, Any], config: dict, source_name: str
) -> VesselEvent:
    status_codes: dict = config.get("status_codes", {})
    date_formats: list = config.get("date_formats", ["%Y%m%d", "%y%m%d"])
    time_formats: list = config.get("time_formats", ["%H%M"])

    # Map status code → EventType
    status_code = (raw.get("status_code") or "").upper()
    event_type = _map_event_type(status_code, status_codes)

    # Parse event timestamp from B4 date + time
    event_ts = _parse_datetime(
        raw.get("status_date"),
        raw.get("status_time"),
        date_formats,
        time_formats,
    )

    # Parse ETA/ETD
    eta = _parse_datetime(
        raw.get("eta_date") or raw.get("vessel_eta_raw"),
        raw.get("eta_time"),
        date_formats,
        time_formats,
    )
    etd = _parse_datetime(
        raw.get("etd_date") or raw.get("vessel_etd_raw"),
        raw.get("etd_time"),
        date_formats,
        time_formats,
    )

    return VesselEvent(
        source_format=SourceFormat.EDI_315,
        source_name=source_name,
        vessel_name=_clean(raw.get("vessel_name")),
        vessel_imo=_clean(raw.get("vessel_imo")),
        voyage_number=_clean(raw.get("voyage_number")),
        event_type=event_type,
        event_timestamp=event_ts,
        estimated_arrival=eta,
        estimated_departure=etd,
        port_locode=_clean(raw.get("port_locode")),
        port_name=_clean(raw.get("port_name")),
        container_number=_clean(raw.get("container_number")),
        booking_number=_clean(raw.get("booking_number")),
        bill_of_lading=_clean(raw.get("bill_of_lading")),
        raw_data=raw,
    )


# ---------------------------------------------------------------------------
# CSV terminal record normalizer
# ---------------------------------------------------------------------------

def _normalize_csv_record(
    raw: dict[str, Any], config: dict, source_name: str
) -> VesselEvent:
    column_map: dict = config.get("column_map", {})
    aliases: dict = config.get("column_aliases", {})
    event_type_map: dict = config.get("event_type_map", {})
    date_formats: list = config.get("date_formats", ["%Y-%m-%d %H:%M:%S"])

    # Build a resolved field dict by checking aliases in priority order
    resolved = _resolve_fields(raw, column_map, aliases)

    # Map event type string → EventType
    # Normalize spaces to underscores so "Gate In" matches "gate_in" in config
    raw_event_type = _clean(resolved.get("event_type_raw")) or ""
    normalized_event_key = raw_event_type.lower().replace(" ", "_")
    event_type = _map_event_type(normalized_event_key, event_type_map)

    # Parse timestamps
    event_ts = _parse_datetime_str(resolved.get("event_timestamp_raw"), date_formats)

    # Combine event_date + event_time if present separately
    if event_ts is None and resolved.get("event_timestamp_raw") and resolved.get("event_time_raw"):
        combined = f"{resolved['event_timestamp_raw']} {resolved['event_time_raw']}"
        event_ts = _parse_datetime_str(combined, date_formats)

    eta = _parse_datetime_str(resolved.get("estimated_arrival_raw"), date_formats)
    etd = _parse_datetime_str(resolved.get("estimated_departure_raw"), date_formats)

    return VesselEvent(
        source_format=SourceFormat.CSV_TERMINAL,
        source_name=source_name,
        vessel_name=_clean(resolved.get("vessel_name")),
        vessel_imo=_clean(resolved.get("vessel_imo")),
        voyage_number=_clean(resolved.get("voyage_number")),
        event_type=event_type,
        event_timestamp=event_ts,
        estimated_arrival=eta,
        estimated_departure=etd,
        port_locode=_clean(resolved.get("port_locode")),
        port_name=_clean(resolved.get("port_name")),
        terminal_code=_clean(resolved.get("terminal_code")),
        terminal_name=_clean(resolved.get("terminal_name")),
        container_number=_clean(resolved.get("container_number")),
        booking_number=_clean(resolved.get("booking_number")),
        bill_of_lading=_clean(resolved.get("bill_of_lading")),
        raw_data={k: v for k, v in raw.items() if not k.startswith("_")},
    )


def _resolve_fields(
    raw: dict[str, Any],
    column_map: dict,
    aliases: dict,
) -> dict[str, Any]:
    """
    Map raw CSV columns to canonical field names.
    First pass: direct column_map lookup.
    Second pass: alias fallback per schema field.
    """
    resolved: dict[str, Any] = {}

    # Direct mapping
    for raw_key, value in raw.items():
        if raw_key.startswith("_"):
            continue
        canonical = column_map.get(raw_key)
        if canonical:
            resolved.setdefault(canonical, value)

    # Alias fallback: for each schema field, check if any alias column exists in raw
    for schema_field, alias_list in aliases.items():
        if schema_field not in resolved:
            for alias in alias_list:
                if alias in raw:
                    resolved[schema_field] = raw[alias]
                    break

    return resolved


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _map_event_type(raw_code: str, mapping: dict) -> EventType:
    if not raw_code:
        return EventType.UNKNOWN
    mapped = mapping.get(raw_code.strip())
    if mapped:
        try:
            return EventType(mapped)
        except ValueError:
            pass
    return EventType.UNKNOWN


def _parse_datetime(
    date_str: Optional[str],
    time_str: Optional[str],
    date_formats: list[str],
    time_formats: list[str],
) -> Optional[datetime]:
    if not date_str:
        return None
    date_str = date_str.strip()
    time_str = (time_str or "").strip()

    combined = f"{date_str} {time_str}".strip() if time_str else date_str

    # Try combined date+time formats first
    for dfmt in date_formats:
        for tfmt in time_formats:
            try:
                return datetime.strptime(combined, f"{dfmt} {tfmt}")
            except ValueError:
                pass

    # Try date-only formats
    for dfmt in date_formats:
        try:
            return datetime.strptime(date_str, dfmt)
        except ValueError:
            pass

    logger.debug("Could not parse date: %s %s", date_str, time_str)
    return None


def _parse_datetime_str(
    raw: Optional[str],
    formats: list[str],
) -> Optional[datetime]:
    if not raw:
        return None
    raw = raw.strip()
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    logger.debug("Could not parse datetime string: %s", raw)
    return None


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned if cleaned else None
