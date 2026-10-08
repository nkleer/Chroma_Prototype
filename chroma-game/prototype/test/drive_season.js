const { chromium } = require(process.env.PW || 'playwright');
const dir = process.argv[2] || '.';  // node test/drive_season.js <shots dir>: a season moment and its turning point, seen in the page
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1360, height: 880 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} });
  const page = await ctx.newPage();
  const logs = [];
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/${n}.png` });
  await page.goto('http://127.0.0.1:' + (process.env.PORT || 8121) + '/page.html');
  await page.waitForSelector('.tarot', { timeout: 90000 }); await page.waitForTimeout(800);
  await page.click('.tarot[data-k="3"]');
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Noor'); await page.click('#go');
  const t0 = Date.now(); let n = 0, step = 0, turn = 0, chip = 0;
  while (Date.now() - t0 < 600000 && (step < 1 || turn < 1)) {
    await page.waitForFunction(() => hud && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 360000 });   // a 20-year past with the world can pass 2 minutes on a loaded machine
    const st = await page.evaluate(() => ({ mode: hud.mode, cp: hud.cp ? (hud.cp.season || null) : undefined, res: !!hud.res, age: hud.life && hud.life.age }));
    if (st.mode === 'over') break;
    if (st.mode !== 'play') { await page.waitForTimeout(300); continue; }
    n++;
    if (st.cp && st.cp.this_week) {
      await page.waitForTimeout(500);
      const seen = await page.evaluate(() => ({ note: (document.getElementById('cpSeason') || {}).textContent || '', chip: (document.getElementById('seasonChip') || {}).textContent || '' }));
      console.log('age', st.age, 'step', st.cp.step, 'transform', st.cp.transform, '| note:', seen.note.trim(), '| chip:', seen.chip.trim());
      if (seen.chip) chip++;
      if (st.cp.transform && !turn) { turn++; await shot('s2-turning-point'); }
      else if (!step) { step++; await shot('s1-season-moment'); }
    }
    await page.evaluate((s) => send(s.cp !== undefined || s.res ? '' : 'd'), st);
    await page.waitForTimeout(100);
  }
  if (chip) { await page.evaluate(() => { const e = document.querySelector('.evwrap'); if (e) e.click(); }); await page.waitForTimeout(400); await page.hover('#seasonChip', { force: true }); await page.waitForTimeout(500); await shot('s3-season-tip'); }
  await page.setViewportSize({ width: 400, height: 860 }); await page.waitForTimeout(400); await shot('s4-phone');
  console.log('scrollWidth', await page.evaluate(() => document.documentElement.scrollWidth));
  console.log('steps', n, 'secs', Math.round((Date.now() - t0) / 1000));
  console.log(logs.join('\n') || 'no page errors');
  await browser.close();
})();
