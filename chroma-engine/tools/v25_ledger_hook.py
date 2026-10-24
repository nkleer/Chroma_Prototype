"""v25's ledger readers as a hook, for lives the caller runs or plays (Release's records/v25/checks.md reads CL0 and AM0
"on LA and SK": v25_ledger_run.py runs LA's lives with it; a played life, as heights_play.py plays it, uses it the same
way). The record is v25_ledger_run.py's file; v25_ledger_judge.py reads it. Test only: nothing is drawn, the lives are
the run's own.

    import v25_ledger_hook as H        # with the engine to check first on sys.path (the game's engine_pin for SK)
    H.install()                        # before the life runs: wraps world_react.React and aims2.Agenda in this process
    o = ...                            # run or play it (E.run, E.run_steps, the Game: its result)
    rec = H.record(o, L)               # L: the Library it ran on; head={...} puts fields first (seed, preset, policy)
    json.dump(rec, open(out, "w"))

A life the game plays: its player lives (aims2_par player, the game's (0,)) are read from the agenda itself, and their
forks are the player's: AM0 then checks that none was resolved for them, and leaves their open forks alone. When the
character died before the end (the game keeps no result: o None), the record is read from the react and agenda objects
the hook saw, without the colours, heights and national parts. reset() clears what was read, for a next life in the
same process. What each row reads is in v25_ledger_run.py's docstring.
"""
import json

import numpy as np

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


CNT = dict(puts=0, answered=0, merged_pairs=0, settled_first=0, deadline_week=0, paused_close=0, arrived=0, title_after_close=0)
CL = dict(puts=[])   # every clash put: (life, week, key, dispute id, n_asked)
AG_REC = dict(arr=[])   # every arrival: (life, slot, field, rung reached, years on the rung, share of them kept at, week,
#                         the years the life's own clock stated at the rung's start: aims2.Agenda.clock's typical, or None)

INST = {}        # the React and Agenda objects of the last life (their output() when the run has no result)
PLAYERS = set()  # the lives the agenda waits on a player for (aims2_par player)
_INSTALLED = [False]


def _clock(s, n, j):
    """AM2: the years the aim's preview states for this life on its current rung (aims2.Agenda.clock's typical), None
    where the rung has no clock (it comes with time, or no effort can be made) or the agenda has none."""
    ck = s.clock(int(n), int(j)) if hasattr(s, "clock") else None
    return None if ck is None else float(ck[0])


def _WR():
    import world_react
    return world_react


def _A2():
    import aims2
    return aims2


def reset():
    """Clear what was read (violations, counts, puts, arrivals, the objects), for a next life in this process."""
    V.clear(); VN.clear(); INST.clear(); PLAYERS.clear(); CL["puts"].clear(); AG_REC["arr"].clear()
    for k_ in CNT:
        CNT[k_] = 0
    _seen.clear()


_seen = {}      # (life, dispute id) -> (sig, holders) at its last put


def install():
    """Wrap world_react.React (_clash_check, _clash_apply) and aims2.Agenda (week, month, moments) in this process, to
    look only. Once a process."""
    if _INSTALLED[0]:
        return
    _INSTALLED[0] = True
    WR = _WR(); A2 = _A2()
    _cc0 = WR.React._clash_check
    _ap0 = WR.React._clash_apply

    def _sigof(d):
        return json.dumps(d.get("sig")), frozenset(int(h) if isinstance(h, (int, np.integer)) else str(h) for h in d["holders"])

    def _cc(self, t, age, dd, ctx):
        INST["react"] = self
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
        twice = "answer" in rec   # (its answer completes the record: a record already answered is answered again;
        # not by id(rec), which a later record can reuse once an answered one is let go)
        rs = _ap0(self, t, age, n, dsp, sub, r_or_family, by_player, ctx, rec, gia, succ=succ)
        CNT["answered"] += 1
        if twice:
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
        return dict(wclose=s.wclose.copy(), st=s.st.copy(), rung=s.rung.copy(), f=s.f.copy(), wround=s.wround.copy(),
                    nlog=len(s.log))

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
        # arrivals: never after the window closed without a way round; in the closing week they count. A title of
        # theirs held, gained through the world's own rules, is a demonstrated outcome, not the window's (decisions:
        # "distinguish effort-based progress, external windows and demonstrated outcomes"): read, counted apart
        up = same & (s.rung > rg0)
        tr = getattr(s, "_lg", None)
        how = {(x["life"], x["slot"]): x.get("how") for x in s.log[pre["nlog"]:] if x["what"] == "arrived"}
        for n, j in zip(*np.nonzero(up)):
            CNT["arrived"] += 1
            if wc0[n, j] >= 0 and t > wc0[n, j] and not wr0[n, j]:
                if how.get((int(n), int(j))) == "its title held":
                    CNT["title_after_close"] += 1
                else:
                    bad("AM0", "a rung reached after its window closed", n, t, field=F["names"][int(s.f[n, j])],
                        rung=int(rg0[n, j]), closed=int(wc0[n, j]), how=how.get((int(n), int(j))))
            if wc0[n, j] >= 0 and t == wc0[n, j]:
                CNT["deadline_week"] += 1
            if tr is not None:
                k = (int(n), int(j)); t0, kw, tw = tr.get(k, (None, 0, 0))
                if t0 is not None:
                    AG_REC["arr"].append((int(n), int(j), F["names"][int(s.f[n, j])], int(rg0[n, j]), round((t - t0) / 52.0, 2),
                                          round(kw / max(tw, 1), 3), int(t), s._ck.get(k)))
                tr[k] = (int(t), 0, 0); s._ck[k] = _clock(s, n, j)   # the next rung's own clock, as its preview states

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
        INST["agenda"] = s; PLAYERS.update(int(x) for x in s.player)
        pre = _snap(s)
        r = _wk0(s, t, *a, **k)
        _after(s, int(t), pre)
        if not hasattr(s, "_lg"):
            s._lg = {}; s._ck = {}
        if t % 4 == 0:
            fd = getattr(s, "funded", None)
            on = (s.f >= 0) & (s.rung < s.F["nr"][np.maximum(s.f, 0)])
            kept = on & (s.st == ACTIVE) & ((fd > 0) if fd is not None and fd.shape == s.st.shape else True)
            for n, j in zip(*np.nonzero(on)):
                k_ = (int(n), int(j)); t0, kw, tw = s._lg.get(k_, (int(t), 0, 0))
                s._lg[k_] = (t0, kw + int(kept[n, j]), tw + 1)
                if k_ not in s._ck:   # first seen on this rung: its clock from here
                    s._ck[k_] = _clock(s, n, j)
        return r
    A2.Agenda.week = _week
    _wrap("month", 0)
    _wrap("moments", 4)


def record(o, L, head=None, base=False, players=()):
    """The ledger record of the life or lives just run: o the run's output (None: a played character who died before
    the end), L the Library, head the fields put first, base True for LB's lives (no v25 records: colours, heights and
    deaths only), players lives whose forks are a player's beside those the agenda names."""
    import engine as E
    if o is None:
        o = {}
    res = dict(head or {})
    ag_ = INST.get("agenda")
    N = len(o["W_hist"][0]) if o.get("W_hist") is not None else len(ag_.forks) if ag_ is not None else 0
    if o.get("W_hist") is not None:
        Wh = np.asarray(o["W_hist"], float)   # (years + 1, N, 5)
        AGES = (18, 20, 30, 40, 50, 70)
        died = np.full(N, np.inf)   # o["died"]: (life, week, cause) for each death in the run
        for d_ in o.get("died") or []:
            died[int(d_[0])] = min(died[int(d_[0])], int(d_[1]) / 52.0)
        res.update(w={a: Wh[a].round(4).tolist() for a in AGES if a < len(Wh)},
                   died=[None if not np.isfinite(x) else round(float(x), 2) for x in died])
        lead = Wh.argmax(2)                                   # (years + 1, N)
        res["lead_changes18"] = [int((lead[19:, n] != lead[18:-1, n]).sum()) if len(lead) > 19 else 0 for n in range(N)]
        step = np.abs(np.diff(Wh, axis=0)).sum(2)             # each year's colour change (L1)
        res["change_20_40"] = step[20:40].sum(0).round(4).tolist() if len(step) >= 40 else None
        res["change_all"] = step.sum(0).round(4).tolist()
        if isinstance(o.get("heights"), dict):
            res["ht_names"] = list(o["heights"]["names"]); res["ht_week"] = np.asarray(o["heights"]["week"]).tolist()
    if not base:
        rx = o.get("react") or (INST["react"].output() if "react" in INST else {}); cl = rx.get("clash") or {}
        CD = _WR().CLASH_DEFAULT
        res["clash"] = dict(stats={k: _js(v) for k, v in cl.items() if k not in ("weeks", "moments", "blocked")},
                            weeks=_js(cl.get("weeks")), moments=_js(cl.get("moments")),
                            thr=float(CD["thr"]), ceilings=dict(sphere_yrs=CD["sphere_yrs"], decade_n=CD["decade_n"],
                                                                young_age=CD["young_age"], young_w=CD["young_w"]))
        for n, ms in enumerate(cl.get("moments") or []):   # one clash moment a week at most
            wk = [int(m[0]) if isinstance(m, (list, tuple)) else int(m) for m in ms]
            if len(wk) != len(set(wk)):
                bad("CL0", "two clash moments in one week", n, -1, weeks=sorted(wk))
        unanswered = sum(1 for d in sum(rx.get("disputes") or [], []) if d.get("family") is None)
        res["clash"]["unanswered_at_end"] = unanswered
        ag = o.get("aims2") or (INST["agenda"].output() if "agenda" in INST else {})
        log = ag.get("log") or []
        players = set(PLAYERS) | set(int(x) for x in players)
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
            if what == "decided" and r.get("by") == "character" and n in players:
                bad("AM0", "a player's fork resolved for them", n, r["week"], kind=r.get("kind"))
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
            A2 = _A2(); FF = A2.compile_fields(L, dict(A2.PAR), E.C, E.NIDX, E.AIM_HEIGHTS)
            res["clocks"] = {nm: [[round(float(FF["ymed"][f, r]), 2), round(float(FF["share"][f, r]), 3)] for r in range(int(FF["nr"][f]))]
                             for f, nm in enumerate(FF["names"])}
        except Exception as e_:   # noqa: BLE001
            res["clocks"] = None; res["clocks_error"] = repr(e_)
        res["counts"] = CNT; res["cl_puts"] = CL["puts"]
    res["violations"] = V; res["violation_counts"] = {f"{r}|{c}": n for (r, c), n in VN.items()}
    return _js(res)
