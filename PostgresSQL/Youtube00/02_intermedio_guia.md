# Nivel 2 — Intermedio (Guía de estudio con ejercicios resueltos)

Objetivo: trabajar con agregaciones, HAVING, subconsultas, CTEs y funciones de ventana básicas.

Ejecutar un ejercicio único (psql):

```bash
psql -h localhost -U slinkter -d northwind -c "<TU_QUERY>"
```

Ejercicios resueltos

1) Clientes por país (conteo) y filtrar países con > 5 clientes.

Solución:

```sql
SELECT country, COUNT(*) AS clientes
FROM customers
GROUP BY country
HAVING COUNT(*) > 5
ORDER BY clientes DESC;
```

2) Promedio de unidades por pedido (order_details) por producto, mostrar top 10.

Solución:

```sql
SELECT p.product_id, p.product_name, ROUND(AVG(od.quantity)::numeric,2) AS avg_qty
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY avg_qty DESC
LIMIT 10;
```

3) Usar una CTE para calcular facturación por pedido y mostrar pedidos con facturación > 1000.

Solución:

```sql
WITH facturacion AS (
  SELECT o.order_id, SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total
  FROM orders o
  JOIN order_details od ON o.order_id = od.order_id
  GROUP BY o.order_id
)
SELECT order_id, ROUND(total::numeric,2) AS total
FROM facturacion
WHERE total > 1000
ORDER BY total DESC;
```

4) Encontrar los 3 clientes con mayor número de pedidos únicos usando ROW_NUMBER() (ventana).

Solución:

```sql
WITH pedidos_por_cliente AS (
  SELECT c.customer_id, c.company_name, COUNT(o.order_id) AS pedidos
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.company_name
)
SELECT customer_id, company_name, pedidos
FROM (
  SELECT *, ROW_NUMBER() OVER (ORDER BY pedidos DESC) AS rn
  FROM pedidos_por_cliente
) t
WHERE rn <= 3;
```

5) Subconsulta correlacionada: obtener la última fecha de pedido por cliente.

Solución:

```sql
SELECT c.customer_id, c.company_name,
  (SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.customer_id) AS ultima_compra
FROM customers c
ORDER BY ultima_compra DESC
LIMIT 10;
```

6) EXPLAIN ANALYZE: comparar una versión con índice y sin índice. Crear índice de ejemplo y medir:

```sql
-- crear índice para la prueba
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);

EXPLAIN (ANALYZE, BUFFERS)
SELECT o.order_id FROM orders o WHERE o.customer_id = 'ALFKI';
```

Consejo: cuando uses ventanas en tablas grandes, aumentar `work_mem` temporalmente para evitar spills a disco.
