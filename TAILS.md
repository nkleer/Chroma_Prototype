# The final wave on Emren's PC: console tails (feature/v25 87caab7bd2749f913cd8b51357c666921dde515c, K3 on e111d9850912e8c47b12c77d46f0ecb171796dd0)

Machine: i9-13900HX, WSL2, 24 GB, Python 3.13.16, numpy 2.5.3, no AVX-512. run.sh jobs: /mnt/project-files (CHROMA_PROJECT
unset), NOPROBE=1, REPO ~/chroma/wt/bcb1017-clone, ~/chroma/venv-ship (out/v25/ship_hook loads). K3 = v22_checks --only
t_steps,identity1 run directly (run.sh refuses engA), original venv. MF, WO, LN, land: original venv. Batch: batch 5: K4 parts 1-4 on e111d98 (all PASS)

- K4 114faf0: k4p2 start 2026-10-24T08:25:19Z end 2026-10-24T08:25:20Z exit 2  [the twin launch by the stopped scheduler; the other twin stopped too, rerun clean]
- K4 114faf0: k4p1 start 2026-10-24T08:24:59Z end 2026-10-24T09:43:20Z exit 0
- K4 114faf0: k4p4 start 2026-10-24T08:25:59Z end 2026-10-24T09:44:11Z exit 0
- K4 114faf0: k4p2 start 2026-10-24T08:26:20Z end 2026-10-24T09:44:33Z exit 1
- K4 114faf0: k4p3 start 2026-10-24T08:25:39Z end 2026-10-24T10:22:00Z exit 1
- K4 e111d98: k4p1 start 2026-10-24T10:50:32Z end 2026-10-24T11:41:09Z exit 0
- K4 e111d98: k4p2 start 2026-10-24T10:51:02Z end 2026-10-24T11:42:11Z exit 0
- K4 e111d98: k4p3 start 2026-10-24T10:51:32Z end 2026-10-24T11:42:25Z exit 0
- K4 e111d98: k4p4 start 2026-10-24T10:52:13Z end 2026-10-24T11:42:44Z exit 0
- memory: orphans of the 225679d previews (s7 lead_check x5, mech fair_check; own sessions, so the group kill at 08:24 missed them) killed 2026-10-24T09:35:47Z
- memory: w:f8a STOPPED 2026-10-24T10:12:13Z for memory (available 984 MB), back at the head
- memory: WSL restarted about 10:23Z: K3 t_steps (from 09:44:40Z), f9a (from 08:52:16Z), LA/NR1 87caab7 (from 08:52:18Z) ended unfinished; partials in /home/emren/chroma/jobs/final/killed_1023
- memory: w:f9a STOPPED 2026-10-24T10:50:03Z on Release's order (K3 and K4 first), requeued after K4

