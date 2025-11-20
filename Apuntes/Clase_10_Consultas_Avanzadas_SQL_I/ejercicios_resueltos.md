# Ejercicios Resueltos - Clase 10: JOIN, Subconsultas y Agrupamiento (SQL Avanzado)

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
