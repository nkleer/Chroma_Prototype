"""Engine check for the pause points (backend plan item 2, 2026-10-08) and each switch's own rows: 74 rows, about an hour
(50 to 65 min measured 10-17: the Engine with T_JOBS=4, Release on #288).

engine.run_steps() is engine.run() pausing six times a week for the game. On a few short runs this checks that
  1. passing every value back unchanged, run_steps() returns exactly what run() returns (every output, bit for bit);
  2. the pauses come in engine.PAUSES order every week, each with its week number (before age 3 only "week");
  3. every name in engine.STATE is in the state at every pause once a whole week has passed at age 3 or more
     (engine.STATE_IF: names there only when a switch is on, such as titles, checked when it is); the state is one dict
     for the run, and at each pause every name in it holds the run's own value (the frame's, the same object);
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
 10. v22.5's own ways (own_open, F12) on the seed library the clan plays, with the Library's worlds.py OWN: likewise.
 11. after every row, no name outside STATE, STATE_IF and STATE_MORE was read at a pause (engine.STATE_MISSED).
 12. the world's burn-in kept (world_link.burned_world): a second run of the same world starts from the kept one and
     lives the same lives as the first, which burned it in.
 13. picks come back (echo_play, the game's played-life hook): switched on and never asked, the lives of it off; a return
     moment (tier: return) in the files changes nothing while batch.RETURN_MOMENTS is off; on and asked at every pick, the
     asked picks' marks plant seeds, each comes back at most once, a year on or more, as a moment of its kind and side,
     in the week the pauses say, and the return moment comes only as a return; a logged life's marks are all in its
     events, on and asked or off.
 14. the town gone grey (grey_gate, the spheres finishing pack's part 5), switched on, world on: with no moment of the
     Library's shadow: gate, the lives of it off and the towns' grey shares read each year; a moment given the gate
     comes only while their town's share is at least the threshold (never with the switch off); with the threshold at
     the run's median town share, an everyday moment given the gate opens and shuts by the week and is met only in weeks
     it was open.
 15. the finishing pack's behaviour (v22.6 bar W2 to W4; world on): a place's closing frees its regulars (the haunt and
     a setting held there gone), steps their rung in its sphere down one (not below 0) and ends any post leading it (the
     check closes a led place now and then); care seeking follows trust in care's bodies (more trust, more care; none
     before trust starts); a release makes 1 or 2 ties a year inside (cap 6) at strength .3, each ended within 10 years;
     the pull back is on only with an active tie, the shadow part over its line and neither a partner nor steady work,
     and moves only the options that break the law, at odds x the data's 1.2.
 16. every change has a cause (role_why, the game's played-life hook): switched on, the lives and the logged lives'
     events of it off (but the causes); every title or perk a logged life gains in time, or loses as time passed or
     slipped away, carries its cause, and every history item named is before the change and inside the rule's window;
     asrc (what moved the want, by source) and the played life's asrc_c are handed over at the pauses.
 17. bold ways (bold_play, the game's played-life hook), on a made-up BOLD table and links: switched on and never asked,
     the lives of it off; asked at every pick, run_steps() lives as run(); asked by the game, the character and the game
     take bold ways, at the odds bold_now told (between .1 and .9), each bold pick outside a link's week plants one seed
     of its kind and side, at most bold_cap due, and the links come back of their side, inside their delay (and a
     season), a shared link only with no own link open, and only as links; the bold way's win comes "through" it.
 18. because of you, and meanwhile (need_why, the game's played-life record): switched on, the lives of it off (world off
     and on, run() and run_steps()); every week the record starts empty at the "week" pause and its sources sum to the
     week's change in each need at the "end" pause; a setback carries its kind; what the caller sets at a pause is the
     player's (at most what was set); off, no record. The hover arrows (foresee.arrows) read at every pick change no
     life, and the picked option's need arrows come within one size of the record's act share.
 19. needs that fit life (need_tab "v7", shared_hist, imp_age): each switched on, run_steps() lives as run() and the
     lives move; no setback comes before its age (realm_earth.IMP_AGE); with the v7 tables a partnership gives meaning.

    python3 -B chroma-engine/tools/t_steps.py [ENGINE_DIR]
T_JOBS=N: the rows of 8 and 9 on N processes (default up to 4, by the cores there are; 1: one after another).
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
    S0, other = None, []   # the state is one dict for the run, each name the frame's own value at the pause
    msg = next(g)
    while True:
        kind, t, S, val = msg
        S0 = S if S0 is None else S0
        if S is not S0 and len(other) < 3:
            other.append(f"week {weeks} {kind}: a new state dict")
        fl_ = g.gi_frame.f_locals
        for nm in [nm for nm in S.keys() if nm in fl_ and dict.__getitem__(S, nm) is not fl_[nm]][:3 - len(other)]:
            other.append(f"week {weeks} {kind}: {nm} is not the run's")
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
    ok = not diff and not order and not missing and not want and weeks == 52 * Y and full > 0 and not other
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}: {N} lives x {Y} years, seed {seed}; {weeks} weeks, "
          f"{full} whole weeks; outputs {len(d1)} keys, {'all equal' if not diff else 'DIFFER: ' + ' '.join(diff)}; "
          f"{len(E.STATE)} STATE names{f' and {len(E.STATE_IF)} title names' if titles else ''} {'all there' if not missing else 'MISSING: ' + str({a: sorted(b) for a, b in missing.items()})}"
          f"{'' if not order else '; ORDER: ' + order[0]}{'' if not other else '; STATE: ' + '; '.join(other)} ({time.process_time() - t0:.0f} s)")

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
    # the first seed from 3 whose life meets a disaster in its 30 years (a fixed seed lost its disaster whenever the lives
    # changed: seed 2 at the Library's sphere moments, PR #49, seed 3 at the v22.4 refit)
    t0 = time.process_time(); fails = []; N, Y = 1, 30
    Pd = dict(E.DEFAULT); Pd["world"] = True
    for seed in range(3, 13):
        kw = dict(N=N, years=Y, seed=seed, lib=EARTH, P=Pd, log_lives=(0,))
        o1 = E.run(**kw)
        if any("read" in e and "hazard" in e["read"] for e in o1["events"][0]):
            break
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
# 12. the world's burn-in kept (world_link.burned_world): a second run of the same world, seed and settings starts from
# the World the first one burned in (a deep copy) and lives exactly its lives; checked from memory, with no folder
import world_link as _wlk
if hasattr(_wlk, "burned_world"):
    t0 = time.process_time(); fails = []
    cdir_ = os.environ.pop("CHROMA_WORLD_CACHE", None)
    _wlk.BURN.clear(); h0_ = _wlk.BURN_HITS[0]
    kw = dict(N=2, years=4, seed=17, lib=EARTH, P=dict(E.DEFAULT, world=True))
    d1 = digest(E.run(**kw)); d2 = digest(E.run(**kw))
    if cdir_ is not None:
        os.environ["CHROMA_WORLD_CACHE"] = cdir_
    if _wlk.BURN_HITS[0] != h0_ + 1:
        fails.append(f"{_wlk.BURN_HITS[0] - h0_} runs from the kept world, not 1")
    diff = sorted(x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x))
    if diff:
        fails.append(f"lives differ in {diff[:4]}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the world's burn-in kept: a second run of the same world lives the first's "
          f"lives{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
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
        Pd = dict(E.DEFAULT, **E.UPD_OFF); Pd["world"] = True; Pd["world_obj"] = W_; Pd[sw] = on   # the rest off, as written
        ds.append(digest(E.run(N=2, years=6, seed=4, lib=EARTH, P=Pd)))
        if on and not ok(W_):
            fails.append("switched on, the world carries no sphere state")
    diff = sorted(x for x in set(ds[0]) | set(ds[1]) if ds[0].get(x) != ds[1].get(x) and x != "world")   # the world's
    if diff:                                                                                   # own record carries its switch
        fails.append(f"lives differ in {diff[:4]}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  {label}, switched on: lives as with it off, world on"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
def _pt_closed(o):
    """place_turnover moved something: some place closed (the run's place_turnover log; a function, not a lambda, so a
    row goes to the T_JOBS processes)."""
    return any(e_["what"] == "closed" for e_ in o.get("place_turnover") or ())


def _pt_made(o):
    """prison_ties' own test: former inmates were made ties (a plain function: the rows go to the worker processes)."""
    return any(e["what"] == "made" for e in o.get("prison_ties", ()))


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
       ("the finishing pack's former inmates as ties (prison_ties; every life serves a 3-year term at 18, the shadows on in "
        "the world)", dict(prison_ties=True, prison_par=dict(years_unknown=2.0, cap=6, active=0.02, pull=None, shadow=0.5, test=(18, 3)),
                          sh_world=True),
        dict(prison_par=dict(years_unknown=2.0, cap=6, active=0.02, pull=None, shadow=0.5, test=(18, 3)), sh_world=True), 30, 4,
        _pt_made),   # (ties made, and the lives move beyond the readout)
       ("their places' eyes and the odd one out (sph_eyes, sph_odd; with the haunts and the events)",
        dict(sph_eyes=True, sph_odd=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("v22.5 S4, the spread of their places learnt over a life (eyes_par odd_vmem; with the eyes and the odd one out)",
        dict(eyes_par=dict(odd_vmem=0.05), sph_eyes=True, sph_odd=True, sph_events=True, sph_haunts=True, sph_hours=True,
             cur_on=True),
        dict(sph_eyes=True, sph_odd=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 40, 10),
       ("ways to lead and the leader's time in post (lead_ways; with the levers and the events)",
        dict(lead_ways=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 40, 10),
       # (10 lives: with v22.3's DEFAULT the row's two lives hold no post in 80 years, so lead_ways had nothing to move)
       ("sacred lines (sacred; with the events and C3; lines quick to form, offers to all they fit, decided off-screen)",
        dict(sacred=True, sacred_par=dict(lead=1.0, paid=0, age=12.0, reach=1.0, c3_reach=1.0), sph_events=True, c3_inst=True,
             sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_events=True, c3_inst=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("places close and open (place_turnover; with the haunts, the levers and the events; some place closed)",
        dict(place_turnover=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24, 2,
        _pt_closed),
       ("seen it done (seen_done; with the haunts)",
        dict(seen_done=True, sph_haunts=True, sph_hours=True, cur_on=True), dict(sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("the sphere titles by their own rules (sph_titles)", dict(sph_titles=True), {}, 40),
       ("fairness read five ways (fair_read; with felt fairness and the events)",
        dict(fair_read=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True),
        dict(sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True), 24),
       ("trust in a sphere's bodies (body_trust; with felt fairness, the levers, the events and C3)",
        dict(body_trust=True, fair_read=True, sph_levers=True, sph_fair=True, sph_events=True, c3_inst=True, sph_haunts=True,
             sph_hours=True, cur_on=True),
        dict(fair_read=True, sph_levers=True, sph_fair=True, sph_events=True, c3_inst=True, sph_haunts=True, sph_hours=True,
             cur_on=True), 40, 6),
       ("colour-even institutions (inst_even)", dict(inst_even=True), {}, 24),
       ("the world's gates on the neighbouring stages' everyday moments (near_gate)", dict(near_gate=True), {}, 24),
       ("C4, nature's own year (c4_nature)", dict(c4_nature=True), {}, 24),
       ("C2 rest, the groups' own view and their world moments (c2_groups; with C3 and C5)",
        dict(c2_groups=True, c3_inst=True, c5_faith=True), dict(c3_inst=True, c5_faith=True), 40),
       ("C3, institution events (c3_inst)", dict(c3_inst=True), {}, 24),
       ("C5, new faith movements (c5_faith)", dict(c5_faith=True), {}, 24),
       ("late births by age and sex (birth_age)", dict(birth_age=True), {}, 60),
       ("the K2 and K6 rule fixes, moves near and far and season steps at their shares (move_near, season_excl)",
        dict(move_near=True, season_excl=True), {}, 30),
       ("what one holds is practice too (role_practice)", dict(role_practice=True), {}, 30),
       ("expertise reads the moment (read_skill)", dict(read_skill=0.5), {}, 30),
       ("the lens looks through who one is becoming (lens_want)", dict(lens_want=0.5), {}, 30),
       ("appraisal in learning as vigilance (app_vigil)", dict(app_vigil=True), {}, 30),
       ("the shadow's pull gives way to the will (sh_will; with the shadows on in the world, sh_world)",
        dict(sh_will=0.5, sh_world=True), dict(sh_world=True), 30),
       ("the will tempers the current (cur_will; with the current, cur_on)", dict(cur_will=1.0, cur_on=True), dict(cur_on=True), 30),
       ("a gap one acts to close weighs less (gap_move)", dict(gap_move=0.5), {}, 30),
       ("a refused first job or job move re-draws to the next-best fit (acc_redraw)", dict(acc_redraw=True), {}, 40),
       ("a body and a mind (body, mind)", dict(body=True, mind=True), {}, 30),
       ("death from the life (death_life; with the body, the mind and the character's own death)",
        dict(death_life=True, body=True, mind=True, self_death=True), dict(body=True, mind=True, self_death=True), 70, 6),
       # v22.5, the many-lives fixes (F14 to F17, F19), each at the value the refit starts from
       ("colours settle with age (set_age, F14)", dict(set_age=((30, 1.0), (50, 0.3), (70, 0.1))), {}, 40),
       ("the start leaves a lean (up_lean, up_self, up_ease, F15; a start of W.6 G.4)",
        dict(up_mix=(0.6, 0.0, 0.0, 0.0, 0.4), up_lean=0.006, up_self=0.05, up_ease=0.8), {}, 30),
       ("colours shape the life course (course, F16)", dict(course=True), {}, 40),
       ("deeds by canon (deed_canon, deed_rare, F17)", dict(deed_canon=1.0, deed_rare=0.15), {}, 30),
       ("a mind that matches life (mind_kid, mind_u, F19)",
        dict(mind_kid=((10, 0.5), (18, 1.0)), mind_u=((45, 0.0), (50, -0.15), (58, 0.0), (68, 0.45), (80, 0.6))), {}, 30),
       # v22.5 realism (chroma-ideas/realism/v22.5-realism-list.md)
       ("F6, dreams that grow up (dream_grow)", dict(dream_grow=True), {}, 20),
       ("F12, a start that holds (start_hold; the devout village start, one life as the game plays it)",
        dict(start_hold=True, faith_inherit=1.0, world_cfg=dict(setting="earth", start=dict(
            place="village", wealth=0.2, faith="held", hard=False, society=[0.6, 0, 0, 0, 0.4]))),
        dict(faith_inherit=1.0), 10, 1),
       ("v22.5 F3, the household's money and ties from the people around them (hh_money, ties_people)",
        dict(hh_money=True, ties_people=True), {}, 30),
       ("v22.5 F7, one roll of the living (one_roll)", dict(one_roll=True), {}, 40),
       ("v22.5 F8, retirement ends work (retire_ends)", dict(retire_ends=True), {}, 80, 6),
       ("v22.5 F10, a world moment only on the world's event (world_only)", dict(world_only=True), {}, 30),
       # v22.5 refit round 2 (F9.20, F9.38 to F9.40), at the refit's values (V225)
       ("v22.5 round 2, loneliness, low pay, a job gap, a couple's pay, colour-leaned pay and ties, a child's ties, firm crises "
        "(lone, low_pay, pay_col, job_gap, pair_pay, mon_drift, tie_col, kid_tie, c_par)",
        {k_: E.V225[k_] for k_ in ("lone", "low_pay", "pay_col", "job_gap", "pair_pay", "mon_drift", "tie_col", "kid_tie", "c_par")
         if k_ in getattr(E, "V225", {})}, {}, 40, 6),
       ("v22.5 G19w, the company a life picks (soc_own)", dict(soc_own=0.2), {}, 30),
       ("v22.5 G19w, practice is shared among the skills in the same ways (skill_room)", dict(skill_room=1.0), {}, 40, 8),
       ("v22.5 round 2, a pension's spread, the help after a long hard spell, deaths at work (pen_pay, low_net, work_die)",
        dict(pen_pay=0.5, low_net=(3.0, 0.1, 1.0), work_die=0.00007), {}, 70, 6),
       ("v22.5 round 3, a home bought again only years later (ev_gapfit)", dict(ev_gapfit={"buying a home": (3, 8)}), {}, 70, 10),
       ("v22.5 round 3d, a lasting illness at its own rates by age (age_pts)",
        dict(age_pts={"living with a chronic illness": ((0, 0.0045), (40, 0.01), (80, 0.05))}), {}, 70, 10)]
# a switch's own readouts, which are not the lives (the finishing pack's)
OWN_KEYS_ = ("world", "place_turnover", "pt_lives", "btrust", "btrust_y", "prison_ties", "grey_y")


def p2_row(row_):
    """One row of 8 and 9: (failed, its line), or None when the engine lacks its switches."""
    label, sw, base, yrs = row_[:4]; n_ = row_[4] if len(row_) > 4 else 2   # (a row may name its lives, and a test
    moved = row_[5] if len(row_) > 5 else None                                # that the switch moved what it moves)
    if not sw or not set(sw) - {"sph_ev_base"} <= set(E.DEFAULT):
        return None
    t0 = time.process_time(); fails = []
    Pd = dict(E.DEFAULT); Pd["world"] = True; Pd.update(sw)
    kw = dict(N=n_, years=yrs, seed=4, lib=EARTH, P=Pd)
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
    off_ = {k: E.UPD_OFF[k] for k in sw if k in E.UPD_OFF}   # off as the go-live has it (the v22.3 DEFAULT has them on)
    d0 = digest(E.run(**dict(kw, P=dict(E.DEFAULT, world=True, **dict(off_, **base)))))
    if not [x for x in set(d0) | set(d1) if d0.get(x) != d1.get(x) and x not in OWN_KEYS_]:
        fails.append("switched on, the lives are those with it off")   # (a switch's own readouts are not the lives)
    if moved is not None and not moved(o1):
        fails.append("switched on, it moved nothing")
    return bool(fails), (f"{'PASS' if not fails else 'FAIL'}  {label}, switched on: run_steps lives as run(), world on; the lives move"
                         f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")


# the rows are independent: T_JOBS processes (default up to 4, the cores there are) run them, printed in their order
_jobs = int(os.environ.get("T_JOBS") or min(4, os.cpu_count() or 1))
if _jobs > 1:
    import multiprocessing as _mp
    with _mp.get_context("fork").Pool(_jobs) as _pool:
        _res = _pool.map(p2_row, P2_, chunksize=1)
else:
    _res = map(p2_row, P2_)
for r_ in _res:
    if r_ is not None:
        bad += r_[0]
        print(r_[1], flush=True)
# 10. v22.5, F12: a culture's own acts always on offer (own_open) in the clan, on the seed library with the Library's
# worlds.py OWN (as the game attaches them): run_steps lives as run(), and the lives move
_wpy = os.path.join(_engine.LIBRARY, "worlds.py")
if "own_open" in E.DEFAULT and hasattr(batch, "own_ways") and os.path.isfile(_wpy):
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("chroma_worlds", _wpy); _wd = _iu.module_from_spec(_sp); _sp.loader.exec_module(_wd)
    t0 = time.process_time(); fails = []
    kw = dict(N=40, years=30, seed=4, lib=batch.own_ways(E.compile_library(), _wd.OWN["tribal"]))
    o1 = E.run(**kw, P=dict(E.DEFAULT, own_open=True)); g = E.run_steps(**kw, P=dict(E.DEFAULT, own_open=True)); msg = next(g)
    while True:
        try:
            msg = g.send(msg[3])
        except StopIteration as done:
            o2 = done.value
            break
    d1, d2 = digest(o1), digest(o2)
    if [x for x in set(d1) | set(d2) if d1.get(x) != d2.get(x)]:
        fails.append("run_steps differs")
    d0 = digest(E.run(**kw, P=dict(E.DEFAULT, own_open=False)))
    if not [x for x in set(d0) | set(d1) if d0.get(x) != d1.get(x)]:
        fails.append("switched on, the lives are those with it off")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  F12, the clan's own acts always on offer (own_open), switched on: run_steps lives "
          f"as run(); the lives move{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
# 13. picks come back (echo_play)
if "echo_play" in E.DEFAULT and "more" in batch.load_batch.__code__.co_varnames:
    import copy
    t0 = time.process_time(); fails = []
    kw = dict(N=2, years=20, seed=6)
    d_off = digest(E.run(**kw, lib=EARTH, P=dict(E.DEFAULT)))
    d_on = digest(E.run(**kw, lib=EARTH, P=dict(E.DEFAULT, echo_play=True)))
    if [x for x in set(d_off) | set(d_on) if d_off.get(x) != d_on.get(x) and x != "returns"]:
        fails.append("on and never asked, the lives move")
    RET = dict(copy.deepcopy(next(x for x in EARTH["src"] if x["name"] == "the same chance comes round again")),
               name="t_steps: the same chance, back", tier="return", of="turned down a chance")
    RET.pop("variant_of", None)
    L_ = batch.load_batch("earth", packs=list(batch.PACKS), more=[RET])
    if L_["S"] != EARTH["S"] or digest(E.run(**kw, lib=L_, P=dict(E.DEFAULT))) != d_off:
        fails.append("a return moment in the files moved the lives with RETURN_MOMENTS off")
    batch.RETURN_MOMENTS = True
    try:
        L_ = batch.load_batch("earth", packs=list(batch.PACKS), more=[RET])
    finally:
        batch.RETURN_MOMENTS = False
    R_ = L_["names"].index(RET["name"])
    P_ = dict(E.DEFAULT, echo_play=True, echo_play_par=dict(E.DEFAULT["echo_play_par"], p=1.0, w=1.0, delay=(1.0, 1.2),
                                                             gap=0.0, again=0.0))
    g = E.run_steps(N=1, years=40, seed=6, lib=L_, P=P_, log_lives=(0,)); msg = next(g); told = []
    while True:
        kind, t, S, val = msg
        if kind == "choose" and S["age"] >= 8:
            S["P"]["echo_asked"] = True
            if S["ep_now"][0] >= 0:
                told.append((t, int(S["ep_now"][0]), int(S["s"][0])))
        try:
            msg = g.send(val)
        except StopIteration as done:
            o_ = done.value
            break
    sd_ = o_["returns"]; got_ = [x for x in sd_ if x["got"] is not None]
    if len(sd_) < 3 or len(got_) < 2:
        fails.append(f"{len(sd_)} seeds, {len(got_)} returns")
    if sorted((x["done"], i_, x["got"]) for i_, x in enumerate(sd_) if x["got"] is not None) != sorted(told):
        fails.append("the returns are not the weeks' moments")
    if len({i_ for _, i_, _ in told}) != len(told):
        fails.append("a seed came back twice")
    if any(x["done"] - x["t"] < 52 for x in got_):
        fails.append("a return within a year")
    if any(L_["src"][x["got"]].get("tier") not in ("echo", "return") for x in got_):
        fails.append("a return that is no echo or return moment")
    if int(o_["sit_n"][0, R_]) != sum(x["got"] == R_ for x in got_):
        fails.append("the return moment came other than as a return")
    o0_ = E.run(**kw, lib=EARTH, P=dict(E.DEFAULT), log_lives=(0, 1))
    for o_m, n_ in [(o_, 1)] + [(o0_, 2)]:   # a logged life's marks are told, on and asked or off (Gamification 10-17)
        if sum("mark" in x for i_ in range(n_) for x in o_m["events"][i_]) != len(o_m["marks"]["log"]):
            fails.append("a logged life's marks are not all in its events")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  picks come back (echo_play): on and never asked, the lives of it off; a return "
          f"moment in the files changes nothing with it off; asked, {len(sd_)} seeds, {len(got_)} returns "
          f"({sum(x['got'] == R_ for x in got_)} the return moment), each once and a year on"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
# 14. the town gone grey (grey_gate)
if "grey_gate" in E.DEFAULT:
    t0 = time.process_time(); fails = []
    kw = dict(N=6, years=25, seed=9, lib=EARTH)
    d0 = digest(E.run(**kw, P=dict(E.DEFAULT, world=True)))
    o_ = E.run(**kw, P=dict(E.DEFAULT, world=True, grey_gate=True))
    d1 = digest(o_)
    if [x for x in set(d0) | set(d1) if d0.get(x) != d1.get(x) and x != "grey_y"]:
        fails.append("with no shadow: moment the lives move")
    if np.shape(o_.get("grey_y")) != (6, 25, 9):
        fails.append(f"grey_y is {np.shape(o_.get('grey_y'))}, not lives x years x 9")
    L_ = dict(EARTH); tg_ = L_["names"].index("tending an allotment")
    L_["W_SHADOW"] = np.full(L_["S"], -1); L_["W_SHADOW"][tg_] = 9          # gated on the town's greyest sphere
    met_ = {}
    for on_ in (False, True):
        o2_ = E.run(**dict(kw, lib=L_), P=dict(E.DEFAULT, world=True, grey_gate=on_))
        met_[on_] = int(o2_["sit_n"][:, tg_].sum())
    if met_[False]:
        fails.append(f"the gated moment came {met_[False]} times with the switch off")
    # the gate opening (v22.6 bar W5): the threshold at the run's median town share (its greyest sphere, yearly), an
    # everyday moment given the gate; each week's open lives (moment_factor) and each meeting (sit_last) are read
    import sphere_data as _sd, world_link as _wl
    thr_ = float(np.median(np.asarray(o_["grey_y"]).max(2))); thr0_ = _sd.SHADOW.get("grey_gate")
    nm_ = next((x for x in ("awake at night worrying about the future", "a deadline at college or work") if x in L_["names"]),
               "tending an allotment")
    tg_ = L_["names"].index(nm_); L_["W_SHADOW"] = np.full(L_["S"], -1); L_["W_SHADOW"][tg_] = 9
    gw_ = dict(open=set(), shut=0, met=0, wrong=0, last=None)
    mf0_ = _wl.WorldLink.moment_factor
    def _mf(self, age, sit_last=None):
        t_ = int(sys._getframe(1).f_locals["t"])
        if sit_last is not None:
            sl_ = np.asarray(sit_last)[:, tg_]
            if gw_["last"] is not None:
                for n_ in np.nonzero(sl_ != gw_["last"])[0].tolist():
                    gw_["met"] += 1; gw_["wrong"] += (n_, int(sl_[n_])) not in gw_["open"]
            gw_["last"] = sl_.copy()
        f_ = mf0_(self, age, sit_last)
        op_ = f_[:, tg_] > 0
        gw_["open"].update((n_, t_) for n_ in np.nonzero(op_)[0].tolist()); gw_["shut"] += int((~op_).sum())
        return f_
    _sd.SHADOW["grey_gate"] = thr_; _wl.WorldLink.moment_factor = _mf
    try:
        o3_ = E.run(**dict(kw, lib=L_), P=dict(E.DEFAULT, world=True, grey_gate=True))
    finally:
        _wl.WorldLink.moment_factor = mf0_
        if thr0_ is None:
            _sd.SHADOW.pop("grey_gate", None)
        else:
            _sd.SHADOW["grey_gate"] = thr0_
    met3_ = int(o3_["sit_n"][:, tg_].sum())
    if not met3_ or not gw_["open"] or not gw_["shut"]:
        fails.append(f"at threshold {thr_:.3f} the gate did not both open and shut and let the moment come "
                     f"({len(gw_['open'])} open, {gw_['shut']} shut life-weeks, met {met3_})")
    if gw_["wrong"]:
        fails.append(f"met {gw_['wrong']} times in a week the gate was shut")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the town gone grey (grey_gate), switched on: with no shadow: moment the lives "
          f"of it off, grey shares read yearly; a gated moment came {met_[True]} times on, {met_[False]} off; at the median "
          f"town share {thr_:.3f}, {nm_!r} open {len(gw_['open'])} and shut {gw_['shut']} life-weeks, met {met3_} times, "
          f"{gw_['met']} of them seen by the probe (week by week), {gw_['wrong']} in a shut week"
          f"{'' if not fails else '; ' + '; '.join(fails)} ({time.process_time() - t0:.0f} s)")
# 15. the finishing pack's behaviour (v22.6 bar W2 to W4), on one world-on run with the parts on, read where they act
if "place_turnover" in E.DEFAULT and hasattr(E, "bt_care") and hasattr(E, "pt_pull_of"):
    import world_people as _wp, sphere_data as _sd
    t0 = time.process_time(); fails = []
    # care seeking's direction, on its own: more trust in care's bodies, more care sought; .5 and no trust yet leave it
    ln_ = np.repeat(np.linspace(-0.9, 0.9, 19), 5); bc_ = np.tile([0.0, 0.25, 0.5, 0.75, 1.0], 19)
    cv_ = E.bt_care(ln_, bc_).reshape(19, 5)
    if (np.diff(cv_, axis=1) < 0).any() or not (cv_[:, 4] > cv_[:, 0]).all():
        fails.append("care seeking does not rise with trust")
    if not np.allclose(cv_[:, 2], ln_.reshape(19, 5)[:, 2]) or not np.allclose(E.bt_care(ln_, np.full(len(ln_), np.nan)), ln_):
        fails.append("trust .5 or not yet started moves care seeking")
    b_ = np.array([False, True])
    for a_, sh_, pa_, st_ in [(a_, sh_, pa_, st_) for a_ in b_ for sh_ in (0.1, 0.4) for pa_ in b_ for st_ in b_]:
        if bool(E.pt_pull_of(np.array([a_]), np.array([sh_]), 0.3, np.array([pa_]), np.array([st_]))[0]) != \
                bool(a_ and sh_ > 0.3 and not pa_ and not st_):
            fails.append("the pull back's rule is not tie, shadow over the line, no partner, no steady work")
            break
    R_ = dict(hits=0, steps=0, posts=0, forced=0, care=0, pull=0, freed=0, pull_u=0, c=set(), why={})
    TV_ = _sd.DEEP["service"]["after_prison"]["tie_values"]
    q0_, b0_, p0_, u0_, a0_, e0_ = (_wp.People._pt_q, E.bt_care, E.pt_pull_of, E.pt_pull_u, _wp.People._add,
                                     _wp.People._lead_end)
    def _ptq(self, t):
        if self.lw and R_["forced"] < 3:   # a post at a closing is rare: the check closes a led place now and then
            W_ = self.W
            for po_ in self.lw_posts:
                if po_["kind"] == "place" and po_["place"] >= 0:
                    l_, h_, i_ = (int(x_) for x_ in np.unravel_index(int(po_["place"]), W_.pt_open.shape))
                    if W_.pt_open[l_, h_, i_] < 0:
                        W_._pt_close(l_, h_, i_, int(W_.t // 13), "check"); R_["forced"] += 1
                        break
        new_ = [e_ for e_ in (getattr(self.W, "pt_log", None) or [])[self._pt_i:] if e_["what"] == "closed"]
        if not new_:
            return q0_(self, t)
        r0_ = self.rung.copy(); h0_ = self.hnt.copy(); s0_ = self.shnt.copy()
        ps0_ = [po_["place"] for po_ in self.lw_posts] if self.lw else []
        ex_ = r0_.copy(); who_ = []
        for e_ in new_:
            p_ = int(e_["place"]); j_ = _wp.SPHERES.index(e_["kind"].split(".")[0])
            w_ = np.nonzero(~self.dead & ((h0_ == p_).any(1) | (s0_ == p_).any(1)))[0]
            who_.append((p_, j_, w_))
            for n_ in w_.tolist():
                ex_[n_, j_] = max(0.0, ex_[n_, j_] + self._pt_par["rung_step"])
        q0_(self, t)
        for p_, j_, w_ in who_:
            for n_ in w_.tolist():
                R_["hits"] += 1; R_["steps"] += bool(r0_[n_, j_] > 0)
                if (self.hnt[n_] == p_).any() or (self.shnt[n_] == p_).any():
                    fails.append(f"life {n_} keeps a place that closed")
                if self.rung[n_, j_] != ex_[n_, j_]:
                    fails.append(f"life {n_}'s rung went {r0_[n_, j_]:.2f} to {self.rung[n_, j_]:.2f}, not {ex_[n_, j_]:.2f}")
            R_["posts"] += ps0_.count(p_)
            if self.lw and any(po_["place"] == p_ for po_ in self.lw_posts):
                fails.append("a post leading a place that closed goes on")
    def _bc(lean_, bc_):
        out_ = b0_(lean_, bc_); ok_ = np.isfinite(bc_); R_["care"] += int(ok_.sum())
        if ((out_ - b0_(lean_, np.where(ok_, 0.5, np.nan))) * np.where(ok_, bc_ - 0.5, 0) < -1e-12).any():
            fails.append("in the run, care seeking moved against trust")
        return out_
    def _po(act_, sh_, thr_, pa_, st_):
        out_ = p0_(act_, sh_, thr_, pa_, st_)
        R_["pull"] += int(out_.sum()); R_["freed"] += int((act_ & (sh_ > thr_) & (pa_ | st_)).sum())
        return out_
    def _pu(U_, pull_, bl_, tau_, f_):
        out_ = u0_(U_, pull_, bl_, tau_, f_); m_ = pull_[:, None] & bl_; R_["pull_u"] += int(m_.sum())
        if f_ != TV_["pull_back"]["reoffend"]:
            fails.append(f"the pull back at odds x{f_}, not the data's {TV_['pull_back']['reoffend']}")
        if (out_ != U_)[~m_].any() or (m_.any() and not np.allclose(np.exp((out_ - U_)[m_] / np.broadcast_to(
                tau_[:, None], U_.shape)[m_]), f_)):
            fails.append("the pull back moved other options, or not at its odds")
        return out_
    def _add(self, F, t, role, *a, **k):
        sl_ = a0_(self, F, t, role, *a, **k)
        fr_ = sys._getframe(1)
        if fr_.f_code.co_name == "pt_release":
            nn_ = fr_.f_locals["nn_"]; ok_ = sl_ >= 0
            R_["c"].update(np.round(self.c[nn_[ok_], sl_[ok_]].astype(float), 6).tolist())
        return sl_
    def _le(self, p, t, why):
        R_["why"][why] = R_["why"].get(why, 0) + 1
        return e0_(self, p, t, why)
    _wp.People._pt_q, E.bt_care, E.pt_pull_of, E.pt_pull_u, _wp.People._add, _wp.People._lead_end = _ptq, _bc, _po, _pu, _add, _le
    try:   # (the pull back's shadow line at .2, so it is on for some weeks; every life serves 3 years from 18)
        Y_ = 40   # (30 lives over 40 years: with the pack on in DEFAULT, 10 over 35 held no led place to close)
        o_ = E.run(N=30, years=Y_, seed=4, lib=EARTH, P=dict(
            E.DEFAULT, world=True, place_turnover=True, lead_ways=True, sph_levers=True, sph_fair=True, sph_events=True,
            sph_haunts=True, sph_hours=True, cur_on=True, body_trust=True, fair_read=True, c3_inst=True, prison_ties=True,
            prison_par=dict(E.DEFAULT["prison_par"], shadow=0.2, test=(18, 3)), sh_world=True))
    finally:
        _wp.People._pt_q, E.bt_care, E.pt_pull_of, E.pt_pull_u, _wp.People._add, _wp.People._lead_end = q0_, b0_, p0_, u0_, a0_, e0_
    made_, ended_, rel_ = {}, {}, {}
    for e_ in o_.get("prison_ties", ()):
        (made_ if e_["what"] == "made" else ended_).setdefault((e_["n"], e_["other"]), e_["t"])
    for (n_, _), t_ in made_.items():
        rel_[(n_, t_)] = rel_.get((n_, t_), 0) + 1
    late_ = [k_ for k_, t_ in made_.items() if ended_.get(k_, Y_ * 52) - t_ > 520]
    if R_["c"] != {round(float(np.float32(TV_["strength"])), 6)}:
        fails.append(f"ties inside made at {sorted(R_['c'])}, not {TV_['strength']}")
    if not rel_ or any(not 3 <= m_ <= 6 for m_ in rel_.values()):   # a 3-year term: 1 or 2 a year, at most cap 6
        fails.append(f"ties a release {sorted(rel_.values())}, not 3 to 6 for a 3-year term")
    if late_:
        fails.append(f"{len(late_)} ties last past 10 years")
    if not R_["hits"] or not R_["steps"] or not R_["posts"] or not R_["why"].get("place closed") or not R_["care"] \
            or not R_["pull"] or not R_["freed"] or not R_["pull_u"]:
        fails.append(f"something was never met: {dict((k_, v_) for k_, v_ in R_.items() if k_ != 'c')}")
    fails = list(dict.fromkeys(fails))
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the finishing pack's behaviour (W2 to W4): {R_['hits']} regulars freed by a "
          f"closing ({R_['steps']} rungs stepped down), {R_['why'].get('place closed', 0)} post ended with its place; care "
          f"seeking rises with trust ({R_['care']} life-weeks read); {len(made_)} ties inside, {sorted(set(rel_.values()))} a "
          f"release at strength {sorted(R_['c'])}, none past 10 years; the pull back on {R_['pull']} life-weeks, off for a "
          f"partner or steady work {R_['freed']}, odds x{TV_['pull_back']['reoffend']} on {R_['pull_u']} options"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 16. every change has a cause (role_why, the game's played-life hook)
if "role_why" in E.DEFAULT:
    t0 = time.process_time(); fails = []
    kw = dict(N=4, years=30, seed=11, lib=EARTH, log_lives=(0, 1))
    o0_ = E.run(**kw, P=dict(E.DEFAULT)); o1_ = E.run(**kw, P=dict(E.DEFAULT, role_why=True))
    def _strip(ev_):
        return {k_: [dict(x, role={a_: b_ for a_, b_ in x["role"].items() if a_ not in ("why", "t")}) if "role" in x else x for x in v_]
                for k_, v_ in ev_.items()}
    d0, d1 = digest(dict(o0_, events=None)), digest(dict(o1_, events=None))
    if d0 != d1 or digest(dict(e=_strip(o1_["events"]))) != digest(dict(e=o0_["events"])):
        fails.append("on, the lives or their events (but the causes) move")
    if any("why" in x.get("role", {}) for v_ in o0_["events"].values() for x in v_):
        fails.append("off, a cause is told")
    R_ = dict(gain=0, loss=0, items=0, none=0)
    for v_ in o1_["events"].values():
        for x in v_:
            r_ = x.get("role")
            if not r_ or not (r_["how"] in ("in time", "time passed", "slipped away")):
                continue
            w_ = r_.get("why")
            if not isinstance(w_, list) or not w_ or "t" not in r_:
                fails.append(f"{r_['what']} {r_['how']} without a cause"); continue
            R_["gain" if r_["what"] == "gained" else "loss"] += 1
            if r_["what"] == "gained" and w_[0]["k"] == "none":
                R_["none"] += 1
            if r_["what"] == "lost" and [it_["k"] for it_ in w_] != (["held"] if r_["how"] == "time passed" else ["unused"]):
                fails.append(f"{r_['name']} {r_['how']}: told as {[it_['k'] for it_ in w_]}")
            for it_ in w_:
                R_["items"] += 1
                if it_.get("k") not in ("mark", "moment", "held", "money", "age", "stage", "none", "pack", "luck",
                                        "unused", "standing", "state", "means", "need", "colour", "since"):
                    fails.append(f"a cause of kind {it_.get('k')}")
                if "t" in it_ and not 0 <= it_["t"] <= r_["t"]:
                    fails.append(f"{r_['name']}: its cause ({it_.get('name', it_.get('mark'))}) not before the change")
                if "t" in it_ and "within" in it_ and it_["k"] in ("mark", "moment") and r_["t"] - it_["t"] > it_["within"] * 52 + 1:
                    fails.append(f"{r_['name']}: its cause ({it_.get('name', it_.get('mark'))}) outside the rule's window")
    if R_["gain"] < 5 or R_["loss"] < 1 or R_["items"] < 5:
        fails.append(f"too few causes read: {R_}")
    g = E.run_steps(N=1, years=4, seed=11, lib=EARTH, P=dict(E.DEFAULT), log_lives=(0,)); msg = next(g); seen_ = False
    while True:
        kind, t, S, val = msg
        if S.get("age", 0) >= 3.5 and not seen_:
            seen_ = True
            if np.shape(S.get("asrc")) != (1, len(E.ASOURCES), len(E.COLORS)) or np.shape(S.get("asrc_c")) != \
                    (len(E.ASOURCES), len(E.COLORS)) or not np.array_equal(S["asrc_c"], S["asrc"][0]):
                fails.append(f"asrc at a pause has shape {np.shape(S.get('asrc'))}, asrc_c {np.shape(S.get('asrc_c'))}")
        try:
            msg = g.send(val)
        except StopIteration:
            break
    fails = list(dict.fromkeys(fails))
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  every change has a cause (role_why), switched on: the lives and events of it off; "
          f"{R_['gain']} gains in time and {R_['loss']} losses as time passed or slipped away, each with its cause "
          f"({R_['items']} items, {R_['none']} with none to name), each before the change and inside the rule's window; "
          f"asrc handed over at the pauses{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 17. bold ways (bold_play, the game's played-life hook), on a made-up BOLD table and links
if "bold_play" in E.DEFAULT and "bold" in batch.load_batch.__code__.co_varnames:
    import copy
    t0 = time.process_time(); fails = []
    BW_ = {"a deadline at college or work": [
        dict(base="leave it to the last night and write it in one wild burst", label="t_steps: an all-nighter, bolder",
             chance=0.35, grants="friend for life", mark="took a wild risk", likelier_if="mark 'learned a skill' +10",
             change=dict(well="t_steps: it paid off", badly="t_steps: a falling-out")),
        dict(base="cancel everything else and hand it in on time, as you promised", label="t_steps: twice the work, on time",
             chance=0.4, likelier_if="has [friend for life] +10", change=dict(well="t_steps: it paid off", badly="t_steps: a falling-out"))],
        "awake at night worrying about the future": dict(base="decide that from tomorrow you look after number one, whatever it takes",
                                                          label="t_steps: quit the safe plan", chance=0.3)}
    src_ = next(x for x in EARTH["src"] if x["name"] == "the same chance comes round again")
    def _lk(nm_, **kw_):
        x_ = dict(copy.deepcopy(src_), name="t_steps: " + nm_, **kw_); x_.pop("variant_of", None); x_.pop("tier", None)
        return x_
    LK_ = [_lk("the all-nighter, on", of_bold="a deadline at college or work / R", side="well", delay="1-2"),
           _lk("the promise, on", of_bold="a deadline at college or work / W", side="badly", delay="1-3"),
           _lk("after a falling-out", of_change="t_steps: a falling-out", side="badly", delay="1-3"),
           _lk("after it paid off", of_change="t_steps: it paid off", side="well", delay="1-3")]
    L_ = batch.load_batch("earth", packs=list(batch.PACKS), bold=BW_, links=LK_)
    kw = dict(N=2, years=20, seed=6, lib=L_)
    d_off = digest(E.run(**kw, P=dict(E.DEFAULT)))
    d_on = digest(E.run(**kw, P=dict(E.DEFAULT, bold_play=True)))
    if [x for x in set(d_off) | set(d_on) if d_off.get(x) != d_on.get(x) and x != "bold"]:
        fails.append("on and never asked, the lives move")
    P_ = dict(E.DEFAULT, bold_play=True, bold_ask="all")
    o1 = E.run(**kw, P=dict(P_)); g = E.run_steps(**kw, P=dict(P_)); msg = next(g)
    while True:
        try:
            msg = g.send(msg[3])
        except StopIteration as done:
            o2 = done.value
            break
    if digest(o1) != digest(o2) or digest(o1) == d_off or not o1["bold"]:
        fails.append("asked at every pick, run_steps does not live as run(), or nothing moved")
    P_ = dict(E.DEFAULT, bold_play=True, bold_cap=3, echo_play=True,
              echo_play_par=dict(E.DEFAULT["echo_play_par"], w=1.0, gap=0.0, again=0.0))
    g = E.run_steps(N=1, years=40, seed=6, lib=L_, P=P_, log_lives=(0,)); msg = next(g)
    offered = took = 0; now_ = None; link_wk = set(); odds_ok = True; slot_ = -1
    while True:
        kind, t, S, val = msg
        if kind == "situation" and S["age"] >= 8:
            S["P"]["bold_ask"] = True
        if kind == "choose":
            now_ = S["bold_now"][0] if S["bold_now"] is not None else None
            if S["ep_now"][0] >= 0 and "bold" in S["ep_seeds"][S["ep_now"][0]]:
                link_wk.add(t)
            if now_:
                offered += 1
                if S["bold_pick"][0] < 0 and offered % 3 == 0:   # the game takes the first slot (a = its base way)
                    S["P"]["bold_take"] = now_[0]["slot"]; val = np.array(val); val[0] = now_[0]["base"]; took += 1
        if kind == "odds" and S["bold_pick"][0] >= 0:
            pw_ = [x for x in now_ if x["slot"] == S["bold_pick"][0]][0]
            odds_ok &= abs(float(val[0]) - pw_["p_act"]) < 1e-3 and 0.1 <= float(val[0]) <= 0.9 and pw_["p"] <= pw_["p_act"] + 1e-4
        try:
            msg = g.send(val)
        except StopIteration as done:
            o_ = done.value
            break
    bl_ = o_["bold"]; sd_ = [x for x in o_["returns"] if "bold" in x]; got_ = [x for x in sd_ if x["got"] is not None]
    if offered < 10 or len(bl_) < 5 or not took or not {0, 1} <= {x[3] for x in bl_}:
        fails.append(f"{offered} asks with bold ways, {len(bl_)} bold picks, {took} taken by the game")
    if not odds_ok:
        fails.append("the odds at the odds pause are not bold_now's p_act, outside .1 to .9, or its card p above them")
    if [(x["t"], L_["BOLD"][x["bold"]]["i"], x["ok"]) for x in sd_] != [(b_[1], b_[2], b_[5]) for b_ in bl_ if b_[1] not in link_wk]:
        fails.append("the seeds are not the bold picks outside the links' weeks")
    if sum(x["due"] is not None for x in sd_) > 3 or any(x["due"] is None and x["done"] != -1 for x in sd_):
        fails.append("more seeds due than bold_cap, or one past the cap not done at once")
    if any(x["kind"] != L_["BOLD"][x["bold"]]["kind"] for x in sd_):
        fails.append("a seed of another kind than its bold way")
    for x in got_:
        c_ = [c_ for c_ in L_["COND"] if c_["s"] == x["got"]][0]
        if c_["side"] != ("well" if x["ok"] else "badly") or c_["of"] != (x["alt"] if x["change"] else x["kind"]) \
                or not x["link"] or not c_["delay"][0] * 52 <= x["done"] - x["t"] <= (c_["delay"][1] + 0.25) * 52 + 1:
            fails.append(f"a link of the wrong kind, side or time: {L_['names'][x['got']]}")
    if not got_ or not any(x["change"] for x in got_):
        fails.append(f"{len(got_)} links, {sum(x['change'] for x in got_)} shared")
    if int(o_["sit_n"][0, [L_["names"].index(x_["name"]) for x_ in LK_]].sum()) != len(got_):
        fails.append("a link moment came other than as a link")
    if any(b_[2] == 0 and b_[5] for b_ in bl_) and not any(x.get("role", {}).get("how") == "through t_steps: an all-nighter, bolder"
                                                          for x in o_["events"][0]):
        fails.append("the bold way's win did not come through it")
    fails = list(dict.fromkeys(fails))
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  bold ways (bold_play): on and never asked, the lives of it off; asked at every "
          f"pick, run_steps lives as run(); asked, {len(bl_)} bold picks of {offered} asks ({took} the game's), at the odds "
          f"bold_now told, {len(sd_)} seeds (cap 3, none in a link's week), {len(got_)} links "
          f"({sum(x['change'] for x in got_)} shared) of their side and delay{'' if not fails else '; ' + '; '.join(fails[:4])} "
          f"({time.process_time() - t0:.0f} s)")
# 18. because of you, and meanwhile (need_why, the game's played-life record)
if "need_why" in E.DEFAULT:
    t0 = time.process_time(); fails = []; NS_ = E.NSOURCES; PL_ = NS_.index("player"); SB_ = NS_.index("setback")
    seen_ = dict(weeks=0, edits=0.0, player=0.0, worst=0.0, imp=0, src=np.zeros(len(NS_)), ar=0, ar_ok=0)
    try:
        import foresee as AR_
        AR_ = AR_ if hasattr(AR_, "arrows") else None
    except ImportError:
        AR_ = None
    for world_, N_, Y_ in ((False, 4, 30), (True, 2, 12)):
        kw = dict(N=N_, years=Y_, seed=11, lib=EARTH, log_lives=(0,))
        Pd = dict(E.DEFAULT, world=world_)
        o0_ = E.run(**kw, P=Pd); o1_ = E.run(**kw, P=dict(Pd, need_why=True))
        if digest(o0_) != digest(o1_):
            fails.append(f"world {'on' if world_ else 'off'}: switched on, the lives move")
        for edit_ in (False, True):   # at each choose pause the "player" lifts the first life's autonomy, or never
            g = E.run_steps(**kw, P=dict(Pd, need_why=True)); msg = next(g); n0_ = None; add_ = 0.0; pick_ = None
            while True:
                kind, t, S, val = msg
                if S["nw"] is None or S["nw_imp"] is None:
                    fails.append("on, nw or nw_imp not handed over"); break
                if kind == "week":
                    n0_ = S["need"].copy(); add_ = 0.0
                    if np.abs(S["nw"]).max() > 0 or (S["nw_imp"] >= 0).any():
                        fails.append(f"week {t}: the record does not start empty")
                elif kind == "choose" and edit_ and t % 2 == 0:
                    S["need"][0, E.NEEDS.index("autonomy")] += 0.03; add_ += 0.03
                elif kind == "choose" and not edit_ and S["age"] >= 3 and AR_ is not None:   # the hover arrows (read-only)
                    ar_ = AR_.arrows(S, 0); pick_ = next((o_ for o_ in ar_ if o_["k"] == int(val[0])), None)
                    for o_ in ar_:
                        for a_ in o_["win"] + o_["fail"]:
                            if not (a_["kind"] in ("need", "means", "people", "title") and a_["dir"] in ("up", "down")
                                    and 1 <= a_["size"] <= 3):
                                fails.append(f"an arrow {a_}")
                elif kind == "end":
                    nw_ = S["nw"]; err_ = float(np.abs(nw_.sum(1) - (S["need"] - n0_)).max())
                    seen_["worst"] = max(seen_["worst"], err_); seen_["weeks"] += 1
                    seen_["src"] += np.abs(nw_).sum((0, 2)) > 0
                    pl_ = float(nw_[0, PL_].sum()); seen_["edits"] += add_; seen_["player"] += pl_
                    if pl_ < -1e-12 or pl_ > add_ + 1e-12 or (not edit_ and np.abs(nw_[:, PL_]).max() > 0):
                        fails.append(f"week {t}: the player's share {pl_:.4f} for {add_:.2f} set")
                    if (np.abs(nw_[:, SB_]).max(1) > 0).any() and ((np.abs(nw_[:, SB_]).max(1) > 0) & (S["nw_imp"] < 0)).any():
                        fails.append(f"week {t}: a setback without its kind")
                    seen_["imp"] += int((S["nw_imp"] >= 0).sum())
                if kind == "end" and not edit_ and pick_ is not None:   # the picked option's need arrows against the record
                    pv_ = np.zeros(len(E.NEEDS))
                    for a_ in pick_["win" if S["succ"][0] else "fail"]:
                        if a_["kind"] == "need":
                            pv_[E.NEEDS.index(a_["name"])] = a_["v"]
                    sz_ = lambda v_: (np.abs(v_)[:, None] >= np.array(AR_.SIZES["need"])).sum(1) * np.sign(v_)
                    seen_["ar"] += len(pv_); seen_["ar_ok"] += int((np.abs(sz_(pv_) - sz_(S["nw"][0, NS_.index("act")])) <= 1).sum())
                    pick_ = None
                try:
                    msg = g.send(val)
                except StopIteration as done:
                    o2_ = done.value
                    break
            if not edit_ and digest(o2_) != digest(o0_):
                fails.append(f"world {'on' if world_ else 'off'}: run_steps with it on, not the lives of run()")
    g = E.run_steps(N=1, years=4, seed=11, lib=EARTH, P=dict(E.DEFAULT), log_lives=(0,)); msg = next(g)
    if msg[2].get("nw", 0) is not None:
        fails.append("off, a record is kept")
    g.close()
    if seen_["worst"] > 1e-9:
        fails.append(f"the sources miss the week's change by up to {seen_['worst']:.2g}")
    if seen_["player"] < 0.5 * seen_["edits"]:
        fails.append(f"the player's share {seen_['player']:.2f} of {seen_['edits']:.2f} set")
    miss_ = [NS_[i] for i in range(len(NS_)) if NS_[i] in ("act", "fade", "setback", "means", "commitments", "care", "player")
             and not seen_["src"][i]]
    if AR_ is not None and (seen_["ar"] < 100 or seen_["ar_ok"] < 0.98 * seen_["ar"]):
        fails.append(f"the picked option's need arrows within a size of the record: {seen_['ar_ok']} of {seen_['ar']}")
    if miss_ or not seen_["imp"]:
        fails.append(f"never moved: {miss_}; {seen_['imp']} setbacks")
    fails = list(dict.fromkeys(fails))
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  because of you, and meanwhile (need_why), switched on: the lives of it off, "
          f"world off and on; {seen_['weeks']} weeks whose sources sum to the week's change (worst {seen_['worst']:.1g}), "
          f"{int((seen_['src'] > 0).sum())} of {len(NS_)} sources seen, {seen_['imp']} setbacks with their kind, the player's "
          f"edits {seen_['player']:.2f} of {seen_['edits']:.2f} set (the rest clipped); the hover arrows read-only, the picked "
          f"option's need arrows within a size of the record {seen_['ar_ok']} of {seen_['ar']}{'' if not fails else '; ' + '; '.join(fails[:4])} "
          f"({time.process_time() - t0:.0f} s)")
# 19. needs that fit life (need_tab, shared_hist, imp_age; workstream 4), Earth and packs, world off
if "imp_age" in E.DEFAULT:
    t0 = time.process_time(); fails = []; NS_ = E.NSOURCES
    kw = dict(N=3, years=40, seed=13, lib=EARTH, log_lives=(0,))
    o0_ = E.run(**kw, P=dict(E.DEFAULT))
    early_, par_m_, d_ = 0, 0.0, {}
    for lab_, sw_ in (("need_tab", dict(need_tab="v7")), ("shared_hist", dict(shared_hist=0.3)), ("imp_age", dict(imp_age=True))):
        P_ = dict(E.DEFAULT, need_why=True, **sw_)
        o1_ = E.run(**kw, P=P_)
        g = E.run_steps(**kw, P=P_); msg = next(g)
        while True:
            kind, t, S, val = msg
            if kind == "end":
                if lab_ == "imp_age":
                    for n_ in np.nonzero(S["nw_imp"] >= 0)[0]:
                        early_ += S["age"] < E.IMP_AGE[int(S["nw_imp"][n_])]
                if lab_ == "need_tab":
                    par_m_ += float(S["nw"][:, NS_.index("commitments"), E.NEEDS.index("meaning")]
                                    [S["held"][:, E.KIDX["partner"]] & ~S["held"][:, E.KIDX["children"]]].clip(0).sum())
            try:
                msg = g.send(val)
            except StopIteration as done:
                o2_ = done.value
                break
        if digest(o1_) != digest(o2_):
            fails.append(f"{lab_} on: run_steps not the lives of run()")
        if digest(o1_) == digest(o0_):
            fails.append(f"{lab_} on: nothing moved")
    if early_:
        fails.append(f"imp_age: {early_} setbacks before their age")
    if par_m_ <= 0:
        fails.append("need_tab v7: a partnership gave no meaning")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  needs that fit life (need_tab v7, shared_hist, imp_age), each switched on: "
          f"run_steps lives as run(), the lives move; no setback before its age; a partnership gives meaning "
          f"({par_m_:.3f}){'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 11. nothing read at a pause outside the handed-over names (an engine without STATE_MISSED reads its whole frame)
if hasattr(E, "STATE_MISSED"):
    bad += bool(E.STATE_MISSED)
    print(f"{'PASS' if not E.STATE_MISSED else 'FAIL'}  the pause state: every name read at a pause is handed over (STATE, "
          f"STATE_IF, STATE_MORE){'' if not E.STATE_MISSED else '; NOT: ' + ' '.join(sorted(E.STATE_MISSED))}")
print("engine", ENG, "engine.py", hashlib.md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12])
print("ALL PASS" if not bad else f"{bad} FAILED")
sys.exit(1 if bad else 0)
