"""Check the packs' aim fields (aims version 2; Pathways and packs thread, 2026-10-23).

PYTHONDONTWRITEBYTECODE=1 python3 -B check_fields.py [pack ...]     (default: every pack with a fields.py)

The format is the Engine's frozen aims shape (chroma-engine/notes/v25/aims-shape.md in the shared folder, sections 2
and 3, after Emren's decision #9): a pack's fields.py holds FIELDS_<PACK>, a dict {aim: field}. A field turns one of
the pack's aims (aims.py, aims version 1) into a ladder shape with a clock on every rung, so every v1 aim of the pack
has a field of the same name, and its rungs keep v1's say, any, req and height. A pack with no aims.py (national) has
fields of its own. Reports:
  1. keys and values: every key of the shape and nothing else, every name a catalogue name, every dream a dream
     (chroma-library/dreams.py, or the packs' new dreams in a pack's dreams.py), haunts from the engine's HAUNT_KINDS,
     the shape's rung count (rungs plus skip), years as (median, 10th, 90th percentile), demand and window in range;
  2. v1 kept: name, face, sphere, domain, dreams (v1's, a field may add), tribal, magic, and each rung's say, any, req
     and height;
  3. first ages (C-X4, the engine never gives a title outside its catalogue ages=): per rung, the youngest age any
     name in `any` can be held, and rung 1's start ages against it;
  4. the clock: medians summed to the Known rung and to the top, and the shares multiplied (who of those who start
     and keep at it reach Known and the top);
  5. ways in: the pack's own moments that grant a rung's names (title:, grants:, aims: on an option), counted per rung;
     the Library's shape moments add the shape's practice, contest, chance and mentor moments to every rung, so a
     rung with none of the pack's own is not a problem, only listed.
Standard library only; nothing is written.
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
COLORS = "WUBRG"
SHAPES = {"competition": 5, "craft": 5, "art": 5, "knowledge": 5, "career": 5, "cause": 5, "home": 4, "land": 5,
          "faith": 5, "venture": 4}   # land: 5 rungs asked of the Engine 10-23 (3 in aims-shape.md 10-21)
DOMAINS = {"career", "partner", "children", "community", "faith", ""}
SPHERES = {"comm", "gather", "care", "learn", "prot", "prod", "rule", "faith", "arts", ""}
HEIGHTS = ["Known", "Notable", "Historic"]
ROLES = {"coach", "rival", "peer", "patron"}
FORKS = {"go_on", "pay", "take", "round"}
NEEDS = {"safety", "belonging", "autonomy", "competence", "meaning"}
UPKEEP_OF = {"proficiency", "access", "credential"}
WINDOW = {"every", "open_weeks", "deadline_age", "deadline_years", "pause_stops"}
FIELD_KEYS = {"shape", "face", "sphere", "domain", "dreams", "calling", "thing", "doing", "contest", "places", "people",
              "round", "below", "tribal", "magic", "rungs", "skip", "prep", "meets"}
RUNG_KEYS = {"say", "any", "req", "height", "years", "share", "start", "contests_y", "forks", "time", "demand",
             "window", "upkeep"}
COND = re.compile(r"\b(has|was|yrs_has)\((['\"])(.+?)\2\)")


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def haunts():
    src = open(os.path.join(P["engine_live"], "world_keys.py"), encoding="utf-8").read()
    m = re.search(r"^HAUNT_KINDS = \[(.*?)\]", src, re.S | re.M)
    return set(re.findall(r'"([a-z]+\.[a-z]+)"', m.group(1)))


def catalogue():
    """name -> youngest age it can be held (catalogue ages=; 0 for a perk or a name with none)."""
    ages = {}
    base = load(f"{LIB}/earth_perks_titles.py", "base_cat")
    items = list(base.TITLES) + list(base.PERKS)
    for f_ in sorted(glob.glob(f"{PACKS}/*/catalogue.py")):
        m_ = load(f_, "cat_" + os.path.basename(os.path.dirname(f_)))
        items += list(m_.TITLES) + list(getattr(m_, "PERKS", []))
    for f_ in sorted(glob.glob(f"{PACKS}/core/*.py")):
        m_ = load(f_, "core_" + os.path.basename(f_)[:-3])
        for k_ in ("PERKS", "TITLES", "PERKS_AIMS", "TITLES_AIMS"):
            items += list(getattr(m_, k_, []))
    for x in items:
        a = x.get("ages")
        ages.setdefault(x["name"], a[0] if isinstance(a, (tuple, list)) and a else 0)
    return ages


def dreams():
    d = load(f"{LIB}/dreams.py", "lib_dreams")
    out = {x["name"] for x in list(d.DREAMS) + list(getattr(d, "DREAMS_MORE", []))}
    for f_ in sorted(glob.glob(f"{PACKS}/*/dreams.py")):
        m_ = load(f_, "dreams_" + os.path.basename(os.path.dirname(f_)))
        out |= {x["name"] for x in getattr(m_, "DREAMS_PACKS", [])}
    return out


def doors(pk, names):
    """The pack's own moments that grant a name: name -> [moment, ...] (title:, grants:, aims: on an option)."""
    out = collections.defaultdict(set)
    for f_ in sorted(glob.glob(f"{PACKS}/{pk}/*.lib")):
        cur = None
        for ln in open(f_, encoding="utf-8"):
            if ln.startswith("== "):
                cur = ln[3:].strip()
            elif cur and re.match(r"- [WUBRG>.0-9 ]+\|", ln):
                for part in ln.split("|")[2:]:
                    k, _, v = part.partition(":")
                    if k.strip() in ("title", "grants", "aims"):
                        for x in re.split(r"[;,]", v):
                            if x.strip() in names:
                                out[x.strip()].add(cur)
    return out


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def check_cond(where, cond, names, prob):
    if cond.count("(") != cond.count(")"):
        prob.append(f"{where}: unbalanced parentheses in req")
    for _, _, nm in COND.findall(cond):
        if nm not in names:
            prob.append(f"{where}: req names {nm!r}, not a catalogue name")


def check_field(pk, aim, f, v1, ages, drm, hk, prob, notes, dr):
    w = f"{pk}: {aim!r}"
    unknown = set(f) - FIELD_KEYS
    if unknown:
        prob.append(f"{w}: unknown keys {sorted(unknown)}")
    for k in ("shape", "face", "sphere", "domain", "dreams", "calling", "thing", "doing", "contest", "places",
              "people", "round", "below", "tribal", "magic", "rungs"):
        if k not in f:
            prob.append(f"{w}: no {k}")
    sh = f.get("shape")
    if sh not in SHAPES:
        prob.append(f"{w}: shape {sh!r}")
    face = str(f.get("face", "")).split()
    if not (1 <= len(face) <= 2) or any(c not in COLORS for c in face):
        prob.append(f"{w}: face {f.get('face')!r}")
    if f.get("domain") not in DOMAINS:
        prob.append(f"{w}: domain {f.get('domain')!r}")
    if f.get("sphere", "") not in SPHERES:
        prob.append(f"{w}: sphere {f.get('sphere')!r}")
    if not isinstance(f.get("calling"), bool):
        prob.append(f"{w}: calling is not True or False")
    for x in f.get("dreams", []):
        if x not in drm:
            prob.append(f"{w}: dream {x!r} is in no dreams list")
    if not f.get("dreams"):
        notes.append(f"{w}: no dream")
    for k in ("thing", "doing", "contest", "below", "tribal", "magic"):
        if not isinstance(f.get(k), str) or not f.get(k, "").strip():
            prob.append(f"{w}: {k} is not words")
    for x in f.get("places", []):
        if x not in hk:
            prob.append(f"{w}: place {x!r} is not a haunt kind")
    if not 1 <= len(f.get("places", [])) <= 3:
        prob.append(f"{w}: {len(f.get('places', []))} places (1 to 3)")
    pe = f.get("people", {})
    if not isinstance(pe, dict) or not pe or set(pe) - ROLES:
        prob.append(f"{w}: people {sorted(pe) if isinstance(pe, dict) else pe!r} (a dict of coach, rival, peer, patron)")
    if not isinstance(f.get("round"), list) or not 2 <= len(f.get("round", [])) <= 3:
        prob.append(f"{w}: round is not a list of 2 or 3 ways")
    for x in f.get("meets", []):
        if x not in NEEDS:
            prob.append(f"{w}: meets {x!r}")
    if not isinstance(f.get("prep", []), list):
        prob.append(f"{w}: prep is not a list")
    R = f.get("rungs", [])
    skip = f.get("skip", [])
    if sh in SHAPES and len(R) + len(skip) != SHAPES[sh]:
        prob.append(f"{w}: {len(R)} rungs and {len(skip)} skipped, the {sh} shape has {SHAPES[sh]}")
    if not 3 <= len(R) <= 5:
        prob.append(f"{w}: {len(R)} rungs (3 to 5)")
    if v1 is not None:
        for k in ("face", "sphere", "domain", "tribal", "magic"):
            if f.get(k) != v1.get(k):
                prob.append(f"{w}: {k} {f.get(k)!r} is not v1's {v1.get(k)!r}")
        miss = [x for x in v1.get("dreams", []) if x not in f.get("dreams", [])]
        if miss:
            prob.append(f"{w}: v1's dreams {miss} left out")
        if len(R) != len(v1.get("steps", [])):
            prob.append(f"{w}: {len(R)} rungs, v1 has {len(v1.get('steps', []))} steps")
    last, med, shr, tops = -1, 0.0, 1.0, {}
    for i, r in enumerate(R):
        ws = f"{w} rung {i + 1}"
        unknown = set(r) - RUNG_KEYS
        if unknown:
            prob.append(f"{ws}: unknown keys {sorted(unknown)}")
        if v1 is not None and i < len(v1.get("steps", [])):
            s = v1["steps"][i]
            for k in ("say", "any", "req", "height"):
                if r.get(k) != s.get(k):
                    prob.append(f"{ws}: {k} {r.get(k)!r} is not v1's {s.get(k)!r}")
        for x in r.get("any", []):
            if x not in ages:
                prob.append(f"{ws}: {x!r} is not a catalogue name")
        if not r.get("any"):
            prob.append(f"{ws}: no names in any")
        if r.get("req"):
            check_cond(ws, r["req"], ages, prob)
        h = r.get("height")
        if h is not None:
            if h not in HEIGHTS or HEIGHTS.index(h) <= last:
                prob.append(f"{ws}: height {h!r}")
            else:
                last = HEIGHTS.index(h)
        y = r.get("years")
        tm = bool(r.get("time"))
        if not (isinstance(y, (tuple, list)) and len(y) == 3 and all(num(v) for v in y) and y[1] <= y[0] <= y[2]
                and y[1] >= 0):
            prob.append(f"{ws}: years {y!r} is not (median, low, high)")
        else:
            med += y[0]
        s_ = r.get("share")
        if not (num(s_) and 0 < s_ <= 1):
            prob.append(f"{ws}: share {s_!r}")
        else:
            shr *= s_
        if h:
            tops[h] = (med, shr)
        st = r.get("start")
        if i == 0:
            if not (isinstance(st, (tuple, list)) and len(st) == 3 and st[0] <= st[1] <= st[2]):
                prob.append(f"{ws}: start {st!r} is not (from, best_to, late_from)")
        elif st is not None:
            prob.append(f"{ws}: start on a rung after the first")
        if not (num(r.get("contests_y")) and r["contests_y"] >= 0):
            prob.append(f"{ws}: contests_y {r.get('contests_y')!r}")
        fk = r.get("forks", [])
        if tm:
            if fk or r.get("contests_y"):
                prob.append(f"{ws}: a rung with time has forks or contests")
        elif not (1 <= len(fk) <= 2) or set(fk) - FORKS:
            prob.append(f"{ws}: forks {fk!r} (one or two of {sorted(FORKS)})")
        d = r.get("demand")
        if not tm:
            if not (isinstance(d, dict) and set(d) == {"hours", "money", "entry", "energy"} and
                    all(num(v) for v in d.values()) and 0 <= d["hours"] <= 60 and
                    all(0 <= d[k] <= 1 for k in ("money", "entry", "energy"))):
                prob.append(f"{ws}: demand {d!r} (dict of hours 0-60, money, entry and energy 0-1)")
        wn = r.get("window")
        if wn is not None and (not isinstance(wn, dict) or set(wn) - WINDOW or not wn):
            prob.append(f"{ws}: window {wn!r} (None or a dict of {sorted(WINDOW)})")
        up = r.get("upkeep")
        if up is not None and (not isinstance(up, dict) or up.get("of") not in UPKEEP_OF or not num(up.get("years"))
                               or not isinstance(up.get("kept_by"), list) or set(up) - {"of", "years", "kept_by"}):
            prob.append(f"{ws}: upkeep {up!r} (None or dict(of, years, kept_by))")
        fa = min((ages.get(x, 0) for x in r.get("any", [])), default=0)
        n_d = sorted({m for x in r.get("any", []) for m in dr.get(x, ())})
        notes.append(f"{ws} {r.get('say', '')!r}: first age {fa}; "
                     f"{len(n_d)} pack moment(s) grant it" + (f" ({'; '.join(n_d[:4])}{' ...' if len(n_d) > 4 else ''})"
                                                              if n_d else ""))
        if i == 0 and isinstance(st, (tuple, list)) and len(st) == 3 and st[1] < fa:
            prob.append(f"{ws}: interest is best by {st[1]}, but no name in any can be held before {fa}")
    if tops:
        notes.append(f"{w}: " + "; ".join(f"{h} after {m:.1f} years' median effort, {s * 100:.2f}% of those who keep at "
                                          f"it" for h, (m, s) in tops.items()))


def main(packs):
    prob, notes = [], []
    ages, drm, hk = catalogue(), dreams(), haunts()
    seen = {}
    for pk in packs:
        f_ = f"{PACKS}/{pk}/fields.py"
        F = getattr(load(f_, f"fields_{pk}"), f"FIELDS_{pk.upper()}", None)
        if not isinstance(F, dict) or not F:
            prob.append(f"{pk}: no FIELDS_{pk.upper()}")
            continue
        a_ = f"{PACKS}/{pk}/aims.py"
        A = getattr(load(a_, f"aims_{pk}"), f"AIMS_{pk.upper()}", {}) if os.path.exists(a_) else {}
        for aim in A:
            if aim not in F:
                prob.append(f"{pk}: v1 aim {aim!r} has no field")
        dr = doors(pk, ages)
        for aim, f in F.items():
            if aim in seen:
                prob.append(f"{pk}: {aim!r} is also a field of {seen[aim]}")
            seen[aim] = pk
            check_field(pk, aim, f, A.get(aim), ages, drm, hk, prob, notes, dr)
    print("# Fields check: " + ", ".join(packs) + "\n")
    for n in notes:
        print(n)
    if prob:
        print(f"\n{len(prob)} problem(s):")
        for p in prob:
            print("  " + p)
        return 1
    print("\nno problems")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(f)) for f in glob.glob(f"{PACKS}/*/fields.py"))
    sys.exit(main(args))
