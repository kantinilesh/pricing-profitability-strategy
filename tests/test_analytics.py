"""
Unit tests for Core Analytical Engines: Profitability, Elasticity, Customer Analytics, and Promo ROI.
"""

import os
import pandas as pd
import pytest
from src.analytics.profitability_engine import ProfitabilityEngine
from src.analytics.pricing_elasticity import PricingElasticityEngine
from src.analytics.customer_analytics import CustomerAnalyticsEngine
from src.analytics.promo_analytics import PromotionAnalyticsEngine

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_profitability_waterfall():
    engine = ProfitabilityEngine(PROCESSED_DIR)
    waterfall = engine.compute_margin_waterfall()
    assert waterfall["gross_revenue"] > 0
    assert waterfall["pocket_profit"] > 0
    assert waterfall["gross_margin_pct"] > waterfall["pocket_margin_pct"]

def test_pareto_analysis():
    engine = ProfitabilityEngine(PROCESSED_DIR)
    pareto = engine.compute_pareto_analysis()
    assert "pareto_tier" in pareto.columns
    assert len(pareto) > 0

def test_pricing_elasticity():
    engine = PricingElasticityEngine(PROCESSED_DIR)
    df_eps = engine.estimate_category_elasticities()
    assert len(df_eps) > 0
    assert (df_eps["price_elasticity"] < 0).all(), "Price elasticity should be negative."
    
    df_opt = engine.calculate_optimal_prices()
    assert "optimal_price_inr" in df_opt.columns
    assert (df_opt["optimal_price_inr"] > 0).all()

def test_customer_whale_curve():
    engine = CustomerAnalyticsEngine(PROCESSED_DIR)
    whale = engine.compute_whale_curve()
    assert "profitability_tier" in whale.columns
    assert "Value Destroyer (Negative Profit)" in whale["profitability_tier"].values

def test_promo_incremental_roi():
    engine = PromotionAnalyticsEngine(PROCESSED_DIR)
    df_roi = engine.compute_incremental_promo_roi()
    assert "incremental_promo_roi" in df_roi.columns
    assert len(df_roi) > 0
