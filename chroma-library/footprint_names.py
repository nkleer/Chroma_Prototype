# Footprints (plan.md workstream 3, 10-19): plain words for the six stacks the game shows (Emren 10-19 11:56: a few
# readable stacks, never thousands of symbols). A foot: item is (kind, value); the game quotes these nouns in the stack's
# one line. Person items name the real person from the cast once the engine adds them, so ROLE is only the fallback.
# Plain data, third person, timeless: no year, brand, country or real faith.

KINDS = {"person": "people", "place": "places", "means": "means", "mark": "marks", "door": "doors", "lesson": "lessons"}

ROLE = {"friend": "a friend", "rival": "a rival", "mentor": "a mentor", "prospect": "someone special",
        "neighbour": "a neighbour", "colleague": "a colleague", "boss": "a boss", "teacher": "a teacher",
        "patron": "a backer", "regular": "a regular", "keeper": "the keeper of a place", "go-between": "a go-between",
        "elder": "an elder", "parent": "a parent", "grandparent": "a grandparent", "sibling": "a brother or sister",
        "partner": "a partner", "ex": "an ex", "child": "a child", "dead": "someone gone"}

HAUNT = {"gather.house": "a home others gather in", "gather.hall": "a club room or hall", "gather.games": "a sports club",
         "gather.circle": "a circle of friends", "gather.night": "nights out", "gather.great": "the big gatherings",
         "gather.talk": "a talking group", "arts.song": "a choir or band", "arts.stage": "the stage",
         "arts.tale": "the storytellers", "arts.page": "the written page", "arts.craft": "a craft workshop",
         "arts.screen": "the screen", "faith.congregation": "a congregation", "faith.orders": "a religious order",
         "faith.seeking": "a quiet retreat", "faith.shrines": "the shrines", "learn.keeping": "the library",
         "learn.higher": "college", "care.houses": "the clinic and care homes", "comm.market": "the market",
         "comm.shop": "a shop", "comm.credit": "the bank", "prod.wild": "the outdoors", "prod.land": "the land",
         "prod.craft": "a workshop", "prot.watch": "the watch", "prot.host": "the forces",
         "prot.rescue": "the rescue volunteers", "rule.voice": "a campaign", "rule.counsel": "a council or committee"}

MEANS = {"money": "money", "time": "time", "health": "health", "ties": "closeness to people", "freedom": "freedom"}

# marks and doors: what the stack line says about one (a door's later moment is told when it opens)
MARK = {"hid a wrong": "a wrong kept hidden", "owned up": "owning up", "kept your word": "a promise kept",
        "broke your word": "a promise broken", "learned a skill": "a skill learned", "took a wild risk": "a wild risk",
        "left home": "leaving home", "stayed home": "staying close to home", "moved away": "moving away",
        "turned down a chance": "a chance turned down", "helped someone in need": "help given",
        "refused someone in need": "help refused", "made an enemy": "an enemy made", "made a friend": "a friend made",
        "defied an authority": "standing up to those in charge", "gave in to pressure": "giving in",
        "came home": "coming home", "kept it hidden": "something kept hidden", "used drugs": "drugs",
        "broke the law": "breaking the law", "took them in": "taking someone in"}


def line(kind, value):
    """The plain words for one foot: item."""
    if kind == "person":
        role, _, lost = value.partition(" ")
        return ("lost " if lost == "lost" else "") + ROLE.get(role, role)
    if kind == "place":
        return HAUNT.get(value, value)
    if kind == "means":
        res, sign = value.rstrip(".0123456789+-"), ("more " if "+" in value else "less ")
        return sign + MEANS.get(res, res)
    if kind in ("mark", "door"):
        return MARK.get(value, value)
    return value


# Which history marks count as a footprint in the marks stack (Library 10-19, the 14 marks no title or perk rule reads;
# the coordinator asked for a call on each, with the reason). A mark counts when something in the life visibly answers
# it. The 11 marks the title and perk rules read count already (tests/check_footprint.py reads them from the rules).
MARKS_WIRED = {   # read today by the engine's people and world code, so the deed shows in how others treat the character
    "owned up": "trust and the cast's view of them (engine.py, world_link_base.py)",
    "left home": "the household, distance and the leaving years (run_14_marks.py, world_people_ticks.py)",
    "stayed home": "the household and the home town's people (world_people_base.py)",
    "turned down a chance": "the doors that close and the people who offered (world_link.py, world_people_base.py)",
    "refused someone in need": "the cast's trust and the one refused (world_link.py, world_people_lives.py)",
    "gave in to pressure": "self-control and the pressure's source (engine.py)",
    "broke the law": "the law's reach: caught, records, the watch (run_08_fixes.py, world_link_base.py)",
}
MARKS_RETIRED = {   # stay history marks the engine reads as now, but never a footprint in the marks stack
    "came out": "who they love, not a deed to stack; never judged by a footprint (as the seed kinds leave it out)",
    "named their gender": "who they are, not a deed to stack (as the seed kinds leave it out)",
    "hurt someone badly": "rare and never graphic; not something the game collects or shows as a stack item",
    "took a life": "rare and never graphic; not something the game collects or shows as a stack item",
    "used drugs": "not a mark to collect; the engine's drug reading stays as it is",
    "kept it hidden": "no engine reader; it stays a door kind (back:) and an echo's condition",
    "took them in": "already a person footprint (a tie moves into the household)",
}
