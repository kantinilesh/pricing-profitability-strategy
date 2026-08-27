-- Business Question 1: What is the monthly top-line net revenue trend across the 24-month horizon?
-- Purpose: Evaluates top-line growth trajectory, MoM velocity, and seasonality spikes (e.g. Oct-Nov festive surge).

SELECT 
    cal.year,
    cal.month,
    cal.month_name,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    SUM(t.units) AS total_units_sold,
    ROUND(SUM(t.revenue), 2) AS monthly_net_revenue_inr,
    ROUND(AVG(t.revenue), 2) AS avg_transaction_revenue_inr,
    ROUND(
        (SUM(t.revenue) - LAG(SUM(t.revenue)) OVER (ORDER BY cal.year, cal.month)) 
        / NULLIF(LAG(SUM(t.revenue)) OVER (ORDER BY cal.year, cal.month), 0) * 100, 2
    ) AS mom_revenue_growth_pct
FROM fact_transactions t
JOIN dim_calendar cal ON t.date = cal.date
GROUP BY cal.year, cal.month, cal.month_name
ORDER BY cal.year, cal.month;
