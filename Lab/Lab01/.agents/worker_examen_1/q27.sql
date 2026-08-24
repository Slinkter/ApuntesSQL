WITH pedidos_trimestre AS (
    SELECT o.order_id, o.customer_id, o.ship_country, o.order_date
    FROM orders o
    WHERE o.order_date >= (
        SELECT MAX(order_date) - INTERVAL '3 months' FROM orders
    )
    AND o.order_date <= (SELECT MAX(order_date) FROM orders)
),
detalle_ventas AS (
    SELECT
        pt.order_id,
        pt.customer_id,
        pt.ship_country,
        od.product_id,
        od.quantity * od.unit_price * (1 - od.discount) AS importe
    FROM pedidos_trimestre pt
    INNER JOIN order_details od ON pt.order_id = od.order_id
),
producto_top AS (
    SELECT product_id, SUM(quantity) AS total_unidades
    FROM order_details
    WHERE order_id IN (SELECT order_id FROM pedidos_trimestre)
    GROUP BY product_id
    ORDER BY total_unidades DESC
    LIMIT 1
),
pais_top AS (
    SELECT ship_country, COUNT(*) AS total
    FROM pedidos_trimestre
    GROUP BY ship_country
    ORDER BY total DESC
    LIMIT 1
)
SELECT
    (SELECT COUNT(DISTINCT order_id) FROM pedidos_trimestre) AS total_pedidos,
    (SELECT COUNT(DISTINCT customer_id) FROM pedidos_trimestre) AS total_clientes,
    (SELECT ROUND(SUM(importe)::numeric, 2) FROM detalle_ventas) AS ingreso_total,
    (SELECT ROUND((SUM(importe) / COUNT(DISTINCT order_id))::numeric, 2) FROM detalle_ventas) AS ticket_promedio,
    (SELECT product_name FROM products WHERE product_id = (SELECT product_id FROM producto_top)) AS producto_top,
    (SELECT ship_country FROM pais_top) AS pais_top;