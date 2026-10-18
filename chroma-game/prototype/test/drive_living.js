const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD (rows V0 to V6): the living layer of the page (web/src/living/), part by part. A probe piece registers
// through CH.piece as the six pieces do and keeps every update it gets; every event is kept too. Each part prints its
// checks and PASS or FAIL; the driver exits 1 on a FAIL, a page error or a console error from the living layer.
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
//   PW=<playwright> node test/drive_living.js URL OUT_DIR [parts: log,switch] [width 1280] [height 800] [preset 4] [age 30] [seed 140892]
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, preset, toAge, seedArg] = process.argv.slice(2);
const parts = (partsArg || 'log').split(','), width = +(W || 1280), height = +(H || 800), P = preset || '4', AGE = +(toAge || 30), SEED = seedArg || '140892';
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600, logs = [], fails = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const warns = [];          // a piece that falls back to today's says so with console.warn: told, not a failure
  page.on('console', (m) => { if (/^living/.test(m.text())) (m.type() === 'error' ? logs : m.type() === 'warning' ? warns : []).push(`console ${m.type()}: ${m.text()}`); });
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
  if (SEED !== '-') {              // the same life every run: this start with the seed, loaded back; the records start after
    const d = JSON.parse(await saved()); d.setup.seed = +SEED; d.inputs = [];
    await loaded(JSON.stringify(d)); await idle();
    await page.evaluate(() => { __lv.updates.length = 0; __lv.events.length = 0; });
  }
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

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living ${parts.join(',')}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
