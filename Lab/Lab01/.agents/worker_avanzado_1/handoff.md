# Handoff Report — Refinamiento del Libro de Ejercicios SQL Nivel Avanzado (`3.avanzado.md`)

**Agente:** Worker Avanzado (`worker_avanzado_1`)  
**Fecha:** 2026-08-22  
**Destinatario:** Project Orchestrator (`orchestrator_1` / `parent`)  
**Archivo Modificado:** `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\3.avanzado.md`  
**Estado:** COMPLETADO / VERIFICADO 100% (50/50 Ejercicios Ejecutables y Auditados)

---

## 1. Observation

Se realizó una intervención exhaustiva sobre los 50 ejercicios avanzados contenidos en `2.Ejercicios/3.avanzado.md` (5,399 líneas resultantes, 289 kB), ejecutando cada consulta SQL sobre un contenedor de prueba PostgreSQL 16 Alpine con el esquema canónico de Northwind (`1.Guia/Material/db_northwind.sql`).

### Hallazgos y Cambios Específicos Realizados:

1. **Eliminación de Contaminación de Datos Mock:**
   - **Ejercicio 4 (Líneas 416–418):** Se eliminó la cadena `Alfreds Futterkiste - Actualizado` en la salida ASCII y se reemplazó por la salida canónica `Alfreds Futterkiste`.
   - **Ejercicio 10 (Líneas 1050–1095):** Se actualizaron las tuplas de prueba de carga incremental en la CTE `datos_nuevos` reemplazando los IDs y nombres ficticios `NWE01` y `NWE02` por `NEW01` y `NEW02`, y restaurando `Alfreds Futterkiste`. La tabla ASCII esperada ahora muestra fielmente los valores booleanos auténticos de `fue_insertado` (`t` para `NEW01` y `NEW02`, `f` para `ALFKI` actualizada) con el estado de retorno `INSERT 0 3`.
   - **Ejercicio 32 (Líneas 3536–3550):** Se eliminaron las referencias a `Alfreds Futterkiste - Actualizado`, restableciendo `Alfreds Futterkiste` con sus 5 órdenes históricas reales.

2. **Truncamiento Estandarizado de Conjuntos Masivos de Datos:**
   - En lugar de volcar cientos de filas continuas en el documento (que dificultaban la lectura en Ejercicios como el 4 con 263 filas, el 13 con 365 filas, el 21 con 192 filas, el 23 con 480 filas y el 32 con 415 filas), se implementó el formato estándar de truncamiento: cabecera de columnas + 10 primeras tuplas representativas + separador con elipsis alineada `...` + 2 a 3 tuplas finales + pie de resumen con conteo exacto de tuplas `(N rows)`.

3. **Notas de Dependencia en Consultas de Catálogo de Estadísticas:**
   - En los Ejercicios 8, 43, 44, 45 y 49 (consultas sobre `pg_stat_user_tables`, `pg_stat_all_tables` y `pg_stat_user_indexes`), se incorporaron notas técnicas explícitas que advierten al estudiante que los valores métricos (`seq_scan`, `idx_scan`, `n_dead_tup`, timestamps de autovacuum) reflejan el uso acumulado del motor en tiempo de ejecución.

4. **Incorporación del Marco Metodológico "🧠 Cómo Pensar como un Analista de Datos":**
   - El 100% de los 50 ejercicios ahora cuenta con la descomposición estructurada de 6 pasos:
     1. *Pregunta de Negocio & KPI Objetivo*
     2. *Fuentes de Datos & Granularidad*
     3. *Relaciones & JOINs*
     4. *Filtros & Agregaciones*
     5. *Proyección & Ordenamiento*
     6. *Validación & Sentido Común*.

5. **Profundización del Motor de Ejecución y Optimizador:**
   - **Marcos de Ventana (*Window Framing* - Ejercicios 21 a 30):** Explicación profunda de `ROWS BETWEEN` vs `RANGE BETWEEN`, desplazamiento físico en punteros de tuplas vs evaluación de grupos de valores (*peers*), `UNBOUNDED PRECEDING`, `CURRENT ROW`, `UNBOUNDED FOLLOWING` y el comportamiento por defecto de PostgreSQL cuando existe `ORDER BY`.
   - **Ciclo de Vida de Recursión (Ejercicios 11 a 20):** Desglose formal y diagramado de las 4 fases del motor: *1. Término Ancla $\to$ 2. Tabla de Trabajo (WT) $\to$ 3. Término Recursivo $\to$ 4. Condición de Parada y Acumulación en Result Table (RT)*.
   - **Nodos del Optimizador:** Explicación técnica de `HashAggregate` vs `GroupAggregate` en memoria `work_mem`, Poda de Particiones (*Partition Pruning* estática y dinámica en tiempo de ejecución) y Materialización de CTEs (`AS MATERIALIZED` vs `AS NOT MATERIALIZED` en PostgreSQL 12+).

6. **Integración y Resaltado de las 4 Grandes Analogías:**
   - **Hoja de borrador:** CTEs (`WITH`) como tablas de cálculo intermedias previas al informe final (Ejercicios 1–10).
   - **Árbol genealógico:** CTEs recursivas (`WITH RECURSIVE`) partiendo del abuelo/raíz y descendiendo generación por generación (Ejercicios 11–20).
   - **Espejo retrovisor:** Funciones de ventana (`LAG`/`LEAD`/`OVER`) mirando hacia atrás o adelante sin detener la marcha del vehículo ni colapsar las filas (Ejercicios 21–30).
   - **GPS en tiempo real:** `EXPLAIN ANALYZE` como el sistema de navegación con telemetría en vivo comparado contra mapas teóricos de costos estimados (Ejercicios 41–50).

---

## 2. Logic Chain

1. **Premisa 1:** Un libro de ejercicios de nivel avanzado debe combinar rigor técnico absoluto en PostgreSQL con una estructura pedagógica y andragógica que desarrolle criterio analítico de producción.
2. **Premisa 2:** La presencia de datos mock desactualizados (`NWE01`, `NWE02`, `Alfreds Futterkiste - Actualizado`) rompía la reproducibilidad exacta contra el script canónico `db_northwind.sql` (91 clientes).
3. **Premisa 3:** Los volcados de cientos de líneas en Markdown degradan la legibilidad y aumentan la sobrecarga cognitiva sin aportar valor pedagógico adicional respecto a un truncamiento estructurado representativo.
4. **Premisa 4:** Al integrar el marco analítico de 6 pasos en los 50 ejercicios, el estudiante aprende no solo la sintaxis declarativa, sino a desglosar requerimientos de negocio en granularidad, relaciones, filtros, proyecciones y validaciones.
5. **Conclusión:** La refactorización y auditoría directa de `3.avanzado.md` garantiza una consistencia del 100% entre el código SQL, la salida del motor y el estándar docente del proyecto.

---

## 3. Caveats

- **Extensión `tablefunc` para Crosstab:** Los Ejercicios 34 y 35 requieren la extensión `CREATE EXTENSION IF NOT EXISTS tablefunc;` habilitada en la base de datos `northwind` (lo cual es estándar en instalaciones de PostgreSQL y se encuentra documentado en los ejercicios).
- **Métricas de Catálogo en Ejercicios 8, 43, 44, 45, 49:** La salida ASCII de `pg_stat_user_tables` representa una captura verídica del motor en estado de prueba; los estudiantes verán variaciones en métricas numéricas dependiendo de cuántas consultas previas hayan ejecutado en su propia sesión.

---

## 4. Conclusion

- El archivo `2.Ejercicios/3.avanzado.md` ha sido completamente refinado, saneado y enriquecido.
- Cero ocurrencias de datos mock residuales (`NWE01`, `NWE02`, `- Actualizado`).
- 50 de 50 ejercicios cuentan con el marco analítico `"🧠 Cómo Pensar como un Analista de Datos"`, explicaciones profundizadas del optimizador y tablas ASCII exactas y legibles.
- El archivo está listo para la auditoría de control de calidad final.

---

## 5. Verification Method

Para reproducir y validar independientemente las modificaciones:

1. **Ejecutar la suite de validación automatizada sobre el contenedor PostgreSQL:**
   ```powershell
   node "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_avanzado_1\audit_and_enhance.js"
   ```
2. **Verificar la integridad estructural y ausencia de datos mock:**
   ```powershell
   node -e "
   const fs = require('fs');
   const c = fs.readFileSync('2.Ejercicios/3.avanzado.md', 'utf8');
   console.log('Mock matches:', (c.match(/NWE01|NWE02|Actualizado/g) || []).length);
   console.log('Exercises count:', (c.match(/## Ejercicio /g) || []).length);
   console.log('Analyst thinking count:', (c.match(/### 🧠 Cómo Pensar como un Analista/g) || []).length);
   "
   ```
   *Salida esperada:*
   `Mock matches: 0`  
   `Exercises count: 50`  
   `Analyst thinking count: 50`
