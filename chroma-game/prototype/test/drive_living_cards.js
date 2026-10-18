const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD, the cards (row V4; plan: the Living HUD in v23, decisions 1, 7 and 8): the hold, the weight on today's
// cards and the outcome's refocus (web/src/living/40-cards.js). Each part prints its checks and PASS or FAIL; the driver
// exits 1 on a FAIL, a page error or any console error.
//   desk   1280x800, a mouse, Living on: #table[data-hold="on"] and every card's data-hold (their own pick 0, the rest 400
//          to 1700 ms, heavier never shorter); the hint names the hold. At the first moment a plain click on another
//          card does not push; a press let go early does not push (the card shows the fill while pressed); a hold of the
//          card's time pushes and its outcome comes, with the refocus on its picture. Then, a moment each: a click on
//          their own pick pushes at once; a number key pushes; "Let them choose" (#evLet) acts at once; Enter on a
//          focused card pushes; a lean turns no card; on an opened "Out of reach" fold a hold pushes. Last the Table
//          menu's Living HUD row is turned off: #table and the cards lose the hold and a plain click pushes again.
//   touch  390x844, touch: the hint for touch; a tap reads the card (.optdetail) and does not push; a second tap on the
//          same card reads again; "Push them to this" (#pushIt) pushes. Next moment: a touch held for the card's time
//          (CDP Input.dispatchTouchEvent) pushes; no long-press menu (contextmenu is cancelled on cards, the callout and
//          text selection are off).
//   shots  a moment, a hold half way, and the outcome's refocus half way, at 1440x900 and 390x844, with motion full,
//          calm and off (the Table menu's Motion row): living-cards-<w>-<motion>-{moment,hold,outcome}.png. With motion
//          off there is no refocus and the cards stand still (two shots 0.8 s apart are equal).
//   cost   1440x900 at pixel ratio 2, 20 s of play (hovering every card, a hold, its outcome and refocus, the next moment):
//          the piece's own time each frame (its entry points add up their time; CH.pieces.get("cards").cost()), mean and
//          95th percentile, and the frame interval.
// The life is always the same one: preset 4 (starts at 14) with seed 140892, as drive_living.js sets it.
// The hold follows the contract that test/hold.js serves the other drivers: read the card's data-hold, press at its
// centre, wait data-hold + 250 ms, let go (touch: CDP touchStart and touchEnd at the centre).
//   PW=<playwright> node test/drive_living_cards.js URL OUT_DIR [parts: desk,touch,shots,cost] [preset 4] [seed 140892]
const { startLife, idleOf } = require('./start.js');
const fs = require('fs');
const [url, dir, partsArg, preset, seedArg] = process.argv.slice(2);
const parts = (partsArg || 'desk,touch,shots,cost').split(','), P = preset || '4', SEED = seedArg || '140892';
const say = (...a) => console.log(...a);
const fails = [], logs = [];
const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
const t0 = Date.now();

(async () => {
  const browser = await chromium.launch();
  // a page at a size, its life started (always the same life) and the probes in it
  async function open(width, height, opts = {}) {
    const touch = !!opts.touch;
    const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: touch, isMobile: touch, deviceScaleFactor: opts.dpr || 1 });
    await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave');
      localStorage.setItem('chroma.motion', 'full'); localStorage.setItem('chroma.look', 'ink'); localStorage.removeItem('chroma.oorOpen'); } catch (_) {} });
    const page = await ctx.newPage();
    const tag = `${width}x${height}`;
    page.on('pageerror', (e) => logs.push(`${tag} pageerror: ${e.message}`));
    page.on('console', (m) => { if (m.type() === 'error') logs.push(`${tag} console error: ${m.text()}`); });
    await page.goto(url);
    await page.waitForFunction(() => window.CH && CH.pieces && CH.pieces.has('cards') && CH.life, null, { timeout: 120000 });
    await startLife(page, P, 'Lale');
    const idle = idleOf(page, logs);
    await idle();
    if (SEED !== '-') {              // the same life every run: this start with the seed, loaded back
      let t = null; for (let i = 0; i < 4 && !t; i++) { t = await page.evaluate(() => askSave()); if (!t) await page.waitForTimeout(1000); }
      const d = JSON.parse(t); d.setup.seed = +SEED; d.inputs = [];
      await page.evaluate((x) => loadText(x), JSON.stringify(d));
      await page.waitForFunction(() => hud && hud.replay, null, { timeout: 120000 }).catch(() => {});
      await page.waitForFunction(() => hud && !hud.replay && !busy && hud.mode === 'play', null, { timeout: 600000 });
      await page.waitForTimeout(1500); await idle();
    }
    // the probes: every pick the page sends (the "pick" event), every refocus laid on a picture, every flyer
    await page.evaluate(() => {
      const T = window.__lc = { picks: [], rf: 0, flyers: 0, menus: [] };
      CH.on('pick', (x) => T.picks.push({ text: x.text, key: x.cp.age + '|' + x.cp.title }));
      new MutationObserver((rs) => rs.forEach((r) => r.addedNodes.forEach((n) => { if (n.nodeType !== 1) return;
        if (n.classList.contains('lv-rf')) T.rf++; if (n.classList.contains('flyer')) T.flyers++; }))).observe(document.body, { childList: true, subtree: true });
      document.addEventListener('contextmenu', (e) => T.menus.push(e.defaultPrevented));
    });
    const cdp = touch ? await ctx.newCDPSession(page) : null;
    return { ctx, page, idle, cdp, touch, width, height };
  }
  const shotOf = (page) => (n) => page.screenshot({ path: `${dir}/living-cards-${n}.png`, scale: 'css' });

  // where the page stands
  const state = (page) => page.evaluate(() => { const up = !document.getElementById('evwrap').hidden;
    return { cp: !!hud.cp && up && !!document.getElementById('evLet'), res: !!hud.res && up && !!document.getElementById('goOn'), rn: !!document.querySelector('#rnKeep'),
      key: lastCpKey, busy, choosing: !!choosing, mode: hud.mode, age: hud.life && hud.life.age, picks: __lc.picks.length, fold: !!document.getElementById('evOOR') }; });
  // on to the next moment: keep a rename, Go on after an outcome, live on to the moment
  async function toMoment(S) {
    for (let i = 0; i < 400; i++) {
      await S.idle();
      const s = await state(S.page);
      if (s.mode !== 'play') throw new Error('the life left play at ' + s.age);
      if (s.cp) { await S.page.waitForTimeout(400); return s; }
      if (s.rn) { await S.page.click('#rnKeep'); continue; }
      if (s.res) { await S.page.evaluate(() => document.getElementById('goOn').click()); continue; }
      await S.page.evaluate(() => send(''));
    }
    throw new Error('no moment came');
  }
  // after an action: did it push? (a pick was sent and its outcome came) or did nothing happen? (the same moment waits)
  async function pushed(S, before, why) {
    const ok = await S.page.waitForFunction((n) => __lc.picks.length > n && hud.res && !document.getElementById('evwrap').hidden && document.getElementById('goOn'), before.picks, { timeout: 60000 }).then(() => true, () => false);
    await S.idle();
    const s = await state(S.page);
    check(ok && s.res, `${why}: pushed, and its outcome came (${ok ? 'pick "' + (await S.page.evaluate(() => __lc.picks[__lc.picks.length - 1].text)) + '"' : 'no pick'})`);
    return ok;
  }
  async function still(S, before, why) {
    await S.page.waitForTimeout(900);
    const s = await state(S.page);
    check(s.cp && !s.busy && !s.choosing && s.key === before.key && s.picks === before.picks, `${why}: no push, the moment still waits`);
  }
  // the cards on screen, their numbers, holds and kinds
  const cards = (page) => page.evaluate(() => [...document.querySelectorAll('#table .opt[data-i]')].filter((b) => b.offsetParent).map((b) => {
    const o = hud.cp.options[+b.dataset.i];
    return { num: b.dataset.num, hold: b.dataset.hold, own: !!o.own, far: o.status === 'out of reach', acc: o.own ? 'own' : o.accept, pass: !o.means.length, cls: b.className, sel: `#table .opt[data-num="${b.dataset.num}"]` };
  }));
  // the hold, by the contract: press the card's centre for data-hold + 250 ms (mid(): called half way, e.g. for a shot)
  async function hold(S, sel, opt = {}) {
    const page = S.page;
    await page.$eval(sel, (b) => b.scrollIntoView({ block: 'center' }));
    await page.waitForTimeout(150);
    const ms = +(await page.$eval(sel, (b) => b.dataset.hold || 0)), bb = await (await page.$(sel)).boundingBox();
    const x = bb.x + bb.width / 2, y = bb.y + bb.height / 2, wait = opt.early ? Math.round(ms * 0.4) : ms + 250;
    if (S.touch) await S.cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
    else { await page.mouse.move(x, y, { steps: 3 }); await page.waitForTimeout(120); await page.mouse.down(); }
    let seen = null;
    if (opt.mid) { await page.waitForTimeout(Math.round(Math.min(wait, ms) * 0.55)); seen = await opt.mid(); await page.waitForTimeout(Math.max(0, wait - Math.round(Math.min(wait, ms) * 0.55))); }
    else await page.waitForTimeout(wait);
    if (S.touch) await S.cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    else await page.mouse.up();
    return { ms, seen };
  }
  // the fill as the card shows it: holding, and how far its wash has come (0 to 1)
  const fillOf = (page, sel) => page.$eval(sel, (b) => { const i = b.querySelector('.lv-hold > i'); if (!i) return { holding: false, p: -1 };
    const t = getComputedStyle(i).transform, m = t && t !== 'none' ? new DOMMatrix(t) : new DOMMatrix(), w = i.offsetWidth || 1; return { holding: b.classList.contains('lv-holding'), p: +(1 + m.m41 / w).toFixed(2) }; });
  const menuRow = (page, what) => page.evaluate((w) => { if (!menuOpen) document.getElementById('tMenu').click(); const b = document.querySelector(`#tPop [data-${w}]`); if (b) b.click(); setMenu(false);
    return { motion: document.documentElement.dataset.motion, living: document.documentElement.dataset.living }; }, what);
  const lightest = (cs) => cs.filter((c) => !c.own && !c.pass && c.hold > 0).sort((a, b) => a.hold - b.hold)[0];
  const heaviest = (cs) => cs.filter((c) => !c.own && c.hold > 0).sort((a, b) => b.hold - a.hold)[0];

  if (parts.includes('desk')) {
    say('part desk (1280x800, mouse)');
    const S = await open(1280, 800), page = S.page;
    say('  started', Math.round((Date.now() - t0) / 1000), 's');
    let s = await toMoment(S), cs = await cards(page);
    const top = await page.evaluate(() => ({ hold: document.getElementById('table').dataset.hold || null, hint: (document.querySelector('#evOpts > .ask small') || {}).textContent }));
    check(top.hold === 'on', '#table carries data-hold="on" while the cards piece is mounted');
    check(top.hint === 'hover to read · hold, or press its number, to push', `the hint names the hold ("${top.hint}")`);
    const RANK = { own: 0, 'would go with it': 1, 'okay with it': 2, reluctant: 3, 'against it': 4 };
    const bad = cs.filter((c) => c.hold == null || (c.own ? c.hold !== '0' : !(+c.hold >= 400 && +c.hold <= 1700)));
    const order = cs.every((a) => cs.every((b) => !(RANK[a.acc] < RANK[b.acc] && a.far === b.far) || +a.hold <= +b.hold));
    check(cs.length > 0 && !bad.length && order, `every card has its hold: own 0, the rest 400 to 1700 ms, heavier never shorter (${cs.map((c) => `${c.num}:${c.hold}${c.far ? '~' : ''}`).join(' ')})`);
    check(cs.every((c) => /\blv\b/.test(c.cls)) && cs.some((c) => /lv-heavy|lv-mid|lv-light/.test(c.cls)), 'every card is dressed with its weight');
    // a plain click on another card does not push
    const c1 = lightest(cs);
    await page.click(c1.sel); await still(S, s, `a plain click on card ${c1.num} (hold ${c1.hold} ms)`);
    // let go early: the card fills while pressed, then nothing
    s = await state(page);
    const e1 = await hold(S, c1.sel, { early: true, mid: () => fillOf(page, c1.sel) });
    check(e1.seen && e1.seen.holding, `pressed, the card is holding (${JSON.stringify(e1.seen)})`);
    await still(S, s, `let go after ${Math.round(e1.ms * 0.4)} of ${e1.ms} ms`);
    check(!(await fillOf(page, c1.sel)).holding, 'let go, the card empties');
    // the hold pushes
    s = await state(page);
    const rf0 = await page.evaluate(() => __lc.rf), want = await page.evaluate((n) => { const o = CPNUM.get(+n); return o ? (o.own ? '' : String(o.n)) : '?'; }, c1.num);
    const h1 = await hold(S, c1.sel, { mid: () => fillOf(page, c1.sel) });
    check(h1.seen && h1.seen.holding && h1.seen.p > 0.05 && h1.seen.p < 1, `half way through the hold the card has filled part way (${JSON.stringify(h1.seen)})`);
    if (await pushed(S, s, `a hold of card ${c1.num} for ${c1.hold} + 250 ms`)) check((await page.evaluate(() => __lc.picks[__lc.picks.length - 1].text)) === want, `the pick sent is the card held ("${want}")`);
    check(await page.evaluate((n) => __lc.rf > n, rf0), 'the outcome\'s picture refocuses (motion full)');
    // a moment each for the rest; the fold whenever one comes
    const todo = ['own', 'key', 'let', 'enter', 'lean'];
    let foldDone = false, offDone = false;
    for (let guard = 0; guard < 16 && !offDone; guard++) {
      s = await toMoment(S); cs = await cards(page);
      let job;
      if (!foldDone && s.fold) job = 'fold';
      else if (todo.length) job = todo.shift();
      else if (foldDone || guard >= 10) job = 'off';
      else { await page.click('#evLet'); await S.idle(); continue; }          // waiting for a moment with a fold
      say('  moment at', s.age.toFixed(2), '->', job);
      if (job === 'own') {
        const c = cs.find((x) => x.own); if (!c) { todo.unshift('own'); await page.click('#evLet'); await S.idle(); continue; }
        await page.click(c.sel); await pushed(S, s, `a click on their own pick (card ${c.num}, hold ${c.hold})`);
      } else if (job === 'key') {
        const c = lightest(cs); if (!c || +c.num > 9) { todo.unshift('key'); await page.click('#evLet'); await S.idle(); continue; }
        await page.mouse.move(2, 2); await page.keyboard.press(String(c.num)); await pushed(S, s, `number key ${c.num}`);
      } else if (job === 'let') {
        await page.click('#evLet'); await pushed(S, s, '"Let them choose" (#evLet)');
      } else if (job === 'enter') {
        const c = lightest(cs);
        await page.$eval(c.sel, (b) => b.focus()); await page.keyboard.press('Enter'); await pushed(S, s, `Enter on focused card ${c.num}`);
      } else if (job === 'lean') {
        const f0 = await page.evaluate(() => __lc.flyers);
        await page.click('#evLean [data-lc]');
        const ok = await page.waitForFunction(() => hud.res && !document.getElementById('evwrap').hidden && document.getElementById('goOn'), null, { timeout: 60000 }).then(() => true, () => false);
        await S.idle();
        const f = await page.evaluate(() => ({ flyers: __lc.flyers, held: document.querySelectorAll('.opt.lv-held').length }));
        check(ok && f.flyers === f0 && !f.held, `a lean: its outcome came and no card turned (${JSON.stringify(f)})`);
      } else if (job === 'fold') {
        foldDone = true;
        const open = await page.evaluate(() => document.getElementById('evOOR').getAttribute('aria-expanded') === 'true');
        if (!open) { await page.click('#evOOR'); await page.waitForTimeout(300); }
        cs = await cards(page);
        const c = heaviest(cs.filter((x) => x.far));
        check(!!c && +c.hold >= 750, `an opened fold's card has its hold (${c ? c.num + ':' + c.hold : 'none'})`);
        if (c) { await hold(S, c.sel); await pushed(S, s, `a hold on the out-of-reach card ${c.num} (${c.hold} ms)`); }
      } else if (job === 'off') {
        offDone = true;
        const r = await menuRow(page, 'lv'); await page.waitForTimeout(400);
        const o = await page.evaluate(() => ({ hold: document.getElementById('table').dataset.hold || null, dressed: document.querySelectorAll('#table .lv, #table [data-hold], #table .lv-lift').length,
          hint: (document.querySelector('#evOpts > .ask small') || {}).textContent }));
        check(r.living === 'off' && !o.hold && !o.dressed, `Living off: #table and the cards lose the hold (${JSON.stringify({ ...r, ...o })})`);
        check(o.hint === 'hover to read · click or press its number to push', 'Living off: today\'s hint again');
        await shotOf(page)('1280-off-moment');
        s = await state(page); cs = await cards(page);
        const c = cs.find((x) => !x.own && !x.pass) || cs[0]; await page.click(c.sel); await pushed(S, s, `Living off: a plain click on card ${c.num}`);
        const r2 = await menuRow(page, 'lv');
        check(r2.living === 'on', 'Living on again');
      }
    }
    check(!todo.length && foldDone && offDone, `every desk step ran (${[...todo, foldDone ? '' : 'fold', offDone ? '' : 'off'].filter(Boolean).join(' ') || 'all'})`);
    await S.ctx.close();
  }

  if (parts.includes('touch') || parts.includes('shots')) {
    say('part touch (390x844, touch)');
    const S = await open(390, 844, { touch: true }), page = S.page, shot = shotOf(page);
    let s = await toMoment(S), cs = await cards(page);
    if (parts.includes('touch')) {
      const hint = await page.evaluate(() => (document.querySelector('#evOpts > .ask small') || {}).textContent);
      check(hint === 'tap to read · hold or tap Push to push', `the hint for touch ("${hint}")`);
      const css = await page.$eval(cs[0].sel, (b) => { const st = getComputedStyle(b); return { callout: st.webkitTouchCallout || st.getPropertyValue('-webkit-touch-callout'), select: st.userSelect || st.webkitUserSelect }; });
      check(css.select === 'none' && (!css.callout || css.callout === 'none'), `on cards the callout and text selection are off (${JSON.stringify(css)})`);
      const c = lightest(cs);
      await page.$eval(c.sel, (b) => b.scrollIntoView({ block: 'center' }));
      await page.tap(c.sel); await page.waitForTimeout(500);
      let d = await page.evaluate((sel) => ({ detail: !!document.querySelector('#table .optdetail #pushIt'), sel: document.querySelector(sel).classList.contains('sel') }), c.sel);
      check(d.detail && d.sel, `a tap on card ${c.num} reads it (.optdetail with #pushIt)`);
      await still(S, s, 'a tap');
      await shot('390-touch-read');
      await page.tap(c.sel); await page.waitForTimeout(500);
      d = await page.evaluate((sel) => ({ detail: document.querySelectorAll('#table .optdetail').length, sel: document.querySelector(sel).classList.contains('sel') }), c.sel);
      check(d.detail === 1 && d.sel, 'a second tap on the same card reads it again');
      await still(S, s, 'a second tap');
      const m0 = await page.evaluate(() => __lc.menus.length);
      const prevented = await page.$eval(c.sel, (b) => { const e = new MouseEvent('contextmenu', { bubbles: true, cancelable: true }); b.dispatchEvent(e); return e.defaultPrevented; });
      check(prevented, 'a long-press menu on a card is cancelled');
      await page.tap('#pushIt'); await pushed(S, s, '"Push them to this" (#pushIt)');
      s = await toMoment(S); cs = await cards(page);
      const h = heaviest(cs);
      const m1 = await page.evaluate(() => __lc.menus.length);
      await hold(S, h.sel);
      await pushed(S, s, `a touch held on card ${h.num} for ${h.hold} + 250 ms`);
      const menus = await page.evaluate((n) => __lc.menus.slice(n), m1);
      check(menus.every((x) => x), `no context menu during the touch hold (${menus.length} contextmenu events, all cancelled)`);
      say('  (', m1 - m0, 'synthetic contextmenu)');
    }
    if (parts.includes('shots')) await shots(S, '390');
    await S.ctx.close();
  }

  // a moment, a hold half way and the refocus half way, in each motion (Table menu's Motion row: full, calm, off)
  async function shots(S, w) {
    say(`part shots (${w})`);
    const page = S.page, shot = shotOf(page);
    for (const m of ['full', 'calm', 'off']) {
      let s = await toMoment(S);
      let now = await page.evaluate(() => document.documentElement.dataset.motion);
      for (let i = 0; i < 3 && now !== m; i++) now = (await menuRow(page, 'lk="motion"')).motion;
      check(now === m, `motion ${m}`);
      await page.waitForTimeout(600);
      await shot(`${w}-${m}-moment`);
      if (m === 'off') {
        const box = await page.$('#evOpts'), a = await box.screenshot(), b = (await page.waitForTimeout(800), await box.screenshot());
        check(Buffer.compare(a, b) === 0, 'motion off: the cards stand still (two shots 0.8 s apart are equal)');
      }
      const cs = await cards(page), c = heaviest(cs.filter((x) => !x.pass)) || heaviest(cs);
      const rf0 = await page.evaluate(() => __lc.rf);
      await hold(S, c.sel, { mid: () => shot(`${w}-${m}-hold`) });
      const got = await page.waitForFunction((n) => __lc.rf > n, rf0, { timeout: m === 'off' ? 4000 : 20000 }).then(() => true, () => false);
      if (got) await page.waitForTimeout(m === 'calm' ? 900 : 560);
      else await page.waitForFunction(() => hud.res && document.getElementById('goOn'), null, { timeout: 30000 }).catch(() => {});
      await shot(`${w}-${m}-outcome`);
      check(m === 'off' ? !got : got, `${m}: ${m === 'off' ? 'no refocus' : 'the outcome\'s picture refocuses'}`);
      await S.idle();
    }
    await menuRow(page, 'lk="motion"');          // back to full
  }

  if (parts.includes('shots') || parts.includes('cost')) {
    const S = await open(1440, 900, { dpr: 2 }), page = S.page;
    if (parts.includes('shots')) await shots(S, '1440');
    if (parts.includes('cost')) {
      say('part cost (1440x900, pixel ratio 2, 20 s)');
      await page.evaluate(() => { const T = window.__fc = { c: [], dt: [] }, f = CH.pieces.get('cards').cost; let last = f(), lt = performance.now();
        const tick = (t) => { const c = f(); T.c.push(c - last); T.dt.push(t - lt); last = c; lt = t; if (!T.stop) requestAnimationFrame(tick); }; requestAnimationFrame(tick); });
      const tEnd = Date.now() + 20000; let pushes = 0;
      while (Date.now() < tEnd) {
        const s = await state(page);
        if (s.cp && !s.busy) {
          const cs = await cards(page);
          for (const c of cs) { if (Date.now() > tEnd - 4000) break; const bb = await (await page.$(c.sel)).boundingBox().catch(() => null); if (bb) await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 6 }); await page.waitForTimeout(120); }
          const c = lightest(cs) || heaviest(cs);
          if (c && Date.now() < tEnd - 3000) { await hold(S, c.sel); pushes++; await page.waitForTimeout(1800); }
        } else if (s.res && !s.busy) await page.evaluate(() => document.getElementById('goOn').click());
        else if (!s.busy && !s.cp) await page.evaluate(() => send(''));
        await page.waitForTimeout(300);
      }
      const r = await page.evaluate(() => { const T = __fc; T.stop = true; const q = (xs, p) => { const s = xs.slice().sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor(p * s.length))] || 0; };
        const mean = (xs) => xs.reduce((a, b) => a + b, 0) / Math.max(1, xs.length);
        return { frames: T.c.length, mean: +mean(T.c).toFixed(4), p95: +q(T.c, 0.95).toFixed(4), max: +Math.max(0, ...T.c).toFixed(3), total: +T.c.reduce((a, b) => a + b, 0).toFixed(2),
          dtMean: +mean(T.dt.slice(1)).toFixed(2), dtP95: +q(T.dt.slice(1), 0.95).toFixed(2) }; });
      say(`  frame cost of the cards piece over 20 s: mean ${r.mean} ms, p95 ${r.p95} ms, max ${r.max} ms, ${r.total} ms in all over ${r.frames} frames; frame interval mean ${r.dtMean} ms, p95 ${r.dtP95} ms; ${pushes} holds`);
      fs.writeFileSync(`${dir}/living-cards-cost.json`, JSON.stringify({ ...r, pushes }, null, 1));
      check(r.frames > 300 && r.mean <= 4 && r.p95 <= 8, `within the budget (all pieces: mean 4 ms, p95 8 ms a frame)`);
    }
    await S.ctx.close();
  }

  console.log(logs.slice(0, 20).join('\n') || 'no page errors, no console errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_cards ${parts.join(',')}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})().catch((e) => { console.log('drive_living_cards: FAIL', e && e.stack || e); console.log(logs.slice(0, 20).join('\n')); process.exit(1); });
