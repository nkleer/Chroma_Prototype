#!/bin/bash
# v22.1 same-lives proof, short plan (coordinator 10-08 12:03 UTC, for Emren's choice): one part per machine, run from
# anywhere; reports land in chroma-release/out/ (speedpass_*_<tag>.txt, v22checks_*); scratch under /tmp. One job after another.
cd /mnt/project-files || exit 1
SP="python3 -B chroma-release/check_speedpass.py --new /mnt/project-files/chroma-engine/v22-speedpass --games \"\" --timing 0"
# part 2: seed 42 at the proof bar's size; then the setup sweeps C and D (own death, framing, faith, wealth, sex)
eval $SP --seeds 42 --lives 400 --years 100 --worlds off,on,seed --scratch /tmp/sp42
P='{"self_death": true, "framing": "pie", "faith_inherit": 1.0, "res0": [0.9, 1.0, 0.95, 0.4, 0.2], "sex": "female"}'
eval $SP --seeds 7 --lives 100 --years 100 --worlds on --tag sweepC --scratch /tmp/spC --Pnew "'$P'" --Pbase "'$P'"
P='{"self_death": true, "framing": "neutral", "faith_inherit": 0.0, "res0": [0.05, 1.0, 0.95, 0.4, 0.2], "sex": "male"}'
eval $SP --seeds 7 --lives 100 --years 100 --worlds off,seed --tag sweepD --scratch /tmp/spD --Pnew "'$P'" --Pbase "'$P'"
echo "PART 2 DONE $(date -u +%H:%M:%S)"
