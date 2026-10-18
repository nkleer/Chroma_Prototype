const { chromium } = require(process.env.PW || 'playwright');
// v23 Living HUD row V5, the story (web/src/living/50-story.js): today's chronicle in the voice's hand. Each part prints its
// checks and PASS or FAIL; the driver exits 1 on a FAIL, a page error or a console error.
//   look    a life lived to AGE (drive_living's: preset 4, seed 140892, pushing the act they mind most where one is minded),
//           counting the lines that soak in on the way; then: every year has its hand and its quill, closed years have the
//           hand of the stop they closed at, the year being lived is marked; the markers keep their hovers (mkTip), the
//           quill and the year's head have theirs; a fold closes and opens; no sideways scroll; shots of the story; with
//           motion off two shots 0.8 s apart are equal and nothing soaked.
//   cost    20 s of the life running (moments let be, Go on): this piece's script time a frame (CH.mods.story.cost), its
//           mean, 95th percentile and worst over every frame drawn.
//   load    the story's look dumped (each year's hand, quill, first line and old hand), the life saved (key s) and loaded
//           back (key o), the dump again: the two must be equal.
//   switch  the Table menu's Living HUD row: off takes every class, property and child out of the story (the first lines
//           as the page wrote them, its words unchanged); on puts them back.
//   PW=<playwright> node test/drive_living_story.js URL OUT_DIR [parts: look,cost,load,switch] [width 1440] [height 900]
//     [motion full|calm|off] [preset 4] [age 30] [seed 140892]
const fs = require('fs');
const { startLife, idleOf } = require('./start.js');
const [url, dir, partsArg, W, H, motionArg, preset, toAge, seedArg] = process.argv.slice(2);
const parts = (partsArg || 'look').split(','), width = +(W || 1440), height = +(H || 900), MOTION = motionArg || 'full';
const P = preset || '4', AGE = +(toAge || 30), SEED = seedArg || '140892';
(async () => {
  const browser = await chromium.launch(process.env.FONTS_PROXY ? { proxy: { server: process.env.FONTS_PROXY } } : {});
  const phone = width < 600, logs = [], fails = [], warns = [], say = (...a) => console.log(...a);
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: phone, isMobile: phone, ignoreHTTPSErrors: !!process.env.FONTS_PROXY });
  await ctx.addInitScript((m) => { try { localStorage.setItem('chroma.pace', 'off'); localStorage.setItem('chroma.motion', m); localStorage.removeItem('chroma.living'); localStorage.removeItem('chroma.autosave'); } catch (_) {} }, MOTION);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') logs.push(`console error: ${m.text()}`); else if (m.type() === 'warning' && /^living/.test(m.text())) warns.push(`console warning: ${m.text()}`); });
  const tag = `${width}-${MOTION}`;
  const shot = (n, o) => page.screenshot(Object.assign({ path: `${dir}/story-${tag}-${n}.png` }, o || {}));
  const idle = idleOf(page, logs);
  const check = (ok, what) => { say(`  ${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) fails.push(what); };
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForFunction(() => window.CH && CH.piece && CH.life && CH.mods && CH.mods.story, null, { timeout: 120000 });
  check(await page.evaluate((m) => document.documentElement.dataset.living === 'on' && document.documentElement.dataset.motion === m, MOTION), `Living on, motion ${MOTION}`);
  // the lines that soak in, counted as they come (an element given sy-in)
  await page.evaluate(() => {
    const T = window.__sy = { soaked: 0, years: 0 };
    new MutationObserver((rs) => { for (const r of rs) { const e = r.target; if (r.attributeName !== 'class' || !e.classList) continue;
      if (e.classList.contains('sy-in') && !(r.oldValue || '').includes('sy-in')) T.soaked++;
      if (e.classList.contains('sy-new') && !(r.oldValue || '').includes('sy-new')) T.years++; } })
      .observe(document.getElementById('feed'), { attributes: true, attributeOldValue: true, attributeFilter: ['class'], subtree: true });
  });
  await startLife(page, P, 'Lale');
  await idle();
  const saved = async () => { let t = null; for (let i = 0; i < 4 && !t; i++) { t = await page.evaluate(() => askSave()); if (!t) await page.waitForTimeout(1000); } return t; };
  const loaded = async (text) => {
    await page.evaluate((x) => loadText(x), text);
    await page.waitForFunction(() => hud && hud.replay, null, { timeout: 120000 }).catch(() => {});
    await page.waitForFunction(() => hud && !hud.replay && !busy && hud.mode === 'play', null, { timeout: 1200000 });
    await page.waitForTimeout(2000);
  };
  if (SEED !== '-') {              // the same life every run: this start with the seed, loaded back
    const d = JSON.parse(await saved()); d.setup.seed = +SEED; d.inputs = [];
    await loaded(JSON.stringify(d)); await idle();
  }
  say('started', Date.now() - t0, 'ms, at age', await page.evaluate(() => hud.life && hud.life.age));
  // to the story: a moment's window is peeked away
  const toStory = async () => { if (await page.evaluate(() => !document.getElementById('evwrap').hidden && !document.getElementById('evwrap').classList.contains('peek'))) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(400); } };
  const fromStory = async () => { if (await page.evaluate(() => document.getElementById('evwrap').classList.contains('peek'))) { await page.click('#evback').catch(() => {}); await page.waitForTimeout(300); } };
  // the story's look: each year's hand, its quill, its first line (and the old hand behind it, rounded to the pixel)
  const dump = () => page.evaluate(() => [...document.getElementById('feed').children].filter((s) => s.classList.contains('yr')).map((s) => {
    const st = getComputedStyle(s), lead = s.querySelector(':scope > .lead'), q = s.querySelector(':scope > .yh > .sy-hand');
    const g = lead && lead.querySelector(':scope > .sy-ghost'), lc = lead && lead.cloneNode(true);
    if (lc) lc.querySelectorAll('.sy-ghost').forEach((x) => x.remove());
    return { age: s.dataset.age || 'pro', cls: [...s.classList].filter((c) => /^sy-(hd|lean|deep|ghosted|now|wet)$/.test(c) || c === 'closed').sort().join(' '),
      hand: ['--h-wght', '--h-opsz', '--h-soft', '--h-wonk', '--h-track', '--h-ws', '--h-lh', '--h-skew', '--h-sh', '--h-ink', '--h-wet'].map((p) => s.style.getPropertyValue(p)).join(','),
      quill: q ? q.dataset.k : '', lead: lc && !lead.hidden ? lc.innerHTML : '', font: lead ? getComputedStyle(lead).fontFamily.split(',')[0] : st.fontFamily.split(',')[0],
      ghost: g ? [...g.children].map((x) => `${x.dataset.a || ''}${x.dataset.w}@${Math.round(parseFloat(x.style.left))},${Math.round(parseFloat(x.style.top))}`).join(' ') : '' };
  }));

  if (parts.includes('look')) {
    say('part look');
    let k = 0, pushed = 0;
    for (const t1 = Date.now(); Date.now() - t1 < 25 * 60000;) {
      await idle();
      const s = await page.evaluate(() => ({ age: hud.life && hud.life.age, mode: hud.mode, cp: !!hud.cp && !document.getElementById('evwrap').hidden, rn: !!document.querySelector('#rnKeep') }));
      if (s.mode !== 'play') { fails.push('the life left play at ' + s.age); break; }
      if (s.cp && s.age >= AGE) break;
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
    await idle(); await page.waitForTimeout(1500);
    say('  at age', await page.evaluate(() => hud.life.age), '; pushed', pushed, 'times');
    await toStory();
    await page.waitForTimeout(MOTION === 'calm' ? 6500 : 3500);         // the last lines dry
    const info = await page.evaluate(() => {
      const feed = document.getElementById('feed'), L = CH.life, sy = CH.mods.story;
      const secs = [...feed.children].filter((s) => s.classList.contains('yr')), yrs = secs.filter((s) => !s.classList.contains('prologue'));
      const key = (v) => { const h = sy.hand(v); return [Math.round(h.wght / 2) * 2, Math.round(h.opsz), h.ink.join(' ')].join(','); };
      const has = (s) => [s.style.getPropertyValue('--h-wght'), s.style.getPropertyValue('--h-opsz'), s.style.getPropertyValue('--h-ink')].join(',');
      const over = yrs.filter((s) => L.ages[L.ages.length - 1] > +s.dataset.age + 1 - 1e-6);
      const wrong = over.filter((s) => has(s) !== key(sy.yearVoice(L, +s.dataset.age))).map((s) => s.dataset.age);
      const last = secs[secs.length - 1];
      const faces = [...document.fonts].filter((f) => /fraunces/i.test(f.family)).map((f) => f.status);
      const hands = new Set(yrs.map(has));
      const ghosts = yrs.filter((s) => s.classList.contains('sy-ghosted')).map((s) => s.dataset.age);
      const words = feed.querySelectorAll('.lead .sy-w').length, gl = feed.querySelectorAll('.sy-gl').length;
      const chron = document.getElementById('chron');
      return { on: feed.classList.contains('sy-on'), years: yrs.length, handed: yrs.filter((s) => s.style.getPropertyValue('--h-wght')).length,
        quills: yrs.filter((s) => s.querySelector(':scope > .yh > .sy-hand')).length, over: over.length, wrong, now: last.classList.contains('sy-now'),
        nowCount: feed.querySelectorAll('.yr.sy-now').length, hands: hands.size, ghosts, words, gl, nofr: document.documentElement.classList.contains('sy-nofr'), faces,
        font: getComputedStyle(feed.querySelector('.en:not(.ledger):not(.start)') || feed).fontFamily, wet: last.style.getPropertyValue('--h-wet'),
        soakLeft: feed.querySelectorAll('.sy-in, .sy-tx').length, soaked: __sy.soaked, newYears: __sy.years, init: feed.querySelectorAll('.lead .sy-init').length,
        leads: secs.filter((s) => { const l = s.querySelector(':scope > .lead'); return l && !l.hidden; }).length,
        sw: document.documentElement.scrollWidth, iw: innerWidth, csw: chron.scrollWidth, ccw: chron.clientWidth };
    });
    say('  ', JSON.stringify(info));
    check(info.on && info.years > 5 && info.handed === info.years, `every year has its hand (${info.handed} of ${info.years})`);
    check(info.quills === info.years, `every year has its quill (${info.quills})`);
    check(info.over > 0 && !info.wrong.length, `a year that is over has the hand of the stop it closed at (${info.over} years; wrong: ${info.wrong.join(' ') || 'none'})`);
    check(info.now && info.nowCount === 1, 'only the year being lived is marked as being lived');
    check(info.init === info.leads, `every first line opens with its gilt capital (${info.init} of ${info.leads})`);
    check(info.soakLeft === 0, 'every line has dried (no soak left, the text back as the page wrote it)');
    if (MOTION === 'off') check(info.soaked === 0 && info.newYears === 0, `motion off: nothing soaked (${info.soaked} lines, ${info.newYears} years)`);
    else check(info.soaked > 10 && info.newYears > 5, `lines soaked in on the way (${info.soaked} lines, ${info.newYears} years)`);
    check(info.sw <= info.iw && info.csw <= info.ccw + 1, `no sideways scroll (page ${info.sw} of ${info.iw}, story ${info.csw} of ${info.ccw})`);
    say(`   hands told apart: ${info.hands}; years with an old hand behind: ${info.ghosts.join(' ') || 'none'}; Fraunces ${info.nofr ? 'not loaded (Spectral)' : 'loaded'} [${info.faces.join(' ')}]; story font ${info.font}`);
    await shot('page');
    await page.locator('#chron').screenshot({ path: `${dir}/story-${tag}-story.png` });
    // still frames with motion off
    if (MOTION === 'off') {
      const a = await page.screenshot(); await page.waitForTimeout(800); const b = await page.screenshot();
      check(a.equals(b), 'motion off: two shots 0.8 s apart are equal');
    }
    // hovers: a marker (the page's mkTip), the quill, the year's head
    const hov = async (sel, want) => {
      const el = await page.$(sel); if (!el) return 'none';
      await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(150);
      if (phone) await el.tap().catch(() => {}); else await el.hover();
      await page.waitForTimeout(350);
      const t = await page.evaluate(() => { const e = document.getElementById('tip'); return e && !e.hidden ? e.innerText.replace(/\s+/g, ' ').slice(0, 160) : ''; });
      return t && (!want || t.includes(want)) ? t : 'MISS: ' + t;
    };
    const mk = await hov('#feed .yr:not(.closed) .en .mk', '');
    check(!/^MISS|^none/.test(mk), `a marker's hover (mkTip): ${mk}`);
    if (!phone) await shot('marker-tip');
    const ld = await hov('#feed .yr:not(.closed):not(.prologue) > .lead .mk', '');
    check(!/^MISS/.test(ld), `a marker on a first line keeps its hover: ${ld}`);
    const qt = await hov('#feed .yr.sy-now > .yh > .sy-hand', "The voice's hand");
    check(!/^MISS|^none/.test(qt), `the quill's hover: ${qt}`);
    if (!phone) await shot('quill-tip');
    const ht = await hov('#feed .yr.sy-now > .yh > .ag', 'Age');
    check(!/^MISS|^none/.test(ht), `the year's head keeps its hover: ${ht}`);
    await page.mouse.move(2, height - 2);
    // a fold: the newest open year closes on a click on its head, then opens again
    const fold = await page.evaluate(async () => {
      const sec = [...document.querySelectorAll('#feed .yr:not(.closed):not(.prologue)')].pop(); if (!sec) return null;
      const head = sec.querySelector(':scope > .yh'), wait = () => new Promise((r) => setTimeout(r, 120));
      head.click(); await wait(); const shut = { closed: sec.classList.contains('closed'), words: sec.querySelectorAll(':scope > .lead .sy-w').length, ghost: sec.querySelectorAll(':scope > .lead .sy-ghost').length };
      head.click(); await wait(); return { shut, open: !sec.classList.contains('closed') };
    });
    check(fold && fold.shut.closed && fold.shut.words === 0 && fold.shut.ghost === 0 && fold.open, `a year folds (one plain line) and opens again (${JSON.stringify(fold)})`);
    await fromStory();
  }

  if (parts.includes('cost')) {
    say('part cost');
    await page.evaluate(() => { const T = window.__cost = { f: [], on: true, last: CH.mods.story.cost.ms };
      const tick = () => { const m = CH.mods.story.cost.ms; T.f.push(m - T.last); T.last = m; if (T.on) requestAnimationFrame(tick); }; requestAnimationFrame(tick); });
    let lived = 0, a0 = await page.evaluate(() => hud.life.age);
    for (const t1 = Date.now(); Date.now() - t1 < 20000;) {
      const s = await page.evaluate(() => ({ cp: !!hud.cp && !busy, res: !!hud.res && !busy, busy, rn: !!document.querySelector('#rnKeep') }));
      if (s.rn) await page.click('#rnKeep').catch(() => {});
      else if (!s.busy) await page.evaluate(() => send(''));
      await page.waitForTimeout(250); lived++;
    }
    const c = await page.evaluate(() => { const T = __cost; T.on = false; const f = T.f.slice(1), s = f.slice().sort((a, b) => a - b), n = f.length;
      return { frames: n, mean: f.reduce((a, b) => a + b, 0) / Math.max(1, n), p95: s[Math.floor(n * 0.95)] || 0, max: s[n - 1] || 0, calls: CH.mods.story.cost.calls }; });
    const a1 = await page.evaluate(() => hud.life.age);
    say(`  ${c.frames} frames over 20 s while the life ran from ${a0.toFixed(2)} to ${a1.toFixed(2)}: mean ${c.mean.toFixed(3)} ms, p95 ${c.p95.toFixed(3)} ms, worst ${c.max.toFixed(2)} ms a frame`);
    check(c.frames > 100 && a1 > a0 + 1, 'the life ran and frames were drawn');
    check(c.mean <= 1 && c.p95 <= 2, `this piece's script a frame fits its share of the budget (mean ${c.mean.toFixed(3)} ms, p95 ${c.p95.toFixed(3)} ms)`);
    await idle();
  }

  if (parts.includes('load')) {
    say('part load');
    await idle(); await page.waitForTimeout(1500);
    const d1 = await dump();
    fs.writeFileSync(`${dir}/story-${tag}-dump-live.json`, JSON.stringify(d1, null, 1));
    const text = await saved();
    check(!!text, 'the life saves');
    await loaded(text);
    await page.waitForTimeout(1500);
    const d2 = await dump();
    fs.writeFileSync(`${dir}/story-${tag}-dump-loaded.json`, JSON.stringify(d2, null, 1));
    let j = 0; while (j < Math.min(d1.length, d2.length) && JSON.stringify(d1[j]) === JSON.stringify(d2[j])) j++;
    if (j < Math.max(d1.length, d2.length)) say('   first differing year', j, '\n   live  ', JSON.stringify(d1[j]).slice(0, 700), '\n   loaded', JSON.stringify(d2[j]).slice(0, 700));
    check(JSON.stringify(d1) === JSON.stringify(d2) && d1.length > 5, `the story looks the same live and after the load (${d1.length} years, ${d1.filter((x) => x.ghost).length} with an old hand)`);
    await toStory(); await shot('loaded'); await fromStory();
  }

  if (parts.includes('switch')) {
    say('part switch');
    await idle();
    if (await page.evaluate(() => !document.getElementById('evwrap').hidden)) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(300); }
    const look = () => page.evaluate(() => {
      const feed = document.getElementById('feed');
      const bad = [...feed.querySelectorAll('*')].filter((e) => [...e.classList].some((c) => c.startsWith('sy-')) || /--h-|--sy-|--g:/.test(e.getAttribute('style') || '')).length;
      const leads = [...feed.querySelectorAll('.lead[data-i]')].filter((l) => !l.hidden), plain = leads.filter((l) => l.innerHTML === rich(ITEMS[+l.dataset.i].text)).length;
      return { living: document.documentElement.dataset.living, on: feed.classList.contains('sy-on'), nofr: document.documentElement.classList.contains('sy-nofr'), bad, leads: leads.length, plain,
        text: feed.innerText, handed: feed.querySelectorAll('.yr.sy-hd').length, quills: feed.querySelectorAll('.sy-hand').length };
    });
    const s0 = await look();
    await page.click('#tMenu'); await page.waitForTimeout(300);
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(400);
    const s1 = await look();
    check(s1.living === 'off' && !s1.on && !s1.nofr && s1.bad === 0 && s1.plain === s1.leads, `off: no class, property or child of the piece left; first lines as the page wrote them (${s1.plain} of ${s1.leads})`);
    check(s1.text === s0.text, 'off: the story\'s words are the same');
    await shot('off');
    await page.click('#tPop [data-lv]'); await page.waitForTimeout(800);
    const s2 = await look();
    check(s2.living === 'on' && s2.on && s2.handed === s0.handed && s2.quills === s0.quills && s2.text === s0.text, `on again: every year handed again (${s2.handed} of ${s0.handed}), the words the same`);
    await page.keyboard.press('Escape');
  }

  if (warns.length) console.log(warns.slice(0, 10).join('\n'));
  console.log(logs.slice(0, 20).join('\n') || 'no page errors');
  const ok = !fails.length && !logs.length;
  console.log(`drive_living_story ${parts.join(',')} ${width}x${height} ${MOTION}: ${ok ? 'PASS' : 'FAIL'}${fails.length ? ' (' + fails.length + ' failed)' : ''} in ${Math.round((Date.now() - t0) / 1000)} s`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
