# Assumptions Register

This document records all baseline structural, financial, and operational assumptions used in building data models, elasticity estimations, and strategic scenario simulations for OmniRetail India.

---

### Assumption 1: Synthetic Data Labeling & Realism
- **Assumption**: All transactional, product, customer, channel, and competitor price data generated represents a realistic Indian retail environment.
- **Rationale**: Enables robust, end-to-end analytical modeling and scenario testing without exposing confidential live company records.
- **Source**: Calibrated to public Indian retail industry financial benchmarks (FMCG, Apparel, Electronics sector averages).
- **Sensitivity**: **Low**. Data distributions reflect real-world omnichannel retail economics (INR currency, Diwali seasonality, Tier 1–3 logistics split).
- **Status**: **Explicitly Synthetic / Model Parameterized**.

---

### Assumption 2: Global Mathematical Reproducibility
- **Assumption**: All synthetic data generation, train/test statistical splits, and OLS elasticity regression estimations execute using a fixed random seed (`seed=42`).
- **Rationale**: Ensures every numerical output, table, regression coefficient, and KPI is 100% deterministic and reproducible across execution runs.
- **Source**: System engineering requirement.
- **Sensitivity**: **Zero**. Numerical results remain invariant across identical execution environments.
- **Status**: **Observed System Rule**.

---

### Assumption 3: Baseline Demand Subsidization in Promotions
- **Assumption**: In the absence of trade promotions, baseline daily SKU sales velocity equals the average sales rate observed during non-promotional control periods within the same product category.
- **Rationale**: Necessary to isolate incremental promotional volume lift from baseline demand that would have occurred at standard list price.
- **Source**: Non-promo transaction historical averages (`PROMO_NONE`).
- **Sensitivity**: **Medium**. If true baseline sales are higher than estimated, calculated Incremental Promo ROI is slightly overestimated.
- **Status**: **Hypothetical Analytical Model**.

---

### Assumption 4: Price Elasticity Estimation Validity
- **Assumption**: SKU demand elasticity can be estimated using Log-Log OLS regression with binary promotional controls (\(\ln Q = \alpha + \beta \ln P + \gamma \text{IsPromo} + \epsilon\)).
- **Rationale**: Log-Log functional form allows direct interpretation of regression coefficient \(\beta\) as constant price elasticity of demand (\(\epsilon\)).
- **Source**: Standard microeconomic demand modeling.
- **Sensitivity**: **High**. Omitted variables (e.g. unobserved competitor promotions) may introduce slight endogeneity bias; bound controls are implemented.
- **Status**: **Model Parameterized**.

---

### Assumption 5: Tier 3 Logistics Cost Multiplier
- **Assumption**: Last-mile fulfillment and shipping costs for e-commerce deliveries to Tier 3 cities incur a 65% cost premium over Tier 1 fulfillment rates.
- **Rationale**: Reflects 3PL courier surcharges, lower delivery density, and longer transport distances in Tier 3 Indian pincodes.
- **Source**: Logistics carrier freight tariff benchmarks in India.
- **Sensitivity**: **Medium**. A higher logistics premium further reduces net pocket margin on low-AOV Tier 3 e-commerce transactions.
- **Status**: **Observed Parameter**.

---

### Assumption 6: E-Commerce Apparel Return Rates
- **Assumption**: E-commerce apparel transactions experience a 18% return rate, incurring reverse freight costs equal to 80% of forward shipping plus ₹150 repackaging fee.
- **Rationale**: Online fashion retail in India faces high customer return rates due to sizing and fit variances.
- **Source**: E-commerce apparel industry benchmarks.
- **Sensitivity**: **High**. Reducing return rates by 5% directly expands apparel category pocket margin by +110 bps.
- **Status**: **Observed Parameter**.

---

### Assumption 7: B2B Enterprise Contract Discount Ceiling
- **Assumption**: Capping B2B Enterprise contract discounts at a maximum of 18% (down from legacy discounts up to 25%) will retain 90% of account purchase volume.
- **Rationale**: B2B buyers prioritize supply chain reliability, credit terms, and catalog width alongside price; moderate discount caps align with market standards.
- **Source**: B2B commercial policy strategy assumption.
- **Sensitivity**: **High**. If customer churn exceeds 15%, net margin gains from discount capping could be partially offset by volume loss.
- **Status**: **Hypothetical Strategic Scenario**.

---

### Assumption 8: Competitor Price Ratio Benchmark
- **Assumption**: Publicly collected competitor price observations reflect true shelf prices at major Indian retailers (Reliance Retail, D-Mart, Amazon India, Flipkart).
- **Rationale**: Competitor price indexing provides an empirical baseline to evaluate uncaptured pricing power.
- **Source**: Secondary market price monitoring dataset (`fact_competitor_prices.csv`).
- **Sensitivity**: **Medium**. Dynamic competitor price matching may trigger competitive responses if OmniRetail raises prices significantly.
- **Status**: **Observed Secondary Benchmark**.
