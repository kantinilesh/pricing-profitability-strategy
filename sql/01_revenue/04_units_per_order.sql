-- Business Question 17: What is the distribution of Units Per Order (UPT) across categories and channels?
-- Purpose: Measures basket depth and item velocity to guide cross-selling and threshold discount rules.

SELECT 
    t.category,
    t.channel,
    COUNT(DISTINCT t.transaction_id) AS order_count,
    SUM(t.units) AS total_units,
    ROUND(CAST(SUM(t.units) AS NUMERIC) / COUNT(DISTINCT t.transaction_id), 2) AS units_per_order,
    ROUND(SUM(t.revenue) / SUM(t.units), 2) AS average_selling_price_per_unit
FROM fact_transactions t
GROUP BY t.category, t.channel
ORDER BY units_per_order DESC;
