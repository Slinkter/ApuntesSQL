WITH ventas_producto AS (
    SELECT
        c.category_name,
        p.product_name,
        SUM(od.quantity) AS unidades_vendidas
    FROM order_details od
    INNER JOIN products p ON od.product_id = p.product_id
    INNER JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.category_name, p.product_name
)
SELECT
    category_name,
    product_name,
    unidades_vendidas,
    ROW_NUMBER() OVER (
        PARTITION BY category_name
        ORDER BY unidades_vendidas DESC
    ) AS ranking
FROM ventas_producto
ORDER BY category_name, ranking
LIMIT 15;