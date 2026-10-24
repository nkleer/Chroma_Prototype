#!/bin/bash
# v25 LA on the freeze candidate: lives left alone with the shipped set (engine.SHIP_V25 over DEFAULT, batch flags
# engine.SHIP_V25_BATCH; records/v25/scope.md "The shipped settings"), 400 lives x 100 years a seed, one core a seed,
# into out/v24/heights/engine_<sha7>_ship/eng_<seed>.json. Cloud only (evaluation.md section 5), and only on a machine
# whose lives equal Release's container's (cloud_lib.sh's probes, about 3 minutes); else it stops with STOP.
#
#   SEEDS='41 42 43 44' bash /mnt/project-files/chroma-release/out/v25/la_ship.sh
#
# DRY=1 sets up, probes and stops. A finished seed is kept and skipped on a rerun. Prints one line a seed and a last
# line "la_ship: k of n seeds".
set -u
. /mnt/project-files/chroma-release/out/v25/cloud_lib.sh
[ -n "${SEEDS:-}" ] || { sed -n 2,10p "$0"; exit 2; }
X=${TMPDIR:-/tmp}/la_$S7; O=$H/engine_${S7}_ship; mkdir -p $X
setup_tree $X || { echo "STOP: no tree for $SHA"; exit 2; }
if [ "$SHA" = "$E25" ]; then same_machine $X; else probe_here; fi || exit 3   # a commit whose lives equal E's (records/v25/STATE.md) probes on E
cp $H/heights_engine24.py $X/; [ "$(md5sum < $X/heights_engine24.py | cut -c1-32)" = c196bfdf055089bfcd453129403da649 ] || { echo "STOP: heights_engine24.py changed"; exit 2; }
PX=$(ship_px $X/wt) || exit 2; mkdir -p $O
echo "== la_ship on ${SHA:0:12}: seeds $SEEDS, $(date -u +%H:%M) UTC, $(hostname), $CORES cores; px $PX"
[ -n "${DRY:-}" ] && { echo "DRY: set up, no lives run"; exit 0; }
t0=$(date +%s); n=0
for s in $SEEDS; do
  [ -f $O/eng_$s.json ] && { echo "seed $s kept"; continue; }
  ( python3 -B $X/heights_engine24.py $X/wt $s 400 100 $X/eng_$s.json "$PX" > $X/eng_$s.log 2>&1 \
      && echo "$ME" > $X/machine_$s.txt && cp $X/eng_$s.json $X/eng_$s.log $X/machine_$s.txt $O/ \
      && echo "seed $s done, $(( ($(date +%s) - t0) / 60 )) min" || { echo "seed $s FAILED:"; tail -5 $X/eng_$s.log; } ) &
  n=$((n + 1)); [ $((n % CORES)) -eq 0 ] && wait
done; wait
got=0; for s in $SEEDS; do [ -f $O/eng_$s.json ] && got=$((got + 1)); done
echo "la_ship: $got of $(echo $SEEDS | wc -w) seeds in $O, $(( ($(date +%s) - t0) / 60 )) min"
[ $got = $(echo $SEEDS | wc -w) ]
