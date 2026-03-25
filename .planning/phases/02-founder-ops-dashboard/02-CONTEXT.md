# Phase 2: Founder Ops Dashboard - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Build `founder.html` — a private, single-user internal dashboard for Sean. It shows pilot health KPIs, a weekly ops task list with localStorage persistence, a freeform notes widget with localStorage persistence, and industry benchmark comparison cards. This is NOT a client-facing tool — it is Sean's daily internal view.

Scope anchor: FND-01 through FND-07 from REQUIREMENTS.md. No new capabilities beyond what's listed there.

</domain>

<decisions>
## Implementation Decisions

### Visual Theme
- **D-01:** Dark navy glassmorphism. Body background `#0B1F3A`. Glass cards use `background: rgba(255,255,255,0.05)`, `backdrop-filter: blur(16px) saturate(180%)`, `-webkit-backdrop-filter: blur(16px) saturate(180%)`, `border: 1px solid rgba(255,255,255,0.10)`, `box-shadow: 0 4px 24px rgba(0,0,0,0.4)`.
- **D-02:** Flat glass — no CSS 3D perspective transforms or hover tilt. Clean and fast.
- **D-03:** Header: same dark navy header structure as `dashboard.html` but the header badge reads "Founder View" in amber/gold (`background: rgba(245,158,11,0.15)`, `border: 1px solid rgba(245,158,11,0.3)`, `color: #F59E0B`) instead of the accent blue used on the demo dashboard.
- **D-04:** Text colors: headings `#FFFFFF`, body text `#E2E8F0`, muted labels `#94A3B8`. No light-mode colors.

### Page Layout
- **D-05:** Single-page scroll. No tab navigation. All sections visible by scrolling from top to bottom.
- **D-06:** Page flow (top to bottom):
  1. Header (logo + "Founder View" badge)
  2. KPI tiles row (3 tiles: Active Pilots, Invoices Processed, Total Savings)
  3. `This Week` section heading
  4. Tasks widget and Notes widget side-by-side (50% / 50% split)
  5. Industry Benchmarks section heading
  6. Benchmark cards row (3 cards)
- **D-07:** Max page width: `1200px`, centered, `padding: 0 48px`. Same horizontal rhythm as `dashboard.html`.

### Pilot KPI Data
- **D-08:** Active Pilots tile: **1** (Pasha Hawaii). This is the real current state.
- **D-09:** Invoices Processed tile: **23** — ties to the `DATA.length` in `dashboard.html` for consistency.
- **D-10:** Total Savings Identified tile: **$187,500** — ties to the Won+Recovered overchargeAmount sum from `dashboard.html` DATA array.
- **D-11:** All 3 KPI tiles animate with GSAP count-up on `DOMContentLoaded` — same pattern as `dashboard.html`. Use `gsap.from('.kpi-tile', { y: 20, opacity: 0, stagger: 0.08, duration: 0.5 })` for entrance, then `gsap.to(obj, { v: val, ... })` for counters.

### Tasks Widget
- **D-12:** Pre-seed with 3 example weekly tasks on first load (when localStorage is empty):
  1. "Follow up with Heather Brown re: Pasha pilot scope"
  2. "Prep ROI summary for first audit batch"
  3. "Identify 2nd pilot prospect outreach"
- **D-13:** Task interaction: checkbox to mark complete (strikethrough text + muted color), delete button (×) per row, input field + "Add" button to add new tasks.
- **D-14:** Persist task list (array of `{id, text, done}`) to `localStorage` under key `'fnd-tasks'`. Load on page init.

### Notes Widget
- **D-15:** Single `<textarea>` that auto-saves to `localStorage` under key `'fnd-notes'` on every `input` event. No save button. Placeholder: "Brain dump, follow-ups, ideas…"
- **D-16:** Notes widget height: `min-height: 180px`, auto-expanding (scrollable, not fixed).

### Industry Benchmarks
- **D-17:** Three benchmark cards — benchmark values:
  1. **Invoice Error Rate** — Industry avg: 38%, VESSIQ target: <5%
  2. **Avg Detention Days** — Industry avg: 4.2 days, VESSIQ target: <1 day
  3. **Dispute Win Rate** — Industry avg: 32%, VESSIQ target: 68% (matches `dashboard.html`)
- **D-18:** Benchmark visualization is Claude's discretion — a progress bar showing VESSIQ's position vs. industry average, or a delta badge showing the advantage. Whatever looks clearest for each metric.

### Claude's Discretion
- Benchmark card visualization style (progress bars vs. delta badges vs. both)
- Typography scale and spacing within glass cards
- Responsive behavior at narrow widths (not a priority but avoid broken layouts)
- Section heading style (font size, weight, separator line vs. none)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing dashboard (primary reference)
- `dashboard.html` — The Phase 1 invoice dashboard. Copy self-hosted font declarations, CSS token set (`:root` block), GSAP CDN link, header HTML structure, and KPI tile HTML/CSS patterns verbatim. The glassmorphism card style for `founder.html` is the DARK version (D-01) not the light version currently in `dashboard.html`.

### Requirements
- `.planning/REQUIREMENTS.md` — FND-01 through FND-07 are the complete requirement list for this phase.

### Roadmap
- `.planning/ROADMAP.md` — Phase 2 goal, success criteria, and dependency on Phase 1.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dashboard.html` CSS token block (`:root` — same variables `--navy`, `--blue`, `--accent`, `--green`, `--red`, `--yellow`, `--white`) — copy verbatim, only body background changes to `--navy`
- `dashboard.html` header HTML — copy structure, swap badge text + color
- `dashboard.html` KPI tile HTML + GSAP count-up pattern — copy and adapt for 3 tiles
- Self-hosted fonts: `/fonts/inter-variable.woff2` and `/fonts/jetbrains-mono-variable.woff2` — already exist on disk, use same `@font-face` declarations

### Established Patterns
- State + render pattern from `dashboard.html` (`state` object + `setState(patch)` → `render()`) — use for task list state
- `localStorage` persistence: load on `DOMContentLoaded`, save on every mutation
- CDN pattern: GSAP from `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` (pinned version)

### Integration Points
- No link between `founder.html` and `dashboard.html` at runtime — completely independent files
- Both files share the same `/fonts/` directory (must be served with a local HTTP server, not `file://`)

</code_context>

<specifics>
## Specific Ideas

- The "Founder View" header badge in amber/gold makes it immediately obvious this is the internal tool, not the client demo — important distinction when Sean is sharing his screen on a sales call
- Pre-seeding tasks with Pasha-specific items (Heather Brown follow-up) makes the dashboard feel lived-in from the first open
- The $187,500 savings number on the founder dashboard ties directly to the demo dashboard — same story, same data, reinforces credibility

</specifics>

<deferred>
## Deferred Ideas

- Multi-pilot view (filter by customer) — V2-05 in REQUIREMENTS.md, not this phase
- Email report from founder dashboard — V2-03, not this phase
- Live API connection to FastAPI backend — V2-01, not this phase

</deferred>

---

*Phase: 02-founder-ops-dashboard*
*Context gathered: 2026-03-25*
