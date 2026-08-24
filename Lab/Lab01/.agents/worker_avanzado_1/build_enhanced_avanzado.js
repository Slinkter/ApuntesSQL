const fs = require('fs');
const { execSync } = require('child_process');

console.log('Building enhanced 3.avanzado.md...');

const rawContent = fs.readFileSync('2.Ejercicios/3.avanzado.md', 'utf8').replace(/\r\n/g, '\n');
const sections = rawContent.split(/\n## Ejercicio /);
const headerText = sections[0].trim();

// Mental models mapping for all 50 exercises
const mentalModels = {
  1: {
    negocio: 'Identificar a los clientes más valiosos por su Valor de Vida del Cliente (LTV - Lifetime Value) para diseñar programas de fidelización VIP.',
    fuentes: 'Tablas `orders` (830 filas, PK: `order_id`) y `order_details` (2,155 filas, PK compuesta: `order_id, product_id`) para métricas de compras, junto a `customers` (91 filas, PK: `customer_id`) para nombres de empresa.',
    relaciones: '`orders` $\\to$ `order_details` vía `order_id` (`INNER JOIN`), y la CTE resultante $\\to$ `customers` vía `customer_id` (`INNER JOIN`).',
    filtros: 'No hay filtros excluyentes previos; se agrupan las ventas y pedidos por `customer_id` en la CTE (`GROUP BY o.customer_id`).',
    proyeccion: '`company_name`, `total_gastado` (redondeado a 2 decimales), `num_pedidos`, `ticket_promedio` (usando `NULLIF` para evitar división por cero). Ordenado por `total_gastado DESC` y limitado a los 10 primeros.',
    validacion: 'Verificar que ningún `ticket_promedio` sea nulo ni negativo, y que la suma de ventas aplique el descuento `(1 - discount)` con exactitud matemática.'
  },
  2: {
    negocio: 'Evaluar la rentabilidad mensual contrastando los ingresos brutos generados contra los costos logísticos de flete pagados.',
    fuentes: '`orders` y `order_details`. Granularidad: órdenes individuales y detalles de producto, agregados a nivel de mes fiscal.',
    relaciones: 'CTE 1 (`ingresos_mensuales`) calcula ventas desde `orders` y `order_details`. CTE 2 (`fletes_mensuales`) calcula fletes desde `orders`. Ambas se combinan vía `mes` (`LEFT JOIN`).',
    filtros: 'Agrupación temporal mediante `DATE_TRUNC(\'month\', order_date)`.',
    proyeccion: '`mes`, `ingresos`, `flete`, `ingreso_neto` (ingresos - flete) y `pct_flete` (porcentaje de flete sobre ingresos). Ordenado cronológicamente por `mes ASC`.',
    validacion: 'Asegurar el uso de `COALESCE` en costos de flete y `NULLIF` en el denominador para proteger el cálculo de porcentajes ante meses sin ventas.'
  },
  3: {
    negocio: 'Medir la productividad del equipo de ventas calculando ingresos totales, pedidos gestionados y ticket promedio por representante comercial.',
    fuentes: '`employees` (9 empleados), `orders` (830 órdenes) y `order_details` (2,155 líneas de venta).',
    relaciones: 'CTE `metricas_empleados` une `orders` y `order_details` por `order_id`. Consulta externa une la CTE con `employees` vía `employee_id`.',
    filtros: 'Agrupación por `employee_id`. Se utiliza el hint `AS MATERIALIZED` para forzar la materialización previa de agregaciones pesadas.',
    proyeccion: 'Nombre completo (`first_name || \' \' || last_name`), `title`, `total_ventas`, `total_pedidos`, `ticket_promedio`. Ordenado por `total_ventas DESC`.',
    validacion: 'Validar que los 9 empleados activos aparezcan reflejados y que los totales de ventas concuerden con las cifras globales de la compañía.'
  },
  4: {
    negocio: 'Obtener el historial reciente de compras extrayendo los últimos 3 pedidos de cada cliente para seguimiento comercial.',
    fuentes: '`customers` (91 clientes) y `orders` (830 pedidos). Granularidad: pedidos individuales numerados por cliente.',
    relaciones: 'La CTE enumera pedidos usando `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC)` con `AS NOT MATERIALIZED`. La consulta principal une con `customers` vía `customer_id`.',
    filtros: 'Filtro en consulta principal: `po.rn <= 3` para retener únicamente los 3 pedidos más recientes por cliente.',
    proyeccion: '`company_name`, `order_id`, `order_date`, `freight`. Ordenado por `company_name ASC, order_date DESC`.',
    validacion: 'Confirmar que ningún cliente tenga más de 3 filas en el resultado final y que los clientes sin pedidos (`FISSA`, `PARIS`) no aparezcan en el INNER JOIN.'
  },
  5: {
    negocio: 'Desglosar el rendimiento trimestral de ventas por categoría en un solo barrido de tabla para análisis de estacionalidad.',
    fuentes: '`categories`, `products`, `orders`, `order_details`. Granularidad: líneas de pedido clasificadas por categoría y trimestre.',
    relaciones: '`categories` $\\to$ `products` $\\to$ `order_details` $\\to$ `orders` mediante sus respectivas claves foráneas.',
    filtros: 'Filtro global `WHERE o.order_date >= \'1997-01-01\' AND o.order_date < \'1998-01-01\'`. Agregaciones condicionales usando `FILTER (WHERE EXTRACT(QUARTER FROM o.order_date) = N)`.',
    proyeccion: '`category_name`, `ventas_totales`, `q1_ventas`, `q2_ventas`, `q3_ventas`, `q4_ventas`. Ordenado por `ventas_totales DESC`.',
    validacion: 'Comprobar matemáticamente que la suma de `q1 + q2 + q3 + q4` coincida exactamente con `ventas_totales` de cada categoría en 1997.'
  },
  6: {
    negocio: 'Detectar productos estancados en inventario sin movimiento en los últimos 90 días del histórico para liquidación o promociones.',
    fuentes: '`products`, `categories`, `orders`, `order_details`. Granularidad: catálogo de productos activos vs órdenes recientes.',
    relaciones: 'CTE `fecha_maxima` obtiene la fecha límite del dataset (`MAX(order_date)`). Consulta principal usa `NOT EXISTS` correlacionado contra `orders` y `order_details`.',
    filtros: '`p.discontinued = 0` y `NOT EXISTS (SELECT 1 FROM orders ... WHERE order_date >= fecha_corte)`.',
    proyeccion: '`product_id`, `product_name`, `category_name`, `unit_price`, `units_in_stock`. Ordenado por `units_in_stock DESC`.',
    validacion: 'Verificar que ningún producto listado tenga pedidos con fecha dentro de la ventana de 90 días respecto al máximo global del dataset.'
  },
  7: {
    negocio: 'Optimizar la gestión de almacén identificando productos cuyo stock disponible sea insuficiente según el umbral de reorden y unidades en pedido.',
    fuentes: '`products` (77 productos) y `suppliers` (29 proveedores).',
    relaciones: '`products` $\\to$ `suppliers` vía `supplier_id` (`INNER JOIN`).',
    filtros: '`p.discontinued = 0` y condición de criticidad `p.units_in_stock + p.units_on_order <= p.reorder_level`.',
    proyeccion: '`product_name`, `company_name` (proveedor), `units_in_stock`, `units_on_order`, `reorder_level`, `deficit_unidades`, `accion_sugerida` con `CASE`. Ordenado por `deficit_unidades DESC`.',
    validacion: 'Comprobar que solo aparezcan productos activos y que el déficit refleje fielmente la fórmula `reorder_level - (units_in_stock + units_on_order)`.'
  },
  8: {
    negocio: 'Auditar el catálogo de base de datos (`pg_stat_user_tables`) para identificar tablas críticas que carezcan de estadísticas frescas de autovacuum o analyze.',
    fuentes: '`pg_stat_user_tables` del catálogo interno de PostgreSQL. Granularidad: una fila por tabla de usuario en el esquema actual.',
    relaciones: 'CTE `analisis_tablas` extrae métricas de actividad (`n_live_tup`, `n_dead_tup`, `last_analyze`, `last_autoanalyze`). Consulta principal proyecta diagnóstico.',
    filtros: '`schemaname = \'public\'` y umbral de evaluación de tuplas muertas o modificaciones sin analizar.',
    proyeccion: '`relname`, `n_live_tup`, `n_dead_tup`, `pct_dead`, `last_analyze`, `estado_estadisticas`, `recomendacion`. Ordenado por `n_dead_tup DESC`.',
    validacion: 'Reconocer que los valores exactos de catálogo varían según el uso en tiempo de ejecución de la instancia PostgreSQL.'
  },
  9: {
    negocio: 'Ejecutar una transferencia atómica de unidades de inventario entre dos productos relacionados garantizando consistencia transaccional.',
    fuentes: 'Tabla `products`. Granularidad: registros de productos origen y destino modificados.',
    relaciones: 'CTE `descontar_origen` ejecuta `UPDATE` con `RETURNING` sobre el producto origen. Consulta principal ejecuta `UPDATE` sobre el producto destino sumando las unidades.',
    filtros: 'Filtro por `product_id` específico y validación de stock disponible suficiente (`units_in_stock >= 10`).',
    proyeccion: '`producto_origen`, `producto_destino`, `unidades_transferidas`, `nuevo_stock_origen`, `nuevo_stock_destino`.',
    validacion: 'Asegurar que la suma total de unidades entre ambos productos se mantenga constante antes y después de la transacción.'
  },
  10: {
    negocio: 'Procesar una carga incremental de clientes (UPSERT) insertando nuevos registros y actualizando datos de contacto en caso de colisión de clave primaria.',
    fuentes: 'Tabla `customers` y lote de datos entrantes definido en la CTE `datos_nuevos` vía `VALUES`.',
    relaciones: '`INSERT INTO customers ... ON CONFLICT (customer_id) DO UPDATE SET ... RETURNING ...`.',
    filtros: 'Detección automática de conflicto sobre la clave primaria `customer_id`.',
    proyeccion: '`customer_id`, `company_name`, `fue_insertado` evaluado mediante la expresión del sistema `(xmax = 0)`.',
    validacion: 'Comprobar que los nuevos clientes arrojen `fue_insertado = true` y los existentes arrojen `fue_insertado = false` con sus campos actualizados.'
  },
  11: {
    negocio: 'Construir el organigrama jerárquico completo de la empresa calculando el nivel organizacional de cada empleado desde el CEO.',
    fuentes: 'Tabla `employees` (9 empleados, auto-referencia en `reports_to` hacia `employee_id`).',
    relaciones: 'Recursión jerárquica: Término ancla busca a la dirección general (`reports_to IS NULL`). Término recursivo une la CTE con `employees` vía `e.reports_to = o.employee_id`.',
    filtros: 'Ancla: `reports_to IS NULL` (nivel 1). Recursión: progresa sumando `nivel + 1` hasta agotar subordinados.',
    proyeccion: '`employee_id`, `nombre_completo`, `title`, `nivel_jerarquico`, `ruta_jerarquica`. Ordenado por `nivel_jerarquico ASC, employee_id ASC`.',
    validacion: 'Verificar que Andrew Fuller aparezca en nivel 1 y que todos los 9 empleados estén correctamente vinculados en el árbol sin ciclos.'
  },
  12: {
    negocio: 'Listar todos los subordinados directos e indirectos bajo la línea de mando de un gerente específico (Andrew Fuller, ID=2).',
    fuentes: 'Tabla `employees`. Granularidad: subordinados en cualquier nivel de profundidad bajo el ID del gerente.',
    relaciones: 'Ancla: empleados con `reports_to = 2`. Recursión: empleados cuyos `reports_to` coincidan con los `employee_id` de la iteración previa.',
    filtros: 'Ancla filtrada por `reports_to = 2`.',
    proyeccion: '`employee_id`, `nombre_subordinado`, `cargo`, `jefe_inmediato`, `distancia_jerarquica`. Ordenado por `distancia_jerarquica, employee_id`.',
    validacion: 'Confirmar que no se incluya al propio gerente en el resultado y que se recuperen exactamente los 8 subordinados de la compañía.'
  },
  13: {
    negocio: 'Generar una dimensión de calendario fiscal continua identificando fines de semana y días laborables para cruces de ventas sin huecos temporales.',
    fuentes: 'Generación sintética mediante `WITH RECURSIVE` o `generate_series` de fechas.',
    relaciones: 'Recursión temporal: ancla con fecha inicial (`1998-01-01`), recursión sumando 1 día hasta fecha final (`1998-12-31`).',
    filtros: 'Condición de parada: `fecha + INTERVAL \'1 day\' <= \'1998-12-31\'`.',
    proyeccion: '`fecha`, `año`, `trimestre`, `mes_nombre`, `dia_semana`, `es_fin_de_semana`, `es_dia_laborable`. Ordenado cronológicamente.',
    validacion: 'Validar que el calendario contenga exactamente 365 días en 1998 y que los sábados (6) y domingos (0) estén correctamente clasificados.'
  },
  14: {
    negocio: 'Calcular el volumen acumulado de ventas gestionado por cada gerente incluyendo su propia facturación y la de toda su línea de subordinados.',
    fuentes: '`employees`, `orders`, `order_details`. Granularidad: ventas agregadas por empleado y propagadas ascendentemente en el organigrama.',
    relaciones: 'CTE 1 calcula ventas individuales por empleado. CTE recursiva propaga y acumula ventas desde las hojas del árbol hacia la raíz.',
    filtros: 'Recursión sobre jerarquía de empleados combinada con agregación de ventas.',
    proyeccion: '`employee_id`, `nombre_completo`, `ventas_propias`, `ventas_equipo_total`, `porcentaje_contribucion`.',
    validacion: 'Comprobar que para el CEO (`Andrew Fuller`), las ventas totales de equipo representen el 100% de la facturación histórica de la empresa.'
  },
  15: {
    negocio: 'Recorrer el grafo de territorios comerciales asignados a los equipos de ventas por región geográfica.',
    fuentes: '`territories`, `region`, `employee_territories`, `employees`. Granularidad: rutas de asignación de territorios.',
    relaciones: 'Término ancla selecciona territorios base; término recursivo expande territorios adyacentes o de la misma región.',
    filtros: 'Filtro por territorio inicial y delimitación de profundidad de grafo.',
    proyeccion: '`territory_id`, `territory_description`, `region_description`, `nivel_cobertura`, `ruta_expansion`.',
    validacion: 'Asegurar que el recorrido en grafo no genere duplicados cíclicos y respete la integridad territorial.'
  },
  16: {
    negocio: 'Trazar la ruta jerárquica ascendente (de abajo hacia arriba) desde un empleado operativo hasta la máxima autoridad ejecutiva.',
    fuentes: 'Tabla `employees`. Granularidad: cadena de supervisores directos.',
    relaciones: 'Ancla selecciona al empleado de partida (`Nancy Davolio`, ID=1). Recursión une `e.employee_id = o.reports_to` hacia arriba.',
    filtros: 'Ancla `employee_id = 1`. Condición de parada cuando `reports_to` es NULL.',
    proyeccion: '`paso`, `employee_id`, `nombre_empleado`, `title`, `superior_directo`. Ordenado por `paso ASC`.',
    validacion: 'Verificar que la secuencia de mando termine en Andrew Fuller (CEO) con `superior_directo = \'Nadie (Dirección General)\'`.'
  },
  17: {
    negocio: 'Construir el organigrama a partir de múltiples gerentes regionales en paralelo de forma eficiente en un solo pase recursivo.',
    fuentes: 'Tabla `employees`. Granularidad: ramas organizacionales concurrentes.',
    relaciones: 'Término ancla selecciona todos los gerentes de primer nivel (`reports_to = 2`). Término recursivo desciende por sus respectivos equipos.',
    filtros: 'Ancla `reports_to = 2`.',
    proyeccion: '`gerente_raiz`, `employee_id`, `nombre_empleado`, `title`, `nivel_en_rama`. Ordenado por `gerente_raiz, nivel_en_rama, employee_id`.',
    validacion: 'Confirmar que cada empleado esté correctamente asignado a la rama de su respectivo gerente regional.'
  },
  18: {
    negocio: 'Simular y consultar un catálogo jerárquico de categorías y subcategorías con cálculo de ruta taxonómica (*breadcrumbs*).',
    fuentes: 'Tabla sintética / CTE con jerarquía de categorías padre-hijo.',
    relaciones: 'Ancla selecciona categorías raíz (`parent_id IS NULL`). Recursión une hijos con padres para formar la ruta taxonómica.',
    filtros: 'Ancla `parent_id IS NULL`.',
    proyeccion: '`category_id`, `category_name`, `nivel`, `ruta_taxonomica` (`Bebidas > Alcohólicas > Vinos`). Ordenado por `ruta_taxonomica`.',
    validacion: 'Comprobar que los separadores de ruta y niveles de profundidad coincidan exactamente con la estructura de árbol.'
  },
  19: {
    negocio: 'Implementar una consulta recursiva con detección y prevención automática de ciclos infinitos utilizando un array de nodos visitados.',
    fuentes: 'Estructura de grafo o jerarquía con posibles referencias circulares introducidas deliberadamente.',
    relaciones: 'Término recursivo evalúa `WHERE NOT (e.employee_id = ANY(o.nodos_visitados))` para abortar ramas circulares.',
    filtros: 'Condición de corte por pertenencia a array (`= ANY(array)`).',
    proyeccion: '`employee_id`, `nombre`, `nivel`, `es_ciclico`, `camino_recorrido`.',
    validacion: 'Verificar que la consulta termine con éxito en tiempo finito sin caer en bucle infinito `ERROR: loop detected`.'
  },
  20: {
    negocio: 'Generar una proyección financiera y de demanda mensual aplicando tasas compuestas de crecimiento e interés mes a mes.',
    fuentes: 'Modelo matemático iterativo implementado mediante `WITH RECURSIVE`.',
    relaciones: 'Ancla establece el mes base (`mes = 1`, `ventas_base = 10000`). Recursión calcula `ventas * (1 + tasa_crecimiento)`.',
    filtros: 'Condición de parada: `mes < 12`.',
    proyeccion: '`mes`, `ventas_proyectadas`, `crecimiento_acumulado`, `flete_estimado`, `margen_proyectado`. Ordenado por `mes ASC`.',
    validacion: 'Asegurar que la progresión numérica respete la fórmula de interés compuesto $V_t = V_0 \\times (1 + r)^t$.'
  },
  21: {
    negocio: 'Analizar el rendimiento mes a mes de cada vendedor comparando su facturación actual contra el mes inmediatamente anterior (MoM - Month over Month).',
    fuentes: '`employees`, `orders`, `order_details`. Granularidad: ventas agregadas por vendedor y mes calendario.',
    relaciones: '`employees` $\\to$ `orders` $\\to$ `order_details`. Agregación previa en CTE y función de ventana `LAG(ventas, 1) OVER (PARTITION BY employee_id ORDER BY mes)`.',
    filtros: 'Agrupación por vendedor y mes en CTE.',
    proyeccion: '`nombre_completo`, `mes`, `ventas_mes`, `ventas_mes_anterior`, `diferencia_absoluta`, `variacion_porcentual`.',
    validacion: 'Validar que el primer mes de cada vendedor tenga `ventas_mes_anterior = NULL` y que la diferencia matemática sea exacta.'
  },
  22: {
    negocio: 'Detectar patrones de alerta temprana identificando clientes cuyos pedidos futuros sufran caídas abruptas de facturación.',
    fuentes: '`customers`, `orders`, `order_details`. Granularidad: pedidos cronológicos por cliente.',
    relaciones: 'Unión de tablas de ventas con ventana `LEAD(total_pedido, 1) OVER (PARTITION BY customer_id ORDER BY order_date)`.',
    filtros: 'Filtro en subconsulta / consulta principal: `diferencia_lead < -500` (caída superior a $500).',
    proyeccion: '`company_name`, `order_id`, `order_date`, `total_pedido`, `siguiente_pedido_total`, `caida_importe`.',
    validacion: 'Confirmar que `siguiente_pedido_total` coincida efectivamente con la orden cronológica subsiguiente del mismo cliente.'
  },
  23: {
    negocio: 'Suavizar fluctuaciones diarias de facturación calculando un promedio móvil de 7 días (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`) para análisis de tendencias.',
    fuentes: '`orders` y `order_details`. Granularidad: total de ventas agregadas por día calendario.',
    relaciones: 'CTE agrega ventas por `order_date`. Consulta externa aplica ventana con marco físico explícito.',
    filtros: 'Agrupación por `order_date`. Marco de ventana: `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`.',
    proyeccion: '`fecha`, `ventas_dia`, `promedio_movil_7d`, `ventas_acumuladas_semana`. Ordenado por `fecha ASC`.',
    validacion: 'Verificar que para los primeros 6 días, el promedio se calcule con las filas disponibles y a partir del día 7 tome exactamente 7 tuplas.'
  },
  24: {
    negocio: 'Calcular el acumulado anual de ventas (YTD - Year-To-Date) particionado por año fiscal utilizando marcos lógicos `RANGE BETWEEN`.',
    fuentes: '`orders` y `order_details`. Granularidad: ingresos mensuales por año.',
    relaciones: 'CTE de ventas mensuales. Ventana `SUM(ingresos) OVER (PARTITION BY anio ORDER BY mes RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.',
    filtros: 'Agrupación por año y mes.',
    proyeccion: '`anio`, `mes`, `ingresos_mes`, `ingresos_acumulados_ytd`, `porcentaje_avance_anual`. Ordenado por `anio, mes`.',
    validacion: 'Comprobar que al cambiar de año (e.g. de 1996 a 1997), el acumulado YTD se reinicie correctamente a las ventas de enero.'
  },
  25: {
    negocio: 'Identificar el producto líder (más costoso) de cada categoría para comparar el precio de cada artículo contra el máximo de su segmento.',
    fuentes: '`products` (77 productos) y `categories` (8 categorías).',
    relaciones: '`products` $\\to$ `categories` vía `category_id`. Ventana `FIRST_VALUE(product_name) OVER (PARTITION BY category_id ORDER BY unit_price DESC)`.',
    filtros: '`p.discontinued = 0`. Marco de ventana por defecto (`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` o explícito a toda la partición).',
    proyeccion: '`category_name`, `product_name`, `unit_price`, `producto_mas_caro`, `precio_mas_caro`, `diferencia_con_lider`.',
    validacion: 'Asegurar que `producto_mas_caro` permanezca constante para todos los productos de una misma categoría.'
  },
  26: {
    negocio: 'Determinar el producto más accesible (más barato) dentro de cada categoría garantizando la correcta definición del marco de ventana final.',
    fuentes: '`products` y `categories`. Granularidad: productos individuales comparados contra el mínimo de categoría.',
    relaciones: '`products` $\\to$ `categories`. Ventana `LAST_VALUE(product_name) OVER (PARTITION BY category_id ORDER BY unit_price DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)`.',
    filtros: '`p.discontinued = 0`. Marco obligatorio `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` para que `LAST_VALUE` vea el final de la partición.',
    proyeccion: '`category_name`, `product_name`, `unit_price`, `producto_mas_barato`, `precio_minimo`.',
    validacion: 'Verificar que sin el marco `UNBOUNDED FOLLOWING`, `LAST_VALUE` retornaría el valor de la fila actual (trampa clásica de SQL).'
  },
  27: {
    negocio: 'Extraer el tercer producto más vendido por categoría para análisis de profundidad de catálogo usando `NTH_VALUE`.',
    fuentes: '`categories`, `products`, `order_details`. Granularidad: productos clasificados por volumen de ventas en su categoría.',
    relaciones: 'Agregación previa de unidades vendidas por producto. Ventana `NTH_VALUE(product_name, 3) OVER (PARTITION BY category_id ORDER BY total_unidades DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)`.',
    filtros: 'Agrupación por categoría y producto en CTE.',
    proyeccion: '`category_name`, `product_name`, `total_unidades`, `tercer_mas_vendido`, `unidades_tercer_lugar`.',
    validacion: 'Confirmar que para categorías con menos de 3 productos, la función retorne `NULL` de manera limpia y sin errores.'
  },
  28: {
    negocio: 'Clasificar a los clientes por facturación total contrastando los rankings con y sin huecos (`DENSE_RANK` vs `ROW_NUMBER` vs `RANK`).',
    fuentes: '`customers`, `orders`, `order_details`. Granularidad: cliente y monto total de ventas.',
    relaciones: '`customers` $\\to$ `orders` $\\to$ `order_details`. Ventanas analíticas sobre el total facturado.',
    filtros: 'Agrupación por `customer_id, company_name`.',
    proyeccion: '`company_name`, `total_facturado`, `ranking_consecutivo` (`ROW_NUMBER`), `ranking_con_empates` (`RANK`), `ranking_denso` (`DENSE_RANK`).',
    validacion: 'Observar el comportamiento ante clientes con ventas idénticas: `RANK` deja huecos posicionales mientras que `DENSE_RANK` preserva la numeración consecutiva.'
  },
  29: {
    negocio: 'Segmentar los productos del catálogo en cuatro cuartiles de rentabilidad (`NTILE(4)`) para priorización de catálogo.',
    fuentes: '`products` y `categories`. Granularidad: 77 productos clasificados en 4 grupos equilibrados.',
    relaciones: '`products` $\\to$ `categories`. Ventana `NTILE(4) OVER (ORDER BY unit_price DESC)`.',
    filtros: '`p.discontinued = 0`.',
    proyeccion: '`product_name`, `category_name`, `unit_price`, `cuartil_precio` (1: Premium, 2: Alto, 3: Medio, 4: Económico), `etiqueta_segmento`.',
    validacion: 'Verificar que los 77 productos queden distribuidos equitativamente en cubetas de tamaño similar (grupos de 20 y 19 tuplas).'
  },
  30: {
    negocio: 'Calcular la posición relativa percentilar (`PERCENT_RANK`) y la distribución acumulada (`CUME_DIST`) del precio de cada producto.',
    fuentes: 'Tabla `products` (77 productos).',
    relaciones: 'Funciones de distribución estadística `PERCENT_RANK() OVER (ORDER BY unit_price)` y `CUME_DIST() OVER (ORDER BY unit_price)`.',
    filtros: '`p.discontinued = 0`.',
    proyeccion: '`product_name`, `unit_price`, `percent_rank` (0.0 a 1.0), `cume_dist` (proporción acumulada de tuplas $\\le$ precio actual).',
    validacion: 'Validar que el producto más barato tenga `PERCENT_RANK = 0.0` y el producto más caro tenga `PERCENT_RANK = 1.0` y `CUME_DIST = 1.0`.'
  },
  31: {
    negocio: 'Extraer los 3 productos más caros de cada una de las 8 categorías comerciales mediante un `CROSS JOIN LATERAL` optimizado.',
    fuentes: '`categories` (8 filas) y `products` (77 filas).',
    relaciones: '`categories c CROSS JOIN LATERAL (SELECT * FROM products WHERE category_id = c.category_id ORDER BY unit_price DESC LIMIT 3) top_prod`.',
    filtros: '`p.discontinued = 0` dentro de la subconsulta lateral.',
    proyeccion: '`category_name`, `product_name`, `unit_price`, `ranking_categoria`. Ordenado por `category_name, unit_price DESC`.',
    validacion: 'Comprobar que el resultado contenga exactamente $8 \\times 3 = 24$ filas y que cada grupo de 3 pertenezca a la categoría correspondiente.'
  },
  32: {
    negocio: 'Construir una vista rápida de clientes activos obteniendo sus 5 órdenes más recientes mediante evaluación lateral indexada.',
    fuentes: '`customers` (91 clientes) y `orders` (830 pedidos).',
    relaciones: '`customers c CROSS JOIN LATERAL (SELECT order_id, order_date, freight FROM orders WHERE customer_id = c.customer_id ORDER BY order_date DESC, order_id DESC LIMIT 5) ultimos_pedidos`.',
    filtros: 'Correlación por `customer_id = c.customer_id` y `LIMIT 5`.',
    proyeccion: '`company_name`, `country`, `order_id`, `order_date`, `freight`. Ordenado por `company_name, order_date DESC`.',
    validacion: 'Confirmar que el resultado devuelva exactamente 415 filas (los 89 clientes activos con hasta 5 pedidos cada uno).'
  },
  33: {
    negocio: 'Analizar a los proveedores identificando para cada uno su producto estrella (más costoso) y el inventario total asociado usando LATERAL.',
    fuentes: '`suppliers` (29 proveedores) y `products` (77 productos).',
    relaciones: '`suppliers s LEFT JOIN LATERAL (SELECT product_name, unit_price, units_in_stock FROM products WHERE supplier_id = s.supplier_id ORDER BY unit_price DESC LIMIT 1) p_top ON true`.',
    filtros: 'Uso de `LEFT JOIN LATERAL ... ON true` para preservar proveedores que eventualmente no tengan productos asignados.',
    proyeccion: '`company_name` (proveedor), `country`, `producto_estrella`, `precio_maximo`, `stock_disponible`.',
    validacion: 'Verificar que los 29 proveedores figuren en la salida y que el producto mostrado sea efectivamente el de mayor precio del proveedor.'
  },
  34: {
    negocio: 'Pivotear las ventas anuales por categoría en columnas dinámicas por año (1996, 1997, 1998) usando la función `crosstab` de PostgreSQL.',
    fuentes: '`categories`, `products`, `orders`, `order_details` procesadas con la extensión `tablefunc`.',
    relaciones: 'Consulta de origen alimenta `crosstab(texto_consulta, texto_categorias)`.',
    filtros: 'Filtrado temporal y agregación de ventas por categoría y año.',
    proyeccion: '`categoria`, `ventas_1996`, `ventas_1997`, `ventas_1998`, `ventas_totales_categoria`. Ordenado por `categoria ASC`.',
    validacion: 'Comprobar que los 8 registros de categorías tengan sus montos pivotados y que las categorías sin ventas en un año muestren 0.00 gracias a `COALESCE`.'
  },
  35: {
    negocio: 'Construir una matriz dinámica de cantidad de pedidos por mes y trimestre combinando `generate_series` y agregación matricial.',
    fuentes: '`orders` y serie sintética de meses generada con `generate_series`.',
    relaciones: 'Cruce entre la dimensión temporal de meses y las órdenes registradas.',
    filtros: 'Rango de fechas del dataset Northwind (julio 1996 a mayo 1998).',
    proyeccion: '`anio`, `mes`, `total_pedidos`, `pedidos_enviados_a_tiempo`, `pedidos_con_retraso`.',
    validacion: 'Asegurar que ningún mes calendario quede omitido en la matriz, incluso si un mes no tuviera órdenes registradas.'
  },
  36: {
    negocio: 'Diseñar una matriz de retención de cohortes mensuales (Cohort Analysis) midiendo el porcentaje de clientes que vuelven a comprar en meses posteriores.',
    fuentes: '`orders` (830 órdenes) agregadas por cliente y fecha de primera compra (*cohorte*).',
    relaciones: 'CTE 1 calcula la fecha mínima de orden por cliente (`cohorte_mes`). CTE 2 calcula los meses transcurridos (*index*) para compras posteriores.',
    filtros: 'Agrupación por `cohorte_mes` e índice de mes (`mes_index = 0, 1, 2, ...`).',
    proyeccion: '`cohorte_mes`, `tamaño_cohorte`, `mes_0`, `mes_1`, `mes_2`, `mes_3` (número de clientes activos y tasa de retención %).',
    validacion: 'Verificar que en `mes_0` la tasa de retención sea siempre del 100% (todos los clientes compraron en su mes inicial).'
  },
  37: {
    negocio: 'Segmentar la retención de cohortes por país de destino para identificar qué mercados geográficos tienen mayor fidelidad de recompra.',
    fuentes: '`customers` y `orders`. Granularidad: cohortes de clientes segmentadas por país.',
    relaciones: 'Unión de clientes con sus órdenes agrupadas por país de facturación y fecha de adquisición.',
    filtros: 'Agrupación por país y mes de cohorte.',
    proyeccion: '`country`, `cohorte_mes`, `clientes_adquiridos`, `clientes_recurrentes_m1`, `tasa_retencion_m1`. Ordenado por `country, cohorte_mes`.',
    validacion: 'Comprobar que los 21 países del modelo canónico queden representados según su historial de compras.'
  },
  38: {
    negocio: 'Clasificar la base de clientes en tres segmentos comerciales: Nuevos, Recurrentes y Perdidos (*Churn*) comparando dos períodos semestrales.',
    fuentes: '`customers` y `orders`. Granularidad: presencia de órdenes en el período base (1997) vs período comparativo (1998).',
    relaciones: 'CTEs de actividad en período 1 y período 2 unidas mediante `FULL OUTER JOIN` con `customers`.',
    filtros: 'Lógica condicional `CASE WHEN p1 IS NOT NULL AND p2 IS NOT NULL THEN \'RECURRENTE\' ... END`.',
    proyeccion: '`segmento`, `total_clientes`, `porcentaje_del_total`. Ordenado por `total_clientes DESC`.',
    validacion: 'Validar que la suma de clientes en los tres segmentos coincida exactamente con los clientes activos en el período evaluado.'
  },
  39: {
    negocio: 'Identificar clientes en riesgo de abandono: clientes que tuvieron al menos una compra en 1997 pero ninguna orden registrada en 1998.',
    fuentes: '`customers` y `orders`. Granularidad: clientes con actividad en 1997 y filtro anti-join en 1998.',
    relaciones: '`customers c` con `LATERAL` o subconsulta correlacionada `WHERE EXISTS (1997) AND NOT EXISTS (1998)`.',
    filtros: '`EXISTS (pedidos 1997)` y `NOT EXISTS (pedidos 1998)`.',
    proyeccion: '`customer_id`, `company_name`, `country`, `total_1997`, `primer_pedido`, `ultimo_pedido`. Ordenado por `total_1997 DESC`.',
    validacion: 'Comprobar que ninguno de los clientes listados posea órdenes con fecha $\\ge$ \'1998-01-01\'.'
  },
  40: {
    negocio: 'Obtener el segundo producto más caro de cada categoría para comparar el escalón de precios respecto al producto líder.',
    fuentes: '`categories` (8 categorías) y `products` (77 productos).',
    relaciones: '`categories c CROSS JOIN LATERAL (SELECT product_name, unit_price FROM products WHERE category_id = c.category_id ORDER BY unit_price DESC OFFSET 1 LIMIT 1) sub`.',
    filtros: '`p.discontinued = 0` y cláusula `OFFSET 1 LIMIT 1` dentro de la subconsulta lateral.',
    proyeccion: '`category_name`, `product_name` (segundo lugar), `unit_price`, `pct_del_max_global`. Ordenado por `unit_price DESC`.',
    validacion: 'Verificar que para cada categoría se proyecte exactamente un solo producto (el ubicado en el segundo puesto de precio).'
  },
  41: {
    negocio: 'Diagnosticar cuellos de botella de rendimiento en una consulta analítica compleja de ventas mediante `EXPLAIN (ANALYZE, BUFFERS)`.',
    fuentes: '`customers`, `orders`, `order_details`, `products`. Consulta analítica con múltiples JOINs, GROUP BY y ORDER BY.',
    relaciones: 'Inspección de nodos de plan de ejecución: `Seq Scan`, `Hash Join`, `HashAggregate`, `Sort`.',
    filtros: 'Evaluación del costo estimado (`cost=...`), tiempo real de ejecución (`actual time=...`) y buffers de memoria leídos (`shared hit/read`).',
    proyeccion: 'Líneas del árbol del plan de ejecución generado por el optimizador de PostgreSQL.',
    validacion: 'Confirmar que `actual rows` sea cercano a las estimaciones de `rows` del optimizador para descartar problemas de estadísticas desactualizadas.'
  },
  42: {
    negocio: 'Medir cuantitativamente el impacto de crear un índice B-Tree sobre `customers(country)` comparando tiempos de ejecución y lecturas de buffers.',
    fuentes: 'Tabla `customers` (91 filas) y `orders` (830 filas).',
    relaciones: 'Consulta de búsqueda antes de crear el índice vs después de indexar.',
    filtros: 'Filtro por país `WHERE c.country = \'Germany\'`.',
    proyeccion: 'Planes de ejecución comparativos `EXPLAIN (ANALYZE, BUFFERS)` antes y después del DDL.',
    validacion: 'Evaluar si en tablas pequeñas PostgreSQL prefiere un `Seq Scan` debido al bajo costo de leer 1-2 páginas completas en memoria.'
  },
  43: {
    negocio: 'Monitorear la salud del motor detectando tablas con acumulación de tuplas muertas (*dead tuples*) que requieran mantenimiento de VACUUM.',
    fuentes: 'Vista del catálogo del sistema `pg_stat_user_tables`.',
    relaciones: 'Cálculo de porcentaje de tuplas muertas `n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0) * 100`.',
    filtros: '`schemaname = \'public\'` y tablas de usuario.',
    proyeccion: '`schemaname`, `relname`, `n_live_tup`, `n_dead_tup`, `pct_dead`, `last_vacuum`, `last_autovacuum`, `tamano`, `accion_recomendada`.',
    validacion: 'Comprender que las métricas reflejan la actividad acumulada del motor en tiempo de ejecución (scans, inserts, updates).'
  },
  44: {
    negocio: 'Identificar tablas con alto porcentaje de escaneos secuenciales (`seq_scan`) que sean candidatas inmediatas para nuevos índices.',
    fuentes: 'Vista de catálogo `pg_stat_all_tables` / `pg_stat_user_tables`.',
    relaciones: 'Contraste entre `seq_scan` e `idx_scan` sobre tablas de usuario en esquema `public`.',
    filtros: '`schemaname = \'public\'` y volumen significativo de lecturas.',
    proyeccion: '`schemaname`, `relname`, `seq_scan`, `seq_tup_read`, `idx_scan_real`, `pct_seq_scan`, `n_live_tup`, `tamano`, `recomendacion`.',
    validacion: 'Asegurar que tablas muy pequeñas (<10 páginas) no reciban recomendación ciega de índice cuando el Seq Scan es la opción óptima.'
  },
  45: {
    negocio: 'Analizar las diferencias operativas y de consumo de recursos entre las 3 estrategias principales de JOIN: `Hash Join`, `Nested Loop` y `Merge Join`.',
    fuentes: '`orders` y `order_details` evaluadas bajo diferentes directivas del planificador (`enable_nestloop`, `enable_hashjoin`, `enable_mergejoin`).',
    relaciones: 'Misma consulta SQL ejecutada forzando diferentes algoritmos de unión física.',
    filtros: 'Filtro de fecha `WHERE o.order_date >= \'1998-01-01\'`.',
    proyeccion: 'Planes de ejecución comparativos generados con `EXPLAIN (ANALYZE, BUFFERS)`.',
    validacion: 'Identificar que `Hash Join` destaca en conjuntos medianos no ordenados, `Merge Join` cuando ambos lados están pre-ordenados, y `Nested Loop` en búsquedas muy selectivas con índice.'
  },
  46: {
    negocio: 'Optimizar el uso de almacenamiento y velocidad de consulta creando un índice parcial (*Partial Index*) que solo indexe productos activos.',
    fuentes: 'Tabla `products` (77 productos).',
    relaciones: 'Índice condicional `CREATE INDEX idx_products_active ON products(product_name) WHERE discontinued = 0`.',
    filtros: 'Consultas que incluyan el predicado exacto `WHERE discontinued = 0`.',
    proyeccion: 'Plan de ejecución `EXPLAIN (ANALYZE, BUFFERS)` mostrando el uso de `Index Scan` sobre el índice parcial.',
    validacion: 'Comprobar que el tamaño en disco del índice parcial sea menor al de un índice completo sobre toda la tabla.'
  },
  47: {
    negocio: 'Diseñar un índice compuesto (*Composite Index*) sobre `(category_id, unit_price DESC)` para eliminar por completo la fase de ordenamiento en memoria.',
    fuentes: 'Tabla `products` y `categories`.',
    relaciones: '`CREATE INDEX idx_products_cat_price ON products(category_id, unit_price DESC)`.',
    filtros: 'Filtro por `category_id = 1` y ordenamiento `ORDER BY unit_price DESC LIMIT 5`.',
    proyeccion: 'Plan de ejecución mostrando `Index Only Scan` o `Index Scan` sin nodo `Sort` adicional.',
    validacion: 'Verificar en el plan que no exista ningún nodo `Sort (cost=...)`, confirmando que el índice entregó los datos ya ordenados.'
  },
  48: {
    negocio: 'Evaluar el impacto de la materialización de CTEs (`MATERIALIZED` vs `NOT MATERIALIZED`) en la propagación de filtros y tiempo de CPU.',
    fuentes: '`customers` y `orders`. CTE de pedidos de 1997 evaluada bajo ambas directivas.',
    relaciones: '`WITH pedidos_1997 AS MATERIALIZED (...)` vs `NOT MATERIALIZED`.',
    filtros: 'Filtro temporal dentro de la CTE y agregación en consulta principal.',
    proyeccion: 'Comparativa de planes de ejecución `EXPLAIN (ANALYZE, BUFFERS)`.',
    validacion: 'Observar cómo `NOT MATERIALIZED` permite al optimizador empujar filtros y reordenar JOINs, mientras que `MATERIALIZED` actúa como optimization fence.'
  },
  49: {
    negocio: 'Auditar el catálogo de índices (`pg_index`, `pg_stat_user_indexes`) para detectar y eliminar índices duplicados o con 0 escaneos acumulados.',
    fuentes: 'Vistas de catálogo `pg_index`, `pg_class`, `pg_stat_user_indexes`.',
    relaciones: 'Agrupación de índices por definición idéntica (`pg_get_indexdef`) y conteo de `idx_scan`.',
    filtros: 'Tablas críticas de usuario (`customers`, `orders`, `products`, `order_details`).',
    proyeccion: '`estado` (\'DUPLICADO\', \'NO USADO\', \'ACTIVO\'), `tabla`, `nombre_indice`, `tamano`, `idx_scan`, `accion_sugerida`.',
    validacion: 'Asegurar que las claves primarias (`pk_*`) y restricciones únicas no sean eliminadas accidentalmente.'
  },
  50: {
    negocio: 'Implementar el flujo de trabajo integral de diagnóstico y optimización (*Query Tuning Workflow*): diagnóstico, análisis de catálogo, indexación, actualización de estadísticas y verificación.',
    fuentes: '`customers`, `orders`, `order_details`, `pg_stat_user_tables`.',
    relaciones: 'Cadena completa de 6 pasos de ingeniería de rendimiento.',
    filtros: 'Consulta representativa de ventas por país y ciudad en 1997-1998.',
    proyeccion: 'Planes de ejecución comparativos antes y después del tuning (`Buffers` reducidos y tiempo de respuesta mejorado).',
    validacion: 'Comprobar que el plan final utilice un acceso indexado eficiente con menor consumo de memoria y CPU.'
  }
};

// Helper to truncate large ASCII tables cleanly
function formatAsciiOutput(rawPsqlOut, exNum) {
  let lines = rawPsqlOut.replace(/^BEGIN\n/, '').replace(/\nROLLBACK\n?$/, '').trim().split('\n');
  
  // Clean mock data leaks if any remain
  lines = lines.map(l => l.replace(/Alfreds Futterkiste - Actualizado/g, 'Alfreds Futterkiste           ')
                         .replace(/Alfreds Futterkiste - Actualizado/g, 'Alfreds Futterkiste'));

  // If small enough, return as is
  if (lines.length <= 25) {
    return lines.join('\n');
  }

  // Large result set -> find table header and data rows
  const headerIdx = lines.findIndex(l => l.includes('---') || l.includes('---+---'));
  if (headerIdx === -1) {
    // Single block or plan
    return lines.slice(0, 15).join('\n') + '\n...\n' + lines.slice(-3).join('\n');
  }

  const colHeaders = lines.slice(0, headerIdx + 1);
  const dataRows = lines.slice(headerIdx + 1);
  
  // Extract total rows footer if present
  let footer = '';
  if (dataRows.length > 0 && /^\(\d+\s+rows?\)/.test(dataRows[dataRows.length - 1].trim())) {
    footer = dataRows.pop().trim();
  }

  const topRows = dataRows.slice(0, 10);
  const bottomRows = dataRows.slice(-3);

  // Synthesize clean ellipsis line with proper column alignment
  const separator = lines[headerIdx];
  const ellipsisRow = separator.split('+').map(part => {
    const len = part.length;
    const dots = '...';
    const padLeft = Math.floor((len - dots.length) / 2);
    const padRight = len - dots.length - padLeft;
    return ' '.repeat(Math.max(1, padLeft)) + dots + ' '.repeat(Math.max(1, padRight));
  }).join('|');

  const formattedRows = [...colHeaders, ...topRows, ellipsisRow, ...bottomRows];
  if (footer) {
    formattedRows.push(footer);
  }
  return formattedRows.join('\n');
}

// Process each exercise
const newSections = [headerText];

for (let i = 1; i < sections.length; i++) {
  let ex = sections[i].trim();
  const titleLine = ex.split('\n')[0].trim();
  
  console.log(`Processing Exercise ${i}: ${titleLine}`);

  // Fix SQL if needed (e.g. clean mock data in Ex 10)
  if (i === 10) {
    ex = ex.replace(/VALUES\s*\(\s*'NWE01'[\s\S]*?'ALFKI', 'Alfreds Futterkiste - Actualizado'[\s\S]*?\)/,
      `VALUES\n        ('NEW01', 'TechCorp Global', 'Carlos Garcia', 'Berlin', 'Germany'),\n        ('NEW02', 'DataLabs International', 'Ana Soto', 'London', 'UK'),\n        ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Berlin', 'Germany')`);
    ex = ex.replace(/\('NWE01', ...\), \('NWE02', ...\), \('ALFKI', ...\)/g, "('NEW01', ...), ('NEW02', ...), ('ALFKI', ...)");
    ex = ex.replace(/- 'NWE01': No existe/g, "- 'NEW01': No existe");
    ex = ex.replace(/- 'NWE02': No existe/g, "- 'NEW02': No existe");
  }

  // Extract SQL
  const sqlMatch = ex.match(/```sql\n([\s\S]*?)\n```/);
  const sql = sqlMatch ? sqlMatch[1].trim() : '';

  // Execute in Docker to get authentic ASCII table
  let rawDbOutput = '';
  if (sql) {
    fs.writeFileSync('temp_test.sql', 'BEGIN;\n' + sql + ';\nROLLBACK;');
    try {
      execSync('docker cp temp_test.sql pg_architect_lab:/tmp/temp_test.sql');
      rawDbOutput = execSync('docker exec pg_architect_lab psql -U slinkter -d northwind -f /tmp/temp_test.sql', { encoding: 'utf8' });
    } catch (err) {
      console.error(`Error running SQL for Ex ${i}:`, err.message);
    }
  }

  // Format authentic ASCII output
  const formattedAscii = formatAsciiOutput(rawDbOutput, i);

  // Replace ASCII table in exercise
  if (formattedAscii) {
    ex = ex.replace(/#### 📊 Resultado Real[^\n]*\n\n```text\n[\s\S]*?\n```/,
      `#### 📊 Resultado Real de Ejecución en PostgreSQL (AWS EC2):\n\n\`\`\`text\n${formattedAscii}\n\`\`\``);
  }

  // Deepen Optimizer & Engine descriptions where needed
  // Window Framing (Ex 21-30)
  if (i >= 21 && i <= 30) {
    if (!ex.includes('Marco de Ventana (Window Framing)')) {
      let framingNote = `\n\n> 🔍 **Profundización en Framing:** En PostgreSQL, cuando se omite la cláusula \`ROWS/RANGE\` pero existe \`ORDER BY\`, el marco por defecto es \`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\`. \`ROWS\` evalúa desplazamientos físicos de tuplas (punteros en memoria muy rápidos), mientras que \`RANGE\` evalúa valores lógicos agrupando duplicados (*peers*), lo que requiere buffering adicional.`;
      ex = ex.replace(/(### Marco Conceptual del Optimizador\n\n[\s\S]*?)(\n\n### Diagrama)/, `$1${framingNote}$2`);
    }
  }

  // Recursive CTE Lifecycle (Ex 11-20)
  if (i >= 11 && i <= 20) {
    if (!ex.includes('Ciclo de Vida de la Recursión')) {
      let recursionLifecycle = `\n\n> 🔄 **Ciclo de Vida de la Recursión (4 Fases en Motor):**\n> 1. **Término Ancla:** Evalúa la consulta base $\\to$ puebla la \`Working Table\` (WT) y la \`Result Table\` (RT).\n> 2. **Tabla de Trabajo (WT):** Semilla de tuplas generadas en la iteración $k-1$.\n> 3. **Término Recursivo:** Evalúa el JOIN contra WT $\\to$ genera tuplas para la \`Intermediate Table\`.\n> 4. **Condición de Parada:** WT se reemplaza por la \`Intermediate Table\`. Si tiene 0 filas, finaliza y retorna RT.`;
      ex = ex.replace(/(### Marco Conceptual del Optimizador\n\n[\s\S]*?)(\n\n### Diagrama)/, `$1${recursionLifecycle}$2`);
    }
  }

  // Catalog queries notes (Ex 8, 43, 44, 45, 49)
  if ([8, 43, 44, 45, 49].includes(i)) {
    if (!ex.includes('Dinámica del Catálogo de Estadísticas')) {
      let catalogNote = `\n\n> ⚠️ **Dinámica del Catálogo de Estadísticas:** Los valores de \`pg_stat_user_tables\`, \`seq_scan\`, \`n_dead_tup\` y timestamps de autovacuum dependen de la actividad acumulada del motor en tiempo de ejecución. En una instancia recién inicializada o tras un \`VACUUM FULL\`, las métricas numéricas reflejarán el estado de carga actual.`;
      ex = ex.replace(/(#### 📊 Resultado Real[\s\S]*?\n```\n)/, `$1${catalogNote}\n\n`);
    }
  }

  // Insert "🧠 Cómo Pensar como un Analista de Datos"
  const mm = mentalModels[i];
  if (mm && !ex.includes('### 🧠 Cómo Pensar como un Analista de Datos')) {
    const analystBlock = `### 🧠 Cómo Pensar como un Analista de Datos

1. **Pregunta de Negocio & KPI:** ${mm.negocio}
2. **Fuentes de Datos & Granularidad:** ${mm.fuentes}
3. **Relaciones & JOINs:** ${mm.relaciones}
4. **Filtros & Agregaciones:** ${mm.filtros}
5. **Proyección & Ordenamiento:** ${mm.proyeccion}
6. **Validación & Sentido Común:** ${mm.validacion}

`;
    // Insert after ### 🎓 Explicación del Profesor and its analogy
    ex = ex.replace(/(### 🎓 Explicación del Profesor\n\n[\s\S]*?\n\n)(### Marco Conceptual)/, `$1${analystBlock}$2`);
  }

  newSections.push(`## Ejercicio ${titleLine}\n\n${ex.substring(titleLine.length).trim()}`);
}

const finalContent = newSections.join('\n\n---\n\n') + '\n';
fs.writeFileSync('2.Ejercicios/3.avanzado.md', finalContent, 'utf8');
console.log('Successfully updated 2.Ejercicios/3.avanzado.md!');

if (fs.existsSync('temp_test.sql')) fs.unlinkSync('temp_test.sql');
