# The game: notes for Claude sessions

Owner: the Gamification thread. The repository-wide rules are in the root `CLAUDE.md`; this page maps the game.
`prototype/` is a live path: it reaches the shared folder only at a publish (`CONTRIBUTING.md`), so `tools/mirror.py`
refuses its files. This file sits one level above it so the build never copies it into the game.

## Where things are (`prototype/`)

Each Game mixin module imports the module names its methods read (from `game_base` and `game_words`), so a method
moves between files without changing what it does. `story.py` is split the same way (`story_base` and four Story
mixins). To find a method: `rg -n 'def name' chroma-game/prototype/game*.py chroma-game/prototype/story*.py`. A new
game-side file must also go in `web/worker.js` `SOURCES`; `test/smoke.py` fails when one is missing.

| File | Lines | What |
|---|---|---|
| `play.py` | 30 | terminal loop around `console.Console`; waits on `input()`, so never run it from a session |
| `console.py` | 783 | the text controller for the terminal and the page: `Console.handle(line)` returns `(text, busy)`; every key (`HELP` lists them) and the setup steps (`CUSTOM_STEPS`, `STEP_FORM`) |
| `game.py` | 435 | `PRESETS` (the six starts; Release's `check_f15.py` reads them from this file's text) and class `Game`: its class attributes and its core, `__init__`, `_intervene`, `age`, `advance`, `decide`. Every name the game layer has is importable from `game` |
| `game_base.py` | 586 | the game layer's settings (`GAME`, `V225`, the `CHROMA_GAME` and `CHROMA_ENGINE` switches), names, `library_for` and helpers: what `game.py` held before class `Game` |
| `game_words.py` | 965 | words and closing texts: the peace reading, the song, `life_paragraph`, `last_talk`, `book_catalog`: what `game.py` held after class `Game` |
| `game_checkpoints.py` | 662 | `CheckpointsMixin`: steers, checkpoints and their options, resolutions, hindsight, turning points |
| `game_world.py` | 600 | `WorldMixin`: the outer world in the story: world effects, levers, far ties, places, posts, lines, talks |
| `game_voice.py` | 667 | `VoiceMixin`: the inner voice, threads, trust, the character's own ways, goals, learning, the weekly hooks |
| `game_life.py` | 785 | `LifeMixin`: states, roles and titles, recall, temperament, the end of a life (`_on_end`), story lines, yearly chapters |
| `game_views.py` | 885 | `ViewsMixin`: status, HUD, routine, family, news, cast, saves, plans, identity, health, the Book, the review |
| `game_causes.py` | 236 | `CausesMixin`: "Every change has a cause" behind `GAME` `causes` and `causes_fold`: a gain or loss names its cause (the Engine's `role_why`), the cause trail (marker `Y`), the year that turned them, the fold line |
| `game_bold.py` | 274 | `BoldMixin`: Bold ways behind `GAME` `bold` (with the Engine's `bold_play`): the situation pause asks for a card's bold ways (`bold_ask`), up to two more ways on the card (number `BOLD_IX` + 100 x slot + base; `bix` gives the base), push and own pick (`bold_take`), the fit hint, win and cost lines, outcome lines, links (a bold try's return) and the Book's list |
| `game_because.py` | 99 | `BecauseMixin`: "Because of you, and meanwhile" behind `GAME` `because` (with the Engine's `need_why`): the outcome's needs split into what the pick did and what else happened, each with its cause (`nw` diffed from the choose pause), and a silent setback's told line (`nw_imp`) |
| `game_foot.py` | 103 | `FootMixin`: v24 footprints behind `GAME` `foot` (with the Engine's `foot_on`): each week's footprints from the Engine's `dict(foot=...)` events into `history["foot"]`, one line per kind after a pick (inside "Because of you"), and the six stacks (people, places, means, marks, doors, lessons) for the HUD and the Book |
| `game_aims.py` | 84 | `AimsMixin`: v24 aims behind `GAME` `aims` (with the Engine's `aims` and `heights`): the aims track for the sheet, the HUD and key a (foresee.aims), the aims they could take up (aim_choices), the player's `aim set` / `aim drop`, the heights reached, and at a choice the options leading into an aim's next step (aim_ways) |
| `game_asks.py` | 142 | `AsksMixin`: v24 asks behind `GAME` `ask_matter` (0, off): how much a moment matters to the character now (an aim's next step, a need they lack, the people in their life), weighed into which moments are asked, and the card's "This matters to them now" line; and behind `steer_between` (off) the player's lean between asks (key ~ and a letter), each unasked choice drawn again with it at a light steer's cost; and behind `talk` (off) talking one option over at a big moment (key t and its number): the character's answer, that option's reluctance falling for this pick, a little autonomy spent |
| `story.py` | 126 | the story layer: class `Story`, its core (`__init__`, `new`, `alive`, `get`, `say`, `nm`). Every name the story layer has is importable from `story` |
| `story_base.py` | 540 | the story's settings, names, places and word lists (values, goals, dreams, the moments' words) and helpers (`mk`, `plain`, `act`, `phase`, `load_library_story`): what `story.py` held before class `Story` |
| `story_cast.py` | 233 | `CastMixin`: roles, who is due and who dies, picking people, filling a line's slots |
| `story_moments.py` | 328 | `MomentsMixin`: thoughts, the voice, births, scenes, acts, outcomes, family, deaths and new kin, marks, streaks |
| `story_lines.py` | 296 | `LinesMixin`: ordinary weeks, outside events, eras, titles, commitments, clashes, rites, conversions, breakthroughs |
| `story_goals.py` | 232 | `GoalsMixin`: goals, dreams and plans, needs, hindsight, resolutions, the yearly chapter, the epitaph |
| `story_text.py` | 711 | `story.py`'s text tables (`SCENES`, `OUTSIDE`, `OUTCOMES`, `MOOD`, ...), data only |
| `routine.py` | 182 | the everyday lines' rules and their `check()` (`python3 -B routine.py`) |
| `routine_text.py` | 427 | the everyday lines themselves (`ROUTINE`), data only |
| `worldview.py` | 706 | the outer world as the player sees it |
| `link.py` | 44 | loads `engine_pin/engine.py` as module `engine` and checks its pause points (`week`, `situation`, `choose`, `odds`, `learn`, `end`) |
| `rarity.json` | | the rarity table; `rarity.py` is built from it |
| `engine_pin/` | | not in git: the engine, Library and packs copied from their owners' folders by `tools/pin.py` (the tests run it first). Never edit or read it; read `chroma-engine/v22-speedpass/`, `chroma-library/`, `chroma-packs/` |
| `README.md` | 25 | what the game is, how to play, where to read on |
| `HISTORY.md` | 644 | history, version by version up to 2026-10-09 (moved from `README.md`). Read one section (`rg -n '^#' HISTORY.md`), not all of it |

## The page (`prototype/web/`)

- Sources in `web/src/`: `head.html` (the title and fonts), the style (`style/`, below), `body.html`, the app (`app/`, below),
  `look.css` and `look.js` (the ink look), `clarity.css` and `clarity.js`, `sprite.svg`, `option-icons-live.json`,
  `pics-left-out.json`, `pic-packs.json`.
- `web/src/build.py` joins them into `web/index.html` (0.07 s, byte for byte). Never edit or read `index.html` or
  `page.html`; change the sources and rebuild. A change meant to leave the page as it was must leave `index.html`
  unchanged (`git status`).
- The app is one script in the page, kept as `web/src/app/NN-name.js` parts (`app.js` until 10-17); `build.py` joins
  them in name order inside one `<script>`, so a part reads the others' names as before. Find a function with
  `rg -n 'function name' chroma-game/prototype/web/src/app/`. `look.js` and `clarity.js` wrap some of its functions.

| Part | Lines | What |
|---|---|---|
| `01-base.js` | 125 | constants, colours, icons and pips, helpers, the marked story text (`rich`), tooltips |
| `02-words.js` | 243 | what the marked words mean; heart and head, what changed, dreams and plans |
| `03-chronicle.js` | 202 | the worker link (`send`, inputs); the chronicle, the story's main text |
| `04-line.js` | 346 | the whole life as a line (the fog ahead); the header and tools |
| `05-hud.js` | 501 | the character HUD and spider graph; the exact definitions; making a plan (key p) |
| `06-moment.js` | 441 | the moment and its cards; the event window |
| `07-interlude.js` | 111 | the interlude between two moments |
| `08-sheet.js` | 263 | the character sheet (key c) and its tabs |
| `09-book.js` | 118 | the Book of Moments |
| `10-save.js` | 99 | saving to a file, loading back, autosave: the save format. Release's `check_pageonly.py` holds a page-only release to it unchanged |
| `11-start.js` | 172 | the life-choice (tarot) cards on the start screen; the end of a life |
| `12-panels.js` | 148 | transport, help, the outer world panel, the keys the page answers itself |
| `13-state.js` | 93 | applying the game's state, the keyboard, the worker's start-up |

- The style is one `<style>` block in the page, kept as `web/src/style/NN-name.css` parts (all in `head.html` until
  10-17); `build.py` joins them in name order after `head.html`, so later rules still win as before. Find a rule with
  `rg -n '\.name' chroma-game/prototype/web/src/style/`. `look.css` and `clarity.css` come after all of it.

| Part | Lines | What |
|---|---|---|
| `01-base.css` | 99 | the colours (`:root`), the night sky, the app frame |
| `02-line.css` | 87 | the life line |
| `03-table.css` | 95 | the main area, the table (a checkpoint), the option cards |
| `04-hud.css` | 148 | the character HUD; the inner voice before a choice and after |
| `05-menus.css` | 130 | transport; menu, setup, review, boot; narrower screens |
| `06-parchment.css` | 231 | v3: dark ink on parchment; the event window |
| `07-v21.css` | 230 | version 21: the spider graph, steers, titles, the interlude, the sheet, the World panel, tarot, the Book of Moments, seasons |
| `08-v22-moment.css` | 201 | v22's look: the top bar, the moment window, the chosen card's motion, the outcome, the compact crest |
| `09-v22-pages.css` | 111 | v22's story page, start, interlude and small panels; narrower screens and the phone |
| `10-sheet.css` | 255 | the character sheet in tabs; the Book and World boxes; the reading beside a moment; short windows; the folded "Out of reach" row |
- `web/worker.js` runs the Python in Pyodide. Its `SOURCES` list names every `.py` file the page loads:
  `tools/build.py` adds missing `engine_pin` files, but a new game-side file must be added by hand.
- The published artifact holds at most 511 files; `tools/webdir.py` packs code and rarer pictures into a few files.

## Building (`chroma-game/tools/`)

`engine_pin/` is not committed (plan by function, step 2): an engine, Library or packs merge needs no re-pin.
`python3 -B chroma-game/tools/pin.py` fills it from the owners' folders (copies what is missing or differs, removes what
the engine no longer asks for; `--check` only reports). The ladder's tests (`smoke`, `prove`, `same_life`, `same_engine`,
`saveload`, `timeless`, `text_check --pin`, `causes_check`) run it first; run it yourself after a pull before a script of
your own. A game folder with `engine_pin/PINNED.txt` (a release branch, main before step 2) is a committed pin, left as
it is.

`python3 -B chroma-game/tools/build.py <new out dir>` (about 10 s) bundles the engine, Library and packs into the
build's `engine_pin/` (the same list as `pin.py`), writes `rarity.py`, completes `SOURCES`, checks the bundle (C-X1) and
that the game loads, and builds the page and the web folder. Build every candidate with it.

## Which test proves what (`prototype/test/`)

Run from `prototype/` with `python3 -B test/<name>`. A whole life takes about 2 minutes. `smoke.py` and `prove.py` keep
each burned-in world in `/tmp/chroma_world_cache` (the engine's `CHROMA_WORLD_CACHE`), so a new life there sets up in
about 2 s instead of 6 s; an empty `CHROMA_WORLD_CACHE=` turns it off, and it stays off while `CHROMA_ENGINE` or
`CHROMA_GAME` is set.

| Test | Proves |
|---|---|
| `smoke.py [--same \| --base DIR \| --update]` | about 20 s: two short lives (presets 1 and 6) with keys, checkpoints and a save; fails on a crash or NaN; `--same` compares the play's md5s with `smoke.golden.json`, `--base` with another game folder |
| `prove.py [--base REF] [--presets 1,3]` | the "no change in play" proof in one command: `smoke.py`, then presets 1 to 6 (seed 7, `same_life.py`'s record and md5) here and on `origin/main`, side by side, naming the first step that differs. Lives are cached by the game files they came from (in the shared folder's `.cache/same-lives`), so main's six are played once per state of main; under 30 s when the game files match or both sides are cached, about 4 minutes otherwise |
| `text_check.py [--pin]` | about 1 s: every string literal in the game's own files, against `timeless.py`'s word list; reports only the real-world words a change adds against `origin/main` |
| `same_life.py <preset> <seed> <out>` | one played life, every step's text and HUD hashed; same md5 on two trees = same lives (use presets 1 to 6, seed 7) |
| `same_engine.py` | the same, engine side only |
| `saveload.py`, `saveload_world.py` | a saved life loads back exactly (without and with the outer world) |
| `end_at_choice.py` | a life ending in the week of a choice still reaches its review |
| `timeless.py` | the played text keeps the timeless modern setting (no real year, brand or event) |
| `markers.py` | the page's story markers are balanced |
| `identity_check.py`, `kin_check.py`, `lines_tied_check.py`, `book_check.py`, `longshot_check.py` | release rows; Release runs them |
| `*.js` | browser drivers and probes; Release runs them |
| `event_rate.py`, `season_ages.py`, `season_rate.py`, `next2_check.py` | scratch or old-batch tools, not checks |

The game's fast check through Release's runner:
`python3 -B chroma-release/v22_checks.py --level fast --only @game --repo <checkout>` (about 2 minutes).
