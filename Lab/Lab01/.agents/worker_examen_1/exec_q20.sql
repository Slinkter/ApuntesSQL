WITH ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY DATE_TRUNC('month', o.order_date)
)
SELECT
    mes,
    ROUND(ventas::numeric, 2) AS ventas_totales,
    ROUND(AVG(ventas) OVER (
        ORDER BY mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS promedio_movil_3m,
    CASE
        WHEN ventas > AVG(ventas) OVER (
            ORDER BY mes
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) THEN 'Por encima'
        ELSE 'Por debajo'
    END AS tendencia
FROM ventas_mensuales
ORDER BY mes
LIMIT 12;