"""A game folder's engine_pin/ for Release's checks, filled the way the game fills it (chroma-game/tools/pin.py; step 2 of
chroma-env/plan-by-function-2026-10-18.md: no committed pin, main 13ef583).

    import gamepin
    gamepin.fill(game, root=None, say=None, also=(), engine=None, lib=None, packs=None)
    gamepin.copy(src, dst, root=None, say=None, also=(), engine=None, lib=None, packs=None)
    gamepin.archive(repo, sha, tree, game="chroma-game/prototype")
    gamepin.where(game)

A checkout's chroma-game/prototype has no engine_pin/ in git; fill() fills it from the owners' folders: the ones given,
else those chroma-env/paths.py names under root (default the game folder's own tree). CHROMA_ENGINE_DIR and the like,
which pin.py honours, never steer it: a check names the folders it plays. A committed pin (engine_pin/PINNED.txt: a
release branch, the shared folder's live game, a commit from before step 2) is left as it is, and so is a filled pin
whose owners' folders are not there (a game folder outside any tree); an empty one stops the check. copy() makes a
scratch copy (web/ and test/ left out) and fills it: from the folders given, in place of whatever pin src holds (so
check_speedpass can play one engine in another game's copy), else from src's own tree. archive() takes a commit's game
by git archive and fills it from that commit's owners' folders. where() says which pin a report should name. pin.py is taken from root's tree, then from the trees in also, then from the tree this script sits in."""
import importlib.util, os, shlex, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = ("__pycache__", "*.pyc", "web", "test")


def tool(*roots):
    """chroma-game/tools/pin.py as a module, from the first of roots (then this script's tree) that holds it."""
    for r in [x for x in roots if x] + [os.path.dirname(HERE)]:
        p = os.path.join(os.path.abspath(r), "chroma-game", "tools", "pin.py")
        if os.path.isfile(p):
            spec = importlib.util.spec_from_file_location("chroma_game_pin", p)
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            return m
    raise SystemExit(f"STOP: no chroma-game/tools/pin.py under {', '.join(x for x in roots if x)} or {os.path.dirname(HERE)}")


def committed(game):
    return os.path.isfile(os.path.join(game, "engine_pin", "PINNED.txt"))


def owners(m, root, **given):
    """The engine, Library and packs folders: given, else paths.py's live names under root (pin.py m's owners(), with
    its environment variables set aside)."""
    saved = {v: os.environ.pop(v) for v in m.ENV.values() if v in os.environ}
    try:
        return m.owners(root, **{k: v for k, v in given.items() if v})
    finally:
        os.environ.update(saved)


def fill(game, root=None, say=None, also=(), **given):
    """Bring game/engine_pin/ in line with the owners' folders (given: engine=, lib=, packs=); returns what changed."""
    game = os.path.abspath(game)
    root = os.path.abspath(root or os.path.dirname(os.path.dirname(game)))
    if committed(game):
        return []
    m = tool(root, *also)
    o = owners(m, root, **given)
    gone = [d for d in o.values() if not os.path.isdir(d)]
    if gone:
        if os.path.isfile(os.path.join(game, "engine_pin", "engine.py")):
            if say:
                say(f"engine_pin of {game}: left as it is (no owners' folders at {', '.join(gone)})")
            return []
        raise SystemExit(f"STOP: {game} has no engine_pin/ and no owners' folders to fill it from ({', '.join(gone)})")
    return m.ensure(game, root, say=say, **o)


def copy(src, dst, root=None, say=None, also=(), **given):
    """A scratch copy of the game folder src at dst, its engine_pin filled by fill(); returns dst."""
    src, dst = os.path.abspath(src), os.path.abspath(dst)
    shutil.rmtree(dst, ignore_errors=True)
    fresh = any(given.values())
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP, *(("engine_pin",) if fresh else ())))
    fill(dst, root=root or os.path.dirname(os.path.dirname(src)), say=say, also=also, **given)
    return dst


def archive(repo, sha, tree, game="chroma-game/prototype"):
    """Commit sha's game folder, by git archive into tree; unless it holds a committed pin, the same commit's owners'
    folders (with chroma-env and chroma-game/tools) go next to it and fill its engine_pin. Returns the game folder."""
    def put(*rel):
        subprocess.run(f"git -C {shlex.quote(repo)} archive {sha} {' '.join(map(shlex.quote, rel))} | tar -x -C {shlex.quote(tree)}",
                       shell=True, check=True)
    put(game)
    g = os.path.join(tree, game)
    if committed(g):
        return g
    put("chroma-env", "chroma-game/tools")
    put(*(os.path.relpath(d, tree) for d in owners(tool(tree), tree).values()))
    fill(g, root=tree)
    return g


def where(game):
    """Which pin plays in game: 'a committed pin', or the folders engine_pin/FROM.txt says filled it."""
    pin = os.path.join(game, "engine_pin")
    if committed(game):
        return "a committed pin"
    try:
        rows = [r.split("\t") for r in open(os.path.join(pin, "FROM.txt"), encoding="utf-8").read().splitlines()[1:4]]
    except OSError:
        return "a pin with no FROM.txt"
    return "a pin filled from " + ", ".join(f"{r[0]} {r[1]}" for r in rows if len(r) == 2)
