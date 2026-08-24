const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');
const lines = content.split('\n');

console.log(`Total lines: ${lines.length}`);
console.log(`Total bytes: ${Buffer.byteLength(content, 'utf8')}`);

// Find all Exercise headers
const exerciseRegex = /^## Ejercicio (\d+):?\s*(.*)$/gm;
let match;
const exercises = [];
while ((match = exerciseRegex.exec(content)) !== null) {
  exercises.push({ num: parseInt(match[1]), title: match[2], index: match.index });
}

console.log(`Found ${exercises.length} exercises.`);
exercises.forEach(e => console.log(`Ex ${e.num}: ${e.title}`));
