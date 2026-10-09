// Writes the full icon review page: every key the game maps, our glyph beside the game-icons picture it replaces.
const fs = require('fs');
const { path: shared } = require('../paths');
const { MAP } = require('./map');
const FILES = ['glyphs', 'glyphs_tags', 'glyphs_needs', 'glyphs_acts', 'glyphs_opts_a', 'glyphs_opts_b', 'glyphs_o1', 'glyphs_o2', 'glyphs_o3', 'glyphs_o4', 'glyphs_o5', 'glyphs_o6', 'glyphs_o7', 'glyphs_p1', 'glyphs_p2', 'glyphs_w42'];
const ALL = FILES.flatMap((f) => require(`./${f}`).GLYPHS);
const byName = new Map(ALL.map((g) => [g.name, g]));
const GI = JSON.parse(fs.readFileSync(shared('art_old_icons', 'icons.json'))).map;
const giSvg = fs.readFileSync(shared('art_old_icons', 'icons.svg'), 'utf8');
const giSym = (id) => (giSvg.match(new RegExp(`<symbol id="${id}"[^>]*>[\\s\\S]*?</symbol>`)) || [''])[0];
const usedGi = [...new Set(Object.values(GI).flatMap((v) => Object.values(v).flat()))];
const sprite = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${ALL.map((g) => g.defs).join('')}</defs>${ALL.map((g) => g.svg).join('')}${usedGi.map(giSym).join('')}</svg>`;
const use = (id, cls = '') => `<svg class="g ${cls}" aria-hidden="true"><use href="#${id}"/></svg>`;
const cap = (s) => s.replace(/^./, (c) => c.toUpperCase());
const COLOR = { W: 'White', U: 'Blue', B: 'Black', R: 'Red', G: 'Green' };
const MEAN = { 'color W': 'a column: order, law, the common good', 'color U': 'an open eye: seeing, knowing', 'color B': 'a crown: power, ambition',
  'color R': 'a tall flame: passion, action', 'color G': 'a seedling: growth, nature', 'meter content': 'the sun up over the horizon',
  'meter peace': 'a moon over still water', 'meter strain': 'a spring pressed flat under a weight', 'meter wanting': 'a star just out of a ladder\'s reach' };
const KEYLABEL = { 'commit:career': 'takes on a career', 'commit:partner': 'commits to a partner', 'commit:children': 'has children',
  'commit:community': 'joins a community', 'commit:faith': 'takes up a faith', 'pay:money': 'pays money', 'win:money': 'gains money', 'win:ties': 'wins someone over' };
const card = (grp, key, name) => {
  const g = byName.get(name), now = (GI[grp] || {})[key];
  const label = grp === 'color' ? COLOR[key] : KEYLABEL[key] || cap(key.replace(/_/g, ' ').replace(/^ai /, 'AI '));
  return `<figure class="card"><div class="big">${use(g.id)}</div><figcaption><b>${label}</b>${MEAN[name] ? `<span class="mean">${MEAN[name]}</span>` : ''}<span class="sizes">${use(g.id, 's28')}${use(g.id, 's18')}${use(g.id, 's13')}</span>${now ? `<span class="now">now ${use(now, 's18 gi')}</span>` : ''}</figcaption></figure>`;
};
const group = (title, note, grps, five) => `<section id="${title.toLowerCase().replace(/[^a-z]+/g, '-')}"><h2>${title}</h2><p class="note">${note}</p><div class="cards${five ? ' five' : ''}">${grps.flatMap((grp) => Object.entries(MAP[grp]).map(([k, n]) => card(grp, k, n))).join('')}</div></section>`;
const PLATE = { W: '#d9cfa8', U: '#4f7fb8', B: '#6b5a73', R: '#c0533a', G: '#5f8a4e' };
// every option of the audited batch, browsable one moment at a time
// usage: node page2.js <moments.json> [out.html]; moments.json is what `python3 -B optmap3/load.py <Library folder>/ <moments.json>`
// writes (the live Library is paths.py's library_live); every option becomes one row
const ROWS = JSON.parse(fs.readFileSync(process.argv[2])).flatMap((m) => m.options.map((o) => ({ sit: m.name, tier: m.tier, mod: m.mod, k: o.k, text: o.text, colors: o.colors })));
const TIERS = [['life event', 'life events'], ['everyday', 'everyday moments'], ['inner', 'inner moments'], ['echo', 'echoes']];
const MODS = [['earth', 'Earth'], ['earth_science', 'Science'], ['earth_politics', 'Politics'], ['earth_stage', 'Stage and Screen']];
const OPT = {};
for (const r of ROWS) (OPT[r.sit] = OPT[r.sit] || { t: r.tier, m: r.mod, o: [] }).o.push([cap(r.text), r.colors[0], byName.get(MAP.option[r.sit][r.k]).id]);
const counts = {}; for (const v of Object.values(MAP.option)) for (const n of v) counts[n] = (counts[n] || 0) + 1;
const optNames = new Set(['o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'p1', 'p2'].flatMap((f) => require(`./glyphs_${f}`).GLYPHS.map((g) => g.name)));
const pickOpts = MODS.flatMap(([md, ml]) => TIERS.map(([t, l]) => [md, t, `${ml}: ${l}`])).map(([md, t, l]) => `<optgroup label="${l}">${Object.keys(OPT).filter((k) => OPT[k].t === t && OPT[k].m === md).sort().map((k) => `<option value="${k.replace(/"/g, '&quot;')}">${cap(k)}</option>`).join('')}</optgroup>`).join('');
const optSec = `<section id="options"><h2>Every option, moment by moment</h2>
<p class="note">All ${Object.keys(OPT).length} moments of the live Library (Earth and the Science, Politics and Stage and Screen packs) and their ${ROWS.length.toLocaleString('en')} options, each with its own icon, on a plate tinted by the option's colour as the event window shows them. Pick a moment, or try a random one.</p>
<div class="picker"><label for="pick">Moment</label><select id="pick">${pickOpts}</select><button type="button" id="rnd">Random moment</button></div>
<div class="moment" id="moment"><h3 id="mname"></h3><div class="rows" id="mrows"></div></div></section>
<section id="option-glyphs"><h2>The option glyphs</h2><p class="note">The ${optNames.size} glyphs drawn for options, with how many of the ${ROWS.length.toLocaleString('en')} options use each. The rest of the options use glyphs from the sections above.</p>
<div class="tiles">${ALL.filter((g) => optNames.has(g.name)).sort((x, y) => (counts[y.name] || 0) - (counts[x.name] || 0)).map((g) => `<figure class="tile">${use(g.id, 's36')}<figcaption>${cap(g.name.replace(/-/g, ' '))}<small>${counts[g.name] || 0}</small></figcaption></figure>`).join('')}</div></section>
<script>
const OPT = ${JSON.stringify(OPT)};
const PLATE = ${JSON.stringify(PLATE)};
const pick = document.getElementById('pick'), rows = document.getElementById('mrows'), mname = document.getElementById('mname');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
function show(k) {
  const m = OPT[k]; if (!m) return; pick.value = k;
  mname.textContent = k.charAt(0).toUpperCase() + k.slice(1);
  rows.innerHTML = m.o.map(([t, c, id]) => '<div class="opt"><span class="plate" style="--pc:' + PLATE[c] + '"><svg class="g s21" aria-hidden="true"><use href="#' + id + '"/></svg></span><span class="ot">' + esc(t) + '</span></div>').join('');
}
pick.addEventListener('change', () => show(pick.value));
document.getElementById('rnd').addEventListener('click', () => { const ks = Object.keys(OPT); show(ks[Math.floor(Math.random() * ks.length)]); });
show('a narrow escape');
</script>`;
const tpl = fs.readFileSync(__dirname + '/page2.tpl.html', 'utf8');
const body = group('The five colours', 'Our own signs for the colour pie, drawn for Chroma. They are deliberately not Magic\'s mana symbols.', ['color'], true)
  + group('The four meters', 'Content, peace, strain and wanting, as they show in the status panel.', ['meter'])
  + group('Life domains', 'The areas of life the game uses for the feed, the timeline and the picture fallbacks; the newer ones reuse a glyph from elsewhere in the set.', ['domain'])
  + group('The life story', 'Marks beside lines of the story and on the timeline, and the kind of moment in the event window.', ['tag', 'tier'])
  + group('Means, needs and goals', 'The five means, the five needs and the three kinds of goal in the status panel, and the commitments a life takes on.', ['res', 'need', 'goal', 'kind'])
  + group('People and worlds', 'The roles of the people around the character, and the three world settings.', ['role', 'setting'])
  + group('The outer world', 'What the world panel shows: the public record and history log, the hazards behind a disaster, the technologies as they arrive, the levers an option can pull, and the panel itself.', ['world', 'hazard', 'tech', 'lever', 'panel'])
  + group('What a life remembers', 'Acts the character\'s history keeps: an option falls back to these when it has no icon of its own.', ['act'])
  + optSec;
const n = new Set(Object.values(MAP).flatMap((v) => Object.values(v).flat())).size;
const html = tpl.replace('%SPRITE%', sprite).replace('%N%', n).replace('%BODY%', body);
const OUT = process.argv[3] || 'iconpage/index.html';
fs.mkdirSync(require('path').dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, html);
console.log('ok', html.length, n);
