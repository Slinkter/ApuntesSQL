# Curso de SQL desde Cero

## Link al video: 
https://youtu.be/Fca_kWJJXvo


## Índice de secciones:
1. [Instalaciones necesarias](instalaciones-necesarias.md)
2. [Crear y eliminar db y tablas](create-drop-db-table.md)
3. [Alter table](alter-table.md)
4. [Insertar información](insert-into-select.md)
5. [Actualizar, eliminar y truncar tablas](update-delete-truncate.md)
6. [Select (where, order by, etc)](select-where-order.md)
7. [Funciones de agregación](funciones-agregacion.md)
8. [Join e inner join](inner-join.md)
9. [Left & Right Join](left-right-join.md)
10. [Subconsultas, group by, having](subconsultas-group-having-coalesce.md)
11. [Buenas prácticas](buenas-practicas.md)

## Ejemplos realistas:
- [Ejemplo Cine](ejemplo1-cine.sql)
- [Ejemplo Videojuegos](ejemplo2-videojuegos.sql)
- [Ejemplo Restaurants](ejemplo3-restaurants.sql)

## Guías con imágenes:
- [Guía paso a paso](Guia/)
  - [Imagen 1](Guia/01.jpg)
  - [Imagen 2](Guia/02.jpg)
  - [Imagen 3](Guia/03.jpg)
  - [Imagen 4](Guia/04.jpg)
  - [Imagen 5](Guia/05.jpg)
  - [Imagen 6](Guia/06.jpg)
  - [Imagen 7](Guia/07.jpg)

## Cheatsheet Join:
- [Tipos de Join](Tipos-Join/)
  - [Join Diagram 1](Tipos-Join/01.jpg)
  - [Join Diagram 2](Tipos-Join/02.jpg)
  - [Join Diagram 3](Tipos-Join/03.jpg)
  - [Join Diagram 4](Tipos-Join/04.jpg)

## Docker Compose ejemplos:
- [MySQL sin variable de entorno](docker-compose/MySQL/docker-compose.yaml)
- [MySQL con variable de entorno](docker-compose/MySQLenv/docker-compose.yaml)
- [PostgreSQL sin variable de entorno](docker-compose/Postgres/docker-compose.yaml)
- [PostgreSQL con variable de entorno](docker-compose/Postgresenv/docker-compose.yaml)

## Familia de comandos SQL

| Tipo    | Nombre completo            | Qué hace                                          | Ejemplo típico                  |
| ------- | -------------------------- | ------------------------------------------------- | ------------------------------- |
| **DDL** | Data Definition Language   | Define estructura (tablas, columnas, constraints) | `CREATE TABLE`, `ALTER`, `DROP` |
| **DML** | Data Manipulation Language | Manipula datos (insertar, modificar, borrar)      | `INSERT`, `UPDATE`, `DELETE`    |
| **DQL** | Data Query Language        | Consulta datos                                    | `SELECT`                        |
| **DCL** | Data Control Language      | Gestiona permisos y accesos                       | `GRANT`, `REVOKE`               |

## Tipo de datos más importantes

| Tipo                | Uso típico            | Ejemplo                  |
| ------------------- | --------------------- | ------------------------ |
| `INT`               | números enteros       | cantidad, id             |
| `DECIMAL(10,2)`     | números con decimales | precio, saldo            |
| `VARCHAR(n)`        | texto corto           | nombre, email            |
| `TEXT`              | texto largo           | descripción, comentarios |
| `DATE` / `DATETIME` | fechas y tiempos      | fecha de registro        |
| `BOOLEAN`           | valores lógicos       | activo/inactivo          |

## Constraints (limitaciones)

| Constraint    | Función                       | Ejemplo                                      |
| ------------- | ----------------------------- | -------------------------------------------- |
| `NOT NULL`    | Obliga a tener un valor       | `email VARCHAR(150) NOT NULL`                |
| `DEFAULT`     | Valor por defecto             | `is_active BOOLEAN DEFAULT TRUE`             |
| `UNIQUE`      | No permite valores duplicados | `email UNIQUE`                               |
| `CHECK`       | Valida condiciones            | `CHECK (price > 0)`                          |
| `FOREIGN KEY` | Vincula tablas                | `FOREIGN KEY (user_id) REFERENCES users(id)` |

## Atributos de Columna 

| Atributo                         | Función                                                                                                                                                    | Ejemplo                                                             |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **AUTO_INCREMENT**               | Genera automáticamente un número consecutivo por cada fila nueva. Solo puede haber uno por tabla y debe estar asociado a una **PRIMARY KEY** o **UNIQUE**. | `id INT AUTO_INCREMENT PRIMARY KEY`                                 |
| **DEFAULT**                      | Asigna un valor automático si no se especifica otro. Puede usar valores fijos o funciones.                                                                 | `created_at DATE DEFAULT (CURRENT_DATE)`                            |
| **COMMENT**                      | Agrega una descripción interna sobre la columna (no afecta los datos).                                                                                     | `price DECIMAL(10,2) COMMENT 'Precio en USD'`                       |
| **GENERATED / STORED / VIRTUAL** | Crea una columna calculada a partir de otras. En MySQL 5.7+ se usa `GENERATED ALWAYS AS (...)`.                                                            | `total DECIMAL(10,2) GENERATED ALWAYS AS (price * quantity) STORED` |
| **CHARACTER SET / COLLATE**      | Define la codificación y reglas de comparación para texto.                                                                                                 | `name VARCHAR(100) CHARACTER SET utf8mb4`                           |
| **ZEROFILL**                     | Rellena con ceros a la izquierda los números enteros. (poco usado hoy)                                                                                     | `code INT(5) ZEROFILL`                                              |


## ALTER TABLE

| Operación           | Descripción                                                              | Ejemplo                                                                                 |
| ------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **ADD COLUMN**      | Agrega una nueva columna.                                                | `ALTER TABLE users ADD COLUMN age INT;`                                                 |
| **DROP COLUMN**     | Elimina una columna existente.                                           | `ALTER TABLE users DROP COLUMN age;`                                                    |
| **RENAME COLUMN**   | Cambia el nombre de una columna.                                         | `ALTER TABLE users RENAME COLUMN name TO full_name;`                                    |
| **MODIFY COLUMN**   | Cambia el tipo o las propiedades de una columna (sin cambiar el nombre). | `ALTER TABLE users MODIFY COLUMN full_name VARCHAR(150) NOT NULL;`                      |
| **ADD CONSTRAINT**  | Crea una nueva constraint (clave foránea, única, etc.).                  | `ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);` |
| **DROP CONSTRAINT** | Elimina una constraint existente (MySQL 8+).                             | `ALTER TABLE orders DROP CONSTRAINT fk_user;`                                           |
| **RENAME TO**       | Cambia el nombre de la tabla.                                            | `ALTER TABLE users RENAME TO customers;`                                                |
| **ADD INDEX**       | Agrega un índice para optimizar consultas.                               | `ALTER TABLE users ADD INDEX idx_email (email);`                                        |
| **DROP INDEX**      | Elimina un índice existente.                                             | `ALTER TABLE users DROP INDEX idx_email;`                                               |
| **ADD CHECK**       | Agrega una validación lógica sobre los datos.                            | `ALTER TABLE products ADD CONSTRAINT chk_price CHECK (price > 0);`                      |
| **DROP CHECK**      | Quita una validación `CHECK`.                                            | `ALTER TABLE products DROP CHECK chk_price;`                                            |

## Operadores más usados

| Operador      | Significado          | Ejemplo                               |
| ------------- | -------------------- | ------------------------------------- |
| `=`           | Igual                | `WHERE name = 'Juan'`                 |
| `<`           | Menor que            | `WHERE price < 1000`                  |
| `>`           | Mayor que            | `WHERE stock > 10`                    |
| `<=`          | Menor o igual        | `WHERE stock <= 5`                    |
| `>=`          | Mayor o igual        | `WHERE price >= 20000`                |
| `<>` o `!=`   | Distinto             | `WHERE id <> 1`                       |
| `BETWEEN`     | Entre un rango       | `WHERE price BETWEEN 10000 AND 50000` |
| `LIKE`        | Coincidencia parcial | `WHERE name LIKE '%notebook%'`        |
| `IN`          | En un conjunto       | `WHERE id IN (1, 2, 3)`               |
| `IS NULL`     | Valor nulo           | `WHERE phone IS NULL`                 |
| `IS NOT NULL` | Valor no nulo        | `WHERE phone IS NOT NULL`             |

## FUNCIONES BASICAS

| Función   | Descripción            | Ejemplo      |
| --------- | ---------------------- | ------------ |
| `COUNT()` | Cuenta registros       | `COUNT(*)`   |
| `SUM()`   | Suma valores numéricos | `SUM(price)` |
| `AVG()`   | Promedio               | `AVG(price)` |
| `MIN()`   | Valor mínimo           | `MIN(price)` |
| `MAX()`   | Valor máximo           | `MAX(price)` |


## JOINS

| Forma completa        | Forma abreviada |
|-----------------------|-----------------|
| INNER JOIN            | JOIN            |
| LEFT OUTER JOIN       | LEFT JOIN       |
| RIGHT OUTER JOIN      | RIGHT JOIN      |


## POSTGRESQL

| Parámetro             | Valor            |
| --------------------- | ---------------- |
| **Puerto**            | 5432             |
| **Usuario**           | postgres         |
| **Contraseña**        | *(sin password)* |

## MYSQL

| Parámetro      | Valor            |
| -------------- | ---------------- |
| **Puerto**     | 3306             |
| **Usuario**    | root             |
| **Contraseña** | *(sin password)* |






