// Version 14 page check: event window, hover, peek, a push, the resolution and the HUD at age 30. v23: the push is a hold
// on the desktop (a click on a page without the hold) and a tap, then "Push them to this", on a phone; one more push on
// the way is made by its number on the keyboard; a push that does not go through fails the run.
// Usage: node test/drive_v14.js URL TAG WIDTH HEIGHT OUTDIR [preset]
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');   // the tarot start screen (release row G8)
const { holdOpt, keyOpt } = require('./hold.js');   // v23: with the Living HUD a pointer pushes a card by holding it
const url = process.argv[2]; const tag = process.argv[3] || 'v8';
const width = parseInt(process.argv[4] || '1280'); const height = parseInt(process.argv[5] || '860');
const dir = process.argv[6]; const preset = process.argv[7] || '3';
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600;
  const page = await browser.newPage({ viewport: { width, height }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push('console ' + m.type() + ': ' + m.text()); });
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 90000 }).catch(() => logs.push('no menu'));
  await page.screenshot({ path: `${dir}/${tag}-0menu.png` });
  const idle = async () => { await page.waitForTimeout(150); await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle')); await page.waitForTimeout(250); };
  await startLife(page, preset, 'Lale');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 }); await idle();
  const state = () => page.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn'), voice: !!document.querySelector('.ev .insight'), ev: !document.getElementById('evwrap').hidden }));
  const next = async () => { const s = await state(); if (s.res) await page.click('#goOn'); else if (s.cp) await page.click('#evLet'); else await page.click('#tMain'); await idle(); };
  for (let i = 0; i < 40; i++) { const s = await state(); if (s.cp && s.voice && (await page.evaluate(() => document.querySelectorAll('.opt').length)) >= 6) break; await next(); }
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${dir}/${tag}-1event.png` });
  const info = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
    opts: [...document.querySelectorAll('.opt')].map(b => b.querySelector('.acc').textContent + ' | ' + b.querySelector('.ot').textContent.slice(0, 50)),
    clipped: [...document.querySelectorAll('.opt .ot')].filter(e => e.scrollWidth > e.clientWidth + 1).length }));
  console.log(JSON.stringify(info, null, 1));
  if (!phone) {
    const o = await page.$$('.opt'); if (o.length > 2) { await o[2].hover(); await page.waitForTimeout(350); await page.screenshot({ path: `${dir}/${tag}-2hover.png` }); }
    await page.mouse.move(5, 5);
    await page.click('#evPeek'); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-3peek.png` });
    await page.click('#evback'); await page.waitForTimeout(300);
  }
  // push them to an option they are okay with (or any not their own)
  const pick = await page.evaluate(() => { const b = [...document.querySelectorAll('.opt')]; const ok = b.find(x => /Okay/.test(x.textContent)) || b.find(x => /Would go/.test(x.textContent)) || b.find(x => !x.classList.contains('own')); return ok ? +ok.dataset.i : -1; });
  // a card is found by its own number: the cards on the page are grouped (and some folded), so their order is not data-i's
  // desktop: the card is held (clicked, on a page without the hold); phone: a tap reads it, then "Push them to this"
  const through = async (k, how) => { if (await page.evaluate((k) => lastCpKey === k && !!document.getElementById('evLet') && !document.getElementById('evwrap').hidden, k)) { logs.push(`push (${how}) did not go through`); process.exitCode = 1; } };
  if (pick >= 0) { const b = await page.$(`.opt[data-i="${pick}"]`), k = await page.evaluate(() => lastCpKey);
    if (!phone) console.log('push:', JSON.stringify(await holdOpt(page, b)));
    else { await b.tap(); await page.waitForTimeout(200); const p = await page.$('#pushIt'); if (p) { await page.screenshot({ path: `${dir}/${tag}-2detail.png` }); await p.click(); } }
    await idle(); await through(k, phone ? 'tap, then Push them to this' : 'hold'); }
  await page.waitForTimeout(900);
  await page.screenshot({ path: `${dir}/${tag}-4resolution.png` });
  console.log('res:', (await page.evaluate(() => (document.querySelector('.ev') || {}).innerText || '')).slice(0, 400).replace(/\n/g, ' | '));
  // one more push on the way, by its number on the keyboard (number keys push at once, with or without the hold)
  let keyed = 0;
  for (let i = 0; i < 25; i++) {
    const s = await state();
    if (!keyed && s.cp && s.ev) { const k = await page.$('#evOpts .opt:not(.own):not(.onone):not(.pass)'); if (k) { const key = await page.evaluate(() => lastCpKey); keyed = await keyOpt(page, k); console.log('key push:', keyed); await idle(); await through(key, 'key ' + keyed); continue; } }
    await next(); const age = await page.evaluate(() => parseFloat((document.querySelector('.who .age b') || {}).textContent || '0')); if (age >= 30) break; }
  const s2 = await state(); if (s2.cp || s2.res) { await page.click('#evPeek'); await page.waitForTimeout(300); }
  await page.screenshot({ path: `${dir}/${tag}-5hud.png` });
  if (phone) { const t = await page.$('#tHud'); if (t) { await t.click(); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-6drawer.png` }); } }
  else { const st = await page.$('.st'); if (st) { await st.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-6state.png` }); } }
  console.log(logs.join('\n'));
  await browser.close();
})();
