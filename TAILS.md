# The final wave on Emren's PC: console tails (feature/v25 326a0f9b6d967a75c717070f92d1563786cd4ead, K3 on 326a0f9b6d967a75c717070f92d1563786cd4ead)

Machine: i9-13900HX, WSL2, 24 GB, Python 3.13.16, numpy 2.5.3, no AVX-512. run.sh jobs: /mnt/project-files (CHROMA_PROJECT
unset), NOPROBE=1, REPO ~/chroma/wt/bcb1017-clone, ~/chroma/venv-ship (out/v25/ship_hook loads). K3 = v22_checks --only
t_steps,identity1 run directly (run.sh refuses engA), original venv. MF, WO, LN, land: original venv. Batch: batch 7: LA (41-44) and NR1 (41-42) on 326a0f9, their md5s and violations, and the ledger judge

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

## wo

start 2026-10-24T12:55:27Z, end 2026-10-24T13:24:49Z, exit 0

(no ship_hook line: not a hook job)

```
seed 41: calm largest mean drift 0.080 {'field': 0.0232, 'wood': 0.0796, 'water': 0.0159} (one town at most {'field': 0.1243, 'wood': 0.3417, 'water': 0.1495}); high extremes fall field +0.157 water +0.155; extremes [1.739, 1.739] / [1.818, 4.135]; [215, 220] s
seed 42: calm largest mean drift 0.062 {'field': 0.0269, 'wood': 0.0622, 'water': 0.0476} (one town at most {'field': 0.1239, 'wood': 0.3471, 'water': 0.2192}); high extremes fall field +0.138 water +0.129; extremes [1.739, 1.739] / [1.818, 4.135]; [221, 233] s
seed 43: calm largest mean drift 0.070 {'field': 0.0242, 'wood': 0.0697, 'water': 0.0308} (one town at most {'field': 0.164, 'wood': 0.2842, 'water': 0.2044}); high extremes fall field +0.155 water +0.143; extremes [1.739, 1.739] / [1.818, 4.135]; [208, 213] s
seed 44: calm largest mean drift 0.085 {'field': 0.0271, 'wood': 0.0846, 'water': 0.0283} (one town at most {'field': 0.1079, 'wood': 0.5536, 'water': 0.1473}); high extremes fall field +0.163 water +0.158; extremes [1.739, 1.739] / [1.818, 4.135]; [212, 232] s
LN2 calm: largest mean drift 0.085 (<= 0.15) ok
LN2 high extremes: mean fall field 0.153, water 0.146 (0.05 to 0.2) ok
LN2 pass
wrote /mnt/project-files/chroma-release/out/v25/pc_final_326a0f9/wo/land_alone.json
```

## f8a

start 2026-10-24T12:53:57Z, end 2026-10-24T13:58:54Z, exit 1

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8a.log)

```
v25 f8a on 326a0f9b6d967a75c717070f92d1563786cd4ead
f8_after (K9), 2026-10-24 12:53 UTC; repo /tmp/v25_f8a/tree, commit 326a0f9b6d967a75c717070f92d1563786cd4ead (--as-is); the game plays a pin filled from engine /tmp/v25_f8a/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8a/tree/chroma-library, packs /tmp/v25_f8a/tree/chroma-packs
engine lives: 1200 (seeds 41-44 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
FAIL F8.1 work moments after retiring, lives that did not go back: 13144 weeks in 230 lives (target 0)
       age 56.69: the rival drawing the newcomers away
       age 57.69: the rival's plan for the whole sphere
       age 58.31: the market square's trading hours
       age 58.48: the rival who wants the town's backing
FAIL F8.2 work moments in a week retired and not working, any life: 16039 weeks (target 0)
       age 56.69: the rival drawing the newcomers away
       age 57.0: the ally who cannot back this one
       age 57.17: the fate of the old mill
       age 57.27: the fate of the old mill
     reported: lives that retired 1143; went back to work after retiring 261; jobs taken while retired without a career pick that week (a title or another path) 12
     moments: the credit union's loans to small traders (1950); the shop's pay and the lean year (1917); the market square's trading hours (1874); the empty shop on the high street (1844); the rival drawing the newcomers away (913); the rival's plan for the whole sphere (895); the rival who wants the town's backing (893); the low fields by the river (683); hiring at the workshop (607); the new machines at the works (596)
f8_after: FAIL (3897 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8a.log)
```

## f8b

start 2026-10-24T12:54:27Z, end 2026-10-24T13:59:42Z, exit 1

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8b.log)

```
v25 f8b on 326a0f9b6d967a75c717070f92d1563786cd4ead
f8_after (K9), 2026-10-24 12:54 UTC; repo /tmp/v25_f8b/tree, commit 326a0f9b6d967a75c717070f92d1563786cd4ead (--as-is); the game plays a pin filled from engine /tmp/v25_f8b/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8b/tree/chroma-library, packs /tmp/v25_f8b/tree/chroma-packs
engine lives: 1200 (seeds 45-48 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
FAIL F8.1 work moments after retiring, lives that did not go back: 13937 weeks in 250 lives (target 0)
       age 56.31: the credit union's loans to small traders
       age 56.35: the shop's pay and the lean year
       age 56.37: the shop's pay and the lean year
       age 56.38: the empty shop on the high street
FAIL F8.2 work moments in a week retired and not working, any life: 17273 weeks (target 0)
       age 54.73: the new machines at the works
       age 55.04: hiring at the workshop
       age 55.23: the fate of the old mill
       age 55.42: the fate of the old mill
     reported: lives that retired 1146; went back to work after retiring 301; jobs taken while retired without a career pick that week (a title or another path) 11
     moments: the empty shop on the high street (1880); the credit union's loans to small traders (1848); the shop's pay and the lean year (1847); the market square's trading hours (1828); the rival drawing the newcomers away (935); the rival who wants the town's backing (928); the rival's plan for the whole sphere (927); what the book about the town will say (773); what the town theatre stages next season (743); who gets the arts fund's money this year (734)
f8_after: FAIL (3914 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8b.log)
```

## f8c

start 2026-10-24T12:54:57Z, end 2026-10-24T14:00:31Z, exit 1

ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8c.log)

```
v25 f8c on 326a0f9b6d967a75c717070f92d1563786cd4ead
f8_after (K9), 2026-10-24 12:54 UTC; repo /tmp/v25_f8c/tree, commit 326a0f9b6d967a75c717070f92d1563786cd4ead (--as-is); the game plays a pin filled from engine /tmp/v25_f8c/tree/chroma-engine/v22-speedpass, lib /tmp/v25_f8c/tree/chroma-library, packs /tmp/v25_f8c/tree/chroma-packs
engine lives: 1200 (seeds 49-52 x 300 lives x 100 years; Earth with the packs, world on); as DEFAULT has them (--as-is)
FAIL F8.1 work moments after retiring, lives that did not go back: 11902 weeks in 258 lives (target 0)
       age 54.71: the empty shop on the high street
       age 54.73: the empty shop on the high street
       age 55.46: the market square's trading hours
       age 55.48: the shop's pay and the lean year
FAIL F8.2 work moments in a week retired and not working, any life: 14709 weeks (target 0)
       age 54.71: the empty shop on the high street
       age 54.73: the empty shop on the high street
       age 55.46: the market square's trading hours
       age 55.48: the shop's pay and the lean year
     reported: lives that retired 1153; went back to work after retiring 250; jobs taken while retired without a career pick that week (a title or another path) 18
     moments: the empty shop on the high street (1616); the shop's pay and the lean year (1546); the credit union's loans to small traders (1534); the market square's trading hours (1532); the rival drawing the newcomers away (804); the rival who wants the town's backing (795); the rival's plan for the whole sphere (788); who gets the arts fund's money this year (676); what the book about the town will say (650); what the town theatre stages next season (647)
f8_after: FAIL (3933 s)
ship_hook: 8 patches in 4 processes (/tmp/v25_ship_f8c.log)
```

