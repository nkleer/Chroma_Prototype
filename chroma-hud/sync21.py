import shutil, glob, os, subprocess, sys
# usage: python3 sync21.py [work dir] [web dir]. Both are taken relative to this script's folder unless absolute; the work
# dir is the one holding prototype/ (or the prototype folder itself). Defaults: w21 and web21 next to this script.
here = os.path.dirname(os.path.abspath(__file__))
def _dir(a): return (a if os.path.isabs(a) else os.path.join(here, a)).rstrip("/") + "/"
G = _dir(sys.argv[1] if len(sys.argv) > 1 else "w21"); G = G + "prototype/" if os.path.isdir(G + "prototype") else G
W = _dir(sys.argv[2] if len(sys.argv) > 2 else "web21")
os.makedirs(W + "py/engine_pin", exist_ok=True)
subprocess.run(["python3", G + "web/src/build.py"], check=True)
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
# the pictures the page names (chroma-art/game/pictures.json: scenes, domains, tiers, tarot, the unwritten fabric), copied
# next to the page when missing or changed
import json, filecmp
ART = os.path.join(here, "chroma-art", "game")
def _urls(x):
    if isinstance(x, dict): return [u for v in x.values() for u in _urls(v)]
    if isinstance(x, list): return [u for v in x for u in _urls(v)]
    return [x] if isinstance(x, str) and x.endswith(".webp") else []
pj = json.load(open(os.path.join(ART, "pictures.json"), encoding="utf-8"))
got = 0
for u in sorted(set(_urls({k: pj.get(k) for k in ("situation", "domain", "tier", "tarot", "texture")}))):
    src_, dst_ = os.path.join(ART, u), W + u
    if os.path.exists(src_) and not (os.path.exists(dst_) and filecmp.cmp(src_, dst_, shallow=False)):
        os.makedirs(os.path.dirname(dst_), exist_ok=True); shutil.copy(src_, dst_); got += 1
print("pictures copied:", got)
print("synced", W)
