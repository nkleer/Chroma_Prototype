"""Engine fast check for the pause points (backend plan item 2, 2026-10-08), under a minute on one core.

engine.run_steps() is engine.run() pausing six times a week for the game. On a few short runs this checks that
  1. passing every value back unchanged, run_steps() returns exactly what run() returns (every output, bit for bit);
  2. the pauses come in engine.PAUSES order every week, each with its week number (before age 3 only "week");
  3. every name in engine.STATE is in the state at every pause once a whole week has passed at age 3 or more
     (engine.STATE_IF: names there only when a switch is on, such as titles, checked when it is).

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
print("engine", ENG, "engine.py", hashlib.md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12])
print("ALL PASS" if not bad else f"{bad} FAILED")
sys.exit(1 if bad else 0)
