// Renders template/usp2.html (real product photos) to output2/<MODEL>_USP.png (layout A) and
// output2/<MODEL>_USP_2.png (layout B), 1080x1080, for every model or the ones named:
//   node render2.mjs                 all models, both layouts
//   node render2.mjs MR8030 MR8035   just these
//   node render2.mjs --layout A      one layout only
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { mkdirSync, readFile } from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    const globalRoot = execSync('npm root -g').toString().trim();
    return createRequire(import.meta.url)(path.join(globalRoot, 'playwright'));
  }
}

const args = process.argv.slice(2);
const li = args.indexOf('--layout');
const layouts = li >= 0 ? [args.splice(li, 2)[1]] : ['A', 'B'];

// serve the folder over http: masks and canvas reads of the photos do not work from file:// pages
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg','.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const file = path.join(here, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!file.startsWith(here)) { res.writeHead(403); return res.end(); }
  readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
    res.end(data);
  });
});
await new Promise(ok => server.listen(0, '127.0.0.1', ok));

const { chromium } = await loadPlaywright();
const outDir = path.join(here, 'output2');
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 1 });
await page.goto(`http://127.0.0.1:${server.address().port}/template/usp2.html`);
await page.evaluate(() => window.ready);

const all = await page.evaluate(() => window.MODELS2.map(m => m.id));
const ids = args.length ? all.filter(id => args.includes(id)) : all;
for (const id of ids) {
  for (const lay of layouts) {
    await page.evaluate(([id, lay]) => window.render(id, lay), [id, lay]);
    const file = path.join(outDir, `${id}_USP${lay === 'B' ? '_2' : ''}.png`);
    await page.locator('#canvas').screenshot({ path: file });
    console.log(`${id} ${lay}  ->  ${path.relative(here, file)}`);
  }
}
await browser.close();
server.close();
