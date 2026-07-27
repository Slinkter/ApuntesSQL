SELECT p.product_id,
       p.product_name,
       length(p.product_name) AS longitud_nombre,
       UPPER(p.product_name) AS mayuscula_nombre,
       s.contact_name AS Contacto
from products p
INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
ORDER BY p.product_name /*  */