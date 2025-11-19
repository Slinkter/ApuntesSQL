# Glosario - Clase 09: Modelamiento de Datos en la Empresa: Normalización (Parte II)

*   **Relación Uno a Uno (1:1):** Tipo de relación entre tablas donde un registro de una tabla se asocia con un único registro de otra tabla.
*   **Relación Uno a Muchos (1:N):** Tipo de relación donde un registro de una tabla puede estar asociado con uno o varios registros de otra tabla, pero un registro de la segunda tabla solo puede asociarse con un registro de la primera.
*   **Relación Muchos a Muchos (N:M):** Tipo de relación donde un registro de una tabla puede asociarse con varios registros de otra tabla, y viceversa. Requiere una tabla intermedia para su implementación.
*   **Tabla Intermedia (Tabla de Enlace/Asociación):** Tabla utilizada para resolver relaciones de Muchos a Muchos, conteniendo claves foráneas de las dos tablas relacionadas.
*   **Cuarta Forma Normal (4FN):** Una relación está en 4FN si está en 3FN y no contiene dependencias multivaluadas no triviales.
*   **Dependencia Multivaluada:** Ocurre cuando un determinante (un atributo o conjunto de atributos) tiene múltiples valores asociados que son independientes entre sí.
*   **Determinante:** Cualquier atributo o conjunto de atributos que determina el valor de otro atributo. En normalización, se refiere a la parte de una relación de la que dependen otros atributos.
*   **Quinta Forma Normal (5FN) / Proyección-Unión Normal Form (PJ/NF):** Una relación está en 5FN si está en 4FN y no contiene dependencias de unión no triviales. No puede descomponerse en tablas más pequeñas sin pérdida de información.
*   **Dependencia de Unión:** Una propiedad de una tabla que permite que se reconstruya a partir de la unión de dos o más de sus proyecciones.
*   **Desnormalización:** Proceso de introducir intencionadamente redundancia en una base de datos para mejorar el rendimiento de la lectura o la simplicidad de las consultas, a menudo a expensas de la integridad de los datos en escenarios de escritura.
