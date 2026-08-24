const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// Find all exercise chunks
const exBlocks = [];
const headerRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const matches = [];
while ((match = headerRegex.exec(content)) !== null) {
  matches.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

for (let i = 0; i < matches.length; i++) {
  const start = matches[i].index;
  const end = (i < matches.length - 1) ? matches[i + 1].index : content.length;
  const chunk = content.substring(start, end);
  
  // Extract SQL solution
  const sqlMatch = chunk.match(/### C[oó]digo de Soluci[oó]n[\s\S]*?```sql\s*([\s\S]*?)```/i);
  const sql = sqlMatch ? sqlMatch[1].trim() : null;
  
  // Extract Result block
  const resultMatch = chunk.match(/#### 📊 Resultado Real[\s\S]*?```(?:text|sql)?\s*([\s\S]*?)```/i);
  const result = resultMatch ? resultMatch[1].trim() : null;
  
  const resultLines = result ? result.split('\n').length : 0;
  const hasMockNWE = chunk.includes('NWE01') || chunk.includes('NWE02') || chunk.includes('TechCorp') || chunk.includes('DataLabs');
  const hasMockAlfred = chunk.includes('Alfreds Futterkiste - Actualizado');
  const hasAnalystThinking = chunk.includes('Cómo Pensar como un Analista de Datos') || chunk.includes('Cómo pensar como un Analista');
  const hasEngineLifecycle = chunk.includes('Ciclo de Vida del Motor') || chunk.includes('Diagrama ASCII de Ejecución en el Motor');
  
  exBlocks.push({
    num: matches[i].num,
    title: matches[i].title,
    sql,
    resultLines,
    hasMockNWE,
    hasMockAlfred,
    hasAnalystThinking,
    hasEngineLifecycle,
    totalChunkLines: chunk.split('\n').length
  });
}

console.log('EXERCISE AUDIT:');
exBlocks.forEach(b => {
  console.log(`Ex ${b.num}: lines=${b.totalChunkLines}, resLines=${b.resultLines}, mockNWE=${b.hasMockNWE}, mockAlf=${b.hasMockAlfred}, analyst=${b.hasAnalystThinking}, engine=${b.hasEngineLifecycle}`);
});
