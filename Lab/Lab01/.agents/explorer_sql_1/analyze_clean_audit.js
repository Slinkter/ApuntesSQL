const fs = require('fs');
const path = require('path');

const explorerDir = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\.agents\\explorer_sql_1';
const raw = JSON.parse(fs.readFileSync(path.join(explorerDir, 'clean_audit_results.json'), 'utf8'));

const analysis = {
  summary: {},
  errors: [],
  mismatches: [],
  clean: []
};

for (const [file, items] of Object.entries(raw)) {
  let fileErrors = 0;
  let fileMismatches = 0;
  let fileClean = 0;

  items.forEach((item, idx) => {
    const isError = !item.res || !item.res.success;
    const output = (item.res && item.res.output) || '';
    const errorStr = (item.res && item.res.error) || '';
    const expectedAscii = item.expectedAscii || '';

    // Extract actual row count from output
    const rowsMatch = output.match(/\((\d+)\s+rows?\)/i);
    const actualRows = rowsMatch ? parseInt(rowsMatch[1], 10) : (output.includes('SELECT 1') ? 1 : null);

    // Extract expected row count from expectedAscii
    const expMatch = expectedAscii.match(/\((\d+)\s+rows?\)/i);
    const expectedRows = expMatch ? parseInt(expMatch[1], 10) : null;

    const rowMismatch = (actualRows !== null && expectedRows !== null && actualRows !== expectedRows);

    const record = {
      file,
      itemNumber: idx + 1,
      title: item.title,
      line: item.line,
      sql: item.sql,
      isError,
      error: errorStr,
      actualRows,
      expectedRows,
      rowMismatch,
      actualOutput: output,
      expectedAscii: expectedAscii
    };

    if (isError) {
      fileErrors++;
      analysis.errors.push(record);
    } else if (rowMismatch) {
      fileMismatches++;
      analysis.mismatches.push(record);
    } else {
      fileClean++;
      analysis.clean.push(record);
    }
  });

  analysis.summary[file] = {
    total: items.length,
    errors: fileErrors,
    mismatches: fileMismatches,
    clean: fileClean
  };
}

fs.writeFileSync(
  path.join(explorerDir, 'clean_analysis_summary.json'),
  JSON.stringify(analysis, null, 2),
  'utf8'
);

console.log('=== CLEAN DB ANALYSIS SUMMARY ===');
console.log(JSON.stringify(analysis.summary, null, 2));

console.log(`\nTOTAL ERRORS: ${analysis.errors.length}`);
analysis.errors.forEach(e => {
  console.log(`\n[${e.file} : Line ${e.line}] ${e.title}`);
  console.log(`SQL:\n${e.sql}\n`);
  console.log(`ERROR:\n${e.error}`);
});

console.log(`\nTOTAL ROW MISMATCHES: ${analysis.mismatches.length}`);
analysis.mismatches.forEach(m => {
  console.log(`\n[${m.file} : Line ${m.line}] ${m.title}`);
  console.log(`  Expected rows: ${m.expectedRows} | Actual rows: ${m.actualRows}`);
  console.log(`SQL:\n${m.sql.split('\n').slice(0, 3).join('\n')}`);
});
