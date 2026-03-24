# VESSIQ — Maritime Application: Invoice Audit & D&D Recovery

---

## Why Maritime (Not Retail Chargebacks)

We evaluated three wedges: rail EDI 322, retail chargebacks, and compliance fines. Retail chargebacks were initially recommended as fastest-to-revenue, but maritime invoice audit won for VESSIQ because:

1. **Higher $ per transaction** — ocean freight disputes are $500-$50,000+ vs. $50-$500 for retail
2. **Lower per-customer friction** — 9 major carriers with standardized surcharges vs. 40+ retailers with unique portals
3. **Weaker competition** — one-man operation (Ocean Audit) is the market leader vs. iNymbus with 40+ retailer integrations
4. **Direct alignment with VESSIQ's maritime thesis** — same industry, same contacts, same data types
5. **Pasha Group relevance** — warm intro already in hand

---

## Three Revenue Streams Within Maritime

### 1. Ocean Freight Invoice Audit
- $10B+ overcharged 2021-2024
- 80% of invoices contain errors
- Errors: double billing, surcharge miscalculation, currency conversion, unauthorized charges
- Invoices come as PDFs, CSVs, EDI 310 — all different formats per carrier
- VESSIQ's normalization engine is the core technology

### 2. Demurrage & Detention (D&D) Dispute Recovery
- FMC requires specific fields on D&D invoices — missing fields = legally invalid invoice
- D.C. Circuit vacated key FMC billing rule in Sept 2025 — regulatory chaos = more disputes
- Common errors: wrong free time, charges during terminal closures, billing wrong party
- Cross-reference terminal data against carrier invoices to catch mismatches

### 3. Forwarder Billing Reconciliation
- Forwarders re-bill carrier charges with added margin
- Pass-through errors + forwarder markup errors compound
- Mid-market shippers rarely audit forwarder invoices
- VESSIQ normalizes invoices from multiple forwarders into single auditable schema

---

## How It Connects to Original VESSIQ Vision

The invoice audit engine IS the data normalization platform:

```
Original Vision: EDI, PDFs, emails → VESSIQ normalization → clean standardized output
Invoice Audit:   Carrier invoices (EDI, PDFs, CSVs) → VESSIQ normalization → discrepancy detection → recovered money
```

Same technology. The difference is that invoice audit has an immediate, quantifiable buyer: "we found $150K in overcharges."

### Evolution Path
- Invoice audit → proves the normalization engine works on real maritime data
- D&D recovery → expands to terminal/port data
- Forwarder reconciliation → adds multi-party data matching
- Compliance monitoring → layers on regulatory intelligence
- Full platform → you ARE the maritime data middle layer

The manifest translation layer lives underneath all of this. It's not abandoned. It's being funded by revenue.
