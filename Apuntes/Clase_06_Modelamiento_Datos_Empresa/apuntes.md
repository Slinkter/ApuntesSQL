# 🧹 Clase 06: Normalización (1FN, 2FN, 3FN)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **¿Qué es Normalización?** | Es el proceso de **limpieza y mejora del diseño lógico** para evitar la duplicación innecesaria de datos (redundancia) y asegurar que las relaciones estén "bien estructuradas". |
| **Anomalías (¡Los Problemas a Evitar!)** | Queremos evitar problemas al manipular datos: **Anomalía de Inserción** (no puedes registrar un dato sin duplicar o inventar otros). **Anomalía de Eliminación** (borras un registro y pierdes datos importantes asociados). **Anomalía de Modificación** (tienes que cambiar el mismo dato en varios lugares). |
| **Dependencia Funcional** | Si el valor del atributo A determina el valor del atributo B, decimos que B es funcionalmente dependiente de A (A  B). |
| **1FN (Primera Forma Normal)** | **¡Todo debe ser Atómico!** Elimina los grupos repetitivos. Cada atributo debe tener un valor indivisible. Por ejemplo, si tienes "Lunes, Miércoles, Viernes" en una celda, debes separar cada día en su propia fila. |
| **2FN (Segunda Forma Normal)** | **¡Dependencia Total de la Clave!** Si tienes una Clave Primaria Compuesta, cada atributo no clave debe depender de *toda* la clave, no solo de una parte (dependencia funcional parcial). Si un atributo depende solo de un pedacito de la clave, ¡sácalo y ponlo en su propia tabla!. |
| **3FN (Tercera Forma Normal)** | **¡No a la Transitividad!** Elimina las **Dependencias Transitivas**. Esto pasa cuando un atributo no clave determina a otro atributo no clave (B  C). Por ejemplo, si el RUC determina el Nombre, y el Nombre determina la Dirección. Debes separarlo para que cada tabla se enfoque en un solo tema. |

**Resumen de la Clase 06:** La normalización es esencial para combatir la redundancia y evitar anomalías (inserción, eliminación, modificación). Seguimos un proceso de descomposición gradual: 1FN (atomicidad y grupos repetitivos), 2FN (dependencia total de la clave primaria) y 3FN (eliminar dependencias transitivas).

---
