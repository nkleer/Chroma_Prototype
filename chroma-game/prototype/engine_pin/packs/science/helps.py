# Chroma content pack: Science, Research and Discovery. Earned odds: what prepares a person for each title.
# Pathways and packs thread, 2026-10-05, after Emren's answer (21:03): "give more chance than real odds, but keep it
# consistent and achievable, if player and character create a good strategy, and they are at right place at right time."
# The rule is in chroma-packs/PROPOSAL.md, section 2 ("Earned odds"). Plain data for the engine; nothing runs.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>). The more of them the person holds, the more that act's chance rises above the real base
# chance, up to the cap the engine sets (proposed: about double the base, never above 90%). The same list works for
# every life, played or simulated, so the rule stays consistent; ordinary lives seldom hold many of them, so the
# shares in simulated lives stay close to the real ones.
# Names in [brackets] in the catalogues are written here plainly; marks are prefixed "mark:".

HELPS_SCIENCE = {
    "research assistant": ["graduate", "lab work", "working with data", "finding things out", "mentor",
                           "teachers' favourite", "mark:learned a skill"],
    "research scientist": ["doctoral graduate", "published research", "experimental design", "statistical judgment",
                           "mentor", "research collaborators", "institutional affiliation"],
    "research project lead": ["research grant", "grant writing", "a research project under way", "project triage",
                              "organising people", "research collaborators"],
    "research group leader": ["research grant", "published research", "name in the field", "supervising researchers",
                              "a loyal research team", "friend in power", "mark:kept your word"],
    "research facility lead": ["instrument troubleshooting", "lab work", "reliable record", "supervising researchers",
                               "trusted with the keys"],
    "independent investigator": ["published research", "a finding that held up", "research grant", "savings", "patron",
                                 "research collaborators", "mark:took a wild risk"],
    "research software engineer": ["writing code", "reproducible workflow", "automating analysis", "graduate"],
    "research data steward": ["working with data", "archive research", "reproducible workflow", "reliable record"],
    "evidence synthesis specialist": ["evidence synthesis", "statistical judgment", "finding things out", "graduate"],
    "science communication specialist": ["explaining science", "public speaking", "reporting", "following online",
                                         "published research"],
    "participatory research coordinator": ["community listening", "community partners", "organising people",
                                           "good name in town"],
    "citizen scientist": [],
    "community observer": ["knowing the woods", "fieldwork", "mark:stayed home"],
    "volunteer research organiser": ["organising people", "community listening", "good name in town",
                                     "mark:helped someone in need"],
    # Round 5, 2026-10-07 (checklist P2, P9, P16): the two appointments now have moments of their own (the postdoc in
    # 'the first week with your own bench' and 'a named fellowship, one a year'; the chair in 'they want you to lead a
    # group', 'the work you would rather be doing' and 'a chair falls vacant at another university')
    "postdoctoral researcher": ["doctoral graduate", "published research", "experimental design", "mentor",
                                "research collaborators"],
    "professor": ["published research", "name in the field", "supervising researchers", "former students",
                  "research grant", "teaching", "a finding that held up"],
}

# Windows ("right place at right time"): the crossings and doors come when an opening exists, and their rate follows
# the outside context (drivers, as on any life event). Proposed as a second, smaller lift on the act's chance when the
# context is favourable, in the same driver words; the engine decides whether to build it.
WINDOWS_SCIENCE = {
    "the contract runs out": "prosper+.3 era+.2",          # money for science in good years; posts open
    "a fellowship of your own": "prosper+.3 era+.3",
    "they want you to lead a group": "prosper+.2 era+.2",
    "the facility needs a head": "era+.2",
    "the funding call closes on Friday": "prosper+.4 harsh-.3 unrest-.3",
    "a finding that makes the news": "era+.2 unrest+.2",   # an anxious public listens to science
    # Round 5, 2026-10-07 (P9): the round 5 long shots open with the money for research, like the crossings
    "a chair falls vacant at another university": "prosper+.3 era+.2",
    "a named fellowship, one a year": "prosper+.3 era+.2",
    "a national centre opens its posts": "prosper+.3 era+.3",
}
