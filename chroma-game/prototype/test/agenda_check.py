"""v25 agenda (GAME agenda, which turns on the Engine's aims v2): the game's checks with it on. Whole Earth lives
through the page's own bridge (console.Console), each moment alternately left to them and pushed to its second way; the
agenda is read at every moment and the terminal's key j is asked once a decade. Reading the agenda draws nothing, so the
lives are the ones played with it on and never read (step, age and text equal: AG3). --forks 1 also puts the player's
forks on fork cards (GAME aim_forks "every"), answered as the moments are.

    python3 -B test/agenda_check.py [--presets 1,2,3,4] [--seeds 1] [--jobs 4] [--forks 0]

    AG1  every life plays to its end with the agenda on (no crash)
    AG2  the agenda is well formed at every moment: each item has its words, a step inside its ladder, a known state,
         priorities 1..n without gaps, forks that name a held aim; capacity words from the game's table
    AG3  the same life with the agenda never read: every step's text, busy, feed and age equal (reading draws nothing)
    AG4  a report: aims on the agenda, how many came with the full engine agenda, forks and bottlenecks seen, fork
         cards a year and the forks still open at the end

Exit 0 when AG1 to AG3 hold, 1 otherwise."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
STATES = {"holding", "pursuing", "reduced", "keeping_up", "paused", "set_aside"}
LOADS = {"room to spare", "full", "stretched", "overcommitted"}


def agenda_bad(A):
    if A is None:
        return ["no agenda"]
    bad = []
    pr = sorted(x["priority"] for x in A["items"])
    if A["full"] and pr != list(range(1, len(pr) + 1)):
        bad.append(f"priorities {pr}")
    slots = {x["slot"] for x in A["items"]}
    for x in A["items"]:
        if not x["aim"] or x["state"] not in STATES or not x["importance"]:
            bad.append(f"item words {x['aim']!r} {x['state']!r}")
        st = x["step"]
        if not (0 <= st["i"] <= st["of"]):
            bad.append(f"step {st}")
        if x["frac"] is not None and not (0 <= x["frac"] <= 1):
            bad.append(f"frac {x['frac']}")
    for f in A["forks"]:
        if f["slot"] not in slots:
            bad.append(f"fork {f['id']} on no held aim")
    for c in A["capacity"]:
        if c["load"] not in LOADS:
            bad.append(f"capacity {c}")
    return bad


def play(preset, seed, out, on):
    sys.path[:0] = [GAME_DIR, HERE]
    os.chdir(GAME_DIR)
    import random
    random.seed(seed)
    import pinned; pinned.ensure()
    from console import Console
    c = Console()
    rec, bad, seen = [], [], dict(items=0, full=0, forks=0, bottlenecks=0, moments=0, cards=0, open_end=0)

    def step(line):
        text, busy = c.handle(line)
        rec.append([line, text, bool(busy), json.dumps(c.take_feed(), sort_keys=True, default=str),
                    round(c.g.age(), 3) if c.g is not None else None])
        return busy
    step(""); step(preset); busy = step("Ari")
    while busy:
        busy = step("")
    k, last_j = 0, -10
    while c.mode == "play" and k < 3000:
        g = c.g
        line = ""
        if g.pending is not None:
            k += 1
            fk = g.pending.get("fork")                    # a fork card put this moment (GAME aim_forks)
            seen["cards"] += bool(fk)
            if fk and not fk.get("on_moment") and k % 2 == 0:   # every other card decided through its review (in both
                # runs: deciding is play; AG3 compares reading the agenda and key j with not reading them)
                R = ((g.hud().get("agenda") or {}).get("reviews") or {}).get(fk.get("review"))
                if R:
                    ch = {f["id"]: next((o["key"] for o in f["options"] if o["key"] != "later"), None) for f in R["forks"]}
                    t, _ = c.handle("agenda apply " + json.dumps(dict(choices={i: o for i, o in ch.items() if o}, set={})))
                    seen["decided"] = seen.get("decided", 0) + 1
                    if re.search(r"\bnan\b", t.lower()) or "{" in t:   # a word, not "governance"
                        bad.append(f"at {g.age():.1f}: review apply: {t[:120]}")
            if on:
                A = g.hud().get("agenda")
                b = agenda_bad(A)
                bad += [f"at {g.age():.1f}: {x}" for x in b]
                if A:
                    seen["moments"] += 1; seen["items"] += len(A["items"]); seen["full"] += A["full"]
                    seen["forks"] += len(A["forks"]); seen["open_end"] = len(A["forks"]); seen["bottlenecks"] += sum(1 for x in A["items"] if x["bottleneck"])
                if g.age() - last_j >= 10:
                    last_j = g.age()
                    t, _ = c.handle("j")
                    if re.search(r"\bnan\b", t.lower()) or "{" in t:
                        bad.append(f"at {g.age():.1f}: key j: {t[:120]}")
            line = "" if k % 2 else "2"
        busy = step(line)
        while busy:
            busy = step("")
    json.dump(dict(preset=preset, seed=seed, age=round(c.g.age(), 2), moments=k, bad=bad, seen=seen, rec=rec),
              open(out, "w"), default=str)


def run(preset, seed, tmp, on, forks=False):
    out = os.path.join(tmp, f"agenda_{os.getpid()}_{preset}_{seed}_{int(on)}.json")
    env = dict(os.environ, CHROMA_GAME=json.dumps(dict(agenda=True, aim_forks="every" if forks else "")))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out, str(int(on))], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, crash=r.returncode)


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, out, on = sys.argv
        return play(preset, int(seed), out, on == "1") or 0
    a = {"presets": "1,2,3,4", "seeds": "1", "jobs": "4", "forks": "0"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    tmp = os.environ.get("TMPDIR", "/tmp")
    seeds = [int(s) for s in a["seeds"].split(",")]
    jobs = [(p, s, on) for p in a["presets"].split(",") for s in seeds for on in (True, False)]
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(j[0], j[1], tmp, j[2], a["forks"] == "1"), jobs))
    by = {(j[0], j[1], j[2]): r for j, r in zip(jobs, res)}
    crash = [r for r in res if "crash" in r]
    bad, same = [], []
    for (p, s, on), r in by.items():
        if not on or "crash" in r:
            continue
        off = by[(p, s, False)]
        bad += r["bad"]
        if "crash" not in off:
            n = min(len(r["rec"]), len(off["rec"]))
            diff = next((i for i in range(n) if r["rec"][i] != off["rec"][i]), None)
            same.append((p, s, len(r["rec"]) == len(off["rec"]) and diff is None, diff if diff is not None else n))
        sn = r["seen"]
        print(f"preset {p} seed {s}: age {r['age']}, {r['moments']} moments; agenda items a moment "
              f"{sn['items'] / max(1, sn['moments']):.1f}, full engine agenda at {sn['full']} of {sn['moments']} moments, "
              f"forks seen {sn['forks']}, bottlenecks {sn['bottlenecks']}; fork cards {sn.get('cards', 0)} "
              f"({sn.get('cards', 0) / max(1.0, r['age'] - 5):.2f} a year, {sn.get('decided', 0)} decided through the review), forks open at "
              f"the end {sn.get('open_end', 0)}")
    print(f"AG1 lives played to their end with the agenda on: {sum(1 for r in res if 'crash' not in r)} of {len(res)}"
          + "".join(f"\n      preset {r['preset']} seed {r['seed']} crashed ({r['crash']})" for r in crash))
    print(f"AG2 problems: {len(bad)}" + "".join("\n      " + b for b in bad[:8]))
    print("AG3 same life with the agenda never read: " + ", ".join(f"preset {p}: {'same' if ok else f'differs at step {d}'}" for p, s, ok, d in same))
    return 0 if not crash and not bad and all(ok for *_, ok, _ in same) else 1


if __name__ == "__main__":
    sys.exit(main())
