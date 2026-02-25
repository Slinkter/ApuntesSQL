# Clase 2.01: Anatomía Interna de PostgreSQL

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: Lo que tu ORM no te cuenta

En 2013, cuando escribías tus sentencias SQL, asumías que el motor de base de datos era una "caja negra" mágica que guardaba tablas. En 2026, un Arquitecto de Datos debe entender exactamente cómo se mueven los bytes, porque a escala, ignorar esto destruye el rendimiento.

### El Heap y las Páginas

PostgreSQL almacena los datos de las tablas en una estructura llamada el **Heap** (Montículo).

- El Heap no es un bloque continuo gigante. Está fraccionado en **Páginas (Pages)** de tamaño fijo (típicamente 8 KB).
- Cada vez que haces un `SELECT`, el sistema operativo no lee "una fila". Lee **Páginas enteras** desde el disco hacia la memoria caché (_Shared Buffers_).
- Si tu fila ocupa 1 KB, en una página caben aproximadamente 8 filas. Si tu consulta necesita leer 8,000 filas, Postgres tendrá que hacer I/O de disco para leer 1,000 páginas.
- **Axioma de Arquitectura:** El diseño de tus tipos de datos define el ancho de tu fila. Mientras más ancha sea tu fila (por tener columnas inútiles o textos gigantes), menos filas caben en la caché (RAM), obligando al motor a rotar la caché e ir al disco NVMe constatemente (provocando altos _Cache Misses_).

### MVCC (Multi-Version Concurrency Control)

PostgreSQL no sobreescribe ni borra los datos físicamente de inmediato.
Cuando ejecutas un `UPDATE fila_1`, Postgres internamente:

1. Marca la `fila_1_version_actual` como _obsoleta_ (Dead Tuple).
2. Inserta una nueva `fila_1_nueva_version` en otra parte de la página de 8 KB (o en otra página si esta está llena).

**¿Por qué hace esto?** Para que otras transacciones que estaban realizando un `SELECT` masivo puedan seguir leyendo la versión antigua sin ser bloqueadas por la escritura. "Las lecturas no bloquean a las escrituras, y las escrituras no bloquean a las lecturas".

## 2. Integración SDLC: La amenaza del "Bloat" y el Vacuum

El diseño basado en MVCC trae una gran responsabilidad operativa: el disco se llena de _Tuplas Muertas_.
Si tienes un proceso que hace un `UPDATE` a una tabla de "estado_sesion" cada segundo, y no controlas el MVCC, tu tabla crecerá hasta el infinito. Esto se llama **Table Bloat**.

- El **Vacuum** es el proceso de limpieza recolector de basura de PostgreSQL. Su trabajo es escanear los archivos de las tablas y marcar el espacio ocupado por tuplas muertas como "disponible" para nuevas inserciones.
- **En el SDLC moderno:** Los monitoreos en CI/CD y Grafana no solo miden CPU. Miden el porcentaje de "Bloat" por tabla y el ratio de ejecución de _Autovacuum_. Si el _Bloat_ supera el 20% en tablas críticas transaccionales, el equipo de plataforma interviene, ya que significa que las consultas están leyendo páginas de 8KB que están en su mayoría vacías.

## 3. Reto de Laboratorio: Optimizando el I/O Físico

Has llegado a un proyecto donde los desarrolladores crearon una tabla de auditoría:

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50),
    old_data TEXT,   -- un JSON gigante con miles de lineas
    new_data TEXT,   -- otro JSON gigante
    created_at TIMESTAMP
);
```

Los reportes que hacen un simple `SELECT user_id, action_type FROM audit_logs ORDER BY created_at DESC LIMIT 100` tardan demasiado, y el DBA indica que la caché se está "ensuciando" porque cada lectura trae demasiados megabytes a la memoria.

**Pregunta del Reto:**
Sabiendo cómo funcionan las Páginas de 8KB de PostgreSQL. Si la consulta NUNCA usa los campos enormes `old_data` ni `new_data` para reportes de actividad visual, pero tu aplicación los necesita consultar una vez al mes para auditorías legales, ¿Qué **patrón de diseño físico de tablas** implementarías para optimizar el almacenamiento y evitar que los textos gigantes desplacen información útil de la memoria caché en las operaciones del día a día?

_(Pista: Considera la separación vertical)._
