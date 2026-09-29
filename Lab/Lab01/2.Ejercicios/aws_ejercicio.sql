SELECT c.category_name,
       COUNT(p.product_id) AS total_productos
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY total_productos DESC;


SELECT c.category_id,
       c.category_name
from categories as c ;


SELECT product_id,
       product_name,
       category_id
from products as p;