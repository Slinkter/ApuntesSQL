# 🧹 Clase 06: Normalización (1FN, 2FN, 3FN)

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **¿Qué es Normalización?** | Es el proceso de **limpieza y mejora del diseño lógico** para evitar la duplicación innecesaria de datos (redundancia) y asegurar que las relaciones estén "bien estructuradas". |
| **Anomalías (¡Los Problemas a Evitar!)** | Queremos evitar problemas al manipular datos: **Anomalía de Inserción** (no puedes registrar un dato sin duplicar o inventar otros). **Anomalía de Eliminación** (borras un registro y pierdes datos importantes asociados). **Anomalía de Modificación** (tienes que cambiar el mismo dato en varios lugares). |
| **Dependencia Funcional** | Si el valor del atributo A determina el valor del atributo B, decimos que B es funcionalmente dependiente de A (A  B). |
| **1FN (Primera Forma Normal)** | **¡Todo debe ser Atómico!** Elimina los grupos repetitivos. Cada atributo debe tener un valor indivisible. Por ejemplo, si tienes "Lunes, Miércoles, Viernes" en una celda, debes separar cada día en su propia fila. |
| **2FN (Segunda Forma Normal)** | **¡Dependencia Total de la Clave!** Si tienes una Clave Primaria Compuesta, cada atributo no clave debe depender de *toda* la clave, no solo de una parte (dependencia funcional parcial). Si un atributo depende solo de un pedacito de la clave, ¡sácalo y ponlo en su propia tabla!. |
| **3FN (Tercera Forma Normal)** | **¡No a la Transitividad!** Elimina las **Dependencias Transitivas**. Esto pasa cuando un atributo no clave determina a otro atributo no clave (B  C). Por ejemplo, si el RUC determina el Nombre, y el Nombre determina la Dirección. Debes separarlo para que cada tabla se enfoque en un solo tema. |

**Resumen de la Clase 06:** La normalización es esencial para combatir la redundancia y evitar anomalías (inserción, eliminación, modificación). Seguimos un proceso de descomposición gradual: 1FN (atomicidad y grupos repetitivos), 2FN (dependencia total de la clave primaria) y 3FN (eliminar dependencias transitivas).

---

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Normalización a 1FN (Primera Forma Normal)

**Problema:** Una tabla `PEDIDOS_CLIENTE` sin normalizar, donde un cliente puede pedir múltiples productos en una misma fila, con los productos y cantidades repetidos en una sola columna.

**Tabla `PEDIDOS_CLIENTE` (Sin Normalizar)**

| ID_Pedido | Fecha      | ID_Cliente | Nombre_Cliente | Productos_Cantidad |
| :-------- | :--------- | :--------- | :------------- | :----------------- |
| 101       | 2023-10-26 | 1          | Ana García     | Laptop (1), Mouse (2) |
| 102       | 2023-10-26 | 2          | Luis Pérez     | Teclado (1)        |
| 103       | 2023-10-27 | 1          | Ana García     | Monitor (1)        |

**Análisis de 1FN:**
*   La columna `Productos_Cantidad` no es atómica, contiene múltiples valores (Laptop, 1; Mouse, 2).
*   Existe un grupo repetitivo.

**Solución (1FN): Descomponer el grupo repetitivo y asegurar atomicidad**

Creamos dos tablas: `PEDIDOS` y `DETALLE_PEDIDO`.

**Tabla `PEDIDOS` (1FN)**

| ID_Pedido | Fecha      | ID_Cliente | Nombre_Cliente |
| :-------- | :--------- | :--------- | :------------- |
| 101       | 2023-10-26 | 1          | Ana García     |
| 102       | 2023-10-26 | 2          | Luis Pérez     |
| 103       | 2023-10-27 | 1          | Ana García     |

**Tabla `DETALLE_PEDIDO` (1FN)**

| ID_Pedido | Producto | Cantidad |
| :-------- | :------- | :------- |
| 101       | Laptop   | 1        |
| 101       | Mouse    | 2        |
| 102       | Teclado  | 1        |
| 103       | Monitor  | 1        |

---

### Ejemplo 2: Normalización a 2FN (Segunda Forma Normal)

**Problema:** Partimos de una tabla `INSCRIPCIONES` que ya está en 1FN.

**Tabla `INSCRIPCIONES` (1FN)**

| ID_Estudiante | ID_Curso | Calificacion | Nombre_Estudiante | Nombre_Curso | Creditos_Curso |
| :------------ | :------- | :----------- | :---------------- | :----------- | :------------- |
| 1             | DB101    | A            | Ana García        | Bases Datos  | 3              |
| 1             | PR201    | B+           | Ana García        | Programación | 4              |
| 2             | DB101    | B            | Luis Pérez        | Bases Datos  | 3              |

**Análisis de 2FN:**
*   **Clave Primaria Compuesta:** (`ID_Estudiante`, `ID_Curso`)
*   **Atributos No Clave:** `Calificacion`, `Nombre_Estudiante`, `Nombre_Curso`, `Creditos_Curso`.
*   **Dependencias Funcionales Parciales:**
    *   `ID_Estudiante` → `Nombre_Estudiante` (El nombre del estudiante depende solo de `ID_Estudiante`, no de `ID_Curso`).
    *   `ID_Curso` → `Nombre_Curso`, `Creditos_Curso` (El nombre y créditos del curso dependen solo de `ID_Curso`, no de `ID_Estudiante`).
*   La tabla no está en 2FN debido a estas dependencias parciales.

**Solución (2FN): Eliminar dependencias parciales**

Creamos tres tablas: `ESTUDIANTES`, `CURSOS` e `INSCRIPCIONES`.

**Tabla `ESTUDIANTES` (2FN)**

| ID_Estudiante | Nombre_Estudiante |
| :------------ | :---------------- |
| 1             | Ana García        |
| 2             | Luis Pérez        |

**Tabla `CURSOS` (2FN)**

| ID_Curso | Nombre_Curso | Creditos_Curso |
| :------- | :----------- | :------------- |
| DB101    | Bases Datos  | 3              |
| PR201    | Programación | 4              |

**Tabla `INSCRIPCIONES` (2FN)**

| ID_Estudiante | ID_Curso | Calificacion |
| :------------ | :------- | :----------- |
| 1             | DB101    | A            |
| 1             | PR201    | B+           |
| 2             | DB101    | B            |

---

### Ejemplo 3: Normalización a 3FN (Tercera Forma Normal)

**Problema:** Partimos de una tabla `EMPLEADOS_DEPARTAMENTOS` que ya está en 2FN.

**Tabla `EMPLEADOS_DEPARTAMENTOS` (2FN)**

| ID_Empleado | Nombre_Empleado | ID_Departamento | Nombre_Departamento | Ubicacion_Departamento |
| :---------- | :-------------- | :-------------- | :------------------ | :--------------------- |
| 101         | Juan Pérez      | 10              | Ventas              | Edificio A             |
| 102         | María López     | 20              | Marketing           | Edificio B             |
| 103         | Carlos Ruiz     | 10              | Ventas              | Edificio A             |

**Análisis de 3FN:**
*   **Clave Primaria:** `ID_Empleado`
*   **Atributos No Clave:** `Nombre_Empleado`, `ID_Departamento`, `Nombre_Departamento`, `Ubicacion_Departamento`.
*   **Dependencia Funcional Transactiva:**
    *   `ID_Departamento` → `Nombre_Departamento`
    *   `ID_Departamento` → `Ubicacion_Departamento`
    *   Esto significa que `Nombre_Departamento` y `Ubicacion_Departamento` no dependen directamente de `ID_Empleado` (la PK), sino de `ID_Departamento`, que a su vez depende de `ID_Empleado`. Es una dependencia transitiva.
*   La tabla no está en 3FN debido a esta dependencia transitiva.

**Solución (3FN): Eliminar dependencias transitivas**

Creamos dos tablas: `EMPLEADOS` y `DEPARTAMENTOS`.

**Tabla `EMPLEADOS` (3FN)**

| ID_Empleado | Nombre_Empleado | ID_Departamento |
| :---------- | :-------------- | :-------------- |
| 101         | Juan Pérez      | 10              |
| 102         | María López     | 20              |
| 103         | Carlos Ruiz     | 10              |

**Tabla `DEPARTAMENTOS` (3FN)**

| ID_Departamento | Nombre_Departamento | Ubicacion_Departamento |
| :-------------- | :------------------ | :--------------------- |
| 10              | Ventas              | Edificio A             |
| 20              | Marketing           | Edificio B             |

---

## ✏️ Ejercicios Resueltos

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

---

