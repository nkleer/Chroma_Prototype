const { chromium } = require(process.env.PW || 'playwright');
// Release row C-G5: one whole life in the browser, from the tarot spread to the review and the Book, as a player would
// play it: about half the moments chosen by the player (a random option), the rest left to the character; every Go on
// clicked. Checks on the way: no page error, no sideways scroll, the autosave slot filled, the event window never left
// open after Go on, and (Build your own) the setup's step 2 with Intersex. Screenshots at the first moment, the first
// outcome, age 30, the end and the Book.
//   node test/drive_life.js <url> <shots dir> <tag> <preset 1-7, 7 = Build your own> <width> <height> [minutes]
const [url, dir, tag, preset, W, H, mins] = process.argv.slice(2);
const { idleOf } = require('./start.js');
(async () => {
  const phone = +W < 600, logs = [], notes = {};
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: +H }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.removeItem('chroma.autosave'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/${tag}-${n}.png` });
  const idle = idleOf(page, logs);
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 120000 }); await page.waitForTimeout(700);
  const card = `.tarot[data-k="${preset}"]`;
  await page.click(card);
  for (let i = 0; i < 3 && !(await page.$('#txt')); i++) { await page.waitForTimeout(500); if (await page.$('#txt')) break;
    const b = await page.$('#begin'); if (b) { await b.click(); await page.waitForSelector('#txt', { timeout: 60000 }).catch(() => {}); } else if (await page.$(card)) await page.click(card); }
  await page.waitForSelector('#txt', { timeout: 60000 });
  await page.fill('#txt', preset === '7' ? '' : 'Lale'); await page.click('#go');
  if (preset === '7') {                                  // Build your own: step 2 Intersex, the rest as offered
    for (let s = 0; s < 14; s++) {
      const vis = (sel) => page.evaluate((q) => [...document.querySelectorAll(q)].some((e) => e.offsetParent !== null), sel);
      try { await page.waitForFunction(() => [...document.querySelectorAll('.ch:not(:disabled), #txt:not(:disabled), #go:not(:disabled), #tMain, .opt')].some((e) => e.offsetParent !== null), null, { timeout: 600000 }); } catch (e) {
        await shot('setup-stuck'); console.log('setup stuck at', s, await page.evaluate(() => document.querySelector('main, body').innerText.slice(0, 400))); throw e; }
      await page.waitForTimeout(200);
      if (await vis('#tMain, .opt')) break;
      const st = await page.evaluate(() => ({ q: (document.querySelector('.setup h2') || {}).innerText || '', ch: [...document.querySelectorAll('.ch')].map((b) => b.innerText.split('\n')[0]) }));
      if (/Sex at birth/.test(st.q)) { notes.step2 = st; await shot('setup-sex'); const i = st.ch.findIndex((x) => /Intersex/.test(x)); await (await page.$$('.ch'))[i].click(); continue; }
      if (await vis('.ch')) await (await page.$$('.ch'))[0].click(); else await page.click('#go');
    }
  }
  const tGo = Date.now();                              // the setup wait: the years before the player takes over, lived at once
  await page.waitForTimeout(3000); await shot('setup-wait');
  notes.waitLine = await page.evaluate(() => { const e = document.querySelector('.live'); return e && e.offsetParent !== null ? e.innerText.replace(/\s+/g, ' ').trim() : '(no status line shown)'; });
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 600000 });   // the years before the player, on a loaded machine
  await idle(); notes.setupWait = Math.round((Date.now() - tGo) / 1000) + ' s to the first idle state, from age ' + (await page.evaluate(() => hud.life && hud.life.age));
  notes.name = await page.evaluate(() => hud.life && hud.life.name);
  let steps = 0, chosen = 0, left = 0, sideways = 0, openAfterGoOn = 0, firstCp = false, firstRes = false, at30 = false, renames = 0, autoSeen = null;
  const readAuto = () => page.evaluate(() => { try { const d = JSON.parse(localStorage.getItem('chroma.autosave') || 'null'); return d ? { name: d.name, age: d.age } : null; } catch (_) { return 'unreadable'; } });
  const t0 = Date.now(), limit = (+mins || 25) * 60000;
  while (Date.now() - t0 < limit) {
    await idle();
    const s = await page.evaluate(() => ({ mode: hud && hud.mode, age: hud && hud.life && hud.life.age,
      ev: !document.getElementById('evwrap').hidden, res: !!document.querySelector('#goOn'), cp: !!document.querySelector('#evLet'),
      rn: !!document.querySelector('#rnKeep'), sx: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1 }));
    if (s.mode === 'over') break;
    if (steps % 10 === 5) { const a_ = await readAuto(); if (a_) autoSeen = a_; }   // the slot fills during play
    if (s.sx) sideways++;
    if (!at30 && s.age >= 30) { at30 = true; await shot('age30'); }
    steps++;
    if (s.ev && s.rn) { renames++; await shot('rename'); await page.click(Math.random() < 0.5 ? '#rnTake' : '#rnKeep'); continue; }
    if (s.ev && s.res) {
      if (!firstRes) { firstRes = true; await shot('outcome'); }
      await page.click('#goOn'); await page.waitForTimeout(450);
      if (await page.evaluate(() => !busy && !document.getElementById('evwrap').hidden && !!document.querySelector('#goOn'))) openAfterGoOn++;
    } else if (s.ev && s.cp) {
      if (!firstCp) { firstCp = true; await shot('moment'); }
      if (Math.random() < 0.5) {
        const opts = await page.$$('#evwrap .opt:not(.pass)'); const o = opts[Math.floor(Math.random() * opts.length)];
        await o.click(); await page.waitForTimeout(200);
        const p = await page.$('#pushIt'); if (p) await p.click();
        chosen++;
      } else { await page.click('#evLet'); left++; }
    } else await page.click('#tMain');
  }
  const end = await page.evaluate(() => ({ mode: hud.mode, age: hud.life && hud.life.age, who: hud.life && hud.life.who, sexword: hud.life && hud.life.sexword }));
  await page.waitForTimeout(1500); await shot('end');
  const atEnd = await readAuto();                       // a finished life leaves no Continue: the review clears the slot
  const auto = end.mode === 'over' ? (autoSeen && !atEnd ? autoSeen : null) : atEnd || autoSeen;
  const rb = await page.$('#rvBook'); if (rb) { await rb.click(); await page.waitForTimeout(700); await shot('book'); }
  console.log(JSON.stringify({ tag, preset, width: +W, name: notes.name, step2: notes.step2, setupWait: notes.setupWait, waitLine: notes.waitLine, end, steps, chosen, left, renames, sideways, openAfterGoOn, autosave: auto, autosaveAtEnd: atEnd, minutes: ((Date.now() - t0) / 60000).toFixed(1) }));
  console.log('errors', JSON.stringify(logs.slice(0, 10)), logs.length);
  await browser.close();
  process.exit(end.mode === 'over' && !logs.length && !sideways && !openAfterGoOn && auto ? 0 : 1);
})();
