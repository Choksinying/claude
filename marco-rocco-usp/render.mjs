// Renders template/usp.html to output/<MODEL>_USP.png (1080x1080) for every model,
// or only the models named on the command line:  node render.mjs MR8013 MR8030
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    // Fall back to a globally installed playwright (npm i -g playwright).
    const globalRoot = execSync('npm root -g').toString().trim();
    return createRequire(import.meta.url)(path.join(globalRoot, 'playwright'));
  }
}

const { chromium } = await loadPlaywright();
const page_url = pathToFileURL(path.join(here, 'template', 'usp.html')).href;
const outDir = path.join(here, 'output');
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 1 });
await page.goto(page_url);
await page.evaluate(() => window.ready);

const all = await page.evaluate(() => window.MODELS.map(m => m.id));
const wanted = process.argv.slice(2);
const ids = wanted.length ? all.filter(id => wanted.includes(id)) : all;

for (const id of ids) {
  await page.evaluate(id => window.render(id), id);
  const hasPhoto = await page.evaluate(() => !document.getElementById('canvas').classList.contains('no-photo'));
  const file = path.join(outDir, `${id}_USP.png`);
  await page.locator('#canvas').screenshot({ path: file });
  console.log(`${id}  ->  ${path.relative(here, file)}${hasPhoto ? '' : '   (no photo in photos/ yet)'}`);
}
await browser.close();
