SELECT c.company_name, COUNT(o.order_id) AS total_pedidos
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name
ORDER BY total_pedidos DESC;