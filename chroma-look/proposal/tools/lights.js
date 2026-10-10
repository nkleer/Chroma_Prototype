// Records where a picture's lights are, from the scene code the picture is drawn from (no repaint).
// node lights.js <scenes file> <name> [<name>...]  -> JSON on stdout: { name: [{x,y,r,s,kind}] }
const KIT = '/mnt/project-files/chroma-art/kit/';
const { painter } = require(KIT + 'engrave');
const file = process.argv[2]; const { SCENES } = require(KIT + file);
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); const out = {};
  for (const n of process.argv.slice(3)) {
    const P = painter(); const rec = []; const paths = [];
    const wrap = (k, f) => { const o = P[k]; P[k] = (...a) => { f(...a); return o(...a); }; };
    wrap('light', (x, y, r, color, o, s) => rec.push({ x, y, r, s: s ?? .5, kind: 'glow' }));
    wrap('lit', (d) => paths.push({ d, kind: 'lit' }));
    wrap('beam', (d, c, s) => paths.push({ d, kind: 'beam', s }));
    SCENES[n](P);
    const boxes = await pg.evaluate((ps) => { const ns = 'http://www.w3.org/2000/svg'; const sv = document.createElementNS(ns, 'svg'); document.body.appendChild(sv);
      return ps.map((p) => { const e = document.createElementNS(ns, 'path'); e.setAttribute('d', p.d); sv.appendChild(e); const bb = e.getBBox(); return [bb.x, bb.y, bb.width, bb.height]; }); }, paths);
    paths.forEach((p, i) => { const [x, y, w, h] = boxes[i]; if (w * h < 4) return;
      // a lit shape made of many small parts (a string of bulbs) is already covered by its glows
      if (p.kind === 'lit' && (w > 300)) return;
      rec.push({ x: x + w / 2, y: y + h / 2, w, h, s: p.s ?? .6, kind: p.kind }); });
    out[n] = rec.map((l) => Object.fromEntries(Object.entries(l).map(([k, v]) => [k, typeof v === 'number' ? Math.round(v * 10) / 10 : v])));
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
