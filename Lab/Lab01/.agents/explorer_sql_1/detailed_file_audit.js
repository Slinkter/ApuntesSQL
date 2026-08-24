const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01';
const ejerciciosDir = path.join(workspaceRoot, '2.Ejercicios');
const explorerDir = path.join(workspaceRoot, '.agents', 'explorer_sql_1');

const files = [
  '0.prerrequisitos.md',
  '1.basico.md',
  '2.intermedio.md',
  '3.avanzado.md',
  '4.examen_entrevista.md',
  'aws_ejercicio.sql'
];

function runIndividualQuery(sql) {
  const tmpFile = path.join(explorerDir, 'single_test.sql');
  // Wrap in transaction rollback to prevent mutating DB
  const wrappedSql = `BEGIN;\n${sql}\n;\nROLLBACK;`;
  fs.writeFileSync(tmpFile, wrappedSql, 'utf8');
  try {
    execSync(`docker cp "${tmpFile}" pg_test_audit:/tmp/single_test.sql`);
    const output = execSync(`docker exec pg_test_audit psql -U postgres -d northwind -f /tmp/single_test.sql`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    const hasError = output.includes('ERROR:') || output.includes('syntax error');
    return { success: !hasError, output, error: hasError ? output.split('\n').filter(l => l.includes('ERROR:') || l.includes('LINE ')).join(' | ') : null };
  } catch (err) {
    const combined = (err.stdout || '') + '\n' + (err.stderr || '') + '\n' + err.message;
    return { success: false, output: combined, error: combined.split('\n').filter(l => l.includes('ERROR:') || l.includes('LINE ')).join(' | ') };
  }
}

const detailedReport = {};

files.forEach(file => {
  const filePath = path.join(ejerciciosDir, file);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf8');
  detailedReport[file] = [];

  if (file.endsWith('.sql')) {
    const res = runIndividualQuery(content);
    detailedReport[file].push({
      exerciseNumber: 'Full File',
      title: file,
      lineStart: 1,
      sql: content,
      res
    });
    return;
  }

  const lines = content.split('\n');
  let currentExerciseTitle = 'General';
  let inSql = false;
  let currentSql = [];
  let sqlStartLine = 0;
  let inAscii = false;
  let currentAscii = [];
  let lastItem = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Ejercicio') || line.startsWith('### Pregunta') || line.startsWith('## Pregunta') || line.startsWith('### P')) {
      currentExerciseTitle = line.replace(/^[#\s]+/, '').trim();
    }

    if (line.trim().startsWith('```sql')) {
      inSql = true;
      currentSql = [];
      sqlStartLine = i + 1;
      continue;
    }
    if (inSql && line.trim().startsWith('```')) {
      inSql = false;
      const sqlText = currentSql.join('\n').trim();
      if (sqlText) {
        const item = {
          exerciseTitle: currentExerciseTitle,
          lineStart: sqlStartLine,
          lineEnd: i + 1,
          sql: sqlText,
          expectedAscii: '',
          res: null
        };
        detailedReport[file].push(item);
        lastItem = item;
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }

    if (line.trim().startsWith('```text') || (line.trim().startsWith('```') && !inSql && lastItem && !lastItem.expectedAscii)) {
      const prevContext = lines.slice(Math.max(0, i - 4), i).join('\n');
      if (prevContext.includes('Resultado') || prevContext.includes('Output')) {
        inAscii = true;
        currentAscii = [];
        continue;
      }
    }
    if (inAscii && line.trim().startsWith('```')) {
      inAscii = false;
      if (lastItem) {
        lastItem.expectedAscii = currentAscii.join('\n').trim();
      }
      currentAscii = [];
      continue;
    }
    if (inAscii) {
      currentAscii.push(line);
    }
  }

  // Now execute each item individually
  console.log(`Auditing file: ${file} (${detailedReport[file].length} code blocks)...`);
  detailedReport[file].forEach((item, idx) => {
    item.res = runIndividualQuery(item.sql);
  });
});

fs.writeFileSync(
  path.join(explorerDir, 'detailed_audit.json'),
  JSON.stringify(detailedReport, null, 2),
  'utf8'
);

console.log('Detailed audit completed! Results saved to detailed_audit.json');
