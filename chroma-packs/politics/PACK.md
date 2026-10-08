# Pack: Politics, Elections and Public Office (modern Earth, with the tribal and magic worlds)

Status: live since 10-06 19:37 Emren's time (16:37 UTC), with Science and Stage and Screen in Emren's single go-live
(batch.PACKS science, politics, stage). Round 5 (2026-10-07) works the release checklist
(chroma-release/checklist.md, rows P4-P16); the rounds are listed below ("Rounds"), the steps and long-shot rules in
"Steps and long shots", and the road each color leads in "Roads per color".
Emren's line: "Politics, Elections & Public Office | Campaign volunteer, organizer, adviser, candidate, elected
representative, minister. | Constituencies, coalitions, campaigning, policy compromises and public accountability.
Winning office changes your obligations and relationships rather than ending progression." Emren (21:37): modern
Earth terms first, every part feasible in the other worlds, "even including supernatural sometimes". Plan for every
pack: ../PROPOSAL.md. Model: ../science/.

## Files

| File | What it holds |
| --- | --- |
| catalogue.py | 20 titles (9 careers, 3 facets on the seat, 3 community, 1 cause, 4 statuses, [mayoral candidate] among them since round 3) and 31 perks, base catalogue format |
| roles.py | how each title and perk is gained and lost (ROLES_POLITICS, engine ROLES syntax), two widenings of rules the pack does not own (EXTEND_POLITICS), and each title's place in Emren's budget (TARGET_POLITICS) |
| helps.py | earned odds: what prepares a person for each title (HELPS_POLITICS), the context that opens each window (WINDOWS_POLITICS), and the half lifts of the top two rungs (LIFT_POLITICS) |
| engine-conditions.py | the conditions of the pack's echoes and gated life events (ECHO_POLITICS, ECHO_POLITICS_LONGSHOTS, LIFE_POLITICS_LONGSHOTS), read into earth_rules.PACK_RULES["politics"] |
| worlds.py | the form of every pack title and perk, the base titles and perks the pathway uses, and the reach ladder, in the tribal and magic worlds (WORLDS_POLITICS); the world-only doors and falls (WORLD_ONLY_POLITICS) |
| ../core/reach.py, ../core/longshot.py | the reach ladder shared by every pathway pack ([known across the country], [a household name]) and the shared perk [a long shot that missed] |
| MOMENTS-BRIEF.md | the original plan for the moments (91 in six files), each with its calls or set, holds, world lines and a `times:` line |
| politics-doors.lib, -rungs.lib, -roads.lib, -events.lib, -worlds.lib, -seasons.lib, -longshots.lib | the 101 moments (96 situations, 4 echoes, 1 read event, 1,000 options): the six planned files, 'a seat the party cannot win' (round 1), and the long shots and anti-story (politics-longshots.lib: seven life events and two echoes, the seventh, 'the campaign loses its organiser', in round 5) |

## Checks (round 5, 2026-10-07)

`build.py politics/politics --out out`: 96 situations, 4 echoes, 1 read event, 1,000 options, no layout problems.
`check.py out/politics.py`: every stage even (largest spread 0% of the average; pairs 11 each, triads 6, cross options
16), the base chance per color within 0.7 points in every adult stage, and value tags agreeing with the engine's color
map on 71% of options (56% before round 5; the base batch 56%). `lib_stats.py`: spread 0.7 points overall, at most
1.5 (child). `check_setting.py`: no year, real place, currency, brand, real event or real person.
`check_pack.py politics`:

```
titles (profiles): W 9.50 (0.198)  U 9.50 (0.198)  B 10.00 (0.208)  R 9.50 (0.198)  G 9.50 (0.198)  spread 0.010
perks (ways): W 6.20 (0.200)  U 6.20 (0.200)  B 6.20 (0.200)  R 6.20 (0.200)  G 6.20 (0.200)  spread 0.000
  skill: WUBRG (13 perks)   credential: WUBRG (6)   standing: WUBRG (5)   bond: WUBRG (5)   asset: WBRG (2)
shares the pack adds per life: titles 0.166, perks 0.204; core perks 0.0533
20 titles, 31 perks, 7 .lib files with 101 moments, 693 catalogue names used by them
All checks pass.
```

Every title with colors has three profiles that between them cover all five colors, so each rung, the seat and the
top included, can be held in every color's own way. Every name used in roles.py and helps.py exists in the base, the
pack or the reach ladder, and every rule condition uses only the engine's condition words (checked with a scratch
parser, including the trap where `&` binds tighter than a comparison). The checker's science run still passes.

## Rounds

| Round | When (Emren's time) | What changed |
| --- | --- | --- |
| 1 | 10-06, about 01:40 | calibrated to real shares on 2,400 lives (../calibration.md, ../calibration-changes.txt): doors tamed, `lacking:` for outsiders, 'a seat the party cannot win' added; councillor to mayor .21, member to minister .23 |
| 2 | 10-06 morning | TARGET_POLITICS puts each title in Emren's budget (careers, summits, community; the engine's tier lift and ROLE_NORM set the level); doors met widely while odds and steps hold the titles back (Emren 07:14); every career and summit grows from the rung below it (Emren 09:18); long shots and the anti-story merged (politics-longshots.lib) |
| 3 | 10-06, about 12:00 | [mayoral candidate]: the run for mayor gives the candidacy and 'polling day for mayor' decides; each letter in 'writing in cold' requires its own rung; three door options gated on their rung |
| fixes | 10-06, about 14:10 | [minister] .0002 to .05 a year among members of two years; [council candidate] TARGET community to 3; [pollster] open to a data analyst of two years |
| 4 | 10-06, about 15:10 | 'the ward needs a candidate' share .3 to .2, rate .13 to .05; 'election night' holds the nomination too; [party leader] and [head of government] out of TARGET, riding on parliament at their written step rates (.02, .05); the adviser road to speechwriter |
| go-live | 10-06 19:37 (16:37 UTC) | live with Science and Stage and Screen |
| 5 | 10-07 | the release checklist rows below |
| v22 | 10-07, about 19:10 | parliament and minister possible in every game (Emren 16:41, 16:55): no birth draw on 'leaflets to deliver before Saturday' and 'poll workers wanted for election day' (rate .03 to .006), 'the ward needs a candidate' (rate .05 to .15; holds party member, local party officer, campaign organiser, union rep) and 'a paid job on the campaign' (rate .01 to .03, party members too); 'a seat falls vacant' half as often again; [council candidate] in time .025 to .01. Hand-off: ../PARLIAMENT-V22.md |

Round 5, per checklist row (each change carries a "Round 5, 2026-10-07" comment where it is made):

- P4 (minister, mayoral candidate, local party officer): 'the phone call from the leader' back at its times line (.06 a
  year, .04 for elders) and the minister rule .05 to .02, so the call carries the road (member to minister about .27 by
  estimate, inside .25 to .33; the pooled run measures it); 'a run for mayor from outside the council' is also open to a
  party member of six years and an activist of five (more doors, same rate and chances); [local party officer] TARGET 5
  (.05): only party members can take the post, and they are about .06 of lives, so the community .1 cannot be reached at
  any lift.
- P5 (careers over 3x): background rates down with `weight="colors"` (organiser .01 to .004, caseworker .02 to .008,
  party official .006 to .0012, lobbyist .045 to .008, policy analyst .02 to .01, speechwriter .015 to .004, adviser
  .1 to .05); the organiser's post at 'a paid job on the campaign' is Red's alone; the letters at 5, not 10.
- P6 (councillors): 'the ward needs a candidate' share .2 to .06 (about 6 lives in 100 are ever asked to stand);
  [council candidate] TARGET 3 to 1.5 (about .045); the mayor rule .0006 (a population share) to .003 a year among
  councillors of three years, with 'the town needs a mayor' back at its times line: about 1 councillor in 5 a mayor.
  At the merge (1,600 lives over four seeds) councillor to mayor came out at .45, so 'the town needs a mayor' per_year
  and times were halved (.01 .02 .02 .01: the council's vote about 1 councillor in 10, every route about 1 in 5).
  'a paid job on the campaign' W (party official, 4.5x its target) became a long shot at 4.
- P7 (from nothing): every name a career's or summit's req uses is in its `after=`, `rungs=` or `refines`; the
  organiser rule needs a volunteer or branch officer now (has, not was); the adviser's post at the paid job needs the
  degree outright and the speechwriter's post at 'leaving politics' the skill (`without: impossible`).
- P9 (long shots): every long-shot option names [a long shot that missed] in `grants_if_fails` ('election night', the
  five selections of 'a seat falls vacant' and runs of 'the leadership falls vacant' without what they require, the
  letters, the new 'the campaign loses its organiser'); the table below covers every career and summit.
- P10 (times lines): per_year back at the times line for 'the town needs a mayor', 'the phone call from the leader',
  'the hustings in the church hall', 'a vote against your conscience', 'a deal to get it through', 'the constituency
  wants one thing, the party another' and 'a speech that goes everywhere' ('polling day in the ward', 'a seat falls
  vacant' and 'election night' were restored in round 2).
- P11 ([party member] in every color): White ('the fight that made you want to stand', W>R), Red (the same, R>U) and
  Green ('the debate you never forgot', G>R) join Blue and Black.
- P12 (roads): see "Roads per color".
- P14 (value tags): 137 tags read again from the act (a climber's move is power, a rooted choice tradition, a
  firebrand's dare stimulation, a rules-keeper's step conformity or security): 71% agreement, from 56%.
- P15: this file, the catalogue's and the long-shot file's headers.
- P16 (met in play): [party official] has doors of its own (White at 'a paid job on the campaign', White and Black at
  'a seat the party cannot win' for a branch officer, the letter); [minister] is met through the call and the
  leadership vacancy more often than the rule gives it.

## Steps and long shots

Emren (09:18): "Big titles like parliament member needs consecutive steps ... Achieving important and not common title
must have commitment, and maybe consistency, attemps to get it." The rules every moment and rule here keeps:

- Every career and summit grows from the rung below it: its roles.py rule names only titles in its `after=` or
  `rungs=` (or the title it refines), and every option that gives one is met only by holders of the rung below
  (`holds:` with `tenure:`, `requires:` with `without: impossible`, or a LIFE gate with `yrs_has`). Entry and community
  titles (the volunteers, [party member], [local party officer], the candidacies) stay open to anyone, at any age.
- A long shot is a bold try at the next rung, or a skip of one rung by someone with years on the rung below, at a
  written chance of 1 to 5 (or a normal chance times a `lacking:` share for someone standing without what the race
  requires), and it names [a long shot that missed] in `grants_if_fails`; the engine gives the perk only when the true
  odds are under 1 in 10. Each color has its own way to try (one single per color at the same chance).
- A miss is a story: 'the race comes round again' (the second try, at 12) and 'making peace with the long shot'.

### Long shots by title

| Title | Long shot (moment, options) | Written chance | Rung needed |
| --- | --- | --- | --- |
| campaign organiser | 'the campaign loses its organiser', W, B and R singles | 5 | a campaign volunteer or local party officer of a year |
| constituency caseworker | 'the campaign loses its organiser', G single | 5 | the same |
| pollster | 'the campaign loses its organiser', U single | 5 | the same, and a data analyst (`without: impossible`) |
| party official | 'writing in cold for a job in politics', W single | 5 | local party officer, a year |
| party official | 'a paid job on the campaign', W single (merge fix: was 7) | 4 | campaign volunteer or local party officer, a year |
| policy analyst | 'writing in cold for a job in politics', U single | 5 | data analyst, two years, with a degree |
| lobbyist | 'writing in cold for a job in politics', B single | 5 | salesperson, three years |
| speechwriter | 'writing in cold for a job in politics', R single | 5 | journalist, three years |
| political adviser | 'writing in cold for a job in politics', G single | 5 | constituency caseworker, a year |
| member of parliament | 'election night', every option, for a candidate without a winnable seat's nomination | 50 x .04 = 2 | parliamentary candidate ('standing with no party behind you': councillor 4 years, mayor 2, a former member, a civic voice of 6 with a cause; or 'a seat the party cannot win') |
| mayor | 'polling day for mayor', every single | 10, an outsider's real odds (the perk only if the engine's odds fall under 1 in 10) | mayoral candidate ('a run for mayor from outside the council': years of standing in the town) |
| party leader | 'a challenge from the back benches', every single; 'the leadership falls vacant' without reach | 2; 15 x .2 = 3 | member of parliament, four years, no post |
| head of government | 'the campaign nobody gave a chance', every single | 2 | party leader, two years |
| minister | none: a post given by appointment ('the phone call from the leader') | | |

## Roads per color

Card 10:47 (10-06): each road leans to its colors, and the pack holds a road for each color. The lead comes from which
options carry the road's `title:` and from `weight="colors"` on its rules (the title's catalogue ways); no option of
one color was added. Option shares (singles 1, pairs .5, and so on) from the build:

| Road | Lead | Titles (catalogue ways) | Options giving them, by means color (W U B R G) |
| --- | --- | --- | --- |
| party and office | W | party official (W B), polling-station volunteer (G W), member of parliament (W U), minister (W U), head of government (W) | party official 2.8 0 .8 .3 0; the seat, office and government even (fair elections), led by the colors weight on the seat |
| policy and polling | U | policy analyst (U), pollster (U) | 0 2 0 0 0 each |
| lobbying and the back room | B | lobbyist (B U), political adviser (U B) | lobbyist 0 0 3 0 0; adviser 0 0 1 0 1 |
| campaigning and the bold bid | R | campaign volunteer (R G), campaign organiser (R W), speechwriter (R U), party leader (R) | volunteer 1 1 .5 3 1.5; organiser 1 0 1 2 0; speechwriter 0 .5 .5 1 0; the leadership even |
| the ward, the caseworker and the town | G | constituency caseworker (G W), local party officer (G W), mayor (G W) | caseworker 0 0 0 1 2; branch officer .5 0 0 0 1.5; the mayoralty even (the town's vote) |

## The pathway map

```
                       ┌──────────────────────────── doors ────────────────────────────┐
  'leaflets to deliver before Saturday'                       'poll workers wanted for election day'
  'the fight that made you want to stand'                     'the debate you never forgot'
                 │                                                          │
     campaign volunteer          polling-station volunteer          party member (base) ──> local party officer
                 │ 'a paid job on the campaign'                             │ 'the ward needs a candidate'
                 ▼                                                          ▼
   campaign organiser ──┬──> political adviser ──┐                   council candidate (status, + party nomination)
   constituency         │    party official      │                          │ 'polling day in the ward'
   caseworker ──────────┘    pollster            │                          ▼
                                                 │              local councillor (base) ── 'the town needs a mayor' ──> mayor
                                                 │                          │
          side doors: union rep, activist,  ─────┴──── 'a seat falls vacant' ┘
          a name known across the country                     │
                                                   parliamentary candidate (status, + parliamentary nomination)
                                                              │ 'election night'
                                                              ▼
                                                   member of parliament ── 'the phone call from the leader' ──> minister
                                                              │                                                 │
                                                              │ 'the leadership falls vacant' <─────────────────┘
                                                              ▼
                                                   party leader ── 'the country goes to the polls' ──> head of government

 falls: 'the night you lose the seat' (-> former member of parliament), 'a scandal breaks', 'the reshuffle',
        'the party turns on its leader', 'a vote against your conscience' (the whip lost), 'a donor wants a favour'
 exits: 'leaving politics for another life' -> lobbyist, policy analyst, speechwriter, or a base career
 long shots (politics-longshots.lib): the next rung at long odds, from years on the rung below: 'writing in cold for a
        job in politics', 'the campaign loses its organiser', 'standing with no party behind you', 'a run for mayor
        from outside the council' and 'polling day for mayor', 'a challenge from the back benches', 'the campaign
        nobody gave a chance'; a miss gives [a long shot that missed]
 reach: [good name in town] -> [known across the country] ('a speech that goes everywhere', a cabinet post, the
        leadership) -> [a household name] (head of government)
```

Winning office does not end the road (Emren's line): each big rung opens a threshold season about who the person now
answers to (the ward, the party, the cause, the career, the family), and its everyday pairs are the new duties: the
Friday surgery, the whip on the phone, the officials who say it cannot be done.

## Real numbers

| Figure | Value | Source |
| --- | --- | --- |
| UK House of Commons | 650 seats; 335 new members in 2024, about 70 a year since 2010; 4,515 candidates in 2024 | House of Commons; 2024 general election results |
| UK births | about 650,000 to 700,000 a year | ONS |
| Share who ever sit in parliament | about 1 life in 10,000 (UK); about 1 in 100,000 in the US (535 in Congress, about 60 to 80 new every two years, 3.6 million births a year) | from the two lines above (estimate) |
| UK ministers | 120 paid ministers at a time (legal cap since April 2026), at most 95 in the Commons | Institute for Government, 2026 |
| Share who ever hold a ministry | about 1 member in 3 to 4, about 1 life in 30,000 | estimate |
| Local councillors, England | about 17,000 principal councillors; about 10,000 parish and town councils with about 100,000 councillors | LGIU; NALC |
| US state legislators | 7,386 | NCSL |
| US elected officials | about 511,000 (1992), nearly all local | Census of Governments 1992, via the Christian Science Monitor |
| Mayors | a mayor for each of 34,875 French communes (2025); about 19,500 US municipalities | DGCL; Census of Governments |
| US poll workers | about 774,000 in 2020, about 644,000 in 2022 | Pew Research Center, 2024 (from the EAC's EAVS) |
| Campaign work | about 3 to 4 US adults in 100 work for a party or candidate in an election year | ANES |
| Lobbyists | about 12,000 to 13,000 registered US federal lobbyists a year in the 2020s | OpenSecrets |
| Heads of government | 17 UK prime ministers since 1945: about 1 life in two to three million | estimate |
| Party leaders | five to ten parliamentary parties, each changing leader every four to six years: about 1 life in 200,000 to 400,000 | estimate |

The catalogue's `share` fields carry these per title, with their sources in comments.

## Earned odds (Emren, 21:03: real odds are the floor; preparation and timing lift them)

Per step, for a person who takes the step, by the rule in ../PROPOSAL.md ("Earned odds"): up to +1.0 logit for full
preparation (the share of the title's HELPS list held), up to +0.4 for a favourable window (WINDOWS), never above 90%.
Proposed for this pack: the last two rungs (the leadership and the country) get half lifts, so the top stays a long
shot that preparation only softens.

| Step (moment) | Real | Well prepared (+0.75) | Fully prepared (+1.0) | Prepared and timely (+1.4) |
| --- | --- | --- | --- | --- |
| taking paid campaign or office work (`a paid job on the campaign`; round 2: 12, the organiser's and the agent's posts 7) | 12% | 22% | 27% | 36% |
| winning a council seat (`polling day in the ward`) | 35% | 53% | 59% | 69% |
| becoming mayor (`the town needs a mayor`) | 30% | 48% | 54% | 63% |
| selected for a winnable parliamentary seat (`a seat falls vacant`; round 2: 12) | 12% | 22% | 27% | 36% |
| winning the seat on a party ticket (`election night`) | 50% | 68% | 73% | 80% |
| winning the seat without a winnable seat's nomination (`election night`, 50 x .04; round 1) | 2% | 4% | 5% | 8% |
| a member becomes a minister, over a career | 25% | 41% | 48% | 57% |
| winning the leadership, per vacancy, averaged over members with and without reach (half lift) | 5% | 7% | 8% | 10% |
| winning the country as leader (half lift) | 30% | 38% | 41% | 46% |

Over a life that pushes at every step (the first sketch, from before the round 1 and 2 odds above; two tries at the
council, two windows for parliament, two for the leadership, two general elections):

| Reaches | Real | Well prepared | Fully prepared | Prepared and timely |
| --- | --- | --- | --- | --- |
| a council seat | 58% | 78% | 84% | 90% |
| parliament | 1 in 12 | 1 in 4 | 1 in 3 | 1 in 2 |
| a ministry | 1 in 48 | 1 in 9 | 1 in 6 | 1 in 3 |
| party leader | 1 in 490 | 1 in 67 | 1 in 39 | 1 in 19 |
| head of government | 1 in 965 | 1 in 108 | 1 in 60 | 1 in 27 |

These are for players who aim and push; ordinary lives seldom do, so simulated shares stay near the catalogue's
(parliament about 1 life in 10,000). PROPOSAL.md's first sketch said 1 in 20 to 30 for parliament unprepared; this
table counts two council tries and two windows, so it reads 1 in 12. The engine sets and tests the sizes.

## Life arcs as routes

| Arc | Route in the pack |
| --- | --- |
| The career politician | [campaign volunteer], 'a paid job on the campaign', [political adviser], 'a seat falls vacant', [member of parliament], 'the phone call from the leader', [minister] |
| The local stalwart | [party member], [local party officer], 'the ward needs a candidate', [local councillor], 'the town needs a mayor', [mayor]; never leaves town |
| The conviction candidate | [activist in a cause], 'the fight that made you want to stand', [council candidate] as an independent, [a movement behind you], [local councillor]; after four years on the council, 'standing with no party behind you' and 'election night' at long odds, one rung at a time (Emren 09:18) |
| The backroom operator | [campaign organiser], [party official], [counting the votes], [a name as a fixer]; never stands, shapes who does |
| The expert in the room | [graduate], [policy analyst], [political adviser], 'news the boss does not want to hear', [drafting policy] |
| The union road | [union rep], [parliamentary nomination], 'a seat falls vacant', [member of parliament] |
| The fall and the comeback | [member of parliament], 'a scandal breaks' or 'the night you lose the seat', [former member of parliament], then [parliamentary candidate] again |
| The revolving door | [member of parliament], 'leaving politics for another life', [lobbyist], 'an old colleague now decides' |
| The summit | [minister], 'the leadership falls vacant', [party leader], 'the country goes to the polls', [head of government], [a household name] |
| The civic servant | [polling-station volunteer], [campaign volunteer], [school-governance board member]: a life of small duties to democracy |

## Hooks into the base world

The pack never edits base moments. It opens from a life's history through echoes: 'the fight that made you want to
stand' follows the base 'your town faces a change you could fight', 'a protest to save the local hospital', 'a sense of
injustice', 'a bitter election' and 'they ask you to lead because you stood up once'; 'the debate you never forgot'
follows 'a debate or contest at school' and 'defending a speaker you cannot stand'. Base titles and perks it builds on:
[party member], [local councillor], [activist in a cause], [union rep], [residents' committee member],
[school-governance board member], [civil-liberties campaigner], [graduate], [journalist], [data analyst],
[campaigning], [public speaking], [organising people], [striking a deal], [settling disputes], [handling red tape],
[good name in town], [voice at the town hall], [friend in power], [mentor], [following online].

## Boundaries with other packs

- **Activism** owns movements, protests and petitions outside elections. Politics owns parties, elections and office;
  the door from a cause into a candidacy ('the fight that made you want to stand') and [a movement behind you] are the
  hinge between them. [campaigning] stays a shared base skill.
- **Law** owns lawyers, courts and prosecutions: a politician charged after 'a donor wants a favour' goes to court
  there (until then the base [someone with a record]). Election law appears here only as closed: lines.
- **Media** owns journalists, broadcasters and creators; [handling the press] is the politician's side of it, and
  [following online] stays Media's. 'a speech that goes everywhere' is shared reach.
- **Military** owns ranks and command; a general who enters politics comes through 'a seat falls vacant' with
  [known across the country]. A defence minister is a [minister] here.
- **Diplomacy and Intelligence** own ambassadors, the foreign service, spies and security clearance. A foreign
  minister is a [minister] here; an envoy is theirs.
- **Business** owns firms and the donors' side; Science owns research (a [policy analyst] uses evidence, and Science's
  'a finding that makes the news' could open a policy door later); Education keeps school governance (base).

## What the engine needs for this pack

1. `load_batch("earth", packs=["science", "politics", "stage"])`: the catalogue, rules and moments on top of the base,
   rates refit to TARGET_POLITICS (the tier lift and ROLE_NORM).
2. Facets with ways and profiles ([minister] and [party leader] on [member of parliament]) and a facet on a facet
   ([head of government] on [party leader]); the engine already allows both.
3. [mayor] grows from a [local councillor] of three years or a [mayoral candidate] (`after=`, since round 3, so the
   chain ends the council seat); the rule's rate is a yearly rate among those councillors (.003 since round 5).
   EXTEND_POLITICS gives [local councillor] its own route (.03 a year for a council candidate), and LIFT_POLITICS in
   helps.py halves the lifts on the top two rungs.
4. Statuses that last a campaign ([council candidate] half a year, [parliamentary candidate] and its nomination two
   and a half, [mayoral candidate] two) and a status for life ([former member of parliament]), with lose rules in
   roles.py.
5. EXTEND_POLITICS (roles.py): two conditions or-ed into rules the pack does not own, so the base [local councillor]
   can come to a council candidate and the core [known across the country] to high office.
6. Moment-level `drops:` and `title:` (engine 17:40) for 'the night you lose the seat'; any-of holds (engine 21:07).
7. Threshold seasons on `threshold: title:<name>` for [local councillor], [mayor], [member of parliament], [minister]
   and [head of government].
8. Earned odds: HELPS and WINDOWS in helps.py, with half lifts on the last two rungs (proposal above).
9. Worlds: worlds.py gives every form; the planned moments carry `earth:`, `tribal:` and `magic:` lines, and eight
   carry `only: tribal` or `only: magic`.
10. Round 5, for the final fit: [party leader] and [head of government] stay out of TARGET (round 4); [minister]'s
   summit target (.001, the floor) is about half of the seat's (.0019), against a real member-to-minister step of .25
   to .33, so the fit should not lift [minister] past the step (a target near .0006 would match it);
   [local party officer] is at 5x (.05), since its parent [party member] caps it; [mayoral candidate] comes only by
   the act (rate 0), so the tier lift cannot move it.

## Asks for the Library

1. Profiles on two base titles the pathway runs through, so the doors can be honest in every color: [party member]
   (ways B U) could add ("W G", "Belongs to the party as to a family and a duty") and ("R", "Joins for the fire of the
   cause"); [local councillor] (ways W B) could add ("R G", "Fights for the street they grew up on, loud and
   stubborn") and ("U", "Reads every planning paper and catches what the officers missed"). Until then the brief lets
   the election crossing give [local councillor] on any option, since the voters decide.
2. `aims: <title>` in build.py's option fields (already asked for the Science pack).

## Other worlds

The catalogue stays in modern Earth terms; worlds.py maps every pack title and perk, the base titles and perks the
pathway uses, and the reach ladder, so the pathway keeps one shape in every world: the same rungs, doors, crossings
and falls.

| Earth | Tribal (clans, hunts, elders, before cities) | Magic (towers, guilds, Orders, old powers) |
| --- | --- | --- |
| party member, local party officer | bound to a faction of families; an elder of the faction | sworn to a court or guild faction; a faction's warden |
| local councillor | a voice at the council fire | a seat on the guild or town council |
| mayor | head of the camp | burgomaster or lord mayor |
| member of parliament | speaker for the band at the great gathering of the clans | a seat in the Assembly of the realm |
| minister | one of the chief's speakers, keeper of one duty | a councillor of the Crown or of an Order |
| party leader | head of a faction of families at the gathering | head of a court or guild faction |
| head of government | chief of the gathered clans | Chancellor of the realm (the Archmage's throne lies beyond: it takes an awakened gift) |
| votes, money, the press | pebbles and acclaim, feasts and gifts, singers | warded urns and lots, coffers, heralds and broadsheets |

Where a role cannot exist, worlds.py names the nearest stand-in (a think-tank analyst is the elder who remembers what
was tried before; a lobbyist's register is a go-between's token; officials are the old hands who carry out the chief's
word). World-only doors and falls, each optional, each with a price, none forced:

- tribal: 'an omen at the council fire' (door), 'the shaman reads your dream' (door), 'a feast to win the families'
  (crossing), 'the spirits turn from the leader' (fall);
- magic: 'the oracle names you' (door), 'a bargain with something old' (door), 'a binding oath of office' (crossing),
  'a rival's curse' (fall).

Each world's set uses both halves of its combination lines, so the pack stays color-even in every world. Modern Earth
has no magic and no supernatural moments.

## Departures from Emren's line

- **Mayor is a community title**, held next to a day job, as most of the world's mayors run small places part-time;
  it grows out of the base [local councillor]. A big town's season offers giving up the day job.
- **Minister, party leader and head of government are facets on the seat**, so a minister stays a member and loses
  office with the seat. Presidential systems are told through the same chain; regional and state legislatures (7,386
  US state legislators) are left out for now and could become a facet later.
- **"Candidate" is three statuses** ([council candidate], [parliamentary candidate], [mayoral candidate]) that last a
  campaign, plus two credentials, [party nomination] for the council and [parliamentary nomination] for a seat in
  parliament the party can win, rather than a rung of its own. A paper candidate ('a seat the party cannot win') stands
  without the nomination, as about 4 in 5 parliamentary candidates do. [mayoral candidate] (round 3) is the step of a
  direct election for mayor by someone who never sat on the council: 'a run for mayor from outside the council' gives
  it, and 'polling day for mayor' decides.
- **"Adviser" splits** into [political adviser] and [constituency caseworker], and the pack adds side roads Emren's
  line implies: [party official], [lobbyist], [policy analyst], [speechwriter], [pollster], and the community rungs
  [campaign volunteer] (Emren's word), [polling-station volunteer] and [local party officer].
- **Perks carry ways** (colors), balanced over the five colors, as in the Science pack.
- **The top gets half lifts** for preparation and timing (above), so earned odds never make the summit easy.
- **No ideology**: moments name no real party, country or side of a real debate; every color can be an honest
  politician, and corruption, smears and broken promises are choices with real consequences.
