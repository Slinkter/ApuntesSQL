# 🛠️ Clase 03: Lenguaje de Definición de Datos (DDL)

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **BDR y SQL** | Una Base de Datos Relacional es una colección de tablas sin punteros físicos, ¡y todo se accede y modifica con sentencias del famoso **SQL**!. |
| **Objetos de la BD** | La BD está hecha de varios "juguetes": la **Tabla** (almacenamiento básico), la **Vista** (representación lógica de los datos), el **Índice** (para mejorar la velocidad de consulta), y la **Secuencia** (para generar valores de PK). |
| **DDL (Definición de Datos)** | Es el conjunto de comandos que usamos para **definir y modificar la estructura** de estos objetos (CREATE, ALTER, DROP). |
| **Restricciones (¡Las Reglas!)** | Hay varios tipos de reglas: **Integridad** (PK única y no nula, FK relacionada con una PK válida), y de **Columna** (el valor debe ser del tipo de dato definido). Las restricciones `NOT NULL`, `UNIQUE` y `CHECK` mantienen el orden. |
| **CREATE TABLE** | Es el comando para construir una tabla, especificando cada columna, su tipo de dato (como `DATE`, `NUMBER`, `VARCHAR2`) y sus restricciones (como `PRIMARY KEY` o `REFERENCES` para la FK). |
| **ON DELETE CASCADE** | Esta es una opción poderosa para la FK. Significa que, si borras un registro en la tabla "Padre" (la que tiene la PK), ¡automáticamente se borran todos los registros dependientes en la tabla "Hijo"!. |
| **ALTER y DROP** | Si necesitas hacer cambios después de crear la tabla, usas **ALTER TABLE** para modificar o eliminar columnas. Si ya no quieres la tabla, la eliminas con **DROP TABLE**. |

**Resumen de la Clase 03:** El enfoque relacional usa SQL para interactuar con objetos como Tablas y Vistas. El DDL nos da las herramientas (`CREATE`, `ALTER`, `DROP`) para construir la estructura, asegurando que las reglas de integridad (PK y FK) se cumplan.

---

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Creación de una Tabla Simple

Este ejemplo demuestra el uso del comando `CREATE TABLE` para definir una tabla básica `PRODUCTOS` con sus columnas, tipos de datos y restricciones clave.

```sql
CREATE TABLE PRODUCTOS (
    ID_Producto   NUMBER(10)     PRIMARY KEY,
    Nombre        VARCHAR2(100)  NOT NULL UNIQUE,
    Descripcion   VARCHAR2(500),
    Precio        NUMBER(10, 2)  NOT NULL CHECK (Precio >= 0),
    Stock         NUMBER(5)      DEFAULT 0 NOT NULL
);
```

**Explicación:**
*   `ID_Producto`: Columna numérica de hasta 10 dígitos, designada como clave primaria (`PRIMARY KEY`). Esto asegura que cada producto tenga un ID único y no nulo.
*   `Nombre`: Texto de hasta 100 caracteres, no puede ser nulo (`NOT NULL`) y cada nombre de producto debe ser único (`UNIQUE`).
*   `Descripcion`: Texto de hasta 500 caracteres, opcional.
*   `Precio`: Numérico con hasta 10 dígitos en total y 2 decimales, no puede ser nulo (`NOT NULL`), y debe ser mayor o igual a cero (`CHECK (Precio >= 0)`).
*   `Stock`: Numérico de hasta 5 dígitos, no puede ser nulo (`NOT NULL`), y su valor por defecto si no se especifica es 0 (`DEFAULT 0`).

### Ejemplo 2: Creación de Tablas con Clave Foránea y `ON DELETE CASCADE`

Este ejemplo ilustra cómo crear una tabla `PEDIDOS` que tiene una relación con la tabla `PRODUCTOS` (Ejemplo 1) y una tabla `CLIENTES`. También muestra el uso de `ON DELETE CASCADE`.

```sql
CREATE TABLE CLIENTES (
    ID_Cliente    NUMBER(10)     PRIMARY KEY,
    Nombre        VARCHAR2(100)  NOT NULL,
    Apellido      VARCHAR2(100)  NOT NULL,
    Email         VARCHAR2(255)  UNIQUE
);

CREATE TABLE PEDIDOS (
    ID_Pedido     NUMBER(10)     PRIMARY KEY,
    ID_Cliente    NUMBER(10)     NOT NULL,
    Fecha_Pedido  DATE           DEFAULT SYSDATE,
    Total         NUMBER(12, 2)  CHECK (Total >= 0),
    
    CONSTRAINT FK_ClientePedido
        FOREIGN KEY (ID_Cliente)
        REFERENCES CLIENTES (ID_Cliente)
        ON DELETE CASCADE -- Si un cliente es borrado, todos sus pedidos también se borran
);

CREATE TABLE DETALLE_PEDIDO (
    ID_Detalle    NUMBER(10)     PRIMARY KEY,
    ID_Pedido     NUMBER(10)     NOT NULL,
    ID_Producto   NUMBER(10)     NOT NULL,
    Cantidad      NUMBER(5)      NOT NULL CHECK (Cantidad > 0),
    Precio_Unitario NUMBER(10, 2) NOT NULL,

    CONSTRAINT FK_PedidoDetalle
        FOREIGN KEY (ID_Pedido)
        REFERENCES PEDIDOS (ID_Pedido)
        ON DELETE CASCADE, -- Si un pedido es borrado, sus detalles también se borran

    CONSTRAINT FK_ProductoDetalle
        FOREIGN KEY (ID_Producto)
        REFERENCES PRODUCTOS (ID_Producto)
        ON DELETE RESTRICT -- No permite borrar un producto si tiene detalles de pedido asociados
);
```

**Explicación de `ON DELETE CASCADE` y `ON DELETE RESTRICT`:**
*   En la tabla `PEDIDOS`, si se elimina un `CLIENTE` de la tabla `CLIENTES`, todos los `PEDIDOS` asociados a ese cliente también se eliminarán automáticamente.
*   En la tabla `DETALLE_PEDIDO`, si se elimina un `PEDIDO` de la tabla `PEDIDOS`, todos los registros de `DETALLE_PEDIDO` asociados a ese pedido también se eliminarán automáticamente.
*   Sin embargo, si se intenta eliminar un `PRODUCTO` de la tabla `PRODUCTOS` que tiene registros en `DETALLE_PEDIDO`, la operación será **rechazada** (`RESTRICT`) para mantener la integridad referencial.

### Ejemplo 3: Modificación y Eliminación de Tablas y Columnas

#### Modificar una Tabla (ALTER TABLE)

Añadir una nueva columna `Categoria` a la tabla `PRODUCTOS`:
```sql
ALTER TABLE PRODUCTOS
ADD Categoria VARCHAR2(50);
```

Modificar la longitud de la columna `Nombre` en `PRODUCTOS`:
```sql
ALTER TABLE PRODUCTOS
MODIFY Nombre VARCHAR2(150);
```

Eliminar la columna `Descripcion` de la tabla `PRODUCTOS`:
```sql
ALTER TABLE PRODUCTOS
DROP COLUMN Descripcion;
```

#### Eliminar una Tabla (DROP TABLE)

Eliminar la tabla `DETALLE_PEDIDO` completamente:
```sql
DROP TABLE DETALLE_PEDIDO;
```
**Precaución:** `DROP TABLE` elimina la tabla y todos sus datos de forma permanente.

---

## ✏️ Ejercicios Resueltos

### Ejercicio 1: Creación de un Esquema de Base de Datos para una Librería

**Enunciado:**
Diseña las sentencias DDL (`CREATE TABLE`) para un pequeño sistema de gestión de una librería. Necesitas gestionar libros, autores y los préstamos a clientes.

**Requerimientos:**

1.  **Tabla `AUTORES`**:
    *   `ID_Autor`: Clave primaria numérica, autoincremental (simular con `NUMBER` y notación de PK).
    *   `Nombre`: Texto, no nulo.
    *   `Nacionalidad`: Texto, opcional.
    *   `Fecha_Nacimiento`: Fecha, opcional.
2.  **Tabla `LIBROS`**:
    *   `ISBN`: Clave primaria de texto (VARCHAR2), de 13 caracteres, no nulo.
    *   `Titulo`: Texto, no nulo.
    *   `ID_Autor`: Clave foránea que referencia a `AUTORES`.
    *   `Anio_Publicacion`: Numérico, debe ser mayor que 1900.
    *   `Precio`: Numérico con 2 decimales, no nulo y mayor que 0.
    *   `Stock`: Numérico, no nulo y mayor o igual a 0, con un valor por defecto de 0.
3.  **Tabla `CLIENTES`**:
    *   `ID_Cliente`: Clave primaria numérica.
    *   `Nombre`: Texto, no nulo.
    *   `Apellido`: Texto, no nulo.
    *   `Email`: Texto, único y no nulo.
    *   `Telefono`: Texto, opcional.
4.  **Tabla `PRESTAMOS`**:
    *   `ID_Prestamo`: Clave primaria numérica.
    *   `ID_Cliente`: Clave foránea que referencia a `CLIENTES`.
    *   `ISBN`: Clave foránea que referencia a `LIBROS`.
    *   `Fecha_Prestamo`: Fecha, no nulo, por defecto la fecha actual.
    *   `Fecha_Devolucion_Prevista`: Fecha, no nulo, debe ser posterior a `Fecha_Prestamo`.
    *   `Fecha_Devolucion_Real`: Fecha, opcional.

**Consideraciones:**

*   Usa los tipos de datos apropiados para cada campo.
*   Define todas las restricciones de integridad (PK, FK, NOT NULL, UNIQUE, CHECK, DEFAULT).
*   Para las claves foráneas, considera la política `ON DELETE CASCADE` para `PRESTAMOS` si se elimina un `CLIENTE`, y `ON DELETE RESTRICT` para `LIBROS` si se elimina un `AUTOR`.

---

**Solución:**

```sql
-- Creación de la tabla AUTORES
CREATE TABLE AUTORES (
    ID_Autor          NUMBER(5)      PRIMARY KEY,
    Nombre            VARCHAR2(100)  NOT NULL,
    Nacionalidad      VARCHAR2(50),
    Fecha_Nacimiento  DATE
);

-- Creación de la tabla LIBROS
CREATE TABLE LIBROS (
    ISBN              VARCHAR2(13)   PRIMARY KEY,
    Titulo            VARCHAR2(255)  NOT NULL,
    ID_Autor          NUMBER(5)      NOT NULL,
    Anio_Publicacion  NUMBER(4)      CHECK (Anio_Publicacion > 1900),
    Precio            NUMBER(7, 2)   NOT NULL CHECK (Precio > 0),
    Stock             NUMBER(5)      DEFAULT 0 NOT NULL CHECK (Stock >= 0),

    CONSTRAINT FK_LibroAutor
        FOREIGN KEY (ID_Autor)
        REFERENCES AUTORES (ID_Autor)
        ON DELETE RESTRICT -- No permite borrar un autor si tiene libros asociados
);

-- Creación de la tabla CLIENTES
CREATE TABLE CLIENTES (
    ID_Cliente        NUMBER(7)      PRIMARY KEY,
    Nombre            VARCHAR2(100)  NOT NULL,
    Apellido          VARCHAR2(100)  NOT NULL,
    Email             VARCHAR2(255)  UNIQUE NOT NULL,
    Telefono          VARCHAR2(20)
);

-- Creación de la tabla PRESTAMOS
CREATE TABLE PRESTAMOS (
    ID_Prestamo                 NUMBER(10)     PRIMARY KEY,
    ID_Cliente                  NUMBER(7)      NOT NULL,
    ISBN                        VARCHAR2(13)   NOT NULL,
    Fecha_Prestamo              DATE           DEFAULT SYSDATE NOT NULL,
    Fecha_Devolucion_Prevista   DATE           NOT NULL,
    Fecha_Devolucion_Real       DATE,

    CONSTRAINT FK_PrestamoCliente
        FOREIGN KEY (ID_Cliente)
        REFERENCES CLIENTES (ID_Cliente)
        ON DELETE CASCADE, -- Si un cliente es borrado, sus préstamos también se borran

    CONSTRAINT FK_PrestamoLibro
        FOREIGN KEY (ISBN)
        REFERENCES LIBROS (ISBN)
        ON DELETE RESTRICT, -- No permite borrar un libro si está en préstamo
    
    CONSTRAINT CHK_FechasDevolucion
        CHECK (Fecha_Devolucion_Prevista > Fecha_Prestamo)
);
```

### Ejercicio 2: Modificación y Eliminación de un Esquema Existente

**Enunciado:**
Basándote en el esquema de la librería del Ejercicio 1, realiza las siguientes modificaciones y eliminaciones:

1.  Añade una nueva columna `Editorial` (VARCHAR2(100), opcional) a la tabla `LIBROS`.
2.  Modifica la columna `Telefono` en la tabla `CLIENTES` para que sea `VARCHAR2(30)`.
3.  Añade una restricción `UNIQUE` a la combinación de `ID_Cliente` y `ISBN` en la tabla `PRESTAMOS` para asegurar que un cliente no pueda tener el mismo libro prestado más de una vez (esto es para préstamos activos, la lógica completa sería más compleja con `Fecha_Devolucion_Real` nula).
4.  Elimina la columna `Nacionalidad` de la tabla `AUTORES`.
5.  Elimina la tabla `PRESTAMOS` (asumiendo que ya no se necesita o se va a rediseñar).

**Solución:**

```sql
-- 1. Añadir una nueva columna 'Editorial' a la tabla LIBROS
ALTER TABLE LIBROS
ADD Editorial VARCHAR2(100);

-- 2. Modificar la longitud de la columna 'Telefono' en la tabla CLIENTES
ALTER TABLE CLIENTES
MODIFY Telefono VARCHAR2(30);

-- 3. Añadir una restricción UNIQUE a (ID_Cliente, ISBN) en PRESTAMOS
ALTER TABLE PRESTAMOS
ADD CONSTRAINT UQ_ClienteLibroPrestado UNIQUE (ID_Cliente, ISBN);

-- 4. Eliminar la columna 'Nacionalidad' de la tabla AUTORES
ALTER TABLE AUTORES
DROP COLUMN Nacionalidad;

-- 5. Eliminar la tabla PRESTAMOS
DROP TABLE PRESTAMOS;
```

---

## 📝 Balotario

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿En qué concepto matemático se basa el modelo relacional de datos?**
a) En la teoría de grafos.
b) En el cálculo lambda.
c) En el concepto de relación, que forma parte de la teoría de conjuntos.
d) En la geometría euclidiana.

**Respuesta Correcta:** c)
**Justificación:** El modelo relacional, propuesto por E.F. Codd, se fundamenta en la rama de las matemáticas discretas de la teoría de conjuntos, donde una "relación" es un conjunto de tuplas (filas).
**Por qué las otras son incorrectas:**
*   a) La teoría de grafos es la base de las bases de datos de grafos, no de las relacionales.
*   b, d) Son ramas de las matemáticas no relacionadas directamente con el modelo relacional.

---

**2. En el modelo relacional, ¿cuál es el término formal para una "fila" o "registro"?**
a) Atributo
b) Tupla
c) Relación
d) Dominio

**Respuesta Correcta:** b)
**Justificación:** Una tupla es el término matemático que representa una instancia única en una relación, es decir, una fila en una tabla.
**Por qué las otras son incorrectas:**
*   a) Un atributo es una columna o campo.
*   c) Una relación es la tabla completa.
*   d) Un dominio es el conjunto de valores permitidos para una columna.

---

**3. ¿Qué describe el "Grado" de una relación?**
a) El número de filas (tuplas).
b) El número de columnas (atributos).
c) El número de claves foráneas.
d) El número de tablas en la base de datos.

**Respuesta Correcta:** b)
**Justificación:** El grado de una relación se define por el número de sus atributos o columnas.
**Por qué las otras son incorrectas:**
*   a) El número de filas se llama cardinalidad.
*   c, d) Son métricas de la base de datos, pero no definen el grado de una relación individual.

---

**4. ¿Cuál de las siguientes afirmaciones sobre una Clave Primaria (PK) es CIERTA?**
a) Puede contener valores nulos.
b) Puede tener valores duplicados.
c) Se utiliza para identificar de forma única cada tupla en una tabla.
d) Una tabla puede tener varias claves primarias.

**Respuesta Correcta:** c)
**Justificación:** La función principal y definitoria de una clave primaria es garantizar la unicidad de cada registro dentro de una tabla.
**Por qué las otras son incorrectas:**
*   a, b) Una clave primaria, por definición, no puede ser nula y debe ser única.
*   d) Una tabla solo puede tener una clave primaria (aunque esta puede estar compuesta por varias columnas).

---

**5. ¿Qué establece una Clave Foránea (FK)?**
a) Una restricción que obliga a que una columna solo acepte números.
b) Una relación entre dos tablas, manteniendo la integridad referencial.
c) Un identificador único para una fila dentro de la misma tabla.
d) Un índice para acelerar las consultas.

**Respuesta Correcta:** b)
**Justificación:** Una clave foránea en una tabla "hija" apunta a la clave primaria de una tabla "padre", creando así un enlace lógico entre ellas y asegurando que los datos relacionados sean consistentes.
**Por qué las otras son incorrectas:**
*   a) Eso es una restricción de tipo de dato o `CHECK`.
*   c) Eso es una clave primaria.
*   d) Aunque las claves foráneas a menudo se indexan, su propósito fundamental es relacional, no de rendimiento.

---

**6. Si se elimina un registro en una tabla "padre" y esto provoca la eliminación automática de los registros relacionados en la tabla "hija", ¿qué acción en cascada se ha definido?**
a) `ON DELETE RESTRICT`
b) `ON DELETE SET NULL`
c) `ON DELETE CASCADE`
d) `ON DELETE NO ACTION`

**Respuesta Correcta:** c)
**Justificación:** La acción `CASCADE` propaga la operación de eliminación (o actualización) desde la tabla padre a todas las filas dependientes en la tabla hija.
**Por qué las otras son incorrectas:**
*   a, d) `RESTRICT` o `NO ACTION` impedirían la eliminación en la tabla padre si existen registros hijos.
*   b) `SET NULL` establecería el valor de la clave foránea en la tabla hija como `NULL`, pero no eliminaría la fila.

---

**7. En álgebra relacional, ¿qué operación se utiliza para filtrar filas de una tabla basándose en una condición?**
a) Proyección (π)
b) Join (⋈)
c) Selección (σ)
d) Producto Cartesiano (×)

**Respuesta Correcta:** c)
**Justificación:** La operación de Selección (sigma) corresponde a la cláusula `WHERE` en SQL y se utiliza para seleccionar un subconjunto de tuplas (filas) que cumplen una condición.
**Por qué las otras son incorrectas:**
*   a) La Proyección selecciona columnas.
*   b) El Join combina tablas.
*   d) El Producto Cartesiano genera todas las combinaciones de filas entre dos tablas.

---

**8. ¿Qué es una "Clave Candidata"?**
a) Cualquier columna que no sea la clave primaria.
b) Una superclave mínima; un atributo o conjunto de atributos que identifica de forma única una tupla y no tiene subconjuntos redundantes.
c) Una clave foránea que podría convertirse en clave primaria.
d) Una columna que contiene datos de texto.

**Respuesta Correcta:** b)
**Justificación:** Una tabla puede tener varios identificadores únicos. Cada uno de estos es una clave candidata. La clave primaria es simplemente una de las claves candidatas que el diseñador elige como el identificador principal.
**Por qué las otras son incorrectas:**
*   a, c, d) No se ajustan a la definición de una clave candidata.

---

**9. La "Cardinalidad" de una relación se refiere a:**
a) El número de columnas.
b) El número de filas.
c) La cantidad de memoria que utiliza la tabla.
d) El tipo de datos de la clave primaria.

**Respuesta Correcta:** b)
**Justificación:** La cardinalidad es el término técnico que se utiliza para referirse al número de tuplas o filas en una relación en un momento dado.
**Por qué las otras son incorrectas:**
*   a) El número de columnas es el grado.
*   c, d) Son propiedades de la implementación física o del diseño, no la definición de cardinalidad.

---

**10. ¿Qué garantiza la "Integridad Referencial"?**
a) Que todas las columnas de texto estén en mayúsculas.
b) Que cada valor de una clave foránea exista como valor en la clave primaria de la tabla referenciada.
c) Que no se puedan insertar filas duplicadas.
d) Que las consultas se ejecuten rápidamente.

**Respuesta Correcta:** b)
**Justificación:** Esta es la esencia de la integridad referencial. Asegura que no haya "punteros rotos" o referencias a registros que no existen, manteniendo la consistencia entre las tablas relacionadas.
**Por qué las otras son incorrectas:**
*   a) Es una regla de formato, no de integridad referencial.
*   c) Es garantizado por las restricciones `PRIMARY KEY` o `UNIQUE`, no por la integridad referencial.
*   d) Se relaciona con el rendimiento, no con la integridad.

---

**11. La operación de Proyección (π) en álgebra relacional es análoga a qué cláusula de SQL?**
a) `SELECT [lista_de_columnas]`
b) `WHERE [condicion]`
c) `GROUP BY [columna]`
d) `ORDER BY [columna]`

**Respuesta Correcta:** a)
**Justificación:** La Proyección se utiliza para seleccionar un subconjunto de atributos (columnas) de una relación, que es exactamente lo que hace la lista de columnas en una sentencia `SELECT`.
**Por qué las otras son incorrectas:**
*   b) `WHERE` corresponde a la Selección (σ).
*   c, d) No tienen un operador directo equivalente en el álgebra relacional clásica.

---

**12. ¿Qué es una "Superclave"?**
a) Una clave primaria compuesta por más de tres columnas.
b) Cualquier atributo o conjunto de atributos que identifica de forma única una fila.
c) El nombre de la base de datos.
d) Una clave foránea que referencia a la misma tabla.

**Respuesta Correcta:** b)
**Justificación:** Una superclave es cualquier conjunto de atributos que garantiza la unicidad. Una clave candidata es una superclave "mínima" (sin atributos redundantes). Por ejemplo, `{ID}` y `{ID, Nombre}` podrían ser ambas superclaves, pero solo `{ID}` sería una clave candidata.
**Por qué las otras son incorrectas:**
*   a, c, d) Son definiciones incorrectas.

---

**13. Si la tabla A tiene 5 filas y la tabla B tiene 3 filas, ¿cuántas filas tendrá el resultado del Producto Cartesiano (A × B)?**
a) 5
b) 3
c) 8
d) 15

**Respuesta Correcta:** d)
**Justificación:** El producto cartesiano combina cada fila de la primera tabla con cada fila de la segunda, por lo que el número total de filas es el producto de las filas de cada tabla (5 * 3 = 15).
**Por qué las otras son incorrectas:**
*   a, b, c) Son cálculos incorrectos.

---

**14. ¿Puede una Clave Foránea (FK) contener valores `NULL`?**
a) No, nunca.
b) Sí, si la relación que representa es opcional.
c) Sí, pero solo si la clave primaria a la que hace referencia también es nula.
d) Solo en bases de datos no relacionales.

**Respuesta Correcta:** b)
**Justificación:** Si un registro en la tabla hija no necesita estar obligatoriamente relacionado con un registro en la tabla padre (relación opcional), la columna de la clave foránea puede permitirse ser `NULL`.
**Por qué las otras son incorrectas:**
*   a) Es incorrecto, los `NULL` son permitidos en FKs.
*   c) Una clave primaria nunca puede ser nula.
*   d) Las claves foráneas son un concepto del modelo relacional.

---

**15. El término "Relación" en el modelo relacional es un sinónimo de:**
a) Tabla
b) Columna
c) Clave
d) Consulta

**Respuesta Correcta:** a)
**Justificación:** En la terminología formal del modelo relacional, una "relación" es el término matemático para lo que comúnmente llamamos una "tabla".
**Por qué las otras son incorrectas:**
*   b, c, d) Son otros conceptos del modelo.

---

**16. ¿Qué define el "Dominio" de un atributo?**
a) El nombre del atributo.
b) Si el atributo es una clave primaria o no.
c) El conjunto de valores permitidos para ese atributo.
d) La tabla a la que pertenece el atributo.

**Respuesta Correcta:** c)
**Justificación:** El dominio especifica el tipo de dato (ej. `INTEGER`, `VARCHAR(50)`) y, opcionalmente, restricciones adicionales (ej. > 0) que definen qué valores son válidos para una columna.
**Por qué las otras son incorrectas:**
*   a, b, d) Son otras propiedades de un atributo, pero no su dominio.

---

**17. La operación de `JOIN` (⋈) en álgebra relacional se puede definir como:**
a) Una Selección seguida de una Proyección.
b) Un Producto Cartesiano seguido de una Selección.
c) Una Unión seguida de una Diferencia.
d) Una Proyección sobre un Producto Cartesiano.

**Respuesta Correcta:** b)
**Justificación:** Conceptualmente, un `JOIN` entre dos tablas es equivalente a realizar primero un producto cartesiano de ambas y luego aplicar una operación de selección para filtrar solo las filas donde las columnas de unión coinciden.
**Por qué las otras son incorrectas:**
*   a, c, d) No describen la operación de `JOIN`.

---

**18. En una relación de Empleados, el conjunto `{ID_Empleado, DNI}` es una superclave. Si tanto `ID_Empleado` como `DNI` son únicos por sí solos, ¿cuál de las siguientes afirmaciones es correcta?**
a) `{ID_Empleado, DNI}` es una clave candidata.
b) Solo `{ID_Empleado}` puede ser una clave candidata.
c) Tanto `{ID_Empleado}` como `{DNI}` son claves candidatas.
d) No hay claves candidatas.

**Respuesta Correcta:** c)
**Justificación:** Una clave candidata es una superclave mínima. Dado que tanto `{ID_Empleado}` como `{DNI}` pueden identificar de forma única una fila por sí solos, ambos son identificadores únicos mínimos y, por lo tanto, ambos son claves candidatas. `{ID_Empleado, DNI}` es una superclave, pero no una clave candidata porque es redundante.
**Por qué las otras son incorrectas:**
*   a) Es incorrecta porque no es mínima.
*   b) Es incorrecta porque `{DNI}` también es una clave candidata.
*   d) Es incorrecta porque existen dos claves candidatas.

---

**19. El operador de álgebra relacional que corresponde a la cláusula `UNION` en SQL es:**
a) Intersección (∩)
b) Diferencia (-)
c) Unión (∪)
d) Proyección (π)

**Respuesta Correcta:** c)
**Justificación:** El operador de Unión (∪) en álgebra relacional combina dos relaciones (tablas) con esquemas compatibles en una sola, eliminando duplicados, que es la función principal de `UNION` en SQL.
**Por qué las otras son incorrectas:**
*   a, b, d) Corresponden a otras operaciones.

---

**20. Si borras una tabla (con `DROP TABLE`), ¿qué sucede con la integridad referencial?**
a) Nada, las claves foráneas en otras tablas que apuntaban a ella seguirán funcionando.
b) El SGBD mostrará un error y no permitirá borrar la tabla si es referenciada por claves foráneas.
c) Las claves foráneas en otras tablas se convertirán automáticamente a `NULL`.
d) Se borra la tabla, pero se mantiene una copia de seguridad automática.

**Respuesta Correcta:** b)
**Justificación:** La integridad referencial protege las relaciones. La mayoría de los SGBD, por defecto, impedirán que se elimine una tabla si existen claves foráneas en otras tablas que dependen de ella, para evitar dejar "referencias huérfanas".
**Por qué las otras son incorrectas:**
*   a) Esto es falso y violaría la integridad referencial.
*   c) El SGBD no modifica automáticamente otras tablas al hacer un `DROP`; simplemente previene la operación.
*   d) `DROP TABLE` es una operación DDL destructiva y no crea una copia de seguridad.

---

