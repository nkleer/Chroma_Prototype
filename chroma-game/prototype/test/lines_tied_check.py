"""Clarity item 6, "every line has a cause" (GAME lines_tied): Release's rows L6.1 to L6.4 (records/v22.5 K28). Each
preset's life is played twice through the page's own bridge (test/same_life.py), with lines_tied on and off, and the
two records are read side by side:
  L6.1 same lives: the HUD is the same at every step once its told words are set aside (every "text" and "story"
       string: the switch changes words only)
  L6.2 no stand-alone memory line: no feed entry tagged "memory" (a memory is told inside its moment, or not at all)
  L6.3 the times only in the year's lead: no feed entry tagged "world_year"
  L6.4 every reading shows its color: each "read" entry carries one
    python3 -B test/lines_tied_check.py [--jobs N] [--out DIR]     (from chroma-game/prototype; last line LINES_TIED: PASS)"""
import sys, os, json, argparse, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVES = ((1, 3), (2, 7), (3, 5), (4, 11), (5, 9), (6, 2))   # (preset, seed), as the re-pin's same-lives runs


def play(preset, seed, on, out):
    f = os.path.join(out, f"p{preset}_s{seed}_{'on' if on else 'off'}.jsonl")
    env = dict(os.environ, CHROMA_GAME=json.dumps({"lines_tied": on}), OMP_NUM_THREADS="1")
    subprocess.run([sys.executable, "-B", os.path.join(HERE, "test", "same_life.py"), str(preset), str(seed), f],
                   cwd=HERE, env=env, check=True, stdout=subprocess.DEVNULL)
    return f


def words_aside(x):
    """The HUD without its told words (every "text" and "story" string), as test/same_life.py's text-only checks read it."""
    if isinstance(x, dict):
        return {k: words_aside(v) for k, v in x.items() if k not in ("text", "story")}
    if isinstance(x, list):
        return [words_aside(v) for v in x]
    return x


def feed(path):
    """Every feed entry once, in order (the bridge hands each step's new entries)."""
    out = []
    for line in open(path):
        out.extend(json.loads(line)[3] or [])
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    a.add_argument("--out", default=None)
    a = a.parse_args()
    out = a.out or tempfile.mkdtemp(prefix="lines_tied_")
    os.makedirs(out, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        runs = {(p, s, on): ex.submit(play, p, s, on, out) for p, s in LIVES for on in (True, False)}
    bad = {k: [] for k in ("L6.1", "L6.2", "L6.3", "L6.4")}
    n = dict(memory_off=0, world_year_off=0, inside=0, reads=0)
    for p, s in LIVES:
        on, off = runs[(p, s, True)].result(), runs[(p, s, False)].result()
        A, B = [json.loads(x) for x in open(on)], [json.loads(x) for x in open(off)]
        if len(A) != len(B):
            bad["L6.1"].append(f"preset {p}: {len(A)} steps on, {len(B)} off")
        else:
            i = next((i for i, (x, y) in enumerate(zip(A, B)) if words_aside(x[4]) != words_aside(y[4])), None)
            if i is not None:
                bad["L6.1"].append(f"preset {p}: the HUD differs from step {i}")
        fo, ff = feed(on), feed(off)
        n["memory_off"] += sum(e.get("tag") == "memory" for e in ff)
        n["world_year_off"] += sum(e.get("tag") == "world_year" for e in ff)
        n["inside"] += sum("⟦O:memory|" in (e.get("text") or "") for e in fo)
        bad["L6.2"] += [f"preset {p}: {e.get('text', '')[:80]}" for e in fo if e.get("tag") == "memory"]
        bad["L6.3"] += [f"preset {p}: {e.get('text', '')[:80]}" for e in fo if e.get("tag") == "world_year"]
        reads = [e for e in fo if e.get("tag") == "read"]
        n["reads"] += len(reads)
        bad["L6.4"] += [f"preset {p}: {e.get('text', '')[:80]}" for e in reads if not e.get("color")]
    print(f"lives: presets 1-6 (seeds {', '.join(str(s) for _, s in LIVES)}), each on and off; records in {out}")
    rows = (("L6.1", "same lives (the HUD at every step)", f"{len(LIVES)} presets"),
            ("L6.2", "no stand-alone memory line", f"{n['memory_off']} off; {n['inside']} told inside a moment on"),
            ("L6.3", "the times only in the year's lead", f"{n['world_year_off']} stand-alone off"),
            ("L6.4", "every reading shows its color", f"{n['reads']} readings"))
    for rid, what, info in rows:
        print(f"{rid} {'PASS' if not bad[rid] else 'FAIL'} {what}: {len(bad[rid])} misses ({info})")
        for x in bad[rid][:5]:
            print("       " + x)
    ok = not any(bad.values()) and n["reads"] > 0
    print(f"LINES_TIED: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
