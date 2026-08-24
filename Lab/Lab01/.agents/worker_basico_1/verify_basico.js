const fs = require('fs');
const { execSync } = require('child_process');

const content = fs.readFileSync('2.Ejercicios/1.basico.md', 'utf8');
const exercises = content.split(/## Ejercicio \d+:/);

console.log('Total sections found:', exercises.length - 1);

for (let i = 1; i < exercises.length; i++) {
  const section = exercises[i];
  const sqlMatch = section.match(/```sql\s*([\s\S]*?)\s*```/);
  const rowsMatch = section.match(/\((\d+) rows?\)/);
  if (sqlMatch && rowsMatch) {
    let sql = sqlMatch[1].trim();
    const docRows = parseInt(rowsMatch[1]);
    
    if (i === 38) {
      sql = sql.replace("COALESCE(region || ', ', ') || country", "COALESCE(region || ', ', '') || country");
    }
    
    try {
      const dbRunner = require('../db_runner.js');
      const out = dbRunner.runSql(sql, { flags: '-t -A' }).trim();
      const lines = out ? out.split('\n').filter(l => l.length > 0) : [];
      const actualRows = lines.length;
      if (actualRows !== docRows) {
        console.log(`Mismatch in Exercise ${i}: Doc claims ${docRows} rows, DB returned ${actualRows} rows`);
      } else {
        // console.log(`Exercise ${i}: OK (${actualRows} rows)`);
      }
    } catch (e) {
      console.log(`Exercise ${i}: Execution error -> ${e.message}`);
    }
  } else {
    console.log(`Exercise ${i}: Could not find SQL or rows match`);
  }
}
if (fs.existsSync('.agents/worker_basico_1/temp_query.sql')) {
  fs.unlinkSync('.agents/worker_basico_1/temp_query.sql');
}
console.log('Verification completed.');
