"""Engine check for the pause points (backend plan item 2, 2026-10-08) and each switch's own rows: 80 rows, about an hour
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
 20. aims v1 and the heights (aims, heights), with the batch's aims, world off and on: run_steps() lives as run(); every
     step reached has a name of it held (or is a Known step, by a sphere rung); a height's week never moves once reached;
     an aim the player sets (foresee.set_aim) is held as theirs, not the character's own; the track, the choices and the
     hover's aim ways (foresee.aims, aim_choices, aim_ways, read at every pick) are well formed and change no life; the
     batch without aims carries none.
 21. footprints (foot_on), with the batch's FOOT tables, world off and on: run_steps() lives as run() and the lives move;
     every pick's footprints are its option's; a means moves by its value (or to 0 or 1), a mark or door is left that
     week, the act's own mark counts only when a rule reads it, a person met is in the cast and a place joined is a
     haunt (world on); at the pauses foot (the last act's footprints) and foot_open (the doors waiting, each once) per
     life, a door only a return reads shut within foot_par door_yrs; foresee.marks_toward (what a mark nears) well
     formed, nearest first; with FOOT in the batch and the switch off, the lives of the batch without it; the batch
     without FOOT carries none.
 22. the world answers v1 (world_answers, wa_phase2), with the batch's world answers moments: world off, the switch moves
     nothing and no such moment comes; world on, loaded with the switch off, none comes and there is no ledger; on with
     every part off, and the ledger alone (a record), the lives of it off; all on with phase 2, run_steps() lives as
     run() and the lives move, the ledger fills for every life with the Library's unit keys, what a life moves a year in
     its groups, places and town grows with its standing (rung), and only Known lives decide for others; the batch
     without them carries none.
 23. cause_fit (E2, the Library's cause audit's tightened rules): switched on, run_steps() lives as run() and the lives
     move; a dog of one's own only within a year of a stray dog, a record only within two years of a law broken.
 24. setbacks that fit the world (imp_world, v25 N3), world on: with every elasticity at 0 the lives of it off (the same
     draws); on, run_steps() lives as run() and the lives move; a setback's named fact is one its kind follows, with its
     words and its cause index; each kind's life weight averages 1 over the living each year (the counts hold).
 25. what a world rewards (tilt_world, v25 #10), Earth and the neutral world, world on: run_steps() lives as run() and the
     lives move; each year's r has a mean of 1 per sphere and every cell within the realm's clip (Earth .67 to 1.5);
     prizes and prizes_moves well formed; the neutral world starts every sphere at .2 a colour, its places even,
     inst_even on, and its r is 1 everywhere, every year.
 26. the land (wa_land, v25 lane D), Earth and packs with the Library's nature moments, world on: loaded with the
     switch off no nature moment comes; on, run_steps() lives as run() and the lives move; nature moments never closer
     than the gap, the company of a kind the moment takes, the stretches in 0..1 and the hazards' feedback the land's
     own state, at most three ways; a flood brought by scn hits every household with its course, and a Known drain of
     the marsh moves its wildness by size x k_land x reach and the flood odds with it; no way before 14 and no step
     above 0 before 18 (LAND_ENGINE way_age); a heat strike makes quarrels
     x 1.1 for its spell; a group's norm moves a little toward the chosen face, a kin's shared memory is kept and
     recalled when they die, and notice pushes back by what a face costs and asks a leaning life in to a way.
 27. national standing (wa_nat_climb, v25 lane D), Earth and packs with the Library's national moments, world on:
     loaded with the switch off no national moment comes; on, run_steps() lives as run() and the lives move;
     recognition, influence and authority kept apart, a seat held by one life and never an engine office, none before
     18, phase 2's national only with a seat, a voice or an office, Known by national standing only with a seat or a
     national name (a voice alone is Known only by the heights), and decisions at nation scope only by them; with aims
     v2 the national pack's route fields are on the agenda only with wa_nat_climb on, and aim_x reads an aim whose next
     rung is a standing-3 seat in the climb's sphere.
 28. aims v2 (aims_v2, v25 lane B), Earth and packs with the Library's and the packs' fields (the druid joined), a player's life (forks
     left open but one answered), world off (every field's first two rungs given a deadline) and on: run_steps() lives as
     run() with the agenda, previews and reviews read; the agenda's handed-over names there; every rung reached through
     an outcome (a title of it held or once held, a test or chance won; never effort alone); every window's closing told
     once, the week after its last, and no test after it but by a way round; the player's forks kept until the player
     answers (or its window closes: it lapses into a way round), effort waiting at the need while they wait, and a fork put on a moment of its own that moment is the week's
     (and its aim the one the moment is about); a player's fork moment the game does not ask (pick_asked unset) answered
     "later": the fork left open, nothing decided, taught or charged (its week idle); no entry cost charged twice (a pause and resume included).
     The scenario pack of the decision's known risks is tools/t_aims2.py (seconds).
 29. reactions, clashes and seeking (react, clash, seek; v25 lane C), Earth and packs with the clash, seeking and repair
     moments, world on: world off the switches move nothing; react alone and all on, run_steps() lives as run() and the
     lives move; every clash has stakes, comes from 10, one a sphere (every sphere its dispute touches) in 2 years, before
     18 one in 2 years in any sphere, and 3 in 10 (one before 18 counting half); every clash, seeking or repair moment
     met took the place of an ask (for a played life the week's own moment too, and at least half its clashes come as
     moments); seeking moves no colour and admits only through a place; states carry durations and k stays at most 1/3;
     the caller's demand (P["scn"]) is recorded with its tag, response and stakes, and two in one week (one dispute)
     each on its own record.
 30. WA3, a standing level reaches its town (wa_reach, v25), world on: with the world answers off, nothing; on, run_steps
     lives as run() and the lives move; an act on the town's sphere from the close circle reads at most 1 + REACH[level, 2]
     and a founding nudges the town by its reach / 3 (off: 3 and the whole nudge); a level-0 life's presence leaves the
     town's spheres alone and a level-1 life's leans its haunts' spheres in its town, recorded as being there; group
     presence x (1 + .5 x REACH[level, 2]); the level lingers (held 3, 6, 11 years ago: 2, 1, 0).

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


def _drain(g):
    """run_steps passing every value back unchanged: its outputs."""
    msg = next(g)
    while True:
        try:
            msg = g.send(msg[3])
        except StopIteration as done:
            return done.value


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
       ("a refused first job or job move re-draws to the next-best fit (acc_redraw)", dict(acc_redraw=True), {}, 40, 4),
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
       # 14 lives: with v24's rates, 10 lives bought no second home inside the gap (the switch had nothing to move)
       ("v22.5 round 3, a home bought again only years later (ev_gapfit)", dict(ev_gapfit={"buying a home": (3, 8)}), {}, 70, 14),
       # 11 lives: with v24's rates, 10 lives met no lasting illness the switch's points moved (it had nothing to move)
       ("v22.5 round 3d, a lasting illness at its own rates by age (age_pts)",
        dict(age_pts={"living with a chronic illness": ((0, 0.0045), (40, 0.01), (80, 0.05))}), {}, 70, 11)]
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
        Y_ = 40   # (30 lives over 40 years: with the pack on in DEFAULT, 10 over 35 held no led place to close; seed 6:
        # with v24, seed 4's 30 lives held no led place either, and seed 5's none)
        o_ = E.run(N=30, years=Y_, seed=6, lib=EARTH, P=dict(
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
    g = E.run_steps(N=1, years=40, seed=9, lib=L_, P=P_, log_lives=(0,)); msg = next(g)   # seed 9: v24 rates (6 met one link, none shared)
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
                    if ((S["nw_imp"] >= 0) != (S["nw_imp_cause"] >= 0)).any():
                        fails.append(f"week {t}: a setback without its cause, or a cause without a setback")
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
# rows 19 to 22 and 23 each switch one v24 part on from every v24 switch off (engine.V24_OFF; the v24 refit turned
# them on in DEFAULT), on a batch without the v24 moments and tables where a row needs one
B24_ = dict(E.DEFAULT, **getattr(E, "V24_OFF", {}))
NO24_ = batch.load_batch("earth", packs=list(batch.PACKS), aims=False, foot=False, wa=False) \
    if "wa" in batch.load_batch.__code__.co_varnames else EARTH
# 19. needs that fit life (need_tab, shared_hist, imp_age; workstream 4), Earth and packs, world off
if "imp_age" in E.DEFAULT:
    t0 = time.process_time(); fails = []; NS_ = E.NSOURCES
    kw = dict(N=3, years=40, seed=13, lib=NO24_, log_lives=(0,))
    o0_ = E.run(**kw, P=dict(B24_))
    early_, par_m_, d_ = 0, 0.0, {}
    for lab_, sw_ in (("need_tab", dict(need_tab="v7")), ("shared_hist", dict(shared_hist=0.3)), ("imp_age", dict(imp_age=True))):
        P_ = dict(B24_, need_why=True, **sw_)
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
# 20. aims v1 and the heights reading (aims, heights; workstream 5), Earth and packs with the aim catalogue
if "aims" in E.DEFAULT and "aims" in batch.load_batch.__code__.co_varnames:
    import foresee as FS_
    t0 = time.process_time(); fails = []
    LA_ = batch.load_batch("earth", packs=list(batch.PACKS), aims=True, foot=False, wa=False)
    if "AIMS" in (NO24_ or {}):
        fails.append("the batch without aims carries them")
    seen_ = dict(steps=0, own=0, set=0, calls=0, track=0, heights=0, ways=0)
    for wl_, N_, Y_, sd_ in ((False, 4, 50, 9), (True, 2, 30, 4)):
        P_ = dict(B24_, aims=True, world=wl_)
        kw = dict(N=N_, years=Y_, seed=sd_, lib=LA_, log_lives=(0,))
        o1_ = E.run(**kw, P=P_)
        for edit_ in (False, True):
            g = E.run_steps(**kw, P=P_); msg = next(g); set_ = None; ht0_ = None
            while True:
                kind, t, S, val = msg
                if kind == "week" and S.get("AIM_ON"):
                    ht_ = S["ht_t"].copy()
                    if ht0_ is not None and ((ht0_ >= 0) & (ht_ != ht0_)).any():
                        fails.append("a height's week changed once reached")
                    ht0_ = ht_
                    if edit_ and set_ is None and S["age"] >= 20:   # the player sets the aim that fits life 0 least
                        held_ = set(int(a_) for a_ in S["ak"][0] if a_ >= 0)
                        a_ = next(int(x_) for x_ in np.argsort(S["aim_fit"](np.asarray(S["w"][0], float))) if int(x_) not in held_)
                        q_, why_ = FS_.set_aim(S, 0, S["AIM"]["names"][a_])
                        if q_ < 0 or S["ak"][0, q_] != a_ or S["aown"][0, q_] or not S["aby"][0, q_]:
                            fails.append(f"set_aim: not held as set by the player ({why_})")
                        set_ = (q_, a_); seen_["set"] += 1
                if kind == "choose" and S.get("AIM_ON") and not edit_:   # the hover's aim ways, read-only
                    for n_ in range(N_):
                        for k_, ws_ in FS_.aim_ways(S, n_).items():
                            seen_["ways"] += len(ws_)
                            if not S["mask"][n_, k_] or any(S["ak"][n_, w_["slot"]] < 0 for w_ in ws_):
                                fails.append("aim_ways names a closed option or an empty slot")
                if kind == "end" and S.get("AIM_ON"):
                    A_ = S["AIM"]
                    for n_, q_ in zip(*np.nonzero(S["ak"] >= 0)):
                        a_ = int(S["ak"][n_, q_]); k_ = int(S["astep"][n_, q_]); st_ = A_["aims"][a_]["steps"]
                        if k_ > len(st_):
                            fails.append("more steps than the ladder"); continue
                        if k_ and not (S["r_ever"][n_, st_[k_ - 1]["any"]].any() or (st_[k_ - 1]["h"] == 1 and wl_)):
                            fails.append(f"{A_['names'][a_]}: step {k_} reached with none of its names held")
                    if (S["aim_best"] < np.where(S["ak"][..., None] == np.arange(A_["A"]), S["astep"][..., None], 0).max(1)).any():
                        fails.append("an aim's best below its steps now")
                if kind == "end" and S.get("AIM_ON") and t % 260 == 0:   # the track and the choices, now and then
                    for n_ in range(N_):
                        tr_ = FS_.aims(S, n_); ch_ = FS_.aim_choices(S, n_)
                        seen_["track"] += len(tr_)
                        if any(x_["reached"] > len(x_["steps"]) or (x_["next"] is None) != (x_["reached"] == len(x_["steps"]))
                               for x_ in tr_) or len(ch_) > 6:
                            fails.append("the aims track or choices malformed")
                try:
                    msg = g.send(val)
                except StopIteration as done:
                    o2_ = done.value
                    break
            if not edit_ and digest(o1_) != digest(o2_):
                fails.append(f"world {'on' if wl_ else 'off'}: run_steps not the lives of run()")
        lg_ = o1_["aims"]["log"]
        seen_["steps"] += sum(r_["what"] == "step" for r_ in lg_); seen_["own"] += sum(r_["what"] == "became their own" for r_ in lg_)
        seen_["calls"] += sum(r_["what"] == "became a calling" for r_ in lg_)
        seen_["heights"] += int((o1_["heights"]["week"] >= 0).sum())
    if not seen_["steps"]:
        fails.append("no step reached")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  aims v1 and the heights, switched on (world off and on): run_steps lives as "
          f"run(); {seen_['steps']} steps reached, each with a name of it held; {seen_['own']} sparked, {seen_['calls']} "
          f"callings, {seen_['heights']} heights reached (never moved once reached); set_aim held as the player's "
          f"({seen_['set']}); the track well formed ({seen_['track']} read), {seen_['ways']} aim ways at the picks{'' if not fails else '; ' + '; '.join(sorted(set(fails))[:4])} "
          f"({time.process_time() - t0:.0f} s)")
# 21. footprints (foot_on; workstream 3), Earth and packs with the batch's FOOT tables
if "foot_on" in E.DEFAULT and "foot" in batch.load_batch.__code__.co_varnames:
    t0 = time.process_time(); fails = []
    import foresee
    LF_ = batch.load_batch("earth", packs=list(batch.PACKS), foot=True, aims=False, wa=False)
    if "FOOT" in (NO24_ or {}):
        fails.append("the batch without FOOT carries it")
    kw = dict(N=3, years=20, seed=11, log_lives=(0,))
    o0_ = E.run(**kw, lib=LF_, P=dict(B24_))
    if digest(E.run(**kw, lib=NO24_, P=dict(B24_))) != digest(o0_) or "footprints" in o0_:
        fails.append("with FOOT in the batch and foot_on off, the lives moved")
    import collections as _co
    seen_ = _co.Counter()
    for wl_, N_, Y_, sd_ in ((False, 4, 40, 3), (True, 2, 25, 4)):
        P_ = dict(B24_, foot_on=True, world=wl_)
        kw = dict(N=N_, years=Y_, seed=sd_, lib=LF_, log_lives=(0,))
        o1_ = E.run(**kw, P=P_)
        g = E.run_steps(**kw, P=P_); msg = next(g); done_ = ml_done_ = 0; open_ = {}
        while True:
            kind, t, S, val = msg
            if kind == "end" and S.get("FOOT_ON"):
                MI_ = {m_: i_ for i_, m_ in enumerate(LF_["MARKS"])}
                left_ = {(e_[0], e_[1], e_[2]) for e_ in S["mark_log"][ml_done_:]}; ml_done_ = len(S["mark_log"])
                if len(S["foot"]) != N_ or len(S["foot_open"]) != N_:
                    fails.append("foot and foot_open not one list a life")
                for n_ in range(N_):   # the doors: one each kind, since a past week; a door gone was shut by a moment met
                    op_ = {d_[0]: d_[1] for d_ in S["foot_open"][n_]}
                    if len(op_) != len(S["foot_open"][n_]) or any(v_ > t for v_ in op_.values()):
                        fails.append("foot_open: a door twice or from the future")
                    seen_["doors shut"] += sum(k_ not in op_ for k_ in open_.get(n_, {}))
                    open_[n_] = op_
                for r_ in S["foot_log"][done_:]:
                    n_ = r_["life"]; si_ = LF_["names"].index(r_["moment"]); ki_ = LF_["labels"][si_].index(r_["label"])
                    if (si_, ki_) not in LF_["FOOT"] and not all(f_.get("own") for f_ in r_["feet"]):
                        fails.append(f"{r_['moment']}: footprints of an option without them")
                    now_ = abs(r_["age"] - round(t / 52, 2)) < 1e-9   # this week's (the first end pause also sees earlier ones)
                    if now_ and S["foot"][n_] != [(f_["kind"], f_["value"], f_.get("cid", -1)) for f_ in r_["feet"]]:
                        fails.append("foot: not the last act's footprints")
                    for f_ in r_["feet"]:
                        seen_[f_["kind"]] += 1; seen_["own marks"] += bool(f_.get("own"))
                        if f_.get("own") and f_["value"] not in LF_["FOOT_OWN"]:
                            fails.append(f"own mark {f_['value']} counted")
                        if now_ and f_["kind"] == "door" and f_["value"] not in [d_[0] for d_ in S["foot_open"][n_]]:
                            fails.append(f"door {f_['value']} not waiting")
                        if f_["kind"] == "means":
                            y_ = float(f_["value"].lstrip("abcdefghijklmnopqrstuvwxyz"))
                            if not (abs(f_["moved"] - y_) < 1e-9 or (abs(f_["moved"]) <= abs(y_) + 1e-9 and f_["moved"] * y_ >= 0)):
                                fails.append(f"means {f_['value']} moved {f_['moved']}")
                            seen_["means moved"] += abs(f_["moved"] - y_) < 1e-9
                        if now_ and f_["kind"] in ("mark", "door") and (n_, t, MI_.get(f_["value"], -1)) not in left_:
                            fails.append(f"{f_['kind']} {f_['value']} not left")
                        if wl_ and f_["kind"] == "person" and "cid" not in f_:
                            fails.append(f"person {f_['value']} with no one in the cast")
                        if wl_ and f_["kind"] == "person" and not f_["value"].endswith(" lost"):
                            if "cid" not in f_ or not (S["WL"].PP.uid[n_] == f_["cid"]).any():
                                fails.append(f"person {f_['value']} not in the cast")
                            else:
                                seen_["person named"] += 1
                        if wl_ and f_["kind"] == "place" and "place" in f_:
                            if f_["place"] not in list(S["WL"].PP.hnt[n_]):
                                fails.append(f"place {f_['value']} not a haunt")
                            else:
                                seen_["haunt joined"] += 1
                done_ = len(S["foot_log"])
                for n_ in range(N_):   # a door only a return reads shuts after door_yrs (Library 10-19)
                    if not S["dead"][n_] and any(LF_["FOOT_RET"][MI_[d_[0]]] and t - d_[1] > 52 * P_["foot_par"]["door_yrs"] + 4
                           for d_ in S["foot_open"][n_] if d_[0] in MI_):
                        fails.append("a door only a return reads open past door_yrs")
                if t % 260 == 0 and hasattr(foresee, "marks_toward"):   # the marks stack: what a mark nears, read-only
                    for n_ in range(N_):
                        mt_ = foresee.marks_toward(S, n_); seen_["marks toward"] += len(mt_)
                        G_ = LF_["ROLES"]
                        if any(not (1 <= d_["have"] <= d_["need"]) or d_["done"] != (d_["have"] >= d_["need"])
                               or S["r_has"][n_, G_["ID"][d_["title"]]] or d_["kind"] != ("title" if G_["ID"][d_["title"]] < G_["NT"] else "perk")
                               or S["mark_n"][n_, MI_[d_["mark"]]] < 1 for d_ in mt_):
                            fails.append("marks_toward: a reading out of shape")
                        if [(d_["done"], d_["need"] - d_["have"]) for d_ in mt_] != sorted((d_["done"], d_["need"] - d_["have"]) for d_ in mt_):
                            fails.append("marks_toward: not nearest first")
            try:
                msg = g.send(val)
            except StopIteration as done:
                o2_ = done.value
                break
        if digest(o1_) != digest(o2_):
            fails.append(f"world {'on' if wl_ else 'off'}: run_steps not the lives of run()")
        if digest(o1_) == digest(E.run(**kw, P=dict(B24_, world=wl_))):
            fails.append(f"world {'on' if wl_ else 'off'}: nothing moved")
    for k_ in ("means", "mark", "door", "lesson", "person named", "own marks", "marks toward"):
        if not seen_[k_]:
            fails.append(f"no {k_} seen")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  footprints, switched on (world off and on): run_steps lives as run(), the lives "
          f"move; {seen_['means']} means ({seen_['means moved']} by their value, the rest clipped), {seen_['mark']} marks "
          f"({seen_['own marks']} the act's own) and {seen_['door']} doors left ({seen_['doors shut']} shut since), "
          f"{seen_['person named']} people in the cast, {seen_['haunt joined']} haunts joined, {seen_['lesson']} lessons told, "
          f"{seen_['marks toward']} marks toward a title or perk read; foot and foot_open per life at the pauses; the FOOT tables with the switch off change nothing; the batch without FOOT "
          f"carries none{'' if not fails else '; ' + '; '.join(sorted(set(fails))[:4])} ({time.process_time() - t0:.0f} s)")
# 22. the world answers v1 (world_answers, wa_phase2; workstream 6), Earth and packs with the world answers moments
if "world_answers" in E.DEFAULT and "wa" in batch.load_batch.__code__.co_varnames:
    import world_keys as WKA_
    t0 = time.process_time(); fails = []
    LWA_ = batch.load_batch("earth", packs=list(batch.PACKS), wa=True, aims=False, foot=False)
    WAI_ = [WKA_.CAST_WANTS.index(k_) for k_ in WKA_.WA_WANTS]
    if np.isin(np.asarray((NO24_ or {}).get("W_WANT", [])), WAI_).any():
        fails.append("the batch without them carries world answers moments")
    WAS_ = np.isin(np.asarray(LWA_["W_WANT"]), WAI_)
    if not WAS_.any():
        fails.append("the batch with them carries none")
    nowa_ = lambda o_: digest({k_: ({n_: [e_ for e_ in v_[n_] if not (isinstance(e_, dict) and "wa_ledger" in e_)]
                                         for n_ in v_} if k_ == "events" else v_)
                               for k_, v_ in o_.items() if k_ != "wa_ledger"})   # the lives, less the ledger's record
    met_ = lambda o_: int(np.asarray(o_["sit_n"])[:, WAS_].sum())
    kw = dict(N=3, years=12, seed=11, lib=LWA_, log_lives=(0,))   # world off: nothing to act on
    a_ = E.run(**kw, P=dict(B24_, world=False))
    b_ = E.run(**kw, P=dict(B24_, world=False, world_answers=True, wa_phase2=True))
    if digest(a_) != digest(b_) or met_(b_):
        fails.append("world off: the switch moved a life, or a world answers moment came")
    kw = dict(N=2, years=46, seed=17, lib=LWA_, log_lives=(0,))   # seed 17 (v24 refit's rates): a Known life who also leads
    PW_ = dict(B24_, world=True, heights=True)
    o0_ = E.run(**kw, P=dict(PW_))
    if met_(o0_) or "wa_ledger" in o0_:
        fails.append("loaded with the switch off: a world answers moment came, or a ledger")
    off_ = dict(wa_groups=False, wa_places=False, wa_ledger=False, wa_notice=False, wa_phase2=False)
    if nowa_(E.run(**kw, P=dict(PW_, world_answers=True, **off_))) != digest(o0_):
        fails.append("on with every part off: the lives moved")
    o_ = E.run(**kw, P=dict(PW_, world_answers=True, **dict(off_, wa_ledger=True)))
    if nowa_(o_) != digest(o0_):
        fails.append("the ledger alone moved the lives (it is a record)")
    if any(x_["told"] == 0 or x_["rings"]["person"]["total"] <= 0 for x_ in o_["wa_ledger"]["lives"]):
        fails.append("the ledger alone: a life with nothing in it")
    P_ = dict(PW_, world_answers=True, wa_phase2=True)
    o1_ = E.run(**kw, P=P_)
    g = E.run_steps(**kw, P=P_); msg = next(g); kn_ = 0
    while True:
        kind, t, S, val = msg
        if kind == "end" and S.get("WA_ON"):
            kn_ += int(np.asarray(S["wa_known"]).sum())
            if len(S["wa_book"]) != kw["N"] or len(S["wa_lines"]) != kw["N"]:
                fails.append("the ledger handed over at a pause malformed")
        try:
            msg = g.send(val)
        except StopIteration as done:
            o2_ = done.value
            break
    if digest(o1_) != digest(o2_):
        fails.append("run_steps not the lives of run()")
    if nowa_(o1_) == digest(o0_):
        fails.append("switched on, nothing moved")
    WL_ = o1_["wa_ledger"]; lv_ = WL_["lives"]
    try:
        import importlib.util as ilu_
        sp_ = ilu_.spec_from_file_location("chroma_earth_world_lines", os.path.join(batch.LIB_DIR, "earth_world_lines.py"))
        wlm_ = ilu_.module_from_spec(sp_); sp_.loader.exec_module(wlm_)
        if (set(WL_["units"]) != set(wlm_.BECAUSE) or set(WL_["nation"]) != set(wlm_.NATION) or set(WL_["rings"]) != set(wlm_.KEPT)
                or any(set(v_) != set(WL_["kept"]) for v_ in wlm_.KEPT.values())):
            fails.append("the ledger's unit keys are not the Library's lines'")
    except FileNotFoundError:
        pass
    lines_ = [ln_ for x_ in lv_ for ln_ in x_["lines"]]
    if any(ln_["unit"] not in WL_["units"] + ["nation"] or ln_["size"] not in WL_["sizes"] for ln_ in lines_):
        fails.append("a told line of an unknown unit or size")
    if any(x_["told"] == 0 or sum(r_["total"] for k_, r_ in x_["rings"].items() if k_ != "person") <= 0 for x_ in lv_):
        fails.append("a life whose ledger moved nothing past its close circle")
    mv_ = np.sum([x_["by_rung"]["moved"] for x_ in lv_], 0); wk_ = np.sum([x_["by_rung"]["weeks"] for x_ in lv_], 0)
    rt_ = [mv_[r_] / wk_[r_] * 52 for r_ in range(5) if wk_[r_] >= 52]
    lo_, hi_ = mv_[:2].sum() / max(wk_[:2].sum(), 1) * 52, mv_[3:].sum() / max(wk_[3:].sum(), 1) * 52
    if not wk_[3:].sum() or not hi_ > lo_:
        fails.append(f"what a life moves did not grow with standing ({lo_:.4f} a year at rung 0-1, {hi_:.4f} at 3-4)")
    dec_ = WL_["decisions"]; kw_ = sum(x_["known_weeks"] for x_ in lv_)
    if not dec_ or any(not d_.get("known") for d_ in dec_) or any(x_["decisions"] and not x_["known_weeks"] for x_ in lv_):
        fails.append("decisions for others: none, or one by a life not Known")
    if not kn_ or kw_ != kn_:
        fails.append(f"the Known weeks at the pauses ({kn_}) are not the ledger's ({kw_})")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the world answers v1 (world_answers, wa_phase2), with its moments: world off and "
          f"loaded with it off, nothing; every part off and the ledger alone, the lives of it off; on, run_steps lives as "
          f"run(), {len(lines_)} lines told ({min(x_['told'] for x_ in lv_)} or more a life), moved a year {lo_:.4f} at rung "
          f"0-1, {hi_:.4f} at 3-4; {len(dec_)} decisions in {kw_ / 52:.1f} Known years, none outside them"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 23. cause_fit (E2): the cause audit's tightened rules (earth_rules.ROLES_FIT), Earth and packs, world off
if "cause_fit" in E.DEFAULT:
    t0 = time.process_time(); fails = []
    LC_ = NO24_; GC_ = LC_["ROLES"]; IDC_ = GC_["ID"]
    if not GC_.get("rule_fit"):
        fails.append("no fitted rule compiled")
    kw = dict(N=40, years=60, seed=21, lib=LC_, log_lives=(0,))
    o0_ = E.run(**kw, P=dict(B24_))
    P_ = dict(B24_, cause_fit=True)
    o1_ = E.run(**kw, P=P_)
    if digest(o1_) == digest(o0_):
        fails.append("on: nothing moved")
    dog_, rec_ = IDC_.get("dog of one's own"), IDC_.get("someone with a record")
    sd_ = LC_["names"].index("a stray dog follows you home"); mb_ = LC_["MARKS"].index("broke the law")
    rule_t_ = {}
    for pn_, tt_, i_, what_, how_ in o1_["roles"]["log"]:
        if what_ == "gained" and how_ == "in time":
            rule_t_.setdefault(int(tt_), set()).add((int(pn_), int(i_)))
    g = E.run_steps(**kw, P=P_); msg = next(g); prev_ = None; stray_ = None; gains_ = [0, 0]
    while True:
        kind, t, S, val = msg
        if kind == "end":
            sn_ = np.asarray(S["sit_n"])[:, sd_]
            if stray_ is None:
                stray_ = np.full(len(sn_), -10 ** 9); sn0_ = sn_.copy()
            stray_ = np.where(sn_ > sn0_, t, stray_); sn0_ = sn_.copy()
            rh_ = np.asarray(S["r_has"])
            if prev_ is not None:   # gains by the rule itself ("in time"; an act may give one with its own cause)
                for n_ in np.nonzero(rh_[:, dog_] & ~prev_[:, dog_])[0]:
                    if (int(n_), dog_) in rule_t_.get(t, ()):
                        gains_[0] += 1
                        if t - stray_[n_] > 53:
                            fails.append(f"a dog of one's own with no stray dog within the year (life {n_}, week {t})")
                for n_ in np.nonzero(rh_[:, rec_] & ~prev_[:, rec_])[0]:
                    if (int(n_), rec_) in rule_t_.get(t, ()):
                        gains_[1] += 1
                        if t - S["mark_last"][n_, mb_] > 2 * 52 + 1:
                            fails.append(f"a record with no law broken within two years (life {n_}, week {t})")
            prev_ = rh_.copy()
        try:
            msg = g.send(val)
        except StopIteration as done:
            o2_ = done.value
            break
    if digest(o1_) != digest(o2_):
        fails.append("on: run_steps not the lives of run()")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  cause_fit (the cause audit's {len(GC_.get('rule_fit') or {})} rules), switched "
          f"on: run_steps lives as run(), the lives move; a dog only after a stray dog ({gains_[0]}), a record only after a law "
          f"broken ({gains_[1]}){'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 24. setbacks that fit the world (imp_world, v25 N3; world_fit.imp_g), Earth and packs, world on
if "imp_world" in E.DEFAULT:
    import world_fit as WF_, realm_earth as RE_
    t0 = time.process_time(); fails = []
    kw = dict(N=6, years=10, seed=5, lib=EARTH, log_lives=(0,))
    P0_ = dict(E.DEFAULT, world=True, need_why=True)
    o0_ = E.run(**kw, P=dict(P0_))
    IW0_ = RE_.IMP_WORLD   # every e at 0 (the facts still read): the draws, and so the lives, are v24's
    RE_.IMP_WORLD = tuple({f_: 0.0 for f_ in d_} for d_ in IW0_)
    try:
        if digest(E.run(**kw, P=dict(P0_, imp_world=True))) != digest(o0_):
            fails.append("every e at 0: the lives moved")
    finally:
        RE_.IMP_WORLD = IW0_
    P1_ = dict(P0_, imp_world=True)
    o1_ = E.run(**kw, P=P1_)
    if digest(o1_) == digest(o0_):
        fails.append("on: nothing moved")
    E_ = WF_.imp_elasticities(RE_, len(IW0_)); fk_ = (E_ != 0).any(1)
    g = E.run_steps(**kw, P=P1_); msg = next(g); n_imp_, n_fact_, worst_ = 0, 0, 0.0; yrs_ = set()
    while True:
        kind, t, S, val = msg
        if kind == "end" and S["age"] >= 1:
            if not all(nm_ in S for nm_ in ("iw_fact", "iw_why", "IW_ON")) or not S["IW_ON"]:
                fails.append("iw_fact, iw_why or IW_ON not handed over"); break
            for n_ in np.nonzero(S["nw_imp"] >= 0)[0]:   # a setback's fact is one its kind follows, with its words
                n_imp_ += 1; k_, f_ = int(S["nw_imp"][n_]), int(S["iw_fact"][n_])
                if f_ >= 0:
                    n_fact_ += 1
                    if E_[k_, f_] == 0 or not isinstance(S["iw_why"][n_], str) \
                            or S["nw_imp_cause"][n_] < len(E.IMP_CAUSES):
                        fails.append(f"life {n_} week {t}: kind {k_} named fact {f_} ({S['iw_why'][n_]!r})")
            if int(S["age"]) not in yrs_ and len(fails) < 4:   # once a year: the life part's mean over the living is 1
                yrs_.add(int(S["age"])); WL_ = S["WL"]; out_ = {}
                WF_.imp_g(RE_, E_, WL_.W, WL_.PP, S["res"][:, E.RIDX["health"]], S["age"], S["dead"], out=out_)
                worst_ = max(worst_, float(np.abs(out_["pop"][:, fk_].mean(0) - 1).max()))
        try:
            msg = g.send(val)
        except StopIteration as done:
            o2_ = done.value
            break
    if digest(o1_) != digest(o2_):
        fails.append("on: run_steps not the lives of run()")
    if worst_ > 0.03:   # the clip at .2 and 4 after normalising moves the mean a little; each kind's count holds
        fails.append(f"a kind's mean weight over the living {1 + worst_:.3f}, not 1")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  setbacks that fit the world (imp_world), world on: every e at 0 the lives "
          f"of it off; on, run_steps lives as run() and the lives move; {n_fact_} of {n_imp_} setbacks named a world fact "
          f"their kind follows; each kind's weight over the living averages 1 (worst {worst_:.3f}, {len(yrs_)} years)"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 25. what a world rewards (tilt_world, v25 #10; world_fit.tilt_year) and the neutral world (realm "neutral"), world on
if "tilt_world" in E.DEFAULT:
    import world_fit as WF_, realm_neutral as RN_
    t0 = time.process_time(); fails = []
    kw = dict(N=3, years=8, seed=5, lib=EARTH, log_lives=(0,))
    o0_ = E.run(**kw, P=dict(E.DEFAULT, world=True))
    seen_ = dict(years=0, moves=0, worst=0.0)
    for rl_ in ("earth", "neutral"):
        P1_ = dict(E.DEFAULT, world=True, tilt_world=True, realm=rl_)
        o1_ = E.run(**kw, P=P1_)
        if rl_ == "earth" and digest(o1_) == digest(o0_):
            fails.append("on: nothing moved")
        g = E.run_steps(**kw, P=P1_); msg = next(g); ver_ = 0
        while True:
            kind, t, S, val = msg
            if kind == "end" and S["age"] >= 1 and S.get("TW_ON"):
                PP_ = S["WL"].PP
                if getattr(PP_, "tilt_ver", 0) != ver_:   # a new year's r: each sphere's mean 1, every cell within .5..2
                    ver_ = PP_.tilt_ver; seen_["years"] += 1
                    lo_, hi_ = PP_._tilt_T["clip"]
                    for r_ in (PP_.tilt_r, PP_.tilt_town):
                        seen_["worst"] = max(seen_["worst"], float(np.abs(r_.mean(-1) - 1).max()))
                        if r_.min() < lo_ - 1e-9 or r_.max() > hi_ + 1e-9:
                            fails.append(f"{rl_}: a cell of r at {r_.min():.3f} or {r_.max():.3f}")
                        if rl_ == "neutral" and np.abs(r_ - 1).max() > 1e-12:   # the neutral world: r 1, always
                            fails.append(f"neutral: r off 1 by {np.abs(r_ - 1).max():.2g} at age {S['age']}")
                    pz_ = S["prizes"]
                    if pz_ is None or len(pz_) != 3 or any(len(d_) != 9 or any(len(v_) != 5 for v_ in d_.values()) for d_ in pz_):
                        fails.append(f"{rl_}: prizes malformed")
                    if not np.isfinite(PP_.tilt_gain).all() or (PP_.tilt_gain <= 0).any():
                        fails.append(f"{rl_}: a gain not finite and positive")
                if S["prizes_moves"] is not None:
                    seen_["moves"] = max(seen_["moves"], sum(len(m_) for m_ in S["prizes_moves"]))
                    if any(not {"sphere", "colour", "age", "by", "cause"} <= set(x_) or abs(x_["by"]) < 0.0195
                           for m_ in S["prizes_moves"] for x_ in m_):
                        fails.append(f"{rl_}: a move malformed or under .02")
            try:
                msg = g.send(val)
            except StopIteration as done:
                o2_ = done.value
                break
        if digest(o1_) != digest(o2_):
            fails.append(f"{rl_}: run_steps not the lives of run()")
        if rl_ == "neutral":   # the neutral world at its start: every sphere .2 a colour, places even, r 1 everywhere
            W_ = S["WL"].W; T_ = WF_.tilt_tables(RN_, W_.perm); M0_ = W_._sph_tables()["M0"]
            r0_, _ = WF_.tilt_town(W_, T_, {}, sph=np.tile(M0_, (W_.n_loc, 1, 1)))
            ho_ = np.abs(getattr(W_, "hp_off", np.zeros((1, 5)))).max(-1)   # a place's lasting lean: only a life's act
            if np.abs(M0_ - 0.2).max() > 0 or (ho_ > 0).mean() > 0.1 or not W_.p.get("inst_even") \
                    or np.abs(r0_ - 1).max() > 1e-12:            # (a founder's, a push) gives one in the neutral world
                fails.append(f"neutral: not even at the start (places with a lean of their own {(ho_ > 0).mean():.2f})")
    if seen_["worst"] > 1e-9:
        fails.append(f"a sphere's mean r off 1 by {seen_['worst']:.2g}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  what a world rewards (tilt_world), Earth and the neutral world, world on: "
          f"run_steps lives as run() and the lives move; {seen_['years']} years of r, each sphere's mean 1 (worst "
          f"{seen_['worst']:.1g}) and every cell within the realm's clip; prizes and {seen_['moves']} moves well formed; the "
          f"neutral world's r 1 at its start and every year{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 26. the land (wa_land, v25 lane D; world_land.py), Earth and packs with the Library's nature moments, world on
if "wa_land" in E.DEFAULT and os.path.exists(os.path.join(batch.LIB_DIR, "earth_nature.py")):
    from world_base import HAZARDS as HZ_
    from world_land import KIN_BITS as WL_KIN_
    t0 = time.process_time(); fails = []; seen_ = dict(years=0, company=0, ways=0, hit=0, hot=0, parts=[], helper=0)
    LAND_ = batch.load_batch("earth", packs=list(batch.PACKS), land=True)
    LM_ = np.array([bool(x_.get("land")) for x_ in LAND_["src"][:LAND_["S"]]])
    kw = dict(N=3, years=22, seed=5, lib=LAND_, log_lives=(0,))
    P0_ = dict(E.DEFAULT, world=True)
    o0_ = E.run(**kw, P=P0_)   # loaded with the switch off: no nature moment comes, and the run has no land
    if "land" in o0_ or any(LM_[s_] for _, _, s_ in o0_["life_events"]):
        fails.append("off: a nature moment came, or the run has a land")
    P1_ = dict(P0_, wa_land=True, scn=True, imp_world=True, wa_land_par=dict(hit_share=(1.0, 0.0)))
    o1_ = E.run(**kw, P=P1_)
    if digest(o1_) == digest(o0_):
        fails.append("on: nothing moved")
    for scn_ in (False, True):   # run_steps as run(); then with a flood and a poor harvest brought at 20 (scn)
        g = E.run_steps(**kw, P=P1_); msg = next(g); hit_w_ = None; kin_ = None
        while True:
            kind, t, S, val = msg
            ld_ = S["WL"].land if S.get("WL") is not None else None
            if kind == "week" and scn_ and abs(S["age"] - 20.0) < 1e-9:
                S["scn_hazard"].append(dict(kind="flood", severity=0.9)); S["scn_hazard"].append(dict(harvest="poor"))
                hit_w_ = int(S["WL"].PP.t); h0_ = ld_.h.copy()
            if kind == "week" and scn_ and abs(S["age"] - 21.0) < 1e-9:   # a heat strike: quarrels x 1.1 for its spell
                S["scn_hazard"].append(dict(kind="heat", severity=0.5))
            if kind == "week" and S.get("LAND_ON"):   # the heat's quarrels: People's ties tick reads the land's own array
                PP_ = S["WL"].PP; hq_, hw_ = ld_.E["heat_quarrel"]
                ex_ = np.where(((int(PP_.t) - ld_.heat_t[np.asarray(PP_.loc)]) < hw_) & ~np.asarray(PP_.dead, bool), hq_, 1.0)
                if PP_.quarrel_x is not ld_.qx or np.abs(np.asarray(PP_.quarrel_x, float) - ex_).max() > 1e-6:
                    fails.append(f"week {t}: the heat's quarrels are not x {hq_} for {hw_} weeks after a heat strike")
                seen_["hot"] += int((ex_ > 1).sum())
            if kin_ is not None and kind == "week" and int(S["WL"].PP.t) > kin_[1]:   # the kin's death read: recalled
                if not any(m_["cid"] == kin_[0] and m_.get("recalled") for m_ in ld_.mem[0]):
                    fails.append("company kin: the shared memory not recalled when that kin died")
                seen_["parts"].append("recall"); kin_ = None
            if kind == "situation" and S.get("LAND_ON"):   # the company: a kind the moment takes; alone has no one
                se_ = np.where(S["had_ev"], S["s_ev"], val)
                for n_, c_ in enumerate(S["company"]):
                    if c_ is None:
                        continue
                    seen_["company"] += 1
                    if c_["kind"] not in ld_.mwith[int(se_[n_])] or (c_["kind"] in ("alone", "stranger", "witness") and c_["cid"] != -1):
                        fails.append(f"week {t}: company {c_} in {LAND_['names'][int(se_[n_])]!r}")
            if kind == "end" and S.get("LAND_ON") and abs(S["age"] - round(S["age"])) < 1e-9 and len(fails) < 6:
                seen_["years"] += 1; W_ = S["WL"].W
                if not (0 <= ld_.h.min() and ld_.h.max() <= 1 and 0 <= ld_.wd.min() and ld_.wd.max() <= 1):
                    fails.append(f"age {S['age']}: a stretch out of 0..1")
                fl_, fi_ = HZ_.index("flood"), HZ_.index("fire")   # the feedback reads the land's physical state only
                if np.abs(W_.land_hx[:, fl_] - (1 + np.maximum(0, ld_.wd0[:, 2] - ld_.wd[:, 2]))).max() > 1e-12 or \
                        np.abs(W_.land_hx[:, fi_] - np.where(ld_.tend[:, 1] > 0, 1, 1 + 0.5 * np.maximum(0, ld_.wd[:, 1] - 0.6))).max() > 1e-12:
                    fails.append(f"age {S['age']}: the hazard feedback is not the land's state")
                wa0_, wa1_ = ld_.E["way_age"]   # a way from 14 (a helper beside an adult), its steps 1 and 2 from 18
                for n_ in range(3):
                    p_ = ld_.person(n_); seen_["ways"] = max(seen_["ways"], len(p_["ways"]))
                    if len(p_["ways"]) > 3 or any(not 0 <= w_["step"] <= 2 for w_ in p_["ways"]):
                        fails.append(f"life {n_}: ways {p_['ways']}")
                    if (S["age"] < wa0_ and p_["ways"]) or (S["age"] < wa1_ and any(w_["step"] > 0 for w_ in p_["ways"])) \
                            or any(w_["worked"] > S["age"] - wa0_ + 1e-9 for w_ in p_["ways"]):
                        fails.append(f"age {S['age']}: life {n_}'s ways {p_['ways']} before {wa0_}, or a step before {wa1_}")
                    seen_["helper"] += bool(S["age"] < wa1_ and p_["ways"])
                pv_ = S["WL"].PP.place_view(0)
                if not {"land", "land_hazard", "harvest", "ways", "bridges_open", "bridges_held"} <= set(pv_) or len(pv_["land"]) != 3:
                    fails.append("the place view has no land row")
            if hit_w_ is not None and kind == "situation" and int(S["WL"].PP.t) == hit_w_:   # the flood just brought
                lv_ = ~S["dead"]; loc_ = np.asarray(S["WL"].PP.loc)
                seen_["hit"] = int((ld_.hit_t == hit_w_).sum())
                if not (ld_.hit_t[lv_] == hit_w_).all() or not (ld_.shape[lv_] >= 0).all():
                    fails.append("scn: a flood at 20 did not hit every household (hit_share 1)")
                if (ld_.harvest[loc_] != 2).any() or (ld_.h[loc_, 2] >= h0_[loc_, 2]).any():
                    fails.append("scn: the poor harvest or the flood's hit on the water is not there")
                si_ = ld_.key_s["drain_the_marsh"][0]; a_ = [nt_.get("land") for nt_ in ld_.notes[si_]].index("U")
                l_ = int(loc_[0]); w0_ = ld_.wd[l_, 2]; x_ = ld_.decide(0, si_, a_, True, False, 3.0, 1.0, 1.0, hit_w_)
                exp_ = ld_.T["reach"]["known"]["clear"] * ld_.T["reach"]["k_land"] * 3.0 * 0.8   # the drain: wildness down
                if x_ is None or abs((w0_ - ld_.wd[l_, 2]) - min(exp_, w0_)) > 1e-9 or \
                        abs(S["WL"].W.land_hx[l_, HZ_.index("flood")] - (1 + max(0, ld_.wd0[l_, 2] - ld_.wd[l_, 2]))) > 1e-12:
                    fails.append(f"a Known drain of the marsh: wildness {w0_:.4f} -> {ld_.wd[l_, 2]:.4f}, flood x not the land's")
                hit_w_ = -1
                PP_ = S["WL"].PP; tn_ = int(PP_.t)   # the company's lasting parts and notice, on life 0 to 2
                sn_ = PP_.snorm[0].astype(float).copy(); ld_._group_norm(0, "G", tn_)   # a group: its norm toward G
                dn_ = PP_.snorm[0].astype(float) - sn_; j_ = int(np.abs(dn_).sum(1).argmax())
                if np.abs(dn_).sum() > 0 and (dn_[j_, 4] <= 0 or abs(PP_.snorm[0, j_].sum() - 1) > 1e-5
                                              or dn_[j_, 4] > ld_.E["group_norm"] + 1e-6):
                    fails.append(f"company group: the norm moved {dn_[j_].round(4)}, not a little toward G")
                seen_["parts"].append("norm" if np.abs(dn_).sum() > 0 else "no group")
                kk_ = np.nonzero(PP_.used[0] & PP_.lv[0] & ((PP_.rmask[0] & WL_KIN_) != 0))[0]
                if len(kk_):   # kin: the shared memory kept, then recalled when they die
                    k_ = int(kk_[0]); u_ = int(PP_.uid[0, k_]); m0_ = len(ld_.mem[0])
                    ld_._company_fx(0, dict(kind="kin", cid=u_), "W", tn_, si_, S["age"])
                    if len(ld_.mem[0]) != m0_ + 1 or ld_.mem[0][-1]["cid"] != u_:
                        fails.append("company kin: no shared memory kept")
                    PP_._die(np.array([0]), np.array([k_]), tn_); kin_ = (u_, tn_)
                ld_.E = dict(ld_.E, notice=dict(ld_.E["notice"], push_p=1.0, ask_y=1.0))   # notice, sure for the test
                ld_.push.pop(1, None); ld_.push.pop(2, None); lb_ = ld_.lean[1].copy()
                ld_._notice(1, "B", 0, tn_); ld_._notice(2, "G", 1, tn_)   # B costs the land (tenders), G the yield (farmers)
                if ld_.push.get(1, [None])[0] != ld_.E["notice"]["push_tend"]["field"] or \
                        ld_.push.get(2, [None])[0] != ld_.E["notice"]["push_work"] or ld_.lean[1, 1] != lb_[1] + 1:
                    fails.append(f"notice: the pushback {ld_.push.get(1)}, {ld_.push.get(2)} or the lean not as the faces cost")
                ld_.lean[0] = (3.0, 0.0); ld_.lean_j[0] = 1; a0_ = ld_.st["asks"]; ld_.news = []
                ld_._asks(tn_, S["age"])
                ask_ = [x_ for n_, x_ in ld_.news if n_ == 0 and x_.get("kind") == "land_ask"]
                if ld_.st["asks"] <= a0_ or not ask_ or ask_[0]["by"] != "tenders" or \
                        ld_.WAYS[ld_.WK[ask_[0]["way"]]]["stretch"] != "wood" or ld_.WAYS[ld_.WK[ask_[0]["way"]]]["lead"][0] not in "WG":
                    fails.append(f"notice: a tender's lean not asked in to a tenders' way on its stretch: {ask_}")
                seen_["parts"].append("notice")
            try:
                msg = g.send(val)
            except StopIteration as done:
                o2_ = done.value
                break
        if not scn_ and digest(o1_) != digest(o2_):
            fails.append("on: run_steps not the lives of run()")
        if scn_ and hit_w_ != -1:
            fails.append("scn: the flood's week never came")
        if scn_ and not seen_["hot"]:
            fails.append("scn: the heat brought at 21 never made a hot week")
    ld1_ = o1_.get("land") or {}
    ev_ = sorted((n_, t_) for n_, t_, s_ in o1_["life_events"] if LM_[s_])
    gap_ = min([b_[1] - a_[1] for a_, b_ in zip(ev_, ev_[1:]) if a_[0] == b_[0]] or [99])
    if not ev_ or gap_ < 13:
        fails.append(f"the budget: {len(ev_)} nature moments, the least gap {gap_} weeks")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  the land (wa_land), world on: loaded with it off no nature moment comes; on, "
          f"run_steps lives as run() and the lives move; {len(ev_)} nature moments, never two in a quarter; {seen_['company']} "
          f"companies of the moment's kinds; the stretches in 0..1 and the hazards' feedback the land's own state "
          f"({seen_['years']} years); ways at most 3 (most {seen_['ways']}), none before 14 and no step before 18 "
          f"({seen_['helper']} helper life-years); a flood brought at 20 hit {seen_['hit']} "
          f"households, each with its course; a Known drain of the marsh moves its wildness by size x k_land x reach and the "
          f"flood odds with it; heat's quarrels x 1.1 for its spell ({seen_['hot']} life-weeks); {', '.join(seen_['parts'])} "
          f"as the company and notice say; counts {dict((k_, (ld1_.get('counts') or {}).get(k_)) for k_ in ('asks', 'pushes', 'memories', 'recalls', 'norm_moves'))}"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 27. national standing (wa_nat_climb, v25 lane D; world_national.py), Earth and packs with the Library's national moments
if "wa_nat_climb" in E.DEFAULT and os.path.exists(os.path.join(batch.LIB_DIR, "earth_national.py")):
    import world_national as WN_
    t0 = time.process_time(); fails = []; seen_ = dict(kinds={k_: 0 for k_ in WN_.KINDS}, seats=0, natdec=0, voice=0, vdec=0)
    NAT_ = batch.load_batch("earth", packs=list(batch.PACKS), national=True)
    NM_ = np.array([bool(x_.get("route") or x_.get("style") or x_.get("scope")) for x_ in NAT_["src"][:NAT_["S"]]])
    kw = dict(N=3, years=24, seed=5, lib=NAT_, log_lives=(0,))
    P0_ = dict(E.DEFAULT, world=True)
    o0_ = E.run(**kw, P=P0_)   # loaded with the switch off: no national moment comes, and the run has no national
    if "national" in o0_ or any(NM_[s_] for _, _, s_ in o0_["life_events"]):
        fails.append("off: a national moment came, or the run has national standing")
    P1_ = dict(P0_, wa_nat_climb=True, wa_nat_par=dict(base=1.0, rung_years=0))   # every adult at a wider step, each
    o1_ = E.run(**kw, P=P1_)                                                      # kind a year: the rules, not the odds
    if digest(o1_) == digest(o0_):
        fails.append("on: nothing moved")

    def nat_steps_(P_, all_):
        """run_steps with national standing on, checked at each mid-year (the yearly climb is settled): Known in phase 2
        by national standing only with a seat held or a national name (a voice alone is not: Vision 10-23)."""
        g = E.run_steps(**kw, P=P_); msg = next(g)
        while True:
            kind, t, S, val = msg
            if kind == "end" and S.get("NAT_ON") and abs(S["age"] % 1 - 0.5) < 1e-9 and len(fails) < 6:   # mid-year
                nt_ = S["WL"].nat; PP_ = S["WL"].PP; dd_ = np.asarray(PP_.dead, bool)
                nk_ = nt_.known(); hk_ = np.asarray(S["ht_t"])[:, 0] >= 0 if S.get("ht_t") is not None else np.zeros(len(nk_), bool)
                if (nk_ & ~dd_ & ~PP_.wa_known).any():
                    fails.append(f"age {S['age']}: a seat or a national name not Known in phase 2")
                if (PP_.wa_known & ~nk_ & ~hk_ & ~dd_).any():
                    fails.append(f"age {S['age']}: Known in phase 2 without the heights, a seat or a national name")
                seen_["voice"] += int((nt_.influence_only() & ~nk_ & ~dd_).sum())
                if all_:
                    seats_ = [x_["authority"]["seat"] for x_ in nt_.kind if x_.get("authority", {}).get("held")]
                    if len(seats_) != len(set(seats_)) or any(nt_.seats[s_]["exists"] for s_ in seats_):
                        fails.append(f"age {S['age']}: seats {seats_} held twice or one of the engine's own offices")
                    for n_, x_ in enumerate(nt_.kind):
                        for k_ in x_:
                            seen_["kinds"][k_] += 1
                        if x_ and S["age"] < 18:
                            fails.append(f"age {S['age']}: national standing before 18")
                    nat_ = nt_.national()
                    if (PP_.wa_nat & ~nat_ & ~np.asarray(S["WL"].gov_office, bool)).any():
                        fails.append(f"age {S['age']}: at national standing in phase 2 without a seat, a voice or an office")
                    if (nt_.dom[nat_].max(1) < 3).any() if nat_.any() else False:
                        fails.append(f"age {S['age']}: a national voice or seat without level 3 in its domain")
                    pv_ = PP_.place_view(0)
                    if set(pv_.get("national", {})) != set(WN_.KINDS) | {"years_at_rung4"}:
                        fails.append("the place view has no national standing")
            try:
                msg = g.send(val)
            except StopIteration as done:
                return done.value

    o2_ = nat_steps_(P1_, True)
    if digest(o1_) != digest(o2_):
        fails.append("on: run_steps not the lives of run()")
    for d_ in (o1_.get("wa_ledger") or {}).get("decisions", []):
        if d_.get("scope") == "nation":
            seen_["natdec"] += 1
            if not d_.get("national"):
                fails.append("a decision at nation scope by a life not at national standing")
    if not seen_["natdec"]:
        fails.append("no decision at nation scope")
    if not all(seen_["kinds"].values()):
        fails.append(f"a kind never reached: {seen_['kinds']}")
    # a voice alone (influence, no name, no seat): Known only by the heights, so its nation-scope decisions are a Known
    # life's
    o3_ = nat_steps_(dict(P1_, wa_nat_par=dict(base=dict(recognition=0.0, influence=1.0, authority=0.0), rung_years=0)), False)
    seen_["vdec"] = sum(d_.get("scope") == "nation" for d_ in (o3_.get("wa_ledger") or {}).get("decisions", []))
    if not seen_["voice"]:
        fails.append("no life held a voice alone")
    # aims v2 (lane B): the national pack's route fields join the agenda only with national standing on, and aim_x reads
    # an aim on the agenda whose next rung is a seat in the climb's sphere (National._aimed); without it, the goal's sphere
    if "aims_v2" in E.DEFAULT and os.path.exists(os.path.join(batch.PACK_DIR, "national", "fields.py")):
        from world_keys import SPHERES as SPH_

        def nat_aims_(P_, probe):
            g = E.run_steps(**dict(kw, years=4), P=P_); msg = next(g); src_ = None   # (pauses past 3)
            while True:
                kind, t, S, val = msg
                if src_ is None and S.get("aim2") is not None:
                    src_ = {it_["src"] for it_ in S["aim2"].ag.F["items"]}
                if probe and kind == "end" and S.get("WL") is not None and S["WL"].nat is not None and "aimed" not in seen_:
                    nt_ = S["WL"].nat; AG_ = nt_.AG; F_ = AG_.F; go_ = np.full(nt_.N, -1)
                    fi_ = F_["names"].index("to keep the country's wild places"); nr_ = int(F_["nr"][fi_])
                    sj_ = SPH_.index(nt_.seats["head of the national parks"]["sphere"])
                    ri_ = [r_["key"] for r_ in nt_.routes].index("living_land_steward")
                    keep_ = (int(AG_.f[0, 0]), int(AG_.st[0, 0]), int(AG_.rung[0, 0]))
                    AG_.f[0, 0] = fi_; AG_.st[0, 0] = 0; AG_.rung[0, 0] = nr_ - 1   # held, the seat next
                    a1_ = nt_._aimed(0, sj_, go_); a2_ = nt_._aimed(0, (sj_ + 1) % len(SPH_), go_)
                    AG_.rung[0, 0] = nr_ - 2; a3_ = nt_._aimed(0, sj_, go_)            # a rung below: not yet
                    AG_.f[0, 0], AG_.st[0, 0], AG_.rung[0, 0] = keep_
                    seen_["aimed"] = (a1_, a2_[0], a3_[0])
                    if a1_ != (True, ri_) or a2_[0] or a3_[0]:
                        fails.append(f"aims v2: aim_x not by an aim whose next rung is the seat in its sphere: {seen_['aimed']}")
                try:
                    msg = g.send(val)
                except StopIteration:
                    return src_ or set()
        if "pack:national" in nat_aims_(dict(P0_, aims_v2=True), False):
            fails.append("aims v2: the national pack's fields without national standing")
        if "pack:national" not in nat_aims_(dict(P1_, aims_v2=True), True) or "aimed" not in seen_:
            fails.append("aims v2: the national pack's fields not on the agenda with national standing, or aim_x unread")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  national standing (wa_nat_climb), world on: loaded with it off no national "
          f"moment comes; on, run_steps lives as run() and the lives move; recognition, influence and authority apart "
          f"({seen_['kinds']} life-years), a seat held once and never an engine office, phase 2's national only with a "
          f"seat, a voice or an office, Known by national standing only with a seat or a name, {seen_['natdec']} "
          f"decisions at nation scope all by national lives; a voice alone ({seen_['voice']} life-years) Known only by "
          f"the heights ({seen_['vdec']} at nation scope); with aims v2 the national fields only with it on, aim_x by an "
          f"aim whose next rung is the seat ({seen_.get('aimed')}){'' if not fails else '; ' + '; '.join(fails[:4])} "
          f"({time.process_time() - t0:.0f} s)")
# 28. aims v2 (aims_v2; v25 lane B, Emren's decision #9), Earth and packs with the Library's fields (or v1's adapter)
if "aims_v2" in E.DEFAULT:
    import foresee as FS_
    t0 = time.process_time(); fails = []
    LB_ = batch.load_batch("earth", packs=list(batch.PACKS))
    seen_ = dict(arrived=0, tests=0, forks=0, answered=0, entries=0, views=0, closed=0, paused=0, moments=0, own=0, told=0)
    import aims2 as A2M_
    WIN_ = {nm_: {0: dict(window=dict(deadline_years=3)), 1: dict(window=dict(deadline_years=4))}
            for nm_ in A2M_.compile_fields(LB_, A2M_.PAR, E.C, E.NIDX, E.AIM_HEIGHTS)["names"]}
    LBF_ = batch.load_batch("earth", packs=list(batch.PACKS), fields=True) if "fields" in batch.load_batch.__code__.co_varnames else None
    ASM_ = np.nonzero(np.asarray(LBF_["AIM_SHAPE"]) != -1)[0] if LBF_ is not None and "AIM_SHAPE" in LBF_ else np.zeros(0, int)
    if len(ASM_):   # with the switch off, the batch's shape moments never come
        o0_ = E.run(N=3, years=30, seed=6, lib=LBF_, P=dict(E.DEFAULT, world=False))
        if np.asarray(o0_["sit_n"])[:, ASM_].sum():
            fails.append("a shape moment came with aims_v2 off")
    cases_ = [(False, 4, 40, 9, LB_, WIN_), (True, 2, 25, 4, LB_, None)] + ([(False, 3, 30, 6, LBF_, None)] if len(ASM_) else [])
    for wl_, N_, Y_, sd_, LL_, FP_ in cases_:   # world off: every field's first two rungs with a deadline; then the shape moments
        P_ = dict(E.DEFAULT, aims_v2=True, world=wl_, aims2_par=dict(player=(0,), field_patch=FP_))
        kw = dict(N=N_, years=Y_, seed=sd_, lib=LL_, log_lives=(0,))
        o1_ = E.run(**kw, P=P_)
        for edit_ in (False, True):
            g = E.run_steps(**kw, P=P_); msg = next(g); made_ = {}; done_ = set(); ans_ = None; pz_ = None; told_ = None
            while True:
                kind, t, S, val = msg
                if S.get("AIM2_ON") and kind == "odds" and S["AG"].told[0]:   # the player's fork moment, not asked (the
                    AG_ = S["AG"]; fk_ = AG_.own_fork(0, int(S["s"][0]))     # game never sets pick_asked here): "later"
                    j_ = fk_["aims"][0]
                    told_ = (t, fk_["id"], (AG_.F["names"][int(AG_.f[0, j_])], int(AG_.rung[0, j_])), len(AG_.log),
                             int(AG_.st[0, j_]), float(AG_.inten[0, j_]))
                if S.get("AIM2_ON") and kind == "learn" and told_ is not None and told_[0] == t and float(np.asarray(val)[0]) != 0.0:
                    fails.append("a player's fork moment not asked taught the life (drift from an unasked later)")
                if S.get("AIM2_ON") and kind == "end" and told_ is not None and told_[0] == t:
                    AG_ = S["AG"]; seen_["told"] += 1; j_ = next(iter(x_["aims"][0] for x_ in AG_.forks[0] if x_["id"] == told_[1]), None)
                    if j_ is None:
                        fails.append("a player's fork moment not asked closed its fork")
                    if not bool(np.asarray(S["idle"])[0]):
                        fails.append("a player's fork moment not asked applied its option (its week not idle)")
                    if any(r_["life"] == 0 and r_.get("id") == told_[1] and r_["what"] == "decided" for r_ in AG_.log[told_[3]:]):
                        fails.append("a player's fork moment not asked decided its fork")
                    if any((e_["field"], e_["rung"]) == told_[2] and e_["week"] == t for e_ in AG_.entry_log[0]):
                        fails.append("a player's fork moment not asked charged its entry")
                    if not any(r_["life"] == 0 and r_["what"] == "moment" and r_.get("told") and r_["tag"] == "later" and r_["week"] == t for r_ in AG_.log):
                        fails.append("a player's fork moment not asked not answered later")
                    told_ = None
                if S.get("AIM2_ON") and kind in ("situation", "end") and S["age"] >= 3:
                    AG_ = S["AG"]
                    for nm_ in ("AG", "aim2", "capacity", "aim_forks", "aim_fork"):
                        if nm_ not in S:
                            fails.append(f"{nm_} not handed over")
                    if kind == "situation" and len(AG_.SM):   # a shape moment only to a life holding an aim it fits
                        for n_ in np.nonzero(np.isin(S["s"], AG_.SM))[0]:
                            seen_["moments"] += 1
                            if AG_.mom[n_] < 0:
                                fails.append("a shape moment to a life with no aim it fits")
                    if kind == "situation" and AG_.put_si[0] >= 0:   # a fork put on its own moment: that is the week's
                        seen_["own"] += 1
                        if int(S["s"][0]) != int(AG_.put_si[0]) or int(AG_.mom[0]) != int(AG_.put_slot[0]):
                            fails.append("a fork put on its own moment that is not the week's moment")
                    if kind == "situation" and not edit_ and t % 52 == 0:   # the views, read-only: no life moves
                        A_ = FS_.agenda(S, 0); seen_["views"] += 1
                        if sorted(x_["priority"] for x_ in A_["items"]) != list(range(1, len(A_["items"]) + 1)):
                            fails.append("agenda priorities not 1..n")
                        for x_ in A_["items"]:
                            FS_.preview(S, 0, x_["slot"])
                        if AG_.forks[0]:
                            FS_.review(S, 0, AG_.forks[0][0]["id"])
                    if kind == "situation" and edit_ and AG_.put_arr[0] >= 0 and ans_ is None and S["age"] >= 15:
                        fk_ = next(x_ for x_ in AG_.forks[0] if x_["id"] == AG_.put_arr[0])   # the player answers one
                        o_ = next((x_ for x_ in ("go_on", "pay", "take", "round", "keep") if x_ in fk_["options"]), None)
                        if o_ is not None:
                            r_ = FS_.apply_review(S, 0, dict(choices={fk_["id"]: o_}, set={}))
                            ans_ = (fk_["id"], fk_["aims"][0], t); seen_["answered"] += 1
                            if r_["errors"]:
                                fails.append(f"apply_review: {r_['errors']}")
                    if kind == "situation" and edit_ and ans_ is not None and pz_ is None and t - ans_[2] >= 104:
                        j_ = ans_[1]   # pause and resume the answered aim: its entry is not charged again
                        if AG_.st[0, j_] == 1:
                            had_ = {(e_["field"], e_["rung"]) for e_ in AG_.entry_log[0]}; n0_ = len(AG_.entry_log[0])
                            FS_.set_pace(S, 0, j_, "paused"); FS_.set_pace(S, 0, j_, "pursuing")
                            pz_ = t; seen_["paused"] += 1
                            if any((e_["field"], e_["rung"]) in had_ for e_ in AG_.entry_log[0][n0_:]):
                                fails.append("an entry charged again after a pause and resume")
                    if kind == "end":
                        F_ = AG_.F; f_ = AG_.f
                        for fk_ in AG_.forks[0]:   # the player's forks: kept until answered, blocking only their aims
                            e0_ = made_.setdefault(fk_["id"], {j_: float(AG_.eff[0, j_]) for j_ in fk_["aims"]})
                            for j_ in fk_["aims"]:   # effort waits at the need (or where it stood when the fork came)
                                if fk_["kind"] != "over" and AG_.eff[0, j_] > max(AG_.need[0, j_], e0_.get(j_, 0.0)) + 1e-9:
                                    fails.append("effort past the need while the player's fork waits")
                        open_ = {x_["id"] for x_ in AG_.forks[0]}
                        for id_ in list(made_):
                            if id_ not in open_ and id_ not in done_:
                                done_.add(id_)
                                if not any(((r_["what"] == "decided" and r_.get("by") == "player") or r_["what"] == "fork lapsed")
                                           and r_.get("id") == id_ and r_["life"] == 0 for r_ in AG_.log):   # or lapsed: its window closed
                                    fails.append(f"the player's fork {id_} resolved without the player")
                        if t % 52 == 0:   # a reached rung: one of its titles held or once held, or a test won (never effort alone)
                            won_ = {(r_["life"], r_["slot"], r_["rung"]) for r_ in AG_.log if r_["what"] == "arrived" and r_["how"].startswith("won")}
                            for n_, j_ in zip(*np.nonzero(f_ >= 0)):
                                fi_ = int(f_[n_, j_])
                                for k_ in range(int(AG_.rung[n_, j_])):
                                    if (int(n_), int(j_), k_) in won_ or S["r_ever"][n_, F_["ids"][fi_][k_]].any() or (wl_ and F_["h"][fi_, k_] == 1):
                                        continue
                                    fails.append(f"{F_['names'][fi_]}: rung {k_ + 1} reached with no outcome")
                try:
                    msg = g.send(val)
                except StopIteration as done:
                    o2_ = done.value
                    break
            if not edit_ and digest(o1_) != digest(o2_):
                fails.append(f"world {'on' if wl_ else 'off'}: run_steps (reading the agenda, its previews and reviews) not the lives of run()")
            a2_ = o2_["aims2"]; lg_ = a2_["log"]
            closed_ = {}
            for r_ in lg_:
                if r_["what"] == "window closed":
                    k_ = (r_["life"], r_["slot"], r_["rung"])
                    if k_ in closed_:
                        fails.append("a window's closing told twice")
                    closed_[k_] = r_["week_closed"]; seen_["closed"] += 1
                    if r_["week"] != r_["week_closed"] + 1:
                        fails.append(f"a window told closed at week {r_['week']}, its last week {r_['week_closed']}")
            rounds_ = set()   # a way round found after the window closed (another route, not the window reopened)
            for r_ in lg_:
                k_ = (r_["life"], r_["slot"], r_["rung"])
                if r_["what"] == "decided" and r_.get("option") == "round":
                    rounds_.add(k_)
                if r_["what"] == "test":
                    seen_["tests"] += 1
                    if k_ in closed_ and r_["week"] > closed_[k_] and k_ not in rounds_:
                        fails.append("a test after its window closed")
                if r_["what"] == "arrived":
                    seen_["arrived"] += 1
                    if not (r_["how"] == "its title held" or r_["how"].startswith("won")):
                        fails.append(f"a rung reached by {r_['how']}")
                if r_["what"] == "fork":
                    seen_["forks"] += 1
            for n_ in range(N_):
                if len({(e_["field"], e_["rung"]) for e_ in a2_["entries"][n_]}) != len(a2_["entries"][n_]):
                    fails.append("an entry cost charged twice")
                seen_["entries"] += len(a2_["entries"][n_])
    if not seen_["arrived"] or not seen_["forks"] or not seen_["answered"] or not seen_["closed"] or (len(ASM_) and not (seen_["moments"] and seen_["told"])):
        fails.append(f"too little seen: {seen_}")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  aims v2 (aims_v2), switched on with a player's life (world off and on): run_steps "
          f"lives as run() with the agenda, previews and reviews read ({seen_['views']} reads); {seen_['arrived']} rungs reached, "
          f"each through an outcome ({seen_['tests']} tests); {seen_['closed']} windows closed, each told once at its last "
          f"week + 1, no test after; {seen_['forks']} forks, the player's kept until answered ({seen_['answered']} answered; {seen_['own']} put on their own moment) and "
          f"blocking only their aims, {seen_['told']} fork moments not asked left open, nothing taught or charged; {seen_['entries']} entry costs, none twice ({seen_['paused']} paused and resumed); "
          f"{seen_['moments']} shape moments (batch FIELDS), each to a life with an aim it fits, none with the switch off"
          f"{'' if not fails else '; ' + '; '.join(sorted(set(fails))[:4])} ({time.process_time() - t0:.0f} s)")
# 29. reactions, clashes and seeking (react, clash, seek; v25 lane C, decisions #2 to #4), Earth and packs, world on
if "react" in E.DEFAULT and "clash" in batch.load_batch.__code__.co_varnames:
    t0 = time.process_time(); fails = []
    import world_react as WRX_
    L26_ = batch.load_batch("earth", packs=list(batch.PACKS), clash=True, seek=True)
    kw = dict(N=6, years=18, seed=5, lib=L26_, log_lives=(0,))
    P0_ = dict(E.DEFAULT, world=True)
    o0_ = E.run(**kw, P=dict(P0_))
    kwo_ = dict(N=4, years=5, seed=7, lib=EARTH, log_lives=(0,))   # world off: the switches do nothing
    if digest(E.run(**kwo_, P=dict(E.DEFAULT, react=True, clash=True, seek=True))) != digest(E.run(**kwo_, P=dict(E.DEFAULT))):
        fails.append("world off: react moved the lives")
    P1_ = dict(P0_, react=True)   # react alone: run_steps lives as run(), the lives move
    o1_ = E.run(**kw, P=P1_)
    if digest(o1_) == digest(o0_):
        fails.append("react: nothing moved")
    if digest(o1_) != digest(_drain(E.run_steps(**kw, P=P1_))):
        fails.append("react: run_steps not the lives of run()")
    P2_ = dict(P0_, react=True, clash=True, seek=True)
    o2_ = E.run(**kw, P=P2_)
    V25_S_ = set(np.nonzero((np.asarray(L26_["W_CLASH"]) >= 0) | (np.asarray(L26_["W_STATE"]) >= 0)
                            | (np.asarray(L26_["REPAIR_TAG"]) >= 0).any(1))[0].tolist())
    g = E.run_steps(**kw, P=P2_); msg = next(g); n_put_, n_seen_ = 0, 0
    while True:
        kind, t, S, val = msg
        if kind == "end" and S["age"] >= 3:
            if not all(S.get(sw_) for sw_ in ("RX_ON", "CL_ON", "SK_ON")) or any(nm_ not in S for nm_ in
                    ("demands", "responses", "react_log", "involve", "states", "clash", "disputes", "clash_now", "seek")):
                fails.append("a v25 name or switch not handed over"); break
            for n_ in range(6):
                for st_, v_ in (S["states"][n_] or {}).items():   # states carry their durations
                    if not (0 <= v_["level"] <= 1 and v_["weeks"] >= 0) and len(fails) < 6:
                        fails.append(f"life {n_} state {st_} {v_}")
                if S["seek"][n_]["k"] > 1 / 3 + 1e-9 and len(fails) < 6:   # k at most 1/3 at full independence
                    fails.append(f"life {n_} seek k {S['seek'][n_]['k']}")
        if kind == "situation" and S["age"] >= 10:
            c_ = S["clash"]
            n_seen_ += sum(1 for n_ in range(6) if c_[n_] is not None)
        try:
            msg = g.send(val)
        except StopIteration as done:
            o3_ = done.value
            break
    d2_, d3_ = digest(o2_), digest(o3_)
    if d2_ != d3_:
        fails.append("all on: run_steps not the lives of run() (" + " ".join(sorted(k_ for k_ in d2_ if d2_[k_] != d3_.get(k_))[:6]) + ")")
    rx_ = o2_["react"]; cl_ = rx_["clash"]; thr_ = WRX_.CLASH_DEFAULT["thr"]
    for n_, wk_ in enumerate(cl_["weeks"]):   # no clash without stakes; from 10; one a sphere (every sphere the
        # dispute touches) in 2 years; before 18 one in 2 years in any sphere; 3 in 10 years, one before 18 counting .5
        for i_, (t_, sp_, k_, a_) in enumerate(wk_):
            if k_ < thr_ or t_ < 520 or any(t2_ > t_ - 104 and set(sp2_) & set(sp_) for t2_, sp2_, _, _ in wk_[:i_]) \
                    or (a_ < 18 and any(t2_ > t_ - 104 for t2_, _, _, _ in wk_[:i_])) \
                    or sum(0.5 if a2_ < 18 else 1.0 for t2_, _, _, a2_ in wk_[:i_] if t2_ > t_ - 520) >= 3 - 1e-9:
                fails.append(f"life {n_}: clash at week {t_}, sphere {sp_}, stakes {k_:.2f} breaks a ceiling"); break
    met_ = sum(1 for n_, t_, s_ in o2_["life_events"] if s_ in V25_S_)   # each v25 moment met took an ask's place
    n_put_ = cl_["replaced_event"] if "replaced_event" in cl_ else 0
    n_put_ += cl_["dropped_natural"] + cl_.get("replaced_week", 0)   # (a played life's: the week's own moment too)
    if met_ > n_put_:
        fails.append(f"{met_} clash, seeking or repair moments met, only {n_put_} asks replaced")
    for n_, lg_ in enumerate(rx_["log"]):   # seeking and repair answers never take a colour step
        if any(e_.get("seek") is not None and (e_.get("layers") or {}).get("drift") for e_ in lg_):
            fails.append(f"life {n_}: a seeking answer moved colours"); break
    for n_, tr_ in enumerate((rx_["seek"] or {}).get("tried", [])):   # admission only through access and a place
        if any(r_["admitted"] and (not r_["access"] or r_["place"] < 0) for r_ in tr_):
            fails.append(f"life {n_}: admitted with no access or place"); break
    if not cl_["put"]:
        fails.append("no clash put in 6 lives x 18 years")
    p_put_, p_mom_ = len(cl_["weeks"][0]), len(cl_["moments"][0])   # the played life (log_lives 0): its clashes as moments
    if p_mom_ > p_put_ or (p_put_ >= 2 and p_mom_ * 2 < p_put_):
        fails.append(f"the played life: {p_mom_} clash moments of {p_put_} clashes")
    # the caller's demand (P["scn"]): its tag and a forced response reach the record, through the same path
    # and its stakes, given as a number, are taken as given (a demand recorded with them, or a dispute opened that week)
    P4_ = dict(P2_, scn=True); g = E.run_steps(**kw, P=P4_); msg = next(g); sent_, st_sent_, st_ok_ = False, -1, None
    while True:
        kind, t, S, val = msg
        if kind == "week" and not sent_ and S["age"] >= 17.8:   # (late: the record keeps the last 40)
            S["scn_demand"][0].append(dict(source=dict(key="household"), tag="t26", response="accept")); sent_ = True
        if kind == "week" and st_sent_ < 0 and S["age"] >= 16.0:
            pu_ = [0.0, 0.0, 1.0, 0.0, 0.0]   # two caller demands in one week, alike (one dispute): each its own record
            S["scn_demand"][1].append(dict(source=dict(key="household"), tag="t26s", stakes=0.9, purpose=pu_))
            S["scn_demand"][1].append(dict(source=dict(key="class"), tag="t26t", stakes=0.9, purpose=pu_)); st_sent_ = t
        if kind == "end" and t == st_sent_:
            st_ok_ = any(d_.get("tag") == "t26s" and d_["stakes"]["score"] == 0.9 for d_ in S["demands"][1]) \
                or any(d_["since"] == t for d_ in S["disputes"][1])
            for tg2_, key2_ in (("t26s", "household"), ("t26t", "class")):
                rc_ = [d_ for d_ in S["demands"][1] if d_.get("tag") == tg2_]
                if len(rc_) != 1 or rc_[0]["source"]["key"] != key2_:
                    fails.append(f"scn: two caller demands in a week, {tg2_} ({key2_}) on "
                                 f"{[(d_['id'], d_['source']['key']) for d_ in rc_]}")
        try:
            msg = g.send(val)
        except StopIteration as done:
            o4_ = done.value
            break
    tg_ = [e_ for e_ in o4_["react"]["log"][0] if e_.get("tag") == "t26"]
    if sent_ and not (tg_ and tg_[0]["response"] == "accept"):
        fails.append(f"scn: the caller's demand not in the record as asked ({tg_[:1]})")
    if not st_ok_:
        fails.append("scn: the caller's stakes not taken as given")
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  reactions, clashes and seeking (react, clash, seek), world on: world off "
          f"nothing; react alone and all on, run_steps lives as run() and the lives move; {cl_['put']} clashes, every one "
          f"with stakes and within the ceilings; {met_} clash, seeking or repair moments met, each in place of an ask; "
          f"{n_seen_} clash cards seen at the situation pause; the played life's clashes {p_put_}, {p_mom_} as moments; seeking moves no colour and admits only through a place; "
          f"the caller's demand recorded with its tag, response and stakes (two in a week: each tag on its own record)"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 30. WA3, a standing level reaches its town (wa_reach, v25; world_people_answers.WA_REACH), world on
if "wa_reach" in E.DEFAULT:
    import world_people_answers as WPA_
    from world_keys import LEVERS as LV30_
    from world_people_base import DI as DI30_, REACH as RE30_
    t0 = time.process_time(); fails = []; seen_ = dict(lever=[], town=0, groups=0, linger=None)
    L30_ = batch.load_batch("earth", packs=list(batch.PACKS), wa=True, aims=bool(E.DEFAULT.get("aims")),
                            foot=bool(E.DEFAULT.get("foot_on")))
    P30_ = dict(E.DEFAULT, world=True)
    kw = dict(N=2, years=12, seed=11, lib=L30_, log_lives=(0,))
    if digest(E.run(**kw, P=dict(P30_, world_answers=False, wa_reach=False))) != digest(E.run(**kw, P=dict(P30_, world_answers=False))):
        fails.append("world answers off: the switch moved a life")
    kw = dict(N=3, years=30, seed=11, lib=L30_, log_lives=(0,))
    o0_ = E.run(**kw, P=dict(P30_, wa_reach=False)); o1_ = E.run(**kw, P=P30_)
    if digest(o0_) == digest(o1_):
        fails.append("on: nothing moved")
    g = E.run_steps(**kw, P=P30_); msg = next(g)
    while True:
        kind, t, S, val = msg
        try:
            msg = g.send(val)
        except StopIteration as done:
            if digest(done.value) != digest(o1_):
                fails.append("on: run_steps not the lives of run()")
            break
    # the rules, on a life at a pause (the run left there)
    g = E.run_steps(N=3, years=12, seed=11, lib=L30_, P=P30_); msg = next(g)
    while True:
        kind, t, S, val = msg
        if kind == "end" and S.get("WL") is not None and S["age"] >= 11:
            PP_ = S["WL"].PP; W_ = PP_.W; N_ = PP_.N; lv_ = np.arange(N_) % 3
            PP_.standing[:, 0] = lv_; PP_.wa_held[:] = WPA_.NEVER
            if not PP_.wa_r or not np.array_equal(PP_.wa_treach(), RE30_[lv_, 2]) or list(RE30_[:, 2]) != [0, 1, 2, 3]:
                fails.append("the switch not read, or the town's ring reach not REACH[level, 2]")
            # the level lingers: level 2 last held 3, 6, 11 years ago reads 2, 1, 0 (one level per 5 years after 5)
            PP_.standing[0, 0] = 0; ly_ = []
            for y_ in (3, 6, 11):
                PP_.wa_held[0] = WPA_.NEVER; PP_.wa_held[0, :3] = t - int(y_ * 52)
                ly_.append(int(PP_.wa_level(0, t)))
            seen_["linger"] = ly_
            if ly_ != [2, 1, 0]:
                fails.append(f"the lingering level: level 2 held 3, 6, 11 years ago reads {ly_}")
            PP_.wa_held[:] = WPA_.NEVER; PP_.standing[:, 0] = lv_
            # groups (A): a member's presence x (1 + .5 x the level's reach at the town's ring)
            PP_._wa_yr = int(PP_._age(t)); PP_._wa_held = lambda t_: None   # (the levels held: set above)
            s0_ = PP_.snorm.copy(); PP_.wa_r = False; PP_._wa_month(t); d0_ = np.abs(PP_.snorm - s0_).sum((1, 2))
            PP_.snorm[...] = s0_; PP_.wa_r = True; PP_._wa_month(t); d1_ = np.abs(PP_.snorm - s0_).sum((1, 2))
            ok_ = d0_ > 1e-9; seen_["groups"] = int(ok_.sum())
            if not np.allclose(d1_[ok_] / d0_[ok_], 1 + WPA_.WA_REACH["groups"] * RE30_[lv_[ok_], 2], rtol=2e-3):
                fails.append(f"groups: presence x {np.round(d1_[ok_] / d0_[ok_], 3)} at levels {lv_[ok_]}")
            # town (with B): a level-0 life's presence leaves the town's spheres alone; a level-1 life's leans its
            # haunts' spheres in its town, recorded as being there
            un_ = []; PP_._wa_unit = lambda n, unit, key, amt, who, t, **k_: un_.append((int(n), unit, key, k_.get("what")))
            hn_ = [n_ for n_ in range(N_) if (PP_.hnt[n_] >= 0).any() and not PP_.dead[n_]]
            if not hn_:
                fails.append("no life with a haunt to probe")
            else:
                n_ = hn_[0]; PP_.standing[:, 0] = 0; PP_.wa_held[:] = WPA_.NEVER; ss_ = W_.sph_s.copy(); PP_._wa_presence(t)
                if not np.array_equal(ss_, W_.sph_s) or any(u_[1] == "town_sphere" for u_ in un_):
                    fails.append("town: level 0 moved the town's spheres")
                PP_.standing[n_, 0] = 1; ss_ = W_.sph_s.copy(); PP_._wa_presence(t)
                js_ = {int(HS30_) for HS30_ in WPA_.HAUNT_SPH[[np.unravel_index(int(p_), W_.hp_s.shape[:3])[1] for p_ in PP_.hnt[n_] if p_ >= 0]]}
                mv_ = {(int(l_), int(j_)) for l_, j_ in zip(*np.nonzero(np.abs(W_.sph_s - ss_).sum(-1) > 1e-12))}
                tu_ = {u_[2] for u_ in un_ if u_[1] == "town_sphere" and u_[0] == n_ and u_[3] == "being there"}
                seen_["town"] = len(mv_)
                if mv_ != {(int(PP_.loc[n_]), j_) for j_ in js_} or tu_ != mv_:
                    fails.append(f"town: level 1 moved {sorted(mv_)}, recorded {sorted(tu_)}, its haunts' spheres {sorted(js_)}")
                del PP_._wa_unit
            # an act on the town's sphere (no place) from the close circle: reach at most 1 + REACH[level, 2], a
            # founding's own town nudge x reach / 3; off, the domain's 3 and 1
            tw_ = []; sl_ = W_.sph_lever
            W_.sph_lever = lambda *a_, **k_: tw_.append(k_.get("tw", 1.0)) or "none"
            PP_.hnt[0] = -1; PP_.dreach[0, DI30_["close"]] = 3.0; ma_ = np.full(5, 0.2)
            for l_ in range(4):
                PP_.standing[0, 0] = l_; PP_.wa_held[0] = WPA_.NEVER
                x_ = PP_._sph_lever(0, 0, LV30_.index("found"), ma_, 1.0, 0, DI30_["close"], t)
                seen_["lever"].append((x_["reach"], round(tw_[-1], 4)) if x_ else None)
            PP_.wa_r = False
            x_ = PP_._sph_lever(0, 0, LV30_.index("found"), ma_, 1.0, 0, DI30_["close"], t)
            seen_["lever"].append((x_["reach"], round(tw_[-1], 4)) if x_ else None)
            W_.sph_lever = sl_
            if seen_["lever"] != [(1.0, 0.3333), (2.0, 0.6667), (3.0, 1.0), (3.0, 1.0), (3.0, 1.0)]:
                fails.append(f"an act on the town's sphere: (reach, town share) {seen_['lever']}")
            break
        try:
            msg = g.send(val)
        except StopIteration:
            fails.append("no pause to probe")
            break
    bad += bool(fails)
    print(f"{'PASS' if not fails else 'FAIL'}  WA3, a standing level reaches its town (wa_reach), world on: with the world "
          f"answers off, nothing; on, run_steps lives as run() and the lives move; an act on the town's sphere from the "
          f"close circle reads (reach, a founding's town share) {seen_['lever'][:4]} at levels 0 to 3 ({seen_['lever'][4:]} "
          f"off); a level-1 life's presence leans {seen_['town']} spheres of its town (its haunts', recorded as being there), "
          f"level 0's none; group presence x (1 + .5 x REACH[level, 2]) in {seen_['groups']} lives; level 2 held 3, 6, 11 "
          f"years ago reads {seen_['linger']}"
          f"{'' if not fails else '; ' + '; '.join(fails[:4])} ({time.process_time() - t0:.0f} s)")
# 11. nothing read at a pause outside the handed-over names (an engine without STATE_MISSED reads its whole frame)
if hasattr(E, "STATE_MISSED"):
    bad += bool(E.STATE_MISSED)
    print(f"{'PASS' if not E.STATE_MISSED else 'FAIL'}  the pause state: every name read at a pause is handed over (STATE, "
          f"STATE_IF, STATE_MORE){'' if not E.STATE_MISSED else '; NOT: ' + ' '.join(sorted(E.STATE_MISSED))}")
print("engine", ENG, "engine.py", hashlib.md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12])
print("ALL PASS" if not bad else f"{bad} FAILED")
sys.exit(1 if bad else 0)
