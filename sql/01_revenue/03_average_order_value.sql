-- Business Question 16: What is the Average Order Value (AOV) across customer segments and channels?
-- Purpose: Evaluates basket size economics to identify low-AOV transactions operating at negative unit margins.

SELECT 
    t.channel,
    t.customer_segment,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    ROUND(SUM(t.revenue), 2) AS total_revenue_inr,
    ROUND(SUM(t.revenue) / COUNT(DISTINCT t.transaction_id), 2) AS average_order_value_inr,
    ROUND(AVG(t.units), 2) AS avg_units_per_order
FROM fact_transactions t
GROUP BY t.channel, t.customer_segment
ORDER BY average_order_value_inr DESC;
