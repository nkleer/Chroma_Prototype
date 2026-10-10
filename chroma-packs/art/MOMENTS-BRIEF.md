# Art and Writing pack: brief for the moment writers (Pathways and packs thread, 2026-10-10)

Status: a v22.4 slice of the planned Art and Writing pack (chroma-pack-ideas/next-packs.md), held in a PR until v22.3 is
live. Emren (10-10): red-led choices should lead to artist, and each life should see richer lanes at different depths.
The catalogue (titles and perks) is catalogue.py next to this file, the rules roles.py, the earned odds helps.py, the
other worlds worlds.py, the engine's conditions engine-conditions.py. The plan this follows is
chroma-packs/notes/v22.4-lanes-sizing.md, finding 2. Engine name: `art`. Moment files: art-*.lib in this folder.

The red road has four depths: taste ([open-mic poet], [life-drawing regular]), practice ([street artist], [illustrator
for hire]), profession ([painter or sculptor], or the base [novelist] for writing) and summit ([renowned artist],
[celebrated author], facets on the career held). The other colours each have a road: White [art teacher], Blue
[illustrator for hire] (the experimenter, U R), Black [gallery owner], Green [craft maker] (base) to [master
craftsperson]. [art school student] is a three-year status.

## Read first (all paths under /mnt/project-files unless they start with /home)

- chroma-library/SPEC.md, sections "Balance layout (per moment)" and "Writing an option" (the layout, chance:, v:,
  flags, marks, self_control).
- chroma-library/notes/library-spec.md and chroma-library/notes/writer-brief.md (the format, colours tagged faithfully,
  story fields).
- The build.py header (chroma-library/build.py, lines 1 to 60, and PAIRSETS / D for the life-event lines).
- The model, copy its shape exactly: the Stage and Screen pack, /home/claude/chroma_prototype/chroma-packs/stage/
  (stage-doors.lib for door pairs and echoes, stage-rungs.lib and stage-roads.lib for holder pairs, stage-events.lib
  for life events and the read event 'the reviews are in', stage-longshots.lib for long shots and their echoes,
  stage-worlds.lib for world-only events) and its MOMENTS-BRIEF.md ("Pack rules on top of the Library's",
  "Calibration lessons", "Balance layout").
- This pack's catalogue.py, roles.py and worlds.py (the tribal and magic forms below are its summary).

## Pack rules (on top of the Library's)

- Every name in title:, drops:, grants:, takes:, suspends:, requires:, holds: and aims: is a title or perk in this
  pack's catalogue.py, chroma-packs/core/*.py, or the base catalogue chroma-library/earth_perks_titles.py. Exact names.
  holds: may name several with "|".
- A door is an option that takes a title by the act (`title: street artist`). Its means colour fits one of that title's
  three profiles (they cover all five colours, so a door can be honest in every colour). Door options also carry
  `aims: <title>` on one or two options. Holder pairs (everyday moments with holds:) use `aims:` and never give a new
  title; they may `grants:` a perk plainly earned and `drops:` the title held.
- **The summits are facets.** [renowned artist] sits on [painter or sculptor], [street artist], [illustrator for hire]
  or [master craftsperson]; write `title: renowned artist` for people who hold one of those. [celebrated author] sits on
  [novelist]: `title: celebrated author`. For someone on the rung below without the career (a long shot that skips one
  rung), write the facet first: `title: renowned artist; painter or sculptor` or `title: celebrated author; novelist`.
- **Real chances** for an ordinary person who tries (the engine's earned-odds lifts in helps.py come on top; never write
  them higher): an art school place 40 to 55; a mural commission won 30 to 40; a first illustration commission 35 to 45;
  a first show that sells and makes a painter 20 to 30; an art teacher's post 45 to 55; a gallery that opens and lasts 30
  to 40; the guild's masterpiece passed 30 to 40; a publisher taking a manuscript 10 to 15; a work bought for the
  national collection 6 to 10; a national prize for writing 5 to 10; long shots 2 to 5. Inside a moment, every colour
  that tries for the same thing gets the same chance.
- A door closed by money or approval stays pickable: `requires: savings | without: means | lacking: .5` (a loan), never
  removed.
- Keep art real and unglamorous where it is: day jobs, rejections, unsold work, cold studios, deadlines, clients who pay
  late. Most artists and writers earn little from the work; a sale is a good month, not a finish line.
- **Wrongs are pickable** with plain labels and no preaching: a forgery signed with a dead painter's name, an idea taken
  from a friend's sketchbook, a friend's secret put in a book, a review written by a friend under another name, a wall
  painted without leave. Mark them (hid a wrong, broke your word, made an enemy, defied an authority) and give a closed:
  line with a real backfire (the dealer is arrested, the friend reads the book, the council fines you). Drink, drugs and
  burnout are possible, never forced, never the premise for someone who did not choose them. Integrity and vanity
  belong to every colour.
- **Each colour's honest road**: White's form and service (the class kept, the commission done to the letter, the art
  room open at lunch); Blue's method and invention (the study, the new technique, the clever brief); Black's ambition
  (the name, the dealer, the price, the rival outshone); Red's raw expression (the wall painted overnight, the poem read
  shaking, the work that has to be made); Green's rootedness (the town's own wall, the old craft, the work from the
  land and the family).
- **Content limits, never broken:** no sexual violence and no harm to children as pickable acts; no life model is ever
  treated as an object of desire in a scene (life drawing is a quiet, professional room; models are adults who are paid
  and agree, and nothing in the text sexualises them); children only in safe, supervised forms (a school, a parent who
  signs, a teacher present); nothing graphic (an injury stays plain and offstage); suicide never pickable and never a
  scene. **No real people, galleries, museums, prizes, publishers, schools, brands, countries or years by name**: "the
  national gallery in the capital", "the great summer show", "a big publisher", "the prize everyone has heard of".
- Role slots only from the spec ({boss} {colleague} {mentor} {rival} {friend} {partner} {elder} {place} ...): a dealer,
  publisher or head of department is {boss}; a fellow artist {colleague}; a teacher or an old artist {mentor}; the
  other artist up for the same wall or prize {rival}.
- **Worlds.** Every moment carries situation-level earth:, tribal: and magic: lines (and `scene tribal:` / `scene
  magic:`), in the forms below. An option whose act reads differently in a world adds its own tribal: or magic:
  wording. A world-only moment is marked `only: tribal` or `only: magic` and has that world's line alone.
  Supernatural acts are one choice among ordinary ones, never forced, always with a price, and never rest on the
  person's own gift: the magic comes from someone else (a hedge-witch's pigment, an enchanter's varnish) on a
  `closed: approval:` line with a backfire. Modern Earth has no magic.
- **Frequency.** Every moment, of every tier, carries a `times:` line in words: how often the people who can meet it
  meet it, how rare it is across all lives (from the catalogue shares), and a source in plain words or "(estimate)".
- **Unique names.** No moment name or option label may appear anywhere else: grep /mnt/project-files/chroma-library/
  earth.py and *.lib, and /home/claude/chroma_prototype/chroma-packs/*/*.lib before you settle a name.

### Forms in the other worlds (worlds.py)
| Title or perk | tribal | magic |
|---|---|---|
| open-mic poet | a speaker of verses at the band's fire | a reader at the poets' night in the tavern |
| life-drawing regular | one who draws on the rock with the others at the painting place | a sketcher at the academy's evening hall |
| art school student | apprentice to the painter of the great cave | a student at the academy of arts |
| street artist | painter of the shelter walls, the hides and the shields | painter of the city's walls and shop signs |
| illustrator for hire | marker of drums, bowls and shields for anyone who asks | an illuminator for hire: books, maps and broadsheets |
| painter or sculptor | the cave painter or the carver | a painter or sculptor of the guild |
| art teacher | the one who teaches the children the marks and the patterns | a drawing master |
| gallery owner | the trader in carvings at the great gatherings | a picture dealer with a hall on the square |
| master craftsperson | the master carver whose work is traded far | a master of the craft guild |
| renowned artist | the painter whose cave every band visits | court painter |
| celebrated author | the maker of the verses every band repeats | chronicler of the realm, whose books are copied |
| novelist (base) | a maker of long tellings | a writer of books |
| writing poems, drawing and painting, sculpting, illustration | verses, rock marks, carving, painted patterns | verse, drawing, sculpture, illumination |
| art school degree | the painter's leave to paint alone | the academy's seal |
| a publishing contract | a place for one's tellings at the gathering | a printer's contract |
| a maker's hallmark | the band's sign cut beside one's own | the guild's mark |
| a name in the art world / a dealer who sells your work | a name among the traders / a trader who carries your carvings | a name at court and in the salons / a dealer |
| a prize for writing / a mural the town loves | the elders' honour at the gathering / a shelter wall the band loves | a laurel from the academy / a wall the quarter loves |
| pupils who remember you / a circle of artists | children who keep your patterns / the ones who paint beside you | pupils / a circle of the studio |
| a body of work / works in collectors' hands / royalties | carvings stored in the cave / pieces in other bands' hands / a share of every trade | a body of work / pieces in noble houses / royalties from the printers |

## Calibration lessons (from the Stage pack's brief, kept)

1. Everyday door pairs carry `share:`, `share_group:`, `rate:` and `gap:`, the same on both halves. `share:` is the
   real share of all people who ever meet the moment. Door rates .02 to .03, gaps 2 to 8 years.
2. Holder pairs use `aims:` and never give a new title: careers and statuses rate .5; community titles .2; with `gap:`
   1-3. They may `grants:` a perk plainly earned and `drops:` the title held.
3. Every moment carries `times:`.
4. A life event's `per_year` is the yearly rate of acting on the chance, by stage (child juvenile young_adult adult
   mature elder), per holder: about .5 for a crossing a short status waits for, .02 to .3 for a regular chance, .005 to
   .02 for a rare one. Values are given below; keep them.
5. Every echo and read moment needs an engine condition (engine-conditions.py, written for the names below). Do not
   add an echo, inner or read moment that is not in this brief.
6. An option with `requires:` carries `lacking:`.
7. Every option except doing nothing carries `chance:`; the mean chance per means colour stays within 3 points in every
   stage. Mean chance about 68 to 72 for everyday moments and life events, 72 to 78 for echoes (parts at their real
   chances pull it down: balance them across colours inside the moment).
8. Long shots: every one-colour option at chance 1 to 5 that gives a title carries `grants_if_fails: a long shot that
   missed`.

## Balance layout

- **Everyday pairs: 10** (2 door pairs, 4 on the red road's rungs, 4 on the side roads and the taste rung). Their
  two-colour calls hold each of the ten colour pairs exactly once (listed per pair below), and each pair's halves use
  the cross cycle given (s1 three times, s2 three times, s3 twice, s4 twice). The two halves of a pair share stages,
  ages, holds:, tenure:, share, share_group, rate and gap.
- **Echoes: 4** (2 in art-doors.lib, 2 in art-longshots.lib), each even on its own: five one-colour options and one
  full cross cycle (given below).
- **Life events (Earth and every world): 22** = 11 steps (art-steps.lib) + 5 falls and wrongs (art-events.lib) + 6
  long shots (art-longshots.lib). Each has the five one-colour options plus one half of a D line: pairs D1a to D6b
  (all twelve halves) and triads D1a to D5b (all ten halves), so every pair appears twice and every triad twice. The
  read event is even on its own.
- **World-only events: 4** (art-worlds.lib): tribal triads D6a and D6b, magic pairs D1a and D1b; each world's own set
  is even.
- In all: 51 moments, about 510 options.

---

## Part 1: doors and echoes (file art-doors.lib), 6 moments

Pair A (no holds; stages child juvenile; age 10-18; share .4; share_group art_youth_doors; rate .03; gap 2-4; cycle s1).
Children hold no title: these doors grant the base skills the taste rung needs.
1. `the art room at lunchtime` (calls WU). The art teacher leaves the art room open at lunch: paper, paint, clay, the
   radio on. Options grant [drawing and painting] (several colours), [sculpting] (clay, one option), `aims: life-drawing
   regular` on one; others: stay out in the playground, help tidy and wash brushes, enter the school's poster
   competition. times: per child or teenager a year: about 1 in 5 schools keep an art room open at lunch or after
   school, and about 15 lives in 100 keep drawing or painting past school (catalogue share; estimate).
2. `a poem for the school magazine` (calls BRG). The English teacher wants poems for the school magazine. Options grant
   [writing poems] (several colours) or [writing stories]; `aims: open-mic poet` on one; others: write one for a
   friend's birthday instead, read it aloud in assembly, say poems are for other people. times: per child or teenager a
   year: about 1 in 4 are asked for a poem or a story for a school magazine or competition; about 3 lives in 100 keep
   writing poems past school (estimate).

Pair B (no holds; stages juvenile young_adult adult mature elder; age 16-90; share .06; share_group art_adult_doors;
rate .02; gap 3-8; cycle s2).
3. `the evening class at the college` (calls BR). The college's prospectus: life drawing, Tuesday evenings, ten weeks,
   all levels. Doors: `title: life-drawing regular` on three or four options of fitting colours; `grants: drawing and
   painting` on one; others: buy the materials and draw at home, ask for the cheaper rate, say no (no time).
   times: per adult a year: about 1 in 30 see an evening art class they could join; about 15 lives in 1,000 draw at a
   weekly class for a year or more (catalogue share; estimate).
4. `the poetry night at the back of the pub` (calls WUG). A chalkboard by the bar: open mic, poets welcome, first
   Thursday. Doors: `title: open-mic poet` on three or four options; `grants: writing poems` on one; others: go and
   listen only, help run the night, say no. times: per adult a year: about 1 in 30 come across a poetry or spoken-word
   night they could read at; about 1 life in 100 reads at one again and again (catalogue share; estimate).

Echoes (each even on its own: five one-colour options and one full cross cycle; once: yes):
5. `the sketchbook in the attic` (rate .05; cycle s3). Years later, clearing a cupboard or a parent's attic, the old
   sketchbook from school. Anchor and gate in engine-conditions.py. Options: `title: life-drawing regular` (two or three
   colours), `grants: drawing and painting`, `aims: painter or sculptor` on one; others: give it to a child, put it back.
   times: per adult who drew as a child, once: about 1 in 10 come back to drawing after twenty years or more (estimate).
6. `the poems you never showed anyone` (rate .05; cycle s4). After a loss, a retirement or a long illness, the notebook
   of poems. Options: `title: open-mic poet` (two or three colours), `grants: writing poems`, `aims: novelist` on one
   (a collection); others: burn them, read one at the funeral, give the notebook to someone. times: per adult who wrote
   poems, once: about 1 in 10 return to writing after a loss or in retirement (estimate).

## Part 2: the red road's rungs (file art-rungs.lib), 8 moments, holder pairs

Each pair: rate .5 for careers and the status, gap 1-3; stages young_adult adult mature elder; age 16-100; no share:
line (as stage-rungs.lib: the holds: gate does the drawing). No new title; aims: the next rung; grants: perks plainly
earned.
7. `the model does not turn up` (holds life-drawing regular; calls UG; cycle s3; rate .2): the class draws
   each other, or the room, or the tutor. Grants [drawing and painting], [a circle of artists]; aims: painter or
   sculptor, street artist.
8. `someone wants to buy the sketch off the easel` (holds life-drawing regular; calls WBR; cycle s3; rate .2; share
   .015). Grants [a circle of artists]; aims: painter or sculptor, illustrator for hire.
9. `the wall is painted over by the council` (holds street artist; calls RG; cycle s4). Grants [a mural
   the town loves]; aims: painter or sculptor; a wrong: paint it again without leave (closed: law, a fine).
10. `a shopkeeper wants the shutters painted` (holds street artist; calls WUB; cycle s4). Grants [a mural
   the town loves], [a name in the art world]; aims: renowned artist.
11. `the brief changes at midnight` (holds illustrator for hire; calls UB; cycle s1). Grants [illustration];
   aims: painter or sculptor.
12. `the client who will not pay` (holds illustrator for hire; calls WRG; cycle s1). Grants [royalties]
   (licence the work again), [a publishing contract] (pitch a picture book); a wrong: keep a client's files hostage.
13. `the studio rent goes up` (holds painter or sculptor; calls WR; cycle s2). Grants [studio of one's own]
   (buy a shed, requires savings), [a circle of artists] (share a studio); drops: painter or sculptor on one option (a
   steady job instead).
14. `a month when nothing works` (holds painter or sculptor; calls UBG; cycle s2). Grants [a body of work],
   [a name in the art world]; aims: renowned artist.

## Part 3: side roads and the taste rung (file art-roads.lib), 8 moments, holder pairs

Same fields as Part 2 (community titles rate .2).
15. `the poem that silenced the room` (holds open-mic poet; calls BG; cycle s1; rate .2). Grants [writing
   poems], [a circle of artists]; aims: novelist (a first collection).
16. `a heckler at the front table` (holds open-mic poet; calls WUR; cycle s1; rate .2). Grants [public
   speaking], [following online]; aims: novelist.
17. `the child who draws all through maths` (holds art teacher; calls WG; cycle s2). Grants [pupils who
   remember you]; aims: gallery owner (a show of the children's work in town).
18. `the art room budget is cut` (holds art teacher; calls UBR; cycle s2). Grants [a mural the town loves]
   (paint the school hall with the children), [organising people]; drops: art teacher on one option.
19. `an artist leaves for a bigger gallery` (holds gallery owner; calls WB; cycle s3). Grants [a name in
   the art world], [contact in the trade]; a wrong: hold back the artist's unsold work.
20. `a buyer wants a discount behind the artist's back` (holds gallery owner; calls URG; cycle s3).
   Grants [works in collectors' hands], [striking a deal].
21. `an apprentice asks to learn the craft` (holds master craftsperson | craft maker; calls UR; cycle s4).
   Grants [pupils who remember you], [a maker's hallmark] (one option, for the patient); aims: master craftsperson.
22. `a machine-made copy in the shop window` (holds master craftsperson | craft maker; calls WBG; cycle s4; share
   .005). Grants [a maker's hallmark], [selling]; aims: master craftsperson.

## Part 4: steps (file art-steps.lib), 11 life events

Each: five one-colour options at the same real chance for the step (doors with title:, the facet first where the rule
says), plus the D half given. Most combinations are honest ways of weighing the step, taking a smaller step, or turning
it down. `drivers:` as in WINDOWS_ART (helps.py).
23. `art school applications` (pairs D1a). holds drawing and painting | life-drawing regular; stages juvenile
   young_adult adult; age 16-35; per_year 0 .15 .08 .02 0 0; drivers prosper+.2 money+.2. Door: `title: art school
   student` at chance 45; requires savings or scholarship on one (lacking .5).
24. `the degree show` (pairs D1b). holds art school student; tenure 2-100; stages young_adult adult; age 19-45;
   per_year 0 0 .6 .6 0 0; drivers prosper+.3. Options: `title: illustrator for hire` (a commission from the show, 25),
   `title: art teacher` (teacher training, 55, requires graduate | without: approval | lacking .3), `grants: a dealer
   who sells your work` (20), `grants: a circle of artists`, `title: street artist` (a mural for the college, 30).
25. `a wall that needs a mural` (pairs D2a). holds life-drawing regular | art school student | art teacher; stages
   juvenile young_adult adult mature; age 16-80; per_year 0 .02 .1 .08 .04 .01; drivers community+.3 prosper+.1.
   Door: `title: street artist` at 35; `grants: a mural the town loves` (for the teacher who paints it with the class).
26. `the first commission` (pairs D2b). holds art school student | life-drawing regular | street artist; stages
   young_adult adult mature elder; age 18-90; per_year 0 0 .1 .08 .04 .02; drivers era+.2 prosper+.2. Door: `title:
   illustrator for hire` at 40.
27. `the first show` (pairs D3a). holds life-drawing regular | street artist | illustrator for hire | art school
   student; tenure 2-100; stages young_adult adult mature elder; age 19-95; per_year 0 0 .06 .06 .04 .02; drivers
   prosper+.3 fortune+.2. Door: `title: painter or sculptor` at 25; grants [a name in the art world], [a dealer who
   sells your work].
28. `the school needs an art teacher` (pairs D3b). holds teacher | painter or sculptor | illustrator for hire | street
   artist | art school degree; stages young_adult adult mature; age 22-65; per_year 0 0 .05 .04 .02 0; drivers era+.1.
   Door: `title: art teacher` at 50; requires professional registration | without: approval | lacking .3 on two.
29. `an empty shop on the corner` (pairs D4a). holds painter or sculptor | art teacher | shop owner | museum curator |
   illustrator for hire; tenure 3-100; stages adult mature elder; age 25-85; per_year 0 0 0 .03 .03 .01; drivers
   prosper+.3 money+.2. Door: `title: gallery owner` at 35, requires savings | without: means | lacking .5.
30. `the guild judges your masterpiece` (pairs D4b). holds craft maker | carpenter; tenure 4-100; stages adult mature
   elder; age 25-95; per_year 0 0 0 .05 .05 .03; drivers community+.2. Door: `title: master craftsperson` at 35 with
   `grants: a maker's hallmark`.
31. `a publisher reads the manuscript` (pairs D5a). holds novelist | open-mic poet | illustrator for hire; stages
   young_adult adult mature elder; age 18-95; per_year 0 0 .05 .05 .04 .03; drivers era+.2. Options: `grants: a
   publishing contract` at 12 (and `grants: book in print`); for the open-mic poet's collection `title: novelist` at
   12 (the base [novelist] is every writer of books); the picture book for the illustrator.
32. `a work in the national collection` (pairs D5b). holds painter or sculptor | street artist | illustrator for hire |
   master craftsperson; tenure 5-100; stages adult mature elder; age 25-100; per_year 0 0 0 .02 .03 .02; drivers
   era+.2 fortune+.3. Door: `title: renowned artist` at 8 (steps at real odds, not long shots: no perk on failure).
33. `a national prize for writing` (pairs D6a). holds novelist; tenure 3-100; stages adult mature elder; age 25-100;
   per_year 0 0 0 .02 .03 .02; drivers era+.2 fortune+.2. Door: `title: celebrated author` at 7 with `grants: a prize
   for writing`.

## Part 5: falls and wrongs, and the read event (file art-events.lib), 6 moments

34. `a dealer asks for a painting in a dead master's hand` (pairs D6b). holds painter or sculptor | illustrator for
   hire | gallery owner; stages young_adult adult mature elder; age 20-95; per_year 0 0 .01 .015 .01 .005. The wrong
   (forge and sign it) pays well: mark hid a wrong; closed: law: backfire, the forgery is found and the name is gone
   (takes: a name in the art world). Others refuse, report the dealer, paint it openly as a copy, use the money talk to
   get a show of their own.
35. `a friend's secret would make the book` (triads D1a). holds novelist | open-mic poet; stages young_adult adult
   mature elder; age 18-100; per_year 0 0 .02 .02 .02 .01. The wrong: put it in (mark broke your word; backfire, the
   friend reads it). Others ask first, change it beyond knowing, leave it out, write it as a poem only for the friend.
36. `the idea in someone else's sketchbook` (triads D1b). holds art school student | illustrator for hire | painter or
   sculptor | street artist; stages young_adult adult mature; age 17-80; per_year 0 0 .03 .02 .01 0. The wrong: take
   the idea (mark hid a wrong; backfire, the friend sees the work). Others ask to build on it together, credit the
   friend, push your own idea further.
37. `an advert wants your style` (triads D2a). holds street artist | illustrator for hire | painter or sculptor |
   renowned artist; stages young_adult adult mature elder; age 18-100; per_year 0 0 .03 .03 .02 .01. Selling out or not:
   take the money (grants royalties or savings), take it and give it to the community centre, refuse, negotiate the
   terms, make the advert into a work of its own.
38. `hands that will not hold the brush` (triads D2b). holds painter or sculptor | master craftsperson | illustrator for
   hire | craft maker; stages adult mature elder; age 40-100; per_year 0 0 0 .02 .04 .06. A plain fall (age, a
   tremor, arthritis, eyes): adapt (bigger brushes, a new material), teach (`grants: pupils who remember you`), stop
   (`drops:` the career on one or two options), get help from an assistant, take it as the end of one chapter.
39. `the reviews of the show are in` (read event; even on its own: five one-colour readings and one cross cycle s1,
   no chance: on readings). Comes to someone whose work was just shown (READ_ART). The readings are how the person takes
   the reviews, not acts.

## Part 6: long shots and their echoes (file art-longshots.lib), 8 moments

Each long shot: five one-colour options, each a long shot (chance 2 to 5) at a title the moment offers, every one with
`grants_if_fails: a long shot that missed`; plus the triad half given (honest ways to weigh it, a smaller step, or
walking away). Gates in engine-conditions.py (LIFE_ART_LONGSHOTS): a bold try at the next rung, or a skip of at most
one rung by someone with years on the rung below.
40. `the sketch that went round the world` (triads D3a). holds life-drawing regular | street artist | illustrator for
   hire; tenure 2-99; stages juvenile young_adult adult mature; age 16-80; per_year 0 .005 .01 .01 .005 0; drivers
   era+.3 fortune+.3. Titles: street artist or illustrator for hire (for the life-drawing regular), painter or sculptor
   (for the street artist or the illustrator).
41. `the open submission to the great summer show` (triads D3b). holds painter or sculptor | life-drawing regular;
   tenure 5-99; stages adult mature elder; age 25-100; per_year 0 0 0 .02 .02 .02; drivers fortune+.3. Titles:
   renowned artist (the painter), `renowned artist; painter or sculptor` (the life-drawing regular of five years).
42. `the manuscript in the pile on the floor` (triads D4a). holds open-mic poet | novelist; tenure 2-99; stages
   young_adult adult mature elder; age 18-100; per_year 0 0 .01 .01 .01 .01. Titles: novelist (the poet), celebrated
   author (the novelist of three years).
43. `the late starter at the easel` (triads D4b). holds life-drawing regular; tenure 2-99; stages mature elder; age
   58-100; per_year 0 0 0 0 .02 .03; drivers fortune+.2. Titles: painter or sculptor, art teacher (the college asks
   them to teach the class).
44. `the other side of the easel` (triads D5a). holds painter or sculptor | illustrator for hire | art teacher;
   tenure 3-99; stages adult mature elder; age 25-90; per_year 0 0 0 .01 .01 .005. Titles: gallery owner, art teacher
   (for the painter or the illustrator), illustrator for hire (for the art teacher).
45. `the judge stops at your table at the craft fair` (triads D5b). holds craft maker | master craftsperson;
   tenure 3-99; stages adult mature elder; age 25-100; per_year 0 0 0 .02 .02 .02; drivers community+.2. Titles:
   master craftsperson (the craft maker), renowned artist (the master craftsperson of five years).
46. `the same canvas, years later` (echo, even on its own, cycle s2; rate .1; once: yes). The second try: `title:
   {missed}` on the one-colour options at chance 4, with `grants_if_fails: a long shot that missed` only where the
   chance stays 1 to 5.
47. `the long shot becomes a class to teach` (echo, even on its own, cycle s3; rate .05; once: yes). Making peace with
   it: `grants: pupils who remember you`, `title: life-drawing regular` (an open rung), `grants: a circle of artists`.

## Part 7: world-only events (file art-worlds.lib), 4 moments

48. `the painted cave at the winter camp` (only: tribal; triads D6a). holds painter or sculptor | street artist |
   life-drawing regular | art school student; adult mature elder; per_year 0 0 0 .02 .02 .01. The band's great cave
   wall for the midwinter gathering; `title: renowned artist` (the cave painter whose wall every band visits) at 8 for
   painters, the rest honest ways to paint it, share it, refuse the elders' choice of subject.
49. `the carver's mask for the dead` (only: tribal; triads D6b). holds master craftsperson | craft maker | painter or
   sculptor; adult mature elder; per_year 0 0 0 .02 .02 .02. A mask for the dead chief's mourning; grants a maker's
   hallmark, pupils who remember you; `title: master craftsperson` at 35 for the craft maker of four years.
50. `the queen's portrait sitting` (only: magic; pairs D1a). holds painter or sculptor | illustrator for hire; tenure
   3-99; adult mature elder; per_year 0 0 0 .02 .02 .01. The court wants a portrait; `title: renowned artist` (court
   painter) at 8; one option buys an enchanter's varnish that makes the portrait smile (closed: approval: the Order's
   leave; backfire, the portrait shows the truth).
51. `the illuminated book for the cathedral` (only: magic; pairs D1b). holds illustrator for hire | art school student |
   life-drawing regular; adult mature elder; per_year 0 0 0 .02 .01 .01. A year's work on a great book; grants
   illustration, a body of work, royalties (from the printers); `title: illustrator for hire` (the illuminator) at 40 for
   the student and the sketcher.

## Checks (each file must pass all three)

- Build: `PYTHONDONTWRITEBYTECODE=1 python3 -B <scratch>/build.py /home/claude/chroma_prototype/chroma-packs/art/<yourfile>.lib --out <scratch>/out`
  (copy /mnt/project-files/chroma-library/build.py to your scratch folder first); it must end with "no layout problems".
- Chance and tags: `PYTHONDONTWRITEBYTECODE=1 python3 -B /home/claude/chroma_prototype/chroma-packs/tools/lib_stats.py /home/claude/chroma_prototype/chroma-packs/art/<yourfile>.lib`:
  the mean chance per means colour within 3 points overall and in every stage; tag counts close to even.
- Names: `cd /home/claude/chroma_prototype && PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-packs/tools/check_pack.py art`:
  no unknown names from your file (other files may still be missing while others write them).

## Files and rules

- Write only your own file in /home/claude/chroma_prototype/chroma-packs/art/ (named in your task). Write moment by
  moment (append), so partial work survives.
- Never write anywhere else in the repository or in /mnt/project-files; read only. Scratch goes in your own folder under
  /tmp/claude-0/-home-claude-chroma-prototype/e40218c8-fe2b-58e7-bec9-a2e19282a5e8/scratchpad/art/. No packages;
  standard library only. Run Python as `PYTHONDONTWRITEBYTECODE=1 python3 -B`. No git commands.
- No AI model names or identifiers in any file.
