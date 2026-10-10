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
  Every choice of words is read from the life, not drawn at random (Emren 10-09): the opening follows the lead color
  (Ovid's for a life of four or more shapes), the images follow the colors that rose, fell or flickered, the turns follow
  their cause and size, a stanza of deeds tells the colors of the ways they acted at the player's moments, how often they
  succeeded and where the player's pushes leaned, and the close follows the shape of their contentment, their losses,
  their long shots, the peace reading and the lead color.
  Built by game.py's `life_paragraph()` (review["story"]); app.js shows it, head.html styles it (`.review .lifep`, stanzas
  kept). The words are built in for now; the Library's wording replaces them.
- 10-09 (implementation list v22, stage 1): the song's words are now the Library's (chroma-library/earth_story.py `SONG`,
  with `SONG_WORLD` for the tribal and magic worlds and `MARK_SAY` for the deeds), key for key; game.py keeps its own words
  as a fallback when the pin lacks the file. After the song comes the last conversation with the voice (`LAST_TALK`): what
  it gave and what it cost, by the character's trust in the player per color, and whether they were glad of it. It has no
  place of its own on the page yet, so it is the song's last stanza and also `review["last_talk"]`. earth_story.py and
  earth_play.py are pinned in engine_pin/ and listed in the worker's sources; earth_play.py is only pinned, never loaded.
- 10-10 (thread "Visual improvement", Emren 10-10 07:30 UTC "Implement all six"): the ink look, a layer that changes no
  lives. `look.css` and `look.js` come after app.js in the built page (build.py); look.js wraps spiderSVG, drawLine,
  animSpider, renderHud, renderTable, renderResolution, addFeed, renderReview, renderTools and openSheet, runs each
  original first and its own part inside `safe()`. The frame is drawn in the pictures' engraving style (paper grain,
  double-ruled cards with ink roundels, hatched meters, wheel and river ribbons, stamped labels); pictures print in and
  their lights flicker (chroma-art/game/lights.json); an outcome turns over and its ink flies into the wheel, which then
  counts to its new values with the change beside each color and meter; the character has a tarot portrait by lead color
  and age (pictures.json `portrait`, 20 new pictures) in the crest, the sheet, the plates and the end; chapter plates
  mark the start, a first identity, a long shot made, a title and the end. For choosing: the gem shows the odds (high,
  middle, low), a storm corner marks a card against the grain, and a lean wheel shows where the hovered card would pull
  the colors. Table menu: Look (ink, classic) and Motion (full, calm, off). Tools in chroma-look/tools.
