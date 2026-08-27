"""
Customer Profitability & Whale Curve Engine.
Ranks customer accounts by net pocket profit contribution, constructs the cumulative profit 
Whale Curve, and identifies value-destroying accounts for discount governance interventions.
"""

import os
import pandas as pd
import numpy as np

class CustomerAnalyticsEngine:
    def __init__(self, processed_dir):
        self.processed_dir = processed_dir
        self.df_cust = pd.read_csv(os.path.join(processed_dir, "customer_profitability_mart.csv"))

    def compute_whale_curve(self):
        """
        Constructs the Bain Customer Profitability Whale Curve dataset.
        Ranks customers from most profitable to least profitable.
        """
        df_sorted = self.df_cust.sort_values(by="total_pocket_profit_inr", ascending=False).copy()
        
        total_profit = df_sorted["total_pocket_profit_inr"].sum()
        df_sorted["cumulative_profit_inr"] = df_sorted["total_pocket_profit_inr"].cumsum()
        df_sorted["cumulative_profit_pct"] = (df_sorted["cumulative_profit_inr"] / total_profit) * 100
        
        df_sorted["customer_rank"] = range(1, len(df_sorted) + 1)
        df_sorted["cumulative_customer_pct"] = (df_sorted["customer_rank"] / len(df_sorted)) * 100

        # Classification into Customer Profit Tiers
        def classify_customer(row):
            if row["total_pocket_profit_inr"] < 0:
                return "Value Destroyer (Negative Profit)"
            elif row["cumulative_profit_pct"] <= 80:
                return "Core Value Driver (Top 80% Profit)"
            else:
                return "Break-Even / Marginal Account"

        df_sorted["profitability_tier"] = df_sorted.apply(classify_customer, axis=1)
        return df_sorted

    def evaluate_customer_segmentation(self):
        """
        Aggregates customer economics by Customer Type (B2B Enterprise, SMB, Retail Tiers).
        """
        segment_summary = self.df_cust.groupby("customer_type").agg(
            customer_count=("customer_id", "count"),
            total_net_revenue_inr=("total_net_revenue_inr", "sum"),
            total_discount_inr=("total_discount_inr", "sum"),
            total_fulfillment_cost_inr=("total_fulfillment_cost_inr", "sum"),
            total_pocket_profit_inr=("total_pocket_profit_inr", "sum"),
            avg_contract_discount_pct=("contract_discount_pct", "mean")
        ).reset_index()

        segment_summary["pocket_margin_pct"] = round(
            (segment_summary["total_pocket_profit_inr"] / segment_summary["total_net_revenue_inr"]) * 100, 2
        )
        segment_summary["discount_rate_pct"] = round(
            (segment_summary["total_discount_inr"] / (segment_summary["total_net_revenue_inr"] + segment_summary["total_discount_inr"])) * 100, 2
        )

        return segment_summary.sort_values(by="pocket_margin_pct", ascending=False)

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    engine = CustomerAnalyticsEngine(processed_dir)
    whale = engine.compute_whale_curve()
    print("--- CUSTOMER PROFITABILITY WHALE CURVE SUMMARY ---")
    print(whale["profitability_tier"].value_counts().to_string())

    print("\n--- CUSTOMER SEGMENT ECONOMICS ---")
    segments = engine.evaluate_customer_segmentation()
    print(segments.to_string())

if __name__ == "__main__":
    main()
