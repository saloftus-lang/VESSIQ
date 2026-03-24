# Domain Pitfalls: B2B SaaS Demo Dashboard (Maritime Invoice Audit)

**Domain:** Enterprise B2B sales demo — standalone HTML, maritime/freight context
**Researched:** 2026-03-24
**Confidence:** MEDIUM-HIGH (mix of verified and WebSearch-sourced findings)

---

## Critical Pitfalls

Mistakes that break a deal, cause a live demo to fail, or permanently damage credibility.

---

### Pitfall 1: External CDN Dependencies That Fail Offline

**What goes wrong:** The demo loads fine in the office but the prospect's conference room has firewall rules, a captive portal, or spotty guest WiFi. Google Fonts, Chart.js CDN, any `cdn.jsdelivr.net` or `cdnjs.cloudflare.com` link fails silently or loudly. Charts don't render. Typography falls back to system sans-serif with completely different spacing, breaking carefully tuned layouts.

**Why it happens:** Developers build with CDN links because it's fast during development, then never test in an offline or firewalled environment.

**Consequences:** Blank chart areas. Text metrics wrapping at wrong widths because the font changed. "FOUT" — Flash of Unstyled Text — during reconnect. In worst case, JavaScript bundle fails to load and the entire demo is broken.

**Prevention:**
- Inline all fonts as base64 in a `<style>` block, or use `@font-face` with a local `woff2` file embedded as a data URI
- Bundle Chart.js (or whichever chart library) as a local `<script>` tag with the minified source inlined or loaded from the same HTML file's directory
- Test the file by opening it with WiFi off. This is the actual demo environment simulation
- If using Google Fonts, use the `&display=swap` parameter AND provide a fallback font stack that doesn't break layout (not just `sans-serif`)

**Detection warning signs:** Blank white rectangles where charts should be. System font (Times New Roman or Helvetica) appears in areas that should show Inter or similar. Loading spinner that never resolves.

---

### Pitfall 2: Fake Data That Signals "This Isn't Real"

**What goes wrong:** Enterprise logistics/finance buyers have spent careers reading freight invoices. They spot fake data immediately: round-dollar amounts, sequential invoice numbers, wrong carrier SCAC codes, impossible port combinations, placeholder company names.

**Why it happens:** Developers generate demo data without domain knowledge. "ACME Corp," "INV-00001," "$1,000.00" are programmer defaults.

**Consequences:** The prospect mentally disengages. A common buyer reaction is "if they couldn't be bothered to put real data in the demo, what does their actual product look like?" This is a credibility signal, not just an aesthetic one.

**Prevention — maritime-specific rules:**

- **Carrier names and SCAC codes must match:** MAEU = Maersk, CMDU = CMA CGM, MSCU = MSC, OOLU = COSCO, HLCU = Hapag-Lloyd. Never invent a fake SCAC code.
- **IMO numbers are 7 digits:** Format is IMO + 7 digits (e.g., IMO 9321483). The check digit must validate — use real vessel names from AIS data (MarineTraffic public listings) and their actual IMO numbers.
- **Port LOCODEs must be real:** USLAX (Los Angeles), USOAK (Oakland), CNSHA (Shanghai), SGSIN (Singapore), NLRTM (Rotterdam). Do not invent USXXX codes.
- **Invoice numbers should look like carrier invoice numbers:** Maersk invoices are alphanumeric (e.g., MCI2400917432), not sequential integers.
- **Amounts should be non-round and include cents:** $14,237.50 looks real. $14,000.00 looks fake.
- **Surcharge line items must be realistic:** BAF (Bunker Adjustment Factor), CAF (Currency Adjustment Factor), PSS (Peak Season Surcharge), EBS (Emergency Bunker Surcharge), D&D (Demurrage and Detention) — using real surcharge names and realistic amounts ($450–$2,800 per container) is essential.
- **Dates should not all cluster on round numbers:** Invoices dated 2024-01-01 or 2024-03-15 look like placeholders. Use specific realistic dates like 2024-03-07, 2024-03-14, 2024-04-02.
- **TEU counts and container numbers:** Container numbers follow ISO 6346 format (4 letters + 7 digits, e.g., MSCU2847315). TEU counts on ocean freight are typically 20, 40, or 45 ft — never odd numbers like 37 TEUs.
- **Voyage numbers follow carrier patterns:** Maersk format is like 418W, CMA CGM uses alphanumeric sequences. Don't make up random strings.
- **Dollar amounts should reflect real market rates:** Ocean freight from CNSHA to USLAX in 2024 was roughly $3,000–$5,500 per FEU (40-foot container). $150 and $50,000 are both wrong.

**Detection warning signs:** Buyer asks "what carrier is that?" or "is this real data from a client?" and the answer involves visible hesitation.

---

### Pitfall 3: Glassmorphism / backdrop-filter Breaking in Safari or Failing Under Dark Backgrounds

**What goes wrong:** `backdrop-filter: blur()` is the dominant glassmorphism technique. In dark mode dashboards (dark navy, deep slate backgrounds), the blur picks up the dark background color and the panel becomes invisible — dark blur on dark background = unreadable. Additionally, Safari requires both `-webkit-backdrop-filter` and `backdrop-filter`, AND requires the element to have a semi-transparent background-color (not just `transparent`). Elements with only `background: transparent` will not activate blur in Safari.

**Why it happens:** Developers test in Chrome and miss Safari's stricter requirements. Dark backgrounds expose contrast gaps that light backgrounds hide.

**Consequences:** Glass panels are invisible or near-invisible on MacBook Safari. Box shadows combined with backdrop-filter in Safari cause the shadow to be blurred into the backdrop region, creating visual smearing.

**Prevention:**
- Always include both prefixes: `backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);`
- The element must have `background-color: rgba(255, 255, 255, 0.08)` or similar — not `transparent`
- On dark dashboards, the glass background should be slightly lighter than the surrounding dark (e.g., `rgba(255,255,255,0.06)` on a `#0B1F3A` navy background)
- Provide a `@supports` fallback: `@supports not (backdrop-filter: blur(1px)) { .glass { background: rgba(15, 23, 42, 0.92); } }`
- Do not apply `box-shadow` and `backdrop-filter` to the same element in Safari — split into wrapper + inner element
- Test specifically on Safari 17+ on macOS and Safari on iOS 17

**Detection warning signs:** Panel appears as a nearly invisible dark rectangle. Shadow bleeds into blurred area. Firefox shows solid fallback color instead of glass.

---

### Pitfall 4: CSS 3D / Perspective Causing Flicker and Layer Explosion

**What goes wrong:** `transform: perspective()`, `rotateX/Y`, `translateZ` trigger GPU compositing layers. Each composited layer uploads a texture to the GPU. A dark dashboard with many 3D-transformed cards (animated KPI cards, perspective chart containers) can exhaust GPU texture memory, causing flicker on entry/exit, stutter during hover, or a full paint invalidation on every frame.

**Why it happens:** 3D transforms feel subtle (a slight tilt on a card) but each one forces a new compositing layer. 20 cards with `transform: rotateY(0.5deg)` = 20 GPU textures, each potentially 200x150px at 2x retina = significant VRAM.

**Consequences:** Visible flicker as animation starts (texture upload lag). Janky hover transitions on low-powered sales laptops. On MacBook Air M1s with Intel integrated graphics (older machines in finance departments), can cause partial render failures.

**Prevention:**
- Reserve 3D transforms for intentional hero moments (one key entrance animation), not every card
- Use `will-change: transform` sparingly and only on elements that will animate — not as a global performance hack
- Prefer `transform: translateX/Y/scale` (2D, compositor-friendly) over `translateZ` or `rotateX/Y` for hover effects
- If using entrance animations, use `opacity` + `translateY` (2D) rather than 3D perspective flips
- Limit compositing layers: check Chrome DevTools Layers panel — aim for under 15-20 active layers
- Test on a mid-range laptop (not an M3 Pro), because buyers often run sales calls on ThinkPads or older MacBooks

**Detection warning signs:** White flash on page load. Card hover causes other cards to briefly flicker. Scroll performance degrades after 5+ seconds on page.

---

### Pitfall 5: Chart Tooltips Clipped at Canvas Boundary

**What goes wrong:** Chart.js (and most canvas-based chart libraries) render tooltips inside the canvas element. When the chart is near the top or right edge of its container, the tooltip renders outside the visible canvas area and is clipped. On dark dashboards, dark tooltip boxes against dark backgrounds also disappear.

**Why it happens:** Canvas-based rendering cannot overflow its bounding box by default. This is a known Chart.js limitation.

**Consequences:** During a live demo when the presenter hovers over a data point, the tooltip either doesn't appear or is half-visible. For a precision tool like an invoice auditing dashboard, invisible data tooltips undermine the "we catch every detail" message.

**Prevention:**
- Use `overflow: visible` on the chart's wrapper `div` — but Chart.js tooltips are drawn on canvas so this alone doesn't help
- For Chart.js: use the external tooltip plugin (custom HTML tooltip outside the canvas) via the `plugins.tooltip.external` option
- For ApexCharts: tooltips render as DOM elements (not canvas), so they overflow naturally — prefer ApexCharts for dark dashboards
- Set explicit `padding` inside chart containers so data points near edges have tooltip room
- Set Chart.js tooltip `position: 'nearest'` and test all four quadrant edge cases manually
- Always set explicit tooltip background, title color, and body color — dark themes will inherit transparent backgrounds that vanish on dark cards

**Detection warning signs:** Hovering the first or last bar in a bar chart shows nothing. Right-side data points appear to have no tooltip.

---

### Pitfall 6: ApexCharts Dark Mode Leaving Ghost Background Colors

**What goes wrong:** ApexCharts has a documented bug where toggling `theme.mode` from `dark` to `light` leaves the chart background color stuck at dark. If the demo's dark mode is toggled or the browser's system preference is dark and the chart initializes once, then the HTML file is opened again, the chart renders with a dark background inside a light card — or vice versa.

**Why it happens:** ApexCharts stores theme state internally and the `updateOptions()` re-render does not fully reset background when switching directions. Issue #4028 and #3387 are both open on the ApexCharts GitHub.

**Consequences:** Dark square inside a white card. Or white square inside a dark card. Extremely obvious during a demo.

**Prevention:**
- For a static demo, pick one theme and hardcode it — do not build a theme toggle
- If the demo is dark-mode-only, initialize all ApexCharts with `theme: { mode: 'dark' }` and `background: 'transparent'` from the start
- Set the chart container div background explicitly in CSS so any ghost background is hidden: `background: transparent !important`
- Test by opening the file on a system with `prefers-color-scheme: dark` enabled, then again with it disabled

**Detection warning signs:** Chart appears with wrong background color. White box in dark UI or vice versa after browser restarts.

---

## Moderate Pitfalls

---

### Pitfall 7: Numbers That Don't Add Up

**What goes wrong:** Summary statistics on the dashboard don't reconcile with the detail rows visible in tables or charts. "Total overcharges recovered: $2.4M" but the invoice table only shows 8 invoices totaling $84,000. Enterprise finance buyers will add numbers in their head.

**Prevention:**
- Build data as a single JavaScript object / array at the top of the file, and derive all displayed numbers from that source of truth using computed sums
- Never hardcode summary stats independently from detail data
- Run a manual sanity check: sum every table column, verify every chart total, confirm every KPI card

---

### Pitfall 8: Mobile Layout Breaking During Screen Share

**What goes wrong:** Screen sharing on Zoom/Teams often triggers responsive CSS breakpoints because the shared window is resized. A dashboard that looks great at 1440px wide may wrap badly at 1024px or 900px when the call attendee resizes their window or shares a partial screen.

**Prevention:**
- Test at 1024px, 1280px, and 1440px widths before any demo
- Avoid `grid-template-columns: repeat(4, 1fr)` for KPI cards without a `minmax` fallback — this breaks catastrophically at narrow viewports
- Set `min-width: 1024px` on the body if the demo is explicitly desktop-only, which prevents any responsive reflow
- For Zoom screen share specifically, open the file in its own Chrome window sized to exactly 1280x800 before the call

---

### Pitfall 9: Sticky Navigation Causing Z-Index Conflicts with Modals/Tooltips

**What goes wrong:** The demo uses `position: sticky` for the tab navigation (as the current demo does at `z-index: 100`). Modals, popovers, chart tooltips, and dropdown elements that need to appear above the nav require `z-index > 100`. Developers forget to set these values, so tooltips appear behind the sticky nav, cut in half.

**Prevention:**
- Establish a z-index scale in CSS variables: `--z-nav: 100; --z-tooltip: 200; --z-modal: 300; --z-overlay: 400`
- Chart tooltip containers must use `--z-tooltip` or higher
- Test by deliberately triggering a tooltip on a row near the top of a scrolled table

---

### Pitfall 10: Fonts That Read Poorly at Small Sizes in Low-Contrast Dark Theme

**What goes wrong:** Dark dashboards with "cool" muted text colors (`#64748B` slate-500 on `#0B1F3A` navy) fail WCAG AA contrast ratios. During a screen share, video compression further degrades contrast, making table text nearly unreadable. Finance buyers often have "can I see that number?" moments that reveal when text is illegible.

**Why it happens:** Designers tune for perfect monitor conditions. Video compression and projector gamma shift color contrasts significantly downward.

**Prevention:**
- Use `#94A3B8` or lighter for secondary text on dark backgrounds — not `#64748B`
- Primary data values (amounts, dates, status) should be `#E2E8F0` or white on dark cards
- Apply WCAG AA minimum (4.5:1 contrast ratio) to ALL text, including table cells and chart axis labels
- Test the demo on a compressed Zoom screen share recording and assess readability

---

### Pitfall 11: Animation Replaying Unexpectedly During Demo

**What goes wrong:** CSS `@keyframes` entrance animations (cards sliding in, numbers counting up) fire on page load. If the presenter scrolls back to a section or refreshes to "reset" the demo, animations replay or — worse — don't replay because the class was already applied and there's no reset mechanism. Either behavior looks broken.

**Prevention:**
- Use JavaScript to add a `.visible` class on entrance so animations can be explicitly reset
- For number count-up animations specifically, ensure they can be re-triggered from a button or simply don't use count-up (static numbers load instantly and look just as compelling)
- Provide a keyboard shortcut or button to reset to "fresh state" for re-demos in the same call

---

## Minor Pitfalls

---

### Pitfall 12: Scrollbar Visible in Presentation Mode

**What goes wrong:** The browser's default scrollbar appears on the right edge of the demo during full-screen presentation. On Windows Chrome it's a wide gray bar; in screen share it's visually distracting.

**Prevention:** Add `scrollbar-width: thin; scrollbar-color: #334155 transparent;` for Firefox and `::-webkit-scrollbar { width: 6px; }` for Chrome/Safari. Or hide entirely with `overflow: hidden` on body if the demo is panel-based (content doesn't scroll).

---

### Pitfall 13: `position: sticky` Breaking Inside Overflow Containers

**What goes wrong:** The tab navigation uses `position: sticky; top: 0`. If any ancestor element has `overflow: auto`, `overflow: hidden`, or `overflow: scroll`, sticky positioning silently fails — the nav scrolls away with the content.

**Prevention:** Ensure no ancestor of the sticky nav has `overflow` set to anything other than `visible`. This is a silent failure that is hard to debug.

---

### Pitfall 14: Print / PDF Export Showing Unstyled Content

**What goes wrong:** Buyers sometimes hit Ctrl+P during or after a call to save the demo as PDF. Without `@media print` styles, dark backgrounds print as solid black consuming ink, glass effects render as opaque blocks, and charts may not render at all in some print engines.

**Prevention:** Add a minimal `@media print { body { background: white; color: black; } .glass { background: white; border: 1px solid #ccc; } }` block.

---

## Phase-Specific Warnings

| Phase / Topic | Likely Pitfall | Mitigation |
|---|---|---|
| KPI summary cards | Numbers don't reconcile with detail data | Derive all stats from a single JS data array |
| Invoice detail table | Fake data exposed by domain experts | Use real SCAC codes, real LOCODEs, real surcharge names |
| Chart rendering | Tooltips clipped or invisible on dark backgrounds | Use ApexCharts (DOM tooltips) or Chart.js external tooltip plugin |
| Glassmorphism effects | Invisible panels on Safari, dark-on-dark failure | Include -webkit- prefix, semi-transparent background required |
| Entrance animations | Animations don't replay on demo reset | JS-controlled class toggling, not CSS-only |
| Demo delivery | Offline environment breaks CDN dependencies | Bundle all JS/fonts locally or inline |
| Screen share | Layout breaks at 1024px or tooltip clips under nav | Set z-index scale, test at narrow widths |
| Enterprise buyer review | Finance/ops buyer verifies numbers mentally | All KPI figures must sum correctly from data |
| Freight-domain credibility | Buyer spots wrong carrier codes or impossible routes | Maritime domain review checklist before demo |

---

## Maritime Domain Credibility Checklist

Before any live demo, verify:

- [ ] All carrier names have correct matching SCAC codes (Maersk = MAEU, MSC = MSCU, CMA CGM = CMDU, Hapag-Lloyd = HLCU, COSCO = OOLU, ONE = ONEY, Evergreen = EGLV)
- [ ] All port LOCODEs are real UN/LOCODE entries (USLAX, USOAK, USNYC, CNSHA, CNNGB, SGSIN, NLRTM, DEHAM, KRPUS)
- [ ] Container numbers follow ISO 6346 format: 4 uppercase letters + 7 digits + check digit
- [ ] IMO numbers are 7-digit and correspond to real vessel names if you use recognizable vessel names
- [ ] Invoice amounts are non-round, include cents, and fall within realistic per-TEU ranges ($2,000–$6,000 ocean, $200–$800 drayage)
- [ ] Surcharge names match real industry codes: BAF, CAF, PSS, EBS, THC, D&D, AMS, ISF
- [ ] Voyage numbers follow carrier-realistic format (not sequential integers)
- [ ] Date ranges span realistic transit times (CNSHA to USLAX is 14–21 days, not 2 days)
- [ ] Discrepancy amounts are plausible: 3–8% overbilling rate, not 50%+ (that would look suspicious even if it's a feature)

---

## Sources

- ApexCharts dark mode ghost background issue: [Issue #4028](https://github.com/apexcharts/apexcharts.js/issues/4028) and [Issue #3387](https://github.com/apexcharts/apexcharts.js/issues/3387) — LOW-MEDIUM confidence (open GitHub issues, not official docs)
- Safari backdrop-filter requirements: [Webflow Forum](https://discourse.webflow.com/t/solved-backdrop-filter-blur-in-safari/277926) and [graffino.com](https://graffino.com/til/how-to-fix-filter-blur-performance-issue-in-safari) — MEDIUM confidence (multiple community sources agree)
- Glassmorphism dark mode contrast failures: [playground.halfaccessible.com](https://playground.halfaccessible.com/blog/glassmorphism-design-trend-implementation-guide) — MEDIUM confidence
- CSS GPU compositing layer flicker: [Smashing Magazine](https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/) and [aerotwist.com](https://aerotwist.com/blog/on-translate3d-and-layer-creation-hacks/) — HIGH confidence (well-established browser behavior)
- Demo fake data quality signals: [Supademo blog](https://supademo.com/blog/dummy-data) and [freecodecamp.org](https://www.freecodecamp.org/news/how-our-test-data-generator-makes-fake-data-look-real-ace01c5bde4a/) — MEDIUM confidence
- SCAC code reference: [Beacon SCAC list](https://www.beacon.com/resources/ocean-carrier-scac-codes-list), [SeaRates](https://www.searates.com/reference/alpha-code/) — HIGH confidence (industry standard reference)
- Chart.js tooltip canvas clipping: [Chart.js docs](https://www.chartjs.org/docs/latest/configuration/tooltip.html) — HIGH confidence (official documentation)
- CSS sticky + overflow failure: established browser behavior, documented in [LambdaTest cross-browser guide](https://www.lambdatest.com/blog/css-browser-compatibility-issues/) — HIGH confidence
- Google Fonts offline / FOUT: [CSS-Tricks](https://css-tricks.com/google-fonts-and-font-display/) — HIGH confidence
- Enterprise buyer demo expectations: [Allego sales demo mistakes](https://www.allego.com/blog/product-demo-mistakes-and-how-to-fix-them-fast/), [Supademo best practices](https://supademo.com/blog/saas-demo-best-practices) — MEDIUM confidence
