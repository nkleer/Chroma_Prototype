"""Spheres of society (item 15), phase 1a: copy the design data the engine needs into v22-speedpass/sphere_data.py.

The engine never reads the design folders at run time; this script makes a plain Python copy of the tables, and --check
compares an existing copy with the files (and recomputes the colour-even rows of spheres-implementation.md section 6
that the copy carries).
    python3 -B chroma-engine/tools/sphere_tables.py SPHERES_DATA_DIR [--check]
SPHERES_DATA_DIR is the master copy chroma-world/spheres/data (the nine sphere files, plan.json, epochs.json, dynamics.json,
marks.json; dynamics.json also gives haunt_shares).
Writes (or checks) sphere_data.py beside engine.py in the tree this script sits in."""
import sys, os, json, pprint
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
    SUB, PLACE, EVENTS = {}, {}, []
    for s in SPHERES:
        f = rd(f"{s}.json")
        SUB[s] = [x["key"] for x in f["subsectors"]]
        for x in f["subsectors"]:
            PLACE[f"{s}.{x['key']}"] = {e: x["place_by_epoch"][e] for e in EPOCHS if e in x.get("place_by_epoch", {})}
        for e in f["events"]:
            EVENTS.append((e["key"], s, e["family"], not no_dice(e.get("chance"))))
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
    return dict(SPHERES=SPHERES, COLORS=list(COLS), EPOCHS=EPOCHS, DRIVERS=DRIVERS, FACE_NEEDS=FACE_NEEDS, M0=M0, J=J,
                D=D, MEETS=MEETS, FACE_NAMES=FACE_NAMES, PARAMS=PARAMS, SUBSECTORS=SUB, PLACE_BY_EPOCH=PLACE, EVENTS=EVENTS,
                TEACH=TEACH, TIME=TIME, TIME_AGES=TIME_AGES, TIME_GROUPS=["early", "middle", "machine", "modern"], DEPTH=DEPTH,
                MARKS=MARKS, MARK_TAU=MARK_TAU, MARK_READING=MARK_READING, HAUNT_SHARES=HAUNT_SHARES)


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
