#!/bin/bash
# v22.1 B7, split over containers (coordinator 10-08): the game's browser drivers on the v22.1 build, a group at a time.
# Run from any container; reads the shared folder only and writes one report, chroma-release/out/b7_<groups>_<UTC>.txt.
#   bash /mnt/project-files/chroma-release/short-v22.1/b7.sh <groups, e.g. A or A,B> [jobs, default 2] [build]
# The build is the out folder of the one build command (chroma-game/tools/build.py <out>, backend plan item 5): its web/
# is served as it is and its game's test/ drivers run. A prototype folder still works (its web/ is assembled here), and
# with no build given, /tmp/v22p1_build/prototype or a fresh make_tree.sh layout in /tmp/b7_tree.
# The page is served from /tmp/b7_<groups>/serve on port 8140 with the Pyodide copy in chroma-release/tools/pyodide.
set -u
GROUPS_=${1:?groups}; JOBS=${2:-2}; P=${3:-/tmp/v22p1_build/prototype}
F=/mnt/project-files; R=$F/chroma-release; TAG=$(echo "$GROUPS_" | tr -d ','); B=/tmp/b7_$TAG; PORT=8140
export PW=${PW:-/opt/node22/lib/node_modules/playwright}
if [ -f "$P/BUILD.md" ] && [ -f "$P/web/page.html" ]; then        # an out folder of chroma-game/tools/build.py
  OUT=$P; P=$OUT/chroma-game/prototype; W=$OUT/web; rm -rf $B; mkdir -p $B/test $B/out
  cp -r $W $B/serve; [ -d $B/serve/pyodide ] || cp -r $R/tools/pyodide $B/serve/
else
  if [ ! -f "$P/web/index.html" ]; then
    rm -rf /tmp/b7_tree; mkdir -p /tmp/b7_tree; bash $F/chroma-game/staging-v22p1/make_tree.sh /tmp/b7_tree > /tmp/b7_tree.log 2>&1 || { echo "make_tree failed: see /tmp/b7_tree.log"; exit 2; }
    P=/tmp/b7_tree/prototype
  fi
  W=$P/web; rm -rf $B; mkdir -p $B/serve/py $B/test $B/out
  { printf '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}</style></head><body>'; cat $W/index.html; printf '</body></html>'; } > $B/serve/page.html
  cp $W/worker.js $B/serve/; cp -r $R/tools/pyodide $B/serve/; ln -sfn $F/chroma-art/game/pics $B/serve/pics
  for f in $(grep -o '"[a-z_/]*\.py"' $W/worker.js | tr -d '"'); do mkdir -p $B/serve/py/$(dirname $f); cp $P/$f $B/serve/py/$f; done
fi
cp $P/test/*.js $P/test/serve.py $B/test/
SPID=$(setsid nohup python3 $B/test/serve.py $PORT $B/serve > $B/serve.log 2>&1 < /dev/null & echo $!)
trap 'kill $SPID 2>/dev/null' EXIT
U=http://127.0.0.1:$PORT/page.html; O=$B/out
declare -A G
G[A]="perks_d perks_p hud2_d hud2_p book"
G[B]="roles_d roles_p v7_d v7_p season world"
G[C]="life_birth_d life_adult_p v14_d v14_p longshot"
G[D]="drive_d drive_p against facet_d facet_p politics"
G[T]="against"   # smoke test
cmd() { case $1 in
  drive_d) echo "node drive.js $U $O/drive_d.png '[\"3\",\"Lale\",\"\",\"\",\"2\",\"\",\"y\",\"d\"]' 1280" ;;
  drive_p) echo "node drive.js $U $O/drive_p.png '[\"3\",\"Lale\",\"\",\"\",\"2\",\"\",\"y\"]' 400" ;;
  hud2_d) echo "node drive_hud2.js $U h2d 1280 860 $O" ;;      hud2_p) echo "node drive_hud2.js $U h2p 400 860 $O" ;;
  v7_d) echo "node drive_v7.js $U v7d 1280 860 $O 3" ;;         v7_p) echo "node drive_v7.js $U v7p 400 860 $O 3" ;;
  v14_d) echo "node drive_v14.js $U v14d 1280 860 $O 3" ;;      v14_p) echo "node drive_v14.js $U v14p 400 860 $O 3" ;;
  against) echo "node drive_against.js $U $O/against.png 2" ;;
  roles_d) echo "node drive_roles.js $U rd 1280 860 $O 3 35" ;; roles_p) echo "node drive_roles.js $U rp 400 860 $O 3 30" ;;
  facet_d) echo "node drive_facet.js $U $O 3 1280" ;;           facet_p) echo "node drive_facet.js $U $O 3 400" ;;
  perks_d) echo "node drive_perks.js $U $O 50 1280" ;;          perks_p) echo "node drive_perks.js $U $O 45 400" ;;
  book) echo "env PORT=$PORT node drive_book.js $O" ;;          longshot) echo "node drive_longshot.js $O $PORT" ;;
  season) echo "env PORT=$PORT node drive_season.js $O" ;;      world) echo "env PORT=$PORT node drive_world.js $O" ;;
  politics) echo "node drive_politics.js $O $PORT 3 1360" ;;
  life_birth_d) echo "node drive_life.js $U $O birth_d 1 1360 880 40" ;;
  life_adult_p) echo "node drive_life.js $U $O adult_p 3 400 860 40" ;;
esac; }
run() { local n=$1 s; s=$(date +%s); (cd $B/test && eval "timeout 2700 $(cmd $n)") > $O/$n.log 2>&1; local e=$?
  echo "exit $e in $(( $(date +%s) - s ))s" >> $O/$n.log; }
LIST=""; for g in $(echo "$GROUPS_" | tr ',' ' '); do LIST="$LIST ${G[$g]}"; done
for i in $(seq 1 60); do curl -sf -o /dev/null $U && break; sleep 1; done
REP=$R/out/b7_${TAG}_$(date -u +%Y%m%d-%H%M%S).txt
md5() { md5sum < $1 | cut -c1-12; }
{ echo "v22.1 B7 drivers, groups $GROUPS_, $(date -u '+%Y-%m-%d %H:%M') UTC, $(hostname)"
  echo "  build $P (index.html $(md5 $W/index.html), app.js $(md5 $P/web/src/app.js), engine_pin/engine.py $(md5 $P/engine_pin/engine.py)); $JOBS at a time"; } > $REP
for n in $LIST; do
  while [ $(jobs -rp | wc -l) -ge $JOBS ]; do wait -n; done
  run $n &
done
wait
bad=0
for n in $LIST; do
  pe=$(grep -c pageerror $O/$n.log); ex=$(tail -1 $O/$n.log); last=$(grep -v "^exit " $O/$n.log | tail -1 | cut -c1-200)
  ok=ok; case "$ex" in "exit 0 "*) [ "$pe" = 0 ] || ok=MISS ;; *) ok=MISS ;; esac; [ $ok = ok ] || bad=$((bad + 1))
  printf '%-4s %-13s %s, %s page errors: %s\n' $ok $n "$ex" $pe "$last" >> $REP
done
echo "B7 groups $GROUPS_: $([ $bad = 0 ] && echo PASS || echo "FAIL ($bad)"); logs and pictures in $O" >> $REP
python3 -B $R/results.py add b7_$TAG $([ $bad = 0 ] && echo PASS || echo FAIL) $REP "browser drivers, groups $GROUPS_"   # item 4
cat $REP; [ $bad = 0 ]
