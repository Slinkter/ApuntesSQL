const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const targetFile = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';
const content = fs.readFileSync(targetFile, 'utf8');

const regex = /### Pregunta (\d+)[\s\S]*?```sql([\s\S]*?)```/g;
let match;
let count = 0;
let passed = 0;

console.log('Extracting and running all SQL blocks from 4.examen_entrevista.md...');

while ((match = regex.exec(content)) !== null) {
  count++;
  const qNum = match[1];
  const sql = match[2].trim();
  try {
    const dbRunner = require('../db_runner.js');
    dbRunner.runSql(sql);
    console.log(`[PASS] Pregunta ${qNum}: Executed successfully.`);
    passed++;
  } catch (err) {
    console.error(`[FAIL] Pregunta ${qNum}: Error -> ${err.stderr ? err.stderr.toString() : err.message}`);
  }
}

console.log(`\nResults: ${passed} / ${count} questions executed cleanly against PostgreSQL 16.`);
