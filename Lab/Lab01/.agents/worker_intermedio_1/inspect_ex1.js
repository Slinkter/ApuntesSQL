const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// Find sections in Exercise 1
const ex1Match = content.substring(content.indexOf('## Ejercicio 1:'), content.indexOf('## Ejercicio 2:'));
console.log('--- EXERCISE 1 STRUCTURE ---');
console.log(ex1Match);
