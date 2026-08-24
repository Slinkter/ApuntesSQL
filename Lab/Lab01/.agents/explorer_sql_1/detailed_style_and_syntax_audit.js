const fs = require('fs');
const path = require('path');

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

const styleAndSyntaxFindings = {};

files.forEach(file => {
  const filePath = path.join(ejerciciosDir, file);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf8');
  styleAndSyntaxFindings[file] = [];

  const lines = content.split('\n');
  let inSql = false;
  let currentSql = [];
  let sqlStartLine = 0;
  let currentHeader = 'General';

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## ') || line.startsWith('### ')) {
      currentHeader = line.replace(/^[#\s]+/, '').trim();
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
        // Check rules
        const issues = [];

        // 1. Check semicolon at the end
        if (!sqlText.endsWith(';')) {
          issues.push({ type: 'MISSING_SEMICOLON', detail: 'Query does not end with a semicolon (;)' });
        }

        // 2. Check for missing AS in aliases
        // Regex pattern: expression alias without AS (heuristic check)
        const noAsMatches = sqlText.match(/\b(COUNT\([^)]+\)|SUM\([^)]+\)|AVG\([^)]+\)|MIN\([^)]+\)|MAX\([^)]+\)|ROUND\([^)]+\))\s+([a-zA-Z_][a-zA-Z0-9_]*)/gi);
        if (noAsMatches) {
          noAsMatches.forEach(m => {
            if (!m.toUpperCase().includes(' AS ')) {
              issues.push({ type: 'MISSING_AS_ALIAS', detail: `Aggregation without explicit AS: "${m}"` });
            }
          });
        }

        // 3. Check for SQL keywords in lowercase
        const lowercaseKeywords = [];
        const mainKeywords = ['select', 'from', 'where', 'group by', 'order by', 'having', 'limit', 'offset', 'inner join', 'left join', 'right join', 'full join', 'cross join'];
        // Split by lines to avoid checking inside string literals or comments
        currentSql.forEach((sqlLine, lIdx) => {
          const trimmed = sqlLine.trim();
          if (trimmed.startsWith('--')) return;
          // check if line starts with lowercase keyword
          mainKeywords.forEach(kw => {
            const re = new RegExp(`^${kw}\\b`, 'i');
            if (re.test(trimmed) && trimmed.startsWith(kw)) {
              lowercaseKeywords.push(`Line ${sqlStartLine + lIdx}: "${kw}" should be uppercase`);
            }
          });
        });
        if (lowercaseKeywords.length > 0) {
          issues.push({ type: 'LOWERCASE_KEYWORDS', detail: lowercaseKeywords.join(', ') });
        }

        // 4. Check for syntax anomalies (quotes, backticks, MySQL functions)
        if (sqlText.includes('`')) {
          issues.push({ type: 'MYSQL_BACKTICKS', detail: 'Contains MySQL backticks (`) instead of double quotes or standard identifiers' });
        }
        if (sqlText.includes('IFNULL(')) {
          issues.push({ type: 'MYSQL_IFNULL', detail: 'Contains IFNULL() instead of standard COALESCE()' });
        }
        if (sqlText.includes("') ||")) {
          issues.push({ type: 'UNTERMINATED_QUOTE_BUG', detail: `Potential syntax error in string quote: "') ||"` });
        }

        // 5. Check table name casing / naming
        const wrongTableNames = sqlText.match(/\b(orderdetails|order_detail|orders_details|Order_Details)\b/gi);
        if (wrongTableNames) {
          issues.push({ type: 'WRONG_TABLE_NAME', detail: `Wrong table name: ${wrongTableNames.join(', ')} (should be order_details)` });
        }

        // 6. Check for "Actualizado" or mock data dependencies
        if (sqlText.includes('NWE01') || sqlText.includes('NWE02')) {
          issues.push({ type: 'MOCK_DATA_DEPENDENCY', detail: 'References mock customer IDs (NWE01, NWE02) not present in canonical Northwind schema' });
        }

        if (issues.length > 0) {
          styleAndSyntaxFindings[file].push({
            header: currentHeader,
            lineStart: sqlStartLine,
            lineEnd: i + 1,
            sql: sqlText,
            issues
          });
        }
      }
      currentSql = [];
      continue;
    }
    if (inSql) {
      currentSql.push(line);
    }
  }
});

fs.writeFileSync(
  path.join(explorerDir, 'style_and_syntax_findings.json'),
  JSON.stringify(styleAndSyntaxFindings, null, 2),
  'utf8'
);

console.log('Style and syntax audit completed!');
for (const [file, items] of Object.entries(styleAndSyntaxFindings)) {
  console.log(`\n${file}: ${items.length} items with style/syntax observations`);
  items.forEach(it => {
    console.log(`  [Line ${it.lineStart}] ${it.header}:`);
    it.issues.forEach(iss => console.log(`    - [${iss.type}] ${iss.detail}`));
  });
}
