### UPDATE, DELETE, TRUNCATE y DROP en MySQL -- Ejemplos practicos con explicacion

---

> **Orden de ejecucion recomendado:** Para seguir este ejercicio, ejecuta primero los archivos `create-drop-db-table.md`, `alter-table.md` e `insert-into-select.md` para crear y poblar las tablas `users`, `products` y `providers`.

> **Analogia:** Imagina que tienes un documento de texto.
> - **UPDATE** es como editar un parrafo: cambias el contenido de lineas especificas.
> - **DELETE** es como borrar un parrafo: la linea desaparece, pero el documento sigue ahi.
> - **TRUNCATE** es como seleccionar todo el contenido y presionar "borrar": el documento queda vacio pero la estructura (margenes, formato) se mantiene.
> - **DROP** es como eliminar el archivo completo: ya no existe.

---

```sql

UPDATE users SET password = 'thingesmimejoramigo', cellphone = '+1500111222' WHERE id = 3;

UPDATE products SET description = 'La ruedita mas comoda de tu ciudad' WHERE id = 2;

UPDATE products SET description = 'Las teclas mas suaves del mercado', stock = 1 WHERE id = 3;

DELETE from products WHERE id = 8;

INSERT INTO products (name, description, price,stock)
VALUES
('Mate', 'Perfecto para Cebar', 100.00, 10)

TRUNCATE TABLE providers;

DROP TABLE providers;

SHOW TABLES;

```

---

### Definicion

Estos comandos te permiten **modificar o eliminar datos y estructuras** dentro de tu base de datos. A continuacion, te muestro ejemplos paso a paso usando las tablas `users`, `products` y `providers`.

> **ADVERTENCIA IMPORTANTE:** Ejecutar `DELETE` o `UPDATE` **sin** una clausula `WHERE` afectara **TODAS** las filas de la tabla. En produccion, esto puede destruir datos criticos. Siempre verifica tu consulta `WHERE` antes de ejecutar.

> **Tip del Profesor:** Para operaciones criticas, envolve tus sentencias en una transaccion. En MySQL usa `START TRANSACTION;` ... `COMMIT;` (o `ROLLBACK;` si algo sale mal). En PostgreSQL es igual. Esto te permite deshacer cambios si te equivocas.

---

#### 1. Actualizar datos en una tabla

```sql
UPDATE users
SET password = 'thingesmimejoramigo', cellphone = '+1500111222'
WHERE id = 3;
```

> Modifica la contrasena y el numero de celular del usuario con `id = 3`.
> El uso del **WHERE** es fundamental para evitar modificar todos los registros por error.

##### MySQL vs PostgreSQL

| Aspecto | MySQL | PostgreSQL |
|---------|-------|------------|
| UPDATE basico | Identico | Identico |
| UPDATE ... FROM | No soportado | `UPDATE t SET col = ... FROM o WHERE t.id = o.fk` permite referenciar otra tabla |
| RETURNING | No disponible | `UPDATE ... SET ... RETURNING *` devuelve las filas modificadas |

```sql
-- PostgreSQL: UPDATE con FROM (actualiza usando datos de otra tabla)
UPDATE products p
SET price = p.price * 1.10
FROM orders o
WHERE o.product_id = p.id
  AND o.order_date >= '2026-01-01';

-- PostgreSQL: RETURNING devuelve lo que se actualizo
UPDATE users
SET password = 'nuevapass'
WHERE id = 3
RETURNING id, name, password;
```

> **Tip del Profesor:** En PostgreSQL, `UPDATE ... FROM` es extremadamente poderoso para actualizaciones masivas basadas en relaciones. En MySQL, necesitas subconsultas para lograr lo mismo.

---

#### 2. Actualizar una descripcion de producto

```sql
UPDATE products
SET description = 'La ruedita mas comoda de tu ciudad'
WHERE id = 2;
```

> Cambia la descripcion del producto con `id = 2` (en este caso, probablemente el *Mouse*).
> Ideal para corregir o mejorar textos sin alterar otros campos.

---

#### 3. Actualizar multiples columnas en un mismo registro

```sql
UPDATE products
SET description = 'Las teclas mas suaves del mercado', stock = 1
WHERE id = 3;
```

> Modifica tanto la descripcion como el stock del producto `id = 3` (el *Keyboard*).
> Podes actualizar varios campos al mismo tiempo separandolos con comas.

> **Tip del Profesor:** Antes de ejecutar un `UPDATE`, prueba tu filtro con un `SELECT` para confirmar que afecta solo los registros deseados:
> ```sql
> SELECT * FROM products WHERE id = 3; -- Verificar antes de UPDATE
> ```

---

#### 4. Eliminar un registro especifico

```sql
DELETE FROM products WHERE id = 8;
```

> Borra el producto con `id = 8`.
> Siempre es recomendable usar `WHERE` para evitar eliminar todos los registros de la tabla.

##### MySQL vs PostgreSQL

| Aspecto | MySQL | PostgreSQL |
|---------|-------|------------|
| DELETE basico | Identico | Identico |
| DELETE con USING | No soportado | `DELETE FROM t USING o WHERE t.id = o.fk` permite filtrar basado en otra tabla |
| RETURNING | No disponible | `DELETE FROM ... RETURNING *` devuelve las filas eliminadas |

```sql
-- PostgreSQL: DELETE con USING (elimina basado en otra tabla)
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.id
  AND o.order_date < '2020-01-01';

-- PostgreSQL: RETURNING muestra que se elimino
DELETE FROM products WHERE id = 8
RETURNING *;
```

> **Tip del Profesor:** En MySQL, si necesitas eliminar basado en otra tabla, usa una subconsulta:
> ```sql
> DELETE FROM order_items WHERE order_id IN (
>   SELECT id FROM orders WHERE order_date < '2020-01-01'
> );
> ```

---

#### 5. Insertar un nuevo producto

```sql
INSERT INTO products (name, description, price, stock)
VALUES
('Mate', 'Perfecto para Cebar', 100.00, 10);
```

> Agrega un nuevo producto a la tabla `products`.
> Esto permite recuperar la informacion de catalogo luego de una eliminacion accidental o al agregar nuevos items.

---

#### 6. Vaciar completamente una tabla (sin eliminar su estructura)

```sql
TRUNCATE TABLE providers;
```

> Elimina **todos los registros** de la tabla `providers`, pero **mantiene la estructura** para volver a usarla.
> Es mas rapido que `DELETE` cuando queres limpiar toda la tabla.

##### MySQL vs PostgreSQL

| Aspecto | MySQL | PostgreSQL |
|---------|-------|------------|
| TRUNCATE basico | Identico | Identico |
| RESET IDENTITY | No automatico | `TRUNCATE TABLE t RESTART IDENTITY` reinicia el contador de secuencia |
| CASCADE | No disponible | `TRUNCATE TABLE t CASCADE` trunca tablas dependientes automaticamente |
| RETURNING | No disponible | No disponible en TRUNCATE |

```sql
-- PostgreSQL: TRUNCATE con reinicio de secuencia
TRUNCATE TABLE providers RESTART IDENTITY;

-- PostgreSQL: TRUNCATE con CASCADE (cuidado, elimina en cascada)
TRUNCATE TABLE providers CASCADE;
```

> **Tip del Profesor:** `TRUNCATE` no dispara triggers y es no transaccional en MySQL (no se puede deshacer con ROLLBACK). En PostgreSQL, si esta dentro de una transaccion, si se puede deshacer.

---

#### 7. Eliminar una tabla por completo

```sql
DROP TABLE providers;
```

> Borra **definitivamente** la tabla `providers` y toda su estructura.
> Despues de ejecutarlo, la tabla deja de existir y no se puede consultar.

```sql
-- Util: evitar error si la tabla no existe
DROP TABLE IF EXISTS providers;
```

---

#### 8. Listar las tablas existentes

```sql
SHOW TABLES;
```

> Muestra las tablas que aun existen en la base de datos actual. Sirve para confirmar si `providers` fue realmente eliminada.

##### MySQL vs PostgreSQL

| MySQL | PostgreSQL |
|-------|------------|
| `SHOW TABLES;` | `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';` |

---

### Resumen

| Comando | Que hace | Estructura | Velocidad | Deshacible |
|---------|----------|------------|-----------|------------|
| `UPDATE` | Modifica registros | Se mantiene | Media | Si (con transaccion) |
| `DELETE` | Elimina filas | Se mantiene | Lenta (registra cada fila) | Si (con transaccion) |
| `TRUNCATE` | Vacia la tabla | Se mantiene | Muy rapida | Solo en PostgreSQL |
| `DROP` | Elimina la tabla | Desaparece | Rapida | No |

> **Tip del Profesor:** En produccion, preferi siempre `DELETE` con `WHERE` sobre `TRUNCATE` cuando necesites control granular. Usa `TRUNCATE` solo para limpiar tablas temporales o de staging. Y siempre, **siempre**, tenes un backup antes de operar.

---

Estas operaciones son fundamentales para **mantener y administrar datos en produccion**, especialmente cuando necesitas limpiar, corregir o reestructurar tu base de datos sin comprometer su integridad.
