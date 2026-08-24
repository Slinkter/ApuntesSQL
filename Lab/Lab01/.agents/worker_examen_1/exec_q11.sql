SELECT
    s.company_name AS proveedor,
    s.country,
    COUNT(p.product_id) AS productos_sin_ventas
FROM suppliers s
INNER JOIN products p ON s.supplier_id = p.supplier_id
LEFT JOIN order_details od ON p.product_id = od.product_id
WHERE od.product_id IS NULL
GROUP BY s.company_name, s.country
HAVING COUNT(p.product_id) >= 1
ORDER BY productos_sin_ventas DESC;