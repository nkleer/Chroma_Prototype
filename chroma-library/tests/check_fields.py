"""Aims as fields (v25, chroma-engine/notes/v25/aims-shape.md sections 3, 4 and 7, 10-23): Earth's fields and the
shape moments they share.
python3 -B tests/check_fields.py [chroma-library dir]    ends "no problems" or lists them; --cover lists each rung's ways in
earth_fields.py holds FIELDS_EARTH {field: dict} (the 60 v1 aims and the dream fields), FIELDS_EARTH_LAND (the land's
30 ways as fields, words only: their numbers stay in land.json) and TITLES_V25 (the new titles the fields' rungs name).
earth_shape_moments.py is built from earth_shape_moments-*.lib ("python3 build.py earth_shape_moments"). Nothing reads
either file until the Engine's aims refit is on.
Rules checked:
    1. a field: its shape; 3 to 5 rungs, which with skip: fill the shape's rungs; the keys of section 3; places are
       haunts; people are coach, rival, peer or patron; two or more ways round; no colour words, Magic or unsafe words;
    2. a v1 aim's field keeps v1's face, sphere, domain, calling, dreams, below, tribal, magic and, step for step, say,
       any, req and height (a land field keeps three of v1's steps, in order); a new field's dreams are in dreams.py;
    3. a rung: say; any names catalogue titles or TITLES_V25; years (median, low, high) with low <= median <= high;
       share 0 to 1; rung 1's start (from, best_to, late_from) in order; contests_y 0 or more; forks one or two of
       go_on, pay, take, round; a time rung has no forks and no contests;
    4. coverage (section 4): every rung not reached by time alone has three or more ways in among the shape moments of
       kind practice, contest, chance or mentor for its shape (or "any") that fit its shape rung, one of them practice.
       Reported, and checked once earth_shape_moments.py exists;
    5. TITLES_V25: names unique and new to the catalogue, each in the catalogue's format (kind, sphere, face, ways,
       profiles, meets, ages, share, say, gained, lost, needs; doors optional). They stay out of earth_perks_titles.py,
       so no life changes until the Engine reads them with the refit on.
Standard library only; nothing is written.
"""
import collections, os, re, sys
sys.dont_write_bytecode = True

LIB = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
sys.path.insert(0, os.path.join(LIB, "tests"))
import check_aims as CA   # its catalogue, word checks and loader

SHAPES = {"competition": 5, "craft": 5, "art": 5, "knowledge": 5, "career": 5, "cause": 5, "home": 4, "land": 3,
          "faith": 5, "venture": 4}
FORKS = {"go_on", "pay", "take", "round"}
PEOPLE = {"coach", "rival", "peer", "patron"}
HEIGHTS = ["", "Known", "Notable", "Historic"]
KEYS = ("shape", "face", "sphere", "domain", "dreams", "calling", "thing", "doing", "contest", "places", "people",
        "round", "below", "tribal", "magic", "rungs")
WAYS_IN = {"practice", "contest", "chance", "mentor"}


def haunts():
    src = open(os.path.join(os.environ.get("CHROMA_ROOT", "/mnt/project-files"), "chroma-library", "build.py")).read()
    return set(re.findall(r'"(\w+\.\w+)"', src[src.index("HAUNT_KINDS = ["):src.index("LADDER = [")]))


def main():
    prob = []
    kind = CA.catalogue()
    dd = CA.load(os.path.join(LIB, "dreams.py"), "lib_dreams")
    dreams = {x["name"] for x in list(dd.DREAMS) + list(getattr(dd, "DREAMS_MORE", []))}
    A = CA.load(os.path.join(LIB, "earth_aims.py"), "earth_aims").AIMS_EARTH
    M = CA.load(os.path.join(LIB, "earth_fields.py"), "earth_fields")
    F, FL, NT = M.FIELDS_EARTH, getattr(M, "FIELDS_EARTH_LAND", {}), getattr(M, "TITLES_V25", [])
    H = haunts()
    new = {}
    for t in NT:
        w = f"title {t.get('name')!r}"
        if t.get("name") in new or t.get("name") in kind:
            prob.append(f"{w}: already named")
        new[t.get("name")] = t.get("kind")
        for k in ("kind", "sphere", "face", "ways", "profiles", "meets", "ages", "share", "say", "gained", "lost", "needs"):
            if not t.get(k):
                prob.append(f"{w}: no {k}")
        for k in ("say", "gained"):
            CA.words(f"{w} {k}", t.get(k), prob)
    names = set(kind) | set(new)
    for aim in A:
        if aim not in F:
            prob.append(f"{aim!r}: a v1 aim with no field")
    shape_rungs = {}   # field -> [(field rung index, shape rung index, rung)]
    for nm, d in list(F.items()) + list(FL.items()):
        w = f"{nm!r}"
        for k in KEYS:
            if k not in d:
                prob.append(f"{w}: no {k}")
        sh = d.get("shape")
        if sh not in SHAPES:
            prob.append(f"{w}: shape {sh!r}")
            continue
        rs, skip = d.get("rungs", []), list(d.get("skip", []))
        lo = 3 if sh != "land" else 3
        if not lo <= len(rs) <= 5 or len(rs) + len(skip) != SHAPES[sh] or any(not 0 <= s < SHAPES[sh] for s in skip):
            prob.append(f"{w}: {len(rs)} rungs and skip {skip} do not fill the {sh} shape's {SHAPES[sh]} rungs")
        idx = [i for i in range(SHAPES[sh]) if i not in skip]
        shape_rungs[nm] = list(zip(range(len(rs)), idx, rs))
        bad = [p for p in d.get("places", []) if p not in H]
        if bad or not d.get("places"):
            prob.append(f"{w}: places {bad or 'none'} (haunt kinds)")
        if not d.get("people") or set(d["people"]) - PEOPLE:
            prob.append(f"{w}: people must be some of {', '.join(sorted(PEOPLE))}")
        if len(d.get("round", [])) < 2:
            prob.append(f"{w}: two or more ways round")
        for k in ("thing", "doing", "contest", "below", "tribal", "magic"):
            CA.words(f"{w} {k}", d.get(k), prob)
        for k in ("people", "round"):
            for x in (d.get(k) or {}).values() if k == "people" else d.get(k, []):
                CA.words(f"{w} {k}", x, prob)
        v1 = A.get(nm)
        if v1:
            for k in ("face", "sphere", "domain", "calling", "dreams", "below", "tribal", "magic"):
                if d.get(k) != v1.get(k):
                    prob.append(f"{w}: {k} is not v1's")
            st = v1["steps"]
            if sh == "land" and len(st) > len(rs):
                kept = [s for s in st if s["say"] in [r.get("say") for r in rs]]
            else:
                kept = st
            if len(kept) != len(rs):
                prob.append(f"{w}: {len(rs)} rungs for v1's {len(st)} steps")
            for i, (s, r) in enumerate(zip(kept, rs)):
                for k in ("say", "any", "req", "height"):
                    if s.get(k, "" if k != "any" else []) != r.get(k, "" if k != "any" else []):
                        prob.append(f"{w} rung {i + 1}: {k} is not v1's step")
        elif nm in F:
            for x in d.get("dreams", []):
                if x not in dreams:
                    prob.append(f"{w}: dream {x!r} is not in dreams.py")
        for i, r in enumerate(rs):
            rw = f"{w} rung {i + 1}"
            if not r.get("say"):
                prob.append(f"{rw}: no say")
            CA.words(rw, r.get("say"), prob)
            for x in r.get("any", []):
                if x not in names:
                    prob.append(f"{rw}: {x!r} is not a catalogue title or TITLES_V25")
            if r.get("height", "") not in HEIGHTS:
                prob.append(f"{rw}: height {r.get('height')!r}")
            if nm in FL:
                continue   # the land's numbers are land.json's
            y = r.get("years")
            if not (isinstance(y, (tuple, list)) and len(y) == 3 and y[1] <= y[0] <= y[2] and y[1] >= 0):
                prob.append(f"{rw}: years must be (median, low, high), low <= median <= high, not {y!r}")
            if not 0 < r.get("share", -1) <= 1:
                prob.append(f"{rw}: share {r.get('share')!r}")
            if i == 0:
                s_ = r.get("start")
                if not (isinstance(s_, (tuple, list)) and len(s_) == 3 and s_[0] <= s_[1] <= s_[2]):
                    prob.append(f"{rw}: start must be (from, best_to, late_from) in order, not {s_!r}")
            if r.get("contests_y", 0) < 0:
                prob.append(f"{rw}: contests_y below 0")
            fk = r.get("forks", [])
            if r.get("time"):
                if fk or r.get("contests_y"):
                    prob.append(f"{rw}: a time rung has no forks and no contests")
            elif not 1 <= len(fk) <= 2 or set(fk) - FORKS:
                prob.append(f"{rw}: forks one or two of {', '.join(sorted(FORKS))}, not {fk!r}")
    cover = []
    f_sm = os.path.join(LIB, "earth_shape_moments.py")
    if os.path.exists(f_sm):
        SM = CA.load(f_sm, "earth_shape_moments").SITUATIONS
        for nm, rows in shape_rungs.items():
            sh = (F.get(nm) or FL.get(nm))["shape"]
            for i, si, r in rows:
                if r.get("time"):
                    continue
                ways = [s for s in SM if s.get("shape") in (sh, "any") and s.get("kind") in WAYS_IN
                        and (s.get("rungs") == "any" or si in s.get("rungs", ()))]
                ks = collections.Counter(s["kind"] for s in ways)
                cover.append((nm, i + 1, len(ways), dict(ks)))
                if len(ways) < 3 or not ks.get("practice"):
                    prob.append(f"{nm!r} rung {i + 1}: {len(ways)} ways in ({dict(ks)}), wants 3 with a practice")
    else:
        print("earth_shape_moments.py not built yet: coverage not checked")
    if "--cover" in sys.argv:
        for c in cover:
            print(f"  {c[0]} rung {c[1]}: {c[2]} ways in {c[3]}")
    print(f"fields {len(F)} (v1 {sum(1 for x in F if x in A)}, new {sum(1 for x in F if x not in A)}), land ways "
          f"{len(FL)}, new titles {len(NT)}; by shape "
          + ", ".join(f"{k} {v}" for k, v in sorted(collections.Counter(d['shape'] for d in F.values()).items())))
    if prob:
        print(f"{len(prob)} problems:")
        for p in prob:
            print("  -", p)
    else:
        print("no problems")
    return prob


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
