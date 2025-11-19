# Balotario - Clase 04: Administración de RDBMS

A continuación se presenta un balotario de 20 preguntas de opción múltiple, diseñadas para evaluar la comprensión de los conceptos clave de esta clase.

---

**1. ¿Cuál es el rol principal de un Administrador de Bases de Datos (DBA)?**
a) Escribir todas las consultas SQL para las aplicaciones.
b) Diseñar la interfaz de usuario de las aplicaciones.
c) Gestionar y mantener la base de datos, asegurando su operación eficiente, segura y confiable.
d) Vender licencias del software de la base de datos.

**Respuesta Correcta:** c)
**Justificación:** El rol del DBA es multifacético y se centra en la salud general de la base de datos, abarcando desde la instalación y configuración hasta la seguridad, el rendimiento y la recuperación ante desastres.
**Por qué las otras son incorrectas:**
*   a) Los desarrolladores suelen escribir las consultas de la aplicación, aunque el DBA puede optimizarlas.
*   b) Es tarea de los diseñadores de UI/UX y desarrolladores de frontend.
*   d) Es una función comercial, no técnica de administración.

---

**2. ¿Cuál de las siguientes tareas NO es una responsabilidad típica de un DBA?**
a) Realizar copias de seguridad (backups).
b) Otorgar y revocar permisos de usuario.
c) Desarrollar la lógica de negocio de la aplicación.
d) Monitorear y optimizar el rendimiento de las consultas.

**Respuesta Correcta:** c)
**Justificación:** La lógica de negocio (las reglas y procesos específicos de la aplicación) es desarrollada por los analistas de negocio y los desarrolladores de aplicaciones. El DBA se asegura de que la base de datos soporte esa lógica de manera eficiente.
**Por qué las otras son incorrectas:**
*   a, b, d) Son responsabilidades fundamentales y diarias de un DBA.

---

**3. En la administración de Oracle, ¿qué es una "Instancia"?**
a) El conjunto de archivos físicos en el disco.
b) Una copia de seguridad completa de la base de datos.
c) Una unidad lógica de almacenamiento que contiene tablas.
d) La combinación de la memoria (SGA/PGA) y los procesos en segundo plano que acceden a los datos.

**Respuesta Correcta:** d)
**Justificación:** La instancia es el conjunto de procesos y estructuras de memoria que están en ejecución y permiten que la base de datos (los archivos en disco) sea accesible. Una base de datos puede ser "montada" por una instancia.
**Por qué las otras son incorrectas:**
*   a) Eso es la base de datos en sí.
*   b) Es un backup.
*   c) Eso describe un Tablespace.

---

**4. ¿Para qué se utiliza una herramienta como RMAN en Oracle?**
a) Para escribir y depurar código PL/SQL.
b) Para crear y restaurar copias de seguridad (backups).
c) Para monitorear el rendimiento de la red.
d) Para diseñar diagramas de Entidad-Relación.

**Respuesta Correcta:** b)
**Justificación:** RMAN (Recovery Manager) es la utilidad principal de Oracle para realizar tareas de respaldo, restauración y recuperación de la base de datos de manera eficiente y confiable.
**Por qué las otras son incorrectas:**
*   a) Para eso se usan herramientas como SQL Developer o TOAD.
*   c) Es tarea de herramientas de monitoreo de red.
*   d) Para eso se usan herramientas CASE como Oracle SQL Developer Data Modeler.

---

**5. ¿Qué es un "Tablespace" en el contexto de Oracle?**
a) Un sinónimo de "Base de Datos".
b) Una unidad lógica de almacenamiento que agrupa objetos de base de datos y se mapea a archivos físicos.
c) Un usuario especial con permisos de administrador.
d) Una herramienta gráfica para visualizar el espacio en disco.

**Respuesta Correcta:** b)
**Justificación:** Un tablespace es una capa de abstracción. El DBA crea tablas y otros objetos dentro de un tablespace, y Oracle gestiona cómo ese tablespace se distribuye en uno o más archivos de datos físicos.
**Por qué las otras son incorrectas:**
*   a) No son sinónimos; una base de datos contiene uno o más tablespaces.
*   c) Es un concepto de almacenamiento, no de usuario.
*   d) Es una estructura lógica, no una herramienta.

---

**6. Si un DBA necesita implementar una solución para minimizar el tiempo de inactividad de la base de datos, está trabajando en:**
a) Optimización del rendimiento.
b) Gestión de Alta Disponibilidad.
c) Diseño físico de la base de datos.
d) Automatización de tareas.

**Respuesta Correcta:** b)
**Justificación:** La Alta Disponibilidad (High Availability - HA) se refiere específicamente a las arquitecturas y tecnologías (como clústeres, replicación, etc.) diseñadas para asegurar que la base de datos permanezca operativa incluso si un componente falla.
**Por qué las otras son incorrectas:**
*   a, c, d) Son tareas importantes del DBA, pero no se enfocan directamente en minimizar el tiempo de inactividad.

---

**7. ¿Cuál es la diferencia entre un "Usuario" y un "Esquema" en Oracle?**
a) No hay diferencia, son lo mismo.
b) Un usuario es una cuenta para conectarse, mientras que un esquema es la colección de objetos que pertenecen a ese usuario.
c) Un esquema es un tipo de privilegio, y un usuario es quien lo recibe.
d) Un usuario solo puede leer datos, mientras que un esquema puede modificarlos.

**Respuesta Correcta:** b)
**Justificación:** En Oracle, cuando se crea un usuario, se crea automáticamente un esquema del mismo nombre. Todos los objetos (tablas, vistas, etc.) que ese usuario crea "viven" dentro de su esquema.
**Por qué las otras son incorrectas:**
*   a) Aunque están estrechamente relacionados, no son conceptualmente idénticos.
*   c, d) Son definiciones incorrectas.

---

**8. La tarea de "Planificación de la Capacidad" implica:**
a) Decidir qué usuarios pueden acceder a qué tablas.
b) Prever el crecimiento futuro de los datos y el uso de recursos.
c) Optimizar una consulta SQL para que se ejecute más rápido.
d) Instalar el software del RDBMS en un nuevo servidor.

**Respuesta Correcta:** b)
**Justificación:** La planificación de la capacidad es una tarea estratégica donde el DBA analiza las tendencias de crecimiento para asegurar que el sistema (almacenamiento, CPU, memoria) podrá soportar la demanda futura.
**Por qué las otras son incorrectas:**
*   a) Es gestión de seguridad.
*   c) Es optimización de rendimiento.
*   d) Es instalación y configuración.

---

**9. ¿Qué es un "Rol" en la seguridad de una base de datos?**
a) El título del puesto de un DBA.
b) Un conjunto de privilegios que se pueden otorgar a los usuarios.
c) Un tipo especial de tabla para auditoría.
d) Una conexión activa a la base de datos.

**Respuesta Correcta:** b)
**Justificación:** Los roles simplifican la gestión de permisos. En lugar de otorgar 20 privilegios individuales a cada nuevo desarrollador, el DBA puede crear un rol "DESARROLLADOR" con esos 20 privilegios y luego simplemente otorgar ese rol al usuario.
**Por qué las otras son incorrectas:**
*   a, c, d) Son conceptos diferentes.

---

**10. La optimización del rendimiento es una tarea reactiva (resolver problemas) y proactiva (prevenirlos). ¿Cuál de las siguientes es una tarea proactiva de optimización?**
a) Matar una sesión que está bloqueando a otras.
b) Analizar el plan de ejecución de una consulta lenta reportada por un usuario.
c) Gestionar y reconstruir índices regularmente.
d) Restaurar una tabla borrada por accidente.

**Respuesta Correcta:** c)
**Justificación:** La gestión regular de índices (crear, eliminar o reconstruir según sea necesario) es una tarea de mantenimiento proactivo para asegurar que las consultas sigan siendo eficientes a medida que los datos cambian.
**Por qué las otras son incorrectas:**
*   a, b) Son tareas reactivas, responden a un problema que ya está ocurriendo.
*   d) Es una tarea de recuperación.

---

**11. SQL*Plus y psql son ejemplos de:**
a) Herramientas Gráficas (GUI)
b) Herramientas de Línea de Comandos
c) Herramientas de Monitoreo
d) Herramientas de Respaldo y Recuperación

**Respuesta Correcta:** b)
**Justificación:** Ambas son interfaces de línea de comandos que permiten a los administradores y desarrolladores interactuar con la base de datos (Oracle y PostgreSQL, respectivamente) mediante texto.
**Por qué las otras son incorrectas:**
*   a) MySQL Workbench o SQL Developer son ejemplos de GUI.
*   c, d) Oracle Enterprise Manager o RMAN son ejemplos de estas categorías.

---

**12. En Oracle, la memoria compartida utilizada por todos los procesos de la instancia se conoce como:**
a) PGA (Program Global Area)
b) Archivos de control
c) SGA (System Global Area)
d) Redo Logs

**Respuesta Correcta:** c)
**Justificación:** La SGA es el área de memoria principal y compartida de una instancia de Oracle, que contiene cachés de datos, el pool compartido (consultas SQL) y otra información necesaria para todos los procesos.
**Por qué las otras son incorrectas:**
*   a) La PGA es un área de memoria privada para cada proceso del servidor.
*   b, d) Son estructuras de archivos físicos en disco, no de memoria.

---

**13. ¿Cuál de las siguientes acciones de un DBA está más relacionada con el "Diseño Físico" de la base de datos?**
a) Entrevistar a los usuarios para entender los requisitos del negocio.
b) Crear un Diagrama Entidad-Relación.
c) Decidir cómo particionar una tabla grande y en qué tablespace colocar los índices.
d) Asignar el rol de "solo lectura" a un usuario de reportes.

**Respuesta Correcta:** c)
**Justificación:** El diseño físico se ocupa de la implementación concreta en el SGBD y el hardware. La partición y la ubicación del almacenamiento son decisiones de diseño físico para optimizar el rendimiento y la gestión.
**Por qué las otras son incorrectas:**
*   a, b) Pertenecen al diseño conceptual y lógico.
*   d) Es una tarea de gestión de seguridad.

---

**14. ¿Por qué es importante para un DBA automatizar tareas?**
a) Para reducir la cantidad de memoria que usa la base de datos.
b) Para asegurar que las tareas de mantenimiento rutinarias se realicen de manera consistente y confiable.
c) Para encriptar los datos de la base de datos.
d) Para aumentar el número de usuarios simultáneos.

**Respuesta Correcta:** b)
**Justificación:** Tareas como la limpieza de logs antiguos, la actualización de estadísticas o la verificación de backups son repetitivas. Automatizarlas (mediante scripts o trabajos programados) reduce el riesgo de error humano y asegura que se ejecuten sin falta.
**Por qué las otras son incorrectas:**
*   a, c, d) La automatización no tiene un impacto directo en estos aspectos.

---

**15. La herramienta `exp` de Oracle, mostrada en los ejemplos, se utiliza para:**
a) Ejecutar consultas SQL complejas.
b) Crear un backup lógico (exportar datos y metadatos a un archivo).
c) Importar datos desde un archivo de texto.
d) Expandir el tamaño de un tablespace.

**Respuesta Correcta:** b)
**Justificación:** `exp` (y su sucesor `expdp` - Data Pump) es una utilidad de Oracle para crear exportaciones lógicas de la base de datos, que pueden ser usadas como copias de seguridad o para migrar datos.
**Por qué las otras son incorrectas:**
*   a) Se hace con SQL*Plus, SQL Developer, etc.
*   c) Para eso se usa `imp` o `impdp` (import) o SQL*Loader.
*   d) Se hace con comandos DDL como `ALTER TABLESPACE`.

---

**16. Un RDBMS se basa en el:**
a) Modelo de grafos.
b) Modelo de documentos.
c) Modelo relacional.
d) Modelo clave-valor.

**Respuesta Correcta:** c)
**Justificación:** La "R" en RDBMS significa Relacional. Estos sistemas organizan los datos en tablas basadas en el modelo relacional de E.F. Codd.
**Por qué las otras son incorrectas:**
*   a, b, d) Son modelos de datos asociados con bases de datos NoSQL.

---

**17. Cuando un DBA otorga un "Privilegio" a un usuario, está:**
a) Dándole permiso para realizar una acción específica (ej. `CREATE TABLE`).
b) Asignándole una tarea de mantenimiento.
c) Creando una copia de seguridad de sus datos.
d) Cambiando su contraseña.

**Respuesta Correcta:** a)
**Justificación:** Un privilegio es un derecho para ejecutar una sentencia SQL particular o para acceder al objeto de otro usuario. Es el mecanismo fundamental de control de acceso.
**Por qué las otras son incorrectas:**
*   b, c, d) Son otras tareas de administración, pero no la definición de otorgar un privilegio.

---

**18. La "Gestión de Versiones y Migraciones" es responsabilidad del DBA y se refiere a:**
a) Controlar las versiones del código de la aplicación.
b) Planificar y ejecutar actualizaciones del software del RDBMS y mover datos entre sistemas.
c) Crear vistas materializadas.
d) Limitar el número de versiones de una fila que se guardan.

**Respuesta Correcta:** b)
**Justificación:** Esta tarea implica aplicar parches al SGBD, actualizarlo a una nueva versión (ej. de Oracle 11g a 19c) o migrar una base de datos completa de un servidor a otro, o de un sistema on-premise a la nube.
**Por qué las otras son incorrectas:**
*   a) Es una tarea de los desarrolladores, usualmente con herramientas como Git.
*   c, d) Son tareas técnicas específicas, no la definición de gestión de versiones.

---

**19. Oracle SQL Developer y MySQL Workbench son ejemplos de:**
a) Sistemas Operativos.
b) RDBMS.
c) Herramientas de Línea de Comandos.
d) Herramientas Gráficas (GUI) para administración y desarrollo.

**Respuesta Correcta:** d)
**Justificación:** Ambas son aplicaciones de escritorio con interfaces gráficas que permiten a los DBAs y desarrolladores interactuar con la base de datos de una manera visual e intuitiva.
**Por qué las otras son incorrectas:**
*   a) Son aplicaciones, no sistemas operativos.
*   b) Son clientes que se conectan a un RDBMS, no son el RDBMS en sí.
*   c) Son GUI, lo opuesto a herramientas de línea de comandos.

---

**20. ¿Qué distingue a un RDBMS de un SGBD genérico?**
a) Un RDBMS es más rápido.
b) Un RDBMS está específicamente basado en el modelo relacional de datos.
c) Un RDBMS solo puede ser ejecutado en sistemas Linux.
d) Un RDBMS no necesita un DBA.

**Respuesta Correcta:** b)
**Justificación:** El término SGBD es genérico. Un RDBMS es un tipo específico de SGBD que implementa el modelo relacional (tablas, claves, integridad referencial, etc.). Todos los RDBMS son SGBD, pero no todos los SGBD son RDBMS (ej. una base de datos de grafos es un SGBD pero no un RDBMS).
**Por qué las otras son incorrectas:**
*   a) La velocidad depende de muchos factores, no del tipo de modelo.
*   c) Los RDBMS son multiplataforma.
*   d) Todos los SGBD de producción requieren administración.
