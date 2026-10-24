"""Check a perks-volume-2 part: python3 /mnt/project-files/chroma-library/drafts/check_perks2.py /mnt/project-files/chroma-library/drafts/perks2/<part>.py [roles file] [links file]
Loads PERKS2 from the part (plain data), checks fields, names (unique against the catalogue and the other parts), kinds,
ways letters, odds (access perks 0), skill_half and retires, say (works after the character's name), references
([title or perk], 'situation' or 'mark'), the color balance within 3% and the share sum; with a roles file, ROLES2
names and condition words; with a links file, TITLE_LINKS names and condition words."""
import sys, os, re, glob, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.environ.get("CHROMA_ROOT", "/mnt/project-files"), "chroma-env"))   # folder names: chroma-env/paths.py
from paths import P as PATHS
LIB = PATHS["library_live"]
def load(p):
    spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3].replace("-", "_"), p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
cat = load(f"{LIB}/earth_perks_titles.py")   # the live catalogue since 2026-10-05 18:25
me = os.path.realpath(sys.argv[1])
part = load(me); T = list(part.PERKS2)
others = []
for p in glob.glob(f"{LIB}/drafts/perks2/*.py"):
    b = os.path.basename(p)
    if os.path.realpath(p) != me and not b.startswith("roles") and not b.startswith("links"):
        try: others += [t["name"] for t in load(p).PERKS2]
        except Exception: pass
OLD = ({x["name"] for x in cat.TITLES} | {x["name"] for x in cat.PERKS}) - {t["name"] for t in T} - set(others)   # once merged, a part's own names are in the catalogue
ALLN = OLD | {t["name"] for t in T} | set(others)
SITS = {l[4:].strip() for l in open(f"{LIB}/earth.md", encoding="utf-8") if l.startswith("### ")}
src = open(f"{LIB}/build.py").read()
MARKS = set(re.findall(r'"([^"]+)"', src[src.index("MARKS = ["):src.index("]", src.index("MARKS = ["))]))
KINDS = ["skill", "credential", "standing", "bond", "asset"]
PRED = {"a", "an", "the", "in", "on", "known", "good", "from", "someone"}   # explain.predicate puts "is" before these
prob = []; P = lambda m: prob.append(m)
names = [t.get("name") for t in T]
for n in set(names):
    if names.count(n) > 1: P(f"duplicate name in this part: {n}")
for t in T:
    n = t.get("name", "?")
    for k in ("name", "kind", "ways", "odds", "skill_half", "retires", "ages", "share", "say", "gained", "lost", "needs"):
        if k not in t: P(f"{n}: missing {k}")
    extra = set(t) - {"name", "kind", "ways", "odds", "skill_half", "retires", "ages", "share", "say", "gained", "lost", "needs"}
    if extra: P(f"{n}: unknown fields {sorted(extra)}")
    if n in OLD: P(f"{n}: already in the catalogue")
    if n in others: P(f"{n}: also in another part")
    if n != n.lower(): P(f"{n}: names are lower case")
    k = t.get("kind")
    if k not in KINDS: P(f"{n}: bad kind {k}")
    if not re.fullmatch(r"[WUBRG]( [WUBRG]){0,2}", t.get("ways", "")) or len(set(t.get("ways", "").split())) != len(t.get("ways", "").split()):
        P(f"{n}: bad ways {t.get('ways')!r}")
    o = t.get("odds")
    if k in ("credential", "asset"):
        if o not in (0, None): P(f"{n}: an access perk ({k}) has odds 0")
    elif not (isinstance(o, (int, float)) and .02 <= o <= .1): P(f"{n}: odds {o!r} outside .02 to .1")
    sh = t.get("skill_half", 0)
    if not (sh is None or (isinstance(sh, (int, float)) and sh > 0)): P(f"{n}: skill_half {sh!r}")
    a = t.get("ages", (0, 0))
    if not (isinstance(a, tuple) and len(a) == 2 and all(isinstance(x, int) for x in a) and 0 <= a[0] < a[1] <= 110): P(f"{n}: ages {a}")
    r = t.get("retires", 0)
    if not (r is None or (isinstance(r, int) and isinstance(a, tuple) and a[0] < r <= a[1] + 1)): P(f"{n}: retires {r!r}")
    s = t.get("share", 0)
    if not (isinstance(s, (int, float)) and 0 < s <= 1): P(f"{n}: share {s}")
    say = t.get("say", "")
    w0 = say.split(" ", 1)[0] if say else ""
    if not say or "{" in say or say != say.strip() or say.endswith("."): P(f"{n}: say should be a short plain phrase")
    elif not (w0 in PRED or w0 in ("can", "is", "has") or w0.endswith("s")):
        P(f"{n}: say {say!r} must read after the name ('can fly a plane', 'holds a pilot's licence', 'a beekeeper')")
    for fld in ("gained", "lost", "needs"):
        for b in re.findall(r"\[([^\]]+)\]", t.get(fld, "")):
            if b not in ALLN: P(f"{n}: {fld} names unknown [{b}]")
        for q in re.findall(r"(?:(?<=^)|(?<=[\s(]))'([^']+)'(?![a-z])", t.get(fld, "")):
            if q not in SITS and q not in MARKS: P(f"{n}: {fld} quotes '{q}', which is not an Earth situation or mark")
cnt = {c: 0.0 for c in "WUBRG"}
for t in T:
    ls = t.get("ways", "").split()
    for c in ls:
        if c in cnt: cnt[c] += 1 / len(ls)
v = list(cnt.values()); mean = sum(v) / 5
print(f"{len(T)} perks in {os.path.basename(me)}; kinds: " + ", ".join(f"{k} {sum(t.get('kind') == k for t in T)}" for k in KINDS))
print("ways per color W U B R G: " + " ".join(f"{x:.2f}" for x in v) + (f"; spread {(max(v) - min(v)) / mean:.1%} (limit 3%)" if mean else ""))
if mean and (max(v) - min(v)) / mean > 0.03: P("colors are not even within 3%")
print(f"share sum {sum(t.get('share', 0) for t in T):.2f}; by kind: " + ", ".join(f"{k} {sum(t.get('share', 0) for t in T if t.get('kind') == k):.2f}" for k in KINDS))
def cond_check(where, code):
    for q in re.findall(r"(?:has|was|yrs_has)\('((?:[^'\\]|\\.)+)'\)", code or ""):
        if q.replace("\\'", "'") not in ALLN: P(f"{where} names unknown {q}")
    for q in re.findall(r"mkn?\('([^']+)'", code or ""):
        if q not in MARKS: P(f"{where} names unknown mark {q}")
    for lst in re.findall(r"had\(\[([^\]]+)\]", code or ""):
        for q in re.findall(r"'([^']+)'", lst):
            if q not in SITS: P(f"{where} had() names unknown situation {q}")
def loses(r):
    l_ = r.get("lose")
    return [c for c, _ in l_] if isinstance(l_, list) else [l_]
if len(sys.argv) > 2:
    R = load(sys.argv[2]).ROLES2
    for k, r in R.items():
        if k not in {t["name"] for t in T}: P(f"roles: {k} is not in this part")
        for fld in ("req",): cond_check(f"roles: {k} {fld}", r.get(fld))
        for c in loses(r): cond_check(f"roles: {k} lose", c)
        bad = set(r) - {"req", "rate", "lose", "lrate", "lwhy", "weight", "grants"}
        if bad: P(f"roles: {k} unknown fields {sorted(bad)}")
        for fld in ("rate", "lrate"):
            if fld in r and not (isinstance(r[fld], (int, float)) and 0 < r[fld] <= 1): P(f"roles: {k} {fld} {r[fld]!r} outside 0 to 1")
        if r.get("weight") not in (None, "practice", "colors", "money", "ties"): P(f"roles: {k} weight {r.get('weight')!r}")
        for g in r.get("grants", []):
            if g not in ALLN: P(f"roles: {k} grants unknown {g}")
    miss = [t["name"] for t in T if t["name"] not in R]
    print(f"roles: {len(R)} rules; perks without a rule: {', '.join(miss) if miss else 'none'}")
if len(sys.argv) > 3:
    TL = load(sys.argv[3]).TITLE_LINKS
    titles = {x["name"] for x in cat.TITLES}
    for k, r in TL.items():
        if k not in titles: P(f"links: {k} is not a catalogue title")
        for g in r.get("grants", []):
            if g not in ALLN: P(f"links: {k} grants unknown {g}")
        cond_check(f"links: {k} req", r.get("req")); cond_check(f"links: {k} lose", r.get("lose") if isinstance(r.get("lose"), str) else "")
        if isinstance(r.get("lose"), list):
            for c, _ in r["lose"]: cond_check(f"links: {k} lose", c)
        if set(r) - {"req", "grants", "lose", "lrate", "why"}: P(f"links: {k} unknown fields {sorted(set(r) - {'req', 'grants', 'lose', 'lrate', 'why'})}")
    print(f"links: {len(TL)} titles")
    TX = getattr(load(sys.argv[3]), "TITLE_TEXT", {})
    for k, r in TX.items():
        if k not in titles: P(f"title text: {k} is not a catalogue title")
        if set(r) - {"needs", "gained", "lost"}: P(f"title text: {k} unknown fields {sorted(set(r) - {'needs', 'gained', 'lost'})}")
        for fld, txt in r.items():
            for b in re.findall(r"\[([^\]]+)\]", txt):
                if b not in ALLN: P(f"title text: {k} {fld} names unknown [{b}]")
            for q in re.findall(r"(?:(?<=^)|(?<=[\s(]))'([^']+)'(?![a-z])", txt):
                if q not in SITS and q not in MARKS: P(f"title text: {k} {fld} quotes '{q}', which is not an Earth situation or mark")
            if not any(f"[{t['name']}]" in txt for t in T): P(f"title text: {k} {fld} names none of this part's perks")
    print(f"title text: {len(TX)} titles")
print("\n".join(prob) if prob else "All checks pass.")
