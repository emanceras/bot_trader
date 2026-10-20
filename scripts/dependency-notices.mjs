// Produce a reviewable inventory from installed packages and the frozen npm lock.
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
const root = resolve(import.meta.dirname, '..');
const web = resolve(root, 'web');
const lock = JSON.parse(readFileSync(resolve(web, 'package-lock.json'), 'utf8'));
const inventory = [];
const notices = ['Third-party runtime notices for bot_trader web. Generated from the locked installation.\n'];
for (const [relative, entry] of Object.entries(lock.packages)) {
  if (!relative) continue;
  const location = resolve(web, relative);
  const installed = existsSync(resolve(location, 'package.json'));
  const record = { path: relative, version: entry.version, license: entry.license ?? 'not declared', development: Boolean(entry.dev), installed };
  inventory.push(record);
  if (!entry.dev && installed) {
    const metadata = JSON.parse(readFileSync(resolve(location, 'package.json'), 'utf8'));
    notices.push(`\n=== ${metadata.name} ${metadata.version} (${record.license}) ===\n`);
    const names = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'LICENSE.js', 'LICENSE-MIT', 'NOTICE'];
    let found = false;
    for (const name of names) {
      const packagePath = resolve(location, name);
      const path = existsSync(packagePath) ? packagePath : resolve(web, 'licenses', metadata.name, name);
      if (existsSync(path)) {
        const bytes = readFileSync(path);
        notices.push(bytes.toString('utf8'));
        record[name] = createHash('sha256').update(bytes).digest('hex');
        found = true;
      }
    }
    if (!found) throw new Error(`Missing runtime notice for ${metadata.name}; review before distribution.`);
  }
}
mkdirSync(resolve(root, 'docs/licenses'), { recursive: true });
writeFileSync(resolve(root, 'docs/licenses/npm-dependencies.json'), JSON.stringify({ scope: 'Resolved packages; optional platform packages may not be installed. This is a metadata inventory, not legal certification.', packages: inventory }, null, 2) + '\n');
writeFileSync(resolve(web, 'public/THIRD_PARTY_NOTICES.txt'), notices.join('\n'));
console.log(`Inventoried ${inventory.length} resolved packages and retained runtime notices.`);
