"""Where the Engine's tools find what they check (backend plan items 6 and 7, 2026-10-08).

Every tool in chroma-engine/tools/ starts with `import _engine`:
  CHROMA_ENGINE=<folder>   the engine to check (a candidate); default the engine of the tree this file sits in
                           (chroma-env/paths.py "engine_live", under CHROMA_ROOT, which defaults to this tree)
  OUT_DIR=<folder>         where a tool writes a file it is not given a path for; default the current folder
The Library and packs come from the tree's "library_live" and "packs_live" (for an engine inside the tree, the ones
beside it, as batch.py always read them) unless a tool's own arguments or variables (LIB, PACKS, PACK_DIR, FINAL_LIB)
say otherwise. The engine folder goes first on sys.path, so `import engine` finds it.
"""
import os
import sys

TREE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this file sits in
os.environ.setdefault("CHROMA_ROOT", TREE)
for _p in (os.path.join(TREE, "chroma-env"), "/mnt/project-files/chroma-env"):
    if os.path.exists(os.path.join(_p, "paths.py")):
        sys.path.insert(0, _p)
        break
from paths import P as PATHS   # noqa: E402

ENGINE = os.path.abspath(os.environ.get("CHROMA_ENGINE") or PATHS["engine_live"])
LIBRARY = PATHS["library_live"]
PACKS = PATHS["packs_live"]
GAME = PATHS["game_live"]
OUT = os.path.abspath(os.environ.get("OUT_DIR") or os.getcwd())
HERE = os.path.dirname(os.path.abspath(__file__))   # the tools folder (engine_v9_golive.py, the frozen v9 engine, is here)
sys.path.insert(0, ENGINE)
sys.dont_write_bytecode = True
# An engine outside a tree (a scratch candidate) has no chroma-library or chroma-packs two folders up, where batch.py
# looks: it gets the tree's. An engine inside a tree reads its own tree's, as before.
_UP = os.path.join(ENGINE, "..", "..")
if not os.path.isdir(os.path.join(_UP, "chroma-packs")):
    os.environ.setdefault("PACK_DIR", PACKS)
if not os.path.isdir(os.path.join(_UP, "chroma-library")):
    import batch as _batch
    _batch.LIB_DIR = LIBRARY


def with_steps():
    """The engine module with run_steps() (the game's pause points). An engine from before backend item 2 has none;
    then the game's link.py of the tree adds it as it always did."""
    if "\ndef run_steps(" in open(os.path.join(ENGINE, "engine.py"), encoding="utf-8").read():
        import engine as E
        return E
    src = open(os.path.join(GAME, "link.py")).read(); src = src[:src.rindex("E = load_engine()")]
    import types
    link = types.ModuleType("link"); link.__file__ = os.path.join(GAME, "link.py")
    exec(compile(src, link.__file__, "exec"), link.__dict__)
    return link.load_engine(ENGINE)
