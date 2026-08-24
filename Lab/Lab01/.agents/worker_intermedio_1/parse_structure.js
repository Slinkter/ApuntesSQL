const fs = require('fs');

const raw = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/exercises_raw.json', 'utf8'));

const parsed = raw.map(ex => {
  const text = ex.fullText;
  
  // Title
  const titleMatch = text.match(/^## Ejercicio \d+:?\s*(.*)$/m);
  const title = titleMatch ? titleMatch[1].trim() : ex.title;
  
  // Profesor
  const profMatch = text.match(/### 🎓 Explicación del Profesor([\s\S]*?)(?=###|$)/i);
  const prof = profMatch ? profMatch[1].trim() : '';
  
  // Optimizador
  const optMatch = text.match(/### Marco Conceptual del Optimizador([\s\S]*?)(?=###|$)/i);
  const opt = optMatch ? optMatch[1].trim() : '';
  
  // Diagram (Mermaid or ASCII)
  const mermaidMatch = text.match(/### Diagrama (?:de Flujo \(Mermaid\)|ASCII de Ejecución en el Motor \(Paso a Paso\))([\s\S]*?)(?=###|$)/i);
  const diagram = mermaidMatch ? mermaidMatch[1].trim() : '';
  
  // SQL
  const sqlMatch = text.match(/### C[oó]digo de Soluci[oó]n[\s\S]*?```sql\s*([\s\S]*?)```/i);
  const sql = sqlMatch ? sqlMatch[1].trim() : '';
  
  // Nota Ingeniero
  const notaMatch = text.match(/> 🛠️ \*\*Nota del Ingeniero de Datos:\*\*([\s\S]*?)(?=###|$)/i);
  const nota = notaMatch ? notaMatch[1].trim() : '';
  
  // Criterio
  const critMatch = text.match(/### Criterio de Evaluaci[oó]n del Entrevistador([\s\S]*?)(?=---|$)/i);
  const crit = critMatch ? critMatch[1].trim() : '';
  
  return {
    num: ex.num,
    title,
    prof,
    opt,
    diagram,
    sql,
    nota,
    crit
  };
});

fs.writeFileSync('.agents/worker_intermedio_1/parsed_structure.json', JSON.stringify(parsed, null, 2), 'utf8');
console.log(`Parsed ${parsed.length} exercises.`);
parsed.slice(0, 5).forEach(p => {
  console.log(`Ex ${p.num}: title="${p.title}", hasProf=${!!p.prof}, hasOpt=${!!p.opt}, hasDiag=${!!p.diagram}, hasSQL=${!!p.sql}, hasNota=${!!p.nota}, hasCrit=${!!p.crit}`);
});
