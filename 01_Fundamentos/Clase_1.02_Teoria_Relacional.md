# Clase 1.02: Teoría Relacional Pura y el Fin de los Monolitos

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: Más allá de "Filas y Columnas"

Si revisamos el material de 2013, la definición de una Base de Datos Relacional era simple: "Es una colección de relaciones o tablas de dos dimensiones para almacenar información". Aunque útil para empezar, esta definición es peligrosa para un arquitecto moderno.

Una tabla no es una hoja de Excel. El modelo relacional, formulado por Edgar F. Codd y pulido por **C.J. Date**, está fundamentado en la **Teoría de Conjuntos** y la lógica de predicados de primer orden.

- **Tuplas vs. Filas:** En matemáticas puras, un conjunto no tiene un orden inherente. Por eso, en SQL, hablar del "siguiente registro" o "el registro anterior" carece de sentido a menos que impongas un ordenamiento explícito (`ORDER BY`). Asumir un orden físico es un antipatrón clásico que rompe la integridad relacional.
- **El Dominio de los Atributos:** En 2013, un atributo (columna) se definía por su tipo de dato básico (`VARCHAR2`, `NUMBER`). En 2026, entendemos que el _Dominio_ de una columna debe ser estrictamente definido (ej. usando de dominios personalizados en PostgreSQL o `CHECK` constraints) para evitar que un salario sea negativo, mucho antes de que la lógica de aplicación intente insertarlo.
- **Normalización Estricta vs. Realidad Distribuida:** En el documento "Normalización de Bases de Datos" antiguo vimos hasta 5 formas normales. En la academia, buscar la 3NF o BCNF es el estándar para evitar anomalías de inserción, actualización y borrado. Sin embargo, en arquitecturas _Data Intensive_ (como menciona **Martin Kleppmann**), los picos o uniones (_JOINs_) masivos sobre 10 tablas altamente normalizadas hundirán el rendimiento de tu CPU. Hoy, aplicamos normalización para asegurar la integridad transaccional (sistemas OLTP puros), pero aplicamos **desnormalización controlada** (usando vistas materializadas, o tipos compuestos como `JSONB`) para optimizar rutas críticas de lectura.

## 2. Integración SDLC: Anomalías en Sistemas Concurrentes

El problema real de un mal diseño relacional no se ve en un esquema de desarrollo con un solo usuario. Se manifiesta en el caos de la concurrencia.

Imagina un esquema antiguo donde el `precio` de un producto se copia en la tabla `detalle_orden` al momento de la venta, pero también dependemos de un campo total precalculado estáticamente en la tabla `orden`.

- ¿Qué pasa si dos transacciones actualizan el mismo registro casi al mismo tiempo (Lost Updates)? En la actualidad, mitigamos esto a nivel de base de datos usando bloqueos explícitos (`SELECT ... FOR UPDATE`), control optimista de concurrencia con columnas de versión, o delegando a niveles de aislamiento superiores (`REPEATABLE READ` o `SERIALIZABLE` en PostgreSQL).
- **El Teorema CAP y PACELC:** En sistemas modernos, tu base de datos probablemente no sea un solo servidor. Tendrás réplicas. El Teorema CAP nos dice que ante una partición de red (P), debes elegir entre Consistencia (C) o Disponibilidad (A). El diseño relacional clásico siempre elige la Consistencia de manera predeterminada. Entender esto te ayuda a justificar por qué una base de datos relacional tradicional puede "caerse" o rechazar escrituras antes que servir datos basura, mientras que un clúster de NoSQL de eventual consistencia seguirá aceptando datos (potencialmente conflictivos).

## 3. Laboratorio Interactivo: El Refactor de la Mueblería

**El Escenario (Rescatado de la Clase 3 de 2013 - "Modelo de Datos de una Muebleria"):**
En el antiguo sílabo (Página 16), tenías un diagrama complejo con tablas: `orden_pedido`, `cliente`, `producto_ordenado`, `producto`, `orden_trabajo`, `linea_orden_trabajo`, `materia_prima`, etc. Todo conectado en una telaraña transaccional monolítica.

En 1999 o 2013, tener 15 tablas para procesar una venta estaba bien. Pero en 2026, si este sistema está en la Nube y la Mueblería procesa miles de pedidos concurrentes, vas a notar que el _lock_ continuo en la tabla de `stock` en `producto` (para actualizar inventario por cada ítem vendido) causará tiempos de espera masivos.

---

### Reto de Diseño Moderno (Refactorización)

Vamos a analizar un punto crítico de ese modelo de la "Mueblería":

- Tienes la tabla `producto` con el atributo `stock` dentro.
- Tienes la tabla `producto_ordenado` (que es el detalle de la compra).

Cuando un cliente compra 3 sillas, tu backend actualiza `producto_ordenado` y, en la misma transacción transaccional, hace un `UPDATE producto SET stock = stock - 3 WHERE id_producto = 'SILLA1';`

**Pregunta del Reto:**
Miles de usuarios intentan comprar la SILLA1 durante una liquidación el mismo segundo. La sentencia `UPDATE producto SET stock...` creará un **Row-Level Lock** y todas las transacciones se formarán en una fila secuencial en la base de datos, destruyendo el rendimiento de las ventas.

Como arquitecto de datos, ¿qué **dos enfoques de diseño a nivel de base de datos** propondrías en 2026 para evitar este cuello de botella extremo en el inventario, sin perder la consistencia de que no puedes vender más de lo que tienes?

_(Pista: Considera separar las sumas y las restas en registros independientes, o usar colas/eventos)._
