"""
VESSIQ REST API
---------------
FastAPI application exposing the VESSIQ normalization engine as a REST API.

Endpoints:
  POST /ingest/edi315          — Ingest raw EDI 315 text
  POST /ingest/csv-terminal    — Ingest CSV terminal export (file upload)
  GET  /events                 — List all normalized events (with filters)
  GET  /events/{event_id}      — Get a single event by ID
  GET  /health                 — Health check

Auto-generated docs: http://localhost:8000/docs

Run with:
  uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from vessiq.normalizer import engine
from vessiq.parsers import csv_terminal as csv_parser
from vessiq.parsers import edi315 as edi_parser
from vessiq.parsers import edi214 as edi214_parser
from vessiq.parsers import edi322 as edi322_parser
from vessiq.schema import EventListResponse, EventType, IngestResponse, SourceFormat, VesselEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VESSIQ Normalization API",
    description=(
        "Maritime data translation and normalization layer. "
        "Ingests raw EDI 315 and terminal CSV data, normalizes it into a "
        "unified vessel event schema, and exposes it via REST API."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the landing page at /
_FRONTEND = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=_FRONTEND), name="static")

@app.get("/", include_in_schema=False)
def landing():
    return FileResponse(_FRONTEND / "index.html")

@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(_FRONTEND / "dashboard.html")

# ---------------------------------------------------------------------------
# In-memory event store (replace with PostgreSQL/Redis in production)
# ---------------------------------------------------------------------------
_event_store: dict[str, VesselEvent] = {}


def _store_events(events: list[VesselEvent]) -> None:
    for event in events:
        _event_store[event.event_id] = event


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "events_stored": len(_event_store)}


# ---------------------------------------------------------------------------
# Ingest — EDI 315
# ---------------------------------------------------------------------------

@app.post(
    "/ingest/edi315",
    response_model=IngestResponse,
    tags=["Ingest"],
    summary="Ingest raw EDI X12 315 message",
    description=(
        "Accepts a raw EDI 315 text body (may contain multiple ST/SE transaction sets). "
        "Parses, normalizes, and stores each vessel event. "
        "Returns the IDs of accepted events."
    ),
)
async def ingest_edi315(
    raw_edi: str = Form(..., description="Raw EDI 315 text content"),
    source_name: str = Form(default="EDI_SOURCE", description="Identifier for the sending carrier/system"),
):
    if not raw_edi.strip():
        raise HTTPException(status_code=400, detail="EDI content is empty")

    try:
        raw_events = edi_parser.parse(raw_edi)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"EDI parse error: {e}")

    if not raw_events:
        raise HTTPException(status_code=422, detail="No valid EDI 315 transactions found in input")

    normalized, errors = engine.normalize_edi315(raw_events, source_name=source_name)
    _store_events(normalized)

    logger.info("EDI 315 ingest: %d accepted, %d errors from %s", len(normalized), len(errors), source_name)

    return IngestResponse(
        accepted=len(normalized),
        rejected=len(errors),
        event_ids=[e.event_id for e in normalized],
        errors=errors,
    )


# ---------------------------------------------------------------------------
# Ingest — EDI 214
# ---------------------------------------------------------------------------

@app.post(
    "/ingest/edi214",
    response_model=IngestResponse,
    tags=["Ingest"],
    summary="Ingest raw EDI X12 214 message",
    description=(
        "Accepts a raw EDI 214 (Transportation Carrier Shipment Status Message) "
        "text body (may contain multiple ST/SE transaction sets). "
        "Parses, normalizes, and stores each shipment status event. "
        "Returns the IDs of accepted events."
    ),
)
async def ingest_edi214(
    raw_edi: str = Form(..., description="Raw EDI 214 text content"),
    source_name: str = Form(default="EDI_214_SOURCE", description="Identifier for the sending carrier/system"),
):
    if not raw_edi.strip():
        raise HTTPException(status_code=400, detail="EDI content is empty")

    try:
        raw_events = edi214_parser.parse(raw_edi)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"EDI parse error: {e}")

    if not raw_events:
        raise HTTPException(status_code=422, detail="No valid EDI 214 transactions found in input")

    normalized, errors = engine.normalize_edi214(raw_events, source_name=source_name)
    _store_events(normalized)

    logger.info("EDI 214 ingest: %d accepted, %d errors from %s", len(normalized), len(errors), source_name)

    return IngestResponse(
        accepted=len(normalized),
        rejected=len(errors),
        event_ids=[e.event_id for e in normalized],
        errors=errors,
    )


# ---------------------------------------------------------------------------
# Ingest — EDI 322
# ---------------------------------------------------------------------------

@app.post(
    "/ingest/edi322",
    response_model=IngestResponse,
    tags=["Ingest"],
    summary="Ingest raw EDI X12 322 message",
    description=(
        "Accepts a raw EDI 322 (Terminal Operations / Intermodal Container Status) "
        "text body (may contain multiple ST/SE transaction sets). "
        "Parses, normalizes, and stores each container status event. "
        "Returns the IDs of accepted events."
    ),
)
async def ingest_edi322(
    raw_edi: str = Form(..., description="Raw EDI 322 text content"),
    source_name: str = Form(default="EDI_322_SOURCE", description="Identifier for the sending railroad/yard system"),
):
    if not raw_edi.strip():
        raise HTTPException(status_code=400, detail="EDI content is empty")

    try:
        raw_events = edi322_parser.parse(raw_edi)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"EDI parse error: {e}")

    if not raw_events:
        raise HTTPException(status_code=422, detail="No valid EDI 322 transactions found in input")

    normalized, errors = engine.normalize_edi322(raw_events, source_name=source_name)
    _store_events(normalized)

    logger.info("EDI 322 ingest: %d accepted, %d errors from %s", len(normalized), len(errors), source_name)

    return IngestResponse(
        accepted=len(normalized),
        rejected=len(errors),
        event_ids=[e.event_id for e in normalized],
        errors=errors,
    )


# ---------------------------------------------------------------------------
# Ingest — CSV Terminal Export
# ---------------------------------------------------------------------------

@app.post(
    "/ingest/csv-terminal",
    response_model=IngestResponse,
    tags=["Ingest"],
    summary="Ingest CSV terminal export file",
    description=(
        "Accepts a CSV file upload from a terminal operating system (TOS) export. "
        "Column names are auto-mapped using the csv_terminal.yaml config. "
        "Returns the IDs of accepted events."
    ),
)
async def ingest_csv_terminal(
    file: UploadFile = File(..., description="CSV file exported from terminal TOS"),
    source_name: str = Form(default="CSV_TERMINAL", description="Terminal identifier e.g. 'PASHA_HONOLULU'"),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = await file.read()
    if not content.strip():
        raise HTTPException(status_code=400, detail="CSV file is empty")

    try:
        raw_rows = csv_parser.parse_file(content, source_name=source_name)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CSV parse error: {e}")

    if not raw_rows:
        raise HTTPException(status_code=422, detail="No data rows found in CSV")

    normalized, errors = engine.normalize_csv_terminal(raw_rows, source_name=source_name)
    _store_events(normalized)

    logger.info("CSV ingest: %d accepted, %d errors from %s", len(normalized), len(errors), source_name)

    return IngestResponse(
        accepted=len(normalized),
        rejected=len(errors),
        event_ids=[e.event_id for e in normalized],
        errors=errors,
    )


# ---------------------------------------------------------------------------
# Query — Events
# ---------------------------------------------------------------------------

@app.get(
    "/events",
    response_model=EventListResponse,
    tags=["Events"],
    summary="List normalized vessel events",
    description="Returns all stored normalized events. Supports filtering by vessel, event type, source, and port.",
)
def list_events(
    vessel_name: Optional[str] = Query(default=None, description="Filter by vessel name (case-insensitive contains)"),
    voyage_number: Optional[str] = Query(default=None, description="Filter by voyage number (exact match)"),
    event_type: Optional[EventType] = Query(default=None, description="Filter by event type"),
    source_format: Optional[SourceFormat] = Query(default=None, description="Filter by source format"),
    source_name: Optional[str] = Query(default=None, description="Filter by source name (exact match)"),
    port_locode: Optional[str] = Query(default=None, description="Filter by UN/LOCODE port code"),
    container_number: Optional[str] = Query(default=None, description="Filter by container number"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max events to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
):
    results = list(_event_store.values())

    if vessel_name:
        results = [e for e in results if e.vessel_name and vessel_name.lower() in e.vessel_name.lower()]
    if voyage_number:
        results = [e for e in results if e.voyage_number == voyage_number]
    if event_type:
        results = [e for e in results if e.event_type == event_type]
    if source_format:
        results = [e for e in results if e.source_format == source_format]
    if source_name:
        results = [e for e in results if e.source_name == source_name]
    if port_locode:
        results = [e for e in results if e.port_locode == port_locode]
    if container_number:
        results = [e for e in results if e.container_number == container_number]

    # Sort by ingested_at descending (newest first)
    results.sort(key=lambda e: e.ingested_at, reverse=True)

    total = len(results)
    paginated = results[offset: offset + limit]

    return EventListResponse(total=total, events=paginated)


@app.get(
    "/events/{event_id}",
    response_model=VesselEvent,
    tags=["Events"],
    summary="Get a single normalized event by ID",
)
def get_event(event_id: str):
    event = _event_store.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event '{event_id}' not found")
    return event


# ---------------------------------------------------------------------------
# Dev entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
