# Glosario - Clase 12: Data Warehouse (Diseño Dimensional)

*   **Business Intelligence (BI):** Conjunto de estrategias, aplicaciones, datos, productos y tecnologías que permiten el acceso y análisis rápido de la información para mejorar y optimizar la toma de decisiones empresariales.
*   **Copo de Nieve (Modelo Snowflake):** Un modelo de diseño dimensional donde las tablas de dimensión están normalizadas, es decir, las jerarquías dentro de una dimensión se separan en tablas adicionales. Esto reduce la redundancia, pero aumenta la complejidad de las consultas y puede afectar el rendimiento.
*   **Cubos de Datos:** Representación lógica de datos multidimensionales, donde los datos se organizan en "celdas" definidas por combinaciones de valores de dimensiones.
*   **Data Warehouse (DW):** Un sistema centralizado de almacenamiento de datos diseñado específicamente para el análisis y la elaboración de informes, en lugar de para el procesamiento de transacciones diarias.
*   **Dimensión (DW):** En el diseño dimensional, es una entidad de negocio que proporciona el "contexto" o "cómo" analizamos las medidas. Contiene atributos descriptivos (ej. Tiempo, Cliente, Producto, Ubicación).
*   **Diseño Dimensional:** Metodología de diseño de bases de datos utilizada principalmente en Data Warehouses, que organiza los datos en tablas de hechos y tablas de dimensiones.
*   **Estrella (Modelo Star Schema):** El modelo de diseño dimensional más simple y común, donde una tabla de hechos central se conecta directamente a un conjunto de tablas de dimensiones desnormalizadas. Es fácil de entender y optimizado para el rendimiento de consultas analíticas.
*   **Fact Table (Tabla de Hechos):** La tabla central en un esquema dimensional que contiene las "medidas" o hechos cuantitativos (valores numéricos) que se analizan, junto con las claves foráneas que la conectan con las tablas de dimensión.
*   **Hechos (DW):** Los eventos o transacciones de negocio sobre los cuales se quieren realizar análisis (ej. ventas, clics, transacciones bancarias).
*   **Medidas (DW):** Los valores numéricos cuantitativos almacenados en la tabla de hechos que pueden ser agregados y analizados (ej. monto de venta, cantidad de unidades, beneficio).
*   **Miembros (Dimensión):** Los valores individuales o instancias dentro de un nivel de una dimensión (ej. "Enero", "Madrid", "Laptop").
*   **Niveles (Dimensión):** Jerarquías dentro de una dimensión que permiten agrupar y desagrupar datos a diferentes granularidades (ej. en la dimensión Tiempo: Año -> Trimestre -> Mes -> Día).
*   **Repositorio Centralizado:** Un único punto de almacenamiento para los datos de un Data Warehouse, consolidando información de múltiples fuentes.
*   **Transacciones Diarias (OLTP):** Operaciones de procesamiento de transacciones en línea, que se centran en el registro rápido y eficiente de transacciones individuales. Los DW no están optimizados para esto.