# Ejercicios Resueltos - Clase 15: Data Warehouse (Arquitectura y Explotación)

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
