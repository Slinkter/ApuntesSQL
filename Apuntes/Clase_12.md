# Clase 12: Data Warehouse (Diseño Dimensional)

---

## 📚 Conceptos Clave

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

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Esquema Estrella (Star Schema) para Ventas

Imaginemos un Data Warehouse para analizar las ventas de una empresa. Un esquema estrella es el diseño más común y efectivo.

**Tabla de Hechos Central: `FACT_VENTAS`**
*   Esta tabla contiene los eventos de venta y las medidas de interés.
*   **Claves Foráneas (FK) a Dimensiones:**
    *   `ID_Fecha` (FK a DIM_TIEMPO)
    *   `ID_Producto` (FK a DIM_PRODUCTO)
    *   `ID_Cliente` (FK a DIM_CLIENTE)
    *   `ID_Sucursal` (FK a DIM_SUCURSAL)
*   **Medidas (Hechos Cuantitativos):**
    *   `Cantidad_Vendida`
    *   `Monto_Venta`
    *   `Costo_Producto`
    *   `Beneficio` (calculado)

**Tablas de Dimensión (proporcionan contexto a las ventas):**

**`DIM_TIEMPO`**
*   `ID_Fecha` (PK)
*   `Dia`
*   `Mes`
*   `Anio`
*   `Numero_Semana`
*   `Dia_Semana`
*   `Festivo` (Sí/No)

**`DIM_PRODUCTO`**
*   `ID_Producto` (PK)
*   `Nombre_Producto`
*   `Marca`
*   `Categoria`
*   `Subcategoria`

**`DIM_CLIENTE`**
*   `ID_Cliente` (PK)
*   `Nombre_Cliente`
*   `Segmento`
*   `Edad`
*   `Genero`
*   `Ciudad`
*   `Pais`

**`DIM_SUCURSAL`**
*   `ID_Sucursal` (PK)
*   `Nombre_Sucursal`
*   `Region`
*   `Tipo_Sucursal` (Online/Física)

**Representación Visual (Conceptual):**

```
                  DIM_TIEMPO
                      |
                      |
DIM_PRODUCTO --- FACT_VENTAS --- DIM_CLIENTE
                      |
                      |
                  DIM_SUCURSAL
```
En este esquema, `FACT_VENTAS` está en el centro, conectada directamente con cada tabla de dimensión. Cada tabla de dimensión es relativamente pequeña y no está relacionada con otras tablas de dimensión, simplificando las consultas.

### Ejemplo 2: Niveles y Miembros de una Dimensión

Tomando la `DIM_TIEMPO` del ejemplo anterior, podemos ver sus niveles y miembros:

*   **Nivel: `Año`**
    *   Miembros: "2022", "2023", "2024"
*   **Nivel: `Trimestre`**
    *   Miembros: "Q1", "Q2", "Q3", "Q4"
*   **Nivel: `Mes`**
    *   Miembros: "Enero", "Febrero", ..., "Diciembre"
*   **Nivel: `Día`**
    *   Miembros: "01", "02", ..., "31"

Estos niveles permiten a los analistas ver las ventas por año, por trimestre, por mes o por día, simplemente agregando o desagregando los datos.

### Ejemplo 3: Modelo Copo de Nieve (Snowflake Schema) para Productos

Si en la `DIM_PRODUCTO` (Ejemplo 1) quisiéramos normalizar la categoría y subcategoría para evitar redundancia (porque muchos productos pueden tener la misma categoría y subcategoría), podríamos usar un esquema copo de nieve.

**Tabla de Hechos Central: `FACT_VENTAS`** (igual que en el Ejemplo 1)

**Tablas de Dimensión:**

**`DIM_TIEMPO`**, **`DIM_CLIENTE`**, **`DIM_SUCURSAL`** (igual que en el Ejemplo 1)

**`DIM_PRODUCTO` (ahora con detalle normalizado)**
*   `ID_Producto` (PK)
*   `Nombre_Producto`
*   `Marca`
*   `ID_Subcategoria` (FK a DIM_SUBCATEGORIA)

**`DIM_SUBCATEGORIA` (Nueva tabla)**
*   `ID_Subcategoria` (PK)
*   `Nombre_Subcategoria`
*   `ID_Categoria` (FK a DIM_CATEGORIA)

**`DIM_CATEGORIA` (Nueva tabla)**
*   `ID_Categoria` (PK)
*   `Nombre_Categoria`

**Representación Visual (Conceptual):**

```
                  DIM_TIEMPO
                      |
                      |
DIM_SUBCATEGORIA --- FACT_VENTAS --- DIM_CLIENTE
        |                 |
        |                 |
DIM_CATEGORIA         DIM_SUCURSAL
```
En este caso, `DIM_PRODUCTO` ya no está directamente unida a `FACT_VENTAS` de forma completa para su categoría y subcategoría, sino que se "ramifica" en tablas adicionales. Esto reduce la redundancia de datos pero introduce más `JOIN`s para las consultas que necesiten la categoría, lo que podría afectar el rendimiento.

---

## ✏️ Ejercicios Resueltos

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

---

