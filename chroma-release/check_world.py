"""Release check C-E16 (chroma-release/checklist.md, section 9): the outer world tests of
chroma-world/calibration-and-tests.md §2, for rows W1-W37.

Part A runs the Engine's own world checks on a copy of its folder, so their .out files land in the copy and nothing is
written in chroma-engine/:
  calib_v10/world_check.py      §2.1 the world alone (economy, state, culture, eras, institutions, outer ring, symmetry,
                                swing, save and load, determinism, W35 scan, timelessness), §2.5 the world's own speed
  calib_v10/people_check.py     the named cast, place and drawn births (§2.2 network, no close friend, moving, Close
                                first, drawn births; §2.3 reach sizes; §2.6 save, load and a legacy birth)
  calib_v10/lives_in_worlds.py  §2.2 lives in worlds: the scorecard, identities at 40, job loss, births and satisfaction
                                in recessions, world lines a year; on several world seeds, and once with the world off
  calib_v10/world_starts.py     every game preset starts with the world on (plus the birth crash of seed 557247)
Part B adds what those scripts do not test, with the real engine:
  B1 one world per world seed: two runs on the same world seed share recessions, eras and laws; the lives diverge (W1)
  B2 big public events always reach the story; world lines a year (§2.2 "when it matters")
  B3 timeless: no year, brand, real country, person or event in any string the world hands the game (§2.2)
  B4 content still works: every moment met with the world off is still met with it on (§2.4); speed on/off (§2.5)
  B5 the game's link.py anchors still match the engine (§2.4)
  B6 reach: an ordinary push moves nothing national; a minister passes what the norms support and fails more often
     against them; a star moves a norm a little, with a lag (§2.3)
  B7 legacy: a saved world loads and runs on, and a grandchild born into it lives in it with the engine (§2.6)

    python3 -B chroma-release/check_world.py [--quick] [--parts A,B] [--proto DIR] [--lib DIR] [--jobs 3] [--keep]

  --quick   small sizes, to see that everything runs (minutes, not an hour); the final check runs without it. At quick
            sizes the symmetry, swing and timing rows are noisy, and other work on the machine slows the timing rows.
  --proto   the engine folder (default chroma-engine/prototype). --lib: a Library folder instead of chroma-library.
  --keep    keep the working copy (its path is printed).
Writes chroma-release/out/world_<UTC time>.txt with every line printed and the Engine scripts' outputs. Exit code 0 when
nothing is MISS. The thresholds marked "release reading" are this check's reading of a target the spec states in words."""
import sys, os, argparse, subprocess, json, re, shutil, tempfile, time, ast, io, contextlib
from concurrent.futures import ThreadPoolExecutor

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--proto", default=P["engine_v23"])   # calib scripts and engine_v9_golive.py live here (backend item 7 may rename)
ap.add_argument("--lib", default=P["library_live"])
ap.add_argument("--packs-dir", default=P["packs_live"])
ap.add_argument("--game", default=P["game_live"])
ap.add_argument("--quick", action="store_true")
ap.add_argument("--parts", default="A,B")
ap.add_argument("--jobs", type=int, default=3)
ap.add_argument("--keep", action="store_true")
ap.add_argument("--work", default=None)
a = ap.parse_args()
Q = a.quick
PARTS = set(a.parts.upper().split(","))

STAMP = time.strftime("%Y%m%d-%H%M", time.gmtime())
OUTDIR = P["release_out"]; os.makedirs(OUTDIR, exist_ok=True)
REPORT = os.path.join(OUTDIR, f"world_{STAMP}{'_quick' if Q else ''}.txt")
LINES = []; MISSES = []; OKS = [0]


def say(s=""):
    print(s, flush=True); LINES.append(s)


def row(name, value, target, ok):
    """ok: True, False, or None for information only."""
    flag = "info" if ok is None else ("ok  " if ok else "MISS")
    say(f"  {flag} {name}: {value}   (target {target})")
    if ok is False:
        MISSES.append(name)
    elif ok:
        OKS[0] += 1


# ---------------------------------------------------------------------------------------------------- the working copy
WORK = a.work or tempfile.mkdtemp(prefix="chroma_world_check_")
WPROTO = os.path.join(WORK, "chroma-engine", "prototype")
os.makedirs(os.path.join(WPROTO, "calib_v10"), exist_ok=True)
for f in os.listdir(a.proto):
    if f.endswith(".py"):
        shutil.copy2(os.path.join(a.proto, f), WPROTO)
for f in os.listdir(os.path.join(a.proto, "calib_v10")):
    if f.endswith(".py"):
        shutil.copy2(os.path.join(a.proto, "calib_v10", f), os.path.join(WPROTO, "calib_v10"))
for name, src in (("chroma-library", a.lib), ("chroma-packs", a.packs_dir)):   # batch.py reads ../../chroma-library
    dst = os.path.join(WORK, name)
    if not os.path.exists(dst):
        os.symlink(os.path.abspath(src), dst)
say(f"C-E16 outer world tests, {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}{' (quick sizes)' if Q else ''}")
say(f"  engine {os.path.abspath(a.proto)} (copied to {WPROTO}); Library {os.path.abspath(a.lib)}")
ENV = dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")


def run_job(job):
    name, argv = job
    t0 = time.time()
    p = subprocess.run([sys.executable, "-B"] + argv, cwd=WPROTO, env=ENV, capture_output=True, text=True)
    return name, p.returncode, p.stdout, p.stderr, time.time() - t0


def last_json(text):
    for ln in reversed(text.strip().splitlines()):
        ln = ln.strip()
        if ln.startswith("{"):
            try:
                return json.loads(ln)
            except Exception:
                pass
    return None


# ------------------------------------------------------------------------------------------- Part A: the Engine's checks
if "A" in PARTS:
    WS = [11] if Q else [11, 12, 13]
    NL, YL = (60, 70) if Q else (300, 80)
    jobs = [("world_check", ["calib_v10/world_check.py"] + (["30", "15"] if Q else ["200", "100"])),
            ("people_check", ["calib_v10/people_check.py"] + (["150", "60"] if Q else ["600", "80"])),
            ("world_starts", ["calib_v10/world_starts.py", "1", "4" if Q else "20", "2"]),
            ("world_starts 557247", ["calib_v10/world_starts.py", "557247", "1", "2"])]
    jobs += [(f"lives_in_worlds {ws} on", ["calib_v10/lives_in_worlds.py", str(ws), str(NL), str(YL), "on"]) for ws in WS]
    jobs += [(f"lives_in_worlds {WS[0]} off", ["calib_v10/lives_in_worlds.py", str(WS[0]), str(NL), str(YL), "off"])]
    say(f"\nPART A: the Engine's world checks ({len(jobs)} runs, {a.jobs} at a time)")
    res = {jobs[0][0]: run_job(jobs[0])}   # world_check alone first, so its own timing row is not slowed by the others
    with ThreadPoolExecutor(a.jobs) as ex:
        res.update({r[0]: r for r in ex.map(run_job, jobs[1:])})
    with open(os.path.join(OUTDIR, f"world_{STAMP}{'_quick' if Q else ''}_engine_outputs.txt"), "w") as f_:
        for name, rc, out, err, sec in res.values():
            f_.write(f"===== {name} (exit {rc}, {sec:.0f} s)\n{out}\n{err[-4000:]}\n")
    for nm in ("world_check", "people_check"):
        name, rc, out, err, sec = res[nm]
        say(f"\n{nm} (exit {rc}, {sec:.0f} s)")
        if rc != 0:
            row(f"{nm} runs", "crashed: " + (err.strip().splitlines() or ["?"])[-1][:200], "runs to the end", False)
            continue
        seen = set()
        for ln in out.splitlines():
            if re.search(r"\bMISS\b", ln) and not ln.lstrip().startswith(("MISS:", "score:")) and not re.search(r"\d+ ok, \d+ MISS", ln):
                txt = re.sub(r"\s+", " ", ln.replace("MISS", "")).strip().rstrip(":").strip()[:150]
                if txt not in seen:
                    seen.add(txt); row(f"{nm}: " + txt, "", "its own target", False)
        m = re.search(r"(\d+) ok, (\d+) MISS", out) or re.search(r"score: (\d+)/(\d+) ok", out)
        if m:
            say(f"  {nm} summary: {m.group(0)}")
            OKS[0] += int(m.group(1))
    for nm in ("world_starts", "world_starts 557247"):
        name, rc, out, err, sec = res[nm]
        j = last_json(out)
        if rc != 0 or j is None:
            row(f"{nm} runs", "crashed: " + (err.strip().splitlines() or ["?"])[-1][:200], "runs", False)
        else:
            row(f"{nm}: presets x seeds started with the world on", f"{j['ran']} ran, {j['failed']} failed"
                + (f"; first: {j['fails'][0]}" if j["failed"] else ""), "none fails", j["failed"] == 0)
    say(f"\nlives_in_worlds ({NL} lives, {YL} years; world seeds {WS})")
    LW = {}
    for nm in [f"lives_in_worlds {ws} on" for ws in WS] + [f"lives_in_worlds {WS[0]} off"]:
        name, rc, out, err, sec = res[nm]
        j = last_json(out)
        if rc != 0 or j is None:
            row(f"{nm} runs", "crashed: " + (err.strip().splitlines() or ["?"])[-1][:200], "runs", False)
        else:
            LW[nm] = j
    off = LW.get(f"lives_in_worlds {WS[0]} off")
    for ws in WS:
        j = LW.get(f"lives_in_worlds {ws} on")
        if not j:
            continue
        say(f"  world seed {ws}: {j['seconds']} s")
        if off and "scorecard" in j and "scorecard" in off:
            same = ws == WS[0]
            row(f"seed {ws}: survey scorecard, world on" + (" vs off on the same lives" if same else ""),
                f"{j['scorecard']} of {len(j['rows'])}" + (f" vs {off['scorecard']}" if same else ""),
                "at least as well as with the world off", j["scorecard"] >= off["scorecard"] - (0 if same else 1))
        if off:
            d = {k: round(j["identity_at_40"][k] - off["identity_at_40"][k], 3) for k in ("one", "two", "three+")}
            row(f"seed {ws}: identities at 40 (one / two / three+ colors)",
                f"{j['identity_at_40']} (off {off['identity_at_40']})",
                "near today's spread, within .05 of the world off (release reading); today about .20/.62/.17",
                all(abs(v) <= 0.05 for v in d.values()))
        if "job_loss_per_week_recession_vs_not" in j:
            r_, n_ = j["job_loss_per_week_recession_vs_not"]
            row(f"seed {ws}: job loss a week, recession vs not", f"{r_} vs {n_} ({r_ / max(n_, 1e-9):.2f}x)",
                "higher in recessions, about double in deep ones (all recessions pooled: 1.3x or more, release reading)",
                r_ >= 1.3 * n_)
            b_r, b_n = j["births_per_week_recession_vs_not"]
            row(f"seed {ws}: births a week, recession vs not", f"{b_r} vs {b_n}", "fewer in downturns", b_r < b_n)
            s_r, s_n = j["satisfaction_recession_vs_not"]
            row(f"seed {ws}: satisfaction, recession years vs not", f"{s_r} vs {s_n}", "dips in recessions",
                s_r is not None and s_r < s_n)
        else:
            row(f"seed {ws}: recessions in the adult years", j.get("recession_share_of_adult_weeks"), "some", None)
        if "world_lines_a_year" in j:
            row(f"seed {ws}: world lines a year in the log", j["world_lines_a_year"],
                "a handful (2 to 15, release reading; the game's story filters further)", 2 <= j["world_lines_a_year"] <= 15)
            row(f"seed {ws}: no close friend at the end of the run", j.get("no_close_friend_at_end"), "info (people_check has the adult share)", None)

# ------------------------------------------------------------------------------------------------ Part B: the gaps
if "B" in PARTS:
    sys.path.insert(0, WPROTO)
    import numpy as np
    with contextlib.redirect_stdout(io.StringIO()):
        import engine as E, batch, world as WM, world_people as PM, world_link as WLM
    LB = batch.load_batch("earth", packs=list(batch.PACKS))
    say(f"\nPART B: tests the Engine's scripts lack (real engine, {LB['S']} moments)")

    def wrun(N, Y, seed, ws=None, on=True, log=(), **kw):
        P = dict(E.DEFAULT); P.update(world=on, **kw)
        if ws is not None:
            P["world_seed"] = ws
        t0 = time.time()
        with contextlib.redirect_stdout(io.StringIO()):
            o = E.run(N=N, years=Y, seed=seed, lib=LB, P=P, log_lives=log)
        return o, time.time() - t0

    # B1 one world per world seed
    say("\nB1 one world per world seed (W1)")
    N1, Y1 = (6, 30) if Q else (20, 60)
    o1, _ = wrun(N1, Y1, seed=101, ws=77, log=(0, 1))
    o2, _ = wrun(N1, Y1, seed=202, ws=77, log=(0,))
    h1, h2 = o1["world"]["hist"], o2["world"]["hist"]
    m = min(len(h1), len(h2))
    hk = lambda h, k, j: h[k] if isinstance(h, dict) else h[j]   # hist entries are dicts since W35-12 (dict(t, recession, ..., era))
    rec = np.mean([hk(h1[i], 'recession', 1) == hk(h2[i], 'recession', 1) for i in range(m)])
    era = np.mean([hk(h1[i], 'era', 6) == hk(h2[i], 'era', 6) for i in range(m)])
    t0w = o1["world"]["t0"]
    laws = lambda o: {(e["t"], e["key"], str(e["value"])) for e in o["world"]["record"] if e["t"] >= t0w and e["kind"] == "law changed"}
    l1, l2 = laws(o1), laws(o2)
    lshare = len(l1 & l2) / max(len(l1 | l2), 1)
    row("same world seed, other lives: recession months shared", f"{rec:.3f}", ".95 or more", rec >= 0.95)
    row("same world seed, other lives: era months shared", f"{era:.3f}", ".95 or more", era >= 0.95)
    row("same world seed, other lives: law changes shared", f"{lshare:.3f} ({len(l1)} and {len(l2)} changes)", ".9 or more", lshare >= 0.9)
    Wend = np.asarray(o1["W_hist"][-1])
    dist = np.mean([np.abs(Wend[i] - Wend[j]).sum() for i in range(N1) for j in range(i + 1, N1)])
    row("lives in one world diverge by their own choices (mean distance of pies at the end)", f"{dist:.3f}", "clearly above 0 (.05 or more)", dist >= 0.05)

    # B2 big public events reach the story
    say("\nB2 big public events reach the story (§2.2, when it matters)")
    rec_ = [e for e in o1["world"]["record"] if e["t"] > t0w]   # after the birth week (the burn-in's last week is history)
    key = lambda e: (e["t"], e["domain"], e["kind"], str(e["key"]))
    logk = {key(e) for e in o1["world"]["log"]}
    big = [e for e in rec_ if e.get("big")]
    miss_big = [e for e in big if key(e) not in logk]
    row("big public events in the log", f"{len(big) - len(miss_big)} of {len(big)}" + (f"; first missing {miss_big[0]}" if miss_big else ""),
        "all", not miss_big)
    row("big public events a year", f"{len(big) / Y1:.1f}", "info", None)
    wl = [sum(1 for e in o1["events"][n] if "world" in e) / Y1 for n in (0, 1)]
    row("world lines a year in a logged life's events", f"{wl[0]:.1f} and {wl[1]:.1f}", "a handful (1 to 15, release reading)",
        all(1 <= x <= 15 for x in wl))

    # B3 timeless
    say("\nB3 timeless modern days (Emren 10-06 10:42)")
    REAL = None
    try:
        tree = ast.parse(open(os.path.join(a.game, "test", "timeless.py")).read())
        for nd in tree.body:
            if isinstance(nd, ast.Assign) and getattr(nd.targets[0], "id", "") == "REAL":
                REAL = re.compile(nd.value.args[0].value, re.I)
    except Exception as ex_:
        say(f"  could not read the game's word list: {ex_!r}")
    if REAL is None:
        row("the game's timeless word list", "not found", "found", False)
    else:
        def strings(x, skip=("save", "people", "rng", "bit_generator")):
            if isinstance(x, str):
                yield x
            elif isinstance(x, dict):
                for k, v in x.items():
                    if k not in skip:
                        yield from strings(k if isinstance(k, str) else "", skip); yield from strings(v, skip)
            elif isinstance(x, (list, tuple)):
                for v in x:
                    yield from strings(v, skip)
        hits = {}
        for o in (o1, o2):
            evs = o["events"].values() if isinstance(o["events"], dict) else o["events"]
            for s_ in list(strings(o["world"])) + list(strings([[e for e in ev if "world" in e or "world_push" in e] for ev in evs])):
                for mm in REAL.finditer(s_):
                    hits.setdefault(mm.group(0).lower(), s_[:120])
        row("strings the world hands the game with a year, brand, real place, person or event",
            "none" if not hits else "; ".join(f"{k}: {v}" for k, v in list(hits.items())[:5]), "none", not hits)

    # B4 content still works, and speed
    say("\nB4 content still works with the world on (§2.4), and speed (§2.5)")
    N4, Y4 = (40, 70) if Q else (300, 80)
    off4, t_off = wrun(N4, Y4, seed=404, on=False)
    on4, t_on = wrun(N4, Y4, seed=404, ws=404, on=True)
    met_off = (np.asarray(off4["sit_n"]) > 0).sum(0); met_on = (np.asarray(on4["sit_n"]) > 0).sum(0)
    names = LB["names"]; WMOM = {w_[3] for w_ in WLM.WORLD_MOMENTS}
    # lost: met by none with the world on although that is a 1-in-1,000 chance or less. Two samples of the same size: if
    # the world changed nothing, all k lives that meet it fall in the world-off run with probability C(N,k)/C(2N,k)
    # (Fisher, one-sided). Until 10-07 14:26 (UTC+3) this read the off share as the true rate, which ignores the off run's own
    # noise and flagged a rare Science moment (8 off, 0 on) that a focused rerun showed is met with the world on.
    p_all_off = lambda k: float(np.prod([(N4 - j) / (2 * N4 - j) for j in range(int(k))]))
    lost = [f"{names[i]} ({int(met_off[i])} off, 0 on)" for i in range(len(names))
            if met_on[i] == 0 and names[i] not in WMOM and p_all_off(met_off[i]) < 1e-3]
    row(f"moments that {N4} lives meet with the world off and never with it on (by chance 1 in 1,000 or less)",
        "none" if not lost else f"{len(lost)}: " + ", ".join(lost[:12]), "none (the world's own moments aside)", not lost)
    gone_w = [nm for nm in WMOM if nm in names and met_on[names.index(nm)] == 0]
    row("the world's own moments (world_link.WORLD_MOMENTS) met with the world on", f"{len(WMOM & set(names)) - len(gone_w)} of {len(WMOM & set(names))}"
        + (f"; never: {', '.join(gone_w)}" if gone_w else ""), "info (they need their event in the run)", None)
    big_shift = [(names[i], int(met_off[i]), int(met_on[i])) for i in range(len(names))
                 if met_off[i] >= 10 and (met_on[i] > 3 * met_off[i] or met_on[i] * 3 < met_off[i])]
    row("moments whose reach moves more than 3x with the world on", f"{len(big_shift)}" + (f", e.g. {big_shift[:6]}" if big_shift else ""),
        "info (the world's rates by season, place and law move them on purpose)", None)
    row("time with the world on vs off, same lives", f"{t_on:.0f} s vs {t_off:.0f} s ({t_on / max(t_off, 1e-9):.2f}x)",
        "at most about 1.33x (C-E15 speed_check.py is the measure)", t_on <= 1.33 * t_off)

    # B5 the game's link.py anchors
    say("\nB5 the game's link.py still finds its anchors (§2.4)")
    try:
        src = open(os.path.join(a.game, "link.py")).read(); tree = ast.parse(src); keep = []
        for nd in tree.body:
            if isinstance(nd, ast.Assign) and getattr(nd.targets[0], "id", "") in ("PATCHES", "SIG"):
                keep.append(nd)
            elif isinstance(nd, ast.FunctionDef) and nd.name == "_with_steps":
                keep.append(nd)
        ns = {}
        exec(compile(ast.Module(body=keep, type_ignores=[]), "link.py", "exec"), ns)
        ns["_with_steps"](open(os.path.join(WPROTO, "engine.py")).read())
        row("every anchor of the game's link.py found once in today's engine.py", f"{len(ns['PATCHES'])} anchors and run()'s signature", "all", True)
    except Exception as ex_:
        row("every anchor of the game's link.py found once in today's engine.py", str(ex_).splitlines()[0][:200]
            + " (the game re-pins after the refit and moves its anchors)", "all", False)

    # B6 reach
    say("\nB6 reach (§2.3), on the world itself")
    LI = {k: i for i, k in enumerate(WM.LAW_KEYS)} if hasattr(WM, "LAW_KEYS") else None
    clone = lambda W: WM.World.load(json.loads(json.dumps(W.save())))   # a JSON round trip: no state shared between clones
    Wb = WM.World(5150, cfg={}); Wb.burn_in(80)
    A_, B_ = clone(Wb), clone(Wb)
    nk = WM.NORM_KEYS[0]
    for _ in range(52):
        A_.push("state", "support", 0.0, +1); A_.push("culture", nk, 0.0, +1); A_.push("state", WM.LAW_KEYS[0], 0.0, +1)
        A_.tick(); B_.tick()
    gap = max(abs(A_.support - B_.support), float(np.max(np.abs(A_.norm_x - B_.norm_x))), float(np.max(np.abs(A_.laws - B_.laws))),
              abs(float(getattr(A_, "unemp", 0)) - float(getattr(B_, "unemp", 0))))
    row("an ordinary voice pushing every week for a year: largest change in support, norms, laws, unemployment", f"{gap:.2g}",
        "not measurable (1e-4 or less)", gap <= 1e-4)
    K6 = 12 if Q else 40
    tally = {True: [0, 0, 0], False: [0, 0, 0]}   # norms support?: [pushed and moved, baseline moved, cases]
    one = {True: [0, 0], False: [0, 0]}           # a single act: [moved, cases]
    for k6 in range(K6):
        W6 = WM.World(6000 + k6, cfg={}); W6.burn_in(60)
        base = json.dumps(W6.save())
        for key, j in LI.items():
            if W6.laws[j] == 0 or key == "conscription":
                continue
            sup = W6.norm(key) >= 0.5
            A6, B6, C6 = (WM.World.load(json.loads(base)) for _ in range(3))
            for wk in range(104):
                if A6.t % 13 == 12:
                    A6.push("state", key, 3.0, +1)
                if wk == 0:
                    C6.push("state", key, 3.0, +1)
                A6.tick(); B6.tick(); C6.tick()
            one[sup][0] += int(C6.laws[j] < W6.laws[j]); one[sup][1] += 1
            tally[sup][0] += int(A6.laws[j] < W6.laws[j]); tally[sup][1] += int(B6.laws[j] < W6.laws[j]); tally[sup][2] += 1
    rate = {s: (tally[s][0] / max(tally[s][2], 1), tally[s][1] / max(tally[s][2], 1), tally[s][2]) for s in (True, False)}
    row("a minister pushing a law toward legal for two years, where the norms support it: passed vs without the push",
        f"{rate[True][0]:.2f} vs {rate[True][1]:.2f} ({rate[True][2]} cases)", "passes, and clearly more often than without",
        rate[True][2] > 0 and rate[True][0] >= 0.5 and rate[True][0] > rate[True][1] + 0.1)
    row("the same against the norms: passed vs without the push", f"{rate[False][0]:.2f} vs {rate[False][1]:.2f} ({rate[False][2]} cases)",
        "info: a two-year campaign at full strength; the single act below is the test", None)
    o1r = {s_: one[s_][0] / max(one[s_][1], 1) for s_ in (True, False)}
    row("a single act of a minister: passed within two years, with the norms vs against them",
        f"{o1r[True]:.2f} vs {o1r[False]:.2f} ({one[True][1]} and {one[False][1]} cases)",
        "against the norms at least .1 less often (release reading)", one[False][1] == 0 or o1r[False] <= o1r[True] - 0.1)
    A7, B7 = clone(Wb), clone(Wb)
    j7 = WM.NORM_KEYS.index(nk)
    while A7.t % 13 != 11:
        A7.tick(); B7.tick()
    A7.push("culture", nk, 2.0, +1)
    A7.tick(); B7.tick()
    lag0 = abs(A7.norm(nk) - B7.norm(nk))
    for _ in range(51):
        A7.tick(); B7.tick()
    yr = A7.norm(nk) - B7.norm(nk)
    row("a star's work on a norm: change before the next quarter, after a year", f"{lag0:.2g}, {yr:+.4f}",
        "none at once, then a little (above 0, under .05)", lag0 == 0 and 0 < yr < 0.05)

    # B7 legacy worlds
    say("\nB7 legacy worlds (§2.6), with the engine")
    try:
        o7, _ = wrun(1, 30 if Q else 50, seed=707, ws=707, log=(0,))
        sv, pv = o7["world"]["save"], o7["world"]["people"][0]
        js = json.dumps(sv); W2 = WM.World.load(json.loads(js))
        snap = o7["world"]["snapshot"]
        row("a saved world loads where it stopped (week, laws, era)", f"week {W2.t} vs {snap['t']}; laws equal {list(W2.snapshot()['laws']) == list(snap['laws'])}; era {W2.snapshot()['era']} vs {snap['era']}",
            "the same", W2.t == snap["t"] and W2.snapshot()["laws"] == snap["laws"] and W2.snapshot()["era"] == snap["era"])
        t_before = W2.t   # the game's route (next-handoff.md, World-on fixes): world_obj, and world_cfg legacy = People.save()
        o8, _ = wrun(1, 5, seed=708, world_obj=W2, world_cfg=dict(legacy=json.loads(json.dumps(pv))), log=(0,))
        row("a grandchild born into the saved world lives in it", f"ran 5 years; world week {t_before} to {W2.t}; first era {(lambda h: h['era'] if isinstance(h, dict) else h[6])(o8['world']['hist'][0])}",
            "runs on from the saved week", abs(W2.t - (t_before + 5 * 52)) <= 1 and o8["world"]["t0"] == t_before)
    except Exception as ex_:
        import traceback
        row("legacy: save, load and a grandchild's life", f"crashed: {ex_!r}"[:200] + " | " + traceback.format_exc().strip().splitlines()[-3][:150], "runs", False)

# -------------------------------------------------------------------------------------------------------------- result
say(f"\nC-E16: {'PASS' if not MISSES else 'FAIL'}; {OKS[0]} ok, {len(MISSES)} MISS")
for m_ in MISSES:
    say(f"  MISS: {m_}")
with open(REPORT, "w") as f_:
    f_.write("\n".join(LINES) + "\n")
say(f"report: {REPORT}")
if not a.keep and not a.work:
    shutil.rmtree(WORK, ignore_errors=True)
else:
    say(f"working copy kept: {WORK}")
import results; results.done('world', 0 if not MISSES else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if not MISSES else 1)
