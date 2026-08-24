const fs = require('fs');

const parsed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/parsed_structure.json', 'utf8'));

let missing = 0;
parsed.forEach(p => {
  const missingFields = [];
  if (!p.prof) missingFields.push('prof');
  if (!p.opt) missingFields.push('opt');
  if (!p.diagram) missingFields.push('diagram');
  if (!p.sql) missingFields.push('sql');
  if (!p.nota) missingFields.push('nota');
  if (!p.crit) missingFields.push('crit');
  if (missingFields.length > 0) {
    console.log(`Ex ${p.num} missing:`, missingFields);
    missing++;
  }
});
console.log(`Total exercises with missing basic fields: ${missing}/50`);
