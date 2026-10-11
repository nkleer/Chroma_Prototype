# Chroma Library: age gates for the Earth batch (v22.5, F4), for engine v22.5 (the v22.5 realism thread, 2026-10-11).
# Asked for by Emren's v22.5 realism list, F4 "Age gates" (2026-10-11): moments open to children with acts no child of
# that age could do (chroma-ideas/realism/child-moments-age-fit.md: 79 of the 193 moments a child can meet), adult
# moments whose own words do not fit every age in their window (a fiftieth birthday at 42, a pension statement at 24,
# fifty years of marriage at 45), and the child versions that touch their teen or adult twins at 12.
# The engine lays it over the moments by name when its load gate batch.AGE_FIT is on (batch._age_fit), before any rule
# reads them; with the gate off the batch loads as before. Plain data: nothing is imported.
#
# AGE_FIT[moment name]: a dict of any of
#   age         a new age window (lo, hi) in years: a later start, or a child version ending at 11.99 so that it is shut
#               in the week its twin opens at 12 (the engine's gate is inclusive: age = weeks / 52)
#   stages      a new stage list, only where the new window needs one (none here needs it)
#   options     {option number from 1: a new label} or {n: dict(label=..., act=...)} when the option carries the
#               narrator's act line; labels second person, lower case start, the option's colour and intent kept
#   scenes      {scene key ("" or a colour letter): new text}, this world's scenes only; the {slots} kept
#   outcomes    (works lines, fails lines), both lists whole
#   setting     the moment's one-line Earth premise (worlds["earth"])
#   variant_of  the twin this child version is: the same event for once, kills, gates, conditions and the event pause
#   why         one plain line: what was unrealistic (read by no rule)
# Child norms written to (the review's): under 5 no reading or writing, no school beyond nursery, no money of their
# own, nothing alone outside the home; 5 to 7 early reading and primary school; 8 to 11 more independence and pocket
# money; 12 to 14 no paid work, no legal acts, no running things, no savings to speak of. A reworded option is written
# for the youngest age of its window and still reads naturally for the oldest.

AGE_FIT = {
    # ---- 1. the 79 child moments of the review (its order; [n] is the moment's place in its export) ----------------
    # [185] reworded: the notebook is {elder}'s forty-year record that the person keeps up, as the scene already says
    "forty years of rain in one notebook": dict(
        options={8: "ask the weather service to pay for an automatic gauge, since it uses the notebook's figures"},
        why="option 8 made the forty-year record the person's own figures, which no twelve-year-old has"),
    # [186]
    "the developers want your survey": dict(
        age=(18, 100),
        why="a planning dispute over years of one's own survey records, a fee and a formal objection: adult acts"),
    # [148]
    "the flood in the community centre": dict(
        age=(18, 95),
        why="hosting one's own group, taking a donor's money, sitting on the rebuilding committee: adult acts"),
    # [179] (a child version of the club's final would be a new moment, not an age fit)
    "the club reaches the final": dict(
        age=(16, 90),
        why="running the tickets and the minibus, finding a kit sponsor, baking for the clubhouse tea: adult volunteers' acts"),
    # [129]
    "a public scandal": dict(
        age=(16, 95),
        why="putting out a careful account and calling in favours are not a twelve-year-old's acts"),
    # [128]
    "a cause you fought for wins": dict(
        age=(15, 95),
        why="two years of campaigning, a fund, a committee and the same fight in ten towns: not open at twelve"),
    # [76]
    "homesick": dict(
        age=(16, 110),
        why="a university or emigrant premise: the warden or the tutor, an orientation course, a lift home"),
    # [173]
    "the job in the group nobody else wants": dict(
        age=(15, 88),
        why="taking on a group's organising, its records and its money is not a twelve-year-old's job"),
    # [180]
    "waking up in hospital": dict(
        age=(14, 110),
        options={4: "pull out the drip and head for the door the moment you can stand"},
        outcomes=(["The doctors let {N} go home after two days, with a leaflet, a bruise and a great deal to think about.",
                   "{N} walks out of the hospital into a bright, cold morning and breathes it in."],
                  ["The doctor's face is serious: there is damage that will take months to heal.",
                   "On the third day the questions start: from the family, from school or work, and from people with forms."]),
        why="a minor cannot discharge themselves, and the questions come from school as well as from work"),
    # [45]
    "a box of craft things and a free hour": dict(
        age=(6, 12),
        options={3: "make bead bracelets and swap them with the kids on your street for their best sweets"},
        scenes={"B": "Everyone at school wants bead bracelets this week, and {N} has a whole tub of beads."},
        why="kite instructions, labelled pressings and a card delivered alone are past a three-year-old; selling at six too"),
    # [56]
    "moving to a new town": dict(
        age=(6, 11.99),
        options={1: "collect every friend's address in a notebook, and promise to send each one a drawing"},
        scenes={"W": "{N} has collected every friend's address in a notebook, with help, and means to send each of them "
                     "a drawing, every month, without fail."},
        outcomes=(["Within a month {N} has a new best friend and a favourite path to school.",
                   "The new town has a river, a library and a kid next door who is just as new."],
                  ["{N} spends playtimes alone for weeks, and the drawings sent to old friends get no answer.",
                   "{N} begs every night to go back, and nothing feels right for a long time."]),
        why="addresses, letters, school clubs and the playground's pecking order are not a three-year-old's; ends before its twin"),
    # [54]
    "two houses from now on": dict(
        age=(6, 11.99),
        why="learning the week by heart, packing one's own bag and holding parents to rules are past a three-year-old; ends before its twin"),
    # [57] reworded: a grandparent's death fits the youngest; the child version of 'losing a grandparent'
    "a grandparent dies": dict(
        age=(3, 11.99),
        variant_of="losing a grandparent",
        options={1: "stand up straight at the funeral and lay a flower, the way you were shown",
                 3: "ask to keep your grandparent's button tin, before anyone else can",
                 6: "help a parent make an album of the old photos, and keep it as your own",
                 8: "help feed your grandparent's dog every day, and be proud of it",
                 9: "slip off to the bottom of the garden where you used to feed the birds together, and sit with it"},
        scenes={"W": "There will be a funeral on Friday, and {N} has been given a flower to lay. {N} wants to do it "
                     "properly, for {grandparent}.",
                "B": "The grown-ups talk in low voices about {grandparent}'s house and things. {N} wonders what will "
                     "happen to the tin of buttons {N} always played with."},
        why="reading a poem, claiming a watch, letters, walking the dog and going alone to a pond at three; the same "
            "death as 'losing a grandparent', which could follow within months at twelve"),
    # [46]
    "sharing a room with your sibling": dict(
        age=(6, 12),
        why="a reading hour, a sibling's diary and fines are past a three-year-old"),
    # [29]
    "too much fizz to sit still": dict(
        age=(7, 12),
        why="organising a street race, digging a neighbour's patch for a coin and walking the fields alone at four"),
    # [33]
    "a stray dog follows you home": dict(
        age=(7, 14),
        options={1: "ask a grown-up to take it to the vet, so they can find its owner"},
        why="a four-year-old cannot take a dog to the vet or go door to door for a reward; at seven the vet still needs a grown-up"),
    # [51]
    "a jar of tadpoles": dict(
        age=(6, 11),
        options={2: "draw the tadpoles every day in a little book, to show the class how they change"},
        why="a diary for a science fair and a class rota and chart are past a four-year-old; science fairs past a six-year-old"),
    # [40]
    "a board game night with the family": dict(
        age=(8, 12),
        why="the game is a property-trading one (banker, cheap streets), played from about eight"),
    # [11]
    "the morning things feel better": dict(
        age=(8, 12),
        why="recovering from a low patch, writing down what helped and biking off with no plan fit eight, not five"),
    # [32]
    "a test at school tomorrow": dict(
        age=(8, 14),
        why="revising, flashcards and questions worth the most marks are not a six-year-old's"),
    # [10]
    "saving up for something big": dict(
        age=(8, 12),
        why="weighing a cheaper bike now against a better one later, and odd jobs for neighbours, fit eight, not six"),
    # [15]
    "trusted with a grown-up job": dict(
        age=(8, 12),
        why="sent to the shop alone with the purse and the change: about eight, not seven"),
    # [49]
    "the school play": dict(
        age=(7, 12),
        options={2: "ask to help the teacher with the lights, and learn what every switch does"},
        why="minding the little ones backstage and working the lights and sound are not a five-year-old's"),
    # [135]
    "the garden bird count": dict(
        age=(7, 14),
        why="an hour by the kitchen clock, the bird book and writing the names in need a reader of about seven"),
    # [131] reworded for four; the child version of 'living with a chronic illness'
    "growing up with an illness": dict(
        age=(4, 11.99),
        options={1: "take the medicine at the right times every day, and put a sticker on the chart each time",
                 2: "ask the nurse how it all works, and help with the checks yourself",
                 4: "spit the medicine out when nobody is looking, and run off to play",
                 7: "show the other children at nursery or school how your kit works, with a grown-up's help"},
        why="a four-year-old does not take medicine unreminded, check it alone or explain an illness to a class; ends before its twin"),
    # [41] reworded for three
    "a holiday meal with the whole family": dict(
        options={2: "sit on your great-uncle's knee and ask him for stories about the old days",
                 3: "sit on the lap of the aunt with the biggest presents, and give her your best smile",
                 6: "lift your cup with the grown-ups for the toast, and say cheers at just the right moment",
                 7: "crawl under the table to hear what the grown-ups at the far end are whispering about"},
        why="buttering up a rich aunt, a word-perfect toast and learning family secrets are not a three-year-old's"),
    # [39] reworded for three
    "a day at the beach": dict(
        options={1: "stay between the flags, and hold a grown-up's hand in the water",
                 7: "watch the waves creep up the sand, and warn your family before they reach the towels",
                 9: "race your sibling to the water's edge and back, and shout that you won"},
        why="minding the younger ones in the water, reading a tide board and buying ice creams at three"),
    # [37] reworded for three
    "the last slice of birthday cake": dict(
        options={2: "challenge your sibling to a guessing game, winner takes the slice",
                 6: "ask a grown-up to be the judge, and let them decide fairly who has it"},
        why="a times-table quiz and a vote are not a three-year-old's"),
    # [44] reworded for three
    "a thunderstorm at night": dict(
        options={2: "count out loud between the flash and the boom, to see if the storm is going away",
                 8: "sneak the tablet under the covers and watch cartoons until the storm stops"},
        why="working out the storm's distance and looking up how storms work need a reader"),
    # [50] reworded for three
    "a long car journey": dict(
        options={2: "look out for every sign and bridge, and ask what each one is",
                 7: "shout out every animal you spot, and ask its name"},
        scenes={"U": "{N} presses against the window, asking what every sign, bridge and river is, and where they all go."},
        why="following the road atlas and keeping a written list need a reader"),
    # [177] reworded for three
    "going into foster care": dict(
        options={7: dict(label="notice which grown-up everyone listens to, and stay close to that one",
                         act="notice which grown-up everyone listens to, and stay close to that one"),
                 10: "draw pictures of everything that happens, to show your parents one day"},
        scenes={"U": "{N} counts the turns on the drive and watches every sign go by, trying to work out how far away "
                     "home is, and how long \"for now\" means."},
        why="a diary and reading every sign are past a three-year-old, and so is working out who decides things"),
    # [3] reworded for four
    "the sibling who always gets more": dict(
        options={2: "keep count of every unfair thing, and tell them all to a parent as proof",
                 8: "trade the sibling a turn on your bike for first pick of the sweets"},
        scenes={"U": "{N} keeps careful count of every time it happens, as proof."},
        why="a dated list and homework are not a four-year-old's"),
    # [27] reworded for four
    "a question that will not go to bed": dict(
        options={1: "ask a grown-up who knows in the morning, and remember exactly what they say",
                 6: "go on every nature walk the nursery or school puts on, and listen to the guide",
                 7: "look at the pictures in the big animal book, then explain it to the family at dinner"},
        why="writing down the teacher's answer, the encyclopedia and a school club are past a four-year-old"),
    # [28] reworded for four
    "an itch to build something": dict(
        options={2: "draw a plan first, with a door and a window, then build it just like the picture",
                 6: "build a kit from the box with a grown-up, and follow each step their way"},
        why="a plan with measurements and a Saturday model club are past a four-year-old"),
    # [1] reworded for five
    "voices raised downstairs after bedtime": dict(
        options={7: "draw what you heard in a secret book with a little lock",
                 8: "make them both a card in the morning, to smooth things over"},
        why="a written diary and making hot tea are not a five-year-old's"),
    # [43] reworded for five
    "your first pocket money": dict(
        options={2: "count your coins against the prices in the shop, with a parent, before choosing anything",
                 3: "lend your sibling a coin, and ask for a sweet back as well",
                 4: "beg to be taken to the shop, and spend the lot on sweets the same afternoon"},
        why="comparing three shops, lending at interest and running to the shop alone are past a five-year-old"),
    # [13] reworded for five
    "a den of your own": dict(
        options={1: "make the den rules with your friends, and draw them on a sign by the door",
                 2: "keep a nature scrapbook in the den, and watch the birds through the gap"},
        scenes={"W": "{N} has made rules for the den and drawn them on a sign by the door: no shouting, and knock first."},
        why="written rules and a nature diary need more writing than a five-year-old has"),
    # [155] reworded: the bedtime song fits three; school and assembly do not
    "the song learned at a parent's knee": dict(
        options={6: "sing it every morning on the way out of the house, stamping on the beat",
                 9: "put a hand up at circle time when the teacher asks who knows a song"},
        why="the walk to school and school assembly at three"),
    # [4] reworded for four
    "the same bad dream again": dict(
        options={7: "look at a picture book about dreams with a parent, and plan a way to wake up from them"},
        why="reading a library book on dreams at four"),
    # [23] reworded for four
    "a new baby takes up all the room": dict(
        options={7: "watch the baby every day, and tell the grown-ups when it is hungry or sleepy"},
        why="a written chart of feeds and naps at four"),
    # [24] reworded for four
    "nobody watches the cartwheel": dict(
        options={8: "talk an older cousin into teaching you a magic trick to amaze everyone"},
        why="pocket money of one's own at four"),
    # [58] reworded for four, still natural at sixteen
    "a pet of your own": dict(
        options={2: "watch the kitten for hours, and learn what its tail is saying",
                 6: "ask the vet how to look after it properly, and remember every word"},
        scenes={"W": "{parent} has written a list on the fridge: feed twice a day, fresh water, clean the tray. {N} has "
                     "it read out twice and nods, very seriously.",
                "U": "{N} watches the kitten for hours, and wants to know what every twitch of that tail means."},
        why="reading library books and the fridge list and writing down the vet's advice at four"),
    # [120] reworded for four; the child version of 'a narrow escape'
    "a close call on the road": dict(
        age=(4, 11.99),
        options={7: "learn the road rules properly, and say them out loud at every kerb"},
        why="being allowed out alone again is not a four-year-old's; ends before its twin"),
    # [48] reworded for five
    "a new kid joins your class": dict(
        options={2: "correct the way the new kid says things, in front of the whole class"},
        why="correcting grammar at five"),
    # [18] reworded for five
    "a fib that will not stop nagging": dict(
        options={2: "draw a sorry picture and leave it on the kitchen table",
                 8: "quietly put something of your own in its place, and say nothing"},
        why="a written note and saving pocket money to buy a new vase are past a five-year-old"),
    # [36] reworded for five
    "your little cousin comes to stay": dict(
        options={2: "learn your cousin's card game, then win every round by peeking at the cards",
                 5: "show your cousin the den at the bottom of the garden that only family knows about"},
        why="marking cards and taking a small cousin to a den by the stream are not a five-year-old's"),
    # [52] reworded for five
    "sports day": dict(
        options={2: "practise your start in the garden until you push off faster than anyone",
                 7: "work out who runs fastest in your team, and tell the teacher"},
        why="weeks of practice and setting a relay order are past a five-year-old"),
    # [14] reworded for six
    "a promise kept all week": dict(
        options={9: "rush everyone into the car at dawn, feed the rabbit, and still reach the party early"},
        why="biking alone across town at six"),
    # [17] reworded for six
    "a friend's new bike stings": dict(
        options={2: "ask how the bell and the gears work, then help a grown-up do up your old bike"},
        why="fixing gears alone at six"),
    # [25] reworded for six
    "standing up for someone smaller": dict(
        options={10: "hold the little one's hand at the school gate every day, and learn which kids to steer clear of"},
        why="walking a smaller child to school alone at six"),
    # [137] reworded for six
    "practice before tea": dict(
        options={8: "beg to switch to the better teacher across town, and offer your birthday money towards it"},
        why="paying for lessons across town oneself at six"),
    # [189] reworded for six
    "the summer show casts its lead": dict(
        options={10: "stay out of the show this year, and keep Saturdays for the lessons you already go to"},
        why="keeping up with school is not a six-year-old's reason"),
    # [188]
    "auditions for the school production": dict(
        age=(11, 17),
        why="a drama teacher and rehearsals until the spring holidays mean secondary school"),
    # [99]
    "a new hobby you cannot put down": dict(
        age=(12, 18),
        why="charging neighbours and making a name online are not a ten-year-old's"),
    # [107]
    "a close friend moves away": dict(
        age=(12, 18),
        why="train times, savings and a cut of a friend's sale are not a ten-year-old's"),
    # [100]
    "your sibling is in trouble and you know why": dict(
        age=(12, 18),
        options={5: "go with your sibling and pay off the rest together, out of your pocket money"},
        why="a debt premise, and savings of one's own, at ten; at twelve it is pocket money"),
    # [103]
    "a friend is being picked on": dict(
        age=(11, 17),
        why="a gang in the year group, the corridors and a head of year mean secondary school"),
    # [109] reworded for eleven
    "you win a scholarship or a place": dict(
        options={10: "ask straight out whether the place comes with the bus fare and the uniform paid, and hold out for both"},
        why="bluffing another offer is not an eleven-year-old's act"),
    # [184] reworded: water tests from the brook fit a twelve-year-old
    "your record does not match the official one": dict(
        options={6: "file it through the agency's own complaints form, so it has to answer",
                 8: "offer the upstream farmer a copy of your records, if he shows you where his drains run"},
        why="getting the parish council to log a complaint and bargaining records with a farmer are adult acts"),
    # [146] reworded for twelve
    "the band comes home after the flood": dict(
        options={2: "help count the buckets for the night, so every gift is counted and seen",
                 3: "fill a bucket of your own, and get your name read out from the stage for it",
                 9: "get a local firm to match every bucket's takings, and say so on the night"},
        why="keeping the books, a business of one's own and matching gifts from one's own savings at twelve"),
    # [153] reworded for twelve
    "the family in the flat below": dict(
        options={3: "put the father in touch with someone who needs an accountant, and be owed a favour",
                 9: "help raise the money for the children's school trip, so they are not left out"},
        scenes={"B": "The father was an accountant at home, the neighbours say. {N} knows someone who needs one."},
        why="knowing a firm that needs an accountant and paying for a school trip at twelve"),
    # [142] reworded for twelve
    "the folk festival in the field": dict(
        options={3: "help sell the family's old craft at a stall, and come home with orders",
                 9: "help raise the money for a coach so the care home's old folk can come for a day"},
        why="an order book of one's own and paying for a coach at twelve"),
    # [149] reworded for twelve
    "the old rail yard becomes a park": dict(
        options={3: "help run a stall on the market square on Saturdays",
                 9: "help raise money for a bench with a plaque, and see that it is kept"},
        why="renting a stall and paying for a bench at twelve"),
    # [150] reworded for twelve
    "the library reopens after the refit": dict(
        options={1: "help at the free reading class on Thursday evenings, setting out the books",
                 9: "help raise money for a shelf of new books, with the family's name on a small plate"},
        why="running a reading class for grown-ups and paying for a shelf at twelve"),
    # [152] reworded for twelve
    "a weekend school for the old language": dict(
        options={3: "offer to help teach the youngest ones at the weekend school, and make a name there",
                 10: "help make simple word cards, so every class learns the same words"},
        why="teaching for a wage and writing a course book at twelve"),
    # [145] reworded for twelve
    "a novel in the home tongue": dict(
        options={3: "keep to the ruling tongue at school, at work and on paper, where it still counts for more",
                 9: "raise money for copies of the novel for the town library and the care home"},
        why="the ruling tongue at work and paying for copies at twelve"),
    # [144] reworded for twelve
    "a free music school with instruments to borrow": dict(
        options={3: "put yourself forward to help run the school, and see where it leads"},
        scenes={"B": "The school will need people to help run it, and there is talk of a paid post one day. {N} likes "
                     "the idea of being the one in charge."},
        why="applying for the paid post running the school at twelve"),
    # [143] reworded for twelve
    "the song about the empty chair": dict(
        options={3: "sing the war songs at every gathering that will have you, and make your name"},
        why="touring the camps and town halls to make a name at twelve"),
    # [147] reworded for twelve
    "the fast ends and the table fills": dict(
        options={3: "use the meal to patch up a quarrel that has been getting in your way"},
        why="a quarrel that has been costing money at twelve"),
    # [178] reworded for twelve
    "everyone is suddenly on the new medium": dict(
        options={10: "speak up for sensible rules on it, wherever people will listen"},
        why="rules for children at the school meeting is a parent's line"),
    # [78] reworded for twelve
    "feeling invisible": dict(
        options={3: "make yourself the one everyone has to ask: the keys, the plans, the list",
                 6: "stand for a seat on a council, a committee or the school council, so your voice has to count"},
        why="holding the money and standing for the council at twelve"),
    # [79] reworded for twelve
    "a sense of injustice": dict(
        options={1: "expose the one responsible in public, and keep at it until they are made to answer for it",
                 3: "get yourself a say where such rules are made, on a council or a committee"},
        why="campaigning until someone loses their post and a seat at the table at twelve"),
    # [121] reworded for twelve
    "losing a grandparent": dict(
        options={3: "help sort through their things, and ask for the keepsake in return",
                 6: "plead hard against selling the old house, so it stays in the family",
                 9: "step up and take on what needs doing, since nobody else will"},
        why="clearing a house, arguing over its sale and organising a funeral are not a twelve-year-old's"),
    # [124] reworded for twelve
    "earning a qualification": dict(
        options={3: "use it at once to ask for more: a better place, a bigger say, a step ahead"},
        why="bargaining for more money at twelve"),
    # [115] reworded for twelve
    "a friend for life": dict(
        options={3: "start something together, a band, a stall or a business, and share what it brings"},
        why="a venture sharing risk and profit at twelve"),
    # [126] reworded for twelve
    "a stranger saves you, or you save one": dict(
        options={3: "put the story and the video out for everyone to see, and enjoy the fame"},
        why="selling a story to the highest bidder at twelve"),
    # [132] reworded for twelve
    "a long dark season": dict(
        options={7: "read up on the illness, and ask hard questions about every treatment offered"},
        why="a minor does not choose their own treatment"),
    # [89] reworded for twelve
    "inspiration strikes": dict(
        options={3: "ask to learn from them, and make yourself indispensable",
                 6: "sign up for proper lessons or a course, and aim for its top prize"},
        why="asking for a job and an academy's formal programme at twelve"),
    # [182] reworded for twelve
    "a project online asks for a thousand pairs of eyes": dict(
        options={3: "log every hour you put in, and climb to the top of the leaderboard"},
        why="a CV at twelve"),

    # ---- 2. adult moments whose words did not fit every age in their window --------------------------------------
    # a threshold season's moments share one window (the season opens at an age within it), so narrowing this one to
    # about fifty would move the whole mature season there: reworded to fit 42 to 52 instead
    "the morning you turn fifty": dict(
        setting="you wake up on a birthday that feels bigger than the others, and the cards on the doormat say the "
                "number in large gold figures",
        scenes={"": "{N} wakes up on a birthday that feels bigger than the others. The cards on the doormat say the "
                    "number in large gold figures, and the face in the bathroom mirror does not argue.",
                "W": "The family has booked a table for Saturday: a cake, a speech, a photograph with everyone in it. "
                     "Marking the day properly is a thing {N} means to do well.",
                "U": "Before getting out of bed {N} does the sum: with ordinary luck, there are still a good many years "
                     "ahead, but fewer now than there are behind.",
                "B": "Past the middle of the road, and most of it spent on what other people needed. The thought "
                     "arrives with the first coffee: the next part is for {N}.",
                "R": "The number on the cards is past forty, and {N} feels about twenty-six. The tattoo talked out of "
                     "at eighteen, the motorbike in the showroom window: the old wants are all still there."},
        outcomes=(["The day turns out better than {N} feared, and the year after it better still.",
                   "Somewhere between the cake and the last guest, {N} stops minding the number."],
                  ["The day comes and goes, and {N} feels every one of the years.",
                   "The plan goes wrong, and the birthday is remembered in the family for the wrong reasons."]),
        why="open from 42 to 52 (its threshold season's window), but its words were a fiftieth birthday"),
    "the birthday party that ends at eleven": dict(
        scenes={"U": "{N} counts it up, half amused: a dentist twice a year, a favourite saucepan, opinions about "
                     "gutters. When did all of that happen?",
                "R": "It is not even midnight. {N} refuses to let the night, or the wild years, end like this."},
        options={5: "sit out on the step at the end, alone, and let the wild years go"},
        outcomes=(["The night ends well, and {N} wakes oddly at peace with the years behind.",
                   "Something {N} said or did that night turns out to be the start of the next chapter."],
                  ["The night ends badly, and the next day goes on apologies.",
                   "{N} wakes with the feeling of having missed something, and it stays for weeks."]),
        why="open from 24, but a pension statement and the end of a decade read as a thirtieth birthday"),
    "your partner dies": dict(
        scenes={"B": "Decades of sharing everything, and now the money, the house and every decision rest on {Ns} "
                     "shoulders alone."},
        why="fifty years of sharing everything at 45"),
    "moving to a smaller home or into care": dict(
        scenes={"": "Decades of things in one house, and the new flat has two rooms. {N} stands in the attic with a "
                    "roll of bin bags."},
        why="forty years of things in one house at 55"),
    "a late love": dict(
        scenes={"G": "{N} thought that part of life had closed, like a season. But here is spring, of all things, "
                     "this late in life."},
        why="'in the seventies' for a love open from 55"),
    "an old flame gets in touch": dict(
        scenes={"": "A message arrives from someone {N} loved at twenty and has not seen in decades: a faded "
                    "photograph, and the words \"remember this?\"",
                "R": "The years fall away in a heartbeat, and {N} is twenty again, with a pounding chest."},
        outcomes=(["Whatever it becomes, an old wound closes, and {N} feels lighter for it.",
                   "{N} and {prospect} find they still have plenty to say after all these years."],
                  ["The meeting is awkward, and both of them wish they had left the past alone.",
                   "Someone sees them together, and the talk starts."]),
        why="loved at twenty and not seen in thirty years fits fifty only, in a window of 40 to 65"),
    "a sudden urge to buy something big": dict(
        scenes={"W": "For years {N} has saved carefully. There is money for once, and a quiet voice says it is meant "
                     "for the family."},
        why="thirty years of careful saving at 40"),
    "a chance to change everything": dict(
        scenes={"": "The house is nearly paid, the heaviest duties of the middle years are lifting, and a buyout "
                    "offer would cover two lean years. For the first time in decades, the next step is wide open."},
        why="thirty years of working life at 42"),
    "up the ladder to clear the gutters": dict(
        scenes={"B": "The firm that does gutters wants a day's wages for twenty minutes' work, and {N} did this job "
                     "for decades without paying anyone."},
        why="forty years of clearing one's own gutters at 55"),
    "a late chance to see the world": dict(
        setting="with the children grown and time at last, someone hands you a ticket to a place you have only seen "
                "on television",
        scenes={"W": "{N} spent decades keeping things running at home. There was always a reason to stay. Now the "
                     "reasons have run out."},
        why="'at sixty' and forty years of keeping house, for an echo open from 50"),
    "the late starter": dict(
        age=(45, 80),
        scenes={"": "The children have left home, the job has ended with a cheque and a handshake, and {N} has played "
                    "at the local theatre for years, always for nothing. On the kitchen table lie adverts cut from the "
                    "papers: a playhouse that wants older actors for its company, an agency that takes on mature "
                    "actors, a film that wants real faces with some years in them, and a touring company that casts "
                    "local people in every town.",
                "R": "{N} reads the advert for real faces with some years in them and laughs out loud. A whole life of "
                     "wanting it, and now the face is the qualification."},
        outcomes=(["A letter comes three weeks later with a start date, and {N} stands in the kitchen reading it aloud "
                   "to nobody, twice.",
                   "Whatever {N} chose, the late start was a real one, and the years that follow have a stage in them "
                   "somewhere."],
                  ["{N} is the oldest in the waiting room by a generation, plays the scene well, gets a kind no, and "
                   "sits outside in the sun afterwards with a coffee, oddly pleased to have been there at all.",
                   "The answer is a letter that praises the nerve and the years on the local stage in one honest "
                   "sentence, and gives the place to someone with twenty years in the trade."]),
        why="grown children and a late start at 35, faces 'over fifty', and thirty years older than the waiting room"),
    "never too late for the stage": dict(
        scenes={"W": "For decades {Ns} week belonged to someone else's timetable. A society with a rehearsal schedule "
                     "and a part to learn by a date is a shape {N} understands."},
        why="forty years of someone else's timetable at 55"),
    "the late starter at the easel": dict(
        options={8: "enter the open show for late starters, and go to the opening in a good coat"},
        why="an open show for over-sixties, for a moment open from 58"),
    "hands that will not hold the brush": dict(
        scenes={"B": "{N} has spent years building a name. The question is how to keep it working when the hands "
                     "will not."},
        why="thirty years building a name at 40"),
    "the sketchbook in the attic": dict(
        scenes={"B": "{N} looks at the best drawing for a long time. It is good, really good, and nobody has seen it "
                     "in years. {N} wonders what it might have led to."},
        why="a school sketchbook unseen for thirty years at 30"),
    "the poems you never showed anyone": dict(
        scenes={"": "After the loss, or the last day at work, the days are suddenly wide and quiet. At the back of a "
                    "drawer {N} finds the notebook: years of poems, written late at night, on trains and in waiting "
                    "rooms, and never shown to a single person.",
                "R": "{N} reads the first one and has to sit down on the floor. Every feeling of those years is in "
                     "there, as raw as the day it was written."},
        why="thirty years of poems at 25"),
    "the speech at the party conference": dict(
        scenes={"G": "Somewhere in the hall are the branch members from home who knocked on doors for {N} in the "
                     "first campaign. {N} looks for their faces before the lights go up."},
        why="campaigners from thirty years ago at 25"),
    "the oldest member wants the lead again": dict(
        scenes={"R": "{elder} taught {N} to act, years ago, in this same hall. The lump in {Ns} throat comes before a "
                     "word is said."},
        why="taught to act thirty years ago, for a moment open from 18"),
    "a friend's secret would make the book": dict(
        scenes={"G": "Years of friendship: the weddings, the funerals, the long walks. {N} thinks of {friend} reading "
                     "the book in the chair by the window."},
        why="thirty years of friendship at 18"),
    "a friend asks you for an alibi": dict(
        scenes={"G": "{friend} has been family to {N} for half a lifetime: weddings, funerals, the bad winter. "
                     "Families stand together; that is what {N} was always taught."},
        why="a friend of thirty years at 25"),
    "everything rested on the one thing": dict(
        scenes={"W": "{N} gave the mill years of loyal work, and believed the loyalty would be returned. The notice on "
                     "the gate says otherwise.",
                "U": "{N} realises there was never a second plan. Years of one skill, one employer, and no alternative "
                     "ever worked out."},
        options={2: "start learning a new trade at the college, whatever your age"},
        why="thirty years at the mill and retraining 'at fifty' for an echo open from 25"),
    "buying a home": dict(
        setting="you sign for a house and a mortgage that will run for years",
        scenes={"": "The offer is accepted. {N} holds a set of keys and a mortgage that will be {Ns} to carry for years "
                    "to come.",
                "W": "{N} reads the mortgage contract slowly, because a debt of many years is a promise, and {N} keeps "
                     "promises."},
        why="a thirty-year mortgage for a purchase open to 85"),
    "the loan the new owners call in": dict(
        options={5: "ask the family for a loan, as your parents once asked theirs"},
        why="borrowing from one's parents, for a moment open to 85"),
    "the rent goes up by a fifth": dict(
        options={5: "move in with family for a year to save"},
        scenes={"G": "{Ns} family lives two streets away, and all of {child}'s friends are on this street."},
        why="moving in with one's parents, and parents two streets away, for a moment open to 90"),
    "a cushion of your own": dict(
        options={8: "buy the cottage near the family while prices are low"},
        why="a cottage near one's parents, for an echo open to 110"),
    # with no living-parent condition of its own, a stroke-struck parent at 90 is a parent of about 115
    "deciding for a parent who cannot speak": dict(
        age=(30, 75),
        why="a parent's stroke decision open to 90, when almost nobody of 76 or more has a living parent"),
    "last year's answers": dict(
        scenes={"U": "{N} came to learn the thing, not to pass a test. But {friend} says everyone else has the answers, "
                     "and that only the paper counts in the end, and {N} cannot quite argue."},
        why="a test that decides who gets the job, in an inner moment open to 110"),
    "two evening classes and time for one": dict(
        setting="you have time for one evening class: the one you love for its own sake, or the one with a "
                "certificate people take notice of",
        scenes={"": "There is room for one evening class this term. One is the old history course {N} has wanted for "
                    "years, just for the joy of it. The other is a certificate that people take notice of."},
        options={6: "take the certificate, and talk someone into paying for the history class too"},
        why="a certificate that counts at work and a boss who pays, in an inner moment open from 14 to 110"),

    # ---- 3. twins at 12: child versions shut the week before their twin opens -------------------------------------
    # (the review's twins, 'moving to a new town', 'two houses from now on', 'growing up with an illness', 'a close
    # call on the road' and 'a grandparent dies', are above with their rows)
    "a teacher who sees something in you": dict(
        age=(6, 11.99), why="open in the same week as its twin 'a teacher or coach who believes in you' at 12"),
    "losing a parent too soon": dict(
        age=(3, 11.99), why="open in the same week as its twin 'a parent dies' at 12"),
    "a best friend of your own": dict(
        age=(6, 11.99), why="open in the same week as its twin 'a friend for life' at 12"),
    "a club where you belong": dict(
        age=(7, 11.99), why="open in the same week as its twin 'welcomed into a community' at 12"),
    "an operation that makes things better": dict(
        age=(4, 11.99), why="open in the same week as its twin 'an operation gives something back' at 12"),
    "the badge you worked for": dict(
        age=(9, 11.99), why="open in the same week as its twin 'earning a qualification' at 12"),
    "a stranger to the rescue": dict(
        age=(6, 11.99), why="open in the same week as its twin 'a stranger saves you, or you save one' at 12"),
    "a sadness that will not lift": dict(
        age=(8, 11.99), why="open in the same week as its twin 'a long dark season' at 12"),
}
