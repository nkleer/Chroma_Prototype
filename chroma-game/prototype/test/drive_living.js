const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD (rows V0 to V6): the living layer of the page (web/src/living/), part by part, and the job that runs every
// piece's own driver after it (plan section 6, rows V1 to V6). A probe piece registers through CH.piece as the pieces do
// and keeps every update it gets; every event is kept too. Each part prints its checks and PASS or FAIL; the driver exits 1
// on a FAIL, a page error or a console error from the living layer (the joint part: any console error).
//   log     a life lived to AGE, pushing the act they mind most wherever one is minded (rel 0.1 or more, so the push is
//           judged; out of reach too, as a player can force it) and else the first considered act at every other moment,
//           stopping at a moment; the stop log (CH.life: stops, pushes, end) dumped to OUT_DIR/living-log.json; the life
//           saved (as key s does) and loaded back (as key o does), the log dumped again. The two dumps must be equal; each
//           push's verdict must equal its own outcome's hindsight.kind as the page showed it, with at least one push
//           judged; the load's replay must stay still and silent (no update, no event); after it, one quiet update with
//           the load, and the moment it came back to told exactly once, quiet.
//           The life is always the same one: preset 4 (starts at 14) with seed 140892, set by saving the new life, putting
//           the seed in its setup and loading it back before the probe's records start. Its acts are minded (its first
//           moment's most minded act is resented when pushed); in preset 3 (an even, studious life) nearly every act is
//           one they would go with or are okay with, rel is 0 and no push is judged, and a random preset-4 life can have
//           only "doing nothing" minded, which has no outcome to judge. SEED "-" keeps the start's own random seed.
//   switch  the Table menu's Living HUD row: off takes the probe down and sets html[data-living] "off" (stored as
//           chroma.living), on mounts it again; under the classic look the row is gone and Living is off.
//   joint   the pieces together (plan step 9): the same life from its start (loaded again when an earlier part lived
//           it) to AGE in four stretches, with the Table menu's Motion row at full, calm and off, then full with the
//           system's reduced motion. In each: CH.motion() as set; what each piece's frames cost (CH.cost(),
//           living/00-core.js: mean, 95th percentile, and the mean over which the per-piece guard would have dropped it
//           to still frames: the guard only reports here, chroma.living.guard "off", so the pieces are measured moving);
//           what the shared beat played (living/95-beat.js: on picks and years in full, nothing with motion off or
//           reduced). The budget is 4 ms a frame on average and 8 ms at the 95th percentile for all the pieces together
//           on a real graphics card; this headless software build reports its numbers and fails only above three times
//           that. With motion off and reduced, two shots 0.8 s apart are equal; in full they differ. Then the switch on,
//           off, on: off takes every piece down and gives today's screen and the ink look's own hooks back (its night,
//           its river light, its own Motion and Look tooltips, no living frame while the life steps on), on puts the
//           pieces back; the one-ink rules (living/90-game.css) hide look's drops and river light only with Living on
//           and the star and river standing (read with stand-ins while those two pieces are not here). Then the guard,
//           turned on: a stand-in piece that takes 8 ms a frame is dropped to still frames after 5 s (it sees and hears
//           motion "off"; one console.warn) while the others keep moving. No console error at all on the way.
//   sky, star, river, cards, story, window   that piece's own driver (test/drive_living_<piece>.js), after the parts
//           above and after this driver's browser has closed (one browser at a time), with the same URL and OUT_DIR, the
//           width and height when they are given here (else the driver's own), and the driver's own default parts, or the
//           ones named after a colon, joined by "+" (sky:look+motion). A piece whose driver is not here yet is skipped with a note. LIVING_PART_TIMEOUT (seconds,
//           default 2700) stops a piece's driver that runs too long (a FAIL).
//   PW=<playwright> node test/drive_living.js URL OUT_DIR [parts: log,switch,joint,sky,star,river,cards,story,window]
//     [width 1280] [height 800] [preset 4] [age 30] [seed 140892]
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, preset, toAge, seedArg] = process.argv.slice(2);
const parts = (partsArg || 'log').split(',').filter(Boolean), width = +(W || 1280), height = +(H || 800), P = preset || '4', AGE = +(toAge || 30), SEED = seedArg || '140892';
const OWN = ['log', 'switch', 'joint'], PIECES = ['sky', 'star', 'river', 'cards', 'story', 'window'];
const own = parts.filter((p) => OWN.includes(p)), pieceParts = parts.filter((p) => PIECES.includes(p.split(':')[0]));
const unknown = parts.filter((p) => !own.includes(p) && !pieceParts.includes(p));
if (unknown.length) { console.log(`drive_living: no part ${unknown.join(', ')} (parts: ${OWN.concat(PIECES).join(', ')})`); process.exit(2); }

// this driver's own parts, in one browser
async function ownParts() {
  const browser = await chromium.launch();
  const phone = width < 600, logs = [], fails = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone });
  // the joint part measures the pieces moving: the per-piece guard (living/00-core.js) only reports from the start, and is
  // turned on for its own check at the end
  await ctx.addInitScript((joint) => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave');
    if (joint) localStorage.setItem('chroma.living.guard', 'off'); else localStorage.removeItem('chroma.living.guard'); } catch (_) {} }, parts.includes('joint'));
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const warns = [];          // a piece that falls back to today's says so with console.warn: told, not a failure
  const errs = [];           // every console error (the joint part allows none; a picture the server lacks is not counted)
  page.on('console', (m) => { const t = m.text();
    if (/^living/.test(t)) (m.type() === 'error' ? logs : m.type() === 'warning' ? warns : []).push(`console ${m.type()}: ${t}`);
    if (m.type() === 'error' && !/Failed to load resource|net::|CERT/.test(t)) errs.push(`console error: ${t}`); });
  const shot = (n) => page.screenshot({ path: `${dir}/living-${n}.png` });
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.piece && CH.life, null, { timeout: 120000 });
  check(await page.evaluate(() => document.documentElement.dataset.living === 'on'), 'Living is on by default (html[data-living])');
  // the probe piece and the event log
  await page.evaluate(() => {
    const T = window.__lv = { updates: [], events: [], mounted: 0 };
    const now = () => ({ replay: !!(hud && hud.replay), busy, age: hud && hud.life ? hud.life.age : null });
    CH.piece('probe', {
      mount() { T.mounted++; },
      update(S, how) { T.updates.push({ ...now(), S: S.age, quiet: !!how.quiet, loaded: !!how.loaded, frames: how.frames.length, rev: S.rev,
        own: S !== hud.life && S.items === ITEMS && Array.isArray(S.want) && typeof hud.life.want === 'number' && S.means === hud.life.res && S.pushes === CH.life.pushes }); },
      destroy() { T.mounted--; },
    });
    const keyOf = (ev, x) => ev === 'moment' ? x.cp.age + '|' + x.cp.title : ev === 'outcome' ? x.res.age + '|' + x.res.title : ev === 'pick' ? x.cp.age + '|' + x.cp.title + '|' + x.text : String(x);
    for (const ev of ['moment', 'outcome', 'pick', 'living']) CH.on(ev, (x) => T.events.push({ ev, key: keyOf(ev, x), quiet: !!(x && x.quiet), S: !!(x && x.S), ...now() }));
  });
  await startLife(page, P, 'Lale');
  await idle();
  const saved = async () => { let t = null; for (let i = 0; i < 4 && !t; i++) { t = await page.evaluate(() => askSave()); if (!t) await page.waitForTimeout(1000); } return t; };
  const loaded = async (text) => {
    await page.evaluate((x) => loadText(x), text);
    const replayed = await page.waitForFunction(() => hud && hud.replay, null, { timeout: 120000 }).then(() => true, () => false);
    await page.waitForFunction(() => hud && !hud.replay && !busy && hud.mode === 'play', null, { timeout: 1200000 });
    await page.waitForTimeout(2000);
    return replayed;
  };
  let startText = null;           // the life at its start, for a part that lives it again (joint)
  if (SEED !== '-') {              // the same life every run: this start with the seed, loaded back; the records start after
    const d = JSON.parse(await saved()); d.setup.seed = +SEED; d.inputs = [];
    startText = JSON.stringify(d);
    await loaded(startText); await idle();
    await page.evaluate(() => { __lv.updates.length = 0; __lv.events.length = 0; });
  } else if (parts.includes('joint')) startText = await saved();
  const startAge = await page.evaluate(() => hud.life && hud.life.age);
  say('started', Date.now() - t0, 'ms, at age', await page.evaluate(() => hud.life && hud.life.age));

  if (parts.includes('log')) {
    say('part log');
    const seen = new Map();          // each outcome as the page showed it
    let k = 0, pushed = 0; const minded = [];
    for (const t1 = Date.now(); Date.now() - t1 < 20 * 60000;) {
      await idle();
      const s = await page.evaluate(() => { const up = !document.getElementById('evwrap').hidden;
        return { age: hud.life && hud.life.age, mode: hud.mode, cp: !!hud.cp && up, rn: !!document.querySelector('#rnKeep'),
          out: hud.res && up ? { key: hud.res.age + '|' + hud.res.title, pushed: !!hud.res.pushed, kind: hud.res.hindsight ? hud.res.hindsight.kind : null } : null }; });
      if (s.out && !seen.has(s.out.key)) seen.set(s.out.key, s.out);
      if (s.mode !== 'play') { fails.push('the life left play at ' + s.age); break; }
      if (s.cp && s.age >= AGE) break;
      if (s.rn) { await page.click('#rnKeep'); await page.waitForTimeout(400); continue; }
      if (s.cp) {
        const c = await page.evaluate((other) => {
          const by = (a, b) => (b.rel || 0) - (a.rel || 0), all = hud.cp.options.filter((o) => !o.own && o.means && o.means.length).sort(by);
          const os = all.filter((o) => o.status !== 'out of reach'), top = all.length && (all[0].rel || 0) >= 0.1 ? all[0] : other && os[0];
          return { n: top ? String(top.n) : '', rel: top ? +(top.rel || 0).toFixed(2) : null, far: !!top && top.status === 'out of reach', age: hud.cp.age };
        }, k++ % 2 === 0);
        minded.push(c); const n = c.n;
        if (n) pushed++;
        await page.evaluate((x) => send(x), n);
        continue;
      }
      await page.evaluate(() => send(''));              // Go on after an outcome, or live on to the next moment
    }
    await idle(); await page.waitForTimeout(1500);       // the autosave's own save request settles
    const at = await page.evaluate(() => ({ age: hud.life.age, cp: hud.cp ? hud.cp.age + '|' + hud.cp.title : '' }));
    say('  stood at age', at.age, 'moment', at.cp, '; pushed', pushed, 'times;', seen.size, 'outcomes seen');
    say('  each moment (age:rel of the act pushed, ~ out of reach, - no push):', minded.map((c) => `${c.age}:${c.n ? c.rel + (c.far ? '~' : '') : '-'}`).join(' '));
    await shot('log-1-live');
    const dump = () => page.evaluate(() => JSON.stringify({ stops: CH.life.stops, pushes: CH.life.pushes, end: CH.life.end_age }));
    const info = () => page.evaluate(() => { const L = CH.life, by = {}; L.stops.forEach((s) => { by[s.kind] = (by[s.kind] || 0) + 1; });
      return { stops: L.stops.length, kinds: by, pushes: L.pushes.length, judged: L.pushes.filter((p) => p.verdict !== 'none').map((p) => p.verdict), bytes: L.bytes, rev: L.rev, items: L.items === ITEMS, n: ITEMS.length }; });
    const d1 = await dump(), i1 = await info();
    require('fs').writeFileSync(`${dir}/living-log.json`, d1);
    const live = await page.evaluate(() => ({ P: CH.life.pushes, R: CH.life.stops.filter((s) => s.kind === 'res').map((s) => s.res) }));
    say('  live log:', JSON.stringify(i1), (i1.bytes / Math.max(1, i1.stops) / 1024).toFixed(2), 'KB a stop');
    check(at.cp !== '', `standing at a moment past ${AGE}`);
    check(i1.stops > 0 && i1.kinds.year > 0 && i1.kinds.cp > 0 && i1.kinds.res > 0, 'the log has years, moments and outcomes');
    check(i1.items, 'CH.life.items is the page\'s ITEMS');
    check(i1.bytes / Math.max(1, i1.stops) < 4096 && i1.bytes < 512 * 1024, 'a stop is a few KB and the log under 0.5 MB');
    // each verdict is its own outcome's hindsight.kind, as the page showed that outcome
    let bad = 0;
    for (const p of live.P) { const o = seen.get(p.age + '|' + p.title); if (!o || !o.pushed || (o.kind || 'none') !== p.verdict) { bad++; say('   push', JSON.stringify(p), 'page showed', JSON.stringify(o)); } }
    for (const r of live.R) { const o = seen.get(r.age + '|' + r.title); if (o && (o.kind || 'none') !== r.verdict) { bad++; say('   outcome', r.age, r.title, r.verdict, 'page showed', o.kind); } }
    const shownPushes = [...seen.values()].filter((o) => o.pushed).length;
    check(bad === 0 && live.P.length === shownPushes && live.P.length > 0, `each push's verdict is its own outcome's hindsight.kind (${live.P.length} pushes, ${shownPushes} shown, judged: ${i1.judged.join(' ') || 'none'})`);
    check(i1.judged.length > 0, `at least one push was judged, so the verdicts were tested (${i1.judged.length} of ${live.P.length})`);
    check(live.R.every((r) => seen.has(r.age + '|' + r.title)) && live.R.length === seen.size, `every outcome the page showed is one stop (${live.R.length} stops, ${seen.size} shown)`);
    // live events: one for each moment and outcome shown, never twice
    const ev0 = await page.evaluate(() => __lv.events.slice());
    const keys = (e) => ev0.filter((x) => x.ev === e).map((x) => x.key), dup = (xs) => xs.length - new Set(xs).size;
    check(dup(keys('moment')) === 0 && dup(keys('outcome')) === 0, `no moment or outcome told twice (${keys('moment').length} moments, ${keys('outcome').length} outcomes, ${keys('pick').length} picks, ${keys('living').length} living)`);
    check([...seen.keys()].every((x) => keys('outcome').includes(x)), 'every outcome shown was told');
    check(ev0.every((x) => x.ev === 'living' || x.S), 'moment, outcome and pick carry S');
    const u0 = await page.evaluate(() => __lv.updates.slice());
    check(u0.length > 0 && u0.every((u) => u.own), `each update's S is its own object and hud.life keeps its want, res and pushes (${u0.length} updates)`);
    // save (key s asks the worker the same way) and load (key o, loadText)
    const text = await saved();
    check(!!text, 'the life saves');
    const mark = await page.evaluate(() => ({ u: __lv.updates.length, e: __lv.events.length }));
    const tL = Date.now();
    if (!await loaded(text)) fails.push('the load never replayed');
    say('  loaded in', Date.now() - tL, 'ms, back at age', await page.evaluate(() => hud.life.age), 'loaded note', JSON.stringify(await page.evaluate(() => hud.loaded || null)));
    await shot('log-2-loaded');
    const d2 = await dump(), i2 = await info();
    say('  loaded log:', JSON.stringify(i2));
    if (d1 !== d2) {
      const a = JSON.parse(d1), b = JSON.parse(d2), n = Math.min(a.stops.length, b.stops.length);
      let j = 0; while (j < n && JSON.stringify(a.stops[j]) === JSON.stringify(b.stops[j])) j++;
      say('   first differing stop', j, '\n   live  ', JSON.stringify(a.stops[j]).slice(0, 600), '\n   loaded', JSON.stringify(b.stops[j]).slice(0, 600));
    }
    check(d1 === d2, `the log after the load equals the log lived (${d1.length} bytes)`);
    const after = await page.evaluate((m) => ({ u: __lv.updates.slice(m.u), e: __lv.events.slice(m.e) }), mark);
    check(after.u.every((u) => !u.replay) && after.e.every((x) => !x.replay), 'the replay is still and silent: no update and no event while it runs');
    check(after.u.length === 1 && after.u[0].quiet && after.u[0].loaded, `one quiet update with the load (${JSON.stringify(after.u.map((u) => ({ q: u.quiet, l: u.loaded, age: u.S })))})`);
    const mo = after.e.filter((x) => x.ev === 'moment');
    check(mo.length === 1 && mo[0].key === at.cp && mo[0].quiet, `the moment the load came back to is told exactly once, quiet (${JSON.stringify(after.e.map((x) => [x.ev, x.key, x.quiet]))})`);
    check(after.e.every((x) => x.ev === 'moment'), 'nothing else is told after the load');
  }

  if (parts.includes('switch')) {
    say('part switch');
    await idle();
    if (await page.evaluate(() => !document.getElementById('evwrap').hidden)) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(300); }
    const st = () => page.evaluate(() => ({ living: document.documentElement.dataset.living, look: document.documentElement.dataset.look, row: !!document.querySelector('#tPop [data-lv]'),
      v: (document.querySelector('#tPop [data-lv] .v') || {}).textContent || '', after: (document.querySelector('#tPop [data-lv]') || {}).previousElementSibling?.dataset?.lk || '',
      stored: localStorage.getItem('chroma.living'), mounted: __lv.mounted }));
    await page.click('#tMenu'); await page.waitForTimeout(300);
    let s = await st();
    check(s.row && s.after === 'look' && s.v === 'on' && s.mounted === 1, `the row sits after Look, on, the probe mounted (${JSON.stringify(s)})`);
    await shot('switch-1-menu');
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(300); s = await st();
    check(s.living === 'off' && s.stored === 'off' && s.v === 'off' && s.mounted === 0, `off: html[data-living] off, stored, the probe taken down (${JSON.stringify(s)})`);
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(300); s = await st();
    check(s.living === 'on' && s.stored === 'on' && s.v === 'on' && s.mounted === 1, `on again: the probe mounted again (${JSON.stringify(s)})`);
    await page.click('#tPop [data-lk="look"]'); await page.waitForTimeout(300); s = await st();
    check(s.look === 'classic' && !s.row && s.living === 'off' && s.mounted === 0, `classic look: no row, Living off (${JSON.stringify(s)})`);
    await page.click('#tPop [data-lk="look"]'); await page.waitForTimeout(300); s = await st();
    check(s.look === 'ink' && s.row && s.living === 'on' && s.mounted === 1, `ink again: the row back, Living on (${JSON.stringify(s)})`);
    await page.keyboard.press('Escape');
  }

  if (parts.includes('joint')) {
    say('part joint');
    await idle();
    // the moment window covers the menu: it is set aside first and brought back after
    const menuRow = async (sel) => {
      const up = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !w.hidden && !w.classList.contains('peek'); });
      if (up) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(400); }
      await page.click('#tMenu'); await page.waitForTimeout(250); await page.click(`#tPop ${sel}`); await page.waitForTimeout(300);
      await page.keyboard.press('Escape').catch(() => {}); await page.waitForTimeout(250);
      if (up) { await page.click('#evback').catch(() => {}); await page.waitForTimeout(400); }
    };
    const setMotion = async (m) => { for (let i = 0; i < 3 && await page.evaluate(() => document.documentElement.dataset.motion) !== m; i++) await menuRow('[data-lk="motion"]'); };
    // the life on to an age, as the log part lives it (a push at every other moment, else their own pick), stopping at a moment
    const liveTo = async (age) => {
      let k = 0;
      for (const t1 = Date.now(); Date.now() - t1 < 15 * 60000;) {
        await idle();
        const s = await page.evaluate(() => { const up = !document.getElementById('evwrap').hidden;
          return { age: hud.life && hud.life.age, mode: hud.mode, cp: !!hud.cp && up, rn: !!document.querySelector('#rnKeep') }; });
        if (s.mode !== 'play') { fails.push('the life left play at ' + s.age); return; }
        if (s.cp && s.age >= age) return;
        if (s.rn) { await page.click('#rnKeep'); await page.waitForTimeout(400); continue; }
        if (s.cp) {
          const n = await page.evaluate((push) => { if (!push) return ''; const o = hud.cp.options.find((x) => !x.own && x.means && x.means.length && x.status !== 'out of reach'); return o ? String(o.n) : ''; }, k++ % 2 === 0);
          await page.evaluate((x) => send(x), n); continue;
        }
        await page.evaluate(() => send(''));
      }
      fails.push('the life did not reach ' + age + ' in 15 minutes');
    };
    // two shots 0.8 s apart, the pointer parked off the panels' hover areas and no tooltip
    const twoShots = async (n) => { await page.mouse.move(width - 2, 2); await page.evaluate(() => hideTip()); await page.waitForTimeout(1500);
      const a = await page.screenshot({ path: `${dir}/living-joint-${width}-${n}-a.png` }); await page.waitForTimeout(800);
      const b = await page.screenshot({ path: `${dir}/living-joint-${width}-${n}-b.png` }); return a.equals(b); };
    const beats = () => page.evaluate(() => Object.assign({}, CH.mods.beat ? CH.mods.beat.count : {}, { playing: document.getAnimations().filter((a) => /^lv-beat/.test(a.id)).length }));
    const f = (v) => (v == null ? '-' : (+v).toFixed(2));
    const age0 = await page.evaluate(() => hud.life.age);
    if (startText && age0 > startAge + 0.5) {            // an earlier part lived it: the same life again from its start
      const tL = Date.now(); await loaded(startText); await idle();
      say('  the life again from its start, age', await page.evaluate(() => hud.life.age), 'in', Date.now() - tL, 'ms');
    }
    const from = await page.evaluate(() => hud.life.age);
    const st0 = await page.evaluate(() => ({ pieces: document.documentElement.dataset.lvPieces || '', cost: typeof CH.cost === 'function' && typeof CH.cost.all === 'function' }));
    check(st0.cost && ['sky', 'story', 'window', 'beat'].every((p) => st0.pieces.split(' ').includes(p)), `the pieces stand: html[data-lv-pieces] "${st0.pieces}"; CH.cost() is there`);
    const MODES = [['full', false], ['calm', false], ['off', false], ['full', true]], step = (AGE - from) / MODES.length;
    const costs = [];
    for (let i = 0; i < MODES.length; i++) {
      const [m, reduce] = MODES[i], label = reduce ? 'reduced' : m;
      await setMotion(m);
      await page.emulateMedia({ reducedMotion: reduce ? 'reduce' : 'no-preference' }); await page.waitForTimeout(500);
      const seen = await page.evaluate(() => [document.documentElement.dataset.motion, CH.motion()]);
      check(seen[1] === (reduce ? 'off' : m), `${label}: html[data-motion] ${seen[0]}, CH.motion() ${seen[1]}`);
      const b0 = await beats(), u0 = await page.evaluate(() => __lv.updates.length); await page.evaluate(() => CH.cost.reset());
      const tS = Date.now(); await liveTo(Math.min(AGE, from + step * (i + 1)));
      const c = await page.evaluate(() => ({ each: CH.cost(), all: CH.cost.all(), age: hud.life.age }));
      const b1 = await beats(), d = (k) => (b1[k] || 0) - (b0[k] || 0);
      const ups = await page.evaluate((u) => { const x = __lv.updates.slice(u); return { n: x.length, busy: x.filter((v) => v.busy).length, years: new Set(x.map((v) => Math.floor(v.S))).size }; }, u0);
      costs.push([label, c]);
      say(`  ${label}: to age ${f(c.age)} in ${Math.round((Date.now() - tS) / 1000)} s; all the pieces ${c.all.n} frames, mean ${f(c.all.mean)} ms, p95 ${f(c.all.p95)} ms, max ${f(c.all.max)} ms`);
      Object.entries(c.each).forEach(([p, x]) => say(`    ${p.padEnd(7)} ${String(x.frames).padStart(5)} frames, mean ${f(x.mean)} ms, p95 ${f(x.p95)} ms, max ${f(x.max)} ms, an update ${f(x.update)} ms${x.tripped ? `; over the guard's ${x.tripped} ms` : ''}${x.still ? ', STILL' : ''}`));
      say(`    ${ups.n} updates (${ups.busy} while time ran, ${ups.years} whole years); the beat: ${d('pick')} picks, ${d('outcome')} outcomes, ${d('year')} years`);
      check(c.all.mean <= 12 && c.all.p95 <= 24, `${label}: all the pieces within three times the budget (mean ${f(c.all.mean)} of 4 ms, p95 ${f(c.all.p95)} of 8 ms)`);
      if (m === 'full' && !reduce) check(d('pick') > 0 && d('year') > 0, `full: the beat plays on picks and years (${d('pick')} picks, ${d('outcome')} outcomes, ${d('year')} years)`);
      if (m === 'off' || reduce) check(d('pick') + d('outcome') + d('year') === 0 && !b1.playing, `${label}: the beat plays nothing (${d('pick')}, ${d('outcome')}, ${d('year')}; ${b1.playing} playing)`);
      const same = await twoShots(label);
      if (m === 'off' || reduce) check(same, `${label}: two shots 0.8 s apart are equal`);
      else if (m === 'full') check(!same, 'full: two shots 0.8 s apart differ (the screen moves)');
      else say(`    calm: two shots 0.8 s apart ${same ? 'are equal' : 'differ'}`);
    }
    await page.emulateMedia({ reducedMotion: 'no-preference' }); await setMotion('full'); await page.waitForTimeout(500);
    const over = await page.evaluate(() => Object.entries(CH.cost()).filter(([, x]) => x.tripped).map(([p, x]) => `${p} ${x.tripped} ms`));
    if (over.length) say(`  note: with the guard on, these would have dropped to still frames on this machine: ${over.join(', ')}`);
    fs.writeFileSync(`${dir}/living-joint-${width}-cost.json`, JSON.stringify(costs));

    // the switch: on, off, on. Off gives today's screen and the ink look's own hooks back
    const view = () => page.evaluate(() => {
      const r = document.documentElement, shown = (s) => { const e = document.querySelector(s); return !!e && getComputedStyle(e).display !== 'none'; };
      const rl = document.querySelector('#river .lk-river'), feed = document.getElementById('feed');
      return { living: r.dataset.living, pieces: r.dataset.lvPieces || '', sky: !!document.querySelector('.lv-sky'), medal: !!document.querySelector('#hud .hud-medal'),
        story: feed.classList.contains('sy-on'), hands: feed.querySelectorAll('.sy-hd, .sy-hand').length, night: ['.sky', '.glow', 'svg.sigil'].map(shown),
        light: rl ? getComputedStyle(rl).display : 'none there', frames: CH.cost.all().frames };
    });
    const tipOf = (sel) => page.evaluate((s) => { const b = document.querySelector(s); if (!b) return ''; showTip(b); const t = tipEl.innerText.replace(/\s+/g, ' '); hideTip(); return t; }, sel);
    // the one-ink rules, read with stand-ins: look's drop and river light, as they would be with the star and river standing
    const oneInk = () => page.evaluate(() => {
      const r = document.documentElement, was = r.dataset.lvPieces;
      const d = document.createElement('span'); d.className = 'lk-drop'; d.setAttribute('aria-hidden', 'true'); document.body.appendChild(d);
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('class', 'lk-river'); document.getElementById('river').appendChild(g);
      const read = () => [getComputedStyle(d).display, getComputedStyle(g).display];
      const now = read();
      r.dataset.lvPieces = ((was || '') + ' star river').trim();
      const withThem = read();
      if (was == null) delete r.dataset.lvPieces; else r.dataset.lvPieces = was;
      d.remove(); g.remove();
      return { now, withThem };
    });
    await idle();
    let v = await view(), ink = await oneInk();
    const tips = async () => ({ motion: await tipOf('#tPop [data-lk="motion"]'), look: await tipOf('#tPop [data-lk="look"]'), row: await tipOf('#tPop [data-lv]') });
    let t = await tips();
    say('  on:', JSON.stringify(v), JSON.stringify(ink));
    check(/slower and fewer/.test(t.motion) && /Living HUD/.test(t.look) && /ink look only/.test(t.row), `on: the Motion, Look and Living rows say what they do now ("${t.motion.slice(0, 80)}...")`);
    check(ink.withThem.every((x) => x === 'none'), `on: with the star and river standing, look's drops and river light are not drawn (${ink.withThem.join(', ')}; now ${ink.now.join(', ')})`);
    await shot(`joint-${width}-switch-1-on`);
    await menuRow('[data-lv]');
    v = await view(); ink = await oneInk(); t = await tips();
    say('  off:', JSON.stringify(v), JSON.stringify(ink));
    check(v.living === 'off' && !v.pieces && !v.sky && !v.medal && !v.story && v.hands === 0, 'off: every piece is taken down (no sky, medallion or hand; html[data-lv-pieces] gone)');
    check(v.night.every((x) => x) && !/none/.test(v.light), `off: today's night, glow and sigil and the ink look's river light are back (${v.night.join(' ')}; light ${v.light})`);
    check(/nothing loops/.test(t.motion) && !/slower and fewer/.test(t.motion) && !/Living HUD/.test(t.look), 'off: the Motion and Look rows have the ink look\'s own words again');
    check(ink.withThem.every((x) => x !== 'none'), `off: the one-ink rules rest (${ink.withThem.join(', ')})`);
    const fr0 = v.frames;
    await page.evaluate(() => send(''));            // a step with Living off: their own pick, then Go on
    await idle();
    if (await page.evaluate(() => !!document.querySelector('#rnKeep'))) { await page.click('#rnKeep').catch(() => {}); await idle(); }
    const lk = await page.evaluate(() => document.querySelectorAll('#feed .lk-in').length);
    await page.waitForTimeout(1200);
    v = await view();
    check(v.frames === fr0 && !v.pieces, `off: a step of the life draws no living frame (${v.frames - fr0} frames) and mounts nothing`);
    say(`  off: the ink look's wet ink on the story's lines: ${lk} lines`);
    await shot(`joint-${width}-switch-2-off`);
    await menuRow('[data-lv]');
    await page.waitForTimeout(1500);
    v = await view(); t = await tips();
    say('  on again:', JSON.stringify(v));
    check(v.living === 'on' && v.sky && v.medal && v.story && v.hands > 0 && ['sky', 'story', 'window', 'beat'].every((p) => v.pieces.split(' ').includes(p)), 'on again: the sky, the medallion and the story\'s hands are back');
    check(v.frames > fr0 && /slower and fewer/.test(t.motion), `on again: the pieces draw (${v.frames - fr0} frames) and the Motion row says slower and fewer`);
    await shot(`joint-${width}-switch-3-on`);
    // the guard itself: a stand-in piece that takes 8 ms a frame drops to still frames after 5 s of it, hears motion "off"
    // and says so once with console.warn; the others keep moving
    await page.evaluate(() => { localStorage.removeItem('chroma.living.guard');
      const G = window.__heavy = { on: true, heard: [] };
      CH.piece('heavy', { mount() { G.offF = CH.frame(() => { if (!G.on) return; const t = performance.now(); while (performance.now() - t < 8); G.seen = CH.motion(); });
        G.offM = CH.on('motion', (m) => G.heard.push(m)); }, destroy() { if (G.offF) G.offF(); if (G.offM) G.offM(); } }); });
    const w0 = warns.length;
    await page.waitForTimeout(8000);
    const g = await page.evaluate(() => { const c = CH.cost(); __heavy.on = false; return { heavy: c.heavy, others: Object.entries(c).filter(([p, x]) => p !== 'heavy' && x.still).map(([p]) => p), seen: __heavy.seen, heard: __heavy.heard, motion: CH.motion() }; });
    const said = warns.slice(w0).filter((x) => /heavy/.test(x));
    say('  guard:', JSON.stringify(g), said.join(' | '));
    check(g.heavy && g.heavy.still && g.heavy.tripped > 6 && g.seen === 'off' && g.heard.includes('off') && said.length === 1,
      `the guard drops a piece over 6 ms a frame for 5 s to still frames: it sees and hears motion "off", told once with console.warn (${g.heavy && g.heavy.tripped} ms)`);
    check(!g.others.length && g.motion === 'full', `the other pieces keep moving (still: ${g.others.join(' ') || 'none'}; CH.motion() ${g.motion})`);
    check(errs.length === 0, `no console error on the way (${errs.length}${errs.length ? ': ' + errs.slice(0, 3).join(' | ') : ''})`);
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living ${own.join(',')}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close();
  return ok;
}

// a piece's own driver, as a child process: its lines are printed with the piece's name before them
function pieceDriver(part) {
  const [name, sub] = part.split(':'), file = path.join(__dirname, `drive_living_${name}.js`);
  if (!fs.existsSync(file)) { console.log(`part ${name}: skipped, its driver (test/drive_living_${name}.js) is not here yet`); return Promise.resolve('skipped'); }
  const args = [file, url, dir, sub ? sub.split('+').join(',') : '', W || '', H || ''];
  console.log(`part ${name}: node ${path.basename(file)} ${args.slice(1).map((a) => (a === '' ? "''" : a)).join(' ')}`);
  return new Promise((done) => {
    const t1 = Date.now(), kid = spawn(process.execPath, args, { cwd: __dirname, env: process.env, stdio: ['ignore', 'pipe', 'pipe'] });
    const out = (s) => s.toString().split('\n').filter((l) => l.length).forEach((l) => console.log(`[${name}] ${l}`));
    kid.stdout.on('data', out); kid.stderr.on('data', out);
    const limit = +(process.env.LIVING_PART_TIMEOUT || 2700) * 1000;
    const stop = setTimeout(() => { console.log(`[${name}] stopped after ${limit / 1000} s`); kid.kill('SIGKILL'); }, limit);
    kid.on('close', (code) => { clearTimeout(stop); const ok = code === 0;
      console.log(`part ${name}: ${ok ? 'PASS' : 'FAIL'} (exit ${code}) in ${Math.round((Date.now() - t1) / 1000)} s`); done(ok ? 'PASS' : 'FAIL'); });
  });
}

(async () => {
  const t0 = Date.now(), res = [];
  if (own.length) res.push([own.join(','), await ownParts().then((ok) => (ok ? 'PASS' : 'FAIL'), (e) => { console.log('drive_living:', (e && e.stack) || e); return 'FAIL'; })]);
  for (const p of pieceParts) res.push([p.split(':')[0], await pieceDriver(p)]);
  const ok = res.every(([, r]) => r !== 'FAIL');
  if (res.length > 1) console.log('parts: ' + res.map(([p, r]) => `${p} ${r}`).join('; '));
  console.log(`drive_living ${parts.join(',')}${own.length || W ? ` ${width}x${height}` : ''}: ${ok ? 'PASS' : 'FAIL'} in ${Math.round((Date.now() - t0) / 1000)} s`);
  process.exit(ok ? 0 : 1);
})();
