"""
pareto_analysis.py
Executes Step 5: 80/20 Pareto Analysis.
Identifies Top 20% Profit Drivers vs Bottom 20% Margin Destroyers across Products,
Customer Accounts, Regions, and Distribution Channels.
"""

import os
import pandas as pd
import numpy as np

def run_pareto_analysis(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # 1. Product Pareto Analysis
    prd = df.groupby(["product_id", "product_name", "category"]).agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index().sort_values(by="gross_profit", ascending=False)

    prd["cumulative_profit"] = prd["gross_profit"].cumsum()
    tot_prd_profit = prd["gross_profit"].sum()
    prd["cumulative_profit_pct"] = (prd["cumulative_profit"] / tot_prd_profit * 100).round(2)
    prd["sku_rank"] = range(1, len(prd) + 1)
    prd["sku_rank_pct"] = (prd["sku_rank"] / len(prd) * 100).round(2)

    top_20_products = prd[prd["sku_rank_pct"] <= 20.0]
    bottom_20_products = prd[prd["sku_rank_pct"] > 80.0]

    # 2. Customer Pareto Analysis
    cst = df.groupby(["customer_id", "customer_name", "customer_segment"]).agg(
        orders=("transaction_id", "count"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index().sort_values(by="gross_profit", ascending=False)

    cst["cumulative_profit"] = cst["gross_profit"].cumsum()
    tot_cst_profit = cst["gross_profit"].sum()
    cst["cumulative_profit_pct"] = (cst["cumulative_profit"] / tot_cst_profit * 100).round(2)
    cst["cust_rank"] = range(1, len(cst) + 1)
    cst["cust_rank_pct"] = (cst["cust_rank"] / len(cst) * 100).round(2)

    top_20_customers = cst[cst["cust_rank_pct"] <= 20.0]
    bottom_20_customers = cst[cst["cust_rank_pct"] > 80.0]

    # 3. Customer Value Destroyers (Negative Gross Profit)
    value_destroying_customers = cst[cst["gross_profit"] < 0]

    pareto_summary = {
        "total_skus": len(prd),
        "top_20_sku_profit_share_pct": round(top_20_products["gross_profit"].sum() / tot_prd_profit * 100, 2),
        "bottom_20_sku_profit_share_pct": round(bottom_20_products["gross_profit"].sum() / tot_prd_profit * 100, 2),
        "total_customers": len(cst),
        "top_20_cust_profit_share_pct": round(top_20_customers["gross_profit"].sum() / tot_cst_profit * 100, 2),
        "value_destroying_customers_count": len(value_destroying_customers),
        "value_destroying_customers_profit_loss_inr": round(value_destroying_customers["gross_profit"].sum(), 2)
    }

    return pareto_summary, top_20_products, bottom_20_products, top_20_customers, value_destroying_customers

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    summary, top_prd, bot_prd, top_cst, val_dest = run_pareto_analysis(processed_dir)

    print("=== PARETO 80/20 ANALYSIS SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\n--- TOP 5 PROFIT-GENERATING SKUS ---")
    print(top_prd[["product_id", "product_name", "category", "revenue", "gross_profit", "cumulative_profit_pct"]].head(5).to_string())

    print("\n--- BOTTOM 5 MARGIN-DILUTING SKUS ---")
    print(bot_prd[["product_id", "product_name", "category", "revenue", "gross_profit"]].head(5).to_string())

if __name__ == "__main__":
    main()
