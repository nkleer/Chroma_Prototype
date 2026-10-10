"""Spheres of society (item 15), phase 1a: copy the design data the engine needs into v22-speedpass/sphere_data.py.

The engine never reads the design folders at run time; this script makes a plain Python copy of the tables, and --check
compares an existing copy with the files (and recomputes the colour-even rows of spheres-implementation.md section 6
that the copy carries).
    python3 -B chroma-engine/tools/sphere_tables.py SPHERES_DATA_DIR [--check]
SPHERES_DATA_DIR is the master copy chroma-world/spheres/data (the nine sphere files, plan.json, epochs.json, dynamics.json,
marks.json; dynamics.json also gives haunt_shares).
Writes (or checks) sphere_data.py beside engine.py in the tree this script sits in."""
import sys, os, re, json, pprint
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "v22-speedpass", "sphere_data.py")
SPHERES = ["rule", "gather", "arts", "faith", "care", "learn", "prod", "comm", "prot"]
COLS = "WUBRG"
EPOCHS = ["bands", "villages", "cities", "realms", "sail", "machine", "modern", "magic"]
DRIVERS = ["insecurity", "plenty", "war", "crowding", "inequality", "schooling", "exposure", "change"]
FACE_NEEDS = ["safety", "belonging", "meaning"]


def no_dice(chance):
    """An event's chance field says it has no dice ("none", "None.", "none; ...", "None: ...")."""
    c = str(chance).strip().lower()
    return c.startswith("none") and (len(c) == 4 or c[4] in ".;:, (")


def build(src):
    rd = lambda f: json.load(open(os.path.join(src, f)))
    ep, plan, dyn = rd("epochs.json"), rd("plan.json"), rd("dynamics.json")
    r2 = ep["round2"]
    M0 = {e: [[r2["M0"][e][s][c] for c in COLS] for s in SPHERES] for e in EPOCHS}
    J = {e: r2["J"][e]["matrix"] for e in EPOCHS}
    D = {d: [[plan["drivers"][d][s][c] for c in COLS] for s in SPHERES] for d in DRIVERS}
    MEETS = [[[plan["meets"][s][c][n] for n in FACE_NEEDS] for c in COLS] for s in SPHERES]
    FACE_NAMES = {f"{s}.{c}": plan["face_names"][s][c] for s in SPHERES for c in COLS}
    PARAMS = {x["key"]: x["value"] for x in dyn["params"] if isinstance(x["value"], (int, float, dict, list))}
    SUB, PLACE, EVENTS, EV = {}, {}, [], []
    for s in SPHERES:
        f = rd(f"{s}.json")
        SUB[s] = [x["key"] for x in f["subsectors"]]
        for x in f["subsectors"]:
            PLACE[f"{s}.{x['key']}"] = {e: x["place_by_epoch"][e] for e in EPOCHS if e in x.get("place_by_epoch", {})}
        for e in f["events"]:
            EVENTS.append((e["key"], s, e["family"], not no_dice(e.get("chance"))))
            # phase 3: the whole event as the engine runs it (rows on a sphere's faces; other rows' targets kept for later)
            EV.append(dict(key=e["key"], sphere=s, family=e["family"], dice=bool(e.get("dice", not no_dice(e.get("chance")))),
                           epochs=list(e.get("epochs", [])), hazard={k: float(v) for k, v in e.get("hazard", {}).items()},
                           chains=[[c["key"], c.get("lag", "years")] for c in e.get("chains_to", [])],
                           rows=[dict(target=r["target"], scope=r.get("scope", "local"), tau=float(r.get("tau", 4)),
                                      faces=[int(r["faces"][c]) for c in COLS] if r.get("faces") else None,
                                      state={k: int(v) for k, v in r.get("state", {}).items()},
                                      **({"shadow": [c for c in COLS if c in r["shadow"]]} if r.get("shadow") else {}))
                                 for r in e["effects"]]))
    # phase 2: what each face teaches (its colour mix), and the time budget by life stage and epoch group (hours a week)
    TEACH = [[[float(rd(f"{s}.json")["faces"][c]["teaches"].get(k, 0.0)) for k in COLS] for c in COLS] for s in SPHERES]
    tb = dyn["exposure"]["time_budget"]; rows = [r["row"] for r in tb["rows"]]
    TIME = {st["stage"]: {r: [float(x) for x in str(st[r]).split("/")] for r in rows} for st in tb["stages"]}
    TIME_AGES = {st["stage"]: [int(a) if a.strip().isdigit() else 200 for a in st["ages"].replace(" on", " to 200").split(" to ")]
                 for st in tb["stages"]}
    DEPTH = {r["row"]: float(r["depth"]) for r in tb["rows"]}
    # the mark of the work (marks.json): each subsector's pull on the worker's colours (W U B R G) at the chosen colour
    # reading, its five marks, and the size (k_mark is already inside each pull; tau_years the drawing-in time)
    mk = rd("marks.json")
    MARKS = {f"{r['sphere']}.{r['subsector']}": dict(pull=[float(r["pull"][c]) for c in COLS],
                                                     **{d: float(r[d]) for d in ("say", "routine", "danger", "wear", "skill")})
             for r in mk["rows"]}
    MARK_TAU = float(mk["size"]["tau_years"]); MARK_READING = str(mk["colour_reading"]["chosen"])
    # how common each haunt kind is (dynamics.json haunt_shares): the modern share of adults for whom it is a regular
    # place, read as a prior on the haunt picks (relative weights times fit)
    HAUNT_SHARES = {k: float(v) for k, v in dyn["haunt_shares"]["shares"].items()}
    # phase 3: the year's rhythm (N7; hours and event hazards by season, each row averaging 1), how separate the spheres
    # are in each epoch (N6; effects spill to joined spheres at J x (1 - separation)), the pair faces' rule
    sz = dyn["seasons"]; SEASONS = dict(order=list(sz["order"]), hours={s: [float(x) for x in sz["hours"][s]] for s in SPHERES},
                                         hazards={s: [float(x) for x in sz["hazards"][s]] for s in SPHERES})
    SEPARATION = {x["key"]: float(x["separation"]) for x in ep["ladder"]}
    # phase 3 rates (dynamics.json events_run, Outer world's answers in chroma-engine/notes/spheres-phase3-answers.md):
    # each event's target count a decade in a calm modern town (local rows only) or society (any big row), by family or
    # its override; the world-fired events (the world's own event fires them; no draw of their own); the 74 sphere
    # states, the 16 of them that are world.py variables, and the states' rule (0..1, start .5, .05 a unit, relax .02 a
    # quarter, memory .01 a quarter)
    er = dyn["events_run"]; ft = er["rates"]["family_targets"]; ov = er["rates"]["overrides"]
    wf = er["rates"]["world_fired"]["keys"]
    for e in EV:
        k_ = f"{e['sphere']}.{e['key']}"
        e["target"] = float(ov.get(k_, ft[e["family"]])); e["fired"] = wf.get(k_)
    STATES = sorted({f"{r['target']}.{k}" for e in EV for r in e["rows"] if r["target"] in SPHERES for k in r["state"]})
    STATE_WORLD = sorted(er["states"]["world_vars"])
    STATE_RULE = dict(start=0.5, step=0.05, relax=0.02, mem=0.01)
    # phase 3 (sph_links): the 72 sphere-to-sphere links of links.json, each through its via states ("a, b -> c; d
    # (down)": the from-sphere's states feed the to-sphere's, "(down)" turning that name's sign), with its lag and
    # strength; and the colour readings of those links (colour.by_colour): the faces of faces_in that the link's low side
    # feeds and starves (a row's "side": "high" reads the other way; the opposite side swaps them)
    lk = rd("links.json")
    def via(txt, s):
        return [[f"{s}.{re.sub(r'[(].*?[)]', '', x).strip()}", -1 if "(down)" in x else 1] for x in re.split("[,;]", txt) if x.strip()]
    LINKS = [dict(id=l["id"], frm=l["from"], to=l["to"], lag=l["lag"], strength=int(l["strength"]), sign=l["sign"],
                  src=via(l["via"].split("->", 1)[0], l["from"]), dst=via(l["via"].split("->", 1)[1], l["to"]))
             for l in lk["links"] if l["kind"] == "sphere-sphere"]
    ids = {l["id"] for l in LINKS}
    LINK_COLOUR = [dict(link=r["link_id"], faces_in=r["faces_in"], strength=int(r["strength"]), side=r.get("side", "low"),
                        feeds=sorted(r["feeds"]), starves=sorted(r["starves"]))
                   for r in lk["colour"]["by_colour"] if r["link_id"] in ids]
    # phase 3 (Outer world's answers, chroma-world/spheres/phase3-rest-answers.md): the four memories (events_run.memories:
    # each memory's feeding events and amounts, the events it raises or lowers and by how much, its fade a quarter),
    # each pair's quarrel events (events_run.pair_quarrels, bare keys; a pair face calms its own sphere's), and the 14
    # cascades (colour.cascades: each step's event, bare, or None, and its lag after the step before)
    bare = lambda k: k.split(".")[-1]
    mm = er["memories"]
    MEMORIES = {m: dict(sphere=v["sphere"], feeds={bare(k): float(a) for k, a in v["feeds"].items()},
                        raises={bare(k): float(a) for k, a in v["raises"].items()}) for m, v in mm["memories"].items()}
    MEM_FADE = float(mm["fade"])
    PAIR_QUARRELS = {p: [bare(k) for k in v] for p, v in er["pair_quarrels"]["pairs"].items()}
    CASCADES = [dict(id=c["id"], epochs=list(c["epochs"]), steps=[[bare(st["event"]) if st.get("event") else None, st["lag"]]
                                                                for st in c["steps"]]) for c in lk["colour"]["cascades"]]
    # phase 4 (Outer world's answers, chroma-world/spheres/phase4-answers.md): what an office act fires or moves in each
    # sphere (levers.office.events; event keys bare), and felt fairness (felt_fairness: each sphere's fair and against
    # states, as "sphere.key", and the option multipliers under low and over high)
    oe = dyn["levers"]["office"]["events"]
    LEVER_OFFICE = {sp: {k: ({"event": bare(v["event"])} if "event" in v else {"state": v["state"], "by": float(v["by"])})
                         for k, v in oe[sp].items()} for sp in SPHERES}
    ff = dyn["felt_fairness"]
    FAIR = dict(states={sp: dict(fair=[f"{sp}.{k}" for k in ff["states"][sp]["fair"]],
                                 against=[f"{sp}.{k}" for k in ff["states"][sp]["against"]]) for sp in SPHERES},
                low=float(ff["effects"]["low"]), high=float(ff["effects"]["high"]),
                low_mult={k: float(v) for k, v in ff["effects"]["low_mult"].items()},
                high_mult={k: float(v) for k, v in ff["effects"]["high_mult"].items()})
    # phase 5 (Outer world's answers, chroma-world/spheres/phase5-answers.md): N5's shadow shares and their effects
    # (shadow_state), and the deep state of a life (deep_state: the care load, service, debts, holdings)
    shs = dyn["shadow_state"]
    SHADOW = dict(share={k: float(v) for k, v in shs["share"].items()}, gate=float(shs["library_gate"]["threshold"]))
    ds = dyn["deep_state"]; cl = ds["care_load"]   # (the frail factor, role, public care, stress and work are in its prose)
    DEEP = dict(care_hours={k: float(v) for k, v in cl["hours_week"].items()}, care_frail=0.2, care_frail_x=1.5,
                care_role=0.5, care_public=0.5, care_stress=0.02, care_work=0.1,
                record_weight={k: float(v) for k, v in ds["service"]["record_weight"].items()},
                service=ds["service"], debts=dict(ledger=int(ds["debts"]["ledger"]), holders=ds["debts"]["holders"]),
                holdings=dict(max=int(ds["holdings"]["max"]), kinds=ds["holdings"]["kinds"]))
    return dict(SPHERES=SPHERES, COLORS=list(COLS), EPOCHS=EPOCHS, DRIVERS=DRIVERS, FACE_NEEDS=FACE_NEEDS, M0=M0, J=J,
                D=D, MEETS=MEETS, FACE_NAMES=FACE_NAMES, PARAMS=PARAMS, SUBSECTORS=SUB, PLACE_BY_EPOCH=PLACE, EVENTS=EVENTS,
                TEACH=TEACH, TIME=TIME, TIME_AGES=TIME_AGES, TIME_GROUPS=["early", "middle", "machine", "modern"], DEPTH=DEPTH,
                MARKS=MARKS, MARK_TAU=MARK_TAU, MARK_READING=MARK_READING, HAUNT_SHARES=HAUNT_SHARES, EV=EV,
                SEASONS=SEASONS, SEPARATION=SEPARATION, STATES=STATES, STATE_WORLD=STATE_WORLD, STATE_RULE=STATE_RULE,
                HAZARD_VARS=[v["key"] for v in dyn["drivers"]["vocabulary"] if v["kind"] == "hazard"],
                LINKS=LINKS, LINK_COLOUR=LINK_COLOUR, MEMORIES=MEMORIES, MEM_FADE=MEM_FADE, PAIR_QUARRELS=PAIR_QUARRELS,
                CASCADES=CASCADES, LEVER_OFFICE=LEVER_OFFICE, FAIR=FAIR, SHADOW=SHADOW, DEEP=DEEP)


def audit(T):
    """The colour-even rows the copy carries (section 6, phase 0): each colour's home ways sum to 1.80 in every epoch,
    every sphere's home ways sum to 1, driver rows sum to 0 in every sphere, each face meets .60, the event keys are
    unique. Returns the failures."""
    bad = []
    for e, m in T["M0"].items():
        m = np.asarray(m)
        if np.abs(m.sum(1) - 1).max() > 0.005 or np.abs(m.sum(0) - 1.8).max() > 0.005:
            bad.append(f"M0 {e}: sphere sums {m.sum(1).round(3).tolist()}, colour sums {m.sum(0).round(3).tolist()}")
    for d, w in T["D"].items():
        if np.abs(np.asarray(w).sum(1)).max() > 0:
            bad.append(f"driver {d}: rows {np.asarray(w).sum(1).tolist()}")
    mt = np.asarray(T["MEETS"]).sum(2)
    if np.abs(mt - 0.6).max() > 0.005:
        bad.append(f"meets: face totals {mt.min():.3f} to {mt.max():.3f}")
    te = np.asarray(T["TEACH"]).sum(2)
    if np.abs(te - 1).max() > 0.005:
        bad.append(f"teaches: face totals {te.min():.3f} to {te.max():.3f}")
    pl = np.array([v["pull"] for v in T["MARKS"].values()])
    if len(T["MARKS"]) != 60 or np.abs(pl.mean(0)).max() > 0.0005:
        bad.append(f"marks: {len(T['MARKS'])} subsectors, mean pull {pl.mean(0).round(4).tolist()}")
    hs = T["HAUNT_SHARES"]
    if len(hs) != 31 or min(hs.values()) <= 0 or max(hs.values()) > 1:
        bad.append(f"haunt shares: {len(hs)} kinds, {min(hs.values())} to {max(hs.values())}")
    for kind in ("hours", "hazards"):
        m = np.array([T["SEASONS"][kind][s] for s in SPHERES])
        if np.abs(m.mean(1) - 1).max() > 0.02:
            bad.append(f"seasons {kind}: a sphere's year averages {m.mean(1).round(3).tolist()}")
    if set(T["SEPARATION"]) != set(EPOCHS):
        bad.append(f"separation: epochs {sorted(T['SEPARATION'])}")
    if len(T["STATES"]) != 74 or not set(T["STATE_WORLD"]) <= set(T["STATES"]):
        bad.append(f"states: {len(T['STATES'])}, world ones outside {sorted(set(T['STATE_WORLD']) - set(T['STATES']))}")
    if sum(e["fired"] is not None for e in T["EV"]) != 27 or min(e["target"] for e in T["EV"]) <= 0:
        bad.append("rates: world-fired events or targets")
    ek = {e["key"] for e in T["EV"]}
    miss = sorted({c[0] for e in T["EV"] for c in e["chains"]} - ek)
    if miss:
        bad.append(f"chains to unknown events: {miss[:5]}")
    st_ = set(T["STATES"])
    lb = [l["id"] for l in T["LINKS"] if not all(k in st_ for k, _ in l["src"] + l["dst"]) or not l["src"] or not l["dst"]]
    if len(T["LINKS"]) != 72 or lb:
        bad.append(f"links: {len(T['LINKS'])} sphere to sphere, via states unknown in {lb[:5]}")
    cb = [r["link"] for r in T["LINK_COLOUR"] if r["faces_in"] not in SPHERES or r["side"] not in ("low", "high")
          or not set(r["feeds"] + r["starves"]) <= set(COLS)]
    if cb:
        bad.append(f"colour readings: {cb[:5]}")
    mk_ = sorted({k for m in T["MEMORIES"].values() for k in list(m["feeds"]) + list(m["raises"])} - ek)
    qk_ = sorted({k for v in T["PAIR_QUARRELS"].values() for k in v} - ek)
    ck_ = sorted({st[0] for c in T["CASCADES"] for st in c["steps"] if st[0]} - ek)
    if len(T["MEMORIES"]) != 4 or mk_ or qk_ or ck_ or len(T["PAIR_QUARRELS"]) != 10 or len(T["CASCADES"]) != 14:
        bad.append(f"memories, quarrels, cascades: unknown events {(mk_ + qk_ + ck_)[:5]}")
    ob_ = [(sp, k) for sp, d in T["LEVER_OFFICE"].items() for k, v in d.items()
           if ("event" in v and v["event"] not in ek) or ("state" in v and v["state"] not in st_)]
    fb_ = [k for d in T["FAIR"]["states"].values() for k in d["fair"] + d["against"] if k not in st_]
    if ob_ or fb_ or set(T["LEVER_OFFICE"]) != set(SPHERES):
        bad.append(f"levers: office {ob_[:3]}, fairness states unknown {fb_[:3]}")
    sh_ = T["SHADOW"]["share"]
    if not (0 <= sh_["start"] <= 1 and 0 < sh_["relax"] < 1) or set(T["DEEP"]["care_hours"]) != {"partner", "parent", "parent_in_law", "grandparent"}:
        bad.append("phase 5: shadow share or care hours malformed")
    keys = [k for k, *_ in T["EVENTS"]]
    if len(set(keys)) != len(keys):
        bad.append("event keys repeat")
    return bad


def render(T, src):
    head = ('"""Spheres of society (item 15): the design tables the engine reads, copied from chroma-world/spheres/data/ by\n'
            'tools/sphere_tables.py. Do not edit by hand: change the data and copy again (--check compares).\n'
            'Order of spheres: ' + " ".join(T["SPHERES"]) + '; colours W U B R G."""\n')
    body = "".join(f"{k} = {pprint.pformat(v, width=118, sort_dicts=False)}\n" for k, v in T.items())
    return head + body


if __name__ == "__main__":
    src = sys.argv[1]
    T = build(src)
    bad = audit(T)
    txt = render(T, src)
    if "--check" in sys.argv[2:]:
        same = os.path.exists(OUT) and open(OUT).read() == txt
        print(f"{'SAME' if same else 'DIFFERS'}: {OUT} against {src}")
        bad += [] if same else ["the copy differs from the files"]
    else:
        open(OUT, "w").write(txt)
        print(f"wrote {OUT}: {len(T['EVENTS'])} events ({sum(x[3] for x in T['EVENTS'])} with dice), "
              f"{sum(len(v) for v in T['SUBSECTORS'].values())} subsectors, {len(T['PARAMS'])} parameters")
    print("audit:", "PASS" if not bad else "FAIL " + "; ".join(bad))
    sys.exit(1 if bad else 0)
