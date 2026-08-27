"""
mix_analysis.py
Executes Step 2 (Mix Investigation): Analyzes Product Mix, Customer Mix, Region Mix, and Channel Mix shifts.
Quantifies how changes in category volume composition, customer segment growth, and distribution channel shares
impact overall gross margin %.
"""

import os
import pandas as pd
import numpy as np

def run_mix_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # 1. Product Mix Analysis
    prod_mix = df.groupby(["year", "category"]).agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    prod_mix["revenue_share"] = prod_mix.groupby("year")["revenue"].transform(lambda x: x / x.sum() * 100).round(2)
    prod_mix["gross_margin_pct"] = (prod_mix["gross_profit"] / prod_mix["revenue"] * 100).round(2)

    # 2. Customer Mix Analysis
    cust_mix = df.groupby(["year", "customer_segment"]).agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    cust_mix["revenue_share"] = cust_mix.groupby("year")["revenue"].transform(lambda x: x / x.sum() * 100).round(2)
    cust_mix["gross_margin_pct"] = (cust_mix["gross_profit"] / cust_mix["revenue"] * 100).round(2)

    # 3. Channel Mix Analysis
    chan_mix = df.groupby(["year", "channel"]).agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    chan_mix["revenue_share"] = chan_mix.groupby("year")["revenue"].transform(lambda x: x / x.sum() * 100).round(2)
    chan_mix["gross_margin_pct"] = (chan_mix["gross_profit"] / chan_mix["revenue"] * 100).round(2)

    # 4. Region Mix Analysis
    reg_mix = df.groupby(["year", "region"]).agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    reg_mix["revenue_share"] = reg_mix.groupby("year")["revenue"].transform(lambda x: x / x.sum() * 100).round(2)
    reg_mix["gross_margin_pct"] = (reg_mix["gross_profit"] / reg_mix["revenue"] * 100).round(2)

    return {
        "product_mix": prod_mix,
        "customer_mix": cust_mix,
        "channel_mix": chan_mix,
        "region_mix": reg_mix
    }

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    mix = run_mix_analysis(processed_dir)

    print("=== PRODUCT CATEGORY MIX EVOLUTION ===")
    print(mix["product_mix"].to_string())

    print("\n=== CUSTOMER SEGMENT MIX EVOLUTION ===")
    print(mix["customer_mix"].to_string())

    print("\n=== CHANNEL DISTRIBUTION MIX EVOLUTION ===")
    print(mix["channel_mix"].to_string())

if __name__ == "__main__":
    main()
