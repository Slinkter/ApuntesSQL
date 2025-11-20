# Ejemplos - Clase 02: Modelo Relacional

### Ejemplo 1: Terminología del Modelo Relacional

Consideremos una tabla `CLIENTES` en una base de datos relacional.

**Tabla CLIENTES (Relación)**

| ID_Cliente (PK) | Nombre    | Apellido  | Email                   | ID_Representante (FK) |
| :-------------- | :-------- | :-------- | :---------------------- | :-------------------- |
| 101             | Juan      | Pérez     | juan.perez@email.com    | 1                     |
| 102             | María     | García    | maria.garcia@email.com  | 2                     |
| 103             | Carlos    | López     | carlos.lopez@email.com  | 1                     |

*   **Relación:** Toda la tabla `CLIENTES` es una relación.
*   **Tupla:** Cada fila de la tabla es una tupla (Ej., la fila que contiene los datos de Juan Pérez es una tupla).
*   **Atributo:** Cada columna es un atributo (Ej., `Nombre`, `Apellido`, `Email` son atributos).
*   **Primary Key (PK):** `ID_Cliente` es la clave primaria. Identifica de forma única a cada cliente. Cada valor es distinto y no puede ser nulo.
*   **Foreign Key (FK):** `ID_Representante` es una clave foránea. Establece una relación con la clave primaria de una tabla `REPRESENTANTES` (que no se muestra aquí), indicando qué representante está asignado a cada cliente.

### Ejemplo 2: Arquitectura de Tres Niveles

Imaginemos un sistema de gestión de una biblioteca.

*   **Nivel Interno (Físico):** Esto describiría cómo los libros y la información de los usuarios están físicamente almacenados en los discos duros: qué tipo de archivos se usan, dónde están los índices para buscar rápidamente, y cómo se gestiona el espacio. Los administradores de la base de datos se preocupan por este nivel para optimizar el rendimiento.

*   **Nivel Conceptual (Lógico):** Es la visión global y abstracta de la biblioteca. Aquí veríamos las entidades principales (Libros, Usuarios, Préstamos, Autores) y cómo se relacionan entre sí. Por ejemplo, un `Usuario` puede realizar muchos `Préstamos`, y cada `Préstamo` se relaciona con un `Libro` específico. Este nivel define qué datos existen y sus relaciones, sin preocuparse por cómo se almacenan físicamente. Los diseñadores de bases de datos trabajan en este nivel.

*   **Nivel Externo (Vistas):** Son las diferentes "ventanas" o vistas personalizadas que los distintos usuarios tienen de la base de datos.
    *   **Vista para el Lector:** Podría ver solo la disponibilidad de los libros y su fecha de devolución, pero no vería los datos personales de otros usuarios ni los registros de multas.
    *   **Vista para el Bibliotecario:** Podría ver los datos de los usuarios, todos los préstamos activos y el historial, y tendría acceso a funciones para registrar nuevos libros o marcar devoluciones. No vería cómo los datos están guardados físicamente, solo la información relevante para su trabajo.

    La **independencia de datos** permite que si se cambia la forma en que los libros se guardan físicamente (cambio en el Nivel Interno), el bibliotecario y el lector no necesitan cambiar su forma de interactuar con el sistema (sus Vistas permanecen iguales).
