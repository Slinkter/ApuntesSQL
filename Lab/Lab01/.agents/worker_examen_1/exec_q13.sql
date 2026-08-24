WITH metricas_cliente AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS total_pedidos,
        MIN(o.order_date) AS primer_pedido,
        MAX(o.order_date) AS ultimo_pedido
    FROM orders o
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT o.order_id) > 5
),
producto_mas_caro AS (
    SELECT DISTINCT ON (o.customer_id)
        o.customer_id,
        p.product_name,
        od.unit_price
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    INNER JOIN products p ON od.product_id = p.product_id
    ORDER BY o.customer_id, od.unit_price DESC
)
SELECT
    c.company_name,
    mc.total_pedidos,
    mc.primer_pedido,
    mc.ultimo_pedido,
    pcm.product_name AS producto_mas_caro,
    pcm.unit_price AS precio
FROM metricas_cliente mc
INNER JOIN customers c ON mc.customer_id = c.customer_id
LEFT JOIN producto_mas_caro pcm ON mc.customer_id = pcm.customer_id
ORDER BY mc.total_pedidos DESC
LIMIT 10;