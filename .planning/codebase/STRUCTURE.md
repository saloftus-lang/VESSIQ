# Codebase Structure

**Analysis Date:** 2026-03-24

## Directory Layout

```
/Users/seanloftus/Desktop/VESSIQ/
├── main.py                           # FastAPI app entry point — all API routes
├── requirements.txt                  # Python package dependencies
├── Procfile                          # Deployment config (Railway)
├── railway.toml                      # Railway platform config
├── CLAUDE.md                         # Project documentation
│
├── vessiq/                           # Core package (data translation layer)
│   ├── __init__.py
│   ├── schema.py                     # Pydantic models: VesselEvent, EventType, SourceFormat
│   ├── parsers/                      # Format-specific parsers
│   │   ├── __init__.py
│   │   ├── edi315.py                 # EDI X12 315 (Ocean Shipment Status) parser
│   │   ├── edi214.py                 # EDI X12 214 (Carrier Shipment Status) parser
│   │   ├── edi322.py                 # EDI X12 322 (Terminal Operations) parser
│   │   └── csv_terminal.py           # CSV terminal export parser
│   ├── normalizer/                   # Unified normalization engine
│   │   ├── __init__.py
│   │   └── engine.py                 # Maps raw fields → VesselEvent using YAML config
│   └── config/                       # Configuration files
│       ├── __init__.py
│       └── mappings/                 # YAML mapping configs (source-specific)
│           ├── edi315.yaml           # EDI 315 field mappings + status codes
│           ├── edi214.yaml           # EDI 214 field mappings + status codes
│           ├── edi322.yaml           # EDI 322 field mappings + status codes
│           └── csv_terminal.yaml     # CSV column mappings + aliases
│
├── sample_data/                      # Example data for testing
│   ├── sample_315.edi                # Sample EDI 315 message (Maersk format)
│   ├── sample_214.edi                # Sample EDI 214 message
│   ├── sample_322.edi                # Sample EDI 322 message
│   └── sample_terminal.csv           # Sample terminal CSV export
│
├── frontend/                         # Static HTML landing page + dashboard
│   ├── index.html                    # Landing page (served at /)
│   └── dashboard.html                # Dashboard page (served at /dashboard)
│
├── .planning/                        # GSD planning artifacts (this file)
│   └── codebase/
│       └── *.md                      # Analysis documents
│
└── demo/, marketing/, frontend-dev-workspace/  # Auxiliary frontend work (not part of core API)
```

## Directory Purposes

**`/Users/seanloftus/Desktop/VESSIQ/`:**
- Purpose: Project root — contains API entry point and all code
- Contains: Main FastAPI app, package manifest, deployment config
- Key files: `main.py`, `requirements.txt`, `CLAUDE.md`

**`vessiq/`:**
- Purpose: Core Python package for data normalization
- Contains: Schema definitions, parsers, normalizer engine, configuration
- Key responsibility: All data translation logic lives here

**`vessiq/parsers/`:**
- Purpose: Format-specific raw data extraction
- Contains: Four parser modules — one per supported EDI/CSV format
- Pattern: Each parser exports `parse()` function → `list[dict]`
- Design: Parsers extract raw fields; they don't normalize or validate

**`vessiq/normalizer/`:**
- Purpose: YAML-driven field mapping and schema normalization
- Contains: Single `engine.py` with four `normalize_*()` functions
- Dependencies: `schema.py`, YAML mappings, date/time utilities
- Key responsibility: Bridge raw parsed dicts → unified VesselEvent

**`vessiq/config/mappings/`:**
- Purpose: Store format-specific translation rules (no Python code)
- Contains: Four YAML files — one per format
- Structure: field_map (raw → canonical), status_codes (source codes → EventType), format hints
- Modification: Change YAML to support new carriers/formats without touching Python

**`sample_data/`:**
- Purpose: Realistic sample inputs for manual testing and development
- Contains: One example file per supported format
- Usage: Test ingest endpoints via API docs or curl
- Format: Raw EDI text + CSV export — same as production inputs

**`frontend/`:**
- Purpose: Serve HTML UI (landing page + dashboard)
- Contains: Two static HTML files served at `/` and `/dashboard`
- Integration: Mounted at StaticFiles in `main.py` line 59
- Note: HTML uses inline CSS/JS; no separate build process

## Key File Locations

**Entry Points:**
- `main.py`: FastAPI application setup, all API routes (ingest + query)
- `frontend/index.html`: Landing page (GET `/`)
- `frontend/dashboard.html`: Dashboard (GET `/dashboard`)

**Configuration:**
- `requirements.txt`: Python package versions
- `CLAUDE.md`: Developer documentation (architecture overview)
- `railway.toml`: Deployment platform config
- `Procfile`: Process manager config for running uvicorn

**Core Logic:**
- `vessiq/schema.py`: Pydantic models defining unified VesselEvent schema
- `vessiq/normalizer/engine.py`: Core translation logic (4 normalize functions + 7 utilities)
- `vessiq/parsers/*.py`: Four format-specific extraction modules

**Data Mapping:**
- `vessiq/config/mappings/edi315.yaml`: Maps EDI 315 status codes → EventType (35 code mappings)
- `vessiq/config/mappings/edi214.yaml`: Maps EDI 214 status codes → EventType
- `vessiq/config/mappings/edi322.yaml`: Maps EDI 322 status codes → EventType
- `vessiq/config/mappings/csv_terminal.yaml`: Maps CSV column names + aliases → schema fields

**Testing/Examples:**
- `sample_data/sample_315.edi`: Complete EDI 315 transaction set (897 bytes)
- `sample_data/sample_214.edi`: Complete EDI 214 message (2.4 KB)
- `sample_data/sample_322.edi`: Complete EDI 322 message (4.6 KB)
- `sample_data/sample_terminal.csv`: Terminal export with 5 columns + sample rows (1.4 KB)

## Naming Conventions

**Files:**
- Python modules: `lowercase_with_underscores.py` (e.g., `edi315.py`, `csv_terminal.py`)
- YAML configs: `lowercase_with_underscores.yaml` (e.g., `edi322.yaml`)
- HTML files: `lowercase_with_underscores.html` (e.g., `index.html`, `dashboard.html`)

**Directories:**
- Package dirs: `lowercase` (e.g., `parsers`, `normalizer`, `config`)
- Logical groupings: `feature_noun` (e.g., `config/mappings`, `frontend-dev-workspace`)

**Functions/Classes:**
- Functions: `snake_case` (e.g., `parse_file`, `normalize_edi315`, `_clean`)
- Classes: `PascalCase` (e.g., `VesselEvent`, `EventType`, `SourceFormat`)
- Private functions: Prefix with `_` (e.g., `_normalize_edi315_record`, `_parse_datetime`)

**Variables/Constants:**
- Module-level: `CONSTANT_CASE` for true constants (e.g., `_MAPPINGS_DIR`, `_FRONTEND`)
- Local: `snake_case` (e.g., `raw_events`, `events`, `status_code`)
- Enum values: `UPPER_CASE` (e.g., `EventType.ARRIVAL`, `SourceFormat.EDI_315`)

**Database/API:**
- Event IDs: UUID format (generated by `str(uuid.uuid4())`)
- Field names in JSON: `snake_case` (e.g., `event_id`, `vessel_name`, `port_locode`)
- Query parameters: `snake_case` (e.g., `?vessel_name=...`, `?event_type=...`)

## Where to Add New Code

**New EDI Format (e.g., EDI 210 - Invoice):**

1. **Create parser:** `vessiq/parsers/edi210.py`
   - Export `parse(raw_edi: str) -> list[dict]`
   - Follow pattern from `edi315.py`: detect delimiters, split segments, extract relevant fields
   - Return raw dicts with EDI-specific field names

2. **Create mapping config:** `vessiq/config/mappings/edi210.yaml`
   - Copy structure from `edi315.yaml` or `edi214.yaml`
   - Define `status_codes` mapping from EDI segments → EventType
   - Define `date_formats` and `time_formats` for parsing

3. **Add normalizer function:** Add to `vessiq/normalizer/engine.py`
   - Copy `normalize_edi315()` pattern (lines 40-63)
   - Create `_normalize_edi210_record()` helper (lines 149-198)
   - Register function in module exports

4. **Add API route:** Add to `main.py`
   - Copy pattern from lines 93-129 (edi315) or 180-217 (edi322)
   - Create `@app.post("/ingest/edi210", ...)` endpoint
   - Call your new parser + normalizer function
   - Store events + return IngestResponse

5. **Add sample data:** `sample_data/sample_210.edi`
   - Realistic example for manual testing

**New CSV-like Format (e.g., Excel terminal export):**

1. **Extend CSV parser:** Modify `vessiq/parsers/csv_terminal.py`
   - Add variant function or parameter for Excel handling
   - Return same `list[dict]` format with normalized keys

2. **Create/extend mapping:** `vessiq/config/mappings/csv_terminal.yaml` (or new `csv_excel.yaml`)
   - Define column aliases for new format variants
   - Add to `column_aliases` section with Excel column names

3. **Add API route:** `main.py`
   - Create `@app.post("/ingest/csv-excel", ...)`
   - Use `normalize_csv_terminal()` with different source_name

**New Field/Property in VesselEvent:**

1. **Update schema:** `vessiq/schema.py` (lines 41-80)
   - Add field to `VesselEvent` class with Optional[Type] and description
   - Example: `container_size: Optional[str] = None`

2. **Update all mapping configs:** `vessiq/config/mappings/*.yaml`
   - Add entry to `field_map` section mapping source field → new field

3. **Update normalizers:** `vessiq/normalizer/engine.py`
   - Add extraction in `_normalize_*_record()` functions
   - Map from raw dict to VesselEvent field in constructor call

4. **Update tests:** Add coverage for new field in test data

**New Query Filter in `/events` endpoint:**

1. **Update route:** `main.py` (lines 278-312)
   - Add Query parameter with type and description
   - Add filter condition in results list comprehension

2. **Example:** To filter by `estimated_arrival`:
   ```python
   estimated_arrival_before: Optional[datetime] = Query(default=None, ...)
   if estimated_arrival_before:
       results = [e for e in results if e.estimated_arrival and e.estimated_arrival <= estimated_arrival_before]
   ```

## Special Directories

**`vessel/config/mappings/`:**
- Purpose: YAML configuration files for field translation
- Generated: No (manually maintained)
- Committed: Yes (essential for production)
- Modification: Add/edit YAML to support new carriers without code changes

**`sample_data/`:**
- Purpose: Test inputs — NOT production data
- Generated: No (manually created samples)
- Committed: Yes (reference for testing)
- Usage: Copy/paste into API docs to test manually

**`frontend/`:**
- Purpose: Static HTML UI
- Generated: No (manually written)
- Committed: Yes (deployed with API)
- Served by: FastAPI StaticFiles middleware (line 59 in main.py)

**`.planning/codebase/`:**
- Purpose: GSD documentation artifacts
- Generated: Yes (by GSD agents)
- Committed: Yes (for planning context)
- Contents: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, etc.

---

*Structure analysis: 2026-03-24*
