## INSERT y SELECT en MySQL - Ejemplos completos y explicacion

> **Analogia:** Imagina que tenes un formulario de registro (INSERT INTO). Lo llenas con tus datos y lo envias. Luego queres ver todos los formularios recibidos (SELECT *). INSERT es como llenar formularios, SELECT es como leerlos. El orden importa: primero llenas, despues lees.

> **IMPORTANTE:** Este archivo asume que ya ejecutaste `create-drop-db-table.md` y `alter-table.md`. Si no los ejecutaste primero, las tablas no existiran y recibiras errores al intentar insertar datos.

---

### 1. Ver la estructura de las tablas

```sql
DESCRIBE users;
DESCRIBE products;
DESCRIBE orders;
```

> `DESCRIBE` muestra la estructura de cada tabla: columnas, tipos de datos, claves primarias y restricciones. Es util para confirmar los nombres de las columnas antes de hacer un `INSERT`.

#### MySQL vs PostgreSQL

```sql
-- MySQL
DESCRIBE users;

-- PostgreSQL: usa \d en psql o information_schema
\d users
```

---

### 2. Insertar registros en la tabla `users`

```sql
INSERT INTO users (name, email, password, cellphone)
VALUES
('Sergie Code', 'info@sergiecode.com', 'ABCabc123,.-', '+44789456123'),
('Ricardo Darin', 'ricardo@darin.com', 'elsecretodetusojos', '+11978954132'),
('Jenna Ortega', 'wednesday@addams.com', 'merlinamiercoles', '+349188646486');
```

> Se insertan tres registros con nombre, email, contrasena y celular.
> El formato es `INSERT INTO <tabla> (columnas) VALUES (valores)`. Podes agregar varios registros en una sola sentencia separando las filas con comas.

> **Tip del Profesor:** Siempre especifica las columnas explicitamente en el `INSERT`. No uses `INSERT INTO users VALUES (...)` sin listar columnas, porque si la tabla cambia, tu consulta fallara.

#### MySQL vs PostgreSQL

```sql
-- MySQL
INSERT INTO users (name, email, password, cellphone)
VALUES ('Sergie Code', 'info@sergiecode.com', 'ABCabc123,.-', '+44789456123');

-- PostgreSQL: mismo sintaxis, pero tambien soporta RETURNING
INSERT INTO users (name, email, password, cellphone)
VALUES ('Sergie Code', 'info@sergiecode.com', 'ABCabc123,.-', '+44789456123')
RETURNING id;
```

> **MySQL vs PostgreSQL:** PostgreSQL ofrece la clausula `RETURNING` que devuelve los datos insertados (como el `id` generado) inmediatamente despues del INSERT. MySQL no tiene esto nativamente; necesitas un `SELECT LAST_INSERT_ID()` separado.

---

### 3. Insertar registros en la tabla `products`

```sql
INSERT INTO products (name, description, price, stock)
VALUES
('Notebook', 'Sirve para programar', 1000.05, 1),
('Mouse', NULL, 5.50, 10),
('Keyboard', NULL, 5.50, NULL);
```

> Crea tres productos distintos.
> Se puede usar `NULL` para valores desconocidos o no requeridos (por ejemplo, stock no definido).

> **Tip del Profesor:** Diferencia entre `NULL` y un valor vacio. `NULL` significa "no tiene valor". Un campo `VARCHAR` con `''` (cadena vacia) es diferente a `NULL`. En tu codigo, maneja ambos casos.

---

### 4. Insertar otro producto con menos columnas

```sql
INSERT INTO products (name, description, price)
VALUES
('Microfono', 'Calidad para Streaming', 305.10);
```

> Podes omitir columnas opcionales como `stock` siempre que la tabla lo permita (por ejemplo, si esa columna acepta `NULL` o tiene un valor por defecto).

> **Tip del Profesor:** Si una columna tiene `DEFAULT 0` y no la mencionas en el INSERT, se usara 0. Si no tiene DEFAULT ni NULL, el INSERT fallara. Siempre revisa la estructura antes de insertar.

---

### 5. Insertar registros en la tabla `orders`

```sql
INSERT INTO orders (user_id, product_id, quantity, total)
VALUES
(1,1,1,1000.05),
(2,2,1,5.50),
(3,4,2,610.20);
```

> Inserta tres pedidos en la tabla `orders`, relacionando usuarios y productos por sus IDs.
> Por ejemplo, el primer pedido indica que el usuario con ID 1 compro el producto con ID 1.

> **Tip del Profesor:** Las foreign keys validan que `user_id` y `product_id` existan. Si intentas insertar un pedido con `user_id = 99` y ese usuario no existe, MySQL devolvera un error de integridad referencial.

---

### 6. Consultar los registros insertados

```sql
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
```

> `SELECT *` muestra todos los registros de una tabla.
> Ideal para verificar que los datos se insertaron correctamente.

> **Tip del Profesor:** En produccion, evita `SELECT *`. Especifica solo las columnas que necesitas: `SELECT name, email FROM users`. Esto es mas eficiente y claro.

---

### 7. Listar todas las tablas existentes

```sql
SHOW TABLES;
```

> Muestra todas las tablas disponibles dentro de la base de datos seleccionada.

#### MySQL vs PostgreSQL

```sql
-- MySQL
SHOW TABLES;

-- PostgreSQL
\dt
```

---

### Errores comunes

> **Tip del Profesor:** Estos son los errores mas comunes al insertar datos:

1. **Violacion de NOT NULL** - Si una columna es `NOT NULL` y no la mencionas en el INSERT sin DEFAULT, el INSERT fallara.
2. **Violacion de UNIQUE** - Si intentas insertar un email que ya existe, recibiras un error de duplicado.
3. **Violacion de FOREIGN KEY** - Si el `user_id` o `product_id` no existe en la tabla referenciada, el INSERT fallara.
4. **Tipo de dato incorrecto** - Si pones texto en un campo INT, MySQL intentara convertirlo (y puede fallar).

#### PostgreSQL: ON CONFLICT

```sql
-- PostgreSQL: manejar duplicados gracefulmente
INSERT INTO users (name, email, password, cellphone)
VALUES ('Sergie Code', 'info@sergiecode.com', 'ABCabc123,.-', '+44789456123')
ON CONFLICT (email) DO UPDATE
SET name = EXCLUDED.name;

-- MySQL equivalente (usar INSERT ... ON DUPLICATE KEY UPDATE)
INSERT INTO users (name, email, password, cellphone)
VALUES ('Sergie Code', 'info@sergiecode.com', 'ABCabc123,.-', '+44789456123')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

> **MySQL vs PostgreSQL:** PostgreSQL usa `ON CONFLICT`, MySQL usa `ON DUPLICATE KEY UPDATE`. Ambos resuelven el mismo problema: que pasa si el registro ya existe. `ON CONFLICT` es mas flexible porque podes especificar que columna o constraint causa el conflicto.

---

### Resumen

Con `INSERT INTO` agregas datos a tus tablas y con `SELECT` podes visualizarlos. Estas operaciones son esenciales para poblar una base de datos y probar relaciones entre entidades (`users`, `products`, `orders`) en un sistema tipo e-commerce.

> **Tip del Profesor:** Siempre ejecuta los archivos en orden: `create-drop-db-table.md` primero, luego `alter-table.md`, y finalmente `insert-into-select.md`. Cada paso asume que el anterior se ejecuto correctamente.
