# External Integrations

**Analysis Date:** 2026-03-24

## APIs & External Services

**None detected** - VESSIQ is a self-contained data normalization layer with no external API integrations. All parsing and normalization happens internally.

## Data Storage

**Databases:**
- None in production code - In-memory dictionary used for event storage
  - Location: `main.py` line 72 - `_event_store: dict[str, VesselEvent] = {}`
  - Current approach: Single-process, ephemeral storage (data lost on restart)
  - **Production Note:** Replace with PostgreSQL/Redis (commented in code)

**File Storage:**
- Local filesystem only - Sample data and mapping configs stored on disk
  - Sample EDI files: `sample_data/sample_315.edi`, `sample_data/sample_terminal.csv`
  - Config files: `vessiq/config/mappings/*.yaml`
  - Frontend assets: `frontend/` directory

**Caching:**
- None - Mapping configs loaded from disk on each ingest call (`engine.py` line 36)

## Data Ingest Sources

**EDI X12 Formats:**
- EDI 315 (Ocean Shipment Status)
  - Ingest endpoint: `POST /ingest/edi315`
  - Parser: `vessiq/parsers/edi315.py`
  - Mapping config: `vessiq/config/mappings/edi315.yaml`
  - Status: Implemented and tested

- EDI 214 (Transportation Carrier Shipment Status Message)
  - Ingest endpoint: `POST /ingest/edi214`
  - Parser: `vessiq/parsers/edi214.py`
  - Mapping config: `vessiq/config/mappings/edi214.yaml`
  - Status: Implemented for Pasha rail pilot (March 2026)

- EDI 322 (Terminal Operations / Intermodal Container Status)
  - Ingest endpoint: `POST /ingest/edi322`
  - Parser: `vessiq/parsers/edi322.py`
  - Mapping config: `vessiq/config/mappings/edi322.yaml`
  - Status: Implemented for Pasha rail pilot (March 2026)

**CSV Terminal Exports:**
- CSV Terminal Operating System (TOS) export files
  - Ingest endpoint: `POST /ingest/csv-terminal`
  - Parser: `vessiq/parsers/csv_terminal.py`
  - Mapping config: `vessiq/config/mappings/csv_terminal.yaml`
  - Flexible column name matching (aliases for common TOS variants)

## Authentication & Identity

**Auth Provider:**
- None - API is open (CORS allows all origins)
- Endpoints are unauthenticated and publicly accessible

**Note:** For production deployment with restricted access, add authentication middleware (JWT, API keys, etc.)

## Monitoring & Observability

**Error Tracking:**
- None - Errors logged to Python logger only

**Logs:**
- Python `logging` module at INFO level
- Ingest operations logged with counts: "EDI 315 ingest: X accepted, Y errors from [source_name]"
- Normalization errors logged as warnings (record-level failures included in response)
- No external log aggregation (stdout only)

**Health Check:**
- Endpoint: `GET /health`
- Returns: `{"status": "ok", "events_stored": int}`
- Used by Railway for liveness checks (`railway.toml` line 6)

## CI/CD & Deployment

**Hosting:**
- Railway platform (deployment configured in `railway.toml`)
- NIXPACKS builder (language detection + automatic dependency management)
- Region: Default Railway region

**CI Pipeline:**
- None detected - No GitHub Actions, GitLab CI, or similar
- Deployments triggered via git push to Railway
- Health check: `/health` endpoint polled by Railway

**Deployment Configuration:**
- Start command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`
- Restart policy: `ON_FAILURE` with max 3 retries
- Port: Environment variable `PORT` or 8000

## Environment Configuration

**Environment Variables:**
- `PORT` - HTTP port (default 8000, set by Railway)
- No application-specific env vars detected
- No secrets management in place

**Secrets Location:**
- No `.env` file in codebase
- No external secrets service integrated
- **Note:** For production, add secrets management (Railway environment variables, Vault, etc.)

## API Query Capabilities

**Event Retrieval:**
- List events with filtering: `GET /events`
  - Filters: vessel_name, voyage_number, event_type, source_format, source_name, port_locode, container_number
  - Pagination: limit (1-1000, default 100), offset
  - Results sorted by ingested_at descending

- Get single event: `GET /events/{event_id}`
  - Returns full `VesselEvent` object or 404

## Data Flow & Integration Pattern

**Ingest Flow:**
1. Raw data arrives at one of four ingest endpoints (EDI 315/214/322 or CSV)
2. Format-specific parser extracts fields into `dict[str, Any]`
3. Normalizer engine loads YAML mapping config and transforms raw dict → `VesselEvent`
4. Validated events stored in `_event_store` (in-memory dict)
5. Response includes: acceptance count, rejection count, event IDs, error messages

**Query Flow:**
1. Client calls `GET /events` with optional filters
2. In-memory store filtered in-process (no database queries)
3. Results paginated and returned as `EventListResponse` JSON

## Future Integration Points

**Recommended for production:**
- PostgreSQL for persistent event storage
- Redis for mapping config caching
- External authentication (JWT, OAuth2, API key middleware)
- Log aggregation service (CloudWatch, Datadog, Splunk)
- Error tracking (Sentry)
- Message queue (RabbitMQ, Kafka) for async ingest at scale

---

*Integration audit: 2026-03-24*
