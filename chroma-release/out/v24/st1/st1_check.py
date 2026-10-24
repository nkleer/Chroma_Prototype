"""v24 ST1 steer_vs_asks (records/v24/scope.md; plan.md §7, "Guard for steering between asks"): across a life, steering
between asks moves the colours less than the player's own picks at the asks do. Whole Earth lives on the Game object as
the page plays it (Release's picks/impact.py play()), each preset and seed played three ways with the same seed:
  base   the voice lets them choose at every ask (impact's `let`)
  steer  as base, and between asks the player leans them toward colour C (the Game's steer_between, as its own
         test/steer_between_check.py does it: from age 16, again whenever no lean is held and no moment waits)
  pick   no lean; at every ask the player pushes the option with most of C (impact's `steer:C`)
with CHROMA_GAME {"steer_between": true, "talk": false} laid over the commit's settings ("Talk to them" off, as the row
says). Release's reading: a way's shift is its share of C minus the base life's, both read each year from 16 (the
engine's colours, softmax z, as impact records them) and averaged over the years lived (across a life); ST1 holds when
the mean shift by steering is below the mean shift by picks, pooled over every preset, seed and colour. The shift at
the end of life and the total variation from the base life are printed beside it, and each colour alone.

    python3 -B st1_check.py <game dir with engine_pin filled> [--colors R,U] [--presets 1,2,3,4] [--seeds 1-3] [--jobs 4] [--out REPORT]

Exit 0 when ST1 holds, 1 when it does not, 2 when a life did not play to its end."""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.abspath(__file__)
SET = {"steer_between": True, "talk": False}
CI = {c: i for i, c in enumerate("WUBRG")}


def play(gdir, way, color, preset, seed, out):
    os.environ.update(PRESET=preset, GAMEDIR=gdir, OMP_NUM_THREADS="1")
    sys.path.insert(0, "/mnt/project-files/chroma-release/picks")
    import impact                                   # puts the game first on sys.path and chdirs there
    import game as G
    held = {}
    if way == "steer":
        orig = G.Game.advance

        def advance(self, *a, **k):
            held["g"] = self
            if self.pending is None and self.age() >= 16 and self.steer_view() is None:
                self.steer_set(color)
            return orig(self, *a, **k)
        G.Game.advance = advance
    else:
        orig = G.Game.advance

        def advance(self, *a, **k):
            held["g"] = self
            return orig(self, *a, **k)
        G.Game.advance = advance
    r = impact.play(int(seed), f"steer:{color}" if way == "pick" else "let")
    g = held["g"]
    ws = [(y["age"], y["w"]) for y in r["yrs"] if y["age"] >= 16 and y.get("w")]
    steers = [x for x in g.history.get("steers", []) if x.get("kind") == "between"]
    json.dump(dict(way=way, color=color, preset=preset, seed=int(seed), age=r["age"], n_cp=r["n_cp"], n_push=r["n_push"],
                   moved=len(steers), years=len(ws), w16=[w for _, w in ws], w_end=ws[-1][1] if ws else None),
              open(out, "w"))


def run(gdir, tmp, way, color, preset, seed):
    out = os.path.join(tmp, f"st1_{way}_{color}_{preset}_{seed}.json")
    if os.path.exists(out):
        return json.load(open(out))
    env = dict(os.environ)
    g = json.loads(env.get("CHROMA_GAME") or "{}") if env.get("CHROMA_GAME") not in (None, "", "off") else {}
    g.update(SET); env["CHROMA_GAME"] = json.dumps(g)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-B", HERE, "_play", gdir, way, color, preset, str(seed), out], env=env,
                       capture_output=True, text=True)
    if p.returncode or not os.path.exists(out):
        return dict(way=way, color=color, preset=preset, seed=seed, crash=p.returncode, err=p.stderr[-400:])
    r = json.load(open(out)); r["secs"] = round(time.time() - t0); json.dump(r, open(out, "w"))
    return r


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    if sys.argv[1:2] == ["_play"]:
        return play(*sys.argv[2:8]) or 0
    gdir = os.path.abspath(sys.argv[1])
    a = {"colors": "R,U", "presets": "1,2,3,4", "seeds": "1-3", "jobs": "4", "out": "", "tmp": ""}
    args = sys.argv[2:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    lo, _, hi = a["seeds"].partition("-")
    seeds = range(int(lo), int(hi or lo) + 1); cols = a["colors"].split(","); pres = a["presets"].split(",")
    tmp = a["tmp"] or os.path.join(os.environ.get("TMPDIR", "/tmp"), f"st1_{os.getpid()}"); os.makedirs(tmp, exist_ok=True)
    jobs = [("base", cols[0], p, s) for p in pres for s in seeds] + \
           [(w, c, p, s) for w in ("steer", "pick") for c in cols for p in pres for s in seeds]
    t0 = time.time()
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(gdir, tmp, *j), jobs))
    crash = [r for r in res if "crash" in r]
    base = {(r["preset"], r["seed"]): r for r in res if r["way"] == "base" and "crash" not in r}
    rows = {}
    for r in res:
        if r["way"] == "base" or "crash" in r or (r["preset"], r["seed"]) not in base:
            continue
        b = base[(r["preset"], r["seed"])]; ci = CI[r["color"]]
        mb, mr = mean([w[ci] for w in b["w16"]]), mean([w[ci] for w in r["w16"]])
        tv = 0.5 * sum(abs(x - y) for x, y in zip(r["w_end"], b["w_end"]))
        rows.setdefault((r["way"], r["color"]), []).append(dict(life=mr - mb, end=r["w_end"][ci] - b["w_end"][ci], tv=tv,
                                                                  moved=r["moved"], push=r["n_push"], cp=r["n_cp"]))
    rep = [f"v24 ST1 steer_vs_asks on {gdir}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC; "
           f"colours {','.join(cols)}, presets {','.join(pres)}, seeds {a['seeds']}; CHROMA_GAME over the commit's: {json.dumps(SET)}",
           f"{len(res)} lives, {len(crash)} did not play to their end; {round((time.time() - t0) / 60)} min", ""]
    for r in crash:
        rep.append(f"  CRASH {r['way']} {r['color']} preset {r['preset']} seed {r['seed']} (exit {r['crash']}): {r.get('err', '')[-200:]}")
    pooled = {}
    for way in ("steer", "pick"):
        allr = [x for c in cols for x in rows.get((way, c), [])]
        pooled[way] = mean([x["life"] for x in allr])
        for c in cols:
            xs = rows.get((way, c), [])
            rep.append(f"  {way:<5} toward {c}: share of {c} over the life {mean([x['life'] for x in xs]):+.3f}, at the end "
                       f"{mean([x['end'] for x in xs]):+.3f}, total variation at the end {mean([x['tv'] for x in xs]):.3f} "
                       f"({len(xs)} lives; choices moved by the lean {mean([x['moved'] for x in xs]):.0f} a life, pushes at asks "
                       f"{mean([x['push'] for x in xs]):.1f} of {mean([x['cp'] for x in xs]):.0f} asks)")
        rep.append(f"  {way:<5} pooled: shift over the life {pooled[way]:+.3f}")
    ok = not crash and pooled["steer"] < pooled["pick"]
    rep += ["", f"ST1: {'PASS' if ok else ('NOT READ' if crash else 'FAIL')}: steering moves the colours {pooled['steer']:+.3f} "
            f"over a life, the picks at the asks {pooled['pick']:+.3f}"]
    txt = "\n".join(rep) + "\n"
    if a["out"]:
        open(a["out"], "w").write(txt)
    print(txt)
    return 2 if crash else (0 if ok else 1)


if __name__ == "__main__":
    sys.exit(main())
