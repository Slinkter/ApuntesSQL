# Ejercicios Resueltos - Clase 05: Modelamiento de Datos en la Empresa

### Ejercicio 1: Identificación de Componentes del Modelo E-R

**Enunciado:**
Una pequeña agencia de viajes quiere registrar información sobre sus `CLIENTES`, los `PAQUETES_TURISTICOS` que ofrece y las `RESERVAS` que realizan los clientes para esos paquetes.

*   Cada `CLIENTE` tiene un `ID_Cliente` único, `Nombre`, `Apellido` y `Email`.
*   Cada `PAQUETE_TURISTICO` tiene un `Codigo_Paquete` único, `Nombre_Paquete`, `Descripcion`, `Precio` y `Duracion_Dias`.
*   Un `CLIENTE` puede realizar varias `RESERVAS`, y cada `RESERVA` es para un único `PAQUETE_TURISTICO`.
*   Para cada `RESERVA` se registra un `ID_Reserva` único, la `Fecha_Reserva`, la `Cantidad_Personas` y el `Estado_Reserva`.

1.  Identifica las **Entidades Fuerte** y **Débil** (si las hay).
2.  Define las **Relaciones** entre las entidades y especifica su **Cardinalidad** (mínima y máxima).
3.  ¿Existen atributos que podrían pertenecer a una entidad asociativa en alguna de las relaciones que identificaste? ¿Cuáles serían?

---

**Solución:**

1.  **Identificación de Entidades:**
    *   **`CLIENTE`**: Entidad Fuerte (tiene `ID_Cliente` único y existe independientemente).
    *   **`PAQUETE_TURISTICO`**: Entidad Fuerte (tiene `Codigo_Paquete` único y existe independientemente).
    *   **`RESERVA`**: Entidad Fuerte (tiene `ID_Reserva` único y, aunque se relaciona con `CLIENTE` y `PAQUETE_TURISTICO`, podría concebirse como fuerte si su existencia no depende exclusivamente de que un cliente la haga en ese momento o de que el paquete turístico exista, aunque en un modelo más estricto podría ser débil). Para este ejercicio, la consideramos fuerte por tener `ID_Reserva` propio.

2.  **Relaciones y Cardinalidad:**

    *   **Relación: `REALIZA` entre `CLIENTE` y `RESERVA`**
        *   Un `CLIENTE` puede realizar cero, una o muchas `RESERVAS`. (0,N)
        *   Una `RESERVA` es realizada por exactamente un `CLIENTE`. (1,1)
        *   **Cardinalidad:** CLIENTE (0,N) --- REALIZA --- (1,1) RESERVA

    *   **Relación: `ES_PARA` entre `RESERVA` y `PAQUETE_TURISTICO`**
        *   Una `RESERVA` es para exactamente un `PAQUETE_TURISTICO`. (1,1)
        *   Un `PAQUETE_TURISTICO` puede tener cero, una o muchas `RESERVAS`. (0,N)
        *   **Cardinalidad:** RESERVA (1,1) --- ES_PARA --- (0,N) PAQUETE_TURISTICO

3.  **Entidades Asociativas:**
    *   En este escenario, la entidad `RESERVA` actúa ya como una **entidad asociativa** (o una entidad regular que resuelve una relación N:M). Los atributos `Fecha_Reserva`, `Cantidad_Personas` y `Estado_Reserva` son propios de la *asociación* entre un `CLIENTE` y un `PAQUETE_TURISTICO` en un momento dado.
    *   Si hubiéramos modelado una relación directa N:M entre `CLIENTE` y `PAQUETE_TURISTICO` (un cliente reserva muchos paquetes, un paquete es reservado por muchos clientes), y luego se nos pide agregar atributos como `Fecha_Reserva`, `Cantidad_Personas`, etc., entonces tendríamos que convertir esa relación N:M en una entidad asociativa (`RESERVA`) para contener esos atributos. En este caso, ya se presentó `RESERVA` como una entidad desde el inicio con su propia clave.

### Ejercicio 2: Reglas de Negocio y su Impacto en el Modelo

**Enunciado:**
Considera las siguientes reglas de negocio para una tienda online y explica cómo influirían en el diseño de un Modelo Entidad-Relación:

1.  "Un producto debe tener al menos una categoría asignada."
2.  "Los clientes VIP pueden tener un máximo de 5 pedidos pendientes a la vez."
3.  "Cada pedido debe contener al menos un artículo."

**Solución:**

1.  **"Un producto debe tener al menos una categoría asignada."**
    *   **Impacto:** Esto afectaría la **cardinalidad mínima** de la relación entre `PRODUCTO` y `CATEGORIA`. Si modelamos una relación donde `PRODUCTO` "pertenece a" `CATEGORIA`, la cardinalidad mínima desde `PRODUCTO` hacia `CATEGORIA` sería (1,N), indicando que cada `PRODUCTO` *debe* estar asociado con al menos una `CATEGORIA`. Además, la clave foránea `ID_Categoria` en la tabla `PRODUCTO` (asumiendo que `PRODUCTO` tiene FK a `CATEGORIA`) debería ser `NOT NULL`.

2.  **"Los clientes VIP pueden tener un máximo de 5 pedidos pendientes a la vez."**
    *   **Impacto:** Esta es una regla de negocio compleja que no se puede representar directamente solo con cardinalidades o restricciones de integridad estándar en un diagrama E-R o en la definición `CREATE TABLE`.
    *   Requeriría una **restricción semántica o procedimental**. En la implementación, esto se gestionaría a nivel de la aplicación o mediante un `TRIGGER` en la base de datos que se activaría al insertar un nuevo `PEDIDO` para un `CLIENTE_VIP` y verificaría el número de pedidos pendientes.

3.  **"Cada pedido debe contener al menos un artículo."**
    *   **Impacto:** Esto afecta la **cardinalidad mínima** de la relación entre `PEDIDO` y `DETALLE_PEDIDO` (la entidad que representa los artículos dentro de un pedido). La cardinalidad mínima desde `PEDIDO` hacia `DETALLE_PEDIDO` sería (1,N), indicando que cada `PEDIDO` *debe* tener al menos un `DETALLE_PEDIDO` asociado. En la implementación, esto a menudo se asegura a nivel de aplicación o mediante una combinación de `NOT NULL` en la FK de `DETALLE_PEDIDO` a `PEDIDO` y un `CHECK` o `TRIGGER` que impida un pedido sin artículos.
