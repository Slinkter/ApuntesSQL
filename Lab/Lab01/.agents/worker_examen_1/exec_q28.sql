-- 1. Creación de la Tabla de Hechos con Columnas Calculadas STORED
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

-- 2. Carga Inicial ETL (Insert ... Select)
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

-- 3. Verificación Analítica OLAP
SELECT
    anio,
    trimestre,
    COUNT(*) AS total_lineas,
    ROUND(SUM(ingreso_neto)::numeric, 2) AS ingreso_total
FROM fact_ventas
GROUP BY anio, trimestre
ORDER BY anio, trimestre;