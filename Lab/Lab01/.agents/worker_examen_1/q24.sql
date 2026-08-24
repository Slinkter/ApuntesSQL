WITH precios_actuales AS (
    SELECT
        product_id,
        product_name,
        unit_price AS precio_actual
    FROM products
    WHERE discontinued = 0
),
precios_simulados AS (
    SELECT
        product_id,
        ROUND((precio_actual * 1.10)::numeric, 2) AS precio_simulado
    FROM precios_actuales
)
SELECT
    pa.product_name,
    pa.precio_actual,
    ps.precio_simulado,
    ROUND((ps.precio_simulado - pa.precio_actual)::numeric, 2) AS diferencia
FROM precios_actuales pa
INNER JOIN precios_simulados ps ON pa.product_id = ps.product_id
ORDER BY diferencia DESC
LIMIT 10;