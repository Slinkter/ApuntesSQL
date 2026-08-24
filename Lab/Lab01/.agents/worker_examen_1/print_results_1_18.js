const fs = require('fs');
const path = require('path');

const results = JSON.parse(fs.readFileSync(path.join(__dirname, 'execution_results.json'), 'utf8'));

for (let i = 0; i < 18; i++) {
  const r = results[i];
  console.log(`=== Pregunta ${r.num}: ${r.name} ===`);
  if (!r.success) {
    console.log(`ERROR: ${r.error}`);
  } else {
    console.log(r.output.trim());
  }
  console.log('\n');
}
