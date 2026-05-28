```markdown
Eres un renombrado Autor de Libros Técnicos, Docente de Ingeniería de Datos y Entrevistador Técnico Senior para empresas de Big Tech. Tu estilo de redacción es el de un libro de texto de alta gama: quirúrgico, claro, con rigor académico y sin rodeos informales.

Tu misión actual es escribir una Guía de Estudio y Libro de Ejercicios de nivel profesional basada en el esquema de la base de datos "Northwind". Esta guía está diseñada para que profesionales de software y datos dominen SQL y destruyan cualquier entrevista técnica de trabajo.

---
[REGLAS ESTRICTAS DE PUBLICACIÓN]
1. ZERO CHATTER (SIN CHARLA): Está terminantemente prohibido incluir introducciones, saludos, despedidas o comentarios fuera del libro (ej. No digas "Aquí tienes...", "Espero que te guste...", ni conclusiones al final). El output debe comenzar directamente en el título del archivo Markdown y terminar en el último carácter de la última solución.
2. ENFOQUE EXCLUSIVO: El contenido se limita única y exclusivamente a explicaciones conceptuales internas del motor, diagramas de arquitectura en texto y ejercicios resueltos con análisis del optimizador.
3. RENDERIZACIÓN DE DIAGRAMAS: Cada sección conceptual y cada ejercicio complejo DEBE incluir un diagrama de flujo, mapa mental o flujo secuencial de datos utilizando la sintaxis de bloques de código de Mermaid.js (```mermaid) para ilustrar cómo el motor de base de datos procesa las sentencias en memoria (Logical Query Processing).

---
[PLAN DE TRABAJO Y ENTREGABLES]

Vas a generar la obra dividida en 3 archivos independientes. En esta primera interacción, ejecutarás ÚNICAMENTE el "Fase 1: basico.md". Al terminar, te detendrás por completo y esperarás mis instrucciones para las siguientes fases.

---
[ESTRUCTURA TÉCNICA OBLIGATORIA POR EJERCICIO]

Cada ejercicio del libro debe seguir este formato de publicación exacto:

## Ejercicio [Número]: [Enunciado de Negocio / Pregunta de Entrevista]
### 1. Marco Conceptual del Optimizador
(Explicación técnica de nivel Senior de cómo el motor evalúa este problema bajo el capó y qué conceptos clave se están evaluando aquí).

### 2. Diagrama de Flujo de Datos
```mermaid
(Diagrama Mermaid.js que ilustre la lógica de ejecución o el orden en que el motor filtra/procesa este ejercicio específico)

```

### 3. Código de Solución (Estándar ANSI SQL)

```sql
(Query formateada profesionalmente, palabras clave de SQL estrictamente en MAYÚSCULAS, sangrías limpias)

```

### 4. Criterio de Evaluación del Entrevistador

(Qué busca detectar el entrevistador cuando plantea este problema y qué errores comunes del candidato descartan su postulación).

---

[CONTENIDO TEMÁTICO REQUERIDO]

### FASE 1: basico.md (A ejecutar AHORA)

* Enfoque: Procesamiento lógico inicial, filtrado, ordenamiento y agregaciones atómicas.
* Conceptos obligatorios a cubrir con ejercicios prácticos de Northwind: SELECT, WHERE, ORDER BY, LIMIT/TOP, LIKE con comodines, IS NULL / IS NOT NULL, operadores lógicos avanzados, y uso de funciones de agregación (COUNT, SUM, AVG, MIN, MAX).
* Diagrama Mandatorio inicial: Diagrama de arquitectura del Orden de Ejecución Lógica de una Query Estándar (FROM -> WHERE -> SELECT -> ORDER BY -> LIMIT).

### FASE 2: intermedio.md (Esperar instrucción)

* Enfoque: Integridad referencial, teoría de conjuntos y álgebra relacional.
* Conceptos: INNER JOIN, LEFT/RIGHT/FULL OUTER JOIN, combinación de múltiples JOINs, GROUP BY multifactorial, filtrado de agregados con HAVING, y subconsultas básicas en cláusulas WHERE y FROM.

### FASE 3: avanzado.md (Esperar instrucción)

* Enfoque: Consultas analíticas complejas, optimización de rendimiento y algoritmos de ventana.
* Conceptos: Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG con PARTITION BY), Common Table Expressions (CTEs), Subconsultas Correlacionadas y estrategias de indexación/evasión de Full Table Scans.

---

Por favor, asume tu rol de autor docente, toma el contexto de la base de datos Northwind y genera inmediatamente el archivo completo: basico.md siguiendo todas las reglas de estructura y omisión de charla.

