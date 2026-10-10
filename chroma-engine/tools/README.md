# chroma-engine/tools: the Engine's checks

The scripts Release's checks run (chroma-release/v22_checks.py rows C-E1 to C-E15, C-X5, E5; check_world.py;
check_identity.py), moved here from the calibration folders `prototype/calib_v7`, `calib_v8`, `calib_v10` and the
prototype's top (backend plan item 7, 2026-10-08). Each one is the same script with only the lines that find the engine,
the Library and the output folder changed: they all `import _engine`.

- **Which engine:** `CHROMA_ENGINE=<folder>`; default the engine of the tree this folder sits in
  (`chroma-env/paths.py` "engine_live"). Library and packs: the tree's "library_live" and "packs_live", unless a tool's
  arguments or `LIB`, `PACKS`, `PACK_DIR`, `FINAL_LIB` say otherwise, as before.
- **Where files go:** a path the tool is given (`FIT_OUT`, `OUT`, an argument), else `OUT_DIR`, else the current folder.
  Run outputs belong in the shared folder's `chroma-engine/runs/<date>/`, never in the repository.
- **Run from anywhere:** `python3 -B chroma-engine/tools/<tool>.py ...`. `cx2run.py <tool> ...` runs a tool on a given
  batch (`FINAL_LIB`, `NOPACKS=1`, `PX='{json}'` laid over the defaults); it still accepts the old `calib_v8/<tool>.py`.

| Tool | Release row | What it checks |
|---|---|---|
| t_steps.py | Engine fast check | run_steps() gives run()'s lives; pause order; every STATE name (about 20 s) |
| score_packs.py | C-E1 | the survey scorecard |
| tier_fit.py | C-E3 | pack careers about 1 in 3, summits about 1 in 20; needs `PACKS=science,politics,stage` (without it, it stops: no pack careers); a fourth argument 1 writes earth_rules.TIER_LIFT, a rate change |
| roles_check.py | C-E4 | titles and perks a life against the catalogue |
| death_check.py | C-E5 | dead by 30, 50, 65, 80 |
| lean_check.py | C-E6, P12 | pack roads' holders lean to their lead colour |
| pie_check.py | C-E6 | the colour pie |
| season_check.py | C-E7 | seasons open; steps |
| repeat_check.py | C-E7 | births, childless |
| chance_check.py | C-E8 | written chance against true odds |
| exits_check.py | C-E9 | at work by age, retiring |
| t_satisf.py | C-E10 | satisfaction U-shape |
| inertia_check.py | C-E10 | turning years move more |
| goals_check.py | C-E11 | dreams, harmony, passions |
| felt_gap.py, plan_felt.py, accept_check.py | C-E12 | felt odds against true; plans; acceptance words |
| foresee_table.py | E5 | the foresee hint |
| rarity_build.py | C-E13 | the Book's rarity table (compare with the engine's rarity.json) |
| speed_check.py | C-E15 | time per life, world off and on; its `v9` run needs the go-live rules and Library (as identity_check) |
| identity_check.py, engine_v9_golive.py | C-E14 | today's engine lives the go-live engine's lives (v9 frozen here). The go-live engine cannot read today's Library: run it with `RULES=<folder holding the v21 game's engine_pin/earth_rules.py>` on a tree whose chroma-library is the v21 batch (paths.py "library_v21"); Release's check_identity.py does both with `--rules` and `--lib` |
| child_deaths.py | C-X5 | a child's death and illness among parents |
| world_check.py, people_check.py, world_starts.py, lives_in_worlds.py | C-E16 (check_world.py) | the outer world |
| colour_count.py | DECISIONS.md CHECK | how many colours adults hold, by age |
| eyes_check.py | v22.4 G7, G8 | S3/S4 colour-even targets with sph_eyes and sph_odd on: `s3_rep`, `s3_caught`, `s4_odd`, `s4_convert` (or `all`); `--stats FILE` lets the four share one run |

The calibration folders these scripts came from (their outputs and the one-off fitting scripts) are kept unchanged in
the shared folder: in `chroma-engine/prototype/` until Release's checks run from here, then under
`_archive/2026-10-08/chroma-engine/prototype/` at the same relative paths (code comments that cite `calib_vN/...` still
find them there).
