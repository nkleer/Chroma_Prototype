// usage: node grid.js <glyphs module> <out.png> [name filter regex]
// A quick check sheet: each glyph at 64 px with its name, then 28, 18 and 13 px, on parchment (left) and night (right).
const path = require('path');
const { chromium } = require('playwright');
const [mod, out, filt] = process.argv.slice(2);
let { GLYPHS } = require(path.resolve(mod));
if (filt) GLYPHS = GLYPHS.filter((g) => new RegExp(filt).test(g.name));
const sprite = `<svg width="0" height="0" style="position:absolute"><defs>${GLYPHS.map((g) => g.defs).join('')}</defs>${GLYPHS.map((g) => g.svg).join('')}</svg>`;
const cell = (g) => `<div class="c"><svg width="64" height="64"><use href="#${g.id}"/></svg><div class="sm">${[28, 18, 13].map((s) => `<svg width="${s}" height="${s}"><use href="#${g.id}"/></svg>`).join('')}</div><span>${g.name}</span></div>`;
const half = (bg, fg) => `<div class="grid" style="background:${bg};color:${fg};min-height:calc(100% - 20px)">${GLYPHS.map(cell).join('')}</div>`;
const html = `<html style="height:100%"><body style="margin:0;min-height:100%;font:11px sans-serif;display:flex;align-items:flex-start">${sprite}
<style>.grid{display:grid;grid-template-columns:repeat(10,112px);gap:8px 4px;padding:10px}.c{display:flex;flex-direction:column;align-items:center;gap:4px}
.sm{display:flex;gap:6px;align-items:center}span{text-align:center;opacity:.75;height:26px}svg{flex:none}</style>
${process.env.NIGHT ? half('#13151a', '#e8dcc0') : half('#ecdfbf', '#21170e')}</body></html>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: (10 * 116 + 20), height: 300 } });
  await p.setContent(html); await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
