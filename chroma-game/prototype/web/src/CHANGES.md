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
  lives. `look.css` and `look.js` come after app.js in the built page (build.py); look.js wraps drawLine, renderScreen,
  animSpider, renderHud, renderTable, renderResolution, addFeed, renderReview, renderTools and openSheet, runs each
  original first and its own part inside `safe()`. The story and the cards are drawn in the pictures' engraving style
  (paper grain, double-ruled cards with ink roundels, stamped seals); the status panel keeps its minimal drawing and the
  life river its v22 bands, now lit like the fog (a breathing glow, a drifting nebula, a gleam from birth to now) with the
  old colors fading into the new when the life moves on (Emren 10-10 09:01 UTC); pictures print in and
  their lights flicker (chroma-art/game/lights.json); an outcome turns over and its ink flies into the wheel, which then
  counts to its new values with the change beside each color and meter; the character has a tarot portrait by lead color
  and age (pictures.json `portrait`, 20 new pictures) in the crest, the sheet, the plates and the end; chapter plates
  mark the start, a first identity, a long shot made, a title and the end. For choosing: the gem shows the odds (high,
  middle, low), a storm corner marks a card against the grain, and a lean wheel shows where the hovered card would pull
  the colors. Table menu: Look (ink, classic) and Motion (full, calm, off). Tools in chroma-look/tools.
- 10-10 (thread "Visual improvement", Emren 10-10 09:54 UTC): the start spread runs I The Cradle to VI The Spires with 0
  The Crossroads (Build your own) last. A click picks a card and puts the cursor in the name; nothing scrolls, a double
  click no longer begins, and once a card is clicked the mouse crossing the others no longer changes the reading. When
  the name would sit below the fold (a short window, a phone), the reading docks at the foot of the window. Enter or
  Begin starts the life. In look.js (wraps renderScreen) and look.css; app.js unchanged.
- 10-10 (thread "Visual improvement", Emren 10-10 10:53 UTC "apply everything to improve visual quality"): the status
  panel reads at a glance. A ▲ or ▼ beside a meter, a mean or a need that moved 4 points or more since a year ago (green
  when good for them, red when not, gold on wanting); a red glow on a meter or mean in a danger zone (satisfaction or
  peace under 20%, strain over 80%, a mean under 15%), gold on wanting close to breaking through; a dotted outline of
  their colors a year ago on the wheel (from the river; "A year ago" in the wheel's key); a line of the last years and
  the value a year ago in the hover of every meter, mean and need; a "?" on the crest with the key to these marks.
  look.js keeps a monthly history per life from the panel's own numbers; it wraps showTip and spiderSVG. app.js unchanged.
- 10-10 (thread "HUD and story flow check", Emren 10-10 10:25 UTC "apply all of them"): the clarity layer, in both looks,
  after look.js (`clarity.css`, `clarity.js`; app.js unchanged, no life changes). Why each part, measured over 17 played
  lives: chroma-hud/gameplay-check/findings.md in the shared folder.
  1. Quiet story: the voice's yearly line, the year's "times" line (it repeats a line already told), a memory whose moment
     is not told and an era they barely noticed leave the story. The interlude between moments ("These weeks") tells what
     happened in those weeks (moments, events, titles, eras) instead of routine lines. A told moment that moved a color by
     a point or more shows which, with arrows; the numbers are on hover.
  2. Voice crest: the voice row is one line: the voice icon (tinted by trust), the two colors the pushes moved most with
     their points, and a ring for the voice's share of how the colors changed. Its name, the trust and its latest line
     are on hover.
  3. One-line inner voice: the moment keeps its quote and "Left alone, they would"; heart and head are icons on their
     cards and in the reading; the tug's numbers are on hover; the outcome and the story drop the heart, head, third-way
     and regret tags, which change nothing in the life.
  4. The times where they count: no "with the times" badge; the reading of a push that costs something says what the
     times do to its cost (the only thing they change).
  5. Honest hovers: memories and moves no longer read as a public event; the sheet's Self-control is called Discipline.
  8. Fewer cards at once: at most five considered cards and Do nothing (their own pick, heart, head and marked cards
     first); the other considered ways and the ways they haven't thought of fold into a row each. Number keys still push
     folded cards; the open or shut state is remembered in this browser.
  9. Needs, + and −: a need's hover lists what lifts it and what pulls it down for this character now (means, titles,
     statuses, family care, acts, the weekly fade).
