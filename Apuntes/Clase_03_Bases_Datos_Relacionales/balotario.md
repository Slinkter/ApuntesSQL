# Balotario - Clase 03: Bases de Datos Relacionales

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿En qué concepto matemático se basa el modelo relacional de datos?**
a) En la teoría de grafos.
b) En el cálculo lambda.
c) En el concepto de relación, que forma parte de la teoría de conjuntos.
d) En la geometría euclidiana.

**Respuesta Correcta:** c)
**Justificación:** El modelo relacional, propuesto por E.F. Codd, se fundamenta en la rama de las matemáticas discretas de la teoría de conjuntos, donde una "relación" es un conjunto de tuplas (filas).
**Por qué las otras son incorrectas:**
*   a) La teoría de grafos es la base de las bases de datos de grafos, no de las relacionales.
*   b, d) Son ramas de las matemáticas no relacionadas directamente con el modelo relacional.

---

**2. En el modelo relacional, ¿cuál es el término formal para una "fila" o "registro"?**
a) Atributo
b) Tupla
c) Relación
d) Dominio

**Respuesta Correcta:** b)
**Justificación:** Una tupla es el término matemático que representa una instancia única en una relación, es decir, una fila en una tabla.
**Por qué las otras son incorrectas:**
*   a) Un atributo es una columna o campo.
*   c) Una relación es la tabla completa.
*   d) Un dominio es el conjunto de valores permitidos para una columna.

---

**3. ¿Qué describe el "Grado" de una relación?**
a) El número de filas (tuplas).
b) El número de columnas (atributos).
c) El número de claves foráneas.
d) El número de tablas en la base de datos.

**Respuesta Correcta:** b)
**Justificación:** El grado de una relación se define por el número de sus atributos o columnas.
**Por qué las otras son incorrectas:**
*   a) El número de filas se llama cardinalidad.
*   c, d) Son métricas de la base de datos, pero no definen el grado de una relación individual.

---

**4. ¿Cuál de las siguientes afirmaciones sobre una Clave Primaria (PK) es CIERTA?**
a) Puede contener valores nulos.
b) Puede tener valores duplicados.
c) Se utiliza para identificar de forma única cada tupla en una tabla.
d) Una tabla puede tener varias claves primarias.

**Respuesta Correcta:** c)
**Justificación:** La función principal y definitoria de una clave primaria es garantizar la unicidad de cada registro dentro de una tabla.
**Por qué las otras son incorrectas:**
*   a, b) Una clave primaria, por definición, no puede ser nula y debe ser única.
*   d) Una tabla solo puede tener una clave primaria (aunque esta puede estar compuesta por varias columnas).

---

**5. ¿Qué establece una Clave Foránea (FK)?**
a) Una restricción que obliga a que una columna solo acepte números.
b) Una relación entre dos tablas, manteniendo la integridad referencial.
c) Un identificador único para una fila dentro de la misma tabla.
d) Un índice para acelerar las consultas.

**Respuesta Correcta:** b)
**Justificación:** Una clave foránea en una tabla "hija" apunta a la clave primaria de una tabla "padre", creando así un enlace lógico entre ellas y asegurando que los datos relacionados sean consistentes.
**Por qué las otras son incorrectas:**
*   a) Eso es una restricción de tipo de dato o `CHECK`.
*   c) Eso es una clave primaria.
*   d) Aunque las claves foráneas a menudo se indexan, su propósito fundamental es relacional, no de rendimiento.

---

**6. Si se elimina un registro en una tabla "padre" y esto provoca la eliminación automática de los registros relacionados en la tabla "hija", ¿qué acción en cascada se ha definido?**
a) `ON DELETE RESTRICT`
b) `ON DELETE SET NULL`
c) `ON DELETE CASCADE`
d) `ON DELETE NO ACTION`

**Respuesta Correcta:** c)
**Justificación:** La acción `CASCADE` propaga la operación de eliminación (o actualización) desde la tabla padre a todas las filas dependientes en la tabla hija.
**Por qué las otras son incorrectas:**
*   a, d) `RESTRICT` o `NO ACTION` impedirían la eliminación en la tabla padre si existen registros hijos.
*   b) `SET NULL` establecería el valor de la clave foránea en la tabla hija como `NULL`, pero no eliminaría la fila.

---

**7. En álgebra relacional, ¿qué operación se utiliza para filtrar filas de una tabla basándose en una condición?**
a) Proyección (π)
b) Join (⋈)
c) Selección (σ)
d) Producto Cartesiano (×)

**Respuesta Correcta:** c)
**Justificación:** La operación de Selección (sigma) corresponde a la cláusula `WHERE` en SQL y se utiliza para seleccionar un subconjunto de tuplas (filas) que cumplen una condición.
**Por qué las otras son incorrectas:**
*   a) La Proyección selecciona columnas.
*   b) El Join combina tablas.
*   d) El Producto Cartesiano genera todas las combinaciones de filas entre dos tablas.

---

**8. ¿Qué es una "Clave Candidata"?**
a) Cualquier columna que no sea la clave primaria.
b) Una superclave mínima; un atributo o conjunto de atributos que identifica de forma única una tupla y no tiene subconjuntos redundantes.
c) Una clave foránea que podría convertirse en clave primaria.
d) Una columna que contiene datos de texto.

**Respuesta Correcta:** b)
**Justificación:** Una tabla puede tener varios identificadores únicos. Cada uno de estos es una clave candidata. La clave primaria es simplemente una de las claves candidatas que el diseñador elige como el identificador principal.
**Por qué las otras son incorrectas:**
*   a, c, d) No se ajustan a la definición de una clave candidata.

---

**9. La "Cardinalidad" de una relación se refiere a:**
a) El número de columnas.
b) El número de filas.
c) La cantidad de memoria que utiliza la tabla.
d) El tipo de datos de la clave primaria.

**Respuesta Correcta:** b)
**Justificación:** La cardinalidad es el término técnico que se utiliza para referirse al número de tuplas o filas en una relación en un momento dado.
**Por qué las otras son incorrectas:**
*   a) El número de columnas es el grado.
*   c, d) Son propiedades de la implementación física o del diseño, no la definición de cardinalidad.

---

**10. ¿Qué garantiza la "Integridad Referencial"?**
a) Que todas las columnas de texto estén en mayúsculas.
b) Que cada valor de una clave foránea exista como valor en la clave primaria de la tabla referenciada.
c) Que no se puedan insertar filas duplicadas.
d) Que las consultas se ejecuten rápidamente.

**Respuesta Correcta:** b)
**Justificación:** Esta es la esencia de la integridad referencial. Asegura que no haya "punteros rotos" o referencias a registros que no existen, manteniendo la consistencia entre las tablas relacionadas.
**Por qué las otras son incorrectas:**
*   a) Es una regla de formato, no de integridad referencial.
*   c) Es garantizado por las restricciones `PRIMARY KEY` o `UNIQUE`, no por la integridad referencial.
*   d) Se relaciona con el rendimiento, no con la integridad.

---

**11. La operación de Proyección (π) en álgebra relacional es análoga a qué cláusula de SQL?**
a) `SELECT [lista_de_columnas]`
b) `WHERE [condicion]`
c) `GROUP BY [columna]`
d) `ORDER BY [columna]`

**Respuesta Correcta:** a)
**Justificación:** La Proyección se utiliza para seleccionar un subconjunto de atributos (columnas) de una relación, que es exactamente lo que hace la lista de columnas en una sentencia `SELECT`.
**Por qué las otras son incorrectas:**
*   b) `WHERE` corresponde a la Selección (σ).
*   c, d) No tienen un operador directo equivalente en el álgebra relacional clásica.

---

**12. ¿Qué es una "Superclave"?**
a) Una clave primaria compuesta por más de tres columnas.
b) Cualquier atributo o conjunto de atributos que identifica de forma única una fila.
c) El nombre de la base de datos.
d) Una clave foránea que referencia a la misma tabla.

**Respuesta Correcta:** b)
**Justificación:** Una superclave es cualquier conjunto de atributos que garantiza la unicidad. Una clave candidata es una superclave "mínima" (sin atributos redundantes). Por ejemplo, `{ID}` y `{ID, Nombre}` podrían ser ambas superclaves, pero solo `{ID}` sería una clave candidata.
**Por qué las otras son incorrectas:**
*   a, c, d) Son definiciones incorrectas.

---

**13. Si la tabla A tiene 5 filas y la tabla B tiene 3 filas, ¿cuántas filas tendrá el resultado del Producto Cartesiano (A × B)?**
a) 5
b) 3
c) 8
d) 15

**Respuesta Correcta:** d)
**Justificación:** El producto cartesiano combina cada fila de la primera tabla con cada fila de la segunda, por lo que el número total de filas es el producto de las filas de cada tabla (5 * 3 = 15).
**Por qué las otras son incorrectas:**
*   a, b, c) Son cálculos incorrectos.

---

**14. ¿Puede una Clave Foránea (FK) contener valores `NULL`?**
a) No, nunca.
b) Sí, si la relación que representa es opcional.
c) Sí, pero solo si la clave primaria a la que hace referencia también es nula.
d) Solo en bases de datos no relacionales.

**Respuesta Correcta:** b)
**Justificación:** Si un registro en la tabla hija no necesita estar obligatoriamente relacionado con un registro en la tabla padre (relación opcional), la columna de la clave foránea puede permitirse ser `NULL`.
**Por qué las otras son incorrectas:**
*   a) Es incorrecto, los `NULL` son permitidos en FKs.
*   c) Una clave primaria nunca puede ser nula.
*   d) Las claves foráneas son un concepto del modelo relacional.

---

**15. El término "Relación" en el modelo relacional es un sinónimo de:**
a) Tabla
b) Columna
c) Clave
d) Consulta

**Respuesta Correcta:** a)
**Justificación:** En la terminología formal del modelo relacional, una "relación" es el término matemático para lo que comúnmente llamamos una "tabla".
**Por qué las otras son incorrectas:**
*   b, c, d) Son otros conceptos del modelo.

---

**16. ¿Qué define el "Dominio" de un atributo?**
a) El nombre del atributo.
b) Si el atributo es una clave primaria o no.
c) El conjunto de valores permitidos para ese atributo.
d) La tabla a la que pertenece el atributo.

**Respuesta Correcta:** c)
**Justificación:** El dominio especifica el tipo de dato (ej. `INTEGER`, `VARCHAR(50)`) y, opcionalmente, restricciones adicionales (ej. > 0) que definen qué valores son válidos para una columna.
**Por qué las otras son incorrectas:**
*   a, b, d) Son otras propiedades de un atributo, pero no su dominio.

---

**17. La operación de `JOIN` (⋈) en álgebra relacional se puede definir como:**
a) Una Selección seguida de una Proyección.
b) Un Producto Cartesiano seguido de una Selección.
c) Una Unión seguida de una Diferencia.
d) Una Proyección sobre un Producto Cartesiano.

**Respuesta Correcta:** b)
**Justificación:** Conceptualmente, un `JOIN` entre dos tablas es equivalente a realizar primero un producto cartesiano de ambas y luego aplicar una operación de selección para filtrar solo las filas donde las columnas de unión coinciden.
**Por qué las otras son incorrectas:**
*   a, c, d) No describen la operación de `JOIN`.

---

**18. En una relación de Empleados, el conjunto `{ID_Empleado, DNI}` es una superclave. Si tanto `ID_Empleado` como `DNI` son únicos por sí solos, ¿cuál de las siguientes afirmaciones es correcta?**
a) `{ID_Empleado, DNI}` es una clave candidata.
b) Solo `{ID_Empleado}` puede ser una clave candidata.
c) Tanto `{ID_Empleado}` como `{DNI}` son claves candidatas.
d) No hay claves candidatas.

**Respuesta Correcta:** c)
**Justificación:** Una clave candidata es una superclave mínima. Dado que tanto `{ID_Empleado}` como `{DNI}` pueden identificar de forma única una fila por sí solos, ambos son identificadores únicos mínimos y, por lo tanto, ambos son claves candidatas. `{ID_Empleado, DNI}` es una superclave, pero no una clave candidata porque es redundante.
**Por qué las otras son incorrectas:**
*   a) Es incorrecta porque no es mínima.
*   b) Es incorrecta porque `{DNI}` también es una clave candidata.
*   d) Es incorrecta porque existen dos claves candidatas.

---

**19. El operador de álgebra relacional que corresponde a la cláusula `UNION` en SQL es:**
a) Intersección (∩)
b) Diferencia (-)
c) Unión (∪)
d) Proyección (π)

**Respuesta Correcta:** c)
**Justificación:** El operador de Unión (∪) en álgebra relacional combina dos relaciones (tablas) con esquemas compatibles en una sola, eliminando duplicados, que es la función principal de `UNION` en SQL.
**Por qué las otras son incorrectas:**
*   a, b, d) Corresponden a otras operaciones.

---

**20. Si borras una tabla (con `DROP TABLE`), ¿qué sucede con la integridad referencial?**
a) Nada, las claves foráneas en otras tablas que apuntaban a ella seguirán funcionando.
b) El SGBD mostrará un error y no permitirá borrar la tabla si es referenciada por claves foráneas.
c) Las claves foráneas en otras tablas se convertirán automáticamente a `NULL`.
d) Se borra la tabla, pero se mantiene una copia de seguridad automática.

**Respuesta Correcta:** b)
**Justificación:** La integridad referencial protege las relaciones. La mayoría de los SGBD, por defecto, impedirán que se elimine una tabla si existen claves foráneas en otras tablas que dependen de ella, para evitar dejar "referencias huérfanas".
**Por qué las otras son incorrectas:**
*   a) Esto es falso y violaría la integridad referencial.
*   c) El SGBD no modifica automáticamente otras tablas al hacer un `DROP`; simplemente previene la operación.
*   d) `DROP TABLE` es una operación DDL destructiva y no crea una copia de seguridad.
