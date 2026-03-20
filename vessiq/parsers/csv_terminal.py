"""
CSV Terminal Export Parser
--------------------------
Parses CSV files exported from terminal operating systems (TOS) such as
Navis N4, SPARCS, or custom terminal portal exports.

Terminal CSVs are notoriously inconsistent — different terminals use different
column names for the same data. This parser handles that via the YAML mapping
config (csv_terminal.yaml), which maps source column names to canonical field names.

This parser returns raw dicts keyed by the original column headers.
The normalizer engine then applies the YAML mapping to produce VesselEvent objects.
"""

from __future__ import annotations

import csv
import io
from typing import Any


def parse(raw_csv: str, source_name: str = "UNKNOWN") -> list[dict[str, Any]]:
    """
    Parse a raw CSV string into a list of row dicts.

    Each dict contains:
      - All original columns (lowercased keys, stripped values)
      - _source_name: the provided source identifier
      - _row_index: 0-based row number for traceability

    Args:
        raw_csv:     Raw CSV text content
        source_name: Identifier for the terminal/source, e.g. "PASHA_HONOLULU"

    Returns:
        List of raw row dicts, one per data row.
    """
    raw_csv = raw_csv.strip()
    if not raw_csv:
        return []

    reader = csv.DictReader(io.StringIO(raw_csv))
    rows = []

    for i, row in enumerate(reader):
        # Normalize keys: lowercase, strip whitespace, replace spaces with underscores
        normalized = {
            _normalize_key(k): v.strip() if isinstance(v, str) else v
            for k, v in row.items()
            if k is not None
        }
        normalized["_source_name"] = source_name
        normalized["_row_index"] = i
        rows.append(normalized)

    return rows


def parse_file(file_content: bytes, source_name: str = "UNKNOWN") -> list[dict[str, Any]]:
    """Parse CSV from raw bytes (e.g. from a file upload)."""
    # Try UTF-8 first, fall back to latin-1 (common in legacy terminal exports)
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = file_content.decode(encoding)
            return parse(text, source_name)
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode CSV file — unsupported encoding")


def _normalize_key(key: str) -> str:
    """Lowercase and underscore-ify a column header for consistent matching."""
    if not key:
        return "_empty"
    return key.strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_")
