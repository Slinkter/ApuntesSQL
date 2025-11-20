# SQL Intermedio: Consultas Complejas y Lógica de Negocio

En esta sección, las consultas se vuelven más complejas, permitiendo análisis más profundos y la implementación de lógica de negocio.

## 1. Uniones de Tablas Avanzadas (`JOIN`)

### `LEFT JOIN`
**Objetivo:** Devolver todas las filas de la tabla izquierda y las filas coincidentes de la tabla derecha. Si no hay coincidencia, el resultado es `NULL` en el lado derecho.

35. **Listar todos los clientes y los pedidos que han realizado. Incluir clientes que no han hecho pedidos.**
    ```sql
    SELECT c.ContactName, o.OrderID
    FROM Customers c
    LEFT JOIN Orders o ON c.CustomerID = o.CustomerID;
    ```

36. **Mostrar todos los productos y, si han sido pedidos, la cantidad vendida. Incluir productos nunca vendidos.**
    ```sql
    SELECT p.ProductName, od.Quantity
    FROM Products p
    LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID;
    ```

### `RIGHT JOIN`
**Objetivo:** Devolver todas las filas de la tabla derecha y las filas coincidentes de la tabla izquierda. Es menos común que `LEFT JOIN`.

37. **Listar todos los empleados y los pedidos que han gestionado. Incluir empleados que no han gestionado pedidos.**
    ```sql
    SELECT e.FirstName, e.LastName, o.OrderID
    FROM Orders o
    RIGHT JOIN Employees e ON o.EmployeeID = e.EmployeeID;
    ```

### `JOIN` con Múltiples Tablas
**Objetivo:** Combinar datos de tres o más tablas.

38. **Para el pedido 10250, mostrar el nombre del cliente, el nombre del producto y la cantidad.**
    ```sql
    SELECT c.ContactName, p.ProductName, od.Quantity
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    WHERE o.OrderID = 10250;
    ```

39. **Mostrar el nombre del cliente, el empleado que lo atendió y el transportista para cada pedido.**
    ```sql
    SELECT o.OrderID, c.ContactName, e.FirstName AS Employee, s.CompanyName AS Shipper
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN Employees e ON o.EmployeeID = e.EmployeeID
    JOIN Shippers s ON o.ShipVia = s.ShipperID;
    ```

## 2. Subconsultas (Subqueries)

**Objetivo:** Anidar una consulta `SELECT` dentro de otra consulta.

### Subconsulta en la Cláusula `WHERE`
40. **Encontrar todos los productos suministrados por proveedores de Japón.**
    ```sql
    SELECT ProductName
    FROM Products
    WHERE SupplierID IN (SELECT SupplierID FROM Suppliers WHERE Country = 'Japan');
    ```

41. **Listar los clientes que han realizado pedidos después del '1998-03-01'.**
    ```sql
    SELECT ContactName
    FROM Customers
    WHERE CustomerID IN (SELECT CustomerID FROM Orders WHERE OrderDate > '1998-03-01');
    ```

### Subconsulta en la Cláusula `FROM`
42. **Calcular el promedio de la cantidad de productos por pedido.**
    ```sql
    SELECT AVG(TotalProducts)
    FROM (SELECT OrderID, COUNT(ProductID) AS TotalProducts FROM OrderDetails GROUP BY OrderID) AS OrderCounts;
    ```

### Subconsulta Correlacionada
**Objetivo:** Una subconsulta que depende de la consulta externa para sus valores. Se ejecuta una vez por cada fila de la consulta externa.

43. **Encontrar productos cuyo precio es superior al precio promedio de los productos de su misma categoría.**
    ```sql
    SELECT ProductName, UnitPrice
    FROM Products p1
    WHERE p1.UnitPrice > (SELECT AVG(UnitPrice) FROM Products p2 WHERE p2.CategoryID = p1.CategoryID);
    ```
    
58. **(Extra) Encontrar los pedidos que contienen el producto 'Chai'**
    ```sql
    SELECT * FROM Orders
    WHERE OrderID IN (
        SELECT OrderID FROM OrderDetails
        WHERE ProductID = (SELECT ProductID FROM Products WHERE ProductName = 'Chai')
    );
    ```

## 3. Cláusula `HAVING`

**Objetivo:** Filtrar grupos basados en una condición de agregación, a diferencia de `WHERE` que filtra filas.

44. **Encontrar países con más de 5 clientes.**
    ```sql
    SELECT Country, COUNT(*)
    FROM Customers
    GROUP BY Country
    HAVING COUNT(*) > 5;
    ```

45. **Listar los empleados que han gestionado más de 80 pedidos.**
    ```sql
    SELECT EmployeeID, COUNT(OrderID)
    FROM Orders
    GROUP BY EmployeeID
    HAVING COUNT(OrderID) > 80;
    ```

46. **Mostrar las categorías donde el precio promedio del producto es mayor a $30.**
    ```sql
    SELECT CategoryID, AVG(UnitPrice)
    FROM Products
    GROUP BY CategoryID
    HAVING AVG(UnitPrice) > 30;
    ```
    
59. **(Extra) Mostrar los proveedores que suministran más de 3 productos.**
    ```sql
    SELECT s.ContactName, COUNT(p.ProductID) AS NumberOfProducts
    FROM Suppliers s
    JOIN Products p ON s.SupplierID = p.SupplierID
    GROUP BY s.SupplierID
    HAVING COUNT(p.ProductID) > 3;
    ```

## 4. `CASE` Statement

**Objetivo:** Añadir lógica condicional (if-then-else) a las consultas.

47. **Clasificar productos por precio: 'Barato' si es < $20, 'Medio' si es entre $20 y $50, 'Caro' si es > $50.**
    ```sql
    SELECT ProductName, UnitPrice,
           CASE
               WHEN UnitPrice < 20 THEN 'Barato'
               WHEN UnitPrice BETWEEN 20 AND 50 THEN 'Medio'
               ELSE 'Caro'
           END AS PriceCategory
    FROM Products;
    ```

48. **Mostrar el nombre del cliente y un comentario sobre su ubicación ('Local' si es de USA, 'Extranjero' si no).**
    ```sql
    SELECT ContactName, Country,
           CASE
               WHEN Country = 'USA' THEN 'Local'
               ELSE 'Extranjero'
           END AS Location
    FROM Customers;
    ```

60. **(Extra) Contar pedidos por prioridad de envío ('Normal', 'Urgente' si es de USA).**
    ```sql
    SELECT OrderID, CustomerID,
           CASE
               WHEN ShipCountry = 'USA' THEN 'Urgente'
               ELSE 'Normal'
           END AS ShippingPriority
    FROM Orders;
    ```

## 5. Expresiones de Tabla Comunes (CTEs - Common Table Expressions)

**Objetivo:** Simplificar consultas complejas y hacerlas más legibles. Una CTE es una tabla temporal con nombre que existe solo para la consulta.

49. **Usar una CTE para listar los clientes de Londres y luego mostrar sus pedidos.**
    ```sql
    WITH LondonCustomers AS (
        SELECT CustomerID, ContactName
        FROM Customers
        WHERE City = 'London'
    )
    SELECT lc.ContactName, o.OrderID
    FROM LondonCustomers lc
    JOIN Orders o ON lc.CustomerID = o.CustomerID;
    ```

50. **Encontrar el total de ventas por cada categoría de producto usando una CTE.**
    ```sql
    WITH ProductSales AS (
        SELECT p.CategoryID, od.Quantity * od.UnitPrice AS SaleAmount
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
    )
    SELECT cat.CategoryName, SUM(ps.SaleAmount) AS TotalSales
    FROM ProductSales ps
    JOIN Categories cat ON ps.CategoryID = cat.CategoryID
    GROUP BY cat.CategoryName
    ORDER BY TotalSales DESC;
    ```

61. **(Extra) Listar los 5 clientes con mayor gasto total.**
    ```sql
    WITH CustomerSpending AS (
        SELECT c.CustomerID, c.ContactName, SUM(od.Quantity * od.UnitPrice) AS TotalSpent
        FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY c.CustomerID, c.ContactName
    )
    SELECT ContactName, TotalSpent
    FROM CustomerSpending
    ORDER BY TotalSpent DESC
    LIMIT 5;
    ```

## 6. Funciones de Ventana (Window Functions)

**Objetivo:** Realizar cálculos a través de un conjunto de filas de tabla que están de alguna manera relacionadas con la fila actual.

### `ROW_NUMBER`, `RANK`, `DENSE_RANK`
51. **Asignar un número de fila único a cada producto, ordenado por precio.**
    ```sql
    SELECT ProductName, UnitPrice,
           ROW_NUMBER() OVER (ORDER BY UnitPrice DESC) AS RowNum
    FROM Products;
    ```

52. **Clasificar productos por precio dentro de cada categoría.**
    ```sql
    SELECT ProductName, CategoryID, UnitPrice,
           RANK() OVER (PARTITION BY CategoryID ORDER BY UnitPrice DESC) AS PriceRank
    FROM Products;
    ```

### `LEAD` y `LAG`
53. **Para cada pedido, mostrar la fecha del pedido y la fecha del siguiente pedido del mismo cliente.**
    ```sql
    SELECT CustomerID, OrderDate,
           LEAD(OrderDate, 1) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS NextOrderDate
    FROM Orders;
    ```
54. **Mostrar el total de una venta y el total de la venta anterior del mismo cliente.**
    ```sql
    WITH CustomerSales AS (
        SELECT o.CustomerID, o.OrderID, o.OrderDate, SUM(od.Quantity * od.UnitPrice) as OrderTotal
        FROM Orders o JOIN OrderDetails od on o.OrderID = od.OrderID
        GROUP BY o.CustomerID, o.OrderID, o.OrderDate
    )
    SELECT CustomerID, OrderID, OrderDate, OrderTotal,
           LAG(OrderTotal, 1, 0) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS PreviousOrderTotal
    FROM CustomerSales;
    ```
### Agregaciones con `OVER`
55. **Mostrar el precio de cada producto junto con el precio promedio de su categoría.**
    ```sql
    SELECT ProductName, UnitPrice, CategoryID,
           AVG(UnitPrice) OVER (PARTITION BY CategoryID) AS AvgCategoryPrice
    FROM Products;
    ```

62. **(Extra) Calcular el total de ventas acumulado por mes.**
    ```sql
    WITH MonthlySales AS (
        SELECT
            DATE_FORMAT(OrderDate, '%Y-%m') AS SaleMonth,
            SUM(od.Quantity * od.UnitPrice) AS MonthlyTotal
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY SaleMonth
    )
    SELECT
        SaleMonth,
        MonthlyTotal,
        SUM(MonthlyTotal) OVER (ORDER BY SaleMonth) AS CumulativeTotal
    FROM MonthlySales;
    ```
    
67. **(Extra) Encontrar el producto más vendido en cada categoría.**
    ```sql
    WITH ProductCategorySales AS (
        SELECT
            p.CategoryID,
            p.ProductName,
            SUM(od.Quantity) as TotalSold,
            RANK() OVER (PARTITION BY p.CategoryID ORDER BY SUM(od.Quantity) DESC) as SalesRank
        FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY p.CategoryID, p.ProductName
    )
    SELECT CategoryID, ProductName, TotalSold
    FROM ProductCategorySales
    WHERE SalesRank = 1;
    ```

## 7. `UNION` y `UNION ALL`

**Objetivo:** Combinar el conjunto de resultados de dos o más consultas `SELECT`. `UNION` elimina duplicados, `UNION ALL` no.

56. **Obtener una lista única de todas las ciudades donde viven clientes y proveedores.**
    ```sql
    SELECT City FROM Customers
    UNION
    SELECT City FROM Suppliers
    ORDER BY City;
    ```
57. **Combinar los nombres de los empleados y los nombres de contacto de los clientes en una sola lista.**
    ```sql
    SELECT ContactName FROM Customers
    UNION ALL
    SELECT CONCAT(FirstName, ' ', LastName) FROM Employees;
    ```

## 8. Otros Operadores

### `EXISTS`
**Objetivo:** Comprobar si una subconsulta devuelve alguna fila.

63. **Encontrar todos los clientes que han realizado al menos un pedido.**
    ```sql
    SELECT CustomerID, ContactName
    FROM Customers c
    WHERE EXISTS (SELECT 1 FROM Orders o WHERE o.CustomerID = c.CustomerID);
    ```
    
### `ANY` y `ALL`
**Objetivo:** Comparar un valor con un conjunto de valores devueltos por una subconsulta.

64. **Encontrar productos cuyo precio es mayor que CUALQUIER producto de la categoría 1.**
    ```sql
    SELECT ProductName, UnitPrice
    FROM Products
    WHERE UnitPrice > ANY (SELECT UnitPrice FROM Products WHERE CategoryID = 1);
    ```

## 9. Joins Adicionales
    
65. **(Extra) Listar las ventas totales por empleado.**
    ```sql
    SELECT e.FirstName, e.LastName, SUM(od.Quantity * od.UnitPrice) as TotalSales
    FROM Employees e
    JOIN Orders o ON e.EmployeeID = o.EmployeeID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY e.EmployeeID
    ORDER BY TotalSales DESC;
    ```
66. **(Extra) Qué clientes han comprado qué categoría de productos.**
    ```sql
    SELECT DISTINCT c.ContactName, cat.CategoryName
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    JOIN Categories cat ON p.CategoryID = cat.CategoryID
    ORDER BY c.ContactName, cat.CategoryName;
    ```
