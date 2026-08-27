-- Business Question 15: What is the monthly breakdown of revenue from New vs Repeat customer orders?
-- Purpose: Measures acquisition vs retention monthly revenue momentum.

WITH customer_first_order AS (
    SELECT 
        customer_id,
        MIN(date) AS first_order_date
    FROM fact_transactions
    GROUP BY customer_id
)
SELECT 
    cal.year,
    cal.month,
    cal.month_name,
    SUM(CASE WHEN t.date = cfo.first_order_date THEN t.revenue ELSE 0 END) AS new_customer_revenue_inr,
    SUM(CASE WHEN t.date > cfo.first_order_date THEN t.revenue ELSE 0 END) AS repeat_customer_revenue_inr,
    ROUND(
        SUM(CASE WHEN t.date > cfo.first_order_date THEN t.revenue ELSE 0 END) * 100.0 
        / NULLIF(SUM(t.revenue), 0), 2
    ) AS repeat_revenue_share_pct
FROM fact_transactions t
JOIN dim_calendar cal ON t.date = cal.date
JOIN customer_first_order cfo ON t.customer_id = cfo.customer_id
GROUP BY cal.year, cal.month, cal.month_name
ORDER BY cal.year, cal.month;
