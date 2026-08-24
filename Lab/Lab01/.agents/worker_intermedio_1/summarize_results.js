const fs = require('fs');

const executed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/executed_queries.json', 'utf8'));

executed.forEach(q => {
  const lines = q.rawOutput.split('\n');
  const lastLine = lines[lines.length - 1];
  console.log(`Ex ${q.num} (${q.title}): total raw lines=${lines.length}, footer='${lastLine}'`);
});
