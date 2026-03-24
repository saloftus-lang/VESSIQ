# Coding Conventions

**Analysis Date:** 2026-03-24

## Naming Patterns

**Files:**
- Module files are lowercase with underscores: `edi315.py`, `csv_terminal.py`, `edi214.py`, `edi322.py`
- Main entry point: `main.py`
- Schema definition: `schema.py`
- Parser modules grouped in `vessiq/parsers/` directory
- Normalizer engine in `vessiq/normalizer/engine.py`

**Functions:**
- Use snake_case for all function names: `parse_transaction()`, `normalize_edi315()`, `_split_segments()`, `_parse_datetime()`
- Private/internal functions prefixed with underscore: `_get()`, `_elements()`, `_normalize_line_endings()`, `_map_event_type()`
- Public API functions have no prefix
- Utility functions grouped with clear naming: `_parse_datetime()` for datetime operations, `_clean()` for string cleanup

**Variables:**
- snake_case for all variables: `raw_events`, `source_name`, `event_id`, `container_number`
- Module-level constants use uppercase with underscores: `_MAPPINGS_DIR`, `_event_store`, `_FRONTEND`
- Private module variables prefixed with underscore: `_event_store`, `_FRONTEND`
- Loop variables are clear and descriptive: `for i, raw in enumerate(raw_events)` not `for i, r in ...`

**Types:**
- Enums are PascalCase: `EventType`, `SourceFormat`
- Enum values are UPPER_SNAKE_CASE: `ARRIVAL`, `DEPARTURE`, `BERTHING`, `GATE_IN`, `CSV_TERMINAL`
- Pydantic models are PascalCase: `VesselEvent`, `IngestResponse`, `EventListResponse`
- Type hints use modern Python syntax: `list[dict[str, Any]]`, `tuple[list[VesselEvent], list[str]]`

## Code Style

**Formatting:**
- 4-space indentation (Python standard)
- Line length: approximately 100 characters (observed in docstrings and comments)
- No explicit formatter configured (no .prettierrc or black config found)
- Clean, readable structure with sections separated by comment headers with dashes

**Linting:**
- No linter config found (no .eslintrc, pylintrc, or flake8 config)
- Code follows PEP 8 conventions implicitly
- Imports follow standard Python ordering: `from __future__ import` → standard library → third-party → local imports

## Import Organization

**Order (observed pattern):**
1. Future imports: `from __future__ import annotations`
2. Standard library: `import logging`, `from pathlib import Path`, `from typing import Optional`
3. Third-party: `from fastapi import ...`, `from pydantic import ...`, `import yaml`
4. Local imports: `from vessiq.normalizer import engine`, `from vessiq.schema import ...`

**Path Aliases:**
- No alias imports observed; all imports use full module paths: `from vessiq.parsers import edi315 as edi_parser`
- Aliases used for clarity: `from vessiq.parsers import edi315 as edi_parser` (helps distinguish similar parsers)
- Module imports then assigned to local names: `engine.normalize_edi315()`

## Error Handling

**Patterns:**
- Try-except blocks around parsing operations that can fail:
  ```python
  try:
      raw_events = edi_parser.parse(raw_edi)
  except Exception as e:
      raise HTTPException(status_code=422, detail=f"EDI parse error: {e}")
  ```
- Normalization returns tuple of `(events, errors)`: `tuple[list[VesselEvent], list[str]]`
- Errors are collected and logged as warnings, not exceptions:
  ```python
  except Exception as e:
      msg = f"EDI 315 record {i}: {e}"
      logger.warning(msg)
      errors.append(msg)
  ```
- HTTP exceptions used for API validation errors with descriptive messages:
  ```python
  if not raw_edi.strip():
      raise HTTPException(status_code=400, detail="EDI content is empty")
  ```
- Graceful partial failure: some records can fail while others succeed; all are returned to caller

## Logging

**Framework:** Python's built-in `logging` module

**Patterns:**
- Initialize logger per module: `logger = logging.getLogger(__name__)`
- Configured at app startup: `logging.basicConfig(level=logging.INFO)`
- Use `logger.info()` for significant events (ingest counts, source names)
  ```python
  logger.info("EDI 315 ingest: %d accepted, %d errors from %s", len(normalized), len(errors), source_name)
  ```
- Use `logger.warning()` for recoverable errors during normalization
  ```python
  logger.warning(msg)  # where msg = f"EDI 315 record {i}: {e}"
  ```
- Use `logger.debug()` for detailed parsing failures (date parsing, etc.)
  ```python
  logger.debug("Could not parse date: %s %s", date_str, time_str)
  ```
- Use printf-style formatting: `logger.info("format %s %d", var1, var2)` not f-strings

## Comments

**When to Comment:**
- Module docstrings at file top explain purpose and key segments/fields
- Section headers separate logical blocks: `# --- Identity ---`, `# --- Vessel ---`
- Complex parsing logic documented inline with segment field meanings:
  ```python
  # B402: Shipment Status Code  ← the event type code (VE, UV, AV, etc.)
  # B403: Status Date (CCYYMMDD or YYMMDD)
  # B404: Status Time (HHMM)
  data["status_code"] = _get(el, 2)
  ```
- Function docstrings explain input/output contracts:
  ```python
  """
  Normalize a list of raw EDI 315 parsed dicts into VesselEvent objects.

  Returns:
      (events, errors) — successfully normalized events + list of error strings
  """
  ```

**JSDoc/TSDoc:**
- Not used (Python codebase, not TypeScript/JavaScript)
- Docstrings use simple text format describing Args/Returns as needed

## Function Design

**Size:** Functions are concise and focused (typically 5-30 lines)
- Parser entry points: `parse()` function is ~15 lines, delegates to helpers
- Normalizer functions: 10-20 lines, focus on mapping a single record type
- Utility functions: 5-10 lines, single responsibility
- Large complex parsers like EDI 315 parsing broken into many small `_parse_transaction()` and element extraction helpers

**Parameters:**
- Functions take explicit parameters, no **kwargs sprawl
- Parser functions take `raw_edi: str` (content) + optional `source_name: str`
- Normalizer functions take `raw_events: list[dict[str, Any]]` + `source_name: str` + optional config
- Config loaded separately and passed in rather than embedded globally:
  ```python
  def _normalize_edi315_record(raw: dict[str, Any], config: dict, source_name: str) -> VesselEvent:
  ```

**Return Values:**
- Explicit return types: `-> dict[str, Any]`, `-> list[VesselEvent]`, `-> tuple[list[VesselEvent], list[str]]`
- Parsers return raw dicts for normalizer to process
- Normalizers return tuples of (success list, error list) for partial failure handling
- APIs use Pydantic models for structured responses: `IngestResponse`, `EventListResponse`

## Module Design

**Exports:**
- No `__all__` declarations observed
- Public functions are those without underscore prefix
- Main entry point `main.py` imports what it needs directly: `from vessiq.normalizer import engine`
- Each parser module exports its `parse()` function as the public API

**Barrel Files:**
- Empty `__init__.py` files in `vessiq/`, `vessiq/parsers/`, `vessiq/normalizer/` directories
- No re-exports or aggregation at package level
- Direct imports from specific modules required: `from vessiq.parsers import edi315 as edi_parser`

## Configuration

**YAML Mapping Configs:**
- Format: `vessiq/config/mappings/{format_key}.yaml` (e.g., `edi315.yaml`, `csv_terminal.yaml`)
- Structure: `field_map` (raw → canonical), `status_codes` (code → EventType), `date_formats` (list of format strings)
- Loaded at runtime: `_load_mapping("edi315")` returns dict, never cached
- Comment-heavy YAML explaining EDI segment structure and code meanings
- Config-driven normalization: change mappings in YAML without modifying Python code

**Environment Configuration:**
- No `.env` or environment variable configuration in core engine
- FastAPI app receives parameters via Form fields: `source_name: str = Form(...)`
- Logging level set at startup: `logging.basicConfig(level=logging.INFO)`
- No secrets management (file uploads and form data, no API keys in code)

---

*Convention analysis: 2026-03-24*
