# SQL Avanzado: Consultas de Alta Complejidad y Análisis de Datos

Esta sección aborda escenarios complejos que requieren un profundo conocimiento de SQL para resolver problemas de negocio, realizar análisis de datos avanzados y optimizar el rendimiento.

## 1. Expresiones de Tabla Comunes Recursivas (Recursive CTEs)

**Objetivo:** Consultar datos jerárquicos, como la estructura de mando de una organización.

68. **Mostrar la jerarquía de empleados, indicando quién reporta a quién.**
    *Nota: La tabla `Employees` tiene una columna `ReportsTo` que se refiere al `EmployeeID` del jefe.*
    ```sql
    WITH RECURSIVE EmployeeHierarchy AS (
        -- Anchor member: el nivel más alto (empleados que no reportan a nadie)
        SELECT EmployeeID, CONCAT(FirstName, ' ', LastName) AS EmployeeName, ReportsTo, 0 AS Level
        FROM Employees
        WHERE ReportsTo IS NULL

        UNION ALL

        -- Recursive member: une la CTE consigo misma para encontrar subordinados
        SELECT e.EmployeeID, CONCAT(e.FirstName, ' ', e.LastName), e.ReportsTo, eh.Level + 1
        FROM Employees e
        INNER JOIN EmployeeHierarchy eh ON e.ReportsTo = eh.EmployeeID
    )
    SELECT * FROM EmployeeHierarchy ORDER BY Level, ReportsTo;
    ```

## 2. Simulación de `PIVOT`

**Objetivo:** Rotar filas en columnas. MySQL no tiene un operador `PIVOT` nativo como SQL Server, pero se puede simular con agregación condicional.

69. **Mostrar el total de pedidos por año, con cada año en una columna separada para cada cliente.**
    ```sql
    SELECT
        c.ContactName,
        SUM(CASE WHEN YEAR(o.OrderDate) = 1996 THEN 1 ELSE 0 END) AS Orders1996,
        SUM(CASE WHEN YEAR(o.OrderDate) = 1997 THEN 1 ELSE 0 END) AS Orders1997,
        SUM(CASE WHEN YEAR(o.OrderDate) = 1998 THEN 1 ELSE 0 END) AS Orders1998
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    GROUP BY c.ContactName
    ORDER BY c.ContactName;
    ```

70. **Mostrar la cantidad total de productos vendidos por categoría, con cada categoría como una columna.**
    ```sql
    SELECT
        p.ProductName,
        SUM(CASE WHEN c.CategoryName = 'Beverages' THEN od.Quantity ELSE 0 END) AS Beverages,
        SUM(CASE WHEN c.CategoryName = 'Condiments' THEN od.Quantity ELSE 0 END) AS Condiments,
        SUM(CASE WHEN c.CategoryName = 'Confections' THEN od.Quantity ELSE 0 END) AS Confections
        -- ... (se pueden añadir más categorías)
    FROM OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    JOIN Categories c ON p.CategoryID = c.CategoryID
    GROUP BY p.ProductName
    LIMIT 10; -- Para una vista más limpia
    ```

## 3. Funciones de Ventana Avanzadas

**Objetivo:** Utilizar marcos de ventana (`ROWS BETWEEN`) para cálculos como promedios móviles.

71. **Calcular el promedio móvil de 3 días de las ventas totales.**
    ```sql
    WITH DailySales AS (
        SELECT
            OrderDate,
            SUM(od.UnitPrice * od.Quantity) AS TotalSale
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY OrderDate
    )
    SELECT
        OrderDate,
        TotalSale,
        AVG(TotalSale) OVER (ORDER BY OrderDate ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MovingAvg3Days
    FROM DailySales;
    ```
    
## 4. Consultas Temporales y `SELF JOIN`

**Objetivo:** Unir una tabla consigo misma para comparar filas dentro de la misma tabla.

72. **Encontrar clientes que viven en la misma ciudad.**
    ```sql
    SELECT A.ContactName, B.ContactName, A.City
    FROM Customers A, Customers B
    WHERE A.CustomerID < B.CustomerID -- Evita duplicados (A,B) y (B,A) y auto-comparaciones (A,A)
    AND A.City = B.City
    ORDER BY A.City;
    ```

73. **Encontrar productos que a menudo se compran juntos (en el mismo pedido).**
    ```sql
    SELECT
        p1.ProductName AS Product1,
        p2.ProductName AS Product2,
        COUNT(*) AS Frequency
    FROM OrderDetails od1
    JOIN OrderDetails od2 ON od1.OrderID = od2.OrderID AND od1.ProductID < od2.ProductID
    JOIN Products p1 ON od1.ProductID = p1.ProductID
    JOIN Products p2 ON od2.ProductID = p2.ProductID
    GROUP BY p1.ProductName, p2.ProductName
    ORDER BY Frequency DESC
    LIMIT 10;
    ```

## 5. Análisis de Cohortes (Cohort Analysis)

**Objetivo:** Agrupar usuarios basados en cuándo realizaron su primera acción (p. ej., su primera compra) y seguir su comportamiento a lo largo del tiempo.

74. **Análisis de cohorte: Calcular la retención mensual de clientes.**
    ```sql
    WITH CustomerFirstOrder AS (
        SELECT
            CustomerID,
            DATE_FORMAT(MIN(OrderDate), '%Y-%m') AS CohortMonth
        FROM Orders
        GROUP BY CustomerID
    ),
    MonthlyOrders AS (
        SELECT DISTINCT
            CustomerID,
            DATE_FORMAT(OrderDate, '%Y-%m') AS OrderMonth
        FROM Orders
    ),
    CohortRetention AS (
      SELECT
        cfo.CohortMonth,
        TIMESTAMPDIFF(MONTH, STR_TO_DATE(cfo.CohortMonth, '%Y-%m'), STR_TO_DATE(mo.OrderMonth, '%Y-%m')) as MonthsSinceFirstOrder,
        COUNT(DISTINCT mo.CustomerID) as RetainedCustomers
      FROM CustomerFirstOrder cfo
      JOIN MonthlyOrders mo ON cfo.CustomerID = mo.CustomerID
      GROUP BY 1, 2
    )
    SELECT * FROM CohortRetention ORDER BY 1, 2;
    ```

## 6. Consultas de Integridad de Datos

**Objetivo:** Encontrar inconsistencias o problemas en los datos.

75. **Encontrar pedidos que no tienen detalles (posible error de datos).**
    ```sql
    SELECT o.OrderID
    FROM Orders o
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE od.OrderID IS NULL;
    ```

76. **Verificar si hay productos con stock negativo (lo cual no debería ser posible).**
    ```sql
    SELECT * FROM Products WHERE UnitsInStock < 0;
    ```

77. **Encontrar duplicados en la tabla de clientes basados en el nombre de la compañía y el contacto.**
    ```sql
    SELECT CompanyName, ContactName, COUNT(*)
    FROM Customers
    GROUP BY CompanyName, ContactName
    HAVING COUNT(*) > 1;
    ```
    
86. **(Extra) Listar los productos que nunca se han vendido.**
    ```sql
    SELECT p.ProductName
    FROM Products p
    LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
    WHERE od.OrderID IS NULL;
    ```

## 7. Optimización de Consultas (`EXPLAIN`)

**Objetivo:** Entender cómo la base de datos ejecuta una consulta para identificar cuellos de botella.

78. **Analizar el plan de ejecución de una consulta compleja.**
    ```sql
    EXPLAIN SELECT c.ContactName, p.ProductName
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    WHERE c.Country = 'Germany';
    ```
    **Cómo leer `EXPLAIN`:**
    - `type`: El tipo de join. `ALL` (full table scan) es malo. `ref`, `eq_ref`, `index` son mejores.
    - `key`: El índice que se está utilizando. Si es `NULL`, puede ser una oportunidad de mejora.
    - `rows`: El número estimado de filas que MySQL debe leer. Un número más bajo es mejor.

## 8. Escenarios de Entrevista Adicionales

79. **Encontrar el segundo empleado con más ventas.**
    ```sql
    WITH EmployeeSales AS (
        SELECT
            e.EmployeeID,
            CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
            SUM(od.Quantity * od.UnitPrice) AS TotalSales,
            DENSE_RANK() OVER (ORDER BY SUM(od.Quantity * od.UnitPrice) DESC) AS SalesRank
        FROM Employees e
        JOIN Orders o ON e.EmployeeID = o.EmployeeID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY e.EmployeeID
    )
    SELECT EmployeeName, TotalSales
    FROM EmployeeSales
    WHERE SalesRank = 2;
    ```

81. **(LATERAL JOIN - MySQL 8+) Obtener los 3 productos más caros de cada categoría.**
    ```sql
    -- Esto requiere MySQL 8.0+
    SELECT c.CategoryName, p_lat.ProductName, p_lat.UnitPrice
    FROM Categories c
    CROSS JOIN LATERAL (
        SELECT p.ProductName, p.UnitPrice
        FROM Products p
        WHERE p.CategoryID = c.CategoryID
        ORDER BY p.UnitPrice DESC
        LIMIT 3
    ) AS p_lat;
    ```

82. **Calcular el porcentaje del total de ventas que representa cada producto.**
    ```sql
    WITH ProductSales AS (
        SELECT
            p.ProductName,
            SUM(od.Quantity * od.UnitPrice) AS ProductTotal
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
        GROUP BY p.ProductName
    ),
    TotalSales AS (
        SELECT SUM(ProductTotal) AS GrandTotal FROM ProductSales
    )
    SELECT
        ps.ProductName,
        ps.ProductTotal,
        (ps.ProductTotal / ts.GrandTotal) * 100 AS PercentageOfTotal
    FROM ProductSales ps, TotalSales ts
    ORDER BY PercentageOfTotal DESC;
    ```
    
83. **Encontrar clientes que solo han comprado productos de una única categoría.**
    ```sql
    SELECT c.ContactName
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    GROUP BY c.ContactName
    HAVING COUNT(DISTINCT p.CategoryID) = 1;
    ```

84. **Calcular el tiempo promedio entre pedidos para cada cliente.**
    ```sql
    WITH CustomerOrderDates AS (
        SELECT
            CustomerID,
            OrderDate,
            LAG(OrderDate, 1) OVER (PARTITION BY CustomerID ORDER BY OrderDate) as PreviousOrderDate
        FROM Orders
    )
    SELECT
        CustomerID,
        AVG(DATEDIFF(OrderDate, PreviousOrderDate)) AS AvgDaysBetweenOrders
    FROM CustomerOrderDates
    WHERE PreviousOrderDate IS NOT NULL
    GROUP BY CustomerID;
    ```
    
85. **Determinar el "valor de vida del cliente" (Customer Lifetime Value - LTV).**
    ```sql
    SELECT
        c.ContactName,
        SUM(od.Quantity * od.UnitPrice) AS LifetimeValue
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY c.ContactName
    ORDER BY LifetimeValue DESC;
    ```

87. **Encontrar el mes con las mayores ventas para cada año.**
    ```sql
    WITH MonthlySales AS (
        SELECT
            YEAR(OrderDate) AS SaleYear,
            MONTH(OrderDate) AS SaleMonth,
            SUM(od.Quantity * od.UnitPrice) AS TotalSales
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY SaleYear, SaleMonth
    ),
    RankedSales AS (
        SELECT
            SaleYear,
            SaleMonth,
            TotalSales,
            RANK() OVER (PARTITION BY SaleYear ORDER BY TotalSales DESC) AS SalesRank
        FROM MonthlySales
    )
    SELECT SaleYear, SaleMonth, TotalSales
    FROM RankedSales
    WHERE SalesRank = 1;
    ```
    
88. **Identificar clientes "VIP": aquellos cuyo gasto total está en el 10% superior.**
    ```sql
    WITH CustomerSpending AS (
        SELECT
            CustomerID,
            SUM(od.Quantity * od.UnitPrice) as TotalSpent
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY CustomerID
    ),
    RankedSpending AS (
        SELECT
            CustomerID,
            TotalSpent,
            NTILE(10) OVER (ORDER BY TotalSpent DESC) as SpendingDecile
        FROM CustomerSpending
    )
    SELECT c.ContactName, rs.TotalSpent
    FROM RankedSpending rs
    JOIN Customers c ON rs.CustomerID = c.CustomerID
    WHERE rs.SpendingDecile = 1; -- El primer decil (top 10%)
    ```

90. **Encontrar el producto más popular (en nº de pedidos) de cada proveedor.**
    ```sql
    WITH ProductPopularity AS (
        SELECT
            p.SupplierID,
            p.ProductName,
            COUNT(DISTINCT od.OrderID) AS NumberOfOrders,
            ROW_NUMBER() OVER (PARTITION BY p.SupplierID ORDER BY COUNT(DISTINCT od.OrderID) DESC) as PopularityRank
        FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY p.SupplierID, p.ProductName
    )
    SELECT s.ContactName as Supplier, pp.ProductName, pp.NumberOfOrders
    FROM ProductPopularity pp
    JOIN Suppliers s ON pp.SupplierID = s.SupplierID
    WHERE pp.PopularityRank = 1;
    ```
    
91. **Calcular la diferencia (en días) entre la fecha de un pedido y la fecha del primer pedido de ese cliente.**
    ```sql
    WITH FirstOrderDate AS (
        SELECT CustomerID, MIN(OrderDate) AS FirstDate
        FROM Orders
        GROUP BY CustomerID
    )
    SELECT
        o.OrderID,
        o.CustomerID,
        o.OrderDate,
        fo.FirstDate,
        DATEDIFF(o.OrderDate, fo.FirstDate) AS DaysSinceFirstOrder
    FROM Orders o
    JOIN FirstOrderDate fo ON o.CustomerID = fo.CustomerID
    ORDER BY o.CustomerID, o.OrderDate;
    ```

93. **Ventas por trimestre para el año 1997.**
    ```sql
    SELECT
        QUARTER(OrderDate) AS Quarter,
        SUM(od.Quantity * od.UnitPrice) as QuarterlySales
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE YEAR(OrderDate) = 1997
    GROUP BY QUARTER(OrderDate)
    ORDER BY Quarter;
    ```
    
94. **Listar clientes que no han comprado en los últimos 6 meses (desde la última fecha de pedido en la BD).**
    ```sql
    SELECT c.ContactName
    FROM Customers c
    WHERE c.CustomerID NOT IN (
        SELECT DISTINCT CustomerID
        FROM Orders
        WHERE OrderDate >= (SELECT DATE_SUB(MAX(OrderDate), INTERVAL 6 MONTH) FROM Orders)
    );
    ```

95. **Obtener el crecimiento de ventas mes a mes en porcentaje.**
    ```sql
    WITH MonthlySales AS (
        SELECT
            DATE_FORMAT(OrderDate, '%Y-%m') AS SaleMonth,
            SUM(od.Quantity * od.UnitPrice) AS MonthlyTotal
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY SaleMonth
    ),
    SalesWithLag AS (
        SELECT
            SaleMonth,
            MonthlyTotal,
            LAG(MonthlyTotal, 1, 0) OVER (ORDER BY SaleMonth) AS PreviousMonthTotal
        FROM MonthlySales
    )
    SELECT
        SaleMonth,
        MonthlyTotal,
        PreviousMonthTotal,
        ( (MonthlyTotal - PreviousMonthTotal) / PreviousMonthTotal ) * 100 AS GrowthPercentage
    FROM SalesWithLag
    WHERE PreviousMonthTotal > 0;
    ```
    
96. **Encontrar el número promedio de productos por pedido para cada cliente.**
    ```sql
    WITH ProductsPerOrder AS (
        SELECT
            o.CustomerID,
            o.OrderID,
            COUNT(od.ProductID) AS ProductCount
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY o.CustomerID, o.OrderID
    )
    SELECT
        c.ContactName,
        AVG(ppo.ProductCount) AS AvgProductsPerOrder
    FROM Customers c
    JOIN ProductsPerOrder ppo ON c.CustomerID = ppo.CustomerID
    GROUP BY c.ContactName
    ORDER BY AvgProductsPerOrder DESC;
    ```

97. **Identificar si un cliente es 'Nuevo' o 'Recurrente' en cada pedido.**
    ```sql
    WITH OrderedOrders AS (
      SELECT
        CustomerID,
        OrderDate,
        ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY OrderDate) as rn
      FROM Orders
    )
    SELECT
      oo.CustomerID,
      oo.OrderDate,
      CASE WHEN oo.rn = 1 THEN 'Nuevo' ELSE 'Recurrente' END as CustomerType
    FROM OrderedOrders oo;
    ```

98. **Ranking de productos por ventas totales dentro de cada país.**
    ```sql
    WITH CountryProductSales AS (
        SELECT
            c.Country,
            p.ProductName,
            SUM(od.Quantity * od.UnitPrice) as TotalSales
        FROM Orders o
        JOIN Customers c ON o.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        GROUP BY c.Country, p.ProductName
    ),
    RankedSales AS (
        SELECT
            Country,
            ProductName,
            TotalSales,
            RANK() OVER (PARTITION BY Country ORDER BY TotalSales DESC) as SalesRank
        FROM CountryProductSales
    )
    SELECT Country, ProductName, TotalSales
    FROM RankedSales
    WHERE SalesRank <= 3 -- Top 3 de cada país
    ORDER BY Country, SalesRank;
    ```
    
99. **Encontrar el proveedor con el margen de ganancia promedio más alto (simulado).**
    ```sql
    -- Asumimos que el costo es 70% del UnitPrice
    SELECT
        s.ContactName,
        AVG(p.UnitPrice / (p.UnitPrice * 0.7) - 1) * 100 as AvgProfitMargin
    FROM Products p
    JOIN Suppliers s ON p.SupplierID = s.SupplierID
    WHERE p.UnitPrice > 0
    GROUP BY s.ContactName
    ORDER BY AvgProfitMargin DESC;
    ```
    
100. **Análisis de "Market Basket": ¿Qué producto se vende más frecuentemente con 'Chai'?**
    ```sql
    WITH ChaiOrders AS (
        -- Encontrar todos los pedidos que contienen 'Chai'
        SELECT DISTINCT od.OrderID
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
        WHERE p.ProductName = 'Chai'
    )
    SELECT
        p.ProductName,
        COUNT(DISTINCT od.OrderID) AS Frequency
    FROM OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    WHERE od.OrderID IN (SELECT OrderID FROM ChaiOrders)
      AND p.ProductName != 'Chai' -- No contarnos a nosotros mismos
    GROUP BY p.ProductName
    ORDER BY Frequency DESC
    LIMIT 5;
    ```
