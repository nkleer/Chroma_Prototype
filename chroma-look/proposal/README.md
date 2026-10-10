# The ink look: proposal (2026-10-10)

Emren asked (10-10 07:06 UTC) for a major visual improvement to the game, with animations and consistent graphics, built in
parallel with v22.3 without changing it. This folder holds the proposal and its preview page. Nothing in it is wired
into the game.

Preview: https://claude.ai/artifact/4pwgcGpspuqWhuaYpFohkQ (thread "Visual improvement", started 10-10 07:06 UTC).

## The six ideas
1. One ink language: the frame redrawn in the pictures' engraving style (hatched meters, engraved wheel, stamped
   status labels, woodcut icons, paper grain and plate marks).
2. Living engravings: pictures print in, then lights flicker and the view drifts. Light positions come from the
   kit's scene code (tools/lights.js); no repaint.
3. Colour you can see move: the chosen card flips to its outcome and ink runs into the wheel, meters and life line.
4. Their own tarot card: an engraved portrait card that ages with the character (tools/scenes_portrait.js, a sketch).
5. Chapter plates: a plate turns in like a book page for big turns.
6. Engraved life line: hatched colour ribbons on night, a ruler of years, the fog kept.

## Files
- preview/src.html + preview/build.py: the preview page (build.py inlines assets/ and lights/).
- tools/lights.js: `node lights.js <scenes file> <name>...` prints each light (glow, lit window, beam) a scene draws.
  Reads the kit at /mnt/project-files/chroma-art/kit/; Playwright from /opt/node22.
- tools/scenes_portrait.js, tools/render_portrait.js: the four-age portrait sketch (350x500 WebP).
- tools/symbols.py: cuts a few ink glyphs (and the masks they use) out of chroma-art/game/ink-icons.svg.
- tools/tour.js: screenshots of the current build (start, moment, choosing, outcome).
