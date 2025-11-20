# ✍️ Clase 04: DML y Consultas Básicas

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Lenguajes de BDR** | Vimos DDL (estructura), DCL (seguridad) y ahora el **DML (Manipulación de Datos)**, que es para interactuar con el contenido de las tablas (filas). |
| **INSERT (Añadir Fila)** | El comando `INSERT` añade una nueva fila (registro) a tu tabla. Recuerda que si un campo tiene la restricción `NOT NULL`, ¡debes ingresarle un valor obligatoriamente!. |
| **UPDATE (Modificar Dato)** | `UPDATE` es para cambiar el valor de un campo existente. Es crucial usar la cláusula **WHERE** para especificar exactamente qué fila(s) quieres modificar. Si olvidas el `WHERE`, ¡podrías actualizar todas las filas de la tabla!. |
| **DELETE (Eliminar Fila)** | `DELETE` elimina una o más filas. ¡Regla de oro!: siempre usa **WHERE** para apuntar a la fila o grupo de filas correcto, o podrías vaciar tu tabla por accidente. |
| **SELECT (Consultar)** | El comando más usado. `SELECT` te permite ver la data. Puedes usar `*` o `ALL` para ver todas las columnas, o `DISTINCT` si solo quieres ver los valores únicos y evitar duplicados. |
| **Filtrado con WHERE** | Usas `WHERE` en el `SELECT` (y también en `UPDATE` y `DELETE`) para poner condiciones y filtrar solo las filas que cumplen ese criterio. Puedes usar conectores lógicos como `AND`, `OR`, y `NOT` para hacer filtros complejos. |

**Resumen de la Clase 04:** El DML nos da control sobre el contenido de las tablas. Aprendimos los comandos esenciales para la vida de los datos: `INSERT` (crear), `UPDATE` (modificar) y `DELETE` (borrar). Y por supuesto, `SELECT` es el rey para la recuperación y consulta de datos, utilizando `WHERE` para filtrar qué queremos ver.

---