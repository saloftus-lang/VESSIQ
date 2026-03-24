# Architecture

**Analysis Date:** 2026-03-24

## Pattern Overview

**Overall:** Config-Driven Data Translation Pipeline

**Key Characteristics:**
- **Source-agnostic:** Pluggable parsers for different EDI formats (315, 214, 322) and CSV
- **YAML-configured normalization:** Field mapping and status code translation driven by configuration files, not code
- **Unified schema:** All sources normalize to a single `VesselEvent` Pydantic model
- **In-memory event store:** Simple dict-based storage (replaceable with PostgreSQL/Redis)
- **REST API-first:** FastAPI exposes all normalization logic via REST endpoints

## Layers

**Parser Layer:**
- Purpose: Extract raw fields from source-specific formats
- Location: `vessiq/parsers/`
- Contains: Four format-specific parsers (`edi315.py`, `edi214.py`, `edi322.py`, `csv_terminal.py`)
- Depends on: Standard library only (csv, re, io)
- Used by: FastAPI ingest endpoints in `main.py`
- Output: `list[dict[str, Any]]` — raw fields preserved with source formatting intact

**Normalizer Engine:**
- Purpose: Map raw parsed fields → unified `VesselEvent` schema using YAML config
- Location: `vessiq/normalizer/engine.py`
- Contains: Four normalization functions (`normalize_edi315`, `normalize_edi214`, `normalize_edi322`, `normalize_csv_terminal`)
- Depends on: Schema models, YAML config files, utility functions for date/time parsing
- Used by: FastAPI ingest endpoints
- Output: `(list[VesselEvent], list[str])` — normalized events + error messages

**Schema Layer:**
- Purpose: Define unified data model and enums
- Location: `vessiq/schema.py`
- Contains: `VesselEvent` (main model), `EventType` enum, `SourceFormat` enum, response models
- Depends on: Pydantic v2
- Used by: Normalizer, API routes, storage/retrieval logic

**Configuration Layer:**
- Purpose: Store format-specific mapping rules
- Location: `vessiq/config/mappings/`
- Contains: Four YAML files (`edi315.yaml`, `edi214.yaml`, `edi322.yaml`, `csv_terminal.yaml`)
- Structure: field mappings, status code mappings, date/time format hints
- Used by: Normalizer engine (`_load_mapping()`)

**API & Storage Layer:**
- Purpose: Expose normalized events via REST API, maintain in-memory store
- Location: `main.py`
- Contains: FastAPI app, ingest routes, query endpoints, event store dict
- Depends on: All layers above
- Exposes: 5 ingest paths, 2 query endpoints, 1 health check

## Data Flow

**Ingest Flow (any format):**

1. Client POSTs raw data to ingest endpoint (`/ingest/{format}`)
2. Endpoint calls format-specific parser (e.g., `edi315_parser.parse(raw_edi)`)
3. Parser returns `list[dict[str, Any]]` with source-specific field names
4. Endpoint calls format-specific normalizer (e.g., `engine.normalize_edi315(raw_events, source_name)`)
5. Normalizer loads YAML config, maps each raw dict to `VesselEvent`
6. Normalized events + errors returned to endpoint
7. Endpoint stores events in `_event_store[event.event_id] = event`
8. Endpoint returns `IngestResponse` with accepted/rejected counts and event IDs

**Query Flow:**

1. Client GETs `/events` with optional filters (vessel_name, event_type, port_locode, etc.)
2. Endpoint retrieves all events from `_event_store`
3. Applies in-memory filtering on: vessel_name, voyage_number, event_type, source_format, source_name, port_locode, container_number
4. Sorts results by ingested_at descending (newest first)
5. Applies pagination (offset/limit)
6. Returns `EventListResponse` with total count and paginated event list

**State Management:**

- State is held in module-level dict `_event_store: dict[str, VesselEvent]`
- Events are keyed by `event.event_id` (UUID)
- No persistence between server restarts
- For production: replace `_store_events()` and `_event_store` dict with database calls

## Key Abstractions

**VesselEvent Model:**
- Purpose: Represents a single normalized maritime event (arrival, departure, gate-in, container load, etc.)
- Files: `vessiq/schema.py` (lines 41-80)
- Pattern: Pydantic BaseModel with optional fields (most fields can be None)
- Core fields: event_id, source_format, vessel_name, event_type, port_locode, container_number, raw_data
- Design: Preserves original raw_data dict for audit trail; all normalized fields are optional

**EventType Enum:**
- Purpose: Standardized event types across all sources
- Files: `vessiq/schema.py` (lines 18-31)
- Values: ARRIVAL, DEPARTURE, BERTHING, GATE_IN, GATE_OUT, LOADED, DISCHARGED, ETA_UPDATE, ETD_UPDATE, CUSTOMS_RELEASED, AVAILABLE, UNKNOWN
- Used by: All normalizers to map source-specific codes → canonical types

**Parser abstraction:**
- Pattern: Each parser exports a `parse(raw_input)` function returning `list[dict]`
- Example: `edi315_parser.parse(raw_edi_text)` extracts B4, Q2, N9, R4, DTM segments
- CSV parser also has `parse_file(bytes)` variant for file uploads

**Normalizer abstraction:**
- Pattern: Each format has a dedicated `normalize_*()` function and internal `_normalize_*_record()` helper
- Internal logic: Load YAML config, iterate raw dicts, map fields, parse dates, return (events, errors) tuple
- Field resolution: For CSV, uses `_resolve_fields()` to check column_map + aliases for flexible column matching

## Entry Points

**REST API Entry Point:**
- Location: `main.py` (lines 40-48)
- Triggers: HTTP requests to any ingest/query endpoint
- Responsibilities:
  - Mount static frontend at `/` and `/dashboard`
  - Route POST requests to parsers → normalizer → storage
  - Route GET requests to query filters
  - Return JSON responses

**Ingest Routes (4 endpoints):**
- `POST /ingest/edi315`: Lines 104-129 in `main.py`
- `POST /ingest/edi214`: Lines 148-173 in `main.py`
- `POST /ingest/edi322`: Lines 192-217 in `main.py`
- `POST /ingest/csv-terminal`: Lines 235-264 in `main.py`

Each ingest route:
1. Validates input (non-empty)
2. Calls parser
3. Calls normalizer with source_name
4. Stores events via `_store_events()`
5. Logs ingestion metrics
6. Returns `IngestResponse`

**Query Routes (2 endpoints):**
- `GET /events`: Lines 278-312 in `main.py` — list with filters and pagination
- `GET /events/{event_id}`: Lines 321-325 in `main.py` — fetch single event by ID

## Error Handling

**Strategy:** Graceful degradation with error collection

**Patterns:**

1. **Parse-level errors:** Parser attempts best-effort extraction; malformed segments logged but don't crash
2. **Normalization errors:** Each record normalized independently; errors collected in `errors` list without halting batch
3. **API-level errors:** HTTPException raised for:
   - Empty input (400)
   - Parse failures (422)
   - Missing events (404)
4. **Logging:** All errors logged via Python logging at WARNING level with context (record index, detail)
5. **Response:** Client receives both successful events AND errors in single response for transparency

Example from `engine.py` lines 54-61:
```python
for i, raw in enumerate(raw_events):
    try:
        event = _normalize_edi315_record(raw, config, source_name)
        events.append(event)
    except Exception as e:
        msg = f"EDI 315 record {i}: {e}"
        logger.warning(msg)
        errors.append(msg)
```

## Cross-Cutting Concerns

**Logging:**
- Framework: Python stdlib logging
- Level: INFO for ingest summary, WARNING for errors, DEBUG for parse details
- Pattern: Structured messages with context (source name, counts, format)
- Location: All parsers and normalizer log key events

**Validation:**
- Framework: Pydantic v2 (automatic on VesselEvent instantiation)
- Pattern: Type hints on VesselEvent fields enforce structure at normalization time
- Approach: Optional fields allow partial data; required fields (source_format, source_name) enforced

**Authentication:**
- Current: None (health endpoint + ingest are public)
- CORS: Enabled for all origins, methods, headers (lines 50-55 in main.py)
- For production: Add API key validation or JWT before ingest routes

**Date/Time Handling:**
- Timezone: All timestamps in UTC (from `datetime.utcnow()`)
- Parsing: Flexible format detection with fallback chains
- Functions: `_parse_datetime()` (EDI date+time split), `_parse_datetime_str()` (pre-combined strings)
- Formats configurable per source in YAML (edi315.yaml lines 61-70)

---

*Architecture analysis: 2026-03-24*
