# Chroma text prototype (game thread)

One life, five colors, on the engine's go-live files with the Library's modern Earth batch, the three content packs
(Science, Politics, Stage and Screen) and the Library's dreams. The player sets the scene, follows the life as a story,
and at checkpoints lets the character choose or pushes them to an option.

## Play

- Browser: the "Chroma Life Console" artifact (https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju, version 22) runs
  these same files with Python and numpy inside the page.
- Terminal: `python3 play.py` here (needs Python 3 and numpy).

Keys: Enter lives on to the next checkpoint; w, m, y, d step a week, month, year, ten years; s shows
status (position, demand, inertia, accelerator, skill, belief, lens, voice, satisfaction, peace, resources,
titles); f changes how often checkpoints come; v changes how much the story tells; l shows the numbers under
the story (ledger); n starts a new life. At a checkpoint, Enter lets them choose (*), a number pushes them,
i shows what may follow (the heart's and the head's share of each option, and why). After each choice the
resolution ("what came of it") waits; Enter goes on. p makes or drops a plan (adults only).

## Files

- `engine_pin/`: a pinned copy of the engine thread's engine.py, library.py, combos.py, batch.py, earth_rules.py,
  foresee.py and explain.py, of the Library's earth.py, earth_perks_titles.py, earth_voice.py, earth_science.py,
  earth_politics.py, earth_stage.py and dreams.py, and of the packs' files in packs/ (schwartz.py and life.py kept for
  reference; see PINNED.txt). Never edited.
- `worldview.py`: the outer world as the player sees it (world panel, world lines in the story, the cast circle,
  reach, lever chips); names people, places and eras. See the last section.
- `link.py`: loads the pinned engine and adds `run_steps()`, a copy of `run()` with six pause points
  (week, situation, choose, odds, learn, end). Loading fails loudly if an anchor line is missing.
- `story.py`: the built-in story layer (see below).
- `game.py`: the game layer (setup, checkpoints, forced-pick costs, life-event timing, status, review); it hands
  every engine event to story.py.
- `console.py`: the text controller shared by the terminal and the browser page.
- `play.py`: the terminal loop.

## What the game adds on top of the engine (candidates to move into the engine)

- Single-life stepping, a checkpoint signal, player override, felt and true odds before the choice,
  and narration from the engine's per-life events log, all through the pause points above.
- Forced picks: reluctance = 1 - exp(-(own utility - pick utility) / 0.7). It lowers the true odds
  (effort), adds stress and pent-up pressure toward what they wanted, and keeps only part of the
  learning (40% at full reluctance). Forcing an out-of-reach option adds risk and can backfire
  (stress, money).
- Checkpoints on engine v6 (pinned 2026-10-05): life events now come at the engine's own real yearly rates
  (personal rate, context drivers, refractory ramp), and every other week is everyday life, mostly "an ordinary
  week". The game's v5 stopgap clock (EVENT_YEARS, CONTEXT) is gone. Because everyday situations now fill most
  weeks, a life event this week counts as more important (+0.5) and may come sooner after the last checkpoint;
  an everyday situation waits longer each time it has already been a checkpoint, so checkpoints stay varied
  (about 22 / 46 / 107 per life at rare / normal / often). Status shows the engine's own context on the
  "around them" line. The default world is the engine's v6 default: mild tension on Magic's five questions.
- A chosen family faith replaces the engine's random inherited faith profile.

## The story layer (story.py)

Emren, 2026-10-04: the log read like incident reports. The life is now told as a story, with built-in lines
only (no generated text, so nothing waits), in a "Mixed" voice: a present-tense narrator plus the character's
own thoughts in *italics*.

- Scenes for all 23 situations, two variants per color for the frequent ones, filled with a cast of named
  people: parents, grandparents, a sibling, friends, a rival, mentors, bosses and colleagues, partners and
  children. People are introduced the first time the player meets them; a bereavement takes someone real
  (grandparents first, then parents, later friends), and the dead stay dead.
- The narration follows the character's colors. Almost every passage has a variant per color, and the one
  told is drawn by the character's voice: 40% who they are now, 60% a memory of who they have been that fades
  over about three years (Emren 23:02). As the identity drifts, the emphasis of the telling drifts with it, and a line marks
  the shift once it has really happened. The chapter header names the identity the voice reflects.
- Thoughts before an act speak for the act's colors (the motive); thoughts after an outcome speak through the
  voice (how the character reads it); a forced pick gets a reluctant thought.
- Each year opens with a short chapter: how the year felt (satisfaction and peace bands, each told through the
  voice), what drives them now, and where the ordinary weeks went.
- Outside events, eras, commitments, clashes, rites of passage, conversions and breakthroughs all have lines.
  Quiet detail tells only checkpoints and life events; normal adds notable events and big moments.
- Key l (ledger) prints the old numeric lines under the story.
- Emren's answers (23:02): the voice's memory of past identities fades over 3 years; chapter headers name the
  identity with a short phrase ("Izzet, the restless inventor"); the setting is chosen at the start: modern
  Earth (default), tribal or a world of magic (presets 5 and 6, or Build your own). Lines that belong to one
  setting carry a world letter (E, T, M); the engine runs the same rules in each until the library's tribal and
  magic worlds land.

## Browser build

Published as the artifact https://claude.ai/artifact/KC9Q3XfqxQrJWCp3AcdMju. The page's sources are in `web/src/`
(head.html, sprite.svg, body.html, app.js); `python3 web/src/build.py` joins them into `web/index.html`. `web/index.html` (the page) and
`web/worker.js` (runs Python in a Web Worker) are kept here. The other published files are Pyodide 0.27.7
(pyodide.js, pyodide.asm.js, pyodide.asm.wasm, pyodide-lock.json), python_stdlib.zip and the numpy 2.0.2
Pyodide wheel (both as base64 text, since the host serves no .zip or .whl), and the .py files above under
`py/` (worker.js lists them in SOURCES). To update the game, copy the changed .py files to `py/` and republish to the same URL; the Pyodide
files can be read back from the artifact.

## Engine v6 in the story (2026-10-05)

- Tension rebounds: when a checkpoint act joins colors the world sets against each other, the outcome adds
  whether the two fit together ("*Both! Why did nobody tell me I could have both?*") or tore.
- After the year's hardest blow (top tenth of years, at most every four years), the chapter says whether the
  people around them carried them through (support, the engine's heal loop) or whether they bore it alone and
  hardened (the harden loop).
- Streaks of trouble or fortune (the engine's loss and gain spirals) get a line, at most every five years.
- Fresh starts: a breakthrough near a round birthday or soon after a move says so; a second move within a year
  is told as moving again.
- Ready for the Library's modern Earth batch: role slots {sibling} and {partner} (a cousin or a companion when
  there is none), {dead} outside a death scene means someone already gone, and moment(..., kills=role) names
  who dies, as the Library's kills: field will.

## The modern Earth batch (2026-10-05)

- Modern Earth lives (presets 1 to 4, and Build your own with Modern Earth) run on the Library's batch, loaded
  through the engine's `batch.load_batch("earth")` with `batch.LIB_DIR` pointed at engine_pin/. Tribal and magic
  settings keep the engine's base library and the game's own world flavor until the Library writes them.
- story.load_library_story() reads the batch's own story fields: scenes per color, outcomes, each option's act
  wording, read events (festivals, news, weather) with per-color readings, and grief moments. The game's own
  scenes only fill in where the batch has none.
- Options show their means and ends colors (`[W>G]`: done the White way, for Green ends).
- People: kills: names who dies in a scene (and the engine's quiet grandparent deaths are told later as a
  short line); echoes bring back the same person as the act they answer; a break-up or a job change told by the
  scene is not told twice; a friend who moves away, or the friends left behind when the family moves, no longer
  turn up as the friend down the street.
- The engine's new events are told: deaths (the role and who is left), marks, readings of public events (at
  most one told every 39 weeks, the same event at most every five years), and a new job after losing one.

## The browser screen: HUD v2, "arcane night" (2026-10-05)

Emren 08:02 chose the look: a card table under an arcane night sky, one screen in three parts with unseen dividers, Magic-style
option cards, and the story as the main text with the mechanics behind it on hover. Artifact version 12.

- **The whole life (top).** A river of the five colors by age, swelling when life is satisfying; an identity ribbon above it
  (who they were each year); glyphs for the life's big events (deaths, titles, moves, rites, breakthroughs, checkpoints);
  a glowing "now". Everything after now is drifting fog ("unwritten"), because the end is unknown; it clears when the life
  ends. Hover a year for its colors and mood; click a year or a glyph to read it in the story. Data: `hud()["river"]`
  (one row per year: age, W U B R G, satisfaction, peace, identity) and the feed.
- **The moment (centre).** The chronicle of the life by year (older years fold), and at a checkpoint the scene in a glowing
  panel with the options dealt as Magic-style cards: name and mana cost (the act's ways), art in the colors of its end,
  type line "Act — Order/Knowledge/Power/Freedom/Harmony" (Unthought or Out-of-reach when so), a star for the stakes, the
  rules text, their reason as flavour on their own card (gold foil), possible gains and losses as icons, how sure they feel
  with a reality arrow, and reluctance dots. Hover a card for what may follow; it also lights the wheel's colors it serves.
- **The character (right; a drawer below 1040px).** Identity crest, color wheel, four rings (content, peace, strain,
  wanting with its breaking mark), means as segmented bars, five title sockets (filled ring = years held; pulsing = clash;
  room for the perks and titles catalogue to come), people as initials coloured by kind, the world around them, temperament.
- **Story markers.** story.py wraps the telling parts of its text in `⟦kind:payload⟧text⟦/⟧` (list at `mk()` in story.py:
  people, acts, the act they wanted, thoughts, values, mood, the year's weeks, how news landed, readings, titles, rebounds,
  aftermaths, streaks, temperament, rites, breakthroughs). The page colours them and explains them on hover with the
  numbers from the feed (an act's felt odds and reality, colors and means it moved, the surprise). `console.handle()`
  strips them, so the terminal is unchanged. `test/markers.py` checks they are balanced and never reach the terminal.
- Feed items carry extra details for this: `dw` (colors moved this week, in points), `dres` (means moved), `delta`,
  `felt`/`real` on choices; `took`/`message` on outside events; `expects` on titles; `wound`/`support`; `streak`; the cast
  has `id`, `met` and `seen`. Tests: `test/markers.py`, `test/fuzz.py`, and `test/drive_hud2.js` (Playwright; local
  server `test/serve.py`).

## Engine v7 in the game (2026-10-05, artifact version 13)

Emren 08:15: the player should see the character's own view of the options before a choice, with an inner-voice hint
("I feel this one most, but this option looks more logical, but I don't care"), and after the choice a resolution: what
happened, who it touched, how the character and their world changed, and a small hint at how the world works. The engine
built it as explain.py and foresee.py (chroma-engine/v7-handoff.md); the game shows it.

- **Before a choice (explain.before at the "choose" pause).** The moment header carries a heart-and-head tug bar (how much
  the head decides: learned discipline, stage, stress, peace). Under the scene, the inner voice says what the heart wants,
  what the head picks and which wins (keys agree, heart_over_head, head_over_heart, torn, dream_calls, duty, need_first,
  habit, becoming, time_short, want_but_doubt, stuck), plus up to two asides (stressed, a blind spot, out of reach,
  hopeful, gloomy, short horizon...). When their own pick is neither, an extra aside says so ("a third way"). Cards wear a
  heart and a head badge; hovering a card shows both shares with their drivers (motives, habit, needs, role, goals,
  horizon; values, becoming, odds...). Felt odds stay the number; reality is only explain's word band ("more often than
  not") with why they misread it (hope, gloom, self-belief, a headwind they do not see). Felt odds show as 1 to 99%.
- **After a choice (explain.snapshot, then explain.after at "end").** game.advance returns "resolved" after the choice
  week and holds there: the panel "What came of it" shows whether it worked against what they expected, whose choice it was
  (heart, head, a push, a third way), regret, the scene's outcome, the people in it, the week's changes as chips ("more
  strained", "lonelier", "more capable"), the color bars that moved, the guild they are drifting toward ("Dimir, on the
  way") and one or two lessons ("How the world works"). Enter or Go on continues. The chronicle entry keeps small chips
  for the same.
- **Dreams, passions and plans.** Goal events are told (a dream begins, becomes a passion or a plan, is reached, let go,
  not reached in time, pushed aside), with the trigger in the setting's words (a parent, a teacher, a book or a parade).
  The HUD lists them under "Dreams and plans": passions first, then plans (felt odds, progress, due age), then dreams.
- **Making a plan (key p, button "Make a plan"; adults).** Pick a horizon (a year, five years, a life), then a life domain
  or a mix of colors; the preview shows how sure the character feels and, roughly, how often plans like it come true
  (foresee.preview), with what the feeling leaves out. Making it calls foresee.add_plan: the character holds it and does
  not drop it alone; d1, d2... drops one. Domains already held (a career they have) are closed.
- **Story markers added:** i (inner voice), j (aside), g (goal), z (a change), y (closer to a guild), n (a lesson).
- Tests: test/markers.py (4 lives, balanced, no leaks), test/fuzz.py (6 lives, 0 errors, plan keys included),
  test/drive_v7.js (Playwright: voice, card hover, resolution, plan dialog; 1280x860 and 400x860). Shots:
  chroma-game/shots/v7-*.png.
- Not yet: the Library's color-voiced VOICE and LESSONS lines (the engine's plain defaults show until then), titles and
  perks (the engine is building them now; the five title sockets are ready).


## Emren's nine points, game side (2026-10-05, artifact versions 14 and 15)

Emren's points of 09:25 (relayed by the coordinator). The game took 1 to 4, the screen side of 7 and 8, and brought in the
visuals thread's icons for 5. The engine takes the mechanics of 3's adjectives, 7, 8 and 9; the Library takes 6.

- **1. Readable text.** The story, HUD, event window and tooltips are parchment panels with dark ink (`.paper` scopes the
  token overrides; every white highlight in the CSS is `rgb(var(--hl) / a)`, so paper panels get warm brown highlights).
- **2 and 4. An event window instead of cards (Paradox style).** A choice opens a pop-up over the life (`#evwrap`,
  `.ev`): a header (age, title, heart-and-head tug, stakes), the scene's picture area and text with the inner voice on
  the left, the options as full-width rows on the right (plate tinted by the end color with an icon and the key number,
  the whole title, colors, needs met, what it could start, how they feel about it, felt odds and the reality arrow).
  Rows are grouped: what they consider, ways they haven't thought of, out of reach. Footer: let them choose, a legend,
  "Look at the life" (closes the window until "Back to the moment"). "What came of it" uses the same window. Phones get
  it full screen with a sticky header.
- **3. Percentages and words.** Every 0..1 quantity reaches the player as a percent; strain is a percent of the most they
  can bear, wanting a percent of the way to breaking through ("100%+" past it). "Around them" shows words per context
  ("money: comfortable", "health: frail") instead of +0.5. Up to five states read from the numbers sit under the crest
  (happy, at peace, restless, stressed, excited, wealthy, broke, lonely, well loved, hemmed in, on a lucky streak...;
  game.STATES, one per variable, children skip money and wanting). The engine will make such adjectives conditions.
- **5. Icons.** The visuals thread's set (chroma-art/game/icons.svg and icons.json; game-icons.net, CC BY 3.0, credits in
  the help box) is inlined by web/src/build.py. Feed and timeline glyphs by tag, title kinds, means, needs, goals,
  people, the four rings; the picture area shows the moment's first life domain (else its tier); an option plate shows
  the icon drawn for that very option, else what the act is (a title it starts, money, the mark it leaves), else the
  color's mana symbol. Pictures come later from the same thread.
- **7. "Would go with it" and "okay with it".** game.reluctance() was rewritten (GAME rel_*). The gap below the best
  option they see is read against the moment's typical gap; "against it" means against who they are (the option's end
  colors are enemies of their identity colors and share none; clash_with()) or far below doing nothing. Rows and
  tooltips say "would go with it", "okay with it", "reluctant", "against it" or "their own pick"; the tooltip names the
  enemy color. The forced-pick cost uses the same number. test/acceptance.py over 16 lives (about 820 moments): of the
  options they see, 27% would go, 59% okay, 8% reluctant, 6% against; 1% of moments read reluctant or against for 70% or
  more of the options (a first try from the best option alone: 36%, because the engine's utility gaps grow to 4 to 8 in
  later life for everything outside the character's colors). Forced picks cost far less than in version 13.
- **8. Odds.** Felt odds show as 1 to 99% with the reality arrow and word band; their bunching near 50% is the engine's
  (chroma-engine/points-8-9.md).
- **9. Content over a life.** Played lives (own picks and half forced) follow the engine's U and do not fall steadily;
  sent to the engine through the coordinator.
- Tests: test/fuzz.py (6 lives, 0 errors), test/markers.py (clean), test/acceptance.py, test/drive_v14.js (1280x860 and
  400x860: no page overflow, no clipped option titles), test/drive_against.js. Shots: chroma-game/shots/v14-*.png.
- The engine pin is unchanged (v7 of 08:53). The engine's titles and perks are inert until the catalogue is approved, and
  its work on points 7 to 9 is in progress, so the next re-pin waits for that hand-off.

## The engine's points 3, 7, 8 and 9, and the event pictures (2026-10-05, artifact version 16)

- **Re-pin** (engine_pin/PINNED.txt): engine.py, batch.py, earth_rules.py, explain.py and foresee.py from the engine's points
  hand-off (chroma-engine/points-handoff.md). link.py's anchors still match. Titles and perks come along and stay off until
  chroma-library/earth_perks_titles.py exists.
- **How they feel (point 7) is now the engine's.** explain.before gives each option `accept` (level, clash, fit,
  reluctance); game._view takes the level as the word ("against" reads "against it") and the reluctance as the cost of a
  push, and recomputes the shown odds with it. "Okay with it" and "would go with it" cost nothing; reluctant and against
  cost weaker effort, strain and pent-up wanting. The game's own rule (reluctance(), clash_with()) remains for options
  before() leaves out, and clash_with() still names the enemy color on hover. Clash follows the world's framing: in the
  neutral world (preset 3) no colors are opposed, so nothing reads reluctant or against for its colors. test/acceptance.py
  in the default mild world, 12 lives (about 620 moments): 37% would go, 49% okay, 10% reluctant, 5% against of the
  options they see; at most 1% of moments read reluctant or against for 70% or more of them.
- **States (point 3) are the engine's adjectives** (engine.ADJECTIVES, read at every pause from `adj`): the HUD row under
  the crest (game.ADJ_LOOK gives icon and tone; the tooltip says what it is read from and for how long). After a choice,
  states that began or ended that week are told ("Lale is lonely now.", "no longer low") and shown as chips. The game's
  own STATES list remains only as a fallback.
- **Point 8 and plans:** felt odds read more of the moment, and plans no longer feel certain (engine and foresee); nothing
  to change in the game.
- **Pictures (point 5):** the visuals thread's 95 engravings (chroma-art/game/pics, pictures.json) show in the event
  window and in "What came of it": by situation, then the original of a child version, then the first life domain, then
  the tier (app.js picFor; game sends variant_of in cp.art). They publish as pics/*.webp next to the page; web/src/build.py
  inlines the map. Without them the page shows the colors and a glyph.
- Tests: fuzz (12 lives, 0 errors), markers (clean), acceptance.py, drive_v14.js and drive_against.js at 1280x860 and
  400x860. Shots: chroma-game/shots/v16-*.png.

## Titles and perks in play (2026-10-05, artifact version 17)

Emren 12:05: "Use this title and perk ideas and implement it to the game. If possible, add related actions/events,
whatever necessary." The Library writes the catalogue and the acts around it; the engine gives and takes titles and perks
(chroma-engine/roles-handoff.md); the game shows them. Built against the Library's first draft (71 titles, 80 perks; see
engine_pin/PINNED.txt). Emren's 100 new titles come in with the next pin, when the engine hands off profiles and facets and
the expanded catalogue is approved.

- **HUD.** Each life-domain socket shows the title held in it (nurse, married, parent, on the team; a community holds up to
  three, shown "+2"); its tooltip lists the titles, their ways, what the first one brings (+meaning, −time) and how long it
  has been held. Statuses (graduate, widowed, new in town, someone with a record) sit under the sockets. A Perks section
  lists perks tinted by their first way: held, on hold (suspended, dashed) or rusty (a skill or credential no longer held
  that still helps while it fades). game.roles() reads r_has, r_since, p_acc, p_sus and p_lev at every pause; role_info()
  gives the words. Terminal: status text lines `title`, `status`, `perks`.
- **Options.** What an option needs and the character lacks (explain.before `needs`: a title, a perk or a state) reads
  "only if Lale can drive", with what stands in the way (law, approval, means) on hover. Perks that help it (`helped_by`)
  are listed on hover with the points each adds; the row names one only when it sets the option apart (a perk that helps
  most options of the moment says little on each row). What an act can give or take (the Library's act fields title,
  grants, drops, takes, suspends and their _if_fails, from ROLES A_FX) shows as chips (+ nurse, − car; if-fails in
  italics) and on hover as "If it works: Lale is a nurse from then on." The shown odds now include the perks' help
  (pbump), as the engine counts it.
- **Story.** Title and perk events are told in the chronicle with a hoverable phrase (marker o: name|kind|ways|title|points
  |state): "Lale is a nurse now.", "Lale can swim now.", "Out of practice, Lale can no longer draw.", status lines of
  their own ("Lale comes home a veteran.", "Half a year on, Lale is still out of work."). A title that comes with a
  commitment started that week is told in the same line ("Lale takes up work as a waiter."; adoptive, foster and
  stepparent starts get their own lines). Levels: titles always; perks at the normal level, and a perk told within the
  last five years again only at the most detailed; losses the commitment's line already tells, titles replaced by the
  next, and grants that came with a title are not told again (game.ROLE_QUIET). About 70 title and perk events a life;
  40 to 50 are told at the normal level (two test lives: 52 and 39).
- **After a choice**, titles and perks gained or lost that week show as chips in "What came of it", and the engine's
  lessons (title_gain, status_gain, title_loss, perk_gain, perk_loss, perk_helped) say how the world works.
- **Acts and events:** the Earth batch has no act fields yet (the Library's next pass adds title:, grants:, takes: and
  requires: to the acts), so needs and act gains show only once it lands. They were tested with stand-in act fields
  (shots v17-option-gains.png and v17-phone-options.png use stand-ins, not the Library's acts).
- Future (engine hand-off pending): title profiles (two or three ways to hold a title, "reshaped" when the person moves
  between them) and facets (newlywed on top of married) will show as the profile's words and as a qualifier.
- Tests: fuzz (12 lives, 0 errors), markers (o: 144, balanced, no leaks), test/roles.py (a life's title and perk lines),
  test/drive_roles.js at 1280x860 and 390x844 (no page errors; the phone page no longer scrolls sideways: the step
  buttons were 7px too wide). Shots: chroma-game/shots/v17-*.png.

## Chroma's own icons (2026-10-05, artifact version 18)

Emren chose "All ours" on the visuals thread's card (15:36): the page draws every glyph from Chroma's own woodcut set
(chroma-art/game/ink-icons.svg and ink-icons.json, ids "ci-..."), and the game-icons.net set and its credits line are gone.

- web/src/build.py inlines ink-icons.svg whole (some glyphs carve details with masks in its defs) and embeds its map.
  app.js treats "ci-" like the old "gi-" (class gx: fill currentColor, no stroke); the credits line shows only when the
  icon set has a credit (it has none now).
- Color signs: the five colors' own glyphs (map.color: pillar, eye, crown, flame, sprout) replace the page's older mana
  symbols in pips, the wheel's orbs, an option's fallback icon and the picture's glyph (`MANA(c)` in app.js).
- Titles, statuses and perks (PERK_ICON, STATUS_ICON in app.js) and the states (ADJ_LOOK and STATES in game.py) use ci- ids.
- Option icons: the set draws one per option of the Library's audited batch (staged order; the texts it was drawn for
  are kept in web/src/ink-option-texts.json). web/src/live_icons.py writes option-icons-live.json for the batch the game
  runs: an icon is kept where the option's text is the text it was drawn for (live batch: 2,227 of 2,500), else null, and
  the page falls back to the act's icon or the color's sign. Re-run it after every re-pin of earth.py, then build.py.
- Shots: shots/v18-ink-options.png, shots/v18-ink-hud.png.

## Titles volume 2 and the audited Earth batch (2026-10-05, artifact version 19)

Emren 17:51: "Publish with that way, no change now. We can change it later, note." Then "Go live now" on the Library's
card at 18:22. Emren's review notes on the batch come later. Re-pinned all six files together, as
chroma-engine/titles-v2-handoff.md says (engine_pin/PINNED.txt):
- the engine's profiles and facets, chance, perks volume 2, retirement, faith drift and engagements;
- the Library's audited batch (324 situations, 3,560 options, each with a `chance`);
- the catalogue (173 titles with Emren's 100, 165 perks).
Prepared and tested beforehand in chroma-game/staging/ (README there).

- Facets (newlywed, single parent, grandparent, raising a child in more than one language...) sit on their title.
  - The socket shows them under the title name ("Parent / two languages"); the tooltip says "Parent, raising a child in
    more than one language".
  - A facet that comes the same week as its title is not told again. One that ends with its title is not told at all.
- Profiles: a title's way of being held shows as "Their way" in tooltips. A change of profile is told: "Ari is still a
  doctor, and now helps people regain control over decisions affecting their lives."
- Loss reasons lead the line: "After missed payments, Ari is no longer good for a loan." (story.LOSS_LEAD).
- The Library's chance shows in the option tooltip as "For most people: it works about 7 times in 10". The terminal's i
  view says "most people manage this about 7 times in 10".
- Faith:
  - A faith that quietly stops mattering (the engine's `drifted`) is told as such: "Somewhere along the way, what Ari
    believed in stops mattering to them."
  - A cause is told as a cause: "Ari takes up a cause. Ari is an activist now."
- New statuses have their own lines and icons ("Ari earns a doctorate.", "Ari moves into a care home.").
- Out of work now reads "A year on, Ari is still out of work."
- Sockets: long words are set smaller, and 26 long titles have short socket names (SOCK_WORD), so all 173 fit two lines.
- Perks fold after 12, with a "+N more" chip (a life holds about 25 over its course).
- Option icons: every one of the 3,560 options has its drawn icon (version 20, below).
- The 13 new pictures (108 in all) publish with the page.
- Fixed on the way: a dream's source mid-sentence is lower case ("After someone they meet, ...", "After their teacher
  Hester, ...").
- Tests: test/fuzz.py (6 lives, 0 errors), markers.py, roles.py, roles2.py; drive_roles.js, drive_facet.js and
  drive_perks.js at 1280 and 390 wide.
- Shots: shots/v19-hud.png, v19-socktip.png, v19-perktip.png, v19-facet.png, v19-perks-phone.png.

## Foster care picture and option icons (2026-10-05, artifact version 20)

- Visuals drew "going into foster care" (picture and option icons; chroma-art/game/pictures.json now maps 80 situations).
- The option-icon stopgap is gone: Visuals checked map.option against the live earth.py (356 moments, 3,560 options),
  and the game checked it too (every moment's options in the drawn order, no empty icon, every icon in the sheet). So
  web/src/option-icons-live.json is deleted and build.py uses map.option as it is. If Emren's review rewords options
  later, run web/src/live_icons.py again until Visuals redraws (it writes the json back and build.py picks it up).
- 109 pictures publish with the page. Shot: shots/v20-options.png.

## Emren's 16 points, game side (version 21, published 2026-10-06 16:51 UTC at the one go-live)

Version 21 went live at the one go-live (16:48 UTC, with the end-of-life fix at 17:20 UTC: page history 22);
prototype/ matched it until the final version's work began (see the last section).

- Point 1, the interlude: between choices a slow card shows the weeks passing: an everyday routine line (routine.py:
  210 modern Earth lines, 56 tribal, 59 magic, picked by age, world, what is held and the season), a picture, the
  season and age, and the spider graph drifting week by week. Pace "slow" (default), "short" or "off" with the i key;
  remembered in the browser. Enter, Space or Escape skips.
- Point 2: the HUD spider animates through the weekly trace (hud.trace: [t, w x5, want x5] per week), not a jump.
- E9 (release round 10-07): each weekly trace row also carries the five bands from explain.bands (one letter each: i in,
  f fading, r rising, o out) and the identity label from E.identity, so the spider eases its band rings and label week
  by week: hud.trace rows are [t, w x5, want x5, bands, label]. Older rows of 11 still read. There is one identity
  rule: the label is E.identity(colors now, M, Game._prev_label), the buffer carried year by year as the engine's own
  identity_path does; the trace, the HUD and the sheet all apply it, so the spider and the crest never name two
  identities at one moment. (Carrying the buffer week by week was tried and dropped: it doubled the identities a life
  passes through, away from the engine's yearly path and the Book's rarity.)
- Point 3: every "around them" chip shows its value as a percent, "(+12%)".
- Point 4: hovers are exact definitions. States: the variable, where it begins and ends over the last three months,
  how common it is among adults. Around them: how the engine computes it and where each word begins. Colors: the
  share and the join/leave rule. Generic footers are gone.
- Point 5: one type scale, --fs-1..5 = 12, 14, 17, 22, 34 px. Spectral for text and display, IBM Plex Sans Condensed
  for the interface, Cinzel only for the logo.
- Point 7, screen side: the color wheel is now a spider graph: now (filled), wants (dashed), holds (inertia + 0.2),
  the pull arrows (thicker when acceleration is higher) and the 18-22% band where a color joins or leaves. Each key
  word's hover gives its exact meaning. The bands come from explain.dynamics at each pause; a weekly band feed is
  release row E9, with the Engine.
- Point 9: Save (s) writes a .json file through the page's downloads capability (else a copy box); Load (o) replays
  the recorded inputs deterministically; New life (n) offers to save first. An autosave lets the start screen offer
  "Continue". test/saveload.py checks that a replayed life matches in every value.
- Point 10: the start screen is a tarot spread with the Visuals thread's plates (tarot-1..7.webp): 0 The Crossroads
  (build your own), I The Cradle, II The Village, III The Library, IV The Streets, V The River, VI The Spires. A
  card's reading sits below; hover or tap reads it, a second click or tap begins. On a phone The Crossroads is a wide
  card above two rows of three.
- Point 13: the character sheet (c): colors, inner life, needs met, means, temperament, states with definitions,
  around them, titles, statuses and perks, dreams and plans, people, and who they have been.
- Point 14: the color map uses the engine's label and draws the .18/.22 band.
- Point 16: Chroma's own names for every combination (game.IDENT_NAME, 31 names): The Guardian (W), The Seeker (U),
  The Striver (B), The Free Spirit (R), The Rooted (G), ... The Whole (WUBRG). Magic's names stay in the tooltip.

Tests: test/fuzz.py 5 lives 0 errors; markers.py clean; roles.py; saveload.py (replay identical). Browser at 1360
and 400 wide (touch): no page errors, no sideways scroll; save, new life and Continue give the same age and colors.

### The game's aim: the Book of Moments and the peace reading (Emren chose "Book and peace", 21:44)

Points 11 and 15: a life is witnessed, not scored (chroma-game/aim-draft.md).
- The peace reading, at the end of each life: how well they lived (satisfaction and peace, averaged from 18 on) and how
  much the life was their own (true to self: 1 minus the mean reluctance of the choices the player pushed; their
  gifts: at each choice, their skill in the chosen act's ways over their best skill). game.peace_reading picks one of
  nine sentences (PEACE_WORDS) from two bands (PEACE_BANDS, checked by test/peace_bands.py on the final pin over 36
  played lives: well .49-.77 with a third high and a sixth low; own .94-.99 when the player never pushes, .76-.88 when
  they push 70% of the choices). The review shows the sentence and four gauges with exact definitions.
- The Book of Moments (key b, the Book button, the start screen once a life is in it, "Open the Book" on the review):
  what every life has met, kept in this browser (localStorage chroma.book; the catalogue in chroma.bookcat). Moments
  (situations and life events), rare ones starred; deeds (the engine's marks); titles ever held; identities lived (the
  31 names); worlds; lives with their reading. Game.book() sends this life's record with each moment, resolution and
  the end; the page merges it by life id (seed, name, world, start age), so a replayed or reloaded life never counts
  twice. book_catalog() sends a world's catalogue once.
- Rarity: rarity.py is the engine's chroma-engine/prototype/calib_v8/rarity.json, copied at each re-pin: the share
  of 1,200 simulated modern Earth lives (the four Earth presets, birth to 80, packs on) that meet each moment, deed and
  title at least once. test/rarity_build.py was the game's own stopgap before the engine published it. Rare = fewer
  than 1 life in 10. Tribal and magic moments have no rarity yet.
- test/book_check.py plays lives and checks the record against the catalogue.
- Long shots (Emren 2026-10-06, packs thread: any title can be pushed for at long odds, and a miss is a story of its own):
  a chosen act that gives a title if it works, when it works for fewer than 1 in 10 people (game.LONG_SHOT, the Library's
  chance; career, community and faith titles), or when failing grants the packs' long-shot perk (grants_if_fails:). The
  outcome card tags it ("a long shot, missed: 3 in 100"), the review names each one under the peace reading ("At 41, they
  tried to become a member of parliament against odds of 3 in 100, and missed. The trying was theirs."), and the Book
  keeps it starred under Long shots (keys l|made|<title> and l|missed|<title>). Today's batch has none; the packs bring
  them. test/longshot_check.py and test/drive_longshot.js (a scratch copy with LONG_SHOT .5 shows the whole path).
- Long shots as a climb (Emren 2026-10-06 09:18: no big title from nothing; steps, commitment, repeated tries): the
  packs reworked long shots into bold tries at the next rung or one skipped rung. The game records the rung the person
  stood on (the title that brought them to the moment, explain.title_held_index, and years on it) and which try this is
  for that title: "At 47, after 9 years as a city councillor, they tried a second time to become a member of parliament
  against odds of 4 in 100, and made it." The outcome card adds "try 2" and a "from <rung>, N years" tag. Second tries
  name `title: {missed}` (batch.MISSED_TITLE): game._role_fx reads it from the engine's missed_t; kind:<kind> drops
  (batch.KIND_ACT) are not shown as chips.
- Content packs at the go-live: worker.js SOURCES lists engine_pin/earth_<pack>.py and engine_pin/packs/core/*.py and
  packs/<pack>/{catalogue,roles,helps}.py for science, politics and stage. golive_pin.sh (in chroma-game/staging-v21/)
  copies them with the engine's files and the live Library batch, checks batch.PACKS is on, and writes rarity.py from
  the engine's calib_v8/rarity.json (same keys). MODE=staged runs the same pin on staging/next2 as a dry run.
- A life that ends in the very week of a choice (the engine stops right after the pick): decide() writes the review and
  advance() returns "over" at once. Before this fix (published 2026-10-06 16:51), a season moment in that last week
  came back as the same checkpoint with no review, about 1 life in 70. test/end_at_choice.py; test/life_ends.py plays
  lives and reports any that stop early or hit a console error, with the traceback.
- Peace bands with the three packs (2026-10-06, 48 lives, test/peace_bands.py 16): well .46-.74, about 2 in 5 high,
  2 in 5 mid, 1 in 5 low; own all high when the player never pushes, mostly mid at push .7. PEACE_BANDS kept as they were.
- Timeless modern days (Emren 2026-10-06 10:42): no calendar year, real brand or platform, real war or historical event,
  real country or real person on screen; technology is a generic modern kit. The game's own text (story.py, routine.py,
  game.py, the page) has none; chapter headings and the timeline count age, never dates. test/timeless.py plays lives
  and scans every string the page could show; run it at the go-live re-pin with the packs.

Published as version 21 at 16:48 UTC: the page with capabilities {downloads: true}, the .py files (text/plain) and
the 7 tarot-*.webp from chroma-art/game/pics/.

### The engine's next hand-off in version 21 (chroma-engine/next-handoff.md, final, pinned 2026-10-06 00:10)

engine.py, batch.py, earth_rules.py and explain.py are the engine's final files for this hand-off (point 7 landed: turning
points on, sat_gap_ref .12). earth.py and earth_perks_titles.py are the Library's next batch, live since the go-live
(16:25 UTC): the new engine and that batch go together, since the engine's relapse rule needs the batch's gap:. The
Science, Politics and Stage and Screen packs were pinned with them (engine_pin/PINNED-golive.txt).
- Sex at setup (P["sex"]): a step in Build your own (female, male, or chance); presets let the engine draw it. The sheet
  says "a woman" or "a man". Attraction and unease stay inside the engine; the Library's moments tell them.
- Own death (P["self_death"]): off while the past is simulated and in childhood, on from the later of the start age and
  16 (game.DEATH_FROM, a game default). The engine reads P live, so the game switches it on in the running locals. A
  death ends the life at once: "Mira dies at 47, after choosing to ..." or "of an illness", then the review, which says
  how the life ended. The Book keeps the life with its age at death.
- Seasons of change (Emren's point 6, explain.season): a chip under the identity on the HUD ("Crossing into young
  adulthood · the in-between", or "Becoming a nurse · settling in") with its step and weeks, and a line on the moment
  that belongs to a season; the transforming chance says "A turning point of this season: this choice can change who
  they become." Every moment of a season is a checkpoint whatever the pacing (game._checkpoint), so a crossing is
  never a quiet level-up. On the next batch every stage season opens at the ages its moments are written for, and
  6 to 15 season moments with 3 to 5 transforming chances reach a played life (test/next2_check.py, season_rate.py).
- {title}: filled from explain.title_held in scenes, lines and option labels (story.fill and the option labels), and act
  fields on {title} (batch.TITLE_HELD) resolve with explain.title_held_index in _role_fx.
- The spider graph takes inertia and acceleration from explain.dynamics. Each color's orb shows its band (a dashed ring:
  fading, held only by the edge; a bright ring: rising), a soft ring marks a window of openness, and the color hover
  gives its place. The sheet adds "Holds: deep / habit / roles" rows and "Open to change".
- Test scripts updated for the extra setup step (fuzz.py, markers.py).
- Content packs (Emren's point 8; one go-live with the Earth batch, Science, Politics and Stage and Screen): game.PACKS
  (None = the engine's approved batch.PACKS) and batch.PACK_DIR = engine_pin/packs. To pin a pack: chroma-packs/core/
  reach.py to engine_pin/packs/core/, the pack's catalogue.py, roles.py and helps.py to engine_pin/packs/<pack>/, the
  Library's earth_<pack>.py to engine_pin/; add every one to web/worker.js SOURCES (the worker makes the folders) and
  publish them as text/plain; rebuild rarity.py. Tried with the staged Science pack in a scratch copy: lives play with
  0 errors, its moments come as choices in some lives, and the page loads it in the browser with no errors. Pack
  moments without their own picture take their life domain's or tier's.

## The final version, version 22 (Emren 2026-10-06 22:24 UTC: one version with everything up to 22:00 UTC and the dreams)

Held until the coordinator said the full version was assembled and every check in chroma-release/checklist.md had
passed (row C-X3, 2026-10-07); published 2026-10-07 20:48 UTC with the Library's and the Engine's go-live (last section).

- Dreams (release rows D3 and G3): engine_pin/dreams.py is the Library's dreams (Emren "fine", 22:19 UTC), in the
  worker's SOURCES. The engine names each dream after the Library's nearest entry; the game tells the spark with the
  trigger's say line ("A firefighter visits the school and lets Mira sit up in the cab of the engine. From that day
  Mira dreams of ..." with the engine's dream name), names a dream again when a new spark feeds one already held, and names passions, plans and life
  goals in the Library's words (story.goal_words, dream_of, life_words). The goal hover shows the dream a passion or
  plan grew from. Tribal and magic lives read the same dreams (game.with_dreams).
- Outer world (rows G2 and W41): worldview.py and the page's World panel (key g) show the public record only: the era
  by Chroma's own name ("the Lawkeeper years"), published figures, government and polls, laws and rights, wars,
  disasters, pandemics, figures as the character reads them, and a timeline beside the life. Big public events and
  the smaller ones that touch the character come as lines in the story. The HUD shows the cast circle by layer and
  felt reach per ring with the reality hint; options that push the world carry a lever chip, and what came of it says
  what the push did. It reads the Engine's world.py (section below); test/mock_world.py stood in before it came (test
  only, never published), and test/drive_world.js still drives it in a patched copy. What the game asked of the Engine:
  chroma-game/world-hooks-for-engine.md.
- ROLE_QUIET "time passed" is back to 1, and game.LONG_SHOT reads the engine's DEFAULT["long_shot"] (rows G5, G6).

## Emren's six points of 01:57 (Emren's time; 2026-10-06 22:57 UTC), game side, in version 22

- N1 sex and gender (spec chroma-identity/for-the-game.md, N1d). Build your own, step 2 "Sex at birth": female, male,
  intersex or chance, each with a hover saying it is the body only, not who they will be or whom they love. The sheet
  (game.gender_view) shows "Born", "Knows themselves as", "Drawn to" and "What their world expects" (role_strict and
  role fit), each row only from the week the engine finds it (found_id); never chosen, never changed by acts. The
  engine's own names are read through game.ID_LOCAL (found_id, RS0, AT0, rfit_avg, named_g, came_o). Two-word titles
  take the character's own word (gword: wife or husband); {seen_as} in scenes is how the world reads them. Naming
  their gender offers a new name (rename keeps the life's id); "came out" and "named their gender" are starred in
  the Book of Moments. test/identity_check.py checks it all in a life.
- N2a the unwritten years are a fabric of stars: chroma-art's texture.unwritten_future behind the fog, breathing
  slowly (head.html .fog .fab).
- N2b the identity ribbon blends each identity into the next, and a thin thread runs on into the fog from who
  they are now.
- N3 the event window: a choice shows "trying..." at once (feedback in about 0.1 s), the outcome comes in the same
  window after a short beat, and Go on closes it (about 0.3 s). Checked by test/probe_popup2.js.
- N4 the Eldest perk at five is the Engine's (birth order), not the game's.
- N5 no ">" between an action's colors: one set of pips, no order between its way and its ends.
- N6 autosave after every moment and choice into one slot in this browser (localStorage "chroma.autosave"), on by
  default, key a turns it off; Continue on the start screen opens it.
- Also: a child's death (Engine R15) greys the child in the family and gets a plain line of its own (story.DEATH_CHILD);
  tool labels in the top bar fold to icons below 1440 px.

## The Engine's outer world in the game (chroma-engine/world.py, world_people.py, world_link.py; P["world"])

game.py turns the world on for Earth lives when the engine has it (WORLD_ON, P["world"], P["world_cfg"]). The week's
state carries the link as WL; worldview.EngineWorld reads it into the shapes test/mock_world.py stood in for: the
public record (from_engine maps each domain and kind to a panel entry, t in the life's weeks), the snapshot (era,
government, economy, laws, rights, figures, place), the cast (cast_view) and reach (reach_view). What the player sees:
- the timeline keeps big events, the country's own news, and local news only from places the character has lived,
  newest 300 (worldview.NATIONAL, HIST_MAX);
- the circle shows layers 1 to 4, the dead only when they were close or kin; strangers seen once (layer 0) never;
- reach per ring shows the Engine's felt reach (0 to 1) and its reality hint in words (REACH_HINT);
- big events of the week come as story lines once (EngineWorld.news, local ones only from home); the copy the engine
  also puts in each life's events is skipped. Non-big events that touch them come from the life's events (WL.story):
  their own town's disaster or crime wave, their own workplace or school, or where their people live or work, worded
  by kind (worldview.SELF_TAIL; a school, unit, congregation or workplace by INST_SELF and INST_TOUCH; who_word). A
  changed law is told in plain words per law and state (worldview.LAW_SAY). A council vote is for the detailed story only.
  One public figure's news is told at most once in eight years (Game.NEWS_GAP); the timeline keeps all of it;
- every public figure has a name of their own (WorldView.fig: the seeded name unless an earlier figure has it);
- every place in one country has a name of its own (worldview.place_name: Earth's 15 localities take 15 of HOME's 30
  names in a seeded order). Emigration (W35-3): when WorldLink switches to a neighbour's World, the record is read from
  the arrival on, its places and figures are keyed apart (loc_key, FIG_SOC) and named from ABROAD; the story says
  "moves abroad, to X, a city in Y" and "comes home", and the panel shows the society, status and language
  (test/abroad_check.py);
- W40: a character who becomes head of government leads the world's government (the panel names them, the timeline
  marks "becomes head of government" and "leaves office").
The family is the world's (Game._kin_sync, after each week's news, at most monthly): the birthplace and the siblings at
the birth (older, in the world's sexes) are in the birth line; a younger sibling born later is told ("kin" lines); a
sibling or grandparent the world lost is said goodbye to if the engine's own death record has not come within
KIN_WAIT weeks. A later child (R15) is told as one more child; a scene that already held a newborn names the same
child; a partner's end told by its moment ("broke up") still ends it among the story's people; a partner's death
without a widowed commitment is told as a death. test/kin_check.py compares the story, the engine's alive columns
and the world's cast every 5 years.
Setup (Build your own): "Which world" (fresh, the world an earlier life left behind, or as its grandchild; the world
is kept in the browser's IndexedDB, newest three, and travels in the save file), "The times" (world_cfg pace) and
"Technology" (tech_level). Memories that come back: a logged act's recall is told once per episode, at most one every
RECALL_GAP years (Game._recall).
A life to 41 runs about 25% slower with the world on (seed 1: 52 s against 42 s), within budget.

## Version 22, published 2026-10-07 20:48 UTC (23:48 Emren's time)

The final version above, with the new look and the release round's fixes, published to the same link on the
coordinator's word (artifact version id 1791406097-00ca; capability downloads kept; 287 files: the page, worker.js,
35 .py as text/plain, 244 pictures, Pyodide). prototype/ is this build; v21's copy is chroma-game/prototype-v21.
- The new look (Emren chose Parchment and the Grid, 2026-10-07 10:19 UTC): chroma-hud/impl/CHANGES.md lists all 15
  changes. What it changes in the sections above: a tarot card opens its reading with the name field and Begin (a
  double click or the card's number key still begins at once); the settings keys f, v, l, i, a, s, o, n sit in the
  Table menu as well as on the keyboard; the desktop interlude moves the crest's wheel instead of a second one; the
  character sheet (c) is in tabs (Portrait, Colors, Inner life, Around them, Ledger); options are two-column cards
  numbered in the order shown, and number keys follow those numbers (CPNUM maps them back to the engine's).
- The reading of a card (release check C-X3, web/src/CHANGES.md): on a screen over 900 px wide it opens as a card over
  the picture in the story column while an option is hovered or has keyboard focus; it never covers or catches an
  option. Windows under 880 px tall get tighter spacing in a moment. Styles only (web/src/head.html).
- Game.decide() finds the chosen option by cp["by_idx"]; v21 used the option's place in the list, which can differ
  from the engine's own option number.
- The final pin (row G1, 2026-10-07 16:19Z, engine_pin/PINNED-final.txt): the Engine's files with the outer world, the
  Library's batch (527 situations, 5,615 options) with dreams, and the packs, with politics at v7: parliament and minister
  reachable in every game for the right habits and choices, rare (about 1 in 250 lives for a member of parliament, 1 in
  1,000 for a minister). rarity.py is the engine's calib_v8/rarity.json of that pin.
- Checks before the publish (chroma-release/checklist.md): C-G1 20 of 20 (test/markers.py now walks every Build your
  own step), the 9 browser drivers with 0 page errors, test/wasm_check.js, 24 steered lives, and the reading's fit
  probes test/probe_fit_cx3.js and test/probe_fit_geo.js at 1280x800, 1280x720 and 1024x768. After it, C-G4 on the live
  files: every worker SOURCE equals prototype/, every picture present.
- Known for the next version: when the mouse leaves one card, the reading of a card that has keyboard focus closes
  (fixed in version 22.1, below).
- To publish again: chroma-game/staging-final/ keeps sync21.py (build the page and the py folder) and pubmap.py (the
  files list: pictures, worker.js, .py as text/plain); publish the page to the same link without capabilities, so
  downloads stays.


## Version 22.1 (Emren 2026-10-08 10:47 UTC: the v22 health list, as recommended; no new features)

Clean, solid and fast, with the same lives as version 22:
- The Engine's speed pass (chroma-engine/v22-speedpass, SPEEDPASS.md): engine.py, world.py, world_link.py and
  world_people.py re-pinned; every other pinned file as before (engine_pin/PINNED-v22.1.txt). Same lives: whole lives
  in all six settings played through the page's bridge give the same record step for step (test/same_life.py).
- A tribal or magic life shows its world's own tarot card (V The River, VI The Spires) where an Earth picture would
  show: the moment and outcome cards, the waiting card and the everyday interlude (worldCard in app.js; v22 showed no
  picture on those moments and modern Earth pictures in the interlude). Earth lives are unchanged (test/world_pics.js).
- When the mouse leaves a card, the reading goes back to the card that has keyboard focus, or a card still under the
  mouse, before it goes idle (test/focus_check.js).
- Windows 760 px tall or less get tighter spacing in a moment, so eleven options fit at 1280x720 without scrolling
  (head.html; test/fit720_lab.js measures it). A sixteen-option moment can still scroll there.
- The help screen (h) lists g, the World panel.
- Saves from version 22 load (test/save_carry.js: the autosave's Continue and a saved file).