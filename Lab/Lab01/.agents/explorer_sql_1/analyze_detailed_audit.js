const fs = require('fs');
const path = require('path');

const explorerDir = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\.agents\\explorer_sql_1';
const raw = JSON.parse(fs.readFileSync(path.join(explorerDir, 'detailed_audit.json'), 'utf8'));

const analysis = {
  summary: {},
  errorsByFile: {},
  outputMismatchByFile: {},
  cleanQueriesByFile: {}
};

for (const [file, items] of Object.entries(raw)) {
  analysis.errorsByFile[file] = [];
  analysis.outputMismatchByFile[file] = [];
  analysis.cleanQueriesByFile[file] = [];

  items.forEach((item, idx) => {
    const isError = !item.res || !item.res.success;
    const output = (item.res && item.res.output) || '';
    const errorStr = (item.res && item.res.error) || '';
    const expectedAscii = item.expectedAscii || '';
    
    // Extract actual row count
    const rowsMatch = output.match(/\((\d+)\s+rows?\)/i);
    const actualRows = rowsMatch ? parseInt(rowsMatch[1], 10) : (output.includes('SELECT 1') ? 1 : null);

    // Extract expected row count from ASCII table
    const expMatch = expectedAscii.match(/\((\d+)\s+rows?\)/i);
    const expectedRows = expMatch ? parseInt(expMatch[1], 10) : null;

    const rowMismatch = (actualRows !== null && expectedRows !== null && actualRows !== expectedRows);

    const record = {
      index: idx + 1,
      title: item.exerciseTitle || item.title || `Item ${idx+1}`,
      lineStart: item.lineStart,
      lineEnd: item.lineEnd,
      sql: item.sql,
      isError,
      error: errorStr,
      actualRows,
      expectedRows,
      rowMismatch,
      rawOutputSnippet: output.slice(0, 400),
      expectedAsciiSnippet: expectedAscii.slice(0, 400)
    };

    if (isError) {
      analysis.errorsByFile[file].push(record);
    } else if (rowMismatch) {
      analysis.outputMismatchByFile[file].push(record);
    } else {
      analysis.cleanQueriesByFile[file].push(record);
    }
  });

  analysis.summary[file] = {
    total: items.length,
    errors: analysis.errorsByFile[file].length,
    mismatches: analysis.outputMismatchByFile[file].length,
    clean: analysis.cleanQueriesByFile[file].length
  };
}

fs.writeFileSync(
  path.join(explorerDir, 'analysis_summary.json'),
  JSON.stringify(analysis, null, 2),
  'utf8'
);

console.log('=== ANALYSIS SUMMARY ===');
console.log(JSON.stringify(analysis.summary, null, 2));

// Print all errors
for (const [file, errs] of Object.entries(analysis.errorsByFile)) {
  if (errs.length > 0) {
    console.log(`\n========================================`);
    console.log(`--- ERRORS IN ${file} (${errs.length}) ---`);
    console.log(`========================================`);
    errs.forEach(e => {
      console.log(`\n[Line ${e.lineStart}] ${e.title}:`);
      console.log(`SQL Snippet:\n${e.sql}\n`);
      console.log(`ERROR:\n${e.error}`);
    });
  }
}

// Print all mismatches
for (const [file, mismatches] of Object.entries(analysis.outputMismatchByFile)) {
  if (mismatches.length > 0) {
    console.log(`\n========================================`);
    console.log(`--- ROW COUNT MISMATCHES IN ${file} (${mismatches.length}) ---`);
    console.log(`========================================`);
    mismatches.forEach(m => {
      console.log(`\n[Line ${m.lineStart}] ${m.title}: Expected (${m.expectedRows} rows), Got (${m.actualRows} rows)`);
      console.log(`SQL:\n${m.sql.split('\n').slice(0, 5).join('\n')}`);
    });
  }
}
