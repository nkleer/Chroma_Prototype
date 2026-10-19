"""Footprints (plan.md workstream 3, 10-19): every option of a checked moment leaves one or two things the player can see.
python3 -B tests/check_footprint.py [chroma-library dir]        prints a summary and ends "no problems" or lists them
python3 -B tests/check_footprint.py . --all                     also counts every life event (a report, not checked)
The checked moments are named in footprint_moments.txt, one per line (every Earth life event; the 80 with pictures first).
A footprint is one of: person, place, means, mark, door, lesson. Existing fields count as they are read today:
    person  mark: made a friend / made an enemy / took them in; bond:, break:, mend:, secret:, trust:; a partner or
            children title; commit:partner, commit:children
    place   commit:community / career / faith; a community, career, faith or standing title or perk
    means   tags win: / lose: / pay:; an asset perk
    mark    mark: a mark some title or perk rule reads (chroma-engine/v22-speedpass/rules_titles.py, rules_perks.py),
            or one of footprint_names.MARKS_WIRED (read by the engine's people and world code)
    door    back: <seed kind>
and foot: adds the rest (compiled to earth_foot.py's FOOT; read only with the engine's foot_on switch). Rules:
    one or two footprints an option; a lesson only when nothing else fits, on 1 option in 5 or fewer a moment, each
    in its own words; foot: mark only a mark a rule reads;
    foot: never repeats what an existing field already leaves.
"""
import collections, os, re, sys
sys.dont_write_bytecode = True

LIB = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
sys.path.insert(0, LIB)
import earth, earth_perks_titles as ept
from earth_foot import FOOT   # foot: compiled to its own table (Engine 10-19), so earth.py stays byte-identical

ROOT = os.path.dirname(LIB)
RULES = os.path.join(ROOT, "chroma-engine", "v22-speedpass")
txt = "".join(open(os.path.join(RULES, f), encoding="utf-8").read() for f in ("rules_titles.py", "rules_perks.py"))
PERSON_MARKS = {"made a friend", "made an enemy", "took them in"}
READ_MARKS = {m for m in earth.MARKS if f"'{m}'" in txt} if isinstance(earth.MARKS, (list, tuple, set)) and earth.MARKS \
    else None
if not READ_MARKS:
    import build   # the mark list lives in build.py when earth.MARKS is empty
    READ_MARKS = {m for m in build.MARKS if f"'{m}'" in txt}
from footprint_names import MARKS_WIRED   # Library 10-19: marks the engine's people and world code answers
READ_MARKS |= set(MARKS_WIRED)
KIND = {t["name"]: t["kind"] for t in ept.TITLES}
KIND.update({p["name"]: p["kind"] for p in ept.PERKS})
BY_KIND = {"partner": "person", "children": "person", "bond": "person", "community": "place", "career": "place",
           "faith": "place", "standing": "place", "asset": "means"}


def names(v):
    return [x.strip() for x in re.split(r"[;,]", v) if x.strip()] if isinstance(v, str) else list(v or [])


def existing(o):
    """The footprints an option already leaves through today's fields, as (kind, what)."""
    tags = str(o[4] or "")
    nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
    out = []
    m = nt.get("mark")
    if m in PERSON_MARKS:
        out.append(("person", m))
    elif m in READ_MARKS:
        out.append(("mark", m))
    for k in ("bond", "break", "mend", "secret", "trust"):
        if nt.get(k):
            out.append(("person", f"{k}: {nt[k]}"))
    commits = {t[7:] for t in tags.split() if t.startswith("commit:")}
    for k in ("title", "grants", "takes", "drops", "suspends"):
        for x in names(nt.get(k)):
            if BY_KIND.get(KIND.get(x)) and not (k == "title" and KIND[x] in commits):   # the commitment's own title
                out.append((BY_KIND[KIND[x]], x))                                       # and its commit: count once
    for t in tags.split():
        if t.startswith("commit:"):
            out.append(({"partner": "person", "children": "person"}.get(t[7:], "place"), t))
        elif re.match(r"(win|lose|pay):", t):
            out.append(("means", t))
    if nt.get("back"):
        out.append(("door", nt["back"]))
    return out


def check(names_, src):
    problems, dist, kinds = [], collections.Counter(), collections.Counter()
    for name in names_:
        s = src.get(name)
        if not s:
            problems.append(f"{name}: not a moment in earth.py")
            continue
        for o in s["options"]:
            where = f"{name} / {o[1]} '{o[0][:50]}'"
            ex = existing(o)
            ft = list(FOOT.get((name, o[0]), []))
            allf = ex + ft
            dist[min(len(allf), 3)] += 1
            for k, _ in allf:
                kinds[k] += 1
            if not allf:
                problems.append(f"{where}: no footprint")
            elif len(allf) > 2:
                problems.append(f"{where}: {len(allf)} footprints (at most two): {allf}")
            if any(k == "lesson" for k, _ in ft) and len(allf) > 1:
                problems.append(f"{where}: a lesson only when nothing else fits: {allf}")
            for k, v in ft:
                if k == "mark" and v not in READ_MARKS:
                    problems.append(f"{where}: foot: mark '{v}' is a mark nothing in the life answers")
                if k == "mark" and v in PERSON_MARKS:
                    problems.append(f"{where}: foot: mark '{v}' is a person; write foot: person friend (or rival)")
                if (k, v) in ex or (k == "mark" and (o[5] or {}).get("mark") == v) or \
                        (k == "door" and (o[5] or {}).get("back") == v):
                    problems.append(f"{where}: foot: {k} {v} repeats what the option already leaves")
        les = [v for o in s["options"] for k, v in FOOT.get((name, o[0]), []) if k == "lesson"]
        if len(les) * 5 > len(s["options"]):   # Vision 10-19: lessons are the weakest footprint, 1 in 5 or fewer a moment
            problems.append(f"{name}: {len(les)} of {len(s['options'])} options have only a lesson (at most 1 in 5)")
        if len(set(les)) < len(les):
            problems.append(f"{name}: two options teach the same lesson words")
    return problems, dist, kinds


def main():
    src = {s["name"]: s for s in earth.SITUATIONS}
    listed = [ln.strip() for ln in open(os.path.join(LIB, "footprint_moments.txt"), encoding="utf-8")
              if ln.strip() and not ln.startswith("#")]
    problems, dist, kinds = check(listed, src)
    n = sum(dist.values())
    print(f"footprints: {len(listed)} moments, {n} options; with 0/1/2/3+ footprints: "
          f"{dist[0]}/{dist[1]}/{dist[2]}/{dist[3]}; by kind: {dict(kinds.most_common())}")
    if "--all" in sys.argv:
        le = [s["name"] for s in earth.SITUATIONS if s.get("tier") == "life event"]
        _, d2, k2 = check(le, src)
        print(f"all life events (report only): {len(le)} moments, {sum(d2.values())} options; 0/1/2/3+: "
              f"{d2[0]}/{d2[1]}/{d2[2]}/{d2[3]}; by kind: {dict(k2.most_common())}")
    try:
        for p in problems:
            print("  " + p)
    except BrokenPipeError:
        pass
    print(f"{len(problems)} problems" if problems else "no problems")
    sys.exit(1 if problems else 0)


main()
