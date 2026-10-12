"""v22.5 rows K9 (F8) and K18 (F7, F10) of records/v22.5/scope.md: retirement ends work, one roll of the living, once
means once. Three checks, one results line each, on lives with their switch on and every other switch as DEFAULT (the
refit's settings on the record's commit):

  f8_after   (F8, retire_ends) Earth with the live packs, the outer world on as presets 1 to 4 play it, every week of
             every life read through engine.run_steps():
               F8.1  no work moment (a moment whose life tag is work or which is set at an employer, not a door back:
                     an option that starts a career) in a week spent retired and not working, in a life that did
                     not go back to work                                                                  0 weeks
               F8.2  the same in any life (after a later retirement too)                                  0 weeks
             Reported: lives that retired and went back; jobs taken while retired without a career pick that week.
  f10_once   (F10, the engine's world_only; the game's line_wait and news_touch)
               F10.1 a once-a-life moment (once:, not once per commitment or per title; a child version counts with its
                     original) comes at most once in a life (the lives of f8_after)                       0 lives
               F10.2 a world moment (the outer world's own, WL.wm_s: elections, takeovers, leaks, rebuilding) comes
                     only in a week the world brought it (its event, forced that week)                    0 weeks
               F10.3 played lives, presets 1 to 6: a line of the kinds line_wait holds is not said again word for
                     word inside line_wait years (5 when the game has none)                               0 lines
               F10.4 played lives: national news (not their own place's, a war, a pandemic or a recession) is not
                     told before news_age, the same kind (a government's fall with its election) not twice inside
                     news_gap years, a law not told again while it stands as last told                    0 lines
  f7_roll    (F7, one_roll) played lives, presets 1 to 6, to the end of each life:
               F7.1  no line names a person after the week of their death, except where the story tells of the dead
                     (the death itself, the dead slot of grief and memory, the quiet deaths)              0 lines
               F7.2  no line names a person the outer world lost 13 or more weeks before                  0 lines
               F7.3  no line names a child of theirs while the engine counts no living child (unborn)     0 lines
               F7.4  a birth named once: each child's birth told in one week; every birth scene ("a child is born")
                     has its newborn                                                                      0
               F7.5  partners met before they matter: a partner's death or split comes after a line that named them
                     in an earlier week                                                                   0 partners
Each judged row passes or not; a check is PASS when all its rows pass, else FAIL.

    python3 -B chroma-release/check_roll.py <f8_after|f10_once|f7_roll|all> [--repo DIR] [--commit SHA]
           [--seeds 41-44] [--lives 300] [--years 100] [--played 1-6x1-4] [--jobs 4] [--as-is] [--out DIR] [--no-record]

--repo: the checkout to check (default the tree this script sits in): its chroma-engine/v22-speedpass with its
chroma-library and chroma-packs (engine lives) and its chroma-game/prototype with the pin (played lives: they run the
game's engine_pin, so an engine branch's played lives read its engine only once the Game has re-pinned it). A row's
switches that DEFAULT (or the game's GAME) still has off are switched on and named in the report; --as-is judges the
checkout exactly as it is, so today's main (every v22.5 switch off) reads what the old rules do. f8_after and f10_once
share their engine lives (with `all`, or f10_once given --engine-from the f8_after run's folder). The bar's K9 reads
3,600 lives: --seeds 41-52. Each unit of work runs in its own process (--jobs at a time). Report: <out>/roll_<check>.txt
(default out/roll_<UTC time>/); one results line per check (results.py) unless --no-record. Exit code 0 when every
check run passes. About an hour on 4 cores for the engine lives at the defaults (1,200 lives), and 15 minutes for the
48 played lives.
"""
import argparse, json, os, re, subprocess, sys, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = ("f8_after", "f10_once", "f7_roll")
EARTH_WORLD = dict(setting="earth", pace=1.0, tech_level="modern", climate="middle")   # the game's Earth world (presets 1 to 4)
ENG_SW = ("retire_ends", "world_only")          # the engine lives' switches (F8, F10)
PLAY_SW = dict(f7_roll=dict(engine=("one_roll",), game=()), f10_once=dict(engine=("world_only",), game=("line_wait", "news_touch")))
LAY_GAME = dict(line_wait=5.0, news_touch=True)  # a game switch still off, laid on for the check (line_wait in years)
LINE_WAIT_TARGET = 5.0                           # F10.3's years when the game holds no line (--as-is)
WORLD_GRACE = 13                                 # F7.2: weeks the story may take to tell a death the world has had


def span(s):
    out = []
    for part in str(s).split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


# ---------------------------------------------------------------------------------------------------- engine lives
def unit_eng(repo, seed, lives, years, as_is):
    """One seed of engine lives through run_steps(): F8 and F10's counts."""
    import numpy as np
    sys.path.insert(0, os.path.join(repo, "chroma-engine", "v22-speedpass"))
    sys.dont_write_bytecode = True
    import engine as E, batch
    import world_keys as WK
    batch.LIB_DIR = os.path.join(repo, "chroma-library"); batch.PACK_DIR = os.path.join(repo, "chroma-packs")
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    P = dict(E.DEFAULT)
    laid = [] if as_is else [k for k in ENG_SW if not P.get(k)]
    P.update({k: True for k in laid}); P.update(world=True, world_cfg=dict(EARTH_WORLD))
    S = L["S"]; KN = [c[0] for c in E.COMMITMENTS]; CAR = KN.index("career")
    life1 = np.array([(s_.get("life") or "").split(",")[0].strip() == "work" for s_ in L["src"]])
    WAT = np.asarray(L.get("W_AT", np.full(S, -1)))
    door = (L["COMMIT"] == CAR).any(1)
    WORK = (life1 | (WAT == WK.INST_KINDS.index("employer"))) & ~door
    ROOT = np.asarray(L.get("ROOT", np.arange(S)))
    ONCE = np.asarray(L["ONCE"], bool); ONCE_K = np.asarray(L["ONCE_K"])
    r = dict(seed=seed, lives=lives, years=years, laid=laid, work_ret=[], unpicked=0, wm_all=0, wm_bad=[])
    ret_prev = np.zeros(lives, bool)          # retired and not working at the end of last week: the state the week met
    wm = None; lifeonce = None
    g = E.run_steps(lives, years, seed, P, lib=L)
    pz = next(g)
    try:
        while True:
            if pz.kind == "end":
                st = pz.state; t = pz.t
                s = np.asarray(st["s"]); dead = np.asarray(st["dead"], bool); recon = np.asarray(st["recon"], bool)
                held = np.asarray(st["held"]); retired = np.asarray(st["retired"], bool)
                live = ~dead & ~recon
                for n in np.nonzero(ret_prev & live & WORK[s])[0]:
                    r["work_ret"].append((int(n), round(t / 52, 2), L["names"][s[n]]))
                back = ret_prev & held[:, CAR]
                if back.any() and "ck" in st and "ok_" in st:
                    r["unpicked"] += int((back & ~(np.asarray(st["ok_"], bool) & (np.asarray(st["ck"]) == CAR))).sum())
                if wm is None and st.get("WL") is not None:
                    wm = np.zeros(S, bool); wm[np.asarray(st["WL"].wm_s, int)] = True
                if wm is not None:
                    m_ = wm[s] & live
                    r["wm_all"] += int(m_.sum())
                    if m_.any():
                        frc = np.asarray(st["frc_"], bool) if "frc_" in st else np.zeros((lives, S), bool)
                        had = np.asarray(st["had_ev"], bool) if "had_ev" in st else np.zeros(lives, bool)
                        sev = np.asarray(st["s_ev"]) if "s_ev" in st else np.full(lives, -1)
                        brought = had & (sev == s) & frc[np.arange(lives), s]
                        for n in np.nonzero(m_ & ~brought)[0]:
                            r["wm_bad"].append((int(n), round(t / 52, 2), L["names"][s[n]]))
                ret_prev = retired & ~held[:, CAR] & ~dead
                if lifeonce is None:               # once a life: not per commitment (ONCE_K), not per title (ONCE_HOLD_)
                    lifeonce = ONCE & (ONCE_K < 0)
                    for ix_ in st.get("ONCE_HOLD_", None) or []:
                        lifeonce[np.asarray(ix_, int)] = False
            pz = g.send(pz.value)
    except StopIteration as e_:
        o = e_.value
    sit_n = np.asarray(o["sit_n"])
    roots = sorted(set(ROOT[lifeonce].tolist()))
    r["once_roots"] = len(roots); r["once_bad"] = []
    for x in roots:
        cnt = sit_n[:, ROOT == x].sum(1)
        for n in np.nonzero(cnt > 1)[0]:
            r["once_bad"].append((int(n), L["names"][x], int(cnt[n])))
    cl = o["commits"]
    r["retired"] = len({e[0] for e in cl if e[2] == CAR and e[3] == "retired"})
    back_lives = {e[0] for e in cl if e[2] == CAR and e[3] == "start" and any(
        f[0] == e[0] and f[2] == CAR and f[3] == "retired" and f[1] < e[1] for f in cl)}
    r["went_back"] = len(back_lives)
    r["work_ret_noback"] = [x for x in r["work_ret"] if x[0] not in back_lives]
    return r


# ---------------------------------------------------------------------------------------------------- played lives
def unit_play(repo, preset, seed, what):
    """One played life of a preset to its end (the game of the checkout, CHROMA_ENGINE and CHROMA_GAME as the run set
    them), with hooks on the story and the game: F7's or F10's counts."""
    GD = os.path.join(repo, "chroma-game", "prototype")
    sys.path.insert(0, GD)
    sys.dont_write_bytecode = True
    import game as GM, story as ST
    laid = []
    for k in filter(None, os.environ.get("ROLL_LAY", "").split(",")):
        if not GM.GAME.get(k):
            GM.GAME[k] = LAY_GAME[k]; laid.append(k)
    PM = re.compile(r"⟦p:(\d+)⟧(.*?)⟦/⟧")
    box = dict(G=None)
    now = lambda: box["G"].t if box["G"] is not None else 0     # advance() plays many weeks before it returns
    pending = []                              # (week, marker, row, detail): a naming to look for in that week's lines
    bad = {k: [] for k in ("F7.1", "F7.2", "F7.3", "F7.4", "F7.5", "F10.3", "F10.4")}
    births, scenes, wdead, news = {}, [], {}, []
    role_was, splits, ever_partner = {}, {}, set()
    serial = [0]

    def frames():
        f = sys._getframe(2)
        while f is not None:
            yield f
            f = f.f_back

    new0, dies0 = ST.Story.new, ST.Story.dies

    def new(self, role, ref, sex=None):
        p = new0(self, role, ref, sex)
        serial[0] += 1; p["_k"] = serial[0]; p["_w0"] = now()
        return p

    def dies(self, p):
        if p is not None and p["alive"]:
            p["_wd"] = now()
        return dies0(self, p)
    ST.Story.new, ST.Story.dies = new, dies

    def naming(fn):
        orig = getattr(ST.Story, fn)

        def w(self, p):
            mark = orig(self, p)
            G = box["G"]
            if p is None or G is None:
                return mark
            legit = birth = False
            for f in frames():
                co = f.f_code.co_name
                if co in ("death", "quiet_deaths", "_who_dies", "dies") or (co == "role" and f.f_locals.get("slot") == "dead") \
                        or (co == "_one" and f.f_locals.get("k") == "dead"):   # the dead slot again (an outcome's {dead})
                    legit = True
                if co == "role" and f.f_locals.get("slot") == "child" and (f.f_locals.get("ctx") or {}).get("_birth"):
                    birth = True
            t = now()
            if not p["alive"] and p.get("_wd", t) < t and not legit:
                pending.append((t, mark, "F7.1", f"{p['role']} {p['name']}, dead since {p['_wd'] / 52:.1f}"))
            if p["alive"] and wdead and not legit:
                cid = {v: k for k, v in (getattr(G, "_castname", None) or {}).items()}.get(p["name"])
                if cid in wdead and t - wdead[cid] >= WORLD_GRACE:
                    pending.append((t, mark, "F7.2", f"{p['role']} {p['name']}, dead in the world since {wdead[cid] / 52:.1f}"))
            if p["role"] == "child" and p["alive"] and self.one_roll and self.kids_n == 0 and p.get("_w0") != t:
                pending.append((t, mark, "F7.3", f"child {p['name']} while the engine counts no living child"))
            if birth:
                births.setdefault(p["_k"], set()).add(t)
            return mark
        setattr(ST.Story, fn, w)
    naming("say"); naming("nm")
    later0, commit0, moment0 = ST.Story.later_child, ST.Story._commitment, ST.Story.moment

    def later_child(self, taken=False):
        line = later0(self, taken)
        if not taken:
            births.setdefault(self.people[-1]["_k"], set()).add(now())
        return line

    def commitment(self, c, m=None, title=None):
        line = commit0(self, c, m, title)
        if line and c.get("kind") == "children" and c.get("what") == "start" and "is born" in ST.plain(line):
            for pid, txt in PM.findall(line):
                for p in self.people:
                    if p["id"] == int(pid) and p["role"] == "child" and p["name"] in txt:
                        births.setdefault(p["_k"], set()).add(now())
        return line

    def moment(self, t, sit, stage, age, kind=None, kills=None):
        if sit == "a child is born" and (not scenes or scenes[-1] != now()):
            scenes.append(now())
        return moment0(self, t, sit, stage, age, kind, kills)
    ST.Story.later_child, ST.Story._commitment, ST.Story.moment = later_child, commitment, moment
    say0, news0, week0 = GM.Game._say, GM.Game._world_news, GM.Game._on_week

    def say(self, line, level=0, tag="note", **meta):
        k0 = len(self.feed)
        say0(self, line, level, tag, **meta)
        if len(self.feed) > k0:
            e = self.feed[-1]; e["_t"] = self.t
            pending[:] = [x for x in pending if x[0] == self.t]
            for _, mark, row, det in pending:
                if mark and mark in e["text"]:
                    bad[row].append(f"{self.t / 52:.1f}: {det}: {ST.plain(e['text'])[:160]}")

    def world_news(self, r_):
        k0 = len(self.feed)
        news0(self, r_)
        if len(self.feed) > k0:
            news.append((self.t, dict(r_)))

    def on_week(self, t, loc):
        for p in self.story.people:             # a partner who became a former partner: the week of the split
            k = p.get("_k")
            if role_was.get(k) == "partner" and p["role"] in ("ex", "former partner"):
                splits.setdefault(k, t - 1)      # (changed during the week before)
            if p["role"] == "partner":
                ever_partner.add(k)
            role_was[k] = p["role"]
        if t % 4 == 0 and self.story.one_roll:  # the outer world's dead, as the world has them
            wd = self.world_data()
            for c in (wd[2] if wd else []):
                if not c.get("alive") and c["id"] not in wdead:
                    wdead[c["id"]] = t
        return week0(self, t, loc)
    GM.Game._say, GM.Game._world_news, GM.Game._on_week = say, world_news, on_week

    G = box["G"] = GM.Game(name="Ari", seed=seed, **{k: v for k, v in GM.PRESETS[preset].items() if k not in ("title", "blurb")})
    for _ in range(100000):
        if G.over:
            break
        if G.advance() == "checkpoint":
            G.decide(None)
    P = G.story.people
    n = Counter()
    GG = GM.GAME
    r = dict(preset=preset, seed=seed, what=what, age=round(G.age(), 1), lines=len(G.feed), one_roll=bool(G.story.one_roll),
             laid=laid, game={k: GG.get(k) for k in ("line_wait", "news_touch", "news_age", "news_gap")})
    if what == "f7_roll":
        first = {}
        for e in G.feed:
            for pid, txt in PM.findall(e["text"]):
                n["namings"] += 1
                for p in P:
                    if p["id"] == int(pid) and p["name"] in txt:
                        first.setdefault(p["_k"], e["_t"])
        for k, ws in births.items():
            n["births"] += 1
            if max(ws) - min(ws) > 5:
                p = next(q for q in P if q.get("_k") == k)
                bad["F7.4"].append(f"{p['name']}: birth told at {', '.join(f'{w / 52:.1f}' for w in sorted(ws))}")
        for w in scenes:
            n["scenes"] += 1
            if not any(p["role"] == "child" and w <= p.get("_w0", -1) <= w + 2 for p in P):
                bad["F7.4"].append(f"{w / 52:.1f}: a birth scene with no newborn")
        for p in P:
            k = p.get("_k")
            if k not in ever_partner:
                continue
            n["partners"] += 1
            for ev, w in (("death", p.get("_wd")), ("split", splits.get(k))):
                fn = first.get(k)
                if w is not None and fn is not None and fn >= w:
                    bad["F7.5"].append(f"{p['name']} ({p['role']}): {ev} at {w / 52:.1f}, first named {fn / 52:.1f}")
    else:
        lw = float(GG.get("line_wait") or 0) or LINE_WAIT_TARGET
        r["line_wait_judged"] = lw
        said = {}
        for e in G.feed:
            if e["tag"] in GM.LINE_WAIT_TAGS and e["text"]:
                n["held_lines"] += 1
                k = ST.plain(e["text"])
                if k in said and e["_t"] - said[k] < lw * 52:
                    bad["F10.3"].append(f"{e['_t'] / 52:.1f}: said at {said[k] / 52:.1f} too: {k[:120]}")
                said[k] = e["_t"]
        last, laws = {}, {}
        gap = float(GG.get("news_gap") or 0) * 52; age0 = float(GG.get("news_age") or 0)
        for t, x in news:
            k_ = x["kind"]
            if x.get("locality") is not None or k_ in GM.NEWS_ALL:
                continue
            n["national_news"] += 1
            if t / 52 < age0:
                bad["F10.4"].append(f"{t / 52:.1f}: {k_} told before {age0:g}")
            if k_ == "law":
                lw_ = laws.get(x.get("law"))           # a law is news when it changes: not again in the state last told
                if lw_ is not None and lw_[0] == x.get("state"):
                    bad["F10.4"].append(f"{t / 52:.1f}: the law {x.get('law')} told again, still {x.get('state')} (told {lw_[1] / 52:.1f})")
                laws[x.get("law")] = (x.get("state"), t)
                continue
            g_ = "government" if k_ in ("gov_falls", "election") else k_
            if g_ in last and t - last[g_] < gap:
                bad["F10.4"].append(f"{t / 52:.1f}: {g_} told again inside {gap / 52:g} years (last {last[g_] / 52:.1f})")
            last[g_] = t
    r["n"] = dict(n)
    r["bad"] = {k: v for k, v in bad.items() if (k.startswith("F7") if what == "f7_roll" else k.startswith("F10"))}
    return r


# ---------------------------------------------------------------------------------------------------- running
def run_units(repo, jobs, todo, out, log):
    """Runs (name, args, env) units, `jobs` at a time, each in its own process; returns their JSON results."""
    res, running, todo = [], [], list(todo)
    while todo or running:
        while todo and len(running) < jobs:
            nm, args, env = todo.pop(0)
            e = {k: v for k, v in os.environ.items() if k not in ("CHROMA_GAME", "CHROMA_ENGINE")}   # the game reads both
            e.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", **env)                           # as JSON settings
            f = open(os.path.join(out, f"{nm}_{'_'.join(map(str, args))}.json"), "w")
            pr = subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "unit", repo, nm] + [str(a) for a in args],
                                  stdout=f, stderr=subprocess.PIPE, env=e, text=True)
            running.append((pr, f, nm, args, time.time()))
        time.sleep(1)
        for it in list(running):
            pr, f, nm, args, t0 = it
            if pr.poll() is None:
                continue
            running.remove(it); f.close()
            err = pr.stderr.read()
            try:
                r = json.loads(open(f.name).read().strip().splitlines()[-1])
            except (ValueError, IndexError):
                r = dict(error=(err or "no output").strip().splitlines()[-1][:300])
                log(f"  unit {nm} {args} failed: {err.strip()[-2000:]}")
            r["_unit"] = [nm] + list(args); r["_secs"] = round(time.time() - t0)
            res.append(r)
    return res


def engine_lives(a, repo, out, log):
    src = a.engine_from
    if src and os.path.exists(os.path.join(src, "engine_lives.json")):
        prev = json.load(open(os.path.join(src, "engine_lives.json")))
        if prev.get("key") == [a.seeds, a.lives, a.years, a.as_is]:
            log(f"  engine lives from {src}")
            return prev["res"]
    res = run_units(repo, a.jobs, [("eng", (sd, a.lives, a.years, int(a.as_is)), {}) for sd in span(a.seeds)], out, log)
    json.dump(dict(key=[a.seeds, a.lives, a.years, a.as_is], res=res), open(os.path.join(out, "engine_lives.json"), "w"))
    return res


def played_lives(a, repo, out, log, what):
    pre, _, sds = a.played.partition("x")
    sw = PLAY_SW[what]; env = {}
    if not a.as_is:
        sys.path.insert(0, os.path.join(repo, "chroma-engine", "v22-speedpass"))
        import engine as E
        env = dict(CHROMA_ENGINE=json.dumps({k: True for k in sw["engine"] if not E.DEFAULT.get(k)}),
                   ROLL_LAY=",".join(sw["game"]))
    todo = [("play", (p, s, what), env) for p in span(pre) for s in span(sds or "1")]
    return run_units(repo, a.jobs, todo, out, log)


def row(lines, rid, what, bad, n_txt, examples=()):
    lines.append(f"{'ok  ' if not bad else 'FAIL'} {rid} {what}: {bad} {n_txt}")
    for x in list(examples)[:4]:
        lines.append(f"       {x}")
    return not bad


def judge_engine(check, res, a):
    lines, ok = [], True
    err = [r for r in res if r.get("error")]
    got = [r for r in res if not r.get("error")]
    if err:
        ok = False; lines.append(f"FAIL engine lives: {len(err)} of {len(res)} seeds gave no result ({err[0]['error']})")
    N = sum(r["lives"] for r in got)
    laid = sorted({k for r in got for k in r["laid"]})
    lines.append(f"engine lives: {N} (seeds {a.seeds} x {a.lives} lives x {a.years} years; Earth with the packs, world on)"
                 + (f"; switched on here (DEFAULT has them off): {', '.join(laid)}" if laid else
                    "; as DEFAULT has them" + (" (--as-is)" if a.as_is else "")))
    if check == "f8_after":
        nb = [x for r in got for x in r["work_ret_noback"]]; al = [x for r in got for x in r["work_ret"]]
        ok &= row(lines, "F8.1", "work moments after retiring, lives that did not go back", len(nb),
                  f"weeks in {len({(r['seed'], x[0]) for r in got for x in r['work_ret_noback']})} lives (target 0)",
                  [f"age {x[1]}: {x[2]}" for x in nb])
        ok &= row(lines, "F8.2", "work moments in a week retired and not working, any life", len(al), "weeks (target 0)",
                  [f"age {x[1]}: {x[2]}" for x in al])
        lines.append(f"     reported: lives that retired {sum(r['retired'] for r in got)}; went back to work after retiring "
                     f"{sum(r['went_back'] for r in got)}; jobs taken while retired without a career pick that week "
                     f"(a title or another path) {sum(r['unpicked'] for r in got)}")
        ex = Counter(x[2] for x in al)
        if ex:
            lines.append("     moments: " + "; ".join(f"{k} ({v})" for k, v in ex.most_common(10)))
    else:
        ob = [x for r in got for x in r["once_bad"]]; wb = [x for r in got for x in r["wm_bad"]]
        wa = sum(r["wm_all"] for r in got)
        ex = Counter(x[1] for x in ob)
        ok &= row(lines, "F10.1", "once-a-life moments that came twice or more", len(ob),
                  f"lives and moments ({got[0]['once_roots'] if got else 0} once-a-life moments; target 0)",
                  [f"{k}: {v} lives" for k, v in ex.most_common(4)])
        ex = Counter(x[2] for x in wb)
        ok &= row(lines, "F10.2", "world moments in a week the world did not bring them", len(wb),
                  f"of {wa} ({wa / max(N, 1):.1f} world moments a life; target 0)", [f"{k}: {v}" for k, v in ex.most_common(4)])
    return lines, ok


def judge_played(check, res, a):
    lines, ok = [], True
    err = [r for r in res if r.get("error")]
    got = [r for r in res if not r.get("error")]
    if err:
        ok = False; lines.append(f"FAIL played lives: {len(err)} of {len(res)} gave no result ({err[0]['error']})")
    laid = sorted({k for r in got for k in r["laid"]})
    lines.append(f"played lives: {len(got)} (presets x seeds {a.played}), to the end of each life; one_roll "
                 f"{'on' if all(r['one_roll'] for r in got) else 'off' if not any(r['one_roll'] for r in got) else 'mixed'}"
                 + (f"; switched on here (GAME has them off): {', '.join(f'{k} {LAY_GAME[k]}' for k in laid)}" if laid else ""))
    tot = Counter()
    for r in got:
        tot.update(r["n"])
    rows = dict(f7_roll=(("F7.1", "lines that name a person after their death", f"of {tot['namings']} namings"),
                         ("F7.2", "lines that name a person the world lost 13 or more weeks before", f"of {tot['namings']} namings"),
                         ("F7.3", "lines that name a child of theirs while the engine counts none", f"of {tot['namings']} namings"),
                         ("F7.4", "births told in two weeks, or birth scenes with no newborn",
                          f"of {tot['births']} births and {tot['scenes']} scenes"),
                         ("F7.5", "partners whose death or split came before any line named them", f"of {tot['partners']} partners")),
                f10_once=(("F10.3", f"lines said again word for word inside line_wait "
                                    f"({got[0].get('line_wait_judged') if got else '?'} years)", f"of {tot['held_lines']} lines it holds"),
                          ("F10.4", "national news before news_age or again inside news_gap "
                                    f"({got[0]['game']['news_age'] if got else '?'}, {got[0]['game']['news_gap'] if got else '?'} years)",
                           f"of {tot['national_news']} national news")))
    for rid, what, n_txt in rows[check]:
        bad = [f"preset {r['preset']} seed {r['seed']}, {x}" for r in got for x in r["bad"].get(rid, [])]
        ok &= row(lines, rid, what, len(bad), n_txt + " (target 0)", bad)
    return lines, ok


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "unit":
        repo, nm, args = sys.argv[2], sys.argv[3], sys.argv[4:]
        if nm == "eng":
            r = unit_eng(repo, int(args[0]), int(args[1]), int(args[2]), bool(int(args[3])))
        else:
            r = unit_play(repo, args[0], int(args[1]), args[2])
        print(json.dumps(r, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("check", choices=CHECKS + ("all",))
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--commit", default=None)
    ap.add_argument("--seeds", default="41-44")
    ap.add_argument("--lives", type=int, default=300)
    ap.add_argument("--years", type=int, default=100)
    ap.add_argument("--played", default="1-6x1-4")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--as-is", action="store_true")
    ap.add_argument("--engine-from", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-record", action="store_true")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    commit = a.commit
    if commit is None:
        try:
            commit = subprocess.run(["git", "-C", repo, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or None
        except OSError:
            commit = None
    out = a.out or os.path.join(HERE, "out", time.strftime("roll_%Y%m%d-%H%M%S", time.gmtime()))
    os.makedirs(out, exist_ok=True)
    checks = CHECKS if a.check == "all" else (a.check,)
    rc = 0
    for check in checks:
        t0 = time.time(); lines = []
        log = lambda s: (lines.append(s), print(s, flush=True))
        log(f"{check} ({'K9' if check == 'f8_after' else 'K18'}), {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC; "
            f"repo {repo}, commit {commit or '?'}" + (" (--as-is)" if a.as_is else ""))
        ok = True
        if check in ("f8_after", "f10_once"):
            L_, ok_ = judge_engine(check, engine_lives(a, repo, out, log), a)
            for l_ in L_:
                log(l_)
            ok &= ok_
        if check in ("f10_once", "f7_roll"):
            L_, ok_ = judge_played(check, played_lives(a, repo, out, log, check), a)
            for l_ in L_:
                log(l_)
            ok &= ok_
        res = "PASS" if ok else "FAIL"
        log(f"{check}: {res} ({round(time.time() - t0)} s)")
        rep = os.path.join(out, f"roll_{check}.txt")
        open(rep, "w").write("\n".join(lines) + "\n")
        if not a.no_record:
            sys.path.insert(0, HERE)
            import results
            results.add(check, res, os.path.relpath(rep, os.path.dirname(HERE)),
                        note=f"{'K9' if check == 'f8_after' else 'K18'}, seeds {a.seeds}, {a.lives} lives, played {a.played}"
                             + (", as is" if a.as_is else ""),
                        candidate={"commit": commit} if commit else None, run=" ".join(sys.argv), secs=round(time.time() - t0))
        rc |= not ok
    return rc


if __name__ == "__main__":
    sys.exit(main())
