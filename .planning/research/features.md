# Feature Landscape: B2B Invoice Chargeback Audit Dashboard + Founder Ops Dashboard

**Domain:** B2B SaaS — maritime/logistics invoice audit + internal ops
**Researched:** 2026-03-24
**Scope:** Two standalone HTML dashboards — one for sales demos (logistics buyers), one for founder ops (internal)

---

## Dashboard 1: Invoice Chargeback Audit Demo

This dashboard is a sales artifact. Its job is to make a logistics buyer feel the pain of overcharges
and immediately see VESSIQ as the solution. It must create an "aha" moment inside 60 seconds.

### Table Stakes (Must-Have for Credibility)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Summary KPI tiles (Total Invoiced, Total Overcharged, Total Recovered, Recovery %) | Every audit dashboard leads with this — buyers immediately ask "how much did you find?" | Low | 4 tiles max across top row |
| Invoices table with status column | Buyers need to see volume — "you processed 847 invoices" is more credible than abstraction | Low | Sortable, filterable by status |
| Error type breakdown (bar or donut chart) | Shows what kinds of errors VESSIQ catches — builds technical credibility | Low | BAF miscalc, duplicate billing, THC overcharge, unauthorized surcharge, D&D errors |
| Dispute status funnel | Shows the workflow: Detected → Disputed → Won / Lost / Pending | Medium | Visual pipeline not just a table |
| Date range filter | Standard for any financial audit tool — buyers will want to see a specific period | Low | Month/Quarter/Year toggle |
| Carrier breakdown | Shows multi-carrier coverage — critical for ocean freight where each carrier has quirks | Low | Bar chart or table: Maersk, MSC, Evergreen, Hapag-Lloyd, CMA CGM |
| Per-invoice drill-down | Buyers need to see one real example — line-by-line breakdown of what was overcharged and why | Medium | Modal or slide-out panel |

### Differentiators (What Sets VESSIQ Apart)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| "Money left on table" callout | Show the buyer what they're CURRENTLY LOSING — not just recovered amount, but estimated annual exposure if not using VESSIQ | Low | Prominent banner or callout block |
| D&D validation panel | Ocean-specific — FMC compliance check on detention/demurrage invoices. Nobody else does this well | Medium | Show FMC-required fields, flag violations |
| Gainshare ROI calculator | Interactive: enter monthly freight spend → see estimated recovery → see VESSIQ fee → see net benefit | Medium | One of the most powerful demo interactions possible |
| Confidence score on disputes | Each flagged invoice has a "dispute confidence: 94%" — shows AI rigor, not just dumb rules | Medium | Color-coded badge on each disputed item |
| Source format badges | Show "EDI 310 / PDF / CSV" tags on each invoice — demonstrates normalization capability | Low | Visual proof of VESSIQ's core tech |

### Anti-Features (Do Not Build in Demo)

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| User auth / login screen | Adds friction to demo — buyers bounce at a login wall | Start demo immediately, no gate |
| Full integration settings UI | Buyers don't care how data gets in during demo — they care about results | Static or pre-loaded sample data is fine |
| Real-time data loading spinners | Fake loading in a demo feels dishonest and slow | Pre-populate all data, instant render |
| 10+ KPI tiles | Overwhelming, dilutes the "aha" moment | Max 4-5 tiles, highest-impact metrics only |
| Editable data fields | Creates confusion in a demo context | Read-only is cleaner and more impressive |

### Invoice Audit Dashboard: Specific Data to Show

These are the numbers that convert in a logistics buyer demo. Use realistic but favorable values.

**KPI Tile Row:**
- Total Invoices Processed: 847
- Overcharge Rate: 34% of invoices (realistic — industry says 10-80% depending on source; ocean is high)
- Total Overcharged Amount: $284,000 (based on ~3 months of freight activity for a mid-market shipper)
- Total Recovered: $187,500 (66% recovery rate — achievable with good dispute management)

**Error Type Distribution (chart data):**
- BAF/bunker surcharge miscalculation: 28%
- Unauthorized surcharges: 22%
- Duplicate billing: 19%
- THC/terminal handling overcharge: 17%
- D&D invoice FMC violations: 14%

**Carrier Coverage (show these carriers specifically):**
- Maersk, MSC, Evergreen, Hapag-Lloyd, CMA CGM, COSCO
(9 major ocean carriers total — showing 6 in demo is sufficient)

**Dispute Status:**
- Auto-disputed and won: 142 disputes, $187,500 recovered
- Pending carrier response: 67 disputes, $94,200 in play
- Insufficient evidence (flagged for review): 31
- Confirmed valid (auto-approved): 607

### Invoice Audit Dashboard: Key Interactions for Demo

Priority order for what interactions to build. Each should produce a visible, satisfying result.

1. **Click a "Disputed" invoice row** → slide-out panel showing line-by-line breakdown: contracted rate vs. billed rate, delta, and auto-generated dispute language. This is the single most impressive interaction.

2. **Toggle carrier filter** → table and charts update instantly to show only that carrier's invoices. Demonstrates granular visibility.

3. **ROI calculator input** → buyer enters their monthly freight spend ($500K), calculator shows estimated overcharges ($25K-$40K/month), estimated VESSIQ fee ($3,750-$6,000), and net recovery. This closes deals.

4. **Date range switch (Month / Quarter / Year)** → tiles and charts update to show the difference in scale. Seeing $60K recovered in one month vs. $187K over a quarter vs. $750K annual projection is motivating.

5. **"Export dispute package" button** → even if it's a fake download in demo, showing a PDF button with "dispute_package_MSC_inv_2024-11-04.pdf" makes it feel real and operational.

---

## Dashboard 2: Founder Ops Dashboard (Internal)

This dashboard is a decision support tool for Sean. It replaces scattered notes, Notion pages,
and mental overhead with a single view that answers: "Where am I, what's next, and is this working?"

### Table Stakes

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Pilot tracker (customer name, status, key dates) | Core operational fact — who are we actually working with | Low | Table: Name, Industry, Status (Active/Stalled/Won/Lost), Freight Spend, Phase |
| Weekly task list with status | Founder needs to see "what I committed to" vs "what I've done" | Low | Simple checklist, not a full PM tool |
| Pipeline KPI tiles | MRR, Pilots Active, Deals in Progress, Avg Time to Close | Low | 4-6 tiles, updated manually or via simple edit |
| Benchmark comparison | Show VESSIQ's current metrics vs. industry benchmarks — "are we on track?" | Medium | Side-by-side: VESSIQ actual vs. benchmark target |
| Key decisions log | Captures the "why" behind strategic pivots — useful for investors and for founder memory | Low | Timestamped log entries with category tags |

### Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Phase progress tracker | Visual timeline of the expansion roadmap (Phase 1 → Phase 4) with current position marked | Low | Linear progress indicator with milestones |
| Customer health scorecard | Each pilot customer gets a simple health score: engagement, data quality, dispute wins | Medium | Traffic light (red/yellow/green) per customer |
| Weekly focus block | Forces prioritization — "this week's ONE thing" prominently displayed | Low | Single text block at top of dashboard |
| Revenue projection bar | Shows current MRR vs. 90-day target — creates visible urgency | Low | Simple progress bar with dollar labels |

### Anti-Features (Founder Ops)

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Full CRM feature set | Overkill — Sean has Notion or a spreadsheet for that | Link out to existing tool, don't replicate it |
| Automated data pipeline | Internal dashboard should be manually updated — complexity kills usage | Simple editable fields or hardcoded values |
| Investor reporting layout | Different audience, different format | Keep this operational, not polished for outsiders |
| Daily check-in prompts | Friction that kills daily usage | Dashboard should be passive — open and see, no input required |

### Founder Ops: Specific KPIs to Track

These are the metrics a pre-revenue or early-revenue logistics SaaS founder should watch.

**Pilot Metrics:**
- Pilots active: target 2-3 in first 90 days
- Avg freight spend per pilot customer (proxy for deal value)
- % invoices successfully parsed on first attempt (data quality signal)
- # disputes filed, # won, win rate % (product validation signal)
- Days since last customer touchpoint (engagement health)

**Business Metrics:**
- MRR (or ARR) — even if zero, show the target
- Customer Acquisition Cost (CAC) — once deals start closing
- Net Revenue Retention — not relevant pre-revenue, but set up the structure
- Burn rate vs. runway (weeks) — existential metric for pre-seed

**Benchmarks to Display (industry context):**
- Freight audit industry overcharge rate: 3-8% of freight spend (National Transportation Institute)
- Ocean-specific overcharge rate: 30-80% of invoices contain errors (per VESSIQ's own research)
- Dispute win rate at mature firms: 60-75%
- Time to first dispute resolution: 15-45 days (carrier dependent)
- Freight Audit & Payment market CAGR: 13.8% (growing fast — good for investor conversations)

### Founder Ops: Task Management Pattern

Do not build a full task manager. Use a structured weekly sprint format:

- **This Week (3 items max):** Constrained list of the top 3 priorities
- **Blocked / Waiting On:** Items where Sean needs an external response
- **Done This Week:** Quick wins log — motivating and useful for weekly recap emails to investors

---

## Industry Benchmarks: What to Show in the Demo

These are cited, real benchmarks to use in the sales demo dashboard. Use them as pre-loaded "proof points."

| Metric | Value | Source Confidence |
|--------|-------|-------------------|
| Freight invoices containing errors | 10% overall; up to 80% for ocean | MEDIUM — National Shippers Strategic Transportation Council (10%), VESSIQ internal analysis (80% ocean) |
| Ocean invoices with errors (2021-2024 peak) | 45% with missing/wrong information | MEDIUM — industry analysis cited in freight audit coverage |
| Ocean invoices with errors (current) | 30%+ still erroneous | MEDIUM — post-2021 improvement but still high |
| Freight spend recoverable via audit | 1-5% conservative; 3-7% typical; 8% high end | HIGH — National Transportation Institute (2-5%), Zero Down Supply Chain (3-7%), Gartner Logistics Report 2025 (8%) |
| AP staff time on invoice disputes | Up to 20% of AP staff time | MEDIUM — industry research cited by freight audit vendors |
| Freight Audit & Payment market CAGR | 13.8% in 2025 | MEDIUM — market research cited by multiple vendors |
| Window to dispute freight errors | Days to 30 days (carrier dependent) | HIGH — widely documented in freight audit literature |
| Avg savings for mid-market shipper | $150K-$750K/year on $5M-$15M freight spend | LOW — extrapolated from 3-5% recovery rate, not a single sourced figure |

**Note on the 80% ocean figure:** VESSIQ's own strategy documents cite "80% of invoices contain errors." This is likely a high-end figure representing any discrepancy including minor ones. Use it in demos but be prepared to explain that severity ranges from minor to material. The defensible number for serious buyers is "30-45% contain billing errors significant enough to dispute."

---

## Interactive Demo Best Practices (HTML Demo Context)

Research confirms these interactions specifically impress enterprise logistics buyers in sales demos.

### The "Aha" Moment Architecture

Every good demo has 2-4 moments where the buyer feels the product value viscerally, not intellectually.
For VESSIQ's invoice audit demo, the architecture should be:

**Moment 1 (within 5 seconds of opening):** The hero number — "$284,000 in overcharges detected" displayed prominently. Buyers think "that's what I'm leaving on the table."

**Moment 2 (within 30 seconds):** Click one disputed invoice row and see the exact line-item breakdown — "Maersk billed BAF at $847, your contract says $612, delta: $235." This proves the product works at a granular, verifiable level.

**Moment 3 (within 60 seconds):** The ROI calculator. They enter their number. They see their potential recovery. They see the VESSIQ fee is small compared to the return. This is the close.

**Moment 4 (optional, for technical buyers):** The source format badge on each invoice ("Parsed from EDI 310 / PDF / CSV") and the confidence score. This proves it's not just a spreadsheet — it's a normalization engine.

### Demo Interaction Rules

- No login gate. Demo opens directly to the populated dashboard.
- All data pre-loaded. No loading states, no spinners.
- Interactions should produce visible, immediate results (filter, drill-down, calculator).
- Max 3 clicks to reach any key insight.
- Mobile-friendly layout — demos increasingly happen on iPads in meetings.
- Personalization hook: include a placeholder "Pasha Group" customer name in the demo data as a subtle signal to the warm intro lead.

### What Enterprise Logistics Buyers Specifically Want to See

Based on research into enterprise freight audit software evaluations:

1. **Multi-carrier coverage** — they want to know you handle their specific carriers, not just one
2. **Contract rate matching** — not just "we found errors" but "your contract says X, they billed Y"
3. **Dispute automation evidence** — they want to see the actual dispute package that gets submitted, not just a flag
4. **Reporting granularity** — lane-level, carrier-level, error-type-level breakdowns
5. **Integration story** — even in demo, showing "works with your TMS / ERP / carrier portals" increases confidence
6. **Audit trail** — they need to show their CFO every decision — every dispute, every approval, every recovery

---

## Feature Dependencies

```
ROI Calculator → needs KPI tiles data (Total Invoiced, Overcharge Rate)
Dispute drill-down → needs invoice table with populated status
Carrier filter → needs invoice table with carrier tags
Source format badges → needs invoice data with format metadata
Customer health scorecard → needs pilot tracker data
Revenue projection bar → needs MRR tile data
```

---

## MVP Recommendation for Demo Build

### Invoice Audit Demo — Build Order

1. Hero KPI tiles row (4 tiles: invoices processed, overcharge rate, total overcharged, recovered)
2. Invoice table with status badges (color-coded: Disputed/Won/Pending/Approved)
3. One-invoice drill-down panel (the most important single interaction)
4. Error type chart (donut or horizontal bar)
5. Carrier breakdown table
6. ROI calculator widget
7. Date range toggle (Month/Quarter/Year)
8. Dispute status funnel (visual pipeline)

### Founder Ops Dashboard — Build Order

1. Weekly focus block ("This week's ONE thing")
2. KPI tiles (MRR, Pilots Active, Deals in Progress, Runway)
3. Pilot tracker table (customer, status, health indicator)
4. This week's tasks + blocked items
5. Phase progress tracker
6. Benchmark comparison panel

### Defer

- Real data connections (both dashboards should be static HTML with hardcoded data for now)
- User auth
- Notification system
- Export to PDF (fake button is sufficient for demo)
- Editable founder ops fields (manual update is fine for now)

---

## Sources

- [Freight Invoice Auditing Software: Purpose, Features & Best Platforms 2025 — Avantiico](https://avantiico.com/freight-invoice-auditing-software/) — MEDIUM confidence
- [Freight Invoice Audits and Why They Matter — FreightWaves](https://www.freightwaves.com/news/freight-invoice-audits-and-why-they-matter) — MEDIUM confidence
- [The 2025 Guide to Freight Recovery Audits — Auditec Solutions](https://auditecsolutions.com/freight-recovery-audit/) — MEDIUM confidence
- [Take Control of Freight Costs with Automated Freight Invoice Audit & Payment — IntelliTrans](https://www.intellitrans.com/2025/02/01/automated-freight-invoice-auditing-payment/) — MEDIUM confidence
- [Why Should You Audit Your Freight Bills? — SupplyChainBrain](https://www.supplychainbrain.com/blogs/1-think-tank/post/37257-why-should-you-audit-your-freight-bills) — MEDIUM confidence
- [Zero Down Supply Chain Solutions: FreightOptics — SupplyChainBrain](https://www.supplychainbrain.com/articles/43708-zero-down-supply-chain-solutions-freightoptics-freight-audit-and-payment-platform) — MEDIUM confidence
- [Interactive Demo Best Practices 2026 — Navattic](https://www.navattic.com/blog/interactive-demos) — MEDIUM confidence
- [Master SaaS Demos 2026 — Reprise](https://www.reprise.com/resources/blog/saas-demo-complete-guide) — MEDIUM confidence
- [UX for SaaS in 2025: What Top-Performing Dashboards Have in Common — Raw.Studio](https://raw.studio/blog/ux-for-saas-in-2025-what-top-performing-dashboards-have-in-common/) — MEDIUM confidence
- [10 B2B SaaS Metrics Founders Need to Track in 2025 — Kalungi](https://www.kalungi.com/blog/10-marketing-kpis-every-b2b-saas-company-should-track) — MEDIUM confidence
- [2025 B2B SaaS Benchmarks: CAC, NRR & Growth Rate Metrics — Pavilion](https://www.joinpavilion.com/resource/b2b-saas-performance-benchmarks) — MEDIUM confidence
- VESSIQ internal strategy documents: VESSIQ_Maritime_Application.md, VESSIQ_Wedge_Analysis.md, VESSIQ_Strategy_Updated.md — HIGH confidence (primary source)
