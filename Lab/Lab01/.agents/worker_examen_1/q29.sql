EXPLAIN (ANALYZE, COSTS OFF)
SELECT c.company_name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name;