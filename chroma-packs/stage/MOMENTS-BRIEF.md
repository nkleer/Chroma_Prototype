# Stage and Screen pack: brief for the moment writers (Pathways and packs thread, 2026-10-06)

Status: the third pathway pack, planned for Emren's single go-live with Science and Politics (packs thread, 01:32).
The catalogue, rules, earned odds, worlds and engine conditions are written; the moments are to be written to this
brief. Emren's ask (packs thread, 01:31): "You can also work on third content package, you can choose the concept name
subject and its content as you seem fit. Lead actor/actresss availability must be inside with all new content." So
every road the pack opens reaches a lead: amateur, youth and school, fringe and one-person shows, stage, screen, voice,
late life, and the tribal and magic worlds (each moment below names the lead route it serves). Emren (point 8,
2026-10-05 20:39): the game must let a character live big lives, never obliged to. Emren (21:37): modern Earth terms
first, but every moment must work in the other worlds, "even including supernatural sometimes". Emren (21:03) on odds:
"give more chance than real odds, but keep it consistent and achievable, if player and character create a good
strategy, and they are at right place at right time."

The pack's catalogue (titles and perks) is /mnt/project-files/chroma-packs/stage/catalogue.py, the rules roles.py, the
earned odds helps.py, the other worlds worlds.py, the engine's conditions for the echoes and the read event
engine-conditions.py; the shared reach perks are in /mnt/project-files/chroma-packs/core/reach.py. The plan for every
pack is /mnt/project-files/chroma-packs/PROPOSAL.md, section 2 (doors, life on the rung, crossings, falls, reach). What
the calibration of the first two packs taught is in /mnt/project-files/chroma-packs/calibration.md; its lessons are
below ("Calibration lessons").

## Read first

- /mnt/project-files/chroma-library/library-spec.md (all of it: Emren's rules, the format, the balance layout, tagging
  colors faithfully, story fields) and /mnt/project-files/chroma-library/writer-brief.md.
- The build.py header (/mnt/project-files/chroma-library/build.py, lines 1 to 45): the .lib syntax, holds:, title:,
  grants:, drops:, requires: with without:, chance:, self_control:, and the world fields earth:, tribal:, magic:, only:.
- /mnt/project-files/chroma-library/drafts/audit/CHANCE-BRIEF.md (every option except read lines carries chance:).
- The Politics pack's moments, the closest model, calibrated: /mnt/project-files/chroma-packs/politics/*.lib and its
  brief; the Science pack's seasons: /mnt/project-files/chroma-packs/science/science-seasons.lib.
- Worked examples, copy their shape exactly: everyday door pair with share, rate and gap: the first two moments of
  /mnt/project-files/chroma-packs/politics/politics-doors.lib; everyday pair of a title: the first two moments of
  /mnt/project-files/chroma-library/earth-titles-careers.lib; life event: "== polling day in the ward" in
  /mnt/project-files/chroma-packs/politics/politics-events.lib; echo: "== the fight that made you want to stand" in
  politics-doors.lib; read event: "== the count goes against you" in politics-events.lib; threshold season:
  /mnt/project-files/chroma-packs/politics/politics-seasons.lib; world-only event: politics-worlds.lib.
- The game's worlds: /mnt/project-files/chroma-game/prototype/story.py, SETTINGS and WORLD (read only), and this pack's
  worlds.py (the form of every title and perk in the tribal and magic worlds).

## Pack rules on top of the Library's

- Every name in title:, drops:, grants:, takes:, suspends:, requires:, holds: and aims: must be a title or perk in the
  pack's catalogue, core/reach.py, or the base catalogue /mnt/project-files/chroma-library/earth_perks_titles.py.
  Exact names. holds: may name several titles or perks with "|" (any of them).
- A door is an option that takes a title by the act (`title: amateur actor`). Its means color must fit one of that
  title's profiles in the pack catalogue. Every pack title with colors has three profiles that together cover all five
  colors, so a door can be honest in every color. Door options also carry `aims: <title>` (one or two per means color
  in the pack), and holder pairs use `aims:` instead of `title:` (calibration lessons).
- **The lead.** [lead actor or actress] is a facet on [professional actor] or [voice actor]. On an option for people who
  already hold one of those, write `title: lead actor or actress`. For anyone else (an amateur, an extra, an
  understudy whose career title may have lapsed, a tribal player) write `title: lead actor or actress; professional
  actor`, the lead first: the earned odds read the first title of the field (helps.py), and the engine holds a facet
  given before its title for a few weeks and grants it with the title. The amateur, child and one-person-show lead is
  the standing perk: `grants: a lead role to remember`. When the lead and the career come together, the lead's season
  opens (a new season replaces one still running).
- **Parts are won in the option's chance**: the chance on an option that takes a part or a place is the real chance for
  an ordinary person who tries: a drama school place 10 to 15 (about 1,550 places for about 12,000 applicants a year);
  an open call for paid work 5 to 10; signing with an agent at the showcase 40 to 50; cast as an understudy 25 to 35;
  the understudy kept on as the lead 15 to 25; the part of a lifetime 4 to 8; a screen test that becomes the lead 8 to
  12; the company actor stepping up when the lead leaves 20 to 30; a fringe show that transfers 8 to 12; signing with
  an agent after a fringe run 10 to 15; the lead voice in a series 10 to 15; a director who calls again 25 to 35; a
  lead at the local players 25 to 35; the lead in a youth theatre show 20 to 30; a child's part in a professional
  show 10 to 15 for a lead, 30 to 40 for the ensemble; a first voice job 20 to 30; a stage management post 45 to 55;
  directing the local players 55 to 65, a paid production 25 to 35; a script competition 5 to 10; an artistic
  directorship 10 to 20. The engine's earned-odds lifts (helps.py, half on the lead) raise these for the prepared and
  the timely; never write them higher. Balance them across colors inside each moment, so no color wins parts more
  easily.
- A door closed by money, law or approval stays pickable: `requires: casting directory listing | without: approval |
  lacking: .3` (seen only at an open call), `requires: savings | without: means | lacking: .5` (the fees borrowed),
  never removed.
- Keep acting real and unglamorous where it is: most of it is auditions, self-tapes, rejection, day jobs, rehearsals,
  short runs and touring digs; 71 in 100 UK actors spend 28 weeks or more of a year outside the industry, and 48 in 100
  earn under 6,000 pounds a year from performing. A flop is common and survivable; a lead is a run, not a finish line.
- Wrongs are pickable with plain labels and no preaching: a whisper about a rival, a lie on the CV ("can ride a
  horse"), a friend's part taken behind their back, an edited self-tape, a contract walked out on, a drink before the
  show, a credit claimed for someone else's idea. Mark them (hid a wrong, broke your word, made an enemy) and give a
  closed: line with a real backfire (the company finds out, the agent drops you, the run ends early). Drink, drugs,
  rivalry and burnout are possible, never forced: one option among others, never the only one, never the moment's
  premise for someone who did not choose it. Integrity belongs to every color, and so does vanity.
- Every color gets its strong, honest acts as well as its risky ones, and its own road to the lead: White's company
  actor and understudy (word-perfect, there every night, ready when the lead falls ill); Blue's craft actor (training,
  the text, the voice); Black's networker (the agent, the producer, the part taken from a rival); Red's raw talent (the
  open call, the fringe, the one-person show); Green's rooted player (the regional company, the local players, the folk
  play, the late bloomer who leads at seventy).
- Content limits (Emren's rules, never broken): no sexual violence and no harm to children as pickable acts (at most an
  indirect mention, as someone's past); **no casting-couch abuse as an option or a scene**, not even offstage as a
  choice; **child actors only in real, supervised, safe forms**: a parent or carer who agrees, a licence, a chaperone,
  school hours kept, rest days, never alone with an adult in the story; nothing graphic (a stage fight is choreographed,
  an accident stays plain and offstage). **No real people, productions, theatres, studios, films, awards, agencies or
  unions by name**: "the actors' union", "the national theatre awards", "a big agency", "a famous old play", "the
  playhouse in the capital", "the largest fringe festival". Plain labels, no preaching.
- Role slots only from the spec ({boss} {colleague} {mentor} {rival} {friend} {partner} {elder} {place} ...). The
  director, producer or chair of the society is {boss}; a fellow actor {colleague}; the other actor up for the part
  {rival}; an agent, a voice teacher or an old actor {mentor}; a child's parent is named in words.
- Pair halves: an everyday pair is two consecutive moments with the same stages, age window, holds:, share, rate and
  gap, and calls that split the five colors 2 and 3. Life events listed together use the two halves of one combination
  line; each half is even on its own, so a half may carry its own stages.
- Worlds (Emren, 21:37). Every moment carries a situation-level earth: line and also tribal: and magic: lines, in the
  forms worlds.py gives (the fire, the tellings at the turning seasons, the great mask of the summer gathering, the
  hidden voices behind the hide screen, the shadow wall; the playhouse under licence, the players' guild and its
  school, the travelling wagons, the illusionists' glamours, the mirror-plays in scrying glasses, the speaking-stones).
  An option whose act reads differently in a world adds its own tribal: or magic: wording. A moment that belongs to
  one world only is marked `only: magic` or `only: tribal` and has that world's line alone. Supernatural acts are one
  choice among ordinary ones, never forced, always with a price; round 5 (2026-10-07): no act rests on the person's own
  awakened gift (held for a later version), so the magic comes from someone else (a medium, a hedge-witch, an
  illusionist) on a `closed: approval:` line with a backfire. Modern Earth has no magic.
- Frequency (game thread: the Book of Moments stars rare moments). Every moment, of every tier (everyday, life event,
  echo, read and season), carries a `times:` line in words, copied from the "times N:" line under it below: how often
  the people who can meet it meet it, how rare it is across all lives where that helps (from the catalogue shares),
  and a source or "(estimate)". Sources are named in plain words ("the UK actors' union, 2024", "US labour
  statistics, 2023"), never by a union's or a company's name. Adjust the words if the moment changes, never the figures
  without a source.

## Calibration lessons (from Science and Politics, ../calibration.md and the engine since)

1. Everyday doors carry `share:`, `rate:` and `gap:`, the same on both halves of a pair. `share:` is the real share of
   all people who ever meet the moment. On a holds: moment the engine now draws among holders at share divided by the
   holders' share (engine 01:45, after the packs' issue 4), so write the share of all lives, not of holders. Door
   rates sit at .02 to .03 with gaps of 1 to 8 years, as listed below.
2. Holder pairs (parts 2 and 3) use `aims:` and never give a new title: careers and statuses rate .5; community titles
   lower (listed per pair), with `gap:`. They may `grants:` a perk plainly earned and `drops:` the title held.
3. Every moment carries `times:`, of every tier.
4. A life event's `per_year` is the yearly rate of acting on the chance, by stage (child juvenile young_adult adult
   mature elder), per holder. Realized success at crossings runs well above the written chance (calibration issue 2),
   so per_year sits below the times lines: about .5 to .8 for a crossing that a short status waits for, .02 to .3 for
   a regular chance, .005 to .02 for a rare one.
5. An echo at rate .3 brings back about 40 in 100 of its anchors; its rate scales that, and `once: yes` is honoured.
   This pack's echoes run at .01, .02, .05 and .1 (moments 7 to 10).
6. Every echo, inner and read moment needs an engine condition: engine-conditions.py holds them (ECHO_STAGE for 7 to
   10, READ_STAGE for 65). Season moments need none. A writer who adds an echo, an inner or a read moment asks for its
   condition first.
7. An option with `requires:` carries `lacking:` (the share of the written chance someone without it still gets: about
   .1 to .3 for an unknown face, .5 for money that can be borrowed).
8. Every option except doing nothing carries `chance:`; the mean chance per means color stays within 3 points in every
   stage.

## Part 1: doors and hooks (file stage-doors.lib)

Everyday pair A (no holds; stages child juvenile; age 8-17; share .2; rate .02; gap 2-4; cycle s1):
1. `a flyer for the youth theatre` (calls WG). A flyer in the school bag: Saturday mornings, games, a summer show, the
   first term free. Doors: `title: youth theatre member` on three or four options of fitting colors (its profiles
   cover every color), `aims: youth theatre member` on one; others: ask for a free place (the fees), stay with
   football, go only if a friend goes. A parent or carer signs the form in every option that joins.
   earth: a flyer in the school bag for the youth theatre on Saturday mornings.
   tribal: the old teller calls the children to the fire to learn the small spirits' parts for midwinter.
   magic: the players' guild's children's company calls for new children at the spring fair, a parent's mark on the roll.
   times 1: per child or teenager a year: about 1 in 5 children see an invitation to a youth theatre or a stage school class; NAYT counted over 100,000 young people in 414 youth theatres in England in 2024, and about 8 lives in 100 belong to one at some point (catalogue share; estimate)
   lead: youth and school, the first step; the youth theatre's summer show casts its lead (54).
2. `auditions for the school production` (calls UBR). A notice on the hall door: auditions for the spring show on
   Thursday after school. Options: audition for the lead (`grants: a lead role to remember` at chance 20 to 25, on
   options in two or three colors), audition for any part (`grants: acting`), paint the set and run the lights
   (`grants: stagecraft`), `title: youth theatre member` (the drama teacher runs the youth theatre too), stay out of it.
   earth: the auditions notice for the school's spring show on the hall door.
   tribal: the elders choose which children will play the animals in the great telling at midsummer.
   magic: the schoolmaster wants players for the feast-day masque, and the best part is the fairy queen.
   times 2: per child or teenager a year: about 1 in 5 meet auditions for a school production they could try for; most secondary schools put on a show a year, with one or two leads (estimate)
   lead: youth and school, the school lead ([a lead role to remember]).
Everyday pair B (no holds; stages juvenile young_adult adult mature elder; age 16-90; share .08; rate .02; gap 3-8;
cycle s2):
3. `the local players need a cast` (calls BR). The amateur society's notice: open auditions for the autumn play, no
   experience needed. Doors: `title: amateur actor` on several options (its profiles cover every color),
   `aims: amateur actor` on one; others: offer to build the set (`grants: stagecraft`), sell the tickets, say no.
   earth: a notice in the library window: the local players hold open auditions for the autumn play.
   tribal: the band's tellers want more players for the midwinter telling.
   magic: the guild's mystery players need new players for the feast-day pageant.
   times 3: per teenager or adult a year: about 1 in 25 see a call from the local players they could answer; the UK amateur theatre association's survey counted 437,800 people taking part (2002), and about 4 lives in 100 act with amateurs at some point (catalogue share; estimate)
   lead: amateur, the first step to 'casting night at the local players' (53).
4. `extras wanted for a film in town` (calls WUG). A film is shooting in the high street and the background agency
   wants locals: a day's pay, a five o'clock call. Doors: `title: background artist` on several options (its profiles
   cover every color), `grants: casting directory listing` (sign with the agency) on one; others: watch from the
   pavement, say no.
   earth: a film is shooting in the high street, and the background agency wants locals for a day.
   tribal: a neighbouring band's great telling needs many bodies for the herd, the war band and the dead.
   magic: the illusionists' procession needs a crowd of townsfolk for its opening night, paid by the night.
   times 4: per teenager or adult a year: about 1 in 25 hear of a call for extras they could answer, more in towns where films are made; the largest US background agency has about 200,000 people registered, and about 8 lives in 1,000 work as an extra at some point (catalogue share; estimate)
   lead: screen, the extra who is given a line ('you, say this line' 39) and 'a screen test' (49).
Everyday pair C (holds: youth theatre member | amateur actor | a lead role to remember | acting; stages juvenile
young_adult adult; age 16-40; share .03; rate .03; gap 1-3; cycle s3):
5. `drama school auditions` (calls WB). The audition season: forms, a fee for each school, two speeches and a song.
   Doors: `title: drama school student` on several options at chance 10 to 15; `requires: savings | without: means |
   lacking: .5` on the option that applies to every school; `aims: drama school student` on one (a foundation year
   first); `grants: auditioning` on one; others: not this year (mark turned down a chance).
   earth: the drama schools' audition season: forms, fees, two speeches and a song.
   tribal: an old teller of another band will take one apprentice this winter, and asks to see what the young ones can do.
   magic: the players' guild school opens its doors for the trials at the spring fair.
   times 5: per young person who acts a year: about 1 in 7 think of applying; about 12,000 apply for about 1,550 places a year at 22 accredited UK drama schools, about 1 in 8 gets one, and about 3 lives in 1,000 train at drama school (catalogue share)
   lead: the craft road (U): drama school, then 'the showcase for agents' (45).
6. `an open audition in the city` (calls URG). An open call for a new production: no agent needed, a queue round the
   block by seven. Doors: `title: professional actor` on several options at chance 5 to 10 (`aims: professional actor`
   on one); `grants: auditioning`; `grants: casting directory listing` (the casting office keeps your details); others:
   leave the queue, go back next year.
   earth: an open call for a new show in the city: no agent needed, and the queue is round the block by seven.
   tribal: the keeper of the gathering's tellings will hear any player before the summer telling.
   magic: a travelling company sets up its wagons in the square and will hear anyone who wants to join.
   times 6: per young person who acts a year: about 1 in 10 go to an open call for paid work; most open calls cast a handful from hundreds (estimate)
   lead: raw talent (R), professional without training; then the stage road to the lead.
Echoes (stages young_adult adult mature elder unless named; five one-color options plus one full cross cycle;
`once: yes`; conditions in engine-conditions.py, ECHO_STAGE):
7. `the part you never got to play` (cycle s4; rate .01; after: 'the school play' as a child under 13; now 18 or more,
   neither acting with the local players nor for a living; delay 6-40). Doors: `title: amateur actor` (two options),
   `title: background artist`, `aims: drama school student` (for a young adult), `grants: acting`, or letting it rest.
   earth: a notice for the local players' auditions, in the same hall where the school play was.
   tribal: the children rehearse the small spirits for midwinter, and you remember the part you wanted.
   magic: the guild's pageant wagons roll past, and you remember the masque you were too shy to try for.
   times 7: per person who met the school play as a child: about 1 in 50 come back to the stage as adults, years later (estimate)
   lead: amateur and late life: the local players, then 'casting night at the local players' (53).
8. `never too late for the stage` (cycle s1; rate .02; after: 'the first months of retirement'; retired, not already an
   amateur actor, health enough; delay 0-3; stages mature elder). Doors: `title: amateur actor` (two options),
   `title: background artist` (the agencies want older faces), `grants: telling a story aloud` (reading stories to
   children at the library), `aims: amateur actor`, or letting it rest.
   earth: a notice for the local players, and a whole week free for rehearsals at last.
   tribal: too old for the hunt, you are asked to tell the old stories at the fire.
   magic: the guild's mystery players want grey heads for the elders in the pageant.
   times 8: per new retiree: about 1 in 40 take up amateur theatre or extra work in the first years of retirement; amateur societies draw members of every age (estimate)
   lead: late life (G): the lead at seventy through 'casting night at the local players' (53), and 'the part of a lifetime is cast' (48) for elders.
9. `the show you wrote to star in` (cycle s2; rate .05; after: 'inspiration strikes' or 'wanting to be noticed' in
   someone with [acting]; 17 or more; no lead and no fringe slot held; delay 0-2). Doors: `grants: a fringe slot` (book
   the venue) on two or three options, one with `requires: savings | without: means | lacking: .5`;
   `grants: a company of your own`; `grants: writing scripts`; `grants: improvisation`; or letting it rest.
   earth: an idea for a one-person show, and the fringe's registration closes in a month.
   tribal: a telling of your own, and the outer fires at the gathering where anyone may play.
   magic: a play of your own, and a pitch at the fair's booths.
   times 9: per person who can act and meets an idea that will not let go, or the wish to be seen: about 1 in 15 write and book a show of their own; the largest fringe festival had over 3,300 shows in 2024, most of them from small companies (estimate)
   lead: fringe and one-person shows (R): whoever wrote it plays the lead; 'opening night at the fringe' (51).
10. `the part that came with the letter` (cycle s3; rate .1; after: 'an unexpected chance: a grant, a role, a stage' in
   someone with [acting]; 17 or more, not yet a professional; delay 0-1; stages young_adult adult mature). Doors:
   `title: professional actor` on two or three options at chance 50 to 60 (the part was offered: say yes);
   `title: lead actor or actress; professional actor` on one at chance 10 to 15 (the letter offers the lead of a small
   touring show); `grants: casting directory listing`; turn it down (mark turned down a chance).
   earth: a letter from a small touring company: someone saw you, and there is a part.
   tribal: a band upriver sends word: their teller has heard of you, and wants you for the winter.
   magic: a sealed letter from a travelling company's master: a part, if you can join the wagons by spring.
   times 10: per person who can act and met an unexpected chance of a role: about 1 in 8 are offered paid work from it (estimate)
   lead: stage, the lucky letter; the lead of a small touring company.

## Part 2: life on the main rungs (file stage-rungs.lib)

One everyday pair per title, holds: that title, stages from the title's ages, rate as listed. First moment from the
title's turning point in the catalogue, second another ordinary moment of the role. Options may carry `drops:`
(leaving the role), `grants:` (a perk plainly earned, such as `grants: learning lines`), `takes:` and `aims:` (a step
the person now wants); never `title:`. The world lines of a pair give both moments, the first before the slash and the
second after it; the times lines come one per moment. Part 3 follows the same layout.
11-12. professional actor (s4; calls UR / WBG; young_adult adult mature elder; age 16-100; rate .5):
   `eight months on tour` (the turning point: the agent rings with a good part in a tour of eight months, and the day
   job will not hold the place; take it, turn it down for a partner or children, ask for six months, take it and keep a
   weekend job; `grants: a company that feels like family` at a low chance; `aims: lead actor or actress`);
   `a self-tape due by nine tomorrow` (two scenes, a reader, a phone on a pile of books; do it straight, do ten takes,
   get a friend to read, skip it; `grants: screen acting`, `grants: auditioning`).
   earth: the agent on the phone about a national tour / a spare room turned into a studio with a bedsheet.
   tribal: a band three valleys away wants you for the whole winter / the elders want to see your telling of the bear before the gathering.
   magic: a travelling company's master offers a place on the wagons for the whole season / the company master wants a glamour-sketch of your best scene by the morning bell.
   times 11: per professional actor a year: about 1 in 4 are offered a long tour that clashes with home or a day job; 71 in 100 UK actors spend 28 weeks or more of a year outside the industry (the UK actors' union's survey), and about 4 lives in 1,000 act for a living at some point (catalogue share; estimate)
   times 12: per professional actor: most months in a working year; most screen castings now begin with a recorded audition (estimate)
   lead: the stage and screen roads: the actor who aims at the lead.
13-14. lead actor or actress (s1; calls BG / WUR; young_adult adult mature elder; age 16-100; rate .5):
   `the producers want a star for the transfer` (the turning point: the show moves to a bigger theatre and the producers
   want a famous name in your part; fight for it, step aside with grace (`drops: lead actor or actress`), call the
   agent, let the company speak for you; `grants: a producer who backs you` at a low chance);
   `a cast member in trouble on the night` (a {colleague} is unwell, frightened or has had a drink before the show;
   cover for them on stage, tell the stage manager, carry the scene, talk them down in the dressing room;
   `grants: a company that feels like family`).
   earth: a meeting with the producers about the transfer / the dressing room at the half.
   tribal: the chief of another band wants his own son behind the great mask / a young player shakes behind the hide screen before the telling.
   magic: a noble patron wants a famous player in your part for the court season / a fellow player has been at the wine before the masque.
   times 13: per lead a year: about 1 in 10 meet a move or a recast that puts their part in doubt; about 1 life in 1,000 plays a lead in a paid production (catalogue share; estimate)
   times 14: per lead: a few times in a run, a member of the company is unwell or not fit on the night (estimate)
   lead: the lead held; how it is kept or given up.
15-16. understudy (s2; calls WR / UBG; young_adult adult mature; age 16-100; rate .5):
   `the understudy rehearsal nobody watches` (Thursday afternoon with the deputy stage manager and an empty stalls:
   work it like a first night, mark it through, make the part your own, ask the director to come;
   `grants: learning lines`; `aims: lead actor or actress`);
   `the lead plays through a fever` (the lead goes on ill, and you are ready in the wings: urge them to rest, stay
   quiet, tell the stage manager, hope; `grants: a director who keeps casting you` at a low chance).
   earth: an understudy call in an empty theatre / the wings during the first act.
   tribal: you practise the great mask's telling alone by the river / the wearer of the great mask is burning with fever at the gathering.
   magic: a rehearsal by lamplight in an empty playhouse / the leading player coughs through the first act of the court masque.
   times 15: per understudy: most weeks of a run; big shows hold understudy rehearsals weekly (estimate)
   times 16: per understudy: once or twice a run; about 1 professional actor in 3 understudies at some point (catalogue share; estimate)
   lead: the company actor's road (W): ready when the lead falls ill; 'the understudy goes on' (47).
17-18. drama school student (s3; calls UG / WBR; juvenile young_adult adult; age 16-40; rate .5):
   `the voice teacher and the accent from home` (the turning point: the accent from home has to go, and it is the
   voice of your family; lose it, keep it, learn both (`grants: accents and voices`), argue);
   `the money runs out in the second year` (fees, rent and a bar job at night: take more shifts, ask family, apply to
   the hardship fund (`grants: scholarship`), leave (`drops: drama school student`)).
   earth: a voice class in a room with a piano / a letter from the bank in the second year.
   tribal: the old teller says you speak like your mother's band, not like a teller / the winter is long and the old teller's family has little meat to share.
   magic: the guild school's master of voice corrects your street speech / the bursary runs dry and the guild wants its fee.
   times 17: per drama school student: once or twice a course; voice work is in every accredited course (estimate)
   times 18: per drama school student: about 1 in 4 run short in the course; many accredited courses charge full fees and leave living costs to the student (estimate)
   lead: the craft road (U): training for the lead.
19-20. director (s4; calls WU / BRG; young_adult adult mature elder; age 20-100; rate .5):
   `the lead does not believe in the idea` (the turning point: three weeks in, the lead says so in front of the
   company; hold the line, rethink, talk alone, recast (closed: approval; backfire: the producer backs the actor);
   `grants: directing actors`);
   `the budget is cut by a third` (cut the set, cut a character, fight the producer, put in your own fee).
   earth: a rehearsal room above a pub / an email from the producer.
   tribal: the wearer of the great mask will not play the ancestor as you shape him / the families give fewer hides for the telling this year.
   magic: the leading player refuses your staging before the whole company / the patron halves his purse for the season.
   times 19: per director a year: about 1 production in 5 has an open quarrel over the idea of the play (estimate)
   times 20: per director a year: about 1 in 5 see a budget cut after rehearsals begin (estimate)
   lead: the director who casts leads; 'the director calls again' (56) for the actors they trust.
21-22. playwright or screenwriter (s1; calls UB / WRG; young_adult adult mature elder; age 18-100; rate .5):
   `the producers want a different ending` (the turning point: change it, keep it, find a third ending, take the
   script elsewhere);
   `the blank page at three in the morning` (a draft due Friday and nothing on the page: write anything, walk, use a
   friend's story without asking (mark hid a wrong; closed: approval; backfire: the friend sees the play), ask for a
   week; `grants: writing scripts`).
   earth: notes on the script from the producers / a laptop at the kitchen table.
   tribal: the elders want the telling to end with the chief's victory / the gathering is a moon away and the new telling is not made.
   magic: the patron wants the hero to live / the play is promised to the playhouse by the new moon.
   times 21: per playwright or screenwriter a year: about 1 script in 3 that is bought is asked for a changed ending (estimate); about 8 lives in 10,000 are paid for a produced script (catalogue share; estimate)
   times 22: per playwright or screenwriter: most months with a deadline (estimate)
   lead: the writer who writes the lead, sometimes for themselves.
23-24. amateur actor (s2; calls RG / WUB; juvenile young_adult adult mature elder; age 14-100; rate .02; gap 3-6):
   `a newcomer gets your part` (the turning point: congratulate them, sulk, help them learn it, leave the society
   (`drops: amateur actor`); `grants: a company that feels like family` on helping);
   `show week in the village hall` (the get-in, a dress rehearsal that runs till midnight, a flat that falls: hold it
   up, laugh, take charge (`grants: stagecraft`), go home).
   earth: the cast list on the society noticeboard / the village hall in show week.
   tribal: the elders give your part in the telling to a girl from another hearth / the night of the midwinter telling, the fire too high and the screens catching.
   magic: the pageant master gives your part to a newcomer / the pageant wagon's axle breaks on the feast morning.
   times 23: per amateur actor: about once in three years a wanted part goes to someone else; about 4 lives in 100 act with amateurs (catalogue share; estimate)
   times 24: per amateur actor: once or twice a year, in each show week (estimate)
   lead: amateur (G R): the lead won and lost in the society.
25-26. youth theatre member (s3; calls WG / UBR; child juvenile; age 6-21; rate .1; gap 2-4):
   `the new child gets the lead` (the turning point: the old hands are angry on your behalf; be glad for them, say
   nothing, tell the leader it is unfair, help the new child learn the lines; `grants: a company that feels like
   family`);
   `first night nerves in the wings` (a parent in the third row, a dry mouth: breathe, go on, hold a friend's hand,
   ask the leader to stand in the wings; `grants: acting`).
   earth: the cast list pinned up on a Saturday morning / the wings of the school hall on the first night.
   tribal: the old teller gives the hare's part to a child from another hearth / the first telling by the fire with the whole band watching.
   magic: the guild's children's master gives the fairy queen to a newcomer / the children's company's first night in the guild hall.
   times 25: per youth theatre member: about once a year, at the summer show's casting (estimate)
   times 26: per youth theatre member: once or twice a year, at each show (estimate)
   lead: youth and school: the child's lead, lost and won; 'the summer show casts its lead' (54).

## Part 3: side roads and community rungs (file stage-roads.lib)

As part 2, one everyday pair per title, holds: that title, rate as listed; `aims:`, never `title:`.
27-28. stage manager (s4; calls BR / WUG; young_adult adult mature elder; age 17-85; rate .5):
   `the lead is not in at the half` (the turning point: the understudy has never had a full rehearsal; send them on,
   hold the curtain, phone round, read the part from the book yourself; `grants: calling the show`);
   `the fit-up runs through the night` (the set does not fit the touring venue: cut it, rebuild it, cancel, call the
   crew in; `grants: stagecraft`).
   earth: the stage door at the half / a touring set in a theatre too small for it.
   tribal: the wearer of the great mask has not come to the fire / the screens will not stand on the new ground of the gathering.
   magic: the leading player is not in the playhouse at the bell / the wagon's stage will not fit the inn yard.
   times 27: per stage manager a year: about 1 in 5 face a missing actor at the half (estimate); about 1 life in 1,000 works as a stage manager (catalogue share; US stage managers worked about 1,066 weeks in an average week in 2018-19, the US stage union's report)
   times 28: per stage manager on tour: most weeks of a tour (estimate)
   lead: the stage manager who sends on the understudy (47).
29-30. casting director (s1; calls WB / URG; young_adult adult mature elder; age 20-90; rate .5):
   `a name or the best audition` (the turning point: the producers want a famous name, and the best audition came from
   an unknown; fight for the unknown, give them the name, offer a smaller part, ask for one more recall;
   `grants: a casting eye`);
   `the actor who cried in the waiting room` (kindness or the schedule: take five minutes, move them later, see them
   now, send them home).
   earth: the casting office after the recalls / a waiting room full of hopefuls.
   tribal: the chief wants his nephew in the telling, and the best player is a hunter's daughter / a young one weeps before showing the elders the bear.
   magic: the patron wants a court favourite, and the best trial came from a street player / a nervous player sobs outside the trial room.
   times 29: per casting director a year: several times a year; about 1 life in 5,000 casts for a living (catalogue share; the Casting Society has nearly 1,200 members; estimate)
   times 30: per casting director: most weeks of auditions (estimate)
   lead: the casting director who gives the unknown the lead.
31-32. talent agent (s2; calls UR / WBG; young_adult adult mature elder; age 20-90; rate .5):
   `two clients, one part` (the turning point: the agency's best-paid client wants a part a young client was about to
   get; put the young client up, put the star up, put both up, tell the truth to both);
   `the client who has not worked in a year` (keep them, drop them, push harder, tell them straight;
   `grants: contact in the trade`).
   earth: the agency's office on a Monday / a client's name with no bookings beside it.
   tribal: two tellers you speak for both want to play the great mask / a teller who has had no call from any band all winter.
   magic: two of your players want the same part at the court playhouse / a player of yours has had no booking since the last fair.
   times 31: per talent agent a year: several times; about 1 life in 2,500 works as an agent for performers (catalogue share; US labour statistics: 12,870 agents and business managers of artists, performers and athletes, 2023; estimate)
   times 32: per talent agent: every few months; most actors on most lists work only a few weeks a year (estimate)
   lead: the networker's road (B): the agent who wins clients their leads.
33-34. drama teacher (s3; calls BG / WUR; young_adult adult mature elder; age 20-85; rate .5):
   `drama cut from the timetable` (the turning point: fight it, run it after school for nothing, move to a stage
   school, accept it);
   `the shy child who wants a line` (give the line, wait for the next show, a group part, a word with the parents;
   `grants: telling a story aloud`).
   earth: a meeting with the head about next year's timetable / a quiet child at the back of the drama studio.
   tribal: the elders say the children are needed at the fish weirs, not the tellings / a small boy who never speaks wants the hare's part.
   magic: the academy's council would turn the players' hours into reckoning hours / a shy pupil asks for a single line in the masque.
   times 33: per drama teacher a year: about 1 in 10 see drama hours cut; English secondary schools had 8,963 drama teachers in 2019 against 11,100 in 2010 (Cultural Learning Alliance)
   times 34: per drama teacher: several times a year, at each casting (estimate)
   lead: youth and school: the teacher who gives a child the lead; drama school for the best.
35-36. voice actor (s4; calls WR / UBG; young_adult adult mature elder; age 16-100; rate .5):
   `a year as the villain` (the turning point: a games studio offers a year of screaming villain work, and the voice may
   not survive it; take it, take it with a coach, turn it down, negotiate shorter sessions);
   `the voice is going` (a cold before a session, or the years: rest, push through, have the session moved, see a
   specialist; `grants: accents and voices`).
   earth: a booking from a games studio / a croak on the morning of a session.
   tribal: the band wants the voice of the cave bear every night of the long winter / your voice cracks before the spirits must speak.
   magic: a puppet theatre wants its demon's roar for a full season / your voice falters before the speaking-stone session.
   times 35: per voice actor a year: about 1 in 10 are offered long, straining work (estimate); about 1 life in 2,000 voices for a living (catalogue share; estimate)
   times 36: per voice actor: a few times a year (estimate)
   lead: voice: the voice that leads a series; 'the lead voice in a series' (52).
37-38. producer (s1; calls UG / WBR; young_adult adult mature elder; age 20-100; rate .5):
   `closing on Saturday` (the turning point: the show loses money every night, and closing means two hundred people out
   of work; close it, put in more money, cut costs, find a new backer (`grants: patron` at a low chance));
   `an investor wants a part for a nephew` (refuse, give a small part, give the part, find the nephew something
   backstage; mark gave in to pressure on giving it).
   earth: the box office figures on a Monday / an investor's lunch.
   tribal: the families who gave hides for the telling want them back / a family that gave the feast wants its son in the telling.
   magic: the play-merchant's ledger is red / a patron wants a part for a favoured boy of his house.
   times 37: per producer a year: about 1 in 5 face closing a show early; most commercial shows do not make their money back (estimate)
   times 38: per producer a year: about 1 in 10 (estimate)
   lead: the producer who backs a lead ([a producer who backs you]).
39-40. background artist (s2; calls WU / BRG; juvenile young_adult adult mature elder; age 16-95; rate .1; gap 2-5):
   `you, say this line` (the turning point: the director points at you and gives you a line; say it as written, make it
   your own, freeze, ask the assistant director what to do; `grants: screen acting`, `grants: casting directory
   listing`; `aims: professional actor`);
   `fourteen hours in a field for one shot` (rain, waiting, cold tea: stay, complain, help an old extra, leave early;
   `grants: reliable record` at a low chance).
   earth: a film set in the high street / a field and a catering van.
   tribal: the shaper of the telling picks you out of the herd to speak the stag's words / the great telling waits all night for the moon to rise.
   magic: the illusionist gives you a line in the procession / the glamour will not hold, and the crowd waits in the square all day.
   times 39: per background artist: about 1 in 20 are given a line at some point (estimate); about 8 lives in 1,000 work as an extra (catalogue share; estimate)
   times 40: per background artist: on most shooting days outdoors (estimate)
   lead: screen, the extra who becomes an actor ('a screen test' 49).
41-42. community theatre director (s3; calls UB / WRG; young_adult adult mature elder; age 18-100; rate .05; gap 2-5):
   `the oldest member wants the lead again` (the turning point: the society's oldest member can no longer remember the
   lines; cast them anyway, a smaller part, a prompter in the wings, a frank talk; `grants: directing actors`);
   `the pantomime that pays for the year` (the panto or a new play: play safe, put on the new play, both, ask the
   members; `grants: name on the local scene`).
   earth: the society's casting meeting / the committee and the bank statement.
   tribal: the oldest player wants to wear the bear mask one more winter / the old midwinter telling, or a new one.
   magic: the pageant's eldest player wants the king's part again / the feast-day pageant pays for the year, or a new mystery play.
   times 41: per community theatre director: about once in three years (estimate); about 3 lives in 1,000 direct the local players (catalogue share; estimate)
   times 42: per community theatre director: once a year, when the season is chosen (estimate)
   lead: amateur and late life: the director who gives the lead at seventy.
43-44. artistic director (s4; calls RG / WUB; adult mature elder; age 25-100; rate .5):
   `a safe season or the new writers` (the turning point: the board wants old favourites to save the money, and the new
   writers were promised a stage; safe, new, half and half, resign over it);
   `the audience that stopped coming` (empty seats on a Tuesday: cheap tickets, a new show, a tour of the schools, cut
   the season; `grants: good name in town`).
   earth: a board meeting about the season / a house a third full.
   tribal: the elders want the old tellings at the gathering, and the young ones have made new ones / fewer bands come to the gathering's tellings.
   magic: the Order's patrons want the old masques, and the new play-makers were promised the stage / the court has found a new pleasure, and the galleries are empty.
   times 43: per artistic director a year: about 1 in 3 (estimate); about 1 life in 10,000 runs a theatre (catalogue share; 1,953 US nonprofit theatres, Theatre Facts 2019; estimate)
   times 44: per artistic director: most seasons have a stretch of empty houses (estimate)
   lead: the artistic director who casts the season's leads.

## Part 4: crossings, parts, falls and reach (file stage-events.lib)

Life events: stakes 1, alpha even, the five one-color options plus one balanced combination set (library-spec
section 3); per_year is the yearly rate per eligible person (the holds: title or perk) by stage (child juvenile
young_adult adult mature elder), with times:, likelier:, rarer: and drivers: in words as in the example (the drivers
the windows in helps.py name). Each line names the set to use.

Crossings and parts (pairs):
45. `the showcase for agents` (holds: drama school student | drama school diploma; D1a pairs; stages young_adult adult;
   age 18-40; per_year 0 0 .3 .1 0 0; gap 2-4). Twenty minutes in front of a hundred agents and casting directors.
   `title: professional actor` with `grants: an agent who believes in you` on options at chance 40 to 50; skip the
   agents and take a show to the fringe (`grants: a fringe slot`); go home to a regional company; `grants: a year group
   from drama school`.
   earth: the graduates' showcase in a studio theatre, an agent in every seat.
   tribal: the apprentices play before the elders of every band at the gathering.
   magic: the guild school's final masque, with the brokers and the company masters in the gallery.
   times 45: per final-year drama school student: once, in the last year; about 700 to 1,000 acting graduates a year leave accredited UK schools, and most sign with an agent at or soon after the showcase (estimate)
   lead: the craft road (U) and the networker (B): the agent who brings the auditions for leads.
46. `cast as understudy to the lead` (holds: professional actor; D1b pairs; stages young_adult adult mature elder;
   per_year 0 0 .08 .06 .03 .01; gap 2-4). `title: understudy` on options at chance 25 to 35; turn it down for a part
   elsewhere; ask for a small part as well; learn it in a week (`grants: learning lines`).
   earth: a long-running musical needs a cover for the lead.
   tribal: the elders want someone who can wear the great mask if its wearer falls.
   magic: the court playhouse needs a second for its leading player for the winter season.
   times 46: per professional actor a year: about 1 in 15 young actors are offered a cover; long runs cover every lead (estimate)
   lead: the company actor and the understudy (W).
47. `the understudy goes on` (holds: understudy; D2a pairs; stages young_adult adult mature elder; per_year 0 0 .5 .5 .5
   .3; gap 1-2). The lead is off tonight. `title: lead actor or actress` on options at chance 15 to 25 (the producers keep
   you on as the lead) in every color; play it as rehearsed (`grants: good notices`), play it your own way, play it for
   the company (`grants: a director who keeps casting you`).
   earth: an announcement before the curtain: at this performance the part will be played by...
   tribal: the wearer of the great mask lies sick, and the mask is handed to you at dusk.
   magic: the leading player's carriage has overturned, and the herald cries your name instead.
   times 47: per understudy: about 1 in 2 go on at least once in a run; about 1 in 5 who go on are kept on or given a lead soon after (estimate)
   lead: stage (W): the understudy who becomes the lead.
48. `the part of a lifetime is cast` (holds: professional actor | voice actor | amateur actor | a lead role to remember;
   D2b pairs; stages young_adult adult mature elder; per_year 0 0 .02 .015 .01 .006; gap 3-8). A great stage part or a
   film wants an unknown, or the right face at any age. `title: lead actor or actress; professional actor` on options in
   every color at chance 4 to 8 with `requires: casting directory listing | without: approval | lacking: .3` (an unlisted
   amateur is seen only at an open call); `grants: auditioning`; withdraw; send a self-tape and forget it.
   earth: the casting call for a famous old play's great part, or a film that wants a face nobody knows.
   tribal: the clans will tell the oldest story at the gathering, and every band sends a player for the first ancestor.
   magic: the court will stage the old epic of the realm, and the master of the play is looking everywhere.
   times 48: per professional actor, voice actor or amateur with a lead behind them a year: about 1 in 50 young adults and fewer later try for a part that could change their life; about 1 in 15 of those who try get it (estimate)
   lead: stage and screen; amateur and late life (a film that casts a non-actor, at any age).
49. `a screen test` (holds: professional actor | background artist | a showreel; D3a pairs; stages young_adult adult
   mature elder; per_year 0 0 .04 .03 .02 .01; gap 2-5). `title: lead actor or actress; professional actor` on options at
   chance 8 to 12; a supporting part in a series (`grants: screen acting`, `grants: a known face` at a low chance);
   ask for notes; turn it down.
   earth: a screen test for the lead in a new series.
   tribal: the shaper of the shadow telling wants to see your shape against the wall.
   magic: the illusionist wants to see if the glamour takes to your face.
   times 49: per professional actor, extra or actor with a showreel a year: about 1 in 25 young adults are tested for a screen part; about 1 test in 10 becomes the lead (estimate)
   lead: screen.
50. `the leading player leaves the company` (holds: professional actor; D3b pairs; stages young_adult adult mature
   elder; per_year 0 0 .04 .05 .04 .02; gap 2-5). In a rep or touring company: `title: lead actor or actress` on options
   at chance 20 to 30 (the company actor steps up); bring in a friend; let the director choose; leave too.
   earth: the regional company's leading actor leaves for television.
   tribal: the band's teller who always wore the great mask goes to live with his wife's people.
   magic: the company's leading player is lured to the court playhouse.
   times 50: per professional actor in a company a year: about 1 in 25 (estimate)
   lead: the company actor (W) and the rooted regional player (G).
51. `opening night at the fringe` (holds: a fringe slot; D4a pairs; stages young_adult adult mature elder; per_year 0 0
   .8 .8 .8 .8; gap 1-2). It is your show. `grants: a lead role to remember` on most options (chance 80 to 90);
   `title: lead actor or actress; professional actor` on the transfer offer at chance 8 to 12; `title: professional
   actor` on signing with the agent who came, at chance 10 to 15; `grants: a cult following` at 15; `grants: good
   notices`; keep the day job and come back next year.
   earth: forty seats, a borrowed light, and a reviewer in the second row.
   tribal: the outer fires of the gathering, where anyone may play, and a chief's teller watching.
   magic: a booth at the fair, a borrowed lamp, and a company master in the crowd.
   times 51: per person with a fringe slot: once a festival; most fringe shows play to small houses, and about 1 in 10 is offered more (estimate)
   lead: fringe and one-person shows (R).
52. `the lead voice in a series` (holds: voice actor; D4b pairs; stages young_adult adult mature elder; per_year 0 0 .08
   .08 .06 .03; gap 2-4). `title: lead actor or actress` on options at chance 10 to 15; `grants: repeat fees`; a smaller
   voice in the same series; turn it down.
   earth: the casting for the lead voice of an animated series.
   tribal: the band wants a hidden voice for the first ancestor in every telling of the winter.
   magic: a puppet theatre wants its hero's voice for every show of the season.
   times 52: per voice actor a year: about 1 in 12 try for a lead voice; about 1 in 8 who try get it (estimate)
   lead: voice.
53. `casting night at the local players` (holds: amateur actor; D5a pairs; stages juvenile young_adult adult mature
   elder; age 14-100; per_year 0 .3 .3 .3 .3 .3; gap 1-2). `grants: a lead role to remember` on options in every color at
   chance 25 to 35; take the small part gladly (`grants: a company that feels like family`); stage manage instead;
   stay home.
   earth: auditions in the church hall for the spring play.
   tribal: the band chooses who will play the old stories at midwinter.
   magic: the guild's mystery players choose the parts for the feast-day pageant.
   times 53: per amateur actor a year: about 1 in 3 audition for a lead; societies put on two to four shows a year, and about 1 in 3 who try get the lead (estimate)
   lead: amateur and late life (G R): the amateur lead, at any age, the lead at seventy included.
54. `the summer show casts its lead` (holds: youth theatre member; D5b pairs; stages child juvenile; age 6-17; per_year
   .3 .3 0 0 0 0; gap 1). `grants: a lead role to remember` at chance 20 to 30; a part in the chorus; help the younger
   ones; stay out of it this year.
   earth: the youth theatre's summer show, and the list on the noticeboard.
   tribal: the children's telling at midsummer, and who will play the hare.
   magic: the children's company's summer masque.
   times 54: per youth theatre member: once a year, at the summer show (estimate)
   lead: youth and school.
55. `a casting call for children` (holds: youth theatre member | a lead role to remember; D6a pairs; stages child
   juvenile; age 7-15; per_year .03 .03 0 0 0 0; gap 2-4). A touring musical or a film wants children. A parent or carer
   agrees or does not; a licence, a chaperone, school hours kept. `grants: child performance licence; a lead role to
   remember` (the child lead) at chance 10 to 15; `grants: child performance licence` (the ensemble) at chance 30 to 40;
   the parents say school first; go along for the experience (`grants: auditioning`).
   earth: a touring musical's open call for children, with a chaperone at every rehearsal.
   tribal: the gathering's keeper of tellings wants a child for the spirit of the spring, with the mother beside her.
   magic: the court playhouse wants a child for the prince, with the guild's licence and a chaperone.
   times 55: per child in a youth theatre or with a lead behind them a year: about 1 in 30 meet a professional casting for children; over 90,000 child performance licences are issued a year in England, many for the same child (an estimate from a third of local authorities, 2014)
   lead: youth and school (safe forms only).
56. `the director calls again` (holds: a director who keeps casting you; D6b pairs; stages young_adult adult mature
   elder; per_year 0 0 .2 .2 .15 .1; gap 1-3). `title: lead actor or actress; professional actor` on options at chance
   25 to 35; a smaller part; turn it down for something new; ask to read for the lead.
   earth: a director you worked with twice rings about a new production.
   tribal: the shaper of the tellings sends a runner: he wants you again for midsummer.
   magic: the master of the play sends a letter: a new piece, and he wants you.
   times 56: per actor with a director who keeps casting them a year: about 1 in 5 are called again; directors recast actors they trust (estimate)
   lead: the craft actor (U) and the company player (W).
Side doors, exits, rivalry and reach (triads):
57. `a voice for the cartoon` (holds: acting | accents and voices | community-radio presenter; D1a triads; stages
   young_adult adult mature elder; per_year 0 0 .01 .01 .006 .003; gap 3-6). `title: voice actor` on options at chance 20
   to 30; `grants: a showreel` (a voice reel); `grants: accents and voices`; let it pass.
   earth: a children's cartoon needs voices, and a friend passes your name on.
   tribal: the band needs hidden voices for the animals in the winter tellings.
   magic: a puppet theatre needs voices for its dragon and its talking cat.
   times 57: per person who acts or has a radio voice a year: about 1 in 100 hear of voice work they could try for (estimate); about 1 life in 2,000 voices for a living (catalogue share; estimate)
   lead: voice, the first step to 'the lead voice in a series' (52).
58. `the stage management team is a person short` (holds: stagecraft | stage technician | drama school student |
   amateur actor; D1b triads; stages young_adult adult mature; per_year 0 0 .03 .02 .01 0; gap 3-6). `title: stage
   manager` on options at chance 45 to 55; `grants: calling the show`; help for a week only; say no.
   earth: a touring show's stage manager has left, and the company needs one by Monday.
   tribal: the keeper of the fire and the masks is sick, and the gathering is in three days.
   magic: the playhouse's book-keeper has fled with the takings, and the season opens on the morrow.
   times 58: per person with stagecraft, a stage technician, a drama student or an amateur actor a year: about 1 in 40 young adults are offered stage management work (estimate)
   lead: the stage manager's road; the one who sends on the understudy (47).
59. `a director is needed for the autumn play` (holds: amateur actor | drama teacher | directing actors; D2a triads;
   stages young_adult adult mature elder; per_year 0 0 .02 .05 .05 .03; gap 3-6). `title: community theatre director`
   on options at chance 55 to 65; `title: director` (a small professional company wants a director) at chance 25 to 35
   with `requires: directing actors | without: means | lacking: .3`; `grants: directing actors`; say no.
   earth: the society's director has moved away, and the autumn play has no one.
   tribal: the old shaper of the tellings has died, and midwinter is coming.
   magic: the guild's master of pageants is gone, and the feast day is a month away.
   times 59: per amateur actor, drama teacher or anyone with directing experience a year: about 1 in 25 adults are asked to direct a show (estimate)
   lead: amateur and late life: the director who casts the local lead.
60. `the script competition` (holds: writing stories | writing scripts | novelist; D2b triads; stages juvenile
   young_adult adult mature elder; per_year 0 .01 .03 .03 .02 .01; gap 2-5). `title: playwright or screenwriter` on options
   at chance 5 to 10; `grants: writing scripts`; `grants: a fringe slot` (the prize is a staged reading); enter
   nothing.
   earth: a national script competition, with a staged reading as the prize.
   tribal: the gathering will hear new tellings this summer, and the best will be played at the great fire.
   magic: the court offers a laurel for a new play, to be staged at midsummer.
   times 60: per person who writes a year: about 1 in 35 enter a script competition (estimate); most competitions get thousands of entries
   lead: the writer who writes the lead, and the one-person show.
61. `the theatre needs an artistic director` (holds: director; D3a triads; stages adult mature elder; per_year 0 0 0 .04
   .05 .02; gap 3-6). `title: artistic director` on options at chance 10 to 20; back another; stay freelance.
   earth: the regional theatre's artistic director steps down after ten years.
   tribal: the keeper of the gathering's tellings has grown too old.
   magic: the court playhouse's master has died, and the Order will choose another.
   times 61: per director a year: about 1 in 25 see a theatre's top post open that they could apply for (estimate); about 1 life in 10,000 runs a theatre (catalogue share; estimate)
   lead: the theatre that chooses its leads.
62. `leaving acting for another life` (holds: professional actor | voice actor | lead actor or actress; D3b triads;
   stages young_adult adult mature elder; per_year 0 0 .06 .08 .08 .05; gap 2-5). `title: drama teacher`, `title: casting
   director` (requires: a casting eye | without: means | lacking: .3), `title: talent agent` (requires: striking a
   deal | without: means | lacking: .3), `title: producer`, `title: stage manager` (requires: stagecraft | without:
   means | lacking: .3), a base career (`drops: professional actor`), or stay.
   earth: a year without a part, a partner who wants a steadier life, an offer from a friend's firm.
   tribal: the hunt and your own hearth call louder than the tellings.
   magic: a merchant house offers a clerk's stool and a wage every week.
   times 62: per professional or voice actor a year: about 1 in 15 weigh leaving; most actors leave the profession within ten years (estimate)
   lead: the leads who leave, and what they become.
62a. (round 5, 2026-10-07, checklist P3, P12, P16) `the city wants the town's show` (holds: community theatre director |
   a company of your own; tenure 3-100; D1b triads; stages young_adult adult mature elder; per_year 0 0 .03 .04 .03
   .015; gap 5-10). A city theatre wants the town's show for a run, and asks who will run it. Singles at 30: W `title:
   stage manager`, U and R `title: director` (all three `requires: community theatre director | without:
   impossible`), B `title: producer`, G keeps the show at home (good name in town). Triads at 70: the budget, the show
   handed to the youngest, the council's grant, the show reworked with the cast, a film of the last night.
   times 62a: per community theatre director or small company of three years a year: about 1 in 30 (estimate).
   lead: each road's first paid post from the town's stage (White stage management, Blue and Red directing, Black
   producing, Green the town).
62b. (round 5, 2026-10-07, checklist P16) `the school needs someone to take drama` (holds: teacher; tenure 2-100; D1b
   pairs; stages young_adult adult mature; per_year 0 0 .025 .025 .015 0; gap 4-8; LIFE_STAGE: acting, or the local
   players or a society of one's own behind them). The school's drama teacher has left, and the head asks. Singles at
   30: W U B `title: drama teacher`, R directs the school musical once (directing actors), G starts a Saturday youth
   theatre (`title: community theatre director`). Pairs at 70: a budget first, a colleague who trained, an evening
   course (`aims: drama teacher`), a play for the year group, the class taken to see the local players. Children only
   in school hours or in the hall with other adults near.
   times 62b: per teacher of two years with a stage history a year: about 1 in 40 (estimate).
   lead: the teacher's step into [drama teacher], which only the background rule carried before.
63. `two actors, one part` (holds: professional actor | understudy; D4a triads; stages young_adult adult mature elder;
   per_year 0 0 .1 .08 .05 .03; gap 1-3). You and {rival} are the last two for the lead. `title: lead actor or actress`
   on fair options at chance 40 to 50; call in the producer who backs you (`requires: a producer who backs you |
   without: approval | lacking: .3`; mark made an enemy); a whisper about the rival (mark hid a wrong; closed: approval;
   backfire: the company finds out); step aside for a friend (mark made a friend); prepare the scene all week.
   earth: two actors left at the recall, and one part.
   tribal: two players want the great mask, and the elders will choose at dawn.
   magic: two players are left for the court lead, and the patron will choose.
   times 63: per professional actor or understudy a year: about 1 in 10 reach the last two for a lead (estimate)
   lead: the networker (B) takes it from a rival, the fair player wins it, the friend gives it up.
64. `the show is a hit` (holds: lead actor or actress | playwright or screenwriter | director | producer; D4b triads;
   stages young_adult adult mature elder; per_year 0 0 .03 .03 .03 .02; gap 3-8). `grants: known across the country` on a
   few options at chance 8 to 15; `grants: an award for acting` for the lead at chance 10; `grants: a producer who backs
   you`; stay with the company; go back to small work.
   earth: queues round the block, a sold-out run and a transfer.
   tribal: every band in the valley asks for your telling.
   magic: the court asks for a command performance.
   times 64: per lead, writer, director or producer a year: about 1 in 30 have a show that sells out and moves on; only a few of those become known across the country (estimate)
   lead: reach for the lead: [known across the country], then [a household name].
65. `the reviews are in` (tier: read; holds: professional actor | lead actor or actress | director | playwright or
   screenwriter | amateur actor | community theatre director; stages young_adult adult mature elder; source: career;
   base: need:competence-.03; condition in engine-conditions.py, READ_STAGE): five readings of the notices, each with
   impact, also and say, as in the read example: a duty done (W: the work was honest, whatever they wrote), a lesson (U:
   the critic saw what the director missed), a game (B: notices sell tickets, nothing more), a wound (R: one line that
   will be remembered for years), the way it goes (G: the local paper always says the same).
   earth: the morning papers and the online notices after the opening.
   tribal: the elders speak of the telling the next morning, and the young ones repeat what they said.
   magic: the broadsheets are cried in the square the morning after the opening.
   times 65: per actor, director or writer with a show that opens: once a production; most professional openings and many amateur ones are reviewed somewhere (estimate)
   lead: every road: what the lead reads in the morning.

## Part 5: world-only moments (file stage-worlds.lib)

Life events like part 4 (stakes 1, alpha even, five one-color options plus one combination set), each pair using the
two halves of one line, so each world stays even on its own. A supernatural act is one choice among ordinary ones,
never the only way; it carries a real price (a debt, a mark, a closed: line with a backfire); round 5 (2026-10-07):
the magic comes from someone else (a medium, a hedge-witch, an illusionist), never from the person's own gift, which is
held for a later version. Each world has a crossing that gives the lead.
Tribal (the spirits and the shaman are part of how the band tells its stories):
66. `the old teller dies at midwinter` (`only: tribal`; holds: acting | amateur actor | youth theatre member | telling a
   story aloud; D5a triads; stages juvenile young_adult adult mature elder; per_year 0 .01 .02 .02 .02 .03; gap 5-10).
   The tellings need a new voice: `title: professional actor` (the band keeps you as its teller-player) at chance 30 to
   40; `title: drama teacher` (teach the children the tellings) for an elder; `grants: telling a story aloud`; let a
   younger one take it; ask the shaman.
   tribal: the old teller dies in the long nights, and the fire is silent where the stories were.
   times 66: per player or teller in the tribal world a year: about 1 in 50, when a band's teller dies or grows too old (estimate)
   lead: tribal door, then 'chosen to wear the great mask' (68).
67. `the spirits ride the dancer` (`only: tribal`; holds: professional actor | lead actor or actress | amateur actor; D5b
   triads; stages young_adult adult mature elder; per_year 0 0 .01 .01 .01 .01; gap 5-10). A fall: in the deepest telling
   you go into a trance the shaman cannot read, and the band fears what rides you: let the shaman cleanse you, say it
   was only the telling, embrace it (mark took a wild risk; the band may cast you out), step down from the great mask
   (`drops: lead actor or actress`), use it to play the ancestor as never before.
   tribal: in the deepest telling the fire roars, you speak in a voice that is not yours, and the band draws back.
   times 67: per player in the tribal world a year: about 1 in 100 (estimate)
   lead: tribal fall: the lead lost, or played as never before.
68. `chosen to wear the great mask` (`only: tribal`; holds: professional actor | amateur actor | understudy | a lead
   role to remember; D2a pairs; stages young_adult adult mature elder; per_year 0 0 .02 .03 .03 .02; gap 3-8). The elders
   choose who will wear the mask of the first ancestor at the summer gathering, and the mask is said to take something
   from whoever wears it: `title: lead actor or actress; professional actor` on options at chance 20 to 30 (one option
   with the mask's price: mark took a wild risk; binds); refuse it; give it to another; ask the shaman what it takes.
   tribal: the elders hold up the great mask at the gathering's first fire, and turn to you.
   times 68: per player in the tribal world a year: about 1 in 40; one player a summer wears the great mask for each gathering (estimate)
   lead: tribal crossing: the lead.
69. `the mimic who mocks the chief` (`only: tribal`; holds: professional actor | amateur actor | lead actor or actress;
   D2b pairs; stages young_adult adult mature elder; per_year 0 0 .02 .02 .02 .01; gap 5-10). A fall: you mocked the chief
   in a telling, the band laughed, the chief did not: apologise at his fire, defy him (mark defied an authority), leave
   for another band (mark left home), turn it into praise next time, step down (`drops: lead actor or actress`).
   tribal: the whole band laughs at your mimic of the chief, and the chief rises and walks out of the firelight.
   times 69: per player in the tribal world a year: about 1 in 50 (estimate)
   lead: tribal fall.
Magic (old powers; a gift may awaken):
70. `the illusionist players come to town` (`only: magic`; no holds; D6a triads; stages juvenile young_adult adult
   mature elder; age 14-90; per_year 0 .01 .01 .01 .005 .005; gap 5-10). A company whose glamours make every scene appear
   in the air needs players and hands: `title: professional actor` (join the wagons) at chance 20 to 30 with `requires:
   acting | without: means | lacking: .3`; `title: background artist` (the procession crowd); `title: amateur actor`
   (the town's own players play with them); `grants: acting`; watch from the crowd.
   magic: painted wagons in the square, and a dragon of light circling the town hall at dusk.
   times 70: per person in the magic world a year: about 1 in 100 (estimate)
   lead: magic door, then 'a glamour that makes the play real' (72).
71. `the theatre where the dead come to watch` (`only: magic`; holds: professional actor | lead actor or actress; D6b
   triads; stages young_adult adult mature elder; per_year 0 0 .005 .005 .005 .005; gap 10-20). On one night a year the
   dead fill the gallery; whoever leads that night is remembered by both worlds: `title: lead actor or actress` at chance
   25 to 35, with a token left for the dead (mark took a wild risk); have the company's medium call the dead into the
   play (round 5: closed: approval, with a backfire); refuse to play; play it for one face in the gallery.
   magic: the old playhouse on the night of the dead, and every seat in the gallery is taken by someone long gone.
   times 71: per player in the magic world a year: about 1 in 200 (estimate)
   lead: magic crossing: the lead.
72. `a glamour that makes the play real` (`only: magic`; holds: professional actor | amateur actor; D1a pairs; stages
   young_adult adult mature elder; per_year 0 0 .01 .01 .01 .005; gap 5-10). An illusionist offers a glamour that makes
   the audience see and feel the play as real, for the lead's night, and it asks for something of the player:
   `title: lead actor or actress; professional actor` at chance 30 to 40 with the glamour (mark took a wild risk; binds);
   play it plain (`title: lead actor or actress; professional actor` at chance 8 to 12); wear a glamour bought from a
   hedge-witch (round 5: closed: approval, with a backfire); refuse the illusionist; tell the Order.
   magic: an illusionist in a velvet coat, in your dressing room, with a small silver bell.
   times 72: per player in the magic world a year: about 1 in 100 (estimate)
   lead: magic crossing: the lead, with a price or without.
73. `the mask that changes its wearer` (`only: magic`; holds: acting | professional actor | amateur actor; D1b pairs;
   stages juvenile young_adult adult mature elder; per_year 0 .01 .01 .01 .01 .01; gap 5-10). An old mask in a costume
   trunk lets its wearer become anyone on stage, and a little more of them each time: wear it once
   (`grants: a lead role to remember`), wear it always (mark took a wild risk; identity), break it, sell it, give it to
   the Order; `title: professional actor` on one option (a company master sees you in it) at chance 20 to 30.
   magic: a mask of white lacquer at the bottom of the costume trunk, warm to the touch.
   times 73: per player in the magic world a year: about 1 in 100 (estimate)
   lead: magic door: the lead in the mask.

## Part 6: threshold seasons (file stage-seasons.lib)

Emren chose a "threshold season" for every crossing (point 6): a few months of linked moments around the rite, the
person more open to change, and one transforming chance. Fields: `threshold: title:<name>` (a season that opens when
that title is gained; the engine brings the steps about 1, 10 and 22 weeks in), `step: 1 | 2 | 3`, `transform: yes`.
Every moment here is `tier: inner` with `requires:` in words ("in the threshold season of <title>: within the first
six months after taking the title"), `likelier:` and `rarer:` in words, `holds: <that title>`, stakes .8, the title's
stages and ages, alpha even with the five one-color options plus one full cross cycle (each season uses s1 to s4 once),
and the usual story fields. Each season has a moment about who the person now answers to: a partner who sees them
less, friends from before, the people at home, the company.
74-77. drama school student (opened by `drama school auditions`; juvenile young_adult adult; age 16-40):
   `the first morning of the first term` (1); `the movement class where you cannot hide` (2); `who you are when you are
   not acting` (2, transform: the craft, the company, the career, the fire, home); `the first-year assessment` (3;
   one option `drops: drama school student` at a low chance, as some schools ask students to leave).
   earth: a converted warehouse, a timetable from nine to nine, and thirty strangers in black.
   tribal: the first winter at an old teller's fire in another band.
   magic: the guild school's hall, its masters and its rules.
   times 74: per new drama school student: once, in the first weeks after taking the title; about 3 lives in 1,000 (catalogue share)
   times 75: per new drama school student: once, in the first months of the threshold season; about 3 lives in 1,000 (catalogue share)
   times 76: per new drama school student: once in the threshold season, for most who are still open to change; about 3 lives in 1,000 (catalogue share)
   times 77: per new drama school student: once, near the end of the first year; about 3 lives in 1,000 (catalogue share)
   lead: the craft road (U).
78-81. professional actor (opened by `the showcase for agents`, `an open audition in the city` or any way in):
   `the first paid read-through` (1); `the second job does not come` (2; the first job over and nothing after; the day
   job, the self-tapes, the doubts); `what kind of actor you will be` (2, transform: the company player, the craft
   actor, the career, the fire, the local stage); `a year on, still an actor` (3).
   earth: a long table, a script with your name on the cast list, and a cup of tea you are too nervous to drink.
   tribal: the first winter as the band's teller-player, fed by every hearth.
   magic: the first reading with a licensed company, and your name on the playbill.
   times 78: per new professional actor: once, in the first weeks after taking the title; about 4 lives in 1,000 (catalogue share)
   times 79: per new professional actor: once, in the first months of the threshold season; about 4 lives in 1,000 (catalogue share)
   times 80: per new professional actor: once in the threshold season, for most who are still open to change; about 4 lives in 1,000 (catalogue share)
   times 81: per new professional actor: once, near the end of the first year; about 4 lives in 1,000 (catalogue share)
   lead: every professional road; the actor's choice of road to the lead.
82-85. lead actor or actress (opened by `the understudy goes on`, `the part of a lifetime is cast`, `a screen test`,
   `the leading player leaves the company`, `opening night at the fringe`, `the lead voice in a series`, `the director
   calls again`, `two actors, one part` or any way in): `your name at the top of the bill` (1); `the company looks to
   you` (2); `who you play it for` (2, transform: the audience, the craft, the career, the company, the people at
   home; its acts carry identity and often binds); `the last night of the run` (3).
   earth: your name above the title, a dressing room with a star on the door, a partner at home who sees you on Sundays.
   tribal: the great mask on its peg by your hearth, and every child of the band watching you.
   magic: your name cried first by the herald, and a patron's flowers in the dressing room.
   times 82: per new lead: once, in the first weeks after taking the part; about 1 life in 1,000 (catalogue share; estimate)
   times 83: per new lead: once, in the first months of the threshold season; about 1 life in 1,000 (catalogue share; estimate)
   times 84: per new lead: once in the threshold season, for most who are still open to change; about 1 life in 1,000 (catalogue share; estimate)
   times 85: per new lead: once, near the end of the run or the first year; about 1 life in 1,000 (catalogue share; estimate)
   lead: the lead held, in every world.
86-89. director (opened by `a director is needed for the autumn play` or any way in): `the first day of rehearsals` (1);
   `the designer who wants a different show` (2); `the show you want to make` (2, transform); `press night` (3).
   earth: a rehearsal room, a model box, and a cast waiting to hear what you think the play is about.
   tribal: the first telling you shape, with the whole band at the fire.
   magic: the first company you direct, in a playhouse that has seen a hundred masters.
   times 86: per new director: once, in the first weeks after taking the title; about 1 life in 1,000 (catalogue share; estimate)
   times 87: per new director: once, in the first months of the threshold season; about 1 life in 1,000 (catalogue share; estimate)
   times 88: per new director: once in the threshold season, for most who are still open to change; about 1 life in 1,000 (catalogue share; estimate)
   times 89: per new director: once, near the end of the first year; about 1 life in 1,000 (catalogue share; estimate)
   lead: the director who chooses and shapes leads.
The transform moment's options are the big forks of that season, each a real way of holding the new title (its
profiles in the catalogue): its acts carry `identity` and often `binds`. Steps 1 and 3 are lighter, with
everyday-sized stakes in the words.

## Balance layout (what keeps the pack even)

- Everyday pairs: 20 in all (3 door pairs, 8 main rungs, 9 side roads and community). Their two-color calls hold each
  of the ten color pairs exactly twice (WG, BR, WB, UR, BG, WR, UG, WU, UB, RG), and each pair's cross cycle rotates
  s1 to s4, five pairs per cycle (s1: A, lead, playwright, casting director, producer; s2: B, understudy, amateur
  actor, talent agent, background artist; s3: C, drama school student, youth theatre member, drama teacher, community
  theatre director; s4: professional actor, director, stage manager, voice actor, artistic director).
- Echoes: four (7 to 10), each even on its own with a full cross cycle (s4, s1, s2, s3).
- Life events (Earth and every world, 20): pairs D1 to D6, both halves (45 to 56), and triads D1 to D4, both halves
  (57 to 64), so every pair appears six times and every triad four times, ally and enemy alike. The read event (65) is
  even on its own.
- World-only life events (8): tribal D5 triads and D2 pairs, both halves (66 to 69); magic D6 triads and D1 pairs, both
  halves (70 to 73). Each world's own set is even, so the pack is even in every world.
- Threshold seasons (16): five one-color options plus one full cross cycle each, the four cycles four times each.
- Chance: the mean chance per means color within 3 points overall and in every stage; mean chance about 68 to 72 for
  everyday and life events, 72 to 78 for echoes and season moments. Parts carry their real chances (the pack rules
  above); balance them across colors inside each moment, so no color wins parts more easily.

- Round 5, 2026-10-07: three new halves. 62a is D1b triads and 62b is D1b pairs (stage-events.lib), and LS7 'the
  other side of the table' (stage-longshots.lib) is D1a pairs, so every pair now appears 11 times across the pack;
  the D1b triads (WUB, WRG, WBG, URG, UBR) appear 8 times and the other five 7, one half apart (an odd number of triad
  halves cannot be even; a later D1a triads moment would close it). Each new moment is even on its own.

In all: 89 moments planned (6 doors and 4 echoes, 16 on the main rungs, 18 on the side roads and community rungs, 20
life events with one read event, 8 world-only events, 16 season moments).

## Balance and checks (each file must pass all three)

- Build: copy build.py to your scratch folder (it already accepts threshold:, step:, transform:, aims:, share:,
  lacking: and the *_if_fails act fields) and run `python3 -B build.py <yourfile>.lib --out <scratch>`; it must end with
  no layout problems. Also make sure no moment name or option label of yours appears in chroma-library/earth.py or in
  the science-, politics- and other stage-*.lib files (grep them).
- Chance and tags: `python3 /mnt/project-files/chroma-packs/tools/lib_stats.py <yourfile>.lib`: the mean chance per
  means color within 3 points overall and in every stage; tag counts (habit, door, identity, binds, self_control + and
  -) close to even per means color.
- Names: `PYTHONDONTWRITEBYTECODE=1 python3 -B /mnt/project-files/chroma-packs/tools/check_pack.py stage` (it reports
  unknown title or perk names and checks the catalogue against this brief); it must print "All checks pass".

## Files and rules

- Write only your own file in /mnt/project-files/chroma-packs/stage/ (named in your task). Write moment by moment
  (append), so partial work survives. Re-read before writing; about ten seconds after writing, read it back and re-apply
  if another write replaced yours.
- Never write into chroma-library/, chroma-engine/, chroma-game/ or chroma-art/, nor into science/ or politics/; read
  only. No packages; standard library only. Scratch goes in
  /tmp/claude-0/-home-claude/e40218c8-fe2b-58e7-bec9-a2e19282a5e8/scratchpad/<your part>/, never in /mnt/project-files.
  Run Python with `PYTHONDONTWRITEBYTECODE=1 python3 -B` so no __pycache__ lands in the shared folder.
- Do not call any mcp__hearthbot__ tool; the thread's own session talks to Emren.
- No AI model names or identifiers in any file.

## Report back

The build line, the lib_stats output (mean chance per means color in every stage), the check_pack line, the moment
names, the share, rate, gap and per_year values you wrote, and anything in this brief you changed and why.
