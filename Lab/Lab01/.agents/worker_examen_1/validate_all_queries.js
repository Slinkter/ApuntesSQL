const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const mdPath = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';
const content = fs.readFileSync(mdPath, 'utf8');

const questions = [
  {
    num: 1,
    name: 'Filtro clientes Europa',
    sql: `SELECT
    company_name,
    contact_name,
    contact_title,
    country
FROM customers
WHERE country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
ORDER BY country, company_name;`
  },
  {
    num: 2,
    name: 'Productos activos > $20',
    sql: `SELECT
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE unit_price > 20
  AND discontinued = 0
ORDER BY unit_price DESC;`
  },
  {
    num: 3,
    name: 'Top 10 fletes',
    sql: `SELECT
    order_id,
    ship_name,
    freight,
    ship_country
FROM orders
ORDER BY freight DESC NULLS LAST
LIMIT 10;`
  },
  {
    num: 4,
    name: 'Empleados con jefe',
    sql: `SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title,
    city,
    reports_to
FROM employees
WHERE reports_to IS NOT NULL
ORDER BY reports_to, last_name;`
  },
  {
    num: 5,
    name: 'Ingreso por categoría > 10000',
    sql: `SELECT
    p.category_id,
    SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso_total
FROM order_details od
INNER JOIN products p ON od.product_id = p.product_id
GROUP BY p.category_id
HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 10000
ORDER BY ingreso_total DESC;`
  },
  {
    num: 6,
    name: 'Transportistas flete promedio > 50',
    sql: `SELECT
    s.company_name AS transportista,
    COUNT(o.order_id) AS total_pedidos,
    ROUND(AVG(o.freight)::numeric, 2) AS flete_promedio
FROM orders o
INNER JOIN shippers s ON o.ship_via = s.shipper_id
GROUP BY s.company_name
HAVING AVG(o.freight) > 50
ORDER BY flete_promedio DESC;`
  },
  {
    num: 7,
    name: 'Productos por categoría con FILTER',
    sql: `SELECT
    c.category_name,
    COUNT(p.product_id) AS total_productos,
    COUNT(*) FILTER (WHERE p.units_in_stock < 20) AS stock_bajo,
    ROUND(AVG(p.unit_price)::numeric, 2) AS precio_promedio,
    MAX(p.unit_price) AS precio_maximo
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
HAVING COUNT(p.product_id) >= 3
ORDER BY total_productos DESC;`
  },
  {
    num: 8,
    name: 'Ingreso trimestral 1997',
    sql: `WITH ingresos_trimestre AS (
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
ORDER BY trimestre;`
  },
  {
    num: 9,
    name: 'Detalle órdenes 1997',
    sql: `SELECT
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
LIMIT 10;`
  },
  {
    num: 10,
    name: 'Clientes sin órdenes (Anti-Join)',
    sql: `SELECT
    c.customer_id,
    c.company_name,
    c.city,
    c.country
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;`
  },
  {
    num: 11,
    name: 'Proveedores sin ventas',
    sql: `SELECT
    s.company_name AS proveedor,
    s.country,
    COUNT(p.product_id) AS productos_sin_ventas
FROM suppliers s
INNER JOIN products p ON s.supplier_id = p.supplier_id
LEFT JOIN order_details od ON p.product_id = od.product_id
WHERE od.product_id IS NULL
GROUP BY s.company_name, s.country
HAVING COUNT(p.product_id) >= 1
ORDER BY productos_sin_ventas DESC;`
  },
  {
    num: 12,
    name: 'Jerarquía empleados',
    sql: `SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo_empleado,
    COALESCE(m.first_name || ' ' || m.last_name, 'Sin jefe') AS jefe,
    COALESCE(m.title, 'N/A') AS cargo_jefe
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;`
  },
  {
    num: 13,
    name: 'Métricas cliente + producto más caro',
    sql: `WITH metricas_cliente AS (
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
LIMIT 10;`
  },
  {
    num: 14,
    name: 'Productos precio > promedio categoría',
    sql: `SELECT
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
LIMIT 10;`
  },
  {
    num: 15,
    name: 'Gasto clientes Beverages',
    sql: `SELECT
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
LIMIT 10;`
  },
  {
    num: 16,
    name: 'Productos > ALL Beverages',
    sql: `SELECT
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
ORDER BY p.unit_price DESC;`
  },
  {
    num: 17,
    name: 'Último pedido cliente',
    sql: `SELECT
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
LIMIT 10;`
  },
  {
    num: 18,
    name: 'Ranking productos por categoría',
    sql: `WITH ventas_producto AS (
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
LIMIT 15;`
  },
  {
    num: 19,
    name: 'Ventas mensuales empleado con LAG',
    sql: `WITH ventas_mensuales AS (
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
LIMIT 10;`
  },
  {
    num: 20,
    name: 'Promedio móvil 3 meses',
    sql: `WITH ventas_mensuales AS (
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
LIMIT 12;`
  },
  {
    num: 21,
    name: 'Ventas acumuladas por cliente',
    sql: `WITH ventas_cliente_mes AS (
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
LIMIT 12;`
  },
  {
    num: 22,
    name: 'Metricas generales de negocio',
    sql: `WITH metricas_generales AS (
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
FROM metricas_generales mg CROSS JOIN top_cliente tc;`
  },
  {
    num: 23,
    name: 'generate_series calendario',
    sql: `WITH dias AS (
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
LIMIT 12;`
  },
  {
    num: 24,
    name: 'Simulacion de precios',
    sql: `WITH precios_actuales AS (
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
LIMIT 10;`
  },
  {
    num: 25,
    name: 'Optimización clientes Germany',
    sql: `SELECT c.company_name, COUNT(o.order_id) AS total_pedidos
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name
ORDER BY total_pedidos DESC;`
  },
  {
    num: 26,
    name: 'LIKE chocolate',
    sql: `SELECT product_name, unit_price
FROM products
WHERE LOWER(product_name) LIKE '%chocolate%';`
  },
  {
    num: 27,
    name: 'Dashboard KPIs trimestre',
    sql: `WITH pedidos_trimestre AS (
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
    (SELECT ship_country FROM pais_top) AS pais_top;`
  },
  {
    num: 28,
    name: 'fact_ventas DDL y reporte',
    sql: `DROP TABLE IF EXISTS fact_ventas;
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

SELECT
    anio,
    trimestre,
    COUNT(*) AS total_lineas,
    ROUND(SUM(ingreso_neto)::numeric, 2) AS ingreso_total
FROM fact_ventas
GROUP BY anio, trimestre
ORDER BY anio, trimestre;`
  },
  {
    num: 29,
    name: 'EXPLAIN ANALYZE',
    sql: `EXPLAIN (ANALYZE, COSTS OFF)
SELECT c.company_name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name;`
  },
  {
    num: 30,
    name: 'Control concurrencia producto 1',
    sql: `SELECT product_id, product_name, units_in_stock FROM products WHERE product_id = 1;`
  }
];

const results = [];

for (const q of questions) {
  const tmpFile = path.join(__dirname, `q${q.num}.sql`);
  fs.writeFileSync(tmpFile, q.sql, 'utf8');
  try {
    execSync(`docker cp "${tmpFile}" pg_architect_lab:/tmp/q.sql`);
    const output = execSync(`docker exec pg_architect_lab psql -U slinkter -d northwind -f /tmp/q.sql`, { encoding: 'utf8' });
    results.push({ num: q.num, name: q.name, success: true, output });
  } catch (err) {
    results.push({ num: q.num, name: q.name, success: false, error: err.stderr ? err.stderr.toString() : err.message });
  }
}

fs.writeFileSync(path.join(__dirname, 'execution_results.json'), JSON.stringify(results, null, 2), 'utf8');
console.log('All 30 queries executed. Results saved.');
