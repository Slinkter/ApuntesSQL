const { execSync } = require('child_process');
const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// Parse exercises
const headerRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const matches = [];
while ((match = headerRegex.exec(content)) !== null) {
  matches.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

const queryResults = [];

for (let i = 0; i < matches.length; i++) {
  const start = matches[i].index;
  const end = (i < matches.length - 1) ? matches[i + 1].index : content.length;
  const chunk = content.substring(start, end);
  
  const sqlMatch = chunk.match(/### C[oó]digo de Soluci[oó]n[\s\S]*?```sql\s*([\s\S]*?)```/i);
  if (!sqlMatch) {
    console.error(`No SQL found for Ex ${matches[i].num}`);
    continue;
  }
  
  let sql = sqlMatch[1].trim();
  
  // Save sql to temp file
  fs.writeFileSync('.agents/worker_intermedio_1/temp_query.sql', sql, 'utf8');
  
  try {
    const psqlOutput = execSync(
      'docker exec -i pg_architect_lab psql -U slinkter -d northwind -f -',
      { input: sql, encoding: 'utf8' }
    );
    queryResults.push({
      num: matches[i].num,
      title: matches[i].title,
      sql,
      success: true,
      rawOutput: psqlOutput.trim()
    });
  } catch (err) {
    console.error(`Error in Ex ${matches[i].num}:`, err.message);
    queryResults.push({
      num: matches[i].num,
      title: matches[i].title,
      sql,
      success: false,
      error: err.message
    });
  }
}

console.log(`Audited ${queryResults.length} queries. Success: ${queryResults.filter(q => q.success).length}/${queryResults.length}`);
fs.writeFileSync('.agents/worker_intermedio_1/executed_queries.json', JSON.stringify(queryResults, null, 2), 'utf8');
