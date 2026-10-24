const { chromium } = require(process.env.PW || 'playwright');
// Geometric copy (game thread, 10-07): the hit tests count the strip even though it lets the pointer through, and each option is
// also focused to open the reading, which must not overlap it. Otherwise the same as the release thread's probe_fit_cx3.js.
// Release check for N7 (thread "What made it into v21"; read only on the game, run from a copy of its prototype/test).
// One life at a given window size (default 1280x800, preset 1 at birth, world on). At every moment:
//  - scroll: how far the card area must scroll to show every option (0 = all fit);
//  - covered: options the reading strip (or anything else) covers at the point a click lands, after scrolling the card
//    into view the nearest way; unreachable: options covered at every scroll position tried (nearest, center, the end).
//  - every other moment it really clicks the bottom option (alternately the last card and Do nothing) as a player would,
//    and records a click the page refuses.
// Coordinator's v22 bar (10-07 21:29 Emren): covered 0, unreachable 0, no failed click; scrolling is reported, not failed.
//   node test/probe_fit_cx3.js <url> <shots dir> [moments] [W] [H] [preset]
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, dir, M, W, H, preset] = [process.argv[2], process.argv[3], +(process.argv[4] || 60), +(process.argv[5] || 1280), +(process.argv[6] || 800), process.argv[7] || '1'];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, preset, 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const out = [], clicks = []; let shots = 0, k2 = 0;
  for (let k = 0; k < 4000 && out.length < M; k++) {
    await idle();
    const atCp = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evOpts') && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (atCp) {
      await page.waitForTimeout(500);   // the cards' entry animation
      await page.mouse.move(1, 1);      // a mouse left resting on a card (after the last click) would close a focused card's reading as the column scrolls under it
      const m = await page.evaluate(async () => {
        const force = document.createElement('style'); force.textContent = '.dstrip { pointer-events: auto !important; }'; document.body.appendChild(force);   // geometric: the strip counts as covering even though it lets clicks through
        const ev = document.getElementById('evOpts'), opts = [...ev.querySelectorAll('.opt')];
        const frame = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
        const hit = (o) => { const b = o.getBoundingClientRect(); const xs = [b.left + b.width / 2]; const ys = [b.top + Math.min(6, b.height / 2), b.top + b.height / 2, b.bottom - Math.min(6, b.height / 2)];
          return ys.every((y) => xs.every((x) => { const e = document.elementFromPoint(x, y); return !!e && o.contains(e); })); };
        const res = { age: hud && hud.life && Math.round(hud.life.age * 10) / 10, n: opts.length, scroll: Math.max(0, ev.scrollHeight - ev.clientHeight), covered: [], unreachable: [] };
        for (const o of opts) {
          const label = (o.querySelector('.ot') || o).textContent.trim().slice(0, 32);
          ev.scrollTop = 0; o.scrollIntoView({ block: 'nearest' }); await frame();
          if (hit(o)) continue;
          res.covered.push(label);
          let ok = false;
          for (const how of ['center', 'end']) { if (how === 'end') ev.scrollTop = ev.scrollHeight; else o.scrollIntoView({ block: 'center' }); await frame(); if (hit(o)) { ok = true; break; } }
          if (!ok) res.unreachable.push(label);
        }
        // the strip opened by focus (as by hover): does it cover the option it reads, after the nearest scroll?
        res.coveredOpen = [];
        const strip = document.getElementById('evStrip');
        if (strip) for (const o of opts) {
          ev.scrollTop = 0; o.scrollIntoView({ block: 'nearest' }); o.focus({ preventScroll: true }); await frame();
          const b = o.getBoundingClientRect(), s = strip.getBoundingClientRect();
          const vis = getComputedStyle(strip).display !== 'none' && s.height > 0, oy = Math.min(b.bottom, s.bottom) - Math.max(b.top, s.top), ox = Math.min(b.right, s.right) - Math.max(b.left, s.left);
          if (strip.classList.contains('idle')) res.focusNoReading = (res.focusNoReading || 0) + 1;   // focus must open the reading as hover does
          if (vis && oy > 0.5 && ox > 0.5) res.coveredOpen.push([(o.querySelector('.ot') || o).textContent.trim().slice(0, 24), Math.round(oy), Math.round(s.height)]);
          o.blur(); await frame();
        }
        force.remove(); ev.scrollTop = 0; await frame();
        return res;
      });
      out.push(m);
      if ((m.covered.length || m.unreachable.length) && shots < 6) { shots++; await page.screenshot({ path: `${dir}/cover-${m.n}opts-age${m.age}.png` }); }
      if (m.n >= 2 && (k2++ % 2 === 0)) {   // click the bottom option as a player would
        const none = (k2 % 4 === 1);
        const sel = none ? '#evOpts .opt.onone' : '#evOpts .ogrid:last-of-type .opt:last-child';
        const h = (await page.$(sel)) || (await page.$$('#evOpts .opt')).slice(-1)[0];
        const label = h ? (await h.evaluate((o) => (o.querySelector('.ot') || o).textContent.trim().slice(0, 32))) : '(none found)';
        let ok = true;
        try { await h.click({ timeout: 10000 }); await page.waitForTimeout(200); const p = await page.$('#pushIt'); if (p && await p.isVisible()) await p.click({ timeout: 10000 }); }
        catch (e) { ok = false; await page.screenshot({ path: `${dir}/clickfail-age${m.age}.png` }).catch(() => {}); }
        clicks.push({ age: m.age, label, ok });
        if (!ok) { try { await page.click('#evLet', { timeout: 10000 }); } catch (_) {} }
        continue;
      }
    }
    if (await page.evaluate(() => typeof hud !== 'undefined' && hud && hud.mode && hud.mode !== 'play')) break;
    try { await next(); } catch (e) { logs.push('next: ' + String(e.message).slice(0, 120)); break; }
  }
  const scroll = out.filter((m) => m.scroll > 1), cov = out.filter((m) => m.covered.length), unr = out.filter((m) => m.unreachable.length), bad = clicks.filter((c) => !c.ok);
  const med = (a) => (a.length ? a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)] : 0);
  console.log(JSON.stringify(out)); console.log('clicks:', JSON.stringify(clicks)); console.log('logs:', JSON.stringify(logs));
  console.log(`moments ${out.length} (by options: ${JSON.stringify(out.reduce((h, m) => (h[m.n] = (h[m.n] || 0) + 1, h), {}))}); last age ${out.length ? out[out.length - 1].age : '-'}`);
  console.log(`scroll needed: ${scroll.length} of ${out.length} moments (median ${med(scroll.map((m) => m.scroll))} px, most ${Math.max(0, ...out.map((m) => m.scroll))} px)`);
  console.log(`strip opened over the option it reads: ${out.filter((m) => (m.coveredOpen || []).length).length} moments, ${out.reduce((a, m) => a + (m.coveredOpen || []).length, 0)} options; worst ${Math.max(0, ...out.flatMap((m) => (m.coveredOpen || []).map((c) => c[1])))} px`);
  console.log(`focus that left the reading closed: ${out.reduce((a, m) => a + (m.focusNoReading || 0), 0)}`);
  console.log(`covered at the nearest scroll: ${cov.length} moments; unreachable: ${unr.length}; bottom-option clicks ${clicks.length - bad.length} of ${clicks.length} ok`);
  const ok = out.length > 0 && !cov.length && !unr.length && !bad.length && !logs.filter((l) => l.startsWith('pageerror') || l.startsWith('next:')).length
    && !out.some((m) => (m.coveredOpen || []).length || m.focusNoReading);   // geometric bar: no overlap with the open reading, focus reads too, no stall
  console.log(`N7 strip (geometric) ${W}x${H}: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
