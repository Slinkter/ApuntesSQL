# Balotario - Clase 05: DML y Consultas Simples

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿Cuál de las siguientes sentencias NO es un comando DML (Data Manipulation Language)?**
a) `SELECT`
b) `INSERT`
c) `UPDATE`
d) `CREATE`

**Respuesta Correcta:** d)
**Justificación:** `CREATE` es un comando DDL (Data Definition Language), ya que se utiliza para definir la estructura de los objetos de la base de datos (como crear una tabla), no para manipular los datos dentro de ellos.
**Por qué las otras son incorrectas:**
*   a, b, c) `SELECT`, `INSERT` y `UPDATE` son los comandos DML fundamentales para consultar, añadir y modificar datos, respectivamente.

---

**2. ¿Qué hace la cláusula `DISTINCT` en una sentencia `SELECT`?**
a) Ordena los resultados en orden descendente.
b) Filtra las filas basándose en una condición.
c) Elimina las filas duplicadas del conjunto de resultados.
d) Selecciona solo la primera fila del resultado.

**Respuesta Correcta:** c)
**Justificación:** `SELECT DISTINCT columna` devuelve solo los valores únicos de esa columna, eliminando cualquier duplicado que pudiera existir.
**Por qué las otras son incorrectas:**
*   a) Para ordenar se usa `ORDER BY ... DESC`.
*   b) Para filtrar filas se usa `WHERE`.
*   d) Para limitar filas se usan otras cláusulas como `ROWNUM` (Oracle) o `LIMIT` (MySQL), no `DISTINCT`.

---

**3. ¿Cuál es el propósito de la cláusula `WHERE`?**
a) Especificar las columnas que se desean mostrar.
b) Indicar la tabla de la cual se extraen los datos.
c) Filtrar las filas que cumplen una condición específica.
d) Ordenar el conjunto de resultados.

**Respuesta Correcta:** c)
**Justificación:** La cláusula `WHERE` es el principal mecanismo de filtrado en SQL, permitiendo seleccionar solo los registros que cumplen con los criterios lógicos definidos.
**Por qué las otras son incorrectas:**
*   a) Eso lo hace la lista de columnas después de `SELECT`.
*   b) Eso lo hace la cláusula `FROM`.
*   d) Eso lo hace la cláusula `ORDER BY`.

---

**4. ¿Qué sucede si se ejecuta una sentencia `UPDATE` o `DELETE` sin una cláusula `WHERE`?**
a) La sentencia dará un error de sintaxis.
b) La operación se aplicará a la primera fila de la tabla.
c) La operación se aplicará a todas las filas de la tabla.
d) La base de datos pedirá confirmación antes de ejecutar.

**Respuesta Correcta:** c)
**Justificación:** La ausencia de una cláusula `WHERE` significa que no hay un filtro, por lo que la acción (modificar o borrar) se aplica a todos los registros de la tabla especificada. Es una de las causas más comunes de errores graves en la manipulación de datos.
**Por qué las otras son incorrectas:**
*   a) La sintaxis es válida, aunque peligrosa.
*   b) No hay una selección implícita de la primera fila.
*   d) La ejecución es inmediata, no hay una solicitud de confirmación por defecto.

---

**5. ¿Qué operador se utiliza para buscar un patrón de texto en una columna `VARCHAR`?**
a) `BETWEEN`
b) `IN`
c) `LIKE`
d) `IS NULL`

**Respuesta Correcta:** c)
**Justificación:** El operador `LIKE` se usa junto con caracteres comodín (`%` para cualquier secuencia de caracteres, `_` para un solo carácter) para realizar búsquedas de patrones en cadenas de texto.
**Por qué las otras son incorrectas:**
*   a) `BETWEEN` se usa para rangos numéricos o de fechas.
*   b) `IN` se usa para comparar con una lista de valores discretos.
*   d) `IS NULL` se usa para verificar la ausencia de valor.

---

**6. ¿Para qué se utiliza la sentencia `INSERT INTO ... SELECT ...`?**
a) Para insertar una única fila con valores seleccionados de otra tabla.
b) Para crear una nueva tabla basada en el resultado de una consulta `SELECT`.
c) Para copiar múltiples filas de una tabla a otra.
d) Para actualizar una tabla con valores de otra.

**Respuesta Correcta:** c)
**Justificación:** Esta sintaxis permite tomar el conjunto de resultados de una consulta `SELECT` (que pueden ser muchas filas) e insertarlo directamente en otra tabla, facilitando la copia masiva de datos entre tablas compatibles.
**Por qué las otras son incorrectas:**
*   a) Puede insertar una fila, pero su poder reside en insertar múltiples filas.
*   b) Para crear una tabla nueva se usa `CREATE TABLE ... AS SELECT ...`.
*   d) Para actualizar se usa la sentencia `UPDATE`.

---

**7. ¿Cómo se ordenan los resultados de una consulta `SELECT` en orden descendente por la columna "fecha"?**
a) `ORDER BY fecha`
b) `SORT BY fecha DESC`
c) `ORDER BY fecha DESC`
d) `GROUP BY fecha DESC`

**Respuesta Correcta:** c)
**Justificación:** La cláusula para ordenar es `ORDER BY`. La palabra clave `DESC` especifica que el orden debe ser descendente (de mayor a menor, o de más reciente a más antiguo).
**Por qué las otras son incorrectas:**
*   a) Esto ordenaría en orden ascendente (ASC), que es el valor por defecto.
*   b) `SORT BY` no es una cláusula SQL estándar.
*   d) `GROUP BY` se usa para agrupar, no para ordenar el resultado final (aunque `ORDER BY` se usa para ordenar los grupos).

---

**8. ¿Cuál de los siguientes operadores lógicos utilizarías para seleccionar filas que cumplan AMBAS condiciones A y B?**
a) `OR`
b) `NOT`
c) `AND`
d) `XOR`

**Respuesta Correcta:** c)
**Justificación:** El operador `AND` combina dos o más condiciones y devuelve verdadero solo si todas las condiciones son verdaderas.
**Por qué las otras son incorrectas:**
*   a) `OR` devuelve verdadero si al menos una de las condiciones es verdadera.
*   b) `NOT` niega una condición.
*   d) `XOR` no es un operador SQL estándar.

---

**9. ¿Qué comando se utiliza para añadir una nueva fila a una tabla?**
a) `ADD ROW`
b) `UPDATE`
c) `CREATE ROW`
d) `INSERT INTO`

**Respuesta Correcta:** d)
**Justificación:** `INSERT INTO` es la sentencia DML estándar para agregar nuevos registros a una tabla.
**Por qué las otras son incorrectas:**
*   a, c) No son comandos SQL válidos.
*   b) `UPDATE` se usa para modificar registros existentes, no para crear nuevos.

---

**10. La consulta `SELECT * FROM productos WHERE precio IS NULL;` devolverá:**
a) Productos con precio igual a cero.
b) Productos que nunca han tenido un precio asignado.
c) Un error, porque no se puede comparar con `NULL`.
d) Todos los productos de la tabla.

**Respuesta Correcta:** b)
**Justificación:** `NULL` en SQL representa la ausencia de un valor. `IS NULL` es el operador correcto para filtrar las filas donde una columna específica no tiene ningún valor registrado.
**Por qué las otras son incorrectas:**
*   a) Un precio de cero es un valor numérico definido, no es lo mismo que `NULL`.
*   c) No da error; `IS NULL` es la sintaxis correcta. Usar `= NULL` no funcionaría como se espera, pero `IS NULL` es válido.
*   d) Solo devolverá los productos que cumplan la condición.

---

**11. ¿Qué carácter comodín se usa con `LIKE` para representar cualquier secuencia de cero o más caracteres?**
a) `_` (guion bajo)
b) `*` (asterisco)
c) `%` (porcentaje)
d) `?` (signo de interrogación)

**Respuesta Correcta:** c)
**Justificación:** El signo de porcentaje (`%`) es el comodín estándar en SQL para representar cualquier cadena de caracteres (incluyendo una cadena vacía).
**Por qué las otras son incorrectas:**
*   a) `_` representa un único carácter.
*   b, d) No son caracteres comodín estándar para `LIKE` en SQL.

---

**12. ¿Cuál es la función de la cláusula `SET` en una sentencia `UPDATE`?**
a) Especificar qué tabla se va a actualizar.
b) Especificar las columnas que se van a modificar y sus nuevos valores.
c) Filtrar las filas que serán actualizadas.
d) Iniciar la transacción.

**Respuesta Correcta:** b)
**Justificación:** La sintaxis es `UPDATE tabla SET columna1 = valor1, columna2 = valor2 ...`. La cláusula `SET` es donde se define la asignación de los nuevos valores.
**Por qué las otras son incorrectas:**
*   a) El nombre de la tabla va justo después de `UPDATE`.
*   c) Para filtrar se usa `WHERE`.
*   d) La transacción se inicia implícitamente con la sentencia DML.

---

**13. Para seleccionar empleados cuyos salarios sean 3000, 5000 o 7000, ¿qué operador es más eficiente que múltiples `OR`?**
a) `LIKE`
b) `BETWEEN`
c) `IN`
d) `ANY`

**Respuesta Correcta:** c)
**Justificación:** `WHERE salario IN (3000, 5000, 7000)` es más conciso y a menudo más optimizado que `WHERE salario = 3000 OR salario = 5000 OR salario = 7000`.
**Por qué las otras son incorrectas:**
*   a) `LIKE` es para patrones de texto.
*   b) `BETWEEN` es para rangos continuos, no para una lista de valores discretos.
*   d) `ANY` se usa de forma diferente, en comparación con un subquery.

---

**14. ¿Qué sentencia DML se utiliza para eliminar un registro específico de una tabla?**
a) `DROP ROW`
b) `DELETE`
c) `TRUNCATE`
d) `REMOVE`

**Respuesta Correcta:** b)
**Justificación:** `DELETE FROM tabla WHERE condicion` es el comando DML estándar para eliminar filas específicas.
**Por qué las otras son incorrectas:**
*   a, d) No son comandos SQL válidos.
*   c) `TRUNCATE` es un comando DDL que elimina *todas* las filas de una tabla de forma masiva y no puede ser deshecho con `ROLLBACK`.

---

**15. ¿Qué representa el asterisco (`*`) en `SELECT * FROM clientes;`?**
a) Todos los clientes cuyo nombre empieza con "A".
b) Todas las columnas de la tabla `clientes`.
c) Un puntero nulo.
d) Un error de sintaxis.

**Respuesta Correcta:** b)
**Justificación:** El `*` es un atajo que significa "todas las columnas" de la(s) tabla(s) especificadas en la cláusula `FROM`.
**Por qué las otras son incorrectas:**
*   a, c, d) Son interpretaciones incorrectas del símbolo.

---

**16. ¿Cuál de las siguientes es una consulta DML válida?**
a) `ALTER TABLE usuarios ADD email VARCHAR(100);`
b) `SELECT nombre, apellido FROM usuarios;`
c) `GRANT SELECT ON usuarios TO public;`
d) `CREATE VIEW v_usuarios AS SELECT * FROM usuarios;`

**Respuesta Correcta:** b)
**Justificación:** `SELECT` es el comando DML por excelencia para la recuperación de datos.
**Por qué las otras son incorrectas:**
*   a, d) Son comandos DDL, ya que modifican o crean la estructura de la base de datos.
*   c) Es un comando DCL, ya que gestiona permisos.

---

**17. La cláusula `ORDER BY` se ejecuta...**
a) Antes de la cláusula `WHERE`.
b) Antes de la cláusula `FROM`.
c) Después de que `SELECT` y `WHERE` han filtrado las filas.
d) Solo si la consulta no tiene `WHERE`.

**Respuesta Correcta:** c)
**Justificación:** Lógicamente, el SGBD primero determina qué filas necesita (`FROM` y `WHERE`) y qué columnas mostrar (`SELECT`), y luego ordena ese conjunto de resultados final.
**Por qué las otras son incorrectas:**
*   a, b) La ordenación se aplica al resultado, no a la tabla original antes de filtrar.
*   d) `ORDER BY` se puede usar con o sin `WHERE`.

---

**18. Para encontrar todos los libros cuyo título contiene la palabra "SQL", ¿qué condición `WHERE` usarías?**
a) `WHERE titulo = '%SQL%'`
b) `WHERE titulo LIKE '_SQL_'`
c) `WHERE titulo CONTAINS 'SQL'`
d) `WHERE titulo LIKE '%SQL%'`

**Respuesta Correcta:** d)
**Justificación:** `%` es el comodín para cero o más caracteres. `%SQL%` significa "cualquier cosa (o nada), seguido de 'SQL', seguido de cualquier cosa (o nada)". Esto encontrará "SQL", "SQL Básico", "Manual de SQL", etc.
**Por qué las otras son incorrectas:**
*   a) El operador de igualdad (`=`) busca una coincidencia exacta con la cadena literal `'%SQL%'`.
*   b) `_` representa un solo carácter, por lo que esto buscaría títulos como "aSQLb", pero no "SQL Básico".
*   c) `CONTAINS` no es un operador SQL estándar para esta tarea.

---

**19. ¿Cuál es el valor por defecto para la ordenación en `ORDER BY` si no se especifica `ASC` o `DESC`?**
a) `DESC` (Descendente)
b) `ASC` (Ascendente)
c) No tiene valor por defecto, es obligatorio especificarlo.
d) El orden depende del SGBD y no es predecible.

**Respuesta Correcta:** b)
**Justificación:** El estándar SQL y la mayoría de las implementaciones de SGBD utilizan el orden ascendente (de la A a la Z, del 0 al 9) como el comportamiento por defecto para `ORDER BY`.
**Por qué las otras son incorrectas:**
*   a, c, d) Son afirmaciones incorrectas.

---

**20. Si quieres modificar el apellido de un solo empleado con un `id_empleado` de 101, ¿qué cláusula es indispensable?**
a) `ORDER BY`
b) `GROUP BY`
c) `WHERE`
d) `DISTINCT`

**Respuesta Correcta:** c)
**Justificación:** Para asegurar que la sentencia `UPDATE` modifique únicamente el registro del empleado 101, es crucial usar `WHERE id_empleado = 101`. Sin esta cláusula, se actualizarían todos los empleados de la tabla.
**Por qué las otras son incorrectas:**
*   a, b, d) Son cláusulas utilizadas en sentencias `SELECT` y no tienen sentido en este contexto de `UPDATE`.
