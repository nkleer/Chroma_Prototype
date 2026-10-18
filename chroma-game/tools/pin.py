"""The game's engine_pin/, made from the owners' folders (plan by function, step 2: no committed pin).

    python3 -B chroma-game/tools/pin.py [--game DIR] [--root DIR] [--check]

engine_pin/ is not in git. The game loads the engine, the Library and the packs from it (link.py, game_base.py,
web/worker.js), so a checkout fills it from the owners' folders that chroma-env/paths.py names (engine_live,
library_live, packs_live, under --root, default the tree this script sits in): the files the engine asks for, the same
list build.py bundles into the page. Each file is copied when it is missing or differs, and a .py file the list no
longer names is removed. --check changes nothing: it lists what differs and exits 1 when anything does.

The game's tests run it first (ensure()), so they always play the owners' current files. A game folder whose
engine_pin/ holds a PINNED.txt is a committed pin (a release branch, or main before step 2): it is left as it is.
"""
import argparse, filecmp, os, re, shutil, sys

TREE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
ENG = ["engine.py", "library.py", "combos.py", "batch.py", "earth_rules.py", "foresee.py", "explain.py", "life.py", "schwartz.py"]
LIB = ["earth.py", "earth_perks_titles.py", "earth_voice.py", "dreams.py", "earth_story.py", "earth_play.py", "earth_spheres.py",
       "worlds.py", "earth_age_fit.py"]   # plus earth_<pack>.py per pack
PACK_FILES = ["catalogue.py", "roles.py", "helps.py"]                               # plus every core/*.py
DIRS = {"engine": "chroma-engine/v22-speedpass", "lib": "chroma-library", "packs": "chroma-packs"}   # paths.py's *_live


def owners(root=None):
    """The engine, Library and packs folders under root (paths.py's engine_live, library_live, packs_live)."""
    root = os.path.abspath(root or TREE)
    sys.path.insert(0, os.path.join(root, "chroma-env"))
    try:
        from paths import NAMES
        names = {k: NAMES[n][0] for k, n in (("engine", "engine_live"), ("lib", "library_live"), ("packs", "packs_live"))}
    except (ImportError, KeyError):
        names = DIRS
    finally:
        sys.path.pop(0)
    return {k: os.path.join(root, v) for k, v in names.items()}


def plan(EN, L, PK_DIR, ls=os.listdir, read=None, isfile=os.path.isfile):
    """[(source, path in engine_pin)], the packs and the outer-world files: what the engine asks for. ls, read and isfile
    read a folder, a file's text and a file's presence (the file system, or a git commit for prove.py)."""
    read = read or (lambda p: open(p, encoding="utf-8").read())
    m = re.search(r"^PACKS = \[(.*)\]", read(os.path.join(EN, "batch.py")), re.M)
    PK = re.findall(r'"(\w+)"', m.group(1)) if m else []
    if not PK:
        raise SystemExit("STOP: the engine's batch.PACKS is empty")
    names = ls(EN)
    WLD = sorted(f for f in names if re.fullmatch(r"world(_\w+)?\.py", f) and not re.match(r"world_(stats|check|test)", f))
    WLD += sorted(f for f in names if re.fullmatch(r"sphere_\w+\.py", f))   # the spheres' tables and fitted event bases
    pins = [(os.path.join(EN, f), f) for f in ENG + WLD]
    pins += [(os.path.join(L, f), f) for f in LIB + [f"earth_{p}.py" for p in PK]]
    pins += [(os.path.join(PK_DIR, "core", f), f"packs/core/{f}") for f in sorted(ls(os.path.join(PK_DIR, "core"))) if f.endswith(".py")]
    pins += [(os.path.join(PK_DIR, p, f), f"packs/{p}/{f}") for p in PK for f in PACK_FILES]
    missing = [s for s, _ in pins if not isfile(s)]
    if missing:
        raise SystemExit("STOP: missing owner files: " + ", ".join(missing))
    return pins, PK, WLD


def committed(game):
    return os.path.isfile(os.path.join(game, "engine_pin", "PINNED.txt"))


def ensure(game=None, root=None, check=False, say=None):
    """Bring game/engine_pin/ in line with the owners' folders; returns the paths changed (or that differ, with check)."""
    game = os.path.abspath(game or os.path.join(TREE, "chroma-game", "prototype"))
    root = os.path.abspath(root or os.path.dirname(os.path.dirname(game)))
    if committed(game):
        return []
    o = owners(root)
    pins, _, _ = plan(o["engine"], o["lib"], o["packs"])
    D = os.path.join(game, "engine_pin")
    want = {d for _, d in pins}
    out = []
    for s, d in pins:
        t = os.path.join(D, d)
        if os.path.isfile(t) and filecmp.cmp(s, t, shallow=False):
            continue
        out.append(d)
        if not check:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            shutil.copyfile(s, t)
    for dd, ds, fs in os.walk(D, topdown=False):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            rel = os.path.relpath(os.path.join(dd, f), D).replace(os.sep, "/")
            if f.endswith(".py") and rel not in want:
                out.append(rel)
                if not check:
                    os.remove(os.path.join(dd, f))
        if not check and dd != D and not os.listdir(dd):
            os.rmdir(dd)
    if say and out:
        say(f"engine_pin: {len(out)} {'differ' if check else 'updated'} from the owners' folders ({', '.join(sorted(out)[:6])}"
            + (", ..." if len(out) > 6 else "") + ")")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default=None)
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    game = os.path.abspath(a.game or os.path.join(TREE, "chroma-game", "prototype"))
    if committed(game):
        print(f"{game}/engine_pin holds a committed pin (PINNED.txt): left as it is")
        return 0
    out = ensure(game, a.root, a.check, print)
    if not out:
        print("engine_pin: the same as the owners' folders")
    return 1 if a.check and out else 0


if __name__ == "__main__":
    sys.exit(main())
