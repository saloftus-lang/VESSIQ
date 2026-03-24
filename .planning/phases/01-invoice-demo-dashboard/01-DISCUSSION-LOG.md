# Phase 1: Invoice Demo Dashboard - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

---

**Date:** 2026-03-24
**Phase:** 1 — Invoice Demo Dashboard
**Mode:** discuss

---

## Context Gate

**No CONTEXT.md existed.** User chose "Run discuss-phase first" before planning.

---

## Prior Context Loaded

- PROJECT.md: standalone HTML, dark navy design system, CSS 3D depth, realistic fake data baked in
- REQUIREMENTS.md: 25 requirements (DS-01–07, INV-01–13, REL-01–05)
- STATE.md: blockers noted (ApexCharts ghost bg bug, Safari backdrop-filter)
- UI-SPEC.md: Complete visual/interaction design contract already approved

No prior phase CONTEXT.md files (this is Phase 1).

---

## Codebase Scout

Existing files inspected:
- `demo/index.html` (1057 lines) — VESSIQ step-by-step ocean freight demo, same CSS tokens as UI-SPEC, wizard flow architecture
- `frontend/dashboard.html` (875 lines) — vessel operations dashboard, different color scheme, useful for JS patterns
- `marketing/index.html` (591 lines) — landing page, not directly relevant

No existing `dashboard.html` at project root.

---

## Gray Areas Analysis

The UI-SPEC.md locked down all visual and interaction design decisions. Three genuine open questions remained for the planner:

1. **File path** — project root vs. `frontend/` directory
2. **Font delivery** — self-hosted vs. Google Fonts CDN
3. **Data volume** — 20–25 rows vs. 40–50 rows

---

## Discussion Q&A

### Area: File path

**Question:** Where should dashboard.html live in the repo?

| Option | Description |
|--------|-------------|
| Project root (chosen) | `/dashboard.html` — simplest path, matches REQUIREMENTS.md spec |
| `frontend/` directory | `/frontend/dashboard.html` — alongside existing frontend/index.html (already occupied) |

**Answer:** Project root

---

### Area: Fonts

**Question:** How should fonts be delivered? UI-SPEC prefers self-hosted for DS-05 offline compliance.

| Option | Description |
|--------|-------------|
| Self-hosted /fonts/ (chosen) | Download Inter + JetBrains Mono woff2, commit to /fonts/, use @font-face |
| Google Fonts CDN | Faster to ship, violates DS-05 (not offline-safe) |

**Answer:** Self-hosted /fonts/

---

### Area: Data volume

**Question:** How many invoice rows in the DATA array?

| Option | Description |
|--------|-------------|
| 20–25 rows (chosen) | Representative sample, all carriers/charge types covered, filters feel meaningful |
| 40–50 rows | More scroll depth, longer to write credibly |

**Answer:** 20–25 rows

---

## Todos Cross-Referenced

No pending todos matched Phase 1 scope.

---

## Decisions Summary

| ID | Decision |
|----|----------|
| D-01 | `dashboard.html` at project root |
| D-02 | Fonts self-hosted in `/fonts/` via `@font-face` — no Google Fonts CDN |
| D-03 | 20–25 DATA rows, values crafted to aggregate to exact KPI totals |
