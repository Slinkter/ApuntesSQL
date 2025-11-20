# Clase 10: Consultas Avanzadas SQL I

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Introducción a Consultas SQL Avanzadas

Las consultas SQL avanzadas permiten a los usuarios extraer información más compleja y realizar análisis sofisticados sobre los datos almacenados en una base de datos. Se construyen sobre las consultas simples (`SELECT`, `FROM`, `WHERE`, `ORDER BY`) añadiendo funcionalidades como agrupamiento, funciones agregadas, uniones entre tablas y subconsultas.

### Agrupamiento de Datos (GROUP BY)

La cláusula `GROUP BY` se utiliza para agrupar filas que tienen los mismos valores en las columnas especificadas en grupos de resumen. A menudo se usa junto con funciones de agregación para realizar cálculos por cada grupo.

**Funciones de Agregación Comunes:**
*   `COUNT()`: Cuenta el número de filas o valores no nulos.
*   `SUM()`: Calcula la suma de los valores.
*   `AVG()`: Calcula el promedio de los valores.
*   `MIN()`: Encuentra el valor mínimo.
*   `MAX()`: Encuentra el valor máximo.

**Sintaxis Básica:**
```sql
SELECT column1, aggregate_function(column2)
FROM table_name
WHERE condition
GROUP BY column1, column3, ...
HAVING aggregate_condition
ORDER BY column1;
```

### Filtrado de Grupos (HAVING)

La cláusula `HAVING` se utiliza para filtrar grupos generados por `GROUP BY`, de manera similar a cómo `WHERE` filtra filas individuales. La condición en `HAVING` típicamente involucra funciones de agregación.

### Uniones de Tablas (JOINs)

Las operaciones `JOIN` permiten combinar filas de dos o más tablas basándose en una columna relacionada entre ellas. Son fundamentales para recuperar datos de bases de datos relacionales normalizadas.

*   **`INNER JOIN` (o simplemente `JOIN`):** Devuelve solo las filas donde hay una coincidencia en ambas tablas. Es el tipo de `JOIN` más común.
    ```sql
    SELECT t1.column, t2.column
    FROM table1 t1
    INNER JOIN table2 t2 ON t1.common_column = t2.common_column;
    ```
*   **`LEFT JOIN` (o `LEFT OUTER JOIN`):** Devuelve todas las filas de la tabla izquierda (la primera en la cláusula `FROM`) y las filas coincidentes de la tabla derecha. Si no hay coincidencia en la derecha, los valores de la tabla derecha son `NULL`.
*   **`RIGHT JOIN` (o `RIGHT OUTER JOIN`):** Devuelve todas las filas de la tabla derecha y las filas coincidentes de la tabla izquierda. Si no hay coincidencia en la izquierda, los valores de la tabla izquierda son `NULL`.
*   **`FULL JOIN` (o `FULL OUTER JOIN`):** Devuelve todas las filas cuando hay una coincidencia en la tabla izquierda o en la derecha. Si no hay coincidencia en una de las tablas, los valores de esa tabla son `NULL`.
*   **`CROSS JOIN`:** Produce el producto cartesiano de las dos tablas, es decir, combina cada fila de la primera tabla con cada fila de la segunda tabla. (Equivalente a `FROM table1, table2` sin `WHERE` o a `INNER JOIN` sin `ON`).
*   **`SELF JOIN`:** Una tabla se une consigo misma, útil para comparar filas dentro de la misma tabla (ej. encontrar empleados que reportan a otros empleados en la misma tabla de empleados).

### Subconsultas (Subqueries/Nested Queries)

Una subconsulta es una consulta SQL que está anidada dentro de otra consulta SQL (la consulta externa o principal). Puede utilizarse en varias cláusulas, como `SELECT`, `FROM`, `WHERE`, `HAVING`.

**Tipos y Usos Comunes:**
*   **En la cláusula `WHERE`:** Para filtrar resultados de la consulta externa basándose en los resultados de la subconsulta.
    *   `WHERE column IN (SELECT ...)`: Comprueba si un valor está presente en el conjunto de resultados de la subconsulta.
    *   `WHERE column = (SELECT ...)`: Para subconsultas que devuelven un solo valor.
    *   `WHERE EXISTS (SELECT ...)`: Comprueba la existencia de filas devueltas por la subconsulta.
*   **En la cláusula `FROM` (Derived Tables/Inline Views):** El resultado de una subconsulta se trata como una tabla temporal.
*   **En la cláusula `SELECT` (Scalar Subqueries):** Devuelve un único valor para cada fila de la consulta externa.

---

## Pistas y Keywords

*   **GROUP BY:** Agrupar filas para agregación.
*   **Funciones Agregadas:** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
*   **HAVING:** Filtrar grupos agregados.
*   **JOIN:** Combinar datos de múltiples tablas.
*   **INNER JOIN:** Coincidencia en ambas tablas.
*   **LEFT JOIN:** Todas las filas de la izquierda.
*   **RIGHT JOIN:** Todas las filas de la derecha.
*   **FULL JOIN:** Todas las filas (izquierda o derecha).
*   **CROSS JOIN:** Producto cartesiano.
*   **SELF JOIN:** Unir una tabla consigo misma.
*   **Subconsulta:** Consulta anidada.
*   **Derived Table:** Subconsulta en `FROM`.
*   **Scalar Subquery:** Subconsulta en `SELECT` que devuelve un valor único.
*   **EXISTS:** Comprueba existencia de filas.

---

## Resumen Final Crítico

Las consultas SQL avanzadas, a través del uso de `GROUP BY` con `HAVING`, diversas operaciones `JOIN` y la versatilidad de las subconsultas, transforman SQL de un lenguaje de recuperación básica a una herramienta poderosa para el análisis de datos. Estas construcciones permiten a los usuarios extraer conocimiento profundo de bases de datos complejas, combinando información de múltiples fuentes, agregando resultados y filtrando basándose en criterios dinámicos. Dominar estas técnicas es crucial para cualquier rol que requiera una interacción significativa con bases de datos relacionales para la toma de decisiones.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase profundiza en el uso de DML (`SELECT`) de la "Clase 05: DML y Consultas Simples". Se basa en la estructura de "Bases de Datos Relacionales" (Clase 03) y en los principios de "Modelamiento de Datos" (Clase 06) para entender cómo combinar tablas eficazmente.
*   **Conexiones Siguientes:** Es la antesala de las "Consultas Avanzadas SQL II" (Clase 11), donde se abordarán temas aún más complejos como funciones de ventana y expresiones de tabla comunes. También sienta las bases para el uso de consultas complejas en "Programación PL/SQL" (Clase 12 y 13) y en el análisis de "Data Warehouse" (Clase 14).

---
**Nota:** El contenido de esta clase ha sido inferido del título del curso y conocimientos generales sobre la materia, dado que el archivo `.ppt` original no pudo ser procesado directamente.
