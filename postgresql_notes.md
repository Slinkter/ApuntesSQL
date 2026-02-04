
# Clase 00: Introducción a Bases de Datos y Ciclo de Vida

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

---

# Ejercicios Resueltos - Clase 00: Introducción a Bases de Datos y Ciclo de Vida

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

# Glosario - Clase 00: Introducción a Bases de Datos y Ciclo de Vida

*   **ACID (Atomicity, Consistency, Isolation, Durability):** Propiedades que garantizan que las transacciones de base de datos se procesen de manera confiable.
*   **Archivos Planos (BD):** Tipo de base de datos simple donde los datos se almacenan en un archivo de texto sin formato, con poca estructura.
*   **Base de Datos (BD):** Almacén digital donde se guarda información de manera persistente, permitiendo su recuperación y consulta.
*   **CRUD (Create, Read, Update, Delete):** Las cuatro operaciones básicas que se pueden realizar sobre los datos en una base de datos.
*   **Dato:** Ingrediente crudo o hecho aislado, sin procesar ni contextualizar.
*   **DBA (Administrador de BD):** Profesional encargado de la planificación, seguridad, respaldo, instalación, creación y monitoreo del desempeño de una base de datos.
*   **DBMS (Database Management System):** Software que administra, organiza y manipula una base de datos, garantizando su disponibilidad, seguridad e integridad.
*   **Fase Conceptual (Diseño BD):** Primera fase del diseño de una base de datos, donde se identifican los requerimientos y las entidades.
*   **Fase Física (Diseiso BD):** Tercera fase del diseño de una base de datos, que determina la representación real de las tablas y estructuras en el software.
*   **Fase Lógica (Diseño BD):** Segunda fase del diseño de una base de datos, donde se definen las relaciones y cómo el sistema soportará los requerimientos, dependiendo del DBMS.
*   **Información:** Datos procesados, contextualizados y organizados que adquieren significado y son útiles para la toma de decisiones.
*   **Jerárquicas (BD):** Tipo de base de datos donde los datos se organizan en una estructura de árbol, con relaciones padre-hijo.
*   **Orientadas a Documentos (BD):** Tipo de base de datos NoSQL que almacena datos en formatos semiestructurados como JSON, ofreciendo gran flexibilidad.
*   **RDBMS (Relational Database Management System):** Sistema de gestión de bases de datos relacionales, donde los datos se organizan en tablas interconectadas por medio de relaciones.

---

# Clase 01: Fundamentos de Administración de Información

**Fecha:** 2013 (Inferido de la diapositiva de presentación), Revisión 2013-1

---

## Pistas y Keywords

*   **Dato vs. Información:** El dato es objetivo, la información es subjetiva.
*   **Jerarquía del Conocimiento:** Datos -> Información -> Conocimiento.
*   **Sistemas Heredados:** Procesamiento tradicional de archivos.
*   **Problemas Clave:**
    *   Redundancia de datos.
    *   Dependencia programa-dato.
    *   Inconsistencia de datos.
*   **Solución:** Enfoque de Base de Datos.
*   **DBMS:** Sistema de Gestión de Base de Datos.
*   **Metadatos:** Datos sobre los datos.
*   **Componentes del Entorno:** CASE, Repositorio, DBMS, Base de Datos, Aplicaciones.
*   **SDLC:** Ciclo de Vida de Desarrollo de Sistemas.
*   **Evolución de BD:** Jerárquico, Redes, Relacional, Objeto-Relacional, NoSQL.
*   **SQL:** Lenguaje de Consulta Estructurado (DML, DDL, DCL).

---

## Notas Generales

### Del Dato al Conocimiento

El punto de partida de la gestión de información es la distinción entre conceptos fundamentales:

*   **Dato:** Es una representación simbólica de un hecho o mensaje, como una cifra o un nombre. Debe ser **objetivo** y tiene poco significado semántico por sí solo. (Ej: 3.50).
*   **Información:** Es el resultado de procesar y contextualizar los datos, disminuyendo la incertidumbre. Puede ser **subjetiva**, ya que su significado es percibido por el receptor. (Ej: Un reporte mostrando que el precio de un producto subió de 2.0 a 3.50).
*   **Conocimiento:** Es el entendimiento derivado de la información, que requiere reflexión y síntesis. A menudo es tácito y permite la toma de decisiones. (Ej: "Las ventas de un producto cayeron porque el precio subió, debemos ajustar la estrategia").

### El Problema: Sistemas Tradicionales de Archivos

Antes del enfoque de bases de datos, las empresas utilizaban sistemas de procesamiento de archivos. Cada aplicación (Facturación, Pedidos, Nóminas) mantenía sus propios archivos de datos privados. Este enfoque presentaba graves desventajas:

1.  **Dependencia Programa-Datos:** El código de la aplicación estaba estrechamente ligado a la estructura física de los datos. Un simple cambio en el formato de un archivo requería modificar todos los programas que lo usaban.
2.  **Redundancia de Datos:** La misma información (como los datos de un cliente) se duplicaba en múltiples archivos, desperdiciando espacio y generando un gran problema de mantenimiento.
3.  **Inconsistencia de Datos:** El principal problema de la redundancia. Si un dato se actualizaba en un archivo pero no en otro, se perdía la integridad y la confianza en la información.
4.  **Acceso Limitado y No Estándar:** No había una forma centralizada o estandarizada de consultar o compartir datos entre aplicaciones.

### La Solución: El Enfoque de Base de Datos

Para resolver estos problemas, surge el concepto de **Base de Datos (BD)**: una colección de datos lógicamente relacionados y centralizados, diseñados para ser compartidos por múltiples usuarios y aplicaciones.

Esta centralización es gestionada por un **Sistema de Gestión de Base de Datos (DBMS)**, que es un software que actúa como intermediario entre los usuarios/aplicaciones y la base de datos física.

**Ventajas del enfoque de BD:**

*   **Independencia Programa-Datos:** El DBMS maneja los metadatos (la definición de los datos). Las aplicaciones ya no necesitan conocer la estructura física de almacenamiento, lo que facilita el mantenimiento.
*   **Redundancia Mínima:** Al centralizar los datos, se reduce drásticamente la duplicación, mejorando la consistencia e integridad.
*   **Calidad y Compartición de Datos Mejoradas:** Se pueden aplicar reglas de validación y restricciones de forma centralizada. Diferentes usuarios pueden acceder a las mismas fuentes de datos.
*   **Reforzamiento de Estándares:** El acceso a los datos se realiza de manera uniforme a través del DBMS.
*   **Seguridad y Recuperación Centralizadas:** El DBMS provee mecanismos para control de acceso, backups y recuperación ante desastres.

### Componentes de un Entorno de Base de Datos

Un entorno de base de datos moderno incluye varios componentes clave que trabajan juntos:

*   **Herramientas CASE:** Para el diseño de la BD y las aplicaciones.
*   **Repositorio:** Una base de conocimientos que almacena los metadatos (definiciones, relaciones, formatos).
*   **DBMS:** El software que gestiona la base de datos.
*   **Base de Datos:** La colección de datos operativos.
*   **Aplicaciones:** Programas que interactúan con la base de datos.

### Evolución de las Bases de Datos

El modelo de bases de datos ha evolucionado a lo largo del tiempo para adaptarse a nuevas necesidades:
*   **1960s:** Modelos Jerárquicos (IMS) y de Redes (CODASYL).
*   **1980s:** Modelo Relacional (Oracle, DB2), que se convirtió en el estándar de la industria.
*   **1990s:** Modelos Orientados a Objetos y Objeto-Relacional.
*   **2000s:** Auge de las bases de datos para la Web, XML y NoSQL, diseñadas para grandes volúmenes de datos y flexibilidad.

---

## Resumen Final Crítico

Esta clase establece la justificación fundamental para la existencia de las bases de datos. La transición desde los sistemas de archivos tradicionales, plagados de redundancia, inconsistencia y altos costos de mantenimiento, hacia un enfoque centralizado gestionado por un DBMS, resolvió problemas críticos de negocio. Comprender que una base de datos no es solo un "almacén", sino un ecosistema completo (con DBMS, metadatos y herramientas) que garantiza la independencia entre datos y aplicaciones, es el pilar para construir sistemas de información robustos, consistentes y mantenibles. Este fundamento histórico y conceptual es esencial para apreciar el diseño y la función del modelo relacional y otras tecnologías de datos que se estudiarán a continuación.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta es la clase fundacional del curso de Ingeniería de Datos.
*   **Conexiones Siguientes:** Los conceptos aquí presentados son la base para entender la **Clase 02 (Sistemas de Gestión de Base de Datos)**, donde se profundizará en el rol y la arquitectura del DBMS. También proporciona el contexto para la **Clase 03 (Bases de Datos Relacionales)**, que explora el modelo dominante que surgió como solución a los problemas aquí planteados, y para la **Clase 04 (Administración de RDBMS)**, que aborda la gestión práctica de estos sistemas.

---

# Ejemplos - Clase 01: Fundamentos de Administración de Información

### Ejemplo 1: Diferencia entre Dato, Información y Conocimiento

Este ejemplo, extraído de las diapositivas de la clase, ilustra cómo los conceptos se conectan en un escenario de negocio.

#### 1.1. Dato

Un **dato** es un valor crudo, sin contexto. Por sí mismo, no nos dice mucho.

| Campo  | Valor |
| :----- | :---- |
| Precio | 3.50  |

Esto es solo un número. No sabemos qué producto es, en qué moneda está o si es un precio de compra o de venta.

Para que tenga más significado, un dato debe formar parte de una estructura.

| Código | Nombre        | Tipo | Precio | Sabor   |
| :----- | :------------ | :--- | :----- | :------ |
| 001    | Cola manzana  | Cola | 3.50   | Manzana |

Ahora tenemos datos estructurados, pero siguen siendo solo eso: datos.

#### 1.2. Información

La **información** se genera al procesar los datos para revelar patrones o tendencias. Reduce la incertidumbre.

**Reporte de Evolución de Precios: Cola Manzana**

| Año  | Precio |
| :--- | :----- |
| 2000 | 2.0    |
| 2001 | 2.7    |
| 2002 | 2.9    |
| 2003 | 3.5    |

Este reporte nos informa que el precio de la "Cola Manzana" ha estado subiendo consistentemente a lo largo de los años. Esto es mucho más útil que el simple dato "3.50".

#### 1.3. Conocimiento

El **conocimiento** se deriva de analizar la información, a menudo combinando diferentes conjuntos de datos, para tomar una decisión informada.

**Reporte Cruzado de Ventas vs. Precios**

| Año  | Nombre Cola   | Precio | Venta      |
| :--- | :------------ | :----- | :--------- |
| 2000 | Cola frutilla | 2.5    | 2,000,000  |
| 2001 | Cola frutilla | 2.5    | 1,800,000  |
| 2000 | Cola manzana  | 2.0    | 2,000,000  |
| 2001 | Cola manzana  | 2.7    | 2,400,000  |

**Análisis y Decisión (Conocimiento):**
> "Observamos que la venta de 'Cola frutilla' ha disminuido a pesar de mantener su precio. Por otro lado, 'Cola manzana', a pesar de haber subido de precio, aumentó sus ventas. **Conclusión:** Debemos darle un mayor impulso de marketing a la 'Cola manzana' y quizás revisar la estrategia de 'Cola frutilla'."

### Ejemplo 2: Metadatos

Los **metadatos** son "datos sobre los datos". Describen la estructura, las reglas y el contexto de los datos de la aplicación.

Tomando el ejemplo de una lista de estudiantes de un curso:

**Tabla de Datos: `ClassRoster`**

| Course               | Section | Semester     | Name             | ID    | Major | GPA |
| :------------------- | :------ | :----------- | :--------------- | :---- | :---- | :-- |
| MGT 500 Business Pol | 2       | Spring 200X  | Baker, Kenneth D | 32491 | MGT   | 3.2 |
| ...                  | ...     | ...          | ...              | ...   | ...   | ... |

**Tabla de Metadatos para `ClassRoster`**

| Data Item | Type         | Length | Min | Max | Description                 |
| :-------- | :----------- | :----- | :-- | :-- | :-------------------------- |
| Course    | Alphanumeric | 30     |     |     | Course ID and name          |
| Section   | Integer      | 1      | 1   | 9   | Section number              |
| Semester  | Alphanumeric | 10     |     |     | Semester and year           |
| Name      | Alphanumeric | 30     |     |     | Student name                |
| ID        | Integer      | 9      |     |     | Student ID (SSN)            |
| Major     | Alphanumeric | 4      |     |     | Student major               |
| GPA       | Decimal      | 3      | 0.0 | 4.0 | Student grade point average |

Esta tabla de metadatos es fundamental para que el DBMS sepa cómo almacenar y validar los datos, y para que los desarrolladores sepan cómo interactuar con ellos.

---

# Ejercicios Resueltos - Clase 01: Fundamentos de Administración de Información

### Ejercicio 1: Identificación de Problemas en un Sistema de Ficheros Tradicional

#### Enunciado

Una pequeña empresa de ventas gestiona sus operaciones con tres departamentos: **Pedidos**, **Contabilidad** y **Nóminas**. Cada departamento ha desarrollado sus propias aplicaciones y gestiona sus propios archivos de datos, como se muestra en el siguiente diagrama (inspirado en la diapositiva 14 de la clase):

*   **Departamento de Pedidos:**
    *   Tiene una aplicación para la **Gestión de Órdenes**.
    *   Utiliza los archivos: `Customer_Master_File.dat`, `Inventory_Master_File.dat` y `Back_Order_File.dat`.

*   **Departamento de Contabilidad:**
    *   Tiene una aplicación para la **Facturación (Invoicing)**.
    *   Utiliza los archivos: `Inventory_Pricing_File.dat` y `Customer_Master_File.dat`.

*   **Departamento de Nóminas:**
    *   Tiene una aplicación para gestionar el **Pago a Empleados**.
    *   Utiliza el archivo: `Employee_Master_File.dat`.

**Preguntas:**

1.  **Redundancia de Datos:** ¿Qué archivo(s) específico(s) representa(n) un claro ejemplo de redundancia de datos en este sistema? ¿Por qué es un problema?
2.  **Inconsistencia de Datos:** Describe un escenario práctico en el que podría ocurrir una inconsistencia de datos. ¿Cuál sería el impacto en el negocio?
3.  **Dependencia Programa-Dato:** El departamento de Contabilidad decide que necesita añadir un campo "descuento_cliente" al `Customer_Master_File.dat`. ¿Qué implicaciones tiene este cambio en el sistema global?

---

#### Solución

##### 1. Redundancia de Datos

*   **Archivo Redundante:** El `Customer_Master_File.dat` es el ejemplo más claro de redundancia. Existe una copia tanto en el departamento de **Pedidos** como en el de **Contabilidad**.
*   **Problema:**
    *   **Ineficiencia de Almacenamiento:** Se está utilizando espacio en disco para guardar la misma información dos veces.
    *   **Complejidad en la Actualización:** Cualquier cambio en los datos de un cliente (ej. cambio de dirección o teléfono) debe realizarse en **ambos archivos** por separado, lo que aumenta la carga de trabajo y el riesgo de errores.
    *   **Fuente de Inconsistencias:** Es la causa directa del siguiente problema.

##### 2. Escenario de Inconsistencia de Datos

*   **Escenario:** Un cliente, "ABC Corp", llama al departamento de Pedidos para informar que ha cambiado su dirección de facturación. El empleado de Pedidos actualiza la dirección en *su* copia del `Customer_Master_File.dat`. Sin embargo, nadie notifica al departamento de Contabilidad para que actualice *su* copia del mismo archivo.
*   **Impacto en el Negocio:**
    *   Al final del mes, Contabilidad emite una factura para "ABC Corp" y la envía a la **dirección antigua**, que está en su archivo desactualizado.
    *   El cliente nunca recibe la factura, o la recibe con mucho retraso.
    *   La empresa experimenta un retraso en el cobro, lo que afecta su flujo de caja.
    *   Se proyecta una imagen poco profesional y se genera una mala experiencia para el cliente, que podría perder la confianza en la empresa.

##### 3. Implicaciones de la Dependencia Programa-Dato

*   **Implicaciones del Cambio:**
    1.  **Modificación en Contabilidad:** El equipo de desarrollo de Contabilidad debe modificar su aplicación de **Facturación** para que pueda manejar el nuevo campo "descuento_cliente" en su versión del `Customer_Master_File.dat`.
    2.  **Falla en Pedidos:** La aplicación de **Gestión de Órdenes** del departamento de Pedidos **dejará de funcionar** o funcionará incorrectamente. Su código no está preparado para leer un archivo `Customer_Master_File.dat` con una estructura diferente (el nuevo campo añadido). No sabe cómo interpretar ese dato extra.
    3.  **Necesidad de Coordinación y Doble Trabajo:** Para que el sistema vuelva a ser estable, el departamento de Pedidos también tendría que modificar su aplicación, incluso si no necesita usar el campo "descuento_cliente". Esto demuestra una fuerte **dependencia programa-dato**: un cambio en los datos obliga a realizar cambios en múltiples programas, generando costos, retrasos y una alta fragilidad en el sistema.

---

# Balotario - Clase 01: Fundamentos de Administración de Información

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿Cuál es la definición principal de "Administración de Información"?**
a) El proceso de crear hardware y software.
b) El proceso de organizar, almacenar y mantener datos para asegurar su disponibilidad, integridad y seguridad.
c) El acto de escribir código para aplicaciones web.
d) La venta de datos a terceros.

**Respuesta Correcta:** b)
**Justificación:** La administración de información se centra en la gestión del ciclo de vida de los datos, garantizando que sean un activo confiable y seguro para la organización.
**Por qué las otras son incorrectas:**
*   a) La creación de hardware y software es parte del desarrollo de sistemas, pero no la definición de la administración de información.
*   c) Escribir código es una tarea de desarrollo de software, no de gestión de la información en sí.
*   d) La venta de datos puede ser un resultado del uso de la información, pero no define el proceso de su administración interna.

---

**2. ¿Cuál es la diferencia fundamental entre "dato" e "información"?**
a) No hay diferencia, son sinónimos.
b) "Dato" es un hecho crudo sin procesar, mientras que "información" son datos procesados con contexto y significado.
c) "Información" son los archivos en una computadora y "dato" es el texto dentro de ellos.
d) "Dato" es la información que ha sido verificada por un gerente.

**Respuesta Correcta:** b)
**Justificación:** El concepto clave es la transformación. Los datos (ej. "30", "Juan") se convierten en información cuando se procesan y contextualizan (ej. "Juan tiene 30 años").
**Por qué las otras son incorrectas:**
*   a) No son sinónimos; representan diferentes niveles de abstracción.
*   c) Esta es una analogía imprecisa; tanto el archivo como su contenido pueden ser considerados datos antes de ser interpretados.
*   d) La verificación es un paso en la gestión de la calidad de los datos, pero no define la diferencia fundamental entre dato e información.

---

**3. ¿Cuáles son los tres pilares de la administración de información mencionados en las notas?**
a) Velocidad, Volumen y Variedad.
b) Hardware, Software y Datos.
c) Disponibilidad, Integridad y Seguridad.
d) Creación, Uso y Eliminación.

**Respuesta Correcta:** c)
**Justificación:** Estos tres pilares son los objetivos principales de la administración de información: que los datos estén disponibles cuando se necesiten, que sean correctos y consistentes (integridad), y que estén protegidos contra accesos no autorizados (seguridad).
**Por qué las otras son incorrectas:**
*   a) Estas son las "3 Vs" del Big Data, no los pilares de la administración de información en general.
*   b) Estos son componentes de un sistema de información, pero no los objetivos de la gestión de los datos.
*   d) Estas son etapas del ciclo de vida de la información, no los pilares de su administración.

---

**4. ¿Qué componente NO forma parte de un Sistema de Información según las notas?**
a) Hardware
b) Personas
c) Procesos de negocio
d) Competencia del mercado

**Respuesta Correcta:** d)
**Justificación:** Un Sistema de Información incluye hardware, software, datos, personas y procesos. La competencia del mercado es un factor externo que puede influir en la estrategia de la empresa, pero no es un componente interno del sistema en sí.
**Por qué las otras son incorrectas:**
*   a, b, c) Todos son componentes estándar de un Sistema de Información.

---

**5. ¿Qué etapa del "Ciclo de Vida de la Información" implica la organización y el almacenamiento de los datos?**
a) Creación o captura
b) Almacenamiento
c) Uso y distribución
d) Archivado o eliminación

**Respuesta Correcta:** b)
**Justificación:** Después de que los datos son creados o capturados, la siguiente etapa lógica es su almacenamiento organizado en un sistema, como una base de datos.
**Por qué las otras son incorrectas:**
*   a) Es la etapa inicial donde se generan los datos.
*   c) Ocurre después de que los datos ya están almacenados.
*   d) Es la etapa final del ciclo de vida.

---

**6. ¿Cuál de los siguientes NO es un beneficio directo de una buena administración de información?**
a) Mejora en la toma de decisiones.
b) Reducción de los salarios de los empleados.
c) Optimización de la eficiencia operacional.
d) Obtención de una ventaja competitiva.

**Respuesta Correcta:** b)
**Justificación:** Una buena administración de información puede mejorar la eficiencia, pero no tiene una relación directa con la reducción de salarios. Su objetivo es hacer que los empleados sean más efectivos, no más baratos.
**Por qué las otras son incorrectas:**
*   a, c, d) Todos son beneficios clave de gestionar la información como un activo estratégico.

---

**7. Desde la perspectiva de las bases de datos, ¿cuál es el componente central para la gestión de la información?**
a) La red de computadoras.
b) El sistema operativo.
c) La base de datos.
d) La interfaz de usuario.

**Respuesta Correcta:** c)
**Justificación:** Las notas establecen que la base de datos es el componente central para la gestión y administración de la información, ya que es el repositorio organizado donde residen los datos.
**Por qué las otras son incorrectas:**
*   a, b, d) Son componentes importantes del sistema de información general, pero la base de datos es el núcleo de la gestión de los datos en sí.

---

**8. Convertir una lista de números (101, 102, 103) en "los códigos de los productos más vendidos" es un ejemplo de:**
a) Creación de datos.
b) Transformación de datos en información.
c) Seguridad de la información.
d) Almacenamiento de datos.

**Respuesta Correcta:** b)
**Justificación:** Se está tomando un dato crudo (la lista de números) y se le está añadiendo contexto y significado ("códigos de los productos más vendidos"), convirtiéndolo en información útil.
**Por qué las otras son incorrectas:**
*   a) Los datos (los números) ya existían.
*   c) No se está aplicando ninguna medida de seguridad.
*   d) El acto descrito es de interpretación, no de almacenamiento.

---

**9. La regla "un cliente no puede tener un saldo negativo" es un ejemplo de:**
a) Disponibilidad
b) Seguridad
c) Integridad
d) Rendimiento

**Respuesta Correcta:** c)
**Justificación:** La integridad se refiere a la exactitud, consistencia y validez de los datos. Una regla de negocio como esta asegura que los datos se mantengan dentro de límites lógicos y correctos.
**Por qué las otras son incorrectas:**
*   a) La disponibilidad se refiere a poder acceder a los datos.
*   b) La seguridad se refiere a proteger los datos del acceso no autorizado.
*   d) El rendimiento se refiere a la velocidad con que se procesan los datos.

---

**10. ¿Por qué es importante el "Cumplimiento Normativo" en la administración de información?**
a) Para asegurar que el software esté actualizado.
b) Para ayudar a cumplir con leyes y regulaciones, como las de protección de datos.
c) Para garantizar que todos los datos se almacenen en un único servidor.
d) Para optimizar el rendimiento de las consultas.

**Respuesta Correcta:** b)
**Justificación:** Muchas industrias y países tienen leyes estrictas sobre cómo se deben manejar los datos personales y financieros (ej. GDPR, HIPAA). La administración de información es clave para cumplir con estas normativas.
**Por qué las otras son incorrectas:**
*   a, c, d) Son aspectos de la gestión de TI, pero no se refieren directamente al cumplimiento de leyes externas.

---

**11. ¿Qué se entiende por "Dato Crudo"?**
a) Información que es difícil de entender.
b) Un hecho individual sin contexto ni procesamiento.
c) Datos que han sido encriptados.
d) Un resumen ejecutivo para la gerencia.

**Respuesta Correcta:** b)
**Justificación:** "Dato crudo" es sinónimo de "dato" en su forma más básica, antes de ser interpretado o procesado para convertirlo en información.
**Por qué las otras son incorrectas:**
*   a) La dificultad de entendimiento no es la definición, aunque los datos crudos pueden serlo.
*   c) La encriptación es una medida de seguridad, no una definición del estado del dato.
*   d) Un resumen es un ejemplo de información altamente procesada, lo opuesto a un dato crudo.

---

**12. La afirmación "esta clase es la piedra angular para comprender los Sistemas de Gestión de Bases de Datos" se refiere a:**
a) La importancia de la seguridad.
b) La conexión de la Clase 01 con las clases siguientes.
c) La dificultad de la Clase 01.
d) La necesidad de usar hardware moderno.

**Respuesta Correcta:** b)
**Justificación:** Esta afirmación, extraída de las notas, explica cómo los conceptos fundamentales de la administración de información sientan las bases para entender las tecnologías específicas (como los SGBD) que se estudiarán más adelante.
**Por qué las otras son incorrectas:**
*   a, c, d) No reflejan el significado de la frase, que trata sobre la secuencia y la dependencia del aprendizaje.

---

**13. Un sistema que permite a un cajero de supermercado escanear productos y procesar un pago es un ejemplo de:**
a) Un sistema para la ventaja competitiva.
b) Un sistema para el cumplimiento normativo.
c) Un sistema para la eficiencia operacional.
d) Un sistema de archivado de datos.

**Respuesta Correcta:** c)
**Justificación:** El propósito principal de este sistema es optimizar y agilizar una operación de negocio diaria (la venta), lo cual es un claro ejemplo de búsqueda de eficiencia operacional.
**Por qué las otras son incorrectas:**
*   a) Aunque la eficiencia puede llevar a una ventaja competitiva, la función principal del sistema es operativa.
*   b) El sistema debe cumplir con normativas (fiscales, etc.), pero su propósito principal es la operación.
*   d) El sistema genera datos que luego pueden ser archivados, pero no es un sistema de archivado en sí.

---

**14. ¿Qué pilar de la administración de información se ve comprometido si un hacker accede a la lista de clientes?**
a) Disponibilidad
b) Integridad
c) Seguridad
d) Rendimiento

**Respuesta Correcta:** c)
**Justificación:** La seguridad se refiere a la protección contra el acceso no autorizado. Un acceso por parte de un hacker es una violación directa de la seguridad de los datos.
**Por qué las otras son incorrectas:**
*   a) La disponibilidad no se ve afectada si los usuarios legítimos aún pueden acceder a los datos.
*   b) La integridad no se ve afectada si el hacker solo lee los datos y no los modifica.
*   d) El rendimiento no tiene relación directa con el acceso no autorizado.

---

**15. ¿Cuál de los siguientes es el mejor ejemplo de "Información"?**
a) 120/80
b) "La presión arterial del paciente es 120/80, lo cual está en el rango normal."
c) La base de datos de pacientes.
d) El nombre "Carlos".

**Respuesta Correcta:** b)
**Justificación:** Esta opción toma los datos crudos ("120/80") y les añade contexto ("presión arterial del paciente") y significado ("rango normal"), convirtiéndolos en información procesable.
**Por qué las otras son incorrectas:**
*   a, d) Son datos crudos.
*   c) Es el contenedor de los datos, no la información interpretada.

---

**16. La etapa final del ciclo de vida de la información es:**
a) Uso y distribución.
b) Almacenamiento.
c) Creación.
d) Archivado o eliminación.

**Respuesta Correcta:** d)
**Justificación:** Una vez que la información ya no es necesaria para las operaciones activas, se archiva para retención a largo plazo o se elimina de forma segura, concluyendo su ciclo de vida.
**Por qué las otras son incorrectas:**
*   a, b, c) Son etapas anteriores en el ciclo de vida de la información.

---

**17. El principal objetivo de la administración de información es:**
a) Acumular la mayor cantidad de datos posible.
b) Transformar los datos en un activo valioso para la organización.
c) Asegurar que todos los empleados tengan acceso a todos los datos.
d) Crear los algoritmos de software más rápidos.

**Respuesta Correcta:** b)
**Justificación:** El objetivo final es tratar los datos como un activo estratégico, lo que implica gestionarlos de manera que generen valor, apoyen decisiones y mejoren las operaciones.
**Por qué las otras son incorrectas:**
*   a) La calidad y la relevancia de los datos son más importantes que la cantidad bruta.
*   c) La seguridad implica un acceso controlado y restringido, no un acceso universal.
*   d) La velocidad de los algoritmos es un tema de desarrollo de software, no el objetivo principal de la gestión de la información.

---

**18. ¿Qué garantiza la "Disponibilidad" de la información?**
a) Que los datos son 100% correctos.
b) Que los datos están protegidos por contraseñas fuertes.
c) Que los usuarios autorizados pueden acceder a los datos cuando los necesitan.
d) Que los datos antiguos se eliminan automáticamente.

**Respuesta Correcta:** c)
**Justificación:** La disponibilidad se centra en el acceso. Un sistema de información bien administrado asegura que no haya interrupciones indebidas y que la información esté accesible para quienes la necesitan para realizar su trabajo.
**Por qué las otras son incorrectas:**
*   a) Esto se refiere a la integridad.
*   b) Esto se refiere a la seguridad.
*   d) Esto se refiere a una política de retención dentro del ciclo de vida.

---

**19. ¿Cuál es la relación entre un "Sistema de Información" y una "Base de Datos"?**
a) Son lo mismo.
b) Una base de datos es uno de los componentes clave de un sistema de información.
c) Un sistema de información es un tipo de base de datos.
d) No tienen ninguna relación.

**Respuesta Correcta:** b)
**Justificación:** Un sistema de información es un concepto amplio que incluye personas, procesos, hardware, software, y datos. La base de datos es el componente de software/datos donde la información se almacena de forma organizada.
**Por qué las otras son incorrectas:**
*   a, c, d) Son afirmaciones incorrectas sobre la relación jerárquica y funcional entre ambos conceptos.

---

**20. Identificar una nueva tendencia de mercado analizando los datos de ventas es un ejemplo de:**
a) Eficiencia operacional.
b) Ventaja competitiva.
c) Ciclo de vida de la información.
d) Disponibilidad de datos.

**Respuesta Correcta:** b)
**Justificación:** Utilizar la información para identificar oportunidades de negocio (como una nueva tendencia) y responder a ellas antes que la competencia es una forma clara de generar una ventaja competitiva.
**Por qué las otras son incorrectas:**
*   a) La eficiencia operacional se refiere a mejorar los procesos internos existentes, no tanto a descubrir nuevas oportunidades.
*   c, d) Son conceptos de la administración de información, pero no describen el resultado estratégico del análisis.

---

# Glosario - Clase 01: Fundamentos de Administración de Información

*   **Administración de Información:** Conjunto de procesos y estrategias para adquirir, organizar, almacenar, proteger y recuperar datos de manera eficiente.
*   **Base de Datos (BD):** Colección organizada de datos lógicamente relacionados y centralizados, diseñados para ser compartidos por múltiples usuarios y aplicaciones.
*   **Ciclo de Vida de Desarrollo de Sistemas (SDLC):** Proceso estructurado que se sigue para el desarrollo de sistemas de información, desde la planificación hasta el mantenimiento.
*   **Dato:** Un hecho o cifra en bruto, sin procesar. Debe ser objetivo.
*   **Dependencia Programa-Dato:** Acoplamiento estrecho entre el código de una aplicación y la estructura física de los datos que maneja. Es un problema clave de los sistemas de ficheros tradicionales.
*   **DBMS (Database Management System):** Sistema de Gestión de Base de Datos. Software que actúa como intermediario entre las aplicaciones y la base de datos, gestionando el acceso y la manipulación de los datos.
*   **Disponibilidad de Datos:** Garantía de que los datos están accesibles para usuarios autorizados cuando se necesitan.
*   **Herramientas CASE (Computer-Aided Software Engineering):** Software utilizado para automatizar y asistir en el diseño y desarrollo de sistemas de información y bases de datos.
*   **Información:** Datos procesados y contextualizados que disminuyen la incertidumbre. Puede ser subjetiva.
*   **Inconsistencia de Datos:** Situación que ocurre cuando copias del mismo dato no coinciden entre sí, generalmente como resultado de la redundancia.
*   **Integridad de Datos:** La exactitud, consistencia y fiabilidad de los datos a lo lo largo de su ciclo de vida.
*   **Metadatos:** "Datos sobre los datos". Describen las propiedades, el formato, la estructura y el contexto de los datos almacenados.
*   **Redundancia de Datos:** Duplicación innecesaria de datos en diferentes lugares, lo que conduce a problemas de inconsistencia y malgasto de espacio.
*   **Repositorio:** Base de conocimientos centralizada que almacena metadatos y definiciones sobre la estructura de la base de datos.
*   **Seguridad de Datos:** Medidas de protección para evitar el acceso, modificación o eliminación no autorizada de los datos.
*   **Sistema de Información (SI):** Conjunto integrado de componentes (hardware, software, datos, personas, procesos) que gestionan información para apoyar a una organización.
*   **SQL (Structured Query Language):** Lenguaje estándar para comunicarse con bases de datos relacionales. Se divide en DDL (Lenguaje de Definición de Datos), DML (Lenguaje de Manipulación de Datos) y DCL (Lenguaje de Control de Datos).
*   **Transacción:** Una operación lógica completa de lectura o escritura sobre la base de datos.

---
