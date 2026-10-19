"""Bold ways (2026-10-18): checks the Library's BOLD table and LINKS in earth_play.py against the design
(chroma-ideas/gameplay-2026-10-17/bold-ways.md).

    python3 -B check_bold.py [library folder] [--stage1 bold-stage1-moments.txt] [--quiet] [--part]

The library folder holds earth.py, earth_play.py and earth_perks_titles.py (default: the folder above this one).
Problems end the run with exit code 1; notes are printed and do not fail it. --part checks one writer's part: the colour
shares are printed, not held to the band.

What it checks, on every bold way (first and second ways of life events, and each link's own bold way):
- names: every title, perk and kind in its act fields, requires: and likelier_if: is in the catalogue; marks are
  marks the Library uses;
- a lasting win on success (title: or grants:, or drops: of a status title) and a lasting cost on failure
  (title_if_fails:, takes_if_fails:, drops_if_fails: or suspends_if_fails:), never money or a bond alone;
- steps: a title won names the rung below its needs in requires: (or needs nothing in brackets);
- odds: chance 25 to 50; likelier_if: adds at most 30, so their own odds stay inside 10 to 90;
- safety: no death_if_fails, kills, kills_if_fails or heavy injury; on moments open to children under 12, costs are
  mild (a community place, or a skill, standing or bond perk), never a record, a job, a partner or a faith role;
- colours: each colour holds 20% +- 4 points of all bold ways, with its mean chance within 3 points of the whole;
- text: timeless (no years, currencies or brand-like capitals in the outcome lines), and no colour words in labels.
- open rows, on life events: no requires:, one win and one cost, and what it gives held at all the moment's ages
  (the Engine offers a bold way only when its win is not held, its cost is held and its gains fit the age).
On links: each first bold way of a life event has a well link and a badly link (moments only for those under 18: the
well link only), one link deep, with delay 1 to 3 years and the root moment's people.
"""
import os
import re
import sys
import importlib.util
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:]]
quiet = "--quiet" in args
part = "--part" in args
stage1 = args[args.index("--stage1") + 1] if "--stage1" in args else None
args = [a for i, a in enumerate(args) if a not in ("--quiet", "--stage1", "--part") and (i == 0 or args[i - 1] != "--stage1")]
LIB = os.path.abspath(args[0]) if args else os.path.dirname(HERE)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(LIB, f"{name}.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


earth, play, cat = load("earth"), load("earth_play"), load("earth_perks_titles")
BOLD, LINKS = getattr(play, "BOLD", {}), getattr(play, "LINKS", [])
TITLES = {x["name"]: x for x in cat.TITLES}
PERKS = {x["name"]: x for x in cat.PERKS}
ITEMS = {**TITLES, **PERKS}
KINDS = ["career", "partner", "children", "community", "faith", "status"]
MOMENTS = {d["name"]: d for d in earth.SITUATIONS if d.get("tier") == "life event"}
LINKM = {d["name"]: d for d in LINKS}
MARKS = {o[5][k] for d in earth.SITUATIONS + getattr(earth, "ECHOES", []) + getattr(earth, "RETURNS", [])
         for o in d["options"] for k in ("mark", "back") if len(o) > 5 and o[5].get(k)}
WIN_OPS, COST_OPS = ("title", "grants"), ("title_if_fails", "takes_if_fails", "drops_if_fails", "suspends_if_fails")
ACT_KEYS = ("title", "drops", "grants", "takes", "suspends")
MILD_PERKS = ("skill", "standing", "bond")
COLOR_WORDS = re.compile(r"\b(white|blue|black|red|green)\b", re.I)
UNTIMELY = re.compile(r"\b(1[89]\d\d|20\d\d)\b|[$€£¥]|\b(dollars?|euros?|pounds sterling|yen)\b", re.I)

problems, notes = [], []


def names(v):
    return [x.strip() for x in str(v or "").split(";") if x.strip()]


def bracket_needs(item):
    """The titles and perks an item's needs: text names in brackets, without the ones after 'not'."""
    txt = item.get("needs", "") or ""
    return [m.group(2) for m in re.finditer(r"(\bnot\s+)?\[([^\]]+)\]", txt) if not m.group(1) and m.group(2) in ITEMS]


LIKELIER = re.compile(r"(has|years|mark)\s+(?:\[([^\]]+)\]|'([^']+)')\s*(\d+(?:\.\d+)?)?\s*\+(\d+)")


def likelier(r):
    """A row's likelier_if: as [(kind, name, years or None, points)]; build.py has already checked its form."""
    out = []
    for bit in [b.strip() for b in str(r.get("likelier_if") or "").split(";") if b.strip()]:
        m = LIKELIER.fullmatch(bit)
        if m:
            out.append((m.group(1), m.group(2) or m.group(3), float(m.group(4)) if m.group(4) else None, int(m.group(5))))
        else:
            problems.append(f"likelier_if: cannot read '{bit}'")
    return out


def check_way(where, r, moment):
    o = r["option"]
    nt, label = o[5], o[0]
    lo = moment["age"][0]
    # names
    for k in [x for op in ACT_KEYS for x in (op, op + "_if_fails")] + ["requires"]:
        for nm in names(nt.get(k)):
            if nm.startswith("kind:"):
                if nm[5:].strip() not in KINDS:
                    problems.append(f"{where}: {k}: '{nm}' is not a kind ({', '.join(KINDS)})")
                elif k in ("title", "grants"):
                    problems.append(f"{where}: {k}: a kind can be dropped, not given")
            elif nm not in ITEMS:
                problems.append(f"{where}: {k}: '{nm}' is not a title or perk")
    for kind, nm, yrs, pts in likelier(r):
        if kind in ("has", "years") and nm not in ITEMS:
            problems.append(f"{where}: likelier_if: '{nm}' is not a title or perk")
        if kind == "mark" and nm not in MARKS:
            problems.append(f"{where}: likelier_if: mark '{nm}' is not a mark the Library uses")
    if nt.get("mark") and nt["mark"] not in MARKS:
        notes.append(f"{where}: new mark '{nt['mark']}'")
    # a lasting win and a lasting cost
    wins = [(k, nm) for k in WIN_OPS for nm in names(nt.get(k))]
    wins += [("drops", nm) for nm in names(nt.get("drops")) if TITLES.get(nm, {}).get("kind") == "status"]
    costs = [(k, nm) for k in COST_OPS for nm in names(nt.get(k))]
    if not wins:
        problems.append(f"{where}: no lasting win (title: or grants:)")
    if not costs:
        problems.append(f"{where}: no lasting cost on failure ({', '.join(COST_OPS)})")
    held = set(names(nt.get("requires"))) | set(names(moment.get("requires")))
    base_gives = set(names(moment["options"][r["base_index"]][5].get("title"))) if moment.get("options") else set()
    for k, nm in costs:
        if k in ("takes_if_fails", "suspends_if_fails", "drops_if_fails") and not nm.startswith("kind:") \
                and nm not in held and nm != "{title}":
            notes.append(f"{where}: {k}: '{nm}' is lost only by those who hold it (not in requires:)")
    # steps: a title won names its rung below in requires:, unless it needs none or the base way gives it too (the
    # wedding's newlywed: the Engine holds a facet until the title it refines comes)
    for k, nm in wins:
        if k == "title" and nm in TITLES and nm not in base_gives:
            need = bracket_needs(TITLES[nm])
            if need and not (set(need) & held):
                problems.append(f"{where}: title: '{nm}' needs {' or '.join('[' + x + ']' for x in need)} first; "
                                "put the rung below in requires:")
            a, b = TITLES[nm].get("ages", (0, 200))
            if moment["age"][1] < a or moment["age"][0] > b:
                problems.append(f"{where}: title: '{nm}' is held at {a}-{b}, outside the moment's ages {moment['age']}")
    # open rows (10-19, Gameplay): a life event's bold way is offered only when its win can be won and its cost can be
    # paid (the Engine's gate), so it asks for nothing held, wins one thing and costs one thing, at all the moment's ages
    if moment.get("tier") == "life event":
        if names(nt.get("requires")):
            problems.append(f"{where}: an open row takes no requires: ({nt['requires']}); win what needs no rung, cost what most hold")
        if len([w for w in wins if w[1] not in base_gives]) > 1 or len(costs) > 1:   # (the wedding's newlywed is the base way's)
            problems.append(f"{where}: an open row wins one thing and costs one thing, not {wins} and {costs}")
        hi_ = min(moment["age"][1], 80)   # (a status cost such as out of work keeps its own ages: no job to lose after them)
        for k, nm in [(k, nm) for k in ("title", "grants") for nm in names(nt.get(k))]:
            a, b = ITEMS.get(nm, {}).get("ages", (0, 200))
            if a > moment["age"][0] + 2 or b < hi_:
                problems.append(f"{where}: {k}: '{nm}' is held at {a}-{b}, so the way is not offered at all of the "
                                f"moment's ages {moment['age']}")
    # odds
    c = nt.get("chance")
    if c is None or not 0.25 <= c <= 0.5:
        problems.append(f"{where}: chance {c} is outside 25 to 50")
    up = sum(x[3] for x in likelier(r))
    if c is not None and not 0.10 <= c + up / 100 <= 0.90:
        problems.append(f"{where}: likelier_if takes their odds to {c + up / 100:.0%}, outside 10 to 90")
    # safety
    for k in ("death_if_fails", "kills", "kills_if_fails"):
        if k in nt:
            problems.append(f"{where}: a bold way never carries {k}:")
    if nt.get("injury") == "heavy":
        problems.append(f"{where}: a bold way carries no heavy injury")
    if lo < 12:
        for k, nm in costs:
            item = ITEMS.get(nm, {})
            mild = (k in ("takes_if_fails", "drops_if_fails") and (nm == "kind:community" or item.get("kind") == "community"
                    or (nm in PERKS and item.get("kind") in MILD_PERKS)))
            if not mild:
                problems.append(f"{where}: the moment is open to children under 12, so its cost must be mild, not {k}: {nm}")
    # text
    if COLOR_WORDS.search(label):
        problems.append(f"{where}: label uses a colour word: '{label}'")
    for t in [label, nt.get("act", "")] + list(r["works"]) + list(r["fails"]):
        if UNTIMELY.search(t or ""):
            problems.append(f"{where}: not timeless: '{t[:60]}'")
        if re.search(r"\b(you|your|yours|yourself)\b", t or "", re.I) and t is not label:
            problems.append(f"{where}: third person only: '{t[:60]}'")
    if not all(r.get("change", {}).get(k) for k in ("well", "badly")) or "?" in str(r.get("change")):
        problems.append(f"{where}: no kind of change for the shared links: {r.get('change')}")
    if label.split()[0].lower() in ("i", "we"):
        problems.append(f"{where}: label speaks as the character: '{label}'")


all_ways = []
for mom, rows in BOLD.items():
    m = MOMENTS.get(mom) or LINKM.get(mom)
    if m is None:
        problems.append(f"bold: {mom}: not a life event or a link")
        continue
    for i, r in enumerate(rows):
        where = f"bold: {mom} / {r['colour']}"
        check_way(where, r, m)
        all_ways.append((mom in LINKM, i, r))

# links: a well and a badly link for each first bold way of a life event; one link deep; the root's people
by_root = defaultdict(set)
for d in LINKS:
    if d.get("of_bold"):
        mom, col = d["of_bold"].rsplit(" / ", 1)
        by_root[(mom, col)].add(d["side"])
        root = MOMENTS.get(mom)
        if root is None:
            problems.append(f"{d['name']}: of_bold: '{mom}' is not a life event")
            continue
        rroles = {x.strip().lower() for x in root.get("roles", "").split(",")}
        for slot in set(re.findall(r"\{(\w+)\}", " ".join(t for sc in d.get("scenes", {}).values() for _, t, *_ in sc))):
            if slot not in ("N", "Ns", "title", "place", "dead") and slot not in rroles:
                notes.append(f"{d['name']}: {{{slot}}} is not among the root moment's roles ({root.get('roles')})")
        if not d.get("scenes_gone"):
            problems.append(f"{d['name']}: no scene gone line")
        PSLOT = re.compile(r"\{(" + "|".join(sorted(rroles | {"friend", "rival", "partner", "prospect", "sibling", "colleague",
                           "boss", "mentor", "parent", "child", "grandparent", "elder"})) + r")\}")
        if any(PSLOT.search(t) for t in d["outcomes"][0] + d["outcomes"][1]) and not d.get("outcomes_gone"):
            problems.append(f"{d['name']}: its outcome lines name the root's person, so it needs works gone / fails gone lines")
        for r in BOLD.get(d["name"], []):
            if any(PSLOT.search(t) for t in r["works"] + r["fails"]) and not r.get("works_gone"):
                problems.append(f"bold: {d['name']} / {r['colour']}: its lines name the root's person, so it needs works gone / "
                                "fails gone lines")
        if d["name"] not in BOLD:
            problems.append(f"{d['name']}: a link carries its own bold way")
        if root["age"][1] < 18 and d["side"] == "badly":
            problems.append(f"{d['name']}: a moment only for those under 18 keeps the win link only")
for mom, rows in BOLD.items():
    if mom in MOMENTS and rows:
        first = rows[0]
        want = {"well"} if MOMENTS[mom]["age"][1] < 18 else {"well", "badly"}
        got = by_root.get((mom, first["colour"]), set())
        if want - got:
            problems.append(f"bold: {mom} / {first['colour']}: no {' and no '.join(sorted(want - got))} link")
        for r in rows[1:]:
            if by_root.get((mom, r["colour"])):
                problems.append(f"bold: {mom} / {r['colour']}: chains go on first bold ways only")

# colours, over all bold ways together
if all_ways and not part:
    n = len(all_ways)
    cnt = Counter(r["colour"] for _, _, r in all_ways)
    mean = sum(r["option"][5]["chance"] for _, _, r in all_ways) / n
    for c in "WUBRG":
        share = cnt[c] / n
        rs = [r["option"][5]["chance"] for _, _, r in all_ways if r["colour"] == c]
        cm = sum(rs) / len(rs) if rs else 0
        if abs(share - 0.2) > 0.04:
            problems.append(f"colours: {c} holds {share:.0%} of {n} bold ways (20% +- 4)")
        if rs and abs(cm - mean) > 0.03:
            problems.append(f"colours: {c}'s mean chance {cm:.0%} is more than 3 points from {mean:.0%}")

if stage1:
    want = [l.split("\t")[1].strip() for l in open(stage1) if l.strip() and not l.startswith("#")]
    miss = [w for w in want if w not in BOLD]
    if miss:
        problems.append(f"stage 1: {len(miss)} of {len(want)} moments have no bold way: {', '.join(miss[:8])}"
                        + (" ..." if len(miss) > 8 else ""))

firsts = sum(1 for lk, i, _ in all_ways if not lk and i == 0)
seconds = sum(1 for lk, i, _ in all_ways if not lk and i > 0)
links_b = sum(1 for lk, _, _ in all_ways if lk)
cnt = Counter(r["colour"] for _, _, r in all_ways)
print(f"bold ways: {len(all_ways)} ({firsts} first, {seconds} second, {links_b} on links) on {len(BOLD)} moments; "
      f"{len(LINKS)} links; colours " + " ".join(f"{c} {cnt[c]}" for c in "WUBRG"))
if notes and not quiet:
    print(f"{len(notes)} notes:")
    for x in notes:
        print("  ~", x)
if problems:
    print(f"{len(problems)} problems:")
    for x in problems:
        print("  -", x)
    sys.exit(1)
print("no problems")
