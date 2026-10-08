const { chromium } = require(process.env.PW || 'playwright');
// Fit lab (game thread, C-X3 fit fix): play one life at 1280 wide; at the biggest moments, measure how far the options
// column overflows at several window heights, with the page's own styles and with a candidate style sheet added.
//   node test/fit_lab.js <url> <candidate.css> [moments to collect] [heights, comma separated] [preset]
const fs = require('fs');
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, cssPath, want, Hs, preset] = [process.argv[2], process.argv[3], +(process.argv[4] || 3), (process.argv[5] || '720,768,800,880').split(',').map(Number), process.argv[6] || '1'];
const css = cssPath && cssPath !== '-' ? fs.readFileSync(cssPath, 'utf8') : '';
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, preset, 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const measure = () => page.evaluate(() => {
    const ev = document.getElementById('evOpts'), s = document.getElementById('evStrip'), opts = [...ev.querySelectorAll('.opt')];
    const last = opts[opts.length - 1].getBoundingClientRect(), sb = s ? s.getBoundingClientRect() : null;
    return { over: ev.scrollHeight - ev.clientHeight, strip: sb ? Math.round(sb.height) : 0, lastUnderStrip: sb ? Math.round(last.bottom - sb.top) : 0,
      card: Math.round(opts[0].getBoundingClientRect().height) };
  });
  let got = 0, best = 0;
  for (let k = 0; k < 4000 && got < want; k++) {
    await idle();
    const n = await page.evaluate(() => { const w = document.getElementById('evwrap'), ev = document.getElementById('evOpts');
      return w && !w.hidden && ev && document.getElementById('evLet') ? ev.querySelectorAll('.opt').length : 0; });
    if (n >= 11 || (n > best && n >= 9)) {
      best = Math.max(best, n); got += n >= 11 ? 1 : 0;
      const age = await page.evaluate(() => hud && hud.life && Math.round(hud.life.age * 10) / 10);
      const row = { age, n, base: {}, cand: {} };
      for (const H of Hs) { await page.setViewportSize({ width: 1280, height: H }); await page.waitForTimeout(250); row.base[H] = await measure(); }
      const tag = css ? await page.evaluateHandle((c) => { const t = document.createElement('style'); t.textContent = c; document.body.appendChild(t); return t; }, css) : null;   // after the page's own styles, as head.html's last rules would be
      if (tag) {
        for (const H of Hs) { await page.setViewportSize({ width: 1280, height: H }); await page.waitForTimeout(250); row.cand[H] = await measure();
          if (process.env.SHOTS) await page.screenshot({ path: `${process.env.SHOTS}/lab-${n}opts-age${age}-${H}.png` }); }
        // hover each of the last three options at 800 tall: how tall the strip grows, and whether the pointer still reaches the card
        await page.setViewportSize({ width: 1280, height: 800 }); await page.waitForTimeout(250); row.hover = [];
        const nOpts = await page.$$eval('#evOpts .opt', (a) => a.length);
        for (let i = Math.max(0, nOpts - 3); i < nOpts; i++) {
          const el = (await page.$$('#evOpts .opt'))[i]; await el.hover(); await page.waitForTimeout(200);
          row.hover.push(await page.evaluate((i) => { const o = document.querySelectorAll('#evOpts .opt')[i], b = o.getBoundingClientRect(), s = document.getElementById('evStrip').getBoundingClientRect();
            const hit = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2);
            return { i, strip: Math.round(s.height), under: Math.round(b.bottom - s.top), hitsCard: !!(hit && o.contains(hit)), over: document.getElementById('evOpts').scrollHeight - document.getElementById('evOpts').clientHeight }; }, i));
        }
        await page.mouse.move(5, 5); await page.waitForTimeout(150);
        await tag.evaluate((t) => t.remove());
      }
      await page.setViewportSize({ width: 1280, height: 800 });
      console.log(JSON.stringify(row));
    }
    if (await page.evaluate(() => !!document.querySelector('.review:not([hidden]), #review:not([hidden]) .rv'))) break;
    try { await next(); } catch (e) { logs.push('next: ' + String(e.message).slice(0, 120)); break; }
  }
  console.log('logs:', JSON.stringify(logs));
  await browser.close();
})();
