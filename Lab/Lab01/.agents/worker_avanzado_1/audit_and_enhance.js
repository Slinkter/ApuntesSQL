const fs = require('fs');
const { execSync } = require('child_process');

const content = fs.readFileSync('2.Ejercicios/3.avanzado.md', 'utf8').replace(/\r\n/g, '\n');
const sections = content.split(/\n## Ejercicio /);

console.log('Total exercises:', sections.length - 1);

for (let i = 1; i < sections.length; i++) {
  const ex = sections[i];
  const title = ex.split('\n')[0].trim();
  const sqlMatch = ex.match(/```sql\n([\s\S]*?)\n```/);
  if (!sqlMatch) {
    console.log(`Ex ${i}: No SQL`);
    continue;
  }
  let sql = sqlMatch[1].trim();

  // If exercise 10, clean mock data
  if (i === 10) {
    sql = `WITH datos_nuevos (customer_id, company_name, contact_name, city, country) AS (
    VALUES
        ('NEW01', 'TechCorp Global', 'Carlos Garcia', 'Berlin', 'Germany'),
        ('NEW02', 'DataLabs International', 'Ana Soto', 'London', 'UK'),
        ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Berlin', 'Germany')
)
INSERT INTO customers (customer_id, company_name, contact_name, city, country)
SELECT customer_id, company_name, contact_name, city, country
FROM datos_nuevos
ON CONFLICT (customer_id) DO UPDATE SET
    company_name = EXCLUDED.company_name,
    contact_name = EXCLUDED.contact_name,
    city = EXCLUDED.city,
    country = EXCLUDED.country
RETURNING customer_id, company_name, (xmax = 0) AS fue_insertado;`;
  }

  let wrapper = 'BEGIN;\n' + sql + ';\nROLLBACK;';
  fs.writeFileSync('temp_test.sql', wrapper);
  try {
    execSync('docker cp temp_test.sql pg_architect_lab:/tmp/temp_test.sql');
    const out = execSync('docker exec pg_architect_lab psql -U slinkter -d northwind -f /tmp/temp_test.sql', { encoding: 'utf8' });
    const cleanOut = out.replace(/^BEGIN\n/, '').replace(/\nROLLBACK\n?$/, '').trim();
    const rowsMatch = cleanOut.match(/\((\d+)\s+rows?\)/);
    const rowCount = rowsMatch ? parseInt(rowsMatch[1], 10) : 0;
    console.log(`Ex ${String(i).padStart(2, '0')} | ${title.padEnd(45).substring(0, 45)} | Rows: ${String(rowCount).padStart(4)}`);
  } catch (err) {
    console.log(`Ex ${String(i).padStart(2, '0')} | ${title.padEnd(45).substring(0, 45)} | ERR: ${err.message}`);
  }
}
if (fs.existsSync('temp_test.sql')) fs.unlinkSync('temp_test.sql');
