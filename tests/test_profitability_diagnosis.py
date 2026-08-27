"""
Unit tests for Phase 4 Profitability Diagnosis scripts.
"""

import os
import pytest
from src.analysis.profitability.profitability_diagnosis import run_profitability_diagnosis
from src.analysis.profitability.profit_bridge import calculate_profit_bridge
from src.analysis.profitability.mix_analysis import run_mix_analysis
from src.analysis.profitability.driver_analysis import run_driver_analysis
from src.analysis.profitability.pareto_analysis import run_pareto_analysis

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_profitability_diagnosis():
    summary, yearly = run_profitability_diagnosis(PROCESSED_DIR)
    assert summary["2024_net_revenue"] > 0
    assert summary["2025_net_revenue"] > summary["2024_net_revenue"]
    assert len(yearly) == 2

def test_profit_bridge():
    summary, details = calculate_profit_bridge(PROCESSED_DIR)
    assert "net_profit_change" in summary
    assert len(details) > 0

def test_mix_analysis():
    mix = run_mix_analysis(PROCESSED_DIR)
    assert "product_mix" in mix
    assert "customer_mix" in mix
    assert "channel_mix" in mix

def test_driver_analysis():
    drivers = run_driver_analysis(PROCESSED_DIR)
    assert "category_costs" in drivers
    assert "channel_costs" in drivers

def test_pareto_analysis():
    summary, top_prd, bot_prd, top_cst, val_dest = run_pareto_analysis(PROCESSED_DIR)
    assert summary["total_skus"] > 0
    assert len(top_prd) > 0
    assert len(val_dest) > 0
