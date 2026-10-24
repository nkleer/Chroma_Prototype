# Chroma library, modern Earth: INTEGRATED ASSETS (v25 prep, draft 10-23, Library thread). Plain data; nothing runs.
# Pours into realm_earth.AIM_ASSETS (aims-shape.md section 5, "Gains"), in place of the engine's provisional table.
#
# What it is: the rare asset a life earns once, when an `integrate` moment (earth_shape_moments-integrate.lib) shows
# two of its aims used together: a shown combination, never the holding of two titles, never effort alone. Once per
# pair a life; switching aims never earns it again.
#
# Format (the engine's contract, realm_earth.py): key (a, b) by name, in either order, of two fields of FIELDS_EARTH
# or two shapes; value dict(
#   name   the asset's words as a life page shows them, a short noun phrase; {a} and {b} are the two fields' `thing`
#          words: {a} from the field (or shape) written first in the key, {b} from the other (Engine 10-23; a key is
#          looked up in either order). The slots appear only in the pairs of a shape with itself, and every field
#          pair names both sides in words,
#   title  "" or the name of a catalogue title or perk (perks_titles/) the asset grants; never one made up here,
#   opens  one plain line: what it opens (people, a place, a seat, a kind of work), never a promise,
#   rungs  (lo, hi): both aims have reached at least lo rungs and one of them at least hi; (2, 3) the usual (the
#          realm's default), (1, 2) a light combination, (3, 4) a rare one).
# The engine's own rules on top: one of the two aims pursued, age 18 or over, once per pair a life, five years between
# two assets.
# The engine reads a field pair before its shapes' pair: the 55 shape pairs below catch every combination; the field
# pairs after them are the combinations people really make, in their own words. All the words are the Library's.
# Rules kept: timeless modern, no year, brand, country, currency, real person, faith or event (faith-shape assets
# speak of a congregation and its works); no colour words, no card-game terms; no preaching; nothing unsafe.

AIM_ASSETS_EARTH = {
    # ---------------------------------------------------------------- shape pairs, in the engine's order
    ("competition", "competition"): dict(name="{a} and {b} trained as one discipline", title="",
        opens="the coaches of both, and the athletes who cross-train", rungs=(2, 3)),
    ("competition", "craft"): dict(name="equipment and food made for the training ground", title="",
        opens="the clubs that need things made, and a trade in supplying them", rungs=(2, 3)),
    ("competition", "art"): dict(name="a performance built on an athlete's training", title="",
        opens="the stage and the arena, and the people who work between them", rungs=(2, 3)),
    ("competition", "knowledge"): dict(name="a coaching method worked out and written down", title="",
        opens="the coaches who want it explained, and a place teaching on a coaching course", rungs=(2, 3)),
    ("competition", "career"): dict(name="a job in the sport's own business", title="",
        opens="the clubs' offices, the event staff and the people who hire for them", rungs=(1, 2)),
    ("competition", "cause"): dict(name="a club opened to the children who could not join", title="",
        opens="the families of the street, and the town hall's sports fund", rungs=(2, 3)),
    ("competition", "home"): dict(name="a sport the whole family trains for together", title="",
        opens="the family days at the club, and other families who play", rungs=(1, 2)),
    ("competition", "land"): dict(name="a race course laid out across the countryside", title="",
        opens="the landowners, the trusts and the runners who come to it", rungs=(2, 3)),
    ("competition", "faith"): dict(name="a congregation's team, coached with care", title="",
        opens="the congregation's teenagers, and the league its team plays in", rungs=(1, 2)),
    ("competition", "venture"): dict(name="a long race through far country, finished", title="",
        opens="the expedition teams, and the people who plan the hard routes", rungs=(3, 4)),
    ("craft", "craft"): dict(name="{a} and {b} joined in one workshop", title="",
        opens="the customers of two trades, and the makers who work across them", rungs=(2, 3)),
    ("craft", "art"): dict(name="handmade pieces shown as works of art", title="",
        opens="the galleries and craft fairs, and the buyers who collect such work", rungs=(2, 3)),
    ("craft", "knowledge"): dict(name="a maker's methods tested and set down", title="",
        opens="the colleges that teach the trade, and the researchers who study it", rungs=(2, 3)),
    ("craft", "career"): dict(name="a trade turned into a working business", title="",
        opens="regular customers, and suppliers willing to give credit", rungs=(2, 3)),
    ("craft", "cause"): dict(name="a workshop class for the street's children", title="",
        opens="the parents of the street, and the hall that lends its rooms", rungs=(1, 2)),
    ("craft", "home"): dict(name="a home built and fitted by its own household", title="",
        opens="the neighbours who ask for help, and the trades that lend tools", rungs=(2, 3)),
    ("craft", "land"): dict(name="a workshop that uses what the land grows", title="",
        opens="the farms and woods that supply it, and the markets for its goods", rungs=(2, 3)),
    ("craft", "faith"): dict(name="work made for a congregation's building", title="",
        opens="the congregation's committee, and other houses of worship needing repairs", rungs=(2, 3)),
    ("craft", "venture"): dict(name="a trade carried along on the road", title="",
        opens="workshops in far places, and travellers who need things mended", rungs=(2, 3)),
    ("art", "art"): dict(name="{a} and {b} brought into one performance", title="",
        opens="two sets of artists, and the stages that book mixed work", rungs=(2, 3)),
    ("art", "knowledge"): dict(name="an art taught with a scholar's method", title="",
        opens="the schools and lecture halls, and students who want both", rungs=(2, 3)),
    ("art", "career"): dict(name="an art that pays its own way", title="",
        opens="the bookings, the commissions and the people who hire performers", rungs=(2, 3)),
    ("art", "cause"): dict(name="a benefit show for a cause", title="",
        opens="the campaign's supporters, and the halls that host benefit nights", rungs=(1, 2)),
    ("art", "home"): dict(name="a family that performs together", title="",
        opens="family gatherings, weddings and the town's festivals", rungs=(1, 2)),
    ("art", "land"): dict(name="a festival held out on the land", title="",
        opens="the farm or field that hosts it, and performers from far around", rungs=(2, 3)),
    ("art", "faith"): dict(name="an art given to the congregation's worship", title="",
        opens="the congregation's services, and other congregations that ask", rungs=(2, 3)),
    ("art", "venture"): dict(name="performances carried from town to town", title="",
        opens="the stages of far places, and the people who book tours", rungs=(2, 3)),
    ("knowledge", "knowledge"): dict(name="{a} and {b} joined in one study", title="",
        opens="two sets of scholars, and readers who follow both fields", rungs=(3, 4)),
    ("knowledge", "career"): dict(name="expert knowledge the firm comes to rely on", title="",
        opens="the senior people at work, and offers of advisory work", rungs=(2, 3)),
    ("knowledge", "cause"): dict(name="evidence gathered for a cause, and heard", title="",
        opens="the committees that decide, and the groups that need the facts", rungs=(2, 3)),
    ("knowledge", "home"): dict(name="a household where learning is a daily habit", title="",
        opens="other parents, and the teachers at the school", rungs=(1, 2)),
    ("knowledge", "land"): dict(name="a long study of one piece of land", title="",
        opens="the trusts and researchers, and the farmers who share notes", rungs=(2, 3)),
    ("knowledge", "faith"): dict(name="scholarship the congregation turns to", title="",
        opens="the congregation's teachers, and readers from other traditions", rungs=(2, 3)),
    ("knowledge", "venture"): dict(name="field notes from far places, published", title="",
        opens="the journals, and expeditions that want someone to keep the record", rungs=(3, 4)),
    ("career", "career"): dict(name="{a} and {b} combined in one working life", title="",
        opens="two circles of colleagues, and jobs that need both", rungs=(2, 3)),
    ("career", "cause"): dict(name="professional skills given to a cause", title="",
        opens="the groups that need professional help, and a place on their boards", rungs=(2, 3)),
    ("career", "home"): dict(name="a working life arranged around the family", title="",
        opens="an employer's trust, and other working parents", rungs=(1, 2)),
    ("career", "land"): dict(name="a business built on what the land yields", title="",
        opens="the buyers, the markets and the neighbouring farms", rungs=(2, 3)),
    ("career", "faith"): dict(name="work done for the congregation's charities", title="",
        opens="the congregation's works, and the people they serve", rungs=(2, 3)),
    ("career", "venture"): dict(name="a job that travels to far places", title="",
        opens="postings in far places, and the people who work there", rungs=(2, 3)),
    ("cause", "cause"): dict(name="{a} and {b} joined in one campaign", title="",
        opens="the members of both groups, and a seat where they meet", rungs=(2, 3)),
    ("cause", "home"): dict(name="a home the neighbours gather in to organise", title="",
        opens="the street's families, and the residents' meetings", rungs=(1, 2)),
    ("cause", "land"): dict(name="a campaign won for the land around the town", title="",
        opens="the trusts, the landowners and the town hall's planners", rungs=(3, 4)),
    ("cause", "faith"): dict(name="a congregation's work for its neighbours, organised", title="",
        opens="the congregation's members, and the groups it works beside", rungs=(2, 3)),
    ("cause", "venture"): dict(name="a cause carried to far places", title="",
        opens="groups in other lands, and the people who link them", rungs=(2, 3)),
    ("home", "home"): dict(name="{a} and {b} held together in one household", title="",
        opens="the wider family, and families who ask how it is done", rungs=(1, 2)),
    ("home", "land"): dict(name="a family living from its own land", title="",
        opens="the neighbouring farms, and the market where they sell", rungs=(2, 3)),
    ("home", "faith"): dict(name="a household that keeps the congregation's customs", title="",
        opens="the congregation's families, and its festivals", rungs=(1, 2)),
    ("home", "venture"): dict(name="a family that travels together and settles anywhere", title="",
        opens="families met on the road, and friends in far places", rungs=(2, 3)),
    ("land", "land"): dict(name="{a} and {b} worked on the same ground", title="",
        opens="the farms and trusts that work the same way", rungs=(2, 3)),
    ("land", "faith"): dict(name="a congregation's garden, kept through the seasons", title="",
        opens="the congregation's members, and the people fed from its garden", rungs=(1, 2)),
    ("land", "venture"): dict(name="a route through wild country, mapped and kept", title="",
        opens="the walkers and guides, and the trusts that keep the paths", rungs=(3, 4)),
    ("faith", "faith"): dict(name="{a} and {b} brought into one practice", title="",
        opens="two circles of believers, and the people who seek both", rungs=(2, 3)),
    ("faith", "venture"): dict(name="a long journey made as a pilgrimage", title="",
        opens="the congregations along the way, and others who make the journey", rungs=(2, 3)),
    ("venture", "venture"): dict(name="{a} and {b} combined in one long journey", title="",
        opens="the travellers and guides who go that far", rungs=(3, 4)),

    # ---------------------------------------------------------------- field pairs people really make
    # teaching with something else
    ("to teach well", "to play football at the top"): dict(name="weekend football coaching for the street's children",
        title="youth coach", opens="the club's junior teams, their parents and a place on the touchline", rungs=(2, 3)),
    ("to teach well", "to win at the highest level"): dict(name="athletes coached from the club to the top",
        title="", opens="the coaches of the top squads, and rising athletes who ask", rungs=(3, 4)),
    ("to teach well", "to master an instrument"): dict(name="music lessons given at home and in schools",
        title="", opens="pupils and their families, and the schools' concerts", rungs=(2, 3)),
    ("to teach well", "to speak every language I meet"): dict(name="language classes for newcomers to the town",
        title="community language teacher", opens="newcomers and their families, and the centre that hosts the classes",
        rungs=(2, 3)),
    ("to teach well", "to study the old texts"): dict(name="weekly classes on the old texts", title="lay religious teacher",
        opens="the congregation's students, and its other teachers", rungs=(2, 3)),
    ("to teach well", "to live wild and free outdoors"): dict(name="outdoor lessons for school groups", title="",
        opens="the schools that book trips, and the centres that run them", rungs=(2, 3)),
    ("to teach well", "to master chess"): dict(name="an after-school chess club", title="",
        opens="the pupils and their parents, and the local chess league", rungs=(1, 2)),
    ("to teach well", "to cook like nobody else"): dict(name="cooking classes in the community kitchen", title="",
        opens="the kitchen's regulars, and people learning to cook on little money", rungs=(1, 2)),
    ("to teach well", "to know every root and mushroom"): dict(name="foraging walks that teach what is safe to pick",
        title="", opens="walkers and families, and the trusts that own the woods", rungs=(2, 3)),
    ("to teach well", "to dance"): dict(name="a dance class for the street's children", title="",
        opens="the children's parents, and the hall that lends its floor", rungs=(1, 2)),
    ("to teach well", "to make video games"): dict(name="a games club where children learn to code", title="",
        opens="the school's pupils and teachers, and people who make games for a living", rungs=(2, 3)),
    ("to teach well", "to be there when it counts"): dict(name="first-aid classes for the street", title="",
        opens="neighbours and parents, and the hall that hosts the classes", rungs=(1, 2)),
    ("to teach well", "to run an animal sanctuary"): dict(name="visiting days that teach children about animals",
        title="", opens="the schools that visit, and the families who come back", rungs=(1, 2)),
    # care with something else
    ("to care for those who cannot manage alone", "to stand up for the underdog"): dict(
        name="a carer's voice in the campaign for better care", title="",
        opens="the campaign's organisers, and the committees that set care standards", rungs=(2, 3)),
    ("to care for those who cannot manage alone", "to cook like nobody else"): dict(
        name="hot meals cooked for neighbours who cannot cook", title="community-kitchen volunteer",
        opens="the neighbours fed, their families, and the community kitchen", rungs=(1, 2)),
    ("to care for those who cannot manage alone", "to belong to a congregation for life"): dict(
        name="visits to the housebound, arranged through the congregation", title="",
        opens="the congregation's visitors, and the families of those visited", rungs=(1, 2)),
    ("to care for those who cannot manage alone", "to work with animals"): dict(
        name="visits with calm animals to care homes", title="",
        opens="the care homes, their residents and the staff who arrange the visits", rungs=(2, 3)),
    ("to care for those who cannot manage alone", "to take in a child who has no one"): dict(
        name="a home ready for children who need care at once", title="",
        opens="the social workers who place children, and other foster carers", rungs=(3, 4)),
    ("to care for those who cannot manage alone", "to grow the perfect garden"): dict(
        name="a quiet garden made for a care home's residents", title="",
        opens="the care home's staff, and the families who visit", rungs=(2, 3)),
    ("to care for those who cannot manage alone", "to stay strong and well for life"): dict(
        name="exercise sessions for people recovering from illness", title="",
        opens="the clinics that refer patients, and the community centre's rooms", rungs=(2, 3)),
    # garden, land and animals
    ("to feed the street from my garden", "to cook like nobody else"): dict(
        name="a street supper cooked from the garden's harvest", title="",
        opens="the street's neighbours, and a seat at the residents' table", rungs=(2, 3)),
    ("to feed the street from my garden", "to make the rules everyone lives by"): dict(
        name="a street garden run by a neighbours' committee", title="community-garden coordinator",
        opens="the town hall's parks office, and the street's growers", rungs=(2, 3)),
    ("to grow the perfect garden", "to know one thing better than anyone"): dict(
        name="garden trials recorded season after season", title="",
        opens="the gardening societies, and growers who share results", rungs=(2, 3)),
    ("to keep the family land", "to save the wild places"): dict(
        name="part of the family land given back to the wild", title="",
        opens="the conservation trusts, and the neighbours who walk it", rungs=(3, 4)),
    ("to work the land", "to know one thing better than anyone"): dict(name="field trials of new ways to farm",
        title="", opens="the farm researchers, and farmers who try the results", rungs=(3, 4)),
    ("to work the land", "to run the family business"): dict(name="a farm shop run beside the fields", title="",
        opens="the shop's regular buyers, and the neighbouring growers", rungs=(2, 3)),
    ("to run an animal sanctuary", "to stand up for the underdog"): dict(
        name="a sanctuary that speaks up for animals' care", title="",
        opens="the campaign groups, and the inspectors who check on animals' care", rungs=(2, 3)),
    ("to breed champion horses", "to win at the highest level"): dict(name="a horse bred and ridden to the top",
        title="", opens="the breeders, the trainers and the stables of the big competitions", rungs=(3, 4)),
    # peace, law and public life
    ("to be the one people come to for advice", "to keep the peace in the street"): dict(
        name="quarrels between neighbours talked through and settled", title="community-mediation volunteer",
        opens="the street's families, and the mediation service that trains volunteers", rungs=(2, 3)),
    ("to be the one people come to for advice", "to see justice done"): dict(
        name="free advice evenings for people facing the courts", title="",
        opens="the advice centre, and the lawyers who give time to it", rungs=(2, 3)),
    ("to speak every language I meet", "to see justice done"): dict(
        name="interpreting for people who cannot follow their own hearing", title="",
        opens="the courts' lists of interpreters, and the families helped", rungs=(3, 4)),
    ("to serve the public well", "to keep a sharp eye on money"): dict(
        name="the town's budget checked and explained to all", title="",
        opens="the council's finance committee, and residents who want answers", rungs=(2, 3)),
    ("to serve the public well", "to build things that last"): dict(name="a public building repaired to last",
        title="", opens="the town hall's works office, and other public buildings needing care", rungs=(2, 3)),
    ("to make the rules everyone lives by", "to save the wild places"): dict(
        name="protection won for the town's wild ground", title="",
        opens="the planning committee, and the trusts that look after the land", rungs=(3, 4)),
    ("to be famous", "to fight for what is right"): dict(name="a known name lent to a cause, and heard", title="",
        opens="the campaign's leaders, and the reporters who cover it", rungs=(2, 3)),
    # rescue and the outdoors
    ("to be there when it counts", "to live wild and free outdoors"): dict(
        name="a place on the hill rescue team", title="search-and-rescue volunteer",
        opens="the rescue team, its training nights and the other volunteers", rungs=(2, 3)),
    ("to fight in the ring", "to stand up for the underdog"): dict(name="a boxing gym open to the street's teenagers",
        title="", opens="the teenagers, their families and the social workers who refer them", rungs=(2, 3)),
    # music, dance and celebration
    ("to master an instrument", "to belong to a congregation for life"): dict(
        name="music played for the congregation's services", title="congregation musician",
        opens="the congregation's choir, and its festivals", rungs=(2, 3)),
    ("to feel something greater in the music", "to master an instrument"): dict(
        name="sacred songs accompanied and arranged", title="",
        opens="the choirs of other congregations, and singers who ask for arrangements", rungs=(2, 3)),
    ("to play in a band", "to throw the parties the town remembers"): dict(name="a summer music day the town comes to",
        title="festival organiser", opens="the bands, the town hall's events office and the local traders", rungs=(2, 3)),
    ("to play in a band", "to fight for what is right"): dict(name="songs the campaign marches to", title="",
        opens="the campaign's crowds, and the halls that host benefit nights", rungs=(2, 3)),
    ("to dance", "to stay strong and well for life"): dict(name="dance classes for older people's strength and balance",
        title="", opens="the community centre's regulars, and the health workers who send people to it", rungs=(2, 3)),
    ("to throw the parties the town remembers", "to cook like nobody else"): dict(
        name="feasts cooked for the town's big days", title="cooking for a crowd",
        opens="the town's organisers, and families who ask for weddings", rungs=(2, 3)),
    # family and home
    ("to know where we come from", "to know one thing better than anyone"): dict(
        name="a family history traced through the archives", title="archive research",
        opens="the archives and their staff, and distant relatives found", rungs=(2, 3)),
    ("to know where we come from", "to keep the family's ways"): dict(
        name="the family's recipes and stories written in one book", title="",
        opens="the wider family, and relatives who send more stories", rungs=(1, 2)),
    ("to build things that last", "to raise a family that holds together"): dict(name="a family house built room by room",
        title="", opens="the neighbours who borrow the know-how, and the local trades", rungs=(1, 2)),
    ("to build things that last", "to belong to a congregation for life"): dict(
        name="the congregation's hall repaired by its own members", title="",
        opens="the congregation's committee, and other halls in need", rungs=(2, 3)),
    ("to raise children who question everything", "to know one thing better than anyone"): dict(
        name="a home where children's questions get real answers", title="",
        opens="the children's teachers, and other curious families", rungs=(1, 2)),
    ("to make a home everyone is welcome in", "to take in a child who has no one"): dict(
        name="an open house where foster children find a family", title="",
        opens="the fostering service, and the families of the children", rungs=(2, 3)),
    ("to run the family business", "to keep the family's ways"): dict(name="the family's old ways kept in its business",
        title="", opens="the oldest customers, and buyers who want things made the old way", rungs=(2, 3)),
    # making, work and money
    ("to make video games", "to know one thing better than anyone"): dict(name="a game that teaches a subject truly",
        title="", opens="teachers and museums who want it, and studios that fund such work", rungs=(3, 4)),
    ("to race cars", "to build things that last"): dict(name="a race car built and raced by hand", title="",
        opens="the racing teams' workshops, and the mechanics of the paddock", rungs=(3, 4)),
    ("to answer to no one", "to cook like nobody else"): dict(name="a market stall selling food of one's own making",
        title="", opens="the market's regular buyers, and the other stallholders", rungs=(2, 3)),
    # travel and the far places
    ("to see the world", "to speak every language I meet"): dict(name="long journeys made in the local languages",
        title="", opens="friends in far places, and work guiding travellers", rungs=(2, 3)),
    ("to see the world", "to cook like nobody else"): dict(name="dishes learned on the road, cooked at home", title="",
        opens="the friends at the table, and cooks met along the way", rungs=(1, 2)),
    ("to explore the far places", "to know one thing better than anyone"): dict(
        name="an expedition that brings back real findings", title="",
        opens="the research societies, and expeditions that need a specialist", rungs=(3, 4)),
    # inner life
    ("to live in balance", "to stay strong and well for life"): dict(
        name="a morning practice of breath and movement, shared", title="",
        opens="the class's regulars, and the hall that hosts it", rungs=(1, 2)),
    ("to find out what is true", "to know one thing better than anyone"): dict(
        name="a question about meaning, argued carefully in print", title="",
        opens="the journals, and thinkers of other traditions", rungs=(3, 4)),
}
