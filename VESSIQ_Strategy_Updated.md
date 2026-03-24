# VESSIQ — Updated Company Strategy
## Last Updated: March 23, 2026

---

## The Pivot (It's Not a Pivot)

VESSIQ's original vision: maritime data translation and normalization platform — the "middle layer" between fragmented shipping data sources and clean outputs.

**What changed:** We identified that data normalization alone isn't directly sellable. Nobody pays for infrastructure until it solves an immediate pain point.

**New approach:** Build the same normalization engine, but enter the market through **ocean freight invoice audit and D&D (demurrage & detention) dispute recovery** — a use case where the output is recovered money, not clean data.

**Why this works:** The normalization engine IS the product. Invoice audit is the first application. The technology is identical — ingest messy data from multiple formats, normalize it, match it against expected values, flag discrepancies.

---

## What We're Building

An AI-powered system that:

1. Ingests ocean freight invoices from any format (PDF, CSV, EDI 310, email)
2. Extracts and normalizes line items into a canonical schema
3. Matches line items against contracted rates
4. Flags overcharges, duplicates, unauthorized charges, and calculation errors
5. Validates D&D invoices against FMC requirements and free time terms
6. Generates dispute packages for carrier submission
7. Tracks recovery and ROI

---

## Market Opportunity

- $5B+ in annual ocean freight overcharges (U.S. alone)
- 80% of carrier invoices contain discrepancies
- Average shipper is overcharged 2-8% on ocean freight
- D&D billing is in regulatory chaos after D.C. Circuit vacated FMC billing rules (Sept 2025)
- Market leader is one person (Steve Ferreira / Ocean Audit) — space is massively underserved
- General freight audit firms (Trax, nVision, Trimble) are weak on ocean-specific billing

### TAM

| Segment | Recoverable Overcharges | VESSIQ Revenue (25% share) |
|---------|------------------------|---------------------------|
| Invoice Audit | $3.6B | $900M |
| D&D Disputes | $750M | $187M |
| Forwarder Reconciliation | $1B | $250M |
| **Total** | **$5.35B** | **$1.34B** |

Realistic Year 3 target: $15-25M ARR from 200 mid-market customers.

---

## Pricing Model

**Hybrid (recommended for early stage):**
- $2K-$3K/month base subscription
- Plus 15% gainshare on recoveries above a threshold
- Alternative: pure gainshare at 25% for pilot customers (lower friction to close)

---

## Scalability

Low customer-specific friction compared to retail chargeback tools:
- Ocean carriers are finite (~9 major carriers)
- Surcharges are standardized (BAF, CAF, THC, etc.) even if calculations vary
- Per-customer onboarding: import their carrier contracts (1-2 hours)
- Core parsing and matching engine is universal

---

## Expansion Roadmap

| Phase | Timeline | What |
|-------|----------|------|
| Phase 1 | Now - Month 3 | Ocean freight invoice audit (MVP) |
| Phase 2 | Months 3-6 | D&D dispute recovery |
| Phase 3 | Months 6-12 | Forwarder billing reconciliation |
| Phase 4 | Months 12-18 | Compliance monitoring (upsell to existing customers) |
| Phase 5 | Year 2+ | Full maritime data normalization platform (VESSIQ original vision) |

**The manifest translation layer is NOT dead.** It becomes the underlying infrastructure that powers all of the above. It's the moat, not the product.

---

## Current Status

### Completed
- Deep market research on three wedges (rail EDI, chargebacks, compliance)
- Decision to pursue ocean freight invoice audit as entry wedge
- Existing website, dashboard, and backend code (needs repurposing, not rebuilding)
- Contact with The Pasha Group — warm intro to two decision-relevant contacts

### In Progress
- Pasha call scheduled for **Friday, March 27, 2026**
- CTO conversation with Brendon (data engineer, 10+ years, AWS/Python/pipelines)
- Demo build for Pasha call

### Next Steps
- Finalize Brendon's role and commitment
- Build demo (sample invoice → parse → flag discrepancies → dashboard)
- Prep for and execute Pasha call Friday
- Get access to real invoice data from Pasha
- Build MVP on real data within 2-4 weeks of receiving it

---

## Team

| Role | Person | Status |
|------|--------|--------|
| CEO / Product / Sales | Sean | Active |
| CTO / Data Architecture | Brendon | Formalizing — call tonight |
| COO / Operations | Nick | 20% equity, 12-month cliff (Nov 2026). Needs clear deliverables |

### Nick's Deliverables (Through November Cliff)
- Build target list of 50 mid-size ocean shippers/NVOCCs
- Competitive intelligence profiles (Ocean Audit, Trax, nVision, Portcast, etc.)
- CRM setup and management (HubSpot)
- Website update to reflect new positioning
- Customer onboarding support (collecting invoices, organizing files)
- Weekly FMC/D&D regulatory monitoring briefs

### Equity Structure (To Be Formalized)
- Sean: 70-75%
- Brendon: 12-15% (vesting TBD, tied to commitment)
- Nick: Current 20% under review — lawyer advises tying to deliverables through cliff
- Reserve pool: 5-10% for future hires/advisors

---

## Key Risks

1. Pasha may not have the invoice pain directly — they may be a terminal operator, not a shipper
2. Ocean freight billing complexity requires domain expertise we're still building
3. iNymbus or a well-funded competitor could enter ocean freight audit
4. Gainshare pricing means delayed, variable revenue
5. Need real invoice data to build anything meaningful — blocked until customer provides it

---

## Competitive Landscape

| Competitor | Focus | Weakness |
|-----------|-------|----------|
| Ocean Audit (Steve Ferreira) | Ocean freight audit, gainshare | One-man operation, not scalable, no self-serve |
| Trax Technologies | Enterprise freight audit & payment | Enterprise-only, weak on ocean-specific billing |
| nVision Global | Multi-modal freight audit | Generalist, not ocean-specialized |
| Intelligent Audit | Parcel/freight audit with ML | Parcel-heavy, ocean is afterthought |
| Portcast | Ocean freight visibility + invoice audit | Visibility-first, audit is new add-on |
| Windward | Maritime AI visibility | Focused on compliance/risk, not invoice recovery |

**VESSIQ's differentiation:** AI-native, ocean-specialized, mid-market focused, built on a normalization engine that expands into adjacent maritime data problems.
