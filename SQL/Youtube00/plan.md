# Plan: Mejorar PostgresSQL/Youtube00 con 150 ejercicios bancarios/retail

**Estado**: Listo para agente (paso a paso)

## 🎯 Objetivo

Transformar las 3 guías de estudio (básico, intermedio, avanzado) en material educativo de nivel Senior Data Architect para bancos y retail, con:
- **150 ejercicios resueltos** (50 básico, 50 intermedio, 50 avanzado)
- **Conceptos integrados**: DDL, DML, JOINs, CTEs, ventanas, subqueries, analítica avanzada
- **Explicaciones infantiles**: como si fuera para un niño de 10 años (pero profundo)
- **Diagramas visuales**: JOINs con ASCII art, diagramas isométricos 2D
- **Contexto bancario/retail**: casos reales (transacciones, inventario, clientes, scoring)
- **Ejercicios ejecutables**: contra db_northwind.sql
- **Nivel entrevista**: problemas de Senior Data Architect en bancos y retail

---

## 📋 Tareas (paso a paso para agente)

### Fase 1: Análisis Northwind
**Acción**: Explorar `PostgresSQL/Youtube00/db_northwind.sql`
- [x] Listar todas las tablas
- [x] Identificar PKs y FKs
- [x] Mapear relaciones entre tablas
- [x] Notar tipos de datos clave
- **Salida esperada**: Diagrama mental de la estructura

---

### Fase 2: Crear 50 Ejercicios BÁSICO

**Ubicación de salida**: `PostgresSQL/Youtube00/1.basico.md`

**Estructura para CADA ejercicio**:
\`\`\`
### Ejercicio N: [Título descriptivo]

**📊 Contexto bancario/retail**: 
[Explicación de por qué es importante en un banco o retail]

**🎯 Enunciado**: 
[Pregunta clara en SQL terms]

**🔑 Conceptos clave** (explicar como para un niño de 10 años):
- Concepto A: "[Explicación simple]"
- Concepto B: "[Explicación simple]"

**📐 Diagrama** (ASCII o simple descripción):
[Mostrar las tablas y cómo se conectan]

**✅ Solución**:
\`\`\`sql
[SQL code aquí - DEBE SER EJECUTABLE]
\`\`\`

**💡 Explicación paso a paso**:
[Desglosar qué hace cada parte, como para un niño]

**⚡ EXPLAIN (ANALYZE)** (si es relevante):
\`\`\`
[Output de EXPLAIN aquí]
\`\`\`
\`\`\`

**Temas a cubrir en 50 ejercicios básico**:
- **Ejercicios 1-10**: SELECT, WHERE, ORDER BY, LIMIT, OFFSET
  - Ej: "Listar los 5 primeros clientes por apellido"
  - Ej: "Mostrar pedidos del año 1997 ordenados por fecha"
  
- **Ejercicios 11-20**: INNER JOIN (relacionar tablas)
  - Ej: "Mostrar cada pedido con el nombre del cliente"
  - Ej: "Listar productos con su categoría"
  
- **Ejercicios 21-30**: LEFT JOIN (incluir registros sin match)
  - Ej: "Mostrar clientes con y sin pedidos"
  - Ej: "Listar empleados y sus supervisores (algunos sin supervisor)"
  
- **Ejercicios 31-40**: COUNT, SUM, AVG (agregaciones simples)
  - Ej: "Contar cuántos pedidos hizo cada cliente"
  - Ej: "Sumar las cantidades vendidas por producto"
  
- **Ejercicios 41-50**: Combinaciones de filtros, múltiples JOINs
  - Ej: "Clientes de 'Germany' con sus pedidos en 1997"
  - Ej: "Productos vendidos por empleados de 'Seattle'"

**Criterio de éxito**: 50 ejercicios, todos ejecutables, con explicación simple y contexto real

---

### Fase 3: Crear 50 Ejercicios INTERMEDIO

**Ubicación de salida**: `PostgresSQL/Youtube00/2.intermedio.md`

**Misma estructura que básico**

**Temas a cubrir en 50 ejercicios intermedio**:
- **Ejercicios 1-10**: GROUP BY + agregaciones con WHERE/HAVING
  - Ej: "Total de ventas por cliente (solo clientes con >5 pedidos)"
  - Ej: "Promedio de cantidad vendida por producto"
  
- **Ejercicios 11-20**: Subconsultas escalares y correlacionadas
  - Ej: "Cliente que gastó más dinero en cada categoría de producto"
  - Ej: "Pedidos con precio mayor al promedio"
  
- **Ejercicios 21-30**: CASE expressions (lógica condicional)
  - Ej: "Clasificar clientes como 'Premium' (>$5000) o 'Regular'"
  - Ej: "Categorizar productos por precio (Caro, Medio, Barato)"
  
- **Ejercicios 31-40**: JOINs complejos (3+ tablas, SELF JOIN)
  - Ej: "Empleado, supervisor, cliente y sus pedidos (4 tablas)"
  - Ej: "Clientes en la misma ciudad (SELF JOIN)"
  
- **Ejercicios 41-50**: Ventanas básicas (ROW_NUMBER, RANK)
  - Ej: "Top 3 productos por categoría (using RANK)"
  - Ej: "Ranking de empleados por facturación total"

**Criterio de éxito**: 50 ejercicios intermedio, todos ejecutables

---

### Fase 4: Crear 50 Ejercicios AVANZADO

**Ubicación de salida**: `PostgresSQL/Youtube00/3.avanzado.md`

**Misma estructura que básico**

**Temas a cubrir en 50 ejercicios avanzado**:
- **Ejercicios 1-10**: CTEs (WITH)
  - Ej: "Usar CTE para calcular facturación por mes, luego filtrar > 10000"
  - Ej: "CTE con múltiples niveles de agregación"
  
- **Ejercicios 11-20**: Recursive CTEs
  - Ej: "Organigrama completo (empleados y sus supervisores recursivamente)"
  - Ej: "Jerarquía de categorías"
  
- **Ejercicios 21-30**: Ventanas avanzadas (ROWS BETWEEN, LAG, LEAD)
  - Ej: "Promedio móvil de ventas diarias (3 días)"
  - Ej: "Diferencia en ventas vs mes anterior (LAG)"
  
- **Ejercicios 31-40**: LATERAL joins, Cohort analysis
  - Ej: "Top 5 productos más caros por categoría (LATERAL)"
  - Ej: "Matriz de retención mensual de clientes"
  
- **Ejercicios 41-50**: Optimization (EXPLAIN ANALYZE, índices, particionamiento)
  - Ej: "Analizar y optimizar una consulta lenta (before/after índice)"
  - Ej: "Explicar cost vs actual time en EXPLAIN ANALYZE"

**Criterio de éxito**: 50 ejercicios avanzado, todos ejecutables, con EXPLAIN detallado

---

## 📊 Resumen de entregas

| Fase | Archivo | Ejercicios | Estado |
|------|---------|-----------|--------|
| 2 | 1.basico.md | 50 | [x] Completado |
| 3 | 2.intermedio.md | 50 | [ ] Por hacer |
| 4 | 3.avanzado.md | 50 | [ ] Por hacer |

---

## ✅ Criterios de éxito GLOBAL

- ✓ 150 ejercicios ejecutables contra Northwind (50 por nivel)
- ✓ Cada uno con contexto bancario/retail realista
- ✓ Explicaciones en lenguaje accesible (como para niño de 10 años) pero técnico
- ✓ Diagramas ASCII simples mostrando tabla relationships
- ✓ Conceptos claros (DDL, DML, JOINs, subconsultas, ventanas) marcados y explicados
- ✓ Listos para entrevista Senior Data Architect en banco/retail
- ✓ EXPLAIN ANALYZE cuando sea relevante

---

## 🚀 Siguientes pasos post-ejercicios

1. Validar cada ejercicio contra PostgreSQL 15+ (puede usar Docker)
2. Commit con todas las guías mejoradas
3. Actualizar README.md en Youtube00 con índice de ejercicios
4. Crear un .sql file separado para cada nivel si es necesario (opcional)

---

**Notas adicionales**:
- Usar la base de datos Northwind disponible en `PostgresSQL/Youtube00/db_northwind.sql`
- Cada ejercicio debe ser ejecutable directamente en psql
- Explicaciones deben ser claras pero técnicas (audiencia: Senior DA candidates)
- Incluir contextos reales (banking: transacciones, clientes; retail: inventario, ventas)
