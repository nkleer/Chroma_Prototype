"""v25 lane C's own scenarios: R1 to R6, C1 and S1 of the life-drivers specs (v25-specs.md, scenario table), each a
short deterministic run through the engine's scenario hooks (P["scn"]: S["scn_cast"], S["scn_demand"]).

    python3 -B chroma-engine/tools/v25_scenarios.py [ENGINE_DIR] [--only R1,C1]

Each scenario sets a life up at a pause, puts demands to it as the engine's own would come (the same path, their tag
carried into the record), and reads what came back: the response odds and draws, compliance, the colour step, trust,
states, clashes and seeking. A fixed seed per scenario, so a run repeats exactly. Prints one line a scenario, PASS or
FAIL with what was read; exit code 0 when every one passes. About 4 minutes on one core. It checks the engine's
behaviour against the scenario table's "expected" and "not acceptable" columns, as far as one short life can show it;
the full pack (chroma-ideas/life-drivers-2026-10-20/scenario-pack) is What shapes a life's."""
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if args:
    os.environ["CHROMA_ENGINE"] = os.path.abspath(args[0])
ONLY = None
for i_, a_ in enumerate(sys.argv):
    if a_ == "--only" and i_ + 1 < len(sys.argv):
        ONLY = set(sys.argv[i_ + 1].split(","))
import _engine   # noqa: E402  (the engine to check, its Library and packs)
import numpy as np   # noqa: E402
import engine as E, batch   # noqa: E402
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS

L = batch.load_batch("earth", packs=list(batch.PACKS), clash=True, seek=True)
COL = "WUBRG"


def col(**k):
    v = np.array([k.get(c, 0.0) for c in COL], float)
    return (v / v.sum()).tolist()


def drive(seed, years, script, N=3, **P_):
    """run_steps with the world, react and the hooks on (and P_), calling script(kind, t, S) at every pause; returns
    the run's outputs and the script's notes."""
    P = dict(E.DEFAULT, world=True, react=True, scn=True); P.update(P_)
    g = E.run_steps(N=N, years=years, seed=seed, lib=L, P=P, log_lives=(0,))
    msg = next(g)
    while True:
        kind, t, S, val = msg
        script(kind, t, S)
        try:
            msg = g.send(val)
        except StopIteration as done:
            return done.value


def responses_with(o, tag, n=0):
    return [e for e in o["react"]["log"][n] if e.get("tag") == tag]


class Collect:
    """At the "end" pause: this week's responses of life n with a tag starting pre (their odds, drift, trust)."""
    def __init__(self, n=0, pre=""):
        self.n, self.pre, self.r = n, pre, []

    def __call__(self, kind, t, S):
        if kind == "end" and S.get("responses") is not None:
            for d_, r_ in zip(S["demands"][self.n], S["responses"][self.n]):
                if str(d_.get("tag") or "").startswith(self.pre) and self.pre:
                    self.r.append(dict(r_, t=t, tag=d_.get("tag")))


def odds(rs, k):
    return float(np.mean([r["odds"][k] for r in rs])) if rs else float("nan")


RESULTS = []


def report(name, ok, what, t0):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {what} ({time.process_time() - t0:.0f} s)", flush=True)


# R1: the same pairing, three answers: a White child, a Red-Black family; trust, control and alternatives varied
def r1():
    t0 = time.process_time(); out = {}
    for var, cast, alt in (("trusted", dict(warmth=.8, control=.3, trust=.85), None),
                           ("overreach", dict(warmth=.3, control=.9, trust=.25), col(G=1)),
                           ("secure", dict(warmth=.8, control=.2, trust=.6), None)):
        col_ = Collect(0, "R1")
        def script(kind, t, S, cast=cast, col_=col_, alt=alt):
            if kind == "week" and 12.0 <= S["age"] < 12.02:
                S["scn_cast"].append((0, "self", dict(colours=col(W=.6, U=.1, B=.1, R=.1, G=.1))))
                S["scn_cast"].append((0, "household", dict(cast, colours=col(B=.5, R=.5))))
                if alt is not None:
                    S["scn_cast"].append((0, "friend", dict(colours=alt, warmth=.8, trust=.8)))
            if kind == "week" and 12.1 <= S["age"] < 13.1 and t % 4 == 1:
                S["scn_demand"][0].append(dict(source=dict(key="household"), purpose=col(B=.5, R=.5), tag=f"R1{var}"))
            col_(kind, t, S)
        drive(71, 14, script)
        out[var] = col_.r
    acc = {v: odds(r, "accept") + odds(r, "adopt") for v, r in out.items()}
    rej = {v: odds(r, "backlash") + odds(r, "disagree") for v, r in out.items()}
    ok = all(out.values()) and acc["trusted"] > acc["overreach"] and rej["overreach"] > rej["trusted"]
    report("R1 same pairing, three answers", ok, "accept+adopt odds " + ", ".join(f"{v} {acc[v]:.2f}" for v in acc)
           + "; disagree+backlash " + ", ".join(f"{v} {rej[v]:.2f}" for v in rej)
           + f"; {sum(len(r) for r in out.values())} demands", t0)


# R2: warmth against control: supportive disagreement keeps the tie; controlling agreement lowers trust
def r2():
    t0 = time.process_time(); out = {}
    for var, cast in (("supportive", dict(warmth=.85, control=.15, trust=.7)), ("controlling", dict(warmth=.3, control=.9, trust=.4))):
        col_ = Collect(0, "R2")
        def script(kind, t, S, cast=cast, col_=col_):
            if kind == "week" and 15.0 <= S["age"] < 15.02:
                S["scn_cast"].append((0, "household", dict(cast, colours=col(W=.5, G=.5))))
            if kind == "week" and 15.1 <= S["age"] < 16.1 and t % 4 == 1:
                S["scn_demand"][0].append(dict(source=dict(key="household"), purpose=col(W=.5, G=.5), tag=f"R2{var}"))
            col_(kind, t, S)
        drive(72, 17, script)
        out[var] = col_.r
    tr = {v: float(np.mean([r["learn"]["trust"] for r in rs])) if rs else float("nan") for v, rs in out.items()}
    cv = {v: float(np.mean([r["convinced"] for r in rs])) if rs else float("nan") for v, rs in out.items()}
    ok = all(out.values()) and tr["supportive"] > tr["controlling"]
    report("R2 warmth against control", ok, f"trust change a demand: supportive {tr['supportive']:+.3f}, controlling "
           f"{tr['controlling']:+.3f}; convinced: supportive {cv['supportive']:.2f}, controlling {cv['controlling']:.2f}", t0)


# R3: constrained compliance: a dependent child with no exit complies outwardly, with no colour step
def r3():
    t0 = time.process_time(); col_ = Collect(0, "R3")
    def script(kind, t, S):
        if kind == "week" and 9.0 <= S["age"] < 9.02:
            S["scn_cast"].append((0, "self", dict(colours=col(W=.1, U=.6, B=.1, R=.1, G=.1))))
            S["scn_cast"].append((0, "household", dict(colours=col(R=.6, G=.4), warmth=.3, control=.95, trust=.3)))
        if kind == "week" and 9.1 <= S["age"] < 10.1 and t % 4 == 1:
            S["scn_demand"][0].append(dict(source=dict(key="household"), purpose=col(R=.6, G=.4), power=.9, control=.95,
                                           exit=False, tag="R3"))
        col_(kind, t, S)
    drive(73, 11, script)
    rs = col_.r; con = [r for r in rs if r["constrained"]]
    ok = bool(rs) and all(r["comply"] for r in con) and all(r["drift"] is None for r in con) \
        and not any(r["response"] == "withdraw" for r in rs)
    report("R3 constrained compliance", ok, f"{len(con)} of {len(rs)} answers constrained, each complying outwardly "
           f"with no colour step; no withdrawal before an exit", t0)


# R4: repair: a partner's dissatisfaction; talk and renegotiation restore trust, staying records history
def r4():
    t0 = time.process_time(); col_ = Collect(0, "R4")
    def script(kind, t, S):
        if kind == "week" and 30.0 <= S["age"] < 30.02:
            S["scn_cast"].append((0, "partner", dict(trust=.3, warmth=.4)))
        if kind == "week" and 30.1 <= S["age"] < 31.1 and t % 8 == 1:
            S["scn_demand"][0].append(dict(source=dict(key="partner"), tag="R4", response="negotiate"))
        col_(kind, t, S)
    o = drive(74, 34, script, seek=True)
    rs = col_.r; ans = [a for a in (o["react"]["seek"] or {}).get("answered", []) if a["kind"] == "repair"]
    good = [r for r in rs if r["response"] == "negotiate" and r["learn"]["works"]]
    ok = bool(rs) and all(r["drift"] is None or r["response"] != "negotiate" or r["learn"]["works"] for r in rs) \
        and all(r["learn"]["trust"] > 0 for r in good)
    report("R4 repair", ok, f"{len(rs)} talks with the partner ({len(good)} won terms, each raising trust); "
           f"{len(ans)} repair moments answered: " + ", ".join(f"{a.get('act')} {a.get('trust', 0):+.2f}" for a in ans[:4])
           + "; no colour step forced by failed talks", t0)


# R5: stability and drift: a contented adult in a fitting place stays settled; a moved one drifts by what they meet
def r5():
    t0 = time.process_time(); out = {}
    for var, place in (("settled", col(W=.6, G=.4)), ("moved", col(U=.5, B=.5))):
        w0 = {}
        def script(kind, t, S, place=place, w0=w0):
            if kind == "week" and 30.0 <= S["age"] < 30.02:
                S["scn_cast"].append((0, "self", dict(colours=col(W=.6, G=.4))))
                for g_ in ("household", "work", "congregation", "neighbours"):
                    S["scn_cast"].append((0, g_, dict(colours=place, warmth=.7, control=.4)))
            if kind == "end" and 30.0 <= S["age"] < 30.02 and "w" not in w0:
                w0["w"] = np.array(S["w"][0], float)
            if kind == "end" and 33.0 <= S["age"] < 33.02:
                w0["w1"] = np.array(S["w"][0], float)
        drive(75, 34, script)
        out[var] = 0.5 * float(np.abs(w0.get("w1", np.nan) - w0.get("w", np.nan)).sum())
    ok = out["settled"] < out["moved"]
    report("R5 stability and drift", ok, f"colour moved in three years: settled {out['settled']:.3f}, moved "
           f"{out['moved']:.3f}", t0)


# R6: Earth nature: a drought on a farm; stakes, responses and consequences, never nature approving a colour
def r6():
    t0 = time.process_time(); col_ = Collect(0, "R6")
    def script(kind, t, S):
        if kind == "week" and 35.0 <= S["age"] < 37.0 and t % 13 == 1:
            S["scn_demand"][0].append(dict(source=dict(key="nature"), stakes=0.5, control=.8, tag="R6"))
        col_(kind, t, S)
    o = drive(76, 38, script, clash=True)
    rs = col_.r
    ok = bool(rs) and all(r["drift"] is None or r["response"] == "withdraw" for r in rs)
    report("R6 Earth nature", ok, f"{len(rs)} answers to the land: " + ", ".join(sorted({r['act'] for r in rs}))
           + "; no colour step from nature (a move away aside)", t0)


# C1: one dispute: a family demand the congregation backs; one merged question, not repeated while nothing changes
def c1():
    t0 = time.process_time(); st = {}
    def script(kind, t, S):
        if kind == "week" and S["age"] >= 15.0 and "t0" not in st:
            ds = S["disputes"]   # a life the ceilings leave room in: no clash in two years, fewer than 3 in ten
            free = [n for n in range(len(ds)) if not any(t - d["since"] < 110 for d in ds[n])
                    and sum(t - d["since"] < 520 for d in ds[n]) < 3]
            if free:
                n = st["n"] = free[0]; st["t0"] = t
                for k_ in ("household", "congregation"):
                    S["scn_demand"][n].append(dict(source=dict(key=k_), purpose=col(B=.6, R=.4), stakes=0.9, power=.8,
                                                   control=.7, legit=.4, tag=f"C1{k_}"))
        if "t0" in st and kind == "week" and st["t0"] < t <= st["t0"] + 8 * 13 and (t - st["t0"]) % 13 == 0:
            S["scn_demand"][st["n"]].append(dict(source=dict(key="household"), purpose=col(B=.6, R=.4), stakes=0.9,
                                                 power=.8, control=.7, legit=.4, tag="C1again"))
        if "t0" in st and kind == "end" and S["clash"][st["n"]] is not None:
            st.setdefault("clash", []).append((t, S["clash"][st["n"]]["id"], list(S["clash"][st["n"]]["holders"])))
    o = drive(77, 18, script, N=6, clash=True)
    cl = st.get("clash", []); first = [c for c in cl if c[0] <= st.get("t0", -99) + 8]
    again = [c for c in cl if c[0] > st.get("t0", 0) + 8 and first and c[1] == first[0][1]]
    ok = "t0" in st and len({c[1] for c in first}) == 1 and not again
    report("C1 one dispute", ok, f"life {st.get('n')}: {len(first)} clash record(s) in the 8 weeks after the backed "
           f"demands, holders {first[0][2] if first else None}; asked again {len(again)} times while unchanged", t0)


# S1: no trap: a bored Blue adult near a Red scene; curiosity draws, entry can fail, seeking never gives a colour
def s1():
    t0 = time.process_time(); st = {}
    def script(kind, t, S):
        if kind == "week" and 30.0 <= S["age"] < 30.02:
            S["scn_cast"].append((0, "self", dict(colours=col(W=.1, U=.6, B=.1, R=.1, G=.1))))
        if kind == "week" and 30.0 <= S["age"] < 31.0 and t % 8 == 0:
            S["scn_demand"][0].append(dict(source=dict(key="scene"), purpose=col(R=.7, G=.3), channel="encounter",
                                           power=0, control=0, tag="S1"))
        if kind == "end" and S.get("seek") is not None and (29.9 <= S["age"] < 29.92 or 31.5 <= S["age"] < 31.52):
            st["a0" if S["age"] < 30 else "a1"] = np.array(S["seek"][0]["attraction"], float)
    o = drive(78, 34, script, N=3, seek=True)
    sk = o["react"]["seek"]; tried = [x for tr in sk["tried"] for x in tr]
    seek_steps = [e for lg in o["react"]["log"] for e in lg if e.get("seek") is not None and (e.get("layers") or {}).get("drift")]
    red = np.array(col(R=.7, G=.3))
    c0 = float(st["a0"] @ red / np.linalg.norm(st["a0"]) / np.linalg.norm(red)) if "a0" in st else np.nan
    c1_ = float(st["a1"] @ red / np.linalg.norm(st["a1"]) / np.linalg.norm(red)) if "a1" in st else np.nan
    ok = not seek_steps and all(not x["admitted"] or x["place"] >= 0 for x in tried)
    report("S1 no trap", ok, f"attraction toward the scene {c0:.2f} -> {c1_:.2f}; {len(tried)} tries, "
           f"{sum(x['admitted'] for x in tried)} admitted, {sum(not x['admitted'] for x in tried)} not; no colour step "
           f"from seeking", t0)


for nm, fn in (("R1", r1), ("R2", r2), ("R3", r3), ("R4", r4), ("R5", r5), ("R6", r6), ("C1", c1), ("S1", s1)):
    if ONLY is None or nm in ONLY:
        fn()
print("ALL PASS" if all(RESULTS) else f"{sum(not x for x in RESULTS)} FAILED")
sys.exit(0 if all(RESULTS) else 1)
