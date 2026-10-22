import { createHash } from 'node:crypto';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

// Pinned npm distribution, served by jsDelivr. Never accept different bytes silently.
const PELE_URL = 'https://cdn.jsdelivr.net/npm/pele@1.8.0/dist/pele.js';
const SHA256 = '30d94f823025c873abb2ec3676e34124e543583731e228ca957f51ddda415a05';
const source = new URL('architecture-overview.mmd', import.meta.url);
const output = new URL('../images/architecture-overview.svg', import.meta.url);

const bundleIndex = process.argv.indexOf('--bundle');
let bundle;
if (bundleIndex >= 0) {
  if (!process.argv[bundleIndex + 1]) throw new Error('--bundle needs a file path');
  bundle = await readFile(process.argv[bundleIndex + 1]);
} else {
  const response = await fetch(PELE_URL);
  if (!response.ok) throw new Error(`Pele download failed: HTTP ${response.status}`);
  bundle = Buffer.from(await response.arrayBuffer());
}
if (createHash('sha256').update(bundle).digest('hex') !== SHA256) {
  throw new Error('Pele download hash mismatch');
}
const temporary = await mkdtemp(join(tmpdir(), 'pele-render-'));
const modulePath = join(temporary, 'pele.mjs');
await writeFile(modulePath, bundle);
const { render } = await import(pathToFileURL(modulePath).href);
const { svg } = render(await readFile(source, 'utf8'));
if (!svg || !svg.includes('<svg')) throw new Error('Pele returned no SVG');
// CSS is part of generation so the committed SVG is readable without page styles.
const style = `<style>
  :root { --pele-bg: #ffffff; --pele-fg: #17212b; --pele-muted: #3c4b59; --pele-line: #34485a; --pele-surface: #f2f6fa; --pele-surface-alt: #e6eef5; --pele-border: #607487; --pele-accent: #175a9e; --pele-font: Arial, sans-serif; }
  @media (prefers-color-scheme: dark) { :root { --pele-bg: #141b23; --pele-fg: #eef4fa; --pele-muted: #c5d0da; --pele-line: #bfd0df; --pele-surface: #243241; --pele-surface-alt: #314458; --pele-border: #a4b5c5; --pele-accent: #8fc5ff; } }
</style>`;
const generated = svg.replace(/<svg\b[^>]*>/, (tag) =>
  `${tag}${style}<title>Directory inventory data flow</title>`);
if (process.argv.includes('--check')) {
  if (generated !== await readFile(output, 'utf8')) throw new Error('SVG is out of date');
} else {
  await writeFile(output, generated, 'utf8');
}
