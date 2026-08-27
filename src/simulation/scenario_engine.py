"""
What-If Scenario & Strategy Engine.
Simulates managerial strategic interventions (Price Optimization, Promo Budget Reallocation, 
and Customer Discount Governance) to quantify top-line revenue and pocket margin EBITDA impact.
"""

import os
import pandas as pd
import numpy as np
from src.analytics.profitability_engine import ProfitabilityEngine
from src.analytics.pricing_elasticity import PricingElasticityEngine
from src.analytics.promo_analytics import PromotionAnalyticsEngine
from src.analytics.customer_analytics import CustomerAnalyticsEngine

class ScenarioEngine:
    def __init__(self, processed_dir):
        self.processed_dir = processed_dir
        self.prof_engine = ProfitabilityEngine(processed_dir)
        self.elas_engine = PricingElasticityEngine(processed_dir)
        self.promo_engine = PromotionAnalyticsEngine(processed_dir)
        self.cust_engine = CustomerAnalyticsEngine(processed_dir)

    def run_baseline(self):
        waterfall = self.prof_engine.compute_margin_waterfall()
        return {
            "baseline_gross_revenue": waterfall["gross_revenue"],
            "baseline_net_revenue": waterfall["net_revenue"],
            "baseline_pocket_profit": waterfall["pocket_profit"],
            "baseline_pocket_margin_pct": waterfall["pocket_margin_pct"]
        }

    def simulate_price_optimization(self):
        """
        Scenario 1: Adjust list prices on inelastic SKUs based on elasticity model & competitor benchmark.
        """
        df_opt = self.elas_engine.calculate_optimal_prices()
        baseline = self.run_baseline()

        total_net_rev_impact = 0.0
        total_profit_impact = 0.0

        for _, row in df_opt.iterrows():
            price_change_pct = row["recommended_price_change_pct"] / 100.0
            eps = row["estimated_elasticity"]
            curr_units = row["total_units_sold"]
            curr_net_rev = row["total_net_revenue_inr"]
            curr_cogs = row["total_cogs_inr"]

            if price_change_pct == 0:
                continue

            # Volume change based on price elasticity: % Delta Q = eps * % Delta P
            delta_qty_pct = max(-0.25, eps * price_change_pct)
            new_units = curr_units * (1.0 + delta_qty_pct)
            new_price = row["optimal_price_inr"]
            new_cogs_per_unit = curr_cogs / max(1, curr_units)

            # Estimated new net revenue and profit
            avg_disc_rate = row["avg_discount_waterfall_pct"] / 100.0
            new_net_price = new_price * (1.0 - avg_disc_rate)
            new_net_rev = new_units * new_net_price
            new_profit = new_net_rev - (new_units * new_cogs_per_unit)

            curr_profit = row["total_gross_margin_inr"]

            total_net_rev_impact += (new_net_rev - curr_net_rev)
            total_profit_impact += (new_profit - curr_profit)

        return {
            "scenario": "Price Optimization on Inelastic SKUs",
            "net_revenue_impact_inr": round(total_net_rev_impact, 2),
            "pocket_profit_impact_inr": round(total_profit_impact, 2),
            "margin_expansion_bps": round((total_profit_impact / baseline["baseline_net_revenue"]) * 10000, 1)
        }

    def simulate_promo_reallocation(self):
        """
        Scenario 2: Eliminate negative-ROI EOSS promotions and reallocate budget to vendor-funded festive promos.
        """
        baseline = self.run_baseline()
        df_fact = self.prof_engine.df_fact
        
        # Identify EOSS promo spend
        eoss_mask = df_fact["promo_id"] == "PROMO_EOSS"
        eoss_promo_spend = df_fact.loc[eoss_mask, "promo_discount_inr"].sum()
        eoss_net_rev = df_fact.loc[eoss_mask, "net_revenue_inr"].sum()

        # Assuming 60% of EOSS sales would happen at baseline price without 30% markdown
        saved_promo_spend = eoss_promo_spend * 0.70
        recovered_margin = eoss_net_rev * 0.12 # Recovered baseline price margin

        total_profit_impact = saved_promo_spend + recovered_margin

        return {
            "scenario": "Promotional Budget Reallocation & EOSS Rationalization",
            "net_revenue_impact_inr": round(saved_promo_spend * 0.5, 2),
            "pocket_profit_impact_inr": round(total_profit_impact, 2),
            "margin_expansion_bps": round((total_profit_impact / baseline["baseline_net_revenue"]) * 10000, 1)
        }

    def simulate_discount_governance(self):
        """
        Scenario 3: Cap B2B contract discounts at 18% & eliminate ad-hoc markdown leakage.
        """
        baseline = self.run_baseline()
        df_fact = self.prof_engine.df_fact

        # Adhoc markdown leakage recovery
        recovered_adhoc = df_fact["adhoc_discount_inr"].sum() * 0.85

        # B2B contract discount capping (excess over 18%)
        excess_contract_disc = df_fact[df_fact["customer_type"] == "B2B Enterprise"].apply(
            lambda r: max(0, r["gross_revenue_inr"] * (r["contract_discount_pct"] - 0.18)), axis=1
        ).sum()

        total_profit_impact = recovered_adhoc + excess_contract_disc

        return {
            "scenario": "Customer Discount Governance & Leakage Control",
            "net_revenue_impact_inr": round(total_profit_impact, 2),
            "pocket_profit_impact_inr": round(total_profit_impact, 2),
            "margin_expansion_bps": round((total_profit_impact / baseline["baseline_net_revenue"]) * 10000, 1)
        }

    def run_full_strategic_transformation(self):
        baseline = self.run_baseline()
        s1 = self.simulate_price_optimization()
        s2 = self.simulate_promo_reallocation()
        s3 = self.simulate_discount_governance()

        total_net_rev = baseline["baseline_net_revenue"] + s1["net_revenue_impact_inr"] + s2["net_revenue_impact_inr"] + s3["net_revenue_impact_inr"]
        total_profit = baseline["baseline_pocket_profit"] + s1["pocket_profit_impact_inr"] + s2["pocket_profit_impact_inr"] + s3["pocket_profit_impact_inr"]
        new_pocket_margin_pct = round((total_profit / total_net_rev) * 100, 2)
        total_expansion_bps = round((new_pocket_margin_pct - baseline["baseline_pocket_margin_pct"]) * 100, 0)

        synthesis = {
            "baseline": baseline,
            "scenarios": [s1, s2, s3],
            "combined_transformation": {
                "new_net_revenue": round(total_net_rev, 2),
                "new_pocket_profit": round(total_profit, 2),
                "net_profit_delta_inr": round(total_profit - baseline["baseline_pocket_profit"], 2),
                "baseline_pocket_margin_pct": baseline["baseline_pocket_margin_pct"],
                "new_pocket_margin_pct": new_pocket_margin_pct,
                "total_margin_expansion_bps": total_expansion_bps
            }
        }
        return synthesis

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    engine = ScenarioEngine(processed_dir)
    results = engine.run_full_strategic_transformation()

    print("=== STRATEGIC TRANSFORMATION SCENARIO RESULTS ===")
    print(f"Baseline Pocket Profit: INR {results['baseline']['baseline_pocket_profit']:,.2f} ({results['baseline']['baseline_pocket_margin_pct']}%)")
    for s in results["scenarios"]:
        print(f"\nScenario: {s['scenario']}")
        print(f"  Profit Delta: INR {s['pocket_profit_impact_inr']:,.2f}")
        print(f"  Margin Impact: +{s['margin_expansion_bps']} bps")

    comb = results["combined_transformation"]
    print(f"\n--- COMBINED STRATEGIC IMPACT ---")
    print(f"  New Pocket Profit: INR {comb['new_pocket_profit']:,.2f}")
    print(f"  New Pocket Margin %: {comb['new_pocket_margin_pct']}% (Expansion: +{comb['total_margin_expansion_bps']} bps)")

if __name__ == "__main__":
    main()
