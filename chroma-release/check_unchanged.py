"""Release check C-X2 (chroma-release/checklist.md, section 9): the final check's runs still describe the files that ship.

Every C-E, C-L, C-P and C-X run in section 9 ran on the final files. This lists every file those runs read that changed
after the last final file landed (world_link.py, 10-07 08:13 UTC), so a late edit cannot slip in behind a passed row:
the engine and world modules and rarity.json in chroma-engine/prototype, the Library's top-level modules, the staged
next3 batch and catalogue, and the packs' modules and .lib sources. foresee.py (09:44 UTC, bff61663a683) is allowed: only the game and
explain read it, it changes no life, and C-X1 compares the game's copy. Read only.

    python3 -B chroma-release/check_unchanged.py [--since "2026-10-07 08:13"] [--allow PATH=MD5 ...]

--allow names a file that changed after --since on purpose, with the md5 (first 12) the rows that reran on it used; it
also replaces that file's expected md5 below. For Emren's parliament and minister change (N8, 10-07 13:55 UTC) the
politics pack, earth_rules.py and any other file it touches go here once the rows that read them have rerun (the
checklist's rerun list under C-X2).
Exit code 0 when nothing else changed after --since (UTC).

Re-pointed 2026-10-08 after the folder cleanup (chroma-env/MAP.md): the engine files are read from the frozen live
copy chroma-engine/archive/live-v22 (chroma-engine/prototype carries paused v23 edits), and the next3 batch and
catalogue from the top of chroma-library (staging/next3 was removed as an identical duplicate). This check goes by file
times, so it only served the v22 round: the go-live copies (10-07 20:48-20:50 UTC) all read as changed after it while
their md5s are the ones the runs used. For the live v22 files use chroma-env/check_live.py with
chroma-env/live-v22-manifest.txt (md5s, read only); v23's C-X2 needs an md5 list of the files its runs read."""
import sys, os, argparse, hashlib, time, calendar

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--since", default="2026-10-07 08:13", help="UTC; the last final file's time")
ap.add_argument("--allow", action="append", default=[], help="PATH=MD5 (path from /mnt/project-files, md5 first 12)")
a = ap.parse_args()
cut = calendar.timegm(time.strptime(a.since, "%Y-%m-%d %H:%M")) + 59
EN = "chroma-engine/archive/live-v22"
ALLOW = {f"{EN}/foresee.py": "bff61663a683"}
KEY = {f"{EN}/engine.py": "5fb02ecd3ab8", f"{EN}/world_link.py": "4e8d7d0cc433",
       f"{EN}/earth_rules.py": "e01a8239afb3", f"{EN}/foresee.py": "bff61663a683",
       "chroma-library/earth.py": "59c9642e0a24",
       "chroma-library/earth_perks_titles.py": "610a1fe1f4b1"}
for x in a.allow:
    p_, h_ = x.split("=", 1); ALLOW[p_] = h_
    if p_ in KEY:
        KEY[p_] = h_
md5 = lambda p: hashlib.md5(open(os.path.join(ROOT, p), "rb").read()).hexdigest()[:12]


def files():
    for d, deep in ((EN, False), ("chroma-library", False), ("chroma-packs", True)):
        for r, ds, fs in os.walk(os.path.join(ROOT, d)):
            ds[:] = [x for x in ds if x not in ("__pycache__", "archive", "tools")] if deep else []
            for f in fs:
                if f.endswith(".py") or (deep and f.endswith(".lib")):   # the packs' .lib sources build the staged pack files
                    yield os.path.relpath(os.path.join(r, f), ROOT)
    yield "chroma-engine/prototype/calib_v8/rarity.json"


print(f"C-X2 files unchanged since {a.since} UTC, checked {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
ok = True; n = 0
for p in sorted(set(files())):
    n += 1
    mt = os.path.getmtime(os.path.join(ROOT, p))
    if mt > cut:
        h = md5(p)
        if ALLOW.get(p) == h:
            print(f"ok   {p} changed {time.strftime('%H:%M', time.gmtime(mt))} UTC, allowed ({h})")
        else:
            print(f"MISS {p} changed {time.strftime('%H:%M', time.gmtime(mt))} UTC ({h}) after the runs that passed on it"); ok = False
for p, h in KEY.items():
    got = md5(p); same = got == h
    print(("ok  " if same else "MISS") + f" {p} {got}" + ("" if same else f" (the runs used {h})")); ok &= same
print(f"{n} files looked at")
print("C-X2 files:", "PASS" if ok else "FAIL")
import results; results.done('unchanged', 0 if ok else 1, "")   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
