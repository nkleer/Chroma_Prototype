const { chromium } = require(process.env.PW || 'playwright');
// The outer world's player side against the stand-in world (test/mock_world.py, patched into a test copy's worker):
// the World panel, the cast by layer, reach, lever chips and a push result. Not for the published page.
//   PORT=8127 node test/drive_world.js <shots dir>
const dir = process.argv[2] || '.', port = process.env.PORT || 8127;
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
  await page.waitForSelector('.tarot', { timeout: 120000 }); await page.waitForTimeout(800);
  await page.click('.tarot[data-k="1"]');
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Mira'); await page.click('#go');
  const t0 = Date.now(); let lever = false, push = false, world = false;
  while (Date.now() - t0 < 900000) {
    await page.waitForFunction(() => hud && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 180000 });
    const st = await page.evaluate(() => ({ mode: hud.mode, cp: !!hud.cp, res: !!hud.res, age: hud.life && hud.life.age, world: !!hud.world,
      lever: !!(hud.cp && hud.cp.options.some((o) => o.lever)), push: !!(hud.res && hud.res.world_push) }));
    if (st.mode === 'over') break;
    if (st.mode !== 'play') { await page.waitForTimeout(300); continue; }
    if (st.cp && st.lever && !lever && st.age > 18) { lever = true; await page.waitForTimeout(500); await shot('w1-checkpoint-levers');
      try { await page.hover('.opt .lever', { force: true, timeout: 3000 }); await page.waitForTimeout(400); await shot('w1b-lever-tip'); } catch (_) {} }
    if (st.res && st.push && !push && st.age > 18) { push = true; await page.waitForTimeout(500); await shot('w2-resolution-push'); }
    if (st.world && !world && st.age > 30) {
      world = true;
      await page.evaluate(() => { hudEl.classList.add('open'); renderHud(hud.life); }); await page.waitForTimeout(500);
      await page.evaluate(() => { const s = [...hudEl.querySelectorAll('.hsec h4')].find((h) => h.textContent === 'People'); if (s) s.scrollIntoView(); }); await page.waitForTimeout(300);
      await shot('w3-hud-circle-reach');
      const av = await page.$('.circle .av'); if (av) { try { await av.hover({ force: true, timeout: 3000 }); await page.waitForTimeout(400); await shot('w3b-person-tip'); } catch (_) {} }
      await page.evaluate(() => closeHud());
      await page.evaluate(() => pageKey('g')); await page.waitForTimeout(600); await shot('w4-world-panel');
      const ev = await page.$('.wline .wev'); if (ev) { try { await ev.hover({ force: true, timeout: 3000 }); await page.waitForTimeout(400); await shot('w4b-event-tip'); } catch (_) {} }
      await page.setViewportSize({ width: 420, height: 860 }); await page.waitForTimeout(500); await shot('w5-world-phone');
      await page.setViewportSize({ width: 1360, height: 880 }); await page.evaluate(() => closeWorld());
    }
    if (lever && push && world) break;
    await page.evaluate((s) => send(s.cp || s.res ? '' : 'd'), st);
    await page.waitForTimeout(120);
  }
  const feedWorld = await page.evaluate(() => [...document.querySelectorAll('.mk-O')].slice(0, 5).map((x) => x.textContent));
  console.log(JSON.stringify({ lever, push, world, feedWorld, logs }, null, 1));
  await browser.close();
})();
