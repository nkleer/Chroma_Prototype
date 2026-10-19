"""Aims v1 (chroma-ideas/next-table-2026-10-19/plan.md section 5, 10-19): the Earth aim catalogue and its moments.
python3 -B tests/check_aims.py [chroma-library dir]     ends "no problems" or lists them; --reach lists every step
                                                         that no moment or rule grants yet (the step moments' to-do);
                                                         --part checks a writer's share (no balance over all faces)
earth_aims.py holds AIMS_EARTH, {aim: fields}, in the packs' format (chroma-packs/tools/check_aims.py) plus four fields:
    face, domain, sphere, dreams, tribal, magic, steps   as the packs' (domain "" is a pursuit; its dreams are pursuits)
    area      what part of life it is about (AREAS below)
    calling   True when the ladder leads toward a height (its last step has one); False for an aim lived close to home,
              whose steps may have no height
    below     how it shows from below before anyone names it: one told line, third person present, with {N}
    spark     the name of its spark moment in earth_aim_moments.py (aim_role: spark)
earth_aim_moments.py is built from earth_aim_moments-*.lib ("python3 build.py earth_aim_moments"): life events with
aim: and aim_role: spark | step <n>. Nothing reads either file until the Engine's aims switch is on.
Rules checked:
    1. fields and names: every step name and req name a catalogue name (base, every pack, the packs' core); dreams of
       the aim's domain; names unique over the packs' aims; no colour words, no Magic terms, no unsafe words;
    2. balance: every face (5 colours, 10 pairs) has the same number of aims; every colour's share within .03;
       every domain holds aims of all five colours; every area at least two aims;
    3. moments: one spark moment an aim, named by its spark field; a step moment's step exists and one of its options
       grants a name of that step; every option of an aim moment leaves one or two footprints (as check_footprint.py);
       a spark moment has a try (dream: test or seal) and at most one dream: drop; labels not used in earth.py.
Standard library only; nothing is written.
"""
import collections, glob, importlib.util, os, re, sys
sys.dont_write_bytecode = True

LIB = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
ROOT = os.path.dirname(LIB)
PACKS = os.path.join(ROOT, "chroma-packs")
RULES = os.path.join(ROOT, "chroma-engine", "v22-speedpass")
sys.path.insert(0, LIB)
COLORS = "WUBRG"
FACES = list(COLORS) + ["WU", "UB", "BR", "RG", "WG", "WB", "UR", "BG", "WR", "UG"]
DOMAINS = {"career", "partner", "children", "community", "faith", ""}
SPHERES = {"comm", "gather", "care", "learn", "prot", "prod", "rule", "faith", "arts", ""}
HEIGHTS = ["Known", "Notable", "Historic"]
AREAS = ["love", "line", "craft", "knowledge", "art", "land", "home", "faith", "community", "cause", "adventure",
         "freedom", "justice", "wealth", "standing", "care", "body"]
COND = re.compile(r"\b(has|was|yrs_has)\((['\"])(.+?)\2\)")
COLOR_WORDS = re.compile(r"\b(white[s]?|whiter|whitest|blue[s]?|bluer|bluest|black[s]?|blacker|blackest|blackened|"
                         r"red[s]?|redder|reddest|reddish|reddened|green[s]?|greener|greenest|greenish)\b", re.I)
MAGIC_WORDS = re.compile(r"\b(colou?rs?|mana|planeswalker\w*|azorius|dimir|rakdos|gruul|selesnya|orzhov|izzet|golgari|"
                         r"boros|simic|bant|esper|grixis|jund|naya|abzan|jeskai|sultai|mardu|temur|mono)\b", re.I)
SAFETY = re.compile(r"\b(rap(e|ed|es|ing|ist)|sexual\w*|sex|molest\w*|suicid\w*|kill (yourself|myself|themselves)|"
                    r"self-harm\w*|tortur\w*|gore|blood\w*|corpse\w*|mutilat\w*|abus\w*|naked|groom(ed|ing))\b", re.I)
PERSON_MARKS = {"made a friend", "made an enemy", "took them in"}


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def catalogue():
    """name -> kind for every title and perk a step may use: the base catalogue, every pack's catalogue, the core."""
    base = load(os.path.join(LIB, "earth_perks_titles.py"), "base_cat")
    kind = {x["name"]: x["kind"] for x in list(base.TITLES) + list(base.PERKS)}
    for f in sorted(glob.glob(f"{PACKS}/*/catalogue.py")) + sorted(glob.glob(f"{PACKS}/core/*.py")):
        m = load(f, "cat_" + f.replace("/", "_")[-40:-3])
        for k in ("TITLES", "PERKS", "PERKS_AIMS", "TITLES_AIMS"):
            kind.update({x["name"]: x.get("kind", "") for x in getattr(m, k, [])})
    return kind


def granted_somewhere():
    """Names some moment or rule can hand out today: title:/grants: of the Earth library, Bold ways and the packs'
    moments, and names quoted in the engine's rules. A report, not proof: a name a rule builds from parts is missed."""
    seen = set()
    import earth
    for s in earth.SITUATIONS:
        for o in s["options"]:
            nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
            for k in ("title", "grants"):
                seen |= set(names(nt.get(k)))
    for f in glob.glob(f"{LIB}/earth_play-*.lib") + glob.glob(f"{PACKS}/*/*.lib") + glob.glob(f"{LIB}/earth-*.lib"):
        for m in re.finditer(r"\b(?:title|grants|threshold: title):\s*([^|\n]+)", open(f, encoding="utf-8").read()):
            seen |= set(names(m.group(1).split(" for_years")[0]))
    txt = "".join(open(f, encoding="utf-8").read() for f in glob.glob(f"{RULES}/*.py"))
    txt += "".join(open(f, encoding="utf-8").read() for f in glob.glob(f"{LIB}/spheres/*.py"))
    return seen, txt


def names(v):
    return [x.strip() for x in re.split(r"[;,]", v) if x.strip()] if isinstance(v, str) else list(v or [])


def footprints(o, read_marks, kind):
    """As check_footprint.py: the footprints an option leaves through today's fields and foot:."""
    tags = str(o[4] or "")
    nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
    out = list(nt.get("foot") or [])
    m = nt.get("mark")
    if m in PERSON_MARKS or m in read_marks:
        out.append(("person" if m in PERSON_MARKS else "mark", m))
    out += [("person", k) for k in ("bond", "break", "mend", "secret", "trust") if nt.get(k)]
    commits = {t[7:] for t in tags.split() if t.startswith("commit:")}
    by = {"partner": "person", "children": "person", "bond": "person", "community": "place", "career": "place",
          "faith": "place", "standing": "place", "asset": "means"}
    for k in ("title", "grants", "takes", "drops", "suspends"):
        for x in names(nt.get(k)):
            if by.get(kind.get(x)) and not (k == "title" and kind[x] in commits):
                out.append((by[kind[x]], x))
    for t in tags.split():
        if t.startswith("commit:"):
            out.append(("person" if t[7:] in ("partner", "children") else "place", t))
        elif re.match(r"(win|lose|pay):", t):
            out.append(("means", t))
    if nt.get("back"):
        out.append(("door", nt["back"]))
    return out


def words(where, text, prob):
    for rx, what in ((COLOR_WORDS, "a colour word"), (MAGIC_WORDS, "a Magic term"), (SAFETY, "an unsafe word")):
        m = rx.search(text or "")
        if m:
            prob.append(f"{where}: {what} \"{m.group(0)}\"")


def main():
    prob, notes = [], []
    kind = catalogue()
    dd = load(os.path.join(LIB, "dreams.py"), "lib_dreams")
    dream_dom = {x["name"]: x["domain"] for x in list(dd.DREAMS) + list(getattr(dd, "DREAMS_MORE", []))}
    packs_aims = {}
    for f in glob.glob(f"{PACKS}/*/aims.py"):
        pk = os.path.basename(os.path.dirname(f))
        packs_aims.update({a: pk for a in getattr(load(f, f"aims_{pk}"), f"AIMS_{pk.upper()}", {})})
    A = load(os.path.join(LIB, "earth_aims.py"), "earth_aims").AIMS_EARTH
    faces, by_dom, by_area = collections.Counter(), collections.defaultdict(set), collections.Counter()
    for aim, d in A.items():
        w = f"{aim!r}"
        if aim in packs_aims:
            prob.append(f"{w}: also an aim of the {packs_aims[aim]} pack")
        for k in ("aim", "below", "tribal", "magic"):
            words(f"{w} {k}", aim if k == "aim" else d.get(k), prob)
        face = "".join(sorted(str(d.get("face", "")).split(), key=COLORS.index)) \
            if all(c in COLORS for c in str(d.get("face", "")).split()) else "?"
        if face not in FACES:
            prob.append(f"{w}: face {d.get('face')!r} is not one colour or a pair")
        faces[face] += 1
        dom = d.get("domain")
        if dom not in DOMAINS:
            prob.append(f"{w}: domain {dom!r}")
        by_dom[dom] |= set(face)
        if d.get("sphere", "") not in SPHERES:
            prob.append(f"{w}: sphere {d.get('sphere')!r}")
        if d.get("area") not in AREAS:
            prob.append(f"{w}: area {d.get('area')!r} (one of {', '.join(AREAS)})")
        by_area[d.get("area")] += 1
        if not isinstance(d.get("calling"), bool):
            prob.append(f"{w}: calling must be True or False")
        b = str(d.get("below", ""))
        if "{N}" not in b or len(b.split()) < 6:
            prob.append(f"{w}: below must be one told line with {{N}}")
        for k in ("tribal", "magic"):
            if not str(d.get(k, "")).strip():
                prob.append(f"{w}: no {k} form (the realm-ready rule)")
        for x in d.get("dreams", []):
            want = dom or "pursuit"
            if x not in dream_dom:
                prob.append(f"{w}: dream {x!r} is not in dreams.py")
            elif dream_dom[x] != want:
                prob.append(f"{w}: dream {x!r} is of the domain {dream_dom[x]!r}, not {want!r}")
        st = d.get("steps", [])
        if not 3 <= len(st) <= 5:
            prob.append(f"{w}: {len(st)} steps (3 to 5)")
        last = -1
        for i, s in enumerate(st):
            ws = f"{w} step {i + 1}"
            words(ws, s.get("say"), prob)
            if not str(s.get("say", "")).strip():
                prob.append(f"{ws}: no say")
            if not s.get("any"):
                prob.append(f"{ws}: no titles or perks in any")
            for x in s.get("any", []):
                if x not in kind:
                    prob.append(f"{ws}: {x!r} is not a catalogue name")
            if s.get("req"):
                for _, _, nm in COND.findall(s["req"]):
                    if nm not in kind:
                        prob.append(f"{ws}: req names {nm!r}, not a catalogue name")
                try:
                    compile(s["req"].replace("&", " and ").replace("|", " or ").replace("~", " not "), ws, "eval")
                except SyntaxError as e:
                    prob.append(f"{ws}: req does not parse ({e.msg})")
            if s.get("height"):
                if s["height"] not in HEIGHTS:
                    prob.append(f"{ws}: height {s['height']!r}")
                elif HEIGHTS.index(s["height"]) <= last:
                    prob.append(f"{ws}: heights out of order")
                else:
                    last = HEIGHTS.index(s["height"])
        if d.get("calling") and st and not st[-1].get("height"):
            prob.append(f"{w}: a calling's last step has a height")
    # 2. balance (not with --part: a writer's own share of the aims)
    part = "--part" in sys.argv
    n = set(faces[f] for f in FACES if not part or faces[f])
    if len(n) != 1:
        prob.append("faces not even: " + ", ".join(f"{f} {faces[f]}" for f in FACES))
    share = collections.Counter()
    for f in FACES:
        for c in f:
            share[c] += faces[f] / len(f)
    tot = sum(share.values()) or 1
    if not part and max(share.values()) / tot - min(share[c] for c in COLORS) / tot > .03:
        prob.append("colour shares more than .03 apart: " + ", ".join(f"{c} {share[c] / tot:.3f}" for c in COLORS))
    for dom in DOMAINS if not part else ():
        if set(COLORS) - by_dom[dom]:
            prob.append(f"domain {dom or 'pursuit'!r} has no aim of {''.join(sorted(set(COLORS) - by_dom[dom]))}")
    for a in AREAS if not part else ():
        if by_area[a] < 2:
            prob.append(f"area {a!r} has {by_area[a]} aims (at least two)")
    # 3. moments
    mf = os.path.join(LIB, "earth_aim_moments.py")
    sparks, steps_done = collections.Counter(), set()
    if os.path.exists(mf):
        import earth
        lab_earth = {o[0] for s in earth.SITUATIONS for o in s["options"]}
        M = load(mf, "earth_aim_moments")
        txt = "".join(open(os.path.join(RULES, f), encoding="utf-8").read() for f in ("rules_titles.py", "rules_perks.py"))
        import build
        read_marks = {m for m in build.MARKS if f"'{m}'" in txt}
        for s in M.SITUATIONS:
            w = s["name"]
            aim, role = s.get("aim"), s.get("aim_role", "")
            if aim not in A:
                prob.append(f"{w}: aim {aim!r} is not in earth_aims.py")
                continue
            if role == "spark":
                sparks[aim] += 1
                if A[aim].get("spark") != w:
                    prob.append(f"{w}: the spark of {aim!r} is named {A[aim].get('spark')!r}")
                acts = [o[5].get("dream") for o in s["options"] if isinstance(o[5], dict)]
                if not {"test", "seal"} & set(acts):
                    prob.append(f"{w}: a spark moment needs a try (dream: test or seal)")
                if acts.count("drop") > 1:
                    prob.append(f"{w}: at most one dream: drop")
            else:
                k = int(role.split()[1])
                st = A[aim].get("steps", [])
                if k > len(st):
                    prob.append(f"{w}: {aim!r} has no step {k}")
                else:
                    gives = {x for o in s["options"] if isinstance(o[5], dict)
                             for f_ in ("title", "grants") for x in names(o[5].get(f_))}
                    if not gives & set(st[k - 1]["any"]):
                        prob.append(f"{w}: no option grants a name of step {k} ({', '.join(st[k - 1]['any'])})")
                    steps_done.add((aim, k))
            for o in s["options"]:
                fp = footprints(o, read_marks, kind)
                if not 1 <= len(fp) <= 2:
                    prob.append(f"{w} / {o[1]} '{o[0][:50]}': {len(fp)} footprints (one or two)")
                if o[0] in lab_earth:
                    prob.append(f"{w} / {o[1]}: label also in earth.py: '{o[0]}'")
    for aim in A:
        if sparks[aim] != 1:
            prob.append(f"{aim!r}: {sparks[aim]} spark moments (one)")
    # report: steps nothing grants yet
    seen, rtxt = granted_somewhere()
    todo = []
    for aim, d in A.items():
        for i, s in enumerate(d.get("steps", [])):
            if (aim, i + 1) in steps_done:
                continue
            if not any(x in seen or f"'{x}'" in rtxt or f'"{x}"' in rtxt for x in s.get("any", [])):
                todo.append(f"{aim!r} step {i + 1} ({', '.join(s.get('any', []))})")
    print(f"aims: {len(A)}; faces {dict((f, faces[f]) for f in FACES)}; areas {dict(by_area.most_common())}; "
          f"domains {dict(collections.Counter(d.get('domain') or 'pursuit' for d in A.values()))}; "
          f"callings {sum(1 for d in A.values() if d.get('calling'))}; spark moments {sum(sparks.values())}, "
          f"step moments {len(steps_done)}; steps nothing grants yet: {len(todo)}")
    if "--reach" in sys.argv:
        for t in todo:
            print("  to do: " + t)
    for p in prob:
        print("  " + p)
    print(f"{len(prob)} problems" if prob else "no problems")
    sys.exit(1 if prob else 0)


if __name__ == "__main__":
    main()
