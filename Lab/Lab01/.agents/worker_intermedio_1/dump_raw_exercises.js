const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

const headerRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const matches = [];
while ((match = headerRegex.exec(content)) !== null) {
  matches.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

const exData = [];

for (let i = 0; i < matches.length; i++) {
  const start = matches[i].index;
  const end = (i < matches.length - 1) ? matches[i + 1].index : content.length;
  const chunk = content.substring(start, end).trim();
  
  exData.push({
    num: matches[i].num,
    title: matches[i].title,
    fullText: chunk
  });
}

fs.writeFileSync('.agents/worker_intermedio_1/exercises_raw.json', JSON.stringify(exData, null, 2), 'utf8');
console.log(`Saved ${exData.length} raw exercises.`);
