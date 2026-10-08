const { chromium } = require(process.env.PW || 'playwright');
// The setup wait (coordinator, 10-07): from Begin to the first state of the life, with what the screen shows meanwhile.
//   node test/probe_start.js <url> <shots dir> <preset> <width>
const [url, dir, preset, W] = process.argv.slice(2);
(async () => {
  const phone = +W < 600, logs = [];
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: phone ? 860 : 880 }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const t0 = Date.now(); await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 180000 }); const tLoad = Date.now() - t0; await page.waitForTimeout(600);
  const card = `.tarot[data-k="${preset}"]`; await page.click(card);
  for (let i = 0; i < 3 && !(await page.$('#txt')); i++) { await page.waitForTimeout(500); const b = await page.$('#begin'); if (b) await b.click(); else await page.click(card); }
  await page.waitForSelector('#txt', { timeout: 30000 }); await page.fill('#txt', 'Lale');
  const tGo = Date.now(); await page.click('#go');
  await page.waitForTimeout(800); await page.screenshot({ path: `${dir}/start-${preset}-${W}-1s.png` });
  const shown = await page.evaluate(() => { const e = document.querySelector('.starting, .live'); return e ? e.innerText.replace(/\s+/g, ' ').trim() : '(nothing)'; });
  const seen = [];
  const tFirst = await (async () => { for (;;) {
    const s = await page.evaluate(() => ({ live: (document.querySelector('.live') || {}).innerText || '', st: !!document.querySelector('.starting'), cp: !!(hud && hud.cp), idle: !!(hud && hud.mode === 'play' && !busy) }));
    const line = s.st ? 'starting' : s.live.replace(/\s+/g, ' ').trim(); if (line && seen[seen.length - 1] !== line) seen.push(line);
    if (s.idle) return Date.now() - tGo; if (Date.now() - tGo > 600000) return -1; await page.waitForTimeout(500); } })();
  await page.screenshot({ path: `${dir}/start-${preset}-${W}-first.png` });
  console.log(JSON.stringify({ preset, width: +W, loadToSpread: (tLoad / 1000).toFixed(1), shownAfterBegin: shown, beginToFirstState: (tFirst / 1000).toFixed(1), lines: seen.slice(0, 12), logs }));
  await browser.close();
})();
