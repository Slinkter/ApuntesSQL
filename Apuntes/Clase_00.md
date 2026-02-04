# ☕ Clase 00: Introducción a Bases de Datos y Ciclo de Vida

---

## 📚 Conceptos Clave

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Dato vs. Información** | **¿Cuál es la diferencia?** Imagina que los **Datos** son los ingredientes crudos: "20", "Manzana", "Lima". Por sí solos no dicen mucho. La **Información** es el plato terminado: "La Manzana cuesta 20 soles en Lima". ¡Los datos procesados nos dan significado y nos ayudan a tomar decisiones!. |
| **¿Qué es una Base de Datos (BD)?** | Una BD es como un almacén digital donde guardamos información de manera **persistente** (no se borra). Sirve para almacenar datos que luego podemos recuperar al consultarlos. |
| **Características de una BD** | Las BD son súper confiables. Usan el concepto **CRUD** (Crear, Leer, Actualizar, Eliminar) y cumplen con **ACID** (Atomicity, Consistency, Isolation, Durability). ¡ACID asegura que todas las operaciones sean seguras y coherentes!. |
| **DBMS (Manejador de BD)** | Es el **software guardián** que administra la BD, asegurando que la información esté disponible y resguardada. Se encarga de crear, organizar y manipular la BD, además de mantener la seguridad y la integridad. |
| **Tipos de BD** | ¡Hay muchos tipos! Las **Relacionales** (RDBMS) son las más famosas (Oracle, MSSQL), organizadas en tablas con filas y columnas interconectadas. También están las **Jerárquicas** (como un árbol familiar o de directorios), los **Archivos Planos** (texto simple, para datos muy sencillos), y las **Orientadas a Documentos** (como MongoDB), que son flexibles y útiles para e-commerce. |
| **DBA (Administrador de BD)** | Es el **superhéroe de la BD**. Sus responsabilidades incluyen la planificación de la seguridad, los respaldos, la instalación del software, la creación de la BD y el monitoreo del desempeño. |
| **Fases de Diseño** | Para construir una BD, seguimos tres pasos: **1. Conceptual** (identificar requerimientos y entidades), **2. Lógico** (definir las relaciones y cómo el sistema soportará los requerimientos, dependiendo del DBMS), y **3. Físico** (determinar la representación real de las tablas en el software). |

**Resumen de la Clase 00:** Esta clase nos presentó la **Ingeniería de Datos**, explicando que los datos sin procesar se transforman en información valiosa para la toma de decisiones. Una BD, manejada por un DBMS, es un conjunto de datos persistentes y confiables (gracias a ACID/CRUD). Vimos que el diseño pasa por fases Conceptual, Lógica y Física, y que el DBA es clave para mantener todo funcionando.

---

---

## 💡 Ejemplos Prácticos

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

---

## ✏️ Ejercicios Resueltos

### Ejercicio 1: Diferenciando Datos e Información

**Enunciado:**
Clasifica los siguientes elementos como **Dato** o **Información** y justifica tu respuesta.

1.  "María"
2.  "La edad promedio de los estudiantes de la clase de Bases de Datos es 22 años."
3.  "25.50"
4.  "El producto 'Café Supremo' se vende a 25.50 soles en la sucursal del centro."

**Solución:**

1.  **"María": Dato.** Es un nombre, un elemento individual sin contexto o procesamiento adicional que le dé un significado más allá de su valor literal.
2.  **"La edad promedio de los estudiantes de la clase de Bases de Datos es 22 años.": Información.** Este enunciado ha sido procesado (se calculó un promedio) y contextualizado (se refiere a los estudiantes de una clase específica), lo que le otorga un significado útil.
3.  **"25.50": Dato.** Es un número aislado. Podría ser un precio, una cantidad, una medida, etc., pero sin contexto, es solo un valor en bruto.
4.  **"El producto 'Café Supremo' se vende a 25.50 soles en la sucursal del centro.": Información.** Se han combinado varios datos (nombre del producto, precio, moneda, ubicación) y se han procesado para ofrecer un mensaje con significado completo y relevante.

### Ejercicio 2: Identificando Roles y Conceptos en BD

**Enunciado:**
Considera el siguiente escenario y responde a las preguntas:

"En una gran universidad, un sistema guarda las calificaciones de los estudiantes, los cursos que toman y la información de los profesores. Todos estos datos se almacenan de manera organizada y persistente. Cuando un profesor sube una nota, esta acción es manejada por un software específico que asegura que la nota se guarde correctamente y que el promedio del estudiante se actualice de forma fiable. Un equipo especializado se encarga de que este sistema funcione 24/7, realice copias de seguridad y gestione quién puede ver o modificar las notas."

1.  ¿Qué concepto fundamental se describe al decir que los datos se guardan de manera "organizada y persistente"?
2.  El "software específico que asegura que la nota se guarde correctamente y que el promedio del estudiante se actualice de forma fiable" ¿a qué componente principal de un sistema de bases de datos se refiere?
3.  El "equipo especializado" que gestiona la operatividad, copias de seguridad y permisos ¿qué rol o figura representa en el ámbito de las bases de datos?
4.  Cuando se menciona que la actualización del promedio del estudiante se hace de forma "fiable", ¿a qué conjunto de propiedades de las transacciones de bases de datos se hace alusión?

**Solución:**

1.  **Base de Datos (BD).** Una base de datos es una colección organizada y persistente de datos.
2.  **DBMS (Sistema de Gestión de Base de Datos).** Es el software encargado de definir, crear, mantener, controlar el acceso y manipular la base de datos de manera fiable y eficiente.
3.  **DBA (Administrador de Base de Datos).** Son los profesionales responsables de la administración, seguridad, rendimiento y disponibilidad de la base de datos.
4.  **Propiedades ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad).** La fiabilidad en las transacciones se asegura mediante el cumplimiento de estas propiedades, que garantizan que las operaciones se completen íntegramente y dejen la base de datos en un estado válido.

---

