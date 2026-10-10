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
- 10-10 (stage 2 item 2, light and shadow; chroma-ideas/shadows-mechanics.md §6 and §10): shown only while the engine's
  `shadows` switch is on (off in v22.2, so nothing changes on the page now). The wheel inks the end of each color's point
  with the visuals thread's hatch mask (`ci-hatch`, `ci-crosshatch` while the state shows), cut square at (1 - s) of the
  point's length; hovering a color adds its line ("Red 25%, a third of it in shadow: reckless") and the sources in words.
  The five shadow states sit beside the other states in the crest and the sheet, hatched, with their `ci-shadow-*` glyphs
  and a hover with the sources, whether they have seen it, and the on/off rule. Once seen, the heart's pick the shadow
  drives carries "their shadow pulls here". The words come from game.py (`shadow_view`, `shadow_pull`); display only.
- 10-10 (engine PRs #84 and #95, behind sph_levers and far_ties, both off): a lever act on the town's spheres is a story
  line of its own (tag `lever`, mark `L`: where it landed, what came of it, their standing there) and a dot on the World
  panel's line by what came of it, with the acts listed under "What they did in town" (panel `levers`). A close tie's news
  from their town is a line (tag `far`, mark `F`: what it meant for the tie), as is a tie taken into the household and how
  their stay ends; a want that came of such news shows why on the circle's hover (`want_why`). The acts and the news are
  game.py's words (`SPH_LEVER`, `FAR_SAY`) until the Library has its own; places, rungs and the events an office sets off
  are the Library's (earth_spheres.py). Nothing shows with the switches off.
