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

function runQueryClean(sql) {
  // Always wrap in BEGIN ... ROLLBACK to never pollute state
  const cleanSql = `BEGIN;\n${sql}\n;\nROLLBACK;`;
  try {
    const output = execSync(`docker exec -i pg_test_audit psql -U postgres -d northwind`, {
      input: cleanSql,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    const hasError = output.includes('ERROR:') || output.includes('syntax error');
    return {
      success: !hasError,
      output,
      error: hasError ? output.split('\n').filter(l => l.includes('ERROR:') || l.includes('LINE ')).join(' | ') : null
    };
  } catch (err) {
    const combined = (err.stdout || '') + '\n' + (err.stderr || '') + '\n' + err.message;
    return {
      success: false,
      output: combined,
      error: combined.split('\n').filter(l => l.includes('ERROR:') || l.includes('LINE ')).join(' | ')
    };
  }
}

const auditReport = {};

files.forEach(file => {
  const filePath = path.join(ejerciciosDir, file);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf8');
  auditReport[file] = [];

  if (file.endsWith('.sql')) {
    const res = runQueryClean(content);
    auditReport[file].push({
      itemNumber: 1,
      title: file,
      line: 1,
      sql: content,
      expectedAscii: '',
      res
    });
    return;
  }

  const lines = content.split('\n');
  let currentTitle = 'General';
  let inSql = false;
  let currentSql = [];
  let sqlStartLine = 0;
  let inAscii = false;
  let currentAscii = [];
  let lastItem = null;
  let count = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Ejercicio') || line.startsWith('### Pregunta') || line.startsWith('## Pregunta') || line.startsWith('### P')) {
      currentTitle = line.replace(/^[#\s]+/, '').trim();
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
        count++;
        const item = {
          itemNumber: count,
          title: currentTitle,
          line: sqlStartLine,
          sql: sqlText,
          expectedAscii: '',
          res: null
        };
        auditReport[file].push(item);
        lastItem = item;
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }

    if (line.trim().startsWith('```text') || (line.trim().startsWith('```') && !inSql && lastItem && !lastItem.expectedAscii)) {
      const prevContext = lines.slice(Math.max(0, i - 5), i).join('\n');
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

  console.log(`Testing ${file} (${auditReport[file].length} queries)...`);
  auditReport[file].forEach(item => {
    item.res = runQueryClean(item.sql);
  });
});

fs.writeFileSync(
  path.join(explorerDir, 'clean_audit_results.json'),
  JSON.stringify(auditReport, null, 2),
  'utf8'
);

console.log('Clean audit complete!');
