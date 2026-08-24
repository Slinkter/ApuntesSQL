SELECT
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE unit_price > 20
  AND discontinued = 0
ORDER BY unit_price DESC;