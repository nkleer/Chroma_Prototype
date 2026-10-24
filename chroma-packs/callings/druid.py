# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (the druid; Green's second calling).
# Pathways and packs thread, 2026-10-23, for v25 (cut-order item 6): Emren's card "Yes, no land" (10-19 14:57) and the
# v25 decision file (chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md), sections 2, 5 and 8. The road climbs
# from base land titles to [steward of the land] (Known: the chair of the town's land trust), [keeper of the land]
# (the summit, known across the country) and [a work that outlives you]; with the land on, ten of land.json's ways and
# six of its bridges lead onto the same rungs. Plain data; nothing runs.
#
# HELD: nothing loads this file. batch.py reads callings' catalogue.py, roles.py, helps.py and the compiled moments,
# never druid.py, and the road's nine moments are in druid/callings-land.lib, a folder no build or check reads.
# `callings` is listed on feature/v25, so pouring the road into those files would change v25's lives; the Engine joins
# it there behind aims_v2, and the land's ways behind wa_land (the Engine, 10-23 18:36). The join, table by table:
#
#   TITLES_LAND                      -> catalogue.py TITLES (TITLES += TITLES_LAND)
#   ROLES_LAND, TARGET_LAND          -> roles.py ROLES_CALLINGS, TARGET_CALLINGS
#   EXTEND_LAND                      -> or-ed onto EXTEND_CALLINGS' keys ("known across the country", "good name in
#                                       town") and added where callings has none ("the one everyone asks")
#   LAND_WAYS_LAND                   -> or-ed onto the steward's req, only with wa_land on
#   HELPS_LAND, WINDOWS_LAND, LIFT_LAND -> helps.py HELPS_CALLINGS, WINDOWS_CALLINGS, LIFT_CALLINGS
#   WORLDS_LAND, WORLD_ONLY_LAND     -> worlds.py WORLDS_CALLINGS, WORLD_ONLY_CALLINGS
#   LIFE_LAND, LIFE_LAND_LONGSHOTS   -> engine-conditions.py LIFE_CALLINGS, LIFE_CALLINGS_LONGSHOTS
#   LIFE_LAND_WAYS                   -> or-ed onto the chair's gate, only with wa_land on
#   LONGSHOTS_LAND                   -> LONGSHOTS_CALLINGS += LONGSHOTS_LAND
#   ECHO_LAND_LONGSHOTS              -> and-ed onto both callings echoes' req (ECHO_CALLINGS_LONGSHOTS)
#   AIMS_LAND, LEGACY_LAND           -> aims.py AIMS_CALLINGS; or-ed onto LEGACY_CALLINGS
#   FIELDS_LAND                      -> fields.py FIELDS_CALLINGS
#   druid/callings-land.lib          -> callings/callings-land.lib, compiled by the Library into earth_callings.py
#   LAND_STEP1 to LAND_STEP3         -> set empty if the land is cut; the road then climbs on base titles alone
#
# Checked joined (a scratch copy of chroma-packs with every table above poured in, 10-23): see callings/PACK.md, "The
# sixth road: the steward of the land (held)".


# ================================================== catalogue
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (Green's second calling; v25 prep,
# Packs, draft 10-23). Catalogue: two titles, no new perks. Written to druid/BRIEF.md (Emren's card "Yes, no land",
# 10-19 14:57; v25.md section 6; the v25 decision file, sections 2, 5 and 8). Plain data in the fields of
# chroma-library/earth_perks_titles.py (its header defines every field); nothing is imported and nothing runs. Modern
# Earth terms; the tribal and magic forms are in WORLDS_LAND below.
#
# The road climbs from base titles, so it stands without the land in lives left alone (the v25 cut-line may take that
# out): [gardener or groundskeeper], [farm hand], [scout or guide], [outdoor instructor] and [professional beekeeper] at
# the taste rung; [farmer], [forester], [park ranger] and [professional beekeeper] for three years at the practice rung;
# then [steward of the land] (the Known rung, of the community kind: the one who chairs the town's land trust), then
# [keeper of the land] (the summit, a facet on the steward: known across the country for the land they kept), then
# [a work that outlives you] (core/legacy.py: a reserve, a wood returned, a river restored). With the land on, ten of
# land.json's ways (two led by each colour) and six of its bridges are ways onto the same rungs (AIMS_LAND,
# ROLES_LAND). It reuses [good name in town], [the one everyone asks], [knowing the woods], [friend in power],
# [apprentice of one's own], [known across the country] (core/reach.py) and [a long shot that missed]
# (core/longshot.py).
#
# Choices, on purpose (NOTES.md):
#   - The steward is of the community kind, as the brief asks and as [mayor] is: keeping a town's land is unpaid
#     civic work beside a living, not a career. It takes the community slot (one community title at a time) and carries
#     the career word in TARGET_LAND, as the faith titles do. [keeper of the land] refines it, as the other summits
#     refine their Known rung, so the steward's lose rule spares a keeper (ROLES_LAND) and the summit stays for life.
#   - Earth's words are plain: no druid on modern Earth. The land trust is "the trust"; its chair is the steward.
#   - Colour balance: three profiles each, the road's single colour and two pairs covering the other four (G | W U |
#     B R and G | W R | U B), so each title reads well for every colour. With the callings' ten titles the pack's tally
#     is W U B R 7.00 and G 8.00 (shares .194 and .222, spread .028, inside check_pack's .03): Green's second calling
#     leans the pack to G by the two singles, as Emren's card accepts.
#
# Shares: share of people in a modern rich country who ever hold it. Sources: the Land Trust Alliance's census (2020:
# about 1,300 land trusts in the United States), the county wildlife trusts' local groups, commons committees and the
# friends' groups of parks and woods, which together give about one such body a town of 10,000 to 20,000. Everything
# else is an estimate and says so. Real names stay in these comments: the moments name no real body, place or person.
#
# The outer world's keywords (chroma-engine/notes/world-fields.md, W38 and W40): institution= (an at: value; a land
# trust is a charity) and standing= (1 local, 2 inside power), as [mayor] carries them without sector=. Spheres:
# sphere= and face= on both titles.
TITLES_LAND = []

# ---------------------------------------------------------------- G: the steward of the land (sphere prod)
TITLES_LAND += [
  dict(name="steward of the land", kind="community", institution="charity", standing=1, sphere="prod",
       face="prod.G", ways="G",
       profiles=[("G", "Keeps the town's meadow, wood and river as one living whole, season after season, and lets them grow."),
                 ("W U", "Runs the land trust by its rules and its records: the counts kept, the plan written, the members heard."),
                 ("B R", "Fights the builders and the council for every field, and buys back the ones that can be bought.")],
       meets="need:meaning+.12 need:belonging+.06 res:ties+.05 res:time-.12",
       ages=(28, 95), share=.001,   # estimate: about one land, wildlife or commons trust a town of 10,000 to 20,000
                                    # (the US census counts about 1,300 land trusts; local wildlife groups and commons
                                    # committees add several times more), chaired for about ten years, with the deputy
                                    # and the warden who keep it beside the chair: about 1 life in 1,000
       say="the town's steward of the land",
       gained="'the land trust needs a chair' after years as a [farmer], [forester], [park ranger] or [professional "
              "beekeeper]; or years at the top of one of the land's ways",
       lost="handing the chair on after years; a split on the trust; age",
       needs="[farmer], [forester], [park ranger] or [professional beekeeper] for years, or a way of keeping the land "
             "held for years; [good name in town] in most towns; [knowing the woods] helps"),
  dict(name="keeper of the land", kind="community", institution="charity", standing=2, sphere="prod",
       face="prod.G", ways="G", refines="steward of the land",
       profiles=[("G", "Kept one valley's land through a lifetime, and the country comes to see what patience did there."),
                 ("W R", "Kept the land where it was hardest: the flooded valley, the poisoned river, the wood everyone wanted gone."),
                 ("U B", "Made the land a model the country copies, and the name opens every door where land is decided.")],
       meets="need:meaning+.12 need:belonging+.05 res:ties+.05 res:time-.1",
       ages=(35, 100), share=.00003,   # estimate: people known across the country for a reserve, a wood or a river they
                                       # kept or brought back, a few hundred living in a large country; higher than real,
                                       # as Emren asked for the summits (10-06 14:41), and below the other summits (.00005)
       say="a keeper of the land known across the country",
       gained="'the country comes to see the land' after years as the [steward of the land]; 'the cranes nest on the old "
              "marsh'",
       lost="never; the land kept stays in the story",
       needs="[steward of the land] for years; [good name in town] and [the one everyone asks] usually come first",
       turning="The council wants the trust's low meadow for the homes the town needs, and the vote that decides it "
               "follows the keeper's word."),
]


# ================================================== roles
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). The
# engine's reading of how the road's two titles come and go, proposed in earth_rules.ROLES syntax
# (chroma-engine/v22-speedpass/earth_rules.py, "ROLES = {"), in the shape of callings/roles.py. Plain data for the
# Engine, which owns the rules and refits every rate (ROLE_NORM, and the tier lift for careers and summits). Condition
# words are the engine's own (batch.COND_VOCAB): has('x'), was('x'), yrs_has('x'), mk('mark'), age, money, time,
# yrs_career. A name with an apostrophe is written in double quotes inside the condition.
#
# As in the other five roads, most steps are taken by the player's own act at a door or a crossing (title: on an option
# in druid/callings-land.lib), so the background rates are low and every req is narrow: years on a land trade below,
# never a perk alone (Emren 10-06 09:18, "never from nothing"). Both titles list their rungs in rungs=, so the was()
# roads (the forester who left for the city and came back to the valley) stay open. Rules are checked every four weeks,
# so odds belong in rate, never in a chance() inside req.
#
# Joined: ROLES_CALLINGS |= ROLES_LAND; the EXTEND keys are or-ed onto callings' own; TARGET likewise.

ROLES_LAND = {
    # ------------------------------------------------ G: the steward of the land (the Known rung, community kind)
    # Years on the land first: a farm or a forest for most of a working life's first half, a ranger's or a beekeeper's
    # years; then the town's trust asks. Eight years on a farm (farmers start young and the trust wants the long view),
    # six in a forest or a park (the post itself is the land's care). The perks are the ones a trust looks for: a name
    # in the town, or a hand that knows the woods, the soil, the animals or the hives.
    "steward of the land": dict(req="(age >= 28) & ((yrs_has('farmer') >= 8) | (yrs_has('forester') >= 6) | "
                                    "(yrs_has('park ranger') >= 6) | (yrs_has('professional beekeeper') >= 8)) & "
                                    "(has('good name in town') | has('knowing the woods') | has('growing food') | "
                                    "has('handling animals') | has('beekeeping'))",
                                rungs=["farmer", "forester", "park ranger", "professional beekeeper"],
                                rate=0.003, entry=True, weight="colors",
                                # the chair is handed on after years; a keeper of the land keeps it for life, so the
                                # summit (a facet on the steward) never loses its base
                                lose="~has('keeper of the land') & (yrs_has('steward of the land') >= 10)", lrate=0.05,
                                lwhy="handed the chair of the land trust on, and stayed on its committee"),
    # ------------------------------------------------ G: the keeper of the land (the summit; refines the steward)
    "keeper of the land": dict(refines="steward of the land", rungs=["steward of the land"],
                               req="has('steward of the land') & (age >= 35) & (yrs_has('steward of the land') >= 8) & "
                                   "(has('good name in town') | has('the one everyone asks') | "
                                   "has('known across the country'))",
                               rate=0.002, weight="colors"),
}

# With the land on (wa_land, v25): the land's own ways onto the Known rung, or-ed onto the steward's req at the pour,
# at the same rate. The road must stand without the land (druid/BRIEF.md: the v25 cut-line may take the land out), so
# this is kept apart and left out when the land is cut. Two ways led by each colour, at their third step (the ladder
# titles of the Library's titles-land.py, not yet in the catalogue): timber (W B) woodland manager, deer_management
# (W R) wood ranger, regen_farming (U G) model farmer, wildlife_survey (U W) county recorder, market_garden (B G) farm
# shop owner, land_dealing (B U) the town's big landowner, wood_guardian (R W) the town's land voice (the Library's
# rename of land.json's "the town's green voice"), trail_running (R G) trail builder, rewilding (G U) reserve founder,
# restore_river (G U) river trust lead. Or a land bridge held (land.json `uses.ways.bridges`: both ways at their second
# step or above): six of the fifteen whose "opens" is a keeping of land or water.
LAND_WAYS_LAND = {
    "steward of the land": (
        "(age >= 28) & ("
        "(yrs_has('woodland manager') >= 2) | (yrs_has('wood ranger') >= 2) | (yrs_has('model farmer') >= 2) | "
        "(yrs_has('county recorder') >= 2) | (yrs_has('farm shop owner') >= 2) | "
        "(yrs_has(\"the town's big landowner\") >= 2) | (yrs_has(\"the town's land voice\") >= 2) | "
        "(yrs_has('trail builder') >= 2) | (yrs_has('reserve founder') >= 2) | (yrs_has('river trust lead') >= 2) | "
        # the bridges: angling and water testing (a seat on the river trust); stalking and foraging (the keeper of an
        # estate's woods); flood warden and wood guardian (the town's voice for its land); survey and rewilding (a
        # reserve under their name); animals and soil farming (a farm others visit); land and water rights (the
        # valley's water and land)
        "((has('match angler') | has('club bailiff')) & (has('river detective') | has('water expert'))) | "
        "((has('permit holder') | has('wood ranger')) & (has('foraging guide') | has('wild food supplier'))) | "
        "((has('ward flood warden') | has('flood board member')) & (has('wood campaigner') | "
        "has(\"the town's land voice\"))) | "
        "((has('survey square holder') | has('county recorder')) & (has('land restorer') | has('reserve founder'))) | "
        "((has('smallholder') | has('show judge')) & (has('soil farmer') | has('model farmer'))) | "
        "((has('landlord of fields') | has(\"the town's big landowner\")) & (has('water rota keeper') | "
        "has('water board chair'))))"),
}

# More ways into rules the pack does not own (or-ed onto the base rule, and onto callings' own EXTEND where the key is
# already there, at the rule's own rate).
EXTEND_LAND = {
    # the summit is national news, as every pack's summit is
    "known across the country": "has('keeper of the land')",
    # the trust's chair is the town's to know
    "good name in town": "yrs_has('steward of the land') >= 2",
    # the one the valley rings about a sick tree, a flooded lane or a buyer for the low field
    "the one everyone asks": "(yrs_has('steward of the land') >= 4) | has('keeper of the land')",
}

# Fit targets (batch._targets), as TARGET_CALLINGS: the steward carries the career word though the catalogue keeps it
# of the community kind (as the faith titles carry it though they are of the faith kind); the keeper is a summit. No
# new perks, so no multiples.
TARGET_LAND = {"steward of the land": "career", "keeper of the land": "summit"}


# ================================================== helps
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). Earned
# odds: what prepares a person for each title, in the shape of callings/helps.py, after Emren's answer (10-05 21:03):
# "give more chance than real odds, but keep it consistent and achievable, if player and character create a good
# strategy, and they are at right place at right time." Plain data for the engine; nothing runs.
# Joined into callings/helps.py's three dicts.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>). Each list mixes colours, so every colour's road to the land is as well prepared as
# another's: White's kept word and the trust's rules, Blue's counts and the woods known by name, Black's land of one's
# own and friends who decide, Red's campaigns and the authority defied, Green's soil, animals, hives and neighbours.
# Marks are prefixed "mark:".

HELPS_LAND = {
    "steward of the land": ["knowing the woods", "growing food", "handling animals", "beekeeping", "good name in town",
                            "the one everyone asks", "finding things out", "neighbour who has your back",
                            "organising people", "plot of land", "campaigning", "mark:kept your word",
                            "mark:defied an authority"],
    "keeper of the land": ["good name in town", "the one everyone asks", "known across the country", "plot of land",
                           "friend in power", "voice at the town hall", "apprentice of one's own", "campaigning",
                           "mark:helped someone in need"],
}

# Windows ("right place at right time"), in the same driver words as WINDOWS_CALLINGS. community: a town that wants its
# meadow, wood and river kept by one of its own; prosper: good years fund the trust and its land; era: the country
# turns to its land, and visitors and papers follow; fortune: the person's own luck (the cranes come where they come).
WINDOWS_LAND = {
    "the land trust needs a chair": "community+.3 prosper+.1",
    "the country comes to see the land": "era+.3 fortune+.2",
    # long shot
    "the cranes nest on the old marsh": "era+.2 fortune+.3",
}

# The summit stays a long shot that preparation only softens, as the other summits: half the preparation and timing
# lifts.
LIFT_LAND = {"keeper of the land": .5}


# ================================================== worlds
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). The road
# in the other worlds, in the shape of callings/worlds.py. The catalogue stays in modern Earth terms (no druid on modern
# Earth: the steward chairs the town's land trust, the keeper is known across the country for the land they kept); this
# file gives each title its form in the game's tribal and magic worlds (chroma-game/prototype/story.py, SETTINGS and
# WORLD), so the road keeps the same shape everywhere: the same rungs, doors, steps and falls. Plain data for the
# Library and the game; nothing runs. Joined into callings/worlds.py's two dicts.
#
# The shape of the road in each world:
#   earth   farms, forests, parks and hives; the town's land trust and its committee; the reserve, the wood and the
#           river the country comes to see.
#   tribal  the band's keeper of the grove, who knows when to burn, when to leave the herds alone and which pools stay
#           clean; the great druid of the clans, whose word the bands follow on the hunting grounds and the groves.
#   magic   a druid of the grove; the archdruid of the circle, keeper of the realm's old woods.
#
# The land is never a judge (the v25 decision file, section 2): a flood, a drought or a dying river is physical, and
# people read it. Supernatural ways are possible sometimes and never forced: the world-only moment below, optional,
# with a price, and resting on someone else's power (the spirits of the deep groves and their old pact), never the
# person's own gift.
#
# Fields: tribal and magic, the form in that world; note, how it maps: "same rung" when the role exists as it is.

WORLDS_LAND = {
    "steward of the land": dict(tribal="the band's keeper of the grove", magic="a druid of the grove",
                                note="same rung"),
    "keeper of the land": dict(tribal="the great druid of the clans", magic="archdruid of the circle",
                               note="same rung"),
}

# World-only moment, optional and with a price (written in druid/callings-land.lib).
WORLD_ONLY_LAND = {
    "the circle meets at the old stones": dict(only="magic", kind="crossing",
                                               what="the druids of every grove gather at the old stones to name a new "
                                                    "archdruid; an old pact with the spirits of the deep groves can "
                                                    "win the name, at the price the spirits set"),
}


# ================================================== engine conditions
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). Proposed
# engine conditions, in the shape of callings/engine-conditions.py and earth_rules.PACK_RULES (LIFE: who a life event
# can come to, read by batch.py as the moment's gate). Plain data for the Engine, which owns PACK_RULES and may reword
# anything. JUST is earth_rules.JUST. Every name is one of this road's own moments (druid/callings-land.lib) or a
# condition the engine already reads. Joined into callings/engine-conditions.py (earth_rules.PACK_RULES['callings']).
JUST = 1 / 12   # earth_rules.JUST, as callings/engine-conditions.py has it

# The rung below (Emren 10-06 09:18; engine 10:38): a life event that gives a career or a summit comes only to someone
# on the rung below with years on it, never to a perk alone. The moments' holds: name the rungs; these gates add the
# exact years. Each gate starts at its title's first age (C-X4): the steward's ages are (28, 95), the keeper's (35,
# 100).
LIFE_LAND = {
    # the step to [steward of the land]: three years or more on a farm, in a forest or a park, or with the hives
    "the land trust needs a chair": dict(req="~has('steward of the land') & (age >= 28) & "
                                             "((yrs_has('farmer') >= 3) | (yrs_has('forester') >= 3) | "
                                             "(yrs_has('park ranger') >= 3) | "
                                             "(yrs_has('professional beekeeper') >= 3))"),
    # the step to [keeper of the land]: five years in the chair
    "the country comes to see the land": dict(req="~has('keeper of the land') & (age >= 35) & "
                                                  "(yrs_has('steward of the land') >= 5)"),
    # the world-only step (magic): three years as a druid of the grove
    "the circle meets at the old stones": dict(req="~has('keeper of the land') & (age >= 35) & "
                                                   "(yrs_has('steward of the land') >= 3)"),
}
# With the land on (wa_land), the step to the steward also comes to the top of one of the land's ways
# (LAND_WAYS_LAND): or-ed onto the gate above at the pour, and left out when the land is cut.
LIFE_LAND_WAYS = {
    "the land trust needs a chair": "~has('steward of the land') & (age >= 28) & ("
                                    "(yrs_has('woodland manager') >= 1) | (yrs_has('wood ranger') >= 1) | "
                                    "(yrs_has('model farmer') >= 1) | (yrs_has('county recorder') >= 1) | "
                                    "(yrs_has('farm shop owner') >= 1) | (yrs_has(\"the town's big landowner\") >= 1) | "
                                    "(yrs_has(\"the town's land voice\") >= 1) | (yrs_has('trail builder') >= 1) | "
                                    "(yrs_has('reserve founder') >= 1) | (yrs_has('river trust lead') >= 1))",
}

# ---------------------------------------------------------------- long shot
# A long shot is a bold try at the next rung, or a skip of at most one rung by someone with years on the rung below
# (Emren 10-06 09:18): here the steward in the chair two years, or a farmer, forester, ranger or beekeeper of eight
# years who skips the chair. Every one-colour option at chance 1 to 5 that gives a title carries
# `grants_if_fails: a long shot that missed` (core/longshot.py).
LONGSHOTS_LAND = ['the cranes nest on the old marsh']
LIFE_LAND_LONGSHOTS = {
    "the cranes nest on the old marsh": dict(
        req="~has('keeper of the land') & (age >= 35) & ((yrs_has('steward of the land') >= 2) | "
            "(yrs_has('farmer') >= 8) | (yrs_has('forester') >= 8) | (yrs_has('park ranger') >= 8) | "
            "(yrs_has('professional beekeeper') >= 8))"),
}
# The echoes: the road writes none of its own. The pour joins it to the callings' two (callings-echoes.lib, "the
# calling, years later" and "the long shot becomes a life of service"): LONGSHOTS_CALLINGS += LONGSHOTS_LAND, so their
# anchors read this moment too, and each echo's req gains the summit's bar, as it has the other five.
ECHO_LAND_LONGSHOTS = {
    "the calling, years later": dict(req_and="~has('keeper of the land')"),
    "the long shot becomes a life of service": dict(req_and="~has('keeper of the land')"),
}


# ================================================== aims (v1)
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). The
# road's ladder for aims version 1, in the shape of callings/aims.py, as druid/BRIEF.md asks (the aim "to keep the
# land", face G, domain community, sphere prod). Its v25 field is FIELDS_LAND below.
#
# The format is set out in chroma-packs/tools/check_aims.py, which checks it.
# Joined: AIMS_CALLINGS |= AIMS_LAND, and LEGACY_LAND is or-ed onto LEGACY_CALLINGS.
#
# Green's second calling (Emren's card "Yes, no land", 10-19 14:57): with the healer, the callings' six faces are W U B
# R G G, so check_aims' rule that each pack's faces are colour-even on their own will flag the callings pack (G 2 of
# 6). The card accepts the lean; NOTES.md asks the Packs thread to record the exception rather than move the face.
#
# The ladder climbs from base titles, so it stands without the land in lives left alone (the v25 cut-line may take it
# out). With the land on, ten of land.json's ways (two led by each colour) are ways onto the first three steps: their
# ladder titles are the Library's (chroma-ideas/v25-prep/library/fields/titles-land.py, TITLES_V25_LAND, and
# titles-land-extra.py), not yet in the catalogue, so check_aims names them until the Library pours them in. They stand
# apart in LAND_STEP1 to LAND_STEP3 below: with the land cut, the Packs thread sets the three lists empty and nothing
# else changes.
# The names are land.json's ladder titles as agreed with the Library (10-23): [wildlife counter] is a land title of its
# own, not the science pack's [community observer].

# The ten ways, in order: timber (W B), deer_management (W R), regen_farming (U G), wildlife_survey (U W), market_garden
# (B G), land_dealing (B U), wood_guardian (R W), trail_running (R G), rewilding (G U), restore_river (G U).
LAND_STEP1 = ["woodcutter", "club stalker", "trial farmer", "wildlife counter", "market stallholder", "landholder",
              "friend of the wood", "trail runner", "rewilder", "river volunteer"]
LAND_STEP2 = ["firewood seller", "permit holder", "soil farmer", "survey square holder", "market gardener",
              "landlord of fields", "wood campaigner", "trail racer", "land restorer", "river restorer"]
LAND_STEP3 = ["woodland manager", "wood ranger", "model farmer", "county recorder", "farm shop owner",
              "the town's big landowner", "the town's land voice", "trail builder", "reserve founder",
              "river trust lead"]

AIMS_LAND = {
    # G, the steward of the land: from hands in the soil to a land kept for good
    "to keep the land": dict(
        face="G", domain="community", sphere="prod",
        dreams=["to make one's town a green and fair place to live", "to keep the band together through the hard seasons",
                "a lasting peace between the town and the forest folk"],
        tribal="to be the great druid of the clans, who keeps the grove and the hunting grounds whole",
        magic="to be archdruid of the circle, keeper of the realm's old woods",
        steps=[
            dict(say="hands in the soil", any=["gardener or groundskeeper", "farm hand", "scout or guide",
                                               "outdoor instructor", "professional beekeeper"] + LAND_STEP1),
            dict(say="keeper of one stretch", any=["farmer", "forester", "park ranger",
                                                   "professional beekeeper"] + LAND_STEP2,
                 req=" | ".join(["(yrs_has('farmer') >= 3)", "(yrs_has('forester') >= 3)",
                                 "(yrs_has('park ranger') >= 3)", "(yrs_has('professional beekeeper') >= 3)"] +
                                [f"was({x!r})" for x in LAND_STEP2])),
            dict(say="the town's steward of the land", any=["steward of the land"] + LAND_STEP3, height="Known"),
            dict(say="a keeper of the land, known across the country", any=["keeper of the land"], height="Notable"),
            dict(say="a land kept for good", any=["a work that outlives you"],
                 req="was('keeper of the land') | (yrs_has('steward of the land') >= 15)", height="Historic"),
        ]),
}

# Who on this road can earn [a work that outlives you] (core/legacy.py): a keeper of the land for years (a reserve, a
# wood returned, a river restored), or a steward in the chair for half a working life with the town's good name.
LEGACY_LAND = ("(age >= 40) & ((yrs_has('keeper of the land') >= 5) | "
               "((yrs_has('steward of the land') >= 15) & has('good name in town')))")


# ================================================== field (v2)
# Chroma content pack: The Five Callings, sixth road: THE STEWARD OF THE LAND (v25 prep, Packs, draft 10-23). The aim
# field (aims version 2): "to keep the land" of AIMS_LAND above as a field on the Engine's land shape, with a clock on
# every rung, written to the Packs' field brief (chroma-ideas/v25-prep/packs/fields/BRIEF.md).
# Joined: FIELDS_CALLINGS |= FIELDS_LAND (callings/fields.py marks the place).
#
# The format is the Engine's frozen aims shape: chroma-engine/notes/v25/aims-shape.md, sections 3 and 8 (the chess
# entry, key for key, with demand, window, upkeep, prep and meets); chroma-packs/tools/check_fields.py checks it. Shape
# `land` with five rungs (aims-shape.md section 2: tending, keeping, stewarding, guarding, a land kept for good; "the
# druid all 5", the Engine 10-23 18:05), none skipped. v1 is kept exactly: the name, face, sphere, domain, dreams (v1's
# three, then six more from the Library's dreams.py that grow into the land: none is in core/dreams.py's AIM_DREAMS),
# tribal and magic, and each step's say, any, req and height. calling=True: the road leads to a height.
#
# Clocks. `years` is (median, 10th, 90th percentile) of steady effort from the rung below, set from land.json's
# ladder_years for the ten ways (chroma-world/spheres/data/land.json, uses.ways.list: first steps 1 to 2.5 years,
# second 3.5 to 7.5, third 10 to 20), from the years the road's own rules ask (ROLES_LAND: a steward from 28 after 8
# years farming or 6 in a forest or a park; a keeper after 8 years in the chair) and from its gates
# (LIFE_LAND: the chair's moment after 3 years on the land, the summit's after 5 in the chair), and
# core/legacy.py through LEGACY_LAND (5 years a keeper, or 15 in the chair). A rung's low is never below the years its
# moment's gate asks. `share` is of those who keep at it, the share who reach the rung, so the shares multiply down the
# ladder; the products at the Known rung (9%) and at the top (0.14%) sit beside the healer's (12% and 0.12%) and
# against TITLES_LAND's share= (the steward about 1 life in 1,000, the keeper 3 in 100,000). `start` puts best_to
# above the youngest first age of rung 1's names ([scout or guide] from 6). `demand` hours are free hours a week
# outside paid work (where the rung's title is the job, a farm or a forest, only the extra: the college course, the
# work parties, the committee); money and entry are shares of a year's free money. `window` only where the step has
# outside timing (the trust elects its chair at its yearly meeting), `upkeep` only where a benefit fades without use (a
# tenancy, a licence to graze or fell, the contacts of a post). All of these are estimates unless a source is named.
# Words a player reads name no real body, place or person, and no colour.

# The ten land ways onto the first three rungs are LAND_STEP1 to LAND_STEP3 above (with the land cut, set them empty).
FIELDS_LAND = {
    # G, the steward of the land. Clock: land.json's ladder_years for the ten ways (above); a farm hand's or a
    # groundskeeper's first year, an agricultural or forestry course of 1 to 3 years and the 3 years at the trade that
    # the practice rung asks; the chair after 6 to 8 years on the land (ROLES_LAND; its gate from 3); the summit
    # after 8 years in the chair (its gate from 5); a reserve, a wood or a river kept for good after 5 years known
    # (LEGACY_LAND). Shares: estimate, against the catalogue's (the steward .001, the keeper .00003).
    "to keep the land": dict(
        shape="land", face="G", sphere="prod", domain="community", calling=True,
        dreams=["to make one's town a green and fair place to live", "to keep the band together through the hard seasons",
                "a lasting peace between the town and the forest folk",
                "to live off the land, owing nothing to anyone", "a farmer", "to know every bird by its song",
                "to walk the lands of the ancestors", "a keeper of the old grove", "a ranger of the borderlands"],
        thing="the land", doing="keeping the land", contest="the spring count",
        places=["prod.land", "prod.wild", "rule.counsel"], prep=["the land", "organising"], meets=["meaning", "belonging"],
        people=dict(coach="an old farmer who has laid the same hedges for fifty years",
                    rival="a developer with plans for the low fields",
                    peer="the work party that meets on the first Saturday of every month",
                    patron="a landowner who wants the estate kept after they are gone"),
        round=["the volunteer days of the wildlife trust in the next valley", "a neighbour's field, rented by the year",
               "the work party on the common, on the first Saturday of every month"],
        below="{N} carries frogspawn from the drying puddle to the pond in a jam jar, three trips before tea",
        tribal="to be the great druid of the clans, who keeps the grove and the hunting grounds whole",
        magic="to be archdruid of the circle, keeper of the realm's old woods",
        rungs=[
            # land.json's first steps take 1 to 2.5 years (median 1 to 1.5); a farm hand's or a groundskeeper's first
            # season; interest starts with the children who keep tadpoles and dens (from 8), best by 25, and late after
            # 45 (estimate)
            dict(say="hands in the soil", any=["gardener or groundskeeper", "farm hand", "scout or guide",
                                               "outdoor instructor", "professional beekeeper"] + LAND_STEP1,
                 years=(1.5, 1, 3), share=0.9, start=(8, 25, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.4), window=None, upkeep=None),
            # a land college course of 1 to 3 years and the 3 years at the trade the rung asks (AIMS_LAND's req);
            # land.json's second steps 3.5 to 7.5 years. A tenancy, a grazing or felling licence and a post's contacts
            # lapse after about 4 years unused (estimate)
            dict(say="keeper of one stretch", any=["farmer", "forester", "park ranger",
                                                   "professional beekeeper"] + LAND_STEP2,
                 req=" | ".join(["(yrs_has('farmer') >= 3)", "(yrs_has('forester') >= 3)",
                                 "(yrs_has('park ranger') >= 3)", "(yrs_has('professional beekeeper') >= 3)"] +
                                [f"was({x!r})" for x in LAND_STEP2]),
                 years=(5, 3, 9), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.08, entry=0.2, energy=0.6), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["work", "the land"])),
            # the chair after 6 to 8 years on the land (ROLES_LAND), its moment's gate from 3; land.json's third
            # steps 10 to 20 years from the start. The trust elects its chair at its yearly meeting (estimate: a month's
            # notice of nominations)
            dict(say="the town's steward of the land", any=["steward of the land"] + LAND_STEP3, height="Known",
                 years=(7, 3, 14), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.5),
                 window=dict(every=1, open_weeks=4), upkeep=None),
            # 8 years in the chair (ROLES_LAND), the moment's gate from 5; known across the country is rare (the
            # catalogue's keeper is 3 in 100 stewards): estimate
            dict(say="a keeper of the land, known across the country", any=["keeper of the land"], height="Notable",
                 years=(10, 5, 22), share=0.05, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=10, money=0.05, entry=0.05, energy=0.6), window=None, upkeep=None),
            # core/legacy.py through LEGACY_LAND: 5 years a keeper, or 15 in the chair; buying the last fields for a
            # reserve is the step's real cost (estimate)
            dict(say="a land kept for good", any=["a work that outlives you"],
                 req="was('keeper of the land') | (yrs_has('steward of the land') >= 15)", height="Historic",
                 years=(8, 5, 18), share=0.3, contests_y=0, forks=["pay", "go_on"],
                 demand=dict(hours=6, money=0.05, entry=0.15, energy=0.45), window=None, upkeep=None),
        ]),
}
