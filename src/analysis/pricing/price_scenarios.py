"""
price_scenarios.py
Price-Volume-Profit Scenario Engine.
Simulates +5%, +10%, -5%, and -10% list price adjustments per category using estimated price elasticities.
Evaluates expected unit volume, revenue, variable cost, gross profit, and gross margin % for each scenario.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure parent directory is in sys.path for script execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from src.analysis.pricing.elasticity import estimate_category_elasticities

def run_price_scenarios(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))
    df_eps, _ = estimate_category_elasticities(processed_dir)
    eps_dict = df_eps.set_index("category")["elasticity_beta"].to_dict()

    cat_baseline = df.groupby("category").agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        variable_cost=("variable_cost", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    scenarios = [0.05, 0.10, -0.05, -0.10]
    scenario_rows = []

    for _, row in cat_baseline.iterrows():
        cat = row["category"]
        base_units = row["units"]
        base_rev = row["revenue"]
        base_vc = row["variable_cost"]
        base_gp = row["gross_profit"]
        base_price = base_rev / base_units
        unit_vc = base_vc / base_units

        beta = eps_dict.get(cat, -0.80)

        # Baseline Scenario
        scenario_rows.append({
            "category": cat,
            "scenario": "Baseline (0%)",
            "price_change_pct": 0.0,
            "estimated_elasticity": beta,
            "unit_price_inr": round(base_price, 2),
            "expected_units": base_units,
            "expected_revenue_inr": round(base_rev, 2),
            "expected_variable_cost_inr": round(base_vc, 2),
            "expected_gross_profit_inr": round(base_gp, 2),
            "gross_margin_pct": round((base_gp / base_rev) * 100, 2),
            "profit_delta_inr": 0.0
        })

        # Test scenarios (+5%, +10%, -5%, -10%)
        for s in scenarios:
            price_mult = 1.0 + s
            new_price = base_price * price_mult
            
            # Volume change based on elasticity formula: % Delta Q = beta * % Delta P
            delta_q_pct = beta * s
            new_units = max(10, int(round(base_units * (1.0 + delta_q_pct))))

            new_rev = new_units * new_price
            new_vc = new_units * unit_vc
            new_gp = new_rev - new_vc
            margin_pct = (new_gp / new_rev) * 100 if new_rev > 0 else 0.0
            profit_delta = new_gp - base_gp

            scenario_rows.append({
                "category": cat,
                "scenario": f"{'+' if s > 0 else ''}{int(s*100)}% Price Change",
                "price_change_pct": round(s * 100, 1),
                "estimated_elasticity": beta,
                "unit_price_inr": round(new_price, 2),
                "expected_units": new_units,
                "expected_revenue_inr": round(new_rev, 2),
                "expected_variable_cost_inr": round(new_vc, 2),
                "expected_gross_profit_inr": round(new_gp, 2),
                "gross_margin_pct": round(margin_pct, 2),
                "profit_delta_inr": round(profit_delta, 2)
            })

    return pd.DataFrame(scenario_rows)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_scen = run_price_scenarios(processed_dir)

    print("=== PRICE-VOLUME-PROFIT SCENARIOS SUMMARY ===")
    sample_cat = "Home & Kitchen"
    print(f"\nScenario Breakdown for Category: {sample_cat}")
    print(df_scen[df_scen["category"] == sample_cat][["scenario", "unit_price_inr", "expected_units", "expected_revenue_inr", "expected_gross_profit_inr", "gross_margin_pct", "profit_delta_inr"]].to_string())

if __name__ == "__main__":
    main()
