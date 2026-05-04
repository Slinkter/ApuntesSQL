# Clase 1.04: Migrations-as-Code y el SDLC del Dato

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: El Caos del DDL Manual

En 2013, el ciclo de vida de un esquema de base de datos solía lucir así:

1. El desarrollador creaba las tablas en su base de datos local (con clics o scripts DDL en una consola gráfica).
2. Se exportaba un gigantesco archivo `schema.sql`.
3. El día del pase a Producción, el DBA ejecutaba ese script (o un archivo `alter.sql` con suerte) sobre la base de datos productiva.
4. Si fallaba, el rollback era un desastre manual que paralizaba al equipo.

Este enfoque no escala. En un entorno moderno (2026), con integración continua (CI) y entrega continua (CD), la base de datos ya no puede ser un componente "fuera de banda". El esquema de la base de datos **es código**, y debe ser tratado con el mismo rigor que tu código funcional: versionado, probado, documentado y desplegado de manera determinista.

### Migrations-as-Code (Esquemas como Código)

Las migraciones son archivos atómicos (usualmente SQL o XML/YAML según la herramienta) que describen un cambio incremental en la base de datos.
Herramientas estándar de la industria (Flyway, Liquibase, o los ORMs como Prisma, Alembic o TypeORM) implementan esto manteniendo una tabla especial de metadatos (ej. `flyway_schema_history`) dentro de la propia base de datos.

Cuando la aplicación inicia y su pipeline corre:

1.  Verifica la tabla de historial de la BD para saber en qué versión está.
2.  Escanea el repositorio por migraciones nuevas o no aplicadas.
3.  Aplica únicamente los deltas faltantes (los _Up scripts_).

## 2. Integración SDLC: Patrones de Evolución Sin Tiempo de Inactividad (Zero Downtime)

En 2013 podías decir: "La aplicación estará en mantenimiento de 2 a 4 AM para actualizar la base de datos". Hoy, un e-commerce global no puede hacer eso.

Tus migraciones deben permitir el _Zero-Downtime Deployment_ (ZDD).
Imagina que quieres cambiar el nombre de la columna `direccion` a `direccion_completa`.

- **El Antipatrón (2013):** Ejecutar `ALTER TABLE clientes RENAME COLUMN direccion TO direccion_completa;`.
    - _Resultado:_ En el milisegundo en que aplicas esto, la versión antigua de tu aplicación que sigue corriendo explotará porque no encuentra `direccion`.

- **La Arquitectura Evolutiva (2026 - Patrón Expand/Contract):**
    1.  **Fase 1 (Expand):** Creación de una migración para agregar la _nueva_ columna `direccion_completa`. Dejar la antigua intacta.
    2.  **Fase 2 (Aplicación):** Modificar la aplicación para que empiece a escribir en _ambas_ columnas (Dual Write) pero siga leyendo de la antigua. Desplegar.
    3.  **Fase 3 (Migración de Datos):** Un script asíncrono en background copia los miles de registros pasados de la columna vieja a la nueva.
    4.  **Fase 4 (Cambio de lectura):** La aplicación cambia a leer de la nueva columna `direccion_completa`.
    5.  **Fase 5 (Contract):** Semanas después, una nueva migración ejecuta `ALTER TABLE clientes DROP COLUMN direccion;`.

## 3. Reto Teórico: Infraestructura Inmutable

**Pensamiento Arquitectónico:**
Observa la carpeta `ULima/Clases` original. Seguro que tenías un "Script_ejemplo_warehouse.txt" (lo vi en la carpeta `otros`). Ese modelo de "ejecuta este archivo enorme" crea servidores "Floco de Nieve" (Snowflake Servers), servidores donde nadie sabe exactamente la historia de cómo llegaron a estar configurados así.

**El Reto:**
Acabas de escribir una migración en SQL para añadir una restricción crítica (Constraint) a tu tabla de `pagos`:
`ALTER TABLE pagos ADD CONSTRAINT pago_positivo CHECK (monto > 0);`

Tus pruebas locales pasan. Haces el commit y el sistema de CI/CD lo despliega a Producción. Sin embargo, la migración **falla rotundamente en Producción y rompe el pipeline**. ¿Por qué una migración de DDL válida (funciona en local/pruebas) fallaría al llegar a Producción de manera inesperada? ¿Qué lección te enseña esto sobre modelar tu base de datos?

_(Piensa en la relación entre los datos existentes y las nuevas reglas)._
