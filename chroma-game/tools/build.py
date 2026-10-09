"""The one build command (backend plan item 5): a release candidate of the game, assembled from the owners' files.

    python3 -B chroma-game/tools/build.py <out dir> [--root DIR] [--game G] [--engine E] [--lib L] [--packs K]
                                          [--same-as DIR] [--live-paths FILE] [--serve] [--rarity FILE|engine]

Inputs are the folders chroma-env/paths.py names (game_live, engine_live, library_live, packs_live, art), found under
--root (default: the tree this script sits in, so the shared folder's copy builds from the shared folder and a checkout's
copy from that checkout; CHROMA_ROOT overrides it).
--game, --engine, --lib and --packs take a paths.py name or a folder, for a candidate in place of the live one.
--rarity takes the rarity table for rarity.py: by default the game's own pin, rarity.json in the game folder, when it
has one (v22.2: Release's rebuild of 2026-10-08 on v22.1, chroma-release/out/rarity_rebuild_20261008-1504.json, B1,
which fixes the Book's "rare" labels; stage 1 moves no rates), else the engine's rarity.json; "engine" takes the
engine's (as v22.1 was built). Replace the pin only with a new rebuild after a rate change.
Every input is read only; the build writes only under <out dir>, which must not exist yet:

  chroma-game/prototype   the game, with engine_pin/ pinned fresh from the engine, Library and packs, rarity.py from the
                          rarity table (--rarity), the worker's SOURCES completed, and web/index.html built
  chroma-art              a link to the art folder (the page build reads ../../../../chroma-art/game, as in the repo)
  web/                    index.html (the page to publish), page.html (the same in a document, to serve), worker.js,
                          py/ and pics/ (webdir.py); with --serve also a link to the Pyodide copy that the release
                          thread keeps (chroma-release/tools/pyodide), so test/serve.py can serve it to the browser checks
  publish.json            the Artifact files map (pubmap.py; with --live-paths, pictures already live are left out)
  BUILD.md                the inputs with the md5 of every pinned file, the outputs, and the checks below

It stops at the first failed check:
  1. Library: the Library's own build.py compiles earth.py from its .lib sources byte for byte as the Library keeps it.
  2. Pin (C-X1): every pinned file equals its owner's copy, and every worker source exists.
  3. Load: the game loads the Earth library with its packs (game.library_for).
  4. With --same-as (a folder or a paths.py name): the built game equals it file for file, engine_pin/PINNED*.txt aside.
     With --rarity engine and --same-as game_live the build gives back the live version (v22.1) exactly.

Then run the checks on <out>/chroma-game/prototype: the game's fast check through the release thread's runner,
    python3 -B /mnt/project-files/chroma-release/v22_checks.py --level fast --only @game --game <out>/chroma-game/prototype
and the browser drivers by serving <out>/web (README.md, "How to check it").
Replaces chroma-game/staging-final/final_pin.sh, chroma-hud/sync21.py and chroma-hud/pubmap.py run by hand.
"""
import argparse, filecmp, hashlib, json, os, pprint, re, shutil, subprocess, sys, time

SHARED = "/mnt/project-files"                                   # the shared folder: tools kept outside the repository
TREE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
ENV = next(d for d in (os.path.join(os.environ.get("CHROMA_ROOT") or TREE, "chroma-env"), os.path.join(SHARED, "chroma-env"))
           if os.path.isfile(os.path.join(d, "paths.py")))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(ENV))
sys.path.insert(0, ENV)
from paths import NAMES, P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = ["engine.py", "library.py", "combos.py", "batch.py", "earth_rules.py", "foresee.py", "explain.py", "life.py", "schwartz.py",
       "sphere_data.py"]   # the spheres' tables; world.py imports it only with sph_town on (Engine PR #52)
LIB = ["earth.py", "earth_perks_titles.py", "earth_voice.py", "dreams.py", "earth_story.py", "earth_play.py"]   # plus earth_<pack>.py per pack
PACK_FILES = ["catalogue.py", "roles.py", "helps.py"]                               # plus every core/*.py


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def stop(msg):
    sys.exit("STOP: " + msg)


def files(root):
    out = set()
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x != "__pycache__"]
        out |= {os.path.relpath(os.path.join(d, f), root) for f in fs}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--root", default=os.environ["CHROMA_ROOT"])
    ap.add_argument("--game", default="game_live")
    ap.add_argument("--engine", default="engine_live")
    ap.add_argument("--lib", default="library_live")
    ap.add_argument("--packs", default="packs_live")
    ap.add_argument("--same-as", default=None)
    ap.add_argument("--live-paths", default="-")
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--rarity", default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    where = lambda x: os.path.abspath(os.path.join(root, NAMES[x][0]) if x in NAMES else x)
    G0, EN, L, PK_DIR = where(a.game), where(a.engine), where(a.lib), where(a.packs)
    ART = where("art")
    OUT = os.path.abspath(a.out)
    if os.path.exists(OUT):
        stop(f"{OUT} exists; the build writes a new folder")
    for d in (G0, EN, L, PK_DIR, ART):
        if not os.path.isdir(d):
            stop(f"no folder {d}")
    t0 = time.time()
    log = []
    say = lambda s: (print(s), log.append(s))

    # what the engine asks for: its packs and its outer-world modules
    m = re.search(r"^PACKS = \[(.*)\]", open(os.path.join(EN, "batch.py")).read(), re.M)
    PK = re.findall(r'"(\w+)"', m.group(1)) if m else []
    if not PK:
        stop("the engine's batch.PACKS is empty")
    WLD = sorted(f for f in os.listdir(EN) if re.fullmatch(r"world(_\w+)?\.py", f) and not re.match(r"world_(stats|check|test)", f))
    pins = [(os.path.join(EN, f), f) for f in ENG + WLD]
    pins += [(os.path.join(L, f), f) for f in LIB + [f"earth_{p}.py" for p in PK]]
    pins += [(os.path.join(PK_DIR, "core", f), f"packs/core/{f}") for f in sorted(os.listdir(os.path.join(PK_DIR, "core"))) if f.endswith(".py")]
    pins += [(os.path.join(PK_DIR, p, f), f"packs/{p}/{f}") for p in PK for f in PACK_FILES]
    missing = [s for s, _ in pins if not os.path.isfile(s)]
    if missing:
        stop("missing owner files: " + ", ".join(missing))
    rj = os.path.join(EN, "rarity.json")
    if not os.path.isfile(rj):
        rj = os.path.join(root, NAMES["rarity_live"][0])
    pin = os.path.join(G0, "rarity.json")                                # the game's own pin, when the game has one
    if a.rarity and a.rarity != "engine":
        rj = os.path.abspath(a.rarity)
    elif a.rarity is None and os.path.isfile(pin):
        rj = pin
    if not os.path.isfile(rj):
        stop(f"no rarity table {rj}")

    # 1. the Library builds earth.py from its sources byte for byte
    lb = os.path.join(OUT, ".library-build")
    os.makedirs(lb)
    lbuild = os.path.join(L, "build.py")                  # the Library's compiler (in the shared folder when L has none)
    if not os.path.isfile(lbuild):
        lbuild = os.path.join(SHARED, NAMES["library_live"][0], "build.py")
    r = subprocess.run([sys.executable, "-B", lbuild, os.path.join(L, "earth.lib"), "--out", lb], capture_output=True, text=True)
    if r.returncode or not os.path.isfile(os.path.join(lb, "earth.py")):
        stop("the Library's build.py failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    if not filecmp.cmp(os.path.join(lb, "earth.py"), os.path.join(L, "earth.py"), shallow=False):
        stop(f"{L}/earth.py is not what its .lib sources build ({md5(os.path.join(lb, 'earth.py'))[:12]}); the Library rebuilds it first")
    say(f"1. Library: earth.py rebuilds from its .lib sources byte for byte ({md5(os.path.join(L, 'earth.py'))[:12]}; "
        + [x for x in r.stdout.splitlines() if x.startswith("earth.py:")][0][len("earth.py: "):] + ")")
    shutil.rmtree(lb)

    # 2. the game, pinned fresh
    G = os.path.join(OUT, "chroma-game", "prototype")
    shutil.copytree(G0, G, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
    os.symlink(ART, os.path.join(OUT, "chroma-art"))
    D = os.path.join(G, "engine_pin")
    for f in files(D):                                   # old pinned code goes; the PINNED*.txt history stays
        if f.endswith(".py"):
            os.remove(os.path.join(D, f))
    if os.path.isdir(os.path.join(D, "packs")):
        shutil.rmtree(os.path.join(D, "packs"))
    for s, d in pins:
        os.makedirs(os.path.dirname(os.path.join(D, d)), exist_ok=True)
        shutil.copyfile(s, os.path.join(D, d))
    R = json.load(open(rj, encoding="utf-8"))
    for k in ("lives", "sit", "read", "mark", "role"):
        if k not in R:
            stop(f"{rj} has no {k}")
    src = ("the engine\'s calib_v8/rarity.json, copied\nat the final re-pin" if rj != pin else
           "the game\'s rarity.json (Release\'s rebuild of\n2026-10-08 on v22.1), copied at the build")
    head = ('"""How rare each moment is in modern Earth lives (the Book of Moments): ' + src + ' (share of simulated lives, birth to 80, that meet each at least once; packs ' + ", ".join(R.get("packs", [])) + ')."""\n')
    open(os.path.join(G, "rarity.py"), "w", encoding="utf-8").write(head + "RARITY = " + pprint.pformat(R, width=118, sort_dicts=True) + "\n")
    wp = os.path.join(G, "web", "worker.js")
    s = open(wp).read()
    m = re.search(r"const SOURCES = (\[[^\]]*\]);", s)
    src = json.loads(m.group(1))
    want = [f"engine_pin/{f}" for f in WLD + ["sphere_data.py"]] + [f"engine_pin/packs/{p}/{f}" for p in PK for f in PACK_FILES] + [f"engine_pin/earth_{p}.py" for p in PK]
    add = [f for f in want if f not in src]
    if add:
        i = src.index("engine_pin/foresee.py")
        src[i:i] = add
        open(wp, "w").write(s.replace(m.group(0), "const SOURCES = " + json.dumps(src) + ";"))
    bad = [d for s_, d in pins if not filecmp.cmp(s_, os.path.join(D, d), shallow=False)]
    gone = [f for f in src if not os.path.isfile(os.path.join(G, f))]
    if bad or gone:
        stop(f"pinned files differ from their owners' copies: {bad}; worker sources missing: {gone}")
    open(os.path.join(D, "PINNED.txt"), "w").write(
        f"Pinned by chroma-game/tools/build.py, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC: the engine ({EN}), the Library ({L}), "
        f"the packs {', '.join(PK)} ({PK_DIR}) and the outer world ({' '.join(WLD)}). Every file and its md5: ../../../BUILD.md.\n")
    say(f"2. Pin (C-X1): {len(pins)} files pinned, each equal to its owner's copy; rarity.py from {os.path.relpath(rj, root)} "
        f"({R['lives']} lives, {len(R['sit'])} moments); worker SOURCES {len(src)} files, {'added ' + ', '.join(add) if add else 'none added'}")

    # 3. the page and the load test
    r = subprocess.run([sys.executable, "-B", os.path.join(G, "web", "src", "build.py")], capture_output=True, text=True)
    if r.returncode:
        stop("the page build failed:\n" + r.stdout + r.stderr)
    r = subprocess.run([sys.executable, "-B", "-c", "import game; L, W = game.library_for('earth'); G = L['ROLES'];"
                        "print('packs', L['PACKS'], 'situations', L['S'], 'titles and perks', G['NI'], 'dreams', len(L.get('DREAMS', [])))"],
                       cwd=G, capture_output=True, text=True)
    if r.returncode:
        stop("the game does not load:\n" + r.stderr[-3000:])
    say("3. Load: " + r.stdout.strip().splitlines()[-1])
    for d, _, _ in os.walk(G):                            # the load test leaves caches
        if os.path.basename(d) == "__pycache__":
            shutil.rmtree(d, ignore_errors=True)

    # 4. the same as a reference game, file for file
    if a.same_as:
        ref = where(a.same_as)
        A, B = files(ref), files(G)
        pinned_txt = lambda f: re.fullmatch(r"engine_pin/PINNED.*\.txt", f)
        diff = sorted(f for f in A & B if not pinned_txt(f) and not filecmp.cmp(os.path.join(ref, f), os.path.join(G, f), shallow=False))
        only = sorted(f for f in (A ^ B) if not pinned_txt(f))
        say(f"4. Same as {os.path.relpath(ref, root) if ref.startswith(root) else ref}: {len(B)} files, {len(diff)} differ, "
            f"{len(only)} only on one side" + (": " + ", ".join((diff + only)[:12]) if diff or only else ""))
        if diff or only:
            stop("the build differs from " + ref)

    # the web folder and the publish map
    W = os.path.join(OUT, "web")
    env = {**os.environ, "CHROMA_ART_GAME": where("art_game")}
    r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "webdir.py"), G, W], capture_output=True, text=True, env=env)
    if r.returncode:
        stop("webdir.py failed:\n" + r.stdout + r.stderr)
    for d, _, _ in os.walk(G):
        if os.path.basename(d) == "__pycache__":
            shutil.rmtree(d, ignore_errors=True)
    r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "pubmap.py"), W, a.live_paths], capture_output=True, text=True)
    if r.returncode:
        stop("pubmap.py failed:\n" + r.stdout + r.stderr)
    fmap = json.loads(r.stdout.splitlines()[0])
    json.dump({"file_path": os.path.join(W, "index.html"), "files": fmap}, open(os.path.join(OUT, "publish.json"), "w"), indent=1)
    if a.serve:
        py = os.path.join(root, NAMES["release"][0], "tools", "pyodide")
        if not os.path.isdir(py):
            py = os.path.join(SHARED, NAMES["release"][0], "tools", "pyodide")
        os.symlink(py, os.path.join(W, "pyodide"))
    pics = sum(1 for k in fmap if k.startswith("pics/"))
    say(f"Web folder: index.html {md5(os.path.join(W, 'index.html'))[:12]}, page.html {md5(os.path.join(W, 'page.html'))[:12]}; "
        f"publish map {len(fmap)} files ({len(fmap) - pics} code, {pics} pictures)" + ("; served with Pyodide" if a.serve else ""))

    rows = "\n".join(f"| engine_pin/{d} | {os.path.relpath(s_, root) if s_.startswith(root) else s_} | {md5(s_)[:12]} |" for s_, d in pins)
    key = ["game.py", "console.py", "link.py", "story.py", "worldview.py", "routine.py", "rarity.py", "web/worker.js",
           "web/src/app.js", "web/src/head.html", "web/src/body.html", "web/index.html"]
    rows2 = "\n".join(f"| {f} | {md5(os.path.join(G, f))[:12]} |" for f in key if os.path.isfile(os.path.join(G, f)))
    open(os.path.join(OUT, "BUILD.md"), "w").write(
        f"# Game build, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC\n\n"
        f"`python3 -B chroma-game/tools/build.py {' '.join(sys.argv[1:])}` ({time.time() - t0:.0f} s)\n\n"
        f"Root {root}. Game from {G0}; engine {EN}; Library {L}; packs {PK_DIR} ({', '.join(PK)}); pictures {ART}.\n\n"
        "## Checks\n\n" + "\n".join("- " + x for x in log) + "\n\n"
        "## Pinned files\n\n| In the game | From | md5 |\n|---|---|---|\n" + rows + "\n\n"
        "## The game's own files\n\n| File | md5 |\n|---|---|\n" + rows2 + "\n")
    print(f"built {OUT} in {time.time() - t0:.0f} s; record in BUILD.md")


if __name__ == "__main__":
    main()
