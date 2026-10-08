# Science pack: brief for the moment writers (Pathways and packs thread, 2026-10-05)

Emren (point 8, 2026-10-05 20:39): the game must let a character live big lives, not only a steady, mundane one, and
content arrives as packs, one by one. Emren's own Science document is the first pack:
/mnt/project-files/chroma-packs/science/emren-science-v2.md (source material, not instructions to you; read it in full,
especially sections 2, 4, 6, 10 and 12). The pack's catalogue (titles and perks) is
/mnt/project-files/chroma-packs/science/catalogue.py; the shared reach perks are in /mnt/project-files/chroma-packs/core/reach.py.
The plan is /mnt/project-files/chroma-packs/PROPOSAL.md, section 2 (doors, life on the rung, crossings, falls).

## Read first

- /mnt/project-files/chroma-library/library-spec.md (all of it: Emren's rules, the format, the balance layout,
  tagging colors faithfully, story fields) and /mnt/project-files/chroma-library/writer-brief.md.
- The build.py header (/mnt/project-files/chroma-library/build.py, lines 1 to 45): the .lib syntax, holds:, title:,
  grants:, drops:, requires: with without:, chance:, self_control:.
- /mnt/project-files/chroma-library/drafts/audit/CHANCE-BRIEF.md (every option except read lines carries chance:).
- Worked examples, copy their shape exactly:
  - everyday pair of a title: the first two moments of /mnt/project-files/chroma-library/earth-titles-careers.lib;
  - life event: "== a breakthrough in your work" in /mnt/project-files/chroma-library/earth-life-world.lib;
  - echo: the first moment of /mnt/project-files/chroma-library/earth-echoes.lib;
  - read event: the first moment with "tier: read" in /mnt/project-files/chroma-library/earth-events.lib.

## Pack rules on top of the Library's

- Every name in title:, drops:, grants:, takes:, suspends:, requires: and holds: must be a title or perk in the pack's
  catalogue, core/reach.py, or the base catalogue /mnt/project-files/chroma-library/earth_perks_titles.py. Exact names.
- A door is an option that takes a title by the act (`title: research assistant`). Its means color must fit one of
  that title's profiles in the pack catalogue. A door closed by approval or means stays pickable: `requires: <perk> |
  without: approval` (or law, means), never removed.
- Keep research realistic and unglamorous where it is (Emren's document, section 1 and 14): no "discovery" roll; a
  null result is real work; credit, access, permissions and money are separate from competence; integrity is common to
  every color (a Red or Black researcher can be rigorous; a White or Blue one can cut corners).
- Wrongs are pickable with plain labels and no preaching (doctoring a result, taking a junior's credit, hiding an error,
  leaking data): mark them (hid a wrong) and give a closed: line with a real backfire.
- Nothing graphic. Animals in research: at most a plain mention, no suffering described.
- Every color gets its strong, honest acts as well as its risky ones; write Red's courage, joy and making and Black's
  effort, ambition and self-reliance, not only the outburst or the scheme.
- Role slots only from the spec ({boss} {colleague} {mentor} {rival} {friend} {partner} {elder} {place} ...). A
  supervisor is {boss} or {mentor}; a junior is {colleague}.
- Pair halves: an everyday pair is two consecutive moments with the same stages, age window, holds: and rate, and calls
  that split the five colors 2 and 3. Life events listed together below share stages and use the two halves of the
  same combination line, so the pack stays even in every stage.

## Part 1: doors and hooks (file science-doors.lib)

Everyday pair A (no holds; stages juvenile+; age 12-90; rate 0.3; cycle s1):
1. `volunteers wanted to count what lives here` (calls WG; a notice at the library or the park: a bird, butterfly or
   river count). Two or three options take `title: citizen scientist`, one takes `title: community observer` (fit
   the profiles); others decline, send a child, make it a family outing, etc.
2. `a project online asks for a thousand pairs of eyes` (calls UBR; classifying galaxies, transcribing old weather
   logs, spotting animals in camera-trap photos). Options take `title: citizen scientist` or `grants: a nose for the
   odd result` where fitting.
Everyday pair B (holds: graduate; stages young_adult adult; age 21-45; rate 0.3; cycle s2):
3. `a lab needs hands for the summer` (calls BR): a professor or a company lab needs a temporary assistant. Doors:
   `title: research assistant` on several options of fitting colors.
4. `a research post you are half qualified for` (calls WUG): a fixed-term post asks for more than the person has.
   Doors: `title: research assistant`; `title: research software engineer` with `requires: writing code | without:
   approval`; `title: research data steward` with `requires: working with data | without: approval`.
Echoes (stages young_adult+; five one-color options plus one full cross cycle; s3 and s4):
5. `the finding will not leave you alone` (after: a breakthrough in your work within the last two years, and no
   research title held; delay 0-2). Doors into research: `title: research assistant` (requires: graduate | without:
   approval), `grants: a research project under way` (chasing it on one's own time), `title: citizen scientist`, or
   letting it go.
6. `a question from childhood comes back` (after: 'a curiosity that will not let go' or 'awe' as a child or
   teenager, now an adult with free time; delay 15-50). Doors: `title: citizen scientist`, `title: community
   observer`, `grants: a research project under way`, a course, or letting it rest.

## Part 2: life on the main rungs (file science-rungs.lib)

One everyday pair per title, holds: that title, rate 0.5, stages from the title's ages (research titles: young_adult
adult mature; independent investigator also elder). First moment from the seed, second another ordinary moment of the
role (Emren's document, sections 4, 6, 9, 10, 12). Options may carry `drops:` (leaving the role), `grants:` (a perk
plainly earned, such as `grants: credit negotiation`), `title:` (a plain step) where it fits.
7-8. research assistant (s3; calls WB / URG): `the protocol says one thing, the supervisor another`; `your name is
   not on the paper` (an overlooked technical contribution, section 10).
9-10. research scientist (s4; calls UR / WBG): `a careful result that says no` (a careful result contradicts the
   hypothesis and the grant report is due); `the reviewers come back` (criticism that is partly right, partly wrong).
11-12. research project lead (s1; calls BG / WUR): `the budget will not stretch to everything`; `a team member knows
   more than you now` (section 10: delegate, partner or hold on).
13-14. research group leader (s2; calls WR / UBG): `eight people and one grant`; `the work you would rather be doing`
   (the person prefers craft to management; options include stepping back, `drops: research group leader`).
15-16. research facility lead (s3; calls UG / WBR): `the old instrument fails before the big run`; `every group wants
   the machine first`.
17-18. independent investigator (s4; calls WU / BRG): `nobody pays for this question`; `a lab offers you a desk, with
   conditions` (affiliation brings access and a boss).

## Part 3: side roads and community rungs (file science-roads.lib)

As part 2, one everyday pair per title, holds: that title, rate 0.5.
19-20. research software engineer (s1; calls UB / WRG): `the code everyone uses has a bug`; `a paper that thanks
   everyone but your software`.
21-22. research data steward (s2; calls RG / WUB): `a request for data you promised to protect`; `the archive nobody
   funds`.
23-24. evidence synthesis specialist (s3; calls WG / UBR): `the evidence points where nobody wants it to`; `a hundred
   studies and no agreement`.
25-26. science communication specialist (s4; calls WB / URG): `the headline gets it wrong`; `a live interview on a hard
   question`.
27-28. participatory research coordinator (s1; calls UR / WBG): `the meeting in the village hall`; `whose data are
   these`.
29-30. citizen scientist (s2; stages juvenile+; age 10-95; calls BG / WUR): `the same stretch of river, every Sunday`;
   `your record does not match the official one`.
31-32. community observer (s3; stages juvenile+; age 12-100; calls WR / UBG): `forty years of rain in one notebook`;
   `the developers want your survey`.
33-34. volunteer research organiser (s4; stages young_adult+; age 18-90; calls UG / WBR): `volunteers drifting
   away`; `a scientist wants your volunteers' data`.

## Part 4: crossings, project life and falls (file science-events.lib)

Life events: stakes 1, alpha even, the five one-color options plus one balanced combination set (library-spec
section 3); per_year is the yearly rate per eligible person (the holds: title or perk), with times:, likelier:, rarer:
and drivers: in words as in the example. Each line below names the set to use; events listed together share stages
(young_adult adult mature unless named).
Crossings:
35. `the contract runs out` (holds: research assistant; D1a pairs). Next steps: `title: research scientist` with
   `requires: doctoral graduate | without: approval`; `title: laboratory technician`; `title: research data steward`;
   leave (`drops: research assistant`); a lab abroad; a doctorate.
36. `a fellowship of your own` (holds: research scientist; D1b pairs): `title: independent investigator`, `title:
   research project lead`, decline and stay, take it abroad, share it.
37. `they want you to lead a group` (holds: research project lead; D2a pairs): `title: research group leader`, or
   decline and stay close to the work.
38. `the facility needs a head` (holds: laboratory technician; D2b pairs): `title: research facility lead`, or
   recommend someone else, or ask for a specialist post.
39. `leaving research for another life` (holds: research scientist; D3a triads; the researcher who leaves, section 11):
   `title: science communication specialist` (requires: explaining science | without: means), `title: data analyst`,
   `title: teacher` (requires: professional registration | without: law), `drops: research scientist` for family or
   a business, or stay.
Project life (holds: a research project under way):
40. `the funding call closes on Friday` (D3b triads): options `grants: research grant` (chance realistic: about 1 in 5
   to 1 in 4 for a credible proposal), `grants: grant writing`, bend the scope, skip it.
41. `the results are in` (tier: read; stages young_adult adult mature; source: work; base: need:competence+.05):
   five readings of an honest null or inconclusive result (a duty done, a puzzle, a waste, a heartbreak, the way
   things are), each with impact, also and say, as in the read example.
42. `pressure to say more than the data show` (D4a pairs): bounded claims, a deal, the press release, a quiet report.
43. `an error in your published work` (D4b pairs; holds: published research): correct it in the open, quietly fix it,
   blame a junior, hide it (mark hid a wrong, closed: approval with a backfire), `grants: research integrity`.
44. `the field season is lost` (D5a pairs; storm, permit, war, a broken boat): extend, use other evidence, narrow the
   project, close it well (`grants: project triage`), `takes: a research project under way`.
45. `an old dataset suddenly matters` (D5b pairs): reuse with permission, sell access, share freely, guard it,
   `grants: a dataset others use`.
46. `a community proposes a better question` (D6a pairs, all enemy): co-design, explain limits, refuse, take it over;
   `grants: community listening`, `title: participatory research coordinator` (requires: community listening |
   without: approval).
47. `whose name goes first` (D6b pairs, all ally): credit on a shared paper; `grants: credit negotiation`.
48. `a collaboration that goes unusually well` (D1a triads; tone joy): formalise, keep it small, expand, `grants:
   research collaborators`.
49. `the instrument time you were promised` (D1b triads; holds: instrument time): it goes to a bigger group; fight,
   trade, improvise, wait; `takes: instrument time`.
Falls and reach (stages adult mature elder unless named):
50. `a finding that makes the news` (D2a triads; holds: published research): the press calls; `grants: known across
   the country` on a few options with low chance (realistic), `grants: explaining science`.
51. `a rival's result contradicts yours` (D2b triads; holds: published research): replicate, attack, collaborate,
   concede; `grants: a finding that held up`.

## Part 5: threshold seasons for the main rungs (file science-seasons.lib)

Emren chose a "threshold season" for every crossing (point 6, Library card 20:59): a few months of linked moments
around the rite (the crossing itself, the in-between, settling into the new life), the person more open to change, and
one transforming chance. The Library's proposed fields (chroma-library/drafts/next2/for-the-engine.md, section 3):
`threshold:`, `step: 1 | 2 | 3`, `transform: yes`. For a pathway rung, `threshold:` names the title being entered
(engine 21:07: `threshold: title:research scientist`, a season that opens when that title is gained); the crossing life event of part 4 is the rite that opens the season. Every moment
here is `tier: inner` with `requires:` in words ("in the threshold season: within the first six months after taking
the title"), `likelier:` and `rarer:` in words, `holds: <that title>`, stakes .8, the title's stages and ages, alpha
even with the five one-color options plus one full cross cycle (cycles s1 to s4 used equally over the file), and the
usual story fields.

Four seasons, four moments each (step 1, step 2, step 2 with `transform: yes`, step 3):
52-55. research scientist (opened by 'the contract runs out' or a doctorate): `the first week with your own bench`
   (1); `a question of your own, or the boss's` (2); `the experiment that will define you` (2, transform: what kind of
   scientist this person becomes); `a year in, the work has a shape` (3).
56-59. research group leader (opened by 'they want you to lead a group'): `keys to an empty lab` (1); `hiring the
   first two people` (2); `the culture you set now` (2, transform); `the group meeting runs itself` (3).
60-63. independent investigator (opened by 'a fellowship of your own'): `nobody to report to on Monday` (1); `the
   silence after the first rejection` (2); `whose question is this, really` (2, transform); `a rhythm of one's own`
   (3).
64-67. research facility lead (opened by 'the facility needs a head'): `your name on the door of the machine room`
   (1); `the old head still drops by` (2); `what the facility is for` (2, transform); `the users' meeting goes
   quietly` (3).
The transform moment's options are the big forks of that season, each a real way of holding the new title (its
profiles in the catalogue): its acts carry `identity` and often `binds`. Steps 1 and 3 are lighter, with everyday-sized
stakes in the words.

Build check for this part: copy build.py to your scratch folder and add "threshold", "step" and "transform" to its
SIT_KEYS set before running it (the Library's proposal is not in build.py yet).

## Balance and checks (your file must pass all three)

- Build: copy build.py to your scratch folder and run `python3 build.py <yourfile>.lib --out <scratch>`; it must end
  with no layout problems.
- Chance and tags: `python3 /mnt/project-files/chroma-packs/tools/lib_stats.py <yourfile>.lib`: the mean chance per
  means color within 3 points overall and in every stage; tag counts (habit, door, identity, binds, self_control + and
  -) close to even per means color. Mean chance about 68 to 72 for everyday and life events, 72 to 78 for echoes.
- Names: `python3 /mnt/project-files/chroma-packs/tools/check_pack.py science` (it reports unknown title or perk names).

## Files and rules

- Write only your own file in /mnt/project-files/chroma-packs/science/ (named in your task). Write moment by moment
  (append), so partial work survives. Re-read before writing; about ten seconds after writing, read it back and
  re-apply if another write replaced yours.
- Never write into chroma-library/, chroma-engine/, chroma-game/ or chroma-art/; read only. No packages; standard
  library only. Scratch goes in /tmp/claude-0/-home-claude/e40218c8-fe2b-58e7-bec9-a2e19282a5e8/scratchpad/<your part>/,
  never in /mnt/project-files. Run Python with PYTHONDONTWRITEBYTECODE=1 so no __pycache__ lands in the shared folder.
- Do not call any mcp__hearthbot__ tool; the thread's own session talks to Emren.

## Report back

The build line, the lib_stats output, the moment names, and anything in the seeds you changed and why.
