const r = require('./db_runner.js');

const sql = `
DELETE FROM customers WHERE customer_id IN ('NWE01', 'NWE02');
UPDATE customers SET company_name = 'Alfreds Futterkiste' WHERE customer_id = 'ALFKI';
`;

try {
  const result = r.runSql(sql);
  console.log('Cleanup result:');
  console.log(result);
} catch (e) {
  console.error('Error during cleanup:', e.message);
}
