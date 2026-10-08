"""Fit the budget's lift per tier (earth_rules.TIER_LIFT) so the packs on together give about 1 life in 3 a big career and
about 1 in 20 a summit (Emren, pack ideas thread, relayed 08:14; earth_rules.BUDGET); within a tier, careers at the same
multiple of their real shares, summits at the square root of theirs with a floor (engine 08:25: every summit is seen, the
order holds).
One lever per tier (batch._targets, tier_z): a positive lift raises who enters a pack career or summit (entry and move
weights) and, by at most e^rung_cap, its rungs' yearly rates (the roads' written chance stays); a negative one lowers
those and the odds of every act that gives one, in the shown chance. The career budget counts lives with any pack
career or summit.
    PACKS=science,politics,stage PACK_MOMENTS='{...}' LIB=<batch dir> \\
    FIT_OUT=<json> python3 chroma-engine/tools/tier_fit.py [lives per worker] [rounds] [catalogue] [paste: 1 writes earth_rules.TIER_LIFT]"""
import sys, os, json, time
from multiprocessing import Pool
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
HERE = _engine.OUT; PROTO = _engine.ENGINE   # tier_lift.json to OUT_DIR; --write edits the engine's earth_rules.py
import engine as E, batch
if os.environ.get("LIB"):
    batch.LIB_DIR = os.environ["LIB"]
CAT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(batch.LIB_DIR, "earth_perks_titles.py")
PACKS_ = [x for x in os.environ.get("PACKS", "").split(",") if x]
PMOM_ = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None
KEY = ",".join(sorted(PACKS_))


def _load(lift):
    os.environ["TIER_LIFT"] = json.dumps(lift)
    return batch.load_batch("earth", roles=CAT, packs=PACKS_, pack_moments=PMOM_)


def one(args):
    seed, n, lift = args
    L = _load(lift); G = L["ROLES"]
    o = E.run(N=n, years=80, seed=seed, lib=L)
    ev = o["roles"]["ever"] > 0
    car = G["TIER"] == 1; sm = G["TIER"] == 2
    return dict(n=n, ever=ev.sum(0), any_c=int(ev[:, car | sm].any(1).sum()), any_s=int(ev[:, sm].any(1).sum()),
                only_c=int(ev[:, car].any(1).sum()))


def logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return float(np.log(p / (1 - p)))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    import earth_rules as R
    L = _load(dict(R.TIER_LIFT.get(KEY, {}))); G = L["ROLES"]; B = G["BUDGET"]
    sm = np.nonzero(G["TIER"] == 2)[0]; car = np.nonzero(G["TIER"] == 1)[0]
    if not len(sm) and not len(car):
        sys.exit("no pack careers or summits: TARGET_<PACK> names no tier words")
    grp = {t_: (ix, G["TARGET"][ix] / G["TARGET"][ix].sum()) for t_, ix in (("career", car), ("summit", sm)) if len(ix)}
    q = grp["summit"][1] if "summit" in grp else np.zeros(0)
    lift = dict(career=0.0, summit=0.0, split={}); lift.update(json.loads(json.dumps(R.TIER_LIFT.get(KEY, {}))))
    if os.environ.get("TIER_WARM"):   # a warm start from an earlier fit's json ({pack set: lift})
        lift.update(json.load(open(os.environ["TIER_WARM"])).get(KEY, {}))
    lift.setdefault("split", {})
    hist = dict(career=[], summit=[]); split_hist = {}
    print(f"packs {KEY}: {len(car)} careers, {len(sm)} summits; budget career {B['career']:.3f}, summit {B['summit']:.3f}", flush=True)
    for rd in range(rounds + 1):
        t0 = time.time()
        with Pool(4) as pool:
            out = pool.map(one, [(s, n, lift) for s in (11, 12, 13, 14)])
        tot = sum(o["n"] for o in out); ever = sum(o["ever"] for o in out)
        a_c = sum(o["any_c"] for o in out) / tot; a_s = sum(o["any_s"] for o in out) / tot
        print(f"round {rd}: {tot} lives, {time.time() - t0:.0f}s; lift career {lift['career']:+.3f}, summit {lift['summit']:+.3f}; "
              f"any career (summits included) {a_c:.3f} (budget {B['career']:.3f}), any summit {a_s:.3f} (budget {B['summit']:.3f}); "
              f"careers only {sum(o['only_c'] for o in out) / tot:.3f}", flush=True)
        hist["career"].append((lift["career"], logit(a_c))); hist["summit"].append((lift["summit"], logit(a_s)))
        if rd == rounds:
            break
        for t_, a_ in (("career", a_c), ("summit", a_s)):   # the tier lift: a fixed slope (the secant drifted with the
            if t_ == "career" and not len(car) or t_ == "summit" and not len(sm):   # noise and the careers' pull on summits)
                continue
            gap = logit(B[t_]) - logit(max(a_, 0.5 / tot))
            lift[t_] = round(float(np.clip(lift[t_] + np.clip(0.8 * gap / 0.6, -1.2, 1.2), -4.0, 6.0)), 4)
        for t_, (ix, qq) in grp.items():   # the split, centred on the tier lift: careers even (the same multiple of their real
            if len(ix) < 2:                # share), summits at the square root of theirs (batch._targets)
                continue
            lam = np.array([lift.get(t_, 0.0) + lift["split"].get(G["names"][i], 0.0) for i in ix])
            hs = split_hist.setdefault(t_, [])
            hs.append((ever[ix].astype(float), tot * np.exp(lam)))
            # each title's base rate, pooled over the rounds (its lives over its exposure, older rounds weigh half as much
            # each round back); half a life of prior keeps a title not yet seen finite, so it is raised, never lowered
            wts = 0.5 ** np.arange(len(hs))[::-1]
            base = (sum(w * c for w, (c, _) in zip(wts, hs)) + 0.5 * qq) / sum(w * e for w, (_, e) in zip(wts, hs))
            want = np.log(qq / base); want -= (qq * want).sum()
            d = np.array([lift["split"].get(G["names"][i], 0.0) for i in ix])
            d = d + 0.7 * (want - d); d = np.clip(d - (qq * d).sum(), -3.0, 3.0)
            lift["split"].update({G["names"][i]: round(float(x), 4) for i, x in zip(ix, d)})
    print(f"\n{'summit':34s} {'real':>8s} {'split target':>12s} {'held':>7s} {'lives':>5s} {'split lift':>10s}")
    for k_, i in enumerate(sm):
        print(f"  {G['names'][i][:32]:32s} {G['share'][i]:8.5f} {q[k_] * B['summit']:12.4f} {ever[i] / tot:7.4f} {int(ever[i]):5d} "
              f"{lift['split'].get(G['names'][i], 0.0):+10.3f}")
    print(f"\n{'career':34s} {'real':>8s} {'held':>7s} {'x real':>7s} {'split lift':>10s}")
    for i in car:
        print(f"  {G['names'][i][:32]:32s} {G['share'][i]:8.5f} {ever[i] / tot:7.4f} {ever[i] / tot / max(G['share'][i], 1e-9):7.1f} "
              f"{lift['split'].get(G['names'][i], 0.0):+10.3f}")
    show = [x for x in os.environ.get("SHOW", "").split(";") if x in G["names"]]   # SHOW='a;b': other titles' held shares
    if show:
        print(f"\n{'other':34s} {'target':>8s} {'held':>7s}")
        for nm in show:
            i = G["names"].index(nm)
            print(f"  {nm[:32]:32s} {G['TARGET'][i]:8.4f} {ever[i] / tot:7.4f}")
    res = {k_: v_ for k_, v_ in lift.items() if k_ in ("career", "summit", "split")}
    with open(os.environ.get("FIT_OUT") or os.path.join(HERE, "tier_lift.json"), "w") as f:
        json.dump({KEY: res}, f, indent=1)
    if len(sys.argv) > 4 and sys.argv[4] == "1":
        paste(KEY, res)


def paste(key, res):
    """Write earth_rules.TIER_LIFT[key] (other pack sets kept)."""
    import earth_rules as R
    tl = dict(R.TIER_LIFT); tl[key] = res
    p = os.path.join(PROTO, "earth_rules.py"); s = open(p).read()
    a = s.index("\nTIER_LIFT = {")
    b = a + len("\nTIER_LIFT = {}\n") if s.startswith("\nTIER_LIFT = {}\n", a) else s.index("\n}\n", a) + 3
    body = "".join(f"    {k_!r}: {json.dumps(v_, sort_keys=True)},\n" for k_, v_ in sorted(tl.items()))
    open(p, "w").write(s[:a] + "\nTIER_LIFT = {\n" + body + "}\n" + s[b:])
    print("TIER_LIFT written for", key)


if __name__ == "__main__":
    main()
