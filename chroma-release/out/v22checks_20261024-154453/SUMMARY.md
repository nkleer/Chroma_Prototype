# v22 checks, 20261024-154453 UTC

Level quick; candidate: engine /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-engine/v22-speedpass, game /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-game/prototype, lib /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-library, packs /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-packs; commit 65ecdf9193b9 (65ecdf9193b9ef9d0045426cb8a78e66f90a09aa) of /home/emren/chroma/wt/65ecdf9-clone; 169 minutes on up to 4 cores.

| Check | Row | Owner | Result | Time | What | Note |
|---|---|---|---|---|---|---|
| identity1 | C-E14 | Release | PASS | 7.0 min | engine.GOLIVE lives the go-live engine's lives (engine_v9_golive.py), 10 lives, seed 5, on the go-live packs (art joins at v22.4 and names titles the v21 batch lacks) |  |
| t_steps | item 2 | Engine | FAIL | 168.9 min | run_steps() lives run()'s lives bit for bit, pauses in PAUSES order, every STATE name at every pause (3 short runs); when chroma-engine/tools/t_steps.py is there and the engine has run_steps() | exit 1: 1 FAILED |

PASS 1, RAN 0 (no reference to compare), MISS 0, FAIL 1 of 2
