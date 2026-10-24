"""Lives with the land on, for Release's land rows (v25 lane D; chroma-world/spheres/land-checks-measure.md run B).

One seed of N lives in one world, v25's shipped set (engine.SHIP_V25 over DEFAULT, batch flags SHIP_V25_BATCH),
unplayed, for the given years. The engine is not changed: the land's own methods are wrapped in this process to log
what the rows read (the moments shown with their tone and the age, the minutes a week in nature, the company drawn,
the ways taken up). Writes one JSON file; land_judge.py reads one or more of them.

    OMP_NUM_THREADS=1 python3 -B chroma-engine/tools/land_lives.py <seed> <N> <years> <out.json>

Release's run B: seeds 41 to 44, 400 lives, 100 years, one core a seed.
"""
import json, os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
import engine as E, batch
import world_land as WLD

seed, N, Y, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
LOG = dict(moments=[], company=[], ways=[], mins_years=0, mins_120=0)
_cur = {}   # the year's minutes: life -> [sum, count]
_yr = [-1]


def _flush():
    for n, (s_, c_) in _cur.items():
        if c_:
            LOG["mins_years"] += 1; LOG["mins_120"] += int(s_ / c_ >= 120.0)
    _cur.clear()


_o_seen = WLD.Land.seen
def seen(self, ns, ss):
    t = int(self.PP.t); a = float(self.PP._age(t))
    for n, si in zip(np.asarray(ns).tolist(), np.asarray(ss).tolist()):
        if 0 <= si < self.S and (self.ls[si] or self.ld[si]):
            LOG["moments"].append([int(n), t, round(a, 2), self.mrow[si], self.mtone[si], bool(self.ld[si])])
    return _o_seen(self, ns, ss)


_o_month = WLD.Land._month
def _month(self, t, a):
    _o_month(self, t, a)
    if not self.dev:
        return
    y = int(t // 52)
    if y != _yr[0]:
        _flush(); _yr[0] = y
    if a >= 18:
        dead = np.asarray(self.PP.dead, bool)
        for n in np.nonzero(~dead)[0].tolist():
            r = _cur.setdefault(n, [0.0, 0]); r[0] += float(self.mins[n]); r[1] += 1


_o_comp = WLD.Land.company_draw
def company_draw(self, n, si, a):
    cm = _o_comp(self, n, si, a)
    if 0 <= si < self.S and self.mwith[si]:
        LOG["company"].append([int(n), round(float(a), 2), None if cm is None else cm["kind"], self.mrow[si]])
    return cm


_o_open = WLD.Land.open_way
def open_way(self, n, key, age, t):
    ok = _o_open(self, n, key, age, t)
    if ok:
        LOG["ways"].append([int(n), key, round(float(age), 2)])
    return ok


_o_year = WLD.Land._year
_snap = {}
def _year(self, t, a):
    """LN7's denominator: each town's stretches' gross movement, year by year (|change| of health and wildness)."""
    if "h" in _snap:
        _snap["gross"] += np.abs(self.h - _snap["h"]) + np.abs(self.wd - _snap["w"])
    else:
        _snap["gross"] = np.zeros_like(self.h)
    _o_year(self, t, a)
    _snap["h"], _snap["w"] = self.h.copy(), self.wd.copy()


WLD.Land.seen, WLD.Land._month, WLD.Land.company_draw, WLD.Land.open_way, WLD.Land._year = seen, _month, company_draw, open_way, _year
for k_, v_ in E.SHIP_V25_BATCH.items():
    setattr(batch, k_, v_)
L = batch.load_batch("earth")
P = dict(E.DEFAULT); P.update(E.SHIP_V25)
t0 = time.time()
o = E.run(N=N, years=Y, seed=seed, lib=L, P=P)
_flush()
land = o.get("land")
if land is None:
    sys.exit("land_lives: no land in the run's output (is wa_land in this engine's shipped set?)")
Wl = np.asarray(o["W_hist"][-1], float)
out = dict(seed=seed, N=N, years=Y, seconds=round(time.time() - t0, 1), lead=["WUBRG"[int(i)] for i in Wl.argmax(1)],
           land=land, national=o.get("national"), log=LOG,
           gross=(_snap["gross"].round(5).tolist() if "gross" in _snap else None))
json.dump(out, open(OUT, "w"))
print(f"land_lives seed {seed}: {N} lives x {Y} years in {out['seconds']} s; {len(LOG['moments'])} land moments, "
      f"{len(LOG['ways'])} ways taken; wrote {OUT}")
