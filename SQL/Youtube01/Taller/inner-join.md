### INNER JOIN en MySQL – Ejemplos prácticos con explicación

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

El comando `INNER JOIN` se utiliza para **combinar datos de dos o más tablas** en función de una relación entre ellas, generalmente definida por una clave foránea (`FOREIGN KEY`). Es fundamental para trabajar con modelos relacionales y consultar información conectada.

---

## JOINS

| Forma completa        | Forma abreviada |
|-----------------------|-----------------|
| INNER JOIN            | JOIN            |
| LEFT OUTER JOIN       | LEFT JOIN       |
| RIGHT OUTER JOIN      | RIGHT JOIN      |

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
> * `orders.user_id` es la **clave foránea** que apunta al usuario que hizo el pedido.
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

> Los **alias** (`u` y `o`) simplifican la lectura del código y son muy útiles cuando se trabaja con varias tablas.
>
> * `AS comprador` renombra la columna en el resultado.
> * Se incluyen campos adicionales como la fecha del pedido (`order_date`).
>
> Este formato es más legible y se usa comúnmente en reportes o vistas.

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
> * `users` → contiene los clientes.
> * `orders` → contiene los pedidos.
> * `products` → contiene los productos comprados.
>
> El `INNER JOIN` garantiza que **solo se muestren los registros con coincidencias en todas las tablas**. Si un pedido no tiene producto o usuario asociado, no aparecerá.
>
> El resultado muestra el nombre del comprador, el producto adquirido, la cantidad y el total pagado.

---

✅ **Resumen:**

* `INNER JOIN` combina filas solo cuando hay coincidencias entre las tablas.
* Es la forma más común de unir datos relacionados (por ejemplo, clientes y pedidos).
* Podés usar alias (`AS`) para acortar nombres de tablas y columnas.
* Se pueden encadenar varios `INNER JOIN` para unir tres o más tablas.

En sistemas tipo e-commerce, este patrón se usa constantemente para obtener información completa sobre cada compra o relación entre entidades.
