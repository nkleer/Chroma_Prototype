# Dreams for the packs' dreamless aims (Packs thread, drafted 2026-10-21, poured 10-23 for v25), for the Library's
# dreams.py.
#
# SWITCHED OFF: nothing reads this file. The packs' aim fields (<pack>/fields.py) name these dreams; they reach a life
# once the Library adds them to dreams.py (below) and the packs' fields are read (aims_v2 on).
#
# Why: 13 of the four packs' 20 aims name no dream (aims.py dreams=[]): art 3, politics 2, science 4, stage 4. In the
# 400 lives left alone on head 10, 68% of the aims a life took up came from its dreams, and 14 of the packs' aims were
# never taken (chroma-ideas/life-drivers-2026-10-20/aims-coverage.md). A dream the catalogue holds lets a life start the
# aim; the refit's ways in only help it climb. The five callings' aims all have dreams already.
#
# What: one dream per dreamless aim in each world (13 x 3), from the aim's own words and its tribal and magic forms, and
# two balancing dreams per world (one U-G for "to master a craft", one B-G for "to save the old theatre") so that the 15
# added in each world give every colour the same weight: 6 dreams x .5 = 3.0 per colour per world (W U B R G). Same
# fields as dreams.py's DREAMS (name, means, domain, stages, worlds, passion, plan, life); DREAM_KIND gives each one's
# kind (play from 4, status from 9, own from 14; dreams.py KIND_FROM). TRIGGER_MORE suggests the sparks that should show
# them. Every name is new to dreams.py (checked by reading it on main 519ce30) and none names a real place, year or
# brand.
#
# At the switch-on: the Library adds DREAMS_PACKS to dreams.py where it judges best (with dream_grow, in DREAMS_MORE
# beside the other later dreams), DREAM_KIND_PACKS to DREAM_KIND and TRIGGER_MORE to TRIGGER_DREAMS. Each pack's
# fields.py already names them (from AIM_DREAMS below); aims.py (v1) keeps dreams=[]. The Library's colour-even rule
# per world is kept by the 15 together; adding only some of them breaks it.

DREAMS_PACKS = [
  # ================= modern Earth =================
  # art
  dict(name="a writer of books", means="R.5 W.5", domain="career", stages="juvenile young_adult adult", worlds="earth",
       passion="writing", plan="write every morning and finish a first book", life="shelves of books with one's name on them"),
  dict(name="an artist", means="R.5 G.5", domain="career", stages="child juvenile young_adult", worlds="earth",
       passion="painting and making pictures", plan="go to art school and paint every day",
       life="a painting people stop in front of"),
  dict(name="an illustrator", means="U.5 B.5", domain="career", stages="child juvenile young_adult", worlds="earth",
       passion="drawing", plan="build a portfolio and find the first clients", life="a lifetime of drawing for a living"),
  # politics
  dict(name="the country's leader", means="W.5 B.5", domain="career", stages="juvenile young_adult adult", worlds="earth",
       passion="politics", plan="join a party, win a seat and rise", life="to lead the country through hard years"),
  dict(name="to change how the country thinks", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="earth", passion="ideas and argument", plan="write, speak and argue until the idea takes hold",
       life="an idea that changed the argument"),
  # science
  dict(name="to lead a great laboratory", means="B.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="earth", passion="big science", plan="win the grants, hire the best and build the team",
       life="a laboratory the best want to join"),
  dict(name="to explain science to everyone", means="R.5 W.5", domain="career", stages="juvenile young_adult adult",
       worlds="earth", passion="telling the story of science", plan="learn the science, then learn to tell it",
       life="a town that understands how the world works"),
  dict(name="a scientist whose work stands", means="W.5 U.5", domain="career", stages="juvenile young_adult",
       worlds="earth", passion="getting the facts right", plan="train in the lab and check every result twice",
       life="work that every later test confirms"),
  dict(name="to keep a record of the world that lasts", means="G.5 B.5", domain="career",
       stages="juvenile young_adult adult", worlds="earth", passion="watching and counting the world",
       plan="take one place's measures every season, without a gap", life="a record of forty years others build on"),
  # stage
  dict(name="a playwright", means="U.5 R.5", domain="career", stages="juvenile young_adult adult", worlds="earth",
       passion="writing plays", plan="write a play a year and get one staged", life="plays still put on long after"),
  dict(name="to run a theatre", means="W.5 U.5", domain="career", stages="juvenile young_adult adult", worlds="earth",
       passion="the theatre", plan="learn every job backstage, then run a house",
       life="a theatre that runs like clockwork and fills every night"),
  dict(name="to save the town's old theatre", means="B.5 G.5", domain="career", stages="juvenile young_adult adult mature",
       worlds="earth", passion="old theatres", plan="raise the money and bring it back to life",
       life="the old theatre full again"),
  dict(name="to give the town a stage of its own", means="G.5 W.5", domain="community",
       stages="juvenile young_adult adult mature elder", worlds="earth", passion="the town's own shows",
       plan="start a company of neighbours and put on a show a year", life="a town that puts on its own plays"),
  # the two that keep the colours even
  dict(name="a master of a craft", means="G.5 U.5", domain="career", stages="child juvenile young_adult", worlds="earth",
       passion="making things by hand", plan="learn from a master and keep at it for years",
       life="work a master's hand would be proud of"),
  dict(name="a theatre of one's own", means="B.5 G.5", domain="career", stages="juvenile young_adult adult mature",
       worlds="earth", passion="theatres", plan="save, take a share, and buy the old house when it comes up",
       life="a theatre of one's own, kept open for the town"),

  # ================= a tribal world =================
  dict(name="a maker of verses", means="R.5 W.5", domain="career", stages="juvenile young_adult adult", worlds="tribal",
       passion="the old verses", plan="learn every old verse by heart and make new ones", life="verses the bands still say"),
  dict(name="a painter of the cave walls", means="R.5 G.5", domain="career", stages="child juvenile young_adult",
       worlds="tribal", passion="painting the walls", plan="grind the colours with the old painter, season after season",
       life="a cave wall every band comes to see"),
  dict(name="a maker of patterns", means="U.5 B.5", domain="career", stages="child juvenile young_adult", worlds="tribal",
       passion="patterns", plan="learn the marks of every band and make new ones", life="patterns traded far beyond the hills"),
  dict(name="the speaker for all the bands", means="W.5 B.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="the gathering's council", plan="speak well at the fires and win the elders' trust",
       life="to speak for every band at the great gathering"),
  dict(name="the voice the gathering heeds", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="changing minds", plan="listen at every fire and learn what moves people",
       life="a new way the bands took up because of one voice"),
  dict(name="a leader of the finders", means="B.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="new ways", plan="gather the band's best finders around you", life="a band known for its new ways"),
  dict(name="a teller of the sky", means="R.5 W.5", domain="career", stages="juvenile young_adult adult", worlds="tribal",
       passion="the sky and the seasons", plan="watch the sky every night and tell it at the fires",
       life="bands that know the seasons by your telling"),
  dict(name="a keeper of true knowledge", means="W.5 U.5", domain="career", stages="juvenile young_adult", worlds="tribal",
       passion="what is true", plan="learn from the elders and test every saying", life="knowledge the band can trust"),
  dict(name="a counter of the seasons", means="G.5 B.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="counting the seasons", plan="cut a mark for every moon and never miss one",
       life="the band's counts of a whole life kept"),
  dict(name="a maker of dances and tellings", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="dances and tellings", plan="make a new telling for every gathering",
       life="dances the bands still dance"),
  dict(name="the one who orders the great dances", means="W.5 U.5", domain="career", stages="juvenile young_adult adult",
       worlds="tribal", passion="the great dances", plan="learn every part of the great dances, then lead them",
       life="a gathering whose dances go as they should"),
  dict(name="to keep the gathering's dances going", means="B.5 G.5", domain="career",
       stages="juvenile young_adult adult mature", worlds="tribal", passion="the old dances",
       plan="gather the gifts and the dancers every winter", life="the dances kept alive through hard winters"),
  dict(name="a keeper of the band's tellings", means="G.5 W.5", domain="community",
       stages="juvenile young_adult adult mature elder", worlds="tribal", passion="the band's own tellings",
       plan="tell the old stories to the young ones every winter", life="a band that keeps its own tellings"),
  dict(name="a master basket-weaver", means="G.5 U.5", domain="career", stages="child juvenile young_adult",
       worlds="tribal", passion="weaving", plan="weave beside the old weaver until the hands know it",
       life="baskets traded at every gathering"),
  dict(name="the keeper of the dancing ground", means="B.5 G.5", domain="career", stages="juvenile young_adult adult mature",
       worlds="tribal", passion="the dancing ground", plan="claim the ground and keep it for the gatherings",
       life="a dancing ground the bands owe to you"),

  # ================= a magic world =================
  dict(name="a chronicler of the realm", means="R.5 W.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="chronicles", plan="copy the old chronicles and write the new ones",
       life="the realm's story told in your hand"),
  dict(name="a court painter", means="R.5 G.5", domain="career", stages="child juvenile young_adult", worlds="magic",
       passion="painting", plan="apprentice in a painter's workshop", life="a portrait that hangs in the great hall"),
  dict(name="an illuminator of books", means="U.5 B.5", domain="career", stages="child juvenile young_adult",
       worlds="magic", passion="illuminated pages", plan="learn the inks and the gold leaf at an Order's scriptorium",
       life="pages the Orders keep for centuries"),
  dict(name="to sit at the head of the council", means="W.5 B.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="the realm's council", plan="serve a councillor and earn a seat",
       life="to lead the realm's council in hard years"),
  dict(name="the voice that turns the council", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="argument", plan="study the old debates and speak at every hearing",
       life="a council that changed its mind because of you"),
  dict(name="to found a school at the academy", means="B.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="learning that grows", plan="win a patron and gather the best students",
       life="a school of one's own at the academy"),
  dict(name="a lecturer to the commons", means="R.5 W.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="explaining the world", plan="learn at the academy and lecture in the squares",
       life="commons who understand the stars and the seasons"),
  dict(name="a master of the archives", means="W.5 U.5", domain="career", stages="juvenile young_adult", worlds="magic",
       passion="true records", plan="serve the archives and check every copy", life="archives without a false page"),
  dict(name="a keeper of the observatory's tables", means="G.5 B.5", domain="career",
       stages="juvenile young_adult adult", worlds="magic", passion="the long tables",
       plan="take the observatory's readings every night", life="tables kept true for a lifetime"),
  dict(name="a writer for the royal playhouse", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="magic", passion="plays", plan="write for the fairs, then for the playhouse", life="plays the court still asks for"),
  dict(name="master of the revels", means="W.5 U.5", domain="career", stages="juvenile young_adult adult", worlds="magic",
       passion="the revels", plan="serve the revels office and learn every festival", life="festivals that go as they should"),
  dict(name="to own the playhouse on the square", means="B.5 G.5", domain="career",
       stages="juvenile young_adult adult mature", worlds="magic", passion="the playhouse",
       plan="save, buy a share and keep the house open", life="the playhouse kept for the town"),
  dict(name="to lead the town's mummers", means="G.5 W.5", domain="community",
       stages="juvenile young_adult adult mature elder", worlds="magic", passion="the mummers' plays",
       plan="join the mummers and keep the old plays", life="a town that keeps its own plays"),
  dict(name="a master of the craft guild", means="G.5 U.5", domain="career", stages="child juvenile young_adult",
       worlds="magic", passion="the guild's craft", plan="apprentice, journey and make a masterpiece",
       life="a master's mark on work the realm uses"),
  dict(name="a patron of the players", means="B.5 G.5", domain="career", stages="juvenile young_adult adult mature",
       worlds="magic", passion="the players", plan="grow a fortune and keep a company of players",
       life="players who owe their stage to you"),
]

DREAM_KIND_PACKS = {
  # Earth
  "a writer of books": "own", "an artist": "play", "an illustrator": "play", "the country's leader": "status",
  "to change how the country thinks": "own", "to lead a great laboratory": "status",
  "to explain science to everyone": "own", "a scientist whose work stands": "own",
  "to keep a record of the world that lasts": "own", "a playwright": "own", "to run a theatre": "status",
  "to save the town's old theatre": "own", "to give the town a stage of its own": "own", "a master of a craft": "play",
  "a theatre of one's own": "status",
  # tribal
  "a maker of verses": "own", "a painter of the cave walls": "play", "a maker of patterns": "play",
  "the speaker for all the bands": "status", "the voice the gathering heeds": "own", "a leader of the finders": "status",
  "a teller of the sky": "own", "a keeper of true knowledge": "own", "a counter of the seasons": "own",
  "a maker of dances and tellings": "own", "the one who orders the great dances": "status",
  "to keep the gathering's dances going": "own", "a keeper of the band's tellings": "own",
  "a master basket-weaver": "play", "the keeper of the dancing ground": "status",
  # magic
  "a chronicler of the realm": "own", "a court painter": "play", "an illuminator of books": "play",
  "to sit at the head of the council": "status", "the voice that turns the council": "own",
  "to found a school at the academy": "status", "a lecturer to the commons": "own", "a master of the archives": "own",
  "a keeper of the observatory's tables": "own", "a writer for the royal playhouse": "own",
  "master of the revels": "status", "to own the playhouse on the square": "own", "to lead the town's mummers": "own",
  "a master of the craft guild": "play", "a patron of the players": "status",
}

# Suggested sparks (TRIGGER_DREAMS[world][spark] gains these names); only sparks dreams.py already has.
TRIGGER_MORE = {
  "earth": {
    "a concert": ("an artist", "a playwright"),
    "a teacher or coach": ("a writer of books", "a scientist whose work stands"),
    "a neighbour's workshop in the shed": ("a master of a craft",),
    "a parade or a festival": ("to give the town a stage of its own",),
    "a street protest": ("to change how the country thinks",),
    "the news": ("the country's leader", "to explain science to everyone"),
    "a nature documentary": ("to keep a record of the world that lasts",),
  },
  "tribal": {
    "a storyteller at the fire": ("a maker of verses", "a keeper of the band's tellings", "a maker of dances and tellings"),
    "an old toolmaker at work": ("a master basket-weaver", "a maker of patterns"),
    "the elders settling a quarrel": ("the speaker for all the bands", "the voice the gathering heeds"),
    "the great gathering at the waterhole": ("the one who orders the great dances", "the keeper of the dancing ground"),
    "the elder who teaches the children": ("a teller of the sky", "a keeper of true knowledge", "a counter of the seasons"),
  },
  "magic": {
    "a book from the old library": ("a chronicler of the realm", "a master of the archives", "an illuminator of books"),
    "a bard's ballad at the inn": ("a writer for the royal playhouse", "to lead the town's mummers"),
    "a puppet show at the fair": ("master of the revels", "a patron of the players"),
    "the trials at the academy": ("to found a school at the academy", "a lecturer to the commons",
                                  "a keeper of the observatory's tables"),
    "a guild procession": ("a master of the craft guild", "to own the playhouse on the square"),
  },
}

# Each pack aim's dreams=[] in aims.py, filled at the switch-on (Packs): the aim's dream in each world.
AIM_DREAMS = {
  "to write books": ["a writer of books", "a maker of verses", "a chronicler of the realm"],
  "to make art people stop for": ["an artist", "a painter of the cave walls", "a court painter"],
  "to draw for a living": ["an illustrator", "a maker of patterns", "an illuminator of books"],
  "to master a craft": ["a master of a craft", "the best toolmaker in the clans", "a master basket-weaver",
                        "a master of the craft guild"],
  "to lead the country": ["the country's leader", "the speaker for all the bands", "to sit at the head of the council"],
  "to change the argument": ["to change how the country thinks", "the voice the gathering heeds",
                             "the voice that turns the council"],
  "to build a great lab": ["to lead a great laboratory", "a leader of the finders", "to found a school at the academy"],
  "to make the world understand": ["to explain science to everyone", "a teller of the sky", "a lecturer to the commons"],
  "to get it right": ["a scientist whose work stands", "a keeper of true knowledge", "a master of the archives"],
  "to keep the long record": ["to keep a record of the world that lasts", "a counter of the seasons",
                              "a keeper of the observatory's tables"],
  "to write what is played": ["a playwright", "a maker of dances and tellings", "a writer for the royal playhouse"],
  "to run a theatre": ["to run a theatre", "the one who orders the great dances", "master of the revels"],
  "to save the old theatre": ["to save the town's old theatre", "a theatre of one's own",
                              "to keep the gathering's dances going", "the keeper of the dancing ground",
                              "to own the playhouse on the square", "a patron of the players"],
  "to give the town its stage": ["to give the town a stage of its own", "a keeper of the band's tellings",
                                 "to lead the town's mummers"],
}
