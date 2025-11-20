# Glosario - Clase 03: Bases de Datos Relacionales

*   **Modelo Relacional:** Un modelo de datos para organizar bases de datos basado en el concepto de relaciones (tablas), donde los datos se almacenan en tablas con filas y columnas.
*   **Relación (Tabla):** Una estructura bidimensional en el modelo relacional, compuesta por filas y columnas, que representa un conjunto de entidades interrelacionadas.
*   **Atributo (Columna/Campo):** Una característica o propiedad que describe la entidad representada por una tabla, y que tiene un nombre único dentro de esa tabla.
*   **Tupla (Fila/Registro):** Una instancia individual de una entidad en una relación, que contiene un conjunto de valores para cada uno de los atributos de la tabla.
*   **Dominio (Relacional):** El conjunto de todos los valores posibles y permitidos para un atributo específico.
*   **Grado (Relacional):** El número de atributos (columnas) que contiene una relación (tabla).
*   **Cardinalidad (Relacional):** El número de tuplas (filas) que contiene una relación (tabla).
*   **Superclave:** Un atributo o conjunto de atributos que, tomados colectivamente, permiten identificar de forma única una tupla dentro de una relación.
*   **Clave Candidata:** Una superclave mínima, es decir, de la que no se puede eliminar ningún atributo sin perder la propiedad de unicidad. Una relación puede tener varias claves candidatas.
*   **Clave Primaria (PK):** Una de las claves candidatas elegida por el diseñador de la base de datos para identificar de forma única cada tupla en una tabla. Sus valores deben ser únicos y no nulos.
*   **Clave Foránea (FK):** Un atributo o conjunto de atributos en una tabla (tabla hija) que hace referencia a la clave primaria de otra tabla (tabla padre), estableciendo una relación entre ellas y manteniendo la integridad referencial.
*   **Integridad Referencial:** Un conjunto de reglas que asegura la validez de las relaciones entre tablas y previene la eliminación o modificación accidental de datos relacionados.
*   **Álgebra Relacional:** Un lenguaje procedimental de consulta de bases de datos que utiliza un conjunto de operadores para manipular relaciones y producir nuevas relaciones como resultado.
*   **Selección (σ):** Operador del álgebra relacional que filtra las filas de una relación basándose en una condición lógica.
*   **Proyección (π):** Operador del álgebra relacional que selecciona un subconjunto de columnas de una relación, eliminando las columnas duplicadas.
*   **Unión (∪):** Operador del álgebra relacional que combina las tuplas de dos relaciones con esquemas compatibles, eliminando duplicados.
*   **Intersección (∩):** Operador del álgebra relacional que devuelve las tuplas que son comunes a dos relaciones con esquemas compatibles.
*   **Diferencia (-):** Operador del álgebra relacional que devuelve las tuplas presentes en una relación pero no en otra, asumiendo esquemas compatibles.
*   **Producto Cartesiano (×):** Operador del álgebra relacional que combina cada tupla de una relación con cada tupla de otra relación, formando todas las combinaciones posibles.
*   **Join (⋈):** Operador del álgebra relacional que combina tuplas de dos relaciones basándose en una condición de igualdad entre los valores de sus atributos comunes, creando una nueva relación.
