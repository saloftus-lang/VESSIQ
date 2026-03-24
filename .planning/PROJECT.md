# VESSIQ UI

## What This Is

VESSIQ is building two polished standalone HTML dashboards: a client-facing invoice chargeback demo (for sales calls and pilots) and a private founder operations dashboard. Both share the same dark-navy B2B SaaS aesthetic with subtle 3D depth effects. The invoice dashboard shows ocean freight and rail/terminal charge audits with full interactivity; the founder dashboard tracks pilot metrics, ops tasks, and industry benchmarks.

## Core Value

A demo-quality invoice chargeback dashboard that makes any prospect say "we need this" in the first 30 seconds.

## Requirements

### Validated

- ✓ EDI 315/214/322 parsing — existing
- ✓ CSV terminal export parsing — existing
- ✓ VesselEvent unified schema — existing
- ✓ FastAPI REST ingest + retrieval endpoints — existing
- ✓ In-memory event store — existing
- ✓ Sample invoice audit demo (demo/index.html) — existing
- ✓ Marketing landing page (marketing/index.html) — existing

### Active

- [ ] `dashboard.html` — Invoice chargeback demo (ocean freight + rail/terminal, fully interactive, realistic fake data)
- [ ] `founder.html` — Founder ops dashboard (pilot metrics, tasks/notes, industry benchmarks)
- [ ] Subtle 3D depth design system (CSS 3D transforms, glassmorphism, layered floating cards) applied across both files
- [ ] Consistent VESSIQ dark navy visual language (#0B1F3A, #1A56A0, #0EA5E9) across both dashboards
- [ ] Invoice dashboard: filter by carrier/date, expandable invoice rows, responsive dispute status buttons
- [ ] Founder dashboard: KPI tiles (active pilots, invoices processed, savings found), task/notes widget, industry benchmark cards

### Out of Scope

- React or build-step frameworks — startup speed, no infra overhead; standalone HTML ships immediately
- Live API integration — dashboards use realistic fake data; connecting to FastAPI is a future milestone
- Authentication or user accounts — not needed for demo or internal founder tool at this stage
- Mobile-first responsive layout — desktop priority for sales call and founder use cases
- Animated 3D globe or WebGL — subtle CSS 3D is enough; full Three.js adds weight without proportional value

## Context

- Existing codebase: Python/FastAPI backend, config-driven EDI normalization engine
- Existing UI artifacts: `demo/index.html` (ocean freight invoice audit), `marketing/index.html` (landing page), `frontend-dev-workspace/` evaluation outputs — use these as visual and structural references
- Target user for invoice dashboard: logistics/finance buyers at maritime shippers (e.g. Pasha Group — Heather Brown contact)
- Target user for founder dashboard: Sean (internal only)
- Design reference: dark navy (#0B1F3A) background, electric blue (#1A56A0) primary, sky accent (#0EA5E9), enterprise maritime feel
- Skills available: `ui-ux-pro-max.skill` and `frontend-dev.skill` — use both for design decisions and implementation
- Deployment: GitHub → Railway → vessiq.net

## Constraints

- **Tech stack**: Standalone HTML/CSS/JS only — no build tools, no npm, no bundler
- **Self-contained**: Each file must work when opened directly in a browser (CDN libs OK)
- **Performance**: No heavy 3D libraries (Three.js) — CSS 3D transforms and SVG only
- **Data**: All data is realistic fake data baked into the HTML — no API calls required to demo

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Standalone HTML over React | Startup speed, zero infra, opens in any browser, easy to share | — Pending |
| Separate files (dashboard.html + founder.html) | Clean separation of demo vs. internal tool | — Pending |
| CSS 3D depth over WebGL/Three.js | Same premium feel, fraction of the weight and complexity | — Pending |
| Realistic fake data baked in | Demo works offline, no API dependency, always looks perfect | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-24 after initialization*
