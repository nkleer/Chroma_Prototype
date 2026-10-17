# Chroma text prototype (game thread)

One life, five colors, on the engine's go-live files with the Library's modern Earth batch, the three content packs
(Science, Politics, Stage and Screen) and the Library's dreams. The player sets the scene, follows the life as a story,
and at checkpoints lets the character choose or pushes them to an option.

## Play

- Browser: the "Chroma Life Console" artifact (https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju) runs
  these same files with Python and numpy inside the page.
- Terminal: `python3 play.py` here (needs Python 3 and numpy).

Keys: Enter lives on to the next checkpoint; w, m, y, d step a week, month, year, ten years; s shows
status (position, demand, inertia, accelerator, skill, belief, lens, voice, satisfaction, peace, resources,
titles); f changes how often checkpoints come; v changes how much the story tells; l shows the numbers under
the story (ledger); n starts a new life. At a checkpoint, Enter lets them choose (*), a number pushes them,
i shows what may follow (the heart's and the head's share of each option, and why). After each choice the
resolution ("what came of it") waits; Enter goes on. p makes or drops a plan (adults only).

## Where things are

- The module map, the page, the build and which test proves what: `../CLAUDE.md` (chroma-game/CLAUDE.md).
- The rules for every session (generated files, the proof ladder): the repository's root `CLAUDE.md`.
- How the game grew, version by version up to 2026-10-09: `HISTORY.md` (what this README held until 2026-10-17).
  Later changes are in the pull requests and in the shared folder's `chroma-game/CHANGELOG.md`.
