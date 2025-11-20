# Clase 11: Consultas Avanzadas SQL II

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Introducción a Funcionalidades Avanzadas de SQL

Esta clase se enfoca en características más complejas de SQL, incluyendo funciones analíticas (o de ventana), expresiones de tabla comunes (CTEs), y otras técnicas avanzadas que permiten resolver problemas de negocio sofisticados y optimizar la legibilidad y el rendimiento de las consultas.

### Funciones Analíticas (Funciones de Ventana)

Las funciones analíticas calculan un valor agregado basándose en un grupo de filas ("ventana") relacionadas con la fila actual, sin agrupar el conjunto de resultados. Esto permite realizar cálculos como totales acumulados, promedios móviles, rankings y diferencias entre filas, manteniendo el detalle de cada fila.

**Estructura Básica:**
```sql
FUNCTION_NAME(arguments) OVER (
    [PARTITION BY expression [, ...]]
    [ORDER BY expression [ASC | DESC] [, ...]]
    [frame_clause]
)
```
*   **`PARTITION BY`:** Divide el conjunto de resultados en grupos lógicos (ventanas), y la función se aplica de forma independiente a cada ventana.
*   **`ORDER BY`:** Define el orden de las filas dentro de cada ventana. Es crucial para funciones que dependen del orden (ej. ranking, acumulados).
*   **`frame_clause` (Cláusula de Ventana):** Define el subconjunto de filas dentro de la partición sobre el cual se calcula la función. Puede ser `ROWS` o `RANGE`, y especifica límites como `UNBOUNDED PRECEDING`, `CURRENT ROW`, `N PRECEDING/FOLLOWING`.

**Ejemplos de Funciones Analíticas:**
*   **`ROW_NUMBER()`:** Asigna un número secuencial único a cada fila dentro de su partición, según el orden especificado.
*   **`RANK()` / `DENSE_RANK()`:** Asigna un rango a cada fila dentro de su partición. `RANK()` deja huecos en caso de empates, `DENSE_RANK()` no.
*   **`LEAD(column, offset, default_value)` / `LAG(column, offset, default_value)`:** Accede a una fila posterior (`LEAD`) o anterior (`LAG`) dentro de la misma partición, útil para comparaciones.
*   **`SUM(...) OVER(...)` / `AVG(...) OVER(...)`:** Funciones de agregación utilizadas como funciones de ventana para calcular sumas o promedios acumulados o móviles.

### Expresiones de Tabla Comunes (CTEs - Common Table Expressions)

Las CTEs (`WITH` clause) son consultas con nombre temporal que se pueden referenciar dentro de una sentencia SQL principal (`SELECT`, `INSERT`, `UPDATE`, `DELETE`). Mejoran la legibilidad y modularidad de las consultas complejas.

**Sintaxis:**
```sql
WITH
  cte_name1 AS (SELECT ...),
  cte_name2 AS (SELECT ... FROM cte_name1 WHERE ...)
SELECT ... FROM cte_name2 WHERE ...;
```
*   **Ventajas:**
    *   **Legibilidad:** Descompone consultas complejas en bloques lógicos más pequeños y fáciles de entender.
    *   **Reutilización:** Una CTE puede ser referenciada múltiples veces dentro de la misma consulta principal.
    *   **Recursividad:** Permiten definir consultas recursivas (útil para estructuras jerárquicas como organigramas).

### Funciones de Ventana para Cálculos Acumulativos

Las funciones de ventana son especialmente útiles para calcular valores acumulativos o móviles.
*   **`SUM(cantidad) OVER (PARTITION BY categoria ORDER BY fecha ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`:** Suma acumulada por categoría y fecha.
*   **`AVG(ventas) OVER (ORDER BY fecha ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`:** Promedio móvil de ventas de los últimos 3 periodos.

### Otros Operadores y Cláusulas Avanzadas

*   **`UNION ALL`:** Combina los resultados de dos o más sentencias `SELECT`, incluyendo las filas duplicadas. (`UNION` elimina duplicados).
*   **`INTERSECT`:** Devuelve las filas comunes a los resultados de dos sentencias `SELECT`.
*   **`EXCEPT` / `MINUS` (Oracle):** Devuelve las filas que están en el primer `SELECT` pero no en el segundo.
*   **`CASE` Expressions:** Permite implementar lógica condicional dentro de una consulta SQL, devolviendo diferentes valores basándose en diversas condiciones.

---

## Pistas y Keywords

*   **Funciones Analíticas:** Cálculos sobre ventanas de filas.
*   **Función de Ventana:** `OVER (PARTITION BY ... ORDER BY ... frame_clause)`.
*   **PARTITION BY:** Divide el conjunto de datos.
*   **ROW_NUMBER(), RANK(), DENSE_RANK():** Funciones de ranking.
*   **LEAD(), LAG():** Acceder a filas anteriores/posteriores.
*   **CTEs (Common Table Expressions):** Consultas temporales con nombre (`WITH`).
*   **`WITH` clause:** Define CTEs.
*   **`UNION ALL`, `INTERSECT`, `EXCEPT/MINUS`:** Operadores de conjunto.
*   **`CASE` Expression:** Lógica condicional en SQL.

---

## Resumen Final Crítico

Las capacidades avanzadas de SQL, como las funciones analíticas y las CTEs, extienden significativamente el poder del lenguaje más allá de las consultas básicas, permitiendo a los analistas y desarrolladores resolver problemas de negocio complejos directamente en la base de datos. Las funciones de ventana son indispensables para análisis de tendencias, comparaciones secuenciales y cálculos acumulativos sin perder el detalle de las filas. Las CTEs mejoran la estructuración y legibilidad de las consultas anidadas, facilitando el mantenimiento y la colaboración. El dominio de estas herramientas es un paso crucial para convertirse en un experto en SQL y explotar al máximo el potencial analítico de los datos.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase se basa directamente en las "Consultas Avanzadas SQL I" (Clase 10), profundizando en técnicas más sofisticadas para manipular y analizar datos. También utiliza los conceptos de `JOIN`s, `GROUP BY` y subconsultas.
*   **Conexiones Siguientes:** Estas técnicas avanzadas de SQL son fundamentales para el desarrollo de sistemas de "Data Warehouse" (Clase 14), donde las consultas complejas para reporting y análisis son la norma. También son herramientas clave para "Tópicos Avanzados de Bases de Datos" (Clase 15) y en la implementación de lógicas complejas dentro de "Programación PL/SQL" (Clase 12 y 13).

---
**Nota:** El contenido de esta clase ha sido inferido del título del curso y conocimientos generales sobre la materia, dado que el archivo `.ppt` original no pudo ser procesado directamente.
