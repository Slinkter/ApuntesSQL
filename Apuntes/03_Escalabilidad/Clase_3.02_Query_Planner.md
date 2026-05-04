# Clase 3.02: Dominando el Query Planner

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: EXPLAIN ANALYZE no miente

En 2013, cuando las consultas SQL de tu Mueblería o de tu Práctica 3 de Películas se ralentizaban, la única pista solía ser mirar el reloj de arena del cliente SQL. En un sistema crítico en 2026, adivinar por qué una consulta se atasca es inaceptable. Tú debes interrogar a PostgreSQL para entender la "Ruta de Ejecución".

El comando `EXPLAIN ANALYZE` no ejecuta la consulta "en vacío" (sólo estimación), la ejecuta **realmente** en la base de datos midiendo tiempos de I/O en milisegundos reales y leyendo el comportamiento de los Buffers.

### Desentrañando el Plan de Ejecución

Un Plan de Consultas en PostgreSQL se lee de adentro hacia afuera (Bottom-Up) y de arriba hacia abajo (Top-Down). PostgreSQL utiliza un "Optimizador Basado en Costos" (CBO). Él calcula si los datos están fragmentados probando internamente diferentes métodos algorítmicos. Las piezas críticas que verás:

1.  **Sequential Scan (`Seq Scan`) / Table Access Full:** Leer la tabla desde el bloque de inicio hasta el bloque final, ignorando índices. Solo es bueno cuando necesitas descargar _toda_ la tabla, o si la tabla es en extremo diminuta y cabe en 1 sola página de memoria (8KB). De lo contrario, este nodo es tu enemigo mortal de rendimiento general.
2.  **Index Scan:** Usar el B-Tree para encontrar los `IDs`. Luego, usar esos IDs para ir a buscar al Heap las columnas que la consulta pidió. El método estándar efectivo.
3.  **Index Only Scan:** El "Santo Grial" del rendimiento. PostgreSQL usa el "Visibility Map". Si **todas** las columnas que solicitaste (`SELECT id, fecha`) ya están almacenadas como "Covering Indexes" dentro de tu propio índice (Ej: `idx_ordenes(id) INCLUDE (fecha)`), Postgres **no viajará jamás a la gigantesca tabla en el disco (Heap)**, sino que las entregará desde la propia estructura comprimida del índice.

## 2. Integración SDLC: Los JOINs Algorítmicos

Cuando unes dos tablas gigantes (`orden_pedido` con `producto_ordenado`), el motor debe decidir **cómo** fusionarlas. Existen tres metodologías que observarás en tu plan de ejecución, y como arquitecto debes entender por qué PostgreSQL escogió una u otra:

- **Nested Loop Join:** Funciona como dos bucles "For" anidados de programación imperativa. Bucle externo: 1.000 filas filtradas, Bucle interno: Buscar usando un `Index Scan`. Excelente para subconjuntos muy pequeños limitados por un `WHERE`.
- **Hash Join:** Crea en RAM una Hash Table extremadamente rápida de la tabla más pequeña unida, luego barre la tabla más grande cotejando contra ese diccionario en memoria. **Es la herramienta letal 2026** de PostgreSQL para unir cientos de miles de registros sin índices, pero debes vigilar agresivamente la configuración de tu `work_mem` (tu RAM disponible por nodo de consulta), para evitar que esa Hashtable se desborde al disco duro causando caídas abismales ("Disk Hash Join").
- **Merge Join:** Supone que las dos tablas gigantes llegan ya **ordenadas previamente**. Va fusionándolas como una cremallera. Rápido, masivo, pero su cuello de botella es el nodo previo de "Sort" explícito.

## 3. Reto de Observabilidad (Laboratorio DML)

**El Escenario:**
Un ingeniero junior escribió una vista (`CREATE VIEW vistazo_peliculas_actor`) para resolver la Pregunta 2 de la Práctica 3 de tu universidad en 2013 (la del actor Charlton Heston).

La vista simplemente hace un `SELECT *` uniendo el millón de Películas interactuando con las Categorías, los Directores y los Actores.
Luego, en su aplicación de backend con Prisma/TypeORM, ejecuta un DML final: `SELECT * FROM vistazo_peliculas_actor WHERE nombre_actor = 'Charlton Heston'`.

En su máquina (BD de 10 megas) tarda 5ms. En Producción (BD de 100GB con caché fría) colapsa la memoria.

**El Diagnóstico de Arquitecto:**
Cuando ejecutas `EXPLAIN (ANALYZE, BUFFERS) SELECT ...`, ves nodos espantosos de:

1. `Sort (Disk)`
2. `Hash Join`
3. Un `Nested Loop` que ejecuta el nodo interno unas 500,000 veces (`loops=500000`).

**El Reto:**
¿Puedes explicar, como Senior Architect, qué defecto de diseño en el uso de esa `VIEW` por parte del desarrollador (utilizando un `SELECT *` oculto y filtrando por fuera) está causando que PostgreSQL ignore la selectividad del índice de 'Charlton Heston' y obligue al motor a materializar en memoria RAM toda la historia cineasta masiva antes del filtrado agresivo?
