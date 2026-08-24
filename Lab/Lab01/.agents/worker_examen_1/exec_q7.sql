SELECT
    c.category_name,
    COUNT(p.product_id) AS total_productos,
    COUNT(*) FILTER (WHERE p.units_in_stock < 20) AS stock_bajo,
    ROUND(AVG(p.unit_price)::numeric, 2) AS precio_promedio,
    MAX(p.unit_price) AS precio_maximo
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
HAVING COUNT(p.product_id) >= 3
ORDER BY total_productos DESC;