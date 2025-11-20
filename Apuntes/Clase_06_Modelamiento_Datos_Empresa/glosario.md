# Glosario - Clase 06: Normalización (1FN, 2FN, 3FN)

*   **1FN (Primera Forma Normal):** Estado de una relación donde todos los atributos son atómicos (indivisibles) y no existen grupos repetitivos.
*   **2FN (Segunda Forma Normal):** Estado de una relación que ya está en 1FN y donde todos los atributos no clave dependen funcionalmente de la clave primaria *completa*, no solo de una parte de ella (elimina dependencias funcionales parciales).
*   **3FN (Tercera Forma Normal):** Estado de una relación que ya está en 2FN y donde no existen dependencias transitivas de atributos no clave (un atributo no clave no determina a otro atributo no clave).
*   **Anomalía de Eliminación:** Problema que ocurre cuando al borrar una tupla, se pierden inadvertidamente otros datos importantes que no están directamente relacionados con la clave primaria de la tupla eliminada.
*   **Anomalía de Inserción:** Problema que ocurre cuando no se puede insertar una tupla en una relación porque se requieren datos de otros atributos que aún no están disponibles o no son relevantes para la tupla a insertar.
*   **Anomalía de Modificación:** Problema que ocurre cuando la modificación de un atributo en una tupla requiere la modificación del mismo atributo en múltiples tuplas para mantener la consistencia, lo que aumenta el riesgo de errores.
*   **Atómico (Atributo):** Un atributo se considera atómico si no puede ser dividido en componentes más pequeños con significado propio (ej. un número telefónico es atómico, una lista de habilidades en un solo campo no lo es).
*   **Dependencia Funcional (A  B):** Una relación entre atributos donde el valor de un atributo (o conjunto de atributos) `A` determina de forma única el valor de otro atributo (o conjunto de atributos) `B`. Se lee "A determina B".
*   **Dependencia Funcional Parcial:** Ocurre cuando un atributo no clave depende funcionalmente solo de una *parte* de la clave primaria compuesta, en lugar de la clave primaria completa.
*   **Dependencia Transactiva:** Ocurre cuando un atributo no clave determina a otro atributo no clave (A → B y B → C, donde C es un atributo no clave).
*   **Diseño Lógico (Normalización):** El proceso de refinar la estructura de la base de datos para asegurar su eficiencia, integridad y consistencia, a menudo a través de la normalización.
*   **Normalización:** Proceso sistemático de analizar las dependencias funcionales de una relación y descomponerla en relaciones más pequeñas y "bien estructuradas" para reducir la redundancia de datos y prevenir anomalías.
*   **Redundancia de Datos:** La duplicación innecesaria de la misma información en múltiples lugares de la base de datos.