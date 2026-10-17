# Chroma: notes for Claude sessions

Chroma is a life simulator in which Magic's colour pie (W, U, B, R, G) explains how one person grows over a whole life.
The game runs in the browser (Python in Pyodide) and is published as a claude.ai artifact. How work moves through this
repository (branches, pull requests, owners, `tools/mirror.py`, publishing) is in `CONTRIBUTING.md`; follow it.

The rules below exist to keep sessions cheap: most of the repository's bytes are generated files and exact copies, and
a whole life takes about two minutes to simulate.

## Who owns what

| Folder | Owner thread | Edit here? |
|---|---|---|
| `chroma-engine/v22-speedpass/` | Engine | owner only; see `chroma-engine/CLAUDE.md` |
| `chroma-engine/tools/` | Engine | owner only; the checks Release runs (`tools/README.md`) |
| `chroma-game/prototype/` | Gamification | owner only, except `engine_pin/`, which nobody edits; see `chroma-game/CLAUDE.md` |
| `chroma-game/tools/` | Gamification | `build.py`, the one build command; `webdir.py`, `pubmap.py` |
| `chroma-library/` | Library | owner only; edit the `.lib` sources, not the compiled files below |
| `chroma-packs/` | Life pathways and content packs | owner only |
| `chroma-art/` | Visuals for the game | owner only; `game/pics/` holds the pictures |
| `chroma-look/tools/` | Game visuals overhaul | owner only |
| `chroma-release/` | Release | owner only; the release checks |
| `chroma-env/`, `tools/`, root files | Workspace cleanup and setup | `env/<topic>` branches |

Every folder is named once in `chroma-env/paths.py`; scripts import it rather than writing paths by hand.

## Files you never open whole

Generated or copied, never edited by hand. `.claude/settings.json` blocks reading the first five and the pictures;
`.ignore` keeps all of them out of searches (`rg` and the Grep tool honour it; `grep -r` does not, so use `rg`), and
`.gitattributes` keeps their text out of `git diff`, `git show` and `git log -p`. In the shared folder, `.ignore` also
hides the run outputs, `_archive/` and the old and staging game copies; search one of those by naming it
(`rg <pattern> <folder>`).

| File | Size | Made by |
|---|---|---|
| `chroma-game/prototype/engine_pin/**` | 47 files, about 11 MB | `chroma-game/tools/build.py` pins the engine, Library and packs here; read the owners' copies instead |
| `chroma-game/prototype/web/index.html` | 1.3 MB, lines up to 254 KB | `python3 -B chroma-game/prototype/web/src/build.py` from `web/src/` (0.07 s, byte for byte) |
| `chroma-game/prototype/web/page.html` | 590 KB | `chroma-game/tools/webdir.py` |
| `chroma-game/prototype/web/src/ink-option-texts.json` | 1.2 MB | a copy of `chroma-art/game/ink-option-texts.json` |
| `chroma-game/prototype/rarity.py` | 101 KB | `chroma-game/tools/build.py`, from the game's `rarity.json` |
| `chroma-library/earth.py`, `earth_art.py`, `earth_play.py`, `earth_politics.py`, `earth_science.py`, `earth_stage.py` | 5.3 MB, 394 KB, 5 KB, 701 KB, 412 KB, 716 KB | compiled from the `.lib` sources by the Library's `build.py` (in the shared folder) |
| `chroma-art/game/lights.json` | 177 KB | `chroma-look/tools/extract_lights.js` |
| `chroma-art/game/pics/*.webp` | 563 pictures | the Visuals thread |

The Library's other `.py` files (`earth_story.py`, `earth_spheres.py`, `earth_voice.py`, `earth_perks_titles.py`,
`earth_age_fit.py`, `dreams.py`, `worlds.py`) are hand-written sources and stay searchable.

## Reading

- Never read a file over about 1,500 lines whole. Find the place with `rg -n`, then read a range.
- Large files people do edit: in `chroma-engine/v22-speedpass/`, `engine.py` (6,461 lines), `world_people.py` (5,900)
  and `world.py` (4,039). The game and story layers are split into files of 126 to 965 lines, the page's script into 13
  parts of 93 to 501 lines and its style into 10 parts of 87 to 255 lines (`chroma-game/CLAUDE.md`).
- `chroma-game/prototype/HISTORY.md` is 60 KB of history. Read the section you need (`rg -n '^#' HISTORY.md`), not all.
- Notes, plans, specs and run outputs live in the shared folder (`/mnt/project-files`), not here. Start from
  `chroma-env/MAP.md` there.

## Running

- Run Python with `-B`, so no `__pycache__` lands in the shared folder.
- Never run `chroma-game/prototype/play.py`: it waits on `input()` forever. Drive `console.Console` from a script, as
  `chroma-game/prototype/test/same_life.py` does: `c.handle(line)` returns `(text, busy)`; call `c.handle("")` while
  `busy`.
- Don't start a browser or Pyodide for an everyday change. The browser checks belong to Release.
- Timings on one core: importing the game 0.65 s; setting up a new life about 5.6 s; one simulated year about 1.3 s;
  one whole life about 2 minutes. Release's statistical runs take from 36 minutes to hours. Don't start one to check
  a small edit; use the ladder below.
- Long runs go in a scratch folder, never in the repository or the shared folder's live paths.

## The proof ladder: the cheapest check that is enough

Every life must stay the same unless Emren asked for a change in play. Pick the row that fits the change.

| Change | Check | Time |
|---|---|---|
| docs, CLAUDE files, comments | none | 0 |
| any game change, first | `python3 -B chroma-game/prototype/test/smoke.py`: a short life, no crash, no NaN; `--same` also checks it plays exactly as `test/smoke.golden.json` | about 20 s |
| game code, no change in play meant | `python3 -B chroma-game/prototype/test/prove.py`: `smoke.py --same`, then presets 1 to 6 (seed 7) on the branch and on `origin/main`, side by side, with main's lives from a shared cache; every life must match. By hand: `same_life.py <preset> 7 <out>` on both trees | under 30 s when cached, else about 4 min |
| game text | `python3 -B chroma-game/prototype/test/text_check.py` after each edit (new real-world words against main); `test/timeless.py` once on the PR | 1 s; 7 to 9 min once |
| game content or behaviour | `smoke.py --update` (the PR says why play changed), `test/text_check.py`, `test/timeless.py`, `test/saveload.py`, then Release's `python3 -B chroma-release/v22_checks.py --level fast --only @game --repo <checkout>` | a few minutes |
| page source (`web/src/`) | rebuild `web/index.html`; with no change meant, its md5 must not move | under 1 s |
| engine | Engine thread only: `chroma-engine/tools/t_steps.py` (about 20 s), then a Game re-pin with `chroma-game/tools/build.py` and Release's `chroma-release/same-lives.sh` (four parts, about 50 min each) | hours |
| Library or packs | the owner's build and checks, then the Game re-pin | owner's job |

If a proof that should match does not, stop and report it. Never update an expected hash to make a check pass.

## Never

- Edit `engine_pin/`, a built file, or a compiled Library file by hand.
- Edit another owner's folder without that owner's check (`CONTRIBUTING.md`, "Making a change").
- Force-push `main` or a `release/` branch, delete a `release/` branch, or delete any branch without Emren's word.
- Commit run outputs, caches, screenshots or anything over 50 MB, or make an `_archive/` folder here (it lives in the
  shared folder).
- Write to the shared folder's tracked files except through `tools/mirror.py`.
