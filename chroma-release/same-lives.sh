#!/bin/bash
# The same-lives proof for an engine change that must keep every life with no player identical to the live game (Emren's
# card "Same-lives proof", 2026-10-08 12:04 UTC; how v22.1 ran it: notes/checklist-v22.1.md, B2). Old engine against new,
# byte for byte: 1,600 lives over four seeds (41 to 44, 400 lives x 100 years; world off, on and the seed library) and four
# setup sweeps of 100 lives. Four parts, one per machine, side by side (about 50 minutes each).
#
#   NEW=<engine dir> [BASE=<engine dir>] [COMMIT=<sha>] bash chroma-release/same-lives.sh <part 1 to 4>
#
# BASE: default the live engine (paths.py "engine_live" in the shared folder). The Library and packs are the shared
# folder's live ones for both engines. COMMIT: the repository commit NEW comes from, kept with each result. Played game
# lives are not compared (they may change by design); check_speedpass.py --game does that when they must not. Reports:
# chroma-release/out/speedpass_<UTC>_<tag>.txt; each run adds a "speedpass" line to out/results.jsonl. Exit code 0 when
# every run of the part is identical. LIVES and YEARS shrink the seed runs for a trial.
[ -n "$NEW" ] && [ -f "$NEW/engine.py" ] || { echo "NEW=<engine dir holding engine.py> is needed"; exit 2; }
NEW=$(cd "$NEW" && pwd)
cd "${CHROMA_PROJECT:-/mnt/project-files}" || exit 2
export CHROMA_COMMIT=${COMMIT:-}
SP=(python3 -B chroma-release/check_speedpass.py --new "$NEW" --games "" --timing 0)
[ -n "$BASE" ] && SP+=(--base "$BASE")
N=${LIVES:-400}; Y=${YEARS:-100}; rc=0
seed() { "${SP[@]}" --seeds "$1" --lives "$N" --years "$Y" --worlds off,on,seed --tag "s$1" --scratch "/tmp/sl$1" || rc=1; }
sweep() { "${SP[@]}" --seeds 7 --lives "${LIVES:-100}" --years "$Y" --worlds "$2" --tag "sweep$1" --scratch "/tmp/sl$1" --Pnew "$3" --Pbase "$3" || rc=1; }
case "$1" in
  1) seed 41
     sweep A on '{"world_cfg": {"setting": "earth", "pace": 2.0, "tech_level": "behind", "climate": "high"}}'
     sweep B on '{"world_cfg": {"setting": "earth", "pace": 0.5, "tech_level": "ahead", "climate": "low"}}' ;;
  2) seed 42
     sweep C on '{"self_death": true, "framing": "pie", "faith_inherit": 1.0, "res0": [0.9, 1.0, 0.95, 0.4, 0.2], "sex": "female"}'
     sweep D off,seed '{"self_death": true, "framing": "neutral", "faith_inherit": 0.0, "res0": [0.05, 1.0, 0.95, 0.4, 0.2], "sex": "male"}' ;;
  3) seed 43 ;;
  4) seed 44 ;;
  *) echo "part 1, 2, 3 or 4"; exit 2 ;;
esac
echo "SAME-LIVES PART $1 $([ $rc = 0 ] && echo PASS || echo FAIL) $(date -u +%H:%M:%S) UTC; new $NEW"
exit $rc
