"""v22.5 refit read (F9 and the means targets, chroma-ideas/means/modifiers.md; chroma-ideas/realism/v22.5-realism-list.md):
Earth with the live packs, world on or off, every switch as DEFAULT plus PX. Prints one JSON line of the rows the refit
fits, then a short table.
    PX='{json}' python3 -B chroma-engine/tools/v225_read.py <lives> <years> <seed> <on|off>
Rows: health, money and ties by age (mean, the middle 80%'s width, the share at 5% or less, health's share at 98% or
more); ever partnered, ever a parent and ever in a faith by 50 and by the end; deaths before 30/50/65/80/90/100 (when
self_death is on) and their causes; per life the enemies, hidden wrongs and defiances; White's breaking-the-law ratio
(its rate per life over the others'); how far the pie moves per decade at 25-35, 45-55 and 65-75."""
import sys, os, json, time
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch
N, Y, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); world = sys.argv[4] == "on"
L = batch.load_batch("earth", packs=list(batch.PACKS))
P = dict(E.DEFAULT); P.update(json.loads(os.environ.get("PX", "{}"))); P["world"] = world
t0 = time.time()
LOG = min(N, int(os.environ.get("LOG", 40)))   # lives with a full event log (homes lost, body and mind threats)
o = E.run(N=N, years=Y, seed=seed, lib=L, P=P, log_lives=list(range(LOG)))
R = np.asarray(o["R_hist"]); W = np.asarray(o["W_hist"])   # years+1 x N x 5
MON, HEA, TIE = 0, 2, 3
dage = np.full(N, np.inf); cause = {}
for n_, t_, c_ in o["died"]:
    dage[n_] = t_ / 52; cause[n_] = c_
out = dict(lives=N, years=Y, seed=seed, world=world, sec=round(time.time() - t0))
AGES = [a for a in (10, 15, 20, 30, 40, 50, 60, 70, 80, 90) if a <= Y]
for nm, i in (("health", HEA), ("money", MON), ("ties", TIE)):
    rows = {}
    for a in AGES:
        live = dage > a
        if live.sum() < 5:
            continue
        x = R[a, live, i]
        rows[a] = dict(mean=round(float(x.mean()), 3), w80=round(float(np.percentile(x, 90) - np.percentile(x, 10)), 3),
                       lo5=round(float((x <= 0.05).mean()), 3), hi98=round(float((x >= 0.98).mean()), 3))
    out[nm] = rows
# commitments ever started (or inherited, for a faith), by 50 and by the end
KS = {"partner": E.KIDX["partner"], "children": E.KIDX["children"], "faith": E.KIDX["faith"]}
first = {k: np.full(N, np.inf) for k in KS}
for c_ in o["commits"]:
    n_, t_, kk, how = c_[0], c_[1], c_[2], c_[3]
    for k, ki in KS.items():
        if kk == ki and how in ("start", "inherited"):
            first[k][n_] = min(first[k][n_], t_ / 52)
for k in KS:
    out[k] = dict(by50=round(float((first[k] <= 50).mean()), 3), ever=round(float(np.isfinite(first[k]).mean()), 3))
if o["died"]:
    out["died_before"] = {a: round(float((dage < a).mean()), 3) for a in (30, 50, 65, 80, 90, 100) if a <= Y}
    out["causes"] = dict(Counter(("own act" if str(c).startswith("through") else c) for c in cause.values()).most_common(10))
mk = o["marks"]; MN = mk["names"]; MC = np.asarray(mk["n"])
for nm in ("made an enemy", "hid a wrong", "defied an authority", "broke the law", "used drugs", "took a life"):
    if nm in MN:
        out["mark: " + nm] = round(float(MC[:, MN.index(nm)].mean()), 2)
if "broke the law" in MN:   # White's rate per life over the rest, by the colour leading at 40
    lead = np.argmax(W[min(40, Y)], 1); bl = MC[:, MN.index("broke the law")]
    if (lead == 0).any() and (lead != 0).any() and bl[lead != 0].mean() > 0:
        out["white_law_ratio"] = round(float(bl[lead == 0].mean() / bl[lead != 0].mean()), 2)
mv = {}
for a0, a1 in ((25, 35), (45, 55), (65, 75)):
    if a1 <= Y:
        live = dage > a1
        mv[f"{a0}-{a1}"] = round(float(np.abs(W[a1, live] - W[a0, live]).sum(1).mean() / 2), 3)
out["pie_move"] = mv
# ---- Release's F9 rows (records/v22.5/scope.md): partners, parents, homes, work, illness, deaths, means
SN = o["sit_names"]; LE = [(n_, t_ / 52, SN[s_]) for n_, t_, s_ in o["life_events"]]
def ev_ages(names):
    d = {}
    for n_, a_, nm_ in LE:
        if nm_ in names:
            d.setdefault(n_, []).append(a_)
    return d
alive_at = lambda a: dage > a
def med(x):
    return round(float(np.median(x)), 1) if len(x) else None
CAR_, PAR_, KID_ = E.KIDX["career"], E.KIDX["partner"], E.KIDX["children"]
cm = {}
for c_ in o["commits"]:
    cm.setdefault((c_[0], c_[2]), []).append((c_[1] / 52, c_[3]))
f9 = {}
# partners: first partnership age, splits, widowed by 80, partner dead before 50
pst = [min(a for a, h in cm.get((n_, PAR_), []) if h == "start") for n_ in range(N) if any(h == "start" for _, h in cm.get((n_, PAR_), []))]
f9["F9.7 first partner age, median"] = med(pst)
partd = [n_ for n_ in range(N) if any(h == "start" for _, h in cm.get((n_, PAR_), []))]
spl = [n_ for n_ in partd if any(h in ("broke up", "left") for _, h in cm.get((n_, PAR_), []))]
f9["F9.8 partnered with a split"] = round(len(spl) / max(len(partd), 1), 3)
wid = [n_ for n_ in partd if any(h == "widowed" for _, h in cm.get((n_, PAR_), []))]
p80 = [n_ for n_ in partd if dage[n_] > 80]
f9["F9.9 widowed, partnered alive at 80"] = round(sum(1 for n_ in p80 if any(h == "widowed" and a < 80 for a, h in cm[(n_, PAR_)])) / max(len(p80), 1), 3)
f9["F9.10 widowed before 50, of partnered"] = round(sum(1 for n_ in partd if any(h == "widowed" and a < 50 for a, h in cm[(n_, PAR_)])) / max(len(partd), 1), 3)
# parents
kst = [min(a for a, h in cm.get((n_, KID_), []) if h == "start") for n_ in range(N) if any(h == "start" for _, h in cm.get((n_, KID_), []))]
f9["F9.2 first child (children commitment) age, median"] = med(kst)
born = ev_ages({"a child is born"})
f9["F9.2b first 'a child is born' age, median"] = med([min(v) for v in born.values()])
par50 = [n_ for n_ in range(N) if any(h == "start" and a <= 50 for a, h in cm.get((n_, KID_), []))]
f9["F9.3 'a child is born' per parent by 50, mean"] = round(float(np.mean([sum(1 for a in born.get(n_, []) if a <= 50) for n_ in par50])), 2) if par50 else None
ab = [a for v in born.values() for a in v]
f9["F9.4 births after 50, share"] = round(float(np.mean(np.array(ab) > 50)), 3) if ab else None
# homes
buy = ev_ages({"buying a home"})
f9["F9.11 bought a home by 50"] = round(sum(1 for v in buy.values() if min(v) <= 50) / N, 3)
f9["F9.12 first purchase age, median"] = med([min(v) for v in buy.values()])
f9["F9.13 purchases per owner"] = round(float(np.mean([len(v) for v in buy.values()])), 2) if buy else None
ba = [a for v in buy.values() for a in v]
f9["F9.14 purchases at 75+, share"] = round(float(np.mean(np.array(ba) >= 75)), 3) if ba else None
lost = set()
for n_, evs in o["events"].items():
    for e_ in evs:
        ds_ = e_.get("deep_state") or {}
        if ds_.get("holding") == "home" and "lost" in str(ds_.get("kind", "")) or ds_.get("kind") in ("evicted", "repossessed"):
            lost.add(n_)
f9["F9.15 lost a home (logged lives)"] = round(len(lost) / max(LOG, 1), 3)
# work
car = {n_: sorted(cm.get((n_, CAR_), [])) for n_ in range(N)}
lj = [sum(1 for _, h in v if h == "lost job") for v in car.values()]
f9["F9.17 job losses per life, mean"] = round(float(np.mean(lj)), 2)
f9["F9.18 at least one / four or more"] = [round(float(np.mean(np.array(lj) >= 1)), 3), round(float(np.mean(np.array(lj) >= 4)), 3)]
f9["F9.19 employers (career starts), mean"] = round(float(np.mean([sum(1 for _, h in v if h == "start") for v in car.values()])), 2)
firm = ev_ages({"new owners take over the firm", "folded into a bigger firm", "the state takes over the failing firm",
                "the loan the new owners call in"})
f9["F9.20 firm crises per life, mean"] = round(sum(len(v) for v in firm.values()) / N, 2)
wy = oy = 0.0
for n_, v in car.items():   # weeks out of work at 20-64, not retired (career intervals from the commitments)
    held_, t0_, ret_ = False, 0.0, None
    ivs = []
    for a, h in v:
        if h == "start" and not held_:
            held_, t0_ = True, a
        elif h in ("lost job", "left", "retired") and held_:
            ivs.append((t0_, a)); held_ = False
        if h == "retired":
            ret_ = a
    if held_:
        ivs.append((t0_, 200.0))
    hi_ = min(64.0, dage[n_], ret_ if ret_ is not None else 64.0)
    if hi_ <= 20:
        continue
    inw = sum(max(0.0, min(b, hi_) - max(a, 20.0)) for a, b in ivs)
    wy += hi_ - 20.0; oy += (hi_ - 20.0) - inw
f9["F9.21 out of work at 20-64 (not retired), share of years"] = round(oy / max(wy, 1e-9), 3)
ra = [a for v in car.values() for a, h in v if h == "retired"]
f9["F9.22 retirement age, median"] = med(ra)
# illness
bd = o.get("body") or {}
if bd:
    ca = np.asarray(bd["conditions"]["age"]); cw = np.asarray(bd["conditions"]["weight"])
    first_c = np.where((cw > 0).any(1), np.where(cw > 0, ca, np.inf).min(1), np.inf)
    f9["F9.23 a lasting condition by 40/65/80 (living)"] = [round(float((first_c[alive_at(a)] <= a).mean()), 3) for a in (40, 65, 80)]
sev = ev_ages({"a frightening diagnosis", "a serious accident or illness"})
f9["F9.24 serious (moments) before 50 / by 80"] = [round(sum(1 for v in sev.values() if min(v) < 50) / N, 3),
                                                   round(sum(1 for v in sev.values() if min(v) <= 80) / max(int(alive_at(80).sum()), 1), 3)]
dep = ev_ages({"a sadness that will not lift", "a long dark season"})
low = set(n_ for n_, evs in o["events"].items() for e_ in evs if (e_.get("body") or {}).get("kind") == "low season"
          and (e_.get("body") or {}).get("what") == "begins" and e_["body"]["age"] <= 65)
f9["F9.25 a low season by 65: moments (all) / body threats (logged)"] = [round(sum(1 for v in dep.values() if min(v) <= 65) / N, 3),
                                                                        round(len(low) / max(LOG, 1), 3)]
f9["F9.26 an addiction takes hold"] = round(len(ev_ages({"an addiction takes hold"})) / N, 3)
# deaths
if o["died"]:
    da = np.array([t_ / 52 for _, t_, _ in o["died"]])
    f9["F9.34 age at death median / mean (the dead)"] = [med(da), round(float(da.mean()), 1)]
    c40 = [c for (_, t_, c) in o["died"] if t_ / 52 < 40]
    f9["F9.35 before 40 by accident or own act"] = round(sum(1 for c in c40 if "accident" in c or str(c).startswith("through")) / max(len(c40), 1), 3) if c40 else None
    f9["F9.35 of old age before 85"] = sum(1 for (_, t_, c) in o["died"] if c == "old age" and t_ / 52 < 85)
# means
Rm = R[:, :, MON]; adult = [a for a in range(18, min(Y, 90) + 1)]
lo_ = np.array([(Rm[a][dage > a] <= 0.05).mean() for a in adult if (dage > a).sum() >= 5])
f9["F9.38 money 5% or less, adults at a time / at 15"] = [round(float(lo_.mean()), 3), out["money"].get(15, {}).get("lo5")]
run5 = 0
for n_ in range(N):
    r_ = 0; mx_ = 0
    for a in range(18, min(Y, int(dage[n_]) if np.isfinite(dage[n_]) else Y) + 1):
        r_ = r_ + 1 if Rm[a, n_] <= 0.05 else 0; mx_ = max(mx_, r_)
    run5 += mx_ >= 5
f9["F9.38 five years running at 5% or less"] = round(run5 / N, 3)
mm = lambda a0, a1: float(np.mean([Rm[a][dage > a].mean() for a in range(a0, min(a1, Y) + 1) if (dage > a).sum() >= 5]))
if Y >= 85:
    f9["F9.38 money mean 70-85 / 40-60"] = round(mm(70, 85) / mm(40, 60), 2)
Rh = R[:, :, HEA]
f9["F9.37 health 98%+, share of adult years"] = round(float(np.mean([(Rh[a][dage > a] >= 0.98).mean() for a in range(30, min(Y, 90) + 1) if (dage > a).sum() >= 5])), 3)
Rt = R[:, :, TIE]
f9["F9.39 ties 5% or less from 15 / under 15"] = [round(float(np.mean([(Rt[a][dage > a] <= 0.05).mean() for a in range(15, min(Y, 90) + 1) if (dage > a).sum() >= 5])), 3),
                                                 round(float(np.mean([(Rt[a] <= 0.05).mean() for a in range(3, 15)])), 3)]
out["f9"] = f9
print(json.dumps(out))
for nm in ("health", "money", "ties"):
    print(f"{nm:7s}" + "".join(f"  {a}: {r['mean']:.2f} w{r['w80']:.2f} lo{r['lo5']:.2f}" + (f" hi{r['hi98']:.2f}" if nm == "health" else "")
                              for a, r in out[nm].items()))
