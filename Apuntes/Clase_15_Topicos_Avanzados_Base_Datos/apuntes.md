# Clase 15: Tópicos Avanzados de Bases de Datos

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Introducción a los Tópicos Avanzados

Los tópicos avanzados de bases de datos exploran tecnologías y conceptos que van más allá de las bases de datos relacionales tradicionales, abordando desafíos modernos como el volumen masivo de datos (Big Data), la necesidad de alta disponibilidad, el rendimiento extremo y la gestión de datos no estructurados o semiestructurados.

### Bases de Datos NoSQL

Las bases de datos NoSQL ("Not only SQL") surgieron para abordar las limitaciones de las bases de datos relacionales en escenarios de Big Data, escalabilidad horizontal, agilidad en el desarrollo y manejo de datos no estructurados. Se clasifican típicamente en varios tipos:

*   **Bases de Datos Clave-Valor:** Almacenan datos como una colección de pares clave-valor. Simples, rápidas y altamente escalables. Ej: Redis, DynamoDB.
*   **Bases de Datos Orientadas a Documentos:** Almacenan datos en documentos flexibles, generalmente en formatos como JSON o BSON. Ideal para datos semiestructurados y cambios de esquema frecuentes. Ej: MongoDB, Couchbase.
*   **Bases de Datos Orientadas a Columnas (Wide-Column Stores):** Almacenan datos en familias de columnas, lo que permite un acceso eficiente a grandes volúmenes de datos dispersos en muchas máquinas. Ej: Cassandra, HBase.
*   **Bases de Datos Orientadas a Grafos:** Almacenan datos como nodos (entidades) y aristas (relaciones) que conectan esos nodos. Optimizadas para manejar relaciones complejas y consultas de grafos. Ej: Neo4j, ArangoDB.

### Big Data

Se refiere a conjuntos de datos tan grandes y complejos que las herramientas tradicionales de procesamiento de datos no pueden gestionarlos eficazmente. Se caracteriza por las "3 Vs":
*   **Volumen:** Cantidades masivas de datos.
*   **Velocidad:** Datos generados y procesados a alta velocidad.
*   **Variedad:** Datos de diferentes tipos y formatos (estructurados, semiestructurados, no estructurados).
A menudo, la gestión de Big Data implica el uso de sistemas distribuidos como Hadoop y Spark.

### Bases de Datos en la Nube (Cloud Databases)

Servicios de bases de datos ofrecidos por proveedores de nube (AWS, Azure, Google Cloud) que permiten a los usuarios aprovisionar, escalar y gestionar bases de datos sin la necesidad de administrar la infraestructura subyacente. Ofrecen flexibilidad, escalabilidad y alta disponibilidad. Ej: Amazon RDS, Azure SQL Database, Google Cloud Spanner.

### Bases de Datos en Memoria (In-Memory Databases - IMDB)

Almacenan todos o la mayoría de los datos en la memoria principal (RAM) de la computadora en lugar de en el disco. Esto resulta en tiempos de acceso a datos y rendimiento de consultas significativamente más rápidos, ideal para aplicaciones que requieren baja latencia y procesamiento en tiempo real. Ej: SAP HANA, Redis, VoltDB.

### Procesamiento Paralelo y Distribuido

Técnicas que involucran la división de tareas de procesamiento de datos entre múltiples procesadores o nodos de una red para acelerar la ejecución. Es fundamental para Big Data y sistemas de bases de datos escalables.
*   **Sharding:** División de una base de datos en piezas más pequeñas y manejables (fragmentos) distribuidas en múltiples servidores.
*   **Replicación:** Creación de múltiples copias de los datos en diferentes ubicaciones para asegurar la alta disponibilidad y la recuperación ante desastres.

### Seguridad Avanzada en Bases de Datos

Más allá de los controles de acceso básicos, incluye:
*   **Cifrado de Datos:** Proteger los datos en reposo y en tránsito.
*   **Enmascaramiento de Datos:** Ocultar datos sensibles para entornos de desarrollo/pruebas.
*   **Auditoría de Bases de Datos:** Registrar y monitorear todas las actividades de acceso y modificación de datos para detección de anomalías y cumplimiento.
*   **Gestión de Vulnerabilidades:** Identificación y mitigación de debilidades de seguridad en el software de la base de datos.

---

## Pistas y Keywords

*   **NoSQL:** Bases de datos no relacionales (clave-valor, documento, columna, grafo).
*   **Big Data:** Volumen, Velocidad, Variedad.
*   **Bases de Datos en la Nube:** DBaaS (Database as a Service).
*   **Bases de Datos en Memoria (IMDB):** Almacenamiento en RAM, alto rendimiento.
*   **Procesamiento Paralelo/Distribuido:** Escalabilidad, Sharding, Replicación.
*   **Seguridad Avanzada (DB):** Cifrado, Enmascaramiento, Auditoría.
*   **Escalabilidad Horizontal:** Añadir más máquinas para capacidad.

---

## Resumen Final Crítico

Los tópicos avanzados de bases de datos reflejan la evolución del campo para satisfacer las crecientes demandas de la era digital, marcada por el Big Data y la necesidad de sistemas altamente escalables, disponibles y seguros. Desde las diversas arquitecturas NoSQL hasta las bases de datos en la nube y en memoria, y las técnicas de procesamiento distribuido, estas innovaciones proporcionan herramientas poderosas para enfrentar desafíos complejos. Comprender estas áreas permite a los profesionales diseñar y gestionar soluciones de datos de vanguardia, adaptadas a requisitos empresariales dinámicos y volúmenes de datos masivos.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase expande los conceptos de diseño y administración de bases de datos vistos en "Bases de Datos Relacionales" (Clase 03) y "Administración de RDBMS" (Clase 04), mostrando alternativas y extensiones a los modelos tradicionales. Los conocimientos de SQL avanzado (Clase 10 y 11) siguen siendo relevantes para interactuar con algunas bases de datos NoSQL y para analizar datos en entornos de Big Data.
*   **Conexiones Siguientes:** Estos tópicos avanzados son cruciales para entender las tendencias actuales en la industria y prepararse para roles en arquitectura de datos, ingeniería de Big Data, o administración de bases de datos en la nube. Proporcionan el contexto para explorar herramientas y plataformas específicas en el ámbito profesional.

---
**Nota:** El contenido de esta clase ha sido inferido del título del curso y conocimientos generales sobre la materia, dado que el archivo `.ppt` original no pudo ser procesado directamente.

---

## Material de Referencia

La siguiente documentación fue utilizada como material de apoyo para esta clase. Se recomienda su revisión para una comprensión más profunda.

*   `../../Ingenieria de datos/otros/Restrictions on Parallel DML.pdf`
*   `../../Ingenieria de datos/otros/Taller_HA_MSSQL2012.pdf`
