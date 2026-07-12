### Subconsultas, GROUP BY, HAVING y COALESCE en MySQL – Ejemplos practicos y explicacion

---

## Analogia

**Subconsultas:** Es como hacer una pregunta dentro de otra pregunta. Por ejemplo: "Dame todos los usuarios (pregunta externa) y, para cada uno, dime cuanto gasto en total (pregunta interna)". La segunda pregunta se ejecuta para cada respuesta de la primera.

**GROUP BY y HAVING:** Imagina que tienes una bolsa de cartas de diferentes palos. `GROUP BY` seria como separarlas en montones por palo (corazones, treboles, picas). Luego, `COUNT(*)` te dice cuantas cartas hay en cada monton. `HAVING` seria como quedarte solo con los montones que tienen mas de 5 cartas.

**COALESCE:** Es como pedir un cafe con leche de soja; si no hay leche de soja, que te pongan leche normal; si no hay leche normal, que te pongan agua; si no hay nada, que te devuelvan el dinero. COALESCE prueba opciones en orden hasta que encuentra una que no sea nula.

---

## Definicion

En SQL, las **subconsultas** y las **funciones de agregacion con GROUP BY** permiten obtener informacion resumida o calculada por grupos de registros. El **HAVING** filtra resultados despues de la agregacion, y **COALESCE** reemplaza valores nulos. Son herramientas esenciales para generar reportes y analisis de comportamiento de usuarios o ventas.

---

#### 1. Subconsulta para calcular el total gastado por cada usuario

```sql
-- Subconsulta correlacionada: se ejecuta por cada fila de users
SELECT
    u.name AS usuario,
    (SELECT SUM(o.total)
     FROM orders o
     WHERE o.user_id = u.id
    ) AS total_gastado
FROM users AS u;
```

> Esta consulta usa una **subconsulta correlacionada**, que se ejecuta por cada fila del resultado principal.
>
> * Para cada usuario (`u`), la subconsulta busca en `orders` la suma de los totales (`SUM(total)`) donde `user_id` coincide con el `id` del usuario.
> * Si un usuario no tiene pedidos, el valor sera `NULL` (no 0).

> **MySQL vs PostgreSQL:** La sintaxis es identica en ambos. Sin embargo, las subconsultas correlacionadas tienden a ser lentas en MySQL (ejecuta la subconsulta por cada fila de la tabla externa). PostgreSQL puede optimizar algunas subconsultas correlacionadas con planos mas eficientes.

---

#### 2. Subconsulta con filtro en el resultado (HAVING) -- MySQL-only

```sql
-- ATENCION: Este HAVING sobre alias de subconsulta es MySQL-only
SELECT
    u.name AS usuario,
    (SELECT SUM(o.total)
     FROM orders o
     WHERE o.user_id = u.id
    ) AS total_gastado
FROM users AS u
HAVING total_gastado > 100;
```

> Esta sintaxis usa `HAVING` para filtrar usuarios cuyo gasto total supere 100.
>
> **MySQL vs PostgreSQL:** En MySQL, `HAVING` puede referirse a alias de columnas en el SELECT, incluso si son subconsultas. **PostgreSQL no lo permite**. En PostgreSQL, un `HAVING` solo puede usarse con GROUP BY y funciones de agregacion en el SELECT. Para lograr el mismo resultado en PostgreSQL, debes usar una subconsulta derivada (ve el siguiente ejemplo).

---

#### 3. Agrupacion y filtrado con subconsulta interna (estandar SQL)

```sql
-- Funciona en MySQL y PostgreSQL: subconsulta derivada con WHERE externo
SELECT usuario, total_gastado
FROM (
    SELECT u.name AS usuario, SUM(o.total) AS total_gastado
    FROM users AS u
    JOIN orders AS o ON u.id = o.user_id
    GROUP BY u.id, u.name
) AS resumen
WHERE total_gastado > 100;
```

> Aqui se crea una **subconsulta derivada (subconsulta anidada)** llamada `resumen`.
>
> * En la subconsulta interna, se agrupan los pedidos por usuario (`GROUP BY`) y se calcula el total gastado por cada uno.
> * Luego, la consulta externa filtra solo aquellos usuarios que gastaron mas de 100.
>
> Este patron es comun en dashboards y reportes donde se aplican filtros despuess de agrupar. Tambien funciona de forma identica en PostgreSQL.

> **Tip de rendimiento:** Las subconsultas derivadas suelen ser mas eficientes que las subconsultas correlacionadas, porque la agregacion se realiza una sola vez para todos los registros.

---

#### 4. COALESCE: manejo de valores nulos con agrupacion directa

```sql
-- COALESCE reemplaza NULL por 0 para usuarios sin pedidos
SELECT
    u.name AS usuario,
    COALESCE(SUM(o.total), 0) AS total_gastado
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_gastado DESC;
```

> Combina `LEFT JOIN` con funciones agregadas y `COALESCE()` para reemplazar valores `NULL` por 0.
>
> * `COALESCE(expr, valor)` devuelve el primer valor no nulo; asegura que todos los usuarios aparezcan (incluso sin pedidos).
> * `GROUP BY u.id, u.name` agrupa los pedidos por usuario. Se agrupa por u.id (clave primaria) para que coincidan aunque haya dos usuarios con el mismo nombre.
> * `ORDER BY total_gastado DESC` ordena del mayor al menor gasto.
>
> **MySQL vs PostgreSQL:** `COALESCE` es estandar SQL y funciona identico en ambos. En MySQL tambien existe `IFNULL(expr, valor)` que es especifico de MySQL; prefiere `COALESCE` para portabilidad.

---

#### 5. GROUP BY con ROLLUP (PostgreSQL y MySQL 8+)

```sql
-- ROLLUP agrega una fila extra con el total general
SELECT
    COALESCE(u.name, 'TOTAL') AS usuario,
    COUNT(o.id) AS pedidos,
    SUM(o.total) AS total_gastado
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
GROUP BY ROLLUP (u.name);
```

> `ROLLUP` genera subtotales y un total general. Es util para reportes jerarquicos.
>
> **MySQL vs PostgreSQL:** Ambos soportan `ROLLUP` desde versiones recientes. PostgreSQL tambien soporta `CUBE` y `GROUPING SETS` (multiples agrupaciones en una sola consulta), que MySQL solo soporta parcialmente.

> **PostgreSQL extra: GROUPING SETS y CUBE**
> ```sql
> -- GROUPING SETS: agrupa por multiples combinaciones
> SELECT u.name, o.status, COUNT(*), SUM(o.total)
> FROM users u JOIN orders o ON u.id = o.user_id
> GROUP BY GROUPING SETS ((u.name), (o.status), ());
>
> -- CUBE genera todas las combinaciones posibles
> SELECT u.name, o.status, COUNT(*), SUM(o.total)
> FROM users u JOIN orders o ON u.id = o.user_id
> GROUP BY CUBE (u.name, o.status);
> ```
> `GROUPING SETS` es mas eficiente que hacer varias consultas con GROUP BY diferentes y unirlas con UNION.

---

#### 6. COALESCE con multiples argumentos (PostgreSQL tip)

```sql
-- COALESCE puede tomar mas de 2 argumentos
-- Devuelve el primer valor no nulo de la lista
SELECT
    u.name AS usuario,
    COALESCE(
        SUM(o.total),        -- 1. intenta el total calculado
        0                    -- 2. si es NULL, devuelve 0
    ) AS total_gastado,
    COALESCE(
        o.note,              -- 1. intenta nota de pedido
        u.name || ' has no notes',  -- 2. crea un mensaje por defecto
        'No info'            -- 3. fallback definitivo (nunca se alcanza si el 2 es no nulo)
    ) AS nota
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
GROUP BY u.id, u.name, o.note;
```

> `COALESCE` acepta cualquier numero de argumentos, lo que le permite implementar una cadena de valores por defecto. Es util para llenar campos opcionales en reportes.

---

### Tip del Profesor

- **Subconsultas vs JOINs:** Las subconsultas correlacionadas son a menudo mas lentas que los JOINs equivalentes. Para la mayoria de los casos, prefiere `LEFT JOIN + GROUP BY` antes que subconsultas en el SELECT. Las subconsultas derivadas (FROM) suelen ser mas eficientes.
- **GROUP BY con HAVING o WHERE:** `WHERE` filtra filas antes de la agrupacion; `HAVING` filtra grupos despues de la agregacion. Recuerda: `WHERE` va antes de `GROUP BY`, `HAVING` va despues.
- **GROUP BY sin columnas de la tabla agrupada:** Siempre agrupa por la clave primaria (o conjunto unico) de la tabla principal. En el ejemplo, se agrupa por `u.id, u.name` para que dos usuarios con el mismo nombre no se mezclen. En PostgreSQL, si agrupas por `u.id`, puedes seleccionar cualquier columna de `users.u`; en MySQL (dependiendo de `sql_mode`), puedes tener un comportamiento permisivo que genera resultados impredecibles.
- **COALESCE vs IFNULL:** `COALESCE` es estandar SQL y funciona en MySQL, PostgreSQL, SQLite, Oracle, etc. `IFNULL` es especifico de MySQL. Usa `COALESCE` a menos que tengas una razon especifica para no hacerlo.
- **PostgreSQL GROUP BY avanzado:** `ROLLUP`, `CUBE` y `GROUPING SETS` son caracteristicas excelentes de PostgreSQL para generar reportes analiticos completos en una sola consulta. Invierta tiempo en aprenderlas si trabajas frecuentemente con data warehousing.

---

## Resumen

* **Subconsultas**: permiten calcular valores derivados por cada fila (utiles, pero pueden ser mas lentas que JOINs en grandes volumenes de datos).
* **GROUP BY**: agrupa registros y permite aplicar funciones de agregacion como `SUM()`, `COUNT()`, `AVG()`, etc.
* **HAVING**: filtra resultados despues de aplicar las funciones de agregacion.
* **WHERE vs HAVING**: `WHERE` filtra filas, `HAVING` filtra grupos. No se pueden intercambiar.
* **COALESCE()**: reemplaza valores nulos para evitar resultados incompletos. Estandar SQL, funciona en todos los motores.
* **ROLLUP / CUBE / GROUPING SETS**: Extensiones de GROUP BY para generar subtotales y totales. Soportados por PostgreSQL y MySQL 8+.

Estas tecnicas son la base de los reportes analiticos en SQL, especialmente para obtener metricas por usuario, categoria o periodo de tiempo.
