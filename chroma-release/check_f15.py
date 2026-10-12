"""v22.5 row K14 (records/v22.5/scope.md): F15, the start leaves a lean, judged on played lives.

    python3 -B chroma-release/check_f15.py run --repo DIR [--commit SHA] [--seeds 1-8] [--far 1-60] [--px JSON]
                                               [--gx JSON] [--jobs N] [--out DIR] [--no-record]
    python3 -B chroma-release/check_f15.py judge DIR [--commit SHA] [--no-record]     # judge a finished run again

`run` plays natural lives (the character always chooses, as the Player impact reads do) of the checkout's game,
chroma-game/prototype with its pinned engine, so at the game's own settings and the pin's DEFAULT: the refit's settings
once they are in. --px lays engine settings over each life's P (the game's CHROMA_ENGINE, JSON) and --gx the game's own
(CHROMA_GAME, JSON), for trying values before they are in; without them neither is set. Every start of PRESETS
(1 to 6) gets --seeds (default 1 to 8); the clan and the towers (the starts whose setting is not earth) get --far
(default 1 to 60). Each life, in its own process, plays to 40 and keeps its pie (softmax of z) at 10, 15, 20, 25,
30, 35 and 40: life_p<preset>_s<seed>.json in --out (default out/f15_<time>/).

The start's lean at an age is the share of the way the pie has gone from even (.2 each) toward the start's upbringing
mix: ((w - .2) . u) / (u . u), u = mix - .2; 0 at even, 1 at the start's own colours.

`judge`, row K14:
  the modern starts (setting earth, with an upbringing: 2, 3, 4): over the lives alive at 35, the mean lean at 35 over
    the mean lean at 15 of the same lives is .35 to .65 ("fades to about half by 35"), each start on its own;
  the clan and the towers (5, 6): each of the five colours leads at least .07 of the lives alive at 40 ("each colour
    can lead about 1 life in 10").
Reported, not judged: the leans by age and the colours leading at 15, 35 and 40 of every start (start 1 has no
upbringing, so no lean). One results line, f15_lean, PASS when every judged part holds, else MISS.
Report: <out>/f15_report.txt. Exit code 0 when it passes.
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = "WUBRG"
AGES = (10, 15, 20, 25, 30, 35, 40)
FADE = (.35, .65)    # lean at 35 over lean at 15, the modern starts
LEAD = .07           # each colour's least share of the lives leading at 40, the clan and the towers


# ---------------------------------------------------------------------------------------------------- one life
def life_main(repo, preset, seed):
    """Plays one natural life to 40 and prints one JSON line: the start, its upbringing mix and the pie at AGES."""
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    sys.path.insert(0, os.path.join(repo, "chroma-game", "prototype"))
    import numpy as np
    import game as G
    E = G.E
    for k_, v_ in list(G.ENGINE_SET.items()):
        if isinstance(v_, list) and k_ in ("f_world", "world_profile"):
            G.ENGINE_SET[k_] = np.asarray(v_, float)
    pr = G.PRESETS[preset]
    g = G.Game(name="Ari", seed=seed, **{k: v for k, v in pr.items() if k not in ("title", "blurb")})
    t0, rec = time.time(), {}
    for A in AGES:
        while not g.over and g.t / 52 < A:
            r = g.advance(until_age=A)
            if r == "checkpoint":
                g.decide(None)
            elif r == "over":
                break
        if g.over:
            break
        rec[str(A)] = [round(float(x), 5) for x in E.softmax(g.loc["z"][0])]
    up = g.up_mix if getattr(g, "up_mix", None) is not None else None
    print(json.dumps(dict(preset=preset, seed=seed, setting=pr.get("setting", "earth"), upbringing=pr.get("upbringing", ""),
                          up_mix=None if up is None else [round(float(x), 5) for x in up], w=rec,
                          end=round(g.t / 52, 2), secs=round(time.time() - t0, 1))))


# ---------------------------------------------------------------------------------------------------- judging
def lean(w, up):
    u = [m - .2 for m in up]
    uu = sum(x * x for x in u)
    return sum((a - .2) * b for a, b in zip(w, u)) / uu if uu else None


def leads(lives, A):
    n = [0] * 5
    for L in lives:
        if str(A) in L["w"]:
            w = L["w"][str(A)]
            n[w.index(max(w))] += 1
    return n


def load(d):
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith("life_") and f.endswith(".json"):
            txt = open(os.path.join(d, f)).read().strip().splitlines()
            if txt:
                out.append(json.loads(txt[-1]))
    return out


def judge(d, commit=None, record=True):
    lives = load(d)
    if not lives:
        sys.exit(f"STOP: no life_*.json in {d}")
    by = {}
    for L in lives:
        by.setdefault(L["preset"], []).append(L)
    ok, lines, notes = True, [], []
    for p in sorted(by, key=lambda s: int(s) if s.isdigit() else s):
        ls = sorted(by[p], key=lambda L: L["seed"])
        L0 = ls[0]
        far = L0["setting"] != "earth"
        seeds = [L["seed"] for L in ls]
        lines.append(f"start {p} ({L0['setting']}, upbringing '{L0['upbringing'] or 'none'}'): {len(ls)} lives, "
                     f"seeds {min(seeds)} to {max(seeds)}")
        up = L0["up_mix"]
        if up:
            row = []
            for A in AGES:
                v = [lean(L["w"][str(A)], up) for L in ls if str(A) in L["w"]]
                if v:
                    row.append(f"{A} {sum(v) / len(v):+.3f}")
            lines.append("       lean (mean of the living): " + ", ".join(row))
        for A in (15, 35, 40):
            n = leads(ls, A)
            lines.append(f"       leading at {A}: " + " ".join(f"{c} {k}" for c, k in zip(COLS, n)) + f" (of {sum(n)})")
        if not far and up:
            alive = [L for L in ls if "35" in L["w"] and "15" in L["w"]]
            if not alive:
                ok = False
                lines.append(f"  MISS start {p}: no life alive at 35")
                notes.append(f"{p} none alive at 35")
                continue
            l15 = sum(lean(L["w"]["15"], up) for L in alive) / len(alive)
            l35 = sum(lean(L["w"]["35"], up) for L in alive) / len(alive)
            r = l35 / l15 if l15 > 0 else None
            good = r is not None and FADE[0] <= r <= FADE[1]
            ok &= good
            lines.append(f"  {'ok  ' if good else 'MISS'} start {p}: lean at 35 over lean at 15, "
                         + (f"{r:.3f}" if r is not None else "none (no lean toward the start at 15)")
                         + f" ({l35:+.3f} over {l15:+.3f}, {len(alive)} lives alive at 35; target {FADE[0]:.2f} to {FADE[1]:.2f})")
            notes.append(f"{p} {r:.2f}" if r is not None else f"{p} no lean at 15")
        elif far:
            n = leads(ls, 40)
            tot = sum(n)
            sh = [k / tot if tot else 0 for k in n]
            good = tot > 0 and min(sh) >= LEAD
            ok &= good
            lines.append(f"  {'ok  ' if good else 'MISS'} start {p}: each colour leads at least {LEAD:.2f} of the lives "
                         f"alive at 40: " + " ".join(f"{c} {s:.3f}" for c, s in zip(COLS, sh)) + f" ({tot} lives)")
            notes.append(f"{p} lowest {COLS[sh.index(min(sh))]} {min(sh):.2f}" if tot else f"{p} none alive at 40")
        else:
            lines.append("       no upbringing, so no start lean: reported only")
        lines.append("")
    want = {"2", "3", "4", "5", "6"}
    if not want <= set(by):
        ok = False
        lines.append(f"MISS: starts not run: {', '.join(sorted(want - set(by)))}")
    head = [f"v22.5 K14 F15 the start leaves a lean (check_f15.py): {len(lives)} played lives"
            + (f", commit {commit[:7]}" if commit else ""), ""]
    body = lines + [f"F15: {'PASS' if ok else 'MISS'}"]
    rep = os.path.join(d, "f15_report.txt")
    open(rep, "w").write("\n".join(head + body) + "\n")
    print("\n".join(head + body))
    if record:
        sys.path.insert(0, HERE)
        import results
        rel = os.path.relpath(rep, os.path.dirname(HERE)) if rep.startswith(os.path.dirname(HERE)) else rep
        results.add("f15_lean", "PASS" if ok else "MISS", report=rel, note=f"{len(lives)} lives; " + "; ".join(notes),
                    candidate={"commit": commit} if commit else None, run=" ".join(sys.argv))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------------- main
def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def span(s):
    a, b = (int(v) for v in s.split("-"))
    return list(range(a, b + 1))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "life":
        life_main(os.path.abspath(arg("--repo", ".")), arg("--preset", "1"), int(arg("--seed", 1)))
        return 0
    if cmd == "judge":
        return judge(sys.argv[2], arg("--commit", os.environ.get("CHROMA_COMMIT")), "--no-record" not in sys.argv)
    if cmd != "run":
        sys.exit(__doc__)
    repo = os.path.abspath(arg("--repo", "."))
    out = os.path.abspath(arg("--out", os.path.join(os.path.dirname(HERE), "chroma-release", "out",
                                                   "f15_" + time.strftime("%Y%m%d-%H%M%S", time.gmtime()))))
    os.makedirs(out, exist_ok=True)
    jobs = int(arg("--jobs", os.cpu_count() or 2))
    sys.path.insert(0, os.path.join(repo, "chroma-game", "prototype"))
    src = open(os.path.join(repo, "chroma-game", "prototype", "game.py"), encoding="utf-8").read()
    presets = {}
    exec(compile(src[src.index("PRESETS = {"):src.index("\n}\n", src.index("PRESETS = {")) + 3], "PRESETS", "exec"), {}, presets)
    presets = presets["PRESETS"]
    near, far = span(arg("--seeds", "1-8")), span(arg("--far", "1-60"))
    todo = [(p, s) for p in presets for s in (far if presets[p].get("setting", "earth") != "earth" else near)]
    env = dict(os.environ)
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        env.setdefault(v, "1")   # one thread a life: the lives run side by side
    for k, a in (("CHROMA_ENGINE", "--px"), ("CHROMA_GAME", "--gx")):
        env.pop(k, None)         # the game reads both as JSON; only --px and --gx set them
        if a in sys.argv:
            env[k] = json.dumps(json.loads(arg(a, "{}")))
    print(f"{len(todo)} lives, {jobs} at a time, into {out}", flush=True)
    t0, live, n_done = time.time(), [], 0
    while todo or live:
        while todo and len(live) < jobs:
            p, s = todo.pop(0)
            nm = os.path.join(out, f"life_p{p}_s{s}")
            f = open(nm + ".json", "w")
            live.append(((p, s), f, subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "life", "--repo", repo,
                                                      "--preset", p, "--seed", str(s)], stdout=f,
                                                     stderr=open(nm + ".log", "w"), env=env)))
        time.sleep(2)
        for item in list(live):
            (p, s), f, pr = item
            if pr.poll() is not None:
                f.close(); live.remove(item); n_done += 1
                if pr.returncode:
                    sys.exit(f"STOP: start {p} seed {s} failed; see {out}/life_p{p}_s{s}.log")
                if n_done % 10 == 0 or not (todo or live):
                    print(f"{n_done} lives done at {time.time() - t0:.0f}s", flush=True)
    return judge(out, arg("--commit", os.environ.get("CHROMA_COMMIT")), "--no-record" not in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
