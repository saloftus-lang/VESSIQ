# Project Research Summary

**Project:** VESSIQ — Invoice Chargeback Audit Demo + Founder Ops Dashboard
**Domain:** Standalone HTML dashboards — B2B SaaS sales demo + internal founder ops
**Researched:** 2026-03-24
**Confidence:** HIGH (stack and architecture), MEDIUM (features and pitfalls)

## Executive Summary

VESSIQ needs two standalone HTML files: a sales demo dashboard that converts logistics buyers in under 60 seconds, and an internal founder ops dashboard Sean can open and read at a glance. The hard constraint is no build pipeline — everything ships as self-contained HTML. Research confirms this is a solved pattern with clear best practices: vanilla CSS with custom properties, ApexCharts via CDN for charts, GSAP for entrance animations, and a thin centralized state object driving render functions. The existing `frontend/dashboard.html` already demonstrates the right baseline — the new files extend that pattern rather than invent a new one.

The most important finding from features research is that the invoice audit demo must produce three "aha" moments in sequence: the hero overcharge number on load, the line-item drill-down on first row click, and the ROI calculator close. Everything else is supporting infrastructure for those three interactions. The architecture recommendation — single `DATA` const, `setState()` dispatcher, named render functions — is specifically designed to make those interactions reliable and fast to build.

The top risk is demo environment failure: CDN dependencies that break on conference room WiFi, fake data that signals inauthenticity to domain experts, and glassmorphism effects that disappear on Safari. All three are preventable with known mitigations, but each requires deliberate action before any live demo. Build order matters: get the data structure right first (domain-accurate, numbers that sum), then build interactions, then polish visual effects.

---

## Key Findings

### Recommended Stack

The stack is intentionally minimal — zero build tools, everything loaded via CDN or written directly. ApexCharts is the clear chart winner for this use case: SVG rendering means crisp currency labels, tooltips render as DOM elements (not canvas), and the dark theme is a single config property. Pin to `apexcharts@3.54.1` — floating `@latest` is dangerous in production HTML files without a lock file.

CSS is written directly with CSS custom properties using a two-tier token system (primitives + semantic aliases). No Tailwind CDN — it is explicitly labeled dev-only by Tailwind's own team and adds 400 KB runtime. GSAP core (free, ~30 KB gzipped) handles counter animations and staggered card entrances. Inter variable font (~17 KB) via Google Fonts covers all weights 300–700 in a single file.

**Core technologies:**
- ApexCharts 3.54.1: charts — SVG rendering, DOM tooltips, built-in dark mode, sparkline support
- Vanilla CSS + custom properties: styling — zero dependencies, full design token control, no FOUC risk
- GSAP 3.12.5 core (free tier): animations — counter animations, staggered entrances, professional timelines
- Inter variable font: typography — B2B SaaS standard, designed for screen readability at small sizes
- JetBrains Mono: monospace font — container numbers, EDI codes, currency amounts in tables

**Critical version/config requirements:**
- Always pin ApexCharts to an exact version number, never `@latest`
- Always load GSAP as UMD bundle (not ESM) so it works over `file://` protocol if needed
- Always include both `backdrop-filter` and `-webkit-backdrop-filter` for Safari support

### Expected Features

The invoice audit demo is a sales artifact, not a product. Its only job is to generate three emotional responses in sequence. Feature decisions should be made against that goal, not against completeness.

**Must have (table stakes for credibility):**
- 4 KPI tiles: Total Invoiced (847), Overcharge Rate (34%), Total Overcharged ($284K), Recovered ($187.5K)
- Invoice table with color-coded status badges (Disputed / Won / Pending / Approved)
- One-invoice drill-down panel: contracted rate vs. billed rate, delta, auto-generated dispute language
- Error type breakdown chart (donut): BAF miscalc, unauthorized surcharges, duplicate billing, THC, D&D
- Carrier filter (Maersk, MSC, Hapag-Lloyd, CMA CGM, Evergreen, COSCO)
- Date range toggle (Month / Quarter / Year)

**Should have (differentiators that close deals):**
- ROI calculator: buyer enters monthly freight spend, sees estimated recovery and VESSIQ fee
- D&D validation panel showing FMC compliance flags
- Confidence score badge on each disputed invoice
- Source format badges (EDI 310 / PDF / CSV) proving normalization capability
- "Money left on table" annual exposure callout

**Founder ops must have:**
- Weekly focus block (this week's ONE thing)
- KPI tiles: MRR, Pilots Active, Deals in Progress, Runway
- Pilot tracker table with health scorecard (red/yellow/green per customer)
- This week's tasks + blocked items (3 items max per column)
- Phase progress tracker (visual timeline of expansion roadmap)

**Defer to later:**
- Real API data connections (both dashboards use hardcoded data)
- User auth or login
- Editable fields in either dashboard
- Real-time notification system
- Actual PDF export (fake button is sufficient for demo)

### Architecture Approach

Both files follow a thin MVC-like pattern in vanilla JS: a single `DATA` const at the top of the script block organized by domain object (not by UI section), a `state` object holding 4–6 UI fields, a `setState(patch)` function that calls `render()`, and named render functions for each UI section that read from both `DATA` and `state`. Event delegation on stable container elements handles all user interactions — no inline `onclick` handlers, no per-row listeners.

**Major components:**
1. `DATA` const — all fake data organized by domain object (chargebacks, carriers, summary); swap for API calls later by replacing these arrays with fetch responses of the same shape
2. `state` object + `setState()` — centralized UI state (activeTab, selectedCarrier, expandedRowId, dateRange); single source of truth for all render decisions
3. Named render functions — one function per UI section (renderKPIs, renderTable, renderFilters); each reads from DATA and state, writes innerHTML to a cached DOM ref
4. CSS token system — two-tier custom properties (primitive colors + semantic aliases); shared verbatim between both files via a labeled `:root` block
5. Event delegation layer — single listener per interactive container (table, filter group, calculator); never per-row

### Critical Pitfalls

1. **CDN failure in offline demo environments** — Conference room firewalls and captive portals will silently break Google Fonts, ApexCharts CDN, and GSAP. Prevention: test the file with WiFi off before any demo. For high-stakes demos, inline the chart library and embed fonts as base64 data URIs.

2. **Fake data that signals inauthenticity** — Maritime finance buyers will spot round dollar amounts, sequential invoice numbers, wrong SCAC codes, and impossible port combinations immediately. Prevention: use real SCAC codes (MAEU=Maersk, MSCU=MSC, CMDU=CMA CGM, HLCU=Hapag-Lloyd), real UN/LOCODEs (USLAX, CNSHA, SGSIN), ISO 6346 container numbers, non-round amounts with cents, and carrier-realistic invoice number formats.

3. **Numbers that don't reconcile** — Enterprise finance buyers add KPI card numbers in their heads. "Total Recovered: $187,500" must equal the sum of resolved dispute rows in the table. Prevention: derive all summary stats from the `DATA` array using computed sums — never hardcode KPI tiles independently from detail data.

4. **Glassmorphism invisible on Safari** — `backdrop-filter` requires `-webkit-backdrop-filter` prefix in all current Safari versions AND requires a semi-transparent `background-color` (not `transparent`). On dark dashboards, the glass background must be lighter than the surrounding dark. Prevention: always declare both prefixes, test on Safari 17+ before demos, add `@supports` fallback.

5. **ApexCharts ghost background on dark mode** — Known open bug: initializing ApexCharts with `theme: { mode: 'dark' }` then opening the file on a system with `prefers-color-scheme: light` can leave dark squares inside the chart container. Prevention: hardcode dark mode, do not build a theme toggle, set `background: 'transparent'` on chart init, and set `background: transparent !important` on the chart container div in CSS.

---

## Implications for Roadmap

### Phase 1: Foundation — Data Structure + Static Shell

**Rationale:** All interactive features depend on having correct, domain-accurate data. Getting the DATA structure right first prevents rework across every subsequent phase. The architecture recommendation is explicit: data organized by domain object, not by UI section.

**Delivers:** Both HTML files with correct data structure (domain-accurate fake data), shared CSS token system, and static HTML shell with correct layout grid.

**Addresses:** Pitfall 2 (fake data) and Pitfall 7 (numbers don't reconcile) — these are the hardest to fix late.

**Avoids:** Organizing data by UI section (anti-pattern identified in ARCHITECTURE.md that causes rework when data changes).

**No research needed:** Well-documented patterns.

---

### Phase 2: Invoice Audit Demo — Table Stakes Interactions

**Rationale:** The three "aha" moments must work before any polish. This phase builds the core demo loop: KPI tiles, invoice table, and the drill-down panel. The drill-down is the most important single interaction.

**Delivers:** Functional invoice audit demo that can be shown to a prospect. KPI tiles, sortable/filterable invoice table, one-invoice drill-down panel with line-item breakdown.

**Implements:** `setState()` / render function pattern, event delegation on table, cached DOM refs.

**Avoids:** Pitfall 1 (CDN failure) — test offline after this phase. Pitfall 9 (z-index conflicts) — establish z-index scale when building the drill-down panel/modal.

---

### Phase 3: Invoice Audit Demo — Differentiators + Charts

**Rationale:** Charts and the ROI calculator are the differentiating features that convert technical buyers. They come after the core table interactions are stable because they depend on the data structure being locked.

**Delivers:** Error type donut chart, carrier breakdown chart, ROI calculator widget, date range toggle, dispute status funnel, source format badges, confidence score badges.

**Uses:** ApexCharts 3.54.1 (initialized inside `DOMContentLoaded`, dark mode hardcoded). GSAP counter animations for KPI tiles on load.

**Avoids:** Pitfall 5 (chart tooltip clipping) — ApexCharts uses DOM tooltips, but still test all edge cases. Pitfall 6 (ApexCharts ghost background) — hardcode `theme: { mode: 'dark' }` and `background: 'transparent'` from the start.

---

### Phase 4: Founder Ops Dashboard

**Rationale:** Independent from the sales demo — can be built in parallel or sequentially. Lower stakes than the demo (internal use only) but follows the same architecture patterns.

**Delivers:** Weekly focus block, KPI tiles (MRR/pilots/runway), pilot tracker with health scorecard, task list, phase progress tracker, benchmark comparison panel.

**Implements:** Same `DATA` / `state` / render function pattern as the invoice demo. Shared CSS token system (copy `:root` block verbatim).

**No research needed:** Follows the same established patterns as Phase 2–3.

---

### Phase 5: Polish + Demo Hardening

**Rationale:** Final pass before any live demo. Focuses specifically on the failure modes identified in pitfalls research: offline resilience, Safari compatibility, screen share layout testing.

**Delivers:** Offline-safe demo (CDN dependencies tested with WiFi off, fallback fonts), Safari-tested glassmorphism, responsive layout verified at 1024px/1280px/1440px, z-index scale finalized, scrollbar styling, print styles.

**Avoids:** Pitfall 1 (CDN failure), Pitfall 3 (Safari glassmorphism), Pitfall 4 (3D CSS layer explosion), Pitfall 8 (mobile layout at screen-share widths), Pitfall 10 (low-contrast text under video compression).

**Includes:** Maritime domain credibility checklist review (SCAC codes, LOCODEs, ISO 6346 container numbers, voyage number formats, realistic per-TEU dollar ranges).

---

### Phase Ordering Rationale

- Data structure first because all render functions depend on `DATA` shape — changing shape later means rewriting render functions
- Core interactions before charts because the drill-down is the highest-stakes demo moment and must be rock-solid
- Charts after core interactions because they're isolated components that don't affect state architecture
- Founder ops dashboard is independent and lower-stakes — ideal to build after the demo loop is proven
- Hardening last because it requires a complete feature set to test against

### Research Flags

Phases with well-documented patterns (no additional research needed):
- **Phase 1:** CSS custom properties and HTML data structure — canonical, well-documented
- **Phase 2:** Vanilla JS state + event delegation — well-established pattern, existing VESSIQ codebase confirms approach
- **Phase 3:** ApexCharts — strong official docs, pitfalls already identified
- **Phase 4:** Follows same patterns as Phase 2
- **Phase 5:** All pitfalls pre-identified in PITFALLS.md — execution, not research

No phases require `/gsd:research-phase` — all patterns are established and the risks are known.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Core recommendations verified via official docs; ApexCharts choice confirmed against existing VESSIQ codebase patterns; only GSAP licensing is MEDIUM |
| Features | MEDIUM | Industry benchmarks sourced from freight audit vendors (potential bias); the 80% ocean error rate is a high-end figure — use 30–45% with serious buyers; interactive demo best practices are community-sourced |
| Architecture | HIGH | Analyzed directly against existing `frontend/dashboard.html`; patterns confirmed via canonical CSS-Tricks and MDN sources |
| Pitfalls | MEDIUM-HIGH | CSS/browser pitfalls are HIGH confidence (well-documented browser behavior); ApexCharts dark mode bug is MEDIUM (open GitHub issues, not official docs); domain data accuracy rules are HIGH (SCAC codes, ISO 6346 are industry standards) |

**Overall confidence:** HIGH for build decisions, MEDIUM for demo content claims.

### Gaps to Address

- **GSAP licensing for premium plugins:** GSAP core is confirmed free. If any premium plugin (SplitText, etc.) is considered later, verify license before adding. For this project, only core is needed.
- **ApexCharts dark mode bug:** Two open GitHub issues confirm the behavior. Mitigation is known (hardcode theme, set transparent background) but verify this resolves it during Phase 3 implementation.
- **80% overcharge rate claim:** VESSIQ strategy documents cite this figure. Use it in demos but be prepared to contextualize — "30–45% contain material billing errors" is more defensible with a skeptical CFO buyer.
- **Offline demo resilience:** The mitigation (inline libraries or local serving) is clear, but the right approach depends on how demos are delivered (laptop standalone vs. Railway-hosted). Confirm delivery method in Phase 5.

---

## Sources

### Primary (HIGH confidence)
- Direct code analysis: `/Users/seanloftus/Desktop/VESSIQ/frontend/dashboard.html` — existing patterns
- VESSIQ internal strategy documents (VESSIQ_Maritime_Application.md, VESSIQ_Wedge_Analysis.md, VESSIQ_Strategy_Updated.md) — product and feature decisions
- MDN Web Docs — file:// CORS restrictions, CSS animation performance, backdrop-filter support
- ApexCharts official docs — chart configuration, theme options
- Tailwind CSS official docs — Play CDN explicitly labeled dev-only
- GSAP official site — free tier licensing confirmation

### Secondary (MEDIUM confidence)
- CSS-Tricks: state management in vanilla JS, CSS architecture patterns
- Smashing Magazine: GPU animation compositing, CSS specificity
- National Transportation Institute / Zero Down Supply Chain / Gartner Logistics 2025 — freight audit recovery rate benchmarks (2–8% of freight spend)
- Navattic / Reprise — interactive demo best practices
- Beacon / SeaRates — SCAC code reference

### Tertiary (LOW confidence)
- ApexCharts GitHub issues #4028 and #3387 — dark mode ghost background bug (open issues, not resolved)
- Extrapolated annual savings figures ($150K–$750K/year) — derived from recovery rate percentages, not a single sourced figure

---

*Research completed: 2026-03-24*
*Ready for roadmap: yes*
