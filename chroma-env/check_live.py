"""Manifest of the files a version of the game is built from, with an MD5 for each.

   python3 -B check_live.py write <out.txt> [--version v22]   record the manifest (default: the live version)
   python3 -B check_live.py check [<manifest>] [--version v22] compare the folder now against a recorded manifest
                                                                (default: the live version's manifest, paths.py live_manifest)
Exit code 0 when nothing recorded changed or went missing (new files are listed but do not fail the check).

Versions, with their folders named in paths.py:
   v22.1  live since 2026-10-08 13:10 UTC: game_live (chroma-game/prototype), engine_live; live-v22.1-manifest.txt
   v22    the rollback: game_v22 (chroma-game/prototype-v22), engine_v22; live-v22-manifest.txt, recorded while v22 sat in
          chroma-game/prototype, so its game paths are read as prototype-v22
The Library, packs, pictures, rarity table and build helpers are the same files in both.

Every recorded file is checked at the path it was recorded under; the folders paths.py names decide only which files
are listed as new. Read-only on the project folder: it only hashes files. Caches (__pycache__) are skipped.
"""
import hashlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, NAMES  # noqa: E402

LIVE = "v22.1"
VERSIONS = {
    "v22.1": dict(game="game_live", engine="engine_live", manifest="live_manifest"),
    "v22": dict(game="game_v22", engine="engine_v22", manifest="live_manifest_v22", old_game="chroma-game/prototype"),
}
SHARED_TREES = ["art_game"]                                      # pictures.json, pics/, ink icons
PACKS = ["core", "politics", "science", "stage"]                 # under packs_live
FILES = ["rarity_live", "build_helpers/sync21.py", "build_helpers/pubmap.py"]
LIB_PY = ["earth.py", "earth_perks_titles.py", "earth_voice.py", "earth_science.py", "earth_politics.py",
          "earth_stage.py", "dreams.py"]                         # plus every .lib at the top of library_live


def rel(name, *parts):
    return os.path.join(NAMES[name][0], *parts)


def listing(version):
    v = VERSIONS[version]
    trees = [rel(v["game"]), rel(v["engine"])] + [rel(t) for t in SHARED_TREES] + [rel("packs_live", p) for p in PACKS]
    out = []
    for t in trees:
        for dp, dn, fn in os.walk(os.path.join(ROOT, t)):
            dn[:] = sorted(d for d in dn if d != "__pycache__")
            out += [os.path.join(dp, f) for f in sorted(fn)]
    d = os.path.join(ROOT, rel("library_live"))
    out += [os.path.join(d, f) for f in LIB_PY]
    out += sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".lib"))
    for f in FILES:
        name, _, rest = f.partition("/")
        out.append(os.path.join(ROOT, rel(name, rest) if rest else rel(name)))
    return out


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write(dst, version):
    rows = [f"{md5(p)}  {os.path.getsize(p):>9}  {os.path.relpath(p, ROOT)}" for p in listing(version)]
    open(dst, "w").write("\n".join(rows) + "\n")
    print(version + ":", len(rows), "files,", round(sum(int(r.split()[1]) for r in rows) / 1e6, 1), "MB ->", dst)
    return 0


def check(src, version):
    v = VERSIONS[version]
    game = rel(v["game"])
    want = {}
    for line in open(src):
        h, s, p = line.split(None, 2)
        p = p.strip()
        if v.get("old_game") and p.startswith(v["old_game"] + "/"):
            p = game + p[len(v["old_game"]):]
        want[p] = h
    # every recorded file is checked where it was recorded, even when paths.py's names no longer reach it (rarity_live
    # moved 10-08); the names only decide which files count as new
    have = [p for p in want if os.path.isfile(os.path.join(ROOT, p))]
    changed = [p for p in have if md5(os.path.join(ROOT, p)) != want[p]]
    missing = [p for p in want if p not in have]
    now = dict.fromkeys(os.path.relpath(p, ROOT) for p in listing(version))
    added = [p for p in now if p not in want]
    for tag, l in (("CHANGED", changed), ("MISSING", missing), ("NEW", added)):
        for p in l:
            print(tag, p)
    print(f"{version}: {len(want)} files recorded: {len(changed)} changed, {len(missing)} missing, {len(added)} new")
    return 0 if not (changed or missing) else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    ver = None
    if "--version" in args:
        i = args.index("--version"); ver = args[i + 1]; del args[i:i + 2]
    if args[0] == "write":
        sys.exit(write(args[1], ver or LIVE))
    src = args[1] if len(args) > 1 else None
    if ver is None:
        ver = "v22" if src and os.path.basename(src) == "live-v22-manifest.txt" else LIVE
    sys.exit(check(src or os.path.join(ROOT, rel(VERSIONS[ver]["manifest"])), ver))
