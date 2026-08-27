"""
Unit tests for Phase 5 Pricing Strategy scripts.
"""

import os
import pytest
from src.analysis.pricing.price_waterfall import run_price_waterfall_analysis
from src.analysis.pricing.elasticity import estimate_category_elasticities
from src.analysis.pricing.price_scenarios import run_price_scenarios

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_price_waterfall():
    res = run_price_waterfall_analysis(PROCESSED_DIR)
    assert "overall_waterfall" in res
    assert res["overall_waterfall"]["avg_list_price_inr"] > res["overall_waterfall"]["avg_realized_price_inr"]
    assert len(res["segment_waterfall"]) > 0

def test_price_elasticity():
    df_eps, meta = estimate_category_elasticities(PROCESSED_DIR)
    assert len(df_eps) > 0
    assert "elasticity_beta" in df_eps.columns
    assert (df_eps["elasticity_beta"] < 0).all()
    assert "model_specification" in meta

def test_price_scenarios():
    df_scen = run_price_scenarios(PROCESSED_DIR)
    assert len(df_scen) > 0
    assert "profit_delta_inr" in df_scen.columns
    # Verify 5 scenarios per category (0%, +5%, +10%, -5%, -10%)
    sample_cat_scens = df_scen[df_scen["category"] == "Home & Kitchen"]
    assert len(sample_cat_scens) == 5
