const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');
const lines = content.split('\n');

for (let i = 0; i < lines.length; i++) {
  if (lines[i].startsWith('## Ejercicio ')) {
    console.log(`Line ${i + 1}: ${lines[i].trim()}`);
  }
}
