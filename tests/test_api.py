"""
Unit tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_waterfall_endpoint():
    response = client.get("/api/v1/waterfall")
    assert response.status_code == 200
    data = response.json()
    assert "gross_revenue" in data
    assert "pocket_profit" in data

def test_elasticity_endpoint():
    response = client.get("/api/v1/elasticity")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) > 0

def test_whale_curve_endpoint():
    response = client.get("/api/v1/whale-curve")
    assert response.status_code == 200
    data = response.json()
    assert "whale_curve" in data

def test_simulate_endpoint():
    payload = {
        "inelastic_price_increase_pct": 5.0,
        "b2b_discount_cap_pct": 18.0,
        "eliminate_eoss_markdowns": True
    }
    response = client.post("/api/v1/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["simulated_pocket_margin_pct"] > data["baseline_pocket_margin_pct"]
