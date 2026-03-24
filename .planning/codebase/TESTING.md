# Testing Patterns

**Analysis Date:** 2026-03-24

## Test Framework

**Status:** No automated test framework currently configured

**What's Present:**
- No `pytest.ini`, `pyproject.toml`, or `tox.ini` configuration
- No test runner dependencies in `requirements.txt`
- No test files found in codebase (no `test_*.py` or `*_test.py` files)
- No test fixtures, factories, or sample data loaders

**Sample Data Available:**
- Realistic sample EDI files for manual testing:
  - `sample_data/sample_315.edi` — EDI 315 ocean shipment status
  - `sample_data/sample_214.edi` — EDI 214 transportation shipment status
  - `sample_data/sample_322.edi` — EDI 322 terminal/container status
  - `sample_data/sample_terminal.csv` — Terminal TOS export CSV

## Testing Approach (Current)

**Manual Testing:**
- Start the API: `uvicorn main:app --reload --port 8000`
- API docs auto-generated at `http://localhost:8000/docs` (Swagger/OpenAPI)
- Use FastAPI's interactive documentation to POST payloads and inspect responses
- Sample files in `sample_data/` can be uploaded or pasted as request bodies

**What's Testable:**
- All parsing logic is in `vessiq/parsers/edi315.py`, `edi214.py`, `edi322.py`, `csv_terminal.py`
- All normalization in `vessiq/normalizer/engine.py` — can be unit tested independently
- Schema validation by Pydantic in `vessiq/schema.py` — models reject invalid data
- API routes and error handling in `main.py` — can be integration tested with `TestClient`

## Recommended Testing Structure

**For Adding Tests:**

Use `pytest` as the test runner. Install with:
```bash
pip install pytest pytest-asyncio
```

**Test File Organization:**
- Place tests adjacent to source: `test_main.py`, `test_schema.py`
- Parser tests: `vessiq/parsers/test_edi315.py`, `test_csv_terminal.py`
- Normalizer tests: `vessiq/normalizer/test_engine.py`
- Integration tests: `tests/integration/test_api.py` (separate directory)

**Suggested Layout:**
```
VESSIQ/
├── main.py
├── test_main.py
├── vessiq/
│   ├── schema.py
│   ├── test_schema.py
│   ├── parsers/
│   │   ├── edi315.py
│   │   └── test_edi315.py
│   └── normalizer/
│       ├── engine.py
│       └── test_engine.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   └── edi_samples.py
│   └── integration/
│       └── test_api.py
└── sample_data/
    └── sample_315.edi
```

## Test Structure Pattern

**Unit Test Example (for future implementation):**
```python
import pytest
from datetime import datetime
from vessiq.schema import VesselEvent, EventType, SourceFormat
from vessiq.normalizer import engine

def test_normalize_edi315_basic():
    """Test normalizing a single EDI 315 record."""
    raw_event = {
        "vessel_name": "MSC GULSUN",
        "vessel_imo": "9633567",
        "voyage_number": "006E",
        "status_code": "VE",
        "status_date": "20240320",
        "status_time": "1430",
        "port_locode": "USLAX",
        "port_name": "Los Angeles",
        "container_number": "MSCU1234567",
        "booking_number": "123456789",
        "bill_of_lading": "987654321",
    }

    config = {
        "status_codes": {"VE": "ARRIVAL"},
        "date_formats": ["%Y%m%d"],
        "time_formats": ["%H%M"],
    }

    event = engine._normalize_edi315_record(raw_event, config, "TEST_SOURCE")

    assert event.event_type == EventType.ARRIVAL
    assert event.vessel_name == "MSC GULSUN"
    assert event.event_timestamp == datetime(2024, 3, 20, 14, 30)
    assert event.source_format == SourceFormat.EDI_315
    assert event.source_name == "TEST_SOURCE"
```

**Integration Test Example (for future implementation):**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_ingest_edi315_success(client):
    """Test EDI 315 ingest endpoint with valid data."""
    edi_content = "ISA*00*          *00*          *ZZ*EDI_SOURCE    *ZZ*RECEIVER      *200320*1430*U*00401*000000001*0*P*:~ST*315*0001~..."

    response = client.post(
        "/ingest/edi315",
        data={"raw_edi": edi_content, "source_name": "TEST_CARRIER"}
    )

    assert response.status_code == 200
    result = response.json()
    assert result["accepted"] >= 0
    assert result["rejected"] >= 0
    assert "event_ids" in result

def test_ingest_edi315_empty_content(client):
    """Test EDI 315 ingest with empty content."""
    response = client.post(
        "/ingest/edi315",
        data={"raw_edi": "   ", "source_name": "TEST_CARRIER"}
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()
```

## Mocking

**Framework:** `unittest.mock` (Python standard library) or `pytest-mock`

**What to Mock:**
- File I/O when testing YAML config loading: `mock.patch('pathlib.Path.open')`
- External API calls if future integrations added
- Datetime for time-dependent tests: `mock.patch('datetime.datetime.utcnow')`

**What NOT to Mock:**
- Parsing logic — test with real sample EDI/CSV data from `sample_data/`
- Normalization engine — test the actual mapping behavior
- Pydantic models — validation is the point
- Database/event store operations in tests (use in-memory store or fixture)

**Mocking Pattern Example:**
```python
from unittest.mock import patch, mock_open
import yaml

def test_load_mapping():
    """Test loading YAML mapping config."""
    yaml_content = """
field_map:
  vessel_name: vessel_name
status_codes:
  VE: ARRIVAL
date_formats: ["%Y%m%d"]
"""
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        config = yaml.safe_load(open("dummy.yaml"))
        assert config["status_codes"]["VE"] == "ARRIVAL"
```

## Fixtures and Factories

**Test Data Location:** `sample_data/` directory contains realistic examples

**Recommended Fixtures (for future implementation):**

Create `tests/conftest.py`:
```python
import pytest
from pathlib import Path

@pytest.fixture
def edi315_sample():
    """Load sample EDI 315 file."""
    path = Path(__file__).parent.parent / "sample_data" / "sample_315.edi"
    return path.read_text()

@pytest.fixture
def csv_terminal_sample():
    """Load sample CSV terminal export."""
    path = Path(__file__).parent.parent / "sample_data" / "sample_terminal.csv"
    return path.read_text()

@pytest.fixture
def sample_raw_event():
    """Factory for a minimal raw EDI 315 record dict."""
    return {
        "vessel_name": "TEST VESSEL",
        "vessel_imo": "1234567",
        "status_code": "VE",
        "status_date": "20240320",
        "port_locode": "USLAX",
    }
```

## Coverage

**Requirements:** None currently enforced

**To Add Coverage Tracking:**
```bash
pip install pytest-cov
pytest --cov=vessiq --cov-report=html
```

**View Coverage:**
```bash
pytest --cov=vessiq --cov-report=term-missing
```

**Target Areas for Coverage:**
- `vessiq/parsers/*.py` — All segment extraction logic (100% coverage goal)
- `vessiq/normalizer/engine.py` — All mapping and normalization paths (95%+ coverage goal)
- `main.py` — All endpoint handlers and error cases (90%+ coverage goal)
- `vessiq/schema.py` — Already validated by Pydantic; minimal test burden

## Test Types

**Unit Tests:**
- Scope: Individual parser functions, normalizer functions, schema models
- Approach: Test each function with known inputs and assert outputs
- Examples: `test_parse_edi315_b4_segment()`, `test_normalize_csv_record()`, `test_map_event_type()`
- Run with: `pytest vessiq/`

**Integration Tests:**
- Scope: Full ingest pipeline (parse → normalize → store → retrieve)
- Approach: Post real EDI/CSV data to API endpoints, verify response and queried results
- Examples: `test_ingest_edi315_e2e()`, `test_list_events_with_filters()`
- Run with: `pytest tests/integration/`

**End-to-End Tests:**
- Not currently present; would test full deployment (API + frontend)
- Optional: Use Playwright or Selenium for browser-based testing if frontend automation added

## Common Testing Patterns

**Async Testing:**
- Not required currently; FastAPI routes are marked `async def` but can be tested synchronously with `TestClient`
- If adding async-specific tests: use `pytest-asyncio`

```python
@pytest.mark.asyncio
async def test_async_ingest():
    # FastAPI's TestClient handles async automatically
    client = TestClient(app)
    response = client.post("/ingest/edi315", data={...})
    assert response.status_code == 200
```

**Error Testing:**
```python
def test_parse_edi315_invalid_delimiters():
    """Test parsing fails gracefully with invalid delimiters."""
    bad_edi = "INVALID~EDI~DATA"
    # Parser should return empty list or minimal result
    result = edi315_parser.parse(bad_edi)
    assert result == [] or len(result) == 0

def test_normalize_handles_missing_fields():
    """Test normalization with incomplete raw data."""
    incomplete_raw = {"status_code": "VE"}  # minimal fields
    config = {"status_codes": {"VE": "ARRIVAL"}, "date_formats": ["%Y%m%d"], "time_formats": ["%H%M"]}

    event = engine._normalize_edi315_record(incomplete_raw, config, "TEST")
    # Should still produce a VesselEvent, with Nones for missing fields
    assert event.event_type == EventType.ARRIVAL
    assert event.vessel_name is None
    assert event.port_locode is None
```

**Datetime Testing:**
```python
def test_parse_datetime_multiple_formats():
    """Test that datetime parser tries multiple formats."""
    # Test format 1
    result = engine._parse_datetime("20240320", "1430", ["%Y%m%d"], ["%H%M"])
    assert result == datetime(2024, 3, 20, 14, 30)

    # Test format 2 (2-digit year)
    result = engine._parse_datetime("240320", "1430", ["%y%m%d"], ["%H%M"])
    assert result == datetime(2024, 3, 20, 14, 30)

    # Test with missing time
    result = engine._parse_datetime("20240320", None, ["%Y%m%d"], ["%H%M"])
    assert result == datetime(2024, 3, 20)
```

---

*Testing analysis: 2026-03-24*
