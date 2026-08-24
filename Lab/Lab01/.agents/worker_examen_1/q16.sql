SELECT
    p.product_name,
    p.unit_price,
    c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
WHERE p.unit_price > ALL (
    SELECT p2.unit_price
    FROM products p2
    INNER JOIN categories c2 ON p2.category_id = c2.category_id
    WHERE c2.category_name = 'Beverages'
)
ORDER BY p.unit_price DESC;