// usage: NODE_PATH=/opt/node-tools/node_modules node band_preview.js <ink-icons.svg> <out.png>
// The shadow band on the wheel (implementation list item 2, chroma-ideas/shadows-mechanics.md section 6), drawn the way the
// game draws its spider graph (chroma-game/prototype/web/src/app.js, spiderSVG: same axes, radius and square-root scale),
// for review and as a reference for the game. A colour's band is the tip of its corner of the "now" polygon: the outer
// share s of the colour's spoke, from (1 - s) of its length out to the corner, so "a quarter in shadow" is the outer
// quarter of the spoke (a length, not the square-root scale, so even a small shadow is seen). It is
// filled with ink through the sprite's hatch mask: single hatch while the state word is off, cross-hatch once it shows
// (force over .5, back under .35), with a hairline where the light part ends.
const fs = require('fs');
const { chromium } = require('playwright');
const { glyph } = require('./glyph');

const SPA = [-90, -18, 54, 126, 198].map((a) => a * Math.PI / 180);
const SPR = 64, SPX = 100, SPY = 100;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const spRad = (v) => SPR * Math.sqrt(clamp(v, 0, 0.8) / 0.8);
const spAt = (i, r) => [SPX + r * Math.cos(SPA[i]), SPY + r * Math.sin(SPA[i])];
const f1 = (p) => p.map((x) => x.toFixed(1)).join(' ');

// the band of colour i: the corner of the polygon beyond the line across axis i at (1 - s) of the spoke.
// Returns the band's path and the hairline where the light part ends ('' when there is no shadow).
function shadowBand(w, s, i) {
  if (!(s[i] > 0)) return { band: '', edge: '' };
  const R = spRad(w[i]), r0 = R * (1 - clamp(s[i], 0, 1)), tip = spAt(i, R);
  const ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]);
  const cutOn = (j) => {                    // where the edge from the tip to neighbour j crosses the line
    const p = spAt(j, spRad(w[j])), pj = (p[0] - SPX) * ux + (p[1] - SPY) * uy;
    const t = clamp((R - r0) / Math.max(R - pj, 1e-6), 0, 1);
    return [tip[0] + (p[0] - tip[0]) * t, tip[1] + (p[1] - tip[1]) * t];
  };
  const a = cutOn((i + 4) % 5), b = cutOn((i + 1) % 5);
  return { band: `M${f1(a)}L${f1(tip)}L${f1(b)}Z`, edge: `M${f1(a)}L${f1(b)}` };
}

// Elif at 34 (shadows-mechanics.md section 7, six months on): White .45 with a quarter-plus in shadow (force .6, the state
// word "rigid" shows), Green .25 with a little, the rest clear. Colours W U B R G.
const LIVES = [
  { k: 'e', name: 'Elif at 34, rigid (force .6)', w: [0.45, 0.15, 0.07, 0.08, 0.25], s: [0.27, 0, 0, 0, 0.08], strong: [true, false, false, false, false] },
  { k: 'r', name: 'a Red life, a little reckless', w: [0.10, 0.12, 0.18, 0.42, 0.18], s: [0, 0.05, 0.15, 0.22, 0], strong: [false, false, false, false, false] },
];
const INK = '#21170e', PAPER = '#ecdfbf', COL = ['#f4ecd2', '#5f8fc4', '#5b4b63', '#c4553d', '#5d8a4e'];
const wheel = (L) => {
  let s = '';
  for (const v of [0.4, 0.8]) s += `<polygon points="${[0, 1, 2, 3, 4].map((i) => f1(spAt(i, spRad(v)))).join(' ')}" fill="none" stroke="${INK}" stroke-opacity=".25"/>`;
  [0, 1, 2, 3, 4].forEach((i) => { const e = spAt(i, SPR); s += `<line x1="${SPX}" y1="${SPY}" x2="${e[0].toFixed(1)}" y2="${e[1].toFixed(1)}" stroke="${INK}" stroke-opacity=".25"/>`; });
  const P = L.w.map((v, i) => spAt(i, spRad(v)));
  [0, 1, 2, 3, 4].forEach((i) => {           // the fan, each slice shading from one colour to the next, as in the game
    const a = P[i], b = P[(i + 1) % 5], g = `g${L.k}${i}`;
    s += `<linearGradient id="${g}" gradientUnits="userSpaceOnUse" x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}"><stop offset="0" stop-color="${COL[i]}"/><stop offset="1" stop-color="${COL[(i + 1) % 5]}"/></linearGradient>`;
    s += `<path d="M${SPX} ${SPY}L${f1(a)}L${f1(b)}Z" fill="url(#${g})" fill-opacity=".8"/>`;
  });
  [0, 1, 2, 3, 4].forEach((i) => {
    const { band, edge } = shadowBand(L.w, L.s, i);
    if (band) s += `<path d="${band}" fill="${INK}" fill-opacity=".85" mask="url(#${L.strong[i] ? 'ci-crosshatch' : 'ci-hatch'})"/><path d="${edge}" stroke="${INK}" stroke-width=".7" fill="none"/>`;
  });
  s += `<polygon points="${P.map(f1).join(' ')}" fill="none" stroke="${INK}" stroke-width="1.6"/>`;
  return `<figure><svg viewBox="-6 -2 212 206" width="318" height="309">${s}</svg><figcaption>${L.name}</figcaption></figure>`;
};
const [spritePath, out] = process.argv.slice(2);
const sprite = fs.readFileSync(spritePath, 'utf8');
const html = `<html><body style="margin:0;background:${PAPER};color:${INK};font:13px sans-serif">${sprite}
<div style="display:flex;gap:24px;padding:16px">${LIVES.map(wheel).join('')}</div>
<style>figure{margin:0;text-align:center}</style></body></html>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 740, height: 380 } });
  await p.setContent(html); await p.screenshot({ path: out }); await b.close();
})();
module.exports = { shadowBand };
