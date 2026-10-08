const { chromium } = require(process.env.PW || 'playwright');
// The Visuals thread's version 22 fixes: the empty reading on the start screen, one wheel in the interlude, the World
// panel's close button, the Wanting ring's percent, and on phone a tapped tip closing when a panel opens.
//   node test/probe_vfix.js <url> <shots dir> <width>
const [url, dir, W] = process.argv.slice(2);
(async () => {
  const phone = +W < 600, logs = [], out = {};
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: phone ? 860 : 880 }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'slow'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const shot = (n) => page.screenshot({ path: `${dir}/vfix-${W}-${n}.png` });
  await page.goto(url); await page.waitForSelector('.tarot', { timeout: 300000 }); await page.waitForTimeout(800);
  await shot('1start');
  out.readingOverlap = await page.evaluate(() => { const r = document.querySelector('.reading.empty'); if (!r) return 'no empty reading';
    const a = r.querySelector('.rk').getBoundingClientRect(), b = r.querySelector('p').getBoundingClientRect(); return a.bottom > b.top + 1 ? 'overlap' : 'apart'; });
  const card = '.tarot[data-k="1"]'; await page.click(card);
  for (let i = 0; i < 3 && !(await page.$('#txt')); i++) { await page.waitForTimeout(500); const b = await page.$('#begin'); if (b) await b.click(); else await page.click(card); }
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Lale'); await page.click('#go');
  const idle = () => page.waitForFunction(() => hud && hud.mode === 'play' && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving') && interEl.hidden, null, { timeout: 600000 });
  await idle();
  let il = null;
  for (let k = 0; k < 40 && !il; k++) {
    const s = await page.evaluate(() => ({ cp: !!(hud && hud.cp), res: !!(hud && hud.res) }));
    await page.evaluate((s) => send(s.cp || s.res ? '' : 'd'), s);
    for (let j = 0; j < 40; j++) { await page.waitForTimeout(250); const c = await page.$('.ilcard'); if (c && await c.isVisible()) { il = c; break; } if (await page.evaluate(() => !busy)) break; }
  }
  if (il) { await page.waitForTimeout(1500); await shot('2interlude');
    out.interlude = await page.evaluate(() => ({ wheels: [...document.querySelectorAll('svg.wheel')].filter((e) => e.getBoundingClientRect().width > 0 && getComputedStyle(e).display !== 'none').length, nowheel: !!document.querySelector('.ilcard.nowheel') })); }
  else out.interlude = 'no interlude seen';
  await page.evaluate(() => { try { ilFinish(); } catch (_) {} }); await idle();
  out.wantRing = await page.evaluate(() => { const r = document.querySelector('[data-ring="want"] .pv'); return r ? r.textContent : '(ring not shown)'; });
  if (phone) {
    await page.tap('#tHud'); await page.waitForTimeout(500);
    const ring = await page.$('#hud [data-tip]'); if (ring) { await ring.tap(); await page.waitForTimeout(400); }
    out.tipAfterTap = await page.evaluate(() => !document.getElementById('tip').hidden);
    await page.evaluate(() => pageKey('b')); await page.waitForTimeout(600);
    out.tipOverBook = await page.evaluate(() => !document.getElementById('tip').hidden); await shot('3book'); await page.evaluate(() => closeBook());
  }
  await page.evaluate(() => pageKey('g')); await page.waitForTimeout(700); await shot('4world');
  out.worldClose = await page.evaluate(() => { const b = document.getElementById('wClose'), h = b && b.closest('.shh'); if (!b) return 'no world panel';
    const r = b.getBoundingClientRect(), hr = h.getBoundingClientRect(); return hr.right - r.right < 30 ? 'top right' : 'beside the title'; });
  console.log(JSON.stringify({ width: +W, ...out, logs }));
  await browser.close();
})();
