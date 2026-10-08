# Page changes after the overhaul drop-in (game thread, version 22)

The overhaul's own list is chroma-hud/impl/CHANGES.md. These came after it, in the game's copy of web/src.

- 10-07 (release check C-X3): on a wide screen (over 900 px), a card's reading no longer sits in a strip under the cards. It
  opens as a card over the picture in the story column, only while an option is hovered or has keyboard focus, and the idle
  hint is gone; the heading already says "hover to read". The reading never covers or catches an option and never moves the
  window. Windows under 880 px tall get tighter spacing in a moment, and Do nothing keeps to one line there. Styles only
  (head.html). The phone is unchanged: it never drew the strip.
- 10-07: "colour" changed to "color" in the page text, and the reading strip got `flex: none` (overhaul thread, app.js 2105a3d7eea3).
