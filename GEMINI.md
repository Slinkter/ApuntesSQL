# ApuntesSQL - PostgreSQL Architecture & Mastery

Este proyecto es una plataforma educativa integral para la maestría en **PostgreSQL**, diseñada bajo estándares de ingeniería de alto rendimiento para el año 2026. Combina material histórico refactorizado con teoría relacional avanzada y prácticas modernas de arquitectura de datos.

## 🚀 Propósito y Filosofía
Transformar el conocimiento fragmentado en una base sólida de **Data Architecture**. El enfoque no es solo aprender SQL, sino entender los *internals* del motor (páginas de 8KB, MVCC, WAL) y la teoría relacional pura (C.J. Date).

## 🛠️ Stack Tecnológico
- **Database Engine:** PostgreSQL 15+ (v15, v16+)
- **Standards:** SQL ANSI 2023, PL/pgSQL
- **Documentation:** Markdown, Mermaid.js (ER Diagrams)
- **Frontend (Apuntes):** HTML/CSS Cornell Style para legibilidad académica.

## 📂 Estructura del Proyecto
```bash
.
├── SQL/
│   ├── 1.basico.md            # PostgreSQL notes básico (refactorizado)
│   ├── 2.intermedio.md        # PostgreSQL notes intermedio (refactorizado)
│   ├── Youtube00/             # Tutorial series (básico → avanzado)
│   │   ├── 1.basico.md
│   │   ├── 2.intermedio.md
│   │   ├── 3.avanzado.md
│   │   ├── db_northwind.sql   # Dataset Northwind para PostgreSQL
│   │   ├── prompt.md          # Persona ArquiDB — auditoría y calidad
│   │   ├── plan.md            # Plan de aprendizaje 16 semanas
│   │   └── README.md
│   └── Youtube01/
│       ├── Taller/            # Workshop: ejercicios + docker-compose
│       │   ├── docker-compose/ # Postgres y MySQL listos para usar
│       │   ├── Guia/          # Guías paso a paso con imágenes
│       │   ├── Tipos-Join/    # Diagramas de JOIN
│       │   └── *.md / *.sql   # Material del taller
│       ├── sql/               # Scripts SQL sueltos
│       ├── *.html             # Cheat sheets y guías de estudio
│       └── README.md
├── ULima/
│   ├── Apuntes/               # HTML estático estilo Cornell (16 semanas)
│   ├── Clases/                # PDFs + TXT de clases originales
│   └── otros/                 # Documentación complementaria
├── Credenciales/
│   ├── Guia_Despliegue_Docker_AWS.md
│   └── key_u_docker.pem
├── AGENTS.md                  # Guía para el agente opencode
├── GEMINI.md                  # Visión del proyecto y plan maestro
├── README.md
└── .github/
    ├── copilot-instructions.md
    └── workflows/
```

## 📖 Plan Maestro (16 Semanas)
1.  **Fundamentos (S01-S07):** DBMS, ERD, DDL, DML, Joins y Subconsultas.
2.  **Examen Parcial (S08):** Validación de fundamentos.
3.  **Avanzado (S09-S15):** Group By, CTEs, PL/pgSQL, Transacciones, Índices y Seguridad.
4.  **Examen Final (S16):** Evaluación integral.

## 🧪 Laboratorio: Northwind en PostgreSQL
El proyecto utiliza una versión adaptada de la base de datos **Northwind** para PostgreSQL.
- **Ubicación:** `SQL/Youtube00/db_northwind.sql`
- **Modelado:** `SQL/Youtube00/1.basico.md` incluye el diagrama ER en formato Mermaid.

## ⚙️ Desarrollo y Auditoría
- **Auditoría:** Se sigue el estándar definido en `prompt.md` para garantizar calidad técnica (vía ArquiDB).
- Convenciones: 
    - Priorizar `JSONB` sobre `JSON`.
    - Usar `SERIAL`/`BIGSERIAL` para IDs secuenciales (o `UUID v7`).
    - Explicar siempre el impacto en I/O de cada consulta (`EXPLAIN ANALYZE`).

## 📝 Historial de Refactorizaciones y OCR (2026-06-25)
- **Re-OCR y Transcripción:** Se aplicó Ollama + GLM-OCR a Clase_00 a Clase_06, logrando transcripciones de alta fidelidad.
- **Limpieza de Encoding:** Todos los archivos TXT e HTML fueron normalizados a UTF-8 sin BOM.
- **Correcciones de Diseño:** Se re-codificaron a UTF-8 los archivos complementarios `extra_*.html` resolviendo problemas de decodificación y eliminando caracteres huérfanos.
- **Fixes de Formato:** Se repararon líneas pegadas detectadas en la auditoría final (`Clase_10.txt`, `Clase_11.txt`, `Script_Ejemplo_Warehouse.txt`).

---
*Mantenido por el Senior Data Solutions Architect.*
