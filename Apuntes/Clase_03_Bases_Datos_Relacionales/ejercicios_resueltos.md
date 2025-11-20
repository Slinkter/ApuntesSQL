# Ejercicios Resueltos - Clase 03: Lenguaje de Definición de Datos (DDL)

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