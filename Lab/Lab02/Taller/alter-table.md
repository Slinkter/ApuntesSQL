## ALTER TABLE en MySQL - Ejemplos practicos y explicacion

> **Analogia:** Imagina que alquilaste una casa (tu tabla) y ahora necesitás hacer reformas: agregar una habitación (ADD COLUMN), demoler un baño (DROP COLUMN), cambiar la puerta de lugar (RENAME COLUMN), o ampliar la cocina (MODIFY COLUMN). `ALTER TABLE` es tu herramienta de remodelación: modificás la estructura sin demolera toda la casa.

> **IMPORTANTE:** Este archivo asume que ya ejecutaste `create-drop-db-table.md` y que la base de datos `ecommerce` con la tabla `users` existe. Tambien asume que NO ejecutaste ningun archivo `DROP` intermedio.

> **Tip del Profesor:** Estos comandos se ejecutan en orden secuencial. Cada paso depende del anterior. Si saltás un paso o ejecutás un paso fuera de orden, recibirás errores porque las columnas o restricciones ya no existen.

---

### Esquema completo de ejecucion

```sql
-- PASO 1: Agregar columna phone
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- PASO 2: Renombrar phone a cellphone
ALTER TABLE users RENAME COLUMN phone TO cellphone;

-- PASO 3: Modificar el tipo de dato de cellphone
ALTER TABLE users MODIFY COLUMN cellphone VARCHAR(30) NOT NULL;

-- PASO 4: Agregar restriccion UNIQUE a cellphone
ALTER TABLE users ADD CONSTRAINT cellphone UNIQUE (cellphone);

-- PASO 5: Renombrar la tabla users a customers
ALTER TABLE users RENAME TO customers;

-- PASO 6: Verificar la estructura final
DESCRIBE customers;

-- PASO 7: Listar tablas
SHOW TABLES;
```

---

### 1. Agregar una columna

```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

> Agrega una nueva columna `phone` de tipo `VARCHAR(20)` a la tabla `users`.
> Este tipo de operacion es util cuando necesitas sumar un nuevo dato a tu modelo, sin perder la informacion existente.

#### MySQL vs PostgreSQL

```sql
-- MySQL
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- PostgreSQL
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- Mismo sintaxis
```

---

### 2. Renombrar una columna

```sql
ALTER TABLE users RENAME COLUMN phone TO cellphone;
```

> Cambia el nombre de la columna `phone` a `cellphone`.
> Ideal para mantener una convencion de nombres mas clara o consistente.

#### MySQL vs PostgreSQL

```sql
-- MySQL
ALTER TABLE users RENAME COLUMN phone TO cellphone;

-- PostgreSQL
ALTER TABLE users RENAME COLUMN phone TO cellphone;
-- Mismo sintaxis
```

---

### 3. Modificar el tipo de dato o restricciones de una columna

```sql
ALTER TABLE users MODIFY COLUMN cellphone VARCHAR(30) NOT NULL;
```

> Cambia las propiedades de la columna `cellphone`, estableciendo un nuevo tamano maximo (30 caracteres) y que no puede ser nula (`NOT NULL`).

#### MySQL vs PostgreSQL

```sql
-- MySQL: MODIFY COLUMN cambia todo de una
ALTER TABLE users MODIFY COLUMN cellphone VARCHAR(30) NOT NULL;

-- PostgreSQL: usa ALTER COLUMN para partes especificas
ALTER TABLE users ALTER COLUMN cellphone TYPE VARCHAR(30);
ALTER TABLE users ALTER COLUMN cellphone SET NOT NULL;

-- O en una sola linea (PostgreSQL 9+)
ALTER TABLE users
    ALTER COLUMN cellphone TYPE VARCHAR(30),
    ALTER COLUMN cellphone SET NOT NULL;
```

> **MySQL vs PostgreSQL:** MySQL usa `MODIFY COLUMN` para redefinir toda la columna de una vez. PostgreSQL separa `TYPE` (tipo de dato) y `SET NOT NULL` (restriccion). Son equivalentes en resultado.

> **Tip del Profesor:** En MySQL no existe `UNSIGNED` en PostgreSQL. Si usas `INT UNSIGNED` en MySQL, en PostgreSQL simplemente usas `INTEGER` o `INT`.

---

### 4. Agregar una restriccion UNIQUE

```sql
ALTER TABLE users ADD CONSTRAINT cellphone UNIQUE (cellphone);
```

> Crea una restriccion de unicidad sobre la columna `cellphone`.
> Esto garantiza que no haya dos usuarios con el mismo numero de celular.

#### MySQL vs PostgreSQL

```sql
-- MySQL
ALTER TABLE users ADD CONSTRAINT cellphone UNIQUE (cellphone);

-- PostgreSQL
ALTER TABLE users ADD CONSTRAINT cellphone UNIQUE (cellphone);
-- Mismo sintaxis
```

---

### 5. Renombrar una tabla

```sql
ALTER TABLE users RENAME TO customers;
```

> Cambia el nombre de la tabla `users` a `customers`.
> Muy comun cuando evolucionas tu modelo de datos o redefinis el dominio del sistema.

#### MySQL vs PostgreSQL

```sql
-- MySQL
ALTER TABLE users RENAME TO customers;

-- PostgreSQL: tambien funciona con ALTER TABLE
ALTER TABLE users RENAME TO customers;

-- O con RENAME TO directo (PostgreSQL)
ALTER TABLE users RENAME TO customers;
```

---

### 6. Consultar la estructura de las tablas

```sql
DESCRIBE customers;
```

> `DESCRIBE` muestra la estructura de la tabla: columnas, tipos de datos, claves primarias y restricciones.
> Sirve para verificar los cambios que hiciste con `ALTER TABLE`.

#### MySQL vs PostgreSQL

```sql
-- MySQL
DESCRIBE customers;

-- PostgreSQL: usa \d en psql o information_schema
\d customers

-- O con SQL estandar
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'customers';
```

---

### 7. Listar todas las tablas de la base de datos

```sql
SHOW TABLES;
```

> Devuelve una lista con todas las tablas existentes en la base de datos seleccionada.

#### MySQL vs PostgreSQL

```sql
-- MySQL
SHOW TABLES;

-- PostgreSQL: usa \dt en psql o information_schema
\dt

-- O con SQL estandar
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

---

### Errores comunes

> **Tip del Profesor:** Los errores mas comunes al usar `ALTER TABLE` son:

1. **Intentar modificar una columna que no existe** - Verifica con `DESCRIBE` antes de modificar.
2. **Ejecutar pasos fuera de orden** - Si renombraste `phone` a `cellphone`, despues no intentes modificar `phone`.
3. **Olvidar el tipo de dato en MODIFY** - En MySQL, `MODIFY COLUMN` requiere el tipo completo, no solo el nombre.
4. **Usar UNSIGNED en PostgreSQL** - PostgreSQL no soporta `UNSIGNED`. Usa rangos de CHECK o BIGINT.

---

### Resumen

`ALTER TABLE` es una herramienta esencial para la **evolucion de un esquema SQL**. Permite modificar la estructura de tus tablas sin perder los datos existentes y adaptarlas a nuevas necesidades del proyecto.

> **Tip del Profesor:** Siempre ejecuta los archivos en orden: `create-drop-db-table.md` primero, luego `alter-table.md`, y finalmente `insert-into-select.md`. Cada paso asume que el anterior se ejecuto correctamente.
