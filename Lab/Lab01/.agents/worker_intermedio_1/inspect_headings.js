const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

const headerRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const matches = [];
while ((match = headerRegex.exec(content)) !== null) {
  matches.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

const exercises = [];

for (let i = 0; i < matches.length; i++) {
  const start = matches[i].index;
  const end = (i < matches.length - 1) ? matches[i + 1].index : content.length;
  const chunk = content.substring(start, end);
  
  // Extract parts
  const lines = chunk.split('\n');
  const titleLine = lines[0];
  
  // Check what subheadings exist
  const subheadings = lines.filter(l => l.startsWith('###') || l.startsWith('####'));
  
  exercises.push({
    num: matches[i].num,
    title: matches[i].title,
    subheadings
  });
}

console.log('SUBHEADINGS PER EXERCISE:');
exercises.slice(0, 10).forEach(e => {
  console.log(`Ex ${e.num} (${e.title}):`, e.subheadings);
});
