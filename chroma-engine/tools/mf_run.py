"""MF, matched families (Release's run for RE2, records/v25/checks.md): a child whose colours oppose its family's, the
same seed and the same lives with the family warm or controlling; only the family's warmth and control differ.

    python3 -B chroma-engine/tools/mf_run.py <tree> <seed> <N> <warm|controlling> <out.json>
        [--hold month|once] [--child own|cast] [--setup-age 12] [--years 25]

<tree> is a repository checkout (its chroma-engine/v22-speedpass, chroma-library and chroma-packs are run). N lives,
to age 25, with the outer world, react, clash and seek on and the scenario hooks (P["scn"]) as v25_scenarios.py drives
them; nothing else in the engine is changed. Both arms run the same seed and N, so life n is the same life in both up
to the set-up week (mf_judge.py checks that each life got the same family in both).

The set-up, the same in both arms (fixed before any reading):
  - At the first week from age 12 (--setup-age) each life gets a family that opposes its colours. --child own (the
    default): the child keeps its own colours; its leading colour then sets the family, the allied pair of the two
    colours that are its enemies (a White-led child gets a Black-Red family, Blue Red-Green, Black Green-White, Red
    White-Blue, Green Blue-Black), .5 each. --child cast: life n gets the pair n % 5 (WU, UB, BR, RG, GW) and the
    child is cast at .6 in the colour that is the enemy of both and .1 in each other (v25_scenarios.py's R1 set-up). A
    cast child relaxes back toward its own colours within weeks (the engine's wants, habits and core pull it back:
    a .6 cast is near .25 by 12.1), so "own" is the default.
  - The caller's cast (S["scn_cast"]) sets the household: its ways and its members' colours (the family's mix),
    warmth and control by the arm: warm (warmth .85, control .15) or controlling (warmth .30, control .90), the two
    households of v25_scenarios.py's R2. Trust is the world's own (the same in both arms up to the set-up).
  - --hold month (the default): each month (t % 4 == 0) while the child still lives in that household (not
    own_home), the household is cast again with the same colours, warmth and control, so the family stays what the arm
    says; --hold once casts it at the set-up only.
  - The family's demands are the household's own (the engine's react, at its own rate); the caller adds none.

Per life the output has: the family's mix and pair, the child's mix at the set-up, its colours (w) at 12, 13, 19 and
the end (25), its L1 distance to the family's mix at 13 and 19, the colours the family's demand opposed (each colour
the family asks nothing of that is the enemy of a colour it asks: for a pair, the other three) and the one opposed by
both of its colours, their rise 13 to 19, the backlash flags (the opposed colours' summed share up .02 or more; and the
opposite colour's alone), the responses to the family's demands (the household's, while the child lives there) and to
all others by kind and age band, the constrained ones and those that were a town event's ask put through the household, the
mean purpose of the household's own demands the child rejected (disagreed with, turned away from or withdrew from)
from 13 to 19, and the age they left home. The header has the
arm's settings, the commit it ran on and the time it took. mf_judge.py reads two sets of these files and gives RE2.
"""
import json
import os
import subprocess
import sys
import time

opts = {}
for i_, a_ in enumerate(sys.argv):
    if a_.startswith("--") and i_ + 1 < len(sys.argv):
        opts[a_[2:]] = sys.argv[i_ + 1]
argv = [a for i_, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and not sys.argv[i_ - 1].startswith("--")]
if len(argv) != 5 or argv[3] not in ("warm", "controlling"):
    sys.exit(__doc__)
TREE, SEED, N, ARM, OUT = os.path.abspath(argv[0]), int(argv[1]), int(argv[2]), argv[3], os.path.abspath(argv[4])
HOLD = opts.get("hold", "month")
CHILD = opts.get("child", "own")
SETUP = float(opts.get("setup-age", 12.0))
YEARS = int(opts.get("years", 25))
assert HOLD in ("month", "once") and CHILD in ("own", "cast")
os.environ["CHROMA_ROOT"] = TREE
os.environ["CHROMA_ENGINE"] = os.path.join(TREE, "chroma-engine", "v22-speedpass")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _engine   # noqa: E402  (the tree's engine, Library and packs)
import numpy as np   # noqa: E402
import engine as E, batch   # noqa: E402
assert os.path.samefile(_engine.ENGINE, os.environ["CHROMA_ENGINE"]), _engine.ENGINE
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS

COL = "WUBRG"
ARMS = dict(warm=dict(warmth=0.85, control=0.15), controlling=dict(warmth=0.30, control=0.90))
PAIRS = ("WU", "UB", "BR", "RG", "GW")
REJECT = ("disagree", "backlash", "withdraw")
BANDS = (("12_13", 0, 13), ("13_19", 13, 19), ("19_25", 19, 99))


def mix(**k):
    v = np.array([k.get(c, 0.0) for c in COL], float)
    return v / v.sum()


def family_of(pair):
    """The family's mix for an allied pair, the colours its demand opposes, and the one opposed by both."""
    fam = mix(**{pair[0]: .5, pair[1]: .5})
    opp = np.nonzero((E.ENEMY @ fam > 0) & (fam == 0))[0]           # enemies of a colour the family asks, asked nothing
    both = int(np.argmax(E.ENEMY @ fam))                              # the enemy of both its colours
    return fam, [COL[i] for i in opp], COL[both]


def pair_against(lead):
    """The allied pair of the two enemies of colour index lead."""
    en = {COL[i] for i in np.nonzero(E.ENEMY[lead] > 0)[0]}
    return next(p for p in PAIRS if set(p) == en)


def git(*a):
    try:
        return subprocess.run(["git", "-C", TREE] + list(a), capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""


def band(age):
    for nm, a0, a1 in BANDS:
        if a0 <= age < a1:
            return nm
    return None


def main():
    t0 = time.time()
    L = batch.load_batch("earth", packs=list(batch.PACKS), clash=True, seek=True)
    t_load = time.time() - t0
    P = dict(E.DEFAULT, world=True, react=True, clash=True, seek=True, scn=True)
    cast = ARMS[ARM]
    lives = [dict(n=n, pair=None, family=None, opposed=None, opposite=None, child_pre=None, child0=None,
                  has_family=None, hh=-1, w={}, left_home=None, dead_at=None,
                  resp={b[0]: dict(family={}, other={}) for b in BANDS}, constrained={b[0]: 0 for b in BANDS},
                  events={b[0]: 0 for b in BANDS}, rej_purpose=np.zeros(5), n_rej=0, casts=0) for n in range(N)]
    st = dict(setup=False)
    marks = (("13", 13.0), ("19", 19.0))
    src_of = [dict() for _ in range(N)]   # demand id -> source key, per life (a clash answered weeks later)

    def script(kind, t, S):
        age = float(S["age"])
        if kind == "week" and age >= SETUP:
            WL = S["WL"]; PP = WL.PP
            if not st["setup"]:
                st["setup"] = True
                for n, lf in enumerate(lives):
                    w_ = np.asarray(S["w"][n], float)
                    lf["child_pre"] = [round(float(x), 5) for x in w_]
                    pair = PAIRS[n % 5] if CHILD == "cast" else pair_against(int(np.argmax(w_)))
                    fam, opp, both = family_of(pair)
                    lf.update(pair=pair, family=fam.round(4).tolist(), opposed=opp, opposite=both)
                    if CHILD == "cast":
                        ch_ = np.full(5, .1); ch_[COL.index(both)] = .6
                        S["scn_cast"].append((n, "self", dict(colours=ch_.tolist())))
                    S["scn_cast"].append((n, "household", dict(cast, colours=lf["family"])))
                    lf["has_family"] = bool(int(PP.hhj[n]) >= 0 and not PP.own_home[n])
                    lf["hh"] = int(PP.hhj[n]); lf["casts"] = 1
            elif HOLD == "month" and t % 4 == 0:
                for n, lf in enumerate(lives):
                    if lf["has_family"] and not PP.own_home[n] and int(PP.hhj[n]) == lf["hh"] and lf["dead_at"] is None:
                        S["scn_cast"].append((n, "household", dict(cast, colours=lf["family"])))
                        lf["casts"] += 1
        if kind != "end" or not st["setup"]:
            return
        PP = S["WL"].PP; dead = S["dead"]; w = S["w"]
        b = band(age)
        for n, lf in enumerate(lives):
            if lf["dead_at"] is None and dead[n]:
                lf["dead_at"] = round(age, 2)
            if lf["left_home"] is None and PP.own_home[n]:
                lf["left_home"] = round(age, 2)
            if "12" not in lf["w"]:   # the set-up week's end: the child's mix (after a cast)
                lf["w"]["12"] = lf["child0"] = [round(float(x), 5) for x in w[n]]
            for nm, a_ in marks:
                if nm not in lf["w"] and age >= a_ and lf["dead_at"] is None:
                    lf["w"][nm] = [round(float(x), 5) for x in w[n]]
            if lf["dead_at"] is None:
                lf["w"]["end"] = [round(float(x), 5) for x in w[n]]; lf["age_end"] = round(age, 2)
            ds, rs = S["demands"][n], S["responses"][n]
            if not rs:
                continue
            for d_ in ds:
                src_of[n][d_["id"]] = ((d_.get("source") or {}).get("key"), d_.get("purpose"), d_.get("by"))
            home = lf["has_family"] and lf["left_home"] is None
            for r_ in rs:
                key, pur, by = src_of[n].get(r_["demand"], (None, None, None))
                g = "family" if key == "household" and home else "other"
                c_ = lf["resp"][b][g]; c_[r_["response"]] = c_.get(r_["response"], 0) + 1
                if g == "family":
                    lf["constrained"][b] += int(bool(r_.get("constrained")))
                    lf["events"][b] += int(by == "event")
                    if r_["response"] in REJECT and pur is not None and b == "13_19" and by != "event":
                        lf["rej_purpose"] += np.asarray(pur, float); lf["n_rej"] += 1

    g = E.run_steps(N=N, years=YEARS, seed=SEED, lib=L, P=P)
    msg = next(g)
    while True:
        kind, t, S, val = msg
        script(kind, t, S)
        try:
            msg = g.send(val)
        except StopIteration:
            break
    t_run = time.time() - t0 - t_load
    for lf in lives:
        fam = np.asarray(lf["family"]); W = lf["w"]
        lf["rej_purpose"] = (lf["rej_purpose"] / lf["n_rej"]).round(4).tolist() if lf["n_rej"] else None
        if "13" in W and "19" in W:
            w13, w19 = np.asarray(W["13"]), np.asarray(W["19"])
            oi = [COL.index(c) for c in lf["opposed"]]; bi = COL.index(lf["opposite"])
            lf["l1_19"] = round(float(np.abs(w19 - fam).sum()), 5)
            lf["l1_13"] = round(float(np.abs(w13 - fam).sum()), 5)
            lf["rise"] = {c: round(float(w19[i] - w13[i]), 5) for i, c in enumerate(COL)}
            lf["rise_opposed"] = round(float(w19[oi].sum() - w13[oi].sum()), 5)
            lf["rise_opposite"] = round(float(w19[bi] - w13[bi]), 5)
            lf["backlash"] = bool(lf["rise_opposed"] >= 0.02)
            lf["backlash_opposite"] = bool(lf["rise_opposite"] >= 0.02)
        else:
            lf["l1_19"] = lf["rise"] = lf["rise_opposed"] = lf["rise_opposite"] = lf["backlash"] = None
    out = dict(tool="mf_run", format=1, tree=TREE, sha=git("rev-parse", "HEAD"),
               dirty=bool(git("status", "--porcelain", "--untracked-files=no", "--", "chroma-engine/v22-speedpass", "chroma-library", "chroma-packs")),
               engine=_engine.ENGINE, library=_engine.LIBRARY, packs=_engine.PACKS, seed=SEED, N=N, arm=ARM,
               settings=dict(arm=ARM, family=cast, hold=HOLD, child=CHILD, setup_age=SETUP, years=YEARS, pairs=PAIRS,
                             switches=dict(world=True, react=True, clash=True, seek=True, scn=True),
                             backlash="opposed colours' summed share up .02 or more from 13 to 19"),
               time=dict(load_s=round(t_load, 1), run_s=round(t_run, 1), per_100_lives_s=round(t_run * 100 / N, 1)),
               lives=lives)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    ok = [lf for lf in lives if lf["l1_19"] is not None and lf["has_family"]]
    print(f"mf_run {ARM} seed {SEED}: {N} lives ({len(ok)} with a family at 12, alive at 19), "
          f"L1 at 19 {np.mean([lf['l1_19'] for lf in ok]) if ok else float('nan'):.3f}, backlash "
          f"{np.mean([lf['backlash'] for lf in ok]) if ok else float('nan'):.3f}; load {t_load:.0f} s, run {t_run:.0f} s "
          f"-> {OUT}", flush=True)


main()
