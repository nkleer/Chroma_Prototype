"""Footprints on the packs' life events (plan.md workstream 3, 10-19; Pathways and packs thread).

PYTHONDONTWRITEBYTECODE=1 python3 -B check_footprint_packs.py [--built DIR] [pack ...]   (default: every pack)

The Library's checker (chroma-library/drafts/check_footprint.py in the shared folder, chroma-library/tests/ on its
branch), read for the packs: the same rules, word for word in check(), with three differences:
  - the moments come from each pack's compiled module: DIR/<pack>.py or DIR/<pack>/<pack>.py when --built is given
    (the Library's build.py run on a copy of the pack's .lib files, which parses foot:), else
    chroma-library/earth_<pack>.py; the foot: fields from the table build.py writes beside it (<module>_foot.py, FOOT
    keyed by (moment, option label): the Engine's 10-19 format, so the moments' file stays byte-identical), and from
    the options themselves for a module built before that;
  - the checked moments are every life event of the pack (its tier: life event);
  - a pack's own titles and perks count as the base ones do (a career, community or faith title or a standing perk is a
    place, an asset a means, a bond a person), and a mark counts as read when a pack's roles.py reads it too.
One difference in the reading: an option that already leaves three or more footprints through its own fields (a
title given, a mark, a career dropped) and has no foot: is listed as left as it is, not as a problem, as the brief says
("If an option already has three or more footprints, leave it as it is and list it"); with a foot: added it stays a
problem. Ends "no problems" (exit 0) or lists them (exit 1). Standard library only; nothing is written.
"""
import collections
import glob
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
sys.path.insert(0, os.path.join(ROOT, "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", ROOT)
from paths import P  # noqa: E402
PACKS = os.environ.get("PACKS_ROOT", P["packs_live"])
LIB = P["library_live"]
RULES = P["engine_live"]
# build.py's MARKS (the shared folder's chroma-library/build.py, 10-19), the marks a .lib may write
MARKS = ["hid a wrong", "owned up", "kept your word", "broke your word", "learned a skill", "took a wild risk",
         "left home", "stayed home", "moved away", "turned down a chance", "helped someone in need",
         "refused someone in need", "made an enemy", "made a friend", "defied an authority", "gave in to pressure",
         "came home", "came out", "kept it hidden", "used drugs", "broke the law", "hurt someone badly", "took a life",
         "named their gender", "took them in"]
PERSON_MARKS = {"made a friend", "made an enemy", "took them in"}
BY_KIND = {"partner": "person", "children": "person", "bond": "person", "community": "place", "career": "place",
           "faith": "place", "standing": "place", "asset": "means"}


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def setup(packs):
    global READ_MARKS, KIND
    txt = "".join(open(os.path.join(RULES, f), encoding="utf-8").read() for f in ("rules_titles.py", "rules_perks.py"))
    txt += "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(f"{PACKS}/*/roles.py")))
    READ_MARKS = {m for m in MARKS if f"'{m}'" in txt}
    base = load(f"{LIB}/earth_perks_titles.py", "base_cat")
    KIND = {t["name"]: t["kind"] for t in base.TITLES}
    KIND.update({p["name"]: p["kind"] for p in base.PERKS})
    for f_ in sorted(glob.glob(f"{PACKS}/*/catalogue.py")) + sorted(glob.glob(f"{PACKS}/core/*.py")):
        m_ = load(f_, "cat_" + f_.replace("/", "_"))
        for x in list(getattr(m_, "TITLES", [])) + list(getattr(m_, "PERKS", [])):
            KIND.setdefault(x["name"], x["kind"])


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
    for k in ("title", "grants", "takes", "drops", "suspends"):
        for x in names(nt.get(k)):
            if BY_KIND.get(KIND.get(x)):
                out.append((BY_KIND[KIND[x]], x))
    for t in tags.split():
        if t.startswith("commit:"):
            out.append(({"partner": "person", "children": "person"}.get(t[7:], "place"), t))
        elif re.match(r"(win|lose|pay):", t):
            out.append(("means", t))
    if nt.get("back"):
        out.append(("door", nt["back"]))
    return out


def feet(o, name, FOOT):
    """The option's foot: items: the FOOT table's, then any left in the option itself (an older build)."""
    nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
    return [tuple(x) for x in FOOT.get((name, o[0]), [])] + [tuple(x) for x in (nt.get("foot") or [])]


def check(names_, src, FOOT):
    problems, kept, dist, kinds = [], [], collections.Counter(), collections.Counter()
    for name in names_:
        s = src.get(name)
        if not s:
            problems.append(f"{name}: not a moment in earth.py")
            continue
        for o in s["options"]:
            where = f"{name} / {o[1]} '{o[0][:50]}'"
            ex = existing(o)
            ft = feet(o, name, FOOT)
            allf = ex + ft
            dist[min(len(allf), 3)] += 1
            for k, _ in allf:
                kinds[k] += 1
            if not allf:
                problems.append(f"{where}: no footprint")
            elif len(allf) > 2:   # the brief: three or more through its own fields, left as it is and listed
                (problems if ft else kept).append(f"{where}: {len(allf)} footprints (at most two): {allf}")
            if any(k == "lesson" for k, _ in ft) and len(allf) > 1:
                problems.append(f"{where}: a lesson only when nothing else fits: {allf}")
            for k, v in ft:
                if k == "mark" and v not in READ_MARKS:
                    problems.append(f"{where}: foot: mark '{v}' is a mark no title or perk rule reads")
                if k == "mark" and v in PERSON_MARKS:
                    problems.append(f"{where}: foot: mark '{v}' is a person; write foot: person friend (or rival)")
                if (k, v) in ex or (k == "mark" and (o[5] or {}).get("mark") == v) or \
                        (k == "door" and (o[5] or {}).get("back") == v):
                    problems.append(f"{where}: foot: {k} {v} repeats what the option already leaves")
        les = [v for o in s["options"] for k, v in feet(o, name, FOOT) if k == "lesson"]
        if len(les) * 5 > len(s["options"]):   # Vision 10-19: lessons are the weakest footprint, 1 in 5 or fewer a moment
            problems.append(f"{name}: {len(les)} of {len(s['options'])} options have only a lesson (at most 1 in 5)")
        if len(set(les)) < len(les):
            problems.append(f"{name}: two options teach the same lesson words")
    return problems, kept, dist, kinds


def main():
    a = sys.argv[1:]
    built = a[a.index("--built") + 1] if "--built" in a else None
    packs = [x for i, x in enumerate(a) if x != "--built" and (i == 0 or a[i - 1] != "--built")]
    packs = packs or sorted(os.path.basename(os.path.dirname(f)) for f in glob.glob(f"{PACKS}/*/catalogue.py"))
    setup(packs)
    bad = 0
    for pk in packs:
        f_ = os.path.join(LIB, f"earth_{pk}.py")
        if built:   # DIR/<pack>.py, or DIR/<pack>/<pack>.py where build.py wrote it beside the pack's .lib copies
            f_ = next((x for x in (os.path.join(built, f"{pk}.py"), os.path.join(built, pk, f"{pk}.py"))
                       if os.path.exists(x)), os.path.join(built, f"{pk}.py"))
        if not os.path.exists(f_):   # a pack not yet built (one not in batch.PACKS has no earth_<pack>.py): build it first
            print(f"{pk}: no compiled moments at {os.path.relpath(f_, ROOT) if f_.startswith(ROOT) else f_}; "
                  f"build its .lib files and pass --built")
            continue
        M = load(f_, f"moments_{pk}")
        ff = f_[:-3] + "_foot.py"
        FOOT = load(ff, f"foot_{pk}").FOOT if os.path.exists(ff) else {}
        src = {s["name"]: s for s in M.SITUATIONS}
        listed = [s["name"] for s in M.SITUATIONS if s.get("tier") == "life event"]
        problems, kept, dist, kinds = check(listed, src, FOOT)
        n = sum(dist.values())
        print(f"{pk} ({os.path.relpath(f_, ROOT) if f_.startswith(ROOT) else f_}): {len(listed)} life events, {n} options; "
              f"with 0/1/2/3+ footprints: {dist[0]}/{dist[1]}/{dist[2]}/{dist[3]}; by kind: {dict(kinds.most_common())}")
        for p_ in problems:
            print("  " + p_)
        if kept:
            print(f"  left as they are (three or more footprints through their own fields, no foot:): {len(kept)}")
            for k_ in kept:
                print("    " + k_)
        bad += len(problems)
    print(f"{bad} problems" if bad else "no problems")
    sys.exit(1 if bad else 0)


main()
