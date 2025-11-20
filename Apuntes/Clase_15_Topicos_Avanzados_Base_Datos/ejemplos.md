# Ejemplos - Clase 15: Data Warehouse (Arquitectura y Explotación)

### Ejemplo 1: Diferencia entre OLTP y DW (Contexto de un Pedido)

Imagina un sistema de ventas online.

**Escenario OLTP (Sistema Transaccional):**
*   **Acción:** Un cliente realiza un pedido.
*   **Datos:** El sistema OLTP registra el `ID_Pedido`, `ID_Cliente`, `Fecha_Hora_Pedido`, `Estado_Pedido`, y los ítems del pedido (`ID_Producto`, `Cantidad`, `Precio_Unitario`) en tablas altamente normalizadas (`Pedidos`, `Clientes`, `Productos`, `DetallePedido`).
*   **Objetivo:** Procesar la transacción lo más rápido posible, asegurar la integridad del pedido, actualizar el stock en tiempo real.
*   **Consulta típica:** "Ver el detalle del pedido número X".
*   **Características:** Datos actuales, transacciones pequeñas y frecuentes, escritura intensiva.

**Escenario DW (Sistema Analítico):**
*   **Acción:** Un analista quiere saber las "Ventas totales por categoría de producto por mes en la región este durante el último año".
*   **Datos:** El DW contiene datos históricos de todos los pedidos, productos y clientes, ya transformados, limpiados e integrados. Las tablas están diseñadas en un esquema dimensional (ej., `FACT_VENTAS`, `DIM_TIEMPO`, `DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_SUCURSAL`).
*   **Objetivo:** Permitir consultas complejas y agregaciones rápidas para identificar tendencias de ventas, productos más vendidos, rendimiento de sucursales, etc.
*   **Consulta típica:** `SELECT SUM(Monto_Venta), DIM_PRODUCTO.Categoria FROM FACT_VENTAS JOIN DIM_PRODUCTO ... GROUP BY DIM_PRODUCTO.Categoria, DIM_TIEMPO.Mes`.
*   **Características:** Datos históricos, grandes volúmenes, lecturas intensivas, agregaciones.

### Ejemplo 2: Proceso ETL (Extracción, Transformación, Carga)

Una empresa tiene datos de ventas en un sistema de inventario (SQL Server) y datos de clientes en un CRM (Oracle). Necesita consolidar esta información en un Data Warehouse.

1.  **Extracción (Extract):**
    *   Conectarse al sistema de inventario (SQL Server) y extraer los datos de ventas de la tabla `Sales.OrderHeader` y `Sales.OrderDetail`.
    *   Conectarse al sistema CRM (Oracle) y extraer los datos de clientes de la tabla `CRM.Customers`.
    *   Extraer datos de la dimensión de tiempo de un generador de fechas.

2.  **Transformación (Transform):**
    *   **Limpieza:** Eliminar registros de ventas duplicados o con `ID_Cliente`s inválidos. Estandarizar formatos de fecha.
    *   **Integración:** Unir los datos de ventas con los de clientes. Resolver IDs de productos entre sistemas si son diferentes.
    *   **Cálculo de Derivados:** Calcular el `Margen_Beneficio` a partir del `Monto_Venta` y el `Costo_Producto`.
    *   **Agregación/Normalización Dimensional:** Crear atributos para las tablas de dimensión (ej., para `DIM_TIEMPO`, derivar `Mes`, `Año`, `Trimestre` de `Fecha_Pedido`). Para `DIM_CLIENTE`, consolidar `Nombre`, `Apellido` en `Nombre_Completo`.

3.  **Carga (Load):**
    *   Insertar los datos transformados en las tablas de hechos (`FACT_VENTAS`) y tablas de dimensiones (`DIM_TIEMPO`, `DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_SUCURSAL`) del Data Warehouse.
    *   Esto puede ser una carga completa (borrar y recargar) o incremental (solo cargar nuevos/cambiados).

### Ejemplo 3: Consulta OLAP (Venta de Productos por Región y Tiempo)

Supongamos que tenemos un cubo de ventas con las dimensiones `Tiempo`, `Producto` y `Geografía`, y la medida `Monto_Venta`.

*   **Drill-down (Profundizar):** Un analista ve el `Monto_Venta` total para el "Producto A" en el "Año 2023". Decide hacer un drill-down en la dimensión `Tiempo` para ver las ventas de ese producto por "Mes".
*   **Roll-up (Subir):** Después de analizar las ventas mensuales del "Producto A", decide hacer un roll-up en la dimensión `Producto` para ver las ventas totales de la "Categoría de Producto" a la que pertenece el "Producto A" por "Mes".
*   **Slice (Rebanar):** Un analista está interesado solo en las ventas de "Enero 2023" para todos los productos y regiones. Se "rebana" el cubo para esa porción específica.
*   **Dice (Dinamizar):** Un analista quiere ver las ventas de "Enero 2023" para "Productos Electrónicos" y "Región Norte". Se "dinamiza" el cubo para mostrar esta intersección específica.

### Ejemplo 4: Data Mining Predictivo (Predecir Churn de Clientes)

Una empresa de telecomunicaciones desea predecir qué clientes tienen una alta probabilidad de cancelar su servicio (churn).

*   **Recolección de Datos (DW):** Se utilizan datos históricos del Data Warehouse que incluyen el tiempo de servicio del cliente, el uso mensual, el tipo de contrato, las quejas registradas, el soporte técnico contactado, etc.
*   **Modelado (Data Mining):** Se construye un modelo de clasificación (ej., usando algoritmos de Árboles de Decisión o Redes Neuronales) entrenado con datos de clientes que ya han hecho churn y clientes que no.
*   **Predicción:** El modelo se aplica a los clientes actuales para asignar una probabilidad de churn a cada uno.
*   **Acción de Negocio:** Los clientes con alta probabilidad de churn son contactados con ofertas especiales o atención personalizada para retenerlos.
