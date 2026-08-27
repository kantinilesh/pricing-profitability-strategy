-- Business Question 20: What is the 24-month trend of Revenue vs Gross Profit vs Margin %?
-- Purpose: Provides executive visibility into top-line revenue vs bottom-line profit divergence over 8 quarters.

SELECT 
    cal.year,
    cal.quarter,
    cal.month,
    cal.month_name,
    ROUND(SUM(t.revenue), 2) AS net_revenue_inr,
    ROUND(SUM(t.gross_profit), 2) AS gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
    ROUND(AVG(t.discount_pct), 2) AS avg_discount_pct
FROM fact_transactions t
JOIN dim_calendar cal ON t.date = cal.date
GROUP BY cal.year, cal.quarter, cal.month, cal.month_name
ORDER BY cal.year, cal.month;
