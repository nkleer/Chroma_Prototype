"""Spheres phase 3: fit each sphere event's base chance a quarter (dynamics.json events_run rates.rule, Outer world's
answers in chroma-engine/notes/spheres-phase3-answers.md item 1):
    base_e = target / 40 / mean of exp(hazard . readings) over calm modern quarters in a world alone
target is the event's count a decade (sphere_data.EV "target": per town for events with only local rows, per society
for events with a big row, whose chance is the towns' mean); calm is no war, no pandemic and no recession. Each event's
hazard is read in every quarter, whatever its epochs (the readings are the same kind in every world). World-fired
events get no base (they fire with the world's own event).
    python3 -B chroma-engine/tools/sphere_ev_fit.py [--seeds 8] [--years 60] [--skip 10] [--check]
Writes (or with --check compares) sphere_ev_base.py beside engine.py in the tree this script sits in."""
import sys, os, argparse, pprint
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "..", "v22-speedpass")
OUT = os.path.join(ENG, "sphere_ev_base.py")
sys.path.insert(0, ENG)
import world as WM, sphere_data as SD


def fit(seeds, years, skip):
    tot = np.zeros(len(SD.EV)); cnt = 0
    for sd in range(1, seeds + 1):
        W = WM.World(sd, params=dict(sph_events=True, sph_ev_base=0.0))
        run = W._sph_events_q
        def hooked(e_need, W=W, run=run):
            nonlocal tot, cnt
            X = run(e_need)
            if W.t >= skip * 52 and W.war == 0 and W.pandemic == 0 and W.phase == 0:
                tot += W._cache_evh.mean(0); cnt += 1
            return X
        W._sph_events_q = hooked
        W.burn_in(years)
    m = tot / max(cnt, 1)
    base = {e["key"]: (0.0 if e.get("fired") else round(float(e["target"] / 40 / m[i]), 8)) for i, e in enumerate(SD.EV)}
    return base, cnt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8); ap.add_argument("--years", type=int, default=60)
    ap.add_argument("--skip", type=int, default=10); ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    base, cnt = fit(a.seeds, a.years, a.skip)
    head = (f'"""Each sphere event\'s fitted base chance a quarter (tools/sphere_ev_fit.py --seeds {a.seeds} --years {a.years} '
            f'--skip {a.skip}; {cnt} calm quarters). Generated: do not edit."""\n')
    txt = head + "BASE = " + pprint.pformat(base, width=120, sort_dicts=False) + "\n"
    if a.check:
        ok = os.path.exists(OUT) and open(OUT).read() == txt
        print("sphere_ev_base.py:", "PASS (as fitted)" if ok else "FAIL (differs from a new fit)")
        sys.exit(0 if ok else 1)
    open(OUT, "w").write(txt)
    print(f"wrote {OUT}: {sum(v > 0 for v in base.values())} events with a base, {cnt} calm quarters")


if __name__ == "__main__":
    main()
