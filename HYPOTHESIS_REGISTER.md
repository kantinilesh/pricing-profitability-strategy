# Hypothesis Register

This register outlines 12 core hypotheses driving the profitability investigation for OmniRetail India.

---

### Hypothesis 1 (H1): Excessive Off-Invoice Discount Leakage
- **Hypothesis**: Uncontrolled off-invoice discounts and ad-hoc coupons on high-volume e-commerce SKUs erode net margin without driving elastic volume gains.
- **Why it might be true**: E-commerce marketing teams frequently apply stackable promotional codes to meet quarterly top-line revenue targets.
- **Evidence Required**: Transaction-level list price, contract discount, promo discount, ad-hoc discount, net revenue, and unit sales volume.
- **KPI**: Discount Waterfall Rate (%) & Net Realized Price.
- **Analysis Method**: Discount waterfall breakdown and volume-price correlation analysis.
- **Decision Implication**: Mandate central governance and approval thresholds for all off-invoice digital markdown coupons.

---

### Hypothesis 2 (H2): Customer Tier Discount Misalignment
- **Hypothesis**: Legacy contract discounts granted to top-volume B2B Enterprise accounts exceed their net margin contribution, rendering specific high-volume accounts unprofitable.
- **Why it might be true**: B2B sales reps are compensated on gross revenue rather than net pocket margin, leading to over-discounting.
- **Evidence Required**: Customer account order history, contract discount rates, fulfillment costs, COGS, and customer-level net margin.
- **KPI**: Customer Pocket Margin (%) & Net Pocket Profit (INR).
- **Analysis Method**: Customer profitability ranking and Bain Whale Curve construction.
- **Decision Implication**: Establish a 18% contract discount ceiling and require minimum order volume thresholds for tier qualification.

---

### Hypothesis 3 (H3): Promotional Demand Cannibalization
- **Hypothesis**: Over 30% of trade promotions yield negative net incremental ROI because they subsidize baseline customer purchases rather than attracting new incremental volume.
- **Why it might be true**: End of Season Sales (EOSS) run predictably every quarter, prompting regular customers to delay planned purchases until discount windows open.
- **Evidence Required**: Daily sales volume pre/post/during promotions, trade promo spend, baseline sales estimates, and vendor co-op funding.
- **KPI**: Net Incremental Promo ROI & Incremental Volume Lift (%).
- **Analysis Method**: Baseline demand decomposition and pre/post promotion event analysis.
- **Decision Implication**: Eliminate low-ROI clearance promotions and reallocate trade marketing spend to vendor-co-funded festive campaigns.

---

### Hypothesis 4 (H4): Tier 3 Logistics Cost Overrun
- **Hypothesis**: Rapid e-commerce expansion into Tier 3 cities has inflated last-mile fulfillment costs relative to average order values, creating loss-making regional transactions.
- **Why it might be true**: Third-party logistics (3PL) carriers charge premium courier rates for remote Tier 3 pincodes while Tier 3 basket sizes remain smaller.
- **Evidence Required**: Pincode-level shipping costs, order weight, average order value (AOV), and regional net profit.
- **KPI**: Fulfillment Cost % of Net Revenue & Regional Pocket Margin (%).
- **Analysis Method**: Regional unit economics decomposition and logistics cost per order analysis.
- **Decision Implication**: Implement minimum order value (AOV) thresholds for free delivery in Tier 3 pincodes.

---

### Hypothesis 5 (H5): Uncaptured Inelastic List Pricing Power
- **Hypothesis**: Premium SKUs in Home & Kitchen and FMCG categories are price inelastic (\(\|\epsilon\| < 1.0\)) and underpriced relative to key Indian retail competitors.
- **Why it might be true**: List prices were set based on historical cost-plus formulas rather than dynamic competitor benchmarking and willingness-to-pay.
- **Evidence Required**: Historical SKU price changes, sales volume, competitor price observations (Amazon IN, Reliance, D-Mart), and category COGS.
- **KPI**: Price Elasticity of Demand (\(\epsilon\)) & Competitor Price Index.
- **Analysis Method**: Log-Log OLS regression modeling and competitor price indexing.
- **Decision Implication**: Implement selective list price increases (+3% to +6%) on identified inelastic SKUs.

---

### Hypothesis 6 (H6): High E-Commerce Return Rate Margin Erosion
- **Hypothesis**: High return rates (~18%) in online Apparel channels generate uncompensated reverse logistics and repackaging costs that erase gross profit margins.
- **Why it might be true**: Customer "sizing uncertainty" leads to multi-item bracket ordering where items are tried and returned.
- **Evidence Required**: Channel return flags, return processing costs, category return rates, and net margin per returned item.
- **KPI**: Return Rate (%) & Net Margin After Return Costs.
- **Analysis Method**: Category return cost impact analysis and basket-level profitability calculation.
- **Decision Implication**: Adjust online apparel sizing charts and apply restocking fees on multi-size bracket returns.

---

### Hypothesis 7 (H7): Product Mix Shift Dilution
- **Hypothesis**: Aggregate gross margin compression is driven by a structural volume shift toward lower-margin Consumer Electronics away from higher-margin Apparel.
- **Why it might be true**: Electronic devices experienced strong post-pandemic consumer demand growth, inflating their share of total revenue mix.
- **Evidence Required**: Category revenue shares, category gross margin %, and historical mix evolution.
- **KPI**: Category Volume Share & Mix-Adjusted Gross Margin (%).
- **Analysis Method**: Shift-share mix decomposition analysis.
- **Decision Implication**: Adjust marketing channel spend to drive traffic toward higher-margin private-label fashion.

---

### Hypothesis 8 (H8): E-Commerce Marketplace Commission Drag
- **Hypothesis**: Selling through external e-commerce marketplaces (Amazon/Flipkart) yields significantly lower pocket margin than Direct App & Web channels due to marketplace commission fees.
- **Why it might be true**: External marketplaces charge 8–12% take rates plus fulfillment-by-marketplace fees.
- **Evidence Required**: Net revenue, marketplace commissions, direct fulfillment expenses, and pocket profit by channel.
- **KPI**: Channel Pocket Margin (%) & Net Channel Contribution (INR).
- **Analysis Method**: Cross-channel unit economics comparative analysis.
- **Decision Implication**: Shift digital ad spend toward driving direct web/app traffic and exclusive direct-to-consumer SKUs.

---

### Hypothesis 9 (H9): Under-Utilized Manufacturer Vendor Co-Op Funding
- **Hypothesis**: Over 25% of eligible vendor co-op promotional rebates are unclaimed due to manual tracking gaps, increasing net trade spend.
- **Why it might be true**: Co-op claim documentation requires proof of promotion placement that store managers fail to upload systematically.
- **Evidence Required**: Vendor co-op contractual rebate rates, promo spend logs, and actual co-op claims received.
- **KPI**: Co-op Capture Rate (%) & Net Vendor Co-Op Funding (INR).
- **Analysis Method**: Promotional financial audit and vendor claim reconciliation.
- **Decision Implication**: Automate co-op rebate tracking within promotion creation workflows.

---

### Hypothesis 10 (H10): Low Average Order Value (AOV) Transaction Loss
- **Hypothesis**: E-commerce transactions with AOV under ₹499 generate negative net pocket profit due to fixed pick, pack, and shipping expenses.
- **Why it might be true**: Fulfillment costs contain fixed per-order components regardless of transaction value.
- **Evidence Required**: Basket transaction value, item count, fixed order fulfillment cost, and pocket profit per order.
- **KPI**: AOV & Pocket Margin by AOV Bracket.
- **Analysis Method**: Order-value tier profitability segmentation.
- **Decision Implication**: Introduce minimum basket thresholds and cross-sell add-on prompts at checkout.

---

### Hypothesis 11 (H11): Store Footfall & Fixed Overhead Mismatch
- **Hypothesis**: Physical stores in Tier 3 locations suffer low sales density, failing to cover store fixed occupancy costs.
- **Why it might be true**: Retail real estate expansion in Tier 3 outpaced local store traffic growth.
- **Evidence Required**: Store square footage, store fixed rent, footfall counts, sales revenue, and store-level operating margin.
- **KPI**: Sales per Square Foot & Store Operating Margin (%).
- **Analysis Method**: Store operating leverage and sales density benchmark analysis.
- **Decision Implication**: Evaluate store downsizing or renegotiation of fixed rent to revenue-share lease structures.

---

### Hypothesis 12 (H12): Unoptimized Price Endings & Threshold Psychology
- **Hypothesis**: Non-standard retail price points (e.g. ₹1,042 vs ₹999) reduce conversion rates without capturing proportional margin.
- **Why it might be true**: Price points missing standard Indian retail psychological thresholds (.99 or .00) suffer conversion friction.
- **Evidence Required**: SKU price points, conversion rate by price ending, and demand volume.
- **KPI**: Conversion Rate (%) & Gross Margin per Impression.
- **Analysis Method**: Price ending threshold analysis.
- **Decision Implication**: Standardize list prices to charm pricing endings across all product lines.
