# v25 readers for lives left alone

Release's readers for v25's LA and LB rows (`records/v25/checks.md`, A2 and F2), in git so that a machine without the
shared folder (Emren's PC) can run them. The working copies stay in the shared folder's `chroma-release/out/v24/heights/`
and `out/v25/`; these files read and judge exactly as those do.

- `heights_engine24.py`: lives left alone, one seed a call:
  `python3 -B heights_engine24.py <tree> <seed> 400 100 eng_<seed>.json`, with `OMP_NUM_THREADS=1` and no `CHROMA_*`
  or `READ_GOALS` set. `<tree>` is a whole repository tree at the commit being read.
- `r0judge.py`: A2 against A0 (`engine_e69b3bf/`) and F2 on the same seeds:
  `python3 -B r0judge.py <sha7> --heights <folder holding engine_<sha7>/ and engine_e69b3bf/>`.
- `heights_v24.py` and `heights_judge.py`: the readers `r0judge.py` imports.
- `f1report.py`: F1, the neutral world, reported: `python3 -B f1report.py <sha7> --heights <folder>` reads
  `<folder>/engine_<sha7>_neutral/` (lives from `heights_engine24.py ... '{"realm": "neutral"}'`).
- `k4.sh`: K4, every v24 and v25 switch off against release/v23.2, byte for byte: `SHA=<full commit> bash
  chroma-release/v25/k4.sh <part 1 to 4>` from a checkout (`DRY=1` prints the switch overrides and stops). It is
  v24's `out/v24/k4/k4.sh` with this checkout's paths and the engine's `V25_OFF` added.

Lives from two machines are never pooled (`records/v25/evaluation.md` section 5): the cloud's numpy uses AVX-512 and
the PC's does not, so their lives differ byte for byte. Keep each machine's lives in its own folder, and judge a
candidate only against an A0 read on the same machine.
