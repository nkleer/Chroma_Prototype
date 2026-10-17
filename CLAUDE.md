# Chroma: notes for Claude sessions

Chroma is a life simulator in which Magic's colour pie (W, U, B, R, G) explains how one person grows over a whole life.
The game runs in the browser (Python in Pyodide) as a claude.ai artifact. Branches, pull requests, owners,
`tools/mirror.py` and publishing are in `CONTRIBUTING.md`; follow it. These notes keep sessions cheap: most of the
repository's bytes are generated files and copies, and a whole life takes about two minutes to simulate.

## Who owns what

Each folder is its owner thread's; change another owner's only with that owner's check. `chroma-env/paths.py` names
every folder once, and scripts import it.

| Folder | Owner thread |
|---|---|
| `chroma-engine/v22-speedpass/`; `chroma-engine/tools/` (the checks Release runs) | Engine (`chroma-engine/CLAUDE.md`) |
| `chroma-game/prototype/` (but nobody edits `engine_pin/`); `chroma-game/tools/` (`build.py`, the one build command) | Gamification (`chroma-game/CLAUDE.md`) |
| `chroma-library/` (edit the `.lib` sources, not the compiled files) | Library |
| `chroma-packs/` | Life pathways and content packs |
| `chroma-art/` (`game/pics/` holds the pictures) | Visuals for the game |
| `chroma-look/tools/` | Game visuals overhaul |
| `chroma-release/` | Release |
| `chroma-env/`, `tools/`, root files (`env/<topic>` branches) | Workspace cleanup and setup |

## Files you never open whole

Generated or copied, never edited by hand. `.claude/settings.json` blocks reading the first five and the pictures;
`.ignore` keeps all of them out of searches (`rg` and the Grep tool honour it, `grep -r` does not); `.gitattributes`
keeps them out of `git diff`, `git show` and `git log -p`. In the shared folder `.ignore` also hides run outputs,
`_archive/` and the old and staging game copies. To search a hidden folder, name it: `rg <pattern> <folder>`.

- `chroma-game/prototype/engine_pin/**` (11 MB): the engine, Library and packs that `chroma-game/tools/build.py` pins.
  Read the owners' copies instead.
- `chroma-game/prototype/web/index.html` (1.3 MB, lines up to 254 KB): built from `web/src/` by
  `python3 -B chroma-game/prototype/web/src/build.py` (0.07 s, byte for byte). `web/page.html` (590 KB):
  `chroma-game/tools/webdir.py`.
- `chroma-game/prototype/web/src/ink-option-texts.json` (1.2 MB): a copy of `chroma-art/game/ink-option-texts.json`.
- `chroma-game/prototype/rarity.py` (101 KB): `chroma-game/tools/build.py`, from the game's `rarity.json`.
- `chroma-library/earth.py` (5.3 MB) and `earth_art.py`, `earth_play.py`, `earth_politics.py`, `earth_science.py`,
  `earth_stage.py`: compiled from the `.lib` sources by the Library's `build.py`. The Library's other `.py` files are
  hand-written and stay searchable.
- `chroma-art/game/lights.json` (177 KB): `chroma-look/tools/extract_lights.js`. `chroma-art/game/pics/*.webp`: the
  pictures.

## Reading

- Never read a file over about 1,500 lines whole. Find the place with `rg -n`, then read a range.
- Large files people do edit: in `chroma-engine/v22-speedpass/`, `engine.py` (6,672 lines), `world_people.py` (6,171)
  and `world.py` (4,205). The game and story layers are split into files of 126 to 965 lines, the page's script into 13
  parts of 93 to 501 lines and its style into 10 parts of 87 to 255 lines (`chroma-game/CLAUDE.md`).
- `chroma-game/prototype/HISTORY.md` is 60 KB of history. Read one section (`rg -n '^#' HISTORY.md`).
- Notes, plans, specs and run outputs live in the shared folder (`/mnt/project-files`), not here. Start from
  `chroma-env/MAP.md` there.

## Running

- Run Python with `-B`, so no `__pycache__` lands in the shared folder.
- Never run `chroma-game/prototype/play.py`: it waits on `input()` forever. Drive `console.Console` from a script, as
  `test/same_life.py` does: `c.handle(line)` returns `(text, busy)`; call `c.handle("")` while `busy`.
- Don't start a browser or Pyodide for an everyday change; the browser checks belong to Release.
- One core: a new life takes about 6 s to set up (about 2 s in `smoke.py` and `prove.py`, which keep burned-in worlds),
  a simulated year about 1.3 s, a whole life about 2 minutes. Release's statistical runs take 36 minutes to hours;
  don't start one for a small edit. Long runs go in a scratch folder.

## The proof ladder: the cheapest check that is enough

Every life must stay the same unless Emren asked for a change in play. Pick the row that fits the change.

| Change | Check | Time |
|---|---|---|
| docs, CLAUDE files, comments | none | 0 |
| any game change, first | `python3 -B chroma-game/prototype/test/smoke.py`: a short life, no crash, no NaN; `--same` also checks it plays exactly as `test/smoke.golden.json` | about 20 s |
| game code, no change in play meant | `python3 -B chroma-game/prototype/test/prove.py`: `smoke.py --same`, then presets 1 to 6 (seed 7) on the branch and on `origin/main`, compared step by step, main's lives from a shared cache | under 30 s cached, else about 4 min |
| game text | `test/text_check.py` after each edit (new real-world words against main); `test/timeless.py` once on the PR | 1 s; 7 to 9 min once |
| game content or behaviour | `smoke.py --update` (the PR says why play changed), `test/text_check.py`, `test/timeless.py`, `test/saveload.py`, then Release's `python3 -B chroma-release/v22_checks.py --level fast --only @game --repo <checkout>` | a few minutes |
| page source (`web/src/`) | rebuild `web/index.html`; with no change meant, `git status` must show it unchanged | under 1 s |
| engine | Engine thread only: `chroma-engine/tools/t_steps.py` (70 rows, about 65 min), then a Game re-pin with `chroma-game/tools/build.py` and Release's `chroma-release/same-lives.sh` (four parts, about 50 min each) | hours |
| Library or packs | the owner's build and checks, then the Game re-pin | owner's job |

If a proof that should match does not, stop and report it. Never update an expected hash to make a check pass.

## Never

- Edit `engine_pin/`, a built file, or a compiled Library file by hand.
- Edit another owner's folder without that owner's check (`CONTRIBUTING.md`, "Making a change").
- Force-push `main` or a `release/` branch, delete a `release/` branch, or delete any branch without Emren's word.
- Commit run outputs, caches, screenshots or anything over 50 MB, or make an `_archive/` folder here (it lives in the
  shared folder).
- Write to the shared folder's tracked files except through `tools/mirror.py`.
