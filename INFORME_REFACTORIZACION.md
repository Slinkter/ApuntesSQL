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

| Archivo | Problema | Accion |
|---------|----------|--------|
| `ULima/Silabus.txt` | Encoding latin1 -> `�` | Recodificado a UTF-8 |
| `ULima/Clases/Clase_10.txt` | ~479 lineas de arte ASCII corrupto (EMPXDEPT cross join) | Extirpadas lineas 56-534 |
| `ULima/Clases/Clase_*.txt` (11 archivos) | Vinietas `▪` `` `❑` `` `➢` | Reemplazadas por `-` `→` `*` |
| `ULima/otros/Taller_HA_MSSQL2012.txt` | Texto stretch: "IIIInnnngggg...." | Normalizado a texto legible |
| `ULima/otros/Restrictions on Parallel DML.txt` | Archivo vacio (0 bytes) | Nota: "Pendiente de transcripcion" |
| `ULima/otros/Practica_03_Sol.txt` | Numeracion de preguntas erronea | Corregido a secuencial 1-10 |

## Fase 2: Mapeo semanal

| Sem | Tema | Fuente TXT | HTML | Lineas |
|-----|------|-----------|------|--------|
| 01 | Fundamentos de Informacion | `Clase_00.txt` | `semana_01.html` | 247 |
| 02 | Sistema de Gestion de BD | `Clase_01.txt` + `Clase_02.txt` | `semana_02.html` | 309 |
| 03 | Bases de Datos Relacionales | `Clase_03.txt` (conceptos) | `semana_03.html` | 263 |
| 04 | DDL y Administracion | `Clase_03.txt` (DDL) | `semana_04.html` | 286 |
| 05 | DML y Consultas Simples | `Clase_04.txt` | `semana_05.html` | 206 |
| 06 | Modelamiento E-R | `Clase_05.txt` | `semana_06.html` | ~220 |
| 07 | Normalizacion 1FN-3FN | `Clase_06.txt` + `NormalizacioBD.txt` | `semana_07.html` | ~280 |
| 08 | **Examen Parcial** | Mock exam (4 secciones) | `semana_08.html` | **507** |
| 09 | BCNF, 4FN, 5FN, Desnormalizacion | `Clase_09.txt` | `semana_09.html` | 342 |
| 10 | JOINs y Subconsultas | `Clase_10.txt` (JOINs) | `semana_10.html` | 256 |
| 11 | GROUP BY, HAVING, Agregacion | `Clase_10.txt` (agrupamiento) | `semana_11.html` | 205 |
| 12 | PL/SQL: Bloques y Cursores | `Clase_11.txt` (intro) | `semana_12.html` | 317 |
| 13 | Procedimientos y Triggers | `Clase_11.txt` (avanzado) | `semana_13.html` | 326 |
| 14 | Data Warehouse | `Clase_12.txt` + `Clase_15.txt` + `Script_Ejemplo_Warehouse.txt` | `semana_14.html` | 378 |
| 15 | Alta Disponibilidad | `Taller_HA_MSSQL2012.txt` | `semana_15.html` | 323 |
| 16 | **Examen Final** | Mock exam (4 secciones) | `semana_16.html` | **340** |

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

| Metrica | Valor |
|---------|-------|
| HTMLs creados/mejorados | 16 |
| HTMLs nuevos | 5 |
| TXT limpiados | 15 |
| Archivos con encoding corregido | 1 (+11 con vinietas) |
| Lineas removidas (datos corruptos) | ~479 |
| Preguntas de examen generadas | 37 (20 teoria + 9 ejercicios practicos + 8 consultas SQL) |
| Solucionarios | 2 completos |
| Clases legacy eliminadas | ~80+ instancias en semana_*.html |
| Emojis removidos | ~50+ instancias |
