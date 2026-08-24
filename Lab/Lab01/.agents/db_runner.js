const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

let ec2Ip = null;
try {
  const cmd = `aws ec2 describe-instances --filters "Name=tag:Name,Values=postgres-northwind-lab" "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].PublicIpAddress" --output text`;
  const fullCmd = `$env:AWS_DEFAULT_REGION="us-east-2"; ${cmd}`;
  
  const out = execSync(fullCmd, { shell: 'powershell.exe', encoding: 'utf8' }).trim();
  if (out && out !== 'None' && out.match(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)) {
    ec2Ip = out;
  }
} catch (e) {
  // Ignore and fall back to local
}

function runSql(sqlCode, options = {}) {
  const flags = options.flags || '';
  if (ec2Ip) {
    const sshKey = 'C:/Users/luisj/Github/ApuntesSQL/Credenciales/key_u_docker.pem';
    const cmd = `ssh -o StrictHostKeyChecking=no -i "${sshKey}" ec2-user@${ec2Ip} "docker exec -i pg_architect_lab psql -U slinkter -d northwind ${flags}"`;
    return execSync(cmd, { input: sqlCode, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
  } else {
    const cmd = `docker exec -i pg_architect_lab psql -U slinkter -d northwind ${flags}`;
    return execSync(cmd, { input: sqlCode, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
  }
}

module.exports = {
  ec2Ip,
  runSql
};
