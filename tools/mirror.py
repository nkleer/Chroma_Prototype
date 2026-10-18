"""Copy merged files from this checkout to the same paths in the shared folder (CONTRIBUTING.md).

    python3 -B tools/mirror.py <path> [<path> ...]             from a clean checkout of main
    python3 -B tools/mirror.py --publish <path> [<path> ...]   from a clean checkout of a release/<version> branch

Copies every tracked file under the named paths to CHROMA_ROOT (default /mnt/project-files), prints each file's md5,
and deletes nothing. Without --publish it refuses files of the live version (chroma-env/live-<version>-manifest.txt,
the live_manifest entry of chroma-env/paths.py), because those change only at a publish.

The game's engine_pin/ is not in git (plan by function, step 2). When a named path covers it, chroma-game/tools/pin.py
first fills it in this checkout from the checkout's own engine, Library and packs, and its files are copied with the
tracked ones, so the shared folder's game plays what the checkout holds. A checkout with a committed pin (one from
before step 2) is copied as it is.
"""
import hashlib, os, shutil, subprocess, sys

ROOT = os.environ.get("CHROMA_ROOT", "/mnt/project-files")


def git(*a):
    return subprocess.run(["git", *a], check=True, capture_output=True, text=True).stdout


def live_files():
    sys.path.insert(0, os.path.join(ROOT, "chroma-env"))
    from paths import P
    return {line.split(None, 2)[2].strip() for line in open(P["live_manifest"]) if line.strip()}


PIN = "chroma-game/prototype/engine_pin"


def pin_files(paths):
    """engine_pin/'s files under the named paths, filled first by chroma-game/tools/pin.py (none if no path covers it)."""
    names = [os.path.normpath(p) for p in paths]
    under = lambda f: any(n == "." or f == n or f.startswith(n + "/") for n in names)
    if not any(under(PIN) or n.startswith(PIN + "/") for n in names) or not os.path.isfile("chroma-game/tools/pin.py"):
        return []
    subprocess.run([sys.executable, "-B", "chroma-game/tools/pin.py"], check=True)
    out = []
    for dp, dn, fn in os.walk(PIN):
        dn[:] = sorted(d for d in dn if d != "__pycache__")
        out += [os.path.join(dp, f) for f in sorted(fn)]
    return [f for f in out if under(f)]


def main(argv):
    publish = "--publish" in argv
    paths = [a for a in argv if a != "--publish"]
    if not paths:
        sys.exit(__doc__)
    os.chdir(git("rev-parse", "--show-toplevel").strip())
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if git("status", "--porcelain", "--untracked-files=no").strip():
        sys.exit("STOP: the checkout has uncommitted changes")
    if publish != branch.startswith("release/") or (not publish and branch != "main"):
        sys.exit(f"STOP: on {branch}; plain mirroring runs on main, --publish on a release/<version> branch")
    files = [f for f in git("ls-files", "-z", "--", *paths).split("\0") if f]
    files = list(dict.fromkeys(files + pin_files(paths)))
    if not files:
        sys.exit("STOP: no tracked files under " + " ".join(paths))
    if not publish:
        held = sorted(set(files) & live_files())
        if held:
            sys.exit("STOP: live files change only at a publish:\n  " + "\n  ".join(held[:20]))
    head = git("rev-parse", "--short", "HEAD").strip()
    for f in files:
        dst = os.path.join(ROOT, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(f, dst)
        print(hashlib.md5(open(dst, "rb").read()).hexdigest()[:12], f)
    print(f"{len(files)} files copied from {branch} {head} to {ROOT}")


if __name__ == "__main__":
    main(sys.argv[1:])
