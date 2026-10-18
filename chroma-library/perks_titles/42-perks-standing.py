# ---------- standing: how others see the person; it fades by skill_half once the person is gone from view
PERKS += [
  dict(name="good name in town", kind="standing", ways="W G", odds=.05, skill_half=10, retires=None,
       ages=(16, 110), share=.3,   # estimate
       say="has a good name in town",
       gained="years of 'kept your word' and 'helped someone in need' where people can see",
       lost="'a public scandal', 'a rumour about you' that sticks; moving away suspends it",
       needs="'kept your word' and 'helped someone in need' several times"),
  dict(name="rank", kind="standing", ways="W B", odds=.05, skill_half=10, retires=65,
       ages=(20, 67), share=.12,   # estimate: a sergeant, a ward sister, a foreman, a head of department
       say="holds a rank",
       gained="'a promotion is open' and years of service behind it",
       lost="demotion, a scandal, retirement",
       needs="a career title held for years; [reliable record]"),
  dict(name="known face at worship", kind="standing", ways="G W", odds=.03, skill_half=10, retires=None,
       ages=(6, 110), share=.2,   # estimate
       say="a known face at the mosque or church",
       gained="years at the same services, 'welcomed into a community'",
       lost="drifting away, a move",
       needs="[regular worshipper]"),
  dict(name="reliable record", kind="standing", ways="W", odds=.04, skill_half=8, retires=None,
       ages=(14, 100), share=.4,   # estimate
       say="known for turning up",
       gained="'kept your word' many times; years without a missed shift",
       lost="'broke your word' once at the wrong moment",
       needs="'kept your word' several times"),
  dict(name="good credit", kind="standing", ways="B W", odds=.04, skill_half=6, retires=None,
       ages=(18, 110), share=.6,   # estimate
       say="good for a loan",
       gained="bills paid on time, a first credit card handled well",
       lost="missed payments, 'financial ruin'",
       needs="age 18 and an income"),
  dict(name="the one everyone asks", kind="standing", ways="U G", odds=.04, skill_half=10, retires=None,
       ages=(25, 110), share=.2,   # estimate
       say="the one everyone asks",
       gained="'a grown child in the family asks for advice', 'years of practice are noticed'",
       lost="a big mistake, being proved wrong in public",
       needs="'learned a skill' many times"),
  dict(name="following online", kind="standing", ways="R B", odds=.04, skill_half=2, retires=None,
       ages=(13, 100), share=.04,   # estimate: tens of thousands of followers or more
       say="has a following online",
       gained="'wanting to be noticed', and a video that spreads overnight",
       lost="a year of silence, 'a public scandal'",
       needs="a phone and nerve"),
  dict(name="name in the field", kind="standing", ways="U B", odds=.06, skill_half=10, retires=None,
       ages=(25, 110), share=.05,   # estimate
       say="known in their field",
       gained="'a breakthrough in your work', 'honoured for your life's work'",
       lost="a scandal, being overtaken by the young",
       needs="a career title for years; 'learned a skill' many times"),
  dict(name="not to be crossed", kind="standing", ways="B R", odds=.04, skill_half=8, retires=None,
       ages=(12, 100), share=.05,   # estimate
       say="is not to be crossed",
       gained="'made an enemy' and come out on top; 'a fight after school' that went their way",
       lost="losing a fight in public, going soft",
       needs="'made an enemy' several times"),
  dict(name="regular at the local", kind="standing", ways="R G", odds=.03, skill_half=5, retires=None,
       ages=(18, 110), share=.3,   # estimate: the pub, the café, the barber's
       say="a regular at the local",
       gained="years at the same table; 'a new friend at the community centre'",
       lost="the place closing, a move",
       needs="'made a friend' there"),
  dict(name="local hero", kind="standing", ways="R W", odds=.04, skill_half=10, retires=None,
       ages=(10, 110), share=.02,   # estimate
       say="a local hero",
       gained="'a stranger saves you, or you save one', with a photo in the local paper",
       lost="people forget",
       needs="'helped someone in need' and 'took a wild risk' at once"),
  dict(name="old family name", kind="standing", ways="G B", odds=.04, skill_half=25, retires=None,
       ages=(0, 110), share=.08,   # estimate
       say="from an old family in the town",
       gained="born to it, or married into it",
       lost="a family scandal, a move far away",
       needs="a family that has lived there for generations"),
  dict(name="inner circle at work", kind="standing", ways="B U", odds=.05, skill_half=3, retires=70,
       ages=(25, 75), share=.08,   # estimate
       say="in the inner circle",
       gained="'your team lands a big contract', 'you are offered the top job'",
       lost="'someone tries to push you out at work', a new boss",
       needs="a career title; a [friend in power] helps"),
  dict(name="teachers' favourite", kind="standing", ways="U W", odds=.04, skill_half=3, retires=19,
       ages=(5, 19), share=.3,   # estimate
       say="a favourite with the teachers",
       gained="'a test at school tomorrow' passed, homework always in, a hand always up",
       lost="trouble at school ('you are grounded for a week' kind of trouble), a new school",
       needs="school"),
]

