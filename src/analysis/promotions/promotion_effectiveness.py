"""
promotion_effectiveness.py
Evaluates promotional volume lift and demand responsiveness across promotion types and product categories.
Compares promoted vs matched non-promoted baseline control periods.
"""

import os
import pandas as pd
import numpy as np

def analyze_promotion_effectiveness(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Baseline daily non-promoted volume rate per category
    non_promo = df[df["promotion_type"] == "Baseline / None"]
    baseline_velocity = non_promo.groupby("category")["units"].mean().to_dict()

    promo_effects = []
    promo_types = df["promotion_type"].unique()

    for ptype in promo_types:
        p_df = df[df["promotion_type"] == ptype]
        if len(p_df) == 0:
            continue

        total_tx = len(p_df)
        total_units = p_df["units"].sum()
        total_revenue = p_df["revenue"].sum()
        total_gross_profit = p_df["gross_profit"].sum()
        avg_discount = p_df["discount_pct"].mean()

        # Estimated baseline volume for transactions if no promotion had run
        baseline_units_est = sum(baseline_velocity.get(cat, 2.0) for cat in p_df["category"])
        incremental_units = total_units - baseline_units_est
        volume_lift_pct = (incremental_units / max(1, baseline_units_est)) * 100

        promo_effects.append({
            "promotion_type": ptype,
            "transaction_count": total_tx,
            "units_sold": total_units,
            "estimated_baseline_units": round(baseline_units_est, 0),
            "estimated_incremental_units": round(incremental_units, 0),
            "volume_lift_pct": round(volume_lift_pct, 2),
            "net_revenue_inr": round(total_revenue, 2),
            "gross_profit_inr": round(total_gross_profit, 2),
            "avg_discount_pct": round(avg_discount, 2)
        })

    return pd.DataFrame(promo_effects).sort_values(by="volume_lift_pct", ascending=False)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_eff = analyze_promotion_effectiveness(processed_dir)

    print("=== PROMOTION VOLUME LIFT & EFFECTIVENESS SUMMARY ===")
    print(df_eff.to_string())

if __name__ == "__main__":
    main()
