const fs = require('fs');

const b5 = {
  41: {
    enunciado: "El departamento de catálogo y pricing necesita asignar un identificador secuencial único a cada artículo según su nivel de precio para una lista de precios oficial. Se solicita listar el nombre del producto, su precio unitario y un número de ranking secuencial consecutivo sin empates (1, 2, 3...) ordenado de mayor a menor precio mediante la función de ventana ROW_NUMBER().",
    analogia: "Es como una carrera de atletismo donde, aunque dos corredores crucen la meta en el mismo segundo, el cronómetro de alta precisión le asigna obligatoriamente la posición 1 al primero y la posición 2 al segundo para que no haya dos personas con el mismo número de turno.",
    concepto: "`ROW_NUMBER() OVER (ORDER BY unit_price DESC)` genera una secuencia entera estrictamente consecutiva (1, 2, 3...) sobre el conjunto particionado u ordenado, garantizando que cada fila tenga un identificador ordinal único.",
    tip: "A diferencia de `RANK()`, `ROW_NUMBER()` nunca genera números duplicados ni saltos en la numeración, lo que lo convierte en la herramienta perfecta para paginación y selección determinista de Top-1.",
    kpi: "Generación de índices ordinales deterministas para listas de precios y paginación.",
    fuentes: "Tabla `products` (77 filas, columnas `product_name`, `unit_price`). Granularidad: 77 filas.",
    relaciones: "Mono-tabla sobre `products`.",
    filtros: "Ninguno.",
    proyeccion: "`product_name`, `unit_price`, `ROW_NUMBER() OVER (ORDER BY unit_price DESC) AS ranking_secuencial`.",
    validacion: "El ranking cubre del 1 al 77 de forma estrictamente continua, encabezado por 'Côte de Blaye' ($263.50).",
    engine: [
      "**1. FROM products:** Escaneo de los 77 productos.",
      "**2. WINDOW (ROW_NUMBER):** El nodo `WindowAgg` ordena las 77 tuplas por `unit_price DESC` y numera secuencialmente del 1 al 77.",
      "**3. SELECT & ORDER BY:** Proyección final ordenada por `ranking_secuencial`."
    ]
  },
  42: {
    enunciado: "El comité de auditoría de precios por categoría necesita analizar la distribución de precios y el manejo de valores idénticos (empates) en cada sector del catálogo. Se solicita listar el identificador de categoría, el nombre del producto, el precio unitario y contrastar en dos columnas simultáneas el ranking con saltos (RANK) y el ranking sin saltos (DENSE_RANK), particionados por categoría y ordenados de mayor a menor precio.",
    analogia: "Es como premiar en una competencia escolar: si dos alumnos empatan en el 1er lugar con 100 puntos, con `RANK` (estilo olímpico) los dos reciben oro y el siguiente recibe bronce (puesto 3, saltando el 2). Con `DENSE_RANK`, los dos reciben oro y el siguiente recibe plata (puesto 2, sin saltos).",
    concepto: "`RANK()` asigna el mismo rango a valores iguales y deja un hueco en la secuencia por cada empate (`1, 1, 3`). `DENSE_RANK()` asigna el mismo rango a los empates pero mantiene la secuencia numérica compacta sin huecos (`1, 1, 2`).",
    tip: "Usa `DENSE_RANK()` cuando quieras obtener, por ejemplo, los '3 precios más altos distintos' sin que los empates consuman posiciones de ranking.",
    kpi: "Análisis comparativo de algoritmos de ranking estadístico sobre particiones de categoría.",
    fuentes: "Tabla `products` (77 filas, columnas `category_id`, `product_name`, `unit_price`). Granularidad: 77 filas.",
    relaciones: "Mono-tabla sobre `products`.",
    filtros: "Ninguno.",
    proyeccion: "`category_id`, `product_name`, `unit_price`, `rango_con_saltos`, `rango_sin_saltos`.",
    validacion: "Las 77 filas se evalúan dentro de sus 8 particiones de categoría.",
    engine: [
      "**1. FROM products:** Escaneo de los 77 productos.",
      "**2. WINDOW (PARTITION BY category_id ORDER BY unit_price DESC):** Se ordenan las tuplas dentro de cada categoría y se evalúan simultáneamente `RANK()` y `DENSE_RANK()`.",
      "**3. SELECT & ORDER BY category_id, rango_con_saltos:** Proyección ordenada."
    ]
  },
  43: {
    enunciado: "La gerencia de comercialización necesita seleccionar una muestra de los 3 productos más caros de cada categoría para un catálogo impreso de lujo. Se solicita listar el identificador de categoría, el nombre de la categoría, el nombre del producto, el precio unitario y su posición de ranking dentro de la categoría, utilizando una CTE con ROW_NUMBER() particionado por categoría y filtrando en la consulta principal los registros con rn <= 3.",
    analogia: "Es como ir a cada departamento de la tienda, ordenar los artículos por precio, tomar los 3 más caros de cada estante y guardarlos en una caja para armar el escaparate principal de la tienda.",
    concepto: "El patrón Top-N por grupo no se puede resolver en una sola pasada con un simple `WHERE ROW_NUMBER() <= 3` (porque las funciones de ventana se evalúan en la fase 5 después del `WHERE` de la fase 2). Requiere una CTE o subconsulta para materializar el número de fila y luego filtrar en la consulta exterior.",
    tip: "Recuerda la regla de oro: las funciones de ventana NUNCA pueden colocarse en las cláusulas `WHERE` ni `HAVING` del mismo nivel de consulta.",
    kpi: "Patrón analítico maestro: Top-N por Grupo (Selección de los 3 productos de mayor precio por categoría).",
    fuentes: "Tablas `products` (77 filas) y `categories` (8 filas). Granularidad: 24 filas (8 categorías × 3 productos).",
    relaciones: "`CTE.category_id = categories.category_id`.",
    filtros: "`WHERE rp.rn <= 3` en la consulta exterior.",
    proyeccion: "`rp.category_id`, `c.category_name`, `rp.product_name`, `rp.unit_price`, `rp.rn`.",
    validacion: "Exactamente 24 filas (3 productos por cada una de las 8 categorías).",
    engine: [
      "**1. CTE (ranked_products):** Escanea `products`, particiona por `category_id`, ordena por `unit_price DESC` y numera las filas con `ROW_NUMBER()`.",
      "**2. FROM & JOIN:** Une la CTE con `categories` sobre `category_id`.",
      "**3. WHERE rp.rn <= 3:** Filtra únicamente las posiciones 1, 2 y 3 de cada categoría.",
      "**4. SELECT & ORDER BY rp.category_id, rp.rn:** Salida ordenada."
    ]
  },
  44: {
    enunciado: "El equipo de fidelización y análisis del ciclo de vida del cliente (LTV) necesita medir el intervalo de tiempo entre compras consecutivas para cada cliente. Se solicita listar el identificador de cliente, el identificador de orden, la fecha del pedido actual, la fecha del pedido inmediatamente anterior (utilizando LAG()) y la diferencia en días entre ambos pedidos, particionado por cliente y ordenado cronológicamente.",
    analogia: "Es como mirar por el espejo retrovisor mientras conduces: vas avanzando en la pista (pedido actual) pero miras hacia atrás para ver cuánto tiempo ha pasado desde el hito anterior (pedido previo del mismo cliente).",
    concepto: "`LAG(columna, 1) OVER (PARTITION BY cliente ORDER BY fecha)` accede a la fila anterior dentro de la misma partición. Al restar `order_date - LAG(order_date, 1)`, PostgreSQL calcula la diferencia exacta de días entre dos fechas.",
    tip: "Para la primera orden de cada cliente, `LAG()` retorna `NULL` porque no existe un evento previo en la partición, resultando en un valor `NULL` en la columna de diferencia de días.",
    kpi: "Cadencia de compra y frecuencia inter-compra (Days Between Orders) para modelos de churn.",
    fuentes: "Tabla `orders` (830 filas, columnas `customer_id`, `order_id`, `order_date`). Granularidad: 830 filas.",
    relaciones: "Mono-tabla sobre `orders` con particionamiento analítico.",
    filtros: "Ninguno.",
    proyeccion: "`customer_id`, `order_id`, `order_date`, `fecha_pedido_anterior`, `dias_entre_pedidos`.",
    validacion: "Las 830 órdenes quedan particionadas en 89 clientes activos.",
    engine: [
      "**1. FROM orders:** Lectura de las 830 órdenes.",
      "**2. WINDOW (LAG):** El motor particiona por `customer_id`, ordena por `order_date` y desplaza un puntero hacia la tupla anterior.",
      "**3. SELECT:** Se evalúa la resta de fechas y se proyectan las columnas.",
      "**4. ORDER BY customer_id, order_date:** Salida cronológica por cliente."
    ]
  },
  45: {
    enunciado: "El departamento de planificación de inventario y retención proactiva necesita anticipar la siguiente fecha de compra de los clientes. Se solicita listar el identificador de cliente, identificador de orden, fecha de orden y la fecha del pedido inmediatamente posterior (utilizando LEAD()) particionado por cliente y ordenado cronológicamente.",
    analogia: "Es como mirar hacia adelante por el parabrisas del auto: te sitúas en la compra actual pero consultas el registro del futuro próximo para saber exactamente cuándo volverá a comprar ese mismo cliente.",
    concepto: "`LEAD(columna, 1) OVER (PARTITION BY cliente ORDER BY fecha)` accede a la fila siguiente dentro de la partición. Para el último pedido de cada cliente, `LEAD()` retorna `NULL` al no existir compras posteriores.",
    tip: "`LEAD()` permite identificar fácilmente la última compra de cada cliente: si `fecha_proximo_pedido IS NULL`, esa fila representa el pedido más reciente del cliente.",
    kpi: "Detección de puntos finales de compra y cálculo de lead time hacia el siguiente evento.",
    fuentes: "Tabla `orders` (830 filas). Granularidad: 830 filas.",
    relaciones: "Mono-tabla sobre `orders`.",
    filtros: "Ninguno.",
    proyeccion: "`customer_id`, `order_id`, `order_date`, `fecha_proximo_pedido`.",
    validacion: "Las 830 órdenes quedan analizadas; el último pedido de cada cliente muestra `NULL` en `fecha_proximo_pedido`.",
    engine: [
      "**1. FROM orders:** Escaneo de las 830 tuplas.",
      "**2. WINDOW (LEAD):** Particionamiento por `customer_id` y lookahead de 1 fila hacia adelante.",
      "**3. SELECT & ORDER BY customer_id, order_date:** Proyección y ordenamiento."
    ]
  },
  46: {
    enunciado: "La dirección financiera requiere un informe de evolución mensual de ingresos y facturación acumulada (Running Total). Se solicita calcular mediante una CTE la facturación neta mensual y, en la consulta principal, calcular el total de ingresos acumulados mes a mes a lo largo del tiempo utilizando la función SUM() OVER con el marco de ventana ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
    analogia: "Es como llevar una alcancía donde cada fin de mes depositas las ganancias netas de ese mes (`ingresos_mes`) y anotas en tu libreta el saldo total acumulado que hay en la alcancía sumando todos los depósitos desde el inicio de los tiempos hasta el mes actual (`ingresos_acumulados`).",
    concepto: "`SUM() OVER (ORDER BY mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` calcula una suma acumulativa continua. El marco explícito de ventana asegura que se sumen todas las filas desde la primera del conjunto hasta la fila actual inclusive.",
    tip: "En PostgreSQL, cuando usas `SUM() OVER (ORDER BY columna)`, el marco por defecto es `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Especificar `ROWS BETWEEN` es más eficiente y evita problemas si existieran valores repetidos en la columna de orden.",
    kpi: "Crecimiento acumulado de facturación (Cumulative Revenue / Running Total) mes a mes.",
    fuentes: "Tablas `orders` y `order_details` (23 meses de actividad entre julio de 1996 y mayo de 1998). Granularidad: 23 filas mensuales.",
    relaciones: "Join entre `orders` y `order_details` en la CTE.",
    filtros: "Ninguno.",
    proyeccion: "`periodo_mes`, `ingresos_mes`, `ingresos_acumulados`.",
    validacion: "En mayo de 1998 la facturación acumulada total de Northwind alcanza los $1,265,793.22 USD.",
    engine: [
      "**1. CTE (monthly_revenue):** Agrupa los 830 pedidos en 23 meses (`TO_CHAR(o.order_date, 'YYYY-MM')`) y calcula `ingresos_mes`.",
      "**2. WINDOW (SUM OVER):** El nodo `WindowAgg` recorre los 23 meses acumulando la suma progresiva de ingresos.",
      "**3. SELECT & ORDER BY periodo_mes:** Proyección cronológica de los 23 meses."
    ]
  },
  47: {
    enunciado: "El departamento de pricing y posicionamiento de catálogo necesita evaluar la dispersión de precios de cada producto respecto a su sector. Se solicita listar el nombre del producto, el identificador de categoría, el precio unitario, el precio promedio de su categoría (utilizando AVG() OVER) y la desviación monetaria exacta (precio unitario menos el promedio de la categoría), ordenados por categoría y precio.",
    analogia: "Es como comparar la estatura de un basquetbolista no con la población general, sino con el promedio de su propio equipo: sabes exactamente cuántos centímetros está por encima o por debajo de la media de sus compañeros.",
    concepto: "`AVG(unit_price) OVER (PARTITION BY category_id)` calcula la media de la categoría para cada fila SIN colapsar las 77 filas del catálogo en 8 grupos. Permite comparar métricas de grano fino contra métricas de grano agregado en una sola consulta.",
    tip: "Las funciones de ventana permiten mezclar atributos de nivel de fila (`unit_price`) con agregaciones de grupo (`AVG OVER`) sin necesidad de realizar costosos joins con subconsultas agregadas.",
    kpi: "Desviación de precios respecto a la media del segmento (Price Dispersion Benchmark).",
    fuentes: "Tabla `products` (77 filas, columnas `product_name`, `category_id`, `unit_price`). Granularidad: 77 filas.",
    relaciones: "Mono-tabla sobre `products` con ventana particionada.",
    filtros: "Ninguno.",
    proyeccion: "`product_name`, `category_id`, `unit_price`, `promedio_categoria`, `desviacion_promedio`.",
    validacion: "Las 77 filas preservan su identidad y reflejan la desviación exacta (+ o -) frente a su categoría.",
    engine: [
      "**1. FROM products:** Escaneo de los 77 productos.",
      "**2. WINDOW (AVG OVER PARTITION BY category_id):** El motor particiona en 8 categorías y calcula la media de cada una.",
      "**3. SELECT:** Se evalúa la resta aritmética `unit_price - promedio` y se redondea.",
      "**4. ORDER BY category_id, unit_price:** Salida ordenada."
    ]
  },
  48: {
    enunciado: "El equipo de reporting comercial necesita mostrar en cada línea de producto los valores extremos de su categoría para referencia rápida. Se solicita listar el identificador de categoría, el nombre del producto, el precio unitario, el producto más caro de la categoría (utilizando FIRST_VALUE()) y el precio más barato de la categoría (utilizando LAST_VALUE() con el marco de ventana completo ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING).",
    analogia: "Es como imprimir una etiqueta de precio donde, además del precio de ese producto, figura el artículo más caro y el precio más barato de toda esa sección para que el comprador sepa en qué parte de la gama se encuentra.",
    concepto: "`FIRST_VALUE()` extrae el primer valor de la partición ordenada. `LAST_VALUE()` extrae el último; sin embargo, para que `LAST_VALUE()` vea el final de la partición, es OBLIGATORIO definir el frame `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, ya que por defecto el frame termina en `CURRENT ROW`.",
    tip: "Esta es una de las trampas más famosas de las entrevistas SQL: si no especificas el marco completo en `LAST_VALUE()`, retornará el valor de la fila actual (`CURRENT ROW`) en lugar del último valor real de la partición.",
    kpi: "Benchmark de extremos de banda de precios (Min/Max Boundary Framing) por categoría.",
    fuentes: "Tabla `products` (77 filas). Granularidad: 77 filas.",
    relaciones: "Mono-tabla sobre `products`.",
    filtros: "Ninguno.",
    proyeccion: "`category_id`, `product_name`, `unit_price`, `producto_mas_caro`, `precio_mas_barato`.",
    validacion: "Las 77 filas reflejan el producto líder y el precio piso de sus respectivas 8 categorías.",
    engine: [
      "**1. FROM products:** Escaneo de los 77 productos.",
      "**2. WINDOW (FIRST_VALUE / LAST_VALUE):** Evaluación de extremos con frame expandido a toda la partición.",
      "**3. SELECT & ORDER BY category_id, unit_price DESC:** Proyección ordenada."
    ]
  },
  49: {
    enunciado: "El departamento de fidelización y segmentación de clientes (CRM) necesita clasificar a toda la cartera de clientes en 4 cuartiles equilibrados según su nivel de compras históricas. Se solicita listar el identificador de cliente, nombre de la empresa, total de pedidos realizados y el cuartil asignado (1 = Top 25% más activo, 4 = 25% menos activo o inactivo), utilizando una CTE con LEFT JOIN y la función de ventana NTILE(4), ordenados por cuartil y volumen de pedidos.",
    analogia: "Es como dividir a los 91 clientes en 4 grupos iguales de aproximadamente 23 personas cada uno: los clientes más leales van a la Clase Platino (Cuartil 1), los siguientes a la Clase Oro (Cuartil 2), luego a la Clase Plata (Cuartil 3) y los menos activos a la Clase Bronce (Cuartil 4).",
    concepto: "`NTILE(4) OVER (ORDER BY total_pedidos DESC)` divide el conjunto ordenado en 4 cubetas numéricas lo más homogéneas posible. En un universo de 91 clientes, asigna 23 clientes a los cuartiles 1, 2 y 3, y 22 clientes al cuartil 4 ($23 \\times 3 + 22 = 91$).",
    tip: "El uso de `LEFT JOIN` en la CTE asegura que los clientes con 0 pedidos (como 'FISSA' y 'PARIS') no se pierdan y se ubiquen correctamente en el Cuartil 4 de inactivos.",
    kpi: "Segmentación RFM (Dimensión Frequency / Cuartiles de Fidelidad) sobre el 100% de la cartera de clientes.",
    fuentes: "Tablas `customers` (91 filas) y `orders` (830 filas). Granularidad: Exactamente 91 filas.",
    relaciones: "`customers c LEFT JOIN orders o ON c.customer_id = o.customer_id`.",
    filtros: "Ninguno (cobertura total de 91 clientes).",
    proyeccion: "`customer_id`, `company_name`, `total_pedidos`, `NTILE(4) OVER (...) AS cuartil`.",
    validacion: "El resultado debe listar exactamente 91 clientes (Q1: 23, Q2: 23, Q3: 23, Q4: 22). Cero registros mock.",
    engine: [
      "**1. CTE (customer_orders):** Left Join entre `customers` (91) y `orders` (830), agrupando por cliente para contar `COUNT(o.order_id)`.",
      "**2. WINDOW (NTILE):** El nodo `WindowAgg` calcula el tamaño total (91 filas), ordena por `total_pedidos DESC` y distribuye los 4 cuartiles.",
      "**3. SELECT & ORDER BY cuartil, total_pedidos DESC:** Salida ordenada por cuartil y volumen."
    ]
  },
  50: {
    enunciado: "El área de auditoría de rentabilidad y promociones necesita calcular la progresión acumulada de unidades vendidas exclusivamente bajo condiciones de descuento para cada producto. Se solicita listar el identificador de orden, identificador de producto, cantidad de unidades vendidas, descuento aplicado y la suma acumulada de unidades vendidas con descuento (utilizando SUM(quantity) FILTER (WHERE discount > 0) OVER), particionado por producto y ordenado por pedido.",
    analogia: "Es como un podómetro de ofertas en la fábrica: cada vez que sale una caja con descuento, el podómetro de ese producto suma las unidades de esa caja al contador acumulado; si la caja se vendió a precio regular sin descuento, el podómetro no se mueve y mantiene la cuenta acumulada previa.",
    concepto: "Combina funciones de ventana analíticas con la cláusula `FILTER (WHERE discount > 0)`. Evalúa la suma acumulada de una ventana exclusivamente sobre aquellas filas que satisfacen el predicado de filtro, preservando todas las filas de la tabla.",
    tip: "Esta sintaxis `SUM(...) FILTER (WHERE ...) OVER (...)` es una característica de élite de PostgreSQL que evita tener que escribir expresiones `CASE` farragosas dentro de las funciones de ventana.",
    kpi: "Seguimiento acumulativo de volumen colocado bajo promociones por producto (Promotional Unit Volume Velocity).",
    fuentes: "Tabla `order_details` (2,155 filas, columnas `order_id`, `product_id`, `quantity`, `discount`). Granularidad: 2,155 filas.",
    relaciones: "Mono-tabla sobre `order_details` con ventana analítica particionada.",
    filtros: "Filtro condicional dentro de la ventana mediante `FILTER`.",
    proyeccion: "`order_id`, `product_id`, `quantity`, `discount`, `unidades_con_descuento_acumuladas`.",
    validacion: "Las 2,155 líneas de detalle reflejan el acumulador condicional por producto a lo largo de los pedidos.",
    engine: [
      "**1. FROM order_details:** Escaneo de las 2,155 tuplas.",
      "**2. WINDOW (SUM FILTER OVER):** Particionamiento por `product_id`, ordenamiento por `order_id` y acumulación selectiva de tuplas con `discount > 0`.",
      "**3. SELECT & ORDER BY product_id, order_id:** Proyección final ordenada."
    ]
  }
};

fs.writeFileSync('.agents/worker_intermedio_1/modules/block5_41_50.json', JSON.stringify(b5, null, 2), 'utf8');
console.log('Saved block 5 (Ex 41-50) JSON successfully.');
