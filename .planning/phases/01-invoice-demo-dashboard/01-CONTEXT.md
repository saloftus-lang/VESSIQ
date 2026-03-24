# Phase 1: Invoice Demo Dashboard - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Build `dashboard.html` — a standalone HTML invoice chargeback audit demo. A prospect opens the file and within 30 seconds sees $284K in overcharges, drills into a disputed invoice line-by-line, and calculates their own ROI. Deliverables: `dashboard.html` at the project root and `/fonts/` directory with self-hosted Inter and JetBrains Mono woff2 files.

This phase does NOT include `founder.html` (Phase 2), live API integration, authentication, mobile layout, or any build tooling.

</domain>

<decisions>
## Implementation Decisions

### File Placement
- **D-01:** `dashboard.html` lives at the project root — `/dashboard.html`. Not in `frontend/` or any subdirectory. Path matches REQUIREMENTS.md spec.

### Font Delivery
- **D-02:** Fonts are self-hosted. Download Inter variable woff2 and JetBrains Mono variable woff2, commit to `/fonts/` directory. Declare via `@font-face` with `font-display: swap` in the `<style>` block. Do NOT use Google Fonts CDN `<link>` tags — violates DS-05 offline-safe requirement. This satisfies DS-05 and REL-01 (no multi-origin CDN dependency for fonts).

### Data Volume
- **D-03:** The `DATA` array contains 20–25 invoice rows. This is enough to make carrier and date filters feel meaningful, covers all required carriers (MAEU, MSCU, EGLV, HLCU, PSHA, BNSF), includes all charge types (BAF, THC, D&D, Duplicate, Unauthorized), and has a realistic mix of dispute statuses (Pending, Filed, Won, Recovered). KPI tile totals (847 audited, 288 overcharges, $187,500 recovery, 68% win rate) are derived by summing the DATA array — the array values must be crafted so they aggregate to exactly these KPI totals.

### Claude's Discretion
- Whether to start from `demo/index.html` as a structural foundation or build from scratch — Claude decides. The `demo/index.html` has identical CSS token names and the header pattern; starting from it may save time. The `frontend/dashboard.html` renderAll()/state pattern is also available as a reference.
- JS organization within the single HTML file (function ordering, inline comments)
- Animation sequencing details beyond what is specified in the UI-SPEC interaction contracts
- Exact data values for the 20–25 DATA rows (must pass the Maritime Data Credibility Checklist in UI-SPEC.md)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Design Contract (primary source of truth for all visual/interaction decisions)
- `.planning/phases/01-invoice-demo-dashboard/01-UI-SPEC.md` — Complete design contract: color tokens, spacing scale, typography, glassmorphism rules, all 9 component specs, layout grid, copywriting, interaction contracts (state machine, row expand, GSAP counters, ApexCharts init), maritime data checklist, CDN stack (pinned versions), known bugs and mitigations. **Read this in full before writing a single line of CSS or JS.**

### Requirements
- `.planning/REQUIREMENTS.md` — 25 requirements for this phase: DS-01 through DS-07, INV-01 through INV-13, REL-01 through REL-05

### Roadmap and Phase Goal
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria (5 verifiable conditions)

### Code References
- `demo/index.html` — Reference for VESSIQ CSS token names, header/logo HTML structure, glassmorphism base patterns. Same color tokens as UI-SPEC.
- `frontend/dashboard.html` — Reference for renderAll() pattern, centralized state object, event delegation on table, tab/filter state management.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `demo/index.html`: CSS custom property block with exact token names matching UI-SPEC (--navy, --blue, --accent, --green, --red, --yellow, --gray-*). Header/logo HTML structure (logo-mark + logo-text + logo-sub + header-badge) can be adapted directly. Glassmorphism border patterns.
- `frontend/dashboard.html`: `renderAll()` pattern, centralized `state` object, event delegation approach on containers, filter/tab click handlers with classList toggling.

### Established Patterns
- State management: single `state = { selectedCarrier, dateRange, expandedRowId, roiInput }` object, all mutations go through `setState(patch)` then `render()`
- Chart updates: `chart.updateSeries()` — never destroy + reinitialize ApexCharts
- Event delegation: one listener on `<tbody>`, `event.target.closest('tr[data-invoice-id]')` to detect row clicks

### Integration Points
- No backend integration — `dashboard.html` is fully self-contained
- Fonts served from `/fonts/` relative path (works with `python3 -m http.server` from project root)
- CDN libraries (ApexCharts 3.54.1, GSAP 3.12.5) loaded from jsDelivr pinned URLs

</code_context>

<specifics>
## Specific Ideas

- KPI values must aggregate mathematically from the DATA array: 847 total rows, 288 with overcharge > 0, sum of overcharge amounts = $187,500, won/(won+filed) = 68%. Craft data carefully.
- Maritime Data Credibility Checklist (UI-SPEC.md Maritime section) must be checked against all DATA rows before considering INV-09 and REL-05 satisfied.
- ApexCharts ghost background bug mitigations (from STATE.md and UI-SPEC.md Known Bugs section) are non-negotiable — hardcode `theme: { mode: 'dark' }` + `chart: { background: 'transparent' }` from init.
- Safari `backdrop-filter` requires both `-webkit-backdrop-filter` and a non-transparent `background-color` fallback — required for DS-04.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-invoice-demo-dashboard*
*Context gathered: 2026-03-24 via /gsd:discuss-phase*
