### LEFT JOIN, RIGHT JOIN y combinaciones multiples en MySQL – Ejemplos con explicacion

---

## Analogia

Imagina que organizas una fiesta y tienes dos listas: la lista de invitados (tabla izquierda) y la lista de regalos que trajeron (tabla derecha). Un `LEFT JOIN` te muestra todos los invitados, incluso los que llegaron sin regalo (NULL en la columna de regalos). Un `RIGHT JOIN` te muestra todos los regalos, incluso aquellos cuyo invitado no esta registrado porque alguien los dejo en la puerta sin identificarse.

Un `FULL OUTER JOIN` seria como tener ambas listas completas: todos los invitados y todos los regalos, incluso si un invitado no trajo regalo o un regalo no tiene dueno conocido.

---

## Definicion

En SQL, los **JOINs** permiten combinar datos de distintas tablas relacionadas. A diferencia del `INNER JOIN`, los `LEFT JOIN` y `RIGHT JOIN` tambien muestran los registros que no tienen coincidencias en una de las tablas, lo que los hace muy utiles para detectar ausencias o generar reportes completos.

**Visualmente:**

- `INNER JOIN`: solo la interseccion (coincidencias en ambas).
- `LEFT JOIN`: toda la tabla izquierda + coincidencias de la derecha (NULL donde no hay).
- `RIGHT JOIN`: toda la tabla derecha + coincidencias de la izquierda (NULL donde no hay).
- `FULL OUTER JOIN`: ambas tablas completas (NULL donde no hay coincidencia). Soportado por PostgreSQL, no nativamente por MySQL.

---

## JOINS

| Forma completa        | Forma abreviada |
|-----------------------|-----------------|
| INNER JOIN            | JOIN            |
| LEFT OUTER JOIN       | LEFT JOIN       |
| RIGHT OUTER JOIN      | RIGHT JOIN      |

> Para una referencia completa de todos los tipos de JOIN, consulta la guia en `Tipos-Join/`.

---

#### 1. LEFT JOIN – mostrar todos los usuarios y sus pedidos (si existen)

```sql
-- Todos los usuarios aparecen; los que no tienen pedidos
-- mostraran NULL en las columnas de orders
SELECT u.name AS usuario, o.id AS pedido, o.total
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id;
```

> El `LEFT JOIN` devuelve **todos los registros de la tabla de la izquierda** (`users`), junto con los datos de `orders` **solo si existen coincidencias**.
>
> Si un usuario no tiene pedidos, las columnas de `orders` apareceran como `NULL`.
>
> Esto es ideal para obtener un listado completo de usuarios y detectar quienes todavia no realizaron compras.

---

#### 2. LEFT JOIN con condicion para mostrar solo los usuarios sin pedidos

```sql
-- Filtra solo los usuarios que NUNCA han hecho un pedido
SELECT u.name AS usuario, o.id AS pedido, o.total
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
WHERE o.id IS NULL;
```

> En este caso, se agrega una condicion `WHERE o.id IS NULL` para **filtrar unicamente a los usuarios sin pedidos asociados**.
>
> Es una consulta muy util en sistemas de e-commerce para identificar clientes inactivos o nuevos.

---

#### 3. RIGHT JOIN – mostrar todos los pedidos y sus usuarios (si existen)

```sql
-- Todos los pedidos aparecen; los que no tengan usuario asociado
-- (datos huerfanos) mostraran NULL en users.name
SELECT u.name AS usuario, o.id AS pedido, o.total
FROM users AS u
RIGHT JOIN orders AS o
ON u.id = o.user_id;
```

> `RIGHT JOIN` funciona igual que `LEFT JOIN`, pero devuelve **todos los registros de la tabla derecha** (`orders`) y solo los usuarios que coinciden.
>
> Es util para verificar si existen pedidos que quedaron sin un usuario valido (por ejemplo, por errores en integridad referencial o pruebas de datos).

---

#### 4. FULL OUTER JOIN (PostgreSQL) – todos los registros de ambas tablas

```sql
-- PostgreSQL unicamente: muestra todos los usuarios y todos los pedidos,
-- incluso si no hay relacion entre ellos
SELECT u.name AS usuario, o.id AS pedido, o.total
FROM users AS u
FULL OUTER JOIN orders AS o
ON u.id = o.user_id;

-- Con manejo de NULLs usando COALESCE
SELECT
  COALESCE(u.name, '(sin usuario)') AS usuario,
  COALESCE(o.id::text, '(sin pedido)') AS pedido,
  o.total
FROM users AS u
FULL OUTER JOIN orders AS o
ON u.id = o.user_id;
```

> **MySQL vs PostgreSQL:** MySQL no soporta `FULL OUTER JOIN` nativamente. En MySQL, debes simularlo con `LEFT JOIN UNION RIGHT JOIN`. PostgreSQL lo soporta directamente.
>
> `COALESCE()` reemplaza valores NULL por un texto o valor por defecto, muy util en reportes con FULL OUTER JOIN para evitar celdas vacias.

---

#### 5. JOIN multiple – combinar usuarios, productos y pedidos

```sql
-- Detalle completo de cada compra combinando 3 tablas
SELECT
  u.name AS usuario,
  p.name AS producto,
  o.quantity AS cantidad,
  o.total,
  o.order_date AS fecha
FROM orders AS o
JOIN users AS u ON o.user_id = u.id
JOIN products AS p ON o.product_id = p.id
ORDER BY u.name;
```

> Esta consulta combina tres tablas (`orders`, `users`, `products`) para obtener un detalle completo de cada compra.
>
> * `JOIN users` une cada pedido con el comprador.
> * `JOIN products` agrega el nombre del producto.
> * `ORDER BY u.name` ordena los resultados alfabeticamente por el nombre del usuario.
>
> Es una forma clara y eficiente de generar reportes de ventas o exportar datos completos.

---

#### 6. LEFT JOIN con varias condiciones y COALESCE (PostgreSQL)

```sql
-- PostgreSQL: LEFT JOIN con COALESCE para manejar NULLs
-- y filtro adicional sobre la tabla secundaria
SELECT
  u.name AS usuario,
  COALESCE(SUM(o.total), 0) AS total_gastado,
  COUNT(o.id) AS total_pedidos
FROM users AS u
LEFT JOIN orders AS o
  ON u.id = o.user_id
  AND o.status = 'paid'  -- Filtro en ON, no en WHERE
GROUP BY u.name
ORDER BY total_gastado DESC;
```

> **MySQL vs PostgreSQL:** En ambos motores, poner condiciones de la tabla secundaria en `ON` (en lugar de `WHERE`) evita que el LEFT JOIN se convierta en INNER JOIN. La diferencia esta en como cada motor optimiza la consulta, pero el resultado es el mismo.
>
> `COALESCE()` es estandar SQL y funciona en ambos motores.

---

### Tip del Profesor

- **LEFT JOIN vs RIGHT JOIN:** Usa `LEFT JOIN` siempre que puedas. `RIGHT JOIN` es menos comun y puede hacer que el codigo sea mas dificil de leer. Si necesitas un `RIGHT JOIN`, considera reordenar las tablas para convertirlo en `LEFT JOIN`.
- **Rendimiento con LEFT JOIN:** En tablas grandes, los `LEFT JOIN` pueden ser costosos porque el motor debe escanear toda la tabla izquierda. Asegurate de tener indices en las columnas del `ON` (claves foraneas indexadas).
- **FULL OUTER JOIN en MySQL:** Para simularlo en MySQL: `SELECT ... FROM a LEFT JOIN b ON ... UNION SELECT ... FROM a RIGHT JOIN b ON ...`. Esto duplica la tabla intermedia, asi que usalo con cuidado en tablas grandes.
- **Filtros en ON vs WHERE:** En un `LEFT JOIN`, poner un filtro de la tabla derecha en `WHERE` (ej. `WHERE o.total > 100`) lo convierte implicitamente en `INNER JOIN`. Si quieres mantener todos los registros de la izquierda, pon ese filtro en `ON`.
- **Detectar datos huerfanos:** Usa `LEFT JOIN WHERE derecha.id IS NULL` para encontrar registros en la tabla izquierda que no tienen relacion en la derecha. Es el patron mas comun para auditoria de integridad referencial.

---

## Resumen

* `LEFT JOIN`: muestra todos los registros de la tabla izquierda, incluso si no hay coincidencias.
* `RIGHT JOIN`: muestra todos los registros de la tabla derecha.
* `FULL OUTER JOIN` (PostgreSQL): muestra todos los registros de ambas tablas.
* `WHERE o.id IS NULL`: sirve para detectar registros sin relacion (antipatron de datos huerfanos).
* `JOIN` multiple: permite combinar varias tablas para obtener informacion completa.
* `COALESCE()`: reemplaza NULLs por valores por defecto en los resultados.

Estos tipos de joins son esenciales para el analisis de datos y el mantenimiento de relaciones en bases de datos relacionales.
