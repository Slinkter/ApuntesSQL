# Clase 3.03: Del Antipatrón PL/pgSQL y Triggers al Event-Driven

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: El Legado de la Semana 12.

En el Sílabo de 2013, las semanas 12 y 13 del curso de la Universidad de Lima abordaban la Programación de Bases de Datos (PL/SQL). El entregable 4 requería explícitamente "la utilización de un procedimiento y un trigger" enlazados a una aplicación web.

Esta arquitectura "State-of-the-Art" para Oracle y SQL Server entre los años 1995-2015, consistía en **ocultar la lógica de negocio dentro del motor de base de datos**.

- **¿Cuál era la idea original?** Rendimiento brutal. En lugar de hacer 3 llamadas de red entre tu servidor de Backend (PHP/Java) y la Base de Datos para verificar stock, registrar la venta, e insertar un recibo de pago, empaquetabas todo en un mega `PROCEDURE` llamado `p_procesar_venta(cliente_id, producto, cant)`.
- **¿Por qué es un Antipatrón en 2026?**
    1. Aritmética de CPUs: Los servidores de BD transaccionales son las cajas de Hardware "Single-Node" más costosas del planeta y el recurso más difícil de escalar horizontalmente (Escalado "Scale-Out"). En contraste, escalar tu backend Node.js, Go o Kotlin en Kubernetes requiere apenas apretar un botón para inyectar 50 Pods "Stateless" más.
    2. Versionado y Pruebas Unitarias: Documentar o retroceder (Rollback) un Trigger erróneo introducido productivamente era (y es) una pesadilla. No existen buenos ecosistemas de "Unit Testing" y "Cobertura" como los hay en lenguajes modernos. El código quemado en un Trigger se vuelve "código espagueti inobservable" para los desarrolladores de la App que de pronto ven cómo los datos mutan mágicamente en sus narices sin rastro explícito en sus métricas de log.

## 2. Integración SDLC: Hacia el Event-Driven con CDC

Hoy en día, un Arquitecto de Datos traslada la orquestación fuera del gestor Relacional hacia la capa aplicativa a través de Patrones de Arquitecturas Orientadas a Eventos (EDA - Event-Driven Architecture) con Kafka y Outbox Patterns.

### Reemplazando el "Trigger" Audit (Ej. de 2013)

En el 2010 la forma usual de auditar "quién borra una factura o cambia un salario" era un `BEFORE/AFTER UPDATE TRIGGER` que insertaba copias textuales en `audit_facturas`.
Consecuencia de Triggers Críticos: Ese `INSERT` a la tabla auditora es síncrono. Bloqueará (_Locking_) tu principal hilo transaccional. En carga hiperconcurrente en Black Friday, los Triggers detienen la economía.

### La solución moderna (Debezium y Change Data Capture - CDC):

1. **El Gestor de Base de Datos es Sagrado:** Hacemos una transacción clásica limpia (`UPDATE cliente SET sueldo = 2000`). Se ejecuta a velocidad luz, sin triggers colgados deteniendo el COMMIT en disco local. Nada más perturba la tabla y la App se va libre rápidamente.
2. Como estudiamos en la Fase 1 (`Física del Dato`), sabemos que esto generó una entrada en el **Log de Transacciones WAL de PostgreSQL**.
3. **El Inyector Lógico:** Instalamos una plataforma tipo "Debezium Connect" (CDC) corriendo como proceso externo (Fuera del cluster relacional de PostgreSQL) que "oye" mágicamente ese log (Lectura lógica de réplica, "Logical Decoder"). Entiende que mutaste un salario y arroja ese paquete a un Tópico de "Apache Kafka" (un broker de Streaming masivo) en milisegundos.
4. Cientos de otros microservicios externos asíncronamente "Saben" qué pasó con el salario al instante (y guardan su auditoría, su envío por email u operan lo que deseen en otros ecosistemas o BD distintas), sin ralentizar jamás al monolito central.

## 3. Reto de Arquitectura Distribuida (Laboratorio)

**El Escenario:**
Has refactorizado el sistema monolítico de 2013 de inventario y "Orden_Trabajo/Factura". Ahora tienes dos bases de datos completamente independientes y distribuidas.

- Microservicio A (Servicio de Ventas/Facturación): Registra al cliente y su pago, confirmando que la 'Factura 901' está pagada. Tiene BD PostgreSQL A.
- Microservicio B (Servicio de Despacho Logístico): Se ocupa de ordenar a maquinaria hacer la silla, rebajar del almacén materia prima y preparar el envío. Tiene BD PostgreSQL B.

**El Reto Mítico Distribuido:**
Tu aplicación Node ejecuta el cargo a la tarjeta, e inserta la factura local (Paso A OK). Ahora tu backend hace un request HTTP (`fetch`) al Servicio B para despachar (Paso B). Si justo cuando terminaste de guardar el Pago "A", el servidor B se cae por un apagón de red... te quedas con un pago cobrado pero NUNCA despacharás (Inconsistencia distribuida grave).

¿Qué técnica o **"Patrón de Arquitectura Distribuido Moderno"** usarías en 2026 para garantizar, que si la factura "A" fue guardada localmente, el evento para el despacho logística "B" se cumpla SÍ o SÍ garantizadamente mediante un sistema de colas, aún si el equipo "B" está apagado durante 3 días?

_(Pista: Tiene que ver con CDC y el patrón Outbox mencionado)._
