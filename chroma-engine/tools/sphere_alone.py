"""The spheres of society alone for 300 years (item 15, phase 1c): are the towns' face mixes colour-even, does every face
live everywhere, and do towns differ? chroma-ideas/spheres-implementation.md section 6, "What must be measured".

Runs 8 worlds (seeds 1 to 8, pace 1) whose society starts with even values (preset .2 each) with the switch `sph_town`
on, for 300 years after the 80-year burn-in, reads each town's nine spheres every ten years and prints each check with
its value, its target and ok or MISS, then a determinism check (the first world run twice). The spheres follow a
town's culture by design (the K term), and the world's culture drifts on its own (LW1, the Outer world's), so the
colour-even row measures the spheres' own lean: each colour's mean face share minus its mean share in the towns'
culture. --preset "typical rich" runs the first society instead (information: its culture leans).

    OMP_NUM_THREADS=1 python3 -B chroma-engine/tools/sphere_alone.py [--worlds 8] [--years 300] [--seed0 1]
        [--preset even|"typical rich"] [--par JSON] [--json FILE]

--json writes the numbers to FILE (under OUT_DIR when relative; never into the repository).
"""
import sys, os, json, time, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
from world import World
from world_keys import SPHERES

C, WK, COLS = 5, 52, "WUBRG"
ROWS = []


def row(name, value, target, ok):
    ROWS.append(dict(name=name, value=value, target=target, flag="ok" if ok else "MISS"))
    print(f"  {name:<58s} {value!s:<26s} {target:<30s} {'ok' if ok else 'MISS'}", flush=True)


def run_world(seed, years, par=None, preset="even"):
    """Face shares (decades x towns x 9 x 5, in the canonical colour frame), sizes (decades x towns x 9) and the towns'
    culture (decades x towns x 5)."""
    cfg = dict(params=dict(sph_town=True, sph_par=par))
    if preset == "even":
        cfg["preset"] = [0.2] * C
    W = World(seed, cfg=cfg)
    W.burn_in(80)
    inv = np.argsort(W.perm)                    # the world's colour frame back to W U B R G
    S, Z, K = [], [], []
    for _ in range(years // 10):
        W.tick(W.t + 10 * WK)
        S.append(W.sph_s[..., inv].copy()); Z.append(W.sph_Z.copy()); K.append(np.asarray(W.loc_mix, float)[:, inv].copy())
    return np.array(S), np.array(Z), np.array(K)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", type=int, default=8)
    ap.add_argument("--preset", default="even", help='even (the check) or "typical rich" (information)'); ap.add_argument("--years", type=int, default=300)
    ap.add_argument("--seed0", type=int, default=1); ap.add_argument("--json", default=None)
    ap.add_argument("--par", default=None, help="sphere parameters over sphere_data.PARAMS, as JSON (tuning)")
    a = ap.parse_args()
    print(f"engine {_engine.ENGINE}")
    print(f"{a.worlds} worlds, seeds {a.seed0} to {a.seed0 + a.worlds - 1}, {a.years} years after an 80-year burn-in, "
          f"spheres read every ten years\n")
    t0 = time.time()
    par = json.loads(a.par) if a.par else None
    if par:
        print(f"parameters over the design values: {par}\n")
    print(f"society: {a.preset}\n")
    runs = [run_world(s, a.years, par, a.preset) for s in range(a.seed0, a.seed0 + a.worlds)]
    secs = time.time() - t0
    S = np.concatenate([r[0].reshape(-1, 9, C) for r in runs])          # town-decades x 9 x 5
    Z = np.concatenate([r[1].reshape(-1, 9) for r in runs])
    K = np.concatenate([r[2].reshape(-1, C) for r in runs])               # town-decades x 5
    mean_c = S.mean((0, 1)); cult_c = K.mean(0); own = mean_c - cult_c
    zmean_c = (Z[..., None] * S).sum((0, 1)) / Z.sum()
    print("colour-even")
    row("the spheres' own lean (face share minus the culture's)", " ".join(f"{c}{v:+.3f}" for c, v in zip(COLS, own)),
        "each within .01", bool(np.abs(own).max() <= 0.01))
    print(f"  mean face share {' '.join(f'{c}{v:.3f}' for c, v in zip(COLS, mean_c))}; the towns' culture "
          f"{' '.join(f'{c}{v:.3f}' for c, v in zip(COLS, cult_c))}; by hours {' '.join(f'{c}{v:.3f}' for c, v in zip(COLS, zmean_c))} (information)")
    print("every face everywhere; towns differ")
    lo = S.min()
    row("lowest face share anywhere", f"{lo:.3f}", "at least .02 (the floor; .0195 rounds)", bool(lo >= 0.0195))
    hi = S.max(0)                                                        # 9 x 5: each face's highest
    row("faces that reach .10 somewhere", f"{int((hi >= 0.10).sum())} of 45", "45 of 45", bool((hi >= 0.10).all()))
    lead = np.zeros((9, C))
    am = S.argmax(2)
    for j in range(9):
        lead[j] = np.bincount(am[:, j], minlength=C) / len(am)
    j_, c_ = np.unravel_index(lead.argmax(), lead.shape)
    row("most often leading face (share of town-decades)", f"{SPHERES[j_]}.{COLS[c_]} {lead.max():.2f}", "under .60",
        bool(lead.max() < 0.60))
    lw = max(max(np.bincount(r[0].reshape(-1, 9, C)[:, j].argmax(1), minlength=C).max() / len(r[0].reshape(-1, 9, C))
                  for j in range(9)) for r in runs)
    print(f"  most often leading face within one world: {lw:.2f} of its town-decades (information: towns in one world "
          f"share its culture)")
    spread = S.std(0).mean()
    print(f"  mean spread of a face share across towns and decades: {spread:.3f} (information)")
    print("  each sphere's mean mix:")
    for j in range(9):
        print(f"    {SPHERES[j]:<7s} " + " ".join(f"{c}{v:.2f}" for c, v in zip(COLS, S[:, j].mean(0)))
              + f"   hours {Z[:, j].mean():.3f}   leads " + " ".join(f"{c}{v:.2f}" for c, v in zip(COLS, lead[j])))
    print("determinism")
    S2, Z2, _ = run_world(a.seed0, a.years, par, a.preset)
    same = np.array_equal(S2, runs[0][0]) and np.array_equal(Z2, runs[0][1])
    row("the first world run twice", "identical" if same else "differs", "identical", same)
    print(f"\n{a.worlds} x {a.years} years in {secs:.0f} s")
    print("ALL ok" if all(r["flag"] == "ok" for r in ROWS) else "MISS: " + ", ".join(r["name"] for r in ROWS if r["flag"] != "ok"))
    if a.json:
        p = a.json if os.path.isabs(a.json) else os.path.join(os.environ.get("OUT_DIR", "."), a.json)
        json.dump(dict(rows=ROWS, mean=mean_c.tolist(), lead=lead.tolist(), secs=secs), open(p, "w"), indent=1)


if __name__ == "__main__":
    main()
