"""
profit_bridge.py
Executes Step 2: Price-Volume-Mix (PVM) & Cost Variance Bridge.
Quantifies the exact financial contribution of Volume Growth, Realized Price Leakage,
Variable Cost Inflation, and Mix Shifts to the net gross profit variance between 2024 and 2025.
"""

import os
import pandas as pd
import numpy as np

def calculate_profit_bridge(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Category-level Y1 (2024) vs Y2 (2025) metrics
    cat_summary = df.groupby(["year", "category"]).agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        variable_cost=("variable_cost", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    p2024 = cat_summary[cat_summary["year"] == 2024].set_index("category")
    p2025 = cat_summary[cat_summary["year"] == 2025].set_index("category")

    categories = p2024.index.intersection(p2025.index)

    bridge_results = []
    
    total_y1_profit = p2024["gross_profit"].sum()
    total_y2_profit = p2025["gross_profit"].sum()
    total_profit_delta = total_y2_profit - total_y1_profit

    y1_total_units = p2024["units"].sum()
    y2_total_units = p2025["units"].sum()
    overall_volume_growth_ratio = y2_total_units / y1_total_units

    volume_effect_total = 0.0
    price_effect_total = 0.0
    cost_effect_total = 0.0
    mix_effect_total = 0.0

    for cat in categories:
        u1 = p2024.loc[cat, "units"]
        u2 = p2025.loc[cat, "units"]
        r1 = p2024.loc[cat, "revenue"]
        r2 = p2025.loc[cat, "revenue"]
        c1 = p2024.loc[cat, "variable_cost"]
        c2 = p2025.loc[cat, "variable_cost"]

        p1 = r1 / u1  # Realized price Y1
        p2 = r2 / u2  # Realized price Y2
        vc1 = c1 / u1 # Unit variable cost Y1
        vc2 = c2 / u2 # Unit variable cost Y2
        m1 = (r1 - c1) / u1 # Unit margin Y1

        # Standard PVM Decomposition Formulas
        # 1. Volume Effect = (Total Volume Growth Ratio - 1) * Y1 Category Profit
        vol_effect = (overall_volume_growth_ratio - 1.0) * (r1 - c1)

        # 2. Mix Effect = (Actual Category Volume - Expected Category Volume under baseline mix) * Y1 Unit Margin
        expected_units = u1 * overall_volume_growth_ratio
        mix_effect = (u2 - expected_units) * m1

        # 3. Price Effect = u2 * (Realized Price Y2 - Realized Price Y1)
        price_effect = u2 * (p2 - p1)

        # 4. Cost Effect = u2 * (Unit Variable Cost Y1 - Unit Variable Cost Y2)
        cost_effect = u2 * (vc1 - vc2)

        volume_effect_total += vol_effect
        mix_effect_total += mix_effect
        price_effect_total += price_effect
        cost_effect_total += cost_effect

        bridge_results.append({
            "category": cat,
            "y1_units": u1,
            "y2_units": u2,
            "y1_gross_profit": round(r1 - c1, 2),
            "y2_gross_profit": round(r2 - c2, 2),
            "volume_effect_inr": round(vol_effect, 2),
            "mix_effect_inr": round(mix_effect, 2),
            "price_effect_inr": round(price_effect, 2),
            "cost_effect_inr": round(cost_effect, 2)
        })

    bridge_summary = {
        "2024_total_gross_profit": round(total_y1_profit, 2),
        "2025_total_gross_profit": round(total_y2_profit, 2),
        "net_profit_change": round(total_profit_delta, 2),
        "volume_effect_inr": round(volume_effect_total, 2),
        "mix_effect_inr": round(mix_effect_total, 2),
        "price_effect_inr": round(price_effect_total, 2),
        "cost_effect_inr": round(cost_effect_total, 2)
    }

    return bridge_summary, pd.DataFrame(bridge_results)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    summary, df_details = calculate_profit_bridge(processed_dir)

    print("=== PROFIT BRIDGE VARIANCE DECOMPOSITION (2024 -> 2025) ===")
    for k, v in summary.items():
        print(f"  {k}: INR {v:,.2f}" if isinstance(v, float) else f"  {k}: {v}")
    
    print("\n--- CATEGORY-LEVEL BRIDGE BREAKDOWN ---")
    print(df_details.to_string())

if __name__ == "__main__":
    main()
