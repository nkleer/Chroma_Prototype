# Chroma

A life simulator in which Magic's colour pie (White, Blue, Black, Red, Green) explains how one person grows over a
whole life. The game runs in the browser (Python in Pyodide) and is published as a claude.ai artifact:
https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju

## What this repository holds

Item 1 of the backend plan Emren accepted on 2026-10-08 (the project's `chroma-env/backend-plan.md`): versions and
branches here replace the folder copies kept in the project's shared folder.

Each `release/<version>` branch holds exactly the files that version is built from, at the same paths they have in the
shared folder, each byte-identical to that version's manifest there (`chroma-env/live-<version>-manifest.txt`); `main`
starts from the newest one and adds finished, checked work. Live now: **v22.1** (published 2026-10-08 13:10 UTC, artifact version 1791464842-7382; 464 files).

The main paths on `main`:

| Path | Owner thread | What |
|---|---|---|
| `chroma-game/prototype/` | Gamification | the game: Python code, page source and built page, `engine_pin/` (the pinned engine, Library and packs) |
| `chroma-engine/v22-speedpass/` | Engine | the live engine (v22's engine with the speed pass: same lives, faster) |
| `chroma-engine/v22-speedpass/rarity.json` | Engine | the rarity table the game's `rarity.py` is built from: on `main` the 10-08 rebuild for v22.2 (PR #30); live v22.1's table is `chroma-engine/prototype/calib_v8/rarity.json` (also on `release/v22.1`) |
| `chroma-engine/tools/` | Engine | the Engine's checks, which Release's rows run (`tools/README.md`) |
| `chroma-library/` | Library | the compiled Earth batch (`earth*.py`, `dreams.py`) and its `.lib` sources |
| `chroma-packs/` | Life pathways and content packs | core, politics (Packs v7), science, stage |
| `chroma-art/game/` | Visuals for the game | the pictures the page uses (`pictures.json`, `pics/`) |
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

`git diff release/v22 release/v22.1` shows everything v22.1 changed. How the threads work in this repository:
`CONTRIBUTING.md`. Notes, briefs, drafts, run outputs and Emren's uploads stay in the shared folder.
