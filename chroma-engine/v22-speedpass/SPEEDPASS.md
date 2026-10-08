# v22 engine speed pass (Engine thread, 2026-10-08)

The live v22 engine (`chroma-engine/archive/live-v22/`, frozen at go-live) with programming-only speed-ups. Every life
is the same: same seeds give the same lives, the same outputs bit for bit, the same rarity numbers. No rate, rule,
switch or default changed; no new feature. Pure Python and numpy only (no numba, Cython or C), so it runs in Pyodide
as before. Asked by Emren 10-08 (10:09 UTC "check engine speed pass", 10:14 UTC "make this version clean, solid and
fast", 10:47 UTC yes to the six-item list: the outer world's code is included).

- Files: the same 12 `.py` files and `rarity.json` as `archive/live-v22/`. Changed: `engine.py`, `world.py`,
  `world_link.py`, `world_people.py`. Unchanged (byte for byte): `batch.py`, `combos.py`, `earth_rules.py`,
  `explain.py`, `foresee.py`, `library.py`, `life.py`, `schwartz.py`, `world_keys.py`, `rarity.json` (MD5SUMS here).
- Switch overrides: none.
- The game's six pause anchors in `run()` (chroma-game/prototype/link.py) are untouched, each still found once, and
  no local variable the game, `explain.py` or `foresee.py` reads was renamed or changes value at a pause. New
  temporaries only were added (`memo_`, `xd_`, `fo_`, `gx_`), and the one loop replaced by a single pass (tenure gates)
  leaves its loop variables as the loop did.

## What changed, and why it gives the same numbers

engine.py
1. `poisson_at_least`, `negbin_at_least` (the felt odds of plans): the old loop ran every element to the largest
   `n` and added 0.0 after its own `n` terms. Now each element adds exactly its own `n` terms, in the same order
   with the same operations (`_cdf_below`), longest first so the ones still adding are always the first K.
2. In the weekly loop, the felt odds are worked out for plans only (`gk == 2`); the other slots' odds were computed
   and thrown away by `np.where(pln, ...)`. Each plan's odds depend only on its own numbers.
3. `ev_cond` (every condition read from text): one globals dict for all conditions instead of a new one per call; an
   answer that is already one value per person is copied as it is instead of going through `broadcast_to`.
4. The monthly condition loop: within one month a condition's text gives the same answer every time it is read
   (the state does not change inside the loop), so each distinct text is read once (`ev_memo`). Never for a text
   that draws `chance` (a fresh draw each time, in the same order as before) or reads `sa`.
5. `factor`: a moment with no likelier/rarer conditions returns 1 directly (clip of ones was 1); the clip itself
   calls numpy's two steps (`minimum(maximum(f, .1), 6)`, values here are never 0 or NaN). The `x 1.0` for
   non-inner moments is skipped (x times 1.0 is x).
6. `had()`: each list of moment names is turned into column numbers once per run, not at every call.
7. `doors()`: only 2 of the 8,218 options need any means, so the sigmoid product runs on those 2 rows; every other
   row's product was exactly 1.0. The matrix product after it is unchanged.
8. Base rates: `np.exp(X @ DRV.T)` was computed twice on the same numbers; now once (`xd_`). The subset products
   for deaths stay as they were.
9. Gap windows (`refr`, `gapw_`, the gap test in `re_`): each moment's column is computed by the one rule that
   keeps it, instead of computing both and picking with `np.where`.
10. Tenure gates (title held so many years): the 100 or so per-moment tests run as one array pass
    (`TEN_*`, `logical_or.reduceat`), then the loop's last variables are set as the loop left them.
11. `holds:` gates: the float32 count runs on the titles some moment names (whole-number sums of 0s and 1s,
    exact in any order).
12. Title rules: each title's age window unpacked once (`AGES_T`, the same numpy numbers); `count_nonzero` for the
    plain "anyone?" tests in the title and echo loops; two small `np.isin` lists written as equalities.
13. `np.clip` inside `run()` calls numpy's clip ufunc directly (`_uclip`), the same function `np.clip` ends in,
    without its Python wrapper.

world.py, world_link.py, world_people.py
14. `np.clip` calls numpy's clip ufunc directly (as 13; two calls with `None` or `out=` keep `np.clip`).
15. `np.isin` against a few whole numbers written as equalities (`_isin_small`) in `reach_pull`, `group_time` and
    the monthly life course.
16. `moment_factor`: settings by kind in one comparison; each technology asked once a week. `rate_factor`: each
    kind's moments found once (the moment kinds never change).

## Proof (Engine thread, 2026-10-08 10:22 to 11:05 UTC, on scratch copies)

Same seeds, every output of `run()` hashed key by key, against the frozen live v22 engine (live Library and packs):

| Run | Identical | CPU live v22 | CPU this | Speed-up |
|---|---|---|---|---|
| 50 lives, world off, seed 1 | yes | 194 s | 161 s | 1.20x |
| 50 lives, world on, seed 2 | yes | 255 s | 215 s | 1.19x |
| 1 life, world on, seed 5 (as the game plays) | yes | 106 s | 82 s | 1.30x |
| 1 life, world on, seed 9 | yes | 103 s | 79 s | 1.30x |

A short run of the release thread's own check (a scratch copy of `check_speedpass.py`, report beside this note as
`speedpass_short.txt`): the engine's seed library (20 lives, as tribal and magic lives play) identical, 1.13x; the
game's preset 1 (an Earth life, world on) played birth to death through a copy of the live game, every text and HUD
identical, 1.19x; preset 5 (a tribal life) identical, 1.04x. CPU times come from runs sharing the 4 cores, so take
them as close, not exact; the full `check_speedpass.py` run gives the release figure.

Where the rest of the time goes: no single block any more. In a played Earth life the outer world's week is about
11 %, the monthly conditions and title rules about 15 %, and the remaining weekly loop is hundreds of small array steps
of 0.5 to 2 % each. A tribal or magic life has no Library conditions or titles to save on, which is why it gains least.
Going further would mean rewriting the weekly loop's arithmetic, where keeping every number bit for bit is much harder
to prove; that is not part of this pass.
