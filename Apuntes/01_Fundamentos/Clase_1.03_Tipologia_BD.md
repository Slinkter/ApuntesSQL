# Clase 1.03: Tipología de Bases de Datos en la Era Cloud

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: El Fin de una Era Monocasco

Si observas todo el plan de estudios original de 2013, la única base de datos que existía en el universo era la Relacional (RDBMS), y la herramienta para todo problema era SQL.

En 2026, intentar resolver cada problema de arquitectura de software únicamente con PostgreSQL es un claro antipatrón (el famoso "Golden Hammer"). Hoy entendemos que los sistemas distribuidos requieren herramientas especializadas según los patrones de lectura y escritura de la aplicación.

### El Espectro de Motores de Persistencia Modernos

1.  **Bases de Datos Relacionales (RDBMS): PostgreSQL, MySQL**
    - **Su Fuerza:** Integridad transaccional absoluta (ACID), operaciones estructuradas complejas (JOINs masivos) y madurez de su ecosistema. En Postgres 15+ tienes capacidades analíticas y documentales con JSONB que difuminan la línea entre RDBMS y NoSQL.
    - **Su Debilidad Histórica:** Escalabilidad horizontal nativa. Aunque existen extensiones como Citus para sharding, lidiar con escalado escribiendo a través de múltiples nodos geográficos sigue siendo complejo.

2.  **NoSQL Orientado a Documentos (MongoDB, Couchbase)**
    - **Su Fuerza:** Flexibilidad pura (_Schema-on-read_). Perfecto para catálogos de productos donde cada ítem tiene atributos diferentes y el volumen de datos obliga a distribuir rápidamente sin las fricciones de bloqueo de un esquema rígido. Si la aplicación cambia de versión frecuentemente, no necesitas planificar complicadas migraciones de tablas DDL.

3.  **NoSQL de Familias de Columnas (Cassandra, ScyllaDB)**
    - **Su Fuerza:** Ingesta MASIVA y escalado multi-datacenter maestro-maestro (Masterless). Excelente para casos de uso IoT (Telemetría de millones de sensores).
    - **El Precio a Pagar:** Debes modelar tu base de datos basándote EXACTAMENTE en la consulta que harás (Modelado Basado en Query). No hay "JOINs" en disco eficientes, toda la desnormalización debe ocurrir en el diseño.

4.  **Graph Databases (Neo4j)**
    - **Su Fuerza:** Relaciones altamente conectadas (Rutas logísticas, Análisis de Fraude, Redes Sociales). Si tienes en un RDBMS tablas con referencias a sí mismas, obligando consultas recursivas ineficientes de 10 niveles de profundidad, un recorrido por grafos (Cypher) lo hará exponencialmente más rápido.

5.  **NewSQL y Vector Databases (CockroachDB / Pinecone, pgvector)**
    - **El Estado del Arte 2026:** Los NewSQL nacen para arreglar el gran defecto del RDBMS: brindan semántica SQL y compatibilidad ACID, pero distribuyen los datos y toleran fallos de nodos en arquitecturas nativas de Cloud (Kubernetes). Y por otra parte, la explosión de Inteligencia Artificial obliga al almacenamiento de _Embeddings_, integrando bases de datos puramente vectoriales o capacidades híbridas directamente en el motor.

## 2. Integración SDLC: La Arquitectura Políglota

En un Ciclo de Desarrollo Moderno, tu microservicio "A" usa Postgres, tu microservicio "B" de analítica de logs usa Elasticsearch, y tu microservicio "C" para los carritos de compras usa Redis.

Tu trabajo como Data Architect no es saber escribir la sentencia de `CREATE TABLE` más compleja, sino diseñar el **Data Mesh**: cómo los eventos y transacciones cruzan de forma resiliente estas tecnologías divergentes.

## 3. Reto de Arquitectura Políglota (Laboratorio)

**El Escenario:**
Piensa en el trabajo final de 2013 (crear reportes de bodega con procedimientos almacenados en una sola DB).

Imagina que hoy te contrata Netflix. Su modelo de datos no puede vivir en un solo Oracle. Ellos manejan:

1.  **Perfiles de Usuarios y Pagos:** (Súper crítico, no puedes perder facturas, millones de operaciones de cobros por mes).
2.  **Catálogo de Películas:** (Altamente distribuido globalmente, los clientes buscan por múltiples metadatos y categorías cambiantes).
3.  **El Motor de Recomendaciones:** (Relaciona lo que ven tus amigos y gente como tú, para recomendar qué ver a continuación en tiempo real).

**El Reto de Decisión Arquitectónica:**
Asigna a cada caso de uso anterior (1, 2 y 3) una Categoría de Base de Datos moderna (RDBMS, Documental, Grafos, Familias de Columnas, en memoria, etc.) y justifica por qué el enfoque clásico de 2013 (ponerlo todo en tablas relacionales con _triggers_) generaría un desastre masivo a escala global.
