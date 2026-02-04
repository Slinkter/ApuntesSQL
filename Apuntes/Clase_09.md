# ⚡ Clase 09: Otras Formas Normales y Desnormalización

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **FNBC (Forma Normal Boyce-Codd)** | Es una versión más estricta de la 3FN. Una relación está en FNBC si **cada atributo determinante (A) es también una clave candidata**. Esto ayuda a resolver casos donde la 3FN aún permite dependencias problemáticas que involucran atributos que *podrían* ser claves. |
| **4FN (Cuarta Forma Normal)** | Se aplica si ya estás en FNBC y no tienes **Dependencias Multivaluadas**. Esto pasa si tienes tres atributos (A, B, C) donde A determina un conjunto de valores para B y un conjunto de valores para C, pero ¡B y C son totalmente independientes!. La solución es separarlos en relaciones binarias (Ej. Curso-Profesor y Curso-Texto). |
| **Desnormalización** | Es el **proceso contrario a la normalización**. Se hace para **crear redundancia intencional** con un objetivo muy específico: **mejorar los tiempos de respuesta** (velocidad) del sistema. |
| **Riesgos de Desnormalizar** | Aunque da velocidad, tiene desventajas: **reduce la integridad** y hace el modelo **menos flexible**. Hay que compensar la integridad con código de programación adicional. |
| **Técnicas Comunes de Desnormalización** | Incluyen: **Unir Entidades** (meter detalles en el maestro para evitar un *join*), **Grabar valores derivados** (guardar un Total en la tabla sin calcularlo cada vez), o usar **Valores Fijos** (sustituir una tabla de referencia pequeña por un campo con código 'M'/'F'). |

**Resumen de la Clase 09:** Después de la 3FN, exploramos la FNBC (determinantes son claves candidatas) y la 4FN (eliminación de dependencias multivaluadas). Finalmente, aprendimos que la **Desnormalización** es una técnica estratégica para introducir redundancia y ganar velocidad, aunque requiere programación adicional para mantener la integridad.

---

---

## 💡 Ejemplos Prácticos

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

---

## ✏️ Ejercicios Resueltos

### Ejercicio 1: Análisis de FNBC

**Enunciado:**
Considera la siguiente tabla `CURSO_PROFESOR_ASISTENTE` en una universidad. Un curso es impartido por un único profesor, pero un profesor puede tener varios asistentes. Un asistente solo trabaja para un profesor.

**Tabla `CURSO_PROFESOR_ASISTENTE`**

| ID_Curso | Nombre_Curso | Nombre_Profesor | Nombre_Asistente |
| :------- | :----------- | :-------------- | :--------------- |
| C101     | Bases Datos  | Prof. Ana       | Asistente X      |
| C101     | Bases Datos  | Prof. Ana       | Asistente Y      |
| C102     | Programación | Prof. Luis      | Asistente Z      |

**Dependencias Funcionales:**
1.  `ID_Curso` → `Nombre_Curso`, `Nombre_Profesor` (Un curso tiene un nombre y un profesor únicos)
2.  `Nombre_Asistente` → `Nombre_Profesor` (Un asistente trabaja para un único profesor)
3.  `ID_Curso`, `Nombre_Asistente` → `Nombre_Curso`, `Nombre_Profesor` (Clave primaria)

**Pregunta:** ¿Está la tabla `CURSO_PROFESOR_ASISTENTE` en 3FN? ¿Está en FNBC? Si no está en FNBC, ¿cómo la normalizarías a FNBC?

---

**Solución:**

1.  **¿Está en 3FN?**
    *   **Clave Primaria:** (`ID_Curso`, `Nombre_Asistente`).
    *   No hay atributos no clave que dependan de una parte de la PK (2FN).
    *   No hay dependencias transitivas (un atributo no clave determina a otro no clave).
    *   Sí, la tabla está en 3FN.

2.  **¿Está en FNBC?**
    *   Un determinante en la tabla es `Nombre_Asistente` (`Nombre_Asistente` → `Nombre_Profesor`).
    *   Pero `Nombre_Asistente` NO es una clave candidata. La clave candidata es `(ID_Curso, Nombre_Asistente)`.
    *   Por lo tanto, la tabla **NO está en FNBC**.

3.  **Normalización a FNBC:**
    Para resolver el problema, debemos separar la dependencia `Nombre_Asistente` → `Nombre_Profesor` en una nueva tabla.

    **Tabla `CURSOS` (FNBC)**

    | ID_Curso | Nombre_Curso | Nombre_Profesor |
    | :------- | :----------- | :-------------- |
    | C101     | Bases Datos  | Prof. Ana       |
    | C102     | Programación | Prof. Luis      |

    **Tabla `PROFESORES_ASISTENTES` (FNBC)**

    | Nombre_Asistente | Nombre_Profesor |
    | :--------------- | :-------------- |
    | Asistente X      | Prof. Ana       |
    | Asistente Y      | Prof. Ana       |
    | Asistente Z      | Prof. Luis      |

    **Tabla `ASIGNACIONES_CURSO_ASISTENTE` (FNBC)**

    | ID_Curso | Nombre_Asistente |
    | :------- | :--------------- |
    | C101     | Asistente X      |
    | C101     | Asistente Y      |
    | C102     | Asistente Z      |

### Ejercicio 2: Identificación de Dependencias Multivaluadas y 4FN

**Enunciado:**
Una empresa de consultoría registra la información de sus `CONSULTORES`, los `PROYECTOS` en los que pueden trabajar y las `TECNOLOGIAS` que dominan. Un consultor puede trabajar en múltiples proyectos y dominar múltiples tecnologías, pero la elección de tecnologías no depende del proyecto, ni viceversa.

**Tabla `CONSULTORES_PROYECTOS_TECNOLOGIAS`**

| ID_Consultor | Proyecto | Tecnología |
| :----------- | :------- | :--------- |
| C1           | P1       | Java       |
| C1           | P1       | Python     |
| C1           | P2       | Java       |
| C1           | P2       | Python     |
| C2           | P1       | C#         |

**Pregunta:** ¿La tabla está en 4FN? Si no, ¿cómo la normalizarías a 4FN?

---

**Solución:**

1.  **Análisis de Dependencias:**
    *   `ID_Consultor` →→ `Proyecto` (Un consultor puede trabajar en un conjunto de proyectos)
    *   `ID_Consultor` →→ `Tecnología` (Un consultor domina un conjunto de tecnologías)
    *   Las tecnologías que domina un consultor son independientes de los proyectos en los que trabaja. Esta es la característica de una **dependencia multivaluada**.
    *   La tabla `CONSULTORES_PROYECTOS_TECNOLOGIAS` no está en 4FN porque tiene dependencias multivaluadas no triviales (`ID_Consultor` →→ `Proyecto` y `ID_Consultor` →→ `Tecnología`) y `Proyecto` no es funcionalmente dependiente de `Tecnología`, ni viceversa.

2.  **Normalización a 4FN:**
    Para alcanzar la 4FN, debemos eliminar las dependencias multivaluadas separando los atributos independientes en tablas separadas.

    **Tabla `CONSULTORES_PROYECTOS` (4FN)**

    | ID_Consultor | Proyecto |
    | :----------- | :------- |
    | C1           | P1       |
    | C1           | P2       |
    | C2           | P1       |

    **Tabla `CONSULTORES_TECNOLOGIAS` (4FN)**

    | ID_Consultor | Tecnología |
    | :----------- | :--------- |
    | C1           | Java       |
    | C1           | Python     |
    | C2           | C#         |

### Ejercicio 3: Escenario de Desnormalización

**Enunciado:**
Una base de datos tiene una tabla `PRODUCTOS` y una tabla `CATEGORIAS`. Para cada producto se almacena su `ID_Producto`, `Nombre_Producto`, `ID_Categoria` y `Precio`. Para cada categoría se almacena `ID_Categoria` y `Nombre_Categoria`.

Se requiere generar un reporte de ventas muy frecuentemente que muestra el `Nombre_Producto`, `Nombre_Categoria` y el `Precio`. Este reporte es crítico para el negocio y debe ejecutarse lo más rápido posible.

**Pregunta:** Propón un escenario de desnormalización para optimizar el rendimiento de este reporte y describe las implicaciones (ventajas y desventajas).

---

**Solución:**

**Escenario de Desnormalización:**
Podemos introducir una columna `Nombre_Categoria` directamente en la tabla `PRODUCTOS`.

**Tabla `PRODUCTOS_DESNORMALIZADA`**

| ID_Producto | Nombre_Producto | ID_Categoria | Nombre_Categoria | Precio |
| :---------- | :-------------- | :----------- | :--------------- | :----- |
| 1           | Laptop          | 10           | Electrónica      | 1200   |
| 2           | Silla           | 20           | Oficina          | 250    |

**Implicaciones:**

*   **Ventajas:**
    *   **Mejora de rendimiento:** El reporte de ventas que requiere el nombre de la categoría ya no necesita realizar un `JOIN` con la tabla `CATEGORIAS`. Esto reduce el tiempo de ejecución de la consulta, especialmente en bases de datos muy grandes o cuando el reporte se ejecuta miles de veces al día.
    *   **Simplificación de consultas:** Las consultas para obtener esta información son más sencillas y directas.

*   **Desventajas:**
    *   **Redundancia de datos:** El `Nombre_Categoria` se duplica en cada fila de `PRODUCTOS_DESNORMALIZADA` que pertenece a esa categoría.
    *   **Anomalías de actualización:** Si el `Nombre_Categoria` cambia en la tabla `CATEGORIAS`, se requerirá una actualización en *todos* los registros de `PRODUCTOS_DESNORMALIZADA` que tengan esa categoría para mantener la consistencia. Esto aumenta la complejidad del mantenimiento de la base de datos y el riesgo de inconsistencias si la actualización no se realiza de forma exhaustiva (ej. con un `TRIGGER`).
    *   **Mayor espacio de almacenamiento:** Se utiliza más espacio en disco debido a la duplicación de datos.

**Conclusión:** La desnormalización es una técnica válida para optimizar el rendimiento en casos críticos, pero debe aplicarse con precaución y con mecanismos compensatorios para gestionar la integridad de los datos, como triggers o procedimientos almacenados que mantengan la sincronización entre los datos redundantes.

---

