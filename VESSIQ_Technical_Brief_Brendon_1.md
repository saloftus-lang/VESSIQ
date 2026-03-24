# VESSIQ — Technical Brief for Data Architecture
## Ocean Freight Invoice Audit & D&D Recovery Engine

---

## What We're Building

A system that ingests ocean freight invoices from multiple sources (PDFs, CSVs, EDI), extracts and normalizes line items, matches them against contracted rates, and flags billing errors and overcharges. Think of it as a data normalization + discrepancy detection engine for maritime billing.

**The core loop:**

```
Invoice (any format) → Parse → Normalize → Match against contract → Flag discrepancies → Generate dispute
```

This same engine will eventually handle demurrage/detention invoices and expand into other maritime document types (manifests, BOLs, etc.). The architecture should be built with that in mind.

---

## The Data Problem

Ocean freight invoices are messy:

- **Multiple formats:** PDF (most common from carriers), CSV exports from carrier portals, EDI 310 (Freight Receipt and Invoice), email attachments, forwarder-reformatted invoices
- **No standard schema:** Maersk invoices look different from CMA CGM, which look different from a forwarder's re-billing of the same shipment
- **20+ possible line item types per invoice:** Base ocean freight, BAF (Bunker Adjustment Factor), CAF (Currency Adjustment Factor), THC (Terminal Handling Charge), ISPS fee, documentation fee, chassis charges, congestion surcharge, peak season surcharge, low sulfur surcharge, VGM fee, seal fee, etc.
- **Surcharge calculation varies:** BAF might be a flat rate per TEU, a percentage of base freight, or indexed to a fuel price formula — differs by carrier and contract
- **Currency complexity:** Contract might be in USD, invoice in EUR, with mid-voyage surcharges in local port currency
- **Multiple parties:** A single container might generate invoices from the ocean carrier, the origin terminal, the destination terminal, the forwarder, and the drayage provider

### Demurrage & Detention (D&D) Invoices — Additional Complexity

- Charges are time-based: calculated from free time expiry to container return/pickup
- Free time varies by: carrier, port, contract terms, import vs. export, container type (dry, reefer, special)
- FMC (Federal Maritime Commission) requires specific fields on D&D invoices: container number, BOL number, free time allowed, charge start/end dates, applicable tariff. Missing fields = invoice is legally invalid
- Common errors: wrong free time calculation, charges during terminal closures, duplicate billing, billing the wrong party

---

## Proposed Data Model

### Core Entities

**1. Customer**
```
customer_id (PK)
company_name
contact_info
annual_ocean_spend (estimated)
created_at
```

**2. Carrier**
```
carrier_id (PK)
carrier_name           -- e.g., "Maersk", "CMA CGM", "MSC"
carrier_code           -- SCAC code
invoice_format_type    -- pdf, csv, edi_310, custom
known_surcharge_codes  -- JSON mapping of carrier-specific codes to normalized codes
```

**3. Contract**
```
contract_id (PK)
customer_id (FK)
carrier_id (FK)
contract_number
effective_date
expiration_date
currency
terms_json             -- full contract terms as structured JSON
```

**4. ContractRate**
```
rate_id (PK)
contract_id (FK)
origin_port            -- UN/LOCODE
destination_port       -- UN/LOCODE
container_type         -- 20GP, 40GP, 40HC, 45HC, 20RF, 40RF
base_rate              -- ocean freight rate
currency
rate_type              -- per_container, per_teu, per_cbm, per_kg
valid_from
valid_to
```

**5. ContractSurcharge**
```
surcharge_id (PK)
contract_id (FK)
surcharge_type         -- normalized code (see Surcharge Taxonomy below)
calculation_method     -- flat_per_container, percentage_of_base, indexed
rate_value             -- flat amount or percentage
index_reference        -- e.g., "Rotterdam Bunker Index" if indexed
currency
valid_from
valid_to
```

**6. Invoice**
```
invoice_id (PK)
customer_id (FK)
carrier_id (FK)
invoice_number
invoice_date
due_date
total_amount
currency
source_format          -- pdf, csv, edi, email
raw_file_path          -- path to original uploaded file
parsing_status         -- pending, parsed, failed, review_needed
parsed_at
```

**7. InvoiceLineItem**
```
line_item_id (PK)
invoice_id (FK)
container_number
bol_number
origin_port
destination_port
container_type
charge_type            -- normalized surcharge code
charge_description     -- raw text from invoice
amount
currency
quantity               -- number of containers if applicable
unit_rate              -- amount / quantity
raw_text               -- original line as extracted from document
```

**8. Discrepancy**
```
discrepancy_id (PK)
line_item_id (FK)
invoice_id (FK)
contract_rate_id (FK)  -- the contract rate it was matched against (nullable)
discrepancy_type       -- overcharge, duplicate, missing_contract_rate, 
                       -- surcharge_miscalculation, unauthorized_charge,
                       -- currency_error, dd_free_time_error, dd_invalid_invoice
invoiced_amount
expected_amount
difference
confidence_score       -- 0-1, how confident the system is this is a real error
status                 -- detected, confirmed, disputed, recovered, written_off
notes
detected_at
```

**9. Dispute**
```
dispute_id (PK)
customer_id (FK)
carrier_id (FK)
discrepancy_ids        -- array of discrepancy IDs in this dispute
total_disputed_amount
dispute_date
carrier_response       -- pending, accepted, partial, rejected
recovered_amount
resolution_date
dispute_document_path  -- generated dispute letter/package
```

**10. DDInvoice (Demurrage & Detention specific)**
```
dd_invoice_id (PK)
invoice_id (FK)         -- links to main Invoice table
container_number
bol_number
charge_type             -- demurrage, detention, per_diem, combined
free_time_allowed_days
free_time_start_date
free_time_end_date
charge_start_date
charge_end_date
daily_rate
total_charge
port_code
terminal_name
-- FMC compliance fields
has_container_number     -- boolean
has_bol_number           -- boolean
has_free_time_info       -- boolean
has_charge_dates         -- boolean
has_tariff_reference     -- boolean
has_dispute_contact      -- boolean
fmc_compliant            -- boolean (all required fields present)
```

---

## Surcharge Taxonomy (Normalized Codes)

The key architectural decision: every carrier uses different names for the same charges. We need a canonical taxonomy that all carrier-specific codes map to.

```
OCEAN_FREIGHT          -- Base ocean freight rate
BAF / BUC / EBS        -- Bunker/fuel surcharges (multiple carrier names)
CAF                    -- Currency adjustment factor
THC_ORIGIN             -- Terminal handling at origin
THC_DEST               -- Terminal handling at destination
ISPS                   -- International Ship and Port Security
DOC_FEE                -- Documentation/bill of lading fee
SEAL_FEE               -- Container seal
VGM_FEE                -- Verified Gross Mass
CHASSIS_FEE            -- Chassis usage
CONGESTION             -- Port congestion surcharge
PEAK_SEASON            -- Peak season surcharge (PSS)
LOW_SULFUR             -- Low sulfur fuel surcharge (LSS)
WAR_RISK               -- War risk surcharge
PIRACY                 -- Piracy surcharge
AMS_FEE                -- Automated Manifest System fee
ISF_FEE                -- Importer Security Filing fee
CUSTOMS_EXAM           -- Customs examination charges
DEMURRAGE              -- Container storage at terminal
DETENTION              -- Container use beyond free time
PER_DIEM               -- Daily equipment charge
REEFER_SURCHARGE       -- Refrigerated container premium
OVERWEIGHT             -- Overweight surcharge
OUT_OF_GAUGE           -- Out of gauge/oversized cargo
HAZMAT                 -- Hazardous materials handling
INLAND_HAULAGE         -- Inland transport component
OTHER                  -- Catch-all for unmapped charges
```

Each carrier gets a mapping table:

```
CarrierSurchargeMapping:
  carrier_id
  carrier_charge_code    -- e.g., Maersk's "EBS" 
  carrier_charge_name    -- e.g., "Emergency Bunker Surcharge"
  normalized_code        -- e.g., "BAF"
```

This mapping is the core IP. It's what allows the system to compare apples to apples across carriers.

---

## Pipeline Architecture

```
┌─────────────┐
│  INGESTION  │
│             │
│ PDF Upload  │──→ PDF Parser (PyMuPDF/pdfplumber + LLM extraction)
│ CSV Upload  │──→ CSV Parser (pandas, configurable column mapping)  
│ EDI 310     │──→ EDI Parser (X12 segment parser)
│ Email       │──→ Email Parser (attachment extraction + body parsing)
│             │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ EXTRACTION  │
│             │
│ Raw text/   │──→ LLM-assisted field extraction
│ structured  │    (invoice #, dates, line items, amounts, ports)
│ data        │──→ Validation checks (amounts sum correctly, dates valid)
│             │──→ Output: structured InvoiceLineItem records
└──────┬──────┘
       │
       ▼
┌──────────────┐
│NORMALIZATION │
│              │
│ Map carrier- │──→ Apply CarrierSurchargeMapping
│ specific     │──→ Normalize currency to contract currency
│ codes to     │──→ Normalize port codes to UN/LOCODE
│ canonical    │──→ Normalize container type codes
│ taxonomy     │
└──────┬───────┘
       │
       ▼
┌─────────────┐
│  MATCHING   │
│             │
│ For each    │──→ Find matching ContractRate (origin, dest, container type, date)
│ line item:  │──→ Find matching ContractSurcharge (type, date)
│             │──→ Compare invoiced amount vs. expected amount
│             │──→ Check for duplicates (same container + charge + date)
│             │──→ For D&D: validate free time, check FMC compliance
│             │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ DISCREPANCY  │
│ DETECTION    │
│              │
│ Flag issues: │──→ Overcharge (invoiced > contracted)
│              │──→ Unauthorized charge (no matching contract surcharge)
│              │──→ Duplicate billing
│              │──→ Currency conversion error
│              │──→ D&D free time miscalculation
│              │──→ D&D FMC non-compliant invoice
│              │──→ Assign confidence score
│              │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   OUTPUT     │
│              │
│ Dashboard    │──→ Total spend, discrepancies found, recovery potential
│ Dispute pkg  │──→ PDF with evidence for carrier submission
│ Analytics    │──→ Error patterns by carrier, charge type, trade lane
│ API          │──→ JSON endpoints for integration with customer ERP
│              │
└──────────────┘
```

---

## Key Architecture Decisions Needed from Brendon

1. **Database choice:** Postgres is the obvious answer for structured invoice data. But do we need a document store (MongoDB) alongside it for raw parsed content? Or just store raw JSON in Postgres JSONB fields?

2. **LLM integration for parsing:** PDF invoices will need LLM-assisted extraction (GPT-4 / Claude) to handle the variety of formats. How do we architect this so it's not a bottleneck at scale? Probably async job queue (Celery/Redis) with caching of extraction results.

3. **Matching algorithm:** Exact match on port pairs + container type is straightforward. But contracts have date ranges, surcharges change quarterly, and some charges are percentage-based on a fluctuating index. How sophisticated does the matching engine need to be for v1?

4. **Multi-tenancy:** Each customer has their own contracts, invoices, and mappings. Standard schema-per-tenant or shared schema with customer_id partitioning?

5. **Confidence scoring:** How do we calculate confidence that a discrepancy is real vs. a parsing error? Simple rules engine for v1, or invest in ML from the start?

6. **Scale targets:** v1 needs to handle maybe 100-500 invoices/month for 1-5 customers. But if this works, we could be processing 50,000+/month within 18 months. Build for the small number now or architect for scale?

---

## What We Need for the Demo (This Week)

Minimum viable demo for the Pasha call:

1. Upload a PDF invoice
2. System extracts line items and displays them in a table
3. Compare against a hardcoded rate table
4. Flag 2-3 obvious discrepancies (overcharge, duplicate, unauthorized surcharge)
5. Show total recovery potential
6. Generate a simple dispute summary

This can use SQLite, hardcoded carrier mappings, and a single PDF parser. Brendon's input on the data model now means the demo code evolves into the real product instead of getting thrown away.

---

## Why This Architecture Matters Long-Term

The normalization layer (carrier-specific codes → canonical taxonomy) is the same pattern we'll use for:
- Manifest data normalization (different carriers, different formats, same underlying shipment data)  
- BOL standardization
- Terminal event normalization (322 EDI from rail, terminal operating system exports)
- Compliance document validation

**We're not building an invoice audit tool. We're building a maritime data normalization engine. Invoice audit is the first application.**
