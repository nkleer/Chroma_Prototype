// Where each event picture's lights are, read from the scene code the picture was drawn from (no repaint).
// node extract_lights.js <kit dir> <pictures dir> <out json>
//   <kit dir>       chroma-art/kit (engrave.js, scenes_*.js, deliver_pics.js; subfolders are searched too)
//   <pictures dir>  the game's pics/ folder (<slug>.webp)
//   <out json>      { "<slug>": [[x, y, size, kind, strength, colour], ...] }
// x, y: fractions of the picture (tarot and portrait cards: of the card window x 293..587, y 40..460 of the 880x500 stage);
// size: fraction of the picture's width (glow: 2r; lit shape: max(w,h)*1.8+14; beam: max(w,h));
// kind: g = P.light glow, w = lit shape of 120 px^2 or more (window, screen, door), f = smaller lit shape (candle, bulb, flame),
// b = P.beam; strength 0..1 (glow and beam: their s; lit: .6, or .6 + .4 * min(1, wash opacity / .8) with a colour); colour the light's wash colour as #rrggbb, or "" when none.
// Also writes <out dir>/missing.txt, <out dir>/summary.txt and <out dir>/lights_raw.json (every recorded light, stage px).
const fs = require('fs'), path = require('path');
const [KIT_ARG, PICS_ARG, OUT_ARG] = process.argv.slice(2);
if (!KIT_ARG || !PICS_ARG || !OUT_ARG) { console.error('usage: node extract_lights.js <kit dir> <pictures dir> <out json>'); process.exit(1); }
const KIT = path.resolve(KIT_ARG), PICS = path.resolve(PICS_ARG), OUT = path.resolve(OUT_ARG), OUTDIR = path.dirname(OUT);
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const { painter, W, H } = require(path.join(KIT, 'engrave'));

const MAX = 18, MERGE = 12, MIN_S = .05, LIT_MAX_W = 300, PART_GAP = 6, SMALL = 120;
const CARD = { x: 293, y: 40, w: 294, h: 420 };   // render_card.js CROP: the tarot art window of the 880x500 stage
const slug = (s) => s.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase();

// ---- 1. every scene in the kit, by slug (top level first, then subfolders, old/ last; first one wins)
const files = [];
const walk = (d, depth) => {
  for (const e of fs.readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) { if (!['node_modules', 'glyph'].includes(e.name)) walk(p, depth + 1); }
    else if (/^scenes.*\.js$/.test(e.name)) files.push({ p, depth, old: /(^|\/)old(\/|$)/.test(path.relative(KIT, d)) });
  }
};
walk(KIT, 0);
files.sort((a, b) => (a.old - b.old) || (a.depth - b.depth));
const INDEX = {}, dups = [], loadErr = [];
for (const f of files) {
  let m; try { m = require(f.p); } catch (e) { loadErr.push(`${path.relative(KIT, f.p)}: ${e.message.split('\n')[0]}`); continue; }
  if (!m || !m.SCENES) continue;
  for (const [k, fn] of Object.entries(m.SCENES)) {
    if (typeof fn !== 'function') { loadErr.push(`${path.relative(KIT, f.p)}: "${k}" is not a function scene (older painter format)`); continue; }
    const s = slug(k);
    if (INDEX[s]) { dups.push(`${s}: ${INDEX[s].file} wins over ${path.relative(KIT, f.p)}`); continue; }
    INDEX[s] = { file: path.relative(KIT, f.p), key: k, fn };
  }
}

// ---- 2. the game's tarot files: menu key -> card scene, read from deliver_pics.js (const TAROT = { 1: 'card-1', ... })
let TAROT = {};
try {
  const src = fs.readFileSync(path.join(KIT, 'deliver_pics.js'), 'utf8');
  const m = src.match(/const TAROT\s*=\s*(\{[^}]*\})/);
  if (m) for (const [, k, v] of m[1].matchAll(/['"]?(\w+)['"]?\s*:\s*['"]([^'"]+)['"]/g)) TAROT[`tarot-${k}`] = v;
} catch (e) { /* no deliver_pics.js: no tarot mapping */ }

// ---- 3. run each picture's scene with a recording painter
const pics = fs.readdirSync(PICS).filter((f) => f.endsWith('.webp')).map((f) => f.slice(0, -5)).sort();
const jobs = [], missing = [];
for (const name of pics) {
  const sceneSlug = TAROT[name] || name;
  const sc = INDEX[sceneSlug];
  if (!sc) { missing.push(name); continue; }
  jobs.push({ name, card: !!TAROT[name] || name.startsWith('portrait-'), sc, rec: [] });
}
const hex = (c) => {
  if (typeof c !== 'string') return '';
  let s = c.trim().toLowerCase();
  if (/^#[0-9a-f]{3}$/.test(s)) s = '#' + [...s.slice(1)].map((ch) => ch + ch).join('');
  if (/^#[0-9a-f]{6}([0-9a-f]{2})?$/.test(s)) return s.slice(0, 7);
  const m = s.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  return m ? '#' + m.slice(1, 4).map((v) => (+v).toString(16).padStart(2, '0')).join('') : '';
};
const runErr = [];
for (const j of jobs) {
  const P = painter(); const clips = [];
  const o = { light: P.light, lit: P.lit, beam: P.beam, clip: P.clip };
  // the painter's own defaults: light(x, y, r, color, o = .4, s = 1), lit(d, color = null, o = .4, line = 1), beam(d, color = null, s = .85, o = .18)
  P.light = (x, y, r, color, op = .4, s = 1) => { j.rec.push({ t: 'g', x, y, r, s: s ?? 1, c: hex(color), clips: [...clips] }); return o.light(x, y, r, color, op, s); };
  P.lit = (d, color = null, op = .4, line = 1) => { j.rec.push({ t: 'lit', d, s: color ? .6 + .4 * Math.min(1, op / .8) : .6, c: hex(color), clips: [...clips] }); return o.lit(d, color, op, line); };
  P.beam = (d, color = null, s = .85, op = .18) => { j.rec.push({ t: 'b', d, s: s ?? .85, c: hex(color), clips: [...clips] }); return o.beam(d, color, s, op); };
  // lights made inside P.clip are clipped by the painter: remember the clip shapes
  P.clip = (d, fn) => o.clip(d, () => { clips.push(d); try { fn(); } finally { clips.pop(); } });
  try { j.sc.fn(P); } catch (e) { runErr.push(`${j.name}: ${e.message}`); }
}

// ---- 4. bounding boxes of every path involved (lit parts, beams, clips), measured by the browser
const pathList = [], pathId = new Map();
const need = (d) => { if (!pathId.has(d)) { pathId.set(d, pathList.length); pathList.push(d); } return pathId.get(d); };
for (const j of jobs) for (const l of j.rec) {
  l.clipIds = l.clips.map(need);
  if (l.t === 'lit') l.partIds = l.d.split(/(?=M)/).filter((p) => p.trim()).map(need);   // the kit's lit paths start every subpath with an absolute M
  if (l.t === 'b') l.id = need(l.d);
}

(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  const boxes = [];
  for (let i = 0; i < pathList.length; i += 2000) {
    boxes.push(...await pg.evaluate((ps) => {
      const ns = 'http://www.w3.org/2000/svg'; const sv = document.createElementNS(ns, 'svg'); document.body.appendChild(sv);
      return ps.map((d) => { const e = document.createElementNS(ns, 'path'); e.setAttribute('d', d); sv.appendChild(e);
        let bb; try { bb = e.getBBox(); } catch (er) { bb = { x: 0, y: 0, width: 0, height: 0 }; } e.remove(); return [bb.x, bb.y, bb.width, bb.height]; });
    }, pathList.slice(i, i + 2000)));
  }
  await b.close();

  const inter = (a, c) => { const x0 = Math.max(a[0], c[0]), y0 = Math.max(a[1], c[1]), x1 = Math.min(a[0] + a[2], c[0] + c[2]), y1 = Math.min(a[1] + a[3], c[1] + c[3]);
    return x1 > x0 && y1 > y0 ? [x0, y0, x1 - x0, y1 - y0] : null; };
  const clipBox = (l) => l.clipIds.reduce((acc, id) => acc && inter(acc, boxes[id]), [-1e5, -1e5, 2e5, 2e5]);

  const out = {}, raw = {}, stats = [];
  let total = 0;
  for (const j of jobs) {
    const F = j.card ? CARD : { x: 0, y: 0, w: W, h: H };
    const L = [];   // stage px: { k, x, y, w, h, size, s, c }
    for (const l of j.rec) {
      const cb = clipBox(l);
      if (!cb) continue;   // clipped away entirely
      if (l.t === 'g') {
        if (!(l.r > 2)) continue;
        let bx = [l.x - l.r, l.y - l.r, 2 * l.r, 2 * l.r];
        if (l.clips.length) { const ib = inter(bx, cb); if (!ib) continue; bx = ib; }
        const x = Math.min(Math.max(l.x, cb[0]), cb[0] + cb[2]), y = Math.min(Math.max(l.y, cb[1]), cb[1] + cb[3]);
        const size = l.clips.length ? Math.min(2 * l.r, Math.max(bx[2], bx[3])) : 2 * l.r;
        L.push({ k: 'g', x, y, w: size, h: size, size, s: l.s, c: l.c });
      } else if (l.t === 'b') {
        let bx = boxes[l.id]; if (l.clips.length) bx = inter(bx, cb);
        if (!bx || bx[2] * bx[3] < 4) continue;
        L.push({ k: 'b', x: bx[0] + bx[2] / 2, y: bx[1] + bx[3] / 2, w: bx[2], h: bx[3], size: Math.max(bx[2], bx[3]), s: l.s, c: l.c });
      } else {
        // a lit path may hold several openings (a row of windows, a string of bulbs): parts closer than PART_GAP px stay one
        // light (the panes of one window), parts further apart become lights of their own
        const parts = l.partIds.map((id) => boxes[id]).map((bx) => (l.clips.length ? inter(bx, cb) : bx)).filter((bx) => bx && bx[2] * bx[3] >= 2);
        const grp = parts.map((bx, i) => i);
        const root = (i) => (grp[i] === i ? i : (grp[i] = root(grp[i])));
        for (let a = 0; a < parts.length; a++) for (let c = a + 1; c < parts.length; c++) {
          const A = parts[a], C = parts[c];
          if (A[0] - PART_GAP <= C[0] + C[2] && C[0] - PART_GAP <= A[0] + A[2] && A[1] - PART_GAP <= C[1] + C[3] && C[1] - PART_GAP <= A[1] + A[3]) grp[root(a)] = root(c);
        }
        const groups = {};
        parts.forEach((bx, i) => { const g = groups[root(i)] = groups[root(i)] || { n: 0, area: 0, x0: 1e9, y0: 1e9, x1: -1e9, y1: -1e9 };
          g.n++; g.area += bx[2] * bx[3]; g.x0 = Math.min(g.x0, bx[0]); g.y0 = Math.min(g.y0, bx[1]); g.x1 = Math.max(g.x1, bx[0] + bx[2]); g.y1 = Math.max(g.y1, bx[1] + bx[3]); });
        for (const g of Object.values(groups)) {
          const w = g.x1 - g.x0, h = g.y1 - g.y0;
          if (w > LIT_MAX_W) continue;                          // a big lit plane (sky, wall), not a light
          if (g.n >= 4 && w * h > 40000) continue;              // many touching parts spread over a big box
          if (g.area < 4) continue;
          L.push({ k: g.area >= SMALL ? 'w' : 'f', x: g.x0 + w / 2, y: g.y0 + h / 2, w, h, size: Math.max(w, h) * 1.8 + 14, s: l.s, c: l.c, area: g.area });
        }
      }
    }
    raw[j.name] = L.map((l) => ({ ...l, x: +l.x.toFixed(1), y: +l.y.toFixed(1), w: +l.w.toFixed(1), h: +l.h.toFixed(1), size: +l.size.toFixed(1) }));
    // reduce: visible strength, inside the picture (or card window), not whole-picture lifts
    let K = L.filter((l) => l.s >= MIN_S && l.x >= F.x && l.x <= F.x + F.w && l.y >= F.y && l.y <= F.y + F.h && !(l.k === 'g' && l.size > W));
    // merge lights of one kind closer than MERGE px: the bigger one stays (with the stronger of the two strengths)
    K.sort((a, b) => b.size - a.size);
    const kept = [];
    for (const l of K) {
      const near = kept.find((m) => m.k === l.k && Math.hypot(m.x - l.x, m.y - l.y) < MERGE);
      if (near) { near.s = Math.max(near.s, l.s); if (!near.c) near.c = l.c; } else kept.push({ ...l });
    }
    // the MAX kept are the most visible (strength x the square root of the glow's size in px, so a phone's glow outranks one
    // window dot of a distant skyline); they are then listed strongest first
    // among near-equal ones (a row of candles, a skyline's windows) the next pick is the one furthest from those already
    // picked, so a capped row keeps lights spread along it instead of its first few
    const score = (l) => l.s * Math.sqrt(l.size), pool = [...kept], fin = [];
    while (fin.length < MAX && pool.length) {
      const top = Math.max(...pool.map(score));
      let bi = -1, bd = -1;
      pool.forEach((l, i) => { if (score(l) < top * .97) return;
        const d = Math.min(1e9, ...fin.filter((m) => m.k === l.k).map((m) => Math.hypot(m.x - l.x, m.y - l.y)));
        if (d > bd) { bd = d; bi = i; } });
      fin.push(pool.splice(bi, 1)[0]);
    }
    fin.sort((a, b) => (b.s - a.s) || (b.size - a.size));
    out[j.name] = fin.map((l) => [+((l.x - F.x) / F.w).toFixed(3), +((l.y - F.y) / F.h).toFixed(3), +(l.size / F.w).toFixed(3), l.k, +Math.min(1, l.s).toFixed(2), l.c]);
    total += fin.length; stats.push([fin.length, j.name, L.length]);
  }

  // compact JSON: one picture per line
  const body = '{\n' + Object.entries(out).map(([k, v]) => `${JSON.stringify(k)}:${JSON.stringify(v)}`).join(',\n') + '\n}\n';
  fs.mkdirSync(OUTDIR, { recursive: true });
  fs.writeFileSync(OUT, body);
  fs.writeFileSync(path.join(OUTDIR, 'lights_raw.json'), JSON.stringify(raw));
  fs.writeFileSync(path.join(OUTDIR, 'missing.txt'),
    `# pictures in ${PICS} with no scene in ${KIT} (searched scenes*.js in the kit and its subfolders, old/ included)\n` +
    missing.map((m) => m + (m === 'unwritten-fabric' ? '\t(texture strip drawn by fabric.js, not a painter scene: no P.light/P.lit/P.beam)' : '')).join('\n') + '\n' +
    (loadErr.length ? '\n# scene files that could not be used\n' + loadErr.join('\n') + '\n' : '') +
    (runErr.length ? '\n# scenes that threw while recording\n' + runErr.join('\n') + '\n' : '') +
    (dups.length ? '\n# keys defined twice\n' + dups.join('\n') + '\n' : ''));
  stats.sort((a, b) => b[0] - a[0] || b[2] - a[2]);
  const kinds = {}; for (const v of Object.values(out)) for (const l of v) kinds[l[3]] = (kinds[l[3]] || 0) + 1;
  const summary = [
    `pictures in ${PICS}: ${pics.length}`,
    `pictures covered (scene found and run): ${jobs.length} (${jobs.filter((j) => j.card).length} tarot cards via deliver_pics.js TAROT: ${Object.entries(TAROT).map(([k, v]) => k + '=' + v).join(', ')})`,
    `pictures with at least one light: ${Object.values(out).filter((v) => v.length).length}; with none: ${Object.values(out).filter((v) => !v.length).length} (${Object.entries(out).filter(([, v]) => !v.length).map(([k]) => k).join(', ')})`,
    `pictures with no scene: ${missing.length} (see missing.txt)`,
    `lights recorded before reduction: ${stats.reduce((a, s) => a + s[2], 0)}; kept: ${total} (${Object.entries(kinds).map(([k, n]) => k + ' ' + n).join(', ')})`,
    `pictures capped at ${MAX}: ${stats.filter((s) => s[0] >= MAX).length}`,
    `lights.json: ${Buffer.byteLength(body)} bytes`,
    'most lights:', ...stats.slice(0, 5).map((s) => `  ${s[1]}: ${s[0]} kept (${s[2]} recorded)`),
  ].join('\n') + '\n';
  fs.writeFileSync(path.join(OUTDIR, 'summary.txt'), summary);
  process.stdout.write(summary);
  if (runErr.length) console.error('scene errors:', runErr.length);
})();
