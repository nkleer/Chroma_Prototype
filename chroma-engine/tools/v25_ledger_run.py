"""v25's ledger readers on engine lives (Release's records/v25/checks.md): the mandatory CL0 (clash logic), AM0 (aim logic)
and NR1 (the fifteen national routes), with CL1, CL3, AM2, F5, RE3 and WA8n's rates read from the same lives. One seed a
call; v25_ledger_judge.py pools the seeds and gives one line a row.

    python3 -B chroma-engine/tools/v25_ledger_run.py <tree> <seed> <N> <years> <out.json> [--base] [--nat-test]

<tree> is a repository checkout (its chroma-engine/v22-speedpass, chroma-library and chroma-packs are run). The lives are
LA's: Earth with its packs, the outer world on, the shipped set (engine.SHIP_V25 over DEFAULT, batch.SHIP_V25_BATCH set
before the Library loads), every *_par as in code, no player. One core.
  --base       LB: the tree's DEFAULT with the world on, nothing laid over (the round 0 base, head 10, for RE3). The v25
               records are then absent and only the colours, heights and deaths are written.
  --nat-test   NR1's targeted lives: the shipped set with the national climb's yearly odds at .5 for each kind and its
               wider step after 1 year at rung 4 (wa_nat_par base .5, rung_years 1; a test setting, never shipped), so
               that every route a life can stand on is drawn. Its file is marked nat_test; the judge reads it for NR1 only.

What is read, and how (no draw is added, so the lives are LA's own; the readers wrap world_react.React and aims2.Agenda
methods in this process and only look):
  CL0  every clash put (React._clash_check): its demand has stakes of the life's own (an aim, a commitment, its time or a
       need) at the clash threshold or more, never colour alone; no dispute put again with nothing changed (the same
       stakes and dependence and no new holder), and no new dispute on a settled one's stake with nothing changed; two
       demands on one stake with purposes as alike as clash_par merge_cos, put the same week, are one dispute (while the
       first is open); every clash answered (React._clash_apply) once, its demand and stakes on its record; at most one
       clash moment a week (a clash moment takes the week's moment, an optional ask, and adds none: an unplayed life has
       no other asks).
  AM0  over every life's agenda (aims2's log, entries and wrapped steps): a rung is reached only by a demonstrated
       outcome (a test, a contest or chance won, a title held), never by effort alone; rungs come in order; a window
       that closed is told once; no arrival after its window closed without a way round, and arrivals in the closing
       week counted (they count); a pause never moves a deadline unless the rung says pause_stops; an entry paid once a
       slot and rung; an integrated asset once a pair; an unattended life's forks resolved only by its own pick (the
       declared policy) and a player's never (with --players none are). The save, load and queue cases are SC1's.
  NR1  the national log: each route reached, by which kind and life, and the national decisions those lives took while
       Known (world answers' ledger), which is the route's asset in use.
  CL1, CL3, AM2, F5, RE3, WA8n: the clash weeks, the agenda's rung clocks, colours by year, heights, national lives.
"""
import json
import os
import sys
import time

argv = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(argv) != 5:
    sys.exit(__doc__)
TREE, SEED, N, YEARS, OUT = os.path.abspath(argv[0]), int(argv[1]), int(argv[2]), int(argv[3]), os.path.abspath(argv[4])
BASE = "--base" in sys.argv; NAT_TEST = "--nat-test" in sys.argv
ENG = os.path.join(TREE, "chroma-engine", "v22-speedpass")
sys.path.insert(0, ENG)
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np   # noqa: E402
import engine as E, batch   # noqa: E402
batch.LIB_DIR = os.path.join(TREE, "chroma-library"); batch.PACK_DIR = os.path.join(TREE, "chroma-packs")

V = []   # violations: (row, case, life, week, detail); the first few of each case are kept whole, every one counted
VN = {}
KEEP = 20


def bad(row, case, n, t, **d):
    k = (row, case); VN[k] = VN.get(k, 0) + 1
    if VN[k] <= KEEP:
        V.append(dict(row=row, case=case, life=int(n), week=int(t), **{k_: _js(v_) for k_, v_ in d.items()}))


def _js(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, (list, tuple)):
        return [_js(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _js(x) for k, x in v.items()}
    return v


CNT = dict(puts=0, answered=0, merged_pairs=0, settled_first=0, deadline_week=0, paused_close=0, arrived=0)
CL = dict(puts=[])   # every clash put: (life, week, key, dispute id, n_asked)
AG_REC = dict(arr=[])   # every arrival: (life, slot, field, rung reached, years on the rung, share of them kept at, week)

if not BASE:
    import world_react as WR
    import aims2 as A2

    _cc0 = WR.React._clash_check
    _ap0 = WR.React._clash_apply
    _seen = {}      # (life, dispute id) -> (sig, holders) at its last put
    _answers = {}   # id(record) -> times answered

    def _sigof(d):
        return json.dumps(d.get("sig")), frozenset(int(h) if isinstance(h, (int, np.integer)) else str(h) for h in d["holders"])

    def _cc(self, t, age, dd, ctx):
        pre = [len(x) for x in self.demands]
        npre = [len(x) for x in self.cl_wk]
        hold = _cc0(self, t, age, dd, ctx)
        cp = self.cp; M = self.M
        by_n = {}
        for i in np.nonzero(hold)[0]:
            n = int(dd["nd"][i])
            v = dict(aim=float(dd["aim_conf"][i]), commit=float(dd["com_conf"][i]), time=float(dd["time_conf"][i]),
                     need=float(dd["need_conf"][i]))
            given = dd["forced"].get(i, {}).get("stakes") is not None
            if max(v.values()) <= 0 and not given:
                bad("CL0", "no stake of its own (colour alone)", n, t, conflicts=v, stakes=float(dd["stakes"][i]))
            if float(dd["stakes"][i]) < cp["thr"] - 1e-9:
                bad("CL0", "stakes under the clash threshold", n, t, stakes=float(dd["stakes"][i]), thr=cp["thr"])
            by_n.setdefault(n, []).append(int(i))
        for n, is_ in by_n.items():   # connected demands (one stake, purposes alike) in one dispute
            recs = self.demands[n][pre[n]:]
            def dsp_of(i):
                kn = dd["kn"][i]; j = int(dd["jd"][i]); pl = j if j < M else -1
                for r in recs:
                    if r.get("clash") is not None and r["source"]["key"] == kn and r["source"]["place"] == pl:
                        return r["clash"]
                return None
            keys = {i: tuple(self._stake_key(dd, i)) for i in is_}
            for a in range(len(is_)):
                for b in range(a + 1, len(is_)):
                    i, i2 = is_[a], is_[b]
                    if keys[i] != keys[i2] or int(dd["jd"][i]) == int(dd["jd"][i2]):
                        continue
                    pu, pv = np.asarray(dd["purpose"][i], float), np.asarray(dd["purpose"][i2], float)
                    cos = float(pu @ pv) / max(np.linalg.norm(pu) * np.linalg.norm(pv), 1e-9)
                    if cos < cp["merge_cos"]:
                        continue
                    CNT["merged_pairs"] += 1
                    d1, d2 = dsp_of(i), dsp_of(i2)
                    if d1 is not None and d2 is not None and d1 != d2:
                        first = next((d for d in self.disputes[n] if d["id"] == min(d1, d2)), None)
                        if first is not None and first.get("open"):
                            bad("CL0", "connected demands put as two disputes", n, t, disputes=[d1, d2], key=keys[i], cos=round(cos, 3))
                        else:
                            CNT["settled_first"] += 1
        for n in range(len(self.cl_wk)):   # what was put: never again with nothing changed
            if len(self.cl_wk[n]) == npre[n]:
                continue
            for d in self.disputes[n]:
                if d.get("last_asked") != int(t):
                    continue
                CNT["puts"] += 1; CL["puts"].append((n, int(t), list(d["key"]), int(d["id"]), int(d["n_asked"])))
                cur = _sigof(d)
                prev = _seen.get((n, d["id"]))
                if prev is not None and prev[0] == cur[0] and prev[1] == cur[1]:
                    bad("CL0", "an unchanged dispute put again", n, t, dispute=d["id"], key=d["key"])
                if prev is None and d["n_asked"] == 1:   # a new dispute on a settled one's stake, nothing changed
                    olds = [d0 for d0 in self.disputes[n] if d0["id"] < d["id"] and d0["key"] == d["key"]]
                    if olds and not olds[-1].get("open"):
                        p0 = _seen.get((n, olds[-1]["id"]))
                        if p0 is not None and p0[0] == cur[0] and cur[1] <= p0[1]:
                            bad("CL0", "a settled dispute put again as new", n, t, dispute=d["id"], was=olds[-1]["id"], key=d["key"])
                _seen[(n, d["id"])] = cur
        return hold

    def _ap(self, t, age, n, dsp, sub, r_or_family, by_player, ctx, rec, gia, succ=None):
        rs = _ap0(self, t, age, n, dsp, sub, r_or_family, by_player, ctx, rec, gia, succ=succ)
        k = id(rec); _answers[k] = _answers.get(k, 0) + 1; CNT["answered"] += 1
        if _answers[k] > 1:
            bad("CL0", "a clash answered twice", n, t, dispute=dsp["id"])
        if rec.get("demand") is None:
            bad("CL0", "a clash with no demand on its record", n, t, dispute=dsp["id"])
        st = rec.get("stakes") or {}
        if not (st.get("aims") or st.get("needs") or st.get("commitments") or st.get("means") or st.get("key", [None])[0] == "given"):
            bad("CL0", "a clash whose record names nothing at stake", n, t, dispute=dsp["id"], stakes=st)
        return rs

    WR.React._clash_check = _cc
    WR.React._clash_apply = _ap

    PAUSED = A2.PAUSED; ACTIVE = A2.ACTIVE

    def _pad(a, shape, fill):
        if a.shape == shape:
            return a
        out = np.full(shape, fill, a.dtype); out[tuple(slice(0, k) for k in a.shape)] = a
        return out

    def _snap(s):
        return dict(wclose=s.wclose.copy(), st=s.st.copy(), rung=s.rung.copy(), f=s.f.copy(), wround=s.wround.copy())

    def _after(s, t, pre):
        sh = s.rung.shape
        wc0, st0, rg0, f0, wr0 = (_pad(pre[k], sh, v) for k, v in (("wclose", -1), ("st", 0), ("rung", 0), ("f", -1), ("wround", False)))
        same = (s.f == f0) & (f0 >= 0)
        F = s.F
        # a pause never moves a deadline unless the rung says pause_stops
        mv = same & (s.rung == rg0) & (wc0 >= 0) & (s.wclose != wc0) & (st0 == PAUSED)
        for n, j in zip(*np.nonzero(mv)):
            f, r = int(s.f[n, j]), int(min(s.rung[n, j], F["nr"][int(s.f[n, j])] - 1))
            if not (bool(F["w_pstop"][f, r]) and float(F["w_dyrs"][f, r]) >= 0):
                bad("AM0", "a pause moved a deadline", n, t, field=F["names"][f], rung=r, was=int(wc0[n, j]), now=int(s.wclose[n, j]))
        # arrivals: never after the window closed without a way round; in the closing week they count
        up = same & (s.rung > rg0)
        tr = getattr(s, "_lg", None)
        for n, j in zip(*np.nonzero(up)):
            CNT["arrived"] += 1
            if wc0[n, j] >= 0 and t > wc0[n, j] and not wr0[n, j]:
                bad("AM0", "a rung reached after its window closed", n, t, field=F["names"][int(s.f[n, j])], rung=int(rg0[n, j]),
                    closed=int(wc0[n, j]))
            if wc0[n, j] >= 0 and t == wc0[n, j]:
                CNT["deadline_week"] += 1
            if tr is not None:
                k = (int(n), int(j)); t0, kw, tw = tr.get(k, (None, 0, 0))
                if t0 is not None:
                    AG_REC["arr"].append((int(n), int(j), F["names"][int(s.f[n, j])], int(rg0[n, j]), round((t - t0) / 52.0, 2),
                                          round(kw / max(tw, 1), 3), int(t)))
                tr[k] = (int(t), 0, 0)

    def _wrap(name, targ):
        f0 = getattr(A2.Agenda, name)

        def w(s, *a, **k):
            t = a[targ] if len(a) > targ else k.get("t")
            pre = _snap(s)
            r = f0(s, *a, **k)
            _after(s, int(t), pre)
            return r
        setattr(A2.Agenda, name, w)

    _wk0 = A2.Agenda.week

    def _week(s, t, *a, **k):   # the rung clocks for AM2: weeks on each slot's rung, and those kept at (active, funded)
        pre = _snap(s)
        r = _wk0(s, t, *a, **k)
        _after(s, int(t), pre)
        if not hasattr(s, "_lg"):
            s._lg = {}
        if t % 4 == 0:
            fd = getattr(s, "funded", None)
            on = (s.f >= 0) & (s.rung < s.F["nr"][np.maximum(s.f, 0)])
            kept = on & (s.st == ACTIVE) & ((fd > 0) if fd is not None and fd.shape == s.st.shape else True)
            for n, j in zip(*np.nonzero(on)):
                k_ = (int(n), int(j)); t0, kw, tw = s._lg.get(k_, (int(t), 0, 0))
                s._lg[k_] = (t0, kw + int(kept[n, j]), tw + 1)
        return r
    A2.Agenda.week = _week
    _wrap("month", 0)
    _wrap("moments", 4)

PX = {}
if BASE:
    P = dict(E.DEFAULT)
else:
    for k_, v_ in E.SHIP_V25_BATCH.items():
        setattr(batch, k_, v_)
    P = dict(E.DEFAULT); P.update(E.SHIP_V25)
    if NAT_TEST:
        P["wa_nat_par"] = dict(base=dict(recognition=0.5, influence=0.5, authority=0.5), rung_years=1)
P["world"] = True
L = batch.load_batch("earth", packs=list(batch.PACKS))
t0 = time.time()
o = E.run(N=N, years=YEARS, seed=SEED, lib=L, P=P)
secs = round(time.time() - t0, 1)

Wh = np.asarray(o["W_hist"], float)   # (years + 1, N, 5)
AGES = (18, 20, 30, 40, 50, 70)
died = np.full(N, np.inf)   # o["died"]: (life, week, cause) for each death in the run
for d_ in o.get("died") or []:
    died[int(d_[0])] = min(died[int(d_[0])], int(d_[1]) / 52.0)
res = dict(tree=TREE, seed=SEED, N=N, years=YEARS, base=BASE, nat_test=NAT_TEST, secs=secs,
           engine_md5=__import__("hashlib").md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12],
           w={a: Wh[a].round(4).tolist() for a in AGES if a < len(Wh)},
           died=[None if not np.isfinite(x) else round(float(x), 2) for x in died])
lead = Wh.argmax(2)                                   # (years + 1, N)
res["lead_changes18"] = [int((lead[19:, n] != lead[18:-1, n]).sum()) if len(lead) > 19 else 0 for n in range(N)]
step = np.abs(np.diff(Wh, axis=0)).sum(2)             # each year's colour change (L1)
res["change_20_40"] = step[20:40].sum(0).round(4).tolist() if len(step) >= 40 else None
res["change_all"] = step.sum(0).round(4).tolist()
if isinstance(o.get("heights"), dict):
    res["ht_names"] = list(o["heights"]["names"]); res["ht_week"] = np.asarray(o["heights"]["week"]).tolist()

if not BASE:
    rx = o.get("react") or {}; cl = rx.get("clash") or {}
    res["clash"] = dict(stats={k: _js(v) for k, v in cl.items() if k not in ("weeks", "moments", "blocked")},
                        weeks=_js(cl.get("weeks")), moments=_js(cl.get("moments")),
                        thr=float(WR.CLASH_DEFAULT["thr"]), ceilings=dict(sphere_yrs=WR.CLASH_DEFAULT["sphere_yrs"],
                                                                          decade_n=WR.CLASH_DEFAULT["decade_n"],
                                                                          young_age=WR.CLASH_DEFAULT["young_age"],
                                                                          young_w=WR.CLASH_DEFAULT["young_w"]))
    for n, ms in enumerate(cl.get("moments") or []):   # one clash moment a week at most
        wk = [int(m[0]) if isinstance(m, (list, tuple)) else int(m) for m in ms]
        if len(wk) != len(set(wk)):
            bad("CL0", "two clash moments in one week", n, -1, weeks=sorted(wk))
    unanswered = sum(1 for d in sum(rx.get("disputes") or [], []) if d.get("family") is None)
    res["clash"]["unanswered_at_end"] = unanswered
    ag = o.get("aims2") or {}
    log = ag.get("log") or []
    players = set()
    last = {}; closed = {}; ints = {}
    for r in log:   # AM0 over the log
        n, j, what = r["life"], r["slot"], r["what"]; k = (n, j)
        if last.get(k, (None,))[0] != r["field"]:
            last[k] = (r["field"], r["rung"])
        if what == "arrived":
            how = str(r.get("how", ""))
            if not (how.startswith("won ") or how == "its title held"):
                bad("AM0", "a rung reached by effort alone", n, r["week"], field=r["field"], rung=r["rung"], how=how)
            if r["rung"] != last[k][1]:
                bad("AM0", "a rung reached out of order", n, r["week"], field=r["field"], rung=r["rung"], was=last[k][1])
            last[k] = (r["field"], r["rung"] + 1)
        else:
            last[k] = (r["field"], r["rung"])
        if what == "window closed":
            kk = (n, j, r["field"], r["rung"]); closed[kk] = closed.get(kk, 0) + 1
            if closed[kk] > 1:
                bad("AM0", "a window's closing told twice", n, r["week"], field=r["field"], rung=r["rung"])
            if r.get("state") == "paused":
                CNT["paused_close"] += 1
        if what == "decided" and r.get("by") != "character" and n not in players:
            bad("AM0", "an unattended life's fork resolved by other than its own pick", n, r["week"], by=r.get("by"), kind=r.get("kind"))
        if what == "fork" and n not in players:
            bad("AM0", "an unattended life's fork left waiting", n, r["week"], kind=r.get("kind"))
        if what == "integrated asset":
            kk = (n, tuple(sorted(r.get("pair") or ()))); ints[kk] = ints.get(kk, 0) + 1
            if ints[kk] > 1:
                bad("AM0", "an integrated asset given twice", n, r["week"], pair=r.get("pair"))
    for n, es in enumerate(ag.get("entries") or []):
        seen = {}
        for e in es:
            kk = (e["field"], e["rung"]); seen[kk] = seen.get(kk, 0) + 1
            if seen[kk] > 1:
                bad("AM0", "an entry cost paid twice", n, e["week"], field=e["field"], rung=e["rung"])
    for n, fl in enumerate(ag.get("open_forks") or []):
        if fl and n not in players:
            bad("AM0", "an unattended life's fork open at the end", n, -1, forks=fl)
    res["aims2"] = dict(log_n=len(log), arrivals=AG_REC["arr"], decisions=ag.get("decisions"),
                        burden=len(ag.get("burden") or []))
    nat = o.get("national") or {}
    res["national"] = dict(log=_js(nat.get("log") or []), ever=_js(nat.get("ever") or []))
    wl = o.get("wa_ledger") or {}
    nd_ = np.zeros(N, int); ns_ = np.zeros(N, int)
    for d_ in wl.get("decisions") or []:   # decisions taken at national standing, and those pushing at the nation's scope
        nd_[int(d_["n"])] += bool(d_.get("national")); ns_[int(d_["n"])] += d_.get("scope") == "nation"
    res["wa"] = [dict(decisions=x.get("decisions"), known_weeks=x.get("known_weeks"), national=int(nd_[n]), nation=int(ns_[n]))
                 for n, x in enumerate(wl.get("lives") or [])]
    import sphere_data as SD
    res["routes"] = [r_["key"] for r_ in SD.WORLD_FIT["national"]["routes"]]
    # AM2's stated clocks: the field's typical years and its share who make it, by field and rung
    try:
        FF = A2.compile_fields(L, dict(A2.PAR), E.C, E.NIDX, E.AIM_HEIGHTS)
        res["clocks"] = {nm: [[round(float(FF["ymed"][f, r]), 2), round(float(FF["share"][f, r]), 3)] for r in range(int(FF["nr"][f]))]
                         for f, nm in enumerate(FF["names"])}
    except Exception as e_:   # noqa: BLE001
        res["clocks"] = None; res["clocks_error"] = repr(e_)
    res["counts"] = CNT; res["cl_puts"] = CL["puts"]

res["violations"] = V; res["violation_counts"] = {f"{r}|{c}": n for (r, c), n in VN.items()}
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f_:
    json.dump(_js(res), f_)
print(f"{OUT}: seed {SEED}, {N} lives x {YEARS} years in {secs} s; "
      + ("base" if BASE else f"{CNT['puts']} clashes put, {CNT['answered']} answered, {CNT['arrived']} rungs reached, "
         f"{sum(VN.values())} violations ({len(VN)} kinds)"))
