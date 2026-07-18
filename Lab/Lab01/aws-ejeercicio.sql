SELECT
    products.product_name,
    products.unit_price,
    products.units_in_stock,
    unit_price * units_in_stock
FROM
    products;

SELECT
    SUM(unit_price * units_in_stock) as Total
FROM
    products;

/*  */
SELECT
    *
from
    categories
LIMIT
    5;

/*  */
SELECT
    *
from
    products
LIMIT
    5;

SELECT
    *
FROM
    products AS p
    INNER JOIN categories AS c ON p.category_id = c.category_id;