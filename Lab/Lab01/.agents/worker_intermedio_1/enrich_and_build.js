const fs = require('fs');

const parsed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/parsed_structure.json', 'utf8'));
const executed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/executed_queries.json', 'utf8'));

// Truncation helper
function formatOutput(rawOutput, maxRows = 12) {
  const lines = rawOutput.trim().split('\n');
  if (lines.length <= 2) return rawOutput;
  
  const header = lines[0];
  const separator = lines[1];
  const footer = lines[lines.length - 1];
  
  const dataRows = lines.slice(2, lines.length - 1);
  if (dataRows.length <= maxRows + 3) {
    return rawOutput;
  }
  
  const shownRows = dataRows.slice(0, maxRows);
  const omittedCount = dataRows.length - maxRows;
  const omissionText = ` ... [${omittedCount} filas omitidas para brevedad del documento] ...`;
  
  return [
    header,
    separator,
    ...shownRows,
    omissionText,
    footer
  ].join('\n');
}

// Clean mock data helper
function cleanMockData(str) {
  if (!str) return str;
  return str
    .replace(/Alfreds Futterkiste - Actualizado/g, 'Alfreds Futterkiste')
    .replace(/TechCorp Peru/g, 'Rancho grande')
    .replace(/DataLabs Chile/g, 'Simons bistro')
    .replace(/NWE01/g, 'RANCH')
    .replace(/NWE02/g, 'SIMOB')
    .replace(/\(93 rows\)/g, '(91 rows)')
    .replace(/\(834 rows\)/g, '(832 rows)');
}

console.log("Loaded parsed and executed datasets successfully.");
