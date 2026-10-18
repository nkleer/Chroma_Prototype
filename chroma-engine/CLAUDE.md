# The engine: notes for Claude sessions

Owner: the Engine thread. The repository-wide rules are in the root `CLAUDE.md`.

- `v22-speedpass/` is the live engine (the folder name is historical; `chroma-env/paths.py` calls it `engine_live`).
  `MD5SUMS` lists its files. `SPEEDPASS.md` explains the speed pass that kept every life identical.
- `engine.py` (about 2,000 lines) is vectorised over N lives, one tick a week. Its module docstring is from v2 and out of
  date; go by the code. Find the entry points with `rg -n '^RUN_PARTS|^def run|^PAUSES|^STATE' engine.py`:
  - `_run(...)` is one function of about 4,860 lines holding the whole weekly loop. Its lines live in 18 files,
    `run_01_start.py` to `run_18_integrate.py` (90 to 500 lines), unchanged and at their own indent; engine.py joins them
    in `RUN_PARTS` order (`parts.py`) and compiles them as the one function, so Python runs the same code. A part is
    not a module: edit it like the stretch of `_run` it is (a name it uses may be set in an earlier part), never import
    it. A traceback names `engine.py+parts`; `parts.where(<line>)` gives the part and line. Setup: `01_start`
    (settings, streams, eras), `02_goals`, `03_moments` (the batch's marks, echoes, inner moments), `04_titles` (title
    and perk helpers `r_*`), `05_conditions` (`cond_ns`, `rw_clause`, `ev_cond`, seasons, shares, roles by sex),
    `06_world` (WorldLink, service, debts, household), `07_body`, `08_fixes` (many-lives fixes, prison ties, option
    causes, `_handed`). The week: `09_week` ("week" pause), `10_situation` (gates, the draw, "situation" pause),
    `11_choice` ("choose", "odds", "learn" pauses), `12_commitments` (resources, money, clashes, goals),
    `13_learning`, `14_marks` (what the week leaves: marks, deaths, endings, moves), `15_titles` (titles gained and lost
    in time), `16_world` (eras, events, needs, pressure), `17_inner` (horizon, temperament, dreams, peace, identity,
    own death), `18_integrate` (integrate, rites, conversion, breakthrough, "end" pause, the outputs). A feature that
    runs at several points of the week has a line in several parts (`rg -n` finds them all).
  - `run()` runs it to the end; `run_steps()` runs it as a generator that pauses at `PAUSES`
    (`week`, `situation`, `choose`, `odds`, `learn`, `end`). The game drives `run_steps()` (`chroma-game/prototype/link.py`).
  - `STATE` names the local variables of `_run` that the game, `explain.py` and `foresee.py` may read at a pause
    (`STATE_IF` and `STATE_MORE` a few more). A pause hands over only these, read from cells (`_handed` in `_run`), in
    one dict refreshed at each pause; a name read that is not there goes in `STATE_MORE` (t_steps lists it).
    Renaming one, or changing its value at a pause, breaks the game.
- `sphere_data.py` holds the nine spheres (`SPHERES`); `world.py`, `world_people.py`, `world_link.py` and
  `world_keys.py` are the outer world; `earth_rules.py` the Earth rules, its tables in `rules_*.py` the same way as
  `_run` (`RULES_PARTS`: moments, drivers, titles, perks, norms, chance, more, packs, art, world); `rarity.json` the
  rarity table the game builds `rarity.py` from.
- `world_people.py` (class `People`, 198 lines) and `world.py` (class `World`, 626 lines) keep the module docstring, the
  class and its core; the rest moved out verbatim. The module code is in `world_people_base.py` and `world_base.py`,
  the methods in mixin modules of 481 to 780 lines that the class inherits, one or more whole sections each (each
  module's `_PARTS` lists them). Every name is still importable from `world_people` and `world`, and a patch on
  `People` or `World` (`People._pt_q = ...`) works as before. Find a method with `rg -n 'def name' v22-speedpass/`;
  a new module name goes in `_PARTS` (the world cache, `people_check`, `world_check` and the stats keys read it), and
  `chroma-game/tools/build.py` pins every `world*.py` (and `parts.py`, `run_*.py`, `rules_*.py`).
  - People, in `world_people_<part>.py`: `roster` (the world through world-build.md's names, adding and dropping
    people, birth), `settings` (settings, spheres phase 2), `ticks` (the ticks, ties, commitments, the life course of
    settings), `lives` (the cast's own lives, wants, far ties), `sacred` (S5, S6), `eyes` (approval, standing, reach,
    S3, S4, what the engine reads), `acts` (acts, levers, pushes, body_trust, place_turnover), `lead` (S7, who slots,
    place and moving), `views` (emigration, views for the game, save and load).
  - WorldLink (`world_link.py`, 497 lines: set-up and the weekly step), split the same way: `world_link_base.py`
    (tables, helpers, the burned-in world's cache), `world_link_week` (what the week brings: congregations, sacred
    lines, offices, disasters, deaths, far ties, eyes, lead, seen), `world_link_rates` (era, moment and title rates,
    closures, norms, channels, odds), `world_link_life` (other societies, titles, moves, safety, resources, causes,
    after the act, output, saves). Each mixin repeats world_link.py's imports so its methods compile as before.
  - World: `world.py` itself (construction, the clock, emigration), `world_hooks` (nature, the C hooks, abroad),
    `world_society` (economy, state, institutions, places, culture, society), `world_years` (figures, history, the
    yearly update, pushes, what the engine reads), `world_spheres` (spheres phases 1c, 2 and 4, place_turnover),
    `world_events` (spheres phase 3, Replace, save and load).
- `tools/` holds the checks Release runs (`tools/README.md`). The quick one: `python3 -B chroma-engine/tools/t_steps.py`
  (71 rows, about an hour, 50 to 65 min measured 10-17: `run_steps()` gives `run()`'s lives, the pause order, every `STATE` name, each switch's own rows).
- `prototype/calib_v8/rarity.json` is the rarity table of v22 and v22.1. The paused v23 engine lives in the shared
  folder's `chroma-engine/prototype/`, not here.

Any change here reaches the game only through a re-pin (`chroma-game/tools/build.py`). A change meant to keep lives
identical needs Release's same-lives proof (`chroma-release/same-lives.sh`, four parts of about 50 minutes); a rate
change needs the full proof. Moving lines between parts, or out of `_run`, needs the Engine thread and that proof; a
split that keeps lines unchanged can show Python's code is the same (`chroma-engine/notes/by-function-2026-10-18.md`).
