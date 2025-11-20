# Glosario - Clase 11: SQL Embebido (PL/SQL)

*   **BEGIN (PL/SQL):** Sección obligatoria en un bloque PL/SQL donde se coloca la lógica de ejecución del programa y las sentencias SQL.
*   **Bloque PL/SQL:** La unidad básica de un programa PL/SQL, que puede ser anónimo o nombrado (procedimiento, función, paquete, trigger).
*   **Cursor:** Estructura de memoria utilizada para procesar un conjunto de filas devuelto por una consulta `SELECT` de forma individual, fila por fila.
*   **DECLARE (PL/SQL):** Sección opcional en un bloque PL/SQL donde se declaran variables, cursores y excepciones.
*   **EXCEPTION (PL/SQL):** Sección opcional en un bloque PL/SQL donde se manejan los errores que puedan ocurrir durante la ejecución del programa.
*   **Función (PL/SQL):** Un tipo de subprograma PL/SQL que realiza una tarea específica y siempre **retorna un único valor** al entorno que la invocó.
*   **LOOP (PL/SQL):** Estructura de control de flujo que permite ejecutar un bloque de código repetidamente.
*   **NO_DATA_FOUND:** Excepción predefinida en PL/SQL que se dispara cuando una sentencia `SELECT INTO` no encuentra ninguna fila.
*   **Paquetes (PL/SQL):** Contenedores lógicos que agrupan procedimientos, funciones, variables, cursores y tipos relacionados, facilitando la organización y reutilización del código.
*   **PL/SQL:** Extensión procedural del lenguaje SQL, que combina la potencia de SQL para la manipulación de datos con las capacidades de programación procedural (variables, estructuras de control, manejo de errores).
*   **Parámetro IN:** Parámetro de un procedimiento o función PL/SQL que se utiliza para pasar valores de entrada al subprograma.
*   **Parámetro IN OUT:** Parámetro de un procedimiento o función PL/SQL que se utiliza para pasar valores de entrada y para retornar valores de salida desde el subprograma.
*   **Parámetro OUT:** Parámetro de un procedimiento o función PL/SQL que se utiliza para retornar valores de salida desde el subprograma.
*   **Procedimiento (PL/SQL):** Un tipo de subprograma PL/SQL que realiza una tarea específica y se almacena en la base de datos. Puede aceptar parámetros de entrada y/o salida, pero no retorna un valor directamente.
*   **SQL Embebido:** La integración de sentencias SQL dentro de un lenguaje de programación procedural (como PL/SQL, Java con JDBC, C# con ADO.NET, etc.).
*   **Trigger (PL/SQL):** Bloque de código PL/SQL que se ejecuta automáticamente (se "dispara") en respuesta a un evento específico en la base de datos, como una operación `INSERT`, `UPDATE` o `DELETE` en una tabla, o un evento de nivel de esquema/base de datos.
*   **Variables (PL/SQL):** Espacios de memoria con nombre que se utilizan para almacenar valores durante la ejecución de un bloque PL/SQL.