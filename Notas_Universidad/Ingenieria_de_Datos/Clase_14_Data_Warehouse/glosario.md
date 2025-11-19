# Glosario - Clase 14: Data Warehouse: Conceptos, Arquitectura y Diseño

*   **Data Warehouse (DW):** Repositorio centralizado de datos históricos de múltiples fuentes, diseñado para el análisis y soporte a la toma de decisiones, no para operaciones diarias.
*   **Business Intelligence (BI):** Conjunto de procesos, tecnologías y herramientas que transforman datos brutos en información significativa y procesable para el análisis empresarial.
*   **Orientado a Temas (Subject-Oriented):** Característica de un DW donde los datos se organizan en torno a las áreas principales de un negocio (ej. ventas, clientes), no a las aplicaciones operacionales.
*   **Integrado (Integrated):** Característica de un DW donde los datos de diversas fuentes se combinan y se estandarizan para proporcionar una vista unificada.
*   **Variante en el Tiempo (Time-Variant):** Característica de un DW que significa que los datos contienen un elemento de tiempo y permiten el análisis de cambios y tendencias históricas.
*   **No Volátil (Non-Volatile):** Característica de un DW que indica que los datos, una vez cargados, no se modifican ni se eliminan; solo se añaden nuevos datos.
*   **OLTP (Online Transaction Processing):** Sistemas transaccionales enfocados en el procesamiento eficiente de grandes volúmenes de transacciones diarias (ej. sistemas de punto de venta, banca en línea).
*   **OLAP (Online Analytical Processing):** Sistemas analíticos enfocados en consultas complejas sobre datos históricos, típicamente para análisis de tendencias, pronósticos y minería de datos.
*   **Staging Area:** Un área temporal dentro de la arquitectura del DW donde los datos se extraen de las fuentes, se limpian y se transforman antes de ser cargados en el Data Warehouse principal.
*   **Data Mart:** Un subconjunto de un Data Warehouse, más pequeño y enfocado en un departamento o área de negocio específica, optimizado para sus necesidades analíticas particulares.
*   **Esquema en Estrella (Star Schema):** Un modelo de datos dimensional popular para DW, que consiste en una tabla de hechos central rodeada por varias tablas de dimensiones directamente relacionadas.
*   **Tabla de Hechos (Fact Table):** En un esquema dimensional, es la tabla central que contiene las medidas numéricas del negocio (hechos) y claves foráneas a las tablas de dimensiones.
*   **Tabla de Dimensiones (Dimension Table):** En un esquema dimensional, es una tabla que contiene los atributos descriptivos para las medidas en la tabla de hechos (ej. cliente, producto, tiempo, ubicación).
*   **Esquema Copo de Nieve (Snowflake Schema):** Una extensión del esquema en estrella donde las tablas de dimensiones se normalizan y se descomponen en tablas adicionales, formando una estructura jerárquica.
*   **ETL (Extract, Transform, Load):** El proceso clave en el llenado de un Data Warehouse, que implica extraer datos de las fuentes, transformarlos para su uso analítico y cargarlos en el DW.
*   **Cubos OLAP:** Estructuras de datos multidimensionales que pre-agregan datos para un acceso y análisis rápidos, permitiendo la exploración desde diferentes perspectivas (dimensiones).
