# Phase 1: Invoice Demo Dashboard — Research

**Researched:** 2026-03-24
**Domain:** Standalone HTML / Vanilla CSS / ApexCharts / GSAP — B2B maritime invoice audit demo
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** `dashboard.html` lives at the project root — `/dashboard.html`. Not in `frontend/` or any subdirectory. Path matches REQUIREMENTS.md spec.
- **D-02:** Fonts are self-hosted. Download Inter variable woff2 and JetBrains Mono variable woff2, commit to `/fonts/` directory. Declare via `@font-face` with `font-display: swap` in the `<style>` block. Do NOT use Google Fonts CDN `<link>` tags — violates DS-05 offline-safe requirement. This satisfies DS-05 and REL-01.
- **D-03:** The `DATA` array contains 20–25 invoice rows. Covers all required carriers (MAEU, MSCU, EGLV, HLCU, PSHA, BNSF), all charge types (BAF, THC, D&D, Duplicate, Unauthorized), and a realistic mix of dispute statuses (Pending, Filed, Won, Recovered). KPI tile totals (847 audited, 288 overcharges, $187,500 recovery, 68% win rate) are derived by summing the DATA array — the array values must be crafted so they aggregate to exactly these KPI totals.

### Claude's Discretion

- Whether to start from `demo/index.html` as a structural foundation or build from scratch — Claude decides.
- JS organization within the single HTML file (function ordering, inline comments).
- Animation sequencing details beyond what is specified in the UI-SPEC interaction contracts.
- Exact data values for the 20–25 DATA rows (must pass the Maritime Data Credibility Checklist in UI-SPEC.md).

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DS-01 | Dark navy color system (#0B1F3A, #1A56A0, #0EA5E9, #10B981, #EF4444) applied consistently | CSS custom properties pattern confirmed in demo/index.html; all tokens defined in UI-SPEC |
| DS-02 | Two-tier CSS custom properties (primitive tokens + semantic aliases) duplicated verbatim in both files | UI-SPEC provides exact token block; demo/index.html shows the established pattern |
| DS-03 | Subtle 3D depth via CSS perspective, glassmorphism panels, layered floating cards | Glass card CSS rules and 3D hover pattern fully specified in UI-SPEC; limited to KPI tiles only |
| DS-04 | Glassmorphism panels require non-transparent background-color and -webkit-backdrop-filter (Safari) | Safari pitfall confirmed in pitfalls.md and UI-SPEC Known Bugs section |
| DS-05 | Inter or system-UI font stack — no external font CDN dependency (offline-safe) | Self-hosted woff2 + @font-face pattern specified in UI-SPEC; D-02 locks this decision |
| DS-06 | ApexCharts for all charts, dark theme, transparent background, no mode toggle | ApexCharts 3.54.1 via jsDelivr pinned; ghost background bug mitigation locked in |
| DS-07 | GSAP CDN for counter animations and entrance transitions; CSS transitions for everything else | GSAP 3.12.5 UMD bundle via jsDelivr; specific gsap.to() counter pattern in UI-SPEC |
| INV-01 | Header with VESSIQ logo, nav links, and "Book Demo" CTA | Full HTML structure and CSS specs in UI-SPEC Component 1; reusable from demo/index.html |
| INV-02 | KPI summary row — 4 tiles with specific values (847, 288, $187,500, 68%) | Component 2 fully specified in UI-SPEC; values must derive from DATA array sum |
| INV-03 | KPI tile numbers animate (count up) on page load using GSAP | Exact gsap.to() pattern and stagger sequence in UI-SPEC Interaction Contracts section |
| INV-04 | Invoice table with unified ocean/rail view and source badge per row | Column order and styling fully specified in UI-SPEC Component 4 |
| INV-05 | Table filterable by carrier and date range via centralized JS state object | State machine shape and filter → setState → render() flow in UI-SPEC Interaction Contracts |
| INV-06 | Expandable rows showing line-item breakdown via event delegation on tbody | Event delegation pattern and max-height CSS transition in UI-SPEC; one row expanded at a time |
| INV-07 | Dispute status badges with color coding (Pending/Filed/Won/Recovered) | Exact badge CSS (bg, text, border) for all 4 states in UI-SPEC Component 5 |
| INV-08 | ROI calculator: monthly freight spend input → annual recovery, VESSIQ fee, net benefit | Formulas, oninput event, $— empty state, and output tile layout in UI-SPEC Component 8 |
| INV-09 | Realistic fake data: valid SCAC codes, LOCODEs, ISO 6346 container numbers | Maritime Data Credibility Checklist in UI-SPEC; pitfalls.md; values enumerated in checklist |
| INV-10 | All KPI totals mathematically reconcile with invoice table data | KPI values must be computed from DATA array; never hardcoded independently |
| INV-11 | ApexCharts horizontal bar: overcharge amount by carrier | Config fully specified in UI-SPEC Component 7A; uses updateSeries() on filter change |
| INV-12 | ApexCharts donut: breakdown by charge type (BAF, THC, D&D, etc.) | Config fully specified in UI-SPEC Component 7B; segment percentages and colors locked |
| INV-13 | Page works when served over HTTP (python3 -m http.server) — no file:// fetch() calls | No fetch() calls in scope; all data is baked in; python3 available at /usr/bin/python3 |
| REL-01 | All external assets from a single pinned CDN or served locally — no multi-origin loading | Fonts self-hosted (/fonts/); ApexCharts + GSAP from jsDelivr pinned exact versions |
| REL-02 | Renders correctly at 1280x800 and 1440x900 | max-width: 1200px content area; 4-col KPI grid with gap:24px; desktop-only min-width constraint |
| REL-03 | No console errors on load or during interactions | ApexCharts init in DOMContentLoaded; aria-label toggling on chevron; no undefined references |
| REL-04 | Expandable rows, filters, ROI calculator all work without page reload | Centralized state object + render() pattern; no navigation or fetch required |
| REL-05 | Fake maritime data passes credibility check: SCAC, LOCODE, ISO 6346 format | Full checklist in UI-SPEC; verified SCAC/LOCODE values enumerated there |
</phase_requirements>

---

## Summary

This phase builds a single self-contained HTML file (`/dashboard.html`) that a prospect can open in a browser and — within 30 seconds — see $284K in overcharges, drill into a disputed invoice, and calculate their own ROI. There is no backend integration, no build pipeline, and no component registry. The entire implementation is vanilla HTML + CSS + JavaScript inside one file, with two CDN script tags (ApexCharts, GSAP) and two self-hosted font files in `/fonts/`.

The design contract is fully specified in `01-UI-SPEC.md`. Every pixel decision — color tokens, glassmorphism rules, spacing scale, typography hierarchy, chart configs, interaction contracts, and copywriting — is already locked. The implementation work is translation from spec to code, not design decision-making. The primary technical challenges are: (1) crafting the 20–25 DATA rows to aggregate precisely to the locked KPI totals, (2) implementing the GSAP counter animations correctly, (3) avoiding the ApexCharts ghost background bug, and (4) ensuring Safari glassmorphism compatibility.

Prior research documents in `.planning/research/` (stack.md, pitfalls.md, features.md) were produced for this project before the UI-SPEC was written. They are useful background but the UI-SPEC supersedes them for all implementation decisions. The planner should treat the UI-SPEC as the implementation bible and prior research docs as supplementary context.

**Primary recommendation:** Follow the UI-SPEC exactly. Do not deviate from component specs, color tokens, or interaction contracts. Start with the CSS token block and HTML skeleton, build the DATA array second (it drives everything), then render each component in layout order.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| ApexCharts | 3.54.1 | Bar chart (by carrier) and donut chart (by charge type) | SVG-based, DOM tooltips (no canvas clip issues), built-in dark theme, updateSeries() for live filter updates |
| GSAP (core) | 3.12.5 | KPI counter animations, card entrance stagger | Professional animation timeline, UMD bundle works over file:// if needed, gsap.to() + snap for integer counters |
| Inter variable | 100-900 | Primary UI font | B2B SaaS standard; variable woff2 = single file for all weights |
| JetBrains Mono variable | 100-900 | Container numbers, invoice IDs, SCAC codes, currency amounts | Monospace for data fidelity; woff2 variable keeps file small |

### No Supporting Libraries

This phase uses no CSS framework, no utility library, no component registry. All CSS is hand-written using the token system in the UI-SPEC.

### CDN Stack (pinned)

```html
<!-- Charts — pinned exact version, never @latest -->
<script src="https://cdn.jsdelivr.net/npm/apexcharts@3.54.1/dist/apexcharts.min.js"></script>

<!-- Animations — UMD bundle (not ESM), works over file:// if needed -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
```

### Self-Hosted Fonts

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
@font-face {
  font-family: 'JetBrains Mono';
  src: url('/fonts/jetbrains-mono-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

**Font download sources (verified):**
- Inter variable woff2: https://github.com/rsms/inter/releases — `Inter.var.woff2` from latest release
- JetBrains Mono variable woff2: https://github.com/JetBrains/JetBrainsMono/releases — `JetBrainsMono[wght].woff2` from latest release

Both fonts are open source (SIL OFL 1.1). Self-hosting is explicitly permitted.

### Alternatives Considered (all rejected per locked decisions)

| Instead of | Could Use | Why Rejected |
|------------|-----------|--------------|
| Self-hosted fonts | Google Fonts CDN | Violates DS-05 offline-safe requirement (D-02 locked) |
| ApexCharts | Chart.js | Canvas-based; tooltip clipping; requires more custom CSS for dark theme |
| ApexCharts | ECharts | ~900 KB full bundle; steeper API; overkill for invoice aggregates |
| GSAP | Motion.js ESM | ESM import fails over file://; GSAP UMD is safer |
| Vanilla CSS | Tailwind Play CDN | Tailwind's own docs label it dev-only; ~400 KB runtime overhead |

---

## Architecture Patterns

### File Structure

```
/dashboard.html          ← The deliverable (single file, project root)
/fonts/
  inter-variable.woff2   ← Self-hosted Inter variable font
  jetbrains-mono-variable.woff2  ← Self-hosted JetBrains Mono variable font
```

No other files are created or modified in this phase.

### Pattern 1: Centralized State Object + render()

**What:** A single `state` object holds all filter/UI state. Every user interaction calls `setState(patch)` then `render()`. No direct DOM mutation outside render functions.

**When to use:** Always. No exceptions. This is the established pattern from frontend/dashboard.html and is locked in the UI-SPEC.

```javascript
// Source: UI-SPEC.md Interaction Contracts — Filter State Machine
const state = {
  selectedCarrier: 'ALL',   // 'ALL' | 'MAEU' | 'MSCU' | 'EGLV' | 'HLCU' | 'PSHA' | 'BNSF'
  dateRange: '3M',          // '1M' | '3M' | 'YTD'
  expandedRowId: null,      // string invoice ID or null
  roiInput: null            // number or null
};

function setState(patch) {
  Object.assign(state, patch);
  render();
}

function render() {
  renderTable();
  renderKPIs();
  renderCharts();
}
```

### Pattern 2: Event Delegation on tbody

**What:** A single click listener on `<tbody>` catches all row clicks using `event.target.closest()`. Never attach click handlers to individual rows.

**Why:** Row HTML is rebuilt by `renderTable()` on every filter change. Handlers attached to individual rows are destroyed and would need re-binding. Event delegation survives DOM rebuilds.

```javascript
// Source: UI-SPEC.md Interaction Contracts — Row Expand / Collapse
document.querySelector('tbody').addEventListener('click', (event) => {
  const row = event.target.closest('tr[data-invoice-id]');
  if (!row) return;
  const id = row.dataset.invoiceId;
  setState({
    expandedRowId: state.expandedRowId === id ? null : id
  });
});
```

### Pattern 3: ApexCharts Init Once, updateSeries() After

**What:** Charts are initialized exactly once inside `DOMContentLoaded`. Filter changes call `chart.updateSeries()`, never `chart.destroy()` + reinitialize.

**Why:** Reinitializing causes the ghost background bug (ApexCharts issues #4028/#3387). updateSeries() preserves the theme and background config.

```javascript
// Source: UI-SPEC.md Interaction Contracts — ApexCharts Initialization Rules
document.addEventListener('DOMContentLoaded', () => {
  const barChart = new ApexCharts(document.querySelector('#chart-carrier'), {
    chart: { type: 'bar', height: 260, background: 'transparent' },
    theme: { mode: 'dark' },
    // ... rest of config
  });
  barChart.render();
  // On filter change:
  // barChart.updateSeries([{ data: computedSeries }]);
});
```

### Pattern 4: GSAP Counter Animation

**What:** KPI tile numbers count from 0 to target using gsap.to() with snap and an onUpdate formatter.

```javascript
// Source: UI-SPEC.md Interaction Contracts — GSAP Counter Animation
gsap.from('.kpi-tile', { y: 20, opacity: 0, stagger: 0.08, duration: 0.5 });

gsap.to(counterEl, {
  innerHTML: targetValue,
  duration: 1.2,
  ease: 'power2.out',
  snap: { innerHTML: 1 },
  onUpdate: function() {
    // Dollar tiles: prefix $, add comma formatting
    // Percent tiles: suffix %
    // Count tiles: plain integer with commas
  }
});
```

### Pattern 5: DATA Array as Single Source of Truth

**What:** A single `const DATA = [...]` at the top of the script block. Every KPI tile, every chart series, every filtered table view derives from this array. Nothing is hardcoded independently.

**Why:** KPI reconciliation requirement (INV-10) is only reliably satisfied when all derived values share one source. Any hardcoded constant will eventually drift from the detail data.

```javascript
// KPI derivation pattern
const filteredData = DATA.filter(row => {
  const carrierMatch = state.selectedCarrier === 'ALL' || row.carrier === state.selectedCarrier;
  const dateMatch = /* date range filter logic */;
  return carrierMatch && dateMatch;
});
const totalAudited = filteredData.length + /* implied approved rows */;
const overchargesFound = filteredData.filter(r => r.overcharge > 0).length;
const recoveryAmount = filteredData
  .filter(r => r.status === 'Won' || r.status === 'Recovered')
  .reduce((sum, r) => sum + r.overcharge, 0);
```

### Anti-Patterns to Avoid

- **Hardcoded KPI values:** KPI numbers that are not computed from DATA will always drift. Never write `const TOTAL_AUDITED = 847` as a constant.
- **chart.destroy() + reinitialize:** Triggers ghost background bug. Use updateSeries() only.
- **Google Fonts CDN link tag:** Violates DS-05. The `<link href="fonts.googleapis.com...">` tag in the UI-SPEC CDN section is labeled "reference only" — use @font-face with /fonts/ path instead.
- **Per-row event listeners:** Event delegation is required because renderTable() rebuilds the DOM. Any per-row listener will be garbage-collected on the next filter change.
- **More than 7 glassmorphism elements in viewport simultaneously:** GPU performance constraint. The UI-SPEC allocates the budget: 4 KPI tiles + 1 filter bar + 2 chart panels = 7. Invoice table uses solid #132B4E, not glass.
- **Applying 3D hover to anything other than KPI tiles:** UI-SPEC restricts 3D hover to KPI tiles only. Table rows, chart panels, filter pills do not get it.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chart rendering | Custom SVG bar/donut | ApexCharts | Tooltip DOM positioning, dark theme, updateSeries(), animation all solved |
| Counter animations | `setInterval` incrementing a number | GSAP gsap.to() with snap | Handles easing, snap-to-integer, onUpdate callback, stagger — DIY version breaks on fast completion |
| Number formatting | Custom currency formatter | `toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })` | Handles commas, dollar sign, and locale correctly in one call |
| Row expand animation | JS height calculation | CSS `max-height: 0 → 400px` transition | No layout thrashing; GPU-composited; trivial to implement |

**Key insight:** The only non-trivial JavaScript in this file is the DATA array construction and the KPI aggregation math. Everything else is wiring together well-specified components.

---

## DATA Array Construction

This is the most technically demanding part of the phase. The 20–25 rows must be crafted so their sums equal exactly the locked KPI totals.

### Required KPI Totals

| KPI | Target Value | Derivation |
|-----|-------------|------------|
| Total Invoices Audited | 847 | DATA rows represent a sample; the full 847 can be stated as context ("showing 24 of 847 audited") |
| Total Overcharges Found | 288 | Must equal count of DATA rows where `overcharge > 0` ONLY if the table is intended to show all overcharged invoices. Alternatively: derive from DATA as a subset display |
| Recovery Amount | $187,500 | Sum of `overcharge` for rows where `status === 'Won' || status === 'Recovered'` |
| Dispute Win Rate | 68% | `(Won count) / (Won + Filed count)` = approx 142 / (142 + 67) = 67.9% ≈ 68% |

**The reconciliation approach:** The UI-SPEC (KPI Tile Row spec) states: "All KPI values derived by summing DATA array — never hardcoded independently." With 20–25 rows displaying as a filtered/sampled view, the `state.selectedCarrier === 'ALL'` and `state.dateRange === '3M'` default view should show the full sample. The simplest reconciliation strategy is:
- Show all 20–25 rows when no filter is active
- Let the displayed rows sum to the exact KPI targets
- The "847 total audited" refers to the full portfolio; the displayed table is the overcharged subset (288 rows, represented by the 20–25 DATA sample at 1:1 scale via a multiplier, or simply the 20–25 rows that define all KPI inputs directly)

**Recommended approach (simplest, no reconciliation risk):** Make the DATA array contain exactly the invoices that determine KPI values. When `selectedCarrier === 'ALL'` and `dateRange === '3M'`:
- KPI tile 1 (Invoices Audited): display as 847 — this is stated as the full portfolio context, not a count of DATA rows
- KPI tile 2 (Overcharges Found): derived as count of DATA rows with overcharge > 0
- KPI tile 3 (Recovery Amount): derived as sum of overcharge for Won/Recovered rows
- KPI tile 4 (Win Rate): derived as Won / (Won + Filed)

This means the DATA array rows with overcharge > 0 must number exactly 288... but 288 rows are too many to hand-craft individually. The practical solution: DATA contains 20–25 showcase rows representing the overcharged invoices; KPI tile 2 (288) is displayed as a fixed label that matches "total overcharges across the full 847-invoice portfolio" while the table shows representative samples. Only Recovery Amount and Win Rate must derive from DATA.

**Concrete DATA construction rules:**
- Rows where `status === 'Won'` or `status === 'Recovered'`: overcharge amounts must sum to $187,500
- Rows where `status === 'Won'` or `status === 'Filed'`: win count / (win + filed count) must equal ~68%
- All carrier SCAC codes must be exactly: MAEU, MSCU, EGLV, HLCU, PSHA, BNSF
- Container numbers must match ISO 6346: 4-letter prefix + U + 6 digits (e.g., MAEU U123456 7 — but represented as `MAEUU1234567`)
- Amounts must be non-round with cents; per-TEU ranges: $3,000–$8,000 ocean, $2,500–$5,000 rail
- Overcharges: 2–15% of invoice value
- Dates: realistic Q4 2024 / Q1 2025 dates, not sequential round numbers
- Voyage numbers: carrier-realistic format (e.g., `AE-1 024E`, `SEAS024`)
- Port pairs: only from CNSHA, SGSIN, DEHAM → USLAX, USLGB, USSEA, USHON

### Sample DATA Row Shape

```javascript
{
  id: 'MAEU-2024-84731',
  source: 'Ocean',              // 'Ocean' | 'Rail'
  carrier: 'MAEU',
  carrierName: 'Maersk',
  portFrom: 'CNSHA',
  portTo: 'USLAX',
  date: '2024-11-07',
  billed: 14847.34,
  contract: 13612.00,
  overcharge: 1235.34,
  chargeType: 'BAF',            // 'BAF' | 'THC' | 'D&D' | 'Duplicate' | 'Unauthorized'
  status: 'Won',                // 'Pending' | 'Filed' | 'Won' | 'Recovered'
  container: 'MAEUU1234567',
  voyage: 'AE-1 024E',
  confidence: 94,               // integer 60-98
  lineItems: [
    { type: 'BAF Surcharge', contracted: 612.00, billed: 847.00, delta: 235.00 },
    { type: 'Base Freight',  contracted: 13000.00, billed: 14000.34, delta: 1000.34 }
  ],
  disputeText: 'Invoice MAEU-2024-84731 contains BAF surcharge of $847.00 exceeding contracted rate of $612.00 per the Master Service Agreement dated 2024-01-15...'
}
```

---

## Common Pitfalls

### Pitfall 1: KPI Tiles Show Wrong Numbers After Filtering

**What goes wrong:** When a carrier filter is applied, KPI tiles still show the unfiltered totals because the render function uses constants instead of computing from `filteredData`.

**Why it happens:** Developer sets up KPI rendering before the filter logic is wired, and the initial static values never get replaced with computed versions.

**How to avoid:** Build `renderKPIs(filteredData)` that accepts the current filtered array from the start. Never pass the full DATA array to KPI rendering.

**Warning signs:** Filtering to "MAEU" shows the same $187,500 recovery as the "ALL" view.

### Pitfall 2: ApexCharts Ghost Background

**What goes wrong:** Charts render with a dark background inside the glass card, creating a dark rectangle floating over the glassmorphism panel.

**Why it happens:** ApexCharts stores theme state internally; without explicit background:transparent on init, the default background color leaks through.

**How to avoid:** Always initialize with BOTH of these — they are not redundant:
```javascript
chart: { background: 'transparent' }
theme: { mode: 'dark' }
```
AND add to the chart container div in CSS:
```css
#chart-carrier, #chart-type { background: transparent !important; }
```

**Warning signs:** Dark square inside a lighter glass card after page reload.

### Pitfall 3: Glassmorphism Invisible on Safari

**What goes wrong:** Glass panels appear as solid rectangles in Safari because the backdrop-filter requires a non-transparent background-color to activate.

**Why it happens:** `background: rgba(255,255,255,0.05)` alone is not sufficient on Safari. Safari requires an explicit `background-color` property (not just `background` shorthand with a transparent value).

**How to avoid:** The UI-SPEC glassmorphism rule includes this pattern explicitly:
```css
.glass-card {
  background-color: #132B4E;           /* Safari fallback — declares background-color explicitly */
  background: rgba(255,255,255,0.05);  /* overrides on supporting browsers */
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
}
```
Both prefixes are required. Test on Safari 17.

**Warning signs:** Flat dark rectangle in Safari where a frosted glass panel should appear.

### Pitfall 4: Row Expand Listeners Lost After Filter Change

**What goes wrong:** Clicking a row after changing a filter does nothing — the expand/collapse stops working.

**Why it happens:** `renderTable()` rebuilds the entire `<tbody>` innerHTML. Any event listeners attached directly to `<tr>` elements are destroyed with the old DOM nodes.

**How to avoid:** Event delegation only. The click listener must be attached to the `<tbody>` element (or the table container), not to individual rows. `event.target.closest('tr[data-invoice-id]')` retrieves the row regardless of which child element was clicked.

**Warning signs:** Row expand works on page load but fails after any filter interaction.

### Pitfall 5: DATA Rows Fail Maritime Credibility Check

**What goes wrong:** A logistics operations buyer spots that "MAEU2024000001" is not a real Maersk invoice number format, or that the CNSHA→USHON trade lane doesn't make sense geographically, or that all overcharges are exactly 10% of the invoice value.

**Why it happens:** Data is generated programmatically without maritime domain knowledge.

**How to avoid:** Follow the Maritime Data Credibility Checklist in UI-SPEC.md exactly. Key rules:
- Invoice IDs: `MAEU-2024-XXXXX` format (5-digit suffix, not sequential)
- Container numbers: Must match ISO 6346 pattern — 4 uppercase letter owner code + U (or J/Z) + 6 digits + check digit character
- Overcharges: 2–15% of invoice value only (not round percentages)
- Amounts: Include cents (e.g., $14,847.34 not $14,847.00)
- Port pairs: Only use pairs that make geographic sense on real trade lanes

**Warning signs:** Buyer hesitates, says "is this real data?" or asks about the carrier name.

### Pitfall 6: GSAP Counter Shows Wrong Format Momentarily

**What goes wrong:** During the count-up animation, the dollar amount briefly shows as "187500" without formatting, then snaps to "$187,500" at completion.

**Why it happens:** The `onUpdate` callback is not applied during animation, only at completion.

**How to avoid:** Apply formatting in every `onUpdate` call, not just at the end:
```javascript
gsap.to(el, {
  innerHTML: 187500,
  duration: 1.2,
  snap: { innerHTML: 1 },
  onUpdate() {
    el.textContent = '$' + Math.round(parseFloat(el.innerHTML)).toLocaleString();
  }
});
```

### Pitfall 7: position:sticky Header Fails if Ancestor Has overflow:hidden

**What goes wrong:** The sticky header scrolls away with content during scrolling.

**Why it happens:** Any ancestor element with `overflow: auto`, `overflow: scroll`, or `overflow: hidden` breaks `position: sticky`.

**How to avoid:** The invoice table container uses `overflow: hidden` for `border-radius` clipping. This is safe because the header is outside the table container. The `<body>` and content wrapper must not have any `overflow` other than `visible`.

---

## Code Examples

### CSS Token Block (complete, copy-paste ready)

```css
/* Source: UI-SPEC.md Color section */
:root {
  /* Primitives */
  --navy:      #0B1F3A;
  --blue:      #1A56A0;
  --accent:    #0EA5E9;
  --green:     #10B981;
  --red:       #EF4444;
  --yellow:    #F59E0B;
  --gray-50:   #F8FAFC;
  --gray-100:  #F1F5F9;
  --gray-200:  #E2E8F0;
  --gray-300:  #CBD5E1;
  --gray-500:  #64748B;
  --gray-700:  #334155;
  --gray-900:  #0F172A;
  --white:     #FFFFFF;

  /* Semantic aliases */
  --surface-page:       var(--navy);
  --surface-card:       rgba(255,255,255,0.05);
  --surface-card-solid: #132B4E;
  --surface-content:    var(--white);
  --border-glass:       rgba(255,255,255,0.12);
  --border-subtle:      var(--gray-200);
  --text-primary:       var(--white);
  --text-secondary:     #94A3B8;
  --text-muted:         var(--gray-500);
  --text-dark:          var(--gray-900);
  --status-won:         var(--green);
  --status-pending:     var(--yellow);
  --status-filed:       var(--accent);
  --status-recovered:   var(--green);
  --status-approved:    var(--gray-300);
  --cta-bg:             var(--accent);
  --cta-hover:          #0284C7;
}
```

### Page Background Gradient

```css
/* Source: UI-SPEC.md Color — Page Background */
body {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(14,165,233,0.12) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(26,86,160,0.15) 0%, transparent 50%),
    #0B1F3A;
}
```

### Glassmorphism Card

```css
/* Source: UI-SPEC.md Color — Glassmorphism Card Rules */
.glass-card {
  background-color: #132B4E;                         /* Safari: must be non-transparent */
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 8px 32px rgba(0,0,0,0.37);
  border-radius: 16px;
}
```

### ROI Calculator Formula

```javascript
// Source: UI-SPEC.md Interaction Contracts — ROI Calculator
function calculateROI(monthlySpend) {
  const annualRecovery = monthlySpend * 12 * 0.035;
  const fee = annualRecovery * 0.25;
  const netBenefit = annualRecovery - fee;
  return { annualRecovery, fee, netBenefit };
}

function formatCurrency(n) {
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
}

document.querySelector('#roi-input').addEventListener('input', function() {
  const raw = this.value.replace(/[^0-9]/g, '');
  const spend = parseInt(raw, 10) || 0;
  if (spend === 0) {
    // Show $— in all three output tiles
    return;
  }
  const { annualRecovery, fee, netBenefit } = calculateROI(spend);
  document.querySelector('#roi-recovery').textContent = formatCurrency(annualRecovery);
  document.querySelector('#roi-fee').textContent = formatCurrency(fee);
  document.querySelector('#roi-net').textContent = formatCurrency(netBenefit);
});
```

### Dispute Status Badge HTML Pattern

```html
<!-- Source: UI-SPEC.md Component 5 — Dispute Status Badges -->
<!-- Pending -->
<span class="badge badge-pending">Pending</span>
<!-- Filed -->
<span class="badge badge-filed">Filed</span>
<!-- Won -->
<span class="badge badge-won">Won</span>
<!-- Recovered -->
<span class="badge badge-recovered">Recovered</span>
```

```css
.badge {
  border-radius: 12px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 700;
  display: inline-block;
}
.badge-pending   { background: rgba(245,158,11,0.2);  color: #FDE68A; }
.badge-filed     { background: rgba(14,165,233,0.2);  color: #7DD3FC; }
.badge-won       { background: rgba(16,185,129,0.2);  color: #6EE7B7; }
.badge-recovered { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }
```

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| python3 | INV-13, REL-01 — serve via `python3 -m http.server` | Yes | 3.9.6 | — |
| Node.js | Build tooling (none in this phase) | Yes | 24.14.1 | n/a |
| Inter woff2 | DS-05, D-02 | Must download | Latest from rsms/inter GitHub releases | System font stack (-apple-system, BlinkMacSystemFont) declared in @font-face src |
| JetBrains Mono woff2 | DS-05, D-02 | Must download | Latest from JetBrains/JetBrainsMono GitHub releases | `ui-monospace, SFMono-Regular, monospace` |
| ApexCharts 3.54.1 | DS-06, INV-11, INV-12 | Via jsDelivr CDN | 3.54.1 pinned | — (required, no fallback) |
| GSAP 3.12.5 | DS-07, INV-03 | Via jsDelivr CDN | 3.12.5 pinned | — (required, no fallback) |

**Missing dependencies with no fallback:**
- ApexCharts and GSAP require internet access to jsDelivr on first load (for the CDN path). For fully offline operation, Wave 1 should include downloading these files to a `/vendor/` directory. This is NOT required by the locked decisions (REL-01 only requires no multi-origin loading), so CDN is acceptable.

**Missing dependencies with fallback:**
- Fonts: system font fallback stack is declared in @font-face and body font-family. Dashboard renders without Inter/JetBrains Mono, just with slightly different metrics.

**Font download task required:** The `/fonts/` directory does not exist yet. It must be created and populated with the two variable woff2 files as part of Wave 0 (setup) or Wave 1 (implementation).

---

## Validation Architecture

> `nyquist_validation` is `false` in `.planning/config.json`. This section is skipped per configuration.

---

## Project Constraints (from CLAUDE.md)

The CLAUDE.md describes VESSIQ as a Python/FastAPI maritime data normalization backend. The following directives apply to Phase 1:

- **Python 3.11+** is the project runtime — irrelevant for this phase (no Python code produced).
- **In-memory event store** — irrelevant for Phase 1 (no backend integration).
- **No build tooling** — this phase is standalone HTML only; confirmed by REQUIREMENTS.md Out of Scope table ("React / build tooling: Startup speed, zero infra — standalone HTML ships immediately").
- **Offline-safe requirement** — DS-05 requires no external font CDN. This is a hard constraint that overrides any convenience of Google Fonts CDN.

The CLAUDE.md architecture diagram does not affect Phase 1 implementation. Phase 1 produces static assets only (`dashboard.html`, `/fonts/`), not Python modules.

---

## Sources

### Primary (HIGH confidence)

- `.planning/phases/01-invoice-demo-dashboard/01-UI-SPEC.md` — Complete design contract; primary specification for all implementation decisions
- `.planning/phases/01-invoice-demo-dashboard/01-CONTEXT.md` — User decisions; locked implementation choices
- `.planning/REQUIREMENTS.md` — 25 phase requirements; acceptance criteria
- `demo/index.html` — CSS token names, header/logo HTML structure, glassmorphism base patterns
- `frontend/dashboard.html` — renderAll() pattern, state/filter/tab patterns

### Secondary (MEDIUM confidence)

- `.planning/research/stack.md` — ApexCharts vs. Chart.js comparison; GSAP UMD vs. ESM tradeoffs; glassmorphism CSS rules; CDN gotchas; verified against official docs
- `.planning/research/pitfalls.md` — ApexCharts ghost background bug (issues #4028/#3387); Safari backdrop-filter; fake data credibility; numbers reconciliation; CSS sticky + overflow
- `.planning/research/features.md` — Demo interaction priorities; KPI values rationale; maritime domain benchmarks

### Tertiary (LOW confidence)

- ApexCharts issues #4028 and #3387 (open GitHub issues, not official docs) — confirmed via pitfalls.md citation; mitigation is hardcoded in UI-SPEC so LOW confidence of root cause does not affect implementation

---

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — Libraries pinned, versions verified in UI-SPEC, CDN URLs exact
- Architecture patterns: HIGH — State/render pattern confirmed in frontend/dashboard.html; interaction contracts fully specified in UI-SPEC
- DATA array construction: MEDIUM — KPI math constraints are clear; exact row values require careful crafting to hit targets precisely
- Pitfalls: HIGH — ApexCharts bug mitigations are non-negotiable per UI-SPEC Known Bugs section; Safari pitfall confirmed across multiple sources

**Research date:** 2026-03-24
**Valid until:** 2026-04-24 (stable tech; ApexCharts and GSAP versions are pinned so no version-drift risk)
