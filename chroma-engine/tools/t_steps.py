"""Engine fast check for the pause points (backend plan item 2, 2026-10-08), under a minute on one core.

engine.run_steps() is engine.run() pausing six times a week for the game. On a few short runs this checks that
  1. passing every value back unchanged, run_steps() returns exactly what run() returns (every output, bit for bit);
  2. the pauses come in engine.PAUSES order every week, each with its week number (before age 3 only "week");
  3. every name in engine.STATE is in the state at every pause once a whole week has passed at age 3 or more
     (engine.STATE_IF: names there only when a switch is on, such as titles, checked when it is);
  4. the played-life settings (own_k, drift_k, ev_push_k, era_push_k, steer) do what they say, and at 1 nothing;
  5. the world's reports on a life (wfx, option_causes, a disaster's hazard) fill without changing the lives;
  6. the next update's switches that lives with no player keep off (E.UPD_OFF), switched on: run_steps() still lives
     the lives of run(), and the switch moves something.
  7. the next update's read-only world switches (the spheres' town, sph_town), switched on: the lives are those of a
     run with them off, and the world carries their state.
  8. the spheres' phase 2 switches (haunts, hours and rungs, the mark of the work), switched on with the world: run_steps()
     still lives the lives of run(), and the lives move.
  9. WL2's small effects (wl2: prices for workers, a recession's hours, a disaster's cost, a pandemic year), likewise,
     over lives long enough to hold a job; the sphere events (sph_events, at a test base chance), over phase 2; and the C
     hooks (item 10: c3_inst, c4_nature, c5_faith), likewise.

    python3 -B chroma-engine/tools/t_steps.py [ENGINE_DIR]
ENGINE_DIR defaults to CHROMA_ENGINE, else the engine of the tree this script sits in (tools/_engine.py), with that
tree's Library and packs: run from a checkout of the repository it checks the checkout, from the shared folder the live
engine. Exit code 0 when every check passes."""
import sys, os, hashlib, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
if len(sys.argv) > 1:
    os.environ["CHROMA_ENGINE"] = os.path.abspath(sys.argv[1])
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
ENG = _engine.ENGINE
import numpy as np
import engine as E, batch
import world as _wm
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS


def h(x, hs):
    if isinstance(x, np.ndarray):
        hs.update(str(x.dtype).encode()); hs.update(str(x.shape).encode())
        if x.dtype == object:
            for y in x.ravel():
                h(y, hs)
        else:
            hs.update(np.ascontiguousarray(x).tobytes())
    elif isinstance(x, dict):
        for k in sorted(x, key=repr):
            hs.update(repr(k).encode()); h(x[k], hs)
    elif isinstance(x, (list, tuple)):
        hs.update(b"[%d" % len(x))
        for y in x:
            h(y, hs)
    elif isinstance(x, (set, frozenset)):
        for y in sorted(x, key=repr):
            h(y, hs)
    elif isinstance(x, np.generic):
        hs.update(repr(x.item()).encode())
    else:
        hs.update(repr(x).encode())


def digest(o):
    out = {}
    for k in sorted(o):
        hs = hashlib.md5(); h(o[k], hs); out[k] = hs.hexdigest()
    return out


EARTH = None
RUNS = [  # (label, library, outer world, lives, years, seed)
    ("seed library, world off", "seed", False, 6, 6, 3),
    ("Earth and packs, world off", "earth", False, 4, 5, 7),
    ("Earth and packs, world on", "earth", True, 2, 4, 5),
]
bad = 0
for label, libk, world, N, Y, seed in RUNS:
    t0 = time.process_time()
    if libk == "earth" and EARTH is None:
        EARTH = batch.load_batch("earth", packs=list(batch.PACKS))
    L = EARTH if libk == "earth" else None
    Pd = dict(E.DEFAULT); Pd["world"] = world
    kw = dict(N=N, years=Y, seed=seed, lib=L, P=Pd, log_lives=(0,))
    o1 = E.run(**kw)
    g = E.run_steps(**kw)
    order, missing, weeks, full, want, titles = [], {}, 0, 0, [], False
    msg = next(g)
    while True:
        kind, t, S, val = msg
        if not want:                                   # a new week starts with its "week" pause
            want = list(E.PAUSES) if kind == "week" and S["age"] >= 3 else ["week"]
        exp = want.pop(0)
        if (kind, t) != (exp, weeks) and len(order) < 3:
            order.append(f"week {weeks}: got {kind} at t={t}, expected {exp}")
        if full:
            need = set(E.STATE) | {nm for nm, sw in E.STATE_IF.items() if S.get(sw)}
            titles |= len(need) > len(E.STATE)
            for nm in need - S.keys():
                missing.setdefault(nm, set()).add(kind)
        if not want:
            weeks += 1; full += kind == "end"
        try:
            msg = g.send(val)
        except StopIteration as done:
            o2 = done.value
            break
    d1, d2 = digest(o1), digest(o2)
    diff = sorted(x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x))
    ok = not diff and not order and not missing and not want and weeks == 52 * Y and full > 0
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}: {N} lives x {Y} years, seed {seed}; {weeks} weeks, "
          f"{full} whole weeks; outputs {len(d1)} keys, {'all equal' if not diff else 'DIFFER: ' + ' '.join(diff)}; "
          f"{len(E.STATE)} STATE names{f' and {len(E.STATE_IF)} title names' if titles else ''} {'all there' if not missing else 'MISSING: ' + str({a: sorted(b) for a, b in missing.items()})}"
          f"{'' if not order else '; ORDER: ' + order[0]} ({time.process_time() - t0:.0f} s)")

# 4. the played-life settings (implementation list stage 1), when the engine has them: each does what it says
if "own_k" in E.DEFAULT:
    def drive(L, world, N, Y, seed, P_, at=None):
        """run_steps with settings P_, calling at(kind, S) at each pause; the run's outputs."""
        Pd = dict(E.DEFAULT); Pd["world"] = world; Pd.update(P_)
        g = E.run_steps(N=N, years=Y, seed=seed, lib=L, P=Pd)
        msg = next(g)
        while True:
            kind, t, S, val = msg
            if at:
                at(kind, S)
            try:
                msg = g.send(val)
            except StopIteration as done:
                return done.value
    for label, libk, world, N, Y, seed in RUNS[::2]:
        t0 = time.process_time(); L = EARTH if libk == "earth" else None; fails = []
        o0 = drive(L, world, N, Y, seed, {})
        # (a) at their values of 1 the four weights change nothing (the engine skips them; this guards a slip)
        o1 = drive(L, world, N, Y, seed, dict(own_k=1.0, drift_k=1.0, ev_push_k=1.0, era_push_k=1.0))
        if digest(o0) != digest(o1):
            fails.append("weights at 1 changed the lives")
        # (b) at 0: no own lesson, no random drift, no outside push on the colours
        seen = dict(noise=0.0)
        def at0(kind, S):
            if kind == "end":
                seen["noise"] = max(seen["noise"], float(np.abs(S["noise"]).max()))
        o2 = drive(L, world, N, Y, seed, dict(own_k=0.0, drift_k=0.0, ev_push_k=0.0, era_push_k=0.0), at0)
        ch = np.asarray(o2["chan"])                    # each channel's total push, by person
        if np.abs(ch[:, 0]).max() > 1e-12 or np.abs(ch[:, 8]).max() > 1e-12 or seen["noise"] > 0:
            fails.append(f"at 0: lesson {np.abs(ch[:, 0]).max():.2g}, outside {np.abs(ch[:, 8]).max():.2g}, noise {seen['noise']:.2g}")
        if np.abs(np.asarray(o0["chan"])[:, 8]).max() <= 0:
            fails.append("no outside push in the plain run to compare")
        # (c) the steer: set before each pick toward Blue, it raises every person's expected Blue share of the pick
        # (an exponential tilt by the Blue share never lowers its mean), reports steer_moved, and is spent
        st = dict(weeks=0, down=0, left=0, moved=0)
        def atS(kind, S):
            if kind == "situation":
                S["P"]["steer"] = np.eye(E.C)[1]; S["P"]["steer_k"] = 2.0
            elif kind == "choose":
                b_ = S["m"][:, :, 1]
                eb, eb0 = (S["pr"] * b_).sum(1), (S["pr0"] * b_).sum(1)
                st["weeks"] += 1; st["down"] += int((eb < eb0 - 1e-9).any())
                st["moved"] += int(np.abs(S["steer_moved"]).max() > 0)
                st["left"] += S["P"]["steer"] is not None
        drive(L, world, N, Y, seed, {}, atS)
        if not st["weeks"] or st["down"] or st["left"] or not st["moved"]:
            fails.append(f"steer: {st}")
        bad += bool(fails)
        print(f"{'PASS' if not fails else 'FAIL'}  played-life settings, {label}: weights at 1 the same lives; at 0 no "
              f"lesson, drift or outside push; the steer raised Blue in {st['weeks']} picks, moved {st['moved']} weeks, "
              f"spent each time{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")

# 5. the world in their life (stage 1, WL1 to WL6), when the engine has it: in a game run (run_steps) with the world on,
# the reports fill and have their keys, the option causes come per option, the disaster story names its hazard, and the
# run still lives exactly the lives of run() (which keeps no reports)
if "wfx_step" in E.DEFAULT:
    # seed 3: since the Library's sphere moments (PR #49), seed 2's life meets no disaster in its 30 years
    t0 = time.process_time(); fails = []; N, Y, seed = 1, 30, 3
    Pd = dict(E.DEFAULT); Pd["world"] = True
    kw = dict(N=N, years=Y, seed=seed, lib=EARTH, P=Pd, log_lives=(0,))
    o1 = E.run(**kw)
    g = E.run_steps(**kw); msg = next(g); fx, oc, kinds = 0, 0, set()
    KEYS = {"kind", "channel", "size", "dir", "cause", "age"}
    while True:
        kind, t, S, val = msg
        if kind == "end":
            for e in S["wfx"][0]:
                fx += 1; kinds.add((e["kind"], e["channel"]))
                if not KEYS <= e.keys() or e["size"] == 0 or e["dir"] != ("up" if e["size"] > 0 else "down"):
                    fails.append(f"report {e}")
        elif kind == "choose":
            c_ = S["option_causes"](0)
            if c_ and len(c_) != len(S["L"]["labels"][int(S["s"][0])]):
                fails.append(f"option causes for {len(c_)} options at week {t}")
            oc += sum(len(x) for x in c_)
        try:
            msg = g.send(val)
        except StopIteration as done:
            o2 = done.value
            break
    d1, d2 = digest(o1), digest(o2)
    diff = sorted(x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x))
    if diff:
        fails.append(f"the reports changed the lives: {diff}")
    rd_ = [e["read"] for e in o2["events"][0] if "read" in e and "hazard" in e["read"]]
    if not fx or not oc or not rd_ or any(r["where"] not in ("home", "near") for r in rd_):
        fails.append(f"{fx} reports, {oc} option causes, {len(rd_)} disaster readings with a hazard")
    # WL6's switch: with it on, a disaster at home brings only the events of its hazard (or those naming none)
    import re, world_link
    o3 = E.run(**dict(kw, P=dict(Pd, dis_match=True)))
    for r in (e["read"] for e in o3["events"][0] if "read" in e and e["read"].get("where") == "home"):
        hz_ = {h_ for h_, rx_ in world_link.HAZ_EVR.items() if re.search(rx_, r["name"], re.I)}
        if hz_ and r["hazard"] not in hz_:
            fails.append(f"dis_match: a {r['hazard']} brought {r['name']}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the world in their life, Earth and packs, world on: {N} life x {Y} years, seed "
          f"{seed}; {fx} reports of {len(kinds)} kinds, {oc} option causes, {len(rd_)} disaster readings naming their hazard; "
          f"lives as run(); dis_match runs{'' if not fails else '; ' + '; '.join(fails[:3])} ({time.process_time() - t0:.0f} s)")
# 6. switches of the next update that are off in lives with no player (E.UPD_OFF), when the engine has them: switched on,
# a game run (run_steps) still lives exactly the lives of run(), and the switch moves something
ON_ = [("the times as a steady current", dict(cur_on=True), lambda o: float(np.asarray(o["current"]).sum()) > 0)]
for label, sw, moved in ON_:
    if not set(sw) <= set(E.DEFAULT):
        continue
    t0 = time.process_time(); fails = []
    for world in (False, True):
        Pd = dict(E.DEFAULT); Pd["world"] = world; Pd.update(sw)
        kw = dict(N=2, years=6, seed=4, lib=EARTH, P=Pd)
        o1 = E.run(**kw); g = E.run_steps(**kw); msg = next(g)
        while True:
            try:
                msg = g.send(msg[3])
            except StopIteration as done:
                o2 = done.value
                break
        d1, d2 = digest(o1), digest(o2)
        diff = sorted(x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x))
        if diff:
            fails.append(f"world {'on' if world else 'off'}: run_steps differs in {diff[:4]}")
        if not moved(o1):
            fails.append(f"world {'on' if world else 'off'}: switched on, it moved nothing")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  {label}, switched on: run_steps lives as run(), world off and on"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
# 7. read-only world switches of the next update (the spheres of society, item 15, phase 1c): with the world on, a run with
# the switch on lives exactly the lives of a run with it off, and the world it ran in carries the new state
RO_ = [("the spheres of society, the town (sph_town)", "sph_town",
        lambda W: getattr(W, "sph_s", None) is not None and np.allclose(W.sph_s.sum(-1), 1) and np.allclose(W.sph_Z.sum(-1), 1))]
for label, sw, ok in RO_:
    if sw not in E.DEFAULT or sw not in getattr(_wm, "SPH_RULES", ()):
        continue
    t0 = time.process_time(); fails = []; ds = []
    for on in (False, True):
        W_ = _wm.World(4, cfg=dict(params={sw: on})); W_.burn_in(20)
        Pd = dict(E.DEFAULT); Pd["world"] = True; Pd["world_obj"] = W_; Pd[sw] = on
        ds.append(digest(E.run(N=2, years=6, seed=4, lib=EARTH, P=Pd)))
        if on and not ok(W_):
            fails.append("switched on, the world carries no sphere state")
    diff = sorted(x for x in set(ds[0]) | set(ds[1]) if ds[0].get(x) != ds[1].get(x) and x != "world")   # the world's
    if diff:                                                                                   # own record carries its switch
        fails.append(f"lives differ in {diff[:4]}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  {label}, switched on: lives as with it off, world on"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
# 8 and 9. switches of the spheres' phase 2 (item 15: haunts, hours and rungs, the mark of the work) and WL2 (world on only): switched on,
# a game run (run_steps) lives exactly the lives of run(), and the lives differ from those with the switches off
P2_ = [("the spheres' haunts, hours and marks (sph_haunts, sph_hours, sph_marks)",
        dict(sph_haunts=True, sph_hours=True, sph_marks=True, cur_on=True), dict(cur_on=True), 8),
       ("WL2, the small effects of the world (wl2)", dict(wl2=True), {}, 24),
       ("the sphere events (sph_events, every event at a test base of .01 a quarter)",
        dict(sph_events=True, sph_ev_base=0.01, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the year's rhythm and the joins (sph_seasons, sph_joins; the events at the test base)",
        dict(sph_seasons=True, sph_joins=True, sph_events=True, sph_ev_base=0.01, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, sph_ev_base=0.01, sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the sphere events at their fitted rates, the 74 states and the world-fired events (sph_events)",
        dict(sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), dict(sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the pair faces (sph_pairs)", dict(sph_pairs=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the links between spheres (sph_links, with the events at their fitted rates)",
        dict(sph_links=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the memories, the pairs' calm and the cascades (sph_memory, pair_calm, sph_cascades; the events at the test base)",
        dict(sph_memory=True, pair_calm=True, sph_cascades=True, sph_pairs=True, sph_events=True, sph_ev_base=0.01,
             sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_pairs=True, sph_events=True, sph_ev_base=0.01, sph_haunts=True, sph_hours=True, cur_on=True), 8),
       ("the levers on places and town spheres, and felt fairness (sph_levers, sph_fair; with the events)",
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("the shadow side, the care load, service, debts and holdings (sph_shadow, sph_deep; with the events and the shadows)",
        dict(sph_shadow=True, sph_deep=True, shadows=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(shadows=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("far-off events through ties (far_ties; with the events)",
        dict(far_ties=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("ways to lead and the leader's time in post (lead_ways; with the levers and the events)",
        dict(lead_ways=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 40),
       ("the sphere titles by their own rules (sph_titles)", dict(sph_titles=True), {}, 40),
       ("fairness read five ways (fair_read; with felt fairness and the events)",
        dict(fair_read=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("colour-even institutions (inst_even)", dict(inst_even=True), {}, 24),
       ("the world's gates on the neighbouring stages' everyday moments (near_gate)", dict(near_gate=True), {}, 24),
       ("C4, nature's own year (c4_nature)", dict(c4_nature=True), {}, 24),
       ("C2 rest, the groups' own view and their world moments (c2_groups; with C3 and C5)",
        dict(c2_groups=True, c3_inst=True, c5_faith=True), dict(c3_inst=True, c5_faith=True), 40),
       ("C3, institution events (c3_inst)", dict(c3_inst=True), {}, 24),
       ("C5, new faith movements (c5_faith)", dict(c5_faith=True), {}, 24),
       ("late births by age and sex (birth_age)", dict(birth_age=True), {}, 30),
       ("the K2 and K6 rule fixes, moves near and far and season steps at their shares (move_near, season_excl)",
        dict(move_near=True, season_excl=True), {}, 30)]
for label, sw, base, yrs in P2_:
    if not set(sw) - {"sph_ev_base"} <= set(E.DEFAULT):
        continue
    t0 = time.process_time(); fails = []
    Pd = dict(E.DEFAULT); Pd["world"] = True; Pd.update(sw)
    kw = dict(N=2, years=yrs, seed=4, lib=EARTH, P=Pd)
    o1 = E.run(**kw); g = E.run_steps(**kw); msg = next(g)
    while True:
        try:
            msg = g.send(msg[3])
        except StopIteration as done:
            o2 = done.value
            break
    d1, d2 = digest(o1), digest(o2)
    diff = sorted(x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x))
    if diff:
        fails.append(f"run_steps differs in {diff[:4]}")
    d0 = digest(E.run(**dict(kw, P=dict(E.DEFAULT, world=True, **base))))
    if not [x for x in set(d0) | set(d1) if d0.get(x) != d1.get(x) and x != "world"]:
        fails.append("switched on, the lives are those with it off")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  {label}, switched on: run_steps lives as run(), world on; the lives move"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
print("engine", ENG, "engine.py", hashlib.md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12])
print("ALL PASS" if not bad else f"{bad} FAILED")
sys.exit(1 if bad else 0)
