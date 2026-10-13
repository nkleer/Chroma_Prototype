"""Titles and perks: lifetime shares against the catalogue, and ROLE_NORM fitted so the engine's own rates match it.

python3 roles_check.py [lives per worker] [fit rounds] [catalogue path] [warm-start json]
Runs 4 workers in parallel. Items the engine grants itself (widowed, retiree...) and rules that are certain once their
condition holds (married: wife or husband) follow the engine's own life course and are reported, not fitted.
"""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
HERE = _engine.OUT   # role_norm_fit.json to OUT_DIR unless FIT_OUT names it
import engine as E
import batch as B_
from batch import load_batch
if os.environ.get("LIB"):                                   # a staged batch (LIB=<folder>)
    B_.LIB_DIR = os.environ["LIB"]

CAT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(_engine.LIBRARY, "earth_perks_titles.py")
# content packs (engine 2026-10-05 22:20): PACKS=science PACK_MOMENTS='{"science": "<compiled moments>"}'; with ONLY_PACKS=1 only
# the packs' items are fitted (the base keeps its ROLE_NORM); FIT_OUT names the json written
PACKS_ = [x for x in os.environ.get("PACKS", "").split(",") if x]
PMOM_ = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None


def _load():
    return load_batch("earth", roles=CAT, packs=PACKS_, pack_moments=PMOM_)
ENGINE_GRANTED = {"widowed", "divorced", "retiree", "out of work", "newcomer", "veteran", "left the faith"}


def one(args):
    seed, n, norm, accs = args
    L = _load()
    for i, r in enumerate(L["ROLES"]["rule"]):
        r["norm"] = norm.get(L["ROLES"]["names"][i], r["norm"])
        r["acc_move"] = accs[0].get(L["ROLES"]["names"][i], r.get("acc_move", 1.0))
        r["acc_first"] = accs[1].get(L["ROLES"]["names"][i], r.get("acc_first", 1.0))
    o = E.run(N=n, years=80, seed=seed, lib=L)
    R = o["roles"]; NT = R["NT"]
    ends = {}
    for (pn, t, kk, why, *_) in o["commits"]:
        if why not in ("start", "inherited"):
            ends[(E.KNAMES[kk], why)] = ends.get((E.KNAMES[kk], why), 0) + 1
    first_age = np.where(R["ever"], 0, np.nan)
    for (pn, t, i, what, how) in R["log"]:
        if what == "gained" and not first_age[pn, i] >= 0:
            pass
    ages = {}; hows = {}
    for (pn, t, i, what, how) in R["log"]:
        if what == "gained":
            ages.setdefault(i, []).append(t / 52)
            rt_ = "move" if how == "changed jobs" else "first" if str(how).startswith("came with the ") else "other"
            hows.setdefault(int(i), {}).setdefault(rt_, 0); hows[int(i)][rt_] += 1
    return dict(ever=R["ever"].sum(0), n=n, titles=R["ever"][:, :NT].sum(1).tolist(), perks=R["ever"][:, NT:].sum(1).tolist(),
                ends={f"{k[0]}|{k[1]}": v for k, v in ends.items()}, ages={int(k): float(np.median(v)) for k, v in ages.items()},
                hows=hows)


B_.FLOORS = os.environ.get("FLOORS") == "1"   # item 16's floors (off until the v22.3 refit)
E.DEFAULT["suit_on"] = os.environ.get("SUIT") == "1" or E.DEFAULT.get("suit_on", False)   # item 16's suitability
SEEDS = tuple(int(x) for x in os.environ.get("SEEDS", "11,12,13,14").split(","))   # other lives per session (fit_average.py)
NORM_MAX = float(os.environ.get("NORM_MAX", 60))   # the highest ROLE_NORM the fit may set (300 for item 16's floors)


def measure(n, norm, seeds=None, accs=({}, {})):
    seeds = seeds or SEEDS
    with Pool(4) as pool:
        out = pool.map(one, [(s, n, norm, accs) for s in seeds])
    tot = sum(o["n"] for o in out)
    ever = sum(o["ever"] for o in out) / tot
    titles = sum((o["titles"] for o in out), []); perks = sum((o["perks"] for o in out), [])
    ends = {}
    for o in out:
        for k, v in o["ends"].items():
            ends[k] = ends.get(k, 0) + v
    ages = {}
    for o in out:
        for k, v in o["ages"].items():
            ages.setdefault(k, []).append(v)
    hows = {}
    for o in out:
        for k, v in o["hows"].items():
            for r_, c_ in v.items():
                hows.setdefault(k, {}).setdefault(r_, 0); hows[k][r_] += c_
    measure.hows = hows
    return ever, tot, titles, perks, ends, {k: float(np.mean(v)) for k, v in ages.items()}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    L = _load(); G = L["ROLES"]
    base_ = set(load_batch("earth", roles=CAT, packs=[])["ROLES"]["ID"]) if os.environ.get("ONLY_PACKS") else set()
    names, share, NT = G["names"], np.array(G.get("TARGET", G["share"]), float), G["NT"]   # packs: TARGET_<PACK> multiples
    if os.environ.get("FIT_TARGETS"):   # fit targets above the catalogue's real share (Emren 05:18: big lives may come more
        # often than real shares; the packs thread hands them over), {name: lifetime share}; the catalogue stays real
        for nm_, v_ in json.load(open(os.environ["FIT_TARGETS"])).items():
            if nm_ not in G["ID"]:
                raise ValueError(f"FIT_TARGETS names {nm_!r}, not in the catalogue")
            share[G["ID"][nm_]] = float(v_)
    norm = {nm: G["rule"][i]["norm"] for i, nm in enumerate(names)}
    if len(sys.argv) > 4 and os.path.exists(sys.argv[4]):      # warm start from an earlier fit
        norm.update(json.load(open(sys.argv[4])))
    import earth_rules as R_
    kind = []
    for i, nm in enumerate(names):
        r = G["rule"][i]
        if nm in ENGINE_GRANTED:
            kind.append("engine")
        elif nm in getattr(R_, "ROLE_FIXED", ()):
            kind.append("fixed")                                  # kept at its written rate (earth_rules.ROLE_FIXED)
        elif "TIER" in G and G["TIER"][i] in (1, 2):
            kind.append("tier")                                   # a pack career or summit: the budget's tier lift (tier_fit.py)
        elif r["rate"] is not None and r["rate"] <= 0:
            kind.append("acts")                                   # rate 0: only through an act (a long shot that missed)
        elif nm in base_:
            kind.append("base")                                   # ONLY_PACKS: kept as fitted on the base
        elif i < NT and G["tkind"][i] < E.NK and r["rate"] is None:
            kind.append("entry")
        elif r["rate"] is not None and r["rate"] >= 1:
            kind.append("certain")
        else:
            kind.append("hazard")
    for i, nm in enumerate(names):
        if kind[i] in ("tier", "fixed"):
            norm.pop(nm, None)                                    # its norm stays as batch sets it, exp(tier lift)
    acc_mv = {nm: G["rule"][i].get("acc_move", 1.0) for i, nm in enumerate(names)}
    acc_fs = {nm: G["rule"][i].get("acc_first", 1.0) for i, nm in enumerate(names)}
    for rd in range(rounds + 1):
        t0 = time.time()
        ever, tot, titles, perks, ends, ages = measure(n, norm, accs=(acc_mv, acc_fs))
        err = [abs(ever[i] - share[i]) for i in range(len(names)) if kind[i] in ("hazard", "entry")]
        print(f"round {rd}: {tot} lives, {time.time() - t0:.0f}s; titles per life {np.mean(titles):.1f}, perks {np.mean(perks):.1f}; "
              f"mean |share error| fitted {np.mean(err):.3f}", flush=True)
        if rd == rounds:
            break
        for i, nm in enumerate(names):
            if kind[i] == "hazard":
                h_t = -np.log(1 - np.clip(share[i], 0.003, 0.97)); h_m = -np.log(1 - np.clip(ever[i], 0.5 / tot, 0.97))
                norm[nm] = float(np.clip(norm[nm] * np.clip(h_t / h_m, 0.1, 10) ** 0.85, 0.005, NORM_MAX))
        # entry titles compete within their commitment kind: only their weights relative to each other matter
        for kk in set(G["tkind"][i] for i in range(NT) if kind[i] == "entry"):
            grp = [i for i in range(NT) if kind[i] == "entry" and G["tkind"][i] == kk]
            rat = {i: np.clip(share[i] / max(ever[i], 0.5 / tot), 0.1, 10) ** 0.7 for i in grp}
            gm = 1.0 if base_ else np.exp(np.mean(np.log(list(rat.values()))))   # a pack's entries: their weight against the base's
            for i in grp:
                norm[names[i]] = float(np.clip(norm[names[i]] * rat[i] / gm, 0.01, NORM_MAX))
        # a title a route overfills even so (only candidate for many, or the fallback first job): that route gives it less
        # often (acc_move, acc_first; Library next3 §3)
        if os.environ.get("FIT_ACC", "1") == "1":
            for i in range(NT):
                if kind[i] != "entry" or ever[i] <= 1.2 * share[i]:
                    if kind[i] == "entry" and ever[i] < 0.9 * share[i]:   # under: give back acceptance first
                        acc_mv[names[i]] = min(1.0, acc_mv[names[i]] * 1.25); acc_fs[names[i]] = min(1.0, acc_fs[names[i]] * 1.25)
                    continue
                hw_ = measure.hows.get(i, {}); mv_, fs_ = hw_.get("move", 0), hw_.get("first", 0)
                k_ = (1.1 * share[i] / ever[i]) ** 0.8
                if mv_ >= fs_ and mv_ > 0:
                    acc_mv[names[i]] = float(np.clip(acc_mv[names[i]] * k_, 0.02, 1.0))
                elif fs_ > 0:
                    acc_fs[names[i]] = float(np.clip(acc_fs[names[i]] * k_, 0.02, 1.0))
    print(f"\n{'item':36s} {'kind':10s} {'how':8s} {'catalogue':>9s} {'engine':>7s} {'age':>5s} {'norm':>6s}")
    for i, nm in enumerate(names):
        k_ = G["kindname"][i]
        print(f"{nm[:36]:36s} {k_[:10]:10s} {kind[i]:8s} {share[i]:9.3f} {ever[i]:7.3f} {ages.get(i, float('nan')):5.0f} "
              f"{norm.get(nm, G['rule'][i]['norm']):6.2f}")
    print("\ntitles per life: mean %.1f, 10%% %.0f, 90%% %.0f; perks per life: mean %.1f, 10%% %.0f, 90%% %.0f" % (
        np.mean(titles), np.percentile(titles, 10), np.percentile(titles, 90), np.mean(perks), np.percentile(perks, 10), np.percentile(perks, 90)))
    print("catalogue expects: titles %.1f, perks %.1f" % (share[:NT].sum(), share[NT:].sum()))
    print("\ncommitment endings per life:", {k: round(v / tot, 2) for k, v in sorted(ends.items())})
    fit = {nm: round(norm[nm], 3) for i, nm in enumerate(names) if kind[i] in ("hazard", "entry") and abs(norm[nm] - 1) > 1e-3}
    with open(os.environ.get("FIT_OUT") or os.path.join(HERE, "role_norm_fit.json"), "w") as f:
        json.dump(fit, f, indent=0)
    accf = dict(ROLE_ACC_MOVE={k: round(v, 3) for k, v in acc_mv.items() if v < 0.999},
                ROLE_ACC_FIRST={k: round(v, 3) for k, v in acc_fs.items() if v < 0.999})
    with open((os.environ.get("FIT_OUT") or os.path.join(HERE, "role_norm_fit.json")).replace(".json", "_acc.json"), "w") as f:
        json.dump(accf, f, indent=0)
    print("acceptance by route:", json.dumps(accf))


if __name__ == "__main__":
    main()
