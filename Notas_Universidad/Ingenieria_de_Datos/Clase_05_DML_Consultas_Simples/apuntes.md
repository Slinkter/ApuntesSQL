# Clase 05: DML y Consultas Simples

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Lenguaje de Manipulación de Datos (DML)

El Lenguaje de Manipulación de Datos (DML) es una parte fundamental de SQL que permite a los usuarios interactuar con los datos almacenados en la base de datos. Se utiliza para consultar, insertar, actualizar y eliminar registros.

### Sentencia SELECT: Consultas Simples

La sentencia `SELECT` es la operación DML más común y se utiliza para recuperar datos de una o varias tablas.

**Sintaxis Básica:**
```sql
SELECT [DISTINCT] column1, column2, ... | *
FROM table_name
[WHERE condition]
[ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...];
```

**Componentes Clave:**
*   **`SELECT`**: Especifica las columnas que se desean recuperar.
    *   `*`: Selecciona todas las columnas de la tabla.
    *   `DISTINCT`: Elimina filas duplicadas del resultado.
*   **`FROM`**: Indica la tabla de la cual se van a recuperar los datos.
*   **`WHERE`**: Filtra las filas basándose en una condición específica.
    *   **Operadores de Comparación:** `=`, `!=` (o `<>`), `>`, `<`, `>=`, `<=`.
    *   **Operadores Lógicos:** `AND`, `OR`, `NOT`.
    *   **Operadores Especiales:**
        *   `BETWEEN valor1 AND valor2`: Rango inclusivo.
        *   `IN (valor1, valor2, ...)`: Coincide con cualquiera de los valores de una lista.
        *   `LIKE 'patron'` (con `%` para múltiples caracteres y `_` para un solo carácter): Búsqueda de patrones en cadenas de texto.
        *   `IS NULL / IS NOT NULL`: Comprueba si un valor es nulo.
*   **`ORDER BY`**: Ordena el conjunto de resultados por una o varias columnas.
    *   `ASC`: Orden ascendente (por defecto).
    *   `DESC`: Orden descendente.

### Sentencia INSERT: Insertar Datos

La sentencia `INSERT` se utiliza para añadir nuevas filas (registros) a una tabla.

**Sintaxis:**
```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);

-- O para insertar todas las columnas (en el orden definido de la tabla):
INSERT INTO table_name
VALUES (value1, value2, ...);

-- Insertar desde otra consulta:
INSERT INTO table_name (column1, column2, ...)
SELECT column_a, column_b, ...
FROM another_table
WHERE condition;
```

### Sentencia UPDATE: Modificar Datos

La sentencia `UPDATE` se utiliza para modificar datos existentes en una o varias filas de una tabla.

**Sintaxis:**
```sql
UPDATE table_name
SET column1 = new_value1, column2 = new_value2, ...
[WHERE condition];
```
**Precaución:** Si se omite la cláusula `WHERE`, la operación `UPDATE` afectará a todas las filas de la tabla.

### Sentencia DELETE: Eliminar Datos

La sentencia `DELETE` se utiliza para eliminar una o varias filas de una tabla.

**Sintaxis:**
```sql
DELETE FROM table_name
[WHERE condition];
```
**Precaución:** Si se omite la cláusula `WHERE`, la operación `DELETE` eliminará todas las filas de la tabla.

### SQL vs. PL/SQL (Contexto)

Aunque en esta clase nos centramos en DML puro (SQL), es importante recordar que en clases posteriores (PL/SQL) aprenderemos a integrar estas sentencias dentro de bloques de código más complejos, añadiendo lógica procedural y control de flujo.

---

## Pistas y Keywords

*   **DML:** Lenguaje de Manipulación de Datos.
*   **SELECT:** Recuperar datos.
*   **FROM:** Especifica la tabla.
*   **WHERE:** Filtra filas.
*   **ORDER BY:** Ordena resultados.
*   **DISTINCT:** Elimina duplicados.
*   **AND, OR, NOT:** Operadores lógicos.
*   **BETWEEN, IN, LIKE, IS NULL:** Operadores de filtrado.
*   **INSERT:** Añadir nuevas filas.
*   **UPDATE:** Modificar filas existentes.
*   **SET:** Asigna nuevos valores en `UPDATE`.
*   **DELETE:** Eliminar filas.

---

## Resumen Final Crítico

Las sentencias DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) constituyen el núcleo de la interacción diaria con una base de datos relacional. Dominar `SELECT` con sus diversas cláusulas de filtrado y ordenación es fundamental para extraer información útil de los datos. De igual manera, las operaciones `INSERT`, `UPDATE` y `DELETE` son cruciales para mantener los datos actualizados y relevantes. Una comprensión sólida de DML es indispensable para cualquier desarrollador, analista o administrador de bases de datos, ya que permite la manipulación directa y precisa de la información almacenada.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase aplica directamente los conceptos de "Bases de Datos Relacionales" (Clase 03), utilizando las tablas y sus atributos. Se basa en el rol del "SGBD" (Clase 02) como la herramienta que procesa estas sentencias.
*   **Conexiones Siguientes:** Es la base para las "Consultas Avanzadas SQL" (Clase 10 y 11), donde se explorarán funciones, agregaciones, `JOIN`s más complejos y subconsultas. También es el punto de partida para la "Programación en Base de Datos con PL/SQL" (Clase 12 y 13), donde estas sentencias DML se integrarán en bloques de código procedurales.

---
**Nota:** El contenido de esta clase ha sido inferido del título del curso y conocimientos generales sobre la materia, dado que el archivo `.ppt` original no pudo ser procesado directamente.
