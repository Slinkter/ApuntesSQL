### Funciones de Agregacion en MySQL -- Ejemplos y explicacion completa

---

> **Orden de ejecucion recomendado:** Para seguir este ejercicio, ejecuta primero los archivos `create-drop-db-table.md`, `alter-table.md` e `insert-into-select.md` para crear y poblar las tablas `products` y `orders`.

> **Analogia:** Imagina que eres contador de una tienda.
> - **COUNT** es como contar cuantos productos hay en el inventario.
> - **SUM** es como sumar todos los montos de las facturas del mes.
> - **AVG** es como calcular el precio promedio de todos los productos.
> - **MIN/MAX** es como saber cual es el producto mas barato y el mas caro.
> - Todas estas funciones son como una calculadora que toma muchas filas y devuelve **un solo numero**.

---

```sql

SELECT COUNT(*) AS productos_total FROM products;

SELECT COUNT(*) AS productos_con_stock FROM products WHERE stock > 0;

SELECT * FROM orders;

SELECT SUM(total) AS ganancia_total FROM orders;

SELECT AVG(price) AS precio_promedio FROM products;

SELECT MIN(price) AS precio_minimo, MAX(price) AS precio_maximo FROM products;

SELECT COUNT(*) AS total_productos, AVG(price) AS precio_promedio, SUM(stock) AS stock_total FROM products;

```

---

### Definicion

Las **funciones de agregacion** permiten realizar calculos sobre conjuntos de registros (filas) y devolver un solo valor como resultado. Son esenciales para generar reportes, estadisticas y analisis dentro de una base de datos.

---

#### 1. Contar la cantidad total de productos

```sql
SELECT COUNT(*) AS productos_total FROM products;
```

> Usa `COUNT(*)` para contar todas las filas de la tabla `products`.
> El alias `productos_total` se utiliza para mostrar el resultado con un nombre mas descriptivo.

> **Tip del Profesor:** `COUNT(*)` cuenta **todas** las filas incluyendo las que tienen NULLs. Si usas `COUNT(columna)`, solo cuenta las filas donde esa columna NO es NULL.

```sql
-- Diferencia critica:
SELECT COUNT(*) FROM products;           -- Cuenta todas las filas
SELECT COUNT(description) FROM products; -- Solo cuenta filas con description NO NULL
```

---

#### 2. Contar solo los productos con stock disponible

```sql
SELECT COUNT(*) AS productos_con_stock FROM products WHERE stock > 0;
```

> Aplica una condicion con `WHERE` para contar unicamente los productos que tienen mas de 0 unidades en stock.

---

#### 3. Ver los registros de la tabla `orders`

```sql
SELECT * FROM orders;
```

> Consulta todos los pedidos para tener una vista general antes de aplicar calculos agregados sobre ellos.

---

#### 4. Calcular la ganancia total (suma de los totales de pedidos)

```sql
SELECT SUM(total) AS ganancia_total FROM orders;
```

> `SUM()` suma todos los valores del campo `total` de la tabla `orders`.
> Ideal para conocer los ingresos acumulados del sistema.

> **Tip del Profesor:** `SUM()` ignora los valores NULL automaticamente. Si todos los valores son NULL, retorna NULL (no 0). Para evitar esto, usa `COALESCE(SUM(total), 0)`.

---

#### 5. Calcular el precio promedio de los productos

```sql
SELECT AVG(price) AS precio_promedio FROM products;
```

> `AVG()` devuelve el valor promedio del campo `price`.
> Util para analizar el rango de precios en el catalogo.

> **Tip del Profesor:** `AVG()` tambien ignora NULLs. Esto puede ser enganioso: si 3 de 10 productos tienen precio NULL, el promedio se calcula sobre los 7 restantes, no sobre 10.

---

#### 6. Obtener el precio minimo y maximo

```sql
SELECT MIN(price) AS precio_minimo, MAX(price) AS precio_maximo FROM products;
```

> `MIN()` devuelve el valor mas bajo, mientras que `MAX()` devuelve el mas alto.
> Se suelen usar juntos para analizar extremos de precios.

---

#### 7. Consultar multiples agregaciones en una sola sentencia

```sql
SELECT
    COUNT(*) AS total_productos,
    AVG(price) AS precio_promedio,
    SUM(stock) AS stock_total
FROM products;
```

> Combina varias funciones de agregacion en una misma consulta.
> Devuelve:
>
> * El total de productos (`COUNT(*)`)
> * El precio promedio (`AVG(price)`)
> * La suma total del stock (`SUM(stock)`).

---

### GROUP BY: Agregaciones por grupo

GROUP BY es la forma de decirle a SQL: "agrupame los resultados por una columna antes de calcular". Sin GROUP BY, las funciones de agregacion operan sobre **toda la tabla**.

```sql
-- Contar productos por cada precio diferente
SELECT
    price,
    COUNT(*) AS cantidad_productos
FROM products
GROUP BY price;
```

> Sin `GROUP BY`, `COUNT(*)` daria un solo numero (el total de productos).
> Con `GROUP BY price`, te dice cuantos productos hay **por cada precio**.

---

#### 8. Contar usuarios por cada tipo

```sql
SELECT
    role,
    COUNT(*) AS total_usuarios
FROM users
GROUP BY role;
```

> Agrupa los usuarios por su rol y cuenta cuantos hay en cada grupo.

---

#### 9. Suma de stock por precio

```sql
SELECT
    price,
    SUM(stock) AS stock_total
FROM products
GROUP BY price
ORDER BY price DESC;
```

> Para cada precio, calcula la suma total del stock.
> `ORDER BY price DESC` ordena de mayor a menor precio.

> **Tip del Profesor:** En MySQL, si el modo `ONLY_FULL_GROUP_BY` esta habilitado (por defecto en MySQL 5.7+), todas las columnas en SELECT deben estar en GROUP BY o ser parte de una funcion de agregacion.

---

### HAVING: Filtrar despues de agrupar

`WHERE` filtra **antes** de agrupar. `HAVING` filtra **despues** de agrupar. Es decir, HAVING permite filtrar sobre el resultado de una funcion de agregacion.

```sql
-- Productos con mas de 5 unidades en stock (filtro individual)
SELECT * FROM products WHERE stock > 5;

-- Precios que tienen mas de 2 productos (filtro sobre grupo)
SELECT
    price,
    COUNT(*) AS cantidad
FROM products
GROUP BY price
HAVING COUNT(*) > 2;
```

> `WHERE stock > 5` evalua fila por fila antes de agrupar.
> `HAVING COUNT(*) > 2` evalua sobre el grupo ya formado.

---

#### 10. Productos con stock total mayor a 20

```sql
SELECT
    price,
    SUM(stock) AS stock_total,
    COUNT(*) AS productos
FROM products
GROUP BY price
HAVING SUM(stock) > 20
ORDER BY stock_total DESC;
```

> Filtra grupos donde la suma de stock supere 20 unidades.
> Solo se muestran los precios cuyo stock acumulado es significativo.

> **Tip del Profesor:** La clausula de ejecucion en SQL es: `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY`. Esto explica por que `WHERE` no puede usar funciones de agregacion (todavia no se calcularon) pero `HAVING` si.

---

### MySQL vs PostgreSQL: Funciones de agregacion avanzadas

| Funcion | MySQL | PostgreSQL |
|---------|-------|------------|
| COUNT, SUM, AVG, MIN, MAX | Identico | Identico |
| FILTER (WHERE ...) | No soportado | `COUNT(*) FILTER (WHERE stock > 0)` |
| ARRAY_AGG | No disponible | `ARRAY_AGG(name)` devuelve un array |
| STRING_AGG | `GROUP_CONCAT(col SEPARATOR ',')` | `STRING_AGG(col, ',')` |
| LISTAGG | No nativo | No nativo (usa STRING_AGG) |

```sql
-- MySQL: GROUP_CONCAT para concatenar valores
SELECT
    role,
    GROUP_CONCAT(name SEPARATOR ', ') AS nombres
FROM users
GROUP BY role;

-- PostgreSQL: STRING_AGG para concatenar valores
SELECT
    role,
    STRING_AGG(name, ', ') AS nombres
FROM users
GROUP BY role;

-- PostgreSQL: FILTER para conteos condicionales
SELECT
    COUNT(*) AS total_productos,
    COUNT(*) FILTER (WHERE stock > 0) AS con_stock,
    COUNT(*) FILTER (WHERE stock = 0) AS sin_stock
FROM products;

-- PostgreSQL: ARRAY_AGG para crear arrays
SELECT
    role,
    ARRAY_AGG(name) AS lista_nombres
FROM users
GROUP BY role;
```

> **Tip del Profesor:** `FILTER` en PostgreSQL es una joya: es mas legible que `CASE WHEN` dentro de funciones de agregacion y tiene el mismo rendimiento.

---

### Resumen

| Funcion | Que hace | Ejemplo |
|---------|----------|---------|
| `COUNT(*)` | Cuenta todas las filas | `SELECT COUNT(*) FROM products;` |
| `COUNT(col)` | Cuenta filas no nulas | `SELECT COUNT(description) FROM products;` |
| `SUM(col)` | Suma valores numericos | `SELECT SUM(total) FROM orders;` |
| `AVG(col)` | Calcula promedio | `SELECT AVG(price) FROM products;` |
| `MIN(col)` | Valor minimo | `SELECT MIN(price) FROM products;` |
| `MAX(col)` | Valor maximo | `SELECT MAX(price) FROM products;` |
| `GROUP BY` | Agrupa por columna | `SELECT role, COUNT(*) FROM users GROUP BY role;` |
| `HAVING` | Filtra grupos | `HAVING COUNT(*) > 2` |

> **Tip del Profesor:** Las funciones de agregacion ignoran NULLs por defecto (excepto `COUNT(*)`). Si necesitas incluir NULLs en calculos, usa `COALESCE` para convertirlos a 0 antes de agregar.
