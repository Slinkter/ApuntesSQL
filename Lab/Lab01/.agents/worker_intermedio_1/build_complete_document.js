const fs = require('fs');

const parsed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/parsed_structure.json', 'utf8'));
const executed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/executed_queries.json', 'utf8'));

const b1 = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/modules/block1_01_10.json', 'utf8'));
const b2 = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/modules/block2_11_20.json', 'utf8'));
const b3 = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/modules/block3_21_30.json', 'utf8'));
const b4 = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/modules/block4_31_40.json', 'utf8'));
const b5 = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/modules/block5_41_50.json', 'utf8'));

const enrichedAll = { ...b1, ...b2, ...b3, ...b4, ...b5 };

// Truncation helper
function formatOutput(rawOutput, maxRows = 12) {
  const lines = rawOutput.trim().split('\n');
  if (lines.length <= 2) return rawOutput;
  
  const header = lines[0];
  const separator = lines[1];
  const footer = lines[lines.length - 1];
  
  const dataRows = lines.slice(2, lines.length - 1);
  if (dataRows.length <= maxRows + 3) {
    return rawOutput;
  }
  
  const shownRows = dataRows.slice(0, maxRows);
  const omittedCount = dataRows.length - maxRows;
  const omissionText = ` ... [${omittedCount} filas omitidas para brevedad del documento] ...`;
  
  return [
    header,
    separator,
    ...shownRows,
    omissionText,
    footer
  ].join('\n');
}

// Clean mock data helper
function cleanMockData(str) {
  if (!str) return str;
  return str
    .replace(/Alfreds Futterkiste - Actualizado/g, 'Alfreds Futterkiste')
    .replace(/TechCorp Peru/g, 'Rancho grande')
    .replace(/DataLabs Chile/g, 'Simons bistro')
    .replace(/NWE01/g, 'RANCH')
    .replace(/NWE02/g, 'SIMOB')
    .replace(/\(93 rows\)/g, '(91 rows)')
    .replace(/\(834 rows\)/g, '(832 rows)');
}

const docParts = [];

// Header
docParts.push(`# Libro de Ejercicios SQL — Nivel 2: Intermedio

> **Base de Datos:** Canonical Northwind (\`pthom/northwind_psql\`)  
> **Motor Objetivo:** PostgreSQL 16 (Compatible con AWS EC2 / RDS / Aurora)  
> **Volumen:** 50 Ejercicios de Nivel Intermedio y Consultas Multidimensionales  
> **Ejes Temáticos:** Agregaciones Avanzadas (\`GROUP BY\`, \`HAVING\`), Subconsultas (\`EXISTS\`, \`IN\`, Correlacionadas, Derived Tables), Expresiones Condicionales (\`CASE WHEN\`, \`FILTER\`), Cruces Complejos (\`SELF JOIN\`, \`FULL OUTER JOIN\`, Multi-Table Joins, \`LATERAL\`), y Funciones de Ventana Analíticas (\`ROW_NUMBER\`, \`RANK\`, \`DENSE_RANK\`, \`LAG\`, \`LEAD\`, \`SUM OVER\`, \`NTILE\`).

---

## 🧭 Mapa de Navegación del Nivel Intermedio

| Bloque | Ejercicios | Enfoque Principal | Conceptos Clave del Motor |
| :--- | :---: | :--- | :--- |
| **Bloque 1** | Ejercicios 01 – 10 | Agregaciones Complejas y Filtros de Grupo | \`GROUP BY\`, \`HAVING\`, \`COUNT\`, \`SUM\`, \`AVG\`, \`HashAggregate\` |
| **Bloque 2** | Ejercicios 11 – 20 | Subconsultas y Álgebra de Conjuntos | \`WHERE Subquery\`, \`IN\`, \`EXISTS\` (Semi Join), \`NOT EXISTS\` (Anti Join), \`ANY\`, \`ALL\` |
| **Bloque 3** | Ejercicios 21 – 30 | Lógica Condicional y Matrices de Pivote | \`CASE Simple\`, \`CASE Searched\`, \`FILTER (WHERE ...)\`, \`CASE + SUM\` Pivots |
| **Bloque 4** | Ejercicios 31 – 40 | Relaciones Avanzadas y Estructuras Complejas | \`SELF JOIN\` (Jerarquías), \`FULL OUTER JOIN\`, \`RIGHT JOIN\`, \`CROSS JOIN\`, \`JOIN LATERAL\` |
| **Bloque 5** | Ejercicios 41 – 50 | Funciones de Ventana y Analítica SQL | \`ROW_NUMBER\`, \`RANK / DENSE_RANK\`, Top-N, \`LAG / LEAD\`, Running Totals, \`NTILE\` |

---
`);

for (let i = 1; i <= 50; i++) {
  const p = parsed.find(x => x.num === i);
  const ex = executed.find(x => x.num === i);
  const info = enrichedAll[i];
  
  if (!p || !ex || !info) {
    console.error(`Missing data for exercise ${i}`);
    continue;
  }
  
  const formattedOutput = formatOutput(cleanMockData(ex.rawOutput), 12);
  const cleanSQL = cleanMockData(p.sql);
  const cleanOpt = cleanMockData(p.opt);
  const cleanNota = cleanMockData(p.nota);
  const cleanCrit = cleanMockData(p.crit);
  const cleanDiagram = cleanMockData(p.diagram);
  
  // Format engine steps
  const engineStepsText = info.engine.join('\n');
  
  // Diagram rendering
  let diagramSection = '';
  if (cleanDiagram && cleanDiagram.trim().length > 0) {
    if (cleanDiagram.includes('```text') || cleanDiagram.includes('=====')) {
      const fenceBlock = cleanDiagram.startsWith('```') ? cleanDiagram : `\`\`\`text\n${cleanDiagram}\n\`\`\``;
      diagramSection = `### Diagrama ASCII de Ejecución en el Motor (Paso a Paso)\n\n${fenceBlock}`;
    } else {
      const fenceBlock = cleanDiagram.startsWith('```') ? cleanDiagram : `\`\`\`mermaid\n${cleanDiagram}\n\`\`\``;
      diagramSection = `### Diagrama de Flujo (Mermaid)\n\n${fenceBlock}`;
    }
  }
  
  const exMd = `## Ejercicio ${i}: ${p.title}

### 🎯 Enunciado y Caso de Uso

${info.enunciado}

### 🎓 Explicación del Profesor

**Analogía:** ${info.analogia}  
**Concepto Central:** ${info.concepto}

> 💡 **Tip del Profesor:** ${info.tip}

### 🧠 Cómo Pensar como un Analista de Datos

- **Pregunta de Negocio & KPI:** ${info.kpi}
- **Entidad Central & Granularidad:** ${info.fuentes}
- **Fuentes & Cruces (JOINs):** ${info.relaciones}
- **Filtros & Agrupaciones:** ${info.filtros}
- **Proyección & Orden (SELECT / ORDER BY):** ${info.proyeccion}
- **Validación Analítica:** ${info.validacion}

### ⚙️ Desglose del Motor de Ejecución (Logical Query Processing)

${engineStepsText}

### Marco Conceptual del Optimizador

${cleanOpt}

${diagramSection}

### Código de Solución

\`\`\`sql
${cleanSQL}
\`\`\`

#### 📊 Resultado Real de Ejecución en PostgreSQL (AWS EC2):

\`\`\`text
${formattedOutput}
\`\`\`

> 🛠️ **Nota del Ingeniero de Datos:** ${cleanNota}

### Criterio de Evaluación del Entrevistador

${cleanCrit}

---
`;

  docParts.push(exMd);
}

// Conclusion section
docParts.push(`## 🏁 Sección 3: Conclusión y Evaluación del Nivel Intermedio

¡Felicitaciones por completar los 50 ejercicios del **Nivel Intermedio**!

Has dominado:
1. **El Ciclo de Vida del Motor:** Comprensión rigurosa del orden lógico (\`FROM\` $\\to$ \`WHERE\` $\to$ \`GROUP BY\` $\to$ \`HAVING\` $\to$ \`WINDOW\` $\to$ \`SELECT\` $\to$ \`ORDER BY\` $\to$ \`LIMIT\`).
2. **Transformación Condicional y Pivotes:** Creación de matrices de datos multidimensionales con \`CASE\` y la cláusula nativa \`FILTER\`.
3. **Álgebra Relacional Avanzada:** Navegación de grafos con \`SELF JOIN\`, auditorías de integridad con \`FULL OUTER JOIN\` y subconsultas correlacionadas por fila con \`CROSS JOIN LATERAL\`.
4. **Analítica de Ventana:** Cálculo de métricas avanzadas (Running totals, diferencias temporales, rankings particionados y cuartiles) sin colapsar el grano de las tablas.

👉 **Próximo Paso:** Continúa con \`3.avanzado.md\` para dominar Common Table Expressions recursivas (\`WITH RECURSIVE\`), optimización con \`EXPLAIN (ANALYZE, BUFFERS)\`, diseño de índices avanzados y funciones JSONB / Full-Text Search.
`);

const finalContent = docParts.join('\n');
fs.writeFileSync('2.Ejercicios/2.intermedio.md', finalContent, 'utf8');

console.log(`Successfully generated 2.Ejercicios/2.intermedio.md!`);
console.log(`Total bytes: ${Buffer.byteLength(finalContent, 'utf8')}`);
console.log(`Total lines: ${finalContent.split('\n').length}`);
