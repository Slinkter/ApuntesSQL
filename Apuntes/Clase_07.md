# Clase 07: Modelamiento de Datos en la Empresa: Normalización (Parte I)

---

## 📚 Conceptos Clave

**Fecha:** Noviembre 18, 2025 (Resumen del documento `NormalizacioBD.pdf`)

---

## Notas Generales

### Introducción a la Normalización

La normalización es un proceso de diseño para bases de datos relacionales que busca eliminar redundancias de datos e inconsistencias de dependencia. Un diseño normalizado facilita la comprensión, ampliación y mantenimiento del código, resultando en una aplicación más rápida y eficiente.

### Formalización Cero (No Normalizado)

Un diseño no normalizado presenta problemas significativos de redundancia y escalabilidad.

**Ejemplo:**
Tabla `usuarios` con datos de usuarios y sus URLs.

| nombre | empresa | direccion_empresa | url1    | url2    |
|--------|---------|-------------------|---------|---------|
| Joe    | ABC     | 1 Work Lane       | abc.com | xyz.com |
| Jill   | XYZ     | 1 Job Street      | abc.com | xyz.com |

**Problemas:**
*   **Grupos Repetitivos:** Las columnas `url1` y `url2` son un grupo repetitivo. ¿Qué pasa si se necesita una tercera URL? Se tendría que alterar la tabla.
*   **Falta de Clave Única:** No hay una clave primaria para diferenciar de forma única a dos usuarios con el mismo nombre.

---

### Primera Forma Normal (1FN)

**Reglas:**
1.  Eliminar los grupos repetitivos.
2.  Crear una tabla separada para cada grupo de datos relacionados.
3.  Identificar cada grupo con una clave primaria.

**Aplicación:**
Se introduce una clave primaria `userId` y se elimina el grupo repetitivo de URLs. Ahora, cada URL de un usuario ocupa su propia fila.

| userId | nombre | empresa | direccion_empresa | url     |
|--------|--------|---------|-------------------|---------|
| 1      | Joe    | ABC     | 1 Work Lane       | abc.com |
| 1      | Joe    | ABC     | 1 Work Lane       | xyz.com |
| 2      | Jill   | XYZ     | 1 Job Street      | abc.com |
| 2      | Jill   | XYZ     | 1 Job Street      | xyz.com |

**Problema Solucionado:** Limitación del número de URLs.
**Nuevo Problema:** Redundancia de datos. La información de la empresa y del usuario se repite para cada URL.

---

### Segunda Forma Normal (2FN)

**Regla:**
1.  Crear tablas separadas para grupos de datos que se aplican a múltiples registros.
2.  Relacionar estas tablas con una clave externa.

*(Nota: La 2FN se enfoca en eliminar dependencias parciales en claves primarias compuestas. El ejemplo aquí ilustra el principio general de separar entidades.)*

**Aplicación:**
Se separa la entidad `urls` en su propia tabla, relacionada con `usuarios` mediante una clave externa `relUserId`.

**Tabla `usuarios`:**
| userId | nombre | empresa | direccion_empresa |
|--------|--------|---------|-------------------|
| 1      | Joe    | ABC     | 1 Work Lane       |
| 2      | Jill   | XYZ     | 1 Job Street      |

**Tabla `urls`:**
| urlId | relUserId | url     |
|-------|-----------|---------|
| 1     | 1         | abc.com |
| 2     | 1         | xyz.com |
| 3     | 2         | abc.com |
| 4     | 2         | xyz.com |

**Problema Solucionado:** Se pueden añadir URLs sin duplicar datos del usuario.
**Nuevo Problema:** Si la empresa ABC tiene 200 empleados, el nombre y la dirección de la empresa se repiten 200 veces en la tabla `usuarios`.

---

### Tercera Forma Normal (3FN)

**Regla:**
1.  Eliminar aquellos campos que no dependan directamente de la clave primaria (dependencias transitivas).

**Aplicación:**
La información de la empresa (`empresa`, `direccion_empresa`) no depende del `userId`, sino que es una entidad propia. Se crea una tabla `empresas`.

**Tabla `usuarios`:**
| userId | nombre | relEmpresaId |
|--------|--------|--------------|
| 1      | Joe    | 1            |
| 2      | Jill   | 2            |

**Tabla `empresas`:**
| emprId | empresa | direccion_empresa |
|--------|---------|-------------------|
| 1      | ABC     | 1 Work Lane       |
| 2      | XYZ     | 1 Job Street      |

**Resultado:** El diseño ahora está en 3FN. La mayoría de los desarrolladores consideran que 3FN es suficiente para la mayoría de las aplicaciones.

---

### Cuarta Forma Normal (4FN)

**Regla:**
1.  En relaciones "varios-con-varios", las entidades independientes no pueden ser almacenadas en la misma tabla.

**Contexto:** Se aplica cuando hay dependencias multivaluadas. Imagina que ahora los usuarios pueden estar asociados a varias URLs predefinidas, y varias URLs pueden ser usadas por varios usuarios (relación N:M).

**Aplicación:**
Se crea una tabla de unión (`url_relations`) para manejar la relación N:M entre usuarios y URLs.

**Tabla `url_relations`:**
| relationId | relatedUrlId | relatedUserId |
|------------|--------------|---------------|
| 1          | 1            | 1             |
| 2          | 1            | 2             |
| 3          | 2            | 1             |
| 4          | 2            | 2             |

Esto elimina la duplicación en la tabla `urls` si varias personas usan la misma URL.

---

### Quinta Forma Normal (5FN)

**Regla:**
1.  La tabla original debe ser reconstruible sin pérdida de información desde las tablas resultantes en las que se ha descompuesto.

**Contexto:** Es un nivel de normalización esotérico y raramente necesario. Asegura que no se han creado columnas extrañas durante la descomposición y que la estructura es del tamaño justo.

---

## Pistas y Keywords

*   **Normalización:** Proceso para reducir redundancia e inconsistencias.
*   **Redundancia:** Repetición de datos.
*   **Anomalías:** Problemas de inserción, actualización o borrado causados por redundancia.
*   **1FN:** Atomicidad, sin grupos repetitivos.
*   **2FN:** Sin dependencias parciales sobre claves compuestas.
*   **3FN:** Sin dependencias transitivas (atributos dependen solo de la PK).
*   **4FN:** Manejo de dependencias multivaluadas (relaciones N:M).
*   **5FN:** Reconstrucción sin pérdida de la tabla original.
*   **Clave Primaria / Externa:** Identificadores para relacionar tablas.

---

## Resumen Final Crítico

La normalización es una técnica paso a paso para organizar los datos en una base de datos relacional. Cada forma normal resuelve un tipo específico de anomalía de datos.
- **1FN** asegura que los datos sean atómicos.
- **2FN** y **3FN** eliminan dependencias funcionales que causan redundancia, asegurando que los atributos describan a la entidad identificada por la clave primaria.
- **4FN** y **5FN** manejan dependencias más complejas (multivaluadas y de unión) que son menos comunes pero importantes en ciertos diseños.
Un diseño en 3FN es generalmente el objetivo para la mayoría de las aplicaciones, logrando un buen equilibrio entre la eliminación de redundancia y la complejidad del esquema.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Se basa en los conceptos de "Modelamiento de Datos" (Clase 06) y "Bases de Datos Relacionales" (Clase 03).
*   **Conexiones Siguientes:** Un esquema normalizado es fundamental para escribir consultas `JOIN` eficientes (Clase 10 y 11) y para el diseño de "Data Warehouses" (Clase 14), que a menudo utilizan esquemas desnormalizados (como el esquema de estrella) por razones de rendimiento en consultas analíticas. Este tema continuará en "Normalización (Parte II)" (Clase 09).

---

