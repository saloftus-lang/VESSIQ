# Architecture Patterns: Standalone HTML Dashboards

**Domain:** Standalone single-file HTML dashboards (no build step, no framework)
**Project:** VESSIQ — dashboard.html (invoice chargeback demo) + founder.html (founder ops)
**Researched:** 2026-03-24
**Overall confidence:** HIGH — existing codebase analyzed directly; patterns confirmed via multiple sources

---

## Executive Summary

VESSIQ's existing `frontend/dashboard.html` already demonstrates a solid baseline: CSS custom properties for tokens, flat class naming, and vanilla JS render functions keyed off a few module-scope state variables. The two new files (`dashboard.html` for invoice chargebacks, `founder.html` for ops) should follow and refine this pattern rather than invent a new one.

The core recommendation: use a **thin centralized state object + explicit re-render functions** for JS (no Proxy, no event bus needed at this scale), a **two-tier CSS custom property system** (primitive tokens + semantic aliases) shared via a `<style>` block at the top of each file, and **hardcoded data in a named const at the top of the script block** organized by domain object (not by UI section).

Both files will share the same design token vocabulary. Since there is no build step, tokens are duplicated at the top of each file's `<style>` block — this is the correct tradeoff for standalone HTML. Keeping them identical is a discipline problem, not a technology problem.

---

## CSS Architecture

### Recommendation: Two-Tier Custom Properties + Semantic Flat Classes

**Do not use BEM or utility classes.** Both create maintenance burden in a standalone file. BEM's double-underscore naming is verbose and its value (preventing naming collisions across files) is irrelevant here — each file is a closed namespace. Utility classes (Tailwind-style) require either a CDN build or a PostCSS step, both of which are anti-patterns for this constraint.

Instead: flat semantic class names (`card`, `panel`, `badge-error`) driven by CSS custom properties.

**Tier 1 — Primitive tokens:** Raw values. Never used directly in components.

```css
:root {
  /* Color primitives */
  --cyan-400: #22d3ee;
  --cyan-500: #0ea5e9;
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --green-500: #22c55e;
  --yellow-500: #eab308;
  --red-500: #ef4444;
  --orange-500: #f97316;

  /* Background primitives */
  --navy-950: #020c17;
  --navy-900: #051422;
  --navy-800: #071929;
  --navy-700: #0b2035;

  /* Alpha primitives */
  --white-03: rgba(255,255,255,.03);
  --white-07: rgba(255,255,255,.07);
  --white-12: rgba(255,255,255,.12);
  --white-18: rgba(255,255,255,.18);
}
```

**Tier 2 — Semantic aliases:** These are what CSS rules actually reference. They map meaning to primitive values.

```css
:root {
  /* Backgrounds */
  --bg:       var(--navy-950);
  --bg-card:  var(--navy-900);
  --bg-input: var(--navy-800);

  /* Borders */
  --border-subtle:  var(--white-03);
  --border-default: var(--white-07);
  --border-strong:  var(--white-12);

  /* Text */
  --text-primary:   #e8f4ff;
  --text-secondary: #6b8eaa;
  --text-muted:     #2d4a66;

  /* Accent */
  --accent: var(--cyan-400);
  --accent-2: var(--blue-500);

  /* Status */
  --status-success: var(--green-500);
  --status-warning: var(--yellow-500);
  --status-error:   var(--red-500);
  --status-info:    var(--blue-500);

  /* Spacing and radius */
  --radius-sm: 7px;
  --radius-md: 12px;
  --radius-lg: 20px;
}
```

**Why two tiers:** Semantic aliases let you change the entire visual vocabulary in one place. If the accent shifts from cyan to violet, you change `--accent` once, not 40 places. Primitive tokens mean the semantic alias layer always has a named constant to point to rather than a raw hex.

**Sharing tokens across two files:** Copy the `:root` block verbatim to both files. Put it at the very top of the `<style>` block and label it with a comment: `/* === SHARED DESIGN TOKENS — keep in sync with founder.html === */`. This is a manual discipline constraint, not a technology one. At two files it is fine.

**CSS structure order within `<style>`:**

```
1. Tokens (:root)
2. Reset (*, body)
3. Layout (grid containers, sidebar, main)
4. Navigation / header
5. Shared components (card, panel, badge, table, button)
6. Page-specific components (chargeback-row, founder-kpi, etc.)
7. Animations (@keyframes)
8. Responsive (@media)
```

---

## JavaScript Organization

### Recommendation: Centralized State Object + Named Render Functions

The existing dashboard uses module-scope `let` variables (`currentNode`, `currentMode`, `currentFeedFilter`) as state. This works but has one weakness: state mutation is implicit and there is no clear boundary between "state changed" and "re-render triggered."

For the new files, formalize this slightly with a single `state` object and an explicit `render()` dispatcher. No Proxy, no PubSub — that's overkill for two demo files.

**Pattern:**

```javascript
// ─── State ─────────────────────────────────────────── //

const state = {
  activeTab: 'overview',      // 'overview' | 'chargebacks' | 'disputes'
  selectedCarrier: 'all',
  expandedRowId: null,
  dateRange: '30d',
};

// ─── State Mutation ─────────────────────────────────── //

function setState(patch) {
  Object.assign(state, patch);
  render();
}

// ─── Render Dispatcher ─────────────────────────────── //

function render() {
  renderKPIs();
  renderTable();
  renderFilters();
  // Only re-render sections that depend on changed state.
  // For demo scale, re-rendering all is fine and simpler.
}
```

**Why not Proxy-based reactivity:** Proxy patterns add ~30 lines of infrastructure code. At this scale you have 3-6 state fields and 4-8 render functions. The overhead is not justified and makes the file harder to read at a glance, which matters when the founder opens it.

**Why not event bus / PubSub:** Same reason. PubSub is for decoupled modules that can't reference each other directly. In a single file, everything can reference `state` and `render()` directly. The indirection adds cognitive load without benefit.

**Component-like vanilla JS — the render function pattern:**

Each UI section gets one render function. The function reads from `state` and `DATA`, produces HTML, and sets `innerHTML` on a container. Template literals are the right tool.

```javascript
function renderChargebackTable() {
  const rows = DATA.chargebacks
    .filter(r => state.selectedCarrier === 'all' || r.carrier === state.selectedCarrier)
    .filter(r => state.dateRange === 'all' || isWithinRange(r.date, state.dateRange));

  document.getElementById('chargebackTableBody').innerHTML = rows.map(row => `
    <tr class="table-row ${state.expandedRowId === row.id ? 'is-expanded' : ''}"
        data-id="${row.id}">
      <td>${row.date}</td>
      <td>${row.carrier}</td>
      <td class="text-mono">${row.invoiceRef}</td>
      <td><span class="badge badge-${row.status}">${row.status}</span></td>
      <td class="text-right text-mono">${formatUSD(row.amount)}</td>
    </tr>
    ${state.expandedRowId === row.id ? renderExpandedRow(row) : ''}
  `).join('');
}
```

**Event delegation instead of per-row listeners:** Attach one listener to the table, not one per row. Row re-renders from `setState` will not re-attach orphaned listeners.

```javascript
document.getElementById('chargebackTable').addEventListener('click', e => {
  const row = e.target.closest('[data-id]');
  if (!row) return;
  const id = row.dataset.id;
  setState({ expandedRowId: state.expandedRowId === id ? null : id });
});
```

**Filter controls pattern:**

```javascript
document.getElementById('carrierFilter').addEventListener('change', e => {
  setState({ selectedCarrier: e.target.value });
});
```

---

## State Management for Interactive Demos

### What needs state

| Interaction | State field | Type |
|---|---|---|
| Active tab | `activeTab` | string enum |
| Filter selection | `selectedCarrier`, `dateRange` | string |
| Expanded table row | `expandedRowId` | string or null |
| Modal open | `modalOpen`, `modalData` | boolean + object |
| Sorted column | `sortCol`, `sortDir` | string, 'asc' \| 'desc' |

### What does NOT need state

- Hover effects (CSS `:hover`)
- Tooltip visibility on hover (CSS `:hover` + `visibility`)
- Badge colors (derived from data value via class map)
- Animated bar widths (set via inline `style` on first render, CSS `transition` does the rest)

### Animated progress bars / number counters

Use CSS `transition` + delayed `style.width` assignment instead of a JS animation loop. The browser handles the interpolation.

```javascript
// After setting innerHTML, defer style assignment one frame
// so the transition fires (not instant).
function animateBars() {
  requestAnimationFrame(() => {
    document.querySelectorAll('[data-fill]').forEach(el => {
      el.style.width = el.dataset.fill;
    });
  });
}
```

In CSS:
```css
.bar-fill {
  width: 0;
  transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## Fake Data Structure

### Recommendation: Single `DATA` const at top of script, organized by domain object

**Do not** organize data by UI section (e.g., `const kpiData`, `const tableData`). UI sections change; domain objects don't. Organize by what the data represents.

```javascript
// ─── Fake Data ────────────────────────────────────── //
// All mock data lives here. Swap for real API calls later.

const DATA = {

  chargebacks: [
    {
      id: 'cb-001',
      date: '2026-03-15',
      carrier: 'Maersk',
      invoiceRef: 'INV-2026-03-0041',
      amount: 12480.00,
      status: 'disputed',      // 'open' | 'disputed' | 'resolved' | 'credited'
      reason: 'Incorrect detention charge — container returned within free time',
      daysOutstanding: 9,
      contactEmail: 'billing@maersk.com',
    },
    // ... more rows
  ],

  carriers: ['Maersk', 'Hapag-Lloyd', 'COSCO', 'ONE', 'Evergreen'],

  summary: {
    totalChargebacks: 48,
    totalValue: 284920,
    resolved: 31,
    avgDaysToResolve: 14,
  },

};
```

**Why a single `DATA` object:**
- One place to find all fake data when the developer wants to update it
- Makes swapping for real API data obvious — replace `DATA.chargebacks` with the API response
- Prevents confusion about which `const` is "the data" vs a derived/filtered list

**Flat arrays of uniform objects:** Each array item should have a consistent shape. Do not put some records with 8 fields and others with 12. If a field doesn't apply, include it as `null` rather than omitting it.

**Dates as ISO strings:** Use `'2026-03-15'` not `'March 15'`. Sorting and filtering are trivial against ISO strings. Display formatting is a separate concern handled in the render function.

**Money as raw numbers:** Store `12480.00`, format to `"$12,480"` in a `formatUSD()` helper in the render layer. Do not store formatted strings in data.

```javascript
const formatUSD = n => '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0 });
const formatPct = n => n.toFixed(1) + '%';
```

---

## Performance

### Lazy loading for charts (Chart.js CDN)

Load Chart.js only when the user navigates to a tab that contains a chart. For standalone HTML, use dynamic `<script>` injection:

```javascript
let chartLoaded = false;

function loadChartJS(callback) {
  if (chartLoaded) { callback(); return; }
  const s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js';
  s.onload = () => { chartLoaded = true; callback(); };
  document.head.appendChild(s);
}

// Called when user clicks the "Spend Trends" tab:
function showSpendTab() {
  setState({ activeTab: 'spend' });
  loadChartJS(() => renderSpendChart());
}
```

This avoids a 50kb+ payload on page load for users who only look at the table.

### IntersectionObserver for scroll-triggered entry animations

Use `IntersectionObserver` to fire entry animations on cards and panels as they scroll into view. Do not use a scroll event listener.

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // fire once
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.card, .panel').forEach(el => observer.observe(el));
```

```css
.card, .panel {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.card.is-visible, .panel.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

### GPU-safe animation properties

Only animate `opacity` and `transform`. Never animate `height`, `width`, `padding`, `box-shadow`, or `background-color` on frequently-updating elements — these trigger layout recalculation.

For expandable rows, use `max-height` transition (not `height`) with a known maximum:

```css
.row-detail {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.row-detail.is-open {
  max-height: 200px; /* generous upper bound */
}
```

### Table performance at demo scale

At 20-100 rows (typical for demo data), `innerHTML` replacement on each state change is fine. Do not introduce virtual DOM concepts. The browser is fast enough.

If rows exceed ~500, consider rendering only the first N rows with a "show more" button rather than pagination (simpler state, better for demos).

### `will-change` — use sparingly

Apply `will-change: transform` only to elements with continuous animation (hover lift effects on cards). Do not apply globally. Overuse creates excess GPU memory consumption.

```css
.card {
  transition: transform 0.15s ease, border-color 0.15s ease;
}
.card:hover {
  transform: translateY(-2px);
}
/* No will-change needed — transition is short and triggered by hover only */
```

---

## Component Patterns to Follow

### Panel with header + content

```html
<div class="panel">
  <div class="panel-header">
    <div class="panel-icon icon-red"><!-- svg --></div>
    <span class="panel-title">Invoice Chargebacks</span>
    <div class="panel-actions"><!-- optional filter/export --></div>
  </div>
  <div class="panel-body" id="chargebackPanel">
    <!-- rendered by renderChargebackTable() -->
  </div>
</div>
```

### Filter pill group

```html
<div class="filter-group" role="group" aria-label="Filter by carrier">
  <button class="filter-pill active" data-value="all">All</button>
  <button class="filter-pill" data-value="Maersk">Maersk</button>
  <button class="filter-pill" data-value="Hapag-Lloyd">Hapag-Lloyd</button>
</div>
```

```javascript
document.querySelector('.filter-group').addEventListener('click', e => {
  const pill = e.target.closest('.filter-pill');
  if (!pill) return;
  document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
  pill.classList.add('active');
  setState({ selectedCarrier: pill.dataset.value });
});
```

### KPI card with trend delta

```javascript
function kpiCard({ label, value, delta, unit }) {
  const dir = delta >= 0 ? 'up' : 'down';
  const sign = delta > 0 ? '+' : '';
  return `
    <div class="card">
      <div class="card-label">${label}</div>
      <div class="card-value">${value}</div>
      <div class="card-delta ${dir}">${sign}${delta}${unit} vs last month</div>
    </div>
  `;
}
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Organizing data by UI section
**What:** `const kpiData = {...}`, `const tableRows = [...]`, `const chartLabels = [...]`
**Why bad:** When data changes (new fields, restructured objects), you update 4-6 separate consts. When you want to cross-reference (e.g., KPI totals derived from table rows), you duplicate logic.
**Instead:** One `DATA` object, derive everything from it.

### Anti-Pattern 2: Inline event listeners in `innerHTML`
**What:** `<button onclick="doThing('${id}')">...</button>`
**Why bad:** Every `innerHTML` replacement destroys and re-creates the DOM including listeners. String-interpolated JS in HTML is also an XSS vector (even for demos, sets bad habits).
**Instead:** Event delegation on stable container elements.

### Anti-Pattern 3: Animating layout-triggering properties
**What:** `transition: height 0.3s`, `transition: padding 0.3s`
**Why bad:** Triggers browser layout recalculation on every frame. Causes jank on slower machines.
**Instead:** Animate `max-height`, `opacity`, `transform` only.

### Anti-Pattern 4: Multiple `document.querySelectorAll` in every render function
**What:** Re-querying the DOM constantly inside render functions.
**Why bad:** Unnecessary DOM traversal. At demo scale it's fine, but it sets a habit of layout thrashing.
**Instead:** Cache container references at init time.

```javascript
const els = {
  kpiGrid:     document.getElementById('kpiGrid'),
  tableBody:   document.getElementById('tableBody'),
  filterGroup: document.getElementById('filterGroup'),
};
```

### Anti-Pattern 5: Storing formatted strings in data
**What:** `amount: '$12,480.00'`, `date: 'March 15, 2026'`
**Why bad:** Can't sort, filter, or compare. Can't reformat for a different locale.
**Instead:** Store raw values, format in render helpers.

### Anti-Pattern 6: Overloading `renderAll()`
**What:** One render function that does everything, called on every state change.
**Why bad:** Fine at 3 components, creates noticeable flicker at 10+ components.
**Instead:** Each render function checks if it needs to run. Or: use targeted `setState` that only re-renders affected sections. The centralized `render()` dispatcher pattern handles this — add section flags if needed.

---

## Scalability Considerations

| Concern | At this scale (demo) | If it becomes production |
|---|---|---|
| State management | Module-scope state object + setState() | Proxy-based store or Redux-lite |
| Data | Hardcoded DATA const | Fetch from /api/chargebacks, same shape |
| Styling | Duplicated :root tokens in two files | Extract to shared tokens.css |
| Charts | Dynamic CDN load | Bundle with esbuild |
| Tables | innerHTML replacement | Virtual scroll (tanstack-virtual) |
| Cross-file reuse | Copy-paste components | Web Components or shared partials |

---

## Sources

- [State Management in Vanilla JS — CSS-Tricks](https://css-tricks.com/build-a-state-management-system-with-vanilla-javascript/) — HIGH confidence, canonical reference
- [CSS Cascade Layers vs BEM vs Utility Classes — Smashing Magazine](https://www.smashingmagazine.com/2025/06/css-cascade-layers-bem-utility-classes-specificity-control/) — HIGH confidence, 2025
- [CSS GPU Animation: Doing It Right — Smashing Magazine](https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/) — HIGH confidence, foundational
- [MDN: CSS and JavaScript animation performance](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance) — HIGH confidence, authoritative
- [Modern State Management in Vanilla JS: 2026 Patterns — Medium/Orami](https://medium.com/@orami98/modern-state-management-in-vanilla-javascript-2026-patterns-and-beyond-ce00425f7ac5) — MEDIUM confidence, community
- [Building scalable CSS architecture with BEM and utility classes — CSS-Tricks](https://css-tricks.com/building-a-scalable-css-architecture-with-bem-and-utility-classes/) — HIGH confidence
- [Chart.js vs D3.js comparison — Luzmo](https://www.luzmo.com/blog/javascript-chart-libraries) — MEDIUM confidence, 2025/2026 survey
- Direct code analysis: `/Users/seanloftus/Desktop/VESSIQ/frontend/dashboard.html` — HIGH confidence (primary source)
