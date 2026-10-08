"""The Library's chance per option (point 8): measure who meets each moment (skill, world push and perks, per color) for
earth_rules.CHANCE_REF, and check that an option's true odds for them come to its chance.
    python3 chroma-engine/tools/chance_check.py measure|refine|check [lives per worker] [lib dir] [catalogue]
measure writes chance_ref.json (to OUT_DIR) (paste into earth_rules.CHANCE_REF); refine moves each moment's reference by
the gap between its options' odds and chances (Jensen and the rest) and writes the same file; check prints how far the odds sit from
the chances (per option, weighted by how often each moment comes)."""
import os, sys, json
import numpy as np
from multiprocessing import Pool
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
HERE = _engine.OUT   # chance_ref.json to OUT_DIR
import engine as E, batch
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"; NW = int(sys.argv[2]) if len(sys.argv) > 2 else 100
LIB = sys.argv[3] if len(sys.argv) > 3 else os.path.join(_engine.LIBRARY, "staging")
CAT = sys.argv[4] if len(sys.argv) > 4 else os.path.join(_engine.LIBRARY, "earth_perks_titles.py")


PACKS_ = [x for x in os.environ.get("PACKS", "").split(",") if x]          # content packs (engine 2026-10-06): PACKS=science,politics
PMOM_ = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None             # PACK_MOMENTS='{"science": "<compiled moments>"}'


def one(seed):
    batch.LIB_DIR = LIB
    L = batch.load_batch("earth", roles=CAT, packs=PACKS_, pack_moments=PMOM_)
    o = E.run(N=NW, years=85, seed=seed, lib=L)
    cr = o["chance_ref"]
    return cr["ref"] * cr["n"][:, None], cr["n"], cr["p_option"] * cr["n_option"], cr["n_option"], cr["earn"] * cr["earn_n"], cr["earn_n"]


if __name__ == "__main__":
    with Pool(4) as pool:
        res = pool.map(one, [101, 102, 103, 104])
    batch.LIB_DIR = LIB
    L = batch.load_batch("earth", roles=CAT, packs=PACKS_, pack_moments=PMOM_)
    n = sum(r[1] for r in res); ref = sum(r[0] for r in res) / np.maximum(n, 1)[:, None]
    no = sum(r[3] for r in res); po = sum(r[2] for r in res) / np.maximum(no, 1)
    names = L["names"]
    if MODE == "measure":
        en = sum(r[5] for r in res); er = sum(r[4] for r in res) / np.maximum(en, 1)
        MIN_ = int(os.environ.get("MIN_MET", "20"))
        out = {names[i]: [round(float(x), 3) for x in ref[i]] + ([round(float(er[i]), 3)] if en[i] >= 5 else [])
               for i in range(L["S"]) if n[i] >= MIN_}
        json.dump(out, open(os.path.join(HERE, "chance_ref.json"), "w"), indent=0)
        print(f"{len(out)} of {L['S']} moments met 20 times or more; mean ref {np.mean([v[:5] for v in out.values()], 0).round(3)}")
        ages = {}
        for i in range(L["S"]):
            if n[i] >= 20:
                ages.setdefault(str(L["src"][i].get("tier")), []).append(ref[i].mean())
        print("ref (mean over colors) by tier:", {k: round(float(np.mean(v)), 3) for k, v in ages.items()})
    if MODE == "refine":   # move each moment's reference by how far its options' odds sit from their chances (logit units)
        import earth_rules as R_
        dflt = np.mean([np.asarray(v, float)[:5] for v in R_.CHANCE_REF.values()], 0)
        C_ = L["CHANCE"]; out = {}
        for i in range(L["S"]):
            used_all = np.asarray(R_.CHANCE_REF.get(names[i], dflt), float); used = used_all[:5]
            tail_ = [round(float(used_all[5]), 3)] if len(used_all) > 5 else []
            ok_ = ~np.isnan(C_[i]) & (no[i] >= 10)
            if n[i] >= 20 and ok_.sum() >= 3:   # per color: err_k = m_k . delta, least squares pulled toward the mean gap
                pc = np.clip(po[i][ok_], 0.005, 0.995); cc = C_[i][ok_]
                err = (np.log(pc / (1 - pc)) - np.log(cc / (1 - cc))) / E.DEFAULT["gain"]
                Mk = L["M"][i][ok_]; lam = 0.3; e0 = err.mean()
                A = np.vstack([Mk, np.sqrt(lam) * np.eye(E.C)]); b = np.concatenate([err, np.sqrt(lam) * np.full(E.C, e0)])
                delta = np.linalg.lstsq(A, b, rcond=None)[0]
                out[names[i]] = [round(float(x), 3) for x in used + delta] + tail_
            elif names[i] in R_.CHANCE_REF:
                out[names[i]] = list(R_.CHANCE_REF[names[i]])
        json.dump(out, open(os.path.join(HERE, "chance_ref.json"), "w"), indent=0)
        print(f"refined {len(out)} moments")
    C = L["CHANCE"]; ok = ~np.isnan(C) & (no >= 20)
    wt = no[ok]
    err = (po - C)[ok]
    print(f"options checked {ok.sum()}: mean chance {np.average(C[ok], weights=wt):.3f}, mean true odds {np.average(po[ok], weights=wt):.3f}, "
          f"mean |odds - chance| {np.average(np.abs(err), weights=wt):.3f}, r {np.corrcoef(C[ok], po[ok])[0, 1]:.3f}")
    for lo, hi in ((0, .3), (.3, .6), (.6, .8), (.8, 1.0)):
        sel = (C[ok] >= lo) & (C[ok] < hi)
        if sel.any():
            print(f"  chance {lo:.1f}-{hi:.1f}: {sel.sum():4d} options, true odds {np.average(po[ok][sel], weights=wt[sel]):.3f}")
    worst = np.argsort(-np.abs(err))[:8]
    idx = np.argwhere(ok)
    for j in worst:
        si, ki = idx[j]
        print(f"  {names[si]!r} option {ki}: chance {C[si, ki]:.2f}, true odds {po[si, ki]:.2f} (met {int(n[si])})")
