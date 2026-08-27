"""
src/utils/helpers.py
Utility functions for currency formatting, data validation, and report printing.
"""

import os
import pandas as pd
import numpy as np

def format_inr(val):
    """Formats numeric values into Crore or Lakh INR strings."""
    if abs(val) >= 10000007:
        return f"₹{val / 10000000:.2f} Crore"
    elif abs(val) >= 100000:
        return f"₹{val / 100000:.2f} Lakh"
    else:
        return f"₹{val:,.2f}"

def format_pct(val):
    """Formats float ratios into percentage strings."""
    return f"{val:.2f}%"
