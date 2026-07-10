SELECT version () AS "Server Info";

-- PostgreSQL 16.14  (Alpine 15.2.0)

SELECT current_database ();

-- northwind

SELECT current_user;

-- slinkter

SELECT inet_server_addr () AS "IP_del_Servidor_Remoto";

-- 172.18.0.2

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- categories
-- customers
-- employee_territories
-- employees
-- order_details
-- orders
-- products
-- region
-- shippers
-- suppliers
-- territories
-- us_states

SELECT *
FROM categories;


SELECT *
FROM customers;


SELECT *
FROM employee_territories;


SELECT *
FROM employees;


SELECT count(*)
FROM categories;


SELECT count(*)
FROM customers;


SELECT count(*)
FROM suppliers;


SELECT *
FROM employees;


SELECT employee_id,
       last_name,
       first_name,
       title
FROM employees;


SELECT count(*)
FROM orders;


SELECT *
FROM PRODUCTS;


SELECT product_name,
       unit_price
FROM PRODUCTS
order by unit_price DESC;


SELECT product_name,
       unit_price
FROM PRODUCTS
where unit_price > 30
ORDER BY unit_price ASC;


SELECT product_name,
       CAST(unit_price AS DECIMAL(10, 2))
FROM PRODUCTS
where unit_price > 30
ORDER BY unit_price DESC;


SELECT order_id,
       customer_id,
       order_date
FROM orders
ORDER by order_date DESC;


select order_id,
       ship_name,
       freight
from orders;


SELECT order_id,
       ship_name,
       freight
FROM orders
SELECT *
FROM information_schema.tables;


SELECT order_id,
       order_date,
       customer_id
FROM ORDERS
ORDER BY order_date DESC
LIMIT 10
OFFSET 20;

--
-- customers

select *
from customers
LIMIT 150;


SELECT customer_id,
       company_name,
       country
from customers
WHERE country IN ('Germany',
                  'UK',
                  'USA')
ORDER BY country,
         company_name;

--8.

SELECT product_id,
       product_name,
       CAST(unit_price AS DECIMAL(10, 2))
FROM products
WHERE unit_price BETWEEN 15 AND 75
ORDER BY unit_price DESC;

-- 9.

SELECT order_id,
       customer_id,
       order_date
FROM orders
where order_date < '1997-01-01'
ORDER BY order_date DESC;

-- 10 .

SELECT employee_id as "ID",
       last_name || ' ' || first_name as "FULL NAME",
       title as "TITLE",
       hire_date as "HIRE DATE"
FROM EMPLOYEES
WHERE hire_date >= '1993-01-01'
ORDER BY hire_date asc
LIMIT 10;

-- 11.
-- %Sales%
-- name_empresa,contact_name , sale

select customer_id,
       company_name,
       contact_name,
       contact_title
from customers
where contact_title like '%Sales%'
ORDER BY company_name;