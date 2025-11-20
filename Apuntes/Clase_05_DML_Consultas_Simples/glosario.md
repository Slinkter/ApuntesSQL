# Glosario - Clase 05: Modelamiento de Datos en la Empresa

*   **Abstracción (Modelado de Datos):** Proceso de simplificar la realidad para representar solo los detalles relevantes en un modelo de datos.
*   **Cardinalidad (Modelo E-R):** En el Modelo Entidad-Relación, especifica el número de instancias de una entidad que pueden asociarse con el número de instancias de otra entidad. Se expresa como mínima y máxima (ej. (0,1) Cero o una; (1,N) Una o muchas).
*   **Cardinalidad Máxima:** El número máximo de ocurrencias de una entidad que puede estar relacionada con una ocurrencia de otra entidad.
*   **Cardinalidad Mínima:** El número mínimo de ocurrencias de una entidad que *debe* estar relacionada con una ocurrencia de otra entidad. Si es cero, la participación es opcional; si es uno, es mandatoria.
*   **Clave Foránea (FK):** Atributo en una entidad que es la clave primaria de otra entidad, utilizada para establecer una relación entre ambas.
*   **Clave Primaria (PK):** Atributo o conjunto de atributos que identifica de forma única cada instancia de una entidad.
*   **Entidad:** En el Modelo Entidad-Relación, representa una "cosa" o "concepto" del mundo real sobre el cual se desea almacenar información (ej. Empleado, Producto, Pedido).
*   **Entidad Asociativa:** Un tipo de entidad que surge de la relación entre dos o más entidades, y a menudo contiene atributos propios de la relación. A veces se le llama "entidad de relación" o "intersección".
*   **Entidad Débil:** Una entidad que no puede existir de forma independiente; su existencia depende de otra entidad (la entidad fuerte). No tiene una clave primaria propia y su clave depende, en parte, de la clave de la entidad fuerte.
*   **Entidad Fuerte:** Una entidad que puede existir de forma independiente, es decir, tiene su propia clave primaria única.
*   **Modelamiento de Datos:** El proceso de crear una representación abstracta de la estructura de datos que necesita una base de datos. Es la parte más importante del desarrollo de un sistema.
*   **Modelo de Datos:** Una colección de conceptos que pueden ser usados para describir la estructura de una base de datos.
*   **Modelo Entidad-Relación (E-R):** Herramienta conceptual de diseño de bases de datos que representa las entidades (objetos o conceptos) y las relaciones entre ellas.
*   **Relación (Modelo E-R):** Una asociación entre dos o más entidades. Describe cómo las instancias de una entidad se conectan con las instancias de otra.
*   **Reglas de Negocio:** Enunciados explícitos que definen o restringen algún aspecto de la operación de una empresa. Son cruciales para determinar la estructura y las restricciones del modelo de datos.
*   **Sistema Orientado a Datos:** Un sistema cuyo diseño y desarrollo priorizan la estructura y estabilidad de los datos, dado que los datos suelen ser más estables que los procesos de negocio.