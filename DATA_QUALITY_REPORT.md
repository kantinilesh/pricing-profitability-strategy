# Data Quality Audit Report

## 1. Executive Data Quality Overview
- **Raw Transaction Records Audited**: `60,480`
- **Exact Duplicate Rows**: `478`
- **Key (Transaction ID) Duplicates**: `480`
- **Negative Revenue Anomalies**: `90`
- **Invalid / Zero Price Records**: `0`
- **Unit Quantity Outliers (>500 units)**: `18`
- **Revenue Reconciliation Failures**: `255`
- **Gross Profit Reconciliation Failures**: `86`

---

## 2. Missing Value Analysis
| Column Name | Missing Count / Pct | Data Quality Status |
|---|---|---|
| `variable_cost` | 0.88% | Action Required (Impute / Flag) |
| `customer_segment` | 1.17% | Action Required (Impute / Flag) |

---

## 3. Category Inconsistency Audit
- **Raw Distinct Category Values Found**: `['Consumer Electronics', 'Apparel & Fashion', 'Footwear', 'Beauty & Cosmetics', 'FMCG & Personal Care', 'Home & Kitchen', 'consumer_electronics', 'Apparel & Fashion  ', 'home_&_kitchen']`
- **Normalized Standard Category Count**: `6` (Consumer Electronics, Apparel & Fashion, Home & Kitchen, FMCG & Personal Care, Footwear, Beauty & Cosmetics)
- **Issue**: Presence of lowercasing (`consumer_electronics`), trailing whitespace (`Apparel & Fashion  `), and underscores (`home_&_kitchen`).

---

## 4. Mathematical Reconciliation Audit
1. **Revenue Reconciliation Check (`revenue == units * selling_price`)**:
   - Status: `255 failures`
   - *Rule*: Revenue must equal quantity multiplied by realized unit selling price.
2. **Gross Profit Reconciliation Check (`gross_profit == revenue - variable_cost`)**:
   - Status: `86 failures`
   - *Rule*: Gross profit must equal revenue minus variable costs.

---

## 5. Documented Treatment & Cleaning Decisions
- **Duplicate Rows**: Remove duplicate transaction records, retaining the first valid occurrence.
- **Category Standardization**: Trim whitespace, apply Title Case, and map legacy string variations to canonical category names.
- **Missing Customer Segments**: Impute missing `customer_segment` as `"Unknown / Unclassified"` to preserve transaction revenue without loss of observations.
- **Missing Variable Costs**: Impute missing `variable_cost` using category-level median variable cost ratios to ensure 100% gross profit coverage.
- **Negative Revenue Anomalies**: Correct negative sign errors caused by manual keying inputs (`revenue = abs(revenue)`).
- **Extreme Unit Outliers**: Flag extreme unit outliers (>500 units) with an `is_outlier` indicator attribute rather than silently deleting records.
