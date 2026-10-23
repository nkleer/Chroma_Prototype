"""Aims v2 (aims_v2, v25 lane B): the scenario pack of Emren's decision #9, on the agenda itself (aims2.Agenda with the
Earth batch's fields and a made-up life around it: no simulation), a few seconds. Each row is one of the decision file's
known risks (section 5) or a mechanism it asks for:

  A1  a window closes exactly at its last week: a test in that week counts, the next week none; the closing is told once;
      a pause does not stop it (pause_stops off), toggling pause and resume never reopens it; with pause_stops a paused
      deadline moves on by the weeks paused
  A2  an entry cost is paid once, when the step is committed to: pause and resume (and the agenda's own pace) never
      charge it again; a refused fee is never charged
  A3  a player's fork is never resolved by the character: it stays in aim_forks, blocks only its aim's progress past it
      (effort stops at the need, no test), the other aims go on; "later" keeps it open; a crowded queue keeps every fork,
      one put a week, the unchanged ones not again within reask weeks
  A4  effort alone never reaches a rung: far past its need with no test and no title held, the rung stays
  A5  learning is kept in proportion after a drop and a pause (no threshold); held again, nothing is earned twice
  A6  the one account: active aims funded by priority; an overfull agenda progresses slower, visibly; shared preparation
      counted once; the agenda review links the forks that want the same hours and its combinations show the cost
  A7  selective upkeep: only a rung that names it lapses after its years without use (the achievement stays), and use
      refreshes it; a rung without upkeep never lapses
  A8  integrated assets: a pair the realm names, both reached and one active, an integrate outcome awards it once per
      life; dropping and taking an aim up again never awards it twice; no table, no asset
  A9  views draw nothing: the agenda, the review and the preview leave the agenda's random stream where it was
  A10 the money rule (Vision 10-23): a step's effort share is the least of its shares of the resources it needs; an
      incidental ask (aims2_par money_min, .02) never caps it; a step that needs money and has none waits, the agenda
      naming money; an entry that cannot be paid is owed, never debited, and paid once it can be
  A12 a rung reached by one's own work sparks a new ambition near it (its sphere or a preparation shared), held with a
      fork, never one the life holds, and none once the agenda holds spark_max aims
  A13 slots grow inside a step (Gamification 10-23's crash): rungs reached in month() and week() spark new aims past the
      slots held (4, then 8, then 16), a player life and one left alone; every mask stays whole, the sparks come after
      the step, and no moment offering "stop" comes about an aim adopted within stop_grace weeks
  A11 the realm's assets (realm_earth.AIM_ASSETS, every pair of shapes): none from first rungs alone, none before
      integrate_age, then one; another pair waits integrate_gap years after it; the asset named by the two fields

    python3 -B chroma-engine/tools/t_aims2.py [ENGINE_DIR]
"""
import copy, os, sys
if len(sys.argv) > 1:
    os.environ["CHROMA_ENGINE"] = os.path.abspath(sys.argv[1])
import _engine
import numpy as np
import engine as E, batch
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS
import aims2 as A2
import foresee as FS

L = batch.load_batch("earth", packs=list(batch.PACKS))
PAR = dict(A2.PAR)
F0 = A2.compile_fields(L, PAR, E.C, E.NIDX, E.AIM_HEIGHTS)
NI = L["ROLES"]["NI"]
fails, notes = [], []


def make(N=2, player=(), par=None, F=None):
    """An agenda with a made-up life around it: money .6, time 1 (36 free hours), no partner, adults."""
    st = dict(r_ever=np.zeros((N, NI), bool), need=np.full((N, len(E.NIDX)), 0.5), gained=[], lost=[], events={0: []})
    ctx = dict(events=st["events"], r_gain=lambda n, i, how: st["gained"].append((n, i, how)),
               r_lose=lambda n, i, why: st["lost"].append((n, i, why)), r_ever=st["r_ever"],
               ev_cond=lambda c, ns: np.ones(N, bool), need=lambda: st["need"], WL=lambda: None, WON=lambda: False,
               ak=None, astr=None, NIDX=E.NIDX, MON=0, TIM=1, PAR=E.KIDX["partner"], CAR=E.KIDX["career"],
               KID=E.KIDX["children"], LOAD=np.array([c[1] for c in E.COMMITMENTS]), RID=L["ROLES"]["ID"],
               PARTNER=lambda n: False)
    p = dict(PAR, player=player, **(par or {}))
    ag = A2.Agenda(N, F if F is not None else F0, p, 11, ctx)
    st["res"] = np.tile([0.6, 1.0, 0.9, 0.4, 0.3], (N, 1)); st["held"] = np.zeros((N, E.NK), bool)
    st["w"] = np.full((N, E.C), 0.2); st["dead"] = np.zeros(N, bool)
    ag.w = st["w"]; ag.t = 30 * 52
    ag.account(st["res"], st["held"], np.zeros(N))
    return ag, st


def tick(ag, st, t):
    if t % 4 == 0:
        ag.month(t, None, st["res"], st["held"], np.zeros(ag.N))
    ag.put(t)
    ag.week(t, st["w"], st["need"], st["res"], st["dead"])


def field(shape, rungs=3):
    return next(i for i, nm in enumerate(F0["names"]) if A2.SHAPES[F0["shape"][i]] == shape and F0["nr"][i] >= rungs)


def patched(f, r, **kw):
    F = copy.deepcopy(F0)
    for k, v in kw.items():
        F[k][f, r] = v
    F["upkeep_any"] = bool((F["up_yrs"] > 0).any())
    return F


T0 = 30 * 52
# ---- A1: a window's exact last week
f = field("competition")
for pstop in (False, True):
    F = patched(f, 0, w_dyrs=1.0, w_pstop=pstop, outy=520.0, time=False)
    ag, st = make(F=F, player=(0,)); n = 0   # a player's life: no fork answers itself
    j = ag.add(n, f, T0)
    ag.set_pace(n, j, "active", 1.0, T0)
    close = int(ag.wclose[n, j])
    if close != T0 + 52:
        fails.append(f"A1 deadline week {close}, not {T0 + 52}")
    calls = []
    real = ag.outcome
    ag.outcome = lambda n_, j_, t_, chance=False: calls.append(t_) or False
    ag.forks[n].clear(); ag.fork[n, j] = -1
    ag.eff[n, j] = 0.0
    paused_wk = 0
    for t in range(T0, close + 30):
        if t == close - 10:
            ag.set_pace(n, j, "paused", None, t)
        if t == close - 4:
            ag.set_pace(n, j, "active", 1.0, t)
            ag.forks[n].clear(); ag.fork[n, j] = -1
        if t >= close - 10 and t < close - 4:
            paused_wk += 1
        if t == close - 1:
            ag.eff[n, j] = ag.need[n, j] + 1   # eligible from here on
        if t == close + 3:                    # toggling after the close never reopens it
            ag.set_pace(n, j, "paused", None, t); ag.set_pace(n, j, "active", 1.0, t)
        ag.forks[n].clear(); ag.fork[n, j] = -1
        tick(ag, st, t)
    told = [r for r in ag.log if r["what"] == "window closed"]
    if not pstop:
        if close not in calls or any(c > close for c in calls):
            fails.append(f"A1 tests at {sorted(set(calls))[-3:]}: the last week {close} must count, none after")
        if len(told) != 1 or told[0]["week"] != close + 1:
            fails.append(f"A1 the closing told {len(told)} times ({[r['week'] for r in told]}), not once at {close + 1}")
    else:
        if int(ag.wclose[n, j]) != close + paused_wk:
            fails.append(f"A1 pause_stops: the deadline at {int(ag.wclose[n, j])}, not {close + paused_wk}")
    ag.outcome = real
notes.append("A1 windows exact")

# ---- A2: an entry paid once
f = next(i for i in range(F0["F"]) if F0["entry"][i, 1] > 0 and F0["nr"][i] >= 3)
ag, st = make(player=(0,)); n = 0
j = ag.add(n, f, T0); ag.rung[n, j] = 1; ag.start_rung(n, j, T0)
ag.activate(n, j, 1.0, T0, pay=True)
for t, pace in ((T0 + 1, "paused"), (T0 + 2, "active"), (T0 + 3, "paused"), (T0 + 4, "active")):
    ag.set_pace(n, j, pace, 1.0 if pace == "active" else None, t)
if len(ag.entry_log[n]) != 1:
    fails.append(f"A2 entry charged {len(ag.entry_log[n])} times")
m0 = st["res"][n, 0]; tick(ag, st, T0 + 4); tick(ag, st, T0 + 5)
if not np.isclose(m0 - st["res"][n, 0], ag.entry_log[n][0]["amount"] * PAR["money_k"]):
    fails.append("A2 the entry not debited once from the money")
j2 = ag.add(n, f, T0, by=False)   # the same field again: the same slot, nothing new
if j2 != j:
    fails.append("A2 a field held twice")
ag2, st2 = make(player=(0,)); jr = ag2.add(0, f, T0); ag2.rung[0, jr] = 1; ag2.start_rung(0, jr, T0)
ag2._do(0, jr, "refuse", "pay", T0); ag2.set_pace(0, jr, "paused", None, T0 + 1); ag2.set_pace(0, jr, "active", 1.0, T0 + 2)
if ag2.entry_log[0]:
    fails.append("A2 a refused fee was charged")
notes.append("A2 entry once")

# ---- A3: a player's fork persists and blocks only its aim; a crowded queue
fa, fb = field("knowledge"), field("craft")
F = copy.deepcopy(F0); F["outy"][:] = 52.0; F["w_every"][:] = 0; F["w_dage"][:] = -1; F["w_dyrs"][:] = -1
ag, st = make(player=(0,), F=F); n = 0
ja = ag.add(n, fa, T0); jb = ag.add(n, fb, T0)
fka = next(x for x in ag.forks[n] if ja in x["aims"]); fkb = next(x for x in ag.forks[n] if jb in x["aims"])
if ag.apply(n, fkb["id"], "go_on" if "go_on" in fkb["options"] else "pay", T0):
    fails.append("A3 the player's answer refused")
ag.st[n, ja] = A2.ACTIVE; ag.inten[n, ja] = 1.0   # pursued, but its fork waits
ag.dirty = True
calls = []
ag.outcome = lambda n_, j_, t_, chance=False: calls.append((j_, t_)) or False
ag.need[n, ja] = ag.need[n, jb] = 0.2
for t in range(T0, T0 + 104):
    tick(ag, st, t)
    if t == T0 + 10:
        ag.apply(n, fka["id"], "later", t)
if not any(x["id"] == fka["id"] for x in ag.forks[n]):
    fails.append("A3 the player's fork was resolved without the player")
if ag.eff[n, ja] > ag.need[n, ja] + 1e-9:
    fails.append("A3 effort past the need while its fork waits")
if any(j_ == ja for j_, _ in calls):
    fails.append("A3 a test for the aim whose fork waits")
if not any(j_ == jb for j_, _ in calls) and not any(x["kind"] == "take" for x in ag.forks[n] if jb in x["aims"]):
    fails.append("A3 the other aim did not go on")
puts = [b for b in ag.burden if b.get("what") == "put"]
if len({b["week"] for b in puts}) != len(puts):
    fails.append("A3 more than one fork put in a week")
ag3, st3 = make(player=(0,)); fs3 = [i for i in range(F0["F"]) if F0["start"][i, 0] <= 30][:6]
for i in fs3:
    ag3.add(0, i, T0)
nf = len(ag3.forks[0])
for t in range(T0, T0 + 60):
    tick(ag3, st3, t)
pw = [b for b in ag3.burden if b.get("what") == "put"]
if len(ag3.forks[0]) != nf or nf < 5:
    fails.append(f"A3 crowded queue: {nf} forks made, {len(ag3.forks[0])} kept")
by_id = {}
for b in pw:
    by_id.setdefault(b["id"], []).append(b["week"])
if len(by_id) < nf or any(b - a < PAR["reask"] for ws in by_id.values() for a, b in zip(ws, ws[1:])):
    fails.append(f"A3 crowded queue: puts {by_id} (every fork put, an unchanged one not again within {PAR['reask']} weeks)")
notes.append(f"A3 {nf} forks kept, {len(pw)} puts in 60 weeks")

# ---- A4: effort alone reaches nothing
f = field("art")
F = copy.deepcopy(F0); F["outy"][f] = 0.0
ag, st = make(F=F); j = ag.add(0, f, T0); ag.set_pace(0, j, "active", 1.5, T0); ag.forks[0].clear(); ag.fork[0, j] = -1
ag.eff[0, j] = 10 * ag.need[0, j]
for t in range(T0, T0 + 200):
    tick(ag, st, t)
if ag.rung[0, j] != 0:
    fails.append("A4 a rung reached by effort alone")
st["r_ever"][0, F["ids"][f][0][:1]] = True   # a door title held: the demonstrated outcome
tick(ag, st, T0 + 200)
if ag.rung[0, j] != 1 or ag.worked[0, j, 0] != 1:
    fails.append("A4 the title held did not reach the rung (worked for)")
notes.append("A4 no rung from effort")

# ---- A5: learning kept in proportion
ag, st = make(); f = field("craft"); j = ag.add(0, f, T0); ag.set_pace(0, j, "active", 1.0, T0)
ag.forks[0].clear(); ag.fork[0, j] = -1
ag.eff[0, j] = 0.37 * ag.need[0, j]; tick(ag, st, T0)
l0 = float(ag.learned[0, j, 0]); ag.set_pace(0, j, "dropped"); [tick(ag, st, t) for t in range(T0 + 1, T0 + 60)]
if not (0.36 <= l0 <= 0.4) or ag.learned[0, j, 0] != l0:
    fails.append(f"A5 learning {l0:.2f} then {ag.learned[0, j, 0]:.2f} after a drop")
ag.add(0, f, T0 + 60)
if ag.st[0, j] != A2.HELD or ag.learned[0, j, 0] != l0:
    fails.append("A5 held again: not the same slot with its learning")
notes.append(f"A5 learning kept {l0:.2f}")

# ---- A6: the account: priority, an overfull week, shared preparation, the review
c1, c2 = [i for i in range(F0["F"]) if A2.SHAPES[F0["shape"][i]] == "competition"][:2]
ag, st = make(player=(0,), par=dict(time_floor=0.2)); st["res"][0, 1] = 0.0   # every hour held: about 7 free
ja, jb = ag.add(0, c1, T0), ag.add(0, c2, T0)
for j in (ja, jb):
    ag.st[0, j] = A2.ACTIVE; ag.inten[0, j] = 1.5
ag.set_priority(0, jb, 0); ag.account(st["res"], st["held"], np.zeros(1))
if not (ag.funded[0, jb] > ag.funded[0, ja]):
    fails.append("A6 the first in priority not funded first")
if not ag.syn[0, ja]:
    fails.append("A6 shared preparation (two competitions) not counted once")
want = (F0["hours"][c1, 0] + F0["hours"][c2, 0]) * 1.5
if not ag.committed["time"][0] < want:
    fails.append("A6 the shared hours counted twice")
for t in range(T0, T0 + 12):
    tick(ag, st, t)
S = dict(AIM2_ON=True, AG=ag, t=T0 + 12)
A = FS.agenda(S, 0)
if sorted(x["priority"] for x in A["items"]) != list(range(1, len(A["items"]) + 1)):
    fails.append("A6 agenda priorities not 1..n")
if not any(x["bottleneck"] and x["bottleneck"]["res"] in ("time", "fork") and x["funded"] < 1 for x in A["items"]) \
        or not A["capacity"]["time"]["committed"] > A["capacity"]["time"]["have"]:
    fails.append("A6 an underfunded aim shows no bottleneck, or the account does not show the overfull week")
grp = [fk for fk in ag.forks[0] if fk["grouped"]]
if len(grp) < 2:
    fails.append(f"A6 the forks wanting the same hours not grouped ({[(x['kind'], x['group']) for x in ag.forks[0]]})")
else:
    rv = FS.review(S, 0, grp[0]["id"])
    if not rv or len(rv["forks"]) < 2 or not rv["combos"] or not any(c["slower"] for c in rv["combos"]):
        fails.append("A6 the review lacks its forks or combinations")
    ch = {rv["forks"][0]["id"]: "pause"}
    out = FS.apply_review(S, 0, dict(choices=ch, set={}))
    if out["errors"] or any(x["id"] == rv["forks"][0]["id"] for x in ag.forks[0]) or not any(x["id"] == rv["forks"][1]["id"] for x in ag.forks[0]):
        fails.append("A6 apply_review: the answered fork not closed once, or the one left out not kept")
    pv = FS.preview(S, 0, ja)
    for k in ("needs", "cost", "hours", "overlaps", "window", "unknown", "exit"):
        if k not in pv:
            fails.append(f"A6 the preview has no {k}")
    if FS.set_pace(S, 0, ja, "fast") != "no such pace: fast":
        fails.append("A6 a wrong pace not refused in words")
notes.append(f"A6 funded {ag.funded[0, jb]:.2f} first, {ag.funded[0, ja]:.2f} second")

# ---- A7: selective upkeep
f = next(i for i in range(F0["F"]) if len(F0["ids"][i][0]) and F0["nr"][i] >= 3 and A2.SHAPES[F0["shape"][i]] == "craft")
F = patched(f, 0, up_yrs=1.0, up_of=2)
ag, st = make(F=F, player=(0,)); j = ag.add(0, f, T0); ag.set_pace(0, j, "active", 1.0, T0); ag.forks[0].clear(); ag.fork[0, j] = -1
st["r_ever"][0, F["ids"][f][0][0]] = True; tick(ag, st, T0)
ag.set_pace(0, j, "paused", None, T0 + 1)
for t in range(T0 + 1, T0 + 120):
    tick(ag, st, t)
lap = [r for r in ag.log if r["what"] == "upkeep lapsed"]
if len(lap) != 1 or not st["lost"] or ag.rung[0, j] != 1 or ag.worked[0, j, 0] < 0:
    fails.append(f"A7 credential: {len(lap)} lapses, {len(st['lost'])} lost, rung {ag.rung[0, j]}")
ag.set_pace(0, j, "active", 1.0, T0 + 120); ag.forks[0].clear(); ag.fork[0, j] = -1
for t in range(T0 + 120, T0 + 160):
    tick(ag, st, t)
if not any(r["what"] == "upkeep refreshed" for r in ag.log) or not any(h == "renewed" for _, _, h in st["gained"]):
    fails.append("A7 renewed use did not refresh the credential")
ag2, st2 = make(); j2 = ag2.add(0, f, T0); st2["r_ever"][0, F0["ids"][f][0][0]] = True; tick(ag2, st2, T0)
for t in range(T0 + 1, T0 + 400):
    tick(ag2, st2, t)
if any(r["what"] == "upkeep lapsed" for r in ag2.log):
    fails.append("A7 a rung with no upkeep lapsed")
notes.append("A7 upkeep selective")

# ---- A8: integrated assets
fa, fb = field("knowledge"), field("land")
tab = {(F0["names"][fa], F0["names"][fb]): dict(name="a field study", title="", opens="a study group asks for them")}
ag, st = make(par=dict(assets=tab, integrate_y=52.0))
ja, jb = ag.add(0, fa, T0), ag.add(0, fb, T0)
ag.rung[0, ja] = ag.rung[0, jb] = 1; ag.st[0, ja] = A2.ACTIVE; ag.fitf[0, :] = 1.25
for t in range(T0, T0 + 520, 4):
    ag.integrate(t)
    if t == T0 + 200:
        ag.set_pace(0, jb, "dropped"); ag.add(0, fb, t); ag.st[0, jb] = A2.PAUSED
if len(ag.assets[0]) != 1:
    fails.append(f"A8 {len(ag.assets[0])} assets for one pair")
ag2, st2 = make(par=dict(assets={}))
ja, jb = ag2.add(0, fa, T0), ag2.add(0, fb, T0); ag2.rung[0, [ja, jb]] = 2; ag2.st[0, ja] = A2.ACTIVE
ag2.month(T0, None, st2["res"], st2["held"], np.zeros(2))
if ag2.assets[0]:
    fails.append("A8 an asset with no table")
notes.append("A8 one asset per pair")

# ---- A11: the realm's assets: rungs, age and the gap between two
import realm_earth as RE_
fk_, fl_, fc_ = field("knowledge"), field("land"), field("competition")
lo_, hi_ = sorted(RE_.AIM_ASSETS[tuple(sorted(("knowledge", "land")))]["rungs"])
ag, st = make(par=dict(integrate_y=52.0))
ja, jb, jc = ag.add(0, fk_, 0), ag.add(0, fl_, 0), ag.add(0, fc_, 0)
ag.st[0, [ja, jb, jc]] = A2.ACTIVE; ag.fitf[0, :] = 1.25
ag.rung[0, [ja, jb, jc]] = max(lo_ - 1, 0)
for t in range(20 * 52, 24 * 52, 4):
    ag.t = t; ag.integrate(t)
n_low = len(ag.assets[0])
ag.rung[0, ja] = lo_; ag.rung[0, jb] = hi_; ag.rung[0, jc] = hi_
age_ok = True
for t in range(int(PAR["integrate_age"] - 3) * 52, int(PAR["integrate_age"]) * 52, 4):
    ag.t = t; ag.integrate(t)
age_ok = not ag.assets[0]
for t in range(int(PAR["integrate_age"]) * 52, int(PAR["integrate_age"]) * 52 + 104, 4):
    ag.t = t; ag.integrate(t)
first_ = list(ag.assets[0])
gap_ok = len(first_) == 1
w1 = first_[0]["week"] if first_ else 0
for t in range(w1 + 4, w1 + int(52 * PAR["integrate_gap"]) - 4, 4):
    ag.t = t; ag.integrate(t)
gap_ok &= len(ag.assets[0]) == 1
for t in range(w1 + int(52 * PAR["integrate_gap"]), w1 + int(52 * PAR["integrate_gap"]) + 208, 4):
    ag.t = t; ag.integrate(t)
if n_low:
    fails.append(f"A11 {n_low} assets from rungs below the realm's")
if not age_ok:
    fails.append("A11 an asset before integrate_age")
if not gap_ok:
    fails.append(f"A11 {len(ag.assets[0])} assets inside the gap")
if len(ag.assets[0]) < 2:
    fails.append("A11 no second asset after the gap")
elif not all("{" not in x["name"] and len(x["fields"]) == 2 for x in ag.assets[0]):
    fails.append("A11 an asset not named by its fields")
F_ = dict(F0); F_["assets_lib"] = {   # the Library's rows (<world>_aim_assets.py) over the realm's; a field pair first
    ("land", "knowledge"): dict(name="the Library's {a} with {b}", title="", opens="", rungs=(1, 1)),
    (F0["names"][fl_], F0["names"][fk_]): dict(name="{a}|{b}", title="", opens="", rungs=(1, 1))}
th_ = lambda f: F0["items"][f]["words"].get("thing") or F0["names"][f]
ag, st = make(par=dict(integrate_y=52.0), F=F_)
ja, jb = ag.add(0, fk_, 0), ag.add(0, fl_, 0); ag.st[0, [ja, jb]] = A2.ACTIVE; ag.fitf[0, :] = 1.25; ag.rung[0, [ja, jb]] = 1
if ag.asset_tab[("knowledge", "land")]["name"] != "the Library's {a} with {b}":
    fails.append("A11 the realm's row over the Library's")
for t in range(30 * 52, 34 * 52, 4):
    ag.t = t; ag.integrate(t)
if not ag.assets[0] or ag.assets[0][0]["name"] != f"{th_(fl_)}|{th_(fk_)}":
    fails.append(f"A11 the field pair not first, or not in the order written: {[x['name'] for x in ag.assets[0]]}")
notes.append(f"A11 realm assets ({len(RE_.AIM_ASSETS)} pairs) by rungs, age and gap, the Library's first")

# ---- A12: a spark from a reached rung
ag, st = make(par=dict(spark_rung=1.0))
fx_ = field("knowledge"); jx_ = ag.add(0, fx_, T0); ag.st[0, jx_] = A2.ACTIVE; ag.eff[0, jx_] = ag.need[0, jx_]
n0_ = int((ag.f[0] >= 0).sum()); ag.arrive(0, jx_, T0 + 4, "won a test")
new_ = [int(ag.f[0, j]) for j in np.nonzero(ag.f[0] >= 0)[0]][n0_:]
if len(new_) != 1:
    fails.append(f"A12 {len(new_)} aims sparked by one rung")
else:
    g_ = new_[0]
    if not ((F0["sph"][g_] == F0["sph"][fx_] and F0["sph"][g_] >= 0) or (F0["prep"][g_] & F0["prep"][fx_])):
        fails.append("A12 a spark far from the rung reached")
    if g_ == fx_:
        fails.append("A12 a spark of an aim already held")
ag2, st2 = make(par=dict(spark_rung=1.0, spark_max=1))
jy_ = ag2.add(0, fx_, T0); ag2.st[0, jy_] = A2.ACTIVE; ag2.eff[0, jy_] = ag2.need[0, jy_]
ag2.arrive(0, jy_, T0 + 4, "won a test")
if int((ag2.f[0] >= 0).sum()) != 1:
    fails.append("A12 a spark past spark_max")
notes.append("A12 a reached rung sparks one near aim")

# ---- A13: slots grow inside a step
ag, st = make(N=2, player=(0,), par=dict(spark_rung=1.0, spark_max=99))
fs13 = [i for i in range(F0["F"]) if F0["nr"][i] >= 3][:8]
for n_ in (0, 1):
    for f_ in fs13[:4]:
        j_ = ag.add(n_, f_, T0); ag.activate(n_, j_, 1.0, T0, pay=False); ag.eff[n_, j_] = ag.need[n_, j_]
st["r_ever"][:] = True   # every title held: rungs come through month()'s titles
ma0 = ag.MA; err13 = None
try:
    for t in range(T0 + 1, T0 + 120):
        for n_ in (0, 1):
            on_ = (ag.f[n_] >= 0) & (ag.st[n_] == A2.ACTIVE)
            ag.eff[n_, on_] = np.maximum(ag.eff[n_, on_], ag.need[n_, on_])
        tick(ag, st, t)
        if ag._depth or (ag.spark_q and not ag._depth):
            fails.append("A13 sparks left inside or after a step"); break
except Exception as e_:
    err13 = repr(e_)
if err13:
    fails.append(f"A13 {err13}")
elif ag.MA <= ma0:
    fails.append(f"A13 the slots never grew ({ag.MA})")
young_ = [(n_, j_) for n_ in (0, 1) for j_ in np.nonzero(ag.f[n_] >= 0)[0] if ag.t - ag.born[n_, j_] < PAR["stop_grace"]]
if len(ag.SM) and young_:
    st_ = [int(x) for x in ag.SM if ag.L_STOP[x]]
    if any(ag._fits(n_, int(j_), x) or ag._fits_fork(n_, int(j_), x) for n_, j_ in young_ for x in st_):
        fails.append("A13 a moment offering stop about an aim adopted within stop_grace")
notes.append(f"A13 slots grew {ma0} to {ag.MA} inside steps")

# ---- A9: views draw nothing
ag, st = make(player=(0,)); [ag.add(0, i, T0) for i in fs3[:3]]
S = dict(AIM2_ON=True, AG=ag, t=T0)
s0 = copy.deepcopy(ag.rng.bit_generator.state)
FS.agenda(S, 0); FS.preview(S, 0, F0["names"][fs3[0]]); FS.preview(S, 0, 0)
if ag.forks[0]:
    FS.review(S, 0, ag.forks[0][0]["id"])
if ag.rng.bit_generator.state != s0:
    fails.append("A9 a view drew from the agenda's stream")
notes.append("A9 views draw nothing")

# ---- A10: the money rule (Vision 10-23): a step's share is the least over the resources it needs; an incidental ask
# (money_min or less) never caps it; a step that needs money and has none waits, money named; an entry owed is not debited
f = field("craft")
F = copy.deepcopy(F0); F["money"][f, 0] = 0.01; F["entry"][f, 0] = 0.0; F["energy"][f, 0] = 0.0
ag, st = make(player=(0,), F=F); st["res"][0, 0] = 0.05   # no free money
j = ag.add(0, f, T0); ag.forks[0].clear(); ag.fork[0, j] = -1; ag.set_pace(0, j, "active", 1.0, T0)
ag.account(st["res"], st["held"], np.zeros(2))
if ag.funded[0, j] < 0.999:
    fails.append(f"A10 an incidental money ask capped the step ({ag.funded[0, j]:.2f})")
F["money"][f, 0] = 0.2; ag.account(st["res"], st["held"], np.zeros(2))
S = dict(AIM2_ON=True, AG=ag, t=T0)
it = next(x for x in FS.agenda(S, 0)["items"] if x["slot"] == j)
if ag.funded[0, j] != 0 or not it["bottleneck"] or it["bottleneck"]["res"] != "money":
    fails.append(f"A10 a step needing money with none: funded {ag.funded[0, j]:.2f}, bottleneck {it['bottleneck']}")
F["money"][f, 0] = 0.0; F["entry"][f, 0] = 0.3; ag.paid[0, j, 0] = False
m0 = st["res"][0, 0]; ag.activate(0, j, 1.0, T0, pay=True); tick(ag, st, T0 + 1)
if not ag.owed[0, j] or ag.entry_log[0] or st["res"][0, 0] != m0 or ag.funded[0, j] != 0:
    fails.append("A10 an entry that cannot be paid was charged, or the step went on without it")
st["res"][0, 0] = 0.9
for t in range(T0 + 4, T0 + 9):
    tick(ag, st, t)
if ag.owed[0, j] or len(ag.entry_log[0]) != 1:
    fails.append("A10 an owed entry not paid once it could be")
notes.append("A10 money rule")

print(("PASS" if not fails else "FAIL") + "  aims v2 scenarios: " + "; ".join(notes))
for x in fails:
    print("   ", x)
sys.exit(1 if fails else 0)
