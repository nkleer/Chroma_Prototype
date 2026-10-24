# The final wave on Emren's PC: console tails (feature/v25 87caab7bd2749f913cd8b51357c666921dde515c, K3 on 5287a434fdfc9e5bdb018360294bdf67ba929e8c)

Machine: i9-13900HX, WSL2, 24 GB, Python 3.13.16, numpy 2.5.3, no AVX-512. run.sh jobs: /mnt/project-files (CHROMA_PROJECT
unset), NOPROBE=1, REPO ~/chroma/wt/bcb1017-clone, ~/chroma/venv-ship (out/v25/ship_hook loads). K3 = v22_checks --only
t_steps,identity1 run directly (run.sh refuses engA), original venv. MF, WO, LN, land: original venv. Batch: batch 2: K4 part 3 on 114faf0; K3 (5287a43) killed at 10:23Z as diagnostics

- K4 114faf0: k4p2 start 2026-10-24T08:25:19Z end 2026-10-24T08:25:20Z exit 2  [the twin launch by the stopped scheduler; the other twin stopped too, rerun clean]
- K4 114faf0: k4p1 start 2026-10-24T08:24:59Z end 2026-10-24T09:43:20Z exit 0
- K4 114faf0: k4p4 start 2026-10-24T08:25:59Z end 2026-10-24T09:44:11Z exit 0
- K4 114faf0: k4p2 start 2026-10-24T08:26:20Z end 2026-10-24T09:44:33Z exit 1
- K4 114faf0: k4p3 start 2026-10-24T08:25:39Z end 2026-10-24T10:22:00Z exit 1
- memory: orphans of the 225679d previews (s7 lead_check x5, mech fair_check; own sessions, so the group kill at 08:24 missed them) killed 2026-10-24T09:35:47Z
- memory: w:f8a STOPPED 2026-10-24T10:12:13Z for memory (available 984 MB), back at the head
- memory: WSL restarted about 10:23Z: K3 t_steps (from 09:44:40Z), f9a (from 08:52:16Z), LA/NR1 87caab7 (from 08:52:18Z) ended unfinished; partials in /home/emren/chroma/jobs/final/killed_1023

