#!/bin/bash
# G16 with the outer world on (records/v22.4/scope.md, "G16 with the world on"): the commit's rarity table rebuilt
# from the commit's own engine, Library and packs with its own tools/rarity_build.py, as the Engine built it (200 lives a
# seed, seeds 101 to 120, each drawing its own world), equals the committed table byte for byte, the engine's and the
# game's. The seeds split over machines; the table is the same however they are split (the tool's own claim).
#
#   SHA=<commit> PART=<first>-<last>|merge [LIVES=200] [SEEDS=20] [REPO=/tmp/v224_repo] bash .../short-v22.4/rarity_w.sh
#   PART=101-105 runs seeds 101 to 105, each written to out/rarity_parts_<sha12>_<LIVES>x<SEEDS>/part_<seed>.json (the
#   shared folder); merge (once every seed's part is there): the table from the parts, compared with the commit's
#   chroma-engine/v22-speedpass/rarity.json and chroma-game/prototype/rarity.json; the result goes to out/results.jsonl
#   as rarity_w.
F=/mnt/project-files; R=$F/chroma-release; REPO=${REPO:-/tmp/v224_repo}; N=${LIVES:-200}; K=${SEEDS:-20}
[ -n "$SHA" ] && [ -n "$PART" ] || { echo "SHA=<commit> PART=<first>-<last>|merge are needed"; exit 2; }
case $PART in
  merge) ;;
  [0-9]*-[0-9]*) a=${PART%-*}; b=${PART#*-}
     [ $a -ge 101 ] && [ $b -le $((100 + K)) ] && [ $a -le $b ] || { echo "PART $PART is not within seeds 101 to $((100 + K))"; exit 2; } ;;
  *) echo "PART is <first>-<last> (seeds 101 to $((100 + K))) or merge"; exit 2 ;;
esac
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
D=$R/out/rarity_parts_${SHA:0:12}_${N}x$K; mkdir -p $D
E=/tmp/v224_rw_${PART}_$(date -u +%H%M%S)
git -C $REPO worktree add -q --detach $E $SHA || exit 2
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_PROJECT LIB PACKS PACK_DIR PACK_MOMENTS OUT OUT_DIR FINAL_LIB
cd $E/chroma-engine/tools || exit 2
case $PART in
  [0-9]*-[0-9]*) python3 -B rarity_build.py $N $K --only $(seq -s, ${PART%-*} ${PART#*-}) --parts $D; rc=$? ;;
  merge) OUT=$E/rebuilt.json python3 -B rarity_build.py $N $K --merge $D; rc=$?
     o=$R/out/rarity_w_$(date -u +%Y%m%d-%H%M%S).txt
     if [ $rc = 0 ]; then
       t=$R/out/rarity_rebuild_$(date -u +%Y%m%d-%H%M)_world.json; cp $E/rebuilt.json $t; echo "$SHA rarity_w" > $t.from
       ce=$(cmp -s $E/rebuilt.json $E/chroma-engine/v22-speedpass/rarity.json && echo same || echo DIFFERENT)
       cg=$(cmp -s $E/rebuilt.json $E/chroma-game/prototype/rarity.json && echo same || echo DIFFERENT)
       { echo "v22.4 G16 rarity_w on ${SHA:0:12}: rarity_build.py $N $K (world on) from the parts in $D"
         echo "rebuilt $t (md5 $(md5sum < $t | cut -c1-12)); the engine's rarity.json: $ce; the game's rarity.json: $cg"
         [ $ce = same ] && [ $cg = same ] && echo "RARITY_W: PASS" || echo "RARITY_W: FAIL"; } > $o
       cat $o
       res=$([ $ce = same ] && [ $cg = same ] && echo PASS || echo FAIL); [ $res = PASS ] || rc=1
       CHROMA_COMMIT=$SHA python3 -B $R/results.py add rarity_w $res $o "rebuilt with the world on ($N lives x $K seeds), engine table $ce, game table $cg"
     fi ;;
esac
cd /; git -C $REPO worktree remove --force $E
exit $rc
