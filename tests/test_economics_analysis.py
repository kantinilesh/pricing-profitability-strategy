"""
Unit tests for Phase 7 Customer and Product Economics scripts.
"""

import os
import pytest
from src.analysis.economics.customer_economics import run_customer_segmentation
from src.analysis.economics.product_portfolio import run_product_portfolio_analysis

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_customer_economics():
    cust_df, summary = run_customer_segmentation(PROCESSED_DIR)
    assert len(cust_df) > 0
    assert "value_matrix_segment" in cust_df.columns
    assert len(summary) == 4

def test_product_portfolio():
    prd_df, summary = run_product_portfolio_analysis(PROCESSED_DIR)
    assert len(prd_df) > 0
    assert "portfolio_archetype" in prd_df.columns
    assert len(summary) > 0
