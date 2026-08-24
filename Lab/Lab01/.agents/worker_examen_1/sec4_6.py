# -*- coding: utf-8 -*-
"""
Sections 4, 5, 6 (Questions 14 to 24) for 4.examen_entrevista.md
"""

sec4_6_text = """## Sección 4: Subconsultas, Expresiones Correlacionadas y Predicados Cuantificados (4 preguntas)

### Pregunta 14 - Nivel: Mid

**Contexto de Negocio:** El área de Pricing y Estrategia Comercial necesita identificar productos que se posicionan con un precio premium por encima de la media de su propia categoría, para evaluar si su margen de contribución justifica posibles descuentos promocionales.

**Enunciado:** Listar el nombre del producto (`product_name`), precio unitario (`unit_price`), nombre de la categoría (`category_name`) y el precio promedio de dicha categoría (`precio_promedio_categoria`). Filtrar únicamente aquellos productos cuyo precio unitario sea estrictamente mayor al precio promedio de su categoría, utilizando una tabla derivada (*Derived Table*) en la cláusula `FROM`. Ordenar por nombre de categoría y luego por precio unitario descendente (mostrar los primeros 10 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Comparativa de precio individual vs media agregada del grupo.
2. **Entidad & Grano:** Tabla `products` (grano: 1 fila por producto).
3. **Subconsulta Derivada:** Cálculo del promedio agrupado por `category_id`.
4. **Filtro de Comparación:** `p.unit_price > sub.precio_promedio_categoria`.
5. **Entrega Ejecutiva:** Ordenamiento por `category_name, unit_price DESC LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
         product_name         | unit_price | category_name | precio_promedio_categoria 
------------------------------+------------+---------------+---------------------------
 Côte de Blaye                |      263.5 | Beverages     |       37.9791666666666667
 Ipoh Coffee                  |         46 | Beverages     |       37.9791666666666667
 Vegie-spread                 | 43.9000015 | Condiments    |       22.8541668250000000
 Northwoods Cranberry Sauce   |         40 | Condiments    |       22.8541668250000000
 Sirop d'érable               |       28.5 | Condiments    |       22.8541668250000000
 Grandma's Boysenberry Spread |         25 | Condiments    |       22.8541668250000000
 Sir Rodney's Marmalade       |         81 | Confections   |       25.1600000623076923
 Tarte au sucre               | 49.2999992 | Confections   |       25.1600000623076923
 Schoggi Schokolade           | 43.9000015 | Confections   |       25.1600000623076923
 Gumbär Gummibärchen          | 31.2299995 | Confections   |       25.1600000623076923
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> 1. Evalúa la tabla derivada 'sub': Agrupa products en 8 categorías y calcula AVG.
                   2. Hash Join entre products (77 tuplas) y 'sub' (8 tuplas) por category_id.
                   3. Hash Join con 'categories' para recuperar category_name.
[4. WHERE]      -> Evalúa predicado escalar: p.unit_price > sub.precio_promedio_categoria.
                   Filtra 25 productos premium -> Conserva los que superan la media.
[8. SELECT]     -> Proyecta columnas requeridas.
[11. ORDER BY]  -> Ordena por category_name ASC, unit_price DESC.
[12. LIMIT]     -> Entrega los primeros 10 registros.
========================================================================================
```

**Análisis de Optimización: Derived Table vs Correlated Subquery:**
- **Tabla Derivada (Derived Table):** Se calcula **una sola vez** en memoria ($O(N)$), produciendo 8 filas que luego se cruzan mediante un `Hash Join` ultra rápido.
- **Subconsulta Correlacionada en WHERE:** `WHERE unit_price > (SELECT AVG(...) FROM products p2 WHERE p2.category_id = p.category_id)` ejecuta conceptualmente $N$ subconsultas (una por cada fila de la tabla externa, $O(N \times M)$), a menos que el optimizador logre desanidar (*decorrelate*) la consulta.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Resuelve con subconsulta correlacionada en el `WHERE`.
- **Mid:** Usa tabla derivada en el `FROM` con `INNER JOIN`.
- **Senior / Lead:** Demuestra la equivalencia con funciones de ventana (`AVG(unit_price) OVER (PARTITION BY category_id)`) y compara los costos en `EXPLAIN`.

</details>

---

### Pregunta 15 - Nivel: Mid

**Contexto de Negocio:** El Gerente de la Unidad de Negocios de Bebidas (*Beverages Business Unit*) necesita identificar a los 10 clientes más leales y de mayor volumen de compra en su categoría para invitarlos a una cata exclusiva de vinos y licores.

**Enunciado:** Listar el identificador del cliente (`customer_id`), nombre de la empresa (`company_name`) y el importe neto total gastado exclusivamente en productos de la categoría `'Beverages'` (`total_beverages`, calculado como `SUM(cantidad * precio * (1 - descuento))`). Ordenar por facturación total en bebidas de mayor a menor, mostrando únicamente los primeros 10 clientes.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Ranking de clientes por gasto específico en la categoría 'Beverages'.
2. **Entidad Base & Cruces:** `orders` $\bowtie$ `customers` $\bowtie$ `order_details` $\bowtie$ `products` $\bowtie$ `categories`.
3. **Filtro Temprano (`WHERE`):** `cat.category_name = 'Beverages'`.
4. **Agregación:** `GROUP BY o.customer_id, c.company_name`.
5. **Entrega Ejecutiva:** `ORDER BY total_beverages DESC LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 customer_id |        company_name        | total_beverages 
-------------+----------------------------+-----------------
 QUICK       | QUICK-Stop                 |        36216.43
 HANAR       | Hanari Carnes              |        20084.15
 RATTC       | Rattlesnake Canyon Grocery |        19208.15
 ERNSH       | Ernst Handel               |        12709.30
 GREAL       | Great Lakes Food Market    |        11694.37
 PICCO       | Piccolo und mehr           |        10608.00
 SIMOB       | Simons bistro              |        10540.00
 QUEEN       | Queen Cozinha              |        10483.50
 SAVEA       | Save-a-lot Markets         |        10032.00
 KOENE       | Königlich Essen            |         9455.10
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM / JOIN] -> Cadena de 4 Hash Joins.
[4. WHERE]       -> Predicate Pushdown: El optimizador aplica cat.category_name = 'Beverages'
                    inmediatamente sobre la tabla 'categories', reduciendo la dimensión a 1 sola fila
                    (category_id=1) antes de cruzar con products (12 bebidas) y order_details.
[5. GROUP BY]    -> HashAggregate por o.customer_id, c.company_name.
[8. SELECT]      -> Calcula la suma neta y redondea a 2 decimales.
[11. ORDER BY]   -> Top-N HeapSort por total_beverages DESC.
[12. LIMIT]      -> Entrega el Top 10 de clientes premium.
========================================================================================
```

**Análisis de Optimización y Pushdown:**
- El optimizador de PostgreSQL reordena internamente la secuencia de joins para filtrar primero la tabla más selectiva (`categories` = 1 fila), evitando uniones innecesarias con productos de otras categorías.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe los 4 joins correctamente pero olvida agrupar por clave primaria + nombre o no redondea.
- **Mid / Senior:** Comprende la propagación de filtros (*Predicate Pushdown*) y garantiza consultas con agrupamiento estricto sobre claves primarias.

</details>

---

### Pregunta 16 - Nivel: Senior

**Contexto de Negocio:** El área de inteligencia de mercado está realizando un estudio sobre productos de lujo supremo. Se desea detectar si existe en todo el catálogo de la empresa algún producto cuyo precio unitario sea estrictamente superior a **TODOS** los precios unitarios de la categoría de Bebidas (`'Beverages'`).

**Enunciado:** Listar el nombre del producto (`product_name`), precio unitario (`unit_price`) y nombre de su categoría (`category_name`) para aquellos productos cuyo precio sea mayor que todos los precios de los productos pertenecientes a la categoría `'Beverages'`, utilizando obligatoriamente el operador cuantificado universal `> ALL (subconsulta)`. Ordenar por precio unitario descendente.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Detección de artículos con precio superior al máximo absoluto de una categoría de referencia.
2. **Operador Cuantificado:** `WHERE p.unit_price > ALL (SELECT p2.unit_price FROM ... WHERE category = 'Beverages')`.
3. **Equivalencia Lógica:** `p.unit_price > ALL (Set)` equivale formalmente a `p.unit_price > MAX(Set)`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 product_name | unit_price | category_name 
--------------+------------+---------------
(0 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. EVALUACIÓN SUBCONSULTA] -> Extrae el conjunto de precios de 'Beverages':
                               {18.00, 19.00, 10.00, 263.50, 4.50, 14.00, 18.00, 263.50 (Côte de Blaye), ...}
                               El valor máximo dentro de Beverages es $263.50.
[2. EVALUACIÓN PREDICADO > ALL] -> Para que una fila pase, su unit_price debe ser > 263.50.
                                   Dado que $263.50 es el precio más alto de TODA la base de datos Northwind,
                                   ningún producto de ninguna categoría supera este umbral.
[3. RETORNO]                -> Entrega conjunto vacío legítimo (0 rows).
========================================================================================
```

**Comportamiento de los Cuantificadores Cuantificados en SQL (`ALL` vs `ANY`):**
- `x > ALL (S)`: Retorna TRUE si `x` es mayor que cada uno de los elementos de `S`.
  - Si `S` está vacío ($\emptyset$), `x > ALL (\emptyset)` evalúa como **TRUE** (vacuously true).
  - Si `S` contiene un `NULL` y no hay falsación estricta, evalúa como **UNKNOWN**.
- `x > ANY (S)` o `x > SOME (S)`: Retorna TRUE si `x` es mayor que al menos un elemento de `S`. Equivale a `x > MIN(S)`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Confunde `> ALL` con `> ANY` o entra en pánico ante el resultado de 0 filas.
- **Mid:** Explica la equivalencia con `> MAX()` y justifica por qué retorna 0 filas en Northwind.
- **Senior / Lead:** Analiza el comportamiento formal ante conjuntos vacíos y presencia de valores NULL, destacando las reglas de inferencia lógica del optimizador.

</details>

---

### Pregunta 17 - Nivel: Mid / Senior

**Contexto de Negocio:** El equipo de fidelización (*Customer Success*) necesita automatizar una encuesta de satisfacción post-compra. Para cada cliente de la empresa, se requiere identificar de forma precisa su orden más reciente registrada en el sistema.

**Enunciado:** Para cada cliente registrado en la base de datos, mostrar el nombre de la empresa (`company_name`), el ID de su pedido más reciente (`order_id`), la fecha de la orden (`order_date`) y el flete (`freight`), utilizando obligatoriamente una **subconsulta correlacionada** en la cláusula `WHERE`. Ordenar por fecha de orden descendente (mostrar los primeros 10 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Última transacción histórica por cliente.
2. **Entidad & Relación:** `orders o` $\bowtie$ `customers c`.
3. **Correlación en WHERE:** `WHERE o.order_date = (SELECT MAX(o2.order_date) FROM orders o2 WHERE o2.customer_id = o.customer_id)`.
4. **Entrega Ejecutiva:** Ordenamiento por `order_date DESC LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
        company_name        | order_id | order_date |   freight   
----------------------------+----------+------------+-------------
 Rattlesnake Canyon Grocery |    11077 | 1998-05-06 |  8.52999973
 Richter Supermarkt         |    11075 | 1998-05-06 |  6.19000006
 Simons bistro              |    11074 | 1998-05-06 |  18.4400005
 Bon app'                   |    11076 | 1998-05-06 |  38.2799988
 Pericles Comidas clásicas  |    11073 | 1998-05-05 |  24.9500008
 Ernst Handel               |    11072 | 1998-05-05 |  258.640015
 Lehmanns Marktstand        |    11070 | 1998-05-05 |         136
 LILA-Supermercado          |    11071 | 1998-05-05 | 0.930000007
 Queen Cozinha              |    11068 | 1998-05-04 |       81.75
 Drachenblut Delikatessen   |    11067 | 1998-05-04 |  7.98000002
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga 'orders o' y cruza con 'customers c'.
[4. WHERE]      -> SubPlan Correlacionado:
                   Por cada orden evaluada, ejecuta la subconsulta pasando 'o.customer_id' como parámetro.
                   Recupera el MAX(order_date) para ese cliente y valida la igualdad.
[8. SELECT]     -> Proyecta company_name, order_id, order_date y freight.
[11. ORDER BY]  -> Top-N HeapSort por order_date DESC.
[12. LIMIT]      -> Entrega las 10 transacciones más recientes.
========================================================================================
```

**⚠️ Caso de Borde en Producción:**
Si un cliente registró múltiples pedidos en exactamente la misma fecha máxima (`order_date`), la subconsulta correlacionada devolverá todas las órdenes de ese día (empates). Para garantizar determinismo estricto de una sola orden por cliente, se debe ordenar adicionalmente por `order_id DESC` utilizando `ROW_NUMBER()` o `DISTINCT ON`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe la correlación pero olvida vincular `o2.customer_id = o.customer_id`.
- **Mid:** Implementa la subconsulta correlacionada exacta.
- **Senior / Lead:** Discute el costo de $O(N \times M)$ del SubPlan y propone crear el índice compuesto `orders(customer_id, order_date DESC)` para transformar el escaneo en una serie de `Index Only Scans` ultra eficientes.

</details>

---

## Sección 5: Funciones de Ventana y Analítica Avanzada (4 preguntas)

### Pregunta 18 - Nivel: Senior

**Contexto de Negocio:** La dirección de producto requiere un ranking de popularidad de artículos para optimizar la ubicación física de mercancías en los centros de distribución (*Warehouse Slotting*). Se debe rankear cada producto según el total de unidades físicas vendidas dentro de su propia categoría, reiniciando la numeración con cada nueva familia de productos.

**Enunciado:** Construir una consulta analítica que calcule el total de unidades vendidas por producto y asigne una posición ordinal continua sin empates (`ranking` ordinal 1, 2, 3...) dentro de cada categoría utilizando `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)`. Mostrar el nombre de la categoría (`category_name`), nombre del producto (`product_name`), unidades vendidas (`unidades_vendidas`) y la posición en el ranking. Ordenar por nombre de categoría y ranking ascendente (mostrar los primeros 15 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Ranking intra-categoría de volumen de ventas.
2. **Nivel 1 (Agregación Base en CTE):** Totalizar unidades por categoría y producto con `SUM(quantity)`.
3. **Nivel 2 (Ventana Analítica):** `ROW_NUMBER() OVER (PARTITION BY category_name ORDER BY unidades_vendidas DESC)`.
4. **Entrega Ejecutiva:** Ordenamiento por `category_name, ranking LIMIT 15`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 category_name |           product_name           | unidades_vendidas | ranking 
---------------+----------------------------------+-------------------+---------
 Beverages     | Rhönbräu Klosterbier             |              1155 |       1
 Beverages     | Guaraná Fantástica               |              1125 |       2
 Beverages     | Chang                            |              1057 |       3
 Beverages     | Lakkalikööri                     |               981 |       4
 Beverages     | Steeleye Stout                   |               883 |       5
 Beverages     | Chai                             |               828 |       6
 Beverages     | Outback Lager                    |               817 |       7
 Beverages     | Chartreuse verte                 |               793 |       8
 Beverages     | Côte de Blaye                    |               623 |       9
 Beverages     | Ipoh Coffee                      |               580 |      10
 Beverages     | Sasquatch Ale                    |               506 |      11
 Beverages     | Laughing Lumberjack Lager        |               184 |      12
 Condiments    | Original Frankfurter grüne Soße  |               791 |       1
 Condiments    | Louisiana Fiery Hot Pepper Sauce |               745 |       2
 Condiments    | Sirop d'érable                   |               603 |       3
(15 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[FASE 1: CTE ventas_producto]
  - Cruza order_details, products y categories -> GROUP BY category_name, product_name.
  - Produce 77 filas agregadas con total de unidades vendidas.

[FASE 2: CONSULTA PRINCIPAL]
  - [1. FROM]   -> Carga las 77 tuplas del CTE.
  - [7. WINDOW] -> WindowAgg:
                   1. Particiona en memoria por 'category_name' (8 particiones).
                   2. Ordena cada partición por 'unidades_vendidas DESC'.
                   3. Asigna contador incremental monótono ROW_NUMBER() (1..N) por partición.
  - [8. SELECT] -> Proyecta columnas y ranking.
  - [11. ORDER BY] -> Ordena por category_name, ranking ASC.
  - [12. LIMIT] -> Entrega 15 tuplas.
========================================================================================
```

**Diferencias Críticas entre Funciones de Ranking en PostgreSQL:**

| Función | Comportamiento ante Empates (Ej: valores 100, 100, 80) | Secuencia Generada | Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **`ROW_NUMBER()`** | No admite empates; asigna números consecutivos arbitrarios. | `1, 2, 3` | Paginación, desduplicación determinista. |
| **`RANK()`** | Asigna el mismo rango en empates y **deja huecos** posteriores. | `1, 1, 3` | Clasificaciones deportivas oficiales. |
| **`DENSE_RANK()`** | Asigna el mismo rango en empates **sin dejar huecos**. | `1, 1, 2` | Rankings comerciales continuos (Top N salarios). |

**¿Por qué las funciones de ventana NO pueden colocarse en `WHERE` o `HAVING`?**
Por el **Orden Lógico de Ejecución**: `WHERE` se evalúa en el Paso 4 y `HAVING` en el Paso 6, mientras que las funciones de ventana (`WINDOW`) se calculan en el Paso 7 sobre el conjunto de filas ya filtrado y agrupado. Intentar filtrar un `ROW_NUMBER()` en `WHERE` producirá `ERROR: window functions are not allowed in WHERE`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Intenta colocar la función de ventana directamente en `WHERE` sin usar CTE.
- **Mid:** Usa CTE y `ROW_NUMBER()`, explicando la partición.
- **Senior / Lead:** Contrasta `ROW_NUMBER()` vs `RANK()` vs `DENSE_RANK()`, explica por qué las ventanas operan en el Paso 7 del pipeline y diseña consultas Top-N con subconsultas de filtrado.

</details>

---

### Pregunta 19 - Nivel: Senior

**Contexto de Negocio:** La Gerencia de Ventas requiere un análisis de evolución mensual (*Month-over-Month - MoM*) del desempeño de cada ejecutivo comercial. Se debe calcular la facturación mensual neta de cada vendedor, compararla contra el mes inmediatamente anterior utilizando la función `LAG()`, y determinar la variación porcentual de crecimiento o contracción de ventas.

**Enunciado:** Para cada empleado y mes calendario en que registró actividad comercial, mostrar el nombre completo del empleado (`empleado`), el mes (`mes`, formateado como fecha de inicio de mes con `DATE_TRUNC`), la facturación neta del mes (`ventas_mes`), la facturación del mes anterior (`ventas_anterior`) y la variación porcentual (`variacion_pct`, calculada como `((ventas - anterior) / anterior) * 100`). Excluir el primer mes de actividad de cada vendedor (donde no existe mes anterior, `ventas_anterior IS NOT NULL`). Proteger el cálculo contra división por cero con `NULLIF()`. Ordenar por empleado y mes cronológico (mostrar los primeros 10 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Tasa de variación porcentual mensual (MoM) por vendedor.
2. **Nivel 1 (Agregación Mensual en CTE):** `DATE_TRUNC('month', order_date)` con `GROUP BY employee_id, mes`.
3. **Nivel 2 (Offset de Ventana):** `LAG(ventas) OVER (PARTITION BY employee_id ORDER BY mes)`.
4. **Nivel 3 (Filtro y Cálculo):** `WHERE ventas_anterior IS NOT NULL` y cálculo porcentual protegido con `NULLIF(ventas_anterior, 0)`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
   empleado    |    mes     | ventas_mes | ventas_anterior | variacion_pct 
---------------+------------+------------+-----------------+---------------
 Andrew Fuller | 1996-08-01 |    1814.00 |         1176.00 |         54.25
 Andrew Fuller | 1996-09-01 |    2950.80 |         1814.00 |         62.67
 Andrew Fuller | 1996-10-01 |    5164.00 |         2950.80 |         75.00
 Andrew Fuller | 1996-11-01 |    4614.58 |         5164.00 |        -10.64
 Andrew Fuller | 1996-12-01 |    6037.68 |         4614.58 |         30.84
 Andrew Fuller | 1997-01-01 |    3059.88 |         6037.68 |        -49.32
 Andrew Fuller | 1997-02-01 |    1584.00 |         3059.88 |        -48.23
 Andrew Fuller | 1997-03-01 |    2844.90 |         1584.00 |         79.60
 Andrew Fuller | 1997-04-01 |   13118.65 |         2844.90 |        361.13
 Andrew Fuller | 1997-05-01 |    4373.32 |        13118.65 |        -66.66
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. CTE 1: Agregación Mensual] -> Colapsa pedidos a nivel (employee_id, mes).
[2. CTE 2: Función LAG]        -> WindowAgg: Particiona por employee_id, ordena por mes ASC.
                                  Para cada fila, recupera la tupla N-1 de la partición.
[3. CONSULTA PRINCIPAL]
  - [4. WHERE]     -> Filtra 'ventas_anterior IS NOT NULL' (elimina el mes ancla de cada vendedor).
  - [8. SELECT]    -> Aplica NULLIF() para evitar divisiones por cero y calcula la tasa de cambio.
  - [11. ORDER BY] -> Ordena por empleado y mes.
========================================================================================
```

**Análisis de Resiliencia en Producción:**
- `NULLIF(cl.ventas_anterior, 0)`: Si las ventas anteriores fueron $0, `NULLIF` transforma el cero en `NULL`. Al dividir por `NULL`, el resultado es `NULL` en lugar de abortar la transacción con un error fatal `division by zero`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Intenta usar auto-joins por mes perdiendo meses discontinuos.
- **Mid:** Usa `LAG()` pero olvida particionar por empleado o no protege la división.
- **Senior / Lead:** Encadena CTEs con `PARTITION BY`, usa `NULLIF()` defensivo y explica la lectura en buffer del nodo `WindowAgg`.

</details>

---

### Pregunta 20 - Nivel: Senior

**Contexto de Negocio:** El área de Finanzas y Planificación Operacional (*FP&A*) necesita suavizar la volatilidad estacional de las ventas para detectar la tendencia de fondo del negocio. Se requiere calcular una media móvil trimestral (*3-Month Rolling Average*) sobre la facturación global de la empresa y clasificar cada mes según si su desempeño superó o estuvo por debajo de dicha media móvil.

**Enunciado:** Calcular las ventas totales netas por mes calendario y su media móvil de 3 meses (considerando el mes actual y los 2 meses precedentes mediante `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`). Mediante una sentencia `CASE`, etiquetar la columna `tendencia` como `'Por encima'` si la venta del mes superó a la media móvil, o `'Por debajo'` en caso contrario. Ordenar cronológicamente por mes (mostrar los primeros 12 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Suavizamiento de serie temporal (Rolling Average de 3 periodos) + clasificación de tendencia.
2. **Grano Base (CTE):** Facturación total agregada por mes calendario (`DATE_TRUNC`).
3. **Marco de Ventana Físico:** `AVG(ventas) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
4. **Lógica de Negocio:** `CASE WHEN ventas > avg_movil THEN 'Por encima' ELSE 'Por debajo' END`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
    mes     | ventas_totales | promedio_movil_3m | tendencia  
------------+----------------+-------------------+------------
 1996-07-01 |       27861.90 |          27861.90 | Por debajo
 1996-08-01 |       25485.28 |          26673.59 | Por debajo
 1996-09-01 |       26381.40 |          26576.19 | Por debajo
 1996-10-01 |       37515.72 |          29794.13 | Por encima
 1996-11-01 |       45600.05 |          36499.06 | Por encima
 1996-12-01 |       45239.63 |          42785.13 | Por encima
 1997-01-01 |       61258.07 |          50699.25 | Por encima
 1997-02-01 |       38483.63 |          48327.11 | Por debajo
 1997-03-01 |       38547.22 |          46096.31 | Por debajo
 1997-04-01 |       53032.95 |          43354.60 | Por encima
 1997-05-01 |       53781.29 |          48453.82 | Por encima
 1997-06-01 |       36362.80 |          47725.68 | Por debajo
(12 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. CTE ventas_mensuales] -> Agrupa las 830 órdenes por mes calendario (produce 23 meses de historia).
[2. CONSULTA PRINCIPAL]
  - [7. WINDOW] -> Framing Físico (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW):
                   - Mes 1: Marco = [Mes 1] -> Promedio = Ventas(Mes 1)
                   - Mes 2: Marco = [Mes 1, Mes 2] -> Promedio = (Ventas 1 + Ventas 2)/2
                   - Mes 3+: Marco = [Mes N-2, Mes N-1, Mes N] -> Promedio exacto de 3 filas.
  - [8. SELECT] -> Evalúa la expresión CASE comparando ventas vs la media móvil.
  - [11. ORDER BY] -> Ordena por mes cronológico.
========================================================================================
```

**Diferencia Fundamental: `ROWS` vs `RANGE` en PostgreSQL:**
- **`ROWS` (Encuadre Físico):** Cuenta un número exacto de tuplas físicas en memoria. `2 PRECEDING` garantiza estrictamente las 2 filas anteriores.
- **`RANGE` (Encuadre Lógico):** Evalúa un rango de valores basado en la columna del `ORDER BY`. Si existen duplicados en la clave de ordenamiento, `RANGE` incluye todos los empates en el mismo marco, lo que puede distorsionar el cálculo de medias móviles.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Usa `AVG() OVER ()` sin framing, calculando la media global estática.
- **Mid:** Usa `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` con el `CASE`.
- **Senior / Lead:** Explica la diferencia técnica entre `ROWS` y `RANGE`, y propone la cláusula reutilizable `WINDOW w AS (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` para no duplicar código en el `CASE`.

</details>

---

### Pregunta 21 - Nivel: Senior

**Contexto de Negocio:** La dirección comercial necesita monitorear la curva de valor acumulado de vida del cliente (*Customer Lifetime Value - LTV Running Total*). Para cada cliente de la empresa, se requiere observar cómo evoluciona su facturación mes a mes y cómo se va acumulando progresivamente el importe total de sus compras desde su primera transacción histórica.

**Enunciado:** Para cada cliente y mes en que haya registrado pedidos, mostrar el nombre de la empresa (`company_name`), el mes (`mes`), la facturación neta del mes (`ventas_mes`) y la facturación acumulada histórica desde su primer pedido (`ventas_acumuladas`, utilizando `SUM(...) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`). Ordenar por nombre de empresa y mes cronológico (mostrar los primeros 12 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Facturación acumulada histórica (*Running Total / Cumulative Sum*) por cliente.
2. **Nivel 1 (CTE):** Agregación mensual a nivel `(customer_id, mes)`.
3. **Nivel 2 (Ventana Acumulativa):** `SUM(ventas) OVER (PARTITION BY customer_id ORDER BY mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
4. **Entrega Ejecutiva:** Ordenamiento por `company_name, mes LIMIT 12`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
            company_name            |    mes     | ventas_mes | ventas_acumuladas 
------------------------------------+------------+------------+-------------------
 Alfreds Futterkiste                | 1997-08-01 |     814.50 |            814.50
 Alfreds Futterkiste                | 1997-10-01 |    1208.00 |           2022.50
 Alfreds Futterkiste                | 1998-01-01 |     845.80 |           2868.30
 Alfreds Futterkiste                | 1998-03-01 |     471.20 |           3339.50
 Alfreds Futterkiste                | 1998-04-01 |     933.50 |           4273.00
 Ana Trujillo Emparedados y helados | 1996-09-01 |      88.80 |             88.80
 Ana Trujillo Emparedados y helados | 1997-08-01 |     479.75 |            568.55
 Ana Trujillo Emparedados y helados | 1997-11-01 |     320.00 |            888.55
 Ana Trujillo Emparedados y helados | 1998-03-01 |     514.40 |           1402.95
 Antonio Moreno Taquería            | 1996-11-01 |     403.20 |            403.20
 Antonio Moreno Taquería            | 1997-04-01 |     749.06 |           1152.26
 Antonio Moreno Taquería            | 1997-05-01 |    1940.85 |           3093.11
(12 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. CTE ventas_cliente_mes] -> Agrupa por (customer_id, mes).
[2. CONSULTA PRINCIPAL]
  - [7. WINDOW] -> WindowAgg:
                   1. Particiona por vcm.customer_id.
                   2. Ordena cronológicamente por vcm.mes ASC.
                   3. Ejecuta acumulador running total: Mantiene el estado de suma en memoria
                      y acumula cada nueva fila desde el inicio de la partición (UNBOUNDED PRECEDING).
                      Al cambiar de cliente, el acumulador se reinicia automáticamente a 0.
  - [8. SELECT] -> Proyecta nombre de empresa, mes, venta mensual y acumulado.
  - [11. ORDER BY] -> Ordena por company_name, mes.
========================================================================================
```

**Análisis de Eficiencia vs Auto-Joins Triangulares:**
- Antes de la introducción de las funciones de ventana en SQL:2003, calcular una suma acumulada requería un **Self-Join Triangular** del tipo `FROM t1 INNER JOIN t2 ON t1.id = t2.id AND t2.mes <= t1.mes`, lo que genera una complejidad cuadrática $O(N^2)$ y colapsa el rendimiento en tablas grandes.
- Con `SUM(...) OVER (...)`, PostgreSQL evalúa la suma en una sola pasada $O(N)$ con consumo mínimo de CPU.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Olvida el `PARTITION BY`, acumulando erróneamente las ventas de todos los clientes mezcladas.
- **Mid:** Escribe el `SUM() OVER (PARTITION BY ... ORDER BY ...)` correctamente.
- **Senior / Lead:** Explica el ahorro algorítmico frente a joins triangulares ($O(N)$ vs $O(N^2)$) y detalla el funcionamiento del autómata acumulador en el nodo `WindowAgg`.

</details>

---

## Sección 6: Expresiones de Tabla Comunes (CTEs) y Datos Sintéticos (3 preguntas)

### Pregunta 22 - Nivel: Senior / Lead

**Contexto de Negocio:** El Directorio de la compañía exige un reporte ejecutivo de una sola fila (*Single-Row Executive KPI Dashboard*) para el tablero de control de mando gerencial. La consulta debe consolidar métricas globales agregadas (total de clientes con compras, total de órdenes, facturación global, ticket promedio) y, en la misma fila, entregar la identidad y facturación del cliente #1 de la historia de la empresa.

**Enunciado:** Construir una consulta utilizando múltiples CTEs (`WITH`) que entregue **exactamente en una sola fila**:
- `total_clientes`: Cantidad de clientes únicos que han realizado al menos una compra.
- `total_pedidos`: Cantidad total de órdenes registradas en la empresa.
- `ingreso_total`: Facturación neta total histórica redondeada a 2 decimales.
- `ticket_promedio`: Facturación neta promedio por pedido (`ingreso_total / total_pedidos`).
- `cliente_top`: Nombre de la empresa cliente con mayor facturación histórica.
- `facturacion_top`: Monto neto facturado por dicho cliente top.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Tablero atómico de KPIs generales + Entidad Top 1 en un solo registro.
2. **Modularización con CTEs:**
   - **CTE 1 (`metricas_generales`):** Agregación escalar de órdenes y líneas de pedido (retorna exactamente 1 fila).
   - **CTE 2 (`top_cliente`):** Agregación a nivel de cliente ordenada por facturación DESC con `LIMIT 1` (retorna exactamente 1 fila).
3. **Consolidación:** Producto cartesiano controlado `CROSS JOIN` entre ambos conjuntos de 1 sola fila ($1 \times 1 = 1$).

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
FROM metricas_generales mg
CROSS JOIN top_cliente tc;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 total_clientes | total_pedidos | ingreso_total | ticket_promedio | cliente_top | facturacion_top 
----------------+---------------+---------------+-----------------+-------------+-----------------
             89 |           830 |    1265793.04 |         1525.05 | QUICK-Stop  |       110277.31
(1 row)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. CTE metricas_generales] -> Escanea orders y order_details -> Produce 1 fila escalar.
[2. CTE top_cliente]        -> Agrupa por cliente -> Sort DESC -> Top 1 (QUICK-Stop, $110,277.31).
[3. CONSULTA PRINCIPAL]
  - [1. FROM / CROSS JOIN]  -> Multiplica 1 fila x 1 fila -> Exactamente 1 tupla combinada.
  - [8. SELECT]             -> Proyecta los 6 KPIs ejecutivos.
========================================================================================
```

**Análisis de Arquitectura:**
- Intentar calcular estos valores en una sola sentencia SQL sin CTEs obligaría a realizar subconsultas anidadas desordenadas en el `SELECT` o a multiplicar granularidades en el `GROUP BY`, degradando la legibilidad y el mantenimiento.
- El uso de `CROSS JOIN` explícito documenta formalmente la intención de unir dos tuplas singleton.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Intenta agruparlo todo en un solo query mezclando el grano general con el grano de cliente.
- **Mid:** Usa CTEs pero utiliza sintaxis implícita de coma `FROM a, b` sin justificar.
- **Senior / Lead:** Estructura CTEs limpios, usa `CROSS JOIN` explícito y explica la optimización de materialización de CTEs en PostgreSQL 12+ (`AS NOT MATERIALIZED`).

</details>

---

### Pregunta 23 - Nivel: Senior

**Contexto de Negocio:** El área de Logística y Operaciones necesita construir un generador de calendarios de control de entregas (*Date Dimension Generator*) para calcular los plazos de entrega (*Lead Time*) considerando exclusivamente días laborales hábiles de lunes a viernes.

**Enunciado:** Utilizando la función generadora de conjuntos nativa de PostgreSQL `generate_series`, generar la serie completa de fechas para el mes de enero de 1997 (`1997-01-01` a `1997-01-31`). Para cada fecha, proyectar el día de la semana en texto (`TO_CHAR(fecha, 'Day')`) y clasificarlo mediante una cláusula `CASE` con la función `EXTRACT(ISODOW FROM fecha)` como `'Laboral'` (si es de lunes a viernes, valores 1 a 5) o `'Fin de semana'` (valores 6 y 7). Ordenar cronológicamente por fecha (mostrar los primeros 12 días).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Generación sintética de dimensión temporal con categorización de días hábiles.
2. **Generador Set-Returning:** `generate_series('1997-01-01'::date, '1997-01-31'::date, '1 day'::interval)`.
3. **Estándar ISO DOW:** `EXTRACT(ISODOW FROM fecha)` (1=Lunes, ..., 7=Domingo).
4. **Entrega Ejecutiva:** Ordenamiento por `fecha ASC LIMIT 12`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
   fecha    | dia_semana |   tipo_dia    
------------+------------+---------------
 1997-01-01 | Wednesday  | Laboral
 1997-01-02 | Thursday   | Laboral
 1997-01-03 | Friday     | Laboral
 1997-01-04 | Saturday   | Fin de semana
 1997-01-05 | Sunday     | Fin de semana
 1997-01-06 | Monday     | Laboral
 1997-01-07 | Tuesday    | Laboral
 1997-01-08 | Wednesday  | Laboral
 1997-01-09 | Thursday   | Laboral
 1997-01-10 | Friday     | Laboral
 1997-01-11 | Saturday   | Fin de semana
 1997-01-12 | Sunday     | Fin de semana
(12 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Function Scan: El motor ejecuta la función C interna generate_series()
                   generando 31 tuplas de tipo fecha en memoria sin leer páginas de disco Heap.
[8. SELECT]     -> Evalúa TO_CHAR() y la lógica booleana ISODOW en el CASE.
[11. ORDER BY]  -> Ordena cronológicamente por fecha ASC.
[12. LIMIT]     -> Entrega los primeros 12 días.
========================================================================================
```

**Diferencia Crítica: `ISODOW` vs `DOW` en PostgreSQL:**
- **`EXTRACT(ISODOW FROM fecha)` (Estándar ISO 8601):**
  Lunes = 1, Martes = 2, Miércoles = 3, Jueves = 4, Viernes = 5, Sábado = 6, Domingo = 7.
  Permite una condición limpia y no ambigua: `BETWEEN 1 AND 5` para días laborables.
- **`EXTRACT(DOW FROM fecha)` (Estándar tradicional):**
  Domingo = 0, Lunes = 1, ..., Sábado = 6.
  Requiere condiciones disyuntivas más complejas: `WHERE DOW BETWEEN 1 AND 5`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Desconoce `generate_series` e intenta crear una tabla física con inserts manuales.
- **Mid:** Usa `generate_series` pero usa `DOW` tradicional de forma confusa.
- **Senior / Lead:** Emplea `ISODOW` estándar ISO 8601, explica el nodo `Function Scan` y demuestra cómo usar esta técnica para rellenar vacíos (*Zero-Filling / Gap Analysis*) en reportes de series de tiempo.

</details>

---

### Pregunta 24 - Nivel: Senior

**Contexto de Negocio:** El Comité de Precios y Estrategia Financiera está simulando un escenario inflacionario donde se incrementa linealmente el precio de todos los productos activos en un **+10%**. Se requiere un análisis de sensibilidad que muestre el precio actual, el precio simulado y la ganancia monetaria adicional por unidad (*Delta de Margen*), ordenando los artículos de mayor a menor impacto financiero.

**Enunciado:** Construir una consulta modular con CTEs encadenados:
- **CTE 1 (`precios_actuales`):** Filtrar los productos vigentes (`discontinued = 0`), obteniendo su ID, nombre y precio actual.
- **CTE 2 (`precios_simulados`):** Calcular sobre el CTE anterior el nuevo precio incrementado en un 10%, redondeado a 2 decimales (`precio_actual * 1.10`).
- **Consulta Principal:** Unir ambos CTEs por `product_id`, proyectar el nombre del producto, precio actual, precio simulado y la diferencia absoluta (`precio_simulado - precio_actual`), ordenando por la mayor diferencia descendente (mostrar los primeros 10 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Simulación de reajuste de precios (+10%) y ranking de impacto unitario.
2. **Diseño Modular Chained CTEs:**
   - CTE 1: Universo base de productos activos.
   - CTE 2: Transformación matemática sobre el CTE 1.
3. **Cálculo de Delta:** Comparación y cálculo de varianza monetaria.
4. **Entrega Ejecutiva:** `ORDER BY diferencia DESC LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
        product_name        | precio_actual | precio_simulado | diferencia 
----------------------------+---------------+-----------------+------------
 Côte de Blaye              |         263.5 |          289.85 |      26.35
 Sir Rodney's Marmalade     |            81 |           89.10 |       8.10
 Carnarvon Tigers           |          62.5 |           68.75 |       6.25
 Raclette Courdavault       |            55 |           60.50 |       5.50
 Manjimup Dried Apples      |            53 |           58.30 |       5.30
 Tarte au sucre             |    49.2999992 |           54.23 |       4.93
 Ipoh Coffee                |            46 |           50.60 |       4.60
 Schoggi Schokolade         |    43.9000015 |           48.29 |       4.39
 Vegie-spread               |    43.9000015 |           48.29 |       4.39
 Northwoods Cranberry Sauce |            40 |           44.00 |       4.00
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. CTE precios_actuales]   -> Filtra products WHERE discontinued = 0 (69 productos activos).
[2. CTE precios_simulados]  -> Aplica proyección escalar de incremento (+10%).
[3. CONSULTA PRINCIPAL]
  - [1. FROM / JOIN]        -> Une ambos CTEs en memoria sobre product_id.
  - [8. SELECT]             -> Calcula la resta aritmética de diferencia.
  - [11. ORDER BY]          -> Top-N HeapSort por diferencia DESC.
  - [12. LIMIT]             -> Entrega los 10 artículos de mayor impacto.
========================================================================================
```

**Análisis de Mantenibilidad:**
- Los CTEs encadenados (*Chained CTEs*) permiten descomponer simulaciones complejas en pasos declarativos legibles, facilitando pruebas unitarias de cada bloque antes de consolidar el modelo financiero final.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Calcula todo en un solo bloque con fórmulas repetidas y poco legibles.
- **Mid / Senior:** Estructura CTEs encadenados modulares, aplica redondeos de moneda y asegura un código autodocumentado y testeable.

</details>

---
"""

print("Section 4-6 loaded.")
