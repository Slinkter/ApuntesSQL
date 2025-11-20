# Ejemplos - Clase 04: DML y Consultas Básicas

Para estos ejemplos, usaremos una tabla `EMPLEADOS` simplificada:

**Tabla `EMPLEADOS`**

| ID_Empleado | Nombre    | Apellido  | Departamento | Salario | Fecha_Contratacion |
| :---------- | :-------- | :-------- | :----------- | :------ | :----------------- |
| 1           | Ana       | García    | Ventas       | 50000   | 2020-01-15         |
| 2           | Luis      | Pérez     | Marketing    | 55000   | 2019-03-20         |
| 3           | Marta     | Sánchez   | Ventas       | 52000   | 2021-06-01         |
| 4           | Pedro     | Ramírez   | TI           | 60000   | 2018-09-10         |
| 5           | Sofía     | Díaz      | Marketing    | 58000   | 2020-11-25         |

### Ejemplo 1: INSERT (Añadir Fila)

**Añadir un nuevo empleado:**
```sql
INSERT INTO EMPLEADOS (ID_Empleado, Nombre, Apellido, Departamento, Salario, Fecha_Contratacion)
VALUES (6, 'Elena', 'Torres', 'TI', 62000, '2022-02-10');
```

### Ejemplo 2: UPDATE (Modificar Dato)

**Aumentar el salario de Ana García a 53000:**
```sql
UPDATE EMPLEADOS
SET Salario = 53000
WHERE ID_Empleado = 1;
```

**Corregir el departamento de Pedro Ramírez a 'Desarrollo' y subir su salario a 63000:**
```sql
UPDATE EMPLEADOS
SET Departamento = 'Desarrollo',
    Salario = 63000
WHERE ID_Empleado = 4;
```

### Ejemplo 3: DELETE (Eliminar Fila)

**Eliminar al empleado Luis Pérez:**
```sql
DELETE FROM EMPLEADOS
WHERE ID_Empleado = 2;
```

**¡Precaución!** Si ejecutas `DELETE FROM EMPLEADOS;` sin la cláusula `WHERE`, ¡se eliminarán *todos* los empleados de la tabla!

### Ejemplo 4: SELECT (Consultar)

**Mostrar todos los datos de todos los empleados:**
```sql
SELECT * FROM EMPLEADOS;
```

**Mostrar solo el nombre, apellido y departamento de los empleados:**
```sql
SELECT Nombre, Apellido, Departamento FROM EMPLEADOS;
```

**Mostrar los diferentes departamentos existentes sin duplicados:**
```sql
SELECT DISTINCT Departamento FROM EMPLEADOS;
```

### Ejemplo 5: SELECT con WHERE (Filtrado de Datos)

**Mostrar los empleados del departamento de Ventas:**
```sql
SELECT *
FROM EMPLEADOS
WHERE Departamento = 'Ventas';
```

**Mostrar los empleados con un salario superior a 55000:**
```sql
SELECT Nombre, Apellido, Salario
FROM EMPLEADOS
WHERE Salario > 55000;
```

**Mostrar los empleados del departamento de Marketing con un salario inferior o igual a 58000:**
```sql
SELECT *
FROM EMPLEADOS
WHERE Departamento = 'Marketing' AND Salario <= 58000;
```

**Mostrar los empleados que no son del departamento de Ventas:**
```sql
SELECT Nombre, Apellido, Departamento
FROM EMPLEADOS
WHERE NOT Departamento = 'Ventas';

-- O de forma alternativa:
SELECT Nombre, Apellido, Departamento
FROM EMPLEADOS
WHERE Departamento <> 'Ventas';
```

**Mostrar los empleados de los departamentos de TI o Marketing:**
```sql
SELECT *
FROM EMPLEADOS
WHERE Departamento = 'TI' OR Departamento = 'Marketing';
```
