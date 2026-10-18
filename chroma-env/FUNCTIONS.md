# Where each part of the game lives

One row per function of the game, and the files that hold it in every folder, so a session goes straight to its place.
`MAP.md` (in the shared folder) says where each folder is and who owns it; this page says what each one holds for a
function. Step 3 of the plan Emren started on 2026-10-18 ("Start all four"; the shared folder's
`chroma-env/plan-by-function-2026-10-18.md`). Kept by the workspace thread; the owner of a file that moves updates its
row in the same pull request.

Engine places inside `engine.py`'s `_run` (lines 1,747 to 6,605, the life loop) are named by their section comment,
which `rg -n '# ---- 2. choice' chroma-engine/v22-speedpass/engine.py` finds. `_run` is to be split into phase files
(plan step 3); the rows change when it is. Folders: `E` is `chroma-engine/v22-speedpass/`, `G` is
`chroma-game/prototype/`, `W` is `chroma-game/prototype/web/src/`, `L` is `chroma-library/`, `K` is `chroma-packs/`.

| Function | Engine (`E`) | Game and story (`G`), page (`W`) | Library (`L`) and packs (`K`) |
|---|---|---|---|
| The five colours: how a life shifts them, identity | `_run` "4. learning channels", "5. integrate", "7. conversion", "8. breakthrough"; `combos.py` (what each colour pair means) | `game_views.py` (identity), `game_voice.py` (the character's own ways) | |
| A week's moment: the situation, its options, the choice, the outcome | `_run` "1. situation", "2. choice", "3. outcome vs expectation"; `library.py` (seed situations); `batch.py` (loads a Library batch); `earth_rules.py` (reads the Earth batch); `explain.py`, `foresee.py` (the character's view before and after) | `game_checkpoints.py` (checkpoints, options, resolutions, hindsight); `story_moments.py`; `W/app/06-moment.js` | `L/*.lib` (the moments, 80 files; compiled into `earth.py` and its packs' files by the shared folder's `build.py`) |
| What an act leaves behind: marks, echoes; Picks come back | `_run` "3d. the Library's batch" and its helper `ep_return`; switch `echo_play` | `game_life.py` (`GAME["returns"]`: the card names the pick it came from) | `L/*.lib` (`back:` and `tier: return` lines); `K/<pack>/engine-conditions.py` (when a pack's echoes come) |
| Resources and commitments | `_run` "3b. resources and commitments" | `game_views.py` (status, plans) | |
| Goals, dreams, passions, plans, the felt horizon | `_run` setup "v7 goals", "3c. v7 goals", "4b2. v7 felt horizon", "4d. v7 dreams, passions and plans" | `game_voice.py` (goals); `story_goals.py` | `L/dreams.py` |
| Work, titles and perks | `_run` setup "titles and perks"; `earth_rules.py` | `game_life.py` (roles and titles) | `L/perks_titles/` (22 parts, joined into `earth_perks_titles.py`); `K/<pack>/roles.py`, `catalogue.py`, `helps.py` |
| The body, the mind, health and death | `_run` "v22.5 F1 and F2" setup and its helpers `body_week`, `death_week`; "4e. identity and the character's own death" | `game_views.py` (health); `game_life.py` (the end of a life); `story_moments.py` (deaths) | |
| Temperament | `_run` "4c. temperament" | `game_life.py` (temperament) | |
| Rites of passage | `_run` "6. rites of passage" | `story_lines.py` (rites, conversions, breakthroughs) | |
| The outer world: society, economy, state, eras, places | `world.py` and its parts `world_base.py`, `world_society.py`, `world_years.py`, `world_hooks.py`; `world_link.py` (how the engine reads the world); `_run` "4b. the outside world" | `game_world.py`; `worldview.py` (the world panel) | `L/worlds.py`; `K/<pack>/worlds.py` |
| The cast: people, family, ties, leaders | `world_people.py` and its parts (`_roster`, `_lives`, `_ticks`, `_lead`, `_eyes`, `_acts`, `_views`) | `story_cast.py`; `game_views.py` (family, cast) | |
| The spheres of society | `world_spheres.py`, `world_events.py`, `world_people_settings.py`, `world_people_sacred.py`; `sphere_data.py` (generated: never edit) | `game_world.py` (posts, lines, talks, the seen) | `L/spheres/` (14 parts, joined into `earth_spheres.py`) |
| Every change has a cause | `_run` helper `option_causes`; switch `role_why` | `game_causes.py` | the cause words in `L/earth_story.py` and `L/perks_titles/` |
| The story's words: the voice, chapters, the song, the epitaph | | `story.py` and its parts; `story_text.py` (text tables); `game_voice.py`; `game_words.py` (closing texts) | `L/earth_story.py`, `L/earth_voice.py` |
| The everyday routine between moments | | `routine.py`; `routine_text.py` (text tables) | |
| What the player sees: the HUD, the Book, the sheet, panels | | `game_views.py`; `console.py` (one controller for terminal and page); `W/app/05-hud.js`, `08-sheet.js`, `09-book.js`, `12-panels.js`; `W/style/` (10 parts) | |
| Saves | `world_events.py`, `world_people_views.py` (save and load) | `game_views.py` (saves); `W/app/10-save.js` | |
| Pictures and option icons | | `W/live_icons.py` | `chroma-art/game/` (`pics/` holds the pictures) |
| Checks | `chroma-engine/tools/` (`t_steps.py` and the rest) | `G/test/` (`smoke.py`, `prove.py`, `text_check.py`, `timeless.py`, `saveload.py`) | `L/tests/`; `K/tools/`; Release: `chroma-release/` |

Built and copied files are in the root `CLAUDE.md` ("Files you never open whole"): never edit them.
