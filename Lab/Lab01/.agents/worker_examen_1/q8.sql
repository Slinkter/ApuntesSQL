WITH ingresos_trimestre AS (
    SELECT
        EXTRACT(QUARTER FROM o.order_date) AS trimestre,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    WHERE EXTRACT(YEAR FROM o.order_date) = 1997
    GROUP BY EXTRACT(QUARTER FROM o.order_date)
)
SELECT
    'Q' || trimestre::text AS trimestre,
    ROUND(ingreso::numeric, 2) AS ingreso_total,
    ROUND((ingreso / SUM(ingreso) OVER () * 100)::numeric, 2) AS porcentaje
FROM ingresos_trimestre
ORDER BY trimestre;