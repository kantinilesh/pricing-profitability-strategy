"""
promotion_segmentation.py
Decomposes promotional lift, discount depth, and margin impact across Customer Segments,
Sales Channels, Product Categories, and Geographic Regions.
"""

import os
import pandas as pd
import numpy as np

def run_promotion_segmentation(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # 1. Promo Effectiveness by Customer Segment
    seg_promo = df.groupby(["customer_segment", "promotion_type"]).agg(
        orders=("transaction_id", "count"),
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum"),
        avg_discount_pct=("discount_pct", "mean")
    ).reset_index()

    seg_promo["gross_margin_pct"] = (seg_promo["gross_profit"] / seg_promo["revenue"] * 100).round(2)

    # 2. Promo Effectiveness by Channel
    chan_promo = df.groupby(["channel", "promotion_type"]).agg(
        orders=("transaction_id", "count"),
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum"),
        avg_discount_pct=("discount_pct", "mean")
    ).reset_index()

    chan_promo["gross_margin_pct"] = (chan_promo["gross_profit"] / chan_promo["revenue"] * 100).round(2)

    # 3. Promo Effectiveness by Category
    cat_promo = df.groupby(["category", "promotion_type"]).agg(
        orders=("transaction_id", "count"),
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum"),
        avg_discount_pct=("discount_pct", "mean")
    ).reset_index()

    cat_promo["gross_margin_pct"] = (cat_promo["gross_profit"] / cat_promo["revenue"] * 100).round(2)

    return {
        "segment_promo": seg_promo,
        "channel_promo": chan_promo,
        "category_promo": cat_promo
    }

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    seg = run_promotion_segmentation(processed_dir)

    print("=== PROMOTION PERFORMANCE BY CHANNEL ===")
    print(seg["channel_promo"].head(10).to_string())

    print("\n=== PROMOTION PERFORMANCE BY CATEGORY ===")
    print(seg["category_promo"].head(10).to_string())

if __name__ == "__main__":
    main()
