#  Clase 12: Data Warehouse (Diseño Dimensional)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Business Intelligence (BI)** | BI es el conjunto de productos que ayuda a los usuarios a acceder y analizar rápidamente la información para la **toma de decisiones estratégicas**. |
| **Data Warehouse (DW)** | Es un **repositorio centralizado** de datos, optimizado para el análisis (no para transacciones diarias). La información se guarda en estructuras llamadas **Cubos**. |
| **Tablas de Hechos (Fact Table)** | Estas son las tablas centrales. Almacenan los **eventos** (los Hechos, Ej. una venta) y contienen las **Medidas** (los valores cuantitativos que analizamos, Ej. monto de la venta, cantidad). |
| **Dimensiones (El Contexto)** | Una **Dimensión** es una entidad de negocio que usamos para **cruzar o categorizar** las medidas. La medida "Ventas" solo tiene sentido si la vemos por una dimensión: ¿Ventas *por* Cliente? ¿Ventas *por* Producto?. |
| **Niveles y Miembros** | Una Dimensión puede tener múltiples **Niveles** de agrupación (Ej. la dimensión "Tiempo" tiene Año, Mes, Día). Las ocurrencias en cada nivel se llaman **Miembros** (Ej. "Lima" es un miembro del nivel Departamento). |
| **Modelo Estrella (STAR)** | ¡El diseño más simple y rápido! La Fact Table se conecta directamente a **cada tabla de dimensión**. Es fácil de entender y tiene baja complejidad de consulta. |
| **Modelo Copo de Nieve (SNOWFLAKE)** | Más complejo. En lugar de una sola tabla de dimensión, cada nivel de la dimensión se separa en su propia tabla. Esto genera más tablas, mayor complejidad de consulta y rendimiento más lento. |

**Resumen de la Clase 12:** El DW facilita el BI, almacenando datos en Cubos multidimensionales. El diseño se centra en dos tipos de tablas: las Tablas de Hechos (con las Medidas) y las Tablas de Dimensión (que dan contexto). Los dos modelos principales son el eficiente Modelo Estrella y el más complejo Copo de Nieve.

---