# Chroma content pack: National standing. Earned odds: what prepares a person for each seat and route asset.
# The rule is in chroma-packs/PROPOSAL.md, section 2 ("Earned odds"), as in the other packs' helps.py: for each title,
# the titles, perks and history marks that count as preparation for an act that takes it (any option with title:
# <name>, in the Library's route encounters). The more of them the person holds, the more that act's chance rises
# above the real base chance (up to about +1.0 logit when the list is complete, never above 90%). Plain data for the
# engine; nothing runs.
#
# SWITCHED OFF: nothing reads this file until the Engine adds `national` to batch.PACKS.
#
# Each list follows the route's five entries (world_fit.json "national", entry_kinds): local contribution, exceptional
# work, collaboration, institution-building and wider recognition, so a person who came by any of them is prepared,
# and none of them needs wealth, a city or a single patron. [known across the country] is one help among the others,
# never the only one. Each list mixes colours, so every colour's road to a seat is as well prepared as another's.
# Names in [brackets] in the catalogues are written here plainly; marks are prefixed "mark:".

HELPS_NATIONAL = {
    # ------------------------------------------------ the seats
    "head of a national faith body": ["head of a faith order", "senior cleric", "standing with both sides", "mediator",
                                      "a flock that follows you", "scripture", "good name in town",
                                      "known across the country", "mark:kept your word"],
    "chief scientist": ["professor", "research group leader", "a finding that held up", "a finding and its method",
                        "name in the field", "published research", "research collaborators",
                        "known across the country", "mark:owned up"],
    "director of a national laboratory": ["research facility lead", "research group leader", "celebrated inventor",
                                          "an invention in everyday use", "a working national system",
                                          "name in the field", "a loyal research team", "known across the country"],
    "editor of a national paper": ["journalist", "source who trusts you", "a record and its sources",
                                   "name in the field", "editing", "reporting", "known across the country",
                                   "mark:owned up"],
    "head of a national industry body": ["chief executive", "founder of a firm", "celebrated inventor",
                                         "a seat on boards", "investors who back you", "the voice of a whole industry",
                                         "striking a deal", "known across the country", "mark:kept your word"],
    "head of a national bank or exchange": ["chief executive", "accountant", "a seat on boards",
                                            "a portfolio of people backed", "bookkeeping", "shares",
                                            "known across the country"],
    "celebrated star of stage or sport": ["lead actor or actress", "professional athlete", "touring musician",
                                          "a lead role to remember", "a signature work and its audience",
                                          "known across the country", "a household name"],
    "head of the national parks": ["park ranger", "forester", "a stretch of land kept alive", "good name in town",
                                   "organising people", "known across the country", "mark:helped someone in need"],
    "keeper of the national heritage": ["museum curator", "archivist", "master craftsperson", "folk musician",
                                        "a living tradition kept", "name in the field", "known across the country"],
    "head of a national charity": ["community centre manager", "community-garden coordinator", "renowned healer",
                                   "a web of groups that help each other", "good name in town", "organising people",
                                   "fundraising", "known across the country", "mark:helped someone in need"],
}

# The assets an act grants without a title (HELPS_PERK, as the stage pack's amateur lead): the route's moments grant
# its asset at the "wider" step, and these prepare for it.
HELPS_PERK_NATIONAL = {
    "a standing mandate": ["head of government", "party leader", "known across the country", "mark:kept your word"],
    "a working public service": ["minister", "drafting policy", "officials who trust you", "mark:kept your word"],
    "standing with both sides": ["mediator", "head of a faith order", "calming people down", "mark:kept your word"],
    "a finding and its method": ["published research", "a finding that held up", "research collaborators",
                                 "mark:owned up"],
    "a working national system": ["celebrated inventor", "research facility lead", "an invention in everyday use"],
    "a record and its sources": ["journalist", "source who trusts you", "reporting", "mark:owned up"],
    "the voice of a whole industry": ["chief executive", "a seat on boards", "striking a deal"],
    "a firm and its people": ["magnate", "chief executive", "founder of a firm", "mark:kept your word"],
    "a portfolio of people backed": ["investors who back you", "a seat on boards", "shares"],
    "a following that turns out": ["party leader", "a following in the party", "rousing a crowd",
                                   "activist in a cause"],
    "a unit that trusts its leader": ["general", "army officer", "leading soldiers", "mentioned in dispatches"],
    "a signature work and its audience": ["lead actor or actress", "touring musician", "professional athlete",
                                          "a lead role to remember"],
    "a living tradition kept": ["master craftsperson", "folk musician", "museum curator", "archivist"],
    "a web of groups that help each other": ["community centre manager", "community-garden coordinator",
                                             "organising people", "mark:helped someone in need"],
    "a stretch of land kept alive": ["park ranger", "forester", "good name in town", "mark:helped someone in need"],
}
