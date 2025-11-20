# Ejemplos - Clase 11: SQL Embebido (PL/SQL)

Para los siguientes ejemplos, asumiremos una tabla `PRODUCTOS` simplificada:

**Tabla `PRODUCTOS`**

| ID_Producto | Nombre    | Precio | Stock |
| :---------- | :-------- | :----- | :---- |
| 1           | Laptop    | 1200   | 50    |
| 2           | Teclado   | 75     | 120   |
| 3           | Ratón     | 25     | 200   |

### Ejemplo 1: Bloque PL/SQL Anónimo Básico

Este bloque simplemente muestra un mensaje.

```sql
DECLARE
  v_mensaje VARCHAR2(100) := '¡Hola desde PL/SQL!';
BEGIN
  DBMS_OUTPUT.PUT_LINE(v_mensaje);
END;
/
```
*(Para ver la salida de `DBMS_OUTPUT.PUT_LINE`, debes ejecutar `SET SERVEROUTPUT ON;` en tu cliente SQL antes del bloque.)*

### Ejemplo 2: Bloque PL/SQL con SELECT INTO

Este bloque recupera el nombre y stock de un producto y lo muestra.

```sql
DECLARE
  v_nombre_producto PRODUCTOS.Nombre%TYPE;
  v_stock_producto  PRODUCTOS.Stock%TYPE;
  v_id_producto     NUMBER := 1; -- Laptop
BEGIN
  SELECT Nombre, Stock
  INTO v_nombre_producto, v_stock_producto
  FROM PRODUCTOS
  WHERE ID_Producto = v_id_producto;

  DBMS_OUTPUT.PUT_LINE('Producto: ' || v_nombre_producto || ', Stock actual: ' || v_stock_producto);
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Producto con ID ' || v_id_producto || ' no encontrado.');
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Ha ocurrido un error inesperado.');
END;
/
```

### Ejemplo 3: Creación de un Procedimiento

Este procedimiento actualiza el stock de un producto dado su ID y la cantidad a añadir/restar.

```sql
CREATE OR REPLACE PROCEDURE ActualizarStockProducto (
  p_id_producto   IN PRODUCTOS.ID_Producto%TYPE,
  p_cantidad_cambio IN NUMBER
)
AS
BEGIN
  UPDATE PRODUCTOS
  SET Stock = Stock + p_cantidad_cambio
  WHERE ID_Producto = p_id_producto;

  IF SQL%ROWCOUNT = 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Producto no encontrado con ID: ' || p_id_producto);
  END IF;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('Stock del producto ' || p_id_producto || ' actualizado.');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE_APPLICATION_ERROR(-20002, 'Error al actualizar stock: ' || SQLERRM);
END;
/

-- Para ejecutar el procedimiento:
-- EXEC ActualizarStockProducto(1, -5); -- Restar 5 unidades a Laptop
-- EXEC ActualizarStockProducto(3, 10);  -- Añadir 10 unidades a Ratón
```

### Ejemplo 4: Creación de una Función

Esta función calcula el valor total en inventario para un producto específico (Precio * Stock).

```sql
CREATE OR REPLACE FUNCTION CalcularValorInventario (
  p_id_producto IN PRODUCTOS.ID_Producto%TYPE
)
RETURN NUMBER
IS
  v_valor_total NUMBER := 0;
BEGIN
  SELECT Precio * Stock
  INTO v_valor_total
  FROM PRODUCTOS
  WHERE ID_Producto = p_id_producto;

  RETURN v_valor_total;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN 0; -- Si el producto no existe, su valor en inventario es 0
  WHEN OTHERS THEN
    RAISE_APPLICATION_ERROR(-20003, 'Error al calcular valor de inventario: ' || SQLERRM);
END;
/

-- Para usar la función:
-- SELECT Nombre, CalcularValorInventario(ID_Producto) AS ValorTotal
-- FROM PRODUCTOS;

-- SELECT CalcularValorInventario(1) FROM DUAL; -- DUAL es una tabla dummy para probar funciones
```

### Ejemplo 5: Creación de un Trigger

Este trigger se dispara *antes* de cada actualización en la tabla `PRODUCTOS` para asegurar que el `Stock` nunca sea negativo.

```sql
CREATE OR REPLACE TRIGGER TRG_PRODUCTOS_STOCK_NEGATIVO
BEFORE UPDATE OF Stock ON PRODUCTOS
FOR EACH ROW
BEGIN
  IF :NEW.Stock < 0 THEN
    -- Levanta un error personalizado que impide la operación
    RAISE_APPLICATION_ERROR(-20004, 'El stock no puede ser negativo para el producto ' || :NEW.ID_Producto);
  END IF;
END;
/

-- Para probar el trigger:
-- -- Esta operación fallará debido al trigger
-- UPDATE PRODUCTOS
-- SET Stock = -10
-- WHERE ID_Producto = 2;

-- -- Esta operación tendrá éxito
-- UPDATE PRODUCTOS
-- SET Stock = 0
-- WHERE ID_Producto = 2;
```
