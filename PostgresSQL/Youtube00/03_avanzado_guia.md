# Nivel 3 — Avanzado (Guía de estudio con ejercicios resueltos)

Objetivo: dominar CTEs recursivas, pivot, marcos de ventana avanzados, LATERAL, cohort analysis y EXPLAIN ANALYZE para optimización.

1) CTE recursiva — reconstruir organigrama (ejemplo resuelto)

```sql
WITH RECURSIVE organigrama AS (
  SELECT employee_id, first_name || ' ' || last_name AS nombre, reports_to, 0 AS nivel
  FROM employees
  WHERE reports_to IS NULL

  UNION ALL

  SELECT e.employee_id, e.first_name || ' ' || e.last_name, e.reports_to, o.nivel + 1
  FROM employees e
  JOIN organigrama o ON e.reports_to = o.employee_id
)
SELECT * FROM organigrama ORDER BY nivel, nombre;
```

2) Pivot (fila a columna) con CASE — ventas por año por cliente (ejemplo resuelto)

```sql
SELECT c.company_name,
  SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1996 THEN 1 ELSE 0 END) AS pedidos_1996,
  SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1997 THEN 1 ELSE 0 END) AS pedidos_1997,
  SUM(CASE WHEN EXTRACT(YEAR FROM o.order_date) = 1998 THEN 1 ELSE 0 END) AS pedidos_1998
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.company_name
ORDER BY c.company_name
LIMIT 50;
```

3) Ventanas y marcos — promedio móvil de 3 días (ejemplo resuelto)

```sql
WITH facturacion_diaria AS (
  SELECT o.order_date::date AS dia,
         SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total
  FROM orders o
  JOIN order_details od ON o.order_id = od.order_id
  GROUP BY o.order_date::date
)
SELECT dia, ROUND(total::numeric,2) AS venta_dia,
       ROUND(AVG(total) OVER (ORDER BY dia ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)::numeric,2) AS promedio_movil_3dias
FROM facturacion_diaria
ORDER BY dia DESC
LIMIT 30;
```

4) LATERAL — 3 productos más caros por categoría

```sql
SELECT c.category_name, p.product_name, p.unit_price
FROM categories c
CROSS JOIN LATERAL (
  SELECT product_name, unit_price
  FROM products p
  WHERE p.category_id = c.category_id
  ORDER BY unit_price DESC
  LIMIT 3
) p;
```

5) Cohort analysis — matriz mensual (ejemplo resuelto)

```sql
WITH first_order AS (
  SELECT customer_id, MIN(order_date)::date AS join_date
  FROM orders
  GROUP BY customer_id
),
months AS (
  SELECT customer_id, DATE_TRUNC('month', order_date)::date AS month
  FROM orders
  GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
cohort AS (
  SELECT f.join_date::date AS cohorte, m.month,
    EXTRACT(YEAR FROM AGE(m.month, f.join_date)) * 12 + EXTRACT(MONTH FROM AGE(m.month, f.join_date)) AS months_from_join
  FROM first_order f
  JOIN months m ON f.customer_id = m.customer_id
)
SELECT cohorte, months_from_join, COUNT(*) AS customers_active
FROM cohort
GROUP BY cohorte, months_from_join
ORDER BY cohorte, months_from_join;
```

6) PL/pgSQL: función simple que retorna ingresos por empleado (resuelto)

```sql
CREATE OR REPLACE FUNCTION ingresos_por_empleado(emp_id INT)
RETURNS NUMERIC LANGUAGE plpgsql AS $$
DECLARE
  total NUMERIC := 0;
BEGIN
  SELECT SUM(od.quantity * od.unit_price * (1 - od.discount)) INTO total
  FROM orders o
  JOIN order_details od ON o.order_id = od.order_id
  WHERE o.employee_id = emp_id;

  RETURN COALESCE(total, 0);
END; $$;

-- Uso:
SELECT employee_id, first_name || ' ' || last_name AS empleado, ingresos_por_empleado(employee_id) AS ingresos
FROM employees
ORDER BY ingresos DESC
LIMIT 5;
```

7) EXPLAIN ANALYZE — medicina del rendimiento

- Siempre interpretar `Seq Scan`, `Index Scan`, `Buffers` y `Actual time`.
- Para pruebas en tablas grandes, crear índices temporales y comparar `EXPLAIN (ANALYZE, BUFFERS)` antes/después.
- Si ejecutas `EXPLAIN ANALYZE` sobre DML destructivo, envolver en `BEGIN; ...; ROLLBACK;`.

8) Extensiones útiles

- `CREATE EXTENSION IF NOT EXISTS tablefunc;` — para `crosstab()` (pivot físico)
- `CREATE EXTENSION IF NOT EXISTS pg_trgm;` — para búsquedas difusas con `ILIKE`/`~`

---

Sugerencia final: cada ejercicio resuelto incluye siempre una variante para que el estudiante pruebe (por ejemplo, cambiar filtros por país, rango de fechas o top-N). Añadir `EXPLAIN (ANALYZE, BUFFERS)` tras cada consulta clave ayuda a entender impacto I/O.
