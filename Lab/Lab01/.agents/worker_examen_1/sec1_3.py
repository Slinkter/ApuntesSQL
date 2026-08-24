# -*- coding: utf-8 -*-
"""
Sections 1, 2, 3 (Questions 1 to 13) for 4.examen_entrevista.md
"""

sec1_3_text = """## Sección 1: Filtro, Proyección y Orden Lógico Básico (4 preguntas)

### Pregunta 1 - Nivel: Junior

**Contexto de Negocio:** El Director Comercial para la región EMEA necesita lanzar una campaña estratégica dirigida a clientes corporativos en países europeos clave (Reino Unido, Alemania, Francia, España e Italia). El equipo de marketing exige un listado ordenado jerárquicamente por país y nombre de empresa para coordinar las asignaciones territoriales de los ejecutivos de cuenta.

**Enunciado:** Obtener el nombre de la empresa (`company_name`), nombre del contacto (`contact_name`), cargo del contacto (`contact_title`) y país (`country`) de todos los clientes ubicados en `'UK'`, `'Germany'`, `'France'`, `'Spain'` e `'Italy'`. Ordenar el resultado alfabéticamente por país y, dentro de cada país, por el nombre de la empresa.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Filtrar el universo de clientes a 5 países estratégicos de Europa.
2. **Entidad & Grano:** Tabla `customers` (grano: 1 fila por empresa cliente).
3. **Filtro Temprano (`WHERE`):** Condición de pertenencia en conjunto `country IN (...)`.
4. **Transformaciones:** Ninguna requerida; proyección directa de 4 atributos.
5. **Entrega Ejecutiva (`ORDER BY`):** Ordenamiento compuesto ascendente `(country, company_name)`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    company_name,
    contact_name,
    contact_title,
    country
FROM customers
WHERE country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
ORDER BY country, company_name;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
             company_name             |    contact_name     |     contact_title     | country 
--------------------------------------+---------------------+-----------------------+---------
 Blondesddsl père et fils             | Frédérique Citeaux  | Marketing Manager     | France
 Bon app'                             | Laurence Lebihan    | Owner                 | France
 Du monde entier                      | Janine Labrune      | Owner                 | France
 Folies gourmandes                    | Martine Rancé       | Assistant Sales Agent | France
 France restauration                  | Carine Schmitt      | Marketing Manager     | France
 La corne d'abondance                 | Daniel Tonini       | Sales Representative  | France
 La maison d'Asie                     | Annette Roulet      | Sales Manager         | France
 Paris spécialités                    | Marie Bertrand      | Owner                 | France
 Spécialités du monde                 | Dominique Perrier   | Marketing Manager     | France
 Victuailles en stock                 | Mary Saveley        | Sales Agent           | France
 Vins et alcools Chevalier            | Paul Henriot        | Accounting Manager    | France
 Alfreds Futterkiste                  | Maria Anders        | Sales Representative  | Germany
 Blauer See Delikatessen              | Hanna Moos          | Sales Representative  | Germany
 Die Wandernde Kuh                    | Rita Müller         | Sales Representative  | Germany
 Drachenblut Delikatessen             | Sven Ottlieb        | Order Administrator   | Germany
 Frankenversand                       | Peter Franken       | Marketing Manager     | Germany
 Königlich Essen                      | Philip Cramer       | Sales Associate       | Germany
 Lehmanns Marktstand                  | Renate Messner      | Sales Representative  | Germany
 Morgenstern Gesundkost               | Alexander Feuer     | Marketing Assistant   | Germany
 Ottilies Käseladen                   | Henriette Pfalzheim | Owner                 | Germany
 QUICK-Stop                           | Horst Kloss         | Accounting Manager    | Germany
 Toms Spezialitäten                   | Karin Josephs       | Marketing Manager     | Germany
 Franchi S.p.A.                       | Paolo Accorti       | Sales Representative  | Italy
 Magazzini Alimentari Riuniti         | Giovanni Rovelli    | Marketing Manager     | Italy
 Reggiani Caseifici                   | Maurizio Moroni     | Sales Associate       | Italy
 Bólido Comidas preparadas            | Martín Sommer       | Owner                 | Spain
 FISSA Fabrica Inter. Salchichas S.A. | Diego Roel          | Accounting Manager    | Spain
 Galería del gastrónomo               | Eduardo Saavedra    | Marketing Manager     | Spain
 Godos Cocina Típica                  | José Pedro Freyre   | Sales Manager         | Spain
 Romero y tomillo                     | Alejandra Camino    | Accounting Manager    | Spain
 Around the Horn                      | Thomas Hardy        | Sales Representative  | UK
 B's Beverages                        | Victoria Ashworth   | Sales Representative  | UK
 Consolidated Holdings                | Elizabeth Brown     | Sales Representative  | UK
 Eastern Connection                   | Ann Devon           | Sales Agent           | UK
 Island Trading                       | Helen Bennett       | Marketing Manager     | UK
 North/South                          | Simon Crowther      | Sales Associate       | UK
 Seven Seas Imports                   | Hari Kumar          | Sales Manager         | UK
(37 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Accede a la relación 'customers' (91 tuplas físicas en disco).
[4. WHERE]      -> Evalúa la condición booleana 'country IN (...)'.
                   En PostgreSQL, esto se transforma internamente en:
                   country = ANY(ARRAY['UK', 'Germany', 'France', 'Spain', 'Italy'])
                   Descarta 54 clientes (USA, Brasil, México, etc.) -> Conserva 37 tuplas.
[8. SELECT]     -> Proyecta únicamente las 4 columnas solicitadas.
[11. ORDER BY]  -> Ejecuta Quicksort / Top-N Sort en memoria por (country ASC, company_name ASC).
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Complejidad Temporal:** $O(N + k \log k)$, donde $N=91$ filas escaneadas y $k=37$ filas ordenadas.
- **Complejidad Espacial:** $O(k)$ en `work_mem` para el buffer de ordenamiento.
- **¿Por qué `IN (...)` y no múltiples `OR`?** El planificador de PostgreSQL reescribe la lista de literales `IN (...)` como una comparación de array `ScalarArrayOpExpr` (`= ANY`), lo que permite utilizar un `Bitmap Index Scan` si existiese un índice B-Tree en `country`.

**⚠️ Trampas Típicas de Entrevista:**
- Intentar usar alias de `SELECT` en la cláusula `WHERE` (falla porque `WHERE` se evalúa en el Paso 4 y `SELECT` en el Paso 8).
- Comparaciones sensibles a mayúsculas: `country IN ('uk', 'germany')` retornará 0 filas porque los datos están almacenados en mayúsculas/minúsculas canónicas.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe `WHERE country = 'UK' OR country = 'Germany'...` de forma verbosa pero correcta.
- **Mid:** Usa `country IN (...)` con sintaxis limpia y `ORDER BY country, company_name`.
- **Senior / Lead:** Justifica el costo de ordenamiento en memoria, menciona el operador interno `= ANY(ARRAY[...])` y propone un índice B-Tree en `country`.

> 🛠️ **Nota de Ingeniería & Producción:** En tablas con millones de registros, un índice `CREATE INDEX idx_customers_country_covering ON customers(country) INCLUDE (company_name, contact_name, contact_title);` permite un **Index-Only Scan**, respondiendo la consulta directamente desde el árbol B-Tree sin tocar las páginas Heap de la tabla.

</details>

---

### Pregunta 2 - Nivel: Junior

**Contexto de Negocio:** El equipo de operaciones comerciales necesita auditar la oferta de productos de alto margen que se encuentran vigentes en el catálogo. Se requiere excluir inmediatamente todos los productos descontinuados para no generar ofertas de inventario inexistente a clientes premium.

**Enunciado:** Listar el nombre del producto (`product_name`), precio unitario (`unit_price`) y unidades en stock (`units_in_stock`) de todos los productos cuyo precio unitario sea estrictamente superior a $20 y que NO estén descontinuados (`discontinued = 0`). Ordenar el resultado del producto más costoso al más económico.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Identificar catálogo activo de alto valor comercial.
2. **Entidad & Grano:** Tabla `products` (grano: 1 fila por producto).
3. **Filtro Temprano (`WHERE`):** Predicado compuesto con conjunción lógica `unit_price > 20 AND discontinued = 0`.
4. **Entrega Ejecutiva (`ORDER BY`):** Ordenamiento descendente `unit_price DESC`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    product_name,
    unit_price,
    units_in_stock
FROM products
WHERE unit_price > 20
  AND discontinued = 0
ORDER BY unit_price DESC;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
           product_name           | unit_price | units_in_stock 
----------------------------------+------------+----------------
 Côte de Blaye                    |      263.5 |             17
 Sir Rodney's Marmalade           |         81 |             40
 Carnarvon Tigers                 |       62.5 |             42
 Raclette Courdavault             |         55 |             79
 Manjimup Dried Apples            |         53 |             20
 Tarte au sucre                   |       49.3 |             17
 Ipoh Coffee                      |         46 |             17
 Vegie-spread                     |       43.9 |             24
 Schoggi Schokolade               |       43.9 |             49
 Northwoods Cranberry Sauce       |         40 |              6
 Queso Manchego La Pastora        |         38 |             86
 Gnocchi di nonna Alice           |         38 |             21
 Gudbrandsdalsost                 |         36 |             26
 Mozzarella di Giovanni           |       34.8 |             14
 Camembert Pierrot                |         34 |             19
 Wimmers gute Semmelknödel        |      33.25 |             22
 Mascarpone Fabioli               |         32 |              9
 Gumbär Gummibärchen              |      31.23 |             15
 Ikura                            |         31 |             31
 Uncle Bob's Organic Dried Pears  |         30 |             15
 Sirop d'érable                   |       28.5 |            113
 Gravad lax                       |         26 |             11
 Nord-Ost Matjeshering            |      25.89 |             10
 Grandma's Boysenberry Spread     |         25 |            120
 Pâté chinois                     |         24 |            115
 Tofu                             |      23.25 |             35
 Chef Anton's Cajun Seasoning     |         22 |             53
 Flotemysost                      |       21.5 |             26
 Louisiana Fiery Hot Pepper Sauce |      21.05 |             76
 Gustaf's Knäckebröd              |         21 |            104
 Queso Cabrales                   |         21 |             22
(31 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Accede a la tabla 'products' (77 tuplas en Heap).
[4. WHERE]      -> Aplica predicado compuesto: (unit_price > 20) AND (discontinued = 0).
                   PostgreSQL aplica evaluación en cortocircuito (Short-Circuit Evaluation).
                   De 77 productos, 31 cumplen ambas condiciones simultáneamente.
[8. SELECT]     -> Proyecta product_name, unit_price y units_in_stock.
[11. ORDER BY]  -> Ordena el subconjunto por unit_price DESC.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Complejidad Temporal:** $O(N + k \log k)$, con $N=77$ y $k=31$.
- **Tipo de Dato:** En el DDL canónico de Northwind, `discontinued` es de tipo `INTEGER NOT NULL` (`0` = activo, `1` = descontinuado), no un tipo `BOOLEAN`.

**⚠️ Trampas Típicas de Entrevista:**
- Asumir que `discontinued` es booleano y escribir `WHERE NOT discontinued` (en PostgreSQL generará `ERROR: argument of NOT must be type boolean, not type integer`).
- Usar `discontinued <> 1` en lugar de `discontinued = 0` cuando existen valores NULL potenciales (no aplica aquí por `NOT NULL`, pero es una buena práctica de diseño).

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe la consulta con `discontinued = 0` y `ORDER BY unit_price DESC`.
- **Mid:** Identifica el tipo de dato entero de `discontinued` y asegura la condición en cortocircuito.
- **Senior / Lead:** Diseña un **Índice Parcial** (`Partial Index`) para optimizar consultas frecuentes sobre productos activos.

> 🛠️ **Nota de Ingeniería & Producción:** Para catálogos con millones de productos donde solo un 5% está descontinuado o activo, un índice parcial es la solución óptima:
> ```sql
> CREATE INDEX idx_products_active_price ON products(unit_price DESC) WHERE discontinued = 0;
> ```
> Este índice ocupará una fracción diminuta de RAM y resolverá tanto el filtro como el ordenamiento (`Index Scan`) sin requerir ordenamiento en memoria.

</details>

---

### Pregunta 3 - Nivel: Junior

**Contexto de Negocio:** La gerencia de cadena de suministro (*Supply Chain*) está auditando los costos logísticos para renegociar contratos con empresas de transporte de carga pesada. Requieren identificar de forma inmediata los 10 pedidos con el costo de flete más oneroso de la historia de la compañía, asegurando que si existen pedidos con fletes no registrados (`NULL`), estos no alteren los primeros lugares del ranking.

**Enunciado:** Mostrar el ID del pedido (`order_id`), nombre del destinatario (`ship_name`), costo del flete (`freight`) y país de destino (`ship_country`) de los 10 pedidos con mayor costo de flete. Garantizar que cualquier valor nulo quede posicionado al final de la ordenación (`NULLS LAST`).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Ranking Top 10 de órdenes por costo de flete.
2. **Entidad & Grano:** Tabla `orders` (grano: 1 fila por pedido).
3. **Entrega Ejecutiva (`ORDER BY` + `LIMIT`):** Ordenamiento descendente con cláusula explícita de nulos `ORDER BY freight DESC NULLS LAST LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    order_id,
    ship_name,
    freight,
    ship_country
FROM orders
ORDER BY freight DESC NULLS LAST
LIMIT 10;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 order_id |         ship_name          |  freight   | ship_country 
----------+----------------------------+------------+--------------
    10540 | QUICK-Stop                 | 1007.64001 | Germany
    10372 | Queen Cozinha              | 890.780029 | Brazil
    11030 | Save-a-lot Markets         |     830.75 | USA
    10691 | QUICK-Stop                 | 810.049988 | Germany
    10514 | Ernst Handel               | 789.950012 | Austria
    11017 | Ernst Handel               |  754.26001 | Austria
    10816 | Great Lakes Food Market    | 719.780029 | USA
    10479 | Rattlesnake Canyon Grocery | 708.950012 | USA
    10983 | Save-a-lot Markets         | 657.539978 | USA
    11032 | White Clover Markets       | 606.190002 | USA
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga la tabla 'orders' (830 registros).
[8. SELECT]     -> Proyecta order_id, ship_name, freight y ship_country.
[11. ORDER BY]  -> Top-N HeapSort: En lugar de ordenar los 830 registros completos con QuickSort,
                   PostgreSQL mantiene un Min-Heap acotado de tamaño 10 en memoria (work_mem).
                   Inserta y descarta elementos en tiempo O(N log K).
[12. LIMIT]     -> Entrega exactamente las 10 tuplas raíz del Heap.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Complejidad Temporal:** $O(N \log K)$ donde $N=830$ y $K=10$, reduciendo drásticamente el costo de un $O(N \log N)$ completo.
- **Semántica de NULLS:** En el estándar SQL y en PostgreSQL por defecto:
  - `ORDER BY col ASC` asume `NULLS LAST` (nulos al final).
  - `ORDER BY col DESC` asume `NULLS FIRST` (¡nulos al inicio!).
  - Por tanto, especificar explícitamente `NULLS LAST` es imperativo en rankings descendentes para evitar que datos faltantes ocupen el Top 1.

**⚠️ Trampas Típicas de Entrevista:**
- Omitir `NULLS LAST` en ordenamientos descendentes en motores donde `NULL` es considerado el valor más alto posible (PostgreSQL/Oracle).

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe `ORDER BY freight DESC LIMIT 10` sin considerar el comportamiento de nulos.
- **Mid:** Agrega `NULLS LAST` y justifica por qué PostgreSQL posiciona los nulos al principio por defecto en `DESC`.
- **Senior / Lead:** Explica el funcionamiento interno del nodo **Top-N HeapSort** en `EXPLAIN` y diseña el índice B-Tree descendente complementario.

> 🛠️ **Nota de Ingeniería & Producción:** Para soportar paginación o rankings de alta velocidad en tablas de millones de pedidos:
> ```sql
> CREATE INDEX idx_orders_freight_desc ON orders(freight DESC NULLS LAST);
> ```
> Esto permite que el planificador realice un `Limit (cost=0.28..1.15)` con un `Index Scan` hacia atrás, consumiendo tiempo de CPU casi instantáneo ($0.03\text{ ms}$).

</details>

---

### Pregunta 4 - Nivel: Junior

**Contexto de Negocio:** La división de Recursos Humanos está actualizando el directorio corporativo de dependencias directas. Se requiere listar a todos los empleados subordinados que reportan formalmente a un supervisor o gerente, excluyendo al Director General / Presidente (quien es la cúspide del organigrama y no reporta a nadie).

**Enunciado:** Listar el nombre completo del empleado (`nombre_completo`, concatenando nombre y apellido), su cargo (`title`), su ciudad (`city`) y el ID del supervisor al que reporta (`reports_to`). Filtrar únicamente aquellos colaboradores que tengan un supervisor asignado (`reports_to IS NOT NULL`). Ordenar por el ID del supervisor y luego por el apellido del empleado.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Directorio de personal operativo con línea de mando directa.
2. **Entidad & Grano:** Tabla `employees` (grano: 1 fila por empleado).
3. **Filtro Temprano (`WHERE`):** Exclusión de la raíz jerárquica mediante `reports_to IS NOT NULL`.
4. **Transformaciones:** Concatenación de cadenas estándar `first_name || ' ' || last_name`.
5. **Entrega Ejecutiva (`ORDER BY`):** Ordenamiento por supervisor y apellido `reports_to, last_name`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title,
    city,
    reports_to
FROM employees
WHERE reports_to IS NOT NULL
ORDER BY reports_to, last_name;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 nombre_completo  |          title           |   city   | reports_to 
------------------+--------------------------+----------+------------
 Steven Buchanan  | Sales Manager            | London   |          2
 Laura Callahan   | Inside Sales Coordinator | Seattle  |          2
 Nancy Davolio    | Sales Representative     | Seattle  |          2
 Janet Leverling  | Sales Representative     | Kirkland |          2
 Margaret Peacock | Sales Representative     | Redmond  |          2
 Anne Dodsworth   | Sales Representative     | London   |          5
 Robert King      | Sales Representative     | London   |          5
 Michael Suyama   | Sales Representative     | London   |          5
(8 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga la tabla 'employees' (9 empleados en total).
[4. WHERE]      -> Evalúa predicado booleano: reports_to IS NOT NULL.
                   Andrew Fuller (employee_id=2, reports_to=NULL) evalúa como FALSE y se descarta.
                   Conserva 8 empleados subordinados.
[8. SELECT]     -> Evalúa la concatenación escalar first_name || ' ' || last_name y proyecta columnas.
[11. ORDER BY]  -> Ordena por reports_to ASC, last_name ASC.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Lógica Trivalente (3-Valued Logic):** En SQL, cualquier comparación directa con NULL usando operadores relacionales (`reports_to != NULL` o `reports_to = NULL`) evalúa como **UNKNOWN** (desconocido). La cláusula `WHERE` solo conserva tuplas donde el predicado evalúa estrictamente como **TRUE**. Por ende, `!= NULL` filtrará erróneamente todas las filas, devolviendo un conjunto vacío.
- **Concatenación:** El operador estándar ANSI/PostgreSQL es `||`. Si cualquiera de las partes fuese NULL, el resultado de `||` sería NULL. Para concatenaciones con posibles nulos, se utiliza `CONCAT()` o `CONCAT_WS()`.

**⚠️ Trampas Típicas de Entrevista:**
- Escribir `WHERE reports_to != NULL` o `WHERE reports_to <> NULL`. Este es el detector #1 de candidatos novatos en entrevistas técnicas de SQL.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Usa `IS NOT NULL` correctamente y concatena con `||`.
- **Mid:** Explica la lógica trivalente de SQL (`TRUE`, `FALSE`, `UNKNOWN`) y por qué `NULL = NULL` no es verdadero.
- **Senior / Lead:** Discute el impacto de índices en columnas con alta presencia de NULLs y el uso de `WITH RECURSIVE` para jerarquías multi-nivel de N profundidades.

</details>

---

## Sección 2: Agregaciones, Agrupamiento y Filtros de Grupo (4 preguntas)

### Pregunta 5 - Nivel: Mid

**Contexto de Negocio:** El Vicepresidente de Finanzas requiere evaluar la rentabilidad bruta por categoría de producto para reasignar el presupuesto de compras del próximo trimestre fiscal. Para evitar analizar categorías marginales, solo se deben incluir aquellas cuya facturación neta total supere los $10,000 USD.

**Enunciado:** Calcular el identificador de categoría (`category_id`) y el ingreso neto total acumulado (considerando `cantidad * precio_unitario * (1 - descuento)`). Filtrar únicamente aquellas categorías con ingreso total superior a $10,000 USD. Ordenar de mayor a menor facturación neta.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Facturación neta consolidada por categoría con umbral mínimo de corte.
2. **Entidad & Grano:** Tablas `order_details` cruzada con `products` (grano final: 1 fila por `category_id`).
3. **Cruce de Fuentes:** `order_details` $\bowtie$ `products` sobre `product_id`.
4. **Agregación & Agrupamiento:** `GROUP BY p.category_id` acumulando con `SUM()`.
5. **Filtro de Grupo (`HAVING`):** Filtrar grupos con ingreso neto $> 10000$.
6. **Entrega Ejecutiva (`ORDER BY`):** Ordenamiento descendente por ingreso total.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    p.category_id,
    SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ingreso_total
FROM order_details od
INNER JOIN products p ON od.product_id = p.product_id
GROUP BY p.category_id
HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 10000
ORDER BY ingreso_total DESC;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 category_id |       ingreso_total       
-------------+---------------------------
           1 |  267868.17975060142003768
           4 |  234507.28452857984016176
           3 | 167357.225438965626070308
           6 | 163022.360348499217401332
           8 | 131261.736550894350451328
           2 |  106047.08459681187133608
           7 |   99984.58007876718934490
           5 |   95744.58735707935501842
(8 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga 'order_details' (2,155 tuplas) y 'products' (77 tuplas).
[2. ON / JOIN]  -> Hash Join por 'product_id'. Empareja cada línea de pedido con su categoría.
[5. GROUP BY]   -> HashAggregate: Construye tabla hash en memoria indexada por 'p.category_id'.
                   Por cada tupla que ingresa al grupo, acumula la expresión del subtotal neto.
[6. HAVING]     -> Evalúa la condición agregada: SUM(subtotal) > 10000 sobre cada cubeta agrupada.
                   Las 8 categorías superan el umbral en Northwind.
[8. SELECT]     -> Proyecta category_id y asigna el alias 'ingreso_total'.
[11. ORDER BY]  -> Ordena los 8 registros agregados por ingreso_total DESC.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Complejidad Temporal:** $O(N + M + G \log G)$, donde $N=2155$ líneas de orden, $M=77$ productos y $G=8$ categorías.
- **Diferencia Fundamental entre WHERE y HAVING:**
  - `WHERE` (Paso 4): Filtra filas individuales ANTES de agrupar. No puede evaluar funciones de agregación.
  - `HAVING` (Paso 6): Filtra grupos consolidados DESPUÉS de ejecutar la agregación.

**⚠️ Trampas Típicas de Entrevista:**
- Intentar colocar la condición de suma en la cláusula `WHERE`: `WHERE SUM(...) > 10000` (produce `ERROR: aggregate functions are not allowed in WHERE`).
- Intentar usar el alias de `SELECT` en la cláusula `HAVING` en motores estándar SQL (falla en la mayoría de DBMS porque `HAVING` ocurre en el Paso 6 y `SELECT` en el Paso 8).

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Entiende la sintaxis básica pero confunde `WHERE` y `HAVING`.
- **Mid:** Utiliza `HAVING` con la expresión completa de agregación y calcula el descuento correctamente.
- **Senior / Lead:** Explica la diferencia entre `HashAggregate` (cuando la tabla hash cabe en `work_mem`) y `GroupAggregate` (cuando requiere datos previamente ordenados por la clave de grupo).

</details>

---

### Pregunta 6 - Nivel: Mid

**Contexto de Negocio:** La dirección de operaciones está evaluando el desempeño de los transportistas contratados (*Shippers*) para identificar a aquellos que gestionan envíos de alto porte logístico. Se requiere calcular el flete promedio por orden para cada transportista y filtrar solo aquellos con un promedio superior a $50 USD.

**Enunciado:** Por cada empresa transportista, mostrar su nombre (`transportista`), el conteo total de pedidos transportados (`total_pedidos`) y el flete promedio redondeado a 2 decimales (`flete_promedio`). Filtrar solo aquellas empresas con flete promedio estrictamente superior a $50 USD. Ordenar por flete promedio descendente.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Métricas de volumen y costo promedio por transportista.
2. **Entidad & Grano:** Tabla `orders` vinculada a `shippers` (grano final: 1 fila por empresa transportista).
3. **Cruce de Fuentes:** `orders o` $\bowtie$ `shippers s` sobre `o.ship_via = s.shipper_id`.
4. **Agregación & Agrupamiento:** `GROUP BY s.company_name` calculando `COUNT(order_id)` y `AVG(freight)`.
5. **Filtro de Grupo:** `HAVING AVG(o.freight) > 50`.
6. **Entrega Ejecutiva:** Casteo explícito a `::numeric` para formateo seguro con `ROUND()`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    s.company_name AS transportista,
    COUNT(o.order_id) AS total_pedidos,
    ROUND(AVG(o.freight)::numeric, 2) AS flete_promedio
FROM orders o
INNER JOIN shippers s ON o.ship_via = s.shipper_id
GROUP BY s.company_name
HAVING AVG(o.freight) > 50
ORDER BY flete_promedio DESC;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
  transportista   | total_pedidos | flete_promedio 
------------------+---------------+----------------
 United Package   |           326 |          86.64
 Federal Shipping |           255 |          80.44
 Speedy Express   |           249 |          65.00
(3 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM / JOIN] -> Hash Join entre 'orders' (830 filas) y 'shippers' (3 transportistas).
[5. GROUP BY]    -> Agrupa por s.company_name, calculando el acumulador COUNT y SUM(freight)/COUNT(freight).
[6. HAVING]      -> Evalúa AVG(o.freight) > 50. Los 3 transportistas cumplen el predicado.
[8. SELECT]      -> Aplica ROUND(..., 2) con casteo ::numeric y proyecta alias.
[11. ORDER BY]   -> Ordena los 3 registros por flete_promedio DESC.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Casteo a Numeric:** En PostgreSQL, la función `ROUND(double precision, integer)` no existe directamente en el catálogo estándar sin extensiones. La función nativa requiere `ROUND(numeric, integer)`. Por ello, castear `AVG(freight)::numeric` garantiza portabilidad y evita errores de tipo en tiempo de ejecución.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Agrupa por transportista pero olvida el casteo a numeric o escribe filtros incorrectos.
- **Mid:** Escribe la consulta exacta con `HAVING` y `ROUND(::numeric, 2)`.
- **Senior / Lead:** Discute la diferencia entre `COUNT(*)` y `COUNT(o.order_id)` en presencia de outer joins y evalúa la selectividad de los índices en `orders(ship_via)`.

</details>

---

### Pregunta 7 - Nivel: Mid

**Contexto de Negocio:** El área de control de inventarios (*Warehouse Management*) necesita un panel consolidado de control de stock por categoría. El informe debe totalizar productos, identificar cuántos artículos tienen inventario crítico (< 20 unidades), calcular el precio medio de lista y señalar el producto más costoso de cada familia de productos, descartando categorías con menos de 3 ítems registrados.

**Enunciado:** Por cada categoría, obtener su nombre (`category_name`), total de productos registrados (`total_productos`), cantidad de productos con stock bajo (`stock_bajo`, unidades en stock menor a 20 utilizando la cláusula nativa `FILTER`), precio unitario promedio redondeado a 2 decimales (`precio_promedio`) y el precio máximo (`precio_maximo`). Mostrar únicamente categorías que contengan al menos 3 productos (`COUNT >= 3`), ordenadas por el total de productos de forma descendente.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Métricas multi-dimensionales de catálogo e inventario crítico por categoría.
2. **Entidad & Grano:** `products` $\bowtie$ `categories` (grano final: 1 fila por categoría).
3. **Agregación Condicional:** Uso de la cláusula estándar `FILTER (WHERE ...)` para evitar subconsultas.
4. **Filtro de Grupo:** `HAVING COUNT(p.product_id) >= 3`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 category_name  | total_productos | stock_bajo | precio_promedio | precio_maximo 
----------------+-----------------+------------+-----------------+---------------
 Confections    |              13 |          6 |           25.16 |            81
 Condiments     |              12 |          4 |           22.85 |    43.9000015
 Beverages      |              12 |          4 |           37.98 |         263.5
 Seafood        |              12 |          3 |           20.68 |          62.5
 Dairy Products |              10 |          4 |           28.73 |            55
 Grains/Cereals |               7 |          0 |           20.25 |            38
 Meat/Poultry   |               6 |          3 |           54.01 |    123.790001
 Produce        |               5 |          2 |           32.37 |            53
(8 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM / JOIN] -> Une 77 productos con 8 categorías por 'category_id'.
[5. GROUP BY]    -> HashAggregate por c.category_name.
                    Durante el ciclo de agregación, la cláusula FILTER evalúa el predicado
                    'units_in_stock < 20' en memoria antes de incrementar el acumulador de stock_bajo.
[6. HAVING]      -> Valida COUNT(product_id) >= 3. Todas las 8 categorías pasan.
[8. SELECT]      -> Proyecta métricas consolidadas y redondea precio promedio.
[11. ORDER BY]   -> Ordena por total_productos DESC.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Cláusula FILTER (ISO:SQL 2003):** PostgreSQL implementa `AGG_FUNC(...) FILTER (WHERE condicion)` de forma nativa en el motor C. Es semánticamente superior y computacionalmente más rápida que la construcción tradicional `SUM(CASE WHEN units_in_stock < 20 THEN 1 ELSE 0 END)`, ya que evita saltos condicionales en tiempo de ejecución del intérprete SQL.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Usa `SUM(CASE WHEN ...)` de forma tradicional.
- **Mid / Senior:** Emplea `COUNT(*) FILTER (WHERE ...)` y demuestra dominio del estándar SQL moderno en PostgreSQL.
- **Lead / Architect:** Compara el costo de ejecución en CPU entre `FILTER` y `CASE WHEN`, señalando la limpieza de planes generados por el compilador de consultas.

</details>

---

### Pregunta 8 - Nivel: Mid / Senior

**Contexto de Negocio:** El CFO solicita un análisis de estacionalidad de ingresos del año 1997. Requiere visualizar la facturación neta de cada trimestre y, de forma simultánea, el porcentaje exacto que representó dicho trimestre sobre la facturación global de todo el año, permitiendo identificar trimestres pico y valles operacionales.

**Enunciado:** Construir una consulta modular utilizando una Expresión de Tabla Común (`WITH / CTE`) que calcule el ingreso neto por trimestre para el año 1997. En la consulta principal, calcular la participación porcentual de cada trimestre respecto al total anual mediante una función de ventana global vacía (`SUM(...) OVER ()`), formateando las métricas a 2 decimales y ordenando cronológicamente por trimestre.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Desglose estacional Q1-Q4 con participación porcentual sobre el total anual.
2. **Entidad & Grano:** `orders` $\bowtie$ `order_details` filtrados al año 1997 (grano del CTE: 1 fila por trimestre).
3. **Métrica Global:** Función de ventana `SUM(ingreso) OVER ()` para obtener el totalizador anual sin requerir un auto-cruce (*Self-Join*) ni subconsultas correlacionadas.
4. **Entrega Ejecutiva:** Formato `'Q' || trimestre` y porcentajes a 2 decimales.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 trimestre | ingreso_total | porcentaje 
-----------+---------------+------------
 Q1        |     138288.93 |      22.41
 Q2        |     143177.04 |      23.20
 Q3        |     153937.77 |      24.95
 Q4        |     181681.46 |      29.44
(4 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[FASE 1: CTE ingresos_trimestre]
  - [1. FROM / JOIN] -> Cruza orders (408 pedidos en 1997) con order_details.
  - [4. WHERE]       -> Filtra EXTRACT(YEAR FROM order_date) = 1997.
  - [5. GROUP BY]    -> Agrupa en 4 cubetas (trimestres 1, 2, 3, 4).

[FASE 2: CONSULTA PRINCIPAL]
  - [1. FROM]        -> Carga las 4 tuplas resultantes del CTE.
  - [7. WINDOW]      -> Evalúa SUM(ingreso) OVER (): Calcula la suma global ($617,085.20)
                        en una sola pasada de ventana sin partición.
  - [8. SELECT]      -> Calcula la división escalar (ingreso / total_global * 100).
  - [11. ORDER BY]   -> Ordena por trimestre cronológico.
========================================================================================
```

**Análisis de Complejidad y Motor:**
- **Eficiencia de Window Functions:** Sin funciones de ventana, calcular el porcentaje requeriría una subconsulta escalar en el `SELECT` o un `CROSS JOIN` con una tabla agregada, lo que obligaría al motor a escanear dos veces las tablas base. Con `OVER ()`, el costo es $O(G)$ sobre los grupos ya consolidados.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Resuelve con subconsultas repetitivas o auto-joins costosos.
- **Mid:** Usa CTE pero lucha con el cálculo del porcentaje total.
- **Senior / Lead:** Usa CTE + `OVER ()` de forma elegante, justifica la evaluación en el Paso 7 del motor y menciona la optimización de inlining de CTEs en PostgreSQL 12+.

</details>

---

## Sección 3: Relaciones, JOINs y Anti-Patrones Relacionales (5 preguntas)

### Pregunta 9 - Nivel: Mid

**Contexto de Negocio:** El área de auditoría de cumplimiento comercial requiere una vista desnormalizada de control de pedidos para el ejercicio fiscal 1997. El reporte debe cruzar la información transaccional de la orden con los datos maestros del cliente, el empleado responsable de la cuenta y la empresa de transporte designada.

**Enunciado:** Mostrar el ID del pedido (`order_id`), fecha de emisión (`order_date`), nombre de la empresa cliente (`cliente`), nombre completo del empleado responsable (`empleado`, nombre y apellido concatenados) y la compañía transportista (`transportista`). Incluir únicamente órdenes del año 1997, ordenadas cronológicamente de forma descendente (mostrar los primeros 10 registros).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Sábana operativa multi-dimensional de transacciones.
2. **Entidad Central:** Tabla `orders` como hecho central.
3. **Cruces de Fuentes:** 3 dimensiones vinculadas: `customers` (cliente), `employees` (vendedor) y `shippers` (transportista).
4. **Filtro Temprano:** Año 1997 sobre la fecha de orden.
5. **Entrega Ejecutiva:** Ordenamiento temporal descendente con límite Top 10.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 order_id | order_date |          cliente          |     empleado     |  transportista   
----------+------------+---------------------------+------------------+------------------
    10807 | 1997-12-31 | Franchi S.p.A.            | Margaret Peacock | Speedy Express
    10806 | 1997-12-31 | Victuailles en stock      | Janet Leverling  | United Package
    10804 | 1997-12-30 | Seven Seas Imports        | Michael Suyama   | United Package
    10805 | 1997-12-30 | The Big Cheese            | Andrew Fuller    | Federal Shipping
    10803 | 1997-12-30 | Wellington Importadora    | Margaret Peacock | Speedy Express
    10801 | 1997-12-29 | Bólido Comidas preparadas | Margaret Peacock | United Package
    10802 | 1997-12-29 | Simons bistro             | Margaret Peacock | United Package
    10798 | 1997-12-26 | Island Trading            | Andrew Fuller    | Speedy Express
    10799 | 1997-12-26 | Königlich Essen           | Anne Dodsworth   | Federal Shipping
    10800 | 1997-12-26 | Seven Seas Imports        | Nancy Davolio    | Federal Shipping
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM / JOIN] -> Árbol de Cruces (Join Tree):
                    1. orders (408 filas filtradas) Hash Join customers por customer_id.
                    2. Resultado intermedio Hash Join employees por employee_id.
                    3. Resultado intermedio Hash Join shippers por ship_via = shipper_id.
[4. WHERE]       -> Filtra tuplas por EXTRACT(YEAR FROM order_date) = 1997.
[8. SELECT]      -> Proyecta columnas enriquecidas y concatena nombre de empleado.
[11. ORDER BY]   -> Top-N HeapSort por order_date DESC.
[12. LIMIT]      -> Entrega las 10 tuplas más recientes.
========================================================================================
```

**Análisis de SARGabilidad:**
- `EXTRACT(YEAR FROM order_date) = 1997` aplica una función sobre la columna, impidiendo el uso directo de un índice B-Tree en `order_date`.
- En producción masiva, es preferible la forma **SARGable** (*Search Argument Able*):
  `WHERE o.order_date >= '1997-01-01' AND o.order_date < '1998-01-01'`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe los joins correctamente pero no optimiza el filtro de fechas.
- **Mid / Senior:** Conoce los algoritmos de Join (`Hash Join` vs `Nested Loop`) y explica el concepto de SARGabilidad en predicados de fecha.

</details>

---

### Pregunta 10 - Nivel: Senior / Lead

**Contexto de Negocio:** La Vicepresidencia de Crecimiento (*Growth*) está estructurando una campaña de re-activación comercial agresiva para cuentas corporativas que fueron registradas en el sistema pero que nunca han concretado una orden de compra en la historia de la compañía. Se requiere aislar estas cuentas mediante el patrón relacional de alto rendimiento **Anti-Join**.

**Enunciado:** Obtener el identificador del cliente (`customer_id`), nombre de la empresa (`company_name`), ciudad (`city`) y país (`country`) de todos los clientes que **NO tengan ningún pedido registrado** en la tabla de órdenes. Implementar obligatoriamente el patrón **Anti-Join** (`LEFT JOIN ... WHERE right_table.pk IS NULL`).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Detección de cuentas inactivas con cero pedidos históricos.
2. **Entidad Base:** `customers` (91 clientes canónicos).
3. **Patrón de Cruce:** `LEFT JOIN orders o ON c.customer_id = o.customer_id`.
4. **Filtro Anti-Join:** `WHERE o.order_id IS NULL` (elimina a todos los clientes que hicieron match).

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    c.customer_id,
    c.company_name,
    c.city,
    c.country
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 customer_id |             company_name             |  city  | country 
-------------+--------------------------------------+--------+---------
 PARIS       | Paris spécialités                    | Paris  | France
 FISSA       | FISSA Fabrica Inter. Salchichas S.A. | Madrid | Spain
(2 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga la tabla 'customers' (91 clientes).
[2. ON]         -> Evalúa c.customer_id = o.customer_id contra 'orders' (830 órdenes).
[3. LEFT JOIN]  -> Preserva los 91 clientes:
                   - 89 clientes hacen match con órdenes -> o.order_id contiene un entero.
                   - 2 clientes (PARIS y FISSA) no tienen órdenes -> o.order_id se rellena con NULL.
[4. WHERE]      -> Filtro Anti-Join: Evalúa 'o.order_id IS NULL'.
                   Descarta los 89 clientes activos -> Conserva exactamente 2 clientes huérfanos.
[8. SELECT]     -> Proyecta customer_id, company_name, city y country.
========================================================================================
```

**Análisis Comparativo de los 3 Patrones de Anti-Join en PostgreSQL:**

| Patrón | Sintaxis SQL | Plan de Ejecución en PostgreSQL | Riesgo de NULLs |
| :--- | :--- | :--- | :--- |
| **1. LEFT JOIN + IS NULL** | `FROM c LEFT JOIN o ON ... WHERE o.id IS NULL` | `Hash Right Anti Join` | Seguro si se prueba la Primary Key. |
| **2. NOT EXISTS** | `WHERE NOT EXISTS (SELECT 1 FROM o WHERE ...)` | `Hash Anti Join` | 100% Seguro y semánticamente óptimo. |
| **3. NOT IN (¡PELIGROSO!)** | `WHERE c.id NOT IN (SELECT customer_id FROM o)` | `Seq Scan + Subplan` | ⚠️ **FATAL:** Si la subconsulta contiene un solo `NULL`, la consulta retorna 0 filas. |

**La Trampa Mortal del `NOT IN` con NULLs:**
En lógica trivalente, `x NOT IN (1, 2, NULL)` se expande a:
`x != 1 AND x != 2 AND x != NULL`.
Dado que `x != NULL` siempre evalúa como **UNKNOWN**, toda la expresión lógica colapsa a **UNKNOWN** (o FALSE en el `WHERE`), destruyendo silenciosamente el resultado de la consulta. Por ello, en entrevistas Senior/Lead, el uso de `NOT IN` sin un filtro explícito `WHERE col IS NOT NULL` es causal de descalificación técnica.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Escribe `NOT IN` sin considerar el riesgo de valores nulos.
- **Mid:** Resuelve con `LEFT JOIN ... IS NULL` obteniendo exactamente las 2 filas canónicas (`PARIS` y `FISSA`).
- **Senior / Lead:** Compara `LEFT JOIN ... IS NULL` contra `NOT EXISTS`, explica el nodo interno `Hash Right Anti Join` del planificador de PostgreSQL y detalla la trampa matemática de la lógica trivalente en `NOT IN`.

> 🛠️ **Nota de Ingeniería & Producción:** El optimizador de PostgreSQL 16 transforma automáticamente tanto `LEFT JOIN ... IS NULL` como `NOT EXISTS` en el mismo nodo físico de bajo costo `Hash Anti Join`, siempre que la columna evaluada en el `WHERE` sea la clave primaria o esté marcada como `NOT NULL`.

</details>

---

### Pregunta 11 - Nivel: Mid

**Contexto de Negocio:** El departamento de compras (*Procurement*) está realizando una auditoría de eficiencia de proveedores (*Suppliers*) para depurar el catálogo maestro. Se requiere identificar si existen proveedores cuyos productos nunca hayan generado una sola venta registrada en las líneas de pedido de la empresa.

**Enunciado:** Listar el nombre del proveedor (`proveedor`), su país (`country`) y la cantidad de productos de su catálogo que nunca han aparecido en ningún pedido (`productos_sin_ventas`). Mostrar únicamente aquellos proveedores que tengan al menos 1 producto sin ventas (`COUNT >= 1`), ordenados de mayor a menor cantidad de productos inactivos.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Identificación de proveedores con catálogo huérfano (sin rotación).
2. **Entidades & Relaciones:** `suppliers s` $\bowtie$ `products p` $\leftouterjoin$ `order_details od`.
3. **Detección de Huérfanos:** `od.product_id IS NULL`.
4. **Agregación & Filtro de Grupo:** `GROUP BY s.company_name, s.country HAVING COUNT(p.product_id) >= 1`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
 proveedor | country | productos_sin_ventas 
-----------+---------+----------------------
(0 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM / JOIN] -> 1. suppliers (29) INNER JOIN products (77): Todos los productos tienen proveedor.
                    2. products (77) LEFT JOIN order_details (2,155).
[4. WHERE]       -> Evalúa 'od.product_id IS NULL'.
                    En el esquema canónico de Northwind, los 77 productos tienen al menos
                    una orden registrada en order_details.
                    Ninguna tupla cumple el predicado IS NULL -> El flujo se reduce a 0 filas.
[5. GROUP BY]    -> No se forman grupos.
[8. SELECT]      -> Entrega conjunto vacío (0 rows).
========================================================================================
```

**Análisis de Validación en Entrevistas:**
- En entrevistas técnicas, los candidatos con poca experiencia suelen entrar en pánico cuando una consulta sintácticamente válida devuelve `(0 rows)` y comienzan a modificar erróneamente la consulta agregando `OR` o cambiando los tipos de join.
- Un candidato de nivel **Senior** valida la integridad del catálogo ejecutando:
  `SELECT COUNT(DISTINCT product_id) FROM order_details;` (resultado: 77), confirmando con seguridad analítica que el resultado esperado es legítimamente 0 filas.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Duda del resultado de 0 filas y asume que su SQL es incorrecto.
- **Mid / Senior:** Explica con aplomo que el resultado de 0 filas refleja la integridad referencial y actividad comercial completa de los 77 productos en el dataset Northwind.

</details>

---

### Pregunta 12 - Nivel: Mid

**Contexto de Negocio:** La Dirección General de la compañía necesita generar una cartografía del organigrama empresarial (*Adjacency List Structure*). El informe debe mostrar la relación jerárquica de cada colaborador con su jefe directo inmediato, garantizando que el ejecutivo de más alto rango (Presidente / Vicepresidente), quien carece de supervisor, aparezca claramente catalogado con el texto descriptivo `"Sin jefe"`.

**Enunciado:** Mostrar el nombre del empleado (`empleado`), su cargo (`cargo_empleado`), el nombre completo de su jefe directo (`jefe`) y el cargo del jefe (`cargo_jefe`). Si el empleado no tiene supervisor (`reports_to IS NULL`), mostrar `'Sin jefe'` en el nombre y `'N/A'` en el cargo del supervisor, utilizando `COALESCE()`. Ordenar por el identificador del empleado (`employee_id`).

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Organigrama de supervisión directa (Self-Referential Join).
2. **Entidad & Grano:** Tabla `employees` cruzada consigo misma (Alias `e` = subordinado, Alias `m` = manager).
3. **Tipo de Cruce:** `LEFT JOIN employees m ON e.reports_to = m.employee_id` (para no perder al Presidente).
4. **Sanitización de Nulos:** `COALESCE(m.first_name || ' ' || m.last_name, 'Sin jefe')`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo_empleado,
    COALESCE(m.first_name || ' ' || m.last_name, 'Sin jefe') AS jefe,
    COALESCE(m.title, 'N/A') AS cargo_jefe
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
     empleado     |      cargo_empleado      |      jefe       |      cargo_jefe       
------------------+--------------------------+-----------------+-----------------------
 Nancy Davolio    | Sales Representative     | Andrew Fuller   | Vice President, Sales
 Andrew Fuller    | Vice President, Sales    | Sin jefe        | N/A
 Janet Leverling  | Sales Representative     | Andrew Fuller   | Vice President, Sales
 Margaret Peacock | Sales Representative     | Andrew Fuller   | Vice President, Sales
 Steven Buchanan  | Sales Manager            | Andrew Fuller   | Vice President, Sales
 Michael Suyama   | Sales Representative     | Steven Buchanan | Sales Manager
 Robert King      | Sales Representative     | Steven Buchanan | Sales Manager
 Laura Callahan   | Inside Sales Coordinator | Andrew Fuller   | Vice President, Sales
 Anne Dodsworth   | Sales Representative     | Steven Buchanan | Sales Manager
(9 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[1. FROM]       -> Carga la instancia 'employees e' (9 empleados).
[2. ON]         -> Cruza e.reports_to con m.employee_id en la segunda instancia 'employees m'.
[3. LEFT JOIN]  -> Preserva los 9 colaboradores:
                   - Para Andrew Fuller (id=2, reports_to=NULL), la tupla derecha 'm' es NULL.
[8. SELECT]     -> COALESCE detecta el NULL en 'm' y sustituye por 'Sin jefe' y 'N/A'.
[11. ORDER BY]  -> Ordena por e.employee_id ASC.
========================================================================================
```

**Análisis de Estructuras Jerárquicas:**
- Esta técnica resuelve relaciones jerárquicas de 1 solo nivel de profundidad ($N=1$).
- Para consultar árboles de decisión o cadenas de mando de profundidad arbitraria ($N \ge 1$), el estándar en PostgreSQL es emplear CTEs Recursivos (`WITH RECURSIVE`).

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Usa `INNER JOIN` perdiendo al empleado principal (Andrew Fuller) y obteniendo 8 filas en lugar de 9.
- **Mid:** Usa `LEFT JOIN` con `COALESCE` de forma impecable.
- **Senior / Lead:** Propone la extensión a `WITH RECURSIVE` para calcular el nivel de profundidad jerárquica (*Hierarchy Level*) y la ruta de reporte (*Breadcrumb Path*).

</details>

---

### Pregunta 13 - Nivel: Senior

**Contexto de Negocio:** El comité ejecutivo de gestión de clientes (*Key Account Management*) necesita un perfil maestro 360 de los clientes más recurrentes de la empresa. Para todas aquellas cuentas corporativas con más de 5 pedidos registrados, se requiere un informe consolidado que detalle su volumen transaccional, el rango temporal de su ciclo de vida (primera y última orden) y el producto unitario de mayor valor que han adquirido a lo largo de su historia.

**Enunciado:** Para todos los clientes con más de 5 pedidos registrados (`COUNT(DISTINCT order_id) > 5`), mostrar el nombre de la empresa (`company_name`), total de pedidos (`total_pedidos`), fecha de la primera orden (`primer_pedido`), fecha de la última orden (`ultimo_pedido`), el nombre del producto más caro que ha comprado (`producto_mas_caro`) y su precio unitario (`precio`). Limitar la salida a los 10 clientes con mayor cantidad de pedidos, ordenados de mayor a menor volumen transaccional.

🧠 **Cómo Pensar como un Analista de Datos:**
1. **Objetivo & KPI:** Perfil integral de clientes de alta recurrencia + producto premium adquirido.
2. **Descomposición Modular:**
   - **CTE 1 (`metricas_cliente`):** Agregación de pedidos (`COUNT`, `MIN`, `MAX`) filtrando con `HAVING COUNT > 5`.
   - **CTE 2 (`producto_mas_caro`):** Aislamiento del producto de mayor precio por cliente usando `DISTINCT ON (customer_id)` ordenado por precio DESC.
3. **Consolidación:** Cruce de ambos CTEs con la tabla maestra de `customers`.
4. **Entrega Ejecutiva:** Ordenamiento por `total_pedidos DESC LIMIT 10`.

<details>
<summary>Solución SQL y Análisis Técnico</summary>

```sql
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
```

#### 📊 Resultado Real de Ejecución en PostgreSQL 16 (AWS EC2 / Northwind Canónico):

```text
         company_name         | total_pedidos | primer_pedido | ultimo_pedido |    producto_mas_caro    |   precio   
------------------------------+---------------+---------------+---------------+-------------------------+------------
 Save-a-lot Markets           |            31 | 1996-10-08    | 1998-05-01    | Thüringer Rostbratwurst | 123.790001
 Ernst Handel                 |            30 | 1996-07-17    | 1998-05-05    | Côte de Blaye           | 210.800003
 QUICK-Stop                   |            28 | 1996-08-05    | 1998-04-14    | Côte de Blaye           |      263.5
 Hungry Owl All-Night Grocers |            19 | 1996-09-05    | 1998-04-30    | Thüringer Rostbratwurst | 123.790001
 Folk och fä HB               |            19 | 1996-07-24    | 1998-04-27    | Thüringer Rostbratwurst | 123.790001
 HILARION-Abastos             |            18 | 1996-07-16    | 1998-04-28    | Raclette Courdavault    |         55
 Berglunds snabbköp           |            18 | 1996-08-12    | 1998-03-04    | Côte de Blaye           |      263.5
 Rattlesnake Canyon Grocery   |            18 | 1996-07-22    | 1998-05-06    | Côte de Blaye           |      263.5
 Bon app'                     |            17 | 1996-10-16    | 1998-05-06    | Manjimup Dried Apples   |         53
 Frankenversand               |            15 | 1996-07-29    | 1998-04-09    | Thüringer Rostbratwurst | 123.790001
(10 rows)
```

#### 🔄 Pipeline Lógico del Motor & Ciclo de Vida (12 Pasos):

```text
========================================================================================
[FASE 1: CTE metricas_cliente]
  - Agrupa 830 órdenes por customer_id -> Filtra HAVING COUNT > 5 (obtiene 49 clientes).
[FASE 2: CTE producto_mas_caro CON DISTINCT ON]
  - Cruza orders con order_details y products.
  - [11. ORDER BY]: Ordena por (customer_id ASC, od.unit_price DESC).
  - [9. DISTINCT ON]: Conserva únicamente la primera tupla de cada cliente (la de mayor precio).
[FASE 3: CONSULTA FINAL]
  - Hash Join de ambos CTEs con 'customers' -> Top-N HeapSort por total_pedidos DESC -> LIMIT 10.
========================================================================================
```

**DISTINCT ON en PostgreSQL vs SQL Estándar:**
- `DISTINCT ON (col1)` es una poderosa cláusula nativa de PostgreSQL que evalúa la unicidad basada exclusivamente en `col1`, conservando la primera fila de acuerdo al criterio de ordenamiento establecido en el `ORDER BY`.
- En SQL estándar ANSI (Oracle, SQL Server, MySQL), la equivalencia se logra mediante `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY unit_price DESC) WHERE rn = 1`.

**🎯 Rúbrica de Evaluación de Entrevista:**
- **Junior:** Intenta resolverlo todo en un solo bloque con JOINs masivos, provocando multiplicación cartesiana de subtotales.
- **Mid:** Usa funciones de ventana o subconsultas derivadas para aislar el producto más caro.
- **Senior / Lead:** Domina la técnica de `DISTINCT ON` en PostgreSQL, diseña una arquitectura con CTEs desacoplados y explica el comportamiento de memoria en el nodo `Unique`.

</details>

---
"""

print("Section 1-3 loaded.")
