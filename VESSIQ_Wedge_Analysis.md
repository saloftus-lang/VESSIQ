# VESSIQ Wedge Analysis: Deep Market Intelligence

## Executive Summary & Recommendation

**Start with Wedge #2: Retail/Logistics Chargeback Recovery — specifically targeting mid-size CPG suppliers selling into Walmart, Amazon, Target, and Costco.**

Why it wins:
- **Immediate, quantifiable ROI** — suppliers lose 2-5% of revenue to invalid deductions; you recover money directly
- **Gainshare pricing** — charge a % of recovered funds, so there's zero risk to the buyer
- **MVP buildable in 2-4 weeks** — parse remittance files, match against PODs/BOLs/ASNs, auto-generate dispute packages
- **Expansion path** — from dispute recovery → prevention → freight audit → full compliance platform → VESSIQ's broader data normalization vision
- **Proven market** — iNymbus (the leader) charges $0.40-$0.70/claim and has transformed 40-person teams into 2-person teams. But they're RPA-heavy, expensive to onboard, and focused on enterprise. The mid-market is wide open.

---

# 1. Rail EDI 322 Exception Automation

## 1.1 Current State of the Market

**What the 322 does:** The EDI 322 transaction set communicates terminal and intermodal ramp activities — ingates, outgates, arrivals, departures — between railroads, terminals, and shippers. It's the heartbeat of intermodal container tracking at rail yards.

**How companies handle this today:**
- Class I railroads (BNSF, UP, CSX, NS, CPKC, CN) each publish their own 322 implementation guides, all theoretically X12-compliant but with railroad-specific quirks
- Shippers receive 322 messages via VAN (value-added network) connections or direct AS2/SFTP. These feed into TMS platforms or custom integrations
- Exception handling is overwhelmingly manual: when a container doesn't show an expected outgate, or arrives at the wrong ramp, or has an equipment mismatch, an ops coordinator investigates via phone/email/railroad portal
- Bourque Logistics (RAILTRAC) is the dominant player for rail shippers — used by 140+ shippers for shipment operations, fleet accounting, and EDI data services. They recently announced RAILTRAC.ai for AI-enhanced operations
- Railinc processes over 9 million EDI messages daily across the North American rail network
- Most mid-size shippers (under 500 carloads/month) use a patchwork of spreadsheets, manual portal checks, and email-based escalation

**Key incumbents:**
- Bourque Logistics (RAILTRAC) — dominant for industrial rail shippers
- Railinc / TransmetriQ — industry utility for rail data
- SPS Commerce, Stedi — general EDI platforms (Stedi starts at ~$2K/month)
- TMS platforms (MercuryGate, BluJay/E2open) — handle some rail EDI but exception handling is bolted-on
- Railroad-specific portals (UP ShipmentTracker, BNSF EquipmentWatch) — free but siloed

## 1.2 Pain Points

**Failure point 1: Exception detection latency**
- 322 exceptions (container stuck at ramp, missed connection, equipment hold) are detected hours or days late because ops teams check portals manually or batch-process EDI
- Who feels it: Rail Operations Coordinators, Intermodal Planners
- Frequency: Daily for any shipper with 50+ intermodal moves/week
- Impact: A 24-hour delay in detecting a stuck container can cascade into missed delivery windows ($500-$2,000 per late delivery in retail), demurrage charges ($150-$350/day), and emergency truck substitutions ($1,500-$3,000)

**Failure point 2: Multi-railroad visibility fragmentation**
- A single intermodal move might touch 2-3 railroads. Each sends 322s in slightly different formats with different event codes. Reconciling these into a single shipment view is painful
- Who feels it: Supply Chain Managers, Transportation Directors
- Frequency: Constant for cross-country intermodal
- Impact: 2-4 hours/week per coordinator spent manually reconciling railroad data

**Failure point 3: Dwell time and demurrage disputes**
- Railroads charge per-diem/demurrage when containers sit too long. Shippers dispute these charges but lack clean data to prove the railroad caused the delay
- Who feels it: Fleet Managers, Finance/AP teams
- Frequency: Monthly billing cycle, but disputes accumulate
- Impact: $50K-$500K/year in demurrage for mid-size intermodal shippers; recovery rate on disputes is often under 30% due to poor documentation

**Failure point 4: Drayage coordination failures**
- When a 322 shows an outgate event, the shipper needs to dispatch a dray truck. If the 322 is late, misread, or the event code is ambiguous, the truck either arrives too early (detention) or too late (another per-diem day)
- Who feels it: Drayage Dispatchers, Intermodal Coordinators
- Frequency: Multiple times daily
- Impact: $200-$500 per miscoordination event

## 1.3 Wedge Opportunities

**Wedge A: Intermodal Exception Alerting**
- What it does: Ingests 322 messages across multiple railroads, normalizes event codes, and fires real-time alerts when containers deviate from expected milestones (missed outgate window, unexpected hold code, ramp diversion)
- Why it's painful: Ops teams currently scan portals or wait for batch EDI reports — they find out about problems after the damage is done
- Why incumbents don't solve it: Bourque is focused on industrial/carload rail, not intermodal exception alerting specifically. TMS platforms have exception modules but they're generic — they don't understand railroad-specific 322 event code nuances. Stedi is infrastructure-only (translation), not application-level
- Expansion path: Alerting → automated drayage dispatch triggering → demurrage audit → full intermodal orchestration platform

**Wedge B: Demurrage & Per-Diem Dispute Automation**
- What it does: Collects 322 event data, constructs a timeline proving railroad-caused delays, auto-generates dispute packages in the format each railroad's claims portal requires
- Why it's painful: Shippers leave 70%+ of valid disputes on the table because building the evidence package is manual and time-consuming
- Why incumbents don't solve it: Railroad billing departments (who charge demurrage) and the shippers' ops teams speak different data languages. No tool automates the evidence assembly
- Expansion path: Dispute recovery → proactive demurrage avoidance → fleet optimization → freight audit integration

**Wedge C: Multi-Railroad 322 Normalization API**
- What it does: Accepts 322 messages from any Class I railroad, normalizes them into a single clean JSON schema, and exposes a unified API for downstream systems
- Why it's painful: Every railroad has quirks in their 322 implementation. Shippers integrating with 3+ railroads spend weeks building custom parsers
- Why incumbents don't solve it: This is literally VESSIQ's core thesis — data translation/normalization. Stedi does generic EDI→JSON but doesn't normalize across railroad-specific implementations
- Expansion path: Normalization → exception detection → analytics → becomes the "Plaid for rail data"

## 1.4 Buyer + Budget Analysis

| Factor | Detail |
|--------|--------|
| Buyer | VP of Transportation, Director of Intermodal Ops, Rail Operations Manager |
| Budget owner | Operations (sometimes IT for integration projects) |
| Urgency (1-10) | 5-6 — painful but most teams have "learned to live with it" |
| Sales friction | HIGH — requires EDI connectivity setup, railroad relationship context, trust with operations data |
| Deal size potential | $3K-$8K/month for mid-size intermodal shipper (100-500 containers/week) |

## 1.5 Competitive Gaps

- Bourque (RAILTRAC) is strong but focused on carload/industrial — intermodal exception handling is secondary
- TMS platforms treat rail as an afterthought — their exception management is mode-agnostic and misses rail-specific nuances
- Stedi is infrastructure-only — they won't build application-layer intelligence
- No one has built a clean, modern, AI-powered tool specifically for intermodal 322 exception automation

## 1.6 Risks / Why This Could Fail

- **Integration friction is enormous.** You need VAN/AS2 connectivity to receive 322 messages. That's a 4-8 week onboarding cycle per shipper. Railroads also control the data pipes and can be slow to add new trading partners
- **Market size is narrow.** Only ~200-300 companies do enough intermodal volume to justify a dedicated tool. TAM might be $50-100M — not venture-scale without aggressive expansion
- **Railroad consolidation risk.** If CPKC or another railroad builds a better shipper portal, the pain decreases
- **Bourque could crush you.** They have 35+ years of rail relationships, 140+ shipper clients, and just launched an AI initiative. If you start winning, they add the feature
- **Data dependency.** You're entirely reliant on railroads sending clean 322 data. If a railroad changes their implementation (happens), your parser breaks
- **Companies may not pay.** Many shippers view this as "ops overhead" — they've built workarounds and the pain isn't acute enough to trigger a purchase

## 1.7 MVP Definition (Best Wedge: Demurrage Dispute Automation)

**Inputs:**
- 322 EDI files (uploaded or ingested via SFTP)
- Railroad billing/invoice files (per-diem or demurrage invoices)
- Shipper's shipment plan (expected pickup dates, delivery windows)

**Core logic:**
- Parse 322 events into a normalized timeline per container
- Compare actual events vs. expected plan to identify railroad-attributable delays
- Calculate disputable charges based on delay attribution
- Generate dispute letter with evidence (timeline, event codes, responsible party)

**Output:**
- Dashboard showing total demurrage, disputable amount, and auto-generated dispute packages
- PDF/CSV dispute files formatted for each railroad's claims submission process

**Build time:** 3-4 weeks with AI tools — but you'd need sample 322 files and railroad billing data, which requires a shipper partner

---

# 2. Chargeback Recovery in Logistics/Supply Chains

## 2.1 Current State of the Market

**What chargebacks are in this context:** Financial penalties imposed by retailers (Walmart, Amazon, Target, Costco, Kroger) on suppliers for non-compliance with shipping, labeling, documentation, and delivery requirements. These are NOT credit card chargebacks — they're B2B operational deductions.

**How companies handle this today:**
- Retailers automatically deduct chargebacks from supplier payments. The supplier sees a short-paid remittance and must manually investigate, gather evidence (BOLs, PODs, ASNs, tracking data), and submit disputes through each retailer's unique portal
- Walmart uses APDP (Accounts Payable Disputes Portal) through Retail Link — requires individual line-level disputes since 2023
- Amazon uses Vendor Central with automated compliance tracking
- Most suppliers have 1-5 dedicated AR/deduction analysts who manually process claims. A study found each claim takes 8-15 minutes of manual work
- Average single chargeback penalty: ~$190, but ranges from 1-5% of invoice value
- Typical mid-size supplier loses 2-5% of revenue to chargebacks/deductions

**Key incumbents:**
- **iNymbus** — market leader for retail deduction automation. Uses RPA bots to log into retailer portals, gather documents, and submit disputes. Supports 40+ retailers. Claims 30x speed improvement and 80-90% cost reduction. Pricing: ~$0.40-$0.70 per claim
- **HighRadius** — broader AR automation platform with deduction management module. Enterprise-focused, expensive
- **BlackLine** — financial close/AR automation. General purpose, not specialized for retail chargebacks
- **Chargebacks911** — focused on credit card chargebacks, not retail supply chain
- Many suppliers still use Excel spreadsheets and manual portal work

**Scale of the problem:**
- A Walmart apparel distributor reported ~3,000 deductions per quarter, requiring 400+ hours of manual processing
- One iNymbus customer transformed a 40-person deduction team into a handful of people
- Over $2 billion in eligible refunds per year goes unclaimed by businesses shipping with UPS and FedEx alone (just for parcel service failures)
- Freight audit firms typically recover 3-7% of total freight spend through audit-driven savings

## 2.2 Pain Points

**Failure point 1: Portal fragmentation**
- Each retailer has a different dispute portal with different evidence requirements, file formats, and submission processes. Walmart's APDP is different from Amazon Vendor Central is different from Target Partners Online
- Who feels it: AR Analysts, Deduction Specialists, Controllers
- Frequency: Daily
- Impact: A supplier selling to 5+ retailers needs staff who know each portal — training costs, turnover risk, and constant process changes

**Failure point 2: Deadline-driven revenue loss**
- Retailers enforce strict dispute windows (often 30-60 days). Missed deadlines = permanent revenue loss. When volume spikes (post-holiday, post-promotional), teams can't keep up
- Who feels it: AR Manager, CFO, VP Finance
- Frequency: Monthly cash flow impact
- Impact: Suppliers routinely write off 30-50% of disputable deductions simply because they couldn't process them in time

**Failure point 3: Document matching**
- Disputing a chargeback requires matching the deduction against BOLs, PODs, ASNs, carrier tracking data, and original PO details. This evidence lives in multiple systems (ERP, TMS, WMS, carrier portals)
- Who feels it: AR Analysts, Logistics Coordinators
- Frequency: Per-claim (thousands per quarter)
- Impact: 8-15 minutes per claim of purely manual document gathering

**Failure point 4: Invalid deductions are common**
- Retailers' automated systems generate many erroneous chargebacks — wrong quantities, duplicate deductions, system glitches. Suppliers who don't dispute them eat the cost
- Who feels it: Finance teams, P&L owners
- Frequency: Industry estimates suggest 30-60% of deductions are disputable
- Impact: Direct bottom-line hit. A $50M/year supplier losing 3% to chargebacks = $1.5M/year; recovering even half would be $750K

## 2.3 Wedge Opportunities

**Wedge A: AI-Powered Deduction Dispute Automation (THE BEST WEDGE)**
- What it does: Connects to supplier's ERP/remittance data, identifies new deductions, auto-matches against shipping documentation, and generates complete dispute packages for each retailer's portal
- Why it's painful: Manual processing costs $15-25 per claim in labor; many claims go uncontested due to volume
- Why incumbents don't solve it well: iNymbus is RPA-based (brittle, breaks when portals change), enterprise-focused (long sales cycles, expensive onboarding), and requires significant configuration. No one has built an AI-native solution for the mid-market ($10M-$200M revenue suppliers). HighRadius and BlackLine are too broad and too expensive
- Expansion path: Dispute recovery → prevention (pre-shipment compliance checks) → freight audit → full VESSIQ data platform

**Wedge B: Walmart-Specific APDP Automation**
- What it does: Narrow focus on automating Walmart deduction disputes through their APDP portal. Parses Walmart remittance data, matches against supplier's shipment records, and generates dispute evidence packages
- Why it's painful: Walmart changed their entire dispute process in 2023 (killed settlement disputing, moved to line-level disputes). Suppliers are still adjusting
- Why incumbents don't solve it well: iNymbus handles Walmart but bundles it with 40+ retailers — overkill and expensive for suppliers whose primary problem is Walmart
- Expansion path: Walmart → Amazon → Target → multi-retailer platform

**Wedge C: Freight Claim Recovery for Shippers**
- What it does: Monitors carrier invoices for service failures (late deliveries, overcharges, incorrect accessorials), auto-files claims with carriers (UPS, FedEx, LTL carriers), and tracks recovery
- Why it's painful: Shippers leave billions on the table annually in unclaimed carrier refunds
- Why incumbents don't solve it well: Freight audit firms (Trax, nVision, Trimble) are enterprise-oriented with 6-12 month implementations. Shipware and similar parcel audit tools use gainshare pricing but are parcel-focused. No modern, AI-native tool handles multi-modal freight claim recovery for the mid-market
- Expansion path: Carrier claims → full freight audit → rate optimization → VESSIQ platform

**Wedge D: Pre-Shipment Compliance Checker**
- What it does: Before a shipment goes out the door, validates it against the retailer's routing guide requirements (labeling, packaging, ASN format, carrier selection, delivery window). Flags violations before they become chargebacks
- Why it's painful: Prevention is 10x cheaper than recovery, but no tool does this well for multi-retailer suppliers
- Why incumbents don't solve it well: WMS systems have basic compliance checks but don't stay current with retailer requirement changes. The Vendor Compliance Federation tracks requirements but doesn't automate checking
- Expansion path: Compliance checking → chargeback recovery → supply chain analytics → VESSIQ platform

## 2.4 Buyer + Budget Analysis

| Factor | Detail |
|--------|--------|
| Buyer | VP Finance, AR Manager, Controller, VP Supply Chain |
| Budget owner | Finance (direct P&L impact makes this an easy budget conversation) |
| Urgency (1-10) | 8-9 — this is literally money being taken from them every month |
| Sales friction | LOW — gainshare pricing (you get paid from recovered money) eliminates risk for the buyer. No upfront cost = fast yes |
| Deal size potential | $2K-$15K/month depending on deduction volume. Gainshare model: 15-25% of recovered deductions |

## 2.5 Competitive Gaps

- **iNymbus is the clear market leader** but has weaknesses:
  - RPA-based (fragile when portals change UI)
  - Enterprise-focused (long sales cycles, $50K+ annual contracts)
  - No self-serve onboarding
  - Limited AI/intelligence — it's essentially a sophisticated bot, not a learning system
- **HighRadius/BlackLine** are too broad and too expensive for mid-market suppliers
- **Nobody serves the $10M-$200M supplier segment well** — too small for iNymbus, too big for spreadsheets
- **No one has built an AI-native tool** that can learn retailer patterns, predict which deductions are worth disputing, and auto-prioritize claims by recovery probability

## 2.6 Risks / Why This Could Fail

- **iNymbus has a 10-year head start.** They support 40+ retailers, have proven case studies, and their RPA bots are production-hardened. Building equivalent portal integrations is a significant engineering lift
- **Portal access dependency.** You need credentials to log into retailer portals (Retail Link, Vendor Central, etc.). The supplier must grant access, and retailers can change portal structures at any time
- **Gainshare model means delayed revenue.** You don't get paid until deductions are successfully recovered, which can take 30-90 days. Cash flow is lumpy
- **Retailers could make disputing easier.** If Walmart or Amazon improves their dispute process (unlikely but possible), the pain decreases
- **Legal/contractual complexity.** Some supplier-retailer agreements have specific provisions about dispute processes. You need to understand these
- **Commoditization risk.** If this becomes a pure RPA/bot play, any IT services firm can replicate it. The moat must be in intelligence, not just automation

## 2.7 MVP Definition (Best Wedge: AI Deduction Dispute Automation)

**Inputs:**
- Supplier's remittance files from 1-2 retailers (start with Walmart or Amazon)
- Supplier's shipment data: BOLs, PODs, ASNs, carrier tracking (from ERP/TMS export or CSV upload)
- Retailer's deduction detail (codes, amounts, PO references)

**Core logic:**
- Parse remittance file to extract all deductions with reason codes, amounts, and PO references
- Match each deduction against supplier's shipment records (fuzzy matching on PO #, date, SKU)
- Classify deduction as: (a) clearly invalid — auto-dispute, (b) ambiguous — flag for review, (c) valid — accept
- For disputable claims: auto-assemble evidence package (BOL excerpt, POD, delivery confirmation, ASN data)
- Generate formatted dispute document in retailer's required format

**Output:**
- Dashboard: total deductions this period, disputable amount, auto-resolved vs. needs-review
- Downloadable dispute packages ready for portal submission (or API submission if portal integration exists)
- Recovery tracking: submitted, pending, won, lost, with running ROI calculation

**Build in 2-4 weeks:**
- Week 1: Remittance parser + deduction classifier for Walmart format
- Week 2: Document matching engine (PO → BOL → POD linkage)
- Week 3: Dispute package generator + simple dashboard
- Week 4: Testing with real supplier data, iterate on matching accuracy

**Critical requirement:** You need ONE supplier partner willing to share their remittance files and shipment data. The Pasha Group conversation could be this — if they sell to retailers or handle goods that flow through retail supply chains.

---

# 3. Compliance Fines Prevention (Customs, Hazmat, Manifests)

## 3.1 Current State of the Market

**The compliance landscape:**
- **Customs (CBP):** Processes $4+ trillion in imports annually. Penalties for negligence reach tens of thousands per entry; fraud penalties can equal the domestic value of merchandise. CBP enforcement is at historic highs under current administration
- **Hazmat (PHMSA/DOT):** Fines range from $617 to $238,000+ per violation as of 2025. Maximum penalty for failure to provide hazmat employee training: $102,348. Non-compliance can also mean shipment rejection, delivery bans, and criminal charges
- **Manifests (AMS/ISF/AES):** Late or inaccurate manifest filings delay cargo and trigger fines. In just-in-time supply chains, even a 2-day customs delay can cascade into significant cost

**How companies handle this today:**
- Large companies: Dedicated compliance departments (5-20+ people), licensed customs brokers, and enterprise compliance software (Descartes, Amber Road/E2open, Thomson Reuters ONESOURCE)
- Mid-size companies: 1-2 compliance analysts using a mix of customs broker services, spreadsheets, and manual checks. Many rely entirely on their broker and hope for the best
- Hazmat: Companies like ShipHazmat automate shipping paper generation with built-in regulatory logic (49 CFR, IATA, IMDG). Training vendors (Hazmat University, Lion Technology, ICC) sell courses
- Freight forwarders: Use platforms like CargoEZ or Descartes for customs filing automation

**Key incumbents:**
- **Descartes Systems** — dominant in customs/trade compliance automation. Enterprise pricing, complex implementation
- **E2open (Amber Road)** — global trade management platform. Enterprise
- **Thomson Reuters ONESOURCE** — compliance and classification. Enterprise
- **CargoEZ** — customs compliance for freight forwarders. Growing mid-market player
- **CustomsCity** — AI-powered customs management for Section 321, AMS, ISF
- **ShipHazmat** — web-based hazmat shipping paper automation
- **Customs brokers** — thousands of licensed brokers handle filing for importers/exporters

## 3.2 Pain Points

**Failure point 1: HS code misclassification**
- Incorrect tariff classification is the #1 source of customs penalties. Products get classified wrong at origin, and nobody catches it until an audit
- Who feels it: Import/Compliance Managers, Supply Chain Directors
- Frequency: Per-shipment risk; audits can look back 5 years
- Impact: Penalties for negligent misclassification: up to $10,000 per entry. For 100 entries/month, a 5% error rate = significant exposure

**Failure point 2: Hazmat documentation errors**
- Manual creation of shipping papers/dangerous goods declarations is error-prone. Wrong UN numbers, missing special provisions, incorrect packaging references
- Who feels it: Shipping Clerks, EHS Managers, Warehouse Managers
- Frequency: Daily for hazmat shippers
- Impact: Shipment rejection ($500-$2,000 per event including rework, re-shipping, and delay costs), plus fine exposure of $617-$238K per violation

**Failure point 3: Late or inaccurate manifest filings**
- AMS (Automated Manifest System) and ISF (Importer Security Filing) filings have strict deadlines. Late filings = cargo holds and fines
- Who feels it: Freight Forwarders, Import Operations, Compliance Officers
- Frequency: Per-shipment
- Impact: $5,000-$10,000 per late ISF filing; cargo holds add $500-$2,000/day in detention/demurrage

**Failure point 4: Export compliance (EAR/ITAR/sanctions screening)**
- Exporters must screen against restricted party lists, classify under ECCN codes, and ensure proper end-use documentation. Failures result in fines, loss of export privileges, and criminal charges
- Who feels it: Export Compliance Officers, Legal
- Frequency: Per-shipment
- Impact: OFAC penalties up to $20M+; BIS penalties up to $300K per violation

## 3.3 Wedge Opportunities

**Wedge A: Automated Hazmat Shipping Paper Generation**
- What it does: Given a product/material description, auto-classifies the hazmat class, generates compliant shipping papers per 49 CFR / IATA / IMDG, and validates against current regulations
- Why it's painful: Manual paper prep is error-prone and regulations change annually
- Why incumbents don't solve it well: ShipHazmat exists but is basic. ERP systems have hazmat modules that are poorly maintained. Most shippers rely on tribal knowledge
- Expansion path: Shipping papers → compliance audit → carrier integration → full supply chain compliance

**Wedge B: Pre-Filing Compliance Validator**
- What it does: Before a customs entry or manifest is filed, runs automated checks: HS code validation, restricted party screening, document completeness, filing deadline alerts
- Why it's painful: Catching errors before filing prevents penalties and delays. Currently, brokers catch some errors but miss others, especially under volume pressure
- Why incumbents don't solve it well: Descartes and E2open are expensive and complex. Brokers are human and error-prone. No lightweight, AI-powered pre-check tool exists for the mid-market
- Expansion path: Pre-filing check → full customs management → trade analytics → VESSIQ platform

**Wedge C: ISF/AMS Filing Automation for Mid-Size Importers**
- What it does: Ingests commercial invoices, packing lists, and booking confirmations, auto-extracts required data fields, and generates/files ISF 10+2 and AMS entries
- Why it's painful: Mid-size importers (100-500 entries/month) pay $30-$75 per entry to customs brokers. Many of these filings are repetitive and follow patterns
- Why incumbents don't solve it well: CustomsCity and Descartes target either small e-commerce or large enterprise. The mid-market gets overcharged by brokers for routine filings
- Expansion path: Filing automation → compliance dashboard → HS code optimization (duty savings) → full trade management

**Wedge D: Compliance Fine Risk Scoring**
- What it does: Analyzes a company's shipping history, identifies patterns that correlate with compliance violations, and generates a risk score per shipment with specific remediation recommendations
- Why it's painful: Companies don't know where their compliance risks concentrate until after an audit/penalty
- Why incumbents don't solve it well: Audit-oriented approach is reactive, not predictive
- Expansion path: Risk scoring → automated remediation → continuous compliance monitoring → platform

## 3.4 Buyer + Budget Analysis

| Factor | Detail |
|--------|--------|
| Buyer | VP of Trade Compliance, Import/Export Manager, EHS Director, CFO (for fine avoidance) |
| Budget owner | Compliance (sometimes Legal, sometimes Ops) |
| Urgency (1-10) | 6-7 — high urgency after a penalty event, low urgency otherwise (the "ambulance" problem) |
| Sales friction | MEDIUM-HIGH — compliance buyers are conservative, want proven solutions, and may require legal review of any new tool |
| Deal size potential | $2K-$10K/month, but long sales cycles (3-6 months) |

## 3.5 Competitive Gaps

- **Enterprise tools are overkill for mid-market** — Descartes, E2open implementations cost $100K+ and take 6-12 months
- **Customs brokers are a middleman** — they charge per-transaction and have little incentive to help importers self-serve
- **Hazmat compliance is fragmented** — training is separate from documentation, which is separate from shipping operations
- **No unified "compliance health dashboard"** exists — companies can't see their aggregate risk across customs, hazmat, and documentation

## 3.6 Risks / Why This Could Fail

- **Regulatory complexity is extreme.** Building a compliance tool that's actually correct across 49 CFR, IATA, IMDG, customs regulations, and export controls is a massive domain challenge. A single error in your product could cause your customer to get fined — destroying trust and creating liability
- **Buyer inertia is the #1 enemy.** Companies that haven't been fined don't feel urgency. Selling prevention is always harder than selling recovery
- **Licensed customs broker requirement.** Many filing activities require a licensed customs broker. You'd either need to obtain a broker license (expensive, regulated) or partner with existing brokers
- **Incumbent moat.** Descartes has deep carrier/customs authority connectivity built over decades. Replicating their integration layer is non-trivial
- **Liability exposure.** If your tool misclassifies a hazmat shipment and someone gets injured, you face enormous liability. Insurance costs for compliance software vendors are high
- **This could easily become a features race** with well-funded competitors. Compliance is a domain where trust and track record matter more than innovation — a startup disadvantage
- **Not naturally aligned with VESSIQ's core thesis.** VESSIQ is about data translation/normalization. Compliance is about regulatory intelligence. The connection exists but isn't direct

## 3.7 MVP Definition (Best Wedge: Automated Hazmat Shipping Paper Generation)

**Inputs:**
- Product/material description (free text or structured)
- UN number (if known)
- Quantity, packaging type
- Transport mode (ground, air, sea)

**Core logic:**
- Map product to correct hazmat class, UN number, packing group
- Apply modal-specific regulations (49 CFR for ground, IATA DGR for air, IMDG for sea)
- Generate compliant shipping papers with proper descriptions, emergency contacts, and certifications
- Validate against current regulatory tables

**Output:**
- Formatted hazmat shipping paper (PDF)
- Validation report flagging any issues
- Regulatory reference links for each determination

**Build in 2-4 weeks:** Feasible for a single mode (ground / 49 CFR only). The core logic is lookup-table-driven with rules engine. However, **you need to validate accuracy extensively** — errors in hazmat documentation create real safety risk.

---

# Comparative Assessment

## Decision Matrix

| Criterion | Rail EDI 322 | Chargeback Recovery | Compliance Fines |
|-----------|:---:|:---:|:---:|
| Time to first revenue | 3-4 months | 4-6 weeks | 3-6 months |
| Sales friction | High | Low (gainshare) | Medium-High |
| Buyer urgency | 5-6/10 | 8-9/10 | 6-7/10 |
| TAM at $5K/mo | $12-18M | $200M+ | $100M+ |
| MVP complexity | High (EDI infra) | Medium | High (regulatory accuracy) |
| Competitive moat potential | Medium | Medium-High | Medium |
| Alignment with VESSIQ vision | Very high | High | Medium |
| Liability risk | Low | Low | High |
| Path to venture scale | Narrow initially | Clear | Unclear |

## The Verdict

**Start with Chargeback Recovery (Wedge 2A).** Here's why:

1. **Fastest path to revenue.** Gainshare pricing means suppliers say yes easily — you're literally offering free money. First revenue in 4-6 weeks with one pilot customer.

2. **Highest buyer urgency.** Finance teams watch deductions erode margins every single month. This isn't a "nice to have" — it's recoverable revenue sitting on the table.

3. **Lowest technical risk.** No EDI infrastructure to set up, no regulatory accuracy to guarantee. You parse remittance files (CSVs), match documents, and generate dispute packages. The AI tools you already have can handle this.

4. **Natural expansion to VESSIQ's vision.** Chargeback recovery requires normalizing data from multiple sources (ERP, TMS, WMS, carrier portals, retailer portals). This IS the data translation problem VESSIQ was built to solve. Start with the most painful application of that problem.

5. **iNymbus's weakness is your opportunity.** They're RPA-heavy and enterprise-focused. An AI-native, mid-market solution that onboards in days (not weeks) and learns from dispute outcomes would be genuinely differentiated.

## What to Build First

1. **Walmart remittance parser** — read APDP deduction data, extract reason codes, amounts, POs
2. **Document matching engine** — link deductions to BOLs, PODs, ASNs via PO number fuzzy matching
3. **Dispute package generator** — assemble evidence into Walmart's required format
4. **Simple dashboard** — show deduction totals, disputable amounts, dispute status, ROI

## What to Avoid

- **Don't start with Rail EDI 322.** The integration overhead (VAN connectivity, railroad onboarding) will burn months before you see revenue. Save this for later when you have cash flow and credibility
- **Don't build a compliance tool.** The liability, regulatory complexity, and buyer inertia will kill your speed. Compliance is a great market for a funded company with domain experts — not for a pre-revenue startup
- **Don't try to boil the ocean.** Start with ONE retailer (Walmart is the best — biggest, most chargebacks, APDP is standardized). Nail it. Then expand
- **Don't build your own RPA bots for portal submission** (yet). Start with generating dispute packages that the supplier's AR team uploads. Automate submission later once you've proven the matching/classification engine works

## Next Steps for Sean

1. **Find one CPG supplier** selling into Walmart with a chargeback problem. Ask Pasha Group contacts if they know anyone, or cold-outreach AR managers at mid-size food/beverage/apparel companies
2. **Get a sample Walmart remittance file** and their shipment records for one quarter
3. **Build the parser + matcher MVP** using Python + Claude/GPT for document extraction
4. **Run a proof-of-concept:** show them how much they could recover, then offer to run disputes on gainshare (20% of recovered funds)
5. **First revenue target:** $2K-$5K/month from one pilot customer within 8 weeks
