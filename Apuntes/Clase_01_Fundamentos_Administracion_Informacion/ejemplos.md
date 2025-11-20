# Ejemplos - Clase 01: Fundamentos de Administración de Información

### Ejemplo 1: Diferencia entre Dato, Información y Conocimiento

Este ejemplo, extraído de las diapositivas de la clase, ilustra cómo los conceptos se conectan en un escenario de negocio.

#### 1.1. Dato

Un **dato** es un valor crudo, sin contexto. Por sí mismo, no nos dice mucho.

| Campo  | Valor |
| :----- | :---- |
| Precio | 3.50  |

Esto es solo un número. No sabemos qué producto es, en qué moneda está o si es un precio de compra o de venta.

Para que tenga más significado, un dato debe formar parte de una estructura.

| Código | Nombre        | Tipo | Precio | Sabor   |
| :----- | :------------ | :--- | :----- | :------ |
| 001    | Cola manzana  | Cola | 3.50   | Manzana |

Ahora tenemos datos estructurados, pero siguen siendo solo eso: datos.

#### 1.2. Información

La **información** se genera al procesar los datos para revelar patrones o tendencias. Reduce la incertidumbre.

**Reporte de Evolución de Precios: Cola Manzana**

| Año  | Precio |
| :--- | :----- |
| 2000 | 2.0    |
| 2001 | 2.7    |
| 2002 | 2.9    |
| 2003 | 3.5    |

Este reporte nos informa que el precio de la "Cola Manzana" ha estado subiendo consistentemente a lo largo de los años. Esto es mucho más útil que el simple dato "3.50".

#### 1.3. Conocimiento

El **conocimiento** se deriva de analizar la información, a menudo combinando diferentes conjuntos de datos, para tomar una decisión informada.

**Reporte Cruzado de Ventas vs. Precios**

| Año  | Nombre Cola   | Precio | Venta      |
| :--- | :------------ | :----- | :--------- |
| 2000 | Cola frutilla | 2.5    | 2,000,000  |
| 2001 | Cola frutilla | 2.5    | 1,800,000  |
| 2000 | Cola manzana  | 2.0    | 2,000,000  |
| 2001 | Cola manzana  | 2.7    | 2,400,000  |

**Análisis y Decisión (Conocimiento):**
> "Observamos que la venta de 'Cola frutilla' ha disminuido a pesar de mantener su precio. Por otro lado, 'Cola manzana', a pesar de haber subido de precio, aumentó sus ventas. **Conclusión:** Debemos darle un mayor impulso de marketing a la 'Cola manzana' y quizás revisar la estrategia de 'Cola frutilla'."

### Ejemplo 2: Metadatos

Los **metadatos** son "datos sobre los datos". Describen la estructura, las reglas y el contexto de los datos de la aplicación.

Tomando el ejemplo de una lista de estudiantes de un curso:

**Tabla de Datos: `ClassRoster`**

| Course               | Section | Semester     | Name             | ID    | Major | GPA |
| :------------------- | :------ | :----------- | :--------------- | :---- | :---- | :-- |
| MGT 500 Business Pol | 2       | Spring 200X  | Baker, Kenneth D | 32491 | MGT   | 3.2 |
| ...                  | ...     | ...          | ...              | ...   | ...   | ... |

**Tabla de Metadatos para `ClassRoster`**

| Data Item | Type         | Length | Min | Max | Description                 |
| :-------- | :----------- | :----- | :-- | :-- | :-------------------------- |
| Course    | Alphanumeric | 30     |     |     | Course ID and name          |
| Section   | Integer      | 1      | 1   | 9   | Section number              |
| Semester  | Alphanumeric | 10     |     |     | Semester and year           |
| Name      | Alphanumeric | 30     |     |     | Student name                |
| ID        | Integer      | 9      |     |     | Student ID (SSN)            |
| Major     | Alphanumeric | 4      |     |     | Student major               |
| GPA       | Decimal      | 3      | 0.0 | 4.0 | Student grade point average |

Esta tabla de metadatos es fundamental para que el DBMS sepa cómo almacenar y validar los datos, y para que los desarrolladores sepan cómo interactuar con ellos.
