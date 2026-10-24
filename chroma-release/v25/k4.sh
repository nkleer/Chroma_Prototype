#!/bin/bash
# v25 K4 "Off is v23.2" (records/v25/checks.md): chroma-release/same-lives.sh part 1 to 4 with every v24 and v25 switch
# off, run from a repository checkout alone (no shared folder needed; Emren's PC), as v24's out/v24/k4/k4.sh did it from
# the shared folder. The only changes: paths come from this checkout, the engine's V25_OFF joins UPD_OFF and V24_OFF, the
# work folder is $TMPDIR and the report goes to $OUT (default chroma-release/out/v25/k4/). What follows is v24's text.
# v24 K4: chroma-release/same-lives.sh part 1 to 4 with every v24 switch off, the
# candidate's engine, Library and packs against release/v23.2's (the live game, Version 35), byte for byte. One part a
# machine of 4 cores (about 50 minutes; about 25 once the base side is kept). Both sides from git trees. The new side:
# every DEFAULT key the candidate moved from v23.2 set to its UPD_OFF value (PNEW, read from the two engines) with the
# engine's V24_OFF laid over it (the Engine, 10-19 21:01 UTC: need_tab, shared_hist, imp_age, aims, heights,
# world_answers, wa_phase2, foot_on, cause_fit), batch.py's v24 flags ($OFF_FLAGS) set False (the loaded aim and world
# answers moments move the draws even with the switches off) and the callings pack taken out of batch.PACKS (a pack is
# on once listed); a key moved with no UPD_OFF or V24_OFF value stops the run (the update rule: every new mechanic can
# be switched off). The new side's batch.py is edited in its own copy, not by environment, so the base side's kept
# digests (keyed by the CHROMA_ environment too) still serve. Results land in out/results.jsonl under the candidate (speedpass_s41 ...).
#
#   SHA=<full commit> bash k4.sh <part>     parts 1 2 3 4 (1s 1A 1B: part 1's runs alone)
#   WARM=1 bash k4.sh <part>                the base side only (BASE_ONLY), kept for the runs after it
#   DRY=1 SHA=<commit> bash k4.sh <part>    print PNEW and stop
set -u
R=$(cd "$(dirname "$0")/.." && pwd); REPO=${REPO:-$(cd "$R/.." && pwd)}; PART=${1:-}; D=chroma-engine/v22-speedpass
OUT=${OUT:-$R/out/v25/k4}
OFF_FLAGS="FOOT AIMS WORLD_ANSWERS"   # batch.py's v24 flags (False on main at f1e3fff; the refit may set them True)
case " 1 2 3 4 1s 1A 1B " in *" $PART "*) ;; *) sed -n 2,13p "$0"; exit 2 ;; esac
[ -n "${WARM:-}" ] || [ -n "${SHA:-}" ] || { sed -n 2,13p "$0"; exit 2; }
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_GAME CHROMA_ENGINE_DIR CHROMA_LIBRARY_DIR CHROMA_PACKS_DIR PNEW FRESH BASE_ONLY
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
X=${TMPDIR:-/tmp}/v25k4_$PART; t0=$(date +%s); mkdir -p $X
[ -e $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2
LIVE=$(git -C $REPO rev-parse origin/release/v23.2) || exit 2
[ "$LIVE" = 34721bbe7a30e58d24735f60b43dae4f3e1ee8b0 ] || { echo "STOP: release/v23.2 is at $LIVE, not 34721bb (Version 35)"; exit 2; }
rm -rf $X/base; mkdir -p $X/base && git -C $REPO archive $LIVE $D chroma-library chroma-packs | tar -x -C $X/base || exit 2
sed 's|^\[ -n "\$BASE" \] && SP+=(--base "\$BASE")$|[ -n "$BASE" ] \&\& SP+=(--base "$BASE"); SP+=(--lib "$BLIB" --packs "$BPACKS")|' $R/same-lives.sh > $X/sl.sh
grep -q -- '--lib "$BLIB"' $X/sl.sh || { echo "STOP: could not name the base Library in the copy of same-lives.sh"; exit 2; }
export BASE=$X/base/$D BLIB=$X/base/chroma-library BPACKS=$X/base/chroma-packs
if [ -n "${WARM:-}" ]; then
  echo "== K4 part $PART: the base side only, release/v23.2 ${LIVE:0:12}, $(date -u +%H:%M) UTC"
  BASE_ONLY=1 bash $X/sl.sh $PART 2>&1 | tee $X/out.txt | tail -n 8; rc=${PIPESTATUS[0]}
  echo "k4.sh WARM part $PART: exit $rc, $(( ($(date +%s) - t0) / 60 )) min"; exit $rc
fi
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
rm -rf $X/new; mkdir -p $X/new && git -C $REPO archive $SHA $D chroma-library chroma-packs | tar -x -C $X/new || exit 2
for f in $OFF_FLAGS; do
  grep -q "^$f = " $X/new/$D/batch.py || { echo "STOP: no '$f = ' line in the candidate's batch.py"; exit 2; }
  sed -i "s/^$f = True /$f = False /" $X/new/$D/batch.py
  grep -q "^$f = False" $X/new/$D/batch.py || { echo "STOP: could not set $f = False in batch.py"; exit 2; }
done
NEWPACKS="${NEWPACKS:-callings}"   # v24's new packs, out of batch.PACKS for the off run
for k in $NEWPACKS; do sed -i "/^PACKS = \[/s/, \"$k\"//" $X/new/$D/batch.py; done
grep -m1 '^PACKS = \[' $X/new/$D/batch.py | grep -q '"callings"' && { echo "STOP: callings still in the new side's batch.PACKS"; exit 2; }
echo "k4: new side's $(grep -m1 '^PACKS = \[' $X/new/$D/batch.py | cut -d'#' -f1)"
pnew=$(python3 -B - $X/new/$D $BASE <<'PY'
import sys, json, pickle, subprocess, tempfile
import numpy as np
READ = ("import sys, pickle; sys.path.insert(0, sys.argv[1]); import engine as E; "
        "pickle.dump((E.DEFAULT, {**E.UPD_OFF, **getattr(E, 'V24_OFF', {}), **getattr(E, 'V25_OFF', {})}), open(sys.argv[2], 'wb'))")
def read(d):   # each engine in its own process: two engines' sibling modules never mix in one
    with tempfile.NamedTemporaryFile(suffix=".pkl") as f:
        subprocess.run([sys.executable, "-B", "-c", READ, d, f.name], cwd=d, capture_output=True, check=True)
        return pickle.load(open(f.name, "rb"))
def same(x, y):
    if hasattr(x, "shape") or hasattr(y, "shape"):
        return bool(np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)))
    return x == y
(ND, NU), (LD, _) = read(sys.argv[1]), read(sys.argv[2])
P, stop, note = {}, [], []
for k, v in ND.items():
    if k in LD and same(LD[k], v):
        continue
    if k not in NU:
        (stop if k in LD else note).append(k)   # a new key with no off value: read only with its part's switch on
    elif not same(NU[k], LD.get(k, NU[k])):
        stop.append(k)                          # its off value is not v23.2's
    elif not same(NU[k], v):
        P[k] = NU[k]
if stop:
    sys.exit("STOP: DEFAULT moved from v23.2 with no UPD_OFF, V24_OFF or V25_OFF value equal to v23.2's: " + ", ".join(stop))
print("k4: settings new with their parts, left as they are: " + (", ".join(note) or "none"), file=sys.stderr)
print(json.dumps(P))
PY
) || { echo "$pnew"; exit 1; }
echo "== K4 part $PART: ${SHA:0:12} against release/v23.2 ${LIVE:0:12}, $(date -u +%H:%M) UTC"
echo "k4: PNEW=$pnew; batch $OFF_FLAGS off"
[ -n "${DRY:-}" ] && { echo "k4: DRY, the lives not run ($X)"; exit 0; }
NEW=$X/new/$D LIB=$X/new/chroma-library PACKS=$X/new/chroma-packs COMMIT=$SHA PNEW="$pnew" \
  bash $X/sl.sh $PART 2>&1 | tee $X/out.txt | tail -n 25; rc=${PIPESTATUS[0]}
mkdir -p $OUT && cp $X/out.txt $OUT/k4_part${PART}_${SHA:0:7}.txt
echo "k4.sh part $PART on ${SHA:0:12}: exit $rc, $(( ($(date +%s) - t0) / 60 )) min"; exit $rc
