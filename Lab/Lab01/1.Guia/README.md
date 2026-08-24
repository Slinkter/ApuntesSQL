# Laboratorio 01: PostgreSQL & Northwind Mastery en AWS EC2

> **Entorno de Trabajo:** PostgreSQL 16 sobre AWS EC2 (Amazon Linux 2023 / Ubuntu 24.04 LTS) con Docker Compose.  
> **Dataset:** Esquema canónico Northwind (`pthom/northwind_psql`).  
> **Estándar Metodológico:** Guía de buenas prácticas y marco analítico en [`STANDARD.md`](STANDARD.md).

---

## 🗺️ Mapa de Navegación del Laboratorio 01

El Laboratorio 01 está organizado siguiendo una ruta de aprendizaje estructurada desde los prerrequisitos y la infraestructura en la nube hasta ejercicios avanzados de optimización y entrevistas técnicas:

### 1. ☁️ Infraestructura y Despliegue en la Nube (`1.Guia/`)
- **[`0.Guia_Docker_AWS.md`](0.Guia_Docker_AWS.md):** Manual paso a paso para aprovisionar la instancia EC2, configurar Security Groups (puertos 22 y 5432 restringidos a `/32`), instalar Docker en **Amazon Linux 2023** (`ec2-user`, `dnf`) / **Ubuntu 24.04** (`ubuntu`, `apt`), transferir archivos mediante `scp` directo y orquestar el contenedor con `docker compose`.
- **[`Material/docker-compose.yml`](Material/docker-compose.yml):** Manifiesto de infraestructura declarativa con PostgreSQL 16 Alpine, mapeo de volúmenes persistentes (`pg_data`), inicialización de base de datos de solo lectura (`:ro`), límites de recursos (RAM 512M), logging y healthcheck.
- **[`Material/.env.example`](Material/.env.example):** Plantilla de variables de entorno seguras (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `PGPORT`).
- **[`Material/.env`](Material/.env):** Archivo de variables de entorno locales por defecto.
- **[`Material/db_northwind.sql`](Material/db_northwind.sql):** Script canónico de inicialización de las 14 tablas relacionales de Northwind.
- **[`STANDARD.md`](STANDARD.md):** Estándar pedagógico, plantillas de ejercicios por nivel, orden lógico de ejecución del motor SQL y marco de 6 pasos *"Cómo Pensar como un Analista de Datos"*.

---

### 2. 📚 Libros de Ejercicios Prácticos Enumerados (`2.Ejercicios/`)
- **[`../2.Ejercicios/0.prerrequisitos.md`](../2.Ejercicios/0.prerrequisitos.md):** Fundamentos teóricos, modelos relacionales, pipeline de 12 pasos de ejecución lógica del motor, matriz de visibilidad de alias, análisis de planes `EXPLAIN (ANALYZE, BUFFERS)`, transacciones ACID y comandos de `psql`.
- **[`../2.Ejercicios/1.basico.md`](../2.Ejercicios/1.basico.md):** 50 ejercicios enumerados cubriendo `SELECT`, `WHERE`, `ORDER BY`, operadores lógicos, `LIKE`, `IS NULL`, funciones de fecha (`AGE`, `EXTRACT`), funciones de texto y sentencias condicionales `CASE WHEN`.
- **[`../2.Ejercicios/2.intermedio.md`](../2.Ejercicios/2.intermedio.md):** Agrupamientos `GROUP BY`, filtros de agregación `HAVING`, combinación de datos mediante `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN` y `Self-Join` de jerarquías.
- **[`../2.Ejercicios/3.avanzado.md`](../2.Ejercicios/3.avanzado.md):** Consultas avanzadas, subconsultas correlacionadas, expresiones de tabla comunes (`WITH` / CTEs), CTEs recursivas y funciones de ventana analíticas (`ROW_NUMBER()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `NTILE()`).
- **[`../2.Ejercicios/4.examen_entrevista.md`](../2.Ejercicios/4.examen_entrevista.md):** Banco de 30 preguntas de alto nivel para entrevistas de Data Analyst / Analytics Engineer / SQL Developer, con casos de negocio y soluciones optimizadas.
- **[`../2.Ejercicios/aws_ejercicio.sql`](../2.Ejercicios/aws_ejercicio.sql):** Script SQL de referencia para validación y pruebas de ejecución en el servidor AWS.

---

## 📐 Estándar de Formato y Metodología
Cada ejercicio sigue estrictamente el formato y marco analítico definido en [`STANDARD.md`](STANDARD.md):
1. **Marco Mental:** 6 pasos de pensamiento del analista de datos (Entender el negocio $\rightarrow$ Fuentes $\rightarrow$ Relaciones $\rightarrow$ Filtros/Agrupaciones $\rightarrow$ Salida $\rightarrow$ Validación).
2. **🎓 Explicación del Profesor:** Analogía pedagógica de alta retención y concepto central.
3. **Desglose del Motor de Ejecución:** Orden lógico de procesamiento (`FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `WINDOW` $\rightarrow$ `SELECT` $\rightarrow$ `DISTINCT` $\rightarrow$ `ORDER BY` $\rightarrow$ `LIMIT`).
4. **Código de Solución SQL:** Sintaxis nativa PostgreSQL comentada, con palabras clave en mayúsculas y alias explícitos con `AS`.
5. **🛠️ Nota del Ingeniero de Datos:** Análisis de rendimiento, algoritmos del optimizador e impacto de índices.
6. **Resultados Verificados:** Salida de tabla ASCII exacta.
