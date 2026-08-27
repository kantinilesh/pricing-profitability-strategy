# Pricing & Profitability Intelligence Platform
## Bain & Company Case-Style Strategy Project | BCN Analyst Level

### 1. Executive Summary & Business Context
**OmniRetail India** is a fictional omnichannel retail chain operating 120+ physical stores across Tier 1, 2, and 3 cities in India alongside an e-commerce platform. Over the past 8 quarters, the company experienced robust top-line revenue growth (+18.4% YoY), driven by digital expansion and aggressive promotional campaigns. However, operating margin compressed by **240 bps**, resulting in volatile and unpredicted profitability.

Management has retained our strategy team to answer five core questions:
1. **Why is profitability changing?**
2. **Which products/customers/regions are driving the problem?**
3. **Are current prices and discounts optimal?**
4. **Which promotions actually create incremental value?**
5. **What pricing/profitability actions should management take?**

---

### 2. Analytical Sequence
Following the Bain & Company analytical framework:
`BUSINESS QUESTION → STRUCTURE → HYPOTHESES → DATA → ANALYSIS → VALIDATION → INSIGHT → QUANTIFICATION → RECOMMENDATION → IMPLEMENTATION`

---

### 3. MECE Issue Tree Architecture

```
                                  [ Net Profitability Compression ]
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
         [ Revenue & Margin Realization ]                           [ Cost Structure & Leakage ]
                   │                                                           │
     ┌─────────────┴─────────────┐                               ┌─────────────┴─────────────┐
     ▼                           ▼                               ▼                           ▼
[ Price Realization ]     [ Product & Channel Mix ]       [ Cost of Goods Sold ]      [ Cost-to-Serve & Spend ]
     │                           │                               │                           │
     ├─ List price vs market     ├─ High-vol / low-margin shift  ├─ Supplier price hikes     ├─ Logistics & fulfillment
     ├─ Off-invoice discounts    ├─ Channel cannibalization      ├─ Category mix inflation   ├─ Trade promo spend
     └─ Unplanned markdowns      └─ Region / tier dilution       └─ Shrinkage & inventory    └─ Returns & customer care
```

---

### 4. Hypothesis Tree

- **H1 (Discount Leakage)**: Uncontrolled off-invoice discounts on high-volume SKUs in e-commerce erode margin without driving proportional volume lift.
- **H2 (Customer Profitability)**: Legacy blanket discount structures for top-volume B2B/Enterprise customer accounts create negative pocket-margin sales.
- **H3 (Promotional Efficiency)**: Over 40% of trade promotions fail to deliver incremental ROI due to baseline demand subsidization and regional cannibalization.
- **H4 (Cost-to-Serve Disparity)**: Rapid Tier 2 & Tier 3 expansion has inflated last-mile fulfillment costs relative to order sizes, compressing regional margins.
- **H5 (Sub-optimal List Pricing)**: Inelastic premium SKUs are underpriced relative to Indian market competitors, leaving margin potential uncaptured.

---

### 5. KPI Dictionary

| Metric Category | KPI Name | Formula / Definition | Target / Benchmark |
|---|---|---|---|
| **Profitability** | Gross Margin % | \(\frac{\text{Net Revenue} - \text{COGS}}{\text{Net Revenue}} \times 100\) | > 35% |
| **Profitability** | Pocket Margin % | \(\frac{\text{Net Revenue} - \text{COGS} - \text{Fulfillment} - \text{Promo Spend}}{\text{Net Revenue}} \times 100\) | > 18% |
| **Pricing** | Discount Waterfall Rate | \(\frac{\text{List Price} - \text{Pocket Price}}{\text{List Price}} \times 100\) | < 15% aggregate |
| **Elasticity** | Price Elasticity (\(\epsilon\)) | \(\frac{\% \Delta \text{ Quantity}}{\% \Delta \text{ Price}}\) | Category specific |
| **Promotions** | Incremental Promo ROI | \(\frac{\text{Incremental Gross Margin} - \text{Promo Spend}}{\text{Promo Spend}}\) | > 1.5x |

---

### 6. Assumptions Register
- **Synthetic Data**: Explicitly labeled synthetic datasets calibrated to realistic Indian retail economics (INR, Festive seasonality, Tier 1/2/3 logistics).
- **Reproducibility**: Global random seed `42` used across data synthesis, statistical regressions, and optimization models.
- **Data Integrity**: Pocket price calculations enforce strict non-negative margin constraints.

---

### 7. Governance & Phase Roadmap
- **Phase 1**: Problem Structuring & Governance setup (Completed)
- **Phase 2**: Data Architecture & Synthetic Data Engine
- **Phase 3**: Data Quality Validation & ETL Pipeline
- **Phase 4**: Core Analytical Engines (Profitability, Pricing Elasticity, Customer, Promotions)
- **Phase 5**: Hypothesis Validation & Scenario Engine
- **Phase 6**: Product / FastAPI Backend & Interactive Executive Dashboard
- **Phase 7**: Executive Deliverables, Recommendation Deck & Git Integration
