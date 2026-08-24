const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = 'C:\\Users\\luisj\\Github\\ApuntesSQL\\Lab\\Lab01';
const ejerciciosDir = path.join(workspaceRoot, '2.Ejercicios');
const explorerDir = path.join(workspaceRoot, '.agents', 'explorer_sql_1');

const files = [
  '0.prerrequisitos.md',
  '1.basico.md',
  '2.intermedio.md',
  '3.avanzado.md',
  '4.examen_entrevista.md',
  'aws_ejercicio.sql'
];

function runQueryDirect(sql) {
  try {
    const out = execSync(`docker exec -i pg_test_audit psql -U postgres -d northwind`, {
      input: sql,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return { ok: !out.includes('ERROR:'), out };
  } catch (e) {
    return { ok: false, out: (e.stdout || '') + '\n' + (e.stderr || '') };
  }
}

// Check Exercise 38 with fix
const ex38Fixed = `SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title || ' - ' || city AS cargo_ubicacion,
    COALESCE(region || ', ', '') || country AS ubicacion_completa
FROM employees
ORDER BY last_name;`;

console.log('Testing Exercise 38 with fix:');
console.log(runQueryDirect(ex38Fixed).out);
