const { chromium } = require(process.env.PW || 'playwright');
// Release row C-G5: one whole life in the browser, from the tarot spread to the review and the Book, as a player would
// play it: about half the moments chosen by the player (a random option), the rest left to the character; every Go on
// clicked. Checks on the way: no page error, no sideways scroll, the autosave slot filled, the event window never left
// open after Go on, every push taken (v23: the first by its number on the keyboard, then held; a phone also taps and
// pushes with "Push them to this"), (Build your own) the setup's step 2 with Intersex, and one reload at age 20 that must come back
// through Continue at the same name and age. Screenshots at the first moment, the first outcome, age 30, the end and the Book.
//   node test/drive_life.js <url> <shots dir> <tag> <preset 1-7, 7 = Build your own> <width> <height> [minutes]
const [url, dir, tag, preset, W, H, mins] = process.argv.slice(2);
const { idleOf } = require('./start.js');
const { holdOpt, pushOpt, keyOpt } = require('./hold.js');   // v23: with the Living HUD a pointer pushes a card by holding it
(async () => {
  const phone = +W < 600, logs = [], notes = {};
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: +H }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off');   // the slot is emptied on the first load only, so the reload finds it
    if (!sessionStorage.getItem('drive.started')) { sessionStorage.setItem('drive.started', '1'); localStorage.removeItem('chroma.autosave'); } } catch (_) {} });
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
  let steps = 0, chosen = 0, keyed = 0, held = 0, notThrough = 0, pushedAt = null, noCard = [], left = 0, sideways = 0, openAfterGoOn = 0, firstCp = false, firstRes = false, at30 = false, renames = 0, autoSeen = null, resume = null;
  const readAuto = () => page.evaluate(() => { try { const d = JSON.parse(localStorage.getItem('chroma.autosave') || 'null'); return d ? { name: d.name, age: d.age } : null; } catch (_) { return 'unreadable'; } });
  const t0 = Date.now(), limit = (+mins || 25) * 60000;
  while (Date.now() - t0 < limit) {
    await idle();
    const s = await page.evaluate(() => ({ mode: hud && hud.mode, age: hud && hud.life && hud.life.age,
      ev: !document.getElementById('evwrap').hidden, res: !!document.querySelector('#goOn'), cp: !!document.querySelector('#evLet'),
      rn: !!document.querySelector('#rnKeep'), sx: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, key: lastCpKey }));
    if (s.mode === 'over') break;
    if (pushedAt !== null) { if (s.cp && s.key === pushedAt) notThrough++; pushedAt = null; }   // the same moment still waits: the push was lost
    if (steps % 10 === 5) { const a_ = await readAuto(); if (a_) autoSeen = a_; }   // the slot fills during play
    if (s.sx) sideways++;
    if (!resume && s.age >= 20) {                       // Release 10-17: reload mid-life; Continue must bring back the same life
      const saved = await readAuto();
      if (saved && saved !== 'unreadable') {
        const tR = Date.now(); await page.reload();
        await page.waitForSelector('#mContinue', { timeout: 120000 }); await page.click('#mContinue');
        await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 600000 }); await idle();
        const back = await page.evaluate(() => ({ name: hud.life && hud.life.name, age: hud.life && hud.life.age }));
        resume = { saved, back, seconds: Math.round((Date.now() - tR) / 1000), ok: back.name === saved.name && Math.abs(back.age - saved.age) < 0.01 };
        await shot('resumed'); continue;
      }
    }
    if (!at30 && s.age >= 30) { at30 = true; await shot('age30'); }
    steps++;
    if (s.ev && s.rn) { renames++; await shot('rename'); await page.click(Math.random() < 0.5 ? '#rnTake' : '#rnKeep'); continue; }
    if (s.ev && s.res) {
      if (!firstRes) { firstRes = true; await shot('outcome'); }
      await page.click('#goOn'); await page.waitForTimeout(450);
      if (await page.evaluate(() => !busy && !document.getElementById('evwrap').hidden && !!document.querySelector('#goOn'))) openAfterGoOn++;
    } else if (s.ev && s.cp) {
      if (!firstCp) { firstCp = true; await shot('moment'); }
      // a random card, or none: every way but Do nothing can be folded away out of reach (the fold is closed)
      const opts = Math.random() < 0.5 ? await page.$$('#evwrap .opt:not(.pass)') : null;
      if (opts && !opts.length) noCard.push(await page.evaluate(() => ({ age: hud.life.age, ways: hud.cp.options.length, oor: hud.cp.options.filter((o) => o.status === 'out of reach').length })));
      if (opts && opts.length) {
        const o = opts[Math.floor(Math.random() * opts.length)];
        // the first push by its number on the keyboard; after it a desktop holds the card (a click, on a page without the
        // hold), and a phone in turn holds it with a finger or taps it to read it and pushes with "Push them to this"
        pushedAt = s.key;
        if (!chosen) { await keyOpt(page, o); keyed++; }
        else if (!phone) { if ((await holdOpt(page, o)).held) held++; }
        else if (chosen % 2) { if ((await pushOpt(page, o, { touch: true })).held) held++; }
        else { await o.tap(); await page.waitForTimeout(200); const p = await page.$('#pushIt'); if (p) await p.click(); }
        chosen++;
      } else { await page.click('#evLet'); left++; }
    } else await page.click('#tMain');
  }
  const end = await page.evaluate(() => ({ mode: hud.mode, age: hud.life && hud.life.age, who: hud.life && hud.life.who, sexword: hud.life && hud.life.sexword }));
  await page.waitForTimeout(1500); await shot('end');
  const atEnd = await readAuto();                       // a finished life leaves no Continue: the review clears the slot
  const auto = end.mode === 'over' ? (autoSeen && !atEnd ? autoSeen : null) : atEnd || autoSeen;
  const rb = await page.$('#rvBook'); if (rb) { await rb.click(); await page.waitForTimeout(700); await shot('book'); }
  console.log(JSON.stringify({ tag, preset, width: +W, name: notes.name, step2: notes.step2, setupWait: notes.setupWait, waitLine: notes.waitLine, end, steps, chosen, keyed, held, notThrough, noCard, left, renames, sideways, openAfterGoOn, autosave: auto, autosaveAtEnd: atEnd, resume, minutes: ((Date.now() - t0) / 60000).toFixed(1) }));
  console.log('errors', JSON.stringify(logs.slice(0, 10)), logs.length);
  await browser.close();
  process.exit(end.mode === 'over' && !logs.length && !sideways && !openAfterGoOn && !notThrough && auto && (!resume || resume.ok) ? 0 : 1);   // resume stays null only for a life over before 20
})();
