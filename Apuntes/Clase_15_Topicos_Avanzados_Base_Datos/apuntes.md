# 📊 Clase 15: Data Warehouse (Arquitectura y Explotación)

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **DW vs. Sistemas Operacionales (OLTP)** | Los **Sistemas Operacionales** (OLTP) ejecutan el negocio (transacciones rápidas, datos actuales, empleados por oficinistas). El **DW** (Sistemas Analíticos) administra el negocio (análisis histórico, integración, usado por *decision makers*). |
| **Definición de Data Warehouse** | Un DW es **Organizado por Temas** (información relacionada), **Variante en el Tiempo** (histórico y auditable), **No Volátil** (permanente) e **Integrado** (consistente). |
| **Data Mart** | Es una versión más pequeña y especializada del DW, diseñada para un grupo o departamento específico (Ej. Ventas o Finanzas), mejorando el acceso y el análisis para ese grupo. |
| **ETL (Extracción, Transformación y Carga)** | Este es el proceso más costoso y largo (¡el **80% de los recursos!**). Implica tomar datos de las fuentes, **transformarlos** (limpiar, integrar, derivar) y **cargarlos** en el DW. |
| **Metadatos y Cubos** | Los **Metadatos** son la clave para entender el contexto de la data. La información se representa en **Cubos de Datos** multidimensionales, que tienen Dimensiones (Ej. Año, País, Color) y Hechos (Medidas de interés). |
| **Explotación de Datos** | ¿Cómo usamos toda esta información? **Query Ad hoc** (consultas puntuales). **OLAP** (Online Analytical Processing): Análisis multidimensional avanzado sobre los cubos (Ej. rodar, picar y rebanar el cubo). **Data Mining** (Minería de Datos): Herramientas que buscan automáticamente **patrones y tendencias**. |
| **Tipos de Data Mining** | **Minería de Descubrimiento** (encontrar patrones en todo el almacén, a veces los más valiosos). **Minería Predictiva** (usar datos conocidos para crear modelos que predicen valores futuros). |

**Resumen de la Clase 15:** Un DW es un sistema analítico integrado, no volátil e histórico, que se diferencia del OLTP. Vimos que el proceso ETL consume la mayor parte del esfuerzo. Finalmente, el análisis de datos se realiza mediante OLAP (consultas multidimensionales) y Data Mining (que descubre patrones y ayuda a la predicción).

---