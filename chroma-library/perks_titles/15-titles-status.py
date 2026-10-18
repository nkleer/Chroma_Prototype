# ---------- status: any number at once, no colors (ways=""), out of the color balance; lasts is "life" or the years
# a status lasts by itself
TITLES += [
  dict(name="graduate", kind="status", ways="",
       meets="need:competence+.05 res:money+.05", lasts="life",
       ages=(20, 110), share=.4,   # about 4 adults in 10 aged 25 to 64 hold a tertiary degree (OECD average)
       say="a graduate",
       gained="three or four years of study, 'exams are coming' every spring, then 'earning a qualification'",
       lost="never",
       needs="'you win a scholarship or a place'; [school-leaving certificate]"),
  dict(name="veteran", kind="status", ways="",
       meets="need:belonging+.03 need:meaning+.03 res:health-.03", lasts="life",
       ages=(19, 110), share=.05,   # as [soldier]: nearly everyone who serves becomes a veteran
       say="a veteran",
       gained="leaving the forces after a term of service",
       lost="never",
       needs="[soldier]"),
  dict(name="has killed in war", kind="status", ways="",
       meets="need:safety-.05 need:meaning-.03 need:belonging+.03 res:health-.05", lasts="life",
       ages=(18, 110), share=.01,   # estimate: few soldiers of rich countries today; many more in the world-war
                                    # generations
       say="a soldier who has killed in war",
       gained="'war comes', and a day under fire",
       lost="never",
       needs="[soldier]"),
  dict(name="has taken a life", kind="status", ways="",   # next batch (Emren 21:00, "By choice, rarely"); granted by the engine
       meets="need:safety-.05 need:meaning-.05 need:belonging-.05 res:ties-.05", lasts="life",
       ages=(16, 110), share=.004,   # estimate: US homicide offending runs about 5 in 100,000 people a year (FBI, BJS), most
                                     # offenders kill once; deaths caused at the wheel and killings in defence add a little
       say="someone who has taken a life",
       gained="a death outside war that the person caused: in defence, in a fight gone wrong, at the wheel, or by choice; "
              "never told in detail",
       lost="never",
       needs="a moment that brings a person there; [someone with a record] follows for about half"),
  dict(name="widowed", kind="status", ways="",   # granted by the engine
       meets="need:belonging-.1 need:safety-.05 need:autonomy+.03 res:ties-.05", lasts="life",
       ages=(18, 110), share=.3,   # estimate: about 4 women in 10 over 65 are widows, far fewer men
       say="a widow or widower",
       gained="'your partner dies'",
       lost="[married again] takes its place in the story, though the loss stays",
       needs="[wife or husband] or [partner of many years]"),
  dict(name="retiree", kind="status", ways="",   # granted by the engine
       meets="need:autonomy+.08 need:competence-.03 need:meaning-.03 res:time+.15 res:money-.05", lasts="life",
       ages=(50, 110), share=.75,   # estimate: most people reach 65, and most who do retire
       say="retired",
       gained="'the first months of retirement', "
              "after 'a party for twenty-five years in the job' that turns into a farewell",
       lost="going back to work",
       needs="a career held for years; a [workplace pension] makes it easier"),
  dict(name="homeowner", kind="status", ways="",
       meets="need:safety+.08 need:autonomy+.05 res:money-.05 res:time-.03", lasts="life",
       ages=(20, 110), share=.7,   # estimate: about 2 households in 3 own their home in the UK and US; more do at
                                   # some point in life
       say="a homeowner",
       gained="'buying a home': a mortgage signed with shaking hands; or 'an unexpected legacy'",
       lost="'losing the home', selling up, 'moving to a smaller home or into care'",
       needs="[savings] for a deposit and [good credit]"),
  dict(name="newcomer", kind="status", ways="",   # granted by the engine
       meets="need:belonging-.08 need:autonomy+.03 res:ties-.08", lasts=2,
       ages=(0, 110), share=.6,   # estimate: most people move to a new town at least once
       say="new in town",
       gained="'the family moves to a new town', or a move for work or love ('moved away')",
       lost="two years of making friends; 'welcomed into a community'",
       needs="a move"),
  dict(name="immigrant", kind="status", ways="",
       meets="need:belonging-.05 need:safety-.03 need:autonomy+.03 res:ties-.08 res:money-.03", lasts="life",
       ages=(0, 110), share=.14,   # foreign-born people are about 14% of the population across rich OECD countries
                                   # (OECD)
       say="an immigrant",
       gained="a visa and a one-way ticket ('moved away'), then 'the first months in a new country'; or the "
              "family's move abroad when they were small",
       lost="never; [citizenship] changes what it costs",
       needs="a reason to leave and a country that lets them in"),
  dict(name="someone with a record", kind="status", ways="",
       meets="need:safety-.03 res:freedom-.1 res:money-.03", lasts="life",
       ages=(10, 110), share=.15,   # estimate: UK and US counts of people with any conviction run from about 1 adult
                                    # in 5 to 1 in 3, minor ones included; fewer in much of Europe
       say="someone with a record",
       gained="a conviction after 'broke the law': 'a chance to make money on the side, not quite legal' that went "
              "wrong, or 'a night out that gets out of hand'",
       lost="in some countries a minor record is spent after some years; otherwise never",
       needs="an offence and a court"),
  dict(name="ex-prisoner", kind="status", ways="",
       meets="need:belonging-.05 res:freedom-.08 res:ties-.05 res:money-.05", lasts="life",
       ages=(15, 110), share=.02,   # about 3 US adults in 100 have been in prison (Shannon et al. 2017); fewer in
                                    # most of Europe
       say="an ex-prisoner",
       gained="a prison sentence served, and the gate opening one morning",
       lost="never",
       needs="[someone with a record]"),
  dict(name="in recovery", kind="status", ways="",
       meets="need:meaning+.05 need:belonging+.03 need:safety-.03 res:health+.05", lasts="life",
       ages=(14, 110), share=.09,   # about 9% of US adults once had a drink or drug problem and no longer do
                                    # (Kelly et al. 2017)
       say="in recovery",
       gained="after 'an addiction takes hold': a first meeting, a first sober month, then the next",
       lost="a relapse; the title can be taken up again",
       needs="an addiction behind them"),
  dict(name="divorced", kind="status", ways="",
       meets="need:autonomy+.05 need:belonging-.05 res:money-.08 res:ties-.03", lasts="life",
       ages=(18, 110), share=.28,   # about 4 marriages in 10 end in divorce in England and Wales (ONS) and the US
       say="divorced",
       gained="'divorce after twenty years', or a short marriage ended in court",
       lost="never; [married again] sits beside it",
       needs="[wife or husband]"),
  dict(name="eldest child", kind="status", ways="",
       meets="need:meaning+.03 need:competence+.03 need:autonomy-.03 res:time-.03", lasts="life",
       ages=(2, 110), share=.35,   # estimate: in families of two or three, a third to a half of the children are
                                   # the eldest
       say="the eldest child",   # 2026-10-07 (Emren's point 4): "the eldest" alone read like an elder's standing
       gained="a younger brother or sister is born, so the first-born becomes the eldest (from about age 2)",
       lost="never",
       needs="a younger sibling"),
  dict(name="carer for a parent", kind="status", ways="",
       meets="need:meaning+.05 need:belonging+.03 need:autonomy-.08 res:time-.15 res:health-.05 res:money-.05",
       lasts=5,
       ages=(10, 90), share=.25,   # 3 in 5 people in the UK become carers at some point (Carers UK); estimate for
                                   # caring for a parent
       say="a carer",
       gained="'a parent comes to stay for a week' and stays; 'a heart attack or stroke' in the family",
       lost="the parent's death, or the parent 'moving to a smaller home or into care'",
       needs="a parent who needs care"),
  dict(name="homeless", kind="status", ways="",
       meets="need:safety-.15 need:belonging-.08 res:health-.1 res:money-.05", lasts=1,
       ages=(14, 110), share=.05,   # about 7 US adults in 100 have been homeless at some point (Link et al. 1994);
                                    # estimate for rich countries
       say="homeless",
       gained="'losing the home', 'financial ruin', or a family row at sixteen and nowhere to go",
       lost="a flat through the council or a charity; a friend's sofa that turns into a room",
       needs="nowhere to go"),
  dict(name="out of work", kind="status", ways="",
       meets="need:competence-.08 need:meaning-.05 need:safety-.05 res:money-.1 res:time+.1", lasts=2,
       ages=(17, 67), share=.15,   # estimate: out of work for a year or more at some point
       say="out of work",
       gained="'losing your job', then months of 'a job interview' that goes nowhere",
       lost="'a new job at last'",
       needs="losing a job, or never finding one"),
  dict(name="cancer survivor", kind="status", ways="",
       meets="need:meaning+.05 need:safety-.03 res:health-.05", lasts="life",
       ages=(5, 110), share=.2,   # 1 person in 2 gets cancer (Cancer Research UK), and about half survive ten years
       say="a cancer survivor",
       gained="'a frightening diagnosis', months of treatment, then the all-clear",
       lost="never",
       needs="cancer, and treatment that works"),
  dict(name="left the faith", kind="status", ways="",
       meets="need:autonomy+.05 need:belonging-.05 need:meaning-.02 res:ties-.03", lasts="life",
       ages=(12, 110), share=.2,   # nearly 1 US adult in 5 was raised in a religion and now has none (Pew 2015)
       say="someone who left the faith they grew up in",
       gained="a long doubt, a scandal, a new life in a city; 'among the faith you left' tests it",
       lost="coming back",
       needs="a faith in childhood"),
]

