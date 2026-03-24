# Technology Stack

**Analysis Date:** 2026-03-24

## Languages

**Primary:**
- Python 3.11+ - Core application logic, data parsers, normalization engine

**Secondary:**
- JavaScript/HTML/CSS - Frontend landing page and dashboard UI (`frontend/` directory)

## Runtime

**Environment:**
- CPython 3.11+
- Uvicorn ASGI server (production)
- Deployment on Railway using NIXPACKS builder

**Package Manager:**
- pip with `requirements.txt` for Python dependencies
- No Node.js or npm (frontend is static HTML/CSS)

**Lockfile:**
- Not present - `requirements.txt` with pinned versions

## Frameworks

**Core:**
- FastAPI 0.115.0 - REST API framework with auto-generated OpenAPI documentation
- Uvicorn[standard] 0.30.6 - ASGI application server (async HTTP server)

**Data Validation & Serialization:**
- Pydantic 2.9.2 - Data validation, schema definition (`VesselEvent`, `EventType` enums)

**Configuration & Parsing:**
- PyYAML 6.0.2 - YAML parsing for field mapping configs (`vessiq/config/mappings/*.yaml`)

**Utilities:**
- python-multipart 0.0.12 - File upload handling (CSV ingest)
- aiofiles 23.2.1 - Async file I/O operations

## Key Dependencies

**Critical:**
- FastAPI - HTTP framework that drives all API routes and request handling
- Pydantic - Validates every normalized event against the `VesselEvent` schema
- PyYAML - Loads mapping configs that drive the normalizer engine (config-driven translation)

**Infrastructure:**
- Uvicorn[standard] - Contains HTTP server + uvloop + httptools for production-grade async performance
- python-multipart - Enables CSV file upload handling at `/ingest/csv-terminal`
- aiofiles - Provides async file operations for the normalizer

## Configuration

**Environment:**
- Railway deployment via `railway.toml`
- Health check endpoint: `/health`
- Port configuration: `${PORT:-8000}` (Railway-injected or defaults to 8000)
- Start command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`

**Build:**
- `railway.toml` - Deployment configuration (NIXPACKS builder, health check path, restart policy)
- `Procfile` - Heroku-compatible process definition for local dev
- CORS middleware enabled for all origins (`allow_origins=["*"]`)

**Mapping Configs:**
- `vessiq/config/mappings/edi315.yaml` - EDI 315 field mappings + status code → event type translations
- `vessiq/config/mappings/edi214.yaml` - EDI 214 shipment status code mappings
- `vessiq/config/mappings/edi322.yaml` - EDI 322 terminal container status code mappings
- `vessiq/config/mappings/csv_terminal.yaml` - CSV column name aliases and event type mappings

## Platform Requirements

**Development:**
- Python 3.11+
- pip
- Text editor/IDE (no build tools required)

**Production:**
- Railway platform (currently hosted)
- 8000 port available (HTTP)
- No external database required (in-memory store — see INTEGRATIONS.md for production notes)

## Logging

**Configuration:**
- Python `logging` module with `basicConfig(level=logging.INFO)`
- Logger in `main.py` logs ingest operations: "EDI 315 ingest: X accepted, Y errors"
- Normalizer engine logs record-level failures as warnings during normalization

## Static Files

**Frontend:**
- `frontend/` directory mounted at `/static` via FastAPI StaticFiles
- Landing page served at `/` → `frontend/index.html`
- Dashboard served at `/dashboard` → `frontend/dashboard.html`

---

*Stack analysis: 2026-03-24*
