"""Check the spheres' game words in earth_spheres.py (item 15). Library thread, 2026-10-09.

    python3 -B tests/check_spheres.py [path/to/earth_spheres.py] [--setting path/to/check_setting.py]

1 coverage    every sphere, face (45), place (60 x 5 readings), rung (9 x 5) and hover line the data names is here
2 length      names 6 words at most, rungs 7, roles 12, lines, readings and hover lines 35
3 duplicates  no line or reading said twice; no two faces of one sphere share a name
4 color words no color named, no Magic term, no combination name in brackets
5 style       straight double quotes, curly apostrophes and double spaces are refused; lines end a sentence, names do not
6 safety      nothing sexual, no self-harm, no harm to a child
7 setting     the timeless setting (patterns from check_setting.py when given)
Exits 1 on any problem.
"""
import os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(HERE)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
SETTING = None
if "--setting" in sys.argv:
    SETTING = sys.argv[sys.argv.index("--setting") + 1]
    args = [a for a in args if a != SETTING]
elif os.path.exists(os.path.join(LIB, "drafts", "check_setting.py")):
    SETTING = os.path.join(LIB, "drafts", "check_setting.py")
PATH = args[0] if args else os.path.join(LIB, "earth_spheres.py")

SPHERES = ["rule", "gather", "arts", "faith", "care", "learn", "prod", "comm", "prot"]
COLORS = "WUBRG"
DRIVERS = ["insecurity", "plenty", "war", "crowding", "inequality", "schooling", "exposure", "change"]
COLOR_WORDS = re.compile(r"\b(white[s]?|whiter|blue[s]?|bluer|black[s]?|blacker|blackened|red[s]?|redder|"
                         r"green[s]?|greener)\b", re.I)
MAGIC_WORDS = re.compile(r"\b(colou?rs?|mana|planeswalker\w*|azorius|dimir|rakdos|gruul|selesnya|orzhov|izzet|"
                         r"golgari|boros|simic|lawkeeper|guild\w*)\b", re.I)
SAFETY = re.compile(r"\b(rap(e|ed|es|ing|ist)|sexual\w*|sex|molest\w*|suicid\w*|self-harm\w*|abus\w* (a|the) child\w*|"
                    r"child abuse)\b", re.I)

problems = {}


def fail(check, msg):
    problems.setdefault(check, []).append(msg)


spec = importlib.util.spec_from_file_location("earth_spheres_checked", PATH)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
SP, FA, PL, RU, PS = (getattr(M, n, {}) for n in ("SPHERE", "FACE", "PLACE", "RUNG", "PLACE_SHORT"))

# ------------------------------------------------------------------------------------------------- 1 coverage
for s in SPHERES:
    if s not in SP or not {"name", "question"} <= set(SP[s]):
        fail("1 coverage", f"SPHERE.{s}: wanted name and question")
    for c in COLORS:
        f = FA.get(f"{s}.{c}")
        if not f or not {"name", "line", "hover"} <= set(f):
            fail("1 coverage", f"FACE.{s}.{c}: wanted name, line and hover")
        elif any(k not in DRIVERS for k in f["hover"]):
            fail("1 coverage", f"FACE.{s}.{c}.hover: a key that is not a driver: {[k for k in f['hover'] if k not in DRIVERS]}")
    if not (isinstance(RU.get(s), list) and len(RU[s]) == 5):
        fail("1 coverage", f"RUNG.{s}: wanted five rungs")
extra = [k for k in FA if k.split(".")[0] not in SPHERES or k.split(".")[1] not in COLORS]
if extra:
    fail("1 coverage", f"FACE: keys that are not faces: {extra}")
if len(PL) != 60:
    fail("1 coverage", f"PLACE: {len(PL)} kinds of place, wanted 60")
for k, p in PL.items():
    if k.split(".")[0] not in SPHERES:
        fail("1 coverage", f"PLACE.{k}: not a sphere's place")
    for c in COLORS:
        if not (isinstance(p.get(c), tuple) and len(p[c]) == 2):
            fail("1 coverage", f"PLACE.{k}.{c}: wanted (role, reading)")
# the data, when it is there: every subsector and driver line it names has words here
DATA = os.path.join(os.environ.get("CHROMA_ROOT", "/mnt/project-files"), "chroma-ideas", "spheres-data")
data_note = "skipped (no chroma-ideas/spheres-data)"
if os.path.isdir(DATA):
    import json
    for s in SPHERES:
        d = json.load(open(os.path.join(DATA, f"{s}.json"), encoding="utf-8"))
        for sub in d["subsectors"]:
            if f"{s}.{sub['key']}" not in PL:
                fail("1 coverage", f"PLACE.{s}.{sub['key']}: the data's subsector has no words")
        for c in COLORS:
            want = set(d["faces"][c].get("driver_lines", {}))
            have = set(FA.get(f"{s}.{c}", {}).get("hover", {}))
            if want - have:
                fail("1 coverage", f"FACE.{s}.{c}.hover: no line for {sorted(want - have)}")
    data_note = "against " + DATA

# ------------------------------------------------------------------------------------------------- lines
ALL = []   # (where, text, kind, word limit)
for s, d in SP.items():
    ALL += [(f"SPHERE.{s}.name", d["name"], "name", 6), (f"SPHERE.{s}.question", d["question"], "line", 35)]
for k, f in FA.items():
    ALL += [(f"FACE.{k}.name", f["name"], "name", 6), (f"FACE.{k}.line", f["line"], "line", 35)]
    ALL += [(f"FACE.{k}.hover.{dr}", t, "line", 35) for dr, t in f["hover"].items()]
for k, p in PL.items():
    ALL += [(f"PLACE.{k}.name", p["name"], "name", 5), (f"PLACE.{k}.kind", p["kind"], "name", 6)]
    for c in COLORS:
        if isinstance(p.get(c), tuple) and len(p[c]) == 2:
            ALL += [(f"PLACE.{k}.{c}.role", p[c][0], "name", 12), (f"PLACE.{k}.{c}.reading", p[c][1], "line", 35)]
for s, rs in RU.items():
    ALL += [(f"RUNG.{s}.{i}", t, "name", 7) for i, t in enumerate(rs)]
for (k, e), t in PS.items():
    ALL.append((f"PLACE_SHORT.{k}.{e}", t, "name", 5))

seen = {}
for at, text, kind, limit in ALL:
    if not isinstance(text, str) or not text.strip():
        fail("1 coverage", f"{at}: empty")
        continue
    n = len(text.split())
    if n > limit:
        fail("2 length", f"{n} words (limit {limit}): {at}: {text}")
    if kind in ("line", "clause"):
        if text in seen:
            fail("3 duplicates", f"{at} repeats {seen[text]}: {text}")
        seen[text] = at
    for m in COLOR_WORDS.finditer(text):
        fail("4 color words", f"\"{m.group(0)}\": {at}")
    for m in MAGIC_WORDS.finditer(text):
        fail("4 color words", f"Magic term \"{m.group(0)}\": {at}")
    if re.search(r"\([^)]*\)", text):
        fail("4 color words", f"a name in brackets (a combination name?): {at}: {text}")
    if '"' in text:
        fail("5 style", f"straight double quote: {at}")
    if "’" in text or "‘" in text:
        fail("5 style", f"curly apostrophe (the Library uses '): {at}")
    if re.search(r"\s{2,}|\s[,.?!]", text):
        fail("5 style", f"double space or space before punctuation: {at}")
    if kind == "line" and not re.search(r"[.?!]$", text):
        fail("5 style", f"a line does not end a sentence: {at}: {text}")
    if kind == "name" and re.search(r"[.!:;,]$", text):
        fail("5 style", f"a name ends in punctuation: {at}: {text}")
    if kind == "clause" and (re.search(r"[.?!:;,]$", text) or text[:1].isupper()):
        fail("5 style", f"a hover clause starts lower case and has no end punctuation: {at}: {text}")
    for m in SAFETY.finditer(text):
        fail("6 safety", f"\"{m.group(0)}\": {at}")
for s in SPHERES:
    names = [FA.get(f"{s}.{c}", {}).get("name") for c in COLORS]
    if len(set(names)) != len(names):
        fail("3 duplicates", f"FACE {s}: two faces share a name: {names}")

setting_note = "skipped: no check_setting.py (give --setting)"
if SETTING and os.path.exists(SETTING):
    src = open(SETTING, encoding="utf-8").read()
    ns = {"__file__": SETTING}
    exec(compile(src.split("\nNEXT = ")[0], SETTING, "exec"), ns)
    pats = [(k, v, re.I) for k, v in ns["PAT"].items()] + [(k, v, 0) for k, v in ns["CASE"].items()]
    for at, text, _, _ in ALL:
        for kind, pat, fl in pats:
            for m in re.finditer(pat, text, fl):
                fail("7 setting", f"{kind}: '{m.group(0)}' in {at}: {text}")
    setting_note = "patterns from " + SETTING

NAMES = ["1 coverage", "2 length", "3 duplicates", "4 color words", "5 style", "6 safety", "7 setting"]
print(f"# check_spheres: {os.path.basename(PATH)}\n")
print(f"{len(ALL)} lines: {len(SP)} spheres, {len(FA)} faces, {len(PL)} places, {len(RU)} ladders; data {data_note}\n")
for nm in NAMES:
    ps = problems.get(nm, [])
    extra_ = f", {setting_note}" if nm == "7 setting" else ""
    print(f"- {nm}: {'PASS' if not ps else f'FAIL ({len(ps)})'}{extra_}")
    for p in ps[:12]:
        print(f"    {p}")
    if len(ps) > 12:
        print(f"    ... and {len(ps) - 12} more")
total = sum(len(v) for v in problems.values())
print(f"\n{'PASS' if not total else 'FAIL'}: {total} problems")
sys.exit(1 if total else 0)
