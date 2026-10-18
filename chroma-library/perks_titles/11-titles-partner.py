# ---------- partner: a sequence over a life, so the shares add past 1
TITLES += [
  dict(name="girlfriend or boyfriend", kind="partner", ways="R",
       meets="need:belonging+.1 need:autonomy-.02 res:ties+.03 res:time-.05",
       ages=(12, 110), share=.9,   # estimate: nearly everyone has a sweetheart at some point
       say="someone's sweetheart",
       gained="'falling in love', 'a dating app match', a slow dance at 'a friend's wedding'",
       lost="'a breakup', or the next step: moving in, getting engaged",
       needs="someone who says yes"),
  dict(name="engaged", kind="partner", ways="W R",
       meets="need:belonging+.08 need:meaning+.05 need:safety+.03 res:money-.03",
       ages=(16, 110), share=.55,   # estimate: most first marriages follow an engagement
       say="engaged to be married",
       gained="a proposal, accepted, often a year or two after 'moving in with a partner'",
       lost="'getting married', or calling it off",
       needs="[girlfriend or boyfriend]"),
  dict(name="living together", kind="partner", ways="U B",
       meets="need:belonging+.08 need:safety+.05 need:autonomy-.05 res:money+.05 res:time-.05",
       ages=(17, 110), share=.65,   # US: close to 6 in 10 women aged 18 to 44 have lived with a partner (NSFG,
                                    # 2010s); more by the end of life
       say="living with a partner",
       gained="'moving in with a partner': two names on a lease and one set of keys too few",
       lost="'a breakup', or 'getting married'",
       needs="[girlfriend or boyfriend]"),
  dict(name="wife or husband", kind="partner", ways="W G",
       meets="need:belonging+.1 need:safety+.08 need:autonomy-.05 res:ties+.05 res:money+.03",
       ages=(16, 110), share=.7,   # estimate: about 7 in 10 people in rich countries marry at least once, fewer in
                                   # younger cohorts
       say="married",
       gained="'getting married', in a registry office or a hall full of cousins",
       lost="'divorce after twenty years', a shorter marriage ended in court, or 'your partner dies'",
       needs="usually [engaged]; a partner willing"),
  dict(name="partner of many years", kind="partner", ways="U G",
       meets="need:belonging+.1 need:safety+.1 need:meaning+.05 need:autonomy-.03 res:ties+.05",
       ages=(40, 110), share=.4,   # estimate: about half of first marriages reach 25 years, plus long unmarried couples
       say="together for many years",
       gained="'twenty-five years together', reached one ordinary day at a time",
       lost="divorce, or 'your partner dies'",
       needs="[wife or husband] or [living together] for twenty years or more; 'kept your word'"),
  dict(name="married again", kind="partner", ways="U R",
       meets="need:belonging+.1 need:safety+.08 need:autonomy-.03 res:ties+.05 res:money+.03",
       ages=(25, 110), share=.15,   # estimate: about 1 married American in 5 has been married before
       say="married again",
       gained="'a late love' or 'an old flame gets in touch' after a divorce or a death; a smaller, surer wedding",
       lost="a second divorce, a death",
       needs="[divorced] or [widowed]"),
]

