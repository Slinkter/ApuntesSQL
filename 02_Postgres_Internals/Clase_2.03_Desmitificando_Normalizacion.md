# Clase 2.03: Desmitificando la Normalización Pura

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: Académico vs. Operacional

Tus documentos `NormalizacioBD.pdf` explicito los cinco niveles o Formas Normales (1NF a 5NF).

- "Crear tablas separadas para aquellos grupos de datos que se aplican a varios registros y relacionarlas mediante una clave externa".
- "Eliminar aquellos campos que no dependan de la clave (3NF)".

Esta teoría matemática salva a tus sistemas ERP o Bancarios de las infames "anomalías de actualización" (si un usuario cambia de correo, solo lo actualizas en la tabla `usuarios`, no en sus 500 tablas de `ordenes`).

Sin embargo, a escala global (sistemas con miles de _Reads per Second_ o RPS), esta fragmentación académica causa caídas catastróficas.
En una base de datos relacional, "reconstruir" la estructura usando sentencias `JOIN` significa que la CPU tiene que cruzar datos leyendo potencialmente de diferentes lugares físicos en el disco o en la memoria. Cargar el historial de facturas de un cliente podría involucrar un `JOIN` de 7 u 8 tablas inmensas si sigues la BCNF (Boyce-Codd Normal Form) estricta.

### La Desnormalización Estratégica (Bounded Contexts)

En 2026 y bajo arquitecturas de Nube, aplicamos la "Desnormalización Estratégica" no porque no conozcamos la teoría, sino justamente porque entendemos sus límites de cómputo (Martin Kleppmann discute esto brillantemente en "Designing Data-Intensive Applications").

- En bases de datos analíticas (OLAP/Data Warehouses), usamos el patrón Estrella o Copo de Nieve (Desnormalizado para poder sumarizar rápidamente).
- En transaccional (OLTP) de alta lectura, embebemos datos.
  Si el nombre de la empresa de logística raramente cambia, y lo que necesitas es leer ese nombre en cada orden 10,000 veces por segundo, podrías copiar el "Nombre de la Logística" a tu tabla de "Órdenes de Compra", pagando el costo de tener que actualizar ese campo textual si alguna vez la empresa cambia de nombre. Intercambias "Eficiencia de actualización" por "Eficiencia masiva de Lectura".

## 2. Integración SDLC: Command Query Responsibility Segregation (CQRS)

En arquitecturas gigantes, el dolor de la normalización es resuelto mediante CQRS.

1.  **Command (Escritura):** Tienes tu motor de base de datos OLTP central altamente Normalizado (3NF). Las escrituras y actualizaciones van ahí. Esto garantiza que tus datos sean puros y cumplan ACID.
2.  **Query (Lectura):** Tienes vistas materializadas (`MATERIALIZED VIEW` en Postgres) o réplicas asíncronas en bases de datos analíticas como ClickHouse o almacenes clave-valor rápidos (Redis).

Tus APIs de consulta de clientes ya no atacan el esquema Normalizado haciendo _JOINs_. Leen representaciones "pre-calculadas" y Totalmente **Desnormalizadas** en las réplicas de lectura.

## 3. Reto Teórico y de Arquitectura (Laboratorio)

**El Escenario:**
En tus apuntes originales (Clase 3, Modelo de Datos de una Mueblería), había una tabla `orden_pedido` (Cabecera) y `producto_ordenado` (Detalle).
Típica implementación 3NF.

Cuando se carga el "Dashboard" del cliente en la aplicación web, el backend ejecuta una consulta que suma `(cantidad_ordenada * precio)` de cada detalle más los impuestos para mostrarle al cliente su total histórico gastado.
A medida que el cliente hace cientos de compras a lo largo de 5 años, mostrar su Dashboard empieza a tardar 3, 5 y finalmente 10 segundos, ahogando los servidores.

**El Reto Arquitectónico:**
El DBA de la "vieja escuela" te sugerirá crear múltiples índices para optimizar la sumatoria matemática del JOIN en tiempo real constante.

Como un Arquitecto de Datos moderno, debes proponer una estrategia de **Desnormalización Estratégica** implementada _dentro_ de PostgreSQL (y el backend) que le permita al Dashboard cargar instantáneamente en 20 milisegundos sin importar cuántos millones de detalles tenga el cliente registrado históricamente.

_(Pista: Pensemos en totales pre-agregados en escrituras, o materialización de datos analíticos)._
