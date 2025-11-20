# Ejemplos - Clase 12: Data Warehouse (Diseño Dimensional)

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