# Pack: Science, Research and Discovery (modern Earth)

Status: live since 2026-10-06 19:37 Emren's time (16:37 UTC), with Politics and Stage and Screen in one go-live
(batch.PACKS science, politics, stage). Round 5 (2026-10-07) works the release checklist
(chroma-release/checklist.md, rows P1 to P16); its changes are listed below and in the dated "Round 5, 2026-10-07"
comments in every file. Source: Emren's "Science, Research & Discovery: expanded design v2" (emren-science-v2.md in this
folder). Plan for every pack: ../PROPOSAL.md. Hand-offs to the engine: ../for-the-engine.md.

## Rounds

| Round | When (Emren's time) | What changed |
| --- | --- | --- |
| 1 | 10-06, about 01:40 | Calibrated to real shares on 2,400 lives (../calibration.md, ../calibration-changes.txt). |
| 2 | 10-06 morning, to 13:44 | TARGET_SCIENCE in roles.py puts each title in Emren's budget (careers, summits, community; the engine's tier lift and ROLE_NORM fit set the level). Doors are met widely and the odds and steps hold the titles back (Emren 07:14). Every career and summit grows from the rung below it, with years on that rung (Emren 09:18): `after=` and `rungs=` in roles.py. Long shots merged early afternoon (science-longshots.lib, engine-conditions.py; ../LONGSHOTS-BRIEF.md). |
| 3 | 10-06, about 12:00 to 15:14 | The research road into Politics' [policy analyst] moved into EXTEND_SCIENCE (the Politics rule names only its own and base titles); the engine's three-pack fit set one budget for all packs: about 1 life in 3 a pack career and 1 in 20 a summit. |
| go-live | 10-06 19:37 | All three packs live. |
| 5 | 10-07 | Release checklist: the facility lead, the postdoc and the independent investigator made reachable, the communicator and other overfed careers lowered, a long shot for every career and summit, the crossings' per_year back to their times lines, a road per color, value tags corrected, these docs (details below). |

## Files

| File | What it holds |
| --- | --- |
| catalogue.py | 16 titles (11 careers, 3 community, 2 colorless facets) and 28 perks, base catalogue format |
| roles.py | how each title and perk is gained and lost (ROLES_SCIENCE, ROLES_REACH), the routes or-ed into base and Politics rules (EXTEND_SCIENCE), and each title's place in the budget (TARGET_SCIENCE) |
| helps.py | earned odds: what prepares a person for each title (HELPS) and the context that opens each window (WINDOWS) |
| engine-conditions.py | the long shots' LIFE gates (LIFE_SCIENCE_LONGSHOTS) and the two echoes anchored on [a long shot that missed] (ECHO_SCIENCE_LONGSHOTS), in the shape of earth_rules.PACK_RULES["science"] |
| ../core/reach.py | the reach ladder shared by every pathway pack: [known across the country], [a household name] |
| ../core/longshot.py | the shared perk [a long shot that missed] |
| science-doors.lib | doors into the pathway and two echoes that open it from a life's history (moments 1 to 6) |
| science-rungs.lib | life on the six main rungs, an everyday pair each (7 to 18) |
| science-roads.lib | life on the side roads and community roles (19 to 34) |
| science-events.lib | crossings between rungs, the life of a project, falls and reach (35 to 51) |
| science-seasons.lib | threshold seasons for four big rungs, four moments each (52 to 67) |
| science-longshots.lib | nine long shots, one or more for every career and summit, and the two echoes of the anti-story |
| MOMENTS-BRIEF.md | the brief the moments were written to |
| checks_science.md | the Library's check.py on the compiled pack (round 5 build) |
| tests/ | t_pack_after_doors.out, the engine's first test of the pack (10-05) |

In all: 78 moments (32 everyday, 25 life events of which 9 are long shots, 16 season moments, 4 echoes, 1 read event)
and 770 options. Build: `build.py <pack folder>/science --out <out>` compiles the six .lib files into science.py.

## The rules the pack follows

- **Steps (Emren 09:18, "never from nothing").** Every career and summit grows from the rung below it. In roles.py each
  career and summit rule names in its `req` only titles in its `after=` (the rungs the step leaves) or `rungs=` (rungs
  kept, such as a degree), or the title it refines, so the engine's "from nothing" check can verify it. In the moments,
  an option that gives a career or summit holds the rung below (`holds:`), requires it (`requires:` with `without:
  impossible`), or sits in a long shot whose LIFE gate asks for years on it (`yrs_has`). Entry titles and the community
  titles (citizen scientist, community observer, volunteer research organiser) stay open to anyone: that is where the
  many starts live.
- **Long shots (../LONGSHOTS-BRIEF.md).** A bold try at the next rung, or a skip of one rung, by someone with years on
  the rung below; written chance 1 to 5 (the long odds come from the skip or the outside post, never from a stranger let
  in); every long-shot option carries `grants_if_fails: a long shot that missed`. Each long shot is a life event, even
  on its own: five one-color singles at one chance (each color's own way of trying) and a pair set of the ordinary next
  steps. A missed try can come back as 'the old door opens a crack' (the same title at 7) and, years later, as 'the story
  of the long shot'.
- **Shown, not given (Emren 07:14).** Doors are met widely and their acts carry real odds (8 to 12 on an everyday door,
  a few in 100 on a long shot); the engine lifts the acts of a career under its target within its cap and lowers them
  above it. An everyday moment comes several times in a life, so an everyday act that gives a career or summit is
  open only to those already near that rung (`requires:` with `without: impossible`), and never goes under 8: the
  engine counts a missed title under 1 in 10 as a long shot.
- **Rates.** A background rule's `rate` is a yearly rate among those who meet its `req`; a life event's `per_year` is
  the real yearly rate in its `times:` line, per holder; everyday doors carry `share:`, a small `rate:` and `gap:`.

## Long shots: every career and summit (round 5, P9)

| Title | Long shot (moment, option) | Rung needed | Chance |
| --- | --- | --- | --- |
| research assistant | 'the survey wants a paid assistant', the five singles | citizen scientist or community observer 4+ years | 4 |
| research scientist | 'a scientist's post at a famous lab', the five singles | research assistant, laboratory technician, research data steward or research software engineer 2+ years, and a degree | 4 |
| postdoctoral researcher | 'a named fellowship, one a year', the five singles | research scientist in the first five years, with [doctoral graduate] | 4 |
| research project lead | 'a national centre opens its posts', B single | research scientist 2+ years | 4 |
| research software engineer | 'a national centre opens its posts', U single (needs [writing code]) | research scientist 2+ years | 4 |
| evidence synthesis specialist | 'a national centre opens its posts', W single | research scientist 2+ years | 4 |
| participatory research coordinator | 'a national centre opens its posts', R single | research scientist 2+ years | 4 |
| research data steward | 'a national centre opens its posts', G single (needs [working with data]) | research scientist 2+ years | 4 |
| science communication specialist | 'a search for a new voice for science', the five singles | [explaining science] 3+ years, a degree, and a research post, journalism or teaching behind it | 5 |
| research group leader (summit) | 'a group of your own, open to all comers', the five singles | research scientist or postdoc 4+ years, with [research grant] (skips the project-lead rung) | 4 |
| research facility lead (summit) | 'a facility looks outside for its next head', the five singles (need [lab work]) | laboratory technician or research scientist 4+ years | 5 |
| independent investigator (summit) | 'a discovery nobody asked you for', the five singles (need [published research]) | research scientist 2+, research assistant 3+, or a volunteer of 5+ (organiser 3+) years | 4 |
| professor (summit) | 'a chair falls vacant at another university', the five singles (need [published research]) | research group leader 3+ years, or research scientist 8+ years (skips the project-lead rung) | 3 |
| any of these | 'the old door opens a crack' (second try), the five singles, `title: {missed}` | still on the rung below, 3 to 12 years after the miss | 7 |

## Roads per color (round 5, P12; Emren's card 10:47, "Road per color")

Each road leans to its lead color by which options carry its titles (`title:`) and by `weight="colors"` on its roles.py
rule (the title's profiles in catalogue.py); every color leads a road, and the pack as a whole stays even.

| Road | Titles | Lead color | Title acts by means color in the moments (share, round 5 build) |
| --- | --- | --- | --- |
| The lab researcher | research assistant, research scientist, research software engineer, professor (postdoc: a colorless facet, its acts W .70) | Blue | U leads each: .36, .45, 1.0, .52 |
| The research leader | research project lead, research group leader | Black | B leads each: .47, .30 |
| The communicator, the one who goes alone | science communication specialist, independent investigator | Red | R leads each: .69, .41 |
| The evidence and the shared record | evidence synthesis specialist, citizen scientist | White | W leads each: .29, .52 |
| The place, the facility and the long record | research facility lead, research data steward, participatory research coordinator, community observer, volunteer research organiser | Green | G leads: FL .36, RDS 1.0, PRC .88, CO .39; VRO .50 tied with B on its one act, its rule now weight="colors" on its profiles (G the single one) |

## Checks (round 5 build, 2026-10-07)

- **Build.** 73 situations, 4 echoes, 1 read event, 770 options, no layout problems.
- **Colors per stage** (check.py section 1, checks_science.md): means and ends even in every stage (largest spread 0%);
  mean chance per means color within 1.3 points in every stage (lib_stats overall spread 1.3).
- **Value tags** (check.py section 4): 64% agreement with the engine's color map (490 of 770; it was 53%, 380 of 720,
  before round 5; base batch 56%). Where a two-value tag pointed off the option's colors and the act is mostly one of
  the two values, the tag now names that value (Library list, drafts/next3/p14-pack-values.md).
- **Pack check.** `tools/check_pack.py science`: all checks pass.
- **Setting.** `drafts/check_setting.py`: no year, real place, currency, brand, real event or real person in player
  text.
- **Smoke runs** (`tools/smoke.py`, 60 lives each, all three packs, the live tier lift; too few lives for the rare
  titles, so the pooled run decides). Seeds 11 and 12 before the last fixes, seed 12 again after them: research assistant
  .23, .23, .35 (target .10); research scientist .13, .15, .25 (.06); project lead .08, .08, .05 (.025); evidence
  synthesis specialist .03, .10, 0 (.0025); participatory research coordinator .05, .08, .017 (.0025); postdoc .03, 0,
  .017 (.03); facility lead 0, 0, .03 (.004, both grown from research scientist); the perk [a long shot that missed]
  .017, .10, .017. No Science career or summit gained from nothing in the last run.
- **Content limits.** No sexual violence, no harm to children, no killing, nothing graphic, no cruelty in the cost of a
  missed long shot.

## Round 5 changes, by checklist row

- **P1 facility lead.** The rule takes [lab work] or [instrument troubleshooting] after four years in post (rate .05, then .005 at the merge: 9.6x its target over 1,600 lives once [lab work] spread);
  technicians gain [lab work] at their bench (EXTEND). 'the facility needs a head' holds laboratory technician or research
  scientist from three years, its title acts need [lab work]; 'a facility looks outside for its next head' from four
  years, needing [lab work]; the software engineer's 'a paper that thanks everyone but your software' can make a tool a
  shared service (G>W, 10).
- **P2 postdoc.** EXTEND_SCIENCE route into [doctoral graduate] (a graduate research assistant of two years, or a
  scientist in the first three years; rate .2), TARGET 4 for the doctorate; the postdoc offered in 'the first week with
  your own bench' (W>U) and 'a named fellowship, one a year'.
- **P4 independent investigator.** Rule rate .004 with the lower rungs named; 'a fellowship of your own' gives the
  title on R, UB and UR (15).
- **P5 overfed careers.** Rates lowered: science communication .006, project lead .15, evidence synthesis .01,
  participatory research .02, research scientist .06, data steward .012, professor .06; the communicator's acts lowered
  (40 in 'leaving research for another life', 5 in 'a search for a new voice for science'). The yearly lift moves a
  rung's rate only between e^.5 and e^1, so these written rates, not the fit, set most of each career's level. After the
  first two smoke runs the volunteer organiser became a rung kept on the coordinator's step (`rungs=`, not `after=`:
  with every organiser stepping up in time, the coordinator came to about 25 times its target), and the everyday title
  acts in 'a careful result that says no' and 'the budget will not stretch to everything' were opened only to those near
  the rung (evidence specialist about 25 times its target).
- **P7.** 'a community proposes a better question' G needs research scientist (the rung below); a volunteer organiser
  reaches the coordinator after a research post (the rule names the organiser in `rungs=`; the step is from a research
  assistant or scientist).
- **P9.** Five new long shots (table above) and 'a search for a new voice for science' made one.
- **P10.** per_year back to the times lines: 'the funding call closes on Friday', 'pressure to say more than the data
  show', 'a finding that makes the news', 'a rival's result contradicts yours' ('a fellowship of your own' already was).
- **P12.** Roads per color (table above): title acts moved in 'they want you to lead a group', 'a lab needs hands for the
  summer', 'the finding will not leave you alone', 'a lab offers you a desk, with conditions'; new acts in the rung
  moments ('your name is not on the paper' U>G scientist, 'a careful result that says no' B>U project lead with a
  [research grant], 'the budget will not stretch to everything' B>R group leader with [a loyal research team]). The
  W>G evidence-synthesis act in 'a careful result that says no' went back to its live form at the merge: two pooled
  runs of 1,600 lives still had the specialist at about 5x its target through it (holders met it every year or two).
- **P14.** Value tags (see Checks).
- **P16.** Moments for the postdoc and the professor ('they want you to lead a group' WU, 'the work you would rather be
  doing' U, 'a chair falls vacant at another university') and more for the facility lead.

## The pathway map

```
                         ┌──────────── doors ────────────┐
 'volunteers wanted to count what lives here'   'a lab needs hands for the summer'
 'a project online asks for a thousand pairs'   'a research post you are half qualified for'
 'the finding will not leave you alone'         'a question from childhood comes back'
                │                                           │
     citizen scientist ─> community observer        research assistant ─┬─> research software engineer
            │   'the survey wants a paid assistant' ──>    │            └─> research data steward
            └─> volunteer research organiser               │ 'the contract runs out', 'a scientist's post at a famous lab'
                         │ (a rung kept on the step)       ▼
                         └─> participatory  <──  research scientist (+ postdoc: 'a named fellowship, one a year')
 (from a research post)      research coordinator     │            │            │
                                                      │ 'a fellowship of your own'   'leaving research for another life'
                                                      │ 'a national centre opens its posts'          │
                                                      ▼            ▼                                 ▼
              laboratory technician            research project lead   independent    science communication specialist,
              (base title)                            │                investigator   evidence synthesis specialist,
                     │ 'the facility needs a head'     │ 'they want you to lead a group'     data analyst, teacher
                     ▼                                 ▼
              research facility lead          research group leader ── 'the work you would rather be doing' ──> back to the bench
                                                       │
                                                       ▼ 'a chair falls vacant at another university'
                                                professor (on the group, or on the scientist's post)
```

Reach grows along the way: [published research] and [name in the field] (base), then [known across the country] after
'a finding that makes the news'. Falls: 'an error in your published work', 'pressure to say more than the data show',
'a rival's result contradicts yours', 'the field season is lost', a contract or grant that ends.

## Emren's ten life arcs as routes

| Arc | Route in the pack |
| --- | --- |
| The technical master | [laboratory technician], [lab work], [instrument troubleshooting], 'the facility needs a head', [research facility lead] |
| The independent analyst | [working with data] or [writing code], [citizen scientist] or [research data steward], [reproducible workflow], [research collaborators] |
| The community investigator | [community observer], [volunteer research organiser], 'a community proposes a better question', [participatory research coordinator] |
| The academic investigator | [research assistant], [doctoral graduate], 'the contract runs out', [research scientist], a postdoc, 'a fellowship of your own', [professor] |
| The applied translator | a career outside research, 'the finding will not leave you alone', [research assistant] or [research project lead] |
| The reluctant leader | [research group leader], 'the work you would rather be doing', back to [research scientist] |
| The returning researcher | a break, then 'a research post you are half qualified for'; skills kept but faded (skill_half) |
| The late entrant | 'a question from childhood comes back', [citizen scientist], 'the survey wants a paid assistant' or 'a discovery nobody asked you for' |
| The evidence custodian | [research data steward], 'an old dataset suddenly matters', [a dataset others use] |
| The researcher who leaves | 'leaving research for another life', [science communication specialist] or a base career; perks stay |

## Hooks into the base world

The pack never edits base moments. It opens from a life's history instead, through echoes: 'the finding will not
leave you alone' follows the base 'a breakthrough in your work'; 'a question from childhood comes back' follows the base
'a curiosity that will not let go' and 'awe'. Base titles and perks it builds on: [graduate], [doctoral graduate],
[laboratory technician], [data analyst], [archivist], [software developer], [journalist], [teacher], [lab work],
[working with data], [writing code], [finding things out], [archive research], [published research], [name in the
field], [research grant], [teaching]. EXTEND_SCIENCE or-s routes into base rules ([doctoral graduate], [research
grant], [published research], [lab work]) and into Politics' [policy analyst].

## Boundaries with other packs (Emren's section 13)

Education owns enrolment and doctoral study (until it exists, the base [graduate] and [doctoral graduate] stand in);
Healthcare owns treating patients (a clinical researcher never gains the right to treat); Business owns ventures built
on a finding; Politics owns campaigns that use evidence; Technology shares [writing code] and [automating analysis]
rather than doubling them.

## What the engine needs for this pack

1. The pack in batch.PACKS (live): catalogue, rules (roles.py) and the compiled moments on top of the base.
2. engine-conditions.py pasted into earth_rules.PACK_RULES["science"] ("science LONGSHOTS"): LIFE_SCIENCE_LONGSHOTS (now
   nine gates) and ECHO_SCIENCE_LONGSHOTS (the second try reads one branch per long shot).
3. After round 5, one refit of ROLE_NORM and the tier lift (TIER_LIFT) for the pack's titles, with TARGET_SCIENCE
   (the doctorate now at 4 times its share).
4. Colorless facets (postdoctoral researcher, professor) on a career title; threshold seasons on research scientist,
   research group leader, independent investigator and research facility lead.
5. Earned odds: HELPS and WINDOWS in helps.py (preparation and timing lifts on acts that take a title).
6. For the refit (round 5 smoke runs, 60 lives each): any pack career ran at .37 to .47 of lives against the .333
   budget, and research assistant and research scientist at about 2.7 and 3 times their targets on average. Half of the
   scientist's gains were "changed jobs" (an entry title, scaled by the lift); the rest grew from the assistant. The
   facility lead, the postdoc, the independent investigator, the professor and the long-shot perk need the pooled run
   (four seeds) to be read.

## Departures from Emren's document

- Perks carry ways (colors), balanced over the five colors; the document keeps them colorless.
- Method facets are story notes, not titles; projects are a perk plus an optional plan, not a new system.
- Emren's six aspects map onto existing quantities, as the document itself asks: no new currencies.
