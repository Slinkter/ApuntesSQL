# Glosario - Clase 11: Consultas Avanzadas SQL II

*   **Funciones Analíticas (SQL):** Funciones que calculan un valor agregado basándose en un grupo de filas (una "ventana") relacionadas con la fila actual, pero sin agrupar el conjunto de resultados.
*   **Funciones de Ventana (SQL):** Sinónimo de funciones analíticas, se refieren a las funciones que usan la cláusula `OVER` para definir un subconjunto de filas para el cálculo.
*   **OVER (Cláusula de Ventana):** Cláusula que define la "ventana" o conjunto de filas sobre el cual se va a aplicar una función analítica, especificando particiones y orden.
*   **PARTITION BY:** Parte de la cláusula `OVER` que divide el conjunto de resultados de la consulta en particiones, y la función analítica se aplica de forma independiente a cada partición.
*   **ORDER BY (en Cláusula de Ventana):** Parte de la cláusula `OVER` que define el orden lógico de las filas dentro de cada partición o ventana.
*   **Cláusula de Ventana (frame_clause: ROWS, RANGE):** Subcláusula de `OVER` que define el subconjunto específico de filas dentro de la partición sobre las que se realizará el cálculo (ej. `ROWS BETWEEN N PRECEDING AND CURRENT ROW`).
*   **ROW_NUMBER():** Función analítica que asigna un número secuencial único a cada fila dentro de su partición, comenzando desde 1.
*   **RANK():** Función analítica que asigna un rango a cada fila dentro de su partición. Si hay valores iguales, se les asigna el mismo rango y se saltan los siguientes números de rango.
*   **DENSE_RANK():** Función analítica similar a `RANK()`, pero asigna rangos consecutivos sin saltar números en caso de valores iguales.
*   **LEAD():** Función analítica que permite acceder a datos de una fila posterior en el mismo conjunto de resultados (ventana), según el orden especificado.
*   **LAG():** Función analítica que permite acceder a datos de una fila anterior en el mismo conjunto de resultados (ventana), según el orden especificado.
*   **Expresiones de Tabla Comunes (CTEs):** Consultas con nombre temporales y auto-contenidas que pueden ser referenciadas dentro de una sentencia SQL principal (SELECT, INSERT, UPDATE, DELETE), mejorando la legibilidad y modularidad.
*   **WITH (Cláusula CTE):** La palabra clave que introduce una Expresión de Tabla Común en SQL.
*   **Consulta Recursiva (CTE):** Un tipo de CTE que se refiere a sí misma, utilizada para procesar datos jerárquicos o en gráficos (ej. árboles, redes).
*   **UNION ALL:** Operador de conjunto que combina los conjuntos de resultados de dos o más sentencias `SELECT`, incluyendo todas las filas resultantes, incluso los duplicados.
*   **INTERSECT (SQL):** Operador de conjunto que devuelve solo las filas que son comunes a los conjuntos de resultados de dos sentencias `SELECT`.
*   **EXCEPT (SQL) / MINUS (Oracle):** Operador de conjunto que devuelve las filas que están en el primer conjunto de resultados de `SELECT` pero no en el segundo.
*   **CASE Expression (SQL):** Una construcción SQL que permite definir lógica condicional (IF-THEN-ELSE) directamente dentro de una sentencia `SELECT`, `WHERE`, `ORDER BY`, etc.
*   **Unbounded Preceding:** En la cláusula de ventana, indica que la ventana comienza desde la primera fila de la partición.
*   **Current Row (frame_clause):** En la cláusula de ventana, indica que la ventana incluye la fila actual.
*   **N Preceding/Following:** En la cláusula de ventana, indica que la ventana incluye las `N` filas anteriores o posteriores a la fila actual.
