# The engine: notes for Claude sessions

Owner: the Engine thread. The repository-wide rules are in the root `CLAUDE.md`.

- `v22-speedpass/` is the live engine (the folder name is historical; `chroma-env/paths.py` calls it `engine_live`).
  `MD5SUMS` lists its files. `SPEEDPASS.md` explains the speed pass that kept every life identical.
- `engine.py` (about 6,400 lines) is vectorised over N lives, one tick a week. Its module docstring is from v2 and out of
  date; go by the code. Find the entry points with `rg -n '^def _run|^def run|^PAUSES|^STATE' engine.py`:
  - `_run(...)` is one function of about 4,500 lines holding the whole weekly loop.
  - `run()` runs it to the end; `run_steps()` runs it as a generator that pauses at `PAUSES`
    (`week`, `situation`, `choose`, `odds`, `learn`, `end`). The game drives `run_steps()` (`chroma-game/prototype/link.py`).
  - `STATE` names the local variables of `_run` that the game, `explain.py` and `foresee.py` may read at a pause
    (`STATE_IF` and `STATE_MORE` a few more). A pause hands over only these, read from cells (`_handed` in `_run`), in
    one dict refreshed at each pause; a name read that is not there goes in `STATE_MORE` (t_steps lists it).
    Renaming one, or changing its value at a pause, breaks the game.
- `sphere_data.py` holds the nine spheres (`SPHERES`); `world.py`, `world_people.py`, `world_link.py` and
  `world_keys.py` are the outer world; `earth_rules.py` the Earth rules; `rarity.json` the rarity table the game builds
  `rarity.py` from.
- `world_people.py` (class `People`, 198 lines) and `world.py` (class `World`, 626 lines) keep the module docstring, the
  class and its core; the rest moved out verbatim. The module code is in `world_people_base.py` and `world_base.py`,
  the methods in mixin modules of 481 to 780 lines that the class inherits, one or more whole sections each (each
  module's `_PARTS` lists them). Every name is still importable from `world_people` and `world`, and a patch on
  `People` or `World` (`People._pt_q = ...`) works as before. Find a method with `rg -n 'def name' v22-speedpass/`;
  a new module name goes in `_PARTS` (the world cache, `people_check`, `world_check` and the stats keys read it), and
  `chroma-game/tools/build.py` pins every `world*.py`.
  - People, in `world_people_<part>.py`: `roster` (the world through world-build.md's names, adding and dropping
    people, birth), `settings` (settings, spheres phase 2), `ticks` (the ticks, ties, commitments, the life course of
    settings), `lives` (the cast's own lives, wants, far ties), `sacred` (S5, S6), `eyes` (approval, standing, reach,
    S3, S4, what the engine reads), `acts` (acts, levers, pushes, body_trust, place_turnover), `lead` (S7, who slots,
    place and moving), `views` (emigration, views for the game, save and load).
  - World: `world.py` itself (construction, the clock, emigration), `world_hooks` (nature, the C hooks, abroad),
    `world_society` (economy, state, institutions, places, culture, society), `world_years` (figures, history, the
    yearly update, pushes, what the engine reads), `world_spheres` (spheres phases 1c, 2 and 4, place_turnover),
    `world_events` (spheres phase 3, Replace, save and load).
- `tools/` holds the checks Release runs (`tools/README.md`). The quick one: `python3 -B chroma-engine/tools/t_steps.py`
  (70 rows, about an hour, 50 to 65 min measured 10-17: `run_steps()` gives `run()`'s lives, the pause order, every `STATE` name, each switch's own rows).
- `prototype/calib_v8/rarity.json` is the rarity table of v22 and v22.1. The paused v23 engine lives in the shared
  folder's `chroma-engine/prototype/`, not here.

Any change here reaches the game only through a re-pin (`chroma-game/tools/build.py`). A change meant to keep lives
identical needs Release's same-lives proof (`chroma-release/same-lives.sh`, four parts of about 50 minutes); a rate
change needs the full proof. Don't split `_run` or move code out of it without the Engine thread and that proof.
