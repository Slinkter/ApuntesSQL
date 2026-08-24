const fs = require('fs');
const path = require('path');

const results = JSON.parse(fs.readFileSync(path.join(__dirname, 'execution_results.json'), 'utf8'));

for (const r of results) {
  console.log(`=== Pregunta ${r.num}: ${r.name} ===`);
  if (!r.success) {
    console.log(`ERROR: ${r.error}`);
  } else {
    console.log(r.output.trim());
  }
  console.log('\n');
}
