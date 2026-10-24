#!/bin/bash
# v24 N1 to N3's base (records/v24/scope.md): needs_check.py run on release/v23.2 (34721bb, the live game, Version 35),
# seeds 41 to 44 side by side, 400 lives x 100 years each, one core a seed (about 65 minutes), into
# out/v24/needs/34721bb/. short-v24/run.sh ndm judges a commit's runs against it.
#   bash base.sh
set -u
F=/mnt/project-files; H=$F/chroma-release/out/v24/needs; REPO=${REPO:-/tmp/next_repo}; X=/tmp/v24_needs_base; t0=$(date +%s)
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_GAME CHROMA_ENGINE_DIR CHROMA_LIBRARY_DIR CHROMA_PACKS_DIR CHROMA_PACKS CHROMA_BATCH_OFF
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO fetch -q origin '+refs/heads/release/v23.2:refs/remotes/origin/release/v23.2' || exit 2
SHA=$(git -C $REPO rev-parse origin/release/v23.2) || exit 2
[ "$SHA" = 34721bbe7a30e58d24735f60b43dae4f3e1ee8b0 ] || { echo "STOP: release/v23.2 is at $SHA, not 34721bb"; exit 2; }
rm -rf $X; mkdir -p $X/tree $H/34721bb
git -C $REPO archive $SHA chroma-engine chroma-library chroma-packs chroma-env chroma-game/prototype | tar -x -C $X/tree || exit 2
cp $H/needs_check.py $X/; echo "needs_check.py md5 $(md5sum < $X/needs_check.py | cut -c1-12)"
for s in 41 42 43 44; do
  [ -f $H/34721bb/s$s.json ] && { echo "seed $s kept"; continue; }
  ( python3 -B $X/needs_check.py run $X/tree $s 400 100 $X/s$s.json > $X/s$s.log 2>&1 && cp $X/s$s.json $X/s$s.log $H/34721bb/ ) &
done; wait
n=$(ls $H/34721bb/s*.json 2>/dev/null | wc -l); for s in 41 42 43 44; do tail -n 1 $X/s$s.log 2>/dev/null; done
echo "base.sh on ${SHA:0:12}: $n of 4 seeds in $H/34721bb, $(( ($(date +%s) - t0) / 60 )) min"; [ $n = 4 ]
