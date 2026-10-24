# W1 on Emren's PC: console tails (feature/v25 225679d46e1c1bd254453760c00f40940857a06c, a preview)

Machine: i9-13900HX, WSL2, Python 3.13.16, numpy 2.5.3, no AVX-512. Wave-1 jobs: /mnt/project-files with CHROMA_PROJECT
unset, REPO ~/chroma/wt/225679d-clone (a plain clone at 225679d), ~/chroma/venv-ship (the same Python and numpy, system
site on, so out/v25/ship_hook's usercustomize loads). Batch: batch 1: step 3 MF and WO, s7 path failure

- step 3: MF start 2026-10-24T07:42:30Z
- step 3: MF end 2026-10-24T07:44:12Z wall 102 s judge rc 0
- step 3: WO start 2026-10-24T07:44:12Z
- step 3: WO end 2026-10-24T07:53:05Z wall 533 s exit 0
- K4 on 225679d: parts 1, 2, 3 started 07:45:31Z, 07:47:32Z, 07:48:02Z, stopped 07:49:49Z on Release's order (no result); part 4 not started

## s7

start 2026-10-24T07:50:20Z, end 2026-10-24T07:50:20Z, exit 1

ship_hook: 0 patches in 0 processes (/tmp/v25_ship_s7.log)

```
v25 s7 on 225679d46e1c1bd254453760c00f40940857a06c
v22 checks, 20261024-075020 UTC, level quick, 1 checks, up to 4 cores; run folder /mnt/project-files/chroma-release/out/v22checks_20261024-075020
  engine /tmp/v22checks_20261024-075020-commit/225679d46e1c/chroma-engine/v22-speedpass   (candidate)
  game   /tmp/v22checks_20261024-075020-commit/225679d46e1c/chroma-game/prototype   (candidate)
  lib    /tmp/v22checks_20261024-075020-commit/225679d46e1c/chroma-library   (candidate)
  packs  /tmp/v22checks_20261024-075020-commit/225679d46e1c/chroma-packs   (candidate)
Traceback (most recent call last):
  File "/mnt/project-files/chroma-release/v22_checks.py", line 939, in <module>
    rejudge() if a.rejudge else main()
                                ~~~~^^
  File "/mnt/project-files/chroma-release/v22_checks.py", line 767, in main
    n = build_tree()
  File "/mnt/project-files/chroma-release/v22_checks.py", line 481, in build_tree
    shutil.copytree(os.path.join(REAL, V21), os.path.join(T, V21), ignore=SKIPF)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/emren/.local/share/uv/python/cpython-3.13.16-linux-x86_64-gnu/lib/python3.13/shutil.py", line 591, in copytree
    with os.scandir(src) as itr:
         ~~~~~~~~~~^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/project-files/chroma-library/archive/live-2026-10-06-1625'
/mnt/project-files/chroma-release/short-v25/run.sh: line 1: /tmp/v25_ship_s7.log: No such file or directory
ship_hook: 0 patches in 0 processes (/tmp/v25_ship_s7.log)
```

