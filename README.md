# Chroma

A life simulator in which Magic's colour pie (White, Blue, Black, Red, Green) explains how one person grows over a
whole life. The game runs in the browser (Python in Pyodide) and is published as a claude.ai artifact:
https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju

## What this repository holds

Item 1 of the backend plan Emren accepted on 2026-10-08 (the project's `chroma-env/backend-plan.md`): versions and
branches here replace the folder copies kept in the project's shared folder.

Each `release/<version>` branch holds exactly the files that version is built from, at the same paths they have in the
shared folder, each byte-identical to that version's manifest there (`chroma-env/live-<version>-manifest.txt`); `main`
starts from the newest one and adds finished, checked work. Live now: **v22.3** (published 2026-10-10 19:52 UTC, artifact version 1791661954-7698; 814 live files).

The main paths on `main`:

| Path | Owner thread | What |
|---|---|---|
| `chroma-game/prototype/` | Gamification | the game: Python code, page source and built page, `engine_pin/` (the pinned engine, Library and packs) |
| `chroma-engine/v22-speedpass/` | Engine | the live engine (v22.3: v22.2's engine with the stage 2 refit, spheres and the K fixes) |
| `chroma-engine/v22-speedpass/rarity.json` | Engine | the rarity table the game's `rarity.py` is built from: v22.2's and v22.2.1's, the 10-08 rebuild (PR #30); v22.1's and v22's is `chroma-engine/prototype/calib_v8/rarity.json` |
| `chroma-engine/tools/` | Engine | the Engine's checks, which Release's rows run (`tools/README.md`) |
| `chroma-library/` | Library | the compiled Earth batch (`earth*.py`, `dreams.py`) and its `.lib` sources |
| `chroma-packs/` | Life pathways and content packs | core, politics (Packs v7), science, stage |
| `chroma-art/game/` | Visuals for the game | the pictures the page uses (`pictures.json`, `pics/`, `lights.json`) |
| `chroma-look/tools/` | Game visuals overhaul | the ink look's scripts: `extract_lights.js` makes `chroma-art/game/lights.json`, `tour.js` is Release's page tour (`tools/README.md`) |
| `chroma-game/tools/` | Gamification | `build.py` (one build command), `webdir.py` and `pubmap.py` (on `release/v22.1` these were `chroma-hud/sync21.py` and `pubmap.py`) |
| `chroma-env/paths.py` | Workspace cleanup and setup | every folder named once; scripts import it to read the tree they sit in (`CONTRIBUTING.md`, "Paths in scripts") |
| `chroma-release/` | What made it into v21 (release) | the release checks: `v22_checks.py` runs every owner's checks, `check_*.py`, `record.py`, the browser probes; records and outputs stay in the shared folder |

## Versions

Each live version is a branch `release/<version>` holding exactly that version's files (plus this README and
`.gitignore`) that is never committed to again (this session cannot push git
tags, so release branches stand in for them). `main` is the newest live version plus finished work.

| Branch | Version | Published | Artifact version |
|---|---|---|---|
| `release/v22` | v22 (456 files; its engine sat in `chroma-engine/archive/live-v22/`) | 2026-10-07 20:48 UTC | 1791406097-00ca |
| `release/v22.1` | v22.1 (464 files) | 2026-10-08 13:10 UTC | 1791464842-7382 |
| `release/v22.2` | v22.2: `main` at dc707f5, the whole repository then; its 474 live files are listed in `chroma-env/live-v22.2-manifest.txt` | 2026-10-09 21:39 UTC | 1791581971-b095 |
| `release/v22.2.1` | v22.2.1, the ink look and the clarity layer on v22.2's lives: `visual/v22.2.1` at 20e7d56 (`release/v22.2` plus the page and pictures); its 499 live files are listed in `chroma-env/live-v22.2.1-manifest.txt` | 2026-10-10 14:03 UTC | 1791640980-ccaa |
| `release/v22.3` | v22.3, stage 2 (spheres and the refit) with S1-S7 off: `main` at 1f63d7e; its 814 live files are listed in `chroma-env/live-v22.3-manifest.txt`. The page leaves out 77 rare moment pictures (`chroma-game/prototype/web/src/pics-left-out.json`) to fit the artifact's 511-file limit | 2026-10-10 19:52 UTC | 1791661954-7698 |

`git diff release/v22.2 release/v22.2.1 -- <path>` shows what a version changed in a path. How the threads work in this repository:
`CONTRIBUTING.md`. Notes, briefs, drafts, run outputs and Emren's uploads stay in the shared folder.
