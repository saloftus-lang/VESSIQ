# Requirements: VESSIQ UI

**Defined:** 2026-03-24
**Core Value:** A demo-quality invoice chargeback dashboard that makes any prospect say "we need this" in the first 30 seconds.

## v1 Requirements

### Design System

- [x] **DS-01**: Dark navy color system (#0B1F3A background, #1A56A0 primary, #0EA5E9 accent, #10B981 success, #EF4444 danger) applied consistently across both files
- [x] **DS-02**: CSS custom properties (two-tier: primitive tokens + semantic aliases) duplicated verbatim in both HTML files as the single coordination point
- [x] **DS-03**: Subtle 3D depth applied via CSS perspective transforms, glassmorphism panels (backdrop-filter + rgba fill + 1px border + box-shadow), and layered floating cards
- [x] **DS-04**: Glassmorphism panels have non-transparent background-color and -webkit-backdrop-filter prefix (Safari compatibility)
- [x] **DS-05**: Inter or system-UI font stack — no external font CDN dependency (offline-safe)
- [x] **DS-06**: ApexCharts used for all charts (dark theme via config, DOM-based tooltips, transparent background locked — no mode toggle)
- [x] **DS-07**: GSAP CDN used for counter animations and entrance transitions; CSS transitions for everything else

### Invoice Dashboard (dashboard.html)

- [x] **INV-01**: Header with VESSIQ logo, nav links, and "Book Demo" CTA
- [x] **INV-02**: KPI summary row — 4 tiles: Total Invoices Audited, Total Overcharges Found, Recovery Amount ($), Dispute Win Rate (%)
- [x] **INV-03**: KPI tile numbers animate (count up) on page load using GSAP
- [ ] **INV-04**: Invoice table showing ocean freight and rail/terminal charges in a unified view, with source badge (Ocean / Rail) per row
- [ ] **INV-05**: Table filterable by carrier and date range — filter state managed via centralized JS state object
- [ ] **INV-06**: Each invoice row expandable on click (event delegation on table container) to reveal line-item breakdown: billed amount vs. contract amount, discrepancy type (BAF, THC, D&D, per diem), and dispute status
- [ ] **INV-07**: Dispute status badges (Pending / Filed / Won / Recovered) with color coding
- [ ] **INV-08**: ROI calculator panel — single input (monthly freight spend $) → output (estimated annual recovery minus VESSIQ fee) using industry benchmark recovery rate
- [x] **INV-09**: Realistic fake data: Maersk, MSC, Evergreen, Hapag-Lloyd (ocean) + Pasha Hawaii, BNSF (rail/terminal) — correct SCAC codes, UN/LOCODE port codes, ISO 6346 container number format
- [x] **INV-10**: All KPI totals mathematically reconcile with the invoice table data (no disconnected numbers)
- [ ] **INV-11**: ApexCharts bar chart: overcharge amount by carrier
- [ ] **INV-12**: ApexCharts donut/pie: breakdown by charge type (BAF, THC, D&D, Other)
- [ ] **INV-13**: Page works when served over HTTP (python3 -m http.server) — no file:// fetch() calls

### Founder Dashboard (founder.html)

- [ ] **FND-01**: Header with VESSIQ logo and "Founder View" label (distinct from demo dashboard)
- [ ] **FND-02**: Pilot metrics section — 3 KPI tiles: Active Pilots, Invoices Processed (total), Total Savings Identified ($)
- [ ] **FND-03**: Ops tasks widget — weekly goal (editable text), to-do list with add/complete/delete (persisted in localStorage)
- [ ] **FND-04**: Notes widget — freeform textarea, saved to localStorage on input
- [ ] **FND-05**: Industry benchmarks section — 3 benchmark cards: Average Invoice Error Rate (industry 30–45%), Average Detention Days, Dispute Win Rate (industry avg vs. VESSIQ target)
- [ ] **FND-06**: Benchmark cards show "Industry avg" vs "VESSIQ target" comparison with visual indicator (progress bar or delta badge)
- [ ] **FND-07**: Same design system as dashboard.html (shared CSS token values, same glassmorphism card style)

### Demo Reliability

- [x] **REL-01**: All external assets (fonts, chart libraries, GSAP) either served locally or from a single pinned CDN URL — no multi-origin loading that can partially fail
- [x] **REL-02**: Page renders correctly at 1280×800 and 1440×900 (common laptop screen share resolutions)
- [ ] **REL-03**: No console errors on load or during interactions
- [ ] **REL-04**: Expandable rows, filters, and ROI calculator all work without page reload
- [x] **REL-05**: Fake maritime data passes credibility check: valid SCAC codes (MAEU, MSCU, EGLV, HLCU, PSHA), valid LOCODEs (USLAX, USLGB, USSEA, USHON), ISO 6346 container format (4-letter prefix + 7 digits + check digit pattern)

## v2 Requirements

### Future Enhancements

- **V2-01**: Live data connection to VESSIQ FastAPI backend (replace fake data with real /events API)
- **V2-02**: Export to PDF/CSV (dispute summary report)
- **V2-03**: Email report functionality from founder dashboard
- **V2-04**: Animated globe showing active port locations (Three.js or Mapbox)
- **V2-05**: Multi-pilot view (filter by customer in founder dashboard)
- **V2-06**: Mobile-responsive layout

## Out of Scope

| Feature | Reason |
|---------|--------|
| React / build tooling | Startup speed, zero infra — standalone HTML ships immediately |
| Authentication / login | Not needed for demo tool or internal founder use at this stage |
| Live API integration | v1 uses fake data; API connection is v2 |
| Three.js / WebGL globe | CSS 3D gives same premium feel at a fraction of the weight |
| Mobile layout | Desktop-only for sales calls and founder use; mobile is v2 |
| Dark/light mode toggle | ApexCharts dark mode bug; single dark theme is safer and on-brand |
| PDF export | v2 — complex, not needed for demo phase |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DS-01 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-02 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-03 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-04 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-05 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-06 | Phase 1: Invoice Demo Dashboard | Complete |
| DS-07 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-01 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-02 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-03 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-04 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-05 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-06 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-07 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-08 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-09 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-10 | Phase 1: Invoice Demo Dashboard | Complete |
| INV-11 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-12 | Phase 1: Invoice Demo Dashboard | Pending |
| INV-13 | Phase 1: Invoice Demo Dashboard | Pending |
| REL-01 | Phase 1: Invoice Demo Dashboard | Complete |
| REL-02 | Phase 1: Invoice Demo Dashboard | Complete |
| REL-03 | Phase 1: Invoice Demo Dashboard | Pending |
| REL-04 | Phase 1: Invoice Demo Dashboard | Pending |
| REL-05 | Phase 1: Invoice Demo Dashboard | Complete |
| FND-01 | Phase 2: Founder Ops Dashboard | Pending |
| FND-02 | Phase 2: Founder Ops Dashboard | Pending |
| FND-03 | Phase 2: Founder Ops Dashboard | Pending |
| FND-04 | Phase 2: Founder Ops Dashboard | Pending |
| FND-05 | Phase 2: Founder Ops Dashboard | Pending |
| FND-06 | Phase 2: Founder Ops Dashboard | Pending |
| FND-07 | Phase 2: Founder Ops Dashboard | Pending |

**Coverage:**
- v1 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-24*
*Last updated: 2026-03-24 after roadmap creation*
