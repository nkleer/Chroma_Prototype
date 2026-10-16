# The game: notes for Claude sessions

Owner: the Gamification thread. The repository-wide rules are in the root `CLAUDE.md`; this page maps the game.
`prototype/` is a live path: it reaches the shared folder only at a publish (`CONTRIBUTING.md`), so `tools/mirror.py`
refuses its files. This file sits one level above it so the build never copies it into the game.

## Where things are (`prototype/`)

Each Game mixin module imports the module names its methods read (from `game_base` and `game_words`), so a method
moves between files without changing what it does. A new game-side file must also go in `web/worker.js` `SOURCES`;
`test/smoke.py` fails when one is missing.

| File | Lines | What |
|---|---|---|
| `play.py` | 30 | terminal loop around `console.Console`; waits on `input()`, so never run it from a session |
| `console.py` | 783 | the text controller for the terminal and the page: `Console.handle(line)` returns `(text, busy)`; every key (`HELP` lists them) and the setup steps (`CUSTOM_STEPS`, `STEP_FORM`) |
| `game.py` | 429 | `PRESETS` (the six starts; Release's `check_f15.py` reads them from this file's text) and class `Game`: its class attributes and its core, `__init__`, `_intervene`, `age`, `advance`, `decide`. Every name the game layer has is importable from `game` |
| `game_base.py` | 578 | the game layer's settings (`GAME`, `V225`, the `CHROMA_GAME` and `CHROMA_ENGINE` switches), names, `library_for` and helpers: what `game.py` held before class `Game` |
| `game_words.py` | 961 | words and closing texts: the peace reading, the song, `life_paragraph`, `last_talk`, `book_catalog`: what `game.py` held after class `Game` |
| `game_checkpoints.py` | 579 | `CheckpointsMixin`: steers, checkpoints and their options, resolutions, hindsight, turning points |
| `game_world.py` | 600 | `WorldMixin`: the outer world in the story: world effects, levers, far ties, places, posts, lines, talks |
| `game_voice.py` | 630 | `VoiceMixin`: the inner voice, threads, trust, the character's own ways, goals, learning, the weekly hooks |
| `game_life.py` | 779 | `LifeMixin`: states, roles and titles, recall, temperament, the end of a life (`_on_end`), story lines, yearly chapters |
| `game_views.py` | 883 | `ViewsMixin`: status, HUD, routine, family, news, cast, saves, plans, identity, health, the Book, the review |
| `story.py` | 1,692 | the story layer: class `Story` and its code |
| `story_text.py` | 711 | `story.py`'s text tables (`SCENES`, `OUTSIDE`, `OUTCOMES`, `MOOD`, ...), data only |
| `routine.py` | 182 | the everyday lines' rules and their `check()` (`python3 -B routine.py`) |
| `routine_text.py` | 427 | the everyday lines themselves (`ROUTINE`), data only |
| `worldview.py` | 704 | the outer world as the player sees it |
| `link.py` | 44 | loads `engine_pin/engine.py` as module `engine` and checks its pause points (`week`, `situation`, `choose`, `odds`, `learn`, `end`) |
| `rarity.json` | | the rarity table; `rarity.py` is built from it |
| `engine_pin/` | | generated: the engine, Library and packs pinned by `tools/build.py`. Never edit or read it; read `chroma-engine/v22-speedpass/`, `chroma-library/`, `chroma-packs/` |
| `README.md` | 657 | history, version by version. Read one section (`rg -n '^#' README.md`), not all of it |

## The page (`prototype/web/`)

- Sources in `web/src/`: `head.html` (one `<style>` block, 1,593 lines), `body.html`, `app.js` (2,859 lines; it holds
  the save format), `look.css` and `look.js` (the ink look), `clarity.css` and `clarity.js`, `sprite.svg`,
  `option-icons-live.json`, `pics-left-out.json`, `pic-packs.json`.
- `web/src/build.py` joins them into `web/index.html` (0.07 s, byte for byte). Never edit or read `index.html` or
  `page.html`; change the sources and rebuild.
- `web/worker.js` runs the Python in Pyodide. Its `SOURCES` list names every `.py` file the page loads:
  `tools/build.py` adds missing `engine_pin` files, but a new game-side file must be added by hand.
- The published artifact holds at most 511 files; `tools/webdir.py` packs code and rarer pictures into a few files.

## Building (`chroma-game/tools/`)

`python3 -B chroma-game/tools/build.py <new out dir>` (about 10 s) pins the engine, Library and packs, writes
`rarity.py`, completes `SOURCES`, checks the pin (C-X1) and that the game loads, and builds the page and the web folder.
Build every candidate with it; never pin by hand.

## Which test proves what (`prototype/test/`)

Run from `prototype/` with `python3 -B test/<name>`. A whole life takes about 2 minutes.

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
