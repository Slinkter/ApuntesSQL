# ⚡ Clase 09: Otras Formas Normales y Desnormalización

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **FNBC (Forma Normal Boyce-Codd)** | Es una versión más estricta de la 3FN. Una relación está en FNBC si **cada atributo determinante (A) es también una clave candidata**. Esto ayuda a resolver casos donde la 3FN aún permite dependencias problemáticas que involucran atributos que *podrían* ser claves. |
| **4FN (Cuarta Forma Normal)** | Se aplica si ya estás en FNBC y no tienes **Dependencias Multivaluadas**. Esto pasa si tienes tres atributos (A, B, C) donde A determina un conjunto de valores para B y un conjunto de valores para C, pero ¡B y C son totalmente independientes!. La solución es separarlos en relaciones binarias (Ej. Curso-Profesor y Curso-Texto). |
| **Desnormalización** | Es el **proceso contrario a la normalización**. Se hace para **crear redundancia intencional** con un objetivo muy específico: **mejorar los tiempos de respuesta** (velocidad) del sistema. |
| **Riesgos de Desnormalizar** | Aunque da velocidad, tiene desventajas: **reduce la integridad** y hace el modelo **menos flexible**. Hay que compensar la integridad con código de programación adicional. |
| **Técnicas Comunes de Desnormalización** | Incluyen: **Unir Entidades** (meter detalles en el maestro para evitar un *join*), **Grabar valores derivados** (guardar un Total en la tabla sin calcularlo cada vez), o usar **Valores Fijos** (sustituir una tabla de referencia pequeña por un campo con código 'M'/'F'). |

**Resumen de la Clase 09:** Después de la 3FN, exploramos la FNBC (determinantes son claves candidatas) y la 4FN (eliminación de dependencias multivaluadas). Finalmente, aprendimos que la **Desnormalización** es una técnica estratégica para introducir redundancia y ganar velocidad, aunque requiere programación adicional para mantener la integridad.

---