"""Check a content pack (Pathways and packs thread, 2026-10-05).

PYTHONDONTWRITEBYTECODE=1 python3 check_pack.py science

Reads chroma-packs/<pack>/catalogue.py (TITLES, PERKS), chroma-packs/core/*.py (PERKS; reach.py first) and every
chroma-packs/<pack>/*.lib, against the base catalogue chroma-library/earth_perks_titles.py and the base moment names
(chroma-library/earth*.lib). Reports:
  1. catalogue fields (as in the base catalogue), names unique against the base;
  2. color balance of the pack's own commitment titles (profiles counted 1 each, split over their letters) and perks
     (ways split over their letters): within 3% of each other (Library rule), and which colors each perk kind holds;
  3. references in gained / lost / needs: [names] must be catalogue names, 'quoted' names a moment or a history mark;
  4. names used by the moments in title:, drops:, grants:, takes:, suspends:, requires:, holds:, aims: must exist
     (kind:<kind> and {title} as the engine reads them);
  5. the share sums the pack adds (titles and perks per life).
Standard library only; nothing is written.
"""
import glob
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = "/mnt/project-files"
PACKS = f"{ROOT}/chroma-packs"
LIB = f"{ROOT}/chroma-library"
COLORS = "WUBRG"
COMMIT = ["career", "partner", "children", "community", "faith"]
NEEDS = {"safety", "belonging", "autonomy", "competence", "meaning"}
RES = {"money", "time", "health", "ties", "freedom"}
PERK_KINDS = ["skill", "credential", "standing", "bond", "asset"]
MARKS = {"hid a wrong", "owned up", "kept your word", "broke your word", "learned a skill", "took a wild risk",
         "left home", "stayed home", "moved away", "turned down a chance", "helped someone in need",
         "refused someone in need", "made an enemy", "made a friend", "defied an authority", "gave in to pressure",
         "came home"}


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def lib_names(paths):
    out = []
    for p in paths:
        for line in open(p, encoding="utf-8"):
            if line.startswith("== "):
                out.append(line[3:].strip())
    return out


def main(pack):
    prob, notes = [], []
    P = prob.append
    base = load(f"{LIB}/earth_perks_titles.py", "base_cat")
    cat = load(f"{PACKS}/{pack}/catalogue.py", f"{pack}_cat")
    reach = load(f"{PACKS}/core/reach.py", "reach")
    T, K = list(cat.TITLES), list(cat.PERKS)
    R = list(reach.PERKS)
    for f_ in sorted(glob.glob(f"{PACKS}/core/*.py")):   # every core file, as batch.py reads them (engine 06:07)
        if os.path.basename(f_) != "reach.py":
            m_ = load(f_, "core_" + os.path.basename(f_)[:-3])
            R += list(getattr(m_, "PERKS", [])) + list(getattr(m_, "TITLES", []))
    base_names = {x["name"] for x in base.TITLES} | {x["name"] for x in base.PERKS}
    pack_names = [x["name"] for x in T + K]
    all_names = base_names | set(pack_names) | {x["name"] for x in R}

    # 1. fields and names
    for n in set(pack_names):
        if pack_names.count(n) > 1:
            P(f"name used twice in the pack: {n}")
        if n in base_names:
            P(f"name already in the base catalogue: {n}")
    for t in T:
        w = t["name"]
        for k in ("name", "kind", "ways", "meets", "ages", "share", "say", "gained", "lost", "needs"):
            if k not in t:
                P(f"{w}: no {k}")
        if t.get("kind") not in COMMIT + ["status"]:
            P(f"{w}: kind {t.get('kind')}")
        if not t.get("ways") and not t.get("refines") and t.get("kind") != "status":
            P(f"{w}: a commitment title without ways (only statuses and colorless facets may)")
        for p in t.get("profiles", []):
            if not re.fullmatch(r"[WUBRG]( [WUBRG])*", p[0]):
                P(f"{w}: profile letters '{p[0]}'")
        if t.get("profiles") and t["profiles"][0][0] != t["ways"]:
            P(f"{w}: ways must be the first profile")
        for part in t.get("meets", "").split():
            m = re.fullmatch(r"(need|res):(\w+)([+-])(\.\d+)", part)
            if not m or (m.group(1) == "need" and m.group(2) not in NEEDS) or (m.group(1) == "res" and m.group(2) not in RES):
                P(f"{w}: meets '{part}'")
            elif float(m.group(4)) > .15:
                P(f"{w}: meets above .15: '{part}'")
        if t.get("refines"):
            for r in t["refines"].split(";"):
                if r.strip() not in all_names:
                    P(f"{w}: refines unknown title '{r.strip()}'")
    for p in K + R:
        w = p["name"]
        for k in ("name", "kind", "ways", "odds", "skill_half", "retires", "ages", "share", "say"):
            if k not in p:
                P(f"{w}: no {k}")
        if p.get("kind") not in PERK_KINDS:
            P(f"{w}: kind {p.get('kind')}")
        if not re.fullmatch(r"[WUBRG]( [WUBRG])*", p.get("ways", "")):
            P(f"{w}: ways '{p.get('ways')}'")
        acc = p.get("kind") in ("credential", "asset")
        if acc and p.get("odds"):
            P(f"{w}: an access perk carries odds 0")
        if not acc and not (.02 <= p.get("odds", 0) <= .1):
            P(f"{w}: odds {p.get('odds')} outside .02 to .10")

    # 2. balance
    def tally(items, use_profiles):
        t = {c: 0.0 for c in COLORS}
        for x in items:
            ps = [q[0] for q in x["profiles"]] if use_profiles and x.get("profiles") else [x["ways"]]
            for q in ps:
                L = q.split()
                for c in L:
                    t[c] += 1 / len(L)
        return t
    tt = tally([t for t in T if t.get("ways") and t["kind"] in COMMIT], True)
    tp = tally(K, False)
    for label, t in (("titles (profiles)", tt), ("perks (ways)", tp)):
        tot = sum(t.values())
        sh = {c: t[c] / tot for c in COLORS}
        spread = max(sh.values()) - min(sh.values())
        notes.append(f"{label}: " + "  ".join(f"{c} {t[c]:.2f} ({sh[c]:.3f})" for c in COLORS) +
                     f"  spread {spread:.3f}" + ("" if spread <= .03 else "  <-- above .03"))
        if spread > .03:
            P(f"{label} color spread {spread:.3f} above .03")
    for k in PERK_KINDS:
        held = sorted({c for p in K if p["kind"] == k for c in p["ways"].split()}, key=COLORS.index)
        if held:
            notes.append(f"  {k}: {''.join(held)} ({sum(1 for p in K if p['kind'] == k)} perks)")

    # 3. references in plain words
    libs = sorted(glob.glob(f"{PACKS}/{pack}/*.lib"))
    moments = set(lib_names(glob.glob(f"{LIB}/earth*.lib"))) | set(lib_names(libs))
    planned = set()
    brief = f"{PACKS}/{pack}/MOMENTS-BRIEF.md"
    if os.path.exists(brief):
        planned = {re.sub(r"\s+", " ", x) for x in re.findall(r"`([a-z][^`|:]+?)`", open(brief, encoding="utf-8").read())}
    for x in T + K + R:
        for k in ("gained", "lost", "needs"):
            txt = x.get(k, "")
            for nm in re.findall(r"\[([^\]]+)\]", txt):
                if nm not in all_names:
                    P(f"{x['name']}: {k} names [{nm}], not in any catalogue")
            for nm in re.findall(r"'([^']+)'", txt):
                if nm in MARKS or nm in moments:
                    continue
                if nm in planned:
                    notes.append(f"  planned moment, not written yet: '{nm}' ({x['name']})")
                else:
                    P(f"{x['name']}: {k} quotes '{nm}', neither a moment nor a mark")

    # 4. names used by the moments
    used = 0
    for path in libs:
        cur = "?"
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            s = line.strip()
            if s.startswith("== "):
                cur = s[3:]
            fields = []
            if s.startswith("- "):
                fields = [f.strip() for f in s.split(" | ")[2:]]
            elif s.startswith("holds:"):
                fields = [s]
            for f in fields:
                if ":" not in f:
                    continue
                k, v = [y.strip() for y in f.split(":", 1)]
                k0 = k[:-9] if k.endswith("_if_fails") else k
                if k0 in ("title", "drops", "grants", "takes", "suspends", "requires", "holds", "aims"):
                    for nm in [y.strip() for y in re.split(r"[;|]", v) if y.strip()]:
                        used += 1
                        if nm.startswith("kind:"):   # every title of a kind held (engine batch.py)
                            if nm[5:] not in COMMIT:
                                P(f"{os.path.basename(path)}:{ln} ({cur}): {k} names '{nm}', not a kind of title")
                            continue
                        if nm in ("{title}", "{missed}"):   # the title held that brought the person here (engine, holds:
                            continue                        # moments); the title of the last failed long shot (08:21)
                        if nm not in all_names:
                            P(f"{os.path.basename(path)}:{ln} ({cur}): {k} names '{nm}', not in any catalogue")

    # 5. shares
    notes.append(f"shares the pack adds per life: titles {sum(t['share'] for t in T):.3f}, perks "
                 f"{sum(p['share'] for p in K):.3f}; core perks {sum(p['share'] for p in R):.4f}")
    notes.append(f"{len(T)} titles, {len(K)} perks, {len(libs)} .lib files with {len(lib_names(libs))} moments, "
                 f"{used} catalogue names used by them")
    print(f"# Pack check: {pack}\n")
    for n in notes:
        print(n)
    print()
    if prob:
        print(f"{len(prob)} problems:")
        for p in prob:
            print("  - " + p)
    else:
        print("All checks pass.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "science")
