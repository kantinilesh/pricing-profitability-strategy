"""
FastAPI Strategy & Intelligence Backend.
Exposes analytical data marts, margin waterfall metrics, econometric elasticity outputs,
and interactive scenario simulation APIs for OmniRetail India.
"""

import os
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.analytics.profitability_engine import ProfitabilityEngine
from src.analytics.pricing_elasticity import PricingElasticityEngine
from src.analytics.customer_analytics import CustomerAnalyticsEngine
from src.analytics.promo_analytics import PromotionAnalyticsEngine
from src.simulation.scenario_engine import ScenarioEngine

PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

app = FastAPI(
    title="Pricing & Profitability Intelligence Platform API",
    description="Bain & Company Case-Style Strategy Intelligence Backend for OmniRetail India",
    version="1.0.0"
)

# Instantiate engines
prof_engine = ProfitabilityEngine(PROCESSED_DIR)
elas_engine = PricingElasticityEngine(PROCESSED_DIR)
cust_engine = CustomerAnalyticsEngine(PROCESSED_DIR)
promo_engine = PromotionAnalyticsEngine(PROCESSED_DIR)
scen_engine = ScenarioEngine(PROCESSED_DIR)

def clean_dict(d):
    """Converts numpy types to standard python types for JSON serialization."""
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict(v) for v in d]
    elif isinstance(d, (np.integer, int)):
        return int(d)
    elif isinstance(d, (np.floating, float)):
        return float(d)
    elif isinstance(d, (np.bool_, bool)):
        return bool(d)
    elif pd.isna(d):
        return None
    else:
        return d

class SimulationRequest(BaseModel):
    inelastic_price_increase_pct: float = Field(default=4.0, ge=0.0, le=20.0, description="Percentage price increase on inelastic SKUs")
    b2b_discount_cap_pct: float = Field(default=18.0, ge=10.0, le=30.0, description="Max contract discount cap for B2B Enterprise accounts")
    eliminate_eoss_markdowns: bool = Field(default=True, description="Whether to eliminate negative ROI EOSS clearance markdowns")

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "platform": "Pricing & Profitability Intelligence Engine", "version": "1.0.0"}

@app.get("/api/v1/waterfall")
def get_waterfall():
    return clean_dict(prof_engine.compute_margin_waterfall())

@app.get("/api/v1/pareto")
def get_pareto():
    df = prof_engine.compute_pareto_analysis()
    return clean_dict(df.to_dict(orient="records"))

@app.get("/api/v1/elasticity")
def get_elasticity():
    df_cat = elas_engine.estimate_category_elasticities()
    df_opt = elas_engine.calculate_optimal_prices()
    return clean_dict({
        "categories": df_cat.to_dict(orient="records"),
        "top_skus": df_opt.head(20).to_dict(orient="records")
    })

@app.get("/api/v1/whale-curve")
def get_whale_curve():
    df_whale = cust_engine.compute_whale_curve()
    df_seg = cust_engine.evaluate_customer_segmentation()
    return clean_dict({
        "whale_curve": df_whale.to_dict(orient="records"),
        "segments": df_seg.to_dict(orient="records")
    })

@app.get("/api/v1/promo-roi")
def get_promo_roi():
    df_promo = promo_engine.compute_incremental_promo_roi()
    return clean_dict(df_promo.to_dict(orient="records"))

@app.get("/api/v1/strategic-transformation")
def get_strategic_transformation():
    return clean_dict(scen_engine.run_full_strategic_transformation())

@app.post("/api/v1/simulate")
def simulate_custom_scenario(req: SimulationRequest):
    baseline = scen_engine.run_baseline()
    
    # Custom price adjustment impact
    s1 = scen_engine.simulate_price_optimization()
    adj_factor = req.inelastic_price_increase_pct / 4.0
    price_profit_delta = s1["pocket_profit_impact_inr"] * adj_factor

    # Promo reallocation impact
    s2 = scen_engine.simulate_promo_reallocation() if req.eliminate_eoss_markdowns else {"pocket_profit_impact_inr": 0.0}

    # Discount governance impact
    s3 = scen_engine.simulate_discount_governance()

    total_profit_delta = price_profit_delta + s2["pocket_profit_impact_inr"] + s3["pocket_profit_impact_inr"]
    new_pocket_profit = baseline["baseline_pocket_profit"] + total_profit_delta
    new_pocket_margin_pct = round((new_pocket_profit / baseline["baseline_net_revenue"]) * 100, 2)
    margin_expansion_bps = round((new_pocket_margin_pct - baseline["baseline_pocket_margin_pct"]) * 100, 0)

    return clean_dict({
        "parameters": req.model_dump(),
        "baseline_pocket_margin_pct": baseline["baseline_pocket_margin_pct"],
        "simulated_pocket_margin_pct": new_pocket_margin_pct,
        "pocket_profit_delta_inr": round(total_profit_delta, 2),
        "margin_expansion_bps": margin_expansion_bps
    })

# Static Files for Web Dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Pricing & Profitability Intelligence Platform API is running. Access /docs for Swagger UI."}
