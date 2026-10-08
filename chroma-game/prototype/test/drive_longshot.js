const { chromium } = require(process.env.PW || 'playwright');
const dir = process.argv[2] || '.', port = process.argv[3] || '8121';  // node test/drive_longshot.js <shots> [port]: push long shots, then the review and the Book
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1360, height: 880 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} });
  const page = await ctx.newPage();
  const logs = [];
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/${n}.png` });
  await page.goto(`http://127.0.0.1:${port}/page.html`);
  await page.waitForSelector('.tarot', { timeout: 90000 }); await page.waitForTimeout(800);
  await page.click('.tarot[data-k="2"]');
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Ilka'); await page.click('#go');
  const t0 = Date.now(); let n = 0, ls = 0, shotRes = false;
  while (Date.now() - t0 < (+process.env.LS_MS || 1800000)) {   // a whole life with the world: about 15 minutes on a busy machine
    await page.waitForFunction(() => hud && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 360000 });   // a 20-year past with the world can pass 2 minutes on a loaded machine
    const st = await page.evaluate((lim) => {
      const cp = hud.cp; let pick = null;
      if (cp) for (const o of cp.options || []) {
        const aim = (o.roles_fx || []).find((x) => x.when === 'ok' && x.gain && x.title && ['career', 'community', 'faith'].includes(x.kind));
        if (aim && o.n != null && (o.base ?? o.true ?? 1) < lim) { pick = o.n; break; }
      }
      return { mode: hud.mode, cp: !!cp, res: !!hud.res, ls: !!(hud.res && hud.res.long_shot), pick };
    }, 0.5);
    if (st.mode === 'over') break;
    if (st.mode !== 'play') { await page.waitForTimeout(300); continue; }
    n++;
    if (st.ls && !shotRes) { await page.waitForTimeout(500); await shot('l1-resolution'); shotRes = true; }
    if (st.pick != null) ls++;
    await page.evaluate((s) => send(s.pick != null ? String(s.pick) : s.cp || s.res ? '' : 'd'), st);
    await page.waitForTimeout(100);
  }
  await page.waitForTimeout(1200); await shot('l2-review');
  const rv = await page.evaluate(() => [...document.querySelectorAll('.review .pls')].map((p) => p.textContent.trim()));
  await page.click('#rvBook'); await page.waitForTimeout(600); await shot('l3-book');
  const bk = await page.evaluate(() => Object.keys(book.seen).filter((k) => k.startsWith('l|')));
  await page.evaluate(() => closeBook());
  await page.setViewportSize({ width: 400, height: 860 }); await page.waitForTimeout(400);
  await page.evaluate(() => { const r = document.querySelector('.review'); if (r) r.scrollTop = 0; }); await shot('l4-review-phone');
  console.log('pushed', ls, 'review lines', JSON.stringify(rv), 'book', JSON.stringify(bk));
  console.log('scrollWidth', await page.evaluate(() => document.documentElement.scrollWidth));
  console.log('steps', n, 'secs', Math.round((Date.now() - t0) / 1000));
  console.log(logs.join('\n') || 'no page errors');
  await browser.close();
})();
