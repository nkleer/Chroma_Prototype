const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD, row V2: the star (web/src/living/20-star.js). It stands over the HUD's wheel (svg#hudWheel stays laid out
// but hidden), plays the wheel's motion, follows the interlude's weeks and answers the wheel's hovers. The star's root
// element carries lvPeek(), a read-only look at what it draws. Each part prints its checks and PASS or FAIL; the driver
// exits 1 on a FAIL, a page error or a console error.
//   look       at the first moment, set aside: the star over the wheel (its size, the canvas at most 2 device pixels a
//              pixel), the svg hidden but laid out; on the phone no sideways scroll, and the HUD drawer opened shows the star.
//              Shots: the page and the wheel's box.
//   hover      (not on touch) each orb fills #tip with the page's own color reading (tipColor), the canvas answers too,
//              #wKey reads the star's key; at the moment each card lights its colors (lvPeek().ends) and leaving clears
//              them; the voice row, when the life has one, runs the voice along the star.
//   motion     the Table menu's Motion row: calm, then off (two shots of the wheel's box 0.8 s apart are equal), then the
//              system's reduced motion with Motion full (still too), then full again (the star breathes: the shots differ).
//   outcome    (not on touch) a choice: the outcome's frames wait on the star until the outcome shows (the "outcome" event),
//              3 s at most, then play.
//   interlude  the everyday interlude (pace slow) after an outcome: on wide screens the HUD's star follows the weeks and
//              moves; on narrow ones (the HUD is a drawer) a small star stands over #ilWheel and moves. After it, the small
//              star is gone and the HUD's star follows the states again.
//   switch     the Table menu's Living HUD row: off brings today's wheel back (no star, the svg shown, #wKey today's key),
//              on brings the star back.
//   cost       the star alone: its mount, update, hooks, events and frame loop timed (the switch turned off and on so the
//              star mounts again under the timers), over 20 s of a life running with the interlude on; mean and p95 ms of
//              script a frame, against the budget for all six pieces (4 ms mean, 8 ms p95).
//   PW=<playwright> node test/drive_living_star.js URL OUT_DIR [parts: look,hover,motion,outcome,interlude,switch,cost]
//     [width 1440] [height 900] [preset 3]
const { startLife, idleOf } = require('./start.js');
const fs = require('fs');
const [url, dir, partsArg, W, H, preset] = process.argv.slice(2);
const parts = (partsArg || 'look,hover,motion,outcome,interlude,switch,cost').split(','), width = +(W || 1440), height = +(H || 900), P = preset || '3';
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600, wide = width > 1040, logs = [], fails = [], say = (...a) => console.log(...a);
  // the phone at 3 device pixels a pixel: the star's canvases must stay at 2
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone, deviceScaleFactor: phone ? 3 : 2 });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); for (const k of ['chroma.living', 'chroma.autosave', 'chroma.motion']) localStorage.removeItem(k); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const warns = [];          // a piece that falls back to today's says so with console.warn: told, not a failure
  page.on('console', (m) => { if (m.type() === 'error') logs.push(`console error: ${m.text()}`); else if (m.type() === 'warning' && /^living/.test(m.text())) warns.push(`console warning: ${m.text()}`); });
  const tag = `${width}x${height}`;
  const shot = (n) => page.screenshot({ path: `${dir}/star-${tag}-${n}.png` });
  const boxShot = async (n, sel = '.wheelw') => { const el = await page.$(sel); return el ? el.screenshot({ path: `${dir}/star-${tag}-${n}.png` }) : null; };
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const HUD = '.wheelw > .lv-star .chs-star', MINI = '.ilside > .lv-star .chs-star';
  const peek = (sel = HUD) => page.evaluate((s) => { const r = document.querySelector(s); return r && r.lvPeek ? r.lvPeek() : null; }, sel);
  const where = () => page.evaluate(() => { const w = document.getElementById('evwrap');
    return { age: hud && hud.life && hud.life.age, cp: !!(hud && hud.cp) && !w.hidden, peek: w.classList.contains('peek'), res: !!document.querySelector('#goOn') && !w.hidden, mode: hud && hud.mode }; });
  // to the next moment, with its window open
  const toMoment = async () => {
    for (let i = 0; i < 40; i++) {
      await idle();
      const s = await where();
      if (s.cp) { if (s.peek) { await page.click('#evback'); await page.waitForTimeout(400); } return true; }
      if (await page.$('#rnKeep')) { await page.click('#rnKeep'); await page.waitForTimeout(400); continue; }
      await page.evaluate(() => send(''));
    }
    return false;
  };
  // the moment set aside ("Look at the life"), so the HUD is free to hover
  const aside = async () => { const s = await where(); if (s.cp && !s.peek) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(500); } };
  // the Table menu and its rows: clicked as an element (on the phone the page's own top bar can sit under the moment's
  // strip, which is not what these checks are about)
  const menu = (sel) => page.evaluate((x) => document.querySelector(x).click(), sel);
  const motionTo = async (m) => {
    await menu('#tMenu'); await page.waitForTimeout(250);
    for (let i = 0; i < 3; i++) {
      const v = await page.evaluate(() => ((document.querySelector('#tPop [data-lk="motion"] .v') || {}).textContent || '').trim());
      if (v === m) break;
      await menu('#tPop [data-lk="motion"]'); await page.waitForTimeout(250);
    }
    await page.keyboard.press('Escape'); await page.waitForTimeout(200);
    return page.evaluate(() => document.documentElement.dataset.motion);
  };
  // the HUD's drawer on narrow screens (1040 px or less), open or shut
  // (open, the drawer covers #tHud on the phone: #hudClose shuts it, as drive_hud2 does)
  const drawer = async (o) => { if (wide) return; if (await page.evaluate(() => hudEl.classList.contains('open')) !== o) { await page.click(o ? '#tHud' : '#hudClose'); await page.waitForTimeout(800); } };
  const same = (a, b) => a && b && a.length === b.length && a.equals(b);
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.piece && CH.pieces && CH.pieces.has('star'), null, { timeout: 120000 });
  await startLife(page, P, 'Lale');
  await idle();
  check(await toMoment(), 'a moment comes');
  say('started', Date.now() - t0, 'ms, at age', (await where()).age);

  if (parts.includes('look')) {
    say('part look');
    await aside(); await page.mouse.move(2, 2); await page.waitForTimeout(1500);
    const s = await page.evaluate(() => { const svg = document.getElementById('hudWheel'), host = document.querySelector('.wheelw > .lv-star'), cv = host && host.querySelector('.st-cv');
      const cs = svg && getComputedStyle(svg);
      return { host: !!host, after: !!host && svg.nextElementSibling === host, stars: document.querySelectorAll('.lv-star .chs-star').length, vis: cs && cs.visibility, disp: cs && cs.display, laid: !!svg && svg.offsetParent !== null,
        svgW: svg && svg.getBoundingClientRect().width, k: cv ? +(cv.width / Math.max(1, cv.offsetWidth)).toFixed(3) : 0, dpr: devicePixelRatio,
        sw: document.documentElement.scrollWidth, iw: innerWidth, orbs: host ? host.querySelectorAll('.st-orb').length : 0, key: (document.getElementById('wKey') || {}).ariaLabel };
    });
    const p = await peek();
    say('  ', JSON.stringify(s), 'star', p && p.s, 'px, label', p && p.label);
    check(s.host && s.after && s.stars === 1, 'one star, its host right after svg#hudWheel in .wheelw');
    check(s.vis === 'hidden' && s.disp !== 'none' && s.laid, `svg#hudWheel hidden but laid out (visibility ${s.vis}, display ${s.disp}, offsetParent ${s.laid})`);
    check(!!p && p.has && p.s >= 60 && p.w.every((x) => x >= 0), `the star draws the life (has ${p && p.has}, ${p && p.s} px)`);
    if (wide) check(p && p.s >= 150 && p.s <= 190, `at the HUD's wheel size (${p && p.s} px; the wheel's svg is ${Math.round(s.svgW)} px wide)`);
    check(s.k > 0 && s.k <= 2.001, `the canvas at most 2 device pixels a pixel (${s.k} at devicePixelRatio ${s.dpr})`);
    check(s.orbs === 5 && s.key === 'How to read the star', `five orbs; #wKey reads the star (${s.key})`);
    if (phone) check(s.sw <= s.iw + 1, `no sideways scroll (${s.sw} wide in ${s.iw})`);
    await shot('look'); await boxShot('wheel');
    if (!wide) {
      await drawer(true);
      const q = await peek(), open = await page.evaluate(() => hudEl.classList.contains('open'));
      const sw = await page.evaluate(() => document.documentElement.scrollWidth);
      say('  drawer', open, 'star', q && q.s, 'px at', q && JSON.stringify(q.box));
      check(open && q && q.s >= 60 && q.box.width >= 60 && q.box.left >= 0 && q.box.right <= width + 1, `the drawer opened shows the star in view (${q && q.s} px)`);
      if (phone) check(sw <= width + 1, `no sideways scroll with the drawer open (${sw})`);
      await shot('drawer'); await boxShot('drawer-wheel');
      await drawer(false);
    }
  }

  if (parts.includes('hover') && !phone) {
    say('part hover');
    await aside(); await drawer(true);
    const tipText = () => page.evaluate(() => { const t = document.getElementById('tip'); return t && !t.hidden ? t.textContent.replace(/\s+/g, ' ').trim() : ''; });   // #tip is fixed: no offsetParent
    const norm = (h) => page.evaluate((x) => { const d = document.createElement('div'); d.innerHTML = x; return d.textContent.replace(/\s+/g, ' ').trim(); }, h);
    let good = 0;
    for (const [i, c] of ['W', 'U', 'B', 'R', 'G'].entries()) {
      await page.hover(`${HUD} .st-orb[data-c="${c}"]`); await page.waitForTimeout(350);
      const got = await tipText(), want = await norm(await page.evaluate((j) => tipColor(hud.life, j), i));
      if (got && got === want) good++; else say(`   orb ${c}: #tip "${got.slice(0, 120)}" wanted "${want.slice(0, 120)}"`);
      const pk = await peek(); if (i === 1) { await shot('hover-orb'); say('   orb', c, 'tip:', got.slice(0, 100)); }
      void pk;
    }
    check(good === 5, `each orb fills #tip with the page's color reading (${good} of 5)`);
    await page.mouse.move(2, 2); await page.waitForTimeout(300);
    const p = await peek();
    const pt = p.P && p.P[0] ? [p.box.left + p.P[0][0] * p.box.width / p.s, p.box.top + p.P[0][1] * p.box.height / p.s] : [p.box.left + p.box.width / 2, p.box.top + p.box.height / 2];
    await page.mouse.move(pt[0], pt[1]); await page.waitForTimeout(400);
    const tc = await tipText(); say('   canvas at', pt.map(Math.round).join(','), 'tip:', tc.slice(0, 100));
    await page.mouse.move(p.box.left + p.box.width / 2, p.box.top + p.box.height / 2); await page.waitForTimeout(400);
    const tm = await tipText(); say('   canvas middle tip:', tm.slice(0, 100));
    check(!!tc || !!tm, 'the canvas fills #tip');
    await page.mouse.move(2, 2); await page.waitForTimeout(300);
    await page.hover('#wKey'); await page.waitForTimeout(400);
    const tk = await tipText();
    check(/How to read the star/.test(tk) && /Now/.test(tk) && /Wants/.test(tk), `#wKey reads the star's key ("${tk.slice(0, 80)}")`);
    await shot('hover-key');
    await page.mouse.move(2, 2); await page.waitForTimeout(300);
    // the voice row, when this life has one
    const vr = await page.$('#voiceRow');
    if (vr && await vr.isVisible()) {
      await vr.hover(); await page.waitForTimeout(300);
      const a = await peek(); await shot('hover-voice');
      await page.mouse.move(2, 2); await page.waitForTimeout(300);
      const b = await peek();
      check(a.voice && !b.voice, `the voice row runs the voice along the star while read (voice ${a.voice}, ${a.flows} flows; after ${b.voice})`);
    } else say('   no voice row in this HUD now');
    // the cards light their colors
    await drawer(false);
    const s = await where(); if (s.cp && s.peek) { await page.click('#evback'); await page.waitForTimeout(500); }
    const cards = await page.evaluate(() => [...tableEl.querySelectorAll('.opt[data-i]')].map((b) => ({ i: +b.dataset.i, ends: (hud.cp.options[+b.dataset.i] || {}).ends || '', vis: b.offsetParent !== null })));
    let lit = 0, tried = 0;
    for (const c of cards.filter((x) => x.vis).slice(0, 4)) {
      await page.hover(`#table .opt[data-i="${c.i}"]`).catch(() => {}); await page.waitForTimeout(250);
      const e = (await peek()).ends.map((j) => 'WUBRG'[j]).join(''), want = [...'WUBRG'].filter((x) => c.ends.includes(x)).join('');
      tried++; if (e === want) lit++; else say(`   card ${c.i}: lit "${e}" wanted "${want}"`);
    }
    if (wide) await shot('hover-card');
    await page.mouse.move(2, 2); await page.waitForTimeout(300);
    const after = (await peek()).ends;
    check(tried > 0 && lit === tried && after.length === 0, `each card lights its colors on the star and leaving clears them (${lit} of ${tried}; after: ${after.length})`);
  }

  if (parts.includes('motion')) {
    say('part motion');
    await aside(); await page.mouse.move(2, 2);
    const m1 = await motionTo('calm'); await drawer(true); await page.waitForTimeout(800);
    const pc = await peek();
    check(m1 === 'calm' && pc && pc.has, `calm: html[data-motion] ${m1}, the star drawn`);
    await boxShot('calm');
    const still = async (n) => { await page.waitForTimeout(900); await boxShot(n + '-a'); await page.waitForTimeout(800); await boxShot(n + '-b');
      return same(fs.readFileSync(`${dir}/star-${tag}-${n}-a.png`), fs.readFileSync(`${dir}/star-${tag}-${n}-b.png`)); };
    const m2 = await motionTo('off'); await drawer(true);
    check(m2 === 'off' && await still('off'), `off: two shots of the wheel's box 0.8 s apart are equal (motion ${m2})`);
    await page.emulateMedia({ reducedMotion: 'reduce' });
    const m3 = await motionTo('full'); await drawer(true);
    check(m3 === 'off' && await still('reduced'), `the system's reduced motion with Motion full: still too (html[data-motion] ${m3})`);
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    const m4 = await motionTo('calm'), m5 = await motionTo('full'); await drawer(true);
    await page.waitForTimeout(900); await boxShot('full-a'); await page.waitForTimeout(800); await boxShot('full-b');
    const moved = !same(fs.readFileSync(`${dir}/star-${tag}-full-a.png`), fs.readFileSync(`${dir}/star-${tag}-full-b.png`));
    check(m5 === 'full' && moved, `full again: the star breathes (shots differ: ${moved}; motion ${m4} then ${m5})`);
    await drawer(false);
  }

  if (parts.includes('outcome') && !phone) {
    say('part outcome');
    await toMoment(); await page.mouse.move(2, 2);
    // the moment's own arrival may still be playing on the star: the choice comes after it
    await page.waitForFunction((sel) => { const r = document.querySelector(sel); return r && r.lvPeek && !r.lvPeek().playing; }, HUD, { timeout: 5000 }).catch(() => {});
    await page.evaluate(() => { window.__out = null; const off = CH.on('outcome', () => { window.__out = performance.now(); off(); });
      // each time the wheel's motion comes to the star: when, how many frames, and whether a choice was being lived
      const p = CH.pieces.get('star'), f = p.hooks.animSpider; window.__plays = [];
      if (!f.__logged) { p.hooks.animSpider = function (svg, fs, ms) { if (svg && svg.id === 'hudWheel') __plays.push({ t: performance.now(), n: fs ? fs.length : 0, ms, choosing: !!choosing }); return f.apply(this, arguments); }; p.hooks.animSpider.__logged = true; } });
    const t1 = await page.evaluate(() => { send(''); return performance.now(); });
    const seen = [];
    for (let i = 0; i < 120; i++) {
      await page.waitForTimeout(50);
      const s = await page.evaluate((sel) => { const r = document.querySelector(sel), p = r && r.lvPeek ? r.lvPeek() : {}; return { t: performance.now(), waiting: p.waiting, playing: p.playing, out: window.__out, choosing: !!choosing,
        flare: document.querySelectorAll('.lv-star .st-orb.flare, .lv-star .st-orb.ebb').length }; }, HUD);
      seen.push(s);
      if (s.out && !s.playing && s.t - s.out > 1500) break;
    }
    const plays = await page.evaluate(() => __plays);
    say('  the wheel\'s motion came at', plays.map((x) => `${Math.round(x.t - t1)} ms (${x.n} frames over ${x.ms} ms${x.choosing ? ', choosing' : ''})`).join('; ') || 'no time');
    const w = seen.filter((s) => s.waiting), out = seen.find((s) => s.out), played = seen.filter((s) => s.playing && !s.waiting);
    const waitEnd = w.length ? w[w.length - 1].t : null, outAt = out ? out.out : null;
    say('  choice at 0 ms; outcome told at', outAt && Math.round(outAt - t1), 'ms; the star waited', w.length ? `${Math.round(w[0].t - t1)} to ${Math.round(waitEnd - t1)} ms` : 'never',
      '; played', played.length ? `from ${Math.round(played[0].t - t1)} ms` : 'nothing', '; orbs flaring at most', Math.max(0, ...seen.map((s) => s.flare)));
    if (w.length) check(outAt && waitEnd <= outAt + 250 && waitEnd - t1 <= 3400, `the outcome's frames wait until the outcome shows (wait ends ${Math.round(waitEnd - (outAt || t1))} ms after it)`);
    else say('   no wait was caught between two samples');
    const early = seen.filter((s) => s.playing && !s.waiting && !s.out).length;
    check(!early && played.length > 0, `the star moves only once the outcome shows (${early} samples moving before it, ${played.length} after)`);
    check(!!outAt, 'the outcome was told');
    await idle(); await shot('outcome');
  }

  if (parts.includes('interlude')) {
    say('part interlude');
    await page.evaluate(() => { try { localStorage.setItem('chroma.pace', 'slow'); } catch (_) {} ilPace = 'slow'; });
    await toMoment(); await page.evaluate(() => send('')); await idle();       // the choice; its outcome
    let s = await where(); if (s.res) await page.evaluate(() => send(''));    // Go on: the interlude runs to the next moment
    const ok = await page.waitForFunction(() => IL.on, null, { timeout: 30000 }).then(() => true, () => false);
    check(ok, 'the interlude runs');
    if (ok) {
      await page.waitForTimeout(600);
      const side = await page.evaluate(() => IL.side), sel = side ? MINI : HUD, xs = [];
      // (sampled until the weeks have run on 6 or more, 12 s at most: on a loaded machine the weeks can come late)
      for (let i = 0; i < 40; i++) { const p = await peek(sel); const k = await page.evaluate(() => IL.on ? IL.k : -1); if (p && k >= 0) xs.push({ k, x: p.x, f: p.following, s: p.s, has: p.has }); else if (k < 0) break;
        if (xs.length > 3 && xs[xs.length - 1].k - xs[0].k >= 6) break; await page.waitForTimeout(300); if (i === 4) await shot('interlude'); }
      say('  samples while it ran (week, following):', xs.map((a) => `${a.k.toFixed(1)}${a.f ? '' : '!'}`).join(' '));
      // moved with the weeks: between two samples the week changed and so did the star
      const moved = xs.some((a, n) => n && a.k - xs[n - 1].k >= 0.5 && a.x.some((v, j) => Math.abs(v - xs[n - 1].x[j]) > 0.002));
      const st = await page.evaluate(() => ({ minis: document.querySelectorAll('.ilside > .lv-star').length, stars: document.querySelectorAll('.lv-star .chs-star').length,
        ilVis: document.getElementById('ilWheel') ? getComputedStyle(document.getElementById('ilWheel')).visibility : null, hudFollow: (() => { const r = document.querySelector('.wheelw > .lv-star .chs-star'); return r ? r.lvPeek().following : null; })() }));
      say('  side', side, JSON.stringify(st), 'weeks', xs.length ? `${xs[0].k.toFixed(1)} to ${xs[xs.length - 1].k.toFixed(1)}` : '-', 'star', xs[0] && xs[0].s, 'px');
      if (side) check(st.minis === 1 && st.ilVis === 'hidden' && xs.length > 0 && xs.every((a) => a.f), `narrow: a small star over #ilWheel (hidden), following the weeks (${st.minis} small star, ${st.stars} stars on the page)`);
      else check(st.minis === 0 && xs.length > 0 && xs.every((a) => a.f), `wide: the HUD's star follows the weeks, no second star (${st.minis} small)`);
      check(moved, `the star moves with the weeks (${xs.length} samples)`);
      if (phone) check(await page.evaluate(() => document.documentElement.scrollWidth) <= width + 1, 'no sideways scroll in the interlude');
      await page.waitForFunction(() => !IL.on, null, { timeout: 60000 }).catch(() => page.click('#ilSkip').catch(() => {}));
      await idle(); await page.waitForTimeout(800);
      const e = await page.evaluate(() => ({ minis: document.querySelectorAll('.ilside > .lv-star').length, f: (() => { const r = document.querySelector('.wheelw > .lv-star .chs-star'); return r ? r.lvPeek().following : null; })() }));
      check(e.minis === 0 && e.f === false, `after it: no small star, the HUD's star follows the states again (${JSON.stringify(e)})`);
    }
    await page.evaluate(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} ilPace = 'off'; });
  }

  if (parts.includes('switch')) {
    say('part switch');
    await idle(); await aside();
    const st = () => page.evaluate(() => { const svg = document.getElementById('hudWheel');
      return { living: document.documentElement.dataset.living, stars: document.querySelectorAll('.lv-star').length, vis: svg && getComputedStyle(svg).visibility, key: (document.getElementById('wKey') || {}).ariaLabel,
        drawn: !!svg && svg.querySelectorAll('*').length > 5 }; });
    const flip = async () => { await menu('#tMenu'); await page.waitForTimeout(300); await menu('#tPop [data-lv]'); await page.waitForTimeout(500); await page.keyboard.press('Escape'); await page.waitForTimeout(500); };
    let s = await st();
    check(s.living === 'on' && s.stars === 1 && s.vis === 'hidden', `on: the star (${JSON.stringify(s)})`);
    await flip(); s = await st();
    check(s.living === 'off' && s.stars === 0 && s.vis === 'visible' && s.drawn && s.key === 'How to read the wheel', `off: today's wheel back, no star (${JSON.stringify(s)})`);
    if (wide) { await page.hover('#wKey'); await page.waitForTimeout(400); const t = await page.evaluate(() => document.getElementById('tip').textContent); check(/How to read the wheel/.test(t), "off: #wKey reads today's key"); await page.mouse.move(2, 2); }
    await drawer(true); await boxShot('switch-off'); await drawer(false);
    await flip(); s = await st(); await page.waitForTimeout(800);
    const p = await peek();
    check(s.living === 'on' && s.stars === 1 && s.vis === 'hidden' && s.key === 'How to read the star' && p && p.has, `on again: the star back (${JSON.stringify(s)})`);
    await drawer(true); await boxShot('switch-on'); await drawer(false);
  }

  if (parts.includes('cost')) {
    say('part cost');
    await idle(); await aside(); await page.mouse.move(2, 2);
    await page.evaluate(() => {
      const C = window.__cost = { cur: 0, depth: 0, samples: [], on: false, calls: 0, by: {} };
      const timed = (fn, what) => function (...a) { if (C.depth) return fn.apply(this, a); C.depth++; const t = performance.now();
        try { return fn.apply(this, a); } finally { C.depth--; const d = performance.now() - t; C.cur += d; C.calls++; if (C.on) { const e = C.by[what] || (C.by[what] = [0, 0]); e[0] += d; e[1]++; } } };
      const p = CH.pieces.get('star');
      for (const k of ['mount', 'update', 'destroy']) if (p[k]) p[k] = timed(p[k], k);
      for (const k of Object.keys(p.hooks || {})) p.hooks[k] = timed(p.hooks[k], 'hook ' + k);
      // the frame loop and the events the star takes on while its own code runs
      const f0 = CH.frame, on0 = CH.on;
      CH.frame = (fn, el) => f0(C.depth ? timed(fn, 'frame') : fn, el);
      CH.on = (ev, fn) => on0(ev, C.depth ? timed(fn, 'on ' + ev) : fn);
      const loop = () => { if (C.on) C.samples.push(C.cur); C.cur = 0; requestAnimationFrame(loop); };
      requestAnimationFrame(loop);
    });
    for (let i = 0; i < 2; i++) { await menu('#tMenu'); await page.waitForTimeout(300); await menu('#tPop [data-lv]'); await page.waitForTimeout(500); await page.keyboard.press('Escape'); await page.waitForTimeout(300); }
    check(await page.evaluate(() => document.documentElement.dataset.living === 'on' && !!document.querySelector('.wheelw > .lv-star')), 'the star mounted again under the timers');
    await page.evaluate(() => { try { localStorage.setItem('chroma.pace', 'slow'); } catch (_) {} ilPace = 'slow'; __cost.samples.length = 0; __cost.on = true; });
    // a running life for 20 s: Go on after an outcome, let them choose at a moment, else live on (the interlude plays)
    const tR = Date.now(); let sent = 0, ils = 0;
    while (Date.now() - tR < 20000) {
      const s = await page.evaluate(() => ({ free: !busy && !choosing && !IL.on && ready, il: IL.on }));
      if (s.il) ils++;
      if (s.free) { await page.evaluate(() => { const w = document.getElementById('evwrap'); if (w.classList.contains('peek')) setPeek(false); send(''); }); sent++; }
      await page.waitForTimeout(250);
    }
    const r = await page.evaluate(() => { __cost.on = false; const s = __cost.samples.slice().sort((a, b) => a - b), n = s.length, sum = s.reduce((a, b) => a + b, 0), busyF = s.filter((x) => x > 0.01);
      const by = Object.fromEntries(Object.entries(__cost.by).map(([k, [t, c]]) => [k, { ms: +t.toFixed(1), calls: c, perFrame: +(t / Math.max(1, n)).toFixed(3) }]));
      return { n, mean: sum / Math.max(1, n), p95: s[Math.floor(n * 0.95)] || 0, p99: s[Math.floor(n * 0.99)] || 0, max: s[n - 1] || 0, drawn: busyF.length, meanDrawn: busyF.reduce((a, b) => a + b, 0) / Math.max(1, busyF.length), calls: __cost.calls, by }; });
    say(`  ${r.n} frames in 20 s (${sent} keys sent, the interlude on in ${ils} of the polls); the star's script: mean ${r.mean.toFixed(3)} ms a frame, p95 ${r.p95.toFixed(3)}, p99 ${r.p99.toFixed(3)}, max ${r.max.toFixed(2)};`
      + ` ${r.drawn} frames with star work (mean ${r.meanDrawn.toFixed(3)} ms on those)`);
    say('  by part (ms a frame):', Object.entries(r.by).map(([k, v]) => `${k} ${v.perFrame} (${v.calls} calls)`).join(', '));
    fs.writeFileSync(`${dir}/star-${tag}-cost.json`, JSON.stringify({ ...r, sent, ils, width, height }, null, 1));
    // headless Chromium draws 7 to 13 frames a second here (no GPU): the bar is 5 frames a second
    check(r.n >= 100 && r.mean <= 4 && r.p95 <= 8, `the star alone within the budget for all six (4 ms mean, 8 ms p95): mean ${r.mean.toFixed(2)}, p95 ${r.p95.toFixed(2)}`);
    await shot('cost-end');
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_star ${parts.join(',')} at ${tag}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
