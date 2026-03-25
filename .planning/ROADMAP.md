# Roadmap: VESSIQ UI

## Overview

Two standalone HTML dashboards built to coarse granularity. Phase 1 delivers the sales-critical invoice chargeback demo — the artifact that makes a logistics buyer say "we need this" in 30 seconds. Phase 2 delivers the founder ops dashboard for internal decision support. The design system is established in Phase 1 and reused verbatim in Phase 2.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Invoice Demo Dashboard** - Sales-ready invoice chargeback demo with design system, charts, interactive table, and ROI calculator
- [ ] **Phase 2: Founder Ops Dashboard** - Internal founder dashboard with pilot metrics, task/notes widgets, and industry benchmarks

## Phase Details

### Phase 1: Invoice Demo Dashboard
**Goal**: A prospect can open dashboard.html and — within 30 seconds — see $284K in overcharges, drill into a disputed invoice line-by-line, and calculate their own ROI
**Depends on**: Nothing (first phase)
**Requirements**: DS-01, DS-02, DS-03, DS-04, DS-05, DS-06, DS-07, INV-01, INV-02, INV-03, INV-04, INV-05, INV-06, INV-07, INV-08, INV-09, INV-10, INV-11, INV-12, INV-13, REL-01, REL-02, REL-03, REL-04, REL-05
**Success Criteria** (what must be TRUE):
  1. Opening dashboard.html shows 4 KPI tiles with count-up animation — Total Invoices Audited, Total Overcharges Found, Recovery Amount, and Dispute Win Rate — all reconciling mathematically with the invoice table data
  2. Clicking any invoice row expands to show the line-item breakdown: billed vs. contract amount, discrepancy type (BAF, THC, D&D), and dispute status badge
  3. Filtering by carrier or date range instantly updates the table — filter state is managed via a centralized JS state object with no page reload
  4. The ROI calculator accepts a monthly freight spend dollar amount and outputs an estimated annual recovery and net benefit after VESSIQ fee
  5. The page renders without console errors at 1280x800 and 1440x900, works when served via python3 -m http.server, and passes the maritime data credibility checklist (valid SCAC codes, LOCODEs, ISO 6346 container format)
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Foundation: design system, fonts, header, KPI tiles with GSAP animation, DATA array
- [x] 01-02-PLAN.md — Interactive table: filter bar, invoice table, expandable rows, dispute badges
- [ ] 01-03-PLAN.md — Charts, ROI calculator, and final demo verification

**UI hint**: yes

### Phase 2: Founder Ops Dashboard
**Goal**: Sean can open founder.html and immediately see pilot health, this week's tasks, and industry benchmark comparisons — all persisted in localStorage
**Depends on**: Phase 1
**Requirements**: FND-01, FND-02, FND-03, FND-04, FND-05, FND-06, FND-07
**Success Criteria** (what must be TRUE):
  1. The founder dashboard header is visually distinct from the demo dashboard ("Founder View" label) while sharing the same dark-navy design system and glassmorphism card style
  2. The ops tasks widget lets Sean add, complete, and delete to-do items — state survives a browser refresh via localStorage
  3. The notes widget accepts freeform text and persists it to localStorage on input with no save button required
  4. The industry benchmarks section shows "Industry avg" vs "VESSIQ target" comparisons with a visual indicator (progress bar or delta badge) for all 3 benchmark cards
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Invoice Demo Dashboard | 1/3 | In Progress|  |
| 2. Founder Ops Dashboard | 0/TBD | Not started | - |
