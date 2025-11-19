# Glosario - Clase 10: Consultas Avanzadas SQL I

*   **SQL Avanzado:** Se refiere al uso de funcionalidades de SQL que van más allá de las consultas básicas, permitiendo la manipulación y análisis de datos de forma más compleja.
*   **GROUP BY:** Cláusula SQL utilizada para agrupar filas que tienen los mismos valores en una o más columnas, a menudo en conjunto con funciones de agregación.
*   **Funciones de Agregación:** Funciones SQL que realizan un cálculo sobre un conjunto de filas y devuelven un único valor de resumen para ese conjunto (ej. `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).
*   **HAVING:** Cláusula SQL utilizada para filtrar grupos de filas resultantes de una cláusula `GROUP BY`, aplicando condiciones a los resultados de las funciones de agregación.
*   **JOIN (SQL):** Operación fundamental en SQL que combina filas de dos o más tablas en función de una columna relacionada entre ellas, permitiendo consultar datos de múltiples fuentes.
*   **INNER JOIN:** Tipo de `JOIN` que devuelve solo las filas que tienen valores coincidentes en ambas tablas unidas.
*   **LEFT JOIN (LEFT OUTER JOIN):** Tipo de `JOIN` que devuelve todas las filas de la tabla izquierda y las filas coincidentes de la tabla derecha. Si no hay coincidencia en la derecha, los valores de la tabla derecha son `NULL`.
*   **RIGHT JOIN (RIGHT OUTER JOIN):** Tipo de `JOIN` que devuelve todas las filas de la tabla derecha y las filas coincidentes de la tabla izquierda. Si no hay coincidencia en la izquierda, los valores de la tabla izquierda son `NULL`.
*   **FULL JOIN (FULL OUTER JOIN):** Tipo de `JOIN` que devuelve todas las filas de ambas tablas cuando hay una coincidencia en la tabla izquierda o en la derecha. Si no hay coincidencia, los valores son `NULL`.
*   **CROSS JOIN:** Un tipo de `JOIN` que devuelve el producto cartesiano de las filas de las tablas unidas, es decir, cada fila de la primera tabla se combina con cada fila de la segunda.
*   **SELF JOIN:** Un tipo de `JOIN` donde una tabla se une consigo misma, útil para comparar filas dentro de la misma tabla.
*   **Subconsulta (Subquery/Nested Query):** Una consulta SQL completa que se anida dentro de otra sentencia SQL, utilizada para filtrar datos, proporcionar valores a expresiones o como una tabla derivada.
*   **Derived Table (Tabla Derivada):** El resultado de una subconsulta que se utiliza en la cláusula `FROM` de una consulta principal, tratándose como una tabla temporal.
*   **Scalar Subquery (Subconsulta Escalar):** Una subconsulta que devuelve un único valor (una sola columna y una sola fila), que puede ser utilizada en la cláusula `SELECT`, `WHERE` o `HAVING`.
*   **EXISTS (SQL):** Operador utilizado con subconsultas para verificar la existencia de filas que cumplen una condición en la subconsulta.
*   **IN (Subconsulta):** Operador que compara un valor con un conjunto de valores devueltos por una subconsulta, devolviendo verdadero si el valor coincide con alguno del conjunto.
*   **Operadores de Conjunto (UNION, INTERSECT, EXCEPT/MINUS):** Operadores SQL que combinan los resultados de dos o más sentencias `SELECT`, tratando sus resultados como conjuntos de filas. `UNION` (combina y elimina duplicados), `INTERSECT` (devuelve filas comunes), `EXCEPT`/`MINUS` (devuelve filas en la primera consulta que no están en la segunda).
