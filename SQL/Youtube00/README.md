# YouTube00 — Ejercicios y laboratorio (Postgres)

Propósito: documentar cómo ejecutar y validar los ejercicios contenidos en esta carpeta (guías y el dataset db_northwind.sql).

Contenido clave
- db_northwind.sql — Dataset Northwind preparado para Postgres (no incluye DROP/CREATE).
- 1.basico.md — Guía de SQL básico (consultas SELECT, filtros, joins simples).
- 2.intermedio.md — Agrupamientos, funciones agregadas y técnicas intermedias.
- 3.avanzado.md — Ventanas, CTEs, PL/pgSQL ejemplos avanzados.
- prompt.md — Persona ArquiDB y checklist de auditoría (leer antes de refactorizar ejercicios).

Requisitos
- psql (cliente) o Docker disponible
- Postgres 15+ recomendado

Semillas y arranque rápido
1) Usando psql local (si tienes Postgres instalado):
   # crear la BD (si no existe)
   createdb northwind
   # cargar dataset
   psql -U <user> -d northwind -f PostgresSQL/Youtube00/db_northwind.sql

2) Usando Docker (auto-inicializa desde el SQL):
   docker run --rm --name pg_lab -e POSTGRES_USER=slinkter -e POSTGRES_PASSWORD=slinkter -e POSTGRES_DB=northwind -p 5432:5432 -v "$(pwd)/PostgresSQL/Youtube00/db_northwind.sql":/docker-entrypoint-initdb.d/db_northwind.sql -d postgres:16-alpine
   # comprobar logs
   docker logs -f pg_lab

Ejecutar un solo ejercicio / consulta
- Ejecutar un archivo .sql:
  psql -h <host> -U <user> -d northwind -f path/to/file.sql
- Ejecutar una consulta rápida (inline):
  psql -h <host> -U <user> -d northwind -c "SELECT * FROM customers LIMIT 5;"
- Ejecutar EXPLAIN ANALYZE para medir I/O/planner:
  psql -h <host> -U <user> -d northwind -c "EXPLAIN ANALYZE <tu_query_aqui>;"

Consejos para trabajar con las guías
- Las .md contienen fragmentos; copiar el bloque SQL a un archivo .sql y usar psql -f para ejecutar pasos completos.
- Mantener idempotencia: no agregar DROP/CREATE DATABASE en db_northwind.sql (esta carpeta asume el uso del SQL "dataset-only").
- Cuando propongas cambios a ejemplos, incluya siempre un `EXPLAIN ANALYZE` de la versión corregida.

¿Deseas que convierta cada sección .md en archivos .sql ejecutables y agregue ejemplos `EXPLAIN ANALYZE` por defecto? (Puedo generarlos y commitearlos si confirmas.)