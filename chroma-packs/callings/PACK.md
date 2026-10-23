# Pack: The Five Callings: Faith, Invention, Business, Command and Healing (modern Earth, with the tribal and magic worlds)

Status: built for v24 on 2026-10-19, switched off. Not in batch.PACKS: merging this folder changes no life until the
Engine adds `callings` (with Emren's word, at a refit). Engine name: `callings`. The plan: chroma-ideas/
next-table-2026-10-19/plan.md, section 5, "Then the missing faces that keep each colour pair fair". The four packs'
twenty public callings give every colour pair two faces and no single colour one (chroma-packs/notes/
v24-aims-ladders.md); these are the five single colours, as the Vision thread agreed (10-19 12:04 UTC). The steward of
the land, or druid, is written for v25 and held apart ("The sixth road" below). Each road is the first slice of a pathway pack in
chroma-pack-ideas/next-packs.md (Faith Leadership, Engineering Crafts and Technology, Business and Wealth, Military,
Medicine and Rescue); when one of those packs is built, it takes its road's titles over.

## The roads

| Colour | Road | Rungs |
|---|---|---|
| W | the faith leader | base [ordained religious minister] or [member of a monastic community]; Known [senior cleric]; summit [head of a faith order] |
| U | the inventor | base [software developer], [civil engineer], [machinist], [electrician], [apprentice] or [founder of a firm]; Known [inventor]; summit [celebrated inventor] (facet on inventor) |
| B | the magnate | base [shop owner], [founder of a firm], [café or bar owner] or [shift manager]; Known [chief executive]; summit [magnate] (facet on chief executive or founder of a firm) |
| R | the commander | base [soldier] (or [graduate] and the academy); Known [army officer]; summit [general] (facet on army officer) |
| G | the healer | base [nurse] or [midwife]; Known [senior nurse or midwife]; summit [renowned healer] (facet on senior nurse or midwife, nurse, midwife, physician or complementary therapist) |

- Each road climbs from base titles, so a calling grows from below, out of the life already lived (Emren, 10-19 11:38:
  a calling should feel bottom-up).
- Every Known rung and summit grows from the rung below (roles.py rungs=, LIFE_CALLINGS gates) and has a step at real
  odds and a long shot (LONGSHOTS_CALLINGS).
- A moment that gives a title starts at that title's first age (the engine gives a title only inside its catalogue
  ages, C-X4): where one moment's singles give titles of different first ages, its gate in engine-conditions.py
  carries the age (the sermon's minister from 35, the stall's owner from 28, the war leader's officer from 40).
- The ladders (aims.py): taste, practice, Known, Notable, Historic, as the other packs' callings. Known is the road's
  Known rung (or a sphere's rung 4 or 5), Notable the summit, Historic the head of an order or [a work that outlives
  you] (core/legacy.py).

## Files

| File | What it holds |
|---|---|
| catalogue.py | 10 titles (5 Known rungs, 5 summits; the faith road's are of the faith kind) and 15 perks, base catalogue format, every share with its source or marked as an estimate; sphere and face tags |
| roles.py | ROLES_CALLINGS (how each title and perk comes and goes), EXTEND_CALLINGS (six widenings of base rules), TARGET_CALLINGS (the one budget's tiers, perk multiples) |
| helps.py | HELPS_CALLINGS (earned odds), WINDOWS_CALLINGS (right place, right time), LIFT_CALLINGS (half lifts on the summits) |
| engine-conditions.py | LIFE_CALLINGS (the rung below, in years), LONGSHOTS_CALLINGS, LIFE_CALLINGS_LONGSHOTS, ECHO_CALLINGS_LONGSHOTS (two echoes) |
| worlds.py | the tribal and magic form of every title and perk (WORLDS_CALLINGS) and the five world-only moments (WORLD_ONLY_CALLINGS) |
| aims.py | AIMS_CALLINGS (the five single-colour callings' ladders) and LEGACY_CALLINGS |
| callings-faith.lib, -invention.lib, -business.lib, -command.lib, -healing.lib, -echoes.lib | the 47 moments, one file per road (MOMENTS-BRIEF.md) |
| MOMENTS-BRIEF.md | the plan for every moment: tier, stages, holds, rates, chances, the balance layout |
| druid.py | the sixth road, held: every table of the steward of the land, each named for the callings table it joins (nothing loads it) |
| druid/callings-land.lib | the sixth road's 9 moments, held in a folder no build or check reads |

## Colour balance

- Titles: every title has three profiles (its road's single colour and two pairs covering the other four), and each
  colour is the single of two titles: W 6.00, U 6.00, B 6.00, R 6.00, G 6.00 (check_pack.py, spread 0).
- Perks: every kind holds three perks (one single and two pairs), each colour the single of one kind: 3.00 each, and
  every kind holds all five colours.
- Aims: one calling per colour (check_aims.py): with the four packs, every single colour now has one public calling and
  every pair two.
- Each road leans to its colour through its ways and its moments, never as a wall.

## Content limits (MOMENTS-BRIEF.md, "Pack rules")

- The command road: killing is rare, by choice, never graphic, never by or of a child, and in this pack's moments never
  at all; no massacre, no harm to civilians, no torture; losses are plain and offstage. No real army, war or country.
- The healer's road leans on life, body, birth and growth, so it does not read as White's service. No baby or child is
  harmed or dies in any text; no option hastens a death.
- The faith road's wrongs are about money, power and lies, never about a child or a vulnerable person. No real faith,
  order or scripture is named, and no belief is mocked.

## How this reads in a magic realm (the realm-ready rule)

The callings rest on the core: a road of rungs (a title held, years on it, the act that takes the next one), a face of
colours, a sphere and a ladder of heights. Only their Earth face is data. In a magic realm the same five roads stand as
they are: the priest of a god's temple who becomes high priest of the order (and an oracle may name them, at a price);
the artificer who becomes the realm's maker of wonders (a flying ship, with an enchanter's binding that must be
renewed); the guild master who becomes a merchant prince (a seat on their council, perhaps bought with a bargain with
something old); the captain of the realm's army who becomes its warlord or general; the healer of the temple house who
becomes a herb-healer or druid-healer known across the realm. In the tribal world they are the keeper of the rites and
the great shaman, the toolmaker whose new ways spread, the trader owed a favour in every camp, the leader of the guard
and the war leader of the clans, the birth-keeper and the healer every band sends for. A realm's own institutions (a
god's orders, a guild's ranks, a realm's army) come as titles in its own realm files on the same rungs; no rule names a
world, and every supernatural way is optional, priced and someone else's power.

## What the Engine and the Library need (at the switch-on, with Emren's word)

1. **Library:** build `chroma-library/earth_callings.py` from callings-*.lib (build.py reads the parts), and run
   check.py and check_footprint.py.
2. **Engine:** paste engine-conditions.py into earth_rules.PACK_RULES["callings"]; add `callings` to batch.PACKS; fit
   TIER_LIFT for the five packs (tier_fit with the floors), then roles_check. Read AIMS_CALLINGS with the aims switch
   on, and add LEGACY_CALLINGS to the or of the packs' LEGACY_<PACK>.
3. **Proof:** packs are always on once listed, so the switch-on changes lives: the full proof with the refit. The pie
   gap against the run without the pack stays at .01 or less (the pack rule).

## The sixth road: the steward of the land (held)

Written 2026-10-23 for v25 (cut-order item 6, the last cut), from druid/BRIEF.md in the shared folder's
`chroma-ideas/v25-prep/packs/`: Emren's card "Yes, no land" (10-19 14:57) and the v25 decision file, sections 2, 5 and
8. Green's second calling climbs from base land titles ([farmer], [forester], [park ranger], [professional beekeeper])
to [steward of the land] (the Known rung, of the community kind: the chair of the town's land trust), [keeper of the
land] (the summit, known across the country) and [a work that outlives you]. With the land on, ten of land.json's ways
(two led by each colour) and six of its bridges lead onto the same rungs.

**Held, not poured.** `callings` is listed in batch.PACKS on feature/v25, so anything in its loaded files would change
v25's lives. The road is therefore kept in `druid.py`, which nothing loads, with its moments in `druid/`, a folder no
build or check reads. The Engine joins it behind `aims_v2`, and the land's ways behind `wa_land` (agreed 10-23 18:36).
`druid.py`'s header lists the join table by table; the step titles from land.json's ways (LAND_STEP1 to LAND_STEP3) are
the Library's drafts and are set empty if the land is cut, which leaves the road climbing on base titles alone.

**Checked joined** (a scratch copy of chroma-packs with every table poured in, 10-23):

| Check | Result |
|---|---|
| `check_pack.py callings` | all checks pass: 12 titles, 15 perks, 56 moments in 7 files; titles W U B R 7.00, G 8.00 (spread .028) |
| `check_fields.py callings` | no problems with the land's step titles left out; "to keep the land" (land shape, 5 rungs) is Known after 13.5 years' median effort (9% of those who keep at it), Notable after 23.5 (0.45%), Historic after 31.5 (0.14%) |
| `check_aims.py callings` | two expected flags: the land's 30 step titles are not yet catalogue names (the Library pours them with the land), and the faces lean to G (W U B R 1, G 2), the lean Emren's card accepts |
| the Library's `build.py` on the moments | 9 situations, 90 options (17 with a footprint), no layout problems |
| the engine's `load_batch` with callings | loads; the steward compiles as a career rung and the keeper as a summit |

**Colour balance.** Both titles carry three profiles, the road's single and two pairs covering the other four (G | W U |
B R and G | W R | U B). The aim's face is G, so with the healer the callings' six faces are W U B R G G; Emren's card
accepts the lean, and this records the exception rather than moving the face.

**In a magic realm.** The steward is the druid of the grove and the keeper the archdruid of the circle, the realm's old
woods in their care; in the tribal world, the great druid of the clans who keeps the grove and the hunting grounds
whole. The rungs, the trust's chair and the summit keep their shape, and any spirit of the deep groves is optional,
priced and someone else's power (WORLDS_LAND). The land is never a judge: a flood, a drought or a dying river is
physical, and people read it.

**At the join (the Engine, with Emren's word):** pour the tables as `druid.py`'s header says, move
`druid/callings-land.lib` up into `callings/` for the Library's build, then the switch-on steps above.
