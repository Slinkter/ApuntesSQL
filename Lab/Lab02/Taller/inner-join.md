### INNER JOIN en MySQL -- Ejemplos practicos con explicacion

---

> **Orden de ejecucion recomendado:** Para seguir este ejercicio, ejecuta primero los archivos `create-drop-db-table.md`, `alter-table.md` e `insert-into-select.md` para crear y poblar las tablas `users`, `orders` y `products`.

> **Analogia:** Imagina que tienes dos listas: una de clientes y otra de pedidos. Cada pedido tiene el nombre del cliente que lo hizo. `INNER JOIN` es como juntar ambas listas y **quedarte solo con los pares que coinciden**. Si un cliente no tiene pedidos, no aparece. Si un pedido no tiene cliente valido, tampoco.

```
  Clientes           Pedidos
  +------+           +------+----------+
  | id   |           | id   | cliente_id |
  | A    |           | 1    | A          |  <-- coincide
  | B    |           | 2    | A          |  <-- coincide
  | C    |           | 3    | B          |  <-- coincide
  +------+           +------+----------+

  Resultado INNER JOIN:
  A - Pedido 1
  A - Pedido 2
  B - Pedido 3
  (C no aparece: no tiene pedidos)
```

---

```sql

SELECT users.name, orders.id, orders.total
FROM users
INNER JOIN orders
ON users.id = orders.user_id;

SELECT
u.name AS comprador,
o.id AS pedido,
o.total,
o.order_date AS fecha
FROM users AS u
INNER JOIN orders AS o
ON u.id = o.user_id;

SELECT
u.name AS comprador,
p.name AS producto,
o.quantity AS cantidad,
o.total
FROM users AS u
INNER JOIN orders AS o ON u.id = o.user_id
INNER JOIN products AS p ON p.id = o.product_id



```

---

### Definicion

El comando `INNER JOIN` se utiliza para **combinar datos de dos o mas tablas** en funcion de una relacion entre ellas, generalmente definida por una clave foranea (`FOREIGN KEY`). Es fundamental para trabajar con modelos relacionales y consultar informacion conectada.

> Solo aparecen las filas donde hay coincidencia en **ambas** tablas. Si una fila no tiene pareja en la otra tabla, queda excluida del resultado.

---

#### 1. Unir usuarios con sus pedidos

```sql
SELECT users.name, orders.id, orders.total
FROM users
INNER JOIN orders
ON users.id = orders.user_id;
```

> Este `INNER JOIN` relaciona la tabla `users` con `orders`.
>
> * `users.id` es la **clave primaria** en `users`.
> * `orders.user_id` es la **clave foranea** que apunta al usuario que hizo el pedido.
>
> El resultado muestra el nombre del usuario, el ID del pedido y el total correspondiente.

---

#### 2. Unir tablas usando alias y columnas renombradas

```sql
SELECT
  u.name AS comprador,
  o.id AS pedido,
  o.total,
  o.order_date AS fecha
FROM users AS u
INNER JOIN orders AS o
ON u.id = o.user_id;
```

> Los **alias** (`u` y `o`) simplifican la lectura del codigo y son muy utiles cuando se trabaja con varias tablas.
>
> * `AS comprador` renombra la columna en el resultado.
> * Se incluyen campos adicionales como la fecha del pedido (`order_date`).
>
> Este formato es mas legible y se usa comunmente en reportes o vistas.

---

#### 3. Unir tres tablas: usuarios, pedidos y productos

```sql
SELECT
  u.name AS comprador,
  p.name AS producto,
  o.quantity AS cantidad,
  o.total
FROM users AS u
INNER JOIN orders AS o ON u.id = o.user_id
INNER JOIN products AS p ON p.id = o.product_id;
```

> En esta consulta se combinan tres tablas relacionadas:
>
> * `users` -> contiene los clientes.
> * `orders` -> contiene los pedidos.
> * `products` -> contiene los productos comprados.
>
> El `INNER JOIN` garantiza que **solo se muestren los registros con coincidencias en todas las tablas**. Si un pedido no tiene producto o usuario asociado, no aparecera.
>
> El resultado muestra el nombre del comprador, el producto adquirido, la cantidad y el total pagado.

> **Tip del Profesor:** El orden de los JOINs importa en tablas grandes. Pon primero la tabla mas pequena o la que mas filas descarte. Esto ayuda al optimizador a generar un mejor plan de ejecucion.

---

### MySQL vs PostgreSQL: Sintaxis de JOIN

#### USING: alternativa a ON

Cuando el nombre de la columna es **igual** en ambas tablas, podes usar `USING` en lugar de `ON`.

```sql
-- Con ON (funciona en MySQL y PostgreSQL)
SELECT u.name, o.id, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Con USING (funciona en MySQL y PostgreSQL)
SELECT u.name, o.id, o.total
FROM users u
INNER JOIN orders o USING (user_id);

-- PostgreSQL: NATURAL JOIN (auto-detecta columnas con mismo nombre)
-- PELIGRO: une por TODAS las columnas con el mismo nombre
SELECT * FROM users NATURAL JOIN orders;
```

> **ADVERTENCIA sobre NATURAL JOIN:** Une automaticamente por todas las columnas con el mismo nombre en ambas tablas. Si ambas tablas tienen una columna `id`, las unira por `id` aunque no sea la intencion. Es propenso a errores: evitalo en codigo de produccion.

---

#### Sintaxis de abreviaturas

| Forma completa | Forma abreviada | MySQL | PostgreSQL |
|----------------|-----------------|-------|------------|
| INNER JOIN | JOIN | Si | Si |
| LEFT OUTER JOIN | LEFT JOIN | Si | Si |
| RIGHT OUTER JOIN | RIGHT JOIN | Si | Si |

---

### Tip del Profesor: Indices y Foreign Keys

> **Indices en claves foraneas:** Asegurate de tener un indice en las columnas que usas en `ON` (como `orders.user_id`). Sin indice, cada JOIN puede requerir un Full Table Scan sobre la tabla derecha, lo cual es O(n*m) en vez de O(n log m).

```sql
-- MySQL: crear indice en clave foranea
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- PostgreSQL: crear indice en clave foranea
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

> En PostgreSQL, los `FOREIGN KEY` **no crean indices automaticamente**. Si haces JOIN sobre una FK sin indice, el rendimiento puede ser muy malo en tablas grandes.

---

### Tip del Profesor: Orden de ejecucion de JOINs

El motor de base de datos evalua los JOINs de izquierda a derecha, pero el optimizador puede reorganizarlos. Para que tu consulta sea eficiente:

1. Filtra primero con `WHERE` si es posible (reduce filas antes de unir).
2. Usa alias consistentes (`u`, `o`, `p`) para legibilidad.
3. Pon la tabla mas pequena primero en JOINs encadenados.

```sql
-- Buena practica: filtro ANTES del JOIN
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;

-- Menos eficiente: filtra DESPUES
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;
-- (En este caso es igual porque el optimizador lo detecta,
--  pero conceptualmente es mejor filtrar antes)
```

---

### Resumen

* `INNER JOIN` combina filas solo cuando hay coincidencias entre las tablas.
* Es la forma mas comun de unir datos relacionados (por ejemplo, clientes y pedidos).
* Podes usar alias (`AS`) para acortar nombres de tablas y columnas.
* Se pueden encadenar varios `INNER JOIN` para unir tres o mas tablas.
* `USING` es una alternativa a `ON` cuando el nombre de columna es igual.
* Asegurate de tener indices en las columnas de JOIN para buen rendimiento.

En sistemas tipo e-commerce, este patron se usa constantemente para obtener informacion completa sobre cada compra o relacion entre entidades.
