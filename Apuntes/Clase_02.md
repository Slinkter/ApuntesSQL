# 📐 Clase 02: Modelo Relacional

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Arquitectura de 3 Niveles** | La BD tiene tres "capas" de vista: **1. Interno** (la estructura física de almacenamiento, lo que el computador ve), **2. Conceptual** (la visión global de toda la BD para todos los usuarios, con sus interrelaciones y restricciones), y **3. Externo** (las vistas personalizadas que ve cada usuario o aplicación). |
| **Independencia de Datos** | Es la capacidad mágica de modificar un esquema (como cambiar la estructura física o **Independencia Física**) sin tener que modificar el nivel superior (como la visión lógica o **Independencia Lógica**). ¡Esto simplifica los cambios! |
| **Terminología Relacional** | En el modelo relacional, las cosas tienen nombres elegantes: una **Tabla** se llama **Relación**, una **Fila** se llama **Tupla**, y una **Columna** se llama **Atributo**. |
| **Restricciones: PK y FK** | Estas son las reglas de integridad: La **PK (Primary Key)** es la cédula de identidad de cada fila; debe ser única y ¡jamás nula!. La **FK (Foreign Key)** es el atributo que usamos para conectar una tabla con la PK de otra (la relación entre un pedido y el cliente que lo hizo). |
| **Funciones del DBMS (Superpoderes)** | El DBMS es multifuncional: maneja a los **usuarios** (permisos), la **performance** (velocidad), el **backup/recovery** (respaldo y restauración) y, muy importante, las **Transacciones**. |
| **Transacción y ACID** | Una transacción es una operación completa de lectura o escritura. Sus propiedades deben ser **ACID**: **A**tomicidad (todo se hace o nada se hace), **C**onsistencia (el estado de la BD es siempre válido), **I**solamiento (las transacciones no se interfieren) y **D**urabilidad (los cambios son permanentes). |

**Resumen de la Clase 02:** Esta clase detalló la arquitectura de la BD (Interna, Conceptual, Externa) y el concepto de Independencia de Datos. Revisamos la terminología clave del Modelo Relacional (Tuplas, Relaciones, Atributos) y las restricciones cruciales como PK y FK. Cerramos con la importancia de las Transacciones y sus propiedades ACID para la confiabilidad.

---

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Terminología del Modelo Relacional

Consideremos una tabla `CLIENTES` en una base de datos relacional.

**Tabla CLIENTES (Relación)**

| ID_Cliente (PK) | Nombre    | Apellido  | Email                   | ID_Representante (FK) |
| :-------------- | :-------- | :-------- | :---------------------- | :-------------------- |
| 101             | Juan      | Pérez     | juan.perez@email.com    | 1                     |
| 102             | María     | García    | maria.garcia@email.com  | 2                     |
| 103             | Carlos    | López     | carlos.lopez@email.com  | 1                     |

*   **Relación:** Toda la tabla `CLIENTES` es una relación.
*   **Tupla:** Cada fila de la tabla es una tupla (Ej., la fila que contiene los datos de Juan Pérez es una tupla).
*   **Atributo:** Cada columna es un atributo (Ej., `Nombre`, `Apellido`, `Email` son atributos).
*   **Primary Key (PK):** `ID_Cliente` es la clave primaria. Identifica de forma única a cada cliente. Cada valor es distinto y no puede ser nulo.
*   **Foreign Key (FK):** `ID_Representante` es una clave foránea. Establece una relación con la clave primaria de una tabla `REPRESENTANTES` (que no se muestra aquí), indicando qué representante está asignado a cada cliente.

### Ejemplo 2: Arquitectura de Tres Niveles

Imaginemos un sistema de gestión de una biblioteca.

*   **Nivel Interno (Físico):** Esto describiría cómo los libros y la información de los usuarios están físicamente almacenados en los discos duros: qué tipo de archivos se usan, dónde están los índices para buscar rápidamente, y cómo se gestiona el espacio. Los administradores de la base de datos se preocupan por este nivel para optimizar el rendimiento.

*   **Nivel Conceptual (Lógico):** Es la visión global y abstracta de la biblioteca. Aquí veríamos las entidades principales (Libros, Usuarios, Préstamos, Autores) y cómo se relacionan entre sí. Por ejemplo, un `Usuario` puede realizar muchos `Préstamos`, y cada `Préstamo` se relaciona con un `Libro` específico. Este nivel define qué datos existen y sus relaciones, sin preocuparse por cómo se almacenan físicamente. Los diseñadores de bases de datos trabajan en este nivel.

*   **Nivel Externo (Vistas):** Son las diferentes "ventanas" o vistas personalizadas que los distintos usuarios tienen de la base de datos.
    *   **Vista para el Lector:** Podría ver solo la disponibilidad de los libros y su fecha de devolución, pero no vería los datos personales de otros usuarios ni los registros de multas.
    *   **Vista para el Bibliotecario:** Podría ver los datos de los usuarios, todos los préstamos activos y el historial, y tendría acceso a funciones para registrar nuevos libros o marcar devoluciones. No vería cómo los datos están guardados físicamente, solo la información relevante para su trabajo.

    La **independencia de datos** permite que si se cambia la forma en que los libros se guardan físicamente (cambio en el Nivel Interno), el bibliotecario y el lector no necesitan cambiar su forma de interactuar con el sistema (sus Vistas permanecen iguales).

---

## ✏️ Ejercicios Resueltos

### Ejercicio 1: Identificación de Componentes Relacionales

**Enunciado:**
Dada la siguiente estructura simplificada de una tabla `EMPLEADOS` en un sistema de base de datos universitario:

**Tabla `EMPLEADOS`**

| ID_Empleado (PK) | Nombre    | Apellido  | Email                 | ID_Departamento (FK) | Fecha_Contratacion | Salario |
| :--------------- | :-------- | :-------- | :-------------------- | :------------------- | :----------------- | :------ |
| 1001             | Ana       | García    | ana.g@uni.edu         | 10                   | 2018-03-01         | 60000   |
| 1002             | Luis      | Pérez     | luis.p@uni.edu        | 20                   | 2020-07-15         | 75000   |
| 1003             | Marta     | Sánchez   | marta.s@uni.edu       | 10                   | 2019-11-01         | 62000   |
| 1004             | Pedro     | Ruíz      | pedro.r@uni.edu       | 30                   | 2021-01-20         | 80000   |

Responde las siguientes preguntas basándote en la terminología del modelo relacional:

1.  ¿Cuál es el nombre de la **Relación**?
2.  Proporciona un ejemplo de **Tupla**.
3.  Proporciona tres ejemplos de **Atributos**.
4.  Identifica la **Primary Key (PK)** y justifica por qué lo es.
5.  Identifica la **Foreign Key (FK)** y explica su propósito.

**Solución:**

1.  **Relación:** `EMPLEADOS`
2.  **Tupla:** `(1001, Ana, García, ana.g@uni.edu, 10, 2018-03-01, 60000)` (cualquier fila completa es una tupla).
3.  **Atributos:** `ID_Empleado`, `Nombre`, `Apellido`, `Email`, `ID_Departamento`, `Fecha_Contratacion`, `Salario` (cualquier tres de estos).
4.  **Primary Key (PK):** `ID_Empleado`. Es la PK porque identifica de forma única a cada empleado; no hay dos empleados con el mismo `ID_Empleado`, y cada empleado debe tener un `ID_Empleado` (no puede ser nulo).
5.  **Foreign Key (FK):** `ID_Departamento`. Su propósito es establecer una relación con la tabla `DEPARTAMENTOS` (asumiendo que existe una tabla con `ID_Departamento` como PK), indicando a qué departamento pertenece cada empleado.

### Ejercicio 2: Aplicando las Propiedades ACID

**Enunciado:**
Un banco tiene un sistema de base de datos para gestionar transferencias de dinero. Un cliente desea transferir 100 USD de su cuenta A a la cuenta B de otro cliente. Describe cómo cada una de las propiedades ACID (`Atomicidad`, `Consistencia`, `Aislamiento`, `Durabilidad`) se aplica a esta operación de transferencia.

**Solución:**

1.  **Atomicidad:** La operación de transferencia completa (restar 100 USD de la cuenta A y sumar 100 USD a la cuenta B) debe ejecutarse por completo o no ejecutarse en absoluto. Si, por ejemplo, el sistema falla después de restar el dinero de la cuenta A pero antes de sumarlo a la cuenta B, la atomicidad asegura que la base de datos se revierta a su estado original, como si la transferencia nunca hubiera ocurrido. No puede haber una situación donde el dinero se pierda en el "aire".

2.  **Consistencia:** Antes de la transferencia, la suma del dinero en cuenta A y cuenta B debe ser un valor `X`. Después de una transferencia exitosa, la suma del dinero en cuenta A (restando 100) y cuenta B (sumando 100) debe seguir siendo `X`. La base de datos debe pasar de un estado consistente a otro estado consistente. Las reglas de negocio (ej. el saldo de una cuenta no puede ser negativo) también deben mantenerse.

3.  **Aislamiento:** Si otro cliente intenta consultar el saldo de la cuenta A o la cuenta B *durante* la transferencia, no verá un estado intermedio (ej. la cuenta A con el dinero restado pero la cuenta B aún sin el dinero sumado). Las operaciones de transferencia se ejecutan de forma aislada, como si fueran la única operación en el sistema. Otros usuarios verán el estado antes de la transferencia o el estado después de que la transferencia se haya completado exitosamente.

4.  **Durabilidad:** Una vez que la transferencia de dinero ha sido confirmada como exitosa (commit), los cambios realizados (dinero restado de A, dinero sumado a B) deben ser permanentes. Incluso si el sistema sufre un fallo de energía inmediatamente después del commit, la base de datos debe ser capaz de recuperar esos cambios y asegurar que el dinero esté correctamente reflejado en ambas cuentas cuando el sistema se reinicie.

---

## 📝 Balotario

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

---

