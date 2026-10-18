"""Picks come back (chroma-ideas/gameplay-2026-10-17/picks-come-back.md): Release's played-life rows P1 to P6.

    python3 -B chroma-release/check_picks.py run --repo DIR --commit SHA --out DIR [--game JSON]
                 [--policies let,random,reader,none] [--presets 1-4] [--seeds 1-6] [--jobs 4]
    python3 -B chroma-release/check_picks.py judge --on DIR --off DIR [--no-record]
    python3 -B chroma-release/check_picks.py noplayer --repo DIR --commit SHA --out DIR [--seeds 41] [--lives 400]
                 [--years 100] [--worlds off,on,seed] [--jobs 4] [--no-record]

run plays whole lives on the Game object as the page plays them, with Release's copy of the player-impact harness
(picks/impact.py: let, random, reader, none), on a git archive of the commit's chroma-game/prototype (the game with its
engine_pin), CHROMA_GAME set to --game: '{"returns": true}' for the "on" side and '{"returns": false}' for the "off" side
(the GAME switch `returns` sets the engine's echo_play), the same policies, presets and seeds on both, so every life has
its pair. One JSON a life: impact.py's record plus
`picks`, one row per ask (age, sit, repeat: the moment was asked before in this life and is not a return, thread: the F5
line shows, seed). `seed` is what the game puts on a return's ask, cp["seed"]:
    age    the seed's age            sit   the seed's moment     way   the way picked then
    t      the seed's week (P3 reads weeks when it is there, else the ages)
    went   "well" or "badly"         person  the seed's person (id), or None for a seed with nobody in it
    near   the seed's person is alive and near at the return
    now    who fills the return's person slot: the person's id, "memory:<id>" or "heard:<id>", or None
    tilt   the change the first time made to the return's ways' odds (mean over its ways, signed)
judge reads both sides and writes chroma-release/out/picks_<UTC>.txt and one results line per row:
    picks_returns  P1 returns asked per life, mean over the played lives with it on: 6 to 10 ("about 8"); none with it off
    picks_person   P2 every return of a seed with a person brings that person back when they are alive and near, and
                   otherwise their memory or someone who heard ("memory:" or "heard:" of that person)
    picks_gap      P3 no return within a year of its seed
    picks_repeats  P4 repeats per life lower with it on than off, over the same lives
    picks_impact   P5 the player-impact reading: well(reader) - well(random) with it on at least as large as with it off
    picks_tilt     P6 a seed that went well tilts its return up and one that went badly down, never by more than .05
Small counts: a row whose difference sits inside its spread reads more seeds (the SMALL COUNTS ruling), its target stays.
judge records only when both sides name the same commit (a trial on two commits takes --no-record).

noplayer is row N1 (records/v23/plan.md, "N1's reading"): batch lives with no player, on a git archive of the
commit's engine, Library and packs, run by check_speedpass.py's worker twice, with echo_play off and on. Every output
must be identical, except the hook's own readout `returns`, which only a run with echo_play on returns and which must
be empty (lives with no player plant no seeds). The runs stay in --out; the report is
chroma-release/out/picks_noplayer_<UTC>.txt and the results line picks_noplayer.
"""
import argparse, glob, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PICKS = os.path.join(HERE, "picks")
GAME_DIR = "chroma-game/prototype"


def plain(x):
    if isinstance(x, dict):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    if hasattr(x, "item"):
        return x.item()
    return x if isinstance(x, (str, int, float, bool)) or x is None else str(x)


def life(a):
    """One life (a subprocess of run): impact.play with each ask recorded."""
    os.environ.update(PRESET=a.preset, GAMEDIR=a.game, CHROMA_GAME=a.game_json, OMP_NUM_THREADS="1")
    sys.path.insert(0, PICKS)
    import impact                                      # puts the game first on sys.path and chdirs there
    import game as G
    rows, seen = [], set()
    orig = G.Game.decide

    def decide(self, *x, **k):
        cp = self.pending
        if cp is not None and not cp.get("turning"):
            sd = cp.get("seed")
            rows.append(dict(age=round(float(cp["age"]), 2), t=int(cp["t"]) if cp.get("t") is not None else None, sit=cp.get("sit"), title=cp.get("title"),
                             repeat=cp.get("sit") in seen and not sd, thread=bool(cp.get("thread")), seed=plain(sd) if sd else None))
            seen.add(cp.get("sit"))
        return orig(self, *x, **k)
    G.Game.decide = decide
    r = impact.play(int(a.seed), a.policy)
    r.pop("yrs", None)
    r.update(preset=a.preset, game_json=a.game_json, picks=rows)
    json.dump(plain(r), open(a.out + ".tmp", "w")); os.replace(a.out + ".tmp", a.out)
    print(a.policy, a.preset, a.seed, r["secs"], "s", len(rows), "asks", sum(1 for x in rows if x["seed"]), "returns", flush=True)


def span(s):
    out = []
    for part in s.split(","):
        lo, _, hi = part.partition("-")
        out += list(range(int(lo), int(hi or lo) + 1))
    return out


def run(a):
    os.makedirs(a.out, exist_ok=True)
    sha = subprocess.run(["git", "-C", a.repo, "rev-parse", a.commit], check=True, capture_output=True, text=True).stdout.strip()
    tree = os.path.join(a.out, "tree")
    stamp = os.path.join(tree, "tree.sha")
    if not (os.path.exists(stamp) and open(stamp).read().strip() == sha):   # never reuse another commit's tree
        subprocess.run(["rm", "-rf", tree], check=True); os.makedirs(tree)
        subprocess.run(f"git -C {a.repo} archive {sha} {GAME_DIR} | tar -x -C {tree}", shell=True, check=True)
        open(stamp, "w").write(sha + "\n")
        for f in glob.glob(os.path.join(a.out, "*_*_*.json")):   # lives of another commit
            os.remove(f)
    json.dump(dict(commit=sha, game=a.game, policies=a.policies, presets=a.presets, seeds=a.seeds,
                   time=time.strftime("%Y-%m-%d %H:%M", time.gmtime())), open(os.path.join(a.out, "meta.json"), "w"))
    env = {k: v for k, v in os.environ.items() if k not in ("CHROMA_ROOT", "CHROMA_ENGINE", "CHROMA_GAME")}
    jobs = []
    for pol in a.policies.split(","):
        for pr in span(a.presets):
            for sd in span(a.seeds):
                f = os.path.join(a.out, f"{pol.replace(':', '')}_{pr}_{sd}.json")
                if not os.path.exists(f):
                    jobs.append([sys.executable, "-B", os.path.abspath(__file__), "life", "--game", os.path.join(tree, GAME_DIR),
                                 "--policy", pol, "--preset", str(pr), "--seed", str(sd), "--game-json", a.game, "--out", f])
    log = open(os.path.join(a.out, "run.log"), "a")
    live, bad = [], 0
    while jobs or live:
        while jobs and len(live) < a.jobs:
            live.append(subprocess.Popen(jobs.pop(0), env=env, stdout=log, stderr=log))
        time.sleep(2)
        for p in [p for p in live if p.poll() is not None]:
            live.remove(p); bad += p.returncode != 0
    print(f"run {sha[:12]} game {a.game}: {len(glob.glob(os.path.join(a.out, '*_*_*.json')))} lives in {a.out}, {bad} failed")
    return 1 if bad else 0


def load(d):
    out = {}
    for f in glob.glob(os.path.join(d, "*_*_*.json")):
        if os.path.basename(f) == "meta.json":
            continue
        r = json.load(open(f))
        out[(r["policy"], str(r["preset"]), int(r["seed"]))] = r
    meta = json.load(open(os.path.join(d, "meta.json"))) if os.path.exists(os.path.join(d, "meta.json")) else {}
    return out, meta


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def sd_mean(xs):
    xs = list(xs)
    if len(xs) < 2:
        return float("nan")
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1) / len(xs)) ** 0.5


def judge(a):
    on, mon = load(a.on)
    off, moff = load(a.off)
    if not a.no_record and (not mon.get("commit") or mon.get("commit") != moff.get("commit")):
        print(f"STOP: the on side names commit {mon.get('commit')} and the off side {moff.get('commit')}; "
              "a results line needs both on one commit (a trial: --no-record)")
        return 2
    keys = sorted(set(on) & set(off))
    played = [k for k in keys if k[0] != "none"]
    lines = [f"Picks come back, played-life rows, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
             f"  on  {a.on}: commit {mon.get('commit', '?')[:12]} game {mon.get('game')}; off {a.off}: commit {moff.get('commit', '?')[:12]} game {moff.get('game')}",
             f"  {len(keys)} paired lives ({len(played)} played: policies {sorted({k[0] for k in played})}, presets {sorted({k[1] for k in keys})}, seeds {len(sorted({k[2] for k in keys}))})"]
    res = {}
    rets = [(k, p) for k in played for p in on[k]["picks"] if p.get("seed")]
    n_on = [sum(1 for p in on[k]["picks"] if p.get("seed")) for k in played]
    n_off = sum(1 for k in keys for p in off[k]["picks"] if p.get("seed"))
    asks_on = [len(on[k]["picks"]) for k in played]
    m = mean(n_on)
    ok = 6 <= m <= 10 and n_off == 0
    res["picks_returns"] = (ok, f"returns {m:.2f} a life (target 6 to 10), {sum(n_on)} of {sum(asks_on)} asks ({sum(n_on) / max(1, sum(asks_on)):.3f}); off {n_off}")
    lines.append(f"{'ok  ' if ok else 'MISS'} P1 returns asked per life {m:.2f} (+-{sd_mean(n_on):.2f}), target 6 to 10; "
                 f"{sum(n_on)} of {sum(asks_on)} asks are returns ({sum(n_on) / max(1, sum(asks_on)):.3f}, about 1 in 8 aimed); with it off {n_off}")
    for pol in sorted({k[0] for k in played}):
        xs = [sum(1 for p in on[k]["picks"] if p.get("seed")) for k in played if k[0] == pol]
        lines.append(f"       {pol:8s} {mean(xs):.2f} a life ({len(xs)} lives)")
    withp = [(k, p) for k, p in rets if p["seed"].get("person") is not None]
    near = [(k, p) for k, p in withp if p["seed"].get("near")]
    same = [1 for k, p in near if p["seed"].get("now") == p["seed"]["person"]]
    far = [(k, p) for k, p in withp if not p["seed"].get("near")]
    kept = [1 for k, p in far if str(p["seed"].get("now") or "") in (f"memory:{p['seed']['person']}", f"heard:{p['seed']['person']}")]
    ok = bool(withp) and len(same) == len(near) and len(kept) == len(far)
    res["picks_person"] = (ok, f"{len(same)} of {len(near)} near seeds came back with their person; {len(kept)} of {len(far)} others as a memory or someone who heard")
    lines.append(f"{'ok  ' if ok else 'MISS'} P2 the same person: {len(withp)} of {len(rets)} returns had a person; {len(same)} of {len(near)} "
                 f"alive and near came back with that person ({len(same) / max(1, len(near)):.3f}); {len(kept)} of {len(far)} gone or far came as a "
                 f"memory of them or someone who heard")
    # in weeks when the seed carries its week (cp["seed"]["t"]) and the ask its own (t); else in years from the ages,
    # where the seed's age is rounded to .1 and a gap just under 1.0 may be a full year
    wk = all(p.get("t") is not None and p["seed"].get("t") is not None for k, p in rets)
    if wk:
        gaps = [(p["t"] - int(p["seed"]["t"])) / 52 for k, p in rets]
    else:
        gaps = [p["age"] - float(p["seed"]["age"]) for k, p in rets if p["seed"].get("age") is not None]
    under = [g for g in gaps if g < 1.0]
    ok = bool(gaps) and not under and len(gaps) == len(rets)
    res["picks_gap"] = (ok, f"{len(under)} of {len(gaps)} returns within a year of their seed ({'weeks' if wk else 'rounded ages'})")
    lines.append(f"{'ok  ' if ok else 'MISS'} P3 no return within a year of its seed: {len(under)} of {len(gaps)} under a year"
                 + (f" (shortest {min(gaps):.2f} years, median {sorted(gaps)[len(gaps) // 2]:.1f})" if gaps else "")
                 + (", read in weeks" if wk else ", read from ages (the seed's rounded to .1: a gap of .95 to 1.0 may be a full year)")
                 + ("" if len(gaps) == len(rets) else f"; {len(rets) - len(gaps)} returns without a seed age"))
    rep_on = [sum(1 for p in on[k]["picks"] if p["repeat"]) for k in played]
    rep_off = [sum(1 for p in off[k]["picks"] if p["repeat"]) for k in played]
    dif = [x - y for x, y in zip(rep_on, rep_off)]
    ok = mean(rep_on) < mean(rep_off)
    res["picks_repeats"] = (ok, f"repeats {mean(rep_on):.2f} a life on, {mean(rep_off):.2f} off")
    lines.append(f"{'ok  ' if ok else 'MISS'} P4 repeats per life {mean(rep_on):.2f} on, {mean(rep_off):.2f} off (paired change {mean(dif):+.2f} "
                 f"+-{sd_mean(dif):.2f}); asks per life {mean(asks_on):.1f} on, {mean(len(off[k]['picks']) for k in played):.1f} off")
    w = lambda side, pol: {k[1:]: side[k]["well"] for k in keys if k[0] == pol and side[k].get("well") is not None}
    gap_on, gap_off = [], []
    for kk in sorted(set(w(on, "reader")) & set(w(on, "random")) & set(w(off, "reader")) & set(w(off, "random"))):
        gap_on.append(w(on, "reader")[kk] - w(on, "random")[kk]); gap_off.append(w(off, "reader")[kk] - w(off, "random")[kk])
    dd = [x - y for x, y in zip(gap_on, gap_off)]
    ok = bool(dd) and mean(dd) >= 0
    res["picks_impact"] = (ok, f"reader - random {mean(gap_on):+.3f} on, {mean(gap_off):+.3f} off ({len(dd)} pairs)")
    lines.append(f"{'ok  ' if ok else 'MISS'} P5 player impact: well(reader) - well(random) {mean(gap_on):+.3f} on, {mean(gap_off):+.3f} off "
                 f"(paired {mean(dd):+.3f} +-{sd_mean(dd):.3f}, {len(dd)} starts and seeds)")
    for pol in ("reader", "random", "let"):
        for side, nm in ((on, "on"), (off, "off")):
            x, b = w(side, pol), w(side, "none")
            ks = sorted(set(x) & set(b))
            if ks:
                lines.append(f"       {pol:6s} {nm:3s} well {mean(x[k] for k in ks):.3f}, against none {mean(x[k] - b[k] for k in ks):+.3f} ({len(ks)})")
    tw = [float(p["seed"]["tilt"]) for k, p in rets if p["seed"].get("went") == "well" and p["seed"].get("tilt") is not None]
    tb = [float(p["seed"]["tilt"]) for k, p in rets if p["seed"].get("went") == "badly" and p["seed"].get("tilt") is not None]
    big = [t for t in tw + tb if abs(t) > 0.05]
    ok = bool(tw) and bool(tb) and mean(tw) > 0 and mean(tb) < 0 and not big
    res["picks_tilt"] = (ok, f"went well {mean(tw):+.3f} ({len(tw)}), badly {mean(tb):+.3f} ({len(tb)}), {len(big)} over .05")
    lines.append(f"{'ok  ' if ok else 'MISS'} P6 the first time tilts this time: went well {mean(tw):+.3f} ({len(tw)} returns), went badly "
                 f"{mean(tb):+.3f} ({len(tb)}); {len(big)} beyond .05")
    allok = all(v[0] for v in res.values())
    lines.append(f"picks: {'PASS' if allok else 'FAIL'} ({sum(v[0] for v in res.values())} of {len(res)} rows)")
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chroma-env"))
    os.environ.setdefault("CHROMA_ROOT", os.path.dirname(HERE))
    from paths import path
    rep = path("release_out", f"picks_{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}.txt")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("report:", rep)
    if not a.no_record:
        sys.path.insert(0, HERE)
        from results import add
        cand = {"commit": mon["commit"]} if mon.get("commit") else None
        for k, (ok_, note) in res.items():
            add(k, "PASS" if ok_ else "FAIL", rep, note=note, candidate=cand, run=" ".join(sys.argv))
    return 0 if allok else 1


NP_DIRS = "chroma-engine/v22-speedpass chroma-library chroma-packs"


def np_same(x, y):
    import pickle
    import numpy as np
    if pickle.dumps(x) == pickle.dumps(y):
        return True
    if isinstance(x, dict) and isinstance(y, dict):
        return x.keys() == y.keys() and all(np_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(np_same(u, v) for u, v in zip(x, y))
    try:
        ax, ay = np.asarray(x), np.asarray(y)
    except Exception:
        return False
    if ax.shape != ay.shape or ax.dtype == object or ay.dtype == object:
        return False
    return bool(np.array_equal(ax, ay, equal_nan=ax.dtype.kind in "fc" and ay.dtype.kind in "fc"))


def noplayer(a):
    """N1: the same batch lives with echo_play off and on, on the commit's own engine, Library and packs."""
    import pickle
    os.makedirs(a.out, exist_ok=True)
    sha = subprocess.run(["git", "-C", a.repo, "rev-parse", a.commit], check=True, capture_output=True, text=True).stdout.strip()
    tree = os.path.join(a.out, "tree")
    stamp = os.path.join(tree, "tree.sha")
    if not (os.path.exists(stamp) and open(stamp).read().strip() == sha):   # never reuse another commit's tree
        subprocess.run(["rm", "-rf", tree], check=True); os.makedirs(tree)
        subprocess.run(f"git -C {a.repo} archive {sha} {NP_DIRS} | tar -x -C {tree}", shell=True, check=True)
        open(stamp, "w").write(sha + "\n")
        for f in glob.glob(os.path.join(a.out, "id_*.pkl")):   # runs of another commit
            os.remove(f)
    eng, lib, packs = (os.path.join(tree, d) for d in NP_DIRS.split())
    env = {k: v for k, v in os.environ.items() if k not in ("CHROMA_ROOT", "CHROMA_ENGINE", "CHROMA_GAME")}
    env.update(OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    worlds = [w for w in a.worlds.split(",") if w]
    order = sorted(worlds, key=lambda w: {"on": 0, "off": 1}.get(w, 2))   # the longest runs first
    runs, jobs = [], []
    for sd in span(a.seeds):
        for w in order:
            for tag, pj in (("off", '{"echo_play": false}'), ("on", '{"echo_play": true}')):
                f = os.path.join(a.out, f"id_{sd}_{w}_{tag}.pkl")
                runs.append((sd, w, tag, f))
                if not os.path.exists(f):
                    jobs.append([sys.executable, "-B", os.path.join(HERE, "check_speedpass.py"), "--worker", eng, lib, packs,
                                 str(sd), w, str(a.lives), str(a.years), pj, f])
    log = open(os.path.join(a.out, "run.log"), "a")
    live, bad = [], 0
    while jobs or live:
        while jobs and len(live) < a.jobs:
            live.append(subprocess.Popen(jobs.pop(0), env=env, cwd=a.out, stdout=log, stderr=log))
        time.sleep(2)
        for p in [p for p in live if p.poll() is not None]:
            live.remove(p); bad += p.returncode != 0
    lines = [f"Picks come back, N1 no player, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
             f"  commit {sha[:12]}: its engine, Library and packs ({tree}); seeds {a.seeds}, {a.lives} lives x {a.years} years, "
             f"worlds {','.join(worlds)}; echo_play off against on, every output equal but the readout returns, which must be empty"]
    ok = not bad
    for sd in span(a.seeds):
        for w in worlds:
            fo, fn = (next(r[3] for r in runs if r[:3] == (sd, w, t)) for t in ("off", "on"))
            if not (os.path.exists(fo) and os.path.exists(fn)):
                ok = False; lines.append(f"MISS {sd} {w}: a run left no output (see {a.out}/run.log)"); continue
            b, n = pickle.load(open(fo, "rb")), pickle.load(open(fn, "rb"))
            extra, gone = sorted(set(n["out"]) - set(b["out"])), sorted(set(b["out"]) - set(n["out"]))
            both = sorted(set(b["out"]) & set(n["out"]))
            diff = [k for k in both if not np_same(b["out"][k], n["out"][k])]
            ret = n["out"].get("returns")
            empty = ret is None or len(ret) == 0
            good = not diff and not gone and extra in ([], ["returns"]) and empty and b["dropped"] == n["dropped"]
            ok &= good
            lines.append(f"{'ok  ' if good else 'MISS'} {sd} {w}: {len(both) - len(diff)} of {len(both)} outputs identical"
                         + (f", differ: {', '.join(diff[:12])}" if diff else "")
                         + (f"; only with it off: {', '.join(gone)}" if gone else "")
                         + (f"; only with it on: {', '.join(extra)}" if extra else "; no returns readout")
                         + ("" if ret is None else f" ({len(ret)} entries{'' if empty else ', must be empty'})")
                         + (f"; not compared (not picklable): {', '.join(sorted(set(b['dropped']) | set(n['dropped'])))}"
                            if b["dropped"] or n["dropped"] else ""))
    lines.append(f"noplayer: {'PASS' if ok else 'FAIL'}" + (f" ({bad} runs failed)" if bad else ""))
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chroma-env"))
    os.environ.setdefault("CHROMA_ROOT", os.path.dirname(HERE))
    from paths import path
    rep = path("release_out", f"picks_noplayer_{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}.txt")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("report:", rep)
    if not a.no_record:
        sys.path.insert(0, HERE)
        from results import add
        add("picks_noplayer", "PASS" if ok else "FAIL", rep, note=f"seeds {a.seeds}, {a.lives} x {a.years}, worlds {a.worlds}",
            candidate={"commit": sha}, run=" ".join(sys.argv))
    return 0 if ok else 1


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("run")
p.add_argument("--repo", required=True); p.add_argument("--commit", required=True); p.add_argument("--out", required=True)
p.add_argument("--game", default="{}"); p.add_argument("--policies", default="let,random,reader,none")
p.add_argument("--presets", default="1-4"); p.add_argument("--seeds", default="1-6"); p.add_argument("--jobs", type=int, default=4)
p = sub.add_parser("life")
for x in ("--game", "--policy", "--preset", "--seed", "--game-json", "--out"):
    p.add_argument(x, required=True)
p = sub.add_parser("judge")
p.add_argument("--on", required=True); p.add_argument("--off", required=True)
p.add_argument("--no-record", action="store_true", help="write the report but no results lines (a trial)")
p = sub.add_parser("noplayer")
p.add_argument("--repo", required=True); p.add_argument("--commit", required=True); p.add_argument("--out", required=True)
p.add_argument("--seeds", default="41"); p.add_argument("--lives", type=int, default=400); p.add_argument("--years", type=int, default=100)
p.add_argument("--worlds", default="off,on,seed"); p.add_argument("--jobs", type=int, default=4)
p.add_argument("--no-record", action="store_true", help="write the report but no results line (a trial)")
a = ap.parse_args()
sys.exit({"run": run, "life": life, "judge": judge, "noplayer": noplayer}[a.cmd](a) or 0)
