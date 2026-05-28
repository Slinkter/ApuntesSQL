# Nivel 1 — Básico (Guía de estudio con ejercicios resueltos)

Objetivo: afianzar SELECT, filtros, JOINs simples y uso de psql/docker para ejecutar consultas.

Requisitos rápidos
- Postgres 15+ o Docker
- Dataset: PostgresSQL/Youtube00/db_northwind.sql

Arranque rápido (Docker):

```bash
docker run --rm --name pg_lab -e POSTGRES_USER=slinkter -e POSTGRES_PASSWORD=slinkter -e POSTGRES_DB=northwind -p 5432:5432 -v "$(pwd)/PostgresSQL/Youtube00/db_northwind.sql":/docker-entrypoint-initdb.d/db_northwind.sql -d postgres:16-alpine
```

Ejecutar un ejercicio único (psql):

```bash
psql -h localhost -U slinkter -d northwind -c "SELECT * FROM customers LIMIT 5;"
```

Ejercicios resueltos

1) Listar 5 clientes de Alemania (country = 'Germany').

Solución:

```sql
SELECT customer_id, company_name, city, country
FROM customers
WHERE country = 'Germany'
ORDER BY company_name
LIMIT 5;
```

2) Contar cuántos pedidos (orders) hizo cada cliente, mostrar los 10 con más pedidos.

Solución:

```sql
SELECT c.customer_id, c.company_name, COUNT(o.order_id) AS total_pedidos
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_pedidos DESC
LIMIT 10;
```

3) Mostrar detalles de los pedidos (orders) con su cliente (JOIN simple) para un pedido específico (order_id = 10248).

Solución:

```sql
SELECT o.order_id, o.order_date, c.company_name, od.product_id, od.quantity, od.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_details od ON o.order_id = od.order_id
WHERE o.order_id = 10248;
```

4) Buscar productos cuyo nombre contenga 'Chai' (uso de ILIKE para búsqueda case-insensitive).

Solución:

```sql
SELECT product_id, product_name, unit_price
FROM products
WHERE product_name ILIKE '%chai%';
```

5) Ejecutar EXPLAIN ANALYZE sobre una consulta de ejemplo (sin modificar datos):

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.customer_id, COUNT(o.order_id) FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY 2 DESC
LIMIT 5;
```

Nota: usar `EXPLAIN ANALYZE` en consultas SELECT está bien; para DML destructivo envolver en transacción y hacer ROLLBACK.

Siguientes pasos: practicar variando WHERE, añadir índices si EXPLAIN indica Seq Scan en tablas grandes.
