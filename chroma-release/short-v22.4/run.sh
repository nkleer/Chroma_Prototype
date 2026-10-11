#!/bin/bash
# v22.4 release record (records/v22.4/scope.md, rows G1 to G19): one job line per machine, run from anywhere. Every result
# lands in chroma-release/out/ with the commit checked: SHA=, or the record's "commit:" line (the final commit, which is
# what record.py counts). Scratch under /tmp.
#   SHA=<refit commit> bash /mnt/project-files/chroma-release/short-v22.4/run.sh <m1|m2|m3|m4|m5|m6>   (when the refit lands)
#   bash /mnt/project-files/chroma-release/short-v22.4/run.sh <final|final_game|b7AB|b7CD|page|g4>    (on the final commit)
# On the refit commit (about 4 cores each):
#   m1   the Book's rarity table rebuilt at 1,000 lives a seed, copied to out/rarity_rebuild_<UTC>.json for the Engine's
#        rarity.json and the Game's re-pin (G16); then the integrity rows: safety, setting, builds, pin, art, the engine's
#        steps and switches, the game plays (G1, G2, G3, G13)
#   m2   the colour pie with and without packs, 400 lives on each of seeds 41 to 44, pooled (1,600) and seed 41 alone (G5);
#        then the page layer against release/v22.3, the fit probes and the tours on the commit's build (G17)
#   m3   death, child deaths, seasons, chance, satisfaction, acceptance, exits, inertia, goals (G5); then the mechanics'
#        own targets: S1, S3 and S4 (one run each, read by their rows), S6, S7 (G6, G7, G8, G10, G11)
#   m4   the game's browser drivers, groups A and B (G15); then g4
#   m5   the game's browser drivers, groups C and D (G15); then the game's own full checks (G13), the steered and Voice
#        rows and S2's own_even (G12)
#   m6   item 26's colour-choice run, judged by check_c26.py (G19; 960 lives, about 75 minutes), and the same with the
#        world on, steered lives picking as a player does (c26_world, G19w; about 80 minutes); then S5's two targets (G9)
# On the final commit (the refit, its rarity table, the Game's re-pin):
#   final       every v22_checks row again (unchanged files are reused in seconds); the rarity row from m1's rebuild when
#               the refit and the final commit differ only in the rarity files, else rebuilt; the old saves (G14); the
#               page rows and g4 carried from the refit then too
#   final_game  the game's own checks, the steered rows and own_even again (those that read the re-pinned rarity.py rerun)
#   page        the page layer on the commit (G17), when `final` could not carry m2's results over
#   b7AB b7CD   the build of the commit, then the game's browser drivers (one per machine: both serve on port 8140)
#   g4          switching v22.4 off gives v22.3's lives (G4): same-lives.sh part 1 (seed 41, 400 lives x 100 years, worlds
#               off, on and seed, and sweeps A and B; about 50 minutes) on the commit's engine, Library and packs against
#               the live v22.3 engine. NEW runs with every v22.4 switch at its UPD_OFF value (read from the commit's
#               engine) and CHROMA_PACKS=science,politics,stage, which keeps the art pack out (the Engine's override; the
#               live engine does not read it)
# Split across helper machines (Emren 10-11 18:22 UTC: more threads to bring v22.4 sooner), one job a machine of about 4
# cores, in any order, on the same SHA; together they are m1 to m6 (with saves_note), so each row runs once:
#   rar     the rarity row alone (G16): RARITY-SAME when the commit carries the rebuilt table; else it rebuilds the table as
#           m1 does, for the Engine's rarity.json and the Game's re-pin (about 70 minutes)
#   quick   m1's integrity rows and the old saves (G1, G2, G3, G13, G14)
#   enga    m3's Engine rows and S5's two targets (G5, G9)
#   mech    S1, S3, S4, S6 and S7 (G6, G7, G8, G10, G11)
#   c26a    item 26's colour-choice run (G19, about 75 minutes)
#   c26b    the same with the world on (G19w, about 80 minutes)
#   lives   the colour pie with and without packs (G5)
#   game    the game's own checks, the steered and Voice rows and S2's own_even (G12, G13), as final_game
#   page, b7AB, b7CD, g4 as above
set -u
F=/mnt/project-files; R=${R:-$F/chroma-release}; REPO=${REPO:-/tmp/v224_repo}; X=/tmp/v224_${1:-}
K=/tmp/v224_keep   # work folders whose path is part of a row's proof (rows that write npz or stats there): the same on
                   # every machine and job, so `final` reuses the refit's passes when nothing they read changed
SHA=${SHA:-$(sed -n 's/^commit: *\([0-9a-f]\{40\}\) *$/\1/p' $F/chroma-release/records/v22.4/scope.md)}   # the record's commit line
[ -n "$SHA" ] || { echo "no SHA= and no commit in records/v22.4/scope.md yet"; exit 2; }
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e $SHA^{commit} 2>/dev/null || git -C $REPO fetch -q origin main || exit 2
SHA=$(git -C $REPO rev-parse $SHA^{commit}) || exit 2
export CHROMA_COMMIT=$SHA PW=${PW:-/opt/node22/lib/node_modules/playwright}
O=${CHROMA_ROOT:-$(dirname $R)}/chroma-release/out; mkdir -p $O
CHK="python3 -B $R/v22_checks.py --repo $REPO --commit $SHA"
RID=${RARITY_ID:-rarity1000}
QUICK=content,setting,voice,timeless,packrules,pack_check,build_earth,build_packs,balance,perks,pack_stats,pack_balance
QUICK=$QUICK,pin,build,icons,art,t_steps,identity1,fuzz,markers,saveload,end_at_choice,saveload_world,life_ends,identity_g
LIVES=lean41,lean42,lean43,lean44,nopack41,nopack42,nopack43,nopack44,lean,pie,pie41
ENGA=death,child_deaths,season,chance,satisf,accept,exits,inertia,goals
MECH=s1_parts,s1_counts,s1_fair,s3_rep,s3_caught,s4_odd,s4_convert,s6_felt,s7_lead
GAME=book_check,kin
# every switch v22.4 adds (scope.md: S1 to S7, item 26, the fallback jobs and green entries), off for g4
OFFKEYS="fair_read sph_eyes sph_odd sacred seen_done lead_ways acc_redraw green_jobs role_practice read_skill lens_want app_vigil"
LOOKBASE=${LOOKBASE:-release/v22.3}   # the published page
LOOK="chroma-game/prototype/web/src/look.css chroma-game/prototype/web/src/look.js chroma-game/prototype/web/src/clarity.css
 chroma-game/prototype/web/src/clarity.js chroma-game/prototype/web/src/build.py
 chroma-game/tools/webdir.py chroma-art/game/lights.json chroma-art/game/pics/portrait-* chroma-look/tools"
HAND="look_same fit_1280 fit_1024 fit_geo fit_phone tour_desktop tour_phone speedpass_s41 speedpass_sweepA speedpass_sweepB"
look() { git -C $REPO fetch -q origin "+refs/heads/$LOOKBASE:refs/remotes/origin/$LOOKBASE" || return 2
  local b=$(git -C $REPO rev-parse origin/$LOOKBASE) o=$O/look_same_$(date -u +%Y%m%d-%H%M%S).txt
  local d=$(git -C $REPO diff --name-only $b $SHA -- $LOOK)
  { echo "v22.4 G17 look_same: the page layer of ${SHA:0:12} against $LOOKBASE (${b:0:12}): $LOOK" | tr -s ' \n' ' '; echo
    [ -z "$d" ] && echo "ok   every page-layer file equal" || { echo "MISS files that differ:"; echo "$d"; }; } > $o; cat $o
  python3 -B $R/results.py add look_same $([ -z "$d" ] && echo PASS || echo FAIL) $o "page layer against $LOOKBASE ${b:0:12}"
  SHA=$SHA BASE=$LOOKBASE bash $R/short-v22.2.1/run.sh page; }   # fits (phone against the v22.3 build) and tours
carry() { local refit=$1; shift   # a hand row's newest PASS on the refit, written again for the final commit
  python3 -B - "$R" "$refit" "$SHA" "$@" <<'PY'
import sys, os
R, refit, sha, ids = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, R)
import results
last = {}
for r in results.read():
    if (r.get("candidate") or {}).get("commit") == refit and r["check"] in ids:
        last[r["check"]] = r
bad = 0
for i in ids:
    r = last.get(i)
    if r and r["result"] == "PASS":
        results.add(i, "PASS", r.get("report", ""), f"carried from the refit {refit[:12]} (only the rarity files changed): "
                    + r.get("note", ""), candidate={"commit": sha})
        print("carried", i)
    else:
        print("NOT CARRIED", i, "(no PASS on the refit)"); bad = 1
sys.exit(bad)
PY
  [ $? = 0 ] || echo "not all carried: run \`run.sh page\` or \`run.sh g4\` on a free machine for those"; }
RARITY_READS="chroma-engine chroma-library chroma-packs"   # what the rarity rebuild and same-lives.sh read
carryp() { local paths=$1; shift   # a hand row's newest PASS on any commit, written again for $SHA when nothing it reads
  python3 -B - "$R" "$REPO" "$SHA" "$paths" "$@" <<'PY'   # (paths; empty: the whole tree) changed but the rarity files
import sys, subprocess
R, repo, sha, paths, ids = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(), sys.argv[5:]
sys.path.insert(0, R)
import results
last, here = {}, set()
for r in results.read():
    c = (r.get("candidate") or {}).get("commit") or ""
    if r["check"] in ids and c == sha:
        here.add(r["check"])
    elif r["check"] in ids and r["result"] == "PASS" and len(c) == 40:
        last[r["check"]] = r
bad = 0
for i in ids:
    r = last.get(i)
    if i in here:
        print("already on", sha[:12], i); continue
    if not r:
        print("NOT CARRIED", i, "(no PASS on any commit)"); bad = 1; continue
    frm = r["candidate"]["commit"]
    d = subprocess.run(["git", "-C", repo, "diff", "--name-only", frm, sha, "--"] + paths, capture_output=True, text=True)
    moved = [f for f in d.stdout.split() if not f.endswith(("/rarity.json", "/rarity.py"))]
    if d.returncode or moved:
        print("NOT CARRIED", i, f"(changed since {frm[:12]}: {', '.join(moved[:4]) or d.stderr.strip()})"); bad = 1; continue
    results.add(i, "PASS", r.get("report", ""), f"carried from {frm[:12]} (nothing it reads changed since but the rarity "
                f"files): " + r.get("note", ""), candidate={"commit": sha})
    print("carried", i, "from", frm[:12])
sys.exit(bad)
PY
  [ $? = 0 ] || echo "not all carried: run their jobs (page, b7AB, b7CD, g4) on free machines"; }
lives() { $CHK --only $LIVES --keep --work $K/lives || $CHK --only $LIVES --no-reuse --keep --work $K/lives; }   # pie reads the npz here
mech() { $CHK --only $MECH --keep --work $K/mech; }            # S1, S3 and S4 rows read their run's stats here
c26() { $CHK --only c26_choice,c26_world --keep --work $K/c26; }   # c26_world: G19 with the world on (G19w)
b7() { rm -rf $X/b7; mkdir -p $X; $CHK --only build --no-reuse --keep --work $X/b7 > $X/b7.log 2>&1   # a reused build leaves no folder
  [ -f $X/b7/w/build/BUILD.md ] || { echo "STOP: no build in $X/b7/w/build (see $X/b7.log)"; return 1; }
  bash $R/short-v22.1/b7.sh $1 2 $X/b7/w/build; }
g4() { local E=$X/g4; rm -rf $E; mkdir -p $E
  git -C $REPO archive $SHA chroma-engine/v22-speedpass chroma-library chroma-packs | tar -x -C $E || return 1
  local pnew; pnew=$(python3 -B - $E/chroma-engine/v22-speedpass $OFFKEYS <<'PY'
import sys, os, json, importlib.util
d, keys = sys.argv[1], sys.argv[2:]
sys.path.insert(0, d)
sp = importlib.util.spec_from_file_location("engine_g4", os.path.join(d, "engine.py"))
E = importlib.util.module_from_spec(sp); sp.loader.exec_module(E)
miss = [k for k in keys if k not in E.UPD_OFF]
if miss:
    sys.exit("STOP: not in the commit's UPD_OFF: " + ", ".join(miss))
print(json.dumps({k: E.UPD_OFF[k] for k in keys}))
PY
) || { echo "$pnew"; return 1; }
  echo "g4: PNEW=$pnew CHROMA_PACKS=science,politics,stage, against the live engine"
  CHROMA_PACKS=science,politics,stage PNEW="$pnew" NEW=$E/chroma-engine/v22-speedpass LIB=$E/chroma-library \
    PACKS=$E/chroma-packs COMMIT=$SHA bash $R/same-lives.sh 1; }
echo "v22.4 ${1:-} on $SHA"
case "${1:-}" in
  m1) rm -rf $X; $CHK --only $RID --no-reuse --keep --work $X/rarity   # its cmp fails until the table is committed: the rebuild is the point
     t=$X/rarity/w/rarity.json; [ -s $t ] || { echo "STOP: no rebuilt table in $X/rarity/w"; exit 1; }
     o=$O/rarity_rebuild_$(date -u +%Y%m%d-%H%M).json; cp $t $o; echo "$SHA $RID" > $o.from
     echo "REBUILT on ${SHA:0:12} ($RID): $o (md5 $(md5sum < $o | cut -c1-12)); the Engine commits it as its rarity.json, the Game re-pins"
     $CHK --only $QUICK ;;
  rar) rm -rf $X; $CHK --only $RID --keep --work $X/rarity && { echo "RARITY-SAME on ${SHA:0:12}: nothing to re-pin"; exit 0; }
     t=$X/rarity/w/rarity.json; [ -s $t ] || { echo "STOP: no rebuilt table in $X/rarity/w"; exit 1; }
     o=$O/rarity_rebuild_$(date -u +%Y%m%d-%H%M).json; cp $t $o; echo "$SHA $RID" > $o.from
     echo "REBUILT on ${SHA:0:12} ($RID): $o (md5 $(md5sum < $o | cut -c1-12)); the Engine commits it as its rarity.json, the Game re-pins" ;;
  quick) $CHK --only $QUICK,saves_note ;;
  enga) $CHK --only $ENGA,s5_lines,s5_money ;;
  mech) mech ;;
  c26a) $CHK --only c26_choice --keep --work $K/c26 ;;
  c26b) $CHK --only c26_world --keep --work $K/c26 ;;
  lives) lives ;;
  game) $CHK --only $GAME; $CHK --only @steered; $CHK --only own_even ;;
  m2) lives; look ;;
  m3) $CHK --only $ENGA; mech ;;
  m4) b7 A,B; g4 ;;
  m5) b7 C,D; $CHK --only $GAME; $CHK --only @steered; $CHK --only own_even ;;
  m6) c26; $CHK --only s5_lines,s5_money ;;
  final) $CHK --only $QUICK,$ENGA,s5_lines,s5_money,saves_note; mech; c26; lives   # reused where nothing they read changed
     rel=$(cd $F/chroma-env && python3 -B -c "from paths import NAMES; print(NAMES['rarity_live'][0])")
     o=$(ls -t $O/rarity_rebuild_*.json 2>/dev/null | head -1); REFIT=; ID=$RID; [ -n "$o" ] && read REFIT ID < $o.from
     moved=x; [ -n "$REFIT" ] && moved=$(git -C $REPO diff --name-only $REFIT $SHA -- $RARITY_READS | grep -v -e '/rarity\.json$' -e '/rarity\.py$')
     rep=$O/${ID}_$(date -u +%Y%m%d-%H%M%S).txt
     if [ -z "$moved" ] && git -C $REPO show $SHA:$rel | cmp -s - $o; then
       { echo "$ID on ${SHA:0:12}: the table rebuilt on ${REFIT:0:12} ($o) equals the commit's $rel byte for byte, and"
         echo "nothing the rebuild reads ($RARITY_READS) changed between them but the rarity files"; echo "RARITY-SAME"; } > $rep
       python3 -B $R/results.py add $ID PASS $rep "rebuilt on ${REFIT:0:12}; nothing it reads changed since"
     else $CHK --only $ID; fi    # reused when the commit carried the table where rar read RARITY-SAME, else rebuilt
     carryp "$RARITY_READS" speedpass_s41 speedpass_sweepA speedpass_sweepB
     carryp "" look_same fit_1280 fit_1024 fit_geo fit_phone tour_desktop tour_phone b7_AB b7_CD ;;
  final_game) $CHK --only $GAME; $CHK --only @steered; $CHK --only own_even ;;
  page) look ;;
  g4) g4 ;;
  b7AB) b7 A,B ;;
  b7CD) b7 C,D ;;
  b7A|b7B|b7C|b7D) b7 ${1#b7} ;;                 # the wide split (Emren 10-11 21:36, "use more threads"): one group a machine
  gameA) $CHK --only $GAME ;;
  gameB) $CHK --only @steered ;;
  gameC) $CHK --only own_even ;;
  qslow1) $CHK --only timeless ;;
  qslow2) $CHK --only life_ends,identity_g ;;
  qslow3) $CHK --only fuzz,markers ;;
  qsteps) $CHK --only t_steps ;;
  quickrest) $CHK --only $(echo $QUICK | tr , '\n' | grep -vxE 'timeless|life_ends|identity_g|fuzz|markers|t_steps' | paste -sd,),saves_note ;;
  mechrest) $CHK --only ${MECH%,s7_lead} --keep --work $K/mech ;;   # s7_lead stands from ef7f273 (ruling "S7's time in post reported")
  *) sed -n 2,43p "$0"; exit 2 ;;
esac
