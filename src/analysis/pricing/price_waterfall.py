"""
price_waterfall.py
Constructs the Price Waterfall (List Price -> Contract Discount -> Promo Discount -> Realized Price -> Variable Cost -> Gross Margin).
Analyzes Price Realization across Customer Segments, Product Categories, Geographies, and Channels.
"""

import os
import pandas as pd
import numpy as np

def run_price_waterfall_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Overall Company Price Waterfall (Per Unit Averages)
    df["total_units"] = df["units"]
    df["total_list_value"] = df["list_price"] * df["units"]
    df["total_discount_value"] = df["discount"] * df["units"]
    df["total_cogs_var"] = df["variable_cost"]

    tot_units = df["total_units"].sum()
    tot_list_val = df["total_list_value"].sum()
    tot_disc_val = df["total_discount_value"].sum()
    tot_net_rev = df["revenue"].sum()
    tot_var_cost = df["variable_cost"].sum()
    tot_gross_profit = df["gross_profit"].sum()

    waterfall_per_unit = {
        "avg_list_price_inr": round(tot_list_val / tot_units, 2),
        "avg_discount_inr": round(tot_disc_val / tot_units, 2),
        "avg_realized_price_inr": round(tot_net_rev / tot_units, 2),
        "avg_variable_cost_inr": round(tot_var_cost / tot_units, 2),
        "avg_gross_profit_inr": round(tot_gross_profit / tot_units, 2),
        "list_to_realized_realization_pct": round((tot_net_rev / tot_list_val) * 100, 2),
        "aggregate_discount_rate_pct": round((tot_disc_val / tot_list_val) * 100, 2),
        "discount_frequency_pct": round((df["discount"] > 0).mean() * 100, 2)
    }

    # 1. Price Realization by Customer Segment
    segment_waterfall = df.groupby("customer_segment").agg(
        units=("units", "sum"),
        list_value=("total_list_value", "sum"),
        revenue=("revenue", "sum"),
        discount_value=("total_discount_value", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    segment_waterfall["avg_list_price"] = (segment_waterfall["list_value"] / segment_waterfall["units"]).round(2)
    segment_waterfall["avg_realized_price"] = (segment_waterfall["revenue"] / segment_waterfall["units"]).round(2)
    segment_waterfall["discount_rate_pct"] = (segment_waterfall["discount_value"] / segment_waterfall["list_value"] * 100).round(2)
    segment_waterfall["price_realization_pct"] = (segment_waterfall["revenue"] / segment_waterfall["list_value"] * 100).round(2)

    # 2. Price Realization by Product Category
    category_waterfall = df.groupby("category").agg(
        units=("units", "sum"),
        list_value=("total_list_value", "sum"),
        revenue=("revenue", "sum"),
        discount_value=("total_discount_value", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    category_waterfall["avg_list_price"] = (category_waterfall["list_value"] / category_waterfall["units"]).round(2)
    category_waterfall["avg_realized_price"] = (category_waterfall["revenue"] / category_waterfall["units"]).round(2)
    category_waterfall["discount_rate_pct"] = (category_waterfall["discount_value"] / category_waterfall["list_value"] * 100).round(2)
    category_waterfall["price_realization_pct"] = (category_waterfall["revenue"] / category_waterfall["list_value"] * 100).round(2)

    # 3. Price Realization by Channel
    channel_waterfall = df.groupby("channel").agg(
        units=("units", "sum"),
        list_value=("total_list_value", "sum"),
        revenue=("revenue", "sum"),
        discount_value=("total_discount_value", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    channel_waterfall["avg_list_price"] = (channel_waterfall["list_value"] / channel_waterfall["units"]).round(2)
    channel_waterfall["avg_realized_price"] = (channel_waterfall["revenue"] / channel_waterfall["units"]).round(2)
    channel_waterfall["discount_rate_pct"] = (channel_waterfall["discount_value"] / channel_waterfall["list_value"] * 100).round(2)
    channel_waterfall["price_realization_pct"] = (channel_waterfall["revenue"] / channel_waterfall["list_value"] * 100).round(2)

    # 4. Price Realization by Geography
    region_waterfall = df.groupby("region").agg(
        units=("units", "sum"),
        list_value=("total_list_value", "sum"),
        revenue=("revenue", "sum"),
        discount_value=("total_discount_value", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()

    region_waterfall["avg_list_price"] = (region_waterfall["list_value"] / region_waterfall["units"]).round(2)
    region_waterfall["avg_realized_price"] = (region_waterfall["revenue"] / region_waterfall["units"]).round(2)
    region_waterfall["discount_rate_pct"] = (region_waterfall["discount_value"] / region_waterfall["list_value"] * 100).round(2)
    region_waterfall["price_realization_pct"] = (region_waterfall["revenue"] / region_waterfall["list_value"] * 100).round(2)

    return {
        "overall_waterfall": waterfall_per_unit,
        "segment_waterfall": segment_waterfall,
        "category_waterfall": category_waterfall,
        "channel_waterfall": channel_waterfall,
        "region_waterfall": region_waterfall
    }

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    res = run_price_waterfall_analysis(processed_dir)

    print("=== OVERALL COMPANY PRICE WATERFALL (PER UNIT AVERAGE) ===")
    for k, v in res["overall_waterfall"].items():
        print(f"  {k}: {v}")

    print("\n=== PRICE REALIZATION BY CUSTOMER SEGMENT ===")
    print(res["segment_waterfall"][["customer_segment", "avg_list_price", "avg_realized_price", "discount_rate_pct", "price_realization_pct"]].to_string())

    print("\n=== PRICE REALIZATION BY CHANNEL ===")
    print(res["channel_waterfall"][["channel", "avg_list_price", "avg_realized_price", "discount_rate_pct", "price_realization_pct"]].to_string())

if __name__ == "__main__":
    main()
