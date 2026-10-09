#!/bin/bash
# v22.2 release record (stage 1 alone; records/v22.2/scope.md): one job per machine, run from anywhere. Every result lands
# in chroma-release/out/ with the commit below, which is what record.py counts. Scratch under /tmp.
#   bash /mnt/project-files/chroma-release/short-v22.2/run.sh <job>
# Jobs (about 4 cores each):
#   same1 same2 same3 same4   the same-lives proof, one part each (S1; about 50 minutes), on the commit's engine, Library, packs
#   steered                   the ten steered and Voice rows, one lives cache (S2, S3; about 35-45 minutes)
#   steer_identity steer_apart steer_rest   the same split over three machines (the Game's split)
#   rows                      every other v22_checks row of the bar (S4 to S10)
#   b7AB b7CD                 the build of the commit, then the game's browser drivers, groups A and B or C and D (S11)
set -u
SHA=${SHA:-ea5aaf0bc70b0c2272e5e10761786d3cd6e39d6c}
F=/mnt/project-files; R=$F/chroma-release; REPO=${REPO:-/tmp/v222_repo}; X=/tmp/v222_$1
[ -d $REPO/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype $REPO || exit 2
git -C $REPO cat-file -e $SHA^{commit} 2>/dev/null || git -C $REPO fetch -q origin main || exit 2
export CHROMA_COMMIT=$SHA
CHK="python3 -B $R/v22_checks.py --repo $REPO --commit $SHA"
STEER_REST=alone_names,push_rare,world_lines,voice_quiet,voice_careful,voice_trust,voice_lines,voice_year
ROWS=pin,content,packrules,identity1,t_steps,build_earth,build_packs,balance,setting,voice,perks,pack_check,pack_stats,pack_balance
ROWS=$ROWS,icons,build,fuzz,markers,saveload,saveload_world,end_at_choice,identity_g,peace_bands,acceptance,longshot_check
ROWS=$ROWS,event_rate,season_rate,roles2,roles_g,book_check,timeless,next2_check,life_ends,season_ages,kin,abroad,art,rarity,saves_note
export_commit() { rm -rf $X; mkdir -p $X; git -C $REPO archive $SHA chroma-engine/v22-speedpass chroma-library chroma-packs | tar -x -C $X; }
case "$1" in
  same[1-4]) export_commit
     NEW=$X/chroma-engine/v22-speedpass LIB=$X/chroma-library PACKS=$X/chroma-packs COMMIT=$SHA bash $R/same-lives.sh ${1#same} ;;
  steered) $CHK --only @steered ;;
  steer_identity|steer_apart) $CHK --only $1 ;;
  steer_rest) $CHK --only $STEER_REST ;;
  rows) $CHK --only $ROWS ;;
  b7AB|b7CD) rm -rf $X; $CHK --only build --keep --work $X || exit 1
     g=${1#b7}; bash $R/short-v22.1/b7.sh ${g:0:1},${g:1:1} 2 $X/w/build ;;
  *) sed -n 2,10p "$0"; exit 2 ;;
esac
