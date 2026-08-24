const fs = require('fs');

const raw = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/exercises_raw.json', 'utf8'));
console.log(`Loaded ${raw.length} exercises from raw JSON.`);
console.log('Sample Ex 1:');
console.log(raw[0].fullText.substring(0, 300));
