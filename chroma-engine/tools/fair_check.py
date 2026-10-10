"""S1 "Fairness read five ways": the colour-even targets of chroma-ideas/social-mechanics.md, judged at v22.4's refit
(chroma-release/records/v22.4/scope.md row G6). Lives with the world on and fair_read switched on; each target is printed
with its values, its spread and ok or MISS:

  s1_parts    every sphere carries all five parts of fairness (W the same rules for all, U the truth and the reasons, B
              their due, R respect and a say, G people who mean well by us), each read from a state of its own or, with
              none, by the sphere's mean step (World.sph_fair_parts); finite in every town
  s1_counts   tagged sphere events (World.fair_tags) that moved felt fairness, counted once per part they carry:
              largest / smallest <= 1.5
  s1_fair     mean felt fairness (over the nine spheres and the adult years, 18 on) by the life's lead colour: largest
              minus smallest <= .03

    python3 -B chroma-engine/tools/fair_check.py TARGET [N=300] [SEEDS=7] [--years 80] [--P JSON] [--stats FILE]

TARGET is one of the three, or "all". SEEDS is a comma list; their counts are pooled (one process per seed). --P lays
switches over the run's own, which are engine DEFAULT with world and fair_read on. --stats FILE keeps the run's counts:
a FILE holding a run of the same engine, lives, years, seeds and switches is read instead of running again, so the three
rows can share one run. Exit code 0 when every printed target is ok. CHROMA_ENGINE names the engine (tools/_engine.py);
LIB a Library folder."""
import sys, os, json, hashlib, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np

COLORS = "WUBRG"
TARGETS = ("s1_parts", "s1_counts", "s1_fair")
RUN_P = dict(world=True, fair_read=True)


def one(argv):
    """One seed's lives; returns the counts as plain lists."""
    N, Y, seed, Pjson = argv
    import engine as E, batch, world_people as PM, world as WM
    batch.LIB_DIR = os.environ.get("LIB") or batch.LIB_DIR
    seen = []; acc = dict(fair=np.zeros(5), years=np.zeros(5))
    init = PM.People.__init__; week = PM.People._fair_week

    def keep(self, *a, **k):   # the run's People, to read its counts (nothing in the run changes)
        init(self, *a, **k); seen.append(self)

    def yearly(self, t):       # each year from 18: felt fairness by the life's lead colour
        week(self, t)
        if t % 52 == 0 and self._age(t) >= 18:
            live = ~self.dead
            lead = np.argmax(np.asarray(self.w, float), 1)
            f = np.asarray(self.fair, float).mean(1)
            np.add.at(acc["fair"], lead[live], f[live]); np.add.at(acc["years"], lead[live], 1.0)
    PM.People.__init__ = keep; PM.People._fair_week = yearly
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    P = dict(E.DEFAULT); P.update(RUN_P); P.update(json.loads(Pjson))
    E.run(N=int(N), years=int(Y), seed=int(seed), lib=L, P=P)
    if not seen or not getattr(seen[-1], "fr_read", False):
        raise SystemExit("fair_check: felt fairness was never read five ways (the world, sph_fair and fair_read must be on)")
    pp = seen[-1]; W = pp.W
    tags = W.fair_tags()
    cnt = np.zeros(5); n_ev = 0
    for _, i_, _l in np.asarray(W.sph_ev_log).tolist():
        mv = tags["events"].get(int(i_))
        if not mv:
            continue
        n_ev += 1
        for _j, ps, _sd in mv:
            for p_ in set(ps):
                cnt[COLORS.index(p_)] += 1
    R = np.asarray(W.sph_fair_parts(), float)   # n_loc x 9 x 5
    import sphere_data as SD
    direct = []
    for sp in WM.SPHERES:
        d = SD.FAIR["states"].get(sp, {})
        ks = list(d.get("fair", [])) + list(d.get("against") or []) or ["rule.favour"]
        direct.append("".join(sorted({p_ for k_ in ks for p_ in (tags["parts"].get(k_) or COLORS)}, key=COLORS.index)))
    return dict(cnt=cnt.tolist(), events=n_ev, fair=acc["fair"].tolist(), years=acc["years"].tolist(),
                finite=bool(np.isfinite(R).all()), direct=direct, spheres=list(WM.SPHERES))


def pooled(runs):
    out = dict(runs[0])
    for k in ("cnt", "fair", "years"):
        out[k] = np.sum([r[k] for r in runs], 0).tolist()
    out["events"] = sum(r["events"] for r in runs); out["finite"] = all(r["finite"] for r in runs)
    return out


def ratio(v):
    v = np.asarray(v, float)
    return float(v.max() / v.min()) if v.min() > 0 else float("inf")


def per(v, d=3):
    return " ".join(f"{c} {float(x):.{d}f}" for c, x in zip(COLORS, v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", choices=TARGETS + ("all",))
    ap.add_argument("N", nargs="?", type=int, default=300)
    ap.add_argument("seeds", nargs="?", default="7")
    ap.add_argument("--years", type=int, default=80)
    ap.add_argument("--P", default="{}")
    ap.add_argument("--stats", default=None)
    a = ap.parse_args()
    seeds = [int(s) for s in a.seeds.split(",") if s.strip()]
    Pj = json.dumps(json.loads(a.P), sort_keys=True)
    md5 = lambda f: hashlib.md5(open(os.path.join(_engine.ENGINE, f), "rb").read()).hexdigest()[:12]
    key = dict(engine=md5("engine.py"), people=md5("world_people.py"), world=md5("world.py"), N=a.N, years=a.years,
               seeds=seeds, P=Pj, lib=os.path.abspath(os.environ.get("LIB") or _engine.LIBRARY))
    st = None
    if a.stats and os.path.exists(a.stats):
        try:
            d = json.load(open(a.stats))
            st = d["stats"] if d.get("key") == key else None
        except Exception:
            st = None
    print(f"S1 fairness read check: engine {_engine.ENGINE} (engine.py {key['engine']}, world_people.py {key['people']}),"
          f" {a.N} lives x {a.years} years, seeds {','.join(map(str, seeds))}, P {Pj} over {json.dumps(RUN_P, sort_keys=True)}"
          + (f"; counts read from {a.stats}" if st is not None else ""), flush=True)
    if st is None:
        jobs = [(a.N, a.years, s, Pj) for s in seeds]
        if len(jobs) > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(len(jobs)) as pool:
                st = pooled(pool.map(one, jobs))
        else:
            st = pooled([one(jobs[0])])
        if a.stats:
            with open(a.stats, "w") as f:
                json.dump(dict(key=key, stats=st), f, sort_keys=True)
    ok_all = True

    def row(name, vals, value, target, ok, note=""):
        nonlocal ok_all
        ok_all &= bool(ok)
        print(f"  {name:<10s} {vals:<46s} {value:<16s} {target:<16s} {'ok' if ok else 'MISS'}{note}", flush=True)

    want = TARGETS if a.target == "all" else (a.target,)
    if "s1_parts" in want:
        mean_ = [sp for sp, d in zip(st["spheres"], st["direct"]) if len(d) < 5]
        row("s1_parts", f"{len(st['spheres'])} spheres x 5 parts", "finite" if st["finite"] else "NOT finite",
            "all five, each", st["finite"],
            "  (by a state of their own: " + ", ".join(f"{sp} {d}" for sp, d in zip(st["spheres"], st["direct"]))
            + (f"; the rest by the mean in {', '.join(mean_)}" if mean_ else "") + ")")
    if "s1_counts" in want:
        r = ratio(st["cnt"])
        row("s1_counts", per(st["cnt"], 0), f"ratio {r:.2f}x" if np.isfinite(r) else "ratio inf (a 0)",
            "target <= 1.5x", st["events"] > 0 and r <= 1.5, f"  ({st['events']} tagged events)")
    if "s1_fair" in want:
        y = np.asarray(st["years"], float); m = np.asarray(st["fair"], float) / np.maximum(y, 1)
        sp = float(m.max() - m.min()) if (y > 0).all() else float("inf")
        row("s1_fair", per(m), f"spread {sp:.3f}", "target <= .030", sp <= 0.03,
            f"  (adult life-years {per(y, 0)})")
    print(("PASS" if ok_all else "MISS") + " " + ",".join(want), flush=True)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
