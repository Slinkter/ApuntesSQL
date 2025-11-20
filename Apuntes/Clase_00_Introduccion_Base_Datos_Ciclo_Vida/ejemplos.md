# Ejemplos - Clase 00: Introducción a Bases de Datos y Ciclo de Vida

### Ejemplo 1: Diferencia entre Dato e Información

Imagina que tienes los siguientes elementos aislados:
*   "20"
*   "Manzana"
*   "Lima"
*   "Soles"

Estos son **datos**. Por sí solos, no nos dan un significado completo ni nos permiten tomar decisiones.

Ahora, si procesamos y contextualizamos estos datos, podemos obtener **información**:
*   "El precio promedio de la fruta 'Manzana' es de '20 Soles' en el mercado de 'Lima'."

Esta información es útil porque nos permite, por ejemplo, comparar precios o decidir si comprar manzanas en Lima es caro o barato.

### Ejemplo 2: Tipos de Bases de Datos

#### Base de Datos Relacional (RDBMS)

Considera una base de datos de una tienda online. Los datos podrían organizarse en tablas interconectadas:

**Tabla `Productos`:**
| ID_Producto | Nombre     | Precio | Stock |
| :---------- | :--------- | :----- | :---- |
| 1           | Laptop     | 1200   | 50    |
| 2           | Teclado    | 75     | 120   |
| 3           | Mouse      | 25     | 200   |

**Tabla `Pedidos`:**
| ID_Pedido | ID_Cliente | Fecha      | Total |
| :-------- | :--------- | :--------- | :---- |
| 101       | 5          | 2023-01-15 | 1300  |
| 102       | 8          | 2023-01-15 | 100   |

**Tabla `Detalle_Pedido`:**
| ID_Detalle | ID_Pedido | ID_Producto | Cantidad | Subtotal |
| :--------- | :-------- | :---------- | :------- | :------- |
| 1          | 101       | 1           | 1        | 1200     |
| 2          | 101       | 3           | 4        | 100      |
| 3          | 102       | 2           | 1        | 75       |
| 4          | 102       | 3           | 1        | 25       |

Aquí, `ID_Producto` en `Detalle_Pedido` es una clave foránea que relaciona esta tabla con la tabla `Productos`, y `ID_Pedido` en `Detalle_Pedido` es una clave foránea que la relaciona con la tabla `Pedidos`. Esta estructura organizada permite consultas complejas y mantiene la integridad de los datos.

#### Base de Datos Orientada a Documentos (NoSQL - MongoDB)

En una BD orientada a documentos, podrías almacenar la información de un pedido como un único documento JSON, ofreciendo flexibilidad si la estructura de los pedidos varía frecuentemente:

```json
{
  "_id": "pedido101",
  "id_cliente": 5,
  "fecha": "2023-01-15",
  "total": 1300,
  "productos": [
    {
      "id_producto": 1,
      "nombre": "Laptop",
      "precio": 1200,
      "cantidad": 1
    },
    {
      "id_producto": 3,
      "nombre": "Mouse",
      "precio": 25,
      "cantidad": 4
    }
  ],
  "direccion_envio": {
    "calle": "Av. Siempre Viva 123",
    "ciudad": "Lima",
    "pais": "Perú"
  }
}
```
Este ejemplo muestra cómo toda la información de un pedido, incluyendo sus detalles y dirección de envío, puede ser contenida en un solo "documento", lo que es útil para datos semiestructurados.
