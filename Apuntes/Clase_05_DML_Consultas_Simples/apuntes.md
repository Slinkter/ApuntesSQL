# 🗺️ Clase 05: Modelamiento de Datos en la Empresa

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Importancia del Modelamiento** | Los expertos dicen que el modelamiento es la **parte más importante** del desarrollo de un sistema. ¿Por qué? Porque los datos suelen ser más estables que los procesos de negocio, ¡así que un sistema orientado a datos dura más!. |
| **Modelo de Datos y Reglas de Negocio** | Un Modelo de Datos es una abstracción del mundo real que representa cómo se organiza la información. Expresa las **Reglas de Negocio**, que son enunciados que definen o limitan algún aspecto de la empresa (Ej. "Un cliente solo puede comprar 10 productos al día"). |
| **Modelo Entidad-Relación (E-R)** | Es la herramienta conceptual que usamos para diseñar la BD. Muestra: **Entidades** (cosas de interés, Ej. Empleado) y sus **Relaciones** (asociaciones, Ej. Empleado *trabaja en* Departamento). |
| **Tipos de Entidad** | Una **Entidad Fuerte** existe por sí misma (Ej. Factura). Una **Entidad Débil** depende de otra para existir (Ej. Línea de Factura). Una **Entidad Asociativa** nace de la relación entre otras dos (¡como un "hijo" de la relación!). |
| **Cardinalidad** | Nos dice cuántas instancias de una entidad pueden asociarse con otra. Puede ser 1-a-1, 1-a-N, o N-a-N. La **Cardinalidad Mínima** es clave: si es cero (0), la relación es **opcional**; si es uno (1), es **mandatoria**. |
| **Claves (PK/FK)** | El modelo E-R también define las claves. La **Clave Primaria (PK)** identifica de forma única y la **Clave Foránea (FK)** es la que se usa para implementar la asociación entre las tablas relacionales. |

**Resumen de la Clase 05:** El modelamiento de datos es fundamental, ya que captura las reglas de negocio en una abstracción del mundo real. El Modelo Entidad-Relación usa entidades (Fuertes/Débiles/Asociativas) y relaciones, definiendo la cardinalidad (1-N, N-N) para establecer cómo se conecta la información.

---
