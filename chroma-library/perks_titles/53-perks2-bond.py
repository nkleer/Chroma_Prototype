# ---------- volume 2, bond: a person (or an animal) on the person's side; when the bond goes, what it taught fades by skill_half
PERKS += [
  dict(name="crew that has your back", kind="bond", ways="R W", odds=.05, skill_half=10, retires=None,
       ages=(16, 80), share=.12,   # estimate: a watch, a boat's crew, a kitchen brigade, a stage crew, a site gang
       say="has a crew that has their back",
       gained="a watch as a [firefighter], a crew as a [lifeboat volunteer], a [merchant seafarer] or a "
              "[stage technician], a kitchen as a [head chef]; 'a narrow escape' together",
       lost="leaving the job, the crew breaking up; what is left becomes [old comrades]",
       needs="work done together in danger or under pressure"),
  dict(name="apprentice of one's own", kind="bond", ways="U G", odds=.03, skill_half=15, retires=None,
       ages=(25, 85), share=.04,   # estimate: tradespeople and craftspeople who train an apprentice through to the end
       say="has an apprentice of their own",
       gained="years as a [machinist], a [welder], a [carpenter], a [baker] or a [tattoo artist]; "
              "'a younger colleague needs a mentor'",
       lost="the apprentice qualifies and goes their own way; what teaching taught stays",
       needs="a trade held for years; [teaching] helps"),
  dict(name="carers' group", kind="bond", ways="G W", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.03,   # England and Wales: about 5 million unpaid carers (Census 2021); estimate for those
                                    # who find a group
       say="has a carers' group to lean on",
       gained="'a week off from caring' found through other carers; years as a [carer for a parent], a "
              "[caregiving partner] or a [parent coordinating complex support needs]",
       lost="the caring years ending; the group folding",
       needs="a caring role"),
  dict(name="source who trusts you", kind="bond", ways="U B", odds=.04, skill_half=3, retires=None,
       ages=(18, 95), share=.005,   # estimate
       say="has a source who trusts them",
       gained="years of 'kept your word' as a [journalist] or a [civil-liberties campaigner]; "
              "'a story nobody in town has covered'",
       lost="'broke your word' once; leaving the work",
       needs="[reporting]; 'kept your word'"),
  dict(name="business partner", kind="bond", ways="B R", odds=.05, skill_half=5, retires=None,
       ages=(18, 90), share=.06,   # estimate: partnerships and co-founded firms
       say="has a business partner",
       gained="'a friend wants to start a project with you', 'a chance to start a business of your own' as a "
              "[founder of a firm] or a [shop owner]",
       lost="'betrayed by a friend or a business partner', 'financial ruin', selling up",
       needs="'made a friend'; 'took a wild risk'"),
  dict(name="godchild", kind="bond", ways="W G", odds=.02, skill_half=15, retires=None,
       ages=(16, 100), share=.2,   # estimate: christenings and naming days are rarer than they were
       say="has a godchild",
       gained="'asked to stand for a child at the naming' by a sister, a brother or a [friend for life]",
       lost="a falling-out with the parents, a move far away",
       needs="[friend for life] or family who ask"),
  dict(name="cat of one's own", kind="bond", ways="U G", odds=.02, skill_half=3, retires=None,
       ages=(4, 110), share=.45,   # about 1 UK adult in 4 owns a cat (PDSA, PAW Report 2024), about 1 US household in 3
                                   # (APPA); estimate over a life
       say="has a cat",
       gained="a kitten as 'a pet of your own', a kitten from a neighbour, a cat from the shelter of an "
              "[animal-shelter campaigner]",
       lost="'your pet dies'; a move to a flat that bans pets",
       needs="a home that allows one"),
  dict(name="people from home", kind="bond", ways="G B", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.08,   # estimate: immigrants and incomers who find their own people in a new city
       say="has people from home nearby",
       gained="'moved away' to a new city, a shop that sells the food of home, 'welcomed into a community' of others "
              "who came as an [immigrant] or a [refugee]",
       lost="another move; 'came home'",
       needs="'moved away', or [immigrant]"),
]

