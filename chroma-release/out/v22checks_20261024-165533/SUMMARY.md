# v22 checks, 20261024-165533 UTC

Level quick; candidate: engine /tmp/v25_keep/mech-commit/65ecdf9193b9/chroma-engine/v22-speedpass, game /tmp/v25_keep/mech-commit/65ecdf9193b9/chroma-game/prototype, lib /tmp/v25_keep/mech-commit/65ecdf9193b9/chroma-library, packs /tmp/v25_keep/mech-commit/65ecdf9193b9/chroma-packs; commit 65ecdf9193b9 (65ecdf9193b9ef9d0045426cb8a78e66f90a09aa) of /home/emren/chroma/wt/65ecdf9-clone; 110 minutes on up to 4 cores.

| Check | Row | Owner | Result | Time | What | Note |
|---|---|---|---|---|---|---|
| s1_parts | G6 | Engine | PASS | 46.6 min | S1: every sphere carries all five parts (300 lives x 80 years, seed 7, world and fair_read on; its first run makes the stats the other two read) |  |
| s1_counts | G6 | Engine | PASS | 0.1 min | S1: the five parts' event counts within 1.5x |  |
| s1_fair | G6 | Engine | FAIL | 0.1 min | S1: mean fair per lead colour within .03 | exit 1: MISS s1_fair |
| s3_rep | G7 | Engine | PASS | 63.4 min | S3: mean rep change per lead colour within .03 (300 lives x 80 years on each of seeds 7 to 10, one worker a seed; makes the stats the S3 and S4 rows read; scope.md, G7 and G8's run size) |  |
| s3_caught | G7 | Engine | FAIL | 0.1 min | S3: caught-between moments per enemy pair within 1.5x | exit 1: MISS s3_caught |
| s4_odd | G8 | Engine | PASS | 0.1 min | S4: odd-one-out years per lead colour within 1.2x, per year at a place |  |
| s4_convert | G8 | Engine | PASS | 0.1 min | S4: conversions per lead colour within 1.5x, per year a life could move a place (scope.md, S4's conversions) |  |
| s6_felt | G10 | Engine | PASS | 11.9 min | S6: mean felt-odds lift per colour way within .01 (60 lives x 80 years, seed 7) |  |

PASS 6, RAN 0 (no reference to compare), MISS 0, FAIL 2 of 8
