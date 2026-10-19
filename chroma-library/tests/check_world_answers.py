"""The world answers v1 (chroma-world/spheres/world-answers-v1.md, 10-19): the Library's moments and lines.
python3 -B tests/check_world_answers.py [chroma-library dir] [--part]   ends "no problems" or lists them
earth_world_answers.py is built from earth_world_answers-*.lib ("python3 build.py earth_world_answers"):
    E4  the sphere asks: cast_want asked_help (rung 2), asked_lead (rung 3), asked_speak (rung 4), with sphere: <code>;
        at least one moment for each sphere and each ask; at least two ways a yes (lever: loyalty or lead)
    F2  decisions for others: tier: decision, cast_want: decide, sphere: <code>; 2 to 4 options, each a colour mix and
        a scope (place, town_sphere, nation); at least four for each sphere; over all of them every colour leads about
        as often (within 1.2 times, as WA8)
    F3  rivals, allies and the successor: cast_want rival_push, ally_won, ally_lost, successor_seen, successor_hand;
        at least two of each
    every option outside the decisions leaves one or two footprints (as check_footprint.py); labels not in earth.py.
earth_world_lines.py holds the told lines (plain data):
    BECAUSE[unit][size][world]   two lines or more, size "a little" | "clearly" | "a lot" (the ledger's steps)
    NATION[push][world]          a national push, told by what it visibly did
    KEPT[ring][level][world]     the end of a life: level "most" (over .6 kept) | "some" | "little" (under .3)
    CAUSE[world]                 how a line names its cause, with {act} and {age}
    worlds earth, tribal, magic; third person with {N}; slots from build.py's list.
--part skips the coverage counts (a writer's share). Standard library only; nothing is written.
"""
import collections, importlib.util, os, re, sys
sys.dont_write_bytecode = True

LIB = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
sys.path.insert(0, LIB)
sys.path.insert(0, os.path.join(LIB, "tests"))
PART = "--part" in sys.argv
COLORS = "WUBRG"
SPHERES = ["rule", "gather", "arts", "faith", "care", "learn", "prod", "comm", "prot"]
ASKS = ["asked_help", "asked_lead", "asked_speak"]
F3 = ["rival_push", "ally_won", "ally_lost", "successor_seen", "successor_hand"]
UNITS = ["person_colours", "person_closer", "person_further", "person_trust_up", "person_trust_down", "group_norm",
         "group_members", "place_mix", "place_founded", "place_kept_open", "town_sphere"]
SIZES = ["a little", "clearly", "a lot"]
PUSHES = ["state", "institution", "economy", "culture", "tech", "belief"]
RINGS = ["person", "group", "place", "town_sphere", "nation"]
LEVELS = ["most", "some", "little"]
WORLDS = ["earth", "tribal", "magic"]


def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    prob = []
    import build, earth
    from check_aims import footprints, catalogue, words, foot_table, lessons   # the same footprint count and word rules
    kind = catalogue()
    rtxt = "".join(open(os.path.join(os.path.dirname(LIB), "chroma-engine", "v22-speedpass", f), encoding="utf-8").read()
                   for f in ("rules_titles.py", "rules_perks.py"))
    read_marks = {m for m in build.MARKS if f"'{m}'" in rtxt}
    read_marks |= set(__import__("footprint_names").MARKS_WIRED)   # Library 10-19
    lab_earth = {o[0] for s in earth.SITUATIONS for o in s["options"]}
    mf = os.path.join(LIB, "earth_world_answers.py")
    asks, decs, f3, lead = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    if os.path.exists(mf):
        FT = foot_table("earth_world_answers")
        for s in load(mf, "earth_world_answers").SITUATIONS:
            w, cw = s["name"], s.get("cast_want")
            sph = str(s.get("sphere") or "").split(".")[0]
            dec = s.get("tier") == "decision" or cw == "decide"
            if dec:
                if cw != "decide":
                    prob.append(f"{w}: a decision needs cast_want: decide")
                decs[sph] += 1
                for o in s["options"]:
                    code = re.sub(r"[^WUBRG]", "", str(o[1]))
                    for c in set(code):
                        lead[c] += 1 / len(set(code))
            elif cw in ASKS:
                asks[(sph, cw)] += 1
                yes = sum(1 for o in s["options"] if isinstance(o[5], dict) and o[5].get("lever") in ("loyalty", "lead"))
                if yes < 2:
                    prob.append(f"{w}: at least two ways to say yes (lever: loyalty or lead), found {yes}")
                if sph not in SPHERES:
                    prob.append(f"{w}: the sphere asks, so it needs sphere: <code>")
            elif cw in F3:
                f3[cw] += 1
            else:
                prob.append(f"{w}: cast_want {cw!r} is not one of the world answers' moments")
            if not dec:
                lessons(w, s["options"], FT, prob)
            for o in s["options"]:
                if o[0] in lab_earth:
                    prob.append(f"{w} / {o[1]}: label also in earth.py: '{o[0]}'")
                if not dec:
                    fp = footprints(o, read_marks, kind, FT.get((w, o[0])))
                    if not 1 <= len(fp) <= 2:
                        prob.append(f"{w} / {o[1]} '{o[0][:50]}': {len(fp)} footprints (one or two)")
    if not PART:
        for sp in SPHERES:
            for a in ASKS:
                if not asks[(sp, a)]:
                    prob.append(f"no {a} moment for the {sp} sphere")
            if decs[sp] < 4:
                prob.append(f"{sp}: {decs[sp]} decisions (at least four)")
        for k in F3:
            if f3[k] < 2:
                prob.append(f"{k}: {f3[k]} moments (at least two)")
        if lead and max(lead[c] for c in COLORS) > 1.2 * min(lead[c] for c in COLORS):
            prob.append("decision colours not even within 1.2 times: " + ", ".join(f"{c} {lead[c]:.1f}" for c in COLORS))
    # the lines
    lf = os.path.join(LIB, "earth_world_lines.py")
    if os.path.exists(lf):
        L = load(lf, "earth_world_lines")

        def lines(where, per, need=2):
            if not isinstance(per, dict):
                prob.append(f"{where}: not a dict by world")
                return
            for wd in WORLDS:
                ls = per.get(wd) or []
                if len(ls) < need:
                    prob.append(f"{where} {wd}: {len(ls)} lines (at least {need})")
                for t in ls:
                    for slot in re.findall(r"\{(\w+)\}", t):
                        if slot not in build.SLOTS | {"act", "age"}:
                            prob.append(f"{where} {wd}: slot {{{slot}}} is not in the game's list")
                    if re.search(r"\b(you|your|yours|yourself)\b", t, re.I):
                        prob.append(f"{where} {wd}: third person, not '{t[:40]}'")
                    words(f"{where} {wd}", t, prob)
        for u in UNITS:
            for z in SIZES:
                lines(f"BECAUSE {u} {z}", getattr(L, "BECAUSE", {}).get(u, {}).get(z))
        for p in PUSHES:
            lines(f"NATION {p}", getattr(L, "NATION", {}).get(p))
        for r in RINGS:
            for lv in LEVELS:
                lines(f"KEPT {r} {lv}", getattr(L, "KEPT", {}).get(r, {}).get(lv))
        lines("CAUSE", getattr(L, "CAUSE", None), 1)
    elif not PART:
        prob.append("no earth_world_lines.py")
    print(f"world answers: asks {sum(asks.values())} ({len({k[0] for k in asks})} spheres), decisions "
          f"{sum(decs.values())} {dict(decs)}, colours leading {dict((c, round(lead[c], 1)) for c in COLORS)}, "
          f"rivals/allies/successor {dict(f3)}")
    for p in prob:
        print("  " + p)
    print(f"{len(prob)} problems" if prob else "no problems")
    sys.exit(1 if prob else 0)


main()
