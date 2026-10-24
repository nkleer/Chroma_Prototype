#!/bin/bash
# v24 FP1 to FP3 (records/v24/scope.md) on a commit, about a minute on one core: the owners' footprint checks on the
# commit's own tree (git archive) and Release's fp_marks.py. Report out/v24/fp/fp_<sha7>_<UTC>.txt; results lines
# fp_pilot, fp_earth, fp_packs, fp_callings, fp_marks under the commit (NORECORD=1: report only).
#   FP1, FP2 Earth  chroma-library/tests/check_footprint.py (its checked moments, footprint_moments.txt, are every Earth
#                   life event with the 80 pictured first, so one run reads both; build.py from the shared folder)
#   FP2 packs       chroma-packs/tools/check_footprint_packs.py, every pack
#   FP2 callings    the same with --built: the shared folder's Library build.py run on a copy of chroma-packs/callings/
#   FP3             fp_marks.py
#
#   SHA=<commit> bash fp.sh
set -u
F=/mnt/project-files; R=$F/chroma-release; H=$R/out/v24/fp; REPO=${REPO:-/tmp/next_repo}
[ -n "${SHA:-}" ] || { sed -n 2,12p "$0"; exit 2; }
export PYTHONDONTWRITEBYTECODE=1
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e "$SHA^{commit}" 2>/dev/null || git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
X=/tmp/v24fp_${SHA:0:7}; rm -rf $X; mkdir -p $X/tree $X/cb
git -C $REPO archive $SHA chroma-library chroma-packs chroma-engine/v22-speedpass chroma-env | tar -x -C $X/tree || exit 2
O=$H/fp_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt
add() { [ -n "${NORECORD:-}" ] || CHROMA_COMMIT=$SHA python3 -B $R/results.py add "$1" "$2" "${O#$F/}" "$3"; }
last() { tail -n 1 "$1" | grep -qx 'no problems' && echo PASS || echo FAIL; }
( cd $X/tree/chroma-library && PYTHONPATH=$F/chroma-library python3 -B tests/check_footprint.py . > $X/earth.txt 2>&1 )
( cd $X/tree && python3 -B chroma-packs/tools/check_footprint_packs.py > $X/packs.txt 2>&1 )
cp $X/tree/chroma-packs/callings/*.lib $F/chroma-library/build.py $X/cb/
( cd $X/cb && PYTHONPATH=$F/chroma-library python3 -B build.py callings > $X/cbuild.txt 2>&1 )
( cd $X/tree && python3 -B chroma-packs/tools/check_footprint_packs.py --built $X/cb callings > $X/callings.txt 2>&1 )
python3 -B $H/fp_marks.py $X/tree > $X/marks.txt 2>&1
pil=$(head -n 80 $X/tree/chroma-library/footprint_moments.txt | grep -c .)
{ echo "v24 FP1 to FP3 on ${SHA:0:12}, $(date -u '+%Y-%m-%d %H:%M') UTC"
  echo; echo "== FP1 and FP2 Earth: chroma-library/tests/check_footprint.py ($pil pictured moments first in footprint_moments.txt)"; cat $X/earth.txt
  echo; echo "== FP2 packs: chroma-packs/tools/check_footprint_packs.py"; grep -v '^    ' $X/packs.txt
  echo; echo "== FP2 callings: build.py (shared folder, md5 $(md5sum < $F/chroma-library/build.py | cut -c1-12)) on chroma-packs/callings/, then --built"
  cat $X/cbuild.txt; grep -v '^    ' $X/callings.txt
  echo; echo "== FP3"; cat $X/marks.txt; } > $O
e=$(last $X/earth.txt); p=$(last $X/packs.txt); c=$(last $X/callings.txt)
grep -q '^callings (' $X/callings.txt || c=FAIL
m=$(grep -q '^FP3: PASS' $X/marks.txt && echo PASS || echo FAIL)
{ echo; echo "fp_pilot $e  fp_earth $e  fp_packs $p  fp_callings $c  fp_marks $m"; } >> $O
add fp_pilot $e "check_footprint.py: no problems over every Earth life event, the $pil pictured among them"
add fp_earth $e "check_footprint.py: $(grep -o '^footprints: [0-9]* moments, [0-9]* options' $X/earth.txt)"
add fp_packs $p "check_footprint_packs.py, every pack; three-footprint options left as they are listed (Rulings)"
add fp_callings $c "check_footprint_packs.py --built on the callings pack built by the Library's build.py"
add fp_marks $m "fp_marks.py: $(head -n 1 $X/marks.txt | sed 's/^FP3 on [^:]*: //')"
cat $O | tail -n 25; echo "report $O"
[ $e = PASS ] && [ $p = PASS ] && [ $c = PASS ] && [ $m = PASS ]
