"""The "no change in play" proof in one command: the smoke test, then whole played lives (presets 1 to 6, seed 7, the
record and md5 of test/same_life.py) on this tree and on a base, side by side, compared step by step.

    python3 -B test/prove.py                  compare with origin/main (or --base REF)
    python3 -B test/prove.py --presets 1,3    only those presets
    python3 -B test/prove.py --fresh          ignore the cache and play every life again

Lives are kept in a cache keyed by the game files they were played from, so a base is played once per state of its game
files, by whichever session gets there first, and a tree whose game files match the base's is the same by construction.
The game files are everything under chroma-game/prototype except test/, web/ and *.md, with engine_pin/ as the files it
holds: a committed pin's, else the owners' engine, Library and packs files that chroma-game/tools/pin.py fills it from
(both trees' engine_pin/ are filled that way before they play). The cache
is $CHROMA_PROOF_CACHE, else /mnt/project-files/.cache/same-lives when the shared folder exists, else
~/.cache/chroma/same-lives; an entry also needs the same Python, numpy, CHROMA_GAME and CHROMA_ENGINE. A base not in the cache is played from a
temporary git worktree of REF, removed afterwards. Prints one line per preset and a verdict; exit 0 when every life
matches and the smoke test passes. When a life differs, it names the first step that differs and its age.
"""
import hashlib, json, os, platform, random, shutil, subprocess, sys, tempfile, time

# The engine keeps each burned-in world in CHROMA_WORLD_CACHE (world_link.burned_world: one file per seed and settings,
# named by the md5 of the code that burns it in and Python's and numpy's versions), so a new life skips its burn-in
# (about 4 s). A set CHROMA_WORLD_CACHE wins, and an empty one turns it off. Not while CHROMA_ENGINE or CHROMA_GAME
# change settings in-process, which the file name does not cover (Engine, 2026-10-17).
if not (os.environ.get("CHROMA_ENGINE") or os.environ.get("CHROMA_GAME")):
    os.environ.setdefault("CHROMA_WORLD_CACHE", os.path.join(tempfile.gettempdir(), "chroma_world_cache"))

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
SKIP = ("test/", "web/")
sys.path.insert(0, HERE)
import pinned  # noqa: E402


def git(*a, cwd=GAME):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout


def versions():
    import numpy as np
    return f"py{platform.python_version()}-np{np.__version__}"


def settings_tag():
    """The cache entry's settings: Python's and numpy's versions, and CHROMA_GAME and CHROMA_ENGINE when set, so a life
    played with other settings is never taken for this one."""
    env = "|".join(os.environ.get(k, "") for k in ("CHROMA_GAME", "CHROMA_ENGINE"))
    return versions() + (f"-env{hashlib.md5(env.encode()).hexdigest()[:8]}" if env != "|" else "")


def tree_key(ref=None):
    """A hash over the game files' paths and git blob ids, of REF, or of the working tree (untracked files included)."""
    top = git("rev-parse", "--show-toplevel").strip()
    pre = os.path.relpath(GAME, top).replace(os.sep, "/") + "/"
    if ref:
        rows = [ln.split(None, 3) for ln in git("ls-tree", "-r", ref, "--", pre, cwd=top).splitlines()]
        files = {r[3][len(pre):]: r[2] for r in rows}
    else:
        names = git("ls-files", "-co", "--exclude-standard", "--", pre, cwd=top).splitlines()
        names = [n for n in names if os.path.isfile(os.path.join(top, n))]
        ids = git("hash-object", "--", *names, cwd=top).split() if names else []
        files = {n[len(pre):]: i for n, i in zip(names, ids)}
    files = {f: i for f, i in files.items() if not f.startswith(SKIP) and not f.endswith(".md")
             and not (f.startswith("engine_pin/PINNED") and f.endswith(".txt"))}
    if not any(f.startswith("engine_pin/") for f in files):     # no committed pin: the owners' files it is filled from
        files.update(pin_ids(ref, top))
    return hashlib.sha1("".join(f"{f} {files[f]}\n" for f in sorted(files)).encode()).hexdigest()[:16]


def pin_ids(ref, top):
    """{engine_pin/<path>: blob id} of the owners' files chroma-game/tools/pin.py fills engine_pin/ from, at REF or in the
    working tree."""
    sys.path.insert(0, pinned.TOOLS)
    import pin as P
    o = P.owners(top)
    rel = lambda p: os.path.relpath(p, top).replace(os.sep, "/")
    if ref is None:
        pins = P.plan(o["engine"], o["lib"], o["packs"])[0]
        ids = git("hash-object", "--", *[s for s, _ in pins], cwd=top).split()
        return {"engine_pin/" + d: i for (_, d), i in zip(pins, ids)}
    rows = [ln.split(None, 3) for ln in git("ls-tree", "-r", ref, "--", *[rel(d) for d in o.values()], cwd=top).splitlines()]
    blob = {r[3]: r[2] for r in rows}
    ls = lambda d: sorted({f[len(rel(d)) + 1:].split("/")[0] for f in blob if f.startswith(rel(d) + "/")})
    read = lambda p: git("show", f"{ref}:{rel(p)}", cwd=top)
    pins = P.plan(o["engine"], o["lib"], o["packs"], ls=ls, read=read, isfile=lambda p: rel(p) in blob)[0]
    return {"engine_pin/" + d: blob[rel(s)] for s, d in pins}


def cache_dir():
    d = os.environ.get("CHROMA_PROOF_CACHE") or ("/mnt/project-files/.cache/same-lives" if os.path.isdir("/mnt/project-files")
                                                 else os.path.expanduser("~/.cache/chroma/same-lives"))
    os.makedirs(d, exist_ok=True)
    return d


def cache_get(key, preset, seed):
    p = os.path.join(cache_dir(), f"{key}-{settings_tag()}-p{preset}-s{seed}.json")
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return None


def cache_put(key, preset, seed, res):
    p = os.path.join(cache_dir(), f"{key}-{settings_tag()}-p{preset}-s{seed}.json")
    tmp = f"{p}.{os.getpid()}.tmp"
    json.dump(dict(res, made=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), host=platform.node()), open(tmp, "w"))
    os.replace(tmp, p)


def life(game_dir, preset, seed):
    """One whole life as test/same_life.py plays it (same record, same md5), with each step's md5 and age kept."""
    sys.path.insert(0, game_dir)
    import numpy as np
    random.seed(seed)
    from console import Console
    c = Console()

    def dflt(o):
        if isinstance(o, np.generic):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)

    h, steps, ages = hashlib.md5(), [], []

    def step(line):
        text, busy = c.handle(line)
        rec = json.dumps([line, text, bool(busy), c.take_feed(), c.hud()], default=dflt, sort_keys=True).encode()
        h.update(rec)
        steps.append(hashlib.md5(rec).hexdigest()[:12])
        ages.append(round(float(c.g.age()), 2) if c.g is not None else None)
        return busy

    step(""); step(preset); step("Ari")
    k = 0
    while c.mode == "play" and len(steps) < 20000:
        line = ""
        if c.g is not None and c.g.pending is not None:
            k += 1
            line = "" if k % 2 else "2"
        while step(line):
            line = ""
    return dict(md5=h.hexdigest(), n=len(steps), age=ages[-1], steps=steps, ages=ages)


def args():
    a = sys.argv[1:]
    def val(k, d):
        return a[a.index(k) + 1] if k in a else d
    return dict(base=val("--base", "origin/main"), presets=val("--presets", "1,2,3,4,5,6").split(","),
                seed=int(val("--seed", "7")), jobs=int(val("--jobs", str(os.cpu_count() or 2))), fresh="--fresh" in a)


def main():
    if sys.argv[1:2] == ["life"]:   # worker: prove.py life <game dir> <preset> <seed>
        print(json.dumps(life(sys.argv[2], sys.argv[3], int(sys.argv[4]))))
        return 0
    o = args()
    t0 = time.time()
    pinned.ensure(GAME)                         # engine_pin/ from the owners' folders (chroma-game/tools/pin.py)
    gold = json.load(open(os.path.join(HERE, "smoke.golden.json")))
    same = ["--same"] if f"py{gold['python']}-np{gold['numpy']}" == versions() else []   # its stored md5s fit this Python
    smoke = subprocess.Popen([sys.executable, "-B", os.path.join(HERE, "smoke.py"), *same], stdout=subprocess.PIPE, text=True)
    here_key, base_key = tree_key(), tree_key(o["base"])
    same_files = here_key == base_key
    print(f"game files: this tree {here_key}, {o['base']} {base_key}"
          + ("  (the same: lives match by construction)" if same_files else ""))
    want = {}   # (side, preset) -> result, from the cache or to play
    todo = []
    for side, key in (("here", here_key), ("base", base_key)):
        if same_files:   # nothing to play: the same files play the same lives
            break
        for p in o["presets"]:
            got = None if o["fresh"] else cache_get(key, p, o["seed"])
            if got:
                want[side, p] = got
            else:
                todo.append((side, key, p))
    wt = None
    if any(s == "base" for s, _, _ in todo):
        wt = tempfile.mkdtemp(prefix="prove-base-")
        top = git("rev-parse", "--show-toplevel").strip()
        git("worktree", "add", "--detach", "-f", wt, o["base"], cwd=top)
        pinned.ensure(os.path.join(wt, os.path.relpath(GAME, top)))    # a base without a committed pin: filled the same way
    try:
        if todo:
            print(f"playing {len(todo)} {'life' if len(todo) == 1 else 'lives'}, {o['jobs']} at a time (about 2 minutes each); "
                  f"{len(want)} from the cache", flush=True)
        live = []
        base_game = wt and os.path.join(wt, os.path.relpath(GAME, git("rev-parse", "--show-toplevel").strip()))
        while todo or live:
            while todo and len(live) < o["jobs"]:
                side, key, p = todo.pop(0)
                cmd = [sys.executable, "-B", os.path.abspath(__file__), "life", GAME if side == "here" else base_game, p, str(o["seed"])]
                live.append((side, key, p, subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)))
            time.sleep(0.5)
            for x in [x for x in live if x[3].poll() is not None]:
                live.remove(x)
                side, key, p, pr = x
                out, err = pr.communicate()
                if pr.returncode:
                    want[side, p] = dict(error=err.strip().splitlines()[-1] if err.strip() else f"exit {pr.returncode}")
                    continue
                res = json.loads(out.strip().splitlines()[-1])
                cache_put(key, p, o["seed"], res)
                want[side, p] = res
    finally:
        if wt:
            subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=GAME, capture_output=True)
            shutil.rmtree(wt, ignore_errors=True)
    ok = True
    for p in o["presets"]:
        if same_files:
            print(f"preset {p}: same (the same game files)")
            continue
        a, b = want[("here", p)], want[("base", p)]
        if "error" in a or "error" in b:
            print(f"preset {p}: FAIL, a life crashed: {a.get('error') or b.get('error')}")
            ok = False
        elif a["md5"] == b["md5"]:
            print(f"preset {p}: same, {a['n']} steps to age {a['age']}, md5 {a['md5']}")
        else:
            i = next((i for i, (x, y) in enumerate(zip(a["steps"], b["steps"])) if x != y), min(a["n"], b["n"]))
            print(f"preset {p}: DIFFERENT from step {i + 1} (age {a['ages'][min(i, a['n'] - 1)]}): md5 {a['md5']} here, "
                  f"{b['md5']} on {o['base']}; test/same_life.py {p} {o['seed']} <out> on both shows the records")
            ok = False
    s = smoke.communicate()[0].strip().splitlines()
    print("smoke:", s[-1] if s else "no output")
    ok &= smoke.returncode == 0
    print(f"prove: {'SAME as ' + o['base'] if ok else 'NOT the same, or a check failed'} in {time.time() - t0:.0f} s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
