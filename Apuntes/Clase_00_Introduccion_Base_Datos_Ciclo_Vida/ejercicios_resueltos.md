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
