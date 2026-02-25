# Clase 1.01: Física del Dato y Sistemas de Almacenamiento

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: La cruda realidad del hardware

Antes de escribir tu primer `CREATE TABLE`, debes entender dónde viven tus datos. Una base de datos no es magia; es una pieza de software finamente ajustada para lidiar con las limitaciones físicas de la arquitectura computacional moderna.

- **El Cuello de Botella del I/O:** La RAM es extremadamente rápida (nanosegundos) pero volátil y costosa. El disco (SSD NVMe o Magnético) es persistente y barato, pero lento (microsegundos a milisegundos). El trabajo de un motor como PostgreSQL es minimizar el tiempo que la CPU pasa esperando al disco.
- **El "Heap" y las Páginas:** En PostgreSQL, los datos de las tablas se almacenan en un área llamada el _Heap_. Este espacio no es continuo, se divide en bloques (generalmente de 8KB, las "Páginas"). Cada vez que haces un `SELECT`, el motor no trae una sola fila a la memoria; carga páginas enteras desde el disco a su caché en memoria (el _Shared Buffers_). Si diseñas filas demasiado anchas (con campos de texto masivos sin compresión `TOAST`), menos filas caben en una página, y por lo tanto, requieres más I/O para leer la misma cantidad de tuplas.
- **MVCC (Multi-Version Concurrency Control):** Cuando actualizas (`UPDATE`) o borras (`DELETE`) una fila en Postgres, los datos antiguos no se borran físicamente en ese instante. El motor inserta una _nueva_ versión de la fila. Esto permite que las lecturas no bloqueen las escrituras. Sin embargo, esto requiere un proceso de limpieza posterior conocido como _Vacuum_, vital para evitar la "hinchazón" o _Bloat_ excesivo en tu disco.

## 2. Integración SDLC: Las implicancias del almacenamiento en el diseño

Cuando participas en el ciclo de vida de desarrollo de software (SDLC) en 2026, el DBA no es alguien al que le pasas un script SQL al final de la construcción de la app. El diseño estructural de la base de datos se diagrama a la vez que el backend.

- **Diseño Físico Consciente:** Al elegir los tipos de datos en el modelado. No usas un `UUID` genérico si no lo necesitas, porque los `UUID v4` son aleatorios, lo que significa que insertarlos masivamente causa fragmentación en los índices (los llamados _Page Splits_). Optas por un `UUID v7` o enteros secuenciales grandes para mantener la localidad de la caché.
- **Afinación de Infraestructura as Code:** En CI/CD y despliegues con Terraform, debes provisionar los volúmenes (EBS en AWS, por ejemplo) en función de tus ratios de Lectura/Escritura. Sistemas pesados en escrituras masivas requerirán configurar volúmenes exclusivos y con altos IOPS pre-provisionados dedicados únicamente a la escritura de los _logs_ de transacciones, manteniéndolos separados de los discos de datos regulares.

## 3. Diferenciación de Tipos de BD (A nivel de disco)

Para el almacenamiento persistente, no todas las bases de datos organizan los bits de la misma forma:

- **Relacionales (B-Trees / PostgreSQL):** Excelentes para transacciones críticas y consultas donde se leen múltiples columnas de unas pocas filas seleccionadas. Utilizan estructuras de almacenamiento orientadas a filas dentro de bloques.
- **Bases de Datos Columnares (ClickHouse, Redshift):** Ideales para analítica (OLAP). Almacenan los valores de una sola columna juntos de manera contigua. ¿Para qué cargar columnas en RAM que tu consulta `SELECT sum(ventas) FROM tx` ni siquiera está pidiendo?
- **NoSQL de Familias de Columnas (Cassandra / ScyllaDB):** Optimizadas para escritura masiva agregando mutaciones a estructuras conocidas como _LSM-Trees_ (Log-Structured Merge-Tree). No hay "Páginas de 8KB" aleatorias como en el Heap de Postgres; la inserción ocurre secuencialmente en disco sin bloqueos agresivos, logrando una tasa de ingesta monstruosa a costa de operaciones relacionales complejas.

## 4. Laboratorio Interactivo: La Anatomía de la Persistencia y el Desastre

**El Escenario (Refactor mental de tu clase de instalación de 2013):**  
En el taller de administración antiguo probabas inserciones y caídas del servidor.
Imagina que hoy, alguien desconecta el servidor eléctrico o tu contenedor en Kubernetes es destruido bruscamente (OOMKilled) justo en medio de 1000 transacciones.
Cuando PostgreSQL reinicia... no hay corrupción de datos. ¿Por qué?

**El Concepto Clave: WAL (Write-Ahead Logging)**

Para sobrevivir al desastre sin destruir el rendimiento (porque escribir inmediatamente cada fila en el bloque disperso correspondiente de disco sería muy lento), PostgreSQL hace lo siguiente:

1.  **Modifica en Memoria:** Modifica la página de datos solo en la memoria RAM (convirtiéndola en una _Dirty Page_).
2.  **Escribe el Log:** Escribe el _intento_ de cambio _secuencialmente_ en un archivo de bitácora en disco (el _WAL_). Esta escritura, al ser puramente agregada secuencialmente al final del archivo, no sufre costosas latencias de búsqueda en el disco.
3.  **Confirma a la App:** Reporta la "Transacción exitosamente completada" (`COMMIT`) a tu aplicación conectada.
4.  **Sincronización Diferida (Checkpoint):** Eventualmente, en un evento conocido como _Checkpoint_, vuelca en un proceso asíncrono en segundo plano (perezosamente) todas las páginas "sucias" de la RAM hacia sus ubicaciones permanentes reales en los archivos del _Heap_.

---

### Reto de Laboratorio (Responder en chat)

Quiero que reflexiones sobre este mecanismo (WAL y Checkpoints) y cómo impacta en la actualidad.

**Pregunta del Reto:**
Tienes un microservicio de e-commerce en la nube atravesando un evento de alto tráfico (Black Friday). Tu aplicación está inyectando una cantidad brutal de órdenes (_inserts_ e _updates_ constantes).
De pronto, los tiempos de respuesta de la base de datos se degradan severamente durante un minuto, y notas que el disco NVMe está saturado al 100% (IOPS al tope). Sin embargo, luego todo vuelve a ser rapidísimo por unos 15 minutos, hasta que repentinamente vuelve a "atragantarse" el disco por un minuto entero y el ciclo se repite.

Basándote en la teoría expuesta de cómo PostgreSQL maneja su caché (páginas sucias) y la sincronización a disco: **¿Qué crees que es ese "evento" periódico que está ahogando el disco e interrumpiendo las operaciones de la app, y por qué ocurre cíclicamente?**

_(Tómate tu tiempo. Escribe tu hipótesis y veamos cómo está tu mentalidad de arquitecto frente al análisis de cuellos de botella reales de I/O)._
