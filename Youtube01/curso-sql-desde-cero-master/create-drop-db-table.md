## 🐬 Esquema MySQL: Base de datos `ecommerce`

---

```sql


CREATE DATABASE ecommerce;
USE ecommerce;
DROP DATABASE ecommerce;

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR (150) UNIQUE NOT NULL,
	password VARCHAR(255),
	created_at DATE DEFAULT (CURRENT_DATE)
)

CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	price DECIMAL(10,2) CHECK (price > 0),
	stock INT DEFAULT 0,
	created_at DATE DEFAULT (CURRENT_DATE)
)

CREATE TABLE orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	product_id INT NOT NULL,
	quantity INT DEFAULT 1 CHECK (quantity > 0),
	total DECIMAL(10,2) CHECK (total > 0),
	order_date DATE DEFAULT (CURRENT_DATE),
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (product_id) REFERENCES products(id)
)

SHOW TABLES;
```

---

### 📦 Crear y eliminar base de datos

```sql
CREATE DATABASE ecommerce;
USE ecommerce;
DROP DATABASE ecommerce;
```

* **CREATE DATABASE**: crea una nueva base de datos llamada `ecommerce`.
* **USE**: selecciona la base para comenzar a trabajar dentro de ella.
* **DROP DATABASE**: elimina completamente la base de datos (y todas sus tablas).

> ⚠️ *Usar DROP DATABASE borra todo. Ideal para tests o reiniciar el entorno, pero no en producción.*

---

### 👤 Tabla `users`

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

---

### 🛒 Tabla `products`

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

> 💡 *El tipo `DECIMAL(10,2)` guarda números exactos, ideal para precios.*

---

### 🧾 Tabla `orders`

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

> 🔗 *Las claves foráneas aseguran integridad referencial entre users → orders y products → orders.*

---

### 📋 Ver tablas creadas

```sql
SHOW TABLES;
```

Muestra la lista de tablas dentro de la base `ecommerce`.

---

✅ **Resumen:**

* Se crean tres tablas relacionadas: `users`, `products`, `orders`.
* Se aplican constraints y atributos comunes: `PRIMARY KEY`, `AUTO_INCREMENT`, `DEFAULT`, `CHECK`, `FOREIGN KEY`.
* Representa un mini modelo E-commerce completo y funcional en MySQL.
