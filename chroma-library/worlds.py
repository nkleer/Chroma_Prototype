# Chroma Library: the words and the own ways of the tribal and magic worlds (v22.5, F12 "The world and the start hold",
# Emren's v22.5 realism list, 2026-10-11). Plain data: nothing is imported.
#
# Tribal and magic lives play on the engine's seed library (chroma-engine/v22-speedpass/library.py), whose situation names
# and option labels are written for modern Earth. The realism check of 10-11 found "lacks money" 35 times in one
# river-clan life, "money lost" after a failed courtship, "Sasha loses their work", committees and institutions in the
# clan, patents in the towers, and the clan's own rites closed as "not on offer around them" (realism-check.md 1.9).
#
# Read only with the game's switch world_words on (the words) and the engine's switch own_open on (OWN); with them off,
# nothing here is read.
#
# WORDS[world]: the game's own words in that world:
#   res       the five means as the game names them (money, time, health, ties, freedom)
#   career    a career as a commitment, as the game says it ("could start ...")
#   job       the work one holds ("loses their ...")
#   backfire  the line when a pick forced out of reach backfires
# TITLES[world][situation]: the moment's title in that world (the game keeps the seed name as the key for its scenes).
# LABELS[world][option label]: the option as it reads in that world: second person, a plain imperative, like the seed
#   label; its ways (colours) are the seed option's. The game tells the act in the third person from it.
# OWN[world]: the seed options that are that culture's own acts (its rites, traditions, sharing and crafts in the clan;
#   study, procedure, rites and guild ways in the towers). With the engine's own_open on they are always on offer
#   around the person: the world never closes them (lacking the means still can). Earth's own acts come from the
#   Library batch's norms and rites (a later step), so earth has none here.

WORDS = {
  "tribal": dict(
    res=dict(money="goods", time="time", health="health", ties="ties", freedom="freedom"),
    career="their life's work", job="place in the work",
    backfire="Forcing what was out of reach backfired: more strain, and some of their goods lost.",
  ),
  "magic": dict(
    res=dict(money="coin", time="time", health="health", ties="ties", freedom="freedom"),
    career="a post", job="post",
    backfire="Forcing what was out of reach backfired: more strain, and some coin lost.",
  ),
}

TITLES = {
  "tribal": {
    "playground dispute": "a fight among the children",
    "hard school task": "a hard lesson from the elders",
    "conflict at work": "a quarrel over the work",
    "money: windfall or squeeze": "a good season or a lean one",
    "community problem": "trouble in the camp",
    "chance to innovate": "a new way to try",
    "something is wrong where you live": "something is wrong in the camp",
  },
  "magic": {
    "playground dispute": "a quarrel among the children",
    "hard school task": "a hard lesson",
    "conflict at work": "a quarrel at the guild",
    "money: windfall or squeeze": "coin: windfall or squeeze",
  },
}

LABELS = {
  "tribal": {
    # childhood
    "tell the teacher": "tell the elder who watches the children",
    "copy a classmate": "copy what another child does",
    "study together with friends": "learn it together with friends",
    "follow the teacher's method exactly": "do it exactly as the elder showed you",
    "refuse, it breaks the rules": "refuse, it breaks the clan's ways",
    # a path
    "serve the community": "serve the clan",
    "pursue a rigorous field": "learn a hard craft from a master of it",
    "chase money and status": "chase goods and standing",
    "join an institution's ranks": "take a place in the chief's circle",
    # injustice, work
    "report it to authority": "take it to the elders",
    "gather evidence first": "find out the whole of it first",
    "follow procedure": "do it the way it has always been done",
    "manoeuvre politically": "win people over one by one",
    # goods
    "save and give a share": "store it and share it out",
    "invest in learning": "trade it for a master's teaching",
    "leverage it for advantage": "use it to put others in your debt",
    "spend it on experiences": "spend it on feasting and journeys",
    # the camp
    "organise a committee": "call the families together at the fire",
    "profit from the gap": "trade on what is missing",
    "protest loudly": "shout it out at the gathering",
    "revive mutual aid": "bring back the old sharing",
    # new ways
    "standardise what works": "make everyone do it the way that works",
    "patent and monetise it": "keep the secret and trade on it",
    "coordinate relief": "lead the families' help",
    # legacy
    "endow an institution": "give the clan a great gift to be remembered by",
    "secure wealth and name": "secure goods and a name",
    # meaning
    "join a church or order": "take your place in the clan's rites",
    "build a philosophy you can defend": "work out an understanding of things you can defend",
    "follow a creed that promises power": "follow a spirit that promises power",
    "return to an ancestral or nature faith": "return to the old spirits of your ancestors",
    "read, plan or tinker with something": "plan or tinker with something",
    # groups and the camp
    "agree on rules and a fair procedure": "agree on rules and a fair way to decide",
    "write clear rules and get them adopted": "set clear rules and get the elders to agree to them",
    "turn the chaos into a show that pays you": "turn the chaos into a show that brings you goods",
    "use an institution's money and rank to fix it your way": "use the elders' stores and standing to fix it your way",
    "invent an unusual fix and test it on the street": "try an unusual fix and test it in the camp",
    "perfect yourself and the system you control": "perfect yourself and the ways you keep",
    "strike fast and hard with your crew": "strike fast and hard with your band",
    "recommit and invest more": "recommit and give it more of yourself",
    "invest in home and kin": "put your strength into home and kin",
    "use it to gain status": "use it to gain standing",
  },
  "magic": {
    "tell the teacher": "tell the tutor",
    "copy a classmate": "copy a fellow pupil",
    "follow the teacher's method exactly": "follow the tutor's method exactly",
    "serve the community": "serve the town",
    "pursue a rigorous field": "pursue a rigorous art",
    "chase money and status": "chase coin and status",
    "join an institution's ranks": "join the ranks of a guild or the Order",
    "report it to authority": "report it to the wardens",
    "follow procedure": "follow the guild's rules",
    "manoeuvre politically": "work the guild's politics",
    "invest in learning": "spend it on learning",
    "spend it on experiences": "spend it on revels and travel",
    "organise a committee": "call a council of the neighbours",
    "standardise what works": "set down the method that works",
    "patent and monetise it": "register it with the guild and sell it",
    "endow an institution": "endow a hall or a chantry",
    "join a church or order": "join a temple or an Order",
    "use an institution's money and rank to fix it your way": "use a guild's coin and rank to fix it your way",
    "invent an unusual fix and test it on the street": "invent an unusual fix and test it in the street",
  },
}

OWN = {
  "tribal": [
    # sharing, kin and the band
    "share and play together", "accept it as how our family is", "go along to belong", "care for the person harmed",
    "build patient alliances", "endure for the family", "save and give a share", "invest in home and kin",
    "revive mutual aid", "coordinate relief", "hunker down and endure", "make sure everyone is included",
    "bring neighbours together to care for each other", "spend it with family, friends or outdoors",
    "keep to your duties and routines",
    # the craft and the old ways
    "continue the family craft", "serve the community", "refuse, it is not our way", "raise them in our traditions",
    "keep the proven old way", "pass on knowledge", "tend family and land",
    "endure: hold your family's ground for generations",
    # rites: death, marriage, children, the spirits
    "hold the proper rites", "accept the cycle of life", "court them properly and marry",
    "grow a slow bond within your circle", "have children as expected of you", "raise a big family",
    "join a church or order", "return to an ancestral or nature faith",
  ],
  "magic": [
    # study and the arts
    "practise methodically", "follow the teacher's method exactly", "pursue a rigorous field", "invest in learning",
    "pass on knowledge", "read, plan or tinker with something", "study what works and adapt it",
    "train mind and body and find the clever path", "gather information quietly",
    # guilds, procedure and the Order
    "join an institution's ranks", "continue the family craft", "follow procedure", "strike a binding deal",
    "standardise what works", "agree on rules and a fair procedure", "write clear rules and get them adopted",
    "keep to your duties and routines",
    # rites and the temples
    "hold the proper rites", "join a church or order",
  ],
}
