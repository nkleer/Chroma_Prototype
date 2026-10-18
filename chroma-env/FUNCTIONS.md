# Where each part of the game lives

One row per function of the game, and the files that hold it in every folder, so a session goes straight to its place.
`MAP.md` (in the shared folder) says where each folder is and who owns it; this page says what each one holds for a
function. Step 3 of the plan Emren started on 2026-10-18 ("Start all four"; the shared folder's
`chroma-env/plan-by-function-2026-10-18.md`). Kept by the workspace thread; the owner of a file that moves updates its
row in the same pull request.

The engine's life loop, `_run`, lives in 18 parts, `run_01_start.py` to `run_18_integrate.py`, and the Earth rules'
tables in `rules_*.py`; `chroma-engine/CLAUDE.md` says what each part holds and how they join, and this page names the
parts each function is in. A function that runs at several points of the week has a line in several parts
(`rg -n name chroma-engine/v22-speedpass/` finds them all). Folders: `E` is `chroma-engine/v22-speedpass/`, `G` is
`chroma-game/prototype/`, `W` is `chroma-game/prototype/web/src/`, `L` is `chroma-library/`, `K` is `chroma-packs/`.

| Function | Engine (`E`) | Game and story (`G`), page (`W`) | Library (`L`) and packs (`K`) |
|---|---|---|---|
| The five colours: how a life shifts them, identity | `run_13_learning.py`; `run_18_integrate.py` (integrate, conversion, breakthrough); `combos.py` (what each colour pair means) | `game_views.py` (identity), `game_voice.py` (the character's own ways) | |
| A week's moment: the situation, its options, the choice, the outcome | `run_10_situation.py`, `run_11_choice.py`; `library.py` (seed situations); `batch.py` (loads a Library batch); `earth_rules.py` with `rules_moments.py` (reads the Earth batch); `explain.py`, `foresee.py` (the character's view before and after) | `game_checkpoints.py` (checkpoints, options, resolutions, hindsight); `story_moments.py`; `W/app/06-moment.js` | `L/*.lib` (the moments, 80 files; compiled into `earth.py` and its packs' files by the shared folder's `build.py`) |
| Chances, conditions and norms: seasons, shares, who a moment can reach | `run_05_conditions.py` (`cond_ns`, `rw_clause`, `ev_cond`); `rules_chance.py`, `rules_norms.py`, `rules_drivers.py`, `rules_more.py`, `rules_art.py` | | `K/<pack>/engine-conditions.py` (when a pack's echoes come) |
| What an act leaves behind: marks, echoes; Picks come back | `run_03_moments.py` (the batch's marks and echoes); `run_05_conditions.py` (`ep_return`); `run_14_marks.py` (what the week leaves); switch `echo_play` | `game_life.py` (`GAME["returns"]`: the card names the pick it came from) | `L/*.lib` (`back:` and `tier: return` lines); `K/<pack>/engine-conditions.py` (when a pack's echoes come) |
| Resources and commitments | `run_12_commitments.py` | `game_views.py` (status, plans) | |
| Goals, dreams, passions, plans, the felt horizon | `run_02_goals.py`; `run_12_commitments.py` (steps taken); `run_17_inner.py` (the felt horizon, dreams, passions and plans) | `game_voice.py` (goals); `story_goals.py` | `L/dreams.py` |
| Work, titles and perks | `run_04_titles.py` (the `r_*` helpers); `run_15_titles.py` (titles gained and lost); `rules_titles.py`, `rules_perks.py`, `rules_packs.py` | `game_life.py` (roles and titles) | `L/perks_titles/` (22 parts, joined into `earth_perks_titles.py`); `K/<pack>/roles.py`, `catalogue.py`, `helps.py` |
| The body, the mind, health and death | `run_07_body.py` (`body_week`, `death_week`); `run_14_marks.py` (deaths); `run_17_inner.py` (identity and the character's own death) | `game_views.py` (health); `game_life.py` (the end of a life); `story_moments.py` (deaths) | |
| Temperament | `run_17_inner.py` | `game_life.py` (temperament) | |
| Rites of passage | `run_18_integrate.py` | `story_lines.py` (rites, conversions, breakthroughs) | |
| The outer world: society, economy, state, eras, places | `world.py` and its parts `world_base.py`, `world_society.py`, `world_years.py`, `world_hooks.py`; `world_link.py` and its parts `world_link_base.py`, `world_link_week.py`, `world_link_rates.py`, `world_link_life.py` (how the engine reads the world); `run_06_world.py`, `run_16_world.py` (eras, events, needs, pressure); `rules_world.py` | `game_world.py`; `worldview.py` (the world panel) | `L/worlds.py`; `K/<pack>/worlds.py` |
| The cast: people, family, ties, leaders | `world_people.py` and its parts (`_roster`, `_lives`, `_ticks`, `_lead`, `_eyes`, `_acts`, `_views`) | `story_cast.py`; `game_views.py` (family, cast) | |
| The spheres of society | `world_spheres.py`, `world_events.py`, `world_people_settings.py`, `world_people_sacred.py`; `sphere_data.py` (generated: never edit) | `game_world.py` (posts, lines, talks, the seen) | `L/spheres/` (14 parts, joined into `earth_spheres.py`) |
| Every change has a cause | `run_08_fixes.py` (`option_causes`); `world_link_life.py` (causes); switch `role_why` (`rg -n role_why` finds its lines in `run_04`, `05`, `14`, `15`) | `game_causes.py` | the cause words in `L/earth_story.py` and `L/perks_titles/` |
| The story's words: the voice, chapters, the song, the epitaph | | `story.py` and its parts; `story_text.py` (text tables); `game_voice.py`; `game_words.py` (closing texts) | `L/earth_story.py`, `L/earth_voice.py` |
| The everyday routine between moments | | `routine.py`; `routine_text.py` (text tables) | |
| What the player sees: the HUD, the Book, the sheet, panels | | `game_views.py`; `console.py` (one controller for terminal and page); `W/app/05-hud.js`, `08-sheet.js`, `09-book.js`, `12-panels.js`; `W/style/` (10 parts) | |
| Saves | `world_events.py`, `world_people_views.py`, `world_link_life.py` (save and load) | `game_views.py` (saves); `W/app/10-save.js` | |
| Pictures and option icons | | `W/live_icons.py` | `chroma-art/game/` (`pics/` holds the pictures) |
| Checks | `chroma-engine/tools/` (`t_steps.py` and the rest) | `G/test/` (`smoke.py`, `prove.py`, `text_check.py`, `timeless.py`, `saveload.py`) | `L/tests/`; `K/tools/`; Release: `chroma-release/` |

Built and copied files are in the root `CLAUDE.md` ("Files you never open whole"): never edit them.
