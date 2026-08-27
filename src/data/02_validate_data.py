"""
02_validate_data.py
Performs automated data quality validation checks on raw CSV datasets in data/raw/.
Audits missing values, duplicates, category inconsistencies, negative revenues, outliers,
and mathematical reconciliation checks (units * selling_price == revenue, revenue - variable_cost == gross_profit).
Outputs DATA_QUALITY_REPORT.md.
"""

import os
import json
import pandas as pd
import numpy as np

def audit_raw_data(raw_dir):
    tx_path = os.path.join(raw_dir, "transactions_raw.csv")
    df_tx = pd.read_csv(tx_path)

    total_rows = len(df_tx)
    
    # 1. Missing Values Audit
    missing_summary = df_tx.isnull().sum().to_dict()
    missing_pct = {k: round((v / total_rows) * 100, 2) for k, v in missing_summary.items() if v > 0}

    # 2. Duplicates Audit
    exact_duplicates = int(df_tx.duplicated().sum())
    key_duplicates = int(df_tx.duplicated(subset=["transaction_id"]).sum())

    # 3. Category Inconsistency Audit
    unique_cats = df_tx["category"].dropna().unique().tolist()
    clean_unique_cats = set([c.strip().lower().replace("_", " ") for c in unique_cats])

    # 4. Invalid / Negative Revenue & Price Audit
    neg_revenue_count = int((df_tx["revenue"] < 0).sum())
    invalid_price_count = int(((df_tx["selling_price"] <= 0) | (df_tx["list_price"] <= 0)).sum())

    # 5. Outlier Detection (Units > 500)
    outliers_units_count = int((df_tx["units"] > 500).sum())

    # 6. Math Reconciliation Audit
    # Revenue = units * selling_price
    calc_revenue = (df_tx["units"] * df_tx["selling_price"]).round(2)
    rev_diff = (df_tx["revenue"] - calc_revenue).abs()
    rev_reconcile_failures = int((rev_diff > 0.05).sum())

    # Gross Profit = revenue - variable_cost
    calc_gp = (df_tx["revenue"] - df_tx["variable_cost"]).round(2)
    gp_diff = (df_tx["gross_profit"] - calc_gp).abs()
    gp_reconcile_failures = int((gp_diff > 0.05).sum())

    audit_results = {
        "raw_record_count": total_rows,
        "missing_values": missing_pct,
        "exact_duplicates": exact_duplicates,
        "key_duplicates": key_duplicates,
        "category_variants_found": unique_cats,
        "standardized_categories_count": len(clean_unique_cats),
        "negative_revenue_count": neg_revenue_count,
        "invalid_price_count": invalid_price_count,
        "outlier_unit_count": outliers_units_count,
        "revenue_reconciliation_failures": rev_reconcile_failures,
        "gross_profit_reconciliation_failures": gp_reconcile_failures
    }

    return audit_results, df_tx

def generate_markdown_report(audit_results, repo_root):
    report_content = f"""# Data Quality Audit Report

## 1. Executive Data Quality Overview
- **Raw Transaction Records Audited**: `{audit_results['raw_record_count']:,}`
- **Exact Duplicate Rows**: `{audit_results['exact_duplicates']:,}`
- **Key (Transaction ID) Duplicates**: `{audit_results['key_duplicates']:,}`
- **Negative Revenue Anomalies**: `{audit_results['negative_revenue_count']:,}`
- **Invalid / Zero Price Records**: `{audit_results['invalid_price_count']:,}`
- **Unit Quantity Outliers (>500 units)**: `{audit_results['outlier_unit_count']:,}`
- **Revenue Reconciliation Failures**: `{audit_results['revenue_reconciliation_failures']:,}`
- **Gross Profit Reconciliation Failures**: `{audit_results['gross_profit_reconciliation_failures']:,}`

---

## 2. Missing Value Analysis
| Column Name | Missing Count / Pct | Data Quality Status |
|---|---|---|
"""
    for col, pct in audit_results["missing_values"].items():
        report_content += f"| `{col}` | {pct}% | Action Required (Impute / Flag) |\n"
    if not audit_results["missing_values"]:
        report_content += "| *None* | 0.0% | Clean |\n"

    report_content += f"""
---

## 3. Category Inconsistency Audit
- **Raw Distinct Category Values Found**: `{audit_results['category_variants_found']}`
- **Normalized Standard Category Count**: `{audit_results['standardized_categories_count']}` (Consumer Electronics, Apparel & Fashion, Home & Kitchen, FMCG & Personal Care, Footwear, Beauty & Cosmetics)
- **Issue**: Presence of lowercasing (`consumer_electronics`), trailing whitespace (`Apparel & Fashion  `), and underscores (`home_&_kitchen`).

---

## 4. Mathematical Reconciliation Audit
1. **Revenue Reconciliation Check (`revenue == units * selling_price`)**:
   - Status: `{audit_results['revenue_reconciliation_failures']} failures`
   - *Rule*: Revenue must equal quantity multiplied by realized unit selling price.
2. **Gross Profit Reconciliation Check (`gross_profit == revenue - variable_cost`)**:
   - Status: `{audit_results['gross_profit_reconciliation_failures']} failures`
   - *Rule*: Gross profit must equal revenue minus variable costs.

---

## 5. Documented Treatment & Cleaning Decisions
- **Duplicate Rows**: Remove duplicate transaction records, retaining the first valid occurrence.
- **Category Standardization**: Trim whitespace, apply Title Case, and map legacy string variations to canonical category names.
- **Missing Customer Segments**: Impute missing `customer_segment` as `"Unknown / Unclassified"` to preserve transaction revenue without loss of observations.
- **Missing Variable Costs**: Impute missing `variable_cost` using category-level median variable cost ratios to ensure 100% gross profit coverage.
- **Negative Revenue Anomalies**: Correct negative sign errors caused by manual keying inputs (`revenue = abs(revenue)`).
- **Extreme Unit Outliers**: Flag extreme unit outliers (>500 units) with an `is_outlier` indicator attribute rather than silently deleting records.
"""
    
    report_path = os.path.join(repo_root, "DATA_QUALITY_REPORT.md")
    with open(report_path, "w") as f:
        f.write(report_content)
    
    print(f"DATA_QUALITY_REPORT.md successfully written to: {report_path}")

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    repo_root = os.path.join(os.path.dirname(__file__), "..", "..")

    print("Executing Data Quality Audit on Raw Datasets...")
    audit_results, _ = audit_raw_data(raw_dir)
    generate_markdown_report(audit_results, repo_root)

if __name__ == "__main__":
    main()
