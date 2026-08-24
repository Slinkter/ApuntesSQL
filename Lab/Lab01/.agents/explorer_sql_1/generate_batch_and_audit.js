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

const allQueries = [];

files.forEach(file => {
  const filePath = path.join(ejerciciosDir, file);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf8');

  if (file.endsWith('.sql')) {
    allQueries.push({
      file,
      id: `${file}_full`,
      title: 'Full SQL File',
      sql: content,
      expectedAscii: ''
    });
    return;
  }

  const lines = content.split('\n');
  let currentHeader = 'General';
  let inSql = false;
  let currentSql = [];
  let inAscii = false;
  let currentAscii = [];
  let queryCountInFile = 0;
  let lastSqlItem = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Ejercicio') || line.startsWith('### Pregunta') || line.startsWith('## Pregunta') || line.startsWith('### P')) {
      currentHeader = line.replace(/^[#\s]+/, '').trim();
    }

    if (line.trim().startsWith('```sql')) {
      inSql = true;
      currentSql = [];
      continue;
    }
    if (inSql && line.trim().startsWith('```')) {
      inSql = false;
      const sqlText = currentSql.join('\n').trim();
      if (sqlText) {
        queryCountInFile++;
        const qId = `${file}_q${queryCountInFile}`;
        lastSqlItem = {
          file,
          id: qId,
          title: currentHeader,
          line: i - currentSql.length,
          sql: sqlText,
          expectedAscii: ''
        };
        allQueries.push(lastSqlItem);
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }

    // Capture ASCII result table if immediately follows
    if (line.trim().startsWith('```text') || line.trim().startsWith('```') && !inSql && lastSqlItem && !lastSqlItem.expectedAscii) {
      // Check if previous lines indicated Result
      const prevContext = lines.slice(Math.max(0, i - 4), i).join('\n');
      if (prevContext.includes('Resultado') || prevContext.includes('Output')) {
        inAscii = true;
        currentAscii = [];
        continue;
      }
    }
    if (inAscii && line.trim().startsWith('```')) {
      inAscii = false;
      if (lastSqlItem) {
        lastSqlItem.expectedAscii = currentAscii.join('\n').trim();
      }
      currentAscii = [];
      continue;
    }
    if (inAscii) {
      currentAscii.push(line);
    }
  }
});

console.log(`Total queries extracted: ${allQueries.length}`);

// Generate batch SQL script with delimiters
let batchSql = '\\set ON_ERROR_STOP off\n\\timing off\n';

allQueries.forEach((q, idx) => {
  batchSql += `\\echo ===DELIM_START_${idx}===\n`;
  batchSql += `${q.sql}\n`;
  if (!q.sql.trim().endsWith(';')) {
    batchSql += ';\n';
  }
  batchSql += `\\echo ===DELIM_END_${idx}===\n`;
});

const batchFile = path.join(explorerDir, 'batch_all.sql');
fs.writeFileSync(batchFile, batchSql, 'utf8');

// Copy and run inside docker
console.log('Copying batch file to postgres container...');
execSync(`docker cp "${batchFile}" pg_test_audit:/tmp/batch_all.sql`);

console.log('Executing batch in PostgreSQL...');
let psqlOutput = '';
try {
  psqlOutput = execSync(`docker exec pg_test_audit psql -U postgres -d northwind -f /tmp/batch_all.sql`, {
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024
  });
} catch (e) {
  psqlOutput = (e.stdout || '') + '\n' + (e.stderr || '');
}

console.log('Parsing results...');
const auditReport = [];

allQueries.forEach((q, idx) => {
  const startMarker = `===DELIM_START_${idx}===`;
  const endMarker = `===DELIM_END_${idx}===`;

  const sIdx = psqlOutput.indexOf(startMarker);
  const eIdx = psqlOutput.indexOf(endMarker);

  let rawOutput = '';
  if (sIdx !== -1 && eIdx !== -1) {
    rawOutput = psqlOutput.substring(sIdx + startMarker.length, eIdx).trim();
  } else {
    rawOutput = 'ERROR: Marker not found in output';
  }

  const isError = rawOutput.includes('ERROR:') || rawOutput.includes('syntax error');
  
  // Extract row count from output (e.g. (10 rows) or (1 row) or count 830)
  const rowsMatch = rawOutput.match(/\((\d+)\s+rows?\)/i);
  const actualRowCount = rowsMatch ? parseInt(rowsMatch[1], 10) : null;

  // Extract expected row count from expectedAscii
  const expRowsMatch = q.expectedAscii.match(/\((\d+)\s+rows?\)/i);
  const expectedRowCount = expRowsMatch ? parseInt(expRowsMatch[1], 10) : null;

  const rowCountMismatch = (actualRowCount !== null && expectedRowCount !== null && actualRowCount !== expectedRowCount);

  auditReport.push({
    index: idx,
    id: q.id,
    file: q.file,
    title: q.title,
    line: q.line,
    sql: q.sql,
    isError,
    errorMessage: isError ? rawOutput.split('\n').filter(l => l.includes('ERROR:')).join(' | ') : null,
    actualRowCount,
    expectedRowCount,
    rowCountMismatch,
    rawOutput: rawOutput.slice(0, 1000), // First 1000 chars
    expectedAscii: q.expectedAscii.slice(0, 1000)
  });
});

fs.writeFileSync(
  path.join(explorerDir, 'audit_report.json'),
  JSON.stringify(auditReport, null, 2),
  'utf8'
);

const errors = auditReport.filter(r => r.isError);
const rowMismatches = auditReport.filter(r => r.rowCountMismatch);

console.log(`=== AUDIT SUMMARY ===`);
console.log(`Total queries tested: ${auditReport.length}`);
console.log(`SQL Errors: ${errors.length}`);
console.log(`Row count mismatches: ${rowMismatches.length}`);

fs.writeFileSync(
  path.join(explorerDir, 'audit_summary.json'),
  JSON.stringify({
    total: auditReport.length,
    errorsCount: errors.length,
    errors,
    rowMismatchesCount: rowMismatches.length,
    rowMismatches
  }, null, 2),
  'utf8'
);
