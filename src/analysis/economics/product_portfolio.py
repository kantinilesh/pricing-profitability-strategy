"""
product_portfolio.py
Executes Product Portfolio & Profitability Matrix Analysis.
Evaluates SKU-level metrics (Revenue, Profit, Margin, Volume, Discount, Promo Dependency, Customer Penetration)
and classifies products into 5 strategic portfolio archetypes.
"""

import os
import pandas as pd
import numpy as np

def run_product_portfolio_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Aggregate SKU-level metrics
    prd_agg = df.groupby(["product_id", "product_name", "category", "list_price"]).agg(
        total_units=("units", "sum"),
        total_revenue=("revenue", "sum"),
        total_gross_profit=("gross_profit", "sum"),
        total_list_value=("list_price", lambda x: (x * df.loc[x.index, "units"]).sum()),
        total_discount_value=("discount", lambda x: (x * df.loc[x.index, "units"]).sum()),
        promo_orders=("promotion_flag", "sum"),
        total_orders=("transaction_id", "count"),
        customer_penetration=("customer_id", "nunique")
    ).reset_index()

    prd_agg["gross_margin_pct"] = (prd_agg["total_gross_profit"] / prd_agg["total_revenue"] * 100).round(2)
    prd_agg["avg_discount_pct"] = (prd_agg["total_discount_value"] / prd_agg["total_list_value"] * 100).round(2)
    prd_agg["promo_dependency_pct"] = (prd_agg["promo_orders"] / prd_agg["total_orders"] * 100).round(2)

    rev_75th = prd_agg["total_revenue"].quantile(0.75)
    margin_median = prd_agg["gross_margin_pct"].median()
    units_75th = prd_agg["total_units"].quantile(0.75)

    def classify_portfolio(row):
        high_rev = row["total_revenue"] >= rev_75th
        high_margin = row["gross_margin_pct"] >= margin_median
        high_vol = row["total_units"] >= units_75th
        high_promo = row["promo_dependency_pct"] >= 40.0

        if high_rev and high_margin:
            return "1. Revenue & Profit Stars (Core Champions)"
        elif not high_rev and high_margin:
            return "2. Profit Stars (Niche High-Margin SKUs)"
        elif high_vol and not high_margin:
            return "3. Volume-Heavy Low-Margin (Electronics / Bulk)"
        elif high_promo:
            return "4. Discount-Dependent Products (Promotional Drag)"
        else:
            return "5. Low-Volume Low-Margin (Dog SKUs)"

    prd_agg["portfolio_archetype"] = prd_agg.apply(classify_portfolio, axis=1)

    portfolio_summary = prd_agg.groupby("portfolio_archetype").agg(
        sku_count=("product_id", "count"),
        total_units_sold=("total_units", "sum"),
        total_revenue_inr=("total_revenue", "sum"),
        total_gross_profit_inr=("total_gross_profit", "sum"),
        avg_gross_margin_pct=("gross_margin_pct", "mean"),
        avg_discount_pct=("avg_discount_pct", "mean"),
        avg_customer_penetration=("customer_penetration", "mean")
    ).reset_index()

    portfolio_summary["revenue_share_pct"] = (portfolio_summary["total_revenue_inr"] / prd_agg["total_revenue"].sum() * 100).round(2)
    portfolio_summary["profit_share_pct"] = (portfolio_summary["total_gross_profit_inr"] / prd_agg["total_gross_profit"].sum() * 100).round(2)

    return prd_agg, portfolio_summary

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    prd_df, summary = run_product_portfolio_analysis(processed_dir)

    print("=== PRODUCT PORTFOLIO ARCHETYPE SUMMARY ===")
    print(summary.to_string())

if __name__ == "__main__":
    main()
