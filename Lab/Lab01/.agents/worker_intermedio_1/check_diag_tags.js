const fs = require('fs');
const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

const regex = /### Diagrama de Flujo \(Mermaid\)\s*```([a-zA-Z]*)/g;
let match;
let i = 0;
while ((match = regex.exec(content)) !== null) {
  i++;
  console.log(`Diagram ${i} tag: '${match[1]}'`);
}
