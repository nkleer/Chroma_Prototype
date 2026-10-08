# Chroma content pack: Politics, Elections and Public Office. The pack in the other worlds.
# Pathways and packs thread, 2026-10-05, after Emren (21:37): "Politics next, you can prioritize modern world
# conditions and terms but dont forget that applications must be feasible for other wordly setting, even including
# supernatural sometimes." The catalogue stays in modern Earth terms (the base catalogue has no worlds field); this file
# gives each title and perk its form in the game's tribal and magic worlds (chroma-game/prototype/story.py, SETTINGS
# and WORLD: "clans, hunts, elders and the turning seasons, before cities"; "towers, guilds and old powers; a gift may
# awaken"), so the pathway keeps the same shape everywhere: the same rungs, doors, crossings and falls. Plain data for
# the Library and the game; nothing runs.
#
# The shape of power in each world:
#   earth   party, ward, council, mayor, parliament, minister, party leader, head of government; votes and the press.
#   tribal  a band of a few dozen to a hundred and fifty, its families gathered in factions. Every grown person may
#           speak at the band's council fire, and the elders weigh what is said (the council). The head of the camp
#           leads between gatherings (the mayor). In summer the clans of a valley meet at the great gathering, and each
#           band sends a speaker (parliament). The chief of the gathered clans, peace-chief or war-chief, is chosen
#           there (head of government), with speakers who keep one duty each: the hunt's share, the peace, the trade
#           with other clans (ministers). Choices are made by acclaim, by standing behind a person or by casting
#           pebbles; feasts and gifts stand where money stands; singers carry what the press carries.
#   magic   walled cities and tower towns under guild and town councils (the council) and a burgomaster or lord mayor
#           (the mayor). Cities, guilds and the great Orders send members to the Assembly of the realm (parliament).
#           Councillors of the Crown and of the Orders keep the offices of the realm (ministers), and the Chancellor is
#           first councillor to the throne (head of government). The throne itself, the Archmage's ("A new Archmage
#           takes the throne, with new decrees"), lies beyond this pathway: it takes an awakened gift and an Order's
#           choosing. Court and guild factions stand where parties stand; votes are sealed lots cast in warded urns;
#           heralds and broadsheets carry the news.
#
# Supernatural ways in and out of power are possible sometimes and never forced: they come as world-only doors and
# falls (WORLD_ONLY_POLITICS below, planned in MOMENTS-BRIEF.md), each one optional, each one with a price. Modern Earth
# has no magic and no supernatural moments.
#
# Fields: tribal and magic, the form in that world (a plain phrase the story can use); note, how it maps: "same rung"
# when the role exists as it is, "nearest" when the role cannot exist there and a stand-in keeps the pathway's shape.

WORLDS_POLITICS = {
    # ------------------------------------------------ pack titles: the road to office
    "campaign organiser": dict(
        tribal="the one who goes from hearth to hearth gathering support for a speaker before the gathering",
        magic="the whip-hand of a faction in the city, who rallies the guild halls and the taverns for a candidate",
        note="same rung; in the tribal world unpaid, kept in meat and favours by the faction"),
    "constituency caseworker": dict(
        tribal="the one who carries the troubles of the families to their speaker at the fire",
        magic="a clerk of petitions to a member of the Assembly",
        note="same rung"),
    "political adviser": dict(
        tribal="the counsellor who sits behind the speaker at the fire and whispers",
        magic="secretary or counsellor to a lord, a councillor or a member of the Assembly",
        note="same rung"),
    "member of parliament": dict(
        tribal="speaker for the band at the great gathering of the clans",
        magic="a seat in the Assembly of the realm, sent by a city, a guild or an Order",
        note="same rung; a band sends one or two speakers; some Assembly seats are filled by an Order's lot"),
    "minister": dict(
        tribal="one of the chief's speakers, keeper of one duty: the hunt's share, the peace, or the trade with other "
               "clans",
        magic="a councillor of the Crown or of an Order: Keeper of the Treasury, Warden of the Roads, Master of Wards",
        note="same rung, a facet on the seat"),
    "party leader": dict(
        tribal="head of a faction of families at the gathering, the one the allied bands follow",
        magic="head of a court or guild faction in the Assembly",
        note="same rung"),
    "head of government": dict(
        tribal="chief of the gathered clans, peace-chief or war-chief, chosen at the great gathering",
        magic="Chancellor of the realm, first councillor to the throne",
        note="the summit in every world; in the magic world the throne itself lies beyond the pathway (an awakened "
             "gift and an Order's choosing)"),
    "party official": dict(
        tribal="keeper of the faction's bonds, who remembers every marriage, gift and debt between its families",
        magic="steward of a faction's house: its rolls, its coffer and its seals",
        note="same rung"),
    "lobbyist": dict(
        tribal="a go-between for another clan or for the flint-traders, pleading their case at the fire for gifts",
        magic="advocate of a guild or a merchant house at court",
        note="same rung"),
    "policy analyst": dict(
        tribal="the elder who remembers what was tried before and what came of it",
        magic="a scholar of statecraft at the academy or in the arcane archives",
        note="tribal: nearest (no trade of ideas before writing); magic: same rung"),
    "speechwriter": dict(
        tribal="the singer who shapes a speaker's words and lends them the old sayings",
        magic="a rhetor or a bard who writes for a lord",
        note="same rung"),
    "pollster": dict(
        tribal="the band's ear, who listens at every hearth and knows what the band will say before the fire is lit",
        magic="a reader of the city's mood, who tallies the guild votes; in some houses a scryer of crowds",
        note="same rung; scrying needs an awakened gift and helps only the gifted"),
    # ------------------------------------------------ pack titles: community, cause and statuses
    "campaign volunteer": dict(
        tribal="walks between the hearths for a speaker",
        magic="carries a faction's banner and tidings through the wards",
        note="same rung"),
    "polling-station volunteer": dict(
        tribal="keeper of the counting stones at the gathering, when a choice is made by casting pebbles",
        magic="a witness at the warded urns, under the Order's seal",
        note="same rung"),
    "mayor": dict(
        tribal="head of the camp, the one the band looks to between gatherings",
        magic="burgomaster or lord mayor of a walled city or a tower town",
        note="same rung"),
    "local party officer": dict(
        tribal="an elder of the faction among the families of the band",
        magic="a faction's warden in a ward or a guild hall",
        note="same rung"),
    "council candidate": dict(
        tribal="asks to be heard as a voice at the council fire",
        magic="stands for a seat on the guild or town council",
        note="same rung"),
    "parliamentary candidate": dict(
        tribal="asks the band to send them as its speaker to the gathering",
        magic="stands for a seat in the Assembly, or for an Order's lot",
        note="same rung"),
    "mayoral candidate": dict(
        tribal="asks the whole band to choose them as head of the camp, without a voice at the council fire",
        magic="stands at the lots for the burgomaster's chain, without a seat on the town council",
        note="same rung"),
    "former member of parliament": dict(
        tribal="once spoke for the band at the gathering",
        magic="once of the Assembly",
        note="same rung"),
    # ------------------------------------------------ pack perks: skills
    "canvassing": dict(tribal="going from hearth to hearth", magic="working the wards door by door", note="same"),
    "rousing a crowd": dict(tribal="stirring the gathering at the fire", magic="rousing a square or a guild hall",
                            note="same"),
    "debating": dict(tribal="arguing at the council fire", magic="disputation in the Assembly", note="same"),
    "fundraising": dict(tribal="gathering gifts for a feast", magic="raising gold from the guilds", note="same"),
    "coalition building": dict(tribal="binding bands and families together",
                               magic="binding guilds, houses and Orders together", note="same"),
    "handling the press": dict(tribal="shaping the stories the singers tell", magic="handling heralds and broadsheets",
                               note="same: the singers are the press"),
    "constituency casework": dict(tribal="taking up the grievance of a family",
                                  magic="taking a petition through the offices of the Crown", note="same"),
    "drafting policy": dict(tribal="framing a new custom for the band", magic="drafting a decree", note="same"),
    "knowing the rules of the house": dict(tribal="knowing the customs of the council fire",
                                           magic="knowing the rules and rites of the Assembly", note="same"),
    "counting the votes": dict(tribal="knowing who will stand with you", magic="counting the lots before they are cast",
                               note="same"),
    "reading the polls": dict(tribal="knowing the mood of the camp",
                              magic="reading the tallies of the guilds (the gifted may scry the crowd)", note="same"),
    "writing speeches": dict(tribal="crafting the words a speaker will say", magic="writing orations", note="same"),
    "knowing every street": dict(tribal="knowing every hearth and every family", magic="knowing every lane of the ward",
                                 note="same"),
    # ------------------------------------------------ pack perks: access
    "party nomination": dict(tribal="the blessing of the faction's elders to be heard at the council fire",
                             magic="the seal of the faction for a seat on the guild or town council", note="same"),
    "parliamentary nomination": dict(tribal="the blessing of the faction's elders to speak at the gathering for a band "
                                            "ready to stand behind the faction",
                                     magic="the seal of the faction for a seat in the Assembly it can win", note="same"),
    "the party whip": dict(tribal="a place in the faction's circle at the gathering",
                           magic="the faction's ring in the Assembly", note="same"),
    "registered lobbyist": dict(tribal="the go-between's token, a shell or a carved stone that marks a guest pleading "
                                       "for another clan",
                                magic="an advocate's licence at court",
                                note="tribal: nearest (no register before writing); magic: same"),
    "a movement behind you": dict(tribal="the young hunters behind you", magic="a guild or a brotherhood behind you",
                                  note="same"),
    "a parliamentary pass": dict(tribal="leave to sit near the council fire",
                                 magic="a pass to the halls of the Assembly, warded to its bearer", note="same"),
    # ------------------------------------------------ pack perks: standing, bonds, assets
    "a following in the party": dict(tribal="a following among the families", magic="a following in the faction",
                                     note="same"),
    "a safe seat": dict(tribal="a band that always sends someone of your family",
                        magic="a seat your house has held for generations", note="same"),
    "a reform with your name on it": dict(tribal="a custom that bears your name", magic="a decree that bears your name",
                                          note="same"),
    "a name for straight talk": dict(tribal="a name for straight talk at the fire", magic="a name for straight talk at "
                                     "court", note="same"),
    "a name as a fixer": dict(tribal="the one who settles things quietly between families", magic="a fixer at court",
                              note="same"),
    "allies in the party": dict(tribal="allies among the families", magic="allies in the faction", note="same"),
    "donors": dict(tribal="families who give to your feasts", magic="patrons in the guilds and merchant houses",
                   note="same: gifts stand for money"),
    "a loyal campaign team": dict(tribal="a band of young followers", magic="a sworn retinue", note="same"),
    "friends across the aisle": dict(tribal="friends in a rival faction", magic="friends in a rival faction",
                                     note="same"),
    "officials who trust you": dict(tribal="the old hands who carry out the chief's word and tell you the truth",
                                    magic="clerks and wardens of the Crown who trust you",
                                    note="tribal: nearest (no officials); magic: same"),
    "a campaign war chest": dict(tribal="stores laid by for a feast: dried meat, furs, ochre and shells to give",
                                 magic="a faction's coffer", note="same"),
    "a list of supporters": dict(tribal="the memory of every gift given and owed", magic="a roll of supporters",
                                 note="same"),
    # ------------------------------------------------ base titles the pathway uses
    "party member": dict(tribal="bound to a faction of families", magic="sworn to a court or guild faction",
                         note="same rung, the first step"),
    "local councillor": dict(tribal="a voice at the council fire", magic="a seat on the guild council or the town "
                             "council", note="same rung"),
    "activist in a cause": dict(tribal="one who will not let a wrong rest at the fire",
                                magic="a member of a brotherhood sworn to a cause", note="same side door"),
    "union rep": dict(tribal="the one who speaks for the hunters or the gatherers when the shares are cut",
                      magic="a guild warden who speaks for the journeymen",
                      note="tribal: nearest (no wage work); magic: same side door"),
    "residents' committee member": dict(tribal="an elder of the hearths of one part of the camp",
                                        magic="a warden of the street", note="same side door"),
    "school-governance board member": dict(tribal="an elder who watches over what the children are taught",
                                           magic="a governor of the academy",
                                           note="tribal: nearest (no schools); magic: same"),
    "civil-liberties campaigner": dict(tribal="one who speaks for the outcast at the fire",
                                       magic="a campaigner against the Order's decrees", note="same side door"),
    # ------------------------------------------------ base perks the pathway uses
    "campaigning": dict(tribal="rallying the families to a cause", magic="rallying the wards to a cause", note="same"),
    "public speaking": dict(tribal="speaking at the fire", magic="speaking in hall", note="same"),
    "organising people": dict(tribal="getting the band to move together", magic="getting a guild to move together",
                              note="same"),
    "striking a deal": dict(tribal="trading gift for gift", magic="striking a bargain", note="same"),
    "handling red tape": dict(tribal="knowing which elder to ask, and in what order",
                              magic="knowing the offices, seals and forms of the Crown",
                              note="tribal: nearest (no paperwork); magic: same"),
    "good name in town": dict(tribal="a good name in the band", magic="a good name in the city", note="same"),
    "voice at the town hall": dict(tribal="a voice the elders heed", magic="a voice at the guild hall", note="same"),
    "friend in power": dict(tribal="a friend at the chief's side", magic="a friend at court", note="same"),
    "mentor": dict(tribal="an old speaker who teaches you", magic="an old councillor who takes you on", note="same"),
    "graduate": dict(tribal="years at the elders' teaching", magic="a scholar of the academy",
                     note="tribal: nearest (no degrees); magic: same"),
    # ------------------------------------------------ the shared reach ladder (chroma-packs/core/reach.py)
    "known across the country": dict(tribal="known among all the clans of the valley", magic="known across the realm",
                                     note="same rung"),
    "a household name": dict(tribal="a name told at every fire, for generations",
                             magic="a name in every tavern song of the realm", note="same rung"),
}

# World-only doors and falls (planned in MOMENTS-BRIEF.md, part 4, "World-only moments"). Each is optional, comes
# sometimes, and has a price; none is forced. Earth has none: modern Earth has no magic.
WORLD_ONLY_POLITICS = {
    "an omen at the council fire": dict(only="tribal", kind="door",
                                        what="a sign at the fire (a hawk, a lightning strike) the elders read for or "
                                             "against a person asking to be heard"),
    "the shaman reads your dream": dict(only="tribal", kind="door",
                                        what="the shaman says a dream names the person as the band's speaker"),
    "a feast to win the families": dict(only="tribal", kind="crossing",
                                        what="giving away the stores of a season to win followers before the "
                                             "gathering"),
    "the spirits turn from the leader": dict(only="tribal", kind="fall",
                                             what="a failed hunt or a sickness blamed on the one who leads"),
    "the oracle names you": dict(only="magic", kind="door",
                                 what="an oracle's sign that the person will rise to an office of the realm"),
    "a bargain with something old": dict(only="magic", kind="door",
                                         what="something under the hill offers the seat, for a price paid later"),
    "a binding oath of office": dict(only="magic", kind="crossing",
                                     what="an oath of office that binds by magic, so breaking it has teeth"),
    "a rival's curse": dict(only="magic", kind="fall",
                            what="a rival lays a curse on an office-holder, and the office begins to slip"),
}
