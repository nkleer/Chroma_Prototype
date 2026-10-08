"""Check the played text against Emren's timeless modern setting (2026-10-06 10:42): no calendar year, real brand or
   platform, real war or historical event, real country, people or holiday on screen. Plays lives through the console and
   scans every string the page could show (feed, HUD, checkpoint, outcome, review). Widened to the outer world (release
   row C-G1): every word list in worldview.py, and every other life plays with the stand-in world (test/mock_world.py)
   so the world panel, world lines, cast circle and reach are scanned too.
   python3 test/timeless.py [lives]"""
import sys, re, random, collections, json
sys.path.insert(0, __file__.rsplit("/test/", 1)[0])
from console import Console

REAL = re.compile(r"\b(tiktok|instagram|facebook|twitter|youtube|google|iphone|ipad|android|netflix|spotify|whatsapp|uber|"
                  r"amazon|coca[- ]cola|mcdonald'?s|starbucks|ikea|lego|toyota|playstation|xbox|nintendo|microsoft|samsung|"
                  r"reddit|snapchat|linkedin|tinder|covid|coronavirus|korean?|vietnam|iraq|afghanistan|ukraine|russian?|soviet|"
                  r"world war|9/11|brexit|trump|obama|biden|putin|hitler|nazis?|stalin|america|american|usa|england|english|"
                  r"britain|british|scotland|wales|france|french|germany|german|china|chinese|japan|japanese|india|indian|turkey|"
                  r"turkish|istanbul|london|paris|new york|berlin|tokyo|europe|european|africa|asia|mexico|canada|brazil|italy|"
                  r"italian|spain|spanish|olympics?|nobel|oscars?|grammys?|emmys?|harvard|oxford|cambridge|yale|nasa|fbi|cia|"
                  r"nato|united nations|wall street|hollywood|bollywood|broadway|silicon valley|bitcoin|chatgpt|dollars?|euros?|"
                  r"christmas|christmases|easter|ramadan|diwali|hanukkah|thanksgiving|halloween|jesus|christ|muhammad|allah|"
                  r"bible|quran|koran|vatican|pope|catholic|protestant|muslim|islam|jewish|hindu|buddhist|"
                  r"(1[89]|20)[0-9]{2}s?|'[0-9]0s)\b", re.I)
MARK = re.compile(r"⟦[^⟧]*⟧")


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            if k not in ("dbg", "debug", "src"):
                yield from strings(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from strings(v)


def scan(x, where, hits, seen):
    for s in strings(x):
        s = MARK.sub("", s)
        for m in REAL.finditer(s):
            w = m.group(0).lower()
            hits[w] += 1
            if (w, s[:80]) not in seen:
                seen.add((w, s[:80])); print(f"  [{where}] {w}: {s[:220]}")


import game, worldview
sys.path.insert(1, __file__.rsplit("/", 1)[0]); from mock_world import MockWorld

WL = collections.Counter(); WS = set()                    # the world's own word lists: names, places, events, phrases
for k, v in vars(worldview).items():
    if k.isupper() and isinstance(v, (list, tuple, dict)):
        scan(v, "worldview." + k, WL, WS)
        if isinstance(v, dict):
            scan(list(v.keys()), "worldview." + k + " keys", WL, WS)
print("worldview word lists:", dict(WL) or "clean")

lives = int(sys.argv[1]) if len(sys.argv) > 1 else 4
rnd = random.Random(23)
hits = collections.Counter(); seen = set(); texts = 0
for trial in range(lives):
    game.Game.world_source = MockWorld(trial) if trial % 2 else None
    c = Console(); c.handle("")
    pick = "1" if trial % 2 == 0 else rnd.choice("234")          # modern Earth most often
    for x in [pick, "T" + str(trial)]:
        c.handle(x)
    n = 0
    while c.mode == "play" and n < 4000:
        n += 1
        if c.job is None and c.g.pending is not None:
            text, busy = c.handle(rnd.choice(["", "", str(rnd.choice(list(c.numbering) or [1]))]))
        else:
            text, busy = c.handle("" if rnd.random() < 0.9 else rnd.choice(["v", "l", "y"]))
        scan(text, "terminal", hits, seen)
        feed = c.take_feed(); scan(feed, "feed", hits, seen)
        scan(c.hud(), "hud", hits, seen); texts += 1
        if c.g.world_source is not None and n % 25 == 0:
            scan(c.g.world_panel(), "world panel", hits, seen)
    if c.g.over:
        scan(c.g.review, "review", hits, seen)
    print(f"life {trial} preset {pick} steps {n} over {c.g.over}")
print("real-world words on screen:", dict(hits) or "none", "| states scanned:", texts, "| worldview lists:", dict(WL) or "clean")
