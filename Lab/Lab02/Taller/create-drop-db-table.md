## Esquema MySQL: Base de datos `ecommerce`

> **Analogia:** Crear una base de datos es como construir una casa. Los planos son tus tablas, las paredes son tus columnas, y las habitaciones son los registros. Cuando demolés la casa (DROP), todo se destruye. Cuando construís una nueva (CREATE), empezás desde cero.

Este archivo contiene las instrucciones para crear la base de datos `ecommerce` con sus tres tablas principales: `users`, `products` y `orders`.

> **IMPORTANTE:** Este archivo debe ejecutarse PRIMERO antes que `alter-table.md` e `insert-into-select.md`, ya que esas guías dependen de estas tablas existentes.

---

### 1. Crear y eliminar base de datos

```sql
-- Paso 1: Crear la base de datos
CREATE DATABASE ecommerce;

-- Paso 2: Seleccionarla para trabajar dentro
USE ecommerce;

-- Paso 3: (Opcional) Eliminar la base de datos para empezar de cero
-- ⚠️ SOLO USAR EN DESARROLLO - BORRA TODO
-- DROP DATABASE ecommerce;
```

* **CREATE DATABASE**: crea una nueva base de datos llamada `ecommerce`.
* **USE**: selecciona la base para comenzar a trabajar dentro de ella.
* **DROP DATABASE**: elimina completamente la base de datos (y todas sus tablas).

> **Tip del Profesor:** `DROP DATABASE` es destructivo e irreversible. En desarrollo sirve para reiniciar el entorno, pero **nunca** lo ejecutes en producción sin un backup. Comentalo o dejalo en un bloque separado.

#### MySQL vs PostgreSQL

```sql
-- MySQL
CREATE DATABASE ecommerce;
USE ecommerce;

-- PostgreSQL (no tiene USE, usás el nombre de la BD en la conexión)
CREATE DATABASE ecommerce;
-- En PostgreSQL te conectás directamente a la BD desde el cliente
```

> **MySQL vs PostgreSQL:** En PostgreSQL no existe `USE`. Te conectás directamente a la base de datos desde tu cliente (TablePlus, DBeaver, psql). Desde la línea de comandos: `psql -U postgres -d ecommerce`.

---

### 2. Tabla `users`

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255),
    created_at DATE DEFAULT (CURRENT_DATE)
);
```

**Explicación:**

* `id INT AUTO_INCREMENT PRIMARY KEY`: genera un ID numérico único automáticamente.
* `name VARCHAR(100) NOT NULL`: nombre obligatorio, máximo 100 caracteres.
* `email VARCHAR(150) UNIQUE NOT NULL`: correo único, no puede repetirse ni ser nulo.
* `password VARCHAR(255)`: campo opcional (por ejemplo, hash de contraseña).
* `created_at DATE DEFAULT (CURRENT_DATE)`: guarda la fecha de creación por defecto.

#### MySQL vs PostgreSQL

```sql
-- PostgreSQL: SERIAL reemplaza AUTO_INCREMENT
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255),
    created_at DATE DEFAULT CURRENT_DATE
);
```

> **MySQL vs PostgreSQL:** En MySQL usás `AUTO_INCREMENT`, en PostgreSQL usás `SERIAL` (o `GENERATED ALWAYS AS IDENTITY` en versiones recientes). Ambos logran lo mismo: un ID que se genera solo.

---

### 3. Tabla `products`

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) CHECK (price > 0),
    stock INT DEFAULT 0,
    created_at DATE DEFAULT (CURRENT_DATE)
);
```

**Explicación:**

* `description TEXT`: permite texto largo (descripciones de producto).
* `price DECIMAL(10,2) CHECK (price > 0)`: precio con dos decimales, debe ser mayor que 0.
* `stock INT DEFAULT 0`: cantidad disponible, con valor inicial 0.

> **Tip del Profesor:** El tipo `DECIMAL(10,2)` guarda números exactos, ideal para precios. Nunca uses `FLOAT` o `DOUBLE` para dinero: redondea mal por ser valores aproximados.

#### MySQL vs PostgreSQL

```sql
-- PostgreSQL: mismo resultado
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) CHECK (price > 0),
    stock INT DEFAULT 0,
    created_at DATE DEFAULT CURRENT_DATE
);
```

> **MySQL vs PostgreSQL:** En PostgreSQL, `TEXT` es un tipo propio (no se diferencia de `VARCHAR` en rendimiento). En MySQL, `TEXT` y `VARCHAR` tienen diferencias sutiles en límites y rendimiento.

---

### 4. Tabla `orders`

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    total DECIMAL(10,2) CHECK (total > 0),
    order_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Explicación:**

* `user_id` y `product_id`: identifican al usuario y al producto relacionado.
* `FOREIGN KEY (...) REFERENCES ...`: crea relaciones entre tablas.
* `quantity` y `total`: usan `CHECK` para validar valores positivos.
* `order_date`: fecha del pedido (por defecto, la actual).

> **Tip del Profesor:** Las claves foráneas aseguran integridad referencial: no podés crear un pedido para un usuario o producto que no existe. Sin embargo, cuidado al eliminar registros padre (users/products) que tengan pedidos asociados.

#### MySQL vs PostgreSQL

```sql
-- PostgreSQL: mismo resultado, misma lógica
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    total DECIMAL(10,2) CHECK (total > 0),
    order_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

### 5. Verificar tablas creadas

```sql
SHOW TABLES;
```

En PostgreSQL:
```sql
-- Desde psql
\dt

-- O con SQL estándar
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

---

### Resumen

* Se crean tres tablas relacionadas: `users`, `products`, `orders`.
* Se aplican constraints y atributos comunes: `PRIMARY KEY`, `AUTO_INCREMENT`, `DEFAULT`, `CHECK`, `FOREIGN KEY`.
* Representa un mini modelo E-commerce completo y funcional.

> **Tip del Profesor:** Antes de crear tablas, pensá en el modelo: ¿qué entidades tenés? ¿Cómo se relacionan? Esto se llama **modelado de datos** y es la base de todo buen diseño de base de datos.
