"""
Data Quality Validation Engine.
Performs automated checks on raw data files to enforce schema integrity,
null constraints, logical business rules, and numerical boundary conditions.
"""

import os
import json
import pandas as pd

class DataValidator:
    def __init__(self, raw_data_dir):
        self.raw_data_dir = raw_data_dir
        self.audit_results = {}

    def validate_all(self):
        print("Running Data Quality Validation Checks...")
        self.audit_results["products"] = self._check_products()
        self.audit_results["customers"] = self._check_customers()
        self.audit_results["stores"] = self._check_stores()
        self.audit_results["promotions"] = self._check_promotions()
        self.audit_results["transactions"] = self._check_transactions()
        self.audit_results["competitors"] = self._check_competitors()
        
        overall_pass = all(res["passed"] for res in self.audit_results.values())
        self.audit_results["overall_pass"] = overall_pass
        return self.audit_results

    def _check_products(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "dim_products.csv"))
        errors = []
        if df["product_id"].duplicated().any():
            errors.append("Duplicate product_id found.")
        if df["list_price_inr"].min() <= 0:
            errors.append("Non-positive list prices detected.")
        if (df["list_price_inr"] < df["base_cogs_inr"]).any():
            errors.append("Base COGS exceeds List Price for some SKUs.")
        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

    def _check_customers(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "dim_customers.csv"))
        errors = []
        if df["customer_id"].duplicated().any():
            errors.append("Duplicate customer_id found.")
        if df["contract_discount_pct"].min() < 0 or df["contract_discount_pct"].max() > 0.5:
            errors.append("Contract discount out of valid range [0, 0.5].")
        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

    def _check_stores(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "dim_stores.csv"))
        errors = []
        if df["store_id"].duplicated().any():
            errors.append("Duplicate store_id found.")
        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

    def _check_promotions(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "dim_promotions.csv"))
        errors = []
        if df["promo_id"].duplicated().any():
            errors.append("Duplicate promo_id found.")
        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

    def _check_transactions(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "fact_transactions.csv"))
        errors = []
        if df["transaction_id"].duplicated().any():
            errors.append("Duplicate transaction_id found.")
        if (df["gross_revenue_inr"] < 0).any():
            errors.append("Negative gross revenue detected.")
        if (df["net_revenue_inr"] > df["gross_revenue_inr"]).any():
            errors.append("Net revenue exceeds gross revenue.")
        if (df["total_discount_inr"] < 0).any():
            errors.append("Negative total discount detected.")
        
        # Verify Revenue Math
        calc_net = (df["gross_revenue_inr"] - df["total_discount_inr"]).round(2)
        diff = (df["net_revenue_inr"] - calc_net).abs()
        if (diff > 0.05).any():
            errors.append("Net revenue math mismatch in transactions.")

        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

    def _check_competitors(self):
        df = pd.read_csv(os.path.join(self.raw_data_dir, "fact_competitor_prices.csv"))
        errors = []
        if (df["competitor_price_inr"] <= 0).any():
            errors.append("Non-positive competitor prices detected.")
        return {"passed": len(errors) == 0, "rows": len(df), "errors": errors}

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    validator = DataValidator(raw_dir)
    results = validator.validate_all()
    
    report_path = os.path.join(processed_dir, "data_quality_report.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Data Quality Report Generated: {report_path}")
    print(f"Overall Quality Status: {'PASSED' if results['overall_pass'] else 'FAILED'}")

if __name__ == "__main__":
    main()
