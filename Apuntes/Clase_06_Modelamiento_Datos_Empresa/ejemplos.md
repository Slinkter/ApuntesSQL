# Ejemplos - Clase 06: Normalización (1FN, 2FN, 3FN)

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