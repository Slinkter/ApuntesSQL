# 🔗 Clase 10: JOIN, Subconsultas y Agrupamiento (SQL Avanzado)

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **JOIN (Unión)** | Un `JOIN` se usa para consultar datos que están en **más de una tabla**. Enlazamos filas usando valores comunes, generalmente entre la PK y la FK. |
| **Cross Join (Producto Cartesiano)** | ¡El **JOIN que no quieres**! Sucede si olvidas la condición de unión. Junta *cada* fila de la primera tabla con *cada* fila de la segunda. ¡El resultado es enorme y sin sentido!. |
| **Tipos de JOIN** | **Equijoin:** El más común; une tablas cuando las columnas son **iguales** (`=`). **Non-Equijoin:** Usa otros operadores (como `BETWEEN` o `>`). **Self Join:** Una tabla se une **consigo misma** (usando alias), útil para relaciones recursivas (Ej. Empleado y Jefe). |
| **Outer Join (LEFT/RIGHT)** | Se utiliza para ver las filas que **normalmente no se mostrarían**. Por ejemplo, un `LEFT OUTER JOIN` muestra todos los clientes, *incluso* si no tienen pedidos relacionados. |
| **Subconsultas** | Es una consulta **anidada** que se ejecuta *primero*. El resultado de la subconsulta (interna) alimenta a la consulta principal (externa). ¡Son perfectas cuando la condición de tu `WHERE` se basa en un valor que no conoces de antemano!. |
| **Funciones de Agrupamiento** | Son funciones que operan sobre conjuntos de filas: `MIN`, `MAX`, `AVG` (promedio), `SUM` y `COUNT`. |
| **GROUP BY y HAVING** | **GROUP BY** divide las filas en subconjuntos y aplica las funciones de agrupamiento a cada uno (Ej. agrupar por `tipo` de cliente y contar cuántos hay). **HAVING** es como el `WHERE`, pero se usa para **filtrar los grupos** (Ej. "Muéstrame solo los grupos donde el conteo sea mayor a 5"). |

**Resumen de la Clase 10:** El `SELECT` avanzado se basa en el `JOIN` para combinar datos de múltiples tablas (evitando el *Cross Join*). Las Subconsultas permiten consultas dinámicas, y el uso de `GROUP BY` y `HAVING` nos da el poder de analizar y filtrar los datos en conjuntos (agrupamiento).

---

---

## 💡 Ejemplos Prácticos

Para los siguientes ejemplos, asumiremos las siguientes tablas simplificadas:

**Tabla `EMPLEADOS`**

| ID_Empleado | Nombre    | Apellido  | ID_Departamento | Salario |
| :---------- | :-------- | :-------- | :-------------- | :------ |
| 1           | Ana       | García    | 10              | 50000   |
| 2           | Luis      | Pérez     | 20              | 55000   |
| 3           | Marta     | Sánchez   | 10              | 52000   |
| 4           | Pedro     | Ramírez   | 30              | 60000   |
| 5           | Sofía     | Díaz      | 20              | 58000   |
| 6           | Elena     | Torres    | NULL            | 62000   |

**Tabla `DEPARTAMENTOS`**

| ID_Departamento | Nombre_Departamento | Ubicacion |
| :-------------- | :------------------ | :-------- |
| 10              | Ventas              | Madrid    |
| 20              | Marketing           | Barcelona |
| 30              | TI                  | Madrid    |
| 40              | I+D                 | Valencia  |

### Ejemplo 1: INNER JOIN (Equijoin)

**Objetivo:** Obtener el nombre de los empleados y el nombre de su departamento.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |

### Ejemplo 2: LEFT JOIN (LEFT OUTER JOIN)

**Objetivo:** Obtener todos los empleados y, si tienen, el nombre de su departamento. Queremos ver también a los empleados sin departamento.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
LEFT JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |
| Elena  | Torres   | NULL                |

### Ejemplo 3: RIGHT JOIN (RIGHT OUTER JOIN)

**Objetivo:** Obtener todos los departamentos y, si tienen, los empleados asignados. Queremos ver también los departamentos sin empleados.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
RIGHT JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |
| NULL   | NULL     | I+D                 |

### Ejemplo 4: Self Join

**Objetivo:** Encontrar empleados que ganan más que su propio manager (asumiendo que `ID_Jefe` es una FK a `ID_Empleado` en la misma tabla `EMPLEADOS`).

**Tabla `EMPLEADOS_CON_JEFE`** (asumiendo una columna `ID_Jefe`)

| ID_Empleado | Nombre    | Salario | ID_Jefe |
| :---------- | :-------- | :------ | :------ |
| 1           | Ana       | 50000   | NULL    |
| 2           | Luis      | 55000   | 1       |
| 3           | Marta     | 52000   | 1       |
| 4           | Pedro     | 60000   | 2       |

```sql
SELECT E.Nombre AS Empleado, E.Salario AS SalarioEmpleado,
       J.Nombre AS Jefe, J.Salario AS SalarioJefe
FROM EMPLEADOS_CON_JEFE E
INNER JOIN EMPLEADOS_CON_JEFE J ON E.ID_Jefe = J.ID_Empleado
WHERE E.Salario > J.Salario;
```

**Resultado (ejemplo hipotético):**

| Empleado | SalarioEmpleado | Jefe | SalarioJefe |
| :------- | :-------------- | :--- | :---------- |
| Pedro    | 60000           | Luis | 55000       |

### Ejemplo 5: Subconsulta Escalar en WHERE

**Objetivo:** Encontrar los empleados cuyo salario es mayor que el salario promedio de todos los empleados.

```sql
SELECT Nombre, Apellido, Salario
FROM EMPLEADOS
WHERE Salario > (SELECT AVG(Salario) FROM EMPLEADOS);
```

**Resultado (si AVG(Salario) es, por ejemplo, 55000):**

| Nombre | Apellido | Salario |
| :----- | :------- | :------ |
| Pedro  | Ramírez  | 60000   |
| Sofía  | Díaz     | 58000   |
| Elena  | Torres   | 62000   |

### Ejemplo 6: Funciones de Agregación con GROUP BY

**Objetivo:** Contar cuántos empleados hay en cada departamento y cuál es el salario promedio por departamento.

```sql
SELECT D.Nombre_Departamento, COUNT(E.ID_Empleado) AS Num_Empleados, AVG(E.Salario) AS Salario_Promedio
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento
GROUP BY D.Nombre_Departamento;
```

**Resultado:**

| Nombre_Departamento | Num_Empleados | Salario_Promedio |
| :------------------ | :------------ | :--------------- |
| Ventas              | 2             | 51000            |
| Marketing           | 2             | 56500            |
| TI                  | 1             | 60000            |

### Ejemplo 7: GROUP BY con HAVING

**Objetivo:** Mostrar los departamentos donde el salario promedio de sus empleados es superior a 52000.

```sql
SELECT D.Nombre_Departamento, AVG(E.Salario) AS Salario_Promedio
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento
GROUP BY D.Nombre_Departamento
HAVING AVG(E.Salario) > 52000;
```

**Resultado:**

| Nombre_Departamento | Salario_Promedio |
| :------------------ | :--------------- |
| Marketing           | 56500            |
| TI                  | 60000            |

---

## ✏️ Ejercicios Resueltos

Para los siguientes ejercicios, utilizaremos las siguientes tablas:

**Tabla `PEDIDOS`**

| ID_Pedido | ID_Cliente | Fecha_Pedido | Total_Pedido |
| :-------- | :--------- | :----------- | :----------- |
| 1         | 101        | 2023-01-05   | 150.00       |
| 2         | 102        | 2023-01-05   | 200.00       |
| 3         | 101        | 2023-01-06   | 50.00        |
| 4         | 103        | 2023-01-07   | 300.00       |
| 5         | 101        | 2023-01-07   | 100.00       |

**Tabla `CLIENTES`**

| ID_Cliente | Nombre_Cliente | Ciudad    |
| :--------- | :------------- | :-------- |
| 101        | Ana            | Madrid    |
| 102        | Luis           | Barcelona |
| 103        | Marta          | Madrid    |
| 104        | Pedro          | Sevilla   |

**Tabla `DETALLE_PEDIDO`**

| ID_Detalle | ID_Pedido | ID_Producto | Cantidad | Precio_Unitario |
| :--------- | :-------- | :---------- | :------- | :-------------- |
| 1          | 1         | 10          | 2        | 75.00           |
| 2          | 1         | 11          | 1        | 0.00            |
| 3          | 2         | 12          | 4        | 50.00           |
| 4          | 3         | 10          | 1        | 50.00           |
| 5          | 4         | 13          | 3        | 100.00          |
| 6          | 5         | 11          | 5        | 20.00           |

**Tabla `PRODUCTOS`**

| ID_Producto | Nombre_Producto | Categoria |
| :---------- | :-------------- | :-------- |
| 10          | Laptop          | Electrónica |
| 11          | Teclado         | Electrónica |
| 12          | Mouse           | Electrónica |
| 13          | Silla           | Oficina   |

### Ejercicio 1: JOIN

**Enunciado:**
1.  Obtén el `ID_Pedido`, `Fecha_Pedido`, `Nombre_Cliente` y `Ciudad` para todos los pedidos.
2.  Lista todos los productos (Nombre_Producto) y, si han sido pedidos, la `Cantidad` de cada pedido. Incluye también los productos que nunca han sido pedidos.
3.  Obtén el `Nombre_Cliente` y el `Nombre_Producto` para todos los ítems de pedido.

**Solución:**

1.  **Pedidos con datos del cliente:**
    ```sql
    SELECT P.ID_Pedido, P.Fecha_Pedido, C.Nombre_Cliente, C.Ciudad
    FROM PEDIDOS P
    INNER JOIN CLIENTES C ON P.ID_Cliente = C.ID_Cliente;
    ```
2.  **Todos los productos y sus cantidades en pedidos (incluyendo los no pedidos):**
    ```sql
    SELECT PR.Nombre_Producto, DP.Cantidad
    FROM PRODUCTOS PR
    LEFT JOIN DETALLE_PEDIDO DP ON PR.ID_Producto = DP.ID_Producto;
    ```
3.  **Nombre de cliente y nombre de producto por ítem de pedido:**
    ```sql
    SELECT CL.Nombre_Cliente, PR.Nombre_Producto
    FROM CLIENTES CL
    INNER JOIN PEDIDOS PE ON CL.ID_Cliente = PE.ID_Cliente
    INNER JOIN DETALLE_PEDIDO DP ON PE.ID_Pedido = DP.ID_Pedido
    INNER JOIN PRODUCTOS PR ON DP.ID_Producto = PR.ID_Producto;
    ```

### Ejercicio 2: Subconsultas

**Enunciado:**
1.  Encuentra los `Nombre_Cliente` de los clientes que han realizado al menos un pedido.
2.  Lista todos los `Nombre_Producto` que aparecen en algún pedido realizado por un cliente de "Madrid".

**Solución:**

1.  **Clientes que han realizado pedidos:**
    ```sql
    SELECT Nombre_Cliente
    FROM CLIENTES
    WHERE ID_Cliente IN (SELECT ID_Cliente FROM PEDIDOS);
    ```
2.  **Productos pedidos por clientes de Madrid:**
    ```sql
    SELECT Nombre_Producto
    FROM PRODUCTOS
    WHERE ID_Producto IN (
        SELECT DP.ID_Producto
        FROM DETALLE_PEDIDO DP
        INNER JOIN PEDIDOS PE ON DP.ID_Pedido = PE.ID_Pedido
        INNER JOIN CLIENTES CL ON PE.ID_Cliente = CL.ID_Cliente
        WHERE CL.Ciudad = 'Madrid'
    );
    ```

### Ejercicio 3: Agrupamiento con GROUP BY y HAVING

**Enunciado:**
1.  Calcula el número total de pedidos y el `Total_Pedido` promedio por cada `ID_Cliente`.
2.  Encuentra las ciudades que tienen más de un cliente.
3.  Lista los `ID_Cliente` que han realizado pedidos por un `Total_Pedido` acumulado superior a 200.

**Solución:**

1.  **Número de pedidos y total promedio por cliente:**
    ```sql
    SELECT ID_Cliente, COUNT(ID_Pedido) AS NumeroPedidos, AVG(Total_Pedido) AS PromedioTotal
    FROM PEDIDOS
    GROUP BY ID_Cliente;
    ```
2.  **Ciudades con más de un cliente:**
    ```sql
    SELECT Ciudad, COUNT(ID_Cliente) AS Num_Clientes
    FROM CLIENTES
    GROUP BY Ciudad
    HAVING COUNT(ID_Cliente) > 1;
    ```
3.  **Clientes con total de pedidos acumulado superior a 200:**
    ```sql
    SELECT ID_Cliente, SUM(Total_Pedido) AS TotalAcumulado
    FROM PEDIDOS
    GROUP BY ID_Cliente
    HAVING SUM(Total_Pedido) > 200;
    ```

---

