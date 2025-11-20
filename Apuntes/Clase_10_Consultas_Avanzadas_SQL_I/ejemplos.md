# Ejemplos - Clase 10: JOIN, Subconsultas y Agrupamiento (SQL Avanzado)

Para los siguientes ejemplos, asumiremos las siguientes tablas simplificadas:

**Tabla `EMPLEADOS`**

| ID_Empleado | Nombre    | Apellido  | ID_Departamento | Salario |
| :---------- | :-------- | :-------- | :-------------- | :------ |
| 1           | Ana       | García    | 10              | 50000   |
| 2           | Luis      | Pérez     | 20              | 55000   |
| 3           | Marta     | Sánchez   | 10              | 52000   |
| 4           | Pedro     | Ramírez   | 30              | 60000   |
| 5           | Sofía     | Díaz      | 20              | 58000   |
| 6           | Elena     | Torres    | NULL            | 62000   |

**Tabla `DEPARTAMENTOS`**

| ID_Departamento | Nombre_Departamento | Ubicacion |
| :-------------- | :------------------ | :-------- |
| 10              | Ventas              | Madrid    |
| 20              | Marketing           | Barcelona |
| 30              | TI                  | Madrid    |
| 40              | I+D                 | Valencia  |

### Ejemplo 1: INNER JOIN (Equijoin)

**Objetivo:** Obtener el nombre de los empleados y el nombre de su departamento.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |

### Ejemplo 2: LEFT JOIN (LEFT OUTER JOIN)

**Objetivo:** Obtener todos los empleados y, si tienen, el nombre de su departamento. Queremos ver también a los empleados sin departamento.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
LEFT JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |
| Elena  | Torres   | NULL                |

### Ejemplo 3: RIGHT JOIN (RIGHT OUTER JOIN)

**Objetivo:** Obtener todos los departamentos y, si tienen, los empleados asignados. Queremos ver también los departamentos sin empleados.

```sql
SELECT E.Nombre, E.Apellido, D.Nombre_Departamento
FROM EMPLEADOS E
RIGHT JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento;
```

**Resultado:**

| Nombre | Apellido | Nombre_Departamento |
| :----- | :------- | :------------------ |
| Ana    | García   | Ventas              |
| Luis   | Pérez    | Marketing           |
| Marta  | Sánchez  | Ventas              |
| Pedro  | Ramírez  | TI                  |
| Sofía  | Díaz     | Marketing           |
| NULL   | NULL     | I+D                 |

### Ejemplo 4: Self Join

**Objetivo:** Encontrar empleados que ganan más que su propio manager (asumiendo que `ID_Jefe` es una FK a `ID_Empleado` en la misma tabla `EMPLEADOS`).

**Tabla `EMPLEADOS_CON_JEFE`** (asumiendo una columna `ID_Jefe`)

| ID_Empleado | Nombre    | Salario | ID_Jefe |
| :---------- | :-------- | :------ | :------ |
| 1           | Ana       | 50000   | NULL    |
| 2           | Luis      | 55000   | 1       |
| 3           | Marta     | 52000   | 1       |
| 4           | Pedro     | 60000   | 2       |

```sql
SELECT E.Nombre AS Empleado, E.Salario AS SalarioEmpleado,
       J.Nombre AS Jefe, J.Salario AS SalarioJefe
FROM EMPLEADOS_CON_JEFE E
INNER JOIN EMPLEADOS_CON_JEFE J ON E.ID_Jefe = J.ID_Empleado
WHERE E.Salario > J.Salario;
```

**Resultado (ejemplo hipotético):**

| Empleado | SalarioEmpleado | Jefe | SalarioJefe |
| :------- | :-------------- | :--- | :---------- |
| Pedro    | 60000           | Luis | 55000       |

### Ejemplo 5: Subconsulta Escalar en WHERE

**Objetivo:** Encontrar los empleados cuyo salario es mayor que el salario promedio de todos los empleados.

```sql
SELECT Nombre, Apellido, Salario
FROM EMPLEADOS
WHERE Salario > (SELECT AVG(Salario) FROM EMPLEADOS);
```

**Resultado (si AVG(Salario) es, por ejemplo, 55000):**

| Nombre | Apellido | Salario |
| :----- | :------- | :------ |
| Pedro  | Ramírez  | 60000   |
| Sofía  | Díaz     | 58000   |
| Elena  | Torres   | 62000   |

### Ejemplo 6: Funciones de Agregación con GROUP BY

**Objetivo:** Contar cuántos empleados hay en cada departamento y cuál es el salario promedio por departamento.

```sql
SELECT D.Nombre_Departamento, COUNT(E.ID_Empleado) AS Num_Empleados, AVG(E.Salario) AS Salario_Promedio
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento
GROUP BY D.Nombre_Departamento;
```

**Resultado:**

| Nombre_Departamento | Num_Empleados | Salario_Promedio |
| :------------------ | :------------ | :--------------- |
| Ventas              | 2             | 51000            |
| Marketing           | 2             | 56500            |
| TI                  | 1             | 60000            |

### Ejemplo 7: GROUP BY con HAVING

**Objetivo:** Mostrar los departamentos donde el salario promedio de sus empleados es superior a 52000.

```sql
SELECT D.Nombre_Departamento, AVG(E.Salario) AS Salario_Promedio
FROM EMPLEADOS E
INNER JOIN DEPARTAMENTOS D ON E.ID_Departamento = D.ID_Departamento
GROUP BY D.Nombre_Departamento
HAVING AVG(E.Salario) > 52000;
```

**Resultado:**

| Nombre_Departamento | Salario_Promedio |
| :------------------ | :--------------- |
| Marketing           | 56500            |
| TI                  | 60000            |