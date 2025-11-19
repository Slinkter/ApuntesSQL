# Clase 12: Programación en Base de Datos I: Introducción a PL/SQL

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Introducción a PL/SQL

PL/SQL (Procedural Language/SQL) es una extensión de programación del lenguaje SQL, desarrollado por Oracle. Permite combinar las sentencias SQL con las características de los lenguajes de programación procedurales (estructuras de control, variables, etc.). Es un lenguaje de programación de cuarta generación (4GL) para la base de datos Oracle.

**Arquitectura de PL/SQL:**
*   Todo código PL/SQL se compone de código PL/SQL y sentencias SQL.
*   El código PL/SQL es ejecutado por un "PL/SQL engine".
*   Las sentencias SQL son ejecutadas por el "SQL Statement Executor" (Oracle Database Server).
*   Oracle Database tiene un engine PL/SQL inherente.

**Beneficios de PL/SQL:**
*   Creación de programas modulares.
*   Integración con herramientas de Oracle.
*   Portabilidad.
*   Manejo de excepciones.

### Bloques PL/SQL

Un bloque PL/SQL es la unidad básica de código en PL/SQL. Puede ser:
*   **Bloque Anónimo:** Código que reside y se ejecuta en el lado del cliente (ej. en SQL Developer). No se almacena en la base de datos.
    ```sql
    [DECLARE] -- Sección opcional para declarar variables, cursores, excepciones
        -- Declaraciones aquí
    BEGIN
        -- Código ejecutable
    [EXCEPTION] -- Sección opcional para manejo de errores
        -- Manejo de excepciones aquí
    END;
    /
    ```
*   **Subprogramas:** Código que reside y se ejecuta en el servidor. Pueden ser Stored Procedures, Funciones, Triggers y Paquetes. Se almacenan en la base de datos y pueden ser reutilizados.

### Declaración de Variables y Tipos de Datos

Las variables se declaran en la sección `DECLARE` de un bloque PL/SQL.
**Sintaxis:** `nombre_variable TIPO_DATO [:= valor_inicial];`

**Tipos de Datos Comunes (Oracle Database 11g):**
*   **CHAR(n):** Caracteres de longitud fija (hasta 32,767 bytes).
*   **VARCHAR2(n):** Caracteres de longitud variable (hasta 32,767 bytes).
*   **NUMBER(p,s):** Números con precisión (p) y escala (s).
*   **BINARY_INTEGER / PLS_INTEGER:** Enteros con signo (más rápidos y con menor almacenamiento que NUMBER para enteros).
*   **BOOLEAN:** Almacena TRUE, FALSE o NULL.
*   **DATE:** Almacena fecha y hora (segundos desde la medianoche).
*   **TIMESTAMP [(precision)] WITH [LOCAL] TIME ZONE:** Almacena fecha, hora y fracciones de segundo, con o sin información de zona horaria.
*   **%TYPE:** Permite declarar una variable con el mismo tipo de dato y tamaño que una columna de tabla o otra variable existente (`variable_name tabla.columna%TYPE;` o `variable_name otra_variable%TYPE;`).

### Estructuras de Control

**1. Condicionales:**
*   **IF-ELSIF-ELSE:**
    ```sql
    IF (condicion_logica) THEN
        -- Acciones
    ELSIF (otra_condicion) THEN
        -- Acciones
    ELSE
        -- Acciones
    END IF;
    ```
*   **CASE:**
    ```sql
    CASE
        WHEN condicion1 THEN -- Acciones
        WHEN condicion2 THEN -- Acciones
        ELSE -- Acciones
    END CASE;
    ```

**2. Bucles:**
*   **LOOP:** Bucle básico que se ejecuta hasta que una condición de salida es met.
    ```sql
    LOOP
        -- Acciones
        EXIT WHEN condicion_salida;
    END LOOP;
    ```
*   **WHILE-LOOP:** Se ejecuta mientras una condición sea verdadera.
    ```sql
    WHILE condicion LOOP
        -- Acciones
    END LOOP;
    ```
*   **FOR-LOOP:** Se usa para iterar un número predefinido de veces.
    ```sql
    FOR variable_contador IN inicio..final LOOP
        -- Acciones
    END LOOP;
    ```
    (Nota: La variable `variable_contador` no necesita ser declarada previamente en la sección `DECLARE`).

### Manejo de Archivos (UTL_FILE)

Oracle Database permite crear y leer archivos en el sistema operativo mediante el paquete `UTL_FILE`.
**Requisitos:** Se debe crear un objeto `DIRECTORY` en la base de datos que apunte a una ruta del sistema operativo.
**Funciones principales:** `FOPEN` (abrir), `FCLOSE` (cerrar), `PUT_LINE` (escribir línea), `GET_LINE` (leer línea).

---

## Pistas y Keywords

*   **PL/SQL:** Lenguaje procedural de Oracle, extensión de SQL.
*   **SQL Statement Executor:** Componente que procesa sentencias SQL en la base de datos.
*   **Bloque Anónimo:** Código PL/SQL no almacenado en la DB.
*   **Subprograma:** Código PL/SQL almacenado en la DB (Procedure, Function, Trigger, Package).
*   **DECLARE:** Sección para declaración de variables.
*   **Data Types:** CHAR, VARCHAR2, NUMBER, PLS_INTEGER, BOOLEAN, DATE, TIMESTAMP.
*   **%TYPE:** Declaración de tipo basado en una columna o variable existente.
*   **Control Structures:** IF/CASE, LOOP/WHILE/FOR.
*   **UTL_FILE:** Paquete para manejo de archivos.
*   **DIRECTORY:** Objeto de base de datos que mapea a una ruta del sistema de archivos.

---

## Resumen Final Crítico

PL/SQL es una herramienta poderosa que integra la funcionalidad de SQL con la lógica procedural, permitiendo a los desarrolladores crear aplicaciones de base de datos más complejas y eficientes. La comprensión de la estructura de bloques, la declaración de variables y el uso de estructuras de control son fundamentales para escribir código PL/SQL efectivo. Aunque existen limitaciones para la manipulación directa del sistema de archivos, el paquete `UTL_FILE` ofrece una interfaz controlada para estas operaciones, lo que es vital para tareas como la generación de informes o la carga de datos. El dominio de estos conceptos básicos es el primer paso esencial para cualquier programación avanzada en Oracle.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase se construye sobre el conocimiento de SQL (Clase 05, 10 y 11), permitiendo la integración de consultas SQL con lógica programática. Los fundamentos de bases de datos relacionales y administración (Clase 03 y 04) son la base sobre la cual PL/SQL opera.
*   **Conexiones Siguientes:** Esta introducción sienta las bases para temas más avanzados de PL/SQL, como el manejo de cursores, excepciones, procedimientos almacenados, funciones, paquetes y triggers, que se explorarán en la Clase 13. La capacidad de programar directamente en la base de datos es crucial para la eficiencia y la seguridad del sistema.
