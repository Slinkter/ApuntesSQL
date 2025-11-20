# Ejemplos - Clase 03: Lenguaje de Definición de Datos (DDL)

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
