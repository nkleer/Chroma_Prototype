# =============================== PERKS ===============================

# ---------- skill: what the hands, the body or the head can do; it fades by skill_half once unused
PERKS += [
  dict(name="swimming", kind="skill", ways="R G", odds=.04, skill_half=40, retires=None,
       ages=(4, 100), share=.8,   # estimate: about 1 adult in 5 in England says they cannot swim
       say="can swim",
       gained="lessons at the town pool, or a patient parent on 'a day at the beach'; "
              "'you never learned to swim' is the late chance",
       lost="only to an injury or great age",
       needs="'learned a skill'"),
  dict(name="cooking for a crowd", kind="skill", ways="G R W", odds=.04, skill_half=30, retires=None,
       ages=(10, 100), share=.35,   # estimate
       say="cooks for a crowd",
       gained="'learning to cook for yourself', a grandmother's kitchen, "
              "'a holiday meal with the whole family' at the stove",
       lost="only when the hands fail",
       needs="'learned a skill'"),
  dict(name="second language", kind="skill", ways="U R", odds=.06, skill_half=10, retires=None,
       ages=(3, 110), share=.45,   # about half of EU adults can hold a conversation in another language
                                   # (Eurobarometer 2012); fewer in the UK, far fewer in the US
       say="speaks a second language",
       gained="a parent's mother tongue, school lessons, 'a trip far from home', 'you take up an instrument or a language'",
       lost="years without speaking it",
       needs="'learned a skill' several times"),
  dict(name="musical instrument", kind="skill", ways="R U", odds=.04, skill_half=10, retires=None,
       ages=(5, 100), share=.25,   # estimate: many more start lessons than keep playing
       say="plays an instrument",
       gained="lessons as a child, 'you take up an instrument or a language', 'a band or a sport that takes over your life'",
       lost="putting it down for years",
       needs="'learned a skill' several times; an [instrument of one's own] to practise on"),
  dict(name="building trade", kind="skill", ways="U W", odds=.07, skill_half=15, retires=None,
       ages=(16, 80), share=.1,   # estimate: carpentry, plumbing, bricklaying and the like
       say="has a trade in their hands",
       gained="an apprenticeship and years on site; 'earning a qualification'",
       lost="a bad back ends the work, not the know-how",
       needs="[apprentice]; 'learned a skill' several times"),
  dict(name="fixing things", kind="skill", ways="U", odds=.03, skill_half=25, retires=None,
       ages=(10, 100), share=.45,   # estimate
       say="can fix things",
       gained="'the house needs repairs' and nobody to call; a parent's toolbox and a Saturday",
       lost="only when the hands fail",
       needs="'learned a skill'"),
  dict(name="car mechanics", kind="skill", ways="U R B", odds=.04, skill_half=12, retires=None,
       ages=(12, 90), share=.12,   # estimate
       say="knows engines",
       gained="a neighbour's shed, an old car that keeps breaking down, a garage job",
       lost="cars changing beyond recognition",
       needs="'learned a skill' several times"),
  dict(name="growing food", kind="skill", ways="G U", odds=.04, skill_half=30, retires=None,
       ages=(6, 100), share=.35,   # estimate
       say="grows food",
       gained="a grandmother's garden, 'tending an allotment', 'an afternoon in the garden'",
       lost="nothing; a flat with no garden suspends it",
       needs="a patch of earth and a season"),
  dict(name="sewing and mending", kind="skill", ways="G B", odds=.03, skill_half=30, retires=None,
       ages=(7, 100), share=.25,   # estimate
       say="can sew and mend",
       gained="taught at home or at school; 'a box of craft things and a free hour'",
       lost="eyes and fingers in old age",
       needs="'learned a skill'"),
  dict(name="public speaking", kind="skill", ways="W B", odds=.05, skill_half=8, retires=None,
       ages=(10, 100), share=.2,   # estimate
       say="can hold a room",
       gained="'a debate or contest at school', 'the school play', a best man's speech; "
              "'the club or congregation asks you to lead'",
       lost="years out of practice",
       needs="'learned a skill', and 'took a wild risk' the first time"),
  dict(name="bookkeeping", kind="skill", ways="W B", odds=.04, skill_half=10, retires=None,
       ages=(14, 100), share=.3,   # estimate
       say="keeps the books",
       gained="'a budget that will not balance' sorted at the kitchen table; "
              "'your first tax form and a stack of bills'; an evening class",
       lost="years of letting someone else do it",
       needs="'learned a skill'"),
  dict(name="boxing or martial arts", kind="skill", ways="R W", odds=.04, skill_half=8, retires=None,
       ages=(6, 75), share=.1,   # estimate
       say="can handle themselves",
       gained="a club in a church hall after 'a fight after school' or 'someone starts mocking you online'",
       lost="injury, age, stopping training",
       needs="'learned a skill' several times"),
  dict(name="dancing", kind="skill", ways="R G", odds=.03, skill_half=15, retires=None,
       ages=(4, 100), share=.3,   # estimate
       say="can dance",
       gained="'dancing at a wedding', Saturday classes, 'a festival weekend'",
       lost="the knees",
       needs="nerve"),
  dict(name="writing code", kind="skill", ways="U B", odds=.06, skill_half=5, retires=None,
       ages=(10, 90), share=.1,   # estimate
       say="writes code",
       gained="'a new hobby you cannot put down', a course, 'new technology changes your job'",
       lost="the tools moving on every five years",
       needs="'learned a skill' several times"),
  dict(name="drawing and painting", kind="skill", ways="R U", odds=.03, skill_half=15, retires=None,
       ages=(3, 110), share=.15,   # estimate
       say="can draw",
       gained="'a box of craft things and a free hour', 'the urge to make something', an art teacher who noticed",
       lost="years without a pencil",
       needs="'learned a skill'"),
  dict(name="home nursing", kind="skill", ways="G W", odds=.04, skill_half=20, retires=None,
       ages=(10, 100), share=.25,   # estimate
       say="knows how to nurse the sick",
       gained="being a [carer for a parent], a sick child, a friend down with 'flu, alone in a rented room'",
       lost="only forgetting",
       needs="'helped someone in need' several times"),
  dict(name="hunting and fishing", kind="skill", ways="G B", odds=.04, skill_half=20, retires=None,
       ages=(8, 90), share=.15,   # estimate
       say="can hunt and fish",
       gained="a grandparent's river at dawn, an uncle's rifle and a cold morning",
       lost="the eyes, the knees, or a move to the city",
       needs="patience; a [hunting licence] to hunt"),
  dict(name="selling", kind="skill", ways="B R", odds=.05, skill_half=10, retires=None,
       ages=(12, 90), share=.2,   # estimate
       say="can sell anything",
       gained="'a Saturday job at the corner shop', 'an idea for a side business', a year as a [salesperson]",
       lost="years away from it",
       needs="'made a friend' or 'took a wild risk'"),
  dict(name="finding things out", kind="skill", ways="U", odds=.05, skill_half=15, retires=None,
       ages=(8, 110), share=.3,   # estimate
       say="knows how to find things out",
       gained="'a curiosity that will not let go', a library card, a degree",
       lost="the mind slowing in great age",
       needs="'learned a skill'"),
  dict(name="minding small children", kind="skill", ways="W G", odds=.04, skill_half=20, retires=None,
       ages=(10, 100), share=.5,   # estimate
       say="is good with little ones",
       gained="'your little cousin comes to stay', babysitting, being a [mother or father]",
       lost="only the years",
       needs="'helped someone in need'"),
  dict(name="calming people down", kind="skill", ways="G U", odds=.05, skill_half=15, retires=None,
       ages=(12, 110), share=.2,   # estimate
       say="can calm people down",
       gained="night shifts as a [nurse], 'a teenager in your care breaks the rules', "
              "'you see a stranger being harassed' handled well",
       lost="years out of the thick of it",
       needs="'helped someone in need' several times"),
  dict(name="striking a deal", kind="skill", ways="B U", odds=.05, skill_half=10, retires=None,
       ages=(14, 100), share=.15,   # estimate
       say="drives a hard bargain",
       gained="'a bonus or a raise' asked for and won, a market stall, 'buying a home' at the right price",
       lost="years away from deals",
       needs="'took a wild risk'"),
  dict(name="scripture", kind="skill", ways="W G", odds=.03, skill_half=25, retires=None,
       ages=(6, 110), share=.15,   # estimate
       say="knows the scriptures",
       gained="years of Sunday school, madrasa or Hebrew school; being a [regular worshipper]",
       lost="only forgetting",
       needs="[regular worshipper] at some time"),
  dict(name="cards for money", kind="skill", ways="B R", odds=.03, skill_half=10, retires=None,
       ages=(14, 100), share=.1,   # estimate
       say="plays a sharp hand of cards",
       gained="a long winter of poker nights; 'a game of cards with old rivals'",
       lost="years away from the table",
       needs="'took a wild risk'"),
  dict(name="teaching", kind="skill", ways="W U R", odds=.04, skill_half=15, retires=None,
       ages=(14, 100), share=.3,   # estimate: training newcomers is part of many jobs and clubs (Library 2026-10-06, was .2)
       say="can explain anything",
       gained="'a younger colleague needs a mentor', being a [teacher] or a [youth coach]; 'years of practice are noticed'",
       lost="years of not doing it",
       needs="'learned a skill' and 'helped someone in need'"),
]

