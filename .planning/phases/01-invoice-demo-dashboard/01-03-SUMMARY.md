---
phase: 01-invoice-demo-dashboard
plan: 03
wave: 3
status: complete
completed_at: "2026-03-25"
commits:
  - sha: a4fd07a
    message: "feat(01-03): add ApexCharts bar+donut charts and ROI calculator"
  - sha: bb1dd67
    message: "feat(01-03): restyle dashboard to light theme with 4-tab navigation"
requirements_delivered:
  - INV-08
  - INV-10
  - INV-11
  - INV-12
  - INV-13
  - REL-03
---

# Wave 3 Summary — Charts, ROI Calculator, and Visual Restyle

## What Was Built

**ApexCharts integration (INV-08, INV-10):**
- Horizontal bar chart showing overcharge amounts by carrier (MAEU, MSCU, EGLV, HLCU, PSHA, BNSF)
- Donut chart showing breakdown by charge type (BAF, Unauthorized, Duplicate, THC, D&D)
- Lazy initialization: `initCharts()` called only on first visit to Analytics tab via `showPanel(2)`
- Charts update on filter change via `chart.updateSeries()` — never re-initialized
- Light theme config: `theme: { mode: 'light' }`, `background: 'transparent'`, `grid.borderColor: '#E2E8F0'`

**ROI Calculator (INV-11):**
- Single input field accepting monthly freight spend
- Computes recovery (3.5% of annual), fee (25% of recovery), net benefit
- Live update on `input` event with `handleRoiInput()`

**Visual restyle (INV-12, INV-13):**
- Complete switch from dark glassmorphism to light white/blue theme matching `demo/index.html`
- 4-tab sticky navigation: Invoice Audit Dashboard | Analytics & Breakdown | ROI Calculator | Scale & Pilot
- Progress bar advances with each tab (25/50/75/100%)
- Navy header with hero section (stat row: $10B+, 80%, 1-8%)
- Scale & Pilot panel populated with pilot CTAs from old demo

**Reliability (REL-03):**
- All KPIs remain reactive via `renderKPIs()` in `render()` call chain
- No static KPI constants — tiles 2-4 computed from `getFilteredData()`
- `PORTFOLIO_TOTAL = 847` is the only permitted constant

## Decisions Made

- Restyled to match `demo/index.html` visual language per user request after seeing both demos
- ApexCharts light mode configured from the start to avoid dark mode ghost background bug (issues #4028/#3387)
- Scale & Pilot tab content populated from old demo to preserve full sales narrative

## Human Verification

User approved: "approved" — dashboard confirmed to look correct with light theme, 4-tab navigation, functional filters, charts, and ROI calculator.
