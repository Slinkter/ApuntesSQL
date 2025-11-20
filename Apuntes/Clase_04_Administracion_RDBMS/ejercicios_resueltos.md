# Ejercicios Resueltos - Clase 04: DML y Consultas Básicas

Para los siguientes ejercicios, utilizaremos la tabla `PRODUCTOS` con los siguientes datos:

**Tabla `PRODUCTOS`**

| ID_Producto | Nombre         | Categoria  | Precio | Stock |
| :---------- | :------------- | :--------- | :----- | :---- |
| 1           | Laptop XYZ     | Electrónica | 1200   | 50    |
| 2           | Teclado Mecánico | Electrónica | 75     | 120   |
| 3           | Mouse Óptico   | Electrónica | 25     | 200   |
| 4           | Silla Ergonómica | Oficina    | 250    | 30    |
| 5           | Monitor 27"    | Electrónica | 300    | 80    |
| 6           | Cuaderno A4    | Papelería  | 5      | 500   |

### Ejercicio 1: Inserción de Datos

**Enunciado:**
Inserta un nuevo producto en la tabla `PRODUCTOS` con la siguiente información:
*   `ID_Producto`: 7
*   `Nombre`: "Escritorio Gamer"
*   `Categoria`: "Oficina"
*   `Precio`: 350
*   `Stock`: 20

**Solución:**
```sql
INSERT INTO PRODUCTOS (ID_Producto, Nombre, Categoria, Precio, Stock)
VALUES (7, 'Escritorio Gamer', 'Oficina', 350, 20);
```

### Ejercicio 2: Actualización de Datos

**Enunciado:**
Actualiza el precio del "Mouse Óptico" (ID_Producto 3) a 20 y reduce su stock en 50 unidades.

**Solución:**
```sql
UPDATE PRODUCTOS
SET Precio = 20,
    Stock = Stock - 50 -- O directamente Stock = 150 si el stock inicial es 200
WHERE ID_Producto = 3;
```

### Ejercicio 3: Eliminación de Datos

**Enunciado:**
Elimina de la tabla `PRODUCTOS` todos los productos que pertenecen a la categoría "Papelería".

**Solución:**
```sql
DELETE FROM PRODUCTOS
WHERE Categoria = 'Papelería';
```

### Ejercicio 4: Consultas Básicas con Filtrado

**Enunciado:**
Realiza las siguientes consultas:

1.  Muestra todos los productos cuyo precio sea mayor a 100.
2.  Muestra el `Nombre` y `Precio` de los productos de la categoría "Electrónica" que tengan un `Stock` menor a 100 unidades.
3.  Muestra todos los productos que no sean de la categoría "Electrónica" o que tengan un `Precio` mayor a 200.

**Solución:**

1.  **Productos con precio mayor a 100:**
    ```sql
    SELECT *
    FROM PRODUCTOS
    WHERE Precio > 100;
    ```
2.  **Nombre y Precio de productos "Electrónica" con stock < 100:**
    ```sql
    SELECT Nombre, Precio
    FROM PRODUCTOS
    WHERE Categoria = 'Electrónica' AND Stock < 100;
    ```
3.  **Productos que no son "Electrónica" o con precio > 200:**
    ```sql
    SELECT *
    FROM PRODUCTOS
    WHERE NOT Categoria = 'Electrónica' OR Precio > 200;
    -- O de forma alternativa para la primera condición:
    -- WHERE Categoria <> 'Electrónica' OR Precio > 200;
    ```