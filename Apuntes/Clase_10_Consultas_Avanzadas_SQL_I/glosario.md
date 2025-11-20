# Glosario - Clase 10: JOIN, Subconsultas y Agrupamiento (SQL Avanzado)

*   **AVG (Función de Agregación):** Calcula el promedio de un conjunto de valores.
*   **COUNT (Función de Agregación):** Cuenta el número de filas que cumplen una condición especificada.
*   **Cross Join:** Une cada fila de la primera tabla con cada fila de la segunda. ¡El "producto cartesiano" que genera resultados enormes y sin sentido si no se usa con precaución!
*   **Equijoin:** El tipo más común de `JOIN`, une tablas cuando los valores en las columnas especificadas son *exactamente iguales* (`=`).
*   **Funciones de Agregamiento:** Funciones SQL que operan sobre un conjunto de filas y devuelven un único valor de resumen (ej. `MIN`, `MAX`, `AVG`, `SUM`, `COUNT`).
*   **GROUP BY:** Cláusula SQL utilizada para agrupar filas que tienen los mismos valores en una o más columnas, permitiendo aplicar funciones de agregación a cada grupo.
*   **HAVING:** Cláusula SQL que filtra los grupos de filas resultantes de una cláusula `GROUP BY`, aplicando condiciones a los resultados de las funciones de agregación (¡es como un `WHERE` para grupos!).
*   **JOIN (Unión):** Operación fundamental en SQL para combinar filas de dos o más tablas basándose en una columna común.
*   **LEFT OUTER JOIN (Left Join):** Devuelve todas las filas de la tabla izquierda y las filas coincidentes de la tabla derecha. Si no hay coincidencia en la derecha, los valores de la tabla derecha son `NULL`.
*   **MAX (Función de Agregación):** Devuelve el valor máximo de un conjunto de valores.
*   **MIN (Función de Agregación):** Devuelve el valor mínimo de un conjunto de valores.
*   **Non-Equijoin:** Un tipo de `JOIN` que une tablas utilizando operadores de comparación distintos de la igualdad (ej. `<`, `>`, `BETWEEN`).
*   **Outer Join:** Categoría de `JOIN` (incluye `LEFT`, `RIGHT`, `FULL`) que devuelve filas que normalmente no se mostrarían, es decir, filas que no tienen una coincidencia en la tabla unida.
*   **RIGHT OUTER JOIN (Right Join):** Devuelve todas las filas de la tabla derecha y las filas coincidentes de la tabla izquierda. Si no hay coincidencia en la izquierda, los valores de la tabla izquierda son `NULL`.
*   **Self Join:** Tipo de `JOIN` donde una tabla se une consigo misma, útil para comparar filas dentro de la misma tabla o para relaciones recursivas (ej. empleado y su jefe, ambos en la misma tabla de empleados).
*   **Subconsultas:** Una consulta SQL anidada dentro de otra sentencia SQL. Se ejecuta primero y su resultado alimenta a la consulta principal.
*   **SUM (Función de Agregación):** Calcula la suma de un conjunto de valores numéricos.