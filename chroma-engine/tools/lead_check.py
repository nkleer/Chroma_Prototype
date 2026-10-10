"""S7 "Ways to lead" refit targets (chroma-ideas/social-mechanics.md S7, "Checks"; v22.4 bar row G11): falls per way
within 1.5x of each other, and mean time in post per lead colour within 1.2x.

Runs Earth with the packs and the outer world on (as the game plays it) and reads every post People modelled (held at
the end and ended), then prints each target's value, its target and ok or MISS:
  s7_falls  falls per way: the legitimacy steps of the falls in numbers (a post's `falls`, by the way held when it came)
            per 10 post-years held in that way; the highest over the lowest, 1.5 or less. A post's years count in its
            first way (its lead colour) until its last change of way (way_t), then in its last way (a post that changed
            way twice puts the middle way's years in the first). Fewer than --min-falls falls in a way is a MISS.
  s7_post   mean time in post per lead colour (the lead colour on taking the post): years from the start to its end, or
            to the run's end for a post still held; the highest over the lowest, 1.2 or less.
Information lines follow (not judged): posts and falls counted per way and colour, posts that ended by a fall, the end
reasons.

    OMP_NUM_THREADS=1 python3 -B chroma-engine/tools/lead_check.py [--lives 300] [--years 80] [--seeds 41]
        [--on] [--P JSON] [--json FILE]

The engine runs with its own DEFAULT (the commit's switches) and world on. --on also switches lead_ways on with what it
needs (sph_levers) and the t_steps row's company (sph_fair, sph_events, sph_haunts, sph_hours, cur_on), for a commit
from before the v22.4 refit; --P adds overrides as JSON. CHROMA_ENGINE picks the engine (tools/_engine.py). --json writes
the numbers to FILE (under OUT_DIR when relative; never into the repository). Exit code 0 when both targets pass.
"""
import sys, os, json, time, argparse, collections
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
import engine as E, batch
import world_link as WLM
from world_keys import LEAD_WAYS

COLS = "WUBRG"
ON = dict(lead_ways=True, sph_levers=True, sph_fair=True, sph_events=True, sph_haunts=True, sph_hours=True, cur_on=True)
ROWS = []


def row(name, value, target, ok, why=""):
    ROWS.append(dict(name=name, value=value, target=target, flag="ok" if ok else "MISS", why=why))
    print(f"  {name:<10s} {value!s:<44s} {target:<34s} {'ok' if ok else 'MISS'}{'  (' + why + ')' if why else ''}",
          flush=True)


_PP = []
_out0 = WLM.WorldLink.output


def _output(self, *a, **k):   # keep the run's People: its posts are read after the run
    _PP.append(self.PP)
    return _out0(self, *a, **k)


WLM.WorldLink.output = _output


def posts_of(N, Y, seed, L, P):
    _PP.clear()
    E.run(N=N, years=Y, seed=seed, lib=L, P=P)
    if not _PP:
        raise SystemExit("the run had no outer world (P['world'] off?)")
    PP = _PP[-1]
    if not getattr(PP, "lw", False):
        raise SystemExit("lead_ways is off on this commit (or sph_levers is): pass --on to switch it on")
    return PP, list(PP.lw_ended) + list(PP.lw_posts), int(PP.t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lives", type=int, default=300)
    ap.add_argument("--years", type=int, default=80)
    ap.add_argument("--seeds", default="41")
    ap.add_argument("--on", action="store_true")
    ap.add_argument("--P", default="{}")
    ap.add_argument("--min-falls", type=int, default=20)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    P = dict(E.DEFAULT); P.update(ON if a.on else {}); P.update(json.loads(a.P)); P["world"] = True
    seeds = [int(s) for s in a.seeds.split(",") if s]
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    print(f"S7 lead_check: engine {_engine.ENGINE} (engine.py {E.__file__ and __import__('hashlib').md5(open(E.__file__, 'rb').read()).hexdigest()[:12]}),"
          f" {a.lives} lives x {a.years} years, seeds {a.seeds}, world on{', --on' if a.on else ''}"
          f"{', P ' + a.P if a.P != '{}' else ''}", flush=True)
    falls = np.zeros(5); expo = np.zeros(5); tip = [[] for _ in range(5)]
    fell = np.zeros(5); why = collections.Counter(); posts_w = np.zeros(5, int); held = 0
    t0_ = time.time()
    for s in seeds:
        PP, posts, T = posts_of(a.lives, a.years, s, L, P)
        for p in posts:
            end = p["end_t"] if p.get("end_t") is not None else T
            held += p.get("end_t") is None
            c0, c1 = int(p["col"]), int(p["way"])
            wt = min(max(int(p.get("way_t", p["t0"])), int(p["t0"])), end)
            expo[c0] += (wt - p["t0"]) / 52.0; expo[c1] += (end - wt) / 52.0
            for f_ in p.get("falls") or []:
                falls[int(f_[1])] += 1
            tip[c0].append((end - p["t0"]) / 52.0)
            posts_w[c1] += 1
            if p.get("why") == "fell":
                fell[c1] += 1
            why[p.get("why") or "held at the end"] += 1
        print(f"  seed {s}: {len(posts)} posts ({time.time() - t0_:.0f} s)", flush=True)
    print()
    rate = np.where(expo > 0, 10 * falls / np.maximum(expo, 1e-9), np.nan)
    vals = " ".join(f"{LEAD_WAYS[i][:4]} {rate[i]:.2f}" for i in range(5))
    few = [LEAD_WAYS[i] for i in range(5) if falls[i] < a.min_falls]
    r_f = float(np.max(rate) / np.min(rate)) if np.all(rate > 0) else float("inf")
    row("s7_falls", f"{r_f:.2f}x" if np.isfinite(r_f) else "n/a", "max/min falls per 10 post-years <= 1.5x", r_f <= 1.5 and not few,
        f"too few falls in {', '.join(few)} (under {a.min_falls})" if few else "")
    print(f"             per 10 post-years: {vals}")
    mp = np.array([np.mean(x) if x else np.nan for x in tip])
    r_p = float(np.max(mp) / np.min(mp)) if np.all(mp > 0) else float("inf")
    emp = [COLS[i] for i in range(5) if not tip[i]]
    row("s7_post", f"{r_p:.2f}x" if np.isfinite(r_p) else "n/a", "max/min mean years in post <= 1.2x", r_p <= 1.2 and not emp,
        f"no posts led by {', '.join(emp)}" if emp else "")
    print("             mean years: " + " ".join(f"{COLS[i]} {mp[i]:.2f}" for i in range(5)))
    print()
    print("  information (not judged):")
    print("    posts by lead colour:   " + " ".join(f"{COLS[i]} {len(tip[i])}" for i in range(5)) + f"; held at the end {held}")
    print("    posts by last way:      " + " ".join(f"{LEAD_WAYS[i]} {posts_w[i]}" for i in range(5)))
    print("    falls by way:           " + " ".join(f"{LEAD_WAYS[i]} {int(falls[i])}" for i in range(5)))
    print("    post-years by way:      " + " ".join(f"{LEAD_WAYS[i]} {expo[i]:.0f}" for i in range(5)))
    print("    posts ended by a fall:  " + " ".join(f"{LEAD_WAYS[i]} {int(fell[i])}" for i in range(5)))
    print("    end reasons:            " + ", ".join(f"{k} {v}" for k, v in why.most_common()))
    ok = all(r["flag"] == "ok" for r in ROWS)
    print(f"\n{'ALL PASS' if ok else 'MISS'}")
    if a.json:
        fn = a.json if os.path.isabs(a.json) else os.path.join(_engine.OUT, a.json)
        with open(fn, "w") as f:
            json.dump(dict(rows=ROWS, lives=a.lives, years=a.years, seeds=seeds, on=a.on, P=json.loads(a.P),
                           falls=falls.tolist(), post_years=expo.tolist(), falls_rate=rate.tolist(),
                           mean_years=mp.tolist(), posts=[len(x) for x in tip], fell=fell.tolist(), why=dict(why)), f,
                      indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
