"""
03_clean_data.py
Executes documented data cleaning transformations on raw transactions:
deduplication, category string normalization, missing value imputation, negative sign correction,
reconciliation math enforcement, and outlier flagging.
Outputs data/processed/transactions_cleaned.csv.
"""

import os
import pandas as pd
import numpy as np

def clean_transactions(raw_dir, processed_dir):
    tx_path = os.path.join(raw_dir, "transactions_raw.csv")
    df = pd.read_csv(tx_path)

    initial_count = len(df)
    print(f"Initial raw records: {initial_count:,}")

    # 1. Deduplication
    df = df.drop_duplicates().copy()
    df = df.drop_duplicates(subset=["transaction_id"], keep="first").copy()
    post_dedup_count = len(df)
    print(f"Records after deduplication: {post_dedup_count:,} (Removed {initial_count - post_dedup_count:,} duplicates)")

    # 2. Category Normalization
    category_map = {
        "consumer_electronics": "Consumer Electronics",
        "apparel & fashion  ": "Apparel & Fashion",
        "home_&_kitchen": "Home & Kitchen",
        "Apparel & Fashion  ": "Apparel & Fashion"
    }

    def normalize_cat(val):
        if pd.isna(val):
            return "Other"
        val_str = str(val).strip()
        if val_str in category_map:
            return category_map[val_str]
        # Title case fallback
        if val_str.lower() == "consumer_electronics":
            return "Consumer Electronics"
        if val_str.lower() == "home_&_kitchen":
            return "Home & Kitchen"
        return val_str

    df["category"] = df["category"].apply(normalize_cat)

    # 3. Missing Value Imputation
    df["customer_segment"] = df["customer_segment"].fillna("Unknown / Unclassified")
    df["promotion_type"] = df["promotion_type"].fillna("Baseline / None")

    # Impute missing variable_cost using category median variable_cost ratio
    df["cost_ratio"] = df["variable_cost"] / df["revenue"]
    median_cost_ratios = df.groupby("category")["cost_ratio"].median().to_dict()

    def impute_var_cost(row):
        if pd.isna(row["variable_cost"]) or row["revenue"] <= 0:
            cat = row["category"]
            ratio = median_cost_ratios.get(cat, 0.75)
            return round(abs(row["revenue"]) * ratio, 2)
        return row["variable_cost"]

    df["variable_cost"] = df.apply(impute_var_cost, axis=1)
    df.drop(columns=["cost_ratio"], inplace=True)

    # 4. Negative Revenue Sign Correction
    df["revenue"] = df["revenue"].abs()

    # 5. Math Reconciliation Enforcement
    # Reconcile discount & discount_pct
    df["discount"] = (df["list_price"] - df["selling_price"]).round(2)
    df["discount_pct"] = (df["discount"] / df["list_price"] * 100).round(2)

    # Reconcile revenue = units * selling_price
    df["revenue"] = (df["units"] * df["selling_price"]).round(2)

    # Reconcile gross_profit = revenue - variable_cost
    df["gross_profit"] = (df["revenue"] - df["variable_cost"]).round(2)

    # 6. Outlier Flagging (>500 units)
    df["is_outlier"] = (df["units"] > 500).astype(int)

    os.makedirs(processed_dir, exist_ok=True)
    out_path = os.path.join(processed_dir, "transactions_cleaned.csv")
    df.to_csv(out_path, index=False)

    print(f"Cleaned dataset saved: {out_path} ({len(df):,} records)")
    return df

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    clean_transactions(raw_dir, processed_dir)

if __name__ == "__main__":
    main()
