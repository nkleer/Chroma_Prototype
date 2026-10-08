"""Chroma library stage: compiled by build.py from stage.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'a flyer for the youth theatre',
 'stages': 'child juvenile',
 'age': (8, 17),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.03,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'play, school, performing',
 'horizon': 'week',
 'roles': "friend, a parent or carer, a cousin, the youth theatre's leader",
 'share': 0.45,
 'share_group': 'youth_doors',
 'worlds': {'earth': 'a flyer in the school bag for the youth theatre on Saturday mornings',
            'tribal': "the old teller calls the children to the fire to learn the small spirits' parts for midwinter",
            'magic': "the players' guild's children's company calls for new children at the spring fair, a parent's "
                     'mark on the roll'},
 'timing': {'times': 'per child or teenager a year: about 1 in 5 children see an invitation to a youth theatre or a '
                     "stage school class; the youth theatres' national census counted over 100,000 young people in "
                     '414 youth theatres in England in 2024, and about 8 lives in 100 belong to one at some point '
                     '(catalogue share; estimate)',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'A flyer comes home crumpled at the bottom of {Ns} school bag: the youth theatre meets on '
                       'Saturday mornings in the community hall, with games, a summer show and the first term free. '
                       'A parent or carer has to sign the form.'),
                      ('W',
                       'The flyer asks for a signed form and a promise to come every week. {N} likes knowing exactly '
                       'what is expected, and keeping to it.'),
                      ('U',
                       '{N} reads the flyer twice: voice games, how a stage fight is made safe, how actors remember '
                       'all those lines. {N} would like to know how it is done.'),
                      ('B',
                       'An older girl from the youth theatre was on television last year, and the whole school knows '
                       'it. {N} looks at the flyer and thinks about that.'),
                      ('R',
                       '{N} is already acting out a dragon in the kitchen with the flyer in one hand. Saturday '
                       'cannot come fast enough.'),
                      ('G',
                       '{friend} goes to the youth theatre already, and so did a cousin before that. It meets in the '
                       'hall at the end of the road, where the summer fair is held every year.')],
            'tribal': [('',
                        'At dusk the old teller calls the children of the band to the fire. Midwinter is coming, the '
                        'small spirits need players, and any child whose mother gives leave may come and learn, with '
                        'the women of the band sitting close by.')],
            'magic': [('',
                       "At the spring fair the players' guild sets up a stall with masks and painted wings. Its "
                       "children's company wants new children, if a parent will put a mark on the roll, and the "
                       "guild's matron keeps the little ones together.")]},
 'outcomes': (['{N} is there from the very first meeting, and comes home hoarse and happy, full of games and new '
               'names.',
               'The question is settled within the week, and {N} is glad of the way it went.'],
              ['Nobody gives the leave in time, and the places are all taken before {N} can have one.',
               'The first meeting is all strangers and loud games, and {N} does not go back.']),
 'options': [
    ('ask a parent to sign the form tonight, and be there every Saturday at nine', 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'youth theatre member', 'habit': True, 'world': {'tribal': "ask your mother's leave, and sit at the teller's fire every evening until midwinter", 'magic': 'ask a parent to put their mark on the roll, and never miss a practice'}, 'chance': 0.85}),
    ('ask a parent to ring up and find out what the children actually learn there', 'U1', None, 0.45, '', {'door': True, 'v': 'self-direction', 'world': {'tribal': 'ask the old teller what the children learn at the fire before midwinter', 'magic': "ask a parent to find out what the guild's children are taught"}, 'chance': 0.85}),
    ("get a parent to sign, and ask to go straight into the older children's group", 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'youth theatre member', 'world': {'tribal': "get your mother's leave, and ask the teller for a place among the older children", 'magic': "get a parent's mark on the roll, and ask to start with the older children"}, 'chance': 0.6}),
    ('put on a show in the kitchen until a parent laughs and signs the form', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'youth theatre member', 'world': {'tribal': 'dance the hare by the hearth until your mother laughs and gives her leave', 'magic': 'play the fairy queen for the family at supper until a parent signs the roll'}, 'chance': 0.85}),
    ('stay with football on Saturdays, and the team you have played with for years', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'habit': True, 'world': {'tribal': 'stay with the children who go to the river with the women, as you always have', 'magic': 'stay with the Saturday games on the green, and the friends you have always had'}, 'chance': 0.92}),
    ('ask the class teacher whether it would help with reading aloud in class', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'door': True, 'world': {'tribal': 'ask the elder who teaches the children whether the tellings would help with learning the old words', 'magic': "ask your tutor whether the guild's lessons would help with your recitations"}, 'chance': 0.7}),
    ('read the small print, and ask a parent to apply for one of the free places', 'U1', 'B.7', 0.5, '', {'v': 'achievement, security', 'aims': 'youth theatre member', 'world': {'tribal': 'find out which children the teller takes without a gift, and ask your mother to speak to the teller', 'magic': "read the guild's notice to the end, and ask a parent to apply for a free place"}, 'chance': 0.7}),
    ('say no: Saturday mornings are for lie-ins and cartoons', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'habit': True, 'world': {'tribal': 'say no: the evenings are for games by the river, not learning parts', 'magic': 'say no: feast-day mornings are for sleeping late and the puppet show'}, 'chance': 0.95}),
    ('say you will go only if your best friend from the street comes too', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'binds': True, 'world': {'tribal': "say you will go to the teller's fire only if your hearth-friend comes too", 'magic': 'say you will join only if your best friend from the lane joins too'}, 'chance': 0.7}),
    ('get a parent to sign, then go with your cousin and help with the little ones', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'title': 'youth theatre member', 'world': {'tribal': "go to the teller's fire with your cousin, your mother's leave given, and mind the little ones", 'magic': "go with your cousin, a parent's mark on the roll, and help with the smallest children"}, 'chance': 0.63}),
 ]},
{'name': 'auditions for the school production',
 'stages': 'child juvenile',
 'age': (8, 17),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.03,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'school, performing',
 'horizon': 'week',
 'roles': 'friend, rival, the drama teacher, a parent or carer',
 'share': 0.45,
 'share_group': 'youth_doors',
 'worlds': {'earth': "the auditions notice for the school's spring show on the hall door",
            'tribal': 'the elders choose which children will play the animals in the great telling at midsummer',
            'magic': 'the schoolmaster wants players for the feast-day masque, and the best part is the fairy queen'},
 'timing': {'times': 'per child or teenager a year: about 1 in 5 meet auditions for a school production they could '
                     'try for; most secondary schools put on a show a year, with one or two leads (estimate)',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'A notice goes up on the hall door: auditions for the spring show on Thursday after school, a '
                       'speech or a song, everyone welcome. There are two big parts, a dozen small ones, and a crew '
                       'wanted for the set and the lights.'),
                      ('W',
                       'The notice lists what to bring and when to arrive, and the drama teacher says everyone who '
                       'comes prepared will get a part. {N} copies the times into a planner.'),
                      ('U',
                       '{N} borrows the script and reads the whole play in one evening. The lead has the best lines, '
                       'and also the hardest ones.'),
                      ('B',
                       '{rival} is already telling the class the lead is as good as theirs. {N} would very much like '
                       'to see that face when the cast list goes up.'),
                      ('R',
                       '{Ns} heart jumps at the notice. A real stage, real lights, the whole school watching: {N} '
                       'wants it so badly it hurts.'),
                      ('G',
                       '{Ns} cousin was in the spring show years ago, and the photograph is still on the corridor '
                       'wall. Half of {Ns} friends are going along on Thursday.')],
            'tribal': [('',
                        'The elders sit at the edge of the dancing ground and call the children one by one: who will '
                        'be the hare, who the crow, who the great elk in the midsummer telling. The mothers watch '
                        'from the shade.')],
            'magic': [('',
                       'The schoolmaster pins a notice to the schoolroom door: players wanted for the feast-day '
                       'masque, and the best part, the fairy queen, still to be cast. The trials are after lessons, '
                       'with the parents welcome to watch.')]},
 'outcomes': (['When the parts are given out, {Ns} name is where {N} hoped it would be.',
               'Within two weeks {N} knows exactly where to stand, what to do, and whose line is the cue.'],
              ['When the parts are given out, {Ns} name is further down than {N} hoped.',
               'On the day {N} loses nerve at the door, and walks home instead.']),
 'options': [
    ('offer to cover the lead in case anyone falls ill, and learn every line anyway', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'grants': 'learning lines', 'world': {'tribal': "offer to learn the hare's part too, in case the chosen child falls sick", 'magic': "offer to learn the fairy queen's lines as a second, in case she falls ill"}, 'chance': 0.35}),
    ('read the whole play first, then audition for the lead with the speech you understand best', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'grants': 'a lead role to remember', 'mark': 'learned a skill', 'world': {'tribal': "listen to every old telling of the hare first, then ask the elders for the hare's part", 'magic': 'read the whole masque first, then try for the fairy queen with the speech you know best'}, 'chance': 0.23}),
    ('go for the lead, and let the drama teacher know nobody wants it more', 'B1', None, 0.45, '', {'v': 'achievement, power', 'grants': 'a lead role to remember', 'identity': True, 'world': {'tribal': "ask for the great elk's part, and let the elders see how much you want it", 'magic': 'try for the fairy queen, and make sure the schoolmaster knows nobody wants it more'}, 'chance': 0.22}),
    ('audition for the lead on the spot, with a speech you made up that morning', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'grants': 'a lead role to remember', 'world': {'tribal': 'jump up and play the hare for the elders, making it up as you go', 'magic': 'try for the fairy queen with a speech you made up on the way to school'}, 'chance': 0.24}),
    ('paint the set and run the lights with the friends who never act', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'grants': 'stagecraft', 'world': {'tribal': 'help the mothers paint the hide screens and gather wood for the fire', 'magic': "help paint the masque's scenery with the friends who never take a part"}, 'chance': 0.88}),
    ('audition for any part, after asking the drama teacher exactly what it needs', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'grants': 'acting', 'world': {'tribal': 'ask the elders what each small part needs, and play whichever part they choose', 'magic': 'ask the schoolmaster what each part needs, and try for whichever suits'}, 'chance': 0.8}),
    ("join the drama teacher's Saturday youth theatre, where she finds her casts, once a parent signs", 'U1', 'B.7', 0.5, '', {'v': 'achievement', 'title': 'youth theatre member', 'world': {'tribal': "ask your mother's leave to learn at the old teller's fire, where the elders find their players", 'magic': "join the guild's children's company, a parent's mark on the roll, where the masque finds its players"}, 'chance': 0.9}),
    ('skip it: the rehearsals would eat every free evening until the spring holidays', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'world': {'tribal': 'skip it: the telling would take every evening you could spend at the river', 'magic': 'skip it: the practices would eat every evening until the feast'}, 'chance': 0.92}),
    ('audition as a pair with your best friend, happy with any parts going', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'grants': 'acting', 'mark': 'made a friend', 'world': {'tribal': 'go before the elders with your hearth-friend, and play two crows together', 'magic': 'try out as a pair with your best friend, glad of any parts'}, 'chance': 0.88}),
    ('ask the drama teacher to let the younger ones from your street sing in the chorus', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'door': True, 'world': {'tribal': 'ask the elders to let the smallest children of your hearth be the young hares', 'magic': 'ask the schoolmaster to let the little ones from your lane sing in the chorus'}, 'chance': 0.3}),
 ]},
{'name': 'the local players need a cast',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.025,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'community, leisure, performing',
 'horizon': 'months',
 'roles': "friend, neighbour, colleague, the society's director",
 'share': 0.15,
 'share_group': 'local_doors',
 'worlds': {'earth': 'a notice in the library window: the local players hold open auditions for the autumn play',
            'tribal': "the band's tellers want more players for the midwinter telling",
            'magic': "the guild's mystery players need new players for the feast-day pageant"},
 'timing': {'times': 'per teenager or adult a year: about 1 in 25 see a call from the local players they could '
                     "answer; the UK amateur theatre association's survey counted 437,800 people taking part (2002), "
                     'and about 4 lives in 100 act with amateurs at some point (catalogue share; estimate)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A notice in the library window: the local players hold open auditions for their autumn play '
                       'on Tuesday evening in the church hall. No experience needed, all ages welcome, and parts for '
                       'eleven.'),
                      ('W',
                       'The society has put on two plays a year for forty years, and the notice says so with some '
                       'pride. {N} likes the thought of helping something that old keep going.'),
                      ('U',
                       '{N} looks the play up: a comedy of manners in three acts, with one part that is all timing '
                       'and another that is all stillness. It would be interesting to find out which {N} could do.'),
                      ('B',
                       'The local paper reviews the players every autumn, and half the town comes to see them. A '
                       "good part would put {Ns} name about, and the society's chair knows everybody."),
                      ('R',
                       '{N} has not been on a stage since school, and has missed it every single year. The thought '
                       'of the lights and the first-night nerves sets {Ns} heart racing.'),
                      ('G',
                       '{friend} has acted with the players for years and keeps saying {N} should come. It is the '
                       'same church hall where {N} went to playgroup, and the same faces at every show.')],
            'tribal': [('',
                        "As the nights lengthen, the band's tellers go from hearth to hearth asking who will play in "
                        'the midwinter telling. They want hunters for the herd, a voice for the wolf, and someone '
                        'who can make the children laugh.')],
            'magic': [('',
                       'A notice goes up at the guild hall: the mystery players need new players for the feast-day '
                       'pageant, no guild token needed, all welcome to try. The pageant wagons are already being '
                       'painted in the yard.')]},
 'outcomes': (['The parts are given out, and {Ns} part has lines worth learning.',
               'By the first rehearsal {N} knows half the company by name, and they know {N}.'],
              ['The night of the choosing clashes with other work, and the parts are given out without {N}.',
               '{N} goes along, reads badly from nerves, and is thanked politely and not called back.']),
 'options': [
    ('go to the open auditions, and promise to be at every single rehearsal', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'title': 'amateur actor', 'binds': True, 'world': {'tribal': 'go to the tellers, and promise to be at the fire every night until midwinter', 'magic': 'go to the trials, and swear to every practice until the feast'}, 'chance': 0.75}),
    ('read the play from the library first, then audition for the part that suits you', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'title': 'amateur actor', 'world': {'tribal': 'listen to the old midwinter tellings first, then ask for the part you could play best', 'magic': 'read the old pageant first, then try for the part that suits you best'}, 'chance': 0.55}),
    ('audition, and make sure the director knows you want a part with real lines', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'amateur actor', 'world': {'tribal': 'go to the tellers, and make sure they know you want more than a place in the herd', 'magic': 'try out, and let the pageant master know you want a part with lines'}, 'chance': 0.55}),
    ('turn up on the night and read for anything, just for the fun of it', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'amateur actor', 'world': {'tribal': "walk into the tellers' circle and play whatever they ask, for the joy of it", 'magic': 'turn up at the trials and read for anything, just for the fun of it'}, 'chance': 0.8}),
    ('audition alongside the neighbour who has been in every play for twenty years', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'amateur actor', 'habit': True, 'world': {'tribal': 'go to the tellers with the old hunter who has played the bear every midwinter of your life', 'magic': 'go to the trials with the neighbour who has played in every pageant for twenty years'}, 'chance': 0.65}),
    ("join the society's committee first, and audition once you know how parts are given", 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'aims': 'amateur actor', 'world': {'tribal': 'sit with the tellers first, and learn how they choose who plays what', 'magic': "join the guild's pageant committee first, and learn how the parts are given"}, 'chance': 0.7}),
    ('watch the dress rehearsal of their spring show, and see whether the spark catches', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'door': True, 'world': {'tribal': 'watch the next telling from the edge of the firelight, and see whether the spark catches', 'magic': 'watch a pageant practice from the yard, and see whether the spark catches'}, 'chance': 0.9}),
    ('say no: the autumn evenings belong to the family', 'B1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'mark': 'turned down a chance', 'world': {'tribal': 'say no: the winter evenings belong to your own hearth', 'magic': 'say no: the evenings belong to the family workshop'}, 'chance': 0.92}),
    ('sell the tickets door to door, with all the cheek you have', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, stimulation', 'body': 'light', 'world': {'tribal': 'go to every hearth and call the families to the telling, with all the cheek you have', 'magic': 'cry the pageant through the lanes, with all the cheek you have'}, 'chance': 0.65}),
    ('help the old set-builder in his shed, and learn how the flats are made', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'grants': 'stagecraft', 'mark': 'learned a skill', 'world': {'tribal': 'help the old mask-maker at her fire, and learn how the masks and screens are made', 'magic': "help the old wagon-wright, and learn how the pageant's scenery is built"}, 'chance': 0.8}),
 ]},
{'name': 'extras wanted for a film in town',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.025,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, community, leisure',
 'horizon': 'week',
 'roles': 'neighbour, friend, colleague, an assistant director',
 'share': 0.15,
 'share_group': 'local_doors',
 'worlds': {'earth': 'a film is shooting in the high street, and the background agency wants locals for a day',
            'tribal': "a neighbouring band's great telling needs many bodies for the herd, the war band and the dead",
            'magic': "the illusionists' procession needs a crowd of townsfolk for its opening night, paid by the "
                     'night'},
 'timing': {'times': 'per teenager or adult a year: about 1 in 25 hear of a call for extras they could answer, more '
                     'in towns where films are made; the largest US background agency has about 200,000 people '
                     'registered, and about 8 lives in 1,000 work as an extra at some point (catalogue share; '
                     'estimate)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'Trucks, cables and a catering van have taken over the high street, and the shop signs have '
                       'been changed to a town that does not exist. A notice in the café window says the background '
                       "agency wants locals for a day: a five o'clock call, a day's pay, and no lines."),
                      ('W',
                       'The notice is very clear: arrive at five, bring two changes of plain clothes with no logos, '
                       'and do exactly what the assistant director says. {N} could do that.'),
                      ('U',
                       '{N} has always wondered how a film is really made: who decides where the camera goes, and '
                       'why it takes all day to shoot a minute. Here is a chance to stand in the middle of it.'),
                      ('B',
                       "A day's pay for standing in a street, and the agency keeps the names of people who turn up "
                       'on time. {N} wonders how many more days a year that could mean.'),
                      ('R',
                       'A real film, with real actors, on {Ns} own high street! {N} wants to be in it, even if only '
                       'as the back of a head.'),
                      ('G',
                       'The whole street is out watching: the baker, the old men from the bench, the children on '
                       'their way to school. {N} has known these pavements all {Ns} life, and now they are going to '
                       'be in a film.')],
            'tribal': [('',
                        'Runners come from the band over the ridge: their great telling needs many bodies for the '
                        'herd, the war band and the dead, and anyone who walks over will be fed for three days.')],
            'magic': [('',
                       'The illusionists have drawn their wagons up outside the walls, and a crier calls for '
                       "townsfolk to walk in the opening night's procession, a copper a night, while the glamours "
                       'blaze overhead.')]},
 'outcomes': (['The day is long and cold and strange, and {N} goes home paid, with a story to tell for years.',
               'Whatever {N} chose, it turns out as {N} wanted, and everyone talks of nothing else for a week.'],
              ['The whole thing is called off at dawn, and {N} hears about it only on arrival.',
               '{N} spends the whole day waiting in the cold, and is used for one moment nobody will ever see.']),
 'options': [
    ("sign up, be there at five, and stand on the crew's exact mark all day", 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'background artist', 'world': {'tribal': "walk over the ridge, and stand in the herd exactly on the shaper's mark", 'magic': "sign up for the procession, and keep exactly to the marks the illusionist's man gives"}, 'chance': 0.4}),
    ('sign up, and spend the day watching how the crew sets up every shot', 'U1', None, 0.45, '', {'v': 'self-direction', 'title': 'background artist', 'world': {'tribal': 'walk over the ridge, and watch how their shaper makes the great telling', 'magic': 'walk in the procession, and watch how the glamours are cast and held'}, 'chance': 0.35}),
    ('sign up, and ask what pays extra: your own car, a costume, a line', 'B1', None, 0.45, '', {'v': 'achievement, security', 'title': 'background artist', 'world': {'tribal': 'walk over, and ask what the band gives for words to speak instead of a place in the herd', 'magic': 'sign up, and ask what pays more than a copper: a costume, a torch, a line'}, 'chance': 0.15}),
    ('sign up just to be in a film, and tell everyone you know', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'background artist', 'world': {'tribal': 'run over the ridge to be in the great telling, and tell every hearth on the way', 'magic': 'sign up for the procession for the fun of it, and tell the whole lane'}, 'chance': 0.5}),
    ('sign up with three neighbours, and stand together in the crowd of your own high street', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'background artist', 'world': {'tribal': 'walk over with your own kin, and play the herd side by side', 'magic': 'walk in the procession through your own streets, beside your own neighbours'}, 'chance': 0.15}),
    ('sign with the background agency properly, photographs and all, for the next calls', 'W1', 'B.7', 0.5, '', {'v': 'security, achievement', 'grants': 'casting directory listing', 'world': {'tribal': 'ask their shaper to remember your name for the tellings to come', 'magic': "put your name on the illusionists' roll for the processions to come"}, 'chance': 0.7}),
    ('ask an assistant director whether locals are ever given a line', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'ask their shaper whether a player from another band is ever given words to speak', 'magic': "ask the illusionist's man whether townsfolk are ever given a line"}, 'chance': 0.75}),
    ("say no: a day's pay will not cover the day off work", 'B1', 'G.7', 0.5, '', {'v': 'power', 'self_control': '+', 'world': {'tribal': 'say no: three days over the ridge is three days of hunting lost', 'magic': 'say no: a copper a night will not cover the shop shut'}, 'chance': 0.92}),
    ("knock on the neighbours' doors so the whole street signs up together", 'R1', 'W.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'made a friend', 'world': {'tribal': 'run to every hearth so the whole band walks over together', 'magic': 'rouse the whole lane to walk in the procession together'}, 'chance': 0.6}),
    ('watch from the pavement with the neighbours, and see how a film is made', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'door': True, 'world': {'tribal': 'watch the great telling from the hillside with your own kin', 'magic': 'watch the procession from your doorstep, and see how the glamours are made'}, 'chance': 0.92}),
 ]},
{'name': 'drama school auditions',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'education, performing, money',
 'horizon': 'months',
 'roles': 'mentor, friend, parent, rival',
 'requires': 'youth theatre member | amateur actor | a lead role to remember | acting',
 'share': 0.12,
 'share_group': 'training_doors',
 'worlds': {'earth': "the drama schools' audition season: forms, fees, two speeches and a song",
            'tribal': 'an old teller of another band will take one apprentice this winter, and asks to see what the '
                      'young ones can do',
            'magic': "the players' guild school opens its doors for the trials at the spring fair"},
 'timing': {'times': 'per young person who acts a year: about 1 in 7 think of applying; about 12,000 apply for about '
                     '1,550 places a year at 22 accredited UK drama schools, about 1 in 8 gets one, and about 3 '
                     'lives in 1,000 train at drama school (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The drama schools' audition season opens in the autumn: a form and a fee for each school, "
                       'two contrasting speeches, sixteen bars of a song, and a train to a city for a day of '
                       'workshops and recalls. Most schools take one applicant in eight, or fewer.'),
                      ('W',
                       'Each school publishes its rules: the length of the speeches, what to wear, the deadlines. '
                       '{N} keeps a folder with every one of them, and {mentor} has offered to hear the speeches '
                       'every week.'),
                      ('U',
                       '{N} has read that the panels look for truth before polish, and has been trying to work out '
                       'what that means in a speech written four hundred years ago.'),
                      ('B',
                       'A place at one of the big schools means agents at the showcase, and agents mean work. {N} '
                       'counts the fees, the schools and the odds, and wonders which panel matters most.'),
                      ('R',
                       '{N} wants this more than anything, and cannot sit still for thinking about it. Two speeches, '
                       'a song, a room of strangers: three minutes to show them everything.'),
                      ('G',
                       'Nobody in {Ns} family has ever done anything like this, and the nearest school is a long way '
                       'from home. {N} thinks about the local players, the friends there, and what leaving would '
                       'mean.')],
            'tribal': [('',
                        'Word comes that an old teller of a band two valleys away will take one apprentice for the '
                        'winter. The young ones who want it must walk there and play before her fire, and she will '
                        'choose one.')],
            'magic': [('',
                       "The players' guild school posts its trials at the spring fair: two pieces, one old and one "
                       'new, a song, and a fee to the guild. The masters take a handful each year from the crowd at '
                       'the door.')]},
 'outcomes': (['Word comes in the spring with the offer of a place, or the thing {N} worked for comes right.',
               'The day of the trial goes well, and {N} leaves knowing every word was true.'],
              ['The answers come back one by one, each a polite no, and {N} keeps every one of them.',
               'The fees, the journeys and the nerves add up, and {N} stops before the season is over.']),
 'options': [
    ('apply to the three schools your drama teacher recommends, and rehearse the speeches by the book', 'W1', None, 0.45, '', {'v': 'conformity', 'title': 'drama school student', 'world': {'tribal': "walk to the old teller with your own elders' blessing, and play the telling exactly as you were taught", 'magic': 'apply to the guild school as your old teacher advises, and learn both pieces by the book'}, 'chance': 0.13}),
    ('spend months on two speeches you understand line by line, then apply', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'title': 'drama school student', 'mark': 'learned a skill', 'habit': True, 'world': {'tribal': 'spend the autumn on one telling until you know why every word is there, then walk over', 'magic': 'spend months on two pieces until you understand every line, then try'}, 'chance': 0.14}),
    ('apply to every accredited school at once, fees and all, to raise your odds', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'drama school student', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'world': {'tribal': 'walk to every teller who might take an apprentice, with a gift for each', 'magic': 'try for every school of players in the realm, and pay every fee'}, 'chance': 0.15}),
    ('audition with the speech you cannot say without crying, and let the panel see it', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'title': 'drama school student', 'identity': True, 'world': {'tribal': 'play the telling that brings the tears, and let the old teller see it', 'magic': 'try with the piece that brings the tears, and let the masters see it'}, 'chance': 0.13}),
    ('audition only at the school in your own city, near family and the local players', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'drama school student', 'world': {'tribal': 'walk only to the teller of the next band along, so your kin are near', 'magic': 'try only for the guild school in your own city, near family and friends'}, 'chance': 0.13}),
    ('ask your old drama teacher to hear your speeches every week until the auditions', 'W1', 'R.7', 0.5, '', {'v': 'conformity, achievement', 'habit': True, 'world': {'tribal': 'ask the old teller of your own band to hear your telling every night until you go', 'magic': 'ask your old teacher to hear your pieces every week until the trials'}, 'chance': 0.85}),
    ('take a foundation year first, and grow into the speeches before auditioning', 'U1', 'G.7', 0.5, '', {'v': 'self-direction, security', 'aims': 'drama school student', 'world': {'tribal': "spend a winter at your own band's fire first, and grow into the telling before walking over", 'magic': "take a year in the guild's preparatory class first, and grow into the pieces"}, 'chance': 0.84}),
    ("take a paid weekend course with one school's own tutors, so they know your face", 'B1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'door': True, 'world': {'tribal': 'bring the old teller a gift in autumn, so she knows your face before the trial', 'magic': "pay for a week of lessons with the guild school's own masters, so they know your face"}, 'chance': 0.83}),
    ('go to every audition you can afford, and treat each one as a lesson', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'grants': 'auditioning', 'door': True, 'aims': 'drama school student', 'world': {'tribal': 'play before every teller who will watch, and learn from each one', 'magic': 'try before every company that holds trials, and learn from each one'}, 'chance': 0.85}),
    ('not this year: work and save the fees, and apply next autumn', 'G1', 'B.7', 0.5, '', {'v': 'security, achievement', 'mark': 'turned down a chance', 'self_control': '+', 'world': {'tribal': 'not this winter: hunt and lay by stores, and walk over next year', 'magic': 'not this year: work and put coin by for the fees, and try next spring'}, 'chance': 0.85}),
 ]},
{'name': 'an open audition in the city',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, performing',
 'horizon': 'week',
 'roles': 'rival, friend, colleague, a casting assistant',
 'requires': 'amateur actor | background artist | drama school student',
 'tenure': (2.0, 100.0),
 'share': 0.12,
 'share_group': 'training_doors',
 'worlds': {'earth': 'an open call for a new show in the city: no agent needed, and the queue is round the block by '
                     'seven',
            'tribal': "the keeper of the gathering's tellings will hear any player before the summer telling",
            'magic': 'a travelling company sets up its wagons in the square and will hear anyone who wants to join'},
 'timing': {'times': 'per amateur actor, extra or drama student of two years or more a year: about 1 in 10 go to an '
                     'open call for paid work; most open calls cast a handful from hundreds (estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'An open call for a new touring show: no agent needed, bring a headshot and a CV, one minute '
                       'of speech. By seven in the morning the queue goes round the block, and the casting assistant '
                       'with the clipboard says they will see everyone, eventually.'),
                      ('W',
                       'There is a system: numbers at the door, groups of ten called in, one minute each and no '
                       'exceptions. {N} has a number, a folder and a bottle of water, and means to do it properly.'),
                      ('U',
                       '{N} has read the play they are casting and knows which parts are still open. One minute is '
                       'not long; it is enough for one true moment, if it is the right one.'),
                      ('B',
                       'The people in the queue are rivals, but they are also a list of who is working and who is '
                       "not. {N} notes the casting assistant's name on the lanyard and remembers it."),
                      ('R',
                       'Six hundred hopefuls and one minute each. {N} feels the old fire: this is the kind of door '
                       'that only opens for someone who kicks it.'),
                      ('G',
                       '{friend} from the local players came along for company, with sandwiches and a flask. '
                       'Whatever happens, they will have a story to take home.')],
            'tribal': [('',
                        "The keeper of the gathering's tellings sits on a rock above the summer camp and will hear "
                        'any player who comes before the great telling. Players from every band wait their turn in '
                        'the long grass.')],
            'magic': [('',
                       'A travelling company has drawn its wagons into a ring in the square, and its master will '
                       'hear anyone who wants to join: one piece, spoken from the tailboard of the first wagon, '
                       'before the whole market.')]},
 'outcomes': (['Days later word comes: they want {N}, or the day gives {N} exactly what {N} came for.',
               '{N} walks out into the evening knowing the minute went as well as it could.'],
              ['{N} waits nine hours, is seen for forty seconds, and never hears another word.',
               'The hearing stops at dusk with half the line still waiting, {N} among them.']),
 'options': [
    ('queue from six with headshot and CV, and give them exactly the speech they asked for', 'W1', None, 0.45, '', {'v': 'conformity', 'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': "wait your turn below the keeper's rock, and play the telling exactly as he asked", 'magic': 'wait your turn by the wagons, and give the master exactly the piece he asked for'}, 'chance': 0.04}),
    ('learn a speech from the very play they are casting, and know every line of it', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'learn a piece of the very telling the keeper means to play, and know every word of it', 'magic': "learn a piece from the company's own play, and know every line of it"}, 'chance': 0.05}),
    ('add "can ride a horse" to your CV, since the show has a horse in it', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'hid a wrong', 'closed': 'approval: a lie on the CV; backfire: the first rehearsal is on horseback, and the company lets the liar go', 'self_control': '-', 'world': {'tribal': 'tell the keeper you have danced the spear-dance at three gatherings, though you never have', 'magic': 'tell the master you can ride, since the play has a cavalry charge'}, 'chance': 0.05}),
    ('give them the rawest minute they will see all day, polish or no polish', 'R1', None, 0.45, '', {'v': 'stimulation', 'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': 'give the keeper the wildest telling he will see all summer', 'magic': 'give the master the wildest piece he will hear at the whole fair'}, 'chance': 0.05}),
    ('go with friends from the local players, and audition together for the ensemble', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'made a friend', 'world': {'tribal': 'go with the players of your own band, and ask to be the herd together', 'magic': 'go with your friends from the mystery players, and try for the crowd parts together'}, 'chance': 0.05}),
    ('wait all day for your slot, and keep your nerve when the queue is cut', 'W1', 'R.7', 0.5, '', {'v': 'conformity, stimulation', 'grants': 'auditioning', 'self_control': '+', 'world': {'tribal': 'wait below the rock from dawn to dusk for your turn, and keep your nerve', 'magic': 'wait the whole market day for your turn on the tailboard, and keep your nerve'}, 'chance': 0.85}),
    ('leave your details with the casting office for the next show, and go home', 'U1', 'G.7', 0.5, '', {'v': 'security, self-direction', 'grants': 'casting directory listing', 'world': {'tribal': 'ask the keeper to remember your name next summer, and walk home', 'magic': "leave your name on the company's roll for the next fair, and go home"}, 'chance': 0.84}),
    ('ask the casting assistant what an agent would want to see, and plan from there', 'B1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'aims': 'professional actor', 'self_control': '+', 'world': {'tribal': "ask the keeper's helper what the keeper looks for, and make a plan for next summer", 'magic': "ask the master's clerk what the company looks for, and plan from there"}, 'chance': 0.84}),
    ('leave the queue at noon, and spend the afternoon at a drop-in improvisation class', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'grants': 'improvisation', 'door': True, 'world': {'tribal': 'leave the waiting at noon, and spend the day making up tellings with the players by the stream', 'magic': 'leave the line at noon, and spend the afternoon playing without a book in the inn yard'}, 'chance': 0.84}),
    ('go home, and come back next year with a better speech and a proper headshot', 'G1', 'B.7', 0.5, '', {'v': 'security, achievement', 'self_control': '+', 'aims': 'professional actor', 'world': {'tribal': 'go home to your band, and come back next summer with a better telling', 'magic': 'go home, and come back to the next fair with a better piece'}, 'chance': 0.84}),
 ]},
{'name': 'the showcase for agents',
 'stages': 'young_adult adult',
 'age': (18, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'young_adult',
 'per_year': (0.0, 0.0, 0.3, 0.1, 0.0, 0.0),
 'drivers': 'prosper+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'mentor, friend, colleague, parent, rival',
 'requires': 'drama school student | drama school diploma',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': "the graduates' showcase in a studio theatre, an agent in every seat",
            'tribal': 'the apprentices play before the elders of every band at the gathering',
            'magic': "the guild school's final masque, with the brokers and the company masters in the gallery"},
 'timing': {'times': 'per final-year drama school student: once, in the last year; about 700 to 1,000 acting '
                     'graduates a year leave accredited UK schools, and most sign with an agent at or soon after the '
                     'showcase (estimate)',
            'likelier': 'the final year of the course, a good year for theatre and television, a showcase scene that '
                        'suits the student',
            'rarer': 'a student who left the course early, a lean year with few agents in the seats, a graduate long '
                     'out of school',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'Thirty graduates, two minutes each, and a hundred agents and casting directors in the dark '
                       'with their notebooks. {friend} is in the scene before {Ns}, and {mentor} is pacing at the '
                       'back of the room.'),
                      ('W',
                       '{N} has rehearsed the two minutes until every move is fixed. The scene belongs to the '
                       'partner in it as much as to {N}, and {N} means to play it that way.'),
                      ('U',
                       '{N} chose the speech for what it shows: range, stillness, and a turn in the middle that the '
                       'room will not see coming. Every second has been weighed.'),
                      ('B',
                       '{N} has the list of who is coming and knows which three agents matter. The rest of the room '
                       'is scenery.'),
                      ('R',
                       '{N} cannot feel {Ns} hands. The lights go down, the room goes quiet, and something inside '
                       'wants to burst out into the dark.'),
                      ('G',
                       '{Ns} family came down on the early train and sits at the back among the agents, in their '
                       'best coats, holding a programme with {Ns} name in it.')],
            'tribal': [('',
                        "At the gathering the old tellers' apprentices play in turn by the great fire, and the "
                        'elders of every band watch to see whom they will ask to winter with them.')],
            'magic': [('',
                       "The guild school's final masque is played in the long hall, and the brokers and company "
                       'masters lean over the gallery rail with their wax tablets.')]},
 'outcomes': (['An agent from the third row finds {N} at the drinks, and by the end of the month there is a contract '
               'and a first audition.',
               'The two minutes go as well as they ever went in rehearsal, and the next morning {Ns} phone holds '
               'three messages.'],
              ["Half the agents leave before the drinks, and {Ns} name is on nobody's list.",
               "{N} dries for a moment in the middle of the speech, and the room's attention drifts on to the next "
               'scene.']),
 'options': [
    ('play the scene exactly as rehearsed, for the partner and not for the room', 'W1', None, 0.45, '', {'title': 'professional actor', 'grants': 'an agent who believes in you', 'v': 'conformity', 'world': {'tribal': 'play the telling exactly as the old teller taught it, for the other player and not for the elders', 'magic': 'play the scene exactly as rehearsed, for the partner and not for the gallery'}, 'chance': 0.3}),
    ('choose the speech that shows a range no other graduate can show', 'U1', None, 0.45, '', {'title': 'professional actor', 'grants': 'an agent who believes in you', 'aims': 'professional actor', 'v': 'achievement', 'world': {'tribal': 'choose the telling that shows every voice the old teller gave you', 'magic': 'choose the speech that shows a range no other scholar can show'}, 'chance': 0.3}),
    ('stay at the drinks until the three agents who matter know the name', 'B1', None, 0.45, '', {'title': 'professional actor', 'grants': 'an agent who believes in you', 'v': 'power, achievement', 'world': {'tribal': "stay by the elders' fire until the three who matter know your name", 'magic': 'stay in the gallery until the three brokers who matter know your name'}, 'chance': 0.3}),
    ('drop the safe speech at the last minute, and play the one that burns', 'R1', None, 0.45, '', {'title': 'professional actor', 'grants': 'an agent who believes in you', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'drop the safe telling at the last moment, and play the one that burns'}, 'chance': 0.3}),
    ("skip the agents' drinks, and ask the theatre back home for a season", 'G1', None, 0.45, '', {'title': 'professional actor', 'aims': 'professional actor', 'mark': 'came home', 'v': 'tradition, security', 'world': {'tribal': 'go back to your own band, and ask to be its teller-player for the winter', 'magic': 'go back to your home city, and ask its playhouse for a season'}, 'chance': 0.3}),
    ('sign with the small agency from home that asks first, and look no further', 'B.5 G.5', None, 0.5, '', {'grants': 'an agent who believes in you', 'binds': True, 'v': 'security, power', 'world': {'tribal': 'take the go-between from your own band who asks first, and look no further', 'magic': 'sign with the first broker who asks, an old hand from your home city, and look no further'}, 'chance': 0.7}),
    ('skip the agents, and book a fringe slot with two classmates instead', 'B.5 R.5', None, 0.5, '', {'grants': 'a fringe slot', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': "skip the elders' fire, and take a place by the outer fires with two others", 'magic': 'skip the gallery, and hire a booth at the summer fair with two classmates'}, 'chance': 0.72}),
    ('promise the year group to keep making work together, whatever happens', 'U.5 G.5', None, 0.5, '', {'grants': 'a year group from drama school', 'binds': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'promise the others who learned beside you to keep telling together', 'magic': 'promise your year at the guild school to keep playing together'}, 'chance': 0.7}),
    ('say out loud to the school that the showcase favours students with money', 'W.5 R.5', None, 0.5, '', {'mark': 'defied an authority', 'identity': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'say out loud at the fire that the elders only ask for the sons and daughters of great hearths', 'magic': 'say out loud that the masque favours scholars with rich patrons'}, 'chance': 0.72}),
    ('ask the voice teacher to stay on as a mentor after the course ends', 'W.5 U.5', None, 0.5, '', {'grants': 'mentor', 'door': True, 'v': 'achievement, conformity', 'world': {'tribal': 'ask the old teller to keep guiding you after the three winters end', 'magic': 'ask the master of voice to keep teaching you after the seal is given'}, 'chance': 0.72}),
 ]},
{'name': 'cast as understudy to the lead',
 'stages': 'young_adult adult mature elder',
 'age': (17, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.08, 0.06, 0.03, 0.01),
 'drivers': 'prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, partner, rival',
 'requires': 'professional actor',
 'worlds': {'earth': 'a long-running musical needs a cover for the lead',
            'tribal': 'the elders want someone who can wear the great mask if its wearer falls',
            'magic': 'the court playhouse needs a second for its leading player for the winter season'},
 'timing': {'times': 'per professional actor a year: about 1 in 15 young actors are offered a cover; long runs cover '
                     'every lead, and about 1 professional actor in 3 understudies at some point (catalogue share; '
                     'estimate)',
            'likelier': 'a long run with a big cast, good years for the theatres, an actor who learns lines fast, a '
                        'director who has worked with the actor before',
            'rarer': 'a short run, a small company that cannot pay for covers, an actor known only for screen work, '
                     'old age',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'The casting office rings: the long-running musical needs a cover for the lead, with a place '
                       'in the ensemble, for a year. Eight shows a week at the back of the stage, and some nights, '
                       'perhaps, the front of it.'),
                      ('W',
                       'A cover is there so the show never stops. {N} thinks of the people who will have paid for '
                       'the lead and got the cover instead, and means to give them a night they will not regret.'),
                      ('U',
                       '{N} has seen the lead three times and has already noticed where the part could go deeper, if '
                       'anyone ever let it.'),
                      ('B',
                       'The biggest show in town, from the inside. {N} wonders who in the building decides what '
                       'comes next, and how to be in that room.'),
                      ('R',
                       'A year at the back of the chorus, waiting for someone else to fall ill? Part of {N} wants to '
                       'laugh, and part of {N} is already singing the big number in the kitchen.'),
                      ('G',
                       '{N} thinks of a whole year with one company: the same dressing room, the same walk to the '
                       'stage door, the same faces at the half. It could feel like home.')],
            'tribal': [('',
                        'The elders want someone who can wear the great mask if its wearer falls sick before the '
                        'summer gathering. They look round the fire, and their eyes stop on {N}.')],
            'magic': [('',
                       'The court playhouse needs a second for its leading player for the winter season: someone who '
                       'knows every line and waits in the wings every night, in case.')]},
 'outcomes': (['The casting office rings back within the week, and by Monday {N} is learning a part {N} may never '
               'get to play, and loving it.',
               'Whatever {N} decides, it is decided well, and the next year has a shape {N} can live with.'],
              ['The cover goes to someone who sings higher, and the casting office is kind about it.',
               'The choice sits badly for months, and {N} keeps wondering about the other road.']),
 'options': [
    ('say yes, and be word-perfect in the part before the first rehearsal', 'W1', None, 0.45, '', {'title': 'understudy', 'grants': 'learning lines', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': 'say yes, and know the great telling word for word before the next moon'}, 'chance': 0.3}),
    ("go to the recall with the lead's part worked out scene by scene", 'U1', None, 0.45, '', {'title': 'understudy', 'aims': 'lead actor or actress', 'v': 'achievement', 'world': {'tribal': 'come before the elders with the great telling learned by heart, every pause in its place', 'magic': 'come to the second trial with the leading part studied scene by scene'}, 'chance': 0.29}),
    ('take the cover, and get the producers to promise a look at the next lead', 'B1', None, 0.45, '', {'title': 'understudy', 'v': 'power, achievement', 'world': {'tribal': 'take the place, and get the elders to promise a look at the next great mask that falls free', 'magic': 'take the place, and get the play-merchant to promise a look at the next leading part'}, 'chance': 0.28}),
    ("sing the lead's big number at the audition as if it were opening night", 'R1', None, 0.45, '', {'title': 'understudy', 'body': 'light', 'v': 'stimulation, hedonism', 'world': {'tribal': "dance the ancestor's telling before the elders as if the gathering had already begun", 'magic': "sing the leading player's great song at the trial as if the court were watching"}, 'chance': 0.32}),
    ('take it, and settle into the company for the whole long run', 'G1', None, 0.45, '', {'title': 'understudy', 'v': 'security, tradition', 'world': {'tribal': "take it, and settle in among the band's tellers for the whole year", 'magic': 'take it, and settle into the court company for the whole winter'}, 'chance': 0.31}),
    ("turn it down for a part in a friend's new play above a pub", 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'self-direction, benevolence', 'world': {'tribal': "turn it down to play in a friend's new telling at the next fire", 'magic': "turn it down for a part in a friend's new piece at a tavern playhouse"}, 'chance': 0.72}),
    ('work out what a year of covering is worth against the screen work it blocks', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'work out what a year waiting for the mask is worth against the hunts it would cost', 'magic': 'work out what a season as second is worth against the glamour work it blocks'}, 'chance': 0.78}),
    ('learn the whole part in a week, just to see if it can be done', 'U.5 R.5', None, 0.5, '', {'grants': 'learning lines', 'self_control': '+', 'habit': True, 'v': 'stimulation, achievement', 'world': {'tribal': 'learn the whole great telling in seven nights, just to see if it can be done'}, 'chance': 0.72}),
    ('turn it down, to honour the contract already signed with a regional theatre', 'W.5 B.5', None, 0.5, '', {'mark': 'kept your word', 'v': 'conformity, security', 'world': {'tribal': 'turn it down, to keep the winter you promised another band', 'magic': 'turn it down, to honour the season already signed with a city playhouse'}, 'chance': 0.74}),
    ('turn it down, because a year away would be hard on the family', 'W.5 G.5', None, 0.5, '', {'mark': 'stayed home', 'v': 'benevolence, tradition', 'world': {'tribal': 'turn it down, because a year at the great fire would take you from your own hearth'}, 'chance': 0.74}),
 ]},
{'name': 'the understudy goes on',
 'stages': 'young_adult adult mature elder',
 'age': (17, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.4, 0.4, 0.4, 0.25),
 'drivers': 'fortune+.4',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, friend, partner, mentor',
 'requires': 'understudy',
 'worlds': {'earth': 'an announcement before the curtain: at this performance the part will be played by...',
            'tribal': 'the wearer of the great mask lies sick, and the mask is handed to you at dusk',
            'magic': "the leading player's carriage has overturned, and the herald cries your name instead"},
 'timing': {'times': 'per understudy of a year or more as a professional actor: about 2 in 5 go on at least once in '
                     'a run; about 1 in 5 who go on are kept on or given a lead soon after (estimate)',
            'likelier': 'a long run, a lead who is ill or injured, a heavy show eight times a week, winter colds in '
                        'the company',
            'rarer': 'a short run, a lead who never misses a show, a second cover ahead in the queue',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       "At four o'clock the company manager rings: the lead has lost a voice, and {N} is on tonight. "
                       'By the half the costume has been taken in, the announcement is written, and {partner} is '
                       'somewhere up in the circle.'),
                      ('W',
                       '{N} has done this part in an empty theatre every Thursday for months. Tonight it is for the '
                       'people who paid, and {N} owes them the show they came for.'),
                      ('U',
                       '{N} has watched every performance from the wings and knows where the lead rushes, where a '
                       'laugh is lost, and what could be done with the second act.'),
                      ('B',
                       'The producers will hear about tonight by morning. {N} has already made sure the agent knows, '
                       'and the casting director too.'),
                      ('R',
                       '{Ns} heart is going like a drum. This is it: the part {N} has sung in the shower for a year, '
                       'in front of a full house.'),
                      ('G',
                       'The company gathers in the wings before curtain up: the dressers, the stage manager, the old '
                       'hands from the chorus. They all want {N} to fly.')],
            'tribal': [('',
                        'The wearer of the great mask lies sick in his shelter, and at dusk the elders bring the '
                        'mask to {N}. The whole gathering waits by the fire.')],
            'magic': [('',
                       "The leading player's carriage has overturned on the bridge, and the herald steps out before "
                       'the curtain to cry {Ns} name instead. The court murmurs in the boxes.')]},
 'outcomes': (['The producers come round after the curtain, and by Friday {N} has the part for the rest of the run.',
               'The house stands at the end, and the company lines the corridor to cheer {N} back to the dressing '
               'room.'],
              ['The lead is back on Monday, and {N} goes back to the wings with one good night to remember.',
               'A missed cue in the second act throws a scene, and the notes the next day are polite and short.']),
 'options': [
    ('play it exactly as rehearsed, every move and every note', 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'grants': 'good notices', 'v': 'conformity', 'world': {'tribal': 'play the telling exactly as the elders set it, every step and every cry'}, 'chance': 0.2}),
    ('play it with the changes worked out over a year in the wings', 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'achievement, self-direction', 'world': {'tribal': 'play it with the changes worked out over a year of watching from behind the screens', 'magic': 'play it with the changes worked out over a season in the wings'}, 'chance': 0.2}),
    ('make sure the producers and the agent are in the house tonight', 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'aims': 'lead actor or actress', 'v': 'power, achievement', 'world': {'tribal': 'make sure the elders of every band are at the fire tonight', 'magic': 'make sure the patron and the broker are in the boxes tonight'}, 'chance': 0.2}),
    ('forget the blocking, and play it the way it has burned in you all year', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'forget the steps the elders set, and play it the way it has burned in you all year'}, 'chance': 0.21}),
    ('go on calmly, as if it were one more night in the long run', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'security, tradition', 'world': {'tribal': 'go out to the fire calmly, as if it were one more night of the winter tellings', 'magic': 'go on calmly, as if it were one more night of the season'}, 'chance': 0.2}),
    ('rest the voice all afternoon, and save it for the big number', 'B.5 G.5', None, 0.5, '', {'self_control': '+', 'v': 'security, achievement', 'world': {'tribal': "rest the voice all day, and save it for the ancestor's great cry", 'magic': 'rest the voice all afternoon, and save it for the great song'}, 'chance': 0.78}),
    ('throw in new business the director never approved, and see if it lands', 'B.5 R.5', None, 0.5, '', {'grants': 'improvisation', 'v': 'stimulation, power', 'world': {'tribal': 'throw in a new turn the elders never saw, and see if the gathering roars', 'magic': 'throw in a new piece of business the master never approved, and see if the court laughs'}, 'chance': 0.72}),
    ('have a large drink in the dressing room to steady the nerves', 'U.5 R.5', None, 0.5, '', {'self_control': '-', 'closed': 'approval: drinking before a show; backfire: the company manager smells it, and the producers never use the cover again', 'v': 'hedonism', 'world': {'tribal': 'drink the strong brew in the shelter to steady the nerves', 'magic': 'drink a large glass of wine in the tiring-room to steady the nerves'}, 'chance': 0.75}),
    ('hold the show together for the company, exactly as the director asked', 'W.5 G.5', None, 0.5, '', {'grants': 'a director who keeps casting you', 'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'hold the telling together for the other players, exactly as the shaper asked', 'magic': 'hold the play together for the company, exactly as the master of the play asked'}, 'chance': 0.72}),
    ('go in early, and run every scene with the stage manager before the half', 'W.5 U.5', None, 0.5, '', {'grants': 'reliable record', 'self_control': '+', 'habit': True, 'v': 'conformity, achievement', 'world': {'tribal': 'come to the fire early, and walk every step of the telling with the keeper of the fire', 'magic': 'come in early, and run every scene with the book-keeper before the bell'}, 'chance': 0.76}),
 ]},
{'name': 'the part of a lifetime is cast',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.015, 0.01, 0.006),
 'drivers': 'era+.2 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'friend, mentor, partner, rival, boss',
 'requires': 'professional actor | voice actor | understudy | amateur actor',
 'worlds': {'earth': "the casting call for a famous old play's great part, or a film that wants a face nobody knows",
            'tribal': 'the clans will tell the oldest story at the gathering, and every band sends a player for the '
                      'first ancestor',
            'magic': 'the court will stage the old epic of the realm, and the master of the play is looking '
                     'everywhere'},
 'timing': {'times': 'per professional or voice actor of two years or more, or amateur of five years or more with a '
                     'lead behind them, a year: about 1 in 50 young adults and fewer later try for a part that could '
                     'change their life; about 1 in 15 of those who try get it (estimate)',
            'likelier': 'a film that wants an unknown face, a famous old play revived with a new lead, a part '
                        "written for someone of the person's age and kind, a good agent",
            'rarer': 'a part already promised to a star, a life far from the cities where films are cast, no listing '
                     'in the casting directory',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The casting call is everywhere at once: a film of a famous old story wants a face nobody '
                       'knows for its great part, any age, any background, actors and non-actors alike. {friend} '
                       'sends the link to {N} with three exclamation marks.'),
                      ('W',
                       '{N} has loved this part since school and knows what it asks: years of discipline in one '
                       'performance. If it is to be done, it must be done properly.'),
                      ('U',
                       '{N} reads the call twice and then the old play itself, all night, looking for the person '
                       'inside the part.'),
                      ('B',
                       'Parts like this make careers, and they are cast through people. {N} starts working out who '
                       'knows the casting director.'),
                      ('R',
                       '{N} feels it the moment the call is read: this part, this person, now. Nothing has felt so '
                       'clear in years.'),
                      ('G',
                       'The part is an old farmer from a small place who never left the valley. {N} has known people '
                       'like that all {Ns} life.')],
            'tribal': [('',
                        'The clans will tell the oldest story at the gathering, and every band must send a player '
                        'for the first ancestor. At {Ns} fire the families look at one another, and then at {N}.')],
            'magic': [('',
                       'The court will stage the old epic of the realm, and the master of the play is said to be '
                       'looking in every tavern and every guild hall for a face the realm has never seen.')]},
 'outcomes': (['The casting director rings on a Thursday night, and {Ns} life divides into before and after.',
               'Whatever comes of the call, {N} meets it the way {N} chose, and is glad of it a year later.'],
              ['The part goes to someone else, as it nearly always does, and {N} reads the news like everyone else.',
               '{N} gets as far as the last six, and the call that comes is kind and short.']),
 'options': [
    ('prepare the audition for months, and arrive word-perfect on the day', 'W1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'casting directory listing', 'without': 'approval', 'lacking': 0.3, 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': "prepare the ancestor's telling for moons, and come to the elders word-perfect", 'magic': 'prepare the trial piece for months, and come before the master word-perfect'}, 'chance': 0.06}),
    ('read everything about the play and its first actors, and build the part from it', 'U1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'casting directory listing', 'without': 'approval', 'lacking': 0.3, 'v': 'achievement, self-direction', 'world': {'tribal': 'learn every way the oldest story has ever been told, and build the ancestor from them', 'magic': 'read every chronicle of the old epic and its first players, and build the part from them'}, 'chance': 0.06}),
    ('get the agent to put the name in front of the casting director first', 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'casting directory listing', 'without': 'approval', 'lacking': 0.3, 'aims': 'lead actor or actress', 'v': 'power', 'world': {'tribal': 'get the go-between to speak your name to the keeper of the tellings first', 'magic': 'get the broker to put your name before the master of the play first'}, 'chance': 0.06}),
    ('walk into the audition and play it straight from the heart, without a note', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'casting directory listing', 'without': 'approval', 'lacking': 0.3, 'v': 'stimulation, self-direction', 'world': {'tribal': 'walk up to the elders and play the ancestor straight from the heart', 'magic': 'walk into the trial and play it straight from the heart, without a note'}, 'chance': 0.06}),
    ('play it plain and true, as the old people of home would know it', 'G1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'casting directory listing', 'without': 'approval', 'lacking': 0.3, 'identity': True, 'v': 'tradition', 'world': {'tribal': 'play it plain and true, as the old ones of your band would know it', 'magic': 'play it plain and true, as the old folk of your village would know it'}, 'chance': 0.06}),
    ("claim on the form that you can ride, then learn on a cousin's farm", 'R.5 G.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: a lie on the casting form; backfire: the director asks to see the riding on the first day, and the part goes elsewhere', 'v': 'achievement, stimulation', 'world': {'tribal': 'tell the elders you can dance the bear dance, and learn it in half a moon from a cousin', 'magic': "swear to the master you can ride, and learn in a fortnight on a cousin's farm"}, 'chance': 0.8}),
    ('send a polished self-tape, and spend the waiting time on other auditions', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, security', 'world': {'tribal': 'show the elders your telling once, and spend the waiting on the winter hunts', 'magic': 'send a glamour-sketch of the scene, and spend the waiting on other trials'}, 'chance': 0.82}),
    ('go along for the day, and learn what you can from watching the others', 'U.5 G.5', None, 0.5, '', {'grants': 'auditioning', 'door': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'go to the gathering, and learn what you can from watching the other players', 'magic': 'go to the trial, and learn what you can from watching the other players'}, 'chance': 0.8}),
    ('withdraw, because the dates clash with a job already signed for', 'W.5 B.5', None, 0.5, '', {'mark': 'kept your word', 'v': 'conformity, security', 'world': {'tribal': 'step back, because the winter is promised to another band', 'magic': 'withdraw, because the dates clash with a season already signed'}, 'chance': 0.82}),
    ('help a friend prepare for it, and drive them to the open call', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence', 'world': {'tribal': "help a friend prepare the ancestor's telling, and walk with them to the gathering", 'magic': 'help a friend prepare the trial piece, and walk with them to the court'}, 'chance': 0.8}),
 ]},
{'name': 'a screen test',
 'stages': 'young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.04, 0.03, 0.02, 0.01),
 'drivers': 'era+.3 prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, mentor, colleague, partner, rival',
 'requires': 'professional actor | voice actor',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'a screen test for the lead in a new series',
            'tribal': 'the shaper of the shadow telling wants to see your shape against the wall',
            'magic': 'the illusionist wants to see if the glamour takes to your face'},
 'timing': {'times': 'per professional or voice actor of two years or more a year: about 1 in 25 young adults are '
                     'tested for a screen part; about 1 test in 10 becomes the lead (estimate)',
            'likelier': 'a boom in new series, an agent with screen contacts, a showreel, a face that suits the '
                        'part, years of work in front of a camera',
            'rarer': 'a lean year for television, a life far from where series are made, no showreel, an actor known '
                     'only for stage work',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'A studio on an industrial estate, a camera on a dolly, a director with a coffee, and two '
                       'scenes and a song to play with a reader who has done this forty times today. The lead in a '
                       'new series about a band on the road is still not cast.'),
                      ('W',
                       '{N} has learned both scenes until they are part of the furniture, and asks the camera '
                       'operator for the marks before anything else.'),
                      ('U',
                       '{N} knows that on screen less is more. The camera sees a thought before the face moves, and '
                       'the whole test is in the eyes.'),
                      ('B',
                       'The producers will watch the tape tonight with three others. {N} is thinking about how to be '
                       'the one they remember.'),
                      ('R',
                       'The camera is so close that {N} can see {Ns} own face in the lens. {N} wants to forget the '
                       'lens entirely and just be the person in the scene.'),
                      ('G',
                       '{N} found the character in someone from home: the way an uncle stood at the bar, the way an '
                       'old neighbour said goodbye.')],
            'tribal': [('',
                        'The shaper of the shadow telling has the fire built high behind the hide screen. {N} must '
                        'play the hunter in silhouette, and every small move is thrown huge across the cave wall.')],
            'magic': [('',
                       'The illusionist lays a glamour across {Ns} face to see if it takes: the audience must see '
                       'the hero in the air above the stage, as large as a house.')]},
 'outcomes': (['The producers watch the tape that night, and on Monday the agent rings with the word {N} has waited '
               'years to hear.',
               'Whatever the producers decide, {N} walks out of the studio knowing the camera saw something true.'],
              ['The part goes to an actor with a name, and the producers say they will keep {N} in mind.',
               'The tape is fine and nothing more, and {N} never hears back from the studio.']),
 'options': [
    ('learn both scenes perfectly, and hit every mark the crew gives', 'W1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants': 'a known face', 'v': 'conformity', 'world': {'tribal': "learn both scenes perfectly, and stand exactly where the shaper's fire throws the shadow", 'magic': 'learn both scenes perfectly, and stand exactly where the glamour is set'}, 'chance': 0.1}),
    ('play it small for the lens, and let the camera find the thought', 'U1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants': 'a known face', 'v': 'achievement', 'world': {'tribal': 'play it small for the wall, and let the fire find every gesture', 'magic': 'play it small for the glamour, and let the spell find the thought'}, 'chance': 0.1}),
    ('get the agent to bring the producers to the test, and play it to them', 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants': 'a known face', 'aims': 'lead actor or actress', 'v': 'power, achievement', 'world': {'tribal': 'get the go-between to bring the elders of the gathering, and play it to them', 'magic': 'get the broker to bring the patron to the trial, and play it to the patron'}, 'chance': 0.1}),
    ('ignore the notes, and play the scene the way it feels in the moment', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants': 'a known face', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': "ignore the shaper's signs, and play the hunt the way it feels in the moment"}, 'chance': 0.1}),
    ('give the part the walk and the voice of someone from home', 'G1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants': 'a known face', 'v': 'tradition', 'world': {'tribal': 'give the hunter the walk and the voice of an old hunter of your band', 'magic': 'give the hero the walk and the voice of someone from your village'}, 'chance': 0.1}),
    ('take the supporting part they offer instead, with a contract for the series', 'B.5 G.5', None, 0.5, '', {'grants': 'screen acting', 'binds': True, 'v': 'security, power', 'world': {'tribal': 'take the smaller shape they offer instead, for every shadow telling of the winter', 'magic': 'take the lesser part they offer instead, for the whole season of glamours'}, 'chance': 0.77}),
    ('turn it down, and go back to the small theatre where the work feels alive', 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'identity': True, 'v': 'self-direction, tradition', 'world': {'tribal': 'turn it down, and go back to the tellings at your own fire', 'magic': 'turn it down, and go back to the small playhouse where the work feels alive'}, 'chance': 0.75}),
    ("dub a better singer's voice under the song on the first self-tape", 'U.5 B.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: a dubbed self-tape; backfire: the producers ask for the song live at the test, and the part goes elsewhere', 'v': 'achievement, power', 'world': {'tribal': 'have a better singer hide behind the screen and sing while you mouth the words', 'magic': "have a better singer's voice laid under yours in the glamour-sketch"}, 'chance': 0.74}),
    ('ask the director straight out for notes, and take them like a professional', 'W.5 R.5', None, 0.5, '', {'grants': 'auditioning', 'v': 'achievement, conformity', 'world': {'tribal': 'ask the shaper straight out what was wrong, and take it without a word', 'magic': 'ask the illusionist straight out for notes, and take them like a professional'}, 'chance': 0.78}),
    ('practise the scenes in front of a camera every night with a coach', 'W.5 U.5', None, 0.5, '', {'grants': 'screen acting', 'self_control': '+', 'habit': True, 'v': 'achievement', 'world': {'tribal': 'practise the shapes in front of the fire every night with an old shadow-player', 'magic': 'practise the scenes in a scrying glass every night with an old player'}, 'chance': 0.76}),
 ]},
{'name': 'the leading player leaves the company',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.04, 0.05, 0.04, 0.02),
 'drivers': 'fortune+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, rival, partner',
 'requires': 'professional actor',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "the regional company's leading actor leaves for television",
            'tribal': "the band's teller who always wore the great mask goes to live with his wife's people",
            'magic': "the company's leading player is lured to the court playhouse"},
 'timing': {'times': 'per professional actor of two years or more in a company a year: about 1 in 25 see the '
                     "company's leading player leave in the middle of a season (estimate)",
            'likelier': 'a repertory or touring company with a fixed ensemble, a leading player courted by '
                        "television, years in the same company, a director who knows the actor's work",
            'rarer': 'freelance work from job to job, a company that casts its leads from outside, a first season in '
                     'the company',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       "The regional company's leading actor has taken a part in a television series and leaves at "
                       'the end of the month, half way through the season. Three plays still need their lead, and '
                       '{boss} calls the company together after the matinee.'),
                      ('W',
                       '{N} has played beside the leading part all season and knows it as well as {Ns} own. The '
                       'company needs the gap filled, and {N} could fill it.'),
                      ('U',
                       '{N} has thought for months about how the three parts could be played, and now the question '
                       'is no longer only in {Ns} head.'),
                      ('B',
                       "A leading part, a leading player's money, and the season's posters. {N} knows exactly what "
                       'this vacancy is worth, and to whom.'),
                      ('R',
                       '{N} wants it so badly that the matinee notes go past unheard. The bar after the show will '
                       'decide everything.'),
                      ('G',
                       '{N} came up through this company: the school tours, the holiday shows, the walk-on parts. '
                       'This is the place {N} belongs, if it will have {N} at the front.')],
            'tribal': [('',
                        "The teller who always wore the great mask has gone to live with his wife's people beyond "
                        'the river. The midsummer telling has no ancestor, and the shaper looks round the fire.')],
            'magic': [('',
                       "The company's leading player has been lured to the court playhouse by a noble patron. The "
                       'wagons leave for the next city in a week, and the master of the play needs a new lead before '
                       'the road.')]},
 'outcomes': (['By the first night of the next play the company has its new lead, and the matter is settled the way '
               '{N} hoped.',
               'The season goes on without a missed show, and {Ns} part in the change is remembered.'],
              ['The director brings in a name from outside, and the company learns to work with a stranger.',
               'The change goes badly, and by the end of the season {N} is looking for a new company.']),
 'options': [
    ('offer to step up, having stood beside the part all season', 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'conformity, achievement', 'world': {'tribal': 'offer to wear the mask, having danced beside it all winter', 'magic': 'offer to step up, having played beside the leading part all season'}, 'chance': 0.1}),
    ('ask the director for the part, with a plan for each of the three plays', 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'achievement', 'world': {'tribal': "ask the shaper for the mask, with a plan for each of the season's tellings", 'magic': 'ask the master for the part, with a plan for each of the three plays'}, 'chance': 0.1}),
    ("ask for the part, and for the leading player's money and dressing room", 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'aims': 'lead actor or actress', 'v': 'power, achievement', 'world': {'tribal': 'ask for the mask, and for the best share of the feast that goes with it', 'magic': "ask for the part, and for the leading player's purse and room at the inn"}, 'chance': 0.1}),
    ('tell the director in the bar that night that you want the part, and why', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'self-direction, stimulation', 'world': {'tribal': 'stand up at the fire that night and say you want the mask, and why', 'magic': 'tell the master in the tavern that night that you want the part, and why'}, 'chance': 0.1}),
    ('stay, and let the company that raised you see if you can carry it', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'stay, and let the band that raised you see if you can carry the mask'}, 'chance': 0.09}),
    ('leave too, and go back to the city to chase screen work', 'B.5 R.5', None, 0.5, '', {'grants': 'auditioning', 'mark': 'moved away', 'v': 'stimulation, power', 'world': {'tribal': 'leave too, and walk to the gathering to find a band that wants a teller', 'magic': 'leave too, and go to the capital to chase the glamour work'}, 'chance': 0.7}),
    ('let the director choose, and help whoever gets it learn the part', 'U.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'let the shaper choose, and help whoever gets the mask learn the telling', 'magic': 'let the master choose, and help whoever gets it learn the part'}, 'chance': 0.7}),
    ('put forward a brilliant friend from outside the company for the part', 'U.5 R.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence, stimulation', 'world': {'tribal': 'name a gifted friend from another band for the mask', 'magic': 'put forward a gifted friend from another company for the part'}, 'chance': 0.64}),
    ('stay on, for a written promise of the next lead that comes free', 'W.5 B.5', None, 0.5, '', {'binds': True, 'v': 'security, power', 'world': {'tribal': "stay, for the elders' promise of the next great mask that falls free", 'magic': 'stay on, for a sealed promise of the next leading part that comes free'}, 'chance': 0.66}),
    ('freeze out the outsider the director brings in for the part', 'W.5 G.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: freezing out a new actor; backfire: the director sees it, and the old hands are the ones not asked back', 'v': 'tradition, conformity', 'world': {'tribal': 'turn your backs on the stranger the shaper brings in for the mask', 'magic': 'freeze out the stranger the master brings in for the part'}, 'chance': 0.7}),
 ]},
{'name': 'opening night at the fringe',
 'stages': 'young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.8, 0.8, 0.8, 0.8),
 'drivers': 'fortune+.3 prosper+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'friend, partner, colleague, mentor, parent',
 'requires': 'a fringe slot',
 'worlds': {'earth': 'forty seats, a borrowed light, and a reviewer in the second row',
            'tribal': "the outer fires of the gathering, where anyone may play, and a chief's teller watching",
            'magic': 'a booth at the fair, a borrowed lamp, and a company master in the crowd'},
 'timing': {'times': 'per person with a fringe slot who is in work or on the rung below it (a professional or voice '
                     'actor, a drama student of a year or more, or an amateur or extra of two years or more): once a '
                     'festival; most fringe shows play to small houses, and about 1 in 10 is offered more; the '
                     'largest fringe festival had over 3,300 shows in 2024, most from small companies',
            'likelier': 'a festival that is going ahead, a show that is ready, a slot in the evening rather than at '
                        'noon',
            'rarer': 'a show cancelled for lack of money, a venue that closes, illness in a company of one',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       'Forty seats in a room above a bar, one borrowed light, and a reviewer in the second row with '
                       'a notebook on one knee. It is {Ns} own show, written in a back bedroom over a winter, and '
                       '{friend} is on the door taking the tickets.'),
                      ('W',
                       '{N} has run the show every evening for a month and knows exactly where it breathes. Whoever '
                       'comes tonight will get every word of it, as promised on the flyer.'),
                      ('U',
                       '{N} watches the audience as closely as they watch {N}: where they lean in, where they shift, '
                       'where the third scene still sags.'),
                      ('B',
                       'A reviewer, a producer from the capital and an agent are all said to be in town this week. '
                       '{N} has made sure each of them has a ticket.'),
                      ('R',
                       'This is the thing {N} made from nothing, with {Ns} own hands and {Ns} own nerve. Tonight it '
                       'lives or dies in front of strangers.'),
                      ('G',
                       '{Ns} family has driven up for the first night, and an aunt has brought a cake for after. '
                       'Whatever the reviewer says, they are proud.')],
            'tribal': [('',
                        'By the outer fires of the gathering, where anyone may play, {N} tells a telling of {Ns} own '
                        "making. A chief's teller from the far valley stands at the edge of the light, listening.")],
            'magic': [('',
                       'In a booth at the summer fair, under a borrowed lamp, {N} plays a piece of {Ns} own writing. '
                       'A company master in a good coat has stopped in the crowd to watch.')]},
 'outcomes': (["The reviewer's notice comes out on the third morning, and by the weekend the forty seats are full "
               'and a phone number is pinned to the dressing-room mirror.',
               'The run ends with a full house and a long night in the bar, and {N} knows the show was worth every '
               'penny of it.'],
              ["Most nights a dozen people come, and the reviewer's paper never prints a word.",
               'The offer that seemed close never arrives, and {N} packs the set into the car on the last night.']),
 'options': [
    ('play every night exactly as rehearsed, to whoever turns up', 'W1', None, 0.45, '', {'grants': 'a lead role to remember', 'habit': True, 'v': 'conformity, tradition', 'world': {'tribal': 'tell it every night exactly as made, to whoever sits down', 'magic': 'play every night exactly as rehearsed, to whoever stops at the booth'}, 'chance': 0.84}),
    ('rewrite the weak scene overnight after the first audience', 'U1', None, 0.45, '', {'grants': 'a lead role to remember; writing scripts', 'v': 'achievement, self-direction', 'world': {'tribal': 'remake the weak part of the telling overnight after the first night'}, 'chance': 0.84}),
    ('fill the house with free tickets, so the reviewer sees it full', 'B1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'power, achievement', 'world': {'tribal': "bring your own friends to every fire, so the chief's teller sees a crowd", 'magic': 'give away seats to fill the booth, so the company master sees a crowd'}, 'chance': 0.9}),
    ('play it flat out every night, as if each one were the last', 'R1', None, 0.45, '', {'grants': 'a lead role to remember', 'body': 'light', 'v': 'stimulation, hedonism', 'chance': 0.9}),
    ('keep the day job, and bring the show back next year, grown', 'G1', None, 0.45, '', {'grants': 'a lead role to remember', 'self_control': '+', 'v': 'security, tradition', 'world': {'tribal': 'keep to the hunt, and bring the telling back next summer, grown', 'magic': "keep the day's trade, and bring the play back to next year's fair, grown"}, 'chance': 0.88}),
    ('write to everyone who loved it, and build a following show by show', 'B.5 G.5', None, 0.5, '', {'grants': 'a cult following; a lead role to remember', 'grants_if_fails': 'a lead role to remember', 'v': 'power, benevolence', 'world': {'tribal': 'remember every face that came back twice, and send word to them each summer', 'magic': 'keep a roll of everyone who loved it, and write to them before every fair'}, 'chance': 0.15}),
    ("take the show home, and ask the town's theatre for a paid run", 'R.5 G.5', None, 0.5, '', {'title': 'professional actor', 'grants': 'a lead role to remember', 'grants_if_fails': 'a lead role to remember', 'mark': 'came home', 'v': 'tradition, stimulation', 'world': {'tribal': 'take the telling home, and ask your own band to keep you as its teller-player', 'magic': "take the play home, and ask the city's playhouse for a paid run"}, 'chance': 0.15}),
    ('rework the show with the producer who wants to move it to the capital', 'U.5 R.5', None, 0.5, '', {'title': 'professional actor', 'grants': 'a lead role to remember', 'grants_if_fails': 'a lead role to remember', 'aims': 'lead actor or actress', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': "remake the telling with the chief's teller, who wants it at the great fire", 'magic': 'rework the play with the company master, who wants it in the capital'}, 'chance': 0.1}),
    ('sign with the agent who came, and let the agent plan the next year', 'W.5 B.5', None, 0.5, '', {'title': 'professional actor', 'grants': 'a lead role to remember', 'grants_if_fails': 'a lead role to remember', 'binds': True, 'v': 'security, achievement', 'world': {'tribal': 'let the go-between who came speak for you to every band next winter', 'magic': 'sign with the broker who came, and let the broker plan the next year'}, 'chance': 0.12}),
    ('send every reviewer a careful note and a ticket for the second night', 'W.5 U.5', None, 0.5, '', {'grants': 'good notices; a lead role to remember', 'grants_if_fails': 'a lead role to remember', 'v': 'achievement, conformity', 'world': {'tribal': 'ask every elder at the gathering to come on the second night, and tell them why', 'magic': 'send every broadsheet a careful note and a seat for the second night'}, 'chance': 0.3}),
 ]},
{'name': 'the lead voice in a series',
 'stages': 'young_adult adult mature elder',
 'age': (17, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.08, 0.08, 0.06, 0.03),
 'drivers': 'era+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss, friend, partner, child',
 'requires': 'voice actor',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'the casting for the lead voice of an animated series',
            'tribal': 'the band wants a hidden voice for the first ancestor in every telling of the winter',
            'magic': "a puppet theatre wants its hero's voice for every show of the season"},
 'timing': {'times': 'per voice actor of two years or more a year: about 1 in 12 try for a lead voice; about 1 in 8 '
                     'who try get it (estimate)',
            'likelier': 'a boom in animated series and audio drama, an agent who knows the voice studios, a voice '
                        'with range, a good reel',
            'rarer': 'a lean year for commissions, a series cast with famous screen faces, a voice that sounds like '
                     'every other',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'An animated series for children has fifty-two episodes ordered, and the studio is casting '
                       'its hero. {N} stands in a small booth with headphones on, a drawing of the hero taped to the '
                       'glass, and three producers listening on the other side.'),
                      ('W',
                       '{N} has read every script the studio sent and marked each place where the hero changes. '
                       'Whatever the producers ask for, {N} will give them exactly that, take after take.'),
                      ('U',
                       '{N} has spent a week working out how the hero breathes: short and quick when frightened, '
                       'slow when sure. The voice is built from the inside out.'),
                      ('B',
                       '{Ns} agent says the producers have three voices on their list and money for one. {N} would '
                       'like to know what the other two are asking.'),
                      ('R',
                       'The hero is a fox who never stops talking. {N} has done the voice in the shower all week, '
                       'and the neighbours have started to knock on the wall.'),
                      ('G',
                       'Children all down {Ns} street will watch this, and {child} will too, perhaps. {N} wants a '
                       'voice a child would trust at bedtime.')],
            'tribal': [('',
                        'For every telling of the winter, the first ancestor needs a voice from behind the hide '
                        'wall, where no one sees who speaks. The elders have asked {N} to come and say a few lines '
                        'in the dark.')],
            'magic': [('',
                       'The puppet theatre by the river needs the voice of its hero, a wooden knight, for every show '
                       'of the season. {N} stands behind the curtain while the puppet master listens with his eyes '
                       'shut.')]},
 'outcomes': (['The studio rings on the Friday, and by the end of the year {Ns} voice is coming out of televisions '
               'in houses {N} will never see.',
               'Whatever {N} chose, it was chosen well, and the work that follows is work {N} is glad of.'],
              ['The lead goes to a voice the producers already knew, and {N} hears it on a trailer a month later.',
               "The series is cut back to a pilot, and the booth is booked for someone else's work by Monday."]),
 'options': [
    ('give three clean takes of every line, each just as the notes asked', 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'conformity', 'world': {'tribal': 'speak each line three times, each just as the elders asked', 'magic': 'give three clean readings of every line, each just as the puppet master asked'}, 'chance': 0.12}),
    ("build the hero's voice from the way the character breathes", 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'achievement, self-direction', 'world': {'tribal': "build the ancestor's voice from the way an old man breathes in the cold", 'magic': "build the knight's voice from the way a tired soldier breathes"}, 'chance': 0.12}),
    ('have the agent ring the producers first, and write repeat fees into the deal', 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'grants': 'repeat fees', 'aims': 'lead actor or actress', 'v': 'power, achievement', 'world': {'tribal': "send a go-between to the elders first, and ask for a share of every winter's gifts", 'magic': 'send the broker to the puppet master first, and ask for a fee for every show'}, 'chance': 0.12}),
    ('do the voice the way a child would, fearless, loud and never still', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'stimulation, hedonism', 'world': {'tribal': 'speak the ancestor the way a child would, fearless and loud', 'magic': 'do the knight the way a child would, fearless, loud and never still'}, 'chance': 0.13}),
    ('give the hero the warmth of a voice from back home', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'tradition, benevolence', 'world': {'tribal': "give the ancestor the warmth of your grandmother's voice", 'magic': 'give the knight the warmth of a voice from your home valley'}, 'chance': 0.12}),
    ("charm the producers at the studio's party, and come away with a contact", 'B.5 R.5', None, 0.5, '', {'grants': 'contact in the trade', 'v': 'power, stimulation', 'world': {'tribal': 'sit by the elders at the feast after, and come away with a friend among them', 'magic': 'charm the puppet master over wine after the trial, and come away with a friend in the trade'}, 'chance': 0.76}),
    ("take the second lead's voice, with repeat fees written into the contract", 'U.5 B.5', None, 0.5, '', {'grants': 'repeat fees', 'binds': True, 'v': 'achievement, power', 'world': {'tribal': "take the second ancestor's voice, with a share of every winter's gifts promised", 'magic': "take the voice of the knight's squire, with a fee for every show written down"}, 'chance': 0.74}),
    ('take a small voice in the series, and learn from the old hands', 'U.5 G.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': 'take a small voice in the tellings, and learn from the old voices behind the wall', 'magic': 'take a small voice in the season, and learn from the old hands behind the curtain'}, 'chance': 0.76}),
    ("turn it down, to finish the children's audiobooks already promised", 'W.5 G.5', None, 0.5, '', {'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'turn it down, to finish the tellings already promised to the children of the band', 'magic': 'turn it down, to finish the storybooks already promised to the printer'}, 'chance': 0.76}),
    ('turn it down, because the series is made to sell toys to small children', 'W.5 R.5', None, 0.5, '', {'identity': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'turn it down, because the elders want the ancestor to tell the children to obey them', 'magic': 'turn it down, because the guild made the show to sell toys to small children'}, 'chance': 0.75}),
 ]},
{'name': 'casting night at the local players',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.3, 0.3, 0.3, 0.3, 0.3),
 'drivers': 'community+.3 ties+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, performing',
 'horizon': 'months',
 'roles': 'friend, neighbour, partner, rival, elder',
 'requires': 'amateur actor',
 'worlds': {'earth': 'auditions in the church hall for the spring play',
            'tribal': 'the band chooses who will play the old stories at midwinter',
            'magic': "the guild's mystery players choose the parts for the feast-day pageant"},
 'timing': {'times': 'per amateur actor a year: about 1 in 3 audition for a lead; societies put on two to four shows '
                     'a year, and about 1 in 3 who try get the lead (estimate)',
            'likelier': 'a society with a full season, a play with a part that fits, a director new to the society, '
                        'a quiet year at work or at school',
            'rarer': 'a society short of money, a director who always casts the same few, exams, a long illness',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       'Auditions for the spring play are in the church hall on a wet Tuesday, with a tea urn, forty '
                       'plastic chairs and the director at a trestle table. Everyone reads for something. Only one '
                       'person will get the lead.'),
                      ('W',
                       '{N} has been with the players for years and knows how a casting night should go: everyone '
                       'gets a fair hearing, and everyone takes the part they are given.'),
                      ('U',
                       '{N} has read the play twice and thinks the lead is usually played wrong. The trick is to '
                       'show the director why in two minutes.'),
                      ('B',
                       '{N} knows the director wants a name the town will come out for, and knows exactly who in the '
                       'room can sell tickets.'),
                      ('R',
                       '{Ns} hands are shaking. Being on stage is the most alive {N} feels all year, and tonight is '
                       'the door to it.'),
                      ('G',
                       "{N} grew up watching these players, sitting on a parent's knee in the third row. {friend} is "
                       'here too, and so is half the street.')],
            'tribal': [('',
                        'At the turn of the year, the band gathers to choose who will play the old stories at '
                        'midwinter. The elder who shapes the tellings sits by the fire and listens to each voice in '
                        'turn.')],
            'magic': [('',
                       "The guild's mystery players meet in the hall above the bakery to choose the parts for the "
                       'feast-day pageant. The pageant master writes each name on a slate.')]},
 'outcomes': (['The cast list goes up on the church hall door on Friday, and {Ns} name is on it where {N} hoped it '
               'would be.',
               'Rehearsals start in the new year, and by the first night the whole company knows {N} was the right '
               'choice.'],
              ['The lead goes to someone the director has worked with before, and {N} reads the cast list twice to '
               'be sure.',
               'The director says it was close, which helps a little, on the walk home in the rain.']),
 'options': [
    ('come word-perfect in the speech, read as the director set it', 'W1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'conformity', 'world': {'tribal': 'come knowing the old story word for word, told as the elder set it', 'magic': 'come word-perfect in the speech, read as the pageant master set it'}, 'chance': 0.3}),
    ('give a reading of the part that nobody in the hall expected', 'U1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'self-direction, achievement', 'world': {'tribal': 'tell the old story in a way nobody at the fire expected'}, 'chance': 0.3}),
    ('make the plain case to the director for being cast in the lead', 'B1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'power, achievement', 'world': {'tribal': 'make the plain case to the elder for telling the great story', 'magic': 'make the plain case to the pageant master for being cast in the lead'}, 'chance': 0.3}),
    ('walk off the nerves outside, then come in and give it everything', 'R1', None, 0.45, '', {'grants': 'a lead role to remember', 'self_control': '+', 'v': 'stimulation, hedonism', 'chance': 0.3}),
    ('try for the lead again, as every spring, with half the street watching', 'G1', None, 0.45, '', {'grants': 'a lead role to remember', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'try to tell the great story again, as every midwinter, with the whole band watching'}, 'chance': 0.3}),
    ('take the part offered, and save your strength for the summer show', 'B.5 G.5', None, 0.5, '', {'self_control': '+', 'v': 'security, power', 'world': {'tribal': 'take the story offered, and save your voice for the summer gathering', 'magic': 'take the part offered, and save your strength for the midsummer fair'}, 'chance': 0.8}),
    ('offer to stage manage instead, and learn how a show is really run', 'U.5 B.5', None, 0.5, '', {'grants': 'stagecraft', 'door': True, 'v': 'achievement, power', 'world': {'tribal': 'offer to keep the fire and the masks instead, and learn how a telling is really run', 'magic': 'offer to run the pageant cart instead, and learn how a show is really put on'}, 'chance': 0.8}),
    ("write a short new play for the society's one-act evening", 'U.5 R.5', None, 0.5, '', {'grants': 'writing scripts', 'identity': True, 'v': 'self-direction, stimulation', 'world': {'tribal': "make a short new telling for the children's fire", 'magic': "write a short new piece for the guild's winter evening"}, 'chance': 0.8}),
    ('take the small part gladly, and help paint the set on Sundays', 'W.5 G.5', None, 0.5, '', {'grants': 'a company that feels like family', 'v': 'benevolence, conformity', 'world': {'tribal': 'take the small part gladly, and help stitch the masks on the rest days', 'magic': 'take the small part gladly, and help paint the pageant cart on feast days'}, 'chance': 0.8}),
    ('stand back, so a newer member can have a first lead', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'universalism, benevolence', 'world': {'tribal': 'stand back, so a younger teller can have a first great story', 'magic': 'stand back, so a new player can have a first lead'}, 'chance': 0.8}),
 ]},
{'name': 'the summer show casts its lead',
 'stages': 'child juvenile',
 'age': (6, 17),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.3, 0.3, 0.0, 0.0, 0.0, 0.0),
 'drivers': 'community+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, performing, play',
 'horizon': 'months',
 'roles': 'friend, parent, sibling, rival',
 'requires': 'youth theatre member',
 'worlds': {'earth': "the youth theatre's summer show, and the list on the noticeboard",
            'tribal': "the children's telling at midsummer, and who will play the hare",
            'magic': "the children's company's summer masque"},
 'timing': {'times': 'per youth theatre member: once a year, at the summer show (estimate)',
            'likelier': 'a youth theatre with a summer show, a show with a part that fits, a child who has been '
                        'coming for a year or more',
            'rarer': 'a summer show cancelled for lack of money or of a hall, a family holiday over the show week, '
                     'exams',
            'gap_years': (1.0, 1.0)},
 'scenes': {'earth': [('',
                       "The youth theatre's summer show is a musical about a ship of runaway animals, and the leader "
                       'is hearing everyone for the parts in the big hall on Saturday morning, the whole group '
                       'sitting in a ring on the floor. The cast list goes up on the noticeboard next week.'),
                      ('W',
                       '{N} has learned the audition song exactly as it was taught and practised it every evening in '
                       'the bedroom, to the wardrobe mirror.'),
                      ('U',
                       '{N} has read the whole script and has ideas about the captain: she is brave on the outside '
                       'and frightened on the inside, which is the interesting bit.'),
                      ('B',
                       '{N} has worked out who else is going for the captain and how many lines each part has, and '
                       'has a plan.'),
                      ('R',
                       '{N} cannot sit still in the ring. Being the captain would be the best thing that has ever '
                       'happened, ever.'),
                      ('G',
                       '{friend} is going for the parrot, and {N} would quite like the two of them to be on stage '
                       'together. {parent} has already booked the time off work for the show.')],
            'tribal': [('',
                        'At midsummer the children tell a telling of their own at the edge of the great fire, and '
                        'someone must be the hare. The old woman who teaches them the tellings listens to each child '
                        'in turn, with the whole group in a ring.')],
            'magic': [('',
                       "The children's company puts on a masque for the summer fair, and the masque mistress hears "
                       'each child in the guild hall with the whole company sitting round. The list of parts goes up '
                       'on the hall door.')]},
 'outcomes': (['The list goes up on the noticeboard on Friday, and {N} reads it four times and then runs to find '
               '{friend}.',
               'On the night, {Ns} family is in the second row, and {N} does not miss a single cue.'],
              ['The captain goes to an older girl who has been coming for three years, and {N} is a deckhand with '
               'two lines.',
               '{N} forgets the second verse in the audition, and has to be told by {parent} in the car that it does '
               'not matter.']),
 'options': [
    ('learn the song exactly as taught, and sing it just like that', 'W1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'conformity, tradition', 'world': {'tribal': "learn the hare's song exactly as taught, and sing it just like that"}, 'chance': 0.25}),
    ('ask the leader what the part needs, and work on just that', 'U1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'self-direction, achievement', 'world': {'tribal': 'ask the old woman what the hare needs, and work on just that', 'magic': 'ask the masque mistress what the part needs, and work on just that'}, 'chance': 0.25}),
    ('go last, after watching what the leader liked in the others', 'B1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'power, achievement', 'world': {'tribal': 'go last, after watching what the old woman liked in the others', 'magic': 'go last, after watching what the masque mistress liked in the others'}, 'chance': 0.25}),
    ('sing the loudest song and finish with a cartwheel', 'R1', None, 0.45, '', {'grants': 'a lead role to remember', 'body': 'light', 'v': 'stimulation, hedonism', 'world': {'tribal': "sing the hare's song loudest, and finish with a leap over the log"}, 'chance': 0.25}),
    ('audition alongside a best friend, so neither goes up alone', 'G1', None, 0.45, '', {'grants': 'a lead role to remember', 'v': 'benevolence, tradition', 'chance': 0.25}),
    ('go for the villain as well, and play it big and nasty', 'B.5 R.5', None, 0.5, '', {'grants': 'auditioning', 'v': 'power, stimulation', 'world': {'tribal': 'go for the fox as well, and play it big and sly', 'magic': 'go for the wicked steward as well, and play it big and nasty'}, 'chance': 0.8}),
    ('promise the friends from the bus to do the chorus together', 'R.5 G.5', None, 0.5, '', {'binds': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'promise the friends from the camp to dance the chorus together'}, 'chance': 0.8}),
    ('help the leader teach the songs to the youngest ones', 'U.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'self_control': '+', 'v': 'benevolence, achievement', 'world': {'tribal': 'help the old woman teach the songs to the smallest children', 'magic': 'help the masque mistress teach the songs to the youngest ones'}, 'chance': 0.8}),
    ('tell the leader which of the others messed about in the warm-up', 'W.5 B.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: telling tales on the others; backfire: the others find out, and nobody sits with {N} at the break', 'v': 'conformity, power', 'world': {'tribal': 'tell the old woman which of the others played about in the warm-up', 'magic': 'tell the masque mistress which of the others messed about in the warm-up'}, 'chance': 0.8}),
    ('stay out of the show this year, to keep up with school', 'W.5 U.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'conformity, achievement', 'world': {'tribal': 'stay out of the telling this year, to keep learning the snares with the hunters', 'magic': 'stay out of the masque this year, to keep up with lessons'}, 'chance': 0.8}),
 ]},
{'name': 'a casting call for children',
 'stages': 'child juvenile',
 'age': (7, 15),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.03, 0.03, 0.0, 0.0, 0.0, 0.0),
 'drivers': 'family+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'performing, family, school',
 'horizon': 'months',
 'roles': 'parent, sibling, friend, rival',
 'requires': 'youth theatre member | a lead role to remember',
 'worlds': {'earth': "a touring musical's open call for children, with a chaperone at every rehearsal",
            'tribal': "the gathering's keeper of tellings wants a child for the spirit of the spring, with the "
                      'mother beside her',
            'magic': "the court playhouse wants a child for the prince, with the guild's licence and a chaperone"},
 'timing': {'times': 'per child in a youth theatre or with a lead behind them a year: about 1 in 30 meet a '
                     'professional casting for children; over 90,000 child performance licences are issued a year in '
                     'England, many for the same child (an estimate from a third of local authorities, 2014)',
            'likelier': 'a touring show or a film shooting nearby, a youth theatre leader who passes the word on, a '
                        'family with the time to drive and to chaperone',
            'rarer': 'a family that cannot take the days off, a school that will not agree to the days out, a long '
                     'way from the city',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'A touring musical is holding an open call for children in the city, for the parts of the '
                       'orphans and one lead. Every child who is cast needs a licence from the council, a licensed '
                       'chaperone at every rehearsal and show, and three hours of lessons on any day away from '
                       'school. The form is on the kitchen table, and {parent} has read it twice.'),
                      ('W',
                       '{N} wants to do it properly: the form filled in, the school asked, the chaperone found, and '
                       'the song learned exactly as the sheet music says.'),
                      ('U',
                       '{N} has watched a recording of the show and wonders what the panel will be listening for. '
                       "The lead's song has a hard bit in the middle that nobody at the youth theatre can sing yet."),
                      ('B',
                       'Children from three counties will be in that queue. {N} wants to know how they choose, and '
                       'how to be the one they remember.'),
                      ('R',
                       'A real stage, a real orchestra and a real audience, every night for months. {N} has been '
                       'singing in the bath since the youth theatre leader mentioned it.'),
                      ('G',
                       '{parent} says it is a family decision, and it is: the long drives, the days away, a little '
                       'brother who will miss his lifts to football. {N} wants everyone to be all right with it.')],
            'tribal': [('',
                        'At the spring gathering, the keeper of tellings wants a child to play the spirit of the '
                        "spring, a child who will walk out of the river mist at dawn. The child's mother or father "
                        "must stand beside the river through every telling, and the child's own lessons with the "
                        'hunters must go on.')],
            'magic': [('',
                       'The court playhouse wants a child to play the young prince for the winter season. The guild '
                       "grants a licence for each child, a guild chaperone sits in every rehearsal, and the child's "
                       'lessons must be kept each morning.')]},
 'outcomes': (['A letter comes from the casting team in the spring, and {parent} reads it out at the kitchen table '
               'twice, the second time more slowly.',
               "The council's licence comes through, the chaperone is a kind woman who knits, and the youth theatre "
               'leader comes to the first night.'],
              ['The queue goes round the block, and the panel hears {N} for forty seconds. No letter comes, and the '
               "youth theatre's own show is in July.",
               'The school will not agree to the days away this year, and {parent} says there will be other calls.']),
 'options': [
    ('go with the forms signed, the school asked and a chaperone booked', 'W1', None, 0.45, '', {'grants': 'child performance licence; a lead role to remember', 'v': 'conformity, security', 'world': {'tribal': "go with the mother's word given, and the hunters told of the days away", 'magic': "go with the guild's forms signed, the tutor told and a chaperone booked"}, 'chance': 0.13}),
    ("learn the lead's hard song first, in the youth theatre's extra class", 'U1', None, 0.45, '', {'grants': 'child performance licence; a lead role to remember', 'v': 'achievement, self-direction', 'world': {'tribal': "learn the spirit's song first, from the oldest singer in the band", 'magic': "learn the prince's hard song first, in the children's company's extra class"}, 'chance': 0.13}),
    ('ask the youth theatre leader what this panel looks for', 'B1', None, 0.45, '', {'grants': 'child performance licence; a lead role to remember', 'v': 'achievement, power', 'world': {'tribal': 'ask the old woman who teaches the tellings what the keeper looks for', 'magic': "ask the masque mistress what the court's players look for"}, 'chance': 0.13}),
    ('sing loud and bright at the open call, and enjoy every minute of it', 'R1', None, 0.45, '', {'grants': 'child performance licence; a lead role to remember', 'v': 'stimulation, hedonism', 'world': {'tribal': 'sing loud and bright at the river, and enjoy every minute of it'}, 'chance': 0.13}),
    ('go with a parent beside all day, as the family agreed', 'G1', None, 0.45, '', {'grants': 'child performance licence; a lead role to remember', 'v': 'benevolence, tradition', 'chance': 0.13}),
    ("try for the orphans' ensemble, with two friends from the youth theatre", 'B.5 G.5', None, 0.5, '', {'grants': 'child performance licence', 'v': 'benevolence, achievement', 'world': {'tribal': 'try for the children of the mist, with two friends from the band', 'magic': "try for the prince's pages, with two friends from the children's company"}, 'chance': 0.37}),
    ('keep to school this year, as the parents ask, and take the extra class', 'U.5 G.5', None, 0.5, '', {'grants': 'acting', 'v': 'security, achievement', 'world': {'tribal': "keep to the hunters' lessons this year, as the parents ask, and learn the tellings at home", 'magic': 'keep to the tutor this year, as the parents ask, and take the extra class'}, 'chance': 0.38}),
    ('go along for the experience of a real audition, and see what happens', 'U.5 R.5', None, 0.5, '', {'grants': 'auditioning', 'v': 'stimulation, self-direction', 'world': {'tribal': 'go to the river for the experience of being heard, and see what happens'}, 'chance': 0.37}),
    ('try for the ensemble, where many more children are taken', 'W.5 B.5', None, 0.5, '', {'grants': 'child performance licence', 'v': 'security, achievement', 'world': {'tribal': 'try for the children of the mist, where many more are taken', 'magic': 'try for the pages, where many more children are taken'}, 'chance': 0.37}),
    ('ask for weekend shows only, so school days stay free', 'W.5 R.5', None, 0.5, '', {'grants': 'child performance licence', 'v': 'conformity, stimulation', 'world': {'tribal': 'ask to walk only at the full-moon tellings, so the hunting days stay free', 'magic': 'ask for feast-day shows only, so lesson days stay free'}, 'chance': 0.37}),
 ]},
{'name': 'the director calls again',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.15, 0.15, 0.12, 0.08),
 'drivers': 'ties+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, partner, rival',
 'requires': 'a director who keeps casting you',
 'worlds': {'earth': 'a director who has cast the actor twice rings about a new production',
            'tribal': 'the shaper of the tellings sends a runner: he wants the same teller again for midsummer',
            'magic': 'the master of the play sends a letter: a new piece, and he wants the same player'},
 'timing': {'times': 'per working actor (professional or voice) of two years or more with a director who keeps '
                     'casting them a year: about 1 in 7 are called again; directors recast actors they trust '
                     '(estimate)',
            'likelier': 'a director with a new production funded, a part that fits, an actor who was good in the '
                        'last one and easy in the room',
            'rarer': 'a director between jobs, a falling-out on the last production, an actor tied up in a long run',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The director who has cast {N} twice rings on a Sunday evening. There is a new production for '
                       'the spring, a play nobody has done for forty years, and a part in it the director has been '
                       'thinking about for {N}. It might be the lead. It might be the brother.'),
                      ('W',
                       'Two productions with this director, and both times {N} was on time, knew the lines and kept '
                       'the company steady. {N} would like to keep that trust.'),
                      ('U',
                       '{N} has read the play overnight. The lead is the part with something new in it, a man who '
                       'changes his mind in the third act, and {N} can see exactly how to do it.'),
                      ('B',
                       "The director is good, and getting known. Being the director's lead in this one could lift "
                       '{N} a long way, if the billing is right.'),
                      ('R',
                       'A new play, a director who trusts {N}, and three months of rehearsal in a cold room. {N} '
                       'wants to say yes before the call is over.'),
                      ('G',
                       "This director's company is the nearest thing {N} has to a second family: the same stage "
                       'manager, the same designer, the same jokes at the tea break.')],
            'tribal': [('',
                        'A runner comes up the valley with word from the shaper of the tellings: there is a new '
                        'telling for midsummer, and he wants {N} again. Perhaps for the great part. Perhaps for the '
                        'brother.')],
            'magic': [('',
                       "A letter with the master of the play's seal arrives: a new piece for the spring, and he "
                       'wants {N} again. The part is not named, but there is a hint of the lead.')]},
 'outcomes': (['The director rings back within the week, and by the first read-through {N} knows the part was the '
               'right one to take.',
               'Whatever {N} chose, the director understands it, and the next call comes in its own good time.'],
              ['The lead goes to a famous face the producers wanted, and the director is sorry about it on the '
               'phone.',
               'The production loses its money in the winter, and the play nobody has done for forty years waits a '
               'little longer.']),
 'options': [
    ('say yes at once, and be the steadiest player in the company again', 'W1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'v': 'conformity, security', 'world': {'tribal': 'send the runner back with a yes, and be the steadiest teller at the fire again', 'magic': 'send word back with a yes, and be the steadiest player in the company again'}, 'chance': 0.12}),
    ('ask to read for the lead, with the whole play worked through', 'U1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'aims': 'lead actor or actress', 'v': 'achievement, self-direction', 'world': {'tribal': 'ask to try the great part, with the whole telling worked through', 'magic': 'ask to read for the lead, with the whole piece worked through'}, 'chance': 0.12}),
    ('have the agent ask for the lead and top billing on the posters', 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'v': 'power, achievement', 'world': {'tribal': 'send a go-between to ask for the great part, and the first place at the feast', 'magic': 'have the broker ask for the lead, and the top line on the playbill'}, 'chance': 0.12}),
    ('say yes on the phone before even hearing which part it is', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'v': 'stimulation', 'world': {'tribal': 'say yes to the runner before even hearing which part it is', 'magic': 'say yes by return before even hearing which part it is'}, 'chance': 0.12}),
    ("go back to the director's company, the old team together again", 'G1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'v': 'tradition, benevolence', 'world': {'tribal': "go back to the shaper's fire, the old tellers together again", 'magic': "go back to the master's company, the old players together again"}, 'chance': 0.12}),
    ('walk out of the current run two weeks early, to be free for it', 'B.5 R.5', None, 0.5, '', {'mark': 'broke your word', 'closed': 'approval: leaving a run early; backfire: the producer of the old run tells everyone, and two casting offices stop calling', 'v': 'power, stimulation', 'world': {'tribal': 'leave the band you promised the winter to, two moons early, to be free for it', 'magic': 'walk out of the current season two weeks early, to be free for it'}, 'chance': 0.76}),
    ("turn it down for a friend's new devised show with no money in it", 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'door': True, 'v': 'self-direction, benevolence', 'world': {'tribal': 'turn it down to make a new telling with a friend at the small fires', 'magic': "turn it down for a friend's new piece at a tavern playhouse"}, 'chance': 0.76}),
    ('take the brother for top billing and a better fee', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "take the brother's part for a better place at the feast and more gifts", 'magic': "take the brother's part for the top line on the playbill and a better fee"}, 'chance': 0.76}),
    ('take the brother gladly, for the sake of the company', 'W.5 G.5', None, 0.5, '', {'grants': 'a company that feels like family', 'v': 'benevolence, conformity', 'world': {'tribal': "take the brother's part gladly, for the sake of the old tellers", 'magic': "take the brother's part gladly, for the sake of the old company"}, 'chance': 0.76}),
    ("take the brother, and learn the lead's part too, just in case", 'W.5 U.5', None, 0.5, '', {'grants': 'learning lines', 'v': 'achievement, conformity', 'world': {'tribal': "take the brother's part, and learn the great part too, just in case", 'magic': "take the brother's part, and learn the lead too, just in case"}, 'chance': 0.76}),
 ]},
{'name': 'a voice for the cartoon',
 'stages': 'young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.03, 0.02, 0.01),
 'drivers': 'era+.2 prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, performing',
 'horizon': 'months',
 'roles': 'friend, colleague, partner, child, boss',
 'requires': 'professional actor | amateur actor | community-radio presenter',
 'worlds': {'earth': "a children's cartoon needs voices, and a friend passes the person's name on",
            'tribal': 'the band needs hidden voices for the animals in the winter tellings',
            'magic': 'a puppet theatre needs voices for its dragon and its talking cat'},
 'timing': {'times': 'per professional actor of a year or more, or amateur actor or community-radio presenter of two '
                     'years or more with accents and voices, a year: about 1 in 33 hear of voice work they could try '
                     'for (estimate); about 1 life in 2,000 voices for a living (catalogue share; estimate)',
            'likelier': 'a boom in cartoons, audiobooks and games, a friend already in the trade, a voice with '
                        'range, a home that can be made quiet enough to record in',
            'rarer': 'a lean year for commissions, no studio within reach, a voice that only does one thing',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "A friend who works in a sound studio rings: a children's cartoon needs voices for a dragon, "
                       'a grandmother and a cat who thinks she is a dog, and the casting session is on Thursday. {N} '
                       'has done funny voices for years, at parties and at bedtime. This would be the first time '
                       'anyone paid for one.'),
                      ('W',
                       '{N} has asked the friend for the test scripts, printed them, and read each one aloud until '
                       'it comes out clean every time.'),
                      ('U',
                       '{N} has been listening to cartoons with the picture off, working out how the best voice '
                       'actors do it: the breath before the joke, the voice that smiles.'),
                      ('B',
                       'A cartoon that sells abroad can run for years. {N} wonders who the friend knows at the '
                       'studio, and who decides.'),
                      ('R',
                       'A dragon! {N} has been roaring in the car all week, and once at the traffic lights, with the '
                       'window down.'),
                      ('G',
                       '{child} laughs hardest at {Ns} grandmother voice, the one borrowed from the old women in the '
                       'market. It would be nice if other children heard it too.')],
            'tribal': [('',
                        'In the long dark of winter the tellings need hidden voices for the animals: the bear, the '
                        'raven, the old hare. Someone has told the elders that {N} can do the raven better than a '
                        'raven.')],
            'magic': [('',
                       'The puppet theatre by the bridge needs voices for its dragon and its talking cat for the '
                       'winter season. A friend who paints its scenery has told the puppet master about {N}.')]},
 'outcomes': (['The studio rings on the Friday, and by the spring {Ns} grandmother voice is on television on '
               'Saturday mornings, and {child} tells everyone at school.',
               'Whatever {N} chose, it was the right size of step, and the voice work is there for when it is '
               'wanted.'],
              ['The studio already had a dragon, and the friend says the session went well, which is what friends '
               'say.',
               'The cartoon is cancelled before the first episode is drawn, and {N} goes back to doing the voices at '
               'bedtime.']),
 'options': [
    ('read the test script exactly as written, every line clean', 'W1', None, 0.45, '', {'title': 'voice actor', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity', 'world': {'tribal': "speak the raven's lines exactly as the elders taught them, every one clean", 'magic': "read the puppet master's lines exactly as written, every one clean"}, 'chance': 0.03}),
    ('work out a different voice for each character before the session', 'U1', None, 0.45, '', {'title': 'voice actor', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'work out a different voice for each animal before the tellings', 'magic': 'work out a different voice for each puppet before the trial'}, 'chance': 0.03}),
    ('ring the studio every Monday after, until a part comes up', 'B1', None, 0.45, '', {'title': 'voice actor', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'power, achievement', 'world': {'tribal': "go to the elders' fire every evening after, until a voice is wanted", 'magic': 'call at the puppet theatre every market day after, until a voice is wanted'}, 'chance': 0.03}),
    ('give the dragon everything, roar and all', 'R1', None, 0.45, '', {'title': 'voice actor', 'grants_if_fails': 'a long shot that missed', 'aims': 'lead actor or actress', 'v': 'stimulation, hedonism', 'world': {'tribal': 'give the bear everything, roar and all'}, 'chance': 0.03}),
    ('voice the grandmother just as the old women in the market talk', 'G1', None, 0.45, '', {'title': 'voice actor', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, benevolence', 'world': {'tribal': 'voice the old hare just as the grandmothers at the fire talk', 'magic': 'voice the cat just as the old women in the market talk'}, 'chance': 0.03}),
    ('practise a new voice every night for a month, recording each one', 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'accents and voices', 'habit': True, 'v': 'achievement, stimulation', 'world': {'tribal': "practise a new animal's voice every night for a moon, until the children guess it", 'magic': 'practise a new voice every night for a month, until the neighbours guess it'}, 'chance': 0.74}),
    ("make a careful voice reel at a friend's little studio", 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'a showreel', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'achievement, security', 'world': {'tribal': 'learn a voice for every animal in the tellings, so the elders can hear them all', 'magic': 'make a careful voice book of every voice, to send to the playhouses'}, 'chance': 0.75}),
    ("offer a day's free work at the studio, to get a foot in the door", 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'power, stimulation', 'world': {'tribal': 'offer to fetch wood for the tellings all winter, to sit near the elders', 'magic': "offer a day's free work at the puppet theatre, to get a foot in the door"}, 'chance': 0.72}),
    ('ask a voice actor friend how the business really works', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'mentor', 'v': 'achievement, security', 'world': {'tribal': 'ask the old voice of the bear how the hidden voices are chosen', 'magic': 'ask an old puppet voice how the trade really works'}, 'chance': 0.74}),
    ('let it pass, for the day job and the family', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence, tradition', 'world': {'tribal': 'let it pass, for the hunt and the family', 'magic': "let it pass, for the day's trade and the family"}, 'chance': 0.76}),
 ]},
{'name': 'the stage management team is a person short',
 'stages': 'young_adult adult mature',
 'age': (17, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.015, 0.01, 0.005, 0.0),
 'drivers': 'prosper+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss, friend, partner, mentor',
 'requires': 'stage technician | drama school student | amateur actor | community theatre director',
 'worlds': {'earth': "a touring show's stage manager has left, and the company needs one by Monday",
            'tribal': 'the keeper of the fire and the masks is sick, and the gathering is in three days',
            'magic': "the playhouse's book-keeper has fled with the takings, and the season opens on the morrow"},
 'timing': {'times': 'per stage technician or drama student of a year or more, or amateur actor or community theatre '
                     'director of two years or more, a year: about 1 in 70 young adults are offered stage management '
                     'work on a touring show (estimate)',
            'likelier': "a busy touring season, a company that knows the person's work backstage, someone who keeps "
                        'calm and keeps lists',
            'rarer': 'a lean year for the theatres, a company with a full team, a person tied to a job or a family '
                     'that cannot move',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "The touring company's stage manager has left in the middle of the run, and the company "
                       'manager rings {N} on a Thursday: the show is in a new town on Monday, the prompt book is a '
                       'mess, and someone has to call the cues.'),
                      ('W',
                       'Somebody has to keep the show running, and {N} knows the cues better than anyone outside the '
                       'booth. It feels like a duty.'),
                      ('U',
                       '{N} has always wondered how the deputy manages forty cues in the storm scene. Now there is a '
                       'chance to find out from the inside.'),
                      ('B',
                       'A stage manager is the person in the building who knows everything. {N} can see what that '
                       'would be worth, and what it should pay.'),
                      ('R',
                       'A new town every week, a van full of scenery and a headset in the dark. Part of {N} wants to '
                       'go tonight.'),
                      ('G',
                       'The tour is away for eleven weeks, and {N} thinks of the people at home, and of the local '
                       "players' play in May, which needs {N} too.")],
            'tribal': [('',
                        'The keeper of the fire and the masks is sick with fever, and the gathering is in three '
                        'days. Someone must know where every mask hangs and when every drum begins, and the elders '
                        'are looking at {N}.')],
            'magic': [('',
                       "The playhouse's book-keeper has fled in the night with the takings and the prompt book, and "
                       'the season opens on the morrow. The master of the house is at {Ns} door before breakfast.')]},
 'outcomes': (['By Monday {N} is in the booth with a headset on and the prompt book open, and the storm scene goes '
               'without a hitch.',
               'Whatever {N} chose, the company got its show up, and {N} is remembered as the one who helped.'],
              ['The company finds someone with more years in the booth, and thanks {N} kindly for the trouble.',
               'The first week is chaos, the cues come late, and {N} wonders whether this was ever the right road.']),
 'options': [
    ('take it, as the company asks, and learn the job from the deputy', 'W1', None, 0.45, '', {'title': 'stage manager', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'conformity, benevolence', 'world': {'tribal': "take it, as the elders ask, and learn the work from the keeper's helper", 'magic': 'take it, as the master asks, and learn the book from the deputy'}, 'chance': 0.03}),
    ('take it, and rebuild the prompt book overnight', 'U1', None, 0.45, '', {'title': 'stage manager', 'grants_if_fails': 'a long shot that missed', 'grants': 'calling the show', 'v': 'achievement, self-direction', 'world': {'tribal': 'take it, and walk the whole telling through overnight, mask by mask', 'magic': 'take it, and write a new prompt book overnight'}, 'chance': 0.03}),
    ('take it, and make running shows the career from now on', 'B1', None, 0.45, '', {'title': 'stage manager', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'achievement, power', 'world': {'tribal': "take it, and make keeping the fire and the masks a life's work", 'magic': 'take it, and make keeping the book a trade for life'}, 'chance': 0.03}),
    ('say yes tonight, and promise to stay as long as they need', 'R1', None, 0.45, '', {'title': 'stage manager', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'stimulation, benevolence', 'world': {'tribal': 'say yes tonight, and promise the elders every gathering until the keeper is well', 'magic': 'say yes tonight, and promise the master the whole season'}, 'chance': 0.03}),
    ('take it, if the tour can get home every Sunday', 'G1', None, 0.45, '', {'title': 'stage manager', 'grants_if_fails': 'a long shot that missed', 'v': 'security, tradition', 'world': {'tribal': 'take it, if the band can be reached by nightfall', 'magic': 'take it, if the season stays in the home city'}, 'chance': 0.03}),
    ('help for one week only, while the company finds someone', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'calling the show', 'v': 'conformity, achievement', 'world': {'tribal': 'help for one gathering only, while the keeper mends', 'magic': 'help for one week only, while the master finds a new book-keeper'}, 'chance': 0.8}),
    ('say no, and put forward a friend who needs the work', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'say no, and put forward a friend who needs the standing'}, 'chance': 0.78}),
    ("run the local players' prompt desk instead, close to home", 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'stayed home', 'v': 'security, tradition', 'world': {'tribal': "keep the masks for the band's own small fires instead, close to home", 'magic': "keep the book for the guild's players instead, close to home"}, 'chance': 0.78}),
    ('say no, because the plan was always to act', 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'self-direction, tradition', 'world': {'tribal': 'say no, because the plan was always to tell'}, 'chance': 0.8}),
    ('take a better-paid job on a film crew instead', 'U.34 B.33 R.33', None, 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': 'go with the hunters for the winter instead, for a better share', 'magic': 'take a better-paid place with a travelling glamour show instead'}, 'chance': 0.74}),
 ]},
{'name': 'a director is needed for the autumn play',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.02, 0.05, 0.05, 0.03),
 'drivers': 'community+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, performing',
 'horizon': 'months',
 'roles': 'friend, neighbour, elder, partner, rival',
 'requires': 'amateur actor | drama teacher | community theatre director',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': "the society's director has moved away, and the autumn play has no one",
            'tribal': 'the old shaper of the tellings has died, and midwinter is coming',
            'magic': "the guild's master of pageants is gone, and the feast day is a month away"},
 'timing': {'times': "per amateur actor, drama teacher or community theatre director of three years' standing or "
                     'more a year: about 1 in 25 adults are asked to direct a show (estimate)',
            'likelier': 'a society that has lost its director, someone who has assisted a director before, a retired '
                        'member with time, a town with a hall and an audience',
            'rarer': 'a society with a director for years to come, a full-time job and a young family, a society '
                     'short of members and money',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "The players' director of twenty years has moved to the coast to be near grandchildren, and "
                       'the autumn play has a cast, a hall booked and no one to direct it. At the committee meeting, '
                       'everyone turns slowly to look at {N}.'),
                      ('W',
                       '{N} has watched the old director work for years and knows how the society likes things done. '
                       'Someone should keep it going properly.'),
                      ('U',
                       '{N} has always had ideas in rehearsal, quietly, about where the actors should stand and why '
                       'the second act drags. Now they could be tried.'),
                      ('B',
                       'Whoever directs chooses the play and casts it, and the society will follow that person for '
                       'years. {N} can see the shape of it.'),
                      ('R',
                       'Directing! The whole play in {Ns} hands, every choice, every risk. {N} wants to say yes '
                       'before the chair finishes the sentence.'),
                      ('G',
                       'The players have been {Ns} second family for years. {N} does not want the autumn play to be '
                       'the first one missed in forty years.')],
            'tribal': [('',
                        'The old shaper of the tellings has died in the autumn, and midwinter is coming. Someone '
                        'must choose who tells which story, and where they stand by the fire, and the elders look at '
                        '{N}.')],
            'magic': [('',
                       "The guild's master of pageants has gone to his rest, and the feast day is a month away. The "
                       'guild masters meet in the hall above the bakery and look at {N}.')]},
 'outcomes': (['The autumn play opens on a Thursday in October to a full hall, and the old director sends a card '
               'from the coast.',
               'Whatever {N} chose, the society finds its feet, and the autumn play goes on.'],
              ['Rehearsals fall behind, two of the cast drop out, and the play opens a month late to half a hall.',
               'The committee argues for weeks, and the autumn play is quietly cancelled.']),
 'options': [
    ('take it on, and run it the way the old director did', 'W1', None, 0.45, '', {'title': 'community theatre director', 'aims': 'director', 'v': 'tradition, conformity', 'world': {'tribal': 'take it on, and shape the tellings the way the old shaper did', 'magic': 'take it on, and run the pageant the way the old master did'}, 'chance': 0.1}),
    ('take it on, and stage the play in a way the town has never seen', 'U1', None, 0.45, '', {'title': 'community theatre director', 'v': 'self-direction, achievement', 'world': {'tribal': 'take it on, and set the tellings in a way the band has never seen', 'magic': 'take it on, and stage the pageant in a way the town has never seen'}, 'chance': 0.2}),
    ('take it on, with a tight budget and a rehearsal plan nobody can argue with', 'B1', None, 0.45, '', {'title': 'community theatre director', 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'take it on, with every night of the tellings planned before the first frost', 'magic': 'take it on, with a tight purse and a plan nobody can argue with'}, 'chance': 0.2}),
    ('take it on, and choose the play everyone said was too hard', 'R1', None, 0.45, '', {'title': 'community theatre director', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'take it on, and choose the old telling everyone said was too hard', 'magic': 'take it on, and choose the old mystery everyone said was too hard'}, 'chance': 0.2}),
    ('take it on, and direct the autumn play every year from now on', 'G1', None, 0.45, '', {'title': 'community theatre director', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'take it on, and shape the midwinter tellings every year from now on', 'magic': 'take it on, and run the feast-day pageant every year from now on'}, 'chance': 0.1}),
    ('run a free workshop for the town, and find a new director in it', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': 'teach the young ones the shaping for a moon, and find a new shaper among them', 'magic': 'hold a free class for the town, and find a new pageant master in it'}, 'chance': 0.8}),
    ("co-direct with the society's oldest member, learning on the way", 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'directing actors', 'v': 'tradition, achievement', 'world': {'tribal': 'shape the tellings beside the oldest teller, learning on the way', 'magic': "run the pageant beside the guild's oldest player, learning on the way"}, 'chance': 0.8}),
    ('back a director who will keep the newcomers out of the leads', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: shutting out the newcomers; backfire: the newcomers leave, and the spring play cannot be cast', 'v': 'tradition, power', 'world': {'tribal': 'back a shaper who will keep the newcomers to the band away from the great stories', 'magic': 'back a master who will keep the newer guild members out of the leads'}, 'chance': 0.78}),
    ('direct for a small professional company that wants someone instead', 'U.34 B.33 R.33', None, 0.5, '', {'title': 'director', 'requires': 'community theatre director', 'without': 'impossible', 'v': 'achievement, power', 'world': {'tribal': 'shape the tellings for a travelling band of players instead', 'magic': 'direct for a small travelling company that wants someone instead'}, 'chance': 0.35}),
    ('say no, because acting is the fun part and someone else will step up', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'hedonism, security', 'world': {'tribal': 'say no, because telling is the fun part and someone else will step up'}, 'chance': 0.82}),
 ]},
{'name': 'the script competition',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.008, 0.02, 0.02, 0.015, 0.008),
 'drivers': 'era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning, making',
 'horizon': 'months',
 'roles': 'friend, mentor, partner, colleague, rival',
 'requires': 'writing stories | writing scripts | novelist | journalist',
 'worlds': {'earth': 'a national script competition, with a staged reading as the prize',
            'tribal': 'the gathering will hear new tellings this summer, and the best will be played at the great '
                      'fire',
            'magic': 'the court offers a laurel for a new play, to be staged at midsummer'},
 'timing': {'times': 'per novelist or journalist of a year or more, or writer of two years or more with a stage '
                     'history (amateur, community theatre, drama school or professional), a year: about 1 in 50 '
                     'enter a script competition (estimate); most competitions get thousands of entries',
            'likelier': 'a new competition with a staged reading as the prize, a finished draft in a drawer, a '
                        'teacher or friend who says send it',
            'rarer': 'a fee to enter, a deadline in a busy month, a writer who never finishes anything',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'A national script competition has opened for new plays. The winner gets a staged reading in '
                       'a real theatre, with real actors and an audience, and a director who reads all the '
                       'shortlist. The deadline is in six weeks, and {N} has a play in a drawer.'),
                      ('W',
                       '{N} has read the rules twice: no more than ninety pages, the name on a separate sheet, a '
                       'font that is easy to read. A good play deserves to be sent in properly.'),
                      ('U',
                       '{Ns} play has a problem in the middle, and {N} knows it. Six weeks is time enough to fix it, '
                       'or to find out it cannot be fixed.'),
                      ('B',
                       'About four thousand scripts will come in. {N} wonders who reads the first ten pages, and '
                       'what makes them read on.'),
                      ('R',
                       'The play came out in a rush last winter, at night, and {N} has not dared to read it since. '
                       'Perhaps it is wonderful. Perhaps it is mad.'),
                      ('G',
                       'The play is about {Ns} town: the closing of the mill, the market, the way people talk at the '
                       'bus stop. {N} wonders whether anyone outside would care.')],
            'tribal': [('',
                        'This summer the gathering will hear new tellings by the long fire, and the best will be '
                        'played at the great fire before every band. {N} has a telling that has grown for years in '
                        'the dark months.')],
            'magic': [('',
                       'The court has offered a laurel for a new play, to be staged at midsummer before the whole '
                       'court. {N} has a play half-copied in a good hand, and a month to finish it.')]},
 'outcomes': (['A letter comes in the spring: the play is on the shortlist of six, and then, a week later, it is the '
               'winner.',
               'Whatever {N} chose, the play is better for it, and a real audience will hear it before long.'],
              ['The results come out in the spring, and {Ns} play is not among the forty on the longlist.',
               '{N} misses the deadline by a day, rewriting the ending one last time.']),
 'options': [
    ('send the play in on time, set out exactly to the rules', 'W1', None, 0.45, '', {'title': 'playwright or screenwriter', 'v': 'conformity', 'world': {'tribal': 'bring the telling to the long fire on the right night, told exactly as the elders ask', 'magic': "send the play to the court on time, copied out exactly as the laurel's rules ask"}, 'chance': 0.08}),
    ('write the play nobody else could have written, and send that', 'U1', None, 0.45, '', {'title': 'playwright or screenwriter', 'identity': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'make the telling nobody else could have made, and bring that'}, 'chance': 0.07}),
    ('rewrite it ten times before sending, cutting every spare line', 'B1', None, 0.45, '', {'title': 'playwright or screenwriter', 'self_control': '+', 'v': 'achievement, power', 'world': {'tribal': 'tell it to the river ten times before the gathering, cutting every spare word'}, 'chance': 0.08}),
    ('write every night for a month, and send it the morning of the deadline', 'R1', None, 0.45, '', {'title': 'playwright or screenwriter', 'habit': True, 'self_control': '+', 'v': 'stimulation, self-direction', 'world': {'tribal': 'make the telling anew every night for a moon, and bring it on the last night'}, 'chance': 0.08}),
    ('write about the town and its people, just as they really talk', 'G1', None, 0.45, '', {'title': 'playwright or screenwriter', 'v': 'tradition, benevolence', 'world': {'tribal': 'make the telling about the band and its people, just as they really speak', 'magic': 'write about the city and its people, just as they really talk'}, 'chance': 0.08}),
    ('hold it back a year, and make the middle work first', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'hold the telling back a summer, and make the middle work first'}, 'chance': 0.7}),
    ("send a short version to the fringe's new writing night", 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'a fringe slot', 'v': 'benevolence, stimulation', 'world': {'tribal': 'tell a short version at the small fires of the gathering', 'magic': "send a short version to the summer fair's new plays night"}, 'chance': 0.68}),
    ('send it to every theatre with an open script window', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'contact in the trade', 'habit': True, 'v': 'power, achievement', 'world': {'tribal': "carry the telling to every band's fire in turn", 'magic': 'send it to every playhouse that reads new plays'}, 'chance': 0.68}),
    ("join a writers' group, and hear the play read aloud there first", 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'writing scripts', 'v': 'self-direction, benevolence', 'world': {'tribal': 'sit with the other tellers, and hear the telling spoken there first', 'magic': "join a players' reading circle, and hear the play read aloud there first"}, 'chance': 0.7}),
    ('turn it into a radio play for the local station', 'U.34 B.33 G.33', None, 0.5, '', {'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': "turn it into a telling for the children's fire", 'magic': 'turn it into a puppet play for the market'}, 'chance': 0.68}),
 ]},
{'name': 'the theatre needs an artistic director',
 'stages': 'adult mature elder',
 'age': (28, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.1, 0.1, 0.05),
 'drivers': 'era+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, publiclife',
 'horizon': 'years',
 'roles': 'colleague, boss, rival, friend, mentor',
 'requires': 'director',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "the regional theatre's artistic director steps down after ten years",
            'tribal': "the keeper of the gathering's tellings has grown too old",
            'magic': "the court playhouse's master has died, and the Order will choose another"},
 'timing': {'times': "per director of two years or more a year: about 1 in 10 see a theatre's top post open that "
                     'they could apply for (estimate); about 1,950 nonprofit theatres in the US each change their '
                     "artistic director about once in ten years (the US theatre network's yearly survey, 2019); "
                     'about 1 life in 10,000 runs a theatre (catalogue share; estimate)',
            'likelier': 'a theatre whose director is stepping down, a board looking for new blood, a director with a '
                        'body of work the town has seen',
            'rarer': 'a theatre in debt, a board with its choice already made, a director who has never run a '
                     'building',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "The regional theatre's artistic director is stepping down after ten years, and the board has "
                       'advertised the post: the building, the money, the seasons, the choice of who plays what for '
                       'years to come. {Ns} name has been mentioned in the bar more than once.'),
                      ('W',
                       'The theatre has served the town well for ten years. Whoever takes it on owes the town the '
                       'same care, and {N} knows the board, the staff and the audience by name.'),
                      ('U',
                       '{N} has seen every show in the building for a decade and knows what is missing from it: the '
                       'new plays, the plays that would bring in the people who never come.'),
                      ('B',
                       'The post decides who works in the region for ten years. {N} counts the board members who '
                       'would back {N}, and the ones who would need persuading.'),
                      ('R',
                       'A whole theatre to fill with whatever {N} wants to see. The thought is like standing at the '
                       'top of a high diving board.'),
                      ('G',
                       'It is the theatre {N} was taken to as a child, the one with the velvet seats and the smell '
                       "of oranges. {N} would want it to stay the town's own.")],
            'tribal': [('',
                        "The keeper of the gathering's tellings has grown too old to walk to the great fire, and the "
                        'elders of every band will choose another. {Ns} name is spoken at more than one fire.')],
            'magic': [('',
                       "The court playhouse's master has died in his chair, and the Order will choose another to run "
                       "the house and its seasons. {Ns} name is said in the players' room more than once.")]},
 'outcomes': (['The board rings on a Friday night, and by the spring {Ns} first season is printed on the posters '
               'outside.',
               'Whatever {N} chose, the theatre is in good hands, and {N} is glad of the part played in it.'],
              ['The post goes to a director from the capital, and the board writes a kind letter.',
               'The interview goes badly, a question about money {N} had not seen coming, and the board chooses '
               'someone else.']),
 'options': [
    ('apply, with a careful plan for the next ten years', 'W1', None, 0.45, '', {'title': 'artistic director', 'v': 'conformity, security', 'world': {'tribal': 'speak to the elders, with a careful plan for the next ten summers', 'magic': 'put in for the post, with a careful plan for the next ten seasons'}, 'chance': 0.08}),
    ('apply, with a first season of new plays nobody else would risk', 'U1', None, 0.45, '', {'title': 'artistic director', 'v': 'self-direction, achievement', 'world': {'tribal': 'speak to the elders, with a summer of new tellings nobody else would risk', 'magic': 'put in for the post, with a first season of new plays nobody else would risk'}, 'chance': 0.1}),
    ('win over the board members one by one before the interview', 'B1', None, 0.45, '', {'title': 'artistic director', 'v': 'power, achievement', 'world': {'tribal': 'win over the elders one by one before the choosing', 'magic': 'win over the masters of the Order one by one before the choosing'}, 'chance': 0.11}),
    ('apply, with a plan to turn the whole building upside down', 'R1', None, 0.45, '', {'title': 'artistic director', 'v': 'stimulation, self-direction', 'world': {'tribal': 'speak to the elders, with a plan to move the great fire itself', 'magic': 'put in for the post, with a plan to turn the whole playhouse upside down'}, 'chance': 0.1}),
    ("apply, to keep the theatre the town's own", 'G1', None, 0.45, '', {'title': 'artistic director', 'v': 'tradition, benevolence', 'world': {'tribal': "speak to the elders, to keep the tellings the bands' own", 'magic': "put in for the post, to keep the playhouse the city's own"}, 'chance': 0.08}),
    ('back a younger director for the post, and help her prepare', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'back a younger teller for the keeping, and help her prepare', 'magic': 'back a younger master for the post, and help her prepare'}, 'chance': 0.74}),
    ("apply for the deputy's post, and learn the building first", 'W.34 U.33 B.33', None, 0.5, '', {'binds': True, 'v': 'achievement, security', 'world': {'tribal': 'ask to stand beside the new keeper, and learn the keeping first', 'magic': "put in for the deputy's post, and learn the house first"}, 'chance': 0.7}),
    ('stay freelance, free to direct wherever the work is', 'W.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'stay a wandering shaper, free to shape tellings at any fire', 'magic': 'stay a wandering master, free to direct wherever the work is'}, 'chance': 0.7}),
    ("back the board's favourite, in return for a promise of work", 'U.34 B.33 G.33', None, 0.5, '', {'v': 'security, power', 'world': {'tribal': "back the elders' choice, in return for a great story every summer", 'magic': "back the Order's choice, in return for a promise of work"}, 'chance': 0.72}),
    ('start a small company instead, with friends and no money', 'B.34 R.33 G.33', None, 0.5, '', {'grants': 'a company of your own', 'mark': 'took a wild risk', 'v': 'self-direction, stimulation', 'world': {'tribal': 'gather a small band of tellers instead, with friends and no gifts', 'magic': 'start a small travelling company instead, with friends and no money'}, 'chance': 0.7}),
 ]},
{'name': 'leaving acting for another life',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.06, 0.08, 0.08, 0.05),
 'drivers': 'stress+.3 money-.2 family+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, money, family',
 'horizon': 'years',
 'roles': 'partner, parent, friend, colleague, child',
 'requires': 'professional actor | voice actor | lead actor or actress',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': "a year without a part, a partner who wants a steadier life, an offer from a friend's firm",
            'tribal': 'the hunt and the hearth call louder than the tellings',
            'magic': "a merchant house offers a clerk's stool and a wage every week"},
 'timing': {'times': 'per professional or voice actor of a year or more a year: about 1 in 15 weigh leaving; most '
                     'actors leave the profession within ten years (estimate)',
            'likelier': 'a year without a part, a partner who wants a steadier life, a child on the way, debts, an '
                        "offer from a friend's firm",
            'rarer': 'a run of good parts, an agent who keeps the auditions coming, money from somewhere else',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'It has been eleven months since the last part. The rent is two weeks late, {partner} has '
                       'stopped asking about auditions, and a friend has offered {N} a job with a wage that arrives '
                       'every month, whether or not anyone is casting.'),
                      ('W',
                       '{N} has always kept promises: to the agent, to the companies, to the people at home. Perhaps '
                       'it is time to keep a different one, to the people who need a steady wage.'),
                      ('U',
                       '{N} has learned more about people in fifteen years of acting than in anything else. The '
                       'question is where that knowledge would be most use now.'),
                      ('B',
                       '{N} knows how the business works from the inside: who casts, who signs, who gets paid. There '
                       'might be more money on the other side of the table.'),
                      ('R',
                       '{N} cannot imagine a life without the stage, and cannot face another year like this one. '
                       'Something has to give, and soon.'),
                      ('G',
                       '{N} thinks of home: the family, the old town, the local players who would take {N} back '
                       'tomorrow. And of the stage, which has been home too.')],
            'tribal': [('',
                        'The tellings have brought little meat to {Ns} fire this year, and the hunt and the hearth '
                        'call louder. The elders say there is no shame in setting down the mask.')],
            'magic': [('',
                       "A merchant house in the city has offered {N} a clerk's stool and a wage every week. The "
                       'playhouses have offered nothing since the spring.')]},
 'outcomes': (['A year later {N} has a different life, and it fits better than {N} expected, though the theatre '
               'still pulls on opening nights.',
               'The choice is made and it holds, and the money worries of the old year fade into the background.'],
              ['The new road is harder than it looked, and within the year {N} is reading the casting pages again.',
               'The offer falls through at the last moment, and {N} is left where {N} started, only more tired.']),
 'options': [
    ('become a casting director, choosing the actors instead of being chosen', 'W1', None, 0.45, '', {'title': 'casting director', 'requires': 'a casting eye', 'without': 'means', 'lacking': 0.3, 'door': True, 'v': 'conformity, benevolence', 'world': {'tribal': 'become the one who chooses the tellers, instead of being chosen', 'magic': 'become a casting master, choosing the players instead of being chosen'}, 'chance': 0.58}),
    ('train to teach drama, and pass on what the stage taught', 'U1', None, 0.45, '', {'title': 'drama teacher', 'identity': True, 'v': 'benevolence, achievement', 'world': {'tribal': 'teach the young ones the tellings, and pass on what the fire taught', 'magic': "train to teach the players' art, and pass on what the stage taught"}, 'chance': 0.58}),
    ("become an agent, and fight for other actors' fees", 'B1', None, 0.45, '', {'title': 'talent agent', 'requires': 'striking a deal', 'without': 'means', 'lacking': 0.3, 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'become a go-between, and win other tellers their gifts', 'magic': "become a broker, and fight for other players' fees"}, 'chance': 0.62}),
    ('start an apprenticeship in a trade, and work with the hands', 'R1', None, 0.45, '', {'title': 'apprentice', 'drops': 'professional actor; voice actor; lead actor or actress', 'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': "learn the bowyer's trade, and work with the hands", 'magic': 'start an apprenticeship with a craftsman, and work with the hands'}, 'chance': 0.6}),
    ('stay, and give the acting one more honest year', 'G1', None, 0.45, '', {'self_control': '+', 'aims': 'lead actor or actress', 'v': 'tradition, security', 'world': {'tribal': 'stay, and give the tellings one more honest year'}, 'chance': 0.55}),
    ('go home to the family firm, and join the local players', 'W.34 U.33 G.33', None, 0.5, '', {'title': 'amateur actor', 'drops': 'professional actor; voice actor; lead actor or actress', 'mark': 'came home', 'v': 'tradition, security', 'world': {'tribal': "go home to the family's hunting grounds, and tell at the band's small fires", 'magic': "go home to the family trade, and join the guild's players"}, 'chance': 0.7}),
    ('start a business coaching people for auditions', 'W.34 B.33 R.33', None, 0.5, '', {'title': 'founder of a firm', 'v': 'achievement, power', 'world': {'tribal': 'teach young tellers for gifts, before they face the elders', 'magic': 'open a school for players before their trials'}, 'chance': 0.62}),
    ("take a stage manager's job, with a steady wage", 'W.34 B.33 G.33', None, 0.5, '', {'title': 'stage manager', 'requires': 'stagecraft', 'without': 'means', 'lacking': 0.3, 'v': 'security, conformity', 'world': {'tribal': 'become keeper of the fire and the masks, with a steady share', 'magic': 'take a post as book-keeper of a playhouse, with a steady wage'}, 'chance': 0.62}),
    ('travel for a year, and decide on the way', 'U.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'walk the far valleys for a year, and decide on the way'}, 'chance': 0.7}),
    ('put the savings into producing a show', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'a company of your own', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'binds': True, 'v': 'achievement, power', 'world': {'tribal': "give the winter's stores to put on a great telling", 'magic': "put the savings into a show of one's own"}, 'chance': 0.55}),
 ]},
{'name': "the city wants the town's show",
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.04, 0.03, 0.015),
 'drivers': 'community+.2 prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, community, performing',
 'horizon': 'months',
 'roles': 'friend, colleague, neighbour, rival, mentor',
 'requires': 'community theatre director | a company of your own',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': "a city theatre wants the town's show for a three-week run, and asks who will run it",
            'tribal': "the elders of a great band want the small band's telling at their own fire, and ask who will "
                      'bring it',
            'magic': "a city playhouse wants the ward's pageant for a short season, and asks who will bring it"},
 'timing': {'times': 'per community theatre director or small company of three years or more a year: about 1 in 30 '
                     'has a show that a city theatre or a touring house asks to take for a run (estimate); amateur '
                     'and small-company shows move to paid runs every year at the largest fringe festival and the '
                     'regional houses, and about 1 in 3 people offered a post in such a run hold it (estimate)',
            'likelier': 'a show the whole town talked about, a reviewer from the city in the hall, a theatre with a '
                        'gap in its season',
            'rarer': 'a society short of money or members, a show built on local jokes, a cast that cannot leave its '
                     'day jobs',
            'gap_years': (5.0, 10.0)},
 'scenes': {'earth': [('',
                       'The autumn show was the best thing the town had seen in years, and a producer from a city '
                       'theatre sat in the third row on the last night. Now she writes: the theatre has three weeks '
                       'free in the spring and would like the show, with its cast if possible, and someone to run '
                       'it. The committee reads the letter twice and looks at {N}.'),
                      ('W',
                       'A show that moves needs someone who knows every cue, every prop and every person in it. {N} '
                       'has kept the prompt book since the first read-through.'),
                      ('U',
                       'The show was made for a church hall. On a real stage it would need rethinking from the first '
                       'scene, and {N} already knows how.'),
                      ('B',
                       'Three weeks in the city, a proper box office, a share of the takings. {N} can see exactly '
                       'what the run would cost and what it could make, and who should hold the purse.'),
                      ('R',
                       'A real stage! {N} wants to take everything the town did and do it twice as boldly, with the '
                       'city watching.'),
                      ('G',
                       'The cast are shop workers and nurses and two retired teachers. {N} wonders what three weeks '
                       'in the city would mean to them, and to the town that made the show.')],
            'tribal': [('',
                        "The elders of a great band two valleys away have heard of the small band's midwinter "
                        'telling, and want it played at their own fire before the thaw. They ask who will bring it, '
                        'and the small band looks at {N}.')],
            'magic': [('',
                       "A city playhouse has heard of the ward's feast-day pageant and wants it for a short season "
                       'after the spring fair. The guild masters read the letter aloud in the hall above the bakery '
                       'and look at {N}.')]},
 'outcomes': (['The run opens in the spring to a full house of strangers, and on the last night half the town comes '
               'up on the train to cheer.',
               'Whatever {N} chose, the show had the life it deserved, and the society is prouder of itself than it '
               'has been in years.'],
              ["The city theatre's money falls through in February, and the letter that comes instead is long, kind "
               'and final.',
               'The run goes ahead, the reviews are polite, the houses are half full, and {N} comes home knowing '
               'exactly what a city run asks of a person.']),
 'options': [
    ('run the stage side of the city run, cue by cue, by the book', 'W1', None, 0.45, '', {'title': 'stage manager', 'requires': 'community theatre director', 'without': 'impossible', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': "keep the fire and the masks for the telling at the great band's fire, sign by sign", 'magic': "keep the book for the city season, cue by cue, as the playhouse's rules ask"}, 'chance': 0.3}),
    ('direct it again for the city, rethought scene by scene for a bigger stage', 'U1', None, 0.45, '', {'title': 'director', 'requires': 'community theatre director', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'shape the telling again for the great fire, every scene thought through anew', 'magic': 'stage the pageant again for the playhouse, rethought scene by scene'}, 'chance': 0.3}),
    ('raise the money for the run, and produce it yourself, purse and contracts', 'B1', None, 0.45, '', {'title': 'producer', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'gather the hides, the masks and the feast for the telling yourself, and be owed for it', 'magic': "put up the coin for the season yourself, and take the play-merchant's share"}, 'chance': 0.3}),
    ("direct the city run, and make it twice as bold as the town's", 'R1', None, 0.45, '', {'title': 'director', 'requires': 'community theatre director', 'without': 'impossible', 'mark': 'took a wild risk', 'v': 'stimulation, power', 'world': {'tribal': 'shape the telling for the great fire, twice as wild as at home', 'magic': "stage the pageant for the city, twice as bold as the ward's"}, 'chance': 0.3}),
    ('keep the show at home for the town, and let the city come to it', 'G1', None, 0.45, '', {'grants': 'good name in town', 'mark': 'stayed home', 'v': 'tradition, benevolence', 'world': {'tribal': "keep the telling at the band's own fire, and let the great band come to hear it", 'magic': 'keep the pageant in the ward, and let the city come to it'}, 'chance': 0.3}),
    ("draw up the run's budget and schedule line by line, for whoever runs it", 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'organising people', 'self_control': '+', 'v': 'achievement, security', 'world': {'tribal': 'count every hide, mask and night of the journey, for whoever brings the telling', 'magic': "draw up the season's purse and calendar line by line, for whoever brings the pageant"}, 'chance': 0.7}),
    ('hand the show to the youngest of the cast to take to the city', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, stimulation', 'world': {'tribal': 'send the youngest players to bring the telling to the great fire', 'magic': 'hand the pageant to the youngest guild players to bring to the city'}, 'chance': 0.7}),
    ('ask the town council to back the run, and bank the grant for the society', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'patron', 'v': 'security, tradition', 'world': {'tribal': 'ask the elders for gifts to carry the telling, and keep what is left for the band', 'magic': "ask the ward's aldermen to back the season, and bank the purse for the guild"}, 'chance': 0.7}),
    ('rework the show with the whole cast for a bigger stage, and let another run it', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'directing actors', 'v': 'self-direction, tradition', 'world': {'tribal': 'rework the telling with every player for the great fire, and let another bring it', 'magic': 'rework the pageant with the whole company for a real stage, and let another run it'}, 'chance': 0.7}),
    ('film the last night, and send the film to every theatre in the city', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'a showreel', 'v': 'stimulation, achievement', 'world': {'tribal': 'carry the telling to the bands at every crossing, so the whole valley asks for it', 'magic': 'have the last night caught in a scrying glass, and send it to every playhouse in the city'}, 'chance': 0.7}),
 ]},
{'name': 'the school needs someone to take drama',
 'stages': 'young_adult adult mature',
 'age': (23, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.025, 0.025, 0.015, 0.0),
 'drivers': 'era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, school, performing',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, partner',
 'requires': 'teacher',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "the school's drama teacher has left, and the head asks a teacher who acts to take the subject "
                     'on',
            'tribal': 'the old teller who taught the children has grown too frail to teach, and the elders ask '
                      'someone who knows the tellings to take it on',
            'magic': "the town school has lost its master of the players' art, and the schoolmaster is asked to take "
                     'the class'},
 'timing': {'times': 'per teacher of two years or more with a stage history a year: about 1 in 40 are asked to take '
                     "on drama when the school's drama teacher leaves or the subject is added (estimate); English "
                     "secondary schools had 8,963 drama teachers in 2019 (an education charity's count), many of "
                     'them teachers of another subject first',
            'likelier': 'a drama teacher who has left in the middle of the year, a head who wants a school play, a '
                        "teacher known for the local players' shows",
            'rarer': 'a school cutting its arts subjects, a full timetable, a teacher close to retiring',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       'The drama teacher has left at the end of the autumn term for a job in another city, and the '
                       'school play is in March. The head stops {N} in the corridor: everyone knows about the local '
                       "players' shows, so would {N} take drama on, for the spring at least, and perhaps for good?"),
                      ('W',
                       'A subject needs a syllabus, a scheme of work and somebody who will be there every week. {N} '
                       'could do it, if it is done properly.'),
                      ('U',
                       '{N} has always thought drama could be taught like any craft: voice, text and movement, step '
                       'by step, until a shy child can stand in front of a room and be heard.'),
                      ('B',
                       'Head of drama means a department, a budget and a line on the timetable. {N} wonders what the '
                       'head would give to have the school play saved.'),
                      ('R',
                       'The school play! {N} is already imagining a musical: the whole year group on stage, a band '
                       'in the pit, the hall roaring.'),
                      ('G',
                       'There are children in every class who never get chosen for anything. {N} thinks of them '
                       'first, and of the school hall on Saturday mornings, empty.')],
            'tribal': [('',
                        'The old teller who taught the children the tellings has grown too frail to sit out in the '
                        'cold, and the small ones sit at the fire with nobody to teach them the voices and the '
                        'masks. The elders look at {N}, who has told at the turning seasons for years.')],
            'magic': [('',
                       "The town school's master of the players' art has gone to a guild school in the capital, and "
                       "the masque is at midsummer. The schoolmaster asks {N}, who plays with the ward's mystery "
                       'players, to take the class.')]},
 'outcomes': (['The school play goes on in March after all, every seat taken, and by the summer drama has a room of '
               'its own and a waiting list.',
               'Whatever {N} chose, the children have a stage this year, and {N} is glad of the part played in it.'],
              ['The head gives drama to a newly qualified teacher from outside, and thanks {N} warmly in the staff '
               'room.',
               'The spring term swallows everything, the play is cut to a reading in the library, and {N} promises '
               'to do it properly next year.']),
 'options': [
    ('take it on properly, with a scheme of work and a course in the holidays', 'W1', None, 0.45, '', {'title': 'drama teacher', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': "take on the children's tellings properly, one telling for each moon", 'magic': "take on the players' class properly, with a plan for every week"}, 'chance': 0.3}),
    ('take it on as a craft, and teach voice, text and movement step by step', 'U1', None, 0.45, '', {'title': 'drama teacher', 'identity': True, 'v': 'achievement, conformity', 'world': {'tribal': 'teach the children the voices, the masks and the steps, one at a time', 'magic': "teach the players' art as a craft, voice, text and movement, step by step"}, 'chance': 0.3}),
    ('take it on as head of drama, with a department and a budget of its own', 'B1', None, 0.45, '', {'title': 'drama teacher', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "take on the teaching, and ask for a teller's share of every hunt for it", 'magic': 'take the class as its master, with a stipend and a room of its own'}, 'chance': 0.3}),
    ('direct the school musical this once, with the whole year group, and hand drama back', 'R1', None, 0.45, '', {'grants': 'directing actors', 'mark': 'took a wild risk', 'v': 'stimulation, benevolence', 'world': {'tribal': 'shape one great telling with every child of the band, and hand the teaching back after', 'magic': 'stage one great masque with the whole school, and hand the class back after'}, 'chance': 0.3}),
    ('start a Saturday youth theatre in the school hall, open to every child in town', 'G1', None, 0.45, '', {'title': 'community theatre director', 'habit': True, 'v': 'tradition, universalism', 'world': {'tribal': 'gather the children at the fire on the quiet nights, every child of the band welcome', 'magic': "start a feast-day players' class in the school hall, open to every child in the ward"}, 'chance': 0.3}),
    ('ask the head for a budget and a proper studio before giving an answer', 'W.5 B.5', None, 0.5, '', {'grants': 'organising people', 'v': 'security, conformity', 'world': {'tribal': 'ask the elders for a sheltered place and hides for masks before giving an answer', 'magic': 'ask the schoolmaster for a stipend and a proper room before giving an answer'}, 'chance': 0.7}),
    ('say no, and hand the class to a colleague who trained in drama', 'W.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': "say no, and send the elders to a teller of the next band who knows the children's tellings", 'magic': 'say no, and put forward a colleague who studied at the guild school'}, 'chance': 0.7}),
    ('take an evening course in teaching drama first, and give an answer next year', 'U.5 B.5', None, 0.5, '', {'grants': 'teaching', 'aims': 'drama teacher', 'v': 'achievement, security', 'world': {'tribal': 'sit with the teller of the next band for a winter first, and give an answer at the thaw', 'magic': "take the guild school's evening course first, and give an answer next year"}, 'chance': 0.7}),
    ('write a play for the year group, with a part for every child who wants one', 'U.5 R.5', None, 0.5, '', {'grants': 'writing scripts', 'v': 'benevolence, stimulation', 'world': {'tribal': 'make a telling for the children, with a voice for every child who wants one', 'magic': 'write a masque for the class, with a part for every child who wants one'}, 'chance': 0.7}),
    ('take the class to see the local players, and let the children decide', 'R.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'stimulation, tradition', 'world': {'tribal': "take the children to the band's midwinter telling, and let them choose their spirits", 'magic': "take the class to the ward's mystery play, and let the children decide"}, 'chance': 0.7}),
 ]},
{'name': 'two actors, one part',
 'stages': 'young_adult adult mature elder',
 'age': (17, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.1, 0.08, 0.05, 0.03),
 'drivers': 'fortune+.1 ties+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, friends',
 'horizon': 'week',
 'roles': 'rival, friend, boss, colleague, partner',
 'requires': 'professional actor | understudy',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'two actors left at the recall, and one part',
            'tribal': 'two players want the great mask, and the elders will choose at dawn',
            'magic': 'two players are left for the court lead, and the patron will choose'},
 'timing': {'times': 'per professional actor of two years or more a year: about 1 in 10 reach the last two for a '
                     'lead (estimate)',
            'likelier': 'a busy year for new productions, an actor whose name is going round, an understudy who went '
                        'on and was seen',
            'rarer': 'a production cast with a famous face from the start, a lean year, an actor out of the city',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The third recall, on a Friday afternoon: {N} and {rival} are the last two for the lead, and '
                       'the director will choose on Monday. They were at drama school together, and they have been '
                       'going for the same parts for ten years.'),
                      ('W',
                       'There is a right way to win a part: be ready, be on time, and let the work speak. {N} means '
                       'to do it that way, whatever happens.'),
                      ('U',
                       '{N} has read the scene forty times and found something in it nobody else has seen: the line '
                       'in the middle where the character lies, and knows it.'),
                      ('B',
                       'A producer who has backed {N} before is putting money into this show. One phone call would '
                       'tip the scales, and everyone in the business makes them.'),
                      ('R',
                       '{N} wants this more than anything in years, and {rival} knows it, and {N} knows that {rival} '
                       'wants it just as much.'),
                      ('G',
                       '{rival} was the first friend {N} made in the city, the one who lent the rent in the first '
                       'hard winter. Now there is one part, and two of them.')],
            'tribal': [('',
                        'Two players want the great mask for the summer, {N} and {rival}, and the elders will choose '
                        'at dawn. They grew up at the same fire and learned the tellings from the same old woman.')],
            'magic': [('',
                       'Two players are left for the court lead, {N} and {rival}, and the patron will choose after '
                       'the last hearing. They came up through the same guild school, a year apart.')]},
 'outcomes': (['The director rings on Monday morning, and {N} sits on the kitchen floor for a while before calling '
               'anyone.',
               'Whatever {N} chose, {N} can look {rival} in the eye at the first night, and does.'],
              ["The part goes to {rival}, and the director says it came down to a coin's weight.",
               'The production is postponed a year, and by the time it is cast again both of them have moved on.']),
 'options': [
    ('play the scene exactly as the director asked, and let the work decide', 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'identity': True, 'v': 'conformity, universalism', 'world': {'tribal': 'tell it exactly as the elders asked, and let the telling decide', 'magic': "play it exactly as the patron's master asked, and let the work decide"}, 'chance': 0.16}),
    ('prepare the scene all week, every beat worked out', 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': 'prepare the telling every night until dawn, every breath worked out'}, 'chance': 0.18}),
    ('ring the producer who has backed the work before, and ask for a word', 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'a producer who backs you', 'without': 'approval', 'lacking': 0.3, 'mark': 'made an enemy', 'v': 'power, achievement', 'world': {'tribal': 'ask the elder who has always favoured the telling to speak at the choosing', 'magic': "send a note to the patron's steward, who has always favoured the work"}, 'chance': 0.17}),
    ('play it as if nothing else in the world mattered', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'stimulation, hedonism', 'chance': 0.18}),
    ('play it the way the old company taught, honest and plain', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'tradition, benevolence', 'world': {'tribal': 'tell it the way the old woman taught, honest and plain', 'magic': 'play it the way the guild school taught, honest and plain'}, 'chance': 0.17}),
    ('run lines with the rival the night before, as a kindness', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'practise the telling with the rival the night before, as a kindness'}, 'chance': 0.76}),
    ("report the rival's missed rehearsal call to the company manager", 'W.34 U.33 B.33', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: reporting a rival; backfire: the company sees why it was done, and the director chooses the rival', 'v': 'conformity, power', 'world': {'tribal': 'tell the elders that the rival missed the gathering of the tellers', 'magic': "report the rival's missed hearing to the patron's steward"}, 'chance': 0.72}),
    ('step aside, so the old friend can have the part', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence, tradition', 'world': {'tribal': 'step aside, so the old friend can wear the mask'}, 'chance': 0.78}),
    ("whisper to the director's assistant that the rival drinks", 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: a whispered lie about a rival; backfire: the company finds out who started it, and nobody will share a dressing room with {N}', 'v': 'power, achievement', 'world': {'tribal': "whisper to the elders' runner that the rival sleeps through the dawn tellings", 'magic': "whisper to the patron's steward that the rival drinks"}, 'chance': 0.72}),
    ('refuse a third recall, and walk away with pride intact', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'door': True, 'v': 'self-direction, power', 'world': {'tribal': 'refuse to tell again at dawn, and walk away with pride intact'}, 'chance': 0.72}),
 ]},
{'name': 'the show is a hit',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.03, 0.03, 0.02),
 'drivers': 'prosper+.2 fortune+.15 era+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, publiclife, money',
 'horizon': 'months',
 'roles': 'colleague, partner, friend, boss, rival',
 'requires': 'lead actor or actress | playwright or screenwriter | director | producer',
 'worlds': {'earth': 'queues round the block, a sold-out run and a transfer',
            'tribal': 'every band in the valley asks for the telling',
            'magic': 'the court asks for a command performance'},
 'timing': {'times': 'per lead, writer, director or producer a year: about 1 in 30 have a show that sells out and '
                     'moves on; only a few of those become known across the country (estimate)',
            'likelier': 'good years for the theatres, a show that catches the mood of the year, a reviewer who loves '
                        'it, a run long enough for word to spread',
            'rarer': 'a lean year, a short run in a small house, a show that opens in the same week as a famous one',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The show has sold out for its whole run, there is a queue for returns round the block every '
                       'evening, and a producer wants to move it to the biggest theatre in the capital. {Ns} name is '
                       'in the papers on Sunday, spelled right for once.'),
                      ('W',
                       '{N} thinks of the company: the stage manager who held it together, the designer, the actor '
                       'who never missed a cue. Whatever comes now, it was all of them.'),
                      ('U',
                       '{N} knows exactly why it works: the second act, the silence before the last scene. The trick '
                       'now is to do it again, better.'),
                      ('B',
                       'For a few months, the doors are open that were shut for years. {N} knows they will not stay '
                       'open long, and means to walk through as many as possible.'),
                      ('R',
                       'The applause at the curtain call goes on so long the cast runs out of bows. {N} has never '
                       'felt anything like it.'),
                      ('G',
                       'The whole family came on the first Saturday, and {Ns} old drama teacher wrote a card. {N} '
                       'keeps thinking of the small theatre where it all began.')],
            'tribal': [('',
                        'Every band in the valley has sent a runner to ask for {Ns} telling at its own fire before '
                        'the summer ends. Children at the far gathering act it out with sticks.')],
            'magic': [('',
                       'The court has asked for a command performance of {Ns} play before the crowned heads. The '
                       'broadsheets cry {Ns} name in the square.')]},
 'outcomes': (['By the end of the run {Ns} face is on the side of buses, and strangers smile at {N} in the street as '
               'if they were old friends.',
               'Whatever {N} chose, the success lasts long enough to change things, and {N} is still glad of how it '
               'was used.'],
              ['The transfer falls through over money, and the show closes when its run ends, a hit that went '
               'nowhere.',
               'The next production is announced, and nobody remembers to put {Ns} name on it.']),
 'options': [
    ('go to the national theatre awards, and thank the whole company on the night', 'W1', None, 0.45, '', {'grants': 'an award for acting', 'requires': 'lead actor or actress', 'without': 'impossible', 'v': 'conformity, benevolence', 'world': {'tribal': 'stand before the elders of every band at the great fire, and name every teller who helped', 'magic': "go before the court's laurel judges, and thank the whole company on the night"}, 'chance': 0.1}),
    ('give interviews about the craft, and never about the fame', 'U1', None, 0.45, '', {'grants': 'known across the country', 'v': 'achievement, self-direction', 'world': {'tribal': 'speak at every fire about how the telling was made, never about the praise', 'magic': 'speak to the broadsheets about the craft, never about the fame'}, 'chance': 0.12}),
    ('say yes to every chat show and advert while the name is hot', 'B1', None, 0.45, '', {'grants': 'known across the country', 'self_control': '-', 'v': 'power, achievement', 'world': {'tribal': 'go to every band that asks, and take every gift while the name is warm', 'magic': 'say yes to every salon and every patron while the name is hot'}, 'chance': 0.12}),
    ('party every night of the run with the famous people who now ring', 'R1', None, 0.45, '', {'grants': 'known across the country', 'self_control': '-', 'v': 'hedonism, stimulation', 'world': {'tribal': 'feast every night of the summer with the chiefs who now send for the teller', 'magic': 'revel every night of the season with the great families who now send for the player'}, 'chance': 0.11}),
    ('take the show on tour to the towns that never get one', 'G1', None, 0.45, '', {'grants': 'known across the country', 'v': 'benevolence, tradition', 'world': {'tribal': 'carry the telling to the far bands that never hear one', 'magic': 'take the play on the road to the towns that never see one'}, 'chance': 0.11}),
    ('go back to small work in the theatre where it all began', 'W.34 U.33 G.33', None, 0.5, '', {'mark': 'came home', 'v': 'tradition, achievement', 'world': {'tribal': 'go back to the small fire where the telling began', 'magic': 'go back to the little playhouse where it all began'}, 'chance': 0.72}),
    ('stay with the company for the next season, as promised', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'kept your word', 'binds': True, 'v': 'benevolence, conformity', 'world': {'tribal': "stay with the band's tellers for the next summer, as promised"}, 'chance': 0.74}),
    ('move the show to the biggest theatre in the capital at once', 'W.34 B.33 R.33', None, 0.5, '', {'door': True, 'v': 'power, stimulation', 'world': {'tribal': 'take the telling to the great fire of all the bands at once', 'magic': 'move the play to the grandest playhouse in the capital at once'}, 'chance': 0.7}),
    ("take the credit in interviews for the company's best ideas", 'U.34 B.33 R.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: taking credit for others' work; backfire: the designer tells the papers whose ideas they were", 'v': 'power, achievement', 'world': {'tribal': "take the praise at every fire for the other tellers' best moments", 'magic': "take the credit with the broadsheets for the company's best ideas"}, 'chance': 0.7}),
    ('sign with a producer for the next three shows', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'a producer who backs you', 'v': 'security, achievement', 'world': {'tribal': "give the next three summers' tellings to a chief who will feast every teller", 'magic': 'sign with a patron for the next three plays'}, 'chance': 0.7}),
 ]},
{'name': 'the lead from the open queue',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.008, 0.006, 0.004, 0.002),
 'drivers': 'era+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, performing, meaning',
 'horizon': 'week',
 'roles': 'friend, rival, partner, a casting assistant',
 'requires': 'professional actor | voice actor | understudy | amateur actor',
 'worlds': {'earth': 'an open call for the lead of a big new musical that wants a new face, and a queue of working '
                     'actors and local leads by dawn',
            'tribal': "the elders will give the great mask to whichever of the bands' players dances the first "
                      "ancestor best at the gathering's first fire",
            'magic': "the master of revels will hear any player of the realm's companies and guild stages for the "
                     'hero of the midsummer masque'},
 'timing': {'times': 'per working actor, understudy or long-standing amateur lead a year: about 1 in 150 queues at '
                     'an open call for the lead of a big new show that wants a new face (estimate); open casting '
                     'days for such a lead can draw several thousand hopefuls for one part (press reports of open '
                     "calls; estimate), so a hopeful's real odds are well under 1 in 100, written here at 2 in 100",
            'likelier': "a new musical or film that wants a new face, a city within a day's travel, a boom in new "
                        'productions, years of singing and dancing kept up',
            'rarer': 'a part already promised to a star, a show that will not release its cast for the day, no money '
                     'for the train',
            'gap_years': (5.0, 12.0)},
 'scenes': {'earth': [('',
                       'A big new musical, bound for the largest theatre in the capital, wants a new face for its '
                       'lead and holds open auditions in five cities: sixteen bars of a song and a minute of speech. '
                       'By six in the morning the queue goes twice round the block: actors between jobs, '
                       'understudies on their day off, the best of a hundred local companies. Everyone in it gets a '
                       'number.'),
                      ('W',
                       "The call's rules are printed on the website, and {N} has read them three times: sixteen "
                       'bars, plain clothes, doors at nine. If there is a fair way through four thousand people, it '
                       'is to be exactly what they asked for.'),
                      ('U',
                       "{N} has listened to the show's songs until the lead's whole story is in them: where the part "
                       'starts, where it breaks, what it wants. Two minutes is long enough to show one true thing, '
                       'if it is the right one.'),
                      ('B',
                       'Four thousand people, and perhaps forty will get past the first room. {N} watches which '
                       'faces the casting assistants remember, and works out who in the building actually decides.'),
                      ('R',
                       '{N} has played every kind of part but this one, and has never wanted anything so simply. '
                       'Somewhere at the front of this queue is a room, and for two minutes in it {N} will be the '
                       'only person in the world.'),
                      ('G',
                       '{friend} came along with a flask and sandwiches, and half the queue are players from towns '
                       'like {Ns} own: the lead of the valley players, two from a touring company, a woman who has '
                       'sung the same pantomime for twenty years. Whatever happens, it is a day none of them will '
                       'forget.')],
            'tribal': [('',
                        'The elders have said it at every fire: this summer the great mask of the first ancestor '
                        "goes to whichever of the bands' players dances him best at the gathering's first fire. By "
                        'dusk the players of every band are pressed round the fire, and those who want it wait their '
                        'turn in the dark.')],
            'magic': [('',
                       "The master of revels has had it cried at every company's door and every guild stage of the "
                       'realm: the hero of the midsummer masque will be chosen from among their players, known or '
                       'not. The line to the hall winds across the square, and a herald gives each player a painted '
                       'tally.')]},
 'outcomes': (['The recalls come one after another, a second room, a third, a fifth, and then a phone call on a '
               'Tuesday night that {N} will repeat word for word for the rest of {Ns} life.',
               'Whatever {N} chose to do with the day, it was the right size of step, and {N} goes home tired and '
               'glad.'],
              ['{N} walks home in the dark with the number still pinned on, sings the sixteen bars once more under '
               'the railway bridge, and keeps the number in a drawer for years.',
               'The casting assistant calls it lovely and plainly means it; on the train home {N} works out the '
               'whole thing lasted ninety seconds, and that {N} would do it again tomorrow.']),
 'options': [
    ('queue from dawn, and give them exactly the song and the speech the call asked for', 'W1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity', 'world': {'tribal': 'wait your turn at the first fire, and play the ancestor exactly as the old tellings set him', 'magic': 'wait for your tally to be called, and give the master exactly the piece the crier named'}, 'chance': 0.02}),
    ('learn the whole story of the part from its songs, and play that in two minutes', 'U1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'learn every telling of the first ancestor, and play the one that is truest', 'magic': 'learn the hero from the old ballads, and play that in two minutes'}, 'chance': 0.02}),
    ('talk your way up the queue, and make sure the casting director learns the name', 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'talk your way to the front of the waiting, and make sure the elders know your hearth', 'magic': 'talk your way up the line, and make sure the master of revels learns your name'}, 'chance': 0.02}),
    ('walk in and sing it as if the theatre were already full', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'identity': True, 'v': 'stimulation, hedonism', 'world': {'tribal': 'leap into the firelight and dance the ancestor as if every clan were already roaring', 'magic': 'walk in and play the hero as if the whole court were already watching'}, 'chance': 0.02}),
    ('sing the old song from home, the way the old people there still sing it', 'G1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'play the ancestor the way the old ones of your band have always told him', 'magic': 'sing the old song of your village, the way the old folk still sing it'}, 'chance': 0.02}),
    ('leave your details with the casting office, and pay for a listing in the directory', 'B.5 G.5', None, 0.5, '', {'grants': 'casting directory listing', 'v': 'security, achievement', 'world': {'tribal': "ask the elders' go-between to remember your hearth for the tellings to come", 'magic': 'pay the brokers to put your name on their roll for the next masque'}, 'chance': 0.85}),
    ('go to every open call this year, and learn to own a room in two minutes', 'B.5 R.5', None, 0.5, '', {'grants': 'auditioning', 'habit': True, 'v': 'stimulation, achievement', 'world': {'tribal': "play before every band's elders who will watch this summer, and learn to own the fire", 'magic': 'try before every company that holds trials this year, and learn to own a room'}, 'chance': 0.85}),
    ("learn the show's other parts on your own, in case the call comes round again", 'U.5 R.5', None, 0.5, '', {'grants': 'learning lines', 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'learn every other part of the telling by heart, in case the mask is offered again', 'magic': "learn the masque's other parts by heart, in case the master calls again"}, 'chance': 0.85}),
    ('go home to your own company, and give it your best season yet', 'W.5 G.5', None, 0.5, '', {'grants': 'a company that feels like family', 'v': 'tradition, benevolence', 'world': {'tribal': "go home to your own band's players, and give them your best winter of tellings", 'magic': 'go home to your own company, and give it your best season yet'}, 'chance': 0.85}),
    ('ask the casting assistant what the panel looks for, and work on it for a year', 'W.5 U.5', None, 0.5, '', {'aims': 'lead actor or actress', 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': "ask the elders' helper what the elders look for, and work on it until next summer", 'magic': 'ask the herald what the master looks for, and work on it until next midsummer'}, 'chance': 0.85}),
 ]},
{'name': 'filmed by chance in the street',
 'stages': 'young_adult adult mature',
 'age': (18, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0008, 0.0006, 0.0003, 0.0),
 'drivers': 'era+.3 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, performing, money',
 'horizon': 'week',
 'roles': 'friend, partner, colleague, a casting director, an agent',
 'requires': 'amateur actor | background artist | amateur band member | name on the local scene | a cult following',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': "a stranger films the person's street act, the clip goes round the country, and the messages "
                     'start',
            'tribal': 'a teller from another band sees the person play at the river crossing, and carries the '
                      'telling to every fire in the valley',
            'magic': "an illusionist catches the person's act in a scrying glass at the market, and the glass is "
                     'shown in the great houses'},
 'timing': {'times': 'per busker, band player, street player, extra or local player with years of performing in '
                     "public, a year: about 1 in 1,500 has a stranger's clip of the act spread far enough for the "
                     'trade to call (estimate); clips of street acts are filmed and shared every day, and only a '
                     'handful a year turn into paid parts (estimate)',
            'likelier': 'an act people stop for, a busy square or station, a year when clips travel fast, a friend '
                        'who knows how to share them',
            'rarer': 'a quiet town, an act that only works live, a performer who seldom plays in public',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'On a Saturday in the square {N} does the act {N} has done for years, for the shoppers and '
                       'the pigeons and whoever stops. A stranger films two minutes of it on a phone. By Wednesday '
                       'the clip has been watched four million times, and {Ns} messages are full: a casting '
                       'director, a voice studio, an agent, a company that tours physical theatre, and every regular '
                       'from the square asking if it is true.'),
                      ('W',
                       '{N} answers nobody for a day, and makes a list instead: who wrote, what they want, which '
                       'offers are real. Somebody has to keep a clear head in all this, and it may as well be {N}.'),
                      ('U',
                       '{N} watches the clip forty times with the sound off and then with it on, to see what the '
                       'four million saw. There is something in the last minute that {N} never knew was there.'),
                      ('B',
                       'Attention like this lasts about a fortnight. {N} sorts the messages by who has money and who '
                       'has power, and starts with the second list.'),
                      ('R',
                       '{N} reads the messages on the bus home, laughing out loud. Years on the cold stones of the '
                       'square, and now everyone wants the act exactly as it is.'),
                      ('G',
                       'The regulars from the square have all seen it: the flower seller, the man with the dog, the '
                       'kids who dance along with a parent close by. They are in the clip too, at the edges, and '
                       'they are prouder than {N} is.')],
            'tribal': [('',
                        'A teller from another band watched {N} play at the river crossing, and has carried the '
                        'telling to every fire in the valley. Now runners come from three bands at once: the elders '
                        'of the gathering want to see this player, and so does the keeper of the hidden voices.')],
            'magic': [('',
                       'An illusionist caught {Ns} market act in a scrying glass, and the glass has been shown in '
                       'every great house in the city. Letters come under strange seals: a company master, a puppet '
                       'theatre, a broker, a troupe of masquers that tours the river towns.')]},
 'outcomes': (['Within a month {N} has a contract, a rehearsal room and a start date, and the square throws a party '
               'on the last Saturday.',
               'Whatever {N} chose, the clip turns out to be the beginning of something rather than the whole of '
               'it.'],
              ["The messages stop after nine days, another clip takes the country's attention, and {N} plays the "
               'square on Saturday to a crowd that never saw it.',
               '{N} goes to the audition in a borrowed jacket, hears the director call the act "pure gold, just not '
               'for us", and laughs about it all the way home.']),
 'options': [
    ('answer the casting director by return, and audition for the ensemble properly', 'W1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': "answer the elders' runner at once, and play before them as a teller-player should", 'magic': 'answer the company master by return, and try for a place in the company properly'}, 'chance': 0.03}),
    ('send the voice studio a clean recording of every voice in the act', 'U1', None, 0.45, '', {'title': 'voice actor', 'requires': 'amateur actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'go to the keeper of the hidden voices, and give every voice in the act behind the screen', 'magic': 'go to the puppet theatre, and give every voice in the act through the speaking-stone'}, 'chance': 0.03}),
    ('sign with the agent who wrote first, and hold out for a part in a series', 'B1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "let the go-between speak for you, and hold out for a place among the gathering's players", 'magic': 'sign with the broker who wrote first, and hold out for a part with a great company'}, 'chance': 0.03}),
    ('say yes to the touring company, and leave with them on Monday', 'R1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'say yes to the travelling players of the valley, and leave with them at dawn', 'magic': "say yes to the masquers' wagons, and leave with them on market day"}, 'chance': 0.03}),
    ('take the regulars from the square along, and audition as a company', 'G1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'made a friend', 'v': 'benevolence, tradition', 'world': {'tribal': 'take the friends who play beside you at the crossing, and go before the elders together', 'magic': 'take the market regulars along, and try for the company together'}, 'chance': 0.03}),
    ('keep playing the square every Saturday, and set your sights on a real stage', 'R.5 G.5', None, 0.5, '', {'aims': 'professional actor', 'habit': True, 'v': 'hedonism, tradition', 'world': {'tribal': "keep playing at the river crossing, and set your sights on the gathering's fire", 'magic': 'keep playing the market every feast day, and set your sights on a real stage'}, 'chance': 0.84}),
    ('cut the clip into a proper showreel, and send it to every casting office', 'U.5 B.5', None, 0.5, '', {'grants': 'a showreel', 'v': 'achievement, power', 'world': {'tribal': 'work the act into a telling the bands will ask for again and again', 'magic': 'have the glass copied into a glamour-reel, and send it to every company'}, 'chance': 0.84}),
    ('go for coffee with the casting director who wrote, and mostly listen', 'U.5 G.5', None, 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'self-direction, benevolence', 'world': {'tribal': "sit with the elders' runner at the crossing, and mostly listen", 'magic': 'take supper with the company master who wrote, and mostly listen'}, 'chance': 0.84}),
    ('sign with a small agency, after reading every line of the contract', 'W.5 B.5', None, 0.5, '', {'grants': 'an agent who believes in you', 'self_control': '+', 'v': 'security, achievement', 'world': {'tribal': 'take a go-between from a band you trust, after the elders hear the terms', 'magic': 'sign with a small broker, after reading every line of the contract'}, 'chance': 0.84}),
    ('say no to all of it, and keep the act free on the street', 'W.5 R.5', None, 0.5, '', {'mark': 'turned down a chance', 'identity': True, 'v': 'self-direction, universalism', 'world': {'tribal': 'send the runners home, and keep the act for anyone at the crossing', 'magic': 'send the letters back, and keep the act free in the market where it belongs'}, 'chance': 0.84}),
 ]},
{'name': 'the film you made with friends',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.006, 0.004, 0.002, 0.001),
 'drivers': 'era+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'making, friends, work',
 'horizon': 'months',
 'roles': 'friend, partner, colleague, mentor, rival',
 'requires': 'novelist | journalist | writing stories | writing scripts',
 'tenure': (4.0, 99.0),
 'worlds': {'earth': "a short film made from the person's own script over three weekends with friends and a phone, "
                     "and a festival's open submissions closing in a week",
            'tribal': "a shadow telling of the person's own making played with friends on the cave wall, and the "
                      "gathering's keeper choosing which new tellings will play at the great fire",
            'magic': "a mirror-play of the person's own writing caught in a scrying glass with friends, and the "
                     "court's revels choosing which new plays will be shown"},
 'timing': {'times': 'per person who has written for years and has a stage or screen history, a year: about 1 in 200 '
                     'makes a short film from their own script with friends and sends it to a festival (estimate); '
                     'the biggest independent film festivals receive over ten thousand films a year and show about 1 '
                     'or 2 in 100 (festival figures, approximate), and far fewer of their writers are taken on for a '
                     'feature script (estimate)',
            'likelier': 'years of writing behind it, a phone with a good camera, friends who will give three '
                        'weekends, a year when festivals look for new voices',
            'rarer': 'no friends with the time, the festival fees, a busy family life',
            'gap_years': (5.0, 12.0)},
 'scenes': {'earth': [('',
                       'Over three weekends {N} and four friends made a short film on a phone from a script {N} '
                       "wrote: borrowed lights, a kitchen for every set, a neighbour's car for the chase. Now it is "
                       "finished, eleven minutes long, and the biggest festival's open submissions close on Friday. "
                       'Last year it took forty films out of four thousand.'),
                      ('W',
                       "{N} has a checklist for the festival's forms: the running time, the subtitles, a signed "
                       'release from everyone in the film. If it goes in, it goes in properly.'),
                      ('U',
                       '{N} has written for years, but never before heard the words played back by people who '
                       'believed them. The cut could be tighter in the middle, and the last shot says everything the '
                       'script meant.'),
                      ('B',
                       'A festival is a market as much as a party. {N} has worked out which producers go to the '
                       'short-film screenings, and which of them are looking for writers.'),
                      ('R',
                       'The film is rough and strange and alive, and {N} loves it more than anything {N} has '
                       'written. The thought of strangers seeing it in the dark is almost too much.'),
                      ('G',
                       'Everyone in it is someone {N} loves: {Ns} oldest friend, a cousin, the old man from the '
                       'corner shop as the grandfather. The whole street turned out for the chase.')],
            'tribal': [('',
                        'Over a moon of nights {N} and four friends made a new shadow telling of {Ns} own on the '
                        'cave wall: hands for the wolf, a burning stick for the moon, the old woman of the next '
                        'hearth as the grandmother. The keeper of the gathering will choose which new tellings play '
                        'at the great fire.')],
            'magic': [('',
                       'Over three market days {N} and four friends caught a play of {Ns} own writing in a scrying '
                       "glass: borrowed lamps, a kitchen for every scene, a neighbour's cart for the chase. The "
                       "court's master of revels will choose a few new mirror-plays to show at the summer revels.")]},
 'outcomes': (['A letter comes in the spring: the film is in, and after the screening a producer waits in the foyer '
               'with a card and a question about what {N} wants to write next.',
               'Whatever {N} chose, the film finds its people, and the friends who made it talk about those three '
               'weekends for years.'],
              ["The festival's letter is short and kind: four thousand films, room for forty, and one line of real "
               'praise for the last scene, which {N} reads a hundred times.',
               '{N} sits in the back row of a small screening to eleven people, three of them in the film, and claps '
               'loudest when the credits roll.']),
 'options': [
    ('enter it in every festival with an open door, the script attached, every form filled', 'W1', None, 0.45, '', {'title': 'playwright or screenwriter', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': 'bring it to the keeper on the right night, every part told exactly as the elders ask', 'magic': 'send it to the court and every great house that shows new plays, every seal in order'}, 'chance': 0.02}),
    ("send the script to a studio's new writers' scheme, with the film as proof", 'U1', None, 0.45, '', {'title': 'playwright or screenwriter', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'carry the telling to the oldest teller of the gathering, and ask to make new tellings for the clans', 'magic': "send the play to the court's play-makers, with the glass as proof"}, 'chance': 0.02}),
    ('show the short to the producer who buys scripts, and pitch the feature', 'B1', None, 0.45, '', {'title': 'playwright or screenwriter', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'show it to the great families, and offer them a great telling of your own making', 'magic': 'show it to the play-merchants, and offer them a full play of your own writing'}, 'chance': 0.02}),
    ("take it to the festival's midnight strand, and pitch the strange feature that comes next", 'R1', None, 0.45, '', {'title': 'playwright or screenwriter', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'identity': True, 'v': 'stimulation, self-direction', 'world': {'tribal': "play it at the gathering's last fire, and offer the strange telling that comes next", 'magic': "show it at the revels' midnight hour, and offer the strange play that comes next"}, 'chance': 0.02}),
    ('write the next film for the same friends, and send the two in together', 'G1', None, 0.45, '', {'title': 'playwright or screenwriter', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'make a second telling for the same friends, and bring the two to the keeper together', 'magic': 'write a second play for the same friends, and send both glasses together'}, 'chance': 0.02}),
    ('sell it to the local channel for a small fee, and share the money out', 'B.5 G.5', None, 0.5, '', {'grants': 'contact in the trade', 'mark': 'kept your word', 'v': 'security, benevolence', 'world': {'tribal': 'give the telling to a neighbouring band for a gift, and share the gift among the players', 'magic': "sell the glass to a tavern's showman for a few coins, and share them out"}, 'chance': 0.82}),
    ('cut it again for a month, until every second earns its place', 'U.5 B.5', None, 0.5, '', {'grants': 'editing', 'self_control': '+', 'v': 'achievement', 'world': {'tribal': 'tell it again and again for a moon, cutting every move that does not earn its place', 'magic': 'recut the glass for a month, until every scene earns its place'}, 'chance': 0.82}),
    ('start the next script the same night, while the friends are still keen', 'U.5 R.5', None, 0.5, '', {'grants': 'writing scripts', 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'start the next telling that same night, while the friends are still keen', 'magic': 'start the next play that same night, while the friends are still keen'}, 'chance': 0.82}),
    ('show it free in the community hall, with the whole street in the audience', 'W.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence, universalism', 'world': {'tribal': "show it free at your own band's fire, with every hearth watching", 'magic': "show it free in the ward's hall, with the whole lane watching"}, 'chance': 0.82}),
    ('put it online for anyone to see, and answer every comment', 'W.5 R.5', None, 0.5, '', {'grants': 'following online', 'v': 'universalism, stimulation', 'world': {'tribal': 'play it at every fire that asks, and answer every question the young ones have', 'magic': 'let the glass be shown in every tavern that asks, and answer every letter'}, 'chance': 0.82}),
 ]},
{'name': 'the old theatre needs someone to save it',
 'stages': 'adult mature elder',
 'age': (28, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.0, 0.005, 0.006, 0.004),
 'drivers': 'community+.3 prosper-.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, work, publiclife',
 'horizon': 'years',
 'roles': 'friend, neighbour, elder, colleague, rival',
 'requires': 'community theatre director | director',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'the old theatre on the high street is to close, and its trust will hand it to whoever brings a '
                     'plan the town will back',
            'tribal': "the painted cave where the band's tellings have been played for generations is to be left, "
                      'unless someone will keep it',
            'magic': 'the old playhouse by the river has lost its licence and its patron, and the guild will give it '
                     'to whoever can keep it open'},
 'timing': {'times': 'per director or long-serving community theatre director a year: about 1 in 200 sees an old '
                     'theatre in their own town close and offers to run it (estimate); every year a few dozen old '
                     'theatre buildings in a country the size of the UK stand at risk of closing, and some are saved '
                     'by local trusts (estimate); 1,953 US nonprofit theatres (theatre facts, 2019) each change '
                     'their artistic director about once in ten years, almost always for a professional (estimate)',
            'likelier': 'a town with a live amateur scene, a trust that would rather hand the building on than sell '
                        'it, years of directing in the town',
            'rarer': 'a building already sold to a developer, a town with no money to give, a person with no time to '
                     'give it',
            'gap_years': (8.0, 20.0)},
 'scenes': {'earth': [('',
                       'The old theatre on the high street, a hundred and twenty years old, is to close: the grant '
                       'has gone and the trust that ran it cannot pay for the roof. At a public meeting in the '
                       'stalls the chair says the trust will hand the building to whoever brings a plan the town '
                       'will back, and someone in the third row says {Ns} name: the person who has directed the '
                       "town's plays for years."),
                      ('W',
                       '{N} has sat on enough committees to know what the trustees will ask: the money, the roof, '
                       'the insurance, the next five years. A theatre is an institution, and an institution needs '
                       'someone to answer for it.'),
                      ('U',
                       '{N} has always known what the old place could be: new plays, the work nobody else will risk, '
                       'a room where the town meets things it has never seen.'),
                      ('B',
                       'A building, an audience and a name over the door, going for nothing to whoever moves first. '
                       '{N} can see exactly what it could be worth, and to whom.'),
                      ('R',
                       '{N} saw a first play in this room at nine years old and has never got over it. The thought '
                       'of the lights going out for good is unbearable.'),
                      ('G',
                       '{Ns} grandparents courted in the back row of the gallery, and every pantomime of {Ns} '
                       "childhood was here. It is the town's own, and the town should keep it.")],
            'tribal': [('',
                        'The band is moving its winter camp downriver, and the painted cave where the tellings have '
                        'been played for longer than anyone remembers is to be left to the bears. At the last fire '
                        "there an elder asks who will keep it, and the faces turn to {N}, who has led the band's "
                        'tellings for years.')],
            'magic': [('',
                       'The old playhouse by the river has lost its licence and its patron in the same season, and '
                       'the guild will give the house to whoever can keep it open. At the meeting in the pit, '
                       "someone calls out the name of {N}, who has staged the ward's plays for years.")]},
 'outcomes': (['The trustees vote on a wet Thursday, and by the autumn the posters outside the old theatre carry a '
               'new season and {Ns} name.',
               'Whatever {N} chose, the old building stays a theatre, and {N} is glad of the part played in keeping '
               'it one.'],
              ['The vote in the stalls goes the other way by nine hands, and {N} walks out under the old chandelier '
               'knowing every one of those faces, and still nods to each of them in the street.',
               'The trustees choose a director from the city, and thank {N} from the stage, in front of the whole '
               'town, for the plan that kept the doors open long enough.']),
 'options': [
    ('put a full plan before the trustees, budget and seasons, and apply to run it', 'W1', None, 0.45, '', {'title': 'artistic director; director', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'security, conformity', 'world': {'tribal': 'lay a plan before the elders for keeping the cave and its tellings, and ask to keep them', 'magic': 'put a full plan before the guild, purse and seasons, and ask to be master of the house'}, 'chance': 0.02}),
    ('propose it as a house for new work, with a first season nobody else would risk', 'U1', None, 0.45, '', {'title': 'artistic director; director', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'offer to keep the cave for new tellings nobody else would dare', 'magic': 'propose the house for new plays, with a first season nobody else would risk'}, 'chance': 0.02}),
    ('put your own savings into the lease, and book touring shows to make it pay', 'B1', None, 0.45, '', {'title': 'producer', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'savings', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "give your own winter stores for the keeping of the cave, and bring other bands' tellers there for gifts", 'magic': 'put your own coin into the lease, and book travelling companies to make it pay'}, 'chance': 0.02}),
    ('reopen it with the wildest season the town has ever seen, and run it yourself', 'R1', None, 0.45, '', {'title': 'artistic director; director', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'light the cave again with tellings nobody has dared, and keep it yourself', 'magic': 'reopen the house with the wildest season the city has seen, and run it yourself'}, 'chance': 0.02}),
    ("rally the town to buy it, and run it as the town's own theatre", 'G1', None, 0.45, '', {'title': 'artistic director; director', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'gather every hearth to keep the cave, and keep it for the band', 'magic': "rally the ward to buy the house, and run it as the city's own"}, 'chance': 0.02}),
    ('start a small company of your own, and rent the empty stage by the night', 'B.5 R.5', None, 0.5, '', {'grants': 'a company of your own', 'door': True, 'v': 'self-direction, power', 'world': {'tribal': 'gather a small band of players of your own, and use the cave when the band is away', 'magic': 'start a small company, and hire the dark house by the night'}, 'chance': 0.82}),
    ('gather every amateur group in town for one last show on the old stage', 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'benevolence, stimulation', 'world': {'tribal': "gather every hearth's players for one last telling in the cave", 'magic': "gather every guild's players for one last pageant in the old house"}, 'chance': 0.82}),
    ("write down the theatre's history with its oldest members, before the doors shut", 'U.5 G.5', None, 0.5, '', {'grants': 'telling a story aloud', 'mark': 'learned a skill', 'v': 'tradition, self-direction', 'world': {'tribal': 'learn every telling ever played in the cave from the oldest ones, before the band leaves', 'magic': "write down the house's history with its oldest players, before the doors shut"}, 'chance': 0.82}),
    ("sit on the trust's board, keep the books straight, and learn how a house is run", 'W.5 B.5', None, 0.5, '', {'grants': 'organising people', 'aims': 'artistic director', 'binds': True, 'v': 'security, conformity', 'world': {'tribal': 'sit with the elders who keep the cave, and learn how the keeping is done', 'magic': "sit on the house's board, keep the guild's books straight, and learn how a house is run"}, 'chance': 0.82}),
    ('back the best plan from someone else, and help them win the vote', 'W.5 U.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'back the best keeper the elders could choose, and help win the band over', 'magic': 'back the best master the guild could choose, and help win the vote'}, 'chance': 0.82}),
 ]},
{'name': 'the late starter',
 'stages': 'adult mature elder',
 'age': (35, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.002, 0.002, 0.001),
 'drivers': 'fortune+.2 money+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning, money',
 'horizon': 'months',
 'roles': 'partner, child, friend, colleague, mentor',
 'requires': 'amateur actor | background artist',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': 'children grown, a redundancy cheque, years on the local stage, and four adverts on the kitchen '
                     'table: a playhouse, an agency, a film and a touring company',
            'tribal': "too old for the long hunts, after years in the band's tellings, with the travelling players "
                      'of the valley looking for an old face for the oldest story',
            'magic': "the shop handed to the eldest, after years in the guild's mystery plays, and the companies' "
                     'notices for grey-haired players on the guild hall door'},
 'timing': {'times': 'per amateur actor or extra of 35 or more, a year: about 1 in 500 decides at last to try for '
                     'paid work in theatre or film (estimate); films and adverts cast real faces of every age, and '
                     'some theatres take older actors into their companies, but a first professional contract after '
                     'fifty is rare (estimate)',
            'likelier': 'children grown, a redundancy payment or a pension, a big birthday, years on the local '
                        'stage, a partner who says go on then',
            'rarer': 'money owed, a family that needs the time, poor health, a town far from any theatre',
            'gap_years': (8.0, 20.0)},
 'scenes': {'earth': [('',
                       'The children have left home, the job has ended with a cheque and a handshake, and {N} has '
                       'played at the local theatre for years, always for nothing. On the kitchen table lie adverts '
                       'cut from the papers: a playhouse that wants older actors for its company, an agency that '
                       'takes on mature actors, a film that wants real faces over fifty, and a touring company that '
                       'casts local people in every town.'),
                      ('W',
                       '{N} has been word-perfect for the players every season for years, and has never missed a '
                       'rehearsal. A theatre that pays would get exactly that, if anyone in one would believe it.'),
                      ('U',
                       '{N} has wondered for years what a whole life would look like on a stage, told by the person '
                       'who lived it. There is a one-person show in the notebooks on the shelf, if anyone would let '
                       'it be played.'),
                      ('B',
                       '{N} spent a working life selling and making deals, and knows that in any business the first '
                       "door is the agent's. An agency that takes on older actors needs to see a sure thing, and {N} "
                       'can be one.'),
                      ('R',
                       '{N} reads the advert for real faces over fifty and laughs out loud. A whole life of wanting '
                       'it, and now the face is the qualification.'),
                      ('G',
                       '{N} knows every village hall and every player in the valley from years on the local stage. A '
                       'touring company that casts local people in every town needs exactly someone like that, and '
                       'the valley would come to see it.')],
            'tribal': [('',
                        "Too old now for the long hunts, {N} sits at the gathering's fires and watches the tellings, "
                        'as {N} has played in them for years. The travelling players of the valley want an old face '
                        'for the oldest story, and a voice that knows every fire.')],
            'magic': [('',
                       "The shop has gone to the eldest child, and {N}, who has played in the guild's mystery plays "
                       "for years, stands at the guild hall's door where the notices hang: grey heads wanted for a "
                       "river company, a broker taking on older players, the court's great masque.")]},
 'outcomes': (['A letter comes three weeks later with a start date, and {N} stands in the kitchen reading it aloud '
               'to nobody, twice.',
               'Whatever {N} chose, the late start was a real one, and the years that follow have a stage in them '
               'somewhere.'],
              ['{N} is the oldest in the waiting room by thirty years, plays the scene well, gets a kind no, and '
               'sits outside in the sun afterwards with a coffee, oddly pleased to have been there at all.',
               'The answer is a letter that praises the nerve and the years on the local stage in one honest '
               'sentence, and gives the place to someone with twenty years in the trade.']),
 'options': [
    ("answer the playhouse's call for older company members, with years of local shows behind", 'W1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': "offer yourself to the travelling players, with years of the band's tellings behind", 'magic': "answer the river company's notice for grey heads, with years of mystery plays behind"}, 'chance': 0.03}),
    ('write a one-person show from your own life, and offer it to the playhouse', 'U1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'make a telling from your own life, and offer it to the travelling players', 'magic': 'write a one-player piece from your own life, and offer it to the river company'}, 'chance': 0.03}),
    ('talk your way onto the books of an agency for older actors', 'B1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "offer the travelling players' speaker a share of your gifts, and ask for a place", 'magic': "talk your way onto a broker's roll of older players"}, 'chance': 0.03}),
    ('send the film a minute of your own face, for one of the older parts', 'R1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'dance the oldest story for the travelling players, as the old one in it', 'magic': "go before the master of revels for the old king's part in the great masque"}, 'chance': 0.03}),
    ("audition with the valley's players for the touring company that casts local people", 'G1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'go before the travelling players with the old ones of your band, together', 'magic': 'try for the river company with the old players of your ward, together'}, 'chance': 0.03}),
    ('take a short acting course first, and audition when ready', 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'acting', 'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': 'sit with the old teller through one winter first, and play when ready', 'magic': 'take a season of lessons with an old player first, and try when ready'}, 'chance': 0.82}),
    ('volunteer front of house at the playhouse, and learn how the building really works', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'achievement, benevolence', 'world': {'tribal': "help at the gathering's fires, and learn how the tellings are really made", 'magic': "help in the playhouse's lobby, and learn how the house really works"}, 'chance': 0.82}),
    ('build and paint the sets for the local players on Saturdays', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'stagecraft', 'habit': True, 'v': 'security, benevolence', 'world': {'tribal': "make the masks and the screens for the band's tellings", 'magic': "build and paint the pageant wagons for the guild's players"}, 'chance': 0.82}),
    ('be an extra on the film for a day, and watch how it is made', 'U.34 R.33 G.33', None, 0.5, '', {'title': 'background artist', 'v': 'stimulation, tradition', 'world': {'tribal': "walk as one of the old ones in the travelling players' procession, and watch how it is made", 'magic': "walk among the grey heads in the masque's crowd, and watch how it is made"}, 'chance': 0.82}),
    ('let it rest: the cheque goes to the family, and the dream stays a dream', 'U.34 B.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, benevolence', 'world': {'tribal': 'let it rest: the winter stores go to the family, and the tellings stay a dream', 'magic': 'let it rest: the coin goes to the family, and the stage stays a dream'}, 'chance': 0.82}),
 ]},
{'name': 'the night both covers are off',
 'stages': 'young_adult adult mature elder',
 'age': (18, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.004, 0.003, 0.002, 0.001),
 'drivers': 'fortune+.4 prosper+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, performing',
 'horizon': 'moment',
 'roles': 'colleague, boss, friend, a company manager',
 'requires': 'professional actor | understudy | drama school student | stage manager | stage technician | calling '
             'the show | sound engineer',
 'worlds': {'earth': 'the lead and the cover both off with the same winter flu, a full house in, and the company '
                     'manager looking for anyone who knows the words',
            'tribal': 'the wearer of the great mask and the one who learned it both lie sick, and the gathering '
                      'waits at the fire',
            'magic': 'the leading player and the second both down with the same fever, the court in the boxes, and '
                     'the master of the play looking along the wings'},
 'timing': {'times': 'per actor, student on placement or crew member of a running show, a year: about 1 in 300 is in '
                     'the building on a night when both the lead and the cover are off (estimate); most shows then '
                     'cancel or send on a second cover, and someone who steps in is very seldom kept on as the lead '
                     '(estimate)',
            'likelier': 'a winter flu in the company, a long run with a small cast, a person who has watched every '
                        'show from the wings',
            'rarer': 'a big show with two covers for every part, a short run, a person who never learns anyone '
                     "else's lines",
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'The same winter flu took the lead on Tuesday and the cover on Thursday, and on Thursday '
                       'night the house is full. At the half the company manager walks the corridor asking everyone '
                       'the same question: does anyone know the words? {N} has watched every show for a year, from '
                       'the wings, the booth or the back of the ensemble, and knows every line.'),
                      ('W',
                       'There is a procedure for this, and the procedure says cancel. But {N} knows the part as well '
                       'as the blocking, and a full house is waiting.'),
                      ('U',
                       '{N} has run the part silently every night for a year, out of habit: every cue, every breath, '
                       'the turn in the second act that the lead always rushes.'),
                      ('B',
                       'The producer is in tonight with two investors, and somebody is going to save this show. {N} '
                       'can see exactly what that would be worth.'),
                      ('R',
                       '{Ns} heart is going like a drum. Nobody has asked yet, and {N} is already halfway to the '
                       'dressing room.'),
                      ('G',
                       'The company has been like a family all year: the dressers, the band, the old hands in the '
                       'chorus. If the show goes up tonight, it goes up for them.')],
            'tribal': [('',
                        'The wearer of the great mask lies sick in his shelter, and the one who learned the telling '
                        'lies sick beside him. The gathering waits at the fire, and the keeper of the masks looks '
                        'along the line of players and helpers for anyone who knows the words.')],
            'magic': [('',
                       'The leading player and the second are both abed with the same fever, and the court is '
                       'already in the boxes. The master of the play walks the wings asking every player and every '
                       'hand: does anyone know the part?')]},
 'outcomes': (['The producers come round after the curtain call, and by the Monday {N} has a contract for the lead '
               'for the rest of the run.',
               'Whatever {N} chose, the night is saved one way or another, and the company remembers who saved it.'],
              ['{N} gets through every scene, the house stands at the end, and on Monday the lead is back and {N} is '
               'back in the company with a story nobody outside will believe.',
               'Halfway through the first act a line goes, the prompt comes from the corner, and the notes the next '
               'day are kind and very short.']),
 'options': [
    ('go on word-perfect, and play it exactly as the director set it', 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'professional actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity', 'world': {'tribal': 'take up the great mask, and play the telling exactly as the elders set it', 'magic': "step out in the leading player's cloak, and play it exactly as the master set it"}, 'chance': 0.03}),
    ('go on, and play it the way a year of watching has shown it should go', 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'professional actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'take up the mask, and play the telling the way a year of watching has shown it', 'magic': 'step out, and play the part the way a season of watching has shown it'}, 'chance': 0.03}),
    ('offer to go on, if the producer promises a look at the next lead', 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'professional actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'offer to wear the mask, if the elders promise a look at the next great telling', 'magic': 'offer to go on, if the patron promises a look at the next leading part'}, 'chance': 0.03}),
    ('grab the costume and go on before anyone can say no', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'professional actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'take up the mask and step into the firelight before anyone can say no', 'magic': 'throw on the cloak and step out before anyone can say no'}, 'chance': 0.03}),
    ('go on for the company, so the people who built the show are not sent home', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'requires': 'professional actor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'take up the mask for the band, so the gathering is not sent away', 'magic': 'step out for the company, so the house is not sent home'}, 'chance': 0.03}),
    ('call the cancellation by the book, and see the house out kindly at the doors', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'tell the gathering by the old custom that there is no telling tonight, and feed them anyway', 'magic': 'send the house home by the book, and see every guest out kindly'}, 'chance': 0.82}),
    ('find the actor who played it on the last tour, at a fair fee for tonight', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "send a runner to the next band's player who once wore the mask, with a fair gift", 'magic': 'send for a player who knew the part at another house, with a fair purse'}, 'chance': 0.82}),
    ('go on for tonight only, and hand the part back on Monday with thanks', 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'a lead role to remember', 'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'take up the mask for tonight only, and hand it back at the next fire with thanks', 'magic': 'step out for tonight only, and hand the part back at the next bell with thanks'}, 'chance': 0.82}),
    ('coach the young ensemble player who also knows it, in the corridor before curtain', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'directing actors', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': 'walk the young player who also knows it through the telling, behind the screens', 'magic': 'coach the young player who also knows it, in the passage before the bell'}, 'chance': 0.82}),
    ('keep the house laughing out front, then ask to be the next cover', 'B.34 R.33 G.33', None, 0.5, '', {'aims': 'lead actor or actress', 'v': 'hedonism, achievement', 'world': {'tribal': 'keep the gathering laughing while the elders decide, then ask to learn the mask', 'magic': 'keep the galleries laughing before the curtain, then ask to be the next second'}, 'chance': 0.82}),
 ]},
{'name': 'the other side of the table',
 'stages': 'young_adult adult mature elder',
 'age': (23, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.006, 0.003),
 'drivers': 'era+.2 prosper+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, performing, meaning',
 'horizon': 'week',
 'roles': 'colleague, friend, mentor, a casting director, a director',
 'requires': 'professional actor',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'a casting director asks a working actor to read the other parts opposite the hopefuls for a '
                     'week, on the far side of the audition table',
            'tribal': 'the keeper of the masks asks a player of the gathering to speak the other parts while the '
                      'elders choose the players for the winter tellings',
            'magic': 'the master of revels asks a player of the companies to read the other parts in the great hall '
                     'while the players for the winter masque are chosen'},
 'timing': {'times': 'per professional actor of three years or more, a year: about 1 in 100 is asked to read the '
                     'other parts opposite the hopefuls at a week of casting (estimate); casting offices often hire '
                     'working actors as readers, and a reader who is offered a post on that side of the table, or a '
                     'part, is rare (estimate)',
            'likelier': 'a busy year for new series and shows, a casting director who remembers a good reader, years '
                        'of reliable work, a quick study',
            'rarer': 'a quiet year, a run that cannot spare the actor for a week, an actor who never learns anyone '
                     "else's lines",
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'For a week {N} sits on the other side of the table. The casting director of a new series '
                       'needs someone to read the other parts opposite the hopefuls, and asked for {N} by name. '
                       'Eighty actors a day come through the door, and {N} reads the same scene with every one of '
                       'them, and watches the director, the producer and the casting director decide in the first '
                       'ten seconds.'),
                      ('W',
                       '{N} keeps the list for the casting assistant without being asked: who came in, who was seen, '
                       'who should be called back. By Wednesday the casting director is asking {N} first.'),
                      ('U',
                       'By the third day {N} can tell what the director wants before the director can say it: the '
                       'scene turns on the pause in the middle, and almost nobody finds it.'),
                      ('B',
                       'The agents ring the casting office all day, and {N} hears every call. There is a whole trade '
                       'on this side of the table, and it runs on knowing whom to ring.'),
                      ('R',
                       'Eighty times a day {N} plays the other half of the scene, and on the fourth day {N} plays it '
                       'so well that the director looks up from the notes.'),
                      ('G',
                       'Most of the actors who come in are frightened, and many have come straight from drama '
                       'school. {N} gives each of them the best reading {N} can, the way someone once did for {N}.')],
            'tribal': [('',
                        'The elders are choosing the players for the winter tellings, and the keeper of the masks '
                        'asks {N} to speak the other parts opposite each of them. For four days {N} sits on the '
                        "elders' side of the fire, and watches how the choosing is done.")],
            'magic': [('',
                       'The master of revels is choosing the players for the winter masque, and asks {N} to read the '
                       "other parts opposite every hopeful in the great hall. For a week {N} stands on the master's "
                       'side of the boards, and watches how the choosing is done.')]},
 'outcomes': (['A week later the call comes, and it is the one {N} asked for; {N} says yes before the sentence is '
               'finished.',
               'Whatever {N} chose, the week on the other side of the table changes how {N} walks into every room '
               'after it.'],
              ['The week ends with thanks and a fee, the office goes with someone it already knew, and {N} goes back '
               'to auditioning, knowing now exactly what happens in the first ten seconds.',
               'The director says it was a great week, plainly means it, and goes another way; {N} keeps the scene '
               'in a coat pocket for years.']),
 'options': [
    ('ask the casting director for a place in the casting office, and start on Monday', 'W1', None, 0.45, '', {'title': 'casting director', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'ask the keeper of the masks to take you on as the one who helps the elders choose', 'magic': "ask the master of revels for a clerk's place at the choosing, and start at the next bell"}, 'chance': 0.03}),
    ('hand the director your notes on every reading, and ask for the next play to direct', 'U1', None, 0.45, '', {'title': 'director', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'tell the elders what each telling needed, and ask to lead the next one', 'magic': 'give the master your notes on every trial, and ask for the next masque to stage'}, 'chance': 0.03}),
    ("take the agents' calls, and set up your own agency with the best of the hopefuls", 'B1', None, 0.45, '', {'title': 'talent agent', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'become the go-between for the best of the young players, and speak for them at every fire', 'magic': 'set up as a broker of players, with the best of the hopefuls on your roll'}, 'chance': 0.03}),
    ('play the other half of the scene until the director casts you in the lead', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'speak the other part so well that the elders give you the great mask', 'magic': 'read the other part so well that the master gives you the hero of the masque'}, 'chance': 0.03}),
    ('give every frightened newcomer your best reading, and ask the drama school for a teaching post', 'G1', None, 0.45, '', {'title': 'drama teacher', 'grants_if_fails': 'a long shot that missed', 'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'give every frightened young player your best, and ask to teach the young ones of the bands', 'magic': 'give every frightened hopeful your best, and ask the guild school for a post teaching the young players'}, 'chance': 0.03}),
    ('ask to sit in on the whole casting, and learn how the choosing is really done', 'W.5 U.5', None, 0.5, '', {'grants': 'a casting eye', 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': 'ask to sit by the elders for every choosing, and learn how it is really done', 'magic': 'ask to sit beside the master for the whole choosing, and learn how it is really done'}, 'chance': 0.85}),
    ('coach the next nervous hopeful through the scene in the corridor, the way a director would', 'W.5 R.5', None, 0.5, '', {'grants': 'directing actors', 'v': 'stimulation, conformity', 'world': {'tribal': 'walk the next nervous player through the telling behind the screens, the way the elders would', 'magic': 'coach the next nervous hopeful through the scene in the passage, the way the master would'}, 'chance': 0.85}),
    ('go out with the agents and the producers after the last session, and make yourself remembered', 'B.5 R.5', None, 0.5, '', {'grants': 'contact in the trade', 'v': 'stimulation, power', 'world': {'tribal': 'sit late with the go-betweens of every band, and make yourself remembered', 'magic': 'drink with the brokers and the patrons after the last trial, and make yourself remembered'}, 'chance': 0.85}),
    ('offer to read in every season, for a fair fee and a seat at every choosing', 'B.5 G.5', None, 0.5, '', {'grants': 'a casting eye', 'v': 'power, tradition', 'world': {'tribal': "offer to speak the other parts at every gathering's choosing, as the old players always did", 'magic': "offer to read for the master at every season's choosing, for a fair purse and a seat in the hall"}, 'chance': 0.85}),
    ('start a free audition class on Sundays for the newcomers who were most afraid', 'U.5 G.5', None, 0.5, '', {'grants': 'teaching', 'habit': True, 'v': 'achievement, benevolence', 'world': {'tribal': 'teach the young players who were most afraid, by the fire on rest days', 'magic': 'teach a free class for the most frightened hopefuls, at the guild hall on feast days'}, 'chance': 0.85}),
 ]},
{'name': 'the lead is not in at the half',
 'stages': 'young_adult adult mature elder',
 'age': (17, 85),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague, boss',
 'requires': 'stage manager',
 'worlds': {'earth': 'the stage door at the half: the lead has not signed in, the phone goes to voicemail, and the '
                     'understudy has never had a full rehearsal',
            'tribal': 'the wearer of the great mask has not come to the fire, the moon is rising, and the one who '
                      'learned the telling has only ever practised it alone',
            'magic': 'the leading player is not in the playhouse at the first bell, and the second has never once '
                     'run the part with the company'},
 'timing': {'times': 'per stage manager a year: about 1 in 5 face a missing actor at the half (estimate); about 1 '
                     'life in 1,000 works as a stage manager (catalogue share; US union stage managers worked 55,423 '
                     "weeks in 2018-19, about 1,066 at work in an average week, the US stage union's report)"},
 'scenes': {'earth': [('',
                       'The half is called, thirty-five minutes to curtain, and the lead has not signed in at the '
                       'stage door. The phone goes to voicemail. The understudy, {colleague}, has only ever run the '
                       'part on a Thursday afternoon in an empty theatre, and the house is filling.'),
                      ('W',
                       'The procedure is on the first page of the prompt book: an actor absent at the half is '
                       'reported, the cover is called, the change is announced. {N} wrote that page.'),
                      ('U',
                       '{N} runs through what the cover has actually rehearsed: the scenes, the fight, and the quick '
                       'change in the second act that nobody has ever timed.'),
                      ('B',
                       '{boss}, the producer, is in the stalls tonight with two investors. Whatever happens next, '
                       'they will remember whose call it was.'),
                      ('R',
                       'The night tips toward disaster, and {N} feels a jolt of something close to glee: this is '
                       'what the job is for.'),
                      ('G',
                       'The company has been together all year, more like a family than a cast. The old dresser is '
                       'already making the cover a cup of sweet tea, and someone has found the lucky scarf.')],
            'tribal': [('',
                        'The fires of the gathering are lit and the moon is coming up over the ridge, and the wearer '
                        'of the great mask has not come. {N}, keeper of the fire and the masks, looks at '
                        '{colleague}, who learned the telling alone by the river and has never spoken it before the '
                        'band.')],
            'magic': [('',
                       "The first bell has rung in the playhouse, and the leading player's dressing room is empty. "
                       '{N}, the book-keeper, has the prompt-book open, and the second, {colleague}, waits in the '
                       'wings, pale as chalk.')]},
 'outcomes': (['The curtain goes up a few minutes late, and the cover gets through the night to a roar at the bow.',
               'The missing lead arrives breathless just before the start, and nobody watching ever knows.'],
              ['The cover loses the words in the second scene, and the rest of the night is held together with '
               'prompts.',
               'The show starts twenty minutes late, and {boss} wants a word with {N} afterwards.']),
 'options': [
    ('call the cover by the book, and have the change announced before curtain', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'give the sign to the one who learned the telling, and have the change told at the fire', 'magic': 'send the second on by the book, and have the herald cry the change'}, 'chance': 0.85}),
    ('talk the cover through every move of the first act in the half hour left', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'walk the young one through every turn of the telling while the moon rises', 'magic': 'walk the second through every entrance of the first act before the last bell'}, 'chance': 0.7}),
    ('ring the producer in the stalls, and make it their decision, on the record', 'B1', None, 0.45, '', {'v': 'security, power', 'world': {'tribal': 'go to the elder who gave the feast, and make it his choice before the band', 'magic': "send up to the play-merchant's box, and make it his decision before a witness"}, 'chance': 0.95}),
    ("read the part yourself, book in hand, in the lead's costume", 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'identity': True, 'world': {'tribal': 'take up the great mask yourself, and speak the telling from memory', 'magic': "step out yourself with the prompt-book in hand, in the leading player's cloak"}, 'chance': 0.55}),
    ('hold the curtain five minutes, and sit with the cover until the shaking stops', 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'let the moon wait a little, and sit with the young one by the river until the shaking stops', 'magic': 'hold the bell a little, and sit with the second until the shaking stops'}, 'chance': 0.7}),
    ('call the company onto the stage, and ask them to carry the cover together', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'call every player to the fire, and ask them to carry the young one through', 'magic': 'call the whole company onto the stage, and ask them to carry the second through'}, 'chance': 0.6}),
    ("rewrite the cues around the cover's moves, and call the show from them", 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'grants': 'calling the show', 'world': {'tribal': 'change the signs for each entrance to fit the young one, and give them from the fire', 'magic': "rewrite the book's cues around the second's moves, and call the changes from it"}, 'chance': 0.72}),
    ('ring an actor who played the part on tour, and offer cash to go on tonight', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "send a runner with a gift to the next band's player, who once wore the mask", 'magic': 'send a boy running with coin to a player who knew the part at another house'}, 'chance': 0.15}),
    ('go out front and win the house over, so nobody asks for a refund', 'R1', 'B.7', 0.5, '', {'v': 'achievement, hedonism', 'world': {'tribal': 'step into the firelight and make the band laugh while the young one is masked', 'magic': 'step before the curtain and charm the galleries, so nobody calls for their coin'}, 'chance': 0.8}),
    ('tell the cover the company will carry them, and to play it from the heart', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, benevolence', 'world': {'tribal': 'tell the young one the ancestors know the telling, and to let it come', 'magic': 'tell the second the company will carry them, and to play it from the heart'}, 'chance': 0.45}),
 ]},
{'name': 'the fit-up runs through the night',
 'stages': 'young_adult adult mature elder',
 'age': (17, 85),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague, boss',
 'requires': 'stage manager',
 'worlds': {'earth': 'a touring set arrives at a theatre too small for it, and the show opens tomorrow night',
            'tribal': 'the screens will not stand on the new ground of the gathering, and the telling is at dusk '
                      'tomorrow',
            'magic': "the wagon's stage will not fit the inn yard, and the town has paid for a play tomorrow night"},
 'timing': {'times': 'per stage manager on tour: most weeks of a tour (estimate)'},
 'scenes': {'earth': [('',
                       'The lorry backs into the dock at four in the afternoon, and by six it is plain: the touring '
                       'set is a metre too wide for this stage, and the show opens tomorrow at half past seven. The '
                       'crew is four people, a local lad with a van, and {N}.'),
                      ('W',
                       "The tour contract promised this venue the full production, and the venue's drawings went out "
                       'months ago. {N} means to keep that promise if it can be kept.'),
                      ('U',
                       '{N} measures the stage twice, then the flats, then the wings, and starts sketching on the '
                       'back of a call sheet: what could fold, what could go.'),
                      ('B',
                       '{boss} will want to know whose mistake this was by the morning. The drawings went out with '
                       "someone else's signature on them, not {Ns}."),
                      ('R',
                       'Midnight, sawdust, a radio playing, and a problem nobody has a rule for. {N} feels wide '
                       'awake and oddly happy.'),
                      ('G',
                       'The crew has done thirty get-ins together on this tour. {colleague} is already making tea on '
                       'the stage door kettle, and nobody has said a word about bed.')],
            'tribal': [('',
                        'The band has come to the gathering ground on a slope of loose stones, and the hide screens '
                        'topple each time they are raised. {N}, keeper of the fire and the masks, watches the light '
                        'go.')],
            'magic': [('',
                       "The wagon's folding stage is a full yard wider than the inn yard's gate. The innkeeper has "
                       "sold every seat, and the company's master is looking at {N}.")]},
 'outcomes': (['The set goes up by dawn, smaller and stranger, and the show opens on time.',
               'The crew sleeps four hours, and the first night is the best of the season.'],
              ['The show opens late on half a set, and the wait goes on far too long.',
               'The first night is called off, and the people who came are sent home.']),
 'options': [
    ("cut the set to the venue's drawings, and log every change for the producer", 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'raise only the screens the ground will bear, and tell the shaper which are gone', 'magic': "cut the stage to the yard's measure, and enter every change in the book"}, 'chance': 0.6}),
    ('redraw the set overnight so it folds into the space', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'grants': 'stagecraft', 'world': {'tribal': 'work out a new way to wedge the screens into the stony slope', 'magic': 'redraw the wagon stage overnight so it folds into the yard'}, 'chance': 0.63}),
    ('cancel the opening, and make sure the producer sees whose drawings were wrong', 'B1', None, 0.45, '', {'v': 'security, power', 'world': {'tribal': 'put off the telling, and make sure the elders know who chose the ground', 'magic': 'put off the play, and make sure the master knows whose measure was wrong'}, 'chance': 0.92}),
    ('strip it back to a bare stage and one chair, and dare the show to work', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'drop the screens altogether, and play the telling by firelight alone', 'magic': 'leave the wagon stage on the road, and play the yard bare'}, 'chance': 0.65}),
    ('put the kettle on, and work through the night with the crew together', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'self_control': '+', 'world': {'tribal': 'build up the fire, and work through the night with the other keepers', 'magic': "send for bread and ale, and work through the night with the company's hands"}, 'chance': 0.9}),
    ('log the set as fitted to the drawings, so nobody on the crew is blamed', 'W1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'self_control': '-', 'mark': 'hid a wrong', 'closed': "approval: a tour report that hides the set's own fault; backfire: the next venue has the same trouble, and the producer reads both reports", 'world': {'tribal': 'tell the elders the screens stood true, so no keeper is blamed', 'magic': 'write in the book that the stage fitted, so no hand is blamed'}, 'chance': 0.75}),
    ('plan the get-in to the minute, and post it on the call board for everyone', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'set the order of the work by the stars, and tell every keeper his turn', 'magic': "plan the night's work to the bell, and pin it to the wagon's side for everyone"}, 'chance': 0.75}),
    ('trade the venue manager a cut of the bar for the workshop and its carpenter', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "trade the gathering's keeper a share of the feast for his best screen-builder", 'magic': 'trade the innkeeper a share of the takings for his workshop and his carpenter'}, 'chance': 0.77}),
    ('rebuild it overnight with your own hands, and take the credit in the morning', 'R1', 'B.7', 0.5, '', {'v': 'achievement, power', 'body': 'heavy', 'world': {'tribal': 'rebuild the screens yourself by firelight, and let the elders see whose hands did it', 'magic': 'rebuild the stage yourself by lamplight, and let the master see whose hands did it'}, 'chance': 0.8}),
    ('build it the old touring way, by eye, and skip the safety sign-off', 'G1', 'R.7', 0.5, '', {'v': 'tradition, self-direction', 'closed': "approval: a set put up without the safety checks; backfire: the venue's safety officer finds it at the half and stops the show", 'self_control': '-', 'world': {'tribal': 'stake the screens the old way, by eye, and never ask the elders to look', 'magic': "build it the old wagoners' way, by eye, and never send for the town's inspector"}, 'chance': 0.75}),
 ]},
{'name': 'a name or the best audition',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'casting director',
 'worlds': {'earth': 'the casting office after the recalls: the producers want a famous name for the lead, and the '
                     'best audition all week came from an unknown',
            'tribal': "the chief wants his nephew in the telling, and the best player the elders saw is a hunter's "
                      'daughter',
            'magic': 'the patron wants a court favourite for the lead, and the best trial came from a street player'},
 'timing': {'times': 'per casting director a year: several times a year; about 1 life in 5,000 casts for a living '
                     "(catalogue share; the US casting directors' society has nearly 1,200 members; estimate)"},
 'scenes': {'earth': [('',
                       'After the recalls the room smells of coffee and nerves. {boss} and the other producers want '
                       'a famous name for the lead, a television face who read the scene flat. The best audition all '
                       'week came from an unknown who made {N} forget to write anything down.'),
                      ('W',
                       'The whole job is a fair hearing for everyone who walks in, and the part to whoever is best '
                       'for it. By that measure the answer is not in doubt.'),
                      ('U',
                       '{N} watches both tapes again with the sound off, then with it on. The name has a following; '
                       'the unknown has the part in their bones. Both facts matter.'),
                      ('B',
                       "The producers pay {Ns} invoices, and the name's agent sends {N} three clients a year. One "
                       'recommendation can keep a lot of doors open.'),
                      ('R',
                       "The unknown's audition is still ringing in {Ns} head. Something in {N} wants to bang the "
                       'table for them.'),
                      ('G',
                       '{N} has seen this before: a name fills the first month, and a show lives or dies on whoever '
                       'can carry it for a year.')],
            'tribal': [('',
                        "The chief's nephew stands by the fire, sure of himself. The hunter's daughter who played "
                        'the bear for the elders at dusk stands back in the dark, and {N}, the elder who chooses, '
                        'has to say a name.')],
            'magic': [('',
                       "The patron's letter names his court favourite for the lead. In {Ns} notebook, underlined "
                       'twice, is the name of a street player who gave the best trial of the season.')]},
 'outcomes': (['The part goes to the actor who earned it, and before long the people who wanted the name are calling '
               'it their own idea.',
               'Everyone gets something they can live with, and the first reading together is full of good will.'],
              ['{N} is overruled without a word, and the unknown hears about it from someone else.',
               'The choice is made, and the actor who lost never quite forgives {N}.']),
 'options': [
    ('recommend the unknown in writing, with your reasons, as the best audition', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'identity': True, 'world': {'tribal': "tell the chief before the band that the hunter's daughter played the bear best", 'magic': 'write to the patron under your seal that the street player gave the best trial'}, 'chance': 0.5}),
    ('cut the two auditions side by side, and let the producers see the difference', 'U1', None, 0.45, '', {'v': 'achievement', 'identity': True, 'grants': 'a casting eye', 'world': {'tribal': 'ask both to play the bear again, side by side before the elders', 'magic': 'have both trials glamoured side by side in the air for the patron'}, 'chance': 0.55}),
    ('give the producers their name, and keep the unknown on file for the next job', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': "give the chief his nephew, and keep the hunter's daughter in mind for next winter", 'magic': "give the patron his favourite, and keep the street player's name on your roll"}, 'chance': 0.95}),
    ('ring the producers tonight and tell them they would be fools to lose the unknown', 'R1', None, 0.45, '', {'v': 'self-direction', 'world': {'tribal': "go to the chief's fire tonight and tell him the girl is the better player", 'magic': "storm into the patron's antechamber and tell him he is passing over the best player in the city"}, 'chance': 0.3}),
    ('offer the name the lead and the unknown the second part, and let the run decide', 'G1', None, 0.45, '', {'v': 'security, benevolence', 'world': {'tribal': "give the nephew the great part and the girl the hunter's, and let the winters show who is better", 'magic': 'give the favourite the lead and the street player the second, and let the season tell'}, 'chance': 0.75}),
    ('ask for one more recall, both actors reading opposite the same partner', 'W1', 'U.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': 'ask the elders to see both again at the next fire, against the same player', 'magic': 'ask for one more trial, both reading with the same company player'}, 'chance': 0.75}),
    ('show the producers the figures: unknown leads cost less and run longer', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'lay out for the chief what a poor telling would cost him before the clans', 'magic': 'show the patron the ledgers: unknown leads cost less and draw longer seasons'}, 'chance': 0.5}),
    ("let the unknown's agent hear how good the audition was, and let the buzz build", 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'mark': 'hid a wrong', 'closed': 'approval: a casting leaked to put pressure on the producers; backfire: the producers find out who leaked it, and the next show goes to another office', 'world': {'tribal': "let the young ones hear how the hunter's daughter played, so the band starts asking for her", 'magic': "let the broadsheet criers hear of the street player's trial, so the city asks for her"}, 'chance': 0.45}),
    ('find the unknown after the recall, and tell them to keep going, whatever happens', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': "find the hunter's daughter at her hearth, and tell her to keep playing, whatever is chosen", 'magic': 'find the street player in the square, and tell her to keep at it, whatever the patron says'}, 'chance': 0.9}),
    ('sleep on it, then let the director who must live with the cast choose', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'sleep on it, then let the shaper of the telling choose, as the old ones did', 'magic': 'sleep on it, then leave the choice to the master of the play, as the old choosers did'}, 'chance': 0.7}),
 ]},
{'name': 'the actor who cried in the waiting room',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, colleague',
 'requires': 'casting director',
 'worlds': {'earth': 'a corridor full of hopefuls with numbered stickers, and one of them is in tears before going '
                     'in',
            'tribal': 'a young hunter weeps at the edge of the firelight before showing the elders the bear',
            'magic': 'a nervous player sobs outside the trial room in the guild hall'},
 'timing': {'times': 'per casting director: most weeks of auditions (estimate)'},
 'scenes': {'earth': [('',
                       'Forty actors in a corridor with numbered stickers, eight minutes each, and the director '
                       'wants to be gone by six. Number twenty-three, a young man with a crumpled script on his '
                       'knee, is crying quietly into his sleeve. {N} has the clipboard and the schedule.'),
                      ('W',
                       'Every actor in that corridor is owed the same eight minutes and the same fair hearing. '
                       'Twenty-three is too.'),
                      ('U',
                       '{N} has seen nerves wreck good actors and sharpen others. The question is which kind this '
                       'is, and what would let the real audition through.'),
                      ('B',
                       '{boss}, the director, is already twenty minutes behind and in a foul mood. A delay now will '
                       'cost {N} more than five minutes.'),
                      ('R',
                       '{N} remembers sitting in exactly that kind of corridor years ago, shaking. The feeling comes '
                       'back so fast it is almost physical.'),
                      ('G',
                       'Some days are like this. People cry in waiting rooms and always have; it passes, if it is '
                       'given a little room.')],
            'tribal': [('',
                        'The young ones wait at the edge of the firelight to show the elders the bear. One of them, '
                        'a young hunter of the river hearths who has never played before the band, is weeping into '
                        'his hands. {N}, the elder who chooses, sees it.')],
            'magic': [('',
                       "In the guild hall's corridor the hopefuls wait for their trials, each with a numbered token. "
                       'One of them, a journeyman from the lower wards, is sobbing by the trial room door. {N}, the '
                       "company's chooser of players, holds the roll and the hourglass.")]},
 'outcomes': (['The actor who was crying gives the best reading of the day, and is asked back.',
               'The day ends only a little late, and everyone who waited had a fair hearing.'],
              ['The day falls apart, and {boss} spends the last hour sighing at the time.',
               'The actor goes in shaking and comes out worse, and {N} wonders all evening what else could have been '
               'done.']),
 'options': [
    ('keep the order, and give number twenty-three the same eight minutes as everyone', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'keep to the order of the fire, and give the weeping one the same turn as the rest', 'magic': 'keep to the roll, and give the weeping player the same turn of the glass'}, 'chance': 0.75}),
    ('move him to the last slot of the day, so he has time to settle', 'U1', None, 0.45, '', {'v': 'benevolence, achievement', 'world': {'tribal': 'let him go last, when the fire is low and the elders are patient', 'magic': 'move him to the last turn of the day, so he can settle'}, 'chance': 0.85}),
    ('send him home, and give the slot to the next name on the reserve list', 'B1', None, 0.45, '', {'v': 'achievement, security', 'mark': 'refused someone in need', 'world': {'tribal': 'send him back to his hearth, and call the next young one', 'magic': "strike him from today's roll, and call the next name"}, 'chance': 0.95}),
    ('sit beside him for five minutes, and tell him about your own worst audition', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'mark': 'helped someone in need', 'world': {'tribal': 'sit by him at the edge of the light, and tell him about the first time you shook before the elders', 'magic': 'sit with him on the bench, and tell him about your own worst trial'}, 'chance': 0.85}),
    ('see him now, tears and all, and let whatever comes come', 'G1', None, 0.45, '', {'v': 'tradition (acceptance), benevolence', 'world': {'tribal': 'call him into the light now, tears and all, and let the bear come as it will'}, 'chance': 0.55}),
    ('explain calmly what the panel looks for, and that one scene is enough', 'W1', 'U.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'tell him plainly what the elders watch for, and that one turn is enough', 'magic': 'tell him plainly what the master looks for, and that one speech is enough'}, 'chance': 0.8}),
    ('watch how he handles it, as a clue to how he would handle a long run', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'watch how he holds himself, as a sign of how he would bear a whole winter', 'magic': 'watch how he bears it, as a sign of how he would bear a long season'}, 'chance': 0.9}),
    ('send him straight in now, ahead of the queue, while the feeling is raw', 'B1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'send him into the light at once, while the feeling is raw', 'magic': 'send him in at once, ahead of the roll, while the feeling is raw'}, 'chance': 0.45}),
    ('take the whole corridor outside for five minutes of air and stretching', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, hedonism', 'world': {'tribal': 'take all the waiting young ones down to the river for a breath of cold air', 'magic': "take all the waiting players into the guild's yard for a breath of air"}, 'chance': 0.75}),
    ('ask a friend from the queue to sit with him, as actors do for each other', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'mark': 'helped someone in need', 'world': {'tribal': 'ask a friend from his hearth to sit with him, as the young always have', 'magic': 'ask a fellow player from the queue to sit with him, as players do for each other'}, 'chance': 0.8}),
 ]},
{'name': 'two clients, one part',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'talent agent',
 'worlds': {'earth': "the agency's office on a Monday: the best-paid client on the list wants the lead a young "
                     'client was about to be offered',
            'tribal': 'two tellers you speak for both want to wear the great mask, and the elders will hear only one '
                      'name',
            'magic': 'two of your players want the same lead at the court playhouse, and its master will see only '
                     'one'},
 'timing': {'times': 'per talent agent a year: several times; about 1 life in 2,500 works as an agent for performers '
                     '(catalogue share; US labour statistics: 12,870 agents and business managers of artists, '
                     'performers and athletes, 2023; estimate)'},
 'scenes': {'earth': [('',
                       'Monday morning. The casting office has all but offered the lead in a new play to {Ns} '
                       "youngest client, three years out of drama school. Then the agency's best-paid client, a face "
                       'everyone knows from television, rings: the part is perfect for them, and they expect {N} to '
                       'put them up.'),
                      ('W',
                       'An agent owes every client on the list the same honesty. Two clients, one part: someone has '
                       'to be told the truth.'),
                      ('U',
                       "{N} lays it out: the part's age, the director's past casting, the producers' taste. The "
                       'young client fits the director; the star fits the money.'),
                      ('B',
                       "The star's commission pays a third of the office rent. The young client may be the future, "
                       "but the future does not pay this month's bills."),
                      ('R',
                       'The young client rang on Friday, almost singing down the phone. {N} cannot stop hearing that '
                       'voice.'),
                      ('G',
                       '{N} has looked after the star for fifteen years, through two divorces and a long bad patch. '
                       'The young one has been on the list a single season.')],
            'tribal': [('',
                        'Both tellers {N} speaks for have come to {Ns} hearth: the old one every band knows, and the '
                        'young one who has never yet worn the great mask. The elders will hear only one name.')],
            'magic': [('',
                       "Two letters lie on {Ns} desk, both from players {N} places: the season's darling and a "
                       'newcomer. Both want the same lead at the court playhouse, and its master will see only '
                       'one.')]},
 'outcomes': (['The part goes to the one who fits it, and a season later both still trust {N}.',
               'Whoever does the choosing thanks {N} for an honest steer, and asks first next time.'],
              ['One of the two gets the part, and the other turns to someone else to speak for them.',
               'Tired of the tug of war, whoever does the choosing gives the part to someone else entirely.']),
 'options': [
    ('tell both clients the truth, and put up whoever fits the part best', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'tell both tellers the truth at your fire, and speak for whoever fits the mask', 'magic': 'write the truth to both players, and recommend whoever fits the part'}, 'chance': 0.6}),
    ('put both up, with a note to the casting director on what each would bring', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'speak for both before the elders, and say plainly what each would bring', 'magic': 'put both forward, with a letter to the master on what each would bring'}, 'chance': 0.85}),
    ('put the star up, and tell the young client the casting office went another way', 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'hid a wrong', 'closed': "approval: a client's part given away behind their back; backfire: the casting director tells the young client the truth, and the client leaves the agency", 'world': {'tribal': 'speak only for the old teller, and tell the young one the elders never asked', 'magic': 'put the darling forward, and tell the newcomer the master never asked'}, 'chance': 0.8}),
    ('ring the young client at once, and promise to fight for the part', 'R1', None, 0.45, '', {'v': 'benevolence, self-direction', 'binds': True, 'world': {'tribal': "go to the young teller's hearth at once, and promise to speak for them", 'magic': 'send word to the newcomer at once, and swear to fight for the part'}, 'chance': 0.85}),
    ('tell the star, as an old friend, that this one belongs to the young client', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'identity': True, 'world': {'tribal': 'tell the old teller, as a friend of many winters, that this mask belongs to the young one', 'magic': 'tell the darling, as an old friend, that this part belongs to the newcomer'}, 'chance': 0.6}),
    ("follow the agency's written rule on clashes, and bill whichever client gets it", 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': "keep to the go-betweens' custom for two tellers and one mask, and take the gift either way", 'magic': "keep to the brokers' guild rule on rival players, and take the cut either way"}, 'chance': 0.75}),
    ('find the star a better part elsewhere this week, so the young client keeps this one', 'U1', 'R.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'find the old teller a better telling at another band, so the young one keeps the mask', 'magic': 'find the darling a better part at another house, so the newcomer keeps this one'}, 'chance': 0.3}),
    ('back the young client, and trade the star first refusal on the next series', 'B1', 'G.7', 0.5, '', {'v': 'power, security', 'binds': True, 'world': {'tribal': "back the young one, for the old teller's promise of the first telling next winter", 'magic': "back the newcomer, and trade the darling first claim on next season's lead"}, 'chance': 0.45}),
    ('tell the star to their face that taking this part would be wrong', 'R1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'world': {'tribal': 'tell the old teller to his face that taking the mask would be wrong', 'magic': 'tell the darling to her face that taking the part would be wrong'}, 'chance': 0.55}),
    ('ask the director, an old acquaintance, which actor they truly want', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the shaper of the telling, whom you have known for years, which one he truly wants', 'magic': 'ask the master of the play, an old acquaintance, which player he truly wants'}, 'chance': 0.8}),
 ]},
{'name': 'the client who has not worked in a year',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'talent agent',
 'worlds': {'earth': "a client's name on the agency board with nothing beside it for a whole year, and the list is "
                     'reviewed on Friday',
            'tribal': 'a teller you speak for has had no call from any band all winter',
            'magic': 'a player of yours has had no booking since the last fair'},
 'timing': {'times': 'per talent agent: every few months; most actors on most lists work only a few weeks a year '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       "On the agency's whiteboard, beside one client's name, there is nothing: no bookings, no "
                       'recalls, twelve months blank. The partners review the list on Friday, and {boss} has already '
                       'circled the name.'),
                      ('W',
                       'When {N} signed this actor, {N} promised to stand by them through the lean years. A promise '
                       'made in good times is still a promise.'),
                      ('U',
                       "{N} goes through the year's submissions: forty-one suggestions, six auditions, no offers. "
                       'Somewhere in that record there is a pattern.'),
                      ('B',
                       'A list is a business, and a client who earns nothing costs the agency hours it could spend '
                       'on clients who do.'),
                      ('R',
                       'The actor rings every Monday, cheerful on the phone, and {N} has started letting it go to '
                       'voicemail. That feels worse than anything on the whiteboard.'),
                      ('G',
                       'Careers have seasons. {N} has seen actors go a whole year without a job and then work for '
                       'ten.')],
            'tribal': [('',
                        'The teller {N} speaks for has sat at the same fire all winter, and no band has sent for the '
                        'telling. {Ns} share of the gifts has been nothing at all.')],
            'magic': [('',
                       "In the broker's ledger the player's page has been blank since the last fair, and the other "
                       'brokers in the guild have begun to whisper that the name is finished.')]},
 'outcomes': (['Before the season is out a part comes in, small but real, and the client weeps with relief.',
               'The talk is hard and honest, and the client goes on to another life with no ill will.'],
              ['Another empty season goes by, and {boss} asks again why the name is still kept on.',
               'The client hears it from someone else first, and never speaks to {N} again.']),
 'options': [
    ('keep them on the list, as you promised when you signed them', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'mark': 'kept your word', 'self_control': '+', 'world': {'tribal': 'go on speaking for the teller at every fire, as you promised', 'magic': 'keep the player in your ledger, as you swore when you took them on'}, 'chance': 0.8}),
    ("go through the year's auditions with them, and find what is not landing", 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': "go over the winter's tellings with them, and find what the bands did not want", 'magic': "go through the year's trials with them, and find what the masters did not want"}, 'chance': 0.9}),
    ('drop them from the list on Friday, with a short, polite letter', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': 'stop speaking for the teller, and say so plainly at the next fire', 'magic': 'strike them from your ledger, with a short, polite note'}, 'chance': 0.95}),
    ('tell them straight, over lunch, that the work has dried up, and ask what they want', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'world': {'tribal': 'tell them straight, over a shared meal, that the bands have stopped asking', 'magic': 'tell them straight, over a cup, that the bookings have dried up'}, 'chance': 0.95}),
    ('keep them on quietly, and wait for the season to turn, as careers do', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'go on as before, and wait for the bands to remember the teller', 'magic': 'keep their page in the ledger, and wait for the fashion to turn'}, 'chance': 0.55}),
    ('give them three months and clear targets, and drop them if none are met', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'give them until the thaw to be asked for, and stop speaking for them if none ask', 'magic': 'give them one season by the ledger to be booked, or be struck off'}, 'chance': 0.65}),
    ('cut a new showreel that makes them look ten years younger than they are', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, achievement', 'self_control': '-', 'mark': 'hid a wrong', 'closed': "approval: a showreel that lies about a client's age; backfire: the casting director sees the actor in the room, and stops taking the agency's calls", 'world': {'tribal': 'teach them to play the young hunters, and tell the bands they are younger than they are', 'magic': 'have a glamour-reel made that shows them ten years younger than they are'}, 'chance': 0.75}),
    ('call in a favour with a casting director you know, for one audition for them', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'grants': 'contact in the trade', 'world': {'tribal': 'call in an old debt with a shaper of another band, for one telling for them', 'magic': 'call in a favour with a master you know, for one trial for them'}, 'chance': 0.6}),
    ('ring every casting office yourself, one by one, until somebody sees them', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, achievement', 'self_control': '+', 'world': {'tribal': "walk to every band's fire yourself until one asks for the teller", 'magic': 'knock on every playhouse door yourself until one master sees them'}, 'chance': 0.45}),
    ('suggest a class and a play for love, so they come back to it fresh', 'G1', 'U.7', 0.5, '', {'v': 'self-direction, tradition', 'door': True, 'world': {'tribal': 'tell them to play at their own hearth this winter, for love, and come back fresh', 'magic': 'suggest a term at the guild school and a play for love, so they come back fresh'}, 'chance': 0.85}),
 ]},
{'name': 'drama cut from the timetable',
 'stages': 'young_adult adult mature elder',
 'age': (20, 85),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'drama teacher',
 'worlds': {'earth': "a meeting with the head about next year's timetable: the drama hours are going to the exam "
                     'subjects',
            'tribal': 'the elders say the children are needed at the fish weirs this spring, not at the tellings',
            'magic': "the academy's council would turn the players' hours into reckoning hours"},
 'timing': {'times': 'per drama teacher a year: about 1 in 10 see drama hours cut; English secondary schools had '
                     '8,963 drama teachers in 2019 against 11,100 in 2010 (a UK arts-in-schools alliance, from the '
                     'school workforce census)'},
 'scenes': {'earth': [('',
                       "{boss}, the head, slides next year's timetable across the desk. The drama hours have gone to "
                       'maths and science, and the school play survives only if it can be run in lunchtimes. {N} has '
                       'taught at this school for eleven years.'),
                      ('W',
                       'The curriculum says every child is entitled to the arts. {N} knows the paragraph by heart, '
                       'and knows the school is bending it.'),
                      ('U',
                       '{N} has the numbers: attendance on drama days, the results of the children who take it, how '
                       'many stay in school because of the play.'),
                      ('B',
                       'The head is under pressure from the governors over results. {N} can see what the head needs, '
                       'and what the head might trade for it.'),
                      ('R',
                       'The quiet boy who found his voice in the third year. The girl who comes in only on drama '
                       'days. The anger comes up hot and fast.'),
                      ('G',
                       'The school play has run every spring for thirty years, and parents who were in it now bring '
                       'their own children to watch. Some things belong to a place.')],
            'tribal': [('',
                        'The elders sit at the council fire: the fish are running early, and every pair of small '
                        "hands is needed at the weirs. The children's tellings, {N} is told, can wait for the dark "
                        'moons.')],
            'magic': [('',
                       "The academy's council has sent its ruling: the hours the children spend with the players' "
                       'master will go to reckoning and the measuring of stars. {N} holds the sealed page.')]},
 'outcomes': (["The children's hours survive, a little smaller, and the spring play goes ahead as it always has.",
               'Something new grows out of the fight: an evening company, a new post, or a play in a new place.'],
              ['The ruling goes through as written, and the room where the children played is given to other work.',
               '{N} wins the hours back for a year, and {boss} makes it plain the matter is not closed.']),
 'options': [
    ("appeal to the governors, quoting the curriculum's own words on the arts", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders to hear the old custom that the children learn the tellings each spring', 'magic': "petition the academy's council under its own charter for the players' hours"}, 'chance': 0.25}),
    ('bring the head the figures on attendance and results for children who take drama', 'U1', None, 0.45, '', {'v': 'achievement', 'identity': True, 'world': {'tribal': 'show the elders that the children who learn the tellings listen best at the weirs too', 'magic': "bring the council the ledgers: the pupils who take the players' hours reckon better too"}, 'chance': 0.5}),
    ('take the better-paid post at the private stage school across town', 'B1', None, 0.45, '', {'v': 'achievement, security', 'door': True, 'world': {'tribal': 'go to teach the children of a richer band upriver, who keep their tellings', 'magic': "take a master's post at a rich players' school in the upper city"}, 'chance': 0.75}),
    ('run the school play after school for nothing, and tell the head so', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'identity': True, 'binds': True, 'self_control': '+', 'world': {'tribal': 'teach the tellings at the fire after the weir work, for nothing, and tell the elders so', 'magic': "teach the players' hours after the bell, unpaid, and tell the council so"}, 'chance': 0.85}),
    ('accept the cut, and keep the play alive in lunchtimes as best you can', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': "accept the elders' word, and teach the tellings in snatches between the weir work", 'magic': 'accept the ruling, and keep the masque going in the midday break'}, 'chance': 0.75}),
    ('set up an evening youth company in the town, with a form signed by every parent', 'W1', 'R.7', 0.5, '', {'v': 'universalism, self-direction', 'binds': True, 'aims': 'community theatre director', 'world': {'tribal': "gather the children at the evening fire to learn the tellings, with every mother's leave", 'magic': "start an evening children's company in the guild hall, with every parent's mark on the roll"}, 'chance': 0.75}),
    ('write up three pupils who stayed in school because of the play, for the governors', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': 'tell the elders of three children the tellings kept close to the band', 'magic': 'write the council the cases of three pupils the masque kept at their books'}, 'chance': 0.55}),
    ('back the head on the new exam plan, in return for drama hours in writing', 'B1', 'W.7', 0.5, '', {'v': 'power, conformity', 'binds': True, 'world': {'tribal': 'back the elders on the weir work, in return for one telling every moon', 'magic': "back the council's reckoning plan, in return for the players' hours under seal"}, 'chance': 0.55}),
    ('push your two best older pupils to audition for drama school this year', 'R1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'send your two best young ones to an old teller of another band, to learn before the tellings are lost', 'magic': 'push your two best older pupils to try for the guild school this spring'}, 'chance': 0.6}),
    ('get the families whose children were all in the play to lean on the head', 'G1', 'B.7', 0.5, '', {'v': 'power, tradition', 'world': {'tribal': 'get the old families whose children all learned the tellings to speak at the council fire', 'magic': 'get the old guild families whose children all played the masque to press the council'}, 'chance': 0.55}),
 ]},
{'name': 'the shy child who wants a line',
 'stages': 'young_adult adult mature elder',
 'age': (20, 85),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague',
 'requires': 'drama teacher',
 'worlds': {'earth': 'a quiet child at the back of the drama class puts up a hand, in front of everyone, and asks '
                     'for one line in the play',
            'tribal': "a small boy who never speaks steps forward at the children's fire and wants the hare's part",
            'magic': 'a shy pupil stands up in front of the class and asks for a single line in the masque'},
 'timing': {'times': 'per drama teacher: several times a year, at each casting (estimate)'},
 'scenes': {'earth': [('',
                       'The whole class sits in a circle, casting the spring play, and {colleague}, the teaching '
                       'assistant, is taking down names. A girl who has not said a word all term puts up her hand '
                       'and asks, very quietly, for one line.'),
                      ('W',
                       'Every child in the room has the same right to a part. {N} made that the rule on the first '
                       'day of term, and the whole class heard it.'),
                      ('U',
                       '{N} has watched her all term: she mouths every line of every scene from the back of the '
                       'circle. She knows the play better than half the cast.'),
                      ('B',
                       'The play goes up in front of the whole school and the governors in six weeks. {N} needs '
                       'strong voices in the parts that carry it.'),
                      ('R',
                       'It took her a whole term to put that hand up. {N} feels a rush of something like joy, and '
                       'the urge to give her the best line in the play.'),
                      ('G',
                       'Some children open slowly, like seeds in cold ground. Push too hard and they close again.')],
            'tribal': [('',
                        "At the children's fire the old teller is giving out the animals for the spring telling, "
                        'with the mothers sitting close by. A small boy of the river hearths who never speaks steps '
                        'forward and points at the hare mask, and his mother catches her breath.')],
            'magic': [('',
                       "In the guild school's practice hall the master is giving out the parts of the children's "
                       'masque, with an usher at the door. A shy pupil who has never once spoken in class stands up '
                       'in front of the others and asks for a single line.')]},
 'outcomes': (['On the night the child says the line clearly, and the family is on its feet.',
               'The child comes back the next week a little taller, and asks for a bigger part next time.'],
              ["On the night the child's voice disappears, and the words go by in a whisper only the nearest hear.",
               'The child takes the answer as a no, and does not ask again that year.']),
 'options': [
    ('give her a line, as every child who asks is given one', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'give him the hare, as every child who asks is given a part', 'magic': 'give her a line in the masque, as every pupil who asks is given one'}, 'chance': 0.95}),
    ('write her a short line that fits exactly what she can do now', 'U1', None, 0.45, '', {'v': 'achievement, benevolence', 'world': {'tribal': "make the hare's part a few words he can say, and let it grow each night"}, 'chance': 0.9}),
    ('keep the speaking parts for the confident ones, and give her a part with no lines', 'B1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'keep the speaking animals for the bold ones, and give him a silent place in the herd', 'magic': 'keep the speaking parts for the bold pupils, and give her a silent place in the masque'}, 'chance': 0.8}),
    ('give her the best line in the play, there and then, in front of everyone', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'hand him the hare mask there and then, in front of every child', 'magic': 'give her the best line in the masque, there and then, before the whole class'}, 'chance': 0.55}),
    ('tell the old tale of the quiet hero, and let her pick a part in it', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'grants': 'telling a story aloud', 'world': {'tribal': 'tell the children the old tale of the quiet hare, and let him pick his part', 'magic': 'tell the old tale of the quiet page who saved the king, and let her choose'}, 'chance': 0.75}),
    ('put her in a chorus that speaks together, so her voice can come out safely', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'put him among the small spirits who call out together, so his voice can come', 'magic': 'put her in the chorus of fairies who speak as one, so her voice can come'}, 'chance': 0.85}),
    ('practise the line in the circle each week, the whole class saying it with her', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, achievement', 'habit': True, 'world': {'tribal': "have all the children say the hare's words together each night by the fire", 'magic': 'practise the line in the circle each lesson, the whole class saying it with her'}, 'chance': 0.85}),
    ('give her a line, and have her cover the narrator, since she knows every word', 'B1', 'W.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "give him the hare, and have him learn the stag's words too, since he knows them all", 'magic': "give her a line, and have her cover the herald's part, since she knows every word"}, 'chance': 0.7}),
    ('make a game of it: everyone shouts their lines, then whispers, then she tries hers', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'make a game of it: the children roar like bears, whisper like mice, then he tries the hare', 'magic': 'make a game of it: the class shouts its lines, then whispers, then she tries hers'}, 'chance': 0.8}),
    ('speak with her parents at pick-up, and plan together a bigger part by summer', 'G1', 'B.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'speak with his mother at her hearth, and plan together a bigger part by midsummer', 'magic': 'speak with her parents at the school gate, and plan together a bigger part by summer'}, 'chance': 0.75}),
 ]},
{'name': 'a year as the villain',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, health',
 'horizon': 'months',
 'roles': 'boss, mentor',
 'requires': 'voice actor',
 'worlds': {'earth': 'a games studio offers a year of steady work as the villain: battle cries, screams and death '
                     'rattles, four hours a session',
            'tribal': 'the band wants the voice of the cave bear behind the hide screen every night of the long '
                      'winter',
            'magic': "a puppet theatre wants its demon's roar for a full season, every night and twice on feast "
                     'days'},
 'timing': {'times': 'per voice actor a year: about 1 in 10 are offered long, straining work (estimate); about 1 '
                     'life in 2,000 voices for a living (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'The offer comes by email: a whole year as the villain of a big new game, and steady money '
                       'for the first time in {Ns} working life. The scripts are attached: page after page of '
                       'screams, battle cries and death rattles, four hours a session.'),
                      ('W',
                       "A year's contract is a year's promise, to a studio and to a whole team building a game "
                       'around the voice. {N} does not sign anything without meaning to see it through.'),
                      ('U',
                       '{N} reads the scripts with a pencil, marking every scream. Shouted from the throat, they '
                       'would wreck a voice in a month; from the body, with care, it might last.'),
                      ('B',
                       "Steady money, a credit in a game millions will play, and a foot in the door for the studio's "
                       'next one. Turning it down would mean turning down a ladder.'),
                      ('R',
                       'The villain is glorious: wild, funny, monstrous. {N} can already hear the roar and wants to '
                       'do it more than anything.'),
                      ('G',
                       '{mentor}, who taught {N} to breathe, lost half a voice to a cartoon dragon thirty years ago '
                       'and still speaks in a husk.')],
            'tribal': [('',
                        "The elders want the cave bear's voice behind the hide screen every night of the long dark, "
                        'from first snow to the thaw. {Ns} throat aches just thinking of it.')],
            'magic': [('',
                       "The puppet theatre's master offers a season's wage for the demon's roar: every night, and "
                       "twice on feast days. {N} has heard what became of the last demon's voice.")]},
 'outcomes': (['The year goes by in roars and screams, and the voice comes out of it whole, and in demand.',
               'The work is agreed on {Ns} own terms, and more is asked for after.'],
              ['By spring the voice is a rasp, and two other bookings have to be turned away.',
               'Another voice is chosen, and the steady living goes with it.']),
 'options': [
    ('sign for the year, and keep every session, whatever it costs', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'binds': True, 'world': {'tribal': 'promise the elders the bear for the whole winter, and keep every night', 'magic': "sign the season's contract, and give the roar every night as promised"}, 'chance': 0.8}),
    ('take it, and book a voice coach to teach screaming without damage', 'U1', None, 0.45, '', {'v': 'achievement, security', 'mark': 'learned a skill', 'binds': True, 'door': True, 'self_control': '+', 'world': {'tribal': 'take it, and learn from the old hidden voices how to roar from the belly', 'magic': 'take it, and pay a master of voice to teach the roar without harm'}, 'chance': 0.75}),
    ('haggle for shorter sessions and a higher fee before signing anything', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': 'agree to the bear on alternate nights only, for a bigger share of the winter meat', 'magic': 'haggle for shorter nights and a fatter purse before setting your mark to it'}, 'chance': 0.45}),
    ('say yes on the spot, and throw yourself into the roar', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'say yes at once, and throw yourself into the bear', 'magic': 'say yes on the spot, and throw yourself into the demon'}, 'chance': 0.95}),
    ('turn it down, and keep the voice for a lead in a series one day', 'G1', None, 0.45, '', {'v': 'security, tradition', 'identity': True, 'mark': 'turned down a chance', 'aims': 'lead actor or actress', 'self_control': '+', 'world': {'tribal': 'turn it down, and keep the voice for the first ancestor one day', 'magic': "turn it down, and keep the voice for a hero's part one day"}, 'chance': 0.85}),
    ('sign, with rest days for the voice written into the contract', 'W1', 'G.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'agree, if the elders let the voice rest one night in three', 'magic': 'sign, with rest nights for the voice written into the contract'}, 'chance': 0.5}),
    ("ask for the studio's rules on vocal strain, and hold them to every line", 'U1', 'W.7', 0.5, '', {'v': 'conformity, security', 'world': {'tribal': 'ask the elders how the old voices were spared, and hold them to it', 'magic': "ask the master for the guild's rules on strained voices, and hold him to them"}, 'chance': 0.6}),
    ('take the year, and spend the money on a long course with the best voice teacher', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'self_control': '+', 'world': {'tribal': 'take the winter, and trade its meat to the best old voice for teaching', 'magic': "take the season, and spend the purse on lessons with the city's best master of voice"}, 'chance': 0.85}),
    ('say yes only if the studio puts you up for the lead in its next game', 'R1', 'B.7', 0.5, '', {'v': 'achievement, power', 'aims': 'lead actor or actress', 'world': {'tribal': "say yes only if the elders promise you the first ancestor's voice next winter", 'magic': "say yes only if the master promises you the hero's voice next season"}, 'chance': 0.45}),
    ('play the villain for the joy of it, and stop the moment the throat aches', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, security', 'world': {'tribal': 'roar for the joy of it, and stop each night the moment the throat aches', 'magic': 'roar for the joy of it, and stop each night the moment the throat aches'}, 'chance': 0.65}),
 ]},
{'name': 'the voice is going',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, health',
 'horizon': 'moment',
 'roles': 'boss, colleague',
 'requires': 'voice actor',
 'worlds': {'earth': 'a croak on the morning of a session, and the booking is for the whole day',
            'tribal': 'the voice cracks on the night the spirits must speak from behind the hide screen',
            'magic': 'the voice falters on the morning of a speaking-stone session'},
 'timing': {'times': 'per voice actor: a few times a year (estimate)'},
 'scenes': {'earth': [('',
                       '{N} wakes at six with a voice like gravel. The session is at ten: a full day of an '
                       'audiobook, eight hours, and {boss}, the director, has travelled in for it.'),
                      ('W',
                       'The booking was made three months ago, and a whole studio has cleared its day. {N} has never '
                       'once missed a session.'),
                      ('U',
                       '{N} knows the anatomy: swollen folds, and every hour of pushing makes them worse. The '
                       'question is how swollen.'),
                      ('B',
                       'Cancelling means the job may go to someone else, and this director has a long memory and a '
                       'short list.'),
                      ('R',
                       'Fury at a body that picks today of all days. {N} paces the kitchen, humming, testing, '
                       'swearing quietly.'),
                      ('G',
                       'The voice has carried {N} for twenty years. Lately it tires sooner, as voices do. Maybe it '
                       'is asking for something.')],
            'tribal': [('',
                        'On the night the spirits must speak, {N} wakes croaking like a crow. Behind the hide screen '
                        "there is no one else who knows the spirits' words.")],
            'magic': [('',
                       'On the morning of the speaking-stone session {Ns} voice cracks on the first word, and the '
                       'stones keep whatever is spoken into them, cracks and all.')]},
 'outcomes': (['The voice holds, and {N} is asked back again before the month is out.',
               'A few days of rest, and the voice comes back clearer than before.'],
              ['Halfway through, the voice goes completely, and the work is lost.',
               'The voice holds for the day, and takes three weeks to recover afterwards.']),
 'options': [
    ('ring the studio at once, say how it is, and offer the first free day', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'tell the elders at once, and offer the next night', 'magic': 'send word to the stone-keepers at once, and offer the first free morning'}, 'chance': 0.75}),
    ('steam, rest the voice, and test it every hour before deciding', 'U1', None, 0.45, '', {'v': 'achievement, security', 'self_control': '+', 'world': {'tribal': 'breathe the steam of hot stones, rest the voice, and test it as the day goes', 'magic': 'breathe herb steam, rest the voice, and test it every hour before deciding'}, 'chance': 0.65}),
    ('say nothing, and pitch the whole day lower so the croak never shows', 'B1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'say nothing, and pitch every spirit lower so the crack never shows', 'magic': 'say nothing, and pitch the session lower so the stones never catch the crack'}, 'chance': 0.6}),
    ('take a hot whisky and a painkiller, and push through at full voice', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'habit': True, 'closed': 'approval: drinking before a booked session; backfire: the engineer smells it, and the studio stops calling', 'self_control': '-', 'world': {'tribal': 'drink the berry brew, and push through at full voice', 'magic': 'take a hot spiced wine and a powder, and push through at full voice'}, 'chance': 0.65}),
    ('cancel, rest for a week, and let the voice come back in its own time', 'G1', None, 0.45, '', {'v': 'security, tradition', 'self_control': '+', 'world': {'tribal': 'let another speak the spirits tonight, and rest until the voice comes back'}, 'chance': 0.9}),
    ('ask the studio to move the session, and find another voice for the urgent lines', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': "ask the elders to put off the spirits' night, and find a younger voice for the small ones", 'magic': 'ask the stone-keepers to move the session, and find another voice for the urgent lines'}, 'chance': 0.7}),
    ('see a voice specialist, and follow the treatment to the letter', 'U1', 'W.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'go to the healer, and do exactly as she says', 'magic': "see the healers' guild's master of throats, and follow the cure to the letter"}, 'chance': 0.75}),
    ('trade the day with a colleague who owes a favour, and spend it learning new accents', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'self_control': '+', 'grants': 'accents and voices', 'world': {'tribal': "trade the night with another hidden voice who owes a favour, and spend it learning the clans' voices", 'magic': 'trade the session with a voice who owes a favour, and spend it learning the speech of the southern cities'}, 'chance': 0.85}),
    ('turn the croak into a gravel voice for the villain, and sell it to the director', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'turn the crack into a new voice for the cave spirit, and tell the elders it was meant', 'magic': 'turn the crack into a new voice for the demon, and sell it to the master'}, 'chance': 0.7}),
    ('go in, and let the tired voice be part of the reading, as old storytellers did', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, tradition', 'world': {'tribal': "go behind the screen, and let the tired voice be the old spirit's voice tonight", 'magic': 'go in, and let the tired voice be part of the tale, as old tellers did'}, 'chance': 0.35}),
 ]},
{'name': 'closing on Saturday',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'colleague, mentor',
 'requires': 'producer',
 'worlds': {'earth': 'the box office figures on a Monday: the show loses money every night, and closing means two '
                     'hundred people out of work by Saturday',
            'tribal': 'the families who gave hides for the great telling want them back, and the gathering is only '
                      'half over',
            'magic': "the play-merchant's ledger shows a loss every night of the season, and the company's wages are "
                     "due at the week's end"},
 'timing': {'times': 'per producer a year: about 1 in 5 face closing a show early; most commercial shows do not make '
                     'their money back (estimate)'},
 'scenes': {'earth': [('',
                       "Monday's box office report: the show lost money every single night last week, and the "
                       'advance is thin. Closing on Saturday would put two hundred people out of work, from the cast '
                       'and the band to the crew and the ushers. Keeping it open costs money {N} does not have.'),
                      ('W',
                       '{N} signed two hundred contracts with a run promised in every one. A notice to close is '
                       'legal; it still breaks a promise.'),
                      ('U',
                       '{N} has the figures by performance, by price, by day of the week. The losses are not spread '
                       'evenly, and that is interesting.'),
                      ('B',
                       "A producer's job is to lose small and win big. Every night this stays open is money that "
                       'could back the next hit.'),
                      ('R',
                       '{N} loves this show more than anything {N} has ever made. The thought of a closing notice on '
                       'the stage door is unbearable.'),
                      ('G',
                       'Shows are born and shows die; {N} has closed a dozen. What matters is how the company is let '
                       'go, and who looks after them after.')],
            'tribal': [('',
                        'Half the families who gave hides and meat for the great telling want their gifts back: the '
                        'gathering is thin, and the other bands have not come. {N}, who gathered the feast, owes '
                        'every one of them.')],
            'magic': [('',
                       "The play-merchant's ledger shows a loss every night of the season, and the company's wages "
                       "are due at the week's end. {N} put up the coin, and the coin is nearly gone.")]},
 'outcomes': (['The show survives the week, and by the end of the month the house is filling again.',
               'The run ends with every debt paid and every hand thanked, and the company leaves with its head up.'],
              ['The money runs out before the week is out, and the closing is rushed and bitter.',
               'The show stays open on hope, and the losses keep coming, now with {Ns} name on them.']),
 'options': [
    ('post the closing notice by the contracts, and pay everyone every penny owed', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'mark': 'kept your word', 'self_control': '+', 'world': {'tribal': "end the telling by custom, and give back every family's hides that can be given", 'magic': 'post the closing notice by the contracts, and pay every wage to the last copper'}, 'chance': 0.9}),
    ('study the nightly figures, and cut the shows and seats that lose most', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'count which nights the bands come, and drop the tellings nobody walks to', 'magic': 'study the takings night by night, and drop the performances that lose most'}, 'chance': 0.95}),
    ('close quietly, and sell the set and the rights to a touring producer', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': 'end the telling, and trade the masks and screens to a band that wants them', 'magic': 'close quietly, and sell the wagon, the costumes and the play to another company'}, 'chance': 0.8}),
    ('give a free night to students and nurses, and let the noise sell seats', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'open the telling free to every band for a night, and let the talk bring them', 'magic': 'open the doors free one night to students and nurses, and let the talk fill the galleries'}, 'chance': 0.65}),
    ('keep it running a fortnight, so the company has time to find other work', 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'keep the telling going a few more nights, so the players can find other hearths'}, 'chance': 0.65}),
    ('call the whole company together, and lay the real figures before them', 'W1', 'U.7', 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': 'call every player and giver to the fire, and tell them plainly what is left', 'magic': 'call the whole company together, and lay the ledger open before them'}, 'chance': 0.8}),
    ("court a new backer with a pitch built on the show's best nights", 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'grants': 'patron', 'world': {'tribal': "win over a rich family with the tale of the telling's best night", 'magic': "court a new patron with the season's best night in a glamour-crystal"}, 'chance': 0.15}),
    ('announce the last weeks loudly, and sell the closing as an event', 'B1', 'R.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'tell every band these are the last nights of the telling, and let them come running', 'magic': 'have the criers call the last nights in every square, and sell the closing as an event'}, 'chance': 0.6}),
    ('put your own savings in, to keep the company together a month longer', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, self-direction', 'binds': True, 'mark': 'took a wild risk', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'world': {'tribal': 'give your own stores to keep the players fed a moon longer', 'magic': 'put your own coin in, to keep the company together a month longer'}, 'chance': 0.8}),
    ('ask the whole company to take the same small cut for a month', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'binds': True, 'world': {'tribal': 'ask every player to take a smaller share for a moon, all alike, to keep the telling alive', 'magic': 'ask the company to take a smaller wage for a month, all alike, to keep the play alive'}, 'chance': 0.5}),
 ]},
{'name': 'an investor wants a part for a nephew',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'colleague, mentor',
 'requires': 'producer',
 'worlds': {'earth': 'lunch with an investor who will put in the last of the money if a nephew of twenty-four is '
                     'given a part',
            'tribal': 'a family that gave the feast for the telling wants its grown son in it',
            'magic': 'a patron wants a part in the season for a favoured young man of his house'},
 'timing': {'times': 'per producer a year: about 1 in 10 (estimate)'},
 'scenes': {'earth': [('',
                       'Over lunch the investor who has promised the last fifth of the money mentions a nephew: '
                       'twenty-four, just finished an acting course, very keen. Surely there is a part? The cheque '
                       "is in the investor's jacket pocket."),
                      ('W',
                       'The cast was chosen in open auditions, and {N} promised the casting director it would stay '
                       'that way.'),
                      ('U',
                       "Under the table {N} looks up the nephew's showreel on the phone. It is not terrible. It is "
                       'not good either.'),
                      ('B',
                       'Money is the oxygen of a show, and this is the last of it. Everybody in this business owes '
                       'somebody a favour.'),
                      ('R',
                       'The cheek of it. {N} feels the heat rise, and the words absolutely not are already halfway '
                       'out.'),
                      ('G',
                       'Families have always got their young into the theatre this way; half the old companies were '
                       'run by cousins. The only question is how much harm it does.')],
            'tribal': [('',
                        'The family that gave the feast for the great telling has come to {Ns} fire. Their grown son '
                        'wants a part, and without their meat there is no gathering at all.')],
            'magic': [('',
                       "Over wine in his great house, the patron who has promised the season's last purse mentions a "
                       'favoured young man of his household, and how well he would look on the stage.')]},
 'outcomes': (['The backing comes in, and the players stay the ones who won their parts.',
               'The young man finds his own level, and the one who asked is quietly glad of it.'],
              ['The backing goes elsewhere, and the show opens a fifth short.',
               'The players hear how the part was filled, and the room goes cold.']),
 'options': [
    ('refuse politely: every part in this show is cast by open audition', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'world': {'tribal': 'refuse politely: the elders choose every player in the telling, by custom', 'magic': 'refuse politely: every part in the company is won by open trial'}, 'chance': 0.65}),
    ('offer the nephew an audition like anyone else, and let the casting director decide', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'identity': True, 'world': {'tribal': 'let the son show the elders what he can do, like any other', 'magic': "offer the young man a trial like any other, and let the company's chooser decide"}, 'chance': 0.9}),
    ('give the nephew a small part with three lines, and bank the cheque', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'give the son a small part, and take the feast', 'magic': 'give the young man a small part with three lines, and take the purse'}, 'chance': 0.85}),
    ('say no with a laugh, and win the investor round over pudding', 'R1', None, 0.45, '', {'v': 'self-direction, hedonism', 'world': {'tribal': 'laugh it off at the fire, and win the family round with a song', 'magic': 'say no with a laugh, and win the patron round over the sweet wine'}, 'chance': 0.65}),
    ('give the nephew the part he wants, as theatre families always have', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'gave in to pressure', 'closed': 'approval: a part given for money against the audition rules; backfire: the cast finds out, and the casting director walks out', 'self_control': '-', 'world': {'tribal': 'give the son the part he wants, as the great families always have', 'magic': "give the young man the part he wants, as patrons' houses always have"}, 'chance': 0.85}),
    ('write it into the investment contract that money buys no say in casting', 'W1', 'U.7', 0.5, '', {'v': 'conformity, security', 'binds': True, 'world': {'tribal': 'have the elders declare before the band that a feast buys no part in the telling', 'magic': "write it into the purse's terms, under seal, that coin buys no say in casting"}, 'chance': 0.4}),
    ("look up the nephew's work, and bargain the investor down to an understudy's place", 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'watch the son play, and bargain the family down to a place among the second players', 'magic': "see the young man play, and bargain the patron down to a second's place"}, 'chance': 0.75}),
    ('play the investor off against a rival backer, so the show stays free to cast', 'B1', 'R.7', 0.5, '', {'v': 'power, self-direction', 'world': {'tribal': 'set the family against another that would give the feast, so the telling stays free', 'magic': 'play the patron off against a rival house, so the company stays free to cast'}, 'chance': 0.5}),
    ('ring the nephew yourself, and tell him straight what this would do to the company', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'go to the son yourself, and tell him straight what this would do to the players', 'magic': 'seek out the young man yourself, and tell him straight what this would do to the company'}, 'chance': 0.65}),
    ('find the nephew a job backstage, where he can learn the trade from the bottom', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'give the son work at the fires and screens, where he can learn from the bottom', 'magic': 'find the young man work in the wings, where he can learn the trade from the bottom'}, 'chance': 0.75}),
 ]},
{'name': 'you, say this line',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.1,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, colleague',
 'requires': 'background artist',
 'worlds': {'earth': 'a film set in the high street: the director points at the extra by the counter and says, you, '
                     'say this line',
            'tribal': "the shaper of the telling picks you out of the herd to speak the stag's words",
            'magic': 'the illusionist points into the procession and gives you a line to cry'},
 'timing': {'times': 'per background artist: about 1 in 20 are given a line at some point (estimate); about 8 lives '
                     'in 1,000 work as an extra (catalogue share; estimate)',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'Take nine of a scene in a cafe. {N} has spent the morning wiping the same table by the '
                       'window. Then the director, {boss}, stops, points straight at {N}, and asks for one line. The '
                       'assistant director hands over a scrap of paper with six words on it.'),
                      ('W',
                       'There are rules on a set: extras do not speak unless asked, and a line means a new contract '
                       'and a better rate, signed by a parent for anyone under eighteen. {N} knows the rules, and '
                       'now has been asked.'),
                      ('U',
                       '{N} has watched the actors all morning: how small they keep it, how the camera loves '
                       'stillness. Six words, and {N} knows exactly how they should go.'),
                      ('B',
                       'A speaking line means a better rate, a credit, maybe a listing as an actor. {N} sees a door '
                       'open a crack.'),
                      ('R',
                       '{Ns} heart is hammering so hard it must show on camera. Six words, and the whole crew '
                       'looking.'),
                      ('G',
                       '{N} came to watch a film being made in the town where {N} grew up. Now the town is in the '
                       'film, and {N} is saying its line.')],
            'tribal': [('',
                        'The great telling of the hunt is played through at dusk, the whole band as the herd. The '
                        'shaper points into the herd at {N}: the stag must speak, and {N} will speak it.')],
            'magic': [('',
                       "The illusionist's procession winds through the square under a glamour of floating lanterns. "
                       'The illusionist stops, points at {N} in the crowd, and gives {N} a line to cry as the dragon '
                       'passes.')]},
 'outcomes': (['Six words, one try, and a nod from the one in charge: {N} has a line now, and a better rate.',
               'It goes so well that {Ns} name is taken down for next time.'],
              ['{Ns} mouth goes dry, and the line is given to someone else.',
               'The line is said, and then dropped, and nobody remembers it but {N}.']),
 'options': [
    ('say it exactly as written, on your mark, as the assistant director asks', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': "speak the stag's words exactly as the shaper gives them", 'magic': 'cry the line exactly as the illusionist gives it, on your mark'}, 'chance': 0.75}),
    ('ask for ten seconds, then say it small and still, as the actors do', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'screen acting', 'world': {'tribal': 'ask a breath to think, then speak it low and still, the way the shadow wall likes', 'magic': 'ask a moment, then say it small and still, the way the glamour likes'}, 'chance': 0.65}),
    ('say it, then ask about the speaking rate and a listing with an agency', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'grants': 'casting directory listing', 'aims': 'professional actor', 'world': {'tribal': 'speak it, then ask the shaper to send your name to the other bands', 'magic': "say it, then ask to have your name put on the brokers' roll"}, 'chance': 0.75}),
    ('say it your own way, loud and alive, and add a word of your own', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': "bellow it your own way, with a stag's snort of your own on the end", 'magic': 'cry it your own way, with a flourish of your own after'}, 'chance': 0.65}),
    ('say it the way people in this town really talk', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'speak it the way your own hearth says such things', 'magic': 'say it the way the lanes of this town really talk'}, 'chance': 0.65}),
    ('get the line confirmed in writing, so the speaking rate is paid', 'W1', 'B.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "ask the shaper to say before the elders that the stag's words are yours, for the larger share", 'magic': "have the line written into your night's chit, so the speaking rate is paid"}, 'chance': 0.6}),
    ('run it under your breath while the camera resets, until it feels alive', 'U1', 'R.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'run the words under your breath while the herd forms again, until they feel alive', 'magic': 'run it under your breath while the glamour resets, until it feels alive'}, 'chance': 0.7}),
    ('say it well, then bargain to keep your neighbour in the crowd on all week', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'speak it well, then ask that your kinsman stand in the herd every night', 'magic': 'say it well, then bargain to keep your neighbour in the procession all week'}, 'chance': 0.6}),
    ('give the line away to the old extra beside you, who has waited years', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'turned down a chance', 'world': {'tribal': "give the stag's words to the old hunter beside you, who has waited years", 'magic': 'give the line to the old walk-on beside you, who has waited years'}, 'chance': 0.7}),
    ('ask the old extras by the counter how a line is done, and listen', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'mark': 'learned a skill', 'world': {'tribal': 'ask the old herd-players how the stag is spoken, and listen', 'magic': 'ask the old walk-ons how a line is cried, and listen'}, 'chance': 0.7}),
 ]},
{'name': 'fourteen hours in a field for one shot',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.1,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague, boss',
 'requires': 'background artist',
 'worlds': {'earth': 'a muddy field and a catering van: fourteen hours of waiting in the rain for one shot of a '
                     'battle',
            'tribal': 'the great telling waits all night for the moon to rise over the herd',
            'magic': 'the glamour will not hold, and the crowd waits in the square all day'},
 'timing': {'times': 'per background artist: on most shooting days outdoors (estimate)', 'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       "A five o'clock call, a muddy field, and a soldier's costume that smells of its last wearer. "
                       'It is now seven in the evening and the battle has been shot once. It is raining again, and '
                       'the tea from the van is cold.'),
                      ('W',
                       '{N} signed for the day, and the day is not over until the assistant director calls the wrap. '
                       'Lying down in a tent is not on the call sheet.'),
                      ('U',
                       '{N} has spent the hours watching how the crew works: the lights, the rain machines, why each '
                       'take is abandoned. It is a better school than any course.'),
                      ('B',
                       'The day rate is the same whether {N} stands in the mud or sits in the tent, and some of the '
                       'extras have already worked out where the cameras cannot see.'),
                      ('R', 'Cold, wet, bored past bearing. {N} would trade the whole fee for a hot bath and a bed.'),
                      ('G',
                       'An old extra, {colleague}, eighty if a day, is shivering in a thin costume. The two of them '
                       'have stood in fields like this before.')],
            'tribal': [('',
                        'The whole band stands as the herd on the hillside, waiting for the moon to rise over the '
                        'great telling. The night is cold, the little ones are asleep in the furs with their '
                        'mothers, and the moon will not come.')],
            'magic': [('',
                       "The illusionist's glamour flickers and fails again over the square. The crowd of walk-ons "
                       'has waited since dawn in their costumes, and the light is going.')]},
 'outcomes': (['The shot is got at last as the light fails, and everyone who stood in the cold gets a cheer.',
               'The day ends wet and long, and {N} goes home with the pay, a new friend and a story.'],
              ['Fourteen hours, and the scene is dropped in the end anyway.',
               '{N} comes down with a streaming cold, and misses the next two calls.']),
 'options': [
    ('stay on your mark till the wrap, and be first back after every break', 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '+', 'grants': 'reliable record', 'world': {'tribal': 'stand in the herd till the moon comes, and be first back after every rest', 'magic': 'stand in the procession till the glamour holds, first back after every break'}, 'chance': 0.25}),
    ('watch the crew all day, and learn how a shot is built', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'door': True, 'mark': 'learned a skill', 'aims': 'professional actor', 'world': {'tribal': 'watch the shapers all night, and learn how the telling is built', 'magic': 'watch the illusionists all day, and learn how a glamour is built'}, 'chance': 0.8}),
    ('slip off to the tent the cameras cannot see, and nap on the day rate', 'B1', None, 0.45, '', {'v': 'hedonism, security', 'habit': True, 'mark': 'hid a wrong', 'closed': 'approval: leaving the set while booked; backfire: the assistant director does a head count, and the agency drops the name', 'self_control': '-', 'world': {'tribal': 'slip off to the furs where the shaper cannot see, and sleep through the waiting', 'magic': "slip off to a tavern bench out of the illusionist's sight, on the night's pay"}, 'chance': 0.8}),
    ('walk off at the dinner break, and go home to a hot bath', 'R1', None, 0.45, '', {'v': 'hedonism, self-direction', 'mark': 'broke your word', 'closed': 'approval: leaving a booked day early; backfire: the agency stops calling', 'self_control': '-', 'world': {'tribal': 'walk off to your own fire before the moon rises', 'magic': 'walk off at the noon bell, and go home to a hot tub'}, 'chance': 0.95}),
    ('share your flask and your coat with the old extra shivering beside you', 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'mark': 'helped someone in need', 'world': {'tribal': 'share your furs and your broth with the old one shivering beside you', 'magic': 'share your flask and your cloak with the old walk-on shivering beside you'}, 'chance': 0.95}),
    ("report the extras hiding in the tent, and earn the assistant director's thanks", 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'mark': 'made an enemy', 'world': {'tribal': 'tell the shaper who has slipped off to sleep, and earn his thanks', 'magic': "tell the illusionist's steward who has slipped away, and earn his thanks"}, 'chance': 0.9}),
    ('teach the extras round you the battle moves as a game, to keep warm', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'teach the herd round you the stamping dance as a game, to keep warm', 'magic': 'teach the walk-ons round you the procession steps as a game, to keep warm'}, 'chance': 0.65}),
    ('trade your place in the shot for an early lift home', 'B1', 'G.7', 0.5, '', {'v': 'security, hedonism', 'world': {'tribal': 'trade your place in the herd for a seat by a warm fire', 'magic': "trade your place in the procession for a ride home on a carter's wagon"}, 'chance': 0.7}),
    ('speak up to the crowd marshal for everyone: hot tea and shelter, now', 'R1', 'W.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'speak up to the shaper for everyone: fire and broth, now', 'magic': 'speak up to the steward for everyone: mulled ale and a roof, now'}, 'chance': 0.7}),
    ('ask the old hands how they get through days like this, and do as they do', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the old herd-players how they get through such nights, and do as they do', 'magic': 'ask the old walk-ons how they bear such days, and do as they do'}, 'chance': 0.75}),
 ]},
{'name': 'the oldest member wants the lead again',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'week',
 'roles': 'elder, colleague',
 'requires': 'community theatre director',
 'worlds': {'earth': "the society's casting meeting: its oldest member wants the lead again, and can no longer keep "
                     'the lines',
            'tribal': 'the oldest player wants to wear the bear mask one more winter',
            'magic': "the pageant's eldest player wants the king's part again"},
 'timing': {'times': 'per community theatre director: about once in three years (estimate); about 3 lives in 1,000 '
                     'direct the local players (catalogue share; estimate)',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       '{elder} has been in the society for fifty-two years and has played the lead in eleven of its '
                       'plays. At the casting meeting {elder} asks for the lead in the autumn comedy, and everyone '
                       'in the room remembers the spring show, when {elder} lost the second act and the prompter had '
                       'to carry it.'),
                      ('W',
                       "The society's rule is that parts go by audition, the oldest member's included. {N} wrote "
                       'that into the constitution.'),
                      ('U',
                       '{N} knows the part: two hundred lines, quick exits, and a long speech at the end. {N} also '
                       'knows what {elder} can still do beautifully.'),
                      ('B',
                       "The society's best young actor wants the same part and could win the regional drama festival "
                       "with it. {N} would like that trophy in the society's cabinet."),
                      ('R',
                       '{elder} taught {N} to act, thirty years ago, in this same hall. The lump in {Ns} throat '
                       'comes before a word is said.'),
                      ('G',
                       'Every society has its grand old player, and every grand old player has a last part. Better '
                       'it comes kindly than by accident.')],
            'tribal': [('',
                        '{elder}, who has worn the bear mask at midwinter longer than anyone remembers, asks for it '
                        "one more winter. Last winter the telling's words went from {elder} halfway through, and the "
                        'young ones had to finish it.')],
            'magic': [('',
                       "The guild's eldest player, {elder}, asks the master of pageants for the king's part once "
                       'more. At the last feast day {elder} forgot the speech on the wagon and stood silent while '
                       'the crowd waited.')]},
 'outcomes': (['On the last night the old player gets every word right, and nobody can remember a louder night.',
               'The news is taken well, and the smaller part is played with a twinkle that steals every scene.'],
              ["The old player is hurt, and stops coming to the players' evenings.",
               'The words go again on the first night, and the audience sits through a long, kind silence.']),
 'options': [
    ('hold an open audition, and let the oldest member try for it like anyone', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'let everyone who wants the bear show it at the fire, the oldest player too', 'magic': "hold the trials for the king's part openly, the eldest player like any other"}, 'chance': 0.55}),
    ('cut the part down, and rework the scenes so the lines come in short pieces', 'U1', None, 0.45, '', {'v': 'achievement, benevolence', 'grants': 'directing actors', 'world': {'tribal': "break the bear's telling into short calls the others can answer", 'magic': "cut the king's part down, and rework the pageant so his speeches come in short pieces"}, 'chance': 0.7}),
    ('give the lead to the young actor who could win the drama festival', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'give the bear to the young player who could win the best hide at the gathering', 'magic': "give the king's part to the young player who could win the guild's laurel"}, 'chance': 0.9}),
    ('cast the oldest member anyway, and back them all the way to the last night', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'give the old player the bear mask again, and stand close by every night', 'magic': "give the eldest player the king's part again, and stand close by every feast day"}, 'chance': 0.65}),
    ("offer the oldest member the grandfather's part, one they could play asleep", 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'offer the old player the old wolf, a part they could play asleep', 'magic': 'offer the eldest player the old herald, a part they could play asleep'}, 'chance': 0.8}),
    ('cast them, and put a prompter in the wings with the book every night', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, security', 'world': {'tribal': 'give the old player the bear, and set a young one behind the screen to whisper the words', 'magic': 'give the eldest player the king, and set a prompter under the wagon with the book'}, 'chance': 0.75}),
    ('go over the lines at their kitchen table each week, with the family helping', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'habit': True, 'world': {'tribal': "go over the telling at the old player's hearth each night, with the grandchildren helping", 'magic': "go over the speeches in the eldest player's parlour each week, with the family helping"}, 'chance': 0.75}),
    ('put the casting to a committee vote, so the choice is shared', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'put the choice to the elders, so it is shared', 'magic': "put the casting to the guild's pageant committee, so the choice is shared"}, 'chance': 0.9}),
    ('tell the oldest member frankly, over a drink, what happened in the spring show', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, benevolence', 'world': {'tribal': 'tell your old friend frankly, by the fire, what happened last winter', 'magic': 'tell the eldest player frankly, over a cup, what happened at the last feast'}, 'chance': 0.85}),
    ('let the oldest member and the young star share the part on alternate nights', 'G1', 'B.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'let the old player and the young one share the bear on alternate nights', 'magic': 'let the eldest and the young player share the king on alternate feast days'}, 'chance': 0.45}),
 ]},
{'name': 'the pantomime that pays for the year',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'months',
 'roles': 'colleague, elder',
 'requires': 'community theatre director',
 'worlds': {'earth': "the committee and the bank statement: the winter pantomime pays the hall's rent for the year, "
                     'and a member has written a new play',
            'tribal': 'the old midwinter telling, or a new one a young player has made about the flood',
            'magic': 'the feast-day pageant pays for the year, or a new mystery play a journeyman has written'},
 'timing': {'times': 'per community theatre director: once a year, when the season is chosen (estimate)',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       "The committee meets round the treasurer's kitchen table with the bank statement. The "
                       "pantomime sells out every January and pays the hall's rent for the whole year. {colleague} "
                       "has written a new play about the town's closed mill, and it is good, and it may play to "
                       'empty rows.'),
                      ('W',
                       "The society's first duty is to keep the hall and the members' subscriptions safe. A society "
                       'that goes broke serves nobody.'),
                      ('U',
                       '{N} has read the new play twice. The second act needs work, but the bones are strong, and '
                       '{N} can already see how to stage it.'),
                      ('B',
                       "A new play could win the regional festival and put the society's name about. A pantomime "
                       'never wins anything except money.'),
                      ('R', 'The new play made {N} cry on the bus. {N} wants it on that stage so badly it hurts.'),
                      ('G',
                       'The pantomime belongs to the town: three generations in the audience, the same jokes, the '
                       'same dame. Children who came at four now bring their own four-year-olds.')],
            'tribal': [('',
                        "The band's midwinter telling has been the same for as long as anyone remembers, and the "
                        'families bring their gifts for it. {colleague}, a young player, has made a new telling '
                        'about the great flood, and the old ones frown.')],
            'magic': [('',
                       "The feast-day pageant fills the guild's coffer for the year, the same pageant every year. "
                       '{colleague}, a journeyman, has written a new mystery play about the plague year, and the '
                       'master of pageants has read it twice.')]},
 'outcomes': (['The house is full, the money holds, and the players argue happily about next year.',
               'The new piece finds its people, and everyone talks about it for weeks.'],
              ['The new piece plays to a few dozen a night, and the money worries begin again.',
               'The safe choice draws its crowd, and {colleague}, whose piece was passed over, quietly leaves.']),
 'options': [
    ("do the pantomime as always, and keep the society's books safe", 'W1', None, 0.45, '', {'v': 'security, conformity', 'world': {'tribal': 'give the old midwinter telling as always, and keep faith with the families who gave', 'magic': "give the feast-day pageant as always, and keep the guild's coffer safe"}, 'chance': 0.85}),
    ('try the new play as a reading first, and rework it from what you learn', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'try the new telling at a small fire first, and reshape it from what you learn', 'magic': 'try the new play as a reading in the guild hall first, and rework it from what you learn'}, 'chance': 0.75}),
    ('put on the new play, and enter it for the regional drama festival', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'aims': 'director', 'world': {'tribal': "play the new telling at the gathering, where every band's shaper will see it", 'magic': "put on the new play, and enter it for the guild's laurel"}, 'chance': 0.35}),
    ('put the new play in the main slot, and trust people to come', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'give the new telling at midwinter in place of the old, and trust the band', 'magic': 'give the new mystery play on the feast day in place of the pageant'}, 'chance': 0.4}),
    ('do the pantomime, and invite the whole town in free for the dress rehearsal', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'identity': True, 'grants': 'name on the local scene', 'world': {'tribal': "give the old telling, and invite the next band's families to the fire", 'magic': 'give the pageant, and let the poor of the ward watch the last rehearsal free'}, 'chance': 0.95}),
    ('do both: the pantomime in winter, and the new play in spring on its takings', 'W1', 'R.7', 0.5, '', {'v': 'security, stimulation', 'world': {'tribal': 'give both: the old telling at midwinter, and the new one at the thaw', 'magic': 'give both: the pageant on the feast day, and the new play in spring on its takings'}, 'chance': 0.65}),
    ('write the mill into the pantomime, so the new story reaches the old audience', 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'weave the flood into the old telling, so the new story reaches every hearth', 'magic': 'weave the plague year into the pageant, so the new story reaches the old crowd'}, 'chance': 0.6}),
    ("find a local firm to sponsor the new play, so the society's money stays safe", 'B1', 'W.7', 0.5, '', {'v': 'security, power', 'world': {'tribal': 'get a rich family to give the feast for the new telling, so the old gifts stay safe', 'magic': 'find a merchant to put up the coin for the new play, so the coffer stays safe'}, 'chance': 0.65}),
    ('run a wild workshop week where the members play scenes from the new play', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': "spend a wild week of nights playing the new telling's scenes with everyone", 'magic': 'spend a wild week where the members play scenes from the new mystery'}, 'chance': 0.9}),
    ("get the mill's old workers and their families to fill the house", 'G1', 'B.7', 0.5, '', {'v': 'achievement, tradition', 'world': {'tribal': 'tell the new telling first to the families the flood hit, and let them fill the fire', 'magic': "read the new play to the plague year's survivors, and let their families fill the benches"}, 'chance': 0.6}),
 ]},
{'name': 'a safe season or the new writers',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'artistic director',
 'worlds': {'earth': 'a board meeting about next season: the board wants the old favourites to save the money, and '
                     'the new writers were promised a stage',
            'tribal': 'the elders want the old tellings at the gathering, and the young ones have made new ones and '
                      'were promised the great fire',
            'magic': "the Order's patrons want the old masques, and the new play-makers were promised the stage"},
 'timing': {'times': 'per artistic director a year: about 1 in 3 (estimate); about 1 life in 10,000 runs a theatre '
                     "(catalogue share; 1,953 US nonprofit theatres in 2019, the US theatre network's yearly survey; "
                     'estimate)'},
 'scenes': {'earth': [('',
                       "The board's treasurer puts up a slide with the deficit in large type. The board wants a "
                       'season of old favourites: a famous comedy, a famous tragedy, a holiday show. Eighteen months '
                       'ago {N} promised three new writers a main-stage production each.'),
                      ('W',
                       "{N} gave those writers a promise in writing, with the board's own blessing at the time. A "
                       'theatre that breaks its word to writers will not be sent the next good script.'),
                      ('U',
                       '{N} has the box office history: new plays lose money in their first week and sometimes make '
                       'it back by the third. The safe season has its own risk: an audience that only grows older.'),
                      ('B',
                       "{boss}, the board's chair, decides whether {Ns} contract is renewed next year. There may be "
                       'a version of this that keeps both the board and the job.'),
                      ('R',
                       'The new plays are the reason {N} took this job. The thought of cancelling them makes {N} '
                       "want to knock the treasurer's laptop off the table."),
                      ('G',
                       'The theatre has stood in this town for ninety years, and the old plays are part of why. '
                       'People come back to them the way they come back to a well-loved song.')],
            'tribal': [('',
                        "At the gathering's council fire the elders want the old tellings: the flood, the first "
                        "hunt, the ancestor's walk. Three young players have made new tellings and were promised the "
                        'great fire. {N}, keeper of the tellings, must choose.')],
            'magic': [('',
                       "The Order's patrons send word: next season, the old masques the court loves. The new "
                       'play-makers {N} promised the stage are waiting in the antechamber.')]},
 'outcomes': (['The season is announced with the new work in it, and the people who pay for it stand behind it.',
               'A season both sides can live with is agreed, and the first new piece draws better than anyone '
               'feared.'],
              ['{N} is overruled, and the new writers hear of it from someone else.',
               'The quarrel goes public, and both sides come out of it smaller.']),
 'options': [
    ('keep the promise: the new plays go on, and tell the board so in writing', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'mark': 'kept your word', 'world': {'tribal': 'keep your word to the young ones, and say so before the elders', 'magic': 'keep your word to the play-makers, and send the Order your answer under seal'}, 'chance': 0.6}),
    ('plan a season pairing each new play with a favourite, with costed figures', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'set each new telling beside an old one, and show the elders how the nights would run', 'magic': 'plan a season pairing each new play with an old masque, with the costs reckoned'}, 'chance': 0.85}),
    ('drop the new plays quietly, please the board, and keep your contract', 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'broke your word', 'self_control': '-', 'world': {'tribal': "drop the young ones' tellings quietly, please the elders, and keep your place", 'magic': 'drop the new plays quietly, please the patrons, and keep your post'}, 'chance': 0.95}),
    ('resign over it, loudly, at the board meeting', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'mark': 'defied an authority', 'drops': 'artistic director', 'world': {'tribal': 'lay down the keeping of the tellings, loudly, at the council fire', 'magic': "throw down the master's chain, loudly, before the Order's patrons"}, 'chance': 0.9}),
    ('do the favourites well, and keep the new plays for the studio, where they began', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'give the old tellings at the great fire, and the new ones at the outer fires', 'magic': 'give the old masques in the great hall, and the new plays in the small one'}, 'chance': 0.7}),
    ('ask for a public meeting, and let the town say what its theatre is for', 'W1', 'G.7', 0.5, '', {'v': 'universalism, tradition', 'world': {'tribal': 'ask the elders to let every band speak at the gathering on which tellings it wants', 'magic': 'ask the Order for an open hearing, and let the city say what its playhouse is for'}, 'chance': 0.55}),
    ('write the new-work promise into the funding agreement, so the board must keep it', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'binds': True, 'world': {'tribal': 'have the promise to the young ones spoken before every elder, so it binds the council', 'magic': "write the new-work promise into the playhouse's charter, so the patrons must keep it"}, 'chance': 0.35}),
    ('find a foundation that funds new writing, and pay for the plays without the board', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'find a family that will give a feast for the new tellings alone', 'magic': "find a guild that pays for new plays, and stage them without the patrons' coin"}, 'chance': 0.3}),
    ('threaten to take the new writers and your name to the theatre across the river', 'R1', 'B.7', 0.5, '', {'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'threaten to take the young tellers to another gathering, and your name with them', 'magic': 'threaten to take the play-makers and your name to the rival playhouse'}, 'chance': 0.65}),
    ('bring the three writers to the board, and let them read their plays aloud', 'G1', 'R.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'bring the young ones to the council fire, and let them give their tellings', 'magic': 'bring the play-makers before the patrons, and let them read their plays aloud'}, 'chance': 0.6}),
 ]},
{'name': 'the audience that stopped coming',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'artistic director',
 'worlds': {'earth': 'a house a third full on a Tuesday night, and most of the third is over seventy',
            'tribal': "fewer bands come to the gathering's tellings each summer, and the young ones sit by the river "
                      'with their own songs',
            'magic': 'the court has found a new pleasure, and the playhouse galleries are empty on feast days'},
 'timing': {'times': 'per artistic director: most seasons have a stretch of empty houses (estimate)'},
 'scenes': {'earth': [('',
                       'Tuesday night, a good production, and the house is a third full. {N} stands at the back of '
                       'the stalls counting the empty seats: four hundred and twelve. Most of the people in the full '
                       'ones are over seventy.'),
                      ('W',
                       'A theatre the town pays for owes the whole town a reason to come in, not only the people who '
                       'always have.'),
                      ('U',
                       '{N} has the postcode figures: whole streets have never bought a ticket, and some are a '
                       'ten-minute walk from the door.'),
                      ('B',
                       "The funders' review is in the spring, and empty seats are the first thing it counts. {N} "
                       'needs a number to show {boss} and the funders.'),
                      ('R',
                       'A brilliant show playing to empty seats. {N} wants to go out and drag people in off the '
                       'street by the arm.'),
                      ('G',
                       'Audiences come and go like tides. The people in the seats tonight have come for forty years; '
                       'their grandchildren have not started yet.')],
            'tribal': [('',
                        'At the summer gathering fewer bands have come to hear the tellings than in any year {N} '
                        'remembers. The young ones sit by the river with songs of their own.')],
            'magic': [('',
                       'The court has taken up the new fashion for mirror-plays in the great houses, and the '
                       "playhouse's galleries are empty on feast days. {N}, master of the playhouse, counts the bare "
                       'benches.')]},
 'outcomes': (['By spring the house is fuller and younger, and those who pay for it are pleased.',
               'The new crowd trickles in, then comes in groups, and many of them are young.'],
              ['The seats stay empty, and those who fund the house count every one.',
               'The new crowd comes once for the novelty, and does not come back.']),
 'options': [
    ('open every Tuesday at a price anyone in town can pay', 'W1', None, 0.45, '', {'v': 'universalism', 'door': True, 'world': {'tribal': 'open the tellings to every band, with no gift asked', 'magic': 'open the playhouse every Tuesday at a price any apprentice can pay'}, 'chance': 0.75}),
    ('find out who never comes, and ask them what would bring them', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': 'go to the bands that stayed away, and ask what they would come for', 'magic': 'send runners to the wards that never come, and ask what would bring them'}, 'chance': 0.7}),
    ('cut the season by two shows, and spend the money on one big name', 'B1', None, 0.45, '', {'v': 'power, achievement', 'identity': True, 'world': {'tribal': 'give fewer tellings, and send for the most famous teller in the valley', 'magic': "cut two plays, and spend the purse on the realm's most famous player"}, 'chance': 0.7}),
    ('take the show out of the building, and play it in the market square', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'door': True, 'world': {'tribal': "take the telling to the young ones' own fire by the river", 'magic': 'take the play out of the playhouse, and give it from a cart in the market square'}, 'chance': 0.75}),
    ('take the actors round the schools, and grow the next audience slowly', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'binds': True, 'habit': True, 'grants': 'good name in town', 'world': {'tribal': 'take the tellers round every hearth with children, and grow the next listeners slowly', 'magic': 'take the players round the schools and the guild halls, and grow the next crowd slowly'}, 'chance': 0.8}),
    ('give free seats every week to the care homes and the youth clubs', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'helped someone in need', 'habit': True, 'world': {'tribal': 'give the best places at the fire to the old ones and the children of every band', 'magic': 'give free benches every week to the almshouses and the apprentices'}, 'chance': 0.9}),
    ('report the free seats as sold in the figures for the funders', 'U1', 'W.7', 0.5, '', {'v': 'security, conformity', 'self_control': '-', 'mark': 'hid a wrong', 'closed': 'approval: free seats counted as sales in a funding report; backfire: the funders audit the box office and cut the grant', 'world': {'tribal': 'tell the elders more bands came than did, so the gathering keeps its tellings', 'magic': 'enter the free benches as sold in the ledger for the Order'}, 'chance': 0.9}),
    ('bring in a famous touring company to fill the house, and study how they sell', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'world': {'tribal': 'invite a famous band of tellers to the gathering, and watch how they draw the crowd', 'magic': 'bring in a famous travelling company, and study how they fill the galleries'}, 'chance': 0.85}),
    ('stage a show the town will argue over, and let the row sell it', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'world': {'tribal': 'give a telling so bold the bands will argue over it, and let the quarrel bring them', 'magic': 'stage a play so bold the city argues over it, and let the scandal fill the galleries'}, 'chance': 0.5}),
    ('open the bar and the foyer to the town every night, music and all', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'keep a fire burning for anyone, every night, with songs and broth', 'magic': 'open the playhouse tavern to the town every night, music and all'}, 'chance': 0.7}),
 ]},
{'name': 'eight months on tour',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, home',
 'horizon': 'months',
 'roles': 'mentor, partner, colleague',
 'requires': 'professional actor',
 'worlds': {'earth': 'the agent on the phone about a national tour: a good part for eight months on the road, and a '
                     'day job that will not hold the place',
            'tribal': 'a band three valleys away wants you for the whole winter, to play the old stories at its fire',
            'magic': "a travelling company's master offers a place on the wagons for the whole season"},
 'timing': {'times': 'per professional actor a year: about 1 in 4 are offered a long tour that clashes with home or '
                     'a day job; 71 in 100 UK actors spend 28 weeks or more of a year outside the industry (the UK '
                     "actors' union's survey), and about 4 lives in 1,000 act for a living at some point (catalogue "
                     'share; estimate)'},
 'scenes': {'earth': [('',
                       '{mentor}, {Ns} agent, rings at the end of a lunch shift: a good part in a national tour of a '
                       'famous old play, eight months on the road, rehearsals in three weeks. The café manager has '
                       "said before that nobody's job is held for eight months."),
                      ('W',
                       '{N} promised the café a summer of shifts, and promised {partner} to pay a fair half of the '
                       'rent this year. Signing for the tour would be a promise to a whole company, for two hundred '
                       'nights.'),
                      ('U',
                       'The part has three real scenes and a speech in the second act that actors talk about. Two '
                       'hundred nights of it would teach {N} more than any class could.'),
                      ('B',
                       'Eight months means a wage, a credit and a director who will remember the name. {N} also '
                       "knows that the money on offer is the company's first figure, not its last."),
                      ('R',
                       'A different town every week, the digs, the van, a stage every night: {N} has wanted exactly '
                       'this since the first school play, and {Ns} heart is already packing.'),
                      ('G',
                       '{N} has only just put down roots: the allotment, Sunday lunch with the family, neighbours '
                       'who know {Ns} name. Eight months is a whole turning of the year away from all of it.')],
            'tribal': [('',
                        'A runner comes from a band three valleys away. Their teller-player died in the autumn, and '
                        'they want {N} for the whole winter, fed by every hearth, though {Ns} own band was counting '
                        'on {N} for the hunt before the snow.')],
            'magic': [('',
                       "A travelling company's master sends a letter under a wax seal: a place on the wagons for the "
                       'whole season, a real part and a share of the takings. The workshop where {N} earns the rent '
                       'will not keep a bench empty for a season.')]},
 'outcomes': (['The choice is made in good time, and everyone it touches hears it from {N} first.',
               'Months later {N} looks back on the decision and would make it again.'],
              ['The plan falls apart within the month, and {N} is left with neither the part nor the work at home.',
               '{mentor} takes it badly, and the next offer is a long time coming.']),
 'options': [
    ('take it, and work every shift until you go, so the café is not short', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'mark': 'kept your word', 'world': {'tribal': 'take it, and hunt every day until you go, so your hearth is not short', 'magic': 'take it, and work at the bench every day until you go, so the workshop is not short'}, 'chance': 0.9}),
    ('take it for the part, and plan how to grow it over two hundred nights', 'U1', None, 0.45, '', {'binds': True, 'v': 'achievement, self-direction', 'mark': 'learned a skill', 'aims': 'lead actor or actress', 'world': {'tribal': 'take it for the telling, and plan how to grow it over the long nights', 'magic': 'take it for the part, and plan how to grow it over a season of nights'}, 'chance': 0.7}),
    ('have the agent push for more money and better billing before saying yes', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'ask the other band for more gifts and a better place at its fire first', 'magic': 'have a broker push the master for a bigger share and a higher place on the bill'}, 'chance': 0.6}),
    ('say yes on the spot, and walk out of the café mid-shift without notice', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'binds': True, 'mark': 'broke your word', 'closed': 'approval: a job left without the notice agreed; backfire: the café will not take the actor back when the tour ends', 'world': {'tribal': 'say yes to the runner on the spot, and leave the hunting party without a word', 'magic': 'say yes to the master at once, and walk out of the workshop mid-task without a word'}, 'chance': 0.95}),
    ('turn it down: the people at home come first this year', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'identity': True, 'mark': 'turned down a chance', 'world': {'tribal': 'turn it down: your own band and its hunt come first this winter'}, 'chance': 0.9}),
    ('ask the company for six months instead, so you are home by the summer', 'W1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'world': {'tribal': 'ask the other band to send you home at the thaw, before the spring hunt', 'magic': 'ask the master to release you at midsummer, so you are home for the harvest'}, 'chance': 0.25}),
    ('take it, and train a friend to take over your shifts at the café', 'U1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'self_control': '+', 'world': {'tribal': 'take it, and teach a young hunter to take your place in the hunt', 'magic': 'take it, and train an apprentice to keep your bench while you are away'}, 'chance': 0.55}),
    ('ask the agent to get you covering the lead too, and learn it on the road', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'aims': 'understudy', 'world': {'tribal': "ask to learn the great mask's telling too, in case its wearer falls sick", 'magic': 'ask the master to make you second to the leading player, and learn that part too'}, 'chance': 0.6}),
    ('ring the director yourself, and ask to read for the bigger part', 'R1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "go to the other band's shaper yourself, and ask to play the bigger spirit", 'magic': 'go to the master of the play yourself, and ask to read for the leading part'}, 'chance': 0.4}),
    ('take it, and make the company and the digs your home for eight months', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'door': True, 'grants': 'a company that feels like family', 'world': {'tribal': "take it, and make the other band's fire your own for the winter", 'magic': 'take it, and make the wagons and the company your family for the season'}, 'chance': 0.35}),
 ]},
{'name': 'a self-tape due by nine tomorrow',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, home',
 'horizon': 'moment',
 'roles': 'mentor, friend',
 'requires': 'professional actor',
 'worlds': {'earth': 'a spare room turned into a studio with a bedsheet: two scenes for a new series, to be taped by '
                     'nine tomorrow',
            'tribal': 'the elders want to see your telling of the bear before the gathering, and there is one '
                      'evening to make it ready',
            'magic': 'the company master wants a glamour-sketch of your best scene by the morning bell'},
 'timing': {'times': 'per professional actor: most months in a working year; most screen castings now begin with a '
                     'recorded audition (estimate)'},
 'scenes': {'earth': [('',
                       'At four in the afternoon {mentor} forwards the email: two scenes for a new series, a '
                       'self-tape by nine tomorrow morning. {N} has a phone, a pile of books to stand it on, a '
                       'bedsheet pinned to the wall, and nobody yet to read the other lines.'),
                      ('W',
                       'The casting brief is exact: a clear slate, two scenes, no cuts, a plain background, the file '
                       'named just so. {N} reads it twice and means to follow it to the letter.'),
                      ('U',
                       '{N} breaks the scenes down beat by beat: what the character wants, what stands in the way, '
                       'where the turn comes. Then {N} looks at the clock.'),
                      ('B',
                       'Two hundred actors will send a tape for this part, and the casting office will watch the '
                       'first ten seconds of most of them. {N} needs those ten seconds to land.'),
                      ('R',
                       'The second scene has a moment in it that makes {N} want to shout. It is also eleven at night '
                       'already.'),
                      ('G',
                       'It is only a phone, a sheet and a lamp. {N} would rather say the lines the way people really '
                       'talk at home than act them at a lens.')],
            'tribal': [('',
                        'The elders want to see {Ns} telling of the bear before they choose the players for the '
                        'gathering. There is one evening, one small fire, and nobody yet to play the hunter '
                        'opposite.')],
            'magic': [('',
                       'The company master wants a glamour-sketch of {Ns} best scene by the morning bell: a few '
                       'minutes of it caught in a palm-sized crystal by the sketch-maker in the next street, if {N} '
                       'can be ready before the shop shuts.')]},
 'outcomes': (['The scene is ready in time, and it is a good one.',
               'Two days later word comes back: they want to see {N} in person.'],
              ['It is not ready in time, and the chance goes to someone else.',
               'Nothing comes back, not even a no, as with most who try.']),
 'options': [
    ('follow the casting brief to the letter: a clear slate, two scenes, no cuts', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': "follow the elders' wishes to the letter: the bear, the hunter, nothing added", 'magic': "follow the master's instructions to the letter: one scene, plainly played"}, 'chance': 0.85}),
    ('do ten takes of each scene, and send the one that finds something new', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'habit': True, 'grants': 'screen acting', 'world': {'tribal': 'tell the bear ten ways by the fire, and keep the one that finds something new', 'magic': 'rehearse it ten ways, and give the sketch-maker the one that finds something new'}, 'chance': 0.7}),
    ('cut a stumble from the middle, so it looks like one clean take', 'B1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': 'approval: an edited tape where the brief asks for one take; backfire: the casting office spots the cut and stops calling the agent', 'world': {'tribal': 'ask a friend to tell the elders you never once miss a word, though you stumble', 'magic': 'pay the sketch-maker to smooth a stumble out of the glamour'}, 'chance': 0.8}),
    ('do it once, straight, at midnight, and send it off before doubt sets in', 'R1', None, 0.45, '', {'v': 'stimulation', 'world': {'tribal': 'tell it once, straight, and go to the elders before doubt sets in', 'magic': 'play it once, straight, and have it caught before doubt sets in'}, 'chance': 0.75}),
    ('skip this one, and spend the evening at supper with the family', 'G1', None, 0.45, '', {'habit': True, 'self_control': '-', 'v': 'benevolence, tradition', 'mark': 'turned down a chance', 'chance': 0.9}),
    ('ask a friend to read the other lines, and cook them supper for it', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'made a friend', 'world': {'tribal': 'ask a friend to play the hunter, and share your meat with them after'}, 'chance': 0.7}),
    ('learn both scenes word-perfect before pressing record', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'self_control': '+', 'world': {'tribal': 'learn the telling word for word before you go to the elders', 'magic': 'learn the scene word-perfect before you go to the sketch-maker'}, 'chance': 0.75}),
    ('ring a casting assistant you know, and ask what they are really looking for', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'door': True, 'world': {'tribal': 'ask a friend of the elders what they are really looking for', 'magic': 'ask a friend in the company what the master is really looking for'}, 'chance': 0.7}),
    ('make a bold choice the brief never asked for, to stand out from the pile', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'aims': 'lead actor or actress', 'grants': 'auditioning', 'world': {'tribal': 'make the bear do something no teller has made him do, to stand out', 'magic': 'play the scene in a way no player has, to stand out from the others'}, 'chance': 0.6}),
    ('tape it in the garden at dusk, where the scene feels real', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'tell it out under the trees at dusk, where the bear feels near', 'magic': 'play it in the orchard at dusk, where the scene feels real'}, 'chance': 0.55}),
 ]},
{'name': 'the producers want a star for the transfer',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, mentor, colleague',
 'requires': 'lead actor or actress',
 'worlds': {'earth': 'a meeting with the producers about the transfer: the show moves to a bigger theatre, and they '
                     'want a famous name in your part',
            'tribal': 'the chief of another band wants his own son behind the great mask',
            'magic': 'a noble patron wants a famous player in your part for the court season'},
 'timing': {'times': 'per lead a year: about 1 in 10 meet a move or a recast that puts their part in doubt; about 1 '
                     'life in 1,000 plays a lead in a paid production (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'The show is a hit, and it is moving to a big theatre in the capital. Over coffee {boss}, the '
                       'lead producer, explains that a bigger house needs a famous name above the title, and that '
                       'the famous name they have in mind wants {Ns} part.'),
                      ('W',
                       '{N} signed for this run and has played every night of it, as the contract asked. The '
                       'contract says nothing at all about a transfer, and {N} has read it three times today.'),
                      ('U',
                       '{N} built this part over a year: every pause, every turn in the second act. A famous name '
                       'would get the role, but not the hundred small discoveries inside it.'),
                      ('B',
                       'The producers want what sells, and a famous name sells. {N} wonders what {Ns} own name would '
                       'need to be worth for the answer to change, and who could make it worth that.'),
                      ('R',
                       'It is {Ns} part. {N} found it, bled for it and made the show a hit with it, and the thought '
                       'of someone else saying those lines is unbearable.'),
                      ('G',
                       'Shows move, parts pass from hand to hand, and the play is older than anyone in it. The '
                       'company is what {N} would miss.')],
            'tribal': [('',
                        'The chief of a larger band has come to the gathering with gifts, and asks that his own son '
                        'wear the great mask this summer. {N} has worn it for two summers, and the elders look at '
                        'the gifts, and then at {N}.')],
            'magic': [('',
                       'A noble patron will take the company to court for the winter season, and wants a famous '
                       'player from the capital in {Ns} part. The master of the play does not meet {Ns} eyes when he '
                       'says it.')]},
 'outcomes': (['The question is settled, and {N} can live with how it was settled.',
               'The company stands by {N}, and the months that follow are better than the ones before.'],
              ['The transfer goes ahead with a famous name in the part, and {N} hears of it with everyone else.',
               'The quarrel leaves a mark on the company, and the last weeks of the run are cold.']),
 'options': [
    ('put in writing what you were promised, and ask them to keep their word', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'remind the elders, before the whole band, what was promised at the last gathering', 'magic': 'set out in a sealed letter what you were promised, and ask the patron to keep his word'}, 'chance': 0.35}),
    ('show them the box office: the houses were full before any famous name', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'remind the elders how the bands came from every valley to see your telling', 'magic': 'show the master the takings: the benches were full before any famous name'}, 'chance': 0.45}),
    ('ask the agent for an hour alone with the lead producer, and make your case', 'B1', None, 0.45, '', {'v': 'power, achievement', 'grants': 'a producer who backs you', 'world': {'tribal': "ask the go-between who speaks for you to win you a night at the chief's fire", 'magic': 'have your broker win you an hour with the patron, and make your case'}, 'chance': 0.25}),
    ('tell them to their faces that you will fight to keep the part', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'mark': 'defied an authority', 'world': {'tribal': 'stand up at the fire, and say you will fight to keep the great mask', 'magic': 'tell the master and the patron to their faces that you will fight for the part'}, 'chance': 0.35}),
    ('step aside with grace, and wish the new lead well', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'drops': 'lead actor or actress', 'world': {'tribal': "hand the great mask to the chief's son with grace, and wish him well", 'magic': 'step aside with grace, and wish the famous player well'}, 'chance': 0.9}),
    ('offer to take the famous name through the part, scene by scene', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'benevolence, achievement', 'world': {'tribal': "offer to teach the chief's son the telling, step by step", 'magic': 'offer to take the famous player through the part, scene by scene'}, 'chance': 0.7}),
    ('find the clause in your contract that promises first refusal on a transfer', 'U1', 'B.7', 0.5, '', {'v': 'power, security', 'world': {'tribal': 'call on the old custom that the mask stays with its wearer while the elders are pleased', 'magic': "find the clause in the company's charter that promises first claim on the part"}, 'chance': 0.4}),
    ('leak the recast to the papers, so the fans kick up a fuss', 'B1', 'R.7', 0.5, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: briefing the press against the producers; backfire: the leak is traced, and the transfer goes ahead without the lead', 'world': {'tribal': 'tell the singers the chief is buying the mask, so the young ones make a noise', 'magic': 'slip the recast to the broadsheets, so the galleries make a noise'}, 'chance': 0.6}),
    ('go straight to the company, and tell them what the producers said in confidence', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, self-direction', 'mark': 'broke your word', 'closed': 'approval: a private meeting told to the company; backfire: the producers stop telling the lead anything', 'world': {'tribal': 'go straight to the other players, and tell them what the elders said in private', 'magic': 'go straight to the company, and tell them what the master said in confidence'}, 'chance': 0.9}),
    ('let the whole company go to the producers together, on your behalf', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': "let the band's players go to the elders together, on your behalf", 'magic': 'let the whole company go to the patron together, on your behalf'}, 'chance': 0.4}),
 ]},
{'name': 'a cast member in trouble on the night',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'moment',
 'roles': 'colleague, boss',
 'requires': 'lead actor or actress',
 'worlds': {'earth': 'the dressing room at the half: a fellow actor is in no state to go on, and the curtain is in '
                     'thirty-five minutes',
            'tribal': 'a young player shakes behind the hide screen before the telling',
            'magic': 'a fellow player has been at the wine before the masque'},
 'timing': {'times': 'per lead: a few times in a run, a member of the company is unwell or not fit on the night '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'At the half, thirty-five minutes before curtain up, {colleague} is sitting on the '
                       'dressing-room floor, grey and shaking. It might be a fever, or stage fright, or the two '
                       'glasses of wine at lunch, and {colleague} will not say which.'),
                      ('W',
                       'The stage manager needs to know, now, who is fit to go on; that is how a company keeps faith '
                       'with nine hundred people who paid. {N} is also the one in the company {colleague} trusts '
                       'most.'),
                      ('U',
                       "{N} watches {colleague}'s hands and eyes, listens to the breathing, and starts to sort fever "
                       'from fear from drink.'),
                      ('B',
                       'The critics are in tonight. If the second act falls apart, it will be {Ns} name in the '
                       "reviews, not {colleague}'s."),
                      ('R',
                       '{N} drops down on the floor beside {colleague} without a thought. Whatever this is, nobody '
                       'should sit through it alone.'),
                      ('G',
                       'Every company has a night like this sooner or later. {N} has seen older actors carried '
                       'through worse by the people around them.')],
            'tribal': [('',
                        "Behind the hide screen, the young player who is to be the crow in tonight's telling is "
                        'shaking so hard the feathers rattle. The whole band is already sitting at the fire.')],
            'magic': [('',
                       'In the tiring-room before the masque, {colleague} smells of the wine cellar and laughs at '
                       'nothing. Beyond the curtain, the court is taking its seats.')]},
 'outcomes': (['The play begins on time, and nobody watching knows how close it came.',
               '{colleague} gets through the night, and the next morning thanks {N} quietly.'],
              ['The second act falls apart, and everyone watching can tell.',
               '{colleague} blames {N} for how it was handled, and the company takes sides.']),
 'options': [
    ('tell the stage manager now, so the understudy can be warned in time', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'tell the keeper of the fire now, so another can be ready to play the crow', 'magic': 'tell the book-keeper now, so the second can be warned in time'}, 'chance': 0.85}),
    ('find out what it is, fever, fear or drink, before anyone decides', 'U1', None, 0.45, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'find out what it is, fever or fear, before anyone decides'}, 'chance': 0.85}),
    ('tell the producers it was drink, true or not, to be rid of a rival', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: a rumour spread about a colleague; backfire: the company finds out who started it', 'world': {'tribal': 'tell the elders the young one is not fit to play, true or not, to be rid of a rival', 'magic': 'tell the master it was the wine, true or not, to be rid of a rival'}, 'chance': 0.85}),
    ("sit on the floor with them, and talk them down until the beginners' call", 'R1', None, 0.45, '', {'v': 'benevolence', 'mark': 'helped someone in need', 'world': {'tribal': 'crouch behind the screen with the young one, and talk them calm until the drums', 'magic': 'sit with them in the tiring-room, and talk them steady until the bell'}, 'chance': 0.75}),
    ('make tea, open a window, and let the company look after its own', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': "bring water, and let the band's old players look after their own", 'magic': 'send for water and bread, and let the company look after its own'}, 'chance': 0.6}),
    ("ask the stage manager to keep tonight out of the show report, for the company's name", 'W1', 'U.7', 0.5, '', {'v': 'security, conformity', 'mark': 'hid a wrong', 'closed': 'approval: a night kept out of the show report; backfire: front of house tells the producers, and the cover-up costs more than the night', 'world': {'tribal': "ask the keeper of the fire to keep the night from the elders, for the band's name", 'magic': "ask the book-keeper to keep the night out of the ledger, for the company's name"}, 'chance': 0.7}),
    ('plan how to carry their scenes, and take the best moments for yourself', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.9}),
    ('send out for strong coffee, and get them on stage whatever it takes', 'B1', 'R.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'give the young one honey and cold water, and get them out there whatever it takes', 'magic': 'send for strong tea, and get them on whatever it takes'}, 'chance': 0.85}),
    ('cover for them on stage: feed them every line, and hold the scene together', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'grants': 'a company that feels like family', 'world': {'tribal': 'cover for them in the telling: speak their words with them, and hold it together'}, 'chance': 0.6}),
    ('ask the oldest hand in the company to sit with them, as the old companies did', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'ask the oldest player of the band to sit with them, as the old ones always have'}, 'chance': 0.7}),
 ]},
{'name': 'the understudy rehearsal nobody watches',
 'stages': 'young_adult adult mature',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'understudy',
 'worlds': {'earth': 'an understudy call in an empty theatre: Thursday afternoon, the deputy stage manager with the '
                     'book, and nobody in the stalls',
            'tribal': "you practise the great mask's telling alone by the river",
            'magic': 'a rehearsal by lamplight in an empty playhouse'},
 'timing': {'times': 'per understudy: most weeks of a run; big shows hold understudy rehearsals weekly (estimate)'},
 'scenes': {'earth': [('',
                       'Thursday at two: the understudy call. The deputy stage manager has the book open in the '
                       'front row, the other covers are marking it through in their coats, and the stalls are empty. '
                       '{boss}, the director, has not come to one of these since the first week.'),
                      ('W',
                       "Every line, every cue, every exit at the same pace as the lead's: if the call ever comes, "
                       'the company must not feel the change. {N} treats the empty stalls as a full house.'),
                      ('U',
                       '{N} has watched the lead from the wings for six weeks and knows where the part is still '
                       'unfinished. Thursday afternoons are the only time to try something else.'),
                      ('B',
                       'Nobody who matters is in the building. {N} wonders what it would take to get someone who '
                       'matters into the stalls next Thursday.'),
                      ('R',
                       'Marking it through in a coat is no way to play a part. {N} wants to tear into the big scene '
                       'at full voice, empty seats or not.'),
                      ('G',
                       'The empty theatre is quiet and old, and its dust smells of a hundred years of matinees. {N} '
                       'likes these afternoons better than the shows.')],
            'tribal': [('',
                        "Away from the camp, by the river, {N} speaks the great mask's telling aloud to the water "
                        'and the reeds. If its wearer falls sick before the gathering, it will be {N} under the '
                        'mask.')],
            'magic': [('',
                       'In the empty playhouse, by the light of a single lamp, the book-keeper reads the cues and '
                       "{N} walks the leading player's part. The master of the play has not come to watch since the "
                       'first week.')]},
 'outcomes': (['By the end of the afternoon the part sits a little deeper, and {N} knows it.',
               'Someone who matters hears about the afternoon, and remembers {Ns} name.'],
              ['The afternoon drifts by, and nothing in the part has moved.',
               '{boss} hears the wrong story about the afternoon, and says so in front of the company.']),
 'options': [
    ('work it like a first night: every line, every cue, at full pace', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'grants': 'learning lines', 'world': {'tribal': 'tell it as if the whole gathering were watching: every word, every step'}, 'chance': 0.8}),
    ('try the big scene three new ways, and note what each one finds', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': "try the ancestor's great speech three new ways, and remember what each one finds"}, 'chance': 0.8}),
    ('ask the director to come next Thursday, and make sure the producer hears of it', 'B1', None, 0.45, '', {'v': 'power, achievement', 'aims': 'lead actor or actress', 'world': {'tribal': 'ask the shaper of the telling to come and watch, and make sure the elders hear of it', 'magic': 'ask the master of the play to come next week, and make sure the patron hears of it'}, 'chance': 0.55}),
    ('play the big scene at full voice, as if the house were full', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': "roar the ancestor's speech at the river, as if the whole gathering were listening"}, 'chance': 0.85}),
    ('spend the afternoon with the family, and let a fellow cover sign your name', 'G1', None, 0.45, '', {'v': 'benevolence, security', 'mark': 'hid a wrong', 'closed': 'approval: signing in for a call not attended; backfire: the deputy stage manager counts heads, and the producers hear', 'world': {'tribal': 'stay at your hearth instead of going to the river, and let a friend say you went', 'magic': 'stay home instead, and have a friend mark you present in the call book'}, 'chance': 0.7}),
    ('keep a log of every call and every note, to show when a part comes up', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'keep every telling in memory, to show the elders when a mask comes free', 'magic': 'keep a ledger of every call, to show the master when a part comes up'}, 'chance': 0.75}),
    ('make the part your own, and find the moments the lead has never found', 'U1', 'R.7', 0.5, '', {'identity': True, 'v': 'self-direction', 'aims': 'lead actor or actress', 'chance': 0.7}),
    ('make a deal with the other covers: mark it through, and all go home early', 'B1', 'G.7', 0.5, '', {'v': 'hedonism, security', 'world': {'tribal': 'make a deal with the other young ones: walk it through, and all go back to the hearth early', 'magic': 'make a deal with the other covers: walk it through, and all go home before the lamps are lit'}, 'chance': 0.9}),
    ('get the other covers to play it properly too, not mark it in their coats', 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': 'get the other young players to come to the river and practise properly too', 'magic': 'get the other seconds to play it properly too, not mumble it by the lamp'}, 'chance': 0.6}),
    ('sit in the stalls and watch the other covers work, and learn from them', 'G1', 'U.7', 0.5, '', {'v': 'achievement, universalism', 'world': {'tribal': 'sit on the bank and watch the other young players, and learn from them', 'magic': 'sit in the pit and watch the other seconds work, and learn from them'}, 'chance': 0.75}),
 ]},
{'name': 'the lead plays through a fever',
 'stages': 'young_adult adult mature',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague, boss',
 'requires': 'understudy',
 'worlds': {'earth': 'the wings during the first act: the lead has gone on ill, and you are in half-costume, ready',
            'tribal': 'the wearer of the great mask is burning with fever at the gathering',
            'magic': 'the leading player coughs through the first act of the court masque'},
 'timing': {'times': 'per understudy: once or twice a run; about 1 professional actor in 3 understudies at some '
                     'point (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       '{colleague}, the lead, went on tonight with a fever and a throat full of honey. From the '
                       'wings {N} watches every exit get slower. {N} is in half-costume and word-perfect, and nobody '
                       'has called for the understudy.'),
                      ('W',
                       'The rules are plain: the stage manager decides who goes on, and the lead decides whether to '
                       'try. {N} is ready, and readiness is all the job asks.'),
                      ('U',
                       '{N} counts the breaths between lines and hears the voice crack on the high notes. By the '
                       'long speech in the second act, it will not hold.'),
                      ('B',
                       'The producer is in the house tonight. If {colleague} falters, {N} will play the last hour of '
                       'the show in front of the one person who decides who gets the lead.'),
                      ('R',
                       'Watching {colleague} struggle out there is awful, and {N} cannot tell whether the knot in '
                       '{Ns} stomach is pity or hunger.'),
                      ('G',
                       '{colleague} has played this part three hundred times and loves it the way some people love a '
                       'house. Some nights the body says no, and it is wiser to listen.')],
            'tribal': [('',
                        'The wearer of the great mask is burning with fever, and the summer gathering is waiting at '
                        'the great fire. {N} has learned the telling by the river all spring, and stands in the dark '
                        'at the edge of the light.')],
            'magic': [('',
                       'The leading player has coughed through the first act of the court masque, and the patron in '
                       'the royal box has noticed. {N}, the second, waits in the wings with the book in a shaking '
                       'hand.')]},
 'outcomes': (['The night is got through, one way or another, and the company is still in one piece.',
               'Whoever plays the last act plays it well, and {boss} notices who was ready.'],
              ['The second act is a struggle from start to finish, and everyone watching can tell.',
               '{colleague} hears what {N} did in the wings, and does not speak to {N} for a week.']),
 'options': [
    ('stay ready and quiet in the wings, and leave the call to the stage manager', 'W1', None, 0.45, '', {'v': 'conformity', 'aims': 'lead actor or actress', 'world': {'tribal': 'stay ready in the dark at the edge of the light, and leave the choice to the elders', 'magic': 'stay ready in the wings, and leave the call to the book-keeper'}, 'chance': 0.9}),
    ('tell the stage manager exactly where the voice will go in the second act', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'tell the keeper of the fire exactly where the fever will take him in the long telling', 'magic': 'tell the book-keeper exactly where the voice will fail in the second act'}, 'chance': 0.75}),
    ('make sure the producer knows you are ready, before the second act', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'make sure the elders see you painted and ready, before the long telling', 'magic': "make sure the patron's steward knows the second is ready, before the second act"}, 'chance': 0.7}),
    ('go to the lead at the interval, and beg them to rest', 'R1', None, 0.45, '', {'v': 'benevolence', 'world': {'tribal': 'go to the masked one between the tellings, and beg him to rest', 'magic': 'go to the leading player at the interval, and beg them to rest'}, 'chance': 0.45}),
    ('wait and hope, and let the night go the way it goes', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'chance': 0.5}),
    ('warm up in full costume, so the director sees a cover ready to go', 'W1', 'B.7', 0.5, '', {'v': 'achievement', 'grants': 'a director who keeps casting you', 'world': {'tribal': 'put on the paint and the skins, so the shaper sees one ready to go', 'magic': "dress in the leading player's spare costume, so the master sees a second ready to go"}, 'chance': 0.25}),
    ('hint to the stage manager that the lead asked to come off, which is untrue', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, self-direction', 'mark': 'hid a wrong', 'closed': 'approval: a lie to the stage manager about the lead; backfire: the lead finishes the show, and the company finds out', 'world': {'tribal': 'tell the keeper of the fire the masked one asked to stop, though he did not', 'magic': 'hint to the book-keeper that the leading player asked to come off, though it is untrue'}, 'chance': 0.45}),
    ('offer the lead a deal: rest the second act, and still take the bow', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'offer the masked one a bargain: rest the long telling, and still be praised at the end', 'magic': 'offer the leading player a bargain: rest the second act, and still take the bow'}, 'chance': 0.55}),
    ('tell the company in the wings you are ready, and lift them for the second act', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'tell the other players you are ready, and lift them for the long telling'}, 'chance': 0.8}),
    ('ask the old dresser what the lead did the last time this happened', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the oldest woman of the band what the masked one did the last time fever came', 'magic': 'ask the old wardrobe-mistress what the leading player did the last time'}, 'chance': 0.75}),
 ]},
{'name': 'the voice teacher and the accent from home',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'school, family',
 'horizon': 'months',
 'roles': 'mentor, parent, colleague',
 'requires': 'drama school student',
 'worlds': {'earth': 'a voice class in a room with a piano: the voice teacher says the accent from home has to go',
            'tribal': "the old teller says you speak like your mother's band, not like a teller",
            'magic': "the guild school's master of voice corrects your street speech"},
 'timing': {'times': 'per drama school student: once or twice a course; voice work is in every accredited course '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'In the voice room, by the piano, {mentor}, the voice teacher, stops {N} halfway through the '
                       'speech. The vowels are lovely, {mentor} says, and they are from home, and most of the parts '
                       '{N} will be seen for will want something else.'),
                      ('W',
                       "The school's method is the method: a neutral voice first, everything else built on top of "
                       'it. {N} came here to be trained, and training means doing what the voice room asks.'),
                      ('U',
                       '{N} can hear the difference now, sound by sound: the dropped letters, the vowels at the back '
                       'of the throat. It is a puzzle of the mouth, and {N} wants to solve it.'),
                      ('B',
                       'The actors who work most can do any voice at all. An accent is a tool, and {N} wants every '
                       'tool there is.'),
                      ('R',
                       'It is how {Ns} grandmother talks, and {Ns} mother, and the whole street. Being told to scrub '
                       'it out makes {Ns} face burn.'),
                      ('G',
                       'The accent carries the place {N} grew up in: the market, the chapel, the songs at weddings. '
                       '{N} rings home every Sunday and hears it at the other end of the line.')],
            'tribal': [('',
                        "The old teller stops {N} by the fire: {N} speaks the tellings like a child of {Ns} mother's "
                        'band, with its soft endings, and a teller must sound like the ancestors themselves.')],
            'magic': [('',
                       "The guild school's master of voice taps the lectern: {Ns} street speech from the lower town "
                       'will not do for kings and queens, and must be mended by the winter assessment.')]},
 'outcomes': (['By the end of the season {N} has a voice that does what the work asks, and has not lost the one from '
               'home.',
               "{mentor} hears the speech again at the season's end, nods, and says nothing more about it."],
              ['The new voice will not come, and now the old one sounds wrong to {N} as well.',
               '{parent} hears the new voice, and goes quiet for a long moment.']),
 'options': [
    ('do the drills every morning until the trained voice comes without thinking', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'habit': True, 'self_control': '+', 'world': {'tribal': 'say the tellings every dawn as the old teller does, until it comes without thinking', 'magic': 'drill the court speech every morning until it comes without thinking'}, 'chance': 0.8}),
    ('learn both: the trained voice for work, and the home voice kept sharp', 'U1', None, 0.45, '', {'aims': 'lead actor or actress', 'identity': True, 'v': 'achievement, self-direction', 'grants': 'accents and voices', 'mark': 'learned a skill', 'world': {'tribal': "learn both: the teller's voice for the fire, and your mother's band's voice kept sharp", 'magic': 'learn both: the court speech for the stage, and the street speech kept sharp'}, 'chance': 0.65}),
    ('learn the trained voice and three more, so you can be cast in anything', 'B1', None, 0.45, '', {'self_control': '+', 'v': 'achievement, power', 'world': {'tribal': "learn the teller's voice and the voices of three other bands, to be asked for anywhere", 'magic': "learn the court speech and three more of the realm's, to be cast in anything"}, 'chance': 0.6}),
    ('argue: the great parts can be played in the voice you were born with', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'defied an authority', 'world': {'tribal': 'argue: the ancestors can speak in the voice you were born with'}, 'chance': 0.35}),
    ('keep it: the accent is home, and home belongs in the work', 'G1', None, 0.45, '', {'v': 'tradition', 'identity': True, 'world': {'tribal': "keep it: your mother's band is in your voice, and belongs in the telling", 'magic': 'keep it: the lower town is in your voice, and belongs on the stage'}, 'chance': 0.7}),
    ('ask for a fair hearing: one speech in your own voice, judged on its truth', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'world': {'tribal': 'ask the old teller to hear one telling in your own voice, and judge it fairly', 'magic': 'ask the master of voice to hear one speech in your own voice, judged on its truth'}, 'chance': 0.5}),
    ('record your grandmother talking, and study what makes the home voice sing', 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'door': True, 'world': {'tribal': "sit with the old women of your mother's band, and learn what makes their voice sing", 'magic': 'sit with your grandmother in the lower town, and study what makes the street speech sing'}, 'chance': 0.9}),
    ("bargain: the trained voice in class, if the school's shows cast home voices too", 'B1', 'W.7', 0.5, '', {'v': 'universalism, power', 'world': {'tribal': 'bargain with the old teller: his voice at the great fire, your own at the small ones', 'magic': "bargain with the master: court speech in class, if the guild's plays use street speech too"}, 'chance': 0.45}),
    ('go home for a weekend, and play the speech to the family in both voices', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, benevolence', 'world': {'tribal': "go back to your mother's band for a moon, and tell them the story in both voices", 'magic': 'go home to the lower town, and play the speech to the family in both voices'}, 'chance': 0.8}),
    ('keep the accent, and make it the thing casting directors remember', 'G1', 'B.7', 0.5, '', {'v': 'achievement, tradition', 'aims': 'professional actor', 'world': {'tribal': "keep your mother's band's voice, and make it the thing every band remembers", 'magic': 'keep the street speech, and make it the thing every company master remembers'}, 'chance': 0.55}),
 ]},
{'name': 'the money runs out in the second year',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'money, school',
 'horizon': 'months',
 'roles': 'parent, friend, mentor',
 'requires': 'drama school student',
 'worlds': {'earth': 'a letter from the bank in the second year: the fees, the rent, and a bar job four nights a '
                     'week',
            'tribal': "the winter is long and the old teller's family has little meat to share",
            'magic': 'the bursary runs dry and the guild wants its fee'},
 'timing': {'times': 'per drama school student: about 1 in 4 run short in the course; many accredited courses charge '
                     'full fees and leave living costs to the student (estimate)'},
 'scenes': {'earth': [('',
                       'The letter from the bank comes in the second spring: the overdraft is at its limit, the rent '
                       "is due, and next year's fees after that. {N} already works four nights a week behind a bar "
                       'and sleeps through the first class on Mondays.'),
                      ('W',
                       '{N} signed for the fees and the rent, and owes both. Debts are debts, and {N} means to pay '
                       'them, somehow, on time.'),
                      ('U',
                       "{N} puts every figure into a spreadsheet: the fees, the rent, the bar's wages, the hours "
                       'left in a week. The sum does not work, and {N} keeps trying it different ways.'),
                      ('B',
                       "Money is a problem with solutions, and some of them are in the small print of the school's "
                       'own funds. {N} starts looking for who has money and what they want for it.'),
                      ('R',
                       '{N} is sick of counting coins at the supermarket till and sick of the bar. Some nights {N} '
                       'wants to throw it all in and go and live.'),
                      ('G',
                       '{Ns} family back home has little to spare, and would give it anyway. {N} knows what it would '
                       'cost them, and that they would never say.')],
            'tribal': [('',
                        "The winter is long, and the old teller's family has little meat to share with an "
                        "apprentice. The hunters look at {N} and wonder aloud what a teller's apprentice is for.")],
            'magic': [('',
                       "The guild school's bursary has run dry, and the bursar's letter says the fee for the second "
                       'year is due at the spring fair. {N} already copies scripts by candlelight for a few '
                       'coins.')]},
 'outcomes': (['The money holds out to the end of the year, just.',
               'Someone {N} did not expect helps, and the worst of the worry lifts.'],
              ['The debts grow faster than {N} can pay them, and the work suffers.',
               '{N} misses a week of lessons to cover what is owed, and {mentor} notices.']),
 'options': [
    ('take more shifts, and pay what is owed on time, whatever it costs in sleep', 'W1', None, 0.45, '', {'v': 'security, conformity', 'self_control': '+', 'world': {'tribal': 'hunt and haul with the band by day, and learn by the fire at night, owing nothing', 'magic': 'copy more scripts by candlelight, and pay the guild on time, whatever it costs in sleep'}, 'chance': 0.8}),
    ('apply to the hardship fund, with a careful and honest budget', 'U1', None, 0.45, '', {'v': 'security, achievement', 'grants': 'scholarship', 'world': {'tribal': "ask the old teller's family for a share of meat, and show them plainly what you bring in return", 'magic': "apply to the guild's hardship purse, with a careful and honest account"}, 'chance': 0.4}),
    ('take out a loan at a high rate, and worry about it later', 'B1', None, 0.45, '', {'v': 'achievement, security', 'binds': True, 'self_control': '-', 'world': {'tribal': "take meat on credit from a hunter, and owe him a winter's service", 'magic': 'borrow from a money-lender in the lower town, and worry about it later'}, 'chance': 0.9}),
    ('leave: the third year can wait, and life is happening now', 'R1', None, 0.45, '', {'self_control': '-', 'v': 'self-direction, hedonism', 'drops': 'drama school student', 'world': {'tribal': "leave the old teller's fire: the third winter can wait", 'magic': 'leave the guild school: the third year can wait, and life is happening now'}, 'chance': 0.95}),
    ('ask the family for help, knowing what it will cost them', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'ask your own kin to send meat, knowing what it will cost them'}, 'chance': 0.7}),
    ('ask the school, properly, for leave to take paid acting work in the holidays', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, conformity', 'world': {'tribal': "ask the old teller's leave to play at other bands' feasts for meat", 'magic': "ask the guild school's leave to play at feasts for coin in the holidays"}, 'chance': 0.6}),
    ('find a cheaper room in a shared house, and cook for everyone in it', 'U1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'world': {'tribal': 'move your sleeping skins to a crowded hearth, and cook for everyone at it', 'magic': 'find a cheaper garret, and share the cooking with the other scholars'}, 'chance': 0.75}),
    ("take a paid advert on the quiet, against the school's rules, to pay what is owed", 'B1', 'W.7', 0.5, '', {'v': 'achievement, security', 'mark': 'hid a wrong', 'closed': "approval: outside work against the school's rules; backfire: the school sees the advert and gives a formal warning", 'world': {'tribal': "play at another band's feast in secret, against the old teller's word, for meat", 'magic': "play at a merchant's feast on the quiet, against the guild's rules, for coin"}, 'chance': 0.75}),
    ('busk speeches at the station on Saturdays, and learn what holds a crowd', 'R1', 'U.7', 0.5, '', {'habit': True, 'self_control': '+', 'v': 'stimulation, achievement', 'mark': 'learned a skill', 'world': {'tribal': 'tell stories at the trading place for gifts, and learn what holds a crowd', 'magic': 'play speeches in the market square for coins, and learn what holds a crowd'}, 'chance': 0.6}),
    ('move back in with an aunt across town, and bank what the rent was', 'G1', 'B.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "move to your aunt's hearth, and keep what you would have given", 'magic': 'move back in with an aunt across the city, and bank what the rent was'}, 'chance': 0.75}),
 ]},
{'name': 'the lead does not believe in the idea',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss',
 'requires': 'director',
 'worlds': {'earth': 'a rehearsal room above a pub, three weeks in: the lead says in front of the company that the '
                     'idea does not work',
            'tribal': 'the wearer of the great mask will not play the ancestor as you shape him',
            'magic': 'the leading player refuses your staging before the whole company'},
 'timing': {'times': 'per director a year: about 1 production in 5 has an open quarrel over the idea of the play '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'Three weeks into rehearsal, in a room above a pub, {colleague}, who plays the lead, puts '
                       'down the script in the middle of a scene and says it in front of the whole company: the idea '
                       'does not work, and {colleague} does not believe in it.'),
                      ('W',
                       'A company needs one clear voice in the room, or it splinters into twelve. {N} also knows '
                       'that a director who cannot hear a fair objection does not deserve the room.'),
                      ('U',
                       '{N} replays the scene in {Ns} head. Somewhere between the second act and the third, the idea '
                       'and the play stopped agreeing, and {colleague} has put a finger on the place.'),
                      ('B',
                       'Eleven actors are watching to see who runs this room. Whatever {N} says in the next minute '
                       'is the story they will tell in the pub tonight.'),
                      ('R', '{Ns} face is hot. {N} has carried this idea for two years, and wants to shout back.'),
                      ('G',
                       'Plays grow their own way, like gardens, and sometimes the actors know before the director '
                       'does which way a play wants to go.')],
            'tribal': [('',
                        'At the fire where the telling is shaped, the wearer of the great mask says he will not play '
                        'the first ancestor as a weary old man: the ancestor was a hunter, and the band will laugh. '
                        'The other players fall silent.')],
            'magic': [('',
                       'Before the whole company, the leading player throws down the book: {Ns} staging of the '
                       "king's death is a mockery, and the leading player will not play it.")]},
 'outcomes': (["The room settles, and by the week's end the play is moving again.",
               'The lead comes in the next morning with a new idea, and it is a good one.'],
              ["The quarrel spreads, and by the week's end the company has split into two camps.",
               '{boss} hears about the scene, and starts coming to rehearsals to watch.']),
 'options': [
    ('hold the line calmly: one director, one idea, and the company follows it', 'W1', None, 0.45, '', {'v': 'conformity, security', 'identity': True, 'world': {'tribal': 'hold to your shaping calmly: one shaper, one telling, and the players follow it', 'magic': 'hold to your staging calmly: one master, one vision, and the company follows it'}, 'chance': 0.6}),
    ('go back to the text with the lead, line by line, and rethink', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'grants': 'directing actors', 'world': {'tribal': 'go back through the telling with the masked one, word by word, and rethink', 'magic': 'go back to the book with the leading player, line by line, and rethink'}, 'chance': 0.7}),
    ('recast the lead, and let the company see what defiance costs', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'made an enemy', 'closed': "approval: recasting without the producer's leave; backfire: the producer backs the actor, and the director is let go", 'world': {'tribal': 'give the great mask to another player, and let the band see what defiance costs', 'magic': 'give the part to another player, and let the company see what defiance costs'}, 'chance': 0.4}),
    ('say out loud that it stings, and ask the company what they really think', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'world': {'tribal': 'say before the fire that it stings, and ask the players what they really think'}, 'chance': 0.7}),
    ('let the lead try it their way for a day, and see what grows', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'world': {'tribal': 'let the masked one play it his way for a night, and see what grows'}, 'chance': 0.65}),
    ('stop for the day, and give the company the afternoon off to cool down', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'world': {'tribal': 'let the fire burn down for the night, and let everyone sleep on it', 'magic': 'end the rehearsal for the day, and give the company the afternoon off'}, 'chance': 0.75}),
    ('talk to the lead alone, and agree a way of working the whole room can see', 'U1', 'W.7', 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': 'walk with the masked one alone, and agree a way the whole band can see'}, 'chance': 0.6}),
    ('find out from the stage manager what the lead has been saying in the pub', 'B1', 'U.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'find out from the keeper of the fire what the masked one has been saying at other hearths', 'magic': 'find out from the book-keeper what the leading player says in the tavern'}, 'chance': 0.8}),
    ('throw the whole idea out overnight, and come in with a bolder one', 'R1', 'B.7', 0.5, '', {'v': 'power, self-direction', 'mark': 'took a wild risk', 'world': {'tribal': 'throw out your whole shaping overnight, and come to the fire with a bolder one', 'magic': 'throw out the staging overnight, and come in with a bolder one'}, 'chance': 0.55}),
    ('take the company out of the room, and play the scene in the park', 'G1', 'R.7', 0.5, '', {'v': 'stimulation, benevolence', 'door': True, 'world': {'tribal': 'take the players away from the fire, and play the scene in the open by the river', 'magic': 'take the company out of the playhouse, and play the scene in the town gardens'}, 'chance': 0.6}),
 ]},
{'name': 'the budget is cut by a third',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'director',
 'worlds': {'earth': 'an email from the producer: a backer has pulled out, and the budget is cut by a third two '
                     'weeks before the get-in',
            'tribal': 'the families give fewer hides for the telling this year',
            'magic': 'the patron halves his purse for the season'},
 'timing': {'times': 'per director a year: about 1 in 5 see a budget cut after rehearsals begin (estimate)'},
 'scenes': {'earth': [('',
                       'The email from {boss}, the producer, comes at seven in the morning: a backer has pulled out, '
                       'and the budget is cut by a third. The set is half built, the get-in is in two weeks, and the '
                       'cast of eleven has been hired for all of it.'),
                      ('W',
                       'There is a contract with the actors and a contract with the set builders, and {N} means to '
                       'keep both if there is any way at all.'),
                      ('U',
                       '{N} opens the budget and goes through it line by line: the revolve, the band, the '
                       'projections, the eleventh actor. Somewhere in it is a cheaper show that is still the same '
                       'show.'),
                      ('B',
                       'Producers cut budgets when directors let them. {N} reads the email twice and starts working '
                       'out what {boss} actually needs to hear.'),
                      ('R',
                       'The revolve was the whole idea. {N} feels the show being sawn in half and wants to put a '
                       'fist through the screen.'),
                      ('G',
                       'Theatre has always been made out of not much: planks, a few lamps, people telling a story. '
                       'The show will be what it can be.')],
            'tribal': [('',
                        'The families have given fewer hides for the screens this year, and less fat for the fires. '
                        'The telling {N} has shaped needs twice what the band will give.')],
            'magic': [('',
                       "The patron has halved his purse for the season, and the playhouse's master sends word: the "
                       'masque {N} has staged must cost half of what it does.')]},
 'outcomes': (['The show that opens is smaller and, to {Ns} surprise, better.',
               '{boss} sees what {N} saved, and the next budget comes without a fight.'],
              ['The cuts take the heart out of the show, and the audience can feel it.',
               'Half the company hears what was cut before {N} can tell them, and the room turns sour.']),
 'options': [
    ('keep every contract, and cut the set and the effects instead', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'kept your word', 'world': {'tribal': 'keep every promise to the players, and cut the screens and the fires instead', 'magic': 'keep every contract, and cut the scenery and the glamours instead'}, 'chance': 0.75}),
    ('rework the staging so the show needs a third less, and keeps its heart', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'reshape the telling so it needs a third fewer hides, and keeps its heart'}, 'chance': 0.65}),
    ("cut the actors' fees by a third, as the small print allows", 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'made an enemy', 'world': {'tribal': "cut the players' share of the feast by a third, as is your right", 'magic': "cut the players' wages by a third, as their contracts allow"}, 'chance': 0.85}),
    ('cut a character today, and tell the actor yourself, face to face', 'R1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'cut a spirit from the telling today, and tell its player yourself', 'magic': 'cut a character today, and tell the player yourself, face to face'}, 'chance': 0.9}),
    ('strip the show back to planks and lamps, and trust the story', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'world': {'tribal': 'strip the telling back to one fire and the voices, and trust the story', 'magic': 'strip the masque back to boards and candles, and trust the story'}, 'chance': 0.7}),
    ('put your own fee into the show, so nobody else loses theirs', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'binds': True, 'world': {'tribal': 'give your own furs and meat to the telling, so no player goes without', 'magic': 'put your own fee into the masque, so nobody else loses theirs'}, 'chance': 0.5}),
    ('find a cheaper supplier for every line of the budget, and keep every contract', 'U1', 'W.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'find cheaper hides and fat from every hearth, and keep every promise', 'magic': 'find cheaper timber and cloth for every line of the account, and keep every contract'}, 'chance': 0.65}),
    ('trade the producer a cheaper set for two more weeks of rehearsal', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'trade the families fewer screens for more nights of practice', 'magic': 'trade the patron cheaper scenery for two more weeks of rehearsal'}, 'chance': 0.55}),
    ('fight the producer for every penny, in front of the backers', 'R1', 'B.7', 0.5, '', {'v': 'power, self-direction', 'mark': 'defied an authority', 'world': {'tribal': 'fight the families for every hide, in front of the whole band', 'magic': "fight the patron's steward for every coin, in front of the court"}, 'chance': 0.45}),
    ("borrow the local players' old set through a friend on their committee, without asking the rest", 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'hid a wrong', 'closed': "approval: a set lent without the committee's leave; backfire: the committee knows its set on the first night, and the friend loses their seat", 'world': {'tribal': 'borrow the masks and skins of past tellings through a friend who keeps them, without asking the elders', 'magic': "borrow the mystery players' old wagon through a friend in their guild, without asking its masters"}, 'chance': 0.65}),
 ]},
{'name': 'the producers want a different ending',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, family',
 'requires': 'playwright or screenwriter',
 'worlds': {'earth': 'notes on the script from the producers: they love it, they want to make it, and they want the '
                     'ending changed',
            'tribal': "the elders want the telling to end with the chief's victory",
            'magic': 'the patron wants the hero to live'},
 'timing': {'times': 'per playwright or screenwriter a year: about 1 script in 3 that is bought is asked for a '
                     'changed ending (estimate); about 8 lives in 10,000 are paid for a produced script (catalogue '
                     'share; estimate)'},
 'scenes': {'earth': [('',
                       'The notes come back from {boss}, the producer, in a long and friendly email. They love the '
                       'script. They want to make it. They want the ending changed: the mother should forgive her '
                       'son in the last scene, not close the door on him.'),
                      ('W',
                       '{N} signed an agreement that gives the producers notes, and promised to take them seriously. '
                       '{N} did not promise to write something false.'),
                      ('U',
                       'The closed door is the whole play: every scene before it bends toward that moment. {N} '
                       'wonders whether there is a third ending nobody has thought of, one that keeps the meaning '
                       'and answers what the producers fear.'),
                      ('B',
                       'The producers have the money, a theatre and a director. {N} has a script and a rent day. The '
                       'question is what the ending is worth, and to whom.'),
                      ('R',
                       '{N} wrote that last scene in one night, in tears, and it is the truest thing {N} has ever '
                       'written. Changing it would be like tearing a page out of a diary.'),
                      ('G',
                       "{N} wrote the play out of {Ns} own family's history, and in the family the door stayed "
                       'closed. Some stories end the way they end.')],
            'tribal': [('',
                        'The elders have heard {Ns} new telling of the war with the river clans, and they like it. '
                        "They want it to end with the chief's victory at the ford, not with the mourning songs {N} "
                        'made for the dead.')],
            'magic': [('',
                       'The patron has read {Ns} new play and will pay for it to be staged at court, if the young '
                       'hero lives at the end instead of dying on the bridge.')]},
 'outcomes': (['The play goes ahead with an ending {N} can put {Ns} name to.',
               'The argument makes the play better, and everyone in the room can tell.'],
              ['The deal falls through, and the play goes back to waiting.',
               'The ending is changed behind {Ns} back, and {N} first hears it with everyone else.']),
 'options': [
    ('take the notes in good faith, and rewrite the ending as asked', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': "take the elders' wish in good faith, and remake the ending as asked", 'magic': "take the patron's wish in good faith, and rewrite the ending as asked"}, 'chance': 0.75}),
    ('find a third ending that keeps the meaning and answers their worry', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.55}),
    ("change it, and ask for more money and a producer's credit in return", 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'change it, and ask the elders for the best hides and a place at their fire in return', 'magic': 'change it, and ask the patron for a richer purse and your name first on the bill'}, 'chance': 0.6}),
    ('keep it, and play the lead yourself at the fringe if nobody will stage it', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'aims': 'lead actor or actress', 'world': {'tribal': 'keep it, and tell it yourself at the outer fires if the elders will not have it', 'magic': 'keep it, and play the lead yourself in a fair booth if nobody will stage it'}, 'chance': 0.5}),
    ('keep it, and let the play wait for the right producer', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'mark': 'turned down a chance', 'world': {'tribal': 'keep it, and let the telling wait for elders who will hear it', 'magic': 'keep it, and let the play wait for the right patron'}, 'chance': 0.65}),
    ('ask for a reading with actors, so both endings can be heard fairly', 'W1', 'U.7', 0.5, '', {'v': 'universalism', 'world': {'tribal': 'ask to tell both endings at the fire, so both can be heard fairly', 'magic': 'ask for a reading with the company, so both endings can be heard fairly'}, 'chance': 0.55}),
    ('offer the producers the ending the script editor sketched last year, as your own', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': "approval: another writer's idea passed off as one's own; backfire: the script editor is at the read-through", 'world': {'tribal': 'offer the elders the ending the old teller once sketched, as your own', 'magic': "offer the patron the ending the guild's old play-maker once sketched, as your own"}, 'chance': 0.6}),
    ('take the script elsewhere, to a producer who will stage it as written', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, power', 'world': {'tribal': "take the telling to another band's elders, who will hear it as it is", 'magic': 'take the play to another playhouse, that will stage it as written'}, 'chance': 0.55}),
    ('go home for a night, and ask the family how the story really ends', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': "go to your mother's hearth for a night, and ask how the story really ends"}, 'chance': 0.8}),
    ('share a long dinner with the producers, and find an ending all can live with', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'sit with the elders through a long night, and find an ending all can live with', 'magic': 'dine with the patron, and find an ending all can live with'}, 'chance': 0.65}),
 ]},
{'name': 'the blank page at three in the morning',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, home',
 'horizon': 'week',
 'roles': 'boss, friend',
 'requires': 'playwright or screenwriter',
 'worlds': {'earth': 'a laptop at the kitchen table at three in the morning: the second act is due on Friday, and '
                     'nothing is on the page',
            'tribal': 'the gathering is a moon away and the new telling is not made',
            'magic': 'the play is promised to the playhouse by the new moon'},
 'timing': {'times': 'per playwright or screenwriter: most months with a deadline (estimate)'},
 'scenes': {'earth': [('',
                       'Three in the morning at the kitchen table. The second act is due to {boss} on Friday, the '
                       'cursor has blinked on an empty page since nine, and the tea went cold at midnight.'),
                      ('W',
                       '{N} promised Friday, and a promise to a theatre is a promise to a whole company waiting on '
                       'the pages. {N} has never once missed a deadline.'),
                      ('U',
                       '{N} knows what the second act has to do, in principle. The trouble is one scene that will '
                       'not come, and {N} keeps circling it like a sum that will not balance.'),
                      ('B',
                       'Writers who miss deadlines stop being asked. {N} thinks of the half-finished things in the '
                       'drawer, and of the story {friend} told over dinner last month, the one that would make a '
                       'perfect second act.'),
                      ('R',
                       'The page is blank and the flat is silent, and {N} wants to scream, or run out into the '
                       'street, or write anything at all just to break it.'),
                      ('G',
                       'Some nights the words come like water, and some nights the well is dry. {N} has learned that '
                       'the dry nights pass.')],
            'tribal': [('',
                        'The summer gathering is a moon away, and the new telling {N} promised the elders has a '
                        'beginning and nothing after it. The fire has burned down to embers.')],
            'magic': [('',
                       'The play is promised to the playhouse by the new moon, and three acts of the five are blank '
                       'pages. The candle has burned down to a stub.')]},
 'outcomes': (['By the day it is due the work is done, and some of it is good.',
               'The scene that would not come turns out to be the best one in the play.'],
              ['The day comes with nothing finished, and {boss} has to be told.',
               'The pages go in, and {boss} says plainly what {N} already knew.']),
 'options': [
    ('sit at the table until five pages exist, good or bad', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'self_control': '+', 'world': {'tribal': 'sit at the fire until the telling has a middle, good or bad', 'magic': 'sit at the desk until five pages exist, good or bad'}, 'chance': 0.7}),
    ('go back to the outline, and find out why the scene will not come', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'go back over the telling from the start, and find out why the middle will not come'}, 'chance': 0.7}),
    ('use the story a friend told over dinner, without asking', 'B1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': "approval: a friend's story used without leave; backfire: the friend sees the play", 'world': {'tribal': 'use the story a friend told at the fire, without asking', 'magic': 'use the tale a friend told at supper, without asking'}, 'chance': 0.9}),
    ('walk the empty streets until the scene comes, or the sun does', 'R1', None, 0.45, '', {'self_control': '+', 'v': 'stimulation, self-direction', 'body': 'light', 'world': {'tribal': 'walk the dark valley until the telling comes, or the sun does', 'magic': 'walk the empty lanes until the scene comes, or the sun does'}, 'chance': 0.65}),
    ('go to bed, and trust the scene to come in the morning', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'chance': 0.6}),
    ('ring the producer at nine, and ask honestly for one more week', 'W1', 'U.7', 0.5, '', {'self_control': '-', 'v': 'conformity, achievement', 'mark': 'owned up', 'world': {'tribal': 'go to the elders at dawn, and ask honestly for one more moon', 'magic': "go to the playhouse's master at the morning bell, and ask honestly for one more week"}, 'chance': 0.6}),
    ('send the strongest scenes first, and buy time for the rest', 'U1', 'B.7', 0.5, '', {'self_control': '-', 'v': 'power, achievement', 'world': {'tribal': 'tell the elders the strongest part first, and buy time for the rest'}, 'chance': 0.75}),
    ('pour a large drink, and write whatever it lets out', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, stimulation', 'habit': True, 'self_control': '-', 'world': {'tribal': 'drink the berry wine, and make whatever it lets out', 'magic': 'open the wine, and write whatever it lets out'}, 'chance': 0.55}),
    ('write the scene as it happened in your own family, raw and unpolished', 'R1', 'G.7', 0.5, '', {'v': 'self-direction, tradition', 'grants': 'writing scripts', 'world': {'tribal': 'make the scene as it happened at your own hearth, raw and unpolished'}, 'chance': 0.65}),
    ('ring an old friend, and talk the scene through until it is clear', 'G1', 'W.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'wake an old friend, and talk the telling through until it is clear', 'magic': "knock on an old friend's door, and talk the scene through until it is clear"}, 'chance': 0.7}),
 ]},
{'name': 'a newcomer gets your part',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.02,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, play',
 'horizon': 'months',
 'roles': 'boss, rival, friend',
 'requires': 'amateur actor',
 'worlds': {'earth': 'the cast list on the society noticeboard: the newcomer has the part everyone thought was yours',
            'tribal': 'the elders give your part in the telling to a girl from another hearth',
            'magic': 'the pageant master gives your part to a newcomer'},
 'timing': {'times': 'per amateur actor: about once in three years a wanted part goes to someone else; about 4 lives '
                     'in 100 act with amateurs (catalogue share; estimate)',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       'The cast list goes up on the society noticeboard on Tuesday night. {N} has waited eleven '
                       'years for this part, and everyone said so, but beside its name is {rival}, who joined in the '
                       'spring.'),
                      ('W',
                       "The society's rules say the director casts and the members accept it, and {N} voted for that "
                       'rule. {N} reads the list twice anyway.'),
                      ('U',
                       '{N} replays the audition: the speech went well, the reading less so. {rival} read the scene '
                       'with the daughter better, and {N} can admit it, just about.'),
                      ('B',
                       'Eleven years of selling raffle tickets, painting flats and turning up, and the part goes to '
                       'someone with a nice voice and no history. {N} starts thinking about who on the committee '
                       'owes {N} a favour.'),
                      ('R',
                       '{Ns} face goes hot in the corridor of the church hall. {N} wants to tear the list off the '
                       'board, or walk out and never come back.'),
                      ('G',
                       'The society has lost and found its leads for sixty years, and parts come round again like '
                       'the seasons. It still stings.')],
            'tribal': [('',
                        'The elders have chosen a young woman from another hearth, newly married into the band, to '
                        'play the old wolf at midwinter. It is the part {N} has played for three winters.')],
            'magic': [('',
                       "The pageant master pins the parts to the guild hall door: the herald's part, {Ns} for five "
                       'feast days, goes to a newcomer from the lower town.')]},
 'outcomes': (['The season goes on, and {N} finds a place in it that feels right.',
               '{rival} plays the part well, and comes to {N} after the last night to say thanks.'],
              ['The sting does not fade, and the rehearsals are a misery from first to last.',
               'The company splits over it, and some old friends stop speaking to {N}.']),
 'options': [
    ('congratulate the newcomer at the first rehearsal, and mean it', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'mark': 'made a friend', 'world': {'tribal': 'greet the newcomer at the first gathering of the players, and mean it'}, 'chance': 0.7}),
    ('take the small part, and use it to work on what the audition lacked', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'world': {'tribal': "take the small spirit's part, and work on what your showing lacked"}, 'chance': 0.75}),
    ('lobby the committee to look at the casting again', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'go round the elders one by one, and ask them to choose again', 'magic': "lobby the guild's elders to look at the casting again"}, 'chance': 0.4}),
    ('walk out of the society, and do not look back', 'R1', None, 0.45, '', {'v': 'self-direction', 'drops': 'amateur actor', 'world': {'tribal': "walk away from the band's tellings, and do not look back", 'magic': 'walk out of the mystery players, and do not look back'}, 'chance': 0.95}),
    ('stay on, take what comes, and wait for the part to come round again', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'self_control': '+', 'chance': 0.7}),
    ('ask the director plainly what it would take to win the next lead', 'W1', 'B.7', 0.5, '', {'v': 'achievement', 'world': {'tribal': 'ask the elders plainly what it would take to win the part next winter', 'magic': 'ask the pageant master plainly what it would take to win the next lead'}, 'chance': 0.7}),
    ('learn the part anyway, and play it alone in the empty hall one night', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'learn the part anyway, and tell it alone to the river one night', 'magic': 'learn the part anyway, and play it alone in the empty guild hall one night'}, 'chance': 0.9}),
    ('put your name down to direct next season instead', 'B1', 'G.7', 0.5, '', {'v': 'power, achievement', 'aims': 'community theatre director', 'world': {'tribal': "offer to shape next midwinter's telling instead", 'magic': "offer yourself as master of next year's pageant instead"}, 'chance': 0.7}),
    ('sulk through the read-through, so everyone sees what was done', 'R1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'self_control': '-', 'world': {'tribal': 'sit apart from the players with your back to them, so everyone sees what was done', 'magic': 'sulk through the first rehearsal, so everyone sees what was done'}, 'chance': 0.2}),
    ('help the newcomer learn it, and pass on what the part taught you', 'G1', 'U.7', 0.5, '', {'v': 'benevolence', 'grants': 'a company that feels like family', 'chance': 0.6}),
 ]},
{'name': 'show week in the village hall',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.02,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community, play',
 'horizon': 'week',
 'roles': 'boss, friend, colleague',
 'requires': 'amateur actor',
 'worlds': {'earth': 'the village hall in show week: the get-in, a dress rehearsal that runs till midnight, and a '
                     'flat that falls',
            'tribal': 'the night of the midwinter telling, the fire too high and the screens catching',
            'magic': "the pageant wagon's axle breaks on the feast morning"},
 'timing': {'times': 'per amateur actor: once or twice a year, in each show week (estimate)',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       'Show week in the village hall. The get-in took all Sunday, the dress rehearsal is running '
                       'past midnight, and in the middle of the second act a flat of the drawing-room wall leans, '
                       'sways and starts to fall toward the stage.'),
                      ('W',
                       'There is a running order, a call sheet and a prompt book, and somebody has to keep to them '
                       'or the first night will be chaos. {N} has been that somebody before.'),
                      ('U',
                       "{N} saw that flat's brace go in on Sunday and knew it was wrong: one bolt where there should "
                       'be two. The fix takes four minutes, if someone knows it.'),
                      ('B',
                       '{boss}, who chairs the society, is panicking in the third row. Whoever takes charge tonight '
                       'will be running this society by next year.'),
                      ('R',
                       'The flat is falling, someone has shrieked, and the whole thing is suddenly the funniest '
                       'thing that has happened all year.'),
                      ('G',
                       'The hall smells of size paint and old radiators, the way it has in every show week for '
                       'thirty years. {N} would not be anywhere else.')],
            'tribal': [('',
                        'It is the night of the midwinter telling, the fire has been built too high, and the edge of '
                        'a hide screen has begun to smoulder while the hunters are still dancing.')],
            'magic': [('',
                       "On the feast morning the pageant wagon's axle cracks in the market square, an hour before "
                       'the procession, with the stage still painted and the costumes on board.')]},
 'outcomes': (['The first night goes off with only the usual mishaps, and the audience laughs in the right places.',
               'Years later, people in the company still tell the story of that night.'],
              ['The fix does not hold, and on the first night it all goes wrong again.',
               'Tempers fray, and two old friends in the cast are not speaking by the end of the week.']),
 'options': [
    ('stay on after midnight, and help re-hang the flat before going home', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'body': 'light', 'world': {'tribal': 'stay on after the telling, and help mend the screen before sleeping', 'magic': 'stay on after the procession, and help mend the wagon before going home'}, 'chance': 0.8}),
    ('find the faulty brace, and show the set builders how to fix it properly', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'find why the screen caught, and show the others how to set it back from the fire', 'magic': 'find the flaw in the axle, and show the carpenters how to mend it properly'}, 'chance': 0.75}),
    ('take charge: clear the stage, hand out the jobs, and run it from the top', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'grants': 'stagecraft', 'world': {'tribal': 'take charge: move the screens, hand out the jobs, and start the telling again', 'magic': 'take charge: unload the wagon, hand out the jobs, and set the stage in the square'}, 'chance': 0.8}),
    ('laugh, and get the whole cast laughing too', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'chance': 0.9}),
    ('go home to bed: the show will be ready when it is ready', 'G1', None, 0.45, '', {'self_control': '-', 'v': 'tradition (acceptance)', 'world': {'tribal': 'go to your sleeping skins: the telling will be ready when it is ready', 'magic': 'go home: the pageant will be ready when it is ready'}, 'chance': 0.6}),
    ('insist the dress rehearsal runs to the end, though the hall is booked only till eleven', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'aims': 'community theatre director', 'mark': 'defied an authority', 'closed': 'approval: the hall kept past its booking; backfire: the hall committee bills the society for the late hours', 'world': {'tribal': 'insist the telling runs to the end, though the elders said the fire must be banked by moonset', 'magic': 'insist the pageant runs its full course, though the town gave the street only till noon'}, 'chance': 0.6}),
    ('change the scene on the spot, so the falling wall becomes part of the play', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'change the telling on the spot, so the smoking screen becomes part of the story', 'magic': 'change the pageant on the spot, so the broken wagon becomes part of the show'}, 'chance': 0.4}),
    ("call in favours from the cast's families: ladders, tools and a van within the hour", 'B1', 'G.7', 0.5, '', {'v': 'power, benevolence', 'world': {'tribal': 'call in what the families owe: poles, hides and strong arms before moonrise', 'magic': "call in favours from the players' families: a new axle and a cart by the next bell"}, 'chance': 0.9}),
    ('dash on stage and catch the flat before it lands on anyone', 'R1', 'W.7', 0.5, '', {'v': 'benevolence', 'body': 'light', 'world': {'tribal': 'dash in and drag the smouldering screen away from the dancers', 'magic': "dash in and prop the wagon's stage before it tips onto anyone"}, 'chance': 0.75}),
    ('ask the old member who built the sets for forty years how it was done', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'mark': 'learned a skill', 'world': {'tribal': 'ask the oldest player how the screens were set in his youth', 'magic': "ask the guild's old wheelwright how it was done in his day"}, 'chance': 0.9}),
 ]},
{'name': 'the new child gets the lead',
 'stages': 'child juvenile',
 'age': (6, 21),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.1,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'play, friends',
 'horizon': 'week',
 'roles': 'friend, parent',
 'requires': 'youth theatre member',
 'worlds': {'earth': 'the cast list pinned up on a Saturday morning: the lead in the summer show has gone to the new '
                     'child',
            'tribal': "the old teller gives the hare's part to a child from another hearth",
            'magic': "the guild's children's master gives the fairy queen to a newcomer"},
 'timing': {'times': "per youth theatre member: about once a year, at the summer show's casting (estimate)",
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'On Saturday morning the cast list for the summer show is pinned up by the hall door. The '
                       'lead has gone to a child who joined in the spring, and {friend} and the other old hands '
                       'crowd round {N}, angrier than {N} is.'),
                      ('W',
                       'The leaders said at the start that every part would be chosen fairly from the auditions, and '
                       "the new child's audition was good. {N} heard it."),
                      ('U',
                       '{N} thinks back over the auditions, trying to work out what the new child did that {N} did '
                       'not. It was something about the stillness.'),
                      ('B',
                       '{N} has come every Saturday for three years and helped with the little ones, and it counted '
                       'for nothing. Next year {N} means to make sure it counts.'),
                      ('R',
                       '{Ns} throat is tight, and {friend} is already saying it is not fair, loudly, right by the '
                       'door where the new child can hear.'),
                      ('G',
                       'The new child is standing alone by the coat pegs, holding the script and looking at the '
                       'floor.')],
            'tribal': [('',
                        "The old teller has given the hare's part in the midsummer telling to a child from another "
                        'hearth, who came to the band in the spring. The children who have played at the fire for '
                        'three summers look at {N}.')],
            'magic': [('',
                       "The guild's children's master has given the fairy queen to a newcomer from the river "
                       "quarter. {Ns} friends in the children's company are whispering by the costume trunks.")]},
 'outcomes': (['By the time of the show the children are one company again, and {N} is part of it.',
               'The new child turns out to be a friend, and the two of them are inseparable by the last night.'],
              ['The bad feeling lasts for weeks, and the sessions are not much fun any more.',
               '{friend} and {N} fall out over it, and do not sit together for weeks.']),
 'options': [
    ('tell the others the casting was fair, and ask them to stop grumbling', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'tell the other children the old teller chose fairly, and ask them to stop', 'magic': "tell the others the children's master chose fairly, and ask them to stop"}, 'chance': 0.55}),
    ('ask the leaders at pick-up time what to work on for next time', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'ask the old teller, at the fire with the others, what to practise for next summer', 'magic': "ask the children's master, with a parent there, what to practise for next time"}, 'chance': 0.8}),
    ('offer to understudy the lead, in case the new child falls ill', 'B1', None, 0.45, '', {'self_control': '+', 'v': 'achievement, power', 'world': {'tribal': "offer to learn the hare's part too, in case the new child falls sick", 'magic': 'offer to learn the fairy queen too, in case the newcomer falls ill'}, 'chance': 0.75}),
    ('tell the leaders loudly, in front of everyone, that it is not fair', 'R1', None, 0.45, '', {'v': 'self-direction, universalism', 'mark': 'defied an authority', 'world': {'tribal': 'tell the old teller loudly, before all the children, that it is not fair', 'magic': "tell the children's master loudly, before the whole company, that it is not fair"}, 'chance': 0.45}),
    ('go and stand with the new child by the coat pegs', 'G1', None, 0.45, '', {'v': 'benevolence', 'mark': 'made a friend', 'world': {'tribal': 'go and sit with the new child at the edge of the fire', 'magic': 'go and stand with the newcomer by the costume trunks'}, 'chance': 0.75}),
    ('say well done to the new child, out loud, so the others hear it', 'W1', 'R.7', 0.5, '', {'v': 'benevolence', 'identity': True, 'world': {'tribal': 'tell the new child well done, out loud, so the others hear'}, 'chance': 0.7}),
    ('help the new child learn the lines at break time', 'U1', 'G.7', 0.5, '', {'v': 'benevolence', 'grants': 'a company that feels like family', 'world': {'tribal': "help the new child learn the hare's words while the others play", 'magic': 'help the newcomer learn the lines between rehearsals'}, 'chance': 0.5}),
    ('tell the others the new child only got it because a parent helps out', 'B1', 'W.7', 0.5, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: an untrue story about another child; backfire: the leaders hear it, and talk to the parents', 'world': {'tribal': "tell the other children the new child's family bought the part with meat for the old teller", 'magic': 'tell the others the newcomer got it because a parent pays the guild'}, 'chance': 0.65}),
    ('go home and act the whole lead part in the garden, just to know you could', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': "go down to the river and play the whole hare's part, just to know you could", 'magic': 'go home and play the whole fairy queen in the yard, just to know you could'}, 'chance': 0.9}),
    ('work at it all year, and set your heart on drama school one day', 'G1', 'B.7', 0.5, '', {'self_control': '+', 'v': 'achievement', 'binds': True, 'aims': 'drama school student', 'world': {'tribal': "work at it all year, and set your heart on learning at an old teller's side one day", 'magic': 'work at it all year, and set your heart on the guild school one day'}, 'chance': 0.6}),
 ]},
{'name': 'first night nerves in the wings',
 'stages': 'child juvenile',
 'age': (6, 21),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.1,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'play, family',
 'horizon': 'moment',
 'roles': 'parent, friend',
 'requires': 'youth theatre member',
 'worlds': {'earth': 'the wings of the school hall on the first night, with a parent in the third row and the cue '
                     'two minutes away',
            'tribal': 'the first telling by the fire with the whole band watching',
            'magic': "the children's company's first night in the guild hall"},
 'timing': {'times': 'per youth theatre member: once or twice a year, at each show (estimate)',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       "The first night of the youth theatre's show, in the school hall. {N} stands in the wings in "
                       'costume with the rest of the group, mouth dry, while the hall fills; {parent} is in the '
                       'third row, and the cue is two minutes away.'),
                      ('W',
                       '{N} learned every line and every move, and the others are counting on {N} to be there for '
                       'the first scene. That is what a company is.'),
                      ('U',
                       '{N} runs the first line in {Ns} head, then the second, then cannot remember the third, then '
                       'can. The mind does strange things before a show.'),
                      ('B',
                       '{parent} has brought half the family, and the drama teacher from the big school is meant to '
                       'be in tonight. This is a chance to be noticed.'),
                      ('R',
                       '{Ns} heart is going like a drum, and {N} cannot tell whether this is terror or the best '
                       'feeling in the world.'),
                      ('G',
                       'Through the gap in the curtain {N} can see {parent} in the third row, waving at the wrong '
                       'side of the stage. Everyone {N} loves is out there.')],
            'tribal': [('',
                        'It is {Ns} first telling by the fire, as the hare, with the whole band watching and '
                        '{parent} among the families at the edge of the light. The old teller nods to the children '
                        'behind the screen: soon.')],
            'magic': [('',
                       "In the guild hall the children's company waits behind the painted cloth for its first night. "
                       '{N} can hear {parent} somewhere in the benches, and the chaperone is counting the children '
                       'for the third time.')]},
 'outcomes': (['{N} gets through the first night, and comes off glowing.',
               '{parent} is waiting at the end with a hug and a long list of favourite moments.'],
              ['{N} dries on the second line, and a friend whispers the rest.',
               'The nerves win for a while, and the first scene goes by in a blur.']),
 'options': [
    ('go through the first scene once more in your head, then walk on', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'go through the first words once more in your head, then step into the light'}, 'chance': 0.85}),
    ('do the breathing the leaders taught: in for four, and out for six', 'U1', None, 0.45, '', {'v': 'achievement, security', 'mark': 'learned a skill', 'world': {'tribal': 'breathe slowly, as the old teller taught, like the river at night', 'magic': "do the breathing the children's master taught: in for four, and out for six"}, 'chance': 0.8}),
    ('decide to be the best thing in the show, so everyone remembers it', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'chance': 0.7}),
    ('grin at the audience through the gap, and bounce on when it is time', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'peep round the hide screen at the band, and leap out when it is time', 'magic': 'peep through the painted cloth, and bounce on when it is time'}, 'chance': 0.85}),
    ("hold a friend's hand in the wings until the cue", 'G1', None, 0.45, '', {'v': 'benevolence, security', 'world': {'tribal': "hold a friend's hand behind the screen until the drums"}, 'chance': 0.8}),
    ('ask a leader to wait in the wings with the whole group', 'W1', 'R.7', 0.5, '', {'v': 'security', 'world': {'tribal': 'ask the old teller to stand by the screen where all the children can see him', 'magic': 'ask the chaperone to wait in the wings with the whole group'}, 'chance': 0.75}),
    ('whisper the first lines with the others, so everyone remembers them', 'U1', 'G.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'whisper the first words with the other children, so everyone remembers them'}, 'chance': 0.75}),
    ('tell the little ones exactly where to stand, so the scene runs like clockwork', 'B1', 'W.7', 0.5, '', {'v': 'power, conformity', 'chance': 0.75}),
    ('go on and play it bigger than in rehearsal, just to see what happens', 'R1', 'U.7', 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'grants': 'acting', 'world': {'tribal': 'play the hare bigger than ever before, just to see what happens'}, 'chance': 0.65}),
    ('find the family through the curtain, and play every line to them', 'G1', 'B.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': 'find the family at the edge of the light, and play every word to them', 'magic': 'find the family in the benches, and play every line to them'}, 'chance': 0.7}),
 ]},
{'name': 'the first morning of the first term',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'learning, friends',
 'horizon': 'week',
 'roles': 'mentor, colleague, parent',
 'requires': 'drama school student',
 'threshold': 'title:drama school student',
 'step': 1,
 'worlds': {'earth': 'the first morning at drama school: a converted warehouse, a timetable from nine to nine, and '
                     'thirty strangers in black',
            'tribal': "the first morning at an old teller's fire in another band, far from your own hearth, with the "
                      'other apprentices watching',
            'magic': "the first morning in the guild school's hall: its masters, its rules, and a bench among "
                     "strangers in the guild's grey"},
 'timing': {'times': 'per new drama school student: once, in the first weeks after taking the title; about 3 lives '
                     'in 1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of drama school student, within the first six months after taking '
                         "the title (opened by 'drama school auditions' or any other way in): step 1, the first "
                         'weeks of the course',
             'likelier': 'a first place won at the auditions; a student who moved to a new city for the course; a '
                         'full-time course of three years',
             'rarer': 'a part-time or foundation course; a student who has already trained somewhere else'},
 'scenes': {'earth': [('',
                       'The first morning of drama school starts in a circle on the floor of a converted warehouse: '
                       'thirty strangers in black, each saying a name and one thing nobody knows about them. The '
                       'timetable runs from nine in the morning to nine at night, and {mentor}, the head of acting, '
                       'says the first year is for taking everything apart.'),
                      ('W',
                       '{N} has bought every book on the reading list, labelled the rehearsal clothes and arrived '
                       'twenty minutes early.'),
                      ('U',
                       '{N} wants to know what each class is for: the voice, the movement, the text, and how they '
                       'fit together into an actor.'),
                      ('B',
                       "{N} sizes up the year group: who already has an agent's eye on them, who came from the "
                       'famous youth company, who is the one to beat.'),
                      ('R',
                       '{N} is giddy. Three years of nothing but acting, and the circle on the floor feels like the '
                       'start of everything.'),
                      ('G',
                       '{N} thinks of the kitchen at home, of {parent} driving {N} to the auditions, and of a town '
                       'that already seems very far away.')],
            'tribal': [('',
                        "At dawn {N} sits for the first time at an old teller's fire in another band, far from home, "
                        'and the other apprentices watch to see what the newcomer can do.')],
            'magic': [('',
                       "In the guild school's great hall the masters stand in their robes, a clerk reads out the "
                       "rules, and {N} takes a bench among strangers in the guild's grey.")]},
 'outcomes': (['By the end of the first week {N} knows the building, the timetable and most of the names, and the '
               'warehouse begins to feel like a place to work.',
               '{mentor} stops {N} in the corridor on Friday to say it was a good first week.'],
              ['The first week is a blur of names and warm-ups, and {N} goes home each night too tired to remember '
               'any of it.',
               'Something {N} said in the first circle is the joke of the year group by Friday, and not a kind '
               'one.']),
 'options': [
    ("learn everyone's name by lunchtime, and keep every rule of the studio", 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': "learn every apprentice's name by midday, and keep every custom of the old teller's fire", 'magic': "learn every scholar's name by the noon bell, and keep every rule of the hall"}, 'chance': 0.8}),
    ('ask the head of acting what each class of the first year is for', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'ask the old teller what each part of the first winter is meant to teach', 'magic': 'ask the master of the school what each class of the first year is for'}, 'chance': 0.88}),
    ('find out which teachers the agents listen to, and get noticed by them', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'find out whose word the elders of other bands trust, and get noticed by the old teller', 'magic': "find out which masters the players' brokers listen to, and get noticed by them"}, 'chance': 0.8}),
    ('throw yourself into the first improvisation game, and make the whole room laugh', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'leap into the first game at the fire, and make the whole circle laugh'}, 'chance': 0.8}),
    ('ring home at the end of the day, and tell them every detail', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'send word home with a trader going upriver that the first day went well', 'magic': 'send a letter home by the evening coach, with every detail of the day'}, 'chance': 0.92}),
    ('come in early every morning to warm up properly, as the movement teacher asked', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'rise before the others every morning to warm the voice, as the old teller asked', 'magic': 'come to the hall before the first bell every morning to warm up, as the master asked'}, 'chance': 0.82}),
    ("read the year above's notes on every teacher, and plan how to stand out", 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "ask the older apprentices about the old teller's moods, and plan how to stand out", 'magic': "buy the year above's notes on every master, and plan how to stand out"}, 'chance': 0.65}),
    ('throw a party for the whole year group in your new flat on the first Friday', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': 'gather the apprentices for a night of meat and stories at the first full moon', 'magic': 'throw a supper for the whole year in your lodgings on the first rest day'}, 'chance': 0.9}),
    ('find the other student who looks lost in the canteen, and sit with them', 'R1', 'G.7', 0.5, '', {'door': True, 'v': 'benevolence', 'mark': 'made a friend', 'world': {'tribal': 'find the other apprentice who is far from home, and share your fire with them', 'magic': 'find the other scholar who looks lost at the long table, and sit with them'}, 'chance': 0.92}),
    ('write to the youth theatre leader who started it all, and promise to make them proud', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'send word to the old one of your own band who taught you, and promise to honour them', 'magic': "write to the children's master who started it all, and promise to make them proud"}, 'chance': 0.88}),
 ]},
{'name': 'the movement class where you cannot hide',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'learning, body',
 'horizon': 'months',
 'roles': 'mentor, colleague',
 'requires': 'drama school student',
 'threshold': 'title:drama school student',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, a bare studio, bare feet and no script, and the movement teacher asks each '
                     'student to stand in the middle and simply be looked at',
            'tribal': 'two moons in, the old teller makes you dance the bear alone in the firelight, with no words '
                      'to hide behind, while the other apprentices watch',
            'magic': "ten weeks in, the guild's master of movement makes you walk the length of the hall in silence "
                     'before the whole year, with no mask and no lines'},
 'timing': {'times': 'per new drama school student: once, in the first months of the threshold season, about ten '
                     'weeks in; about 3 lives in 1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of drama school student, within the first six months after taking '
                         'the title: step 2, some weeks into the course, when the classes start to ask for more than '
                         'talent',
             'likelier': 'a course with daily movement and voice classes; a student who has always hidden behind a '
                         'character; a student from a family or a school where nobody acted',
             'rarer': 'a student who trained as a dancer or an athlete; a part-time course with few movement '
                      'classes'},
 'scenes': {'earth': [('',
                       'Ten weeks in, movement is the class {N} dreads. Bare feet, no script, and today {mentor} '
                       'asks each student to stand alone in the middle of the studio for two minutes and do nothing '
                       'while the year group watches. {N} is next.'),
                      ('W',
                       '{N} decides that it is an exercise like any other, set for a reason, and that the rules of '
                       'the room protect everyone in it.'),
                      ('U',
                       '{N} has read about this exercise and knows why it works. Knowing does not stop {Ns} legs '
                       'from shaking.'),
                      ('B',
                       '{N} watches the others go first and notes what the teacher praises: stillness, breath, eyes '
                       'up.'),
                      ('R', 'Being looked at with nothing to do makes {N} want to laugh, run and cry, all at once.'),
                      ('G',
                       '{N} thinks of the body {N} has always known: the walk from home, the way {Ns} family stands. '
                       'Here it is being taken apart.')],
            'tribal': [('',
                        'The old teller beats the drum slowly and points at {N}: dance the bear, alone, in the '
                        'firelight, with no words, while the other apprentices watch.')],
            'magic': [('',
                       'The master of movement strikes his staff on the floor, and {N} must walk the length of the '
                       'hall in silence, without a mask, before the whole year.')]},
 'outcomes': (['{N} stands in the middle and is looked at for two minutes, and the floor does not open.',
               '{mentor} nods once at {N}, which in that studio counts as high praise.'],
              ['{N} freezes, and the two minutes feel like a week.',
               '{N} gets through the class and cries on the bus home, and the next movement class comes round all '
               'the same.']),
 'options': [
    ('do exactly what is asked, and stand there for the full two minutes', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'do what the old teller asks, and dance until the drum stops', 'magic': 'do what the master asks, and walk the whole hall at his pace'}, 'chance': 0.85}),
    ('ask the teacher afterwards what the exercise is for, and keep a notebook on it', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': 'ask the old teller afterwards what the bear dance is for, and remember every word'}, 'chance': 0.9}),
    ('copy exactly what the teacher praised in the others, and give them that', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'copy what the old teller praised in the others, and give him that', 'magic': 'copy what the master praised in the others, and give him that'}, 'chance': 0.7}),
    ('let whatever comes come, tears or laughter, in front of everyone', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'let whatever comes come in the dance, tears or laughter, in front of everyone', 'magic': 'let whatever comes come on the walk, tears or laughter, in front of everyone'}, 'chance': 0.8}),
    ('breathe slowly and think of a place at home until the fear passes', 'G1', None, 0.45, '', {'v': 'tradition, security', 'self_control': '+', 'world': {'tribal': "breathe slowly and think of your own band's river until the fear passes", 'magic': 'breathe slowly and think of the lane where you grew up until the fear passes'}, 'chance': 0.7}),
    ("volunteer to go first, as a good student should, and earn the teacher's eye", 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': "step into the firelight first, as a good apprentice should, and earn the old teller's eye", 'magic': "volunteer to walk first, as a good scholar should, and earn the master's eye"}, 'chance': 0.6}),
    ('make a private game of it: how little can you do and still hold the room', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': "make a private game of it: how little can the bear do and still hold the band's eyes"}, 'chance': 0.78}),
    ('fake a twisted ankle to sit it out, and take the train home for the weekend', 'B1', 'G.7', 0.5, '', {'v': 'security, hedonism', 'mark': 'hid a wrong', 'closed': 'approval: lying to a teacher to miss a class; backfire: the movement teacher sees through it, and the year group hears', 'self_control': '-', 'world': {'tribal': 'say your foot is hurt to sit out the dance, and walk home to your own band for a few days', 'magic': 'plead a twisted ankle to sit out the walk, and take the coach home for the rest day'}, 'chance': 0.85}),
    ('step up beside a classmate who freezes, so they are not alone', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'helped someone in need', 'world': {'tribal': 'step into the firelight beside an apprentice who froze, and dance with them', 'magic': 'walk beside a scholar who froze, so they are not alone'}, 'chance': 0.65}),
    ('find the walk of someone from home in your body, and use it', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'dance the bear the way the old hunters of your band move, and use it', 'magic': 'walk the way your grandmother walked down the lane, and use it'}, 'chance': 0.72}),
 ]},
{'name': 'who you are when you are not acting',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'learning, meaning, friends',
 'horizon': 'years',
 'roles': 'mentor, friend, parent',
 'requires': 'drama school student',
 'threshold': 'title:drama school student',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'four months in, a teacher asks the year who each of them is when they are not acting, and the '
                     'school has started to swallow everything else',
            'tribal': 'by midwinter, the old teller asks each apprentice what they will be when the winter is over, '
                      'and your own band feels very far away',
            'magic': 'by midwinter, the masters ask each scholar who they will be when the masks come off, and the '
                     'life before the guild feels very far away'},
 'timing': {'times': 'per new drama school student: once in the threshold season, about four months in, for most who '
                     'are still open to change; about 3 lives in 1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of drama school student, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, when the course has begun to take "
                         'over the rest of life',
             'likelier': 'a student who moved away from home for the course; old friends and a partner from before; '
                         'a teacher who asks the hard question out loud',
             'rarer': 'a student who lives at home through the course; an older student with a life already settled'},
 'scenes': {'earth': [('',
                       'Four months in, {mentor} stops a class and asks the year a question: who is each of them '
                       'when they are not acting? Nobody answers well. On the bus home {N} sees that the school has '
                       'taken over everything: the friends from before have stopped calling, {parent} asks on the '
                       'phone what all this is for, and the year group has become the only people {N} sees.'),
                      ('W',
                       '{N} thinks of the year group as a company already: thirty people who will carry each other '
                       'through three years, or not at all.'),
                      ('U',
                       '{N} thinks the answer is in the work: the voice, the body, the text. An actor is a '
                       'craftsman, and the craft is enough.'),
                      ('B',
                       '{N} counts: three years, then the showcase, then a hundred agents in the seats. Everything '
                       'here is a step toward that night.'),
                      ('R',
                       '{N} came here because acting is the only time {N} feels fully alive, and that is answer '
                       'enough.'),
                      ('G',
                       '{N} thinks of home: the youth theatre, the town, the people who will come to see whatever '
                       '{N} becomes. Whoever {N} is, {N} is from there.')],
            'tribal': [('',
                        'By midwinter the old teller asks each apprentice what they will be when the winter is over. '
                        "{N} looks at this band's fire and thinks of {Ns} own, far up the river.")],
            'magic': [('',
                       'At the midwinter masque the masters ask each scholar who they will be when the masks come '
                       'off, and {N} finds that the life before the guild has grown very faint.')]},
 'outcomes': (['Before the term ends {N} has an answer to the question, and the work starts to feel like {Ns} own.',
               '{friend} from home comes to the end-of-term sharing and says {N} is more like {N} than ever.'],
              ['Every answer {N} tries sounds false by the next morning, and the question follows {N} into every '
               'class.',
               'The old friends drift away, the school swallows the rest, and {N} is no longer sure whose life this '
               'is.']),
 'options': [
    ('give yourself to the year group, and be the one the company can always count on', 'W1', None, 0.45, '', {'identity': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'give yourself to the apprentices, and be the one the others can always count on', 'magic': 'give yourself to your year, and be the scholar the others can always count on'}, 'chance': 0.8}),
    ('make the craft your life: voice, body and text, every day, for good', 'U1', None, 0.45, '', {'identity': True, 'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'make the telling your life: the voices, the dances and the old words, every day, for good'}, 'chance': 0.65}),
    ('treat the three years as a plan for the showcase, and spend every choice on it', 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'self_control': '+', 'world': {'tribal': "treat the three winters as a road to the summer gathering, where every band's elders will see you", 'magic': 'treat the three years as a road to the final masque, where the brokers sit in the gallery'}, 'chance': 0.85}),
    ('swear to act or do nothing, and burn every other bridge', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'self-direction, stimulation', 'mark': 'took a wild risk', 'world': {'tribal': 'swear to be a teller or nothing, and turn your back on the hunt for good', 'magic': 'swear to be a player or nothing, and turn your back on your old trade for good'}, 'chance': 0.72}),
    ('stay who you were at home, and bring that person into every part', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, self-direction', 'world': {'tribal': 'stay a child of your own band, its speech and its ways, and bring them into every telling', 'magic': 'stay who you were in your own lane, speech and all, and bring it into every part'}, 'chance': 0.7}),
    ('promise the year group a show at the fringe together when the course ends', 'W1', 'R.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'swear with the other apprentices to play together at the outer fires one summer', 'magic': 'swear with your year to take a wagon to the fair together when the course is done'}, 'chance': 0.45}),
    ("join the school's three-year project collecting the old plays of your region", 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'tradition, achievement', 'world': {'tribal': 'learn every telling of your own band by heart, and promise to carry them on', 'magic': "join the school's long work of collecting the old pageants of your home country"}, 'chance': 0.85}),
    ("stand for year rep, and run the year group's dealings with the school", 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, conformity', 'world': {'tribal': 'become the one who speaks for the apprentices to the old teller', 'magic': "stand for the year's speaker, and run its dealings with the masters"}, 'chance': 0.45}),
    ('throw out everything from before, and let the teachers start again from nothing', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, achievement', 'world': {'tribal': 'forget every way of playing from home, and let the old teller start again from nothing', 'magic': 'throw out every habit from before, and let the masters start again from nothing'}, 'chance': 0.7}),
    ('keep the weekend job back home, so you owe nobody and can always go back', 'G1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'security, power', 'world': {'tribal': "keep your place in your own band's hunts, so you owe nobody and can always go back", 'magic': 'keep your old trade at home on rest days, so you owe nobody and can always go back'}, 'chance': 0.72}),
 ]},
{'name': 'the first-year assessment',
 'stages': 'juvenile young_adult adult',
 'age': (16, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'learning, family',
 'horizon': 'months',
 'roles': 'mentor, parent, colleague',
 'requires': 'drama school student',
 'threshold': 'title:drama school student',
 'step': 3,
 'worlds': {'earth': 'the first-year assessment: a speech, a song and a movement piece before the staff panel, and a '
                     'one-to-one that decides who goes on',
            'tribal': 'near the end of the first winter, the old teller hears each apprentice tell the great story '
                      'alone, and says who may stay for a second winter',
            'magic': "the first-year trial: each scholar plays before the guild's masters, and a clerk writes who "
                     'stays on the roll'},
 'timing': {'times': 'per new drama school student: once, about five months in, at the first-year assessment near '
                     'the end of the threshold season; about 3 lives in 1,000 (catalogue share); a few schools ask '
                     'some first-year students to leave (estimate)'},
 'trigger': {'requires': 'in the threshold season of drama school student, within the first six months after taking '
                         'the title: step 3, near the end of the six months, at the first-year assessment',
             'likelier': 'a school that assesses its first-years and keeps the right to ask some to leave; a family '
                         'that lent the fees; a student who had a warning in the first term',
             'rarer': 'a school that never asks a student to leave; a student already picked out as one of the '
                      "year's best"},
 'scenes': {'earth': [('',
                       'At the first-year assessment every student performs a speech, a song and a movement piece '
                       'for the staff panel, then sits in a small room with {mentor} for ten minutes that decide the '
                       "second year. Two of last year's group were not asked back. {parent}, who lent the money for "
                       'the fees, has rung twice to ask when {N} will know.'),
                      ('W',
                       '{N} has kept every note from every class in a folder, and has done everything the teachers '
                       'asked, in order.'),
                      ('U',
                       '{N} knows exactly which notes keep coming back (the breath, the jaw, the hurry) and has '
                       'worked on each one.'),
                      ('B',
                       '{N} has noticed which students the head of acting talks about in the canteen, and {N} is not '
                       'yet one of them.'),
                      ('R', '{N} is sick of being careful. Five months of exercises, and {N} wants to just act.'),
                      ('G',
                       '{N} thinks of the family who lent the money, and of the people at home who keep asking how '
                       'it is going.')],
            'tribal': [('',
                        'Near the end of the first winter the old teller sits by the fire and hears each apprentice '
                        "tell the great story alone. Two of last winter's apprentices were sent home after it.")],
            'magic': [('',
                       'The masters sit in a row in the great hall, and a clerk waits with the roll to write down '
                       'who stays.')]},
 'outcomes': (['The panel keeps {N} on, with notes for the summer and a good word from {mentor}.',
               '{parent} hears the news on the phone, goes quiet, then says they always knew.'],
              ['The verdict is hard: a warning at best, and {N} walks out of the small room shaking.',
               'The one-to-one is ten minutes of things {N} did not want to hear, and the rest of the year will have '
               'to prove them wrong.']),
 'options': [
    ('rehearse the set pieces exactly as taught, every evening for a month', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, tradition', 'self_control': '+', 'grants': 'learning lines', 'world': {'tribal': 'rehearse the great story exactly as the old teller tells it, every evening for a moon', 'magic': 'rehearse the set pieces exactly as the masters taught, every evening for a month'}, 'chance': 0.83}),
    ('work on the one note that keeps coming back, and nothing else', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'world': {'tribal': 'work on the one fault the old teller keeps naming, and nothing else'}, 'chance': 0.6}),
    ('ask the head of acting for a private word about what the panel wants', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'sit with the old teller before the hearing, and find out what he wants to see', 'magic': 'seek out the head master before the trial, and find out what the masters want to see'}, 'chance': 0.7}),
    ('throw away the careful version, and play the speech as you feel it that day', 'R1', None, 0.45, '', {'v': 'stimulation', 'world': {'tribal': 'put aside the careful telling, and tell the story as it comes to you by the fire'}, 'chance': 0.6}),
    ('ask the family to come to the end-of-term sharing, and play it for them', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'ask your own kin to come down the river for the hearing, and tell it for them', 'magic': 'ask your family to come to the end-of-term playing, and play it for them'}, 'chance': 0.65}),
    ('spend the last week helping the classmates who are struggling, not only yourself', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'helped someone in need', 'world': {'tribal': 'spend the last days helping the apprentices who are struggling, not only yourself'}, 'chance': 0.9}),
    ('write out every note from the panel this year, and answer each one in turn', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'self_control': '+', 'world': {'tribal': 'go over every fault the old teller named all winter, and mend each in turn', 'magic': 'copy out every note the masters gave all year, and answer each one in turn'}, 'chance': 0.85}),
    ("borrow last year's best student's notes, and copy how they passed", 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, power', 'world': {'tribal': "ask last winter's best apprentice how they passed, and copy them", 'magic': "buy last year's best scholar's notes, and copy how they passed"}, 'chance': 0.88}),
    ('skip the classes you find pointless, and pour the time into your acting piece', 'R1', 'B.7', 0.5, '', {'v': 'self-direction, achievement', 'drops_if_fails': 'drama school student', 'world': {'tribal': 'skip the dances you find pointless, and pour the days into your telling', 'magic': 'skip the lessons you find pointless, and pour the hours into your piece'}, 'chance': 0.85}),
    ('spend the weekend before at home, walking the old places, and come back fresh', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, tradition', 'world': {'tribal': 'go back up the river to your own band before the hearing, and come back fresh', 'magic': 'spend the rest day at home walking the old lanes, and come back fresh'}, 'chance': 0.9}),
 ]},
{'name': 'the first paid read-through',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work, friends',
 'horizon': 'week',
 'roles': 'boss, colleague, partner',
 'requires': 'professional actor',
 'threshold': 'title:professional actor',
 'step': 1,
 'worlds': {'earth': 'the first paid job: a long table, a script with your name on the cast list, and a cup of tea '
                     'you are too nervous to drink',
            'tribal': "the first winter as the band's teller-player, fed by every hearth, and the first night you "
                      'sit among the tellers as one of them',
            'magic': 'the first reading with a licensed company, and your name in small letters on the playbill'},
 'timing': {'times': 'per new professional actor: once, in the first weeks after taking the title; about 4 lives in '
                     '1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of professional actor, within the first six months after taking '
                         "the title (opened by 'the showcase for agents', 'an open audition in the city' or any "
                         'other way in): step 1, the first paid job',
             'likelier': 'a first paid part after drama school or an open call; a company of older actors; a '
                         'director who reads the play round a table on the first day',
             'rarer': 'a first job on a film set with no read-through; an actor who turned professional after years '
                      'as an amateur in the same company'},
 'scenes': {'earth': [('',
                       'The first day of the first paid job: a long table in a rehearsal room, a script with {Ns} '
                       'name on the cast list, and a cup of tea {N} is too nervous to drink. Around the table sit '
                       'actors {N} has watched for years. {boss}, the director, says a few words, and the '
                       'read-through begins.'),
                      ('W',
                       '{N} has learned the first act already, marked every entrance and arrived forty minutes '
                       'early.'),
                      ('U',
                       '{N} has read the play six times, has a question about every scene, and is not sure whether a '
                       'new actor may ask them.'),
                      ('B',
                       '{N} notices who the director laughs with, which actor the producer came to see, and where '
                       'the next job might come from.'),
                      ('R', '{N} cannot stop grinning. Someone is paying {N} to do this.'),
                      ('G',
                       '{N} thinks of {partner} and the people at home who said it would never happen, and of the '
                       'old company that taught {N} how.')],
            'tribal': [('',
                        "For the first time {N} sits among the band's tellers as one of them, and every hearth has "
                        "sent meat to the tellers' fire for the winter.")],
            'magic': [('',
                       'The company gathers at a long table in the playhouse, the playbill on the wall carries {Ns} '
                       'name in small letters, and the master of the play calls for the first reading.')]},
 'outcomes': (['By the end of the read-through {N} has stopped shaking, and {boss} catches {Ns} eye at a good '
               'moment.',
               'The company goes to the pub afterwards, and someone saves {N} a seat.'],
              ['{N} stumbles over the first line and never quite recovers, and the day goes by in a blur of nerves.',
               'Something {N} did at the table is remembered by the whole company, and not in a good way.']),
 'options': [
    ('read exactly as you rehearsed at home, and mark every note in pencil', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'world': {'tribal': 'tell your part exactly as you learned it, and keep every word the shaper gives', 'magic': 'read exactly as you prepared it, and mark every note in the margin'}, 'chance': 0.9}),
    ('ask the director one good question about your character at the first break', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'ask the shaper one good question about your spirit at the first rest', 'magic': 'ask the master of the play one good question about your part at the first break'}, 'chance': 0.85}),
    ('sit next to the actor the producer came to see, and make them laugh', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'sit beside the teller the elders favour, and make them laugh', 'magic': "sit beside the company's favourite player, and make them laugh"}, 'chance': 0.82}),
    ('read your big scene full out, as if it were the first night', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'tell your part full out, as if the whole band were watching', 'magic': 'read your big scene full out, as if the house were full'}, 'chance': 0.78}),
    ('bring a cake for the whole company, as your old company always did', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': "bring a share of your own family's meat to the tellers' fire", 'magic': 'bring a basket of buns for the whole company, as your old pageant players always did'}, 'chance': 0.92}),
    ('learn the name of everyone in the company and crew before lunch', 'W1', 'B.7', 0.5, '', {'door': True, 'v': 'conformity, power', 'world': {'tribal': 'learn the name of every teller and every keeper of the fire before midday', 'magic': 'learn the name of every player and stagehand before the noon bell'}, 'chance': 0.75}),
    ('listen hard to the others, and enjoy every surprise the play holds', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': "listen to the others' tellings more than your own, and enjoy every surprise in the story"}, 'chance': 0.9}),
    ("get cheap digs through the stage manager's contacts, and send the savings home", 'B1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'world': {'tribal': 'get a place at a rich hearth through the keeper of the fire, and send your own meat home to your kin', 'magic': "get cheap lodgings through the book-keeper's friends, and send the savings home"}, 'chance': 0.72}),
    ('admit at the first break that you have not finished learning the second act', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, self-direction', 'mark': 'owned up', 'world': {'tribal': 'admit at the first rest that you do not yet know the second part of the telling', 'magic': 'admit at the first break that you have not yet learned the second act'}, 'chance': 0.8}),
    ('ask the oldest actor at the table how they have kept going for forty years', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'tradition, achievement', 'mark': 'made a friend', 'world': {'tribal': 'ask the oldest teller at the fire how they kept their voice for forty winters', 'magic': "ask the company's oldest player how they have kept going for forty seasons"}, 'chance': 0.92}),
 ]},
{'name': 'the second job does not come',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'work, money, family',
 'horizon': 'months',
 'roles': 'partner, friend',
 'requires': 'professional actor',
 'threshold': 'title:professional actor',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the first job has closed, the agent has gone quiet, and the bar job is back, '
                     'with self-tapes squeezed in between the shifts',
            'tribal': 'two moons in, the winter tellings are over, the band no longer feeds its tellers, and you are '
                      'back on the hunt with nothing to tell',
            'magic': "ten weeks in, the company's season has closed, no master has sent for you, and you are back at "
                     'your old trade, learning speeches by candlelight'},
 'timing': {'times': 'per new professional actor: once, in the first months of the threshold season, about ten weeks '
                     'in, for most whose first job has ended; 71 in 100 UK actors spend 28 weeks or more of a year '
                     "outside the industry (the UK actors' union's survey); about 4 lives in 1,000 (catalogue "
                     'share)'},
 'trigger': {'requires': 'in the threshold season of professional actor, within the first six months after taking '
                         'the title: step 2, some weeks into the career, when the first job has closed and no second '
                         'one has come',
             'likelier': 'a first job that was a short run; an actor without an agent; hard years for theatres; a '
                         'day job to go back to',
             'rarer': 'an actor who went straight from one job into the next; an actor kept on by a company for the '
                      'whole season'},
 'scenes': {'earth': [('',
                       'Ten weeks in, the first job has closed. The agent has gone quiet, three self-tapes have '
                       'vanished without a word, and {N} is back on the early shift at the café, running lines at '
                       'the till. {partner} asks gently whether this is how it is going to be, and {friend} has '
                       'offered a proper job with a proper wage.'),
                      ('W',
                       '{N} keeps the routine: a self-tape when one comes, a class every week, the day job done '
                       'well. It is what working actors do.'),
                      ('U',
                       '{N} goes over every audition, looking for the reason. There must be something to learn from '
                       'each no.'),
                      ('B',
                       '{N} works out who is getting the parts and how: whose agent, which class, which casting '
                       "director's favourite."),
                      ('R',
                       'The waiting is unbearable. {N} wants to do something, anything, to be acting again tonight.'),
                      ('G',
                       'Everyone said it would be like this. {N} thinks of the old actors who said the work comes in '
                       'seasons, like the weather.')],
            'tribal': [('',
                        'Two moons in, the winter tellings are over and the band no longer feeds its tellers. {N} is '
                        'back on the hunt, and the young hunters ask when the next telling will be.')],
            'magic': [('',
                       "The company's season has closed, no master has sent word, and {N} is back at the old "
                       'workbench, learning speeches by candlelight between orders.')]},
 'outcomes': (["A call comes at last: a small part and a few weeks' work, and {N} is an actor again.",
               '{N} learns to live in the gaps: the day job, the classes, the self-tapes, and a life that goes on '
               'between them.'],
              ['The weeks turn into months, and {N} stops telling people at parties what {N} does.',
               '{partner} and {N} have the same argument about money for the third time, and nobody wins it.']),
 'options': [
    ('keep the day job, do every self-tape properly, and go to class each week', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'hunt with the band by day, and keep your tellings sharp by the fire every night', 'magic': 'keep your trade by day, and practise your speeches every night, as players must'}, 'chance': 0.78}),
    ('watch your own self-tapes back, and find what the casting directors are not seeing', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'go over every telling you gave in your head, and find what the elders did not see in it', 'magic': 'go over every trial you gave, and find what the masters did not see in it'}, 'chance': 0.7}),
    ('add two credits you never had and stage combat to your CV', 'B1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': 'approval: false credits and skills on a casting CV; backfire: a casting director checks, or the next job puts the actor in a sword fight', 'world': {'tribal': 'tell the other bands you played in two great tellings you never saw', 'magic': 'add two companies you never played with, and swordplay, to your letter to the brokers'}, 'chance': 0.78}),
    ('put on your own show in a pub back room every week, rather than wait', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'self_control': '+', 'world': {'tribal': 'tell a story of your own at the outer fire every few nights, rather than wait to be asked', 'magic': 'play a piece of your own in a tavern yard every week, rather than wait for a company'}, 'chance': 0.74}),
    ("take the old friend's steady job, and let acting go for now", 'G1', None, 0.45, '', {'v': 'security, tradition', 'self_control': '-', 'drops': 'professional actor', 'world': {'tribal': 'go back to the hunt for good, and let the tellings go for now', 'magic': 'go back to your old trade for good, and let the playhouse go for now'}, 'chance': 0.85}),
    ('make one rule and keep it: an audition or a show every week, however small', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, conformity', 'self_control': '+', 'world': {'tribal': 'make one rule and keep it: a telling at some fire every moon, however small', 'magic': 'make one rule and keep it: a trial or a show every week, however small'}, 'chance': 0.6}),
    ('learn the regional theatres near home inside out, and write to each with a plan', 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'learn which bands near your own want which tellings, and send word to each with an offer', 'magic': 'learn the playhouses of your home country inside out, and write to each with a plan'}, 'chance': 0.45}),
    ("take paid work as a casting office's reader, to be in the room every week", 'B1', 'W.7', 0.5, '', {'v': 'achievement, security', 'grants': 'contact in the trade', 'world': {'tribal': 'become the one who speaks the other parts when the elders hear new players', 'magic': "get paid work as the reader at a company's trials, to be in the room every week"}, 'chance': 0.55}),
    ('go to every free workshop and late-night class in the city, out of pure hunger', 'R1', 'U.7', 0.5, '', {'habit': True, 'door': True, 'v': 'stimulation, achievement', 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'sit at every fire where an old teller is teaching, out of pure hunger', 'magic': 'go to every open lesson and late class in the city, out of pure hunger'}, 'chance': 0.9}),
    ('ask your old youth theatre leader to put your name forward to anyone they know', 'G1', 'B.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the old teller of your own band to speak for you at other fires', 'magic': "ask your old children's master to put your name forward to the companies he knows"}, 'chance': 0.55}),
 ]},
{'name': 'what kind of actor you will be',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'mentor, colleague',
 'requires': 'professional actor',
 'threshold': 'title:professional actor',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'four months in, new photographs for the casting directory, and one line beneath them that says '
                     'what kind of actor you are',
            'tribal': 'four moons in, the elders ask at the fire what kind of teller-player you mean to be, and the '
                      'band will remember your answer',
            'magic': "four months in, the brokers' roll asks for a line beneath your name, and an old player asks "
                     'over wine what kind of player you mean to be'},
 'timing': {'times': 'per new professional actor: once in the threshold season, about four months in, for most who '
                     'are still open to change; about 4 lives in 1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of professional actor, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, when the first choices about the kind "
                         'of work begin',
             'likelier': 'an actor with two kinds of offer at once; an agent who asks for a plan; an actor who '
                         'trained in one tradition and worked in another',
             'rarer': 'an actor with no work at all that month; an older actor who came to it late and wants only to '
                      'act'},
 'scenes': {'earth': [('',
                       'Four months in, {N} sits for new photographs for the casting directory, and the form asks '
                       'for one line beneath them: what kind of actor is this? {mentor}, an old actor from the first '
                       'job, says over a drink that the next three choices will answer the question whether {N} does '
                       'or not.'),
                      ('W',
                       '{N} thinks of the old hands on the first job: there every night, word-perfect, holding the '
                       'show together without anyone noticing.'),
                      ('U',
                       '{N} thinks of the parts that frighten {N}, the great old plays, and the years of work it '
                       'would take to be ready for them.'),
                      ('B',
                       '{N} looks at the careers {N} admires and sees the pattern: the right agent, the right parts, '
                       'a plan, and no time wasted.'),
                      ('R',
                       '{N} wants the rush of the first night again and again: the big part, the risk. Nothing else '
                       'feels like being alive.'),
                      ('G',
                       '{N} thinks of the theatre in the home town, of the people there who would come every season, '
                       'and of acting as something that belongs to a place.')],
            'tribal': [('',
                        'Four moons in, the elders ask {N} at the fire what kind of teller-player {N} means to be. '
                        'The band will remember the answer.')],
            'magic': [('',
                       "Four months in, the brokers' roll asks for a line beneath {Ns} name, and an old player of "
                       'the company asks over wine what kind of player {N} means to be.')]},
 'outcomes': (['The answer holds: within weeks the next choices fall into line, and the work starts to look like a '
               'road.',
               '{mentor} hears what {N} chose and raises a glass to it.'],
              ['{N} writes three different lines under the photographs and deletes them all, and the next job '
               'decides for {N}.',
               'The choice is made, the first door it needs stays shut, and {N} wonders whether it was the wrong '
               'one.']),
 'options': [
    ('be the company player: word-perfect, there every night, ready for whatever the show needs', 'W1', None, 0.45, '', {'identity': True, 'v': 'conformity, benevolence', 'world': {'tribal': "be the band's steady teller: word-perfect, there every night, ready for whatever the telling needs", 'magic': "be the company's steady player: word-perfect, there every night, ready for any part"}, 'chance': 0.82}),
    ('train for the great parts: a class every week for years, voice, text and body', 'U1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': 'train for the great tellings: every voice and every dance, every day for years', 'magic': 'train for the great parts of the old plays with a master of voice, for years'}, 'chance': 0.7}),
    ('build a career with a plan: the right agent, the right parts, nothing beneath it', 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'world': {'tribal': 'plan a road to the great mask: the right elders, the right tellings, nothing beneath it', 'magic': 'plan a road to the court playhouse: the right broker, the right parts, nothing beneath it'}, 'chance': 0.7}),
    ('chase the frightening parts, and never take the safe one', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation', 'world': {'tribal': 'ask for the tellings that frighten the others, and never take the safe part'}, 'chance': 0.68}),
    ('go back to the theatre of your home region, and become its actor', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'tradition, benevolence', 'mark': 'came home', 'world': {'tribal': 'go back to your own band, and become its teller-player for good', 'magic': 'go back to the playhouse of your home town, and become its player'}, 'chance': 0.45}),
    ('join a touring company that takes plays to towns that never see one', 'W1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, benevolence', 'world': {'tribal': 'walk with the tellers who carry the old stories to the small bands of the hills', 'magic': 'join a wagon company that plays the villages no licensed company visits'}, 'chance': 0.6}),
    ('specialise in the old verse plays, and learn their rules line by line', 'U1', 'W.7', 0.5, '', {'identity': True, 'v': 'achievement, conformity', 'world': {'tribal': 'learn the oldest tellings word for word, as the band has always kept them', 'magic': 'specialise in the old verse plays of the realm, and learn their rules line by line'}, 'chance': 0.78}),
    ('sign with an agent for adverts and company films, and pay for training with it', 'B1', 'U.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'achievement, security', 'world': {'tribal': 'promise to play at every feast a rich family gives, and trade the gifts for lessons with the best teller', 'magic': 'sign with a broker for the mirror-plays of the great houses, and pay a master of voice with it'}, 'chance': 0.7}),
    ('throw everything at one big audition season, and make your name or quit', 'R1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'achievement, stimulation', 'mark': 'took a wild risk', 'world': {'tribal': 'throw everything at the summer gathering, to be seen by every band or go back to the hunt', 'magic': "throw everything at the court season's trials, to make your name or go home"}, 'chance': 0.35}),
    ('act wherever the road leads, with whoever is there, for the joy of it', 'G1', 'R.7', 0.5, '', {'identity': True, 'v': 'hedonism, self-direction', 'world': {'tribal': 'play wherever the band camps, with whoever is at the fire, for the joy of it'}, 'chance': 0.85}),
 ]},
{'name': 'half a year on, still an actor',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work, friends, family',
 'horizon': 'months',
 'roles': 'friend, partner, colleague',
 'requires': 'professional actor',
 'threshold': 'title:professional actor',
 'step': 3,
 'worlds': {'earth': 'five months in and still an actor: friends from before ask when you will be on television, a '
                     'partner sees you between jobs, and a company has become a second family',
            'tribal': 'five moons in and still a teller-player: the hunters you grew up with tease you at the river, '
                      "and the tellers' fire has become a second hearth",
            'magic': 'five months in and still a player: old friends ask when you will play at court, and the '
                     'company has become a second family on the road'},
 'timing': {'times': 'per new professional actor: once, about five months in, near the end of the threshold season; '
                     'about 4 lives in 1,000 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of professional actor, within the first six months after taking '
                         'the title: step 3, near the end of the six months, when the first months as an actor have '
                         'settled into a life',
             'likelier': 'an actor with a partner or a family from before; old friends outside the trade; a few jobs '
                         'behind them',
             'rarer': 'an actor who has worked without a break; an actor from a family of actors'},
 'scenes': {'earth': [('',
                       'Five months on, {N} is still an actor, just: a second job, a few days on a series, and a lot '
                       'of waiting in between. At a wedding {friend} introduces {N} as "the actor", and everyone '
                       'asks the same two questions: what has {N} been in, and has {N} met anyone famous? {partner} '
                       'has learned the timetable of a working actor: weeks of nothing, then weeks of never being '
                       'home.'),
                      ('W',
                       "{N} has found the rhythm: the day job's rota, the class on Tuesdays, self-tapes on Sundays, "
                       'the union subscription paid on time.'),
                      ('U',
                       '{N} has started to notice what {N} does better than six months ago, and what has not changed '
                       'at all.'),
                      ('B',
                       '{N} counts what the first months have brought: two credits, a few contacts, a casting '
                       'director who remembers {Ns} name. A beginning.'),
                      ('R',
                       '{N} is tired of explaining at weddings what an actor does all week, and longs for the next '
                       'first night.'),
                      ('G',
                       'The old friends from home have not changed, and {N} has, a little. Some evenings that is a '
                       'comfort, and some evenings it is not.')],
            'tribal': [('',
                        "Five moons on, the hunters {N} grew up with tease {N} at the river about the tellers' soft "
                        "hands, and the tellers' fire has become a second hearth.")],
            'magic': [('',
                       'Five months on, old friends in the lane ask when {N} will play at court, and the company has '
                       'become a second family on the road.')]},
 'outcomes': (['Half a year in, {N} can say "I\'m an actor" without looking at the floor.',
               '{partner} comes to see the small part in the latest show, and cheers at the curtain call.'],
              ['The half-year ends with more waiting than working, and {N} counts the money twice a week.',
               'An old friend says, not unkindly, that {N} has changed, and {N} cannot say they are wrong.']),
 'options': [
    ('pay the union subscription, keep a diary, and treat acting as a proper job', 'W1', None, 0.45, '', {'v': 'conformity, security', 'grants': 'union card', 'world': {'tribal': "take your place among the band's tellers before the elders, and keep its customs", 'magic': "pay your dues to the players' guild, and keep your token bright"}, 'chance': 0.9}),
    ('write down what you can do now that you could not six months ago', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'go over by the fire what you can do now that you could not five moons ago'}, 'chance': 0.95}),
    ('follow up every contact from the half-year with a note and a new photograph', 'B1', None, 0.45, '', {'habit': True, 'v': 'power, achievement', 'self_control': '+', 'world': {'tribal': 'send a small gift to every teller and elder who praised your telling this winter', 'magic': 'send a note and a new likeness to every master and broker you met this season'}, 'chance': 0.85}),
    ('answer the questions at the wedding with a wild story, and dance till they close', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'world': {'tribal': "answer the hunters' teasing with a wild telling of your own, and dance till the fire dies", 'magic': 'answer the questions at the feast with a tall tale, and dance till the tavern closes'}, 'chance': 0.94}),
    ('keep Sunday dinner with the family, whatever job you are in', 'G1', None, 0.45, '', {'habit': True, 'v': 'tradition, benevolence', 'self_control': '+', 'world': {'tribal': "eat at your mother's hearth every few days, whatever telling you are in", 'magic': 'keep the rest-day meal with your family, whatever company you are with'}, 'chance': 0.6}),
    ('go to class every Tuesday, even in the weeks when there is work', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'sit with the old teller every few nights, even when you are in a telling', 'magic': "go to the guild's lesson every week, even when you are in a play"}, 'chance': 0.65}),
    ('work out which castings led to work, and spend your time only on those', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'work out which tellings brought gifts, and give your days only to those', 'magic': 'work out which trials led to a part, and spend your coin only on those'}, 'chance': 0.75}),
    ('spend the fee from the last job on a week away with your partner', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': "trade the winter's gifts for a feast with your partner", 'magic': "spend the season's wages on a week by the sea with your partner"}, 'chance': 0.9}),
    ('bring your new actor friends home to meet the old ones, and see what happens', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'made a friend', 'world': {'tribal': "bring the tellers to your own band's fire, and let the two worlds meet", 'magic': 'bring the company to the old tavern in your lane, and let the two worlds meet'}, 'chance': 0.75}),
    ('go back to your old youth theatre, and run a free workshop for the children', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': "go back to the children of your own band, and teach them the small spirits' parts", 'magic': "go back to the guild's children's company, and teach them a free lesson"}, 'chance': 0.9}),
 ]},
{'name': 'your name at the top of the bill',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work, public life',
 'horizon': 'week',
 'roles': 'boss, colleague, partner',
 'requires': 'lead actor or actress',
 'threshold': 'title:lead actor or actress',
 'step': 1,
 'worlds': {'earth': 'the first weeks as the lead: your name above the title or at the top of the call sheet, your '
                     'name on a dressing room door, and a whole company taking its cue from you',
            'tribal': 'the first days with the great mask on its peg by your hearth, and every child of the band '
                      'watching you pass',
            'magic': "the first weeks as the leading player: your name cried first by the herald, and a patron's "
                     'flowers in the dressing room'},
 'timing': {'times': 'per new lead: once, in the first weeks after taking the part; about 1 life in 1,000 (catalogue '
                     'share; estimate)'},
 'trigger': {'requires': 'in the threshold season of lead actor or actress, within the first six months after taking '
                         "the part (opened by 'the understudy goes on', 'the part of a lifetime is cast', 'a screen "
                         "test', 'the leading player leaves the company', 'opening night at the fringe', 'the lead "
                         "voice in a series', 'the director calls again', 'two actors, one part' or any other way "
                         'in): step 1, the first weeks at the top of the bill',
             'likelier': 'a first lead; a run in a big theatre, or a series with a launch; an actor who was unknown '
                         'a month ago',
             'rarer': 'a lead in a small touring show; an actor who has led a company before'},
 'scenes': {'earth': [('',
                       'In the first week as the lead, {Ns} name goes up above the title: on the poster, on the '
                       'front of the theatre, at the top of the call sheet. There is a dressing room with {Ns} name '
                       'on the door, a car on the first morning, and a company that now takes its cue from {N}. '
                       '{boss} says the show will be as good as its lead, and means it kindly.'),
                      ('W',
                       '{N} feels the weight of it: thirty people whose work now depends on the lead turning up, '
                       'word-perfect and well, every single night.'),
                      ('U',
                       '{N} goes back to the script and reads it as the lead for the first time. Every scene is now '
                       'about how {N} carries it.'),
                      ('B',
                       '{N} notices what has changed: the producer returns calls, the press office wants interviews, '
                       'and a bigger agency has rung twice.'),
                      ('R',
                       '{N} walks past the poster three times on the first morning, and laughs out loud the third '
                       'time.'),
                      ('G',
                       '{N} thinks of the actors who led this company before, and of {partner} at home, who will now '
                       'see {N} mostly on Sundays.')],
            'tribal': [('',
                        'The great mask of the first ancestor hangs on its peg by {Ns} hearth. Every child of the '
                        'band stops to look at it, and then at {N}.')],
            'magic': [('',
                       "The herald cries {Ns} name first in the square, before the name of the play, and a patron's "
                       'flowers wait in the dressing room with no card.')]},
 'outcomes': (['By the end of the first week the company has taken to {N} as its lead, and the part has started to '
               'feel like {Ns} own.',
               '{boss} watches the Friday run and says nothing at all, which from {boss} is high praise.'],
              ['The first week goes by in interviews, fittings and nerves, and {N} has barely rehearsed.',
               'Something {N} said or did in the first week reaches the whole company by Friday, and the dressing '
               'rooms go a little quieter.']),
 'options': [
    ('be first in and last out every day, and learn every name in the building', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, benevolence', 'world': {'tribal': 'be first to the fire and last to leave it every day, and know every player by name', 'magic': 'be first into the playhouse and last out every day, and learn every name in it'}, 'chance': 0.85}),
    ('go back to the script, and rework every scene as the one who carries it', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'go back over the whole telling, and rework every part as the one who wears the mask'}, 'chance': 0.8}),
    ('take the call from the bigger agency, and hear what they offer', 'B1', None, 0.45, '', {'door': True, 'v': 'power, achievement', 'world': {'tribal': 'hear out the go-between from a greater band, and what they offer', 'magic': "hear out the grandest players' broker in the city, and what she offers"}, 'chance': 0.95}),
    ('walk past your own name on the poster, and point it out to a stranger', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'world': {'tribal': 'walk through the camp past the great mask, and grin at every child who stares', 'magic': 'stand in the square while the herald cries your name, and grin at the crowd'}, 'chance': 0.9}),
    ('ask the last actor to lead this company how they held it', 'G1', None, 0.45, '', {'v': 'tradition, achievement', 'mark': 'made a friend', 'world': {'tribal': 'ask the last wearer of the great mask how they carried it', 'magic': "ask the company's last leading player how they held it"}, 'chance': 0.75}),
    ('throw a first-week party for the whole company and crew, at your own cost', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, hedonism', 'world': {'tribal': 'give a feast for every player and keeper of the fire, from your own stores', 'magic': 'throw a feast for the whole company and the stagehands, at your own cost'}, 'chance': 0.88}),
    ('read up on everyone who ever played the part, and learn from the old productions', 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'listen to the old ones tell of every wearer of the great mask there has ever been', 'magic': "read the playhouse's records of every player who ever held the part"}, 'chance': 0.92}),
    ('use your new weight to win the understudies a proper rehearsal every week', 'B1', 'W.7', 0.5, '', {'v': 'universalism, power', 'world': {'tribal': 'use your new place to make the elders let the second learn the mask properly at the fire', 'magic': 'use your new name to win the seconds a proper rehearsal every week'}, 'chance': 0.65}),
    ('throw out the way you rehearsed it, and find the part again with the full company', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'forget how you practised the mask, and find it again at the full fire'}, 'chance': 0.45}),
    ('bring old friends from home in as your dresser and your driver', 'G1', 'B.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'bring your own kin to the gathering to keep your mask, your fire and your food', 'magic': 'bring old friends from the lane in as your dresser and your coachman'}, 'chance': 0.4}),
 ]},
{'name': 'the company looks to you',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'work, friends, family',
 'horizon': 'months',
 'roles': 'colleague, boss, partner',
 'requires': 'lead actor or actress',
 'threshold': 'title:lead actor or actress',
 'step': 2,
 'worlds': {'earth': "ten weeks in, eight shows a week, a tired company with a quarrel in it, a sponsors' dinner "
                     'after the show, and a partner you only see asleep',
            'tribal': 'two moons in, a telling every night, two players quarrelling at the fire, the elders wanting '
                      'you at every council, and your own hearth gone cold',
            'magic': "ten weeks in, two plays a day, a company feuding in the wings, a patron's supper after every "
                     'show, and a household that sees you only asleep'},
 'timing': {'times': 'per new lead: once, in the first months of the threshold season, about ten weeks into the run; '
                     'about 1 life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of lead actor or actress, within the first six months after taking '
                         "the part: step 2, some weeks into the run, when the lead's weight on the company is felt",
             'likelier': 'a long run with eight shows a week; a large company; a show the producers need to sell; a '
                         'partner at home',
             'rarer': 'a short run; a play for two actors; a lead voice recorded alone in a booth'},
 'scenes': {'earth': [('',
                       'Ten weeks in, eight shows a week. Two of the company have stopped speaking to each other, '
                       'the houses are thin on wet Tuesdays, and the stage manager says quietly that everyone is '
                       "waiting to see what the lead does. The producers want {N} at a sponsors' dinner after "
                       "Thursday's show, and {partner} has not seen {N} awake on a weekday for a month."),
                      ('W',
                       'The lead sets the tone. If {N} is late, tired or careless, the whole company will be too, '
                       'and {N} feels it every night.'),
                      ('U',
                       '{N} can feel the show from the inside going slack: a scene rushed here, a laugh lost there.'),
                      ('B',
                       "The sponsors' dinner matters. These are the people who pay for the next show, and the next "
                       'lead.'),
                      ('R',
                       '{N} is exhausted and still wired after every show, and wants nothing more than to stay out '
                       'till three with the company.'),
                      ('G',
                       '{N} misses home: the Sunday walks, the small life. The company has become a family of its '
                       'own, with all the quarrels of one.')],
            'tribal': [('',
                        'Two moons in, the tellings come every night. Two players quarrel at the fire, the elders '
                        'want {N} at every council, and {Ns} own hearth goes cold.')],
            'magic': [('',
                       'Ten weeks in, two plays a day. Two players feud in the wings, a patron wants {N} at supper '
                       'after every show, and {Ns} household sees {N} only asleep.')]},
 'outcomes': (['The company settles, the slack goes out of the show, and the dressing rooms are cheerful again by '
               'the end of the month.',
               '{partner} says one Sunday that {N} seems to have found a way to lead and still come home.'],
              ['The quarrel spreads, the show goes flat, and the company blames the lead.',
               '{N} holds the company together and falls apart a little at home, too tired to talk.']),
 'options': [
    ('call the two who are feuding into your dressing room, and settle it fairly', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'call the two quarrelling players to your hearth, and settle it by custom', 'magic': 'call the feuding players to your dressing room, and settle it fairly'}, 'chance': 0.45}),
    ('read every comment about the show online after each performance, into the small hours', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '-', 'world': {'tribal': 'lie awake going over every word the band said about the telling, into the small hours', 'magic': 'read every broadsheet and every scrap of gossip about the show, into the small hours'}, 'chance': 0.85}),
    ("go to the sponsors' dinner every week, and become the face of the show", 'B1', None, 0.45, '', {'habit': True, 'v': 'power, achievement', 'world': {'tribal': "sit at every elders' council, and become the face of the tellings", 'magic': "go to the patron's supper after every show, and become the face of the company"}, 'chance': 0.85}),
    ("go drinking with the company after every show, to keep everyone's spirits up", 'R1', None, 0.45, '', {'habit': True, 'v': 'hedonism, stimulation', 'self_control': '-', 'world': {'tribal': 'dance with the players every night after the telling, till the fire dies', 'magic': 'drink and sing with the company in the tavern every night after the show'}, 'chance': 0.78}),
    ('keep one day a week for home, and guard it from the producers', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'self_control': '+', 'world': {'tribal': 'keep one day in every few at your own hearth, and guard it from the elders', 'magic': 'keep the rest day for your household, and guard it from every patron'}, 'chance': 0.7}),
    ('start a company meal between the Saturday shows, everyone at one table', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'mark': 'made a friend', 'world': {'tribal': "share one meal at the tellers' fire before every telling, everyone together", 'magic': 'start a company supper between the two plays on market days, everyone at one table'}, 'chance': 0.8}),
    ('ask the director back in to rehearse the slack scenes, with a clean-up call', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'ask the shaper to come back and work the slack parts with the players', 'magic': 'ask the master of the play to call the company for a clean-up rehearsal'}, 'chance': 0.45}),
    ('use your weight to have the feuding actor moved, and the part recast', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'mark': 'made an enemy', 'world': {'tribal': 'use your place to have the quarrelling player sent from the telling', 'magic': 'use your name to have the troublemaker moved, and the part recast'}, 'chance': 0.4}),
    ("tell the producers there will be no more sponsors' dinners, and let them sulk", 'R1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'mark': 'defied an authority', 'world': {'tribal': 'tell the elders you will sit at no more councils, and let them grumble', 'magic': 'tell the patron you will sup with him no more, and let him sulk'}, 'chance': 0.66}),
    ('take the whole company to the park on a free afternoon, to play like children', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'body': 'light', 'world': {'tribal': 'take the players to the river on a free day, to swim and play like children', 'magic': 'take the company to the meadows on a rest day, to play like children'}, 'chance': 0.82}),
 ]},
{'name': 'who you play it for',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'partner, colleague',
 'requires': 'lead actor or actress',
 'threshold': 'title:lead actor or actress',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'four months in, a long interview asks who you play the part for every night, and the true '
                     'answer is not the one you gave',
            'tribal': 'four moons in, the shaman sits by your fire and asks who you wear the great mask for, and the '
                      'summer is half gone',
            'magic': 'four months in, a broadsheet asks whom the leading player plays for, and the question will not '
                     'leave you'},
 'timing': {'times': 'per new lead: once in the threshold season, about four months in, for most who are still open '
                     'to change; about 1 life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of lead actor or actress, within the first six months after taking '
                         "the part: step 2, the season's transforming chance, once the run has shown what the lead "
                         'costs and what it brings',
             'likelier': 'a run that has gone well; an offer of the next part; an actor who came to the lead from '
                         'far away',
             'rarer': 'a run about to close early; an actor who has led many times before'},
 'scenes': {'earth': [('',
                       'Four months in, a journalist doing a long interview asks a simple question: who does {N} '
                       'play it for, every night? {N} gives a good answer for the article and lies awake afterwards, '
                       'because it was not the true one. The run will end, and the next choices will show what the '
                       'lead was for.'),
                      ('W',
                       '{N} thinks of the company: the understudy, the dressers, the stage manager calling the show. '
                       'The lead serves them first.'),
                      ('U',
                       '{N} thinks of the part itself, and of the scene in the second act that {N} has still not got '
                       'right after a hundred performances.'),
                      ('B',
                       '{N} thinks of what comes next: the film offer, the bigger agency, the next lead. This part '
                       'is a door, and {N} means to go through it.'),
                      ('R',
                       '{N} thinks of the house: the moment the lights go down and eight hundred strangers hold '
                       'their breath together. That is what it is for.'),
                      ('G',
                       '{N} thinks of the people from home who drove four hours to see it, and the old drama teacher '
                       'in the third row, crying.')],
            'tribal': [('',
                        'Four moons in, the shaman sits by {Ns} fire and asks who {N} wears the great mask for: the '
                        'band, the ancestor, {Ns} own name, the other players or {Ns} own hearth.')],
            'magic': [('',
                       'Four months in, a broadsheet asks whom the leading player plays for, and {N} finds that the '
                       'question will not leave.')]},
 'outcomes': (['The answer holds, and the last months of the run feel like {Ns} own, whatever the notices say.',
               'Long after, people who worked on the show can say what kind of lead {N} was, and they say it '
               'warmly.'],
              ['{N} tries to play it for everyone at once, and some nights it is played for nobody at all.',
               'The answer chosen costs more than {N} expected, and {partner} says so.']),
 'options': [
    ('play it for the company: lead by example, and see everyone through the run', 'W1', None, 0.45, '', {'identity': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'wear it for the players: lead by example, and see every one of them through the summer', 'magic': 'play it for the company: lead by example, and see every player through the season'}, 'chance': 0.78}),
    ('play it for the part: a voice coach all run, and new work every night', 'U1', None, 0.45, '', {'identity': True, 'binds': True, 'habit': True, 'v': 'achievement, self-direction', 'self_control': '+', 'world': {'tribal': 'wear it for the ancestor: sit with the old teller all summer, and find something new every night', 'magic': 'play it for the part: a master of voice for the season, and new work every night'}, 'chance': 0.72}),
    ('play it for the career: use the run to land the next and bigger part', 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'world': {'tribal': 'wear it for your name: use the summer to be asked for by every band', 'magic': 'play it for your name: use the season to win a place at the court playhouse'}, 'chance': 0.72}),
    ('play it for the house: give everything every night, as if it were the last', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation, hedonism', 'self_control': '+', 'world': {'tribal': 'wear it for the band: give everything every night, as if it were the last'}, 'chance': 0.78}),
    ('play it for the people at home, and go back to them between every job', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'wear it for your own hearth, and go back to them between every gathering', 'magic': 'play it for your own people, and go home to them between every season'}, 'chance': 0.72}),
    ('promise the director to keep the show exactly as it opened, every night of the run', 'W1', 'U.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'conformity, achievement', 'mark': 'kept your word', 'world': {'tribal': 'swear to the shaper to keep the telling exactly as it was first told, every night', 'magic': 'swear to the master of the play to keep the show exactly as it opened, every night'}, 'chance': 0.62}),
    ('study the leads whose careers you want, and plan five years like a campaign', 'U1', 'B.7', 0.5, '', {'identity': True, 'v': 'achievement, power', 'world': {'tribal': 'study the great wearers of the mask, and plan your next five summers like a hunt', 'magic': 'study the great leading players of the realm, and plan five seasons like a campaign'}, 'chance': 0.65}),
    ('sign with the big agency, and say yes to fame: the interviews, the parties, the cameras', 'B1', 'R.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'hedonism, power', 'world': {'tribal': 'let the go-between carry your name to every band, and take every feast and gift that comes', 'magic': 'sign with the grandest broker, and take every supper, every portrait and every crowd'}, 'chance': 0.7}),
    ('go out to the stage door every night of the run, for everyone who waited', 'R1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'go out among the families every night after the telling, for everyone who waited', 'magic': 'go out to the playhouse door every night, for everyone who waited'}, 'chance': 0.8}),
    ("keep the company's old customs: the warm-up circle, the half-hour toast, the last-night gift", 'G1', 'W.7', 0.5, '', {'identity': True, 'v': 'tradition, conformity', 'world': {'tribal': "keep the tellers' old ways: the circle before the fire, the gift to the ancestor, the last song", 'magic': "keep the company's old customs: the circle, the toast at the bell, the last-night gift"}, 'chance': 0.95}),
 ]},
{'name': 'the last night of the run',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, family, friends',
 'horizon': 'months',
 'roles': 'partner, colleague',
 'requires': 'lead actor or actress',
 'threshold': 'title:lead actor or actress',
 'step': 3,
 'worlds': {'earth': 'five months in, the last night of the run or the last day of filming: the flowers, the speech, '
                     'the empty dressing room, and a diary with nothing in it',
            'tribal': 'at the end of the summer gathering, the last telling: the great mask lifted from your face '
                      'and hung back on its peg',
            'magic': 'at the end of the season, the last night: the herald cries your name one more time, and the '
                     'wagons are already packed'},
 'timing': {'times': 'per new lead: once, about five months in, near the end of the run or of the threshold season; '
                     'about 1 life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of lead actor or actress, within the first six months after taking '
                         'the part: step 3, near the end of the six months, when the run or the series ends',
             'likelier': 'a fixed run of a few months; a series that finishes filming; a lead with nothing booked '
                         'next',
             'rarer': 'an open-ended run; a series renewed at once; a lead who goes straight into the next part'},
 'scenes': {'earth': [('',
                       'Five months in, the last night. The house stands at the curtain call, the company gives {N} '
                       'flowers and a card everyone has signed, and the set comes down overnight. The next morning '
                       'there is no call, no car, no half-hour, and a diary with nothing in it. {partner} has '
                       'planned a week away. {N} is not sure who {N} is without the part.'),
                      ('W',
                       '{N} wants to end it properly: a speech for the crew, a card for every dresser, the dressing '
                       'room left clean.'),
                      ('U', '{N} can feel what the part taught, and wants to write it down before it goes.'),
                      ('B',
                       'The run is over, but the name is bigger than it was. {N} has three meetings next week and '
                       'means to make them count.'),
                      ('R',
                       '{N} wants the last night to last forever: the party, the dawn, the company one more time.'),
                      ('G',
                       '{N} feels the season turning. A run ends as a summer ends, and something else will grow.')],
            'tribal': [('',
                        'At the end of the summer gathering the great mask is lifted from {Ns} face for the last '
                        'time and hung back on its peg, and the band turns back to the hunt.')],
            'magic': [('',
                       "On the last night the herald cries {Ns} name one more time, the patron's flowers wilt in the "
                       'dressing room, and the wagons are already packed for the road.')]},
 'outcomes': (['The last night ends well, and {N} walks out of the stage door into the morning with the part folded '
               'away like a good coat.',
               '{partner} and {N} have the week away, and by the third day {N} sleeps through the night.'],
              ['The morning after, the empty diary feels like a fall, and {N} spends the week waiting for the phone.',
               'The last night goes on too long, and something said at the party follows {N} into the next job.']),
 'options': [
    ('thank every member of the crew by name, from the stage', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'thank every player and every keeper of the fire by name at the last fire', 'magic': 'thank every stagehand and player by name from the stage'}, 'chance': 0.92}),
    ('write down every lesson of the part before it fades', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': 'go over every lesson of the mask by the fire before it fades', 'magic': 'write every lesson of the part in your book before it fades'}, 'chance': 0.94}),
    ('line up the next three meetings before the set comes down', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'send a go-between to every band before the camp breaks, to ask for your telling', 'magic': 'arrange meetings with three masters of the play before the wagons roll'}, 'chance': 0.9}),
    ('party with the company until dawn, and say goodbye to the part properly', 'R1', None, 0.45, '', {'v': 'hedonism', 'world': {'tribal': 'dance with the players at the last fire until dawn', 'magic': 'feast with the company until dawn in the empty playhouse'}, 'chance': 0.9}),
    ('take the week away with your partner, and let the part go', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'go back to your own hearth with your partner, and let the mask go', 'magic': 'go to the sea with your partner for a week, and let the part go'}, 'chance': 0.8}),
    ('thank the director and producers in writing, and offer to work with them again', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'take a gift to the shaper and to the elder who gathered the hides, and offer to tell for them again', 'magic': 'write to the master of the play and the patron with thanks, and offer to play for them again'}, 'chance': 0.8}),
    ('travel somewhere new for a month, to see how others make theatre', 'U1', 'R.7', 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'walk alone to the far valleys for a moon, to see how other bands tell', 'magic': 'travel to a city you have never seen, to see how its players work'}, 'chance': 0.7}),
    ("save most of the run's money for the lean months that always follow", 'B1', 'G.7', 0.5, '', {'v': 'security', 'self_control': '+', 'world': {'tribal': "lay by the summer's gifts for the lean moons that always follow", 'magic': "put the season's wages by for the lean months that always follow"}, 'chance': 0.8}),
    ('tell the truth in the last-night speech: what was hard, and who held the show up', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'tell the band at the last fire what was hard, and who held the telling up', 'magic': 'tell the company in the last-night speech what was hard, and who held the show up'}, 'chance': 0.82}),
    ('go back to your old drama teacher, and talk the whole run through', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'go back to the old teller who taught you, and tell the whole summer through', 'magic': 'go back to the old master who taught you, and talk the whole season through'}, 'chance': 0.85}),
 ]},
{'name': 'the first day of rehearsals',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'director',
 'threshold': 'title:director',
 'step': 1,
 'worlds': {'earth': 'the first day of rehearsals: a rehearsal room, a model box of the set, and a cast waiting to '
                     'hear what you think the play is about',
            'tribal': 'the first fire of the first telling you shape, with the whole band gathered and the players '
                      'waiting for your first word',
            'magic': 'the first day with the first company you direct, in a playhouse that has seen a hundred '
                     'masters of the play'},
 'timing': {'times': 'per new director: once, in the first weeks after taking the title; about 1 life in 1,000 '
                     '(catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of director, within the first six months after taking the title '
                         "(opened by 'a director is needed for the autumn play' or any other way in): step 1, the "
                         'first day of rehearsals of the first production',
             'likelier': 'a first paid production; a cast of experienced actors; an actor, a stage manager or a '
                         'teacher who has crossed over to directing',
             'rarer': 'a director who has already run many amateur productions; a first film with no rehearsals at '
                      'all'},
 'scenes': {'earth': [('',
                       'The first day of rehearsals: a room above a pub, a model box of the set on a trestle table, '
                       'coffee in paper cups and a cast of eight waiting to hear what {N} thinks the play is about. '
                       '{N} has rewritten the opening talk four times. {boss}, the producer, sits at the back with a '
                       'notebook.'),
                      ('W',
                       '{N} has drawn up the rehearsal schedule to the quarter hour, with the breaks where the '
                       "actors' union says they should be."),
                      ('U',
                       '{N} has read the play forty times and has a reading of it that fits on one page, and a '
                       'second page of doubts.'),
                      ('B',
                       'This production is the calling card. The producer in the corner is deciding whether there '
                       'will be a second one.'),
                      ('R',
                       '{N} cannot wait to get the actors on their feet. The talk can wait; the play is in their '
                       'bodies, not on the page.'),
                      ('G',
                       '{N} thinks of the directors who taught by example, and of the old rehearsal rooms where {N} '
                       'first sat at the side and watched.')],
            'tribal': [('',
                        'At the first fire of the new telling the band gathers to see what {N} will make of the old '
                        'story, and the players wait for {Ns} first word.')],
            'magic': [('',
                       'In a playhouse that has seen a hundred masters of the play, the company waits on its benches '
                       'for {Ns} first word, and the carved faces on the walls seem to wait too.')]},
 'outcomes': (['By the end of the first day the cast is on its feet, the play has started to breathe, and {boss} '
               'closes the notebook and smiles.',
               'An actor stops {N} on the stairs to say it has been years since a first day felt like this.'],
              ["The opening talk runs long, the cast's eyes glaze over, and the day ends with nobody quite sure what "
               'play they are in.',
               '{N} says something on the first day that the cast repeats in the pub that night, and not kindly.']),
 'options': [
    ('set the schedule and the rules of the room, and keep them from the start', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'set out how the telling will be made and the customs of the fire, and keep them', 'magic': 'set the schedule and the rules of the company, and keep them from the first bell'}, 'chance': 0.9}),
    ('give the cast your one-page reading of the play, and ask them to argue with it', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': 'tell the players what you think the story means, and ask them to argue with it'}, 'chance': 0.84}),
    ('make sure the producer sees the cast laughing and working by lunchtime', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'make sure the elders see the players laughing and working by midday', 'magic': "make sure the patron's man sees the company laughing and working by noon"}, 'chance': 0.82}),
    ('skip the talk, and get the actors on their feet in the first ten minutes', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'skip the speeches, and have the players moving in the firelight at once'}, 'chance': 0.92}),
    ('open with a circle where everyone says why they came to this play', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'open with the old circle, everyone saying which of their ancestors loved this story', 'magic': 'open with a circle where each player says why they came to this play'}, 'chance': 0.9}),
    ('take the whole company, crew included, to see the place where the play is set', 'W1', 'G.7', 0.5, '', {'door': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'walk the whole band of players to the place where the story happened', 'magic': 'walk the whole company to the old quarter where the play is set'}, 'chance': 0.62}),
    ('go through the text line by line around the table for the whole first week', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'self_control': '+', 'world': {'tribal': 'go through the telling word by word at the fire for the first moon', 'magic': 'go through the text line by line at the table for the whole first week'}, 'chance': 0.82}),
    ('spend half the spare budget on the best movement coach in the city', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'give half the spare hides to the best dancer of the valley, to teach the players', 'magic': 'spend half the spare purse on the best master of movement in the city'}, 'chance': 0.85}),
    ('announce on day one that this production will do what nobody has dared with the play', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'mark': 'took a wild risk', 'world': {'tribal': 'declare at the first fire that this telling will do what no shaper has dared', 'magic': 'declare on the first day that this staging will do what no master has dared'}, 'chance': 0.55}),
    ('start each day with the old games your first company played, and let the room laugh', 'G1', 'R.7', 0.5, '', {'habit': True, 'v': 'tradition, hedonism', 'world': {'tribal': 'start each day with the old games the children of your band play, and let the players laugh', 'magic': 'start each day with the old games of your first pageant players, and let the room laugh'}, 'chance': 0.9}),
 ]},
{'name': 'the designer who wants a different show',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss',
 'requires': 'director',
 'threshold': 'title:director',
 'step': 2,
 'worlds': {'earth': "ten weeks in, the designer's final model shows a different show from the one you are making, "
                     'and the workshop starts building on Monday',
            'tribal': 'two moons in, the maker of the masks and screens has made them for a different telling from '
                      'the one you are shaping',
            'magic': "ten weeks in, the playhouse's illusionist has woven a glamour for a different play from the "
                     'one you are staging'},
 'timing': {'times': 'per new director: once, in the first months of the threshold season, about ten weeks in; about '
                     '1 life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of director, within the first six months after taking the title: '
                         'step 2, some weeks in, when the design and the staging pull apart',
             'likelier': 'a designer older and better known than the director; a producer who loves the design; '
                         'little money for changes',
             'rarer': 'a director who designs their own shows; a bare-stage production with no set to speak of'},
 'scenes': {'earth': [('',
                       'Ten weeks in, {colleague}, the designer, unveils the final model box, and it is beautiful, '
                       'and it is a different show: a bare, empty room where {N} imagined a crowded kitchen. The '
                       'workshop starts building on Monday. The designer is older, admired and sure, and {boss} '
                       'loves the model and says it will photograph well.'),
                      ('W',
                       'There was an agreement: the first design meeting, the brief, the drawings everyone signed. '
                       '{N} wants to know what happened to it.'),
                      ('U',
                       '{N} studies the model for an hour and has to admit it is interesting. The question is '
                       'whether it serves the play.'),
                      ('B',
                       'Whoever wins this argument runs the production, and {N} knows the whole team is watching.'),
                      ('R',
                       '{N} hates it on sight, and has to sit on both hands not to say so in front of everyone.'),
                      ('G',
                       '{N} thinks of the play as written: a family, a kitchen, a table they have eaten at for '
                       'thirty years. The empty room has no roots.')],
            'tribal': [('',
                        'The maker of masks and screens has painted them for a different telling: no forest and no '
                        'river, only a bare wall of hide where {N} wanted the hunt.')],
            'magic': [('',
                       "The playhouse's illusionist has woven a glamour for a different play: a palace of light "
                       'where {N} wanted a smoky inn.')]},
 'outcomes': (['Director and designer find a show they can both believe in, and the workshop builds it.',
               'The cast walks into the finished set for the first time and goes quiet, in the good way.'],
              ['The design goes ahead as it was, and {N} spends the rest of rehearsals directing around it.',
               'The quarrel spreads to the whole team, and the production starts to split into sides.']),
 'options': [
    ("accept the producer's ruling on the design, though it is not your show", 'W1', None, 0.45, '', {'v': 'conformity', 'mark': 'gave in to pressure', 'self_control': '-', 'world': {'tribal': "accept the elders' word on the masks, though it is not your telling", 'magic': "accept the play-merchant's ruling on the glamour, though it is not your play"}, 'chance': 0.88}),
    ('spend a day in the room testing both versions with the actors', 'U1', None, 0.45, '', {'door': True, 'v': 'achievement, universalism', 'world': {'tribal': 'try both tellings at the fire with the players for a day', 'magic': 'try both stagings with the company for a day, the glamour and the plain'}, 'chance': 0.75}),
    ('go to the producer first, and get the final say on design put in your hands', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'go first to the elder who gathered the hides, and get the last word put in your hands', 'magic': 'go first to the play-merchant, and get the last word put in your hands'}, 'chance': 0.62}),
    ('tell the designer straight out, in front of everyone, that it is the wrong show', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'mark': 'made an enemy', 'world': {'tribal': 'tell the maker straight out at the fire that it is the wrong telling', 'magic': 'tell the illusionist before the whole company that it is the wrong play'}, 'chance': 0.4}),
    ('wait a week before anyone decides, and sleep on it', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'wait a moon before anyone decides, and let the fire settle it'}, 'chance': 0.55}),
    ('go through the play scene by scene against the drawings everyone signed', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'go through the telling part by part against what was agreed at the fire', 'magic': 'go through the play scene by scene against the drawings everyone sealed'}, 'chance': 0.7}),
    ('find the one change that makes the design serve your staging, and trade for it', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'find the one change that would serve your telling, and bargain the maker into it', 'magic': 'find the one change that would serve your staging, and bargain the illusionist into it'}, 'chance': 0.65}),
    ('wait for the technical rehearsal, and quietly cut whatever you dislike then', 'B1', 'R.7', 0.5, '', {'v': 'power, self-direction', 'world': {'tribal': 'wait for the last practice at the fire, and quietly leave out whatever you dislike then', 'magic': 'wait for the last rehearsal with the glamour, and quietly cut whatever you dislike then'}, 'chance': 0.75}),
    ("take the designer to the pub, and talk about your own family's kitchen", 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'made a friend', 'world': {'tribal': "sit with the maker by the river, and talk of your own family's fire", 'magic': "take the illusionist to the tavern, and talk of your own family's kitchen"}, 'chance': 0.66}),
    ('ask the old head of the workshop how such quarrels were settled here before', 'G1', 'W.7', 0.5, '', {'door': True, 'v': 'tradition, conformity', 'world': {'tribal': 'ask the oldest keeper of the masks how such quarrels were settled before', 'magic': "ask the playhouse's oldest stage-wright how such quarrels were settled before"}, 'chance': 0.75}),
 ]},
{'name': 'the show you want to make',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'mentor, boss',
 'requires': 'director',
 'threshold': 'title:director',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'four months in, a producer asks over lunch what kind of work you want to make, and the answer '
                     'will shape every room you run',
            'tribal': 'four moons in, the elders ask what tellings you will shape now, and the next summer will '
                      'follow your answer',
            'magic': 'four months in, a patron asks over supper what plays you mean to make, and his purse waits on '
                     'the answer'},
 'timing': {'times': 'per new director: once in the threshold season, about four months in, for most who are still '
                     'open to change; about 1 life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of director, within the first six months after taking the title: '
                         "step 2, the season's transforming chance, when the next production is offered and the "
                         'director must say what work they make',
             'likelier': 'a first production that went well; a producer or a theatre that asks what comes next; a '
                         'director with actors around them already',
             'rarer': 'a director with nothing offered; a director hired for one show only'},
 'scenes': {'earth': [('',
                       'Four months in, {boss}, a producer, has asked {N} to lunch to talk about the next '
                       'production, and over coffee the question comes: what kind of work does {N} want to make? '
                       '{mentor}, the old director who gave {N} a first chance, once said that every director makes '
                       'one show over and over all their life. {N} would like to choose which.'),
                      ('W',
                       '{N} thinks of the rehearsal room as a small society: fair hours, clear rules, everyone '
                       'heard. A good room makes good work.'),
                      ('U',
                       '{N} thinks of the great plays nobody has truly understood yet, and wants to spend a life '
                       'inside them.'),
                      ('B',
                       '{N} thinks of the directors whose names sell tickets, and of the bigger stages that come '
                       'with a name.'),
                      ('R',
                       '{N} wants to make shows that frighten people, that set rooms alight, that nobody forgets.'),
                      ('G',
                       '{N} thinks of the actors from the first show, already like a family, and of a town that '
                       'could have its own company for years.')],
            'tribal': [('',
                        'Four moons in, the elders ask {N} at the fire what tellings {N} will shape now. The next '
                        'summer will follow the answer.')],
            'magic': [('',
                       'Four months in, a patron leans across the supper table and asks what plays {N} means to '
                       'make, and his purse waits on the answer.')]},
 'outcomes': (['The answer holds, and within the year the next production looks like the work {N} chose.',
               '{mentor} sees the next show and sends {N} a short note: yes, that one.'],
              ["{N} says yes to everything offered, and the next year's work looks like nobody's in particular.",
               'The choice is made, and the first producer who hears it says politely that there is no money for '
               'that.']),
 'options': [
    ('run fair, ordered rooms where everyone is heard, whatever the play', 'W1', None, 0.45, '', {'identity': True, 'v': 'universalism, conformity', 'world': {'tribal': "shape every telling by the fire's customs, where every player is heard", 'magic': 'run fair, ordered companies where every player is heard, whatever the play'}, 'chance': 0.8}),
    ('serve the great plays: read each one until it gives up its meaning, and stage that', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, universalism', 'world': {'tribal': 'serve the oldest tellings: listen to each until it gives up its meaning, and shape that', 'magic': 'serve the great plays of the realm: read each until it gives up its meaning'}, 'chance': 0.72}),
    ('build a name: take every bigger stage offered, and make the shows people talk about', 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'world': {'tribal': 'build a name: take every greater fire offered, and shape the tellings every band talks about', 'magic': 'build a name: take every greater playhouse offered, and make the plays the court talks about'}, 'chance': 0.62}),
    ('make raw, dangerous shows, and never play it safe', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation, self-direction', 'mark': 'took a wild risk', 'world': {'tribal': 'shape wild, frightening tellings, and never tell it safe'}, 'chance': 0.72}),
    ('build a company of the same actors and designers, show after show', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'gather the same players around you, telling after telling', 'magic': 'gather a company of the same players and makers, play after play'}, 'chance': 0.65}),
    ('found a company with a written charter, fair pay and your name on the door', 'W1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, conformity', 'grants': 'a company of your own', 'world': {'tribal': 'gather players under customs you set, with fair shares and your name on the telling', 'magic': 'found a licensed company with a charter, fair wages and your name on the wagon'}, 'chance': 0.4}),
    ('commit to three years of new plays with young writers, and learn by failing', 'U1', 'R.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'promise three summers of new tellings with the young makers, and learn by failing', 'magic': 'promise three seasons of new plays with young play-makers, and learn by failing'}, 'chance': 0.6}),
    ('sign on as the regular director of one small theatre, a show there every year', 'B1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, tradition', 'world': {'tribal': "become one band's shaper of tellings for good, and make the tellings yours", 'magic': 'sign on as the regular master of the play at one small town playhouse'}, 'chance': 0.58}),
    ('direct only plays that say what is wrong in the world, and say it loud', 'R1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, stimulation', 'world': {'tribal': 'shape only tellings that say what is wrong in the band, and say it loud', 'magic': 'stage only plays that say what is wrong in the realm, and say it loud'}, 'chance': 0.78}),
    ('go back to the folk plays of your region, and learn to stage them anew', 'G1', 'U.7', 0.5, '', {'identity': True, 'v': 'tradition, achievement', 'world': {'tribal': 'go back to the oldest tellings of your own band, and learn to shape them anew', 'magic': 'go back to the old mystery plays of your region, and learn to stage them anew'}, 'chance': 0.72}),
 ]},
{'name': 'press night',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, public life, family',
 'horizon': 'months',
 'roles': 'partner, boss, colleague',
 'requires': 'director',
 'threshold': 'title:director',
 'step': 3,
 'worlds': {'earth': 'five months in, press night: critics in the third row, the producer pacing at the back, the '
                     'cast in your hands, and your partner in the seat you saved',
            'tribal': 'five moons in, the first great telling you have shaped, with the elders of every band at the '
                      'fire to judge it',
            'magic': 'five months in, opening night before the city: the patron in his box, and the broadsheet men '
                     'in the pit'},
 'timing': {'times': 'per new director: once, about five months in, near the end of the threshold season; about 1 '
                     'life in 1,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of director, within the first six months after taking the title: '
                         'step 3, near the end of the six months, on the press night of the first production',
             'likelier': 'a professional production that critics review; a partner or family who come; a producer '
                         'who must decide on the next show',
             'rarer': 'an amateur or touring production no critic sees; a show that opened quietly'},
 'scenes': {'earth': [('',
                       'Press night. The critics are in, the producer paces at the back of the stalls, and the cast '
                       "are in their dressing rooms with {Ns} cards on their mirrors. A director's work is done "
                       'before the curtain goes up, and that is the hard part: {N} can only watch. {partner} sits in '
                       'the seat {N} saved, holding {Ns} hand too tightly.'),
                      ('W',
                       '{N} has done everything properly: the notes given, the cards written, the crew thanked. Now '
                       'the show belongs to the actors.'),
                      ('U', '{N} watches the critics as much as the stage, trying to read what they see.'),
                      ('B',
                       "Tomorrow's notices decide the next job, and {N} has already planned what to say to the press "
                       'in the bar afterwards.'),
                      ('R',
                       '{N} cannot sit still, and watches the first act standing at the back, mouthing every line.'),
                      ('G',
                       '{N} thinks of the play as something that will live on without {N} now, like a child leaving '
                       'home.')],
            'tribal': [('',
                        'At the first great telling {N} has shaped, the elders of every band sit closest to the '
                        'fire, and {N} can only watch from the dark.')],
            'magic': [('',
                       'On opening night the patron leans out of his box, the broadsheet men fill the pit, and {N} '
                       'can only watch from the wings.')]},
 'outcomes': (['The notices are good, the cast is happy, and the producer rings at breakfast about a second show.',
               '{partner} says on the way home that it was the best night out they have ever had, and {N} believes '
               'it.'],
              ['One notice dismisses the show in a paragraph, and the cast reads it before {N} does.',
               'The night goes well and the papers do not, and {N} learns how little a director controls after the '
               'curtain goes up.']),
 'options': [
    ('leave it to the actors, and sit quietly in your seat through the whole show', 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '+', 'world': {'tribal': 'leave it to the players, and sit still at the edge of the firelight till the end', 'magic': 'leave it to the players, and sit quietly in your box through the whole play'}, 'chance': 0.75}),
    ('watch from the back and write notes for tomorrow, whatever the papers say', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'watch from the dark and remember every fault, to tell the players tomorrow', 'magic': 'watch from the back and write notes for tomorrow, whatever the broadsheets say'}, 'chance': 0.9}),
    ("take the credit for the designer's best idea in the interviews afterwards", 'B1', None, 0.45, '', {'v': 'power, achievement', 'mark': 'hid a wrong', 'closed': "approval: claiming a colleague's idea as one's own; backfire: the designer reads the interview, and the theatre world hears of it", 'world': {'tribal': "tell the elders afterwards that the maker's best idea was yours", 'magic': "tell the broadsheet men that the illusionist's best idea was yours"}, 'chance': 0.9}),
    ('watch standing at the back, mouthing every line, and hug every actor at the interval', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'stand in the dark mouthing every word, and embrace every player when the telling breaks', 'magic': 'watch from the wings mouthing every line, and embrace every player at the interval'}, 'chance': 0.95}),
    ('sit with your partner and family, and let the night be theirs too', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'sit with your own kin at the fire, and let the night be theirs too', 'magic': 'sit with your household in the gallery, and let the night be theirs too'}, 'chance': 0.92}),
    ('give a speech at the party thanking every last person, and then dance', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, hedonism', 'world': {'tribal': 'thank every player and helper at the feast, and then dance'}, 'chance': 0.92}),
    ('read the notices with the cast the next morning, and talk them through together', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': "hear the elders' judgment with the players at dawn, and talk it through together", 'magic': 'read the broadsheets with the company the next morning, and talk them through together'}, 'chance': 0.7}),
    ('introduce every actor to the producers and casting directors at the party', 'B1', 'W.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'bring every player before the elders of the other bands at the feast', 'magic': 'present every player to the patrons and brokers at the supper'}, 'chance': 0.8}),
    ('slip out at the interval, walk round the block, and come back with fresh eyes', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'slip away from the fire at the break, walk to the river and back, and watch it fresh', 'magic': 'slip out of the playhouse at the interval, walk round the square, and watch it fresh'}, 'chance': 0.9}),
    ('take the producer home to dinner with your family, and talk about the next show there', 'G1', 'B.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': "bring the elder who gathered the hides to your own kin's fire, and talk of the next telling there", 'magic': 'bring the patron to supper with your household, and talk of the next play there'}, 'chance': 0.55}),
 ]},
{'name': 'the old teller dies at midwinter',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.01, 0.02, 0.02, 0.02, 0.03),
 'drivers': 'harsh+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, meaning',
 'horizon': 'months',
 'roles': 'elder, mentor, rival, friend, child',
 'requires': 'amateur actor | drama school student',
 'tenure': (2.0, 100.0),
 'worlds': {'tribal': 'the old teller dies in the long nights, and the fire is silent where the stories were'},
 'only': 'tribal',
 'timing': {'times': "per player of the band of two winters or more (an amateur actor, or an old teller's "
                     "apprentice) in the tribal world a year: about 1 in 50, when a band's teller dies or grows too "
                     'old (estimate)',
            'likelier': 'a hard winter, an old teller who never named an apprentice, a player who sat at the old '
                        "one's side",
            'rarer': 'a band with several tellers, a young teller already in place, a player who keeps to the edge '
                     'of the firelight',
            'gap_years': (5.0, 10.0)},
 'scenes': {'tribal': [('',
                        'The old teller dies in the deepest of the long nights, and the band lays her masks beside '
                        'her. Since then the fire has been silent where the stories were, and every evening the '
                        'children ask who will tell them now.'),
                       ('W',
                        "{N} sat at the old one's side for years and knows how each telling must go, word for word "
                        'and night by night. Someone has to keep them as they were given.'),
                       ('U',
                        '{N} has heard every story told a dozen ways. The old teller changed them a little each '
                        'winter, and {N} wants to know which parts were the bones and which the skin.'),
                       ('B',
                        "Whoever takes the teller's place will sit near the elders and be fed first after the hunt. "
                        'Across the fire, {rival} is plainly thinking the same.'),
                       ('R',
                        'The silence at the fire is more than {N} can stand. Ready or not, {N} wants to get up in '
                        'the firelight and fill it.'),
                       ('G',
                        "The stories belong to the band, not to any one voice. {N} thinks of the old teller's hands, "
                        'and of the little ones who have never heard the winter tellings to the end.')]},
 'outcomes': (['By the next new moon the fire has its stories again, and the band settles close to listen.',
               'The elders nod over how it was settled, and the children fall asleep to the old tellings once more.'],
              ['The band cannot agree, and for the rest of the winter the fire stays half silent.',
               '{rival} speaks first and loudest, and the elders give the stories to another voice.']),
 'options': [
    ('keep every telling exactly as the old teller gave it, night after night', 'W1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'tradition, conformity', 'chance': 0.05}),
    ('piece the tellings together from what every old one remembers, and tell them whole', 'U1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'self-direction, universalism', 'chance': 0.05}),
    ("ask the elders for the teller's place, and the teller's share of every hunt", 'B1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'chance': 0.05}),
    ('stand up at the silent fire the first night, and tell the bear story by heart', 'R1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'aims': 'professional actor', 'v': 'stimulation, self-direction', 'chance': 0.05}),
    ('keep the stories alive through the winter, until a younger voice is ready', 'G1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'identity': True, 'v': 'benevolence, tradition', 'chance': 0.05}),
    ('ask the elders for a night of trials, and tell a piece of your own there', 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'telling a story aloud', 'door': True, 'v': 'universalism, stimulation', 'chance': 0.7}),
    ("stand aside, and ask the band to give the place to the old one's apprentice", 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'self_control': '+', 'v': 'benevolence, tradition', 'chance': 0.7}),
    ("teach the band's children the tellings, as the old ones always have", 'W.34 B.33 G.33', None, 0.5, '', {'title': 'drama teacher', 'requires': 'telling a story aloud', 'without': 'approval', 'lacking': 0.5, 'v': 'tradition, benevolence', 'chance': 0.7}),
    ('make new tellings of your own, and play them at the summer gathering', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'writing scripts', 'identity': True, 'v': 'self-direction, achievement', 'chance': 0.7}),
    ('ask the shaman quietly whom the old teller meant to follow her', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'tradition, security', 'chance': 0.7}),
 ]},
{'name': 'the spirits ride the dancer',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.01),
 'drivers': 'harsh+.3',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, meaning',
 'horizon': 'months',
 'roles': 'elder, friend, rival',
 'requires': 'professional actor | lead actor or actress | amateur actor',
 'worlds': {'tribal': 'in the deepest telling the fire roars, you speak in a voice that is not yours, and the band '
                      'draws back'},
 'only': 'tribal',
 'timing': {'times': 'per player in the tribal world a year: about 1 in 100 (estimate)',
            'likelier': 'a long fast before the telling, a hard season that makes the band fearful, a player who '
                        'gives everything to the deep tellings',
            'rarer': 'a shaman who knows the player well, light tellings for the children, a player who keeps a '
                     'little back',
            'gap_years': (5.0, 10.0)},
 'scenes': {'tribal': [('',
                        'In the deepest telling of the winter the fire roars up, and {N} speaks in a voice nobody '
                        'knows, old and slow, for as long as it takes a log to burn through. When it ends the band '
                        'has drawn back from the light, and the shaman cannot say what it was.'),
                       ('W',
                        'There is a rite for everything that comes out of the dark. {N} wants this put right the '
                        "proper way, before the band's fear hardens into something worse."),
                       ('U',
                        '{N} remembers almost nothing, only heat and a long fall. A fast, the smoke, three nights '
                        'without sleep: there may be plain reasons, and {N} wants to find them.'),
                       ('B',
                        'Since that night the young ones look at {N} with awe, and even the elders lower their eyes. '
                        'Fear is a kind of power, and {N} can feel it.'),
                       ('R',
                        'Whatever happened at the fire, {N} has never felt so alive. Part of {N} wants to go back '
                        'into it, whatever the band says.'),
                       ('G',
                        "The band's peace matters more than any telling. {N} sees the mothers pulling the children "
                        'close, and {friend} keeping to the far side of the fire.')]},
 'outcomes': (["By the spring the band's fear has eased, and {N} is welcome at the fire again.",
               'The elders settle it among themselves, and the talk of that night turns from fear to wonder.'],
              ['The fear does not ease, and families move their sleeping hides further from {Ns} fire.',
               '{rival} keeps the whispering alive all winter, and the elders begin to look the other way.']),
 'options': [
    ("go through the shaman's cleansing rite, and fast as long as he says", 'W1', None, 0.45, '', {'self_control': '+', 'v': 'tradition, conformity', 'chance': 0.67}),
    ('tell the band plainly that it was the fast and the smoke, nothing more', 'U1', None, 0.45, '', {'identity': True, 'v': 'self-direction, universalism', 'chance': 0.6}),
    ('let the band believe the first ancestor spoke, and take the seat nearest the fire', 'B1', None, 0.45, '', {'closed': "approval: claiming the ancestor's voice; backfire: the shaman says no ancestor spoke, and the band turns away", 'self_control': '-', 'v': 'power', 'chance': 0.65}),
    ('go back into the trance at the next telling, and let it take hold', 'R1', None, 0.45, '', {'mark': 'took a wild risk', 'closed': 'approval: a trance the shaman has forbidden; backfire: the band casts the player out for a season', 'v': 'stimulation, hedonism', 'chance': 0.67}),
    ('step back from the great tellings, and dance only in the herd for a year', 'G1', None, 0.45, '', {'drops': 'lead actor or actress', 'v': 'security, tradition', 'chance': 0.6}),
    ('sit with the shaman and the oldest dancers until they agree on what it was', 'W.34 U.33 G.33', None, 0.5, '', {'door': True, 'v': 'tradition, universalism', 'chance': 0.65}),
    ('dance the deep tellings only with the shaman beside the fire, by his rule', 'W.34 U.33 B.33', None, 0.5, '', {'binds': True, 'v': 'conformity, security', 'chance': 0.7}),
    ("wear the great mask at the gathering, and let the trance into the ancestor's dance", 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'good notices', 'requires': 'lead actor or actress', 'without': 'impossible', 'mark': 'took a wild risk', 'v': 'achievement, stimulation', 'chance': 0.45}),
    ('go alone into the hills for three days, and come back knowing what it was', 'U.34 R.33 G.33', None, 0.5, '', {'body': 'heavy', 'identity': True, 'v': 'self-direction, universalism', 'chance': 0.65}),
    ('take the family to another band, where nobody saw that night', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'left home', 'moves': True, 'v': 'security, self-direction', 'chance': 0.7}),
 ]},
{'name': 'chosen to wear the great mask',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.02, 0.03, 0.03, 0.02),
 'drivers': 'community+.3',
 'tier': 'life event',
 'tone': 'hope',
 'life': 'work, community, meaning',
 'horizon': 'months',
 'roles': 'elder, rival, friend, mentor',
 'requires': 'professional actor | voice actor | understudy | amateur actor',
 'worlds': {'tribal': "the elders hold up the great mask at the gathering's first fire, and turn to you"},
 'only': 'tribal',
 'timing': {'times': 'per teller-player of the band of two winters or more, or amateur player of five winters with a '
                     'lead behind them, in the tribal world a year: about 1 in 40; one player a summer wears the '
                     'great mask for each gathering (estimate)',
            'likelier': 'a player the elders have watched for years, a gathering after a good winter, an old '
                        'mask-wearer grown too stiff to dance',
            'rarer': 'a band whose mask-wearer is still in his prime, a player new to the band, a quarrel with the '
                     'elders',
            'gap_years': (3.0, 8.0)},
 'scenes': {'tribal': [('',
                        'At the first fire of the summer gathering the elders hold up the great mask of the first '
                        "ancestor, and the band's eldest calls out {Ns} name. Every band has put forward its best "
                        'dancer, and the elders of all the clans will choose one by the last night. The mask is old '
                        'and heavy, and they say it takes something from whoever wears it.'),
                       ('W',
                        'The great mask belongs to the first ancestor, not to any dancer. If {N} is to wear it, '
                        'every fast and every taboo that goes with it will be kept.'),
                       ('U',
                        '{N} has watched three wearers dance the first ancestor, each one differently. Which way is '
                        'the true one, and what does the mask really take?'),
                       ('B',
                        'Whoever wears the great mask is spoken of at every fire in the valley for a generation. {N} '
                        'means it to be {N}, and {rival} from the river band means it to be {rival}.'),
                       ('R',
                        '{Ns} heart pounds like the gathering drums. To dance the first ancestor before every clan '
                        'in the valley: nothing else could ever come close.'),
                       ('G',
                        '{N} thinks of the old wearers, the ones who wore it once and the ones it changed, and of '
                        'the band that called out {Ns} name with such pride.')]},
 'outcomes': (['By the last night of the gathering it has gone the way {N} hoped, and the whole band walks a little '
               'taller.',
               'The elders of the clans speak {Ns} name with respect, and the band talks of that summer for years.'],
              ['On the last night the elders of the clans turn to {rival}, and {N} watches from among the drummers.',
               'The summer goes wrong from the first dance, and the band walks home quieter than it came.']),
 'options': [
    ('accept by the old rite, and keep every fast and taboo of the mask', 'W1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'professional actor', 'without': 'approval', 'lacking': 0.3, 'v': 'tradition, conformity', 'chance': 0.15}),
    ('learn every telling the first ancestor appears in, before the last night', 'U1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'professional actor', 'without': 'approval', 'lacking': 0.3, 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.15}),
    ("accept, and ask the elders for the wearer's seat at the council fire too", 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'professional actor', 'without': 'approval', 'lacking': 0.3, 'aims': 'lead actor or actress', 'identity': True, 'v': 'power, achievement', 'chance': 0.15}),
    ('take the mask, whatever it takes from its wearer, and dance as nobody has', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'professional actor', 'without': 'approval', 'lacking': 0.3, 'mark': 'took a wild risk', 'binds': True, 'v': 'stimulation, self-direction', 'chance': 0.15}),
    ("accept for the band's sake, with the whole band drumming behind", 'G1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'requires': 'professional actor', 'without': 'approval', 'lacking': 0.3, 'v': 'benevolence, tradition', 'chance': 0.15}),
    ('ask the shaman, by the old custom, what the mask takes from its wearer', 'W.5 U.5', None, 0.5, '', {'v': 'tradition, conformity', 'chance': 0.7}),
    ('give the mask to the old dancer who has waited for it all his life', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'chance': 0.7}),
    ('turn the mask down, and make up a new telling of the first ancestor instead', 'U.5 R.5', None, 0.5, '', {'grants': 'improvisation', 'v': 'self-direction, stimulation', 'chance': 0.7}),
    ("ask the elders to give the mask to your own kin's best dancer instead", 'B.5 G.5', None, 0.5, '', {'v': 'security, benevolence', 'chance': 0.7}),
    ('turn the mask down, and win the outer fires with a telling of your own', 'B.5 R.5', None, 0.5, '', {'grants': 'a fringe slot', 'door': True, 'v': 'achievement, stimulation', 'chance': 0.7}),
 ]},
{'name': 'the mimic who mocks the chief',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.02, 0.02, 0.02, 0.01),
 'drivers': 'unrest+.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'elder, rival, friend',
 'requires': 'professional actor | amateur actor | lead actor or actress',
 'worlds': {'tribal': 'the whole band laughs at your mimic of the chief, and the chief rises and walks out of the '
                      'firelight'},
 'only': 'tribal',
 'timing': {'times': 'per player in the tribal world a year: about 1 in 50 (estimate)',
            'likelier': 'a chief who has made hard choices, a winter of short tempers, a player with a gift for '
                        'voices',
            'rarer': 'a well-loved chief, a band that keeps its tellings to the old stories, a player careful whom '
                     'the mimic touches',
            'gap_years': (5.0, 10.0)},
 'scenes': {'tribal': [('',
                        'In the midwinter telling {N} plays the greedy chief of the old story, and gives him the '
                        "real chief's walk, his cough and his way of eating first. The band roars with laughter. The "
                        'chief rises without a word and walks out of the firelight, and the laughter dies away.'),
                       ('W',
                        'The chief is the chief, and a telling is no place to shame him. {N} knows a line was '
                        'crossed, and that the band will be watching what comes next.'),
                       ('U',
                        'The old stories have always laughed at greedy chiefs; that is what they are for. {N} '
                        'wonders how this chief could be brought to see it that way.'),
                       ('B',
                        'Half the band laughed until they cried, and some of them looked at {N} afterwards in a new '
                        'way. A chief who cannot take a joke is a chief who can be weakened.'),
                       ('R',
                        '{N} is still burning from the roar of the laughter. It was the best night at the fire in '
                        'years, and every word of it was true.'),
                       ('G',
                        "The band's peace has been broken, and {N} broke it. {N} thinks of the families who must "
                        "live beside the chief's fire all winter.")]},
 'outcomes': (['By the thaw the anger has cooled, and things have settled the way {N} hoped.',
               'The band talks about that night for years, and in the end the stories remember {N} kindly.'],
              ["The chief's anger does not cool, and {N} finds fewer places kept at the fire.",
               "{rival} carries every word to the chief's fire, and the winter grows long and cold for {N}."]),
 'options': [
    ("go to the chief's fire at dawn, and ask his pardon before the elders", 'W1', None, 0.45, '', {'mark': 'owned up', 'v': 'conformity, tradition', 'chance': 0.65}),
    ("at the next telling, turn the mimic into a song in the chief's praise", 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'chance': 0.62}),
    ('count who laughed loudest, and gather them around your own fire', 'B1', None, 0.45, '', {'mark': 'made an enemy', 'v': 'power', 'chance': 0.62}),
    ('play the mimic again at the next fire, louder', 'R1', None, 0.45, '', {'mark': 'defied an authority', 'closed': 'approval: mocking the chief a second time; backfire: the chief bars the player from the fire for a season', 'v': 'stimulation, hedonism', 'chance': 0.65}),
    ("step back from the tellings, and keep away from the chief's fire for a season", 'G1', None, 0.45, '', {'drops': 'lead actor or actress', 'v': 'security, tradition', 'chance': 0.62}),
    ("walk with your own kin to the river band, where the chief's word does not reach", 'R.5 G.5', None, 0.5, '', {'mark': 'left home', 'moves': True, 'v': 'self-direction, tradition', 'chance': 0.65}),
    ('find out who carried the tale to the chief, and quietly settle the score', 'U.5 B.5', None, 0.5, '', {'v': 'power, security', 'chance': 0.65}),
    ('ask the oldest teller what the bands of old did when a chief was mocked', 'U.5 G.5', None, 0.5, '', {'door': True, 'v': 'universalism, tradition', 'chance': 0.65}),
    ('send the chief the best hide from your next hunt, with words of respect', 'W.5 B.5', None, 0.5, '', {'v': 'security, conformity', 'chance': 0.65}),
    ('tell the chief to his face that the fire has always laughed at chiefs', 'W.5 R.5', None, 0.5, '', {'mark': 'defied an authority', 'identity': True, 'v': 'self-direction, universalism', 'chance': 0.6}),
 ]},
{'name': 'the illusionist players come to town',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.005, 0.005, 0.005, 0.0025, 0.0025),
 'drivers': 'prosper+.3',
 'tier': 'life event',
 'tone': 'hope',
 'life': 'work, leisure',
 'horizon': 'week',
 'roles': 'friend, parent, elder',
 'worlds': {'magic': 'painted wagons in the square, and a dragon of light circling the town hall at dusk'},
 'only': 'magic',
 'timing': {'times': 'per person in the magic world a year: about 1 in 100 (estimate)',
            'likelier': 'a prosperous summer, a town on the high road between cities, a fair or a feast day',
            'rarer': 'hard years, a town off the roads, a strict Order that frowns on wagon players',
            'gap_years': (5.0, 10.0)},
 'scenes': {'magic': [('',
                       'The illusionist players roll into the square in six painted wagons, and by dusk a dragon of '
                       'light is circling the town hall while the children shriek below. The company master has '
                       'nailed a notice to the well: players, hands and walk-ons wanted for the week, and children '
                       "for the fairy scene, each with a parent's leave and a chaperone."),
                      ('W',
                       'The company has a licence from the Order, sealed and hung on the first wagon, and a list of '
                       'rules for everyone who travels with it. {N} reads every line of it twice.'),
                      ('U',
                       '{N} has never seen a glamour up close. How does a dragon hold its shape in the air, and who '
                       'decides where it flies?'),
                      ('B',
                       'The company master pays by the night, the notice says, and more for anyone who can carry a '
                       'part. {N} works out what a summer on the road might be worth.'),
                      ('R',
                       'The wagons, the lamps, the dragon: {N} has wanted something like this for years without '
                       'knowing it. The company leaves at the end of the week.'),
                      ('G',
                       'Half the town is in the square, {friend} among them, and the old folk say the illusionists '
                       "came once before, long ago, and played the town's own stories.")]},
 'outcomes': (['By the time the wagons roll on, the week has given {N} just what {N} hoped for.',
               'The company master remembers {Ns} name, and the dragon of light circles the town hall one last '
               'time.'],
              ['The company has all it needs by the second night, and {N} watches the rest of the week from the edge '
               'of the crowd.',
               'The week passes in a blur of rain and missed chances, and the wagons roll out at dawn without {N}.']),
 'options': [
    ("sign the company's articles, and keep every rule of the wagons", 'W1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'requires': 'amateur actor', 'without': 'impossible', 'v': 'conformity, security', 'chance': 0.05}),
    ('learn two of their plays by heart overnight, and show the company master at dawn', 'U1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'requires': 'amateur actor', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.05}),
    ("haggle for a player's share of the takings before signing on", 'B1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'requires': 'amateur actor', 'without': 'impossible', 'v': 'power, achievement', 'chance': 0.05}),
    ('sign on the spot, and leave with the wagons at the end of the week', 'R1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'requires': 'amateur actor', 'without': 'impossible', 'v': 'stimulation, self-direction', 'chance': 0.05}),
    ("join for the summer, and bring the town's old songs into their plays", 'G1', None, 0.45, '', {'title': 'professional actor', 'grants_if_fails': 'a long shot that missed', 'requires': 'amateur actor', 'without': 'impossible', 'aims': 'professional actor', 'v': 'tradition, benevolence', 'chance': 0.05}),
    ("ask the company to let the town's mystery players play a scene with them", 'W.34 U.33 R.33', None, 0.5, '', {'title': 'amateur actor', 'door': True, 'v': 'universalism, stimulation', 'chance': 0.75}),
    ('walk in the procession under the dragon each night, paid by the night', 'W.34 B.33 R.33', None, 0.5, '', {'title': 'background artist', 'v': 'stimulation, security', 'chance': 0.75}),
    ("sign on as chaperone for the town's children in the fairy scene", 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'cleared to work with children', 'v': 'benevolence, security', 'chance': 0.75}),
    ('take whatever small parts they need each night, and learn from the players', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'acting', 'habit': True, 'v': 'stimulation, self-direction', 'chance': 0.75}),
    ('watch from the crowd every night, and work out how a glamour holds its shape', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'self-direction, security', 'chance': 0.75}),
 ]},
{'name': 'the theatre where the dead come to watch',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.005, 0.005, 0.005, 0.005),
 'drivers': 'fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'dead, rival, friend, elder',
 'requires': 'professional actor | lead actor or actress',
 'tenure': (2.0, 100.0),
 'worlds': {'magic': 'the old playhouse on the night of the dead, and every seat in the gallery is taken by someone '
                     'long gone'},
 'only': 'magic',
 'timing': {'times': 'per working player (professional or lead) of two years or more in the magic world a year: '
                     'about 1 in 200 (estimate)',
            'likelier': 'a company that plays the old playhouses, a player the house master has watched, the turn of '
                        'the year toward the long nights',
            'rarer': 'a company that keeps to the new halls, a player new to the city, a year when the Order shuts '
                     'the old house',
            'gap_years': (10.0, 20.0)},
 'scenes': {'magic': [('',
                       'On the night of the dead the old playhouse opens its gallery, and every seat fills with '
                       'people long gone, pale and patient, in the clothes of their own times. The house master will '
                       'choose the lead for that one night from three players, and {N} is one of them. Whoever leads '
                       'it, the city says, is remembered by both worlds.'),
                      ('W',
                       "The Order's rules for the night are old and strict: a token for the dead at the stage door, "
                       'no names spoken from the stage, the lamps never fully out. {N} knows every one of them.'),
                      ('U',
                       'The house keeps a record of every night of the dead for three hundred years: who played, '
                       'what the gallery did, who was never the same after. {N} wants to read all of it.'),
                      ('B',
                       "The fee for the night is ten times a season's wage, and the fame of it lasts a lifetime. "
                       '{rival} wants it as badly as {N} does.'),
                      ('R',
                       'To play to the living and the dead at once, with the whole gallery leaning forward: {N} can '
                       'hardly breathe for wanting it.'),
                      ('G',
                       '{N} cannot stop thinking about one face that might be in the gallery: {dead}, gone these '
                       'many years, who never once saw {N} on a stage.')]},
 'outcomes': (['When the lamps come up the gallery is empty again, and the night has gone the way {N} hoped.',
               'Years later the old players still speak of that night of the dead, and of {N}.'],
              ['The night goes cold and strange, and {N} leaves the playhouse before the lamps are out.',
               "The house master gives the night to {rival}, and {N} hears the gallery's silence from the street."]),
 'options': [
    ("try for the lead by the Order's rules, with a token left for the dead", 'W1', None, 0.45, '', {'title': 'lead actor or actress', 'mark': 'took a wild risk', 'aims': 'lead actor or actress', 'v': 'tradition, conformity', 'chance': 0.3}),
    ("read the house's record of every night of the dead, then try for the lead", 'U1', None, 0.45, '', {'title': 'lead actor or actress', 'mark': 'learned a skill', 'aims': 'lead actor or actress', 'v': 'self-direction, achievement', 'chance': 0.3}),
    ('try for the lead for the fee, and the fame in both worlds', 'B1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'power, achievement', 'chance': 0.3}),
    ('try for the lead, to play for the living and the dead at once', 'R1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'stimulation, self-direction', 'chance': 0.3}),
    ('try for the lead, and play it for one face in the gallery', 'G1', None, 0.45, '', {'title': 'lead actor or actress', 'v': 'benevolence, tradition', 'chance': 0.3}),
    ('refuse to play that night, and ask the Order to bless the house first', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'tradition, security', 'chance': 0.7}),
    ("learn the lead's part as its second, and wait in the wings that night", 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'learning lines', 'habit': True, 'binds': True, 'v': 'achievement, conformity', 'chance': 0.7}),
    ('take a small part that night, and keep the young players close by the lamps', 'W.34 R.33 G.33', None, 0.5, '', {'binds': True, 'v': 'benevolence, stimulation', 'chance': 0.7}),
    ("ask the company's medium to call the dead down from the gallery into the play", 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'good notices', 'mark': 'took a wild risk', 'closed': "approval: calling the dead onto the stage without the Order's leave; backfire: nothing answers but a cold wind, and the house master shuts the old playhouse to the company for a year", 'v': 'stimulation, power', 'chance': 0.7}),
    ('climb to the gallery after the curtain, and look for your own dead', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'took a wild risk', 'v': 'benevolence, stimulation', 'chance': 0.7}),
 ]},
{'name': 'a glamour that makes the play real',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.005),
 'drivers': 'fortune+.2 prosper+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'rival, mentor, friend',
 'requires': 'professional actor | voice actor | understudy | amateur actor',
 'worlds': {'magic': 'an illusionist in a velvet coat, in your dressing room, with a small silver bell'},
 'only': 'magic',
 'timing': {'times': 'per working player (professional or voice) of two years or more, or amateur of five years with '
                     'a lead behind them, in the magic world a year: about 1 in 100 (estimate)',
            'likelier': 'a first try-out in a lead, a city where glamours are sold under the counter, a player with '
                        'more nerves than nights on stage',
            'rarer': 'a company the Order watches closely, a player long settled in the lead, a house master who '
                     'searches the dressing rooms',
            'gap_years': (5.0, 10.0)},
 'scenes': {'magic': [('',
                       'The night before {Ns} first try-out in a lead, an illusionist in a velvet coat is waiting in '
                       'the dressing room with a small silver bell. One ring before the curtain, he says, and the '
                       'house will see and feel the play as if it were real: they will weep, and they will not '
                       'forget. He does not say what it costs, only that it asks something of the player.'),
                      ('W',
                       "Glamours on a public stage need the Order's licence, and this one carries none that {N} can "
                       'see. There are rules for this, and good reasons for them.'),
                      ('U',
                       'Every glamour draws its power from somewhere. {N} wants to know exactly where this one draws '
                       'it from before touching the bell.'),
                      ('B',
                       'If the house loves the try-out, the lead is {Ns} for the whole season. {rival} would ring '
                       'that bell without a second thought, and {N} knows it.'),
                      ('R',
                       '{N} can feel the pull of it already: one ring, and the whole house in the palm of a hand. Or '
                       "there is the hedge-witch in the lanes behind the playhouse, who sells a night's glamour and "
                       'asks no questions.'),
                      ('G',
                       'The company has played the plain way for forty years, and {mentor} always says a house can '
                       'tell when it is being cheated.')]},
 'outcomes': (['The curtain comes down to a silence, then a roar, and the night ends the way {N} wanted.',
               'Long after the season ends, {N} is glad of the choice made in that dressing room.'],
              ["The try-out goes wrong from the first scene, and the house master gives the season's lead to "
               '{rival}.',
               'Something of that night stays wrong for a long time, and {N} is never quite sure what it cost.']),
 'options': [
    ('report the illusionist to the Order, which licenses every glamour in the city', 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.64}),
    ('make the illusionist write down exactly what the glamour takes, before any answer', 'U1', None, 0.45, '', {'v': 'self-direction, security', 'chance': 0.84}),
    ("pay the illusionist's price, and play the try-out under the glamour", 'B1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'mark': 'took a wild risk', 'binds': True, 'v': 'power, achievement', 'chance': 0.35}),
    ('wear a glamour bought from a hedge-witch for the night, and go on', 'R1', None, 0.45, '', {'title': 'lead actor or actress; professional actor', 'mark': 'took a wild risk', 'closed': 'approval: an unlicensed glamour on a public stage; backfire: the glamour breaks in the first scene, the whole house sees it, and the company lets the player go', 'v': 'stimulation, self-direction', 'chance': 0.3}),
    ('send the illusionist away, and warn the rest of the company about him', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'chance': 0.5}),
    ("keep the illusionist's card, for a night when the company needs it more", 'B.5 G.5', None, 0.5, '', {'door': True, 'self_control': '+', 'v': 'security, power', 'chance': 0.8}),
    ("sell the story of the illusionist's offer to the broadsheets", 'B.5 R.5', None, 0.5, '', {'mark': 'made an enemy', 'v': 'achievement, stimulation', 'chance': 0.8}),
    ("ask the company's oldest player what glamours have taken from players before", 'U.5 G.5', None, 0.5, '', {'v': 'universalism, tradition', 'chance': 0.5}),
    ('throw the illusionist out of the dressing room, bell and all', 'W.5 R.5', None, 0.5, '', {'v': 'universalism, stimulation', 'chance': 0.9}),
    ('play the try-out plain, on craft and long rehearsal alone', 'W.5 U.5', None, 0.5, '', {'title': 'lead actor or actress; professional actor', 'self_control': '+', 'v': 'conformity, achievement', 'chance': 0.12}),
 ]},
{'name': 'the mask that changes its wearer',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.01, 0.01, 0.01, 0.01, 0.01),
 'drivers': 'fortune+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'friend, mentor, rival, elder',
 'requires': 'professional actor | amateur actor | background artist | drama school student',
 'tenure': (1.0, 100.0),
 'worlds': {'magic': 'a mask of white lacquer at the bottom of the costume trunk, warm to the touch'},
 'only': 'magic',
 'timing': {'times': 'per player, extra or drama student of a year or more in the magic world a year: about 1 in 100 '
                     '(estimate)',
            'likelier': 'an old playhouse or guild hall with trunks nobody has opened in years, a company that buys '
                        'old costumes, a player restless in small parts',
            'rarer': 'a new company with new costumes, a player who never goes near the wardrobe, a city where the '
                     'Order searches every trunk',
            'gap_years': (5.0, 10.0)},
 'scenes': {'magic': [('',
                       'At the bottom of an old costume trunk, under moth-eaten cloaks, {N} finds a mask of pale '
                       'lacquer that is warm to the touch. The wardrobe mistress says it belonged to a famous '
                       'player, long dead, whose family still lives in the old quarter. Whoever wears it, the story '
                       'goes, becomes anyone on the stage, and a little more of them each time.'),
                      ('W',
                       'A thing like this belongs with the Order, which keeps such things safe. {N} knows that is '
                       'what the rules say, whatever the mask might do on a stage.'),
                      ('U',
                       "Who made it, and how? {N} turns the mask over and over, looking for a maker's mark, and "
                       'finds only a line of tiny letters in no tongue {N} knows.'),
                      ('B',
                       'Collectors of strange things pay fortunes for less. And worn on the right night, before the '
                       'right company master, it might be worth more than any fortune.'),
                      ('R',
                       '{N} holds it up to the lamp and feels the warmth spread into {Ns} fingers. One night in it, '
                       'just one, to be anyone at all.'),
                      ('G',
                       "Old things like this have their own ways, and the wardrobe mistress makes the Order's sign "
                       'whenever she passes the trunk. {N} thinks of the players the mask must have changed, and of '
                       'the family it came from.')]},
 'outcomes': (['Months later {N} is still sure it was the right choice, and the wardrobe trunk is just a trunk '
               'again.',
               'The whole company notices something new in {N}, and {N} likes what it is.'],
              ['The mask turns up again where {N} least expects it, as warm as ever.',
               'Something of the mask stays with {N} for a long time, and {friend} says {N} has not been the same '
               'since.']),
 'options': [
    ("take the mask to the Order's house, and let them keep it safe", 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.85}),
    ('study how the mask was made, and wear it only in rehearsal', 'U1', None, 0.45, '', {'mark': 'learned a skill', 'v': 'self-direction, universalism', 'chance': 0.67}),
    ('sell the mask to a collector of strange things, for a very good price', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.8}),
    ('wear it in every play from now on, whatever it changes', 'R1', None, 0.45, '', {'mark': 'took a wild risk', 'identity': True, 'self_control': '-', 'v': 'stimulation, self-direction', 'chance': 0.67}),
    ('break the mask, and bury the pieces under the old yew behind the playhouse', 'G1', None, 0.45, '', {'v': 'tradition, security', 'chance': 0.57}),
    ('wear it once, for one great part, and then put it away', 'U.5 R.5', None, 0.5, '', {'grants': 'a lead role to remember', 'self_control': '+', 'v': 'stimulation, self-direction', 'chance': 0.5}),
    ("wear it at the guild's open trial, by the guild's rules, with a company master watching", 'W.5 B.5', None, 0.5, '', {'title': 'professional actor', 'v': 'achievement, conformity', 'chance': 0.25}),
    ('ask a mask-maker what it is worth, and what it has taken from its wearers', 'U.5 B.5', None, 0.5, '', {'door': True, 'self_control': '+', 'v': 'security, power', 'chance': 0.8}),
    ('throw it in the river at night, and walk home free of it', 'R.5 G.5', None, 0.5, '', {'v': 'self-direction, tradition', 'chance': 0.8}),
    ('give it back to the family of the player it once belonged to', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'chance': 0.7}),
 ]},
]

ECHOES = [
{'name': 'the part you never got to play',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.01,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'performing, leisure, meaning',
 'horizon': 'months',
 'roles': "friend, partner, colleague, the players' director",
 'once': True,
 'worlds': {'earth': "a notice for the local players' auditions, in the same hall where the school play was",
            'tribal': 'the children rehearse the small spirits for midwinter, and you remember the part you wanted',
            'magic': "the guild's pageant wagons roll past, and you remember the masque you were too shy to try for"},
 'timing': {'times': 'per person who met the school play as a child: about 1 in 50 come back to the stage as adults, '
                     'years later (estimate)'},
 'after': "moment 'the school play' as a child under 13, and now 18 or more, neither acting with the local players "
          'nor for a living (no [amateur actor], no [professional actor])',
 'delay_years': (6, 40),
 'likelier': 'much Red and Green in the color history; time to spare; singing or dancing kept up since',
 'rarer': 'stress above 1.5; little money; children at home and little time',
 'scenes': {'earth': [('',
                       'Years after the school play, {N} walks past the old school hall and sees a notice in the '
                       'porch: the local players hold their auditions there next week. The smell of floor polish and '
                       'dusty curtains comes back all at once.'),
                      ('W',
                       '{N} never did get the part back then, and always half believed it went to the right child. '
                       'Still, the notice says all are welcome, and there is no rule about being too old.'),
                      ('U',
                       '{N} still remembers the lines of the part that went to someone else, every one of them, '
                       'which is strange after so many years. It would be interesting to know whether there was '
                       'anything there.'),
                      ('B',
                       'The child who got that part went on to nothing much, {N} has heard. {N} wonders, not for the '
                       'first time, what the right chance might have led to.'),
                      ('R',
                       'Standing in that porch, {N} feels the old ache like a bruise: the costume made from '
                       'curtains, the part that went to someone else, the wanting. It has not gone anywhere.'),
                      ('G',
                       '{N} thinks of the teacher who ran the play, the families on plastic chairs, the curtains '
                       'that stuck. It belongs to a time and a place, and the place is still here.')],
            'tribal': [('',
                        'The children of the band are learning the small spirits for midwinter, squeaking like mice '
                        "and stamping like elk. {N} watches from the edge of the firelight and remembers the hare's "
                        'part, given to another child all those winters ago.')],
            'magic': [('',
                       "The guild's pageant wagons roll through the square, painted and garlanded, and the players "
                       'wave from the tailboards. {N} remembers the schoolroom masque, and the part {N} was too shy '
                       'to try for.')]},
 'outcomes': (['{N} steps onto a stage again, or close to one, and finds the old ache has turned into something '
               'better.',
               'Within a few months {N} has a part, a place or a plan, and wonders what took so long.'],
              ['The day comes and goes, and {N} stays home and tells no one.',
               '{N} goes along, feels too old and too slow among the regulars, and does not go back.']),
 'options': [
    ('go to the auditions in that same hall, and take any part they offer', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'amateur actor', 'identity': True, 'world': {'tribal': "ask the band's tellers for a place in the midwinter telling, whatever part they give", 'magic': "go to the mystery players' trials, and take any part they offer"}, 'chance': 0.8}),
    ('find out whether the drama schools take people your age, and send for the forms', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'aims': 'drama school student', 'identity': True, 'world': {'tribal': 'ask whether an old teller of another band would take an apprentice of your age', 'magic': 'find out whether the guild school takes scholars of your age, and send for the rolls'}, 'chance': 0.65}),
    ("ring the players' director, and ask what it would take to be cast in something good", 'B1', None, 0.45, '', {'v': 'achievement, power', 'door': True, 'world': {'tribal': 'ask the shaper of the telling, quietly, what it would take to be given a real part', 'magic': 'call on the pageant master, and ask what it would take to be cast well'}, 'chance': 0.75}),
    ('turn up at the auditions on a whim, and sing the song from the school play', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'amateur actor', 'world': {'tribal': "walk into the tellers' circle and dance the hare the way you always wanted to", 'magic': 'turn up at the trials on a whim, and sing the song from the old masque'}, 'chance': 0.7}),
    ('let it rest: that part belongs to the child you were', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'let it rest: that part belongs to the child you were', 'magic': 'let it rest: the masque belongs to the child you were'}, 'chance': 0.8}),
    ('sign up as an extra for the film in town, and bring the family to watch', 'W1', 'G.7', 0.5, '', {'v': 'conformity, benevolence', 'title': 'background artist', 'world': {'tribal': "walk in the herd at a neighbouring band's great telling, with your own kin alongside", 'magic': "walk in the illusionists' procession, and bring the family to watch"}, 'chance': 0.7}),
    ("offer to help backstage at the local players' next show, and watch how it is made", 'U1', 'W.7', 0.5, '', {'v': 'benevolence, self-direction', 'world': {'tribal': 'offer to tend the fire and the screens at midwinter, and watch how the telling is made', 'magic': 'offer to help with the pageant wagons, and watch how the play is made'}, 'chance': 0.85}),
    ('pay a coach for a few lessons, and find out if there is anything there', 'B1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'grants': 'acting', 'mark': 'learned a skill', 'world': {'tribal': "give an old teller a good hide for a winter's teaching, and find out if there is anything there", 'magic': 'pay an old player for lessons, and find out if there is anything there'}, 'chance': 0.75}),
    ('post the old school-play photograph online, and announce you are going back on stage', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'identity': True, 'world': {'tribal': 'tell every hearth you mean to play at midwinter, and a better part than the hare', 'magic': 'tell the whole tavern you mean to be in the next pageant, and in a part worth having'}, 'chance': 0.75}),
    ('put on a little play at home with the children in the family', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, hedonism', 'world': {'tribal': 'play the hare for the children of your hearth by the fire, the way you always wanted to', 'magic': 'put on a little masque at home for the children of the family'}, 'chance': 0.7}),
 ]},
{'name': 'never too late for the stage',
 'stages': 'mature elder',
 'age': (55, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.02,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'leisure, community, performing',
 'horizon': 'months',
 'roles': "partner, friend, neighbour, the players' director",
 'once': True,
 'worlds': {'earth': 'a notice for the local players, and a whole week free for rehearsals at last',
            'tribal': 'too old for the hunt, you are asked to tell the old stories at the fire',
            'magic': "the guild's mystery players want grey heads for the elders in the pageant"},
 'timing': {'times': 'per new retiree: about 1 in 40 take up amateur theatre or extra work in the first years of '
                     'retirement; amateur societies draw members of every age (estimate)'},
 'after': "moment 'the first months of retirement', and now retired, not already an amateur actor (no [amateur "
          'actor]), with health enough for evening rehearsals',
 'delay_years': (0, 3),
 'likelier': 'an amateur actor, a youth theatre member or a lead role in the past; time to spare; much Green and Red '
             'in the color history',
 'rarer': 'poor health; little money; a partner who gives little support',
 'scenes': {'earth': [('',
                       'The leaving party is a few weeks behind {N}, and the days have a strange width to them. In '
                       'the library a notice says the local players are casting their spring play, rehearsals on '
                       'Tuesday and Thursday evenings, and they are short of older actors.'),
                      ('W',
                       "For forty years {Ns} week belonged to someone else's timetable. A society with a rehearsal "
                       'schedule and a part to learn by a date is a shape {N} understands.'),
                      ('U',
                       '{N} has always wondered how actors remember it all, and what it is like to become someone '
                       'else for two hours. There is time to find out now.'),
                      ('B',
                       '{N} spent a working life being listened to in meetings, and misses it more than expected. A '
                       'stage is another room where people listen.'),
                      ('R',
                       '{N} feels oddly giddy reading the notice, like a teenager. Why not? Who is going to stop {N} '
                       'now?'),
                      ('G',
                       "Half the faces in the players' photographs are people {N} has known for years: the woman "
                       'from the post office, the old headmaster, a neighbour from two doors down. They are all '
                       'growing older together, on a stage.')],
            'tribal': [('',
                        'The hunt has gone on without {N} this season, and the young ones run faster now. At the '
                        'fire one night the old teller nods at {N}: the band needs someone to tell the old stories, '
                        'and {N} remembers them all.')],
            'magic': [('',
                       "The guild's mystery players nail a notice to the hall door: grey heads wanted for the elders "
                       'and the kings in the feast-day pageant, no experience needed. {N} reads it twice.')]},
 'outcomes': (['By the spring {N} has a part, a head full of lines, and a whole new set of friends.',
               '{N} finds that the years have left a voice worth hearing, and people who want to hear it.'],
              ['The first evening is all in-jokes and old hands, and {N} slips out before the end and does not go '
               'back.',
               'A bad winter for {Ns} health puts the whole idea away for another year.']),
 'options': [
    ('join the local players, and be word-perfect by the first read-through', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'amateur actor', 'self_control': '+', 'world': {'tribal': "join the band's players for the midwinter telling, and know every word by the first fire", 'magic': 'join the mystery players, and know your lines before the first practice'}, 'chance': 0.7}),
    ('take an acting class for older beginners at the college, and learn it properly', 'U1', None, 0.45, '', {'v': 'self-direction', 'grants': 'acting', 'mark': 'learned a skill', 'world': {'tribal': 'sit with the old teller through the winter, and learn how a telling is held', 'magic': 'take lessons from an old player of the guild, and learn the craft properly'}, 'chance': 0.75}),
    ('sign with the background agency: adverts and films want older faces, and it pays', 'B1', None, 0.45, '', {'v': 'achievement, security', 'title': 'background artist', 'world': {'tribal': "offer to walk as one of the dead in a neighbouring band's great telling, for a share of the feast", 'magic': "put your name down for the illusionists' processions: they pay grey heads by the night"}, 'chance': 0.75}),
    ("audition for the players' next show on a whim, and go for the loudest part", 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'amateur actor', 'world': {'tribal': 'stand up at the fire and play the old bear, loud enough to wake the sleepers', 'magic': "try for the pageant's king on a whim, the loudest part in it"}, 'chance': 0.65}),
    ('let it rest: the garden and the family fill the week well enough', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'let it rest: the grandchildren and your own fire are enough', 'magic': 'let it rest: the garden and the family fill the days well enough'}, 'chance': 0.8}),
    ('offer to prompt for the players, and learn how a show is put together', 'W1', 'U.7', 0.5, '', {'v': 'benevolence, self-direction', 'door': True, 'aims': 'amateur actor', 'world': {'tribal': 'offer to keep the masks and give the players their signs, and learn how a telling runs', 'magic': 'offer to hold the book for the mystery players, and learn how a pageant is made'}, 'chance': 0.8}),
    ('read the plays the players have chosen, and pick the part you could win', 'U1', 'B.7', 0.5, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'listen to the tellings the band will play, and choose the part you could win', 'magic': "read the pageant's book, and pick the part you could win"}, 'chance': 0.75}),
    ('start a play-reading group at home, and choose every play yourself', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'habit': True, 'world': {'tribal': 'gather the old ones at your own hearth for tellings, and choose every story yourself', 'magic': 'start a reading circle in your parlour, and choose every play yourself'}, 'chance': 0.75}),
    ("read stories aloud at the library's Saturday story time for small children", 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'grants': 'telling a story aloud', 'habit': True, 'world': {'tribal': 'tell the children of the band the old stories at dusk, with all the voices', 'magic': 'read tales aloud to the children at the guild hall on feast days'}, 'chance': 0.85}),
    ("go along with an old friend to the players' social evening first", 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'mark': 'made a friend', 'world': {'tribal': "sit with your old friends at the tellers' fire first, and listen", 'magic': "go with an old friend to the mystery players' supper first"}, 'chance': 0.7}),
 ]},
{'name': 'the show you wrote to star in',
 'stages': 'young_adult adult mature elder',
 'age': (17, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'performing, making, money',
 'horizon': 'months',
 'roles': 'friend, partner, colleague, mentor',
 'once': True,
 'worlds': {'earth': "an idea for a one-person show, and the fringe's registration closes in a month",
            'tribal': 'a telling of your own, and the outer fires at the gathering where anyone may play',
            'magic': "a play of your own, and a pitch at the fair's booths"},
 'timing': {'times': 'per person who can act and meets an idea that will not let go, or the wish to be seen: about 1 '
                     'in 15 write and book a show of their own; the largest fringe festival had over 3,300 shows in '
                     '2024, most of them from small companies (estimate)'},
 'after': "moment 'inspiration strikes' or 'wanting to be noticed' in someone who can act ([acting]), 17 or more, "
          'holding no lead ([lead actor or actress]) and no [a fringe slot]',
 'delay_years': (0, 2),
 'likelier': 'writing stories or scripts; improvisation; much Red and Blue in the color history',
 'rarer': 'stress above 1.5; little money; more than one child at home',
 'scenes': {'earth': [('',
                       'The idea arrives whole on a bus and will not leave: a one-person show, an hour long, about '
                       "something only {N} could tell. The fringe's registration closes in a month, and the cheapest "
                       'rooms go first.'),
                      ('W',
                       '{N} wants to do it properly: the script finished before a room is booked, a budget written '
                       "down, every form in on time. The festival's rules run to forty pages, and {N} reads all of "
                       'them.'),
                      ('U',
                       'The idea has a shape {N} can almost see: where it starts, where it turns, the one image it '
                       'builds toward. {N} fills a notebook in a week.'),
                      ('B',
                       'Nobody is going to hand {N} a part worth having. A show of {Ns} own, with {Ns} own name on '
                       'the poster, is a part nobody can give to someone else.'),
                      ('R',
                       '{N} cannot sleep for it. The show is already playing in {Ns} head every night, to a full '
                       'room that laughs in all the right places.'),
                      ('G',
                       "The story is really {Ns} grandmother's, or the street's: something that happened here, to "
                       'people {N} knows, that nobody has ever put on a stage.')],
            'tribal': [('',
                        'A telling of {Ns} own has been growing all winter, a story nobody in the band has heard. At '
                        'the gathering the outer fires belong to anyone who wants to play, and the clans wander from '
                        'one to the next.')],
            'magic': [('',
                       "A play of {Ns} own has been going round {Ns} head for a season. The fair's booths can be "
                       'hired by the week, and the crowds that come for the wagons spill into them.')]},
 'outcomes': (['The show goes up, rough at the edges, and the people who came stay behind to talk about it.',
               '{N} has something of {Ns} own at last, with {Ns} own name on it, and it feels better than any part '
               'ever given.'],
              ['The money, the forms and the fear pile up, and the idea goes back to sleep.',
               'The show goes up to a room of seven people, three of them friends, and {N} wonders what it was all '
               'for.']),
 'options': [
    ('finish the script first, then register with the fringe properly, every form on time', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'grants': 'a fringe slot', 'world': {'tribal': 'shape the telling to its end first, then ask the keeper for a place at the outer fires', 'magic': "finish the play first, then take out the fair's licence properly, every seal in order"}, 'chance': 0.7}),
    ('write and rewrite the script for a month before showing it to anyone', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'grants': 'writing scripts', 'habit': True, 'self_control': '+', 'world': {'tribal': 'tell it to yourself on the long walks, over and over, until every part fits', 'magic': 'write and rewrite the play for a month before anyone sees a page'}, 'chance': 0.75}),
    ('book the best room you can afford with your savings, and sell it hard', 'B1', None, 0.45, '', {'v': 'achievement, power', 'grants': 'a fringe slot', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'binds': True, 'world': {'tribal': 'trade your best furs for a good place at the outer fires, and bring the crowd yourself', 'magic': 'hire the best booth you can afford, and cry it through the fair yourself'}, 'chance': 0.8}),
    ('book the cheapest room at the fringe tonight, before the nerve goes', 'R1', None, 0.45, '', {'v': 'stimulation', 'grants': 'a fringe slot', 'world': {'tribal': 'walk to the gathering with nothing but the telling, and take the first empty fire', 'magic': 'hire the cheapest booth at the fair tonight, before your nerve goes'}, 'chance': 0.7}),
    ('let it rest: the idea can grow quietly in a notebook for a year or two', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'let it rest: the telling can grow quietly by your own fire for a winter or two', 'magic': 'let it rest: the play can grow in a drawer for a year or two'}, 'chance': 0.8}),
    ('set up a small company with two friends, with a bank account and a written agreement', 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'grants': 'a company of your own', 'binds': True, 'world': {'tribal': 'gather two friends as a band of players, with a promise sworn at the fire', 'magic': 'found a small company with two friends, with a licence and a written agreement'}, 'chance': 0.75}),
    ('work the show out by improvising it for friends, week after week', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'grants': 'improvisation', 'world': {'tribal': 'make the telling up anew at your own fire each night, until it finds its shape', 'magic': 'play it without a book for friends, week after week, until it finds its shape'}, 'chance': 0.7}),
    ('ask the family business to pay the venue fee, with its name on the poster', 'B1', 'G.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'ask your kin to feast the crowd at your fire, and promise them the honour of it', 'magic': 'ask the family workshop to pay for the booth, its name on the playbill'}, 'chance': 0.65}),
    ('put the show on free in the community hall first, for anyone who comes', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'tell it free at every hearth of your own band first', 'magic': "play it free in the ward's hall first, for anyone who comes"}, 'chance': 0.75}),
    ('ask the old ones at home for their stories, and build the show from them', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'world': {'tribal': 'sit with the old ones of your band, and build the telling from what they remember', 'magic': 'ask the old folk of the lane for their stories, and build the play from them'}, 'chance': 0.65}),
 ]},
{'name': 'the part that came with the letter',
 'stages': 'young_adult adult mature',
 'age': (17, 65),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.1,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'work, performing, home',
 'horizon': 'months',
 'roles': 'partner, boss, friend, colleague',
 'once': True,
 'worlds': {'earth': 'a letter from a small touring company: someone saw you, and there is a part',
            'tribal': 'a band upriver sends word: their teller has heard of you, and wants you for the winter',
            'magic': "a sealed letter from a travelling company's master: a part, if you can join the wagons by "
                     'spring'},
 'timing': {'times': 'per amateur actor, extra or drama student who can act and met an unexpected chance of a role: '
                     'about 1 in 8 are offered paid work from it (estimate)'},
 'after': "moment 'an unexpected chance: a grant, a role, a stage' in someone who can act ([acting]), 17 or more and "
          'not yet a professional actor (no [professional actor]), on the rung below a paid part: an amateur actor '
          'or an extra of two years or more, or a drama student of a year or more',
 'delay_years': (0, 1),
 'likelier': 'a lead role to remember; acting with the local players; a listing in the casting directory',
 'rarer': 'stress above 1.5; more than one child at home; poor health',
 'scenes': {'earth': [('',
                       'A letter comes from a small touring company {N} has never heard of. Its director saw {N} in '
                       'a show, and there is a part in the spring tour: twelve weeks, forty towns, a small fee, and '
                       'a different bed every week.'),
                      ('W',
                       'The letter is courteous and exact: the dates, the fee, the terms of the contract, a reply by '
                       'the end of the month. {N} reads it like a promise someone is already keeping.'),
                      ('U',
                       '{N} looks the company up: three tours, good notices in small papers, and a play {N} has read '
                       'and loved. It is a real chance to learn the work from the inside.'),
                      ('B',
                       "A paid part means a real credit, the actors' union, an agent who might return a call. {N} "
                       'reads the cast list twice and sees the lead has not been cast yet.'),
                      ('R',
                       '{N} reads it three times standing in the hall, then shouts. Someone saw {N}, and wants {N}, '
                       'and it is real.'),
                      ('G',
                       'Twelve weeks on the road means twelve weeks away from home: {partner}, the friends, the day '
                       'job, the garden. {N} sits with the letter at the kitchen table for a long time.')],
            'tribal': [('',
                        'A runner comes down the river with word from a band upriver: their teller has heard of {Ns} '
                        'tellings at the gathering, and wants {N} at their fire for the whole winter, fed by every '
                        'hearth.')],
            'magic': [('',
                       "A sealed letter with a travelling company's mark comes by the carrier: its master saw {N} at "
                       'the fair, and there is a part for {N}, if {N} can join the wagons by spring.')]},
 'outcomes': (['The answer goes back, and {N} never once regrets it in the year that follows.',
               'By spring {N} is on the road with a company, learning the work from the inside.'],
              ['The company goes quiet after the first reply, and the part goes to someone else.',
               'Three weeks into the tour the money runs out, and {N} comes home with nothing but stories.']),
 'options': [
    ('write back by return, accept the part, and give the day job proper notice', 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'professional actor', 'world': {'tribal': 'send word back by the runner that you will come, and settle your duties at home first', 'magic': 'seal your answer the same day, and give your master proper notice'}, 'chance': 0.58}),
    ('ask for the script first, read it twice, then say yes', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'title': 'professional actor', 'binds': True, 'world': {'tribal': 'ask the runner which tellings they will want, and say yes once you know them', 'magic': 'ask for the play first, read it twice, then send your answer'}, 'chance': 0.55}),
    ('see that the lead is not cast yet, and ask to read for it instead', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'professional actor', 'grants': 'a lead role to remember', 'aims': 'professional actor', 'world': {'tribal': 'ask to wear the great mask of their winter telling, not a lesser part', 'magic': 'write back asking to read for the leading part, not the one offered'}, 'chance': 0.12}),
    ('say yes, and walk out of the day job the same afternoon', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'title': 'professional actor', 'mark': 'broke your word', 'closed': 'approval: leaving a job without notice; backfire: no reference, and the old boss tells anyone who asks', 'self_control': '-', 'world': {'tribal': 'leave with the runner that same day, hunt or no hunt', 'magic': "say yes, and walk out of your master's shop the same afternoon"}, 'chance': 0.55}),
    ('turn it down: home, the family and the day job come first', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'mark': 'turned down a chance', 'identity': True, 'world': {'tribal': 'send word back that your place is with your own band this winter', 'magic': 'write back that home and family come first'}, 'chance': 0.9}),
    ("ask the day job for twelve weeks' unpaid leave, by the book, before answering", 'W1', 'R.7', 0.5, '', {'v': 'conformity, stimulation', 'world': {'tribal': "ask the elders' leave to be gone for the winter, before answering", 'magic': "ask your master for a season's leave, by the guild's rules, before answering"}, 'chance': 0.45}),
    ('ask for a week to think, and ask an actor you trust about the company', 'U1', 'G.7', 0.5, '', {'v': 'security, self-direction', 'world': {'tribal': 'ask an old teller who has been upriver what that band is like, before answering', 'magic': 'ask an old player what the company is really like, before answering'}, 'chance': 0.5}),
    ('put your name in the casting directory, now that a company has written', 'B1', 'W.7', 0.5, '', {'v': 'achievement, security', 'grants': 'casting directory listing', 'world': {'tribal': 'make sure every band at the gathering hears that a band upriver has sent word', 'magic': "put your name on the brokers' roll, now that a company has sent word"}, 'chance': 0.9}),
    ('turn it down, but ask to sit in on their rehearsals and learn', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, stimulation', 'self_control': '+', 'world': {'tribal': 'send word you cannot come, but ask to watch their tellings at the gathering', 'magic': 'decline, but ask to watch the company rehearse when it passes through'}, 'chance': 0.48}),
    ('write back that you will come if the company finds work for your partner too', 'G1', 'B.7', 0.5, '', {'v': 'benevolence, security', 'binds': True, 'world': {'tribal': "send word you will come if your partner's hearth can winter there too", 'magic': 'write back that you will come if the company takes your partner on as well'}, 'chance': 0.15}),
 ]},
{'name': 'the same door, years later',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.1,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'work, performing, meaning',
 'horizon': 'months',
 'roles': 'friend, partner, mentor, rival',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, the same kind of door opens a crack: an open call, a '
                     'festival, a theatre post',
            'tribal': 'winters after the attempt that failed, the gathering again asks for players, makers and '
                      'keepers',
            'magic': 'years after the attempt that failed, the same kind of notice goes up on the guild hall door'},
 'timing': {'times': 'per person who missed a stage long shot: about 1 in 8 meet the same kind of door again years '
                     'later (estimate); many actors, writers and theatre-makers say they got in on a later try, and '
                     'few long shots land on the first one (estimate)'},
 'after': "a long shot missed in one of the moments of stage-longshots.lib ('the lead from the open queue', 'filmed "
          "by chance in the street', 'the film you made with friends', 'the old theatre needs someone to save it', "
          "'the late starter', 'the night both covers are off'), holding [a long shot that missed], within the month "
          'of the miss; now 21 or more, not playing a lead (no [lead actor or actress]) and not running a theatre '
          '(no [artistic director]); the try is for the same title again ({missed})',
 'delay_years': (3, 15),
 'likelier': 'acting, writing or directing kept up since; much Red and Black in the color history; time to spare',
 'rarer': 'stress above 1.5; little money; poor health',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, the same kind of door opens a crack: a notice for an '
                       "open call, a festival's new call for films, a theatre that needs someone again. {N} reads it "
                       'twice, standing very still.'),
                      ('W',
                       'Last time {N} did what was asked, and it was not enough. This time {N} knows exactly what is '
                       'asked, and has had years to get it right.'),
                      ('U',
                       '{N} has thought about that day more than anyone would guess, and knows now what went wrong '
                       'in the room, and what was missing from the work.'),
                      ('B',
                       'The people who decide are older now, and some of them owe {N} a favour. The odds are still '
                       'long, but they are not the same odds.'),
                      ('R',
                       'The old ache comes back in one breath, as if no time had passed at all. {N} is older now, '
                       'and has stopped caring what anyone thinks.'),
                      ('G',
                       '{friend} still has the photograph from that day, and has said for years that one try is not '
                       'a life. The town would turn out to see it, either way.')],
            'tribal': [('',
                        'Winters after the attempt that failed, the gathering again asks for players and makers. {N} '
                        'sits at the edge of the firelight, older now, and the old wanting stirs.')],
            'magic': [('',
                       'Years after the attempt that failed, the same kind of notice goes up on the guild hall door, '
                       "in the same crier's hand. {N} reads it twice.")]},
 'outcomes': (['This time the call comes back, and {N} sits on the stairs with the phone for a long while, laughing, '
               'before telling anyone.',
               'Whatever {N} chose, the second time feels different: steadier, kinder, and entirely {Ns} own.'],
              ['It is the same kind of no as last time, almost to the word, and {N} finds that it stings less, and '
               'is proud of having gone back.',
               '{N} gets one room further than before, hears a real compliment from someone who matters, and walks '
               'home through the park in no hurry at all.']),
 'options': [
    ('go back to the same kind of door, prepared this time to the last detail', 'W1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': 'go back to the same fire, prepared this time to the last step', 'magic': 'go back before the same kind of master, prepared this time to the last line'}, 'chance': 0.04}),
    ('go back with the work rebuilt from everything the first try taught', 'U1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'self-direction, achievement', 'world': {'tribal': 'go back with the telling rebuilt from everything the first try taught', 'magic': 'go back with the piece rebuilt from everything the first try taught'}, 'chance': 0.04}),
    ('go back through an old contact, and be put forward properly this time', 'B1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'go back through an elder who owes your hearth a gift, and be put forward properly', 'magic': 'go back through an old patron, and be put forward properly this time'}, 'chance': 0.04}),
    ('walk back in older, with nothing left to lose', 'R1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'identity': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'walk back into the firelight older, with nothing left to lose', 'magic': 'walk back into the trial hall older, with nothing left to lose'}, 'chance': 0.04}),
    ('go back with your own people behind this time', 'G1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'go back with your own band drumming behind this time', 'magic': 'go back with your own ward cheering behind this time'}, 'chance': 0.04}),
    ('work with a coach for a year first, and wait for the next door', 'W1', 'U.7', 0.5, '', {'grants': 'auditioning', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': "sit a winter at the old teller's fire first, and wait for the next gathering", 'magic': 'take a year of lessons first, and wait for the next notice'}, 'chance': 0.78}),
    ('ask the people who said no, plainly, what was missing last time', 'U1', 'B.7', 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'ask the elders who chose another, plainly, what was missing', 'magic': 'ask the master who said no, plainly, what was missing'}, 'chance': 0.78}),
    ('put the old clip and the old film back out, and see who still remembers', 'B1', 'R.7', 0.5, '', {'grants': 'following online', 'v': 'stimulation, power', 'world': {'tribal': 'tell the old attempt at every fire again, and see who still remembers', 'magic': 'show the old glass again in the taverns, and see who still remembers'}, 'chance': 0.78}),
    ('play it again where it all started, for the people at home', 'R1', 'G.7', 0.5, '', {'mark': 'came home', 'v': 'hedonism, tradition', 'world': {'tribal': "play it again at your own band's fire, for the people who knew you first", 'magic': "play it again in your own ward's hall, for the people who knew you first"}, 'chance': 0.78}),
    ('go along with a younger hopeful who is trying now, and wait outside', 'G1', 'W.7', 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, tradition', 'world': {'tribal': 'walk with a young one who is trying now, and wait at the edge of the firelight', 'magic': 'go with a young hopeful who is trying now, and wait in the square'}, 'chance': 0.78}),
 ]},
{'name': 'the long shot becomes a story to tell',
 'stages': 'young_adult adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.15,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'meaning, friends, performing',
 'horizon': 'years',
 'roles': 'friend, partner, child, colleague',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, someone younger asks about it, and the story is there '
                     'to be told',
            'tribal': 'winters after the attempt that failed, a child at the fire asks about it, and the telling is '
                      'there',
            'magic': 'years after the attempt that failed, an apprentice asks about it in the tavern, and the tale '
                     'is there to be told'},
 'timing': {'times': 'per person who missed a stage long shot: about 1 in 5 come to tell it as a story of their own, '
                     'years later, in a class, at a table or to someone younger (estimate)'},
 'after': "a long shot missed in one of the moments of stage-longshots.lib (as for 'the same door, years later'), "
          'holding [a long shot that missed]; now 25 or more and not playing a lead (no [lead actor or actress])',
 'delay_years': (5, 30),
 'likelier': 'years gone by since the attempt; teaching, telling stories or acting kept up; much White and Green in '
             'the color history',
 'rarer': 'stress above 1.5; poor health',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, a young cousin who has just joined the youth theatre '
                       'asks {N} at a family lunch whether it is true that {N} once went for something enormous and '
                       'did not get it. The whole table goes quiet to hear the answer.'),
                      ('W',
                       '{N} tells it straight, the way it happened: what was asked, what {N} did, and the letter '
                       'that said no. There is nothing in it to be ashamed of, and the young ones should know that.'),
                      ('U',
                       'Over the years {N} has understood the day better than at the time: what the people in the '
                       'room were looking for, and what {N} had not yet learned. That is worth passing on.'),
                      ('B',
                       'It has become a good story, and {N} knows it. It gets a laugh in the right place, and people '
                       'remember who told it.'),
                      ('R',
                       'The ache has gone, mostly, and what is left is the memory of the nerve: the morning {N} '
                       'walked in anyway. {N} would not trade it for anything.'),
                      ('G',
                       "It belongs to the family's stories now, somewhere between the grandmother's dance-hall days "
                       "and the uncle's famous fish. {N} likes it there.")],
            'tribal': [('',
                        'At the fire one winter a child asks {N} whether it is true that {N} once walked up to the '
                        'elders and asked for the great mask, and did not get it. The whole hearth goes quiet to '
                        'hear the telling.')],
            'magic': [('',
                       'In the tavern one evening a young apprentice asks {N} whether it is true that {N} once went '
                       "before the master of revels for the hero's part. The table goes quiet to hear the tale.")]},
 'outcomes': (['The story is told, and the young ones listening go off to their own auditions a little braver for '
               'it.',
               'Whatever {N} chose, the long shot sits easily now, a part of the life rather than a hole in it.'],
              ['The telling comes out wrong, too bitter in one place, and {N} lies awake afterwards wishing it had '
               'been said better.',
               'The young one listens politely and goes off to do it differently, and {N} finds, a little to {Ns} '
               'own surprise, that this is fine.']),
 'options': [
    ('drive a younger hopeful to every audition, and cheer from the back of the hall', 'W1', None, 0.45, '', {'mark': 'helped someone in need', 'v': 'benevolence, conformity', 'world': {'tribal': 'walk with a young player to every fire where the elders listen, and cheer from the dark', 'magic': 'take a young hopeful to every trial, and cheer from the back of the hall'}, 'chance': 0.78}),
    ('teach an evening class for adult beginners, and tell them how it really went', 'U1', None, 0.45, '', {'grants': 'teaching', 'habit': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'teach the grown ones who never played, and tell them how it really went', 'magic': 'teach an evening class for grown beginners at the guild hall, and tell them how it really went'}, 'chance': 0.78}),
    ('tell the story at every dinner for years, a little better each time', 'B1', None, 0.45, '', {'grants': 'public speaking', 'v': 'achievement, hedonism', 'world': {'tribal': 'tell the attempt at every fire for years, a little better each winter', 'magic': 'tell the tale at every supper for years, a little better each time'}, 'chance': 0.78}),
    ('join the local players, and play whatever part comes, for the joy of it', 'R1', None, 0.45, '', {'title': 'amateur actor', 'v': 'hedonism, stimulation', 'world': {'tribal': "join the band's own tellings at midwinter, and play whatever part comes", 'magic': "join the guild's mystery players, and play whatever part comes"}, 'chance': 0.78}),
    ('let it rest: frame the letter from that day, and hang it in the hall', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, security', 'world': {'tribal': 'let it rest: hang the token from that day by the hearth', 'magic': 'let it rest: frame the tally from that day, and hang it by the door'}, 'chance': 0.78}),
    ('thank the people who said no, and offer to help at their next open call', 'W1', 'B.7', 0.5, '', {'grants': 'contact in the trade', 'v': 'benevolence, achievement', 'world': {'tribal': 'thank the elders who chose another, and offer to tend the fire at the next gathering', 'magic': 'thank the master who said no, and offer to help at the next trials'}, 'chance': 0.78}),
    ('turn the whole attempt into a short play, and give it to the youth theatre', 'U1', 'R.7', 0.5, '', {'grants': 'writing scripts', 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'make a telling of the attempt, and give it to the children for midwinter', 'magic': "write the attempt into a short play, and give it to the guild's children's company"}, 'chance': 0.78}),
    ('set up a small yearly fund for young hopefuls from the town', 'B1', 'G.7', 0.5, '', {'grants': 'good name in town', 'binds': True, 'v': 'benevolence, power', 'world': {'tribal': 'give a fine hide every summer to the young one who plays best at the fire', 'magic': 'set up a small purse each year for a young hopeful of the ward'}, 'chance': 0.78}),
    ('tell the story to the youth theatre on its first night, nerves and all', 'R1', 'W.7', 0.5, '', {'grants': 'telling a story aloud', 'v': 'benevolence, stimulation', 'world': {'tribal': 'tell the children at the fire before their first telling, nerves and all', 'magic': "tell the guild's children before their first masque, nerves and all"}, 'chance': 0.78}),
    ('sit down with the old letter, and write out what the day taught', 'G1', 'U.7', 0.5, '', {'self_control': '+', 'v': 'tradition, self-direction', 'world': {'tribal': 'sit by the fire with the old token, and put into words what the day taught', 'magic': 'sit with the old letter, and write out what the day taught'}, 'chance': 0.78}),
 ]},
]

EVENTS_READ = [{'name': 'the reviews are in',
  'source': 'career',
  'tone': 'mixed',
  'base': 'need:competence-.03',
  'worlds': {'earth': 'the morning papers and the online notices after the opening',
             'tribal': 'the elders speak of the telling the next morning, and the young ones repeat what they said',
             'magic': 'the broadsheets are cried in the square the morning after the opening'},
  'timing': {'times': 'per actor, director or writer with a show that opens: once a production; most professional '
                      'openings and many amateur ones are reviewed somewhere (estimate)',
             'likelier': 'a professional opening in a city, a reviewer in the house on the first night, a lead part, '
                         'a fringe show in festival week',
             'rarer': 'a small amateur show in a village with no paper of its own, an opening in a week full of '
                      'bigger news',
             'window': (16, 100),
             'gap_years': (1.0, 2.0)},
  'readings': [('a duty done: the work was honest, whatever they wrote',
                'W1',
                1.0,
                'meaning+.05',
                'W',
                '{N} reads the notices once, folds the paper away, and is at the theatre for the half as on any '
                'other night.'),
               ('a lesson: the critic saw what the director missed',
                'U1',
                0.9,
                'competence+.05',
                'U',
                '{N} underlines the one sharp sentence, takes it into the next rehearsal, and changes the way the '
                'second act begins.'),
               ('a game: notices sell tickets, and nothing more',
                'B1',
                0.6,
                'autonomy+.05',
                'B',
                '{N} checks the box office figures before the papers, and has the best line on the posters by '
                'Monday.'),
               ('a wound: one line that will be remembered for years',
                'R1',
                0.6,
                'belonging+.05',
                'R',
                '{N} reads the cruel line over and over, then goes out with the company after the show, and by '
                'midnight they are laughing at it together.'),
               ('the way it goes: the local paper always says the same',
                'G1',
                0.9,
                'safety+.05',
                'G',
                '{N} cuts the notice out for the family scrapbook, good or bad, and puts the kettle on.')],
  'scenes': {'earth': [('',
                        'The morning after the opening, the notices are in: two papers, a website and a long post by '
                        'someone who was in the third row. {N} sits at the kitchen table with a cup of coffee going '
                        'cold, reading them one by one.')],
             'tribal': [('',
                         'The morning after the telling, the elders speak of it by the cooking fires, and by noon '
                         'the young ones are repeating what they said, the kind words and the sharp ones, all '
                         'through the camp.')],
             'magic': [('',
                        'The broadsheets are cried in the square the morning after the opening, and {N} buys all '
                        'three from the boy at the corner and reads them on the playhouse steps.')]}}]

MARKS = {}
