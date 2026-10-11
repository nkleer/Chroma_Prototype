#!/bin/bash
# G16 with the outer world on (records/v22.4/scope.md, "G16 with the world on"; the Engine's rarity_build.py from
# 6cc6c8e: 500 lives a seed, seeds 101 to 108, each drawing its own world): the commit's rarity table rebuilt from the
# commit's own engine, Library and packs equals the committed table byte for byte, the engine's and the game's. The
# seeds split over two machines; the table is the same however they are split (the tool's own claim).
#
#   SHA=<commit> PART=a|b|merge [REPO=/tmp/v224_repo] bash chroma-release/short-v22.4/rarity_w.sh
#   a: seeds 101 to 104, b: 105 to 108, each part written to out/rarity_parts_<sha12>/part_<seed>.json (the shared
#   folder); merge (once all eight are there): the table from the parts, compared with the commit's
#   chroma-engine/v22-speedpass/rarity.json and chroma-game/prototype/rarity.json; the result goes to out/results.jsonl
#   as rarity_w. LIVES=<n> runs a trial into a parts folder of its own (its merge never matches).
F=/mnt/project-files; R=$F/chroma-release; REPO=${REPO:-/tmp/v224_repo}; N=${LIVES:-500}
[ -n "$SHA" ] && [ -n "$PART" ] || { echo "SHA=<commit> PART=a|b|merge are needed"; exit 2; }
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
D=$R/out/rarity_parts_${SHA:0:12}$([ "$N" = 500 ] || echo "_n$N"); mkdir -p $D
E=/tmp/v224_rw_${PART}_$(date -u +%H%M%S)
git -C $REPO worktree add -q --detach $E $SHA || exit 2
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_PROJECT LIB PACKS PACK_DIR PACK_MOMENTS OUT OUT_DIR FINAL_LIB
cd $E/chroma-engine/tools || exit 2
case $PART in
  a) python3 -B rarity_build.py $N 8 --only 101,102,103,104 --parts $D; rc=$? ;;
  b) python3 -B rarity_build.py $N 8 --only 105,106,107,108 --parts $D; rc=$? ;;
  merge) OUT=$E/rebuilt.json python3 -B rarity_build.py $N 8 --merge $D; rc=$?
     o=$R/out/rarity_w_$(date -u +%Y%m%d-%H%M%S).txt
     if [ $rc = 0 ]; then
       t=$R/out/rarity_rebuild_$(date -u +%Y%m%d-%H%M)_world.json; cp $E/rebuilt.json $t; echo "$SHA rarity_w" > $t.from
       ce=$(cmp -s $E/rebuilt.json $E/chroma-engine/v22-speedpass/rarity.json && echo same || echo DIFFERENT)
       cg=$(cmp -s $E/rebuilt.json $E/chroma-game/prototype/rarity.json && echo same || echo DIFFERENT)
       { echo "v22.4 G16 rarity_w on ${SHA:0:12}: rarity_build.py $N 8 (world on) from the parts in $D"
         echo "rebuilt $t (md5 $(md5sum < $t | cut -c1-12)); the engine's rarity.json: $ce; the game's rarity.json: $cg"
         [ $ce = same ] && [ $cg = same ] && echo "RARITY_W: PASS" || echo "RARITY_W: FAIL"; } > $o
       cat $o
       res=$([ $ce = same ] && [ $cg = same ] && echo PASS || echo FAIL); [ $res = PASS ] || rc=1
       CHROMA_COMMIT=$SHA python3 -B $R/results.py add rarity_w $res $o "rebuilt with the world on ($N lives x 8 seeds), engine table $ce, game table $cg"
     fi ;;
  *) echo "PART is a, b or merge"; rc=2 ;;
esac
cd /; git -C $REPO worktree remove --force $E
exit $rc
