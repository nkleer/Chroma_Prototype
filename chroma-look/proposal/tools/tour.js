// Tour of the live look: start spread, first screen, a moment, an outcome. Usage: node tour.js URL OUTDIR WIDTH HEIGHT
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const T = '/home/user/Chroma_Prototype/chroma-game/prototype/test/';
const { startLife, idleOf, nextOf } = require(T + 'start.js');
const [url, out, W, H] = [process.argv[2], process.argv[3], +(process.argv[4] || 1280), +(process.argv[5] || 860)];
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const logs = []; page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  const idle = idleOf(page, logs); const next = nextOf(page, idle);
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 120000 }); await page.waitForTimeout(2500);
  await page.screenshot({ path: `${out}/1-start-${W}.png` });
  await page.hover('.tarot[data-k="2"]').catch(()=>{}); await page.waitForTimeout(900);
  await page.screenshot({ path: `${out}/2-start-hover-${W}.png` });
  await startLife(page, '2', 'Lale'); await idle(); await page.waitForTimeout(800);
  await page.screenshot({ path: `${out}/3-first-${W}.png` });
  let gotMoment = false, gotOut = false;
  for (let i = 0; i < 40 && !(gotMoment && gotOut); i++) {
    const s = await page.evaluate(() => ({ cp: !!document.querySelector('#evLet') && !document.getElementById('evwrap').hidden,
      res: !!document.querySelector('#goOn') && !document.getElementById('evwrap').hidden }));
    if (s.cp && !gotMoment) {
      await page.waitForTimeout(1200); await page.screenshot({ path: `${out}/4-moment-${W}.png` });
      const o = await page.$('.opt'); if (o) { await o.hover(); await page.waitForTimeout(700); await page.screenshot({ path: `${out}/5-moment-hover-${W}.png` });
        await o.click(); await page.waitForTimeout(250); await page.screenshot({ path: `${out}/6-choosing-${W}.png` }); await idle(); await page.waitForTimeout(900);
        await page.screenshot({ path: `${out}/7-outcome-${W}.png` }); gotOut = true; }
      gotMoment = true; continue;
    }
    await next();
  }
  await page.screenshot({ path: `${out}/8-later-${W}.png` });
  console.log(logs.join('\n') || 'no page errors');
  await browser.close();
})();
