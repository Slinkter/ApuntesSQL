const { execSync } = require('child_process');
const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// Extract all SQL blocks
const sqlRegex = /```sql\s*([\s\S]*?)```/g;
let match;
let count = 0;
let errors = 0;

while ((match = sqlRegex.exec(content)) !== null) {
  count++;
  const sql = match[1].trim();
  try {
    const dbRunner = require('../db_runner.js');
    dbRunner.runSql(sql);
  } catch (err) {
    console.error(`❌ SQL Block ${count} failed:`, err.message);
    errors++;
  }
}

console.log(`Executed ${count} SQL blocks. Errors: ${errors}`);
if (errors === 0) {
  console.log('✅ 100% of SQL blocks in 2.Ejercicios/2.intermedio.md are valid and executable!');
}
