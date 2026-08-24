const fs = require('fs');

const b2 = {
  11: {
    enunciado: "El equipo de marketing y catálogo necesita destacar en la portada del catálogo el producto insignia de mayor valor de toda la tienda. Se solicita obtener el nombre del producto y su precio unitario para el artículo más caro de todo el catálogo utilizando una subconsulta escalar en la cláusula WHERE.",
    analogia: "Es como enviar a un asistente a revisar todas las etiquetas de la tienda para que anote en un papelito el precio más alto ($263.50). Luego, regresas a los estantes y tomas el artículo que coincida exactamente con ese precio anotado en el papelito.",
    concepto: "Una subconsulta escalar retorna exactamente una fila y una columna (un único valor atómico). Al situarse en la cláusula `WHERE`, el motor la evalúa una sola vez (`InitPlan`), y luego usa ese valor constante para filtrar las filas de la consulta externa.",
    tip: "Asegúrate de que la subconsulta escalar use funciones como `MAX()`, `MIN()` o `LIMIT 1`. Si por error la subconsulta retorna más de una fila, el motor lanzará `ERROR: more than one row returned by a subquery used as an expression`.",
    kpi: "Identificar el producto de precio máximo del catálogo para campañas de productos insignia y análisis de dispersión de precios.",
    fuentes: "Tabla `products` (77 filas, columnas `product_name`, `unit_price`). Granularidad: 1 fila de resultado.",
    relaciones: "Subconsulta independiente sobre la misma tabla `products`.",
    filtros: "`WHERE unit_price = (SELECT MAX(unit_price) FROM products)`.",
    proyeccion: "`product_name`, `unit_price`.",
    validacion: "En Northwind, el producto más caro es 'Côte de Blaye' con un precio de $263.50.",
    engine: [
      "**1. InitPlan (Subconsulta):** El motor ejecuta primero la subconsulta `SELECT MAX(unit_price) FROM products`, obteniendo el valor escalar `263.50`.",
      "**2. FROM products:** Se escanea la tabla `products` (77 tuplas).",
      "**3. WHERE unit_price = 263.50:** Se comparan los precios contra la constante calculada en el paso 1; solo 1 tupla coincide.",
      "**4. SELECT:** Se proyecta `product_name` y `unit_price`."
    ]
  },
  12: {
    enunciado: "El departamento de relaciones internacionales y logística asiática necesita preparar un informe sobre el catálogo de origen japonés. Se solicita listar el identificador de producto, nombre del producto y precio unitario de todos los artículos provistos por proveedores ubicados en Japón, utilizando una subconsulta con el operador IN.",
    analogia: "Es como buscar primero en el directorio de proveedores la lista de códigos de empresas japonesas (IDs 4 y 6). Luego vas al inventario y seleccionas todos los productos cuyo código de proveedor coincida con alguno de los números de tu lista.",
    concepto: "El operador `IN` evalúa si el valor de una columna coincide con cualquiera de los valores retornados por un conjunto o subconsulta multi-fila. El optimizador de PostgreSQL a menudo reescribe subconsultas `IN` como un `Semi Join` o `Hash Join` altamente eficiente.",
    tip: "Si la subconsulta con `IN` pudiera contener valores `NULL`, ten cuidado con `NOT IN` (que puede fallar debido a la lógica trivaluada de SQL). Con `IN`, los `NULL` son descartados de forma segura.",
    kpi: "Auditar el catálogo dependiente de proveedores japoneses para evaluar tiempos de tránsito marítimo y cobertura de stock.",
    fuentes: "Tablas `products` (77 filas) y `suppliers` (29 filas). Granularidad: 1 fila por producto japonés.",
    relaciones: "`products.supplier_id IN (SELECT supplier_id FROM suppliers WHERE country = 'Japan')`.",
    filtros: "Filtro geográfico en subconsulta: `country = 'Japan'`.",
    proyeccion: "`product_id`, `product_name`, `unit_price`.",
    validacion: "En Northwind existen 2 proveedores japoneses (Tokyo Traders y Mayumi's) que abastecen un total de 6 productos.",
    engine: [
      "**1. Subconsulta (suppliers):** Se escanea `suppliers` filtrando `country = 'Japan'`, generando la lista de IDs `{4, 6}`.",
      "**2. FROM products:** Escaneo de `products` (77 tuplas).",
      "**3. WHERE supplier_id IN (4, 6):** El motor filtra los 6 productos correspondientes.",
      "**4. SELECT & ORDER BY product_name:** Proyección y ordenamiento alfabético."
    ]
  },
  13: {
    enunciado: "El equipo de pricing estratégico necesita identificar productos sobrevalorados dentro de sus respectivos segmentos. Se solicita listar el identificador de categoría, el nombre del producto y su precio unitario para todos aquellos artículos cuyo precio sea estrictamente superior al precio promedio de todos los productos de su misma categoría, utilizando una subconsulta correlacionada.",
    analogia: "Es como evaluar alumnos en diferentes colegios: no comparas la nota de un alumno con el promedio de todo el país, sino con el promedio de su propio colegio. Si saca más que la media de sus compañeros de clase, destaca en su grupo.",
    concepto: "Una subconsulta correlacionada hace referencia a una columna de la consulta externa (`p1.category_id = p2.category_id`). Conceptualmente se reevalúa para cada fila candidata externa, aunque el optimizador puede transformar la correlación en un join con agregación previa (decorrelation).",
    tip: "Las subconsultas correlacionadas en `WHERE` son muy expresivas, pero en tablas masivas pueden derivar en bucles anidados si no existen índices adecuados en la columna de correlación.",
    kpi: "Detección de productos de precio premium relativo por categoría (precio > media de su categoría).",
    fuentes: "Tabla `products` (alias `p1` y `p2`). Granularidad: 1 fila por producto.",
    relaciones: "Auto-correlación sobre `products` mediante `category_id`.",
    filtros: "`p1.unit_price > (SELECT AVG(p2.unit_price) FROM products p2 WHERE p2.category_id = p1.category_id)`.",
    proyeccion: "`p1.category_id`, `p1.product_name`, `p1.unit_price`.",
    validacion: "En Northwind, 27 de los 77 productos tienen un precio superior al promedio de su categoría.",
    engine: [
      "**1. FROM products p1:** Escaneo de cada tupla externa `p1`.",
      "**2. Subconsulta correlacionada:** Para la categoría de `p1`, se calcula `AVG(p2.unit_price)` sobre `products p2`.",
      "**3. WHERE p1.unit_price > AVG:** Se compara el precio de la fila actual contra el promedio calculado de su categoría.",
      "**4. SELECT & ORDER BY p1.category_id, p1.unit_price DESC:** Proyección ordenada."
    ]
  },
  14: {
    enunciado: "La gerencia de logística y despacho necesita dimensionar el tamaño de empaque promedio de los envíos. Se solicita calcular el número promedio de ítems distintos (líneas de detalle) que contiene un pedido en Northwind, utilizando una tabla derivada (Derived Table) en la cláusula FROM.",
    analogia: "Es como contar cuántos productos distintos metió cada cliente en su bolsa de compras y luego promediar el tamaño de todas las bolsas para saber qué tamaño estándar de caja de cartón comprar.",
    concepto: "Una tabla derivada (o subconsulta en `FROM`) genera un conjunto de resultados intermedio en memoria con su propio alias obligatorio (`AS sub`). La consulta externa aplica una función agregada de segundo nivel (`AVG`) sobre la métrica precalculada en la tabla derivada.",
    tip: "En PostgreSQL y en el estándar ANSI SQL, toda subconsulta en la cláusula `FROM` debe tener obligatoriamente un alias de tabla (ej. `AS sub`), de lo contrario arrojará `ERROR: subquery in FROM must have an alias`.",
    kpi: "Promedio de líneas de detalle por orden (Basket Breadth) para dimensionar empaquetado logístico.",
    fuentes: "Tabla `order_details` (2,155 filas agrupadas en 830 órdenes). Granularidad: 1 fila escalar.",
    relaciones: "Agregación interna por `order_id` y agregación externa global.",
    filtros: "Ninguno.",
    proyeccion: "`ROUND(AVG(items_por_pedido)::numeric, 2) AS promedio_items_por_pedido`.",
    validacion: "2,155 líneas divididas entre 830 órdenes da exactamente 2.60 líneas de detalle por pedido.",
    engine: [
      "**1. Subconsulta interna (Derived Table):** Escanea `order_details`, agrupa por `order_id` y cuenta `COUNT(*) AS items_por_pedido` para los 830 pedidos.",
      "**2. Consulta externa:** Toma el conjunto virtual de 830 filas resultantes.",
      "**3. SELECT AVG():** Calcula el promedio de las 830 cifras.",
      "**4. ROUND():** Redondea a 2 decimales."
    ]
  },
  15: {
    enunciado: "El área de auditoría de cuentas comerciales necesita identificar a todos los clientes que han registrado actividad comercial real en la plataforma. Se solicita listar el identificador y nombre de empresa de aquellos clientes que cuentan con al menos un pedido registrado, utilizando el operador EXISTS (Semi Join).",
    analogia: "Es como pararte en la puerta de un club con una lista de socios y un detector: en cuanto encuentras el primer comprobante de compra de un socio en el sistema, lo marcas como 'Activo' y dejas de buscar más pedidos para él.",
    concepto: "`EXISTS` evalúa si una subconsulta correlacionada devuelve al menos una fila. En cuanto encuentra la primera coincidencia, cortocircuita (retorna `TRUE`) sin necesidad de contar ni escanear el resto de filas. PostgreSQL lo ejecuta mediante un `Hash Semi Join`.",
    tip: "Usar `SELECT 1` o `SELECT *` dentro de `EXISTS` es computacionalmente equivalente en PostgreSQL, ya que el optimizador ignora la lista de proyección y solo verifica la existencia de tuplas.",
    kpi: "Tasa de activación de clientes: Identificar clientes con actividad comercial histórica (`EXISTS orders`).",
    fuentes: "Tablas `customers` (91 filas) y `orders` (830 filas). Granularidad: 1 fila por cliente activo.",
    relaciones: "`EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)`.",
    filtros: "Condición de correlación en subconsulta.",
    proyeccion: "`c.customer_id`, `c.company_name`.",
    validacion: "En el dataset canónico de Northwind, de los 91 clientes, exactamente 89 han realizado pedidos (solo 'FISSA' y 'PARIS' tienen 0 pedidos).",
    engine: [
      "**1. FROM customers c:** Escaneo de los 91 clientes.",
      "**2. Semi Join (EXISTS):** El motor sondea el índice en `orders.customer_id`. Si encuentra 1 coincidencia, la tupla de `customers` califica de inmediato.",
      "**3. Filtro:** Pasan 89 clientes activos; se descartan 2.",
      "**4. SELECT & ORDER BY c.company_name:** Salida ordenada alfabéticamente."
    ]
  },
  16: {
    enunciado: "El equipo de catálogo y depuración de inventario necesita identificar productos obsoletos o 'fantasmas' que nunca han tenido ninguna venta histórica. Se solicita listar el identificador y nombre de los productos que no registran ninguna venta en toda la historia de la empresa, utilizando el operador NOT EXISTS (Anti Join).",
    analogia: "Es como revisar cada artículo del almacén y buscar si alguna vez se emitió una factura por él: si no existe ni un solo registro de venta en el historial, el producto se marca como inactivo para descatalogarlo.",
    concepto: "`NOT EXISTS` ejecuta un `Anti Join`: retorna las filas de la tabla externa que NO encuentran ninguna correspondencia en la subconsulta. A diferencia de `NOT IN`, `NOT EXISTS` maneja de forma totalmente segura los valores `NULL` sin riesgo de retornar conjuntos vacíos accidentales.",
    tip: "Prefiere siempre `NOT EXISTS` sobre `NOT IN` cuando la columna de la subconsulta pueda contener `NULL`s, ya que `NOT IN (..., NULL)` evalúa a `UNKNOWN` y descarta todas las filas.",
    kpi: "Detección de productos de rotación cero (Catálogo muerto / Zero-sales items).",
    fuentes: "Tablas `products` (77 filas) y `order_details` (2,155 filas). Granularidad: 1 fila por producto sin ventas.",
    relaciones: "`NOT EXISTS (SELECT 1 FROM order_details od WHERE od.product_id = p.product_id)`.",
    filtros: "Condición de Anti-Join.",
    proyeccion: "`p.product_id`, `p.product_name`.",
    validacion: "En Northwind todos los 77 productos han tenido al menos una venta histórica, por lo que el resultado esperado es exactamente 0 filas (`0 rows`).",
    engine: [
      "**1. FROM products p:** Escaneo de los 77 productos.",
      "**2. Anti Join (NOT EXISTS):** Se verifica la presencia de `product_id` en `order_details`.",
      "**3. Filtro:** Los 77 productos tienen al menos una venta registrada.",
      "**4. Resultado:** Conjunto vacío (0 filas)."
    ]
  },
  17: {
    enunciado: "El comité de análisis competitivo necesita identificar productos fuera del segmento básico de bebidas. Se solicita listar el identificador, nombre y precio unitario de todos los productos que tengan un precio superior a CUALQUIERA de los productos de la categoría 1 (Bebidas), utilizando el operador ANY.",
    analogia: "Es como decir: 'Muéstrame todos los artículos de la tienda que sean más caros que el artículo más barato de la sección de Bebidas'. Si superas a cualquiera (al mínimo), ya calificas.",
    concepto: "`> ANY (subconsulta)` equivale lógicamente a `> (SELECT MIN(columna) FROM subconsulta)`. Es decir, la condición se cumple si el valor es mayor que al menos un elemento del conjunto devuelto.",
    tip: "`> ANY` evalúa si el valor es mayor que el mínimo del conjunto. En contraste, `< ANY` evalúa si el valor es menor que el máximo del conjunto.",
    kpi: "Análisis de umbrales cruzados de precios frente a la categoría de referencia (Categoría 1: Bebidas).",
    fuentes: "Tabla `products` (77 filas). Granularidad: 1 fila por producto calificado.",
    relaciones: "Subconsulta sobre `products` filtrada por `category_id = 1`.",
    filtros: "`unit_price > ANY (SELECT unit_price FROM products WHERE category_id = 1)`.",
    proyeccion: "`product_id`, `product_name`, `unit_price`.",
    validacion: "El producto más barato de la Categoría 1 cuesta $4.50 (Guaraná Fantástica). Todo producto con precio > $4.50 califica (75 productos en total).",
    engine: [
      "**1. Subconsulta:** Se obtienen los 12 precios de los productos de la categoría 1 (mínimo = $4.50).",
      "**2. FROM products:** Escaneo de los 77 productos.",
      "**3. WHERE unit_price > ANY (...):** Pasan todos los productos con precio > $4.50 (75 productos).",
      "**4. SELECT & ORDER BY unit_price DESC:** Proyección y ordenamiento descendente."
    ]
  },
  18: {
    enunciado: "El departamento comercial busca identificar productos ultra-exclusivos de alta gama. Se solicita listar el identificador, nombre y precio unitario de todos aquellos productos cuyo precio sea superior a TODOS los productos pertenecientes a la categoría 1 (Bebidas), utilizando el operador ALL.",
    analogia: "Es como decir: 'Muéstrame los artículos que sean más caros que el producto más caro de toda la sección de Bebidas'. Tienes que superar a todos sin excepción para calificar.",
    concepto: "`> ALL (subconsulta)` equivale lógicamente a `> (SELECT MAX(columna) FROM subconsulta)`. La condición solo es verdadera si el valor supera a cada uno de los elementos devueltos por la subconsulta.",
    tip: "Si la subconsulta de `ALL` retorna un conjunto vacío, la condición `> ALL` evalúa a `TRUE` para todas las filas. Ten en cuenta este comportamiento en casos borde.",
    kpi: "Identificar artículos de ultra-lujo que superen el techo de precios de la categoría 1 ($263.50).",
    fuentes: "Tabla `products` (77 filas). Granularidad: 1 fila por producto ultra-lujo.",
    relaciones: "Subconsulta sobre `products` con `category_id = 1`.",
    filtros: "`unit_price > ALL (SELECT unit_price FROM products WHERE category_id = 1)`.",
    proyeccion: "`product_id`, `product_name`, `unit_price`.",
    validacion: "El producto más caro de la categoría 1 es 'Côte de Blaye' ($263.50), que es a la vez el producto más caro de todo el catálogo. Por ende, ningún producto supera a todos (resultado: 0 rows).",
    engine: [
      "**1. Subconsulta:** Obtiene los precios de la categoría 1 (máximo = $263.50).",
      "**2. FROM products:** Escaneo de los 77 productos.",
      "**3. WHERE unit_price > ALL (...):** Se evalúa `unit_price > 263.50`. Ningún producto lo supera.",
      "**4. Salida:** 0 filas."
    ]
  },
  19: {
    enunciado: "El equipo de CRM y retención necesita auditar la fecha del último pedido registrado para cada cliente de la cartera. Se solicita listar el identificador de cliente, el nombre de la empresa y la fecha de su pedido más reciente, utilizando una subconsulta correlacionada en la cláusula SELECT.",
    analogia: "Es como tener una lista con los 91 clientes de tu empresa y, al lado de cada nombre, consultar en el archivo de órdenes la fecha más reciente en que ese cliente específico firmó un contrato. Si nunca compró, queda en blanco (NULL).",
    concepto: "Una subconsulta escalar en la cláusula `SELECT` se evalúa para cada fila proyectada de la consulta principal. Si la subconsulta correlacionada no encuentra ningún registro en `orders` para un cliente dado (como los clientes sin pedidos), retorna automáticamente `NULL`.",
    tip: "En PostgreSQL, para reportes grandes, un `LEFT JOIN` con `MAX()` y `GROUP BY` o un `LEFT JOIN LATERAL` suele ser más eficiente que una subconsulta escalar en `SELECT`, pero la subconsulta en `SELECT` es muy intuitiva y no altera la cardinalidad de la tabla externa.",
    kpi: "Recencia de Clientes (Dimensión Recency de RFM): Fecha de última compra por cliente en la base.",
    fuentes: "Tablas `customers` (91 filas) y `orders` (830 filas). Granularidad: Exactamente 91 filas (1 por cliente de la base).",
    relaciones: "Correlación: `WHERE o.customer_id = c.customer_id` en la subconsulta de `SELECT`.",
    filtros: "Ninguno en la consulta externa.",
    proyeccion: "`c.customer_id`, `c.company_name`, `(SELECT MAX(o.order_date) FROM orders o WHERE o.customer_id = c.customer_id) AS fecha_ultimo_pedido`.",
    validacion: "Deben figurar exactamente los 91 clientes canónicos de Northwind. Los clientes 'FISSA' y 'PARIS' mostrarán `NULL` al no registrar compras.",
    engine: [
      "**1. FROM customers c:** Se leen secuencialmente los 91 clientes.",
      "**2. Proyección de SELECT:** Por cada cliente, se ejecuta la subconsulta correlacionada sondeando el índice en `orders.customer_id` y calculando `MAX(order_date)`.",
      "**3. SELECT:** Se asignan los valores calculados y el alias `fecha_ultimo_pedido`.",
      "**4. ORDER BY c.customer_id:** Se ordenan los 91 registros alfabéticamente."
    ]
  },
  20: {
    enunciado: "La gerencia general requiere un reporte ejecutivo de los 5 productos que mayor facturación neta han generado en toda la historia de la compañía. Se solicita obtener el nombre del producto y su facturación total neta acumulada utilizando una subconsulta anidada en la cláusula FROM, ordenada de forma descendente y limitada al Top 5.",
    analogia: "Es como generar primero una hoja de cálculo con la facturación total de cada uno de los 77 productos y luego ordenar esa hoja para recortar y presentar en la junta directiva únicamente los 5 productos más rentables.",
    concepto: "Combina una subconsulta en `FROM` que agrega y calcula el total neto con descuento `ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2)` por producto, con una consulta externa que ordena por el alias derivado y aplica `LIMIT 5`.",
    tip: "Al anidar en `FROM`, el cálculo pesado de agregación se resuelve en la tabla derivada, permitiendo que la consulta exterior solo se encargue de la presentación, ordenamiento y acotamiento.",
    kpi: "Identificar los 5 productos estrella (Top-Revenue Drivers) de la empresa.",
    fuentes: "Tablas `products` (77 filas) y `order_details` (2,155 filas). Granularidad: 5 filas finales.",
    relaciones: "`products.product_id = order_details.product_id`.",
    filtros: "`LIMIT 5` en la consulta exterior.",
    proyeccion: "`product_name`, `facturacion_total`.",
    validacion: "El producto Top 1 es 'Côte de Blaye' con $141,396.74 de facturación neta.",
    engine: [
      "**1. Subconsulta (FROM sub):** Hash Join entre `products` y `order_details`, agrupando por `product_name` y calculando la facturación total de los 77 productos.",
      "**2. Consulta externa:** Recibe las 77 filas precalculadas.",
      "**3. ORDER BY facturacion_total DESC:** Ordenamiento descendente en memoria `work_mem`.",
      "**4. LIMIT 5:** El nodo `Limit` extrae las 5 tuplas superiores y finaliza la ejecución."
    ]
  }
};

fs.writeFileSync('.agents/worker_intermedio_1/modules/block2_11_20.json', JSON.stringify(b2, null, 2), 'utf8');
console.log('Saved block 2 (Ex 11-20) JSON successfully.');
