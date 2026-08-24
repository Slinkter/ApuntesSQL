SELECT
    order_id,
    ship_name,
    freight,
    ship_country
FROM orders
ORDER BY freight DESC NULLS LAST
LIMIT 10;