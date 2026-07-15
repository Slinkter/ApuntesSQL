SELECT
    *
FROM
    orders
WHERE
    order_date < '1996-08-01'
ORDER BY
    order_date desc
    -- 
SELECT
    min(order_date),
    MAX(order_date)
FROM
    orders;

-- 
SELECT
    MAX(order_date) - MIN(order_date) as DIFF
FROM
    orders;

-- 10.
SELECT
    employee_id,
    last_name || ' ' || first_name,
    hire_date
FROM
    employees
ORDER BY
    hire_date asc
    -- 11.
    /* 11. */
SELECT
    customers.customer_id,
    customers.company_name,
    customers.contact_title
FROM
    customers
WHERE
    customers.contact_title like '%Sales%'
    --
SELECT
    customer_id
from
    customers
    /* 12. */
select
    products.product_id,
    products.product_name
from
    products
where
    products.product_name like 'C%'
    /* 13. */
SELECT
    employee_id,
    first_name || ' ' || last_name AS empleado,
    title
FROM
    employees
WHERE
    title ILIKE '%sales%';

/* 14 */
select
    customer_id,
    company_name,
    contact_name,
    city,
    country,
    region
from
    customers
WHERE
    region is not null
    /* 15 */
SELECT
    product_id,
    product_name,
    units_in_stock
FROM
    products
WHERE
    units_in_stock is not null
ORDER BY
    units_in_stock DESC
    /* 16. */
SELECT
    customer_id,
    company_name,
    country
FROM
    customers
WHERE
    country IN ('USA', 'Canada');

/* 17. */
SELECT
    product_id,
    product_name,
    discontinued
FROM
    products
Where
    discontinued <> 1