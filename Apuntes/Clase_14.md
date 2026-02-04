# Clase 14: Data Warehouse: Conceptos, Arquitectura y Diseño

---

## 📚 Conceptos Clave

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### ¿Qué es un Data Warehouse?

Un Data Warehouse (DW), o Almacén de Datos, es un sistema diseñado para el almacenamiento de grandes volúmenes de datos históricos provenientes de diversas fuentes operacionales. Su propósito principal es apoyar el análisis empresarial, la toma de decisiones y la generación de informes (Business Intelligence - BI), más que las operaciones diarias de una empresa.

**Características Clave de un Data Warehouse (según Bill Inmon):**
*   **Orientado a Temas (Subject-Oriented):** Los datos se organizan en torno a temas importantes del negocio (ej. clientes, productos, ventas) en lugar de procesos operacionales.
*   **Integrado (Integrated):** Los datos se consolidan de múltiples fuentes dispares, se limpian y se transforman para asegurar la consistencia y la uniformidad.
*   **Variante en el Tiempo (Time-Variant):** Los datos en el DW representan una serie de puntos en el tiempo, permitiendo el análisis de tendencias y patrones históricos. Se registra cuándo es válido un dato.
*   **No Volátil (Non-Volatile):** Una vez que los datos se cargan en el Data Warehouse, no se modifican ni se eliminan. Se añaden nuevos datos periódicamente, pero los datos existentes permanecen estables para el análisis histórico.

### Diferencias entre OLTP y OLAP

Es fundamental distinguir entre los sistemas de procesamiento de transacciones en línea (OLTP) y los sistemas de procesamiento analítico en línea (OLAP), que es el rol principal de un DW:

| Característica        | OLTP (Online Transaction Processing)             | OLAP (Online Analytical Processing)              |
| :-------------------- | :----------------------------------------------- | :----------------------------------------------- |
| **Propósito**         | Soporte a operaciones diarias, transacciones     | Soporte a la toma de decisiones, análisis        |
| **Tipo de Datos**     | Datos actuales, detallados, optimizados para escritura | Datos históricos, resumidos, optimizados para lectura |
| **Esquema**           | Normalizado (ej. 3FN)                            | Desnormalizado (ej. Esquema en Estrella)         |
| **Operaciones**       | `INSERT`, `UPDATE`, `DELETE` frecuentes          | `SELECT` complejas, agregaciones, drill-down     |
| **Usuarios**          | Empleados operacionales                          | Analistas de datos, gerentes                     |
| **Rendimiento**       | Rápido para transacciones pequeñas               | Rápido para consultas complejas                  |

### Arquitectura de un Data Warehouse

Una arquitectura típica de Data Warehouse incluye:
1.  **Fuentes de Datos Operacionales:** Sistemas transaccionales, ERPs, CRMs, archivos planos, etc.
2.  **Área de Staging (Staging Area):** Un área temporal donde los datos se extraen, se limpian y se transforman antes de cargarse en el DW.
3.  **Data Warehouse Central:** El repositorio principal de datos integrados y variantes en el tiempo.
4.  **Data Marts:** Subconjuntos del Data Warehouse, orientados a un departamento o área de negocio específica, diseñados para satisfacer necesidades analíticas particulares.
5.  **Herramientas de BI y Presentación:** Herramientas de reporting, dashboards, cubos OLAP, minería de datos, etc., que utilizan los datos del DW.

### Modelado de Datos para Data Warehouses

Los modelos de datos tradicionales (normalizados) no son óptimos para consultas analíticas. En DW, se prefieren modelos dimensionales:

*   **Esquema en Estrella (Star Schema):** El modelo más común. Consiste en una **Tabla de Hechos (Fact Table)** central rodeada por múltiples **Tablas de Dimensiones (Dimension Tables)**. Las tablas de dimensiones no están normalizadas o lo están muy poco.
    *   **Tabla de Hechos:** Contiene las métricas o medidas numéricas del negocio (ej. cantidad vendida, precio, coste) y claves foráneas a las tablas de dimensiones.
    *   **Tabla de Dimensiones:** Contiene los atributos descriptivos de los "quién, qué, dónde, cuándo, cómo" del negocio (ej. Cliente, Producto, Tiempo, Ubicación).
*   **Esquema Copo de Nieve (Snowflake Schema):** Similar al esquema en estrella, pero las tablas de dimensiones están parcial o totalmente normalizadas, extendiéndose en ramas como un copo de nieve. Reduce la redundancia, pero aumenta la complejidad de las consultas.

### Proceso ETL (Extract, Transform, Load)

El ETL es la columna vertebral de cualquier Data Warehouse:
*   **Extracción (Extract):** Obtener datos de las diversas fuentes operacionales.
*   **Transformación (Transform):** Limpiar, consolidar, estandarizar y reformatear los datos para que sean coherentes y aptos para el análisis. Incluye la aplicación de reglas de negocio y agregaciones.
*   **Carga (Load):** Mover los datos transformados al Data Warehouse (carga inicial o incremental).

### Cubos OLAP

Los cubos OLAP son estructuras multidimensionales que pre-agregan y organizan los datos del Data Warehouse para un acceso y análisis rápidos. Permiten realizar operaciones como `drill-down` (ver más detalle), `roll-up` (ver menos detalle/más agregación), `slice` (filtrar por una dimensión) y `dice` (seleccionar un subcubo).

---

## Pistas y Keywords

*   **Data Warehouse (DW):** Almacén de datos para análisis.
*   **OLTP:** Procesamiento Transaccional Online (operacional).
*   **OLAP:** Procesamiento Analítico Online (analítico).
*   **Orientado a Temas:** Datos enfocados en aspectos de negocio.
*   **Integrado:** Datos consolidados de múltiples fuentes.
*   **Variante en el Tiempo:** Datos con contexto histórico.
*   **No Volátil:** Datos no modificables una vez cargados.
*   **Arquitectura DW:** Componentes de un sistema DW (fuentes, staging, DW, marts, BI).
*   **Staging Area:** Área temporal para preparación de datos.
*   **Data Mart:** Subconjunto temático o departamental del DW.
*   **Esquema en Estrella:** Modelo dimensional con tabla de hechos central y dimensiones.
*   **Esquema Copo de Nieve:** Esquema en estrella con dimensiones normalizadas.
*   **Tabla de Hechos (Fact Table):** Contiene medidas y claves foráneas.
*   **Tabla de Dimensiones (Dimension Table):** Contiene atributos descriptivos.
*   **ETL:** Extract, Transform, Load (proceso de carga de datos).
*   **Cubos OLAP:** Estructuras multidimensionales para análisis.
*   **Business Intelligence (BI):** Conjunto de estrategias y herramientas para transformar datos en conocimiento.

---

## Resumen Final Crítico

El Data Warehouse es una pieza central en la estrategia de Business Intelligence de cualquier organización, ofreciendo una visión unificada e histórica de los datos para facilitar el análisis y la toma de decisiones informadas. Su diseño, que contrasta marcadamente con los sistemas OLTP, se centra en la optimización de las consultas de lectura a través de modelos dimensionales como el esquema en estrella. El proceso ETL es vital para asegurar la calidad y consistencia de los datos, mientras que los cubos OLAP proporcionan herramientas poderosas para la exploración multidimensional. Aunque la implementación de un DW es un esfuerzo considerable, los beneficios en términos de inteligencia empresarial y ventaja competitiva son invaluables.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Los conceptos de modelado de datos (Clase 06, 07 y 09) y SQL (Clase 05, 10, 11) son fundamentales para entender cómo los datos se estructuran en el DW y cómo se extraen y transforman. Los conocimientos de programación en PL/SQL (Clase 12 y 13) son útiles para implementar el proceso ETL y desarrollar rutinas de carga.
*   **Conexiones Siguientes:** Esta clase proporciona la base para la comprensión de los Tópicos Avanzados de Bases de Datos (Clase 15), donde se podrían explorar temas como Big Data, bases de datos NoSQL, o herramientas más específicas de Business Intelligence y Data Science que operan sobre infraestructuras de Data Warehouse. También se conecta con los objetivos de proyectos finales que requieren análisis de datos empresariales.

---

