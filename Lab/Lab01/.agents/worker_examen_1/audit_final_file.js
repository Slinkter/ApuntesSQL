const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const targetFile = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';
const content = fs.readFileSync(targetFile, 'utf8');

console.log('=== AUDITING 4.examen_entrevista.md ===');
console.log(`Total lines: ${content.split('\n').length}`);
console.log(`Total bytes: ${fs.statSync(targetFile).size}`);

// Check 1: Mock data contamination
const hasNWE01 = content.includes('NWE01');
const hasNWE02 = content.includes('NWE02');
const hasActualizado = content.includes('Alfreds Futterkiste - Actualizado');
const hasActualizado2 = content.includes('- Actualizado');

console.log(`\n1. Mock data check:`);
console.log(`   - NWE01 present? ${hasNWE01}`);
console.log(`   - NWE02 present? ${hasNWE02}`);
console.log(`   - "Alfreds Futterkiste - Actualizado" present? ${hasActualizado}`);
console.log(`   - "- Actualizado" present? ${hasActualizado2}`);

if (hasNWE01 || hasNWE02 || hasActualizado || hasActualizado2) {
  console.error('FAILED: Mock data detected!');
} else {
  console.log('   PASSED: 100% clean of mock data.');
}

// Check 2: Pregunta 10
console.log(`\n2. Pregunta 10 verification:`);
const p10Section = content.substring(content.indexOf('### Pregunta 10'), content.indexOf('### Pregunta 11'));
console.log(`   - Contains PARIS? ${p10Section.includes('PARIS')}`);
console.log(`   - Contains FISSA? ${p10Section.includes('FISSA')}`);
console.log(`   - Contains (2 rows)? ${p10Section.includes('(2 rows)')}`);
console.log(`   - Contains (4 rows)? ${p10Section.includes('(4 rows)')}`);

// Check 3: Check all 30 questions exist
console.log(`\n3. Checking presence of all 30 questions:`);
let allQuestionsPresent = true;
for (let i = 1; i <= 30; i++) {
  const marker = `### Pregunta ${i}`;
  if (!content.includes(marker)) {
    console.error(`   MISSING: Pregunta ${i}`);
    allQuestionsPresent = false;
  }
}
if (allQuestionsPresent) {
  console.log('   PASSED: All 30 questions are present.');
}

// Check 4: Check 12-step pipeline references
console.log(`\n4. 12-step pipeline check:`);
console.log(`   - Contains "PIPELINE LÓGICO DE PROCESAMIENTO SQL"? ${content.includes('PIPELINE LÓGICO DE PROCESAMIENTO SQL')}`);
console.log(`   - Contains "Matriz de Visibilidad de Identificadores"? ${content.includes('Matriz de Visibilidad de Identificadores')}`);
console.log(`   - Contains "Framework Mental"? ${content.includes('Framework Mental')}`);

// Check 5: Code fence balancing
const sqlFences = (content.match(/```sql/g) || []).length;
const textFences = (content.match(/```text/g) || []).length;
const endFences = (content.match(/```\n/g) || []).length + (content.match(/```\r\n/g) || []).length;
const allFences = (content.match(/```/g) || []).length;

console.log(`\n5. Markdown formatting check:`);
console.log(`   - Total code fences: ${allFences} (Even? ${allFences % 2 === 0})`);
console.log(`   - Details tags open: ${(content.match(/<details>/g) || []).length}, close: ${(content.match(/<\/details>/g) || []).length}`);

console.log('\n=== AUDIT COMPLETE ===');
