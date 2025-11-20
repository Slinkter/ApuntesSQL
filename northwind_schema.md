# Esquema de la Base de Datos: Northwind

Aquí tienes la descripción detallada del esquema de la base de datos `Northwind`, incluyendo todas las tablas, sus columnas y las relaciones de clave primaria y foránea.

## Tablas y sus Columnas:

---

### `Categories`
*   **CategoryID**: `int` (Primary Key, auto_increment)
*   **CategoryName**: `varchar(25)`
*   **Description**: `varchar(255)`

---

### `Customers`
*   **CustomerID**: `int` (Primary Key, auto_increment)
*   **CustomerName**: `varchar(50)`
*   **ContactName**: `varchar(50)`
*   **Address**: `varchar(50)`
*   **City**: `varchar(20)`
*   **PostalCode**: `varchar(10)`
*   **Country**: `varchar(15)`

---

### `Employees`
*   **EmployeeID**: `int` (Primary Key, auto_increment)
*   **LastName**: `varchar(15)`
*   **FirstName**: `varchar(15)`
*   **BirthDate**: `datetime`
*   **Photo**: `varchar(25)`
*   **Notes**: `varchar(1024)`

---

### `OrderDetails`
*   **OrderDetailID**: `int` (Primary Key, auto_increment)
*   **OrderID**: `int` (Foreign Key)
*   **ProductID**: `int` (Foreign Key)
*   **Quantity**: `int`

---

### `Orders`
*   **OrderID**: `int` (Primary Key, auto_increment)
*   **CustomerID**: `int` (Foreign Key)
*   **EmployeeID**: `int` (Foreign Key)
*   **OrderDate**: `datetime`
*   **ShipperID**: `int` (Foreign Key)

---

### `Products`
*   **ProductID**: `int` (Primary Key, auto_increment)
*   **ProductName**: `varchar(50)`
*   **SupplierID**: `int` (Foreign Key)
*   **CategoryID**: `int` (Foreign Key)
*   **Unit**: `varchar(25)`
*   **Price**: `decimal(10,0)`

---

### `Shippers`
*   **ShipperID**: `int` (Primary Key, auto_increment)
*   **ShipperName**: `varchar(25)`
*   **Phone**: `varchar(15)`

---

### `Suppliers`
*   **SupplierID**: `int` (Primary Key, auto_increment)
*   **SupplierName**: `varchar(50)`
*   **ContactName**: `varchar(50)`
*   **Address**: `varchar(50)`
*   **City**: `varchar(20)`
*   **PostalCode**: `varchar(10)`
*   **Country**: `varchar(15)`
*   **Phone**: `varchar(15)`

---

## Relaciones de Clave Foránea:

Estas son las conexiones entre las tablas, vitales para entender cómo se relacionan los datos.

*   **`OrderDetails`**
    *   `OrderID` hace referencia a `Orders.OrderID`
    *   `ProductID` hace referencia a `Products.ProductID`

*   **`Orders`**
    *   `EmployeeID` hace referencia a `Employees.EmployeeID`
    *   `CustomerID` hace referencia a `Customers.CustomerID`
    *   `ShipperID` hace referencia a `Shippers.ShipperID`

*   **`Products`**
    *   `CategoryID` hace referencia a `Categories.CategoryID`
    *   `SupplierID` hace referencia a `Suppliers.SupplierID`
