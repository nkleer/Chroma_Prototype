"""Seed situation library for the Chroma engine prototype.

Each situation is a recurring kind of life moment. Each option is described only by
its METHOD mix (how you act, which colors' tools you use) and, when it differs from
the default, its ENDS (which colors' values the act serves or violates).
Color effects are never authored here: the engine derives them from outcome,
expectation, agency and the person's own lens.
"""
COLORS = "WUBRG"

# (label, means, ends_override_or_None, difficulty[, tags])
# tags (v4): "req:money.3 time.2" what the option needs to be open at all; "pay:" spent when acting;
# "win:"/"lose:" resource change on success/failure; "commit:career" success starts that commitment.
# Situation keys (v4): needs="partner" (only while held), excludes="career" (only while not held),
# domain="career1 community.3" (which commitments the situation belongs to: makes it more frequent
# for holders and brings that role's expectations into the choice); rate=0.4 (how often it comes up).
# v6: per_year=(child, juvenile, young_adult, adult, mature, elder) marks a LIFE EVENT and gives its real base rate
# per year in each stage (bereavement, disaster, meeting someone...). Life events interrupt ordinary life at those
# rates; every other week brings one of the everyday situations (no per_year), drawn by rate, niche and roles.
# Event timing is never fixed (Emren 2026-10-04): each person gets their own rate for each kind of event, drawn once
# from a range around per_year (engine ev_spread), and the outside context moves it week by week through drivers:
#   family (partner, children, community held), ties, money, health (resources), era (an era in progress),
#   harsh, unrest, prosper (the world: environment, state and institutions, economy), community, stress.
# e.g. drivers="harsh+1 unrest+.8 money-.6": disasters come more often in a harsh, unstable world and to the poor.
# trouble and fortune are the person's own record: big events that went badly or well in the last few years (loss and
# gain spirals, Hobfoll; prior trauma predicts later trauma, Benjet et al. 2016).
# means/ends use compact strings: "W.6 U.4" or "W+.5 B-.4"
SITUATIONS = [
  # ---------- childhood ----------
  dict(name="playground dispute", stages="child", age=(3, 13), alpha="R.3 W.2 B.2", stakes=0.6, options=[
    ("tell the teacher", "W1", None, 0.45),
    ("work out a clever trade", "U.6 B.4", None, 0.45),
    ("take the toy", "B.7 R.3", None, 0.45),
    ("shout and shove", "R1", None, 0.45),
    ("share and play together", "G.6 W.4", None, 0.45),
    ("walk away", "G1", "G+.3", 0.45),
  ]),
  dict(name="hard school task", rite="juvenile", stages="child juvenile", age=(5, 18), alpha="U.4", stakes=0.5, options=[
    ("practise methodically", "U.7 W.3", None, 0.45),
    ("copy a classmate", "B1", None, 0.45),
    ("give up and go play", "R1", None, 0.45),
    ("study together with friends", "G.5 U.5", None, 0.45),
    ("follow the teacher's method exactly", "W1", None, 0.45),
    ("tinker with an odd approach", "U.5 R.5", None, 0.45),
  ]),
  dict(name="family rule you dislike", rite="juvenile", stages="child juvenile", age=(4, 18), alpha="W.2 R.3 B.1", stakes=0.6, options=[
    ("obey the rule", "W1", None, 0.45),
    ("argue it with reasons", "U1", None, 0.45),
    ("get round it quietly", "B.6 U.4", None, 0.45),
    ("openly defy it", "R1", None, 0.45),
    ("accept it as how our family is", "G1", None, 0.45),
  ]),
  # ---------- adolescence ----------
  dict(name="peer pressure to take a risk", rite="juvenile young_adult", stages="juvenile young_adult", age=(12, 25), alpha="R.3 G.1 B.1 W.1", stakes=0.8, options=[
    ("refuse, it breaks the rules", "W1", None, 0.45),
    ("weigh the odds first", "U1", None, 0.5),
    ("use it to gain status", "B.6 R.4", None, 0.55, "req:ties.2"),
    ("go for the thrill", "R1", None, 0.5, "req:health.4 freedom.4; lose:health-.1"),
    ("go along to belong", "G.5 R.5", None, 0.4),
    ("make a pact to look out for each other", "R.5 W.5", None, 0.55),
  ]),
  dict(name="choosing a path", per_year=(0, 0.5, 0.8, 0.3, 0.15, 0), drivers="prosper+.4 money+.3 unrest-.3 era+.3 fortune+.1", excludes="career", domain="career1", rite="young_adult adult", stages="juvenile young_adult adult mature", age=(16, 65), alpha="U.2 B.2 R.2", stakes=1.0, options=[
    ("serve the community", "W1", None, 0.5, "commit:career"),
    ("pursue a rigorous field", "U1", None, 0.5, "req:money.2 time.3; pay:money-.05; commit:career"),
    ("chase money and status", "B1", None, 0.55, "req:ties.2; commit:career"),
    ("follow your passion", "R1", None, 0.55, "req:freedom.5; commit:career"),
    ("continue the family craft", "G1", None, 0.5, "req:ties.3; commit:career"),
    ("join an institution's ranks", "W.5 U.5", None, 0.55, "commit:career"),
    ("build something wild and new", "U.5 R.5", None, 0.65, "req:money.3 time.4; lose:money-.15; commit:career"),
  ]),
  dict(name="witnessing an injustice", domain="community.3 faith.3", rite="juvenile young_adult", stages="juvenile young_adult adult mature elder", age=(10, 90), alpha="W.3 R.2 U.1", stakes=0.8, options=[
    ("report it to authority", "W1", None, 0.5),
    ("gather evidence first", "U1", None, 0.5),
    ("use what you saw as leverage", "B1", None, 0.5),
    ("step in on the spot", "R.6 W.4", None, 0.55, "req:health.3; lose:health-.05"),
    ("care for the person harmed", "G.6 W.4", None, 0.45),
    ("look away", "B.5 G.5", "B+.3 W-.4", 0.3),
  ]),
  # ---------- adulthood ----------
  dict(name="conflict at work", needs="career", domain="career1", rite="adult mature", stages="young_adult adult mature", age=(18, 70), alpha="B.3 U.2 W.1", stakes=0.9, options=[
    ("follow procedure", "W1", None, 0.5),
    ("out-think the problem", "U1", None, 0.5),
    ("manoeuvre politically", "B.7 U.3", None, 0.55),
    ("confront it head on", "R1", None, 0.55),
    ("build patient alliances", "G.6 W.4", None, 0.55),
    ("strike a binding deal", "W.5 B.5", None, 0.6),
  ]),
  dict(name="relationship strain", needs="partner", domain="partner1", rite="young_adult adult", stages="juvenile young_adult adult mature elder", age=(16, 90), alpha="R.3 G.2 W.1 U.1", stakes=1.0, options=[
    ("agree clear rules together", "W.6 U.4", None, 0.5, "req:time.1"),
    ("analyse what went wrong", "U1", None, 0.5),
    ("put your own needs first", "B1", None, 0.5),
    ("pour your heart out", "R1", None, 0.5),
    ("endure for the family", "G.7 W.3", None, 0.45),
    ("rekindle it wildly", "R.5 G.5", None, 0.55, "req:time.2"),
  ]),
  dict(name="money: windfall or squeeze", per_year=(0, 0, 0.3, 0.3, 0.3, 0.3), drivers="era+.6 unrest+.5 prosper+.3 trouble+.15 fortune+.15", domain="career.3 children.3", rite="adult", stages="young_adult adult mature elder", age=(18, 90), alpha="B.3 U.2 G.1", stakes=0.9, options=[
    ("save and give a share", "W1", None, 0.4, "pay:money-.05; win:ties+.05"),
    ("invest in learning", "U1", None, 0.5, "req:money.2 time.3; pay:money-.1"),
    ("leverage it for advantage", "B1", None, 0.55, "req:money.3; win:money+.2; lose:money-.15"),
    ("spend it on experiences", "R1", None, 0.4, "req:money.3; pay:money-.1"),
    ("invest in home and kin", "G1", None, 0.5, "req:money.25; pay:money-.1; win:ties+.05"),
    ("gather information quietly", "U.5 B.5", None, 0.55, "req:time.2; win:money+.1"),
    ("salvage and reuse what others waste", "B.5 G.5", None, 0.5, "win:money+.05"),
  ]),
  dict(name="community problem", domain="community1", rite="mature elder", stages="young_adult adult mature elder", age=(16, 90), alpha="W.2 G.2 U.2 B.1", stakes=0.8, options=[
    ("organise a committee", "W1", None, 0.5, "req:time.2 ties.3; commit:community"),
    ("design a solution", "U1", None, 0.5, "req:time.2"),
    ("profit from the gap", "B1", None, 0.5, "req:money.2; win:money+.1"),
    ("protest loudly", "R1", None, 0.5, "req:freedom.5"),
    ("revive mutual aid", "G.6 W.4", None, 0.5, "req:ties.3; commit:community"),
    ("cultivate a living fix", "G.5 U.5", None, 0.6, "req:time.3"),
  ]),
  dict(name="tempting shortcut", domain="career.3", stages="juvenile young_adult adult mature elder", age=(14, 90), alpha="B.3 U.1", stakes=0.9, options=[
    ("refuse on principle", "W1", None, 0.45),
    ("calculate the consequences", "U1", None, 0.5),
    ("take it", "B1", "B+.7 W-.5", 0.5, "win:money+.1; lose:ties-.1"),
    ("take it for the rush", "B.4 R.6", None, 0.5),
    ("refuse, it is not our way", "G1", None, 0.5),
  ]),
  dict(name="raising a child", needs="children", domain="children1", rite="adult mature", stages="young_adult adult mature", age=(22, 70), alpha="G.3 W.2 B.1", stakes=1.0, options=[
    ("set firm rules", "W1", None, 0.5),
    ("teach and explain", "U1", None, 0.5),
    ("push them to compete", "B1", None, 0.55, "req:money.2"),
    ("let them roam free", "R1", None, 0.5),
    ("raise them in our traditions", "G1", None, 0.5),
    ("let them adapt and find their nature", "G.5 U.5", None, 0.55),
  ]),
  dict(name="chance to innovate", domain="career.7", rite="mature", stages="young_adult adult mature elder", age=(16, 80), alpha="U.4 R.2", stakes=0.8, options=[
    ("standardise what works", "W.6 U.4", None, 0.5),
    ("experiment boldly", "U.5 R.5", None, 0.65, "req:time.3 money.15"),
    ("patent and monetise it", "B.6 U.4", None, 0.6, "req:money.2; win:money+.15"),
    ("improvise on instinct", "R.6 G.4", None, 0.55),
    ("keep the proven old way", "G1", None, 0.45),
  ]),
  dict(name="crisis or disaster", per_year=(0.03, 0.04, 0.05, 0.04, 0.04, 0.05), drivers="harsh+1 unrest+.8 era+.6 money-.6 health-.4 trouble+.25", domain="community.3 children.3 partner.3 faith.3", rite="juvenile young_adult adult mature elder", stages="child juvenile young_adult adult mature elder", age=(8, 90), alpha="W.2 U.2 B.2 R.2 G.2", stakes=1.3, options=[
    ("coordinate relief", "W1", None, 0.55, "req:ties.3 time.2"),
    ("plan ahead calmly", "U1", None, 0.5),
    ("secure your own first", "B1", None, 0.5),
    ("act heroically", "R.6 W.4", None, 0.6, "req:health.5; lose:health-.1"),
    ("hunker down and endure", "G1", None, 0.5),
    ("fight off whoever threatens you", "R.5 B.5", None, 0.55, "req:health.4; lose:health-.1"),
  ]),
  # ---------- later life ----------
  dict(name="bereavement", per_year=(0.05, 0.06, 0.08, 0.10, 0.15, 0.25), drivers="family+.5 ties+.4 harsh+.7 unrest+.4 era+.3", domain="partner.5 children.3 faith.5", rite="juvenile young_adult adult mature elder", stages="child juvenile young_adult adult mature elder", age=(5, 95), alpha="G.2 R.1 U.1 W.1 B.1", stakes=1.0, options=[
    ("hold the proper rites", "W.5 G.5", None, 0.4),
    ("seek to understand it", "U1", None, 0.5),
    ("channel it into ambition", "B1", None, 0.5),
    ("grieve openly and fiercely", "R1", None, 0.45),
    ("accept the cycle of life", "G1", None, 0.5),
    ("accept death, keep what remains useful", "B.5 G.5", None, 0.5),
  ]),
  dict(name="thinking about legacy", per_year=(0, 0, 0, 0, 0.2, 0.4), drivers="family+.4 health-.5", domain="children.5 community.5 faith.5", rite="elder", stages="mature elder", age=(50, 95), alpha="W.1 G.2 U.2 B.1", stakes=0.8, options=[
    ("endow an institution", "W1", None, 0.5, "req:money.5; pay:money-.15"),
    ("pass on knowledge", "U1", None, 0.5),
    ("secure wealth and name", "B1", None, 0.55, "req:money.3"),
    ("live fully while you can", "R1", None, 0.45, "req:health.3 money.2"),
    ("tend family and land", "G1", None, 0.5, "req:ties.2"),
  ]),
  # ---------- commitments (v4) ----------
  dict(name="meeting someone", per_year=(0, 0, 1.0, 0.6, 0.3, 0.15), drivers="ties+1 community+.4 fortune+.15", rite="young_adult adult", excludes="partner", domain="partner1", stages="young_adult adult mature elder", age=(16, 90), alpha="R.2 G.2 W.1 B.1", stakes=0.9, options=[
    ("court them properly and marry", "W.6 G.4", None, 0.5, "req:ties.2; commit:partner"),
    ("choose someone who thinks like you", "U1", None, 0.5, "commit:partner"),
    ("choose someone who raises your standing", "B.7 W.3", None, 0.55, "commit:partner"),
    ("fall headlong in love", "R1", None, 0.5, "commit:partner"),
    ("grow a slow bond within your circle", "G1", None, 0.5, "req:ties.3; commit:partner"),
    ("keep it casual and free", "R.5 B.5", None, 0.4, ""),
  ]),
  dict(name="deciding about children", per_year=(0, 0, 0.5, 0.5, 0, 0), drivers="ties+.3 money+.3 prosper+.2 unrest-.3", rite="adult", needs="partner", excludes="children", domain="partner.5 children1", stages="young_adult adult", age=(20, 45), alpha="G.3 W.2", stakes=1.0, options=[
    ("have children as expected of you", "W.6 G.4", None, 0.45, "commit:children"),
    ("plan the timing carefully", "U1", None, 0.5, "req:money.3; commit:children"),
    ("have them to carry on your name", "B.5 G.5", None, 0.5, "commit:children"),
    ("let it happen when it happens", "R.5 G.5", None, 0.45, "commit:children"),
    ("raise a big family", "G1", None, 0.5, "req:ties.3; commit:children"),
    ("stay child-free to keep your freedom", "R.5 B.5", None, 0.4, ""),
  ]),
  dict(name="a search for meaning", excludes="faith", domain="faith1", per_year=(0, 0.1, 0.15, 0.1, 0.1, 0.1), drivers="era+.6 stress+.6", stages="juvenile young_adult adult mature elder", age=(12, 90), alpha="W.2 U.2 G.2 R.1 B.1", stakes=0.8, options=[
    ("join a church or order", "W.7 G.3", None, 0.45, "req:ties.2; commit:faith"),
    ("build a philosophy you can defend", "U1", None, 0.55, "commit:faith"),
    ("follow a creed that promises power", "B.7 R.3", None, 0.5, "commit:faith"),
    ("give yourself to a cause that sets your heart on fire", "R.7 W.3", None, 0.5, "commit:faith"),
    ("return to an ancestral or nature faith", "G1", None, 0.5, "commit:faith"),
    ("live without a creed", "U.5 R.5", None, 0.4, ""),
  ]),
  # ---------- color combinations (v4, Emren 2026-10-04: dual and tri-color actions). One option per
  # two-color pair and per three-color group, so enemy pairs and wedges are exactly as available as allies.
  # Labels follow the core idea Magic gives each combination (see combos.py).
  # ---------- ordinary life (v6) ----------
  # Most weeks hold no drama. A person spends an ordinary week in their own way, at low stakes; needs are still met
  # (the engine does not tie need-meeting to drama). One option per color; the niche and habit decide which comes easily.
  dict(name="an ordinary week", rate=2.0, stages="child juvenile young_adult adult mature elder", age=(3, 95), alpha="", stakes=0.5, options=[
    ("keep to your duties and routines", "W1", None, 0.4),
    ("read, plan or tinker with something", "U1", None, 0.4),
    ("look after your own interests", "B1", None, 0.4),
    ("do whatever you feel like", "R1", None, 0.4),
    ("spend it with family, friends or outdoors", "G1", None, 0.4),
  ]),
  dict(name="your group must decide how to act", stages="juvenile young_adult", age=(12, 25), alpha="R.2 G.2 W.2 U.2 B.2", stakes=0.7, options=[
    ("agree on rules and a fair procedure", "W.5 U.5", None, 0.5),                 # Azorius
    ("work the angles in secret", "U.5 B.5", None, 0.5),                            # Dimir
    ("make it a party and a show", "B.5 R.5", None, 0.5),                           # Rakdos
    ("ignore the adults and do it our way", "R.5 G.5", None, 0.5),                  # Gruul
    ("make sure everyone is included", "W.5 G.5", None, 0.5),                       # Selesnya
    ("let whoever has the most pull decide, and owe them", "W.5 B.5", None, 0.5),   # Orzhov
    ("try the crazy idea and see what happens", "U.5 R.5", None, 0.55),             # Izzet
    ("drop the losers and reuse what works", "B.5 G.5", None, 0.5),                 # Golgari
    ("stand up for the one being wronged", "W.5 R.5", None, 0.5),                   # Boros
    ("study what works and adapt it", "U.5 G.5", None, 0.5),                        # Simic
  ]),
  dict(name="something is wrong where you live", rate=0.6, domain="community.6", stages="young_adult adult mature elder", age=(18, 90), alpha="W.2 U.2 B.2 R.2 G.2", stakes=0.9, options=[
    ("write clear rules and get them adopted", "W.5 U.5", None, 0.55, "req:time.2; commit:community"),
    ("find out who is behind it and use what you learn", "U.5 B.5", None, 0.55),
    ("turn the chaos into a show that pays you", "B.5 R.5", None, 0.55),
    ("rally people to tear the broken thing down", "R.5 G.5", None, 0.55, "req:ties.2"),
    ("bring neighbours together to care for each other", "W.5 G.5", None, 0.5, "req:ties.2; commit:community"),
    ("use an institution's money and rank to fix it your way", "W.5 B.5", None, 0.55, "req:money.3"),
    ("invent an unusual fix and test it on the street", "U.5 R.5", None, 0.6, "req:time.3"),
    ("let what is failing die and reuse what is left", "B.5 G.5", None, 0.5),
    ("lead a righteous charge to fix it now", "W.5 R.5", None, 0.55, "req:health.3"),
    ("study how it grew and help it adapt", "U.5 G.5", None, 0.55, "req:time.2"),
  ]),
  dict(name="a crossroads in how you live", per_year=(0, 0, 0, 0.1, 0.1, 0.1), drivers="stress+.6 era+.4", rite="mature elder", stages="adult mature elder", age=(26, 90), alpha="W.2 U.2 B.2 R.2 G.2", stakes=1.1, options=[
    ("build an honourable order that protects everyone", "W.34 U.33 G.33", None, 0.55),    # Bant
    ("perfect yourself and the system you control", "W.34 U.33 B.33", None, 0.6),         # Esper
    ("take power by any means, without restraint", "U.34 B.33 R.33", None, 0.6),         # Grixis
    ("fight to survive and come out on top", "B.34 R.33 G.33", None, 0.55),              # Jund
    ("throw heart, body and people into life", "R.34 G.33 W.33", None, 0.5, "req:health.3 ties.2"),   # Naya
    ("endure: hold your family's ground for generations", "W.34 B.33 G.33", None, 0.55, "req:ties.2"), # Abzan
    ("train mind and body and find the clever path", "U.34 R.33 W.33", None, 0.6, "req:time.3"),     # Jeskai
    ("patiently exploit what others neglect", "B.34 G.33 U.33", None, 0.55),             # Sultai
    ("strike fast and hard with your crew", "R.34 W.33 B.33", None, 0.55, "req:health.3"),           # Mardu
    ("trust instinct and adapt as things come", "G.34 U.33 R.33", None, 0.5),             # Temur
  ]),
  # Not sampled by stage: the engine opens it when a commitment stops fitting. The first
  # three options' ways of acting are set at run time from the commitment itself.
  dict(name="reconsidering a commitment", stages="", age=(0, 0), alpha="", stakes=1.0, options=[
    ("recommit and invest more", "W1", None, 0.45),
    ("reshape it toward who you want to be", "U1", None, 0.55),
    ("walk away", "R.5 U.3 B.2", None, 0.5),
  ]),
]

# Unchosen impositions: things that happen TO the person. They hit human needs
# directly (needs are shared across colors), and raise stress. sampled with
# probability impose_p per week.
IMPOSITIONS = [
  ("a rule is imposed on you", "autonomy-.6"),
  ("an institution betrays its promise", "safety-.4 meaning-.3"),
  ("you are lied to and misled", "competence-.3 safety-.3"),
  ("someone takes what you earned", "autonomy-.3 competence-.3"),
  ("your community or habitat is damaged", "belonging-.4 safety-.3"),
  ("you are forbidden to see someone you love", "belonging-.6"),
  ("evidence you trusted is overturned", "competence-.4 meaning-.2"),
  ("you are made dependent on others", "autonomy-.5"),
  ("your traditions are mocked or banned", "meaning-.4 belonging-.3"),
  ("lawlessness spreads around you", "safety-.6"),
]

# Life stages. `rite` on a situation lists the stages it can open.
# A person enters the next stage through a rite of passage: an
# impactful event inside the stage's entry window (earliest, latest age). The
# bar for "impactful" falls as the window closes; at the latest age the
# transition happens quietly. Plasticity is a property of the stage, not of age.
STAGES = [
  # name,          entry window, plasticity
  ("child",        (0, 0),   0.6),
  ("juvenile",     (10, 15), 1.0),
  ("young_adult",  (15, 25), 0.9),
  ("adult",        (24, 36), 0.6),
  ("mature",       (40, 60), 0.45),
  ("elder",        (60, 80), 0.35),
]

# Human needs and which colors' ends can meet them (rows sum to 1, columns sum to 1).
NEEDS = ["safety", "belonging", "autonomy", "competence", "meaning"]
NEED_MAP = [
  #  W     U     B     R     G
  [0.35, 0.15, 0.20, 0.00, 0.30],   # safety: order, foresight, self-protection, rootedness
  [0.25, 0.00, 0.00, 0.35, 0.40],   # belonging: duty, love and passion, community
  [0.00, 0.25, 0.45, 0.30, 0.00],   # autonomy: mastery of self, power, freedom
  [0.15, 0.45, 0.25, 0.10, 0.05],   # competence: skill, knowledge, results
  [0.25, 0.15, 0.10, 0.25, 0.25],   # meaning: duty, understanding, passion, place in the whole
]
# v6: autonomy and competence are met by HOW one acts, in any color (self-determination theory, Ryan & Deci 2000):
# autonomy by acting as oneself (self-concordance, Sheldon & Elliot 1999) plus free time and freedom; competence by
# succeeding at what is hard for you (effectance). The engine supplies both. Colors' ends meet the three needs that
# depend on WHAT one serves: safety, belonging and meaning, and every color meets the same total (columns sum to 0.6).
# In v5 Black and Blue met most of autonomy and competence, so the scarcest needs made Black-, Blue- and White-leaners
# the most satisfied and Red-leaners the least, while surveys find values barely predict life satisfaction.
NEED_MAP_V6 = [
  #  W     U     B     R     G
  [0.25, 0.20, 0.20, 0.15, 0.20],   # safety: order, foresight, self-protection and means, standing up for one's own, home and roots
  [0.15, 0.10, 0.15, 0.30, 0.30],   # belonging: duty, kinship of minds, alliances, love and passion, community
  [0.00, 0.00, 0.00, 0.00, 0.00],   # autonomy: acting as oneself (engine), free time and freedom
  [0.00, 0.00, 0.00, 0.00, 0.00],   # competence: succeeding at what is hard for you (engine), in any color
  [0.20, 0.30, 0.25, 0.15, 0.10],   # meaning: duty and faith, understanding, ambition and legacy, passion, place in the whole
]

# v4: resources (0..1). Time is free time left after commitments; freedom is permission to act.
RESOURCES = ["money", "time", "health", "ties", "freedom"]
# v4: commitments: (name, weekly time load, needs it meets while held, scaled by its strength)
COMMITMENTS = [
  ("career",    0.40, "competence.6 meaning.3 safety.1"),
  ("partner",   0.15, "belonging.7 safety.3"),
  ("children",  0.30, "meaning.6 belonging.4"),
  ("community", 0.10, "belonging.5 meaning.5"),
  ("faith",     0.05, "meaning.6 belonging.3 safety.1"),   # a religion, ideology or cause; often inherited in childhood
]
# v6: duties. A held commitment makes the needs of the people it serves felt as one's own (a parent feels the child's
# need for safety; a job asks for competence and provision). This is why roles move values (social investment).
DUTIES = {
  "career":    "competence.5 safety.5",
  "partner":   "belonging.6 safety.4",
  "children":  "safety.6 belonging.4",
  "community": "belonging.5 safety.5",
  "faith":     "meaning.6 belonging.4",
}


# ---------- the outside world (v4, Emren 2026-10-04): perturbations from outside the person.
# Every perturbation brings a MESSAGE, the color mix it asks of people, and the person decides how to take it:
# exposure depends on their situation (ties, commitments, means), acceptance on their history (whether the message
# fits their mindset, how content they are, how open they are right now, how strongly they hold what it would take,
# and for social sources whether they lean to the group or to the individual). Nothing here says how a person reacts.
# (name, source, message, strength, rate per year, effects)
#   message: a color mix; "random" = 1 to 3 colors drawn evenly (enemies as likely as allies); "niche" = the person's
#   own surroundings; "faith" = their faith if they hold one, otherwise random; "era" = the times; "none" = it works
#   through needs and resources only (the person decides which colors could meet them)
#   effects: "need:safety-.4" needs, "res:health-.2" resources, "move" new surroundings, "door" opens the message's ways
SOURCES = ["community", "institution", "daily life", "environment", "cosmology"]
EVENTS = [
  # community and peers
  ("new friends with a different way of life", "community", "random", 0.6, 0.12, "door"),
  ("your circle closes ranks around its norms", "community", "niche", 0.5, 0.10, ""),
  ("moving somewhere new", "community", "random", 0.8, 0.04, "move"),
  ("a mentor takes you under their wing", "community", "random", 0.8, 0.04, "door"),
  ("a friend's life choice makes you wonder", "community", "random", 0.4, 0.20, ""),
  # policies and institutions
  ("a new rule changes how things are done", "institution", "random", 0.5, 0.10, "need:autonomy-.15 door"),
  ("an institution rewards a kind of person", "institution", "random", 0.5, 0.08, "door"),
  ("you are judged by an official process", "institution", "W.5 U.5", 0.4, 0.04, "need:safety-.1"),
  # daily life
  ("a book, film or idea grips you", "daily life", "random", 0.4, 0.30, ""),
  ("small daily frictions add up", "daily life", "none", 0.3, 0.50, "need:autonomy-.1 need:belonging-.05"),
  ("an illness", "daily life", "none", 0.6, 0.06, "res:health-.25 need:safety-.2"),
  ("an unexpected windfall or loss of money", "daily life", "none", 0.5, 0.05, "res:money-.2 need:safety-.15"),
  # environment and nature
  ("a natural disaster hits where you live", "environment", "none", 1.0, 0.02, "need:safety-.5 need:belonging-.2 res:money-.15 res:health-.1"),
  ("a hard season of scarcity", "environment", "none", 0.6, 0.04, "need:safety-.3 res:money-.1"),
  ("a season of plenty", "environment", "none", 0.4, 0.04, "need:safety+.2 res:money+.1"),
  # cosmology and the supernatural
  ("an experience you cannot explain", "cosmology", "faith", 0.8, 0.03, "need:meaning+.2"),
  ("a sign or prophecy that seems to come true", "cosmology", "random", 0.6, 0.02, "need:meaning+.1"),
  ("a brush with death", "cosmology", "random", 1.0, 0.015, "need:safety-.3 need:meaning-.2 res:health-.2"),
]
# Eras: the times everyone in a society lives through together (policy, institutions, cosmology). An era favours a
# color combination: its institutions open those ways, reward them, and preach them. Eras arrive at random
# (era_rate per year) and are drawn evenly from single colors, pairs and three-color groups.
ERA_KINDS = ["policy", "institutions", "cosmology"]

# v7: what can spark a dream (Emren 2026-10-05, 1A: people and stories a person admires, read through their own colors;
# "a book, cinema or a parade also can trigger that dream, depending on the character"). Seed content for modern Earth;
# the Library owns the real lists per world.
#   name, source, weight by stage (child juvenile young_adult adult mature elder), what it shows ("" = drawn per source)
# Sources: family (someone in the family, close to the family's ways), circle (someone around them now), story (a
# book, film or show: any ways at all, partly the culture's), spectacle (a public event: mostly the culture's and the
# times' ways), stranger (anyone). Whether a spark takes depends on the person: how well what it shows fits who they
# are and want to be, and how open they are just now.
DREAM_TRIGGERS = [
  ("a parent or relative at their work",  "family",    (1.0, 0.6, 0.3, 0.1, 0.1, 0.1), ""),
  ("an older sibling or cousin",          "family",    (0.7, 0.6, 0.3, 0.1, 0.0, 0.0), ""),
  ("a teacher or coach",                  "circle",    (0.5, 0.8, 0.5, 0.2, 0.1, 0.1), ""),
  ("a friend's family",                   "circle",    (0.4, 0.5, 0.3, 0.2, 0.2, 0.1), ""),
  ("someone they meet",                   "circle",    (0.2, 0.4, 0.6, 0.6, 0.5, 0.4), ""),
  ("a book",                              "story",     (0.5, 0.7, 0.6, 0.5, 0.5, 0.5), ""),
  ("a film or a show",                    "story",     (0.7, 0.8, 0.6, 0.5, 0.4, 0.4), ""),
  ("a parade or a festival",              "spectacle", (0.6, 0.4, 0.3, 0.2, 0.2, 0.2), ""),
  ("a match or a contest",                "spectacle", (0.5, 0.6, 0.4, 0.2, 0.1, 0.1), ""),
  ("a ceremony",                          "spectacle", (0.3, 0.3, 0.3, 0.3, 0.3, 0.3), ""),
  ("a stranger passing through",          "stranger",  (0.2, 0.2, 0.3, 0.3, 0.3, 0.3), ""),
]
