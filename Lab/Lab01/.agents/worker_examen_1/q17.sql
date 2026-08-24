SELECT
    c.company_name,
    o.order_id,
    o.order_date,
    o.freight
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date = (
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
)
ORDER BY o.order_date DESC
LIMIT 10;