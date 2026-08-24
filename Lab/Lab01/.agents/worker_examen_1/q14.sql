SELECT
    p.product_name,
    p.unit_price,
    c.category_name,
    sub.precio_promedio_categoria
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
INNER JOIN (
    SELECT category_id, AVG(unit_price) AS precio_promedio_categoria
    FROM products
    GROUP BY category_id
) sub ON p.category_id = sub.category_id
WHERE p.unit_price > sub.precio_promedio_categoria
ORDER BY c.category_name, p.unit_price DESC
LIMIT 10;