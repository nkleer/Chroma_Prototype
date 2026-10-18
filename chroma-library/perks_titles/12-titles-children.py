# ---------- children: nested (three or more, single parent, grandparent come after a first child)
TITLES += [
  dict(name="mother or father", kind="children", ways="G W",
       meets="need:meaning+.12 need:belonging+.05 need:autonomy-.05 res:time-.15 res:money-.08 res:health-.03",
       ages=(14, 110), share=.8,   # 86% of US women aged 40 to 44 are mothers (Pew 2018); fewer men are fathers
       say="a parent",
       gained="'a child is born', or 'a baby on the way, planned or not'",
       lost="never quite; the daily duties ease when 'the children leave home'",
       needs="a partner, usually; or adoption"),
  dict(name="parent of three or more", kind="children", ways="G R",
       meets="need:meaning+.12 need:belonging+.08 need:autonomy-.08 res:ties+.05 res:time-.15 res:money-.12",
       ages=(20, 110), share=.22,   # about 4 US mothers in 10 have three or more (Pew 2015); far fewer in most of
                                    # Europe; estimate
       say="a parent of three",
       gained="'a child is born' for the third time, and a bigger car",
       lost="never; the house goes quiet when 'the children leave home'",
       needs="[mother or father]"),
  dict(name="single parent", kind="children", ways="B G",
       meets="need:meaning+.12 need:autonomy+.03 need:safety-.05 res:time-.15 res:money-.12 res:health-.05",
       ages=(16, 70), share=.2,   # about 1 family with children in 4 has one parent at a time (UK ONS); estimate
                                  # for ever being one
       say="a single parent",
       gained="'a breakup' or 'your partner dies' with a child at home, or a child raised alone from the start",
       lost="a new partner moving in, or the youngest growing up and leaving",
       needs="[mother or father]"),
  dict(name="stepparent", kind="children", ways="U G",
       meets="need:meaning+.05 need:belonging+.03 need:safety-.03 res:time-.08 res:money-.05",
       ages=(20, 110), share=.12,   # about 13% of US adults have a stepchild (Pew 2011)
       say="a stepparent",
       gained="'moving in with a partner' or 'getting married' to someone who already has children",
       lost="a divorce, though the bond can outlast it",
       needs="a partner with children"),
  dict(name="foster parent", kind="children", ways="W",
       meets="need:meaning+.12 need:safety-.03 res:ties+.03 res:time-.15 res:money-.03",
       ages=(25, 75), share=.015,   # estimate: well under 1 household in 100 fosters at any time
       say="a foster parent",
       gained="'you take in a child who needs a home', after training, checks and a social worker's visit",
       lost="children moving on, retirement, stopping after a hard placement",
       needs="age 21 to 25 or more, a spare room, a background check ([cleared to work with children])"),
  dict(name="adoptive parent", kind="children", ways="W U",
       meets="need:meaning+.12 need:belonging+.05 res:time-.12 res:money-.08",
       ages=(25, 110), share=.02,   # about 2 children in 100 in the US are adopted (US Census 2010); estimate
       say="an adoptive parent",
       gained="two years of forms, assessments and waiting, then a phone call; 'you take in a child who needs a home'",
       lost="never; it is for life",
       needs="age 21 or more, a stable home, a background check"),
  dict(name="grandparent", kind="children", ways="G R U",
       meets="need:meaning+.08 need:belonging+.08 res:ties+.05 res:time-.03",
       ages=(35, 110), share=.6,   # estimate: most people who live past 65 become grandparents
       say="a grandparent",
       gained="'your first grandchild'",
       lost="never",
       needs="[mother or father], and a child who has a child"),
]

