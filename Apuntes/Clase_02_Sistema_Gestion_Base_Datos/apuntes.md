# 📐 Clase 02: Modelo Relacional

| Columna de Palabras Clave y Preguntas | Columna de Notas: Conceptos Clave (¡Sencillo y Divertido!) |
| :--- | :--- |
| **Arquitectura de 3 Niveles** | La BD tiene tres "capas" de vista: **1. Interno** (la estructura física de almacenamiento, lo que el computador ve), **2. Conceptual** (la visión global de toda la BD para todos los usuarios, con sus interrelaciones y restricciones), y **3. Externo** (las vistas personalizadas que ve cada usuario o aplicación). |
| **Independencia de Datos** | Es la capacidad mágica de modificar un esquema (como cambiar la estructura física o **Independencia Física**) sin tener que modificar el nivel superior (como la visión lógica o **Independencia Lógica**). ¡Esto simplifica los cambios! |
| **Terminología Relacional** | En el modelo relacional, las cosas tienen nombres elegantes: una **Tabla** se llama **Relación**, una **Fila** se llama **Tupla**, y una **Columna** se llama **Atributo**. |
| **Restricciones: PK y FK** | Estas son las reglas de integridad: La **PK (Primary Key)** es la cédula de identidad de cada fila; debe ser única y ¡jamás nula!. La **FK (Foreign Key)** es el atributo que usamos para conectar una tabla con la PK de otra (la relación entre un pedido y el cliente que lo hizo). |
| **Funciones del DBMS (Superpoderes)** | El DBMS es multifuncional: maneja a los **usuarios** (permisos), la **performance** (velocidad), el **backup/recovery** (respaldo y restauración) y, muy importante, las **Transacciones**. |
| **Transacción y ACID** | Una transacción es una operación completa de lectura o escritura. Sus propiedades deben ser **ACID**: **A**tomicidad (todo se hace o nada se hace), **C**onsistencia (el estado de la BD es siempre válido), **I**solamiento (las transacciones no se interfieren) y **D**urabilidad (los cambios son permanentes). |

**Resumen de la Clase 02:** Esta clase detalló la arquitectura de la BD (Interna, Conceptual, Externa) y el concepto de Independencia de Datos. Revisamos la terminología clave del Modelo Relacional (Tuplas, Relaciones, Atributos) y las restricciones cruciales como PK y FK. Cerramos con la importancia de las Transacciones y sus propiedades ACID para la confiabilidad.

---