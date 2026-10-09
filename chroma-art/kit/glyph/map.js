// Which glyph the game shows for each key. Same groups as the game-icons map (chroma-art/old/icons.json), values are glyph names.
const D = (n) => `domain ${n}`;
const MAP = {
  tag: {
    birth: 'birth', start: 'quill', choice: 'signpost', ordinary: 'cup', moment: 'cup', loss: 'heartbreak', death: 'gravestone',
    crisis: 'storm', outside: 'globe', move: 'box', era: D('era'), read: 'newspaper', clash: 'swords', rite: 'steps', turn: 'u-turn',
    breakthrough: 'breakthrough', healed: 'stump', hardened: 'wall', trouble: 'raincloud', fortune: 'horseshoe', temper: 'masks',
    ledger: 'diary', goal: 'dream',
  },
  kind: { career: D('work'), partner: D('partner'), children: D('children'), community: D('community'), faith: D('faith') },
  res: { money: D('money'), time: 'clock', health: D('health'), ties: 'handshake', freedom: 'bird' },
  need: { safety: 'shield', belonging: 'campfire', autonomy: 'compass', competence: 'anvil', meaning: 'lantern' },
  goal: { dream: 'dream', passion: D('passion'), plan: 'checklist' },
  role: { kin: D('family'), love: D('love'), friend: D('friends'), work: D('work'), rival: 'rival', child: D('children'), other: 'person' },
  meter: { content: 'meter content', peace: 'meter peace', strain: 'meter strain', wanting: 'meter wanting' },
  setting: { earth: 'globe', tribal: 'hut', magic: 'crystal-ball' },
  domain: Object.fromEntries(['work', 'family', 'home', 'body', 'health', 'school', 'friends', 'leisure', 'money', 'community', 'love', 'loss',
    'inner', 'children', 'nature', 'public life', 'partner', 'play', 'conflict', 'faith', 'era', 'passion', 'travel', 'mind', 'study'].map((d) => [d, D(d)]).concat(Object.entries({
    // life domains the packs and the newer Earth moments use (live batch of 2026-10-06), each on an existing glyph
    meaning: 'lantern', performing: 'masks', learning: D('study'), education: 'mortarboard', music: 'music-note', making: 'anvil',
    art: 'paintbrush', time: D('era'), history: 'bookshelf', tradition: 'roots', identity: 'mirror', self: 'hand-on-heart',
    sport: 'running-shoe', cause: 'placard', publiclife: D('public life'), media: 'screen', law: 'gavel', justice: 'scales',
    freedom: 'broken-chain', calling: 'bell', fear: 'storm', risk: 'dice', food: 'plate', mentor: 'teacher', care: 'hug',
    volunteering: 'holding-hands', rescue: 'lifebuoy', boredom: 'shrug', 'a team': 'crowd', 'a choir': 'music-note',
    everyday: 'cup', neighbours: D('community'), memory: 'picture-frame', aging: 'elder', door: 'door-open', place: 'map',
    rest: 'bed', any: 'sparkle',
    // the outer world's moments (Library W39, 2026-10-07)
    duty: 'helmet', state: 'town-hall',
  }))),
  tier: { 'life event': 'sparkle', everyday: 'cup', inner: D('inner'), read: 'newspaper', echo: 'u-turn' },
  act: {
    'commit:career': D('work'), 'commit:partner': D('partner'), 'commit:children': D('children'), 'commit:community': D('community'),
    'commit:faith': D('faith'), 'pay:money': D('money'), 'win:money': D('money'), 'win:ties': 'handshake', 'learned a skill': 'anvil',
    'made an enemy': 'rival', 'hid a wrong': 'locked-chest', 'made a friend': D('friends'), 'helped someone in need': 'lifebuoy',
    'took a wild risk': 'dice', 'kept your word': 'sealed-scroll', 'owned up': 'palm', 'moved away': 'box', 'defied an authority': 'fist',
    'turned down a chance': 'door-shut', 'stayed home': D('home'), 'left home': 'door-open', 'broke your word': 'torn-scroll',
    'refused someone in need': 'padlock', 'gave in to pressure': 'puppet', 'came home': 'key',
    'broke the law': 'gavel', 'came out': 'hand-on-heart', 'named their gender': 'hand-on-heart', 'kept it hidden': 'finger-on-lips', 'used drugs': 'pills',
    'took a life': 'gravestone', 'hurt someone badly': 'storm',
  },
  color: { W: 'color W', U: 'color U', B: 'color B', R: 'color R', G: 'color G' },
  // the outer world (W42, chroma-game/notes/world-display-keys.md, 2026-10-06): public record kinds, hazards (engine world.HAZARDS),
  // technologies (world_keys.TECH_KEYS), levers on options, and the world panel's own places
  world: {
    era: D('era'), era_end: D('era'), recession: 'chart-falling', recession_over: 'chart', poll: 'talk', election: 'placard',
    gov_falls: 'placard', local_election: 'town-hall', law: 'gavel', right: 'scales', war: 'swords', war_end: 'swords',
    disaster: 'storm', local_disaster: 'storm', pandemic: 'first-aid', revolution: 'fist', revival: 'sparkle', tech: 'lightbulb',
    figure_rise: 'figure-rising', figure_fall: 'figure-falling', scandal: 'newspaper', inst_scandal: 'newspaper',
    figure_death: 'candle', layoffs: 'factory', closure: 'door-shut', crime_wave: 'shield',
  },
  hazard: { flood: 'flood', fire: 'flame', quake: 'quake', storm: 'storm', heat: 'sun' },
  tech: {
    phone: 'phone', computer: 'laptop', internet: 'signal', 'video calls': 'screen', 'online dating': 'phone-heart',
    'remote work': 'laptop', 'ai helper': 'chat-spark', 'modern medicine': 'pills', car: 'car', plane: 'plane',
  },
  lever: { exit: 'door-open', voice: 'megaphone', loyalty: 'anchor', neglect: 'shrug', subvert: 'domino-mask' },
  panel: { world: 'globe', push: 'crowd' },
  // the shadow states, by the state word a colour's shadow shows (item 2 of the implementation list, chroma-ideas/shadows-mechanics.md)
  shadow: { rigid: 'shadow-rigid', indecisive: 'shadow-indecisive', ruthless: 'shadow-ruthless', reckless: 'shadow-reckless', stuck: 'shadow-stuck' },
  // every option of the live Library (2026-10-06: earth, science, politics, stage; situations and echoes): moment name -> one glyph per option, in option order
  option: require('./option_map.json'),
};
module.exports = { MAP };
