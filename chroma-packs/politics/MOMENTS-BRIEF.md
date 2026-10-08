# Politics pack: brief for the moment writers (Pathways and packs thread, 2026-10-05)

Status: Emren confirmed Politics as the next pack (thread, 21:37: "Politics next"); the moments were written to this
brief and are live since 10-06 19:37 Emren's time (16:37 UTC). This brief is the original plan; PACK.md holds the
current state (round 5, 2026-10-07), including Emren's 09:18 steps rule: every career and summit grows from the rung
below it, while entry and community titles stay open to anyone. Emren (point 8, 2026-10-05 20:39): the game must
let a character live big lives, never obliged to; packs come one by one. Emren's line for this pack: "Campaign volunteer, organizer, adviser, candidate, elected
representative, minister. Constituencies, coalitions, campaigning, policy compromises and public accountability.
Winning office changes your obligations and relationships rather than ending progression." Emren (21:37): modern
Earth terms first, but every moment must work in the other worlds, "even including supernatural sometimes".

The pack's catalogue (titles and perks) is /mnt/project-files/chroma-packs/politics/catalogue.py, the rules roles.py,
the earned odds helps.py, the other worlds worlds.py; the shared reach perks are in
/mnt/project-files/chroma-packs/core/reach.py. The plan is /mnt/project-files/chroma-packs/PROPOSAL.md, section 2
(doors, life on the rung, crossings, falls, reach).

## Read first

- /mnt/project-files/chroma-library/library-spec.md (all of it: Emren's rules, the format, the balance layout, tagging
  colors faithfully, story fields) and /mnt/project-files/chroma-library/writer-brief.md.
- The build.py header (/mnt/project-files/chroma-library/build.py, lines 1 to 45): the .lib syntax, holds:, title:,
  grants:, drops:, requires: with without:, chance:, self_control:, and the world fields earth:, tribal:, magic:, only:.
- /mnt/project-files/chroma-library/drafts/audit/CHANCE-BRIEF.md (every option except read lines carries chance:).
- The Science pack's moments, the model for this one: /mnt/project-files/chroma-packs/science/*.lib and its brief.
- Worked examples, copy their shape exactly: - everyday pair of a title: the first two moments of
  /mnt/project-files/chroma-library/earth-titles-careers.lib; - life event: "== a breakthrough in your work" in
  /mnt/project-files/chroma-library/earth-life-world.lib; - echo: the first moment of
  /mnt/project-files/chroma-library/earth-echoes.lib; - read event: the first moment with "tier: read" in
  /mnt/project-files/chroma-library/earth-events.lib; - threshold season:
  /mnt/project-files/chroma-packs/science/science-seasons.lib.
- The game's worlds: /mnt/project-files/chroma-game/prototype/story.py, SETTINGS and WORLD (read only), and this pack's
  worlds.py (the form of every title and perk in the tribal and magic worlds).

## Pack rules on top of the Library's

- Every name in title:, drops:, grants:, takes:, suspends:, requires: and holds: must be a title or perk in the pack's
  catalogue, core/reach.py, or the base catalogue /mnt/project-files/chroma-library/earth_perks_titles.py. Exact names.
  holds: may name several titles or perks with "|" (any of them; engine 21:07).
- A door is an option that takes a title by the act (`title: campaign volunteer`). Its means color must fit one of that
  title's profiles in the pack catalogue. Every pack title has profiles that together cover all five colors. The base
  [party member] (ways B U) and [local councillor] (ways W B) have no profiles yet; the pack asks the Library for them
  (PACK.md, "Asks"). Until they land, a door to [party member] uses B or U means, and the election crossing
  `polling day in the ward` may give [local councillor] on any option, since the voters decide, not the means.
- A door closed by approval, law or means stays pickable: `requires: party nomination | without: approval` (stand as an
  independent, at a lower chance), never removed. Door options also carry `aims: <title>` (build.py accepts it), one or two per means color in the pack.
- Elections are won in the option's chance: the chance on an option that takes a seat is the real chance of winning it,
  for an ordinary candidate (council about 30 to 45, a parliamentary selection 15 to 25, a party candidate in a winnable
  seat 45 to 55, an independent 5 to 10, a mayoralty 25 to 35, the leadership 10 to 20, the country 30 to 45). The
  engine's earned-odds lifts (helps.py) raise it for the prepared and the timely; never write it higher.
- Keep politics realistic and unglamorous where it is: most of it is casework, meetings, leaflets, rotas and small
  compromises; a defeat is common and survivable; winning office brings new duties and strains on old ties (a partner,
  friends, the day job), not a finish line.
- Wrongs are pickable with plain labels and no preaching: a smear, a leak, a bribe, a donor's favour, a broken promise,
  padded expenses, a lie to the house, a fixed selection. Mark them (hid a wrong, broke your word, gave in to pressure)
  and give a closed: line with a real backfire (a scandal, a lost whip, the police, a lost seat). Integrity belongs to
  every color, and so does corruption: a White member can bend a rule for the party, a Black one can keep every promise.
- No ideology on the page. Moments never name a real party, country, leader or side of a real debate; the person's cause
  is "the cause", the bill is "the bill", the other side is "the other side". A Green conservative of the land, a Red
  radical, a Blue technocrat, a White institutionalist and a Black power-broker are all honest politicians.
- Every color gets its strong, honest acts as well as its risky ones: Red's courage, conviction and warmth on the
  doorstep; Black's effort, ambition and deal-making that gets things built; Green's loyalty to a place; Blue's mastery
  of the brief; White's duty and fairness. Not only the outburst or the scheme.
- Content limits (Emren's rules): no sexual violence and no harm to children as pickable acts (at most an indirect
  mention, as someone's past); nothing graphic (a riot, an attack on a member or a war stays offstage and plain). A
  threat to a politician may be mentioned, never shown.
- Role slots only from the spec ({boss} {colleague} {mentor} {rival} {friend} {partner} {elder} {place} ...). The
  leader, a whip or the chair of the branch is {boss}; an opponent is {rival}; a fellow member is {colleague}; a
  constituent or a donor is a stranger named in words.
- Pair halves: an everyday pair is two consecutive moments with the same stages, age window, holds: and rate, and calls
  that split the five colors 2 and 3. Life events listed together below share stages and use the two halves of the same
  combination line, so the pack stays even in every stage.
- Worlds (Emren, 21:37). Every moment carries a situation-level earth: line and also tribal: and magic: lines, in the
  forms worlds.py gives (the council fire, the head of the camp, the great gathering, the chief; the guild council, the
  burgomaster, the Assembly of the realm, the councillors of the Crown and of the Orders, the Chancellor). An option
  whose act reads differently in a world adds its own tribal: or magic: wording. A moment that belongs to one world only
  is marked `only: magic` or `only: tribal` and has that world's line alone. Supernatural ways into and out of power are
  possible sometimes in the magic world (an oracle's sign, a spirit's favour, a binding oath, a bargain with something
  old, a rival's curse), always as one choice among ordinary ones, never forced; magic acts need an awakened gift, as
  the Library's rules say. Modern Earth has no magic.
- Frequency (game thread: the Book of Moments stars rare moments). Every moment, of every tier (everyday, life event,
  echo, read, inner and season), carries a `times:` line in words, copied from the "times N:" line under it below: how
  often the people who can meet it meet it, how rare it is across all lives where that helps (from the catalogue
  shares), and a source or "(estimate)", in the style of the `times:` lines in science/science-events.lib. Adjust the
  words if the moment changes, never the figures without a source.

## Part 1: doors and hooks (file politics-doors.lib)

Everyday pair A (no holds; stages juvenile+; age 14-90; rate 0.3; cycle s1):
1. `leaflets to deliver before Saturday` (calls WG). A local candidate's team is short of hands for the last streets.
   Doors: `title: campaign volunteer` on two or three options of fitting colors, `title: party member` on one (B or U
   means); others decline, bring a friend, deliver half and bin the rest (closed: approval; backfire: a neighbour sees).
   earth: a candidate's team leaves a box of leaflets and a map of streets at the door.
   tribal: a speaker's kin ask for someone to walk to the far hearths and speak for him before the gathering.
   magic: a faction's herald needs broadsheets carried through the lower wards before the lots are cast.
   times 1: per person a year: about 8 in 100 teenagers and adults are asked to help a local campaign in a year with an election, fewer in other years; about 3 to 4 US adults in 100 do campaign work in an election year (ANES), and about 8 lives in 100 volunteer at some point (catalogue share; estimate)
2. `poll workers wanted for election day` (calls UBR). A notice from the town hall: a long paid day at the polling
   station, training on Tuesday. Doors: `title: polling-station volunteer` on several options (its profiles cover all
   colors); others pass, take it for the fee, offer to drive voters instead.
   earth: the council needs clerks for the polling stations, a fee and a fifteen-hour day.
   tribal: the elders need someone with a clear head to keep the counting stones at the gathering.
   magic: the Order asks for witnesses at the warded urns, under its seal, for a day's silver.
   times 2: per adult a year: about 3 in 100 see a call for polling-station staff they could answer; the US staffed about 774,000 poll workers in 2020 (Pew Research Center 2024), and about 3 lives in 100 work a polling station at some point (catalogue share; estimate)
Everyday pair B (holds: party member | activist in a cause | union rep | campaign volunteer | residents' committee
member; stages young_adult adult mature elder; age 18-85; rate 0.3; cycle s2):
3. `the ward needs a candidate` (calls BR). The branch, the street or the cause has nobody to stand in the ward. Doors:
   `title: council candidate` on several options; `grants: party nomination` with
   `requires: party member | without: approval` (otherwise stand as an independent); `title: local party officer`
   (requires: party member) for the one who would rather run the branch; others nominate a friend, refuse.
   earth: the council elections are in May and the ward has no candidate.
   tribal: the band will choose who speaks at the council fire this winter, and no one from your hearths has asked.
   magic: a seat on the town council falls open, and the faction has no one to put up for it.
   times 3: per party member, activist, union rep, campaign volunteer or residents' committee member a year: about 5 in 100 young adults, 8 in 100 adults and 10 in 100 in midlife and old age are asked, or see the chance, to stand for a local seat; England has about 17,000 principal and 100,000 parish councillors (LGIU, NALC), many parish seats go uncontested, and about 3 lives in 100 stand for a local seat at some point (catalogue share; estimate)
4. `a paid job on the campaign` (calls WUG). Six weeks of paid work, then perhaps more. Doors:
   `title: campaign organiser`; `title: constituency caseworker`; `title: political adviser` with
   `requires: graduate | without: approval`; `title: pollster` with `requires: working with data | without: means`;
   others keep the day job.
   earth: a campaign needs paid staff for six weeks, and someone has passed your name on.
   tribal: a speaker who wants to be chief needs someone to walk the valley for him all summer, fed at his fire.
   magic: a faction's house hires clerks and runners for the season of the lots, with board and a wage.
   times 4: per party member, activist, union rep, campaign volunteer or residents' committee member a year: about 3 in 100 young adults, 2 in 100 adults and 1 in 100 in midlife hear of paid campaign or office work they could take, most of it in big election years; about 1 life in 500 works a paid campaign and 1 in 330 as an adviser (catalogue shares; estimate)
Echoes (stages young_adult+; five one-color options plus one full cross cycle):
5. `the fight that made you want to stand` (cycle s3; after: 'your town faces a change you could fight', 'a protest to
   save the local hospital', 'a sense of injustice', 'a bitter election' or 'they ask you to lead because you stood up
   once' within the last three years; no office held; delay 0-3). Doors: `title: council candidate`,
   `title: party member` (B or U means), `title: campaign volunteer`, `grants: a movement behind you`, or letting it
   rest.
   earth: the fight you lost or won still makes you angry, and the next election is close.
   tribal: the quarrel at the fire is over, but you keep thinking you could have spoken for the band yourself.
   magic: the guild's ruling still stings, and the town council will sit again in spring.
   times 5: per person who met a local fight, a protest, an injustice or a bitter election in the last three years: about 1 in 10 feel the pull to stand in the years after; many councillors say a local fight first brought them in (estimate)
6. `the debate you never forgot` (cycle s4; after: 'a debate or contest at school' or 'defending a speaker you cannot
   stand' as a teenager; now an adult with time; delay 8-30). Doors: `title: party member`, `title: campaign volunteer`,
   `title: council candidate`, `title: political adviser` (requires: graduate | without: approval), `grants: debating`,
   or letting it rest.
   earth: a television debate reminds you of the school debate you won, or lost, years ago.
   tribal: an argument at the fire stirs the memory of the first time you stood up to speak as a child.
   magic: a disputation in the market square takes you back to the academy's debating hall.
   times 6: per person who debated at school or defended a speaker as a teenager: about 1 in 20 come back to it as adults, ten to thirty years later (estimate)

## Part 2: life on the main rungs (file politics-rungs.lib)

One everyday pair per title, holds: that title, rate 0.5, stages from the title's ages. First moment from the title's
turning point in the catalogue, second another ordinary moment of the role. Options may carry `drops:` (leaving the
role), `grants:` (a perk plainly earned, such as `grants: coalition building`), `takes:` and a plain `title:` step.
The world lines of a pair give both moments, the first before the slash and the second after it; the times lines come
one per moment. Part 3 follows the same layout; in part 5 a season's world lines set the scene for its four moments.
7-8. party member (s3; calls WB / URG; young_adult adult mature elder; age 16-95): `the branch meeting runs late` (a
   motion on the local hospital, two hours of procedure; options: speak, stay quiet, walk out,
   `title: local party officer`, `grants: knowing the rules of the house`); `the party changes its line` (the leadership
   drops a promise the member joined for; stay and fight, stay quiet, `drops: party member`, join the rebels).
   earth: a branch meeting above a pub / a policy shift announced on the news.
   tribal: the faction's elders talk late at the fire / the faction makes peace with the family it swore against.
   magic: the faction's ward meeting in a back room of the guild hall / the faction takes the Order's side.
   times 7: per party member a year: an active member sits through a long branch meeting several times a year, though fewer than half of members ever attend one; about 6 lives in 100 belong to a party at some point (catalogue share; estimate)
   times 8: per party member a year: about 1 in 10 see the leadership drop or reverse a promise they joined for; it comes with most new leaders and most manifestos (estimate)
9-10. local councillor (s4; calls UR / WBG; young_adult adult mature elder; age 18-90):
   `the planning committee and the field` (houses on the last green field of the ward: vote with the officers, with the
   residents, against the party; `grants: coalition building`, `grants: a reform with your name on it` at a low chance);
   `a knock at the door at ten at night` (a resident with a crisis at the door: help now, refer, set a surgery,
   `grants: constituency casework`).
   earth: the planning application for the field / a constituent on the doorstep after dark.
   tribal: the band wants to move camp onto the old burial ground / a family comes to your hearth at night with a feud.
   magic: a guild wants the common meadow for its new hall / a petitioner at the door after the curfew bell.
   times 9: per local councillor a year: a contested planning vote comes several times a year, a big one on a green field every few years; about 1 life in 100 sits on a council (catalogue share; about 117,000 councillors in England, LGIU and NALC)
   times 10: per local councillor a year: most councillors are approached at home by a resident in trouble a few times a year (estimate)
11-12. campaign organiser (s1; calls BG / WUR; young_adult adult mature; age 18-70):
   `forty volunteers and one weekend left` (the catalogue's turning point: the target lists say the ward is lost);
   `the candidate goes off script` (a gaffe on camera at noon: spin, own it, hide the candidate, quit;
   `grants: handling the press`).
   earth: a campaign office with a whiteboard of streets / a clip spreading on phones.
   tribal: a dozen young hunters to send to the far bands before the gathering / the speaker insults a rival clan's
   elder.
   magic: forty runners and a single day before the lots / the candidate mocks the Order in the square.
   times 11: per campaign organiser: once or twice a campaign the volunteers and the days run short of the target; about 1 life in 500 works as a paid organiser (catalogue share; estimate)
   times 12: per campaign organiser: about one campaign in three has a candidate's slip that spreads (estimate)
13-14. political adviser (s2; calls WR / UBG; young_adult adult mature; age 20-75):
   `news the boss does not want to hear` (the night before the big announcement: tell it straight, soften it, bury it,
   leak it; `grants: a name for straight talk`); `a briefing off the record` (a journalist wants the line: brief,
   refuse, brief against a rival (closed: approval; backfire: traced), `grants: handling the press`).
   earth: an evening in the office before the announcement / a journalist on the phone.
   tribal: the speaker means to promise the hunt's share away tomorrow / a singer wants to know what the speaker really
   thinks.
   magic: the councillor will read a decree at dawn that you know is flawed / a broadsheet writer asks for the inside
   story.
   times 13: per political adviser a year: several times a year an adviser holds news the boss will not like; about 1 life in 330 works as an adviser or staffer (catalogue share; estimate)
   times 14: per political adviser a year: advisers who deal with the press are asked for an off-the-record line most weeks, a hard one against a colleague a few times a year (estimate)
15-16. mayor (s3; calls UG / WBR; young_adult adult mature elder; age 21-95): `a developer offers the town a stadium`
   (the turning point: the price is the old park; options include `grants: a reform with your name on it` at a low
   chance and a kickback (closed: law; backfire: arrested)); `the bins have not been collected` (a strike, a heatwave, a
   town that blames the mayor).
   earth: the stadium deal on the council table / rubbish piling up in the high street.
   tribal: a neighbouring clan offers to build a great fish weir if the band gives up its spring hunting ground /
   the camp's middens overflow and the families quarrel over whose turn it is.
   magic: a merchant house offers a new market hall if the town gives up the old grove / the city's refuse-golems stop
   working, or the carters strike.
   times 15: per mayor a year: about 1 in 10 face a big development offer that splits the town; about 1 life in 500 is a mayor (catalogue share; a mayor for each of 34,875 French communes, DGCL 2025, and about 19,500 US municipalities; estimate)
   times 16: per mayor a year: a failure of a basic service that the town blames on the mayor comes most years (estimate)
17-18. member of parliament (s4; calls WU / BRG; young_adult adult mature elder; age 18-95):
   `the queue at the Friday surgery` (the advice session in the constituency: the cases nobody else will take;
   `grants: constituency casework`); `the whip on the phone` (the catalogue's turning point: vote for a bill the
   constituency hates; vote with the party, rebel, abstain, trade the vote; `takes_if_fails: the party whip` on the
   rebel option, `grants: knowing the rules of the house`).
   earth: a library meeting room on a Friday / the whip's call on the train.
   tribal: the families line up at your hearth when you come back from the gathering / the faction head tells you how
   to speak at the gathering.
   magic: petitioners in your town house on the weekly day / the faction's warden comes with the line for tomorrow's
   vote in the Assembly.
   times 17: per member of parliament: most weeks; members hold advice surgeries in the constituency most Fridays; about 1 life in 10,000 sits in parliament (House of Commons, ONS: about 70 new members a year against about 650,000 UK births)
   times 18: per member of parliament a year: a whipped vote the member dislikes comes several times a year, a hard one against the constituency about once a year (estimate)
19-20. minister (s1; calls UB / WRG; adult mature elder; age 21-95): `the officials say it cannot be done` (the policy
   the minister promised meets the department; press on, listen, find another way, overrule;
   `grants: officials who trust you`); `defending a policy you argued against` (the turning point: collective
   responsibility in the chamber; defend it, resign, defend it badly, leak your doubts (closed: approval)).
   earth: a meeting room in the department / the despatch box.
   tribal: the old hands say the hunt cannot be moved before the herds pass / the chief chose the war you argued
   against,
   and you must speak for it.
   magic: the clerks of the Treasury say the coffers cannot bear it / the throne's decree goes against your counsel, and
   you must read it in the Assembly.
   times 19: per minister a year: several times a year; about 1 life in 30,000 becomes a minister (catalogue share; Institute for Government: 120 paid ministers at a time; estimate)
   times 20: per minister a year: about 1 in 3 must defend in public a policy they argued against in private; collective responsibility binds every minister (estimate)
21-22. party leader (s2; calls RG / WUB; adult mature elder; age 25-95): `the party at war with itself` (the turning
   point: two wings, one leader; choose, unite, purge, delay); `the speech at the party conference` (the year's speech:
   `grants: a following in the party`, `grants: rousing a crowd`).
   earth: two wings briefing against each other / the conference hall.
   tribal: two family lines in the faction will not sit at the same fire / the great feast where the faction head
   speaks.
   magic: two houses of the faction draw blades in the Assembly's yard / the faction's midwinter oration.
   times 21: per party leader a year: about 1 in 3 face open war between the wings of the party; about 1 life in 200,000 leads a national party (catalogue share; estimate)
   times 22: per party leader: once a year, at the party conference (estimate)
23-24. head of government (s3; calls WG / UBR; adult mature elder; age 30-95): `the call at three in the morning` (the
   turning point: a decision that cannot wait for cabinet); `a decision nobody else can take` (a slow, divisive choice:
   consult, decide alone, delay, put it to the people).
   earth: a phone by the bed / a long table with the cabinet.
   tribal: a runner at dawn with news of raiders / whether the clans move to the coast before winter.
   magic: a warden at the Chancellor's door before dawn / whether to open the old gate the Orders keep shut.
   times 23: per head of government a year: several times a year a crisis needs a decision at night; about 1 life in two to three million heads a government (catalogue share; the UK has had 17 prime ministers since 1945)
   times 24: per head of government a year: about once or twice (estimate)

## Part 3: side roads and community rungs (file politics-roads.lib)

As part 2, one everyday pair per title, holds: that title, rate 0.5.
25-26. constituency caseworker (s4; calls BR / WUG; young_adult adult mature; age 18-75):
   `a family about to lose their home` (an eviction on Monday: phone the landlord, the council, the press, the member;
   `grants: constituency casework`); `the same case for the third time`.
   earth: an eviction notice on the desk / the same name in the inbox again.
   tribal: a family the band means to drive out over a feud / the same widow at the fire with the same grievance.
   magic: a family to be thrown out of their tenement by the guild / the same petition, back again with a new seal.
   times 25: per constituency caseworker a year: a housing case most weeks, an eviction at short notice every month or two; about 1 life in 1,000 works as a caseworker (catalogue share; estimate)
   times 26: per constituency caseworker: most months (estimate)
27-28. party official (s1; calls WB / URG; young_adult adult mature; age 20-75):
   `the leadership wants its favourite selected` (the rules say an open selection; keep the rules, bend them, fix it
   (closed: approval), warn the branch); `the party is broke after the election` (cut staff, cut yourself, find a donor,
   `grants: fundraising`).
   earth: an email from headquarters / a meeting about the overdraft.
   tribal: the faction head wants his nephew sent to the gathering / the faction's stores are gone after the feasting.
   magic: the faction's lord wants his favourite on the lot / the faction's coffer is empty after the lots.
   times 27: per party official a year: about 1 in 5 meet a selection the centre wants to steer; about 1 life in 2,000 works for a party (catalogue share; estimate)
   times 28: per party official: after most lost elections, about one year in four, money and staff are cut (estimate)
29-30. lobbyist (s2; calls UR / WBG; young_adult adult mature elder; age 22-80): `a client wants the minister by Friday`
   (the turning point: call in a favour, refuse, find another way; `requires: registered lobbyist | without: law` on the
   acts that contact office-holders); `an old colleague now decides` (a friend from the old office now holds the pen).
   earth: a client on the phone / a former colleague's name in the new appointments.
   tribal: the flint-traders want the chief's ear before the gathering ends / the hunter you grew up with is now the
   chief's speaker.
   magic: a merchant house wants the Keeper of the Treasury by the end of the week / your old fellow clerk is now a
   councillor of the Crown.
   times 29: per lobbyist a year: several times; about 1 life in 500 lobbies for a living (catalogue share; OpenSecrets: about 12,000 to 13,000 registered US federal lobbyists a year; estimate)
   times 30: per lobbyist a year: about 1 in 5 find a former colleague in a post that decides a client's case, most often after a change of government (estimate)
31-32. policy analyst (s3; calls BG / WUR; young_adult adult mature elder; age 21-85):
   `the report the funders will not like`; `a party takes your idea and twists it` (`grants: drafting policy`).
   earth: a draft report and a funder's email / your idea in a speech, turned inside out.
   tribal: the elders ask what happened the last time the band split, and the answer will anger them / a speaker
   uses your old story to argue the opposite.
   magic: the academy's patron dislikes your findings / a faction quotes your treatise to justify a decree.
   times 31: per policy analyst a year: about 1 in 5; about 1 life in 500 works as a policy analyst (catalogue share; estimate)
   times 32: per policy analyst a year: about 1 in 10 see an idea of theirs taken up and changed by a party (estimate)
33-34. speechwriter (s4; calls WR / UBG; young_adult adult mature elder; age 21-80): `the line the leader will not say`;
   `the speech is due at midnight` (`grants: writing speeches`).
   earth: a draft with one line struck out / an empty document at eight in the evening.
   tribal: the speaker refuses the words you gave him for the gathering / the gathering is at dawn and the words are not
   ready.
   magic: the lord strikes your best line / the oration is at the morning bell.
   times 33: per speechwriter a year: several times; about 1 life in 5,000 writes speeches for a living (catalogue share; estimate)
   times 34: per speechwriter: most months (estimate)
35-36. pollster (s1; calls UG / WBR; young_adult adult mature elder; age 21-80):
   `the poll that says your client is losing` (report it straight, soften it, bury it, leak it;
   `grants: reading the polls`); `the night the exit poll lands`.
   earth: a poll on the screen / the studio on election night.
   tribal: you have listened at every hearth and the speaker will not be sent again / the gathering casts its pebbles.
   magic: the tallies show your patron's faction falling / the night the urns are opened.
   times 35: per pollster a year: about 1 in 2 deliver numbers a client does not want, in any year with an election; about 1 life in 2,000 works as a pollster (catalogue share; estimate)
   times 36: per pollster: once a national election, about every four years (estimate)
37-38. campaign volunteer (s2; calls WU / BRG; stages juvenile+; age 14-100): `a door slammed in your face` (`grants:
   canvassing`); `the candidate remembers your name`.
   earth: a doorstep on a wet evening / a handshake at the count.
   tribal: a hearth that turns its back on your speaker / the speaker greets you by name at the fire.
   magic: a door shut in your face in the lower wards / the candidate calls you by name in the square.
   times 37: per campaign volunteer: several times on any evening of canvassing; about 8 lives in 100 volunteer (catalogue share; estimate)
   times 38: per campaign volunteer: once or twice a campaign (estimate)
39-40. polling-station volunteer (s3; calls UB / WRG; stages young_adult+; age 16-95): `a voter not on the list` (follow
   the rules, bend them, call the supervisor); `the count runs past midnight`.
   earth: a polling station in a school hall / the count in a sports centre.
   tribal: a stranger from another band wants to cast a pebble / the counting goes on by firelight.
   magic: a voter with no seal wants a lot / the urns are counted under the Order's lamps until dawn.
   times 39: per polling-station volunteer: on most election days at a busy station; about 3 lives in 100 work a polling station (catalogue share; estimate)
   times 40: per polling-station volunteer who stays for the count: at most national counts (estimate)
41-42. local party officer (s4; calls RG / WUB; stages young_adult+; age 16-100): `the annual meeting nobody comes to`
   (stand for chair, keep the minutes, close the branch, bring new people); `two members want the same nomination`
   (`grants: counting the votes`).
   earth: six people in a cold church hall / two friends after the same council seat.
   tribal: few families come to the faction's fire / two of the faction's young want to be its voice at the fire.
   magic: an empty back room in the guild hall / two members want the faction's seal for one seat.
   times 41: per local party officer: once a year; many branches struggle to reach a quorum outside election years; about 1 life in 100 holds a local party office (catalogue share; estimate)
   times 42: per local party officer a year: about 1 in 5, most of all in the year before local elections (estimate)

## Part 4: crossings, campaigns, office, falls and reach (file politics-events.lib)

Life events: stakes 1, alpha even, the five one-color options plus one balanced combination set (library-spec section
3); per_year is the yearly rate per eligible person (the holds: title or perk), with times:, likelier:, rarer: and
drivers: in words as in the example (the drivers the windows in helps.py name). Each line names the set to use; events
listed together share stages (young_adult adult mature elder unless named) and use the two halves of the line.

Crossings:
43. `polling day in the ward` (holds: council candidate; D1a pairs; per_year about 2, once per candidacy). The last day:
   knock until the polls close, drive voters in, a last leaflet with a smear (closed: law; backfire: a complaint to the
   police), stay home and trust the work, demand a recount. `title: local councillor` on most options at chance 30 to 45
   (see the pack rules); `grants: a loyal campaign team`, `grants: a list of supporters`.
   earth: polling day, from the first voter at seven to the count after ten.
   tribal: the night the band speaks at the council fire and says who will be heard.
   magic: the day the town council's lots are cast in the warded urns.
   times 43: per council candidate: once a candidacy; about 3 lives in 100 stand for a local seat at some point (catalogue share), and about 1 candidate in 3 wins (estimate from about three candidates for each principal seat in England)
44. `a seat falls vacant` (holds: local councillor | mayor | political adviser | party official | campaign organiser |
   union rep; D1b pairs; per_year about .05; drivers: era+, unrest+). Seek the nomination for parliament:
   `grants: party nomination; title: parliamentary candidate` on options at chance 15 to 25; stand as an independent
   (`title: parliamentary candidate`, no nomination); back a friend; stay local.
   earth: the member for the seat stands down, and the selection is in six weeks.
   tribal: the band's speaker to the gathering has died, and the families must send another.
   magic: a seat in the Assembly falls open, and the faction will choose its candidate at the new moon.
   times 44: per local councillor, mayor, political adviser, party official, campaign organiser or union rep a year: about 3 in 100 young adults, 6 in 100 adults, 5 in 100 in midlife and 1 in 100 elders see a parliamentary selection they could enter; about 70 UK seats a year get a new member (House of Commons), and a selection for a winnable seat is won about 1 time in 5 (estimate)
45. `election night` (holds: parliamentary candidate; D2a pairs; per_year about 1). `title: member of parliament` on
   options at chance 45 to 55 with `requires: party nomination | without: approval` (an independent wins at 5 to 10);
   concede, call a recount, celebrate, thank the team (`grants: a loyal campaign team`).
   earth: the count in a sports hall, and the returning officer at the microphone.
   tribal: the great gathering, where the bands stand behind the speakers they choose.
   magic: the night the Assembly's urns are opened in the city square.
   times 45: per parliamentary candidate: once a candidacy; 4,515 candidates stood for 650 seats in 2024 (House of Commons), so about 1 in 7 wins, and about 1 in 2 of those picked for a winnable seat; about 1 life in 1,000 stands for parliament (catalogue share; estimate)
46. `the town needs a mayor` (holds: local councillor; D2b pairs; per_year about .04). `title: mayor` at chance 25 to
   35; back another, stay a councillor, a deal for the deputy post.
   earth: the mayor stands down and the council, or the town, must choose.
   tribal: the head of the camp is too old to lead the moves, and the band looks for another.
   magic: the burgomaster dies in office, and the town council must choose before the fair.
   times 46: per local councillor a year: about 2 in 100 young adults, 4 in 100 adults and in midlife and 2 in 100 elders; about 1 councillor in 5 becomes a mayor or council leader at some point, about 1 life in 500 (catalogue share; estimate)
47. `the phone call from the leader` (holds: member of parliament; D3a pairs; stages adult mature elder; per_year about
   .06, much higher when a new government forms). `title: minister` on accepting (chance 85 to 90), on bargaining for a
   bigger post (chance 40), on asking for a post that fits (chance 70); refuse to stay free.
   earth: the leader's office calls on reshuffle day.
   tribal: the chief calls you to his fire and asks you to keep the peace with the river clans.
   magic: a sealed letter: the throne would have you as a councillor of the Crown.
   times 47: per member of parliament a year: about 6 in 100, many more in the year a new government forms; about 1 member in 3 ever holds office (Institute for Government: 120 paid ministers at a time; estimate)
48. `the leadership falls vacant` (holds: member of parliament | minister; D3b pairs; stages adult mature elder;
   per_year about .03). `title: party leader` at chance 10 to 20 with
   `requires: known across the country | without: approval`; back a rival for a post (`title: minister`), run to make a
   point, stay out.
   earth: the leader resigns after a defeat, and nominations close on Friday.
   tribal: the faction head has fallen in a hunt, and the families will choose who leads them to the gathering.
   magic: the head of the faction steps down, and the houses will choose a new one at midsummer.
   times 48: per member of parliament or minister a year: about 3 in 100 adults, 4 in 100 in midlife and 2 in 100 elders see the leadership of their party open; most parties change leader every four to six years, and only those known across the country have a real chance (estimate)
49. `the country goes to the polls` (holds: party leader; D4a pairs; stages adult mature elder; per_year about .25).
   `title: head of government` at chance 30 to 45; `grants: a household name` on a win; concede, form a coalition
   (`grants: coalition building`), fight on.
   earth: a general election campaign, with the leader's face on every screen.
   tribal: the great gathering will choose a chief of the clans for the hard years ahead.
   magic: the throne will name its Chancellor from the faction that wins the Assembly.
   times 49: per party leader: about once in four years; the leader of one of the two largest parties wins about 1 time in 2, a smaller party's almost never; about 1 life in two to three million heads a government (catalogue share; estimate)
50. `leaving politics for another life` (holds: member of parliament | political adviser | mayor | campaign organiser;
   D4b pairs; stages adult mature elder). `title: lobbyist` (requires: a parliamentary pass | without: approval),
   `title: policy analyst`, `title: speechwriter`, `drops: member of parliament` for family, a base career, or stay.
   earth: an offer from a firm, a partner who wants their life back, a seat that feels like a cage.
   tribal: the hunt, the family and the quiet of one camp call louder than the gathering.
   magic: a merchant house offers you a fortune to plead its case instead.
   times 50: per member of parliament, political adviser, mayor or campaign organiser a year: about 5 in 100 adults, 7 in 100 in midlife and 10 in 100 elders weigh leaving for another life; more UK members leave by standing down than by defeat in most elections (estimate)
Campaigns (holds: council candidate | parliamentary candidate):
51. `the hustings in the church hall` (D5a pairs). A public debate with every candidate: `grants: debating`,
   `grants: rousing a crowd`, a cheap shot (closed: approval), a straight answer (`grants: a name for straight talk`).
   earth: a church hall, a moderator and a hundred folding chairs.
   tribal: the candidates speak in turn at the fire, and the elders ask the hard questions.
   magic: the candidates dispute on the steps of the guild hall.
   times 51: per candidate: once or twice a campaign for a parliamentary candidate, for about 1 council candidate in 3 (estimate)
52. `the money runs short three weeks out` (D5b pairs). `grants: fundraising`, `grants: a campaign war chest`, put in
   your own savings, take money that breaks the spending rules (closed: law; backfire: the campaign fined, the seat
   lost), `grants: donors`.
   earth: the campaign account is nearly empty three weeks before polling day.
   tribal: the stores for the speaker's feast are nearly gone, and the gathering is a moon away.
   magic: the coffer is empty, and the heralds want paying before the lots.
   times 52: per candidate: about 1 campaign in 2 runs short in the last weeks (estimate)
53. `a file on your opponent` (D6a pairs, all enemy). Someone brings dirt on the {rival}: use it, leak it anonymously
   (mark hid a wrong; closed: approval; backfire: traced back), refuse it, check it first, warn the rival.
   earth: an envelope of documents about the other candidate.
   tribal: a woman tells you the rival's speaker once broke a hunting oath.
   magic: a sealed packet of letters that would ruin your rival, if they are real.
   times 53: per candidate: about 1 campaign in 10 is offered damaging material on a rival, more in close races (estimate)
In office (holds: member of parliament | local councillor):
54. `a vote against your conscience` (D6b pairs, all ally). The party wants the vote; conscience says no: rebel
   (`takes_if_fails: the party whip`; mark defied an authority), abstain, vote with the party (mark gave in to
   pressure), win a concession (`grants: counting the votes`).
   earth: a division bell, and a bill you think is wrong.
   tribal: the faction will stand behind a raid you think will bring a blood feud.
   magic: the faction will vote to hand the old forest to the Order, and you know what lives there.
   times 54: per member of parliament or local councillor a year: about 1 in 4; party discipline makes most members vote against their own view now and then (estimate)
55. `the count goes against you` (tier: read; holds: council candidate | parliamentary candidate; stages young_adult
   adult mature elder; source: community; base: need:belonging-.04): five readings of a defeat, each with impact, also
   and say, as in the read example: a duty done (the voters decided, and that is the point), a lesson (the numbers show
   where it went wrong), a waste (years and money thrown away), a heartbreak, the way things are (this place has always
   voted that way).
   earth: the returning officer reads out the numbers, and yours is not the highest.
   tribal: the band stands behind another, and you are left by the fire.
   magic: the urns are opened, and the lots favour your rival.
   times 55: per candidate who loses: once a defeat; most candidates lose (4,515 candidates for 650 seats in 2024, House of Commons), about 2 council candidates in 3 and 6 parliamentary candidates in 7 (estimate)
56. `a deal to get it through` (holds: member of parliament | local councillor | mayor | minister; D1a triads). A
   coalition partner wants a price for the votes: pay it, split the bill, go to the other side, give up.
   `grants: coalition building`, `grants: a reform with your name on it` at a low chance (10 to 15),
   `grants: friends across the aisle`.
   earth: a hung chamber and a bill with your name on it.
   tribal: the river clans will stand with the band at the gathering if it shares the salmon pools.
   magic: the Order of the Tower will lend its votes if the decree exempts its lands.
   times 56: per member of parliament, local councillor, mayor or minister a year: about 1 in 4 where no party holds a majority, about 1 in 20 where one does (estimate)
57. `the constituency wants one thing, the party another` (holds: member of parliament | local councillor; D1b triads).
   A factory, a road, a closure: the place against the line.
   earth: a closure the party backs and the town hates.
   tribal: the faction wants the band to move north; your own hearths want to stay by the lake.
   magic: the faction backs the new road through the ward you speak for.
   times 57: per member of parliament or local councillor a year: about 1 in 5 (estimate)
Falls (stages young_adult adult mature elder unless named):
58. `a donor wants a favour` (holds: donors | a campaign war chest; D2a triads). A contract, a permit, a word in the
   right ear: refuse (`takes: donors`), do it (mark hid a wrong; closed: law; backfire: the police, a scandal), report
   it, trade something lawful.
   earth: a dinner, and a question about a planning permit.
   tribal: the family that gave most to your feast wants the best hunting ground.
   magic: a merchant prince who filled your coffer wants the harbour licence.
   times 58: per person with donors or a campaign war chest a year: about 1 in 10 are asked for something in return; most ask for access, a few for something unlawful (estimate)
59. `a scandal breaks` (holds: member of parliament | minister | mayor | local councillor | political adviser; D2b
   triads; tone trouble; per_year about .02). Expenses, a lie, an old photograph, a friend's deal: resign (`drops:` the
   office held), own it and stay, blame staff (closed: approval), ride it out, deny it (mark hid a wrong). Several
   options carry `grants_if_fails: known across the country` (the story reaches every paper).
   earth: the story is on the front page in the morning.
   tribal: the singers make a mocking song about you, and every band hears it.
   magic: the heralds cry it in every square by noon.
   times 59: per member of parliament, minister, mayor, local councillor or political adviser a year: about 2 in 100; about 1 member in 5 meets a public scandal over a career, from expenses to conduct (estimate)
60. `the reshuffle` (holds: minister; D3a triads; stages adult mature elder; per_year about .3). Moved, sacked or kept:
   accept a lesser post, `drops: minister` with grace, resign in protest, plead, brief against the leader (closed:
   approval; backfire: the whip taken), `takes: allies in the party` on some.
   earth: the call on reshuffle day that does not go the way you hoped.
   tribal: the chief gives your duty to another speaker.
   magic: the throne recalls your seal of office.
   times 60: per minister a year: about 1 in 3 are moved, sacked or kept at a reshuffle; UK ministers stay in one post for about two years on average (Institute for Government; estimate)
61. `the night you lose the seat` (holds: member of parliament; D3b triads; stages adult mature elder; per_year about
   .06). At the top of the moment `drops: member of parliament` and `title: former member of parliament` (it happens
   whatever is chosen); the options are the responses: concede with grace, blame the leader, start the comeback
   (`grants: party nomination` at a low chance), go back to the old career, take the offer (`title: lobbyist`).
   earth: the count, the cameras, and the other candidate's speech.
   tribal: the bands stand behind another speaker, and your place at the gathering is gone.
   magic: the urns turn against you, and your seat in the Assembly passes to another.
   times 61: per member of parliament a year: about 4 in 100 adults and in midlife and 3 in 100 elders lose the seat; in a landslide a party can lose a third or more of its members in one night (estimate)
62. `the party turns on its leader` (holds: party leader; D4a triads; stages adult mature elder; per_year about .15). A
   confidence vote: fight (chance 40), resign with dignity (`drops: party leader`), purge the plotters, strike a deal.
   earth: letters of no confidence and a vote on Tuesday.
   tribal: the families meet without you, and the faction's elders come to your fire.
   magic: the houses of the faction meet in secret to unseat you.
   times 62: per party leader a year: about 15 in 100; most leaders leave after a defeat or a revolt (estimate)
Reach:
63. `a speech that goes everywhere` (holds: member of parliament | mayor | local councillor | party leader | council
   candidate | parliamentary candidate; D4b triads; stages adult mature elder). `grants: known across the country` on a
   few options at chance 8 to 15 (realistic), `grants: rousing a crowd`, `grants: a following in the party`.
   earth: a speech filmed on a phone that the whole country shares by morning.
   tribal: words spoken at the fire that every band in the valley repeats by the next moon.
   magic: an oration the heralds carry to every city of the realm.
   times 63: per member of parliament, mayor, councillor, party leader or candidate a year: about 2 in 100 adults and in midlife and 1 in 100 elders give a speech the whole country shares; only a few in a hundred of those become known across the country by it (estimate)

## World-only moments (file politics-worlds.lib)

Life events like part 4 (stakes 1, alpha even, five one-color options plus one combination set; stages young_adult
adult mature elder), each pair using the two halves of one line, so each world stays even on its own. A supernatural
act is one choice among ordinary ones, never the only way; it carries a real price (a debt, a mark, a closed: line
with a backfire), and a magic act needs an awakened gift (`requires:` in words, as the Library writes it).
Tribal (the spirits and the shaman are part of how the band decides):
64. `an omen at the council fire` (`only: tribal`; holds: council candidate; D5a triads). A hawk drops a feather at your
   feet, or lightning strikes the far bank, as the band is choosing: claim the omen (`title: local councillor` at chance
   50), ask the shaman, refuse to lean on signs, make a sign of your own (mark hid a wrong; closed: approval; backfire:
   found out).
   tribal: as the band weighs who will be heard at the fire, a sign comes, and every face turns to you.
   times 64: per council candidate in the tribal world: about 1 candidacy in 10 meets a sign the band reads for or against the person (estimate)
65. `the spirits turn from the leader` (`only: tribal`; holds: mayor | member of parliament | party leader | head of
   government; D5b triads). A failed hunt or a sickness, blamed on the one who leads: perform the rite, step down
   (`drops:` the office held), blame a rival, lead a new hunt yourself.
   tribal: the herds have not come, the children are sick, and the band whispers that the spirits have turned from you.
   times 65: per head of the camp, speaker, faction head or chief in the tribal world a year: about 5 in 100, after a failed hunt or a sickness (estimate)
66. `the shaman reads your dream` (`only: tribal`; holds: party member | campaign volunteer | local councillor; D2a
   pairs). The shaman says your dream names you as the band's speaker: accept (`title: parliamentary candidate`), ask
   for a sign, refuse, pay the shaman to say it louder (closed: approval).
   tribal: you tell the shaman a dream of a great fire, and the shaman says it means the band will send you to the
   gathering.
   times 66: per faction member, hearth-walker or voice at the fire in the tribal world a year: about 1 in 100 (estimate)
67. `a feast to win the families` (`only: tribal`; holds: council candidate | parliamentary candidate | party leader;
   D2b pairs). Give away the stores of a season to win followers before the gathering: give it all (`takes: a campaign
   war chest`, `grants: a following in the party`), give a little, borrow from kin, refuse the custom.
   tribal: the gathering is a moon away, and the families will follow whoever feasts them best.
   times 67: per candidate or faction head in the tribal world: once a candidacy, before the gathering (estimate)
Magic (old powers; a gift may awaken):
68. `the oracle names you` (`only: magic`; holds: member of parliament | local councillor | mayor; D6a triads). An
   oracle's sign says you will rise: believe it (`title: minister` on one option at chance 25, for a member of the
   Assembly), seek its price first, tell the faction, refuse to be ruled by prophecy.
   magic: the oracle of the high tower speaks your name in front of the whole court.
   times 68: per member of the Assembly, town councillor or burgomaster in the magic world a year: about 1 in 100 (estimate)
69. `a bargain with something old` (`only: magic`; holds: parliamentary candidate | member of parliament | party leader;
   D6b triads). Something under the hill offers the seat or the faction for a price paid later: accept (`title: member
   of parliament` or `title: party leader`, chance 70; mark took a wild risk; binds), refuse, try to trick it (closed:
   impossible without an awakened gift), bind it with an oath, tell the Order.
   magic: in the barrow on the night before the lots, a voice offers you the Assembly, and asks for something later.
   times 69: per candidate, member of the Assembly or faction head in the magic world a year: about 1 in 200; most refuse, and few who accept are found out (estimate)
70. `a binding oath of office` (`only: magic`; holds: minister | mayor | head of government; D1a pairs). The oath binds
   by magic, so breaking it will have teeth: swear plainly, swear with a hidden reservation (closed: approval; backfire:
   the oath bites), ask for the words to be changed, refuse the office (`drops:` the office held).
   magic: the Order's mages bring the old oath of office, and the words burn as you read them.
   times 70: per councillor of the Crown, burgomaster or Chancellor in the magic world: once, on taking the office, where an Order keeps the old oath (estimate)
71. `a rival's curse` (`only: magic`; holds: member of parliament | minister | mayor | party leader; D1b pairs). A rival
   lays a curse, and the office begins to slip: seek a counter-charm, expose the rival to the Order, bear it, curse back
   (closed: law; backfire: the Order's court), resign (`drops:` the office held).
   magic: your voice fails in the Assembly three days running, and a hex-mark is found under your door.
   times 71: per office-holder in the magic world a year: about 1 in 100 (estimate)

## Part 5: threshold seasons for the big rungs (file politics-seasons.lib)

Emren chose a "threshold season" for every crossing (point 6): a few months of linked moments around the rite (the
crossing itself, the in-between, settling into the new life), the person more open to change, and one transforming
chance. Fields: `threshold: title:<name>` (a season that opens when that title is gained; engine 21:07), `step: 1 |
2 | 3`, `transform: yes`. The crossing life event of part 4 is the rite that opens the season. Every moment here is
`tier: inner` with `requires:` in words ("in the threshold season: within the first six months after taking the
title"), `likelier:` and `rarer:` in words, `holds: <that title>`, stakes .8, the title's stages and ages, alpha even
with the five one-color options plus one full cross cycle (cycles s1 to s4 used five times each over the file), and the
usual story fields. Emren's line is the heart of it: winning office changes duties and relationships (a partner who
sees less of them, friends who now want favours, a day job, the people who sent them), so each season has a moment
about who the person now answers to.

Five seasons, four moments each (step 1, step 2, step 2 with `transform: yes`, step 3):
72-75. local councillor (opened by `polling day in the ward`): `the first full council meeting` (1);
   `the casework that never stops` (2); `whose councillor you are` (2, transform: the ward, the party, the cause, the
   career, the neighbours); `a year on, the ward knows your name` (3).
   earth: the council chamber, a pile of reports, a phone that rings at dinner.
   tribal: a first winter as a voice at the fire; the families now bring their quarrels to your hearth.
   magic: the first sitting of the town council in the guild hall; petitions under the door.
   times 72: per new local councillor: once, in the first weeks after taking the title; about 1 life in 100 (catalogue share)
   times 73: per new local councillor: once, in the first months of the threshold season; about 1 life in 100 (catalogue share)
   times 74: per new local councillor: once in the threshold season, for most who are still open to change; about 1 life in 100 (catalogue share)
   times 75: per new local councillor: once, near the end of the first year; about 1 life in 100 (catalogue share)
76-79. mayor (opened by `the town needs a mayor`): `the chain of office` (1); `the day job or the town` (2: a big town
   needs a full-time mayor; options include `drops:` of the career title held); `the kind of mayor you will be` (2,
   transform); `the first budget passes` (3).
   earth: the chain, the office, the first budget.
   tribal: the first move of camp you lead; the hunt or the camp, you cannot do both.
   magic: the burgomaster's seal and keys; the old craft or the town.
   times 76: per new mayor: once, in the first weeks after taking the title; about 1 life in 500 (catalogue share; estimate)
   times 77: per new mayor: once, in the first months of the threshold season; about 1 life in 500 (catalogue share; estimate)
   times 78: per new mayor: once in the threshold season, for most who are still open to change; about 1 life in 500 (catalogue share; estimate)
   times 79: per new mayor: once, near the end of the first year; about 1 life in 500 (catalogue share; estimate)
80-83. member of parliament (opened by `election night`): `the first day in the chamber` (1); `the maiden speech` (2);
   `who you answer to` (2, transform: constituency, party, conscience, ambition, place; its acts carry identity and
   often binds); `a year on, the Thursday train home` (3; family and old friends after a year away all week).
   earth: the chamber, a desk shared with three others, a flat in the capital and a family at home.
   tribal: the first gathering as the band's speaker, far from your own hearth for a whole summer.
   magic: the first sitting of the Assembly; rooms in the capital and letters from home.
   times 80: per new member of parliament: once, in the first weeks after taking the title; about 1 life in 10,000 (House of Commons, ONS)
   times 81: per new member of parliament: once, in the first months of the threshold season; about 1 life in 10,000 (House of Commons, ONS)
   times 82: per new member of parliament: once in the threshold season, for most who are still open to change; about 1 life in 10,000 (House of Commons, ONS)
   times 83: per new member of parliament: once, near the end of the first year; about 1 life in 10,000 (House of Commons, ONS)
84-87. minister (opened by `the phone call from the leader`): `the first morning at the department` (1);
   `the brief you did not ask for` (2); `the decision that will carry your name` (2, transform;
   `grants: a reform with your name on it` at a low chance); `the department starts to trust you` (3;
   `grants: officials who trust you`).
   earth: a car at the door, a red box, and a department of thousands.
   tribal: the chief gives you one duty, and the old hands wait to see what you are.
   magic: the seal of an office of the Crown, and clerks who served ten councillors before you.
   times 84: per new minister: once, in the first weeks after taking the title; about 1 life in 30,000 (catalogue share; estimate)
   times 85: per new minister: once, in the first months of the threshold season; about 1 life in 30,000 (catalogue share; estimate)
   times 86: per new minister: once in the threshold season, for most who are still open to change; about 1 life in 30,000 (catalogue share; estimate)
   times 87: per new minister: once, near the end of the first year; about 1 life in 30,000 (catalogue share; estimate)
88-91. head of government (opened by `the country goes to the polls`): `the door closes behind you` (1);
   `a crisis in the first week` (2); `what this government is for` (2, transform); `the country gets used to your face`
   (3).
   earth: the famous door, the cameras, the first night in the official flat.
   tribal: the first council of the gathered clans with you at its head.
   magic: the Chancellor's chain, and a first audience at the foot of the throne.
   times 88: per new head of government: once, in the first weeks after taking the title; about 1 life in two to three million (catalogue share; estimate)
   times 89: per new head of government: once, in the first months of the threshold season; about 1 life in two to three million (catalogue share; estimate)
   times 90: per new head of government: once in the threshold season, for most who are still open to change; about 1 life in two to three million (catalogue share; estimate)
   times 91: per new head of government: once, near the end of the first year; about 1 life in two to three million (catalogue share; estimate)
The transform moment's options are the big forks of that season, each a real way of holding the new title (its
profiles in the catalogue): its acts carry `identity` and often `binds`. Steps 1 and 3 are lighter, with everyday-sized
stakes in the words.

## Balance layout (what keeps the pack even)

- Everyday pairs: 20 in all (2 doors, 9 main rungs, 9 side roads and community). Their two-color calls hold each of the
  ten color pairs exactly twice (WG, BR, WB, UR, BG, WR, UG, WU, UB, RG), and each pair's cross cycle rotates s1 to s4,
  five pairs per cycle.
- Echoes: two (5, 6), each even on its own with a full cross cycle (s3, s4).
- Life events (Earth and every world, 20): pairs D1 to D6, both halves (43 to 54), and triads D1 to D4, both halves (56
  to 63), so every pair appears six times and every triad four times, ally and enemy alike. The read event (55) is even
  on its own.
- World-only life events (8): tribal D5 triads and D2 pairs, both halves (64 to 67); magic D6 triads and D1 pairs, both
  halves (68 to 71). Each world's own set is even, so the pack is even in every world.
- Threshold seasons (20): five one-color options plus one full cross cycle each, the four cycles five times each.
- Chance: the mean chance per means color within 3 points overall and in every stage; mean chance about 68 to 72 for
  everyday and life events, 72 to 78 for echoes and season moments. Seats and posts carry their real chances (the pack
  rules above); balance them across colors inside each moment, so no color wins elections more easily.

In all: 91 moments planned (6 doors and echoes, 18 on the main rungs, 18 on the side roads and community rungs, 21
life events with one read event, 8 world-only events, 20 season moments).

## Balance and checks (each file must pass all three)

- Build: copy build.py to your scratch folder (it already accepts threshold:, step:, transform:, aims: and the
  *_if_fails act fields) and run `python3 -B build.py <yourfile>.lib --out <scratch>`; it must end with no layout
  problems. Also make sure no moment name or option label of yours appears in chroma-library/earth.py or in the other
  politics-*.lib and science-*.lib files (grep them).
- Chance and tags: `python3 /mnt/project-files/chroma-packs/tools/lib_stats.py <yourfile>.lib`: the mean chance per
  means color within 3 points overall and in every stage; tag counts (habit, door, identity, binds, self_control + and
  -) close to even per means color.
- Names: `python3 /mnt/project-files/chroma-packs/tools/check_pack.py politics` (it reports unknown title or perk names
  and checks the catalogue against this brief).

## Files and rules

- Write only your own file in /mnt/project-files/chroma-packs/politics/ (named in your task). Write moment by moment
  (append), so partial work survives. Re-read before writing; about ten seconds after writing, read it back and re-apply
  if another write replaced yours.
- Never write into chroma-library/, chroma-engine/, chroma-game/ or chroma-art/; read only. No packages; standard
  library only. Scratch goes in /tmp/claude-0/-home-claude/e40218c8-fe2b-58e7-bec9-a2e19282a5e8/scratchpad/<your part>/,
  never in /mnt/project-files. Run Python with PYTHONDONTWRITEBYTECODE=1 so no __pycache__ lands in the shared folder.
- Do not call any mcp__hearthbot__ tool; the thread's own session talks to Emren.

## Report back

The build line, the lib_stats output, the moment names, and anything in the seeds you changed and why.
