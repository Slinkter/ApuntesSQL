# 🛠️ Clase 03: Lenguaje de Definición de Datos (DDL)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **BDR y SQL** | Una Base de Datos Relacional es una colección de tablas sin punteros físicos, ¡y todo se accede y modifica con sentencias del famoso **SQL**!. |
| **Objetos de la BD** | La BD está hecha de varios "juguetes": la **Tabla** (almacenamiento básico), la **Vista** (representación lógica de los datos), el **Índice** (para mejorar la velocidad de consulta), y la **Secuencia** (para generar valores de PK). |
| **DDL (Definición de Datos)** | Es el conjunto de comandos que usamos para **definir y modificar la estructura** de estos objetos (CREATE, ALTER, DROP). |
| **Restricciones (¡Las Reglas!)** | Hay varios tipos de reglas: **Integridad** (PK única y no nula, FK relacionada con una PK válida), y de **Columna** (el valor debe ser del tipo de dato definido). Las restricciones `NOT NULL`, `UNIQUE` y `CHECK` mantienen el orden. |
| **CREATE TABLE** | Es el comando para construir una tabla, especificando cada columna, su tipo de dato (como `DATE`, `NUMBER`, `VARCHAR2`) y sus restricciones (como `PRIMARY KEY` o `REFERENCES` para la FK). |
| **ON DELETE CASCADE** | Esta es una opción poderosa para la FK. Significa que, si borras un registro en la tabla "Padre" (la que tiene la PK), ¡automáticamente se borran todos los registros dependientes en la tabla "Hijo"!. |
| **ALTER y DROP** | Si necesitas hacer cambios después de crear la tabla, usas **ALTER TABLE** para modificar o eliminar columnas. Si ya no quieres la tabla, la eliminas con **DROP TABLE**. |

**Resumen de la Clase 03:** El enfoque relacional usa SQL para interactuar con objetos como Tablas y Vistas. El DDL nos da las herramientas (`CREATE`, `ALTER`, `DROP`) para construir la estructura, asegurando que las reglas de integridad (PK y FK) se cumplan.

---