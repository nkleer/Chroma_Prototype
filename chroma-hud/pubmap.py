"""The files map for publishing the final version from a web dir (default web21): the page index.html goes as file_path;
worker.js, every file in worker.js SOURCES (as py/<file>, text/plain) and the pictures the page names go as files.
A publish keeps files it leaves out, so pictures already live can be skipped: pass a text file listing the live
artifact's published paths (one per line) as the second argument. A publish carries at most 255 files: with "pics"
as the third argument only pictures are listed, with "code" only worker.js and the sources.
   python3 pubmap.py [web dir] [live paths file or -] [all|pics|code]"""
import os, sys, json, re
here = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1] if len(sys.argv) > 1 else "web21"; W = (W if os.path.isabs(W) else os.path.join(here, W)).rstrip("/") + "/"
have = set()
if len(sys.argv) > 2 and sys.argv[2] != "-":
    have = {l.strip() for l in open(sys.argv[2]) if l.strip()}
part = sys.argv[3] if len(sys.argv) > 3 else "all"
src = json.loads(re.search(r"const SOURCES = (\[[^\]]*\])", open(W + "worker.js").read()).group(1))
m = {}
if part in ("all", "code"):
    m["worker.js"] = W + "worker.js"
    for f in src:
        assert os.path.exists(W + "py/" + f), f
        m["py/" + f] = {"from": W + "py/" + f, "contentType": "text/plain"}
if part in ("all", "pics"):
    page = open(W + "index.html", encoding="utf-8").read()
    for u in sorted(set(re.findall(r'pics/[A-Za-z0-9_.-]+\.webp', page))) + [f"pics/tarot-{i}.webp" for i in range(1, 8)]:
        if u not in have and u not in m and os.path.exists(W + u):
            m[u] = W + u
print(json.dumps(m)); print(len(m), "files", file=sys.stderr)
