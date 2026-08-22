# Laboratorio 01: PostgreSQL & Northwind Mastery en AWS EC2

> **Entorno de Trabajo:** PostgreSQL 16 sobre AWS EC2 (Amazon Linux 2023 / Ubuntu) con Docker Compose.
> **Dataset:** Esquema canónico Northwind (`pthom/northwind_psql`).

---

## 🗺️ Mapa de Navegación del Laboratorio 01

El Laboratorio 01 está organizado siguiendo una ruta de aprendizaje estructurada desde los prerrequisitos y la infraestructura en la nube hasta ejercicios avanzados de optimización y entrevistas técnicas:

### 1. ☁️ Infraestructura y Despliegue en la Nube
- **[`aws/Guia_Docker_AWS.md`](aws/Guia_Docker_AWS.md):** Manual paso a paso para aprovisionar la instancia EC2, configurar Security Groups, instalar Docker en **Amazon Linux 2023** (`ec2-user`, `dnf`) / **Ubuntu**, transferir archivos mediante `scp` y orquestar el contenedor con `docker compose`.
- **[`aws/docker-compose.yml`](aws/docker-compose.yml):** Manifiesto de infraestructura declarativa con PostgreSQL 16 Alpine, mapeo de volúmenes persistentes y healthcheck.
- **[`aws/db_northwind.sql`](aws/db_northwind.sql):** Script canónico de inicialización de las 14 tablas relacionales de Northwind.

---

### 2. 📚 Libros de Ejercicios Prácticos Enumerados
- **[`Ejercicios/0.prerrequisitos.md`](Ejercicios/0.prerrequisitos.md):** Fundamentos teóricos, modelos relacionales, análisis de planes de ejecución `EXPLAIN (ANALYZE, BUFFERS)`, transacciones ACID y comandos esenciales de `psql`.
- **[`Ejercicios/1.basico.md`](Ejercicios/1.basico.md):** 50 ejercicios enumerados cubriendo `SELECT`, `WHERE`, `ORDER BY`, operadores lógicos, `LIKE`, `IS NULL`, funciones de fecha (`AGE`, `EXTRACT`), funciones de texto y sentencias condicionales `CASE WHEN`.
- **[`Ejercicios/2.intermedio.md`](Ejercicios/2.intermedio.md):** Agrupamientos `GROUP BY`, filtros de agregación `HAVING`, combinación de datos mediante `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN` y `Self-Join` de jerarquías.
- **[`Ejercicios/3.avanzado.md`](Ejercicios/3.avanzado.md):** Consultas avanzadas, subconsultas correlacionadas, expresiones de tabla comunes (`WITH` / CTEs) y funciones de ventana analíticas (`ROW_NUMBER()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `NTILE()`).
- **[`Ejercicios/4.examen_entrevista.md`](Ejercicios/4.examen_entrevista.md):** Banco de preguntas tipo prueba técnica y entrevistas para roles de Data Engineer / SQL Developer, con casos de negocio y soluciones optimizadas.
- **[`Ejercicios/aws_ejercicio.sql`](Ejercicios/aws_ejercicio.sql):** Script SQL práctico de validación de cálculo de antigüedad de empleados en el servidor AWS.

---

## 📐 Estándar de Formato
Cada ejercicio sigue estrictamente el formato definido en [`STANDARD.md`](STANDARD.md):
1. **Enunciado y Objetivo de Negocio**
2. **🎓 Explicación del Profesor:** Analogía pedagógica y concepto central.
3. **Código de Solución SQL:** Sintaxis nativa PostgreSQL comentada y con palabras clave en mayúscula.
4. **🛠️ Nota del Ingeniero de Datos:** Análisis de rendimiento, algoritmos del optimizador e impacto de índices.
