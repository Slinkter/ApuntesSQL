# Ejemplos - Clase 05: Modelamiento de Datos en la Empresa

### Ejemplo 1: Identificación de Entidades y Atributos

Imagina un sistema para una universidad. Podemos identificar las siguientes entidades principales y algunos de sus atributos:

*   **Entidad: `ESTUDIANTE`**
    *   `ID_Estudiante` (PK)
    *   `Nombre`
    *   `Apellido`
    *   `Fecha_Nacimiento`
    *   `Email`
*   **Entidad: `CURSO`**
    *   `ID_Curso` (PK)
    *   `Nombre_Curso`
    *   `Creditos`
    *   `ID_Departamento`
*   **Entidad: `PROFESOR`**
    *   `ID_Profesor` (PK)
    *   `Nombre`
    *   `Apellido`
    *   `Departamento`
    *   `Titulo_Academico`

### Ejemplo 2: Tipos de Entidades (Fuerte y Débil)

Considera un sistema de gestión de pedidos:

*   **Entidad Fuerte: `PEDIDO`**
    *   `ID_Pedido` (PK)
    *   `Fecha_Pedido`
    *   `ID_Cliente` (FK)
    *   Un `PEDIDO` puede existir por sí mismo, incluso si aún no tiene productos asociados.

*   **Entidad Débil: `DETALLE_PEDIDO` (o Ítem de Línea de Pedido)**
    *   `ID_Pedido` (parte de la clave, FK)
    *   `Numero_Linea` (identificador dentro del pedido)
    *   `ID_Producto` (FK)
    *   `Cantidad`
    *   Un `DETALLE_PEDIDO` no puede existir sin un `PEDIDO` al que pertenezca. Su existencia depende directamente de la entidad `PEDIDO`.

### Ejemplo 3: Relaciones y Cardinalidades

Usando las entidades del Ejemplo 1, podemos definir relaciones y sus cardinalidades:

#### Relación entre `ESTUDIANTE` y `CURSO`: "Inscripción"

*   Un `ESTUDIANTE` se inscribe en muchos `CURSOS`.
*   Un `CURSO` tiene muchos `ESTUDIANTES` inscritos.
*   Esto es una relación de Muchos a Muchos (N:M).
*   **Cardinalidad:**
    *   (1,N) de `ESTUDIANTE` a `CURSO` (Un estudiante se inscribe en al menos 1 curso, o en muchos)
    *   (0,N) de `CURSO` a `ESTUDIANTE` (Un curso puede no tener estudiantes inscritos (0) o tener muchos (N))

**Representación en un Modelo E-R (Texto):**
`ESTUDIANTE` (1,N) ---- `SE_INSCRIBE_EN` ---- (0,N) `CURSO`

#### Relación entre `PROFESOR` y `CURSO`: "Imparte"

*   Un `PROFESOR` puede impartir varios `CURSOS`.
*   Un `CURSO` es impartido por un único `PROFESOR`.
*   Esto es una relación de Uno a Muchos (1:N).
*   **Cardinalidad:**
    *   (0,N) de `PROFESOR` a `CURSO` (Un profesor puede no impartir ningún curso (0) o impartir muchos (N))
    *   (1,1) de `CURSO` a `PROFESOR` (Un curso debe ser impartido por exactamente 1 profesor)

**Representación en un Modelo E-R (Texto):**
`PROFESOR` (0,N) ---- `IMPARTE` ---- (1,1) `CURSO`

### Ejemplo 4: Entidad Asociativa

Cuando tenemos una relación de Muchos a Muchos, a menudo se resuelve creando una entidad asociativa.

Consideremos la relación "Inscripción" entre `ESTUDIANTE` y `CURSO`. Un estudiante se inscribe en un curso, y en esa inscripción se genera una `Fecha_Inscripcion` y una `Calificacion`. Estos atributos no pertenecen ni solo al estudiante ni solo al curso, sino a la *inscripción misma*.

*   **Entidad Asociativa: `INSCRIPCION`**
    *   `ID_Estudiante` (parte de la PK, FK)
    *   `ID_Curso` (parte de la PK, FK)
    *   `Fecha_Inscripcion`
    *   `Calificacion`
    *   Esta entidad `INSCRIPCION` asocia a un `ESTUDIANTE` con un `CURSO` y almacena atributos específicos de esa asociación.