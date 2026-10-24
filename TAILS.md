# The final wave on Emren's PC: console tails (feature/v25 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa, K3 on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa)

Machine: i9-13900HX, WSL2, 24 GB, Python 3.13.16, numpy 2.5.3, no AVX-512. run.sh jobs: /mnt/project-files (CHROMA_PROJECT
unset), NOPROBE=1, REPO ~/chroma/wt/bcb1017-clone, ~/chroma/venv-ship (out/v25/ship_hook loads). K3 = v22_checks --only
t_steps,identity1 run directly (run.sh refuses engA), original venv. MF, WO, LN, land: original venv. Batch: batch 10: K3 on 65ecdf9 (t_steps 1 FAIL, identity1 PASS); wave 1 c26b, fit4

- K4 114faf0: k4p2 start 2026-10-24T08:25:19Z end 2026-10-24T08:25:20Z exit 2  [the twin launch by the stopped scheduler; the other twin stopped too, rerun clean]
- K4 114faf0: k4p1 start 2026-10-24T08:24:59Z end 2026-10-24T09:43:20Z exit 0
- K4 114faf0: k4p4 start 2026-10-24T08:25:59Z end 2026-10-24T09:44:11Z exit 0
- K4 114faf0: k4p2 start 2026-10-24T08:26:20Z end 2026-10-24T09:44:33Z exit 1
- K4 114faf0: k4p3 start 2026-10-24T08:25:39Z end 2026-10-24T10:22:00Z exit 1
- memory: orphans of the 225679d previews (s7 lead_check x5, mech fair_check; own sessions, so the group kill at 08:24 missed them) killed 2026-10-24T09:35:47Z
- memory: w:f8a STOPPED 2026-10-24T10:12:13Z for memory (available 984 MB), back at the head
- memory: WSL restarted about 10:23Z: K3 t_steps (from 09:44:40Z), f9a (from 08:52:16Z), LA/NR1 87caab7 (from 08:52:18Z) ended unfinished; partials in /home/emren/chroma/jobs/final/killed_1023
- memory: w:f9a STOPPED 2026-10-24T10:50:03Z on Release's order (K3 and K4 first), requeued after K4
- memory: hold 2026-10-24T12:23:10Z: no new 87caab7 job until Release says what reruns on d12881c
- memory: 2026-10-24T12:28:54Z stopped (obsolete, Release 12:28): land, wa, waoff, f8a, f8b on 87caab7; K3 on e111d98
- memory: hold lifted 2026-10-24T12:29:05Z
- memory: 2026-10-24T12:38:08Z stopped everything on d12881c (Release 12:37: CL1 fix coming)
- memory: 2026-10-24T15:44:02Z stopped every 326a0f9 run (Release: freeze is 65ecdf9)

## wo

start 2026-10-24T15:46:54Z, end 2026-10-24T16:18:47Z, exit 0

(no ship_hook line: not a hook job)

```
seed 41: calm largest mean drift 0.080 {'field': 0.0232, 'wood': 0.0796, 'water': 0.0159} (one town at most {'field': 0.1243, 'wood': 0.3417, 'water': 0.1495}); high extremes fall field +0.157 water +0.155; extremes [1.739, 1.739] / [1.818, 4.135]; [246, 264] s
seed 42: calm largest mean drift 0.062 {'field': 0.0269, 'wood': 0.0622, 'water': 0.0476} (one town at most {'field': 0.1239, 'wood': 0.3471, 'water': 0.2192}); high extremes fall field +0.138 water +0.129; extremes [1.739, 1.739] / [1.818, 4.135]; [255, 268] s
seed 43: calm largest mean drift 0.070 {'field': 0.0242, 'wood': 0.0697, 'water': 0.0308} (one town at most {'field': 0.164, 'wood': 0.2842, 'water': 0.2044}); high extremes fall field +0.155 water +0.143; extremes [1.739, 1.739] / [1.818, 4.135]; [216, 212] s
seed 44: calm largest mean drift 0.085 {'field': 0.0271, 'wood': 0.0846, 'water': 0.0283} (one town at most {'field': 0.1079, 'wood': 0.5536, 'water': 0.1473}); high extremes fall field +0.163 water +0.158; extremes [1.739, 1.739] / [1.818, 4.135]; [216, 227] s
LN2 calm: largest mean drift 0.085 (<= 0.15) ok
LN2 high extremes: mean fall field 0.153, water 0.146 (0.05 to 0.2) ok
LN2 pass
wrote /mnt/project-files/chroma-release/out/v25/pc_final_65ecdf9/wo/land_alone.json
```

## f8a

start 2026-10-24T15:45:23Z, end 2026-10-24T16:54:27Z, exit 0

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8a.log)

```
v25 f8a on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa
f8_after (K9), 2026-10-24 15:45 UTC; repo /tmp/v25_f8a/tree, commit 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa (--as-is); the game plays a pin filled from engine /tmp/v25_f8a/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8a/tree/chroma-library, packs /tmp/v25_f8a/tree/chroma-packs
engine lives: 1200 (seeds 41-44 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
ok   F8.1 work moments after retiring, lives that did not go back: 0 weeks in 0 lives (target 0)
ok   F8.2 work moments in a week retired and not working, any life: 0 weeks (target 0)
     reported: lives that retired 1175; went back to work after retiring 326; jobs taken while retired without a career pick that week (a title or another path) 12
f8_after: PASS (4143 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8a.log)
```

## f8b

start 2026-10-24T15:45:53Z, end 2026-10-24T16:54:49Z, exit 0

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8b.log)

```
v25 f8b on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa
f8_after (K9), 2026-10-24 15:45 UTC; repo /tmp/v25_f8b/tree, commit 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa (--as-is); the game plays a pin filled from engine /tmp/v25_f8b/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8b/tree/chroma-library, packs /tmp/v25_f8b/tree/chroma-packs
engine lives: 1200 (seeds 45-48 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
ok   F8.1 work moments after retiring, lives that did not go back: 0 weeks in 0 lives (target 0)
ok   F8.2 work moments in a week retired and not working, any life: 0 weeks (target 0)
     reported: lives that retired 1169; went back to work after retiring 337; jobs taken while retired without a career pick that week (a title or another path) 14
f8_after: PASS (4135 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8b.log)
```

## f8c

start 2026-10-24T15:46:23Z, end 2026-10-24T16:55:15Z, exit 0

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8c.log)

```
v25 f8c on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa
f8_after (K9), 2026-10-24 15:46 UTC; repo /tmp/v25_f8c/tree, commit 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa (--as-is); the game plays a pin filled from engine /tmp/v25_f8c/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8c/tree/chroma-library, packs /tmp/v25_f8c/tree/chroma-packs
engine lives: 1200 (seeds 49-52 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
ok   F8.1 work moments after retiring, lives that did not go back: 0 weeks in 0 lives (target 0)
ok   F8.2 work moments in a week retired and not working, any life: 0 weeks (target 0)
     reported: lives that retired 1152; went back to work after retiring 333; jobs taken while retired without a career pick that week (a title or another path) 9
f8_after: PASS (4130 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8c.log)
```

## c26b

start 2026-10-24T17:11:54Z, end 2026-10-24T17:54:05Z, exit 0

ship_hook: 5 patches in 3 processes (/tmp/v25_ship_c26b.log)

```
v25 c26b on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa
v22 checks, 20261024-171154 UTC, level quick, 1 checks, up to 4 cores; run folder /mnt/project-files/chroma-release/out/v22checks_20261024-171154
  engine /tmp/v25_keep/c26-commit/65ecdf9193b9/chroma-engine/v22-speedpass   (candidate)
  game   /tmp/v25_keep/c26-commit/65ecdf9193b9/chroma-game/prototype   (candidate)
  lib    /tmp/v25_keep/c26-commit/65ecdf9193b9/chroma-library   (candidate)
  packs  /tmp/v25_keep/c26-commit/65ecdf9193b9/chroma-packs   (candidate)
  the Engine's rows run from chroma-engine/tools
  the tree's game plays a pin filled from engine <T>/chroma-engine/v22-speedpass, lib <T>/chroma-library, packs <T>/chroma-packs
  work tree /tmp/v25_keep/c26/tree: 13 copied scripts re-pointed to it; engine.py 594b1a452f94, game.py 3d3df6268005, earth.py 6ef7d4e606df
  packs the engine plays: science,politics,stage,art,callings
  start c26_world (G19w, Engine)
  PASS c26_world (G19w) in 2529s  [proof: 138 files]
PASS 1, RAN 0 (no reference to compare), MISS 0, FAIL 0 of 1
summary: /mnt/project-files/chroma-release/out/v22checks_20261024-171154/SUMMARY.md
ship_hook: 5 patches in 3 processes (/tmp/v25_ship_c26b.log)
```

## fit4

start 2026-10-24T17:54:12Z, end 2026-10-24T18:29:51Z, exit 0

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_fit4.log)

```
v25 fit4 on 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa
f4_age (K17), 2026-10-24 17:54 UTC; repo /tmp/v25_fit4/tree, commit 65ecdf9193b9ef9d0045426cb8a78e66f90a09aa; the game plays a pin filled from engine /tmp/v25_fit4/tree/chroma-engine/v22-speedpass, lib /tmp/v25_fit4/tree/chroma-library, packs /tmp/v25_fit4/tree/chroma-packs
       1200 lives x 50 years, seeds 41, 43, 44, 42; 40 moments with an age fit, 13 child versions shut at 11.99; switched on here: none
  ok   F4.1 no fitted moment before its new start: 0 weeks
  ok   F4.2 no child version at 12 or over: 0 weeks
  ok   F4.3 a child version and its twin never both at 12: 0 lives
       reported, not judged: other moments outside their age window (weeks): reconsidering a commitment 8177; the company is short of hands for the spring show 314; the residents' club needs hands for the street fair 261; the elders ask for Saturday mornings at the shared meal 161; the credit union's loans to small traders 121; who may join the residents' club 75; what the movement asks of the council about the empty shops 71; what the tenants' movement asks for 68; the planting scheme 65; the festival in the square 62; the traders ask for spring fair Saturdays 58; the mural on the market wall 54; the fate of the old mill 38; the bill on recalling officials 33; the empty shop on the high street 32
f4_age: PASS (2138 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_fit4.log)
```

## enga

start 2026-10-24T15:44:53Z, end 2026-10-24T18:33:50Z, exit 1

(no ship_hook line: not a hook job)

```
v22 checks, 20261024-154453 UTC, level quick, 2 checks, up to 4 cores; run folder /mnt/project-files/chroma-release/out/v22checks_20261024-154453
  engine /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-engine/v22-speedpass   (candidate)
  game   /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-game/prototype   (candidate)
  lib    /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-library   (candidate)
  packs  /tmp/v22checks_20261024-154453-commit/65ecdf9193b9/chroma-packs   (candidate)
  the Engine's rows run from chroma-engine/tools
  the tree's game plays a pin filled from engine <T>/chroma-engine/v22-speedpass, lib <T>/chroma-library, packs <T>/chroma-packs
  work tree /tmp/v22checks_20261024-154453/tree: 13 copied scripts re-pointed to it; engine.py 594b1a452f94, game.py 3d3df6268005, earth.py 6ef7d4e606df
  packs the engine plays: science,politics,stage,art,callings
  start identity1 (C-E14, Release): no earlier proof
  start t_steps (item 2, Engine): no earlier proof
  PASS identity1 (C-E14) in 420s  [proof: 56 files]
  FAIL t_steps (item 2) in 10135s exit 1: 1 FAILED
PASS 1, RAN 0 (no reference to compare), MISS 0, FAIL 1 of 2
summary: /mnt/project-files/chroma-release/out/v22checks_20261024-154453/SUMMARY.md
```

