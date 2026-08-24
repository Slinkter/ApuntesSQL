const fs = require('fs');
const executed = JSON.parse(fs.readFileSync('.agents/worker_intermedio_1/executed_queries.json', 'utf8'));

executed.forEach(q => {
  console.log(`\n=================== EXERCISE ${q.num}: ${q.title} ===================`);
  console.log(q.sql);
});
