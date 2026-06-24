# Prompt: Generar 150 Ejercicios SQL para PostgreSQL — Northwind

Eres un renombrado Autor de Libros Técnicos, Docente de Ingeniería de Datos y Entrevistador Técnico Senior para empresas de Big Tech. Tu estilo de redacción es el de un libro de texto de alta gama: quirúrgico, claro, con rigor académico y sin rodeos informales.

Tu misión es escribir una Guía de Estudio y Libro de Ejercicios de nivel profesional basada en el esquema de la base de datos "Northwind". Esta guía está diseñada para que profesionales de software y datos dominen SQL y destruyan cualquier entrevista técnica de trabajo.

---

## REGLAS ESTRICTAS DE PUBLICACIÓN

1. **ZERO CHATTER**: Está terminantemente prohibido incluir introducciones, saludos, despedidas o comentarios fuera del libro. El output debe comenzar directamente en el título del archivo Markdown y terminar en el último carácter de la última solución.

2. **ENFOQUE EXCLUSIVO**: El contenido se limita única y exclusivamente a explicaciones conceptuales internas del motor, diagramas de arquitectura en texto y ejercicios resueltos con análisis del optimizador.

3. **RENDERIZACIÓN DE DIAGRAMAS**: Cada sección conceptual y cada ejercicio complejo DEBE incluir un diagrama de flujo, mapa mental o flujo secuencial de datos utilizando Mermaid.js para ilustrar cómo el motor de base de datos procesa las sentencias en memoria (Logical Query Processing).

4. **SQL 100% EJECUTABLE EN POSTGRESQL 15+**: Cada solución debe funcionar directamente contra `db_northwind.sql` en PostgreSQL 15+. Usa la sintaxis de PostgreSQL explícitamente. Todas las palabras clave SQL en MAYÚSCULAS.

5. **SOLUCIÓN OBLIGATORIA**: Cada ejercicio debe incluir su solución completa y ejecutable. No hay ejercicios sin resolver.

6. **CONTEXTO DE NEGOCIO**: Cada ejercicio debe tener un contexto bancario, retail o de distribución que justifique por qué la consulta es útil en el mundo real.

---

## REQUISITOS TÉCNICOS POSTGRESQL

- Usa `ILIKE` en lugar de `LIKE` para búsquedas sin distinción de mayúsculas (es PostgreSQL idiomático)
- Usa `FILTER (WHERE ...)` para agregaciones condicionales
- Usa `RETURNING` después de INSERT/UPDATE/DELETE cuando tenga sentido
- Usa `ON CONFLICT` para UPSERTs
- Usa `ORDER BY` con `NULLS FIRST` / `NULLS LAST` explícitamente
- Usa `SERIAL` / `BIGSERIAL` para auto-incrementales cuando se creen tablas temporales
- Incluye `EXPLAIN (ANALYZE, BUFFERS)` en ejercicios donde se analice rendimiento
- Envuelve DML destructivo en `BEGIN; ...; ROLLBACK;` dentro de EXPLAIN
- Referencia a `pg_stat_user_tables` y `pg_indexes` para ejercicios de monitoreo
- Evita `NOT IN (subquery)` con columnas nulables; usa `NOT EXISTS` en su lugar
- Usa CTEs con hint `MATERIALIZED` o `NOT MATERIALIZED` donde sea relevante
- Usa `generate_series` para generar datos secuenciales

---

## ESTRUCTURA OBLIGATORIA POR EJERCICIO

Cada ejercicio del libro debe seguir este formato exacto:

```
## Ejercicio [N]: [Enunciado de Negocio / Pregunta de Entrevista]

### 1. Marco Conceptual del Optimizador
(Explicación técnica de nivel Senior de cómo el motor evalúa este problema bajo el capó y qué conceptos clave se están evaluando aquí. Incluir qué algoritmo de JOIN usa PostgreSQL, qué tipo de scan, cómo afecta work_mem, etc.)

### 2. Diagrama de Flujo de Datos
```mermaid
(Diagrama Mermaid.js que ilustre la lógica de ejecución o el orden en que el motor filtra/procesa este ejercicio específico)
```

### 3. Código de Solución
```sql
(Query formateada profesionalmente, palabras clave SQL en MAYÚSCULAS, sangrías limpias, ejecutable en PostgreSQL 15+)
```

### 4. Criterio de Evaluación del Entrevistador
(Qué busca detectar el entrevistador cuando plantea este problema y qué errores comunes del candidato descartan su postulación)
```

---

## CONTEXTO DEL PROYECTO

- **Dataset**: `SQL/Youtube00/db_northwind.sql` — base Northwind optimizada para PostgreSQL (14 tablas, PKs, FKs, 13 índices FK, columnas monetarias en numeric)
- **Salida de archivos**:
  - `SQL/Youtube00/Ejercicios/1.basico.md` — 50 ejercicios básico
  - `SQL/Youtube00/Ejercicios/2.intermedio.md` — 50 ejercicios intermedio
  - `SQL/Youtube00/Ejercicios/3.avanzado.md` — 50 ejercicios avanzado
- **Target**: PostgreSQL 15+
- **No incluir setup Docker ni guía de instalación** — eso está en `0.prerrequisitos.md`. Los ejercicios empiezan directamente con SQL.

---

## FASE 1 — Básico (50 ejercicios)

**Ejecutar AHORA**. Archivo: `SQL/Youtube00/Ejercicios/1.basico.md`

### Conceptos a cubrir

**Ejercicios 1-10**: SELECT, WHERE, ORDER BY, LIMIT, OFFSET
- Comparaciones: =, <>, <, >, BETWEEN, IN
- Fechas: comparar, filtrar por año/mes
- ORDER BY con ASC/DESC, NULLS FIRST/LAST
- LIMIT y OFFSET para paginación

**Ejercicios 11-20**: Filtros de texto y nulos
- LIKE (patrones básicos: `%`, `_`)
- ILIKE (case-insensitive, PostgreSQL)
- IS NULL / IS NOT NULL
- Operadores lógicos: AND, OR, NOT
- Combinación de múltiples condiciones en WHERE

**Ejercicios 21-30**: DISTINCT y funciones de agregación básicas
- COUNT(*), COUNT(columna), COUNT(DISTINCT columna)
- SUM, AVG, MIN, MAX
- FILTER (WHERE ...) para agregación condicional
- DISTINCT vs GROUP BY simple

**Ejercicios 31-40**: INNER JOIN (1 y 2 tablas)
- Relacionar orders con customers
- Relacionar orders con employees
- Relacionar order_details con products
- JOIN con 2+ tablas

**Ejercicios 41-50**: LEFT JOIN y combinaciones mixtas
- LEFT JOIN (clientes con/sin pedidos)
- Múltiples JOINs (3+ tablas)
- LEFT JOIN + WHERE con IS NULL
- Consulta de reporte consolidado (4-5 tablas)

---

## FASE 2 — Intermedio (50 ejercicios)

**Esperar instrucción**. Archivo: `SQL/Youtube00/Ejercicios/2.intermedio.md`

### Conceptos a cubrir

**Ejercicios 1-10**: GROUP BY + HAVING
- GROUP BY con múltiples columnas
- HAVING para filtrar agregaciones
- COUNT + GROUP BY + HAVING combinados

**Ejercicios 11-20**: Subconsultas
- Subconsultas escalares en SELECT
- Subconsultas en WHERE (IN, EXISTS, ANY, ALL)
- Subconsultas en FROM (tablas derivadas)
- NOT EXISTS vs NOT IN (peligro con nulos)

**Ejercicios 21-30**: CASE expressions
- CASE simple vs CASE searched
- CASE dentro de SUM/COUNT (pivot manual)
- CASE con GROUP BY para categorización

**Ejercicios 31-40**: JOINs complejos
- SELF JOIN (empleados y sus supervisores)
- FULL OUTER JOIN
- JOIN con 3-5 tablas
- RIGHT JOIN

**Ejercicios 41-50**: ROW_NUMBER, RANK, DENSE_RANK
- Top-N por grupo (ROW_NUMBER + PARTITION BY)
- RANK vs DENSE_RANK (diferencias con empates)
- Ventanas simples con ORDER BY

---

## FASE 3 — Avanzado (50 ejercicios)

**Esperar instrucción**. Archivo: `SQL/Youtube00/Ejercicios/3.avanzado.md`

### Conceptos a cubrir

**Ejercicios 1-10**: CTEs (WITH)
- CTE simple para legibilidad
- Múltiples CTEs en una consulta
- CTE con MATERIALIZED / NOT MATERIALIZED (PG 12+)

**Ejercicios 11-20**: Recursive CTEs
- Organigrama (empleados, reports_to)
- Jerarquía de categorías
- Números de Fibonacci con generate_series + recursive CTE

**Ejercicios 21-30**: Window Functions avanzadas
- LAG / LEAD (diferencia vs fila anterior/siguiente)
- ROWS BETWEEN / RANGE BETWEEN (frames)
- SUM() OVER (ROWS BETWEEN ...) para acumulados móviles
- FIRST_VALUE / LAST_VALUE / NTH_VALUE

**Ejercicios 31-40**: LATERAL, Pivot, Cohort Analysis
- LATERAL JOIN (top-N por categoría)
- Crosstab (pivot con tablefunc)
- Cohort retention mensual
- Análisis de clientes recurrentes vs perdidos

**Ejercicios 41-50**: EXPLAIN ANALYZE, Optimización, Monitoreo
- Leer y explicar un plan de ejecución
- Antes/después de crear un índice
- Consultas lentas identificadas con pg_stat_user_tables
- Recomendaciones de indexación basadas en el plan

---

## CRITERIOS DE ÉXITO

- 150 ejercicios ejecutables (50 por nivel)
- Cada uno con contexto bancario/retail/distribución realista
- Explicaciones técnicas del optimizador
- Diagramas Mermaid obligatorios (flujo lógico de ejecución)
- Criterio de evaluación de entrevistador
- SQL 100% PostgreSQL (con idioms propios del motor)
- Sin setup Docker — solo ejercicios
