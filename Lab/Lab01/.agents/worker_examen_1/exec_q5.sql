SELECT
    p.category_id,
    SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso_total
FROM order_details od
INNER JOIN products p ON od.product_id = p.product_id
GROUP BY p.category_id
HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 10000
ORDER BY ingreso_total DESC;