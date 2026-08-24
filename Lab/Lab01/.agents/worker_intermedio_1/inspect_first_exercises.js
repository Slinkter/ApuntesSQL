const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// Parse exercises
const headerRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const matches = [];
while ((match = headerRegex.exec(content)) !== null) {
  matches.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

for (let i = 0; i < 5; i++) {
  const start = matches[i].index;
  const end = (i < matches.length - 1) ? matches[i + 1].index : content.length;
  console.log(`=== EXERCISE ${matches[i].num}: ${matches[i].title} ===`);
  console.log(content.substring(start, end).trim());
  console.log('\n----------------------------------------\n');
}
