#!/bin/bash
# v22.1 same-lives proof, short plan (coordinator 10-08 12:03 UTC, for Emren's choice): one part per machine, run from
# anywhere; reports land in chroma-release/out/ (speedpass_*_<tag>.txt, v22checks_*); scratch under /tmp. One job after another.
cd /mnt/project-files || exit 1
SP="python3 -B chroma-release/check_speedpass.py --new /mnt/project-files/chroma-engine/v22-speedpass --games \"\" --timing 0"
# part 1: seed 41 at the proof bar's size; then the setup sweeps A and B (history pace, technology, climate), world on
eval $SP --seeds 41 --lives 400 --years 100 --worlds off,on,seed --scratch /tmp/sp41
P='{"world_cfg": {"setting": "earth", "pace": 2.0, "tech_level": "behind", "climate": "high"}}'
eval $SP --seeds 7 --lives 100 --years 100 --worlds on --tag sweepA --scratch /tmp/spA --Pnew "'$P'" --Pbase "'$P'"
P='{"world_cfg": {"setting": "earth", "pace": 0.5, "tech_level": "ahead", "climate": "low"}}'
eval $SP --seeds 7 --lives 100 --years 100 --worlds on --tag sweepB --scratch /tmp/spB --Pnew "'$P'" --Pbase "'$P'"
echo "PART 1 DONE $(date -u +%H:%M:%S)"
