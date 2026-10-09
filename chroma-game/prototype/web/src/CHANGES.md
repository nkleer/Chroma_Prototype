# Page changes after the overhaul drop-in (game thread, version 22)

The overhaul's own list is chroma-hud/impl/CHANGES.md. These came after it, in the game's copy of web/src.

- 10-07 (release check C-X3): on a wide screen (over 900 px), a card's reading no longer sits in a strip under the cards. It
  opens as a card over the picture in the story column, only while an option is hovered or has keyboard focus, and the idle
  hint is gone; the heading already says "hover to read". The reading never covers or catches an option and never moves the
  window. Windows under 880 px tall get tighter spacing in a moment, and Do nothing keeps to one line there. Styles only
  (head.html). The phone is unchanged: it never drew the strip.
- 10-07: "colour" changed to "color" in the page text, and the reading strip got `flex: none` (overhaul thread, app.js 2105a3d7eea3).
- 10-09 (implementation list item 1, Emren 10-08 21:44 and 10-09): the end of a life shows the life as one paragraph under
  the epitaph, told as a story from the yearly colors: steady stretches, swings between two identities (the colors held
  all along and the one that came and went), drifts (which color grew, which faded) and what turned them (a death close
  by, a title, a rare world event). The rarest things the life met are told where they fell, and it closes on how
  content and at peace they were across the decades. Built by game.py's `life_paragraph()` (review["story"]); app.js
  shows it, head.html styles it (`.review .lifep`). The words are built in for now; the Library's wording replaces them.
