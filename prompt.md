# ApuntesSQL

## /_ Febrero del 2018 02 12_/

https://github.com/Slinkter/Frontend/tree/ec1c00c2225b21c8ba58d97a46f4c8fd632be13e/R06.SQL

mysql -h 127.0.0.1 -P 3306 -u root -p'372421luis' --ssl-mode=DISABLED

# Prompt: Auditor de Calidad y Mentor - Estándares PostgreSQL

## 1. Contexto y rol

Nombre: ArquiDB — Principal Data Architect & Senior DBA (Distinguished Engineer)

Especialización: PostgreSQL Enterprise (v15+), Cloud Architecture, Data Engineering. +25 años en infraestructuras críticas (ex-IBM/Oracle).

Tono y estilo: profesional, técnico, directo y mentorizador. Usar analogías de ingeniería real. No omitir seguridad ni escalabilidad.

---

## 2. Objetivos principales

1. Mentoría avanzada: guiar la transformación del autor en un especialista de bases de datos, con foco en los internals, teoría relacional y arquitectura de datos moderna.
2. Auditoría y refactorización: revisar materiales antiguos (HTML, PDFs, ejercicios) para extraer la lógica atemporal y actualizar ejemplos a prácticas de 2026 y PostgreSQL idiomático.

Lecturas obligatorias de referencia: C.J. Date, Abraham Silberschatz, Martin Kleppmann.

---

## 3. Entregables por clase (formato requerido)

Cada "clase" o unidad debe entregarse en Markdown y contener:

- Resumen teórico (alto nivel).
- Código SQL ejecutable y limpio (Postgres v15+).
- Laboratorio resuelto: ejercicios con soluciones y variantes para práctica.
- Instrucciones de ejecución (psql / Docker / docker-compose) y comandos para ejecutar una sola consulta o script.
- Observabilidad: al menos un `EXPLAIN (ANALYZE, BUFFERS)` para consultas clave, con interpretación breve.
- Notas de compatibilidad (si algo es específico de Postgres frente a SQL ANSI).

---

## 4. Criterios de auditoría y competencias evaluadas

Dominio técnico (no exhaustivo):

- Tipos nativos: `SERIAL`, `BIGSERIAL`, `UUID`, `JSONB`, `ARRAY`, `HSTORE`.
- Ventanas y funciones analíticas (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`).
- CTEs recursivas (`WITH RECURSIVE`).
- Particionamiento, VACUUM/autovacuum, y mantenimiento.
- Replicación lógica/física y conceptos de HA.
- Extensiones relevantes: `pg_trgm`, `tablefunc`, `uuid-ossp`, `postgis`.
- Row Level Security (RLS) y buenas prácticas de seguridad.

Estándares y estilo:

- Preferir constructos Postgres idiomáticos (`RETURNING`, `ON CONFLICT`, operadores JSONB).
- Evitar sintaxis propietaria de otros motores (Oracle, SQL Server) salvo que se documente la conversión.

Buenas prácticas de diseño:

- Normalización hasta 3FN/BCNF cuando aplique; documentar decisiones de denormalización.
- Selección correcta de tipos de datos e impacto en I/O.
- Indexación estratégica (B-tree, GIN, GiST, BRIN) y cuándo usar cada una.
- Constraints semánticos y validaciones (CHECK, FK, UNIQUE).

PL/pgSQL:

- Distinción entre funciones y procedimientos, manejo de excepciones y triggers (función + trigger pattern).
- Preferir marcar funciones como `IMMUTABLE/STABLE/VOLATILE` según corresponda.

---

## 5. Formato del informe de auditoría (plantilla)

Para cada archivo analizado producir un bloque breve:

📄 archivo: `ruta/archivo`
Estado: `✅ CORRECTO` / `⚠️ ADVERTENCIA` / `❌ INCORRECTO`

Cambios recomendados (priorizados):

1. [línea o sección] Breve descripción y código sugerido (si aplica).
2. [línea o sección] Otro cambio.

Ejemplo de sugerencia (Postgres):

```sql
CREATE TABLE example (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);
```

Cuando se muestre código erróneo legado (p. ej. Oracle), incluir la corrección Postgres equivalente.

---

## 6. Inicio operativo (primeros pasos que debe ejecutar el asistente)

1. Presentarse como ArquiDB adoptando el tono pedido.
2. Proponer un índice detallado para la Fase 1 (Fundamentos y teoría).
3. Solicitar o esperar los archivos a auditar.

---

## 7. Observaciones prácticas adicionales (puntuales)

- Incluir comandos reproducibles para ejecutar ejemplos (psql o docker). Ejemplos:
    - `psql -h localhost -U slinkter -d northwind -f ejercicios.sql`
    - `docker run --rm --name pg -e POSTGRES_USER=slinkter -e POSTGRES_PASSWORD=slinkter -e POSTGRES_DB=northwind -v "$PWD/db_northwind.sql":/docker-entrypoint-initdb.d/db_northwind.sql -d postgres:16-alpine`

- EXPLAIN ANALYZE: usarlo para SELECT; para DML destructivo envolver en `BEGIN; EXPLAIN ANALYZE <DML>; ROLLBACK;`.
- CSS/UI: el `index.html` usa la paleta correcta; las páginas `semana01.html`...`semana16.html` necesitan revisión de estilos. Proponer consolidar estilos en `master.css` y aplicar metodología BEM.

---

## 8. Versiones y compatibilidad

Objetivo: compatibilidad con PostgreSQL v15+. Documentar cualquier feature dependiente de v16+.

---

Mantener este prompt conciso. Al generar auditorías, priorizar claridad: una recomendación accionable por ítem y un fragmento de código que funcione en Postgres v15+.

# Plan de Trabajo — ApuntesSQL Refactorización

## Fases del proyecto

### [x] Fase 1: Limpieza de archivos TXT

- [x] Corregir encoding latin1 → UTF-8 en `Silabus.txt`
- [x] Limpiar caracteres de control y viñetas en todos los `Clase_*.txt`
- [x] Extirpar arte ASCII corrupto en `Clase_10.txt` (líneas 56–534) — 479 líneas eliminadas
- [x] Marcar `Restrictions on Parallel DML.txt` (vacío) — nota agregada
- [x] Normalizar whitespace en todos los TXT
- [x] Corregir `Taller_HA_MSSQL2012.txt` (texto stretch, viñetas (cid:1))
- [x] Corregir `Practica_03_Sol.txt` (numeración de preguntas)

### [x] Fase 2: Mapeo semanal según sílabo

| Sem | Tema                                         | Fuente TXT                                                       | HTML                                                      |
| --- | -------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| 01  | Fundamentos de Administración de Información | `Clase_00.txt`                                                   | `semana_01.html` (247 líneas)                             |
| 02  | Sistema de Gestión de BD                     | `Clase_01.txt` + `Clase_02.txt`                                  | `semana_02.html` (309 líneas)                             |
| 03  | Bases de Datos Relacionales                  | `Clase_03.txt` (conceptos)                                       | `semana_03.html` (263 líneas)                             |
| 04  | DDL y Administración de BD                   | `Clase_03.txt` (DDL)                                             | `semana_04.html` (286 líneas)                             |
| 05  | DML y Consultas Simples                      | `Clase_04.txt`                                                   | `semana_05.html` (206 líneas)                             |
| 06  | Modelamiento de Datos (ERD)                  | `Clase_05.txt`                                                   | `semana_06.html`                                          |
| 07  | Normalización (1FN, 2FN, 3FN)                | `Clase_06.txt` + `NormalizacioBD.txt`                            | `semana_07.html`                                          |
| 08  | **Examen Parcial**                           | Resumen 1-7 + mock exam                                          | `semana_08.html` (507 líneas, 4 secciones + solucionario) |
| 09  | BCNF, 4FN, 5FN, Desnormalización             | `Clase_09.txt`                                                   | `semana_09.html` (342 líneas)                             |
| 10  | JOINs y Subconsultas                         | `Clase_10.txt` (JOINs)                                           | `semana_10.html` (256 líneas)                             |
| 11  | GROUP BY, HAVING, Funciones de Grupo         | `Clase_10.txt` (agrupamiento)                                    | `semana_11.html` (205 líneas)                             |
| 12  | PL/SQL: Bloques, Variables, Cursores         | `Clase_11.txt` (intro)                                           | `semana_12.html` (317 líneas)                             |
| 13  | Procedimientos, Funciones, Triggers          | `Clase_11.txt` (avanzado)                                        | `semana_13.html` (326 líneas)                             |
| 14  | Data Warehouse                               | `Clase_12.txt` + `Clase_15.txt` + `Script_Ejemplo_Warehouse.txt` | `semana_14.html` (378 líneas)                             |
| 15  | Tópicos Avanzados (HA)                       | `Taller_HA_MSSQL2012.txt`                                        | `semana_15.html` (323 líneas)                             |
| 16  | **Examen Final**                             | Resumen 9-15 + mock exam                                         | `semana_16.html` (340 líneas, 4 secciones + solucionario) |

### [x] Fase 3a: Construcción de HTMLs

- [x] Semanas 01–07: rehacer HTMLs con plantilla Cornell + BEM
- [x] Semanas 10, 11, 12, 14, 15: crear HTMLs nuevos
- [x] Semanas 09, 13, 16: mejorar HTMLs existentes

### [x] Fase 3b: Exámenes tipo

- [x] `semana_08.html`: mock exam parcial (teoría + ER + normalización + SQL + solucionario)
- [x] `semana_16.html`: mock exam final (PL/SQL + consultas complejas + DW + solucionario)

### [x] Fase 4: Consolidación final

- [x] `index.html` rehecho con orden exacto del sílabo (16 tarjetas + exámenes)
- [x] `master.css` — sin cambios (ya soporta todas las clases BEM necesarias)
- [x] Navegación consistente entre todas las semanas
- [x] Enlaces rotos corregidos — todos los 16 HTMLs existen y se referencian correctamente

---

## Resultado de la Revisión ArquiDB

- [x] No hay errores de encoding (`�`) en ningún HTML
- [x] Las 16 semanas cubren el sílabo estrictamente
- [x] Todos los HTMLs usan BEM classes de `master.css` (sin clases legacy en semana\_\*.html)
- [x] `extra_*.html` mantienen su estructura legacy (contenido complementario no modificado)
- [x] Exámenes tipo con 4 secciones + solucionario completo

---

## Agentes

| Agente             | Rol                                         |
| ------------------ | ------------------------------------------- |
| **ArquiDB**        | Data Architect — revisa y aprueba cada fase |
| **TXT Cleaner**    | Limpia encoding, artefactos, whitespace     |
| **Content Mapper** | Mapea contenido TXT a estructura semanal    |
| **HTML Builder**   | Genera HTMLs con plantilla y UI/UX          |
| **Exam Builder**   | Crea exámenes tipo con solucionarios        |

# INFORME DE REFACTORIZACION — ApuntesSQL

## Proyecto

Repositorio de apuntes de Ingenieria de Datos (ULima 2013-2). Contiene apuntes de clase en PDF convertidos a TXT, y una carpeta `ULima/Apuntes/` con HTMLs educativos.

## Objetivo

1. Verificar integridad PDF a TXT
2. Reorganizar contenido siguiendo el silabo estrictamente
3. Crear/mejorar 16 HTMLs educativos con diseno Cornell + BEM
4. Generar examenes tipo con solucionarios (semana 08 y 16)
5. Rol: Data Architect (ArquiDB) revisando calidad

---

## Fase 1: Limpieza de TXT

| Archivo                                        | Problema                                                 | Accion                             |
| ---------------------------------------------- | -------------------------------------------------------- | ---------------------------------- |
| `ULima/Silabus.txt`                            | Encoding latin1 -> `�`                                   | Recodificado a UTF-8               |
| `ULima/Clases/Clase_10.txt`                    | ~479 lineas de arte ASCII corrupto (EMPXDEPT cross join) | Extirpadas lineas 56-534           |
| `ULima/Clases/Clase_*.txt` (11 archivos)       | Vinietas `▪` `` `❑` `` `➢`                             | Reemplazadas por `-` `→` `*`       |
| `ULima/otros/Taller_HA_MSSQL2012.txt`          | Texto stretch: "IIIInnnngggg...."                        | Normalizado a texto legible        |
| `ULima/otros/Restrictions on Parallel DML.txt` | Archivo vacio (0 bytes)                                  | Nota: "Pendiente de transcripcion" |
| `ULima/otros/Practica_03_Sol.txt`              | Numeracion de preguntas erronea                          | Corregido a secuencial 1-10        |

## Fase 2: Mapeo semanal

| Sem | Tema                             | Fuente TXT                                                       | HTML             | Lineas  |
| --- | -------------------------------- | ---------------------------------------------------------------- | ---------------- | ------- |
| 01  | Fundamentos de Informacion       | `Clase_00.txt`                                                   | `semana_01.html` | 247     |
| 02  | Sistema de Gestion de BD         | `Clase_01.txt` + `Clase_02.txt`                                  | `semana_02.html` | 309     |
| 03  | Bases de Datos Relacionales      | `Clase_03.txt` (conceptos)                                       | `semana_03.html` | 263     |
| 04  | DDL y Administracion             | `Clase_03.txt` (DDL)                                             | `semana_04.html` | 286     |
| 05  | DML y Consultas Simples          | `Clase_04.txt`                                                   | `semana_05.html` | 206     |
| 06  | Modelamiento E-R                 | `Clase_05.txt`                                                   | `semana_06.html` | ~220    |
| 07  | Normalizacion 1FN-3FN            | `Clase_06.txt` + `NormalizacioBD.txt`                            | `semana_07.html` | ~280    |
| 08  | **Examen Parcial**               | Mock exam (4 secciones)                                          | `semana_08.html` | **507** |
| 09  | BCNF, 4FN, 5FN, Desnormalizacion | `Clase_09.txt`                                                   | `semana_09.html` | 342     |
| 10  | JOINs y Subconsultas             | `Clase_10.txt` (JOINs)                                           | `semana_10.html` | 256     |
| 11  | GROUP BY, HAVING, Agregacion     | `Clase_10.txt` (agrupamiento)                                    | `semana_11.html` | 205     |
| 12  | PL/SQL: Bloques y Cursores       | `Clase_11.txt` (intro)                                           | `semana_12.html` | 317     |
| 13  | Procedimientos y Triggers        | `Clase_11.txt` (avanzado)                                        | `semana_13.html` | 326     |
| 14  | Data Warehouse                   | `Clase_12.txt` + `Clase_15.txt` + `Script_Ejemplo_Warehouse.txt` | `semana_14.html` | 378     |
| 15  | Alta Disponibilidad              | `Taller_HA_MSSQL2012.txt`                                        | `semana_15.html` | 323     |
| 16  | **Examen Final**                 | Mock exam (4 secciones)                                          | `semana_16.html` | **340** |

HTMLs NUEVOS (no existian antes): semana_10, 11, 12, 14, 15.

## Fase 3: Especificaciones tecnicas de HTMLs

**Sistema de diseno:**

- CSS: `master.css` con diseno Cornell (sidebar 280px + main flex)
- Variables CSS: colores (navy, slate, PostgreSQL blue), sombras, bordes, transiciones
- Sistema BEM: `.header`, `.cornell`, `.sidebar`, `.sidebar__title`, `.sidebar__item`, `.main`, `.main__title`, `.main__text`, `.box--note/concept/example/exercise/warning`, `.table`, `.table__th/td/tr`, `.nav`, `.nav__link`, `.tag`, `.architect-insight`

**Restricciones aplicadas:**

- 0 emojis en HTML (usar texto: "Nota:", "Importante:", "Ejemplo:")
- 0 clases legacy (`header-box`, `cornell-container`, `keywords-sidebar`, `main-content`, `box-note`, `box-ejemplo`)
- 0 estilos inline (excepto minimo necesario en sidebar resources)
- Encoding UTF-8 sin errores
- Navegacion secuencial consistente entre semanas

## Fase 4: Examennes tipo

**semana_08.html** (507 lineas):

- Seccion 1: Teoria (10 preguntas, 30 pts) — V/F + opcion multiple
- Seccion 2: Modelamiento E-R (2 ejercicios, 20 pts)
- Seccion 3: Normalizacion (2 ejercicios, 20 pts)
- Seccion 4: SQL (5 consultas, 30 pts)
- Solucionario completo al final

**semana_16.html** (340 lineas):

- Seccion 1: Teoria Avanzada (10 preguntas, 30 pts) — BCNF, OLAP, HA
- Seccion 2: PL/SQL (3 ejercicios, 25 pts) — procedimiento + funcion + trigger
- Seccion 3: Consultas Complejas (5 ejercicios, 25 pts) — JOINs, subconsultas, GROUP BY
- Seccion 4: Data Warehouse (2 ejercicios, 20 pts) — Star Schema
- Solucionario completo al final

## Archivos NO modificados (intencionalmente)

- `extra_*.html` (8 archivos) — contenido complementario legacy
- `SQL/` — contenido moderno PostgreSQL
- `Credenciales/` — guia de despliegue AWS
- `GEMINI.md`, `prompt.md` — documentacion del proyecto

## Puntos de atencion para el revisor

1. **Semana 08 y 16** — Los examenes tienen solucionario incluido. Verificar que las respuestas sean correctas tecnicamente.
2. **`Restrictions on Parallel DML.txt`** — Estaba vacio. El PDF original puede tener contenido no transcrito.
3. **`extra_*.html`** — Usan clases CSS legacy que no estan en `master.css` (clases como `header-box`). Si se quiere integrar completamente, necesitan refactorizacion.
4. **Contenido Oracle vs PostgreSQL** — El material original usa sintaxis Oracle (`VARCHAR2`, `NUMBER`). Los HTMLs preservan esa sintaxis pero los `architect-insight` mencionan alternativas PostgreSQL.
5. **Mermaid diagrams** — No se agregaron diagramas Mermaid a los HTMLs (pendiente para iteracion futura).

## Estadisticas finales

| Metrica                            | Valor                                                     |
| ---------------------------------- | --------------------------------------------------------- |
| HTMLs creados/mejorados            | 16                                                        |
| HTMLs nuevos                       | 5                                                         |
| TXT limpiados                      | 15                                                        |
| Archivos con encoding corregido    | 1 (+11 con vinietas)                                      |
| Lineas removidas (datos corruptos) | ~479                                                      |
| Preguntas de examen generadas      | 37 (20 teoria + 9 ejercicios practicos + 8 consultas SQL) |
| Solucionarios                      | 2 completos                                               |
| Clases legacy eliminadas           | ~80+ instancias en semana\_\*.html                        |
| Emojis removidos                   | ~50+ instancias                                           |
