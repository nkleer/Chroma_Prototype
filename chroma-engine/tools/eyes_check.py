"""S3 "Their places' eyes" and S4 "The odd one out": the colour-even targets of chroma-ideas/social-mechanics.md, judged at
v22.4's refit (chroma-release/records/v22.4/scope.md rows G7 and G8). Lives with the world on and the places' eyes
switched on; each target is printed with its value per lead colour (or enemy pair), its spread and ok or MISS:

  s3_rep      mean `rep` change per place reading, by the reader's lead colour: largest minus smallest <= .03
  s3_caught   caught-between moments met per enemy pair (WB WR UR UG BG): largest / smallest <= 1.5
  s4_odd      share of life-years spent the odd one out at a place, by lead colour: largest / smallest <= 1.2
  s4_convert  conversions (Moscovici: a year in which a held-out minority moves its place, three years held) per
              life-year of each lead colour: largest / smallest <= 1.5

    python3 -B chroma-engine/tools/eyes_check.py TARGET [N=300] [SEEDS=7] [--years 80] [--P JSON] [--stats FILE]

TARGET is one of the four, or "all". SEEDS is a comma list; their counts are pooled (one process per seed). --P lays
switches over the run's own, which are engine DEFAULT with world, sph_haunts, sph_hours, sph_events, cur_on, sph_eyes
and sph_odd on (as t_steps' row). --stats FILE keeps the run's counts: a FILE holding a run of the same engine, lives,
years, seeds and switches is read instead of running again, so the four rows can share one run. The caught-between and
odd-one-out moments join the batch as at v22.4's refit (batch.EYES_MOMENTS set True when the engine has it); with none
in the Library, s3_caught has nothing to count and says so. Exit code 0 when every printed target is ok. CHROMA_ENGINE
names the engine (tools/_engine.py); LIB a Library folder."""
import sys, os, json, hashlib, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np

COLORS = "WUBRG"
ENEMY = ("WB", "WR", "UR", "UG", "BG")   # the Canon's enemy pairs, in the order People names them (place a's lead first)
TARGETS = ("s3_rep", "s3_caught", "s4_odd", "s4_convert")
RUN_P = dict(world=True, sph_haunts=True, sph_hours=True, sph_events=True, cur_on=True, sph_eyes=True, sph_odd=True)


def one(argv):
    """One seed's lives; returns the places' counts (world_people.People.eyes_stats) as plain lists and dicts."""
    N, Y, seed, Pjson = argv
    import engine as E, batch, world_people as PM
    batch.LIB_DIR = os.environ.get("LIB") or batch.LIB_DIR
    if hasattr(batch, "EYES_MOMENTS"):
        batch.EYES_MOMENTS = True
    seen = []
    init = PM.People._eyes_init

    def keep(self, wp_):   # the run's People, to read its counts after the run (nothing in the run changes)
        init(self, wp_); seen.append(self)
    PM.People._eyes_init = keep
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    P = dict(E.DEFAULT); P.update(RUN_P); P.update(json.loads(Pjson))
    E.run(N=int(N), years=int(Y), seed=int(seed), lib=L, P=P)
    if not seen:
        raise SystemExit("eyes_check: the places' eyes never started (sph_eyes and the world must be on)")
    st = seen[-1].eyes_stats
    plain = lambda v: v.tolist() if isinstance(v, np.ndarray) else v
    return {k: plain(v) for k, v in st.items()}


def pooled(runs):
    out = {}
    for st in runs:
        for k, v in st.items():
            if isinstance(v, dict):
                d = out.setdefault(k, {})
                for k2, v2 in v.items():
                    d[k2] = d.get(k2, 0) + v2
            elif isinstance(v, list):
                out[k] = (np.asarray(out[k]) + np.asarray(v)).tolist() if k in out else list(v)
            else:
                out[k] = out.get(k, 0) + v
    return out


def ratio(v):
    v = np.asarray(v, float)
    return float(v.max() / v.min()) if v.min() > 0 else float("inf")


def rt(r):
    return f"ratio {r:.2f}x" if np.isfinite(r) else "ratio inf (a 0)"


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
    key = dict(engine=md5("engine.py"), people=md5("world_people.py"), N=a.N, years=a.years, seeds=seeds, P=Pj,
               lib=os.path.abspath(os.environ.get("LIB") or _engine.LIBRARY))
    st = None
    if a.stats and os.path.exists(a.stats):
        try:
            d = json.load(open(a.stats))
            st = d["stats"] if d.get("key") == key else None
        except Exception:
            st = None
    print(f"S3/S4 places' eyes check: engine {_engine.ENGINE} (engine.py {key['engine']}, world_people.py {key['people']}),"
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
    life_y = np.asarray(st["life_years"], float)
    if "s3_rep" in want:
        nr = np.asarray(st["nrep"], float)
        m = np.asarray(st["drep"], float) / np.maximum(nr, 1)
        sp = float(m.max() - m.min()) if (nr > 0).all() else float("inf")
        row("s3_rep", per(m), f"spread {sp:.3f}", "target <= .030", sp <= 0.03,
            f"  ({int(nr.sum())} place readings)")
    if "s3_caught" in want:
        c = st.get("caught", {})
        v = [c.get(p, 0) for p in ENEMY]
        r = ratio(v)
        other = {k: n for k, n in c.items() if k not in ENEMY}
        row("s3_caught", " ".join(f"{p} {n}" for p, n in zip(ENEMY, v)), rt(r), "target <= 1.5x",
            sum(v) > 0 and r <= 1.5, ("  (no caught-between moment met: none in the batch?)" if sum(v) == 0 else "")
            + (f"  other pairs {other}" if other else ""))
    if "s4_odd" in want:
        sh = np.asarray(st["odd_years"], float) / np.maximum(life_y, 1)
        r = ratio(sh)
        row("s4_odd", per(sh), rt(r), "target <= 1.2x", r <= 1.2)
    if "s4_convert" in want:
        cv = np.asarray(st["held"], float) / np.maximum(life_y, 1)
        r = ratio(cv)
        row("s4_convert", per(cv, 4), rt(r), "target <= 1.5x", r <= 1.5,
            f"  ({int(sum(st['held']))} place-years moved)")
    # for reading, not judged
    met = np.asarray(st["blend"], float) + np.asarray(st["hold"], float) + np.asarray(st["leave"], float)
    print(f"  info: life-years {per(life_y, 0)}; odd-one-out moments offered {per(st['odd_fired'], 0)}; blend {per(st['blend'], 0)},"
          f" hold {per(st['hold'], 0)}, leave {per(st['leave'], 0)}; blends per odd moment met {per(np.asarray(st['blend']) / np.maximum(met, 1), 2)}",
          flush=True)
    print(f"  info: caught {st.get('caught_why', {})}, picks {st.get('caught_tag', {})}; talk {st.get('talk', 0)}; acts read"
          f" {st.get('acts', {})}", flush=True)
    print(("PASS" if ok_all else "MISS") + " " + ",".join(want), flush=True)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
