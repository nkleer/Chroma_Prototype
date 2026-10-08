#!/bin/bash
# v22.1 same-lives proof, short plan (coordinator 10-08 12:03 UTC, for Emren's choice): one part per machine, run from
# anywhere; reports land in chroma-release/out/ (speedpass_*_<tag>.txt, v22checks_*); scratch under /tmp. One job after another.
cd /mnt/project-files || exit 1
SP="python3 -B chroma-release/check_speedpass.py --new /mnt/project-files/chroma-engine/v22-speedpass --games \"\" --timing 0"
# part 3: seed 43 at the proof bar's size; then on the rebuilt v22.1 game (/tmp/v22p1_build/prototype, from
# chroma-game/staging-v22p1/make_tree.sh): the six whole game lives against live v22, and every quick check (old saves included)
G=${G:-/tmp/v22p1_build/prototype}
[ -f "$G/game.py" ] || { echo "no game at $G: run bash /mnt/project-files/chroma-game/staging-v22p1/make_tree.sh /tmp/v22p1_build first"; exit 1; }
eval $SP --seeds 43 --lives 400 --years 100 --worlds off,on,seed --scratch /tmp/sp43
python3 -B chroma-release/check_speedpass.py --new /mnt/project-files/chroma-engine/v22-speedpass --seeds "" --timing 0 \
  --base-game /mnt/project-files/chroma-game/prototype --game "$G" --tag build_games --scratch /tmp/spg
python3 -B chroma-release/v22_checks.py --level quick --skip speedpass --engine /mnt/project-files/chroma-engine/v22-speedpass \
  --game "$G" --ref /mnt/project-files/chroma-release/out/v22checks_20261008-105541 --work /tmp/v22q_build
echo "PART 3 DONE $(date -u +%H:%M:%S)"
