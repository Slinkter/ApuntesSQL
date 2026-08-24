const fs = require('fs');

const b4 = {
  31: {
    enunciado: "El departamento de Recursos Humanos necesita representar la estructura jerárquica de la organización. Se solicita listar el nombre completo del empleado, su cargo y el nombre completo de su supervisor directo inmediato, asegurando que el Director General (que no tiene supervisor) también aparezca en el listado mostrando 'Director General / Sin Manager', utilizando un SELF JOIN con LEFT JOIN.",
    analogia: "Es como dibujar el árbol genealógico de la empresa: cada empleado busca a su jefe en la misma lista de personal. El fundador o director general no tiene a nadie por encima, por lo que su casilla de jefe queda con un rótulo especial de honor.",
    concepto: "Un `SELF JOIN` une una tabla consigo misma empleando dos alias distintos (`employees e1` para los subordinados y `employees e2` para los jefes). Se usa `LEFT JOIN` para preservar al empleado raíz cuya columna `reports_to` es `NULL`.",
    tip: "Usa `COALESCE()` para reemplazar de forma amigable los valores `NULL` del supervisor raíz en lugar de mostrar celdas vacías.",
    kpi: "Mapeo de jerarquías de mando y líneas de reporte en el organigrama empresarial.",
    fuentes: "Tabla `employees` (9 filas, alias `e1` y `e2`, columnas `employee_id`, `reports_to`, `title`). Granularidad: 9 filas.",
    relaciones: "`e1.reports_to = e2.employee_id` (relación recursiva 1:N).",
    filtros: "Ninguno.",
    proyeccion: "`e1.first_name || ' ' || e1.last_name AS empleado`, `e1.title AS cargo`, `COALESCE(e2.first_name || ' ' || e2.last_name, 'Director General / Sin Manager') AS supervisor`.",
    validacion: "En Northwind hay 9 empleados; Andrew Fuller (ID 2, Vice President) tiene `reports_to IS NULL` y es el nodo raíz.",
    engine: [
      "**1. FROM employees e1 LEFT JOIN employees e2:** Se cruza la tabla consigo misma sobre `e1.reports_to = e2.employee_id`.",
      "**2. Preservación:** El `LEFT JOIN` preserva a Andrew Fuller (a pesar de tener `reports_to` nulo).",
      "**3. SELECT:** Se evalúa `COALESCE` y la concatenación de nombres.",
      "**4. ORDER BY e1.employee_id:** Se ordenan los 9 colaboradores por su ID."
    ]
  },
  32: {
    enunciado: "El departamento de Desarrollo Organizacional necesita mapear parejas de compañeros de equipo que reportan a la misma jefatura para programas de mentoría cruzada (Peer Mentoring). Se solicita listar los pares únicos de empleados (empleado_1 y empleado_2) que comparten el mismo manager, junto con el nombre del manager, evitando combinaciones duplicadas o autoreferenciales, mediante un SELF JOIN.",
    analogia: "Es como sentar en una mesa redonda a dos hermanos que tienen los mismos padres: no quieres sentar a una persona consigo misma (e1 = e2), ni quieres registrar a (Juan, Pedro) y luego a (Pedro, Juan) como si fueran dos parejas distintas.",
    concepto: "Para encontrar pares únicos sin duplicados simétricos ni autoreferencias, se une la tabla consigo misma con la doble condición: `e1.reports_to = e2.reports_to AND e1.employee_id < e2.employee_id`. El operador `<` garantiza que cada par aparezca una sola vez.",
    tip: "Usar `e1.employee_id < e2.employee_id` es el patrón canónico en SQL para eliminar duplicados simétricos `(A, B)` vs `(B, A)` y evitar el emparejamiento trivial `(A, A)`.",
    kpi: "Identificación de redes de pares (Peer-to-Peer Networks) dentro de los mismos equipos de reporte.",
    fuentes: "Tabla `employees` (tres alias: `e1`, `e2` y `m` para el manager). Granularidad: 1 fila por par único de compañeros.",
    relaciones: "`e1.reports_to = e2.reports_to AND e1.employee_id < e2.employee_id` y `e1.reports_to = m.employee_id`.",
    filtros: "Condición de desigualdad estricta en el `ON`.",
    proyeccion: "`empleado_1`, `empleado_2`, `manager`.",
    validacion: "En Northwind se forman exactamente 13 combinaciones únicas de parejas de subordinados bajo los 2 managers activos (Andrew Fuller y Steven Buchanan).",
    engine: [
      "**1. FROM employees e1 INNER JOIN employees e2:** Cruce sobre `reports_to` filtrado por `e1.employee_id < e2.employee_id`.",
      "**2. INNER JOIN employees m:** Se une con la ficha del manager sobre `e1.reports_to = m.employee_id`.",
      "**3. SELECT & ORDER BY:** Proyección y ordenamiento alfabético por manager y empleado."
    ]
  },
  33: {
    enunciado: "El equipo de auditoría territorial y recursos humanos necesita contrastar la asignación de personal comercial frente a los territorios geográficos. Se solicita listar todos los empleados y todos los territorios asignados, mostrando tanto a empleados sin territorios asignados (si los hubiera) como a territorios sin empleados asignados, utilizando un FULL OUTER JOIN.",
    analogia: "Es como cruzar la lista completa de guardias de seguridad con la lista completa de puertas de un edificio: quieres ver quién vigila qué puerta, pero también si hay guardias sin puerta asignada o puertas desprotegidas sin guardia.",
    concepto: "Un `FULL OUTER JOIN` combina los resultados de un `LEFT JOIN` y un `RIGHT JOIN`. Preserva todas las filas de ambas tablas, rellenando con `NULL` las columnas del lado opuesto cuando no existe coincidencia.",
    tip: "En `ORDER BY` con `FULL OUTER JOIN`, utiliza `NULLS LAST` para asegurar que las filas con valores nulos se ubiquen de forma consistente al final del reporte.",
    kpi: "Auditoría de cobertura y asignación de recursos en relaciones muchos a muchos (N:M).",
    fuentes: "Tablas `employees` (9 filas) y `employee_territories` (49 filas asignadas). Granularidad: 49 filas de asignación.",
    relaciones: "`employees.employee_id = employee_territories.employee_id`.",
    filtros: "Ninguno.",
    proyeccion: "`e.employee_id`, `empleado`, `et.territory_id`.",
    validacion: "En Northwind todos los 9 empleados tienen al menos un territorio asignado (49 tuplas en total).",
    engine: [
      "**1. FROM employees e FULL OUTER JOIN employee_territories et:** Se evalúa la coincidencia en `employee_id` preservando ambas tablas.",
      "**2. SELECT:** Se proyectan las columnas concatenadas.",
      "**3. ORDER BY e.employee_id NULLS LAST, et.territory_id NULLS LAST:** Ordenamiento con control de nulos."
    ]
  },
  34: {
    enunciado: "El área de calidad de datos y auditoría de cuentas necesita una conciliación total entre la base de clientes y el registro de órdenes. Se solicita listar el identificador del cliente, el nombre de la empresa, el identificador de orden y la fecha de la orden, mostrando absolutamente todos los clientes (hayan comprado o no) y todas las órdenes (incluso órdenes huérfanas si existieran), utilizando un FULL OUTER JOIN ordenado por identificador de cliente y de orden con NULLS LAST.",
    analogia: "Es como cruzar el padrón completo de ciudadanos con el registro de votos emitidos en una urna: quieres ver los ciudadanos que votaron, los que no votaron (clientes con 0 pedidos), y detectar si hay votos emitidos sin ciudadano registrado (órdenes huérfanas).",
    concepto: "El `FULL OUTER JOIN` entre `customers` y `orders` es la prueba reina de integridad referencial. Revela clientes inactivos con pedidos `NULL` y órdenes no asociadas con cliente `NULL`.",
    tip: "En Northwind canónico, existen exactamente 830 pedidos realizados por 89 clientes, más 2 clientes que jamás compraron ('FISSA' y 'PARIS'), totalizando exactamente 832 filas en el FULL JOIN.",
    kpi: "Auditoría de integridad referencial y conciliación 100% exhaustiva entre maestros y transacciones.",
    fuentes: "Tablas `customers` (91 filas) y `orders` (830 filas). Granularidad: Exactamente 832 filas.",
    relaciones: "`customers.customer_id = orders.customer_id` (FULL OUTER JOIN).",
    filtros: "Ninguno.",
    proyeccion: "`c.customer_id AS id_cliente`, `c.company_name`, `o.order_id`, `o.order_date`.",
    validacion: "El resultado debe arrojar exactamente 832 filas (830 pedidos asociados + 2 clientes con valores nulos en pedidos). Cero datos mock.",
    engine: [
      "**1. FROM customers c FULL OUTER JOIN orders o:** El motor ejecuta un `Hash Full Join` sobre `customer_id`.",
      "**2. Preservación:** Se preservan las 830 órdenes coincidentes y los 2 clientes sin órdenes ('FISSA' y 'PARIS').",
      "**3. SELECT:** Proyección de las 4 columnas.",
      "**4. ORDER BY c.customer_id NULLS LAST, o.order_id NULLS LAST:** Ordenamiento consistente de las 832 filas."
    ]
  },
  35: {
    enunciado: "El departamento de control de calidad y trazabilidad integral necesita reconstruir el camino completo de cada artículo despachado. Se solicita listar el identificador de orden, nombre del producto, nombre de la categoría, nombre de la empresa proveedora, fecha de la orden, cantidad y precio unitario, cruzando las 5 tablas maestras del flujo transaccional mediante INNER JOINs.",
    analogia: "Es como el código de barras de trazabilidad alimentaria: tomas un frasco de salsa de una caja despachada y puedes ver en qué fecha se vendió, a qué categoría pertenece, qué proveedor produjo la materia prima y a qué precio se comercializó.",
    concepto: "Un `INNER JOIN` de 5 tablas (`order_details` -> `products` -> `categories` -> `suppliers` -> `orders`) navega el grafo relacional uniendo claves primarias y foráneas para consolidar la vista analítica 360° del producto.",
    tip: "El orden de escritura de los `INNER JOIN` en SQL no altera el resultado final ni restringe al optimizador, quien reordena los joins basándose en las estadísticas de costos (`cost-based optimizer`).",
    kpi: "Trazabilidad completa de suministro, catálogo y despacho por línea de venta.",
    fuentes: "Tablas `order_details` (2,155 filas), `products`, `categories`, `suppliers`, `orders`. Granularidad: 2,155 filas.",
    relaciones: "Cadena de 4 uniones `INNER JOIN`.",
    filtros: "Ninguno.",
    proyeccion: "`od.order_id`, `p.product_name`, `c.category_name`, `s.company_name AS proveedor`, `o.order_date`, `od.quantity`, `od.unit_price`.",
    validacion: "La consulta debe retornar exactamente las 2,155 líneas de detalle históricas de Northwind.",
    engine: [
      "**1. FROM order_details:** Escaneo de las 2,155 tuplas base.",
      "**2. JOIN products:** Hash Join sobre `product_id` (77 productos).",
      "**3. JOIN categories:** Hash Join sobre `category_id` (8 categorías).",
      "**4. JOIN suppliers:** Hash Join sobre `supplier_id` (29 proveedores).",
      "**5. JOIN orders:** Hash Join sobre `order_id` (830 órdenes).",
      "**6. SELECT & ORDER BY od.order_id, p.product_name:** Proyección y ordenamiento final."
    ]
  },
  36: {
    enunciado: "La gerencia de operaciones y despacho logístico necesita auditar los envíos de los pedidos más recientes. Se solicita obtener el identificador del pedido, la fecha de la orden, el nombre del cliente, el nombre completo del empleado vendedor, el nombre de la empresa transportista (`shipper`) y el costo de flete, limitando la salida a los 20 pedidos más recientes mediante un JOIN de 4 tablas.",
    analogia: "Es como la hoja de ruta de una central de despacho donde ves qué cliente compró, qué ejecutivo cerró la venta, qué empresa de camiones transporta la carga y cuánto costó el flete.",
    concepto: "Cruza la tabla de hechos `orders` con tres tablas dimensionales satélite (`customers`, `employees`, `shippers`) en un diseño de esquema en estrella clásico.",
    tip: "El uso de `LIMIT 20` junto con `ORDER BY o.order_date DESC` permite al optimizador utilizar un algoritmo de `Top-N Heap Sort` en memoria sin necesidad de ordenar la tabla completa en disco.",
    kpi: "Auditoría de despacho de pedidos recientes y asignación de transportistas.",
    fuentes: "Tablas `orders` (830 filas), `customers`, `employees`, `shippers`. Granularidad: 20 filas acotadas.",
    relaciones: "`orders.customer_id = customers.customer_id`, `orders.employee_id = employees.employee_id`, `orders.ship_via = shippers.shipper_id`.",
    filtros: "`LIMIT 20` sobre orden cronológico inverso.",
    proyeccion: "`o.order_id`, `o.order_date`, `c.company_name AS cliente`, `e.first_name || ' ' || e.last_name AS empleado`, `s.company_name AS transportista`, `o.freight`.",
    validacion: "Los 20 registros devueltos corresponden a los pedidos de fechas más recientes (abril y mayo de 1998).",
    engine: [
      "**1. FROM orders o:** Escaneo de las 830 órdenes.",
      "**2. JOINs satélite:** Cruces con `customers`, `employees` y `shippers`.",
      "**3. ORDER BY o.order_date DESC:** Ordenamiento descendente por fecha.",
      "**4. LIMIT 20:** Corte de las primeras 20 tuplas."
    ]
  },
  37: {
    enunciado: "El departamento de auditoría interna de ventas necesita constatar la actividad de todos los empleados de la compañía. Se solicita listar el identificador de empleado, el nombre completo del empleado, el identificador de orden y la fecha de la orden, asegurando que todos los empleados figuren en el reporte incluso si alguno de ellos no tuviera pedidos asignados, utilizando un RIGHT JOIN.",
    analogia: "Es como tomar la lista de todos los empleados de la empresa (tabla de la derecha) y pegarle al lado los pedidos que cerraron. Aunque un empleado sea nuevo y no haya cerrado pedidos, su nombre permanece en la lista con campos de pedido en blanco.",
    concepto: "Un `RIGHT JOIN` preserva todas las filas de la tabla de la derecha (`employees`), emparejándolas con la tabla de la izquierda (`orders`). Es equivalente a invertir las tablas con un `LEFT JOIN`.",
    tip: "En la práctica profesional se suele preferir `LEFT JOIN` por legibilidad (leyendo de izquierda a derecha), pero dominar `RIGHT JOIN` es fundamental para entender la simetría del álgebra relacional.",
    kpi: "Monitoreo integral de asignación de pedidos sobre la totalidad del equipo de ventas.",
    fuentes: "Tablas `orders` (830 filas) y `employees` (9 filas). Granularidad: 830 filas (los 9 empleados registran pedidos).",
    relaciones: "`orders.employee_id = employees.employee_id` (RIGHT JOIN).",
    filtros: "Ninguno.",
    proyeccion: "`e.employee_id`, `e.first_name || ' ' || e.last_name AS empleado`, `o.order_id`, `o.order_date`.",
    validacion: "En Northwind todos los 9 empleados han procesado pedidos, resultando en exactamente 830 filas.",
    engine: [
      "**1. FROM orders o RIGHT JOIN employees e:** El motor preserva todas las tuplas de `employees`.",
      "**2. Emparejamiento:** Se asocian las 830 órdenes correspondientes.",
      "**3. SELECT & ORDER BY e.employee_id:** Proyección ordenada por identificador de empleado."
    ]
  },
  38: {
    enunciado: "El equipo de auditoría de integridad de catálogo necesita verificar la coherencia entre el nombre del producto y su categoría asignada. Se solicita listar el nombre del producto, el nombre de la categoría y el precio unitario, generando conceptualmente un producto cartesiano con CROSS JOIN y filtrando mediante la cláusula WHERE las tuplas donde category_id coincida.",
    analogia: "Es como colocar todas las fichas de productos en una fila horizontal y todas las fichas de categorías en una columna vertical para formar una cuadrícula gigante de todas las combinaciones posibles (77 × 8 = 616 combinaciones), y luego quedarte solo con las casillas donde la categoría de la ficha coincide con la categoría de la fila.",
    concepto: "El `CROSS JOIN` con filtro en `WHERE (p.category_id = c.category_id)` es la formulación relacional clásica equivalente al `INNER JOIN ... ON`. El optimizador de PostgreSQL reconoce esta equivalencia y lo transforma internamente en un `Hash Join` óptimo.",
    tip: "Nunca ejecutes un `CROSS JOIN` sin filtro sobre tablas grandes en producción, ya que generaría un producto cartesiano masivo ($N \\times M$) que saturaría la memoria del servidor.",
    kpi: "Demostración de equivalencia algebraica entre producto cartesiano filtrado e INNER JOIN.",
    fuentes: "Tablas `products` (77 filas) y `categories` (8 filas). Granularidad: 77 filas.",
    relaciones: "`CROSS JOIN` filtrado por `p.category_id = c.category_id`.",
    filtros: "`WHERE p.category_id = c.category_id`.",
    proyeccion: "`p.product_name`, `c.category_name`, `p.unit_price`.",
    validacion: "El resultado debe contener exactamente los 77 productos del catálogo.",
    engine: [
      "**1. FROM products p CROSS JOIN categories c:** Reconocimiento de la condición de unión en `WHERE`.",
      "**2. Optimización:** El optimizador reescribe el producto cartesiano como un `Hash Join` directo.",
      "**3. SELECT & ORDER BY c.category_name, p.product_name:** Proyección ordenada por categoría y producto."
    ]
  },
  39: {
    enunciado: "El equipo de auditoría comercial necesita examinar exclusivamente las ventas que gozaron de descuento promocional. Se solicita listar el identificador de pedido, la fecha de la orden, el identificador de producto y el porcentaje de descuento, uniendo orders y order_details mediante un JOIN con una condición compuesta en la cláusula ON que filtre en el cruce únicamente los registros con descuento mayor a cero.",
    analogia: "Es como abrir la puerta del almacén de pedidos y decir: 'Solo quiero que entren a la sala de revisión los detalles de órdenes que hayan tenido descuento aplicado (> 0)'. Los detalles a precio de lista se quedan afuera antes del cruce.",
    concepto: "Colocar un predicado en la cláusula `ON` (`AND od.discount > 0`) en un `INNER JOIN` filtra las filas de la tabla secundaria antes de la unión.",
    tip: "En un `INNER JOIN`, filtrar en el `ON` produce el mismo resultado lógico que filtrar en el `WHERE`. Sin embargo, en un `LEFT JOIN` la diferencia es crucial: en `ON` preserva la fila izquierda con `NULL`, en `WHERE` la descarta.",
    kpi: "Auditoría de transacciones con margen reducido por aplicación de descuentos.",
    fuentes: "Tablas `orders` (830 filas) y `order_details` (2,155 filas). Granularidad: 838 filas con descuento.",
    relaciones: "`orders.order_id = order_details.order_id AND od.discount > 0`.",
    filtros: "`od.discount > 0` en la cláusula `ON`.",
    proyeccion: "`o.order_id`, `o.order_date`, `od.product_id`, `od.discount`.",
    validacion: "En Northwind, de las 2,155 líneas de detalle, exactamente 838 tienen un descuento estrictamente superior a 0.",
    engine: [
      "**1. FROM orders o INNER JOIN order_details od:** Hash Join con predicado compuesto `o.order_id = od.order_id AND od.discount > 0`.",
      "**2. Filtrado temprano:** Se descartan las 1,317 líneas con descuento cero.",
      "**3. SELECT & ORDER BY od.discount DESC:** Proyección ordenada por porcentaje de descuento."
    ]
  },
  40: {
    enunciado: "El área de retención y fidelización de clientes requiere consultar el último pedido realizado por cada cliente mediante una subconsulta lateral por fila. Se solicita listar el identificador de cliente, nombre de la empresa, identificador del último pedido y fecha de ese último pedido, utilizando la cláusula CROSS JOIN LATERAL.",
    analogia: "Es como tener una fila de 91 clientes y contratar a un asistente para que tome la ficha de cada cliente en orden, vaya al archivo de pedidos, busque el pedido más reciente de ese cliente específico con `LIMIT 1`, y lo engrape a la ficha del cliente antes de pasar al siguiente.",
    concepto: "`JOIN LATERAL` permite a una subconsulta hacer referencia a columnas de tablas precedentes en la cláusula `FROM` (actuando como un `for each row` relacional). Es una de las capacidades más avanzadas y optimizadas de PostgreSQL.",
    tip: "Con `CROSS JOIN LATERAL`, si un cliente no tiene ningún pedido, la subconsulta retorna 0 filas y el cliente queda excluido. Para preservar clientes sin compras (como FISSA y PARIS), se usaría `LEFT JOIN LATERAL ... ON true`.",
    kpi: "Extracción del último evento transaccional por entidad (Top-1 Per Entity Pattern) mediante LATERAL.",
    fuentes: "Tablas `customers` (91 filas) y `orders` (830 filas). Granularidad: 89 filas (clientes con al menos 1 pedido).",
    relaciones: "`CROSS JOIN LATERAL (SELECT ... WHERE o.customer_id = c.customer_id ... LIMIT 1)`.",
    filtros: "`LIMIT 1` por cliente en la subconsulta lateral.",
    proyeccion: "`c.customer_id`, `c.company_name`, `ultimo_pedido.order_id`, `ultimo_pedido.order_date`.",
    validacion: "Retorna exactamente los 89 clientes que tienen pedidos históricos en Northwind.",
    engine: [
      "**1. FROM customers c:** Lectura de clientes.",
      "**2. Evaluación LATERAL:** Por cada fila de `c`, el motor ejecuta el subplan parametrizado en `orders` ordenando por `order_date DESC` y extrayendo 1 tupla.",
      "**3. Proyección & ORDER BY ultimo_pedido.order_date DESC:** Ordenamiento de los 89 clientes por fecha de compra más reciente."
    ]
  }
};

fs.writeFileSync('.agents/worker_intermedio_1/modules/block4_31_40.json', JSON.stringify(b4, null, 2), 'utf8');
console.log('Saved block 4 (Ex 31-40) JSON successfully.');
