const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD, row V3: the river (web/src/living/30-river.js), the life line drawn as a river on three canvases
// under svg#river. Each part prints its checks and PASS or FAIL; the driver exits 1 on a FAIL, a page error or a console error.
//   live    a life lived to AGE as drive_living.js lives it (preset 4, seed 140892: its acts are minded, so pushes are
//           judged and the river has seams and knots), pushing the act they mind most at every other moment and else the
//           first considered act; over the first 20 s of it the river's own cost each frame (CH.pieces river perf():
//           its script, draws and updates together) is read, mean and p95 in ms.
//   look    the river is mounted (#line.lv-river, its canvas first in #line, under svg#river); the line is 120 px on
//           screens taller than 800 px, 92 px on shorter ones and 64 px on a phone; no sideways scroll; the fog, the
//           page's own river and band are hidden, its glyphs and ages stay; a shot of the page and of #line.
//   read    a glyph's hover shows its year (Age N) and its click opens that year in the story (openYear); the canvas
//           answers hovers across its rows with its readings (the years ahead, the doors, threads, beds, gems, pushes)
//           in the page's #tip; a hover on the lived years reads the age.
//   motion  the Table menu's Motion row through full, calm and off: a shot each; with motion off two shots of #line
//           0.8 s apart are equal, byte for byte.
//   switch  the Table menu's Living HUD row: off takes the river down (no canvas, no .lv-river, the page's own river,
//           band and fog back), on puts it back.
//   reduced with RV_REDUCED=1 (the system asks for reduced motion): it counts as motion off; after time runs the line
//           has changed, and two shots of #line 0.8 s apart are equal. Not with live, whose cost wants motion.
//   PW=<playwright> [RV_REDUCED=1] node test/drive_living_river.js URL OUT_DIR [parts: live,look,read,motion,switch,reduced] [width 1440] [height 900] [preset 4] [age 30] [seed 140892]
const fs = require('fs');
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, preset, toAge, seedArg] = process.argv.slice(2);
const parts = (partsArg || 'live,look,read,motion,switch').split(','), width = +(W || 1440), height = +(H || 900), P = preset || '4', AGE = +(toAge || 30), SEED = seedArg || '140892';
const tag = `${width}x${height}`;
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600, logs = [], fails = [], warns = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone, reducedMotion: process.env.RV_REDUCED ? 'reduce' : 'no-preference' });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); ['chroma.living', 'chroma.autosave', 'chroma.motion', 'chroma.look'].forEach((k) => localStorage.removeItem(k)); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { const t = m.text(); if (m.type() === 'error') logs.push(`console error: ${t}`); else if (m.type() === 'warning' && /^living/.test(t)) warns.push(`console warning: ${t}`); });
  const shot = (n) => page.screenshot({ path: `${dir}/river-${tag}-${n}.png` });
  const lineShot = (n) => page.locator('#line').screenshot(n ? { path: `${dir}/river-${tag}-${n}.png` } : {});
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const settle = async () => {          // the event window aside ("Look at the life"), an outcome closed with Go on
    for (let i = 0; i < 6; i++) {
      const s = await page.evaluate(() => { const w = document.getElementById('evwrap');
        return { ev: !w.hidden && !w.classList.contains('peek'), res: !!document.querySelector('#goOn'), cp: !!document.querySelector('#evPeek') }; });
      if (!s.ev) return;
      if (s.res) { await page.click('#goOn'); await idle(); continue; }
      if (s.cp) { await page.click('#evPeek'); await page.waitForTimeout(400); }
      return;
    }
  };
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.piece && CH.life && CH.pieces.has('river'), null, { timeout: 120000 });
  check(await page.evaluate(() => document.documentElement.dataset.living === 'on'), 'Living is on by default (html[data-living])');
  // a probe piece keeps the doors of the last state the pieces were given
  await page.evaluate(() => CH.piece('rvprobe', { mount() {}, update(S) { window.__rvS = { doors: S.doors, about: (S.doorsAbout || []).slice() }; window.__rvSall = S; }, destroy() {} }));
  await startLife(page, P, 'Lale');
  await idle();
  const saved = async () => { let t = null; for (let i = 0; i < 4 && !t; i++) { t = await page.evaluate(() => askSave()); if (!t) await page.waitForTimeout(1000); } return t; };
  if (SEED !== '-') {              // the same life every run: this start with the seed, loaded back
    const d = JSON.parse(await saved()); d.setup.seed = +SEED; d.inputs = [];
    await page.evaluate((x) => loadText(x), JSON.stringify(d));
    await page.waitForFunction(() => hud && hud.replay, null, { timeout: 120000 }).catch(() => {});
    await page.waitForFunction(() => hud && !hud.replay && !busy && hud.mode === 'play', null, { timeout: 1200000 });
    await page.waitForTimeout(1500); await idle();
  }
  say('started', Date.now() - t0, 'ms, at age', await page.evaluate(() => hud.life && hud.life.age));
  const river = () => page.evaluate(() => { const line = document.getElementById('line'), rv = line.querySelector(':scope > .rv'), cv = rv && rv.querySelector('canvas');
    const vis = (sel) => { const e = line.querySelector(sel); return !!e && getComputedStyle(e).display !== 'none'; };
    return { cls: line.classList.contains('lv-river'), first: line.firstElementChild === rv, under: !!rv && !!(rv.compareDocumentPosition(document.getElementById('river')) & 4),
      cv: !!cv && cv.width > 0 && cv.height > 0, k: cv ? +(cv.width / cv.clientWidth).toFixed(2) : 0, h: line.getBoundingClientRect().height,
      fog: vis('#fog'), band: vis('#river .band'), lays: vis('#river .lays'), glyphs: line.querySelectorAll('#river .gl[data-age]').length, ticks: line.querySelectorAll('.tick').length,
      sw: document.documentElement.scrollWidth, iw: window.innerWidth }; });

  if (parts.includes('live')) {
    say('part live');
    let k = 0, pushed = 0, cost = null;
    await page.evaluate(() => CH.pieces.get('river').perf().reset());
    const tc = Date.now(), costT = setTimeout(async () => { cost = await page.evaluate(() => { const p = CH.pieces.get('river').perf(); return p && { frames: p.frames, mean: p.mean, p95: p.p95, max: p.max, parts: p.parts }; }).catch(() => null); }, 20000);
    for (const t1 = Date.now(); Date.now() - t1 < 20 * 60000;) {
      await idle();
      const s = await page.evaluate(() => { const up = !document.getElementById('evwrap').hidden;
        return { age: hud.life && hud.life.age, mode: hud.mode, cp: !!hud.cp && up, rn: !!document.querySelector('#rnKeep') }; });
      if (s.mode !== 'play') { fails.push('the life left play at ' + s.age); break; }
      if (s.cp && s.age >= AGE && Date.now() - tc > 21000) break;
      if (s.rn) { await page.click('#rnKeep'); await page.waitForTimeout(400); continue; }
      if (s.cp) {
        const n = await page.evaluate((other) => {
          const by = (a, b) => (b.rel || 0) - (a.rel || 0), all = hud.cp.options.filter((o) => !o.own && o.means && o.means.length).sort(by);
          const os = all.filter((o) => o.status !== 'out of reach'), top = all.length && (all[0].rel || 0) >= 0.1 ? all[0] : other && os[0];
          return top ? String(top.n) : '';
        }, k++ % 2 === 0);
        if (n) pushed++;
        await page.evaluate((x) => send(x), n);
        continue;
      }
      await page.evaluate(() => send(''));
    }
    clearTimeout(costT);
    if (!cost) cost = await page.evaluate(() => { const p = CH.pieces.get('river').perf(); return p && { frames: p.frames, mean: p.mean, p95: p.p95, max: p.max, parts: p.parts }; });
    await idle();
    const st = await page.evaluate(() => ({ age: hud.life.age, pushes: CH.life.pushes.length, judged: CH.life.pushes.filter((p) => p.verdict !== 'none').length, stops: CH.life.stops.length }));
    say('  stood at age', st.age, ';', pushed, 'pushes sent,', st.pushes, 'in the log,', st.judged, 'judged,', st.stops, 'stops');
    say(`  the river's cost over ${cost ? cost.frames : 0} frames of the first 20 s: mean ${cost ? cost.mean.toFixed(2) : '?'} ms, p95 ${cost ? cost.p95.toFixed(2) : '?'} ms, worst ${cost ? cost.max.toFixed(1) : '?'} ms`);
    if (cost && cost.parts) say('  by part (ms a frame, calls, ms a call, worst):', Object.entries(cost.parts).map(([k, q]) => `${k} ${q.perFrame.toFixed(2)} ${q.n} ${q.each.toFixed(2)} ${q.max.toFixed(1)}`).join('; '));
    fs.writeFileSync(`${dir}/river-${tag}-cost.json`, JSON.stringify({ width, height, ...cost }));
    check(!!cost && cost.frames > 300, `the river drew while the life ran (${cost ? cost.frames : 0} frames in 20 s)`);
    // (the release's budget is read at 1440x900; at other sizes the cost is told, not judged)
    if (width === 1440 && height === 900) check(!!cost && cost.mean < 4 && cost.p95 < 8, 'its cost alone is inside the budget the six share (4 ms mean, 8 ms p95)');
    check(st.pushes > 0, 'the life has pushes for the river to show');
  }

  if (parts.includes('look')) {
    say('part look');
    await settle();
    await page.waitForTimeout(1200);
    const r = await river();
    const want = phone ? 64 : height > 800 ? 120 : 92;
    say('  ', JSON.stringify(r));
    check(r.cls && r.first && r.under && r.cv, 'the river is mounted: #line.lv-river, its canvas first in #line, under svg#river');
    check(r.k > 0 && r.k <= 2, `the canvas's pixel ratio is at most 2 (${r.k})`);
    check(Math.abs(r.h - want) < 0.6, `the line is ${want} px high (${r.h})`);
    check(r.sw <= r.iw, `no sideways scroll (${r.sw} <= ${r.iw})`);
    check(!r.fog && !r.band && !r.lays, 'the fog and the page\'s own river and band are hidden');
    check(r.glyphs > 0 && r.ticks > 0, `the page's glyphs and ages stay on top (${r.glyphs} glyphs, ${r.ticks} ages)`);
    await shot('page'); await lineShot('line');
  }

  if (parts.includes('read')) {
    say('part read');
    await settle();
    await page.evaluate(() => { const o = window.openYear; window.__rvOpened = []; window.openYear = (...a) => { __rvOpened.push(a[0]); return o(...a); }; });
    const tipHead = () => page.evaluate(() => { const t = document.getElementById('tip'); return t && !t.hidden && t.style.display !== 'none' && t.innerText.trim() ? t.innerText.trim().split('\n')[0] : ''; });
    const g = await page.$('#river .gl[data-age]');
    if (phone) {                      // a finger: the first tap reads the year, as the page's own tapped tips do
      check(!!g, 'a glyph to tap');
    } else if (g) {
      const age = +(await g.getAttribute('data-age'));
      await g.hover(); await page.waitForTimeout(350);
      const h = await tipHead();
      check(/^Age \d+/.test(h), `a glyph's hover shows its year (${h})`);
      await shot('glyph');
      await g.click(); await page.waitForTimeout(700);
      const opened = await page.evaluate(() => __rvOpened.slice());
      check(opened.includes(age), `its click opens that year in the story (openYear ${JSON.stringify(opened)}, glyph ${age})`);
    } else check(false, 'a glyph to hover');
    if (!phone) {
      // the canvas, row by row: every reading it gives
      const box = await page.locator('#line').boundingBox(), heads = new Map();
      for (let y = 4; y < box.height - 6; y += 5) for (let x = 6; x < box.width - 4; x += 9) {
        await page.mouse.move(box.x + x, box.y + y);
        const h = await tipHead(); if (h && !heads.has(h)) heads.set(h, [x, y]);
      }
      await page.mouse.move(box.x + box.width / 2, box.y + box.height + 60); await page.waitForTimeout(200);
      const hs = [...heads.keys()];
      say('  readings:', hs.length, '\n   ' + hs.map((h) => `${h} @${heads.get(h).join(',')}`).join('\n   '));
      fs.writeFileSync(`${dir}/river-${tag}-readings.txt`, hs.map((h) => `${h}\t${heads.get(h).join(',')}`).join('\n') + '\n');
      check(hs.some((h) => /^The years ahead/.test(h)), 'the fog reads as the years ahead');
      check(hs.some((h) => /'s ways: /.test(h)), 'a door reads as a colour\'s ways');
      check(hs.some((h) => /^Age \d+/.test(h)), 'the lived years still read their age');
      check(hs.length >= 6, `the river gives many readings (${hs.length})`);
      const about = await page.evaluate(() => window.__rvS || null);
      say('  doors', JSON.stringify(about));
      // decision 10: a door the game holds at its last clear reading says "about"; the others do not
      const NAMES = ['White', 'Blue', 'Black', 'Red', 'Green'];
      for (const [h, at] of heads.entries()) {
        const m = /^(\w+)'s ways: /.exec(h); if (!m || !about) continue;
        await page.mouse.move(box.x + at[0], box.y + at[1]); await page.waitForTimeout(250);
        const t = await page.evaluate(() => document.getElementById('tip').innerText), ab = !!about.about[NAMES.indexOf(m[1])];
        check(/about \d+% of usual/.test(t) === ab, `${m[1]}'s door ${ab ? 'says "about"' : 'gives its reading plainly'} (${(/\(([^)]*of usual)\)/.exec(t) || [])[1]})`);
      }
      // the same doors with the game holding every way steady (S.doorsAbout all true, handed to the river by hand once)
      const door = [...heads.entries()].find(([h]) => /'s ways: /.test(h));
      if (door && about && !about.about.some(Boolean)) {
        await page.evaluate(() => CH.pieces.get('river').update(Object.assign({}, window.__rvSall, { doorsAbout: [true, true, true, true, true] })));
        await page.mouse.move(box.x + door[1][0], box.y + door[1][1] + 1); await page.waitForTimeout(250);
        const t = await page.evaluate(() => document.getElementById('tip').innerText);
        check(/about \d+% of usual/.test(t) && /holds it steady/.test(t), `a door the game holds steady says "about" (${(/\(([^)]*of usual)\)/.exec(t) || [])[1]})`);
        await page.evaluate(() => CH.pieces.get('river').update(window.__rvSall));
      }
      // a reading of the fog, held for the record
      const f = heads.get(hs.find((h) => /^The years ahead/.test(h)) || '');
      if (f) { await page.mouse.move(box.x + f[0], box.y + f[1]); await page.waitForTimeout(250); await shot('reading'); }
      await page.mouse.move(box.x + box.width / 2, box.y + box.height + 60);
    } else {
      // a tap on the river reads it, and closes by itself
      const box = await page.locator('#line').boundingBox();
      await page.touchscreen.tap(box.x + box.width * 0.9, box.y + box.height * 0.3); await page.waitForTimeout(400);
      const h = await tipHead();
      check(!!h, `a tap on the river reads it (${h})`);
      await shot('tap');
    }
  }

  if (parts.includes('motion')) {
    say('part motion');
    await settle();
    const setMotion = async (m) => {
      await page.click('#tMenu'); await page.waitForTimeout(250);
      for (let i = 0; i < 4 && (await page.evaluate(() => document.documentElement.dataset.motion)) !== m; i++) { await page.click('#tPop [data-lk="motion"]'); await page.waitForTimeout(250); }
      await page.keyboard.press('Escape'); await page.waitForTimeout(250);
      if (await page.$('#tPop:not([hidden])')) { await page.click('#tMenu'); await page.waitForTimeout(200); }
      return page.evaluate(() => document.documentElement.dataset.motion);
    };
    for (const m of ['full', 'calm', 'off']) {
      const got = await setMotion(m);
      check(got === m, `motion ${m} (${got})`);
      await page.waitForTimeout(1200);
      await lineShot(`motion-${m}`);
    }
    await page.mouse.move(2, height - 2);
    await page.waitForTimeout(1500);
    const a = await lineShot(), _ = await page.waitForTimeout(800), b = await lineShot();
    check(a.equals(b), 'motion off: two shots of the line 0.8 s apart are equal');
    await setMotion('full');
  }

  if (parts.includes('reduced')) {
    say('part reduced');
    await settle();
    const m = await page.evaluate(() => [document.documentElement.dataset.motion, CH.motion()]);
    check(m[0] === 'off' && m[1] === 'off', `reduced motion counts as motion off (${m.join(', ')})`);
    await page.mouse.move(2, height - 2); await page.waitForTimeout(300);
    const was = await lineShot();
    // time runs: a year, or with a moment waiting, let them choose
    const y = await page.$('.steps4 button[data-key="y"]:not([disabled])');
    if (y) await y.click(); else await page.evaluate(() => send(''));
    await idle(); await settle(); await page.mouse.move(2, height - 2); await page.waitForTimeout(1500);
    const a = await lineShot('reduced'), _ = await page.waitForTimeout(800), b = await lineShot();
    check(!a.equals(was), 'reduced motion: the river still follows the life (a still frame per change)');
    check(a.equals(b), 'reduced motion: two shots of the line 0.8 s apart are equal');
  }

  if (parts.includes('switch')) {
    say('part switch');
    await settle();
    const st = () => page.evaluate(() => { const line = document.getElementById('line'), vis = (sel) => { const e = line.querySelector(sel); return !!e && getComputedStyle(e).display !== 'none'; };
      return { living: document.documentElement.dataset.living, cls: line.classList.contains('lv-river'), rv: !!line.querySelector('.rv'), fog: vis('#fog'), band: vis('#river .band'), lays: vis('#river .lays'),
        h: line.getBoundingClientRect().height, hov: +((document.getElementById('lineHov') || { getAttribute: () => -1 }).getAttribute('y')) }; });
    await page.click('#tMenu'); await page.waitForTimeout(300);
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(700);
    let s = await st();
    check(s.living === 'off' && !s.cls && !s.rv && s.fog && s.band && s.lays && s.hov === 0, `off: no river, the page's own line back (${JSON.stringify(s)})`);
    await page.keyboard.press('Escape'); await page.waitForTimeout(300); await lineShot('switch-off');
    await page.click('#tMenu'); await page.waitForTimeout(300);
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(900);
    s = await st();
    check(s.living === 'on' && s.cls && s.rv && !s.fog && !s.band, `on again: the river back (${JSON.stringify(s)})`);
    await page.keyboard.press('Escape'); await page.waitForTimeout(600); await lineShot('switch-on');
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_river ${parts.join(',')} ${tag}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
