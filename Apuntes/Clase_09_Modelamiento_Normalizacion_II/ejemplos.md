# Ejemplos - Clase 09: Otras Formas Normales y Desnormalización

### Ejemplo 1: FNBC (Forma Normal de Boyce-Codd) vs 3FN

Consideremos una tabla `ALUMNOS_CURSOS_PROFESORES` que registra qué alumnos se inscriben en qué cursos y qué profesor imparte cada curso. Un profesor puede impartir varios cursos, pero un curso es impartido por un único profesor. Cada curso tiene un código único.

**Tabla `ALUMNOS_CURSOS_PROFESORES`**

| ID_Alumno | ID_Curso | Nombre_Profesor |
| :-------- | :------- | :-------------- |
| A1        | C1       | Prof. García    |
| A2        | C1       | Prof. García    |
| A1        | C2       | Prof. Díaz      |

**Dependencias Funcionales:**
1.  `(ID_Alumno, ID_Curso)` → `Nombre_Profesor` (Un alumno en un curso específico tiene un profesor asignado)
2.  `ID_Curso` → `Nombre_Profesor` (Un curso es impartido por un único profesor)
3.  `Nombre_Profesor` → `ID_Curso` (Un profesor puede impartir un único curso o varios cursos, pero si la regla de negocio fuera que un profesor solo imparte *un* curso, esto sería una DF). En nuestro caso, `Nombre_Profesor` no determina `ID_Curso`.

**Análisis:**
*   **3FN:** La tabla está en 3FN porque no tiene dependencias parciales ni transitivas sobre su clave primaria `(ID_Alumno, ID_Curso)`.
*   **FNBC:** La tabla NO está en FNBC. ¿Por qué? Porque `ID_Curso` es un determinante (`ID_Curso` → `Nombre_Profesor`), pero `ID_Curso` NO es una clave candidata (la clave candidata es `(ID_Alumno, ID_Curso)`). Esto causa redundancia, ya que el `Nombre_Profesor` para `C1` se repite.

**Solución FNBC:**
Descomponemos la tabla en `INSCRIPCIONES` y `CURSOS_IMPARTIDOS`.

**Tabla `INSCRIPCIONES` (FNBC)**

| ID_Alumno | ID_Curso |
| :-------- | :------- |
| A1        | C1       |
| A2        | C1       |
| A1        | C2       |

**Tabla `CURSOS_IMPARTIDOS` (FNBC)**

| ID_Curso | Nombre_Profesor |
| :------- | :-------------- |
| C1       | Prof. García    |
| C2       | Prof. Díaz      |

### Ejemplo 2: 4FN (Cuarta Forma Normal) y Dependencias Multivaluadas

Consideremos una tabla `PROYECTO_HABILIDADES_IDIOMAS` que registra los proyectos, las habilidades necesarias para ese proyecto y los idiomas requeridos.

**Tabla `PROYECTO_HABILIDADES_IDIOMAS`**

| ID_Proyecto | Habilidad | Idioma |
| :---------- | :-------- | :----- |
| P1          | Java      | Inglés |
| P1          | Java      | Español |
| P1          | Python    | Inglés |
| P1          | Python    | Español |
| P2          | C#        | Inglés |

**Análisis de Dependencias Multivaluadas:**
*   Para `P1`, el conjunto de habilidades es `{Java, Python}` y el conjunto de idiomas es `{Inglés, Español}`.
*   El conjunto de habilidades `{Java, Python}` es independiente del conjunto de idiomas `{Inglés, Español}`. Es decir, `ID_Proyecto` determina múltiples habilidades y `ID_Proyecto` determina múltiples idiomas, pero las habilidades y los idiomas no se determinan mutuamente.
*   Esto es una **Dependencia Multivaluada**: `ID_Proyecto` →→ `Habilidad` y `ID_Proyecto` →→ `Idioma`.

**Problema:** Redundancia. Si añadimos un nuevo idioma a `P1` (ej. Francés), tenemos que añadirlo para *cada* habilidad existente.

**Solución 4FN:**
Descomponemos la tabla en `PROYECTO_HABILIDADES` y `PROYECTO_IDIOMAS`.

**Tabla `PROYECTO_HABILIDADES` (4FN)**

| ID_Proyecto | Habilidad |
| :---------- | :-------- |
| P1          | Java      |
| P1          | Python    |
| P2          | C#        |

**Tabla `PROYECTO_IDIOMAS` (4FN)**

| ID_Proyecto | Idioma  |
| :---------- | :------ |
| P1          | Inglés  |
| P1          | Español |
| P2          | Inglés  |

### Ejemplo 3: Desnormalización para Mejorar el Rendimiento

Imagina una base de datos de una tienda online. Tenemos las tablas `PRODUCTOS` y `PEDIDOS_DETALLE`.

**Tabla `PRODUCTOS`**
| ID_Producto | Nombre_Producto | Descripcion | Precio_Unitario |
| :---------- | :-------------- | :---------- | :-------------- |
| 1           | Camiseta        | ...         | 25.00           |

**Tabla `PEDIDOS_DETALLE`**
| ID_Detalle | ID_Pedido | ID_Producto | Cantidad |
| :--------- | :-------- | :---------- | :------- |
| 1001       | 500       | 1           | 2        |

Para generar un reporte de pedidos que muestre el nombre del producto y el precio unitario en cada línea de pedido, tendríamos que hacer un `JOIN` entre `PEDIDOS_DETALLE` y `PRODUCTOS`. Si este reporte se ejecuta miles de veces al día en una base de datos gigante, los `JOIN` pueden ser costosos.

**Desnormalización Aplicada:**
Añadimos `Nombre_Producto` y `Precio_Unitario` directamente a la tabla `PEDIDOS_DETALLE`.

**Tabla `PEDIDOS_DETALLE_DESNORMALIZADA`**

| ID_Detalle | ID_Pedido | ID_Producto | Cantidad | Nombre_Producto | Precio_Unitario |
| :--------- | :-------- | :---------- | :------- | :-------------- | :-------------- |
| 1001       | 500       | 1           | 2        | Camiseta        | 25.00           |

**Ventaja:** Los reportes que solo necesitan la información de la línea de pedido no requieren un `JOIN`, lo que acelera la consulta.
**Desventaja:**
*   **Redundancia:** `Nombre_Producto` y `Precio_Unitario` están duplicados.
*   **Anomalía de Actualización:** Si el `Precio_Unitario` de la `Camiseta` cambia en la tabla `PRODUCTOS`, ese cambio no se reflejará automáticamente en los `PEDIDOS_DETALLE_DESNORMALIZADA` históricos. Se necesitaría un mecanismo adicional para mantener la consistencia (ej. un `TRIGGER` o un proceso batch).
*   **Integridad reducida:** Se pierde parte de la integridad referencial implícita si no se gestiona bien.

La desnormalización se justifica cuando el beneficio en rendimiento para consultas críticas supera el costo de gestionar la redundancia y las posibles anomalías.
