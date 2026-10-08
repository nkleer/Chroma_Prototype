const { chromium } = require(process.env.PW || 'playwright');
// Event window timing (C-G6): feedback within 0.1 s of a click, the outcome in the same window, Go on closes it.
const dir = process.argv[2], port = process.env.PORT || 8121, rounds = +(process.argv[3] || 3), vw = +(process.argv[4] || 1360);
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: vw, height: vw < 600 ? 860 : 880 } })).newPage();
  const logs = []; page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  await page.goto(`http://127.0.0.1:${port}/page.html`);
  await page.waitForSelector('.tarot', { timeout: 120000 }); await page.waitForTimeout(800);
  await page.click('.tarot[data-k="1"]'); await page.click('.tarot[data-k="1"]').catch(() => {});
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Mira'); await page.click('#go');
  const state = () => page.evaluate(() => ({ busy, cp: !!(hud && hud.cp), res: !!(hud && hud.res), ev: !evWrap.hidden, il: !interEl.hidden && IL.on, age: hud && hud.life && hud.life.age,
    choosing: tableEl.classList.contains('choosing'), chosen: !!tableEl.querySelector('.opt.chosen'), trying: !!tableEl.querySelector('.trying'), shownRes: !!tableEl.querySelector('#goOn'), shownCp: !!tableEl.querySelector('#evOpts') }));
  const out = [];
  let n = 0;
  for (let k = 0; k < 600 && n < rounds; k++) {
    await page.waitForFunction(() => hud && !busy, null, { timeout: 180000 });
    const st = await state();
    if (hud_over(st)) break;
    if (st.cp && st.ev && st.shownCp && !st.il && st.age > 5) {
      n++; await page.waitForTimeout(300);
      const opts = await page.$$('.opt'); const pick = opts[Math.min(opts.length - 1, n % 3)];
      await page.evaluate(() => {   // in the page: from the pointer going down to the "trying" sign, without the driver's own lag
        window.__t = null; window.__f = null;
        const mo = new MutationObserver(() => { if (window.__f == null && tableEl.querySelector('.trying')) { window.__f = performance.now(); mo.disconnect(); } });
        mo.observe(tableEl, { subtree: true, childList: true, attributes: true });
        document.addEventListener('pointerdown', () => { window.__t = performance.now(); }, { capture: true, once: true });
      });
      await pick.evaluate((el) => el.scrollIntoView({ block: 'center' })); await page.waitForTimeout(300);   // on a phone the pinned bar covers the lower options
      const t0 = Date.now(); await pick.click({ force: true });
      const a = await state(); const ta = Date.now() - t0;
      const inPage = await page.evaluate(() => window.__t != null && window.__f != null ? Math.round(window.__f - window.__t) : null);
      if (n === 1) await page.screenshot({ path: `${dir}/r${n}-a-trying.png` });
      await page.waitForFunction(() => !!tableEl.querySelector('#goOn') && !evWrap.hidden, null, { timeout: 60000 });
      const tres = Date.now() - t0; await page.waitForTimeout(600);
      if (n === 1) await page.screenshot({ path: `${dir}/r${n}-b-outcome.png` });
      const t1 = Date.now(); await page.click('#goOn');
      await page.waitForFunction(() => evWrap.hidden, null, { timeout: 5000 }).catch(() => {});
      const tclose = Date.now() - t1; const c = await state();
      if (n === 1) { await page.waitForTimeout(1500); await page.screenshot({ path: `${dir}/r${n}-c-after-goon.png` }); }
      out.push({ n, age: st.age, feedback_ms: inPage, driver_ms: ta, feedback: a, outcome_ms: tres, close_ms: tclose, after: c });
      continue;
    }
    if (st.il) { await page.waitForTimeout(300); continue; }
    await page.evaluate((s) => send(s.cp || s.res ? '' : 'd'), st);
    await page.waitForTimeout(100);
  }
  function hud_over(st) { return false; }
  await page.screenshot({ path: `${dir}/z-line.png`, clip: { x: 0, y: 0, width: vw, height: 200 } });
  console.log(JSON.stringify(out, null, 0)); console.log(JSON.stringify(logs)); await browser.close();
  const ok = out.length === rounds && !logs.length && out.every((r) => r.feedback_ms != null && r.feedback_ms <= 100 && r.after && !r.after.ev);
  console.log(`C-G6: ${ok ? "PASS" : "FAIL"} (feedback in the page ${out.map((r) => r.feedback_ms).join(", ")} ms; the window closed after Go on in ${out.filter((r) => r.after && !r.after.ev).length} of ${out.length})`);
  process.exit(ok ? 0 : 1);
})();
