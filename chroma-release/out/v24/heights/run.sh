#!/bin/bash
# v24 heights on a candidate (records/v24/scope.md A1 to A5): the A0 baseline's tools (out/heights/heights_play.py, and
# heights_engine24.py here, its copy with the aims added) on any commit, one job a machine of 4 cores. Output in
# out/v24/heights/play_<sha7>[_<tag>]/ and engine_<sha7>/; heights_v24.py judges them against the baseline.
#
#   SHA=<full commit> [BR=<branch holding it>] [TAG=<name> GAMESET='<json>'] [SEEDS='7 8 9 10 11 12'] bash run.sh <job>
#   none let reader reader-aims oracle   played lives, presets 1 to 4 x seeds 1 to 6 (the baseline's), 4 at a time,
#                                        about 15 to 25 minutes; GAMESET is laid over the game's settings (CHROMA_GAME)
#                                        and TAG names its folder (A5: TAG=boldoff GAMESET='{"bold": false}'); other
#                                        SEEDS go to wide_<sha7>/ (A1 read on 48 lives in v24, scope.md Rulings)
#   steerU                               PB (v25 SK1, SK2): always pushing Blue, impact.py's steer:U, as reader-aims's 24 lives
#   engine                               lives left alone, seeds 41 to 44 side by side, 400 lives x 100 years each, one
#                                        core a seed (about 61 minutes a seed on v23.1)
#   eng41 eng42 eng43 eng44              one of those seeds alone
set -u
F=/mnt/project-files; R=$F/chroma-release; H=$R/out/v24/heights; REPO=${REPO:-/tmp/next_repo}; JOB=${1:-}
case " none let reader reader-aims oracle steerU engine eng41 eng42 eng43 eng44 " in *" $JOB "*) ;; *) sed -n 2,15p "$0"; exit 2 ;; esac
[ -n "${SHA:-}" ] || { sed -n 2,15p "$0"; exit 2; }
[ -z "${GAMESET:-}" ] || [ -n "${TAG:-}" ] || { echo "TAG=<name> is needed with GAMESET"; exit 2; }
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_GAME CHROMA_ENGINE_DIR CHROMA_LIBRARY_DIR CHROMA_PACKS_DIR READ_GOALS
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e "$SHA^{commit}" 2>/dev/null || git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2; S7=${SHA:0:7}
X=/tmp/h24_${JOB}${TAG:+_$TAG}; WT=$X/wt; t0=$(date +%s)
git -C $REPO worktree remove --force $WT 2>/dev/null; rm -rf $WT; mkdir -p $X
git -C $REPO worktree add -q --detach $WT $SHA || exit 2
echo "== heights $JOB${TAG:+ ($TAG: $GAMESET)} on ${SHA:0:12}, $(date -u +%H:%M) UTC"
if [[ $JOB == eng* ]]; then
  O=$H/engine_$S7; mkdir -p $O; cp $H/heights_engine24.py $X/
  seeds=$([ $JOB = engine ] && echo "41 42 43 44" || echo ${JOB#eng})
  for s in $seeds; do
    [ -f $O/eng_$s.json ] && { echo "seed $s kept: $O/eng_$s.json"; continue; }
    ( python3 -B $X/heights_engine24.py $WT $s 400 100 $X/eng_$s.json > $X/eng_$s.log 2>&1 && cp $X/eng_$s.json $X/eng_$s.log $O/ ) &
  done; wait
  got=0; for s in $seeds; do [ -f $O/eng_$s.json ] && got=$((got + 1)); tail -n 1 $X/eng_$s.log 2>/dev/null; done
  n=$(echo $seeds | wc -w)
  echo "run.sh $JOB on ${SHA:0:12}: $got of $n seeds in $O, $(( ($(date +%s) - t0) / 60 )) min"; [ $got = $n ]; exit
fi
python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$WT/chroma-game/prototype', root='$WT')" || exit 2
SEEDS=${SEEDS:-1 2 3 4 5 6}; W=play; [ "$SEEDS" = "1 2 3 4 5 6" ] || W=wide
O=$H/${W}_$S7${TAG:+_$TAG}; OUT=$X/${W/play/}lives_$S7; mkdir -p $OUT $O   # lives kept by commit: a rerun on another commit plays afresh
cp $R/out/heights/heights_play.py $X/heights_play.py
POL=$JOB; [ "$JOB" = reader-aims ] && { POL=reader; export READ_GOALS=1; }
[ "$JOB" = steerU ] && POL=steer:U
[ -n "${GAMESET:-}" ] && export CHROMA_GAME="$GAMESET"
run1() { python3 -B $X/heights_play.py $WT/chroma-game/prototype $POL $1 $2 $OUT/${JOB}_$1_$2.json >> $X/run.log 2>&1 || echo "life $1 $2 failed" >> $X/run.log; }
n=0; touch $X/run.log
for p in 1 2 3 4; do for s in $SEEDS; do
  [ -f $OUT/${JOB}_${p}_${s}.json ] && continue
  run1 $p $s & n=$((n + 1)); [ $((n % 4)) -eq 0 ] && wait
done; done; wait
cp $OUT/*.json $O/ 2>/dev/null; cp $X/run.log $O/run_$JOB.log
got=$(ls $OUT/*.json 2>/dev/null | wc -l); bad=$(grep -c failed $X/run.log)
tail -n 4 $X/run.log
echo "run.sh $JOB${TAG:+ ($TAG)} on ${SHA:0:12}: $got of 24 lives into $O, $bad failed, $(( ($(date +%s) - t0) / 60 )) min"
[ "$got" -eq 24 ] && [ "$bad" -eq 0 ]
