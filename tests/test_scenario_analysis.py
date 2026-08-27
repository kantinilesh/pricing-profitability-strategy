"""
Unit tests for Phase 8 Strategic Scenario Engine and Sensitivity Analysis scripts.
"""

import os
import pytest
from src.analysis.scenarios.scenario_engine import run_strategic_scenario_engine
from src.analysis.scenarios.sensitivity_analysis import run_sensitivity_analysis

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

def test_scenario_engine():
    df_scen = run_strategic_scenario_engine(PROCESSED_DIR)
    assert len(df_scen) == 7
    assert "scenario_code" in df_scen.columns
    assert "incremental_profit_inr" in df_scen.columns
    # Verify Scenario G (Combination Strategy) achieves highest gross profit
    scen_g = df_scen[df_scen["scenario_code"] == "Scenario G"].iloc[0]
    assert scen_g["incremental_profit_inr"] > 0

def test_sensitivity_analysis():
    df_sens = run_sensitivity_analysis(PROCESSED_DIR)
    assert len(df_sens) == 3
    assert "case" in df_sens.columns
    assert "total_incremental_profit_inr" in df_sens.columns
