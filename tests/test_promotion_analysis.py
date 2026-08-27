"""
Unit tests for Phase 6 Promotion Effectiveness scripts.
"""

import os
import pytest
from src.analysis.promotions.promotion_effectiveness import analyze_promotion_effectiveness
from src.analysis.promotions.promotion_roi import calculate_promotion_roi
from src.analysis.promotions.promotion_segmentation import run_promotion_segmentation

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_promotion_effectiveness():
    df_eff = analyze_promotion_effectiveness(PROCESSED_DIR)
    assert len(df_eff) > 0
    assert "volume_lift_pct" in df_eff.columns

def test_promotion_roi():
    df_roi = calculate_promotion_roi(PROCESSED_DIR)
    assert len(df_roi) > 0
    assert "net_incremental_promo_roi" in df_roi.columns
    assert "profitability_classification" in df_roi.columns

def test_promotion_segmentation():
    res = run_promotion_segmentation(PROCESSED_DIR)
    assert "segment_promo" in res
    assert "channel_promo" in res
    assert "category_promo" in res
