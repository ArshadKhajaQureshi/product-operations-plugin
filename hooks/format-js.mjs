// hooks/format-js.mjs
// Fires after every Write or Edit tool call.
// Runs Prettier on JavaScript and JSON files.
import { execSync } from 'child_process';

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const event = JSON.parse(Buffer.concat(chunks).toString());
const file  = event?.tool_input?.file_path ?? '';

if (!file || !/\.(js|jsx|ts|tsx|json|md)$/.test(file)) process.exit(0);

try {
  execSync(`npx prettier --write "${file}" --log-level silent`, { stdio: 'pipe' });
  process.stdout.write(JSON.stringify({ additionalContext: `Formatted: ${file}` }));
} catch {
  process.stdout.write(JSON.stringify({
    additionalContext: `Prettier could not format ${file} — check for syntax errors.`
  }));
}
process.exit(0);
