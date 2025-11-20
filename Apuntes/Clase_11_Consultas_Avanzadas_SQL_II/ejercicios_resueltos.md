# Ejercicios Resueltos - Clase 11: SQL Embebido (PL/SQL)

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