## Estructura y diseno de la base de datos

---

## Analogia

Disenar una base de datos es como construir una casa. Los cimientos (estructura de tablas) deben estar bien planificados antes de poner los muebles (datos). Una mala decision al inicio, como usar el tipo de dato incorrecto en una columna, puede obligarte a demoler paredes mas adelante. Asi como un arquitecto planifica los espacios antes de construir, un buen disenador de bases de datos define tipos de datos, restricciones y relaciones antes de insertar el primer registro.

---

## Definicion

Este capitulo reune las **mejores practicas** para el diseno de esquemas en bases de datos relacionales. Algunas son universales (aplican a MySQL, PostgreSQL y otros motores), otras son especificas de MySQL o PostgreSQL. Se indica claramente cuando una practica es particular de un motor.

---

### Tabla de referencia rapida: tipos de campo y convenciones

| Caso / Campo tipico | Convencion recomendada | Motivo / Buenas practicas | Motor |
|---|---|---|---|
| **ID principal** | `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY` (MySQL) | Identificador unico y auto incremental. `UNSIGNED` evita negativos y amplia el rango. | MySQL |
| **ID principal** | `SERIAL PRIMARY KEY` o `BIGSERIAL PRIMARY KEY` (PostgreSQL) | `SERIAL` es equivalente a `INT NOT NULL DEFAULT nextval(...)`. `BIGSERIAL` para tablas que superaran 2B filas. | PostgreSQL |
| **UUID como ID** | `UUID DEFAULT gen_random_uuid() PRIMARY KEY` | Ideal para sistemas distribuidos o sincronizacion offline. PostgreSQL lo soporta nativamente; en MySQL requiere funcion UUID(). | Ambos |
| **Campos obligatorios** | `NOT NULL` | Obliga a completar datos esenciales y evita registros incompletos. | Universal |
| **Email de usuario** | `VARCHAR(255) UNIQUE NOT NULL` | Evita duplicados y respeta la longitud maxima estandar. | Universal |
| **Contrasena** | `password VARCHAR(255) NOT NULL` | Soporta hashes (`bcrypt`, `argon2`, etc.). Nunca guardar texto plano. | Universal |
| **Booleanos** | `is_active BOOLEAN DEFAULT TRUE` | Claros, semanticos y con valores por defecto logicos. En MySQL, `BOOLEAN` es alias de `TINYINT(1)`. | Ambos |
| **Fechas de creacion y actualizacion** | `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`, `updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Auditoria automatica de cambios. En PostgreSQL usa `TIMESTAMP`; en MySQL, `DATETIME` o `TIMESTAMP`. | Ambos |
| **Campos numericos sin negativos** | `UNSIGNED` (MySQL) o `CHECK (columna >= 0)` (PostgreSQL) | MySQL permite `UNSIGNED` que evita negativos y amplia el rango positivo. PostgreSQL no tiene `UNSIGNED`; usa `CHECK` o dominio personalizado. | Depende |
| **Foreign Keys** | `FOREIGN KEY (campo_id) REFERENCES otra_tabla(id)` | Mantiene integridad referencial. `ON DELETE` y `ON UPDATE` definen el comportamiento en cascada. | Universal |
| **Campos de estado o tipo** | `ENUM('active','inactive','pending')` (MySQL) o `VARCHAR + CHECK` (PostgreSQL) | MySQL soporta `ENUM` nativo. PostgreSQL recomienda `VARCHAR` con `CHECK IN (...)` o tabla de referencia para conjuntos que puedan crecer. | Depende |
| **Campos de texto largos** | `TEXT` o `LONGTEXT` | Permite textos amplios sin limite fijo. | Universal |
| **Campos opcionales** | `NULL` permitido | Flexibilidad cuando no todos los registros completan esos campos. | Universal |
| **Borrado logico** | `deleted BOOLEAN DEFAULT FALSE` o `deleted_at TIMESTAMP NULL` | Permite mantener registros eliminados sin perder historial. | Universal |
| **Nombres de tabla y columna** | `snake_case`, sin mayusculas, acentos ni espacios | Uniformidad y compatibilidad multiplataforma. En PostgreSQL, los nombres se convierten a minusculas automaticamente. | Universal |
| **Charset / Collation** | `utf8mb4_unicode_ci` (MySQL) o `UTF8` (PostgreSQL) | MySQL requiere `utf8mb4` para soporte completo de Unicode (emojis). PostgreSQL usa `UTF8` por defecto. | Depende |
| **Storage Engine** | `ENGINE=InnoDB` (MySQL) o (no aplica en PostgreSQL) | InnoDB soporta transacciones y claves foraneas. PostgreSQL usa un solo engine (no configurable). | MySQL only |

---

> **MySQL vs PostgreSQL sobre UNSIGNED:**
> En MySQL, `UNSIGNED` es una caracteristica del tipo numerico que duplica el rango positivo a cambio de no permitir negativos. PostgreSQL no tiene `UNSIGNED`; en su lugar se usa `CHECK (columna >= 0)`. La ventaja de `CHECK` es que es estandar SQL y portatil entre motores.

> **MySQL vs PostgreSQL sobre ENUM:**
> MySQL tiene `ENUM` como tipo de dato nativo, eficiente en almacenamiento pero rigido: agregar un nuevo valor requiere `ALTER TABLE`. PostgreSQL no tiene `ENUM` nativo (aunque puede crearse con `CREATE TYPE`), y la recomendacion general es usar `VARCHAR` con `CHECK IN (...)` o, mejor aun, una tabla de referencia con clave foranea. La tabla de referencia es la opcion mas flexible y escalable.

---

## 1. Entidades de personas / usuarios

### Campos tipicos y por que se definen asi

```sql
-- Nombre real de la persona
name VARCHAR(100) NOT NULL
```

* Siempre `NOT NULL` porque una persona sin nombre no tiene sentido logico.
* 100 caracteres suele ser suficiente incluso con nombres compuestos.

```sql
-- Apellido de la persona
surname VARCHAR(100) NOT NULL
```

* Mismo criterio.
* No se recomienda unir nombre y apellido en un solo campo (dificulta busquedas y ordenamiento).

```sql
-- Correo electronico, usado como identificador de login
email VARCHAR(255) UNIQUE NOT NULL
```

* `UNIQUE` para evitar duplicados de cuentas.
* `NOT NULL` porque el correo es parte del login o contacto.
* `255` es el limite maximo permitido por estandar.

```sql
-- Hash de contrasena (nunca texto plano)
password VARCHAR(255) NOT NULL
```

* Espacio suficiente para hashes (`bcrypt`, `argon2`, `bcrypt` genera 60 chars, `argon2` hasta 128).
* Nunca se guarda texto plano.
* `NOT NULL` porque el usuario debe tener credenciales validas.

```sql
-- Estado activo/inactivo
is_active BOOLEAN DEFAULT TRUE
```

* Permite desactivar un usuario sin borrarlo.
* `DEFAULT TRUE` evita tener que definirlo al crear.

```sql
-- Auditoria de creacion y modificacion
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

* Auditoria automatica, estandar en cualquier tabla que se modifique.
* En PostgreSQL, usa `TIMESTAMP` (sin zona horaria) o `TIMESTAMPTZ` (con zona horaria) segun la necesidad.

```sql
-- Ultimo inicio de sesion (opcional)
last_login TIMESTAMP NULL
```

* Se deja `NULL` hasta que el usuario realmente inicie sesion.

```sql
-- Verificacion de correo electronico
email_verified_at TIMESTAMP NULL
```

* Fecha del momento en que el usuario confirmo su correo.
* `NULL` significa "pendiente de verificacion".

---

## 2. Clientes / empresas

```sql
company_name VARCHAR(255) NOT NULL
```

* Siempre requerido: sin nombre no hay entidad comercial.

```sql
tax_id VARCHAR(30) UNIQUE NOT NULL
```

* CUIT/CUIL/RUC o similar.
* `UNIQUE` porque es identificador fiscal unico.

```sql
contact_email VARCHAR(255) NULL
```

* A veces no tienen correo registrado, por eso `NULL` permitido.

```sql
phone VARCHAR(20) NULL
```

* `VARCHAR` (no numerico) porque puede tener `+`, `-`, espacios y parentesis.

```sql
address TEXT NULL
```

* Se usa `TEXT` si puede ser largo (calles, referencias, etc.).

```sql
is_client BOOLEAN DEFAULT TRUE
```

* Permite usar la misma tabla para contactos potenciales (`FALSE`) o clientes reales (`TRUE`).

---

## 3. Profesores, alumnos o empleados

```sql
employee_number VARCHAR(20) UNIQUE NOT NULL
```

* Codigo interno o legajo.
* `UNIQUE` para evitar duplicados.

```sql
hire_date DATE NOT NULL
```

* Fecha obligatoria: indica antiguedad laboral.

```sql
birth_date DATE NULL
```

* `NULL` si no se conoce o no es obligatorio.

```sql
salary DECIMAL(10,2) NOT NULL CHECK (salary >= 0)
```

* En MySQL: `DECIMAL(10,2) UNSIGNED NOT NULL` (MySQL permite UNSIGNED en decimales).
* En PostgreSQL: `DECIMAL(10,2) NOT NULL CHECK (salary >= 0)`.
* `DECIMAL` para evitar errores de redondeo (nunca uses `FLOAT` para dinero).

```sql
is_full_time BOOLEAN DEFAULT FALSE
```

* Permite distinguir contratos o tipo de trabajo.

```sql
department_id INT NOT NULL,
FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
```

* Si se elimina el departamento, no queremos borrar al empleado, solo dejarlo sin asignacion.
* **Tip:** `ON DELETE SET NULL` requiere que `department_id` permita `NULL`.

---

## 4. Productos / inventario

```sql
name VARCHAR(150) NOT NULL
```

* `NOT NULL` porque un producto sin nombre no tiene sentido.

```sql
sku VARCHAR(50) UNIQUE NOT NULL
```

* Codigo unico por producto (Stock Keeping Unit).
* Usa `UNIQUE` para garantizar que no haya dos productos con el mismo SKU.

```sql
price DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (price >= 0)
```

* En MySQL: `UNSIGNED NOT NULL DEFAULT 0.00`.
* En PostgreSQL: `NOT NULL DEFAULT 0.00 CHECK (price >= 0)`.
* `DEFAULT 0.00` util para evitar errores si no se define.

```sql
stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0)
```

* En MySQL: `INT UNSIGNED NOT NULL DEFAULT 0`.
* En PostgreSQL: `INT NOT NULL DEFAULT 0 CHECK (stock >= 0)`.
* `DEFAULT 0` inicializa correctamente el inventario.

```sql
is_available BOOLEAN DEFAULT TRUE
```

* Permite marcar un producto como descontinuado sin borrarlo.

```sql
category_id INT NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
```

* Si se borra una categoria, se eliminan sus productos.
* Ideal cuando los productos dependen completamente de esa categoria.

---

## 5. Ventas / pedidos

```sql
order_number VARCHAR(50) UNIQUE NOT NULL
```

* Numero de pedido unico, util para trazabilidad.

```sql
user_id INT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

* Si se elimina un usuario, tambien sus pedidos (dependencia directa).

```sql
total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0)
```

* Monto total, no negativo.

```sql
status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled'))
```

* En MySQL se usa frecuentemente `ENUM('pending','paid','shipped','cancelled')`.
* En PostgreSQL, la recomendacion es `VARCHAR` con `CHECK` o una tabla de referencia.
* Si el conjunto de estados es fijo y no cambiara, `ENUM` (MySQL) es eficiente. Si puede crecer (ej. agregar "refunded"), usa una tabla de referencia en ambos motores.

```sql
paid_at TIMESTAMP NULL
```

* `NULL` hasta que el pago se confirme.

---

## 6. Roles y permisos

```sql
name VARCHAR(50) UNIQUE NOT NULL
```

* Nombre unico: "admin", "editor", "user".

```sql
description TEXT NULL
```

* Descripcion opcional.

```sql
is_default BOOLEAN DEFAULT FALSE
```

* Indica si es el rol asignado por defecto a nuevos usuarios.

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

* Auditoria de creacion.

**Tabla intermedia (usuarios <-> roles):**

```sql
user_id INT NOT NULL,
role_id INT NOT NULL,
PRIMARY KEY (user_id, role_id),
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
```

* Clave compuesta para evitar duplicados.
* `ON DELETE CASCADE` para mantener integridad: si se elimina un usuario o un rol, la relacion se elimina automaticamente.

---

## 7. Auditoria y logica de negocio

```sql
deleted BOOLEAN DEFAULT FALSE
```

* "Soft delete": permite marcar registros como eliminados sin perder el historial.

```sql
deleted_at TIMESTAMP NULL
```

* Guarda cuando fue eliminado logicamente.

```sql
created_by INT NULL,
updated_by INT NULL,
FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
```

* Guarda quien creo o modifico cada registro.

```sql
version INT DEFAULT 1
```

* Para sistemas con control de versiones de datos (documentos, contratos, etc.).

---

## 8. Otras practicas generales

### Universales (aplican a cualquier motor)

* **Usar `InnoDB` en MySQL** o el motor por defecto en PostgreSQL: soporta transacciones y foreign keys.
* **Definir `utf8mb4` en MySQL** (o `UTF8` en PostgreSQL): soporte total de Unicode.
* **Usar `snake_case`** para nombres (`user_profiles`, no `UserProfiles`). En PostgreSQL, los nombres se convierten a minusculas automaticamente; si usas mayusculas, debes entrecomillarlos siempre.
* **Evitar `NULL` en campos booleanos**: usar `DEFAULT FALSE` o `DEFAULT TRUE`.
* **Prefijos claros**: `user_id`, `order_id`, `product_id` -- mas legible en joins.
* **Evitar tipos `FLOAT` o `DOUBLE`** para dinero o precision contable. Usa `DECIMAL` siempre.
* **Evitar `TEXT` para campos que se filtran frecuentemente** (no indexables facilmente en MySQL; en PostgreSQL se puede crear indice sobre TEXT).
* **Siempre indexar foreign keys** para performance en joins.

### MySQL-specific

* **Usar `UNSIGNED`** en columnas numericas que nunca seran negativas (edad, precio, stock).
* **`AUTO_INCREMENT`**: el estandar para IDs auto-incrementales en MySQL. En PostgreSQL se usa `SERIAL` o `IDENTITY`.
* **`ENUM`**: eficiente para conjuntos fijos y pequenos. Si el conjunto puede crecer, evitalo y usa tabla de referencia.

### PostgreSQL-specific

* **`SERIAL` / `BIGSERIAL`**: equivalentes a `AUTO_INCREMENT`. `BIGSERIAL` para tablas que superaran 2^31 filas.
* **`UUID`**: ideal para sistemas distribuidos. PostgreSQL tiene funciones nativas como `gen_random_uuid()`.
* **Indices parciales**: `CREATE INDEX ON users (email) WHERE is_active = TRUE;` -- solo indexa filas que cumplen la condicion, ahorrando espacio y mejorando performance.
* **`CHECK`**: la alternativa portatil a `UNSIGNED` y `ENUM` de MySQL.

### Indexing strategy

* **Primary keys**: se indexan automaticamente.
* **Foreign keys**: debes indexarlas explicitamente en MySQL (InnoDB lo hace automaticamente en la FK, pero no siempre); en PostgreSQL tambien se recomienda crearlas.
* **Columnas de filtro frecuente**: columnas usadas en `WHERE` (ej. `status`, `email`, `customer_id`).
* **Indices compuestos**: para consultas con multiples condiciones en el WHERE (ej. `INDEX (status, created_at)`).
* **No sobre-indexar**: cada indice ralentiza `INSERT`, `UPDATE`, `DELETE`. Indexa solo lo que tus queries usan.

### Advertencia sobre ON DELETE CASCADE

```sql
-- USAR CON PRECAUCION: elimina en cascada
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

-- Alternativa mas segura
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
```

`ON DELETE CASCADE` es poderoso pero peligroso. Si alguien elimina un usuario, **todos sus pedidos, comentarios, evaluaciones y registros relacionados se borraran automaticamente**. En muchos sistemas, esto no es deseable (perderias historial de ventas, datos de auditoria, etc.).

**Alternativas recomendadas:**

| Comportamiento | Que hace | Uso tipico |
|---|---|---|
| `ON DELETE CASCADE` | Elimina las filas relacionadas | Datos que no tienen sentido sin el padre (ej. items de un pedido) |
| `ON DELETE SET NULL` | Pone NULL en la FK | El registro hijo sigue existiendo pero sin referencia (ej. empleado sin departamento) |
| `ON DELETE RESTRICT` | Impide eliminar si hay hijos | Datos que no deben perderse jamas (ej. no borrar un usuario con pedidos) |
| `ON DELETE NO ACTION` | Similar a RESTRICT | Estandar SQL, comportamiento similar |

---

### Tip del Profesor

- **Naming conventions:** La consistencia es mas importante que la eleccion especifica. Si eliges `snake_case`, usalo en todas las tablas, columnas, indices y constraints. Mezclar `snake_case`, `camelCase` y `PascalCase` en el mismo schema es una senal de diseno descuidado.
- **Normalizacion hasta 3FN:** Disena al menos hasta Tercera Forma Normal (3FN). La desnormalizacion solo se justifica por razones de rendimiento comprobadas, no por pereza.
- **Planificar para el crecimiento:** Un `INT` llega a ~2.1B filas. Parece mucho, pero en sistemas de logs, eventos o IoT se alcanza rapido. Considera `BIGINT` o `BIGSERIAL` para tablas que escalen.
- **PostgreSQL `IDENTITY` vs `SERIAL`:** Desde PostgreSQL 10, se recomienda `GENERATED BY DEFAULT AS IDENTITY` sobre `SERIAL`, porque cumple el estandar SQL y tiene mejor manejo de permisos. `SERIAL` funciona pero es considerado legacy.
- **Evitar el "enum antipattern":** Si defines un `ENUM` o `CHECK` con valores fijos y luego necesitas agregar uno nuevo, deberas hacer un `ALTER TABLE`. Para estados que cambian frecuentemente, prefiere una tabla de referencia con clave foranea.
- **Documenta tu esquema:** Manten un diccionario de datos (que significa cada tabla, cada columna, que valores puede tomar). Tu yo del futuro te lo agradecera cuando tengas que modificar el esquema 6 meses despues.
- **Prueba con datos realistas:** Al disenar, inserta miles de registros de prueba para verificar que los indices funcionan y que las queries no degradan. Un diseno que funciona bien con 10 filas puede colapsar con 10 millones.
