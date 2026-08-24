# -*- coding: utf-8 -*-
"""
Sections 7, 8, 9 (Questions 25 to 30 + Summary Table) for 4.examen_entrevista.md
"""

sec7_9_text = """## Sección 7: Arquitectura de Índices y Optimización de Consultas (2 preguntas)

### Pregunta 25 - Nivel: Senior / Lead

**Contexto de Negocio:** El equipo de analistas de BI ejecuta continuamente el siguiente reporte regional para la gerencia de ventas de Alemania. En la base de datos de producción (con millones de clientes y pedidos), la consulta presenta una degradación severa de tiempos de respuesta por escaneos secuenciales masivos.

**Consulta a Optimizar:**
```sql
SELECT c.company_name, COUNT(o.order_id) AS total_pedidos
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name
ORDER BY total_pedidos DESC;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
       company_name       | total_pedidos 
--------------------------+---------------
 QUICK-Stop               |            28
 Lehmanns Marktstand      |            15
 Frankenversand           |            15
 Königlich Essen          |            14
 Ottilies Käseladen       |            10
 Die Wandernde Kuh        |            10
 Blauer See Delikatessen  |             7
 Toms Spezialitäten       |             6
 Drachenblut Delikatessen |             6
 Alfreds Futterkiste      |             6
 Morgenstern Gesundkost   |             5
(11 rows)
```

**Enunciado:** Analizar exhaustivamente el ciclo de ejecución de la consulta, identificar los cuellos de botella de acceso a datos y proponer una estrategia integral de indexación en 3 niveles (Filtro, Join y Covering Index), justificando el impacto en el planificador de PostgreSQL.

<details>
<summary>Respuesta y Análisis de Arquitectura de Base de Datos</summary>

#### 🔄 Pipeline Lógico del Motor & Diagnóstico de Cuellos de Botella:

```text
========================================================================================
[DIAGNÓSTICO SIN ÍNDICES]
1. [1. FROM / WHERE] -> Seq Scan sobre 'customers': Lee todas las páginas Heap para encontrar
                         los 11 clientes de Germany (Rows Removed by Filter: 80).
2. [2. ON / JOIN]    -> Seq Scan sobre 'orders': Sin índice en la Foreign Key 'customer_id',
                         el motor debe escanear todas las órdenes de la empresa.
3. [5. GROUP BY]     -> HashAggregate en memoria agrupando por company_name.
========================================================================================
```

#### 🛠️ Estrategia de Indexación Recomendada:

**Nivel 1: Índice de Filtro B-Tree (Index Scan)**
```sql
CREATE INDEX idx_customers_country ON customers(country);
```
- **Impacto:** Transforma el `Seq Scan` en `customers` en un `Bitmap Index Scan` o `Index Scan`, localizando instantáneamente los 11 punteros de tuplas de Alemania en el árbol B-Tree sin escanear el resto de la tabla.

**Nivel 2: Índice de Cruce en Foreign Key (Join Optimization)**
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```
- **Impacto:** Permite que el optimizador utilice un `Nested Loop Left Join` con `Bitmap Index Scan` sobre `orders`, recuperando exclusivamente los pedidos asociados a los 11 clientes filtrados en lugar de escanear la tabla transaccional completa.

**Nivel 3: Índice Cubriente con Cláusula INCLUDE (Index-Only Scan de Élite)**
```sql
CREATE INDEX idx_customers_country_covering 
ON customers(country) 
INCLUDE (customer_id, company_name);
```
- **Impacto Arquitectónico:**
  - Las columnas de la clave (`country`) se almacenan en las páginas raíz e intermedias del B-Tree para la búsqueda binaria rápida.
  - Las columnas del `INCLUDE` (`customer_id`, `company_name`) se almacenan **únicamente en las páginas hoja del índice**, sin sobrecargar el árbol de navegación.
  - **Resultado:** **Index-Only Scan**. PostgreSQL resuelve la consulta de clientes íntegramente desde la memoria del índice sin realizar un solo acceso a disco hacia las páginas Heap de la tabla.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Sugiere índices genéricos sin diferenciar columnas de filtro vs join.
- **Mid:** Propone crear índices en `country` y en la FK `orders(customer_id)`.
- **Senior / Lead:** Diseña el **Covering Index** con `INCLUDE`, explica la estructura interna de páginas del B-Tree y detalla cómo el Visibility Map de PostgreSQL permite los *Index-Only Scans*.

</details>

---

### Pregunta 26 - Nivel: Senior / Lead

**Contexto de Negocio:** El motor de búsqueda del portal de comercio electrónico permite a los clientes buscar productos mediante términos libres. La siguiente consulta de búsqueda de texto se ejecuta con alta concurrencia pero genera alertas de CPU al 100%:

```sql
SELECT product_name, unit_price
FROM products
WHERE LOWER(product_name) LIKE '%chocolate%';
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
        product_name        | unit_price 
----------------------------+------------
 Teatime Chocolate Biscuits | 9.19999981
(1 row)
```

**Enunciado:** Diagnosticar la causa raíz por la cual un índice B-Tree estándar en `product_name` resulta completamente inútil para esta consulta, y proponer la solución definitiva de grado de producción en PostgreSQL 16.

<details>
<summary>Respuesta y Análisis de Arquitectura de Base de Datos</summary>

#### 🔍 Diagnóstico Forense de la Falla del Índice B-Tree:

1. **El Problema del Comodín Inicial (`%...`):**
   Los índices B-Tree estándar están estructurados para búsquedas por prefijo ordenado de izquierda a derecha (como un diccionario telefónico). Un patrón con comodín a la izquierda (`'%chocolate%'` o `'%chocolate'`) no tiene un prefijo anclado, obligando al motor a realizar un escaneo secuencial exhaustivo (**Sequential Scan**) sobre el 100% de la tabla.
2. **Incompatibilidad Funcional (`LOWER()`):**
   Cualquier función escalar aplicada sobre la columna en la cláusula `WHERE` invalida el uso de un índice simple en `product_name`, a menos que se cree un índice funcional dedicado.

#### 🚀 Solución de Producción: Extensión `pg_trgm` + Índice GIN de Trigramas

```sql
-- 1. Habilitar la extensión de trigramas
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 2. Crear índice GIN especializado en trigramas
CREATE INDEX idx_products_name_trgm_gin 
ON products USING GIN (product_name gin_trgm_ops);

-- 3. Consulta optimizada (PostgreSQL usará Bitmap Index Scan automáticamente)
SELECT product_name, unit_price
FROM products
WHERE product_name ILIKE '%chocolate%';
```

#### 🔄 Diagrama de Flujo y Mecánica de Trigramas:

```text
========================================================================================
[ANATOMÍA DE TRIGRAMAS EN GIN]
Texto indexado: "Teatime Chocolate Biscuits"
Trigramas generados (subcadenas de 3 caracteres contiguos):
{"  c", " ch", "cho", "hoc", "oco", "col", "ola", "lat", "ate", "te ", ...}

Término buscado: "chocolate"
Trigramas requeridos: {"  c", " ch", "cho", "hoc", "oco", "col", "ola", "lat", "ate", "te "}

El índice GIN (Generalized Inverted Index) intersecta en memoria las listas de posting
de cada trigrama en O(1), recuperando exactamente el puntero de la tupla sin escanear el Heap.
========================================================================================
```

**Comparativa Técnica:**
- **Índice Funcional B-Tree (`CREATE INDEX ON products(LOWER(product_name))`):** Solo acelera búsquedas con prefijo fijo: `LIKE 'chocolate%'`, pero sigue siendo inútil para `%chocolate%`.
- **Índice GIN con Trigramas:** Acelera búsquedas con comodines en cualquier posición (`%texto%`), búsquedas insensibles a mayúsculas (`ILIKE`) y operadores de similitud difusa (*Fuzzy Matching* con `%`).

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Sugiere agregar más condiciones en el `WHERE` sin entender la causa de la falla del B-Tree.
- **Mid:** Sugiere un índice funcional `LOWER(product_name)` sin notar que el comodín `%` inicial invalida el B-Tree.
- **Senior / Lead:** Diagnostica la falla del árbol B-Tree, implementa `pg_trgm` con índice `GIN`, detalla la descomposición en trigramas y compara los costos de inserción vs velocidad de lectura.

</details>

---

## Sección 8: Modelado Dimensional y Casos Prácticos de Negocio (2 preguntas)

### Pregunta 27 - Nivel: Senior / Lead

**Contexto de Negocio:** La Mesa Directiva requiere un panel ejecutivo consolidado que capture la fotografía operacional completa del **último trimestre móvil con datos** registrados en el sistema. La consulta debe calcular en una sola fila atómica métricas financieras, transaccionales, de clientes y los líderes en productos y países.

**Enunciado:** Construir una consulta analítica que retorne **en una sola fila**:
1. `total_pedidos`: Total de órdenes emitidas en los últimos 3 meses respecto a la fecha máxima de la base de datos (`MAX(order_date) - INTERVAL '3 months'`).
2. `total_clientes`: Cantidad de clientes únicos que compraron en dicho periodo.
3. `ingreso_total`: Facturación neta del trimestre redondeada a 2 decimales.
4. `ticket_promedio`: Facturación neta promedio por pedido en dicho periodo.
5. `producto_top`: Nombre del producto con mayor volumen de unidades vendidas en el trimestre.
6. `pais_top`: Nombre del país con mayor cantidad de órdenes enviadas (`ship_country`).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Dashboard ejecutivo multi-grano en un solo registro atómico.
2. **Ventana Temporal Dinámica:** `order_date >= (SELECT MAX(order_date) - INTERVAL '3 months' FROM orders)`.
3. **Modularización:** CTEs separados para la ventana temporal, detalle de ventas, producto top y país top.
4. **Consolidación:** Subconsultas escalares en el `SELECT` principal.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 total_pedidos | total_clientes | ingreso_total | ticket_promedio | producto_top | pais_top 
---------------+----------------+---------------+-----------------+--------------+----------
           205 |             73 |     320348.22 |         1562.67 | Konbu        | USA
(1 row)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. SEGMENTACIÓN TEMPORAL DINÁMICA] -> Determina fecha máxima: 1998-05-06.
                                       Filtra rango: 1998-02-06 a 1998-05-06 (205 pedidos).
[2. EVALUACIÓN PARALELA DE CTEs]   -> Agrega ventas, halla producto top (Konbu) y país top (USA).
[3. ENSAMBLADO ESCALAR]            -> Proyecta los 6 KPIs consolidados en un registro único.
========================================================================================
```

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Hardcodea fechas estáticas (ej. `'1998-01-01'`) que rompen si ingresan nuevos datos.
- **Mid:** Usa CTEs pero lucha para unificar granularidades distintas en una sola fila.
- **Senior / Lead:** Construye la ventana temporal dinámica con `INTERVAL`, desacopla métricas en CTEs modulares y asegura cero multiplicaciones cartesianas.

</details>

---

### Pregunta 28 - Nivel: Lead / Data Architect

**Contexto de Negocio:** El equipo de Data Engineering está migrando la base transaccional Northwind hacia un esquema dimensional optimizado para Business Intelligence (*Data Mart de Ventas*). Se requiere diseñar e instanciar la tabla de hechos `fact_ventas` utilizando columnas generadas físicamente almacenadas (`GENERATED ALWAYS AS ... STORED`), poblarla con un proceso ETL vía `INSERT INTO ... SELECT`, y validar la consistencia del modelo ejecutando una consulta analítica de facturación por año y trimestre.

**Enunciado:**
1. Crear la tabla de hechos `fact_ventas` con clave primaria compuesta `(order_id, product_id)` y columnas generadas `STORED`:
   - `ingreso_neto`: `ROUND((quantity * unit_price * (1 - discount))::numeric, 2)`.
   - `trimestre`: `EXTRACT(QUARTER FROM order_date)::int`.
   - `anio`: `EXTRACT(YEAR FROM order_date)::int`.
2. Poblar la tabla de hechos desde `order_details` y `orders`.
3. Consultar la tabla generada agrupando por `anio` y `trimestre`, mostrando el conteo de líneas de venta (`total_lineas`) y la facturación total acumulada (`ingreso_total`), ordenada cronológicamente.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
DROP TABLE
CREATE TABLE
INSERT 0 2155
 anio | trimestre | total_lineas | ingreso_total 
------+-----------+--------------+---------------
 1996 |         3 |          185 |      79728.56
 1996 |         4 |          220 |     128355.39
 1997 |         1 |          241 |     138288.90
 1997 |         2 |          253 |     143177.03
 1997 |         3 |          256 |     153937.74
 1997 |         4 |          309 |     181681.44
 1998 |         1 |          452 |     298491.56
 1998 |         2 |          239 |     142132.33
(8 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. DDL & GENERATED STORED] -> El motor crea la estructura física. Las columnas STORED
                               se calculan y serializan en disco durante cada operación INSERT/UPDATE.
[2. CARGA ETL]              -> Inserta exactamente 2,155 tuplas desde el modelo relacional.
[3. CONSULTA ANALÍTICA]     -> Agrupa instantáneamente por anio y trimestre precalculados,
                               eliminando el costo de CPU de evaluar expresiones temporales en tiempo de consulta.
========================================================================================
```

**Análisis de Modelado Dimensional (Kimball):**
- **Grano de la Tabla de Hechos:** Una fila por ítem de producto dentro de una orden transaccional (`Transaction Fact Table`).
- **Clave Primaria:** `(order_id, product_id)` garantiza unicidad e idempotencia en cargas incrementales de datos.
- **Columnas Generadas STORED vs Vistas:** Las columnas `STORED` consumen espacio en disco pero aceleran drásticamente los dashboards al evitar cálculos repetitivos en tiempo real.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Define columnas simples y recalcula expresiones en cada consulta.
- **Mid:** Diseña la tabla con PK compuesta y carga con `INSERT INTO ... SELECT`.
- **Senior / Lead:** Implementa `GENERATED ALWAYS AS ... STORED`, justifica el grano dimensional según la metodología Kimball y detalla la estrategia de indexación B-Tree sobre las claves foráneas dimensionales.

</details>

---

## Sección 9: Rendimiento del Motor, Diagnóstico de Planes y Concurrencia (2 preguntas)

### Pregunta 29 - Nivel: Lead / Principal DBA

**Contexto de Negocio:** Un Data Engineer Junior solicita tu asistencia como Database Architect para diagnosticar el siguiente plan de ejecución obtenido en el ambiente de producción tras ejecutar `EXPLAIN (ANALYZE, COSTS OFF)` sobre la consulta de clientes alemanes:

```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT c.company_name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.company_name;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
QUERY PLAN                                                    
-----------------------------------------------------------------------------------------------------------------
 GroupAggregate (actual time=0.213..0.226 rows=11 loops=1)
   Group Key: c.company_name
   ->  Sort (actual time=0.209..0.213 rows=122 loops=1)
         Sort Key: c.company_name
         Sort Method: quicksort  Memory: 30kB
         ->  Nested Loop Left Join (actual time=0.022..0.162 rows=122 loops=1)
               ->  Seq Scan on customers c (actual time=0.005..0.013 rows=11 loops=1)
                     Filter: ((country)::text = 'Germany'::text)
                     Rows Removed by Filter: 80
               ->  Bitmap Heap Scan on orders o (actual time=0.007..0.010 rows=11 loops=11)
                     Recheck Cond: ((c.customer_id)::text = (customer_id)::text)
                     Heap Blocks: exact=78
                     ->  Bitmap Index Scan on idx_orders_customer_id (actual time=0.005..0.005 rows=11 loops=11)
                           Index Cond: ((customer_id)::text = (c.customer_id)::text)
 Planning Time: 0.808 ms
 Execution Time: 0.282 ms
(16 rows)
```

**Enunciado:** Interpretar técnicamente cada nodo del plan de ejecución generado por PostgreSQL 16:
1. Explicar la mecánica del cruce `Nested Loop Left Join` y el rol del índice `idx_orders_customer_id`.
2. Explicar por qué el motor utiliza `Bitmap Index Scan` + `Bitmap Heap Scan` en lugar de un `Index Scan` directo.
3. Explicar el significado de `actual time`, `rows`, `loops`, `quicksort Memory: 30kB` y por qué el planificador eligió `GroupAggregate` tras el nodo `Sort`.

<details>
<summary>Respuesta y Análisis de Ingeniería del Motor PostgreSQL</summary>

#### 🔬 Desglose Forense del Plan de Ejecución:

1. **Acceso a la Tabla Externa (`customers c`):**
   - `Seq Scan on customers c`: Escanea las páginas Heap de `customers`. Dado que la tabla solo tiene 91 registros que residen en una sola página de memoria buffer, un escaneo secuencial es más económico para el planificador que descender por un árbol B-Tree.
   - `Filter: (country = 'Germany')`: Evalúa el predicado, reteniendo 11 filas y descartando 80 (`Rows Removed by Filter: 80`).

2. **Cruce Anidado Indexado (`Nested Loop Left Join`):**
   - El motor ejecuta un bucle anidado que itera sobre los 11 clientes alemanes (`loops=11`).
   - Por cada cliente alemán, ejecuta un `Bitmap Index Scan on idx_orders_customer_id` para localizar las posiciones físicas de sus órdenes en memoria en tiempo logarítmico.
   - `Bitmap Heap Scan`: Convierte la lista de punteros en un mapa de bits ordenado por número de bloque de disco, leyendo secuencialmente las páginas exactas de `orders` (`Heap Blocks: exact=78`) para evitar accesos aleatorios desordenados.
   - Retorna un flujo combinado de 122 tuplas correspondientes a los pedidos de clientes alemanes.

3. **Agrupamiento y Consolidación (`GroupAggregate` vs `HashAggregate`):**
   - `Sort (quicksort Memory: 30kB)`: Ordena las 122 tuplas por `c.company_name` en RAM (`work_mem`).
   - `GroupAggregate`: Dado que las tuplas ya se encuentran ordenadas en memoria, el motor solo necesita una pasada lineal $O(N)$ para contar los pedidos de cada cliente a medida que cambia el valor de la clave de grupo, entregando el resultado final de 11 filas en solo **0.282 ms**.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Lee los tiempos globales sin entender los nodos del árbol.
- **Mid:** Identifica el Nested Loop y el filtro de país.
- **Senior / Lead:** Desglosa el mecanismo de `Bitmap Index Scan` vs `Index Scan`, analiza el uso de `work_mem` en el Quicksort, explica la diferencia de I/O y memoria entre `GroupAggregate` y `HashAggregate`, y formula recomendaciones de sintonización de parámetros (`random_page_cost`, `effective_cache_size`).

</details>

---

### Pregunta 30 - Nivel: Lead / Principal Architect

**Contexto de Negocio:** La plataforma de e-commerce experimentó un incidente crítico de sobreventa (*Overselling Bug*) durante un evento masivo de descuentos. Dos usuarios compraron simultáneamente la última unidad en stock del producto #1 (`Chai`), provocando que el inventario cayera a valores negativos y generando fallas de cumplimiento logístico.

**Enunciado:**
1. Diagnosticar la condición de carrera (*Race Condition*) de actualización perdida (*Lost Update*) que genera la sobreventa en el nivel de aislamiento por defecto de PostgreSQL (`READ COMMITTED`).
2. Diseñar la solución técnica definitiva de grado empresarial utilizando **Bloqueo Pesimista a Nivel de Fila** con `SELECT ... FOR UPDATE` dentro de un bloque transaccional atómico.
3. Explicar la diferencia entre los niveles de aislamiento `READ COMMITTED`, `REPEATABLE READ` (Snapshot Isolation) y `SERIALIZABLE` en PostgreSQL 16.

```sql
-- Consulta de verificación de stock del producto en disputa
SELECT product_id, product_name, units_in_stock FROM products WHERE product_id = 1;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 product_id | product_name | units_in_stock 
------------+--------------+----------------
          1 | Chai         |             39
(1 row)
```

<details>
<summary>Respuesta y Análisis de Arquitectura de Concurrencia</summary>

#### 💥 Diagnóstico de la Condición de Carrera (Lost Update):

En el nivel de aislamiento por defecto `READ COMMITTED`:
1. **Transacción A (Usuario 1):** Lee `units_in_stock = 1`.
2. **Transacción B (Usuario 2):** Lee concurrentemente `units_in_stock = 1` antes de que A termine.
3. **Transacción A:** Ejecuta `UPDATE products SET units_in_stock = 1 - 1 = 0` y hace `COMMIT`.
4. **Transacción B:** Basándose en su lectura inicial desactualizada (1), ejecuta `UPDATE products SET units_in_stock = 1 - 1 = 0` o resta sobre el stock causando que se vendan 2 unidades habiendo solo 1 física en almacén.

#### 🛡️ Solución Definitiva: Bloqueo Pesimista Atómico con `SELECT ... FOR UPDATE`

```sql
BEGIN;

-- 1. Adquiere un bloqueo exclusivo a nivel de fila (RowExclusiveLock)
SELECT product_id, units_in_stock 
FROM products 
WHERE product_id = 1 
FOR UPDATE;

-- 2. La lógica de aplicación valida que units_in_stock >= cantidad_solicitada
-- 3. Ejecución atómica de la reserva de inventario
UPDATE products 
SET units_in_stock = units_in_stock - 1 
WHERE product_id = 1;

COMMIT;
```

#### 🔄 Diagrama de Secuencia y Serialización de Locks:

```text
========================================================================================
CONTROL DE CONCURRENCIA PESIMISTA: SELECT ... FOR UPDATE
========================================================================================

  Transacción A (Usuario 1)                     Transacción B (Usuario 2)
  --------------------------                    --------------------------
  BEGIN;                                        BEGIN;
  
  SELECT units_in_stock                         SELECT units_in_stock
  FROM products                                 FROM products
  WHERE product_id = 1                          WHERE product_id = 1
  FOR UPDATE;                                   FOR UPDATE;
     │                                             │
  [RowExclusiveLock Adquirido]                   [EN ESPERA EN COLA DE LOCKS...]
     │                                             │ (Bloqueado a nivel de kernel)
  UPDATE products                                  │
  SET units_in_stock = 1 - 1 = 0;                  │
     │                                             │
  COMMIT; ──────────────────────────────────────► [Lock Liberado y Adquirido por B]
  [Transacción A Finalizada]                       Lee stock actualizado (= 0)
                                                   Evalúa stock < 1 -> Aborta / Rollback
                                                   "Producto Agotado" (0 sobreventas)
========================================================================================
```

#### 🧭 Matriz de Niveles de Aislamiento en PostgreSQL 16:

| Nivel de Aislamiento | Implementación en PostgreSQL | Anomalías Prevenidas | Riesgo / Costo Operacional |
| :--- | :--- | :--- | :--- |
| **`READ COMMITTED`** *(Default)* | Cada sentencia SQL ve un nuevo snapshot con commits ajenos confirmados. | Previene lecturas sucias (*Dirty Reads*). | No previene *Lost Updates* concurrentes sin `FOR UPDATE`. |
| **`REPEATABLE READ`** | **Snapshot Isolation:** Toda la transacción ve el snapshot congelado al momento del primer query. | Previene *Dirty Reads*, *Non-Repeatable Reads* y *Lost Updates*. | Si otra transacción modifica la misma fila, arroja `ERROR: could not serialize access`. Requiere lógica de reintento. |
| **`SERIALIZABLE`** | **SSI (Serializable Snapshot Isolation):** Detecta dependencias de lectura/escritura (SIREAD locks). | Previene **TODAS** las anomalías teóricas, incluyendo *Write Skew* y *Phantom Reads*. | Alto costo de memoria y abortos frecuentes bajo alta contención de transacciones. |

> 🛠️ **Nota de Arquitectura & Alta Disponibilidad:** En arquitecturas de microservicios de alto tráfico (Black Friday), la estrategia de la industria es mantener `READ COMMITTED` con `SELECT ... FOR UPDATE NOWAIT` o `SKIP LOCKED` para procesar colas asíncronas de órdenes sin generar bloqueos en cascada ni degradar el pool de conexiones (`PgBouncer`).

</details>

---

## 📋 Resumen Maestro de Preguntas y Dominio Técnico

| # | Sección Temática | Dominio de Negocio | Nivel de Entrevista | Clave de Ejecución y Motor PostgreSQL |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Filtro y Proyección | Marketing EMEA | **Junior** | `WHERE IN (...)` reescrito a `= ANY(ARRAY[...])`, ordenamiento compuesto. |
| **2** | Filtro y Proyección | Catálogo Premium | **Junior** | Predicados booleanos en cortocircuito, tipo `integer` en `discontinued`. |
| **3** | Filtro y Proyección | Logística de Fletes | **Junior** | `ORDER BY freight DESC NULLS LAST LIMIT 10`, nodo Top-N HeapSort en memoria. |
| **4** | Filtro y Proyección | Organigrama RRHH | **Junior** | Lógica trivalente con `IS NOT NULL`, concatenación `\|\|` estándar. |
| **5** | Agregación y Grupos | Rentabilidad de Ventas | **Mid** | `GROUP BY` vs `HAVING`, cálculo de ingreso neto con descuento. |
| **6** | Agregación y Grupos | Tarifas de Shippers | **Mid** | `HAVING AVG() > 50`, casteo explícito `::numeric` para `ROUND()`. |
| **7** | Agregación y Grupos | Inventario Crítico | **Mid** | Cláusula nativa estándar `COUNT(*) FILTER (WHERE stock < 20)`. |
| **8** | Agregación y Grupos | Estacionalidad Trimestral | **Mid / Senior** | CTE modular + Función de ventana global `SUM() OVER ()` para porcentajes. |
| **9** | Relaciones y Cruces | Auditoría Transaccional | **Mid** | Árbol de múltiples Hash Joins, SARGabilidad de fechas. |
| **10** | Relaciones y Cruces | Re-activación de Clientes | **Senior / Lead** | **Anti-Join Canónico:** `LEFT JOIN ... IS NULL` (2 filas: PARIS, FISSA). Peligro de `NOT IN`. |
| **11** | Relaciones y Cruces | Catálogo de Proveedores | **Mid** | Cardinalidad Cero `(0 rows)` como validación de integridad referencial. |
| **12** | Relaciones y Cruces | Jerarquía Empresarial | **Mid** | Self `LEFT JOIN` para preservar la raíz jerárquica con `COALESCE`. |
| **13** | Relaciones y Cruces | Perfil Maestro 360 | **Senior** | CTEs desacoplados con `DISTINCT ON (customer_id)` exclusivo de PostgreSQL. |
| **14** | Subconsultas | Pricing vs Media Sector | **Mid** | Tabla Derivada (*Derived Table*) en `FROM` vs subconsulta correlacionada. |
| **15** | Subconsultas | Segmentación Beverages | **Mid** | Predicate Pushdown en cadena de Joins relacionales. |
| **16** | Subconsultas | Catálogo de Ultra-Lujo | **Senior** | Predicado cuantificado universal `> ALL (subquery)` y casos de borde. |
| **17** | Subconsultas | Post-Venta y Última Orden | **Mid / Senior** | Subconsulta correlacionada en `WHERE` con `MAX(order_date)`. |
| **18** | Funciones de Ventana | Slotting de Almacén | **Senior** | `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)` vs `RANK()`. |
| **19** | Funciones de Ventana | Análisis MoM Vendedores | **Senior** | Función `LAG()`, tasa de variación y protección con `NULLIF(..., 0)`. |
| **20** | Funciones de Ventana | Tendencia y Medias Móviles | **Senior** | Encuadre físico `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` vs `RANGE`. |
| **21** | Funciones de Ventana | LTV y Running Total | **Senior** | Acumulación continua `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. |
| **22** | CTEs y Datos Sintéticos | KPI Dashboard Atómico | **Senior / Lead** | Consolidación de granularidades con `CROSS JOIN` de singletons en 1 fila. |
| **23** | CTEs y Datos Sintéticos | Dimensión Calendario | **Senior** | `generate_series` SRF y categorización ISO con `EXTRACT(ISODOW)`. |
| **24** | CTEs y Datos Sintéticos | Simulación Financiera | **Senior** | CTEs encadenados (*Chained CTEs*) para análisis de sensibilidad de precios. |
| **25** | Optimización e Índices | Clientes de Alemania | **Senior / Lead** | Estrategia de indexación en 3 niveles: B-Tree, Join y Covering Index con `INCLUDE`. |
| **26** | Optimización e Índices | Búsqueda Parcial `%text%` | **Senior / Lead** | Falla de B-Tree con comodín inicial, extensión `pg_trgm` con índice `GIN`. |
| **27** | Modelado y Negocio | Dashboard Trimestre Móvil | **Senior / Lead** | Ventanas temporales dinámicas con `INTERVAL` y subconsultas escalares. |
| **28** | Modelado y Negocio | Data Mart `fact_ventas` | **Lead / Architect** | DDL dimensional, columnas `GENERATED ALWAYS AS ... STORED` y carga ETL. |
| **29** | Rendimiento y Concurrencia | Diagnóstico de Planes | **Lead / Principal DBA** | Interpretación de `EXPLAIN (ANALYZE, COSTS OFF)`: Hash Join, Memory, Loops. |
| **30** | Rendimiento y Concurrencia | Prevención de Sobreventa | **Lead / Architect** | Control de concurrencia pesimista con `SELECT ... FOR UPDATE` y niveles de aislamiento. |
"""

print("Section 7-9 loaded.")
