# Page changes after the overhaul drop-in (game thread, version 22)

The overhaul's own list is chroma-hud/impl/CHANGES.md. These came after it, in the game's copy of web/src.

- 10-07 (release check C-X3): on a wide screen (over 900 px), a card's reading no longer sits in a strip under the cards. It
  opens as a card over the picture in the story column, only while an option is hovered or has keyboard focus, and the idle
  hint is gone; the heading already says "hover to read". The reading never covers or catches an option and never moves the
  window. Windows under 880 px tall get tighter spacing in a moment, and Do nothing keeps to one line there. Styles only
  (head.html). The phone is unchanged: it never drew the strip.
- 10-07: "colour" changed to "color" in the page text, and the reading strip got `flex: none` (overhaul thread, app.js 2105a3d7eea3).
- 10-09 (implementation list item 1, Emren 10-08 21:44 and 10-09): the end of a life shows the life as a bard's song
  under the epitaph, in stanzas: an invocation with epithets from the two colors they lived by; each turn told as a
  metamorphosis (the color that rose and the one that fell, each with its image) with what turned them; swings between two
  identities as a ship between two winds; the rarest things the life met, where they fell; the bitter and sweet decades and
  their peace; the player's pushes as the gods' hand; their death; and the bards singing it where the cups are filled.
  Built by game.py's `life_paragraph()` (review["story"]); app.js shows it, head.html styles it (`.review .lifep`, stanzas
  kept). The words are built in for now; the Library's wording replaces them.
