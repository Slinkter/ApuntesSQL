# Diagrama de Entidad-Relación de Northwind (Formato Mermaid)

Este archivo contiene el código en formato Mermaid para generar un diagrama visual de la base de datos `Northwind`. Puedes copiar y pegar este bloque de código en un editor compatible con Mermaid para ver el gráfico.

```mermaid
erDiagram
    Customers {
        int CustomerID PK
        varchar CustomerName
        varchar ContactName
        varchar Address
        varchar City
        varchar PostalCode
        varchar Country
    }

    Orders {
        int OrderID PK
        int CustomerID FK
        int EmployeeID FK
        datetime OrderDate
        int ShipperID FK
    }

    OrderDetails {
        int OrderDetailID PK
        int OrderID FK
        int ProductID FK
        int Quantity
    }

    Products {
        int ProductID PK
        varchar ProductName
        int SupplierID FK
        int CategoryID FK
        varchar Unit
        decimal Price
    }

    Categories {
        int CategoryID PK
        varchar CategoryName
        varchar Description
    }

    Suppliers {
        int SupplierID PK
        varchar SupplierName
        varchar ContactName
        varchar Address
        varchar City
        varchar PostalCode
        varchar Country
        varchar Phone
    }

    Employees {
        int EmployeeID PK
        varchar LastName
        varchar FirstName
        datetime BirthDate
        varchar Photo
        varchar Notes
    }

    Shippers {
        int ShipperID PK
        varchar ShipperName
        varchar Phone
    }

    Customers ||--o{ Orders : "places"
    Employees ||--o{ Orders : "manages"
    Shippers ||--o{ Orders : "ships"
    Orders ||--|{ OrderDetails : "has"
    Products ||--|{ OrderDetails : "details"
    Categories ||--o{ Products : "contains"
    Suppliers ||--o{ Products : "supplies"
```
