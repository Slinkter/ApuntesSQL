const fs = require('fs');
const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

const diagRegex = /### Diagrama[^\n]*/g;
const matches = content.match(diagRegex);
console.log('Diagram headings count:', matches ? matches.length : 0);
console.log('Headings:', matches);
