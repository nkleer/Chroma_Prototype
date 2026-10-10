"""Check the spheres' game words in earth_spheres.py (item 15). Library thread, 2026-10-09.

    python3 -B tests/check_spheres.py [path/to/earth_spheres.py] [--setting path/to/check_setting.py]

1 coverage    every sphere, face (45), pair (90), modern event (175), cascade (13), cast (45), haunt kind (31), shadow (45), grey side (9), place (60 x 5 readings), rung (9 x 5) and hover line the data names is here
2 length      names 6 words at most (event names 10), rungs 7, roles 12 (cast roles 14), lines, readings and hover lines 35
3 duplicates  no line or reading said twice; no two faces of one sphere share a name
4 color words no color named, no Magic term, no combination name in brackets
5 style       straight double quotes, curly apostrophes and double spaces are refused; lines end a sentence, names do not
6 safety      nothing sexual, no self-harm, no harm to a child
7 setting     the timeless setting (patterns from check_setting.py when given)
8 faces       in the earth-spheres-*.lib moments (also read by 4 and 6, comments aside) every option has a sphere: face, and the faces are even by colour
              (each option counts 1, split over its face's letters; the totals within 1%)
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
SP, FA, PL, RU, PS, PA, EV, CA, CC = (getattr(M, n, {}) for n in ("SPHERE", "FACE", "PLACE", "RUNG", "PLACE_SHORT", "PAIR",
                                                                  "EVENT", "CAST", "CASCADE"))
HA = getattr(M, "HAUNT", {})
SH, GR, DP = (getattr(M, n, {}) for n in ("SHADOW", "GREY", "DEEP"))
HAUNT_KINDS = ["gather.house", "gather.hall", "gather.games", "gather.circle", "gather.night", "arts.song", "arts.stage",
               "arts.tale", "arts.page", "arts.craft", "faith.congregation", "faith.orders", "faith.seeking",
               "learn.keeping", "learn.higher", "care.houses", "comm.market", "comm.shop", "comm.credit", "prod.wild",
               "prod.land", "prod.craft", "prot.watch", "prot.host", "rule.voice", "rule.counsel", "gather.great",
               "gather.talk", "arts.screen", "faith.shrines", "prot.rescue"]   # build.py HAUNT_KINDS
WHEEL = "WU UB BR RG GW WB UR BG RW GU".split()

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
    for pk in WHEEL:
        p = PA.get(f"{s}.{pk}")
        if not p or not {"name", "idea", "line", "shadow", "place", "role"} <= set(p):
            fail("1 coverage", f"PAIR.{s}.{pk}: wanted name, idea, line, shadow, place and role")
if set(k.split(".")[1] for k in PA) - set(WHEEL):
    fail("1 coverage", "PAIR: a key not in wheel order")
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
MODERN = set()   # the data's modern event keys, sphere.event
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
        want = {f"{s}.{e['key']}" for e in d["events"] if (e.get("wording") or {}).get("modern")}
        MODERN |= want
        have = {k for k in EV if k.split(".")[0] == s}
        if want - have:
            fail("1 coverage", f"EVENT: modern events with no words: {sorted(want - have)}")
        if have - want:
            fail("1 coverage", f"EVENT: keys the data does not have: {sorted(have - want)}")
    L = json.load(open(os.path.join(DATA, "links.json"), encoding="utf-8"))
    want = {c["id"] for c in L["colour"]["cascades"] if "modern" in c["epochs"]}
    if want != set(CC):
        fail("1 coverage", f"CASCADE: wanted {sorted(want)}, have {sorted(CC)}")
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
for k, p in PA.items():
    ALL += [(f"PAIR.{k}.name", p["name"], "name", 7), (f"PAIR.{k}.place", p["place"], "name", 12),
            (f"PAIR.{k}.role", p["role"], "name", 12)]
    ALL += [(f"PAIR.{k}.{f}", p[f], "line", 40) for f in ("idea", "line", "shadow")]
for k, e in EV.items():
    if e.get("tone") not in ("good", "bad", "mixed"):
        fail("1 coverage", f"EVENT.{k}.tone: {e.get('tone')}")
    ALL += [(f"EVENT.{k}.name", e["name"], "name", 10), (f"EVENT.{k}.line", e["line"], "line", 40),
            (f"EVENT.{k}.self", e["self"], "line", 40)]
for k, c in CA.items():
    if k not in FA:
        fail("1 coverage", f"CAST.{k}: not a face")
    ALL += [(f"CAST.{k}.role", c["role"], "name", 14), (f"CAST.{k}.place", c["place"], "name", 12),
            (f"CAST.{k}.line", c["line"], "line", 35)]
if len(CA) != 45:
    fail("1 coverage", f"CAST: {len(CA)} faces, wanted 45")
for k, c in CC.items():
    ALL.append((f"CASCADE.{k}.name", c["name"], "name", 6))
    for i, st in enumerate(c["steps"]):
        if st["event"] and st["event"] in MODERN and st["event"] not in EV:
            fail("1 coverage", f"CASCADE.{k}.{i}: event {st['event']} has no EVENT words")
        ALL.append((f"CASCADE.{k}.{i}.t", st["t"], "line", 40))
        if st["me"]:
            ALL.append((f"CASCADE.{k}.{i}.me", st["me"], "line", 40))
for k in FA:
    if k not in SH:
        fail("1 coverage", f"SHADOW.{k}: no shadow line")
for s in SPHERES:
    if s not in GR:
        fail("1 coverage", f"GREY.{s}: no words")
ALL += [(f"SHADOW.{k}", t, "line", 35) for k, t in SH.items()]
for k, g in GR.items():
    ALL += [(f"GREY.{k}.name", g["name"], "name", 6)] + [(f"GREY.{k}.{f}", g[f], "line", 35) for f in ("line", "grows", "shrinks")]
for k, g in DP.items():
    ALL += [(f"DEEP.{k}.name", g["name"], "name", 4)] + [(f"DEEP.{k}.{f}", g[f], "line", 25) for f in ("hover", "begins", "ends")]
if set(HA) != set(HAUNT_KINDS):
    fail("1 coverage", f"HAUNT: missing {sorted(set(HAUNT_KINDS) - set(HA))}, extra {sorted(set(HA) - set(HAUNT_KINDS))}")
hnames = {}
for k, h in HA.items():
    for n in h.get("names", []):
        if n in hnames:
            fail("3 duplicates", f"HAUNT.{k}: the name {n} is also {hnames[n]}'s")
        hnames[n] = k
        ALL.append((f"HAUNT.{k}.names", n, "name", 4))
    ALL += [(f"HAUNT.{k}.{f}", h[f], "name", 6) for f in ("keeper", "regular", "patron")]
    for f in ("go_between", "newcomer", "known"):
        for i, t in enumerate(h[f]):
            ALL.append((f"HAUNT.{k}.{f}.{i}", t, "line", 30))
            if "{N}" not in t or set(re.findall(r"\{(\w+)\}", t)) - {"N", "keeper", "regular"}:
                fail("1 coverage", f"HAUNT.{k}.{f}.{i}: wants {{N}} and no slot but keeper and regular: {t}")
for s, rs in RU.items():
    ALL += [(f"RUNG.{s}.{i}", t, "name", 7) for i, t in enumerate(rs)]
for (k, e), t in PS.items():
    ALL.append((f"PLACE_SHORT.{k}.{e}", t, "name", 5))
FP, FR = getattr(M, "FAIR_PART", {}), getattr(M, "FAIR", {})   # S1 fairness read five ways (social-mechanics.md S1)
PARTS = ["rules", "reasons", "due", "respect", "goodwill"]
if FP or FR:
    if sorted(FP) != sorted(PARTS):
        fail("1 coverage", f"FAIR_PART: parts {sorted(FP)}, wanted {PARTS}")
    want_ = {f"{s_}.{p_}" for s_ in SPHERES for p_ in PARTS}
    if set(FR) != want_:
        fail("1 coverage", f"FAIR: missing {sorted(want_ - set(FR))}, extra {sorted(set(FR) - want_)}")
    for k, d in FP.items():
        ALL.append((f"FAIR_PART.{k}.name", d.get("name", ""), "name", 6))
    for nm_, tab_ in (("FAIR_PART", FP), ("FAIR", FR)):
        for k, d in tab_.items():
            ALL += [(f"{nm_}.{k}.{f}", d.get(f, ""), "clause", 16) for f in ("unfair", "fair")]
LN = getattr(M, "LINE", {})   # S5 sacred lines (social-mechanics.md S5)
KINDS = ["promise", "truth", "own_say", "loved", "home"]
if LN:
    if sorted(LN) != sorted(KINDS):
        fail("1 coverage", f"LINE: kinds {sorted(LN)}, wanted {KINDS}")
    for k, d in LN.items():
        ALL.append((f"LINE.{k}.name", d.get("name", ""), "name", 6))
        wn_ = d.get("will_not", [])
        if len(wn_) != 3:
            fail("1 coverage", f"LINE.{k}.will_not: {len(wn_)} lines, wanted 3")
        ALL += [(f"LINE.{k}.will_not.{i}", t, "clause", 10) for i, t in enumerate(wn_)]
        ALL.append((f"LINE.{k}.peace", d.get("peace", ""), "clause", 8))
        for f in ("formed", "held", "crossed", "healed"):
            t = d.get(f, "")
            ALL.append((f"LINE.{k}.{f}", t, "line", 22))
            if "{N}" not in t or set(re.findall(r"{(\w+)}", t)) - {"N", "Ns"}:
                fail("1 coverage", f"LINE.{k}.{f}: needs {{N}} and no other slot but {{Ns}}: {t}")

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

import glob
face_w = {c: 0.0 for c in COLORS}
n_opt = 0
for f in sorted(glob.glob(os.path.join(os.path.dirname(PATH), "earth-spheres-*.lib"))):
    for i, ln in enumerate(open(f, encoding="utf-8"), 1):
        if not ln.startswith("#"):
            for m in list(COLOR_WORDS.finditer(ln)) + list(MAGIC_WORDS.finditer(ln)):
                fail("4 color words", f"\"{m.group(0)}\": {os.path.basename(f)}:{i}")
            for m in SAFETY.finditer(ln):
                fail("6 safety", f"\"{m.group(0)}\": {os.path.basename(f)}:{i}")
        if not ln.startswith("- "):
            continue
        n_opt += 1
        m = re.search(r"\| sphere: ([a-z]+)\.([WUBRG]{1,2}) ?(\||$)", ln)
        if not m:
            fail("8 faces", f"{os.path.basename(f)}:{i}: an option with no sphere: face")
            continue
        for c in m.group(2):
            face_w[c] += 1 / len(m.group(2))
if n_opt and max(face_w.values()) - min(face_w.values()) > .01 * n_opt / 5:
    fail("8 faces", f"faces uneven by colour over {n_opt} options: {face_w}")
NAMES = ["1 coverage", "2 length", "3 duplicates", "4 color words", "5 style", "6 safety", "7 setting", "8 faces"]
print(f"# check_spheres: {os.path.basename(PATH)}\n")
print(f"{len(ALL)} lines: {len(SP)} spheres, {len(FA)} faces, {len(PA)} pairs, {len(EV)} events, {len(CC)} cascades, {len(HA)} haunts, {len(PL)} places, {len(RU)} ladders, {len(FR)} fairness, {len(LN)} lines; data {data_note}\n")
for nm in NAMES:
    ps = problems.get(nm, [])
    extra_ = f", {setting_note}" if nm == "7 setting" else (f", {n_opt} options: " + " ".join(f"{c} {v:.0f}" for c, v in face_w.items()) if nm == "8 faces" else "")
    print(f"- {nm}: {'PASS' if not ps else f'FAIL ({len(ps)})'}{extra_}")
    for p in ps[:12]:
        print(f"    {p}")
    if len(ps) > 12:
        print(f"    ... and {len(ps) - 12} more")
total = sum(len(v) for v in problems.values())
print(f"\n{'PASS' if not total else 'FAIL'}: {total} problems")
sys.exit(1 if total else 0)
