### Subconsultas y GROUP BY en MySQL – Ejemplos prácticos y explicación

---

```sql

SELECT name AS usuario,
 (SELECT SUM(total)
 FROM orders
 WHERE user_id = u.id
) AS total_gastado
FROM users AS u;

SELECT name AS usuario,
 (SELECT SUM(total)
 FROM orders
 WHERE user_id = u.id
) AS total_gastado
FROM users AS u
HAVING total_gastado > 100;

SELECT usuario, total_gastado
FROM (
	SELECT u.name AS usuario, SUM(o.total) AS total_gastado
	FROM users AS u
	JOIN orders AS o ON u.id = o.user_id
	GROUP BY u.id, u.name
) AS resumen
WHERE total_gastado > 100;

SELECT u.name AS usuario, COALESCE(SUM(o.total),0) AS total_gastado
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_gastado DESC;

```

---

En SQL, las **subconsultas** y las **funciones de agregación con GROUP BY** permiten obtener información resumida o calculada por grupos de registros. Son muy utilizadas para generar reportes y análisis de comportamiento de usuarios o ventas.

---

#### 1. Subconsulta para calcular el total gastado por cada usuario

```sql
SELECT name AS usuario,
 (SELECT SUM(total)
  FROM orders
  WHERE user_id = u.id
 ) AS total_gastado
FROM users AS u;
```

> Esta consulta usa una **subconsulta correlacionada**, que se ejecuta por cada fila del resultado principal.
>
> * Para cada usuario (`u`), la subconsulta busca en `orders` la suma de los totales (`SUM(total)`) donde `user_id` coincide con el `id` del usuario.
> * Si un usuario no tiene pedidos, el valor será `NULL`.

---

#### 2. Subconsulta con filtro en el resultado (HAVING)

```sql
SELECT name AS usuario,
 (SELECT SUM(total)
  FROM orders
  WHERE user_id = u.id
 ) AS total_gastado
FROM users AS u
HAVING total_gastado > 100;
```

> Usa `HAVING` para filtrar usuarios cuyo gasto total supere 100.
>
> A diferencia de `WHERE`, el `HAVING` se utiliza para filtrar resultados que contienen funciones agregadas o subconsultas ya calculadas.

---

#### 3. Agrupación y filtrado con subconsulta interna

```sql
SELECT usuario, total_gastado
FROM (
  SELECT u.name AS usuario, SUM(o.total) AS total_gastado
  FROM users AS u
  JOIN orders AS o ON u.id = o.user_id
  GROUP BY u.id, u.name
) AS resumen
WHERE total_gastado > 100;
```

> Aquí se crea una **subconsulta anidada (subconsulta derivada)** llamada `resumen`.
>
> * En la subconsulta interna, se agrupan los pedidos por usuario (`GROUP BY`) y se calcula el total gastado por cada uno.
> * Luego, la consulta externa filtra solo aquellos usuarios que gastaron más de 100.
>
> Este patrón es común en dashboards y reportes donde se aplican filtros después de agrupar.

---

#### 4. Manejo de valores nulos con COALESCE y agrupación directa

```sql
SELECT u.name AS usuario, COALESCE(SUM(o.total),0) AS total_gastado
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_gastado DESC;
```

> Combina `LEFT JOIN` con funciones agregadas y `COALESCE()` para reemplazar valores `NULL` por 0.
>
> * `COALESCE(expr, valor)` devuelve el primer valor no nulo, asegurando que todos los usuarios aparezcan en el resultado (incluso sin pedidos).
> * `GROUP BY` agrupa los pedidos por usuario.
> * `ORDER BY total_gastado DESC` ordena del mayor al menor gasto.

---

✅ **Resumen:**

* **Subconsultas**: permiten calcular valores derivados por cada fila (útiles, pero pueden ser más lentas en grandes volúmenes de datos).
* **GROUP BY**: agrupa registros y permite aplicar funciones agregadas como `SUM()`, `COUNT()`, `AVG()`, etc.
* **HAVING**: filtra resultados después de aplicar las funciones agregadas.
* **COALESCE()**: reemplaza valores nulos para evitar resultados incompletos.

Estas técnicas son la base de los reportes analíticos en SQL, especialmente para obtener métricas por usuario, categoría o período de tiempo.
