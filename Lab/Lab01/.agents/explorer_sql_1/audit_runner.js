const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01';
const ejerciciosDir = path.join(workspaceRoot, '2.Ejercicios');

const files = [
  '0.prerrequisitos.md',
  '1.basico.md',
  '2.intermedio.md',
  '3.avanzado.md',
  '4.examen_entrevista.md',
  'aws_ejercicio.sql'
];

function runQuery(sql) {
  const tmpFile = path.join(workspaceRoot, '.agents', 'explorer_sql_1', 'tmp_query.sql');
  fs.writeFileSync(tmpFile, sql, 'utf8');
  try {
    execSync(`docker cp "${tmpFile}" pg_test_audit:/tmp/tmp_query.sql`);
    const output = execSync(`docker exec pg_test_audit psql -U postgres -d northwind -f /tmp/tmp_query.sql`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    return { success: true, output };
  } catch (err) {
    return { success: false, error: (err.stderr || err.message || '').toString(), stdout: (err.stdout || '').toString() };
  }
}

const auditResults = {};

for (const file of files) {
  const filePath = path.join(ejerciciosDir, file);
  if (!fs.existsSync(filePath)) continue;
  const content = fs.readFileSync(filePath, 'utf8');
  auditResults[file] = [];

  if (file.endsWith('.sql')) {
    console.log(`Auditing SQL file: ${file}`);
    const result = runQuery(content);
    auditResults[file].push({
      blockId: 'full_file',
      sql: content,
      result
    });
    continue;
  }

  const lines = content.split('\n');
  let currentExercise = 'Intro / Setup';
  let inSql = false;
  let currentSql = [];
  let exerciseIndex = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Ejercicio') || line.startsWith('### Pregunta') || line.startsWith('## Pregunta') || line.startsWith('## ') || line.startsWith('### ')) {
      if (line.includes('Ejercicio') || line.includes('Pregunta') || line.includes('Nivel') || line.includes('P1') || line.includes('P2')) {
        currentExercise = line.trim();
      }
    }

    if (line.trim().startsWith('```sql')) {
      inSql = true;
      currentSql = [];
      continue;
    }
    if (inSql && line.trim().startsWith('```')) {
      inSql = false;
      const sqlCode = currentSql.join('\n').trim();
      if (sqlCode) {
        exerciseIndex++;
        const res = runQuery(sqlCode);
        auditResults[file].push({
          exercise: currentExercise,
          sql: sqlCode,
          line: i - currentSql.length,
          result: res
        });
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }
  }
}

fs.writeFileSync(
  path.join(workspaceRoot, '.agents', 'explorer_sql_1', 'audit_raw.json'),
  JSON.stringify(auditResults, null, 2),
  'utf8'
);
console.log('Finished raw audit. Results saved to audit_raw.json');
