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
| Sem | Tema | Fuente TXT | HTML |
|-----|------|-----------|------|
| 01 | Fundamentos de Administración de Información | `Clase_00.txt` | `semana_01.html` (247 líneas) |
| 02 | Sistema de Gestión de BD | `Clase_01.txt` + `Clase_02.txt` | `semana_02.html` (309 líneas) |
| 03 | Bases de Datos Relacionales | `Clase_03.txt` (conceptos) | `semana_03.html` (263 líneas) |
| 04 | DDL y Administración de BD | `Clase_03.txt` (DDL) | `semana_04.html` (286 líneas) |
| 05 | DML y Consultas Simples | `Clase_04.txt` | `semana_05.html` (206 líneas) |
| 06 | Modelamiento de Datos (ERD) | `Clase_05.txt` | `semana_06.html` |
| 07 | Normalización (1FN, 2FN, 3FN) | `Clase_06.txt` + `NormalizacioBD.txt` | `semana_07.html` |
| 08 | **Examen Parcial** | Resumen 1-7 + mock exam | `semana_08.html` (507 líneas, 4 secciones + solucionario) |
| 09 | BCNF, 4FN, 5FN, Desnormalización | `Clase_09.txt` | `semana_09.html` (342 líneas) |
| 10 | JOINs y Subconsultas | `Clase_10.txt` (JOINs) | `semana_10.html` (256 líneas) |
| 11 | GROUP BY, HAVING, Funciones de Grupo | `Clase_10.txt` (agrupamiento) | `semana_11.html` (205 líneas) |
| 12 | PL/SQL: Bloques, Variables, Cursores | `Clase_11.txt` (intro) | `semana_12.html` (317 líneas) |
| 13 | Procedimientos, Funciones, Triggers | `Clase_11.txt` (avanzado) | `semana_13.html` (326 líneas) |
| 14 | Data Warehouse | `Clase_12.txt` + `Clase_15.txt` + `Script_Ejemplo_Warehouse.txt` | `semana_14.html` (378 líneas) |
| 15 | Tópicos Avanzados (HA) | `Taller_HA_MSSQL2012.txt` | `semana_15.html` (323 líneas) |
| 16 | **Examen Final** | Resumen 9-15 + mock exam | `semana_16.html` (340 líneas, 4 secciones + solucionario) |

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
- [x] Todos los HTMLs usan BEM classes de `master.css` (sin clases legacy en semana_*.html)
- [x] `extra_*.html` mantienen su estructura legacy (contenido complementario no modificado)
- [x] Exámenes tipo con 4 secciones + solucionario completo

---

## Agentes

| Agente | Rol |
|--------|-----|
| **ArquiDB** | Data Architect — revisa y aprueba cada fase |
| **TXT Cleaner** | Limpia encoding, artefactos, whitespace |
| **Content Mapper** | Mapea contenido TXT a estructura semanal |
| **HTML Builder** | Genera HTMLs con plantilla y UI/UX |
| **Exam Builder** | Crea exámenes tipo con solucionarios |
