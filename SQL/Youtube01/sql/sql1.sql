-- mysql -h 127.0.0.1 -P 3306 -u root  --ssl-mode=DISABLED

show databases;

+--------------------+
| Database           |
+--------------------+
| ecommerce          |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+


use ecommerce;

show tables ; 
+---------------------+
| Tables_in_ecommerce |
+---------------------+
| orders              |
| products            |
| providers           |
| users               |
+---------------------+




select
    *
from
    orders;

select
    *
from
    products;

select
    *
from
    providers;

select
    *
from
    users;

insert into
    products (name, description, price, stock)
VALUES
    ('Laptop', 'msi.', 1200.00, 50),
    ('Smartphone', 'iphone.', 800.00, 100),
    ('Headphones', 'skullcandy', 150.00, 200),
    ('Smartwatch', 'xioami', 250.00, 75),
    ('Tablet', 'samsun', 300.00, 80);

select
    *
from
    products
where
    price > 100;

-- select 1
SELECT
    *
FROM
    products
WHERE
    stock >= 10;

SELECT
    name,
    price,
    stock
FROM
    products
Where
    stock >= 10
    and price > 10
ORDER BY
    stock ASC;

select
    name
from
    products
where
    name != 'mouse'
ORDER BY
    name ASC;

SELECT
    name
FROM
    products
WHERE
    name != 'notebook';

SELECT
    products.name,
    products.price,
    products.stock
FROM
    products
WHERE
    products.price BETWEEN 10 AND 50
ORDER BY
    products.price ASC;

SELECT
    products.name
FROM
    products
WHERE
    products.name LIKE "%op";

SELECT
    products.name
FROM
    products
WHERE
    products.id in (1, 2, 3);

SELECT
    *
FROM
    products
WHERE
    products.description IS NULL;

select
    name,
    stock,
    price
from
    products
where
    price BETWEEN 50 and 150
ORDER BY
    stock DESC;

-- no se podia poner null en products.name
-- cambiar modificar el campo para null
ALTER TABLE products MODIFY name VARCHAR(100) NULL;



DESCRIBE users;
DESCRIBE products;
DESCRIBE orders;


SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;


UPDATE products
SET
    products.name = NULL,
    products.description = NULL,
    products.price = NULL,
    products.STOCK = NULL
WHERE
    products.id = 10;

UPDATE users
SET 
    users.email = 'dante2006@example.com '
WHERE
    users.id = 1


UPDATE users
SET
    users.password = '*************'


UPDATE products
SET 
    products.price = 35.50
WHERE 
    products.id = 2;


UPDATE products
SET 
    products.name = 'bookmate',
    products.description = 'laptop gamer',
    products.price = 1000
WHERE
    products.id = 4;



SHOW
CREATE TABLE
    products;

DESCRIBE customer;


INSERT INTO orders (user_id , product_id , quantity  , total) 
VALUES (8,12,24,670);

SELECT * FROM users;


select * from products ORDER BY name DESC;
SELECT * FROM products Limit 3;

SELECT DISTINCT products.description FROM products Limit 3;


SELECT DISTINCT u.name FROM users as u ;
SELECT DISTINCT p.name FROM products as p ;
SELECT DISTINCT p.created_at FROM products as p ;

SELECT u.name FROM users as u;

SELECT count(*) as producto_total FROM products;

SELECT count(*) as producto_total FROM products WHERE stock < 50;

SELECT * FROM orders;
SELECT * FROM products;

SELECT SUM(total) as Ventas  FROM orders;



SELECT AVG(price) FROM products;
SELECT MIN(price) FROM products;
SELECT MAX(price) FROM products;

SELECT * FROM users; 
SELECT * FROM orders;

SELECT u.created_at , u.name ,p.description, o.quantity,  o.total 
FROM users as u 
INNER JOIN orders as o ON u.id = o.user_id
INNER JOIN products as p ON p.id = o.product_id;


SELECT u.id ,u.name,o.quantity from users as u left join orders as o on u.id = o.user_id;



SELECT u.name, (select sum(total) FROM orders where user_id = u.id) as TOTAL_GASTO FROM users AS u ;




SELECT usuario,total_gastado 
FROM (

    
)

/*  */











