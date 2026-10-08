# Chroma

A life simulator in which Magic's colour pie (White, Blue, Black, Red, Green) explains how one person grows over a
whole life. The game runs in the browser (Python in Pyodide) and is published as a claude.ai artifact:
https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju

## What this repository holds

Item 1 of the backend plan Emren accepted on 2026-10-08 (the project's `chroma-env/backend-plan.md`): versions and
branches here replace the folder copies kept in the project's shared folder.

The first commit, kept on the branch `release/v22`, is exactly the 456 files live v22 is built from (published 2026-10-07 20:48 UTC,
artifact version 1791406097-00ca), at the same paths they have in the shared folder, byte-identical to
`chroma-env/live-v22-manifest.txt`:

| Path | Owner thread | What |
|---|---|---|
| `chroma-game/prototype/` | Gamification | the game: Python code, page source and built page, `engine_pin/` (the pinned engine, Library and packs) |
| `chroma-engine/archive/live-v22/` | Engine | the live engine, frozen at go-live |
| `chroma-engine/prototype/calib_v8/rarity.json` | Engine | the rarity table the game's `rarity.py` came from |
| `chroma-library/` | Library | the compiled Earth batch (`earth*.py`, `dreams.py`) and its `.lib` sources |
| `chroma-packs/` | Life pathways and content packs | core, politics (Packs v7), science, stage |
| `chroma-art/game/` | Visuals for the game | the pictures the page uses (`pictures.json`, `pics/`) |
| `chroma-hud/sync21.py`, `pubmap.py` | Gamification | build and publish helpers |

## Versions

Each live version is a branch `release/<version>` that is never committed to again (this session cannot push git
tags, so release branches stand in for them). `main` is the newest live version plus finished work.

## Until v22.1 is live

The shared folder (`/mnt/project-files`) stays the working copy while v22.1 is built there. When v22.1 publishes, its
files are committed here and kept on `release/v22.1`; after that the threads move their work into this repository (branches per
version, a merge after each owner's checks pass) and the layout is tidied (backend plan items 1, 5 and 8). Notes,
briefs, drafts, run outputs and Emren's uploads stay in the shared folder.
