"""Checks for earth_book.py (the Book's and the chapters' words, next version). Library thread, 2026-10-07.

    python3 check_book.py [path/to/earth_book.py]      exit status 1 if a check fails

1. shape: the keys and counts the game asked for (2026-10-07): QUESTION 2 per colour, ANSWER 4 bands per colour
   with 2 or more each, LEANING and TURN 2-4 per side for all ten sides, SIDE_PHRASE and VOICE_SIDE for all ten
   sides, LIFE and VOICE_LEAN with {a} and {b}, PAIR_LOVE and PAIR_ARGUMENT 2 per pair for all ten pairs,
   VOICE_IDENT with {name}, VOICE_STEER 4 bands, VOICE_FORMING;
2. fills: story lines take {N} only (LEANING, TURN and the pair lines must use it); the Your Voice lines take only
   {name}, {a} and {b} and speak to "you"; phrases take none;
3. words: no colour words, no Magic terms, never enemy or ally; no digits, dashes or straight double quotes;
4. length and form: story lines at most 22 words, answers at most 14, phrases at most 8; lines end a sentence,
   phrases do not; no line twice;
5. filled: every line filled with a sample name and every side phrase leaves no placeholder.
"""
import importlib.util
import itertools
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "earth_book.py")
COLORS = "WUBRG"
AXES = ["group vs individual", "security vs freedom", "head vs heart", "destiny vs free will", "nature vs nurture"]
SIDES = [(a, s) for a in AXES for s in (+1, -1)]
PAIRS = ["".join(p) for p in itertools.combinations(COLORS, 2)]
BANNED = re.compile(r"\b(white|blue|black|red|green|colou?rs?|mana|planeswalker|guild|enem(y|ies)|all(y|ies)|"
                    r"azorius|orzhov|boros|selesnya|dimir|izzet|simic|rakdos|golgari|gruul)\b", re.I)
FILL = re.compile(r"\{(\w+)\}")

spec = importlib.util.spec_from_file_location("earth_book", PATH)
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
fails = []


def fail(check, msg):
    fails.append(f"{check}: {msg}")


rows = []   # (kind, where, text): kind story | answer | phrase | voice | template


def need(name):
    v = getattr(B, name, None)
    if v is None:
        fail("1 shape", f"{name} is missing")
    return v


Q, A = need("QUESTION"), need("ANSWER")
for c in COLORS:
    qs = (Q or {}).get(c, [])
    if len(qs) != 2:
        fail("1 shape", f"QUESTION[{c}] has {len(qs)} variants, expected 2")
    rows += [("story", f"QUESTION[{c}]", q) for q in qs]
    bands = (A or {}).get(c, [])
    if len(bands) != 4:
        fail("1 shape", f"ANSWER[{c}] has {len(bands)} bands, expected 4")
    for i, band in enumerate(bands):
        if len(band) < 2:
            fail("1 shape", f"ANSWER[{c}][{i}] has {len(band)} answers, expected 2 or more")
        rows += [("answer", f"ANSWER[{c}][{i}]", x) for x in band]
for name in ("LEANING", "TURN"):
    d = need(name) or {}
    for side in SIDES:
        vs = d.get(side, [])
        if not 2 <= len(vs) <= 4:
            fail("1 shape", f"{name}[{side}] has {len(vs)} variants, expected 2 to 4")
        rows += [("story", f"{name}[{side}]", x) for x in vs]
    extra = set(d) - set(SIDES)
    if extra:
        fail("1 shape", f"{name} has unknown sides {sorted(extra)}")
for name in ("SIDE_PHRASE", "VOICE_SIDE"):
    d = need(name) or {}
    for side in SIDES:
        if not isinstance(d.get(side), str):
            fail("1 shape", f"{name}[{side}] is missing")
        else:
            rows.append(("phrase", f"{name}[{side}]", d[side]))
for name in ("PAIR_LOVE", "PAIR_ARGUMENT"):
    d = need(name) or {}
    for p in PAIRS:
        vs = d.get(p, [])
        if len(vs) != 2:
            fail("1 shape", f"{name}[{p}] has {len(vs)} variants, expected 2")
        rows += [("story", f"{name}[{p}]", x) for x in vs]
for name, fills in (("LIFE", {"a", "b"}), ("VOICE_LEAN", {"a", "b"}), ("VOICE_IDENT", {"name"})):
    for x in need(name) or []:
        if set(FILL.findall(x)) != fills:
            fail("2 fills", f"{name} line must use exactly {sorted(fills)}: {x}")
        rows.append(("template" if name == "LIFE" else "voice", name, x))
steer = need("VOICE_STEER") or []
if len(steer) != 4:
    fail("1 shape", f"VOICE_STEER has {len(steer)} bands, expected 4")
for i, band in enumerate(steer):
    rows += [("voice", f"VOICE_STEER[{i}]", x) for x in band]
rows += [("voice", "VOICE_FORMING", x) for x in need("VOICE_FORMING") or []]

seen = {}
for kind, where, x in rows:
    used = set(FILL.findall(x))
    allowed = {"story": {"N"}, "answer": {"N"}, "phrase": set(), "template": {"a", "b"}, "voice": {"name", "a", "b"}}[kind]
    if used - allowed:
        fail("2 fills", f"{where} uses {sorted(used - allowed)}: {x}")
    if kind == "story" and where.startswith(("LEANING", "TURN", "PAIR")) and "N" not in used:
        fail("2 fills", f"{where} does not name the character with {{N}}: {x}")
    if kind == "voice" and where != "VOICE_SIDE" and not re.search(r"\byou(r|rs)?\b", x, re.I):
        fail("2 fills", f"{where} does not speak to the player as you: {x}")
    if "{Ns}" in x:
        fail("2 fills", f"{where} uses {{Ns}}; write {{N}}'s: {x}")
    if BANNED.search(x):
        fail("3 words", f"{where} has a banned word '{BANNED.search(x).group(0)}': {x}")
    if re.search(r"\d|[–—]|\"", x):
        fail("3 words", f"{where} has a digit, a dash or a straight double quote: {x}")
    words = len(x.split())
    limit = {"story": 22, "answer": 14, "phrase": 8, "template": 10, "voice": 14}[kind]
    if words > limit:
        fail("4 length", f"{where} has {words} words (at most {limit}): {x}")
    ends = x.rstrip().endswith((".", "?", "!"))
    if kind == "phrase" and ends:
        fail("4 length", f"{where} is a phrase and should not end a sentence: {x}")
    if kind != "phrase" and not ends:
        fail("4 length", f"{where} does not end a sentence: {x}")
    if x in seen and kind != "phrase":
        fail("4 length", f"{where} repeats {seen[x]}: {x}")
    seen.setdefault(x, where)

sample = {"N": "Sam", "name": "The Wild Heart"}
phrases = list(getattr(B, "SIDE_PHRASE", {}).values())
vphr = list(getattr(B, "VOICE_SIDE", {}).values())
for kind, where, x in rows:
    outs = []
    if "{a}" in x:
        src = phrases if kind == "template" else vphr
        outs = [x.replace("{a}", a).replace("{b}", b) for a in src for b in src if a != b]
    else:
        outs = [x]
    for o in outs:
        o = o.replace("{N}", sample["N"]).replace("{name}", sample["name"])
        if FILL.search(o):
            fail("5 filled", f"{where} leaves a placeholder: {o}")
        if re.search(r"\b(\w+) \1\b", o, re.I):
            fail("5 filled", f"{where} doubles a word: {o}")

print(f"earth_book.py: {len(rows)} lines and phrases checked")
if fails:
    print(f"{len(fails)} problems:")
    print("\n".join("  - " + f for f in fails))
    sys.exit(1)
print("all checks pass")
