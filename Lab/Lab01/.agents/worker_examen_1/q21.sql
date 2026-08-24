WITH ventas_cliente_mes AS (
    SELECT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.customer_id, DATE_TRUNC('month', o.order_date)
)
SELECT
    c.company_name,
    vcm.mes,
    ROUND(vcm.ventas::numeric, 2) AS ventas_mes,
    ROUND(SUM(vcm.ventas) OVER (
        PARTITION BY vcm.customer_id
        ORDER BY vcm.mes
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ventas_acumuladas
FROM ventas_cliente_mes vcm
INNER JOIN customers c ON vcm.customer_id = c.customer_id
ORDER BY c.company_name, vcm.mes
LIMIT 12;