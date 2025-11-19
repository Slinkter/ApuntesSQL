# Glosario - Clase 13: Programación en Base de Datos II: Temas Avanzados de PL/SQL

*   **Records (PL/SQL):** Estructuras de datos compuestas que permiten agrupar campos de diferentes tipos de datos bajo un único nombre, mejorando la organización del código.
*   **Index By Tables (Tablas Asociativas):** Colecciones unidimensionales flexibles, indexadas por valores enteros o de cadena, utilizadas para almacenar datos de forma temporal en PL/SQL.
*   **Nested Tables (Tablas Anidadas):** Colecciones unidimensionales que pueden ser almacenadas como columnas en tablas de base de datos, con tamaño dinámico y métodos como `EXTEND`.
*   **VArrays (Vectores de Tamaño Variable):** Colecciones unidimensionales similares a las tablas anidadas, pero con un tamaño máximo predefinido desde su declaración.
*   **Cursor Explícito:** Un puntero nombrado a un área de memoria que almacena el conjunto de resultados de una sentencia `SELECT`, controlado explícitamente por el programador.
*   **OPEN (Cursor):** Comando que ejecuta la consulta asociada a un cursor explícito y lo prepara para recuperar filas.
*   **FETCH (Cursor):** Comando que recupera una o varias filas del cursor y las asigna a variables PL/SQL.
*   **CLOSE (Cursor):** Comando que libera los recursos asociados a un cursor explícito.
*   **Atributos de Cursor:** Propiedades de un cursor que proporcionan información sobre su estado o los resultados de la operación (`%ISOPEN`, `%NOTFOUND`, `%FOUND`, `%ROWCOUNT`).
*   **Cursores con Parámetros:** Cursores explícitos que aceptan parámetros de entrada, permitiendo reutilizar su definición con diferentes condiciones de consulta.
*   **REF CURSOR (Cursor Genérico):** Un tipo de datos PL/SQL que representa un puntero a un conjunto de resultados, permitiendo mayor flexibilidad al asignar dinámicamente la consulta en tiempo de ejecución.
*   **WHERE CURRENT OF:** Cláusula utilizada en sentencias `UPDATE` o `DELETE` para afectar la fila actual sobre la que está posicionado un cursor `FOR UPDATE`.
*   **Manejo de Excepciones (PL/SQL):** Mecanismo para detectar y responder a errores de tiempo de ejecución de manera controlada, evitando que el programa termine abruptamente.
*   **Excepción Predefinida:** Errores comunes de Oracle que tienen nombres específicos en PL/SQL (ej. `NO_DATA_FOUND`, `TOO_MANY_ROWS`).
*   **PRAGMA EXCEPTION_INIT:** Directiva del compilador que asocia un nombre de excepción definido por el usuario a un número de error estándar de Oracle.
*   **SQLERRM:** Función que devuelve el mensaje de error asociado al último error de SQL o PL/SQL.
*   **SQLCODE:** Función que devuelve el número de error asociado al último error de SQL o PL/SQL.
*   **RAISE_APPLICATION_ERROR:** Procedimiento que permite a los desarrolladores lanzar excepciones definidas por el usuario con mensajes y códigos de error personalizados.
*   **Paquete (PL/SQL):** Una unidad de esquema que agrupa lógicamente procedimientos, funciones, variables, cursores y otros elementos PL/SQL relacionados.
*   **Especificación de Paquete:** La parte de un paquete que declara la interfaz pública de sus elementos (lo que es visible y accesible desde fuera).
*   **Cuerpo de Paquete:** La parte de un paquete que contiene la implementación detallada de los elementos declarados en la especificación y puede incluir elementos privados.
*   **Trigger (PL/SQL):** Bloques de código PL/SQL o SQL que se ejecutan automáticamente en respuesta a un evento específico en la base de datos (ej. operaciones DML, sentencias DDL, eventos de la base de datos).
*   **Trigger DML:** Un trigger que se dispara por sentencias `INSERT`, `UPDATE` o `DELETE` en una tabla o vista.
*   **Trigger INSTEAD OF:** Un tipo de trigger que se dispara en vistas no actualizables para realizar operaciones de DML en las tablas subyacentes.
*   **:NEW (Trigger):** Pseudoregistro en triggers que contiene los nuevos valores de la fila afectada por una operación de DML.
*   **:OLD (Trigger):** Pseudoregistro en triggers que contiene los valores originales de la fila afectada por una operación de DML.
*   **EXECUTE IMMEDIATE:** Sentencia utilizada para ejecutar SQL o PL/SQL dinámico (construido como una cadena de texto) en tiempo de ejecución.
*   **NOCOPY:** Un hint de compilación que permite que los parámetros `OUT` e `IN OUT` de procedimientos y funciones se pasen por referencia, mejorando el rendimiento al evitar la copia de datos.
*   **BULK COLLECT:** Cláusula utilizada con `FETCH` para recuperar múltiples filas en una colección PL/SQL con una sola operación de E/S, reduciendo los "context switches".
*   **FORALL:** Sentencia utilizada para ejecutar una instrucción DML (INSERT, UPDATE, DELETE, MERGE) múltiples veces sobre una colección de datos con una sola operación de E/S, optimizando el rendimiento.
*   **Programación Orientada a Objetos en PL/SQL:** La capacidad de PL/SQL para definir y manipular tipos de objetos con atributos y métodos, soportando conceptos como encapsulación, herencia y polimorfismo.
*   **Tipo de Objeto (PL/SQL):** Un esquema definido por el usuario que encapsula datos (atributos) y el comportamiento (métodos) de una entidad del mundo real.
*   **Herencia (PL/SQL):** La capacidad de un tipo de objeto de derivar atributos y métodos de otro tipo de objeto (su supertipo), lo que permite la reutilización de código.
*   **Polimorfismo (PL/SQL):** La capacidad de que un método en un subtipo tenga una implementación diferente a la del supertipo, sobreescribiendo el comportamiento (`OVERRIDING MEMBER FUNCTION`).
