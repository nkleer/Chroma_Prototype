#!/bin/bash
# v23 release record (records/v23/scope.md, rows K1 to K28, N1, N3, P1 to P6, W1 to W5; the jobs: plan.md §3):
# one job a machine of about 4 cores, run from anywhere. Every result lands in chroma-release/out/ with the commit it
# checked. Scratch under /tmp. Two commits:
#   the refit   main after the Engine's joint refit merges (engine/v226-refit, #294): the engine-only jobs, while the
#               rarity table is rebuilt and the Game re-pins
#   the final   the record's commit: main after the rarity table and the Game's re-pin
#
#   SHA=<refit> bash /mnt/project-files/chroma-release/short-v23/run.sh <refit job>
#   SHA=<final> REFIT=<refit> [N3BASE=<re-pin, returns off>] bash /mnt/project-files/chroma-release/short-v23/run.sh <final job>
# A trial keeps its reports and results lines out of the shared folder with CHROMA_PROJECT=<overlay>: a folder of links
# to every shared-folder entry, whose chroma-release/ links every entry but out/, a scratch folder.
#
# On the refit (engine-only; nothing they read is in the game, so they carry to the final commit when the engine,
# Library, packs and chroma-env differ only in the rarity files):
#   rar1 .. rar5   the world-on rarity rebuild (K25), seeds 101-104, 105-108, 109-112, 113-116, 117-120 a machine
#   rarm           its merge, once the five parts are in: the rebuilt table for the Engine's rarity.json and the re-pin
#   f9a .. f9f     check_f9 seeds 41-42, 43-44, .. 51-52 into out/f9_<refit7> (K6 to K13, K15, K16; judged in `final`)
#   f8a f8b f8c    check_roll f8_after seeds 41-44, 45-48 and 49-52 into out/roll8_<refit7>_<seeds> (K9; judged in rollA)
#   engA | engA1 engA2   K3: t_steps (every row, T_JOBS up to 4) and identity1 | t_steps alone | identity1 alone
#   engB | engB1 engB2 engB3   K5's engine rows and S5: death, child_deaths, satisf, accept | chance, season, exits,
#                  inertia, goals | s5_lines, s5_money
#   mech           S1, S3, S4 and S6 (K19)
#   s7             s7_lead (K19: falls 1.5x and time in post 1.2x)
#   c26a c26b      G19 and G19w with the lift judged (K20)
#   lives          lean41-44, nopack41-44, lean, pie and pie41 in one call (K5; pie reads the npz of the same run)
#   g4 | g4s g4a g4b   K4: same-lives part 1 (seed 41, sweeps A and B; or each alone) against live v22.5, with every
#                  DEFAULT key the commit moved from live v22.5 at its UPD_OFF value (PNEW, read from the two engines)
#                  and the pack's batch flags off ($OFF_FLAGS): they change lives alone, as their moments join the
#                  library (Engine, #294)
#   fit4 fit6      check_fit f4_age and f6_dreams (K17; engine-only, carried)
#   pack1 .. pack4 check_pack.py run (W2, W3, W5), three worlds each: seeds 41-43, 44-46, 47-49, 50-52, into
#                  out/pack_<refit7>
#   pack5          check_pack.py run's four test worlds (W4), seeds 41-44, into the same folder
#   packm          check_pack.py judge on out/pack_<refit7>, once the five parts are in (12 seeds, 4 test seeds)
#   np             N1: check_picks.py noplayer, seed 41, 400 lives x 100 years, worlds off, on and seed, echo_play
#                  off against on (about 20 min on 4 cores)
# On the final commit:
#   quick | q1 .. q5   K1, K2, K22's quick game rows, K23's old saves and K28 lines_tied (pin and build need the re-pin):
#                  the fast rows | timeless | life_ends, identity_g | fuzz, markers | lines_tied
#   game | gameA gameB gameC   book_check and kin | the steered rows | own_even (K21, K22; with own_ix on, W1)
#   pr30 | pr30a pr30b pr30c pr30m   push_rare on 30 seeds (K21): one machine, or seeds 1-10, 11-20, 21-30, then the merge
#   b7A b7B b7C b7D | b7AB b7CD   the browser drivers (K24; one per machine: they serve on port 8140)
#   roll | rollA rollB rollC   K9's f8_after judged once from the f8a-c folders (carried) | f10_once (its engine lives
#                  from f8a's folder) | f7_roll (K18), every one --as-is
#   fit | fitk f15 check_fit all (K17), then check_f15 (K14); or each on its own machine
#   fit12          check_fit f12_start (K17; the game)
#   f15a .. f15d f15m   check_f15 in four parts into out/f15_<final7> (the starts with an upbringing, seeds 1-20 and
#                  start 1 | 21-40 | the far starts, seeds 1-30 | 31-60), then the judge that records f15_lean (K14)
#   picks_on1 .. picks_on4    P1 to P6's on side (`returns` on), preset 1 .. 4 a machine: let and none seeds 1-6,
#                  reader and random seeds 1-18, into out/picks_on_<final7>
#   picks_off1 .. picks_off4  the same lives with `returns` off, into out/picks_off_<final7>
#   picksm         check_picks.py judge on the two folders, once the eight parts are in (192 lives a side)
#   n3             N3: test/same_life.py presets 1-6, seed 7, on the final commit with `returns` off against N3BASE
#                  (the Game's re-pin commit before `returns` goes on), byte for byte
#   page           the page layer against release/v22.5, the fit probes and the tours (K26)
#   final          the refit's rows on the final commit: v22_checks rows again (reused in seconds where nothing they
#                  read changed), the hand rows carried (g4's speedpass rows, pie and pie41, f4_age and f6_dreams,
#                  the pack's W2 to W5, N1's picks_noplayer, check_f9's ten tables, rarity_w) with the evidence in
#                  out/carry_<final7>.txt, each carried line's note saying so
set -u
JOBS=" rar1 rar2 rar3 rar4 rar5 rarm f9a f9b f9c f9d f9e f9f f8a f8b f8c engA engA1 engA2 engB engB1 engB2 engB3 mech s7
 c26a c26b lives g4 g4s g4a g4b fit4 fit6 pack1 pack2 pack3 pack4 pack5 packm np quick q1 q2 q3 q4 q5 game gameA gameB
 gameC pr30 pr30a pr30b pr30c pr30m b7A b7B b7C b7D b7AB b7CD roll rollA rollB rollC fit fitk fit12 f15 f15a f15b f15c
 f15d f15m picks_on1 picks_on2 picks_on3 picks_on4 picks_off1 picks_off2 picks_off3 picks_off4 picksm n3 page final "
[[ "${JOBS//$'\n'/ }" == *" ${1:-none} "* ]] || { sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2; }
F=${CHROMA_PROJECT:-/mnt/project-files}; R=$F/chroma-release; REPO=${REPO:-/tmp/v23_repo}; X=/tmp/v23_${1:-}; JOB=${1:-}
K=/tmp/v23_keep   # --keep --work folders: the same path on every machine, so `final` reuses the refit's proofs
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
CARRY_READS="chroma-engine chroma-library chroma-packs chroma-env"   # what the engine-only jobs read (the rarity files aside)
OFF_FLAGS="TURNOVER_MOMENTS TRUST_MOMENTS INMATE_MOMENTS SHADOW_MOMENTS"   # the pack's batch flags, on from the refit (K4: off)
CARRIED="speedpass_s41 speedpass_sweepA speedpass_sweepB pie pie41 f4_age f6_dreams sph_places sph_trust sph_inmates sph_grey picks_noplayer"
F9_TABLES="f9_parents f9_partners f9_homes f9_work f9_illness f9_deaths f9_means f14_settle f17_deeds f19_mind"
LOOKBASE=${LOOKBASE:-release/v22.5}   # the published page
LOOK="chroma-game/prototype/web/src/look.css chroma-game/prototype/web/src/look.js chroma-game/prototype/web/src/clarity.css
 chroma-game/prototype/web/src/clarity.js chroma-game/prototype/web/src/build.py
 chroma-game/tools/webdir.py chroma-art/game/lights.json chroma-art/game/pics/portrait-* chroma-look/tools"
tree() { [ -d $X/tree ] && [ "$(cat $X/tree.sha 2>/dev/null)" = "$SHA" ] && return 0   # the commit's files, stamped with it
  rm -rf $X/tree $X/tree.sha; mkdir -p $X/tree && git -C $REPO archive $SHA | tar -x -C $X/tree && echo $SHA > $X/tree.sha; }
moved() { local f; git -C $REPO diff --name-only $1 $2 -- $CARRY_READS | grep -v -e '/rarity\.json$' -e '/rarity\.py$' |
  while read -r f; do   # an MD5SUMS whose only changed line is rarity.json's is a rarity file too
    [[ $f == */MD5SUMS ]] && [ -z "$(git -C $REPO diff -U0 $1 $2 -- $f | grep '^[-+][^-+]' | grep -v ' rarity\.json$')" ] && continue
    echo "$f"; done; }
need_refit() { [ -n "$REFIT" ] || { echo "REFIT=<the refit commit> is needed for $1"; exit 2; }
  local m; m=$(moved $REFIT $SHA)
  [ -z "$m" ] || { echo "NOT CARRIED: the engine, Library or packs changed between ${REFIT:0:12} and ${SHA:0:12}:"; echo "$m" | head
                   echo "run the refit jobs (f9a-f f8a-c g4 pack1-5 np rar1-5) on ${SHA:0:12} itself"; exit 1; }; }
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
g4() { local E=$X/g4 D=chroma-engine/v22-speedpass f; rm -rf $E; mkdir -p $E
  git -C $REPO archive $SHA $D chroma-library chroma-packs | tar -x -C $E || return 1
  for f in $OFF_FLAGS; do sed -i "s/^$f = True /$f = False/" $E/$D/batch.py
    grep -q "^$f = False" $E/$D/batch.py || { echo "STOP: no '$f = True' line in batch.py"; return 1; }; done
  local pnew; pnew=$(python3 -B - $E/$D $F/$D <<'PY'
import sys, json, pickle, subprocess, tempfile
import numpy as np
READ = ("import sys, pickle; sys.path.insert(0, sys.argv[1]); import engine as E; "
        "pickle.dump((E.DEFAULT, E.UPD_OFF), open(sys.argv[2], 'wb'))")
def read(d):   # each engine in its own process: two engines' sibling modules never mix in one
    with tempfile.NamedTemporaryFile(suffix=".pkl") as f:
        subprocess.run([sys.executable, "-B", "-c", READ, d, f.name], cwd=d, capture_output=True, check=True)
        return pickle.load(open(f.name, "rb"))
def same(x, y):
    if hasattr(x, "shape") or hasattr(y, "shape"):
        return bool(np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)))
    return x == y
(ND, NU), (LD, _) = read(sys.argv[1]), read(sys.argv[2])
P, stop, note = {}, [], []
for k, v in ND.items():
    if k in LD and same(LD[k], v):
        continue
    if k not in NU:
        (stop if k in LD else note).append(k)   # a new part's own setting, read only with its switch on
    elif not same(NU[k], LD.get(k, NU[k])):
        stop.append(k)
    elif not same(NU[k], v):
        P[k] = NU[k]
if stop:
    sys.exit("STOP: DEFAULT moved from live v22.5 with no UPD_OFF value to set back: " + ", ".join(stop))
print("g4: settings new with their parts, left as they are: " + ", ".join(note), file=sys.stderr)
print(json.dumps(P))
PY
) || { echo "$pnew"; return 1; }
  echo "g4: PNEW=$pnew; batch $OFF_FLAGS off; ${SHA:0:12} against the live engine (v22.5)"
  [ -n "${DRY:-}" ] && { echo "g4: DRY, the lives not run ($E)"; return 0; }
  PNEW="$pnew" NEW=$E/$D LIB=$E/chroma-library PACKS=$E/chroma-packs COMMIT=$SHA bash $R/same-lives.sh $1; }
pool() {   # $1: a folder of split jobs' files; every parts/<job>.json (a job's meta.json) must name SHA and agree but for the split
  python3 -B - "$1" "$SHA" <<'PY'
import json, glob, os, sys
d, sha = sys.argv[1:3]
ms = sorted(glob.glob(os.path.join(d, "parts", "*.json")))
if not ms:
    sys.exit(f"STOP: no parts/<job>.json in {d}")
SPLIT = ("seeds", "test_seeds", "presets", "policies", "time")
M = [json.load(open(m)) for m in ms]
bad = [os.path.basename(m) for m, x in zip(ms, M) if x.get("commit") != sha]
if bad:
    sys.exit(f"STOP: {', '.join(bad)} name another commit than {sha[:12]}")
odd = [os.path.basename(m) for m, x in zip(ms, M) if {k: v for k, v in x.items() if k not in SPLIT} != {k: v for k, v in M[0].items() if k not in SPLIT}]
if odd:
    sys.exit(f"STOP: {', '.join(odd)} differ from {os.path.basename(ms[0])} in more than the split")
out = dict(M[0], parts=[os.path.basename(m) for m in ms])
json.dump(out, open(os.path.join(d, "meta.json"), "w"))
print(f"pooled {len(ms)} parts in {d}, every one on {sha[:12]}")
PY
}
packp() { local o=$O/pack_${SHA:0:7} w=$X/pack; mkdir -p $o   # a part of check_pack's worlds; packm judges the folder
  python3 -B $R/check_pack.py run --repo $REPO --commit $SHA --out $w --jobs 4 "$@" || return 1
  cp $w/seed*.json $w/test*.json $o/ 2>/dev/null; mkdir -p $o/parts && cp $w/meta.json $o/parts/$JOB.json
  echo "PACK PART done ($*): $(ls $o/seed*.json 2>/dev/null | wc -l) of 12 seeds and $(ls $o/test*.json 2>/dev/null | wc -l) of 4 test seeds in $o"; }
packm() { local o=$O/pack_${SHA:0:7}
  [ $(ls $o/seed*.json 2>/dev/null | wc -l) = 12 ] && [ $(ls $o/test*.json 2>/dev/null | wc -l) = 4 ] ||
    { echo "STOP: $o holds $(ls $o/seed*.json 2>/dev/null | wc -l) of 12 seeds and $(ls $o/test*.json 2>/dev/null | wc -l) of 4 test seeds"; return 1; }
  pool $o && python3 -B $R/check_pack.py judge $o; }
picksp() { local o=$O/picks_$1_${SHA:0:7} w=$X/picks g n; mkdir -p $o   # $1 on|off, $2 the preset
  g=$([ $1 = on ] && echo '{"returns": true}' || echo '{"returns": false}')
  python3 -B $R/check_picks.py run --repo $REPO --commit $SHA --out $w --game "$g" --policies let,none --presets $2 --seeds 1-6 --jobs 4 &&
    python3 -B $R/check_picks.py run --repo $REPO --commit $SHA --out $w --game "$g" --policies reader,random --presets $2 --seeds 1-18 --jobs 4 || return 1
  n=$(ls $w/*_$2_*.json | wc -l); [ $n = 48 ] || { echo "PICKS PART FAILED: $n of 48 lives in $w"; return 1; }
  cp $w/*_$2_*.json $o/ && mkdir -p $o/parts && cp $w/meta.json $o/parts/$JOB.json
  echo "PICKS PART done ($1, preset $2): $(ls $o/*_*_*.json | wc -l) of 192 lives in $o"; }
picksm() { local a=$O/picks_on_${SHA:0:7} b=$O/picks_off_${SHA:0:7} d
  for d in $a $b; do [ $(ls $d/*_*_*.json 2>/dev/null | wc -l) = 192 ] || { echo "STOP: $d holds $(ls $d/*_*_*.json 2>/dev/null | wc -l) of 192 lives"; return 1; }
    pool $d || return 1; done
  python3 -B $R/check_picks.py judge --on $a --off $b; }
n3() { [ -n "${N3BASE:-}" ] || { echo "N3BASE=<the Game's re-pin commit before returns goes on> is needed"; return 2; }
  local b p side c ok=0 d=$X/n3 o=$O/n3_${SHA:0:7}_$(date -u +%Y%m%d-%H%M%S).txt; b=$(git -C $REPO rev-parse "$N3BASE^{commit}") || return 2
  rm -rf $d; mkdir -p $d/new $d/base
  git -C $REPO archive $SHA chroma-game/prototype | tar -x -C $d/new && git -C $REPO archive $b chroma-game/prototype | tar -x -C $d/base || return 1
  for p in ${N3P:-1 2 3 4 5 6}; do for side in new base; do
    while [ $(jobs -rp | wc -l) -ge 4 ]; do sleep 2; done
    ( cd $d/$side/chroma-game/prototype && { [ $side = new ] && export CHROMA_GAME='{"returns": false}'; true; } &&
      python3 -B test/same_life.py $p 7 $d/${side}_$p.jsonl > $d/${side}_$p.out 2>&1 ) &
  done; done; wait
  { echo "v23 N3 on ${SHA:0:12} with returns off (CHROMA_GAME) against ${b:0:12} (N3BASE), test/same_life.py presets ${N3P:-1 2 3 4 5 6}, seed 7"
    for p in ${N3P:-1 2 3 4 5 6}; do
      if [ -s $d/new_$p.jsonl ] && cmp -s $d/new_$p.jsonl $d/base_$p.jsonl; then echo "ok   preset $p: $(wc -l < $d/new_$p.jsonl) steps, identical ($(tail -1 $d/new_$p.out))"
      else ok=1; echo "MISS preset $p: $(cmp $d/new_$p.jsonl $d/base_$p.jsonl 2>&1 | head -1)"; fi; done
    echo "N3: $([ $ok = 0 ] && echo PASS || echo FAIL)"; } > $o; cat $o
  python3 -B $R/results.py add prove_same $([ $ok = 0 ] && echo PASS || echo FAIL) ${o#$F/} \
    "same_life.py presets 1-6 seed 7, returns off, against the re-pin before returns ${b:0:12}"; }
look() { git -C $REPO fetch -q origin "+refs/heads/$LOOKBASE:refs/remotes/origin/$LOOKBASE" || return 2
  local b=$(git -C $REPO rev-parse origin/$LOOKBASE) o=$O/look_same_$(date -u +%Y%m%d-%H%M%S).txt
  local d=$(git -C $REPO diff --name-only $b $SHA -- $LOOK)
  { echo "v23 K26 look_same: the page layer of ${SHA:0:12} against $LOOKBASE (${b:0:12}): $LOOK" | tr -s ' \n' ' '; echo
    [ -z "$d" ] && echo "ok   every page-layer file equal" || { echo "differ (each must be a v23 change the bar names):"; echo "$d"; }; } > $o; cat $o
  python3 -B $R/results.py add look_same $([ -z "$d" ] && echo PASS || echo FAIL) $o "page layer against $LOOKBASE ${b:0:12}"
  SHA=$SHA BASE=$LOOKBASE bash $R/short-v22.2.1/run.sh page; }
carry_final() {   # the refit's hand rows written again for the final commit, with the evidence
  need_refit final
  local c=$O/carry_${SHA:0:7}.txt
  { echo "v23 carry: refit ${REFIT:0:12} -> final ${SHA:0:12}; $(CARRY_NOTE)"
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
    { echo "v23 K25 rarity_w on ${SHA:0:12}: the table rebuilt with the world on from the refit ${REFIT:0:12} ($t, md5"
      echo "$(md5sum < $t | cut -c1-12)); the engine's rarity.json: $ce; the game's rarity.json: $cg; $(CARRY_NOTE)"
      [ $ce = same ] && [ $cg = same ] && echo "RARITY_W: PASS" || echo "RARITY_W: FAIL"; } > $rep
    python3 -B $R/results.py add rarity_w $([ $ce = same ] && [ $cg = same ] && echo PASS || echo FAIL) ${rep#$F/} \
      "rebuilt on the refit ${REFIT:0:12} (world on, 200 x 20); engine table $ce, game table $cg"
    echo "rarity_w: engine $ce, game $cg ($rep)" >> $c
  else echo "NOT CARRIED rarity_w: no rebuilt world table from ${REFIT:0:12} (run rar1-5 and rarm on it)" >> $c; fi
  cat $c; }
echo "v23 ${1:-} on $SHA$([ -n "$REFIT" ] && echo " (refit $REFIT)")"
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
  engA1) $CHK --only t_steps ;;
  engA2) $CHK --only identity1 ;;
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
  pack[1-4]) a=$((41 + 3 * (${1#pack} - 1))); packp --seeds $a-$((a + 2)) --test-seeds "" ;;
  pack5) packp --seeds "" --test-seeds 41-44 ;;
  packm) packm ;;
  np) python3 -B $R/check_picks.py noplayer --repo $REPO --commit $SHA --out $X/np --jobs 4 ;;
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
  picks_on[1-4]) picksp on ${1#picks_on} ;;
  picks_off[1-4]) picksp off ${1#picks_off} ;;
  picksm) picksm ;;
  n3) n3 ;;
  page) look ;;
  final) $CHK --only $ENGA,$ENGB; $CHK --only $MECH --keep --work $K/mech; $CHK --only s7_lead
     $CHK --only c26_choice,c26_world --keep --work $K/c26; $CHK --only $LIVES8 --keep --work $K/lives; carry_final ;;
  *) sed -n '2,/^set -u/{/^#/p}' "$0"; exit 2 ;;
esac
