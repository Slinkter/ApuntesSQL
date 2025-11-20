# Balotario - Clase 02: Sistema de Gestión de Base de Datos (SGBD)

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿Cuál es la definición más precisa de un SGBD (Sistema de Gestión de Base de Datos)?**
a) Un tipo de base de datos que solo almacena números.
b) Un lenguaje de programación como Java o Python.
c) Un software que actúa como interfaz entre el usuario y los datos, permitiendo definir, crear y controlar la base de datos.
d) Un componente de hardware para almacenar grandes volúmenes de datos.

**Respuesta Correcta:** c)
**Justificación:** Un SGBD es fundamentalmente una capa de software que abstrae la complejidad del almacenamiento físico y proporciona herramientas para gestionar los datos de manera eficiente y segura.
**Por qué las otras son incorrectas:**
*   a) Los SGBD pueden gestionar todo tipo de datos, no solo números.
*   b) Es un tipo de software, pero no un lenguaje de programación de propósito general. Interactúa con lenguajes como SQL.
*   d) El hardware (discos duros, SSD) almacena los datos, pero el SGBD es el software que los gestiona.

---

**2. ¿A qué categoría de lenguaje de base de datos pertenece el comando `CREATE TABLE`?**
a) DML (Data Manipulation Language)
b) DDL (Data Definition Language)
c) DCL (Data Control Language)
d) TCL (Transaction Control Language)

**Respuesta Correcta:** b)
**Justificación:** DDL se utiliza para definir la estructura y el esquema de la base de datos. `CREATE TABLE` es un comando que define una nueva tabla, por lo que pertenece a esta categoría.
**Por qué las otras son incorrectas:**
*   a) DML (ej. `SELECT`, `INSERT`) se usa para manipular los datos dentro de las tablas.
*   c) DCL (ej. `GRANT`, `REVOKE`) se usa para gestionar permisos de usuario.
*   d) TCL (ej. `COMMIT`, `ROLLBACK`) se usa para gestionar transacciones.

---

**3. La capacidad de un SGBD para permitir que múltiples usuarios accedan y modifiquen datos simultáneamente sin causar inconsistencias se llama:**
a) Control de Concurrencia
b) Integridad de Datos
c) Recuperación y Respaldo
d) Independencia de Datos

**Respuesta Correcta:** a)
**Justificación:** El control de concurrencia es la función específica del SGBD que gestiona las interacciones simultáneas de los usuarios para prevenir conflictos y mantener la consistencia de los datos.
**Por qué las otras son incorrectas:**
*   b) La integridad se refiere a la corrección y validez de los datos, que es protegida por el control de concurrencia, pero no es el mecanismo en sí.
*   c) Se refiere a la protección contra fallos del sistema.
*   d) Se refiere a la separación entre la lógica y el almacenamiento físico.

---

**4. ¿Qué ventaja de usar un SGBD se refiere a la separación entre la definición lógica de los datos y su almacenamiento físico?**
a) Reducción de Redundancia
b) Seguridad de Datos
c) Independencia de Datos
d) Compartición de Datos

**Respuesta Correcta:** c)
**Justificación:** La independencia de datos permite que la forma en que se almacenan los datos físicamente (ej. en qué archivos o discos) pueda cambiar sin que las aplicaciones que acceden a ellos necesiten ser modificadas.
**Por qué las otras son incorrectas:**
*   a) Se logra mediante la normalización y un diseño centralizado.
*   b) Se logra mediante mecanismos de autenticación y autorización.
*   d) Es una consecuencia de tener un sistema centralizado, pero no define la independencia de datos.

---

**5. El comando `INSERT INTO usuarios VALUES ('Juan', 25)` es un ejemplo de:**
a) DDL
b) DCL
c) DML
d) TCL

**Respuesta Correcta:** c)
**Justificación:** DML (Data Manipulation Language) se utiliza para manipular los datos existentes en las tablas. `INSERT` es un comando DML que añade nuevas filas de datos.
**Por qué las otras son incorrectas:**
*   a) DDL define la estructura, no los datos.
*   b) DCL gestiona permisos.
*   d) TCL gestiona la transacción en su conjunto.

---

**6. ¿Qué componente de un SGBD es responsable de asegurar las propiedades ACID de las transacciones?**
a) El Procesador de Consultas
b) El Gestor de Transacciones
c) El Motor de Base de Datos
d) El Catálogo del Sistema

**Respuesta Correcta:** b)
**Justificación:** El Gestor de Transacciones es el componente específicamente diseñado para garantizar la Atomicidad, Consistencia, Aislamiento y Durabilidad (ACID) de cada transacción.
**Por qué las otras son incorrectas:**
*   a) El Procesador de Consultas se encarga de interpretar y optimizar las sentencias SQL.
*   c) El Motor de Base de Datos se encarga de la escritura y lectura física.
*   d) El Catálogo del Sistema almacena metadatos.

---

**7. El "Catálogo del Sistema" de un SGBD contiene:**
a) Una copia de todos los datos de la base de datos.
b) Información sobre la estructura de la base de datos (metadatos).
c) El código fuente del SGBD.
d) Un registro de todas las transacciones de los usuarios.

**Respuesta Correcta:** b)
**Justificación:** El Catálogo del Sistema, o diccionario de datos, almacena "datos sobre los datos" (metadatos), como nombres de tablas, columnas, tipos de datos, índices, restricciones y permisos.
**Por qué las otras son incorrectas:**
*   a) Sería una copia de seguridad, no el catálogo.
*   c) El código fuente no es accesible a los usuarios.
*   d) Esto se almacena en los logs de transacciones, no en el catálogo.

---

**8. ¿Cuál de las siguientes NO es una de las propiedades ACID?**
a) Atomicidad
b) Consistencia
c) Integridad
d) Aislamiento

**Respuesta Correcta:** c)
**Justificación:** Las propiedades ACID son Atomicidad, Consistencia, Aislamiento (Isolation) y Durabilidad. La integridad es un concepto más general de la base de datos que es mantenido, en parte, por las propiedades ACID, pero no es una de ellas.
**Por qué las otras son incorrectas:**
*   a, b, d) Son tres de las cuatro propiedades ACID.

---

**9. La función de "Recuperación y Respaldo" de un SGBD sirve principalmente para:**
a) Prevenir el acceso no autorizado a los datos.
b) Permitir el acceso simultáneo de múltiples usuarios.
c) Restaurar la base de datos a un estado consistente después de un fallo.
d) Definir nuevas tablas y columnas en la base de datos.

**Respuesta Correcta:** c)
**Justificación:** Esta función es crucial para la tolerancia a fallos. Permite que, en caso de un error de hardware, software o humano, la base de datos pueda ser restaurada a un punto en el tiempo anterior al fallo.
**Por qué las otras son incorrectas:**
*   a) Eso es control de acceso y seguridad.
*   b) Eso es control de concurrencia.
*   d) Eso es definición de datos (DDL).

---

**10. ¿Cuál es una ventaja clave de la "Reducción de Redundancia" que ofrece un SGBD?**
a) Reduce la necesidad de hardware potente.
b) Ayuda a prevenir inconsistencias en los datos.
c) Acelera todas las consultas de la base de datos.
d) Reduce el número de usuarios que pueden acceder a los datos.

**Respuesta Correcta:** b)
**Justificación:** Si el mismo dato (ej. la dirección de un cliente) se almacena en un solo lugar, al actualizarlo, se evita el riesgo de que existan versiones diferentes y conflictivas de ese dato en la base de datos (inconsistencia).
**Por qué las otras son incorrectas:**
*   a) Aunque reduce el espacio de almacenamiento, no necesariamente reduce la necesidad de hardware potente para el procesamiento.
*   c) No todas las consultas se aceleran; de hecho, las consultas que requieren unir muchas tablas normalizadas pueden ser más lentas.
*   d) No tiene relación con el número de usuarios.

---

**11. El comando `GRANT SELECT ON empleados TO juan;` pertenece al:**
a) DDL
b) DML
c) DCL
d) TCL

**Respuesta Correcta:** c)
**Justificación:** DCL (Data Control Language) se utiliza para controlar los permisos y el acceso a los datos. `GRANT` es el comando principal para otorgar privilegios.
**Por qué las otras son incorrectas:**
*   a) DDL define la estructura.
*   b) DML manipula los datos.
*   d) TCL gestiona transacciones.

---

**12. El "Motor de Base de Datos" es:**
a) Una herramienta gráfica para escribir consultas.
b) Un lenguaje para definir la estructura de las tablas.
c) El componente central del SGBD que almacena y recupera los datos.
d) Un conjunto de reglas para garantizar la integridad referencial.

**Respuesta Correcta:** c)
**Justificación:** El motor es el núcleo del SGBD, el software que realiza las operaciones de bajo nivel de lectura y escritura en los archivos físicos de la base de datos.
**Por qué las otras son incorrectas:**
*   a) Es una utilidad o herramienta de cliente.
*   b) Es el DDL.
*   d) Son las restricciones de integridad, gestionadas por el SGBD.

---

**13. ¿Por qué un SGBD ayuda a reducir el tiempo de desarrollo de aplicaciones?**
a) Escribe el código de la aplicación automáticamente.
b) Proporciona funciones integradas para tareas complejas como respaldo, seguridad y concurrencia.
c) Ofrece plantillas de diseño de interfaz de usuario.
d) Incluye un compilador para lenguajes de propósito general.

**Respuesta Correcta:** b)
**Justificación:** Al utilizar un SGBD, los desarrolladores no necesitan programar desde cero la lógica para manejar el acceso concurrente, la recuperación de fallos o la seguridad de los datos, ya que el SGBD se encarga de estas tareas complejas.
**Por qué las otras son incorrectas:**
*   a, c, d) Un SGBD no realiza estas funciones.

---

**14. La propiedad de "Atomicidad" en ACID garantiza que:**
a) Cada transacción se ejecuta de forma aislada de las demás.
b) Una transacción se completa en su totalidad o no se realiza en absoluto.
c) Los resultados de una transacción exitosa se almacenan permanentemente.
d) La base de datos se mantiene en un estado consistente.

**Respuesta Correcta:** b)
**Justificación:** La atomicidad asegura que las transacciones son indivisibles. Si cualquier parte de la transacción falla, toda la transacción se deshace (`ROLLBACK`), asegurando que la base de datos no quede en un estado intermedio e inconsistente.
**Por qué las otras son incorrectas:**
*   a) Es la propiedad de Aislamiento (Isolation).
*   c) Es la propiedad de Durabilidad (Durability).
*   d) Es la propiedad de Consistencia (Consistency).

---

**15. Un "Procesador de Consultas" tiene como una de sus funciones principales:**
a) Crear copias de seguridad de la base de datos.
b) Otorgar permisos a los usuarios.
c) Interpretar y optimizar las sentencias SQL para una ejecución eficiente.
d) Almacenar los datos en el disco duro.

**Respuesta Correcta:** c)
**Justificación:** El procesador de consultas analiza una sentencia SQL, determina el plan de ejecución más eficiente (ej. qué índices usar, en qué orden unir las tablas) y luego lo pasa al motor de la base de datos para su ejecución.
**Por qué las otras son incorrectas:**
*   a) Es una utilidad de respaldo.
*   b) Es una función del DCL.
*   d) Es una función del motor de la base de datos.

---

**16. ¿Cuál de las siguientes opciones es una desventaja potencial de usar un SGBD?**
a) Mayor seguridad de los datos.
b) Complejidad y costo inicial de adquisición e implementación.
c) Mayor consistencia de los datos.
d) Mejor compartición de datos.

**Respuesta Correcta:** b)
**Justificación:** Los SGBD, especialmente los de nivel empresarial, pueden ser costosos de licenciar e implementar. Requieren personal capacitado (DBAs) y una configuración inicial compleja en comparación con un sistema simple de archivos.
**Por qué las otras son incorrectas:**
*   a, c, d) Son ventajas clave de usar un SGBD.

---

**17. El comando `ROLLBACK;` pertenece al:**
a) DML
b) DDL
c) DCL
d) TCL

**Respuesta Correcta:** d)
**Justificación:** TCL (Transaction Control Language) se utiliza para gestionar el ciclo de vida de una transacción. `ROLLBACK` es el comando que deshace los cambios realizados en la transacción actual.
**Por qué las otras son incorrectas:**
*   a) DML manipula los datos.
*   b) DDL define la estructura.
*   c) DCL gestiona permisos.

---

**18. La función de "Integridad de Datos" en un SGBD se implementa principalmente mediante:**
a) La creación de muchos índices.
b) El uso de hardware rápido.
c) La aplicación de reglas y restricciones (constraints).
d) La encriptación de toda la base de datos.

**Respuesta Correcta:** c)
**Justificación:** La integridad se mantiene definiendo restricciones como `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL` y `CHECK`, que el SGBD se encarga de hacer cumplir automáticamente.
**Por qué las otras son incorrectas:**
*   a, b) Mejoran el rendimiento, no la integridad.
*   d) Mejora la seguridad, no la integridad (corrección) de los datos.

---

**19. ¿Qué son los metadatos en el contexto de un SGBD?**
a) Datos que rara vez se utilizan.
b) Datos sobre los usuarios del sistema.
c) Datos sobre los datos, como la estructura de las tablas y los tipos de datos.
d) Datos que han sido archivados.

**Respuesta Correcta:** c)
**Justificación:** Los metadatos describen la estructura, las restricciones y otras características de los datos de la base de datos. Se almacenan en el catálogo del sistema.
**Por qué las otras son incorrectas:**
*   a, d) Describen el estado o uso de los datos, no qué son los metadatos.
*   b) La información sobre los usuarios es una parte de los metadatos, pero no su definición completa.

---

**20. Si eliminas una fila de una tabla usando `DELETE` y luego apagas la base de datos sin hacer `COMMIT` o `ROLLBACK`, ¿qué sucederá al reiniciar?**
a) La fila se eliminará permanentemente.
b) La eliminación se deshará automáticamente.
c) La tabla quedará corrupta.
d) El SGBD preguntará al usuario qué hacer.

**Respuesta Correcta:** b)
**Justificación:** Gracias a las propiedades ACID, una transacción no confirmada no es duradera. El SGBD utiliza sus logs de transacciones para realizar una recuperación de instancia al arrancar, y cualquier transacción incompleta (no confirmada) se deshará (`ROLLBACK`) para garantizar un estado consistente.
**Por qué las otras son incorrectas:**
*   a) La eliminación no fue confirmada, por lo que no es permanente.
*   c) El SGBD está diseñado para evitar la corrupción en estos casos.
*   d) El proceso de recuperación es automático, no interactivo.
