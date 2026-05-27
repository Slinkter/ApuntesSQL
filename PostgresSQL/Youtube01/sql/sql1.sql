select * from orders;

select * from products;

select * from providers;

select * from users;

insert into
    products (
        name,
        description,
        price,
        stock
    )
VALUES ('Laptop', 'msi.', 1200.00, 50),
    (
        'Smartphone',
        'iphone.',
        800.00,
        100
    ),
    (
        'Headphones',
        'skullcandy',
        150.00,
        200
    ),
    (
        'Smartwatch',
        'xioami',
        250.00,
        75
    ),
    (
        'Tablet',
        'samsun',
        300.00,
        80
    );

select * from products where price > 100;

-- select 1

SELECT * FROM products WHERE stock >= 10;

SELECT name, price, stock
FROM products
Where
    stock >= 10
    and price > 10
ORDER BY stock ASC;

select name from products 
where name != 'mouse' 
ORDER BY name ASC;

SELECT name FROM products 
WHERE name != 'notebook';

SELECT products.name,products.price,products.stock  FROM products
WHERE products.price BETWEEN 10 AND 50 
ORDER BY products.price ASC;


SELECT products.name FROM products 
WHERE products.name LIKE "%op";

SELECT products.name FROM products 
WHERE products.id in (1,2,3);

SELECT * FROM products 
WHERE products.description IS NULL;

select name, stock, price
from products
where
    price BETWEEN 50 and 150
ORDER BY stock DESC;

-- no se podia poner null en products.name
-- cambiar modificar el campo para null

ALTER TABLE products MODIFY name VARCHAR(100) NULL;

UPDATE products
SET
    products.name = NULL,
    products.description = NULL,
    products.price = NULL,
    products.STOCK = NULL
WHERE
    products.id = 10;

SHOW CREATE TABLE products;