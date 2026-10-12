"""v22.5 rows K9 (F8) and K18 (F7, F10) of chroma-release/records/v22.5/scope.md: retirement ends work, one roll of
the living and once means once, judged on lives with their switches on at the refit's settings.

    python3 -B chroma-engine/tools/roll_once.py f8_after [--seeds 41-52] [--lives 300] [--years 100] [--jobs 4]
    python3 -B chroma-engine/tools/roll_once.py f10_once [same] [--played 1-6x1-4]
    python3 -B chroma-engine/tools/roll_once.py f7_roll  [--played 1-6x1-4] [--jobs 4]
    (common: --px JSON, engine settings laid over DEFAULT; --gx JSON, game settings over GAME; --out DIR; --strict)

Every switch is as the engine's DEFAULT (and the game's GAME), which is the refit's once it is merged. A row's own
switches that DEFAULT still has off (one_roll, world_only, retire_ends; the game's line_wait and news_touch) are laid on
for the check and the report says so; with --strict a switch still off in DEFAULT is a FAIL instead. Engine lives:
Earth with the live packs and the outer world on, as presets 1 to 4 play it, driven through run_steps so that every
week's moment is seen with the state it was drawn in. Played lives: the game's presets through game.Game, played to the
end (chroma-game/prototype/test/roll_once_game.py, one process a life).

f8_after   No work moment (a moment whose life tag is work or which is set at an employer, other than a door back: an
           option that starts a career) in a week they spent retired and not working, in a life that did not go back
           (the bar: 0 in 3,600 lives). Also counted and judged: the same in any life after a retirement they did not
           go back from, and a job that came to the retired without their act.
f10_once   Engine: a once-a-life moment (once:, not tied to a commitment or a title) comes at most once in a life,
           counting a child version with its original; a world moment (the outer world's own: elections, takeovers,
           leaks, rebuilding) comes only in a week the world brought it. Game: a line of a kind line_wait holds is not
           said again word for word inside line_wait years; national news (not their own place's, a war, a pandemic or
           a recession) is not told before news_age, the same kind (a government's fall with its election) not twice
           inside news_gap years, a law not twice for the same state.
f7_roll    Played lives (game): no line names a person after their death (the story's or the world's), except where the
           story tells of the dead (a death, a funeral, grief, a memory, the Book); no child is named before they are
           born or taken in; each child's birth is told once and every birth scene names a newborn; a partner is met
           (named in an earlier week) before their death, a split, a wedding or a child is told.

Prints one line per check and a last line "<id>: PASS" or "<id>: FAIL"; exit code 0 on PASS. Reports and each seed's
JSON go to --out (default OUT_DIR or the current folder, roll_once_<id>_<time>/).
"""
import json, os, subprocess, sys, time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.dirname(os.path.dirname(HERE))
GAME_TEST = os.path.join(TREE, "chroma-game", "prototype", "test", "roll_once_game.py")
ROW_SW = dict(f8_after=("retire_ends",), f10_once=("world_only",), f7_roll=("one_roll",))
ROW_GSW = dict(f8_after=(), f10_once=("line_wait", "news_touch"), f7_roll=())


def span(s):
    """'41-52' or '41,43' -> [41, ..., 52]."""
    out = []
    for part in str(s).split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def args_of(argv):
    a = dict(seeds="41-52", lives=300, years=100, jobs=4, px="{}", gx="{}", out=None, strict=False, played="1-6x1-4",
             engine_from=None)
    i = 0
    while i < len(argv):
        k = argv[i].lstrip("-")
        if k == "strict":
            a["strict"] = True; i += 1; continue
        a[k.replace("-", "_")] = argv[i + 1]; i += 2
    a["lives"], a["years"], a["jobs"] = int(a["lives"]), int(a["years"]), int(a["jobs"])
    return a


# ------------------------------------------------------------------------------------------- engine lives (one seed)
def engine_seed(seed, lives, years, px):
    """One seed of engine lives through run_steps; returns the counts as a dict (JSON-safe)."""
    import _engine   # noqa: F401  (the engine to check: CHROMA_ENGINE, default the tree's live engine)
    import numpy as np
    import engine as E, batch
    import world_keys as WK
    batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    P = dict(E.DEFAULT); P["world"] = True; P.update(px)
    S = L["S"]; KN = [c[0] for c in E.COMMITMENTS]; CAR = KN.index("career")
    life1 = np.array([(s_.get("life") or "").split(",")[0].strip() == "work" for s_ in L["src"]])
    WAT = np.asarray(L.get("W_AT", np.full(S, -1)))
    door = (L["COMMIT"] == CAR).any(1)
    WORK = (life1 | (WAT == WK.INST_KINDS.index("employer"))) & ~door
    ROOT = np.asarray(L.get("ROOT", np.arange(S)))
    ONCE = np.asarray(L["ONCE"], bool); ONCE_K = np.asarray(L["ONCE_K"])
    g = E.run_steps(N=lives, years=years, seed=seed, lib=L, P=P)
    msg = next(g)
    ret_prev = np.zeros(lives, bool)          # retired and not working at the end of last week (the state the moment met)
    went_back = np.zeros(lives, bool)
    work_ret = []                             # (life, age, moment) in a week spent retired and not working
    job_unasked = 0                           # a job held this week that last week's retired did not take by their act
    wm = None; wm_all = 0; wm_bad = []
    lifeonce = None
    o = None
    while True:
        kind, t, st, val = msg
        if kind == "end":
            s = np.asarray(st["s"]); dead = np.asarray(st["dead"], bool); recon = np.asarray(st["recon"], bool)
            held = np.asarray(st["held"]); retired = np.asarray(st["retired"], bool)
            if wm is None and st.get("WL") is not None:
                wm = np.zeros(S, bool); wm[np.asarray(st["WL"].wm_s, int)] = True
            live = ~dead & ~recon
            hit = ret_prev & live & WORK[s]
            for n in np.nonzero(hit)[0]:
                work_ret.append((int(n), round(t / 52, 2), L["names"][s[n]]))
            if ret_prev.any():                    # back at work this week: their own act or a job that came by itself
                back = ret_prev & held[:, CAR]
                if back.any():
                    went_back |= back
                    own = np.asarray(st.get("ok_", np.zeros(lives, bool)), bool) if "ok_" in st else None
                    ck = np.asarray(st["ck"]) if "ck" in st else None
                    if own is not None and ck is not None:
                        job_unasked += int((back & ~(own & (ck == CAR))).sum())
            if wm is not None:
                m_ = wm[s] & live
                wm_all += int(m_.sum())
                frc = np.asarray(st["frc_"], bool) if "frc_" in st else np.zeros((lives, S), bool)
                had = np.asarray(st["had_ev"], bool) if "had_ev" in st else np.zeros(lives, bool)
                sev = np.asarray(st["s_ev"]) if "s_ev" in st else np.full(lives, -1)
                brought = had & (sev == s) & frc[np.arange(lives), s]
                for n in np.nonzero(m_ & ~brought)[0]:
                    wm_bad.append((int(n), round(t / 52, 2), L["names"][s[n]]))
            ret_prev = retired & ~held[:, CAR] & ~dead
            if lifeonce is None:                  # once a life: not per commitment, not per title (ONCE_HOLD_)
                lifeonce = ONCE & (ONCE_K < 0)
                for ix_ in st.get("ONCE_HOLD_", []) or []:
                    lifeonce[np.asarray(ix_, int)] = False
        try:
            msg = g.send(val)
        except StopIteration as done:
            o = done.value
            break
    sit_n = np.asarray(o["sit_n"])
    roots = sorted(set(ROOT[lifeonce].tolist())) if lifeonce is not None else []
    once_bad = []
    for r in roots:
        cnt = sit_n[:, ROOT == r].sum(1)
        for n in np.nonzero(cnt > 1)[0]:
            once_bad.append((int(n), L["names"][r], int(cnt[n])))
    cl = o["commits"]
    retired_lives = {e[0] for e in cl if e[2] == CAR and e[3] == "retired"}
    back_lives = {e[0] for e in cl if e[2] == CAR and e[3] == "start" and any(
        f[0] == e[0] and f[2] == CAR and f[3] == "retired" and f[1] < e[1] for f in cl)}
    return dict(seed=seed, lives=lives, years=years, retired=len(retired_lives), went_back=len(back_lives),
                work_ret=work_ret, work_ret_noback=[x for x in work_ret if x[0] not in back_lives],
                job_unasked=job_unasked, wm_all=wm_all, wm_bad=wm_bad, once_roots=len(roots), once_bad=once_bad,
                sw={k: P.get(k) for k in ("retire_ends", "world_only", "one_roll")})


def run_engine(a, px, out):
    procs, res = [], []
    seeds = span(a["seeds"])
    src = a.get("engine_from")
    for sd in seeds:
        f = os.path.join(out, f"engine_seed{sd}.json")
        if src and os.path.exists(os.path.join(src, f"engine_seed{sd}.json")):   # the same lives, lived for the other row
            prev = json.load(open(os.path.join(src, f"engine_seed{sd}.json")))
            if prev.get("lives") == a["lives"] and prev.get("years") == a["years"] and prev.get("px") == px:
                json.dump(prev, open(f, "w")); continue
        cmd = [sys.executable, "-B", os.path.abspath(__file__), "_seed", str(sd), str(a["lives"]), str(a["years"]),
               json.dumps(px), f]
        while len([p for p in procs if p.poll() is None]) >= a["jobs"]:
            time.sleep(2)
        procs.append(subprocess.Popen(cmd, stdout=open(f + ".log", "w"), stderr=subprocess.STDOUT))
    for p in procs:
        p.wait()
    for sd in seeds:
        f = os.path.join(out, f"engine_seed{sd}.json")
        if not os.path.exists(f):
            print(f"engine seed {sd}: no result (see {f}.log)")
            res.append(None); continue
        res.append(json.load(open(f)))
    return res


# ------------------------------------------------------------------------------------------- played lives (game)
def run_played(a, px, gx, out, what):
    pre, _, sds = a["played"].partition("x")
    lives = [(p, s) for p in span(pre) for s in span(sds or "1")]
    procs, res = [], []
    env = dict(os.environ, CHROMA_ENGINE=json.dumps(px), CHROMA_GAME=json.dumps(gx), RO_LAY=",".join(ROW_GSW[what]))
    for p, s in lives:
        f = os.path.join(out, f"played_{p}_{s}.json")
        while len([q for q in procs if q.poll() is None]) >= a["jobs"]:
            time.sleep(2)
        procs.append(subprocess.Popen([sys.executable, "-B", GAME_TEST, str(p), str(s), what, f],
                                      cwd=os.path.dirname(os.path.dirname(GAME_TEST)), env=env,
                                      stdout=open(f + ".log", "w"), stderr=subprocess.STDOUT))
    for q in procs:
        q.wait()
    for p, s in lives:
        f = os.path.join(out, f"played_{p}_{s}.json")
        res.append(json.load(open(f)) if os.path.exists(f) else dict(preset=p, seed=s, error=f"no result, see {f}.log"))
    return res


def E_DEFAULT():
    import _engine   # noqa: F401
    import engine as E
    return E.DEFAULT


def switches(row, a):
    """The row's engine switches as DEFAULT has them; those still off are laid on (or fail with --strict)."""
    import _engine   # noqa: F401
    import engine as E
    px = json.loads(a["px"]); off = [k for k in ROW_SW[row] if k not in px and not E.DEFAULT.get(k)]
    px.update({k: True for k in off})
    return px, off


def main():
    row = sys.argv[1]
    if row == "_seed":
        sd, n_, y_, px_, f = sys.argv[2:7]
        r = engine_seed(int(sd), int(n_), int(y_), json.loads(px_))
        r["px"] = json.loads(px_)
        json.dump(r, open(f, "w"))
        return 0
    if row not in ROW_SW:
        print(__doc__); return 2
    a = args_of(sys.argv[2:])
    out = a["out"] or os.path.join(os.environ.get("OUT_DIR") or os.getcwd(), f"roll_once_{row}_{time.strftime('%Y%m%d-%H%M%S')}")
    os.makedirs(out, exist_ok=True)
    px, off = switches(row, a); gx = json.loads(a["gx"])
    lines = [f"{row}: engine settings over DEFAULT {json.dumps(px)}" + (f"; game settings over GAME {json.dumps(gx)}" if gx else "")]
    ok = True
    if off:
        lines.append(("FAIL still off in DEFAULT (--strict): " if a["strict"] else
                      "     still off in DEFAULT, laid on for this check: ") + ", ".join(off))
        ok = not a["strict"]
    t0 = time.time()
    if row in ("f8_after", "f10_once"):
        pe = dict(px)
        for k in ("retire_ends", "world_only"):          # one set of lives serves both rows (--engine-from)
            if k not in pe and not E_DEFAULT().get(k):
                pe[k] = True
        res = run_engine(a, pe, out)
        got = [r for r in res if r]
        if len(got) < len(res):
            ok = False; lines.append(f"FAIL engine lives: {len(res) - len(got)} of {len(res)} seeds gave no result")
        N = sum(r["lives"] for r in got)
        lines.append(f"engine lives: {N} ({a['seeds']} x {a['lives']} lives x {a['years']} years, Earth with the packs, world on)")
        if row == "f8_after":
            nb = sum(len(r["work_ret_noback"]) for r in got); al = sum(len(r["work_ret"]) for r in got)
            ln = len({(r["seed"], x[0]) for r in got for x in r["work_ret_noback"]})
            ret = sum(r["retired"] for r in got); back = sum(r["went_back"] for r in got)
            ju = sum(r["job_unasked"] for r in got)
            for nm_, v_, txt in (("work moments after retiring, lives that did not go back", nb, f"{nb} in {ln} lives"),
                                 ("work moments in weeks retired and not working, any life", al, str(al)),
                                 ("jobs that came to the retired without their act", ju, str(ju))):
                lines.append(f"{'ok  ' if v_ == 0 else 'FAIL'} {nm_}: {txt} (target 0)")
                ok &= v_ == 0
            lines.append(f"     lives that retired: {ret}; went back to work after retiring: {back}")
            ex = Counter(x[2] for r in got for x in r["work_ret"])
            if ex:
                lines.append("     moments: " + "; ".join(f"{k} ({v})" for k, v in ex.most_common(12)))
        else:
            ob = sum(len(r["once_bad"]) for r in got); wb = sum(len(r["wm_bad"]) for r in got)
            wa = sum(r["wm_all"] for r in got)
            lines.append(f"{'ok  ' if ob == 0 else 'FAIL'} once-a-life moments that came twice or more: {ob} "
                         f"(life and moment pairs; {got[0]['once_roots'] if got else 0} once-a-life moments; target 0)")
            ok &= ob == 0
            ex = Counter(x[1] for r in got for x in r["once_bad"])
            if ex:
                lines.append("     moments: " + "; ".join(f"{k} ({v})" for k, v in ex.most_common(12)))
            lines.append(f"{'ok  ' if wb == 0 else 'FAIL'} world moments in a week the world did not bring them: {wb} of "
                         f"{wa} ({wa / max(N, 1):.1f} world moments a life; target 0)")
            ok &= wb == 0
            ex = Counter(x[2] for r in got for x in r["wm_bad"])
            if ex:
                lines.append("     moments: " + "; ".join(f"{k} ({v})" for k, v in ex.most_common(12)))
    if row in ("f10_once", "f7_roll"):
        res = run_played(a, px, gx, out, row)
        err = [r for r in res if r.get("error")]
        if err:
            ok = False; lines.append(f"FAIL played lives: {len(err)} of {len(res)} gave no result ({err[0]['error']})")
        got = [r for r in res if not r.get("error")]
        lines.append(f"played lives: {len(got)} (presets x seeds {a['played']}), to the end of each life")
        laid = sorted({k for r in got for k in r.get("laid", [])})
        if laid:
            lines.append(("FAIL still off in GAME (--strict): " if a["strict"] else
                          "     still off in GAME, laid on for this check: ") + ", ".join(
                f"{k} {got[0]['game'][k]}" for k in laid))
            ok &= not a["strict"]
        keys = Counter()
        for r in got:
            for k, v in r["checks"].items():
                keys[k] += 0
        for k in keys:
            bad = [(r["preset"], r["seed"], x) for r in got for x in r["checks"][k]["bad"]]
            n_ = sum(r["checks"][k]["n"] for r in got)
            lines.append(f"{'ok  ' if not bad else 'FAIL'} {got[0]['checks'][k]['what']}: {len(bad)} of {n_} (target 0)")
            ok &= not bad
            for p_, s_, x in bad[:4]:
                lines.append(f"     preset {p_} seed {s_}: {x}")
    lines.append(f"{row}: {'PASS' if ok else 'FAIL'} ({time.time() - t0:.0f} s; report {out}/report.txt)")
    open(os.path.join(out, "report.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
