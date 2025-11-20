# Glosario - Clase 03: Lenguaje de Definición de Datos (DDL)

*   **ALTER TABLE:** Comando DDL utilizado para modificar la estructura existente de una tabla, como añadir, modificar o eliminar columnas, o añadir/eliminar restricciones.
*   **Atributo (Columna/Campo):** Una característica o propiedad que describe la entidad representada por una tabla, y que tiene un nombre único dentro de esa tabla.
*   **Base de Datos Relacional (BDR):** Un modelo de datos donde la información se organiza en tablas (relaciones) interconectadas, sin punteros físicos.
*   **Cardinalidad (Relacional):** El número de tuplas (filas) que contiene una relación (tabla).
*   **CHECK (Restricción):** Restricción de columna o tabla que asegura que todos los valores en una columna cumplan una condición específica.
*   **Clave Candidata:** Una superclave mínima, de la que no se puede eliminar ningún atributo sin perder la propiedad de unicidad.
*   **Clave Foránea (FK):** Un atributo o conjunto de atributos en una tabla (tabla hija) que hace referencia a la clave primaria de otra tabla (tabla padre), estableciendo una relación entre ellas y manteniendo la integridad referencial.
*   **Clave Primaria (PK):** Una de las claves candidatas elegida para identificar de forma única cada tupla en una tabla. Sus valores deben ser únicos y no nulos.
*   **CREATE TABLE:** Comando DDL fundamental para construir una nueva tabla en la base de datos, especificando sus columnas, tipos de datos y restricciones.
*   **DDL (Data Definition Language):** Lenguaje de Definición de Datos. Es el conjunto de comandos SQL utilizados para definir, modificar y gestionar la estructura de los objetos de la base de datos (tablas, vistas, índices, etc.).
*   **Dominio (Relacional):** El conjunto de todos los valores posibles y permitidos para un atributo específico.
*   **DROP TABLE:** Comando DDL utilizado para eliminar una tabla existente de la base de datos, junto con todos sus datos y estructuras dependientes.
*   **Índice:** Objeto de la base de datos que mejora la velocidad de recuperación de datos para las consultas al proporcionar un acceso rápido a las filas de una tabla, similar a un índice de libro.
*   **Integridad Referencial:** Reglas que aseguran la validez de las relaciones entre tablas, garantizando que una FK siempre apunte a una PK existente o sea nula.
*   **NOT NULL (Restricción):** Restricción de columna que obliga a que un atributo siempre tenga un valor y no pueda estar vacío.
*   **Objetos de la BD:** Elementos estructurados que componen una base de datos, como tablas, vistas, índices, secuencias, etc.
*   **ON DELETE CASCADE:** Opción de restricción de clave foránea que, al eliminar una fila en la tabla "padre", automáticamente elimina todas las filas dependientes en la tabla "hija".
*   **Relación (Tabla):** Una estructura bidimensional en el modelo relacional, compuesta por filas y columnas, que representa un conjunto de entidades.
*   **Restricciones de Columna:** Reglas que se aplican a los valores de una columna específica para mantener la validez y consistencia de los datos.
*   **Restricciones de Integridad:** Reglas que aseguran que los datos en la base de datos sean precisos y consistentes, especialmente en las relaciones entre tablas.
*   **Secuencia:** Objeto de la base de datos que genera valores numéricos únicos en una serie, a menudo utilizados para claves primarias autoincrementales.
*   **SQL (Structured Query Language):** Lenguaje estándar para interactuar con bases de datos relacionales, incluyendo comandos DDL, DML y DCL.
*   **Superclave:** Un atributo o conjunto de atributos que identifica de forma única una tupla dentro de una relación.
*   **Tupla (Fila/Registro):** Una instancia individual de una entidad en una relación, que contiene un conjunto de valores para cada uno de los atributos de la tabla.
*   **UNIQUE (Restricción):** Restricción de columna o tabla que asegura que todos los valores en una columna o conjunto de columnas sean únicos dentro de la tabla.
*   **Vista:** Objeto de la base de datos que es una tabla virtual o lógica, cuyo contenido se define mediante una consulta SQL, mostrando una representación específica de los datos de una o más tablas.