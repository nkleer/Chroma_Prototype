#!/bin/bash
# The same-lives proof for an engine change that must keep every life with no player identical to the live game (Emren's
# card "Same-lives proof", 2026-10-08 12:04 UTC; how v22.1 ran it: notes/checklist-v22.1.md, B2). Old engine against new,
# byte for byte: 1,600 lives over four seeds (41 to 44, 400 lives x 100 years; world off, on and the seed library) and four
# setup sweeps of 100 lives. Four parts, one per machine, side by side (about 50 minutes each, about 25 once the live
# engine's side is kept: check_speedpass.py keeps a digest of every base run, keyed by the files it reads and its settings).
#
#   NEW=<engine dir> [BASE=<engine dir>] [LIB=<library dir>] [PACKS=<packs dir>] [COMMIT=<sha>] [PNEW=<json>] \
#       bash chroma-release/same-lives.sh <part 1 to 4, or 1s 1A 1B: part 1's seed 41, sweep A, sweep B>
#
# BASE: default the live engine (paths.py "engine_live" in the shared folder); it runs on the shared folder's live
# Library and packs. LIB and PACKS: the Library and packs NEW runs on (default the live ones too); give a candidate
# commit's own chroma-library and chroma-packs, so a Library or packs change that moves lives with no player shows.
# COMMIT: the repository commit NEW comes from, kept with each result. Played game lives are not compared (they may
# change by design); check_speedpass.py --game does that when they must not. Reports:
# chroma-release/out/speedpass_<UTC>_<tag>.txt; each run adds a line to out/results.jsonl under the id speedpass_<tag>
# (speedpass_s41, speedpass_sweepA, ...), the ids a release record's bar names. Exit code 0 when every run of the part is
# identical. LIVES and YEARS shrink the seed runs for a trial. PNEW: switch overrides for NEW only, as JSON (check_speedpass
# --Pnew), for example a candidate's new switches set off so it must equal the live engine (v22.4 G4); each sweep's
# setup is laid over it. FRESH=1 runs the live engine again even where its side is kept. BASE_ONLY=1 (no NEW) runs and
# keeps the live engine's side of the part only, for example right after a publish, so the proofs after it run NEW alone.
if [ -z "$BASE_ONLY" ]; then
  [ -n "$NEW" ] && [ -f "$NEW/engine.py" ] || { echo "NEW=<engine dir holding engine.py> is needed (or BASE_ONLY=1)"; exit 2; }
  NEW=$(cd "$NEW" && pwd)
fi
cd "${CHROMA_PROJECT:-/mnt/project-files}" || exit 2
export CHROMA_COMMIT=${COMMIT:-}
SP=(python3 -B chroma-release/check_speedpass.py --games "" --timing 0)
if [ -n "$BASE_ONLY" ]; then SP+=(--base-only); else SP+=(--new "$NEW"); fi
[ -n "$FRESH" ] && SP+=(--fresh)
[ -n "$BASE" ] && SP+=(--base "$BASE")
for v in LIB PACKS; do [ -n "${!v}" ] && { [ -d "${!v}" ] || { echo "$v=${!v} is not a folder"; exit 2; }; }; done
[ -n "$LIB" ] && SP+=(--new-lib "$(cd "$LIB" && pwd)")
[ -n "$PACKS" ] && SP+=(--new-packs "$(cd "$PACKS" && pwd)")
PN=${PNEW:-"{}"}; python3 -c 'import json,sys; assert isinstance(json.loads(sys.argv[1]), dict)' "$PN" || { echo "PNEW=$PN is not a JSON object"; exit 2; }
pnew() { python3 -c 'import json,sys; p=json.loads(sys.argv[1]); p.update(json.loads(sys.argv[2])); print(json.dumps(p))' "$PN" "$1"; }
N=${LIVES:-400}; Y=${YEARS:-100}; rc=0
seed() { "${SP[@]}" --jobs "${2:-4}" --seeds "$1" --lives "$N" --years "$Y" --worlds off,on,seed --tag "s$1" --scratch "/tmp/sl$1" --Pnew "$PN"; }
sweep() { "${SP[@]}" --jobs "${4:-4}" --seeds 7 --lives "${LIVES:-100}" --years "$Y" --worlds "$2" --tag "sweep$1" --scratch "/tmp/sl$1" --Pnew "$(pnew "$3")" --Pbase "$3"; }
SA='{"world_cfg": {"setting": "earth", "pace": 2.0, "tech_level": "behind", "climate": "high"}}'
SB='{"world_cfg": {"setting": "earth", "pace": 0.5, "tech_level": "ahead", "climate": "low"}}'
SC='{"self_death": true, "framing": "pie", "faith_inherit": 1.0, "res0": [0.9, 1.0, 0.95, 0.4, 0.2], "sex": "female"}'
SD='{"self_death": true, "framing": "neutral", "faith_inherit": 0.0, "res0": [0.05, 1.0, 0.95, 0.4, 0.2], "sex": "male"}'
pids=()
side() { "$@" & pids+=($!); }   # parts 1 and 2: the seed on two cores and each sweep on one, side by side (4 runs at a time)
case "$1" in
  1) side seed 41 2; side sweep A on "$SA" 1; side sweep B on "$SB" 1 ;;
  1s) seed 41 || rc=1 ;;   # 1s, 1A, 1B: part 1's three runs each on its own machine
  1A) sweep A on "$SA" || rc=1 ;;
  1B) sweep B on "$SB" || rc=1 ;;
  2) side seed 42 2; side sweep C on "$SC" 1; side sweep D off,seed "$SD" 1 ;;
  3) seed 43 || rc=1 ;;
  4) seed 44 || rc=1 ;;
  *) echo "part 1 (or 1s, 1A, 1B), 2, 3 or 4"; exit 2 ;;
esac
for p in "${pids[@]}"; do wait "$p" || rc=1; done
if [ -n "$BASE_ONLY" ]; then echo "SAME-LIVES PART $1 BASE SIDE $([ $rc = 0 ] && echo KEPT || echo FAIL) $(date -u +%H:%M:%S) UTC"
else echo "SAME-LIVES PART $1 $([ $rc = 0 ] && echo PASS || echo FAIL) $(date -u +%H:%M:%S) UTC; new $NEW"; fi
exit $rc
