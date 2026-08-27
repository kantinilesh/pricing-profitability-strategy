# Pricing & Profitability Intelligence Platform
> **Bain & Company Case-Style Strategy & Analytics Engine**  
> *A portfolio-quality business analytics platform designed for an omnichannel Indian retailer experiencing revenue growth alongside margin compression.*

---

## 📌 Executive Overview & Business Case

An omnichannel Indian retail enterprise ("OmniRetail India") with 120+ physical stores and a major e-commerce channel achieved **+18.4% top-line YoY revenue growth**, but suffered a **240 bps drop in operating margins**.

Management retained our strategy team to resolve **5 Key Management Questions**:
1. **Why is profitability changing?** (Revenue & cost waterfall decomposition)
2. **Which products, customer segments, and regions drive margin leakage?** (80/20 Pareto & Cost-to-Serve)
3. **Are current prices and discounts optimal?** (Econometric price elasticity estimation)
4. **Which promotions actually generate net incremental margin?** (Baseline demand decomposition)
5. **What strategic pricing and profitability interventions should management execute?** (Scenario Engine & Actionable 30-60-90 Day Roadmap)

---

## 🧭 Bain Analytical Sequence

```mermaid
flowchart LR
    A[Business Question] --> B[MECE Structure]
    B --> C[Hypothesis Tree]
    C --> D[Data Quality ETL]
    D --> E[Econometric Analysis]
    E --> F[Validation]
    F --> G[Strategic Insights]
    G --> H[Scenario Quantification]
    H --> I[Pyramid Recommendation]
    I --> J[Implementation Roadmap]
```

---

## 📂 Repository Structure

```
pricing-profitability-strategy/
├── PROJECT_CHARTER.md          # Business Context, MECE Trees, Hypotheses & KPI Dictionary
├── README.md                   # Main Project Documentation & Setup Guide
├── data/
│   ├── raw/                    # Synthetic Indian omnichannel raw transactions & master tables
│   └── processed/              # Cleaned analytical data marts (Parquet / DuckDB / SQL)
├── src/
│   ├── etl/                    # Data quality validation & ETL engine
│   ├── analytics/              # Profitability, Pricing Elasticity, Customer & Promo engines
│   └── simulation/             # What-if Scenario Engine
├── app/                        # FastAPI backend for strategy intelligence
├── dashboards/                 # Power BI / Web executive dashboard specifications
├── tests/                      # Pytest suite for business logic & data validation
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Tech Stack & Methodology

- **Analysis & Data Pipeline**: Python, Pandas, NumPy, DuckDB / SQL
- **Econometric & Statistical Modeling**: Scikit-Learn, Statsmodels (Log-Log Price Elasticity Regression)
- **Application & API Layer**: FastAPI, Uvicorn, Pydantic
- **Dashboard & Visualization**: Interactive Web Dashboard & Power BI Specification
- **Methodological Standard**: Bain & Company MECE Problem Structuring, Pyramid Principle Communication, 80/20 Prioritization

---

## 📋 Project Roadmap

- [x] **Phase 1: Project Charter & Problem Structuring** (MECE Issue Tree, Hypothesis Tree, KPI Dictionary)
- [ ] **Phase 2: Realistic Indian Retail Data Engine** (Transactions, Products, Customers, Channels, Promos)
- [ ] **Phase 3: Data Quality Validation & ETL Mart Creation**
- [ ] **Phase 4: Core Analytical Engines** (Decomposition, Elasticity, Customer Whale Curve, Promo ROI)
- [ ] **Phase 5: Hypothesis Validation & What-If Scenario Engine**
- [ ] **Phase 6: FastAPI Application & Executive Dashboard**
- [ ] **Phase 7: Bain-Style Executive Deck & Implementation Plan**

---

## 🔬 Reproducibility & Credibility Standards
- **Zero Hallucination Policy**: All numerical conclusions are directly backed by code output.
- **Explicit Synthetic Data Flag**: Generated data is explicitly labeled as synthetic, modeled after benchmark retail economics in India.
- **Deterministic Execution**: Global random seed `42` ensures exact reproducibility across all models.
