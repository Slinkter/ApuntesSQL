# 💻 Clase 11: SQL Embebido (PL/SQL)

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **PL/SQL** | Es una extensión procedural de SQL, que nos permite usar lógica de programación (variables, sentencias condicionales, *loops*) junto con las sentencias SQL. |
| **Estructura PL/SQL** | Todo programa tiene tres secciones: **DECLARE** (opcional, se definen variables, cursores), **BEGIN** (obligatorio, se ejecuta la lógica y el SQL), y **EXCEPTION** (opcional, se manejan los errores, como `NO_DATA_FOUND`). |
| **Cursor (La Ventana)** | Un **Cursor** es una estructura que se usa cuando una consulta retorna muchas filas, permitiéndonos procesar el resultado **fila por fila** dentro del programa (usando `OPEN`, `FETCH` y `CLOSE`). |
| **Procedimientos (Acciones)** | Un `PROCEDURE` es un subprograma que ejecuta un conjunto de acciones y se almacena en la BD. Puede recibir parámetros de entrada (`IN`), salida (`OUT`) o ambos (`IN OUT`). |
| **Funciones (Retorna Valor)** | Una `FUNCTION` es similar a un procedimiento, pero su objetivo principal es **calcular y retornar un único valor** al entorno que la llamó (Ej. calcular un impuesto). |
| **Triggers (Eventos Automáticos)** | Un `TRIGGER` es código PL/SQL que se ejecuta **automáticamente** y de forma reactiva, justo *antes* o *después* de un evento específico (como un `INSERT`, `UPDATE` o `DELETE`). Son perfectos para chequear reglas de negocio al instante (Ej. verificar que el salario no exceda un límite). |
| **Paquetes** | Los paquetes son contenedores lógicos que agrupan procedimientos y funciones relacionados. |

**Resumen de la Clase 11:** PL/SQL combina SQL con programación procedural, permitiendo crear bloques lógicos y manejar excepciones. Las estructuras clave son los Procedimientos (para ejecutar acciones) y las Funciones (para retornar un valor). Además, los Triggers son vitales para ejecutar código automáticamente basado en eventos.

---

---

## 💡 Ejemplos Prácticos

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

---

## ✏️ Ejercicios Resueltos

Para los siguientes ejercicios, utilizaremos una tabla `EMPLEADOS` simplificada:

**Tabla `EMPLEADOS`**

| ID_Empleado | Nombre    | Apellido  | Salario | ID_Departamento |
| :---------- | :-------- | :-------- | :------ | :-------------- |
| 1           | Ana       | García    | 50000   | 10              |
| 2           | Luis      | Pérez     | 55000   | 20              |
| 3           | Marta     | Sánchez   | 52000   | 10              |
| 4           | Pedro     | Ramírez   | 60000   | 30              |

### Ejercicio 1: Bloque PL/SQL Anónimo con Condicional

**Enunciado:**
Escribe un bloque PL/SQL anónimo que, dado un `ID_Empleado`, determine si el salario del empleado es "Alto" (>= 55000), "Medio" (>= 50000 y < 55000) o "Bajo" (< 50000). Muestra el nombre del empleado y su clasificación salarial.

**Solución:**
```sql
DECLARE
  v_id_empleado EMPLEADOS.ID_Empleado%TYPE := 2; -- Cambia el ID para probar
  v_nombre      EMPLEADOS.Nombre%TYPE;
  v_salario     EMPLEADOS.Salario%TYPE;
  v_clasificacion VARCHAR2(20);
BEGIN
  SELECT Nombre, Salario
  INTO v_nombre, v_salario
  FROM EMPLEADOS
  WHERE ID_Empleado = v_id_empleado;

  IF v_salario >= 55000 THEN
    v_clasificacion := 'Alto';
  ELSIF v_salario >= 50000 THEN
    v_clasificacion := 'Medio';
  ELSE
    v_clasificacion := 'Bajo';
  END IF;

  DBMS_OUTPUT.PUT_LINE('El empleado ' || v_nombre || ' tiene un salario ' || v_clasificacion || '.');
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Empleado con ID ' || v_id_empleado || ' no encontrado.');
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Ha ocurrido un error inesperado: ' || SQLERRM);
END;
/
```

### Ejercicio 2: Procedimiento para Aumentar Salario por Departamento

**Enunciado:**
Crea un procedimiento PL/SQL llamado `AUMENTAR_SALARIO_DEP` que reciba el `ID_Departamento` y un `Porcentaje_Aumento`. El procedimiento debe aumentar el salario de todos los empleados de ese departamento en el porcentaje especificado. Si el departamento no existe, debe mostrar un mensaje de error.

**Solución:**
```sql
CREATE OR REPLACE PROCEDURE AUMENTAR_SALARIO_DEP (
  p_id_departamento EMPLEADOS.ID_Departamento%TYPE,
  p_porcentaje_aumento NUMBER
)
AS
  v_num_empleados_afectados NUMBER;
BEGIN
  UPDATE EMPLEADOS
  SET Salario = Salario * (1 + p_porcentaje_aumento / 100)
  WHERE ID_Departamento = p_id_departamento;

  v_num_empleados_afectados := SQL%ROWCOUNT;

  IF v_num_empleados_afectados = 0 THEN
    DBMS_OUTPUT.PUT_LINE('No se encontraron empleados en el departamento ' || p_id_departamento || '.');
  ELSE
    COMMIT;
    DBMS_OUTPUT.PUT_LINE(v_num_empleados_afectados || ' empleados del departamento ' || p_id_departamento || ' actualizados con éxito.');
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error al aumentar salario: ' || SQLERRM);
END;
/

-- Para ejecutar el procedimiento:
-- EXEC AUMENTAR_SALARIO_DEP(10, 5); -- Aumentar 5% el salario de empleados del departamento 10
-- EXEC AUMENTAR_SALARIO_DEP(99, 10); -- Probar con un departamento que no existe
```

### Ejercicio 3: Función para Obtener el Salario Máximo por Departamento

**Enunciado:**
Crea una función PL/SQL llamada `GET_MAX_SALARIO_DEP` que reciba un `ID_Departamento` y retorne el salario máximo de ese departamento. Si el departamento no tiene empleados o no existe, debe retornar 0.

**Solución:**
```sql
CREATE OR REPLACE FUNCTION GET_MAX_SALARIO_DEP (
  p_id_departamento EMPLEADOS.ID_Departamento%TYPE
)
RETURN NUMBER
IS
  v_max_salario EMPLEADOS.Salario%TYPE := 0;
BEGIN
  SELECT MAX(Salario)
  INTO v_max_salario
  FROM EMPLEADOS
  WHERE ID_Departamento = p_id_departamento;

  RETURN NVL(v_max_salario, 0); -- NVL para retornar 0 si MAX(Salario) es NULL (no hay empleados)
EXCEPTION
  WHEN OTHERS THEN
    RAISE_APPLICATION_ERROR(-20001, 'Error en GET_MAX_SALARIO_DEP: ' || SQLERRM);
END;
/

-- Para usar la función:
-- SELECT GET_MAX_SALARIO_DEP(10) FROM DUAL;
-- SELECT GET_MAX_SALARIO_DEP(20) FROM DUAL;
-- SELECT GET_MAX_SALARIO_DEP(99) FROM DUAL;
```

### Ejercicio 4: Trigger para Controlar el Salario Mínimo

**Enunciado:**
Crea un trigger `BEFORE INSERT OR UPDATE` en la tabla `EMPLEADOS` que impida que el `Salario` de un empleado sea menor a 10000. Si se intenta insertar o actualizar con un salario menor, debe generar un error.

**Solución:**
```sql
CREATE OR REPLACE TRIGGER TRG_SALARIO_MINIMO
BEFORE INSERT OR UPDATE OF Salario ON EMPLEADOS
FOR EACH ROW
BEGIN
  IF :NEW.Salario < 10000 THEN
    RAISE_APPLICATION_ERROR(-20002, 'El salario no puede ser inferior a 10000.');
  END IF;
END;
/

-- Para probar el trigger:
-- -- Esto fallará
-- INSERT INTO EMPLEADOS (ID_Empleado, Nombre, Apellido, Salario, ID_Departamento)
-- VALUES (5, 'Nuevo', 'Empleado', 5000, 10);

-- -- Esto también fallará
-- UPDATE EMPLEADOS
-- SET Salario = 8000
-- WHERE ID_Empleado = 1;

-- -- Esto funcionará
-- UPDATE EMPLEADOS
-- SET Salario = 12000
-- WHERE ID_Empleado = 1;
```

---

