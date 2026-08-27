# Pricing Strategy Analysis & Econometric Evaluation
## OmniRetail India | Bain Case-Style Pricing Strategy

---

## 📌 Executive Summary & Core Strategic Recommendation

> **Core Question Answered**: *"What price strategy should management consider, for which products/customers, and why?"*

Management must **abandon one-size-fits-all cost-plus pricing** and execute a **differentiated 4-pillar pricing strategy** tailored by product category price sensitivity and customer segment willingness-to-pay:

```
                            DIFFERENTIATED PRICING STRATEGY
                                          │
        ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
        ▼                   ▼                           ▼                   ▼
┌───────────────┐   ┌───────────────┐           ┌───────────────┐   ┌───────────────┐
│ CATEGORY 1:   │   │ CATEGORY 2:   │           │ CUSTOMER 1:   │   │ CUSTOMER 2:   │
│ HOME & FASHION│   │ ELECTRONICS   │           │ B2B ENTERPRISE│   │ RETAIL PREMIUM│
├───────────────┤   ├───────────────┤           ├───────────────┤   ├───────────────┤
│ Selective +5% │   │ Strict Floor  │           │ Enforce 18%   │   │ Protect High  │
│ List Price    │   │ Pricing & Zero│           │ Contract Cap  │   │ Value & Co-Op │
│ Increase      │   │ Coupon Policy │           │ & Tiering     │   │ Bundles       │
└───────────────┘   └───────────────┘           └───────────────┘   └───────────────┘
```

1. **Home & Kitchen / FMCG**: **Selective List Price Increase (+5% to +10%)**.
   - *Why*: Highly inelastic demand (\(\beta = -0.062\) to \(-0.084\)) combined with strong competitor price headroom (indexed at 0.91 vs market). Generating **+₹4.97 Crore** in incremental gross profit.
2. **Consumer Electronics**: **Strict Price Floor & Coupon Elimination**.
   - *Why*: Low baseline gross margin (0.74% after fulfillment); price decreases (-5% or -10%) reduce profit without generating sufficient volume elasticity to cover variable costs.
3. **B2B Enterprise Accounts**: **Contract Discount Ceiling (18% Max Cap)**.
   - *Why*: Current legacy discounts (22.75% avg) create 84 value-destroying accounts; capping discounts recovers **+₹7.08 Crore** in net profit.
4. **E-Commerce Channels**: **Threshold Free-Shipping & Promo Rationalization**.
   - *Why*: Eliminating ad-hoc off-invoice coupons recovers **17.4% discount leakage**.

---

## 🎯 1. Business Objective Definition

The primary business objective is to **Maximize Operating Profit & Protect Net Margin** while maintaining selective top-line revenue momentum. 

- **Primary Goal**: Expand Gross Margin % from **34.3% to 37.5% (+320 bps)** within 12 months.
- **Secondary Goal**: Eliminate uncompensated discount leakage without sacrificing core retail customer retention.

---

## 🔬 2. Four Pricing Perspectives Analysis

```
                              4 PRICING PERSPECTIVES
                                        │
        ┌───────────────────┬───────────┴───────────┬───────────────────┐
        ▼                   ▼                       ▼                   ▼
    [ COST ]         [ COMPETITION ]        [ CUSTOMER VALUE ]     [ ELASTICITY ]
(Floor Protection)  (Index Benchmark)    (Willingness to Pay)  (Demand Response)
```

### 2.1 Perspective 1: Cost Structure & Floor Pricing
- **Finding**: Variable cost per unit averages **₹5,413.56** against an average list price of **₹7,755.20**.
- **Implication**: In low-margin categories like Consumer Electronics (variable cost ratio **99.26%**), cost floor protection is mandatory to prevent loss-making orders.

### 2.2 Perspective 2: Competitive Positioning & Price Indexing
- **Finding**: Home & Kitchen SKUs are priced **9% below** major Indian retail competitors (Amazon India, Reliance Retail, D-Mart). Consumer Electronics list prices are tightly matched (price index 0.99).
- **Implication**: Uncaptured pricing power exists in Home & Kitchen where competitors charge higher standard prices.

### 2.3 Perspective 3: Customer Value & Willingness to Pay
- **Finding**: Retail Platinum and Gold customers display low price sensitivity (avg discount rate **6.22%**), prioritizing catalog availability and convenience over markdowns. B2B Enterprise accounts capture **22.75% discounts** due to legacy contract terms rather than true volume tiering.
- **Implication**: B2B accounts are over-subsidized relative to their willingness to pay.

### 2.4 Perspective 4: Econometric Demand Response & Elasticity

#### Model Specification
$$\ln(\text{Units}) = \alpha + \beta \ln(\text{Realized Price}) + \gamma_1 \text{IsPromo} + \gamma_2 \text{IsWeekend} + \epsilon$$

| Product Category | Sample Size (\(N\)) | Elasticity (\(\beta\)) | Std Error | p-value | \(R^2\) | Demand Classification |
|---|---|---|---|---|---|---|
| **Consumer Electronics** | 12,109 | **-0.103** | 0.015 | < 0.0001 | 0.004 | Highly Inelastic |
| **Apparel & Fashion** | 11,922 | **-0.099** | 0.017 | < 0.0001 | 0.003 | Highly Inelastic |
| **Footwear** | 8,155 | **-0.129** | 0.023 | < 0.0001 | 0.004 | Highly Inelastic |
| **Beauty & Cosmetics** | 7,893 | **-0.134** | 0.023 | < 0.0001 | 0.004 | Highly Inelastic |
| **FMCG & Personal Care** | 8,004 | **-0.084** | 0.021 | 0.0001 | 0.002 | Highly Inelastic |
| **Home & Kitchen** | 11,917 | **-0.062** | 0.016 | 0.0001 | 0.001 | Highly Inelastic |

#### Methodological Limitations & Confounders
- **Correlation vs Causation**: Estimated elasticities reflect historical observational correlation rather than randomized A/B price test causality.
- **Omitted Variable Confounders**: Local competitor promotional campaigns and unobserved marketing spend may soften observed price sensitivity.
- **Endogeneity**: Store managers may apply discretionary markdowns when inventory velocity slows, confounding price and volume trends.

---

## 📊 3. Price Waterfall & Realization Breakdown

### Overall Company Unit Price Waterfall

```
[ List Price: ₹7,755.20 ]
        │
        ├── Contract Discounts: -₹580.40 (7.49%)
        ├── Promo & Ad-hoc Markdowns: -₹655.09 (8.44%)
        ▼
[ Realized Price: ₹6,519.71 ] (84.07% Realization)
        │
        ├── Variable COGS & Logistics: -₹5,413.56
        ▼
[ Gross Profit: ₹1,106.15 ] (16.97% Net Unit Margin)
```

- **List-to-Realized Realization**: **84.07%** (15.93% Aggregate Discount Rate).
- **Discount Frequency**: **46.14%** of all transactions receive an off-invoice discount.

### Price Realization by Segment, Channel, and Region

| Segment / Channel | Avg List Price (INR) | Avg Realized Price (INR) | Discount Rate % | Realization Rate % | Gross Margin % |
|---|---|---|---|---|---|
| **B2B Enterprise** | ₹8,154.67 | ₹6,299.17 | **22.75%** | **77.25%** | 15.07% |
| **B2B SMB** | ₹7,362.15 | ₹6,265.58 | **14.89%** | **85.11%** | 11.43% |
| **Retail Platinum** | ₹8,313.17 | ₹7,736.63 | **6.94%** | **93.06%** | 25.07% |
| **Retail Standard** | ₹8,318.11 | ₹7,694.03 | **7.50%** | **92.50%** | 31.085% |
| **E-Commerce Direct** | ₹7,696.16 | ₹6,355.48 | **17.42%** | **82.58%** | 17.41% |
| **E-Commerce Marketplace** | ₹7,581.64 | ₹6,293.77 | **16.99%** | **83.01%** | 7.64% |
| **Physical Retail Store** | ₹7,848.87 | ₹6,679.96 | **14.89%** | **85.11%** | 20.33% |

---

## 📈 4. Price-Volume-Profit Scenario Simulation

### Home & Kitchen Category Scenarios
- **Baseline (0%)**: Revenue ₹102.13 Crore | Gross Profit ₹38.74 Crore | Margin **37.94%**
- **+5% Price Hike**: Revenue ₹106.90 Crore | Gross Profit **₹43.71 Crore** | Margin **40.89%** (**+₹4.97 Crore Profit**)
- **+10% Price Hike**: Revenue ₹111.64 Crore | Gross Profit **₹48.65 Crore** | Margin **43.58%** (**+₹9.91 Crore Profit**)
- **-5% Price Cut**: Revenue ₹97.32 Crore | Gross Profit **₹33.74 Crore** | Margin **34.67%** (**-₹5.00 Crore Loss**)
- **-10% Price Cut**: Revenue ₹92.48 Crore | Gross Profit **₹28.71 Crore** | Margin **31.04%** (**-₹10.04 Crore Loss**)

---

## 💡 5. Tailored Strategic Pricing Recommendations

### Recommendation 1: Home & Kitchen & FMCG Categories
- **Action**: Implement selective **+5% list price increase** on top 30 SKUs.
- **Rationale**: Demand is price inelastic (\(\beta = -0.062\)); prices are 9% lower than market competitors.
- **Financial Impact**: **+₹4.97 Crore gross profit expansion**.

### Recommendation 2: B2B Enterprise Accounts
- **Action**: Enforce an **18.0% contract discount ceiling** combined with a minimum annual volume commitment of ₹50 Lakhs.
- **Rationale**: Enterprise discounts currently average 22.75%, driving 84 accounts into negative margin territory.
- **Financial Impact**: **+₹7.08 Crore profit recovery**.

### Recommendation 3: Consumer Electronics Category
- **Action**: Establish a **strict price floor** equal to COGS + 4% fulfillment cost; terminate off-invoice digital coupons.
- **Rationale**: Price decreases dilute margin without driving sufficient volume elasticity to offset unit cost.
- **Financial Impact**: Protects baseline gross margin from eroding below zero.
