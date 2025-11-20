# Ejercicios Resueltos - Clase 12: Data Warehouse (Diseño Dimensional)

### Ejercicio 1: Diseño de un Esquema Estrella Simple

**Enunciado:**
Una cadena de supermercados desea analizar las ventas de sus productos. Necesitan poder analizar las ventas por fecha, por producto y por la tienda donde se realizó la venta.

**Requerimientos:**
*   **Medidas:** `Cantidad_Vendida`, `Precio_Venta_Unitario`, `Monto_Total_Venta`.
*   **Dimensiones:**
    *   **Tiempo:** Permite analizar ventas por día, mes, año.
    *   **Producto:** Incluye nombre del producto, categoría, marca.
    *   **Tienda:** Incluye nombre de la tienda, ciudad, región.

**Tarea:**
Diseña un esquema estrella (`CREATE TABLE` o descripción conceptual) identificando la tabla de hechos y sus tablas de dimensiones asociadas. Incluye al menos 3 atributos para cada dimensión.

---

**Solución (Conceptual con Atributos):**

**Tabla de Hechos: `FACT_VENTAS_SUPERMERCADO`**

*   `ID_Venta` (Clave Primaria de la transacción original, si se desea)
*   `ID_Fecha` (FK a DIM_TIEMPO)
*   `ID_Producto` (FK a DIM_PRODUCTO)
*   `ID_Tienda` (FK a DIM_TIENDA)
*   `Cantidad_Vendida` (Medida)
*   `Precio_Venta_Unitario` (Medida)
*   `Monto_Total_Venta` (Medida)

**Dimensiones:**

**`DIM_TIEMPO`**
*   `ID_Fecha` (PK)
*   `Fecha_Completa` (ej. '2023-10-27')
*   `Dia`
*   `Mes`
*   `Anio`

**`DIM_PRODUCTO`**
*   `ID_Producto` (PK)
*   `Nombre_Producto`
*   `Categoria_Producto`
*   `Marca_Producto`

**`DIM_TIENDA`**
*   `ID_Tienda` (PK)
*   `Nombre_Tienda`
*   `Ciudad_Tienda`
*   `Region_Tienda`

### Ejercicio 2: Identificación de Componentes en un Reporte

**Enunciado:**
Un analista de datos te pide un reporte que muestre el "Total de ventas por categoría de producto y por mes en el último año".

**Tarea:**
Identifica cuáles son las **Medidas**, las **Dimensiones** y los **Niveles** involucrados en este reporte, basándote en el diseño de un Data Warehouse.

---

**Solución:**

*   **Medidas:**
    *   "Total de ventas" (Esto sería una agregación de una medida como `Monto_Total_Venta` de una tabla de hechos).

*   **Dimensiones:**
    *   **Producto:** Se necesita para obtener la "categoría de producto".
    *   **Tiempo:** Se necesita para obtener el "mes" y el "último año".

*   **Niveles (dentro de sus respectivas dimensiones):**
    *   **Categoría de Producto:** Nivel dentro de la dimensión `DIM_PRODUCTO`.
    *   **Mes:** Nivel dentro de la dimensión `DIM_TIEMPO`.
    *   **Año:** Nivel dentro de la dimensión `DIM_TIEMPO`.

### Ejercicio 3: Ventajas y Desventajas de Modelos Estrella vs. Copo de Nieve

**Enunciado:**
Compara el Modelo Estrella (Star Schema) y el Modelo Copo de Nieve (Snowflake Schema) en términos de:
1.  Simplicidad de diseño y comprensión.
2.  Rendimiento de las consultas.
3.  Uso de espacio de almacenamiento.
4.  Flexibilidad y mantenibilidad.

---

**Solución:**

| Característica                 | Modelo Estrella (Star Schema)                                | Modelo Copo de Nieve (Snowflake Schema)                              |
| :----------------------------- | :----------------------------------------------------------- | :------------------------------------------------------------------- |
| **1. Simplicidad de Diseño**   | **Ventaja:** Muy simple, intuitivo y fácil de entender. La tabla de hechos se une directamente a las dimensiones. | **Desventaja:** Más complejo, ya que las dimensiones están normalizadas y pueden requerir múltiples JOINs para acceder a los atributos. |
| **2. Rendimiento de Consultas** | **Ventaja:** Excelente rendimiento para consultas analíticas. Menos JOINs (típicamente entre la tabla de hechos y cada dimensión) resultan en consultas más rápidas. | **Desventaja:** Menor rendimiento para algunas consultas analíticas debido al mayor número de JOINs necesarios para acceder a los atributos de las dimensiones normalizadas. |
| **3. Uso de Espacio**          | **Desventaja:** Mayor redundancia de datos en las dimensiones (atributos repetidos si una jerarquía está en una sola tabla de dimensión), lo que consume más espacio. | **Ventaja:** Menor redundancia de datos en las dimensiones (están normalizadas), lo que ahorra espacio de almacenamiento. |
| **4. Flexibilidad/Mantenibilidad** | **Ventaja:** Fácil de añadir nuevas medidas o dimensiones. La estructura es robusta y los cambios suelen ser localizados. | **Ventaja:** Mayor flexibilidad para añadir nuevos atributos o niveles a las dimensiones, ya que la normalización permite cambios más localizados. |
