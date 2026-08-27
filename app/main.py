"""
app/main.py
FastAPI Executive Business Intelligence Dashboard API Server.
Exposes filtered analytical data endpoints for the 7 Executive Dashboard Pages:
Page 1: Executive Summary
Page 2: Profitability Diagnosis & Bridge
Page 3: Pricing Strategy & Elasticity
Page 4: Product Portfolio & Pareto
Page 5: Customer Economics & Segmentation
Page 6: Promotion Effectiveness & Trade Spend ROI
Page 7: Strategic Scenarios & Sensitivity Analysis
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Query, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.analysis.profitability.profitability_diagnosis import run_profitability_diagnosis
from src.analysis.profitability.profit_bridge import calculate_profit_bridge
from src.analysis.profitability.mix_analysis import run_mix_analysis
from src.analysis.profitability.driver_analysis import run_driver_analysis
from src.analysis.profitability.pareto_analysis import run_pareto_analysis
from src.analysis.pricing.price_waterfall import run_price_waterfall_analysis
from src.analysis.pricing.elasticity import estimate_category_elasticities
from src.analysis.pricing.price_scenarios import run_price_scenarios
from src.analysis.promotions.promotion_effectiveness import analyze_promotion_effectiveness
from src.analysis.promotions.promotion_roi import calculate_promotion_roi
from src.analysis.promotions.promotion_segmentation import run_promotion_segmentation
from src.analysis.economics.customer_economics import run_customer_segmentation
from src.analysis.economics.product_portfolio import run_product_portfolio_analysis
from src.analysis.scenarios.scenario_engine import run_strategic_scenario_engine
from src.analysis.scenarios.sensitivity_analysis import run_sensitivity_analysis
from src.analysis.rag_recommendation import rag_engine_instance

class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Executive strategy question or prompt")

PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

app = FastAPI(
    title="OmniRetail India Executive BI Dashboard API",
    description="7-Page Executive Strategy & Profitability Intelligence Platform",
    version="2.0.0"
)

def clean_dict(d):
    """Recursively converts numpy and pandas types to standard JSON types."""
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

def get_filtered_dataset(
    category: Optional[str] = None,
    region: Optional[str] = None,
    channel: Optional[str] = None,
    segment: Optional[str] = None
):
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "analytical_dataset.csv"))
    if category and category != "All":
        df = df[df["category"] == category]
    if region and region != "All":
        df = df[df["region"] == region]
    if channel and channel != "All":
        df = df[df["channel"] == channel]
    if segment and segment != "All":
        df = df[df["customer_segment"] == segment]
    return df

@app.get("/api/v1/health")
@app.get("/api/v2/health")
def health_check():
    return {"status": "healthy", "platform": "OmniRetail Executive BI Dashboard Engine", "version": "2.0.0"}

@app.get("/api/v2/filters/options")
def get_filter_options():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "analytical_dataset.csv"))
    return clean_dict({
        "categories": ["All"] + sorted(df["category"].dropna().unique().tolist()),
        "regions": ["All"] + sorted(df["region"].dropna().unique().tolist()),
        "channels": ["All"] + sorted(df["channel"].dropna().unique().tolist()),
        "segments": ["All"] + sorted(df["customer_segment"].dropna().unique().tolist())
    })

@app.get("/api/v2/page1/executive-summary")
def get_page1_summary(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    df = get_filtered_dataset(category, region, channel, segment)
    tot_rev = float(df["revenue"].sum())
    tot_gp = float(df["gross_profit"].sum())
    tot_units = int(df["units"].sum())
    margin = round((tot_gp / tot_rev * 100), 2) if tot_rev > 0 else 0.0

    return clean_dict({
        "title": "Operating Margin Compressed by 240 bps Despite 18.4% Revenue Growth",
        "revenue_inr": tot_rev,
        "gross_profit_inr": tot_gp,
        "units_sold": tot_units,
        "gross_margin_pct": margin,
        "major_change": "Variable costs expanded +23.1% YoY, outpacing +18.4% top-line revenue growth.",
        "top_driver": "Volume shift toward low-margin Consumer Electronics (0.74% gross margin) & un-capped B2B discounts.",
        "key_recommendation": "Execute Full Transformation Scenario G to recover +359 bps (+₹19.12 Crore profit)."
    })

@app.get("/api/v2/page2/profitability")
def get_page2_profitability(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    df = get_filtered_dataset(category, region, channel, segment)
    
    monthly = df.groupby(["year", "month", "month_name"]).agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    monthly["margin_pct"] = (monthly["gross_profit"] / monthly["revenue"] * 100).round(2)

    cat_prof = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    cat_prof["margin_pct"] = (cat_prof["gross_profit"] / cat_prof["revenue"] * 100).round(2)

    reg_prof = df.groupby("region").agg(
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    ).reset_index()
    reg_prof["margin_pct"] = (reg_prof["gross_profit"] / reg_prof["revenue"] * 100).round(2)

    return clean_dict({
        "title": "Profit Erosion is Driven by Price-Volume-Mix Leakage and Regional Logistics Overruns",
        "monthly_trend": monthly.to_dict(orient="records"),
        "category_profitability": cat_prof.to_dict(orient="records"),
        "region_profitability": reg_prof.to_dict(orient="records")
    })

@app.get("/api/v2/page3/pricing")
def get_page3_pricing(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    df = get_filtered_dataset(category, region, channel, segment)
    
    avg_list = (df["list_price"] * df["units"]).sum() / df["units"].sum()
    avg_selling = df["revenue"].sum() / df["units"].sum()
    disc_rate = ((avg_list - avg_selling) / avg_list) * 100

    df_eps, meta = estimate_category_elasticities(PROCESSED_DIR)

    return clean_dict({
        "title": "Uncaptured Pricing Power Exists in Price-Inelastic Home & Kitchen SKUs",
        "avg_list_price_inr": round(avg_list, 2),
        "avg_realized_price_inr": round(avg_selling, 2),
        "aggregate_discount_rate_pct": round(disc_rate, 2),
        "elasticities": df_eps.to_dict(orient="records")
    })

@app.get("/api/v2/page4/products")
def get_page4_products(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    df_prd, summary = run_product_portfolio_analysis(PROCESSED_DIR)
    return clean_dict({
        "title": "Top 20% SKUs Generate 75.7% of Profit While 35 Dog SKUs Dilute Margin",
        "portfolio_summary": summary.to_dict(orient="records"),
        "top_skus": df_prd.sort_values(by="total_gross_profit", ascending=False).head(10).to_dict(orient="records")
    })

@app.get("/api/v2/page5/customers")
def get_page5_customers(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    cust_df, summary = run_customer_segmentation(PROCESSED_DIR)
    return clean_dict({
        "title": "84 B2B Accounts Destroy ₹7.08 Crore Profit Due to Un-Capped Contract Discounts",
        "matrix_summary": summary.to_dict(orient="records"),
        "top_customers": cust_df.sort_values(by="total_gross_profit", ascending=False).head(10).to_dict(orient="records")
    })

@app.get("/api/v2/page6/promotions")
def get_page6_promotions(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    segment: Optional[str] = Query(None)
):
    df_roi = calculate_promotion_roi(PROCESSED_DIR)
    return clean_dict({
        "title": "End of Season Clearance Markdowns Operate at -1.88x Negative ROI",
        "promotions_roi": df_roi.to_dict(orient="records")
    })

@app.get("/api/v2/page7/scenarios")
def get_page7_scenarios():
    df_scen = run_strategic_scenario_engine(PROCESSED_DIR)
    df_sens = run_sensitivity_analysis(PROCESSED_DIR)
    return clean_dict({
        "title": "Full Transformation Scenario G Recovers +359 bps (+₹19.12 Crore) Net Profit",
        "scenarios": df_scen.to_dict(orient="records"),
        "sensitivity": df_sens.to_dict(orient="records")
    })

# RAG Recommendation Engine Endpoints
@app.get("/api/v2/rag/prompts")
def get_rag_prompts():
    return clean_dict(rag_engine_instance.get_preset_prompts())

@app.post("/api/v2/rag/recommend")
def post_rag_recommendation(payload: RAGQueryRequest):
    return clean_dict(rag_engine_instance.query(payload.query))

@app.get("/api/v2/rag/recommend")
def get_rag_recommendation(q: str = Query(..., description="Strategy query string")):
    return clean_dict(rag_engine_instance.query(q))

# SaaS Client Multi-Tenant Data Management Endpoints
TENANT_STATE = {
    "mode": "Demo Benchmark",
    "tenant_name": "OmniRetail India Benchmark",
    "total_records": 12500,
    "last_sync": "Live Benchmark"
}

ORIGINAL_DATASET_BACKUP = os.path.join(PROCESSED_DIR, "analytical_dataset_original.csv")

@app.get("/api/v2/saas/tenant-info")
def get_tenant_info():
    return clean_dict(TENANT_STATE)

@app.post("/api/v2/saas/upload-dataset")
async def upload_custom_dataset(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            return {"success": False, "message": "Only CSV files are supported."}

        # Backup original dataset on first custom upload
        dataset_path = os.path.join(PROCESSED_DIR, "analytical_dataset.csv")
        if os.path.exists(dataset_path) and not os.path.exists(ORIGINAL_DATASET_BACKUP):
            import shutil
            shutil.copy(dataset_path, ORIGINAL_DATASET_BACKUP)

        content = await file.read()
        import io
        df = pd.read_csv(io.BytesIO(content))

        # Flexible column mapping / defaults
        required_cols = ["revenue", "gross_profit", "units", "category", "region", "channel", "customer_segment"]
        for col in required_cols:
            if col not in df.columns:
                if col in ["revenue", "gross_profit", "units"]:
                    df[col] = 0.0 if col != "units" else 0
                else:
                    df[col] = "Default"

        # Save uploaded dataset
        df.to_csv(dataset_path, index=False)

        # Update Tenant State
        TENANT_STATE["mode"] = "Custom Client Workspace"
        TENANT_STATE["tenant_name"] = f"Client Workspace ({file.filename})"
        TENANT_STATE["total_records"] = len(df)
        TENANT_STATE["last_sync"] = "Just Now"

        # Re-index RAG Knowledge Base
        rag_engine_instance.reindex_dataset(df)

        tot_rev = float(df["revenue"].sum())
        tot_gp = float(df["gross_profit"].sum())

        return clean_dict({
            "success": True,
            "message": f"Dataset '{file.filename}' uploaded successfully! Analyzed {len(df):,} records.",
            "tenant_state": TENANT_STATE,
            "summary": {
                "records": len(df),
                "total_revenue_inr": tot_rev,
                "total_profit_inr": tot_gp,
                "margin_pct": round(tot_gp / tot_rev * 100, 2) if tot_rev > 0 else 0.0
            }
        })
    except Exception as e:
        return {"success": False, "message": f"Failed to parse CSV: {str(e)}"}

@app.post("/api/v2/saas/reset-demo")
def reset_to_demo_benchmark():
    dataset_path = os.path.join(PROCESSED_DIR, "analytical_dataset.csv")
    if os.path.exists(ORIGINAL_DATASET_BACKUP):
        import shutil
        shutil.copy(ORIGINAL_DATASET_BACKUP, dataset_path)
    
    df = pd.read_csv(dataset_path)
    rag_engine_instance.reindex_dataset(df)

    TENANT_STATE["mode"] = "Demo Benchmark"
    TENANT_STATE["tenant_name"] = "OmniRetail India Benchmark"
    TENANT_STATE["total_records"] = len(df)
    TENANT_STATE["last_sync"] = "Live Benchmark"

    return clean_dict({
        "success": True,
        "message": "Reset to OmniRetail India Benchmark dataset.",
        "tenant_state": TENANT_STATE
    })


# Serve Static Assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "OmniRetail India 7-Page Executive BI Dashboard API is running."}
