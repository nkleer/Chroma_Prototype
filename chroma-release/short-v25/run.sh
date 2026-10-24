#!/bin/bash
# v25 integrated assessment (records/v25/jobs.md, checks.md, evaluation.md): v24's wave runner (short-v24/run.sh, its
# jobs and readers unchanged) with three v25 changes:
#   - every job first proves its machine plays Release's lives byte for byte: out/v25/cloud_lib.sh's four probes on E
#     (about 3 minutes; NOPROBE=1 skips them in Release's own container). A machine that differs stops with STOP.
#   - the engine-reading jobs run the shipped set: CHROMA_SHIP=v25 with out/v25/ship_hook on PYTHONPATH lays the v25
#     switches of engine.SHIP_V25 over DEFAULT and sets SHIP_V25_BATCH on batch (records/v25/scope.md, "The shipped
#     settings"), with v22_checks --no-reuse; the game's jobs play the game as committed (it sets the shipped set itself,
#     checked by ship_game). The hook's log is printed at the end of the job.
#   - K3 (t_steps) and K4 (same-lives) run on Emren's PC; LA (A2, F2) is out/v25/la_ship.sh; the rarity table is
#     out/v25/rarity_part.sh (rar1 .. rar5) and rarm here.
# E = the Engine's freeze, feature/v25 225679d (engine.SHIP_V25 in code). G = Gamification's switch-on commit with the
# rarity table and the golden: the frozen candidate.
#   SHA=<E> bash /mnt/project-files/chroma-release/short-v25/run.sh <E job>
#   SHA=<G> REFIT=<E> bash /mnt/project-files/chroma-release/short-v25/run.sh <G job>
#
# v24's jobs, as they run here:
# On E (engine-only; they carry to G when the engine, Library, packs and chroma-env differ only in the rarity files):
#   rar1 .. rar5   the world-on rarity rebuild (K25), seeds 101-104, 105-108, 109-112, 113-116, 117-120 a machine
#   rarm           its merge, once the five parts are in: the rebuilt table, which the Engine commits as
#                  chroma-engine/v22-speedpass/rarity.json and the Game as chroma-game/prototype/rarity.json
#   f9a .. f9f     check_f9 seeds 41-42, 43-44, .. 51-52 into out/f9_<E7> (K6 to K13, K15, K16; judged in `final`)
#   f9all          the same twelve seeds in one call, F9JOBS (default 3) at once, on one machine (v25: Release's container)
#   f8a f8b f8c    check_roll f8_after seeds 41-44, 45-48 and 49-52 into out/roll8_<E7>_<seeds> (K9; judged in rollA)
#   engA | engA1 engA2   K3: t_steps (every row, T_JOBS up to 4) and identity1 | t_steps alone | identity1 alone
#   engB | engB1 engB2 engB3   K5's engine rows and S5: death, child_deaths, satisf, accept | chance, season, exits,
#                  inertia, goals | s5_lines, s5_money
#   mech           S1, S3, S4 and S6 (K19)
#   s7             s7_lead (K19)
#   c26a c26b      c26_choice and c26_world (K20)
#   lives          lean41-44, nopack41-44, lean, pie and pie41 in one call (K5)
#   k4p1 .. k4p4   K4: same-lives parts 1 to 4 with every v24 switch off against release/v23.2 (out/v24/k4/k4.sh)
#   fit4 fit6      check_fit f4_age and f6_dreams (K17; engine-only, carried)
#   heng           A2, A4: lives left alone, seeds 41-44 side by side (out/v24/heights/run.sh engine; judged in `hjudge`)
#   wa | waoff     WA1 to WA4, WA7 to WA9: out/v24/wa/wa_check.py run, seeds 41-44 side by side, 400 lives x 100 years,
#                  the commit's defaults (phase 2 as set there) | the same with wa_notice off (WA4's other side), into
#                  out/v24/wa/<sha7>/on/ | off/ (about 20 to 60 min a seed, one core a seed)
#   wam            WA1 to WA4, WA7 to WA9 judged, once wa and waoff are in (WA5 is K4's engine side, WA6 the text rows)
# On G:
#   quick | q1 .. q5   K1, K2, K22's quick game rows, K23's old saves and K28 lines_tied: the fast rows | timeless |
#                  life_ends, identity_g | fuzz, markers | lines_tied
#   game | gameA gameB gameC   book_check and kin | the steered rows | own_even (K21, K22)
#   pr30 | pr30a pr30b pr30c pr30m   push_rare on 30 seeds (K21): one machine, or seeds 1-10, 11-20, 21-30, then merge
#   b7A b7B b7C b7D | b7AB b7CD   the browser drivers (K24; one per machine: they serve on port 8140)
#   roll | rollA rollB rollC   K9's f8_after from the f8a-c folders (carried) | f10_once | f7_roll (K18), --as-is
#   fit | fitk f15 check_fit all (K17), then check_f15 (K14); or each on its own machine
#   fit12          check_fit f12_start (K17; the game)
#   f15a .. f15d f15m   check_f15 in four parts into out/f15_<G7>, then the judge that records f15_lean (K14)
#   page           the page layer against release/v23.2, the fit probes and the tours (K26)
#   needs          N1 to N3: out/v24/needs/needs_check.py run, seeds 41-44 side by side, 400 lives x 100 years, into
#                  out/v24/needs/<sha7>/ (about 25 to 45 min). On G, not E: N3 reads the Game's panel too (game_because.py
#                  reading the engine's setback cause, Emren's card 10-20 "Cause now, world fit v25")
#   nbase          needs on the base (SHA=34721bb), without the ship hook: for a machine that compares both sides itself
#   ndm            N1 to N3 judged against the base (NBASE, default 34721bb: release/v23.2, kept), once `needs` is in
#   fp             FP1 to FP3: the owners' footprint checks and fp_marks.py (out/v24/fp/fp.sh; a minute)
#   hp_none hp_let hp_reader hp_aims hp_oracle   the played heights lives, one policy a machine (out/v24/heights/run.sh)
#   hp_aims2       A1's seeds 7 to 12 (reader-aims into out/v24/heights/wide_<sha7>/): A1 is read on 48 lives in v24, read
#                  only (Emren typed "Bar to v25", 10-20 08:37 UTC; records/v24/scope.md Rulings)
#   hp_boldoff     A5: reader-aims with Bold ways off (TAG boldoff), when the commit ships Bold ways on
#   pb             PB, v25 SK1 and SK2: always pushing Blue (impact.py steer:U), presets 1 to 4 x seeds 1 to 6, on G and
#                  on the played base 7a8cac6 (SHA=7a8cac6); read as What shapes a life's tools/directed.py reads
#   hjudge         A1 to A5 from the hp_* folders and heng's (out/v24/heights/heights_v24.py), once those are in
#   st1            ST1: out/v24/st1/st1_check.py, colours R and U, presets 1-4, seeds 1-3 (about 30 minutes)
#   hover          H1: out/v24/hover/hover_check.py, presets 1-4, seeds 1-3, the reader, scope forecast (about 6 min)
#   q1asks         Q1: test/same_life.py presets 1-6, seed 7, with the asks setting and its parts at the defaults against
#                  the same lives with them off (CHROMA_GAME ask_matter 0, steer_between and talk off), step by step
#                  (out/v24/q1/q1same.py), all but the HUD's life.steer and cp.talk (Emren 10-19 22:01 UTC, "Same play
#                  for the asks check": only the Between-asks buttons and the talk offer may differ)
#   foot           FP5: the Game's test/foot_check.py, presets 1-4, seeds 1-2 (F2 the after-panel, F3 the six stacks)
#   fp4            FP4 fp_titles and fp_alone_well from hp_let, hp_reader and hp_none's lives (out/v24/fp/fp4.py; FP4RULE
#                  today, Emren's reading of the titles band: "Not above today", card tapped 10-19 21:07 UTC)
#   gv24           the Game's own six v24 checks (arrows, foot, aims, asks, steer_between, talk), seeds 1-2: a report only
#   final          E's rows on G: v22_checks rows again (reused where nothing they read changed), the hand rows carried
#                  (K4's eight speedpass rows, pie and pie41, f4_age and f6_dreams, check_f9's ten tables, rarity_w)
#                  with the evidence in out/carry_<G7>.txt; fp_ties from f9_parents, f9_partners and f9_means; and A0
#                  heights_base, read on v23.1
#   merged         every row's latest line on G (MERGED) written again for M, when M's tree is G's (out/carry_merged_<M7>.txt)
set -u
JOBS=" rar1 rar2 rar3 rar4 rar5 rarm f9all f9a f9b f9c f9d f9e f9f f8a f8b f8c engA engA1 engA2 engB engB1 engB2 engB3 mech s7
 c26a c26b lives k4p1 k4p2 k4p3 k4p4 fit4 fit6 heng quick q1 q2 q3 q4 q5 game gameA gameB gameC pr30 pr30a pr30b pr30c pr30m
 b7A b7B b7C b7D b7AB b7CD roll rollA rollB rollC fit fitk fit12 f15 f15a f15b f15c f15d f15m page fp needs nbase ndm wa waoff wam hover hp_none hp_let
 hp_reader hp_aims hp_aims2 hp_oracle hp_boldoff pb hjudge st1 q1asks foot fp4 gv24 final merged "
[[ "${JOBS//$'\n'/ }" == *" ${1:-none} "* ]] || { sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2; }
F=${CHROMA_PROJECT:-/mnt/project-files}; R=$F/chroma-release; V=$R/out/v24; REPO=${REPO:-/tmp/v25_repo}; X=/tmp/v25_${1:-}; JOB=${1:-}
K=/tmp/v25_keep   # --keep --work folders: the same path on every machine, so `final` reuses E's proofs
[ -n "${SHA:-}" ] || { echo "SHA=<commit> is needed"; exit 2; }
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e "$SHA^{commit}" 2>/dev/null || git -C $REPO fetch -q origin '+refs/heads/*:refs/remotes/origin/*' || exit 2
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
REFIT=${REFIT:-}; [ -n "$REFIT" ] && { REFIT=$(git -C $REPO rev-parse "$REFIT^{commit}") || exit 2; }
MERGED=${MERGED:-}; [ -n "$MERGED" ] && { MERGED=$(git -C $REPO rev-parse "$MERGED^{commit}") || exit 2; }
unset CHROMA_GAME CHROMA_ENGINE   # every job plays the commit's own settings unless it sets its own
export CHROMA_COMMIT=$SHA PW=${PW:-/opt/node22/lib/node_modules/playwright}
if [ -z "${NOPROBE:-}" ]; then ( . $R/out/v25/cloud_lib.sh; probe_here ) || { echo "v25 $JOB: STOP, this machine's lives differ from Release's"; exit 3; }; fi
HOOK_JOBS=" f9all f9a f9b f9c f9d f9e f9f f8a f8b f8c engB engB1 engB2 engB3 mech s7 c26a c26b lives fit4 fit6 fit fitk wa waoff needs final "
SHIPNOTE="the game as committed"
if [[ "$HOOK_JOBS" == *" $JOB "* ]]; then
  export CHROMA_SHIP=v25 PYTHONPATH=$R/out/v25/ship_hook${PYTHONPATH:+:$PYTHONPATH} CHROMA_SHIP_LOG=/tmp/v25_ship_$JOB.log
  rm -f $CHROMA_SHIP_LOG; SHIPNOTE="the shipped set by out/v25/ship_hook"
  trap 'echo "ship_hook: $(wc -l < $CHROMA_SHIP_LOG 2>/dev/null || echo 0) patches in $(cut -d" " -f1 $CHROMA_SHIP_LOG 2>/dev/null | sort -u | wc -l) processes ($CHROMA_SHIP_LOG)"' EXIT
fi
O=$R/out; mkdir -p $O
CHK="python3 -B $R/v22_checks.py --repo $REPO --commit $SHA$([ -n "${CHROMA_SHIP:-}" ] && echo " --no-reuse")"
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
CARRY_READS="chroma-engine chroma-library chroma-packs chroma-env"   # what the engine-only jobs read (the rarity files aside)
CARRIED="speedpass_s41 speedpass_s42 speedpass_s43 speedpass_s44 speedpass_sweepA speedpass_sweepB speedpass_sweepC
 speedpass_sweepD pie pie41 f4_age f6_dreams wa1_forest wa2_tree wa3_standing wa4_noticed
 wa7_known wa8_decisions wa9_kept"
F9_TABLES="f9_parents f9_partners f9_homes f9_work f9_illness f9_deaths f9_means f14_settle f17_deeds f19_mind"
LOOKBASE=${LOOKBASE:-release/v23.2}   # the published page (Version 35)
LOOK="chroma-game/prototype/web/src/look.css chroma-game/prototype/web/src/look.js chroma-game/prototype/web/src/clarity.css
 chroma-game/prototype/web/src/clarity.js chroma-game/prototype/web/src/build.py
 chroma-game/tools/webdir.py chroma-art/game/lights.json chroma-art/game/pics/portrait-* chroma-look/tools"
tree() { [ -d $X/tree ] && [ "$(cat $X/tree.sha 2>/dev/null)" = "$SHA" ] && return 0   # the commit's files, stamped with it
  rm -rf $X/tree $X/tree.sha; mkdir -p $X/tree && git -C $REPO archive $SHA | tar -x -C $X/tree && echo $SHA > $X/tree.sha; }
moved() { local f; git -C $REPO diff --name-only $1 $2 -- $CARRY_READS | grep -v -e '/rarity\.json$' -e '/rarity\.py$' |
  while read -r f; do   # an MD5SUMS whose only changed line is rarity.json's is a rarity file too
    [[ $f == */MD5SUMS ]] && [ -z "$(git -C $REPO diff -U0 $1 $2 -- $f | grep '^[-+][^-+]' | grep -v ' rarity\.json$')" ] && continue
    echo "$f"; done; }
need_refit() { [ -n "$REFIT" ] || { echo "REFIT=<E, the Engine's freeze> is needed for $1"; exit 2; }
  local m; m=$(moved $REFIT $SHA)
  [ -z "$m" ] || { echo "NOT CARRIED: the engine, Library or packs changed between ${REFIT:0:12} and ${SHA:0:12}:"; echo "$m" | head
                   echo "run E's jobs (f9a-f f8a-c k4p1-4 rar1-5 heng ...) on ${SHA:0:12} itself"; exit 1; }; }
CARRY_NOTE() { echo "lives run on E ${REFIT:0:12}; nothing they read (${CARRY_READS// /, }) changed since but the rarity files"; }
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
roll1() { need_refit $1; tree   # one of K9's and K18's roll rows on G
  local ds=$(f8dir $REFIT 41-44),$(f8dir $REFIT 45-48),$(f8dir $REFIT 49-52) o=$O/roll_${SHA:0:7} c=$1 v
  if [ $c = f7_roll ]; then python3 -B $R/check_roll.py f7_roll --repo $X/tree --commit $SHA --as-is --jobs 4 --out $o/f7_roll; return; fi
  python3 -B $R/check_roll.py $c --repo $X/tree --commit $SHA $([ $c = f8_after ] && echo --seeds 41-52) --as-is --jobs 4 \
    --engine-from $ds --out $o/$c --no-record   # engine lives carried from E's f8a-c folders: recorded with that note
  v=$(sed -n "s/^$c: \(PASS\|FAIL\).*/\1/p" $o/$c/roll_$c.txt | tail -1)
  python3 -B $R/results.py add $c ${v:-FAIL} ${o#$F/}/$c/roll_$c.txt "$([ $c = f8_after ] && echo "K9, seeds 41-52, 300 lives" \
    || echo "K18, engine seeds 41-44 x 300, played 1-6x1-4 on ${SHA:0:12}"), as is; engine $(CARRY_NOTE)"; }
hp() { SHA=$SHA REPO=$REPO bash $V/heights/run.sh "$@"; }   # the played heights lives (TAG/GAMESET pass through)
hjudge() { need_refit hjudge
  local o=$V/heights/heights_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt off=""
  [ -d $V/heights/play_${SHA:0:7}_boldoff ] && off="--off boldoff"
  python3 -B $V/heights/heights_v24.py ${SHA:0:7} --engine-dir $V/heights/engine_${REFIT:0:7}_ship $off --out $o > /dev/null || return 1
  cat $o | sed -n '/^A1/,/^$/p'
  local r id
  for r in "A1 heights_skilled" "A2 heights_alone" "A3 reader_lift" "A4 aims_even" "A5 bold_heights"; do
    # the verdict after the row's last ": " (A4's line has it straight after the id); RAN: A1, read only in v24
    id=${r#* }; v=$(sed -n "s/^${r% *} $id:\(.*:\)\{0,1\} \(PASS\|FAIL\|RAN\)\( .*\)\{0,1\}$/\2/p" $o | tail -1)
    [ -n "$v" ] || { echo "$id: not read (see $o)"; continue; }
    python3 -B $R/results.py add $id $v ${o#$F/} "$(sed -n "s/^${r% *} $id: //p" $o | tail -1 | cut -c1-200)$([ $id = heights_alone ] && echo "; engine $(CARRY_NOTE)")"
  done; }
st1() { tree; local g=$X/tree/chroma-game/prototype o=$V/st1/st1_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt rc
  python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$g', root='$X/tree')" || return 2
  python3 -B $V/st1/st1_check.py $g --colors R,U --presets 1,2,3,4 --seeds 1-3 --jobs 4 --tmp $X/st1 --out $o; rc=$?
  [ $rc = 2 ] && return 2
  python3 -B $R/results.py add steer_vs_asks $([ $rc = 0 ] && echo PASS || echo FAIL) ${o#$F/} "$(tail -n 1 $o | cut -c1-200)"; }
q1asks() { tree; local g=$X/tree/chroma-game/prototype p side ok=0 d=$X/q1 o=$V/q1/asks_same_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt
  local OFF='{"ask_matter": 0.0, "steer_between": false, "talk": false}'; [ -n "${Q1OFF:-}" ] && OFF=$Q1OFF
  # Q1DROP: HUD keys left out of both sides (out/v24/q1/q1same.py). Emren, 10-19 22:01 UTC, typed "Same play for the asks
  # check" (card 21:56): every step, age, text, feed and screen value matches but the Between-asks buttons (life.steer) and
  # the talk offer (cp.talk); Q1DROP= alone is byte for byte
  local DROP=${Q1DROP-life.steer,cp.talk}
  python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$g', root='$X/tree')" || return 2
  rm -rf $d; mkdir -p $d $V/q1
  for p in ${Q1P:-1 2 3 4 5 6}; do for side in on off; do
    while [ $(jobs -rp | wc -l) -ge 4 ]; do timeout 2 tail -f /dev/null; done
    ( cd $g && { [ $side = off ] && export CHROMA_GAME="$OFF"; true; } &&
      python3 -B test/same_life.py $p 7 $d/${side}_$p.jsonl > $d/${side}_$p.out 2>&1 ) &
  done; done; wait
  { echo "v24 Q1 asks_same on ${SHA:0:12}: test/same_life.py presets ${Q1P:-1 2 3 4 5 6}, seed 7, the commit's settings against CHROMA_GAME $OFF"
    for p in ${Q1P:-1 2 3 4 5 6}; do
      python3 -B $V/q1/q1same.py $d/on_$p.jsonl $d/off_$p.jsonl $p "$DROP" "$(tail -1 $d/on_$p.out 2>/dev/null)" || ok=1
    done
    echo "Q1 asks_same: $([ $ok = 0 ] && echo PASS || echo FAIL)"; } > $o; cat $o
  python3 -B $R/results.py add asks_same $([ $ok = 0 ] && echo PASS || echo FAIL) ${o#$F/} \
    "same_life.py presets 1-6 seed 7: the defaults against ask_matter 0, steer_between and talk off, $([ -n "$DROP" ] && echo "HUD $DROP left out (Emren: Same play)" || echo "byte for byte")"; }
look() { git -C $REPO fetch -q origin "+refs/heads/$LOOKBASE:refs/remotes/origin/$LOOKBASE" || return 2
  local b=$(git -C $REPO rev-parse origin/$LOOKBASE) o=$O/look_next_$(date -u +%Y%m%d-%H%M%S).txt
  local d=$(git -C $REPO diff --name-only $b $SHA -- $LOOK)
  { echo "v24 K26 look_next: the page layer of ${SHA:0:12} against $LOOKBASE (${b:0:12}): $LOOK" | tr -s ' \n' ' '; echo
    [ -z "$d" ] && echo "ok   every page-layer file equal" || { echo "differ (each must be a v24 change the bar names; Release reads them):"; echo "$d"; }; } > $o; cat $o
  python3 -B $R/results.py add look_next $([ -z "$d" ] && echo PASS || echo RAN) ${o#$F/} "page layer against $LOOKBASE ${b:0:12}$([ -n "$d" ] && echo "; $(echo "$d" | wc -l) files differ, each to be read")"
  SHA=$SHA BASE=$LOOKBASE PAGE_ONLY=${PAGE_ONLY:-} bash $R/short-v22.2.1/run.sh page; }   # (set -u there; empty = every page row)
carry_final() {   # E's hand rows written again for G, with the evidence
  need_refit final
  local c=$O/carry_${SHA:0:7}.txt
  { echo "v24 carry: E ${REFIT:0:12} -> G ${SHA:0:12}; $(CARRY_NOTE)"
    echo "files that differ under $CARRY_READS: $(git -C $REPO diff --name-only $REFIT $SHA -- $CARRY_READS | paste -sd' ')"; } > $c
  python3 -B - "$R" "$REFIT" "$SHA" "$(CARRY_NOTE)" $CARRIED >> $c <<'PY'
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
        print("NOT CARRIED", i, "(no PASS on E: run its E job on G itself)")
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
    { echo "v24 K25 rarity_w on ${SHA:0:12}: the table rebuilt with the world on from E ${REFIT:0:12} ($t, md5"
      echo "$(md5sum < $t | cut -c1-12)); the engine's rarity.json: $ce; the game's rarity.json: $cg; $(CARRY_NOTE)"
      [ $ce = same ] && [ $cg = same ] && echo "RARITY_W: PASS" || echo "RARITY_W: FAIL"; } > $rep
    python3 -B $R/results.py add rarity_w $([ $ce = same ] && [ $cg = same ] && echo PASS || echo FAIL) ${rep#$F/} \
      "rebuilt on E ${REFIT:0:12} (world on, 200 x 20); engine table $ce, game table $cg"
    echo "rarity_w: engine $ce, game $cg ($rep)" >> $c
  else echo "NOT CARRIED rarity_w: no rebuilt world table from ${REFIT:0:12} (run rar1-5 and rarm on it)" >> $c; fi
  local ft=PASS t9
  for t9 in f9_parents f9_partners f9_means; do grep -q "^carried $t9 PASS" $c || ft=FAIL; done
  python3 -B $R/results.py add fp_ties $ft ${c#$F/} "FP4 ties and belonging: f9_parents, f9_partners and f9_means on E with footprints on ($(grep -E '^carried f9_(parents|partners|means) ' $c | awk '{print $2, $3}' | paste -sd' '))"
  echo "fp_ties: $ft" >> $c
  python3 -B $R/results.py add heights_base RAN out/heights/baseline_20261019-1325.txt \
    "A0, read on v23.1 e69b3bf (1,600 lives left alone and 120 played), 10-19 13:25 UTC: the baseline every heights row reads"
  echo "heights_base: RAN, the baseline on v23.1" >> $c
  cat $c; }
foot() { tree; local g=$X/tree/chroma-game/prototype o=$V/fp/foot_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt rc n
  python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$g', root='$X/tree')" || return 2
  ( cd $g && python3 -B test/foot_check.py --presets 1,2,3,4 --seeds 1-2 --jobs 4 ) > $o 2>&1; rc=$?
  n=$(sed -n 's/^F2+F3  problems: \([0-9]*\).*/\1/p' $o | tail -1); cat $o | tail -n 12
  local v=$([ $rc = 0 ] && [ "${n:-x}" = 0 ] && echo PASS || echo FAIL)
  python3 -B $R/results.py add fp_panel $v ${o#$F/} "test/foot_check.py F2 (at most one footprint line per kind after a pick), presets 1-4 seeds 1-2, exit $rc"
  python3 -B $R/results.py add fp_stacks $v ${o#$F/} "test/foot_check.py F3 (six stacks in the HUD and the Book, counts add up), presets 1-4 seeds 1-2, exit $rc"; }
fp4() { FP4RULE=${FP4RULE:-today}   # Emren's card, 10-19 21:07 UTC: "Not above today" (records/v24/scope.md, Rulings)
  tree; mkdir -p $X/base && git -C $REPO show e69b3bfefb0934b1b034cd93e384211837f22825:chroma-library/earth_perks_titles.py > $X/base/earth_perks_titles.py || return 2
  local o=$V/fp/fp4_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt
  python3 -B $V/fp/fp4.py ${SHA:0:7} --rule $FP4RULE --lib $X/tree/chroma-library --base-lib $X/base --out $o
  local id; for id in fp_titles fp_alone_well; do
    v=$(sed -n "s/^FP4 $id: .*\(PASS\|FAIL\).*/\1/p" $o | tail -1)
    python3 -B $R/results.py add $id ${v:-FAIL} ${o#$F/} "$(sed -n "s/^FP4 $id: //p" $o | cut -c1-200)"; done; }
gv24() { tree; local g=$X/tree/chroma-game/prototype o=$V/gv24_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt t
  python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$g', root='$X/tree')" || return 2
  for t in arrows foot aims asks steer_between talk; do
    { echo "== test/${t}_check.py"; ( cd $g && python3 -B test/${t}_check.py --presets 1,2,3,4 --seeds 1-2 --jobs 4 ); echo "exit $?"; } >> $o 2>&1
  done; grep -E '^(==|exit|[A-Z][0-9])' $o; echo "report $o"; }
needs() { tree; local o=$V/needs/${SHA:0:7} n s; mkdir -p $o
  for s in 41 42 43 44; do
    [ -f $o/s$s.json ] && { echo "seed $s kept: $o/s$s.json"; continue; }
    ( OMP_NUM_THREADS=1 python3 -B $V/needs/needs_check.py run $X/tree $s 400 100 $X/s$s.json > $X/s$s.log 2>&1 && cp $X/s$s.json $X/s$s.log $o/ ) &
  done; wait
  n=$(ls $o/s*.json 2>/dev/null | wc -l); for s in 41 42 43 44; do tail -n 1 $X/s$s.log 2>/dev/null; done
  echo "needs on ${SHA:0:12}: $n of 4 seeds in $o"; [ $n = 4 ]; }
ndm() { local d=$V/needs/${SHA:0:7} b=$V/needs/${NBASE:-34721bb} o=$V/needs/needs_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt r v
  for x in $d $b; do [ $(ls $x/s*.json 2>/dev/null | wc -l) = 4 ] || { echo "STOP: $x holds $(ls $x/s*.json 2>/dev/null | wc -l) of 4 seeds"; return 1; }; done
  python3 -B $V/needs/needs_check.py judge $d --base $b --out $o > /dev/null || return 1
  for r in "N1 needs_age" "N2 needs_alone" "N3 needs_setbacks"; do
    v=$(sed -n "s/^$r \+\(PASS\|MISS\) .*/\1/p" $o | head -1)
    python3 -B $R/results.py add ${r#* } $([ "$v" = PASS ] && echo PASS || echo FAIL) ${o#$F/} "$(sed -n "s/^$r \+//p" $o | head -1 | cut -c1-220)"
  done; grep -E '^N[123] ' $o | cut -c1-300; }
wa() { tree; local side=$([ $JOB = waoff ] && echo off || echo on) s n; local o=$V/wa/${SHA:0:7}/$side; mkdir -p $o
  for s in 41 42 43 44; do
    [ -f $o/wa$s.json ] && { echo "seed $s kept: $o/wa$s.json"; continue; }
    ( OMP_NUM_THREADS=1 python3 -B $V/wa/wa_check.py run $X/tree $s 400 100 $X/wa$s.json $([ $side = off ] && echo --notice-off) \
        > $X/wa$s.log 2>&1 && cp $X/wa$s.json $X/wa$s.log $o/ ) &
  done; wait
  n=$(ls $o/wa*.json 2>/dev/null | wc -l); for s in 41 42 43 44; do tail -n 1 $X/wa$s.log 2>/dev/null; done
  echo "$JOB on ${SHA:0:12}: $n of 4 seeds in $o"; [ $n = 4 ]; }
wam() { local d=$V/wa/${SHA:0:7} o=$V/wa/wa_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt r id v L x
  for x in on off; do [ $(ls $d/$x/wa*.json 2>/dev/null | wc -l) = 4 ] || { echo "STOP: $d/$x holds $(ls $d/$x/wa*.json 2>/dev/null | wc -l) of 4 seeds"; return 1; }; done
  python3 -B $V/wa/wa_check.py judge $d/on --off $d/off --out $o > /dev/null || return 1
  for r in "WA1 wa1_forest" "WA2 wa2_tree" "WA3 wa3_standing" "WA4 wa4_noticed" "WA7 wa7_known" "WA8 wa8_decisions" "WA9 wa9_kept"; do
    id=${r#* }; L=$(grep "^${r% *} " $o)   # PASS only when every line of the row passes: a MISS or a NOT READ fails it
    v=FAIL; [ -n "$L" ] && ! echo "$L" | grep -v -q ' PASS ' && v=PASS
    python3 -B $R/results.py add $id $v ${o#$F/} "$(echo "$L" | sed -e 's/^WA[0-9] //' -e 's/   */ /g' | cut -c1-90 | paste -sd';' - | cut -c1-220)"
  done; grep -E '^WA[0-9]' $o | cut -c1-220; }
hover() { tree; local g=$X/tree/chroma-game/prototype o=$V/hover/hover_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt rc
  python3 -B -c "import sys; sys.path.insert(0, '$R'); import gamepin; gamepin.fill('$g', root='$X/tree')" || return 2
  python3 -B $V/hover/hover_check.py $g --presets 1,2,3,4 --seeds 1-3 --jobs 4 --keep $X/hover --out $o; rc=$?
  python3 -B $R/results.py add hover_sizes $([ $rc = 0 ] && grep -q '^H1: PASS' $o && echo PASS || echo FAIL) ${o#$F/} \
    "$(grep -E '^H1(a|c picks)' $o | cut -c1-110 | paste -sd';' -)"; }
merged() {   # G's rows for M: only when M's tree is G's
  [ -n "$MERGED" ] || { echo "MERGED=<G, the branch head that merged> is needed"; exit 2; }
  local c=$O/carry_merged_${SHA:0:7}.txt
  git -C $REPO diff --quiet $MERGED $SHA || { echo "NOT CARRIED: the trees of ${MERGED:0:12} and ${SHA:0:12} differ:"
    git -C $REPO diff --name-only $MERGED $SHA | head; exit 1; }
  { echo "v24 merged carry: G ${MERGED:0:12} -> M ${SHA:0:12}; the two trees are identical (git diff --quiet)"
    python3 -B - "$R" "$MERGED" "$SHA" <<'PY'
import sys
R, g, m = sys.argv[1:4]
sys.path.insert(0, R)
import results
last = {}
for r in results.read():
    if (r.get("candidate") or {}).get("commit") == g:
        last[r["check"]] = r
for i, r in sorted(last.items()):
    results.add(i, r["result"], r.get("report", ""), f"carried from G {g[:12]} (the same tree): " + r.get("note", ""),
                candidate={"commit": m})
    print("carried", i, r["result"], "from", r.get("report", ""))
PY
  } > $c; cat $c; }
echo "v25 ${1:-} on $SHA$([ -n "$REFIT" ] && echo " (E $REFIT)")$([ -n "$MERGED" ] && echo " (G $MERGED)")"
case "${1:-}" in
  rar[1-5]) n=${1#rar}; a=$((97 + 4 * n)); SHA=$SHA CHUNK=$a,$((a + 1)),$((a + 2)),$((a + 3)) bash $R/out/v25/rarity_part.sh ;;
  rarm) tree; d=$R/out/v25/rarity_${SHA:0:7}; SHIP=v25 OUT=$d/rarity.json python3 -B $X/tree/chroma-engine/tools/rarity_build.py 200 20 --merge $d/parts \
     && echo "REBUILT on ${SHA:0:12} (SHIP=v25, 200 x 20): $d/rarity.json md5 $(md5sum < $d/rarity.json | cut -c1-12)" ;;
  engA|engA1|engA2|k4p[1-4]) echo "v25: K3 t_steps and K4 same-lives run on Emren's PC (records/v25/evaluation.md section 5)"; exit 2 ;;
  heng) echo "v25: LA is out/v25/la_ship.sh (SEEDS=...)"; exit 2 ;;
  f9[a-f]) tree; a=$((41 + 2 * ($(printf %d "'${1:2:1}") - 97))); s=$a-$((a + 1))   # f9a 41-42 .. f9f 51-52
     python3 -B $R/check_f9.py run --repo $X/tree --commit $SHA --seeds $s --out $O/f9_${SHA:0:7} --no-record ;;
  f9all) tree; python3 -B $R/check_f9.py run --repo $X/tree --commit $SHA --seeds ${F9SEEDS:-41-52} --jobs ${F9JOBS:-2} \
     --out ${F9OUT:-$O/f9_${SHA:0:7}} --no-record ;;   # all six f9 parts on one machine, F9JOBS seeds at once (v25 seeds pass 4.7 GB: 3 at once ran out on 16 GB, 10-24)
  f8a|f8b|f8c) tree; s=$(case $1 in f8a) echo 41-44;; f8b) echo 45-48;; f8c) echo 49-52;; esac)
     python3 -B $R/check_roll.py f8_after --repo $X/tree --commit $SHA --seeds $s --as-is --jobs 4 --no-record --out $(f8dir $SHA $s) ;;
  engB) $CHK --only $ENGB ;;
  engB1) $CHK --only $ENGB1 ;;
  engB2) $CHK --only $ENGB2 ;;
  engB3) $CHK --only $ENGB3 ;;
  mech) $CHK --only $MECH --keep --work $K/mech ;;
  s7) $CHK --only s7_lead ;;
  c26a) $CHK --only c26_choice --keep --work $K/c26 ;;
  c26b) $CHK --only c26_world --keep --work $K/c26 ;;
  lives) $CHK --only $LIVES --keep --work $K/lives ;;
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
  fp) SHA=$SHA REPO=$REPO bash $V/fp/fp.sh ;;
  needs) needs ;;
  nbase) needs ;;   # needs on NBASE (34721bb) with no ship_hook, so ndm compares one machine's two sides (v25: the PC)
  ndm) ndm ;;
  wa|waoff) wa ;;
  wam) wam ;;
  hover) hover ;;
  hp_none) hp none ;;
  hp_let) hp let ;;
  hp_reader) hp reader ;;
  hp_aims) hp reader-aims ;;
  hp_aims2) SEEDS="7 8 9 10 11 12" hp reader-aims ;;
  hp_oracle) hp oracle ;;
  hp_boldoff) TAG=boldoff GAMESET='{"bold": false}' hp reader-aims ;;
  pb) hp steerU ;;   # PB (SK1, SK2): on G and on the played base 7a8cac6 (records/v25/round0.md), into out/v24/heights/play_<sha7>/
  hjudge) hjudge ;;
  st1) st1 ;;
  q1asks) q1asks ;;
  final) $CHK --only $ENGB; $CHK --only $MECH --keep --work $K/mech; $CHK --only s7_lead
     $CHK --only c26_choice,c26_world --keep --work $K/c26; $CHK --only $LIVES8 --keep --work $K/lives; carry_final ;;
  foot) foot ;;
  fp4) fp4 ;;
  gv24) gv24 ;;
  merged) merged ;;
  *) sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2 ;;
esac
