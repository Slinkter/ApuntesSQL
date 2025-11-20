# Glosario - Clase 07: Modelamiento de Datos en la Empresa: Normalización (Parte I)

*   **Normalización:** Proceso de organizar los campos y tablas de una base de datos relacional para minimizar la redundancia de datos y mejorar la integridad de los datos.
*   **Bases de Datos Relacionales (BD):** Modelo de base de datos que organiza los datos en una o más tablas (o "relaciones") de filas y columnas, con un identificador único para cada fila.
*   **Redundancia de datos:** Ocurrencia de la misma información en múltiples lugares dentro de una base de datos. Es un objetivo clave de la normalización eliminarla.
*   **Inconsistencia de dependencia:** Situación donde los datos duplicados no se actualizan de manera uniforme, lo que lleva a diferentes versiones de la misma información.
*   **Formalización Cero:** Estado de una base de datos donde no se ha aplicado ninguna regla de normalización, resultando en redundancia y posibles inconsistencias.
*   **Primera Forma Normal (1FN):** Una relación está en 1FN si contiene solo valores atómicos, y no existen grupos repetitivos de columnas. Cada celda debe tener un único valor.
*   **Clave Primaria:** Un atributo o conjunto de atributos que identifica de forma única cada fila en una tabla. No puede contener valores nulos.
*   **Clave Externa (Foreign Key):** Un campo (o colección de campos) en una tabla que se refiere a la Clave Primaria de otra tabla. Establece una relación entre las dos tablas.
*   **Segunda Forma Normal (2FN):** Una relación está en 2FN si está en 1FN y todos sus atributos no clave dependen completamente de la clave primaria. Se aplica principalmente a claves primarias compuestas.
*   **Dependencia Parcial:** Ocurre cuando un atributo no clave depende de solo una parte de una clave primaria compuesta.
*   **Tercera Forma Normal (3FN):** Una relación está en 3FN si está en 2FN y no existen dependencias transitivas entre atributos no clave.
*   **Dependencia Transitiva:** Ocurre cuando un atributo no clave depende de otro atributo no clave, en lugar de depender directamente de la clave primaria.
