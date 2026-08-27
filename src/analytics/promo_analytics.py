"""
Promotion Incremental Value Engine.
Evaluates campaign performance by decomposing promotional volume into baseline vs incremental lift,
calculating trade spend efficiency, vendor co-op offsets, and net incremental margin ROI.
"""

import os
import pandas as pd
import numpy as np

class PromotionAnalyticsEngine:
    def __init__(self, processed_dir):
        self.processed_dir = processed_dir
        self.df_fact = pd.read_csv(os.path.join(processed_dir, "analytical_transaction_fact.csv"))
        self.df_promo_mart = pd.read_csv(os.path.join(processed_dir, "promo_performance_mart.csv"))

    def compute_incremental_promo_roi(self):
        """
        Calculates Net Incremental Margin ROI for each promotion campaign.
        Baseline volume is estimated from non-promo transaction velocity per product category.
        """
        # Baseline non-promo daily volume rate per product category
        df_no_promo = self.df_fact[self.df_fact["promo_id"] == "PROMO_NONE"]
        cat_baseline = df_no_promo.groupby("category")["quantity"].mean().to_dict()

        promo_results = []
        promos = self.df_fact["promo_id"].unique()

        for pid in promos:
            if pid == "PROMO_NONE":
                continue

            df_p = self.df_fact[self.df_fact["promo_id"] == pid].copy()
            promo_name = df_p["promo_name"].iloc[0]
            promo_type = df_p["promo_type"].iloc[0]

            total_qty = df_p["quantity"].sum()
            total_net_rev = df_p["net_revenue_inr"].sum()
            total_cogs = df_p["base_cogs_inr"].sum()
            actual_gross_margin = total_net_rev - total_cogs
            
            promo_spend = df_p["promo_discount_inr"].sum()
            vendor_coop = df_p["vendor_coop_rebate_inr"].sum()
            net_trade_spend = max(1.0, promo_spend - vendor_coop)

            # Estimated Baseline Quantity & Baseline Gross Margin (if no promo occurred)
            # Baseline assumes items were sold at list price - contract discount without promo discount
            expected_baseline_qty = sum(cat_baseline.get(row["category"], 2.0) for _, row in df_p.iterrows())
            incremental_qty = max(0, total_qty - expected_baseline_qty)

            # Baseline margin per unit
            avg_unit_list = (df_p["gross_revenue_inr"] / df_p["quantity"]).mean()
            avg_unit_cogs = (df_p["base_cogs_inr"] / df_p["quantity"]).mean()
            avg_unit_contract_disc = (df_p["contract_discount_inr"] / df_p["quantity"]).mean()
            baseline_unit_margin = avg_unit_list - avg_unit_contract_disc - avg_unit_cogs

            estimated_baseline_margin = expected_baseline_qty * baseline_unit_margin
            incremental_gross_margin = actual_gross_margin - estimated_baseline_margin

            incremental_roi = round(incremental_gross_margin / net_trade_spend, 2)

            if incremental_roi > 1.0:
                classification = "Highly Value Accretive"
            elif incremental_roi >= 0.0:
                classification = "Marginally Positive"
            else:
                classification = "Value Destructive (Negative ROI)"

            promo_results.append({
                "promo_id": pid,
                "promo_name": promo_name,
                "promo_type": promo_type,
                "total_units_sold": total_qty,
                "estimated_incremental_units": round(incremental_qty, 0),
                "total_net_revenue_inr": round(total_net_rev, 2),
                "promo_discount_spend_inr": round(promo_spend, 2),
                "vendor_coop_rebate_inr": round(vendor_coop, 2),
                "net_trade_spend_inr": round(net_trade_spend, 2),
                "incremental_gross_margin_inr": round(incremental_gross_margin, 2),
                "incremental_promo_roi": incremental_roi,
                "efficiency_classification": classification
            })

        return pd.DataFrame(promo_results).sort_values(by="incremental_promo_roi", ascending=False)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    engine = PromotionAnalyticsEngine(processed_dir)
    df_roi = engine.compute_incremental_promo_roi()
    print("--- PROMOTION INCREMENTAL ROI ANALYSIS ---")
    print(df_roi.to_string())

if __name__ == "__main__":
    main()
