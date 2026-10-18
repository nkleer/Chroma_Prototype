# ---------- faith: a religion, an ideology or a cause, held one at a time
TITLES += [
  dict(name="regular worshipper", kind="faith", sphere="faith", face="faith.W", ways="W G",
       meets="need:meaning+.08 need:belonging+.08 res:ties+.05 res:time-.03",
       ages=(5, 110), share=.3,    # estimate: about 3 Americans in 10 attend weekly (Gallup), under 1 Briton in 10;
                                   # more hold a stretch of it over a life
       say="a regular at church, mosque, temple or synagogue",
       gained="raised in it from 'starting school', or 'welcomed into a community' later in life",
       lost="drifting away, 'a scandal in the congregation', a move",
       needs="a faith held"),
  dict(name="believer on the big days", kind="faith", sphere="faith", face="faith.G", ways="U B G",
       meets="need:belonging+.05 need:meaning+.03 res:ties+.03",
       ages=(5, 110), share=.4,   # estimate: in most rich countries more people are raised in a faith and keep its
                                  # feasts, weddings and funerals than attend services (engine 10:15 asked for them)
       say="a believer on the big days",
       gained="raised in a faith at home, then drifting from the services in the teenage years while keeping the feasts",
       lost="finding a real faith ([regular worshipper], [convert]) or letting the last customs go",
       needs="raised in a faith"),
  dict(name="deacon or elder", kind="faith", sphere="faith", face="faith.W", ways="W B",
       meets="need:meaning+.1 need:belonging+.08 res:ties+.05 res:time-.08",
       ages=(30, 100), share=.03,   # estimate
       say="an elder of the congregation",
       gained="'the club or congregation asks you to lead'",
       lost="stepping down, a split in the congregation, 'a scandal in the congregation'",
       needs="[regular worshipper] for years; [known face at worship]"),
  dict(name="activist in a cause", kind="faith", sphere="rule", face="rule.R", ways="R G",
       meets="need:meaning+.1 need:belonging+.05 need:safety-.03 res:time-.08 res:freedom-.02",
       ages=(14, 100), share=.1,   # estimate
       say="an activist",
       gained="'a protest in your city', 'a sense of injustice', 'a protest to save the local hospital'",
       lost="'a cause you fought for wins', 'burnout', a job that takes every evening",
       needs="a cause that matters to them"),
  dict(name="party member", kind="faith", sphere="rule", face="rule.B", ways="B U",
       profiles=[("B U", "Joins for influence and a clear idea of how the country should run."),
                 ("W G", "Belongs to the party as to a family and a duty."),   # packs thread 22:20 (Politics pack)
                 ("R", "Joins for the fire of the cause.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.03 res:time-.03",
       ages=(16, 100), share=.06,   # estimate: under 2 adults in 100 belong to a party at a time in most of Europe
       say="a party member",
       gained="'a bitter election', or a friend's invitation to a branch meeting above a pub",
       lost="a quarrel with the leadership, letting the membership lapse",
       needs="age 14 to 16 or more"),
  dict(name="convert", kind="faith", sphere="faith", face="faith.B", ways="U B",
       meets="need:meaning+.1 need:belonging+.05 res:ties-.03",
       ages=(14, 110), share=.08,   # about a third of US adults have changed religion, most of them to none (Pew 2015);
                                   # estimate for joining a new faith
       say="a convert",
       gained="a long search, a partner's faith, 'welcomed into a community'",
       lost="leaving again",
       needs="a faith they were not raised in"),
  dict(name="seeker", kind="faith", sphere="faith", face="faith.U", ways="G U",
       meets="need:meaning+.08 need:autonomy+.03 res:time-.03",
       ages=(15, 110), share=.1,   # estimate
       say="a seeker",
       gained="'a sleepless night: is this all there is?', a meditation class, 'awe' on a mountain",
       lost="settling into one faith, or giving the search up",
       needs="nothing"),
]

