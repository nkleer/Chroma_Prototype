#!/bin/bash
# v22.3 release record (records/v22.3/scope.md): one job line per machine, run from anywhere. Every result lands in
# chroma-release/out/ with the commit checked: SHA=, or the record's "commit:" line (the final commit, which is what
# record.py counts). Scratch under /tmp.
#   SHA=<refit commit> bash /mnt/project-files/chroma-release/short-v22.3/run.sh <m1|m2|m3|m4|m5>   (when the refit lands)
#   bash /mnt/project-files/chroma-release/short-v22.3/run.sh <final|final_game|b7AB|b7CD>         (on the final commit)
# On the refit commit (about 4 cores each):
#   m1   the Book's rarity table rebuilt at 1,000 lives a seed (four seeds side by side), copied to
#        out/rarity_rebuild_<UTC>.json for the Engine's rarity.json and the Game's re-pin (RARITY_ID=rarity: 300 a seed);
#        then the integrity rows (safety, setting, builds, pin, art, the engine's steps and switches, the game plays)
#   m2   the colour pie with and without packs, 400 lives on each of seeds 41 to 44, pooled (1,600) and seed 41 alone;
#        then the page layer (Q10): its files equal v22.2.1's, the fit probes and the tours on the commit's build
#   m3   death, child deaths, seasons, chance, satisfaction, acceptance, exits, inertia, goals (world off and on); then
#        the Library's titles and reach, the go-live identity at full size, ages and the outer world
#   m4   the game's browser drivers, groups A and B; then the survey scores, tiers, roles, repeats, felt odds, plans,
#        foresight, the 200-life pies and the speed
#   m5   the game's browser drivers, groups C and D; then the game's own full checks and the steered and Voice rows
# On the final commit (the refit, its rarity table, the Game's re-pin):
#   final       every v22_checks row again (unchanged files are reused in seconds); the rarity row from m1's rebuild when
#               the refit and the final commit differ only in the rarity files, else rebuilt again; the old saves
#   final_game  the game's own checks and the steered rows again (those that read the re-pinned rarity.py run again)
#   page        the page layer on the commit (Q10), when `final` could not carry m2's results over
#   b7AB b7CD   the build of the commit, then the game's browser drivers (one per machine: both serve on port 8140)
set -u
F=/mnt/project-files; R=${R:-$F/chroma-release}; REPO=${REPO:-/tmp/v223_repo}; X=/tmp/v223_$1
SHA=${SHA:-$(sed -n 's/^commit: *\([0-9a-f]\{40\}\) *$/\1/p' $F/chroma-release/records/v22.3/scope.md)}   # the record's commit line
[ -n "$SHA" ] || { echo "no SHA= and no commit in records/v22.3/scope.md yet"; exit 2; }
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
ENGA=death,death_won,child_deaths,season,chance,satisf,satisf_won,accept,exits,exits_won,inertia,goals,goals_won
ACROSS=titles,reach,identity,identity_full,ages,world
ENGB=score21,score23,tier,roles,repeat,felt_gap,plan_felt,foresee_off,foresee_on,pie_packs,pie_nopacks,pie_won,speed
GAME=peace_bands,acceptance,longshot_check,event_rate,season_rate,roles2,roles_g,book_check,next2_check,season_ages,kin,abroad
LOOKBASE=${LOOKBASE:-release/v22.2.1}   # the published visual update; before it is pushed: LOOKBASE=visual/v22.2.1
LOOK="chroma-game/prototype/web/src/look.css chroma-game/prototype/web/src/look.js chroma-game/prototype/web/src/clarity.css
 chroma-game/prototype/web/src/clarity.js chroma-game/prototype/web/src/build.py
 chroma-game/tools/webdir.py chroma-art/game/lights.json chroma-art/game/pics/portrait-* chroma-look/tools"
HAND="look_same fit_1280 fit_1024 fit_geo fit_phone tour_desktop tour_phone"   # rows outside v22_checks
look() { git -C $REPO fetch -q origin "+refs/heads/$LOOKBASE:refs/remotes/origin/$LOOKBASE" || return 2
  local b=$(git -C $REPO rev-parse origin/$LOOKBASE) o=$O/look_same_$(date -u +%Y%m%d-%H%M%S).txt
  local d=$(git -C $REPO diff --name-only $b $SHA -- $LOOK)
  { echo "v22.3 Q10 look_same: the page layer of ${SHA:0:12} against $LOOKBASE (${b:0:12}): $LOOK" | tr -s ' \n' ' '; echo
    [ -z "$d" ] && echo "ok   every page-layer file equal" || { echo "MISS files that differ:"; echo "$d"; }; } > $o; cat $o
  python3 -B $R/results.py add look_same $([ -z "$d" ] && echo PASS || echo FAIL) $o "page layer against $LOOKBASE ${b:0:12}"
  SHA=$SHA BASE=$LOOKBASE bash $R/short-v22.2.1/run.sh page; }   # fits (phone against the v22.2.1 build) and tours
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
  [ $? = 0 ] || echo "page layer not carried: run \`run.sh page\` on a free machine"; }
lives() { $CHK --only $LIVES --keep --work $X/lives || $CHK --only $LIVES --no-reuse --keep --work $X/lives; }   # pie reads the npz here
b7() { rm -rf $X/b7; mkdir -p $X; $CHK --only build --no-reuse --keep --work $X/b7 > $X/b7.log 2>&1   # a reused build leaves no folder
  [ -f $X/b7/w/build/BUILD.md ] || { echo "STOP: no build in $X/b7/w/build (see $X/b7.log)"; return 1; }
  bash $R/short-v22.1/b7.sh $1 2 $X/b7/w/build; }
echo "v22.3 $1 on $SHA"
case "$1" in
  m1) rm -rf $X; $CHK --only $RID --no-reuse --keep --work $X/rarity   # its cmp fails until the table is committed: the rebuild is the point
     t=$X/rarity/w/rarity.json; [ -s $t ] || { echo "STOP: no rebuilt table in $X/rarity/w"; exit 1; }
     o=$O/rarity_rebuild_$(date -u +%Y%m%d-%H%M).json; cp $t $o; echo "$SHA $RID" > $o.from
     echo "REBUILT on ${SHA:0:12} ($RID): $o (md5 $(md5sum < $o | cut -c1-12)); the Engine commits it as its rarity.json, the Game re-pins"
     $CHK --only $QUICK ;;
  m2) lives; look ;;
  m3) $CHK --only $ENGA; $CHK --only $ACROSS ;;
  m4) b7 A,B; $CHK --only $ENGB ;;
  m5) b7 C,D; $CHK --only $GAME; $CHK --only @steered ;;
  final) $CHK --only $QUICK,$ENGA,$ACROSS,$ENGB,saves_note; lives
     o=$(ls -t $O/rarity_rebuild_*.json | head -1); read REFIT ID < $o.from
     moved=$(git -C $REPO diff --name-only $REFIT $SHA | grep -v -e '/rarity\.json$' -e '/rarity\.py$')
     rel=$(cd $F/chroma-env && python3 -B -c "from paths import NAMES; print(NAMES['rarity_live'][0])")
     rep=$O/${ID}_$(date -u +%Y%m%d-%H%M%S).txt
     if [ -z "$moved" ] && git -C $REPO show $SHA:$rel | cmp -s - $o; then
       { echo "$ID on ${SHA:0:12}: the table rebuilt on the refit ${REFIT:0:12} ($o) equals the commit's $rel byte for byte,"
         echo "and the two commits differ only in the rarity files:"; git -C $REPO diff --name-only $REFIT $SHA; echo "RARITY-SAME"; } > $rep
       python3 -B $R/results.py add $ID PASS $rep "rebuilt on the refit ${REFIT:0:12}; nothing it reads changed since"
     else echo "the refit and the final commit differ beyond the rarity files, or the table differs: rebuilding"; $CHK --only $ID; fi
     if [ -z "$moved" ]; then carry $REFIT $HAND; else echo "page layer: run \`run.sh page\` on a free machine"; fi ;;
  final_game) $CHK --only $GAME; $CHK --only @steered ;;
  page) look ;;
  b7AB) b7 A,B ;;
  b7CD) b7 C,D ;;
  *) sed -n 2,28p "$0"; exit 2 ;;
esac
