"""
Profitability Decomposition Engine.
Decomposes gross-to-pocket margin waterfalls, calculates Pareto 80/20 distributions,
and evaluates channel & regional cost-to-serve leakages.
"""

import os
import pandas as pd
import numpy as np

class ProfitabilityEngine:
    def __init__(self, processed_dir):
        self.processed_dir = processed_dir
        self.df_fact = pd.read_csv(os.path.join(processed_dir, "analytical_transaction_fact.csv"))
        self.df_prod = pd.read_csv(os.path.join(processed_dir, "product_margin_mart.csv"))

    def compute_margin_waterfall(self):
        """
        Computes total company gross-to-pocket margin waterfall metrics.
        """
        gross_rev = self.df_fact["gross_revenue_inr"].sum()
        contract_disc = self.df_fact["contract_discount_inr"].sum()
        promo_disc = self.df_fact["promo_discount_inr"].sum()
        adhoc_disc = self.df_fact["adhoc_discount_inr"].sum()
        total_disc = self.df_fact["total_discount_inr"].sum()
        net_rev = self.df_fact["net_revenue_inr"].sum()
        cogs = self.df_fact["base_cogs_inr"].sum()
        gross_margin = net_rev - cogs
        fulfillment = self.df_fact["fulfillment_cost_inr"].sum()
        returns = self.df_fact["return_cost_inr"].sum()
        vendor_coop = self.df_fact["vendor_coop_rebate_inr"].sum()
        pocket_profit = self.df_fact["pocket_profit_inr"].sum()

        waterfall = {
            "gross_revenue": round(gross_rev, 2),
            "contract_discounts": round(-contract_disc, 2),
            "promo_discounts": round(-promo_disc, 2),
            "adhoc_markdown_discounts": round(-adhoc_disc, 2),
            "net_revenue": round(net_rev, 2),
            "cogs": round(-cogs, 2),
            "gross_margin": round(gross_margin, 2),
            "fulfillment_logistics": round(-fulfillment, 2),
            "return_costs": round(-returns, 2),
            "vendor_coop_rebates": round(vendor_coop, 2),
            "pocket_profit": round(pocket_profit, 2),
            "gross_margin_pct": round((gross_margin / net_rev) * 100, 2),
            "pocket_margin_pct": round((pocket_profit / net_rev) * 100, 2),
            "total_leakage_pct": round(((gross_rev - pocket_profit) / gross_rev) * 100, 2)
        }
        return waterfall

    def compute_pareto_analysis(self, group_col="product_id"):
        """
        Performs 80/20 Pareto Analysis on SKUs or Categories by Pocket Profit contribution.
        """
        df_sorted = self.df_prod.sort_values(by="total_pocket_profit_inr", ascending=False).copy()
        total_profit = df_sorted["total_pocket_profit_inr"].sum()
        
        df_sorted["cumulative_profit"] = df_sorted["total_pocket_profit_inr"].cumsum()
        df_sorted["cumulative_profit_pct"] = (df_sorted["cumulative_profit"] / total_profit) * 100
        df_sorted["sku_rank"] = range(1, len(df_sorted) + 1)
        df_sorted["cumulative_sku_pct"] = (df_sorted["sku_rank"] / len(df_sorted)) * 100

        # Classification into Pareto Tiers
        def classify_pareto(cum_pct):
            if cum_pct <= 70:
                return "Tier A (Top 70% Profit)"
            elif cum_pct <= 90:
                return "Tier B (Next 20% Profit)"
            else:
                return "Tier C (Tail / Low Margin)"

        df_sorted["pareto_tier"] = df_sorted["cumulative_profit_pct"].apply(classify_pareto)
        return df_sorted

    def compute_channel_regional_leakage(self):
        """
        Analyzes fulfillment and return cost leakage across channels and city tiers.
        """
        grouped = self.df_fact.groupby(["channel", "city_tier"]).agg(
            net_revenue=("net_revenue_inr", "sum"),
            cogs=("base_cogs_inr", "sum"),
            fulfillment_cost=("fulfillment_cost_inr", "sum"),
            return_cost=("return_cost_inr", "sum"),
            pocket_profit=("pocket_profit_inr", "sum"),
            order_count=("transaction_id", "count")
        ).reset_index()

        grouped["gross_margin_pct"] = round((grouped["net_revenue"] - grouped["cogs"]) / grouped["net_revenue"] * 100, 2)
        grouped["fulfillment_cost_pct"] = round(grouped["fulfillment_cost"] / grouped["net_revenue"] * 100, 2)
        grouped["return_cost_pct"] = round(grouped["return_cost"] / grouped["net_revenue"] * 100, 2)
        grouped["pocket_margin_pct"] = round(grouped["pocket_profit"] / grouped["net_revenue"] * 100, 2)

        return grouped.sort_values(by="pocket_margin_pct", ascending=True)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    engine = ProfitabilityEngine(processed_dir)
    waterfall = engine.compute_margin_waterfall()
    print("--- MARGIN WATERFALL ANALYSIS ---")
    for k, v in waterfall.items():
        print(f"  {k}: {v}")
    
    pareto = engine.compute_pareto_analysis()
    print(f"\n--- PARETO SUMMARY --- Total SKUs: {len(pareto)}")
    print(pareto["pareto_tier"].value_counts())

if __name__ == "__main__":
    main()
