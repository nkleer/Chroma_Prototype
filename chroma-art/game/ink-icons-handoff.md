# Chroma's own icons: switching the game over (visuals thread, 2026-10-05 15:45 UTC)

Emren chose "All ours" (15:36): the game's icons become our own woodcut glyphs, and the game-icons.net set and its
credits drop out. Review page: https://claude.ai/artifact/1rf6ziXg6FqYcrPKNR9FzE

## Files (chroma-art/game/)

- `ink-icons.svg`: one sprite, 238 `<symbol id="ci-...">` (viewBox 0 0 48 48, fill only, currentColor). Some glyphs carve
  their details with a `<mask>` that sits in the same sprite's `<defs>`, so inline the whole sprite once, as build.py
  already does with icons.svg. About 300 KB.
- `ink-icons.json`: the same shape as icons.json (about, credit, fallback_order, map, icons), with "ci-" ids. `credit` is
  null: no third-party art. The map has the same groups (tag, kind, res, need, goal, role, meter, setting, domain, tier,
  act, color, option), plus three tag keys the page already uses (moment, ledger, goal).
- `map.option` covers every situation and echo of the live batch (live since 18:22): 356 moments, 3,560 options, in
  option order. "going into foster care" was added at 18:35 (existing glyphs only, so ink-icons.svg is unchanged).
- icons.svg and icons.json (game-icons) moved to chroma-art/old/ after the game switched (v18, 15:54).

## What the game changes (tested with the page's own CSS rules)

1. build.py: read `ink-icons.json` and `ink-icons.svg` instead of `icons.json` and `icons.svg`.
2. app.js: let `isGi` accept the new prefix, so ci- icons get the same `gx` class (fill currentColor, stroke none):
   `const isGi = (name) => /^(gi|ci)-/.test(String(name || ""));`
   Without the gx class, `svg.i` would stroke the glyphs.
3. app.js, the credits line (`<p class="muted credits">Icons from game-icons.net ...`): drop it, or render it only when
   `GI_DATA.credit` is set (it is null now, so the current line would throw).
4. Optional: `map.color` (ci-color-w ... ci-color-g) are our own colour signs. They can replace the page's m-W..m-G
   symbols (pips, orbs, the mana fallback on option rows). Where those uses set `fill="var(--pInk)"`, give the use
   `class="gx"` and `color: var(--pInk)` instead, because gx forces fill to currentColor.

## v22 update (2026-10-06 23:25 UTC): every live option, packs included

- `ink-icons.svg`: 273 glyphs (238 before, plus 35 new: manuscript, script, folder, rubber-stamp, eraser, leaflet,
  ticket, rosette, chain-of-office, town-hall, knock, applause, laughing-face, crossed-fingers, target, ring-box,
  chef-hat, plane, spotlight, stage-curtain, radio, specimen-jar, gauge, server, clapperboard, film-camera, fishing-rod,
  staff, deer, feather, standing-stone, tribal-mask, spirit, wand, wagon). About 350 KB. Same ids for every old glyph.
- `ink-icons.json` `map.option`: all 786 moments of the live Library (earth.py 485 situations + 34 echoes,
  earth_science.py 68 + 4, earth_politics.py 95 + 4, earth_stage.py 90 + 6), 7,860 options, ten different icons in each
  moment. The tribal and magic wordings of an option share its icon.
- `map.domain` gains the 38 life domains the newer moments and the packs use (meaning, performing, learning, music,
  identity, cause, publiclife, any, ...), each on an existing glyph; `map.tier` gains `echo` (u-turn); `map.act` gains
  the six new marks (broke the law, came out, kept it hidden, used drugs, took a life, hurt someone badly).
- `ink-option-texts.json` (new here, V4): the option texts map.option was drawn for, in the same shape as
  web/src/ink-option-texts.json (`about`, `option`: moment -> texts in order), for all 786 moments. Copy it over the
  game's file.
- C-G2: `web/src/live_icons.py` loads only engine_pin/earth.py. Load the three pack modules too
  (earth_science, earth_politics, earth_stage), SITUATIONS and ECHOES of each. Checked here against both
  chroma-library/ and the game's current engine_pin/: all 7,860 options keep their drawn icon, none fall back.

## W42 update (2026-10-06 23:55 UTC): the outer world

282 glyphs (273 + 9 new); every earlier symbol and map entry is unchanged. New map groups in ink-icons.json, each
key -> one "ci-" id, following chroma-game/world-display-keys.md:

- `world`: public record kinds (era, recession, poll, election, law, right, war, disaster, pandemic, revolution, revival,
  tech, figure_rise/fall, scandal, figure_death, layoffs, closure, crime_wave, ...). Changed from the game's list:
  recession -> ci-chart-falling, local_election -> ci-town-hall, poll -> ci-talk, figure_rise -> ci-figure-rising,
  figure_fall -> ci-figure-falling. recession_over keeps ci-chart (a rising chart).
- `hazard` (engine world.HAZARDS, for disaster and local_disaster records that name one): flood ci-flood, fire ci-flame,
  quake ci-quake, storm ci-storm, heat ci-sun.
- `tech` (world_keys.TECH_KEYS): phone ci-phone, computer ci-laptop, internet ci-signal, video calls ci-screen, online
  dating ci-phone-heart, remote work ci-laptop, ai helper ci-chat-spark, modern medicine ci-pills, car ci-car,
  plane ci-plane.
- `lever`: exit ci-door-open, voice ci-megaphone, loyalty ci-anchor, neglect ci-shrug, subvert ci-domino-mask.
- `panel`: world ci-globe, push ci-crowd.

ci-quake and ci-figure-falling read best from 18 px up; at 13 px they still read as a split block and a figure tipping
off steps.

## V6 update (2026-10-07 00:10 UTC): the 27 outer-world moments (Library W39)

map.option now covers 813 moments (786 + 27): the civic moments, the eight era life events, the ten cast wants and the
migrant path from chroma-library/drafts/w39/*.lib, each with ten different icons, all from the existing 282 glyphs (no
new glyphs, the sprite is unchanged). ink-option-texts.json carries their option texts, so live_icons.py keeps them as
soon as the Library's batch has the same wording. map.domain adds duty (ci-helmet) and state (ci-town-hall), the two new
life domains these moments use. Every earlier entry is unchanged.

## V6 update 2 (2026-10-07 00:25 UTC): identity and roles (N1c), the pregnancy options (R14), a child's illness and death (R15)

map.option now covers 826 moments: + the 11 moments of chroma-library/drafts/new3/earth-identity-roles.lib, + the two
events of drafts/new3/earth-child-illness.lib, and 'a baby on the way, planned or not' grows from 10 to 15 icons (options
10 to 14 are the five drafts/next3/apply_r14.py appends before the moment's first works: line, in its order BG, UB, UR,
WG, WR). All from the existing 282 glyphs; the sprite is unchanged. ink-option-texts.json carries every new text in the
same order. map.act adds 'named their gender' (ci-hand-on-heart, as 'came out'). The nine options apply_n1c.py edits
change only their mark, not their wording, so their icons stay.

## Coverage on the staged batch (2026-10-07 01:13 UTC)

map.option and ink-option-texts.json now follow chroma-library/staging/next3/ (earth.py, earth_science.py,
earth_politics.py, earth_stage.py, situations and echoes; EVENTS_READ have no options): 837 moments, 8,375 options, every
option with its own icon, checked text by text against the staged modules. New: 11 moments (two Earth faith moments, five
Science, one Politics and three Stage events of Packs round 5). Changed: 98 options the Library reworded in 82 moments
(most dark acts rewritten as fair ones) got icons that fit the new words (kit/glyph/optmap3/fix_reworded.py). All from the
existing 282 glyphs; the sprite is unchanged.
