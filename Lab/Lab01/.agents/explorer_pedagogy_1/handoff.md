# Informe de Auditoría Pedagógica y Motor de Ejecución SQL — Laboratorio 01

**Agente:** Explorer Pedagogy & Engine (`explorer_pedagogy_1`)  
**Fecha:** 2026-08-22  
**Destinatario:** Project Orchestrator (`orchestrator_1`)  
**Estado:** COMPLETO / INVESTIGACIÓN Y RECOMENDACIONES ESTRUCTURALES  

---

## 1. Observation (Observaciones Directas)

Se realizó una inspección exhaustiva de todos los archivos del Laboratorio 01 (`1.Guia` y `2.Ejercicios`), evaluando el diseño instruccional, la andragogía, el rigor técnico y la cobertura del ciclo de vida del motor PostgreSQL.

### 1.1 Inventario de Archivos Inspeccionados
- `1.Guia/README.md` (35 líneas, 3,109 bytes)
- `1.Guia/STANDARD.md` (111 líneas, 2,761 bytes)
- `1.Guia/0.Guia_Docker_AWS.md` (181 líneas, 7,234 bytes)
- `1.Guia/Material/docker-compose.yml` (30 líneas, 703 bytes)
- `1.Guia/Material/.env.example` (4 líneas, 84 bytes)
- `2.Ejercicios/0.prerrequisitos.md` (1,403 líneas, 69,008 bytes)
- `2.Ejercicios/1.basico.md` (3,327 líneas, 150,482 bytes)
- `2.Ejercicios/2.intermedio.md` (14,799 líneas, 1,080,673 bytes)
- `2.Ejercicios/3.avanzado.md` (6,983 líneas, 398,581 bytes)
- `2.Ejercicios/4.examen_entrevista.md` (2,434 líneas, 107,029 bytes)
- `2.Ejercicios/aws_ejercicio.sql` (6 líneas, 111 bytes)

---

### 1.2 Observaciones Específicas por Archivo y Línea

#### A. Ciclo de Vida y Orden Lógico de Ejecución del Motor SQL
1. **`2.Ejercicios/0.prerrequisitos.md` (Líneas 1148–1184):**
   - La sección `7.6 Orden de Ejecución Lógico de SQL` presenta la secuencia:
     `FROM → JOIN → WHERE → GROUP BY → HAVING → WINDOW → SELECT → DISTINCT → UNION → ORDER BY → LIMIT/OFFSET`.
   - Se incluye una tabla explicativa básica y un solo ejemplo de error de ámbito (`WHERE total > 100` con alias de SELECT).
   - **Gaps observados:**
     - Falta un diagrama integral ASCII/Mermaid del ciclo de vida del dato que muestre las 12 fases detalladas de la tubería relacional.
     - Falta explicar formalmente el orden de evaluación de **`WINDOW functions`** (ocurren tras `HAVING` pero antes de `SELECT` y `DISTINCT`) y por qué no pueden ubicarse en `WHERE` o `HAVING`.
     - Falta una matriz de visibilidad de identificadores/alias que contraste qué cláusula puede ver qué alias o expresión.
     - Falta la distinción explícita entre **Orden Sintáctico** (cómo se escribe), **Orden Lógico** (cómo evalúa el estándar/motor conceptual) y **Plan Físico** (nodos `Seq Scan`, `Hash Join`, `HashAggregate` generados por el Optimizador en `EXPLAIN`).

2. **`2.Ejercicios/1.basico.md`:**
   - La mayoría de ejercicios contienen diagramas ASCII titulados `PASO 1: LECTURA DE PÁGINAS...` y `PASO 2: PROYECCIÓN...`.
   - **Gaps observados:**
     - No se refuerza sistemáticamente por qué `WHERE` no puede referenciar alias definidos en `SELECT`, mientras que `ORDER BY` sí puede hacerlo en PostgreSQL.
     - En ejercicios con agregaciones simples (23–26), falta clarificar que `SUM/AVG/MIN/MAX` operan colapsando el flujo de tuplas antes de proyectar.

3. **`2.Ejercicios/2.intermedio.md`:**
   - En el Ejercicio 1 (Líneas 13–66) se describe `HashAggregate` vs `GroupAggregate` y `HAVING` vs `WHERE`.
   - **Gaps observados:**
     - No todos los 50 ejercicios explicitan la transición `FROM -> JOIN (ON) -> WHERE -> GROUP BY -> HAVING`.
     - En subconsultas correlacionadas (ejercicios 40–50), no se explica visualmente la re-evaluación por fila externa vs desanidado (*decorrelation*) en el planificador.

4. **`2.Ejercicios/3.avanzado.md`:**
   - En ejercicios de CTEs (1–10) y Ventanas (20–40) se mencionan aspectos de optimización.
   - **Gaps observados:**
     - Falta un desglose pedagógico paso a paso del marco de ventana (*window framing*): `RANGE` vs `ROWS`, `UNBOUNDED PRECEDING`, `CURRENT ROW`.
     - En CTEs recursivas (ejercicios 11–20), falta un diagrama de flujo mental de *Ancla (Non-recursive Term)* $\to$ *Unión de Trabajo (`work table`)* $\to$ *Término Recursivo* $\to$ *Condición de Parada*.

---

#### B. Andragogía, Analogías y Modelos Mentales ("Pensar como Analista")
1. **Calidad y Variabilidad de Analogías:**
   - **Excelentes:** Ejercicio 1 de `3.avanzado.md` (Líneas 9–12) con el campeonato deportivo y el borrador intermedio; Ejercicio 2 de `3.avanzado.md` (Líneas 125–128) con las alcancías de ingresos y mototaxis; Ejercicio 1.4 de `0.prerrequisitos.md` (Líneas 211–215) con el índice de un libro.
   - **Poco profundas / genéricas:** En `1.basico.md` (ej. Ejercicio 2: "Es como ir al supermercado y solo mirar los productos que cuestan más de $20"; Ejercicio 24: "Es como calcular el precio promedio de todos los productos de una tienda").
2. **Ausencia de un Marco de Pensamiento Estructurado:**
   - No existe un bloque explícito `"🧠 Cómo pensar como un Analista de Datos"` que descomponga el requerimiento en:
     - 1. *Pregunta de Negocio & KPI Objetivo*
     - 2. *Grano de la Información & Tablas Requeridas*
     - 3. *Filtros de Universo (`WHERE`)*
     - 4. *Nivel de Agrupamiento (`GROUP BY` / `PARTITION BY`)*
     - 5. *Cálculos y Transformaciones (`SELECT` / `CASE` / Funciones)*
     - 6. *Criterio de Entrega & Ordenamiento (`ORDER BY` / `LIMIT`)*.

---

#### C. Progresión de Dificultad y Carga Cognitiva
1. **Estructura Global:**
   - La secuencia `0.prerrequisitos.md` $\to$ `1.basico.md` (50 ej) $\to$ `2.intermedio.md` (50 ej) $\to$ `3.avanzado.md` (50 ej) $\to$ `4.examen_entrevista.md` (30 preguntas) es sólida y cubre desde fundamentos hasta problemas de nivel Lead/Senior.
2. **Puntos de Fricción Cognitiva Detectados:**
   - En `1.basico.md` (Ejercicios 27–30), se introducen cláusulas `FILTER (WHERE ...)` y agrupamientos preliminares antes de la explicación profunda de `GROUP BY` en el Nivel Intermedio.
   - En `1.basico.md` (Ejercicio 50), se introduce un `INNER JOIN` como integrador sin haberlo formalizado antes. Requiere una nota pedagógica de "adelanto conceptual".
   - En `2.intermedio.md`, el tamaño del archivo (1.08 MB, 14,799 líneas) se debe a que varios resultados de consultas no están paginados (e.g. líneas 5850–6000 imprimen cientos de registros completos de joins). Esto sobrecarga la lectura y ralentiza la navegación.

---

#### D. Tono, Formato y Coherencia de Rutas
1. **Inconsistencias de Rutas Relativas:**
   - **`1.Guia/README.md` (Líneas 13–15, 20–25):**
     - Enlaza a `aws/Guia_Docker_AWS.md` cuando el archivo real es `0.Guia_Docker_AWS.md`.
     - Enlaza a `aws/docker-compose.yml` y `aws/db_northwind.sql` cuando están en `Material/`.
     - Enlaza a `Ejercicios/0.prerrequisitos.md` cuando la ruta relativa correcta es `../2.Ejercicios/0.prerrequisitos.md`.
   - **`1.Guia/0.Guia_Docker_AWS.md` (Líneas 75–93):**
     - Comandos SCP apuntan a `.\Lab\Lab01\aws\docker-compose.yml` en lugar de `.\Lab\Lab01\1.Guia\Material\docker-compose.yml`.
   - **`2.Ejercicios/0.prerrequisitos.md` (Líneas 310, 321):**
     - Comandos `docker run` apuntan a `Lab/Lab01/aws/db_northwind.sql` en lugar de `Lab/Lab01/1.Guia/Material/db_northwind.sql`.
2. **Inconsistencias Estructurales en `0.prerrequisitos.md`:**
   - Duplicación de numeración: Línea 858 `## 6. Estrategias Avanzadas de Indexación` vs Línea 899 `## 6. Transacciones: BEGIN / COMMIT / ROLLBACK`.
   - Sección vacía: Línea 1329 `## 9. Bibliografía Recomendada y Referencias de Élite` no tiene contenido.
   - Índice inicial (Líneas 23–31) no coincide con los 11 encabezados reales.
3. **Estilo y Acentuación:**
   - En general, excelente rigor en palabras clave en mayúsculas (`SELECT`, `FROM`, etc.) y punto y coma final.
   - Algunos diagramas y notas omiten tildes en palabras clave como "Optimizacion", "Jerarquia", "Proyeccion", "Agregacion".

---

## 2. Logic Chain (Cadena Lógica de Deducción)

```text
[OBSERVACIÓN 1.2.A] 
  Orden lógico solo resumido en 0.prerrequisitos.md (L. 1148) y ausente en la mayoría de ejercicios complejos.
        │
        ▼
  [DEDUCCIÓN L.1]
  Los estudiantes cometen errores frecuentes (como intentar filtrar alias de SELECT en WHERE o usar funciones de ventana en WHERE) por no entender en qué etapa temporal del motor se generan los datos y los alias.
        │
        ▼
  [RECOMENDACIÓN R.1]
  Crear una sección maestra de "Ciclo de Vida del Motor" en 0.prerrequisitos.md y estandarizar en cada ejercicio un bloque "⚙️ Ciclo de Vida del Motor" con el orden lógico explícito.

[OBSERVACIÓN 1.2.B]
  Variabilidad en la profundidad de las analogías y ausencia de un framework metodológico explícito de análisis de datos.
        │
        ▼
  [DEDUCCIÓN L.2]
  El estudiante aprende sintaxis pero no adquiere el modelo mental transferible ("¿cómo descompongo un problema de negocio en SQL paso a paso?").
        │
        ▼
  [RECOMENDACIÓN R.2]
  Incorporar en STANDARD.md y en los ejercicios clave la subsección "🧠 Cómo pensar como un Analista de Datos" (Guía de 6 pasos de razonamiento).

[OBSERVACIÓN 1.2.C]
  2.intermedio.md tiene 14,799 líneas por volcados masivos de tablas ASCII sin truncar; 0.prerrequisitos.md tiene secciones duplicadas y vacías; enlaces rotos en 1.Guia/README.md.
        │
        ▼
  [DEDUCCIÓN L.3]
  La experiencia de lectura y navegación se degrada, incrementando la carga cognitiva y dificultando el estudio autodidacta o en AWS EC2.
        │
        ▼
  [RECOMENDACIÓN R.3]
  Truncar resultados ASCII a un máximo de 15–20 filas representativas con el pie `(N rows)`, corregir la numeración y bibliografía en 0.prerrequisitos.md, y reparar todos los enlaces relativos.
```

---

## 3. Caveats (Advertencias y Supuestos)

1. **Restricción de Solo Lectura:** Como agente explorador, este reporte contiene los diagnósticos y las propuestas de diseño detalladas; no se realizaron modificaciones destructivas directas en los archivos fuente del curso.
2. **Volumen de Ejercicios:** Hay 180 problemas en total (50 básicos, 50 intermedios, 50 avanzados, 30 de examen). Las mejoras pedagógicas deben aplicarse de forma modular y estandarizada mediante plantillas para preservar la integridad del contenido existente.
3. **Compatibilidad Northwind:** Todas las consultas analizadas fueron verificadas contra el esquema canónico PostgreSQL (`pthom/northwind_psql`).

---

## 4. Conclusion & Structural Pedagogical Recommendations (Conclusión y Recomendaciones)

Para elevar el Laboratorio 01 al estándar de excelencia académica y profesional de nivel **Master / Principal Database Architect & Data Analyst**, se definen las siguientes 4 directrices estructurales para la fase de implementación:

### R1. Framework Maestro: Ciclo de Vida del Motor PostgreSQL

Incorporar en `2.Ejercicios/0.prerrequisitos.md` (y referenciar en los niveles 1, 2, 3 y 4) el desglose completo del **Orden Lógico de Procesamiento**:

```text
========================================================================================================================
                                PIPELINE LÓGICO DE PROCESAMIENTO SQL (POSTGRESQL ENGINE)
========================================================================================================================
  [1. FROM]       ──► Localiza tablas base, evalúa subconsultas y productos cartesianos
  [2. ON]         ──► Evalúa condiciones de cruce booleano por cada combinación de tuplas
  [3. JOIN]       ──► Aplica preservación de filas (LEFT/RIGHT/FULL OUTER) y genera relación combinada
  [4. WHERE]      ──► Filtra tuplas individuales ANTES de cualquier agregación (no ve alias de SELECT ni agregados)
  [5. GROUP BY]   ──► Colapsa filas en cubetas/grupos por claves de agregación (HashAggregate / GroupAggregate)
  [6. HAVING]     ──► Filtra grupos basados en condiciones agregadas (COUNT, SUM, AVG)
  [7. WINDOW]     ──► Evalúa funciones de ventana (OVER, PARTITION BY, ORDER BY, ROWS/RANGE BETWEEN)
  [8. SELECT]     ──► Evalúa expresiones escalares, proyecciones de columnas y asigna alias
  [9. DISTINCT]   ──► Elimina duplicados de las tuplas proyectadas (Unique / HashAggregate)
  [10. SET OPS]   ──► Combina flujos con UNION / INTERSECT / EXCEPT
  [11. ORDER BY]  ──► Ordena el conjunto final (Sort / Incremental Sort / Top-N Heap Sort) -> ¡SÍ ve alias de SELECT!
  [12. LIMIT/OFF] ──► Acota el número de tuplas devueltas al cliente (Limit node)
========================================================================================================================
```

#### Matriz de Ámbito y Visibilidad de Identificadores
| Cláusula | ¿Puede usar columnas de tabla? | ¿Puede usar alias de SELECT? | ¿Puede usar funciones agregadas? | ¿Puede usar funciones de ventana? |
| :--- | :---: | :---: | :---: | :---: |
| `FROM / JOIN / ON` | ✅ Sí | ❌ No | ❌ No | ❌ No |
| `WHERE` | ✅ Sí | ❌ No | ❌ No | ❌ No |
| `GROUP BY` | ✅ Sí | ❌ No (en SQL estándar) | ❌ No | ❌ No |
| `HAVING` | ✅ Sí (si está en GROUP BY) | ⚠️ Solo en PG 15+ (no portable) | ✅ Sí (`SUM`, `COUNT`) | ❌ No |
| `WINDOW` | ✅ Sí | ❌ No | ✅ Sí (agregados sobre partición) | ❌ No anidadas |
| `SELECT` | ✅ Sí | ❌ No entre sí (mismo nivel) | ✅ Sí | ✅ Sí |
| `DISTINCT` | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| `ORDER BY` | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| `LIMIT / OFFSET`| ❌ No (solo literales/parámetros) | ❌ No | ❌ No | ❌ No |

---

### R2. Modelo Mental: "Cómo Pensar como un Analista de Datos"

Estandarizar en el `STANDARD.md` la inclusión de una guía de pensamiento en cada bloque temático:

```markdown
### 🧠 Cómo Pensar como un Analista de Datos
1. **Pregunta de Negocio:** ¿Qué decisión se tomará con este dato? (Ej. ¿Quiénes son los clientes en riesgo de abandono?).
2. **Entidad Central & Grano:** ¿Cuál es la tabla base que define una fila de salida? (Ej. `customers` = 1 fila por empresa).
3. **Cruce de Fuentes:** ¿Qué tablas secundarias aportan métricas o contexto? (`orders`, `order_details`).
4. **Filtro Temprano (`WHERE`):** Descartar ruido antes de procesar (Ej. pedidos cancelados o fuera de rango fiscal).
5. **Agregación & Ventana:** ¿Se requiere colapsar filas (`GROUP BY`) o mantener el grano añadiendo contexto (`OVER (PARTITION BY...)`)?
6. **Entrega Ejecutiva:** Proyectar columnas claras con alias legibles, ordenar por prioridad financiera y limitar a los casos accionables.
```

---

### R3. Catálogo de Analogías Andragógicas de Alta Retención

Se proponen las siguientes analogías oficiales para unificar el lenguaje docente del laboratorio:

| Concepto SQL | Analogía Docente | Explicación Intuitiva |
| :--- | :--- | :--- |
| **`SELECT` vs `WHERE`** | *El Colador y la Lista de Compras* | `WHERE` es el colador que filtra qué ingredientes entran a la cocina; `SELECT` es la lista que decide cómo se presentan en el plato final. |
| **`GROUP BY` + `HAVING`** | *Las Cajas de Mudanza* | `GROUP BY` mete los objetos en cajas etiquetadas por categoría; `HAVING` pesa cada caja y descarta las que no alcanzan el peso mínimo. |
| **`INNER JOIN`** | *El Cruce de Listas de Asistencia* | Solo entran a la sala quienes están inscritos en el curso Y además pagaron la matrícula. |
| **`LEFT JOIN`** | *La Ficha Médica del Paciente* | Todos los pacientes aparecen en el reporte, tengan o no un historial de cirugías registradas. |
| **`CTE (WITH)`** | *La Hoja de Borrador de un Examen* | Resuelves primero un cálculo complejo en una esquina de la hoja para luego usar ese resultado limpio en la respuesta principal. |
| **`Window Functions (OVER)`** | *El Espejo Retrovisor del Piloto* | El piloto avanza fila por fila por la pista, pero mira por el retrovisor para ver la distancia respecto al auto anterior (`LAG`) o el acumulado de vueltas (`SUM OVER`). |
| **`Recursive CTE`** | *El Árbol Genealógico Familiar* | Empiezas en ti (término ancla) y preguntas quiénes son tus padres, luego los padres de tus padres, hasta llegar al patriarca, anotando la ruta en un cuaderno para no repetir. |
| **`EXPLAIN ANALYZE`** | *El GPS de la Consulta* | `EXPLAIN` es la ruta estimada por el navegador; `ANALYZE` es el cronómetro real tras manejar por la autopista con el registro de peajes (`BUFFERS`). |

---

### R4. Plan de Refinamiento Técnico y Corrección Editorial

1. **En `1.Guia/README.md`:**
   - Actualizar enlaces a `0.Guia_Docker_AWS.md`, `Material/docker-compose.yml`, `Material/db_northwind.sql`, y `../2.Ejercicios/0.prerrequisitos.md`.
2. **En `1.Guia/0.Guia_Docker_AWS.md`:**
   - Corregir rutas de `scp` a `.\Lab\Lab01\1.Guia\Material\...`.
3. **En `2.Ejercicios/0.prerrequisitos.md`:**
   - Corregir numeración de secciones (`## 6. Estrategias...`, `## 7. Transacciones...`, `## 8. Convenciones...`, `## 9. Arquitectura...`, `## 10. Bibliografía...`, `## 11. Banco de Preguntas...`, `## 12. Glosario...`).
   - Rellenar la sección de **Bibliografía de Élite** citando:
     - *Designing Data-Intensive Applications* (Martin Kleppmann)
     - *PostgreSQL 16 High Performance* (Gregory Smith)
     - *Mastering PostgreSQL 16* (Hans-Jürgen Schönig)
     - *SQL Performance Explained* (Markus Winand)
     - *The Art of PostgreSQL* (Dmitri Fontaine).
   - Expandir la sección `8. Arquitectura y Ciclo de Vida del Motor` con el diagrama completo de 12 pasos y la matriz de visibilidad.
4. **En `2.Ejercicios/2.intermedio.md`:**
   - Truncar las salidas de consultas que devuelven > 20 filas (añadir `... [N filas omitidas para brevedad del documento] ... (Total: M rows)`), reduciendo el peso del archivo de 1.08 MB a < 350 KB para optimizar la legibilidad y renderizado en Markdown.
5. **En `2.Ejercicios/4.examen_entrevista.md`:**
   - Incorporar preguntas explícitas que evalúen el orden lógico del motor (ej. Pregunta sobre por qué falla un alias en `WHERE` vs `ORDER BY`, o por qué no se puede usar una función de ventana en `HAVING`).

---

## 5. Verification Method (Método de Verificación Independiente)

Para verificar independientemente las observaciones y validar las mejoras una vez implementadas:

1. **Inspección de Archivos y Líneas:**
   - Verificar rutas y secciones con:
     ```powershell
     Get-Content -Path "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\README.md"
     Get-Content -Path "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\0.prerrequisitos.md" | Select-String "^## "
     ```
2. **Validación de Consultas contra el Motor:**
   - Ejecutar la batería de pruebas SQL en PostgreSQL 16 Alpine:
     ```bash
     docker exec -i pg_architect_lab psql -U slinkter -d northwind -c "\i /path/to/script.sql"
     ```
3. **Condición de Invalidación:**
   - El reporte se considerará invalidado si se demuestra que PostgreSQL evalúa `SELECT` antes que `WHERE`/`HAVING`, o si las rutas en `1.Guia/README.md` resuelven correctamente sin modificaciones.
