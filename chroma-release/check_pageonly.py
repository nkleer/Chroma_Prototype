"""v22.2.1 row V1 (records/v22.2.1/scope.md): a page-only update leaves lives as they were.

Against a base commit (release/v22.2), the candidate commit changes no file outside the page, the art and the look tools,
and its build's worker.js and every py/ file equal the base build's byte for byte (the game runs those in the page's
Python, so the same files play the same lives). Builds both with the one build command (v22_checks.py --only build).

    python3 -B chroma-release/check_pageonly.py --repo DIR --base SHA --commit SHA --work DIR

Exit code 0 when both hold. Writes chroma-release/out/pageonly_<UTC>.txt and its result line (id pageonly)."""
import argparse, os, subprocess, sys, time, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chroma-env"))
from paths import path   # noqa: E402

ALLOWED = ("chroma-game/prototype/web/src/", "chroma-game/tools/webdir.py", "chroma-art/game/", "chroma-art/kit/",
           "chroma-look/")
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--base", required=True); ap.add_argument("--commit", required=True)
ap.add_argument("--work", required=True)
a = ap.parse_args()
REPORT = path("release_out", f"pageonly_{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}.txt")
lines, ok = [], True
git = lambda *x: subprocess.run(["git", "-C", a.repo] + list(x), check=True, capture_output=True, text=True).stdout
base, cand = git("rev-parse", a.base).strip(), git("rev-parse", a.commit).strip()
lines.append(f"v22.2.1 V1 page only, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC: candidate {cand[:12]} against base {base[:12]}")
changed = [f for f in git("diff", "--name-only", base, cand).split("\n") if f]
outside = [f for f in changed if not f.startswith(ALLOWED)]
lines.append(f"{'ok  ' if not outside else 'MISS'} {len(changed)} files changed, {len(outside)} outside the page, the art and the look tools"
             + (": " + ", ".join(outside[:20]) if outside else ""))
ok &= not outside
builds = {}
for tag, sha in (("base", base), ("candidate", cand)):
    w = os.path.join(a.work, tag)
    r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "v22_checks.py"), "--repo", a.repo, "--commit", sha, "--only", "build",
                        "--no-reuse", "--keep", "--work", w], capture_output=True, text=True)
    web = os.path.join(w, "w", "build", "web")
    if r.returncode or not os.path.exists(os.path.join(web, "worker.js")):
        lines.append(f"MISS the {tag} build failed (exit {r.returncode}): {r.stdout.strip().splitlines()[-1:] }"); ok = False
    builds[tag] = web
if ok:
    files = ["worker.js"] + sorted(os.path.relpath(os.path.join(d, f), builds["base"]) for d, _, fs in os.walk(os.path.join(builds["base"], "py")) for f in fs)
    extra = sorted(os.path.relpath(os.path.join(d, f), builds["candidate"]) for d, _, fs in os.walk(os.path.join(builds["candidate"], "py")) for f in fs)
    extra = [f for f in extra if f not in files]
    diff = [f for f in files if not os.path.exists(os.path.join(builds["candidate"], f))
            or not filecmp.cmp(os.path.join(builds["base"], f), os.path.join(builds["candidate"], f), shallow=False)]
    lines.append(f"{'ok  ' if not diff and not extra else 'MISS'} worker.js and {len(files) - 1} py/ files: {len(diff)} differ or are missing, "
                 f"{len(extra)} new" + (": " + ", ".join(diff + extra) if diff or extra else " (the same lives)"))
    ok &= not diff and not extra
lines.append(f"pageonly: {'PASS' if ok else 'FAIL'}")
open(REPORT, "w").write("\n".join(lines) + "\n"); print("\n".join(lines)); print("report:", REPORT)
import results; results.done("pageonly", 0 if ok else 1, REPORT)
sys.exit(0 if ok else 1)
