const { chromium } = require(process.env.PW || 'playwright');
// v22 patch (Emren 10-07 21:44 UTC): a tribal or magic life shows its own world's tarot card (V The River, VI The Spires)
// wherever an Earth picture would show; an Earth life shows the same pictures as before. One whole life in the browser, as
// drive_life.js plays it (about half the moments chosen, the rest left to the character), with the everyday interlude on
// so its pictures show too. Every picture the page puts in after the life starts is recorded:
//   tribal (preset 5) or magic (preset 6): every picture is that world's tarot card, never an Earth engraving;
//   Earth (any other preset): no tarot card, and each moment's picture is the one v22's picFor gives (by situation, then
//   the original of a child version, then the first life domain, then the tier).
// Also no page error, no sideways scroll and every push taken (v23: the first by its number on the keyboard, then held;
// a phone also taps and pushes with "Push them to this").
//   node test/world_pics.js <url> <shots dir> <tag> <preset> <width> <height> [minutes] [pace: short|slow|off]
const [url, dir, tag, preset, W, H, mins, pace] = process.argv.slice(2);
const { idleOf } = require('./start.js');
const { holdOpt, pushOpt, keyOpt } = require('./hold.js');   // v23: with the Living HUD a pointer pushes a card by holding it
(async () => {
  const phone = +W < 600, logs = [];
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: +H }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript((p) => {
    try { localStorage.setItem('chroma.pace', p); localStorage.removeItem('chroma.autosave'); } catch (_) {}
    window.__pics = []; window.__picsOn = false;
    const note = (img, where) => { if (window.__picsOn && img.getAttribute('src')) window.__pics.push([img.getAttribute('src'), where]); };
    const where = (n) => { const e = n.closest && n.closest('[id]'); return e ? e.id : '?'; };
    new MutationObserver((ms) => { for (const m of ms) {
      if (m.type === 'attributes' && m.target.tagName === 'IMG') note(m.target, where(m.target));
      for (const n of m.addedNodes || []) { if (n.nodeType !== 1) continue; if (n.tagName === 'IMG') note(n, where(n)); n.querySelectorAll && n.querySelectorAll('img').forEach((i) => note(i, where(i))); }
    } }).observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['src'] });
  }, pace || 'short');
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
  await page.evaluate(() => { window.__picsOn = true; });   // the setup's own tarot cards are not counted
  await page.fill('#txt', 'Lale'); await page.click('#go');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 600000 });
  await idle();
  const setting = await page.evaluate(() => hud.life && hud.life.setting);
  const want = { tribal: 'pics/tarot-5.webp', magic: 'pics/tarot-6.webp' }[setting] || null;
  // v22's picFor, as published (Earth lives must read exactly this)
  const OLD = (a) => { if (!a) return ''; const d = String(a.life || '').split(',').map((x) => x.trim()).find((x) => PICS.domain[x]);
    return PICS.situation[a.sit] || PICS.situation[a.variant_of] || (d && PICS.domain[d]) || PICS.tier[a.tier] || ''; };
  let steps = 0, chosen = 0, keyed = 0, held = 0, notThrough = 0, pushedAt = null, noCard = [], left = 0, sideways = 0, moments = 0, il = 0, firstCp = false, firstIl = false, at30 = false;
  const bad = [];
  const t0 = Date.now(), limit = (+mins || 40) * 60000;
  while (Date.now() - t0 < limit) {
    await idle();
    if (await page.evaluate(() => IL.on)) {             // the interlude plays out (its pictures are recorded), or is skipped
      await page.waitForFunction(() => !IL.on, null, { timeout: 30000 }).catch(() => {});
      if (await page.evaluate(() => IL.on)) { const k = await page.$('#tSkip'); if (k) await k.click().catch(() => {}); }
      await page.waitForTimeout(600); continue;
    }
    const s = await page.evaluate((old) => {
      const OLD = eval(old), cp = hud && hud.cp, img = document.querySelector('#evwrap .evart img');
      return { mode: hud && hud.mode, age: hud && hud.life && hud.life.age,
        ev: !document.getElementById('evwrap').hidden, res: !!document.querySelector('#goOn'), cp: !!document.querySelector('#evLet'),
        rn: !!document.querySelector('#rnKeep'), sx: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, key: lastCpKey,
        shown: img ? img.getAttribute('src') : null, old: cp && cp.art ? OLD(cp.art) : null, sit: cp && cp.art ? cp.art.sit : null,
        il: !!document.querySelector('#ilPic img') };
    }, OLD.toString());
    if (s.mode === 'over') break;
    if (pushedAt !== null) { if (s.cp && s.key === pushedAt) notThrough++; pushedAt = null; }   // the same moment still waits: the push was lost
    if (s.sx) sideways++;
    if (s.il && !firstIl) { firstIl = true; await shot('interlude'); }
    if (!at30 && s.age >= 30) { at30 = true; await shot('age30'); }
    steps++;
    if (s.ev && s.rn) { await page.click(Math.random() < 0.5 ? '#rnTake' : '#rnKeep'); continue; }
    if (s.ev && s.res) { await page.click('#goOn'); await page.waitForTimeout(450); }
    else if (s.ev && s.cp) {
      moments++;
      if (!firstCp) { firstCp = true; await shot('moment'); }
      if (want ? s.shown !== want : s.shown !== (s.old || null)) bad.push({ age: s.age, sit: s.sit, shown: s.shown, expected: want || s.old });
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
    } else if (s.ev) {                                   // something else in the window: note it once and look
      if (!bad.some((b) => b.odd)) { await shot('odd'); bad.push({ odd: await page.evaluate(() => document.getElementById('evwrap').innerText.replace(/\s+/g, ' ').slice(0, 200)) }); }
      break;
    } else await page.click('#tMain');
  }
  const end = await page.evaluate(() => ({ mode: hud.mode, age: hud.life && hud.life.age }));
  await page.waitForTimeout(1500); await shot('end');
  const pics = await page.evaluate(() => window.__pics);
  const by = {}; for (const [src, w] of pics) { const k = src + ' @' + w; by[k] = (by[k] || 0) + 1; }
  const tarot = pics.filter(([src]) => /tarot-/.test(src)), other = pics.filter(([src]) => !/tarot-/.test(src));
  il = pics.filter(([, w]) => w === 'ilPic').length;
  const wrong = want ? pics.filter(([src]) => src !== want) : tarot;
  console.log(JSON.stringify({ tag, preset, setting, width: +W, end, steps, moments, chosen, keyed, held, notThrough, noCard, left, sideways, pictures: pics.length, interludePictures: il,
    tarotPictures: tarot.length, otherPictures: other.length, wrongPictures: wrong.length, momentMismatches: bad.length }));
  console.log('pictures by source and place', JSON.stringify(by));
  if (wrong.length) console.log('wrong', JSON.stringify(wrong.slice(0, 10)));
  if (bad.length) console.log('moment mismatches', JSON.stringify(bad.slice(0, 10)));
  console.log('errors', JSON.stringify(logs.slice(0, 10)), logs.length);
  const ok = end.mode === 'over' && moments > 0 && pics.length > 0 && !wrong.length && !bad.length && !sideways && !notThrough && !logs.length;
  console.log(`world pictures ${tag}: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close();
  process.exit(ok ? 0 : 1);
})();
