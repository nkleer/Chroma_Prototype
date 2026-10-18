# ---------- volume 2, standing: how others see the person; it fades by skill_half once the person is gone from view
PERKS += [
  dict(name="book in print", kind="standing", ways="R U", odds=.04, skill_half=20, retires=None,
       ages=(16, 110), share=.01,   # estimate: authors of a book from a publisher, academic and local history books
                                    # included
       say="has a book in print",
       gained="a first published book as a [novelist], a history of the town, a [doctoral graduate]'s thesis turned "
              "into a book; 'the notebooks come together'",
       lost="the book going out of print and out of mind",
       needs="[writing stories] or a subject; a publisher"),
  dict(name="published research", kind="standing", ways="U W", odds=.05, skill_half=15, retires=None,
       ages=(22, 110), share=.015,   # OECD: about 9 researchers per 1,000 people in work (Main Science and Technology
                                     # Indicators); estimate for those who ever publish
       say="has published research",
       gained="a thesis as a [doctoral graduate], papers from the bench as a [laboratory technician] or from a dig as "
              "an [archaeologist]; 'a breakthrough in your work'",
       lost="a paper withdrawn; being overtaken by the young",
       needs="[graduate]; [lab work] or [archive research] often"),
  dict(name="loyal clientele", kind="standing", ways="B", odds=.05, skill_half=2, retires=None,
       ages=(18, 90), share=.06,   # estimate: about 1 worker in 7 in the EU is self-employed (Eurostat); fewer keep
                                   # regulars who follow them
       say="has a loyal clientele",
       gained="years of good work as a [tattoo artist], a [baker], a [plumber] or a [civil celebrant]; "
              "'a client asks to cut out the agency'",
       lost="giving up the work, a move away from the clients",
       needs="a career title for years; [reliable record] helps"),
  dict(name="award for bravery", kind="standing", ways="W R", odds=.03, skill_half=25, retires=None,
       ages=(8, 110), share=.004,   # estimate: medals and commendations from the services and the humane societies,
                                    # a few thousand a year in a large country
       say="has an award for bravery",
       gained="'a stranger saves you, or you save one', on a shout as a [firefighter] or a [lifeboat volunteer], or "
              "off duty; a ceremony and a framed certificate",
       lost="only 'a public scandal'",
       needs="'helped someone in need' and 'took a wild risk' at once"),
  dict(name="voice at the town hall", kind="standing", ways="W B", odds=.05, skill_half=4, retires=None,
       ages=(18, 110), share=.02,   # estimate: the people the council phones before it decides
       say="has a voice at the town hall",
       gained="years as a [school-governance board member], a [neighbourhood-watch coordinator] or a "
              "[disability-rights organiser]; 'your town faces a change you could fight'",
       lost="a move, 'a public scandal', 'a bitter election'",
       needs="[good name in town] or a cause; years in the same place"),
  dict(name="name on the local scene", kind="standing", ways="R G", odds=.04, skill_half=5, retires=None,
       ages=(16, 100), share=.03,   # estimate: music, food, art and clubs in one town
       say="a name on the local scene",
       gained="years of gigs as an [amateur band member], a [festival organiser]'s street party, a weekly show as a "
              "[community-radio presenter]",
       lost="a move to a new town; the scene moving on without them",
       needs="'made a friend' several times"),
  dict(name="trusted with the keys", kind="standing", ways="W G", odds=.03, skill_half=5, retires=None,
       ages=(18, 110), share=.2,   # estimate: keyholders of a hall, a church, a club or a neighbour's house, and of a shop or site at work (was .12)
       say="is trusted with the keys",
       gained="years as a [cleaner], a [club treasurer] or a [deacon or elder]; 'kept your word' where people could see",
       lost="'broke your word' or 'hid a wrong', found out; a move",
       needs="[reliable record]"),
  dict(name="trophies won", kind="standing", ways="R B", odds=.03, skill_half=20, retires=None,
       ages=(8, 110), share=.05,   # estimate: county, league and national titles, not a medal for taking part
       say="has trophies to their name",
       gained="seasons [on the team], 'the Saturday team wins at last', years as a [professional athlete] or in "
              "[boxing or martial arts]",
       lost="people forget",
       needs="'tryouts for the team' passed"),
]

