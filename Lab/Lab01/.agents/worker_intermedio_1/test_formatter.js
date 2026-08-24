const fs = require('fs');

const executed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/executed_queries.json', 'utf8'));

function formatOutput(rawOutput, maxRows = 12) {
  const lines = rawOutput.trim().split('\n');
  if (lines.length <= 2) return rawOutput; // empty or single line
  
  const header = lines[0];
  const separator = lines[1];
  const footer = lines[lines.length - 1]; // e.g. (55 rows)
  
  const dataRows = lines.slice(2, lines.length - 1);
  if (dataRows.length <= maxRows + 3) {
    return rawOutput; // small enough, keep full
  }
  
  const shownRows = dataRows.slice(0, maxRows);
  const omittedCount = dataRows.length - maxRows;
  
  // Format omission notice
  const sepWidth = separator.length;
  const omissionText = `... [${omittedCount} filas omitidas para brevedad del documento] ...`;
  
  return [
    header,
    separator,
    ...shownRows,
    omissionText,
    footer
  ].join('\n');
}

executed.forEach(q => {
  const formatted = formatOutput(q.rawOutput, 12);
  const flines = formatted.split('\n').length;
  console.log(`Ex ${q.num}: originalLines=${q.rawOutput.split('\n').length} -> formattedLines=${flines}`);
});
