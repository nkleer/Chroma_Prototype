#!/bin/bash
# v22.2.1 release record (the visual update alone on release/v22.2; records/v22.2.1/scope.md): one job per machine, run
# from anywhere. Every result lands in chroma-release/out/ with the record's commit (its "commit:" line, or SHA=), which is
# what record.py counts. Scratch under /tmp.
#   bash /mnt/project-files/chroma-release/short-v22.2.1/run.sh <job>
# Jobs:
#   rows       pin, build, art and the game's fast rows on the commit (V2, V6; a few minutes)
#   pageonly   the commit against release/v22.2: only page and art files change, worker.js and py/ equal (V1; two builds)
#   page       a fresh build served locally: the fit probes at 1280x800, 1024x700 and the geometric one, the phone probe
#              against the release/v22.2 build at 390x844 (options per moment, check_phonefit.py), and the tours at
#              desktop and phone size (V3, V4; about 30 min)
#   b7AB b7CD  the build of the commit, then the game's browser drivers, groups A and B or C and D (V5; one at a time
#              per machine, both serve on port 8140)
#   artlook    PR #98's art check (portraits, lights) from ART_REF on the commit's tree (V6, row art_look; seconds)
set -u
F=/mnt/project-files; R=${R:-$F/chroma-release}; REPO=${REPO:-/tmp/v2221_repo}; X=/tmp/v2221_$1; BASE=${BASE:-release/v22.2}
SHA=${SHA:-$(sed -n 's/^commit: *\([0-9a-f]\{40\}\) *$/\1/p' $F/chroma-release/records/v22.2.1/scope.md)}   # the record's commit line
[ -n "$SHA" ] || { echo "no commit in records/v22.2.1/scope.md yet"; exit 2; }
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2   # the commit sits on a branch, not on main
git -C $REPO cat-file -e $SHA^{commit} || { echo "STOP: $SHA is not in the repository"; exit 2; }
BASE_SHA=$(git -C $REPO rev-parse origin/$BASE) || exit 2
export CHROMA_COMMIT=$SHA PW=${PW:-/opt/node22/lib/node_modules/playwright}
O=${CHROMA_ROOT:-$(dirname $R)}/chroma-release/out; mkdir -p $O   # where results.py and the reports live
CHK="python3 -B $R/v22_checks.py --repo $REPO"
add() { python3 -B $R/results.py add "$@"; }                  # id, PASS or FAIL, report, note (with CHROMA_COMMIT)
build() { rm -rf $2; $CHK --commit $1 --only build --no-reuse --keep --work $2 > $2.log 2>&1   # a reused build leaves no folder
  [ -f $2/w/build/BUILD.md ] || { echo "STOP: no build in $2/w/build (see $2.log)"; exit 1; }; }
serve() { local b=$1/w/build s=$1/serve; rm -rf $s; cp -r $b/web $s; [ -d $s/pyodide ] || cp -r $F/chroma-release/tools/pyodide $s/
  setsid nohup python3 $b/chroma-game/prototype/test/serve.py $2 $s > $1/serve.log 2>&1 < /dev/null &
  for i in $(seq 1 60); do curl -sf -o /dev/null http://127.0.0.1:$2/page.html && return 0; sleep 1; done; echo "STOP: no server on $2"; exit 1; }
case "$1" in
  rows) $CHK --commit $SHA --only pin,build,art,icons,saveload,end_at_choice,saveload_world ;;
  pageonly) python3 -B $R/check_pageonly.py --repo $REPO --base $BASE_SHA --commit $SHA --work $X ;;
  page) mkdir -p $X; build $SHA $X/cand; build $BASE_SHA $X/base; serve $X/cand 8151; serve $X/base 8152
     T=$X/cand/w/build/chroma-game/prototype/test; L=$X/look/chroma-look/tools; mkdir -p $X/look $X/shots
     git -C $REPO archive $SHA chroma-look/tools | tar -x -C $X/look
     mkdir -p $X/look/chroma-game/prototype; ln -sfn $T $X/look/chroma-game/prototype/test   # tour.js finds the game's start.js
     U=http://127.0.0.1:8151/page.html; UB=http://127.0.0.1:8152/page.html; STAMP=$(date -u +%Y%m%d-%H%M%S)
     probe() { local id=$1 js=$2 url=$3 w=$4 h=$5 out=$O/${1}_$STAMP.txt
       (cd $T && timeout 3600 node $js $url $X/shots/$id 60 $w $h) > $out 2>&1; echo "exit $? " >> $out; echo $out; }
     for spec in "fit_1280 probe_fit_cx3.js 1280 800" "fit_1024 probe_fit_cx3.js 1024 700" "fit_geo probe_fit_geo.js 1280 800"; do
       set -- $spec; mkdir -p $X/shots/$1; o=$(probe $1 $2 $U $3 $4)
       if grep -q "^N7 .*: PASS" $o && ! grep -q pageerror $o; then add $1 PASS $o "$2 at $3x$4"; else add $1 FAIL $o "$2 at $3x$4"; fi
     done
     mkdir -p $X/shots/fit_phone $X/shots/fit_phone_base
     o=$(probe fit_phone probe_fit_cx3.js $U 390 844); ob=$(probe fit_phone_base probe_fit_cx3.js $UB 390 844)
     v=$(python3 -B $R/check_phonefit.py $o $ob) && r=PASS || r=FAIL   # options per moment: the two lives differ in length
     echo "$v (base report $ob)" >> $o
     add fit_phone $r $o "${v#phone 390x844 by options: }"
     for spec in "tour_desktop 1280 860" "tour_phone 390 844"; do
       set -- $spec; mkdir -p $X/shots/$1; o=$O/${1}_$STAMP.txt
       (cd $L && timeout 1800 node tour.js $U $X/shots/$1 $2 $3) > $o 2>&1; e=$?; echo "exit $e" >> $o
       if [ $e = 0 ] && grep -q "^no page errors" $o; then add $1 PASS $o "tour.js at $2x$3"; else add $1 FAIL $o "tour.js at $2x$3"; fi
     done
     pkill -f "serve.py 815[12]"; grep -h "" $O/*_$STAMP.txt | grep -E "^N7|^phone|^no page errors|pageerror|^exit" ;;
  b7AB|b7CD) build $SHA $X; g=${1#b7}; bash $R/short-v22.1/b7.sh ${g:0:1},${g:1:1} 2 $X/w/build ;;
  artlook) A=${ART_REF:-origin/claude/project-thread-fidk7k}; AS=$(git -C $REPO rev-parse $A) || exit 2   # PR #98's branch
     rm -rf $X; mkdir -p $X; git -C $REPO archive $SHA chroma-art chroma-env chroma-game/prototype/engine_pin chroma-game/prototype/web/src chroma-look | tar -x -C $X
     git -C $REPO show $AS:chroma-art/kit/check_art.py > $X/chroma-art/kit/check_art.py; o=$O/art_look_$(date -u +%Y%m%d-%H%M%S).txt
     { echo "v22.2.1 V6 art_look: chroma-art/kit/check_art.py of $A ($AS) on the tree of $SHA"; (cd $X && CHROMA_ROOT=$X python3 -B chroma-art/kit/check_art.py 2>&1); } > $o
     cat $o; if grep -q "^art check: pass" $o; then add art_look PASS $o "check_art.py of $A on the commit's tree"; else add art_look FAIL $o "check_art.py of $A on the commit's tree"; fi ;;
  *) sed -n 2,16p "$0"; exit 2 ;;
esac
