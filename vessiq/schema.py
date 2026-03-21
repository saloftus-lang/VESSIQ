"""
VESSIQ Unified Schema
---------------------
Every vessel event, regardless of source format, is normalized into a VesselEvent.
This is the single source of truth for what VESSIQ outputs.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Standardized vessel/container event types used across all sources."""
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"
    BERTHING = "BERTHING"
    GATE_IN = "GATE_IN"
    GATE_OUT = "GATE_OUT"
    LOADED = "LOADED"
    DISCHARGED = "DISCHARGED"
    ETA_UPDATE = "ETA_UPDATE"
    ETD_UPDATE = "ETD_UPDATE"
    CUSTOMS_RELEASED = "CUSTOMS_RELEASED"
    AVAILABLE = "AVAILABLE"
    UNKNOWN = "UNKNOWN"


class SourceFormat(str, Enum):
    EDI_315 = "EDI_315"
    EDI_214 = "EDI_214"
    EDI_322 = "EDI_322"
    CSV_TERMINAL = "CSV_TERMINAL"


class VesselEvent(BaseModel):
    """
    The VESSIQ normalized vessel event schema.
    Every ingest path — EDI 315, CSV terminal, future sources — maps to this.
    """

    # --- Identity ---
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_format: SourceFormat
    source_name: str = Field(..., description="Name of the data source, e.g. 'PASHA_TERMINAL'")
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

    # --- Vessel ---
    vessel_name: Optional[str] = None
    vessel_imo: Optional[str] = None
    voyage_number: Optional[str] = None

    # --- Event ---
    event_type: EventType = EventType.UNKNOWN
    event_timestamp: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    estimated_departure: Optional[datetime] = None

    # --- Location ---
    port_locode: Optional[str] = None      # UN/LOCODE e.g. "USLAX"
    port_name: Optional[str] = None
    terminal_code: Optional[str] = None
    terminal_name: Optional[str] = None

    # --- Cargo References ---
    container_number: Optional[str] = None
    booking_number: Optional[str] = None
    bill_of_lading: Optional[str] = None

    # --- Raw Preservation ---
    raw_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Original parsed fields preserved verbatim for audit/debugging"
    )

    model_config = {"use_enum_values": True}


class IngestResponse(BaseModel):
    """Returned after a successful ingest call."""
    accepted: int
    rejected: int
    event_ids: list[str]
    errors: list[str] = []


class EventListResponse(BaseModel):
    total: int
    events: list[VesselEvent]
