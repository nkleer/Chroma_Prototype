# Pack: Stage and Screen: Acting, Theatre, Film and Television (modern Earth, with the tribal and magic worlds)

Status: live since 2026-10-06 19:37 Emren's time (16:37 UTC), with Science and Politics (batch.PACKS science,
politics, stage; ../for-the-engine.md, "Go-live and round 5"). Round 5 (2026-10-07) works this pack's rows of the
release checklist (chroma-release/checklist.md, section 5: P3, P5, P8, P9, P12, P14, P15, P16). As of round 5 the
seven .lib files hold 100 moments and build to stage.py: 93 situations, 6 echoes, 1 read event, 990 options, no
layout problems; the Library's check.py: every stage even across W U B R G (largest spread 0% of the average), choice
share .200 for every color, value-tag agreement 62% (the base batch 56%). Emren's ask (packs thread, 01:31): "You can
also work on third content package, you can choose the concept name subject and its content as you seem fit. Lead
actor/actresss availability must be inside with all new content." Emren (21:37): modern Earth terms first, every part
feasible in the other worlds, "even including supernatural sometimes". Emren (21:03): "give more chance than real
odds, but keep it consistent and achievable, if player and character create a good strategy, and they are at right
place at right time." Plan for every pack: ../PROPOSAL.md. Models: ../politics/ and ../science/. Engine name: `stage`.

## Rounds

| Round | When (Emren's time) | What changed in this pack |
| --- | --- | --- |
| 1 | 10-06 morning | calibration on the next2 batch with Science and Politics: door shares, written chances, one more step before a summit, background rates ("Calibration (2026-10-06)" below) |
| 2 | 10-06 13:44 | the steps rule (Emren 09:18, "never from nothing"): every career and summit grows from the rung below (holds:, tenure:, LIFE_STAGE); the long shots merged (stage-longshots.lib: six long shots and two echoes on [a long shot that missed]) |
| fit | 10-06 15:14 | the engine's three-pack fit: one budget for all packs, 1 life in 3 a pack career and 1 in 20 a summit (TARGET_STAGE tiers in roles.py) |
| 3 and 4 | 10-06 15:00, 18:35 | Politics only |
| go-live | 10-06 19:37 (16:37 UTC) | all three packs live; 10-07 about 01:50 the two closed: lines in stage-worlds.lib made strict |
| 5 | 10-07 | the release checklist, row by row (below) |

Round 5, row by row (each change carries a dated "Round 5, 2026-10-07" comment in its file):

- **P3, artistic director and director.** [artistic director]'s rule asks three years as [director] (was five: the
  engine's director stints last about 1 to 4.5 years) at rate .05 (was .02); 'the theatre needs an artistic director'
  comes to a director of two years (tenure 2-100, was 3) at per_year .1. The director's own road opens from all three
  rungs: [directing actors] also comes to a stage manager of three years or a professional actor of five, 'the city
  wants the town's show' (new) offers [director] at 30 to the society's director of three years, and 'the other side
  of the table' (new) gives [director] its long shot.
- **P5, no title above 3x.** Rates lowered title by title (roles.py, the old rate in each comment): [voice actor] .002
  to .0007, [lead actor or actress] .02 to .015, [playwright or screenwriter] .015 to .004, [producer] .05 to .012,
  [stage manager] .003 to .0005, [casting director] .01 to .0025, [talent agent] .012 to .004, [drama teacher] .02 to
  .005. Moments: 'the understudy goes on' per_year .4 (stages 3-5) and .25, 'the director calls again' .15 to .08, 'a
  voice for the cartoon' per_year .03 with its singles at 3 (was 5), 'the stage management team is a person short'
  per_year .015 (only on a touring show) with its singles at 3, 'the script competition' per_year .02.
- **P8, the rung below in roles.py.** Every career and summit lists its rungs below in `rungs=` (table in "Steps and
  long shots"), and every title its req names is among them. `rungs=`, not `after=`: after= would let the rule come only
  to someone who still holds the rung and drop it on the step, which shuts the was() roads (the actor who left, the
  drama school that ended). The holes the "from nothing" check could see are closed: 'filmed by chance in the street'
  needs three years with the local players or as an extra (LIFE gate; its voice try requires [amateur actor]), 'the
  film you made with friends' needs a rung in the writer's rungs= (LIFE gate), [talent agent] no longer comes on a
  casting eye alone, and [drama teacher]'s teacher road needs two years of teaching with the local players behind them.
- **P9, long shots.** Every one-color option at chance 1 to 5 that gives a title carries `grants_if_fails: a long
  shot that missed` (the five step moments whose singles are long shots included), and every career and summit has
  one: 'the other side of the table' (new, pairs D1a) gives [director], [casting director], [talent agent] and [drama
  teacher] theirs. LONGSHOTS_STAGE in engine-conditions.py names all twelve moments; LONGSHOTS_STAGE_PROPOSED is
  retired (those five moments stay steps at real odds 6 to 58). Table in "Steps and long shots".
- **P12, road per color.** One lead color per road, every color covered (table in "Road per color").
- **P14, value tags.** 51 options retagged so their v: values read one of their own colors: agreement 56% to 62%.
- **P15, this file.** Status, rounds, steps and long-shot rules, files and stale pointers brought up to date.
- **P16, met in play.** Two new step moments carry the roads that came only "in time": 'the city wants the town's
  show' (triads D1b; the stage manager, director and producer from the society or a company of one's own) and 'the
  school needs someone to take drama' (pairs D1b; [drama teacher] from [teacher]); with 'leaving acting for another
  life' and LS7 every career and summit has a moment that offers it.
- **The magic world's two gift acts** (coordinator, 10-07): no act rests on the person's own gift (the catalogue has
  no awakened gift, and a perk for it would be a new concept). In 'the theatre where the dead come to watch' the
  company's medium calls the dead down into the play, and in 'a glamour that makes the play real' Red wears a glamour
  bought from a hedge-witch; both keep their colors, chance, grants, mark and v: tags, and their `closed:` is now
  `approval:` with a backfire (the Order's leave; an unlicensed glamour on a public stage).

## Files

| File | What it holds |
| --- | --- |
| catalogue.py | 17 titles (9 careers, 2 facets, 4 community, 2 statuses) and 30 perks, base catalogue format, every share with its source or marked as an estimate |
| roles.py | how each title and perk is gained and lost (ROLES_STAGE, engine ROLES syntax; every career and summit names its rungs below in `rungs=`, round 5), the tiers of the engine's one budget (TARGET_STAGE), and five or-ed widenings of rules the pack does not own (EXTEND_STAGE) |
| helps.py | earned odds: what prepares a person for each title (HELPS_STAGE), the context that opens each window (WINDOWS_STAGE), the half lift on the lead (LIFT_STAGE), and HELPS for the amateur lead perk (HELPS_PERK_STAGE, read by the engine since 03:11) |
| worlds.py | the form of every pack title and perk, the base titles and perks the pathway uses, and the reach ladder, in the tribal and magic worlds (WORLDS_STAGE); the eight world-only doors, crossings and falls (WORLD_ONLY_STAGE) |
| engine-conditions.py | the engine conditions for earth_rules.PACK_RULES["stage"]: the four echoes (ECHO_STAGE) and the two long-shot echoes (ECHO_STAGE_LONGSHOTS), the read event (READ_STAGE), the rung below for twelve life events (LIFE_STAGE) and for the seven long shots (LIFE_STAGE_LONGSHOTS), and LONGSHOTS_STAGE, the twelve moments whose long shots anchor the echoes (the long-shot conditions were merged into this file on 10-06) |
| ../core/reach.py | the reach ladder shared by every pathway pack: [known across the country], [a household name] |
| stage-doors.lib, -rungs.lib, -roads.lib, -events.lib, -worlds.lib, -seasons.lib, -longshots.lib | the 100 moments (round 5): 3 door pairs and 4 echoes (doors); 8 main-rung pairs (rungs); 9 side-road pairs (roads); 22 life events and the read event (events: round 5 added 'the city wants the town's show' and 'the school needs someone to take drama'); 8 world-only events (worlds); 4 threshold seasons of 4 moments (seasons); 7 long shots and their 2 echoes (longshots: round 5 added 'the other side of the table') |
| MOMENTS-BRIEF.md | the plan for the first 89 moments (round 5 notes the new 62a and 62b) in six files (stage-doors, -rungs, -roads, -events, -worlds, -seasons .lib), each with tier, stages, calls or set, holds, rate or per_year, share and gap, a `times:` line, world lines and the lead route it serves |

The 17 titles: careers [professional actor], [voice actor], [director], [playwright or screenwriter], [producer],
[stage manager], [casting director], [talent agent], [drama teacher]; facets [lead actor or actress] (on [professional
actor] or [voice actor]) and [artistic director] (on [director]); community [background artist], [amateur actor],
[youth theatre member], [community theatre director]; statuses [drama school student] (three years) and [understudy]
(one run). The 30 perks: 12 skills, 5 credentials, 5 standing, 5 bonds, 3 assets.

## Checks (round 5, 2026-10-07)

`PYTHONDONTWRITEBYTECODE=1 python3 -B ../tools/check_pack.py stage`:

```
titles (profiles): W 9.00 (0.200)  U 9.00 (0.200)  B 9.00 (0.200)  R 9.00 (0.200)  G 9.00 (0.200)  spread 0.000
perks (ways): W 6.00 (0.200)  U 6.00 (0.200)  B 6.00 (0.200)  R 6.00 (0.200)  G 6.00 (0.200)  spread 0.000
  skill: WUBRG (12 perks)   credential: WUBRG (5)   standing: WUBRG (5)   bond: WUBRG (5)   asset: WUBRG (3)
shares the pack adds per life: titles 0.147, perks 0.249; core perks 0.0533
17 titles, 30 perks, 7 .lib files with 100 moments, 751 catalogue names used by them
All checks pass.
```

Round 5 also: build.py "no layout problems" (93 situations, 6 echoes, 1 read event, 990 options); lib_stats mean
chance per means color 60.5 to 60.8 overall, spread 0.3 to 0.5 points in every stage; check.py section 1 even in every
stage (pairs 11 each; triads 7 or 8, see MOMENTS-BRIEF.md "Balance layout"), section 4 agreement 62% (W 75%, U 46%,
B 72%, R 59%, G 64%); check_setting.py: no year, real place, currency, brand, real event or real person in player text.
(The block above is the round 5 run; the paragraphs below are from the first build, 10-06.)

(The checker also lists each moment the catalogue quotes that is planned in MOMENTS-BRIEF.md and not written yet.)
Every one of the 15 titles with colors has three profiles, one single color and two pairs that cover the other four,
and each color is the single color of three titles, so the titles are exactly even; every perk kind holds all five
colors. Every name used in roles.py, helps.py and engine-conditions.py exists in the base catalogue, the pack, the
reach ladder, the marks, the base moments or the brief's planned moments, and every rule condition uses only the
engine's condition words, with no `&` or `|` inside a comparison (the trap where `&` binds tighter than `>=`), and no
chance() in a req (checked with a scratch parser). The checker's science and politics runs still pass; check_pack.py
was not changed. The engine loads the pack as it stands: `load_batch("earth", packs=["science", "politics", "stage"])`
reads the catalogue, the rules, EXTEND_STAGE, HELPS_STAGE and LIFT_STAGE without an error, with the lead refining both
of its titles and its lift at .5.

**First background run (scratch, 2026-10-06, no moments yet).** The rules alone, 400 lives on each of seeds 11 and 12,
with Science and Politics loaded. The first draft let [acting] reach 69 lives in 100 (x11) through 'the school play',
and that carried [accents and voices] (x52, through the base [second language]), [voice actor] (x30), [drama teacher]
(x9) and the community titles with it. The rules were narrowed (the school play now leads only to [youth theatre
member]; the second-language route needs [professional actor]; [drama teacher] needs drama training, acting work, or a
teacher's own youth theatre or amateur past), and the community rates lowered. After that the rules alone give
[youth theatre member] .11 (x1.4), [amateur actor] .03 to .035 (x0.8), [background artist] .003 to .005, [acting] .045
to .055 (x0.8), [a lead role to remember] .01 (x0.3), and no career: the doors and crossings are meant to carry those,
and calibration follows once the moments exist. ([youth theatre member]'s rate was then halved again, to leave room for
its door.) The colour pie stays with the run without the pack: pooled over the two seeds, every colour is within .006 at
40 and at 70 (Science and Politics only: [.243 .173 .161 .198 .228] at 40, [.261 .164 .156 .180 .241] at 70; with
Stage and Screen: [.243 .176 .159 .201 .222] and [.263 .163 .150 .186 .239]).

## The pathway map

```
 doors ─ 'a flyer for the youth theatre'      'the local players need a cast'     'drama school auditions'
         'auditions for the school production' 'extras wanted for a film in town'  'an open audition in the city'
 echoes  'the part you never got to play' (the school play)   'never too late for the stage' (retirement)
         'the show you wrote to star in' (an idea, the wish to be seen)   'the part that came with the letter'
            │                          │                         │                          │
  youth theatre member ─────> amateur actor ──────> community    background artist     drama school student (status)
   'the summer show casts its lead'   │            theatre director   │ 'you, say this line'   │ 'the showcase for agents'
   'a casting call for children'      │ 'casting night at the        │ 'a screen test'         ▼
   (+ child performance licence)      │  local players'              └──────────────> professional actor <── 'an open audition
            │                         ▼                                                  │   ▲                  in the city'
            └───────────> [a lead role to remember] <── 'opening night at the fringe' <─┼───┘ (a fringe run, an agent)
                          (the amateur, child and                                        │
                           one-person-show lead)       'cast as understudy to the lead' ─┤──> understudy (status)
                                                       'the understudy goes on' ─────────┤
                                                       'the leading player leaves the company', 'the director calls again',
                                                       'a screen test', 'the part of a lifetime is cast', 'two actors, one part'
                                                                                         ▼
  'a voice for the cartoon' ──> voice actor ── 'the lead voice in a series' ──> lead actor or actress (facet)
                                                                                         │ 'the show is a hit'
                                                                                         ▼
                                                              [known across the country] ──> [a household name]
 side roads: 'the stage management team is a person short' -> stage manager; 'a director is needed for the autumn play'
   -> community theatre director or director -> 'the theatre needs an artistic director' -> artistic director (facet);
   'the script competition' -> playwright or screenwriter
 exits: 'leaving acting for another life' -> drama teacher, casting director, talent agent, producer, stage manager, or
   a base career; perks stay
 round 5: 'the city wants the town's show' -> stage manager, director or producer (from the society or a company of
   one's own); 'the school needs someone to take drama' -> drama teacher (from teacher); the long shots, each from the
   rung below: stage-longshots.lib and 'Steps and long shots' below
 falls: 'the second job does not come', 'two actors, one part' lost, 'the reviews are in', 'the producers want a star
   for the transfer', 'burnout' (base); tribal 'the mimic who mocks the chief', 'the spirits ride the dancer'
```

## The lead on every road (Emren's ask)

A lead is a part, not a job. The professional lead is the facet [lead actor or actress], held on top of [professional
actor] or [voice actor] for a run or a series; the amateur, child and one-person-show lead is the standing perk [a lead
role to remember], which stays with a person for life ("once played the lead, and people still talk about it"). Every
road the pack opens reaches one of them, and most reach both:

| Road | How the lead is reached | Moments |
| --- | --- | --- |
| Amateur | the lead in the local players' show, at any age; a film that casts an amateur of five years with a lead behind them (the one-rung skip) | 'the local players need a cast', 'casting night at the local players' ([a lead role to remember]); 'the part of a lifetime is cast' ([lead actor or actress] with [professional actor], at a lower chance without a listing) |
| Youth and school | the school lead, the youth theatre's summer lead, a child's lead in a professional show (licence, chaperone, school hours) | 'auditions for the school production', 'the summer show casts its lead', 'a casting call for children' |
| Fringe and one-person shows | the person who wrote it plays it; a transfer brings the professional lead | 'the show you wrote to star in', 'opening night at the fringe' |
| Stage | the understudy who goes on, the company actor who steps up, the director who calls again, the part won from a rival | 'cast as understudy to the lead', 'the understudy goes on', 'the leading player leaves the company', 'the director calls again', 'two actors, one part', 'the part that came with the letter' |
| Screen | the screen test, the great part, the extra who is given a line | 'extras wanted for a film in town', 'you, say this line', 'a screen test', 'the part of a lifetime is cast' |
| Voice | the lead voice of a series (the facet sits on [voice actor]) | 'a voice for the cartoon', 'the lead voice in a series' |
| Late life | the retiree who joins the local players and leads at seventy; a film that wants an old face | 'never too late for the stage', 'casting night at the local players', 'the part of a lifetime is cast' (elders included) |
| Tribal world | the teller-player who wears the great mask of the first ancestor at the summer gathering | 'the old teller dies at midwinter', 'chosen to wear the great mask' |
| Magic world | the leading player of a company; a lead with an illusionist's glamour, or on the night the dead watch | 'the illusionist players come to town', 'the mask that changes its wearer', 'a glamour that makes the play real', 'the theatre where the dead come to watch' |

Each color has its own road to the lead, and its own way of holding it (the facet's profiles: R raw presence, U B the
built career, W G the company's first servant):

- **White**: the company actor and the understudy: word-perfect, there every night, ready when the lead falls ill
  ('the understudy goes on', 'the leading player leaves the company').
- **Blue**: the craft actor: youth theatre, drama school, the showcase, a director who keeps casting them ('the
  director calls again').
- **Black**: the networker: the agent, the producer and the part taken from a rival ('two actors, one part', 'the show
  is a hit').
- **Red**: raw talent: the open call after years with the local players or as an extra, without drama school, the fringe and the one-person show ('the show you wrote to star
  in', 'opening night at the fringe').
- **Green**: the rooted player: the regional company, the local players, the folk play at midwinter, and the late
  bloomer who leads at seventy ('casting night at the local players', 'never too late for the stage').

Each lead moment balances its chances across the five colors, so no color wins parts more easily (MOMENTS-BRIEF.md,
"Pack rules").

## Steps and long shots (Emren 09:18 and 12:18; round 5)

The steps rule: every career and summit grows from the rung below it. A moment option that gives a career or a summit
holds or requires the rung below (`holds:` with `tenure:`, `requires:` with `without: impossible`, or a LIFE gate with
yrs_has in engine-conditions.py), and a rule in roles.py names only titles in its `rungs=` (or the title it refines),
so the engine's "from nothing" check can verify it. A step takes a year or more on the rung below (two for a summit,
three for the directors). A perk alone (acting, a lead role to remember, writing stories, a fringe slot) never stands
in for a rung. The entry and community titles stay open to anyone: [youth theatre member], [amateur actor],
[background artist], [community theatre director], and the statuses [drama school student] and [understudy].

| Title | Rungs below (roles.py `rungs=`, round 5) |
| --- | --- |
| professional actor | drama school student, understudy, amateur actor, background artist |
| voice actor | professional actor, amateur actor, community-radio presenter |
| lead actor or actress (facet) | professional actor or voice actor (refines); understudy; amateur actor (five years with a lead behind them, the one-rung skip) |
| director | community theatre director, stage manager, professional actor |
| artistic director (facet) | director (refines); community theatre director (many years, the one-rung skip) |
| playwright or screenwriter | novelist, journalist, professional actor, drama school student, amateur actor, community theatre director |
| producer | stage manager, director, community theatre director, a company of your own |
| stage manager | stage technician, drama school student, amateur actor, community theatre director, professional actor, voice actor |
| casting director | professional actor, talent agent, stage manager, producer, director, voice actor |
| talent agent | professional actor, casting director, producer, voice actor |
| drama teacher | drama school student, professional actor, teacher, amateur actor, community theatre director, voice actor |

The long-shot rule (LONGSHOTS-BRIEF.md): a long shot is a bold try at the next rung, or a skip of at most one rung by
someone with years on the rung below, at a written chance of 1 to 5 (the long odds come from the step itself, never
from `lacking:`), and every long-shot option carries `grants_if_fails: a long shot that missed`. The perk anchors the
two echoes, 'the same door, years later' (`title: {missed}` at 4) and 'the long shot becomes a story to tell'.

| Title | Moment and option (chance) | Rung needed |
| --- | --- | --- |
| professional actor | 'an open audition in the city', every single (4 to 5) | amateur actor, extra or drama student of two years |
| | 'filmed by chance in the street', W B R G (3) | amateur actor or extra of three years |
| | 'the late starter', every single (3) | amateur actor or extra of two years, 35 or older, never paid |
| | tribal 'the old teller dies at midwinter', every single (5) | amateur actor or drama student of two years |
| | magic 'the illusionist players come to town', every single (5) | amateur actor of a year |
| voice actor | 'a voice for the cartoon', every single (3) | professional actor of a year, or amateur or radio voice of two with accents and voices |
| | 'filmed by chance in the street', U (3) | amateur actor of three years |
| lead actor or actress | 'the lead from the open queue', every single (2) | professional or voice actor, understudy; or amateur of five years with a lead behind them |
| | 'the night both covers are off', every single (3) | professional actor (understudies hold it) |
| | 'the other side of the table', R (3) | professional actor of three years |
| director | 'the other side of the table', U (3) | professional actor of three years |
| artistic director | 'the old theatre needs someone to save it', W U R G (2) | director of three years, or community theatre director of eight |
| playwright or screenwriter | 'the film you made with friends', every single (2) | four years writing, with a novelist's, journalist's or stage rung behind |
| producer | 'the old theatre needs someone to save it', B (2) | director of three years, or community theatre director of eight |
| stage manager | 'the stage management team is a person short', every single (3) | technician or drama student of a year, or amateur or community director of two |
| casting director | 'the other side of the table', W (3) | professional actor of three years |
| talent agent | 'the other side of the table', B (3) | professional actor of three years |
| drama teacher | 'the other side of the table', G (3) | professional actor of three years |

Every other title option in the pack is a step at real odds (6 and up), such as 'the part of a lifetime is cast', 'a
screen test', 'the script competition', 'opening night at the fringe' and 'the part that came with the letter'.

## Road per color (round 5, checklist P12)

Each road leans to one lead color, chosen from the catalogue's first ways and single-color profiles, and the five
roads cover the five colors. The lean comes from which options carry a road's `title:` (one per color in 'leaving
acting for another life', 'the city wants the town's show' and 'the other side of the table') and from
`weight="colors"` on its rule, which leans each title to its own single-color profile; no option of one color was
added. The single-title steps (the lead's crossings, the open audition, the cartoon) keep their title on every color,
so the lead stays reachable on every road.

| Lead color | Road | Titles (first ways) | Where the road's own color carries the title |
| --- | --- | --- | --- |
| Red | acting and the lead | professional actor (R B), lead actor or actress (R) | the lead on every color at its crossings; Red's single in 'the other side of the table' |
| Blue | writing, directing, voice and teaching | playwright or screenwriter (U R), director (U W), voice actor (U), drama teacher (U) | Blue's director in 'the city wants the town's show' and 'the other side of the table'; Blue's drama teacher in 'leaving acting for another life' and 'the school needs someone to take drama' |
| White | stage management, casting and running a theatre | stage manager (W U), casting director (W), artistic director (W B) | White's casting director in 'leaving acting for another life' and 'the other side of the table'; White's stage manager in 'the city wants the town's show' |
| Black | producing and agents | producer (B), talent agent (B) | Black's agent in 'leaving acting for another life' and 'the other side of the table'; Black's producer in 'the city wants the town's show' and 'the old theatre needs someone to save it' |
| Green | community theatre and the extras | amateur actor (R G), community theatre director (G W), background artist (G), youth theatre member (R G), a lead role to remember | Green's community directorship in 'the school needs someone to take drama'; Green's home show in 'the city wants the town's show' |

## Real numbers

| Figure | Value | Source |
| --- | --- | --- |
| Actors employed (US) | 62,560 at a time; median pay 20.50 dollars an hour | US Bureau of Labor Statistics, May 2023 (27-2011) |
| Producers and directors (US) | 154,470 | BLS, May 2023 (27-2012) |
| Agents and business managers of artists, performers and athletes (US) | 12,870 | BLS, May 2023 (13-1011) |
| UK actors' union | 48,606 members (2024) | Equity, via Wikipedia |
| UK actors' earnings and day jobs | 48 in 100 earned under 6,000 pounds a year from performing; 6 in 100 earned 30,000 or more; 71 in 100 spent 28 weeks or more of the year outside the industry | Equity members' survey, via netribution.co.uk |
| US screen actors' union | about 160,000 members; about 87 in 100 earn under the 26,470-dollar health-plan threshold from acting | SAG-AFTRA, via CBS News (2023) and Roosevelt House |
| US stage actors' union | 51,938 members in 2018-19, 19,369 of them worked (37 in 100); 2,259 new members; stage managers worked 55,423 work weeks (about 1,066 in an average week) | Actors' Equity Association annual report 2018-19 |
| UK drama schools | about 12,000 applicants for about 1,550 places a year at 22 accredited schools; about 700 to 1,000 acting graduates a year | actingcoachscotland.co.uk; shootingpeople.org |
| UK amateur theatre | 437,800 taking part (29 in 100 under 21), 25,760 performances, 2,300 to 2,500 societies (2002); about 500 groups compete in about 100 drama festivals; the Little Theatre Guild has over 100 theatres | NODA survey, via Wikipedia "Amateur theatre"; artshub.co.uk |
| US community theatres | about 7,000 (923 AACT members in 2009) | AACT; ticketpeak |
| Youth theatres (England) | over 100,000 young people in 414 youth theatres | NAYT Youth Theatre Census 2024 |
| Stage school pupils | about 60,000 a week in one chain | Stagecoach |
| Directors, writers, casting | Directors Guild of America 19,673 members (2026); US stage directors' society 2,643 (2013); WGA West about 14,000 (2026); Writers' Guild of Great Britain 3,074 (2024); Casting Society nearly 1,200 | Wikipedia; Backstage |
| Drama teachers (English secondary schools) | 8,963 (2019 headcount), 11,100 in 2010 | Cultural Learning Alliance |
| Background actors (US) | about 200,000 registered | Central Casting |
| Child performance licences (England) | over 90,000 a year (2013, an estimate from a third of local authorities) | "That's Entertainment", University of the West of Scotland, 2014 |
| Child licence rules (UK) | a licensed chaperone; three hours of education on a school day missed; at most six days in a row; twelve hours off overnight | gov.uk, departmental advice on child performance licensing |
| US nonprofit theatre | 1,953 theatres, 21,000 productions, 180,000 performances, 38 million attendances | TCG Theatre Facts 2019, americantheatre.org |
| Scripted US series | 600 in 2022, 516 in 2023 | FX research, via Variety |
| Largest fringe festival | over 3,300 to 3,500 shows in 2024 | edfringe.com; Express and Star |
| Births | about 680,000 a year (UK), about 3.6 million (US) | ONS; CDC |

The catalogue's `share` fields carry these per title, with their sources in comments; everything else is marked as an
estimate there. The moments never name a real person, production, theatre, studio, film, award, agency or union: their
`times:` lines cite sources in plain words ("the UK actors' union's survey").

## Earned odds (Emren, 21:03: real odds are the floor; preparation and timing lift them)

(Round 5 note: these tables are the first design's; the written chances have moved since, in "Calibration" below
and in "Steps and long shots" above, and the engine's tier fit now sets the lifts.)

Per step, for a person who takes the step, by the rule in ../PROPOSAL.md ("Earned odds") as the engine built it: up to
+1.0 logit for full preparation (the share of the title's HELPS list held), up to +0.4 for a favourable window
(WINDOWS), never above 90%. Emren's lead gets half lifts (LIFT_STAGE), as Politics' party leader does, so a lead stays
a long shot that preparation only softens; the paths to it (drama school, the agent, the understudy's cover, the
voice job) get full lifts.

| Step (moment) | Real | Well prepared (+0.75) | Fully prepared (+1.0) | Prepared and timely (+1.4) |
| --- | --- | --- | --- | --- |
| a drama school place (`drama school auditions`) | 13% | 24% | 29% | 38% |
| paid work from an open call without drama school, after two years as an amateur or an extra (`an open audition in the city`; round 5: 4 to 5) | 5% | 10% | 13% | 18% |
| an agent and first work at the showcase (`the showcase for agents`) | 45% | 63% | 69% | 77% |
| an agent after a fringe run (`opening night at the fringe`) | 12% | 22% | 27% | 36% |
| cast as understudy (`cast as understudy to the lead`) | 30% | 48% | 54% | 63% |
| a first voice job (`a voice for the cartoon`) | 25% | 41% | 48% | 57% |
| a stage management post (`the stage management team is a person short`) | 50% | 68% | 73% | 80% |
| directing the local players (`a director is needed for the autumn play`) | 60% | 76% | 80% | 86% |
| directing a paid production (the same moment) | 30% | 48% | 54% | 63% |
| a script competition won (`the script competition`) | 8% | 16% | 19% | 26% |
| an artistic directorship (`the theatre needs an artistic director`) | 15% | 27% | 32% | 42% |

The lead, at half lifts (+0.375, +0.5, +0.7):

| Step (moment) | Real | Well prepared | Fully prepared | Prepared and timely |
| --- | --- | --- | --- | --- |
| the understudy kept on as the lead (`the understudy goes on`) | 20% | 27% | 29% | 33% |
| the company actor steps up (`the leading player leaves the company`) | 25% | 33% | 35% | 40% |
| the director calls again with the lead (`the director calls again`) | 30% | 38% | 41% | 46% |
| a screen test that becomes the lead (`a screen test`) | 10% | 14% | 15% | 18% |
| a fringe show that transfers with its lead (`opening night at the fringe`) | 10% | 14% | 15% | 18% |
| the lead voice in a series (`the lead voice in a series`) | 12% | 17% | 18% | 22% |
| the part of a lifetime (`the part of a lifetime is cast`) | 6% | 8% | 10% | 11% |
| the amateur lead (`casting night at the local players`), no lift today (an ask) | 30% | 30% | 30% | 30% |

Over a life that pushes at every step (two tries at drama school and the showcase if in; two open calls and a fringe
run either way; then, as a professional, two screen tests, a cover that goes on, a leading player who leaves and the
part of a lifetime once; two tries at a first voice job and two at a lead voice; two hits after the lead; three casting
nights at the local players):

| Reaches | Real | Well prepared | Fully prepared | Prepared and timely |
| --- | --- | --- | --- | --- |
| a drama school place | 24% | 42% | 49% | 61% |
| paid work as an actor | 31% | 56% | 65% | 78% |
| a lead, once professional | 46% | 60% | 65% | 72% |
| a professional lead, from the start | 23% | 43% | 51% | 65% |
| a lead voice | 1 in 10 | 20% | 24% | 31% |
| known across the country | 1 in 31 | 13% | 20% | 33% |
| the amateur lead, today (no lift) | 66% | 66% | 66% | 66% |
| the amateur lead, if the engine reads HELPS for it (engine need 6) | 66% | 86% | 90% | 95% |

These are for players who aim and push; ordinary lives seldom meet these moments or prepare for them, so simulated
shares stay near the catalogue's (a professional lead about 1 life in 1,000, a professional actor 4 in 1,000, an
amateur lead about 4 in 100). The engine sets and tests the sizes.

## Life arcs as routes

| Arc | Route in the pack |
| --- | --- |
| The company player (W) | [professional actor], 'cast as understudy to the lead', [understudy], 'the understudy goes on', [lead actor or actress]; [a director who keeps casting you] |
| The craft actor (U) | [youth theatre member], 'drama school auditions', [drama school student], 'the showcase for agents', [professional actor], 'the director calls again', the lead |
| The networker (B) | [an agent who believes in you], [a producer who backs you], 'two actors, one part', the lead taken from a rival, 'the show is a hit', [known across the country] |
| The raw talent (R) | 'an open audition in the city' after two years with the local players or as an extra, without drama school, or 'the show you wrote to star in', [a fringe slot], 'opening night at the fringe', the lead in a transfer |
| The rooted player (G) | 'the local players need a cast', [amateur actor], 'casting night at the local players', [a lead role to remember], [community theatre director]; or the regional company and 'the leading player leaves the company' |
| The late bloomer | 'the first months of retirement', 'never too late for the stage', [amateur actor] or [background artist], the lead at seventy at 'casting night at the local players'; 'the part of a lifetime is cast' for an elder |
| The child performer | 'a flyer for the youth theatre', [youth theatre member], 'the summer show casts its lead', 'a casting call for children' with [child performance licence] (a parent, a chaperone, school hours), then drama school |
| The voice | [accents and voices], 'a voice for the cartoon', [voice actor], 'the lead voice in a series', [repeat fees] |
| The extra who got a line | 'extras wanted for a film in town', [background artist], 'you, say this line', 'a screen test', [professional actor] |
| The theatre-maker | [stage manager] or [community theatre director], 'a director is needed for the autumn play', [director], 'the theatre needs an artistic director', [artistic director] |
| The writer | [writing stories], 'the script competition', [playwright or screenwriter], 'the producers want a different ending' |
| The one who left | 'leaving acting for another life', [drama teacher], [casting director], [talent agent], [producer] or a base career; the perks stay |

## Hooks into the base world

The pack never edits base moments. It opens from a life's history through four echoes: 'the part you never got to
play' follows the base 'the school play' (a child under 13); 'never too late for the stage' follows 'the first months
of retirement'; 'the show you wrote to star in' follows 'inspiration strikes' or 'wanting to be noticed' in someone who
can act; 'the part that came with the letter' follows 'an unexpected chance: a grant, a role, a stage' in someone who
can act. The background rules read 'the school play' too ([acting], [youth theatre member], [a lead role to
remember]). Base titles and perks it builds on: [stage technician], [teacher], [novelist], [journalist],
[community-radio presenter], [festival organiser], [stagecraft], [singing], [dancing], [writing stories], [following
online], [public speaking], [name on the local scene], [good name in town], [cleared to work with children],
[teaching], [graduate], [professional registration], [mentor], [patron], [contact in the trade], [striking a deal],
[selling], [organising people], [savings], [scholarship], [second language], [boxing or martial arts], [reliable
record], [grandparent], and the base studio of one's own. EXTEND_STAGE widens five rules the pack does not own: the
core [known across the country] (a lead with a known face, an award or repeat fees), the base [stagecraft] (stage
managers, community theatre directors), [name on the local scene] (the amateur lead, the local director), [cleared to
work with children] (drama teachers and community theatre directors, with the base rule's record check) and the
studio of one's own (a voice actor's booth at home).

## Boundaries with other packs

- **Music and Performance** (a later pack) owns singers, musicians, dancers and comedians as careers, concerts, bands
  and stand-up. [singing] and [dancing] stay base skills that this pack counts as preparation (a musical's lead is an
  actor here); [improvisation] here is the actor's skill, and stand-up is theirs.
- **Art and Writing** (a later pack) owns novels, poetry and visual art. [novelist] and [writing stories] stay base;
  scripts are here ([writing scripts], [playwright or screenwriter]), and a novelist reaches the stage through 'the
  script competition'.
- **Media** owns journalists, critics, broadcasters, presenters and online creators; [following online] stays theirs.
  The notices are a read event here ('the reviews are in'); the critic who writes them is Media's.
- **Education** owns schools and universities as institutions: [drama school student] stands in for drama training
  until Education exists, and [teacher] stays base, with [drama teacher] here.
- **Business** owns theatres and studios as firms; [producer] here is the show's producer and [a company of your own]
  a small company, not a firm of shareholders.
- Technical theatre: [stage technician] and [sound engineer] stay base; stage management is here. Politics and Science
  share only the reach ladder.

## What the engine needs for this pack

1. `load_batch("earth", packs=["science", "politics", "stage"])`: the catalogue, rules and moments on top of
   the base, and the second ROLE_NORM refit Emren's single go-live needs (../calibration.md).
2. Facets: [lead actor or actress] refines two titles ("professional actor; voice actor", the same set in the catalogue
   and the rules) and [artistic director] refines [director]. Both are already supported (a facet on several titles,
   professor in Science).
3. A facet given before its title: options for someone without an actor's title carry `title: lead actor or actress;
   professional actor`, the lead first (the engine reads the first title for the earned odds, and holds the facet in
   f_pend until the title comes). When both come at once, the lead's season replaces the actor's (sea_open: a new one
   replaces one still running), as intended.
4. Statuses that last: [drama school student] 3 years (ending in [drama school diploma] by its rule), [understudy] one
   run; [child performance licence] retires at 16.
5. EXTEND_STAGE (roles.py): five strings or-ed into rules the pack does not own (above).
6. **Built by the engine (03:11): earned odds for a perk act** (batch.py reads HELPS_PERK_<PACK>; LIFT_<PACK> may name a perk).
   The ask was: The amateur, child and one-person-show lead is `grants: a lead role to
   remember`, with no title:, so today it gets no lift. Emren wants the lead reachable with earned odds on every road;
   the pack asks the engine to read helps for an act that grants a standing perk as it does for title:, from a list such
   as HELPS_PERK_STAGE in helps.py (HELPS keys must be titles today, so it is a separate name the engine does not read).
7. LIFT_STAGE in helps.py: half lifts on [lead actor or actress].
8. PACK_RULES["stage"]: ECHO_STAGE (four echoes) and ECHO_STAGE_LONGSHOTS (two), READ_STAGE ('the reviews are in'),
   and LIFE_STAGE (twelve life events) and LIFE_STAGE_LONGSHOTS (seven long shots): who each moment that gives a career
   or a summit can come to, the rung below (Emren 09:18), from engine-conditions.py (round 5 adds the gates of 'the
   school needs someone to take drama', 'the other side of the table', 'filmed by chance in the street' and 'the film
   you made with friends').
9. Threshold seasons on `threshold: title:<name>` for [drama school student] (a status), [professional actor], [lead
   actor or actress] (a facet) and [director]: sea_open runs for any title gained, so a status and a facet open their
   seasons like a career.
10. `share:` on a holds: moment as the share of all people (engine 01:45): the brief's pair C ('drama school
   auditions', 'an open audition in the city') carries share .12 of all lives (.03 before the calibration), drawn
   among holders of [youth theatre member], [amateur actor], [a lead role to remember] or [acting] for drama school,
   and among amateur actors, extras and drama students of two years or more for the open audition (`tenure: 2-100`).
11. Worlds: worlds.py gives every form; the planned moments carry `earth:`, `tribal:` and `magic:` lines, and eight carry
   `only: tribal` or `only: magic`.

## Asks for the Library

1. Profiles on the base [teacher] (ways W U, none yet), so a teacher's move into [drama teacher] reads the right way:
   ("R G", "Runs the school play and the trips, and the children remember them for life") and ("B", "Wants results,
   the inspection and the head's job").
2. A content review of the child moments (1, 2, 25, 26, 54, 55) against the pack's safe-forms rule: a parent or carer
   who agrees, a licence, a chaperone, school hours kept, never alone with an adult in the story.
3. The build.py fields the moments use are already accepted (threshold:, step:, transform:, aims:, share:, lacking:,
   the *_if_fails acts); a look at the value tags check.py questions, as for the other packs.

## Other worlds

The catalogue stays in modern Earth terms; worlds.py maps every pack title and perk, the base titles and perks the
pathway uses, and the reach ladder, so the pathway keeps one shape in every world: the same rungs, doors, crossings,
falls and a lead on every road.

| Earth | Tribal (clans, hunts, elders, before cities) | Magic (towers, guilds, Orders, old powers) |
| --- | --- | --- |
| youth theatre, school play | the children who play the small spirits in the tellings | the players' guild's children's company |
| amateur actor, community theatre director | a player in the band's own tellings; the shaper of the midwinter telling | the guild's mystery players; the master of pageants |
| drama school student | an apprentice to an old teller for three winters | a scholar of the players' guild school |
| professional actor, understudy | a teller-player kept by the band through the winter; the one who learns the great mask's telling | a player in a licensed or travelling company; a second to the leading player |
| lead actor or actress | the one who wears the great mask of the first ancestor | the leading player, whose name the herald cries |
| screen, extras | the shadow wall; the herd and the war band in a great telling | the illusionists' glamours and the mirror-plays; walk-ons in the procession |
| voice actor | a hidden voice behind the hide screen | a voice for the speaking-stones and the puppet theatres |
| director, artistic director | the shaper of a telling; the keeper of the gathering's tellings | master of the play; master of a royal or guild playhouse |
| agent, producer, union card | a go-between; the one who gathers the hides and the feast; a place among the tellers | a players' broker; a play-merchant; the guild token |

Where a role cannot exist, worlds.py names the nearest stand-in (screen acting is playing for the shadow wall or the
glamour; a showreel is a telling the bands ask for again, or a crystal of scenes; a union card is a place among the
band's tellers). World-only doors, crossings and falls, each optional, each with a price, none forced:

- tribal: 'the old teller dies at midwinter' (door), 'chosen to wear the great mask' (crossing to the lead), 'the
  mimic who mocks the chief' (fall), 'the spirits ride the dancer' (fall);
- magic: 'the illusionist players come to town' (door), 'the mask that changes its wearer' (door), 'a glamour that
  makes the play real' (crossing to the lead), 'the theatre where the dead come to watch' (crossing to the lead).

Each world's set uses both halves of its combination lines, so the pack stays color-even in every world. Modern Earth
has no magic and no supernatural moments.

## Departures, and the concept decisions changed

- **17 titles, not about 18**: the lead's list plus [producer] (the Black road's money and the transfer, and an exit
  for actors) and [artistic director] (the director's summit, a facet on [director]). [voice actor] is a career of its
  own, so the voice road has a lead.
- **The lead is a facet on two titles**: [lead actor or actress] refines [professional actor] and [voice actor], so the
  voice road reaches a lead too; it lasts a run or a series (lose after a year at rate .4).
- **[drama teacher] is its own career with no `after: teacher`**: `after` would give it only to teachers and end the
  teacher title; its req lets a teacher with [acting] move into it (the engine's job move) and also an actor who
  teaches.
- **No child career title**: a child performs through [youth theatre member], [a lead role to remember] and [child
  performance licence], always with a parent's consent, a chaperone and school hours (UK licensing rules).
- **The amateur lead is a standing perk, [a lead role to remember] (ways R G)**, which every road can reach, including
  the late bloomer at seventy; its earned odds are an ask (engine need 6).
- **Door rates follow the calibration**, not .0005 to .003: everyday doors carry share, rate .025 to .05 and gap, the
  same on both halves (../calibration.md, "The share lines"); pair C's share is of all lives, by the engine's 01:45
  change.
- **Perk names carry no apostrophes** ("union card", "a company of your own"), so the checker's quote matching works.
- **[an award for acting] includes the amateur drama festivals' best-actor awards** (share .002), so the rooted
  player's road can win one too.
- **READ_STAGE** sits next to ECHO_STAGE in engine-conditions.py, since 'the reviews are in' is a read event and needs a
  condition too.
- **Perks carry ways** (colors), balanced over the five colors, as in the Science and Politics packs.
- **No real names on the page**: real unions, schools and festivals appear only as sources in comments and in this
  file's table of real numbers.

## Calibration (2026-10-06)

Emren's targets moved during the day: "About 10x" (05:20); then many lives should see a door and fewer take it (07:14:
limit titles through success odds and steps, not by hiding the door); then one budget for all packs, which the engine
fits itself (08:11, engine 08:21). TARGET_STAGE in roles.py gives each title its tier (career, summit or community)
and each perk a multiple, and the engine fits one lift per tier. The pack's own part is the shape: every title
reachable, every lead road open, the titles of a tier at similar multiples of their real shares, believable steps.
What changed, from runs on the next2 batch with Science and Politics:

- The doors reach more lives: pair A (youth theatre, school production) share .45, rate .03; pair B (the local
  players, extras) share .15, rate .025; pair C (drama school, the open audition) share .12, rate .05.
- Written chances carry the limits: [voice actor] and [stage manager] at 5 at their side doors (round 5: 3, as long
  shots); the community
  directorship at 10 to 20; the showcase at 30; the open audition at 4 to 6 (round 5: 4 to 5); the lead at 16 to 18 among the last two,
  12 when the director calls again, 9 to 10 when the leading player leaves; [artistic director] at 8 to 11; the
  extras' parts at 15 to 50; in the tribal and magic worlds the teller's place and the illusionists' wagons at 5 and
  the great mask at 15.
- One more step where a summit was one click away: the screen test goes to a working actor, and 'a director is
  needed for the autumn play' comes after three years with the society or its school (`tenure: 3-100`).
- The rung below (Emren 09:18): every route to a career or a summit starts from the rung below it, or skips one rung
  after years on the rung below; a perk alone (acting, a lead role to remember, writing stories, a fringe slot)
  never stands in for a rung, and a step takes a year or more on the rung below (two for a summit, three for the
  directors; engine 10:38). The moments' holds: name the rungs, and `tenure:` or LIFE_STAGE in engine-conditions.py
  adds the years; the rules in roles.py name the same rungs. The lead comes from a working actor (professional, voice,
  understudy), or from an amateur of five years with a lead behind them; the fringe, the letter and the
  illusionists give the first paid part, never the lead; the professional company's director is the society's
  director; an actor's savings buy a company of one's own, the step before [producer].
- The illusionist players come at half the rate (per_year .005): in the magic world they reached more than half of all
  lives. The cartoon comes four times as often (per_year .04; round 5: .03) to the fewer who now meet it (the rung below voice
  work). No other per_year changed.
- Rules: background rates raised where a title had no road but its rule (director .05, producer .05, talent agent
  .012, drama teacher .02, playwright or screenwriter .015, artistic director .02, casting director .01) and for
  the perks those careers need (round 5 lowered most of these again, title by title: "Rounds" above); professional actors leave faster (lrate .15: most actors leave the profession within
  ten years); [writing scripts] also comes to an improviser who acts, and [a showreel] to an actor with a casting
  directory listing.
- Realized success at the crossings still runs above the written chance (the engine's own measure); the engine's tier
  lift and its second fit take it from here.
