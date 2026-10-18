# ---------- credential: a licence, a certificate or a paper; it can be suspended or taken, and the skill under it stays
PERKS += [
  dict(name="driving licence", kind="credential", ways="R G", odds=0, skill_half=20, retires=None,
       ages=(17, 100), share=.85,   # about 3 adults in 4 in England hold a full licence (DfT); nearly 9 in 10 in
                                    # the US (FHWA)
       say="can drive",
       gained="lessons, a test failed once and passed the second time; 'a long car journey' as a passenger long before",
       lost="a ban for drink-driving, or 'the doctor says to stop driving'; the skill stays",
       needs="age 17 or 18; 'learned a skill'"),
  dict(name="first-aid certificate", kind="credential", ways="W R", odds=0, skill_half=3, retires=None,
       ages=(12, 100), share=.25,   # estimate
       say="knows first aid",
       gained="a day's course at work or with the scouts; it comes into its own when 'a stranger saves you, "
              "or you save one'",
       lost="it lapses after three years, and the know-how fades nearly as fast",
       needs="a day's course"),
  dict(name="passport", kind="credential", ways="R U", odds=0, skill_half=20, retires=None,
       ages=(0, 110), share=.75,   # estimate: most Britons and Europeans hold one; under half of Americans
                                   # (US State Department)
       say="has a passport",
       gained="'a trip far from home', 'a long-planned trip', a form and a photo booth",
       lost="it expires or is taken away; knowing how to travel stays",
       needs="citizenship somewhere, and the fee"),
  dict(name="school-leaving certificate", kind="credential", ways="W U", odds=0, skill_half=20, retires=None,
       ages=(16, 110), share=.85,   # about 8 adults in 10 have finished upper secondary school (OECD average)
       say="has finished school",
       gained="'exams are coming', and then they are passed",
       lost="never",
       needs="'learned a skill' several times"),
  dict(name="professional registration", kind="credential", ways="W U", odds=0, skill_half=10, retires=70,
       ages=(21, 75), share=.1,   # estimate: nurses, teachers, doctors, lawyers, engineers, social workers
       say="is registered to practise",
       gained="a degree, an exam and a yearly fee; 'earning a qualification'",
       lost="struck off after a complaint upheld, or let lapse; the knowledge stays",
       needs="[graduate]"),
  dict(name="lorry or bus licence", kind="credential", ways="R B", odds=0, skill_half=15, retires=None,
       ages=(18, 75), share=.03,   # estimate
       say="can drive a lorry",
       gained="a course paid for by an employer or out of [savings]",
       lost="a failed medical, a ban",
       needs="[driving licence]"),
  dict(name="trade ticket", kind="credential", ways="U B", odds=0, skill_half=15, retires=None,
       ages=(18, 80), share=.04,   # estimate: registered electricians, gas fitters and the like
       say="a registered tradesperson",
       gained="the end of an apprenticeship: 'earning a qualification'",
       lost="a lapsed registration, a serious fault found",
       needs="[apprentice]; [building trade]"),
  dict(name="hunting licence", kind="credential", ways="G B", odds=0, skill_half=15, retires=None,
       ages=(16, 90), share=.04,   # estimate: firearms or hunting licences
       say="holds a hunting licence",
       gained="a hunting club, a farm, a background check and a locked cabinet",
       lost="a conviction, a move to the city",
       needs="not [someone with a record]; [hunting and fishing]"),
  dict(name="motorbike licence", kind="credential", ways="R", odds=0, skill_half=15, retires=None,
       ages=(16, 85), share=.1,   # estimate
       say="rides a motorbike",
       gained="a test at sixteen or seventeen, or 'the itch to be somewhere else' at forty-five",
       lost="an accident, a ban, a partner's worry",
       needs="a basic training course"),
  dict(name="citizenship", kind="credential", ways="W B", odds=0, skill_half=None, retires=None,
       ages=(5, 110), share=.08,   # about 14 in 100 people are foreign-born and about 6 in 10 of them naturalise (OECD), so about 8 in 100 (2026-10-07; was .06)
       say="has citizenship",
       gained="years of residence as an [immigrant], a test on the history and laws, then 'the oath of citizenship'",
       lost="almost never",
       needs="[immigrant]; years of legal residence"),
  dict(name="drinks licence", kind="credential", ways="B R", odds=0, skill_half=10, retires=None,
       ages=(18, 80), share=.03,   # estimate: a personal licence to sell alcohol, for running a pub or a shop
       say="holds a licence to sell drink",
       gained="a course and a police check before taking on a pub or an off-licence",
       lost="a bad night with the police called, or the business closing",
       needs="age 18, and no serious conviction"),
  dict(name="coaching badge", kind="credential", ways="R W", odds=0, skill_half=10, retires=None,
       ages=(16, 85), share=.05,   # estimate
       say="a qualified coach",
       gained="a weekend course run by the sport's association",
       lost="it lapses",
       needs="[on the team] once"),
  dict(name="referee's badge", kind="credential", ways="W", odds=0, skill_half=10, retires=None,
       ages=(14, 75), share=.03,   # estimate
       say="a qualified referee",
       gained="a course, a rule book learned by heart, and a first match where both sides shout",
       lost="it lapses; the knees go",
       needs="[on the team] once"),
]

