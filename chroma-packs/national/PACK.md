# Pack: National standing: fifteen routes to a national seat (modern Earth, with the tribal and magic worlds)

Status: built for v25 on 2026-10-23, switched off. Not in batch.PACKS: merging this folder changes no life until the
Engine adds `national` (with `callings`, which it builds on). Engine name: `national`. Leaving it out is the clean cut for
national standing, third in v25's cut order (`chroma-ideas/next-table-2026-10-19/v25-operation.md`): with the pack off,
the five seats that exist are as v24 has them and none of the routes' seats, assets or fields exists.

Why: no v24 life reached national standing. Only five titles give it (catalogue standing=3), all in rule, prot or comm
and led by W, R or B. Emren's decision #11 (`v25-decisions-emren.md`, section 10) asks for fifteen shared routes to
national standing, by colour coverage, not eligibility, each with its own activities, dilemma, useful asset and
obligations, and ten pair and ten triad styles that reuse them; recognition, influence and formal authority kept apart.
Outer world's data holds the routes and the styles (`chroma-world/spheres/data/world_fit.json` "national",
`world-fit-v2.md` section 3); the Engine's part is the climb (`chroma-engine/notes/v25/other-shapes.md` section 5);
this pack holds the ten new seats, the fifteen assets and the ten new routes' fields.

## The fifteen routes

Each route ends in one seat, so every sphere has a seat and every colour leads three routes (Vision agreed the map and
the three renames, 10-23 15:57).

| Colour | Route | Seat | Asset | Route's aim |
|---|---|---|---|---|
| W | Mandate Builder | head of government (politics) | a standing mandate | to lead the country (politics) |
| W | Public Service Architect | minister (politics) | a working public service | to be the one who makes things happen (politics) |
| W | Common-Ground Maker | head of a national faith body | standing with both sides | to bring the sides together |
| U | Discoverer | chief scientist | a finding and its method | to find what no one knew |
| U | Systems Inventor | director of a national laboratory | a working national system | to build what the country runs on |
| U | Truthfinder | editor of a national paper | a record and its sources | to tell the country the truth |
| B | Enterprise Builder | magnate (callings) | a firm and its people | to build an empire (callings) |
| B | Coalition Builder | head of a national industry body | the voice of a whole industry | to make a whole industry move together |
| B | Opportunity Patron | head of a national bank or exchange | a portfolio of people backed | to back the ones who will matter |
| R | Rallying Voice | party leader (politics) | a following that turns out | to build a movement (politics) |
| R | National Virtuoso | celebrated star of stage or sport | a signature work and its audience | to perform for the whole country |
| R | Commander | general (callings) | a unit that trusts its leader | to command an army (callings) |
| G | Living-Land Steward | head of the national parks | a stretch of land kept alive | to keep the country's wild places |
| G | Living-Heritage Keeper | keeper of the national heritage | a living tradition kept | to keep the old ways alive |
| G | Community Weaver | head of a national charity | a web of groups that help each other | to join the helpers of every town |

The renames from Outer world's first draft: "national laureate" became the editor of a national paper (the base
[journalist] sits in gather); "leader of a national movement" became the keeper of the national heritage (the engine's
movement road already gives a movement's leader national influence, and the Rallying Voice is the party leader); the
"laboratory or library" seat narrowed to the laboratory (the library and the museum are the heritage keeper's).

A route's colour says whose motives it suits; anyone may walk it (tendencies, not walls). The twenty styles (Outer
world's) change which dilemmas come up on these routes and how options read; they add no power and no seat.

## The three kinds of national standing

- **Authority** is a seat: standing 3 while it is held, with the 8 to 12 national decisions a year (WA8). Each seat
  ends as its catalogue lost= says (a term, a vote, a scandal, age), and never after its catalogue ages (C-X4).
- **Influence** is the route's asset: 4 to 8 national proposals a year in the Engine's lane D, earned on the route or in
  the seat and kept after it while its obligation is kept (roles.py lose= names the broken obligation). Five assets
  belong to the seats (odds 0); the five standings and five bonds also come by a moment's grant (odds .05).
- **Recognition** is the shared reach ladder ([known across the country], [a household name], `core/reach.py`): one way
  into a seat among others, never given by one (roles.py has no EXTEND onto it).

## Files

| File | What |
|---|---|
| `catalogue.py` | the ten seats (standing=3, sphere, face, institution, ways and three profiles each) and the fifteen assets; DEPENDS on politics, callings, science, stage, art |
| `roles.py` | ROLES_NATIONAL: each seat's req (years at the title it refines, and a good name, the route's asset or the reach), its ends; each asset's req and lose; TARGET_NATIONAL |
| `helps.py` | HELPS_NATIONAL and HELPS_PERK_NATIONAL: what prepares a person for each seat and asset, along the route's five entries |
| `worlds.py` | WORLDS_NATIONAL: each seat and asset in the tribal and magic worlds, from each route's realm reading |
| `fields.py` | FIELDS_NATIONAL: the ten new routes as aims fields (five rungs, the seat at the top), and ROUTES, the fifteen routes' aims |
| `dreams.py` | ten new modern Earth dreams, one per new route, for the Library's dreams.py |

No moments: the routes' encounters (about 60, and 40 for the styles) are the Library's (Outer world's split, `world-fit-
v2.md` section 5).

## Colour balance

- Seats: each seat's ways are its route's pair; its three profiles are that pair, a second pair and the fifth colour
  alone. Each colour is the single profile of exactly two seats, so the ten seats are exactly even (W U B R G 6.00
  each; `check_pack.py national`).
- Assets: one per route, so each colour holds one standing, one bond and one asset, and every kind holds all five.
- Dreams: ten pairs at .5 each, 2.0 per colour (`dreams.py`).
- Fields: each route's face is its seat's ways pair.

## Clocks

Every route field has five rungs: the local step, the trade, the Known rung, the Notable rung (the "wider" step of
Outer world's climb: the asset has spread, or the summit the seat refines) and the seat. From the start, a life that
keeps at it reaches its seat after about 17 to 31 years of median effort, and about 2 to 10 in 10,000 of those who keep
at it do (`check_fields.py national`). Each field's comment names its sources; most figures are estimates. The game's
targets for national standing (.01 to .03 of lives left alone, .15 to .30 of skilled aim-directed lives; WA7, WA8n) are
the Engine's calibration through the climb and its aim factor, never a reason to change these real-world shares.

## How this reads in a magic realm (the realm-ready rule)

National is the realm's widest ring: in the tribal world the moot of all the clans of a valley at the summer gathering,
in the magic world the realm's court, its Assembly and the great Orders and guilds. Each route keeps its shape there,
the same rungs, asset, obligation and ends, and only its words change, after each route's `realm` in Outer world's data:
the Common-Ground Maker is a peace-weaver between houses, the Discoverer a sage of the high college, the Living-Land
Steward a druid of the circle or a warden of the wilds (`worlds.py`). A seat in the tribal world is held by acclaim at
the gathering and kept while the clans still send for the holder; in the magic world by warrant of the throne, an Order
or a guild. Nothing in the engine part is Earth's: a seat is a title with standing 3 in a sphere, an asset a perk with
an obligation, a route an aims field.

## Content limits

Timeless modern: no real year, body, paper, bank, park, faith, firm, person or country in any word a player reads (real
figures stay in comments). No colour words or game terms in player text. Nothing graphic; no harm to a child; the
army's seat is the callings pack's general and adds no killing.

## Switching it on (the Engine, with Emren's word)

1. `callings` in batch.PACKS first (DEPENDS; it is listed on feature/v25), then `national`, with `wa_nat_climb`.
2. The Engine's climb gives the seats their chance in time (.02 a year, times 1.5 with an aim for the route, only to a
   free seat) and reads each seat's req in roles.py as its gate; the seats' own rate is 0, so the chance is counted
   once. The seats are calibrated by the climb against WA7, not by TARGET_NATIONAL (which holds only the assets).
3. The ten dreams are in the Library's dreams.py (DREAMS_NATIONAL, feature/v25), read only with `wa_nat_climb` on;
   `dreams.py` here is their source and is never loaded. The Library writes the routes' and styles' encounters.
4. The game's proof, `check_pack.py national`, `check_fields.py national`, and Release's WA7, WA8 and WA8n.

## Agreed with the other owners (10-23)

- Outer world's `world_fit.json` SEATS follow this catalogue (the editor in gather, U R; the heritage keeper in arts,
  G R; the parks in prod, G U); Truthfinder's spheres gained gather and the Living-Land Steward's are prod, prot and
  rule (land is not one of the nine spheres).
- The Engine: `callings` is listed in feature/v25; listing `national` is the Engine's change when `wa_nat_climb` lands.
- The Library writes the moments only, in `earth_national.py`: route encounters keyed `route: <world_fit.json route
  key>`, style moments `style: <colours>`, decisions `scope: nation`. The fields here are keyed by aim name, as every
  aim is; `ROUTES` in `fields.py` maps each route key to its aim.
