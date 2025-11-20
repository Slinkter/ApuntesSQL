# Ejercicios Resueltos - Clase 09: Otras Formas Normales y Desnormalización

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
