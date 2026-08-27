"""
Unit tests for ETL pipeline, data quality checks, and data mart integrity.
"""

import os
import json
import pandas as pd
import pytest

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_raw_files_exist():
    expected_files = [
        "dim_products.csv", "dim_customers.csv", "dim_stores.csv",
        "dim_promotions.csv", "fact_transactions.csv", "fact_competitor_prices.csv"
    ]
    for fname in expected_files:
        assert os.path.exists(os.path.join(RAW_DIR, fname)), f"Missing raw file: {fname}"

def test_data_quality_report():
    report_path = os.path.join(PROCESSED_DIR, "data_quality_report.json")
    assert os.path.exists(report_path), "Data quality report missing."
    with open(report_path) as f:
        data = json.load(f)
    assert data["overall_pass"] is True, f"Data quality check failed: {data}"

def test_analytical_marts_exist():
    expected_marts = [
        "analytical_transaction_fact.csv",
        "product_margin_mart.csv",
        "customer_profitability_mart.csv",
        "promo_performance_mart.csv",
        "channel_region_mart.csv"
    ]
    for mname in expected_marts:
        path = os.path.join(PROCESSED_DIR, mname)
        assert os.path.exists(path), f"Missing data mart: {mname}"
        df = pd.read_csv(path)
        assert len(df) > 0, f"Data mart {mname} is empty."

def test_revenue_and_discount_math():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "analytical_transaction_fact.csv"))
    # Check gross - total discount = net revenue
    expected_net = (df["gross_revenue_inr"] - df["total_discount_inr"]).round(2)
    diff = (df["net_revenue_inr"] - expected_net).abs()
    assert (diff <= 0.05).all(), "Net revenue math mismatch in transaction mart."

def test_pocket_profit_calculation():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "analytical_transaction_fact.csv"))
    # Net Rev - COGS - Fulfillment - Return Cost + Vendor Coop = Pocket Profit
    calc_pocket = (df["net_revenue_inr"] - df["base_cogs_inr"] - df["fulfillment_cost_inr"] - df["return_cost_inr"] + df["vendor_coop_rebate_inr"]).round(2)
    diff = (df["pocket_profit_inr"] - calc_pocket).abs()
    assert (diff <= 0.05).all(), "Pocket profit calculation mismatch in transaction mart."
