# Executive Business Intelligence Dashboard Specification
## OmniRetail India | Bain Case-Style BI Dashboard Design

---

## 📌 Executive Philosophy: Action-Oriented Decision Support

> **Philosophy**: A strategy dashboard is **NOT a collection of generic charts**. It is an interactive executive decision support platform where every page answers a specific management question using **top-down communication** and **concise action-oriented titles**.

```
                         7-PAGE EXECUTIVE BI DASHBOARD ARCHITECTURE
                                              │
        ┌───────────────┬───────────────┬─────┴─────────┬───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼               ▼               ▼               ▼               ▼
     PAGE 1          PAGE 2          PAGE 3          PAGE 4          PAGE 5          PAGE 6          PAGE 7
 Executive       Profitability       Pricing         Products        Customers       Promotions      Scenarios
  Summary          Diagnosis         Strategy       Portfolio        Economics      Effectiveness    Engine
```

---

## 📄 Page-by-Page Specifications & Action Titles

### Page 1: Executive Summary
- **Concise Action Title**: *"Operating Margin Compressed by 240 bps Despite 18.4% Revenue Growth"*
- **Management Question Answered**: What is the overall state of the business, what is the core driver of margin change, and what is the primary recommendation?
- **Key Metrics Displayed**: Total Net Revenue (₹532.5M), Gross Profit (₹90.35M), Gross Margin % (16.97%), Major Change Summary, Top Driver Summary, Quantified Recovery Opportunity (+359 bps).
- **Core Visuals**: High-level Executive KPI cards & Strategic Transformation callout box.

### Page 2: Profitability Diagnosis & Bridge
- **Concise Action Title**: *"Profit Erosion is Driven by Price-Volume-Mix Leakage and Regional Logistics Overruns"*
- **Management Question Answered**: Why is margin compressing over time, and how do categories and regions contribute to gross profit variance?
- **Key Metrics Displayed**: Monthly Revenue & Margin % trend line, Category Gross Profit share, Regional Margin variance (West 36.8% vs North-East 31.1%).
- **Core Visuals**: 24-Month Margin Trend Line Chart & Category/Region Margin Variance Table.

### Page 3: Pricing Strategy & Demand Response
- **Concise Action Title**: *"Uncaptured Pricing Power Exists in Price-Inelastic Home & Kitchen SKUs"*
- **Management Question Answered**: How large is the gap between list and realized prices, and what is the category-level price elasticity of demand?
- **Key Metrics Displayed**: Average MSRP List Price (₹7,755), Realized Price (₹6,520), Aggregate Discount Rate (15.93%), Log-Log Econometric Elasticities (\(\beta\)) per category.
- **Core Visuals**: Category Price Elasticity Table & Discount Waterfall Summary.

### Page 4: Product Portfolio & Pareto
- **Concise Action Title**: *"Top 20% SKUs Generate 75.7% of Profit While 35 Dog SKUs Dilute Margin"*
- **Management Question Answered**: Which products drive gross profit vs which SKUs absorb inventory capital while delivering low margins?
- **Key Metrics Displayed**: 80/20 SKU Pareto Distribution, Portfolio Archetypes (Revenue & Profit Stars, Niche Profit Stars, Volume-Heavy Low-Margin, Dog SKUs).
- **Core Visuals**: Product Portfolio Matrix Archetype Table & Top SKUs Summary.

### Page 5: Customer Economics & Segmentation
- **Concise Action Title**: *"84 B2B Accounts Destroy ₹7.08 Crore Profit Due to Un-Capped Contract Discounts"*
- **Management Question Answered**: Which customer segments deliver net margin vs which accounts are over-discounted relative to volume contribution?
- **Key Metrics Displayed**: Customer Account Count, 2x2 Value x Discount Matrix (Core Champions, Subsidized Accounts, Margin Diluters, Occasional Retail Buyers), AOV, Margin %.
- **Core Visuals**: Customer Value Matrix Table & Value-Destroying B2B Account Breakdown.

### Page 6: Promotion Effectiveness & Trade Spend ROI
- **Concise Action Title**: *"End of Season Clearance Markdowns Operate at -1.88x Negative ROI"*
- **Management Question Answered**: Which promotional campaigns create net incremental profit vs which sales subsidize baseline demand?
- **Key Metrics Displayed**: Net Trade Spend, Estimated Incremental Gross Profit, Net Incremental Promo ROI, Campaign Decision Classification (**Continue / Modify / Stop**).
- **Core Visuals**: Campaign Archetype ROI Matrix Table.

### Page 7: Strategic Scenarios & Sensitivity Analysis
- **Concise Action Title**: *"Full Transformation Scenario G Recovers +359 bps (+₹19.12 Crore) Net Profit"*
- **Management Question Answered**: How do strategic alternatives (Scenarios A through G) compare in expected profit, margin expansion, and sensitivity risk?
- **Key Metrics Displayed**: Revenue, Gross Profit, Gross Margin %, Incremental Profit Delta, Margin Impact (bps), 3-Tier Sensitivity Analysis (Base, Upside, Downside).
- **Core Visuals**: Strategic Scenarios Matrix Table & 3-Tier Sensitivity Matrix Table.

---

## 🎛️ Interactive Global Filter Controls

Every page allows real-time interactive slicing and filtering across 4 business dimensions:
1. **Product Category**: `All`, `Consumer Electronics`, `Apparel & Fashion`, `Home & Kitchen`, `FMCG & Personal Care`, `Footwear`, `Beauty & Cosmetics`.
2. **Geographic Region**: `All`, `North`, `South`, `West`, `East`, `Central`, `North-East`.
3. **Sales Channel**: `All`, `Physical Retail Store`, `E-Commerce Direct`, `E-Commerce Marketplace`, `Quick-Commerce`.
4. **Customer Segment**: `All`, `B2B Enterprise`, `B2B SMB`, `Retail Platinum`, `Retail Gold`, `Retail Silver`, `Retail Standard`.

---

## 💻 Local Access & Application Execution

- **Start Dashboard API & Server**:
  ```bash
  uvicorn app.main:app --reload --port 8000
  ```
- **Access in Browser**: `http://localhost:8000/`
