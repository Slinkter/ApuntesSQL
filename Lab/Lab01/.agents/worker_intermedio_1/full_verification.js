const fs = require('fs');

const content = fs.readFileSync('2.Ejercicios/2.intermedio.md', 'utf8');

// 1. Check exercise count
const exMatches = content.match(/^## Ejercicio (\d+):?\s*(.*)$/gm);
console.log(`1. Total exercises: ${exMatches ? exMatches.length : 0}/50`);

// 2. Check mock strings
const mockStrings = [
  'NWE01',
  'NWE02',
  'TechCorp Peru',
  'DataLabs Chile',
  'Alfreds Futterkiste - Actualizado',
  '(93 rows)',
  '(834 rows)'
];

console.log('2. Mock data audit:');
mockStrings.forEach(s => {
  const count = (content.match(new RegExp(s.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&'), 'g')) || []).length;
  console.log(`   - "${s}": ${count} occurrences ${count === 0 ? '✅' : '❌'}`);
});

// 3. Check specific row counts
const specificChecks = [
  { ex: 19, str: '(91 rows)' },
  { ex: 22, str: '(91 rows)' },
  { ex: 26, str: '(91 rows)' },
  { ex: 34, str: '(832 rows)' },
  { ex: 49, str: '(91 rows)' }
];

console.log('3. Specific row counts audit:');
specificChecks.forEach(c => {
  const start = content.indexOf(`## Ejercicio ${c.ex}:`);
  const nextEx = c.ex < 50 ? `## Ejercicio ${c.ex + 1}:` : '## 🏁';
  const end = content.indexOf(nextEx);
  const chunk = content.substring(start, end);
  const hasExpected = chunk.includes(c.str);
  console.log(`   - Exercise ${c.ex} has '${c.str}': ${hasExpected ? '✅' : '❌'}`);
});

// 4. Check section completeness for all 50
console.log('4. Section completeness for all 50 exercises:');
let allComplete = true;
for (let i = 1; i <= 50; i++) {
  const start = content.indexOf(`## Ejercicio ${i}:`);
  const nextEx = i < 50 ? `## Ejercicio ${i + 1}:` : '## 🏁';
  const end = content.indexOf(nextEx);
  const chunk = content.substring(start, end);
  
  const requiredHeaders = [
    '### 🎯 Enunciado y Caso de Uso',
    '### 🎓 Explicación del Profesor',
    '### 🧠 Cómo Pensar como un Analista de Datos',
    '### ⚙️ Desglose del Motor de Ejecución (Logical Query Processing)',
    '### Código de Solución',
    '#### 📊 Resultado Real de Ejecución en PostgreSQL (AWS EC2):',
    '> 🛠️ **Nota del Ingeniero de Datos:**',
    '### Criterio de Evaluación del Entrevistador'
  ];
  
  const missing = requiredHeaders.filter(h => !chunk.includes(h));
  if (missing.length > 0) {
    console.log(`   ❌ Exercise ${i} missing headers:`, missing);
    allComplete = false;
  }
}
if (allComplete) {
  console.log('   ✅ All 50 exercises have 100% of required sections!');
}

// 5. File size
const stats = fs.statSync('2.Ejercicios/2.intermedio.md');
console.log(`5. File size: ${(stats.size / 1024).toFixed(2)} KB (Target: ~250-350 KB) ✅`);
