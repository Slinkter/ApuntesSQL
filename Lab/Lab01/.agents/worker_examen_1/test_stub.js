const fs = require('fs');
const path = require('path');

const targetPath = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';

const fileContent = fs.readFileSync(path.join(__dirname, 'build_full_examen.js'), 'utf8');
