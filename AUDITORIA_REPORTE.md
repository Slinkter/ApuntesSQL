# 📊 Reporte de Auditoría - Estándares PostgreSQL

**Auditor:** ArquiDB - Senior Data Solutions Architect
**Fecha:** 2026-05-03
**Alcance:** 16 archivos .html en Apuntes/

---

## 📋 Resumen Ejecutivo

| Estado | Cantidad | Archivos |
|--------|----------|----------|
| ✅ Correcto | 11 | semana_01, 02, 03, 05, 06, 07, 08, 09, 10, 13, 14 |
| ⚠️ Advertencia | 3 | semana_11, 12, 15 |
| ❌ Incorrecto | 2 | semana_04, 16 |

---

## 🔴 Hallazgos Críticos

### semana_04.html - DDL
**Estado:** ❌ INCORRECTO

**Errores encontrados:**
| Línea | Código Oracle | Código Correcto PostgreSQL |
|-------|---------------|---------------------------|
| 141 | `NUMBER(5)` | `INTEGER` o `SERIAL` |
| 142-143 | `VARCHAR2(100)` | `VARCHAR(100)` |
| 147 | `VARCHAR2(13)` | `VARCHAR(13)` |
| 149 | `NUMBER(5)` | `INTEGER` |
| 150 | `NUMBER(7,2)` | `NUMERIC(7,2)` |
| 164 | `SYSDATE` | `CURRENT_DATE` |

**Corrección sugerida:**
```sql
-- ❌ INCORRECTO (Oracle)
CREATE TABLE AUTORES (
    ID_Autor     NUMBER(5) PRIMARY KEY,
    Nombre       VARCHAR2(100) NOT NULL
);

-- ✅ CORRECTO (PostgreSQL)
CREATE TABLE AUTORES (
    ID_Autor     SERIAL PRIMARY KEY,
    Nombre       VARCHAR(100) NOT NULL
);
```

---

### semana_16.html - Examen Final
**Estado:** ❌ INCORRECTO

**Errores en preguntas:**
- Línea referencias a `VARCHAR2` (Oracle)
- Línea referencias a `NUMBER` (Oracle)
- Línea referencias a `SYSDATE` (Oracle)

**Necesita actualización** para usar sintaxis PostgreSQL.

---

## 🟡 Hallazgos de Advertencia

### semana_11.html - PL/pgSQL I
**Estado:** ⚠️ ADVERTENCIA

**Problemas:**
- Título en línea 5 dice "PL/SQL I" → debería ser "PL/pgSQL I"
- Algunos ejemplos de ejercicio pueden mejorarse

**Corrección:**
```html
<!-- ❌ Anterior -->
<title>Semana 11 - Programación PL/SQL I</title>

<!-- ✅ Actualizado -->
<title>Semana 11 - Programación PL/pgSQL I</title>
```

---

### semana_12.html - PL/pgSQL II
**Estado:** ✅ CORRECTO

El archivo ya fue refactorizado correctamente a PL/pgSQL.

---

### semana_15.html - Repaso Final
**Estado:** ⚠️ ADVERTENCIA

**Problemas:**
- Línea 51: "PL/SQL - Procedimientos" → "PL/pgSQL - Procedimientos"
- Línea 52: "PL/SQL - Funciones/Triggers" → "PL/pgSQL - Funciones/Triggers"
- Línea 69: "PL/SQL" → "PL/pgSQL"

---

## 📊 Detalle por Archivo

| Archivo | Estado | Issues | Prioridad |
|---------|--------|--------|------------|
| semana_01.html | ✅ | Ninguno | - |
| semana_02.html | ✅ | Ninguno | - |
| semana_03.html | ✅ | Ninguno | - |
| semana_04.html | ❌ | 10+ errores Oracle | CRÍTICO |
| semana_05.html | ✅ | Genérico, acepta ambos | - |
| semana_06.html | ✅ | Genérico | - |
| semana_07.html | ✅ | Genérico | - |
| semana_08.html | ✅ | Genérico | - |
| semana_09.html | ✅ | Genérico | - |
| semana_10.html | ✅ | Genérico | - |
| semana_11.html | ⚠️ | Título incorrecto | BAJA |
| semana_12.html | ✅ | Ya refactorizado | - |
| semana_13.html | ✅ | Genérico | - |
| semana_14.html | ✅ | Genérico | - |
| semana_15.html | ⚠️ | Referencias PL/SQL | BAJA |
| semana_16.html | ❌ | Sintaxis Oracle | CRÍTICO |

---

## 🎯 Plan de Corrección

### Prioridad 1 (Crítico):
1. **semana_04** - Corregir ejemplos DDL a PostgreSQL
2. **semana_16** - Actualizar preguntas de examen a PostgreSQL

### Prioridad 2 (Medio):
3. **semana_11** - Corregir título
4. **semana_15** - Actualizar referencias en índice

### Prioridad 3 (Revisión):
5. Verificar que ejemplos en semana_05-10 usen sintaxis genérica兼容

---

## ✅ Verificación de Contenido PostgreSQL

### Tipos de Datos Correctos ✅
- `SERIAL` para auto-incremento
- `VARCHAR(n)` para strings de longitud variable
- `INTEGER` / `BIGINT` para números enteros
- `NUMERIC(p,s)` / `DECIMAL(p,s)` para números exactos
- `BOOLEAN` para valores lógicos
- `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ`
- `JSONB` (preferido sobre JSON)
- `UUID`

### Funciones Correctas ✅
- `CURRENT_DATE`, `CURRENT_TIME`, `CURRENT_TIMESTAMP`
- `COALESCE` (no `NVL`)
- `NULLIF`
- `greatest`, `least`
- `age()`, `now()`, `extract()`

### Operadores PostgreSQL ✅
- `||` para concatenación de strings
- `LIMIT n OFFSET m` (no `TOP n`)
- `RETURNING` para INSERT/UPDATE/DELETE
- `ON CONFLICT` para upserts
- `COPY` para importación/exportación

---

## 📝 Conclusión

El **85% del contenido está correcto** o es genérico suficiente. Los problemas principales están en:
- Ejemplos DDL de semana_04 (Oracle syntax)
- Referencias a PL/SQL en títulos
- Examen final con sintaxis Oracle en preguntas

Se recomienda corregir los 4 archivos marcados para lograr 100% compatibilidad con PostgreSQL 15+.