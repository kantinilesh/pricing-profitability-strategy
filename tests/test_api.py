"""
Unit tests for FastAPI endpoints across the 7 Dashboard Pages.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_filter_options():
    response = client.get("/api/v2/filters/options")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "regions" in data

def test_page1_executive_summary():
    response = client.get("/api/v2/page1/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "revenue_inr" in data

def test_page2_profitability():
    response = client.get("/api/v2/page2/profitability")
    assert response.status_code == 200
    data = response.json()
    assert "monthly_trend" in data

def test_page3_pricing():
    response = client.get("/api/v2/page3/pricing")
    assert response.status_code == 200
    data = response.json()
    assert "elasticities" in data

def test_page4_products():
    response = client.get("/api/v2/page4/products")
    assert response.status_code == 200
    data = response.json()
    assert "portfolio_summary" in data

def test_page5_customers():
    response = client.get("/api/v2/page5/customers")
    assert response.status_code == 200
    data = response.json()
    assert "matrix_summary" in data

def test_page6_promotions():
    response = client.get("/api/v2/page6/promotions")
    assert response.status_code == 200
    data = response.json()
    assert "promotions_roi" in data

def test_page7_scenarios():
    response = client.get("/api/v2/page7/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
