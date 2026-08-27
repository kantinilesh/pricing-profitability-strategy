"""
promotion_roi.py
Calculates Net Incremental Revenue, Incremental Gross Margin, Gross Promo Spend,
Vendor Co-Op Offsets, and Net Incremental Promotion ROI.
Classifies promotions into Profitable (ROI > 1.0x), Break-Even (0.0x-1.0x), and Value-Destroying (ROI < 0.0x).
Performs 80/20 Pareto analysis on campaign incremental profit.
"""

import os
import pandas as pd
import numpy as np

def calculate_promotion_roi(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Baseline daily non-promoted volume & margin rate per category
    non_promo = df[df["promotion_type"] == "Baseline / None"]
    cat_baseline_units = non_promo.groupby("category")["units"].mean().to_dict()
    cat_baseline_margin_per_unit = (non_promo.groupby("category")["gross_profit"].sum() / non_promo.groupby("category")["units"].sum()).to_dict()

    roi_results = []
    promo_types = df["promotion_type"].unique()

    for ptype in promo_types:
        if ptype == "Baseline / None":
            continue

        p_df = df[df["promotion_type"] == ptype]
        
        actual_units = p_df["units"].sum()
        actual_revenue = p_df["revenue"].sum()
        actual_gross_profit = p_df["gross_profit"].sum()

        # Promo Discount Spend & Vendor Co-Op Rebate Recovery
        # Total list value = list_price * units
        list_val = (p_df["list_price"] * p_df["units"]).sum()
        gross_promo_spend = (p_df["discount"] * p_df["units"]).sum()
        vendor_coop_pct = p_df["vendor_coop_share_pct"].iloc[0]
        vendor_coop_rebate = gross_promo_spend * vendor_coop_pct
        net_trade_spend = max(1.0, gross_promo_spend - vendor_coop_rebate)

        # Baseline Margin Estimation (What would have been earned without promo)
        baseline_units_est = sum(cat_baseline_units.get(cat, 2.0) for cat in p_df["category"])
        baseline_margin_est = sum(cat_baseline_units.get(cat, 2.0) * cat_baseline_margin_per_unit.get(cat, 500.0) for cat in p_df["category"])

        incremental_revenue = actual_revenue - (baseline_units_est * (actual_revenue / actual_units))
        incremental_gross_profit = actual_gross_profit - baseline_margin_est

        # Net Incremental Promo ROI
        net_promo_roi = (incremental_gross_profit - net_trade_spend) / net_trade_spend

        if net_promo_roi > 1.0:
            classification = "Profitable (High Incremental ROI)"
        elif net_promo_roi >= 0.0:
            classification = "Break-Even (Marginal Return)"
        else:
            classification = "Value-Destroying (Negative ROI)"

        roi_results.append({
            "promotion_type": ptype,
            "actual_units": actual_units,
            "actual_net_revenue_inr": round(actual_revenue, 2),
            "actual_gross_profit_inr": round(actual_gross_profit, 2),
            "gross_promo_spend_inr": round(gross_promo_spend, 2),
            "vendor_coop_rebate_inr": round(vendor_coop_rebate, 2),
            "net_trade_spend_inr": round(net_trade_spend, 2),
            "estimated_incremental_gross_profit_inr": round(incremental_gross_profit, 2),
            "net_incremental_promo_roi": round(net_promo_roi, 2),
            "profitability_classification": classification
        })

    df_roi = pd.DataFrame(roi_results).sort_values(by="net_incremental_promo_roi", ascending=False)

    # 80/20 Pareto Analysis on Promotional Campaigns
    df_roi["cumulative_incremental_profit"] = df_roi["estimated_incremental_gross_profit_inr"].clip(lower=0).cumsum()
    tot_inc_profit = df_roi["estimated_incremental_gross_profit_inr"].clip(lower=0).sum()
    df_roi["cumulative_profit_pct"] = (df_roi["cumulative_incremental_profit"] / max(1.0, tot_inc_profit) * 100).round(2)

    return df_roi

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_roi = calculate_promotion_roi(processed_dir)

    print("=== PROMOTION ROI & PROFITABILITY CLASSIFICATION ===")
    print(df_roi.to_string())

if __name__ == "__main__":
    main()
