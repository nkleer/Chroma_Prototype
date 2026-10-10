"""The files map for publishing a web folder (made by webdir.py) as the live Artifact: the page index.html goes as
file_path; worker.js, every file in worker.js SOURCES (packed as py/code-<n>.json when webdir.py set CODE_PARTS, else
as py/<file>, text/plain) and the pictures the page names go as
files. A publish keeps files it leaves out, so pictures already live can be skipped: pass a text file listing the live
artifact's published paths (one per line) as the second argument. A publish carries at most 255 files: with "pics"
as the third argument only pictures are listed, with "code" only worker.js and the sources.
   python3 -B pubmap.py <web dir> [live paths file or -] [all|pics|code]
Was chroma-hud/pubmap.py (v21 to v22.1); tools/build.py runs it as the last step of the build."""
import json, os, re, sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
W = os.path.abspath(sys.argv[1]).rstrip("/") + "/"
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
    nparts = int(re.search(r"const CODE_PARTS = (\d+);", open(W + "worker.js").read()).group(1))
    if nparts:   # the sources packed by webdir.py: py/code-<n>.json instead of one file each
        for n in range(1, nparts + 1):
            m[f"py/code-{n}.json"] = {"from": W + f"py/code-{n}.json", "contentType": "application/json"}
    else:
        for f in src:
            m["py/" + f] = {"from": W + "py/" + f, "contentType": "text/plain"}
if part in ("all", "pics"):
    page = open(W + "index.html", encoding="utf-8").read()
    pp = re.search(r"const PIC_PACKS = (\{.*?\});", page)
    in_pack = json.loads(pp.group(1)) if pp else {}   # pictures that go in pics/pack-<n>.json (webdir.py), not as files
    for u in sorted(set(re.findall(r'pics/[A-Za-z0-9_.-]+\.webp', page))) + [f"pics/tarot-{i}.webp" for i in range(1, 8)]:
        if u not in have and u not in m and u not in in_pack and os.path.exists(W + u):
            m[u] = W + u
    for n in sorted(set(in_pack.values())):
        u = f"pics/pack-{n}.json"
        assert os.path.exists(W + u), u
        m[u] = {"from": W + u, "contentType": "application/json"}
print(json.dumps(m)); print(len(m), "files", file=sys.stderr)
