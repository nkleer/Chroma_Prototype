// Plays until a moment offers an option the character is against, hovers it and saves a shot.
// Usage: node test/drive_against.js URL OUT.png [preset]
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');   // the tarot start screen (release row G8)
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1280, height: 860 }, colorScheme: 'dark' });
  const logs = []; page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await page.goto(process.argv[2]); await page.waitForSelector('.tarot', { timeout: 90000 });
  const idle = async () => { await page.waitForTimeout(150); await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle')); await page.waitForTimeout(200); };
  await startLife(page, process.argv[4] || '2', 'Ada');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 }); await idle();
  const state = () => page.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn') }));
  let found = false;
  for (let i = 0; i < 120 && !found; i++) {
    const s = await state();
    if (s.cp) { const k = await page.evaluate(() => [...document.querySelectorAll('.opt')].findIndex(b => /Against/.test(b.querySelector('.acc').textContent))); if (k >= 0) { const b = (await page.$$('.opt'))[k]; await b.scrollIntoViewIfNeeded(); await b.hover(); await page.waitForTimeout(400); await page.screenshot({ path: process.argv[3] }); found = true;
      console.log(await page.evaluate(() => (document.getElementById('evStrip') || document.getElementById('tip') || {}).innerText));   /* v22 new look: the reading strip under the cards */ break; } await page.click('#evLet'); }
    else if (s.res) await page.click('#goOn'); else await page.click('#tMain');
    await idle();
  }
  console.log('found', found, logs.join('\n')); await browser.close();
})();
