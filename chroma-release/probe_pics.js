const { chromium } = require(process.env.PW || 'playwright');
// v22.1 picture check (thread "What made it into v21"; read only on the game, run from a copy of its prototype/test).
// One life with a preset. It steps as a player would and records the picture behind every moment and every outcome
// (.evart img), the "A moment is waiting" button while the moment is set aside (#evback img, once a life), and every
// <img> the page shows. It writes <out>/<tag>.json and prints a one-line verdict.
//  - expect22: the picture version 22's picFor() would show for the same moment, computed in the page from the same
//    PICS (situation, then variant_of, then the first life domain PICS knows, then the tier).
//  - tarot: PICS.tarot's cards (and tarotPic(k) for k 0..7).
//  - earth mode: PASS when every recorded picture equals expect22 and there is no page error.
//  - world mode (the v22.1 bar): PASS when every moment and outcome shows the preset's own tarot card (tarotPic), no
//    other picture is placed anywhere once the life has begun (a MutationObserver sees every <img> the page puts in,
//    the everyday interlude included, which must have shown at least one), and there is no page error. Live v22 fails
//    it: its world moment cards are blank and its interlude shows Earth pictures.
//  - earth mode also fails if any tarot card is placed once the life has begun.
//  - the everyday interlude runs at pace "short" (start.js switches it off for other drivers); [pace] off skips it.
//   node test/probe_pics.js <url> <out dir> <tag> <preset> <moments> <earth|world> [W] [H] [pace]
const { startLife, idleOf, nextOf } = require('./start.js');
const fs = require('fs');
const [url, dir, tag, preset, M, mode, W, H, pace] = [process.argv[2], process.argv[3], process.argv[4], process.argv[5] || '1',
  +(process.argv[6] || 40), process.argv[7] || 'earth', +(process.argv[8] || 1280), +(process.argv[9] || 800), process.argv[10] || 'short'];
const READ = () => {
  const ex = (a) => {
    if (!a) return '';
    const d = String(a.life || '').split(',').map((x) => x.trim()).find((x) => PICS.domain[x]);
    return PICS.situation[a.sit] || PICS.situation[a.variant_of] || (d && PICS.domain[d]) || PICS.tier[a.tier] || '';
  };
  const w = document.getElementById('evwrap');
  const open = w && !w.hidden && !w.classList.contains('peek');
  const img = open ? w.querySelector('.evart img') : null;
  const res = open && !!document.querySelector('#goOn');
  const cp = open && !res && !!document.querySelector('#evLet');
  const a = cp ? (hud && hud.cp && hud.cp.art) : res ? lastArt : null;
  const L = hud && hud.life;
  return { cp, res, title: cp ? (hud.cp.title || '') : '', sit: a ? a.sit || '' : '', shown: img ? img.getAttribute('src') : '',
    expect22: a ? ex(a) : '', age: L ? Math.round(L.age * 10) / 10 : null, setting: (L && L.setting) || (hud && hud.setting) || '',
    mode: hud && hud.mode, imgs: [...document.images].filter((i) => i.offsetParent !== null).map((i) => i.getAttribute('src') || '') };
};
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  // every picture the page puts on screen once the life has begun (moment and outcome cards, the waiting button, the
  // everyday interlude, anything else), with where it went: v22.1 added the interlude to the bar (10-08)
  await page.addInitScript(() => {
    window.__rec = false; window.__pics = {};
    const where = (i) => (i.closest('.ilpic') ? 'interlude' : i.closest('.evart') ? 'card' : i.closest('#evback') ? 'waiting' : 'other');
    const note = (i) => { if (!window.__rec || !i.getAttribute) return; const s = i.getAttribute('src'); if (!s) return; const k = where(i) + '|' + s; window.__pics[k] = (window.__pics[k] || 0) + 1; };
    new MutationObserver((ms) => { for (const m of ms) {
      if (m.type === 'attributes' && m.target.tagName === 'IMG') note(m.target);
      for (const n of m.addedNodes || []) { if (n.tagName === 'IMG') note(n); else if (n.querySelectorAll) n.querySelectorAll('img').forEach(note); }
    } }).observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['src'] });
  });
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 120000 });
  const pics = await page.evaluate((p) => {
    const t = new Set(Object.values((PICS && PICS.tarot) || {}));
    for (let k = 0; k <= 7; k++) { try { const s = tarotPic(String(k)); if (s) t.add(s); } catch (_) {} }
    let h = 0; const s = JSON.stringify(PICS); for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    let own = ''; try { own = tarotPic(p) || ''; } catch (_) {}
    return { tarot: [...t], hash: h.toString(16), texture: (PICS.texture && PICS.texture.unwritten_future) || '', own };
  }, preset);
  await startLife(page, preset, 'Mira', { pace });
  await page.evaluate(() => { window.__rec = true; });
  // the drivers' idle does not wait for the interlude, which holds the next moment back until it ends
  const idle0 = idleOf(page, logs);
  const idle = async () => {
    await idle0();
    if (await page.evaluate(() => IL.on)) {
      await page.waitForFunction(() => !IL.on, null, { timeout: 120000 }).catch(() => logs.push('timeout interlude'));
      await page.waitForTimeout(800); await idle0();
    }
  };
  const next = nextOf(page, idle);
  const rows = [], seen = new Set(); let peek = null, nCp = 0;
  for (let k = 0; k < 4000 && nCp < M; k++) {
    await idle();
    const r = await page.evaluate(READ);
    r.imgs.forEach((s) => seen.add(s));
    if (r.mode && r.mode !== 'play') break;
    if (r.cp || r.res) rows.push({ kind: r.cp ? 'moment' : 'outcome', age: r.age, sit: r.sit, title: r.title, shown: r.shown, expect22: r.expect22, setting: r.setting });
    if (r.cp) {
      nCp++;
      if (nCp === 3 && !peek && await page.$('#evPeek')) {   // the moment set aside: the button that brings it back shows its picture
        await page.click('#evPeek'); await page.waitForTimeout(400);
        peek = await page.evaluate(() => { const b = document.getElementById('evback'); const i = b && b.querySelector('img'); return { shown: i ? i.getAttribute('src') : '', expect22: (() => { const a = hud && hud.cp && hud.cp.art; if (!a) return ''; const d = String(a.life || '').split(',').map((x) => x.trim()).find((x) => PICS.domain[x]); return PICS.situation[a.sit] || PICS.situation[a.variant_of] || (d && PICS.domain[d]) || PICS.tier[a.tier] || ''; })() }; });
      }
    }
    try { await next(); } catch (e) { logs.push('step failed: ' + String(e.message || e).slice(0, 160)); break; }
  }
  const placed = await page.evaluate(() => window.__pics || {});
  const tar = new Set(pics.tarot);
  const placedSrc = [...new Set(Object.keys(placed).map((k) => k.split('|').slice(1).join('|')))];
  const byWhere = {}; for (const [k, n] of Object.entries(placed)) { const w = k.split('|')[0]; byWhere[w] = (byWhere[w] || 0) + n; }
  const recorded = rows.map((r) => r.shown).concat(peek ? [peek.shown] : []).filter(Boolean);
  const shownAll = [...seen].filter(Boolean);
  const out = { tag, preset, mode, url, W, H, pace, pics_hash: pics.hash, texture: pics.texture, tarot: pics.tarot, placed, placed_by_where: byWhere,
    moments: rows.filter((r) => r.kind === 'moment').length, outcomes: rows.filter((r) => r.kind === 'outcome').length,
    settings: [...new Set(rows.map((r) => r.setting))], peek, errors: logs, rows, shown_all: shownAll };
  let pass;
  if (mode === 'earth') {
    const bad = rows.filter((r) => r.shown !== r.expect22).concat(peek && peek.shown !== peek.expect22 ? [{ kind: 'peek', ...peek }] : []);
    out.mismatch = bad; out.with_picture = recorded.length;
    out.tarot_shown = recorded.filter((s) => tar.has(s)).length;
    out.tarot_placed = placedSrc.filter((s) => tar.has(s));
    pass = bad.length === 0 && out.tarot_placed.length === 0 && logs.filter((l) => l.startsWith('pageerror')).length === 0 && rows.length > 0;
  } else {
    const nonTarot = [...new Set(recorded.concat(shownAll, placedSrc).filter((s) => !tar.has(s)))];
    out.non_tarot = nonTarot; out.tarot_used = [...new Set(recorded.filter((s) => tar.has(s)))];
    out.blank = rows.filter((r) => !r.shown).length; out.own_tarot = pics.own;
    out.other_tarot = [...new Set(out.tarot_used.concat(placedSrc.filter((s) => tar.has(s))))].filter((s) => s !== pics.own);
    out.interlude_pictures = byWhere.interlude || 0;
    // v22.1 bar (with pace off no interlude is shown, so it is not required): only the world's own tarot card, behind every moment and outcome
    pass = nonTarot.length === 0 && out.other_tarot.length === 0 && out.blank === 0 && !!pics.own && (out.interlude_pictures > 0 || pace === 'off') &&
      logs.filter((l) => l.startsWith('pageerror')).length === 0 && rows.length > 0;
  }
  out.pass = pass;
  fs.writeFileSync(`${dir}/${tag}.json`, JSON.stringify(out, null, 1));
  await page.screenshot({ path: `${dir}/${tag}-last.png` }).catch(() => {});
  console.log(`${tag}: ${pass ? 'PASS' : 'FAIL'} preset ${preset} ${mode}: ${out.moments} moments, ${out.outcomes} outcomes, settings ${out.settings.join('/')}, ` +
    `placed ${JSON.stringify(byWhere)}, ` +
    (mode === 'earth' ? `${out.mismatch.length} pictures differ from v22, ${out.with_picture} with a picture, ${out.tarot_shown} tarot, ${out.tarot_placed.length} tarot placed anywhere` :
      `${out.non_tarot.length} non-tarot pictures (${out.non_tarot.slice(0, 4).join(' ')}), tarot ${out.tarot_used.join(' ')} (own card ${out.own_tarot}, ${out.other_tarot.length} other cards), ${out.blank} blank`) +
    `, peek ${peek ? (peek.shown || 'none') : 'not reached'}, ${logs.length} log lines (${logs.filter((l) => l.startsWith('pageerror')).length} page errors), PICS ${pics.hash}`);
  await browser.close();
  process.exit(pass ? 0 : 1);
})().catch((e) => { console.log(`${tag}: ERROR ${e.message}`); process.exit(2); });
