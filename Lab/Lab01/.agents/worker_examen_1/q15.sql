SELECT
    o.customer_id,
    c.company_name,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS total_beverages
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN products p ON od.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE cat.category_name = 'Beverages'
GROUP BY o.customer_id, c.company_name
ORDER BY total_beverages DESC
LIMIT 10;