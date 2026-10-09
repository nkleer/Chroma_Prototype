// Renders a review sheet: each new glyph beside the current game-icon, at 64, 28, 18 and 13 px, on parchment and night.
const fs = require('fs');
const { path: shared } = require('../paths');
const { GLYPHS } = require('./glyphs');
const GI = JSON.parse(fs.readFileSync(shared('art_old_icons', 'icons.json'))).map;
const giSvg = fs.readFileSync(shared('art_old_icons', 'icons.svg'), 'utf8');
const cur = (n) => { const [k, v] = n.split(' '); const key = n.slice(k.length + 1); return (GI[k] || {})[key]; };
const sprite = `<svg width="0" height="0" style="position:absolute"><defs>${GLYPHS.map((g) => g.defs).join('')}</defs>${GLYPHS.map((g) => g.svg).join('')}</svg>` + giSvg;
const row = (g) => { const c = cur(g.name); const sizes = [64, 28, 18, 13];
  return `<div class="row"><div class="lab">${g.name}</div>${sizes.map((s) => `<svg width="${s}" height="${s}"><use href="#${g.id}"/></svg>`).join('')}<span class="vs">${c ? sizes.slice(1).map((s) => `<svg class="gx" width="${s}" height="${s}"><use href="#${c}"/></svg>`).join('') : ''}</span></div>`; };
const half = (bg, fg) => `<div class="col" style="background:${bg};color:${fg}">${GLYPHS.map(row).join('')}</div>`;
const html = `<html><body style="margin:0;font:12px sans-serif">${sprite}<style>.col{display:inline-block;vertical-align:top;padding:10px}.row{display:flex;align-items:center;gap:10px;height:70px}.lab{width:110px}.vs{display:flex;gap:8px;align-items:center;margin-left:14px;opacity:.6}.gx{fill:currentColor}svg{flex:none}</style>
${half('#ecdfbf', '#21170e')}${half('#13151a', '#e8dcc0')}</body></html>`;
fs.writeFileSync(__dirname + '/sheet.html', html);
(async () => {
  const { chromium } = require('playwright')   // NODE_PATH=/opt/node-tools/node_modules;
})().catch(() => {});
