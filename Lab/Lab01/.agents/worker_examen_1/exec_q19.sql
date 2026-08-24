WITH ventas_mensuales AS (
    SELECT
        o.employee_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.employee_id, DATE_TRUNC('month', o.order_date)
),
con_lag AS (
    SELECT
        employee_id,
        mes,
        ventas,
        LAG(ventas) OVER (PARTITION BY employee_id ORDER BY mes) AS ventas_anterior
    FROM ventas_mensuales
)
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    cl.mes,
    ROUND(cl.ventas::numeric, 2) AS ventas_mes,
    ROUND(cl.ventas_anterior::numeric, 2) AS ventas_anterior,
    ROUND(((cl.ventas - cl.ventas_anterior) / NULLIF(cl.ventas_anterior, 0) * 100)::numeric, 2) AS variacion_pct
FROM con_lag cl
INNER JOIN employees e ON cl.employee_id = e.employee_id
WHERE cl.ventas_anterior IS NOT NULL
ORDER BY empleado, cl.mes
LIMIT 10;