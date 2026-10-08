const { chromium } = require(process.env.PW || 'playwright');
// 720 px lab (v22.1): at each moment of one life, how far the option area must scroll with the page's own styles and
// with each candidate style laid over it. node test/fit720_lab.js <url> <moments> <W> <H> <candidates.json>
const { startLife, idleOf, nextOf } = require('./start.js');
const fs = require('fs');
const [url, M, W, H, cf] = [process.argv[2], +(process.argv[3] || 20), +(process.argv[4] || 1280), +(process.argv[5] || 720), process.argv[6]];
const C = cf ? JSON.parse(fs.readFileSync(cf, 'utf8')) : {};
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url); await startLife(page, '1', 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const res = { base: [] }; for (const k in C) res[k] = [];
  let n = 0;
  for (let k = 0; k < 4000 && n < M; k++) {
    await idle();
    const at = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (!at) { if (await page.evaluate(() => hud && hud.mode !== 'play')) break; try { await next(); } catch (e) { break; } continue; }
    n++; await page.mouse.move(2, 2); await page.waitForTimeout(500);
    const meas = () => page.evaluate(() => { const ev = document.getElementById('evOpts'); return [Math.max(0, ev.scrollHeight - ev.clientHeight), ev.querySelectorAll('.opt').length]; });
    res.base.push(await meas());
    for (const key in C) {
      await page.evaluate(([key, css]) => { const s = document.createElement('style'); s.id = 'lab'; s.textContent = css; document.body.appendChild(s); }, [key, C[key]]);
      await page.waitForTimeout(80); res[key].push(await meas());
      if (process.env.SHOTS && res[key].length && res[key][res[key].length - 1][1] >= 11 && !res[key].shot) { res[key].shot = 1; await page.screenshot({ path: `${process.env.SHOTS}/lab-${key}.png` }); }
      await page.evaluate(() => document.getElementById('lab').remove());
    }
    await page.click('#evLet', { timeout: 15000 }).catch(() => {});
  }
  for (const key in res) { const r = res[key]; console.log(key.padEnd(8), 'scrolled', r.filter((x) => x[0] > 1).length, 'of', r.length, 'max', Math.max(0, ...r.map((x) => x[0])), 'by n', JSON.stringify(r.filter((x) => x[0] > 1).map((x) => x[1] + ':' + x[0]))); }
  console.log('logs', JSON.stringify(logs));
  await browser.close();
})();
