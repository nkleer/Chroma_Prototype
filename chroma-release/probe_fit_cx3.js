const { chromium } = require(process.env.PW || 'playwright');
// Release check for N7 (thread "What made it into v21"; read only on the game, run from a copy of its prototype/test).
// One life at a given window size (default 1280x800, preset 1 at birth, world on). At every moment:
//  - scroll: how far the card area must scroll to show every option (0 = all fit; reported, not failed);
//  - covered: options that anything placed over the page (sticky, fixed or absolute, visible) overlaps by geometry, with no
//    card hovered and again while the lowest card is hovered (the reading opens then); pointer-events do not matter here;
//  - blocked: options whose click point another element takes, after scrolling the card into view the nearest way;
//  - moved: the window or the hovered card shifting when a card is hovered (jitter);
//  - real clicks: every other moment the bottom card or Do nothing, otherwise "Let them choose", each timed; a click that
//    takes over 3 s is a stall.
// Coordinator's v22 bar (10-07 22:09 Emren): covered 0, blocked 0, moved 0, no stall, no failed click, no page error.
//   node test/probe_fit_cx3.js <url> <shots dir> [moments] [W] [H] [preset]
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, dir, M, W, H, preset] = [process.argv[2], process.argv[3], +(process.argv[4] || 60), +(process.argv[5] || 1280), +(process.argv[6] || 800), process.argv[7] || '1'];
const MEASURE = async (hovered) => {
  const ev = document.getElementById('evOpts'), wrap = document.getElementById('evwrap'), opts = [...ev.querySelectorAll('.opt')];
  const vis = (e) => { const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; const b = e.getBoundingClientRect(); return b.width > 2 && b.height > 2; };
  const overlays = [...wrap.querySelectorAll('*')].filter((e) => { const p = getComputedStyle(e).position; return (p === 'sticky' || p === 'fixed' || p === 'absolute') && vis(e); });
  const label = (o) => (o.querySelector('.ot') || o).textContent.trim().slice(0, 32);
  const lap = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  const evb = ev.getBoundingClientRect();
  const covered = [];
  for (const o of opts) {
    const b = o.getBoundingClientRect();
    const seen = { left: b.left, right: b.right, top: Math.max(b.top, evb.top), bottom: Math.min(b.bottom, evb.bottom) };   // the part not scrolled away
    if (seen.bottom - seen.top < 4) continue;
    for (const e of overlays) {
      if (e.contains(o) || o.contains(e)) continue;
      if (e.closest('.opt')) continue;   // a card's own badges
      const a = lap(seen, e.getBoundingClientRect());
      if (a > 16) { covered.push(label(o) + ' <- ' + (e.id ? '#' + e.id : '.' + [...e.classList].join('.')) + ' ' + Math.round(a) + ' px2'); break; }
    }
  }
  return { covered, scroll: Math.max(0, ev.scrollHeight - ev.clientHeight), n: opts.length };
};
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, preset, 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const out = [], clicks = []; let shots = 0, k2 = 0;
  const timedClick = async (h, what, age) => {
    const t = Date.now(); let ok = true;
    try { await h.click({ timeout: 15000 }); } catch (e) { ok = false; await page.screenshot({ path: `${dir}/clickfail-age${age}.png` }).catch(() => {}); }
    const ms = Date.now() - t; clicks.push({ age, what, ok, ms }); return ok;
  };
  for (let k = 0; k < 4000 && out.length < M; k++) {
    await idle();
    const atCp = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evOpts') && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (atCp) {
      await page.mouse.move(2, 2); await page.waitForTimeout(600);   // nothing hovered; the cards' entry animation done
      const m0 = await page.evaluate(MEASURE);
      const age = await page.evaluate(() => hud && hud.life && Math.round(hud.life.age * 10) / 10);
      // blocked: the click point of each card after a nearest scroll
      const blocked = await page.evaluate(async () => {
        const ev = document.getElementById('evOpts'), out = [], frame = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
        for (const o of ev.querySelectorAll('.opt')) { o.scrollIntoView({ block: 'nearest' }); await frame(); const b = o.getBoundingClientRect(); const e = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); if (!e || !o.contains(e)) out.push((o.querySelector('.ot') || o).textContent.trim().slice(0, 32)); }
        ev.scrollTop = 0; await frame(); return out;
      });
      // hover the lowest card that is in view: the reading opens; nothing may cover a card or move
      const low = await page.evaluateHandle(() => { const ev = document.getElementById('evOpts'), eb = ev.getBoundingClientRect(); const os = [...ev.querySelectorAll('.opt')].filter((o) => { const b = o.getBoundingClientRect(); return b.bottom <= eb.bottom + 1 && b.top >= eb.top - 1; }); return os[os.length - 1] || ev.querySelector('.opt'); });
      const pos = (o) => page.evaluate((o) => { const a = o.getBoundingClientRect(), w = document.getElementById('evwrap').querySelector('.ev') || document.getElementById('evwrap'); const b = w.getBoundingClientRect(); return [a.left, a.top, b.left, b.top, b.width, b.height].map(Math.round); }, o);
      const r0 = await pos(low), bb = await low.boundingBox();
      await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 2 }); await page.waitForTimeout(400);   // no actionability wait: a jittering card must not stop the probe
      const rs = []; for (let i = 0; i < 6; i++) { rs.push(await pos(low)); await page.waitForTimeout(150); }
      const m1 = await page.evaluate(MEASURE);
      const r1 = rs[rs.length - 1];
      const moved = rs.some((r) => r.some((v, i) => Math.abs(v - r0[i]) > (i === 1 ? 3 : 1)));   // the hovered card may lift 2 px; anything else moving is jitter
      const m = { age, n: m0.n, scroll: m0.scroll, covered: m0.covered, coveredHover: m1.covered, blocked, moved, r0, r1 };
      out.push(m);
      if ((m.covered.length || m.coveredHover.length || m.blocked.length || m.moved) && shots < 8) { shots++; await page.screenshot({ path: `${dir}/bad-${m.n}opts-age${age}.png` }); }
      // the mouse stays on the lowest card, as a player reading the cards would leave it, so a click on "Let them choose" meets any jitter
      if (m.n >= 2 && (k2++ % 2 === 0)) {   // click the bottom card or Do nothing as a player would
        const none = (k2 % 4 === 1);
        const h = (none && await page.$('#evOpts .opt.onone')) || (await page.$$('#evOpts .opt:not(.onone)')).slice(-1)[0];
        if (await timedClick(h, none ? 'Do nothing' : 'bottom card', age)) { await page.waitForTimeout(200); const p = await page.$('#pushIt'); if (p && await p.isVisible()) await p.click({ timeout: 10000 }); }
        else await page.click('#evLet', { timeout: 15000 }).catch(() => {});
      } else await timedClick(await page.$('#evLet'), 'Let them choose', age);
      continue;
    }
    if (await page.evaluate(() => typeof hud !== 'undefined' && hud && hud.mode && hud.mode !== 'play')) break;
    try { await next(); } catch (e) { logs.push('next: ' + String(e.message).slice(0, 120)); break; }
  }
  const med = (a) => (a.length ? a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)] : 0);
  const sc = out.filter((m) => m.scroll > 1), cov = out.filter((m) => m.covered.length || m.coveredHover.length), blk = out.filter((m) => m.blocked.length), mov = out.filter((m) => m.moved);
  const bad = clicks.filter((c) => !c.ok), slow = clicks.filter((c) => c.ok && c.ms > 3000);
  console.log(JSON.stringify(out)); console.log('clicks:', JSON.stringify(clicks)); console.log('logs:', JSON.stringify(logs));
  console.log(`moments ${out.length} (by options: ${JSON.stringify(out.reduce((h, m) => (h[m.n] = (h[m.n] || 0) + 1, h), {}))}); last age ${out.length ? out[out.length - 1].age : '-'}`);
  console.log(`scroll needed: ${sc.length} of ${out.length} moments (median ${med(sc.map((m) => m.scroll))} px, most ${Math.max(0, ...out.map((m) => m.scroll))} px)`);
  console.log(`covered: ${cov.length} moments (${out.filter((m) => m.coveredHover.length).length} while a card is hovered); blocked click point: ${blk.length}; window or card moved on hover: ${mov.length}`);
  console.log(`clicks: ${clicks.length - bad.length} of ${clicks.length} taken; slowest ${Math.max(0, ...clicks.map((c) => c.ms))} ms; stalls over 3 s: ${slow.length} (${slow.map((c) => c.what + ' ' + c.ms + ' ms').join(', ')})`);
  const ok = out.length > 0 && !cov.length && !blk.length && !mov.length && !bad.length && !slow.length && !logs.filter((l) => l.startsWith('pageerror')).length;
  console.log(`N7 ${W}x${H}: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
