// usage: node build_icons.js <out dir>
// Writes ink-icons.svg (one sprite: masks and symbols in <defs>) and ink-icons.json (the map, ids "ci-...") for the game.
const fs = require('fs'), path = require('path');
const { MAP } = require('./map');
const { path: shared } = require('../paths');
const { GLYPHS: ALL } = require('./all');
const byName = new Map();
for (const g of ALL) { if (byName.has(g.name)) throw new Error(`duplicate glyph ${g.name}`); byName.set(g.name, g); }
const id = (n) => { const g = byName.get(n); if (!g) throw new Error(`no glyph named ${n}`); return g.id; };
const map = Object.fromEntries(Object.entries(MAP).map(([grp, v]) => [grp,
  Object.fromEntries(Object.entries(v).map(([k, x]) => [k, Array.isArray(x) ? x.map(id) : id(x)]))]));
const used = new Set(Object.values(map).flatMap((v) => Object.values(v).flat()));
const unused = ALL.filter((g) => !used.has(g.id)).map((g) => g.name);
const out = process.argv[2] || '.';
fs.mkdirSync(out, { recursive: true });
// the engraved hatch for a colour's shadow band on the wheel (item 2): masks in the page's own units, lines 3.2 apart at 45
// degrees; fill the band with ink and give it mask="url(#ci-hatch)", or url(#ci-crosshatch) once the state word shows
const lines = (k, w) => `<pattern id="ci-${k}-lines" patternUnits="userSpaceOnUse" width="3.2" height="3.2" patternTransform="rotate(45)">${w}</pattern>`
  + `<mask id="ci-${k}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000"><rect x="-2000" y="-2000" width="4000" height="4000" fill="url(#ci-${k}-lines)"/></mask>`;
const HATCH = lines('hatch', '<rect width="1.25" height="3.2" fill="#fff"/>') + lines('crosshatch', '<rect width="1.25" height="3.2" fill="#fff"/><rect width="3.2" height="1.25" fill="#fff"/>');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${HATCH}${ALL.map((g) => g.defs).join('')}\n${ALL.map((g) => g.svg).join('\n')}\n</defs></svg>\n`;
fs.writeFileSync(path.join(out, 'ink-icons.svg'), svg);
const json = {
  about: "Chroma's own icons, drawn by the visuals thread as woodcut glyphs (chroma-art/kit/glyph). Every icon is a <symbol id=\"ci-...\"> in ink-icons.svg, viewBox 0 0 48 48, fill only, coloured by currentColor. Some carve their details with a <mask> that sits in the same sprite's <defs>, so inline the whole sprite once in the page. No third-party art, so no credits are needed. masks names the hatch masks for the shadow band on the wheel (lines in the page's own units: fill the band with ink and set mask=\"url(#ci-hatch)\").",
  credit: null,
  fallback_order: JSON.parse(fs.readFileSync(shared('art_old_icons', 'icons.json'))).fallback_order,
  map,
  masks: { shadow_band: 'ci-hatch', shadow_band_strong: 'ci-crosshatch' },
  icons: Object.fromEntries(ALL.map((g) => [g.id, { name: g.name }])),
};
fs.writeFileSync(path.join(out, 'ink-icons.json'), JSON.stringify(json, null, 1) + '\n');
console.log(`${ALL.length} glyphs, ${used.size} used, svg ${svg.length} bytes${unused.length ? `, unused: ${unused.join(', ')}` : ''}`);
