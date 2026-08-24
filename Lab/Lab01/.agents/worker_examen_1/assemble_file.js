const fs = require('fs');
const path = require('path');

const targetFile = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01\\2.Ejercicios\\4.examen_entrevista.md';

// Read python files and extract the multiline string contents
function extractPyString(filename, varName) {
  const content = fs.readFileSync(path.join(__dirname, filename), 'utf8');
  const startMarker = varName + ' = """';
  const startIndex = content.indexOf(startMarker);
  if (startIndex === -1) {
    throw new Error(`Variable ${varName} not found in ${filename}`);
  }
  const stringStart = startIndex + startMarker.length;
  const endIndex = content.indexOf('"""', stringStart);
  if (endIndex === -1) {
    throw new Error(`End marker not found for ${varName} in ${filename}`);
  }
  return content.substring(stringStart, endIndex);
}

const header = extractPyString('make_examen.py', 'header');
const sec1_3 = extractPyString('sec1_3.py', 'sec1_3_text');
const sec4_6 = extractPyString('sec4_6.py', 'sec4_6_text');
const sec7_9 = extractPyString('sec7_9.py', 'sec7_9_text');

const fullDoc = header.trim() + '\n\n' + sec1_3.trim() + '\n\n' + sec4_6.trim() + '\n\n' + sec7_9.trim() + '\n';

fs.writeFileSync(targetFile, fullDoc, 'utf8');
console.log(`Successfully assembled ${targetFile}`);
console.log(`Total size: ${fullDoc.length} characters / ${fs.statSync(targetFile).size} bytes`);
