# Codebase Concerns

**Analysis Date:** 2026-03-24

## Tech Debt

**In-Memory Event Store Not Production-Ready:**
- Issue: `_event_store` dict in `main.py` (line 72) is an unbounded in-memory dictionary. All ingested events accumulate in RAM with no persistence layer, expiration, or cleanup.
- Files: `main.py:72`, `main.py:75-77`
- Impact:
  - Memory leaks: Events stay in memory until process restart
  - Data loss: All events disappear on deployment or crash
  - No scalability: Can ingest only as many events as RAM allows
  - No data recovery: No audit trail or backup
- Fix approach: Replace with persistent store (PostgreSQL, MongoDB, or Redis). Add schema/migration system. Implement data expiration/archival policy.

**Monolithic In-Memory Store Blocks Multi-Instance Deployment:**
- Issue: The in-memory `_event_store` dict is process-local. Running multiple API instances (horizontal scaling, auto-restart, rolling deploy) means each instance has its own separate event store. Requests to different instances see different data.
- Files: `main.py:72`, `main.py:289` (list_events reads from local dict)
- Impact:
  - Horizontal scaling impossible without session affinity
  - User requests may see "event not found" if routed to different pod/instance
  - Post-deployment, previous instance's data is lost
  - CI/CD deployments cause silent data loss
- Fix approach: Use shared database (PostgreSQL recommended). Ensure Railway/deployment platform can handle stateless instances.

**Insufficient EDI Delimiter Detection Logic:**
- Issue: `_detect_delimiters()` in edi315.py/edi214.py/edi322.py reads fixed positions from ISA segment (lines 55-81 in edi315.py), but relies on hardcoded indices and fallback defaults. EDI messages with malformed ISA headers or non-standard delimiters silently fall back to "~*:" which may not match the actual message.
- Files: `vessiq/parsers/edi315.py:55-81`, `vessiq/parsers/edi214.py`, `vessiq/parsers/edi322.py` (duplicate code)
- Impact:
  - Silent parsing failures: Message parsed incorrectly, fields assigned to wrong positions
  - Data corruption: Container numbers, dates, status codes extracted from wrong segments
  - No error visibility: Logs only debug messages; API returns "accepted" even if data is mangled
  - Carriers sending non-standard EDI variants silently produce wrong normalized events
- Fix approach: Add strict ISA validation. Raise explicit errors for unparseable messages. Add per-carrier delimiter overrides in YAML config. Log warnings for fallback delimiters.

**Unbounded CSV File Upload with No Size Limits:**
- Issue: `ingest_csv_terminal()` endpoint (main.py:235) accepts file uploads without size restrictions. FastAPI's default max upload is unbounded in async context.
- Files: `main.py:235-264`
- Impact:
  - Denial of service: Single 1GB CSV crashes server by exhausting memory
  - Slow queries: Once in-memory store, list_events() with large datasets does O(n) filter loops (line 291-304)
  - No rate limiting: Attacker can saturate API with large uploads
- Fix approach: Add `max_upload_size` parameter to FastAPI. Implement chunked CSV parsing. Add request rate limiting (FastAPI-limiter). Add file size validation before decode.

**No Validation of EDI Message Integrity:**
- Issue: Parsers split transactions by ST/SE markers (edi315.py:93-113) but never validate that segment counts match SE trailer. EDI 315 messages with malformed SE (incorrect segment count) are silently accepted.
- Files: `vessiq/parsers/edi315.py:93-113`, `edi214.py`, `edi322.py`
- Impact:
  - Truncated messages accepted: Parser stops at malformed SE, treats remainder as orphaned
  - Missing status codes: Critical segments (B4, Q2, DTM) may be skipped
  - Silent data loss: No warning in logs; API returns "accepted" for incomplete transactions
- Fix approach: Validate SE segment count. Reject malformed transactions. Add segment audit logging.

**Duplicate EDI Parser Code Across Three Formats:**
- Issue: `edi315.py` (236 lines), `edi214.py` (238 lines), `edi322.py` (254 lines) have nearly identical parsing logic (`_normalize_line_endings`, `_detect_delimiters`, `_split_segments`, `_split_transactions`, `_get` helper). Changes/fixes to one parser require updates in three places.
- Files: `vessiq/parsers/edi315.py`, `edi214.py`, `edi322.py`
- Impact:
  - Maintenance burden: Bug fixes, EDI standard updates require three separate edits
  - Inconsistency risk: Parsers drift as developers update one but forget others
  - Test duplication: Must test same logic in three places
- Fix approach: Extract shared EDI parsing logic into `edi_base.py`. Have specific parsers inherit/call shared functions. Only override segment-specific logic (B4 vs AT7 vs Q5 extraction).

**No Logging of Raw Input Data for Debugging:**
- Issue: When normalization fails, the error message in `engine.py` (lines 54-61) logs only the error text, not the raw dict that failed. For debugging field mapping issues, engineers must ask users to resend data.
- Files: `vessiq/normalizer/engine.py:54-61`, similar in lines 80-87, 106-113, 132-140
- Impact:
  - Slow debugging: Can't diagnose why a specific message failed
  - User friction: Must request raw data from carrier, wait for resend
  - Incomplete telemetry: Logs don't capture failure context
- Fix approach: Add structured logging with raw event dict (truncated for PII). Use `logger.warning(f"EDI 315 record {i}: {e}", extra={"raw_data": raw})` pattern. Consider structured logging library (structlog).

---

## Known Bugs

**CSV Column Name Matching Too Permissive:**
- Symptoms: Typos in CSV header columns silently match wrong fields via aliasing fallback. Example: "vesse_name" (typo) fails to match "vessel_name" and may match "vessel_imo" via alias.
- Files: `vessiq/normalizer/engine.py:352-380` (_resolve_fields function), `csv_terminal.yaml`
- Trigger: Any CSV with misspelled column headers
- Workaround: Strict matching required in mapping config; no typo tolerance
- Fix approach: Add fuzzy matching with confidence threshold. Log warnings for ambiguous alias matches. Validate column headers before normalization.

**DateTime Parsing Returns None Silently for Unparseable Dates:**
- Symptoms: EDI message with status_date="20260399" (invalid date) silently becomes None instead of rejecting the message. Event gets stored with NULL timestamp, breaks any time-based filtering.
- Files: `vessiq/normalizer/engine.py:399-428` (_parse_datetime), `engine.py:431-444` (_parse_datetime_str)
- Trigger: Any malformed date in EDI (YYYYMMDD with invalid day/month)
- Workaround: None — events with NULL timestamps are indistinguishable from real events
- Fix approach: Add configurable strictness: `strict_dates=True` to raise error instead of returning None. Log warnings for unparseable dates. Validate date values before parsing.

---

## Security Considerations

**CORS Configuration Allows All Origins:**
- Risk: `allow_origins=["*"]` (main.py:52) permits requests from any domain. If VESSIQ serves sensitive cargo/vessel data, this exposes data to CSRF attacks and enables cross-site scraping.
- Files: `main.py:50-55`
- Current mitigation: None
- Recommendations:
  1. Change `allow_origins` to explicit list: `["https://vessiq.net", "https://api.vessiq.net"]`
  2. In production, use environment variable: `os.getenv("ALLOWED_ORIGINS", "").split(",")`
  3. Set `allow_credentials=False` to prevent credential leaks via CORS

**No Authentication on API Endpoints:**
- Risk: All endpoints (`/ingest/*`, `/events`) are publicly accessible. Any client can query full cargo manifest or inject fraudulent EDI 315 messages impersonating a carrier.
- Files: `main.py:93-264` (ingest endpoints), `main.py:271-312` (list_events)
- Current mitigation: None
- Recommendations:
  1. Add API key auth: Check `X-API-Key` header, validate against env var
  2. Add Bearer token support for future OAuth2
  3. Restrict `/ingest` endpoints to authenticated clients only (carriers)
  4. Restrict `/events` to authorized users (terminal operators, internal staff)
  5. Implement role-based access control (RBAC): read-only vs ingest

**No Input Validation on source_name and Query Parameters:**
- Risk: `source_name` parameter in ingest endpoints (main.py:106, 150, 194, 237) is accepted verbatim without validation. Attacker can inject arbitrary strings, polluting event records. Query filters (vessel_name, etc.) use case-insensitive substring matching but no length limits.
- Files: `main.py:104-106`, `main.py:278-287`
- Current mitigation: None
- Recommendations:
  1. Whitelist source_name values: `if source_name not in ALLOWED_SOURCES: raise HTTPException(400, "Invalid source")`
  2. Add max length validation: `if len(vessel_name) > 200: raise HTTPException(400, "Query too long")`
  3. Use regex pattern matching instead of substring contains for vessel_name filter
  4. Add rate limiting on `/events` query endpoint to prevent data exfiltration

**Event Store Dump Risk:**
- Risk: The in-memory `_event_store` is a global dict accessible throughout the process. If code is ever compromised or debugger attached, entire cargo manifest is readable.
- Files: `main.py:72`
- Current mitigation: None (in-memory, no encryption)
- Recommendations:
  1. Use persistent encrypted database (PostgreSQL with SSL)
  2. Never hold full events in memory; page from disk
  3. Implement field-level encryption for sensitive data (container numbers, etc.)
  4. Add audit logging of all data access

---

## Performance Bottlenecks

**O(n) Linear Scans for Event Filtering:**
- Problem: `list_events()` endpoint (main.py:289-307) converts entire in-memory dict to list, then filters with Python list comprehensions. With 100K events, every query does 100K comparisons.
- Files: `main.py:289-307`
- Cause: No indexing. In-memory dict with no query engine.
- Improvement path:
  1. Short term: Add in-memory indexing by common query fields (vessel_name, port_locode, event_type)
  2. Long term: Use database with indexes (PostgreSQL B-tree indexes on port_locode, vessel_name, event_type, source_name)
  3. Implement pagination limits (already exist: limit=100) but document that large offsets are slow

**CSV Column Header Normalization Repeated Per Row:**
- Problem: `parse_file()` in csv_terminal.py calls `_normalize_key()` for every column of every row (lines 45-54). For a 10K-row CSV with 30 columns, normalizes 300K keys.
- Files: `vessiq/parsers/csv_terminal.py:45-54`
- Cause: Normalization not cached; happens during parsing instead of once on headers
- Improvement path: Normalize column headers once after reading CSV header row. Map indices instead of re-normalizing each row.

**DateTime Parsing Tries Multiple Formats Per Field:**
- Problem: `_parse_datetime()` (engine.py:399-428) tries all combinations of date_formats × time_formats (nested loops). For 4 date formats × 3 time formats = 12 attempts per field per event.
- Files: `vessiq/normalizer/engine.py:412-418`
- Cause: No detection of actual date format before parsing
- Improvement path: Detect format once per source config (inspect first few rows). Cache format. Use single parse attempt per field.

---

## Fragile Areas

**EDI Segment Extraction Assumes Fixed Element Positions:**
- Files: `vessiq/parsers/edi315.py:142-227`, `edi214.py:~70-200`, `edi322.py:~100+`
- Why fragile: Code uses hardcoded indices like `_get(el, 2)` for status_code, `_get(el, 3)` for status_date. If a carrier's EDI variant reorders elements or omits optional fields, indices shift and extract wrong values.
- Safe modification: Add "segment schema" to YAML config that maps element positions per carrier. Validate actual position count before extract. Use named tuple or dict for segment instead of list indices.
- Test coverage: No unit tests for parser logic. Only integration tests (sample_315.edi) cover happy path.

**YAML Config Mapping Not Validated at Startup:**
- Files: `vessiq/normalizer/engine.py:31-37` (_load_mapping)
- Why fragile: Mappings are lazy-loaded on first ingest request. If edi315.yaml is malformed or missing a required field, API doesn't fail until a customer sends EDI 315 data.
- Safe modification: Add startup validation. Load all mapping files at app startup (main.py). Validate schema (required keys: field_map, status_codes, date_formats). Fail fast if config is invalid.
- Test coverage: None

**No Null Safety on Dictionary Lookups:**
- Files: `vessiq/normalizer/engine.py` throughout (lines 185-196, 232-237, 281-295, etc.)
- Why fragile: Code assumes raw.get() returns string or None, but could get dict, list, or int if parser misbehaves. Calling .strip() on non-string causes AttributeError at runtime.
- Safe modification: Add type checking: `if isinstance(vessel_name, str): vessel_name = vessel_name.strip()`
- Test coverage: None

---

## Scaling Limits

**In-Memory Store Limited by Server RAM:**
- Current capacity: Assumes ~8GB RAM instance. At ~1KB per event JSON, max ~8M events before OOM
- Limit: Scales vertically only (bigger servers). Horizontal scaling (multiple API instances) requires shared database
- Scaling path: Implement PostgreSQL backend (handles 10B+ events efficiently). Use connection pooling (pgbounce). Shard if needed (but unlikely before 1B events)

**CSV Upload Parser Loads Entire File into Memory:**
- Current capacity: Safe for CSVs <100MB. Beyond that, memory pressure
- Limit: Framework limit ~ 1GB (FastAPI default max request size)
- Scaling path: Implement streaming CSV parser. Read file in chunks, normalize 1000 rows at a time, write to DB batch. Avoid holding entire CSV in memory.

---

## Dependencies at Risk

**PyYAML Safety:**
- Risk: `yaml.safe_load()` used in engine.py:37 is safe (doesn't execute code), but vulnerable to billion-laughs denial-of-attack if config files grow large. No YAML schema validation.
- Impact: Attacker could inject massive YAML file to exhaust memory during startup
- Migration plan: Use `strictyaml` library or validate YAML schema at load time. Set max YAML size limit.

**python-multipart Version May Have Security Issues:**
- Risk: `python-multipart==0.0.12` is from 2023. No pinned patch version. May have unpatched CVEs
- Impact: File upload exploits
- Migration plan: Update to latest patch: `python-multipart>=0.0.18`. Run `pip-audit` in CI to detect CVE versions.

**No Dependency Auditing in CI:**
- Risk: requirements.txt is static. No automated checks for CVEs in production
- Impact: Vulnerable dependencies silently deployed to production
- Migration plan: Add `pip-audit` or `safety` to CI. Fail build if CVEs found. Run `pip list --outdated` regularly.

---

## Missing Critical Features

**No Duplicate Detection:**
- Problem: API has no deduplication logic. If the same EDI 315 is ingested twice, two separate VesselEvent records are created with different event_ids. Leads to duplicate cargo manifests, double-counting, and user confusion.
- Blocks: Reliable cargo tracking, financial accuracy, supply chain visibility
- Fix approach: Add deduplication key based on source_format + source_name + raw_data hash. Check before storing. Return existing event_id if duplicate.

**No Data Retention / Expiration Policy:**
- Problem: Events never expire. Old EDI messages from 2020 stay in database forever. No retention configuration.
- Blocks: Compliance (GDPR, data minimization), storage cost control, performance optimization
- Fix approach: Add configurable TTL per source format. Delete events older than N days. Add "soft delete" (marked as archived, not queried) instead of hard delete for audit trail.

**No Error Detail in Rejection Responses:**
- Problem: `ingest_edi315` returns `errors: ["EDI 315 record 5: ..."]` but doesn't include which field failed, what the invalid value was, or how to fix it. User gets unhelpful error.
- Blocks: User self-service debugging, carrier integration troubleshooting
- Fix approach: Return structured error details: `{record_index: 5, field: "status_date", raw_value: "20260399", error: "Invalid date format", suggestion: "Use YYYYMMDD format"}`

**No Event Schema Versioning:**
- Problem: VesselEvent schema will evolve (add new fields, enum values). Once v2 schema is deployed, old clients still send v1 format, or v2 events break v1 consumers.
- Blocks: Backward-compatible upgrades, multi-version API support
- Fix approach: Add `schema_version` field to VesselEvent. Implement migration layer. Document version policy (support last 2 major versions).

**No Webhook / Push Notification System:**
- Problem: Users must poll `/events` endpoint to see new events. No callback mechanism for real-time updates.
- Blocks: Real-time supply chain visibility, event-driven workflows
- Fix approach: Add webhooks: POST to registered URLs when events created. Use message queue (Redis, RabbitMQ) to decouple publishing from subscriber latency.

---

## Test Coverage Gaps

**No Unit Tests for Parsers:**
- What's not tested: `_detect_delimiters()`, `_split_transactions()`, `_parse_transaction()` logic in edi315/214/322 and csv_terminal
- Files: `vessiq/parsers/edi315.py`, `edi214.py`, `edi322.py`, `csv_terminal.py`
- Risk: Subtle bugs in delimiter detection or segment extraction silently produce wrong events
- Priority: High — parsers are critical path for data correctness

**No Unit Tests for Normalizer:**
- What's not tested: `_normalize_edi315_record()`, `_parse_datetime()`, `_resolve_fields()`, field mapping logic
- Files: `vessiq/normalizer/engine.py`
- Risk: Field mappings produce NULL values, dates fail to parse, missing field handling untested
- Priority: High — normalizer is where data transforms happen

**No Integration Tests:**
- What's not tested: End-to-end ingest→normalize→query flow using sample_315.edi, sample_214.edi, sample_322.edi, sample_terminal.csv
- Files: No test files found in repo
- Risk: New changes break API contract without detection
- Priority: Medium — at minimum, smoke tests for happy path

**No Error Case Tests:**
- What's not tested: Malformed EDI (missing segments, wrong delimiters), invalid CSV (bad encoding, missing headers), null fields, edge case dates (leap years, Y2K), boundary conditions (empty containers, null vessel_imo)
- Risk: Assumed error handling is untested and breaks in production
- Priority: Medium

**No Performance/Load Tests:**
- What's not tested: How many events can be ingested before OOM? How fast does list_events() respond with 100K records? Can CSV upload handle 100MB file?
- Risk: Scaling limits unknown until production incident
- Priority: Low (for MVP, but required before launch)

---

*Concerns audit: 2026-03-24*
