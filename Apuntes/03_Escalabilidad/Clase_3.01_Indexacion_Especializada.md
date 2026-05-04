# Clase 3.01: Indexación Especializada

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: El B-Tree ya no es suficiente

En la década de 2010, la respuesta universal a "mi consulta es lenta" era "agrégale un índice". Por omisión, al ejecutar `CREATE INDEX`, el 99% de los motores (incluyendo PostgreSQL) crean un **B-Tree** (Balanced Tree).

El B-Tree es fantástico para buscar igualdades escalares (`id = 5`) o rangos pequeños (`fecha BETWEEN 'x' AND 'y'`). Funciona navegando desde la raíz del árbol hacia las hojas. Pero en arquitecturas de datos intensivos (2026), trabajamos con textos gigantes, coordenadas GPS (Geolocalización) y documentos JSON masivos. El B-Tree falla miserablemente ante estos tipos de datos.

### El Arsenal de un Arquitecto de Datos

Debes conocer cuándo aplicar los índices especializados de PostgreSQL:

- **GIN (Generalized Inverted Index):** El motor principal para búsquedas tipo "Google". Ideal para documentos `JSONB`, arreglos (`ARRAY`) o Búsqueda de Texto Completo (Full Text Search - FTS). En lugar de indexar la fila, documenta cada valor individual dentro del documento y te dice en qué filas se encuentra.
- **GiST (Generalized Search Tree):** El titán de las búsquedas espaciales y de geometría (PostGIS). Si necesitas hacer una consulta: _"Encuentra todos los restaurantes a 2 km de mis coordenadas actuales"_, GiST, trabajando con _Bounding Boxes_ superpuestas (R-Trees), lo resuelve en submilisegundos. También excelente para superposición de rangos (`daterange` o `tsrange`).
- **BRIN (Block Range Index):** El secreto mejor guardado para el ahorro masivo de Terabytes. Si tienes una tabla de Big Data (Ej. Logs de eventos de un año de tu Mueblería de 10.000 millones de filas), un B-Tree ocuparía 500 GB solo de índice, hundiendo tu RAM. Un **BRIN** en cambio, solo almacena los valores _Mínimos_ y _Máximos_ de páginas secuenciales de bloques. Usará literalmente 5 MB de espacio, siendo brutalmente rápido para consultas por fechas (`WHERE timestamp BETWEEN X AND Y`) en tablas donde los datos se escriben naturalmente en orden temporal (Append-Only).

## 2. Integración SDLC: Índices Parciales y Funcionales

Los ingenieros comunes indexan las columnas.
Los arquitectos indexan **los patrones de consulta**.

### Índices Funcionales (Expression Indexes)

Imagina tu código legado haciendo: `SELECT * FROM clientes WHERE LOWER(email) = 'test@test.com'`.
Esa función `LOWER()` envuelta alrededor de la columna anula automáticamente un índice B-Tree normal sobre `email` (provocando un "Full Table Scan").
En Postgres 15+ usamos índices aplicados a funciones exactas:
`CREATE INDEX idx_clientes_email_lw ON clientes (LOWER(email));`

### Índices Parciales

Supón que gestionas la tabla de `orden_pedido` (de tu silabo), que tiene 5 Millones de órdenes históricas (Canceladas, Entregadas, Fallidas), pero el negocio **solo** consulta ávidamente las "Pendientes" (que son unas 200).

- **Antipatrón:** Crear un índice sobre la columna `estado`. PostreSQL ignorará el índice si más del 20% de la tabla comparte el valor, porque es más barato para el disco leer secuencialmente.
- **Solución 2026:** `CREATE INDEX idx_ordenes_pendientes ON orden_pedido (fecha_colocacion) WHERE estado = 'PENDIENTE';`
    - Este índice de 5 KB de peso solo existe en disco para esas 200 filas. Es microscópico, rapidísimo de actualizar (porque no tienes que actualizarlo si la orden ya 'Se Entregó') y se ajusta como un guante a tu necesidad transaccional.

## 3. Reto de Laboratorio: BRIN vs B-Tree

**El Escenario:**
Has rediseñado la tabla `producto_ordenado` (Ventas de detalle). Tienes 5 Terabytes de datos históricos correspondientes a 8 años de ventas, almacenados en PostgreSQL.
Cada noche hay reportes que dicen: `SELECT sum(cantidad * precio) FROM producto_ordenado WHERE fecha_venta BETWEEN '2026-01-01' AND '2026-01-31';`

**El Problema Operativo:**

1. Crear un índice tradicional **B-Tree** de fechas sobre 5 TB de datos consumirá muchísimos GB de tu preciosa Memoria RAM para estar "caliente" (útil), y ralentizará severamente el ingreso de nuevas ventas diarias (`INSERTs`).
2. Sin embargo, no crear NADA, obligará a barrer 5 TB diariamente (_Full Scan_).

**El Reto (Pensamiento de DBA Senior):**
El Senior DBA sugiere usar `BRIN`. Explícamé por qué el índice BRIN sería perfecto en este caso de registros "históricos de ventas" frente al índice B-Tree, y de qué forma evitaría que tu memoria RAM se termine colapsando.
