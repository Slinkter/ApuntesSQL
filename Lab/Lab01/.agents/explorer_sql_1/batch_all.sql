\set ON_ERROR_STOP off
\timing off
\echo ===DELIM_START_0===
-- Ejemplo de cada subconjunto en acción:

-- DDL: Crear una tabla
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DML: Insertar un registro
INSERT INTO audit_log (action) VALUES ('Usuario conectado');

-- DQL: Consultar registros
SELECT * FROM audit_log WHERE action = 'Usuario conectado';

-- DCL: Dar permisos (requiere superusuario)
GRANT SELECT ON audit_log TO report_user;
\echo ===DELIM_END_0===
\echo ===DELIM_START_1===
-- Consulta que demuestra las 3 tablas relacionadas
SELECT
    c.company_name,          -- de customers
    o.order_date,            -- de orders
    p.product_name,          -- de products
    od.quantity,             -- de order_details
    od.unit_price            -- de order_details
FROM order_details od
JOIN orders o     ON od.order_id = o.order_id
JOIN customers c  ON o.customer_id = c.customer_id
JOIN products p   ON od.product_id = p.product_id
LIMIT 5;
\echo ===DELIM_END_1===
\echo ===DELIM_START_2===
-- Ejemplo de relación autorreferencial: jerarquía de empleados
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    COALESCE(m.first_name || ' ' || m.last_name, '(CEO)') AS reporta_a
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.reports_to;
\echo ===DELIM_END_2===
\echo ===DELIM_START_3===
-- Ejemplo práctico: crear un índice y verificar su uso
-- Paso 1: Crear índice en la columna de búsqueda
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Paso 2: Verificar que PostgreSQL lo usa
EXPLAIN SELECT * FROM orders WHERE customer_id = 'ALFKI';

-- Output esperado:
-- Index Scan using idx_orders_customer on orders
--   Index Cond: (customer_id = 'ALFKI'::character(5))

-- Paso 3: Comparar con y sin índice
-- Sin índice: Seq Scan (lee las 830 filas)
-- Con índice: Index Scan (salta directamente a las filas de ALFKI)
;
\echo ===DELIM_END_3===
\echo ===DELIM_START_4===
SET search_path TO public;
\echo ===DELIM_END_4===
\echo ===DELIM_START_5===
-- Ver el search_path actual
SHOW search_path;

-- Resultado por defecto: "$user", public
-- PostgreSQL primero busca en un schema con tu nombre de usuario,
-- luego en "public"

-- En este laboratorio siempre estamos en "public"
SET search_path TO public;
\echo ===DELIM_END_5===
\echo ===DELIM_START_6===
-- Conectarse
northwind=# \conninfo
You are connected to database "northwind" as user "postgres" via socket in "/var/run/postgresql" at port "5432".

-- Ver tablas disponibles
northwind=# \dt
             List of relations
 Schema |      Name      | Type  |  Owner
--------+----------------+-------+---------
 public | categories     | table | postgres
 public | customers      | table | postgres
 public | employees      | table | postgres
 public | orders         | table | postgres
 public | order_details  | table | postgres
 public | products       | table | postgres
 public | suppliers      | table | postgres
 public | shippers       | table | postgres
 ...

-- Ver estructura de una tabla
northwind=# \d customers
                       Table "public.customers"
    Column    |         Type          | Collation | Nullable | Default
--------------+-----------------------+-----------+----------+---------
 customer_id  | character(5)          |           | not null |
 company_name | character varying(40) |           | not null |
 contact_name | character varying(30) |           |          |
 country      | character varying(15) |           |          |
Indexes:
    "pk_customers" PRIMARY KEY, btree (customer_id)

-- Habilitar medición de tiempo
northwind=# \timing on
Timing is on.

-- Ejecutar una query y ver el tiempo
northwind=# SELECT COUNT(*) FROM orders;
 count
-------
   830
Time: 0.482 ms

-- Cambiar a formato expandido para registros anchos
northwind=# \x
Expanded display is on.

northwind=# SELECT * FROM customers WHERE customer_id = 'ALFKI';
-[ RECORD 1 ]+------------------------------------
customer_id  | ALFKI
company_name | Alfreds Futterkiste
contact_name | Maria Anders
country      | Germany
;
\echo ===DELIM_END_6===
\echo ===DELIM_START_7===
-- Ejemplo: ver cuántos productos tiene cada categoría
SELECT
    c.category_name,
    COUNT(p.product_id) AS total_productos
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY total_productos DESC;
\echo ===DELIM_END_7===
\echo ===DELIM_START_8===
-- Ejemplo: ver el detalle de un pedido específico
SELECT
    p.product_name,
    od.quantity,
    od.unit_price,
    od.discount,
    (od.quantity * od.unit_price * (1 - od.discount)) AS total_linea
FROM order_details od
JOIN products p ON od.product_id = p.product_id
WHERE od.order_id = 10248;
\echo ===DELIM_END_8===
\echo ===DELIM_START_9===
-- Ejemplo: ver la jerarquía de empleados
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo,
    COALESCE(m.first_name || ' ' || m.last_name, '(CEO / Sin jefe)') AS reporta_a
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.reports_to NULLS FIRST;
\echo ===DELIM_END_9===
\echo ===DELIM_START_10===
EXPLAIN (ANALYZE, BUFFERS) SELECT ... ;
\echo ===DELIM_END_10===
\echo ===DELIM_START_11===
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.company_name, COUNT(o.order_id) AS pedidos
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Mexico'
GROUP BY c.company_name;
\echo ===DELIM_END_11===
\echo ===DELIM_START_12===
-- ANTES del índice: Seq Scan en 830 filas
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 'ALFKI';
-- Seq Scan on orders  (cost=0.00..22.30 rows=1 width=...)
--   Filter: (customer_id = 'ALFKI'::character(5))
--   Rows Removed by Filter: 829
-- Execution Time: 0.15 ms  (pero lee TODA la tabla)

-- Crear el índice
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- DESPUÉS del índice: Index Scan directo
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 'ALFKI';
-- Index Scan using idx_orders_customer on orders
--   Index Cond: (customer_id = 'ALFKI'::character(5))
-- Execution Time: 0.05 ms  (salta directamente a la fila)
;
\echo ===DELIM_END_12===
\echo ===DELIM_START_13===
-- 1. Índice Compuesto con Orden Específico (Multi-column)
CREATE INDEX idx_orders_user_date ON orders(customer_id, order_date DESC);

-- 2. Índice Parcial (Partial Index) - Reduce el tamaño del índice en un 80%
CREATE INDEX idx_orders_unshipped ON orders(order_id) 
WHERE shipped_date IS NULL;

-- 3. Índice Expresional (Expression / Functional Index)
CREATE INDEX idx_customers_lower_company ON customers(lower(company_name));

-- 4. Índice Cubriente (Covering Index con cláusula INCLUDE) - Index Only Scan
CREATE INDEX idx_orders_covering ON orders(customer_id) 
INCLUDE (order_date, freight);

-- 5. Índice GIN para datos JSONB o Full-Text Search
-- CREATE INDEX idx_events_data_gin ON events USING gin(data);
\echo ===DELIM_END_13===
\echo ===DELIM_START_14===
-- Identificar el TOP 10 de consultas más lentas y su tasa de acierto en memoria caché
SELECT 
    query, 
    calls, 
    round(total_exec_time::numeric, 2) AS total_time_ms, 
    round(mean_exec_time::numeric, 2) AS mean_time_ms, 
    rows,
    round((100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0))::numeric, 2) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_exec_time DESC 
LIMIT 10;
\echo ===DELIM_END_14===
\echo ===DELIM_START_15===
-- Iniciar transacción (crea un punto de guardado)
BEGIN;

INSERT INTO orders (order_id, customer_id, employee_id, order_date)
VALUES (99999, 'ALFKI', 1, CURRENT_DATE);

UPDATE customers
SET contact_name = 'Nuevo Contacto'
WHERE customer_id = 'ALFKI';

-- Confirmar cambios (punto de guardado permanente)
COMMIT;
\echo ===DELIM_END_15===
\echo ===DELIM_START_16===
BEGIN;
DELETE FROM orders WHERE order_id = 99999;
-- Ups, no quería borrar ese pedido
ROLLBACK;  -- todo vuelve al estado anterior, como si el DELETE nunca hubiera existido
;
\echo ===DELIM_END_16===
\echo ===DELIM_START_17===
BEGIN;
  INSERT INTO customers ...;
  SAVEPOINT sp1;               -- creamos un sub-punto de guardado
  INSERT INTO orders ...;      -- esto falla
  ROLLBACK TO SAVEPOINT sp1;   -- deshace solo el INSERT orders
  -- customers insertado se conserva
COMMIT;
\echo ===DELIM_END_17===
\echo ===DELIM_START_18===
-- Ejemplo: cambiar nivel de aislamiento
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM orders WHERE customer_id = 'ALFKI';  -- ve 5 pedidos
-- otro usuario inserta un pedido de ALFKI mientras tanto
SELECT COUNT(*) FROM orders WHERE customer_id = 'ALFKI';  -- AÚN ve 5 pedidos (mismo snapshot)
COMMIT;
\echo ===DELIM_END_18===
\echo ===DELIM_START_19===
-- SIN transacción (Peligroso):
-- Usuario A: Lee stock = 10
-- Usuario B: Lee stock = 10
-- Usuario A: UPDATE stock = 10 - 3 = 7
-- Usuario B: UPDATE stock = 10 - 5 = 5  ← ¡Sobrescribió el cambio de A!
-- Resultado final: stock = 5 (pero se vendieron 8 unidades, debería ser 2)

-- CON transacción (Seguro):
BEGIN;
SELECT units_in_stock FROM products WHERE product_id = 1;
-- stock = 10
UPDATE products SET units_in_stock = units_in_stock - 3 WHERE product_id = 1;
-- stock = 7 (otro usuario ve 7, no 10)
COMMIT;
\echo ===DELIM_END_19===
\echo ===DELIM_START_20===
-- Patrón seguro para DML destructivo en producción
BEGIN;
EXPLAIN ANALYZE
DELETE FROM orders WHERE order_date < '1990-01-01';
-- Veo que borraría 0 filas (la fecha más antigua es 1996)
ROLLBACK;  -- no ejecuto el DELETE, solo quería ver el impacto
;
\echo ===DELIM_END_20===
\echo ===DELIM_START_21===
-- PostgreSQL: eficiente con RETURNING
INSERT INTO customers (customer_id, company_name, city, country)
VALUES ('NEWCO', 'Nueva Corp', 'Lima', 'Peru')
RETURNING customer_id, company_name, city;
-- Obtienes el resultado inmediatamente

-- MySQL: necesitas dos queries
-- INSERT INTO customers (customer_id, company_name, ...) VALUES (...);
-- SELECT LAST_INSERT_ID();
\echo ===DELIM_END_21===
\echo ===DELIM_START_22===
-- PostgreSQL: UPSERT limpio
INSERT INTO products (product_id, product_name, unit_price)
VALUES (100, 'Producto Nuevo', 15.50)
ON CONFLICT (product_id)
DO UPDATE SET
  product_name = EXCLUDED.product_name,
  unit_price = EXCLUDED.unit_price;
-- Si product_id 100 ya existe: actualiza nombre y precio
-- Si no existe: inserta normalmente

-- Ignorar conflicto silenciosamente
INSERT INTO products (product_id, product_name, unit_price)
VALUES (100, 'Producto Nuevo', 15.50)
ON CONFLICT (product_id) DO NOTHING;
\echo ===DELIM_END_22===
\echo ===DELIM_START_23===
-- PostgreSQL: case-insensitive
SELECT * FROM customers WHERE company_name ILIKE '%food%';
-- Encuentra "Food", "FOOD", "food", "FoOd", etc.

-- Si no tienes ILIKE (ej: en MySQL), necesitas:
SELECT * FROM customers WHERE LOWER(company_name) LIKE '%food%';
-- Más verboso, y puede no usar índices eficientemente
;
\echo ===DELIM_END_23===
\echo ===DELIM_START_24===
-- PostgreSQL: elegante con FILTER
SELECT
  COUNT(*) AS total_pedidos,
  COUNT(*) FILTER (WHERE ship_country = 'USA') AS usa,
  COUNT(*) FILTER (WHERE ship_country = 'Germany') AS germany,
  COUNT(*) FILTER (WHERE ship_country = 'Brazil') AS brazil
FROM orders;

-- MySQL: necesitas CASE WHEN
SELECT
  COUNT(*) AS total_pedidos,
  SUM(CASE WHEN ship_country = 'USA' THEN 1 ELSE 0 END) AS usa,
  SUM(CASE WHEN ship_country = 'Germany' THEN 1 ELSE 0 END) AS germany,
  SUM(CASE WHEN ship_country = 'Brazil' THEN 1 ELSE 0 END) AS brazil
FROM orders;
\echo ===DELIM_END_24===
\echo ===DELIM_START_25===
-- SERIAL: el atajo de PostgreSQL
CREATE TABLE mi_tabla (
  id SERIAL PRIMARY KEY,  -- crea secuencia + default automáticamente
  nombre TEXT
);

-- Equivalente exacto (lo que SERIAL crea internamente)
CREATE TABLE mi_tabla (
  id INTEGER PRIMARY KEY,
  nombre TEXT
);
-- PostgreSQL crea automáticamente:
-- SEQUENCE mi_tabla_id_seq
-- DEFAULT nextval('mi_tabla_id_seq')

-- SQL Estándar (recomendado para nuevos proyectos)
CREATE TABLE mi_tabla (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre TEXT
);
\echo ===DELIM_END_25===
\echo ===DELIM_START_26===
-- Ejemplo: ¿por qué no puedes usar alias de SELECT en WHERE?
SELECT
  product_name,
  unit_price * quantity AS total
FROM order_details
WHERE total > 100;  -- ❌ ERROR: "total" no existe aún en el orden de ejecución

-- Solución correcta: repetir la expresión o usar subquery
SELECT * FROM (
  SELECT
    product_name,
    unit_price * quantity AS total
  FROM order_details
) sub
WHERE total > 100;  -- ✅ Funciona porque el alias está en el FROM
;
\echo ===DELIM_END_26===
\echo ===DELIM_START_27===
-- Patrón seguro: ver qué harías SIN ejecutar
BEGIN;
EXPLAIN (ANALYZE, BUFFERS)
DELETE FROM orders WHERE order_date < '1990-01-01';
-- Output: "Seq Scan on orders ... Rows Removed by Filter: 830"
-- PostgreSQL estima 0 filas (la fecha más antigua es 1996)
ROLLBACK;  -- no ejecuto nada, solo quería ver el impacto

-- Si el EXPLAIN muestra muchas filas que SÍ quieres borrar:
BEGIN;
DELETE FROM orders WHERE order_date < '1997-01-01';
-- Verificar cuántas filas se borraron
SELECT COUNT(*) FROM orders WHERE order_date < '1997-01-01';
-- Si es correcto:
COMMIT;
-- Si no es correcto:
ROLLBACK;
\echo ===DELIM_END_27===
\echo ===DELIM_START_28===
-- MATERIALIZED: ejecuta la CTE una vez y reutiliza el resultado
WITH ventas_por_producto AS MATERIALIZED (
  SELECT
    product_id,
    SUM(quantity * unit_price) AS total_ventas
  FROM order_details
  GROUP BY product_id
)
SELECT
  p.product_name,
  v.total_ventas
FROM ventas_por_producto v
JOIN products p ON v.product_id = p.product_id
WHERE v.total_ventas > 1000;

-- NOT MATERIALIZED: el optimizador puede reescribir la CTE como subquery
WITH productos_activos AS NOT MATERIALIZED (
  SELECT product_id, product_name
  FROM products
  WHERE discontinued = 0
)
SELECT * FROM productos_activos WHERE product_id < 20;
-- PostgreSQL puede "colapsar" la CTE y optimizarla junto con el WHERE
;
\echo ===DELIM_END_28===
\echo ===DELIM_START_29===
-- Generar números del 1 al 10
SELECT generate_series(1, 10) AS numero;

-- Generar fechas diarias
SELECT generate_series('2024-01-01'::date, '2024-01-10'::date, '1 day'::interval) AS fecha;

-- Caso de uso real: reporte diario sin datos faltantes
-- (cuando quieres ver 0 ventas en días sin actividad)
SELECT
  d::date AS dia,
  COUNT(o.order_id) AS pedidos
FROM generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day'::interval) d
LEFT JOIN orders o ON o.order_date = d::date
GROUP BY d::date
ORDER BY d::date;
\echo ===DELIM_END_29===
\echo ===DELIM_START_30===
-- Monitoreo de Tuplas Muertas (Dead Tuples) y Bloat en el Esquema
SELECT 
    schemaname,
    relname AS tabla,
    n_live_tup AS tuplas_vivas,
    n_dead_tup AS tuplas_muertas,
    round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS pct_bloat,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
\echo ===DELIM_END_30===
\echo ===DELIM_START_31===
SELECT
    employee_id,
    last_name,
    first_name,
    title
FROM employees
ORDER BY employee_id;
\echo ===DELIM_END_31===
\echo ===DELIM_START_32===
SELECT
    product_name,
    unit_price
FROM products
WHERE unit_price > 30
ORDER BY unit_price DESC;
\echo ===DELIM_END_32===
\echo ===DELIM_START_33===
SELECT
    order_id,
    customer_id,
    order_date
FROM orders
ORDER BY order_date DESC;
\echo ===DELIM_END_33===
\echo ===DELIM_START_34===
SELECT
    order_id,
    ship_name,
    freight
FROM orders
ORDER BY freight DESC NULLS LAST;
\echo ===DELIM_END_34===
\echo ===DELIM_START_35===
SELECT
    product_name,
    unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 5;
\echo ===DELIM_END_35===
\echo ===DELIM_START_36===
SELECT
    order_id,
    order_date,
    customer_id
FROM orders
ORDER BY order_date ASC
LIMIT 10 OFFSET 20;
\echo ===DELIM_END_36===
\echo ===DELIM_START_37===
SELECT
    customer_id,
    company_name,
    country
FROM customers
WHERE country IN ('Germany', 'UK', 'USA')
ORDER BY country, company_name;
\echo ===DELIM_END_37===
\echo ===DELIM_START_38===
SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE unit_price BETWEEN 15 AND 75
ORDER BY unit_price;
\echo ===DELIM_END_38===
\echo ===DELIM_START_39===
SELECT
    order_id,
    customer_id,
    order_date
FROM orders
WHERE order_date < '1997-01-01'
ORDER BY order_date;
\echo ===DELIM_END_39===
\echo ===DELIM_START_40===
SELECT
    employee_id,
    first_name || ' ' || last_name AS empleado,
    title,
    hire_date
FROM employees
WHERE hire_date >= '1993-01-01'
ORDER BY hire_date ASC
LIMIT 10;
\echo ===DELIM_END_40===
\echo ===DELIM_START_41===
SELECT
    company_name,
    contact_name,
    contact_title
FROM customers
WHERE contact_title LIKE '%Sales%'
ORDER BY company_name;
\echo ===DELIM_END_41===
\echo ===DELIM_START_42===
SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE product_name LIKE 'C%'
ORDER BY product_name;
\echo ===DELIM_END_42===
\echo ===DELIM_START_43===
SELECT
    employee_id,
    first_name || ' ' || last_name AS empleado,
    title
FROM employees
WHERE title ILIKE '%manager%';
\echo ===DELIM_END_43===
\echo ===DELIM_START_44===
SELECT
    customer_id,
    company_name,
    city,
    country
FROM customers
WHERE region IS NULL;
\echo ===DELIM_END_44===
\echo ===DELIM_START_45===
SELECT
    product_name,
    units_in_stock
FROM products
WHERE units_in_stock IS NOT NULL
ORDER BY units_in_stock DESC;
\echo ===DELIM_END_45===
\echo ===DELIM_START_46===
SELECT
    customer_id,
    company_name,
    country,
    phone
FROM customers
WHERE country = 'USA'
   OR country = 'Canada'
ORDER BY country, company_name;
\echo ===DELIM_END_46===
\echo ===DELIM_START_47===
SELECT
    product_id,
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE discontinued <> 1
ORDER BY product_name;
\echo ===DELIM_END_47===
\echo ===DELIM_START_48===
SELECT
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE unit_price > 20
  AND units_in_stock > 50
ORDER BY unit_price DESC;
\echo ===DELIM_END_48===
\echo ===DELIM_START_49===
SELECT
    order_id,
    customer_id,
    required_date,
    shipped_date
FROM orders
WHERE shipped_date > required_date
ORDER BY shipped_date;
\echo ===DELIM_END_49===
\echo ===DELIM_START_50===
SELECT
    employee_id,
    first_name || ' ' || last_name AS empleado,
    title,
    hire_date,
    country
FROM employees
WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31'
  AND country <> 'USA'
ORDER BY hire_date;
\echo ===DELIM_END_50===
\echo ===DELIM_START_51===
SELECT DISTINCT
    country
FROM customers
ORDER BY country;
\echo ===DELIM_END_51===
\echo ===DELIM_START_52===
SELECT
    country,
    COUNT(*) AS total_clientes
FROM customers
GROUP BY country
ORDER BY total_clientes DESC;
\echo ===DELIM_END_52===
\echo ===DELIM_START_53===
SELECT
    SUM(unit_price * units_in_stock) AS valorizacion_total
FROM products;
\echo ===DELIM_END_53===
\echo ===DELIM_START_54===
SELECT
    ROUND(AVG(unit_price)::numeric, 2) AS precio_promedio
FROM products;
\echo ===DELIM_END_54===
\echo ===DELIM_START_55===
SELECT
    MIN(unit_price) AS precio_minimo,
    MAX(unit_price) AS precio_maximo,
    ROUND((MAX(unit_price) - MIN(unit_price))::numeric, 2) AS rango
FROM products;
\echo ===DELIM_END_55===
\echo ===DELIM_START_56===
SELECT
    product_id,
    SUM(quantity * unit_price * (1 - discount)) AS ingreso_total
FROM order_details
GROUP BY product_id
ORDER BY ingreso_total DESC;
\echo ===DELIM_END_56===
\echo ===DELIM_START_57===
SELECT
    COUNT(*) AS total_pedidos,
    COUNT(*) FILTER (WHERE freight > 200) AS pedidos_flete_elevado
FROM orders;
\echo ===DELIM_END_57===
\echo ===DELIM_START_58===
SELECT
    ROUND(AVG(freight) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 1996)::numeric, 2) AS flete_promedio_1996,
    ROUND(AVG(freight) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 1997)::numeric, 2) AS flete_promedio_1997,
    ROUND(AVG(freight) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 1998)::numeric, 2) AS flete_promedio_1998
FROM orders;
\echo ===DELIM_END_58===
\echo ===DELIM_START_59===
SELECT
    employee_id,
    COUNT(*) AS total_territorios,
    COUNT(*) FILTER (WHERE territory_id LIKE '0%') AS territorios_costa_este
FROM employee_territories
GROUP BY employee_id
ORDER BY total_territorios DESC;
\echo ===DELIM_END_59===
\echo ===DELIM_START_60===
SELECT
    category_id,
    COUNT(*) AS total_productos,
    COUNT(*) FILTER (WHERE unit_price > 50) AS productos_premium,
    ROUND(AVG(unit_price)::numeric, 2) AS precio_promedio,
    ROUND(AVG(unit_price) FILTER (WHERE units_in_stock > 0)::numeric, 2) AS precio_promedio_stock_disponible
FROM products
GROUP BY category_id
ORDER BY category_id;
\echo ===DELIM_END_60===
\echo ===DELIM_START_61===
SELECT
    country,
    city,
    COUNT(DISTINCT customer_id) AS total_clientes
FROM customers
GROUP BY country, city
HAVING COUNT(DISTINCT customer_id) > 1
ORDER BY total_clientes DESC;
\echo ===DELIM_END_61===
\echo ===DELIM_START_62===
SELECT
    product_name,
    unit_price,
    units_in_stock,
    unit_price * units_in_stock AS valor_inventario,
    ROUND((unit_price * 1.10)::numeric, 2) AS precio_con_10_pct_aumento
FROM products
WHERE discontinued = 0
ORDER BY valor_inventario DESC;
\echo ===DELIM_END_62===
\echo ===DELIM_START_63===
SELECT
    product_name AS "Nombre del Producto",
    unit_price AS "Precio Unitario ($)",
    units_in_stock AS "Unidades en Stock",
    category_id AS "ID Categoría"
FROM products
WHERE discontinued = 0
ORDER BY unit_price DESC;
\echo ===DELIM_END_63===
\echo ===DELIM_START_64===
SELECT
    product_name,
    COALESCE(unit_price, 0) AS precio_seguro,
    COALESCE(units_in_stock, 0) AS stock_seguro,
    COALESCE(unit_price, 0) * COALESCE(units_in_stock, 0) AS valor_inventario
FROM products
ORDER BY valor_inventario DESC;
\echo ===DELIM_END_64===
\echo ===DELIM_START_65===
SELECT
    product_name,
    LENGTH(product_name) AS longitud_nombre,
    UPPER(product_name) AS nombre_mayusculas,
    contact_name AS contacto
FROM products p
INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
ORDER BY longitud_nombre DESC;
\echo ===DELIM_END_65===
\echo ===DELIM_START_66===
SELECT
    company_name,
    LOWER(company_name) AS nombre_minusculas,
    TRIM(company_name) AS nombre_limpio,
    LENGTH(company_name) AS largo_original,
    LENGTH(TRIM(company_name)) AS largo_sin_espacios
FROM customers
WHERE country = 'Germany'
ORDER BY company_name;
\echo ===DELIM_END_66===
\echo ===DELIM_START_67===
SELECT
    customer_id,
    company_name,
    SUBSTRING(customer_id FROM 1 FOR 2) AS prefijo_cliente,
    LEFT(customer_id, 1) AS primera_letra
FROM customers
ORDER BY customer_id;
\echo ===DELIM_END_67===
\echo ===DELIM_START_68===
SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title || ' - ' || city AS cargo_ubicacion,
    COALESCE(region || ', ', ') || country AS ubicacion_completa
FROM employees
ORDER BY last_name;
\echo ===DELIM_END_68===
\echo ===DELIM_START_69===
SELECT
    order_id,
    order_date,
    EXTRACT(YEAR FROM order_date) AS anio,
    EXTRACT(MONTH FROM order_date) AS mes,
    EXTRACT(DAY FROM order_date) AS dia,
    EXTRACT(ISODOW FROM order_date) AS dia_semana
FROM orders
WHERE order_date >= '1997-01-01'
ORDER BY order_date
LIMIT 10;
\echo ===DELIM_END_69===
\echo ===DELIM_START_70===
SELECT
    DATE_TRUNC('month', order_date) AS mes_truncado,
    COUNT(*) AS total_pedidos,
    ROUND(SUM(freight)::numeric, 2) AS total_flete
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY mes_truncado;
\echo ===DELIM_END_70===
\echo ===DELIM_START_71===
SELECT
    first_name || ' ' || last_name AS empleado,
    hire_date,
    AGE(CURRENT_DATE, hire_date) AS antiguedad_intervalo,
    EXTRACT(YEAR FROM AGE(hire_date)) AS anos_en_empresa,
    CASE
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 10 THEN 'Veterano'
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 5 THEN 'Experimentado'
        ELSE 'Nuevo'
    END AS categoria
FROM employees
ORDER BY hire_date;
\echo ===DELIM_END_71===
\echo ===DELIM_START_72===
SELECT
    CURRENT_DATE AS fecha_hoy,
    CURRENT_DATE - INTERVAL '30 days' AS hace_30_dias,
    CURRENT_DATE + INTERVAL '3 months' AS en_3_meses,
    AGE(CURRENT_DATE, '1997-01-01') AS tiempo_desde_northwind
;
\echo ===DELIM_END_72===
\echo ===DELIM_START_73===
SELECT
    order_id,
    TO_CHAR(order_date, 'DD/MM/YYYY') AS fecha_corta,
    TO_CHAR(order_date, 'Day, DD de Month YYYY') AS fecha_larga,
    TO_CHAR(order_date, 'Month YYYY') AS mes_ano
FROM orders
WHERE order_date >= '1997-06-01'
ORDER BY order_date
LIMIT 10;
\echo ===DELIM_END_73===
\echo ===DELIM_START_74===
SELECT
    product_name,
    unit_price,
    CASE
        WHEN unit_price < 15 THEN 'Económico'
        WHEN unit_price < 50 THEN 'Intermedio'
        ELSE 'Premium'
    END AS categoria_precio
FROM products
WHERE discontinued = 0
ORDER BY unit_price;
\echo ===DELIM_END_74===
\echo ===DELIM_START_75===
SELECT
    category_id,
    COUNT(*) AS total_productos,
    SUM(CASE WHEN unit_price < 20 THEN 1 ELSE 0 END) AS economicos,
    SUM(CASE WHEN unit_price >= 20 AND unit_price < 50 THEN 1 ELSE 0 END) AS intermedios,
    SUM(CASE WHEN unit_price >= 50 THEN 1 ELSE 0 END) AS premium
FROM products
WHERE discontinued = 0
GROUP BY category_id
ORDER BY category_id;
\echo ===DELIM_END_75===
\echo ===DELIM_START_76===
SELECT
    order_id,
    order_date,
    EXTRACT(QUARTER FROM order_date) AS trimestre,
    CASE
        WHEN EXTRACT(MONTH FROM order_date) BETWEEN 1 AND 3 THEN 'Enero-Marzo'
        WHEN EXTRACT(MONTH FROM order_date) BETWEEN 4 AND 6 THEN 'Abril-Junio'
        WHEN EXTRACT(MONTH FROM order_date) BETWEEN 7 AND 9 THEN 'Julio-Septiembre'
        ELSE 'Octubre-Diciembre'
    END AS periodo,
    freight
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 1997
ORDER BY order_date;
\echo ===DELIM_END_76===
\echo ===DELIM_START_77===
SELECT
    order_id,
    customer_id,
    order_date,
    shipped_date,
    CASE
        WHEN shipped_date IS NULL THEN 1
        WHEN shipped_date <= required_date THEN 2
        ELSE 3
    END AS prioridad_envio,
    CASE
        WHEN shipped_date IS NULL THEN 'Pendiente'
        WHEN shipped_date <= required_date THEN 'A tiempo'
        ELSE 'Con retraso'
    END AS estado_envio
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 1997
ORDER BY
    CASE
        WHEN shipped_date IS NULL THEN 1
        WHEN shipped_date <= required_date THEN 2
        ELSE 3
    END,
    order_date;
\echo ===DELIM_END_77===
\echo ===DELIM_START_78===
SELECT
    customer_id,
    company_name,
    CASE
        WHEN region IS NULL THEN 'Sin región'
        ELSE region
    END AS region_completa,
    CASE
        WHEN fax IS NOT NULL THEN fax
        WHEN phone IS NOT NULL THEN phone
        ELSE 'Sin contacto'
    END AS mejor_contacto
FROM customers
WHERE country = 'Germany'
ORDER BY company_name;
\echo ===DELIM_END_78===
\echo ===DELIM_START_79===
SELECT
    p.product_id,
    UPPER(p.product_name) AS nombre_producto,
    p.unit_price AS precio_actual,
    COALESCE(p.units_in_stock, 0) AS stock,
    COALESCE(p.unit_price, 0) * COALESCE(p.units_in_stock, 0) AS valor_inventario,
    LENGTH(p.product_name) AS largo_nombre,
    CASE
        WHEN p.discontinued = 0 THEN 'Activo'
        ELSE 'Descontinuado'
    END AS estado,
    CASE
        WHEN p.unit_price < 20 THEN 'Económico'
        WHEN p.unit_price < 50 THEN 'Normal'
        ELSE 'Premium'
    END AS categoria
FROM products p
WHERE p.discontinued = 0
ORDER BY p.unit_price DESC
LIMIT 20;
\echo ===DELIM_END_79===
\echo ===DELIM_START_80===
SELECT
    o.order_id,
    o.order_date,
    c.company_name AS cliente,
    COALESCE(o.ship_country, 'No especificado') AS pais_destino,
    o.freight AS flete,
    ROUND((o.freight * 1.19)::numeric, 2) AS flete_con_igv,
    CASE
        WHEN o.freight > 500 THEN 'Alto'
        WHEN o.freight > 100 THEN 'Medio'
        ELSE 'Bajo'
    END AS categoria_flete,
    CASE
        WHEN o.shipped_date IS NULL THEN 'Pendiente'
        WHEN o.shipped_date <= o.required_date THEN 'A tiempo'
        ELSE 'Retrasado'
    END AS estado_envio
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '1997-01-01'
  AND o.order_date < '1998-01-01'
ORDER BY o.freight DESC
LIMIT 25;
\echo ===DELIM_END_80===
\echo ===DELIM_START_81===
SELECT
    country,
    COUNT(*) AS total_clientes
FROM customers
GROUP BY country
HAVING COUNT(*) > 5
ORDER BY total_clientes DESC;
\echo ===DELIM_END_81===
\echo ===DELIM_START_82===
SELECT
    category_id,
    COUNT(*) AS total_productos
FROM products
GROUP BY category_id
HAVING COUNT(*) > 10
ORDER BY total_productos DESC;
\echo ===DELIM_END_82===
\echo ===DELIM_START_83===
SELECT
    employee_id,
    COUNT(order_id) AS total_pedidos
FROM orders
GROUP BY employee_id
HAVING COUNT(order_id) > 80
ORDER BY total_pedidos DESC;
\echo ===DELIM_END_83===
\echo ===DELIM_START_84===
SELECT
    s.supplier_id,
    s.company_name,
    COUNT(p.product_id) AS total_productos
FROM suppliers s
INNER JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.company_name
HAVING COUNT(p.product_id) > 3
ORDER BY total_productos DESC;
\echo ===DELIM_END_84===
\echo ===DELIM_START_85===
SELECT
    o.customer_id,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS facturacion_total
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
GROUP BY o.customer_id
HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 5000
ORDER BY facturacion_total DESC;
\echo ===DELIM_END_85===
\echo ===DELIM_START_86===
SELECT
    product_id,
    SUM(quantity) AS unidades_vendidas
FROM order_details
GROUP BY product_id
HAVING SUM(quantity) > 200
ORDER BY unidades_vendidas DESC;
\echo ===DELIM_END_86===
\echo ===DELIM_START_87===
SELECT
    EXTRACT(YEAR FROM order_date)::int AS anio,
    COUNT(*) AS total_pedidos
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date)
HAVING COUNT(*) > 100
ORDER BY anio;
\echo ===DELIM_END_87===
\echo ===DELIM_START_88===
SELECT
    ship_country,
    ROUND(AVG(freight)::numeric, 2) AS flete_promedio,
    COUNT(*) AS total_pedidos
FROM orders
GROUP BY ship_country
HAVING AVG(freight) > 50
ORDER BY flete_promedio DESC;
\echo ===DELIM_END_88===
\echo ===DELIM_START_89===
SELECT
    city,
    COUNT(*) AS total_empleados
FROM employees
GROUP BY city
HAVING COUNT(*) > 1
ORDER BY total_empleados DESC;
\echo ===DELIM_END_89===
\echo ===DELIM_START_90===
SELECT
    category_id,
    ROUND(AVG(unit_price)::numeric, 2) AS precio_promedio,
    COUNT(*) AS total_productos
FROM products
GROUP BY category_id
HAVING AVG(unit_price) > 25
ORDER BY precio_promedio DESC;
\echo ===DELIM_END_90===
\echo ===DELIM_START_91===
SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE unit_price = (
    SELECT MAX(unit_price)
    FROM products
);
\echo ===DELIM_END_91===
\echo ===DELIM_START_92===
SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE supplier_id IN (
    SELECT supplier_id
    FROM suppliers
    WHERE country = 'Japan'
)
ORDER BY product_name;
\echo ===DELIM_END_92===
\echo ===DELIM_START_93===
SELECT
    product_name,
    unit_price,
    category_id
FROM products p1
WHERE unit_price > (
    SELECT AVG(unit_price)
    FROM products p2
    WHERE p2.category_id = p1.category_id
)
ORDER BY category_id, unit_price DESC;
\echo ===DELIM_END_93===
\echo ===DELIM_START_94===
SELECT
    ROUND(AVG(total_productos)::numeric, 2) AS promedio_items_por_pedido
FROM (
    SELECT
        order_id,
        COUNT(product_id) AS total_productos
    FROM order_details
    GROUP BY order_id
) AS pedido_counts;
\echo ===DELIM_END_94===
\echo ===DELIM_START_95===
SELECT
    customer_id,
    company_name,
    country
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
)
ORDER BY company_name;
\echo ===DELIM_END_95===
\echo ===DELIM_START_96===
SELECT
    product_id,
    product_name,
    unit_price
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_details od
    WHERE od.product_id = p.product_id
);
\echo ===DELIM_END_96===
\echo ===DELIM_START_97===
SELECT
    product_id,
    product_name,
    unit_price,
    category_id
FROM products
WHERE unit_price > ANY (
    SELECT unit_price
    FROM products
    WHERE category_id = 1
)
ORDER BY unit_price;
\echo ===DELIM_END_97===
\echo ===DELIM_START_98===
SELECT
    product_id,
    product_name,
    unit_price,
    category_id
FROM products
WHERE unit_price > ALL (
    SELECT unit_price
    FROM products
    WHERE category_id = 1
)
ORDER BY unit_price;
\echo ===DELIM_END_98===
\echo ===DELIM_START_99===
SELECT
    customer_id,
    company_name,
    (
        SELECT MAX(order_date)
        FROM orders o
        WHERE o.customer_id = c.customer_id
    ) AS ultima_compra
FROM customers c
ORDER BY ultima_compra DESC NULLS LAST;
\echo ===DELIM_END_99===
\echo ===DELIM_START_100===
SELECT
    p.product_id,
    p.product_name,
    r.ingresos_totales
FROM (
    SELECT
        product_id,
        ROUND(SUM(quantity * unit_price * (1 - discount))::numeric, 2) AS ingresos_totales
    FROM order_details
    GROUP BY product_id
    ORDER BY ingresos_totales DESC
    LIMIT 5
) r
INNER JOIN products p ON r.product_id = p.product_id
ORDER BY r.ingresos_totales DESC;
\echo ===DELIM_END_100===
\echo ===DELIM_START_101===
SELECT
    product_name,
    unit_price,
    CASE
        WHEN unit_price < 20 THEN 'Económico'
        WHEN unit_price <= 50 THEN 'Intermedio'
        ELSE 'Premium'
    END AS categoria_costo
FROM products
ORDER BY unit_price;
\echo ===DELIM_END_101===
\echo ===DELIM_START_102===
SELECT
    company_name,
    country,
    CASE
        WHEN country IN ('USA', 'Canada', 'Mexico') THEN 'Norteamérica'
        WHEN country IN ('UK', 'Germany', 'France', 'Spain', 'Italy') THEN 'Europa'
        ELSE 'Resto del Mundo'
    END AS zona_logistica
FROM customers
ORDER BY country;
\echo ===DELIM_END_102===
\echo ===DELIM_START_103===
SELECT
    COUNT(*) FILTER (
        WHERE country IN ('USA', 'Canada', 'Mexico')
    ) AS norteamerica,
    COUNT(*) FILTER (
        WHERE country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
    ) AS europa,
    COUNT(*) FILTER (
        WHERE country NOT IN ('USA', 'Canada', 'Mexico', 'UK', 'Germany', 'France', 'Spain', 'Italy')
    ) AS resto_del_mundo
FROM customers;
\echo ===DELIM_END_103===
\echo ===DELIM_START_104===
SELECT
    o.customer_id,
    ROUND(SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1996
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS ventas_1996,
    ROUND(SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1997
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS ventas_1997,
    ROUND(SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1998
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS ventas_1998
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
\echo ===DELIM_END_104===
\echo ===DELIM_START_105===
SELECT
    employee_id,
    first_name || ' ' || last_name AS nombre_completo,
    EXTRACT(YEAR FROM AGE(hire_date))::int AS anios_antiguedad,
    CASE
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 30 THEN 'Veterano'
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 20 THEN 'Senior'
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 10 THEN 'Experimentado'
        ELSE 'Nuevo'
    END AS categoria_antiguedad
FROM employees
ORDER BY anios_antiguedad DESC;
\echo ===DELIM_END_105===
\echo ===DELIM_START_106===
SELECT
    customer_id,
    company_name,
    country
FROM customers
ORDER BY
    CASE
        WHEN country = 'USA' THEN 1
        WHEN country = 'Germany' THEN 2
        WHEN country = 'UK' THEN 3
        ELSE 4
    END,
    country;
\echo ===DELIM_END_106===
\echo ===DELIM_START_107===
SELECT
    o.employee_id,
    ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 1
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS q1,
    ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 2
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS q2,
    ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 3
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS q3,
    ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 4
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS q4,
    COUNT(*) FILTER (WHERE od.discount > 0) AS pedidos_con_descuento
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
GROUP BY o.employee_id
ORDER BY o.employee_id;
\echo ===DELIM_END_107===
\echo ===DELIM_START_108===
SELECT
    category_id,
    COUNT(*) AS total_productos,
    SUM(CASE WHEN unit_price > 30 THEN 1 ELSE 0 END) AS productos_caros,
    ROUND(
        SUM(CASE WHEN unit_price > 30 THEN 1 ELSE 0 END)::numeric
        / COUNT(*)::numeric * 100, 2
    ) AS porcentaje_caros
FROM products
GROUP BY category_id
HAVING SUM(CASE WHEN unit_price > 30 THEN 1 ELSE 0 END) >= 3
ORDER BY porcentaje_caros DESC;
\echo ===DELIM_END_108===
\echo ===DELIM_START_109===
SELECT
    order_id,
    product_id,
    discount,
    CASE
        WHEN discount = 0 THEN 'Precio completo'
        ELSE
            CASE
                WHEN discount <= 0.05 THEN 'Mínima promoción'
                WHEN discount <= 0.15 THEN 'Promoción media'
                ELSE 'Alta promoción'
            END
    END AS tipo_descuento
FROM order_details
ORDER BY discount DESC;
\echo ===DELIM_END_109===
\echo ===DELIM_START_110===
SELECT
    o.employee_id,
    ROUND(SUM(CASE WHEN o.ship_country IN ('USA', 'Canada', 'Mexico')
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS norteamerica,
    ROUND(SUM(CASE WHEN o.ship_country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS europa,
    ROUND(SUM(CASE WHEN o.ship_country IN ('Argentina', 'Brazil', 'Venezuela')
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS latam,
    ROUND(SUM(CASE WHEN o.ship_country NOT IN ('USA', 'Canada', 'Mexico', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Argentina', 'Brazil', 'Venezuela')
              THEN od.quantity * od.unit_price * (1 - od.discount) ELSE 0 END)::numeric, 2) AS resto_mundo
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
GROUP BY o.employee_id
ORDER BY o.employee_id;
\echo ===DELIM_END_110===
\echo ===DELIM_START_111===
SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo_empleado,
    m.first_name || ' ' || m.last_name AS manager,
    m.title AS cargo_manager
FROM employees e
INNER JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;
\echo ===DELIM_END_111===
\echo ===DELIM_START_112===
SELECT
    e1.employee_id AS empleado1_id,
    e1.first_name || ' ' || e1.last_name AS empleado1,
    e2.employee_id AS empleado2_id,
    e2.first_name || ' ' || e2.last_name AS empleado2,
    e1.reports_to AS manager_id
FROM employees e1
INNER JOIN employees e2 ON e1.reports_to = e2.reports_to
    AND e1.employee_id < e2.employee_id
ORDER BY e1.reports_to, e1.employee_id;
\echo ===DELIM_END_112===
\echo ===DELIM_START_113===
SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name AS empleado,
    et.territory_id
FROM employees e
FULL OUTER JOIN employee_territories et ON e.employee_id = et.employee_id
ORDER BY e.employee_id NULLS LAST, et.territory_id NULLS LAST;
\echo ===DELIM_END_113===
\echo ===DELIM_START_114===
SELECT
    c.customer_id AS id_cliente,
    c.company_name,
    o.order_id,
    o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id NULLS LAST, o.order_id NULLS LAST;
\echo ===DELIM_END_114===
\echo ===DELIM_START_115===
SELECT
    od.order_id,
    p.product_name,
    c.category_name,
    s.company_name AS proveedor,
    o.order_date,
    od.quantity,
    od.unit_price
FROM order_details od
INNER JOIN products p ON od.product_id = p.product_id
INNER JOIN categories c ON p.category_id = c.category_id
INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
INNER JOIN orders o ON od.order_id = o.order_id
ORDER BY od.order_id, p.product_name;
\echo ===DELIM_END_115===
\echo ===DELIM_START_116===
SELECT
    o.order_id,
    o.order_date,
    c.company_name AS cliente,
    e.first_name || ' ' || e.last_name AS empleado,
    s.company_name AS transportista,
    o.freight
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN employees e ON o.employee_id = e.employee_id
INNER JOIN shippers s ON o.ship_via = s.shipper_id
ORDER BY o.order_date DESC
LIMIT 20;
\echo ===DELIM_END_116===
\echo ===DELIM_START_117===
SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name AS empleado,
    o.order_id,
    o.order_date
FROM orders o
RIGHT JOIN employees e ON o.employee_id = e.employee_id
ORDER BY e.employee_id;
\echo ===DELIM_END_117===
\echo ===DELIM_START_118===
SELECT
    p.product_name,
    c.category_name,
    p.unit_price
FROM products p
CROSS JOIN categories c
WHERE p.category_id = c.category_id
ORDER BY c.category_name, p.product_name;
\echo ===DELIM_END_118===
\echo ===DELIM_START_119===
SELECT
    o.order_id,
    o.order_date,
    od.product_id,
    od.discount
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
    AND od.discount > 0
ORDER BY od.discount DESC;
\echo ===DELIM_END_119===
\echo ===DELIM_START_120===
SELECT
    c.customer_id,
    c.company_name,
    ultimo_pedido.order_id,
    ultimo_pedido.order_date
FROM customers c
CROSS JOIN LATERAL (
    SELECT o.order_id, o.order_date
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    LIMIT 1
) ultimo_pedido
ORDER BY ultimo_pedido.order_date DESC;
\echo ===DELIM_END_120===
\echo ===DELIM_START_121===
SELECT
    product_name,
    unit_price,
    ROW_NUMBER() OVER (ORDER BY unit_price DESC) AS ranking_secuencial
FROM products
ORDER BY ranking_secuencial;
\echo ===DELIM_END_121===
\echo ===DELIM_START_122===
SELECT
    category_id,
    product_name,
    unit_price,
    RANK() OVER (PARTITION BY category_id ORDER BY unit_price DESC) AS rango_con_saltos,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY unit_price DESC) AS rango_sin_saltos
FROM products
ORDER BY category_id, rango_con_saltos;
\echo ===DELIM_END_122===
\echo ===DELIM_START_123===
WITH ranked_products AS (
    SELECT
        category_id,
        product_id,
        product_name,
        unit_price,
        ROW_NUMBER() OVER (
            PARTITION BY category_id
            ORDER BY unit_price DESC
        ) AS rn
    FROM products
)
SELECT
    rp.category_id,
    c.category_name,
    rp.product_name,
    rp.unit_price,
    rp.rn
FROM ranked_products rp
INNER JOIN categories c ON rp.category_id = c.category_id
WHERE rp.rn <= 3
ORDER BY rp.category_id, rp.rn;
\echo ===DELIM_END_123===
\echo ===DELIM_START_124===
SELECT
    customer_id,
    order_id,
    order_date,
    LAG(order_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS fecha_pedido_anterior,
    order_date - LAG(order_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS dias_entre_pedidos
FROM orders
ORDER BY customer_id, order_date;
\echo ===DELIM_END_124===
\echo ===DELIM_START_125===
SELECT
    customer_id,
    order_id,
    order_date,
    LEAD(order_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS fecha_proximo_pedido
FROM orders
ORDER BY customer_id, order_date;
\echo ===DELIM_END_125===
\echo ===DELIM_START_126===
WITH monthly_revenue AS (
    SELECT
        TO_CHAR(o.order_date, 'YYYY-MM') AS periodo_mes,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ingresos_mes
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
)
SELECT
    periodo_mes,
    ingresos_mes,
    ROUND(SUM(ingresos_mes) OVER (
        ORDER BY periodo_mes
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ingresos_acumulados
FROM monthly_revenue
ORDER BY periodo_mes;
\echo ===DELIM_END_126===
\echo ===DELIM_START_127===
SELECT
    product_name,
    category_id,
    unit_price,
    ROUND(AVG(unit_price) OVER (PARTITION BY category_id)::numeric, 2) AS promedio_categoria,
    ROUND((unit_price - AVG(unit_price) OVER (PARTITION BY category_id))::numeric, 2) AS desviacion_promedio
FROM products
ORDER BY category_id, unit_price;
\echo ===DELIM_END_127===
\echo ===DELIM_START_128===
SELECT
    category_id,
    product_name,
    unit_price,
    FIRST_VALUE(product_name) OVER (
        PARTITION BY category_id
        ORDER BY unit_price DESC
    ) AS producto_mas_caro,
    LAST_VALUE(unit_price) OVER (
        PARTITION BY category_id
        ORDER BY unit_price DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS precio_mas_barato
FROM products
ORDER BY category_id, unit_price DESC;
\echo ===DELIM_END_128===
\echo ===DELIM_START_129===
WITH customer_orders AS (
    SELECT
        c.customer_id,
        c.company_name,
        COUNT(o.order_id) AS total_pedidos
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.company_name
)
SELECT
    customer_id,
    company_name,
    total_pedidos,
    NTILE(4) OVER (ORDER BY total_pedidos DESC) AS cuartil
FROM customer_orders
ORDER BY cuartil, total_pedidos DESC;
\echo ===DELIM_END_129===
\echo ===DELIM_START_130===
SELECT
    order_id,
    product_id,
    quantity,
    discount,
    SUM(quantity) FILTER (WHERE discount > 0) OVER (
        PARTITION BY product_id
        ORDER BY order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS unidades_con_descuento_acumuladas
FROM order_details
ORDER BY product_id, order_id;
\echo ===DELIM_END_130===
\echo ===DELIM_START_131===
WITH ventas_por_cliente AS (
    SELECT
        o.customer_id,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total_gastado,
        COUNT(DISTINCT o.order_id) AS num_pedidos
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.customer_id
)
SELECT
    c.company_name,
    ROUND(v.total_gastado::numeric, 2) AS total_gastado,
    v.num_pedidos,
    ROUND((v.total_gastado / NULLIF(v.num_pedidos, 0))::numeric, 2) AS ticket_promedio
FROM ventas_por_cliente v
INNER JOIN customers c ON v.customer_id = c.customer_id
ORDER BY v.total_gastado DESC
LIMIT 10;
\echo ===DELIM_END_131===
\echo ===DELIM_START_132===
WITH ingresos_mensuales AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingresos
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY DATE_TRUNC('month', o.order_date)
),
fletes_mensuales AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS mes,
        SUM(freight) AS costo_flete
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    i.mes,
    ROUND(i.ingresos::numeric, 2) AS ingresos,
    ROUND(f.costo_flete::numeric, 2) AS flete,
    ROUND((i.ingresos - COALESCE(f.costo_flete, 0))::numeric, 2) AS ingreso_neto,
    ROUND((COALESCE(f.costo_flete, 0) / NULLIF(i.ingresos, 0) * 100)::numeric, 2) AS pct_flete
FROM ingresos_mensuales i
LEFT JOIN fletes_mensuales f ON i.mes = f.mes
ORDER BY i.mes;
\echo ===DELIM_END_132===
\echo ===DELIM_START_133===
WITH metricas_empleados AS MATERIALIZED (
    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name AS nombre,
        e.hire_date,
        COUNT(DISTINCT o.order_id) AS pedidos_gestionados,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingresos_generados,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS antiguedad_anios
    FROM employees e
    INNER JOIN orders o ON e.employee_id = o.employee_id
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY e.employee_id
)
SELECT nombre, pedidos_gestionados, ROUND(ingresos_generados::numeric, 2) AS ingresos, antiguedad_anios
FROM metricas_empleados
ORDER BY ingresos_generados DESC;
\echo ===DELIM_END_133===
\echo ===DELIM_START_134===
WITH pedidos_ordenados AS NOT MATERIALIZED (
    SELECT
        o.customer_id,
        o.order_id,
        o.order_date,
        o.freight,
        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC, o.order_id DESC
        ) AS rn
    FROM orders o
)
SELECT
    c.company_name,
    po.order_id,
    po.order_date,
    ROUND(po.freight::numeric, 2) AS freight
FROM customers c
INNER JOIN pedidos_ordenados po ON c.customer_id = po.customer_id
WHERE po.rn <= 3
ORDER BY c.company_name, po.order_date DESC;
\echo ===DELIM_END_134===
\echo ===DELIM_START_135===
WITH ventas_trimestrales AS (
    SELECT
        c.category_name,
        SUM(od.quantity * od.unit_price * (1 - od.discount))
            FILTER (WHERE EXTRACT(QUARTER FROM o.order_date) = 1) AS ingreso_q1,
        SUM(od.quantity * od.unit_price * (1 - od.discount))
            FILTER (WHERE EXTRACT(QUARTER FROM o.order_date) = 2) AS ingreso_q2,
        SUM(od.quantity * od.unit_price * (1 - od.discount))
            FILTER (WHERE EXTRACT(QUARTER FROM o.order_date) = 3) AS ingreso_q3,
        SUM(od.quantity * od.unit_price * (1 - od.discount))
            FILTER (WHERE EXTRACT(QUARTER FROM o.order_date) = 4) AS ingreso_q4,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total_anual
    FROM categories c
    INNER JOIN products p ON c.category_id = p.category_id
    INNER JOIN order_details od ON p.product_id = od.product_id
    INNER JOIN orders o ON od.order_id = o.order_id
    GROUP BY c.category_name
)
SELECT *
FROM ventas_trimestrales
ORDER BY total_anual DESC;
\echo ===DELIM_END_135===
\echo ===DELIM_START_136===
WITH productos_activos AS (
    SELECT DISTINCT od.product_id
    FROM order_details od
    INNER JOIN orders o ON od.order_id = o.order_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '90 days'
)
SELECT
    p.product_id,
    p.product_name,
    p.units_in_stock,
    p.discontinued
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM productos_activos pa
    WHERE pa.product_id = p.product_id
)
ORDER BY p.product_name;
\echo ===DELIM_END_136===
\echo ===DELIM_START_137===
WITH estado_inventario AS (
    SELECT
        product_id,
        product_name,
        units_in_stock,
        units_on_order,
        reorder_level,
        discontinued,
        (units_in_stock - units_on_order) AS inventario_neto,
        CASE
            WHEN (units_in_stock - units_on_order) <= 0 THEN 'CRITICO'
            WHEN (units_in_stock - units_on_order) <= reorder_level * 0.5 THEN 'URGENTE'
            WHEN (units_in_stock - units_on_order) <= reorder_level THEN 'ALERTA'
            ELSE 'NORMAL'
        END AS prioridad
    FROM products
)
SELECT *
FROM estado_inventario
WHERE prioridad IN ('CRITICO', 'URGENTE', 'ALERTA')
  AND discontinued = 0
ORDER BY
    CASE prioridad
        WHEN 'CRITICO' THEN 1
        WHEN 'URGENTE' THEN 2
        WHEN 'ALERTA' THEN 3
    END,
    inventario_neto ASC;
\echo ===DELIM_END_137===
\echo ===DELIM_START_138===
WITH diagnostico_tablas AS (
    SELECT
        schemaname,
        relname,
        n_live_tup,
        n_dead_tup,
        n_mod_since_analyze,
        last_analyze,
        last_autoanalyze,
        pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS tamano
    FROM pg_stat_user_tables
    WHERE schemaname = 'public'
)
SELECT *,
    ROUND((n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100), 2) AS pct_tuplas_muertas
FROM diagnostico_tablas
WHERE (n_dead_tup > 1000 AND n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) > 0.1)
   OR (n_mod_since_analyze > 10000 AND last_analyze IS NULL)
   OR (last_analyze IS NOT NULL AND last_analyze < CURRENT_TIMESTAMP - INTERVAL '1 day')
ORDER BY n_dead_tup DESC;
\echo ===DELIM_END_138===
\echo ===DELIM_START_139===
BEGIN;

WITH ajuste_origen AS (
    UPDATE products
    SET units_in_stock = units_in_stock - 10
    WHERE product_id = 1 AND units_in_stock >= 10
    RETURNING product_id, product_name, units_in_stock AS stock_origen_restante
),
ajuste_destino AS (
    UPDATE products
    SET units_in_stock = units_in_stock + 10
    WHERE product_id = 2
    RETURNING product_id, product_name, units_in_stock AS stock_destino_nuevo
)
SELECT
    ao.product_name AS producto_origen,
    ao.stock_origen_restante,
    ad.product_name AS producto_destino,
    ad.stock_destino_nuevo,
    10 AS cantidad_transferida
FROM ajuste_origen ao, ajuste_destino ad;

COMMIT;
\echo ===DELIM_END_139===
\echo ===DELIM_START_140===
WITH datos_nuevos (customer_id, company_name, contact_name, city, country) AS (
    VALUES
        ('NWE01', 'TechCorp Peru', 'Carlos Garcia', 'Lima', 'Peru'),
        ('NWE02', 'DataLabs Chile', 'Ana Soto', 'Santiago', 'Chile'),
        ('ALFKI', 'Alfreds Futterkiste - Actualizado', 'Maria Anders', 'Berlin', 'Germany')
)
INSERT INTO customers (customer_id, company_name, contact_name, city, country)
SELECT customer_id, company_name, contact_name, city, country
FROM datos_nuevos
ON CONFLICT (customer_id) DO UPDATE SET
    company_name = EXCLUDED.company_name,
    contact_name = EXCLUDED.contact_name,
    city = EXCLUDED.city,
    country = EXCLUDED.country
RETURNING customer_id, company_name, (xmax = 0) AS fue_insertado;
\echo ===DELIM_END_140===
\echo ===DELIM_START_141===
WITH RECURSIVE organigrama AS (
    SELECT
        employee_id,
        first_name || ' ' || last_name AS nombre,
        reports_to,
        0 AS nivel,
        first_name || ' ' || last_name AS ruta
    FROM employees
    WHERE reports_to IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name,
        e.reports_to,
        o.nivel + 1,
        o.ruta || ' -> ' || e.first_name || ' ' || e.last_name
    FROM employees e
    INNER JOIN organigrama o ON e.reports_to = o.employee_id
)
SELECT
    nivel,
    REPEAT('  ', nivel) || nombre AS nombre_jerarquico,
    ruta
FROM organigrama
ORDER BY ruta;
\echo ===DELIM_END_141===
\echo ===DELIM_START_142===
WITH RECURSIVE subordinados AS (
    SELECT
        employee_id,
        first_name || ' ' || last_name AS nombre,
        reports_to,
        1 AS nivel,
        first_name || ' ' || last_name AS ruta
    FROM employees
    WHERE reports_to = 2

    UNION ALL

    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name,
        e.reports_to,
        s.nivel + 1,
        s.ruta || ' -> ' || e.first_name || ' ' || e.last_name
    FROM employees e
    INNER JOIN subordinados s ON e.reports_to = s.employee_id
)
SELECT
    nivel,
    REPEAT('  ', nivel - 1) || nombre AS jerarquia,
    ruta
FROM subordinados
ORDER BY ruta;
\echo ===DELIM_END_142===
\echo ===DELIM_START_143===
WITH RECURSIVE calendario AS (
    SELECT '1997-01-01'::date AS fecha

    UNION ALL

    SELECT fecha + 1
    FROM calendario
    WHERE fecha < '1997-12-31'::date
)
SELECT
    fecha,
    TO_CHAR(fecha, 'Day') AS dia_semana,
    EXTRACT(ISODOW FROM fecha) AS num_dia_semana,
    CASE
        WHEN EXTRACT(ISODOW FROM fecha) BETWEEN 1 AND 5 THEN TRUE
        ELSE FALSE
    END AS es_laborable
FROM calendario
ORDER BY fecha;
\echo ===DELIM_END_143===
\echo ===DELIM_START_144===
WITH RECURSIVE equipo AS (
    SELECT employee_id AS lider_id, employee_id AS miembro_id, 0 AS profundidad
    FROM employees

    UNION ALL

    SELECT
        e.lider_id,
        emp.employee_id,
        e.profundidad + 1
    FROM equipo e
    INNER JOIN employees emp ON emp.reports_to = e.miembro_id
    WHERE e.profundidad < 10
)
SELECT
    l.employee_id,
    l.first_name || ' ' || l.last_name AS lider,
    COUNT(DISTINCT e.miembro_id) AS total_equipo,
    ROUND(SUM(COALESCE(od_sub.ingresos, 0))::numeric, 2) AS ingresos_del_equipo
FROM employees l
INNER JOIN equipo e ON l.employee_id = e.lider_id
LEFT JOIN LATERAL (
    SELECT SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingresos
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    WHERE o.employee_id = e.miembro_id
) od_sub ON TRUE
GROUP BY l.employee_id, l.first_name, l.last_name
ORDER BY ingresos_del_equipo DESC;
\echo ===DELIM_END_144===
\echo ===DELIM_START_145===
WITH RECURSIVE red_territorios AS (
    SELECT DISTINCT
        et.territory_id,
        et.employee_id,
        0 AS profundidad,
        ARRAY[et.territory_id]::text[] AS territorios_visitados
    FROM employee_territories et
    WHERE et.employee_id = 1

    UNION ALL

    SELECT
        et.territory_id,
        et.employee_id,
        r.profundidad + 1,
        r.territorios_visitados || et.territory_id::text
    FROM employee_territories et
    INNER JOIN red_territorios r ON et.employee_id = r.employee_id
    WHERE NOT (et.territory_id = ANY(r.territorios_visitados))
      AND r.profundidad < 3
)
SELECT
    t.territory_description,
    r.employee_id,
    r.profundidad,
    array_to_string(r.territorios_visitados, ' -> ') AS ruta_territorios
FROM red_territorios r
INNER JOIN territories t ON r.territory_id = t.territory_id
ORDER BY r.profundidad, r.territory_id;
\echo ===DELIM_END_145===
\echo ===DELIM_START_146===
WITH RECURSIVE cadena_mando AS (
    SELECT
        employee_id,
        first_name || ' ' || last_name AS nombre,
        reports_to,
        0 AS nivel,
        first_name || ' ' || last_name AS ruta
    FROM employees
    WHERE employee_id = 8

    UNION ALL

    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name,
        e.reports_to,
        cm.nivel + 1,
        cm.ruta || ' <- ' || e.first_name || ' ' || e.last_name
    FROM employees e
    INNER JOIN cadena_mando cm ON e.employee_id = cm.reports_to
)
SELECT
    nombre,
    CASE
        WHEN nivel = 0 THEN 'EMPLEADO INICIAL'
        WHEN reports_to IS NULL THEN 'CEO'
        ELSE 'Nivel ' || nivel
    END AS rol,
    ruta
FROM cadena_mando
ORDER BY nivel DESC;
\echo ===DELIM_END_146===
\echo ===DELIM_START_147===
WITH RECURSIVE gerentes_y_equipos AS (
    -- Ancla: empleados que son gerentes (su ID aparece en reports_to de otros)
    SELECT
        employee_id,
        first_name || ' ' || last_name AS nombre,
        reports_to,
        employee_id AS gerente_raiz_id,
        first_name || ' ' || last_name AS nombre_gerente_raiz,
        0 AS nivel
    FROM employees
    WHERE employee_id IN (SELECT DISTINCT reports_to FROM employees WHERE reports_to IS NOT NULL)

    UNION ALL

    -- Recursión: subordinados
    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name,
        e.reports_to,
        g.gerente_raiz_id,
        g.nombre_gerente_raiz,
        g.nivel + 1
    FROM employees e
    INNER JOIN gerentes_y_equipos g ON e.reports_to = g.employee_id
)
SELECT
    nombre_gerente_raiz,
    nivel,
    REPEAT('  ', nivel) || nombre AS miembro_equipo,
    reports_to
FROM gerentes_y_equipos
ORDER BY nombre_gerente_raiz, nivel, nombre;
\echo ===DELIM_END_147===
\echo ===DELIM_START_148===
WITH RECURSIVE jerarquia_categorias AS (
    SELECT
        category_id,
        category_name,
        NULL::int AS parent_category_id,
        0 AS nivel,
        category_name::text AS ruta
    FROM categories
    WHERE category_id IN (1, 2)

    UNION ALL

    SELECT
        c.category_id,
        c.category_name,
        j.category_id,
        j.nivel + 1,
        j.ruta || ' -> ' || c.category_name
    FROM categories c
    INNER JOIN jerarquia_categorias j ON c.category_id = j.category_id + 2
    WHERE j.nivel < 2
)
SELECT
    nivel,
    REPEAT('  ', nivel) || category_name AS categoria,
    ruta
FROM jerarquia_categorias
ORDER BY ruta;
\echo ===DELIM_END_148===
\echo ===DELIM_START_149===
WITH RECURSIVE exploracion_segura AS (
    SELECT
        employee_id,
        first_name || ' ' || last_name AS nombre,
        reports_to,
        0 AS nivel,
        ARRAY[employee_id] AS visitados,
        FALSE AS tiene_ciclo
    FROM employees
    WHERE reports_to IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name,
        e.reports_to,
        es.nivel + 1,
        es.visitados || e.employee_id,
        e.employee_id = ANY(es.visitados)
    FROM employees e
    INNER JOIN exploracion_segura es ON e.reports_to = es.employee_id
    WHERE NOT es.tiene_ciclo
      AND es.nivel < 20
)
SELECT
    nivel,
    REPEAT('  ', nivel) || nombre AS jerarquia,
    CASE WHEN tiene_ciclo THEN 'CICLO DETECTADO' ELSE 'OK' END AS estado
FROM exploracion_segura
ORDER BY nivel, nombre;
\echo ===DELIM_END_149===
\echo ===DELIM_START_150===
WITH RECURSIVE proyeccion_mensual AS (
    SELECT
        DATE_TRUNC('month', MAX(o.order_date))::date AS mes_base,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas_reales,
        0 AS mes_proyectado
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    WHERE o.order_date >= '1998-01-01'
      AND o.order_date < '1998-02-01'

    UNION ALL

    SELECT
        (mes_base + INTERVAL '1 month' * (mes_proyectado + 1))::date,
        ventas_reales * (1.02 ^ (mes_proyectado + 1)),
        mes_proyectado + 1
    FROM proyeccion_mensual
    WHERE mes_proyectado < 11
)
SELECT
    mes_base + INTERVAL '1 month' * mes_proyectado AS mes_proyectado,
    ROUND(ventas_reales::numeric, 2) AS ventas_estimadas,
    ROUND((ventas_reales / NULLIF(FIRST_VALUE(ventas_reales) OVER (ORDER BY mes_proyectado), 0) * 100 - 100)::numeric, 2) AS crecimiento_acumulado_pct
FROM proyeccion_mensual
ORDER BY mes_proyectado;
\echo ===DELIM_END_150===
\echo ===DELIM_START_151===
WITH ventas_mensuales_emp AS (
    SELECT
        o.employee_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.employee_id, DATE_TRUNC('month', o.order_date)
)
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    v.mes,
    ROUND(v.ventas::numeric, 2) AS ventas_mes,
    ROUND(LAG(v.ventas) OVER (PARTITION BY v.employee_id ORDER BY v.mes)::numeric, 2) AS ventas_mes_anterior,
    ROUND((v.ventas - LAG(v.ventas) OVER (PARTITION BY v.employee_id ORDER BY v.mes))::numeric, 2) AS diferencia,
    ROUND(((v.ventas - LAG(v.ventas) OVER (PARTITION BY v.employee_id ORDER BY v.mes)) / NULLIF(LAG(v.ventas) OVER (PARTITION BY v.employee_id ORDER BY v.mes), 0) * 100)::numeric, 2) AS variacion_pct
FROM ventas_mensuales_emp v
INNER JOIN employees e ON v.employee_id = e.employee_id
ORDER BY empleado, v.mes;
\echo ===DELIM_END_151===
\echo ===DELIM_START_152===
WITH frecuencia_cliente AS (
    SELECT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        COUNT(DISTINCT o.order_id) AS pedidos
    FROM orders o
    GROUP BY o.customer_id, DATE_TRUNC('month', o.order_date)
),
tendencia_cliente AS (
    SELECT
        customer_id,
        mes,
        pedidos,
        LEAD(pedidos) OVER (PARTITION BY customer_id ORDER BY mes) AS pedidos_siguiente_mes,
        LEAD(mes) OVER (PARTITION BY customer_id ORDER BY mes) AS mes_siguiente
    FROM frecuencia_cliente
)
SELECT
    c.company_name,
    tc.mes,
    tc.pedidos,
    tc.pedidos_siguiente_mes,
    tc.mes_siguiente,
    ROUND((tc.pedidos_siguiente_mes::numeric / NULLIF(tc.pedidos, 0) * 100), 2) AS tasa_retencion_pct
FROM tendencia_cliente tc
INNER JOIN customers c ON tc.customer_id = c.customer_id
WHERE tc.pedidos_siguiente_mes IS NOT NULL
  AND (tc.pedidos_siguiente_mes::numeric / NULLIF(tc.pedidos, 0)) < 0.5
ORDER BY tasa_retencion_pct ASC;
\echo ===DELIM_END_152===
\echo ===DELIM_START_153===
WITH ventas_diarias AS (
    SELECT
        o.order_date::date AS fecha,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS venta
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.order_date::date
)
SELECT
    fecha,
    ROUND(venta::numeric, 2) AS venta_diaria,
    ROUND(AVG(venta) OVER (
        ORDER BY fecha
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS promedio_movil_7dias,
    ROUND((venta - AVG(venta) OVER (
        ORDER BY fecha
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ))::numeric, 2) AS desviacion_diaria,
    CASE
        WHEN venta > AVG(venta) OVER (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) * 1.5 THEN 'PICO'
        WHEN venta < AVG(venta) OVER (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) * 0.5 THEN 'CAIDA'
        ELSE 'NORMAL'
    END AS tendencia
FROM ventas_diarias
ORDER BY fecha;
\echo ===DELIM_END_153===
\echo ===DELIM_START_154===
WITH meses AS (
    SELECT generate_series(
        '1996-07-01'::date,
        '1998-05-01'::date,
        '1 month'::interval
    )::date AS mes
),
ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY DATE_TRUNC('month', o.order_date)
)
SELECT
    m.mes,
    COALESCE(ROUND(v.ventas::numeric, 2), 0) AS ventas_mes,
    ROUND(SUM(COALESCE(v.ventas, 0)) OVER (
        ORDER BY m.mes
        RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ventas_acumuladas,
    ROUND(AVG(COALESCE(v.ventas, 0)) OVER (
        ORDER BY m.mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS promedio_movil_3meses
FROM meses m
LEFT JOIN ventas_mensuales v ON m.mes = v.mes
ORDER BY m.mes;
\echo ===DELIM_END_154===
\echo ===DELIM_START_155===
WITH productos_por_categoria AS (
    SELECT
        p.category_id,
        c.category_name,
        p.product_name,
        p.unit_price,
        FIRST_VALUE(p.product_name) OVER (
            PARTITION BY p.category_id
            ORDER BY p.unit_price DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS producto_mas_caro,
        FIRST_VALUE(p.unit_price) OVER (
            PARTITION BY p.category_id
            ORDER BY p.unit_price DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS precio_maximo
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
),
ranking AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY category_id
            ORDER BY unit_price DESC
        ) AS rn
    FROM productos_por_categoria
)
SELECT category_name, product_name, unit_price, precio_maximo
FROM ranking
WHERE rn = 1
ORDER BY category_name;
\echo ===DELIM_END_155===
\echo ===DELIM_START_156===
WITH precios_categoria AS (
    SELECT
        p.category_id,
        c.category_name,
        p.product_name,
        p.unit_price,
        LAST_VALUE(p.product_name) OVER (
            PARTITION BY p.category_id
            ORDER BY p.unit_price DESC
            ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
        ) AS producto_mas_barato,
        LAST_VALUE(p.unit_price) OVER (
            PARTITION BY p.category_id
            ORDER BY p.unit_price DESC
            ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
        ) AS precio_minimo
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
)
SELECT DISTINCT category_name, producto_mas_barato, precio_minimo
FROM precios_categoria
ORDER BY category_name;
\echo ===DELIM_END_156===
\echo ===DELIM_START_157===
WITH ventas_producto AS (
    SELECT
        p.category_id,
        c.category_name,
        p.product_id,
        p.product_name,
        SUM(od.quantity) AS total_unidades_vendidas
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
    INNER JOIN order_details od ON p.product_id = od.product_id
    GROUP BY p.category_id, c.category_name, p.product_id, p.product_name
),
ranking AS (
    SELECT *,
        NTH_VALUE(product_name, 3) OVER (
            PARTITION BY category_id
            ORDER BY total_unidades_vendidas DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS tercer_producto,
        NTH_VALUE(total_unidades_vendidas, 3) OVER (
            PARTITION BY category_id
            ORDER BY total_unidades_vendidas DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS ventas_tercero,
        ROW_NUMBER() OVER (
            PARTITION BY category_id
            ORDER BY total_unidades_vendidas DESC
        ) AS rn
    FROM ventas_producto
)
SELECT category_name, tercer_producto, ventas_tercero
FROM ranking
WHERE rn = 1
ORDER BY category_name;
\echo ===DELIM_END_157===
\echo ===DELIM_START_158===
WITH facturacion_clientes AS (
    SELECT
        o.customer_id,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total_facturado
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.customer_id
)
SELECT
    c.company_name,
    ROUND(total_facturado::numeric, 2) AS facturacion,
    ROW_NUMBER() OVER (ORDER BY total_facturado DESC) AS row_number,
    RANK() OVER (ORDER BY total_facturado DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY total_facturado DESC) AS dense_rank,
    CASE
        WHEN ROW_NUMBER() OVER (ORDER BY total_facturado DESC) <= 5 THEN 'TOP 5'
        WHEN DENSE_RANK() OVER (ORDER BY total_facturado DESC) <= 10 THEN 'TOP 10'
        ELSE 'ESTANDAR'
    END AS segmento
FROM facturacion_clientes fc
INNER JOIN customers c ON fc.customer_id = c.customer_id
ORDER BY facturacion DESC
LIMIT 20;
\echo ===DELIM_END_158===
\echo ===DELIM_START_159===
WITH rentabilidad_producto AS (
    SELECT
        p.product_id,
        p.product_name,
        c.category_name,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingresos,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) / NULLIF(SUM(od.quantity), 0) AS rentabilidad_por_unidad
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
    INNER JOIN order_details od ON p.product_id = od.product_id
    GROUP BY p.product_id, p.product_name, c.category_name
)
SELECT
    product_name,
    category_name,
    ROUND(ingresos::numeric, 2) AS ingresos_totales,
    ROUND(rentabilidad_por_unidad::numeric, 4) AS margen_unitario,
    NTILE(4) OVER (ORDER BY ingresos DESC) AS cuartil_ingresos,
    NTILE(4) OVER (ORDER BY rentabilidad_por_unidad DESC) AS cuartil_margen,
    CASE
        WHEN NTILE(4) OVER (ORDER BY ingresos DESC) = 1 AND NTILE(4) OVER (ORDER BY rentabilidad_por_unidad DESC) = 1
            THEN 'ESTRELLA'
        WHEN NTILE(4) OVER (ORDER BY ingresos DESC) = 4 AND NTILE(4) OVER (ORDER BY rentabilidad_por_unidad DESC) = 4
            THEN 'PERRO'
        ELSE 'INTERMEDIO'
    END AS clasificacion_matrix
FROM rentabilidad_producto
ORDER BY ingresos DESC;
\echo ===DELIM_END_159===
\echo ===DELIM_START_160===
WITH distribucion_precios AS (
    SELECT
        p.product_name,
        c.category_name,
        p.unit_price,
        PERCENT_RANK() OVER (ORDER BY p.unit_price DESC) AS percent_rank_precio,
        CUME_DIST() OVER (ORDER BY p.unit_price DESC) AS cume_dist_precio,
        ROW_NUMBER() OVER (ORDER BY p.unit_price DESC) AS posicion
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
)
SELECT
    product_name,
    category_name,
    unit_price,
    ROUND(percent_rank_precio::numeric, 4) AS percent_rank,
    ROUND(cume_dist_precio::numeric, 4) AS cume_dist,
    CASE
        WHEN percent_rank_precio <= 0.25 THEN 'CARO (top 25%)'
        WHEN percent_rank_precio <= 0.50 THEN 'MEDIO-ALTO'
        WHEN percent_rank_precio <= 0.75 THEN 'MEDIO-BAJO'
        ELSE 'ECONOMICO'
    END AS segmento_percentilar
FROM distribucion_precios
ORDER BY unit_price DESC;
\echo ===DELIM_END_160===
\echo ===DELIM_START_161===
SELECT
    c.category_name,
    p.product_name,
    p.unit_price
FROM categories c
CROSS JOIN LATERAL (
    SELECT product_name, unit_price
    FROM products
    WHERE category_id = c.category_id
    ORDER BY unit_price DESC
    LIMIT 3
) p
ORDER BY c.category_name, p.unit_price DESC;
\echo ===DELIM_END_161===
\echo ===DELIM_START_162===
SELECT
    c.company_name,
    c.country,
    ultimos_pedidos.order_id,
    ultimos_pedidos.order_date,
    ROUND(ultimos_pedidos.freight::numeric, 2) AS freight
FROM customers c
CROSS JOIN LATERAL (
    SELECT order_id, order_date, freight
    FROM orders
    WHERE customer_id = c.customer_id
    ORDER BY order_date DESC, order_id DESC
    LIMIT 5
) ultimos_pedidos
ORDER BY c.company_name, ultimos_pedidos.order_date DESC;
\echo ===DELIM_END_162===
\echo ===DELIM_START_163===
SELECT
    s.company_name AS proveedor,
    s.country,
    producto_estrella.product_name,
    producto_estrella.unit_price
FROM suppliers s
CROSS JOIN LATERAL (
    SELECT product_name, unit_price
    FROM products
    WHERE supplier_id = s.supplier_id
    ORDER BY unit_price DESC
    LIMIT 1
) producto_estrella
ORDER BY producto_estrella.unit_price DESC;
\echo ===DELIM_END_163===
\echo ===DELIM_START_164===
SELECT * FROM crosstab(
    $$
    SELECT
        c.category_name::text,
        EXTRACT(YEAR FROM o.order_date)::int AS anio,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ventas
    FROM categories c
    INNER JOIN products p ON c.category_id = p.category_id
    INNER JOIN order_details od ON p.product_id = od.product_id
    INNER JOIN orders o ON od.order_id = o.order_id
    WHERE o.order_date >= '1996-01-01' AND o.order_date < '1999-01-01'
    GROUP BY c.category_name, EXTRACT(YEAR FROM o.order_date)
    ORDER BY c.category_name, anio
    $$,
    $$ VALUES (1996), (1997), (1998) $$
) AS (
    category_name TEXT,
    ventas_1996 NUMERIC,
    ventas_1997 NUMERIC,
    ventas_1998 NUMERIC
)
ORDER BY category_name;
\echo ===DELIM_END_164===
\echo ===DELIM_START_165===
SELECT * FROM crosstab(
    $$
    SELECT
        customer_id::text,
        EXTRACT(MONTH FROM order_date)::int AS mes,
        COUNT(*)::int AS pedidos
    FROM orders
    WHERE order_date >= '1997-01-01' AND order_date < '1998-01-01'
    GROUP BY customer_id, EXTRACT(MONTH FROM order_date)
    ORDER BY customer_id, mes
    $$,
    $$ SELECT generate_series(1, 12) $$
) AS (
    customer_id TEXT,
    ene INT, feb INT, mar INT, abr INT, may INT, jun INT,
    jul INT, ago INT, sep INT, oct INT, nov INT, dic INT
)
ORDER BY customer_id
LIMIT 20;
\echo ===DELIM_END_165===
\echo ===DELIM_START_166===
WITH cohorte AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date))::date AS cohorte_mes
    FROM orders
    GROUP BY customer_id
),
actividad AS (
    SELECT DISTINCT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::date AS mes_activo
    FROM orders o
)
SELECT
    c.cohorte_mes,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 0) AS mes_0,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 1) AS mes_1,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 2) AS mes_2,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 3) AS mes_3,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 4) AS mes_4,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE calc.edad_cohorte = 5) AS mes_5
FROM cohorte c
INNER JOIN actividad a ON c.customer_id = a.customer_id
CROSS JOIN LATERAL (
    SELECT EXTRACT(YEAR FROM AGE(a.mes_activo, c.cohorte_mes)) * 12 +
           EXTRACT(MONTH FROM AGE(a.mes_activo, c.cohorte_mes)) AS edad_cohorte
) calc
GROUP BY c.cohorte_mes
ORDER BY c.cohorte_mes;
\echo ===DELIM_END_166===
\echo ===DELIM_START_167===
WITH cohorte_cliente AS (
    SELECT
        o.customer_id,
        c.country,
        DATE_TRUNC('month', MIN(o.order_date))::date AS cohorte_mes
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.country
),
actividad_mensual AS (
    SELECT DISTINCT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::date AS mes_activo
    FROM orders o
)
SELECT
    cc.country,
    cc.cohorte_mes,
    COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 0) AS mes0,
    COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 1) AS mes1,
    COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 2) AS mes2,
    COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 3) AS mes3,
    ROUND(
        COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 3)::numeric /
        NULLIF(COUNT(DISTINCT cc.customer_id) FILTER (WHERE edad_cohorte = 0), 0) * 100, 2
    ) AS retencion_mes3_pct
FROM cohorte_cliente cc
INNER JOIN actividad_mensual am ON cc.customer_id = am.customer_id
CROSS JOIN LATERAL (
    SELECT EXTRACT(YEAR FROM AGE(am.mes_activo, cc.cohorte_mes)) * 12 +
           EXTRACT(MONTH FROM AGE(am.mes_activo, cc.cohorte_mes)) AS edad_cohorte
) calc
GROUP BY cc.country, cc.cohorte_mes
ORDER BY cc.country, cc.cohorte_mes;
\echo ===DELIM_END_167===
\echo ===DELIM_START_168===
WITH p1 AS (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE order_date >= '1997-01-01' AND order_date < '1998-01-01'
),
p2 AS (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE order_date >= '1998-01-01' AND order_date < '1999-01-01'
),
segmentos AS (
    SELECT
        COALESCE(p1.customer_id, p2.customer_id) AS customer_id,
        CASE
            WHEN p1.customer_id IS NOT NULL AND p2.customer_id IS NOT NULL THEN 'RECURRENTE'
            WHEN p1.customer_id IS NOT NULL AND p2.customer_id IS NULL THEN 'PERDIDO'
            WHEN p1.customer_id IS NULL AND p2.customer_id IS NOT NULL THEN 'NUEVO'
        END AS segmento
    FROM p1
    FULL OUTER JOIN p2 ON p1.customer_id = p2.customer_id
)
SELECT
    segmento,
    COUNT(*) AS total_clientes,
    ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS porcentaje
FROM segmentos
GROUP BY segmento
ORDER BY
    CASE segmento
        WHEN 'RECURRENTE' THEN 1
        WHEN 'NUEVO' THEN 2
        WHEN 'PERDIDO' THEN 3
    END;
\echo ===DELIM_END_168===
\echo ===DELIM_START_169===
SELECT
    c.customer_id,
    c.company_name,
    c.country,
    pedidos_1997.total_1997,
    pedidos_1997.primer_pedido,
    pedidos_1997.ultimo_pedido
FROM customers c
CROSS JOIN LATERAL (
    SELECT
        COUNT(*) AS total_1997,
        MIN(order_date) AS primer_pedido,
        MAX(order_date) AS ultimo_pedido
    FROM orders o
    WHERE o.customer_id = c.customer_id
      AND o.order_date >= '1997-01-01'
      AND o.order_date < '1998-01-01'
) pedidos_1997
WHERE pedidos_1997.total_1997 > 0
  AND NOT EXISTS (
      SELECT 1
      FROM orders o
      WHERE o.customer_id = c.customer_id
        AND o.order_date >= '1998-01-01'
        AND o.order_date < '1999-01-01'
  )
ORDER BY pedidos_1997.total_1997 DESC;
\echo ===DELIM_END_169===
\echo ===DELIM_START_170===
SELECT
    c.category_name,
    segundo.product_name,
    segundo.unit_price,
    ROUND((segundo.unit_price / MAX(segundo.unit_price) OVER () * 100)::numeric, 2) AS pct_del_max_global
FROM categories c
CROSS JOIN LATERAL (
    SELECT product_name, unit_price
    FROM products
    WHERE category_id = c.category_id
    ORDER BY unit_price DESC
    LIMIT 1 OFFSET 1
) segundo
ORDER BY segundo.unit_price DESC;
\echo ===DELIM_END_170===
\echo ===DELIM_START_171===
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT
    c.company_name,
    p.product_name,
    SUM(od.quantity) AS total_unidades,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS total_ventas
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN products p ON od.product_id = p.product_id
WHERE c.country = 'Germany'
  AND o.order_date BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY c.company_name, p.product_name
ORDER BY total_ventas DESC
LIMIT 10;
\echo ===DELIM_END_171===
\echo ===DELIM_START_172===
-- ANTES: Sin índice
EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM customers
WHERE country = 'Germany';

-- Crear índice
CREATE INDEX idx_customers_country ON customers(country);

-- DESPUÉS: Con índice
EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM customers
WHERE country = 'Germany';

-- Limpieza (opcional)
DROP INDEX IF EXISTS idx_customers_country;
\echo ===DELIM_END_172===
\echo ===DELIM_START_173===
WITH metricas_tablas AS (
    SELECT
        schemaname,
        relname,
        n_live_tup,
        n_dead_tup,
        ROUND((n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100), 2) AS pct_dead,
        n_mod_since_analyze,
        last_analyze,
        last_autoanalyze,
        last_vacuum,
        last_autovacuum,
        pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS tamano
    FROM pg_stat_user_tables
    WHERE schemaname = 'public'
),
diagnostico_mantenimiento AS (
    SELECT
        *,
        CASE
            WHEN n_dead_tup > 0 AND n_live_tup = 0 THEN 'VACUUM (0 live)'
            WHEN pct_dead > 30 THEN 'VACUUM URGENTE'
            WHEN pct_dead > 10 THEN 'VACUUM recomendado'
            WHEN n_mod_since_analyze > n_live_tup * 0.2 THEN 'ANALYZE necesario'
            ELSE 'OK'
        END AS accion_recomendada
    FROM metricas_tablas
)
SELECT *
FROM diagnostico_mantenimiento
WHERE accion_recomendada != 'OK'
ORDER BY
    CASE
        WHEN accion_recomendada LIKE '%URGENTE%' THEN 1
        WHEN accion_recomendada LIKE '%VACUUM%' THEN 2
        WHEN accion_recomendada LIKE '%ANALYZE%' THEN 3
    END,
    pct_dead DESC;
\echo ===DELIM_END_173===
\echo ===DELIM_START_174===
WITH analisis_escaneos AS (
    SELECT
        schemaname,
        relname,
        seq_scan,
        seq_tup_read,
        COALESCE(idx_scan, 0) AS idx_scan_real,
        CASE
            WHEN seq_scan + COALESCE(idx_scan, 0) = 0 THEN 0
            ELSE ROUND(seq_scan::numeric / (seq_scan + COALESCE(idx_scan, 0)) * 100, 2)
        END AS pct_seq_scan,
        n_live_tup,
        pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS tamano
    FROM pg_stat_all_tables
    WHERE schemaname = 'public'
      AND seq_scan > 10
)
SELECT *,
    CASE
        WHEN pct_seq_scan > 90 AND n_live_tup > 1000 THEN 'REQUIERE INDICE'
        WHEN pct_seq_scan > 70 AND n_live_tup > 5000 THEN 'CONSIDERAR INDICE'
        WHEN idx_scan_real = 0 AND seq_scan > 50 THEN 'REVISAR PATRON DE CONSULTA'
        ELSE 'OK'
    END AS recomendacion
FROM analisis_escaneos
ORDER BY pct_seq_scan DESC, n_live_tup DESC
LIMIT 10;
\echo ===DELIM_END_174===
\echo ===DELIM_START_175===
-- Fuerza Hash Join (por defecto si work_mem suficiente)
SET enable_nestloop = OFF;
SET enable_mergejoin = OFF;

EXPLAIN (ANALYZE, BUFFERS)
SELECT o.order_id, SUM(od.quantity)
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
WHERE o.order_date >= '1998-01-01'
GROUP BY o.order_id;

-- Restaurar configuración
RESET enable_nestloop;
RESET enable_mergejoin;

-- Comparar con Nested Loop forzado
SET enable_hashjoin = OFF;
SET enable_mergejoin = OFF;

EXPLAIN (ANALYZE, BUFFERS)
SELECT o.order_id, SUM(od.quantity)
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
WHERE o.order_date >= '1998-01-01'
GROUP BY o.order_id;

RESET enable_hashjoin;
RESET enable_mergejoin;
\echo ===DELIM_END_175===
\echo ===DELIM_START_176===
DROP INDEX IF EXISTS idx_products_active;

CREATE INDEX idx_products_active ON products(product_name)
WHERE discontinued = 0;

EXPLAIN (ANALYZE, BUFFERS)
SELECT product_id, product_name, unit_price
FROM products
WHERE discontinued = 0
  AND product_name ILIKE '%chai%';

DROP INDEX IF EXISTS idx_products_active;
\echo ===DELIM_END_176===
\echo ===DELIM_START_177===
-- Crear índice compuesto
CREATE INDEX idx_products_cat_price ON products(category_id, unit_price DESC);

-- Consulta optimizada
EXPLAIN (ANALYZE, BUFFERS)
SELECT product_name, unit_price
FROM products
WHERE category_id = 1
ORDER BY unit_price DESC
LIMIT 5;

-- Mostrar Index Only Scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT category_id, unit_price
FROM products
WHERE category_id = 1
ORDER BY unit_price DESC;

DROP INDEX IF EXISTS idx_products_cat_price;
\echo ===DELIM_END_177===
\echo ===DELIM_START_178===
EXPLAIN (ANALYZE, BUFFERS)
WITH pedidos_1997 AS MATERIALIZED (
    SELECT customer_id, order_id, order_date, freight
    FROM orders
    WHERE order_date >= '1997-01-01' AND order_date < '1998-01-01'
)
SELECT c.company_name, COUNT(p.order_id) AS total_pedidos, SUM(p.freight) AS total_flete
FROM customers c
INNER JOIN pedidos_1997 p ON c.customer_id = p.customer_id
GROUP BY c.company_name
ORDER BY total_pedidos DESC
LIMIT 10;
\echo ===DELIM_END_178===
\echo ===DELIM_START_179===
WITH info_indices AS (
    SELECT
        c.relname AS tabla,
        i.indexrelid::regclass AS nombre_indice,
        pg_get_indexdef(i.indexrelid) AS definicion,
        COALESCE(s.idx_scan, 0) AS idx_scan,
        pg_size_pretty(pg_relation_size(i.indexrelid)) AS tamano
    FROM pg_index i
    INNER JOIN pg_class c ON i.indrelid = c.oid
    LEFT JOIN pg_stat_user_indexes s ON i.indexrelid = s.indexrelid
    WHERE c.relname IN ('customers', 'orders', 'products', 'order_details')
),
indices_agrupados AS (
    SELECT
        tabla,
        nombre_indice,
        definicion,
        idx_scan,
        tamano,
        ROW_NUMBER() OVER (PARTITION BY definicion ORDER BY idx_scan DESC) AS rn
    FROM info_indices
)
SELECT
    CASE
        WHEN rn > 1 THEN 'DUPLICADO'
        WHEN idx_scan = 0 THEN 'NO USADO'
        ELSE 'ACTIVO'
    END AS estado,
    tabla,
    nombre_indice,
    tamano,
    idx_scan,
    CASE
        WHEN rn > 1 THEN 'DROP INDEX IF EXISTS ' || nombre_indice || ';'
        WHEN idx_scan = 0 THEN 'CONSIDERAR DROP INDEX IF EXISTS ' || nombre_indice || ';'
        ELSE '-- Conservar'
    END AS accion_sugerida
FROM indices_agrupados
ORDER BY tabla, estado, idx_scan;
\echo ===DELIM_END_179===
\echo ===DELIM_START_180===
-- PASO 1: Capturar consulta original
EXPLAIN (ANALYZE, BUFFERS, SETTINGS)
SELECT
    c.country,
    c.city,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ventas
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
WHERE o.order_date >= '1997-01-01'
GROUP BY c.country, c.city
ORDER BY ventas DESC;

-- PASO 2: Verificar estadísticas
SELECT schemaname, relname, last_analyze, last_autoanalyze, n_mod_since_analyze
FROM pg_stat_user_tables
WHERE relname IN ('customers', 'orders', 'order_details');

-- PASO 3: Crear índices si es necesario
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX IF NOT EXISTS idx_order_details_order ON order_details(order_id);

-- PASO 4: Actualizar estadísticas
ANALYZE customers;
ANALYZE orders;
ANALYZE order_details;

-- PASO 5: Re-ejecutar con los mismos parámetros
EXPLAIN (ANALYZE, BUFFERS, SETTINGS)
SELECT
    c.country,
    c.city,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ventas
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
WHERE o.order_date >= '1997-01-01'
GROUP BY c.country, c.city
ORDER BY ventas DESC;

-- PASO 6: Comparar y documentar mejora
SELECT 'Antes: Seq Scan en orders, Sort externo, 3000 buffers'
UNION ALL
SELECT 'Después: Index Scan en orders, Hash Join, 150 buffers';
\echo ===DELIM_END_180===
\echo ===DELIM_START_181===
SELECT
    company_name,
    contact_name,
    contact_title,
    country
FROM customers
WHERE country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
ORDER BY country, company_name;
\echo ===DELIM_END_181===
\echo ===DELIM_START_182===
SELECT
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE unit_price > 20
  AND discontinued = 0
ORDER BY unit_price DESC;
\echo ===DELIM_END_182===
\echo ===DELIM_START_183===
SELECT
    order_id,
    ship_name,
    freight,
    ship_country
FROM orders
ORDER BY freight DESC NULLS LAST
LIMIT 10;
\echo ===DELIM_END_183===
\echo ===DELIM_START_184===
SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title,
    city,
    reports_to
FROM employees
WHERE reports_to IS NOT NULL
ORDER BY reports_to, last_name;
\echo ===DELIM_END_184===
\echo ===DELIM_START_185===
SELECT
    p.category_id,
    SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso_total
FROM order_details od
INNER JOIN products p ON od.product_id = p.product_id
GROUP BY p.category_id
HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 10000
ORDER BY ingreso_total DESC;
\echo ===DELIM_END_185===
\echo ===DELIM_START_186===
SELECT
    s.company_name AS transportista,
    COUNT(o.order_id) AS total_pedidos,
    ROUND(AVG(o.freight)::numeric, 2) AS flete_promedio
FROM orders o
INNER JOIN shippers s ON o.ship_via = s.shipper_id
GROUP BY s.company_name
HAVING AVG(o.freight) > 50
ORDER BY flete_promedio DESC;
\echo ===DELIM_END_186===
\echo ===DELIM_START_187===
SELECT
    c.category_name,
    COUNT(p.product_id) AS total_productos,
    COUNT(*) FILTER (WHERE p.units_in_stock < 20) AS stock_bajo,
    ROUND(AVG(p.unit_price)::numeric, 2) AS precio_promedio,
    MAX(p.unit_price) AS precio_maximo
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
HAVING COUNT(p.product_id) >= 3
ORDER BY total_productos DESC;
\echo ===DELIM_END_187===
\echo ===DELIM_START_188===
WITH ingresos_trimestre AS (
    SELECT
        EXTRACT(QUARTER FROM o.order_date) AS trimestre,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    WHERE EXTRACT(YEAR FROM o.order_date) = 1997
    GROUP BY EXTRACT(QUARTER FROM o.order_date)
)
SELECT
    'Q' || trimestre::text AS trimestre,
    ROUND(ingreso::numeric, 2) AS ingreso_total,
    ROUND((ingreso / SUM(ingreso) OVER () * 100)::numeric, 2) AS porcentaje
FROM ingresos_trimestre
ORDER BY trimestre;
\echo ===DELIM_END_188===
\echo ===DELIM_START_189===
SELECT
    o.order_id,
    o.order_date,
    c.company_name AS cliente,
    e.first_name || ' ' || e.last_name AS empleado,
    s.company_name AS transportista
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN employees e ON o.employee_id = e.employee_id
INNER JOIN shippers s ON o.ship_via = s.shipper_id
WHERE EXTRACT(YEAR FROM o.order_date) = 1997
ORDER BY o.order_date DESC
LIMIT 10;
\echo ===DELIM_END_189===
\echo ===DELIM_START_190===
SELECT
    c.customer_id,
    c.company_name,
    c.city,
    c.country
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
\echo ===DELIM_END_190===
\echo ===DELIM_START_191===
SELECT
    s.company_name AS proveedor,
    s.country,
    COUNT(p.product_id) AS productos_sin_ventas
FROM suppliers s
INNER JOIN products p ON s.supplier_id = p.supplier_id
LEFT JOIN order_details od ON p.product_id = od.product_id
WHERE od.product_id IS NULL
GROUP BY s.company_name, s.country
HAVING COUNT(p.product_id) >= 1
ORDER BY productos_sin_ventas DESC;
\echo ===DELIM_END_191===
\echo ===DELIM_START_192===
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo_empleado,
    COALESCE(m.first_name || ' ' || m.last_name, 'Sin jefe') AS jefe,
    COALESCE(m.title, 'N/A') AS cargo_jefe
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;
\echo ===DELIM_END_192===
\echo ===DELIM_START_193===
WITH metricas_cliente AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS total_pedidos,
        MIN(o.order_date) AS primer_pedido,
        MAX(o.order_date) AS ultimo_pedido
    FROM orders o
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT o.order_id) > 5
),
producto_mas_caro AS (
    SELECT DISTINCT ON (o.customer_id)
        o.customer_id,
        p.product_name,
        od.unit_price
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    INNER JOIN products p ON od.product_id = p.product_id
    ORDER BY o.customer_id, od.unit_price DESC
)
SELECT
    c.company_name,
    mc.total_pedidos,
    mc.primer_pedido,
    mc.ultimo_pedido,
    pcm.product_name AS producto_mas_caro,
    pcm.unit_price AS precio
FROM metricas_cliente mc
INNER JOIN customers c ON mc.customer_id = c.customer_id
LEFT JOIN producto_mas_caro pcm ON mc.customer_id = pcm.customer_id
ORDER BY mc.total_pedidos DESC
LIMIT 10;
\echo ===DELIM_END_193===
\echo ===DELIM_START_194===
SELECT
    p.product_name,
    p.unit_price,
    c.category_name,
    sub.precio_promedio_categoria
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
INNER JOIN (
    SELECT category_id, AVG(unit_price) AS precio_promedio_categoria
    FROM products
    GROUP BY category_id
) sub ON p.category_id = sub.category_id
WHERE p.unit_price > sub.precio_promedio_categoria
ORDER BY c.category_name, p.unit_price DESC
LIMIT 10;
\echo ===DELIM_END_194===
\echo ===DELIM_START_195===
SELECT
    o.customer_id,
    c.company_name,
    ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS total_beverages
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN products p ON od.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE cat.category_name = 'Beverages'
GROUP BY o.customer_id, c.company_name
ORDER BY total_beverages DESC
LIMIT 10;
\echo ===DELIM_END_195===
\echo ===DELIM_START_196===
SELECT
    p.product_name,
    p.unit_price,
    c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
WHERE p.unit_price > ALL (
    SELECT p2.unit_price
    FROM products p2
    INNER JOIN categories c2 ON p2.category_id = c2.category_id
    WHERE c2.category_name = 'Beverages'
)
ORDER BY p.unit_price DESC;
\echo ===DELIM_END_196===
\echo ===DELIM_START_197===
SELECT
    c.company_name,
    o.order_id,
    o.order_date,
    o.freight
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date = (
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
)
ORDER BY o.order_date DESC
LIMIT 10;
\echo ===DELIM_END_197===
\echo ===DELIM_START_198===
WITH ventas_producto AS (
    SELECT
        c.category_name,
        p.product_name,
        SUM(od.quantity) AS unidades_vendidas
    FROM order_details od
    INNER JOIN products p ON od.product_id = p.product_id
    INNER JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.category_name, p.product_name
)
SELECT
    category_name,
    product_name,
    unidades_vendidas,
    ROW_NUMBER() OVER (
        PARTITION BY category_name
        ORDER BY unidades_vendidas DESC
    ) AS ranking
FROM ventas_producto
ORDER BY category_name, ranking
LIMIT 15;
\echo ===DELIM_END_198===
\echo ===DELIM_START_199===
WITH ventas_mensuales AS (
    SELECT
        o.employee_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.employee_id, DATE_TRUNC('month', o.order_date)
),
con_lag AS (
    SELECT
        employee_id,
        mes,
        ventas,
        LAG(ventas) OVER (PARTITION BY employee_id ORDER BY mes) AS ventas_anterior
    FROM ventas_mensuales
)
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    cl.mes,
    ROUND(cl.ventas::numeric, 2) AS ventas_mes,
    ROUND(cl.ventas_anterior::numeric, 2) AS ventas_anterior,
    ROUND(((cl.ventas - cl.ventas_anterior) / NULLIF(cl.ventas_anterior, 0) * 100)::numeric, 2) AS variacion_pct
FROM con_lag cl
INNER JOIN employees e ON cl.employee_id = e.employee_id
WHERE cl.ventas_anterior IS NOT NULL
ORDER BY empleado, cl.mes
LIMIT 10;
\echo ===DELIM_END_199===
\echo ===DELIM_START_200===
WITH ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY DATE_TRUNC('month', o.order_date)
)
SELECT
    mes,
    ROUND(ventas::numeric, 2) AS ventas_totales,
    ROUND(AVG(ventas) OVER (
        ORDER BY mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS promedio_movil_3m,
    CASE
        WHEN ventas > AVG(ventas) OVER (
            ORDER BY mes
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) THEN 'Por encima'
        ELSE 'Por debajo'
    END AS tendencia
FROM ventas_mensuales
ORDER BY mes
LIMIT 12;
\echo ===DELIM_END_200===
\echo ===DELIM_START_201===
WITH ventas_cliente_mes AS (
    SELECT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::date AS mes,
        SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.customer_id, DATE_TRUNC('month', o.order_date)
)
SELECT
    c.company_name,
    vcm.mes,
    ROUND(vcm.ventas::numeric, 2) AS ventas_mes,
    ROUND(SUM(vcm.ventas) OVER (
        PARTITION BY vcm.customer_id
        ORDER BY vcm.mes
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ventas_acumuladas
FROM ventas_cliente_mes vcm
INNER JOIN customers c ON vcm.customer_id = c.customer_id
ORDER BY c.company_name, vcm.mes
LIMIT 12;
\echo ===DELIM_END_201===
\echo ===DELIM_START_202===
WITH metricas_generales AS (
    SELECT
        COUNT(DISTINCT o.customer_id) AS total_clientes,
        COUNT(DISTINCT o.order_id) AS total_pedidos,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS ingreso_total,
        ROUND((SUM(od.quantity * od.unit_price * (1 - od.discount)) / COUNT(DISTINCT o.order_id))::numeric, 2) AS ticket_promedio
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
),
top_cliente AS (
    SELECT
        o.customer_id,
        c.company_name,
        ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS facturacion
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    INNER JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.company_name
    ORDER BY facturacion DESC
    LIMIT 1
)
SELECT
    mg.total_clientes,
    mg.total_pedidos,
    mg.ingreso_total,
    mg.ticket_promedio,
    tc.company_name AS cliente_top,
    tc.facturacion AS facturacion_top
FROM metricas_generales mg, top_cliente tc;
\echo ===DELIM_END_202===
\echo ===DELIM_START_203===
WITH dias AS (
    SELECT
        generate_series(
            '1997-01-01'::date,
            '1997-01-31'::date,
            '1 day'::interval
        )::date AS fecha
)
SELECT
    fecha,
    TO_CHAR(fecha, 'Day') AS dia_semana,
    CASE
        WHEN EXTRACT(ISODOW FROM fecha) BETWEEN 1 AND 5 THEN 'Laboral'
        ELSE 'Fin de semana'
    END AS tipo_dia
FROM dias
ORDER BY fecha
LIMIT 12;
\echo ===DELIM_END_203===
\echo ===DELIM_START_204===
WITH precios_actuales AS (
    SELECT
        product_id,
        product_name,
        unit_price AS precio_actual
    FROM products
    WHERE discontinued = 0
),
precios_simulados AS (
    SELECT
        product_id,
        ROUND((precio_actual * 1.10)::numeric, 2) AS precio_simulado
    FROM precios_actuales
)
SELECT
    pa.product_name,
    pa.precio_actual,
    ps.precio_simulado,
    ROUND((ps.precio_simulado - pa.precio_actual)::numeric, 2) AS diferencia
FROM precios_actuales pa
INNER JOIN precios_simulados ps ON pa.product_id = ps.product_id
ORDER BY diferencia DESC
LIMIT 10;
\echo ===DELIM_END_204===
\echo ===DELIM_START_205===
SELECT c.company_name, COUNT(o.order_id) AS total_pedidos
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name
ORDER BY total_pedidos DESC;
\echo ===DELIM_END_205===
\echo ===DELIM_START_206===
SELECT product_name, unit_price
FROM products
WHERE LOWER(product_name) LIKE '%chocolate%';
\echo ===DELIM_END_206===
\echo ===DELIM_START_207===
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING GIN (product_name gin_trgm_ops);

SELECT product_name, unit_price
FROM products
WHERE product_name ILIKE '%chocolate%';
\echo ===DELIM_END_207===
\echo ===DELIM_START_208===
CREATE INDEX idx_products_lower_name ON products(LOWER(product_name));

SELECT product_name, unit_price
FROM products
WHERE LOWER(product_name) LIKE '%chocolate%';
\echo ===DELIM_END_208===
\echo ===DELIM_START_209===
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
\echo ===DELIM_END_209===
\echo ===DELIM_START_210===
-- 1. Crear la tabla de hechos
DROP TABLE IF EXISTS fact_ventas;
CREATE TABLE fact_ventas (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    customer_id VARCHAR(5),
    employee_id INT,
    order_date DATE,
    quantity INT,
    unit_price NUMERIC,
    discount NUMERIC,
    ingreso_neto NUMERIC GENERATED ALWAYS AS (
        ROUND((quantity * unit_price * (1 - discount))::numeric, 2)
    ) STORED,
    trimestre INT GENERATED ALWAYS AS (
        EXTRACT(QUARTER FROM order_date)::int
    ) STORED,
    anio INT GENERATED ALWAYS AS (
        EXTRACT(YEAR FROM order_date)::int
    ) STORED,
    PRIMARY KEY (order_id, product_id)
);

-- 2. Insertar datos
INSERT INTO fact_ventas (
    order_id, product_id, customer_id, employee_id,
    order_date, quantity, unit_price, discount
)
SELECT
    od.order_id,
    od.product_id,
    o.customer_id,
    o.employee_id,
    o.order_date,
    od.quantity,
    od.unit_price,
    od.discount
FROM order_details od
INNER JOIN orders o ON od.order_id = o.order_id;

-- 3. Verificar
SELECT
    anio,
    trimestre,
    COUNT(*) AS total_lineas,
    ROUND(SUM(ingreso_neto)::numeric, 2) AS ingreso_total
FROM fact_ventas
GROUP BY anio, trimestre
ORDER BY anio, trimestre;
\echo ===DELIM_END_210===
\echo ===DELIM_START_211===
EXPLAIN (ANALYZE, COSTS OFF)
SELECT c.company_name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name;
\echo ===DELIM_END_211===
\echo ===DELIM_START_212===
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
\echo ===DELIM_END_212===
\echo ===DELIM_START_213===
-- Consulta de verificación de stock
SELECT product_id, product_name, units_in_stock FROM products WHERE product_id = 1;
\echo ===DELIM_END_213===
\echo ===DELIM_START_214===
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
\echo ===DELIM_END_214===
\echo ===DELIM_START_215===
BEGIN;
-- Bloquea la fila para que otras transacciones esperen
SELECT units_in_stock FROM products WHERE product_id = 1 FOR UPDATE;

-- Ahora el UPDATE usa el valor más reciente garantizado (post-lock)
UPDATE products SET units_in_stock = units_in_stock - 1 WHERE product_id = 1;
COMMIT;
\echo ===DELIM_END_215===
\echo ===DELIM_START_216===
SELECT employee_id,
       last_name,
       first_name,
       title
FROM employees
ORDER BY employee_id;
\echo ===DELIM_END_216===
