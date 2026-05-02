### Funciones de Agregación en MySQL – Ejemplos y explicación completa

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

Las **funciones de agregación** permiten realizar cálculos sobre conjuntos de registros (filas) y devolver un solo valor como resultado. Son esenciales para generar reportes, estadísticas y análisis dentro de una base de datos.

---

#### 1. Contar la cantidad total de productos

```sql
SELECT COUNT(*) AS productos_total FROM products;
```

> Usa `COUNT(*)` para contar todas las filas de la tabla `products`.
> El alias `productos_total` se utiliza para mostrar el resultado con un nombre más descriptivo.

---

#### 2. Contar solo los productos con stock disponible

```sql
SELECT COUNT(*) AS productos_con_stock FROM products WHERE stock > 0;
```

> Aplica una condición con `WHERE` para contar únicamente los productos que tienen más de 0 unidades en stock.

---

#### 3. Ver los registros de la tabla `orders`

```sql
SELECT * FROM orders;
```

> Consulta todos los pedidos para tener una vista general antes de aplicar cálculos agregados sobre ellos.

---

#### 4. Calcular la ganancia total (suma de los totales de pedidos)

```sql
SELECT SUM(total) AS ganancia_total FROM orders;
```

> `SUM()` suma todos los valores del campo `total` de la tabla `orders`.
> Ideal para conocer los ingresos acumulados del sistema.

---

#### 5. Calcular el precio promedio de los productos

```sql
SELECT AVG(price) AS precio_promedio FROM products;
```

> `AVG()` devuelve el valor promedio del campo `price`.
> Útil para analizar el rango de precios en el catálogo.

---

#### 6. Obtener el precio mínimo y máximo

```sql
SELECT MIN(price) AS precio_minimo, MAX(price) AS precio_maximo FROM products;
```

> `MIN()` devuelve el valor más bajo, mientras que `MAX()` devuelve el más alto.
> Se suelen usar juntos para analizar extremos de precios.

---

#### 7. Consultar múltiples agregaciones en una sola sentencia

```sql
SELECT COUNT(*) AS total_productos, AVG(price) AS precio_promedio, SUM(stock) AS stock_total FROM products;
```

> Combina varias funciones de agregación en una misma consulta.
> Devuelve:
>
> * El total de productos (`COUNT(*)`)
> * El precio promedio (`AVG(price)`)
> * La suma total del stock (`SUM(stock)`).

---

✅ **Resumen:**
Las funciones de agregación más comunes en MySQL son:

* `COUNT()` → cuenta filas.
* `SUM()` → suma valores.
* `AVG()` → calcula promedios.
* `MIN()` / `MAX()` → obtienen el mínimo y máximo.

Podés combinarlas con `WHERE` para filtrar datos y con `GROUP BY` (en consultas más avanzadas) para agrupar resultados según una columna específica.
