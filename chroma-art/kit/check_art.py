"""The art's own check (backend plan item 3: a fast check per owner). Reads only; writes nothing in the shared folder.

  python3 -B chroma-art/kit/check_art.py           # fast, a few seconds: run after every edit
  python3 -B chroma-art/kit/check_art.py --full    # also rebuilds the icons from the kit (Node; needs kit/glyph)

It checks the tree it sits in (a checkout, or the shared folder), or the tree CHROMA_ROOT names.

Fast: every picture pictures.json names exists, has its size (880x500 events, 700x1000 tarot) and weight (120 KB or less);
every life event the game runs (engine_pin: Earth and the three packs) has its own picture; every icon id in
ink-icons.json is a symbol in ink-icons.svg; every moment the game runs has one icon per option and, for each icon, the
text it was drawn for. Notes, not failures: option texts that differ from the game's batch (the game keeps an icon for
words reworded in place, its web/src/live_icons.py, check C-G2), and a game copy of ink-option-texts.json that differs
from this one (the Game copies this one over, then reruns live_icons.py).
Full: also rebuilds ink-icons.svg and ink-icons.json from kit/glyph in a temporary folder and compares them with game/
(the JSON byte for byte, the sprite symbol by symbol and mask by mask). A pass ends with the line "art check: pass".
"""
import glob, importlib.util, json, os, re, struct, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
sys.path.insert(0, os.path.join(os.environ.get('CHROMA_ROOT') or ROOT, 'chroma-env'))
os.environ.setdefault('CHROMA_ROOT', ROOT)
from paths import path

ART = path('art')
GAME = path('art_game')
fails, notes = [], []
def fail(msg): fails.append(msg)

def webp_size(f):
    b = open(f, 'rb').read(40)
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP': return None
    kind = b[12:16]
    if kind == b'VP8 ': return struct.unpack('<H', b[26:28])[0] & 0x3fff, struct.unpack('<H', b[28:30])[0] & 0x3fff
    if kind == b'VP8L':
        v = struct.unpack('<I', b[21:25])[0]; return 1 + (v & 0x3fff), 1 + ((v >> 14) & 0x3fff)
    if kind == b'VP8X': return 1 + int.from_bytes(b[24:27], 'little'), 1 + int.from_bytes(b[27:30], 'little')
    return None

# pictures
pics = json.load(open(os.path.join(GAME, 'pictures.json'), encoding='utf-8'))
want = {'situation': (880, 500), 'domain': (880, 500), 'tier': (880, 500), 'tarot': (700, 1000)}
named = set()
for grp, wh in want.items():
    for key, rel in pics[grp].items():
        f = os.path.join(GAME, rel); named.add(os.path.normpath(f))
        if not os.path.exists(f): fail(f'pictures.json {grp} "{key}": {rel} is missing'); continue
        if webp_size(f) != wh: fail(f'pictures.json {grp} "{key}": {rel} is {webp_size(f)}, not {wh}')
        if grp != 'tarot' and os.path.getsize(f) > 120 * 1024: fail(f'{rel} weighs {os.path.getsize(f)} bytes, over 120 KB')
for key, rel in pics.get('texture', {}).items():
    f = os.path.join(GAME, rel); named.add(os.path.normpath(f))
    if not os.path.exists(f): fail(f'pictures.json texture "{key}": {rel} is missing')
if any(pics.get('missing', {}).values()): fail(f'pictures.json lists missing keys: {pics["missing"]}')
unnamed = [os.path.basename(f) for f in glob.glob(os.path.join(GAME, 'pics', '*')) if os.path.normpath(f) not in named]
if unnamed: notes.append(f'{len(unnamed)} files in game/pics are not named in pictures.json: {", ".join(sorted(unnamed)[:5])}')

# the game's batch (its pinned Library copy): Earth and the three packs, situations and echoes
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pin = path('game_live', 'engine_pin')
mods = [load(os.path.join(pin, 'earth.py'), 'art_earth')] + [load(os.path.join(pin, f'earth_{k}.py'), f'art_{k}')
        for k in ('science', 'politics', 'stage') if os.path.exists(os.path.join(pin, f'earth_{k}.py'))]
moments = [s for m in mods for s in list(m.SITUATIONS) + list(getattr(m, 'ECHOES', []))]
events = [s for m in mods for s in m.SITUATIONS if s.get('tier') == 'life event']
nopic = [s['name'] for s in events if s['name'] not in pics['situation'] and s.get('variant_of') not in pics['situation']]
if nopic: fail(f'{len(nopic)} life events have no picture of their own: {nopic[:5]}')

# icons
svg = open(os.path.join(GAME, 'ink-icons.svg'), encoding='utf-8').read()
symbols = set(re.findall(r'<symbol id="([^"]+)"', svg))
ink = json.load(open(os.path.join(GAME, 'ink-icons.json'), encoding='utf-8'))
for grp, v in ink['map'].items():
    for key, x in v.items():
        for i in (x if isinstance(x, list) else [x]):
            if i not in symbols: fail(f'ink-icons.json map.{grp} "{key}": {i} is not in ink-icons.svg')
for key, i in ink.get('masks', {}).items():
    if f'<mask id="{i}"' not in svg: fail(f'ink-icons.json masks "{key}": {i} is not a mask in ink-icons.svg')
texts = json.load(open(os.path.join(GAME, 'ink-option-texts.json'), encoding='utf-8'))['option']
opt = ink['map']['option']
for s in moments:
    n, k = s['name'], len(s['options'])
    if len(opt.get(n, [])) != k: fail(f'"{n}": {len(opt.get(n, []))} option icons for {k} options')
    if len(texts.get(n, [])) != len(opt.get(n, [])): fail(f'"{n}": {len(texts.get(n, []))} drawn-for texts for {len(opt.get(n, []))} icons')
    for i, (o, t) in enumerate(zip(s['options'], texts.get(n, []))):
        if o[0] != t: notes.append(f'"{n}" option {i}: the game says "{o[0]}", the icon was drawn for "{t}"')
game_texts = path('game_live', 'web', 'src', 'ink-option-texts.json')
if os.path.exists(game_texts) and json.load(open(game_texts, encoding='utf-8'))['option'] != texts:
    notes.append('game/ink-option-texts.json differs from the game\'s copy (chroma-game/prototype/web/src/ink-option-texts.json): '
                 'the Game copies it over and reruns live_icons.py')

# full: rebuild the icons from the kit and compare
if '--full' in sys.argv:
    with tempfile.TemporaryDirectory() as out:
        builder = os.path.join(ART, 'kit', 'glyph', 'build_icons.js')
        r = subprocess.run(['node', builder, out], capture_output=True, text=True) if os.path.exists(builder) else None
        if r is None: fail(f'--full needs {builder} (the icon kit), which this tree does not have')
        elif r.returncode: fail(f'build_icons.js failed: {r.stderr.strip()[-300:]}')
        else:
            if open(os.path.join(out, 'ink-icons.json'), 'rb').read() != open(os.path.join(GAME, 'ink-icons.json'), 'rb').read():
                fail('ink-icons.json rebuilt from kit/glyph differs from game/ink-icons.json')
            # the live sprite also carries a provenance <metadata> block the build does not write, so compare the drawings
            drawn = lambda s: (re.findall(r'<symbol id="[^"]+".*?</symbol>', s, re.S), re.findall(r'<mask id="[^"]+".*?</mask>', s, re.S))
            if drawn(open(os.path.join(out, 'ink-icons.svg'), encoding='utf-8').read()) != drawn(svg):
                fail('ink-icons.svg rebuilt from kit/glyph draws different symbols or masks than game/ink-icons.svg')

print(f'pictures: {len(pics["situation"])} situations, {len(pics["domain"])} domains, {len(pics["tier"])} tiers, '
      f'{len(pics["tarot"])} tarot cards; {len(events)} life events in the game, {len(nopic)} without a picture')
print(f'icons: {len(symbols)} glyphs; {len(moments)} moments, {sum(len(s["options"]) for s in moments)} options in the game; '
      f'{len(opt)} moments mapped' + ('; rebuilt from the kit' if '--full' in sys.argv else ''))
for n in notes: print('note:', n)
for f in fails: print('FAIL:', f)
print('art check: pass' if not fails else f'art check: {len(fails)} failures')
sys.exit(1 if fails else 0)
