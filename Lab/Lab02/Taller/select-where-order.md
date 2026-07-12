### SELECT en MySQL -- Ejemplos practicos con explicacion

---

> **Orden de ejecucion recomendado:** Para seguir este ejercicio, ejecuta primero los archivos `create-drop-db-table.md`, `alter-table.md` e `insert-into-select.md` para crear y poblar las tablas `users`, `products` y `orders`.

> **Analogia:** Imagina una biblioteca gigante.
> - **SELECT** es como pedirle al bibliotecario que te traiga libros. Podes pedir todos (`SELECT *`) o solo los de cierta seccion (`SELECT name, price`).
> - **WHERE** es como poner filtros: "quiero solo los libros de ciencia ficcion" o "los que cuesten menos de $20".
> - **ORDER BY** es como pedir que los ordene: "de la A a la Z" o "del mas caro al mas barato".
> - **LIMIT** es como decir "dame solo los primeros 5 resultados".

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

### Definicion

El comando `SELECT` se utiliza para **consultar informacion de las tablas** en una base de datos. Permite filtrar, ordenar, renombrar y limitar resultados. Es el comando mas utilizado en SQL y la base de cualquier analisis o reporte.

---

#### 1. Seleccionar todos los registros

```sql
SELECT * FROM products;
```

> Muestra todas las columnas y todos los registros de la tabla `products`.
> El asterisco (`*`) significa "todas las columnas".

> **Tip del Profesor:** En produccion, evita `SELECT *` en tablas anchas (muchas columnas). Solo selecciona las columnas que necesitas: reduce trafico de red y memoria.

---

#### 2. Seleccionar columnas especificas

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

> **Tip del Profesor:** Si la columna `price` tiene un indice, MySQL/PostgreSQL pueden usar un Index Range Scan para encontrar los registros rapidamente sin escanear toda la tabla.

---

#### 4. Filtrar por stock mayor o igual a 10

```sql
SELECT name, price, stock FROM products WHERE stock >= 10;
```

> Muestra productos con buen stock disponible (10 o mas unidades).

---

#### 5. Filtrar por multiples condiciones

```sql
SELECT name, price, stock FROM products WHERE stock >= 10 AND price > 10;
```

> Combina condiciones usando `AND`.
> Devuelve productos con stock suficiente y precio mayor a 10.

---

#### 6. Excluir un nombre especifico

```sql
SELECT name FROM products WHERE name != 'Taza';
```

> Muestra todos los productos excepto aquellos cuyo nombre sea "Taza".

---

#### 7. Filtrar valores dentro de un rango

```sql
SELECT name, price, stock FROM products WHERE price BETWEEN 50 AND 150;
```

> Devuelve productos con precios dentro del rango 50 a 150 (inclusive).
> `BETWEEN` es inclusivo: incluye ambos limites.

---

#### 8. Buscar coincidencias parciales con LIKE

```sql
SELECT name FROM products WHERE name LIKE '%mo%';
```

> Busca nombres que contengan "mo" en cualquier parte del texto.
> `%` funciona como comodin (wildcard): representa cualquier secuencia de caracteres.

> **Tip del Profesor:** `LIKE '%texto%'` (comodin al inicio) impide el uso de indices B-Tree, forzando un Full Table Scan. Si buscas frecuentemente por texto, considera un indice FULLTEXT en MySQL o `pg_trgm` en PostgreSQL.

---

#### 9. Buscar por valores especificos con IN

```sql
SELECT name FROM products WHERE id IN (1, 2, 3);
```

> Devuelve productos cuyos IDs sean 1, 2 o 3.
> Equivalente a `id = 1 OR id = 2 OR id = 3` pero mas limpio.

---

#### 10. Buscar valores nulos

```sql
SELECT name FROM products WHERE description IS NULL;
```

> Devuelve productos que **no tienen descripcion cargada**.
> **Nunca** uses `= NULL`; siempre usa `IS NULL`. NULL no es igual a nada, ni siquiera a si mismo.

---

#### 11. Buscar valores no nulos

```sql
SELECT name FROM products WHERE description IS NOT NULL;
```

> Devuelve productos con descripcion presente.

---

#### 12. Ordenar resultados de forma ascendente

```sql
SELECT * FROM products ORDER BY name ASC;
```

> Ordena los resultados alfabeticamente (de A a Z) por el campo `name`.
> `ASC` es el valor por defecto, podes omitirlo.

---

#### 13. Ordenar resultados de forma descendente

```sql
SELECT * FROM products ORDER BY description DESC;
```

> Ordena los productos por la descripcion de Z a A.

##### MySQL vs PostgreSQL: Ordenamiento de nulos

```sql
-- PostgreSQL: controlar donde aparecen los NULLs
SELECT * FROM products ORDER BY description ASC NULLS LAST;

-- MySQL: los NULLs van primero en ASC, al final en DESC
-- No soporta NULLS FIRST/LAST nativamente
-- Workaround en MySQL:
SELECT * FROM products ORDER BY IF(ISNULL(description), 1, 0), description ASC;
```

> **Tip del Profesor:** En PostgreSQL, `NULLS FIRST` y `NULLS LAST` son extremadamente utiles. Los NULLs se comportan diferente segun el motor: en PostgreSQL son "mayores" que cualquier valor, en MySQL varia segun el modo de comparacion.

---

#### 14. Limitar la cantidad de resultados

```sql
SELECT * FROM products LIMIT 3;
```

> Devuelve solo los primeros tres registros de la tabla.

##### MySQL vs PostgreSQL: Paginacion

```sql
-- MySQL y PostgreSQL: LIMIT basico
SELECT * FROM products ORDER BY price DESC LIMIT 10;

-- PostgreSQL: LIMIT con OFFSET (paginacion)
SELECT * FROM products ORDER BY price DESC LIMIT 10 OFFSET 20;

-- MySQL: LIMIT con OFFSET (sintaxis alternativa)
SELECT * FROM products ORDER BY price DESC LIMIT 20, 10;
```

> **Tip del Profesor:** `OFFSET` alto es lento en tablas grandes porque el motor lee y descarta filas. Para paginacion eficiente, usa "keyset pagination" (WHERE id > ultimo_id_visto).

---

#### 15. Eliminar duplicados con DISTINCT

```sql
SELECT DISTINCT name, description, price FROM products;
```

> Muestra combinaciones unicas de `name`, `description` y `price`, sin repetir filas identicas.

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

> Asigna un alias (`u`) a la tabla `users`, util para simplificar consultas y especialmente util en *joins*.

---

#### 18. SELECT con expresiones y alias

```sql
SELECT
    name AS producto,
    price AS precio,
    stock,
    price * stock AS valor_inventario,
    price * 1.21 AS precio_con_impuesto
FROM products
WHERE stock > 0
ORDER BY valor_inventario DESC;
```

> Podes usar expresiones aritmeticas directamente en `SELECT` para calcular valores derivados.
> Las expresiones se evaluan en tiempo de consulta: no modifican los datos originales.

> **Tip del Profesor:** Para expresiones complejas, usa alias con `AS` para que los resultados sean legibles. Sin alias, la columna mostraria la expresion completa como nombre.

---

#### 19. Bqueda case-insensitive con LIKE

##### MySQL vs PostgreSQL

| MySQL | PostgreSQL |
|-------|------------|
| `LIKE` es case-insensitive por defecto (depende del collation) | `LIKE` es case-sensitive |
| `WHERE name LIKE '%taza%'` encuentra "Taza", "TAZA", "taza" | Necesitas `ILIKE` o `LOWER()` |

```sql
-- MySQL: LIKE ya es case-insensitive (con collation default)
SELECT name FROM products WHERE name LIKE '%taza%';

-- PostgreSQL: ILIKE para busqueda case-insensitive
SELECT name FROM products WHERE name ILIKE '%taza%';

-- PostgreSQL: alternativa con LOWER (funciona en ambos motores)
SELECT name FROM products WHERE LOWER(name) LIKE '%taza%';
```

> **Tip del Profesor:** En MySQL, el comportamiento de `LIKE` depende de la collation de la columna. Si usas `utf8mb4_bin`, LIKE sera case-sensitive.

---

### Resumen

`SELECT` es el comando mas versatil de SQL. Te permite obtener informacion especifica, ordenada y filtrada segun tus necesidades. Combinado con condiciones (`WHERE`), rangos (`BETWEEN`), busquedas parciales (`LIKE`), y alias (`AS`), se convierte en la base de cualquier analisis o reporte de datos.

| ClAUSE | Funcion | Tip |
|--------|---------|-----|
| `SELECT` | Elige columnas | Evita `SELECT *` en produccion |
| `WHERE` | Filtra filas | Usa indices para mejorar rendimiento |
| `ORDER BY` | Ordena resultados | ASC es por defecto; cuidado con NULLs |
| `LIMIT` | Limita filas | Fundamental para paginacion |
| `DISTINCT` | Elimina duplicados | Costoso en tablas grandes |
| `AS` | Renombra columnas/tablas | Siempre para columnas calculadas |
