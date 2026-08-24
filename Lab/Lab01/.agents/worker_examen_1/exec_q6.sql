SELECT
    s.company_name AS transportista,
    COUNT(o.order_id) AS total_pedidos,
    ROUND(AVG(o.freight)::numeric, 2) AS flete_promedio
FROM orders o
INNER JOIN shippers s ON o.ship_via = s.shipper_id
GROUP BY s.company_name
HAVING AVG(o.freight) > 50
ORDER BY flete_promedio DESC;