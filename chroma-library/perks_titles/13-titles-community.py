# ---------- community: one at a time ([team captain] follows [on the team])
TITLES += [
  dict(name="on the team", kind="community", sphere="gather", face="gather.R", ways="R G",
       meets="need:belonging+.08 need:competence+.03 res:health+.05 res:time-.08",
       ages=(7, 60), share=.5,   # estimate: about half of young people play on an organised team at some point
       say="on the team",
       gained="'tryouts for the team', 'sports day', 'a band or a sport that takes over your life'",
       lost="being dropped, an injury, leaving school, growing out of it",
       needs="turning up on Saturday mornings"),
  dict(name="scout or guide", kind="community", sphere="learn", face="learn.G", ways="W G",
       meets="need:belonging+.08 need:competence+.03 res:time-.05",
       ages=(6, 18), share=.2,   # estimate
       say="a scout",
       gained="a friend brings them along to the hall on a Tuesday; 'summer camp'",
       lost="growing out of it, 'the family moves to a new town'",
       needs="age 6 or more"),
  dict(name="prefect", kind="community", sphere="learn", face="learn.W", ways="W U",
       meets="need:competence+.03 need:belonging+.03 need:meaning+.03 res:time-.03",
       ages=(10, 18), share=.1,   # estimate
       say="a prefect",
       gained="'a teacher offers you a role of responsibility', 'you are picked for something special'",
       lost="leaving school, or losing the badge for breaking the rules",
       needs="[teachers' favourite]"),
  dict(name="team captain", kind="community", sphere="gather", face="gather.R", ways="R B",
       meets="need:belonging+.08 need:competence+.05 need:meaning+.03 res:health+.05 res:time-.1",
       ages=(10, 50), share=.12,   # estimate
       say="the captain",
       gained="picked by the coach or voted in by the team after 'tryouts for the team'",
       lost="a loss of form or nerve, a new captain, leaving the team",
       needs="[on the team]"),
  dict(name="neighbourhood volunteer", kind="community", sphere="gather", face="gather.G", ways="G W",
       meets="need:belonging+.08 need:meaning+.05 res:ties+.05 res:time-.05",
       ages=(12, 100), share=.35,   # about 1 adult in 4 in England volunteers formally at least once a year
                                    # (Community Life Survey); estimate for holding it as a role
       say="a volunteer",
       gained="'a volunteer drive in your neighbourhood', 'a young neighbour needs help'",
       lost="a busier job, a move, a falling-out with the organisers",
       needs="nothing but a free Saturday"),
  dict(name="union rep", kind="community", sphere="prod", face="prod.W", ways="W R",
       meets="need:meaning+.05 need:belonging+.05 need:safety-.02 res:time-.05",
       ages=(20, 67), share=.03,   # estimate
       say="the union rep",
       gained="elected by workmates after 'a wave of layoffs at work', or 'they ask you to lead because you stood up once'",
       lost="losing the vote, leaving the job, being eased out",
       needs="a job with a union; 'defied an authority' helps"),
  dict(name="local councillor", kind="community", sphere="rule", ways="W B",
       profiles=[("W B", "Serves the town through its rules and knows how the council's power works."),
                 ("R G", "Fights for the street they grew up on, loud and stubborn."),   # third and second: packs
                 ("U B", "Reads every planning paper and catches what the officers missed.")],   # thread 22:20, Library
       meets="need:meaning+.05 need:competence+.03 need:safety-.02 res:ties+.05 res:time-.1",
       ages=(18, 90), share=.01,   # estimate: about 1 adult in 500 in England sits on a council, parish ones included
       say="a councillor",
       gained="a campaign on doorsteps and a vote; 'your town faces a change you could fight'",
       lost="losing the next election, a scandal, standing down",
       needs="[good name in town]; age 18 or more"),
  dict(name="youth coach", kind="community", sphere="learn", face="learn.R", ways="R U",
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(18, 80), share=.06,   # estimate
       say="a coach",
       gained="the old coach quits and a parent on the touchline is asked to take over",
       lost="their own children growing out of the team, 'burnout'",
       needs="[on the team] once; a [coaching badge] in most clubs"),
  dict(name="residents' committee member", kind="community", sphere="rule", face="rule.G", ways="B G",
       meets="need:belonging+.05 need:safety+.03 need:autonomy+.02 res:time-.05",
       ages=(25, 100), share=.05,   # estimate
       say="on the residents' committee",
       gained="'a seat on the residents' committee', often after 'break-ins on the street'",
       lost="moving away, a row at the meeting, standing down",
       needs="[homeowner] or a long tenancy"),
  dict(name="club treasurer", kind="community", sphere="gather", face="gather.B", ways="U B",
       meets="need:competence+.05 need:belonging+.05 res:ties+.03 res:time-.05",
       ages=(18, 90), share=.05,   # estimate: sports clubs, choirs, allotment societies and the like
       say="the club treasurer",
       gained="'the club or congregation asks you to lead', and nobody else will take the books",
       lost="an audit that goes badly, standing down at the yearly meeting, a move",
       needs="[bookkeeping]; [reliable record]"),
  dict(name="club member", kind="community", ways="W R",
       meets="need:belonging+.08 need:competence+.03 res:ties+.05 res:time-.05",
       ages=(16, 100), share=.4,   # estimate: a grown-up's first club, the commonest first community title for adults
                                   # (engine 10:15: neighbourhood volunteer took most community starts)
       say="a member of a club",
       gained="a friend's invitation to a running club, a choir, a five-a-side side, a chess club or a book group",
       lost="a move, a busier job or a new baby, a falling-out, the club folding",
       needs="a free evening a week"),
  dict(name="in a street gang", kind="community", ways="B R G",
       meets="need:belonging+.1 need:autonomy+.02 need:safety-.08 res:freedom-.05 res:health-.05",
       ages=(12, 30), share=.03,   # estimate: US youth surveys find several teenagers in 100 who were ever in a gang;
                                   # fewer in most rich countries
       say="in a gang",
       gained="drifting in through older friends on the estate after 'a fight after school' or 'money runs out at home'",
       lost="growing up, moving away, prison, a death that changes everything",
       needs="age 12 or more"),
]

