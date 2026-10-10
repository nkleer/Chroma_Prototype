# The ink look: its tools

The ink look (Emren, thread "Visual improvement", 10-10 07:30 UTC: "Implement all six") is a layer over the page that
changes no lives. Its code is in the game's page sources; this folder holds the scripts that make its data.

## Where it lives

- `chroma-game/prototype/web/src/look.css` and `look.js`: appended after `app.js` by `web/src/build.py`. `look.js` wraps
  a few of app.js's top-level functions (each call runs the original first; every addition runs inside `safe()`, so an
  error in the look never stops the game) and reads app.js's globals. It never changes the state a life is played from.
- `chroma-art/game/lights.json`: where each picture's lights are (made by `extract_lights.js`, packed into look.js by
  build.py).
- `chroma-art/game/pictures.json` key `portrait` and `chroma-art/game/pics/portrait-<w|u|b|r|g>-<child|youth|adult|elder>.webp`:
  the character's own tarot card (made by `render_portraits.js`).

## What the player sees

1. One ink language: paper grain, double-ruled cards with ink roundels, hatched meters and wheel, stamped labels.
2. Living engravings: pictures print in, their candles, lamps and windows flicker, the plate breathes slowly.
3. Color you can see move: the outcome card turns, its ink flies into the wheel, the wheel and meters count to their new
   values with the change floating beside them.
4. Their own tarot card: a portrait that follows the lead color and ages (child under 13, youth under 26, adult under 60,
   elder), in the crest, the character sheet, plates and the end of the life.
5. Chapter plates: a page turns in for the start of a life, the first time an identity is taken, a long shot made, a
   title gained and the end. Any key or click dismisses it; it never takes a click.
6. Engraved life line: hatched color ribbons on the river.

Helpers for choosing: odds tint each card's gem (high, middle, low), a hatched storm corner marks a card that goes
against the grain, and a small lean wheel on the picture (and on the wide-screen reading card) points where the
hovered card would pull the colors (solid for what it is for, dashed for how it is done).

Settings (the Table menu, saved in the browser): Look `ink` or `classic` (`html[data-look]`, key `chroma.look`) and
Motion `full`, `calm` or `off` (`html[data-motion]`, key `chroma.motion`). Off and the system's reduced-motion setting
stop every animation.

## Rules it keeps

- Every page id and class the drivers use stays. Overlays take no pointer events. Nothing clickable carries an endless
  transform. Picture lights stay inside their picture.
- Checks: `chroma-game/prototype/test/probe_fit_cx3.js` and `probe_fit_geo.js` (covered 0, blocked 0, moved 0, no
  stall, no page error), the Release fast checks for the game, and a tour (`tour.js`) at desktop and phone size.

## The scripts

All take Playwright from `require('playwright')` or `/opt/node22/lib/node_modules/playwright`. The drawing kit
(`chroma-art/kit/engrave.js`, `props*.js`, `scenes_*.js`) is only in the shared folder; it is read, never written.

- `extract_lights.js`: `node extract_lights.js <kit dir> <pictures dir> <out json>` reads every scene the pictures were
  drawn from and records each light it paints (glows, lit windows and screens, candles, beams), without repainting.
  Run it again when the Visuals thread adds or redraws pictures: `node chroma-look/tools/extract_lights.js
  /mnt/project-files/chroma-art/kit chroma-art/game/pics chroma-art/game/lights.json`, then rebuild the page.
- `scenes_portrait.js`, `render_portraits.js`: the 20 portrait cards. `OUT=<a scratch folder> node
  chroma-look/tools/render_portraits.js [portrait-w-child ...]` paints each on the 880x500 stage, keeps the card
  window and saves it at 420x600 under 45 KB, with PNG previews and a contact sheet in `OUT/png/`; copy the `.webp`
  files into `chroma-art/game/pics/`. `KIT` names another kit copy.
- `tour.js`: `node chroma-look/tools/tour.js <url of a served build> <out dir> [width] [height]` takes screenshots of
  the start spread, the first screen, a moment and an outcome, and prints any page error.
