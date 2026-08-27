-- Business Question 4: How is total net revenue distributed across Product Categories?
-- Purpose: Evaluates category scale and top-line revenue contribution.

SELECT 
    t.category,
    COUNT(DISTINCT t.product_id) AS sku_count,
    SUM(t.units) AS total_units_sold,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.revenue) * 100.0 / SUM(SUM(t.revenue)) OVER (), 2) AS category_revenue_share_pct
FROM fact_transactions t
GROUP BY t.category
ORDER BY total_net_revenue_inr DESC;
