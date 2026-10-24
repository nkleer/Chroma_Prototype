#!/bin/bash
# v22.1 same-lives proof, short plan (coordinator 10-08 12:03 UTC, for Emren's choice): one part per machine, run from
# anywhere; reports land in chroma-release/out/ (speedpass_*_<tag>.txt, v22checks_*); scratch under /tmp. One job after another.
cd /mnt/project-files || exit 1
SP="python3 -B chroma-release/check_speedpass.py --new /mnt/project-files/chroma-engine/v22-speedpass --games \"\" --timing 0"
# part 4 (the release thread's machine, beside the browser checks B4, B5, B7): seed 44 at the proof bar's size
eval $SP --seeds 44 --lives 400 --years 100 --worlds off,on,seed --scratch /tmp/sp44
echo "PART 4 DONE $(date -u +%H:%M:%S)"
