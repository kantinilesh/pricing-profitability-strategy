"""
Econometric Pricing & Elasticity Engine.
Estimates price elasticity of demand using Log-Log OLS Regression,
classifies SKU price sensitivity, and calculates optimal margin-maximizing price points.
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

class PricingElasticityEngine:
    def __init__(self, processed_dir):
        self.processed_dir = processed_dir
        self.df_fact = pd.read_csv(os.path.join(processed_dir, "analytical_transaction_fact.csv"))
        self.df_prod = pd.read_csv(os.path.join(processed_dir, "product_margin_mart.csv"))

    def estimate_category_elasticities(self):
        """
        Runs Category-level Log-Log OLS Regression to estimate price elasticity (\epsilon).
        Formula: ln(Quantity) = \alpha + \beta * ln(Effective Price) + Control Dummy (Promo)
        """
        results = []
        
        # Compute effective unit price per transaction
        self.df_fact["unit_effective_price"] = (self.df_fact["net_revenue_inr"] / self.df_fact["quantity"]).clip(lower=1.0)
        self.df_fact["log_qty"] = np.log(self.df_fact["quantity"].clip(lower=1))
        self.df_fact["log_price"] = np.log(self.df_fact["unit_effective_price"])
        self.df_fact["is_promo"] = (self.df_fact["promo_id"] != "PROMO_NONE").astype(int)

        categories = self.df_fact["category"].unique()
        for cat in categories:
            cat_df = self.df_fact[self.df_fact["category"] == cat].copy()
            if len(cat_df) < 50:
                continue

            X = cat_df[["log_price", "is_promo"]]
            X = sm.add_constant(X)
            y = cat_df["log_qty"]

            model = sm.OLS(y, X).fit()
            elasticity = round(model.params["log_price"], 3)
            p_value = round(model.pvalues["log_price"], 4)
            r_squared = round(model.rsquared, 3)

            sensitivity = "Highly Elastic" if elasticity < -1.5 else ("Elastic" if elasticity < -1.0 else "Inelastic")

            results.append({
                "category": cat,
                "price_elasticity": elasticity,
                "p_value": p_value,
                "r_squared": r_squared,
                "sensitivity_classification": sensitivity,
                "transaction_count": len(cat_df)
            })

        return pd.DataFrame(results)

    def calculate_optimal_prices(self):
        """
        Calculates optimal list price P* based on microeconomic margin optimization formula:
        P* = COGS * ( \epsilon / (1 + \epsilon) ) for elastic SKUs,
        and recommended price hikes for inelastic SKUs.
        """
        cat_elasticities = self.estimate_category_elasticities().set_index("category")["price_elasticity"].to_dict()

        df_opt = self.df_prod.copy()
        
        def optimize_sku(row):
            cat = row["category"]
            eps = cat_elasticities.get(cat, -1.2)
            cogs = row["base_cogs_inr"]
            curr_price = row["list_price_inr"]
            comp_index = row["avg_competitor_price_index"]

            if eps < -1.0:
                # Standard Lerner Index optimal price
                opt_price = cogs * (eps / (1.0 + eps))
                # Bound change within realistic retail limits [-15%, +15%]
                opt_price = max(curr_price * 0.85, min(curr_price * 1.15, opt_price))
            else:
                # Inelastic SKU - room for price increase (especially if competitors are higher)
                if comp_index < 1.0:  # OmniRetail is cheaper than competitors
                    hike_pct = 0.06
                else:
                    hike_pct = 0.03
                opt_price = curr_price * (1 + hike_pct)

            opt_price = round(opt_price, 2)
            price_change_pct = round(((opt_price - curr_price) / curr_price) * 100, 2)

            return pd.Series([eps, opt_price, price_change_pct], index=["estimated_elasticity", "optimal_price_inr", "recommended_price_change_pct"])

        opt_cols = df_opt.apply(optimize_sku, axis=1)
        df_res = pd.concat([df_opt, opt_cols], axis=1)
        return df_res

def main():
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    engine = PricingElasticityEngine(processed_dir)
    df_cat_eps = engine.estimate_category_elasticities()
    print("--- CATEGORY PRICE ELASTICITIES ---")
    print(df_cat_eps.to_string())

    df_opt = engine.calculate_optimal_prices()
    print("\n--- SAMPLE SKU OPTIMAL PRICES ---")
    print(df_opt[["sku_code", "category", "list_price_inr", "optimal_price_inr", "recommended_price_change_pct", "avg_competitor_price_index"]].head(10).to_string())

if __name__ == "__main__":
    main()
