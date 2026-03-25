# Phase 2: Founder Ops Dashboard - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-25
**Phase:** 02-founder-ops-dashboard
**Areas discussed:** Visual theme, Page layout, Pilot KPI data

---

## Visual Theme

| Option | Description | Selected |
|--------|-------------|----------|
| Dark navy + glassmorphism | Background #0B1F3A, glass cards with backdrop-filter blur, white text | ✓ |
| Match light dashboard.html | White cards, #F8FAFC background, same look as the demo | |

**User's choice:** Dark navy + glassmorphism
**Notes:** Visually distinct from the light demo dashboard — makes it clear this is the internal tool.

### Glassmorphism depth

| Option | Description | Selected |
|--------|-------------|----------|
| Flat glass | Clean backdrop-filter + 1px white border + soft box-shadow. No 3D transforms | ✓ |
| 3D depth cards | CSS perspective transforms, floating/layered feel | |

**User's choice:** Flat glass

### Header style

| Option | Description | Selected |
|--------|-------------|----------|
| Same navy header, amber "Founder View" badge | Reuse dashboard.html header, swap badge color to gold/amber | ✓ |
| Full-bleed minimal bar | Just logo + label, no CTA | |

**User's choice:** Same navy header with amber "Founder View" badge

---

## Page Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Single-page scroll | All sections visible by scrolling. KPIs → tasks+notes → benchmarks | ✓ |
| 4-tab nav like dashboard.html | Same step-by-step tab pattern | |

**User's choice:** Single-page scroll
**Notes:** Daily-use internal tool — scrolling is more natural than tabs.

### Section header

| Option | Description | Selected |
|--------|-------------|----------|
| "This Week" heading above tasks/notes | Small section label to anchor context | ✓ |
| No section header | Just cards side-by-side | |

**User's choice:** "This Week" heading

### Widget width split

| Option | Description | Selected |
|--------|-------------|----------|
| Equal 50/50 split | Tasks and notes cards same width | ✓ |
| Tasks wider (60/40) | More space for the to-do list | |

**User's choice:** 50/50 split

---

## Pilot KPI Data

### Active pilots count

| Option | Description | Selected |
|--------|-------------|----------|
| 1 active pilot (Pasha) | Honest reflection of current state | ✓ |
| 2 active pilots | Pasha + one more in progress | |
| 3 active pilots | Optimistic view of near-term pipeline | |

**User's choice:** 1 (Pasha)

### Total Savings number

| Option | Description | Selected |
|--------|-------------|----------|
| $187,500 (tie to dashboard.html) | Same won+recovered sum as demo data | ✓ |
| $284K+ (bigger portfolio view) | Full audit value including all disputes | |

**User's choice:** $187,500 — tied to dashboard.html DATA array

### Invoices Processed count

| Option | Description | Selected |
|--------|-------------|----------|
| 23 (tie to dashboard.html DATA.length) | Exact number of invoice rows | ✓ |
| 847 (PORTFOLIO_TOTAL) | Full portfolio size from demo | |

**User's choice:** 23

### KPI animations

| Option | Description | Selected |
|--------|-------------|----------|
| GSAP count-up on load | Same entrance animation as dashboard.html | ✓ |
| No animation | Static numbers | |

**User's choice:** GSAP count-up

---

## Claude's Discretion

- Benchmark card visualization style (progress bars vs. delta badges)
- Typography scale and spacing within glass cards
- Section heading style and separators

## Deferred Ideas

- Multi-pilot view (V2-05)
- Email report (V2-03)
- Live API connection (V2-01)
