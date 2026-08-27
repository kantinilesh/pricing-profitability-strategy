"""
elasticity.py
Econometric Econometrics & Demand Response Engine.
Fits Log-Log OLS Regressions (ln Q = alpha + beta * ln Realized Price + Control Variables) per category,
evaluates price elasticity coefficients, and documents model specifications, confounders, and limitations.
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

def estimate_category_elasticities(processed_dir):
    df = pd.read_csv(os.path.join(processed_dir, "analytical_dataset.csv"))

    # Prepare log variables
    df["unit_selling_price"] = (df["revenue"] / df["units"]).clip(lower=1.0)
    df["log_units"] = np.log(df["units"].clip(lower=1))
    df["log_price"] = np.log(df["unit_selling_price"])
    df["is_promo"] = df["promotion_flag"]

    categories = df["category"].unique()
    elasticity_results = []

    for cat in categories:
        cat_df = df[df["category"] == cat].copy()
        if len(cat_df) < 50:
            continue

        X = cat_df[["log_price", "is_promo", "is_weekend"]]
        X = sm.add_constant(X)
        y = cat_df["log_units"]

        model = sm.OLS(y, X).fit()

        beta = round(model.params["log_price"], 3)
        se = round(model.bse["log_price"], 3)
        p_val = round(model.pvalues["log_price"], 4)
        r_sq = round(model.rsquared, 3)

        if beta < -1.5:
            classification = "Highly Elastic (Price Sensitive)"
        elif beta < -1.0:
            classification = "Elastic"
        elif beta < -0.5:
            classification = "Inelastic (Moderate Pricing Power)"
        else:
            classification = "Highly Inelastic (Strong Pricing Power)"

        elasticity_results.append({
            "category": cat,
            "sample_size": len(cat_df),
            "elasticity_beta": beta,
            "std_error": se,
            "p_value": p_val,
            "r_squared": r_sq,
            "demand_classification": classification
        })

    model_metadata = {
        "model_specification": "Log-Log Ordinary Least Squares (OLS) Linear Regression",
        "formula": "ln(Units) = alpha + beta * ln(Realized_Price) + gamma_1 * IsPromo + gamma_2 * IsWeekend + epsilon",
        "dependent_variable": "ln(Units Sold)",
        "primary_independent_variable": "ln(Realized Unit Selling Price in INR)",
        "control_variables": ["IsPromo (Binary flag for campaign discount)", "IsWeekend (Binary flag for Saturday/Sunday)"],
        "assumptions": [
            "Constant elasticity functional form over historical price variation range.",
            "Independent and identically distributed transaction residuals after control conditioning."
        ],
        "limitations_and_confounders": [
            "Correlation vs Causation: Price elasticity reflects observed historical transaction correlation rather than pure randomized A/B price test causality.",
            "Omitted Variable Bias: Unobserved competitor price promotions or local store marketing events may distort price sensitivity.",
            "Endogeneity: Discretionary store markdowns may be triggered when inventory velocity slows down."
        ]
    }

    return pd.DataFrame(elasticity_results), model_metadata

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
    df_eps, meta = estimate_category_elasticities(processed_dir)

    print("=== ESTIMATED CATEGORY PRICE ELASTICITIES ===")
    print(df_eps.to_string())

    print("\n=== MODEL SPECIFICATION & LIMITATIONS ===")
    print(f"Model: {meta['model_specification']}")
    print(f"Formula: {meta['formula']}")
    print("Confounders & Limitations:")
    for lim in meta["limitations_and_confounders"]:
        print(f"  • {lim}")

if __name__ == "__main__":
    main()
