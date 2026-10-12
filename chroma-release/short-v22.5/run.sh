#!/bin/bash
# v22.5 release record (records/v22.5/scope.md, rows K1 to K28): one job a machine of about 4 cores, run from anywhere.
# Every result lands in chroma-release/out/ with the commit it checked. Scratch under /tmp. Two commits:
#   the refit   the Engine's refit commit (engine/v225-allon): the engine-only jobs, while the rarity table is rebuilt
#   the final   the record's commit: main after the refit merge, its rarity table and the Game's re-pin
#
#   SHA=<refit> bash /mnt/project-files/chroma-release/short-v22.5/run.sh <refit job>
#   SHA=<final> REFIT=<refit> bash /mnt/project-files/chroma-release/short-v22.5/run.sh <final job>
#
# On the refit (engine-only; nothing they read is in the game, so they carry to the final commit when the engine,
# Library and packs differ only in the rarity files):
#   rar1 .. rar5   the world-on rarity rebuild (K25), seeds 101-104, 105-108, 109-112, 113-116, 117-120 a machine
#   rarm           its merge, once the five parts are in: the rebuilt table for the Engine's rarity.json and the re-pin
#   f9a .. f9f     check_f9 seeds 41-42, 43-44, .. 51-52 into out/f9_<refit7> (K6 to K13, K15, K16; judged in `final`)
#   f8a f8b f8c    check_roll f8_after seeds 41-44, 45-48 and 49-52 into out/roll8_<refit7>_<seeds> (K9; judged in rollA)
#   engA           t_steps and identity1 (K3)
#   engB | engB1 engB2 engB3   K5's engine rows and S5: death, child_deaths, satisf, accept | chance, season, exits,
#                  inertia, goals | s5_lines, s5_money
#   mech           S1, S3, S4 and S6 (K19)
#   s7             s7_lead (K19: falls 1.5x and time in post 1.2x)
#   c26a c26b      G19 and G19w with the lift judged (K20)
#   lives          lean41-44, nopack41-44, lean, pie and pie41 in one call (K5; pie reads the npz of the same run)
#   g4 | g4s g4a g4b   K4: same-lives part 1 (seed 41, sweeps A and B; or each alone) with every V225 key at its UPD_OFF
#                  value and batch.AGE_FIT off, against live v22.4.1
#   fit4 fit6      check_fit f4_age and f6_dreams (K17; engine-only, carried)
# On the final commit:
#   quick | q1 .. q5   K1, K2, K22's quick game rows, K23's old saves and K28 lines_tied (pin and build need the re-pin):
#                  the fast rows | timeless | life_ends, identity_g | fuzz, markers | lines_tied
#   game | gameA gameB gameC   book_check and kin | the steered rows | own_even (K21, K22)
#   pr30 | pr30a pr30b pr30c pr30m   push_rare on 30 seeds (K21): one machine, or seeds 1-10, 11-20, 21-30, then the merge
#   b7A b7B b7C b7D | b7AB b7CD   the browser drivers (K24; one per machine: they serve on port 8140)
#   roll | rollA rollB rollC   K9's f8_after judged once from the f8a-c folders (carried) | f10_once (its engine lives
#                  from f8a's folder) | f7_roll (K18), every one --as-is
#   fit | fitk f15 check_fit all (K17), then check_f15 (K14); or each on its own machine
#   fit12          check_fit f12_start (K17; the game)
#   f15a .. f15d f15m   check_f15 in four parts into out/f15_<final7> (the starts with an upbringing, seeds 1-20 and
#                  start 1 | 21-40 | the far starts, seeds 1-30 | 31-60), then the judge that records f15_lean (K14)
#   page           the page layer against release/v22.4.1, the fit probes and the tours (K26)
#   final          the refit's rows on the final commit: v22_checks rows again (reused in seconds where nothing they
#                  read changed), the hand rows carried (g4's speedpass rows, pie and pie41, f4_age and f6_dreams,
#                  check_f9's ten tables, rarity_w) with the evidence in out/carry_<final7>.txt, each carried line's
#                  note saying so
set -u
JOBS=" rar1 rar2 rar3 rar4 rar5 rarm f9a f9b f9c f9d f9e f9f f8a f8b f8c engA engB engB1 engB2 engB3 mech s7 c26a c26b
 lives g4 g4s g4a g4b fit4 fit6 quick q1 q2 q3 q4 q5 game gameA gameB gameC pr30 pr30a pr30b pr30c pr30m b7A b7B b7C b7D
 b7AB b7CD roll rollA rollB rollC fit fitk fit12 f15 f15a f15b f15c f15d f15m page final "
[[ "${JOBS//$'\n'/ }" == *" ${1:-none} "* ]] || { sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2; }
F=/mnt/project-files; R=$F/chroma-release; REPO=${REPO:-/tmp/v225_repo}; X=/tmp/v225_${1:-}
K=/tmp/v225_keep   # --keep --work folders: the same path on every machine, so `final` reuses the refit's proofs
[ -n "${SHA:-}" ] || { echo "SHA=<commit> is needed"; exit 2; }
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e "$SHA^{commit}" 2>/dev/null || git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
REFIT=${REFIT:-}; [ -n "$REFIT" ] && { REFIT=$(git -C $REPO rev-parse "$REFIT^{commit}") || exit 2; }
export CHROMA_COMMIT=$SHA PW=${PW:-/opt/node22/lib/node_modules/playwright}
O=$R/out; mkdir -p $O
CHK="python3 -B $R/v22_checks.py --repo $REPO --commit $SHA"
Q1=content,setting,voice,packrules,pack_check,build_earth,build_packs,balance,perks,pack_stats,pack_balance
Q1=$Q1,pin,build,icons,art,saveload,end_at_choice,saveload_world,saves_note
Q2=timeless; Q3=life_ends,identity_g; Q4=fuzz,markers; Q5=lines_tied
QUICK=$Q1,$Q2,$Q3,$Q4,$Q5
ENGA=t_steps,identity1
ENGB1=death,child_deaths,satisf,accept; ENGB2=chance,season,exits,inertia,goals; ENGB3=s5_lines,s5_money
ENGB=$ENGB1,$ENGB2,$ENGB3
MECH=s1_parts,s1_counts,s1_fair,s3_rep,s3_caught,s4_odd,s4_convert,s6_felt
LIVES8=lean41,lean42,lean43,lean44,nopack41,nopack42,nopack43,nopack44,lean
LIVES=$LIVES8,pie,pie41   # pie reads the npz in the run's own work folder (no proof): `final` carries it, the rest reused
CARRY_READS="chroma-engine chroma-library chroma-packs"   # what the engine-only jobs read (the rarity files aside)
F9_TABLES="f9_parents f9_partners f9_homes f9_work f9_illness f9_deaths f9_means f14_settle f17_deeds f19_mind"
LOOKBASE=${LOOKBASE:-release/v22.4.1}   # the published page
LOOK="chroma-game/prototype/web/src/look.css chroma-game/prototype/web/src/look.js chroma-game/prototype/web/src/clarity.css
 chroma-game/prototype/web/src/clarity.js chroma-game/prototype/web/src/build.py
 chroma-game/tools/webdir.py chroma-art/game/lights.json chroma-art/game/pics/portrait-* chroma-look/tools"
tree() { [ -d $X/tree ] && return 0; mkdir -p $X/tree && git -C $REPO archive $SHA | tar -x -C $X/tree; }   # the commit's files
moved() { git -C $REPO diff --name-only $1 $2 -- $CARRY_READS | grep -v -e '/rarity\.json$' -e '/rarity\.py$'; }
need_refit() { [ -n "$REFIT" ] || { echo "REFIT=<the refit commit> is needed for $1"; exit 2; }
  local m; m=$(moved $REFIT $SHA)
  [ -z "$m" ] || { echo "NOT CARRIED: the engine, Library or packs changed between ${REFIT:0:12} and ${SHA:0:12}:"; echo "$m" | head
                   echo "run the refit jobs (f9a f9b f8a f8b f8c g4 rar1-5) on ${SHA:0:12} itself"; exit 1; }; }
CARRY_NOTE() { echo "lives run on the refit ${REFIT:0:12}; nothing they read (${CARRY_READS// /, }) changed since but the rarity files"; }
b7() { rm -rf $X/b7; mkdir -p $X; $CHK --only build --no-reuse --keep --work $X/b7 > $X/b7.log 2>&1   # a reused build leaves no folder
  [ -f $X/b7/w/build/BUILD.md ] || { echo "STOP: no build in $X/b7/w/build (see $X/b7.log)"; return 1; }
  bash $R/short-v22.1/b7.sh $1 2 $X/b7/w/build; }
f8dir() { echo $O/roll8_${1:0:7}_$2; }
f15p() { tree; local o=$O/f15_${SHA:0:7}; mkdir -p $X   # a part of check_f15's lives; f15m judges the folder once all are in
  python3 -B $R/check_f15.py run --repo $X/tree --commit $SHA --seeds $1 --far $2 --plain $3 --out $o --no-record > $X/f15.log 2>&1
  local n; n=$(sed -n 's/^\([0-9]*\) lives, .*/\1/p' $X/f15.log | head -1)
  if [ -n "$n" ] && grep -q "^$n lives done" $X/f15.log && ! grep -q 'STOP' $X/f15.log; then
    echo "F15 PART done: $n lives (--seeds $1 --far $2 --plain $3) into $o; $(ls $o/life_*.json | wc -l) in all (f15m judges)"
  else tail -5 $X/f15.log; echo "F15 PART FAILED (see $X/f15.log)"; return 1; fi; }
roll1() { need_refit $1; tree   # one of K9's and K18's roll rows on the final commit
  local ds=$(f8dir $REFIT 41-44),$(f8dir $REFIT 45-48),$(f8dir $REFIT 49-52) o=$O/roll_${SHA:0:7} c=$1 v
  if [ $c = f7_roll ]; then python3 -B $R/check_roll.py f7_roll --repo $X/tree --commit $SHA --as-is --jobs 4 --out $o/f7_roll; return; fi
  python3 -B $R/check_roll.py $c --repo $X/tree --commit $SHA $([ $c = f8_after ] && echo --seeds 41-52) --as-is --jobs 4 \
    --engine-from $ds --out $o/$c --no-record   # engine lives carried from the refit's f8a-c folders: recorded with that note
  v=$(sed -n "s/^$c: \(PASS\|FAIL\).*/\1/p" $o/$c/roll_$c.txt | tail -1)
  python3 -B $R/results.py add $c ${v:-FAIL} ${o#$F/}/$c/roll_$c.txt "$([ $c = f8_after ] && echo "K9, seeds 41-52, 300 lives" \
    || echo "K18, engine seeds 41-44 x 300, played 1-6x1-4 on ${SHA:0:12}"), as is; engine $(CARRY_NOTE)"; }
g4() { local E=$X/g4; rm -rf $E; mkdir -p $E
  git -C $REPO archive $SHA chroma-engine/v22-speedpass chroma-library chroma-packs | tar -x -C $E || return 1
  sed -i 's/^AGE_FIT = True /AGE_FIT = False/' $E/chroma-engine/v22-speedpass/batch.py
  grep -q '^AGE_FIT = False' $E/chroma-engine/v22-speedpass/batch.py || { echo "STOP: no AGE_FIT = True line in batch.py"; return 1; }
  local pnew; pnew=$(cd $E/chroma-engine/v22-speedpass && python3 -B - <<'PY'
import sys, json, importlib.util
sys.path.insert(0, ".")
sp = importlib.util.spec_from_file_location("engine_g4", "engine.py"); E = importlib.util.module_from_spec(sp); sp.loader.exec_module(E)
miss = [k for k in E.V225 if k not in E.UPD_OFF]
if miss:
    sys.exit("STOP: V225 keys not in UPD_OFF: " + ", ".join(miss))
print(json.dumps({k: E.UPD_OFF[k] for k in E.V225}))
PY
) || { echo "$pnew"; return 1; }
  echo "g4: every V225 key at UPD_OFF, batch.AGE_FIT off, against the live engine (v22.4.1)"
  PNEW="$pnew" NEW=$E/chroma-engine/v22-speedpass LIB=$E/chroma-library PACKS=$E/chroma-packs COMMIT=$SHA bash $R/same-lives.sh $1; }
look() { git -C $REPO fetch -q origin "+refs/heads/$LOOKBASE:refs/remotes/origin/$LOOKBASE" || return 2
  local b=$(git -C $REPO rev-parse origin/$LOOKBASE) o=$O/look_same_$(date -u +%Y%m%d-%H%M%S).txt
  local d=$(git -C $REPO diff --name-only $b $SHA -- $LOOK)
  { echo "v22.5 K26 look_same: the page layer of ${SHA:0:12} against $LOOKBASE (${b:0:12}): $LOOK" | tr -s ' \n' ' '; echo
    [ -z "$d" ] && echo "ok   every page-layer file equal" || { echo "differ (each must be a v22.5 change the bar names):"; echo "$d"; }; } > $o; cat $o
  python3 -B $R/results.py add look_same $([ -z "$d" ] && echo PASS || echo FAIL) $o "page layer against $LOOKBASE ${b:0:12}"
  SHA=$SHA BASE=$LOOKBASE bash $R/short-v22.2.1/run.sh page; }
carry_final() {   # the refit's hand rows written again for the final commit, with the evidence
  need_refit final
  local c=$O/carry_${SHA:0:7}.txt
  { echo "v22.5 carry: refit ${REFIT:0:12} -> final ${SHA:0:12}; $(CARRY_NOTE)"
    echo "files that differ under $CARRY_READS: $(git -C $REPO diff --name-only $REFIT $SHA -- $CARRY_READS | paste -sd' ')"; } > $c
  python3 -B - "$R" "$REFIT" "$SHA" "$(CARRY_NOTE)" speedpass_s41 speedpass_sweepA speedpass_sweepB pie pie41 f4_age f6_dreams \
    >> $c <<'PY'
import sys
R, refit, sha, why, ids = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
sys.path.insert(0, R)
import results
last = {}
for r in results.read():
    if (r.get("candidate") or {}).get("commit") == refit and r["check"] in ids:
        last[r["check"]] = r
for i in ids:
    r = last.get(i)
    if r and r["result"] == "PASS":
        results.add(i, "PASS", r.get("report", ""), why + ": " + r.get("note", ""), candidate={"commit": sha})
        print("carried", i, "PASS from", r.get("report", ""))
    else:
        print("NOT CARRIED", i, "(no PASS on the refit: run its refit job on the final commit)")
PY
  local d=$O/f9_${REFIT:0:7}
  if [ $(ls $d/seed*.json 2>/dev/null | wc -l) = 12 ]; then
    python3 -B $R/check_f9.py judge $d --commit $SHA --no-record > /dev/null
    for t in $F9_TABLES; do
      v=$(sed -n "s/^$t: \(PASS\|MISS\).*/\1/p" $d/f9_report.txt | head -1)
      [ -n "$v" ] || { echo "NOT CARRIED $t (no line in $d/f9_report.txt)" >> $c; continue; }
      python3 -B $R/results.py add $t $([ $v = PASS ] && echo PASS || echo FAIL) ${d#$F/}/f9_report.txt "$(CARRY_NOTE) (check_f9 seeds 41-52)"
      echo "carried $t $v" >> $c
    done
  else echo "NOT CARRIED f9 tables: $d holds $(ls $d/seed*.json 2>/dev/null | wc -l) of 12 seeds" >> $c; fi
  local t=$(ls -t $O/rarity_rebuild_*_world.json 2>/dev/null | head -1) rep=$O/rarity_w_$(date -u +%Y%m%d-%H%M%S).txt
  if [ -n "$t" ] && [ "$(cut -d' ' -f1 $t.from)" = "$REFIT" ]; then
    ce=$(git -C $REPO show $SHA:chroma-engine/v22-speedpass/rarity.json | cmp -s - $t && echo same || echo DIFFERENT)
    cg=$(git -C $REPO show $SHA:chroma-game/prototype/rarity.json | cmp -s - $t && echo same || echo DIFFERENT)
    { echo "v22.5 K25 rarity_w on ${SHA:0:12}: the table rebuilt with the world on from the refit ${REFIT:0:12} ($t, md5"
      echo "$(md5sum < $t | cut -c1-12)); the engine's rarity.json: $ce; the game's rarity.json: $cg; $(CARRY_NOTE)"
      [ $ce = same ] && [ $cg = same ] && echo "RARITY_W: PASS" || echo "RARITY_W: FAIL"; } > $rep
    python3 -B $R/results.py add rarity_w $([ $ce = same ] && [ $cg = same ] && echo PASS || echo FAIL) ${rep#$F/} \
      "rebuilt on the refit ${REFIT:0:12} (world on, 200 x 20); engine table $ce, game table $cg"
    echo "rarity_w: engine $ce, game $cg ($rep)" >> $c
  else echo "NOT CARRIED rarity_w: no rebuilt world table from ${REFIT:0:12} (run rar1-5 and rarm on it)" >> $c; fi
  cat $c; }
echo "v22.5 ${1:-} on $SHA$([ -n "$REFIT" ] && echo " (refit $REFIT)")"
case "${1:-}" in
  rar[1-5]) n=${1#rar}; a=$((97 + 4 * n)); SHA=$SHA PART=$a-$((a + 3)) REPO=$REPO bash $R/short-v22.4/rarity_w.sh ;;
  rarm) SHA=$SHA PART=merge REPO=$REPO bash $R/short-v22.4/rarity_w.sh
     t=$(ls -t $O/rarity_rebuild_*_world.json | head -1)
     echo "REBUILT on ${SHA:0:12}: $t (md5 $(md5sum < $t | cut -c1-12)); the Engine commits it as chroma-engine/v22-speedpass/rarity.json and the Game re-pins (its compare above fails until then)" ;;
  f9[a-f]) tree; a=$((41 + 2 * ($(printf %d "'${1:2:1}") - 97))); s=$a-$((a + 1))   # f9a 41-42 .. f9f 51-52
     python3 -B $R/check_f9.py run --repo $X/tree --commit $SHA --seeds $s --out $O/f9_${SHA:0:7} --no-record ;;
  f8a|f8b|f8c) tree; s=$(case $1 in f8a) echo 41-44;; f8b) echo 45-48;; f8c) echo 49-52;; esac)
     python3 -B $R/check_roll.py f8_after --repo $X/tree --commit $SHA --seeds $s --as-is --jobs 4 --no-record --out $(f8dir $SHA $s) ;;
  engA) $CHK --only $ENGA ;;
  engB) $CHK --only $ENGB ;;
  engB1) $CHK --only $ENGB1 ;;
  engB2) $CHK --only $ENGB2 ;;
  engB3) $CHK --only $ENGB3 ;;
  mech) $CHK --only $MECH --keep --work $K/mech ;;
  s7) $CHK --only s7_lead ;;
  c26a) $CHK --only c26_choice --keep --work $K/c26 ;;
  c26b) $CHK --only c26_world --keep --work $K/c26 ;;
  lives) $CHK --only $LIVES --keep --work $K/lives ;;
  g4) g4 1 ;;
  g4s) g4 1s ;;
  g4a) g4 1A ;;
  g4b) g4 1B ;;
  fit4) tree; python3 -B $R/check_fit.py f4_age --repo $X/tree --commit $SHA ;;
  fit6) tree; python3 -B $R/check_fit.py f6_dreams --repo $X/tree --commit $SHA ;;
  quick) $CHK --only $QUICK ;;
  q[1-5]) v=Q${1#q}; $CHK --only ${!v} ;;
  game) $CHK --only book_check,kin; $CHK --only @steered; $CHK --only own_even ;;
  gameA) $CHK --only book_check,kin ;;
  gameB) $CHK --only @steered ;;
  gameC) $CHK --only own_even ;;
  pr30) SHA=$SHA N=30 REPO=$REPO bash $R/short-v22.4/push_rare_n.sh ;;
  pr30a) SHA=$SHA N=30 PART=1-10 REPO=$REPO bash $R/short-v22.4/push_rare_n.sh ;;
  pr30b) SHA=$SHA N=30 PART=11-20 REPO=$REPO bash $R/short-v22.4/push_rare_n.sh ;;
  pr30c) SHA=$SHA N=30 PART=21-30 REPO=$REPO bash $R/short-v22.4/push_rare_n.sh ;;
  pr30m) SHA=$SHA N=30 PART=merge REPO=$REPO bash $R/short-v22.4/push_rare_n.sh ;;
  b7AB|b7CD) b7 ${1:2:1},${1:3:1} ;;
  b7A|b7B|b7C|b7D) b7 ${1#b7} ;;
  roll) roll1 f8_after; roll1 f10_once; roll1 f7_roll ;;
  rollA) roll1 f8_after ;;
  rollB) roll1 f10_once ;;
  rollC) roll1 f7_roll ;;
  fit) tree; python3 -B $R/check_fit.py all --repo $X/tree --commit $SHA; python3 -B $R/check_f15.py run --repo $X/tree --commit $SHA ;;
  fitk) tree; python3 -B $R/check_fit.py all --repo $X/tree --commit $SHA ;;
  f15) tree; python3 -B $R/check_f15.py run --repo $X/tree --commit $SHA ;;
  fit12) tree; python3 -B $R/check_fit.py f12_start --repo $X/tree --commit $SHA ;;
  f15a) f15p 1-20 1-0 1-8 ;;
  f15b) f15p 21-40 1-0 1-0 ;;
  f15c) f15p 1-0 1-30 1-0 ;;
  f15d) f15p 1-0 31-60 1-0 ;;
  f15m) python3 -B $R/check_f15.py judge $O/f15_${SHA:0:7} --commit $SHA ;;
  page) look ;;
  final) $CHK --only $ENGA,$ENGB; $CHK --only $MECH --keep --work $K/mech; $CHK --only s7_lead
     $CHK --only c26_choice,c26_world --keep --work $K/c26; $CHK --only $LIVES8 --keep --work $K/lives; carry_final ;;
  *) sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2 ;;
esac
