const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD, row V6: the life's window (web/src/living/60-window.js). Each part prints its checks and PASS or FAIL;
// the driver exits 1 on a FAIL, a page error or a console error (a picture the server lacks is not counted).
//   medal   a life to AGE: the medallion sits in the Status panel's crest (right, 46 px; in the narrow screens' drawer,
//           36 px under its close button) over none of the crest's other parts, and adds no height to it (the drawer's
//           crest keeps at least 92 px); the same medallion stays across the HUD's rebuilds; its glass is glazed; a hover
//           (a tap on a phone) and the arrow keys read a year; no sideways scroll; shots in motion full, calm and off
//           (off: two shots 0.8 s apart equal); the switch off (no medallion, the crest as today), on (back); the
//           window's own script per frame over SECONDS of a running life (mean and p95), and any task over 50 ms meanwhile.
//   end     a life that starts old (a save of preset 3 with its setup's start_age set to START and the seed SEED, loaded
//           back), played to its end with their own picks: the full window in the review where the ink look's portrait
//           was (.lk-final hidden), their name and years beneath; #again and #rvBook never covered; the light waits for
//           the "Finis" plate, then lights up in about 11 s ("lighting" to "lit"; it waits while scrolled out of view);
//           during it Enter (kept from the page), Space on a button (it opens the Book) and Esc (it closes the Book) do
//           not skip; a hover reads a year; the script per frame while it lights and once lit; the switch off (the
//           portrait back), on (the window back, lit); #again then starts a new life, the window gone.
//   skip    the same old life to its end three more times: Space (focus on no button), a click in the review and Esc each
//           skip the light to "lit" at once.
//   still   the same old life to its end with motion off: lit at once, and two shots 0.8 s apart are equal.
//   PW=<playwright> node test/drive_living_window.js URL OUT_DIR [parts: medal,end,skip,still] [width 1440] [height 900]
//     [age 30] [start 76] [seed 140892] [seconds 20]
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, toAge, startArg, seedArg, secArg] = process.argv.slice(2);
const parts = (partsArg || 'medal').split(','), width = +(W || 1440), height = +(H || 900), AGE = +(toAge || 30);
const START = +(startArg || 76), SEED = +(seedArg || 140892), SECONDS = +(secArg || 20);
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600, logs = [], warns = [], fails = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone });
  // the per-piece guard (living/00-core.js) only reports here: on a slow headless machine it would hold the piece still,
  // and this driver checks the piece's own motion (test/drive_living.js joint checks the guard)
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.setItem('chroma.living.guard', 'off'); localStorage.setItem('chroma.motion', 'full'); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { const t = m.text();
    if (m.type() === 'error' && !/Failed to load resource|net::|CERT/.test(t)) logs.push(`console error: ${t}`);
    else if (m.type() === 'warning' && /^living/.test(t)) warns.push(`console warning: ${t}`); });
  const tag = `${width}x${height}`, shot = (n, clip) => page.screenshot({ path: `${dir}/window-${tag}-${n}.png`, ...(clip ? { clip } : {}) });
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.pieces && CH.pieces.has('window') && CH.life, null, { timeout: 120000 });
  // the window's own script time: every frame function it starts (CH.frame), its update and its hooks, by animation frame.
  // Only the window's frames: the other pieces start theirs again when Living comes back on (the sky's in its mount), and
  // the core names the piece starting one (CH.owner(), living/00-core.js)
  await page.evaluate(() => {
    const T = window.__w = { acc: 0, frames: [], on: false, long: [] };
    const timed = (f) => function (...a) { const s = performance.now(); try { return f.apply(this, a); } finally { T.acc += performance.now() - s; } };
    const mine = () => !CH.owner || !CH.owner() || CH.owner() === 'window';
    const f0 = CH.frame; CH.frame = (fn, el) => f0(mine() ? timed(fn) : fn, el);
    const p = CH.pieces.get('window'); p.update = timed(p.update); for (const k in p.hooks) p.hooks[k] = timed(p.hooks[k]);
    T.start = () => { T.frames = []; T.acc = 0; T.long = []; T.on = true; const k = () => { T.frames.push(T.acc); T.acc = 0; if (T.on) requestAnimationFrame(k); }; requestAnimationFrame(k); };
    T.stop = () => { T.on = false; const f = T.frames.slice(1).sort((a, b) => a - b), n = f.length || 1;
      return { frames: f.length, mean: f.reduce((s, v) => s + v, 0) / n, p95: f[Math.min(f.length - 1, Math.floor(f.length * 0.95))] || 0, max: f[f.length - 1] || 0, long: T.long.slice() }; };
    try { new PerformanceObserver((l) => { if (T.on) l.getEntries().forEach((e) => T.long.push(Math.round(e.duration))); }).observe({ type: 'longtask', buffered: false }); } catch (_) {}
  });
  const cost = async (what, ms, during) => {
    await page.evaluate(() => __w.start());
    const t1 = Date.now(); if (during) await during(); const left = ms - (Date.now() - t1); if (left > 0) await page.waitForTimeout(left);
    const c = await page.evaluate(() => __w.stop());
    say(`  cost ${what}: ${c.frames} frames, script ${c.mean.toFixed(3)} ms mean, ${c.p95.toFixed(3)} ms p95, ${c.max.toFixed(2)} ms max; tasks over 50 ms (all of the page): ${c.long.length ? c.long.join(' ') : 'none'}`);
    return c;
  };
  const menuRow = async (sel) => { await page.click('#tMenu'); await page.waitForTimeout(250); await page.click(`#tPop ${sel}`); await page.waitForTimeout(350); await page.keyboard.press('Escape').catch(() => {}); await page.waitForTimeout(150); };
  const setMotion = async (m) => { for (let i = 0; i < 3 && await page.evaluate(() => document.documentElement.dataset.motion) !== m; i++) await menuRow('[data-lk="motion"]'); };
  const living = (on) => page.evaluate(() => document.documentElement.dataset.living).then(async (v) => { if ((v === 'on') !== on) await menuRow('[data-lv]'); });
  const box = (sel) => page.evaluate((q) => { const e = document.querySelector(q); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; }, sel);
  const same = (a, b) => a.length === b.length && a.equals(b);
  // a step on, as a player who leaves every choice to them would: Keep a rename, else Enter (their own pick, Go on, live on)
  const step = async () => {
    await idle();
    const s = await page.evaluate(() => ({ mode: hud.mode, age: hud.life && hud.life.age, rn: !!document.querySelector('#rnKeep') }));
    if (s.mode !== 'play') return s;
    if (s.rn) { await page.click('#rnKeep').catch(() => {}); await page.waitForTimeout(300); return s; }
    await page.evaluate(() => send('')); return s;
  };
  const glazed = () => page.evaluate(() => {   // how much of the medallion's glass has colour (a share of its pixels)
    const c = document.querySelector('.hud-medal canvas.chw-glass'); if (!c || !c.width) return -1;
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0, k = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i + 3] < 200) continue; n++; const mx = Math.max(d[i], d[i + 1], d[i + 2]), mn = Math.min(d[i], d[i + 1], d[i + 2]); if (mx > 60 && mx - mn > 50) k++; }
    return n ? k / n : 0; });
  const crest = () => page.evaluate(() => { const c = document.querySelector('#hud .crestbox'), m = document.querySelector('#hud .crestbox .hud-medal');
    const r = c && c.getBoundingClientRect(), mr = m && m.getBoundingClientRect(), p = c && c.querySelector('.lk-pc.crest'), pr = p && p.getBoundingClientRect();
    return { h: r ? Math.round(r.height * 10) / 10 : -1, medal: mr ? [Math.round(mr.right - r.right), Math.round(mr.top - r.top), mr.width, mr.height] : null, portrait: pr ? [Math.round(pr.left - r.left), Math.round(pr.top - r.top)] : null,
      kept: !!(m && m.__kept), cls: !!(c && c.classList.contains('chw-crest')), chw: document.querySelectorAll('.chw').length,
      // what of the crest the medallion lies over: its other parts, the drawer's close button
      over: mr ? [...c.children, document.getElementById('hudClose')].filter((e) => e && e !== m && getComputedStyle(e).display !== 'none').filter((e) => { const b = e.getBoundingClientRect();
        return b.width && !(b.right <= mr.left || mr.right <= b.left || b.bottom <= mr.top || mr.bottom <= b.top); }).map((e) => e.id || e.className) : [] }; });
  const openHud = async () => { if (!phone) return; await page.click('#evPeek', { timeout: 1500 }).catch(() => {}); await page.click('#tHud').catch(() => {}); await page.waitForTimeout(500); };
  const closeHud = async () => { if (!phone) return; await page.click('#hudClose').catch(() => {}); await page.waitForTimeout(300); };

  if (parts.includes('medal')) {
    say('part medal');
    await startLife(page, '3', 'Lale');
    for (let i = 0; i < 6; i++) await step();
    await idle(); await page.waitForTimeout(1200);
    await openHud();
    let c = await crest();
    say('  crest', JSON.stringify(c));
    const drawer = width <= 1040, want = drawer ? [-3, 31, 36] : [-2, 2, 46];
    check(!!c.medal && c.medal[2] === want[2] && c.medal[3] === want[2] && Math.abs(c.medal[0] - want[0]) <= 1 && Math.abs(c.medal[1] - want[1]) <= 1 && c.cls,
      `the medallion sits in the crest, ${drawer ? 'under the drawer\'s close button' : 'top right'}, ${want[2]} px`);
    check(!c.over.length, `the medallion lies over none of the crest's other parts${c.over.length ? ' (' + c.over.join(', ') + ')' : ''}`);
    check(c.chw === 1, 'one window on the page while they live');
    const g1 = await glazed();
    check(g1 > 0.02, `the years lived are glazed (${(g1 * 100).toFixed(1)}% of the medallion's pixels in colour at age ${await page.evaluate(() => hud.life.age.toFixed(1))})`);
    const mb = await box('.hud-medal');
    await shot('medal-1', { x: mb.x - 260, y: mb.y - 8, width: 320, height: 130 });
    // the same medallion across the HUD's rebuilds
    await page.evaluate(() => { document.querySelector('.hud-medal').__kept = 1; });
    await closeHud();
    for (let i = 0; i < 4; i++) await step();
    await idle(); await page.waitForTimeout(800); await openHud();
    c = await crest();
    check(c.kept && c.cls && c.chw === 1, 'the same medallion is back in the rebuilt crest');
    // a year read by hover (a tap on a phone) and by the arrow keys
    const m = await box('.hud-medal canvas.chw-glass');
    const R = m.width * 0.48 / 1.22, at = { x: m.x + m.width / 2, y: m.y + m.height / 2 - R * 0.17 };
    if (phone) await page.touchscreen.tap(at.x, at.y); else await page.mouse.move(at.x, at.y);
    await page.waitForTimeout(400);
    const tip = await page.evaluate(() => { const t = document.getElementById('tip'); return t.hidden ? '' : t.innerText.replace(/\s+/g, ' ').slice(0, 160); });
    check(/^Age 0\b/.test(tip), `a ${phone ? 'tap' : 'hover'} on the first ring reads age 0 ("${tip}")`);
    if (!phone) await page.mouse.move(2, 2);
    await page.focus('.hud-medal canvas.chw-glass'); await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(250);
    const said = await page.evaluate(() => document.querySelector('.hud-medal .chw-sr').textContent);
    check(/^Age \d+\. /.test(said), `the arrow keys read a year aloud ("${said.slice(0, 90)}")`);
    await page.evaluate(() => document.activeElement && document.activeElement.blur());
    if (!phone) await page.mouse.move(2, 2);
    await page.evaluate(() => hideTip());
    // no sideways scroll; the crest's height with the medallion and without (the switch)
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'no sideways scroll');
    await closeHud();
    for (const mo of ['full', 'calm', 'off']) {
      await setMotion(mo); await openHud(); await page.waitForTimeout(900);
      const b = await box('.hud-medal');
      const clip = { x: Math.max(0, b.x - 4), y: Math.max(0, b.y - 4), width: b.width + 8, height: b.height + 8 };
      await shot(`medal-${mo}`); const a1 = await page.screenshot({ clip });
      await page.waitForTimeout(800); const a2 = await page.screenshot({ clip });
      if (mo === 'off') check(same(a1, a2), 'motion off: the medallion is still (two shots 0.8 s apart equal)');
      else say(`  motion ${mo}: the medallion ${same(a1, a2) ? 'is still at rest' : 'moves'} (shots 0.8 s apart)`);
      await closeHud();
    }
    await setMotion('full');
    await openHud(); const hOn = (await crest()).h; await closeHud();
    await living(false); await openHud();
    const off = await crest(); const fin = await page.evaluate(() => ({ chw: document.querySelectorAll('.chw, .hud-medal, .chw-crest').length, living: document.documentElement.dataset.living }));
    check(fin.living === 'off' && fin.chw === 0 && !off.medal, `off: no medallion, no window, the crest as today (${JSON.stringify(fin)})`);
    // in the narrow screens' drawer the crest keeps at least 92 px for the close button, the medallion and the key
    const hWant = width <= 1040 ? Math.max(off.h, 92) : off.h;
    check(Math.abs(hWant - hOn) < 0.5, `the medallion adds no height to the crest${width <= 1040 ? ' beyond the drawer\'s 92 px' : ''} (${hOn} px on, ${off.h} px off)`);
    await shot('switch-off'); await closeHud();
    await living(true); await openHud(); await page.waitForTimeout(600);
    c = await crest();
    check(!!c.medal && c.cls && c.chw === 1 && await glazed() > 0.02, 'on again: the medallion back, glazed');
    await shot('switch-on'); await closeHud();
    // the cost while the life runs: Enter at every stop, the weeks running between
    const run = async () => { const until = Date.now() + SECONDS * 1000; while (Date.now() < until) { const s = await page.evaluate(() => ({ busy, mode: hud.mode })); if (s.mode !== 'play') break; if (!s.busy) await page.evaluate(() => send('')); await page.waitForTimeout(150); } };
    const cm = await cost(`while the life runs, ${SECONDS} s`, SECONDS * 1000, run);
    check(cm.frames > 30 && cm.mean < 0.5 && cm.p95 < 1.5, `the medallion's script per frame is small (${cm.mean.toFixed(3)} ms mean, ${cm.p95.toFixed(3)} ms p95)`);
    await idle();
    say('  at age', await page.evaluate(() => hud.life.age.toFixed(1)));
  }

  // a life that starts old, from a save of preset 3 with its start age and seed set, played to the end with their own picks
  let oldSave = null;
  const oldLife = async () => {
    if (!oldSave) {
      if (await page.evaluate(() => !hud || hud.mode !== 'play')) await startLife(page, '3', 'Lale');
      await idle();
      let t = null; for (let i = 0; i < 4 && !t; i++) { t = await page.evaluate(() => askSave()); if (!t) await page.waitForTimeout(1000); }
      const d = JSON.parse(t); d.setup.start_age = START; d.setup.seed = SEED; d.inputs = []; oldSave = d;
    }
    for (let k = 0; k < 6; k++) {
      oldSave.setup.seed = SEED + k;
      await page.evaluate((x) => loadText(x), JSON.stringify(oldSave));
      await page.waitForFunction(() => hud && hud.replay, null, { timeout: 120000 }).catch(() => {});
      await page.waitForFunction(() => hud && !hud.replay && !busy && ['play', 'over'].includes(hud.mode), null, { timeout: 1200000 });
      await idle();
      const s = await page.evaluate(() => ({ mode: hud.mode, age: hud.life.age }));
      if (s.mode === 'play') { say(`  an old life: seed ${oldSave.setup.seed}, taken over at ${s.age.toFixed(1)}`); break; }
      say(`  seed ${oldSave.setup.seed} ended before ${START}; the next seed`);
    }
    let n = 0; for (const t1 = Date.now(); Date.now() - t1 < 30 * 60000; n++) { const s = await step(); if (s.mode === 'over') break; }
    await page.waitForFunction(() => hud.mode === 'over' && !document.getElementById('review').hidden, null, { timeout: 60000 });
    say(`  the end at ${await page.evaluate(() => hud.life.age.toFixed(1))}, after ${n} steps`);
  };
  const endState = () => page.evaluate(() => { const r = document.getElementById('review'), e = r.querySelector('.chw-end'), f = r.querySelector('.lk-final'), p = document.querySelector('.lk-plate');
    return { light: e ? (e.querySelector('.chw') || {}).dataset?.light || '' : '', plate: !!(p && !p.hidden), end: !!e, fin: f ? getComputedStyle(f).display : 'none',
      after: e ? (e.previousElementSibling || {}).className || '' : '', yrs: e ? e.querySelector('.lk-yrs').textContent : '', book: !document.querySelector('.help.sheetwrap:not([hidden])') ? '' : 'open' }; });
  // poll the end's light every 100 ms: when each state began, in ms after the review showed
  const watch = async (ms, act) => {
    const seen = []; let last = ''; const ts = Date.now();
    for (; Date.now() - ts < ms;) {
      const s = await endState(), k = `${s.plate ? 'plate' : 'clear'}|${s.light}`;
      if (k !== last) { seen.push([Date.now() - ts, s.plate, s.light]); last = k; }
      if (act && await act(s, Date.now() - ts)) break;
      if (!act && s.light === 'lit' && !s.plate) break;
      await page.waitForTimeout(100);
    }
    return seen;
  };
  const covered = (id) => page.evaluate((q) => { const b = document.getElementById(q); if (!b) return 'missing'; b.scrollIntoView({ block: 'center' });
    const r = b.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2, at = document.elementFromPoint(x, y);
    const e = document.querySelector('.chw-end'), er = e && e.getBoundingClientRect();
    const lap = er && !(er.right <= r.left || r.right <= er.left || er.bottom <= r.top || r.bottom <= er.top);
    return at && at.closest('#' + q) && !lap ? '' : `covered by ${at ? at.tagName + '.' + at.className : 'nothing'}${lap ? ', the window box' : ''}`; }, id);

  if (parts.includes('end')) {
    say('part end');
    await setMotion('full');
    await oldLife();
    let s = await endState();
    check(s.end && s.fin === 'none' && /lk-final|mh/.test(s.after) && /· \d+ years$/.test(s.yrs), `the full window in the portrait's place, their name and years beneath (${JSON.stringify(s)})`);
    await shot('end-1-review');
    watch.tried = 0;
    const seen = await watch(40000, async (x, t) => {
      if (x.light === 'lighting' && !x.plate && !watch.tried) {
        watch.tried = 1; await page.evaluate(() => __w.start()); await shot('end-2-lighting');
        // Enter is the page's (a new life): kept from the page here, it must not skip the light
        await page.evaluate(() => { const r = document.getElementById('review'), stop = (e) => e.stopPropagation(); r.addEventListener('keydown', stop); r.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })); r.removeEventListener('keydown', stop); });
        watch.enter = (await endState()).light;
        await page.focus('#rvBook'); await page.keyboard.press(' '); await page.waitForTimeout(400);
        const b = await endState(); watch.space = b.light + (b.book ? ' (the Book open)' : ' (no Book)');
        await page.keyboard.press('Escape'); await page.waitForTimeout(300);
        const e = await endState(); watch.esc = e.light + (e.book ? ' (the Book still open)' : ' (the Book closed)');
        // the focus on #rvBook scrolled the review down: the light waits while the window is out of view
        await page.evaluate(() => { document.activeElement && document.activeElement.blur(); document.querySelector('.chw-end').scrollIntoView({ block: 'center' }); });
        return false;
      }
      return x.light === 'lit' && !x.plate;
    });
    say('  the light, ms after the review showed [ms, plate up, light]:', JSON.stringify(seen));
    const cw = await page.evaluate(() => __w.stop());   // from the light's start to lit (the key checks and the Book meanwhile)
    say(`  cost while it lights: ${cw.frames} frames, script ${cw.mean.toFixed(3)} ms mean, ${cw.p95.toFixed(3)} ms p95, ${cw.max.toFixed(2)} ms max; tasks over 50 ms (all of the page): ${cw.long.length ? cw.long.join(' ') : 'none'}`);
    check(cw.frames > 30 && cw.mean < 4 && cw.p95 < 8, `the light's script per frame stays in the budget (${cw.mean.toFixed(3)} ms mean, ${cw.p95.toFixed(3)} ms p95)`);
    const tp = (seen.filter((x) => x[1]).pop() || [0])[0], plateGone = (seen.find((x, i) => i && !x[1] && seen[i - 1][1]) || [0])[0];
    const tl = (seen.find((x) => x[2] === 'lighting') || [-1])[0], tlit = (seen.find((x) => x[2] === 'lit') || [-1])[0];
    check(tl >= 0 && (!tp || tl >= plateGone), `the light waits for the "Finis" plate (plate gone at ${plateGone} ms, lighting at ${tl} ms)`);
    check(tlit > tl && tlit - tl >= 7000 && tlit - tl <= 16000, `it lights up in about 11 s (${((tlit - tl) / 1000).toFixed(1)} s from lighting to lit)`);
    check(watch.enter === 'lighting', `Enter (kept from the page) does not skip (${watch.enter})`);
    check(/^lighting \(the Book open\)/.test(watch.space || ''), `Space on a button presses the button and does not skip (${watch.space})`);
    check(/^lighting \(the Book closed\)/.test(watch.esc || ''), `Esc closing the Book does not skip (${watch.esc})`);
    await shot('end-3-lit');
    for (const id of ['again', 'rvBook']) { const v = await covered(id); check(v === '', `#${id} is not covered${v ? ' (' + v + ')' : ''}`); }
    await page.evaluate(() => document.querySelector('.chw-end').scrollIntoView({ block: 'center' })); await page.waitForTimeout(300);
    const wb = await box('.chw-endwin');
    await shot('end-4-window', { x: Math.max(0, wb.x - 60), y: Math.max(0, wb.y - 40), width: wb.width + 120, height: wb.height + 110 });
    const at = { x: wb.x + wb.width / 2, y: wb.y + wb.height / 2 - wb.width * 0.485 / 1.075 * 0.17 };
    if (phone) await page.touchscreen.tap(at.x, at.y); else await page.mouse.move(at.x, at.y);
    await page.waitForTimeout(400);
    const tip = await page.evaluate(() => { const t = document.getElementById('tip'); return t.hidden ? '' : t.innerText.replace(/\s+/g, ' ').slice(0, 200); });
    check(/^Age 0\b/.test(tip), `a ${phone ? 'tap' : 'hover'} reads the year ("${tip}")`);
    if (!phone) await page.mouse.move(2, 2);
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'no sideways scroll at the end');
    const cl = await cost('the lit window, 5 s', 5000);
    check(cl.mean < 1 && cl.p95 < 3, `the lit window's script per frame is small (${cl.mean.toFixed(3)} ms mean, ${cl.p95.toFixed(3)} ms p95)`);
    await living(false); s = await endState();
    const fin = await page.evaluate(() => ({ chw: document.querySelectorAll('.chw, .chw-end, .hud-medal, .chw-gone').length, fin: !!document.querySelector('#review .lk-final') }));
    check(!s.end && fin.chw === 0 && (s.fin !== 'none' || !fin.fin), `off: the review as today, its portrait back (${JSON.stringify(fin)}, .lk-final ${s.fin})`);
    await shot('end-5-off');
    await living(true); await page.waitForTimeout(700); s = await endState();
    check(s.end && s.light === 'lit' && s.fin === 'none', `on again: the window back, lit at once (${s.light})`);
    // a new life through #again: the review's window goes, the start's cards come
    await page.click('#again'); await page.waitForSelector('.tarot', { timeout: 60000 }).catch(() => {});
    const na = await page.evaluate(() => ({ mode: hud.mode, tarot: document.querySelectorAll('.tarot').length, end: document.querySelectorAll('.chw-end').length, chw: document.querySelectorAll('.chw').length }));
    check(na.tarot > 0 && na.end === 0 && na.chw <= 1, `#again starts a new life, the window gone (${JSON.stringify(na)})`);
  }

  if (parts.includes('skip')) {
    say('part skip');
    await setMotion('full');
    for (const how of ['Space', 'click', 'Escape']) {
      await oldLife();
      const seen = await watch(30000, async (x) => {
        if (x.light !== 'lighting' || x.plate) return false;
        await page.waitForTimeout(1500);
        const ts = Date.now();
        if (how === 'click') await page.click('#review .epi'); else { await page.evaluate(() => document.activeElement && document.activeElement.blur()); await page.keyboard.press(how === 'Space' ? ' ' : 'Escape'); }
        await page.waitForTimeout(150);
        watch.skip = [(await endState()).light, Date.now() - ts]; return true;
      });
      check(watch.skip && watch.skip[0] === 'lit', `${how} skips to the lit window at once (${JSON.stringify(watch.skip)}; ${JSON.stringify(seen)})`);
      watch.skip = null;
      await shot(`skip-${how}`);
      check(await page.evaluate(() => hud.mode === 'over' && !document.getElementById('review').hidden), `${how}: the review stays`);
    }
  }

  if (parts.includes('still')) {
    say('part still');
    await setMotion('off');
    await oldLife();
    await page.waitForTimeout(600);
    const s = await endState();
    check(s.light === 'lit', `motion off: lit at once (${s.light})`);
    await page.evaluate(() => document.querySelector('.chw-end').scrollIntoView({ block: 'center' })); await page.waitForTimeout(300);
    const wb = await box('.chw-end'), clip = { x: wb.x, y: wb.y, width: wb.width, height: wb.height };
    const a1 = await page.screenshot({ clip }); await page.waitForTimeout(800); const a2 = await page.screenshot({ clip });
    check(same(a1, a2), 'motion off: the end is still (two shots 0.8 s apart equal)');
    await shot('still-end');
    await setMotion('full');
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_window ${parts.join(',')} at ${tag}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
