SELECT product_name, unit_price
FROM products
WHERE LOWER(product_name) LIKE '%chocolate%';