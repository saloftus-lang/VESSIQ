# Phase 2: Founder Ops Dashboard - Research

**Researched:** 2026-03-25
**Domain:** Standalone HTML dashboard — glassmorphism dark theme, localStorage persistence, GSAP animations
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Dark navy glassmorphism. Body background `#0B1F3A`. Glass cards use `background: rgba(255,255,255,0.05)`, `backdrop-filter: blur(16px) saturate(180%)`, `-webkit-backdrop-filter: blur(16px) saturate(180%)`, `border: 1px solid rgba(255,255,255,0.10)`, `box-shadow: 0 4px 24px rgba(0,0,0,0.4)`.
- **D-02:** Flat glass — no CSS 3D perspective transforms or hover tilt. Clean and fast.
- **D-03:** Header: same dark navy header structure as `dashboard.html` but the header badge reads "Founder View" in amber/gold (`background: rgba(245,158,11,0.15)`, `border: 1px solid rgba(245,158,11,0.3)`, `color: #F59E0B`) instead of the accent blue used on the demo dashboard.
- **D-04:** Text colors: headings `#FFFFFF`, body text `#E2E8F0`, muted labels `#94A3B8`. No light-mode colors.
- **D-05:** Single-page scroll. No tab navigation. All sections visible by scrolling from top to bottom.
- **D-06:** Page flow (top to bottom): Header → KPI tiles row (3 tiles) → "This Week" heading → Tasks + Notes side-by-side (50%/50%) → "Industry Benchmarks" heading → Benchmark cards row (3 cards).
- **D-07:** Max page width: `1200px`, centered, `padding: 0 48px`. Same horizontal rhythm as `dashboard.html`.
- **D-08:** Active Pilots tile: **1** (Pasha Hawaii).
- **D-09:** Invoices Processed tile: **23**.
- **D-10:** Total Savings Identified tile: **$187,500**.
- **D-11:** All 3 KPI tiles animate with GSAP count-up on `DOMContentLoaded` — same pattern as `dashboard.html`.
- **D-12:** Pre-seed tasks with 3 items on first load (when localStorage is empty): "Follow up with Heather Brown re: Pasha pilot scope", "Prep ROI summary for first audit batch", "Identify 2nd pilot prospect outreach".
- **D-13:** Task interaction: checkbox to mark complete (strikethrough text + muted color), delete button (×) per row, input field + "Add" button to add new tasks.
- **D-14:** Persist task list (array of `{id, text, done}`) to `localStorage` under key `'fnd-tasks'`. Load on page init.
- **D-15:** Single `<textarea>` that auto-saves to `localStorage` under key `'fnd-notes'` on every `input` event. No save button. Placeholder: "Brain dump, follow-ups, ideas…"
- **D-16:** Notes widget height: `min-height: 180px`, auto-expanding (scrollable, not fixed).
- **D-17:** Three benchmark cards — Invoice Error Rate (Industry 38% / VESSIQ <5%), Avg Detention Days (Industry 4.2 days / VESSIQ <1 day), Dispute Win Rate (Industry 32% / VESSIQ 68%).
- **D-18:** Benchmark visualization is Claude's discretion.

### Claude's Discretion

- Benchmark card visualization style (progress bars vs. delta badges vs. both)
- Typography scale and spacing within glass cards
- Responsive behavior at narrow widths (not a priority but avoid broken layouts)
- Section heading style (font size, weight, separator line vs. none)

### Deferred Ideas (OUT OF SCOPE)

- Multi-pilot view (filter by customer) — V2-05
- Email report from founder dashboard — V2-03
- Live API connection to FastAPI backend — V2-01
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FND-01 | Header with VESSIQ logo and "Founder View" label (distinct from demo dashboard) | D-03: amber badge pattern confirmed from dashboard.html header HTML |
| FND-02 | Pilot metrics section — 3 KPI tiles: Active Pilots, Invoices Processed, Total Savings Identified | D-08/09/10/11: static values locked, GSAP counter pattern confirmed |
| FND-03 | Ops tasks widget — to-do list with add/complete/delete (persisted in localStorage) | D-12/13/14: full spec locked, state+render pattern from dashboard.html applies |
| FND-04 | Notes widget — freeform textarea, saved to localStorage on input | D-15/16: pattern is a single textarea with `input` event listener |
| FND-05 | Industry benchmarks section — 3 benchmark cards | D-17: all three values locked, card structure parallels KPI tile HTML |
| FND-06 | Benchmark cards show "Industry avg" vs "VESSIQ target" with visual indicator | D-18 (discretion): progress bar approach recommended — see Architecture Patterns |
| FND-07 | Same design system as dashboard.html (shared CSS token values, same glassmorphism card style) | CSS `:root` block, @font-face, GSAP CDN all copied verbatim — dark override applied |
</phase_requirements>

---

## Summary

Phase 2 builds `founder.html` as a private internal dashboard for Sean. It is a standalone HTML file with zero build tooling, served by the same local HTTP server as `dashboard.html`. All required patterns already exist in Phase 1: the CSS token set, GSAP count-up, `state`/`setState`/`render()` loop, and localStorage primitives are all present and verified in `dashboard.html`.

The primary technical challenge is the visual direction shift from Phase 1's light-background design to a full dark navy glassmorphism surface. Every card in `founder.html` sits on a `#0B1F3A` body background with glass cards using translucent white fill — the exact opposite of Phase 1's white cards on a gray body. This is a CSS-only change; no JavaScript patterns are different.

The tasks widget is the most logic-intensive component. It mirrors a minimal to-do list: an in-memory array of `{id, text, done}` objects, persisted to localStorage on every mutation, rendered to a `<ul>` via a `renderTasks()` function. The pattern from `dashboard.html`'s `state`/`setState`/`render()` cycle applies directly.

**Primary recommendation:** Copy `dashboard.html`'s `:root`, `@font-face`, header HTML, and GSAP counter block verbatim; then layer the dark glassmorphism surface on top. Build tasks as a self-contained mini state machine. Ship.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| GSAP | 3.12.5 (pinned CDN) | KPI count-up entrance animation | Already in use in Phase 1; pinned version avoids CDN churn |
| Vanilla JS | ES2020 (browser native) | State, localStorage, DOM rendering | Zero-dependency; matches Phase 1 architecture decision |
| CSS backdrop-filter | Native (Chrome 76+, Safari 9+) | Glassmorphism blur | Native browser API, no library needed |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| ApexCharts | NOT USED | Charts | Not needed for Phase 2 — no chart requirements in FND-01 through FND-07 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pinned GSAP CDN | Latest GSAP CDN | Pinned is safer for demo reliability (REL-01) |
| Vanilla JS task state | Alpine.js / Vue | Zero-infra constraint in REQUIREMENTS.md rules out any framework |

**Installation:** No package install. CDN links only.

```html
<!-- GSAP — copy verbatim from dashboard.html -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
```

**Version verification:** GSAP 3.12.5 is the version pinned in `dashboard.html` line 791. No upgrade needed — version consistency between the two files is the requirement.

---

## Architecture Patterns

### Recommended File Structure

```
VESSIQ/
├── dashboard.html        # Phase 1 — unchanged
├── founder.html          # Phase 2 — new file
└── fonts/
    ├── inter-variable.woff2       # shared, already on disk
    └── jetbrains-mono-variable.woff2  # shared, already on disk
```

No new directories or build artifacts. `founder.html` is a single self-contained file.

### Pattern 1: Dark Glassmorphism Surface Override

**What:** In `dashboard.html`, `body { background: var(--gray-50); }` and `.card { background: white; }`. In `founder.html`, override both to a dark navy surface with translucent glass cards. The `:root` token block is copied verbatim — only the `body` and `.card` rules change.

**When to use:** Applied globally to `founder.html`. Not applied to `dashboard.html`.

```css
/* Source: Phase 2 CONTEXT.md D-01/D-04 */
body {
  background: #0B1F3A;
  color: #E2E8F0;
}

.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}
```

**Safari requirement:** Both `backdrop-filter` and `-webkit-backdrop-filter` must be present. The `background` must NOT be fully transparent (rgba fill > 0) or Safari ignores blur. The `rgba(255,255,255,0.05)` value satisfies this.

### Pattern 2: KPI Tile Count-Up (verbatim from dashboard.html)

**What:** GSAP entrance animation + numeric counter tween on `DOMContentLoaded`.

**When to use:** All 3 KPI tiles in FND-02.

```javascript
// Source: dashboard.html lines 1040–1060
document.addEventListener('DOMContentLoaded', () => {
  gsap.from('.kpi-tile', { y: 20, opacity: 0, stagger: 0.08, duration: 0.5 });

  const targets = [
    { id: 'kpi-pilots',   val: 1,       prefix: '',  suffix: '' },
    { id: 'kpi-invoices', val: 23,      prefix: '',  suffix: '' },
    { id: 'kpi-savings',  val: 187500,  prefix: '$', suffix: '' },
  ];

  targets.forEach(({ id, val, prefix, suffix }) => {
    const el = document.getElementById(id);
    const obj = { v: 0 };
    gsap.to(obj, { v: val, duration: 1.2, ease: 'power2.out',
      onUpdate: () => { el.textContent = prefix + Math.round(obj.v).toLocaleString('en-US') + suffix; }
    });
  });

  initTasks();
  loadNotes();
});
```

### Pattern 3: Tasks Mini State Machine

**What:** In-memory array `tasks = [{id, text, done}]`, loaded from localStorage on init, saved on every mutation. A `renderTasks()` function rebuilds the `<ul>` from scratch on each call.

**When to use:** FND-03 tasks widget.

```javascript
// Source: CONTEXT.md D-12/13/14 + dashboard.html state pattern
const TASKS_KEY = 'fnd-tasks';
const DEFAULT_TASKS = [
  { id: 1, text: 'Follow up with Heather Brown re: Pasha pilot scope', done: false },
  { id: 2, text: 'Prep ROI summary for first audit batch',             done: false },
  { id: 3, text: 'Identify 2nd pilot prospect outreach',               done: false },
];

let tasks = [];

function initTasks() {
  const saved = localStorage.getItem(TASKS_KEY);
  tasks = saved ? JSON.parse(saved) : DEFAULT_TASKS;
  renderTasks();
}

function saveTasks() {
  localStorage.setItem(TASKS_KEY, JSON.stringify(tasks));
}

function renderTasks() {
  const ul = document.getElementById('task-list');
  ul.innerHTML = tasks.map(t => `
    <li class="task-item${t.done ? ' done' : ''}" data-id="${t.id}">
      <label class="task-check">
        <input type="checkbox" ${t.done ? 'checked' : ''}>
        <span class="task-text">${escapeHtml(t.text)}</span>
      </label>
      <button class="task-delete" data-id="${t.id}">×</button>
    </li>
  `).join('');
}

// Event delegation — one listener per container
document.getElementById('task-list').addEventListener('change', e => {
  if (e.target.type !== 'checkbox') return;
  const id = +e.target.closest('[data-id]').dataset.id;
  tasks = tasks.map(t => t.id === id ? { ...t, done: e.target.checked } : t);
  saveTasks(); renderTasks();
});

document.getElementById('task-list').addEventListener('click', e => {
  const btn = e.target.closest('.task-delete');
  if (!btn) return;
  tasks = tasks.filter(t => t.id !== +btn.dataset.id);
  saveTasks(); renderTasks();
});

document.getElementById('task-add-btn').addEventListener('click', () => {
  const input = document.getElementById('task-input');
  const text = input.value.trim();
  if (!text) return;
  tasks.push({ id: Date.now(), text, done: false });
  input.value = '';
  saveTasks(); renderTasks();
});
```

**Key detail:** Use `escapeHtml()` when rendering task text to `innerHTML`. Prevents XSS from user-typed task content. Simple implementation:

```javascript
function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
```

### Pattern 4: Notes Auto-Save

**What:** Single textarea wired to `input` event that writes to localStorage. No debounce needed at this scale — `input` fires on each keystroke and `localStorage.setItem` is synchronous and fast.

**When to use:** FND-04 notes widget.

```javascript
// Source: CONTEXT.md D-15/16
const NOTES_KEY = 'fnd-notes';

function loadNotes() {
  const saved = localStorage.getItem(NOTES_KEY);
  if (saved) document.getElementById('notes-area').value = saved;
}

document.getElementById('notes-area').addEventListener('input', e => {
  localStorage.setItem(NOTES_KEY, e.target.value);
});
```

### Pattern 5: Benchmark Card with Progress Bar

**What:** Each benchmark card shows two rows: "Industry avg" and "VESSIQ target", plus a progress bar showing where VESSIQ stands relative to industry. For metrics where lower is better (Error Rate, Detention Days), VESSIQ's value appears near the left (near zero) while the industry bar reaches toward the right. For metrics where higher is better (Dispute Win Rate), inverse. A delta badge showing the advantage gap gives an instant "so what."

**When to use:** FND-05 and FND-06 for all 3 benchmark cards.

```
[ Invoice Error Rate               ]
  Industry avg   ████████████ 38%
  VESSIQ target  ██ <5%
  Delta: -33 percentage points
```

**Recommended implementation:** A simple `<div>` progress bar using width % on a fixed-height bar track. No external library needed.

```css
.bench-bar-track {
  height: 6px;
  background: rgba(255,255,255,0.08);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 4px;
}
.bench-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}
.bench-bar-fill.industry { background: rgba(239,68,68,0.7); }  /* red — bad */
.bench-bar-fill.vessiq   { background: #10B981; }               /* green — good */
```

### Anti-Patterns to Avoid

- **Using `file://` protocol:** Both fonts use `url('/fonts/...')` with absolute paths that only resolve over HTTP. Always serve with `python3 -m http.server` or equivalent.
- **Using `backdrop-filter` with fully transparent background:** Safari 17 renders no blur if `background` is `transparent` or `rgba(0,0,0,0)`. Keep `rgba(255,255,255,0.05)` minimum fill.
- **Using `innerHTML` unsanitized with user task input:** Task text is user-typed. Always run through `escapeHtml()` before injecting into innerHTML.
- **Storing `tasks` as a string via JSON.stringify without parse guard:** Wrap `JSON.parse` in try/catch — malformed localStorage data should fall back to `DEFAULT_TASKS`.
- **Sharing localStorage keys with dashboard.html:** `dashboard.html` uses no localStorage. `founder.html` uses `'fnd-tasks'` and `'fnd-notes'`. No collision risk, but keep keys namespaced with `fnd-` prefix for clarity.
- **Adding 3D CSS perspective transforms:** D-02 locks flat glass. Do not add `transform: perspective(...)` or `rotateX/rotateY` hover effects.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Numeric count-up animation | Custom `setInterval` counter | GSAP `gsap.to(obj, { v: val, onUpdate })` | Already in project; handles easing, cleanup, and frame timing correctly |
| localStorage JSON serialization | Custom encode/decode | `JSON.stringify` / `JSON.parse` (native) | Standard, zero overhead |
| HTML entity escaping | Regex chain | Simple `escapeHtml()` helper (4 replacements) | Sufficient for this use case — no need for a DOM sanitizer library |
| CSS blur effect | Canvas-based blur | `backdrop-filter: blur()` (native CSS) | Native is GPU-accelerated; canvas approach is complex and slower |

**Key insight:** This phase has no new external dependencies. Everything needed is already in the project or in the browser.

---

## Common Pitfalls

### Pitfall 1: Safari backdrop-filter Fails Silently

**What goes wrong:** Glass cards show no blur on Safari — they appear as flat translucent rectangles with no depth effect.

**Why it happens:** Safari requires both `-webkit-backdrop-filter` AND a non-transparent `background-color`. If `background` is omitted or set to `transparent`, Safari skips the blur entirely without error.

**How to avoid:** Always pair:
```css
backdrop-filter: blur(16px) saturate(180%);
-webkit-backdrop-filter: blur(16px) saturate(180%);
background: rgba(255,255,255,0.05);  /* must NOT be transparent */
```

**Warning signs:** Glass cards look flat on Safari but correct on Chrome; no console error.

### Pitfall 2: Font URLs Fail on file:// Protocol

**What goes wrong:** Inter and JetBrains Mono fonts fail to load. Browser console shows net::ERR_FILE_NOT_FOUND for `/fonts/inter-variable.woff2`.

**Why it happens:** The `@font-face` src uses `/fonts/...` (absolute path from server root). On `file://`, there is no server root — the path resolves incorrectly.

**How to avoid:** Serve with `python3 -m http.server 8080` from the VESSIQ root directory. Both `dashboard.html` and `founder.html` must be served from the same server.

**Warning signs:** Text renders in system sans-serif instead of Inter. Monospaced numbers use a different font.

### Pitfall 3: localStorage Parse Error Crashes Tasks Widget

**What goes wrong:** Tasks widget shows blank on reload, or JavaScript throws and all JS stops executing.

**Why it happens:** If `localStorage.getItem('fnd-tasks')` returns a malformed string (e.g., from a manual browser edit or partial write), `JSON.parse()` throws a SyntaxError.

**How to avoid:**
```javascript
function loadTasks() {
  try {
    return JSON.parse(localStorage.getItem(TASKS_KEY)) || DEFAULT_TASKS;
  } catch (e) {
    return DEFAULT_TASKS;
  }
}
```

**Warning signs:** Tasks widget is empty after reload even though items were previously added.

### Pitfall 4: Stacking backdrop-filter Elements Causes Performance Drop

**What goes wrong:** Page feels sluggish on lower-powered laptops during scroll.

**Why it happens:** Multiple elements with `backdrop-filter` trigger GPU compositing for each layer. Stacking many blurred panels (6+ in the viewport) can cause frame drops.

**How to avoid:** The page has at most 9 glass cards visible at once (3 KPI + 2 widget + 3 benchmark + header). This is well within browser limits for glassmorphism. No mitigation needed — just do not add additional nested glass cards.

**Warning signs:** DevTools Performance panel shows compositing cost > 8ms per frame during scroll.

### Pitfall 5: Amber Badge Color Conflict with Accent Blue

**What goes wrong:** The "Founder View" badge uses amber (`#F59E0B`) but the `:root` CSS inherits the accent blue from dashboard.html's token set, and other UI elements (links, focus rings) may accidentally appear amber.

**Why it happens:** If `--yellow: #F59E0B` is the amber color in the `:root` token set and `.header-badge` references `var(--yellow)` without scoping, any element that accidentally inherits or re-uses `--yellow` shows amber.

**How to avoid:** Keep the badge styles inline or in a `.founder-badge` class. Do not redefine `--accent` to amber globally. The `--yellow` token is already defined in the `:root` as `#F59E0B` — use it directly for the badge, do not change the token.

---

## Code Examples

Verified patterns from dashboard.html source:

### GSAP Entrance + Counter (from dashboard.html lines 1040–1060)
```javascript
document.addEventListener('DOMContentLoaded', () => {
  gsap.from('.kpi-tile', { y: 20, opacity: 0, stagger: 0.08, duration: 0.5 });

  const targets = [
    { id: 'kpi-pilots',   val: 1,      prefix: '',  suffix: '' },
    { id: 'kpi-invoices', val: 23,     prefix: '',  suffix: '' },
    { id: 'kpi-savings',  val: 187500, prefix: '$', suffix: '' },
  ];
  targets.forEach(({ id, val, prefix, suffix }) => {
    const el = document.getElementById(id);
    const obj = { v: 0 };
    gsap.to(obj, { v: val, duration: 1.2, ease: 'power2.out',
      onUpdate: () => { el.textContent = prefix + Math.round(obj.v).toLocaleString('en-US') + suffix; }
    });
  });
});
```

### Header HTML (from dashboard.html lines 526–534, adapted for Founder View)
```html
<header>
  <div class="logo">
    <div class="logo-mark">V</div>
    <div>
      <div class="logo-text">VESSIQ</div>
      <div class="logo-sub">Freight Audit Platform</div>
    </div>
  </div>
  <div class="header-badge founder-badge">Founder View</div>
</header>
```

```css
/* Amber badge — override for founder.html only */
.founder-badge {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #F59E0B;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}
```

### CSS Root Tokens (from dashboard.html lines 21–37 — copy verbatim)
```css
:root {
  --navy:    #0B1F3A;
  --blue:    #1A56A0;
  --accent:  #0EA5E9;
  --green:   #10B981;
  --red:     #EF4444;
  --yellow:  #F59E0B;
  --gray-50:  #F8FAFC;
  --gray-100: #F1F5F9;
  --gray-200: #E2E8F0;
  --gray-300: #CBD5E1;
  --gray-400: #94A3B8;
  --gray-500: #64748B;
  --gray-700: #334155;
  --gray-900: #0F172A;
  --white:   #FFFFFF;
}
```

### Two-Column Section Layout (50/50 split for Tasks + Notes)
```css
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 40px;
}
@media (max-width: 900px) {
  .two-col { grid-template-columns: 1fr; }
}
```

### Three-Column Row Layout (KPI tiles and Benchmark cards)
```css
.three-col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| CSS `filter: blur()` on element itself | `backdrop-filter: blur()` on overlay | CSS Filters Level 2 (2019+) | Blurs what is BEHIND the element, not the element itself — correct for glass UI |
| `localStorage` with raw strings | `JSON.stringify/parse` with try/catch | Long-established best practice | Structured data, safe parse |
| Manual animation loops | GSAP tweens | GSAP 3.x (2019) | Declarative, GPU-optimized, correct easing |

**Deprecated/outdated:**
- `webkitRequestAnimationFrame`: replaced by `requestAnimationFrame` — not relevant here since GSAP handles this internally.
- CSS `transition: height` for expanding elements: `dashboard.html` STATE.md notes use `max-height` transition instead (0 to 400px) to avoid needing JS height measurement. Not needed in Phase 2 (no expandable rows).

---

## Open Questions

1. **Benchmark bar normalization for "Avg Detention Days"**
   - What we know: Industry avg = 4.2 days, VESSIQ target = <1 day. These are absolute day counts, not percentages.
   - What's unclear: What is the scale max for the progress bar? Using 4.2 days as 100% of the bar, VESSIQ's <1 day (~24%) looks like a small improvement visually.
   - Recommendation: Set bar max to 5 days for visual clarity. Industry bar = 84% width, VESSIQ bar = 20% width. Label each bar with the raw value. Delta badge shows "−3.2 days" advantage.

2. **Task `id` generation for pre-seeded items**
   - What we know: `DEFAULT_TASKS` uses static IDs (1, 2, 3). New tasks use `Date.now()` as ID.
   - What's unclear: If user clears localStorage and re-seeds, static IDs reset to 1/2/3 — no collision with Date.now()-based IDs in practice.
   - Recommendation: Use static small integers for default tasks, `Date.now()` for user-added tasks. No issue.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Inter variable font | FND-07 typography | Yes (on disk) | `/fonts/inter-variable.woff2` | System UI sans-serif (acceptable fallback) |
| JetBrains Mono variable font | FND-07 monospace numbers | Yes (on disk) | `/fonts/jetbrains-mono-variable.woff2` | `'Courier New', monospace` |
| GSAP 3.12.5 | FND-02 count-up animation | Yes (CDN) | 3.12.5 pinned | None — required; CDN reachable (same as dashboard.html) |
| python3 http.server | Local serving (fonts) | Yes | System Python 3 | Any local HTTP server |
| localStorage | FND-03, FND-04 persistence | Yes (all modern browsers) | Browser-native | None — required, universally available |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None — all dependencies confirmed available.

---

## Project Constraints (from CLAUDE.md)

These directives from CLAUDE.md apply to this phase:

- Python 3.11+, FastAPI, Pydantic v2, PyYAML — these govern the backend (not relevant to standalone HTML, but noted)
- No React / build tooling — confirmed, `founder.html` is standalone HTML
- Realistic fake data baked in — KPI values (1 pilot, 23 invoices, $187,500) are consistent with backend data concepts
- No authentication — confirmed, internal tool only
- In-memory store (no DB dependency) — not applicable to HTML frontend

CLAUDE.md is primarily a backend architecture document. None of its constraints conflict with the Phase 2 approach. The standalone HTML approach was explicitly selected in REQUIREMENTS.md (Out of Scope table) for startup speed and zero-infra deployment.

---

## Sources

### Primary (HIGH confidence)
- `dashboard.html` (project source) — CSS `:root` tokens, header HTML, GSAP count-up pattern, KPI tile structure, font declarations — read directly from lines 1–1067
- `02-CONTEXT.md` (project decisions) — All locked implementation decisions D-01 through D-18
- `.planning/REQUIREMENTS.md` (project requirements) — FND-01 through FND-07 complete requirement set
- `.planning/STATE.md` (project history) — Safari backdrop-filter pitfall documented from Phase 1; solid background table approach noted

### Secondary (MEDIUM confidence)
- MDN Web Docs knowledge (August 2025 cutoff) — `backdrop-filter` browser compatibility, localStorage API, CSS grid

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — verified from dashboard.html source and CONTEXT.md locked decisions
- Architecture: HIGH — all patterns extracted directly from existing working code in dashboard.html
- Pitfalls: HIGH for Safari/font/localStorage pitfalls (documented in STATE.md and CONTEXT.md); MEDIUM for performance pitfall (general CSS knowledge)

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (stable domain — vanilla HTML/CSS/JS, no fast-moving libraries)
