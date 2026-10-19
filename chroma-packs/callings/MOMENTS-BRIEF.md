# The Five Callings pack: brief for the moment writers (Pathways and packs thread, 2026-10-19)

Status: v24, switched off (`callings` is not in batch.PACKS). The plan: chroma-ideas/next-table-2026-10-19/plan.md,
section 5 ("Then the missing faces that keep each colour pair fair"); the Vision thread agreed the five single-colour
callings on 10-19 (12:04 UTC). The catalogue (titles and perks) is catalogue.py next to this file, the rules roles.py,
the earned odds helps.py, the other worlds worlds.py, the engine's conditions engine-conditions.py, the ladders
aims.py. Engine name: `callings`. Moment files: callings-*.lib in this folder, one per road.

The five roads, each a single colour's calling (a tendency, never a wall: every colour can walk every road):

| Road | Colour | Rungs (base titles in plain, the pack's in bold) |
|---|---|---|
| faith (callings-faith.lib) | W | ordained religious minister or member of a monastic community, then **senior cleric**, then **head of a faith order** (summit) |
| invention (callings-invention.lib) | U | software developer, civil engineer, machinist, electrician, apprentice or founder of a firm, then **inventor**, then **celebrated inventor** (summit facet on inventor) |
| business (callings-business.lib) | B | shop owner, founder of a firm, café or bar owner or shift manager, then **chief executive**, then **magnate** (summit facet on chief executive or founder of a firm) |
| command (callings-command.lib) | R | soldier (or graduate and the academy), then **army officer**, then **general** (summit facet on army officer) |
| healing (callings-healing.lib) | G | nurse or midwife, then **senior nurse or midwife**, then **renowned healer** (summit facet on senior nurse or midwife, nurse, midwife, physician or complementary therapist) |

## Read first (all paths under /mnt/project-files unless they start with /home)

- chroma-library/SPEC.md, sections "Balance layout (per moment)" and "Writing an option" (the layout, chance:, v:,
  flags, marks, self_control).
- chroma-library/notes/library-spec.md and chroma-library/notes/writer-brief.md (the format, colours tagged faithfully,
  story fields).
- The build.py header (chroma-library/build.py, lines 1 to 120: the fields, CYCLES, D and PAIRSETS).
- **The footprints brief: chroma-library/drafts/footprints-brief.md.** Every option of every life event (the steps, the
  falls and wrongs, the long shots and the world-only moments) leaves one or two footprints: the fields it already has
  (a mark the rules read, a bond, a title or perk given or taken, commit:, win:/lose:/pay:, back:) count, and an option
  with none gets `foot: <kind> <what>` just before `chance:`. A lesson only when nothing else fits, at most 1 in 5
  options of a moment, never the same lesson words twice in a moment. Everyday and echo moments need no foot:.
- The model, copy its shape exactly: the Art and Writing pack, chroma-packs/art/
  (art-rungs.lib and art-roads.lib for holder pairs, art-steps.lib for steps, art-events.lib for falls and wrongs,
  art-longshots.lib for long shots and their echoes, art-worlds.lib for world-only events) and its MOMENTS-BRIEF.md
  ("Pack rules", "Calibration lessons", "Balance layout"). Its life events now carry foot: fields too.
- This pack's catalogue.py, roles.py, worlds.py and aims.py (the forms below are worlds.py's summary).

## Pack rules (on top of the Library's)

- Every name in title:, drops:, grants:, takes:, suspends:, requires:, holds: and aims: is a title or perk in this
  pack's catalogue.py, chroma-packs/core/*.py, or the base catalogue chroma-library/earth_perks_titles.py. Exact names.
  holds: may name several with "|".
- A door is an option that takes a title by the act (`title: senior cleric`). Its means colour fits one of that title's
  three profiles (they cover all five colours, so a door can be honest in every colour). Holder pairs (everyday moments
  with holds:) use `aims:` and never give a new title; they may `grants:` a perk plainly earned and `drops:` the title
  held on the one act that truly ends it.
- **The summits are facets** (except the faith road's, which refines two titles). Write `title: celebrated inventor`
  for an inventor, `title: magnate` for a chief executive or a founder of a firm, `title: general` for an army officer,
  `title: renowned healer` for a senior nurse or midwife, nurse, midwife, physician or complementary therapist, and
  `title: head of a faith order` for a senior cleric or a member of a monastic community. For someone on the rung below
  without the career (a long shot that skips one rung), write the facet first: `title: celebrated inventor; inventor`.
- **Real chances** for an ordinary person who tries (the engine's earned-odds lifts in helps.py come on top; never write
  them higher): the senior post in a congregation 30; the order's headship 6; a prototype that works and makes a living
  25; an invention in every home 6; the board's choice of chief executive 25; a rival firm bought and an empire begun 6;
  officer selection passed 35; a general's post 6; the ward or birth centre to run 40; a healer known across the land
  6; long shots 2 to 5. Inside a moment, every colour that tries for the same thing gets the same chance.
- A door closed by money or approval stays pickable: `requires: savings | without: means | lacking: .5` (a loan), never
  removed.
- Keep each calling real and unglamorous where it is: the minister's long evenings and empty pews, the inventor's
  failed prototypes and unpaid patents, the founder's debts and the board's knives, the soldier's boredom, mud and
  orders, the nurse's night shifts and short staff. A step up is a good year, not a finish line.
- **Wrongs are pickable** with plain labels and no preaching, each with a mark (hid a wrong, broke your word, made an
  enemy, defied an authority, gave in to pressure) and a closed: line with a real backfire: money for the poor taken
  and buried, a vote bought in a congregation quarrel, a safety test skipped, a design taken from an employer, a rumour
  spread about a rival shop, figures moved before the audit, a pension cut quietly, a friend's mistake covered in a
  report, a recruit's bullying looked away from, checks signed that were not done, a dose mistake hidden. Integrity and
  vanity belong to every colour.
- **Each colour's honest road** in every moment: White's rule and duty (the rite kept, the test done to the letter, the
  books honest, the order obeyed or lawfully refused, the protocol); Blue's mind and method (the study, the clever
  design, the plan, the diagnosis); Black's ambition and leverage (the backers, the deal, the rank, the name, the
  rival outdone); Red's courage and heart (the sermon from the gut, the risky prototype, the bold bid, first through the
  door, the night nobody else will work); Green's people, place and patience (the flock known by name, the old machine
  mended, the family firm, the unit as family, the body, birth and growth).
- **The healer's road leans on life, body, birth and growth** (the Vision thread, 10-19), so it never reads as White's
  service: births, the body healing, herbs and gardens, the district's families from first breath to last, patience.
- **Content limits, never broken:**
  - No sexual violence and no harm to children as pickable acts. No child or baby dies or is harmed in any text: a
    birth ends with mother and baby well, or plainly taken to special care and recovering. Children appear only in
    safe forms (a family, a school, a parent present). No faith scandal touches a child or a vulnerable person: the
    faith road's wrongs are about money, power and lies.
  - Suicide is never pickable and never a scene. No option helps anyone die or hastens a death; a death at the end of
    a long illness is natural, peaceful and plain.
  - The command road: killing is rare, by choice, never graphic, never by or of a child, and in this pack's moments
    never at all; no massacre, no harm to civilians and no torture is ever pickable, nor shown. Accidents and losses
    are plain and offstage (a broken leg on exercise, a vehicle overturned, a soldier who did not come home). No real
    army, war, regiment, rank title of a real country, or country.
  - Nothing graphic anywhere: an injury or an illness stays plain and offstage.
  - No real people, faiths, churches, orders, scriptures, firms, brands, products, armies, wars, hospitals, schools,
    countries or years by name: "the faith", "the order", "the house of worship", "the big firm", "the army", "the
    hospital in the city". Every faith is treated with respect; no option mocks a belief.
- Role slots only from the spec ({boss} {colleague} {mentor} {rival} {friend} {partner} {elder} {place} ...): the
  faith's leaders, the board, the commanding officer or the hospital's managers are {boss}; a fellow minister,
  engineer, officer or nurse {colleague}; an old minister, engineer, sergeant or midwife {mentor}; the other candidate
  {rival}.
- **Worlds.** Every moment carries situation-level earth:, tribal: and magic: lines (and `scene tribal:` / `scene
  magic:`), in the forms below. An option whose act reads differently in a world adds its own tribal: or magic:
  wording. A world-only moment is marked `only: tribal` or `only: magic` and has that world's line alone. Supernatural
  acts are one choice among ordinary ones, never forced, always with a price, and never rest on the person's own gift:
  the magic comes from someone else (an oracle, an enchanter, a spirit, something old) on a `closed: approval:` line
  with a backfire. Modern Earth has no magic.
- **Frequency.** Every moment, of every tier, carries a `times:` line in words: how often the people who can meet it
  meet it, how rare it is across all lives (from the catalogue shares), and a source in plain words or "(estimate)".
- **Unique names.** No moment name or option label may appear anywhere else: grep /mnt/project-files/chroma-library/
  earth.py and *.lib, and chroma-packs/*/*.lib before you settle a name. The moment names
  below are already checked; keep them exactly.

### Forms in the other worlds (worlds.py)
| Title or perk | tribal | magic |
|---|---|---|
| ordained religious minister / member of a monastic community (base) | one who leads the band's rites / one who lives apart at the sacred place | a priest / a monk or nun of an order |
| senior cleric | a keeper of the rites for many bands | a priest of a great temple |
| head of a faith order | the great shaman whom every band heeds | high priest of a god's order |
| inventor | the toolmaker whose new ways spread from band to band | an artificer |
| celebrated inventor | the maker whose boat first crossed the great lake | the realm's artificer, maker of wonders |
| founder of a firm (base) | one who starts a trade of their own between the bands | a merchant with a house of their own |
| chief executive | the trader who runs a band's trade at the gatherings | a guild master |
| magnate | the trader owed a favour in every camp | a merchant prince |
| soldier (base) | a hunter of the guard | a soldier of the realm |
| army officer | a leader of the hunters and the guard | a captain of the realm's army |
| general | the war leader of the clans | a warlord, general of the realm |
| senior nurse or midwife | the band's birth-keeper and first healer | a healer of the temple house |
| renowned healer | the healer every band sends for, who knows every plant | a herb-healer or druid-healer known across the realm |
| preaching / prototyping / leading soldiers | speaking for the spirits at the fire / making a new tool and trying it / leading the guard | preaching / building a working model / leading soldiers |
| a degree in theology / an officer's commission / licence to prescribe | the old shaman's years of teaching / the elders' leave to lead the guard / the leave to give the strong plants | the temple school's seal / a captain's commission / the apothecaries' licence |
| an invention in everyday use / a seat on boards / mentioned in dispatches | a tool every band now makes / a voice at every trading circle / named for courage at the fire | a device in every household / a seat on the guild councils / named in the captain's report |
| families who send for you / a flock that follows you / investors who back you | families who send for you / followers who would move camp with you / traders who share their goods with you | the same / a congregation that follows you / backers among the merchant houses |
| a business empire / a patent of your own / a clinic of your own | trade in every camp along the rivers / a tool only you may make / a healer's lodge of your own | a merchant house of many halls / the guild's grant on a design / a house of healing of your own |

## Calibration lessons (from the Art and Stage packs' briefs, kept)

1. Holder pairs use `aims:` and never give a new title: careers and faith titles rate .5, with `gap:` 1-3. They may
   `grants:` a perk plainly earned and `drops:` the title held. No share: line on holder pairs (the holds: gate does
   the drawing), as art-rungs.lib.
2. Every moment carries `times:`.
3. A life event's `per_year` is the yearly rate of acting on the chance, by stage (child juvenile young_adult adult
   mature elder), per holder; values are given below; keep them, and write 0 for a stage the moment does not list.
4. Every echo needs an engine condition (engine-conditions.py, written for the names below). Do not add an echo,
   inner or read moment that is not in this brief.
5. An option with `requires:` carries `lacking:`.
6. Every option except doing nothing carries `chance:`; the mean chance per means colour stays within 3 points in every
   stage. Mean chance about 68 to 72 for everyday moments and life events, 72 to 78 for echoes (parts at their real
   chances pull it down: balance them across colours inside the moment).
7. Long shots: every one-colour option at chance 1 to 5 that gives a title carries `grants_if_fails: a long shot that
   missed`. Steps at real odds (6 to 40) carry no perk on failure.

## Balance layout

- **Everyday pairs: 10** (two per road: one on the rung below the Known title, one on the Known title). Their
  two-colour calls hold each of the ten colour pairs exactly once, and each pair's halves use the cross cycle given (s1
  three times, s2 three times, s3 twice, s4 twice). The two halves of a pair share stages, ages, holds:, rate and gap;
  calls split the colours 2 and 3.
- **Life events (Earth and every world): 20** = 10 steps + 5 falls and wrongs + 5 long shots, four per road. Each has
  the five one-colour options plus one half of a D line: pairs D1a to D5b (all ten halves, on the steps) and triads D1a
  to D5b (all ten halves, on the falls and the long shots), so every pair and every triad appears five times.
- **Echoes: 2** (callings-echoes.lib), each even on its own: five one-colour options and one full cross cycle.
- **World-only events: 5**: magic pairs D6a, D6b and D1a; tribal triads D6a and D6b; each world's own set is even.
- In all: 47 moments, about 470 options.

---

## The faith road (file callings-faith.lib), 9 moments

Everyday pair W-A (holds `ordained religious minister | member of a monastic community`; stages young_adult adult
mature elder; age 23-95; rate .5; gap 1-3; cycle s1):
1. `the parish no one else will take` (calls WG). The faith's leaders need someone for a poor, far, shrinking
   congregation, or a house of the order in a hard place: a cold building, a handful of old faithful, a town that has
   lost its work. Grants [a flock that follows you] (stay and build it up), [preaching]; `aims: senior cleric` on one
   or two; others: say no and stay where you are, take it for one year, ask for a second minister.
   times: per minister or member of an order a year: about 1 in 6 are asked to take a hard post (estimate); about 4
   lives in 1,000 are ministers of religion (catalogue share).
2. `a quarrel splits the congregation` (calls UBR). Two factions over a change: the music, the old or the new words of
   the service, selling the hall. Grants [settling disputes], [a flock that follows you]; `aims: senior cleric`; a
   wrong: take one side's large gift and give them your voice (mark hid a wrong; closed: approval: a gift for a vote;
   backfire: the other side finds out and half the congregation leaves).
Everyday pair W-B (holds `senior cleric`; stages adult mature elder; age 35-95; rate .5; gap 1-3; cycle s2):
3. `the old house of worship needs a roof` (calls WB). The great old building is falling in, and the money for it
   would feed the poor for years. Grants [organising people], [a flock that follows you]; `aims: head of a faith
   order`; a wrong: sell the old silver from the vestry quietly (mark hid a wrong; closed: approval; backfire: it is
   missed at the feast, and the faith's council asks where it went).
4. `the young want the old rite back` (calls URG). Young members want the ancient rite and its old words; the elders
   who fought for the modern service are hurt. Grants [leading a ceremony], [scripture], [a flock that follows you];
   `aims: head of a faith order`.

Steps (life events):
5. `the congregation needs a senior minister` (pairs D1a). holds ordained religious minister | member of a monastic
   community; tenure 6-100; stages adult mature elder; age 35-85; per_year 0 0 0 .04 .05 .02; drivers community+.3.
   Door: `title: senior cleric` at chance 30 on the five one-colour options (each colour's own way of taking it on);
   one requires a degree in theology (`requires: a degree in theology | without: approval | lacking: .3`). The pair
   half: honest ways to weigh it (take a smaller post nearby, put a friend's name forward, stay with the flock you
   have, ask the congregation first, take it on for a set term).
6. `the order chooses its head` (pairs D1b). holds senior cleric | member of a monastic community; tenure 6-100; stages
   adult mature elder; age 45-100; per_year 0 0 0 .01 .03 .03; drivers community+.2 fortune+.2. Door: `title: head of
   a faith order` at 6 (a step at real odds, not a long shot: no perk on failure).

Fall and wrong:
7. `a colleague's theft the faith would rather bury` (triads D1a). holds senior cleric | ordained religious minister |
   head of a faith order | deacon or elder; stages adult mature elder; age 25-100; per_year 0 0 0 .01 .015 .01. A
   fellow cleric has been taking money given for the poor; the faith's leaders want it handled quietly. The wrong: bury
   it (mark hid a wrong; closed: approval: a theft buried; backfire: the papers find it, and the trust is gone:
   `takes: a flock that follows you`). Others: take it to the faith's council, to the police, confront the colleague,
   make them repay it and leave, tell the congregation the truth. Money only: no person is harmed.

Long shot:
8. `a sermon that goes round the country` (triads D3b). holds ordained religious minister | lay religious teacher |
   street preacher; tenure 3-99; stages adult mature elder; age 25-95 (a minister from 35); per_year 0 0 0 .01 .01 .005; drivers era+.2
   fortune+.3. Someone records a sermon and it spreads. Titles at 2 to 5 with `grants_if_fails: a long shot that
   missed`: senior cleric (the minister), ordained religious minister (the lay teacher or the street preacher, the
   faith's leaders asking them to train). The triad half: weigh it, a smaller step, or walk away from the attention.

World-only:
9. `the god speaks in the temple` (only: magic; pairs D6a). holds senior cleric | ordained religious minister; tenure
   3-99; stages adult mature elder; age 45-100; per_year 0 0 0 .02 .02 .01. An oracle says the god has chosen a new
   high priest. `title: head of a faith order` (high priest of a god's order) at 6 for the senior cleric; one option
   takes the oracle's bargain (closed: approval: the oracle's price; backfire: the god's favour is a debt). The rest
   honest ways: wait for the council, put a better priest forward, refuse a choice made by an oracle.

## The invention road (file callings-invention.lib), 9 moments

Everyday pair U-A (holds `software developer | civil engineer | machinist | electrician | founder of a firm |
apprentice`; stages young_adult adult mature elder; age 18-90; rate .5; gap 1-3; cycle s1):
1. `the idea in the shed at night` (calls UR). An idea that will not let go, built at night from parts. Grants
   [prototyping]; `aims: inventor`; a wrong: build it with the employer's parts and time and say nothing (mark hid a
   wrong; closed: law: an employer's design taken; backfire: the firm claims the idea).
2. `the machine nobody can fix` (calls WBG). At work, the old machine or system everyone depends on fails, and the
   maker is long gone. Grants [prototyping], [fixing things]; `aims: inventor`.
Everyday pair U-B (holds `inventor`; stages young_adult adult mature elder; age 20-95; rate .5; gap 1-3; cycle s3):
3. `a big firm wants to buy the patent` (calls UG). Grants [investors who back you], [savings]; `aims: celebrated
   inventor`; a wrong: sell it to the buyer who will bury it to protect their own product, without telling the
   partner who helped (mark broke your word; closed: approval; backfire).
4. `the prototype catches fire` (calls WBR). A test goes wrong in the workshop: smoke, a burnt hand at most, plain.
   Grants [prototyping]; `aims: celebrated inventor`; a wrong: hide the fault from the backers until the next round
   (mark hid a wrong; closed: approval; backfire: it fails again in front of them).

Steps:
5. `the prototype works` (pairs D2a). holds software developer | civil engineer | machinist | electrician | founder of
   a firm | apprentice; tenure 2-100; stages young_adult adult mature elder; age 20-90; per_year 0 0 .03 .04 .03 .01;
   drivers era+.3 fortune+.2. Door: `title: inventor` at 25, with `grants: a patent of your own` on some
   (`requires: savings | without: means | lacking: .5`).
6. `an invention in every home` (pairs D2b). holds inventor; tenure 4-100; stages adult mature elder; age 25-100;
   per_year 0 0 0 .02 .03 .02; drivers era+.3 prosper+.2. Door: `title: celebrated inventor` at 6 with `grants: an
   invention in everyday use`.

Fall and wrong:
7. `the safety test you could skip` (triads D1b). holds inventor | civil engineer | celebrated inventor | founder of a
   firm; stages young_adult adult mature elder; age 22-95; per_year 0 0 .01 .015 .01 .005. The launch is next week and
   the last safety test takes a month. The wrong: skip it (mark hid a wrong; closed: law: a safety test skipped;
   backfire: it fails in use, someone is hurt (plain), and `takes: an invention in everyday use` or the name). Others:
   delay the launch, run the test cheaply, tell the buyers the truth, test it on yourself (plain risk).

Long shot:
8. `the garage invention` (triads D4a). holds apprentice | machinist | electrician | software developer |
   repair-cafe volunteer; tenure 1-99; stages young_adult adult mature elder; age 18-95; per_year 0 0 .01
   .01 .005 .005; drivers era+.3 fortune+.3. Titles at 2 to 5 with `grants_if_fails: a long shot that missed`:
   inventor (for each holder; `title: inventor` is the next rung for all of them). The triad half: weigh it, a smaller
   step (`grants: prototyping`), or walk away.

World-only:
9. `the guild commissions a flying ship` (only: magic; pairs D6b). holds inventor | civil engineer | machinist;
   tenure 3-99; stages adult mature elder; age 25-100; per_year 0 0 0 .02 .02 .01. The artificers' guild wants a ship
   that flies. `title: celebrated inventor` (the realm's artificer) at 6 for the inventor; `title: inventor` (an
   artificer) at 25 for the civil engineer or the machinist; one option buys an enchanter's binding that makes it rise
   (closed: approval: the Order's leave; backfire: the binding must be renewed, at a price).

## The business road (file callings-business.lib), 9 moments

Everyday pair B-A (holds `shop owner | founder of a firm | café or bar owner | shift manager`; stages young_adult
adult mature elder; age 18-90; rate .5; gap 1-3; cycle s2):
1. `a rival opens across the street` (calls UB). Grants [striking a deal], [investors who back you]; `aims: chief
   executive`; a wrong: spread a rumour about the rival's kitchen or books (mark made an enemy; closed: approval;
   backfire: the rumour is traced back).
2. `the bank calls in the loan` (calls WRG). Grants [good credit], [investors who back you]; `drops: shop owner` or
   `drops: café or bar owner` on one option (sell up and start again); `aims: chief executive` on one.
Everyday pair B-B (holds `chief executive`; stages adult mature elder; age 28-90; rate .5; gap 1-3; cycle s3):
3. `the board wants cuts by Friday` (calls BG). Cut jobs, cut pay, or find another way. Grants [a seat on boards];
   `aims: magnate`; a wrong: cut the workers' pension promises quietly (mark hid a wrong; closed: law; backfire: the
   regulator and the papers find out).
4. `a takeover bid at dawn` (calls WUR). A bigger firm bids for yours. Grants [investors who back you], [shares];
   `aims: magnate`.

Steps:
5. `the board needs a chief executive` (pairs D3a). holds founder of a firm | shop owner | café or bar owner | shift
   manager; tenure 3-100; stages adult mature elder; age 28-80; per_year 0 0 0 .03 .03 .01; drivers prosper+.3
   money+.2. Door: `title: chief executive` at 25.
6. `a rival firm is for sale` (pairs D3b). holds chief executive | founder of a firm; tenure 4-100; stages adult
   mature elder; age 30-90; per_year 0 0 0 .02 .03 .02; drivers prosper+.2 money+.3. Door: `title: magnate` at 6 with
   `grants: a business empire`; requires savings or shares on two (`requires: savings | without: means | lacking: .5`).

Fall and wrong:
7. `the numbers that would look better moved` (triads D2a). holds chief executive | magnate | founder of a firm | shop
   owner; stages young_adult adult mature elder; age 22-100; per_year 0 0 .01 .015 .015 .01. The year's figures are
   short, the backers are watching. The wrong: move the numbers (mark hid a wrong; closed: law: the accounts falsified;
   backfire: the auditors find it, `takes: a seat on boards`). Others: tell the backers the truth, cut costs openly,
   sell a part of the firm, take the loss on your own savings.

Long shot:
8. `the market stall that became a chain` (triads D4b). holds shop owner | café or bar owner | shop assistant; tenure
   2-99; stages young_adult adult mature elder; age 18-90; per_year 0 0 .01 .01 .01 .005; drivers prosper+.3
   fortune+.2. Titles at 2 to 5 with `grants_if_fails: a long shot that missed`: chief executive (the shop owner or the
   café owner whose idea grows into a chain), founder of a firm (the shop assistant who starts the chain). The triad
   half: weigh it, a smaller step, or walk away.

World-only:
9. `a seat among the merchant princes` (only: magic; pairs D1a). holds chief executive | founder of a firm; tenure
   3-99; stages adult mature elder; age 30-100; per_year 0 0 0 .02 .02 .01. A seat on the council of merchant princes
   falls free. `title: magnate` (a merchant prince) at 6; one option strikes a bargain with something old for the votes
   (closed: approval: the bargain's price; backfire: it collects).

## The command road (file callings-command.lib), 9 moments

Everyday pair R-A (holds `soldier`; stages young_adult adult mature; age 17-55; rate .5; gap 1-3; cycle s4):
1. `the corporal is hurt on exercise` (calls WR). On a night exercise in the hills the section's corporal falls and
   breaks a leg (plain, offstage), and someone has to take charge and get everyone down. Grants [leading soldiers],
   [mentioned in dispatches]; `aims: army officer`.
2. `the platoon gets a new sergeant` (calls UBG). A new sergeant who is hard on the weakest recruit. Grants [old
   comrades], [leading soldiers]; `aims: army officer`; a wrong: look away, and laugh along (mark gave in to pressure;
   closed: approval; backfire: the recruit leaves, and the inquiry asks who saw it). Nothing graphic: words and
   punishments only.
Everyday pair R-B (holds `army officer`; stages young_adult adult mature; age 20-62; rate .5; gap 1-3; cycle s1):
3. `an order you think is wrong` (calls BR). An order from above would put the soldiers at needless risk to meet a
   deadline. Options: obey, refuse (mark defied an authority), find a smarter way, go above the commander's head, ask
   for it in writing. Grants [leading soldiers]; `aims: general`. No option harms anyone outside the unit.
4. `the unit comes home one short` (calls WUG). A soldier of the unit did not come home from a deployment (told plainly,
   offstage). Visit the family, speak at the memorial, push the inquiry, keep the unit together. Grants [old
   comrades]; `aims: general`.

Steps:
5. `officer selection` (pairs D4a). holds soldier | graduate | national service done; stages young_adult adult; age
   20-40; per_year 0 0 .08 .04 0 0; drivers era+.1. Door: `title: army officer` at 35 (the academy's selection board;
   with `grants: an officer's commission`).
6. `the army needs a new general` (pairs D4b). holds army officer; tenure 12-100; stages adult mature; age 40-62;
   per_year 0 0 0 .02 .04 0; drivers era+.2 fortune+.2. Door: `title: general` at 6.

Fall and wrong:
7. `the report on the night that went wrong` (triads D2b). holds army officer | soldier | general; stages young_adult
   adult mature; age 18-65; per_year 0 0 .01 .015 .01 0. On an exercise, a friend's mistake overturned a vehicle and a
   soldier was hurt (plain). The wrong: write the report to cover the friend (mark hid a wrong; closed: law: a report
   falsified; backfire: the inquiry finds it, `takes: rank`). Others: write it true, tell the friend to own up first,
   take some of the blame yourself, fix the training that let it happen.

Long shot:
8. `the field commission` (triads D5a). holds soldier; tenure 3-99; stages young_adult adult mature; age 20-45;
   per_year 0 0 .01 .01 .005 0; drivers fortune+.3. In a flood or a fire the army is sent to, the soldier holds a
   crossing and gets everyone out, and a general sees it. Title army officer at 2 to 5 with `grants_if_fails: a long
   shot that missed`. Not about fighting.

World-only:
9. `the war leader is chosen at the gathering` (only: tribal; triads D6a). holds army officer | soldier; tenure 3-99;
   stages adult mature elder; age 25-80; per_year 0 0 0 .02 .02 .01. The clans gather to choose who will lead them if
   raiders come. `title: general` (the war leader of the clans) at 6 for the army officer of years; `title: army
   officer` (a leader of the hunters and the guard) at 35 for the soldier; one option asks the spirits through the
   shaman (closed: approval: the spirits' price; backfire). No fighting in the moment.

## The healing road (file callings-healing.lib), 9 moments

Everyday pair G-A (holds `nurse | midwife | care worker | paramedic`; stages young_adult adult mature elder; age
20-75; rate .5; gap 1-3; cycle s2):
1. `the birth that will not wait` (calls RG). A baby comes fast in the wrong place: a lift, a farmhouse cut off by
   snow, the back of a taxi. In every outcome mother and baby are well. Grants [families who send for you], [emergency
   care]; `aims: senior nurse or midwife`.
2. `the ward is two nurses short` (calls WUB). The night shift is short again. Grants [used to night shifts],
   [organising people]; `aims: senior nurse or midwife`; a wrong: sign off the checks that were not done (mark hid a
   wrong; closed: approval; backfire: the audit finds the gaps).
Everyday pair G-B (holds `senior nurse or midwife`; stages adult mature elder; age 26-75; rate .5; gap 1-3; cycle s4):
3. `a family asks you to stay to the end` (calls WU). An old patient is dying, peacefully, of a long illness, and the
   family asks the nurse to be there. No option hastens a death. Grants [families who send for you], [calming people
   down]; `aims: renowned healer`.
4. `the managers want the birth centre closed` (calls BRG). Grants [a clinic of your own] (open one yourself:
   `requires: savings | without: means | lacking: .5`), [organising people]; `aims: renowned healer`.

Steps:
5. `the ward needs someone in charge` (pairs D5a). holds nurse | midwife; tenure 4-100; stages adult mature; age
   26-67; per_year 0 0 0 .06 .04 0; drivers prosper+.1 community+.2. Door: `title: senior nurse or midwife` at 40;
   requires professional registration on two (`requires: professional registration | without: approval | lacking:
   .3`).
6. `patients come from far away` (pairs D5b). holds senior nurse or midwife | midwife | nurse | physician |
   complementary therapist; tenure 8-100; stages adult mature elder; age 30-100; per_year 0 0 0 .01 .03 .02; drivers
   community+.3 fortune+.2. Door: `title: renowned healer` at 6 with `grants: families who send for you`.

Fall and wrong:
7. `the wrong dose on the night shift` (triads D3a). holds senior nurse or midwife | nurse | midwife | physician;
   stages young_adult adult mature elder; age 21-75; per_year 0 0 .02 .02 .015 .005. A dose mistake, caught in time:
   the patient is fine by morning. Tell or hide. The wrong: hide it (mark hid a wrong; closed: approval: a mistake
   hidden; backfire: the record shows it, `suspends:` the career held, or `takes: licence to prescribe`). Others: tell
   the patient and the ward (mark owned up), report it to change the system, cover for an exhausted colleague, ask for
   fewer night shifts.

Long shot:
8. `the remedy that worked` (triads D5b). holds nurse | midwife | complementary therapist | senior nurse or midwife;
   tenure 3-99; stages adult mature elder; age 30-95; per_year 0 0 0 .01 .01 .01; drivers community+.2 fortune+.3. A
   way of caring the families talk about: a gentler way through a hard birth, a dressing from the garden that heals
   a wound that would not, a way of calming the frightened. Titles at 2 to 5 with `grants_if_fails: a long shot that
   missed`: renowned healer (each holder: the facet sits on each of them). The triad half: weigh it, write it up, teach
   it, or keep it for the families.

World-only:
9. `the sickness in the winter camp` (only: tribal; triads D6b). holds senior nurse or midwife | nurse | midwife;
   tenure 2-99; stages adult mature elder; age 30-90; per_year 0 0 0 .02 .02 .02. A fever runs through
   the winter camp. Grants [families who send for you]; `title: renowned healer` (the healer every band sends for) at
   6 for the band's birth-keeper and the healers of years; one option asks a spirit for a cure (closed: approval: the
   spirit's price; backfire). Nobody dies in the text; the camp recovers or the fever passes.

## Echoes (file callings-echoes.lib), 2 moments (written with the faith road)

Each even on its own: five one-colour options and one full cross cycle; once: yes; the anchors and gates are in
engine-conditions.py (ECHO_CALLINGS_LONGSHOTS). They follow any of the five long shots.
1. `the calling, years later` (cycle s2; rate .1). The second try: years later the same kind of door opens a crack.
   `title: {missed}` on the one-colour options at chance 4, with `grants_if_fails: a long shot that missed` only where
   the chance stays 1 to 5. Others: let it pass, help someone younger try.
2. `the long shot becomes a life of service` (cycle s3; rate .05). Making peace with it: the long shot becomes service
   at the rung the person holds, a young one taught, a door held open. `grants: apprentice of one's own` (the one
   taught), `grants: good name in town` (the service); others: let it go, tell the story to the family.

## Checks (each file must pass all of them)

- Build: `cd <your scratch> && CHROMA_ROOT=<repo> PYTHONDONTWRITEBYTECODE=1 python3 -B
  <scratch>/build.py chroma-packs/callings/<yourfile>.lib --out <scratch>/out` (copy
  /mnt/project-files/chroma-library/build.py to your scratch folder first); it must end with "no layout problems".
- Footprints: copy `<scratch>/out/<yourfile>.py` to `<scratch>/chk/callings.py` and `<scratch>/out/<yourfile>_foot.py`
  (build.py writes foot: to its own table, FOOT, since the Engine's 10-19 call) to `<scratch>/chk/callings_foot.py`,
  then `cd <repo>
  && PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-packs/tools/check_footprint_packs.py --built <scratch>/chk callings`:
  0 options with no footprint and no other problem.
- Chance and tags: `PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-packs/tools/lib_stats.py
  chroma-packs/callings/<yourfile>.lib`: the mean chance per means colour within 3 points
  overall and in every stage; tag counts close to even.
- Names: `cd <repo> && PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-packs/tools/check_pack.py
  callings`: no unknown names from your file (other files may still be missing while others write them).

## Files and rules

- Write only your own file in chroma-packs/callings/ (named in your task). Write moment
  by moment (append), so partial work survives.
- Never write anywhere else in the repository or in /mnt/project-files; read only. Scratch goes in a folder of your own
  outside the repository. No packages;
  standard library only. Run Python as `PYTHONDONTWRITEBYTECODE=1 python3 -B`. No git commands.
- No AI model names or identifiers in any file.
