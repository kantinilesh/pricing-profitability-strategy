"""
driver_analysis.py
Executes Step 3: Cost & Driver Analysis.
Decomposes variable costs, channel fulfillment costs, return expenses, and promotional spend
across categories, channels, and regions to identify cost leakages.
"""

import os
import pandas as pd
import numpy as np

def run_driver_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # 1. Cost Breakdown by Category
    cat_costs = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        variable_cost=("variable_cost", "sum"),
        gross_profit=("gross_profit", "sum"),
        list_value=("list_price", lambda x: (x * df.loc[x.index, "units"]).sum()),
        discount_value=("discount", lambda x: (x * df.loc[x.index, "units"]).sum())
    ).reset_index()

    cat_costs["cost_pct_of_rev"] = (cat_costs["variable_cost"] / cat_costs["revenue"] * 100).round(2)
    cat_costs["gross_margin_pct"] = (cat_costs["gross_profit"] / cat_costs["revenue"] * 100).round(2)
    cat_costs["avg_discount_pct"] = (cat_costs["discount_value"] / cat_costs["list_value"] * 100).round(2)

    # 2. Channel Fulfillment & Take-Rate Cost Analysis
    chan_costs = df.groupby("channel").agg(
        order_count=("transaction_id", "count"),
        revenue=("revenue", "sum"),
        variable_cost=("variable_cost", "sum"),
        gross_profit=("gross_profit", "sum"),
        avg_take_rate=("take_rate_pct", "mean"),
        avg_cost_to_serve=("cost_to_serve_base_pct", "mean")
    ).reset_index()

    chan_costs["variable_cost_pct"] = (chan_costs["variable_cost"] / chan_costs["revenue"] * 100).round(2)
    chan_costs["gross_margin_pct"] = (chan_costs["gross_profit"] / chan_costs["revenue"] * 100).round(2)

    # 3. Promotional Spend & Co-op Offset Analysis
    promo_costs = df.groupby("promotion_type").agg(
        order_count=("transaction_id", "count"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum"),
        avg_discount_pct=("discount_pct", "mean"),
        vendor_coop_pct=("vendor_coop_share_pct", "mean")
    ).reset_index()

    promo_costs["gross_margin_pct"] = (promo_costs["gross_profit"] / promo_costs["revenue"] * 100).round(2)

    return {
        "category_costs": cat_costs,
        "channel_costs": chan_costs,
        "promo_costs": promo_costs
    }

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    drivers = run_driver_analysis(processed_dir)

    print("=== CATEGORY COST & DISCOUNT BREAKDOWN ===")
    print(drivers["category_costs"].to_string())

    print("\n=== CHANNEL COST-TO-SERVE & FULFILLMENT BREAKDOWN ===")
    print(drivers["channel_costs"].to_string())

if __name__ == "__main__":
    main()
