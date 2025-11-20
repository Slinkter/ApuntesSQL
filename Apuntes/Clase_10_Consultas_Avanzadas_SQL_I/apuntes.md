# 🔗 Clase 10: JOIN, Subconsultas y Agrupamiento (SQL Avanzado)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **JOIN (Unión)** | Un `JOIN` se usa para consultar datos que están en **más de una tabla**. Enlazamos filas usando valores comunes, generalmente entre la PK y la FK. |
| **Cross Join (Producto Cartesiano)** | ¡El **JOIN que no quieres**! Sucede si olvidas la condición de unión. Junta *cada* fila de la primera tabla con *cada* fila de la segunda. ¡El resultado es enorme y sin sentido!. |
| **Tipos de JOIN** | **Equijoin:** El más común; une tablas cuando las columnas son **iguales** (`=`). **Non-Equijoin:** Usa otros operadores (como `BETWEEN` o `>`). **Self Join:** Una tabla se une **consigo misma** (usando alias), útil para relaciones recursivas (Ej. Empleado y Jefe). |
| **Outer Join (LEFT/RIGHT)** | Se utiliza para ver las filas que **normalmente no se mostrarían**. Por ejemplo, un `LEFT OUTER JOIN` muestra todos los clientes, *incluso* si no tienen pedidos relacionados. |
| **Subconsultas** | Es una consulta **anidada** que se ejecuta *primero*. El resultado de la subconsulta (interna) alimenta a la consulta principal (externa). ¡Son perfectas cuando la condición de tu `WHERE` se basa en un valor que no conoces de antemano!. |
| **Funciones de Agrupamiento** | Son funciones que operan sobre conjuntos de filas: `MIN`, `MAX`, `AVG` (promedio), `SUM` y `COUNT`. |
| **GROUP BY y HAVING** | **GROUP BY** divide las filas en subconjuntos y aplica las funciones de agrupamiento a cada uno (Ej. agrupar por `tipo` de cliente y contar cuántos hay). **HAVING** es como el `WHERE`, pero se usa para **filtrar los grupos** (Ej. "Muéstrame solo los grupos donde el conteo sea mayor a 5"). |

**Resumen de la Clase 10:** El `SELECT` avanzado se basa en el `JOIN` para combinar datos de múltiples tablas (evitando el *Cross Join*). Las Subconsultas permiten consultas dinámicas, y el uso de `GROUP BY` y `HAVING` nos da el poder de analizar y filtrar los datos en conjuntos (agrupamiento).

---