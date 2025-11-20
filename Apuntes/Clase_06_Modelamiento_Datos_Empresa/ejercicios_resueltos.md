# Ejercicios Resueltos - Clase 06: Normalización (1FN, 2FN, 3FN)

### Ejercicio 1: Normalización a 3FN para un Sistema de Proyectos

**Enunciado:**
Considera la siguiente tabla `PROYECTOS_EMPLEADOS` que registra información sobre los proyectos en los que trabajan los empleados de una empresa, los departamentos a los que pertenecen y sus habilidades.

**Tabla `PROYECTOS_EMPLEADOS` (Sin normalizar)**

| ID_Proyecto | Nombre_Proyecto | Fecha_Inicio_Proyecto | ID_Empleado | Nombre_Empleado | Salario_Empleado | Departamento_Empleado | Ubicacion_Departamento | Habilidades_Empleado |
| :---------- | :-------------- | :-------------------- | :---------- | :-------------- | :--------------- | :-------------------- | :--------------------- | :------------------- |
| P1          | Diseño Web      | 2023-01-01            | E1          | Ana Gómez       | 60000            | Desarrollo            | Edificio Sur           | Java, SQL, JS        |
| P1          | Diseño Web      | 2023-01-01            | E2          | Luis Pérez      | 70000            | Desarrollo            | Edificio Sur           | Python, AWS          |
| P2          | App Móvil       | 2023-02-15            | E1          | Ana Gómez       | 60000            | Desarrollo            | Edificio Sur           | Java, SQL, JS        |
| P3          | Análisis Datos  | 2023-03-01            | E3          | Marta Solís     | 65000            | BI                    | Edificio Norte         | Python, R            |

**Tarea:**
Normaliza la tabla `PROYECTOS_EMPLEADOS` hasta la Tercera Forma Normal (3FN), mostrando cada paso (1FN, 2FN, 3FN) e identificando las dependencias funcionales y anomalías.

---

**Solución:**

#### Paso 1: Normalización a 1FN (Primera Forma Normal)

**Anomalías a resolver:**
*   La columna `Habilidades_Empleado` no es atómica, contiene múltiples valores ("Java, SQL, JS").

**Acciones:**
1.  Descomponer `Habilidades_Empleado` en filas separadas o en una tabla aparte de muchos-a-muchos. Para este ejercicio, la separamos en una tabla de N:M.
2.  Identificar la clave primaria: `(ID_Proyecto, ID_Empleado, Habilidad)`.

**Dependencias Funcionales (Parciales):**
*   `ID_Proyecto` → `Nombre_Proyecto`, `Fecha_Inicio_Proyecto`
*   `ID_Empleado` → `Nombre_Empleado`, `Salario_Empleado`, `Departamento_Empleado`, `Ubicacion_Departamento`

**Tabla `PROYECTOS_EMPLEADOS_1FN`:**

| ID_Proyecto | Nombre_Proyecto | Fecha_Inicio_Proyecto | ID_Empleado | Nombre_Empleado | Salario_Empleado | Departamento_Empleado | Ubicacion_Departamento |
| :---------- | :-------------- | :-------------------- | :---------- | :-------------- | :--------------- | :-------------------- | :--------------------- |
| P1          | Diseño Web      | 2023-01-01            | E1          | Ana Gómez       | 60000            | Desarrollo            | Edificio Sur           |
| P1          | Diseño Web      | 2023-01-01            | E2          | Luis Pérez      | 70000            | Desarrollo            | Edificio Sur           |
| P2          | App Móvil       | 2023-02-15            | E1          | Ana Gómez       | 60000            | Desarrollo            | Edificio Sur           |
| P3          | Análisis Datos  | 2023-03-01            | E3          | Marta Solís     | 65000            | BI                    | Edificio Norte         |

**Tabla `EMPLEADO_HABILIDADES` (Nueva, para N:M de Habilidades):**

| ID_Empleado | Habilidad |
| :---------- | :-------- |
| E1          | Java      |
| E1          | SQL       |
| E1          | JS        |
| E2          | Python    |
| E2          | AWS       |
| E3          | Python    |
| E3          | R         |

#### Paso 2: Normalización a 2FN (Segunda Forma Normal)

**Anomalías a resolver:**
*   **Dependencias Funcionales Parciales** en `PROYECTOS_EMPLEADOS_1FN`:
    *   `ID_Proyecto` (parte de la clave) determina `Nombre_Proyecto` y `Fecha_Inicio_Proyecto`.
    *   `ID_Empleado` (parte de la clave) determina `Nombre_Empleado`, `Salario_Empleado`, `Departamento_Empleado`, `Ubicacion_Departamento`.

**Acciones:**
Descomponer la tabla `PROYECTOS_EMPLEADOS_1FN` en tablas donde los atributos no clave dependan de la clave primaria *completa*.

**Tabla `PROYECTOS` (2FN):**

| ID_Proyecto | Nombre_Proyecto | Fecha_Inicio_Proyecto |
| :---------- | :-------------- | :-------------------- |
| P1          | Diseño Web      | 2023-01-01            |
| P2          | App Móvil       | 2023-02-15            |
| P3          | Análisis Datos  | 2023-03-01            |

**Tabla `EMPLEADOS` (2FN):**

| ID_Empleado | Nombre_Empleado | Salario_Empleado | Departamento_Empleado | Ubicacion_Departamento |
| :---------- | :-------------- | :--------------- | :-------------------- | :--------------------- |
| E1          | Ana Gómez       | 60000            | Desarrollo            | Edificio Sur           |
| E2          | Luis Pérez      | 70000            | Desarrollo            | Edificio Sur           |
| E3          | Marta Solís     | 65000            | BI                    | Edificio Norte         |

**Tabla `ASIGNACIONES` (2FN, para la relación N:M entre PROYECTOS y EMPLEADOS):**

| ID_Proyecto | ID_Empleado |
| :---------- | :---------- |
| P1          | E1          |
| P1          | E2          |
| P2          | E1          |
| P3          | E3          |

#### Paso 3: Normalización a 3FN (Tercera Forma Normal)

**Anomalías a resolver:**
*   **Dependencia Funcional Transitiva** en la tabla `EMPLEADOS` (2FN):
    *   `ID_Empleado` → `Departamento_Empleado`
    *   `Departamento_Empleado` → `Ubicacion_Departamento`
    *   Es decir, `Ubicacion_Departamento` depende de `Departamento_Empleado`, que a su vez depende de `ID_Empleado`.

**Acciones:**
Descomponer la tabla `EMPLEADOS` para eliminar esta dependencia transitiva.

**Tablas resultantes en 3FN:**

**Tabla `PROYECTOS` (Ya en 3FN):**

| ID_Proyecto | Nombre_Proyecto | Fecha_Inicio_Proyecto |
| :---------- | :-------------- | :-------------------- |
| P1          | Diseño Web      | 2023-01-01            |
| P2          | App Móvil       | 2023-02-15            |
| P3          | Análisis Datos  | 2023-03-01            |

**Tabla `EMPLEADOS` (3FN):**

| ID_Empleado | Nombre_Empleado | Salario_Empleado | ID_Departamento |
| :---------- | :-------------- | :--------------- | :-------------- |
| E1          | Ana Gómez       | 60000            | D1              |
| E2          | Luis Pérez      | 70000            | D1              |
| E3          | Marta Solís     | 65000            | D2              |

**Tabla `DEPARTAMENTOS` (3FN - Nueva tabla para resolver la dependencia transitiva):**

| ID_Departamento | Nombre_Departamento | Ubicacion_Departamento |
| :-------------- | :------------------ | :--------------------- |
| D1              | Desarrollo          | Edificio Sur           |
| D2              | BI                  | Edificio Norte         |

**Tabla `ASIGNACIONES` (Ya en 3FN):**

| ID_Proyecto | ID_Empleado |
| :---------- | :---------- |
| P1          | E1          |
| P1          | E2          |
| P2          | E1          |
| P3          | E3          |

**Tabla `EMPLEADO_HABILIDADES` (Ya en 3FN):**

| ID_Empleado | Habilidad |
| :---------- | :-------- |
| E1          | Java      |
| E1          | SQL       |
| E1          | JS        |
| E2          | Python    |
| E2          | AWS       |
| E3          | Python    |
| E3          | R         |
```