const fs = require('fs');
const path = require('path');

const targetFile = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';

let doc = [];

doc.push(`# Guía Maestra de Entrevistas Técnicas SQL - Northwind

> **Motor de Base de Datos:** PostgreSQL 16+ | **Esquema:** Northwind Canónico (\`pthom/northwind_psql\`)  
> **Estructura:** 30 Problemas Reales de Selección | **Duración Estimada:** 120 minutos  
> **Público Objetivo:** Junior Data Analyst $\\to$ Mid BI Developer $\\to$ Senior Data Engineer $\\to$ Lead Database Architect

---

## 🎯 Estructura y Metodología de Evaluación

Este examen técnico simula una prueba técnica exhaustiva para posiciones de datos y arquitectura de bases de datos. Cada pregunta evalúa cuatro pilares fundamentales:
1. **Rigor Sintáctico y Estándar SQL/PostgreSQL:** Uso de sintaxis precisa, funciones nativas óptimas y expresiones portables.
2. **Ciclo de Vida y Orden Lógico del Motor:** Comprensión profunda de la tubería de ejecución del motor PostgreSQL (de \`FROM\` a \`LIMIT\`).
3. **Eficiencia Algorítmica y Uso de Recursos:** Complejidad temporal $O(N)$ y espacial en memoria (\`work_mem\`), escaneos secuenciales vs indexados, y algoritmos de Join y Agregación (\`Hash Join\`, \`Merge Join\`, \`Nested Loop\`, \`HashAggregate\`, \`GroupAggregate\`).
4. **Resiliencia Operacional y Casos de Borde:** Manejo impecable de la lógica trivalente de \`NULL\`, cardinalidades cero, división por cero y condiciones de carrera (\`Race Conditions\`).

### 📊 Matriz de Evaluación por Nivel

| Nivel | Rango Salarial / Rol Típico | Criterio de Aprobación en SQL | Dominio Esperado del Motor |
| :--- | :--- | :--- | :--- |
| **Junior** | Junior Data Analyst / QA Tester | Resuelve filtros, proyecciones, ordenamientos y joins básicos. | Entiende \`SELECT\`, \`WHERE\`, \`ORDER BY\` y el manejo básico de \`NULL\` con \`IS NULL\`. |
| **Mid** | Data Analyst / BI Specialist | Agrupaciones complejas, subconsultas, multi-joins y anti-joins. | Diferencia \`WHERE\` de \`HAVING\`, entiende el orden lógico de ejecución y derived tables. |
| **Senior** | Senior Data Analyst / Data Engineer | Window functions (\`OVER\`, \`PARTITION BY\`, frames), CTEs modulares, \`DISTINCT ON\`. | Domina planes de ejecución, \`ROWS\` vs \`RANGE\`, índices B-Tree/GIN, y escalabilidad. |
| **Lead / Architect** | Lead Data Architect / Principal DBA | Optimización extrema, modelado dimensional, control de concurrencia (\`FOR UPDATE\`). | Domina \`EXPLAIN (ANALYZE, BUFFERS)\`, niveles de aislamiento (\`REPEATABLE READ\`), locking y I/O. |

---

## ⚙️ El Ciclo de Vida del Motor: Pipeline Lógico de 12 Pasos

Para responder con nivel Senior o Principal Architect, es mandatorio dominar el orden en que PostgreSQL evalúa conceptualmente cada cláusula de una consulta SQL:

\`\`\`text
========================================================================================================================
                                PIPELINE LÓGICO DE PROCESAMIENTO SQL (POSTGRESQL 16)
========================================================================================================================
  [1. FROM]       ──► Carga tablas base, evalúa subconsultas derivadas y productos cartesianos iniciales.
  [2. ON]         ──► Evalúa condiciones de cruce booleano por cada combinación de tuplas.
  [3. JOIN]       ──► Aplica preservación de filas (LEFT/RIGHT/FULL OUTER JOIN) e incorpora tuplas no coincidentes.
  [4. WHERE]      ──► Filtra tuplas individuales ANTES de cualquier agregación (no ve alias de SELECT ni agregados).
  [5. GROUP BY]   ──► Colapsa filas en cubetas/grupos según claves de agregación (HashAggregate / GroupAggregate).
  [6. HAVING]     ──► Filtra grupos consolidados basados en funciones de agregación (COUNT, SUM, AVG, MIN, MAX).
  [7. WINDOW]     ──► Evalúa funciones de ventana (OVER, PARTITION BY, ORDER BY, ROWS/RANGE BETWEEN).
  [8. SELECT]     ──► Evalúa expresiones escalares, proyecciones de columnas, llamadas a funciones y asigna alias.
  [9. DISTINCT]   ──► Elimina duplicados de las tuplas proyectadas (Unique / HashAggregate / DISTINCT ON).
  [10. SET OPS]   ──► Combina flujos con UNION / INTERSECT / EXCEPT.
  [11. ORDER BY]  ──► Ordena el conjunto final (Sort / Incremental Sort / Top-N HeapSort) -> ¡SÍ ve alias de SELECT!
  [12. LIMIT/OFF] ──► Acota el número de tuplas devueltas al cliente (Limit node).
========================================================================================================================
\`\`\`

### 🧭 Matriz de Visibilidad de Identificadores y Expresiones
| Cláusula | ¿Puede usar columnas de tabla? | ¿Puede usar alias de SELECT? | ¿Puede usar funciones agregadas? | ¿Puede usar funciones de ventana? |
| :--- | :---: | :---: | :---: | :---: |
| \`FROM / JOIN / ON\` | ✅ Sí | ❌ No | ❌ No | ❌ No |
| \`WHERE\` | ✅ Sí | ❌ No | ❌ No | ❌ No |
| \`GROUP BY\` | ✅ Sí | ❌ No (en SQL estándar) | ❌ No | ❌ No |
| \`HAVING\` | ✅ Sí (si está en GROUP BY) | ⚠️ Solo en PG 15+ (no portable) | ✅ Sí (\`SUM\`, \`COUNT\`) | ❌ No |
| \`WINDOW\` | ✅ Sí | ❌ No | ✅ Sí (agregados sobre partición) | ❌ No anidadas |
| \`SELECT\` | ✅ Sí | ❌ No entre sí (mismo nivel) | ✅ Sí | ✅ Sí |
| \`DISTINCT\` | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| \`ORDER BY\` | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| \`LIMIT / OFFSET\`| ❌ No (solo literales/parámetros) | ❌ No | ❌ No | ❌ No |

---

## 🧠 Framework Mental: "Cómo Pensar como un Analista de Datos"

Ante cualquier requerimiento de entrevista, aplica sistemáticamente esta secuencia de 6 pasos:
1. **Pregunta de Negocio & KPI Objetivo:** ¿Cuál es el objetivo analítico y qué decisión de negocio respalda?
2. **Entidad Central & Granularidad:** ¿Cuál es la tabla base y cuál es el grano de salida (1 fila por cliente, por pedido, por mes)?
3. **Cruce de Fuentes (JOINs):** ¿Qué relaciones aportan atributos descriptivos o métricas adicionales?
4. **Filtro Temprano (\`WHERE\`):** ¿Qué registros deben descartarse antes de consumir memoria y procesamiento?
5. **Agregación o Ventana (\`GROUP BY\` vs \`OVER\`):** ¿Se requiere colapsar filas en grupos o conservar el detalle calculando métricas contextuales?
6. **Entrega Ejecutiva (\`ORDER BY\` + \`LIMIT\`):** ¿Cómo debe estructurarse la salida final para máxima claridad de negocio?

---
`);

fs.writeFileSync(path.join(__dirname, 'part1.md'), doc.join('\n'), 'utf8');
console.log('Part 1 ready.');
