"""
sensitivity_analysis.py
Performs 3-Tier Sensitivity Analysis (Base Case, Upside Case, Downside Case)
on key uncertain assumptions: Elasticity responsiveness, B2B account retention, and freight cost inflation.
"""

import os
import pandas as pd
import numpy as np

def run_sensitivity_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    base_rev = float(df["revenue"].sum())
    base_gp = float(df["gross_profit"].sum())

    # Key Variable 1: B2B Enterprise Account Retention Rate under 18% Discount Cap
    # Base = 90%, Upside = 95%, Downside = 80%
    b2b_mask = df["customer_segment"] == "B2B Enterprise"
    b2b_df = df[b2b_mask]
    excess_disc = b2b_df.apply(lambda r: max(0, r["revenue"] * (r["contract_discount_pct"] - 0.18)), axis=1).sum()

    # Key Variable 2: Price Elasticity Responsiveness to +5% Price Hike in Home & FMCG
    # Base = -0.07 (Volume delta -0.35%), Upside = -0.04 (Volume delta -0.20%), Downside = -0.15 (Volume delta -0.75%)
    hk_fmcg_mask = df["category"].isin(["Home & Kitchen", "FMCG & Personal Care"])
    hk_fmcg_rev = df.loc[hk_fmcg_mask, "revenue"].sum()
    hk_fmcg_gp = df.loc[hk_fmcg_mask, "gross_profit"].sum()

    # Key Variable 3: Freight Logistics Cost Multiplier
    # Base = 1.00x, Upside = 0.95x (5% efficiency gain), Downside = 1.05x (5% cost inflation)
    tot_var_cost = float(df["variable_cost"].sum())

    sensitivities = []

    # 1. Base Case
    b2b_gain_base = excess_disc * 0.90
    hk_price_gain_base = (hk_fmcg_rev * 0.05) * (1.0 - 0.0035)
    freight_delta_base = 0.0
    tot_inc_profit_base = b2b_gain_base + hk_price_gain_base + freight_delta_base

    sensitivities.append({
        "case": "Base Case (Expected)",
        "b2b_retention_rate": "90.0%",
        "price_elasticity_assumed": "Standard (-0.07)",
        "freight_cost_multiplier": "1.00x",
        "b2b_profit_gain_inr": round(b2b_gain_base, 2),
        "price_hike_profit_gain_inr": round(hk_price_gain_base, 2),
        "freight_cost_impact_inr": round(freight_delta_base, 2),
        "total_incremental_profit_inr": round(tot_inc_profit_base, 2),
        "new_gross_margin_pct": round(((base_gp + tot_inc_profit_base) / (base_rev + hk_price_gain_base + b2b_gain_base)) * 100, 2),
        "data_status": "Modelled Estimate"
    })

    # 2. Upside Case (Optimistic)
    b2b_gain_up = excess_disc * 0.95
    hk_price_gain_up = (hk_fmcg_rev * 0.05) * (1.0 - 0.0020)
    freight_delta_up = tot_var_cost * 0.02  # 2% efficiency savings
    tot_inc_profit_up = b2b_gain_up + hk_price_gain_up + freight_delta_up

    sensitivities.append({
        "case": "Upside Case (Optimistic)",
        "b2b_retention_rate": "95.0%",
        "price_elasticity_assumed": "Low Sensitivity (-0.04)",
        "freight_cost_multiplier": "0.98x (-2% savings)",
        "b2b_profit_gain_inr": round(b2b_gain_up, 2),
        "price_hike_profit_gain_inr": round(hk_price_gain_up, 2),
        "freight_cost_impact_inr": round(freight_delta_up, 2),
        "total_incremental_profit_inr": round(tot_inc_profit_up, 2),
        "new_gross_margin_pct": round(((base_gp + tot_inc_profit_up) / (base_rev + hk_price_gain_up + b2b_gain_up)) * 100, 2),
        "data_status": "Modelled Estimate"
    })

    # 3. Downside Case (Pessimistic)
    b2b_gain_down = excess_disc * 0.80
    hk_price_gain_down = (hk_fmcg_rev * 0.05) * (1.0 - 0.0075)
    freight_delta_down = -1 * (tot_var_cost * 0.02)  # 2% cost inflation
    tot_inc_profit_down = b2b_gain_down + hk_price_gain_down + freight_delta_down

    sensitivities.append({
        "case": "Downside Case (Pessimistic)",
        "b2b_retention_rate": "80.0%",
        "price_elasticity_assumed": "High Sensitivity (-0.15)",
        "freight_cost_multiplier": "1.02x (+2% inflation)",
        "b2b_profit_gain_inr": round(b2b_gain_down, 2),
        "price_hike_profit_gain_inr": round(hk_price_gain_down, 2),
        "freight_cost_impact_inr": round(freight_delta_down, 2),
        "total_incremental_profit_inr": round(tot_inc_profit_down, 2),
        "new_gross_margin_pct": round(((base_gp + tot_inc_profit_down) / (base_rev + hk_price_gain_down + b2b_gain_down)) * 100, 2),
        "data_status": "Modelled Estimate"
    })

    return pd.DataFrame(sensitivities)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_sens = run_sensitivity_analysis(processed_dir)

    print("=== SENSITIVITY ANALYSIS (BASE / UPSIDE / DOWNSIDE CASES) ===")
    print(df_sens.to_string())

if __name__ == "__main__":
    main()
