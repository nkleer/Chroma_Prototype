"""Manifest of the files a version of the game is built from, with an MD5 for each.

   python3 -B check_live.py write <out.txt> [--version v22.2]   record the manifest (default: the live version)
   python3 -B check_live.py check [<manifest>] [--version v22.2] compare the folder now against a recorded manifest
                                                                (default: the live version's manifest, paths.py live_manifest)
Exit code 0 when nothing recorded changed or went missing (new files are listed but do not fail the check).

Versions, with their folders named in paths.py:
   v22.2.1 live since 2026-10-10 14:03 UTC (release/v22.2.1): game_live (chroma-game/prototype), engine_live,
          game_tools (the build it was published with); live-v22.2.1-manifest.txt. A page and pictures update: the
          engine and the Library are v22.2's
   v22.2  the rollback, in the same folders: v22.2.1 changed six of its files (web/index.html, web/src/build.py and
          CHANGES.md, test/drive_v14.js, tools/webdir.py, pictures.json), so its check shows those six as changed;
          live-v22.2-manifest.txt
   v22.1  the older rollback: game_v22_1 (chroma-game/prototype-v22.1), engine_v22_1 (in _archive/2026-10-09/live-v22.1/);
          live-v22.1-manifest.txt, recorded while v22.1 was live, so its game and engine paths are read at those folders
   v22    the oldest rollback: game_v22 (chroma-game/prototype-v22), engine_v22; live-v22-manifest.txt, read the same way
The Library's compiled files, the packs and the pictures are shared; each version lists the ones it was built from.
So a rollback's check shows a shared file as changed once a later version changed it, or missing once it dropped it
(v22.1 and v22: three chroma-art/game ink files changed and ink-icons-handoff.md dropped since v22.2, and pictures.json
changed since v22.2.1); release/<version> holds that version's exact files.
A manifest is written from the shared folder only after its files match the release branch (CONTRIBUTING.md).

An .svg or .webp is recorded and compared without the C2PA stamp the shared folder adds to it. Every recorded file is
checked at the path it was recorded under; the folders paths.py names decide only which files are listed as new.
Read-only on the project folder: it only hashes files. Caches (__pycache__) are skipped.
"""
import hashlib, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, NAMES  # noqa: E402

LIB_PY = ["earth.py", "earth_perks_titles.py", "earth_voice.py", "earth_science.py", "earth_politics.py",
          "earth_stage.py", "dreams.py"]                         # plus every .lib at the top of library_live
OLD_HELPERS = ["build_helpers/sync21.py", "build_helpers/pubmap.py"]
LIVE = "v22.2.1"
# game, engine: the version's folders now; trees: folders listed whole; files: single files ("name" or "name/file");
# moved: recorded path prefix -> the paths.py name of the folder it is read from now
LIB_V22_2 = LIB_PY + ["earth_play.py", "earth_story.py"]
VERSIONS = {
    "v22.2.1": dict(game="game_live", engine="engine_live", manifest="live_manifest", trees=["game_tools"],
                    files=[], lib=LIB_V22_2),
    "v22.2": dict(game="game_live", engine="engine_live", manifest="live_manifest_v22_2", trees=["game_tools"],
                  files=[], lib=LIB_V22_2),
    "v22.1": dict(game="game_v22_1", engine="engine_v22_1", manifest="live_manifest_v22_1", trees=[],
                  files=["rarity_v22_1"] + OLD_HELPERS, lib=LIB_PY,
                  moved={"chroma-game/prototype": "game_v22_1", "chroma-engine/v22-speedpass": "engine_v22_1"}),
    "v22": dict(game="game_v22", engine="engine_v22", manifest="live_manifest_v22", trees=[],
                files=["rarity_v22_1"] + OLD_HELPERS, lib=LIB_PY, moved={"chroma-game/prototype": "game_v22"}),
}
SHARED_TREES = ["art_game"]                                      # pictures.json, pics/, ink icons
PACKS = ["core", "politics", "science", "stage"]                 # under packs_live


def rel(name, *parts):
    return os.path.join(NAMES[name][0], *parts)


def listing(version):
    v = VERSIONS[version]
    trees = ([rel(v["game"]), rel(v["engine"])] + [rel(t) for t in SHARED_TREES + v["trees"]]
             + [rel("packs_live", p) for p in PACKS])
    out = []
    for t in trees:
        for dp, dn, fn in os.walk(os.path.join(ROOT, t)):
            dn[:] = sorted(d for d in dn if d != "__pycache__")
            out += [os.path.join(dp, f) for f in sorted(fn)]
    d = os.path.join(ROOT, rel("library_live"))
    out += [os.path.join(d, f) for f in v["lib"]]
    out += sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".lib"))
    for f in v["files"]:
        name, _, rest = f.partition("/")
        out.append(os.path.join(ROOT, rel(name, rest) if rest else rel(name)))
    return list(dict.fromkeys(out))


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# The shared folder stamps a new .svg or .webp written to it with a C2PA provenance block (a new one each time, within
# seconds). In an .svg: an xmlns:c2pa attribute and a <metadata><c2pa:manifest>...</c2pa:manifest></metadata> block
# (Visuals found this on 10-09). In a .webp: a "C2PA" chunk after the picture, with the RIFF size grown to hold it (the
# v22.2.1 portraits, 10-10). It is not content, so these files are recorded and compared without it.
C2PA = re.compile(rb"<metadata><c2pa:manifest>.*?</c2pa:manifest></metadata>", re.S)
STAMPED = (".svg", ".webp")


def plain_webp(data):
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return data
    out, i = [], 12
    while i + 8 <= len(data):
        size = struct.unpack("<I", data[i + 4:i + 8])[0]
        end = i + 8 + size + (size & 1)                          # chunks are padded to an even length
        if data[i:i + 4] != b"C2PA":
            out.append(data[i:end])
        i = end
    body = b"WEBP" + b"".join(out)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def plain(p, data):
    if p.endswith(".webp"):
        return plain_webp(data)
    return C2PA.sub(b"", data, count=1).replace(b' xmlns:c2pa="http://c2pa.org/manifest"', b"", 1)


def hashes(p):
    """The md5s a recorded file may match: its bytes, and for an .svg or .webp also its bytes without the C2PA stamp."""
    h = md5(p)
    if not p.endswith(STAMPED):
        return {h}
    with open(p, "rb") as f:
        return {h, hashlib.md5(plain(p, f.read())).hexdigest()}


def record(p):
    """A row's md5 and size: of the file's bytes, and for an .svg or .webp of its bytes without the C2PA stamp."""
    if not p.endswith(STAMPED):
        return md5(p), os.path.getsize(p)
    with open(p, "rb") as f:
        data = plain(p, f.read())
    return hashlib.md5(data).hexdigest(), len(data)


def write(dst, version):
    rows = ["{}  {:>9}  {}".format(*record(p), os.path.relpath(p, ROOT)) for p in listing(version)]
    open(dst, "w").write("\n".join(rows) + "\n")
    print(version + ":", len(rows), "files,", round(sum(int(r.split()[1]) for r in rows) / 1e6, 1), "MB ->", dst)
    return 0


def check(src, version):
    v = VERSIONS[version]
    want = {}
    for line in open(src):
        h, s, p = line.split(None, 2)
        p = p.strip()
        for old, name in v.get("moved", {}).items():
            if p.startswith(old + "/"):
                p = rel(name) + p[len(old):]
                break
        want[p] = h
    # every recorded file is checked where it was recorded, even when paths.py's names no longer reach it (rarity_live
    # moved 10-08); the names only decide which files count as new
    have = [p for p in want if os.path.isfile(os.path.join(ROOT, p))]
    changed = [p for p in have if want[p] not in hashes(os.path.join(ROOT, p))]
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
        m = re.fullmatch(r"live-(v[0-9.]+)-manifest\.txt", os.path.basename(src or ""))
        ver = m.group(1) if m and m.group(1) in VERSIONS else LIVE   # a version's manifest names its version
    sys.exit(check(src or os.path.join(ROOT, rel(VERSIONS[ver]["manifest"])), ver))
