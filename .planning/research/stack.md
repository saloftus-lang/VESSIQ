# Technology Stack Research: VESSIQ Invoice Dashboard (Standalone HTML)

**Project:** VESSIQ — B2B SaaS Invoice Dashboard UI Layer
**Researched:** 2026-03-24
**Mode:** Ecosystem
**Overall Confidence:** HIGH (core recommendations), MEDIUM (bundle size specifics)

---

## Context

Greenfield UI layer sitting on top of the existing Python/FastAPI backend. The constraint is
**standalone HTML files only** — no React, no Vue, no npm, no build pipeline. Everything must
load from a `<script src="...">` or `<link>` tag. The dashboard is B2B maritime/logistics,
so the aesthetic needs to feel credible to operators and finance teams, not playful.

---

## 1. Charting Library

### Recommendation: ApexCharts

**Use ApexCharts** (`cdn.jsdelivr.net/npm/apexcharts`) as the primary charting engine.

**Why ApexCharts beats the alternatives for this project:**

| Criterion | Chart.js | ApexCharts | ECharts |
|-----------|----------|------------|---------|
| CDN size (gzipped) | ~60 KB | ~131 KB | ~900 KB (full), ~200 KB (core) |
| Rendering | Canvas | SVG | Canvas or SVG |
| Built-in interactivity | Manual | Built-in (zoom, pan, brush, tooltips) | Built-in |
| Annotation support | Plugin only | Native | Native |
| Default aesthetics | Minimal, needs styling | Polished out-of-box | Good, but denser API |
| Learning curve | Low | Low-Medium | High |
| Dark theme | Manual | `theme: { mode: 'dark' }` one-liner | Requires config object |
| Animation | Basic | Smooth SVG transitions | Canvas transitions |
| Real-time updates | `chart.update()` | `chart.updateSeries()` | `setOption()` |
| Suited for invoices | Adequate | Excellent | Overkill |

**ApexCharts strengths for VESSIQ specifically:**
- SVG rendering means crisp text labels at any scale — important for currency amounts
- Built-in zoom/pan without extra plugins (users will want to zoom into date ranges)
- `darkTheme` config is a single property, not custom CSS overrides
- Tooltip customization is straightforward for showing dollar amounts + event counts together
- `sparkline` mode is purpose-built for KPI cards (savings widgets, dispute rates)
- Annotations API lets you mark significant dates (vessel arrival, invoice dispute filed)

**CDN tag:**
```html
<script src="https://cdn.jsdelivr.net/npm/apexcharts@3.54.1/dist/apexcharts.min.js"></script>
```
Pin to a specific version — `@latest` is a footgun in production HTML files with no lock file.

**When to reach for ECharts instead:** If a future phase requires rendering 100K+ data points
(e.g., per-container event streams across all voyages), ECharts' hybrid Canvas/WebGL renderer
handles that volume cleanly. For invoice aggregates (dozens to hundreds of rows), ApexCharts is
the better DX.

**Do not use D3** for this project. D3 is a primitives library, not a charting library.
Building charts with D3 from scratch requires 3-5x the implementation time for standard bar/line
charts. Correct choice if you need custom maritime map overlays — not correct for invoice KPIs.

---

## 2. CSS Framework

### Recommendation: Vanilla CSS with CSS Custom Properties (no framework)

**Do not use Tailwind Play CDN in production standalone HTML files.**

Tailwind's Play CDN is explicitly labeled "development only" by the Tailwind team. It injects a
runtime JS compiler into the page, adds ~400 KB overhead, and can cause flash-of-unstyled-content
on slower connections. It is not suitable for files delivered to enterprise clients.

**The right approach: CSS custom properties + utility-style vanilla CSS.**

The existing VESSIQ demo files already use this pattern well (CSS variables like `--navy`,
`--accent`, `--gray-900`). Extend that approach rather than replacing it with a framework.

**Why this is superior for this project:**

1. Zero dependencies — the HTML file is fully self-contained
2. Custom properties cascade correctly, meaning dark/light theme toggle is 10 lines of JS
3. No build step risk — what you write is exactly what ships
4. File size: 0 KB CDN overhead
5. The glassmorphism patterns needed are 4-6 CSS rules, not a framework feature

**If you want pre-built component scaffolding,** Flowbite works via CDN and provides 400+
components with dark mode via HTML data attributes. Include it as:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js"></script>
```
But be aware Flowbite depends on Tailwind styles being present — use it as a component reference
to copy patterns from, not as a runtime dependency in standalone files.

**Verdict:** Write CSS directly. Adopt a utility-class naming convention internally
(`flex`, `gap-4`, `text-sm` as class names pointing to your own rules). This gives Tailwind-like
readability without the runtime.

---

## 3. Glassmorphism and CSS Depth Techniques

### Recommendation: CSS backdrop-filter + CSS custom properties depth system

**Browser support as of 2025:** `backdrop-filter` works in Chrome, Edge, Firefox 103+, and
Safari (with `-webkit-` prefix). Global support is ~95%. This is safe to use without a polyfill
if you provide a solid-color fallback.

**The four rules that make glassmorphism work:**

```css
.glass-card {
  background: rgba(255, 255, 255, 0.05);      /* semi-transparent fill */
  backdrop-filter: blur(12px) saturate(180%); /* the frosted glass effect */
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12); /* subtle light border */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37); /* depth shadow */
}
```

**3D depth via CSS transforms (no JavaScript required):**

```css
.card {
  transform-style: preserve-3d;
  perspective: 1000px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px) rotateX(2deg);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}
```

**Performance warning:** Limit glass elements to 5-7 per viewport. `backdrop-filter` is GPU
composited — more than 10 overlapping blur elements causes visible lag on mid-range hardware.
For a dashboard with many cards, apply glass effect to the sidebar and header only, and use
solid semi-transparent backgrounds for individual data cards.

**Dark background requirement:** Glassmorphism only reads as glass if there is a colorful or
gradient background behind it. A plain dark `#0F172A` background makes it look like a gray
rectangle. Use a subtle gradient mesh or a dark radial gradient as the page background:

```css
body {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
    #0B1F3A;
}
```

---

## 4. Animation Libraries

### Recommendation: GSAP (core only) for enter animations; CSS transitions for everything else

**Decision matrix:**

| Library | CDN Size | Use Case | Verdict for VESSIQ |
|---------|----------|----------|--------------------|
| CSS transitions/animations | 0 KB | Hover, state changes, simple fades | Use always |
| AOS (Animate on Scroll) | ~8 KB gzipped | Scroll reveals on landing pages | Too light-entertainment for B2B |
| Motion.js (vanilla) | ~2.3 KB (mini) | Programmatic tweens | Good option |
| GSAP core | ~30 KB gzipped | Professional timelines, stagger, counters | Recommended |
| GSAP + ScrollTrigger | ~50 KB gzipped | Scroll-pinned sequences | Overkill for dashboard |

**Use GSAP for:**
- Counter animations on KPI cards (savings amount counting up on load)
- Staggered card entrance (`.from(cards, { y: 20, opacity: 0, stagger: 0.08 })`)
- Number transitions when data refreshes

**CDN tag (free tier — GSAP core is free for most uses):**
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
```

**GSAP licensing note (MEDIUM confidence):** GSAP's core is free including commercial use.
Certain premium plugins (SplitText, MorphSVG, DrawSVG) require a paid Club GreenSock membership.
For invoice dashboards, only free plugins are needed — ScrollTrigger is also free.

**Motion.js** (formerly Framer Motion, now motion.dev) is a strong alternative if GSAP feels
heavy. The mini vanilla build is 2.3 KB:
```html
<script type="module">
  import { animate } from "https://cdn.jsdelivr.net/npm/motion@latest/+esm";
  animate(".card", { opacity: [0, 1], y: [20, 0] }, { duration: 0.4 });
</script>
```
The `type="module"` import approach works in all modern browsers but requires the file be served
over HTTP (not `file://` — see gotchas below).

**Do not use AOS** for a B2B enterprise dashboard. Its "elements flying in from the side as
you scroll" pattern reads as a marketing landing page, not as a professional data tool.

---

## 5. Typography

### Recommendation: Inter via Google Fonts CDN (variable font, subset to Latin)

**Inter** is the established standard for B2B SaaS interfaces. It was designed specifically
for screen readability at small sizes — exactly the use case for dashboard data tables and
metric labels.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap" rel="stylesheet">
```

The `wght@300..700` range syntax requests the variable font — a single ~17 KB file covering all
weights 300-700, versus ~98 KB if you loaded each weight separately. Always use this syntax.

**CSS:**
```css
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
```

The system font fallback chain (`-apple-system, BlinkMacSystemFont`) means the dashboard
renders immediately with no layout shift if Google Fonts is slow. Add `font-display: swap`
via the URL parameter `&display=swap` (already included above).

**Geist** (Vercel's font) is a credible alternative — slightly rounder than Inter, excellent
for developer tooling aesthetic. Available via Google Fonts or self-hosting. Inter is safer
because it has broader brand recognition in enterprise SaaS contexts.

**Do not mix more than 2 font families.** Use Inter for body, and optionally a monospace
(JetBrains Mono or system `ui-monospace`) for EDI codes, container numbers, and amounts in
tables.

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 6. Gotchas: Standalone HTML Files

These are the failure modes that will cost hours if not anticipated.

### Gotcha 1: file:// protocol blocks fetch() entirely

**Severity: CRITICAL**

When you open an HTML file with `File > Open` in a browser (the `file://` protocol), the browser
blocks all outbound `fetch()` and `XMLHttpRequest` calls — including calls to `localhost`. This
is a hard browser security policy, not a CORS header issue.

**Symptom:** Dashboard loads, but all API calls silently fail or throw `Cross-Origin Request
Blocked: The Same Origin Policy disallows reading the remote resource at http://localhost:8000`.

**Fix:** Always serve the HTML file over HTTP, even in development:
```bash
# Python (already available since the backend uses Python)
python3 -m http.server 3000 --directory /path/to/dashboards/

# Or via uvicorn's static file serving — add a StaticFiles mount in main.py
```

Even a trivial local server resolves this. The demo files in `frontend-dev-workspace/` likely
need the same treatment.

### Gotcha 2: CORS headers must be set on the FastAPI backend

**Severity: HIGH**

Even when served over HTTP, `fetch()` from `http://localhost:3000` calling `http://localhost:8000`
is a cross-origin request. The FastAPI backend must explicitly allow it.

In `main.py`, add:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.vessiq.net"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

When the HTML is served from the same domain as the API (same origin), CORS headers are
irrelevant — but during development they are required.

### Gotcha 3: ES Module imports require a server

**Severity: MEDIUM**

The `import` syntax (`<script type="module">`) does not work over `file://`. If you use Motion.js
or any other CDN ESM package, the HTML must be served over HTTP. GSAP's legacy UMD bundle
(`gsap.min.js`) does work over `file://` because it uses globals, not imports.

**Implication:** Recommend GSAP UMD over Motion.js ESM unless the files are always served.

### Gotcha 4: Tailwind Play CDN is not for production

**Severity: MEDIUM**

The Tailwind Play CDN (`cdn.tailwindcss.com`) compiles CSS at runtime in the browser. This
introduces ~400 KB of JS overhead, flash-of-unstyled-content on load, and unpredictable class
purging behavior. The Tailwind team explicitly labels it "not for production."

### Gotcha 5: ApexCharts requires a DOM container to exist at render time

**Severity: LOW**

ApexCharts throws if you call `new ApexCharts(document.querySelector("#chart"), options)` before
the element exists. Always initialize charts in `DOMContentLoaded` or at the bottom of `<body>`:

```html
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const chart = new ApexCharts(document.querySelector("#revenue-chart"), options);
    chart.render();
  });
</script>
```

### Gotcha 6: backdrop-filter Safari requires -webkit- prefix

**Severity: LOW**

Safari does support `backdrop-filter` but requires the `-webkit-` prefix in all current versions
including Safari 17. Always declare both:
```css
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
```

---

## 7. Complete Recommended CDN Stack

```html
<!-- Typography -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">

<!-- Charts -->
<script src="https://cdn.jsdelivr.net/npm/apexcharts@3.54.1/dist/apexcharts.min.js"></script>

<!-- Animations (optional — only if counter/stagger animations are needed) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>

<!-- No CSS framework — write CSS directly with custom properties -->
```

**Total CDN weight (gzipped approximate):**
- Inter variable font: ~17 KB
- ApexCharts: ~131 KB
- GSAP: ~30 KB
- Total: ~178 KB

This is reasonable for a B2B SaaS dashboard. Linear's app ships ~800 KB+ of JS. Notion is ~2 MB.
Enterprise users on corporate networks have fast connections; prioritize feature richness
over micro-optimizations at this stage.

---

## 8. Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Charts | ApexCharts | Chart.js | Less interactivity out-of-box; no built-in zoom/brush; requires more custom CSS for dark theme |
| Charts | ApexCharts | ECharts | ~900 KB full bundle; steeper API; better for 100K+ data points (not this use case) |
| Charts | ApexCharts | D3 | Primitives library, not charts; 3-5x implementation time for standard charts |
| CSS | Vanilla CSS | Tailwind Play CDN | Not production-safe; runtime compiler adds 400 KB; FOUC risk |
| CSS | Vanilla CSS | Bootstrap CDN | Opinionated component styles that fight dark/glass aesthetic |
| Animation | GSAP | AOS | Landing-page feel; not appropriate for data dashboard; limited to scroll reveals |
| Animation | GSAP | Motion.js (ESM) | Requires ES module / HTTP server; UMD option is fine but GSAP has better docs |
| Fonts | Inter | Geist | Both are excellent; Inter has slightly broader SaaS brand recognition |
| Fonts | Inter | System font stack only | System fonts are inconsistent across Windows/Mac; Inter at 17 KB is worth the consistency |

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| ApexCharts recommendation | HIGH | Verified via official docs, multiple comparison sources, existing VESSIQ demo already uses pattern-compatible CSS |
| Vanilla CSS over Tailwind CDN | HIGH | Tailwind's own docs explicitly label Play CDN as dev-only |
| GSAP licensing (free tier) | MEDIUM | Official GSAP site confirms core is free; premium plugins require membership — verify before adding any plugin |
| bundle sizes | MEDIUM | Figures sourced from Bundlephobia/npm-compare, may vary by exact version |
| backdrop-filter browser support | HIGH | MDN and caniuse.com confirm ~95% global support as of 2025 |
| file:// CORS behavior | HIGH | MDN explicitly documents file:// same-origin restrictions |
| Motion.js ESM CDN | MEDIUM | Confirmed via jsDelivr and motion.dev docs; ESM/file:// constraint is real but single-sourced in search results |

---

## Sources

- [ApexCharts JavaScript Charts Comparison](https://apexcharts.com/javascript-charts-comparison/)
- [LogRocket: Comparing most popular JavaScript charting libraries](https://blog.logrocket.com/comparing-most-popular-javascript-charting-libraries/)
- [SciChart: Best JavaScript Chart Libraries 2025](https://www.scichart.com/blog/best-javascript-chart-libraries/)
- [Tailwind CSS Play CDN documentation](https://tailwindcss.com/docs/installation/play-cdn)
- [Flowbite quickstart (CDN)](https://flowbite.com/docs/getting-started/quickstart/)
- [GSAP official site](https://gsap.com/)
- [Motion.dev quick start (vanilla JS)](https://motion.dev/docs/quick-start)
- [MDN: CORS request not HTTP (file:// restriction)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSRequestNotHttp)
- [Inter font — rsms.me](https://rsms.me/inter/)
- [Google Fonts CSS2 API docs](https://developers.google.com/fonts/docs/css2)
- [Glassmorphism implementation guide 2025](https://playground.halfaccessible.com/blog/glassmorphism-design-trend-implementation-guide)
- [DEV Community: Best AOS libraries 2025](https://dev.to/idevgames/best-aos-animation-on-scroll-libraries-in-2025-c9o)
- [Harrison Broadbent: 7 SaaS fonts worth trying](https://harrisonbroadbent.com/blog/saas-fonts/)
