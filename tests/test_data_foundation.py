"""
Unit tests for Phase 2 Data Foundation pipeline scripts (01_generate, 02_validate, 03_clean, 04_build).
"""

import os
import pandas as pd
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(REPO_ROOT, "data", "processed")

def test_raw_files_generated():
    expected_files = [
        "calendar.csv", "regions.csv", "channels.csv",
        "promotions.csv", "products.csv", "customers.csv", "transactions_raw.csv"
    ]
    for f in expected_files:
        assert os.path.exists(os.path.join(RAW_DIR, f)), f"Missing raw file: {f}"

def test_analytical_dataset_schema():
    mart_path = os.path.join(PROCESSED_DIR, "analytical_dataset.csv")
    assert os.path.exists(mart_path), "Analytical dataset CSV missing."
    df = pd.read_csv(mart_path)
    
    assert len(df) == 60000, f"Expected 60,000 cleaned transactions, got {len(df)}"
    
    required_cols = [
        "transaction_id", "date", "customer_id", "product_id", "category",
        "region", "channel", "units", "list_price", "selling_price",
        "discount", "discount_pct", "revenue", "variable_cost", "gross_profit",
        "gross_margin_pct", "promotion_flag", "promotion_type", "customer_segment"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column in analytical dataset: {col}"

def test_reconciliation_math():
    mart_path = os.path.join(PROCESSED_DIR, "analytical_dataset.csv")
    df = pd.read_csv(mart_path)
    
    # Revenue = units * selling_price
    expected_rev = (df["units"] * df["selling_price"]).round(2)
    rev_diff = (df["revenue"] - expected_rev).abs()
    assert (rev_diff <= 0.05).all(), "Revenue reconciliation math failed in cleaned analytical dataset."

    # Gross profit = revenue - variable_cost
    expected_gp = (df["revenue"] - df["variable_cost"]).round(2)
    gp_diff = (df["gross_profit"] - expected_gp).abs()
    assert (gp_diff <= 0.05).all(), "Gross profit reconciliation math failed in cleaned analytical dataset."

def test_no_null_critical_fields():
    mart_path = os.path.join(PROCESSED_DIR, "analytical_dataset.csv")
    df = pd.read_csv(mart_path)
    
    critical_cols = ["transaction_id", "revenue", "gross_profit", "variable_cost", "category", "customer_segment"]
    for col in critical_cols:
        assert df[col].isnull().sum() == 0, f"Unresolved null values found in critical column: {col}"
