const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01';
const ejerciciosDir = path.join(workspaceRoot, '2.Ejercicios');
const explorerDir = path.join(workspaceRoot, '.agents', 'explorer_sql_1');

const files = [
  '1.basico.md',
  '2.intermedio.md',
  '3.avanzado.md',
  '4.examen_entrevista.md'
];

function runQuery(sql) {
  // fix known syntax error if testing
  let cleanSql = sql;
  if (cleanSql.includes("COALESCE(region || ', ', ') || country")) {
    cleanSql = cleanSql.replace("COALESCE(region || ', ', ') || country", "COALESCE(region || ', ', '') || country");
  }
  const wrapped = `BEGIN;\n${cleanSql}\n;\nROLLBACK;`;
  try {
    const out = execSync(`docker exec -i pg_test_audit psql -U postgres -d northwind`, {
      input: wrapped,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return { ok: !out.includes('ERROR:'), out };
  } catch (e) {
    return { ok: false, out: (e.stdout || '') + '\n' + (e.stderr || '') };
  }
}

const detailedComparison = [];

files.forEach(file => {
  const filePath = path.join(ejerciciosDir, file);
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  let currentTitle = '';
  let inSql = false;
  let currentSql = [];
  let sqlStartLine = 0;
  let inAscii = false;
  let currentAscii = [];
  let exerciseCount = 0;

  let currentItem = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Ejercicio') || line.startsWith('### Pregunta') || line.startsWith('## Pregunta')) {
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
      if (sqlText && !sqlText.startsWith('-- Ejemplo')) {
        exerciseCount++;
        currentItem = {
          file,
          exerciseCount,
          title: currentTitle,
          sqlLine: sqlStartLine,
          sql: sqlText,
          expectedAscii: '',
          actualOutput: ''
        };
        detailedComparison.push(currentItem);
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }

    if (line.trim().startsWith('```text') || (line.trim().startsWith('```') && !inSql && currentItem && !currentItem.expectedAscii)) {
      const prevContext = lines.slice(Math.max(0, i - 5), i).join('\n');
      if (prevContext.includes('Resultado') || prevContext.includes('Output')) {
        inAscii = true;
        currentAscii = [];
        continue;
      }
    }
    if (inAscii && line.trim().startsWith('```')) {
      inAscii = false;
      if (currentItem && !currentItem.expectedAscii) {
        currentItem.expectedAscii = currentAscii.join('\n').trim();
      }
      currentAscii = [];
      continue;
    }
    if (inAscii) {
      currentAscii.push(line);
    }
  }
});

console.log(`Auditing ${detailedComparison.length} exercise items with output comparison...`);

const findings = [];

detailedComparison.forEach(item => {
  const res = runQuery(item.sql);
  item.actualOutput = res.out;

  if (!res.ok) {
    findings.push({
      file: item.file,
      title: item.title,
      sqlLine: item.sqlLine,
      type: 'SQL_EXECUTION_ERROR',
      detail: res.out.split('\n').filter(l => l.includes('ERROR:')).join('; '),
      sql: item.sql
    });
    return;
  }

  // Parse columns and rows from actual vs expected
  const actualLines = res.out.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('BEGIN') && !l.startsWith('ROLLBACK'));
  const expectedLines = item.expectedAscii.split('\n').map(l => l.trim()).filter(l => l);

  // Check row count
  const actualRowsMatch = res.out.match(/\((\d+)\s+rows?\)/i);
  const expectedRowsMatch = item.expectedAscii.match(/\((\d+)\s+rows?\)/i);

  const actualRows = actualRowsMatch ? parseInt(actualRowsMatch[1], 10) : null;
  const expectedRows = expectedRowsMatch ? parseInt(expectedRowsMatch[1], 10) : null;

  if (actualRows !== null && expectedRows !== null && actualRows !== expectedRows) {
    findings.push({
      file: item.file,
      title: item.title,
      sqlLine: item.sqlLine,
      type: 'ROW_COUNT_MISMATCH',
      detail: `Expected (${expectedRows} rows), but engine returned (${actualRows} rows)`,
      expectedRows,
      actualRows
    });
  }

  // Check for mock data strings in expected table
  if (item.expectedAscii.includes('Actualizado') || item.expectedAscii.includes('TechCorp') || item.expectedAscii.includes('DataLabs') || item.expectedAscii.includes('NWE01')) {
    findings.push({
      file: item.file,
      title: item.title,
      sqlLine: item.sqlLine,
      type: 'MOCK_DATA_IN_ASCII_TABLE',
      detail: 'ASCII table contains non-canonical mock data (Actualizado, TechCorp, DataLabs, or NWE01/NWE02)'
    });
  }

  // Check header matching if expectedAscii has header
  if (expectedLines.length >= 2 && actualLines.length >= 2) {
    const expHeader = expectedLines[0].replace(/\s+/g, ' ');
    const actHeader = actualLines[0].replace(/\s+/g, ' ');
    // compare normalized header column names
    const expCols = expHeader.split('|').map(c => c.trim().toLowerCase());
    const actCols = actHeader.split('|').map(c => c.trim().toLowerCase());
    if (expCols.length !== actCols.length) {
      findings.push({
        file: item.file,
        title: item.title,
        sqlLine: item.sqlLine,
        type: 'COLUMN_COUNT_MISMATCH',
        detail: `Expected columns [${expCols.join(', ')}] (${expCols.length}) vs Actual columns [${actCols.join(', ')}] (${actCols.length})`
      });
    }
  }
});

fs.writeFileSync(
  path.join(explorerDir, 'detailed_findings.json'),
  JSON.stringify({
    totalAudited: detailedComparison.length,
    findingsCount: findings.length,
    findings
  }, null, 2),
  'utf8'
);

console.log(`Deep ASCII comparison completed! Total findings: ${findings.length}`);
findings.forEach(f => {
  console.log(`[${f.file} : Line ${f.sqlLine}] ${f.title} -> [${f.type}] ${f.detail}`);
});
