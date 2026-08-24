WITH metricas_generales AS (
    SELECT
        COUNT(DISTINCT o.customer_id) AS total_clientes,
        COUNT(DISTINCT o.order_id) AS total_pedidos,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ingreso_total,
        ROUND((SUM(od.quantity * od.unit_price * (1 - od.discount)) / COUNT(DISTINCT o.order_id))::numeric, 2) AS ticket_promedio
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
),
top_cliente AS (
    SELECT
        o.customer_id,
        c.company_name,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS facturacion
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    INNER JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.company_name
    ORDER BY facturacion DESC
    LIMIT 1
)
SELECT
    mg.total_clientes,
    mg.total_pedidos,
    mg.ingreso_total,
    mg.ticket_promedio,
    tc.company_name AS cliente_top,
    tc.facturacion AS facturacion_top
FROM metricas_generales mg
CROSS JOIN top_cliente tc;