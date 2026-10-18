# ---------- asset: what the person owns; when it is gone it is gone (skill_half None)
PERKS += [
  dict(name="savings", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(10, 110), share=.5,   # estimate: three months' pay or more put by, at some point in life
       say="has savings put by",
       gained="'a cushion of your own', saving from 'your first pocket money', 'money worries end'",
       lost="'a bill you did not expect', 'financial ruin', 'a sudden urge to buy something big'",
       needs="money left over at the end of the month"),
  dict(name="paid-off home", kind="asset", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(35, 110), share=.45,   # estimate
       say="owns their home outright",
       gained="the last mortgage payment, or 'an unexpected legacy'",
       lost="'losing the home', 'moving to a smaller home or into care'",
       needs="[homeowner] for years"),
  dict(name="car", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(17, 100), share=.85,   # estimate: about 3 households in 4 have a car in England, more in the US
       say="has a car",
       gained="a first old banger bought with savings; 'a sudden urge to buy something big'",
       lost="a crash, 'money runs out at home', 'the doctor says to stop driving'",
       needs="[driving licence], and money for petrol"),
  dict(name="family business", kind="asset", ways="B W G", odds=0, skill_half=None, retires=None,
       ages=(14, 100), share=.07,   # estimate
       say="has the family business",
       gained="taken in by a relative who runs their own shop, or handed down at a parent's retirement",
       lost="'financial ruin', 'a dispute over an inheritance', selling up",
       needs="a family that owns one; [shop owner] or [farmer] often follows"),
  dict(name="inheritance", kind="asset", ways="G B U", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.4,   # estimate: a sum that changes something, not a keepsake
       say="has inherited money",
       gained="'a parent dies' or 'a grandparent dies', then 'an unexpected legacy'",
       lost="spent, or lost to 'a dispute over an inheritance'",
       needs="a relative with something to leave"),
  dict(name="workplace pension", kind="asset", ways="W U", odds=0, skill_half=None, retires=None,
       ages=(22, 110), share=.7,   # estimate: most UK employees are now enrolled in one
       say="has a pension",
       gained="years in a job with a scheme; 'your pension statement arrives' every spring",
       lost="cashed in early, or a firm that goes under with it",
       needs="a career title for years"),
  dict(name="plot of land", kind="asset", ways="G", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.08,   # estimate: an allotment, a field, a farm
       say="has a plot of land",
       gained="'tending an allotment' after years on the waiting list; a field inherited",
       lost="selling up, giving it up when the knees go",
       needs="a waiting list, or money"),
  dict(name="shares", kind="asset", ways="B U", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.4,   # about 6 Americans in 10 own shares, many through pensions (Gallup 2023); fewer in
                                   # Europe
       say="has money invested",
       gained="'a bonus or a raise' put to work; 'a gamble that paid asks for another'",
       lost="'a recession', cashing out",
       needs="[savings]"),
  dict(name="van and tools", kind="asset", ways="R U", odds=0, skill_half=None, retires=None,
       ages=(18, 80), share=.08,   # estimate
       say="has a van and tools",
       gained="the first year of working for themselves",
       lost="theft, a crash, selling up at retirement",
       needs="[building trade] or [trade ticket]; [driving licence]"),
  dict(name="flat to rent out", kind="asset", ways="B", odds=0, skill_half=None, retires=None,
       ages=(25, 110), share=.06,   # about 1 adult in 20 in the UK lets out property (HMRC counts about 2.8 million
                                    # landlords); estimate
       say="a landlord",
       gained="an [inheritance] or years of [savings] turned into bricks",
       lost="selling, a tenant who wrecks it, a fall in prices",
       needs="[savings] or an [inheritance]; [good credit]"),
  dict(name="place by the sea", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(25, 110), share=.08,   # estimate: a second home or a holiday caravan
       say="has a place by the sea",
       gained="savings spent at last, or a grandparent's caravan handed down",
       lost="selling it when money is short",
       needs="[savings]"),
  dict(name="scholarship", kind="asset", ways="U W", odds=0, skill_half=None, retires=25,
       ages=(11, 30), share=.08,   # estimate
       say="on a scholarship",
       gained="'you win a scholarship or a place'",
       lost="grades that slip; graduating",
       needs="'learned a skill' several times; [school-leaving certificate] for a university one"),
  dict(name="workshop", kind="asset", ways="U G", odds=0, skill_half=None, retires=None,
       ages=(14, 110), share=.15,   # estimate: a shed or garage with real tools in it
       say="has a workshop",
       gained="a shed and years of birthday tools; a grandfather's bench",
       lost="a move to a flat, a house sale",
       needs="[fixing things]"),
  dict(name="instrument of one's own", kind="asset", ways="R U", odds=0, skill_half=None, retires=None,
       ages=(5, 110), share=.2,   # estimate
       say="has an instrument of their own",
       gained="a second-hand guitar for a birthday, 'a band or a sport that takes over your life', or 'you take up "
              "an instrument or a language'",
       lost="sold when money is short",
       needs="money, or a generous relative"),
]


