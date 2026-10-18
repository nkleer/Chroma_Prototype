# ---------- bond: a person (or an animal) on the person's side; when the bond goes, what it taught fades by skill_half
PERKS += [
  dict(name="mentor", kind="bond", ways="U W", odds=.05, skill_half=20, retires=None,
       ages=(10, 90), share=.5,   # about 2 young Americans in 3 had a mentor of some kind (MENTOR, 2014); estimate for
                                  # one who counts
       say="has a mentor",
       gained="'a teacher or coach who believes in you'; an older hand at work who takes them under a wing",
       lost="the mentor dies, retires or moves on; the lessons stay",
       needs="'learned a skill' or 'helped someone in need'"),
  dict(name="friend in power", kind="bond", ways="B U", odds=.05, skill_half=5, retires=None,
       ages=(16, 110), share=.08,   # estimate
       say="has a friend in power",
       gained="a school friend who rose high, or 'made a friend' of the boss's boss",
       lost="the friend falls, or turns away",
       needs="'made a friend'"),
  dict(name="patron", kind="bond", ways="B R", odds=.06, skill_half=5, retires=None,
       ages=(14, 100), share=.02,   # estimate
       say="has a patron",
       gained="'an unexpected chance: a grant, a role, a stage', 'praise from a stranger' with money behind it",
       lost="a quarrel, the patron's death",
       needs="a gift worth backing; 'took a wild risk'"),
  dict(name="family who will always take you in", kind="bond", ways="G", odds=.04, skill_half=20, retires=None,
       ages=(0, 110), share=.7,   # estimate
       say="always has a home to go back to",
       gained="born to it; or 'making peace with family you had cut off'",
       cause="born into a family that holds together",
       lost="a deep break, or the old ones dying one by one",
       needs="a family"),
  dict(name="friend for life", kind="bond", ways="R G", odds=.04, skill_half=15, retires=None,
       ages=(6, 110), share=.6,   # estimate
       say="has a friend for life",
       gained="'a friend for life', who may have been 'a new kid joins your class' once",
       lost="'betrayed by a friend or a business partner', 'your closest friend dies'",
       needs="'made a friend'"),
  dict(name="old school network", kind="bond", ways="U B", odds=.04, skill_half=15, retires=None,
       ages=(18, 110), share=.15,   # estimate
       say="knows people from school",
       gained="a well-connected school or university, and a reunion every five years",
       lost="letting it go cold",
       needs="[graduate] or a school with a name"),
  dict(name="sponsor in recovery", kind="bond", ways="W G", odds=.05, skill_half=10, retires=None,
       ages=(16, 110), share=.03,   # estimate
       say="has a sponsor",
       gained="the first weeks at meetings after 'an addiction takes hold'",
       lost="the sponsor moves or relapses, and a new one is found",
       needs="[in recovery]"),
  dict(name="neighbour who has your back", kind="bond", ways="G W", odds=.03, skill_half=5, retires=None,
       ages=(16, 110), share=.4,   # estimate
       say="has a good neighbour",
       gained="'new people move in next door' and become friends; 'break-ins on the street' bring the street together",
       lost="a move, or 'a neighbour's dog keeps you awake' turned into a feud",
       needs="'made a friend' or 'helped someone in need'"),
  dict(name="contact in the trade", kind="bond", ways="B G", odds=.04, skill_half=5, retires=None,
       ages=(18, 90), share=.15,   # estimate
       say="has a contact in the trade",
       gained="years of work done well for the same people; 'someone you helped returns the favour'",
       lost="a falling-out, the contact retiring",
       needs="a career title"),
  dict(name="family abroad", kind="bond", ways="R U", odds=.03, skill_half=15, retires=None,
       ages=(0, 110), share=.2,   # estimate
       say="has family abroad",
       gained="a family spread over two countries; 'a long-lost relative finds you'",
       cause="with relatives spread over two countries",
       lost="the cousins die or drift",
       needs="relatives who once 'moved away'"),
  dict(name="old comrades", kind="bond", ways="R W", odds=.04, skill_half=15, retires=None,
       ages=(20, 110), share=.1,   # estimate: army mates, an old team, a crew that went through something together
       say="has old comrades",
       gained="years as a [soldier] or [on the team] in the same hard place",
       lost="deaths, quarrels",
       needs="[veteran], or years on a team"),
  dict(name="godparent who looks out", kind="bond", ways="W B", odds=.03, skill_half=10, retires=None,
       ages=(0, 60), share=.15,   # estimate
       say="has a godparent who looks out for them",
       gained="chosen by the parents at a naming day",
       cause="chosen at the naming",
       lost="a falling-out, the godparent's death",
       needs="parents who chose one"),
  dict(name="dog of one's own", kind="bond", ways="G R", odds=.02, skill_half=3, retires=None,
       ages=(4, 110), share=.4,   # estimate
       say="has a dog",
       gained="'a stray dog follows you home', or a puppy as 'a pet of your own'",
       cause="after a dog comes into the home",
       lost="'your pet dies', a move to a flat that bans dogs",
       needs="a home that allows one, and money for food"),
  dict(name="in-laws who took you in", kind="bond", ways="R G", odds=.03, skill_half=10, retires=None,
       ages=(18, 110), share=.35,   # estimate
       say="has in-laws who treat them as their own",
       gained="'a holiday dinner with both families' that goes well; years of Sunday lunches",
       lost="a divorce, a row at a funeral",
       needs="[wife or husband] or [living together]"),
]

