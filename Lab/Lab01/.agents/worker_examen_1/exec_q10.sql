SELECT
    c.customer_id,
    c.company_name,
    c.city,
    c.country
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;