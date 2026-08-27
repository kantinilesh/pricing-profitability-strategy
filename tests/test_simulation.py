"""
Unit tests for Scenario Engine & Strategic Simulations.
"""

import os
import pytest
from src.simulation.scenario_engine import ScenarioEngine

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_scenario_engine_baseline():
    engine = ScenarioEngine(PROCESSED_DIR)
    baseline = engine.run_baseline()
    assert baseline["baseline_net_revenue"] > 0
    assert baseline["baseline_pocket_profit"] > 0

def test_full_strategic_transformation():
    engine = ScenarioEngine(PROCESSED_DIR)
    results = engine.run_full_strategic_transformation()
    comb = results["combined_transformation"]
    assert comb["new_pocket_profit"] > results["baseline"]["baseline_pocket_profit"]
    assert comb["total_margin_expansion_bps"] > 0
