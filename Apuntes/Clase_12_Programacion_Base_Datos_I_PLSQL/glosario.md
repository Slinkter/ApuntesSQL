# Glosario - Clase 12: Programación en Base de Datos I: Introducción a PL/SQL

*   **PL/SQL (Procedural Language/SQL):** Extensión procedural del lenguaje SQL de Oracle, que permite combinar sentencias SQL con estructuras de control y lógica de programación.
*   **Bloque Anónimo:** Unidad básica de código PL/SQL que se compila y ejecuta en tiempo de ejecución, pero no se almacena en la base de datos.
*   **Subprograma (PL/SQL):** Unidades de código PL/SQL nombradas que se almacenan en la base de datos y pueden ser reutilizadas (ej. procedimientos, funciones, paquetes, triggers).
*   **Procedimiento Almacenado (PL/SQL):** Subprograma PL/SQL que realiza una acción específica y puede aceptar parámetros de entrada y salida, pero no devuelve un valor directamente.
*   **Función (PL/SQL):** Subprograma PL/SQL que calcula y devuelve un único valor, típicamente utilizado en expresiones SQL.
*   **DECLARE (PL/SQL):** Sección opcional en un bloque PL/SQL donde se declaran variables, constantes, cursores y excepciones.
*   **BEGIN (PL/SQL):** Sección obligatoria en un bloque PL/SQL que contiene el código ejecutable.
*   **EXCEPTION (PL/SQL):** Sección opcional en un bloque PL/SQL donde se manejan los errores de tiempo de ejecución.
*   **END (PL/SQL):** Final de un bloque PL/SQL o subprograma.
*   **DBMS_OUTPUT.PUT_LINE:** Procedimiento del paquete `DBMS_OUTPUT` que permite mostrar información en la consola o buffer de salida durante la ejecución de PL/SQL.
*   **Tipos de Datos PL/SQL:** Categorías para almacenar diferentes tipos de información en variables (ej. CHAR, VARCHAR2, NUMBER, PLS_INTEGER, BOOLEAN, DATE, TIMESTAMP).
*   **%TYPE:** Atributo que permite declarar una variable con el mismo tipo de dato y tamaño que una columna de tabla existente o otra variable.
*   **IF-ELSIF-ELSE:** Estructura de control condicional para ejecutar diferentes bloques de código según una o varias condiciones.
*   **CASE (PL/SQL):** Estructura de control condicional que evalúa una expresión o múltiples condiciones para ejecutar un bloque de código específico.
*   **LOOP (PL/SQL):** Estructura de bucle básica que repite un bloque de código hasta que se encuentra una condición de salida (`EXIT WHEN`).
*   **WHILE-LOOP:** Estructura de bucle que repite un bloque de código mientras una condición específica sea verdadera.
*   **FOR-LOOP:** Estructura de bucle que itera sobre un rango de valores numéricos o sobre los resultados de un cursor.
*   **UTL_FILE:** Paquete estándar de Oracle que proporciona funcionalidades para leer y escribir archivos en el sistema operativo desde PL/SQL.
*   **DIRECTORY (Oracle):** Objeto de base de datos que crea un alias para una ruta física en el sistema de archivos del servidor, utilizado por paquetes como `UTL_FILE`.
*   **FOPEN:** Función de `UTL_FILE` para abrir un archivo.
*   **FCLOSE:** Función de `UTL_FILE` para cerrar un archivo.
*   **PUT_LINE:** Procedimiento de `UTL_FILE` para escribir una línea de texto en un archivo.
*   **GET_LINE:** Procedimiento de `UTL_FILE` para leer una línea de texto de un archivo.
