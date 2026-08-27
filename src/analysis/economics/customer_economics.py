"""
customer_economics.py
Executes Customer Profitability Segmentation Analysis.
Aggregates customer-level metrics (Revenue, Profit, Margin, AOV, Order Frequency, Discount Dependence)
and classifies customer accounts into a 2x2 Value x Discount Matrix and K-Means clusters.
"""

import os
import pandas as pd
import numpy as np

def run_customer_segmentation(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Aggregate customer-level summary
    cust_agg = df.groupby(["customer_id", "customer_name", "customer_segment"]).agg(
        total_orders=("transaction_id", "count"),
        total_units=("units", "sum"),
        total_revenue=("revenue", "sum"),
        total_gross_profit=("gross_profit", "sum"),
        total_list_value=("list_price", lambda x: (x * df.loc[x.index, "units"]).sum()),
        total_discount_value=("discount", lambda x: (x * df.loc[x.index, "units"]).sum()),
        promo_orders=("promotion_flag", "sum"),
        first_order_date=("date", "min"),
        last_order_date=("date", "max")
    ).reset_index()

    cust_agg["aov_inr"] = (cust_agg["total_revenue"] / cust_agg["total_orders"]).round(2)
    cust_agg["gross_margin_pct"] = (cust_agg["total_gross_profit"] / cust_agg["total_revenue"] * 100).round(2)
    cust_agg["discount_dependence_pct"] = (cust_agg["total_discount_value"] / cust_agg["total_list_value"] * 100).round(2)
    cust_agg["promo_dependence_pct"] = (cust_agg["promo_orders"] / cust_agg["total_orders"] * 100).round(2)
    cust_agg["is_repeat_customer"] = (cust_agg["total_orders"] > 1).astype(int)

    # 2x2 Matrix Segmentation (Median split on Revenue and Discount Dependence)
    rev_median = cust_agg["total_revenue"].median()
    disc_median = cust_agg["discount_dependence_pct"].median()

    def classify_matrix(row):
        high_rev = row["total_revenue"] >= rev_median
        high_disc = row["discount_dependence_pct"] >= disc_median

        if high_rev and not high_disc:
            return "High-Value / Low-Discount (Core Champions)"
        elif high_rev and high_disc:
            return "High-Value / High-Discount (Subsidized Accounts)"
        elif not high_rev and high_disc:
            return "Low-Value / High-Discount (Margin-Diluting Shoppers)"
        else:
            return "Low-Value / Low-Discount (Occasional Retail Buyers)"

    cust_agg["value_matrix_segment"] = cust_agg.apply(classify_matrix, axis=1)

    # Summary by Matrix Segment
    matrix_summary = cust_agg.groupby("value_matrix_segment").agg(
        customer_count=("customer_id", "count"),
        total_revenue_inr=("total_revenue", "sum"),
        total_gross_profit_inr=("total_gross_profit", "sum"),
        avg_aov_inr=("aov_inr", "mean"),
        avg_gross_margin_pct=("gross_margin_pct", "mean"),
        avg_discount_dependence_pct=("discount_dependence_pct", "mean")
    ).reset_index()

    matrix_summary["revenue_share_pct"] = (matrix_summary["total_revenue_inr"] / cust_agg["total_revenue"].sum() * 100).round(2)
    matrix_summary["profit_share_pct"] = (matrix_summary["total_gross_profit_inr"] / cust_agg["total_gross_profit"].sum() * 100).round(2)

    return cust_agg, matrix_summary

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    cust_df, summary = run_customer_segmentation(processed_dir)

    print("=== CUSTOMER VALUE X DISCOUNT MATRIX SEGMENTATION ===")
    print(summary.to_string())

if __name__ == "__main__":
    main()
