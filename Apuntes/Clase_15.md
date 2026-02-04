# 📊 Clase 15: Data Warehouse (Arquitectura y Explotación)

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **DW vs. Sistemas Operacionales (OLTP)** | Los **Sistemas Operacionales** (OLTP) ejecutan el negocio (transacciones rápidas, datos actuales, empleados por oficinistas). El **DW** (Sistemas Analíticos) administra el negocio (análisis histórico, integración, usado por *decision makers*). |
| **Definición de Data Warehouse** | Un DW es **Organizado por Temas** (información relacionada), **Variante en el Tiempo** (histórico y auditable), **No Volátil** (permanente) e **Integrado** (consistente). |
| **Data Mart** | Es una versión más pequeña y especializada del DW, diseñada para un grupo o departamento específico (Ej. Ventas o Finanzas), mejorando el acceso y el análisis para ese grupo. |
| **ETL (Extracción, Transformación y Carga)** | Este es el proceso más costoso y largo (¡el **80% de los recursos!**). Implica tomar datos de las fuentes, **transformarlos** (limpiar, integrar, derivar) y **cargarlos** en el DW. |
| **Metadatos y Cubos** | Los **Metadatos** son la clave para entender el contexto de la data. La información se representa en **Cubos de Datos** multidimensionales, que tienen Dimensiones (Ej. Año, País, Color) y Hechos (Medidas de interés). |
| **Explotación de Datos** | ¿Cómo usamos toda esta información? **Query Ad hoc** (consultas puntuales). **OLAP** (Online Analytical Processing): Análisis multidimensional avanzado sobre los cubos (Ej. rodar, picar y rebanar el cubo). **Data Mining** (Minería de Datos): Herramientas que buscan automáticamente **patrones y tendencias**. |
| **Tipos de Data Mining** | **Minería de Descubrimiento** (encontrar patrones en todo el almacén, a veces los más valiosos). **Minería Predictiva** (usar datos conocidos para crear modelos que predicen valores futuros). |

**Resumen de la Clase 15:** Un DW es un sistema analítico integrado, no volátil e histórico, que se diferencia del OLTP. Vimos que el proceso ETL consume la mayor parte del esfuerzo. Finalmente, el análisis de datos se realiza mediante OLAP (consultas multidimensionales) y Data Mining (que descubre patrones y ayuda a la predicción).

---

---

## 💡 Ejemplos Prácticos

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

---

## ✏️ Ejercicios Resueltos

### Ejercicio 1: Comparación OLTP vs. Data Warehouse

**Enunciado:**
Completa la siguiente tabla comparativa entre un sistema OLTP (Online Transaction Processing) y un Data Warehouse (DW), basándote en sus características principales.

| Característica        | Sistema OLTP               | Data Warehouse (DW)                                |
| :-------------------- | :------------------------- | :------------------------------------------------- |
| **Propósito**         | ...                        | ...                                                |
| **Tipo de Operación** | ...                        | ...                                                |
| **Datos**             | ...                        | ...                                                |
| **Horizonte Temporal**| ...                        | ...                                                |
| **Nivel de Detalle**  | ...                        | ...                                                |
| **Optimización**      | ...                        | ...                                                |
| **Usuarios Típicos**  | ...                        | ...                                                |

---

**Solución:**

| Característica        | Sistema OLTP               | Data Warehouse (DW)                                |
| :-------------------- | :------------------------- | :------------------------------------------------- |
| **Propósito**         | Procesa transacciones diarias | Soporte a la toma de decisiones y análisis de negocio |
| **Tipo de Operación** | CRUD (lecturas/escrituras) frecuentes y pequeñas | Consultas complejas, agregaciones, análisis (lecturas intensivas) |
| **Datos**             | Actuales, transaccionales, detallados         | Históricos, consolidados, resumidos, integrados       |
| **Horizonte Temporal**| Corto (meses, días)        | Largo (años, décadas)                             |
| **Nivel de Detalle**  | Muy detallado              | Agregado, resumido, aunque puede tener detalle granular |
| **Optimización**      | Para escrituras rápidas, consistencia transaccional | Para lecturas rápidas, análisis multidimensional     |
| **Usuarios Típicos**  | Empleados operativos (cajeros, operadores) | Analistas de negocio, gerentes, científicos de datos |

### Ejercicio 2: Fases del Proceso ETL

**Enunciado:**
Describe brevemente las tres fases principales del proceso ETL (Extracción, Transformación, Carga) en el contexto de la construcción de un Data Warehouse, y menciona un ejemplo de tarea que se realizaría en cada fase.

---

**Solución:**

1.  **Extracción (Extraction):**
    *   **Descripción:** Consiste en obtener los datos de diversas fuentes operacionales (bases de datos, archivos planos, sistemas externos). El objetivo es identificar los datos relevantes y copiarlos para su posterior procesamiento.
    *   **Ejemplo de Tarea:** Conectarse a la base de datos de ventas de un sistema de punto de venta (POS) y extraer todos los registros de transacciones del último día.

2.  **Transformación (Transformation):**
    *   **Descripción:** Es la fase más compleja, donde los datos extraídos se limpian, se validan, se unifican, se enriquecen y se adaptan al esquema del Data Warehouse. Se aplican reglas de negocio y se resuelven inconsistencias.
    *   **Ejemplo de Tarea:** Estandarizar formatos de fecha (`DD/MM/YYYY` a `YYYY-MM-DD`), convertir unidades de medida (libras a kilos), calcular nuevos campos (ej. `beneficio = venta - costo`), y resolver claves entre diferentes sistemas.

3.  **Carga (Load):**
    *   **Descripción:** Los datos ya transformados y limpios se cargan en el Data Warehouse. Puede ser una carga inicial completa (full load) o una carga incremental (solo los cambios desde la última carga).
    *   **Ejemplo de Tarea:** Insertar las nuevas filas de la tabla de hechos `FACT_VENTAS` y actualizar las dimensiones `DIM_PRODUCTO` y `DIM_CLIENTE` con los nuevos o modificados registros después de que hayan pasado por la fase de transformación.

### Ejercicio 3: Consulta OLAP y Data Mining

**Enunciado:**
Una empresa de streaming de música tiene un Data Warehouse. Explica cómo utilizaría:
1.  **OLAP** para un analista de marketing que quiere entender el rendimiento de una nueva campaña.
2.  **Data Mining predictivo** para el equipo de gestión de clientes.

---

**Solución:**

1.  **Uso de OLAP para el Analista de Marketing:**
    *   El analista de marketing utilizaría una herramienta OLAP (ej. Tableau, Power BI o Excel conectado a un cubo OLAP) para explorar las métricas de la campaña.
    *   Podría empezar con una vista de alto nivel del "Número total de reproducciones" (medida) de canciones promocionadas en la campaña.
    *   Luego, haría un **drill-down** para ver las reproducciones por "Género musical" (dimensión).
    *   A continuación, podría **slice** los datos para enfocarse solo en la "Región" (dimensión) donde se lanzó la campaña.
    *   Finalmente, podría **pivotar** (dice) los datos para ver las reproducciones por "Género" vs. "Tipo de Dispositivo" (dimensión).
    *   Esto le permitiría identificar rápidamente qué géneros o dispositivos respondieron mejor a la campaña, sin escribir SQL complejo.

2.  **Uso de Data Mining Predictivo para Gestión de Clientes:**
    *   El equipo de gestión de clientes podría usar Data Mining predictivo para identificar a los clientes con riesgo de "churn" (cancelar su suscripción).
    *   **Proceso:**
        *   Se recolectarían datos históricos del DW sobre el comportamiento de los usuarios (tiempo de suscripción, frecuencia de uso, géneros escuchados, quejas al soporte, interacciones con la app).
        *   Un algoritmo de Machine Learning (ej. Random Forest, Regresión Logística) se entrenaría con estos datos para aprender patrones que preceden a la cancelación de la suscripción.
        *   Una vez entrenado, el modelo se aplicaría a los clientes activos para calcular una "Puntuación de Riesgo de Churn" para cada uno.
    *   **Acción:** Los clientes con una alta puntuación de riesgo recibirían ofertas personalizadas, descuentos o un contacto proactivo del servicio al cliente para intentar retenerlos antes de que cancelen.

---

