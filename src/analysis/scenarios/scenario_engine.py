"""
scenario_engine.py
Executes Strategic Scenario Engine for OmniRetail India.
Evaluates 7 Strategic Alternatives (Scenarios A through G) and calculates Revenue, Units,
Gross Profit, Contribution Margin, Incremental Profit, Customer Impact, and Risk Indicators.
Clearly labels outputs as Observed, Modelled, or Assumed.
"""

import os
import pandas as pd
import numpy as np

def run_strategic_scenario_engine(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Baseline Observed Aggregates
    base_units = int(df["units"].sum())
    base_rev = float(df["revenue"].sum())
    base_vc = float(df["variable_cost"].sum())
    base_gp = float(df["gross_profit"].sum())
    base_margin = round((base_gp / base_rev) * 100, 2)

    # Elasticity Dictionary (Assumed / Modelled from Phase 5)
    eps_dict = {
        "Consumer Electronics": -0.103,
        "Apparel & Fashion": -0.099,
        "Footwear": -0.129,
        "Beauty & Cosmetics": -0.134,
        "FMCG & Personal Care": -0.084,
        "Home & Kitchen": -0.062
    }

    scenarios = []

    # -------------------------------------------------------------------------
    # Scenario A: Maintain Current Pricing (Baseline)
    # -------------------------------------------------------------------------
    scenarios.append({
        "scenario_code": "Scenario A",
        "scenario_name": "Maintain Current Pricing (Baseline)",
        "units": base_units,
        "revenue_inr": round(base_rev, 2),
        "variable_cost_inr": round(base_vc, 2),
        "gross_profit_inr": round(base_gp, 2),
        "gross_margin_pct": base_margin,
        "incremental_profit_inr": 0.0,
        "margin_expansion_bps": 0,
        "customer_impact": "Status quo. Continued baseline attrition.",
        "risk_indicator": "Low Operational Risk / High Margin Risk",
        "data_status": "Observed Data"
    })

    # -------------------------------------------------------------------------
    # Scenario B: Increase Prices Selectively (+5% on Home & Kitchen & FMCG)
    # -------------------------------------------------------------------------
    hk_fmcg_mask = df["category"].isin(["Home & Kitchen", "FMCG & Personal Care"])
    hk_fmcg_units = df.loc[hk_fmcg_mask, "units"].sum()
    hk_fmcg_rev = df.loc[hk_fmcg_mask, "revenue"].sum()
    hk_fmcg_vc = df.loc[hk_fmcg_mask, "variable_cost"].sum()
    hk_fmcg_price = hk_fmcg_rev / hk_fmcg_units
    unit_vc = hk_fmcg_vc / hk_fmcg_units

    # Price hike +5%, elasticity ~ -0.07 -> volume delta -0.35%
    b_new_price = hk_fmcg_price * 1.05
    b_new_units = int(hk_fmcg_units * (1.0 - 0.0035))
    b_new_rev = b_new_units * b_new_price
    b_new_vc = b_new_units * unit_vc
    b_hk_gp_delta = (b_new_rev - b_new_vc) - (hk_fmcg_rev - hk_fmcg_vc)

    scenarios.append({
        "scenario_code": "Scenario B",
        "scenario_name": "Increase Prices Selectively (+5% Home & FMCG)",
        "units": base_units - int(hk_fmcg_units * 0.0035),
        "revenue_inr": round(base_rev + (b_new_rev - hk_fmcg_rev), 2),
        "variable_cost_inr": round(base_vc + (b_new_vc - hk_fmcg_vc), 2),
        "gross_profit_inr": round(base_gp + b_hk_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + b_hk_gp_delta) / (base_rev + (b_new_rev - hk_fmcg_rev))) * 100, 2),
        "incremental_profit_inr": round(b_hk_gp_delta, 2),
        "margin_expansion_bps": round(((b_hk_gp_delta) / base_rev) * 10000, 0),
        "customer_impact": "Minimal volume loss (<0.4%) due to high pricing power.",
        "risk_indicator": "Low Risk",
        "data_status": "Modelled Estimate"
    })

    # -------------------------------------------------------------------------
    # Scenario C: Reduce Discounts (Enforce 18% B2B Contract Ceiling)
    # -------------------------------------------------------------------------
    b2b_mask = df["customer_segment"] == "B2B Enterprise"
    b2b_df = df[b2b_mask]
    excess_disc = b2b_df.apply(lambda r: max(0, r["revenue"] * (r["contract_discount_pct"] - 0.18)), axis=1).sum()
    c_gp_delta = excess_disc * 0.90  # 90% account retention assumed

    scenarios.append({
        "scenario_code": "Scenario C",
        "scenario_name": "Reduce Discounts (18% B2B Contract Ceiling)",
        "units": base_units - int(df.loc[b2b_mask, "units"].sum() * 0.02),
        "revenue_inr": round(base_rev + c_gp_delta, 2),
        "variable_cost_inr": round(base_vc, 2),
        "gross_profit_inr": round(base_gp + c_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + c_gp_delta) / (base_rev + c_gp_delta)) * 100, 2),
        "incremental_profit_inr": round(c_gp_delta, 2),
        "margin_expansion_bps": round((c_gp_delta / base_rev) * 10000, 0),
        "customer_impact": "B2B accounts face discount caps; ~10% pushback risk.",
        "risk_indicator": "Medium Risk",
        "data_status": "Modelled Estimate"
    })

    # -------------------------------------------------------------------------
    # Scenario D: Increase Discounts Selectively (+5% Festive Retail Push)
    # -------------------------------------------------------------------------
    ret_gold_mask = df["customer_segment"].isin(["Retail Gold", "Retail Silver"])
    ret_gold_rev = df.loc[ret_gold_mask, "revenue"].sum()
    d_gp_delta = -1 * (ret_gold_rev * 0.05) + (ret_gold_rev * 0.08)  # +8% volume lift offsets 5% discount

    scenarios.append({
        "scenario_code": "Scenario D",
        "scenario_name": "Increase Discounts Selectively (Retail Festive Push)",
        "units": base_units + int(df.loc[ret_gold_mask, "units"].sum() * 0.08),
        "revenue_inr": round(base_rev + (ret_gold_rev * 0.03), 2),
        "variable_cost_inr": round(base_vc + (ret_gold_rev * 0.04), 2),
        "gross_profit_inr": round(base_gp + d_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + d_gp_delta) / (base_rev + (ret_gold_rev * 0.03))) * 100, 2),
        "incremental_profit_inr": round(d_gp_delta, 2),
        "margin_expansion_bps": round((d_gp_delta / base_rev) * 10000, 0),
        "customer_impact": "Positive retail sentiment; drives short-term volume.",
        "risk_indicator": "Low-Medium Risk",
        "data_status": "Modelled Estimate"
    })

    # -------------------------------------------------------------------------
    # Scenario E: Change Product Mix (+10% Volume Shift to Apparel & Beauty)
    # -------------------------------------------------------------------------
    app_beauty_mask = df["category"].isin(["Apparel & Fashion", "Beauty & Cosmetics"])
    app_beauty_gp = df.loc[app_beauty_mask, "gross_profit"].sum()
    e_gp_delta = app_beauty_gp * 0.10  # 10% volume expansion

    scenarios.append({
        "scenario_code": "Scenario E",
        "scenario_name": "Change Product Mix (+10% Apparel & Beauty Shift)",
        "units": base_units + int(df.loc[app_beauty_mask, "units"].sum() * 0.10),
        "revenue_inr": round(base_rev + (df.loc[app_beauty_mask, "revenue"].sum() * 0.10), 2),
        "variable_cost_inr": round(base_vc + (df.loc[app_beauty_mask, "variable_cost"].sum() * 0.10), 2),
        "gross_profit_inr": round(base_gp + e_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + e_gp_delta) / (base_rev + (df.loc[app_beauty_mask, "revenue"].sum() * 0.10))) * 100, 2),
        "incremental_profit_inr": round(e_gp_delta, 2),
        "margin_expansion_bps": round((e_gp_delta / base_rev) * 10000, 0),
        "customer_impact": "Increased retail engagement in high-margin fashion lines.",
        "risk_indicator": "Low Risk",
        "data_status": "Modelled Estimate"
    })

    # -------------------------------------------------------------------------
    # Scenario F: Change Promotion Strategy (Eliminate EOSS Clearance Sales)
    # -------------------------------------------------------------------------
    eoss_mask = df["promotion_type"] == "EOSS Clearance"
    eoss_disc = (df.loc[eoss_mask, "discount"] * df.loc[eoss_mask, "units"]).sum()
    f_gp_delta = eoss_disc * 0.70  # Save 70% of clearance markdown spend

    scenarios.append({
        "scenario_code": "Scenario F",
        "scenario_name": "Change Promotion Strategy (Eliminate EOSS Clearance)",
        "units": base_units - int(df.loc[eoss_mask, "units"].sum() * 0.15),
        "revenue_inr": round(base_rev + (f_gp_delta * 0.5), 2),
        "variable_cost_inr": round(base_vc, 2),
        "gross_profit_inr": round(base_gp + f_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + f_gp_delta) / (base_rev + (f_gp_delta * 0.5))) * 100, 2),
        "incremental_profit_inr": round(f_gp_delta, 2),
        "margin_expansion_bps": round((f_gp_delta / base_rev) * 10000, 0),
        "customer_impact": "Eliminates bargain-hunter clearance subsidization.",
        "risk_indicator": "Medium Risk",
        "data_status": "Modelled Estimate"
    })

    # -------------------------------------------------------------------------
    # Scenario G: Combination Strategy (Full Transformation = B + C + F)
    # -------------------------------------------------------------------------
    g_gp_delta = b_hk_gp_delta + c_gp_delta + f_gp_delta
    g_rev_delta = (b_new_rev - hk_fmcg_rev) + c_gp_delta + (f_gp_delta * 0.5)

    scenarios.append({
        "scenario_code": "Scenario G",
        "scenario_name": "Combination Strategy (Full Strategic Transformation)",
        "units": base_units - int(hk_fmcg_units * 0.0035) - int(df.loc[b2b_mask, "units"].sum() * 0.02) - int(df.loc[eoss_mask, "units"].sum() * 0.15),
        "revenue_inr": round(base_rev + g_rev_delta, 2),
        "variable_cost_inr": round(base_vc + (b_new_vc - hk_fmcg_vc), 2),
        "gross_profit_inr": round(base_gp + g_gp_delta, 2),
        "gross_margin_pct": round(((base_gp + g_gp_delta) / (base_rev + g_rev_delta)) * 100, 2),
        "incremental_profit_inr": round(g_gp_delta, 2),
        "margin_expansion_bps": round((g_gp_delta / base_rev) * 10000, 0),
        "customer_impact": "Optimized customer economics; B2B discount caps enforced.",
        "risk_indicator": "Managed Strategic Transformation Risk",
        "data_status": "Modelled Estimate"
    })

    return pd.DataFrame(scenarios)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_scen = run_strategic_scenario_engine(processed_dir)

    print("=== STRATEGIC ALTERNATIVE SCENARIO ENGINE OUTPUT ===")
    print(df_scen[["scenario_code", "scenario_name", "gross_profit_inr", "gross_margin_pct", "incremental_profit_inr", "margin_expansion_bps", "data_status"]].to_string())

if __name__ == "__main__":
    main()
