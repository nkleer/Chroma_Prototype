"""Chroma library art: compiled by build.py from art.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'the art room at lunchtime',
 'stages': 'child juvenile',
 'age': (10, 18),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.03,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'school, play, making',
 'horizon': 'week',
 'roles': 'friend, the art teacher, a parent or carer',
 'share': 0.4,
 'share_group': 'art_youth_doors',
 'worlds': {'earth': 'the art teacher leaves the art room open at lunch, with paper, paint, clay and the radio on',
            'tribal': 'at midday the one who teaches the children the marks lays out ochre and charcoal at the flat '
                      'rock',
            'magic': "the drawing master leaves the schoolroom's paint cupboard open through the noon hour"},
 'timing': {'times': 'per child or teenager a year: about 1 in 5 schools keep an art room open at lunch or after '
                     'school, and about 15 lives in 100 keep drawing or painting past school (catalogue share; '
                     'estimate)',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'At lunchtime the art room door is propped open. The art teacher eats a sandwich at the desk '
                       'with the radio on low, and there is paper, paint and a bag of clay for anyone who wants '
                       'them, as long as the brushes are washed before the bell.'),
                      ('W',
                       'A sign on the door gives the rules: aprons on, no food near the paint, brushes washed and '
                       'back in the jar before the bell. {N} likes a room where everyone knows what to do.'),
                      ('U',
                       "On the art teacher's desk lies a book of drawings with every line explained: how the bones "
                       'of a hand sit, where the shadow falls on a face. {N} wants to know how it is done.'),
                      ('B',
                       'The best work from the lunchtime room goes up in the main corridor, where every visitor to '
                       'the school sees it, with a name card underneath. {N} has noticed whose names are there.'),
                      ('R',
                       'The radio is on, the paint is out, and nobody is marking anything. For a whole hour {N} '
                       'could paint anything at all.'),
                      ('G',
                       '{friend} is already at the clay table, rolling coils for a pot, and the window looks out '
                       'over the playing field and the trees. It is the quietest, warmest room in the school.')],
            'tribal': [('',
                        'At midday, while the hunters sleep in the shade, the woman who teaches the children the '
                        'marks lays out ochre, charcoal and a grinding stone at the flat rock. Any child may come '
                        'and paint, if they sweep the rock clean after.')],
            'magic': [('',
                       'Through the noon hour the drawing master leaves the paint cupboard unlocked and sits reading '
                       'by the window. There is paper, chalk, a lump of modelling clay and a jar of good paint, and '
                       'the rule is that everything goes back where it was.')]},
 'outcomes': (['{N} comes back the next day, and the next, with paint under {Ns} fingernails and something to show '
               'for it.',
               'By the end of the season {N} has a pile of work to show, and the one who teaches knows {Ns} name.'],
              ['It is too crowded and too loud, and {N} drifts off and does not come back.',
               'What {N} makes comes out nothing like it looked in {Ns} head, and is thrown away before anyone sees '
               'it.']),
 'options': [
    ('help paint the backdrop for the school play, as the art teacher asked', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'help paint the hides for the midsummer telling, as the woman who teaches the marks asked', 'magic': 'help paint the scenery for the feast-day masque, as the drawing master asked'}, 'chance': 0.85}),
    ("copy the drawings in the art teacher's book, line by line, to see how they work", 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'grants': 'drawing and painting', 'habit': True, 'world': {'tribal': 'copy the old marks on the rock, line by line, to learn how they were made', 'magic': "copy the drawings in the master's pattern book, line by line, to see how they work"}, 'chance': 0.9}),
    ('paint something big and bold for the corridor display, with your name card on it', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'world': {'tribal': 'paint the biggest bison on the flat rock, where the hunters pass on their way out', 'magic': 'paint something bold for the schoolroom wall, where the visiting parents will see it, with your name beneath'}, 'chance': 0.45}),
    ('paint whatever comes into your head for the whole hour, radio up', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'grants': 'drawing and painting', 'habit': True, 'world': {'tribal': 'paint whatever comes into your head on the rock until the shade moves', 'magic': 'paint whatever comes into your head for the whole noon hour'}, 'chance': 0.8}),
    ('build a coil pot at the clay table, the old way, slowly', 'G1', None, 0.45, '', {'v': 'tradition', 'grants': 'sculpting', 'self_control': '+', 'mark': 'learned a skill', 'world': {'tribal': 'shape a bowl from the river clay, coil by coil, the way the grandmothers do', 'magic': 'build a coil pot from the modelling clay, the old way, slowly'}, 'chance': 0.55}),
    ("ask the art teacher for a place in the older pupils' drawing club", 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'grants': 'drawing and painting', 'aims': 'life-drawing regular', 'habit': True, 'mark': 'learned a skill', 'world': {'tribal': 'ask for a place among the older children who draw the animals on the rock', 'magic': "ask the drawing master for a place at the older pupils' drawing evenings"}, 'chance': 0.75}),
    ("enter the school's poster competition with a design worked out in pencil first", 'U1', 'B.7', 0.5, '', {'v': 'achievement', 'world': {'tribal': "work out a pattern in the dust first, then offer it for the band's new drum", 'magic': "enter the school's broadsheet competition with a design worked out in chalk first"}, 'chance': 0.3}),
    ('stay out in the playground: lunch is for football, not more school', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'world': {'tribal': 'stay down at the river: midday is for swimming, not more learning', 'magic': 'stay out in the yard: the noon hour is for games, not more lessons'}, 'chance': 0.95}),
    ('paint the trees outside the window, fast, before the light changes', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'paint the river birds on the rock, fast, before they fly', 'magic': 'paint the elms outside the window, fast, before the light changes'}, 'chance': 0.8}),
    ('stay behind to help the art teacher wash the brushes and wipe the tables', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'stay behind to help sweep the flat rock and grind the ochre for tomorrow', 'magic': 'stay behind to help the drawing master wash the brushes and stopper the paint pots'}, 'chance': 0.85}),
 ]},
{'name': 'a poem for the school magazine',
 'stages': 'child juvenile',
 'age': (10, 18),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.03,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'school, writing, friends',
 'horizon': 'week',
 'roles': 'friend, the literature teacher, a grandparent',
 'share': 0.4,
 'share_group': 'art_youth_doors',
 'worlds': {'earth': 'the literature teacher wants poems for the school magazine, and the best one wins a small '
                     'prize',
            'tribal': 'the elders want new verses from the children for the midsummer gathering',
            'magic': "the schoolmaster wants verses from the pupils for the school's year-end broadsheet"},
 'timing': {'times': 'per child or teenager a year: about 1 in 4 are asked for a poem or a story for a school '
                     'magazine or competition; about 3 lives in 100 keep writing poems past school (catalogue share; '
                     'estimate)',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'The literature teacher pins a notice by the classroom door: poems wanted for the school '
                       'magazine, any subject, any length, by Friday week. The best one goes on the front page and '
                       'wins a small prize, and the magazine goes home to every family in the school.'),
                      ('W',
                       'The notice gives the rules: one poem each, written in class or at home, handed in on time '
                       'with a name on it. {N} likes knowing exactly what is asked.'),
                      ('U',
                       'Last week the literature teacher read the class a poem that rhymed without seeming to, and '
                       '{N} has been trying to work out how it was done ever since.'),
                      ('B',
                       "Last year's front-page poem was by a girl in the year above, and the teachers still mention "
                       'it. Whoever wins this one will be known for it.'),
                      ('R',
                       'There is something {N} has never said to anyone, and it has been sitting in {Ns} chest for '
                       'months. A poem might be the only way to say it.'),
                      ('G',
                       '{grandparent} used to recite long poems by heart at family gatherings, the old ones about '
                       'the hills and the harvest. {N} has always loved the sound of them.')],
            'tribal': [('',
                        'At the new moon the elders call the children together: at the midsummer gathering the '
                        'children will speak verses of their own, and the best will be kept and said again. The old '
                        'ones will be listening.')],
            'magic': [('',
                       'The schoolmaster announces that the year-end broadsheet will print verses from the pupils, '
                       'and the best will be read before the parents on prize day. Paper and ink are to be had from '
                       'his desk.')]},
 'outcomes': (['The poem is chosen, and people {N} barely knows say a line of it back days later.',
               '{N} finds that words can be pushed and turned like clay, and keeps on making them long after.'],
              ['The day comes and goes, and {N} has nothing but crossings-out and half a line.',
               'The poems are chosen, and {Ns} is not among them.']),
 'options': [
    ("write the poem in the form the teacher set, and enter it for the magazine's prize", 'W1', None, 0.45, '', {'v': 'conformity', 'grants': 'writing poems', 'world': {'tribal': "make the verse in the old measure the elders taught, and offer it for the gathering's honour", 'magic': 'write the verse in the form the schoolmaster set, and enter it for the prize'}, 'chance': 0.3}),
    ('count the syllables and redraft the poem until every word is right', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'grants': 'writing poems', 'self_control': '+', 'mark': 'learned a skill', 'world': {'tribal': 'say the verse over and over on the walk to the river, until every word sits right', 'magic': 'count the syllables and redraft the verse until every word is right'}, 'chance': 0.85}),
    ("offer to run the magazine's poetry page, and choose which poems go in", 'B1', None, 0.45, '', {'v': 'power, achievement', 'binds': True, 'world': {'tribal': "ask the elders for the say in which children's verses are spoken at the gathering", 'magic': "offer to edit the broadsheet's verse column, and choose which verses go in"}, 'chance': 0.45}),
    ('ask to read your poem aloud in assembly, though your hands are shaking', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'grants': 'writing poems', 'aims': 'open-mic poet', 'identity': True, 'mark': 'took a wild risk', 'world': {'tribal': 'stand up at the fire and speak your verse to the whole band, though your voice shakes', 'magic': 'ask to read your verse aloud before the whole school, though your hands are shaking'}, 'chance': 0.45}),
    ('write about the street, the farm or the grandparent you know best', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'grants': 'writing poems', 'world': {'tribal': 'make a verse about the old camp by the river, and the grandmother who knows every song', 'magic': 'write about the lane, the farm or the grandparent you know best'}, 'chance': 0.8}),
    ('ask the literature teacher for a book of poems, to learn how they are made', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'door': True, 'world': {'tribal': 'ask the old teller to say the oldest verses again, to learn how they are made', 'magic': 'ask the schoolmaster for a book of verse, to learn how it is made'}, 'chance': 0.9}),
    ('write a clever story instead, with an ending the whole class will talk about', 'U1', 'B.7', 0.5, '', {'v': 'achievement, self-direction', 'grants': 'writing stories', 'world': {'tribal': 'make up a telling instead, with an ending the children will talk about for days', 'magic': 'write a clever tale instead, with an ending the whole schoolroom will talk about'}, 'chance': 0.75}),
    ('say poems are for other people, and keep the evenings for games', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'world': {'tribal': 'say verses are for other children, and keep the evenings for games by the river', 'magic': 'say verse is for other pupils, and keep the evenings for games in the yard'}, 'chance': 0.95}),
    ("write a poem for a friend's birthday instead, and give it in a card", 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'made a friend', 'world': {'tribal': "make a verse for your hearth-friend's naming day instead, and say it to them alone", 'magic': "write a verse for a friend's name-day instead, and give it on a folded paper"}, 'chance': 0.75}),
    ("write the verse for the old caretaker's leaving card, for the whole school", 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'make a verse for the old hunter who can hunt no longer, for the whole band to say', 'magic': "write the verse for the old porter's leaving gift, for the whole school"}, 'chance': 0.6}),
 ]},
{'name': 'the evening class at the college',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.02,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'leisure, making, community',
 'horizon': 'months',
 'roles': 'friend, colleague, partner, the class tutor',
 'share': 0.06,
 'share_group': 'art_adult_doors',
 'worlds': {'earth': "the college's prospectus: life drawing, Tuesday evenings, ten weeks, all levels",
            'tribal': "the band's painters climb to the painting place in the evenings, and anyone may sit and draw "
                      'with them',
            'magic': "the academy's evening hall opens its drawing class to townsfolk: ten evenings, a small fee, "
                     'all levels'},
 'timing': {'times': 'per adult a year: about 1 in 30 see an evening art class they could join; about 15 lives in '
                     '1,000 draw at a weekly class for a year or more (catalogue share; estimate)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       "The college's evening prospectus comes through the door with the free paper: life drawing, "
                       'Tuesday evenings, seven till nine, ten weeks, all levels welcome, materials provided the '
                       'first night. A paid model holds each pose while the room draws in silence, and a tutor goes '
                       'round the easels.'),
                      ('W',
                       'The course has a clear shape: a register, a tutor, short poses in the first weeks and longer '
                       'ones by the end. {N} likes the idea of a class that builds week by week, and of keeping to '
                       'it.'),
                      ('U',
                       '{N} has always drawn heads and hands badly and wondered why. Ten weeks with a tutor who '
                       'explains how the weight falls and where the light sits would answer that.'),
                      ('B',
                       'The tutor shows at a gallery in town and knows the people who buy. Drawing well enough to '
                       'sell would be something, and every artist {N} has read about drew from life.'),
                      ('R',
                       '{N} used to draw all the time, at the back of every lesson, and stopped somewhere along the '
                       'way without ever deciding to. The page in the prospectus makes {Ns} hand itch.'),
                      ('G',
                       'The college is the old building by the river where {parent} once went to evening classes '
                       'too. The drawing room has tall windows, and people of every age go there, year after year.')],
            'tribal': [('',
                        "When the hunters come back in the evening, the band's painters climb to the painting place "
                        'with charcoal and ochre and draw the animals, and each other, on the smooth rock. Anyone '
                        'may sit with them who brings a lamp and keeps quiet.')],
            'magic': [('',
                       "A notice at the academy gate: this season the evening hall's drawing class is open to "
                       'townsfolk, ten evenings, a small fee, a master going round the easels. The candles are lit '
                       'at the seventh bell, and the sitter is paid by the night.')]},
 'outcomes': (['Within a month {N} has a folder of drawings, a regular seat, and people who nod hello every week.',
               'Somewhere around the sixth week the lines start to do what {N} means them to.'],
              ['Too few sign up, the class is cancelled, and {N} never quite gets round to finding another.',
               '{N} goes twice, finds every drawing worse than the last, and stops going.']),
 'options': [
    ('enrol for all ten weeks, pay in full, and never miss a Tuesday', 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'life-drawing regular', 'habit': True, 'self_control': '+', 'world': {'tribal': "ask the painters' leave, and climb to the painting place every evening without fail", 'magic': 'enrol for all ten evenings, pay the fee in full, and never miss one'}, 'chance': 0.65}),
    ('buy the materials and a book on drawing the figure, and work at home', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'grants': 'drawing and painting', 'world': {'tribal': 'gather charcoal and a smooth hide, and practise the figure alone by your own fire', 'magic': 'buy chalk, paper and a book on drawing the figure, and work at home by candlelight'}, 'chance': 0.65}),
    ('enrol, set up at the front, and make sure the tutor sees your best work', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'life-drawing regular', 'habit': True, 'world': {'tribal': 'sit at the painting place where the best painter can see your marks', 'magic': 'enrol, take the easel nearest the master, and make sure the master sees your best work'}, 'chance': 0.65}),
    ('turn up on the first Tuesday without booking, and draw as fast as the poses change', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'life-drawing regular', 'world': {'tribal': 'climb up that very evening unasked, and draw as fast as the light allows', 'magic': 'turn up on the first evening without enrolling, and draw as fast as the poses change'}, 'chance': 0.65}),
    ('draw the people at the bus stop and in the café, as you always have', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'habit': True, 'world': {'tribal': 'draw the band at their work by the shelters, as you always have', 'magic': 'draw the people in the market and at the well, as you always have'}, 'chance': 0.7}),
    ('ask for the cheaper rate, with every form filled in properly', 'W1', 'B.7', 0.5, '', {'v': 'security, power', 'aims': 'life-drawing regular', 'world': {'tribal': 'offer the painters a share of your ochre for a place, by the old custom', 'magic': 'ask for the reduced fee, with every paper sealed properly'}, 'chance': 0.75}),
    ('go to the one-night taster first, and find out whether it suits', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'sit at the edge of the painting place for one evening, and find out whether it suits', 'magic': "go to the academy's open evening first, and find out whether it suits"}, 'chance': 0.7}),
    ("say no: the overtime on Tuesdays pays for the family's holiday", 'B1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'self_control': '+', 'mark': 'turned down a chance', 'world': {'tribal': 'say no: the evenings are for setting snares, and the children need the meat', 'magic': "say no: the evening work at the shop pays for the family's winter"}, 'chance': 0.85}),
    ('talk three friends from work into joining, so the class has enough to run', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, stimulation', 'binds': True, 'world': {'tribal': 'rouse three friends to climb up together, so the painters make room for newcomers', 'magic': 'talk three friends from the shop into enrolling, so the class has enough to run'}, 'chance': 0.65}),
    ('enrol with an old school friend, and learn it side by side', 'G1', 'U.7', 0.5, '', {'v': 'benevolence, self-direction', 'title': 'life-drawing regular', 'binds': True, 'world': {'tribal': 'climb up with your oldest friend, and learn the marks side by side', 'magic': 'enrol with a friend from the old schoolroom, and learn it side by side'}, 'chance': 0.65}),
 ]},
{'name': 'the poetry night at the back of the pub',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 90),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.02,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'leisure, writing, community',
 'horizon': 'months',
 'roles': 'friend, neighbour, the host, a regular',
 'share': 0.06,
 'share_group': 'art_adult_doors',
 'worlds': {'earth': 'a chalkboard by the bar: open mic, poets welcome, first Thursday',
            'tribal': "on the long nights anyone may stand at the band's fire and speak verses",
            'magic': "the tavern on the square holds a poets' night on the first of the month, and anyone may read"},
 'timing': {'times': 'per adult a year: about 1 in 30 come across a poetry or spoken-word night they could read at; '
                     'about 1 life in 100 reads at one again and again (catalogue share; estimate)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A chalkboard by the bar of the pub on the corner: open mic, poets welcome, first Thursday of '
                       'the month, back room, sign up by eight. Through the doorway there are thirty chairs, a '
                       'microphone on a stand, and a woman reading from a notebook while the whole room listens.'),
                      ('W',
                       'The rules are chalked up under the date: five minutes each, names on the list by eight, no '
                       'talking during a reading, applause for everyone. {N} likes that it is fair, and that '
                       'everyone gets a turn.'),
                      ('U',
                       '{N} stands in the doorway and listens to how the readers do it: where they pause, how they '
                       'hold a line back for the end. There is a craft to it, and {N} wants to learn it.'),
                      ('B',
                       "The host runs the town's writing festival, and a small press sells pamphlets from a table by "
                       'the door. People who read well here get asked to read elsewhere.'),
                      ('R',
                       'A young man is reading about his father, and his voice cracks, and the room goes completely '
                       'still. {N} has notebooks full of things like that at home.'),
                      ('G',
                       'Half the room are regulars who have come every month for years, and the landlady knows them '
                       'all by name. The poems are about the town, the river, the old mill, and people {N} has known '
                       'all {Ns} life.')],
            'tribal': [('',
                        'On the long nights, when the meat is eaten, the band sits close round the fire and anyone '
                        'may stand and speak verses: about the hunt, the dead, the river in flood. The old ones nod '
                        'when a verse is good, and say it back.')],
            'magic': [('',
                       "On the first of the month the tavern on the square clears its back room for the poets' "
                       "night. A bell marks each reader's time, the landlord keeps the list, and the academy's "
                       'students sit at the back with their own pages.')]},
 'outcomes': (['{Ns} name goes on the list, and by the third month the regulars save {N} a seat.',
               'The room goes quiet in the right place, and afterwards a stranger asks to hear it again.'],
              ['On the night {N} sits through every reader and leaves without once standing up.',
               '{N} reads too fast, loses a line in the middle, and goes home certain never to go back.']),
 'options': [
    ('sign the list by eight, keep to the five minutes, and come back every month', 'W1', None, 0.45, '', {'v': 'conformity, tradition', 'title': 'open-mic poet', 'identity': True, 'world': {'tribal': 'wait your turn at the fire, speak no longer than the others, and stand again every long night', 'magic': "put your name on the landlord's list, keep to the bell, and come back every month"}, 'chance': 0.65}),
    ('go and listen only, month after month, and learn how the readers hold the room', 'U1', None, 0.45, '', {'v': 'self-direction', 'door': True, 'world': {'tribal': 'sit and listen only, night after night, and learn how the old ones hold the fire', 'magic': 'sit at the back and listen, month after month, and learn how the readers hold the tavern'}, 'chance': 0.8}),
    ("read the strongest poem you have, then ask the host about the town's festival", 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'open-mic poet', 'door': True, 'world': {'tribal': 'speak your strongest verse, then ask the old ones about speaking at the great gathering', 'magic': "read your strongest verse, then ask the landlord about reading at the academy's festival"}, 'chance': 0.65}),
    ('put your name down on the spot, and read the poem folded in your pocket', 'R1', None, 0.45, '', {'v': 'stimulation', 'title': 'open-mic poet', 'world': {'tribal': 'stand up at once and speak the verse carried in your head all winter', 'magic': 'put your name down on the spot, and read the verse folded in your pocket'}, 'chance': 0.65}),
    ('say no: the poems are for the kitchen table, not a microphone', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'say no: your verses are for your own hearth, not the whole band', 'magic': "say no: your verses are for the family's table, not a tavern"}, 'chance': 0.8}),
    ('offer to keep the list and ring the bell for the host, and meet every reader', 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'aims': 'open-mic poet', 'binds': True, 'world': {'tribal': 'offer to tend the fire on the long nights, and come to know every speaker', 'magic': "offer to keep the landlord's list and ring the bell, and come to know every reader"}, 'chance': 0.75}),
    ('rewrite one poem for the ear, then read it on the night', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'title': 'open-mic poet', 'world': {'tribal': 'shape one verse for the ear on the long walks, then speak it at the fire', 'magic': 'rewrite one verse for the ear, then read it at the tavern'}, 'chance': 0.65}),
    ("talk the landlord into a ticketed night of the town's old stories and songs", 'B1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'talk the elders into a night at the fire for the oldest songs, with a share of the meat for the speakers', 'magic': "talk the landlord into a paying night of the quarter's old tales and songs"}, 'chance': 0.65}),
    ('read the poem of a friend who is too shy to stand up and read it', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'helped someone in need', 'world': {'tribal': 'speak the verse of a friend who is too shy to stand at the fire', 'magic': 'read the verse of a friend who is too shy to stand up and read it'}, 'chance': 0.85}),
    ("join the library's poetry workshop, with the old regulars who have gone for years", 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'grants': 'writing poems', 'door': True, 'world': {'tribal': 'sit with the old makers of verses at their own fire, where they have sat for years', 'magic': 'join the circle of old verse-makers who meet at the guild hall, as they have for years'}, 'chance': 0.65}),
 ]},
{'name': "a dealer asks for a painting in a dead master's hand",
 'stages': 'young_adult adult mature elder',
 'age': (20, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.01, 0.005),
 'drivers': 'prosper+.2 money-.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, friend, colleague, rival',
 'requires': 'painter or sculptor | illustrator for hire | gallery owner',
 'worlds': {'earth': "a dealer wants a painting in a dead master's hand, signed with the master's name, for a buyer "
                     'who will not ask',
            'tribal': "a trader in carvings at the gathering wants a carving in a dead master carver's hand, with "
                      "the dead one's sign cut on it",
            'magic': "a picture dealer on the square wants a canvas in a dead court painter's hand, under the dead "
                     "painter's seal"},
 'timing': {'times': 'per painter, illustrator or gallery owner a year: about 1 in 80 is asked, plainly or with a '
                     "wink, to make or pass on a picture in a dead master's manner as the master's own; the three "
                     'careers are about 4 lives in 1,000 (catalogue shares), so about 1 life in 2,000 ever meets it '
                     '(estimate); museum and auction-house studies find that a real share of the works they test are '
                     'not by the hand on the label',
            'likelier': 'a booming art market, a painter with a gift for other hands, debts, a dealer with buyers '
                        'far away who ask few questions',
            'rarer': 'a painter with a name of their own, a small town far from the trade, a dealer who has been '
                     'caught before',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       '{boss}, a dealer who has sold a few of {Ns} pictures, closes the door of the back room and '
                       'opens a catalogue on the table: a small landscape by a painter dead these sixty years. There '
                       'is a buyer, {boss} says, who wants another one and will pay what a real one fetches. Nobody '
                       'needs to know who held the brush.'),
                      ('W',
                       'A signature is a promise about who made the thing. {N} looks at the catalogue and thinks of '
                       'every buyer who ever trusted one.'),
                      ('U',
                       '{N} could do it. The dead painter laid in the sky first and dragged the trees wet into it; '
                       '{N} saw that in a museum years ago and has never forgotten. It would be a fascinating '
                       'problem, and a crime.'),
                      ('B',
                       'The fee is more than {N} has earned from painting in three years. {N} weighs the offer, and '
                       'what {boss} would owe afterwards.'),
                      ('R',
                       '{Ns} face burns. Years of making work that is truly {Ns} own, and this is what it comes to: '
                       'a good copy of somebody else.'),
                      ('G',
                       'The painter in the catalogue is buried in a village churchyard, and the grandchildren still '
                       'live in the house where the landscapes were painted. {N} thinks of them.')],
            'tribal': [('',
                        'At the great gathering a trader in carvings draws {N} behind the hide shelters and unwraps '
                        'a small bone horse, cut by a master carver dead these many winters. A trader from the far '
                        'rivers wants another, and will give a whole canoe of flints for it. Nobody needs to know '
                        'whose hands cut it.')],
            'magic': [('',
                       '{boss}, a picture dealer with a hall on the square, closes the shutters and unrolls a small '
                       'canvas by a court painter dead these sixty years. A lord in the north wants another, under '
                       "the dead painter's seal, and will pay what a true one fetches. Nobody needs to know who held "
                       'the brush.')]},
 'outcomes': (["The matter is settled the way {N} meant it to be, and {N} can walk past the dealer's window without "
               'looking away.',
               'A month later the money, the picture and the trouble are where {N} wanted them, and the studio is '
               'quiet again.'],
              ['Word of the back-room offer gets round the trade, and for a season some doors close to {N} without a '
               'reason given.',
               'It goes wrong from the first week, and {boss} makes sure the trade hears {Ns} name in the wrong '
               'way.']),
 'options': [
    ('paint it as an honest copy, marked as one on the back and the bill', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': "cut it as an honest copy, with your own sign beside the dead master's", 'magic': 'paint it as an honest copy, marked as one on the back and the bill of sale'}, 'chance': 0.7}),
    ("copy the master's sky for the studio wall, only to learn how it was built", 'U1', None, 0.45, '', {'mark': 'learned a skill', 'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': "cut a copy of the master's horse for your own shelter, only to learn how it was made"}, 'chance': 0.7}),
    ('say no, but keep a written note of the offer to hold over the dealer', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': "say no, but remember every word of the trader's offer, to use one day", 'magic': 'say no, but keep a witnessed note of the offer to hold over the dealer'}, 'chance': 0.85}),
    ('tell the dealer what the offer is worth, loudly, in front of the customers', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation, universalism', 'world': {'tribal': 'tell the trader what the offer is worth, loudly, in front of the whole gathering'}, 'chance': 0.8}),
    ("tell the dead painter's family what the dealer is planning", 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': "tell the dead carver's kin what the trader is planning", 'magic': "tell the dead painter's heirs what the dealer is planning"}, 'chance': 0.65}),
    ("paint it in the master's hand, sign the dead name, and take the fee", 'U.5 B.5', None, 0.5, '', {'grants': 'savings', 'takes_if_fails': 'a name in the art world', 'mark': 'hid a wrong', 'closed': "law: forging a dead painter's work and name; backfire: an expert finds a modern pigment under the varnish, the dealer is arrested and names the painter", 'self_control': '-', 'v': 'power, achievement', 'world': {'tribal': "cut it in the dead master's hand, cut the dead one's sign, and take the flints", 'magic': "paint it in the master's hand, set the dead painter's seal on it, and take the fee"}, 'chance': 0.66}),
    ('report the dealer to the police, with a note of every word that was said', 'W.5 U.5', None, 0.5, '', {'mark': 'made an enemy', 'identity': True, 'v': 'conformity, universalism', 'world': {'tribal': 'tell the elders of the gathering every word the trader said', 'magic': 'report the dealer to the city watch, with a note of every word that was said'}, 'chance': 0.66}),
    ("warn the other painters in town about the dealer's back-room work", 'W.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'universalism, benevolence', 'world': {'tribal': "warn the other carvers at the gathering about the trader's offer", 'magic': "warn the painters' guild about the dealer's back-room work"}, 'chance': 0.66}),
    ('turn the money talk round, and ask for a show of your own work instead', 'B.5 R.5', None, 0.5, '', {'grants': 'a dealer who sells your work', 'aims': 'painter or sculptor', 'door': True, 'v': 'power, achievement', 'world': {'tribal': 'turn the trading talk round, and ask the trader to carry your own carvings instead', 'magic': "turn the money talk round, and ask for a showing of your own work in the dealer's hall"}, 'chance': 0.36}),
    ('laugh it off, and paint the dead master a tribute under your own name', 'R.5 G.5', None, 0.5, '', {'habit': True, 'v': 'stimulation, tradition', 'world': {'tribal': 'laugh it off, and cut the dead master a horse of your own, under your own sign'}, 'chance': 0.76}),
 ]},
{'name': "a friend's secret would make the book",
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.02, 0.02, 0.01),
 'drivers': 'ties+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'friend, boss, partner, colleague',
 'requires': 'novelist | open-mic poet',
 'worlds': {'earth': 'the best chapter of the book is a story a friend told in trust, years ago',
            'tribal': 'the best part of the long telling is something a friend told at a low fire, years ago, in '
                      'trust',
            'magic': 'the best chapter of the book is a story a friend told in trust, years ago, in a tavern corner'},
 'timing': {'times': 'per novelist or open-mic poet a year: about 1 in 50 finds that the best thing in the book or '
                     'the poems is a story a friend told in trust (estimate); the two titles are about 1 life in 100 '
                     "(catalogue shares), so about 1 life in 200 meets it; writers' memoirs and the law reports both "
                     "show how often a friend or a relative finds themselves in someone's book",
            'likelier': 'a first book drawn from life, a long friendship, a story nobody else knows, an editor who '
                        'wants the book to be braver',
            'rarer': 'a writer of thrillers or fantasy, a friend long dead and without family, a writer who keeps '
                     'work and friends apart',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'The book has been stuck for a year, and then one night {N} sees it: the story {friend} told '
                       'years ago and has told nobody since, of the months spent leaving the house every morning in '
                       'a suit after the job was gone. It is the heart the book has been missing. {friend} is still '
                       '{Ns} closest friend.'),
                      ('W',
                       '{friend} told it in trust, and said that {N} was the only one who would ever know. A promise '
                       'does not stop being one because a book needs it.'),
                      ('U',
                       'Told straight it would be the best chapter {N} has ever written. Changed enough, it might '
                       'still be; {N} turns over how much a story can be changed before it stops being true.'),
                      ('B',
                       'An editor has said the book needs one more true, hard thing. This is that thing, and {N} '
                       'knows exactly what it would do for the book.'),
                      ('R',
                       '{N} cannot stop writing it. The scene arrives whole, at three in the morning, and it is the '
                       'truest thing {N} has ever put on a page.'),
                      ('G',
                       'Thirty years of friendship: the weddings, the funerals, the long walks. {N} thinks of '
                       '{friend} reading the book in the chair by the window.')],
            'tribal': [('',
                        'The long telling has lacked its heart all winter, and now {N} knows what it is: the thing '
                        '{friend} told at a low fire years ago, about the hunt where {friend} ran, and has told '
                        'nobody since. It would hold the whole band silent.')],
            'magic': [('',
                       'The book has stalled for a year, and now {N} sees what it lacks: the story {friend} told '
                       'years ago in a tavern corner, of the season spent pretending to go to the counting house '
                       'after the post was lost. It is the heart the book has been missing.')]},
 'outcomes': (['The book goes to the publisher in the spring, and {friend} is at the launch, raising a glass in the '
               'second row.',
               'Whatever {N} chose, the book is finished at last, and the friendship comes through it.'],
              ['The book comes out, and a month later a short letter arrives from {friend}, and then nothing for a '
               'long time.',
               'The chapter never comes right whichever way {N} turns it, and the book goes back into the drawer.']),
 'options': [
    ('leave it out: a secret told in trust stays a secret', 'W1', None, 0.45, '', {'mark': 'kept your word', 'v': 'conformity, benevolence', 'world': {'tribal': 'leave it out of the telling: what was told at a low fire stays there'}, 'chance': 0.77}),
    ('change it beyond knowing: another town, another age, another life', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'change it beyond knowing: another band, another valley, another winter', 'magic': 'change it beyond knowing: another city, another reign, another life'}, 'chance': 0.7}),
    ("offer the friend a share of the book's money for the right to use it", 'B1', None, 0.45, '', {'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'offer the friend a share of every gift the telling brings, for the right to tell it'}, 'chance': 0.7}),
    ('put it in word for word, because the book is truer with it', 'R1', None, 0.45, '', {'mark': 'broke your word', 'closed': "approval: a friend's secret put in print; backfire: the friend reads it in the first week, and does not speak to the writer again", 'self_control': '-', 'v': 'stimulation, self-direction', 'world': {'tribal': 'tell it word for word at the gathering, because the telling is truer with it'}, 'chance': 0.82}),
    ('write it as one poem for the friend alone, and keep it out of the book', 'G1', None, 0.45, '', {'self_control': '+', 'v': 'benevolence, tradition', 'world': {'tribal': 'make it a verse for the friend alone, and keep it out of the telling'}, 'chance': 0.72}),
    ('put it in, and tell the friend face to face before the book comes out', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'owned up', 'closed': "approval: a friend's secret put in print without leave, though with warning; backfire: the friend begs for it to come out, and when it stays in, the friendship ends in front of everyone they share", 'v': 'universalism, stimulation', 'world': {'tribal': 'put it in the telling, and tell the friend face to face before the gathering'}, 'chance': 0.55}),
    ('ask the friend first, and cut whatever they ask to be cut', 'W.34 U.33 G.33', None, 0.5, '', {'binds': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'ask the friend first, and leave out whatever the friend asks'}, 'chance': 0.65}),
    ('agree in writing with the friend what may go in, and keep to it', 'W.34 B.33 R.33', None, 0.5, '', {'binds': True, 'v': 'security, power', 'world': {'tribal': 'agree with the friend before the elders what may be told, and keep to it', 'magic': 'agree under seal with the friend what may go in, and keep to it'}, 'chance': 0.7}),
    ('keep the pages in a drawer, for a book written years from now', 'U.34 B.33 G.33', None, 0.5, '', {'self_control': '+', 'v': 'security, tradition', 'world': {'tribal': 'keep the story to yourself for many winters, for a telling far ahead', 'magic': 'keep the pages locked in a chest, for a book written years from now'}, 'chance': 0.9}),
    ('ask the friend to write that chapter in their own words, under their own name', 'B.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'benevolence, self-direction', 'world': {'tribal': "ask the friend to tell that part at the fire, in the friend's own voice"}, 'chance': 0.5}),
 ]},
{'name': "the idea in someone else's sketchbook",
 'stages': 'young_adult adult mature',
 'age': (17, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.02, 0.01, 0.0),
 'drivers': 'community+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'week',
 'roles': 'friend, mentor, colleague, rival',
 'requires': 'art school student | illustrator for hire | painter or sculptor | street artist',
 'worlds': {'earth': "a friend's sketchbook left open on the studio table, with the idea in it",
            'tribal': "a friend's marking stone left by the fire, with a new way of drawing the running deer "
                      'scratched on it',
            'magic': "a friend's sketchbook left open on the academy's long table, with the idea in it"},
 'timing': {'times': 'per art student, illustrator, painter or street artist a year: about 1 in 40 sees in a '
                     "friend's sketchbook, or on a shared studio wall, the idea they have been circling, done first "
                     '(estimate); the four titles are about 2 lives in 100 (catalogue shares), so about 1 life in '
                     '400 meets it; arguments over who had an idea first are as old as shared studios and art '
                     'schools',
            'likelier': 'a shared studio or a crowded art school, a friend a little ahead, a deadline close, a brief '
                        'that both are working on',
            'rarer': 'a painter who works alone, a friend with a very different style, the later years of a career',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       '{friend} has gone out for coffee and left the sketchbook open on the studio table. On the '
                       'page is the idea {N} has been circling for a year, the one that would make the end-of-year '
                       'piece, done in six quick drawings and better than {N} ever got it.'),
                      ('W',
                       '{N} should not have looked, and knows it. Whatever happens next, it has to start with that.'),
                      ('U',
                       "{N} studies the six drawings for a long time. The friend's version is good; it is also only "
                       'one of the ways the idea could go.'),
                      ('B', 'Nobody saw {N} look. The show is in three weeks, and {friend} works slowly.'),
                      ('R',
                       'Something between envy and joy goes through {N}. It is a wonderful idea, and it is not '
                       '{Ns}.'),
                      ('G',
                       'Ideas drift round a studio like seeds on the wind, and nobody knows whose they were first. '
                       "Still, it is {Ns} friend's book, open on the table.")],
            'tribal': [('',
                        '{friend} has gone down to the river and left a marking stone by the fire. Scratched on it '
                        'is a new way of drawing the running deer, the way {N} has tried to find for two winters, '
                        'and it is right.')],
            'magic': [('',
                       "{friend} has gone out to the bakery and left the sketchbook open on the academy's long "
                       'table. On the page is the idea {N} has chased all year, done in six quick drawings and '
                       'better than {N} ever got it.')]},
 'outcomes': (['By the end of the term the idea has found its way onto a wall, and {N} and {friend} still share a '
               'table in the studio.',
               'Whatever {N} chose, the show opens with work {N} can stand beside without flinching.'],
              ['The show opens, and {friend} looks from one wall to the other for a long moment and then leaves '
               'early.',
               'Three weeks are not enough, nothing comes right, and {N} hangs an old piece and feels the lack of it '
               'all evening.']),
 'options': [
    ('tell the friend the sketchbook lay open, and what was seen in it', 'W1', None, 0.45, '', {'mark': 'owned up', 'v': 'conformity, universalism', 'world': {'tribal': 'tell the friend the marking stone was seen, and what was on it'}, 'chance': 0.73}),
    ("push your own idea further, until it no longer needs the friend's", 'U1', None, 0.45, '', {'mark': 'learned a skill', 'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': "work your own marks further, until they no longer need the friend's"}, 'chance': 0.68}),
    ('tell the friend the idea could sell, and offer to find the buyer', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'tell the friend the marks could be traded, and offer to find the trader'}, 'chance': 0.75}),
    ('close the sketchbook, and make something wholly your own that night', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'turn the stone face down, and paint something wholly your own that night'}, 'chance': 0.73}),
    ("make the piece from the friend's idea, and let it grow as your own", 'G1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "approval: an idea taken from a friend's sketchbook; backfire: the friend sees the piece at the show, and the whole studio knows whose idea it was", 'self_control': '-', 'v': 'universalism, achievement', 'world': {'tribal': "paint the running deer the friend's way, and let the band think it your own"}, 'chance': 0.7}),
    ("make the piece, with the friend's name beside your own on the label", 'W.34 U.33 B.33', None, 0.5, '', {'self_control': '-', 'v': 'conformity, achievement', 'world': {'tribal': 'paint it, and tell the band at the fire whose marks it grew from'}, 'chance': 0.75}),
    ('ask the friend to make it together, as one piece with both names', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'made a friend', 'door': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'ask the friend to paint it together, side by side on the same rock'}, 'chance': 0.6}),
    ('urge the friend to enter it for the open show, and help pay the fee', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, security', 'world': {'tribal': "urge the friend to show the marks at the gathering, and carry the friend's paints there", 'magic': "urge the friend to enter it for the academy's open show, and help pay the fee"}, 'chance': 0.65}),
    ('leave a note in the sketchbook: this one is good, make it', 'U.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': "leave a sign of praise scratched beside the friend's marks"}, 'chance': 0.85}),
    ('make an answer to it, and hang both side by side at the show', 'U.34 B.33 R.33', None, 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'paint an answer to it, and show both side by side at the gathering'}, 'chance': 0.55}),
 ]},
{'name': 'an advert wants your style',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.03, 0.02, 0.01),
 'drivers': 'prosper+.3 era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, friend, colleague, neighbour',
 'requires': 'street artist | illustrator for hire | painter or sculptor | renowned artist',
 'worlds': {'earth': "a big firm wants an artist's style for a year of adverts",
            'tribal': "a trading clan from downriver wants an artist's painted patterns on every pot it trades",
            'magic': "a merchant house wants an artist's style on its shop signs and its printed bills for a year"},
 'timing': {'times': 'per street artist, illustrator or painter a year: about 1 in 30 is asked by a firm or its '
                     'agency to lend their style to an advert, a shop front or a product (estimate); the three '
                     'careers are about 4 lives in 1,000 (catalogue shares), so about 1 life in 1,000 meets it; '
                     'advertising has borrowed from street art and illustration for as long as both have existed, '
                     'sometimes without asking',
            'likelier': 'a style that has gone round online, a mural in a busy street, good years for advertising, a '
                        'name in the art world',
            'rarer': 'a painter known only to a few collectors, a style too strange to sell things, lean years',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The email comes from an agency: a big firm that makes soft drinks wants {Ns} style for a '
                       'year of adverts, on the sides of buses and on screens in the stations. The walls, the '
                       'lettering, the faces: all of it, in {Ns} hand. The fee is more than {N} has earned in the '
                       'last two years together.'),
                      ('W',
                       'A contract is only as good as what it says. {N} reads the attachment twice, looking for '
                       'where the work would end up, and for how long.'),
                      ('U',
                       '{N} can see three ways to answer the brief, and one way to turn it inside out so that the '
                       'advert becomes something else entirely.'),
                      ('B',
                       'The figure in the email is real money. {N} wonders what the firm would pay if asked, and '
                       'what the name would be worth after a year on every bus.'),
                      ('R',
                       'The style came from nights on cold walls with friends, painting what the street needed to '
                       'see. {N} reads the email aloud to {friend} and they both start laughing.'),
                      ('G',
                       '{N} learned to paint on the shutters of the street where {N} grew up. The neighbours still '
                       'stop to look at those walls. {N} thinks of them seeing the same faces selling soft drinks.')],
            'tribal': [('',
                        'A trading clan from downriver has sent its headman with gifts: the clan wants {Ns} painted '
                        "patterns on every pot it trades, so the bands downriver will know the clan's pots by them. "
                        'The gifts are more than {Ns} hearth has had in two winters.')],
            'magic': [('',
                       'A merchant house has sent its factor with a letter: it wants {Ns} style on its shop signs '
                       'and its printed bills for a year, in every town on the river. The fee is more than {N} has '
                       'earned from painting in two years.')]},
 'outcomes': (['The year turns out the way {N} wanted, and the work, whoever paid for it, still looks like {Ns} own.',
               'Whatever {N} chose, {N} can look the neighbours in the eye when the buses go past.'],
              ["The firm's lawyers rewrite everything at the last minute, and the year goes sour in a slow, "
               'expensive way.',
               'The agency goes to another artist with a style a little like {Ns}, and by the summer it is on every '
               'bus anyway.']),
 'options': [
    ('say yes, on a contract listing every place the work may appear', 'W1', None, 0.45, '', {'grants': 'savings', 'v': 'conformity, security', 'world': {'tribal': 'agree, but only for the pots the clan names before the elders', 'magic': 'say yes, on a sealed contract listing every place the work may appear'}, 'chance': 0.66}),
    ('license the style for one year and one product, and keep every right', 'U1', None, 0.45, '', {'grants': 'royalties', 'v': 'achievement, security', 'world': {'tribal': 'let the clan use the patterns for one summer and one kind of pot, and keep the rest', 'magic': 'license the style to the merchant house for one year and one ware'}, 'chance': 0.73}),
    ('take the money, and push the fee up before signing', 'B1', None, 0.45, '', {'grants': 'savings', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': "take the clan's gifts, and ask for more before agreeing", 'magic': "take the merchant's gold, and push the fee up before signing"}, 'chance': 0.71}),
    ('turn it down, and paint the offer letter into the next wall as a joke', 'R1', None, 0.45, '', {'mark': 'turned down a chance', 'v': 'stimulation, hedonism', 'world': {'tribal': 'turn it down, and paint the trading clan as fat ducks on the shelter wall', 'magic': "turn it down, and paint the merchant's letter into the next wall as a joke"}, 'chance': 0.74}),
    ('take it, and give the fee to the community centre where it all started', 'G1', None, 0.45, '', {'grants': 'good name in town', 'identity': True, 'v': 'benevolence, tradition', 'world': {'tribal': "take the gifts, and share them out among the band's old ones", 'magic': "take it, and give the fee to the ward's hall where it all started"}, 'chance': 0.66}),
    ('say no, and write an open letter about who owns a style', 'W.34 U.33 R.33', None, 0.5, '', {'identity': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'say no, and tell every fire whose patterns these are', 'magic': 'say no, and post a letter on the guild hall door about who owns a style'}, 'chance': 0.65}),
    ('ask the neighbours who helped paint the walls, and do what they decide', 'W.34 U.33 G.33', None, 0.5, '', {'door': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'ask the band whose shelter walls taught the patterns, and do what it decides', 'magic': 'ask the quarter whose walls taught the style, and do what it decides'}, 'chance': 0.7}),
    ('send the firm to a younger artist who needs the work more', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, security', 'world': {'tribal': 'send the trading clan to a younger painter who needs the gifts more', 'magic': 'send the merchant house to a younger painter who needs the work more'}, 'chance': 0.75}),
    ('make the advert a work of its own that quietly mocks the product', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'following online', 'mark': 'took a wild risk', 'v': 'stimulation, achievement', 'world': {'tribal': 'paint the pots so the patterns quietly laugh at the clan that trades them', 'magic': 'make the shop sign a work of its own that quietly mocks the ware'}, 'chance': 0.55}),
    ('take the money, and buy a year to paint nothing but your own work', 'B.34 R.33 G.33', None, 0.5, '', {'binds': True, 'v': 'self-direction, hedonism', 'world': {'tribal': 'take the gifts, and spend a whole winter painting only what you choose', 'magic': 'take the gold, and buy a year to paint nothing but your own work'}, 'chance': 0.65}),
 ]},
{'name': 'hands that will not hold the brush',
 'stages': 'adult mature elder',
 'age': (40, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.04, 0.06),
 'drivers': 'health-.5 stress+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, health',
 'horizon': 'years',
 'roles': 'partner, colleague, mentor, friend, child',
 'requires': 'painter or sculptor | master craftsperson | illustrator for hire | craft maker',
 'worlds': {'earth': 'the hands shake, or stiffen, and the fine work will not come',
            'tribal': "the carver's hands stiffen in the cold, and the fine lines will not come",
            'magic': "the guild painter's hands begin to shake, and the fine work will not come"},
 'timing': {'times': 'per painter, illustrator or maker a year: about 1 in 25 in later life finds the hands or the '
                     'eyes failing the fine work (a tremor, arthritis in the fingers, cataracts or a macular '
                     'change); the four careers are about 1 life in 100 (catalogue shares), so about 1 life in 300 '
                     'meets it (estimate); hand osteoarthritis and essential tremor both become common after sixty',
            'likelier': 'old age, decades of fine close work, a family history of tremor, a hard winter in a cold '
                        'studio',
            'rarer': 'middle age, work on a large scale with the whole arm, good health, a maker who has always '
                     'worked with assistants',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'It starts with the fine work: the line that will not stay where it is put, the knuckles that '
                       'ache by noon, the brush that slips. The specialist is kind and plain about it. It will not '
                       'get better, though it may get worse slowly, and there are things that help.'),
                      ('W',
                       'There is a way to meet this, as there is a way to do everything: the treatment, the '
                       'exercises, the hours kept. {N} means to do it properly.'),
                      ('U',
                       '{N} watches the hand like a problem to be solved: which tools it can still hold, which '
                       'movements still come clean, what larger marks might do that small ones cannot.'),
                      ('B',
                       '{N} has spent thirty years building a name. The question is how to keep it working when the '
                       'hands will not.'),
                      ('R',
                       '{N} throws the brush across the studio, and then laughs, because the mark it leaves on the '
                       'wall is wilder than anything painted all year.'),
                      ('G',
                       'Every maker {N} has known came to this in the end, the old masters too. {N} sits a long time '
                       'at the bench in the afternoon light, thinking of the work that is already done.')],
            'tribal': [('',
                        "Since the long cold the carver's fingers will not close round the fine flint, and the lines "
                        'of the antlers come out wrong. The old ones nod; it came to their own hands too, in the '
                        'end.')],
            'magic': [('',
                       "The guild painter's hands have begun to shake at the fine work, and the physicians' hall has "
                       'no cure for it, only salves and patience.')]},
 'outcomes': (['A year on, the work has found a new shape, smaller or larger or in other hands, and {N} has made a '
               'kind of peace with it.',
               'Whatever {N} chose, the studio is not a sad place, and people still come to it.'],
              ['The months go by in waiting rooms and bad days, and {N} cannot settle to anything.',
               'The plan does not hold, the hand gets worse faster than anyone said, and {N} has to begin again from '
               'somewhere else.']),
 'options': [
    ('see the specialist, and follow the treatment to the letter', 'W1', None, 0.45, '', {'self_control': '+', 'habit': True, 'v': 'conformity, security', 'world': {'tribal': 'go to the healer, and keep every rule of the cure', 'magic': "go to the physicians' hall, and follow the cure to the letter"}, 'chance': 0.64}),
    ('change the method: longer brushes, a strap at the wrist, a new material', 'U1', None, 0.45, '', {'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'change the way of working: a longer stick, a thong at the wrist, a softer stone'}, 'chance': 0.72}),
    ('turn the name into prints, licences and a shop of the old work', 'B1', None, 0.45, '', {'grants': 'royalties', 'habit': True, 'v': 'power, achievement', 'world': {'tribal': 'trade the old carvings far and wide while the name still carries', 'magic': 'sell prints and copies of the old work while the name still sells'}, 'chance': 0.67}),
    ('work with the shaking hand, and let the shake into the work', 'R1', None, 0.45, '', {'mark': 'took a wild risk', 'self_control': '+', 'v': 'stimulation, self-direction', 'chance': 0.67}),
    ('put the tools down for good, and take it as the end of one chapter', 'G1', None, 0.45, '', {'drops': 'painter or sculptor; master craftsperson; illustrator for hire; craft maker', 'v': 'tradition, universalism', 'world': {'tribal': 'lay the tools down for good, and take it as the turn of a season'}, 'chance': 0.65}),
    ('teach at the college two days a week, and pass on the method', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'pupils who remember you', 'door': True, 'v': 'benevolence, achievement', 'world': {'tribal': 'teach the young ones the ways of the hand, two days in every moon', 'magic': 'teach at the academy two days a week, and pass on the method'}, 'chance': 0.6}),
    ('give the tools and the workshop to a young maker who needs them', 'W.34 R.33 G.33', None, 0.5, '', {'drops': 'painter or sculptor; master craftsperson; illustrator for hire; craft maker', 'mark': 'helped someone in need', 'v': 'benevolence, tradition', 'world': {'tribal': 'give the tools and the carving place to a young carver of the band', 'magic': 'give the tools and the workshop to a young guild maker who needs them'}, 'chance': 0.8}),
    ('finish the last commissions as promised, whatever it costs the hands', 'W.34 B.33 R.33', None, 0.5, '', {'mark': 'kept your word', 'self_control': '+', 'v': 'conformity, power', 'world': {'tribal': 'finish the carvings promised to the traders, whatever it costs the hands'}, 'chance': 0.65}),
    ('learn to draw with the other hand, slowly, like a child again', 'U.34 R.33 G.33', None, 0.5, '', {'habit': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'learn to cut with the other hand, slowly, like a child again'}, 'chance': 0.5}),
    ('take on an assistant, and teach them every step while there is time', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'pupils who remember you', 'binds': True, 'v': 'tradition, achievement', 'world': {'tribal': 'take a young helper, and show every step while there is time', 'magic': 'take on an apprentice, and teach every step while there is time'}, 'chance': 0.7}),
 ]},
{'name': 'the sketch that went round the world',
 'stages': 'juvenile young_adult adult mature',
 'age': (16, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.005, 0.01, 0.01, 0.005, 0.0),
 'drivers': 'era+.3 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, making, money',
 'horizon': 'week',
 'roles': 'friend, colleague, mentor, rival, a dealer',
 'requires': 'life-drawing regular | street artist | illustrator for hire',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': 'a sketch posted on a quiet evening is shared round the world overnight, and the messages '
                     'start: a gallery, a publisher, the town council, a dealer',
            'tribal': 'a trader carries a drawing on a scraped hide from the river crossing to every band in the '
                      'valley, and the elders of far camps send for the hand that made it',
            'magic': 'a sketch left on a tavern table is copied by the printers and pinned up in every city of the '
                     'realm, and letters come under strange seals'},
 'timing': {'times': 'per life-drawing regular, street artist or illustrator with two years or more of drawing '
                     'behind them, a year: about 1 in 100 has a drawing shared far beyond their own circle '
                     '(estimate); pictures are shared online by the million every day, and only a handful a year '
                     'turn into a first show, a book or a wall (estimate); about 15 lives in 1,000 draw at a weekly '
                     'class and about 1 in 1,000 earn a living from painting (catalogue shares)',
            'likelier': 'work people stop for, a year when pictures travel fast online, a friend who shares it well, '
                        'years of drawing behind it',
            'rarer': 'work never shown outside the class or the sketchbook, a quiet year online, no time to answer '
                     'the messages',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'On a wet Tuesday {N} drew the market from a café window in twenty minutes: the stalls '
                       'packing up, a woman holding an umbrella over the fruit, the lights coming on. {N} posted it '
                       'before bed. By Thursday it has been seen by eleven million people, and the messages will not '
                       'stop: a gallery in the capital, a publisher of picture books, the town council, a dealer, '
                       'and every friend {N} has asking if it is true.'),
                      ('W',
                       '{N} answers nobody for a day and makes a list instead: who wrote, what each one offers, '
                       "which offers are real. The council's letter is the only one on headed paper, and it has a "
                       'plan attached.'),
                      ('U',
                       '{N} looks at the sketch for an hour, trying to see what eleven million people saw. It is '
                       'something in the line, quick and sure, that {N} has chased for years and caught only once.'),
                      ('B',
                       'Attention like this lasts about a fortnight. {N} sorts the messages into the ones with money '
                       'behind them and the ones with names, and starts with the names.'),
                      ('R',
                       '{N} reads the messages on the bus to work, laughing out loud. Years of drawing for nobody in '
                       'particular, and now the whole world wants to see the next one, and {N} wants to make it '
                       'today.'),
                      ('G',
                       'The stallholders have all seen it. The woman with the umbrella is the fruit seller, and she '
                       'has printed it out and taped it to her till; the whole market is prouder of it than {N} '
                       'is.')],
            'tribal': [('',
                        '{N} drew the gathering at the river crossing on a scraped hide, quick and sure, and a '
                        'trader carried it off to barter. Now runners come from far camps: their elders have seen '
                        'the hide, and want the hand that made it to paint their shelter walls, mark their drums, or '
                        'paint a wall of the great cave.')],
            'magic': [('',
                       '{N} sketched the market in the rain on the back of a bill in a tavern and left it there. The '
                       'printers copied it, and now it is pinned up in every city of the realm; letters come under '
                       "strange seals: a picture dealer, the printers' guild, the city's council, a lord's "
                       'steward.')]},
 'outcomes': (['Within a month there is a contract on the kitchen table, a start date and a wall, a book or a show '
               'with {Ns} name on it, and the friends from the old class throw a party.',
               'Whatever {N} chose, the sketch turns out to be the start of something rather than the whole of it.'],
              ["The messages stop after nine days, another picture takes the world's attention, and {N} goes back to "
               'work on the Monday with a story nobody there quite believes.',
               'The meetings go well and nothing comes of them; the last one ends with "lovely, not quite ready", '
               'and {N} draws the market again that night, out of pure stubbornness.']),
 'options': [
    ('answer the council by return, and paint the sketch as a mural to their plan', 'W1', None, 0.45, '', {'title': 'street artist', 'requires': 'life-drawing regular', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': "answer the far elders' runner, and paint the drawing on their shelter wall exactly as they ask", 'magic': "answer the city council's seal, and paint the sketch on the guildhall wall to their plan"}, 'chance': 0.03}),
    ("work the sketch's quick line into a style, and send a publisher twenty drawings in it", 'U1', None, 0.45, '', {'title': 'illustrator for hire', 'requires': 'life-drawing regular', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': "work the drawing's quick line into a pattern, and offer to mark the far camps' drums with it", 'magic': "work the sketch's quick line into a hand, and send the printers twenty plates in it"}, 'chance': 0.03}),
    ('sign with the dealer who wrote first, and hold out for a solo show', 'B1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'let the trader who carried the hide speak for the hand, and hold out for a wall of the great cave', 'magic': 'sign with the picture dealer who wrote first, and hold out for a hall of the work alone'}, 'chance': 0.03}),
    ('leave the day job, and paint the sketch as big as a wall, twenty times over', 'R1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'identity': True, 'v': 'stimulation, hedonism', 'world': {'tribal': 'leave the hunt to the others, and paint the drawing huge on every rock at the painting place', 'magic': 'leave the shop to the apprentice, and paint the sketch on canvases as tall as a door'}, 'chance': 0.03}),
    ("paint the market's own people one by one, and show them in the town hall", 'G1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'door': True, 'mark': 'made a friend', 'v': 'tradition, benevolence', 'world': {'tribal': 'paint the people of the crossing one by one, and show them at the home fire', 'magic': "paint the market's stallholders one by one, and hang them in the ward's hall"}, 'chance': 0.03}),
    ("ask the class's old tutor to go through everything, and study for a year first", 'W.34 U.33 R.33', None, 0.5, '', {'aims': 'painter or sculptor', 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': 'ask the old painter of the rock to look at everything, and learn for a winter first', 'magic': 'ask the old master of the evening hall to look at everything, and study a year first'}, 'chance': 0.84}),
    ('license the sketch to a magazine for a fair fee, with a proper contract', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'royalties', 'binds': True, 'v': 'security, achievement', 'world': {'tribal': 'let a far band copy the drawing on their drums, for a share of every trade', 'magic': 'let the printers sell the sketch for a fair share, under a sealed contract'}, 'chance': 0.84}),
    ('turn the offers down, and give the original to the woman with the umbrella', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence, universalism', 'world': {'tribal': 'send the runners home, and give the hide to the woman it shows', 'magic': 'send the letters back, and give the sketch to the fruit seller it shows'}, 'chance': 0.84}),
    ('have coffee with the gallery that wrote, and mostly listen', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'achievement, benevolence', 'world': {'tribal': 'sit with the far trader at the crossing, and mostly listen', 'magic': 'take supper with the picture dealer who wrote, and mostly listen'}, 'chance': 0.84}),
    ('post a new drawing every day while the world is still watching', 'B.34 R.33 G.33', None, 0.5, '', {'grants': 'following online', 'habit': True, 'v': 'stimulation, power', 'world': {'tribal': 'draw a new hide every day while the traders are still asking', 'magic': 'leave a new sketch in a tavern every day while the printers are still copying'}, 'chance': 0.84}),
 ]},
{'name': 'the open submission to the great summer show',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.02),
 'drivers': 'fortune+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, making, meaning',
 'horizon': 'months',
 'roles': 'friend, partner, mentor, rival, colleague',
 'requires': 'painter or sculptor | life-drawing regular',
 'tenure': (5.0, 99.0),
 'worlds': {'earth': 'the forms for the great summer show at the academy in the capital, open to anyone who pays the '
                     'fee, and a closing date on Friday',
            'tribal': 'every band brings its best painted hides to the great gathering, the elders hang one in ten '
                      'on the cliff below the painted cave, and most summers one hide by an unknown hand is carried '
                      'up into the cave to stay',
            'magic': 'the academy of arts throws its great hall open to any painter who pays the fee, and most years '
                     'the court buys one canvas by a name nobody knew'},
 'timing': {'times': 'per painter, sculptor or life-drawing regular of five years or more, a year: about 1 in 60 '
                     'sends work to a great open-submission summer show (estimate); the biggest such show in one '
                     "capital receives about 15,000 entries a year and hangs about 1,200 (the show's own figures, "
                     'approximate), and only a very few unknown entrants a decade go on to a national name '
                     '(estimate); about 1 life in 10,000 becomes a renowned artist (catalogue share)',
            'likelier': 'years of finished work, a canvas that stops people, a summer with money for the fee, a '
                        'selector who likes the kind of thing',
            'rarer': 'no finished work this year, the fee, a summer of family duties',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'Every summer the academy in the capital hangs the great summer show, and anyone may send two '
                       'works and a fee. Fifteen thousand works come in each spring; about one in ten is hung, frame '
                       'to frame up to the ceiling; and most years the critics single out one name nobody knew, '
                       'whose work the national gallery buys before the show closes. The forms are on {Ns} kitchen '
                       'table, the closing date is Friday, and the canvases stand against the wall.'),
                      ('W',
                       '{N} reads the rules twice: the sizes, the framing, the label on the back, the fee paid by '
                       'Friday. If there is a fair way through fifteen thousand, it is to send exactly what was '
                       'asked, finished properly.'),
                      ('U',
                       '{N} has read that the selectors give each work about four seconds. Four seconds is enough '
                       'for one idea, if it is the right idea, made as well as it can be made.'),
                      ('B',
                       'The selectors are painters and academicians with names, and every one of them has friends. '
                       '{N} has worked out which openings they go to, and who at those openings owes {N} a drink.'),
                      ('R',
                       'There is one canvas in the corner that nobody has understood yet, too big for the car and '
                       'too strange for the living room. {N} has never wanted anything as much as to see it on that '
                       'wall.'),
                      ('G',
                       '{N} has painted the old neighbour across the road all winter, by her window, in her own '
                       'chair. She asks every week whether it will go to the capital, and {N} has not had the heart '
                       'to tell her how few do.')],
            'tribal': [('',
                        'Every summer the bands bring their best painted hides to the great gathering, and the '
                        'elders hang one in ten on the cliff below the painted cave; most summers one hide by an '
                        'unknown hand is carried up into the cave itself, to stay. {N} has five winters of painting '
                        'behind, and a hide rolled up by the door.')],
            'magic': [('',
                       'Every summer the academy of arts throws open its great hall to any painter of the realm who '
                       'pays the fee; the canvases hang frame to frame, and most years the court buys one by a name '
                       'nobody knew. {N} has the form, the coin and years of painting behind.')]},
 'outcomes': (['A letter in a stiff envelope comes in late spring: the work is hung, a critic stops in front of it '
               'on the first morning, and by the end of the summer the national gallery has bought it and {Ns} name '
               'is in every paper.',
               'Whatever {N} chose, the summer is a good one for the work, and the next canvas is better than the '
               'last.'],
              ['The letter is short and printed: the selectors thank {N} and regret. {N} collects the canvas from a '
               'warehouse stacked with thousands of others, and drives it home in the rain.',
               'The work is hung, high in a corner above a door; nobody buys it, a stranger writes one kind sentence '
               "about it in the visitors' book, and {N} copies the sentence into the back of a sketchbook."]),
 'options': [
    ('send the two best canvases, framed to the rules, the fee paid on time', 'W1', None, 0.45, '', {'title': 'renowned artist; painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'bring the two best hides to the gathering on the right night, laced as the elders ask', 'magic': "send the two best canvases, framed to the academy's rules, the fee paid on the day"}, 'chance': 0.02}),
    ("paint one new canvas for it, a year's study of one idea, and send only that", 'U1', None, 0.45, '', {'title': 'renowned artist; painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': "paint one new hide for it, a whole winter's study of one beast, and bring only that", 'magic': "paint one new canvas for it, a year's study of one idea, and send that alone"}, 'chance': 0.02}),
    ('get a selector to look at the work beforehand, through a friend of a friend', 'B1', None, 0.45, '', {'title': 'renowned artist; painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'power, achievement', 'world': {'tribal': "get one of the choosing elders to see the hide beforehand, through a cousin's hearth", 'magic': "have an academician see the canvas beforehand, through a patron's steward"}, 'chance': 0.02}),
    ('send the strangest canvas in the room, the one nobody has understood yet', 'R1', None, 0.45, '', {'title': 'renowned artist; painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'bring the great strange hide that nobody at the painting place has understood', 'magic': 'send the huge strange canvas that the evening hall laughed at'}, 'chance': 0.02}),
    ("send the winter's portrait of the old neighbour, painted in her own chair", 'G1', None, 0.45, '', {'title': 'renowned artist; painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'bring the hide painted with the old woman of the next hearth, by her own fire', 'magic': 'send the portrait of the old widow across the lane, painted in her own chair'}, 'chance': 0.02}),
    ('go on the opening day, and spend the whole day looking at what was hung', 'W.34 U.33 G.33', None, 0.5, '', {'mark': 'learned a skill', 'v': 'universalism, conformity', 'world': {'tribal': "climb to the cliff on the gathering's first day, and look at every hide that was hung", 'magic': 'go to the great hall on the opening day, and look at every canvas that was hung'}, 'chance': 0.82}),
    ('take a stall at the summer art fair in the park instead, and sell what sells', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'selling', 'v': 'power, stimulation', 'world': {'tribal': "spread the hides at the gathering's trading ground instead, and trade what people want", 'magic': 'take a stall at the midsummer fair on the square instead, and sell what sells'}, 'chance': 0.82}),
    ("hang the work in the local art society's summer show, and help hang everyone else's", 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'good name in town', 'mark': 'made a friend', 'v': 'benevolence, security', 'world': {'tribal': "paint the shelter hides of your own band this summer, and help paint everyone else's", 'magic': "hang the work in the ward's own summer show, and help hang everyone else's"}, 'chance': 0.82}),
    ('send nothing this year, and paint outdoors all summer with the old crowd from the class', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'a circle of artists', 'habit': True, 'v': 'universalism, stimulation', 'world': {'tribal': 'bring nothing to the cliff this year, and paint the rocks all summer with the ones who paint beside you', 'magic': 'send nothing this year, and paint in the fields all summer with the old crowd from the evening hall'}, 'chance': 0.82}),
    ('enter every smaller open show in the region this year, and note what each one hangs', 'U.34 B.33 R.33', None, 0.5, '', {'aims': 'renowned artist', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': 'bring hides to every smaller gathering this summer, and watch what each one hangs', 'magic': "send work to every town's open show this year, and note what each one hangs"}, 'chance': 0.82}),
 ]},
{'name': 'the manuscript in the pile on the floor',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.01),
 'drivers': '',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, making, meaning',
 'horizon': 'months',
 'roles': "friend, partner, mentor, rival, a publisher's reader",
 'requires': 'open-mic poet | novelist',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': 'a finished manuscript, and the pile of unasked-for manuscripts on the floor of a big '
                     "publisher's office, read by a junior on Fridays",
            'tribal': 'a long telling worked over many winters, and the keeper of tellings at the great gathering, '
                      'who hears one new telling a night and forgets most by morning',
            'magic': 'a finished manuscript wrapped in oilcloth, and the heap of unasked-for manuscripts on the '
                     'floor of the great printing house, read by an apprentice on market days'},
 'timing': {'times': 'per open-mic poet of two years or novelist of three, a year: about 1 in 100 sends a finished '
                     'manuscript unasked to a big publisher (estimate); the big houses that still read unasked work '
                     'receive thousands of manuscripts a year and take one or two at most, most years none '
                     '(estimate); about 5 lives in 10,000 live as novelists and about 1 in 10,000 become celebrated '
                     'authors (catalogue shares)',
            'likelier': 'a finished manuscript in a drawer, years of writing behind it, a publisher that still reads '
                        'the pile, a friend who says send it',
            'rarer': 'no finished book, a house that reads only through agents, a busy year at work or at home',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       "In the corner of a big publisher's office the manuscripts nobody asked for stand in stacks "
                       'on the floor, a few thousand a year. On Friday afternoons a junior reader takes the top of '
                       'the pile home in a bag, and once every few years one of them goes upstairs. {N} has a '
                       'finished manuscript in a drawer: years of work, and a one-page letter rewritten twenty '
                       'times.'),
                      ('W',
                       "The publisher's page says how: the first three chapters, double-spaced, a synopsis of one "
                       'page, no telephone calls. {N} has printed the page and pinned it above the desk.'),
                      ('U',
                       '{N} knows the book is nearly right. There is a chapter in the middle that sags, and a reader '
                       'on a tired Friday afternoon will feel it at the same page {N} does.'),
                      ('B',
                       'Someone reads that pile, and that someone has a name, a lunch hour and a favourite café. '
                       'Finding out who is the first job, and the second is being remembered.'),
                      ('R',
                       'The book came out in a rush, most of it in one cold month, and {N} is half afraid of it. '
                       'Sending it now, before the nerve goes, feels like jumping into the sea in winter.'),
                      ('G',
                       'The book is full of the town: the regulars at the poetry night, the old men at the bowls '
                       "club, {Ns} own grandmother's sayings. {N} asked each of them before writing a word, and "
                       'every one of them said yes.')],
            'tribal': [('',
                        'At the great gathering the keeper of tellings hears the new long tellings brought to the '
                        'fire, one a night, and most are forgotten by morning; once in many summers one is taken up '
                        'and told at every fire in the valley. {N} has a long telling ready, worked over many '
                        'winters.')],
            'magic': [('',
                       'In the back room of the great printing house the unasked-for manuscripts lie in heaps on the '
                       'floor, and an apprentice reads from the top of them on market days; once in some years one '
                       'goes upstairs to the master printer. {N} has a finished manuscript wrapped in oilcloth, and '
                       'a letter rewritten twenty times.')]},
 'outcomes': (['Seven months later the telephone rings on a Friday evening: the junior reader took it home, read it '
               'in one night and carried it upstairs, and a year after that the book is in shop windows with {Ns} '
               'name on the cover.',
               'Whatever {N} chose, the book goes out into the world in some form, and {N} starts the next one the '
               'same week.'],
              ['The manuscript comes back after eight months with a printed slip, a coffee ring on the first page, '
               "and nobody's name at the bottom.",
               'There is no answer at all; {N} stops watching for the post in the spring, and by the summer is '
               'writing something new.']),
 'options': [
    ("send it exactly as the publisher's page asks: three chapters, one page of synopsis, nothing more", 'W1', None, 0.45, '', {'title': 'novelist', 'requires': 'open-mic poet', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'conformity', 'world': {'tribal': 'bring the telling to the keeper on the right night, every part in the old order', 'magic': 'send the printers three quires and a letter, exactly as their notice asks'}, 'chance': 0.02}),
    ('rewrite the sagging chapter a ninth time, then send the whole book', 'U1', None, 0.45, '', {'title': 'celebrated author', 'requires': 'novelist', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'work the slack part of the telling over a ninth winter, then bring the whole of it', 'magic': 'rewrite the sagging chapter a ninth time, then send the whole book to the master printer'}, 'chance': 0.02}),
    ('find out who reads the pile on Fridays, and make sure this one reaches them', 'B1', None, 0.45, '', {'title': 'celebrated author', 'requires': 'novelist', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': "find out which of the keeper's helpers chooses the tellings, and sit by them at the fire", 'magic': 'learn which apprentice reads the heap on market days, and see that this one reaches them'}, 'chance': 0.02}),
    ('send the wild first draft tonight, before the nerve goes', 'R1', None, 0.45, '', {'title': 'novelist', 'requires': 'open-mic poet', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'habit': True, 'v': 'stimulation, hedonism', 'world': {'tribal': 'stand up at the fire tonight and give the whole new telling, before the nerve goes', 'magic': "send the wild first draft by tonight's coach, before the nerve goes"}, 'chance': 0.02}),
    ("send the book of the town's own stories, with the blessing of everyone in it", 'G1', None, 0.45, '', {'title': 'novelist', 'requires': 'open-mic poet', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': "bring the telling of your own band's people, with the blessing of everyone in it", 'magic': "send the book of the ward's own tales, with the blessing of everyone in it"}, 'chance': 0.02}),
    ("join a writers' group at the library, and swap chapters every fortnight for a year", 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'writing stories', 'habit': True, 'v': 'self-direction, conformity', 'world': {'tribal': 'sit with the other makers of tellings, and trade parts every moon for a year', 'magic': "join the scriveners' circle at the tavern, and swap chapters every fortnight for a year"}, 'chance': 0.84}),
    ('send it to twenty literary agents instead, one a week, each by their own rules', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'contact in the trade', 'self_control': '+', 'v': 'security, achievement', 'world': {'tribal': 'take the telling to the go-betweens of twenty bands, one each moon, as each one asks', 'magic': "send it to twenty booksellers' agents, one a week, each by their own rules"}, 'chance': 0.84}),
    ("print a small run with the town's own press, and launch it at the library", 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'book in print', 'binds': True, 'v': 'tradition, security', 'world': {'tribal': 'tell it at every hearth of your own band through one winter, until the children know it', 'magic': "have a small run printed by the ward's own press, and launch it at the guildhall"}, 'chance': 0.84}),
    ('read the best chapter aloud at the poetry night, and see if the room goes quiet', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'public speaking', 'v': 'stimulation, universalism', 'world': {'tribal': "tell the best part at the band's fire on the long night, and see if the fire goes quiet", 'magic': "read the best chapter at the poets' night in the tavern, and see if the room goes quiet"}, 'chance': 0.84}),
    ('put the first chapter online for free, and let readers ask for the rest', 'B.34 R.33 G.33', None, 0.5, '', {'grants': 'following online', 'door': True, 'v': 'stimulation, power', 'world': {'tribal': 'tell the first part at every trading place, and let the listeners ask for the rest', 'magic': 'have the first chapter cried in the market for free, and let the listeners ask for the rest'}, 'chance': 0.84}),
 ]},
{'name': 'the late starter at the easel',
 'stages': 'mature elder',
 'age': (58, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.02, 0.03),
 'drivers': 'fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, making, meaning',
 'horizon': 'months',
 'roles': 'partner, child, friend, mentor, colleague',
 'requires': 'life-drawing regular',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': 'the job ended, the children grown, years of Tuesday nights at the life class, and a notice on '
                     'the college board: the tutor is retiring',
            'tribal': 'too old for the long hunts, after years at the painting place, with the old painter of the '
                      'great cave failing and the young ones needing someone to show them the marks',
            'magic': "the shop handed to the eldest, years of sketching at the academy's evening hall, and a notice "
                     'on its door: the drawing master is retiring'},
 'timing': {'times': 'per life-drawing regular of 58 or more with two years at the class, a year: about 1 in 40 '
                     'decides at last to try to make art a second career, to sell, show or teach (estimate); '
                     'adult-education art classes are taught by working artists, and a first show or a teaching post '
                     'after sixty is rare but not unknown (estimate); about 15 lives in 1,000 draw at a weekly '
                     'class, about 1 in 1,000 earn a living from painting and about 3 in 1,000 teach art (catalogue '
                     'shares)',
            'likelier': 'the job ended or a pension begun, children grown, years at the class, a room to spare, a '
                        'partner who says go on then',
            'rarer': 'money owed, a family that needs the time, poor eyes or hands, a town with no college',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'The job ended last spring with a cake and a card, the children have homes of their own, and '
                       "{N} has drawn at the college's Tuesday class for years, most weeks the oldest in the room. "
                       'In the spare room the canvases lean three deep against the wall. On the board in the college '
                       'corridor this week: the Tuesday tutor is retiring after twenty years and the college needs '
                       'someone; underneath, a café on the high street wants local work for its walls, and an open '
                       'show for artists over sixty is taking entries.'),
                      ('W',
                       'In all those years of Tuesdays {N} has missed four. Somebody has to keep the class going, '
                       'and {N} knows exactly how it runs: the easels out by seven, a break on the hour, the kettle '
                       'on at half past eight.'),
                      ('U',
                       '{N} has drawn hands for two years, only hands, and has filled nine sketchbooks with them. '
                       'There is something there, if there were time at last to follow it to the end.'),
                      ('B',
                       '{N} spent a working life in sales, and knows the canvases in the spare room are worth '
                       'something to somebody. Nobody has ever been asked to pay for one.'),
                      ('R',
                       'Forty years of doing what was sensible, and {N} is done with it. The spare room smells of '
                       'turpentine already, and the next canvas wants to be enormous.'),
                      ('G',
                       'The village hall has had no art class since the old tutor died, and half the street has '
                       'asked {N} to start one. Most of them want to paint the hills they have looked at all their '
                       'lives.')],
            'tribal': [('',
                        'Too old now for the long hunts, {N} sits at the painting place with the others most days, '
                        'as for years past. The old painter of the great cave is failing, the young ones need '
                        'someone to show them the marks, and the traders want hides from a steady hand.')],
            'magic': [('',
                       "The shop has gone to the eldest, and {N}, who has sketched at the academy's evening hall for "
                       'years, reads the notices on its door: the drawing master is retiring, a tavern on the square '
                       'wants pictures for its walls, and the academy holds an open show for grey-haired '
                       'painters.')]},
 'outcomes': (['By the autumn {N} has a key to a room, a list of names or a show on a wall, and stands in front of '
               'it on the first night trying not to look as pleased as {N} is.',
               'Whatever {N} chose, the late start is a real one, and the years that follow have paint in them.'],
              ['The college gives the class to a young graduate and the galleries are kind and full; {N} goes back '
               'to the Tuesday easel as before, and draws better than ever, out of something close to defiance.',
               'The answers are polite letters that praise the nerve in one sentence and give the chance to someone '
               'with thirty years in the trade; {N} pins the kindest of them above the easel.']),
 'options': [
    ('offer to take over the Tuesday class, with a plan for every week of the year', 'W1', None, 0.45, '', {'title': 'art teacher', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'conformity, benevolence', 'world': {'tribal': 'offer to show the young ones the marks when the old painter cannot, every day without fail', 'magic': 'offer to take the evening hall when the drawing master retires, with a plan for every week'}, 'chance': 0.03}),
    ('paint twenty canvases of hands, and offer the series to the college gallery', 'U1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'paint only hands on the rock for a whole winter, and offer them for the cave', 'magic': "paint twenty canvases of hands, and offer the series to the academy's small gallery"}, 'chance': 0.03}),
    ("price the spare room's canvases properly, and take them round every gallery in town", 'B1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'power, achievement', 'world': {'tribal': 'carry your best hides to every trader at the gathering, and ask a fair price for each', 'magic': 'price the canvases properly, and carry them to every picture dealer on the square'}, 'chance': 0.03}),
    ('turn the spare room into a studio, and paint the way the young never dared', 'R1', None, 0.45, '', {'title': 'painter or sculptor', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'identity': True, 'v': 'stimulation, hedonism', 'world': {'tribal': 'take a rock of your own at the painting place, and paint the way the young never dared', 'magic': 'turn the spare room into a studio, and paint as the young never dared'}, 'chance': 0.03}),
    ("start the village hall's own class, and teach it the way the old tutor did", 'G1', None, 0.45, '', {'title': 'art teacher', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'tradition, benevolence', 'world': {'tribal': 'gather the children of your own hearths, and show them the marks the old way', 'magic': "start the ward's own drawing class in its hall, and teach it as the old master did"}, 'chance': 0.03}),
    ("join the college's sculpture course, the oldest in the room by forty years", 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'sculpting', 'self_control': '+', 'v': 'self-direction, conformity', 'world': {'tribal': 'learn to carve from the young carver, the oldest at the work by forty winters', 'magic': "join the academy's sculpture course, the oldest in the room by forty years"}, 'chance': 0.82}),
    ("hang the whole Tuesday class's work in the café, every hand side by side", 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'a circle of artists', 'mark': 'made a friend', 'v': 'benevolence, universalism', 'world': {'tribal': 'paint one rock with everyone from the painting place, every hand side by side', 'magic': "hang the whole evening hall's work in the tavern, every hand side by side"}, 'chance': 0.82}),
    ('enter the open show for over-sixties, and go to the opening in a good coat', 'W.34 B.33 R.33', None, 0.5, '', {'aims': 'painter or sculptor', 'identity': True, 'v': 'achievement, stimulation', 'world': {'tribal': "bring a hide to the elders' showing of the old ones' work, and stand by it all night", 'magic': "send a canvas to the academy's show for grey heads, and go to the opening in a good coat"}, 'chance': 0.82}),
    ('sell a few small pictures at the winter fair, and watch what people pick up', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'selling', 'door': True, 'v': 'power, stimulation', 'world': {'tribal': 'trade a few small painted bowls at the winter gathering, and watch what people reach for', 'magic': 'sell a few small panels at the winter fair on the square, and watch what people pick up'}, 'chance': 0.82}),
    ('keep the best twenty canvases, give the rest to the family, and paint on', 'U.34 B.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'habit': True, 'v': 'tradition, universalism', 'world': {'tribal': 'keep the best hides, give the rest to the families of the band, and paint on', 'magic': 'keep the best twenty canvases, give the rest to the family, and paint on in peace'}, 'chance': 0.82}),
 ]},
{'name': 'the other side of the easel',
 'stages': 'adult mature elder',
 'age': (25, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.01, 0.005),
 'drivers': '',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, making, money',
 'horizon': 'week',
 'roles': 'colleague, boss, mentor, friend, a dealer',
 'requires': 'painter or sculptor | illustrator for hire | art teacher',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': "a week on the art school's panel for its portfolio days: three hundred hopefuls, each with a "
                     'folder and twenty minutes',
            'tribal': 'a place beside the elders while the young ones of every band bring their first painted hides '
                      'to be judged for the cave',
            'magic': "a seat on the academy's bench for its entrance week: three hundred hopefuls, each with a folio "
                     'and an hour of fear'},
 'timing': {'times': 'per painter, illustrator or art teacher of three years or more, a year: about 1 in 100 is '
                     "asked to sit on an art school's panel for a week of portfolio interviews (estimate); art "
                     "schools ask working artists and teachers to help choose each year's intake, and a panellist "
                     'who opens a gallery, wins a teaching post or a first book from that week is rare (estimate); '
                     'about 3 lives in 10,000 run a gallery and about 3 in 1,000 teach art (catalogue shares)',
            'likelier': 'a name at the school, years of reliable work, a busy year of applications, a good eye',
            'rarer': 'a school far away, a week that cannot be spared, little money behind any plan',
            'gap_years': (5.0, 12.0)},
 'scenes': {'earth': [('',
                       'The art school asks {N} to sit on its panel for the portfolio days: a week in spring, a long '
                       'table, three hundred young hopefuls, each with a folder and twenty minutes. {N} sat on the '
                       'other side of that table once. Beside {N} sit the head of the foundation year, the art '
                       'director of a picture-book publisher looking for new hands, and a dealer who comes every '
                       'year to see who is coming up.'),
                      ('W',
                       "{N} reads the school's marking guide twice and keeps to it all week, the same questions for "
                       'every hopeful. By Wednesday the head of the foundation year is asking {N} to settle the '
                       'scores.'),
                      ('U',
                       'By the third day {N} can see in the first drawing what a hopeful will be in five years. The '
                       'art director at the end of the table has noticed that {N} is usually right.'),
                      ('B',
                       'The dealer takes a name or two each year, and the ones taken are the ones who get shown. {N} '
                       "watches the dealer's pen more than the folders."),
                      ('R',
                       'Half the hopefuls are terrified and one or two are on fire, and {N} wants to leap the table '
                       'and tell them all to keep going. Teaching was never part of any plan.'),
                      ('G',
                       'Many of the hopefuls come from towns like {Ns} own, with folders full of their own streets. '
                       '{N} thinks of the empty shops on the high street at home, and all the makers there with '
                       'nowhere to show.')],
            'tribal': [('',
                        'The old painter of the great cave asks {N} to sit beside the elders while the young ones of '
                        'every band bring their first painted hides to be judged; a trader from the coast sits there '
                        'too, looking for hands whose work he can carry.')],
            'magic': [('',
                       'The academy of arts asks {N} to sit on its bench for the entrance week: three hundred '
                       'hopefuls, each with a folio and an hour of fear. Beside {N} sit the master of the first '
                       "year, a printer's master of plates looking for illuminators, and a picture dealer from the "
                       'square.')]},
 'outcomes': (['A month later the call comes, and it is the one {N} asked for; by the autumn there is a new key on '
               '{Ns} ring and a new name on a door.',
               'Whatever {N} chose, the week on the far side of the table changes how {N} looks at every drawing '
               'after it.'],
              ['The week ends with thanks and a small cheque; the post goes to someone the school already knew, and '
               '{N} goes back to work knowing exactly what happens in the first minute with a folder.',
               'The plan is good and the money is not there; the empty shop on the high street becomes a phone '
               'repair stall, and {N} walks past it most mornings without minding much.']),
 'options': [
    ('ask the head of the foundation year for a teaching post, starting in the autumn', 'W1', None, 0.45, '', {'title': 'art teacher', 'requires': 'painter or sculptor', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'conformity, security', 'world': {'tribal': 'ask the old painter to let you teach the young ones the marks, from the next moon', 'magic': 'ask the master of the first year for a post as drawing master, from the autumn'}, 'chance': 0.03}),
    ('show the art director a folder of new drawings, and ask for a first book', 'U1', None, 0.45, '', {'title': 'illustrator for hire', 'requires': 'art teacher', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'show the coast trader a bowl of your own patterns, and ask to mark the drums he carries', 'magic': 'show the master of plates a folio of new drawings, and ask for a first book to illuminate'}, 'chance': 0.03}),
    ('put your savings into a lease, and open a gallery under your own name', 'B1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'put your winter stores behind the best young hands, and carry their hides to the gathering under your own sign', 'magic': 'put your savings into a hall on the square, and open it under your own name'}, 'chance': 0.03}),
    ('ask to teach the boldest of the hopefuls, and stay with them all three years', 'R1', None, 0.45, '', {'title': 'art teacher', 'requires': 'illustrator for hire', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'stimulation, universalism', 'world': {'tribal': 'ask to teach the boldest of the young hands, and stay with them for three winters', 'magic': 'ask to teach the boldest of the hopefuls at the academy, and stay with them all three years'}, 'chance': 0.03}),
    ("gather the town's makers into a shared shop on the high street, and keep its books", 'G1', None, 0.45, '', {'title': 'gallery owner', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'mark': 'made a friend', 'v': 'tradition, benevolence', 'world': {'tribal': 'gather the carvers and painters of your own band into one trading place at the gathering', 'magic': "gather the ward's makers into a shared hall by the market, and keep its books"}, 'chance': 0.03}),
    ('write the school a fairer way to judge a folder, and offer it for next year', 'W.34 U.33 R.33', None, 0.5, '', {'door': True, 'v': 'self-direction, conformity', 'world': {'tribal': 'show the elders a fairer way to judge a young hand, for the next gathering', 'magic': 'write the academy a fairer way to judge a folio, and offer it for next year'}, 'chance': 0.85}),
    ('stay late with the hopefuls turned away, and tell each one what to try next', 'W.34 R.33 G.33', None, 0.5, '', {'self_control': '+', 'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'sit late with the young ones turned away, and tell each one what to try next', 'magic': 'stay late with the hopefuls turned away, and tell each what to try next'}, 'chance': 0.85}),
    ('keep a seat on the panel every year, and the best names in a notebook', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'contact in the trade', 'habit': True, 'v': 'security, tradition', 'world': {'tribal': 'keep a place beside the elders at every judging, and the best young hands in mind', 'magic': "keep a seat on the academy's bench every year, and the best names in a book"}, 'chance': 0.85}),
    ('take the boldest hopeful on as a summer assistant, before the dealer does', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'teaching', 'binds': True, 'v': 'power, stimulation', 'world': {'tribal': 'take the boldest young hand to paint beside you for a summer, before the trader does', 'magic': 'take the boldest hopeful on as a summer apprentice, before the dealer does'}, 'chance': 0.85}),
    ("go home and draw the week's three hundred faces from memory", 'U.34 B.33 G.33', None, 0.5, '', {'self_control': '+', 'mark': 'learned a skill', 'v': 'self-direction, universalism', 'world': {'tribal': 'go home and paint the faces of all the young hands from memory', 'magic': "go home and draw the week's three hundred faces from memory, by candle"}, 'chance': 0.85}),
 ]},
{'name': 'the judge stops at your table at the craft fair',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.02),
 'drivers': 'community+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, making, community',
 'horizon': 'moment',
 'roles': 'friend, partner, colleague, rival, a judge',
 'requires': 'craft maker | master craftsperson',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'the great craft fair on the showground, and the judge of the top award stopping at the table '
                     'to turn a bowl over in her hands',
            'tribal': 'the master carvers of every band laying out their work by the river at the gathering, and the '
                      'eldest of them stopping at the hide to lift a carved bowl',
            'magic': "the midsummer fair of the craft guilds in the cloth hall, and the guild's grand warden "
                     'stopping at the table to turn a bowl in her hands'},
 'timing': {'times': 'per craft maker of three years or master craftsperson of five, a year: about 1 in 50 has a '
                     'judge, a curator or a buyer of note stop at their table at a big fair (estimate); a big craft '
                     'fair hands out one or two top awards among several hundred makers, and very few makers a year '
                     'are chosen for a national collection or a touring show (estimate); about 8 lives in 10,000 '
                     'become master craftspeople and about 1 in 10,000 renowned artists (catalogue shares)',
            'likelier': "a town that keeps its makers, a big fair within a day's drive, years of work at the same "
                        'table, a piece that stops people',
            'rarer': 'a year with no money for the stall, poor health, a fair cancelled by the weather',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'Once a year the makers of half the country set up their tables on the showground for the '
                       'great craft fair: potters, weavers, woodworkers, silversmiths. On the Saturday morning the '
                       "judge of the fair's top award walks the rows, and this year she stops at {Ns} table, picks "
                       'up a bowl, turns it over to look at the foot, and does not put it down. The next three '
                       'tables go quiet. Everyone knows she also chooses work for the national touring show of '
                       "crafts, and for a museum's collection."),
                      ('W',
                       "{N} has made to the guild's standard for years, every joint and every glaze checked twice. "
                       'If the judge is looking for a fault, she will not find one.'),
                      ('U',
                       'The glaze on that bowl took ten years of firing notes to get right, and {N} knows every one '
                       'of its variables. Nobody else at the fair could make it twice.'),
                      ('B',
                       "A judge's stop is worth more than a week of sales, if it is used. {N} notices the "
                       'photographer from the craft magazine drifting over, and straightens the price cards.'),
                      ('R',
                       '{Ns} hands are still grey with clay from the demonstration wheel at the end of the row. {N} '
                       'wants to throw another bowl right now, while she is watching.'),
                      ('G',
                       "The clay is dug from the riverbank below {Ns} grandmother's old farm every autumn, and the "
                       'shape is the one {Ns} teacher taught. {N} would like the judge to know that more than '
                       'anything.')],
            'tribal': [('',
                        'At the great gathering the master carvers of every band lay out their work on hides by the '
                        'river, and the eldest of them walks the rows choosing what will go to the far peoples in '
                        'trade. This summer the eldest stops at {Ns} hide, lifts a carved bowl and turns it in the '
                        'light.')],
            'magic': [('',
                       'At the midsummer fair of the craft guilds the makers of the realm set out their wares in the '
                       "cloth hall, and the guild's grand warden walks the aisles choosing work for the court and "
                       "the guild's masterworks. This year the warden stops at {Ns} table, and turns a bowl in her "
                       'hands.')]},
 'outcomes': (['A letter comes before the winter, and by the spring a piece from {Ns} table is where {N} hoped it '
               'would be, with {Ns} mark on its foot and a waiting list behind it.',
               'Whatever {N} chose, the fair is a good one, and the van goes home lighter than it came.'],
              ['The judge puts the bowl down with a small nod and walks on; the award goes to a weaver three rows '
               'over, and {N} sells the bowl that afternoon to a woman who never heard of the judge.',
               'Nothing comes of it but a photograph in the craft magazine with {Ns} name spelled wrong, which {N} '
               'cuts out and keeps anyway.']),
 'options': [
    ("put the piece forward for the guild's masterpiece, every rule of the guild met", 'W1', None, 0.45, '', {'title': 'master craftsperson', 'requires': 'craft maker', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'conformity, tradition', 'world': {'tribal': 'ask the eldest carver to judge the bowl by the old marks, every one of them met', 'magic': "put the bowl forward for the guild's masterwork, every one of the warden's rules met"}, 'chance': 0.03}),
    ('show the judge the ten years of firing notes behind the glaze', 'U1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'master craftsperson', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': "show the eldest how the bowl's colour was found, winter after winter", 'magic': 'show the warden the ten years of kiln books behind the glaze'}, 'chance': 0.03}),
    ('name a price three times higher, hold to it, and mention the waiting list', 'B1', None, 0.45, '', {'title': 'master craftsperson', 'requires': 'craft maker', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'ask three times the usual trade for the bowl, hold to it, and speak of the bands already waiting', 'magic': 'name a price three times higher, hold to it, and mention the noble houses waiting'}, 'chance': 0.03}),
    ('throw a new bowl at the demonstration wheel, there and then, while the judge watches', 'R1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'master craftsperson', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'carve a new bowl there on the riverbank, while the eldest watches', 'magic': "throw a new bowl on the fair's wheel, there and then, while the warden watches"}, 'chance': 0.03}),
    ('tell the judge where the clay is dug, and who taught the making', 'G1', None, 0.45, '', {'title': 'master craftsperson', 'requires': 'craft maker', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'tell the eldest which riverbank gave the wood, and which old carver taught the making', 'magic': 'tell the warden where the clay is dug, and which old master taught the making'}, 'chance': 0.03}),
    ('take a young maker from the town as an apprentice for a year', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'teaching', 'binds': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'take a young one of the band to sit at your side for a winter, learning the knife', 'magic': "take a young maker of the ward as an apprentice, with the guild's papers"}, 'chance': 0.84}),
    ("agree a fair trade price with the fair's gallery for a dozen pieces every season", 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'contact in the trade', 'habit': True, 'v': 'security, achievement', 'world': {'tribal': 'agree with a coast trader on a dozen bowls each summer, at a fair trade', 'magic': 'agree a price with a hall on the square for a dozen pieces every season'}, 'chance': 0.84}),
    ('book a bigger stall for next year, in the front row by the gate', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'selling', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': "claim a bigger hide by the river crossing for next summer's gathering", 'magic': 'book a larger table for next year, in the front row of the cloth hall'}, 'chance': 0.84}),
    ("spend the evening at the makers' camp, swapping glazes and stories", 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'a circle of artists', 'door': True, 'v': 'stimulation, universalism', 'world': {'tribal': "spend the night at the carvers' fire, trading tricks of the knife and stories", 'magic': "spend the evening in the makers' tavern, swapping glazes and stories"}, 'chance': 0.84}),
    ("chalk the judge's words on the stall's board, and raise the prices by Sunday", 'B.34 R.33 G.33', None, 0.5, '', {'identity': True, 'v': 'power, stimulation', 'world': {'tribal': 'tell everyone at the river what the eldest said, and ask more for every bowl by nightfall', 'magic': "chalk the warden's words on the stall's board, and raise the prices by the last bell"}, 'chance': 0.84}),
 ]},
{'name': 'the poem that silenced the room',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'community, meaning',
 'horizon': 'moment',
 'roles': 'friend, colleague',
 'requires': 'open-mic poet',
 'worlds': {'earth': 'the poetry night at the back of the pub: a new poem read, and the room goes so quiet the '
                     'glasses stop clinking',
            'tribal': "new verses spoken at the band's fire, and the whole band goes still, down to the last child",
            'magic': "a new poem read at the poets' night in the tavern, and the whole taproom falls silent"},
 'timing': {'times': 'per open-mic poet a year: about 1 in 10 read a poem that stops the room dead (estimate); about '
                     '1 life in 100 reads at a poetry night again and again (catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Third on the chalkboard list at the back of the pub, {N} reads the new poem, the one written '
                       'at the kitchen table at two in the morning. When the last line ends there is no applause at '
                       'first, only a silence so deep that the ice can be heard settling in a glass. Then the room '
                       'breaks.'),
                      ('W',
                       "The night has its customs: three minutes each, the host's little bell, names on the "
                       'chalkboard in order. {N} kept to every one of them, and the silence came anyway.'),
                      ('U',
                       '{N} knows which line did it: the turn in the eleventh line, redrafted fourteen times on the '
                       'bus. It is good to know, for certain, that a thing works.'),
                      ('B',
                       'At the back, a woman who edits a small poetry magazine has written something down. {N} '
                       'notices, and notices who else noticed.'),
                      ('R',
                       '{Ns} hands are still shaking on the way back to the table. The poem said the thing that '
                       'could not be said any other way, and the whole room heard it.'),
                      ('G',
                       'The poem was about the street {N} grew up on, and half the room grew up there too. An old '
                       'man by the bar is wiping his eyes with the back of his hand.')],
            'tribal': [('',
                        "At the band's fire, {N} speaks the new verses about the winter the river froze. When they "
                        'end no one speaks; even the children are still, and the old ones look into the flames.')],
            'magic': [('',
                       "At the poets' night in the back room of the tavern, {N} reads the new poem. The taproom goes "
                       'so still that the landlord stops drawing ale halfway through a pour.')]},
 'outcomes': (['The poem is asked for again and again, and {N} goes home with new friends and the names of people '
               'who want more.',
               'For a week the poem goes round, passed from hand to hand and said aloud, and {N} keeps writing.'],
              ["The next poem {N} reads falls flat, and the night's spell does not come back.",
               'The silence turns out to have been one good night, and the notebook stays shut for a month.']),
 'options': [
    ('offer to keep the list and the bell for the host, every month from now on', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'grants': 'a circle of artists', 'world': {'tribal': 'offer to keep the order of the speakers at every fire from now on', 'magic': "offer to keep the readers' list for the landlord at every poets' night from now on"}, 'chance': 0.85}),
    ('ask the quietest listener afterwards which line did it, and note it down', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'writing poems', 'world': {'tribal': 'ask the oldest listener afterwards which words did it, and keep them close', 'magic': 'ask the quietest listener afterwards which line did it, and note it in your book'}, 'chance': 0.8}),
    ('send the editor at the back a new poem every month until one is taken', 'B1', None, 0.45, '', {'v': 'power, achievement', 'habit': True, 'aims': 'novelist', 'world': {'tribal': "send new verses with the next band's teller to every gathering, until some are carried", 'magic': 'send the broadsheet printer from the taproom a new poem every month until one is printed'}, 'chance': 0.5}),
    ('read it again straight away when they shout for more, louder this time', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'world': {'tribal': 'speak the verses again when they call for more, louder, on your feet', 'magic': 'read it again when the taproom calls for more, standing on the bench'}, 'chance': 0.75}),
    ('copy the poem out by hand for the old man by the bar', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'mark': 'made a friend', 'world': {'tribal': 'teach the verses to the old one by the fire, so they stay with the band', 'magic': 'copy the poem out by hand for the old drover by the hearth'}, 'chance': 0.95}),
    ("join the host's monthly workshop, and bring a new draft to every session", 'W1', 'U.7', 0.5, '', {'v': 'achievement, conformity', 'habit': True, 'grants': 'writing poems', 'world': {'tribal': 'sit with the old teller at every new moon, and bring new verses each time', 'magic': "join the poets' circle that meets above the tavern each month, with a new draft every time"}, 'chance': 0.7}),
    ('start shaping a first collection around this poem, to send to publishers', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'binds': True, 'self_control': '+', 'aims': 'novelist', 'world': {'tribal': 'start shaping a long telling around these verses, to speak at the great gathering', 'magic': 'start shaping a first book of poems around this one, to send to the printers'}, 'chance': 0.65}),
    ('talk your way onto the bill at the big slam in the city next week', 'B1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': "ask to speak at the great gathering's fire, before every band, at the next moon", 'magic': "talk your way onto the bill at the great poets' contest in the capital"}, 'chance': 0.55}),
    ('stay at the bar with the other poets till closing, swapping notebooks', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, benevolence', 'habit': True, 'grants': 'a circle of artists', 'world': {'tribal': 'stay by the embers with the other speakers of verses till the stars turn', 'magic': 'stay in the taproom with the other poets till the last bell, swapping books'}, 'chance': 0.9}),
    ("gather the regulars' own poems about the town into a booklet for the library", 'G1', 'W.7', 0.5, '', {'v': 'tradition, universalism', 'world': {'tribal': "gather the band's old verses about the land, and teach them to the young ones at the fire", 'magic': "gather the quarter's own poems into a little booklet for the temple library"}, 'chance': 0.75}),
 ]},
{'name': 'a heckler at the front table',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, meaning',
 'horizon': 'moment',
 'roles': 'friend, colleague',
 'requires': 'open-mic poet',
 'worlds': {'earth': 'the poetry night: a man at the front table, three pints in, talks through the poem and shouts '
                     'that it does not even rhyme',
            'tribal': "at the band's fire, a young hunter back from the chase laughs over the verses and calls them "
                      'babble',
            'magic': "at the tavern's poets' night, a drover deep in his cups bangs his tankard on the front bench "
                     'and jeers at the poem'},
 'timing': {'times': 'per open-mic poet a year: about 1 in 3 read through a heckler or a loud table at the front '
                     '(estimate); about 1 life in 100 reads at a poetry night again and again (catalogue share; '
                     'estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Halfway through {Ns} poem, the man at the front table, three pints in, starts talking to his '
                       'friends over it. Then he turns round and calls out, loud enough for the whole room, that it '
                       'does not even rhyme. Someone laughs. The next line is the hardest one in the poem.'),
                      ('W',
                       'The night has one rule, chalked on the board by the door: listen to the poet. Everyone in '
                       'the room knows it, including him.'),
                      ('U',
                       '{N} has seen good poets lose a room this way, and has thought about what the best of them '
                       'do. The next five seconds are a problem to be solved.'),
                      ('B',
                       'Every eye in the room has turned, and for a moment {N} has more of the room than any poet '
                       'all night. The question is what to do with it.'),
                      ('R',
                       'The blood comes up hot in {Ns} face. The poem is about something real, and he is laughing at '
                       'it.'),
                      ('G',
                       'There is one at every night, sooner or later. The regulars have their way with them, and the '
                       'poem will still be there when he has gone.')],
            'tribal': [('',
                        "At the band's fire, as {N} speaks the new verses, a young hunter back from the chase laughs "
                        'over them and calls them babble. A few of his friends laugh too, and the old ones frown.')],
            'magic': [('',
                       "At the poets' night in the tavern, a drover deep in his cups bangs his tankard on the front "
                       'bench and jeers that the poem would not sell a lame horse. The taproom turns to look.')]},
 'outcomes': (['By the last line the room is back on {Ns} side, and {N} is asked to read again next time.',
               'The heckler goes quiet, and the poem ends to warmer applause than it would have had.'],
              ['The poem is lost under the noise, and {N} sits down before the end.',
               'The night turns sour, and {N} does not go back for a month.']),
 'options': [
    ("stop the poem there, and leave him to the host and the night's rule", 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '-', 'world': {'tribal': 'stop the verses there, and leave him to the elder who keeps the order of the fire', 'magic': 'stop the poem there, and leave him to the landlord and the house rule'}, 'chance': 0.85}),
    ('answer him with a rhyme made up on the spot, and carry on', 'U1', None, 0.45, '', {'v': 'achievement, stimulation', 'identity': True, 'grants': 'public speaking', 'world': {'tribal': 'answer him with a verse made on the spot, and carry on', 'magic': 'answer him with a couplet made on the spot, and carry on'}, 'chance': 0.45}),
    ('turn on him, and play the rest of the set to the room at his expense', 'B1', None, 0.45, '', {'v': 'power, achievement', 'mark': 'made an enemy', 'world': {'tribal': 'turn on him, and keep the band laughing at the hunter for the rest of the night', 'magic': 'turn on him, and play the rest of the night to the taproom at his cost'}, 'chance': 0.75}),
    ('step down off the stage, and read the rest of the poem straight to his face', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'self_control': '+', 'body': 'light', 'world': {'tribal': 'walk round the fire, and speak the rest of the verses straight into his face', 'magic': 'step down off the bench, and read the rest straight into his face'}, 'chance': 0.6}),
    ('let him talk, finish softly for those leaning in, and write him into a poem later', 'G1', None, 0.45, '', {'v': 'universalism, benevolence', 'aims': 'novelist', 'world': {'tribal': 'let him laugh, finish softly for those leaning in, and make a verse of him later', 'magic': 'let him jeer, finish softly for those leaning in, and write him into a poem later'}, 'chance': 0.75}),
    ('sign up for a course in reading aloud, and practise every week', 'W1', 'U.7', 0.5, '', {'v': 'achievement, conformity', 'door': True, 'grants': 'public speaking', 'world': {'tribal': 'ask the old teller to teach you to hold the fire, and practise every night', 'magic': 'take lessons in declaiming from the old herald, and practise every week'}, 'chance': 0.8}),
    ('post the clip of his heckle online, cut to your best comeback', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'mark': 'made an enemy', 'closed': "approval: a stranger filmed and posted without his say; backfire: the clip spreads with the night's name on it, and the host asks the poet to stay away for a while", 'grants': 'following online', 'world': {'tribal': 'make a mocking verse of the hunter, sharp as a flint, and teach it to the young ones', 'magic': "write a broadsheet ballad of the drover's jeer and your answer, and sell it in the square"}, 'chance': 0.4}),
    ('buy him a drink at the break, and have him cheering by the end', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': 'give him a share of your meat at the break, and have him cheering by the end', 'magic': 'stand him an ale at the break, and have him cheering by the end'}, 'chance': 0.8}),
    ('invite him up to read something of his own, if he thinks he can do better', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'mark': 'made a friend', 'world': {'tribal': 'invite him into the firelight to speak a verse of his own', 'magic': 'invite him up onto the bench to read something of his own'}, 'chance': 0.6}),
    ('let the regulars hush him, the way the room has always done', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'let the old ones hush him, as the band has always done', 'magic': 'let the regulars hush him, the way the taproom always has'}, 'chance': 0.65}),
 ]},
{'name': 'the child who draws all through maths',
 'stages': 'young_adult adult mature elder',
 'age': (22, 80),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'colleague, boss',
 'requires': 'art teacher',
 'worlds': {'earth': "the maths teacher brings a pupil's exercise book to the art room: every page of sums has "
                     'drawings in the margins, and they are good',
            'tribal': 'the keeper of the herd count brings a flat stone: the girl meant to cut a mark for each beast '
                      'has drawn every beast instead, alive',
            'magic': "the reckoning master brings the drawing master a pupil's slate: the sums are wrong, and the "
                     'margins are full of horses'},
 'timing': {'times': 'per art teacher a year: most have a pupil or two who draw through other lessons, and about 1 '
                     'in 4 are brought one by a colleague (estimate); about 3 lives in 1,000 teach art (catalogue '
                     'share; about 1 secondary teacher in 25 teaches art and design, the UK and US teaching '
                     'workforce counts)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'At break, {colleague}, who teaches maths, drops an exercise book on {Ns} desk in the art '
                       'room. A boy of twelve has failed every test this term, and every page of sums is crowded '
                       "with drawings: hands, bicycles, a horse, the maths teacher's own face, all of them good."),
                      ('W',
                       'A boy who draws through maths is breaking a rule, and {colleague} is right to be cross. {N} '
                       'also made a promise to every child in the school: that drawing can be learned, properly, by '
                       'anyone who wants it.'),
                      ('U',
                       '{N} turns the pages slowly. The perspective is wrong in an interesting way; nobody taught '
                       'him this, he has worked it out alone.'),
                      ('B',
                       "Work like this could win the schools' competition in the spring, and the art department's "
                       'budget follows its prizes.'),
                      ('R',
                       'The horse on page nine is so alive that {N} laughs out loud. This is the thing itself, the '
                       'thing that cannot be taught.'),
                      ('G',
                       'Every few years one comes along. They need less pushing than room, and time, and someone who '
                       'notices.')],
            'tribal': [('',
                        "The keeper of the herd count brings {N} a flat stone from the children's lesson. A girl of "
                        'the river hearth was meant to cut one mark for each beast in the herd; instead she has '
                        'drawn every beast, and they are alive.')],
            'magic': [('',
                       "The reckoning master puts a pupil's slate on {Ns} table in the academy's drawing hall. The "
                       'sums are wrong from top to bottom, and the margins are full of horses that look ready to '
                       'run.')]},
 'outcomes': (['The child draws in the right places now, and the sums creep up with it.',
               'Years later the child, grown, still draws, and remembers who noticed.'],
              ['The child goes quiet and stops drawing anywhere, even in art.',
               '{colleague} complains to {boss}, and {N} is told to keep out of other subjects.']),
 'options': [
    ('agree a rule with him and his maths teacher: sums first, then the margins are his', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'self_control': '+', 'world': {'tribal': 'agree a rule with her and the keeper: the count first, then the beasts are hers', 'magic': 'agree a rule with the pupil and the reckoning master: sums first, then the margins'}, 'chance': 0.8}),
    ('show him how the geometry from maths would fix his perspective', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'show her how the count of the marks can set the beasts in their right places', 'magic': 'show the pupil how the reckoning of angles would set the horses true'}, 'chance': 0.7}),
    ("enter his best drawings in the schools' competition, with his parents' leave", 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': "carry her stone to the gathering, with her mother's leave, for the traders to see", 'magic': "send the best slate to the academy's prize day, with the parents' leave"}, 'chance': 0.35}),
    ('give him a good sketchbook, and tell him to draw in maths if he must', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'mark': 'defied an authority', 'closed': "approval: a pupil told he may draw in another teacher's lesson; backfire: the maths teacher goes to the head, and the art teacher is warned", 'world': {'tribal': 'give her a smooth stone of her own, and tell her to draw at the count if she must', 'magic': 'give the pupil a sketchbook, and tell them to draw in reckoning if they must'}, 'chance': 0.85}),
    ("talk with his parents at parents' evening about what he loves", 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'grants': 'pupils who remember you', 'world': {'tribal': 'sit with her mother at the hearth, and talk of what the girl loves', 'magic': "talk with the pupil's parents on visiting day about what the child loves"}, 'chance': 0.8}),
    ("put him forward for the gifted pupils' Saturday art course, forms and all", 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': "put her forward to the painter of the great cave, with the elders' word", 'magic': "put the pupil forward for the academy's scholars' bench, with every form signed"}, 'chance': 0.55}),
    ('set him a project: a comic of the maths lesson, drawn properly, frame by frame', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'set her a task: the whole hunt drawn on one hide, beast by beast', 'magic': 'set the pupil a task: the whole reckoning lesson drawn as a picture-story'}, 'chance': 0.75}),
    ("talk the empty shop on the high street into a week's show of the children's work", 'B1', 'G.7', 0.5, '', {'v': 'achievement, benevolence', 'aims': 'gallery owner', 'world': {'tribal': "talk the traders into laying out the children's stones at the great gathering", 'magic': "talk the owner of the empty hall on the square into a week's show of the pupils' drawings"}, 'chance': 0.6}),
    ('stand up for him at the staff meeting when detentions for doodling come up', 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': "speak up for her at the elders' fire when the keeper wants her kept from the stones", 'magic': "speak up for the pupil at the masters' table when punishments for idle drawing come up"}, 'chance': 0.55}),
    ('let him draw at the lunchtime art club, and just watch how he works', 'G1', 'U.7', 0.5, '', {'v': 'universalism, self-direction', 'habit': True, 'grants': 'pupils who remember you', 'world': {'tribal': 'let her draw with the other children at the painting place, and watch how she sees', 'magic': 'let the pupil draw in the drawing hall at midday with the others, and watch how the hand moves'}, 'chance': 0.75}),
 ]},
{'name': 'the art room budget is cut',
 'stages': 'young_adult adult mature elder',
 'age': (22, 80),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'art teacher',
 'worlds': {'earth': "the head's plan for next year: the art room's budget is halved, and the cracked kiln will not "
                     'be mended',
            'tribal': 'the elders say the ochre and the fat for paint must go to the hides this winter',
            'magic': "the academy's bursar halves the drawing master's purse for pigment and paper"},
 'timing': {'times': "per art teacher a year: about 1 in 8 see the art room's budget cut (estimate); about 3 lives "
                     'in 1,000 teach art (catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{boss}, the head, says it kindly and plainly across the desk: next year the art budget is '
                       'halved. Paper, paint and clay for six hundred children on half of not much, and the kiln '
                       'that cracked in the spring will not be mended.'),
                      ('W',
                       "{N} has kept the art room's accounts to the penny for nine years and handed them in on time "
                       'every term. The cut is already in the minutes, signed off by the governors.'),
                      ('U',
                       'On the back of the letter {N} is already working it out: what paper costs, what clay costs, '
                       'what can be made from nothing at all.'),
                      ('B',
                       'The sports hall got a new floor this year. {N} knows which governors decide, and what they '
                       "like to see in the school's brochure."),
                      ('R',
                       'Halved. After the year the children turned the whole hall into a forest. It lands like a '
                       'slap.'),
                      ('G',
                       'Artists have always worked with what was at hand: earth, charcoal, the backs of old posters. '
                       'The children will make things either way.')],
            'tribal': [('',
                        'At the winter council the elders speak: the ochre and the fat are needed for the hides, and '
                        "the children's painting must wait for spring. {N}, who teaches the children the marks and "
                        'the patterns, sits with the empty paint shells.')],
            'magic': [('',
                       "The academy's bursar sends a sealed note: from the new term the drawing master's purse for "
                       'pigment and paper is halved. {N} reads it twice in the cold drawing hall.')]},
 'outcomes': (["Somehow the art room keeps going, and the children's work fills the corridors by summer.",
               'The fight brings new help, from parents, a giver or an old hand, and next year looks less bare.'],
              ['The cut goes through as written, and the kiln stays cold all year.',
               '{N} wins a little back, and makes up the rest from {Ns} own stores all year.']),
 'options': [
    ('report the cut to the schools inspectors as a breach of the curriculum', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'mark': 'defied an authority', 'closed': "approval: going over the head's head to the inspectors; backfire: nothing changes, and the head stops trusting the art room", 'world': {'tribal': 'take the matter to the elders of the other bands at the gathering, as custom allows', 'magic': "write to the academy's visitors that the charter's drawing hours are broken"}, 'chance': 0.4}),
    ('plan a year of art from found things: cardboard, charcoal, river clay, old magazines', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'plan a winter of marks from what the land gives: charcoal, chalk, clay from the river', 'magic': 'plan a year of drawing from scraps: charcoal, chalk, river clay, old broadsheets'}, 'chance': 0.8}),
    ('take the design job a friend has offered, and leave at the end of term', 'B1', None, 0.45, '', {'v': 'power, achievement', 'self_control': '-', 'drops': 'art teacher', 'world': {'tribal': "go to paint shields for the chief's kin, and leave the children's marks to others", 'magic': "take the post a printer has offered, and leave the academy at the term's end"}, 'chance': 0.9}),
    ('paint the school hall with the children in the last week, with whatever paint is left', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'body': 'light', 'grants': 'a mural the town loves', 'world': {'tribal': 'paint the shelter wall with the children before the ochre goes, every hand on it', 'magic': "paint the academy's hall with the pupils in the last week, with every pot that is left"}, 'chance': 0.55}),
    ('bring in wood, wool and clay from home and the allotment, as makers always have', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'gather berries, chalk and soot with the children, as the old ones did', 'magic': "bring in wool, wood and clay from home and the town's gardens, as makers always have"}, 'chance': 0.8}),
    ("set up a parents' committee for the art room, with a treasurer and minutes", 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'grants': 'organising people', 'world': {'tribal': "gather the mothers into a council for the children's paints, each with her task", 'magic': 'found a friends-of-the-drawing-hall society, with a treasurer and a seal'}, 'chance': 0.7}),
    ('write the children a project they run themselves: a gallery of junk sculpture', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, achievement', 'world': {'tribal': 'set the children a game: beasts made from bones, twigs and stones, each one their own', 'magic': 'set the pupils a task they run themselves: a gallery of scrap sculpture'}, 'chance': 0.75}),
    ("get the builders' merchant in town to give the paint, for a thank-you on the wall", 'B1', 'G.7', 0.5, '', {'v': 'achievement, benevolence', 'mark': 'made a friend', 'world': {'tribal': 'trade a carved horn to the next band for ochre for the children', 'magic': 'get the paint-seller on the square to give the pigment, for his name on the wall'}, 'chance': 0.7}),
    ("walk into the governors' meeting unannounced, arms full of the children's work", 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': "walk into the elders' council unbidden, arms full of the children's painted stones", 'magic': "walk into the council's sitting unbidden, arms full of the pupils' drawings"}, 'chance': 0.45}),
    ("ask the town's retired art teachers how they got through the lean years", 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'door': True, 'world': {'tribal': 'ask the oldest painter how the children were taught in the hungry winters', 'magic': "ask the town's old drawing masters how they managed in the lean years"}, 'chance': 0.7}),
 ]},
{'name': 'an artist leaves for a bigger gallery',
 'stages': 'young_adult adult mature elder',
 'age': (25, 90),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague, rival',
 'requires': 'gallery owner',
 'worlds': {'earth': 'the painter the gallery gave a first show six years ago is leaving for a big gallery in the '
                     'capital, with eleven paintings still in the storeroom',
            'tribal': 'the carver whose pieces the trader has carried to every great gathering will go now with a '
                      "richer band's trader",
            'magic': 'the painter the hall on the square made is leaving for a grand house in the capital, with '
                     'eleven canvases still in the store'},
 'timing': {'times': 'per gallery owner a year: about 1 in 6 lose an artist they launched to a bigger gallery '
                     '(estimate); about 3 lives in 10,000 run a gallery (catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{colleague}, the painter {N} gave a first show six years ago, comes in on a Monday morning '
                       'with flowers and bad news: a big gallery in the capital has offered to represent the work. '
                       'Eleven paintings are still in {Ns} storeroom on consignment, and three collectors are '
                       'waiting on the next show.'),
                      ('W',
                       "The contract says three months' notice, and the consignment terms are written down. {N} "
                       'wrote them to protect both sides, and they will.'),
                      ('U',
                       '{N} wonders what the big gallery saw, what it will charge, and what this gallery could learn '
                       'from either.'),
                      ('B',
                       'Six years of building that name, wall by wall and buyer by buyer, and {rival} in the capital '
                       'will now sell it. {N} has not finished with this yet.'),
                      ('R', 'It stings more than {N} would ever say aloud. It feels like being left.'),
                      ('G',
                       'Galleries like this one are where artists start, and starting is what they are for. It has '
                       'happened before, and it will happen again.')],
            'tribal': [('',
                        '{colleague}, the carver whose pieces {N} has carried to every great gathering for six '
                        'summers, comes to {Ns} fire with a gift and bad news: a trader from a richer band will '
                        'carry the carvings now. Eleven pieces still sit in {Ns} shelter.')],
            'magic': [('',
                       '{colleague}, the painter {N} first hung in the hall on the square, comes with flowers and '
                       'bad news: a grand house in the capital has offered to take the work. Eleven canvases are '
                       'still in {Ns} store.')]},
 'outcomes': (["The parting is clean, and the artist's name keeps pointing back to where it started.",
               'A new maker turns up within the month, and the empty place fills again.'],
              ['The best spot stands empty for a season, and the trade falls with it.',
               'Word goes round the trade that {N} handled it badly.']),
 'options': [
    ("hold to the contract: three months' notice, and the consignment settled to the penny", 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': "hold to the old terms: a season's notice, and every piece returned or traded as agreed", 'magic': "hold to the contract: a quarter's notice, and the consignment settled to the last coin"}, 'chance': 0.9}),
    ("ask the big gallery's director to lunch, and learn how they price and pick", 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'door': True, 'grants': 'contact in the trade', 'world': {'tribal': "sit with the rich band's trader at the gathering, and learn what he asks and why", 'magic': "dine with the grand house's keeper, and learn how the capital prices and picks"}, 'chance': 0.7}),
    ('make sure every story about the move says where the artist was found', 'B1', None, 0.45, '', {'v': 'power, achievement', 'identity': True, 'grants': 'a name in the art world', 'world': {'tribal': "make sure every band hears whose trading first carried the carver's name", 'magic': 'make sure every salon hears which hall on the square found the painter'}, 'chance': 0.7}),
    ('tell the artist exactly how it feels, then take them out for a drink anyway', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'world': {'tribal': "tell the carver straight how it feels, then share the night's meat anyway", 'magic': 'tell the painter straight how it feels, then stand them a supper anyway'}, 'chance': 0.85}),
    ('throw the artist a farewell night in the gallery, and let them go with thanks', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'mark': 'made a friend', 'world': {'tribal': 'hold a farewell fire for the carver, and let them go with thanks', 'magic': 'hold a farewell evening in the hall, and let the painter go with thanks'}, 'chance': 0.85}),
    ('release the artist from the notice in writing, so they can go at once', 'W1', 'R.7', 0.5, '', {'v': 'universalism, self-direction', 'world': {'tribal': "release the carver from the season's terms before the elders, so they can go at once", 'magic': 'release the painter from the notice under seal, so they can go at once'}, 'chance': 0.9}),
    ("write the gallery's history of its first artists, with this one's first show at its heart", 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'self_control': '+', 'world': {'tribal': "teach the young ones the story of the trading, with the carver's first pieces at its heart", 'magic': "write the chronicle of the hall's first painters, with this one's first showing at its heart"}, 'chance': 0.75}),
    ('keep the unsold paintings back until the notice is served to the day', 'B1', 'W.7', 0.5, '', {'v': 'power, security', 'closed': "approval: an artist's own work held back as leverage; backfire: the new gallery's lawyer writes, and the story goes round the trade", 'world': {'tribal': "keep the carvings in your shelter until the season's terms are kept to the day", 'magic': "keep the unsold canvases back until the quarter's notice is served to the day"}, 'chance': 0.75}),
    ('drive to the capital that night to see the big gallery for yourself', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'door': True, 'world': {'tribal': "walk through the night to the rich band's camp to see the trader for yourself", 'magic': 'take the night coach to the capital to see the grand house for yourself'}, 'chance': 0.85}),
    ("let the town's old collectors know over dinner that the artist left for money", 'G1', 'B.7', 0.5, '', {'v': 'power, tradition', 'self_control': '-', 'mark': 'made an enemy', 'closed': 'approval: an old friend run down behind their back; backfire: it gets back to the artist, and the trade hears it too', 'world': {'tribal': 'let the old families know at their hearths that the carver left for richer gifts', 'magic': "let the quarter's old patrons know at supper that the painter left for gold"}, 'chance': 0.6}),
 ]},
{'name': "a buyer wants a discount behind the artist's back",
 'stages': 'young_adult adult mature elder',
 'age': (25, 90),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'colleague',
 'requires': 'gallery owner',
 'worlds': {'earth': 'a collector will buy the largest painting in the show today, at a third off, if the artist is '
                     'never told',
            'tribal': "a far band's trader will take the great carving today if the small one goes with it, and the "
                      'carver is never told',
            'magic': "a lord's steward will buy the great canvas today at a third off, if the painter never hears of "
                     'it'},
 'timing': {'times': 'per gallery owner a year: several times a year a buyer asks for a discount, and about 1 in 5 '
                     'owners are asked to keep one from the artist (estimate); about 3 lives in 10,000 run a gallery '
                     '(catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The collector has been round the show three times. In front of the largest painting he '
                       'lowers his voice: he will buy it today if {N} takes a third off. The artist need never know; '
                       'the gallery can take its cut, and the price on the paperwork can say whatever {N} likes.'),
                      ('W',
                       "The artist's contract sets the price and the split, and both are in {Ns} own handwriting. A "
                       "discount is the artist's to give."),
                      ('U',
                       '{N} reads the collector: a careful man who wants to feel clever more than he wants the '
                       'money. There is a price at which both can be true.'),
                      ('B',
                       "A third off is still a sale, the biggest of the season, and the gallery's rent is due on "
                       'Friday.'),
                      ('R', 'The cheek of it. {N} feels the answer rising before the man has finished talking.'),
                      ('G',
                       'The painting took {colleague} a whole winter. It will find its wall, and its person, in its '
                       'own time.')],
            'tribal': [('',
                        'At the great gathering a trader from a far band turns the great carving in his hands. He '
                        'will take it today, he says, if {N} puts the small one in with it, and the carver back at '
                        'the camp need never know.')],
            'magic': [('',
                       "A lord's steward stands before the great canvas in the hall on the square. His master will "
                       'buy it today, he murmurs, at a third off, if the painter never hears of it.')]},
 'outcomes': (['The work goes to a good home, and the artist knows exactly how and for how much.',
               'The collector comes back for more, and {N} keeps both the buyer and the artist.'],
              ['The buyer walks away, and the work is still unsold when the season ends.',
               'The artist hears how the sale was handled, and the next show goes elsewhere.']),
 'options': [
    ("tell him plainly the gallery never discounts behind an artist's back", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'world': {'tribal': "tell him plainly that no trade is made behind a carver's back", 'magic': "tell him plainly the hall never sells cheap behind a painter's back"}, 'chance': 0.75}),
    ('agree, and enter the sale at a price the artist will never think to question', 'U1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'self_control': '-', 'closed': "approval: the artist's share cut in secret; backfire: the artist sees the real price in the collector's sale catalogue, and leaves with the rest of the work", 'world': {'tribal': 'agree, and tell the carver the trader drove a harder bargain than he did', 'magic': 'agree, and enter the sale in the ledger at a price the painter will never query'}, 'chance': 0.85}),
    ('hold the price: he wants it, and he will be back by Friday', 'B1', None, 0.45, '', {'v': 'power, achievement', 'self_control': '+', 'grants': 'striking a deal', 'world': {'tribal': 'hold to the price: he wants it, and he will be back before the gathering ends', 'magic': "hold the price: his master wants it, and the steward will be back by the week's end"}, 'chance': 0.65}),
    ('tell him what the offer says about him, and show him the door', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'identity': True, 'world': {'tribal': 'tell him what the offer says about him, and turn your back', 'magic': 'tell him what the offer says about his master, and show him the door'}, 'chance': 0.9}),
    ('let the painting wait on the wall for a buyer who will pay what it asks', 'G1', None, 0.45, '', {'v': 'universalism, tradition', 'self_control': '+', 'world': {'tribal': 'keep the carving by the fire for a trader who will give what it is worth', 'magic': 'let the canvas hang for a buyer who will pay what it asks'}, 'chance': 0.5}),
    ('ring the artist from the back office, and let them decide, here and now', 'W1', 'R.7', 0.5, '', {'v': 'universalism, self-direction', 'mark': 'kept your word', 'world': {'tribal': "send a runner to the carver's camp, and let the carver decide", 'magic': "send a boy running to the painter's lodging, and let the painter decide"}, 'chance': 0.75}),
    ('show him the sketchbooks and the valley it was painted in, till the price makes sense', 'U1', 'G.7', 0.5, '', {'v': 'universalism, achievement', 'grants': "works in collectors' hands", 'world': {'tribal': 'tell him of the tree the carving came from and the winters it took', 'magic': "show him the painter's sketches and the valley it was painted in, till the price makes sense"}, 'chance': 0.6}),
    ('say yes, and pay the artist their full share out of your own cut', 'B1', 'W.7', 0.5, '', {'v': 'benevolence, power', 'self_control': '+', 'grants': "works in collectors' hands", 'world': {'tribal': 'say yes, and give the carver a full share out of your own', 'magic': 'say yes, and pay the painter a full share from your own cut'}, 'chance': 0.9}),
    ("take the buyer to the artist's studio that afternoon, and let them talk", 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': "walk the trader to the carver's fire that day, and let them talk", 'magic': "walk the steward to the painter's garret that afternoon, and let them talk"}, 'chance': 0.6}),
    ('offer him a smaller work at its price, and let him grow into a collector', 'G1', 'B.7', 0.5, '', {'v': 'achievement, tradition', 'world': {'tribal': 'offer him a small carving at its worth, and let him come back each summer', 'magic': 'offer the steward a smaller canvas at its price, and let his master grow into a patron'}, 'chance': 0.45}),
 ]},
{'name': 'an apprentice asks to learn the craft',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'colleague, mentor',
 'requires': 'master craftsperson | craft maker',
 'worlds': {'earth': 'a young woman of nineteen at the workshop door asks to learn the craft; she cannot pay, and '
                     'she says she will sweep the floors',
            'tribal': 'a youth from another hearth has sat at the edge of the carving place every day for a moon, '
                      'and now asks to learn',
            'magic': "a lad of the town asks to be bound apprentice, though the guild's rolls say the workshop "
                     'already has its share'},
 'timing': {'times': 'per craft maker or master a year: about 1 in 8 are asked by someone young to teach them the '
                     'craft (estimate); about 5 lives in 1,000 make and sell crafts, and about 8 in 10,000 become '
                     'master craftspeople (catalogue shares; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'A young woman of nineteen has stood outside the workshop window on and off for a week. Today '
                       'she comes in, holding a small wooden spoon she carved herself with a kitchen knife, and asks '
                       '{N} to teach her the craft. She cannot pay. She will sweep the floors.'),
                      ('W',
                       'The guild has rules for this: written terms, four years, a test piece at the end, and a '
                       'master who has earned the right to teach. {N} has lived by them.'),
                      ('U',
                       '{N} turns the spoon over. The grain is cut the wrong way and the bowl is lopsided, but she '
                       'has understood something about the wood that took {N} years.'),
                      ('B',
                       'The waiting list is eleven months long. Another pair of hands, even untrained ones, would '
                       'mean more pieces out of the door.'),
                      ('R',
                       '{N} remembers standing at a door just like this one, at about her age, burning to start.'),
                      ('G',
                       '{mentor} took {N} in like this, long ago, from nothing. Crafts live by being handed on, or '
                       'they do not live at all.')],
            'tribal': [('',
                        'A youth from another hearth has come to the edge of the carving place every day for a moon, '
                        'watching {Ns} hands. Today the youth sets down a small bird cut from bone with a flint, and '
                        'asks to learn.')],
            'magic': [('',
                       'A lad of the town stands in the workshop with his cap in his hands and a crooked little box '
                       "he made himself. He asks to be bound apprentice, though the guild's rolls say {Ns} workshop "
                       'already has its share.')]},
 'outcomes': (["Years on, the apprentice's work is hard to tell from {Ns} own.",
               'The workshop is busier and louder, and {N} learns nearly as much as {N} teaches.'],
              ['The apprentice drifts away within the year, and the bench stands empty again.',
               'The arrangement sours, and word of it gets round.']),
 'options': [
    ('take her on with written terms: hours, safety, tools back where they hang', 'W1', None, 0.45, '', {'v': 'conformity, security', 'binds': True, 'world': {'tribal': 'take the youth on before the elders, with the old terms said aloud', 'magic': "take the lad on with indentures signed before the guild's clerk"}, 'chance': 0.85}),
    ('set her a test piece first: one joint, cut true, before saying yes', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'set the youth a test first: one bird, cut true, before saying yes', 'magic': 'set the lad a test piece first: one joint, cut true, before saying yes'}, 'chance': 0.7}),
    ('say yes, if she works the first year for nothing', 'B1', None, 0.45, '', {'v': 'power, achievement', 'closed': "law: a year's work with no wage; backfire: she leaves after six months, and the town hears how she was used", 'world': {'tribal': 'say yes, if the youth hunts for your hearth all winter in return', 'magic': 'say yes, if the lad works the first year for bread and a bench'}, 'chance': 0.9}),
    ('hand her a chisel there and then, and start her on a real piece', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'body': 'light', 'world': {'tribal': 'hand the youth a flint there and then, and start on a real piece', 'magic': 'hand the lad a chisel there and then, and start him on a real piece'}, 'chance': 0.7}),
    ('let her sweep and watch for a season, as you once did for your own master', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'world': {'tribal': 'let the youth sit and watch for a season, as you once did', 'magic': 'let the lad sweep and watch for a season, as you once did for your master'}, 'chance': 0.6}),
    ("go the guild's way: your own masterpiece judged first, then four years of hers", 'W1', 'G.7', 0.5, '', {'v': 'tradition, conformity', 'self_control': '+', 'grants': "a maker's hallmark", 'aims': 'master craftsperson', 'world': {'tribal': "go the old way: earn the band's sign beside your own first, then teach the youth four winters", 'magic': "go the guild's way: your own masterpiece passed first, then the lad's four years"}, 'chance': 0.35}),
    ('write down every step of the craft for her, the first manual the workshop has had', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'make a cord of knotted marks for each step of the craft, for the youth to follow', 'magic': "write down every step of the craft for the lad, the workshop's first book of practice"}, 'chance': 0.7}),
    ('take her on, and have her teach you the design software she learned at college', 'B1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'door': True, 'mark': 'learned a skill', 'act': 'take her on, and have her teach them the design software she learned at college', 'world': {'tribal': "take the youth on, and learn the other hearth's way of cutting bone in return", 'magic': "take the lad on, and learn the new joint his father's shop uses in return"}, 'chance': 0.85}),
    ('take her on, and enter the big craft fair together this autumn under your name', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, achievement', 'binds': True, 'aims': 'master craftsperson', 'world': {'tribal': 'take the youth on, and carry your pieces together to the great gathering this summer', 'magic': 'take the lad on, and take a stall together at the great autumn fair'}, 'chance': 0.55}),
    ("teach her the old way, by eye and hand, and skip the guild's papers", 'G1', 'R.7', 0.5, '', {'v': 'tradition, self-direction', 'binds': True, 'grants': 'pupils who remember you', 'closed': "approval: an apprentice taught without the guild's papers; backfire: the guild hears, and her years do not count toward a mark of her own", 'world': {'tribal': "teach the youth by eye and hand, and never ask the elders' leave", 'magic': "teach the lad by eye and hand, and never enter him on the guild's rolls"}, 'chance': 0.7}),
 ]},
{'name': 'a machine-made copy in the shop window',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague',
 'requires': 'master craftsperson | craft maker',
 'worlds': {'earth': "in a homeware shop on the high street, a machine-made copy of the maker's best-known bowl, at "
                     'a tenth of the price',
            'tribal': "a trader at the gathering offers carvings cut in the maker's own pattern by careless hands, "
                      'for a tenth of the gifts',
            'magic': "in a shop on the square, a stack of mould-pressed copies of the maker's best jug, at a tenth "
                     'of the price'},
 'timing': {'times': 'per craft maker or master a year: about 1 in 20 find a design of their own copied for sale by '
                     'a firm (estimate); about 5 lives in 1,000 make and sell crafts (catalogue share of the craft '
                     'maker; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'On the way to the post office, {N} stops dead in front of the homeware shop on the high '
                       'street. In the window, stacked twelve high, is {Ns} best-known bowl: the same shape, the '
                       'same glaze, pressed by a machine somewhere far away, at a tenth of the price. A little card '
                       'says handmade style.'),
                      ('W',
                       "Somewhere there must be a rule against this. {N} has paid the guild's fees for twenty years "
                       'for exactly this kind of day.'),
                      ('U',
                       '{N} looks closely through the glass. The foot ring is wrong, the glaze is sprayed, and the '
                       'rim is too even. A machine copied a photograph, not the bowl.'),
                      ('B',
                       'A tenth of the price, and a window on the high street. The firm has found buyers {N} never '
                       'reached, and that is worth knowing.'),
                      ('R',
                       '{Ns} hands are fists before {N} knows it. Twenty years of work, stacked twelve high under a '
                       'card that says handmade style.'),
                      ('G',
                       'Makers have been copied for as long as there have been makers. The real thing is still the '
                       'real thing, and the people who hold one know it.')],
            'tribal': [('',
                        'At the great gathering a trader from downriver has a whole hide spread with carvings cut in '
                        '{Ns} own pattern by careless hands, and he is letting them go for a tenth of the gifts {Ns} '
                        'carvings fetch.')],
            'magic': [('',
                       'In the window of a shop on the square, {N} sees a stack of jugs pressed in a mould from {Ns} '
                       'own best design, sold at a tenth of the price under a card that says in the old style.')]},
 'outcomes': (['The real work holds its own, and the people who want it find their way to {N}.',
               'The copies fade within the season, and {Ns} name stands a little taller for the fight.'],
              ['The copies sell by the dozen, and {Ns} own orders thin that year.',
               'Nothing {N} does touches the copier, and the copies stay on sale all year.']),
 'options': [
    ('ask the guild to name the shop at its meeting, and call for a boycott', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'made an enemy', 'closed': "approval: a firm named as copyists before any finding; backfire: the firm's lawyer writes to the guild, and the guild withdraws the notice with an apology", 'world': {'tribal': "ask the elders to name the trader at the gathering's fire, and turn every band from him", 'magic': 'ask the guild to cry the shop as a copier at its hall, and bar its trade'}, 'chance': 0.6}),
    ('study the copy, and change the design so no mould could ever take it', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': 'study the copies, and change your pattern so no careless hand can follow it', 'magic': 'study the copy, and change the design so no mould can ever take it'}, 'chance': 0.75}),
    ('have a lawyer write to the firm over the design, and ask for a licence fee', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': "go to the trader's elders, and ask a share of every carving cut in your pattern", 'magic': "have a notary write to the shop's master over the design, and ask a fee"}, 'chance': 0.4}),
    ('buy one, and break it on the pavement in front of the shop', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'mark': 'broke the law', 'self_control': '-', 'closed': 'law: a scene in the street and broken pottery on the pavement; backfire: a police officer takes a name, and the photograph is in the local paper', 'world': {'tribal': 'snatch up one of the copies, and smash it on a rock before the trader', 'magic': 'buy one, and smash it on the cobbles before the shop door'}, 'chance': 0.9}),
    ('let it be: whoever holds the real thing knows the difference', 'G1', None, 0.45, '', {'v': 'universalism, tradition', 'world': {'tribal': 'let it be: whoever holds a real carving knows the difference', 'magic': 'let it be: whoever holds the real jug knows the difference'}, 'chance': 0.6}),
    ("apply for the guild's hallmark, so every real piece carries the maker's mark", 'W1', 'G.7', 0.5, '', {'v': 'tradition, conformity', 'grants': "a maker's hallmark", 'aims': 'master craftsperson', 'world': {'tribal': "ask the elders' leave to cut the band's sign beside your own on every real piece", 'magic': 'send your best piece to the guild for its mark, so every true jug carries it'}, 'chance': 0.35}),
    ('label every piece with its making: the clay, the firing, the hours, the maker', 'U1', 'W.7', 0.5, '', {'v': 'universalism, achievement', 'habit': True, 'world': {'tribal': 'cut into every piece the marks of its making: the wood, the moons it took, the hand', 'magic': 'tag every piece with its making: the clay, the firing, the hours, the maker'}, 'chance': 0.75}),
    ('sell the firm the design for a fee, and put it toward a bigger kiln', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'binds': True, 'grants': 'selling', 'world': {'tribal': 'trade the pattern to the trader for a good stone axe, and keep cutting', 'magic': 'sell the shop the design for silver, and put it toward a bigger kiln'}, 'chance': 0.7}),
    ('set up a stall outside the shop with the real ones, and sell all afternoon', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, achievement', 'self_control': '+', 'grants': 'selling', 'world': {'tribal': "spread your own carvings on a hide beside the trader's, and trade all day", 'magic': 'set up a stall outside the shop with the true jugs, and cry them all afternoon'}, 'chance': 0.5}),
    ('make the next batch freer and wilder, every piece different from the last', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'identity': True, 'world': {'tribal': 'cut the next carvings freer and wilder, every one different', 'magic': 'throw the next batch freer and wilder, every jug unlike the last'}, 'chance': 0.7}),
 ]},
{'name': 'the model does not turn up',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'making, friends',
 'horizon': 'moment',
 'roles': 'mentor, colleague',
 'requires': 'life-drawing regular',
 'worlds': {'earth': "the Tuesday life class at the college: easels in a ring, the heater on, and the booked model's "
                     'phone going to voicemail',
            'tribal': 'the painting place under the overhang: ochre ground, torches lit, and the one who was to '
                      'stand for the drawing not come',
            'magic': "the academy's evening hall: lamps trimmed, boards set out, and word that the hired sitter "
                     'cannot come'},
 'timing': {'times': 'per life-drawing regular a year: about 1 in 3 meet an evening when the booked model is ill or '
                     'does not come (estimate); about 15 lives in 1,000 draw at a weekly class for a year or more '
                     '(catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "Seven o'clock on Tuesday at the college. Twelve easels stand in a ring round an empty dais "
                       'with a chair and a heater on it, and {mentor}, the tutor, is ringing the booked model for '
                       'the third time. Nobody answers, and the class has paid for two hours.'),
                      ('W',
                       'The class runs on a few quiet rules: the tutor sets the poses, nobody talks over the work, '
                       'everyone gets their two hours. {N} paid for a model booked through the college, and the '
                       'college has let the class down.'),
                      ('U',
                       'An empty dais is a problem to solve. {N} remembers that the old academies drew plaster '
                       'casts, skeletons and one another when a sitter failed, and wonders which would teach the '
                       'most in two hours.'),
                      ('B',
                       'Two hours paid for and nothing on the dais. {N} works out what can still be got out of the '
                       'evening, and who in the room might be worth knowing better.'),
                      ('R',
                       '{N} came straight from work with the whole day still buzzing, wanting to draw something, '
                       'anything, fast. The empty chair is almost funny.'),
                      ('G',
                       'The radiator ticks, rain runs down the tall windows, and the old plaster casts stand in the '
                       'corner as they have for fifty years. There is plenty in the room to draw, if anyone looks.')],
            'tribal': [('',
                        'Under the overhang the ochre is ground and the torches are lit, but the young hunter who '
                        'was to stand with his spear for the drawing has not come down from the camp. The others '
                        'look at the bare rock, and then at each other.')],
            'magic': [('',
                       "In the academy's evening hall the lamps are trimmed and the drawing boards set out, but a "
                       'boy brings word that the hired sitter is ill and will not come tonight. The drawing master '
                       'looks at the clock and sighs.')]},
 'outcomes': (['The two hours are not wasted, and {N} goes home with something worth keeping.',
               'By the end of the night the others feel more like friends than strangers.'],
              ['The evening drags, and half the group leaves early.',
               'Nobody can agree what to do, and the night ends early in a bad mood.']),
 'options': [
    ('write to the college that this model should not be booked again', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'made an enemy', 'closed': 'approval: a complaint made before anyone knows why the model missed; backfire: the model was in hospital, and the class turns cold on whoever complained', 'world': {'tribal': 'tell the oldest painter that the one who failed to come should never stand for the drawing again', 'magic': "write to the academy's steward that this sitter should not be hired again"}, 'chance': 0.75}),
    ('draw the plaster casts in the corner, slowly, the way the old academies taught', 'U1', None, 0.45, '', {'habit': True, 'v': 'achievement, conformity', 'mark': 'learned a skill', 'grants': 'drawing and painting', 'world': {'tribal': 'draw the old carved horse on the ledge, slowly, the way the old painters did', 'magic': "draw the academy's plaster casts, slowly, as the old masters were taught"}, 'chance': 0.75}),
    ('spend the two hours on your own portfolio, and show it to the tutor after', 'B1', None, 0.45, '', {'v': 'achievement, power', 'aims': 'painter or sculptor', 'world': {'tribal': 'spend the night on your own marks, and show them to the oldest painter after', 'magic': 'spend the evening on your own portfolio, and show it to the drawing master after'}, 'chance': 0.8}),
    ('pin a huge sheet to the wall, and draw the whole room, big and fast', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'aims': 'street artist', 'body': 'light', 'world': {'tribal': 'take a burnt stick, and draw the whole painting place on the rock, big and fast', 'magic': 'pin a great sheet to the wall, and draw the whole hall, big and fast'}, 'chance': 0.85}),
    ('draw the empty chair, the heater and the rain on the windows', 'G1', None, 0.45, '', {'v': 'universalism, tradition', 'world': {'tribal': 'draw the bare rock, the torches and the rain beyond the overhang', 'magic': 'draw the empty chair, the lamps and the rain on the leaded panes'}, 'chance': 0.85}),
    ('set up a rota so everyone sits five minutes in their coat, and draw fast', 'W1', 'R.7', 0.5, '', {'v': 'conformity, stimulation', 'world': {'tribal': 'set a turn for each to stand a short while in their furs, and draw fast', 'magic': 'set a rota so each sits a few minutes in their cloak, and draw fast'}, 'chance': 0.8}),
    ("pair everyone up to draw each other, and learn the class's faces properly", 'U1', 'G.7', 0.5, '', {'v': 'benevolence, achievement', 'mark': 'made a friend', 'world': {'tribal': 'pair the painters off to draw one another, and learn each face properly', 'magic': 'pair the sketchers off to draw one another, and learn each face properly'}, 'chance': 0.75}),
    ('press the college for a free session next term, for the whole class', 'B1', 'W.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'press the elders for another night at the rock, for everyone who came', 'magic': "press the academy's steward for a free evening next term, for the whole hall"}, 'chance': 0.7}),
    ('draw the tutor pacing about on the phone, to learn how a body moves', 'R1', 'U.7', 0.5, '', {'habit': True, 'v': 'stimulation', 'world': {'tribal': 'draw the oldest painter pacing under the overhang, to learn how a body moves', 'magic': 'draw the drawing master pacing by the door, to learn how a body moves'}, 'chance': 0.75}),
    ('take the class to the pub after, and plan a group show together', 'G1', 'B.7', 0.5, '', {'door': True, 'v': 'achievement', 'grants': 'a circle of artists', 'world': {'tribal': 'take the painters to the fire after, and plan to show your marks at the gathering together', 'magic': "take the sketchers to the tavern after, and plan a showing of the hall's work together"}, 'chance': 0.75}),
 ]},
{'name': 'someone wants to buy the sketch off the easel',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'making, money',
 'horizon': 'moment',
 'roles': 'mentor, colleague',
 'requires': 'life-drawing regular',
 'worlds': {'earth': 'the end of the life class: someone waiting for the tutor stops at your charcoal drawing and '
                     'asks what you want for it',
            'tribal': 'a trader resting at the camp sees the hide you drew on and holds out a flint blade for it',
            'magic': "a merchant's wife fetching her son from the evening hall asks the price of your sketch"},
 'timing': {'times': 'per life-drawing regular a year: about 1 in 10 are asked whether a drawing from the class is '
                     'for sale; most class drawings are never sold, and a first sale is a small thing people '
                     'remember (estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "Nine o'clock, the end of the Tuesday class. The model has been paid and gone home, the "
                       'easels are being folded, and a man who has come to collect {mentor}, the tutor, stops in '
                       'front of {Ns} charcoal drawing of the seated pose and asks, quite seriously, what {N} wants '
                       'for it.'),
                      ('W',
                       'The model agreed to sit for a class, and the college has rules about the work made in it. '
                       '{N} is not sure the drawing is {Ns} alone to sell, and would like to do this properly.'),
                      ('U',
                       'It is a two-hour drawing, and {N} can see every place where it went wrong: the foreshortened '
                       'arm, the hand that never came right. A buyer would not see those, but {N} does.'),
                      ('B',
                       'Nobody has ever offered {N} money for a drawing before. The first price sets the next one, '
                       'and {N} knows it.'),
                      ('R',
                       '{N} is still buzzing from two hours of drawing, and a stranger wants the thing {N} just '
                       'made. The urge is to hand it straight over.'),
                      ('G',
                       'The drawing is one of hundreds in the stack at home, one Tuesday out of years of Tuesdays. '
                       'Somebody wanting it is a surprise, like finding something growing that nobody planted.')],
            'tribal': [('',
                        'As the painters wash the ochre from their hands, a trader from the coast, resting at the '
                        'camp, stops at the hide on which {N} drew the young hunter standing, and holds out a fine '
                        'blade of flint for it.')],
            'magic': [('',
                       "As the evening hall empties, a merchant's wife who has come to fetch her son stops at {Ns} "
                       'board and asks, in front of the drawing master, what the sketch would cost.')]},
 'outcomes': (['The drawing goes to someone who wanted it, and {N} walks home lighter.',
               'Word goes round, and soon two more people ask to see {Ns} drawings.'],
              ['The buyer loses interest, and the drawing goes back in the stack.',
               'It goes for less than it was worth, and {N} feels foolish all the way home.']),
 'options': [
    ("ask the tutor what the class's rules say about selling, and go by them", 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'ask the oldest painter whether marks made at the painting place may be traded, and go by it', 'magic': "ask the drawing master what the academy's rules say about selling, and go by them"}, 'chance': 0.8}),
    ('say it is not finished, and offer a better one worked up from it next week', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, conformity', 'world': {'tribal': 'say it is not finished, and offer a better hide worked up from it by the next moon'}, 'chance': 0.7}),
    ('name a price twice what you first thought of, and offer to draw to order', 'B1', None, 0.45, '', {'v': 'power, achievement', 'aims': 'illustrator for hire', 'world': {'tribal': 'ask for two blades, not one, and offer to mark anything else the trader wants', 'magic': 'name a price twice what you first thought of, and offer to draw to order'}, 'chance': 0.6}),
    ('sell it for whatever is in their pocket, and buy the class a round', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'grants': 'a circle of artists', 'world': {'tribal': 'trade it for whatever the trader carries, and share it out among the painters', 'magic': 'sell it for whatever is in her purse, and buy the hall a round'}, 'chance': 0.9}),
    ('let them have it for whatever they think it is worth', 'G1', None, 0.45, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'let the trader give whatever he thinks it is worth', 'magic': 'let her have it for whatever she thinks it is worth'}, 'chance': 0.9}),
    ('sell it at a fair price, and spend it on a day off to paint', 'W1', 'R.7', 0.5, '', {'v': 'conformity, stimulation', 'world': {'tribal': 'trade it at a fair price, and spend what it fetches on a day away from the hunt to paint'}, 'chance': 0.8}),
    ('ask the buyer what they see in it, and listen properly before deciding', 'U1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'mark': 'made a friend', 'world': {'tribal': 'ask the trader what he sees in it, and listen properly before deciding', 'magic': 'ask her what she sees in it, and listen properly before deciding'}, 'chance': 0.8}),
    ('sell it, and strike a deal that a share goes to the model', 'B1', 'W.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'trade it, and make sure the young hunter who stood for it gets a share', 'magic': 'sell it, and settle that a share goes to the sitter'}, 'chance': 0.8}),
    ('keep it, and draw the buyer on the spot instead, just for the practice', 'R1', 'U.7', 0.5, '', {'v': 'stimulation', 'world': {'tribal': 'keep the hide, and draw the trader on the spot instead, just for the practice', 'magic': 'keep it, and sketch her on the spot instead, just for the practice'}, 'chance': 0.8}),
    ('keep it for the stack at home, and invite them to the summer show instead', 'G1', 'B.7', 0.5, '', {'v': 'achievement', 'aims': 'painter or sculptor', 'world': {'tribal': 'keep it, and tell the trader to look for your hides at the summer gathering', 'magic': "keep it, and invite her to the hall's summer showing instead"}, 'chance': 0.7}),
 ]},
{'name': 'the wall is painted over by the council',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'friend, boss',
 'requires': 'street artist',
 'worlds': {'earth': 'a council van by the railway bridge on Monday: by noon the mural you painted there is under '
                     'flat grey paint',
            'tribal': "the elders have had the shelter wall you painted scraped bare for the new season's marks",
            'magic': 'the wardens of the quarter have had your wall by the fish market limewashed over'},
 'timing': {'times': 'per street artist a year: about 1 in 3 see a wall of theirs painted over, cleaned off or '
                     'knocked down; councils clean thousands of walls a year, and work painted without leave rarely '
                     'lasts (estimate); about 5 lives in 10,000 are paid to paint walls (catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'On Monday morning a council van parks by the railway bridge, and by noon the mural {N} spent '
                       'three weekends on, the kingfisher, the old mill and the names of the streets, is under a '
                       'coat of flat grey paint. {friend} sends a photo with no words.'),
                      ('W',
                       '{N} never had a permit for that wall, only a nod from the shops beside it. The council kept '
                       'its own rules, and {N} knows it, though it still stings.'),
                      ('U',
                       'There is a process for this: a public art scheme, a form, a panel that meets every quarter. '
                       '{N} looks it up that evening and reads it twice.'),
                      ('B',
                       'The photo of the mural was shared two thousand times; a photo of the grey wall could be '
                       'shared more. {N} sees that the story is worth more than the paint ever was.'),
                      ('R',
                       'Three weekends of work, gone in a morning under the roller of a man who never looked at it. '
                       '{N} wants to go back tonight with every can in the van.'),
                      ('G',
                       'People loved that wall: the old man from the corner shop stood in front of it every morning '
                       'with his paper. Walls come and go, and a street remembers what it loved.')],
            'tribal': [('',
                        "The elders have had the young ones scrape the shelter wall bare, ready for the new season's "
                        'marks, and the herd of running deer {N} painted there last winter is gone. Nobody asked '
                        '{N}.')],
            'magic': [('',
                       'The wardens of the quarter have had {Ns} wall by the fish market limewashed over by order of '
                       "the guild council: the ship, the gulls and the old fishwives' faces, all gone under one flat "
                       'coat.')]},
 'outcomes': (['Before the year is out, the street has a painted wall again.',
               'People stop {N} in the street to talk about the wall, and the next paid work comes from one of '
               'them.'],
              ['The wall stays bare, and {N} walks the long way round to avoid it.',
               'The fuss dies down in a week, and nobody remembers the old wall but {N}.']),
 'options': [
    ("go to the next council meeting, and ask for a legal wall for the town's painters", 'W1', None, 0.45, '', {'identity': True, 'v': 'universalism, conformity', 'world': {'tribal': "speak at the elders' fire, and ask for one wall where any painter may paint", 'magic': "go before the council of the quarter, and ask for a lawful wall for the city's painters"}, 'chance': 0.4}),
    ('paint the lost mural again on canvas, from the photographs, to keep it', 'U1', None, 0.45, '', {'v': 'achievement, security', 'aims': 'painter or sculptor', 'world': {'tribal': 'paint the lost herd again on a hide, from memory, to keep it', 'magic': 'paint the lost wall again on a panel, from the sketches, to keep it'}, 'chance': 0.8}),
    ('post the before and after online, and let the outcry make your name', 'B1', None, 0.45, '', {'v': 'power, achievement', 'grants': 'following online', 'world': {'tribal': 'tell the story at every fire until the bands come asking for your marks', 'magic': 'give the story to the broadsheet criers, and let the outcry make your name'}, 'chance': 0.6}),
    ('go back tonight, and paint it again, bigger, without leave', 'R1', None, 0.45, '', {'v': 'stimulation', 'mark': 'defied an authority', 'closed': 'law: a wall painted without leave; backfire: the council fines the painter, and the police keep the name on file', 'world': {'tribal': "go back by night, and paint the herd again, bigger, without the elders' leave", 'magic': "go back by night, and paint it again, bigger, without the wardens' leave"}, 'chance': 0.7}),
    ('let it go, and look for a wall the street itself wants painted', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'world': {'tribal': 'let it go, and look for a wall the band itself wants painted', 'magic': 'let it go, and look for a wall the quarter itself wants painted'}, 'chance': 0.85}),
    ("collect the neighbours' names on a letter asking the council to bring it back", 'W1', 'G.7', 0.5, '', {'v': 'universalism, conformity', 'grants': 'a mural the town loves', 'world': {'tribal': 'gather the hearths that loved the herd, and ask the elders together to let it be painted back', 'magic': "collect the neighbours' marks on a petition asking the council of the quarter to bring it back"}, 'chance': 0.4}),
    ('write a proper proposal for the scheme, with drawings, costs and upkeep', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'work out for the elders where, with what and how the wall will be kept, and ask their leave', 'magic': 'write a proper proposal for the guild council, with drawings, costs and upkeep'}, 'chance': 0.4}),
    ("use the fuss to meet the council's arts officer, and learn how walls are commissioned", 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, power', 'mark': 'learned a skill', 'world': {'tribal': 'use the talk at the fires to sit with the elders, and learn how the walls are given out', 'magic': 'use the fuss to win an hour with the clerk of works, and learn how walls are commissioned'}, 'chance': 0.7}),
    ('stand by the grey wall with a placard, and make sure the papers come', 'R1', 'B.7', 0.5, '', {'identity': True, 'v': 'stimulation, power', 'mark': 'made an enemy', 'world': {'tribal': 'stand by the bare wall, and shout the story to every band that passes', 'magic': 'stand by the limewashed wall with a placard, and make sure the criers come'}, 'chance': 0.55}),
    ('get the street out one Sunday to paint a new wall together, without asking anyone', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'grants': 'a mural the town loves', 'mark': 'defied an authority', 'closed': 'law: a wall painted without leave; backfire: the council fines the residents who held the brushes', 'world': {'tribal': 'get the whole band out one morning to paint a new wall together, without the elders', 'magic': 'get the street out one feast day to paint a new wall together, without asking the wardens'}, 'chance': 0.4}),
 ]},
{'name': 'a shopkeeper wants the shutters painted',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'boss',
 'requires': 'street artist',
 'worlds': {'earth': 'the bakery on the high street wants its three roller shutters painted before the summer fair, '
                     'and asks what you would charge',
            'tribal': "the old tanner's family want the hides of their shelter painted before the gathering, and "
                      'offer a haunch of meat',
            'magic': 'the spice merchant on the square wants his sign and shutters painted before the midsummer '
                     'fair'},
 'timing': {'times': 'per street artist a year: about 1 in 2 are asked by a shop, a cafe or a garage to paint its '
                     'shutters or its front; painted shutters are among the commonest paid work for wall painters '
                     '(estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{boss}, who runs the bakery on the high street, has seen the walls {N} paints. The shop has '
                       'three roller shutters, and {boss} wants them painted before the summer fair, something '
                       'people will stop for when the shop is shut, and asks over the counter what {N} would '
                       'charge.'),
                      ('W',
                       'A real job, for a real shop, with a date on it. {N} wants to quote fairly, put it in writing '
                       'and paint exactly what is agreed.'),
                      ('U',
                       'Shutters are a strange surface: ridged steel that rolls up into a box. The design has to '
                       'work rolled half up, in the rain and under a streetlight, and {N} is already sketching how.'),
                      ('B',
                       'A painted shutter on the high street is an advert every evening and all day on Sundays. If '
                       'it is good, every shop on the street will want one, and the price {N} names now will be the '
                       'price for all of them.'),
                      ('R',
                       'Three shutters, a whole street to look at them, and a client who says to go wild. {N} can '
                       'already see it.'),
                      ('G',
                       'The bakery has been on the high street for three generations, and {N} bought bread there as '
                       'a child. Whatever goes on the shutters should belong to the street.')],
            'tribal': [('',
                        'The family of the old tanner, at the far end of the camp, want the hides of their shelter '
                        'painted before the gathering, so every visiting band can see whose hearth it is, and they '
                        'offer a haunch of meat for the work.')],
            'magic': [('',
                       'The spice merchant on the square wants his sign and his shutters painted before the '
                       'midsummer fair, something to stop the crowds, and asks {N} across the counter what it would '
                       'cost.')]},
 'outcomes': (['The work is finished in time, and people stop in the street to look at it.',
               'Within the month two more people ask {N} to paint for them, and pay without haggling.'],
              ['The client does not like it, and pays half with a sour face.',
               'Rain and a slow week ruin the timing, and the day comes and goes before it is done.']),
 'options': [
    ('write a fair quote and a simple contract, and paint exactly what is agreed', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'kept your word', 'world': {'tribal': 'agree before the elders what you will paint and what meat is fair, and keep to it', 'magic': 'set down a fair price and a contract before a notary, and paint exactly what is agreed'}, 'chance': 0.85}),
    ('design it to work open, half open and shut, and test it on paper first', 'U1', None, 0.45, '', {'v': 'achievement, conformity', 'world': {'tribal': 'design it to read from the fire, the path and across the river, and try it on bark first'}, 'chance': 0.75}),
    ('quote high, sign it big, and leave a card in every shop on the street', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'aims': 'renowned artist', 'world': {'tribal': 'ask for the hide as well as the meat, and set your own sign beside the marks', 'magic': 'quote high, sign it big, and leave a card in every shop on the square'}, 'chance': 0.75}),
    ('say yes on the spot, and paint all three in one night', 'R1', None, 0.45, '', {'binds': True, 'v': 'stimulation, hedonism', 'body': 'light', 'world': {'tribal': 'say yes at once, and paint all the hides in one night by the fire', 'magic': 'say yes on the spot, and paint it all in one night by lamplight'}, 'chance': 0.75}),
    ("paint the bakery's own story: the first baker, the old ovens, the street", 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'grants': 'a mural the town loves', 'world': {'tribal': "paint the tanner's own story: the first hunt, the old hearth, the river", 'magic': "paint the shop's own story: the first spice ship, the old warehouse, the square"}, 'chance': 0.4}),
    ('ask the shops on either side for their blessing first, so the street is happy', 'W1', 'G.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the hearths on either side for their leave first, so the camp is at peace with it', 'magic': 'ask the shops on either side for their leave first, so the square is happy'}, 'chance': 0.8}),
    ('use a paint that lasts ten years outdoors, and leave the baker a care sheet', 'U1', 'W.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'grind the ochre with fat so it lasts through the rains, and show the family how to keep it', 'magic': 'use an oil that lasts ten winters outdoors, and show the merchant how to keep it'}, 'chance': 0.75}),
    ('do it at cost, in return for the back wall to try new methods on', 'B1', 'U.7', 0.5, '', {'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': 'ask less meat, in return for a bare hide to try new marks on'}, 'chance': 0.7}),
    ('paint one giant face across all three shutters, to get the whole town talking', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'grants': 'a name in the art world', 'world': {'tribal': 'paint one giant face across all the hides, to get every band at the gathering talking', 'magic': 'paint one giant face across sign and shutters, to get the whole city talking'}, 'chance': 0.4}),
    ('let the regulars each add a brushstroke, so the street feels it is theirs', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'made a friend', 'world': {'tribal': 'let every hearth add a handprint, so the band feels it is theirs', 'magic': 'let the regulars each add a brushstroke, so the square feels it is theirs'}, 'chance': 0.8}),
 ]},
{'name': 'the brief changes at midnight',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, partner',
 'requires': 'illustrator for hire',
 'worlds': {'earth': 'an email at five to midnight from the art director: the client has changed the brief, and the '
                     'cover is still due at nine',
            'tribal': 'the hunter who asked for a stag on his drum comes back at moonrise wanting a bear, for the '
                      'dance at dawn',
            'magic': 'a runner at midnight: the scholar wants beasts round the map, not flowers, and the binder '
                     'comes at dawn'},
 'timing': {'times': 'per illustrator for hire a year: most meet a late change to a brief several times a year; '
                     'surveys of freelance illustrators put changes after sign-off and unpaid extra rounds among '
                     'their commonest complaints (estimate); about 3 lives in 1,000 illustrate for hire (catalogue '
                     'share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'At five to midnight the email comes from {boss}, the art director: the client has seen the '
                       'book cover {N} finished on Friday and changed the brief. The fox is now to be a hare, the '
                       'autumn wood a winter one, and the deadline is still nine in the morning.'),
                      ('W',
                       '{N} agreed to the brief in writing, and the contract allows two rounds of changes. This '
                       'would be the third, and {N} is not sure whether saying so is fair or petty.'),
                      ('U',
                       'A hare is not a fox with long ears: it sits differently, runs differently, holds its head '
                       'another way. {N} opens the folder of reference and starts to work out how to do it properly '
                       'in nine hours.'),
                      ('B',
                       'A third round of changes is extra work, and the contract prices extra work at the day rate, '
                       'if {N} says so now. This client is also the biggest {N} has ever had.'),
                      ('R',
                       '{N} reads the email twice, swears at the screen and nearly replies in capitals. Then, '
                       'annoyingly, {N} starts to see the hare.'),
                      ('G',
                       '{partner} is asleep upstairs, and the house is quiet. Clients change their minds the way the '
                       'weather does, and the work will come right or it will not.')],
            'tribal': [('',
                        'At moonrise the hunter who asked {N} to mark his great drum with a running stag comes back '
                        'to the fire: a dream told him it must be a bear, and the drum is to sound for the first '
                        'time at the dance at dawn.')],
            'magic': [('',
                       'At midnight a runner knocks with a note: the scholar who ordered the map of the northern '
                       'roads wants beasts round its border, not flowers, and the binder comes for it at dawn.')]},
 'outcomes': (['The work is ready in time, and the one who asked for it says it is better than the first.',
               'The next time there is work to give, it comes to {N} first, and for more.'],
              ['It is not ready in time, and the next work goes to someone else.',
               'It is ready in time but rushed, and {N} cannot look at it without wincing.']),
 'options': [
    ('do the third round without a word, to keep the client happy', 'W1', None, 0.45, '', {'self_control': '-', 'v': 'conformity', 'mark': 'gave in to pressure', 'world': {'tribal': 'mark the bear without a word, to keep the hunter happy', 'magic': 'paint the beasts without a word, to keep the scholar happy'}, 'chance': 0.85}),
    ('trace a hare from a photograph online, and paint over it to save hours', 'U1', None, 0.45, '', {'v': 'achievement, security', 'mark': 'hid a wrong', 'closed': "law: a photograph traced without the photographer's leave; backfire: the photographer sees the cover in a shop and sends a bill", 'world': {'tribal': "copy the bear from another marker's shield, line for line, and say nothing", 'magic': "copy the beasts from another illuminator's bestiary, line for line, and say nothing"}, 'chance': 0.8}),
    ('say yes, and send an invoice for the extra round at the day rate', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'say yes, and ask for a second haunch of meat for the second drawing', 'magic': 'say yes, and send a bill for the extra work at the day rate'}, 'chance': 0.7}),
    ('stay up and redraw the whole thing from scratch, on coffee and fury', 'R1', None, 0.45, '', {'self_control': '+', 'v': 'stimulation', 'world': {'tribal': 'stay up by the fire and mark the whole drum again, on fury and moonlight', 'magic': 'stay up and paint the whole border again, on strong tea and fury'}, 'chance': 0.7}),
    ('reply that it will be done when it is done, and go to bed', 'G1', None, 0.45, '', {'self_control': '-', 'v': 'tradition', 'world': {'tribal': 'tell him the bear will come when it comes, and go to sleep', 'magic': 'send word that it will be done when it is done, and go to bed'}, 'chance': 0.5}),
    ("ask the art director for the client's exact words before touching a line", 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'ask the hunter to tell the dream again, word for word, before marking anything', 'magic': "ask the runner for the scholar's exact words before touching a line"}, 'chance': 0.8}),
    ('redo only the hare, and rework the rest cleverly so it takes three hours', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'grants': 'illustration', 'world': {'tribal': "change only the beast, and turn the stag's antlers into the bear's fur, so it takes half the night", 'magic': "change only the beasts, and turn the flowers' stems into their tails, so it takes three hours"}, 'chance': 0.7}),
    ('drop in a hare you drew for another client, and hope nobody notices', 'B1', 'R.7', 0.5, '', {'self_control': '-', 'v': 'hedonism, power', 'mark': 'hid a wrong', 'closed': 'approval: work already sold to another client used again; backfire: the first client sees it on the shelves and stops sending work', 'world': {'tribal': "mark the drum with the bear you made for another hunter's shield, and hope nobody notices", 'magic': 'copy in beasts already sold to another patron, and hope nobody notices'}, 'chance': 0.85}),
    ('ring the art director now, and talk it through honestly, person to person', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'mark': 'made a friend', 'world': {'tribal': "go to the hunter's fire now, and talk it through, one person to another", 'magic': "go to the scholar's door now, and talk it through, one person to another"}, 'chance': 0.6}),
    ('paint it by hand, the old way, and keep to the deadline all the same', 'G1', 'W.7', 0.5, '', {'identity': True, 'v': 'tradition, conformity', 'aims': 'painter or sculptor', 'world': {'tribal': 'mark it with the old patterns, as the old markers did, and have it ready by dawn', 'magic': 'paint it by hand in the old manner, and have it ready by dawn'}, 'chance': 0.65}),
 ]},
{'name': 'the client who will not pay',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss',
 'requires': 'illustrator for hire',
 'worlds': {'earth': 'ninety days and three reminders: a magazine has printed your drawings in two issues and paid '
                     'for neither',
            'tribal': 'the hunter whose shield you marked has carried it to two hunts, and the meat he promised has '
                      'not come',
            'magic': 'the printer on the bridge has sold your woodcuts all season and paid nothing for them'},
 'timing': {'times': 'per illustrator for hire a year: about 1 in 3 have an invoice paid very late or not at all; '
                     'surveys of freelance illustrators and writers put late payment near the top of their troubles '
                     '(estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The invoice is ninety days old. The magazine has run {Ns} drawings in two issues, the '
                       'editor, {boss}, has stopped answering emails, and the rent is due on Friday.'),
                      ('W',
                       'The terms were in writing: payment in thirty days. There is a proper way to chase a debt, '
                       'letter by letter, and {N} means to follow it to the end.'),
                      ('U',
                       "{N} reads up on the small claims process, the magazine's filed accounts, and what a licence "
                       'to print the same drawings elsewhere would be worth.'),
                      ('B',
                       "The magazine still needs the files for next month's cover from {N}, and {N} knows exactly "
                       'how much it needs them.'),
                      ('R',
                       '{N} is furious. The drawings are good, they are in print, the people who sold them have the '
                       'money, and {N} wants to go round there right now.'),
                      ('G',
                       'Most illustrators {N} knows have a story like this one. The work is out in the world either '
                       'way, and there will be other clients.')],
            'tribal': [('',
                        'The hunter whose shield {N} marked with a running wolf has carried it to two hunts and '
                        'boasted of it at the fire, but the meat he promised has never come to {Ns} hearth.')],
            'magic': [('',
                       'The printer on the bridge has sold {Ns} woodcuts of the city gates all season, and every '
                       'time {N} calls for the money the apprentice says the master is out.')]},
 'outcomes': (['The money comes in the end, and {N} pays what is owed at home with a week to spare.',
               'Something better comes out of the fight, and {N} is glad of it a year later.'],
              ['Nothing is ever paid, and it is a lean month.',
               'The quarrel spreads, and some of the work that used to come {Ns} way stops coming.']),
 'options': [
    ('send a formal letter before action, then take it to the small claims court', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'bring the matter before the elders at the next full moon', 'magic': "put the matter before the guild's court of claims"}, 'chance': 0.65}),
    ('license the same drawings to another publisher, as the contract allows', 'U1', None, 0.45, '', {'binds': True, 'v': 'achievement, security', 'grants': 'royalties', 'world': {'tribal': "mark the same wolf on another hunter's shield, for a share of every kill", 'magic': 'sell the right to print the same woodcuts to another printer, as the agreement allows'}, 'chance': 0.5}),
    ('keep the files for the next cover until the old invoices are paid', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'broke your word', 'closed': 'approval: work held back against an agreed contract; backfire: the magazine tells the trade, and other art directors stop calling', 'world': {'tribal': 'keep the second shield he ordered until the meat comes', 'magic': 'keep the blocks for the next broadsheet until the old debt is paid'}, 'chance': 0.7}),
    ('turn up at their office, and refuse to leave without a cheque', 'R1', None, 0.45, '', {'body': 'light', 'v': 'stimulation, power', 'mark': 'defied an authority', 'closed': 'law: refusing to leave a private office; backfire: security walks the illustrator out, and the magazine bans the name', 'world': {'tribal': 'go to his hearth, and sit there until the meat comes', 'magic': "go to the printer's shop, and refuse to leave without the money"}, 'chance': 0.5}),
    ('write it off, and work only for clients who pay on time from now on', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'let it go, and mark only for those who bring the meat first from now on', 'magic': 'write it off, and work only for those who pay on time from now on'}, 'chance': 0.9}),
    ("join the illustrators' association, and learn its ways of chasing a debt", 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'security, conformity', 'world': {'tribal': 'ask the old markers how they make sure the meat comes, and do as they do', 'magic': "join the illuminators' guild, and learn from its clerk how a debt is chased"}, 'chance': 0.65}),
    ('add the late fees the law allows, and send a final demand with the total', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'claim the extra meat the old custom gives for a late debt, before the elders', 'magic': 'add the late fees the guild allows, and send a final demand with the total'}, 'chance': 0.6}),
    ('post the whole story online, name the magazine, and warn every illustrator you know', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'mark': 'made an enemy', 'world': {'tribal': 'tell the whole story at every fire, and warn every marker in the band', 'magic': 'tell the whole story in every tavern, and warn every illuminator in the city'}, 'chance': 0.75}),
    ('ring the editor, say how much it hurts, and ask as one person to another', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'go to the hunter, tell him how it hurts, and ask as one hearth to another', 'magic': 'go to the printer, tell him how it hurts, and ask as one neighbour to another'}, 'chance': 0.55}),
    ('pitch a picture book of the woods where you grew up, for children', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'grants': 'a publishing contract', 'world': {'tribal': "make a long telling in marks of the woods where you grew up, for the children's fire", 'magic': 'offer a printer a picture book of the woods where you grew up, for children'}, 'chance': 0.15}),
 ]},
{'name': 'the studio rent goes up',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague',
 'requires': 'painter or sculptor',
 'worlds': {'earth': 'a letter from the landlord of the old printworks: the studio rent goes up by half from next '
                     'quarter',
            'tribal': 'the elders want the dry cave where you carve, to store the meat for the winter',
            'magic': "the guild's steward raises the rent of the painting rooms under the roof by half at midsummer"},
 'timing': {'times': 'per painter or sculptor a year: about 1 in 5 face a steep rent rise or the loss of a studio; '
                     'studio providers in most big cities report long waiting lists and rents rising faster than '
                     "artists' incomes (estimate); about 1 life in 1,000 earns a real part of a living from painting "
                     'or sculpture (catalogue share; estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The letter from the landlord of the old printworks is short and polite. From the first of '
                       'next quarter the rent on {Ns} studio, a cold room with a north light and a sink, goes up by '
                       'half. Twelve artists rent rooms in the building, and {colleague} is already standing in the '
                       'corridor holding the same letter.'),
                      ('W',
                       '{N} has paid on the first of every month for six years and kept the room as the lease asks. '
                       'The rise is legal, but it is not fair, and twelve tenants together are not nothing.'),
                      ('U',
                       "{N} works the numbers: last year's sales, the hours at the day job, the rent as a share of "
                       'everything. Then the other numbers: what a shed would cost, what sharing would cost, what '
                       'giving it up would cost.'),
                      ('B',
                       'Everyone knows the printworks is being sold for flats. {N} wonders who is buying, and what a '
                       'building full of artists might be worth to them in a brochure.'),
                      ('R',
                       'The room is where the work happens. {Ns} hands want to be in it every evening, and the '
                       'letter makes {N} want to throw something through a window.'),
                      ('G',
                       'The light through that north window, the paint stains on the floor from three tenants '
                       'before, the sound of the trains going by. {N} has grown into this room.')],
            'tribal': [('',
                        'The elders want the dry cave where {N} has carved through three winters, to store the meat '
                        "for the long cold. There is a damp overhang by the river, and an old cave a half day's walk "
                        'up the valley.')],
            'magic': [('',
                       "The guild's steward pins a notice to the stair: from midsummer the rent of the painting "
                       'rooms under the guildhall roof goes up by half, and the rooms will go to whoever pays it.')]},
 'outcomes': (['{N} keeps working through the change, and the work does not suffer for it.',
               'The new arrangement turns out better than the old one, and {N} wonders why it took a push.'],
              ['The work stops for months while {N} sorts out somewhere to do it.',
               'Money runs short, and a stack of unfinished work goes into storage.']),
 'options': [
    ('gather the tenants, and hold back the rise together until the landlord talks', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'mark': 'defied an authority', 'closed': 'law: rent held back against the lease; backfire: the landlord serves notice on the tenants who signed first', 'world': {'tribal': 'gather the carvers and painters, and refuse the elders together until they talk', 'magic': 'gather the tenants, and refuse the rise together until the steward talks'}, 'chance': 0.4}),
    ('work out exactly what you can afford, and find a smaller room that fits', 'U1', None, 0.45, '', {'self_control': '+', 'v': 'security, achievement', 'world': {'tribal': 'weigh up every shelter in reach, and move to the one that keeps the work dry'}, 'chance': 0.7}),
    ('offer the landlord a painting a year in place of the rise', 'B1', None, 0.45, '', {'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'offer the elders a carving for each gathering, if the cave stays yours', 'magic': 'offer the steward a painting for the guildhall each year in place of the rise'}, 'chance': 0.5}),
    ('pack the van tonight, and paint out of doors all summer, wherever you like', 'R1', None, 0.45, '', {'door': True, 'v': 'stimulation, hedonism', 'world': {'tribal': 'walk out tonight, and carve under the open sky all summer, wherever you like', 'magic': 'pack a cart tonight, and paint out of doors all summer, wherever you like'}, 'chance': 0.85}),
    ('move everything home, and work at the kitchen table for now', 'G1', None, 0.45, '', {'self_control': '+', 'v': 'tradition', 'world': {'tribal': 'carry your tools to your own hearth, and carve there for now'}, 'chance': 0.85}),
    ('sign the new lease, and take extra shifts at the day job to pay for it', 'W1', 'B.7', 0.5, '', {'binds': True, 'v': 'security', 'world': {'tribal': 'give up the cave, and hunt twice as often to trade for a better shelter', 'magic': 'sign the new lease, and take extra work at the inn to pay for it'}, 'chance': 0.75}),
    ('build a shed in the garden, insulate it, and make it a studio', 'U1', 'R.7', 0.5, '', {'v': 'achievement, security', 'grants': "studio of one's own", 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'world': {'tribal': 'dig a dry hollow into the bank, roof it with hides, and make it your own', 'magic': 'build a workshop in the yard, and make it a painting room of your own'}, 'chance': 0.6}),
    ('find the buyer of the building, and pitch a floor kept for its artists', 'B1', 'G.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'go to the chief, and win a place in the new cave for all the carvers', 'magic': "find the guild's new master, and win a floor kept for its painters"}, 'chance': 0.35}),
    ('give up the studio on the spot, and take the steady job you were offered', 'R1', 'W.7', 0.5, '', {'self_control': '-', 'v': 'security, stimulation', 'drops': 'painter or sculptor', 'world': {'tribal': 'give up the carving on the spot, and go back to the hunt for good', 'magic': "give up the rooms on the spot, and take the clerk's post you were offered"}, 'chance': 0.9}),
    ('share the room with two friends and learn from them, though the lease says one', 'G1', 'U.7', 0.5, '', {'binds': True, 'v': 'benevolence, achievement', 'grants': 'a circle of artists', 'mark': 'made a friend', 'closed': 'approval: a room shared against the lease; backfire: the landlord finds out and ends the lease early', 'world': {'tribal': 'share a hearth with two other carvers and learn from them, though the elders gave it to you alone', 'magic': 'share the room with two other painters and learn from them, though the guild lets it to one'}, 'chance': 0.75}),
 ]},
{'name': 'a month when nothing works',
 'stages': 'young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, inner',
 'horizon': 'months',
 'roles': 'mentor',
 'requires': 'painter or sculptor',
 'worlds': {'earth': 'four weeks in the studio and every canvas scraped back, with the show at the gallery in two '
                     'months',
            'tribal': 'a whole moon of carving, and every antler cracks or comes out dead, with the gathering two '
                      'moons off',
            'magic': "a month at the easel under the guild roof, and every panel wiped back, with the merchant's "
                     'order due at the fair'},
 'timing': {'times': 'per painter or sculptor a year: about 1 in 2 meet a month or more when the work will not come; '
                     "most artists' working lives run in such fits and starts (estimate)",
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Four weeks in the studio and nothing has worked. Every canvas has been scraped back or '
                       'turned to the wall, the clay heads have slumped, and the show at the gallery in town opens '
                       'in two months. {mentor} rings to ask how it is going, and {N} lets it ring.'),
                      ('W',
                       '{N} keeps the hours anyway, nine to five, because keeping them is the only thing that has '
                       'ever carried {N} through a bad patch.'),
                      ('U',
                       'Something has gone wrong in the method, and {N} goes back over it: the ground, the palette, '
                       'the size, the light. A problem has a cause, and a cause can be found.'),
                      ('B',
                       'The gallery has a list of collectors waiting for this show. {N} could give them more of what '
                       'sold last time, and few of them would know the difference.'),
                      ('R',
                       '{N} has stopped sleeping well, and the studio smells of turps and failure. The urge is to '
                       'throw the whole lot out and start again with a bucket and a broom.'),
                      ('G',
                       'Everyone {N} admires talked about the fallow months, when nothing grows above ground and the '
                       'roots go deeper. {N} would like to believe it.')],
            'tribal': [('',
                        'For a whole moon {Ns} carving has gone wrong: the antler cracks, the stone splits, the '
                        'horses come out stiff and dead. The gathering, where the traders come, is two moons away.')],
            'magic': [('',
                       'For a month {Ns} panels under the guild roof have come to nothing, each wiped back to the '
                       'ground by evening, and the merchant who ordered three for his hall expects them at the '
                       'autumn fair.')]},
 'outcomes': (['The work comes back, slowly at first, and then all at once.',
               'Something new comes out of the bad month, and it is the best thing {N} has made in years.'],
              ['Nothing comes right in time, and the work that goes out is not {Ns} best.',
               'The bad month becomes a bad season, and {N} starts to wonder about giving up.']),
 'options': [
    ('keep the hours anyway: at the easel nine to five, every day, until it turns', 'W1', None, 0.45, '', {'habit': True, 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'keep at the carving from first light to dusk, every day, until it turns', 'magic': "keep the guild's hours at the easel, every day, until it turns"}, 'chance': 0.7}),
    ("copy an old master's composition closely, and say nothing about where it came from", 'U1', None, 0.45, '', {'self_control': '-', 'v': 'achievement, security', 'mark': 'hid a wrong', 'closed': 'approval: a composition lifted from an old painting and shown as new; backfire: a critic names the source in the review', 'world': {'tribal': 'carve the horse exactly as it stands on the old cave wall, and say it came to you', 'magic': "copy an old master's design closely, and say nothing of where it came from"}, 'chance': 0.7}),
    ('paint more of what sold last time, and keep the collectors happy', 'B1', None, 0.45, '', {'habit': True, 'v': 'achievement, power', 'world': {'tribal': 'carve more of the horses that traded well last summer, and keep the traders happy', 'magic': 'paint more of what sold last season, and keep the merchant happy'}, 'chance': 0.8}),
    ('throw out every failed canvas, and start again in an empty room', 'R1', None, 0.45, '', {'v': 'stimulation', 'world': {'tribal': 'throw every failed piece in the river, and start again with nothing', 'magic': 'scrape every failed panel bare, and start again in an empty room'}, 'chance': 0.7}),
    ('stop for a month, walk every day, and wait for the work to come back', 'G1', None, 0.45, '', {'habit': True, 'v': 'universalism, tradition', 'world': {'tribal': 'stop for a moon, walk the valley every day, and wait for the carving to come back', 'magic': 'stop for a month, walk the hills every day, and wait for the work to come back'}, 'chance': 0.7}),
    ('ring the gallery now, own up, and ask to move the show back', 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'mark': 'owned up', 'world': {'tribal': 'tell the traders now that the carvings will not be ready, and ask them to come at the next gathering', 'magic': 'go to the merchant now, own up, and ask for the panels by the spring'}, 'chance': 0.5}),
    ('try a material you have never touched, and push it as far as it goes', 'U1', 'R.7', 0.5, '', {'door': True, 'v': 'stimulation', 'aims': 'renowned artist', 'world': {'tribal': 'try a stone you have never carved, and push it as far as it goes', 'magic': 'try a pigment you have never touched, and push it as far as it goes'}, 'chance': 0.6}),
    ('gather ten years of work, catalogue it, and offer the gallery all of it', 'B1', 'G.7', 0.5, '', {'v': 'achievement', 'grants': 'a body of work', 'world': {'tribal': 'lay out every carving of ten winters, and offer the traders all of it', 'magic': 'gather ten years of panels, list them, and offer the guild a showing of all of it'}, 'chance': 0.6}),
    ('open the studio to the public for a weekend, failures and all', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'grants': 'a name in the art world', 'world': {'tribal': 'show the cracked carvings to the whole band at the fire, failures and all', 'magic': 'open the rooms to the city for a feast day, failures and all'}, 'chance': 0.4}),
    ('go back to the place where you first painted, and paint it again, slowly', 'G1', 'U.7', 0.5, '', {'v': 'tradition', 'mark': 'came home', 'world': {'tribal': 'go back to the cave where you first carved, and carve there again, slowly', 'magic': 'go back to the village where you first painted, and paint it again, slowly'}, 'chance': 0.75}),
 ]},
{'name': 'art school applications',
 'stages': 'juvenile young_adult adult',
 'age': (16, 35),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'young_adult',
 'per_year': (0.0, 0.15, 0.08, 0.02, 0.0, 0.0),
 'drivers': 'prosper+.2 money+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'school, work',
 'horizon': 'months',
 'roles': 'mentor, parent, grandparent, friend, rival',
 'requires': 'drawing and painting | life-drawing regular',
 'worlds': {'earth': 'the art school applications: a form, a statement and a portfolio for the interview',
            'tribal': 'the painter of the great cave will take an apprentice for three winters, and the young ones '
                      'bring their marks',
            'magic': 'the academy of arts takes new students once a year, and each one brings a folio to the '
                     'masters'},
 'timing': {'times': 'per person aged 16 to 35 who draws (the base skill or the life class) a year: about 1 in 7 at '
                     'seventeen or eighteen, and fewer later, send a portfolio to an art school; creative arts and '
                     'design is about 1 university student in 12 in the UK, and about 15 lives in 1,000 study fine '
                     'art, illustration or design (UK higher-education statistics; catalogue share; estimate)',
            'likelier': 'an art teacher who pushes the portfolio, a foundation year done, good years with grants and '
                        'loans easy to get, parents who back it',
            'rarer': 'no portfolio, fees the family cannot meet, parents who want a safer subject, a life already '
                     'full of work and children',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The applications close after the holidays: a form, a statement, and a portfolio of twenty '
                       'pieces for an interview in the spring. {Ns} drawings cover the bedroom floor, and {mentor} '
                       'has said more than once that {N} should apply.'),
                      ('W',
                       '{N} has read the guidance three times, and every piece is mounted, labelled and in the order '
                       'the course asks for.'),
                      ('U',
                       '{N} keeps thinking about what the interviewers really look for: not finished pictures, but '
                       'the thinking, the sketchbooks, the mistakes worked through.'),
                      ('B',
                       'Three art schools matter and the rest are back-ups. {N} wants the one whose graduates end up '
                       'on the walls of the big galleries.'),
                      ('R',
                       '{N} cannot imagine spending a life on anything else. The portfolio is a mess of everything '
                       'at once, and every page of it is alive.'),
                      ('G',
                       'The drawings are of home: the allotments, the old men on the bench by the bus stop, the '
                       'hands of {grandparent}. {N} wonders whether art school is a way out, or a way further in.')],
            'tribal': [('',
                        'The painter of the great cave will take one apprentice this winter, for three winters. The '
                        'young ones of the band lay their marks out by the fire, scratched on bark and bone and '
                        'smoothed hide.')],
            'magic': [('',
                       'The academy of arts opens its gates to new students once a year. Each one brings a folio for '
                       "the masters, and the fees are paid in silver at the porter's lodge.")]},
 'outcomes': (["A letter comes in the spring with the college's crest on it, and in the autumn {N} carries a "
               'portfolio case up the stairs of the art school.',
               'Whatever {N} chose, the drawing goes on, and a year later {N} is glad of the road taken.'],
              ['The letter is short and kind: many strong applicants this year, and no place.',
               'The interview goes badly, a question about a favourite painter leaves {N} blank, and the train home '
               'is very long.']),
 'options': [
    ('send the portfolio exactly as the guidance asks, every piece mounted and labelled', 'W1', None, 0.45, '', {'title': 'art school student', 'v': 'conformity', 'world': {'tribal': 'lay out the marks exactly as the painter asked, each in its place by the fire', 'magic': "send the folio exactly as the academy's rules ask, every leaf mounted and labelled"}, 'chance': 0.45}),
    ('take a paid portfolio course on Saturdays, and apply with what it teaches', 'U1', None, 0.45, '', {'title': 'art school student', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'habit': True, 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': "give a good fur to sit with the painter's helper for a moon, and bring what you learn", 'magic': 'pay a master for a season of lessons, and apply with what they teach'}, 'chance': 0.45}),
    ('apply only to the school whose graduates end up in the big galleries', 'B1', None, 0.45, '', {'title': 'art school student', 'aims': 'painter or sculptor', 'v': 'achievement, power', 'world': {'tribal': "ask only the painter whose apprentices are wanted at every band's cave", 'magic': 'apply only to the academy whose students end up painting for the court'}, 'chance': 0.45}),
    ('throw out the safe pieces, and fill the portfolio with the wild new work', 'R1', None, 0.45, '', {'title': 'art school student', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'throw away the careful marks, and bring the wild ones made in the night', 'magic': 'throw out the careful studies, and fill the folio with the wild new work'}, 'chance': 0.45}),
    ('apply to the art school in your own town, with home in every drawing', 'G1', None, 0.45, '', {'title': 'art school student', 'mark': 'stayed home', 'v': 'tradition, benevolence', 'world': {'tribal': "ask the painter of your own band's cave, with your own hills in every mark", 'magic': 'apply to the academy in your own city, with its streets in every leaf'}, 'chance': 0.45}),
    ("work a year in the sign-writer's shop in town, and save the fees", 'B.5 G.5', None, 0.5, '', {'grants': 'savings', 'self_control': '+', 'v': 'power, tradition', 'world': {'tribal': 'scrape hides for the elders through a winter, and save the gifts the painter asks', 'magic': "work a year in the sign-painter's shop, and save the academy's fees in silver"}, 'chance': 0.75}),
    ('skip art school, and sell prints at the weekend market instead', 'B.5 R.5', None, 0.5, '', {'grants': 'selling', 'mark': 'turned down a chance', 'v': 'self-direction, stimulation', 'world': {'tribal': "skip the painter's cave, and trade your marked hides at the gathering instead", 'magic': 'skip the academy, and sell prints at the market cross instead'}, 'chance': 0.75}),
    ('take the free foundation year at the local college before choosing', 'U.5 G.5', None, 0.5, '', {'grants': 'sculpting', 'door': True, 'v': 'achievement, security', 'world': {'tribal': 'spend a winter learning to carve from the old carver of your band before choosing', 'magic': "take the free year at the town's drawing school before choosing"}, 'chance': 0.75}),
    ('tell your parents straight that this is the life you want, and ask their blessing', 'W.5 R.5', None, 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'tell your mother and father at the fire that this is the life you want, and ask their blessing'}, 'chance': 0.75}),
    ('ask the art teacher at school to go through the portfolio piece by piece', 'W.5 U.5', None, 0.5, '', {'grants': 'mentor', 'door': True, 'v': 'achievement, conformity', 'world': {'tribal': 'ask the old woman who paints the shields to judge every mark, one by one', 'magic': 'ask your old drawing master to go through the folio leaf by leaf'}, 'chance': 0.75}),
 ]},
{'name': 'the degree show',
 'stages': 'young_adult adult',
 'age': (19, 45),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'young_adult',
 'per_year': (0.0, 0.0, 0.6, 0.6, 0.0, 0.0),
 'drivers': 'prosper+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, school',
 'horizon': 'months',
 'roles': 'mentor, friend, parent, colleague, rival',
 'requires': 'art school student',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'the degree show: three years of work on the walls for four days, and the city comes to look',
            'tribal': "the apprentice's three winters end, and the bands come to see the first wall painted alone",
            'magic': "the academy's graduation hall, where every student hangs a year's work for the city and the "
                     'guilds'},
 'timing': {'times': 'per art school student in the last year of the course: once, at the degree show; most '
                     'graduates of fine art and illustration work outside the arts within a few years, and about 1 '
                     'in 10 is earning from art five years on; about 15 lives in 1,000 hold an art school place '
                     '(catalogue share; graduate outcome surveys; estimate)',
            'likelier': 'a final year that went well, a show in a city with galleries and agencies, good years for '
                        'galleries and publishers',
            'rarer': 'a course left early, a show far from where art is bought, a lean year',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'The degree show opens on Thursday night: {Ns} space at the end of the corridor, three years '
                       'of work on the walls, a price list on the table and a bowl of crisps going soft. Dealers, '
                       'art directors, teachers, parents and a reporter from the local paper drift through the '
                       'noise.'),
                      ('W',
                       '{N} has hung the space to the centimetre and printed a list of every piece with its medium '
                       'and its size. The show is a promise kept to three years of tutors.'),
                      ('U',
                       "{N} watches who stops and for how long, and which piece holds them. By nine o'clock {N} has "
                       'a theory about it.'),
                      ('B',
                       '{N} can tell which visitors are dealers by their shoes, and has a card ready for each of '
                       'them.'),
                      ('R',
                       'Three years of work, and tonight the walls are finally full. {N} wants to shout, and settles '
                       'for dancing in the corridor after the speeches.'),
                      ('G',
                       '{Ns} family have come on the coach and stand before every piece as if in church, and the '
                       'year group are already talking about what happens next, and whether it can happen '
                       'together.')],
            'tribal': [('',
                        "The apprentice's three winters are ending. At the gathering the bands crowd into the side "
                        'cave to see the first wall {N} has painted alone, and the traders in carvings look as '
                        'carefully as the elders.')],
            'magic': [('',
                       "The academy's great hall is hung with every student's year of work, and the city comes to "
                       'look: guild masters, picture dealers from the square, drawing masters from the town schools, '
                       'and proud parents in their best.')]},
 'outcomes': (['A week after the show {N} has an answer, an address and a start date, and the summer has a shape.',
               "By the last day the visitors' book is full, and the road {N} chose opens the way it should."],
              ['The show closes on Sunday, the work comes down into a borrowed van, and the phone stays quiet.',
               'The one visitor who mattered never comes back, and {N} goes home to a bedroom stacked with '
               'canvases.']),
 'options': [
    ("sign up for a year's teacher training, to teach art in a school", 'W1', None, 0.45, '', {'title': 'art teacher', 'binds': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'ask to sit beside the one who teaches the children the marks, and learn to teach them', 'magic': 'ask a drawing master to take you on as an under-master for a year'}, 'chance': 0.55}),
    ('send the art director who lingered at the show a drawing made to her brief', 'U1', None, 0.45, '', {'title': 'illustrator for hire', 'aims': 'illustrator for hire', 'v': 'achievement, conformity', 'world': {'tribal': "mark a bowl in the trader's own pattern, and send it to him the next morning", 'magic': 'send the printer who lingered at the wall a page illuminated to his own brief'}, 'chance': 0.25}),
    ('work the private view until the dealers know the name and the prices', 'B1', None, 0.45, '', {'grants': 'a dealer who sells your work', 'v': 'power, achievement', 'world': {'tribal': 'walk with the traders all evening, until they know the name and what each piece costs', 'magic': 'work the hall all evening, until the picture dealers know the name and the prices'}, 'chance': 0.2}),
    ('offer the college a mural for the wall by its gates, painted in a weekend', 'R1', None, 0.45, '', {'title': 'street artist', 'body': 'light', 'v': 'stimulation', 'world': {'tribal': 'offer to paint the wall at the cave mouth, and finish it before the gathering ends', 'magic': 'offer the academy a mural for the wall by its gate, and paint it in a weekend'}, 'chance': 0.3}),
    ('keep the year together in a shared studio at the old mill, rent split six ways', 'G1', None, 0.45, '', {'grants': 'a circle of artists', 'v': 'benevolence, tradition', 'world': {'tribal': 'keep the apprentices together, painting side by side in the old cave by the river', 'magic': "keep the year together in a shared studio above the dyers' yard, rent split six ways"}, 'chance': 0.56}),
    ('go home for the summer, and paint whatever comes, with no plan at all', 'R.5 G.5', None, 0.5, '', {'mark': 'came home', 'v': 'hedonism, tradition', 'world': {'tribal': 'go back to your own band for the summer, and paint whatever comes', 'magic': 'go home to your village for the summer, and paint whatever comes'}, 'chance': 0.82}),
    ("price every piece sensibly, and sell what sells to the show's visitors", 'U.5 B.5', None, 0.5, '', {'grants': 'selling', 'v': 'achievement, power', 'world': {'tribal': 'set a fair price on every piece, and trade what the visitors will take', 'magic': "price every piece sensibly, and sell what sells to the hall's visitors"}, 'chance': 0.86}),
    ('go and assist a working sculptor in the next city, mixing plaster and learning', 'U.5 R.5', None, 0.5, '', {'grants': 'sculpting', 'door': True, 'binds': True, 'v': 'achievement, stimulation', 'world': {'tribal': 'go and help the old carver of the next band, grinding stone and learning', 'magic': 'go and assist a guild sculptor in the next city, mixing plaster and learning'}, 'chance': 0.78}),
    ('take a steady job in a framing shop, and keep a foot in the trade', 'W.5 B.5', None, 0.5, '', {'grants': 'contact in the trade', 'v': 'security, achievement', 'world': {'tribal': 'take a steady place stretching hides for the traders, and keep near the trade', 'magic': "take a steady place in a frame-maker's shop, and keep a foot in the trade"}, 'chance': 0.86}),
    ("go home, and apply for the arts centre's one residency, teaching its Saturday classes", 'W.5 G.5', None, 0.5, '', {'grants': "studio of one's own", 'v': 'benevolence, tradition', 'world': {'tribal': 'go back to your own band, and ask the elders for the bare wall of the old shelter', 'magic': 'go home, and ask the guildhall for the one painting room it gives a young painter'}, 'chance': 0.25}),
 ]},
{'name': 'a wall that needs a mural',
 'stages': 'juvenile young_adult adult mature',
 'age': (16, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.02, 0.1, 0.08, 0.04, 0.0),
 'drivers': 'community+.3 prosper+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'friend, elder, rival, boss, colleague',
 'requires': 'life-drawing regular | art school student | art teacher',
 'worlds': {'earth': 'the council wants a mural for the long wall of the underpass, and asks local painters for '
                     'designs',
            'tribal': "the band's new winter shelter has a long bare wall, and the elders want it painted before the "
                      'snows',
            'magic': "the quarter's council wants the blank wall of the old granary painted, and asks the city's "
                     'painters for designs'},
 'timing': {'times': 'per life-drawing regular, art student or art teacher a year: about 1 in 10 young adults and '
                     'fewer later answer a call for a mural on a public wall; councils, schools and shops pay for '
                     'murals in most towns, and about 1 life in 2,000 is paid to paint walls for a year or more '
                     '(catalogue share; estimate)',
            'likelier': 'a council with money for its streets, a town that likes its walls painted, a portfolio of '
                        "walls already done, friends on the residents' committee",
            'rarer': 'a council cutting back, a town that wants its walls plain, no wall work to show',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The council has pinned a notice in the library: the long grey wall of the underpass by the '
                       'station is to have a mural, designs by the end of the month, a small fee, the paint and the '
                       'scaffold provided. {friend} has photographed the notice and sent it to {N} twice.'),
                      ('W',
                       'A wall the whole town walks past every day deserves a design agreed with the people who live '
                       'beside it, and paint that will last twenty years.'),
                      ('U',
                       '{N} has paced the wall out and noticed the drainpipes, the cracks and the way the light '
                       "falls at four o'clock. Every one of them could be part of the picture."),
                      ('B',
                       'The underpass is on the way to the station: thousands of people a day. {N} thinks about '
                       'whose name would be on that wall, and what it would bring.'),
                      ('R',
                       '{N} can already see it: colour from end to end, something huge and alive where the grey has '
                       'been for forty years.'),
                      ('G',
                       '{N} grew up on this estate, and so did {Ns} parents. The wall should look like the people '
                       'who walk past it.')],
            'tribal': [('',
                        'The band has dug its new winter shelter into the hillside, and its long back wall is bare '
                        'rock. The elders want it painted before the first snows, and they ask who will do it.')],
            'magic': [('',
                       "The quarter's council wants the blank wall of the old granary on the square painted, and has "
                       'nailed a notice to the well: designs to the clerk by the new moon, a small purse, and the '
                       'paint paid.')]},
 'outcomes': (['The council chooses {Ns} design in the spring, and by early summer the underpass is scaffolded and '
               '{N} is up a ladder in old clothes.',
               'Whatever {N} chose, the wall gets painted, and people stop on the way to the station to look at it.'],
              ['The council chooses a design from a firm in the city, and thanks every local painter in a printed '
               'letter.',
               'The money is cut in the autumn, and the wall stays grey for another year.']),
 'options': [
    ('plan the design with the neighbours and the council, squared up to last', 'W1', None, 0.45, '', {'title': 'street artist', 'v': 'conformity, benevolence', 'world': {'tribal': 'plan the wall with the elders and the families of the shelter, every mark agreed', 'magic': "plan the design with the neighbours and the quarter's council, squared up to last"}, 'chance': 0.35}),
    ("design it around the wall's cracks and drainpipes, so the picture seems to belong there", 'U1', None, 0.45, '', {'title': 'street artist', 'v': 'achievement, conformity', 'world': {'tribal': "draw the design around the rock's own cracks and bulges, so the animals seem to move", 'magic': "design it around the granary's cracks and beams, so the picture seems to belong there"}, 'chance': 0.35}),
    ('get the local paper to print your design before the council votes', 'B1', None, 0.45, '', {'title': 'street artist', 'v': 'power, achievement', 'world': {'tribal': 'show your design to every family before the elders choose, until the band talks of nothing else', 'magic': 'get the broadsheet to print your design before the council votes'}, 'chance': 0.35}),
    ('send in a design so bold the committee cannot look away from it', 'R1', None, 0.45, '', {'title': 'street artist', 'aims': 'painter or sculptor', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'show the elders a design so bold they cannot look away from it', 'magic': 'send in a design so bold the council cannot look away from it'}, 'chance': 0.35}),
    ("paint it with a class from the school, the parents' forms signed", 'G1', None, 0.45, '', {'grants': 'a mural the town loves', 'requires': 'art teacher', 'without': 'approval', 'lacking': 0.3, 'v': 'universalism, benevolence', 'world': {'tribal': 'paint it with the children of the band, their mothers sitting by', 'magic': "paint it with a class from the quarter's school, their master alongside"}, 'chance': 0.35}),
    ('paint it for nothing, for the name it will bring in town', 'B.5 G.5', None, 0.5, '', {'grants': 'name on the local scene', 'v': 'achievement, universalism', 'world': {'tribal': 'paint it for no gift, for the name it will bring among the families', 'magic': 'paint it for no purse, for the name it will bring in the quarter'}, 'chance': 0.74}),
    ('turn it down, and paint the empty garage walls by the canal on your own terms', 'B.5 R.5', None, 0.5, '', {'grants': 'following online', 'mark': 'turned down a chance', 'v': 'self-direction, stimulation', 'world': {'tribal': 'turn it down, and paint the rocks by the river where nobody tells you what to paint', 'magic': 'turn it down, and paint the empty warehouse walls by the canal on your own terms'}, 'chance': 0.74}),
    ('help the painter who wins, and learn how a wall that size is done', 'U.5 R.5', None, 0.5, '', {'grants': 'a circle of artists', 'mark': 'made a friend', 'binds': True, 'v': 'achievement, stimulation', 'world': {'tribal': 'help the painter the elders choose, and learn how a wall that size is done'}, 'chance': 0.74}),
    ("get the residents' committee to reject the outsider the council picked", 'W.5 G.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': "approval: shutting out the council's chosen painter; backfire: the council goes ahead anyway, and the painter it chose tells the local paper who blocked her", 'v': 'tradition, conformity', 'world': {'tribal': 'get the families of the shelter to refuse the painter the elders brought from another band', 'magic': "get the quarter's guild to refuse the painter the council brought from across the river"}, 'chance': 0.72}),
    ('offer to restore the faded old mural on the library wall instead', 'W.5 U.5', None, 0.5, '', {'grants': 'restoring old things', 'v': 'conformity, security', 'world': {'tribal': 'offer to renew the faded marks in the old shelter instead', 'magic': 'offer to restore the faded old mural on the chapter house wall instead'}, 'chance': 0.76}),
 ]},
{'name': 'the first commission',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.1, 0.08, 0.04, 0.02),
 'drivers': 'era+.2 prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, friend, colleague, mentor',
 'requires': 'art school student | life-drawing regular | street artist',
 'worlds': {'earth': 'a small press wants a cover and twelve drawings for a book, paid, in three weeks',
            'tribal': 'a trader from the next band wants his drums and bowls marked with a pattern of his own',
            'magic': 'a printer on the bridge wants a frontispiece and a dozen cuts for an almanac, paid in silver'},
 'timing': {'times': 'per art student, life-drawing regular or street artist a year: about 1 in 10 young adults and '
                     'fewer later are offered a first paid drawing job (a cover, a label, a set of drawings for a '
                     'book); about 3 lives in 1,000 work as freelance illustrators for a year or more (catalogue '
                     'share; estimate)',
            'likelier': 'drawings shown online or at a show, a friend who works in publishing or design, a boom in '
                        'illustrated books and packaging',
            'rarer': 'no portfolio anyone can see, a lean year for small presses, a life far from where books and '
                     'magazines are made',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'An email from a small press: they have seen {Ns} drawings online and want a cover and twelve '
                       'drawings for a book of country walks, sold to raise money for keeping the paths open. The '
                       'fee is small, the deadline is three weeks, and they need an answer by Friday.'),
                      ('W',
                       '{N} reads the brief twice and writes down every drawing it asks for, with a date beside each '
                       'one.'),
                      ('U',
                       'The brief is vague in all the interesting places. {N} starts sketching three different books '
                       'in the margin of the email.'),
                      ('B',
                       'A cover with {Ns} name on it, in shops. {N} wonders what the press really pays, and what it '
                       'would pay if asked.'),
                      ('R',
                       'Someone wants to pay for drawings! {N} rings {friend} and shouts down the phone before '
                       'reading to the end.'),
                      ('G',
                       'The walks are the ones {N} grew up on: the river path, the beech wood, the old drove road. '
                       '{N} knows every stile.')],
            'tribal': [('',
                        'A trader from the next band has seen the marks on {Ns} shield and wants his own drums and '
                        'bowls marked with a pattern nobody else carries. He has brought good flint to pay.')],
            'magic': [('',
                       'A printer from the bridge has seen {Ns} sketches in the tavern and wants a frontispiece and '
                       "a dozen cuts for next year's almanac, paid in silver, the blocks by the new moon.")]},
 'outcomes': (['The press loves the cover, the book comes back from the printer with {Ns} name on the back flap, and '
               'a second email arrives from a firm that saw it.',
               'Whatever {N} chose, the three weeks go well, and the book of walks is in the shops by the spring.'],
              ['The press goes with an illustrator they used before, and sends a polite email about next time.',
               'The deadline slips, the drawings arrive a week late, and the press uses photographs instead.']),
 'options': [
    ('deliver every drawing to the brief, on the day it was promised', 'W1', None, 0.45, '', {'title': 'illustrator for hire', 'mark': 'kept your word', 'self_control': '+', 'v': 'conformity', 'world': {'tribal': "mark every drum and bowl to the trader's pattern, on the day you promised", 'magic': "deliver every cut to the printer's brief, on the day it was promised"}, 'chance': 0.4}),
    ('send three roughs that answer the brief three different ways', 'U1', None, 0.45, '', {'title': 'illustrator for hire', 'v': 'achievement, conformity', 'world': {'tribal': 'show the trader three patterns that answer his wish three different ways', 'magic': 'send three trial sketches that answer the brief three different ways'}, 'chance': 0.4}),
    ('quote a proper rate, and ask for the name on the cover', 'B1', None, 0.45, '', {'title': 'illustrator for hire', 'v': 'power, achievement', 'world': {'tribal': 'ask a proper price in flint, and for your own sign beside his on every drum', 'magic': 'name a proper price, and ask for the name on the title page'}, 'chance': 0.4}),
    ('stay up three nights, and draw the whole book in one burst', 'R1', None, 0.45, '', {'title': 'illustrator for hire', 'body': 'light', 'v': 'stimulation, hedonism', 'world': {'tribal': 'sit up three nights by the fire, and mark every drum and bowl in one burst', 'magic': 'sit up three nights by the candle, and cut every block in one burst'}, 'chance': 0.4}),
    ('walk every route in the book, and draw each path from life', 'G1', None, 0.45, '', {'title': 'illustrator for hire', 'v': 'tradition, universalism', 'world': {'tribal': "walk to the trader's own camp, and mark his things with the animals of his hills", 'magic': 'walk every road in the almanac, and draw each one from life'}, 'chance': 0.4}),
    ("waive the fee, since the book's money goes to keeping the paths open", 'R.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, stimulation', 'world': {'tribal': "mark the drums for no flint, since they are for the gathering's dances", 'magic': "waive the silver, since the almanac's money goes to mending the roads"}, 'chance': 0.76}),
    ('trace the reference photographs, and send them as drawings', 'U.5 B.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: traced photographs passed off as drawings; backfire: the photographer finds the book in a shop, and the press pays nothing and says why', 'self_control': '-', 'v': 'achievement, power', 'world': {'tribal': "press the trader's old bowl into wet clay, and pass the copy off as your own marking", 'magic': "trace the old engravings in the printer's own cupboard, and send them as new cuts"}, 'chance': 0.74}),
    ('ask for a single drawing first, to learn how a brief is done', 'U.5 G.5', None, 0.5, '', {'grants': 'illustration', 'v': 'achievement, security', 'world': {'tribal': 'ask to mark a single bowl first, to learn what a trader wants', 'magic': "ask for a single cut first, to learn how a printer's brief is done"}, 'chance': 0.76}),
    ('have the contract read line by line before signing anything', 'W.5 B.5', None, 0.5, '', {'grants': 'striking a deal', 'v': 'security, power', 'world': {'tribal': 'have the elders hear the bargain spoken out before you shake on it', 'magic': 'have a notary read the contract line by line before you sign'}, 'chance': 0.76}),
    ('pass the job to a friend from the class who needs the money more', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, stimulation', 'world': {'tribal': 'send the trader to a friend who paints shields and needs the flint more', 'magic': 'pass the job to a friend from the academy who needs the silver more'}, 'chance': 0.76}),
 ]},
{'name': 'the first show',
 'stages': 'young_adult adult mature elder',
 'age': (19, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.06, 0.06, 0.04, 0.02),
 'drivers': 'prosper+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, friend, partner, rival, colleague',
 'requires': 'life-drawing regular | street artist | illustrator for hire | art school student',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "a small gallery offers a first show of one's own: three weeks on its walls, the opening on a "
                     'Friday',
            'tribal': "the traders in carvings will lay out one maker's pieces alone at the gathering, for every "
                      'band to see',
            'magic': 'a picture dealer offers a month in the small room of his hall on the square'},
 'timing': {'times': 'per person two years or more on the rung below (the life class, walls, illustration or art '
                     'school) a year: about 1 in 16 are offered a first show of their own in a gallery, a café or a '
                     'library; most first shows sell little, and about 1 life in 1,000 earns a real part of a living '
                     'from painting or sculpture for some years (catalogue share; estimate)',
            'likelier': 'good years when people buy art, a body of work already made, a friend who runs a gallery, a '
                        'lucky cancellation',
            'rarer': 'a lean year, no work finished, a town with no gallery and no café that hangs pictures',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The small gallery off the high street has had a cancellation: three weeks in the spring, and '
                       'the walls are {Ns} if {N} can fill them. The owner takes forty in every hundred of each '
                       'sale, and wants the list of works in a month.'),
                      ('W',
                       '{N} makes a list: twenty pieces framed alike, a price on each that a teacher could afford, '
                       'and a catalogue with every title spelled right.'),
                      ('U',
                       '{N} lays all the work out on the studio floor and looks for the thread that runs through it. '
                       'A show is an argument, and this one is nearly there.'),
                      ('B',
                       "The gallery's mailing list has three collectors and a critic on it. {N} intends to meet all "
                       'four before the wine runs out.'),
                      ('R',
                       'Two months is no time, and {N} does not care: there is a whole new body of work trying to '
                       'get out, and the walls are waiting for it.'),
                      ('G',
                       'The pieces are of the town: the harbour wall, the allotments in winter, the faces of the '
                       'neighbours who sat for them in their own kitchens.')],
            'tribal': [('',
                        "At the gathering the traders in carvings will set out one maker's pieces alone on a hide by "
                        'the great fire, and every band will walk past them. This year they have asked for {Ns}.')],
            'magic': [('',
                       "A picture dealer on the square offers {N} a month in the small room of his hall, the city's "
                       'collectors invited to the first evening, and a third of every sale for the house.')]},
 'outcomes': (['The first night sells half the walls, the local paper sends someone, and by the summer {N} is '
               'painting full time, in a cold studio, on the strength of it.',
               'Whatever {N} chose, the show goes up and comes down well, and the people who came remember it.'],
              ['The show is kindly reviewed and almost nothing sells, and {N} carries most of it home again.',
               'The opening night is wet and half empty, and the gallery owner is already talking about next '
               "season's artists."]),
 'options': [
    ('hang the show as planned, with a catalogue and an honest price on each piece', 'W1', None, 0.45, '', {'title': 'painter or sculptor', 'grants': 'a name in the art world', 'v': 'conformity', 'world': {'tribal': 'lay the pieces out as planned, with a fair price in furs set by each one', 'magic': 'hang the show as planned, with a printed list and an honest price on each piece'}, 'chance': 0.25}),
    ('build the show around one idea, each piece answering the last', 'U1', None, 0.45, '', {'title': 'painter or sculptor', 'grants': 'a name in the art world', 'identity': True, 'v': 'achievement, security', 'world': {'tribal': 'lay the pieces out around one animal, each carving answering the last', 'magic': 'build the show around one idea, each canvas answering the last'}, 'chance': 0.25}),
    ("meet every collector and critic on the gallery's list before the wine runs out", 'B1', None, 0.45, '', {'title': 'painter or sculptor', 'grants': 'a dealer who sells your work', 'door': True, 'v': 'power, achievement', 'world': {'tribal': 'sit with every trader from the far bands before the feast is over', 'magic': "meet every collector on the dealer's list before the wine runs out"}, 'chance': 0.25}),
    ('paint the whole show new in two months, the work that has to be made', 'R1', None, 0.45, '', {'title': 'painter or sculptor', 'grants': 'a name in the art world', 'aims': 'renowned artist', 'mark': 'took a wild risk', 'self_control': '+', 'v': 'stimulation', 'world': {'tribal': 'carve every piece new in two moons, the work that has to be made'}, 'chance': 0.25}),
    ("show a year of the town: the harbour, the allotments, the neighbours' faces", 'G1', None, 0.45, '', {'title': 'painter or sculptor', 'grants': 'a name in the art world', 'v': 'tradition, universalism', 'world': {'tribal': 'show a year of the band: the river, the hunt, the faces of the old ones', 'magic': "show a year of the quarter: the quay, the market gardens, the neighbours' faces"}, 'chance': 0.25}),
    ('take the smaller show at the café on the high street, and keep every sale', 'B.5 G.5', None, 0.5, '', {'grants': 'name on the local scene', 'v': 'power, tradition', 'world': {'tribal': "lay the pieces out at your own band's fire instead, and keep every trade", 'magic': 'take the smaller wall in the tavern on your own street, and keep every sale'}, 'chance': 0.77}),
    ('turn the opening into a party for everyone who sat, and drink till closing', 'R.5 G.5', None, 0.5, '', {'grants': 'a circle of artists', 'self_control': '-', 'habit': True, 'v': 'hedonism, benevolence', 'world': {'tribal': 'turn the first night into a feast for everyone who was carved, and drink the strong brew till dawn', 'magic': "turn the first evening into a party for everyone who sat, and drink the dealer's wine till closing"}, 'chance': 0.75}),
    ('ask the gallery for the sales of every first show it has hung, before signing', 'U.5 B.5', None, 0.5, '', {'grants': 'striking a deal', 'v': 'achievement, power', 'world': {'tribal': 'ask the traders what every first maker before you got in trade, before you agree', 'magic': 'ask the dealer for the sales of every first show he has hung, before signing'}, 'chance': 0.75}),
    ('turn the show down until the work is ready, and say so plainly', 'W.5 R.5', None, 0.5, '', {'mark': 'turned down a chance', 'identity': True, 'v': 'conformity, universalism', 'world': {'tribal': 'tell the traders plainly that the carvings are not ready, and wait a year', 'magic': 'turn the dealer down until the work is ready, and say so plainly'}, 'chance': 0.77}),
    ('give a talk on the work in the gallery on the second Saturday', 'W.5 U.5', None, 0.5, '', {'grants': 'public speaking', 'v': 'achievement, conformity', 'world': {'tribal': 'tell the story of every carving at the fire on the second night', 'magic': "give a talk on the work in the dealer's hall on the second market day"}, 'chance': 0.75}),
 ]},
{'name': 'the school needs an art teacher',
 'stages': 'young_adult adult mature',
 'age': (22, 65),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.05, 0.04, 0.02, 0.0),
 'drivers': 'era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, school',
 'horizon': 'months',
 'roles': 'colleague, boss, friend, rival',
 'requires': 'teacher | painter or sculptor | illustrator for hire | street artist | art school degree',
 'worlds': {'earth': "the secondary school's art teacher is leaving, and the post is advertised in the local paper",
            'tribal': 'the one who teaches the children the marks has grown too old, and the elders look for another',
            'magic': 'the town school needs a drawing master, and the governors post the place on the guildhall '
                     'door'},
 'timing': {'times': 'per teacher, art graduate or working artist a year: about 1 in 20 young adults and fewer later '
                     "see an art teacher's post they could apply for; about 1 secondary teacher in 25 teaches art "
                     'and design, and about 3 lives in 1,000 teach art (UK and US teaching workforce counts; '
                     'catalogue share; estimate)',
            'likelier': 'a teacher retiring, a school adding art back to the timetable, a teaching qualification '
                        'held, a town with several schools',
            'rarer': 'schools cutting art, a full staff room, no teaching qualification and no wish to get one',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "The secondary school's art teacher is retiring at the end of the spring term, and the post "
                       'is in the local paper: art and design, full time, from the autumn. {colleague} says the art '
                       'room is the best room in the building, and the head is desperate.'),
                      ('W',
                       'A school needs its art taught properly, every year group, every week, as carefully as '
                       'anything else on the timetable. {N} could do that, and do it well.'),
                      ('U',
                       '{N} has always thought drawing can be taught like a language: line, tone, proportion, step '
                       'by step, until any child can do it.'),
                      ('B',
                       "Head of art, in time. A budget, a department, and the school's walls to fill. {N} reads the "
                       'pay scale twice.'),
                      ('R',
                       '{N} remembers {Ns} own art teacher, the one who let the class paint the ceiling. Every child '
                       'deserves one of those.'),
                      ('G',
                       'It is the school down the road, where half the street went. The art room looks out over the '
                       'playing fields and the hill behind.')],
            'tribal': [('',
                        'The old woman who taught the children the marks and the patterns can no longer see the rock '
                        'clearly. The elders look round the fire for someone who knows the marks and has patience '
                        'for small hands.')],
            'magic': [('',
                       'The town school needs a drawing master by the autumn, and the governors have posted the '
                       'place on the guildhall door: a room, a salary, and forty children who have never held a '
                       'silverpoint.')]},
 'outcomes': (['The head rings on the evening of the interviews, and by the autumn {N} has a classroom that smells '
               'of poster paint and a timetable pinned to the door.',
               'Whatever {N} chose, the art room is in good hands this year, and {N} is glad of the part played in '
               'it.'],
              ['The post goes to a newly qualified teacher from the city, and the head writes a kind letter.',
               'The interview lesson goes wrong, a class that will not settle and a head who writes everything down, '
               'and the letter is short.']),
 'options': [
    ('apply properly, with a scheme of work for every year group', 'W1', None, 0.45, '', {'title': 'art teacher', 'aims': 'art teacher', 'v': 'conformity, benevolence', 'world': {'tribal': 'offer to teach the children properly, a new pattern for every moon', 'magic': 'apply properly, with a plan of lessons for every form'}, 'chance': 0.5}),
    ('apply with a plan to teach drawing as a method, step by step', 'U1', None, 0.45, '', {'title': 'art teacher', 'v': 'achievement, conformity', 'world': {'tribal': 'offer to teach the marks as the old way teaches a hunt, one step at a time', 'magic': 'apply with a plan to teach drawing as a method, from the line to the figure'}, 'chance': 0.5}),
    ('apply as the first step to head of art, and say so at the interview', 'B1', None, 0.45, '', {'title': 'art teacher', 'v': 'power, achievement', 'world': {'tribal': 'offer to teach, and ask the elders for the first say over the painting place', 'magic': "apply as the first step to master of the school's drawing, and say so to the governors"}, 'chance': 0.5}),
    ('teach the interview lesson with charcoal and a roll of paper across the floor', 'R1', None, 0.45, '', {'title': 'art teacher', 'body': 'light', 'v': 'stimulation, benevolence', 'world': {'tribal': 'teach the children before the elders with burnt sticks and a whole rock face', 'magic': 'teach the trial lesson with charcoal and a roll of paper across the floor'}, 'chance': 0.5}),
    ('apply to the school down the road, where half the street went', 'G1', None, 0.45, '', {'title': 'art teacher', 'mark': 'stayed home', 'v': 'tradition, benevolence', 'world': {'tribal': "offer to teach your own band's children, as the old woman taught you", 'magic': 'apply to the school in your own quarter, where half the street learned its letters'}, 'chance': 0.5}),
    ('turn it down, and run paid weekend classes from the studio instead', 'B.5 R.5', None, 0.5, '', {'grants': 'teaching', 'mark': 'turned down a chance', 'habit': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'turn it down, and teach any who bring you a gift at your own fire', 'magic': 'turn it down, and take paying pupils on market days in your own studio'}, 'chance': 0.75}),
    ('help in the art room one morning a week for a term, the checks done first', 'U.5 G.5', None, 0.5, '', {'grants': 'cleared to work with children', 'v': 'achievement, benevolence', 'world': {'tribal': 'sit with the old woman and the children one morning in every few, and learn how she does it', 'magic': "help the old master one morning a week for a term, with the governors' leave"}, 'chance': 0.77}),
    ('start a lunchtime comic club at the school, with a teacher in the room', 'U.5 R.5', None, 0.5, '', {'grants': 'illustration', 'v': 'stimulation, achievement', 'world': {'tribal': 'teach the children to mark the story of a hunt on hides, their mothers sitting by', 'magic': 'start a broadsheet club at the school after hours, with a master in the room'}, 'chance': 0.75}),
    ('ask the head for the pay, the hours and the budget in writing first', 'W.5 B.5', None, 0.5, '', {'grants': 'handling red tape', 'v': 'security, power', 'world': {'tribal': 'ask the elders what share of the hunt the teaching brings, before saying yes', 'magic': 'ask the governors for the salary, the hours and the room in writing first'}, 'chance': 0.77}),
    ('tell the head quietly that the outside candidate never stays anywhere long', 'W.5 G.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': "approval: running down a rival for the post; backfire: the head checks with the candidate's last school, and neither of you is asked back", 'v': 'security, tradition', 'world': {'tribal': 'tell the elders quietly that the stranger from the next band never stays at any fire long', 'magic': 'tell the governors quietly that the master from the capital never stays anywhere long'}, 'chance': 0.73}),
 ]},
{'name': 'an empty shop on the corner',
 'stages': 'adult mature elder',
 'age': (25, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.03, 0.01),
 'drivers': 'prosper+.3 money+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'years',
 'roles': 'partner, friend, colleague, boss, rival',
 'requires': 'painter or sculptor | art teacher | shop owner | museum curator | illustrator for hire',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the empty shop on the corner of the high street, and a landlord who wants a tenant',
            'tribal': 'the old trader in carvings has died, and his place by the great fire at the gathering stands '
                      'empty',
            'magic': "the old picture dealer's hall on the square stands empty, and the guild will let it to whoever "
                     'can pay'},
 'timing': {'times': 'per painter, art teacher, shop owner, curator or illustrator of three years or more a year: '
                     "about 1 in 40 look seriously at opening a gallery or a makers' shop; most small galleries "
                     'close within a few years, and about 3 lives in 10,000 run one (catalogue share; estimate)',
            'likelier': 'an empty high street with low rents, savings or a patron, years of contacts among the '
                        "town's painters and buyers, good years when people buy art",
            'rarer': 'high rents, no savings, a town where nobody buys pictures, a lean year',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The old shoe shop on the corner has been empty for a year, its window full of dust and post. '
                       'The landlord has put a card in it: a low rent for the first year, to the right tenant. '
                       '{partner} walks past it every day, and has started to say "imagine".'),
                      ('W',
                       'A gallery would be a place the town could trust: fair prices, honest books, every artist '
                       'paid on time. {N} has been thinking for years about how one ought to be run.'),
                      ('U',
                       '{N} has walked through the empty shop in the mind a dozen times: the light from the big '
                       'window, the back room for framing, the long wall that would take the big canvases.'),
                      ('B',
                       'The corner is the best in town: the bus stop, the school run, the market on Saturdays. {N} '
                       'knows exactly which painters would sell from that window.'),
                      ('R',
                       '{N} wants to get the door open and paint the inside of the window tonight. Wine on Fridays, '
                       'music, people spilling out onto the pavement.'),
                      ('G',
                       "The shoe shop was there for sixty years. {N} would want the town's own makers in it: the "
                       'potter, the weaver, the man who carves spoons on the allotments.')],
            'tribal': [('',
                        'The old trader in carvings has died, and his place by the great fire at the gathering, '
                        'where the far bands come to look and trade, stands empty. The elders ask who will keep '
                        'it.')],
            'magic': [('',
                       'The old picture dealer on the square has died, and his hall stands empty with its shutters '
                       "down. The guild will let it to whoever can pay the first year's rent in silver on the "
                       'quarter day.')]},
 'outcomes': (['By the autumn there is a name above the door, a show in the window and a bell that rings when '
               "someone comes in, and the first months' sales pay the rent.",
               'Whatever {N} chose, the corner comes alive for a while, and the town notices.'],
              ['The bank says no, and the landlord lets the shop to a phone repair stall.',
               'The first winter is long and quiet, the rent outruns the sales, and by spring the card is back in '
               'the window.']),
 'options': [
    ('take the lease, and promise every artist honest books and a fair share', 'W1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'conformity, benevolence', 'world': {'tribal': 'take the place by the fire, and promise every carver an honest count and a fair share', 'magic': 'take the lease, and promise every painter honest books and a fair share'}, 'chance': 0.35}),
    ('open with one careful show, every piece researched and hung by theme', 'U1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'achievement, security', 'world': {'tribal': 'open with one careful laying-out, every carving placed by the animal it shows', 'magic': 'open with one careful show, every canvas studied and hung by its subject'}, 'chance': 0.35}),
    ('open with the two painters in town who already sell, and price them high', 'B1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'aims': 'gallery owner', 'v': 'power, achievement', 'world': {'tribal': 'open with the two carvers whose pieces already travel, and ask a high price for them', 'magic': 'open with the two painters in the city who already sell, and price them high'}, 'chance': 0.35}),
    ('take the shop on a handshake, and open on Friday before the licence comes', 'R1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'mark': 'defied an authority', 'closed': "law: trading before the council's licence for the change of use; backfire: the council fines the gallery and shuts its door for a month", 'v': 'stimulation, self-direction', 'world': {'tribal': 'take the place by the fire before the elders have agreed, and start trading that night', 'magic': "take the hall on a handshake, and open on market day before the guild's licence comes"}, 'chance': 0.35}),
    ("open a room for the town's own makers: the potter, the weaver, the carver", 'G1', None, 0.45, '', {'title': 'gallery owner', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'tradition, universalism', 'world': {'tribal': 'keep the place for the makers of your own band: the carver, the bowl-maker, the sewer of hides', 'magic': "open a hall for the quarter's own makers: the potter, the weaver, the carver"}, 'chance': 0.35}),
    ("rent only the window, and sell the town's painters on commission", 'B.5 G.5', None, 0.5, '', {'grants': 'selling', 'habit': True, 'v': 'power, tradition', 'world': {'tribal': 'keep only a corner of the hide, and trade the carvings of others for a share', 'magic': "rent only the window, and sell the quarter's painters for a share"}, 'chance': 0.76}),
    ('open it as a pop-up for one month with friends, and see what happens', 'R.5 G.5', None, 0.5, '', {'grants': 'a circle of artists', 'v': 'stimulation, benevolence', 'world': {'tribal': 'keep the place for one gathering with friends, and see what happens', 'magic': 'open the hall for one month with friends, and see what happens'}, 'chance': 0.76}),
    ('rent it as a studio instead, and paint in the window for passers-by', 'U.5 R.5', None, 0.5, '', {'grants': "studio of one's own", 'v': 'stimulation, achievement', 'world': {'tribal': "carve by the fire in the trader's old place, where every passer-by can watch", 'magic': 'rent the hall as a studio instead, and paint in the window for passers-by'}, 'chance': 0.74}),
    ('go into business with the shop owner next door, the costs split in writing', 'W.5 B.5', None, 0.5, '', {'grants': 'business partner', 'binds': True, 'v': 'security, power', 'world': {'tribal': 'keep the place together with a trader in flint, the shares agreed before the elders', 'magic': 'go into business with the bookseller next door, the costs split in a sealed deed'}, 'chance': 0.74}),
    ('write a business plan, and take it to the bank before signing anything', 'W.5 U.5', None, 0.5, '', {'grants': 'bookkeeping', 'v': 'security, achievement', 'world': {'tribal': 'count the furs and the flint you have against a year of trading, before you agree', 'magic': "write out the year's costs, and take them to the moneylender before signing anything"}, 'chance': 0.76}),
 ]},
{'name': 'the guild judges your masterpiece',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.05, 0.05, 0.03),
 'drivers': 'community+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'mentor, grandparent, colleague, rival, friend',
 'requires': 'craft maker | carpenter',
 'tenure': (4.0, 100.0),
 'worlds': {'earth': "the makers' guild judges masterpieces for its mark once a year, in the old hall",
            'tribal': "the master carvers of the gathering judge a new carver's piece, to cut the band's sign beside "
                      "the maker's own",
            'magic': "the craft guild's masters sit to judge a journeyman's masterpiece for the guild's mark"},
 'timing': {'times': 'per craft maker of four years or carpenter of six a year: about 1 in 20 put a piece before a '
                     'guild, a craft council or a selection panel for its mark; about 1 life in 1,000 is a maker '
                     'whose work is shown, collected or taught (catalogue share; estimate)',
            'likelier': "a guild or craft council in the county, an old master who pushes, a workshop of one's own, "
                        'years of pieces sold',
            'rarer': 'no guild within reach, a maker who sells well without a mark, hands or eyes beginning to fail',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       "Once a year the county's makers' guild judges pieces for its mark in the old corn exchange: "
                       'three masters, a long table, a magnifying glass, and no talking. {N} has been a maker for '
                       'years, and {mentor} says this is the year.'),
                      ('W',
                       "The guild's standard is written down to the last joint and glaze, and {N} has a copy pinned "
                       'above the bench. Every line of it is a promise to whoever will use the piece.'),
                      ('U',
                       '{N} has been working on one problem for two winters: a joint that holds without glue or pin. '
                       'If it works, the masters will not have seen it before.'),
                      ('B',
                       "The guild's mark doubles the price of a piece overnight. {N} knows which shops in the city "
                       'stock only marked work.'),
                      ('R',
                       "{N} has dreamed of one piece for ten years and never had the nerve. The guild's day is a "
                       'reason to make it at last.'),
                      ('G',
                       'The wood is from the old ash that fell in the storm behind the house of {grandparent}, '
                       'seasoned six years in the shed. {N} knows its grain like a face.')],
            'tribal': [('',
                        'At the gathering the master carvers sit in a row on the hides, and any carver who thinks '
                        "the work is ready lays one piece before them. If they nod, the band's sign is cut beside "
                        "the maker's own.")],
            'magic': [('',
                       "The craft guild's masters sit in their hall once a year to judge the journeymen's "
                       "masterpieces. A piece that passes earns the guild's mark, the right to keep an apprentice, "
                       "and a seat at the guild's table.")]},
 'outcomes': (["The three masters nod, the steward stamps the guild's mark into the underside of the piece, and {N} "
               'drives home very slowly with it on the passenger seat.',
               "Whatever {N} chose, the year's work is done properly, and the piece will outlast its maker."],
              ['The masters find a hairline gap in a joint, and the piece goes home with a polite note and an '
               'invitation to try again.',
               'The judging day is put off, and put off again, and the piece waits under a blanket in the workshop '
               'for another year.']),
 'options': [
    ("make the piece exactly to the guild's standard, every joint by the book", 'W1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'v': 'conformity', 'world': {'tribal': 'carve the piece exactly as the master carvers carve, every cut as they taught it'}, 'chance': 0.35}),
    ('make a piece around a joint nobody in the guild has seen before', 'U1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'v': 'achievement', 'world': {'tribal': 'carve a piece around a new way of setting bone in wood that no carver has seen'}, 'chance': 0.35}),
    ("make the piece the guild's own collectors would queue to buy", 'B1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'v': 'power, achievement', 'world': {'tribal': "carve the piece the far bands' traders would give the most for", 'magic': "make the piece the guild masters' own patrons would queue to buy"}, 'chance': 0.35}),
    ('make the piece dreamed of for ten years, whatever the guild expects', 'R1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'carve the piece dreamed of for ten winters, whatever the master carvers expect'}, 'chance': 0.35}),
    ('make it the old way, by hand, from the wood of your own valley', 'G1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'aims': 'master craftsperson', 'identity': True, 'v': 'tradition', 'world': {'tribal': 'carve it the old way, from the antler of a deer of your own hills'}, 'chance': 0.35}),
    ('skip the guild, and sell straight to the shops that want the work', 'B.5 R.5', None, 0.5, '', {'grants': 'loyal clientele', 'mark': 'turned down a chance', 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'skip the master carvers, and trade straight with the bands that want your pieces', 'magic': 'skip the guild, and sell straight to the merchants who want the work'}, 'chance': 0.76}),
    ('ask a master you know which pieces passed in past years, and why', 'U.5 B.5', None, 0.5, '', {'grants': 'contact in the trade', 'v': 'achievement, power', 'world': {'tribal': 'ask a master carver you know which pieces they nodded at before, and why'}, 'chance': 0.74}),
    ('have your old master quietly finish the joint you cannot get right', 'U.5 G.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: another maker's hand in a judged piece; backfire: the masters see two hands in the work, and the guild bars the maker for five years", 'v': 'achievement, benevolence', 'world': {'tribal': 'have the old carver who taught you quietly finish the cut you cannot get right', 'magic': "buy a hedge-witch's binding paste to hide the joint you cannot get right"}, 'chance': 0.76}),
    ('wait another year, and make it under the eye of the old master who taught you', 'W.5 G.5', None, 0.5, '', {'grants': 'mentor', 'self_control': '+', 'v': 'tradition, conformity', 'world': {'tribal': 'wait another winter, and carve it beside the old carver who taught you'}, 'chance': 0.74}),
    ('say at the guild meeting that its rules keep newcomers out', 'W.5 R.5', None, 0.5, '', {'mark': 'defied an authority', 'identity': True, 'v': 'universalism, stimulation', 'world': {'tribal': 'say at the gathering that the master carvers only nod at their own kin', 'magic': "say before the guild's table that its rules keep newcomers out"}, 'chance': 0.74}),
 ]},
{'name': 'a publisher reads the manuscript',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.05, 0.05, 0.04, 0.03),
 'drivers': 'era+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'boss, friend, mentor, rival',
 'requires': 'novelist | open-mic poet | illustrator for hire',
 'worlds': {'earth': 'an editor at a big publisher has asked to read the whole manuscript',
            'tribal': 'the elders of the gathering will hear one new long telling at the great fire, and choose '
                      'whether every band learns it',
            'magic': 'a printer of the city has asked to read the whole manuscript, and may take it to the press'},
 'timing': {'times': 'per novelist, poet of two years or illustrator of two years a year: about 1 in 20 have a '
                     'finished manuscript read in full by a publisher; publishers take on about 1 in 100 unsolicited '
                     'manuscripts and about 1 in 8 of those they ask to read in full, and about 2 lives in 1,000 '
                     'hold a contract for a book of their own (catalogue share; estimate)',
            'likelier': 'a finished and redrafted manuscript, a good year for the kind of book it is, a friend in '
                        'publishing, a prize or a reading that got noticed',
            'rarer': 'a half-finished manuscript, a crowded year for first books, no contacts at all',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'An email from an editor at a big publisher: she read the first pages from the pile and wants '
                       'the whole manuscript by the end of the month, if it is ready. {N} reads the email in the '
                       'kitchen four times, and then rings {friend}.'),
                      ('W',
                       '{N} owes this book to the people in it, the ones whose story nobody else has told. It has to '
                       'go out finished, and right.'),
                      ('U',
                       '{N} knows the middle sags. There is a month to fix it, and the whole thing is already pulled '
                       'apart across the floor.'),
                      ('B',
                       'An editor at a big house is a door that does not open twice. {N} wants to know who else is '
                       'on her list, and what they were paid.'),
                      ('R',
                       'Someone wants to read it, all of it! {N} has carried this book around like a fever for '
                       'years.'),
                      ('G',
                       'The book is about the town and the family: the farm, the chapel, the long winters, the '
                       'people who are gone. {N} made it so they would not be forgotten.')],
            'tribal': [('',
                        'At the gathering the elders will hear one new long telling at the great fire, and if they '
                        'nod, every band will learn it and carry it home. They have asked to hear {Ns}.')],
            'magic': [('',
                       'A printer of the city has read the first pages and wants the whole manuscript by the next '
                       'quarter day. If his reader likes it, it goes to the press, and the book is cried in the '
                       'market.')]},
 'outcomes': (['The editor rings on a Tuesday, a contract follows, and a year later there is a box of books on the '
               'doorstep with {Ns} name on every spine.',
               'Whatever {N} chose, the manuscript goes out into the world, and the writing goes on.'],
              ['The editor writes back after six weeks: she loved the voice, but the list is full, and she wishes '
               '{N} luck.',
               'Nothing comes back at all, and the manuscript goes into a drawer with the others.']),
 'options': [
    ('send the manuscript to one publisher at a time, exactly as each one asks', 'W1', None, 0.45, '', {'grants': 'a publishing contract; book in print', 'v': 'conformity', 'world': {'tribal': 'tell the long telling to the elders exactly as it was given to you, word for word', 'magic': 'send the manuscript to one printer at a time, exactly as each one asks'}, 'chance': 0.12}),
    ('redraft the opening chapters until every line earns its place, then send them', 'U1', None, 0.45, '', {'grants': 'a publishing contract; book in print', 'aims': 'celebrated author', 'v': 'achievement, conformity', 'world': {'tribal': 'work the telling over every night until each turn of it earns its place'}, 'chance': 0.12}),
    ("get the manuscript onto the editor's desk through a friend of a friend", 'B1', None, 0.45, '', {'grants': 'a publishing contract; book in print', 'v': 'power, achievement', 'world': {'tribal': "get a go-between who has the elders' ear to speak of your telling first", 'magic': "get the manuscript onto the printer's desk through a friend of a friend"}, 'chance': 0.12}),
    ('send the poems as they are, raw, with a letter written that night', 'R1', None, 0.45, '', {'title': 'novelist', 'grants': 'a publishing contract; book in print', 'v': 'stimulation', 'world': {'tribal': 'speak the verses as they came, raw, at the fire that night', 'magic': 'send the verses as they are, raw, with a letter written that night'}, 'chance': 0.12}),
    ('send the picture book made for the children of the family, just as it is', 'G1', None, 0.45, '', {'grants': 'a publishing contract; book in print', 'v': 'benevolence, tradition', 'world': {'tribal': 'show the elders the painted hide made for the children of your hearth, just as it is'}, 'chance': 0.12}),
    ('pay a small press to print five hundred copies, and sell them at readings', 'B.5 G.5', None, 0.5, '', {'grants': 'book in print', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'self-direction, universalism', 'world': {'tribal': 'give furs to the speakers of your own band to carry the telling round the fires', 'magic': 'pay a small printer for five hundred copies, and sell them at readings'}, 'chance': 0.76}),
    ('trade a read of the manuscript for editing work with a friend in publishing', 'U.5 B.5', None, 0.5, '', {'grants': 'editing', 'v': 'achievement, power', 'world': {'tribal': 'trade a winter of hunting for a hearing from an old teller who knows the elders', 'magic': "trade a read of the manuscript for copying work with a friend at the printer's"}, 'chance': 0.76}),
    ('claim in the covering letter that a famous writer has read and loved it', 'U.5 R.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: a famous name claimed in a covering letter; backfire: the editor knows the writer, and asks', 'v': 'achievement, stimulation', 'world': {'tribal': 'tell the elders a famous teller of the old days gave you the telling', 'magic': 'claim in the letter that a famous poet has read and loved it'}, 'chance': 0.74}),
    ('read the manuscript chapter by chapter to the writing group at the library', 'W.5 G.5', None, 0.5, '', {'grants': 'a circle of artists', 'door': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'tell the telling night by night to the others at your own fire', 'magic': "read the manuscript chapter by chapter to the writers' circle at the inn"}, 'chance': 0.76}),
    ('send it out, and promise yourself to write every morning whatever comes back', 'W.5 R.5', None, 0.5, '', {'grants': 'writing stories', 'habit': True, 'self_control': '+', 'v': 'conformity, stimulation', 'world': {'tribal': 'tell it at the gathering, and promise yourself a new verse every morning whatever comes'}, 'chance': 0.76}),
 ]},
{'name': 'a work in the national collection',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.03, 0.02),
 'drivers': 'era+.2 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'boss, mentor, partner, rival, friend',
 'requires': 'painter or sculptor | street artist | illustrator for hire | master craftsperson',
 'tenure': (5.0, 100.0),
 'worlds': {'earth': 'a curator from the national gallery in the capital asks about a piece for the national '
                     'collection',
            'tribal': 'the elders of every band will choose one carving or painted hide to keep in the great cave '
                      'for always',
            'magic': "the keeper of the realm's pictures asks about a piece for the royal gallery"},
 'timing': {'times': 'per painter, sculptor, street artist, illustrator or master craftsperson of five years or more '
                     'a year: about 1 in 40 in mid-life have a piece looked at for a national or regional public '
                     'collection; national collections buy a handful of works by living artists each year, and about '
                     '1 life in 10,000 becomes a renowned artist (catalogue share; estimate)',
            'likelier': 'a name in the art world, a dealer who shows the work in the capital, a body of work that '
                        'has been seen, a fashion that turns toward the work',
            'rarer': "a career far from the capital, a year when the collection's money is cut, work nobody has seen",
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A curator from the national gallery in the capital stood for a long time before {Ns} piece '
                       'in a mixed show, and has written to ask whether it might be offered to the national '
                       'collection. The acquisitions committee meets in the spring, and buys perhaps one work in a '
                       'hundred it is shown.'),
                      ('W',
                       '{N} thinks of the piece in the national collection, seen by school parties for a hundred '
                       'years. It should go there properly, or not at all.'),
                      ('U',
                       '{N} has always known which piece holds the whole of the work in it. The question is whether '
                       'the committee can be made to see it.'),
                      ('B',
                       'The national collection is the one line in a biography that changes every price after it. '
                       '{N} rings the dealer before replying.'),
                      ('R',
                       '{N} reads the letter standing up in the cold studio, and has to sit down on a paint tin.'),
                      ('G',
                       'The piece is of the valley where {N} grew up, made over three winters. {N} wonders whether '
                       'it belongs in the capital at all.')],
            'tribal': [('',
                        'Once in a generation the elders of every band choose one carving or one painted hide to be '
                        'carried to the great cave and kept there for always, where every band will see it. This '
                        'winter they have come to look at {Ns}.')],
            'magic': [('',
                       "The keeper of the realm's pictures has seen {Ns} work in the guildhall and asks whether a "
                       'piece might be offered to the royal gallery. The court decides at midsummer, and it takes '
                       'very few.')]},
 'outcomes': (["The committee meets, and the letter that follows carries the national gallery's crest at the top and "
               'a date for the hanging.',
               'Whatever {N} chose, the piece goes where {N} meant it to go, and the work goes on.'],
              ["The committee admires the piece and buys another, and the curator's letter is warm and short.",
               "The collection's money is cut that year, and nothing new is bought at all."]),
 'options': [
    ('offer the piece at a fair price, with its full history and condition report', 'W1', None, 0.45, '', {'title': 'renowned artist', 'aims': 'renowned artist', 'v': 'conformity', 'world': {'tribal': 'offer the piece freely, with its whole story told to the elders, from the first cut', 'magic': 'offer the piece at a fair price, with its full history and a report of its state'}, 'chance': 0.08}),
    ("write the curator an account of where the piece sits in a lifetime's work", 'U1', None, 0.45, '', {'title': 'renowned artist', 'v': 'achievement, conformity', 'world': {'tribal': 'tell the elders where the piece sits among all the work of your life', 'magic': "write the keeper an account of where the piece sits in a lifetime's work"}, 'chance': 0.08}),
    ('let the dealer set a high price, and wait for the curator to come back', 'B1', None, 0.45, '', {'title': 'renowned artist', 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'let the trader who carries your carvings ask a high gift, and wait for the elders to come back', 'magic': 'let the dealer set a high price, and wait for the keeper to come back'}, 'chance': 0.08}),
    ('offer the piece the curator did not ask for, the one that feels truer', 'R1', None, 0.45, '', {'title': 'renowned artist', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'offer the elders the piece they did not ask for, the one that feels truer', 'magic': 'offer the keeper the piece he did not ask for, the one that feels truer'}, 'chance': 0.08}),
    ('offer the piece made from the place and its people, and let it speak for them', 'G1', None, 0.45, '', {'title': 'renowned artist', 'v': 'tradition, universalism', 'world': {'tribal': 'offer the piece carved from the river stone of your own hills, and let it speak for them'}, 'chance': 0.08}),
    ('tell the curator a private buyer wants the piece by Friday, though none does', 'B.5 R.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: a bluff to a public collection; backfire: the curator calls the bluff, and the committee buys another artist's work", 'v': 'power, stimulation', 'world': {'tribal': 'tell the elders a far band wants the piece by the next moon, though none does', 'magic': 'tell the keeper a duke wants the piece by the quarter day, though none does'}, 'chance': 0.74}),
    ("give the piece to the town's own small museum instead, where the work began", 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'benevolence, tradition', 'world': {'tribal': "give the piece to your own band's cave instead, where the work began", 'magic': "give the piece to your own town's guildhall instead, where the work began"}, 'chance': 0.76}),
    ('lend the piece for a year, so the curators can live with it before deciding', 'U.5 G.5', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'let the piece stay in the great cave for a winter, so the elders can live with it before choosing', 'magic': 'lend the piece for a year, so the court can live with it before deciding'}, 'chance': 0.76}),
    ('sell it to the private collector who offered more, and tell the curator plainly', 'W.5 B.5', None, 0.5, '', {'grants': 'savings', 'self_control': '-', 'v': 'power, security', 'world': {'tribal': 'trade it to the far band that offered more, and tell the elders plainly', 'magic': 'sell it to the merchant who offered more, and tell the keeper plainly'}, 'chance': 0.76}),
    ('catalogue the work of a lifetime properly, every piece dated and photographed', 'W.5 U.5', None, 0.5, '', {'grants': 'a body of work', 'habit': True, 'v': 'security, achievement', 'world': {'tribal': 'lay out the work of a lifetime in the cave, every piece in the order it was made', 'magic': 'catalogue the work of a lifetime properly, every piece dated and drawn in a book'}, 'chance': 0.76}),
 ]},
{'name': 'a national prize for writing',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.03, 0.02),
 'drivers': 'era+.2 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning, publiclife',
 'horizon': 'months',
 'roles': 'boss, rival, friend, partner, mentor',
 'requires': 'novelist',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the latest book is on the shortlist for the prize everyone has heard of',
            'tribal': 'the elders will honour one maker of verses at the gathering, and every band will learn the '
                      'verses that win',
            'magic': "the academy will give its laurel to one book of the year, and the realm's chronicle will be "
                     'offered to its writer'},
 'timing': {'times': 'per novelist of three years or more a year: about 1 in 50 in mid-life see a book longlisted or '
                     'shortlisted for a national prize; the big prizes choose one book a year from a shortlist of '
                     'five or six, and about 1 life in 10,000 becomes a celebrated author (catalogue share; '
                     'estimate)',
            'likelier': "a book that sold and was reviewed, a publisher who enters it, a year when the book's "
                        'subject is in the air',
            'rarer': 'a small press that cannot afford the entry, a book out of fashion, a crowded year',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The phone rings at breakfast: {Ns} last book is on the shortlist for the prize everyone has '
                       'heard of, six books, the winner announced at a dinner in the capital in six weeks. By lunch '
                       'there are interview requests from three papers, and {partner} has opened something fizzy.'),
                      ('W',
                       'Six weeks of readings, interviews and a dinner in a hired suit. {N} means to do every part '
                       'of it properly, for the book and for the people in it.'),
                      ('U',
                       '{N} has read the other five books, and knows exactly how the judges will be comparing them. '
                       'The question is what {Ns} book does that the others do not.'),
                      ('B',
                       'A shortlist changes the next contract whatever happens. {N} wants the publisher spending '
                       'money on this book now, not next year.'),
                      ('R',
                       '{N} wants to run out into the street. Then, a moment later, wants to hide under the table '
                       'until it is over.'),
                      ('G',
                       'The book is about the valley and the people in it, most of them gone now. {N} thinks of them '
                       'reading about the shortlist in the local paper, and smiles.')],
            'tribal': [('',
                        'At the gathering the elders will honour one maker of verses above the others, and every '
                        'band will learn the winning verses by heart and carry them home. {Ns} name is spoken at '
                        'three fires.')],
            'magic': [('',
                       'The academy will give its laurel to one book of the year, and the court has let it be known '
                       "that the realm's chronicle will be offered to the winner. {Ns} book is one of six still on "
                       "the masters' table.")]},
 'outcomes': (['The envelope is opened at the dinner, the room turns, and {N} walks up to the stage with the speech '
               'folded in a pocket and not needed.',
               'Whatever {N} chose, the six weeks pass well, and the book finds more readers than it ever had.'],
              ['The prize goes to another book, the room applauds, and {N} claps with everyone else and means it, '
               'mostly.',
               "The judges' choice is a surprise to everyone, and the shortlist is forgotten by the spring."]),
 'options': [
    ('go to every reading the prize asks for, and speak about the book with care', 'W1', None, 0.45, '', {'title': 'celebrated author', 'grants': 'a prize for writing', 'v': 'conformity', 'world': {'tribal': 'speak the verses at every fire the elders ask, and speak of them with care', 'magic': 'go to every reading the academy asks for, and speak about the book with care'}, 'chance': 0.07}),
    ("show the prize's audiences how the book was built, part by part", 'U1', None, 0.45, '', {'title': 'celebrated author', 'grants': 'a prize for writing', 'v': 'achievement, conformity', 'world': {'tribal': 'show the bands how the verses were built, turn by turn', 'magic': "show the academy's audiences how the book was built, part by part"}, 'chance': 0.07}),
    ('let the publisher spend on the campaign: interviews, posters and parties', 'B1', None, 0.45, '', {'title': 'celebrated author', 'grants': 'a prize for writing', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'let the go-between carry your verses to every fire, and feast the elders who matter', 'magic': 'let the printer spend on the campaign: broadsheets, readings and suppers'}, 'chance': 0.07}),
    ('read the hardest chapter aloud on the shortlist night, and let it land', 'R1', None, 0.45, '', {'title': 'celebrated author', 'grants': 'a prize for writing', 'v': 'stimulation', 'world': {'tribal': 'speak the hardest verses at the great fire on the night of choosing, and let them land', 'magic': 'read the hardest chapter aloud before the academy, and let it land'}, 'chance': 0.07}),
    ('take the shortlist tour to the small towns the book is about', 'G1', None, 0.45, '', {'title': 'celebrated author', 'grants': 'a prize for writing', 'aims': 'celebrated author', 'v': 'tradition, benevolence', 'world': {'tribal': 'carry the verses back to the bands whose stories they tell', 'magic': 'take the book to the small towns of the valley it is about'}, 'chance': 0.07}),
    ('sign the next two books with the old publisher, at a better advance', 'B.5 G.5', None, 0.5, '', {'grants': 'a publishing contract', 'binds': True, 'v': 'power, tradition', 'world': {'tribal': "promise your next two tellings to the band's own speakers, for a better share", 'magic': 'sign the next two books with the old printer, at a better advance'}, 'chance': 0.76}),
    ('turn the tour down, and go back to the desk for the next book', 'U.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'self_control': '+', 'v': 'achievement, security', 'world': {'tribal': 'stay at your own fire, and go back to making the next telling', 'magic': 'turn the readings down, and go back to the desk for the next book'}, 'chance': 0.76}),
    ('drink through the prize dinner, and tell the judges what the prize is worth', 'U.5 R.5', None, 0.5, '', {'mark': 'made an enemy', 'self_control': '-', 'v': 'hedonism, stimulation', 'world': {'tribal': 'drink the strong brew through the feast, and tell the elders what their honour is worth', 'magic': "drink through the academy's supper, and tell the masters what their laurel is worth"}, 'chance': 0.74}),
    ('ask a judge you know from a festival committee to put in a word', 'W.5 B.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: lobbying a prize judge; backfire: a journalist hears of it, and the publisher withdraws the book from the prize', 'v': 'power, security', 'world': {'tribal': 'ask an elder you know from the gatherings to speak for your verses at the choosing', 'magic': "ask a master you know from the academy's council to put in a word"}, 'chance': 0.74}),
    ('give the shortlist money to the library where you first read, and say why', 'W.5 R.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'benevolence, conformity', 'world': {'tribal': 'give the gifts that came with the shortlist to the old teller who first taught you, and say why', 'magic': 'give the purse that came with the shortlist to the free library of your town, and say why'}, 'chance': 0.76}),
 ]},
{'name': 'the painted cave at the winter camp',
 'stages': 'adult mature elder',
 'age': (22, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'community+.2 harsh+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, community, meaning',
 'horizon': 'months',
 'roles': 'elder, rival, mentor, friend',
 'requires': 'painter or sculptor | street artist | life-drawing regular | art school student',
 'worlds': {'tribal': 'the elders choose who paints the great cave wall for the midwinter gathering, and what'},
 'only': 'tribal',
 'timing': {'times': 'per painter of the band in the tribal world (the cave painter or carver of two winters, the '
                     "painter of shelter walls of two, one who draws on the rock of three, or the great cave's "
                     'apprentice) a year: about 1 in 50, when the band winters at the great cave and the elders '
                     'choose who paints it (estimate); the great painted caves were painted and repainted over many '
                     'generations',
            'likelier': 'a winter at the great cave, a good autumn hunt to honour, an old cave painter who can no '
                        'longer climb',
            'rarer': 'a hard winter in the open, a band with a famous cave painter in his prime, a quarrel with the '
                     'elders',
            'gap_years': (5.0, 10.0)},
 'scenes': {'tribal': [('',
                        'The band has come back to the great cave for the winter, and the elders want a new wall for '
                        'the midwinter gathering, when every band in the valley comes to see the painted beasts. '
                        "They have chosen the subject already: the chief's great hunt of the autumn, the bison "
                        'falling at the river. They have not yet said who will paint it, and they are looking at '
                        '{N}.'),
                       ('W',
                        'The wall belongs to the band, and the elders have spoken. {N} thinks of every beast in its '
                        'right place, and of the old rules for which way the herds must run.'),
                       ('U',
                        'The damp creeps down the great wall every winter and the old ochre runs. {N} has been '
                        'grinding earths by the river all autumn, looking for one that holds.'),
                       ('B',
                        'Every band in the valley will stand before this wall at midwinter. Whoever paints it will '
                        'be spoken of at every fire for a generation, and {rival} knows it as well as {N} does.'),
                       ('R',
                        "{N} can already see the herd pouring across the rock in the torchlight, the bison's breath, "
                        'the hunters running. The hands itch for the charcoal.'),
                       ('G',
                        'The oldest walls of the cave were painted by the first painters, so long ago that nobody '
                        'remembers their names. {N} wonders what the new wall owes to the old.')]},
 'outcomes': (['By midwinter the wall is finished, and the bands that come for the gathering stand before it a long '
               'time in the torchlight.',
               'Whatever {N} chose, the wall is painted, and the band walks past it every morning a little prouder.'],
              ['The damp gets into the rock before the gathering, and half the beasts run and fade.',
               'The elders give the wall to {rival}, and {N} carries torches for the painting instead.']),
 'options': [
    ('paint the great wall exactly as the elders ask, every beast in its place', 'W1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'painter or sculptor', 'without': 'impossible', 'v': 'conformity, tradition', 'chance': 0.08}),
    ('grind a new ochre that holds in the damp, and paint the wall with it', 'U1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'painter or sculptor', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.08}),
    ("paint the wall so every band in the valley learns the painter's name", 'B1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'painter or sculptor', 'without': 'impossible', 'aims': 'renowned artist', 'v': 'power, achievement', 'chance': 0.08}),
    ('paint for three nights without sleep, by torchlight, as the beasts come', 'R1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'painter or sculptor', 'without': 'impossible', 'mark': 'took a wild risk', 'body': 'light', 'v': 'stimulation, hedonism', 'chance': 0.08}),
    ("paint the chief's hunt among the old herds, so the new wall speaks with the old", 'G1', None, 0.45, '', {'title': 'renowned artist', 'requires': 'painter or sculptor', 'without': 'impossible', 'v': 'tradition, universalism', 'chance': 0.08}),
    ('paint it with the other painters of the band, each beast by a different hand', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'made a friend', 'door': True, 'v': 'universalism, stimulation', 'chance': 0.7}),
    ('paint the chief at the head of the hunt, larger than life, as the chief wants', 'W.34 B.33 R.33', None, 0.5, '', {'self_control': '-', 'v': 'power, conformity', 'chance': 0.7}),
    ('ask the elders to give a place at the wall to the apprentice who has waited', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, security', 'chance': 0.7}),
    ('paint the old herds of the first painters, not the hunt the elders chose', 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'defied an authority', 'closed': "approval: painting against the elders' word; backfire: the elders have the wall rubbed out, and the next wall goes to another painter", 'v': 'self-direction, tradition', 'chance': 0.7}),
    ('mark the whole wall out in charcoal, and let the apprentices fill it in', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'pupils who remember you', 'binds': True, 'self_control': '+', 'v': 'achievement, tradition', 'chance': 0.7}),
 ]},
{'name': "the carver's mask for the dead",
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.02),
 'drivers': 'harsh+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community, faith',
 'horizon': 'months',
 'roles': 'elder, mentor, friend, rival',
 'requires': 'master craftsperson | craft maker | painter or sculptor',
 'worlds': {'tribal': 'the old chief has died, and the band needs a mask for the mourning'},
 'only': 'tribal',
 'timing': {'times': 'per carver of the band in the tribal world (a craft maker of four winters, a master carver or '
                     'a cave carver) a year: about 1 in 50, when a chief or an elder of standing dies and the band '
                     'wants a mask for the mourning (estimate); masks and carved grave goods for the honoured dead '
                     'are among the oldest carved things people have left',
            'likelier': "an old chief in a hard winter, a band that keeps the mourning masks, a carver the chief's "
                        'kin trust',
            'rarer': 'a young chief in good health, a band whose old carver is still strong, a carver new to the '
                     'band',
            'gap_years': (5.0, 15.0)},
 'scenes': {'tribal': [('',
                        'The old chief died in the first snow, and the band will mourn until the new moon. The '
                        "chief's kin come to {N} with a block of the old pine from beside the chief's hearth: a mask "
                        "is needed, for the chief's eldest to wear at the burying and then to lay with the chief in "
                        'the ground.'),
                       ('W',
                        'There are old measures for a mourning mask: so wide between the eyes, so long from brow to '
                        "chin, the band's marks on the cheeks. {N} knows them all, and means to keep every one."),
                       ('U',
                        "{N} remembers the chief's face better than most: the crooked nose from a fall, the way one "
                        'eye half closed when he laughed. A mask can hold a face, if it is cut truly enough.'),
                       ('B',
                        'Every band in the valley will come to the burying. The mask will be seen by all of them, '
                        'and so will the hand that cut it.'),
                       ('R',
                        "{N} sat at the chief's fire as a child. The grief is still new, and it wants to come out "
                        'through the knife.'),
                       ('G',
                        "The pine by the chief's hearth was old when the chief was young. {N} runs a hand over the "
                        'block and thinks of all the chiefs it has seen.')]},
 'outcomes': (["At the burying the chief's eldest wears the mask, and the whole band falls silent when the face "
               'comes into the firelight.',
               'Whatever {N} chose, the mask goes into the ground with the chief, and the band speaks of it at every '
               'mourning after.'],
              ['The wood splits along a hidden fault on the last night, and the mask is finished in haste by another '
               'hand.',
               "The chief's kin look at the mask for a long time and say nothing, and another carver's mask goes "
               'into the ground.']),
 'options': [
    ('carve the mask by the old measures, every line as the elders remember it', 'W1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'requires': 'craft maker', 'without': 'impossible', 'v': 'conformity, tradition', 'chance': 0.35}),
    ("carve the chief's face true, from memory and from the kin's telling", 'U1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'requires': 'craft maker', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.35}),
    ('carve it so finely that every band at the burying asks whose hand it was', 'B1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'requires': 'craft maker', 'without': 'impossible', 'aims': 'master craftsperson', 'v': 'power, achievement', 'chance': 0.35}),
    ('carve through the nights of mourning, with the grief in every cut', 'R1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'requires': 'craft maker', 'without': 'impossible', 'habit': True, 'self_control': '+', 'v': 'stimulation, benevolence', 'chance': 0.35}),
    ("carve it from the old pine by the chief's hearth, as the chief would have wished", 'G1', None, 0.45, '', {'title': 'master craftsperson', 'grants': "a maker's hallmark", 'requires': 'craft maker', 'without': 'impossible', 'identity': True, 'v': 'tradition, benevolence', 'chance': 0.35}),
    ("carve it with the oldest carvers, as the band's mask and no one hand's", 'W.34 U.33 G.33', None, 0.5, '', {'mark': 'made a friend', 'v': 'tradition, conformity', 'chance': 0.7}),
    ("carve a second mask for the band to keep, so the chief's face is not lost", 'W.34 U.33 B.33', None, 0.5, '', {'binds': True, 'v': 'security, achievement', 'chance': 0.7}),
    ('carve it with the young carvers beside, each cutting one line of it', 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'pupils who remember you', 'door': True, 'v': 'benevolence, tradition', 'chance': 0.7}),
    ('carve the chief as the chief truly was, scars and temper and all', 'U.34 B.33 R.33', None, 0.5, '', {'mark': 'defied an authority', 'closed': "approval: an unkind likeness of the dead chief; backfire: the chief's kin refuse the mask, and the band talks of it all winter", 'identity': True, 'v': 'self-direction, stimulation', 'chance': 0.7}),
    ('carve it fierce in a single night, from the skull of the bear the chief killed', 'B.34 R.33 G.33', None, 0.5, '', {'body': 'light', 'self_control': '-', 'v': 'stimulation, tradition', 'chance': 0.7}),
 ]},
{'name': "the queen's portrait sitting",
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'fortune+.2 prosper+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, publiclife, money',
 'horizon': 'months',
 'roles': 'boss, rival, mentor, partner',
 'requires': 'painter or sculptor | illustrator for hire',
 'tenure': (3.0, 99.0),
 'worlds': {'magic': 'the court wants a portrait of the queen, and the chamberlain has sent for the painter'},
 'only': 'magic',
 'timing': {'times': 'per guild painter or illuminator of three years or more in the magic world a year: about 1 in '
                     '60 is asked to sit with a member of the royal house for a portrait (estimate); court painters '
                     'were few, one or two in a generation, and many painters were tried before one was kept',
            'likelier': 'a name at court and in the salons, a portrait of a noble that was talked about, an old '
                        'court painter retiring',
            'rarer': 'a painter far from the capital, a court in mourning, a painter whose work the Order has '
                     'frowned on',
            'gap_years': (8.0, 15.0)},
 'scenes': {'magic': [('',
                       "The chamberlain's letter comes under the royal seal: the queen will sit for a portrait in "
                       'the long gallery, six mornings in the spring, and the court will judge it at midsummer. '
                       'Whoever paints her well, the gossip says, may be the next court painter. In the lanes behind '
                       'the academy an enchanter sells a varnish that makes a portrait smile at whoever looks at it, '
                       "for a price, and without the Order's leave."),
                      ('W',
                       'The court has its rules for a royal likeness: the robes of state, the crown on the left, the '
                       'hand on the orb. {N} has read them all and means to keep them.'),
                      ('U',
                       "The queen's face has been painted a hundred times, always the same way. {N} wants to see "
                       'what is really there, and twenty mornings would be better than six.'),
                      ('B',
                       "Court painter: a salary for life, rooms in the palace, the whole realm's commissions. "
                       "{rival} has been asked to sit with the queen's sister, and {N} has heard about the "
                       "enchanter's varnish."),
                      ('R',
                       'Every portrait of her in the long gallery is cold and stiff. {N} has seen her laugh at the '
                       'summer fair, once, and wants to paint that.'),
                      ('G',
                       'The queen grew up in the river country, far from the capital. {N} wonders whether anyone has '
                       'ever painted her among the fields and the people she came from.')]},
 'outcomes': (['At midsummer the court gathers in the long gallery, and the queen looks at the portrait a long time '
               'before she smiles.',
               'Whatever {N} chose, the spring at court is remembered well, and the name is spoken in the salons for '
               'years.'],
              ["The court chooses {rival}'s portrait, and {N} is thanked, paid and shown the door.",
               'The sittings are cut to three, the queen is tired and cross, and the portrait hangs in a corridor '
               'nobody uses.']),
 'options': [
    ('paint her in the robes and the pose the court herald sets, by every rule', 'W1', None, 0.45, '', {'title': 'renowned artist', 'v': 'conformity, tradition', 'chance': 0.08}),
    ('study her face through twenty sittings, and paint what is truly there', 'U1', None, 0.45, '', {'title': 'renowned artist', 'aims': 'renowned artist', 'self_control': '+', 'v': 'achievement, self-direction', 'chance': 0.08}),
    ("buy an enchanter's varnish that makes the portrait smile at whoever looks", 'B1', None, 0.45, '', {'title': 'renowned artist', 'mark': 'hid a wrong', 'closed': "approval: an enchanter's varnish used without the Order's leave; backfire: on the day of the unveiling the varnish shows the truth, the smile turns to a sneer, and the painter is sent from court", 'habit': True, 'v': 'power, achievement', 'chance': 0.18}),
    ('paint her with all the fire the court keeps hidden, and let it shock them', 'R1', None, 0.45, '', {'title': 'renowned artist', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'chance': 0.08}),
    ('paint her among the fields and the people of the river country she came from', 'G1', None, 0.45, '', {'title': 'renowned artist', 'v': 'tradition, benevolence', 'chance': 0.08}),
    ('ask for a field by the river for the family, in place of the fee', 'B.5 G.5', None, 0.5, '', {'grants': 'plot of land', 'door': True, 'self_control': '+', 'v': 'security, tradition', 'chance': 0.6}),
    ('paint her quickly, as she wishes to be seen, and charge the court double', 'B.5 R.5', None, 0.5, '', {'grants': 'savings', 'v': 'power, stimulation', 'chance': 0.6}),
    ('ask to paint her at ease in her garden, over many quiet sittings', 'U.5 G.5', None, 0.5, '', {'habit': True, 'v': 'universalism, achievement', 'chance': 0.8}),
    ('turn the court down, to keep the promise to paint the town hall first', 'W.5 R.5', None, 0.5, '', {'mark': 'kept your word', 'identity': True, 'v': 'conformity, self-direction', 'chance': 0.8}),
    ("ask the last court painter's widow for his notes on painting the queen", 'W.5 U.5', None, 0.5, '', {'v': 'achievement, conformity', 'chance': 0.6}),
 ]},
{'name': 'the illuminated book for the cathedral',
 'stages': 'adult mature elder',
 'age': (20, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.01, 0.01),
 'drivers': 'prosper+.2 era+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, faith, money',
 'horizon': 'years',
 'roles': 'boss, mentor, colleague, friend',
 'requires': 'illustrator for hire | art school student | life-drawing regular',
 'worlds': {'magic': "the Order's chapter wants a great book illuminated for the cathedral, a year's work"},
 'only': 'magic',
 'timing': {'times': 'per illuminator, academy student or sketcher of two years in the magic world a year: about 1 '
                     'in 60 is offered a share of the work on a great book for a cathedral or a noble house '
                     '(estimate); a great illuminated book took one hand or a small workshop a year or more',
            'likelier': "a new cathedral or a rich chapter, a hand the academy's masters have praised, a printer in "
                        'the town',
            'rarer': 'lean years, a chapter that sends its books to the capital, a sketcher no one has seen draw',
            'gap_years': (5.0, 10.0)},
 'scenes': {'magic': [('',
                       "The Order's chapter has commissioned a great book for the cathedral's high altar: two "
                       "hundred pages of the old hymns, every capital gilded, every border painted. The chapter's "
                       'clerk lays the first quire on the table before {N}, with a purse for the pigments and a year '
                       'to do it in. In the lanes behind the cathedral a wizard sells gold that shines by itself in '
                       "the dark, without the Order's blessing."),
                      ('W',
                       'The chapter keeps a pattern book of every border and capital ever used in its books. {N} '
                       'turns the pages slowly; a year of work, done right, page by page.'),
                      ('U',
                       "The gold in the old books has cracked in the cathedral's cold. {N} wants to know why, and "
                       'how to lay it so it never will.'),
                      ('B',
                       'A great book for the cathedral is the kind of work that makes a name in the city, and the '
                       'printers in the square copy anything that sells.'),
                      ('R',
                       'Two hundred empty margins, and a whole year. {N} can already see the beasts climbing the '
                       'borders and the saints laughing in the capitals.'),
                      ('G',
                       'The herbs and birds of the valley fill the old books {N} saw as a child in the village '
                       'chapel. {N} would like the new book to belong to the same country.')]},
 'outcomes': (['On the feast day the book is carried up the nave, and the gold catches the candlelight on every '
               'page.',
               "Whatever {N} chose, the year's work is done, and the chapter's clerk asks whether {N} would take the "
               'next book.'],
              ['The pigments run short in the winter and the chapter will not pay for more, and the book is finished '
               'by another hand.',
               "The chapter's new prior dislikes the borders, and the book goes into the library unshown."]),
 'options': [
    ("illuminate every page to the chapter's pattern book, letter by letter", 'W1', None, 0.45, '', {'title': 'illustrator for hire', 'grants': 'illustration', 'self_control': '+', 'v': 'conformity, tradition', 'chance': 0.4}),
    ('find a way of laying gold that will not crack in the cold of the nave', 'U1', None, 0.45, '', {'title': 'illustrator for hire', 'grants': 'illustration', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.4}),
    ('take the commission at the highest fee the chapter will pay', 'B1', None, 0.45, '', {'title': 'illustrator for hire', 'grants': 'illustration', 'aims': 'illustrator for hire', 'v': 'power, achievement', 'chance': 0.4}),
    ('fill the margins with wild beasts and laughing saints, and dare the chapter', 'R1', None, 0.45, '', {'title': 'illustrator for hire', 'grants': 'illustration', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'chance': 0.4}),
    ('paint the herbs and birds of the valley into every border, as the old books did', 'G1', None, 0.45, '', {'title': 'illustrator for hire', 'grants': 'illustration', 'v': 'tradition, universalism', 'chance': 0.4}),
    ("paint the town's own people and beasts into the margins, for them to find", 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'benevolence, stimulation', 'chance': 0.7}),
    ('sell the printers the right to copy the pages, for a share of every copy', 'U.5 B.5', None, 0.5, '', {'grants': 'royalties', 'door': True, 'v': 'achievement, power', 'chance': 0.7}),
    ("buy a wizard's gold that shines by itself in the dark nave, and gild every capital", 'U.5 R.5', None, 0.5, '', {'mark': 'took a wild risk', 'closed': "approval: unblessed wizard's gold in the Order's book; backfire: the gold turns to lead on the feast day, and the chapter takes the book from the illuminator", 'self_control': '-', 'binds': True, 'v': 'stimulation, achievement', 'chance': 0.7}),
    ('agree a fee for every page with the chapter, and hire two helpers', 'W.5 B.5', None, 0.5, '', {'grants': 'organising people', 'v': 'security, power', 'chance': 0.7}),
    ("work the whole year at the chapter's side, and keep every page and sketch", 'W.5 G.5', None, 0.5, '', {'grants': 'a body of work', 'habit': True, 'binds': True, 'v': 'conformity, tradition', 'chance': 0.7}),
 ]},
]

ECHOES = [
{'name': 'the sketchbook in the attic',
 'stages': 'young_adult adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'making, memory, home',
 'horizon': 'months',
 'roles': 'parent, child, friend, the class tutor',
 'once': True,
 'worlds': {'earth': "clearing a cupboard or a parent's attic, the old sketchbook from school",
            'tribal': 'clearing an old shelter, the painted hide from childhood, its marks still bright',
            'magic': "clearing a parent's attic, the old sketchbook from the drawing master's schoolroom"},
 'timing': {'times': 'per adult who drew as a child, once: about 1 in 10 come back to drawing after twenty years or '
                     'more (estimate)'},
 'after': "moment 'the urge to make something' or 'inspiration strikes' in someone who can draw ([drawing and "
          'painting]), 30 or more, who draws neither at a class nor for a living (no [life-drawing regular], '
          '[painter or sculptor], [street artist] or [illustrator for hire])',
 'delay_years': (0, 1),
 'likelier': 'much Red and Blue in the colour history; time to spare; retired',
 'rarer': 'stress above 1.5; more than one child at home; little money',
 'scenes': {'earth': [('',
                       'The urge to make something has been nagging at {N} for weeks. Then, clearing a cupboard, or '
                       'the attic of the old family house, {N} finds the sketchbook from school: a horse, a hand '
                       'drawn over and over, a portrait of {grandparent}, all in soft pencil gone silver with the '
                       'years.'),
                      ('W',
                       'Every page is dated in the corner, in a careful hand. {N} remembers the rule of drawing '
                       'something every single day, and how long it was kept.'),
                      ('U',
                       'Some of the drawings are better than {N} remembered and some are worse, and {N} can see '
                       'exactly why. The hand drawn twenty times on one page gets closer to right on the last one.'),
                      ('B',
                       '{N} looks at the best drawing for a long time. It is good, really good, and nobody has seen '
                       'it in thirty years. {N} wonders what it might have led to.'),
                      ('R',
                       '{N} sits on the floor in the dust and turns every page, and it all comes back at once: the '
                       'hours that vanished, the smell of the pencils, not caring about anything else.'),
                      ('G',
                       'There is a drawing of the garden as it was, the old apple tree, the shed that came down long '
                       'ago. {N} turns the pages slowly, as if they were letters from someone dear.')],
            'tribal': [('',
                        'Clearing an old shelter before the move to the winter camp, {N} finds a painted hide rolled '
                        "up in the roof poles: a running deer, a child's hand, marks made long ago at the flat rock, "
                        'still bright with ochre.')],
            'magic': [('',
                       "Clearing the attic of the old family house, {N} finds a sketchbook from the drawing master's "
                       'schoolroom, its corners nibbled by mice: a horse, a hand drawn over and over, a portrait of '
                       '{grandparent}, the chalk gone soft with age.')]},
 'outcomes': (['Within a few months {N} is drawing again, badly and then better, and wonders where the years went.',
               'The old drawings are taken out, shown and talked about, and at last they have somewhere to go.'],
              ['The sketchbook goes back in the box, the box goes back in the attic, and life fills up again.',
               '{N} tries, and every line comes out stiff and strange, and the pencils go back in the drawer.']),
 'options': [
    ('sign up for the Tuesday class at the college, and keep every Tuesday free for it', 'W1', None, 0.45, '', {'v': 'conformity', 'title': 'life-drawing regular', 'world': {'tribal': 'ask the painters for a place at the painting place, and climb up every evening', 'magic': "enrol in the academy's evening class, and keep every one of its evenings free"}, 'chance': 0.7}),
    ('finish the half-done drawings in it, properly, one each evening', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'grants': 'drawing and painting', 'habit': True, 'mark': 'learned a skill', 'world': {'tribal': 'finish the half-made marks on the hide, properly, one each evening', 'magic': 'finish the half-done drawings in the book, properly, one each evening'}, 'chance': 0.75}),
    ('show the best drawings to a framer, and ask what new ones would sell for', 'B1', None, 0.45, '', {'v': 'achievement, power', 'aims': 'painter or sculptor', 'world': {'tribal': 'show the hide to a trader at the gathering, and ask what new marks like these would fetch', 'magic': 'show the best drawings to a picture dealer, and ask what new ones would fetch'}, 'chance': 0.8}),
    ('go to a drop-in life class that same week, and draw fast until it comes back', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'life-drawing regular', 'door': True, 'world': {'tribal': 'climb to the painting place that same evening, and draw fast until it comes back', 'magic': "go to the academy's evening hall that same week, and draw fast until it comes back"}, 'chance': 0.7}),
    ('put it back in the box: it belongs to the child who drew it', 'G1', None, 0.45, '', {'v': 'tradition, security', 'mark': 'turned down a chance', 'world': {'tribal': 'roll the hide up again and leave it in the roof: it belongs to the child who painted it', 'magic': 'put it back in the chest: it belongs to the child who drew it'}, 'chance': 0.9}),
    ("book a week's painting course by the sea, and keep the promise made at fifteen", 'W1', 'R.7', 0.5, '', {'v': 'stimulation, hedonism', 'mark': 'kept your word', 'world': {'tribal': 'walk to the painted cliffs by the sea for a moon, and keep the promise made as a child', 'magic': "take a season's lodging at the painters' colony on the coast, and keep the promise made at fifteen"}, 'chance': 0.8}),
    ('pass it to a child in the family, with notes on how each drawing works', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'give the hide to a child of your hearth, and show how each mark was made', 'magic': 'pass the book to a child in the family, with notes on how each drawing works'}, 'chance': 0.75}),
    ("join the town's art society for its weekly drawing night, and stand for its committee", 'B1', 'W.7', 0.5, '', {'v': 'power, conformity', 'title': 'life-drawing regular', 'habit': True, 'world': {'tribal': 'join the painters at the painting place, and ask for a say in which walls are painted', 'magic': "join the painters' society for its weekly drawing night, and stand for its council"}, 'chance': 0.7}),
    ('draw every day for a month, fast and badly, to find out what is left', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'habit': True, 'self_control': '+', 'world': {'tribal': 'make marks every day for a moon, fast and rough, to find out what is left', 'magic': 'draw every day for a month, fast and rough, to find out what is left'}, 'chance': 0.8}),
    ('draw the old street from memory, and sell prints to the neighbours who lived there', 'G1', 'B.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'paint the old camp from memory on hides, and trade them to the families who lived there', 'magic': 'draw the old lane from memory, and sell prints to the neighbours who lived there'}, 'chance': 0.6}),
 ]},
{'name': 'the poems you never showed anyone',
 'stages': 'young_adult adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'writing, grief, meaning',
 'horizon': 'months',
 'roles': 'partner, child, friend, the host of the poetry night',
 'once': True,
 'worlds': {'earth': 'after a loss or a retirement, the notebook of poems in a drawer, never shown to anyone',
            'tribal': 'after a loss or the end of the hunting years, the verses made alone and never spoken at the '
                      'fire',
            'magic': 'after a loss or the end of working days, the bundle of verses tied with string in a drawer'},
 'timing': {'times': 'per adult who wrote poems, once: about 1 in 10 return to writing after a loss or in retirement '
                     '(estimate)'},
 'after': "moment 'the first months of retirement', 'your partner dies' or 'the notebooks come together' in someone "
          'who writes ([writing poems] or [writing stories]), 25 or more, who neither reads at a poetry night nor '
          'writes books (no [open-mic poet], no [novelist])',
 'delay_years': (0, 1),
 'likelier': 'much Red and White in the colour history; time to spare',
 'rarer': 'stress above 1.8; poor health',
 'scenes': {'earth': [('',
                       'After the loss, or the last day at work, the days are suddenly wide and quiet. At the back '
                       'of a drawer {N} finds the notebook: thirty years of poems, written late at night, on trains '
                       'and in waiting rooms, and never shown to a single person.'),
                      ('W',
                       '{N} wrote them the way some people keep a diary, faithfully, one a week for years, and then '
                       'stopped. It seems a kind of duty to see them through to something.'),
                      ('U',
                       'Reading them now, {N} can see what each one was trying to do, where it fell short, and how '
                       'it could be mended. The old ones read like drafts of something not yet written.'),
                      ('B',
                       'A few of them are good, better than some {N} has seen in print. It is strange to have kept '
                       'them hidden for so long, out of nothing but fear.'),
                      ('R',
                       '{N} reads the first one and has to sit down on the floor. Every feeling of thirty years is '
                       'in there, as raw as the day it was written.'),
                      ('G',
                       'The poems follow the years like rings in a tree: the first flat, the children small, the '
                       'garden, the long illness, the seasons going round. They belong to the family as much as to '
                       '{N}.')],
            'tribal': [('',
                        'In the quiet after a loss, or when the hunt goes on without {N}, the old verses come back: '
                        'made alone on long walks, never once spoken at the fire. {N} still knows every one of '
                        'them.')],
            'magic': [('',
                       'After a loss, or the last day in the counting house, {N} finds the bundle of verses tied '
                       'with string at the back of a drawer: thirty years of them, written by candlelight and on the '
                       'road, and never read by anyone.')]},
 'outcomes': (['The poems leave the drawer at last, and {N} finds out what they were for.',
               'Someone hears one and says that is exactly how it was.'],
              ['The poems go back where they were kept, and stay there.',
               '{N} starts, finds the old feelings too near, and has to stop.']),
 'options': [
    ("read one at the library's poetry evening, and go back every month after", 'W1', None, 0.45, '', {'v': 'conformity, tradition', 'title': 'open-mic poet', 'world': {'tribal': 'speak one at the fire on the next long night, and stand again every long night after', 'magic': "read one at the poets' night in the tavern, and go back every month after"}, 'chance': 0.7}),
    ('type them up, sort them, and redraft the best twenty into a collection', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'aims': 'novelist', 'identity': True, 'world': {'tribal': 'shape the best of them into one long telling, verse by verse, until it holds together', 'magic': 'copy them out fair, sort them, and redraft the best twenty into a book'}, 'chance': 0.7}),
    ('read the best of them at the poetry night in town, and make the room remember', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'open-mic poet', 'mark': 'took a wild risk', 'world': {'tribal': 'speak the best of them at the fire of the great gathering, and make every band remember it', 'magic': "read the best of them at the tavern's poets' night, and make the room remember it"}, 'chance': 0.7}),
    ('burn them in the garden, a page at a time', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'give them to the fire one by one, and never say them again', 'magic': 'burn them in the grate, a page at a time'}, 'chance': 0.9}),
    ('give the notebook to the one in the family who will keep it safe', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'teach the verses to the child of your hearth who will keep them', 'magic': 'give the bundle to the one in the family who will keep it safe'}, 'chance': 0.8}),
    ("read one of them aloud at the funeral or the family's next gathering", 'W1', 'G.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'speak one of them at the mourning fire, or the next time the family gathers', 'magic': "read one of them aloud at the burial or the family's next gathering"}, 'chance': 0.8}),
    ('join the writing group at the community centre, and help edit its yearly booklet', 'U1', 'W.7', 0.5, '', {'v': 'self-direction, benevolence', 'grants': 'writing poems', 'binds': True, 'world': {'tribal': 'join the old ones who keep the verses, and help choose which are spoken at the gathering', 'magic': 'join the verse circle at the chapter house, and help edit its yearly broadsheet'}, 'chance': 0.8}),
    ('pay a published poet to read them and tell the plain truth about them', 'B1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'give a good hide to the maker of verses every band repeats, for the plain truth about them', 'magic': 'pay a poet of the academy to read them and tell the plain truth about them'}, 'chance': 0.8}),
    ('post the rawest one online under your own name, for anyone to read', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': "speak the rawest one at another band's fire, where nobody knows the speaker", 'magic': 'pin the rawest one to the tavern door under your own name, for anyone to read'}, 'chance': 0.6}),
    ("read them at the care home's afternoons, where the old ones gather, every month", 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'title': 'open-mic poet', 'habit': True, 'identity': True, 'world': {'tribal': 'speak them to the old ones by the sheltered fire, where they sit through the cold days', 'magic': "read them on the almshouse's feast afternoons, where the old ones gather, every month"}, 'chance': 0.7}),
 ]},
{'name': 'the same canvas, years later',
 'stages': 'young_adult adult mature elder',
 'age': (18, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.1,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'work, making, meaning',
 'horizon': 'months',
 'roles': 'friend, partner, mentor, rival',
 'once': True,
 'worlds': {'earth': "years after the long shot that missed, the same kind of door opens again: the summer show's "
                     "forms, a publisher's window for new writing, a post advertised, the fair's judge named for the "
                     'coming summer',
            'tribal': 'winters after the attempt that failed, the elders again ask for hides for the cave, carvings '
                      'for the far trade and new tellings for the fire',
            'magic': "years after the attempt that failed, the same kind of notice goes up on the academy's door, in "
                     "the same clerk's hand"},
 'timing': {'times': 'per person who missed an art, craft or writing long shot: about 1 in 8 meet the same kind of '
                     'door again years later (estimate); many painters, makers and writers say they were taken on a '
                     'later try, after rejections, and few long shots land on the first one (estimate)'},
 'after': "a long shot missed in one of the moments of art-longshots.lib ('the sketch that went round the world', "
          "'the open submission to the great summer show', 'the manuscript in the pile on the floor', 'the late "
          "starter at the easel', 'the other side of the easel', 'the judge stops at your table at the craft fair'), "
          'holding [a long shot that missed], within the month of the miss; now 18 or more, not a [renowned artist] '
          'or a [celebrated author]; the try is for the same title again ({missed})',
 'delay_years': (3, 15),
 'likelier': 'drawing, painting, making or writing kept up since; much Red and Black in the colour history; time to '
             'spare',
 'rarer': 'stress above 1.5; little money; poor health',
 'scenes': {'earth': [('',
                       "Years after the long shot that missed, the same kind of door opens again: the summer show's "
                       'forms in the post, a publisher opening its doors to new writing for a month, a post '
                       'advertised, the judge for the coming fair named in the paper. {N} reads it twice, standing '
                       'very still, and then goes to look at the work from that time, still leaning against the wall '
                       'of the spare room.'),
                      ('W',
                       'Last time {N} did what was asked, and it was not enough. This time {N} knows exactly what is '
                       'asked, and has had years to get every part of it right.'),
                      ('U',
                       '{N} has gone over that attempt more often than anyone would guess, and knows now what was '
                       'missing from the work, and why it showed.'),
                      ('B',
                       'The people who decide are older now, and one or two of them know {Ns} name. The odds are '
                       'still long, but they are not the same odds.'),
                      ('R',
                       'The old hunger comes back all at once, as sharp as the first time. {N} is older, and has '
                       'long since stopped caring who thinks it foolish.'),
                      ('G',
                       '{friend} kept the cutting from that time in a drawer, and has said for years that one try is '
                       'not a life. The people at home would turn out for it, whatever came of it.')],
            'tribal': [('',
                        'Winters after the attempt that failed, the elders again send word round the bands: hides '
                        'for the cave, carvings for the far trade, new tellings for the long nights. {N} hears it at '
                        'the edge of the firelight, and the old wanting stirs.')],
            'magic': [('',
                       "Years after the attempt that failed, the same kind of notice goes up on the academy's door, "
                       "in the same clerk's careful hand. {N} reads it twice on the way to market, and does not go "
                       'to market.')]},
 'outcomes': (['This time the answer is yes; {N} reads it standing at the kitchen window, reads it again, and walks '
               'twice round the block before telling anyone.',
               'Whatever {N} chose, the second time feels different: steadier, and entirely {Ns} own.'],
              ['It is the same kind of no as last time, nearly to the word, and {N} finds that it stings less, and '
               'is glad to have gone back at all.',
               'The work gets further than before, and one person who matters says one true thing about it; {N} goes '
               'home the long way, in no hurry at all.']),
 'options': [
    ('try the same door again, the work finished and every rule met this time', 'W1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'conformity, security', 'world': {'tribal': 'go back to the same fire, the work finished and every old mark met', 'magic': 'go back to the same door, the work finished and every rule of the house met'}, 'chance': 0.04}),
    ('give it one more full year, then try again with the work rebuilt', 'U1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'give it one more full winter, then go back with the work remade', 'magic': 'give it one more full year, then go back with the work remade'}, 'chance': 0.04}),
    ('try again only when someone who matters will put the work forward', 'B1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'go back only when an elder who owes your hearth a gift will name the work', 'magic': 'go back only when a patron of standing will put the work forward'}, 'chance': 0.04}),
    ('try again older, staking a whole year on the boldest work yet', 'R1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'walk back into the firelight older, a whole winter staked on the boldest work yet', 'magic': 'walk back into the hall older, a whole year staked on the boldest work yet'}, 'chance': 0.04}),
    ('try again with everyone who stood by the first time behind the work', 'G1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'mark': 'made a friend', 'v': 'tradition, benevolence', 'world': {'tribal': 'go back with your own band behind the work this time, every hearth of it', 'magic': 'go back with your own ward behind the work this time, every lane of it'}, 'chance': 0.04}),
    ('keep a ledger of every open call for a year, and enter only the best three', 'W1', 'B.7', 0.5, '', {'habit': True, 'v': 'achievement', 'world': {'tribal': "keep count of every gathering's call for a year, and answer only the best three", 'magic': 'keep a ledger of every notice for a year, and answer only the best three'}, 'chance': 0.78}),
    ('try a new material for a year, only to see what it does', 'U1', 'R.7', 0.5, '', {'door': True, 'v': 'stimulation', 'world': {'tribal': 'carve in a new stone for a year, only to see what it does', 'magic': 'try a new medium for a year, only to see what it does'}, 'chance': 0.78}),
    ("use the name the first try made to start the town's own open show", 'B1', 'G.7', 0.5, '', {'grants': 'good name in town', 'habit': True, 'v': 'achievement, universalism', 'world': {'tribal': "use the name the first try made to start a showing for the band's own young hands", 'magic': "use the name the first try made to start the ward's own open show"}, 'chance': 0.78}),
    ('make the piece again from scratch before the old class, every step shown', 'R1', 'W.7', 0.5, '', {'self_control': '+', 'v': 'stimulation, security', 'world': {'tribal': 'paint the work again at the painting place before the others, every step shown', 'magic': 'make the piece again before the evening hall, every step shown'}, 'chance': 0.78}),
    ('go back to where the first work came from, and study it for a season', 'G1', 'U.7', 0.5, '', {'self_control': '+', 'v': 'tradition, universalism', 'world': {'tribal': 'go back to the place the first work came from, and watch it for a season', 'magic': 'go back to the place the first work came from, and study it for a season'}, 'chance': 0.78}),
 ]},
{'name': 'the long shot becomes a class to teach',
 'stages': 'young_adult adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'meaning, friends, making',
 'horizon': 'years',
 'roles': 'friend, partner, colleague, mentor',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, the library asks for a Saturday class for adult '
                     'beginners, and the story comes into the room with the teacher',
            'tribal': 'winters after the attempt that failed, the young ones of the band ask to learn the marks, and '
                      'the telling of the attempt comes with them',
            'magic': "years after the attempt that failed, the ward's guildhall asks for a class for grown beginners "
                     'on rest days, and the tale of it comes with the teacher'},
 'timing': {'times': 'per person who missed an art, craft or writing long shot: about 1 in 10 come to teach or tell '
                     'it years later, in a class, a workshop or a circle (estimate); most people who teach drawing '
                     'or writing to adult beginners once tried for something bigger themselves (estimate)'},
 'after': "a long shot missed in one of the moments of art-longshots.lib (as for 'the same canvas, years later'), "
          'holding [a long shot that missed]; now 25 or more, not a [renowned artist] or a [celebrated author]',
 'delay_years': (5, 30),
 'likelier': 'years gone by since the attempt; teaching, a class or a circle kept up; much White and Green in the '
             'colour history',
 'rarer': 'stress above 1.5; poor health',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, the library asks {N} to run a class for adult '
                       'beginners on Saturday mornings, ten weeks, drawing or writing, whichever {N} likes. On the '
                       'first morning, before anyone has picked up a pencil, a woman of sixty asks whether {N} ever '
                       'tried to make it big. The room goes quiet to hear the answer.'),
                      ('W',
                       '{N} tells it straight: what was asked, what {N} sent, and the letter that said no. Then the '
                       'register is taken and the class starts on time, because that is how a class should run.'),
                      ('U',
                       'Over the years {N} has understood that attempt better than at the time: what the people '
                       'choosing were looking for, and what {N} had not yet learned. That is worth teaching, more '
                       'than any technique.'),
                      ('B',
                       'It has become a good story, and {N} knows how to tell it: the long odds, the nerve, the near '
                       'thing at the end. A class remembers a teacher with a story.'),
                      ('R',
                       'The ache has mostly gone, and what is left is the memory of the nerve it took. {N} would '
                       'like every beginner in the room to feel that once.'),
                      ('G',
                       'The attempt is part of {Ns} life now, like the old house and the long friendships. What '
                       'matters this morning is the man at the back who has never drawn a line and whose hands are '
                       'shaking.')],
            'tribal': [('',
                        'One winter the young ones of the band ask {N} to show them the marks at the painting place, '
                        'and one of them asks whether it is true that {N} once took a hide to the elders and was '
                        'turned away. The young ones go quiet to hear the telling.')],
            'magic': [('',
                       "The ward's guildhall asks {N} to teach grown beginners on rest days, and on the first "
                       "morning an old weaver asks whether {N} once tried for the academy's great hall. The class "
                       'goes quiet to hear the tale.')]},
 'outcomes': (['The class fills up for a second term and a third, and years later strangers stop {N} in the street '
               'to say they still draw, or write, because of a Saturday morning at the library.',
               'Whatever {N} chose, the old attempt has found its place in the life, and {N} no longer flinches when '
               'it comes up.'],
              ['The class shrinks to three by the fifth week, and {N} teaches those three as well as {N} has ever '
               'done anything.',
               'Someone asks whether it was worth it, an answer comes out sharper than {N} meant, and {N} thinks '
               'about it on the bus home for a week.']),
 'options': [
    ("run the beginners' class every Saturday for years, and never miss a week", 'W1', None, 0.45, '', {'grants': 'pupils who remember you', 'habit': True, 'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'show the young ones the marks at the painting place every rest day, for years', 'magic': "teach the guildhall's beginners every rest day for years, and never miss one"}, 'chance': 0.78}),
    ('teach the class how the choosing really works, from inside a long shot', 'U1', None, 0.45, '', {'grants': 'teaching', 'door': True, 'v': 'achievement, conformity', 'world': {'tribal': 'teach the young ones how the elders really choose, from inside a long try', 'magic': 'teach the beginners how the academy really chooses, from inside a long shot'}, 'chance': 0.78}),
    ("tell the long shot's story at every talk and opening, a little better each time", 'B1', None, 0.45, '', {'grants': 'public speaking', 'habit': True, 'v': 'achievement, hedonism', 'world': {'tribal': "tell the long try at every gathering's fire, a little better each summer", 'magic': 'tell the tale at every opening and supper, a little better each time'}, 'chance': 0.78}),
    ('go back to a weekly life class, and draw for the joy of it', 'R1', None, 0.45, '', {'title': 'life-drawing regular', 'habit': True, 'v': 'hedonism, stimulation', 'world': {'tribal': 'go back to the painting place with the others, and paint for the joy of it', 'magic': 'go back to the evening hall with a sketchbook, and draw for the joy of it'}, 'chance': 0.78}),
    ('gather the old class and the new into one circle that meets in the kitchen', 'G1', None, 0.45, '', {'grants': 'a circle of artists', 'door': True, 'habit': True, 'mark': 'made a friend', 'v': 'benevolence, universalism', 'world': {'tribal': 'gather the old painters and the young into one circle at the painting place', 'magic': 'gather the old circle and the new beginners round one long kitchen table'}, 'chance': 0.78}),
    ("keep a fair list at the library's open-mic night, so every newcomer gets a turn", 'W1', 'R.7', 0.5, '', {'identity': True, 'door': True, 'v': 'universalism, stimulation', 'world': {'tribal': "keep the order fair at the long night's fire, so every young speaker gets a turn", 'magic': "keep a fair list at the poets' night in the tavern, so every newcomer reads"}, 'chance': 0.78}),
    ("write down what the attempt taught, and leave it in the class's library", 'U1', 'G.7', 0.5, '', {'identity': True, 'mark': 'learned a skill', 'v': 'universalism, tradition', 'world': {'tribal': 'put what the long try taught into a telling, and leave it with the band', 'magic': "write out what the attempt taught, and leave the pages in the guildhall's library"}, 'chance': 0.78}),
    ("set up a small yearly prize for the town's young artists, in your name", 'B1', 'W.7', 0.5, '', {'grants': 'good name in town', 'identity': True, 'v': 'power', 'world': {'tribal': 'give a fine hide each summer to the young painter of the band who paints best', 'magic': "found a small yearly purse for the ward's young painters, in your own name"}, 'chance': 0.78}),
    ('paint the long shot itself, the day and the nerves, until it is right', 'R1', 'U.7', 0.5, '', {'self_control': '+', 'v': 'stimulation', 'world': {'tribal': 'paint the long try itself on the rock, the day and the fear, until it is right', 'magic': 'paint the attempt itself, the day and the nerves, until it is right'}, 'chance': 0.78}),
    ('give the work from that day to the town hall, to hang where people pass', 'G1', 'B.7', 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': "give the work from that summer to the band's great cave, where every hearth passes", 'magic': "give the work from that day to the ward's hall, to hang where everyone passes"}, 'chance': 0.78}),
 ]},
]

EVENTS_READ = [{'name': 'the reviews of the show are in',
  'source': 'career',
  'tone': 'mixed',
  'base': 'need:competence-.03',
  'worlds': {'earth': 'the papers and the online notices the morning after the private view',
             'tribal': 'the talk at every fire after the carvings are shown at the gathering',
             'magic': 'the broadsheets cried in the square the morning after the showing in the guild hall'},
  'timing': {'times': 'per painter, street artist, illustrator or master craftsperson whose work is shown: once a '
                      'show; most shows in a city gallery are noticed somewhere, and many small ones get a line in '
                      'the local paper or a post online (estimate)',
             'likelier': "a first show of one's own, a gallery in a city, a critic at the private view, a name in "
                         'the art world',
             'rarer': 'a group show in a village hall, a week full of bigger news, work shown only online',
             'window': (17, 100),
             'gap_years': (1.0, 3.0)},
  'readings': [('a show hung and a promise kept: the work was honest, whatever they wrote',
                'W1',
                1.0,
                'meaning+.05',
                'W',
                '{N} reads the notices once, puts them in the folder with the price list, and is at the gallery at '
                'ten to meet the school party, as arranged.'),
               ('a lesson: one critic saw the weak corner of the big canvas',
                'U1',
                0.9,
                'competence+.05',
                'U',
                '{N} underlines the sharp sentence about the big canvas, goes back to the studio, and repaints the '
                'corner it was right about.'),
               ('a price list: a good line sells three pictures, a bad one sells one',
                'B1',
                0.6,
                'autonomy+.05',
                'B',
                '{N} rings the gallery before reading a word, asks how many pictures have sold, and has the best '
                'line printed on the card for the next show.'),
               ('a wound: one sentence that will sting for years',
                'R1',
                0.6,
                'belonging+.05',
                'R',
                '{N} reads the cruel sentence until it is learned by heart, then goes to the pub with the other '
                'painters from the show, and by closing time they have made a song of it.'),
               ('the way of things: some seasons the work is loved, and some it is not',
                'G1',
                0.9,
                'safety+.05',
                'G',
                '{N} cuts the kind paragraph out of the local paper for the family album, leaves the rest where it '
                'lies, and goes out to the garden.')],
  'scenes': {'earth': [('',
                        'The morning after the private view the notices are in: a short piece in the city paper, a '
                        'long one on an art website, and three lines in the local weekly. {N} reads them at the '
                        'kitchen table, with the invitation card still propped against the kettle.')],
             'tribal': [('',
                         'Traders from three bands have walked past the new carvings on the gathering ground, and by '
                         'evening every fire has its opinion: the old carvers grunt, the young ones scratch the '
                         'horses into the dust, and one elder says it plainly to {Ns} face.')],
             'magic': [('',
                        'The morning after the showing in the guild hall, the broadsheets are cried in the square: '
                        'two kind, one cruel, and a long letter from a gentleman of the academy. {N} reads them in '
                        'the window seat of the bakery opposite.')]}}]

MARKS = {}
