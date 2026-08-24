const fs = require('fs');

const b1 = {
  1: {
    enunciado: "El departamento comercial y de expansión internacional requiere identificar los mercados geográficos estratégicos con alta densidad de clientes. Se solicita listar todos los países que cuentan con más de 5 clientes registrados en la base de datos, junto con el conteo total de clientes en cada país, ordenados de forma descendente por volumen de clientes.",
    analogia: "Imagina que tienes una gran cantidad de cartas de clientes desordenadas en tu escritorio. Usas cajas de mudanza etiquetadas con el nombre de cada país para clasificar las cartas (GROUP BY). Luego, tomas una báscula y descartas todas las cajas que contengan 5 o menos cartas (HAVING). Solo te quedas con las cajas pesadas que representan mercados consolidados.",
    concepto: "La cláusula `GROUP BY` colapsa conjuntos de filas que comparten valores idénticos en una o más columnas en una sola fila representativa por grupo. Para filtrar estos grupos resultantes basados en condiciones agregadas (`COUNT(*) > 5`), es obligatorio utilizar `HAVING`, ya que `WHERE` opera exclusivamente antes de que los grupos sean creados.",
    tip: "Nunca intentes escribir `WHERE COUNT(*) > 5`. El motor PostgreSQL arrojará inmediatamente `ERROR: aggregate function calls cannot be used in WHERE` porque `WHERE` evalúa fila por fila antes de que existan las funciones de agregación.",
    kpi: "Identificar países con masa crítica comercial (densidad > 5 clientes) para focalizar campañas de retención y soporte local.",
    fuentes: "Tabla `customers` (clave primaria `customer_id`, 91 clientes totales). Granularidad requerida: 1 fila por país clasificado.",
    relaciones: "Consulta mono-tabla sobre `customers`. No requiere JOINs adicionales.",
    filtros: "Filtro post-agregación: `HAVING COUNT(*) > 5` sobre los grupos formados por `country`.",
    proyeccion: "Proyectar `country` y `COUNT(*) AS total_clientes`, ordenados por `total_clientes DESC`.",
    validacion: "Verificar que ningún país del reporte tenga 5 o menos clientes. El total de países devueltos debe sumar solo aquellos con volumen representativo (USA, France, Germany, Brazil, UK).",
    engine: [
      "**1. FROM customers:** El motor escanea secuencialmente las 91 tuplas de la tabla `customers`.",
      "**2. WHERE:** No hay predicados de fila a nivel de tupla individual, por lo que las 91 tuplas pasan a la siguiente fase.",
      "**3. GROUP BY country:** El motor clasifica las tuplas en 21 cubetas (buckets) según el valor de `country`, inicializando un acumulador para `COUNT(*)` en memoria `work_mem`.",
      "**4. HAVING COUNT(*) > 5:** Se evalúa el predicado agregado sobre cada una de las 21 cubetas. Solo 5 países superan el umbral estricto de 5 clientes; los otros 16 grupos son descartados.",
      "**5. SELECT:** Se proyectan las columnas `country` y se asigna el alias `total_clientes` al conteo evaluado.",
      "**6. ORDER BY total_clientes DESC:** Se ordenan los 5 grupos finales de mayor a menor volumen."
    ]
  },
  2: {
    enunciado: "El equipo de gestión de inventario y compras necesita auditar la variedad de productos ofrecidos en el catálogo. Se requiere listar el identificador de categoría, el nombre de la categoría y la cantidad total de productos pertenecientes a ella, filtrando únicamente aquellas categorías que tengan más de 10 productos registrados, ordenadas descendentemente por volumen de productos.",
    analogia: "Imagina los pasillos de un supermercado (Lácteos, Bebidas, Carnes). Cuentas los productos en cada pasillo y solo reportas al gerente los pasillos que tienen más de 10 productos distintos en estantería para asegurar que tengan suficiente personal asignado.",
    concepto: "Al cruzar dos tablas (`categories` y `products`) mediante un `INNER JOIN`, agrupamos por la clave primaria y descriptores de la tabla dimensional (`c.category_id, c.category_name`). `HAVING COUNT(p.product_id) > 10` asegura que solo se retornen categorías densamente pobladas.",
    tip: "Cuando agrupas después de un `JOIN`, incluye siempre la clave primaria de la tabla padre en `GROUP BY`. En PostgreSQL, si incluyes la clave primaria de una tabla en `GROUP BY`, el motor infiere la dependencia funcional de las demás columnas de esa misma tabla, aunque es buena práctica explicitar las columnas proyectadas para total portabilidad.",
    kpi: "Identificar categorías de alta densidad de catálogo (> 10 productos) para dimensionar espacio en góndola y esfuerzo de abastecimiento.",
    fuentes: "Tablas `categories` (8 filas) y `products` (77 filas). Granularidad: 1 fila por categoría clasificada.",
    relaciones: "`categories.category_id = products.category_id` (relación 1:N).",
    filtros: "Post-agregación: `HAVING COUNT(p.product_id) > 10`.",
    proyeccion: "`c.category_id`, `c.category_name`, `COUNT(p.product_id) AS total_productos`.",
    validacion: "Verificar que todas las categorías del resultado contengan estrictamente 11 o más productos.",
    engine: [
      "**1. FROM & JOIN:** El motor lee `categories` (8 filas) y `products` (77 filas) realizando un `Hash Join` sobre `category_id`.",
      "**2. WHERE:** No hay predicados de fila individuales.",
      "**3. GROUP BY c.category_id, c.category_name:** Se crean 8 grupos en memoria.",
      "**4. HAVING COUNT(p.product_id) > 10:** Se evalúa el conteo de productos por grupo; pasan solo las 4 categorías con más de 10 ítems.",
      "**5. SELECT:** Se proyectan las columnas dimensionales y la métrica agregada.",
      "**6. ORDER BY total_productos DESC:** Se ordenan las 4 categorías de mayor a menor."
    ]
  },
  3: {
    enunciado: "La gerencia de operaciones comerciales necesita evaluar el desempeño de la fuerza de ventas para un programa de incentivos. Se solicita obtener el identificador de empleado y la cantidad total de pedidos gestionados, filtrando únicamente aquellos empleados que hayan procesado más de 80 pedidos en total, ordenados de forma descendente por productividad.",
    analogia: "Imagina un tablero de control donde se registran los pedidos de los vendedores. Quieres otorgar un bono exclusivo a los vendedores de élite que hayan cerrado más de 80 operaciones comerciales.",
    concepto: "Esta consulta realiza una agregación mono-tabla sobre la entidad transaccional `orders` (830 filas), agrupando por `employee_id` y filtrando mediante `HAVING COUNT(order_id) > 80`.",
    tip: "Agrupar directamente sobre la tabla de hechos (`orders`) antes de cruzar con la tabla dimensional (`employees`) ahorra trabajo al motor si solo se necesitan las claves de los empleados.",
    kpi: "Medir volumen de pedidos procesados por representante de ventas para identificar al top tier comercial (> 80 pedidos).",
    fuentes: "Tabla `orders` (830 filas, clave primaria `order_id`, clave foránea `employee_id`). Granularidad: 1 fila por empleado.",
    relaciones: "Mono-tabla sobre `orders`.",
    filtros: "Post-agregación: `HAVING COUNT(order_id) > 80`.",
    proyeccion: "`employee_id`, `COUNT(order_id) AS total_pedidos`.",
    validacion: "Verificar que todos los empleados en la salida tengan más de 80 pedidos. En Northwind, 5 de los 9 empleados superan esta meta.",
    engine: [
      "**1. FROM orders:** Escaneo secuencial de las 830 tuplas de la tabla `orders`.",
      "**2. WHERE:** No aplica.",
      "**3. GROUP BY employee_id:** Se generan 9 cubetas en memoria correspondientes a los 9 empleados activos.",
      "**4. HAVING COUNT(order_id) > 80:** Se evalúa el acumulador de cada cubeta; 5 empleados superan el límite de 80.",
      "**5. SELECT & ORDER BY total_pedidos DESC:** Se proyectan las métricas y se ordenan descendentemente."
    ]
  },
  4: {
    enunciado: "El departamento de cadena de suministro desea auditar a los socios estratégicos clave. Se requiere listar el identificador del proveedor, el nombre de la empresa proveedora y la cantidad de productos que suministran, considerando únicamente a aquellos proveedores que abastecen con más de 3 productos al catálogo, ordenados de forma descendente por cantidad de productos.",
    analogia: "Es como revisar tu libreta de proveedores de materias primas y seleccionar únicamente aquellos que son distribuidores integrales (te venden más de 3 productos distintos), para consolidar pedidos y negociar descuentos por volumen.",
    concepto: "Combina `suppliers` y `products` mediante `INNER JOIN`, agrupando por `s.supplier_id, s.company_name`. El filtro `HAVING COUNT(p.product_id) > 3` identifica a los proveedores con portafolio amplio.",
    tip: "Recuerda que si una columna descriptiva como `company_name` está en el `SELECT`, debe figurar obligatoriamente en el `GROUP BY` para evitar errores de sintaxis estándar.",
    kpi: "Identificar proveedores clave con portafolio diversificado (> 3 productos) para consolidación de compras.",
    fuentes: "Tablas `suppliers` (29 filas) y `products` (77 filas). Granularidad: 1 fila por proveedor.",
    relaciones: "`suppliers.supplier_id = products.supplier_id`.",
    filtros: "Post-agregación: `HAVING COUNT(p.product_id) > 3`.",
    proyeccion: "`s.supplier_id`, `s.company_name`, `COUNT(p.product_id) AS total_productos`.",
    validacion: "Comprobar que en el resultado final ningún proveedor tenga 3 o menos productos.",
    engine: [
      "**1. FROM suppliers INNER JOIN products:** Se realiza un `Hash Join` uniendo las 29 filas de `suppliers` con las 77 filas de `products`.",
      "**2. WHERE:** No aplica.",
      "**3. GROUP BY s.supplier_id, s.company_name:** Se generan las 29 agrupaciones.",
      "**4. HAVING COUNT(p.product_id) > 3:** Se descartan los proveedores con 3 o menos productos (quedan 4 proveedores).",
      "**5. SELECT & ORDER BY total_productos DESC:** Proyección y ordenamiento final."
    ]
  },
  5: {
    enunciado: "El área de finanzas y fidelización de clientes necesita segmentar la base comercial para una campaña VIP. Se requiere calcular la facturación monetaria total neta generada por cada cliente (considerando cantidad, precio unitario y descuento aplicado), mostrando únicamente aquellos clientes cuyo volumen de compras acumulado supere los $5,000 USD, ordenados descendentemente por facturación total.",
    analogia: "Imagina calcular el gasto total que cada cliente ha dejado en la caja registradora a lo largo de todo el año, aplicando los descuentos de cada ticket de compra, y premiar con una tarjeta dorada a todos los que hayan acumulado más de $5,000.",
    concepto: "Requiere unir la cabecera del pedido (`orders`) con sus líneas de detalle (`order_details`), calcular el importe neto por línea `od.quantity * od.unit_price * (1 - od.discount)` y agregarlo con `SUM()`. El filtro `HAVING SUM(...) > 5000` extrae a los clientes de alto valor monetario.",
    tip: "El descuento (`discount`) es un valor fraccionario (ej. 0.05 para 5% o 0.20 para 20%). Multiplicar por `(1 - discount)` descuenta automáticamente la fracción exacta del precio bruto.",
    kpi: "Segmentación RFM (Dimensión Monetary): Identificar clientes con facturación acumulada > $5,000 USD.",
    fuentes: "Tablas `orders` (830 filas) y `order_details` (2,155 filas). Granularidad: 1 fila por cliente.",
    relaciones: "`orders.order_id = order_details.order_id`.",
    filtros: "Post-agregación: `HAVING SUM(od.quantity * od.unit_price * (1 - od.discount)) > 5000`.",
    proyeccion: "`o.customer_id`, `ROUND(SUM(od.quantity * od.unit_price * (1 - od.discount))::numeric, 2) AS facturacion_total`.",
    validacion: "Verificar que el cliente con mayor facturación sea QUICK ($110,277.31) y que 55 de los 91 clientes cumplan con el criterio de facturación.",
    engine: [
      "**1. FROM orders INNER JOIN order_details:** `Hash Join` entre las 830 órdenes y los 2,155 detalles de orden.",
      "**2. WHERE:** No hay filtros a nivel de fila.",
      "**3. GROUP BY o.customer_id:** Se agrupan los 2,155 registros en 89 cubetas de clientes con pedidos.",
      "**4. HAVING SUM(...) > 5000:** Se evalúa la facturación total acumulada por cubeta; 55 clientes superan los $5,000.",
      "**5. SELECT:** Se redondea el monto a 2 decimales convirtiendo a tipo `numeric`.",
      "**6. ORDER BY facturacion_total DESC:** Se ordenan los 55 clientes de mayor a menor ingreso generado."
    ]
  },
  6: {
    enunciado: "El departamento de logística y almacenes necesita identificar los artículos de alta rotación para optimizar la política de reabastecimiento. Se solicita calcular la cantidad total de unidades vendidas por cada producto, mostrando el identificador, nombre del producto y total de unidades, filtrando únicamente aquellos productos que hayan superado las 500 unidades vendidas, ordenados de forma descendente.",
    analogia: "Es como revisar el contador del almacén para ver qué cajas salen más rápido de las estanterías: aquellos productos que han vendido más de 500 unidades son tus productos estrella de alta rotación (Fast Movers).",
    concepto: "Une el catálogo maestro `products` con el histórico de ventas `order_details`, colapsa por producto con `GROUP BY p.product_id, p.product_name` y filtra los grupos con `HAVING SUM(od.quantity) > 500`.",
    tip: "Distinguir entre volumen de facturación monetaria ($) y volumen físico de unidades vendidas (uds). Aquí medimos rotación física mediante `SUM(od.quantity)`.",
    kpi: "Análisis de Rotación de Inventario (Fast-Moving Consumer Goods): Identificar productos con > 500 unidades vendidas.",
    fuentes: "Tablas `products` (77 filas) y `order_details` (2,155 filas). Granularidad: 1 fila por producto.",
    relaciones: "`products.product_id = order_details.product_id`.",
    filtros: "Post-agregación: `HAVING SUM(od.quantity) > 500`.",
    proyeccion: "`p.product_id`, `p.product_name`, `SUM(od.quantity) AS unidades_vendidas`.",
    validacion: "Comprobar que en la salida todos los productos tengan más de 500 unidades. 72 de los 77 productos superan esta cota.",
    engine: [
      "**1. FROM products INNER JOIN order_details:** Hash Join sobre `product_id`.",
      "**2. WHERE:** Sin filtros de fila.",
      "**3. GROUP BY p.product_id, p.product_name:** Se forman 77 grupos en memoria.",
      "**4. HAVING SUM(od.quantity) > 500:** Pasan 72 productos.",
      "**5. SELECT & ORDER BY unidades_vendidas DESC:** Proyección y ordenamiento descendente."
    ]
  },
  7: {
    enunciado: "La dirección ejecutiva solicita un informe macroeconómico de crecimiento interanual. Se requiere extraer el año de emisión de los pedidos y calcular el número total de órdenes registradas en cada año, ordenadas cronológicamente de forma ascendente.",
    analogia: "Es como mirar un calendario histórico y contar cuántos contratos se firmaron en cada año fiscal (1996, 1997, 1998) para evaluar el ritmo de expansión de la empresa.",
    concepto: "Utiliza la función de extracción de fecha `EXTRACT(YEAR FROM order_date)` tanto en la proyección como en la cláusula `GROUP BY`, colapsando los 830 pedidos en los 3 años de actividad histórica de Northwind.",
    tip: "En PostgreSQL puedes usar `EXTRACT(YEAR FROM order_date)` o `DATE_PART('year', order_date)`. `EXTRACT` es el estándar ANSI SQL preferido.",
    kpi: "Volumen transaccional interanual para análisis de tendencias de crecimiento y estacionalidad macro.",
    fuentes: "Tabla `orders` (830 filas, columna `order_date`). Granularidad: 1 fila por año calendario.",
    relaciones: "Mono-tabla sobre `orders`.",
    filtros: "Ninguno.",
    proyeccion: "`EXTRACT(YEAR FROM order_date) AS anio`, `COUNT(order_id) AS total_pedidos`.",
    validacion: "La suma de los pedidos de los 3 años (152 en 1996, 408 en 1997, 270 en 1998) debe dar exactamente los 830 pedidos de Northwind.",
    engine: [
      "**1. FROM orders:** Lectura de las 830 tuplas de la tabla `orders`.",
      "**2. GROUP BY EXTRACT(YEAR FROM order_date):** Se evalúa la función escalar de fecha sobre cada fila y se agrupan en 3 cubetas: 1996, 1997 y 1998.",
      "**3. SELECT:** Se proyecta el año y el acumulador de `COUNT(order_id)`.",
      "**4. ORDER BY anio ASC:** Se ordenan los 3 registros cronológicamente."
    ]
  },
  8: {
    enunciado: "El departamento de operaciones y logística internacional necesita auditar las rutas de envío de alto costo. Se solicita listar el país de destino (`ship_country`) y el costo de flete promedio por pedido, mostrando únicamente aquellos países donde el flete promedio supere los $50 USD, ordenados de mayor a menor costo promedio.",
    analogia: "Es como revisar los gastos de envío internacional de tu tienda online: si enviar paquetes a ciertos países cuesta en promedio más de $50, debes revisar tus convenios con las empresas de transporte o cobrar un recargo logístico a los clientes de esas zonas.",
    concepto: "Agrupa los pedidos por país de destino `ship_country`, calcula la media con `AVG(freight)` y filtra con `HAVING AVG(freight) > 50`.",
    tip: "Aplica siempre `ROUND(..., 2)` y casteo a `numeric` sobre funciones como `AVG()` para evitar números de punto flotante con decenas de decimales en el reporte final.",
    kpi: "Detección de destinos de exportación de alto costo logístico (flete promedio > $50 USD).",
    fuentes: "Tabla `orders` (830 filas, columnas `ship_country`, `freight`). Granularidad: 1 fila por país de destino.",
    relaciones: "Mono-tabla sobre `orders`.",
    filtros: "Post-agregación: `HAVING AVG(freight) > 50`.",
    proyeccion: "`ship_country`, `ROUND(AVG(freight)::numeric, 2) AS flete_promedio`.",
    validacion: "Verificar que los 13 países resultantes tengan promedios superiores a $50, encabezados por Austria ($184.79).",
    engine: [
      "**1. FROM orders:** Escaneo de las 830 filas de `orders`.",
      "**2. GROUP BY ship_country:** Clasificación en las 21 cubetas de países de destino.",
      "**3. HAVING AVG(freight) > 50:** Se evalúa la media de flete; 13 países superan los $50.",
      "**4. SELECT & ORDER BY flete_promedio DESC:** Proyección y ordenamiento de mayor a menor costo."
    ]
  },
  9: {
    enunciado: "El departamento de Recursos Humanos necesita coordinar espacios de trabajo colaborativo o sedes físicas compartidas. Se solicita obtener las ciudades donde reside más de un empleado de la empresa, junto con la cantidad total de empleados en cada una de esas ciudades, ordenadas descendentemente.",
    analogia: "Imagina un mapa con pines que representan las casas de los trabajadores de una empresa remota: quieres saber en qué ciudades hay 2 o más compañeros viviendo cerca para abrir una oficina física o coworking compartido.",
    concepto: "Agrupa la tabla de personal `employees` (9 filas) por `city` y filtra mediante `HAVING COUNT(employee_id) > 1` para detectar concentraciones urbanas.",
    tip: "Al contar registros de personas, utiliza `COUNT(employee_id)` o `COUNT(*)` sobre la clave primaria para garantizar exactitud.",
    kpi: "Concentración geográfica de talento interno para evaluación de sedes corporativas (ciudades con > 1 empleado).",
    fuentes: "Tabla `employees` (9 filas, clave primaria `employee_id`, columna `city`). Granularidad: 1 fila por ciudad clasificada.",
    relaciones: "Mono-tabla sobre `employees`.",
    filtros: "Post-agregación: `HAVING COUNT(employee_id) > 1`.",
    proyeccion: "`city`, `COUNT(employee_id) AS total_empleados`.",
    validacion: "En Northwind, de las 5 ciudades donde residen empleados, solo London (4 empleados) y Seattle (2 empleados) tienen más de 1 colaborador.",
    engine: [
      "**1. FROM employees:** Lectura de las 9 tuplas de la tabla `employees`.",
      "**2. GROUP BY city:** Agrupamiento en 5 cubetas urbanas (London, Seattle, Tacoma, Kirkland, Redmond).",
      "**3. HAVING COUNT(employee_id) > 1:** London (4) y Seattle (2) superan la condición; las otras 3 ciudades son descartadas.",
      "**4. SELECT & ORDER BY total_empleados DESC:** Salida ordenada."
    ]
  },
  10: {
    enunciado: "El comité de fijación de precios y catálogo necesita auditar las líneas de producto de gama alta. Se solicita listar el identificador de categoría, el nombre de la categoría y el precio unitario promedio de los productos que contiene, filtrando únicamente las categorías cuyo precio promedio sea superior a $30 USD, ordenadas de mayor a menor precio promedio.",
    analogia: "Es como clasificar las secciones de una tienda departamental (Joyería, Electrónica, Ropa básica) y marcar con una etiqueta dorada las secciones de lujo donde el producto promedio cuesta más de $30.",
    concepto: "Cruza `categories` y `products`, agrupa por categoría y evalúa `HAVING AVG(p.unit_price) > 30`, redondeando el promedio resultante.",
    tip: "El cálculo del promedio ignora automáticamente los valores `NULL`, aunque en `products.unit_price` todos los valores están definidos.",
    kpi: "Identificar categorías premium (ticket promedio de producto > $30 USD) para estrategias de pricing.",
    fuentes: "Tablas `categories` (8 filas) y `products` (77 filas). Granularidad: 1 fila por categoría clasificada.",
    relaciones: "`categories.category_id = products.category_id`.",
    filtros: "Post-agregación: `HAVING AVG(p.unit_price) > 30`.",
    proyeccion: "`c.category_id`, `c.category_name`, `ROUND(AVG(p.unit_price)::numeric, 2) AS precio_promedio`.",
    validacion: "Comprobar que las 5 categorías resultantes (Produce, Meat/Poultry, Beverages, Dairy Products, Confections) tengan promedios superiores a $30.",
    engine: [
      "**1. FROM categories INNER JOIN products:** Hash Join sobre `category_id`.",
      "**2. GROUP BY c.category_id, c.category_name:** Agrupamiento en 8 categorías.",
      "**3. HAVING AVG(p.unit_price) > 30:** 5 categorías superan el umbral.",
      "**4. SELECT & ORDER BY precio_promedio DESC:** Proyección con redondeo y ordenamiento descendente."
    ]
  }
};

fs.writeFileSync('.agents/worker_intermedio_1/modules/block1_01_10.json', JSON.stringify(b1, null, 2), 'utf8');
console.log('Saved block 1 (Ex 1-10) JSON successfully.');
