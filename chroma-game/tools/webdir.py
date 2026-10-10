"""Builds a web folder from a game folder: the page, the worker, the Python sources and the pictures the page names.

    python3 -B webdir.py <game dir> <web dir>

The game dir is a prototype folder (or a folder holding prototype/). The web dir gets index.html (the page as published,
the Artifact's file_path), page.html (the same page inside a document, for serving locally), worker.js, py/ (the game's
Python and engine_pin/) and pics/ (the pictures chroma-art/game/pictures.json names, copied when missing or changed).
Pictures come from the art folder that chroma-env/paths.py names art_game, in the tree this script sits in (CHROMA_ROOT
overrides it; CHROMA_ART_GAME names the folder outright, as build.py does).
Was chroma-hud/sync21.py (v21 to v22.1); tools/build.py runs it as one step of the build.
"""
import filecmp, glob, json, os, shutil, subprocess, sys

TREE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
ENV = next(d for d in (os.path.join(os.environ.get("CHROMA_ROOT") or TREE, "chroma-env"), "/mnt/project-files/chroma-env")
           if os.path.isfile(os.path.join(d, "paths.py")))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(ENV))
sys.path.insert(0, ENV)
from paths import P  # noqa: E402

if len(sys.argv) != 3:
    sys.exit(__doc__)
G = os.path.abspath(sys.argv[1]).rstrip("/") + "/"; G = G + "prototype/" if os.path.isdir(G + "prototype") else G
W = os.path.abspath(sys.argv[2]).rstrip("/") + "/"
ART = os.environ.get("CHROMA_ART_GAME", P["art_game"])
os.makedirs(W + "py/engine_pin", exist_ok=True)
subprocess.run([sys.executable, "-B", G + "web/src/build.py"], check=True)
s = open(G + "web/index.html", encoding="utf-8").read()
open(W + "index.html", "w", encoding="utf-8").write(s)
shutil.copy(G + "web/worker.js", W + "worker.js")
for f in ["link.py", "story.py", "worldview.py", "game.py", "console.py", "routine.py", "rarity.py"]:
    if os.path.exists(G + f): shutil.copy(G + f, W + "py/" + f)
for f in glob.glob(G + "engine_pin/**/*.py", recursive=True):   # engine_pin/*.py and engine_pin/packs/<pack>/*.py
    d = W + "py/engine_pin/" + os.path.relpath(f, G + "engine_pin")
    os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy(f, d)
head = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}</style></head><body>'
open(W + "page.html", "w", encoding="utf-8").write(head + s + "</body></html>")
# the pictures the page names (pictures.json: scenes, domains, tiers, tarot, the unwritten fabric, the portrait cards of the
# ink look), copied next to the page
def _urls(x):
    if isinstance(x, dict): return [u for v in x.values() for u in _urls(v)]
    if isinstance(x, list): return [u for v in x for u in _urls(v)]
    return [x] if isinstance(x, str) and x.endswith(".webp") else []
pj = json.load(open(os.path.join(ART, "pictures.json"), encoding="utf-8"))
got = 0
for u in sorted(set(_urls({k: pj.get(k) for k in ("situation", "domain", "tier", "tarot", "texture", "portrait")}))):
    src_, dst_ = os.path.join(ART, u), W + u
    if os.path.exists(src_) and not (os.path.exists(dst_) and filecmp.cmp(src_, dst_, shallow=False)):
        os.makedirs(os.path.dirname(dst_), exist_ok=True); shutil.copy(src_, dst_); got += 1
print("pictures copied:", got)
print("web folder", W)
