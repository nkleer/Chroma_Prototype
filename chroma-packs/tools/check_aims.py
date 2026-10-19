"""Check the packs' aim ladders (aims version 1; Pathways and packs thread, 2026-10-19).

PYTHONDONTWRITEBYTECODE=1 python3 -B check_aims.py [pack ...]     (default: every pack with an aims.py)

The format (chroma-ideas/next-table-2026-10-19/plan.md, section 5: "a goal slot gets a ladder of 3 to 5 steps that can
be read in the life's state"). A pack's aims.py holds AIMS_<PACK>, a dict {aim: fields}, and LEGACY_<PACK>:
  aim      the aim as the character would say it ("to lead the country"); unique over every pack
  face     the colour face: one colour or a pair, letters of W U B R G with spaces ("W B")
  domain   the goal domain: career, partner, children, community or faith (the engine's COMMITMENTS), or "" for a
           pursuit (engine goal slots, domain -1)
  sphere   the sphere whose rung 4 or 5 (index 3 or 4) also counts as reaching the ladder's Known step: one of the nine
           sphere codes (comm gather care learn prot prod rule faith arts), or ""
  dreams   names from the Library's dreams (chroma-library/dreams.py, DREAMS and DREAMS_MORE) that can grow into the
           aim, of the aim's own domain; may be empty (the engine can still match a goal by its colours and domain)
  tribal, magic   the aim in the game's other worlds (the realm-ready rule, plan.md section 2)
  steps    3 to 5 dicts, the ladder from below:
             say     the step, told
             any     titles or perks (base catalogue, any pack's catalogue, core/*.py); the step is reached when one of
                     them is held or was held
             req     optional: an engine condition that must also hold when the step is reached (for names that can
                     come from anywhere, such as [known across the country]); has() was() yrs_has() name catalogue names
             height  optional: Known, Notable or Historic, in that order along the ladder; the last step has one
LEGACY_<PACK>  an engine condition: who in the pack can earn [a work that outlives you] (core/legacy.py), the
           Historic marker; the Engine joins the loaded packs' conditions into ROLES_AIMS's req.

Reports:
  1. fields, names and conditions (every name a catalogue name, every dream a dream of the aim's domain);
  2. colour balance: each pack's faces counted 1 each, split over their letters, within .03 in shares of each other
     (the packs' rule: colour-even on their own), and the faces of all the packs together;
  3. the pair table: how many callings each colour pair and each single colour has, over the packs checked;
  4. the heights each face can reach, and the steps per height.
Standard library only; nothing is written.
"""
import collections
import glob
import importlib.util
import itertools
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
DOMAINS = {"career", "partner", "children", "community", "faith", ""}
SPHERES = {"comm", "gather", "care", "learn", "prot", "prod", "rule", "faith", "arts", ""}
HEIGHTS = ["Known", "Notable", "Historic"]
COND = re.compile(r"\b(has|was|yrs_has)\((['\"])(.+?)\2\)")


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def catalogue_names():
    """Every title and perk name a step or a condition may use: the base catalogue, every pack's catalogue, the core."""
    base = load(f"{LIB}/earth_perks_titles.py", "base_cat")
    names = {x["name"] for x in base.TITLES} | {x["name"] for x in base.PERKS}
    for f_ in sorted(glob.glob(f"{PACKS}/*/catalogue.py")):
        m_ = load(f_, "cat_" + os.path.basename(os.path.dirname(f_)))
        names |= {x["name"] for x in list(m_.TITLES) + list(getattr(m_, "PERKS", []))}
    for f_ in sorted(glob.glob(f"{PACKS}/core/*.py")):
        m_ = load(f_, "core_" + os.path.basename(f_)[:-3])
        for k_ in ("PERKS", "TITLES", "PERKS_AIMS", "TITLES_AIMS"):
            names |= {x["name"] for x in getattr(m_, k_, [])}
    return names


def dream_domains():
    d = load(f"{LIB}/dreams.py", "lib_dreams")
    return {x["name"]: x["domain"] for x in list(d.DREAMS) + list(getattr(d, "DREAMS_MORE", []))}


def check_cond(where, cond, names, prob):
    if cond.count("(") != cond.count(")"):
        prob.append(f"{where}: unbalanced parentheses")
    for _, _, nm in COND.findall(cond):
        if nm not in names:
            prob.append(f"{where}: condition names {nm!r}, not a catalogue name")
    try:
        compile(cond.replace("&", " and ").replace("|", " or ").replace("~", " not "), where, "eval")
    except SyntaxError as e:
        prob.append(f"{where}: does not parse ({e.msg})")


def main(packs):
    prob = []
    names = catalogue_names()
    dreams = dream_domains()
    seen = {}
    faces_by_pack = {}
    heights_by_face = collections.defaultdict(set)
    steps_per_height = collections.Counter()
    for pk in packs:
        f_ = f"{PACKS}/{pk}/aims.py"
        m = load(f_, f"aims_{pk}")
        A = getattr(m, f"AIMS_{pk.upper()}", None)
        if not isinstance(A, dict) or not A:
            prob.append(f"{pk}: no AIMS_{pk.upper()}")
            continue
        leg = getattr(m, f"LEGACY_{pk.upper()}", None)
        if not isinstance(leg, str) or not leg.strip():
            prob.append(f"{pk}: no LEGACY_{pk.upper()}")
        else:
            check_cond(f"{pk} LEGACY", leg, names, prob)
        faces_by_pack[pk] = []
        for aim, d in A.items():
            w = f"{pk}: {aim!r}"
            if aim in seen:
                prob.append(f"{w}: name also in {seen[aim]}")
            seen[aim] = pk
            face = str(d.get("face", "")).split()
            if not (1 <= len(face) <= 2) or any(c not in COLORS for c in face) or len(set(face)) != len(face):
                prob.append(f"{w}: face {d.get('face')!r} is not one colour or a pair")
            else:
                faces_by_pack[pk].append("".join(sorted(face, key=COLORS.index)))
            if d.get("domain") not in DOMAINS:
                prob.append(f"{w}: domain {d.get('domain')!r}")
            if d.get("sphere", "") not in SPHERES:
                prob.append(f"{w}: sphere {d.get('sphere')!r}")
            for x in d.get("dreams", []):
                if x not in dreams:
                    prob.append(f"{w}: dream {x!r} is not in dreams.py")
                elif dreams[x] != d.get("domain"):
                    prob.append(f"{w}: dream {x!r} is of the domain {dreams[x]!r}, not {d.get('domain')!r}")
            for k in ("tribal", "magic"):
                if not str(d.get(k, "")).strip():
                    prob.append(f"{w}: no {k} form (the realm-ready rule)")
            st = d.get("steps", [])
            if not (3 <= len(st) <= 5):
                prob.append(f"{w}: {len(st)} steps (3 to 5)")
            last = -1
            for i, s in enumerate(st):
                ws = f"{w} step {i + 1}"
                if not str(s.get("say", "")).strip():
                    prob.append(f"{ws}: no say")
                if not s.get("any"):
                    prob.append(f"{ws}: no titles or perks in any")
                for x in s.get("any", []):
                    if x not in names:
                        prob.append(f"{ws}: {x!r} is not a catalogue name")
                if s.get("req"):
                    check_cond(ws, s["req"], names, prob)
                h = s.get("height")
                if h is not None:
                    if h not in HEIGHTS:
                        prob.append(f"{ws}: height {h!r}")
                        continue
                    if HEIGHTS.index(h) <= last:
                        prob.append(f"{ws}: height {h} out of order")
                    last = HEIGHTS.index(h)
                    heights_by_face[faces_by_pack[pk][-1] if faces_by_pack[pk] else "?"].add(h)
                    steps_per_height[h] += 1
                unknown = set(s) - {"say", "any", "req", "height"}
                if unknown:
                    prob.append(f"{ws}: unknown fields {sorted(unknown)}")
            if st and st[-1].get("height") is None:
                prob.append(f"{w}: the last step has no height")
            unknown = set(d) - {"face", "domain", "sphere", "dreams", "tribal", "magic", "steps"}
            if unknown:
                prob.append(f"{w}: unknown fields {sorted(unknown)}")

    print("# Aims check: " + ", ".join(packs) + "\n")
    tot = collections.Counter()
    for pk, fs in faces_by_pack.items():
        c = collections.Counter()
        for f in fs:
            for x in f:
                c[x] += 1 / len(f)
        tot.update(c)
        n = sum(c.values()) or 1
        sh = {x: c[x] / n for x in COLORS}
        spread = max(sh.values()) - min(sh.values())
        print(f"{pk}: {len(fs)} aims, faces " + " ".join(f"{x} {c[x]:.2f}" for x in COLORS) + f"  spread {spread:.3f}")
        if spread > .03:
            prob.append(f"{pk}: faces not colour-even (spread {spread:.3f} in shares)")
    n = sum(tot.values()) or 1
    print("all: faces " + " ".join(f"{x} {tot[x]:.2f}" for x in COLORS) +
          f"  spread {max(tot[x] / n for x in COLORS) - min(tot[x] / n for x in COLORS):.3f}")

    allf = collections.Counter(f for fs in faces_by_pack.values() for f in fs)
    print("\nfaces (callings over the packs checked; a single colour, then each pair):")
    keys = list(COLORS) + ["".join(p) for p in itertools.combinations(COLORS, 2)]
    print("  " + "  ".join(f"{k} {allf.get(k, 0)}" for k in keys))
    print("  pairs with no calling: " + (", ".join(k for k in keys[5:] if not allf.get(k)) or "none") +
          "; single colours with none: " + (", ".join(k for k in COLORS if not allf.get(k)) or "none"))
    print("\nheights each face can reach: " + "; ".join(f"{f} {'/'.join(h for h in HEIGHTS if h in heights_by_face[f])}"
                                                      for f in keys if f in heights_by_face))
    print("steps per height: " + ", ".join(f"{h} {steps_per_height[h]}" for h in HEIGHTS))

    if prob:
        print(f"\n{len(prob)} problem(s):")
        for p_ in prob:
            print("  - " + p_)
        return 1
    print("\nAll checks pass.")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(f)) for f in glob.glob(f"{PACKS}/*/aims.py"))
    sys.exit(main(args))
