"""Steered lives (Emren 10-10: "choices must impact achieving perks: blue-dominated choices must increase chances to
become researcher, red-dominated ones to become artist"): what a life that keeps choosing one color reaches, and what it
costs, against unsteered lives of the same world.
    python3 -B chroma-engine/tools/choice_check.py run <lives per worker> <push> <out.npz> [groups]   one run, 4 workers
    python3 -B chroma-engine/tools/choice_check.py sum <npz> [npz...]                                  the tables
groups: comma-separated, "-" unsteered, else a color letter; default "-,W,U,B,R,G". Person n is in group n % len(groups).
push: added each week to a steered person's want (y, log-ratio) for the group's color, as a player who keeps choosing
it; .01 brings that want to about .45 to .6 by forty. Packs: PACKS, default science,politics,stage (the catalogue's).
PX='{json}': switches and values laid over E.DEFAULT for the run (as cx2run.py), e.g. PX='{"role_practice": true}'.
The 10-10 run (480 lives per worker, push .01, 320 lives a group) found black, red and green identity following the
push (.34 to .36 at forty) and white and blue barely (.20, .21), with contentment falling from .60 to .45 and .46."""
import os, sys, re, json
import numpy as np
from multiprocessing import Pool
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E
from batch import load_batch
CAT = os.path.join(_engine.LIBRARY, "earth_perks_titles.py")
PACKS = [x for x in os.environ.get("PACKS", "science,politics,stage").split(",") if x]
SEEDS = (21, 22, 23, 24)
CN = dict(zip("WUBRG", ["white", "blue", "black", "red", "green"]))


def _load():
    return load_batch("earth", roles=CAT, packs=PACKS)


def one(args):
    seed, n, push, groups = args
    L = _load()
    grp = np.arange(n) % len(groups)
    def steer(t, P, nic, y):
        for g, c in enumerate(groups):
            if c != "-":
                y[grp == g, "WUBRG".index(c)] += push
    o = E.run(N=n, years=80, seed=seed, lib=L, intervention=steer, P=json.loads(os.environ.get("PX") or "{}"))
    return dict(ever=o["roles"]["ever"], grp=grp, W=o["W_hist"].transpose(1, 0, 2), A=o["A_hist"].transpose(1, 0, 2),
                nperks=o["V_hist"]["n_perks"].T, res=o["R_hist"].transpose(1, 0, 2), content=o["V_hist"]["content"].T)


def run(n, push, out, groups):
    with Pool(4) as p:
        rs = p.map(one, [(s, n, push, groups) for s in SEEDS])
    np.savez_compressed(out, **{k: np.concatenate([r[k] for r in rs]) for k in rs[0]}, groups=np.array(groups),
                        px=np.array(os.environ.get("PX") or "{}"))
    print("saved", out)


def summary(files):
    G = _load()["ROLES"]; names = list(G["names"]); NT = G["NT"]; ways = np.asarray(G["ways"]); kn = np.array(G["kindname"])
    pack = {}
    for p in PACKS:
        for nm in re.findall(r'dict\(name="([^"]+)"', open(os.path.join(_engine.PACKS, p, "catalogue.py")).read()):
            pack[nm] = p
    groups, runs = {}, []
    for k, f in enumerate(files):
        d = np.load(f); gl = [str(c) for c in d["groups"]]
        sfx = str(k + 1) if len(files) > 1 else ""                      # several runs: each group carries its run's number
        lab_ = {c: (f"unsteered{k + 1}" if c == "-" else CN[c] + sfx) for c in gl}
        for g, c in enumerate(gl):
            m = d["grp"] == g
            groups[lab_[c]] = {x: d[x][m] for x in ("ever", "W", "A", "nperks", "res", "content")}
        runs.append(lab_)
    GN = list(groups)
    def row(lab, vals, fmt="{:9.3f}"):
        print(f"{lab:34s} " + " ".join(fmt.format(v) for v in vals))
    print(f"{'':34s} " + " ".join(f"{g:>9s}" for g in GN))
    for k, f in enumerate(files):
        print(f"  run {k + 1}: {f}, PX {np.load(f)['px'] if 'px' in np.load(f) else '{}'}")
    row("lives", [len(groups[g]["ever"]) for g in GN], "{:9d}")
    for lab, key in (("identity colors at 40", "W"), ("wants at 40", "A")):
        print("\n" + lab)
        for c in range(5):
            row(f"  {CN['WUBRG'[c]]}", [groups[g][key][:, 40, c].mean() for g in GN])
    title = np.arange(len(names)) < NT; car = kn == "career"
    mono = lambda c: np.array([(ways[i] > 0).sum() == 1 and ways[i, c] > 0 for i in range(len(names))])
    print("\nshare of lives that ever reach")
    for p in PACKS:
        row(f"  a {p}-pack title", [groups[g]["ever"][:, np.array([pack.get(x) == p for x in names]) & title].any(1).mean()
                                    for g in GN])
    for c in range(5):
        m = mono(c) & car
        row(f"  a mono-{CN['WUBRG'[c]]} career ({m.sum()})", [groups[g]["ever"][:, m].any(1).mean() for g in GN])
    print("\ncareers and perks")
    row("  careers ever", [groups[g]["ever"][:, car].sum(1).mean() for g in GN], "{:9.1f}")
    row("  perks ever", [groups[g]["ever"][:, NT:].sum(1).mean() for g in GN], "{:9.1f}")
    row("  perks held at 50", [groups[g]["nperks"][:, 50].mean() for g in GN], "{:9.1f}")
    row("  perks held at 50, 90%", [np.percentile(groups[g]["nperks"][:, 50], 90) for g in GN], "{:9.0f}")
    print("\nlife outcomes (mean)")
    for r, nm in enumerate(E.RESOURCES):
        row(f"  {nm} at 60", [groups[g]["res"][:, 60, r].mean() for g in GN])
    row("  contentment, ages 30-70", [np.nanmean(groups[g]["content"][:, 30:70]) for g in GN])
    for lab_ in runs:   # careers each steered group reaches most often against its own run's unsteered group
        u = next((groups[v] for c, v in lab_.items() if c == "-"), None)
        if u is None:
            continue
        for c, v in lab_.items():
            if c == "-":
                continue
            s = groups[v]; ns, nu = len(s["ever"]), len(u["ever"]); rr = []
            for i in np.nonzero(car)[0]:
                a, b = s["ever"][:, i].sum(), u["ever"][:, i].sum()
                if a >= 6:
                    rr.append(((a + .5) / ns / ((b + .5) / nu), names[i], a / ns, b / nu, i))
            print(f"\ncareers {v} lives reach most often against unsteered (ratio, steered, unsteered):")
            for x in sorted(rr, reverse=True)[:10]:
                print(f"  {x[1]:32s} {''.join('WUBRG'[j] for j in range(5) if ways[x[4], j] > 0):4s} {x[0]:5.1f}  {x[2]:.3f}  {x[3]:.3f}")


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]), float(sys.argv[3]), sys.argv[4], (sys.argv[5] if len(sys.argv) > 5 else "-,W,U,B,R,G").split(","))
    else:
        summary(sys.argv[2:])
