# Chroma

A life simulator in which Magic's colour pie (White, Blue, Black, Red, Green) explains how one person grows over a
whole life. The game runs in the browser (Python in Pyodide) and is published as a claude.ai artifact:
https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju

## What this repository holds

Item 1 of the backend plan Emren accepted on 2026-10-08 (the project's `chroma-env/backend-plan.md`): versions and
branches here replace the folder copies kept in the project's shared folder.

`main` holds exactly the files the live version is built from, at the same paths they have in the shared folder, each
byte-identical to that version's manifest in the shared folder (`chroma-env/live-<version>-manifest.txt`). Live now:
**v22.1** (published 2026-10-08 13:10 UTC, artifact version 1791464842-7382; 464 files).

| Path | Owner thread | What |
|---|---|---|
| `chroma-game/prototype/` | Gamification | the game: Python code, page source and built page, `engine_pin/` (the pinned engine, Library and packs) |
| `chroma-engine/v22-speedpass/` | Engine | the live engine (v22's engine with the speed pass: same lives, faster) |
| `chroma-engine/prototype/calib_v8/rarity.json` | Engine | the rarity table the game's `rarity.py` came from |
| `chroma-library/` | Library | the compiled Earth batch (`earth*.py`, `dreams.py`) and its `.lib` sources |
| `chroma-packs/` | Life pathways and content packs | core, politics (Packs v7), science, stage |
| `chroma-art/game/` | Visuals for the game | the pictures the page uses (`pictures.json`, `pics/`) |
| `chroma-hud/sync21.py`, `pubmap.py` | Gamification | build and publish helpers |

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
