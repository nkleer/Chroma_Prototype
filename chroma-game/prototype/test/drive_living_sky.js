const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD row V1, the sky and the ink (web/src/living/10-atmos.js), in the style of drive_living.js. Each part
// prints its checks and PASS or FAIL; the driver exits 1 on a FAIL, a page error or any console error.
//   look    the start screen and the first moment of a life: the sky stands in a fixed layer just before #app, today's
//           night, glow and sigil are hidden, --wet and the ink filter #chs-ink are there, the renderer is named; no
//           sideways scroll; shots. The open sky's reading opens on a hover (a tap on a phone) at the page's margin and
//           not over a panel; a press there drops ink.
//   motion  at the moment, by the Table menu's Motion row: full (two shots 0.8 s apart differ), calm, off (they are
//           equal), then full again with the system's reduced motion (equal again).
//   switch  the Living HUD row off: the sky is taken down (no layer, today's night back, no --wet, no #chs-ink); on: it
//           stands again; the classic look takes it down too and the ink look puts it back.
//   cost    a running life for 20 s (their own pick at every moment, Go on after every outcome): the sky's own script per
//           frame (performance.now() around its draw), mean and 95th percentile, with the field and sparks apart.
//   gl      add it to run the others with WebGL forced: the browser launched with --use-gl=swiftshader and
//           --enable-unsafe-swiftshader, chroma.living.gl "force"; the renderer must be webgl, shaders and all.
//   PW=<playwright> node test/drive_living_sky.js URL OUT_DIR [parts: look,motion,switch,cost] [width 1440] [height 900] [preset 4]
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, preset] = process.argv.slice(2);
const parts = (partsArg || 'look,motion,switch,cost').split(','), width = +(W || 1440), height = +(H || 900), P = preset || '4';
const GL = parts.includes('gl'), tag = `${width}${GL ? '-gl' : ''}`;
(async () => {
  const browser = await chromium.launch(GL ? { args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] } : {});
  const phone = width < 600, logs = [], fails = [], warns = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone });
  // the per-piece guard (living/00-core.js) only reports here: on a slow headless machine it would hold the piece still,
  // and this driver checks the piece's own motion (test/drive_living.js joint checks the guard)
  await ctx.addInitScript((gl) => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.setItem('chroma.living.guard', 'off'); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave');
    localStorage.removeItem('chroma.motion'); localStorage.removeItem('chroma.look'); if (gl) localStorage.setItem('chroma.living.gl', 'force'); else localStorage.removeItem('chroma.living.gl'); } catch (_) {} }, GL);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') logs.push(`console error: ${m.text()}`); else if (m.type() === 'warning' && /^living/.test(m.text())) warns.push(`console warning: ${m.text()}`); });
  const shot = (n) => page.screenshot({ path: `${dir}/sky-${tag}-${n}.png` });
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const sky = () => page.evaluate(() => {
    const h = document.querySelector('.lv-sky'), app = document.getElementById('app'), st = CH.pieces.get('sky');
    const shown = (s) => { const e = document.querySelector(s); return !!e && getComputedStyle(e).display !== 'none'; };
    return { living: document.documentElement.dataset.living, host: !!h, before: !!h && h.nextElementSibling === app, fixed: !!h && getComputedStyle(h).position === 'fixed',
      renderer: h ? h.dataset.renderer : '', canvases: h ? h.querySelectorAll('canvas').length : 0, today: ['.sky', '.glow', 'svg.sigil'].map(shown),
      wet: document.documentElement.style.getPropertyValue('--wet'), filter: !!document.getElementById('chs-ink'), stats: st && st.stats ? st.stats() : null };
  });
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.pieces && CH.pieces.get('sky') && document.querySelector('.tarot'), null, { timeout: 120000 });
  await page.waitForTimeout(1500);
  let s = await sky();
  say('start screen', JSON.stringify(s));
  check(s.living === 'on' && s.host && s.before && s.fixed && s.canvases === 3, 'the sky stands in a fixed layer just before #app, three canvases');
  check(s.today.every((x) => !x), "today's night, glow and sigil are hidden while it stands");
  check(GL ? s.renderer === 'webgl' : ['webgl', 'canvas'].includes(s.renderer), `the renderer: ${s.renderer}${GL ? ' (WebGL forced)' : ''}`);
  check(+s.wet > 0 && +s.wet <= 1 && s.filter, `--wet on <html> (${s.wet}) and the ink filter #chs-ink`);
  await shot('1-start');
  const sideways = () => page.evaluate(() => document.scrollingElement.scrollWidth - innerWidth);
  check(await sideways() <= 0, `no sideways scroll on the start screen (${await sideways()} px)`);

  await startLife(page, P, 'Lale');
  await idle();
  // the first moment the life comes to (live on until one is up)
  for (let i = 0; i < 40 && !(await page.evaluate(() => !!hud.cp && !document.getElementById('evwrap').hidden)); i++) { await page.evaluate(() => send('')); await idle(); }
  const age = await page.evaluate(() => hud.life && hud.life.age);
  say('at a moment, age', age, 'in', Math.round((Date.now() - t0) / 1000), 's');
  await page.waitForTimeout(1500);

  if (parts.includes('look')) {
    say('part look');
    s = await sky();
    check(s.host && s.today.every((x) => !x), 'in play the sky still stands and today\'s night stays hidden');
    check(await sideways() <= 0, `no sideways scroll at the moment (${await sideways()} px)`);
    await shot('2-moment');
    // the moment set aside ("Look at the life"), so the margin is the open sky
    await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(400);
    await shot('3-life');
    const pt = { x: phone ? 4 : 7, y: Math.round(height * 0.5) };
    const at = await page.evaluate((p) => { const e = document.elementFromPoint(p.x, p.y); return e ? (e.id || e.tagName) : ''; }, pt);
    const tipText = () => page.evaluate(() => { const t = document.getElementById('tip'); return t.hidden ? '' : t.innerText.split('\n')[0]; });
    if (phone) { await page.touchscreen.tap(pt.x, pt.y); await page.waitForTimeout(300); }
    else { await page.mouse.move(pt.x, pt.y - 20); await page.mouse.move(pt.x, pt.y, { steps: 3 }); await page.waitForTimeout(200); }
    const t1 = await tipText();
    check(/sky is their mind/i.test(t1), `the open sky's reading at the margin (${at}): "${t1}"`);
    await shot('4-reading');
    if (!phone) {
      const hb = await page.evaluate(() => { const r = document.getElementById('hud').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + 30 }; });
      await page.mouse.move(hb.x, hb.y, { steps: 4 }); await page.waitForTimeout(200);
      const t2 = await tipText();
      check(!/sky is their mind/i.test(t2), `over the status panel the sky's reading closes ("${t2}")`);
      await page.mouse.move(pt.x, pt.y, { steps: 4 }); await page.waitForTimeout(100);
      await page.mouse.down(); await page.mouse.move(pt.x + 2, pt.y + 60, { steps: 12 }); await page.mouse.up();
    } else {
      await page.touchscreen.tap(pt.x, pt.y + 40);
    }
    await page.waitForTimeout(700);
    const inked = await page.evaluate(() => getComputedStyle(document.querySelector('.lv-sky .chs-atmos-ink')).visibility);
    check(inked === 'visible', `a press on the open sky drops ink (the ink layer is ${inked})`);
    const sel = await page.evaluate(() => String(getSelection() || '').length);
    check(sel === 0, `the drag selected no text in the panels (${sel} characters)`);
    await shot('5-ink');
    await page.click('#evback').catch(() => {}); await page.waitForTimeout(400);
  }

  // a row of the Table menu (the moment window covers the menu: it is set aside first and brought back after)
  const menuRow = async (sel) => {
    const up = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !w.hidden && !w.classList.contains('peek'); });
    if (up) { await page.click('#evPeek'); await page.waitForTimeout(400); }
    await page.click('#tMenu'); await page.waitForTimeout(250); await page.click(`#tPop ${sel}`); await page.waitForTimeout(250); await page.keyboard.press('Escape'); await page.waitForTimeout(250);
    if (up) { await page.click('#evback').catch(() => {}); await page.waitForTimeout(400); }
  };
  const motionNow = () => page.evaluate(() => [document.documentElement.dataset.motion, CH.motion()]);
  // two shots 0.8 s apart (the pointer parked off the panels' hover areas first)
  const still = async (n) => { await page.mouse.move(width - 2, 2); await page.evaluate(() => hideTip()); await page.waitForTimeout(1500);
    const a = await page.screenshot({ path: `${dir}/sky-${tag}-${n}-a.png` }); await page.waitForTimeout(800); const b = await page.screenshot({ path: `${dir}/sky-${tag}-${n}-b.png` }); return a.equals(b); };

  if (parts.includes('motion')) {
    say('part motion');
    await idle();
    if (await page.evaluate(() => document.getElementById('evwrap').classList.contains('peek'))) { await page.click('#evback').catch(() => {}); await page.waitForTimeout(300); }
    check(!(await still('motion-full')), `full motion: the sky moves (two shots 0.8 s apart differ; ${JSON.stringify(await motionNow())})`);
    await menuRow('[data-lk="motion"]');
    const calm = await motionNow();
    check(calm[0] === 'calm' && calm[1] === 'calm', `calm by the Motion row (${calm})`);
    await page.waitForTimeout(1000); await shot('motion-calm');
    await menuRow('[data-lk="motion"]');
    const off = await motionNow();
    check(off[0] === 'off' && off[1] === 'off', `off by the Motion row (${off})`);
    check(await still('motion-off'), 'motion off: two shots 0.8 s apart are equal');
    await menuRow('[data-lk="motion"]');
    await page.emulateMedia({ reducedMotion: 'reduce' }); await page.waitForTimeout(500);
    const red = await motionNow();
    check(red[0] === 'off' && red[1] === 'off', `the system's reduced motion counts as off (${red})`);
    check(await still('motion-reduced'), 'reduced motion: two shots 0.8 s apart are equal');
    await page.emulateMedia({ reducedMotion: 'no-preference' }); await page.waitForTimeout(500);
    check((await motionNow())[0] === 'full', 'full motion again');
  }

  if (parts.includes('switch')) {
    say('part switch');
    await menuRow('[data-lv]');
    s = await sky();
    check(s.living === 'off' && !s.host && s.today.every((x) => x) && !s.wet && !s.filter && !s.stats, `off: the sky is taken down, today's night is back (${JSON.stringify(s)})`);
    await shot('switch-off');
    await menuRow('[data-lv]');
    s = await sky();
    check(s.living === 'on' && s.host && s.before && s.today.every((x) => !x) && s.filter, `on again: the sky stands again (${s.renderer})`);
    await menuRow('[data-lk="look"]');
    s = await sky();
    check(s.living === 'off' && !s.host && s.today.every((x) => x), 'the classic look: no sky, today\'s night');
    await menuRow('[data-lk="look"]');
    s = await sky();
    check(s.living === 'on' && s.host && s.today.every((x) => !x), 'the ink look again: the sky stands');
    await page.waitForTimeout(1000);
    await shot('switch-on');
  }

  if (parts.includes('cost')) {
    say('part cost');
    await idle();
    await page.evaluate(() => CH.pieces.get('sky').stats(true));
    const tC = Date.now(); let n = 0;
    while (Date.now() - tC < 20000) {
      const st = await page.evaluate(() => ({ busy, up: !document.getElementById('evwrap').hidden, cp: !!hud.cp, res: !!hud.res, rn: !!document.querySelector('#rnKeep'), mode: hud.mode }));
      if (st.mode !== 'play') break;
      if (!st.busy && !(await page.evaluate(() => !!choosing))) {
        if (st.rn) await page.click('#rnKeep').catch(() => {});
        else { await page.evaluate(() => send('')); n++; }
      }
      await page.waitForTimeout(250);
    }
    const c = await page.evaluate(() => CH.pieces.get('sky').stats());
    const f = (v) => (v == null ? '-' : (+v).toFixed(2));
    say(`  ${Math.round((Date.now() - tC) / 1000)} s, ${n} steps sent, ${c.n} frames, renderer ${c.renderer}: mean ${f(c.mean)} ms, p95 ${f(c.p95)} ms, p50 ${f(c.p50)}, max ${f(c.max)}; field ${f(c.field)}, sparks ${f(c.sparks)}, ink ${f(c.ink)}${c.fieldHz ? `, field ${c.fieldHz}/s` : ''}${c.gpu != null ? `, gpu ${f(c.gpu)}` : ''}; ease ${f(c.ease)} s`);
    require('fs').writeFileSync(`${dir}/sky-${tag}-cost.json`, JSON.stringify(c));
    // at least 5 frames a second: headless Canvas2D draws about 13, software WebGL (SwiftShader) about 6
    check(c.n > 100, `the sky drew while the life ran (${c.n} frames)`);
    await shot('cost-end');
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_sky ${parts.join(',')} ${width}x${height}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
