# VESSIQ — Normalization & Translation Engine

## What this project is
VESSIQ is a data normalization and translation layer for maritime/logistics data.
It ingests raw vessel event data from multiple formats (EDI 315, CSV terminal exports),
normalizes it into a single unified JSON schema, and exposes it via a REST API.

Think: Plaid for maritime data.

## Architecture

```
Raw Data (EDI 315 / CSV)
        │
        ▼
   Parsers (vessiq/parsers/)
        │  Extract raw fields from each format
        ▼
   Normalizer (vessiq/normalizer/engine.py)
        │  Maps raw fields → unified VesselEvent schema
        │  Driven by YAML config (vessiq/config/mappings/)
        ▼
   Schema (vessiq/schema.py)
        │  Pydantic-validated VesselEvent objects
        ▼
   REST API (main.py)
        │  FastAPI endpoints for ingest + retrieval
        ▼
   Normalized JSON output
```

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app entry point — all API routes |
| `vessiq/schema.py` | Pydantic models: `VesselEvent`, `EventType` enum |
| `vessiq/parsers/edi315.py` | Parses raw EDI X12 315 text into dicts |
| `vessiq/parsers/csv_terminal.py` | Parses CSV terminal export files |
| `vessiq/normalizer/engine.py` | Maps parsed dicts → VesselEvent using YAML config |
| `vessiq/config/mappings/edi315.yaml` | Field mapping config for EDI 315 sources |
| `vessiq/config/mappings/csv_terminal.yaml` | Field mapping config for CSV terminal sources |
| `sample_data/sample_315.edi` | Realistic EDI 315 sample (Maersk → Pasha format) |
| `sample_data/sample_terminal.csv` | Realistic terminal CSV export sample |

## Running the API

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs auto-generated at: http://localhost:8000/docs

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ingest/edi315` | Ingest raw EDI 315 text body |
| POST | `/ingest/csv-terminal` | Ingest CSV file upload |
| GET | `/events` | List all normalized events (filterable) |
| GET | `/events/{event_id}` | Get a single event by ID |
| GET | `/health` | Health check |

## Adding a New Data Source

1. Create a new parser in `vessiq/parsers/your_source.py`
   - Must return a `list[dict]` of raw field dicts
2. Create a mapping config in `vessiq/config/mappings/your_source.yaml`
   - Follow the pattern in `edi315.yaml` or `csv_terminal.yaml`
3. Add a new ingest route in `main.py`
4. The normalizer engine will handle the rest automatically

## Unified Schema Fields

Every event, regardless of source, is normalized to a `VesselEvent` with:
- `event_id`, `source_format`, `source_name`, `ingested_at`
- `vessel_name`, `vessel_imo`, `voyage_number`
- `event_type` (ARRIVAL, DEPARTURE, BERTHING, GATE_IN, GATE_OUT, LOADED, DISCHARGED, ETA_UPDATE, ETD_UPDATE, CUSTOMS_RELEASED, AVAILABLE, UNKNOWN)
- `event_timestamp`, `estimated_arrival`, `estimated_departure`
- `port_locode`, `port_name`, `terminal_code`, `terminal_name`
- `container_number`, `booking_number`, `bill_of_lading`
- `raw_data` (original parsed fields preserved)

## Development Notes

- Python 3.11+
- FastAPI + Uvicorn for the API server
- Pydantic v2 for schema validation
- PyYAML for mapping configs
- In-memory event store (replace with PostgreSQL/Redis for production)
- The normalizer is config-driven: add new field mappings in YAML without touching Python code
