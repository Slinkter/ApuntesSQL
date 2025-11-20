# Clase 13: Programación en Base de Datos II: Temas Avanzados de PL/SQL

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Manejo de Estructuras Complejas

PL/SQL permite la creación y manipulación de estructuras de datos más complejas que las variables escalares:

*   **Registros (Records):** Permiten agrupar un conjunto de campos de diferentes tipos de datos, similar a una estructura en otros lenguajes de programación. Pueden ser basados en tablas (`%ROWTYPE`) o definidos por el usuario.
*   **Index By Tables (Tablas Asociativas):** Arreglos unidimensionales que se indexan por un `BINARY_INTEGER`, `PLS_INTEGER` o `VARCHAR2`. Son flexibles y no requieren inicialización previa de los nodos.
*   **Nested Tables (Tablas Anidadas):** Arreglos unidimensionales que pueden ser almacenados como columnas de tabla. Se inicializan y requieren el método `EXTEND` para añadir elementos.
*   **VArrays (Vectores de Tamaño Variable):** Arreglos unidimensionales con un tamaño máximo predefinido. También pueden almacenarse como columnas de tabla y requieren `EXTEND`.

### Manejo de Cursores

Un cursor es un puntero a un área de memoria en la que se almacenan los resultados de una sentencia `SELECT`.

*   **Cursores Implícitos:** Creados automáticamente por Oracle para cada sentencia DML o `SELECT INTO`.
*   **Cursores Explícitos:** Definidos por el programador para manejar consultas `SELECT` que devuelven múltiples filas.
    *   **Ciclo de vida:** `DECLARE` (definir cursor), `OPEN` (abrir cursor), `FETCH` (obtener filas), `CLOSE` (cerrar cursor).
    *   **Atributos de Cursor:** `%ISOPEN`, `%NOTFOUND`, `%FOUND`, `%ROWCOUNT`.
    *   **Cursores con Parámetros:** Permiten reutilizar la misma definición de cursor con diferentes valores.
    *   **Cursores Genéricos (REF CURSOR):** Tipos de cursor flexibles que pueden asociarse a diferentes sentencias `SELECT` en tiempo de ejecución.
    *   **`WHERE CURRENT OF`:** Permite actualizar o borrar la fila actual apuntada por un cursor, requiere `SELECT FOR UPDATE`.

### Manipulación de Excepciones

PL/SQL proporciona un robusto mecanismo para manejar errores de tiempo de ejecución (excepciones).

*   **Bloque `EXCEPTION`:** Sección en un bloque PL/SQL donde se captura y maneja un error.
*   **Excepciones Predefinidas:** Errores comunes de Oracle (ej. `NO_DATA_FOUND`, `TOO_MANY_ROWS`).
*   **Excepciones Definidas por el Usuario:** Se pueden declarar excepciones propias y asociarlas a códigos de error Oracle (`PRAGMA EXCEPTION_INIT`).
*   **`SQLERRM` y `SQLCODE`:** Funciones que devuelven el mensaje y el código del último error.
*   **`WHEN OTHERS THEN`:** Captura cualquier excepción no manejada específicamente.
*   **`RAISE_APPLICATION_ERROR`:** Permite lanzar errores personalizados con códigos y mensajes definidos por el usuario.

### Creación de Stored Procedures y Funciones

*   **Procedimientos Almacenados:** Subprogramas que realizan acciones. Sintaxis: `CREATE OR REPLACE PROCEDURE nombre (parametros) IS ... BEGIN ... END;`. Parámetros pueden ser `IN`, `OUT`, `IN OUT`.
*   **Funciones:** Subprogramas que calculan y devuelven un valor. Sintaxis: `CREATE OR REPLACE FUNCTION nombre (parametros) RETURN tipo IS ... BEGIN ... RETURN valor; END;`.

### Creación de Paquetes

Un paquete es una agrupación lógica de variables, cursores, procedimientos y funciones relacionados.

*   **Especificación (Specification):** Define la interfaz pública del paquete (lo que es visible desde fuera).
*   **Cuerpo (Body):** Contiene la implementación de los subprogramas declarados en la especificación y puede incluir elementos privados.
*   **Beneficios:** Modularidad, ocultación de información, rendimiento (carga una vez en memoria).

### Creación de Triggers

Los triggers son subprogramas que se disparan automáticamente en respuesta a eventos de la base de datos (DML, DDL, eventos de la base de datos).

*   **Tipos:**
    *   **Triggers DML:** Se disparan en operaciones `INSERT`, `UPDATE`, `DELETE`. Pueden ser `BEFORE` o `AFTER`, y `FOR EACH ROW` (nivel de fila) o de sentencia (nivel de sentencia).
    *   **Triggers `INSTEAD OF`:** Se usan para actualizar vistas no modificables directamente.
*   **Variables de Transición:** `:NEW` (valores después de la operación), `:OLD` (valores antes de la operación).
*   **Restricciones:** No pueden crear objetos en `SYS`, ni confirmar o anular transacciones DML.

### Consideraciones en el Diseño de Código PL/SQL

*   **Ejecución de Operaciones DDL y DCL:** Se usa `EXECUTE IMMEDIATE` para ejecutar sentencias SQL dinámicas.
*   **`NOCOPY`:** Hint para pasar parámetros `OUT` e `IN OUT` por referencia, mejorando el rendimiento al evitar copias de datos grandes.
*   **`BULK COLLECT`:** Optimiza la recuperación de datos de cursores o sentencias `SELECT` al cargar múltiples filas en una colección (tabla indexada, tabla anidada, varray) con un solo "context switch".
*   **`FORALL`:** Optimiza la ejecución de sentencias DML (INSERT, UPDATE, DELETE) al aplicarlas a colecciones de datos con un solo "context switch".

### Programación Orientada a Objetos en PL/SQL

PL/SQL soporta conceptos de POO a través de **Tipos de Objeto**, que permiten definir objetos con atributos y métodos, soportando herencia (`UNDER`) y polimorfismo (`OVERRIDING`). Los objetos pueden ser almacenados en tablas.

---

## Pistas y Keywords

*   **Record (PL/SQL):** Estructura de datos para agrupar campos.
*   **%ROWTYPE:** Declaración de registro basada en una fila de tabla.
*   **Index By Table:** Arreglo asociativo indexado por BINARY_INTEGER/PLS_INTEGER/VARCHAR2.
*   **Nested Table:** Arreglo unidimensional, puede ser columna de tabla, necesita EXTEND.
*   **VArray:** Arreglo de tamaño fijo, puede ser columna de tabla, necesita EXTEND.
*   **Cursor:** Puntero a un conjunto de resultados SQL.
*   **OPEN, FETCH, CLOSE:** Ciclo de vida de un cursor explícito.
*   **%ISOPEN, %NOTFOUND, %FOUND, %ROWCOUNT:** Atributos de cursor.
*   **REF CURSOR:** Cursor genérico, flexible.
*   **EXCEPTION:** Bloque de manejo de errores.
*   **PRAGMA EXCEPTION_INIT:** Asociar excepción definida por usuario a código de error.
*   **SQLERRM, SQLCODE:** Funciones para obtener mensaje y código de error.
*   **RAISE_APPLICATION_ERROR:** Lanzar error personalizado.
*   **Stored Procedure:** Subprograma que realiza acciones.
*   **Function (PL/SQL):** Subprograma que devuelve un valor.
*   **Package:** Agrupación lógica de subprogramas y variables.
*   **Trigger:** Subprograma que se dispara por eventos (DML, DDL).
*   **:NEW, :OLD:** Variables de transición en triggers.
*   **EXECUTE IMMEDIATE:** Ejecutar SQL dinámico.
*   **NOCOPY:** Pasar parámetros por referencia.
*   **BULK COLLECT:** Optimizar FETCH múltiple de filas.
*   **FORALL:** Optimizar DML múltiple de filas.
*   **OOP PL/SQL:** Tipos de objeto, herencia, polimorfismo.

---

## Resumen Final Crítico

La segunda parte de PL/SQL profundiza en funcionalidades avanzadas que son indispensables para construir aplicaciones robustas, escalables y eficientes. El manejo de estructuras complejas (Records, colecciones), la gestión de cursores para el procesamiento de conjuntos de datos, y una sólida estrategia de manipulación de excepciones son pilares fundamentales para la fiabilidad del código. Además, la creación y organización de código a través de procedimientos, funciones, paquetes y triggers permite una modularidad y reutilización excepcionales. Finalmente, técnicas de optimización como `NOCOPY`, `BULK COLLECT` y `FORALL` son vitales para mejorar el rendimiento, mientras que la capacidad de PL/SQL para la programación orientada a objetos abre nuevas avenidas para el diseño de soluciones complejas. Dominar estos aspectos convierte a un desarrollador en un programador PL/SQL experto.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase es una continuación directa de los fundamentos de PL/SQL vistos en la Clase 12, construyendo sobre la sintaxis básica, la declaración de variables y las estructuras de control. También utiliza los conceptos de SQL y modelamiento de datos de clases previas para manipular y consultar la base de datos de manera programática.
*   **Conexiones Siguientes:** Los temas avanzados de PL/SQL son cruciales para el desarrollo de sistemas de Data Warehouse (Clase 14) y la implementación de soluciones en tópicos avanzados de bases de datos (Clase 15), donde la eficiencia, la automatización y la lógica de negocio compleja a menudo se implementan directamente en la capa de la base de datos.

---

## Material de Referencia

La siguiente documentación de Oracle fue utilizada como material de apoyo para esta clase. Se recomienda su revisión para una comprensión más profunda.

*   `../../Ingenieria de datos/0.Documentacion Oracle/Taller_Oracle_PLSQL_22112010.pdf`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Concepto_HA_CTG.pdf`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les01.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les02.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les03.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les04.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les05.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les06.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les07.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les08.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les09.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les10.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les11.ppt`
