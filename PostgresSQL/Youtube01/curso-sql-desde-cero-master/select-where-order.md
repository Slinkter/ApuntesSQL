### SELECT en MySQL – Ejemplos prácticos con explicación

---

```sql

SELECT * FROM products;

SELECT name, description FROM products;

SELECT * FROM products WHERE price > 100;

SELECT name, price, stock FROM products WHERE stock >= 10;

SELECT name, price, stock FROM products WHERE stock >= 10 AND price > 10;

SELECT name FROM products WHERE name != 'Taza';

SELECT name, price, stock FROM products WHERE price BETWEEN 50 AND 150;

SELECT name FROM products WHERE name LIKE '%mo%';

SELECT name FROM products WHERE id IN (1,2,3)

SELECT name FROM products WHERE description IS NULL;

SELECT name FROM products WHERE description IS NOT NULL;

SELECT * FROM products ORDER BY name ASC;

SELECT * FROM products ORDER BY description DESC;

SELECT * FROM products LIMIT 3;

SELECT DISTINCT name,description, price FROM products;

SELECT name AS producto, price AS precio FROM products;

SELECT u.name AS usuario FROM users AS u;

```

---

El comando `SELECT` se utiliza para **consultar información de las tablas** en una base de datos. Permite filtrar, ordenar, renombrar y limitar resultados. A continuación, te muestro ejemplos aplicados a la tabla `products` y otras relacionadas.

---

#### 1. Seleccionar todos los registros

```sql
SELECT * FROM products;
```

> Muestra todas las columnas y todos los registros de la tabla `products`.
> El asterisco (`*`) significa “todas las columnas”.

---

#### 2. Seleccionar columnas específicas

```sql
SELECT name, description FROM products;
```

> Muestra solo las columnas `name` y `description`.
> Ideal para mejorar rendimiento y claridad en consultas.

---

#### 3. Filtrar por precio mayor a 100

```sql
SELECT * FROM products WHERE price > 100;
```

> Devuelve solo los productos cuyo precio sea mayor a 100.

---

#### 4. Filtrar por stock mayor o igual a 10

```sql
SELECT name, price, stock FROM products WHERE stock >= 10;
```

> Muestra productos con buen stock disponible (10 o más unidades).

---

#### 5. Filtrar por múltiples condiciones

```sql
SELECT name, price, stock FROM products WHERE stock >= 10 AND price > 10;
```

> Combina condiciones usando `AND`.
> Devuelve productos con stock suficiente y precio mayor a 10.

---

#### 6. Excluir un nombre específico

```sql
SELECT name FROM products WHERE name != 'Taza';
```

> Muestra todos los productos excepto aquellos cuyo nombre sea “Taza”.

---

#### 7. Filtrar valores dentro de un rango

```sql
SELECT name, price, stock FROM products WHERE price BETWEEN 50 AND 150;
```

> Devuelve productos con precios dentro del rango 50 a 150 (inclusive).

---

#### 8. Buscar coincidencias parciales con LIKE

```sql
SELECT name FROM products WHERE name LIKE '%mo%';
```

> Busca nombres que contengan “mo” en cualquier parte del texto.
> `%` funciona como comodín (wildcard).

---

#### 9. Buscar por valores específicos con IN

```sql
SELECT name FROM products WHERE id IN (1,2,3);
```

> Devuelve productos cuyos IDs sean 1, 2 o 3.

---

#### 10. Buscar valores nulos

```sql
SELECT name FROM products WHERE description IS NULL;
```

> Devuelve productos que **no tienen descripción cargada**.

---

#### 11. Buscar valores no nulos

```sql
SELECT name FROM products WHERE description IS NOT NULL;
```

> Devuelve productos con descripción presente.

---

#### 12. Ordenar resultados de forma ascendente

```sql
SELECT * FROM products ORDER BY name ASC;
```

> Ordena los resultados alfabéticamente (de A a Z) por el campo `name`.

---

#### 13. Ordenar resultados de forma descendente

```sql
SELECT * FROM products ORDER BY description DESC;
```

> Ordena los productos por la descripción de Z a A.

---

#### 14. Limitar la cantidad de resultados

```sql
SELECT * FROM products LIMIT 3;
```

> Devuelve solo los primeros tres registros de la tabla.

---

#### 15. Eliminar duplicados con DISTINCT

```sql
SELECT DISTINCT name, description, price FROM products;
```

> Muestra combinaciones únicas de `name`, `description` y `price`, sin repetir filas idénticas.

---

#### 16. Renombrar columnas en la consulta

```sql
SELECT name AS producto, price AS precio FROM products;
```

> Usa `AS` para mostrar nombres personalizados en el resultado. Ideal para reportes.

---

#### 17. Alias para tablas

```sql
SELECT u.name AS usuario FROM users AS u;
```

> Asigna un alias (`u`) a la tabla `users`, útil para simplificar consultas y especialmente útil en *joins*.

---

✅ **Resumen:**
`SELECT` es el comando más versátil de SQL. Te permite obtener información específica, ordenada y filtrada según tus necesidades. Combinado con condiciones (`WHERE`), rangos (`BETWEEN`), búsquedas parciales (`LIKE`), y alias (`AS`), se convierte en la base de cualquier análisis o reporte de datos.
