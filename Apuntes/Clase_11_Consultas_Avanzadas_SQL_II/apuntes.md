# 💻 Clase 11: SQL Embebido (PL/SQL)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **PL/SQL** | Es una extensión procedural de SQL, que nos permite usar lógica de programación (variables, sentencias condicionales, *loops*) junto con las sentencias SQL. |
| **Estructura PL/SQL** | Todo programa tiene tres secciones: **DECLARE** (opcional, se definen variables, cursores), **BEGIN** (obligatorio, se ejecuta la lógica y el SQL), y **EXCEPTION** (opcional, se manejan los errores, como `NO_DATA_FOUND`). |
| **Cursor (La Ventana)** | Un **Cursor** es una estructura que se usa cuando una consulta retorna muchas filas, permitiéndonos procesar el resultado **fila por fila** dentro del programa (usando `OPEN`, `FETCH` y `CLOSE`). |
| **Procedimientos (Acciones)** | Un `PROCEDURE` es un subprograma que ejecuta un conjunto de acciones y se almacena en la BD. Puede recibir parámetros de entrada (`IN`), salida (`OUT`) o ambos (`IN OUT`). |
| **Funciones (Retorna Valor)** | Una `FUNCTION` es similar a un procedimiento, pero su objetivo principal es **calcular y retornar un único valor** al entorno que la llamó (Ej. calcular un impuesto). |
| **Triggers (Eventos Automáticos)** | Un `TRIGGER` es código PL/SQL que se ejecuta **automáticamente** y de forma reactiva, justo *antes* o *después* de un evento específico (como un `INSERT`, `UPDATE` o `DELETE`). Son perfectos para chequear reglas de negocio al instante (Ej. verificar que el salario no exceda un límite). |
| **Paquetes** | Los paquetes son contenedores lógicos que agrupan procedimientos y funciones relacionados. |

**Resumen de la Clase 11:** PL/SQL combina SQL con programación procedural, permitiendo crear bloques lógicos y manejar excepciones. Las estructuras clave son los Procedimientos (para ejecutar acciones) y las Funciones (para retornar un valor). Además, los Triggers son vitales para ejecutar código automáticamente basado en eventos.

---