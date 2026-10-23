"""Chroma library earth_callings_land: compiled by build.py from earth_callings_land.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'the old hedge along the top lane',
 'stages': 'young_adult adult mature elder',
 'age': (18, 85),
 'alpha': 'W.15 U.15 B.4 R.15 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, nature',
 'horizon': 'months',
 'roles': 'boss, mentor',
 'requires': 'farmer | forester | park ranger | professional beekeeper | gardener or groundskeeper | farm hand',
 'worlds': {'earth': 'the old hedge along the top lane is overgrown and full of gaps, and the farm wants it gone so '
                     'the big machines can turn',
            'tribal': 'the old break of thorn and hazel along the top of the valley has grown wild, and the hunters '
                      'want it burned off so the herds come through',
            'magic': "the old hedge along the top lane of the lord's land has grown wild, and the steward wants it "
                     'grubbed out so the great ploughs can turn'},
 'timing': {'times': 'per farmer, forester, park ranger, beekeeper, groundskeeper or farm hand a year: about 1 in 20 '
                     'are asked to grub out, cut back or lay an old hedge or a line of old trees on the land they '
                     'work (estimate); old hedges are among the oldest things on farmland, and many were taken out '
                     'to make fields bigger (estimate); about 1.5 lives in 100 are farmers, 3 in 100 gardeners or '
                     'groundskeepers and 3 in 100 farm hands (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The hedge along the top lane is older than anything else on the land: hazel, hawthorn and '
                       'old field maple, laid by hand three generations ago and let go since. It is full of gaps, it '
                       "leans into the lane, and the contractor's machines cannot turn at the end of the field. "
                       '{boss} wants it out before the spring, and the contractor can come on Thursday. {mentor} '
                       'says there are nests in it every year, and that a hedge that old may be protected.'),
                      ('W',
                       "Old hedges have rules: some may not be taken out without the council's leave, and there is a "
                       'form for asking. {N} would rather know which kind this is before Thursday.'),
                      ('U',
                       'Nobody has ever counted what lives in it. {N} suspects the answer is more than anyone '
                       'thinks: the nests, the bats along it at dusk, the bees in the bank below.'),
                      ('B',
                       'A field without the hedge is two acres bigger and an hour quicker to work. {N} can see '
                       'exactly what that is worth, and what the hazel and the timber would fetch.'),
                      ('R',
                       '{N} has walked that lane since childhood, and the thought of a machine tearing through it '
                       'makes {N} want to stand in the gateway with arms folded.'),
                      ('G',
                       'A hedge like that is laid once a generation: each stem cut half through, bent over and '
                       'woven, and in three springs it is thick again from the root. {N} learned how from {mentor}, '
                       'and the hands still know it.')],
            'tribal': [('',
                        'Along the top of the valley runs an old break of thorn and hazel, planted by the '
                        "grandmothers of the band's grandmothers to turn the herds and the wind. It has grown wild "
                        'and gappy, and {boss}, the leader of the hunters, wants it burned off before the spring so '
                        'the herds will come through to the hunting ground. {mentor} says the birds have always '
                        'nested in it.')],
            'magic': [('',
                       "The hedge along the top lane of the lord's land is older than the manor: hazel and thorn and "
                       "old maple, laid by hand long ago and let go since. {boss}, the lord's steward, wants it "
                       "grubbed out before the spring so the great ploughs can turn, and the hedge-wardens' roll at "
                       "the lord's court may have its name on it.")]},
 'outcomes': (['By the spring it is settled, and the top lane looks the way {N} meant it to.',
               'The next summer {N} walks the top lane at dusk, and is glad of what was decided.'],
              ['The work takes twice as long as it should, through mud and rain, and {boss} is not pleased.',
               'It ends in a quarrel at the gate, and for a season {N} and {boss} barely speak.']),
 'options': [
    ('ask the council whether the hedge is protected, and wait for the answer', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'ask the elders whether the old break may be burned, and wait for their word', 'magic': "ask at the lord's court whether the hedge is on the wardens' roll, and wait"}, 'chance': 0.8}),
    ('walk the hedge at dawn and dusk for a week, and count what lives in it', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'grants': 'knowing the woods', 'world': {'tribal': 'watch the old break at dawn and dusk for a moon, and mark what lives in it'}, 'chance': 0.75}),
    ('grub it out in the winter, before anyone asks whether it is protected', 'B1', None, 0.45, '', {'v': 'power, achievement', 'mark': 'hid a wrong', 'closed': "law: a protected hedge grubbed out without leave; backfire: the council's officer sees the gap from the lane, and the fine and the order to replant follow", 'world': {'tribal': 'burn the old break off before the elders can talk about it', 'magic': "grub it out in the winter, before the court's wardens can look at the roll"}, 'chance': 0.85}),
    ('refuse to take it out, and tell {boss} to find someone else for the job', 'R1', None, 0.45, '', {'v': 'self-direction, universalism', 'mark': 'defied an authority', 'world': {'tribal': 'refuse to burn it, and tell the hunters to find other hands', 'magic': 'refuse to grub it out, and tell the steward to find another labourer'}, 'chance': 0.7}),
    ('lay the hedge by hand this winter, the old way, so it thickens from the root', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'habit': True, 'body': 'light', 'aims': 'steward of the land', 'world': {'tribal': "cut and bend the old break by hand, the grandmothers' way, so it thickens from the root", 'magic': 'lay the hedge by hand this winter, as the hedge-layers of the old manor did'}, 'chance': 0.75}),
    ('apply for a protection order on the hedge, and fight for it at the council', 'W1', 'R.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders to forbid any burning on the break, and speak for it at the fire', 'magic': "petition the lord's court to put the hedge on the wardens' roll, and argue for it"}, 'chance': 0.6}),
    ('work out a wider gate for the machines, so the hedge can stay', 'U1', 'G.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'work out a wider gap for the herds at one end, so the break can stay', 'magic': 'work out a wider gateway for the ploughs, so the hedge can stay'}, 'chance': 0.65}),
    ('sell the hazel and the timber, and pay for replanting the gaps by the book', 'B1', 'W.7', 0.5, '', {'v': 'power, conformity', 'aims': 'steward of the land', 'world': {'tribal': 'trade the hazel poles at the gathering, and plant new thorn in the gaps as the elders say', 'magic': "sell the hazel and the timber, and replant the gaps as the court's rules ask"}, 'chance': 0.55}),
    ('walk the hedge with the contractor at dawn, and show what lives in it', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'walk the break with the hunters at dawn, and show them the nests', 'magic': 'walk the hedge with the ploughmen at dawn, and show them what lives in it'}, 'chance': 0.7}),
    ('sell the sloes, nuts and poles every autumn, so the hedge pays its way', 'G1', 'B.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': "trade the break's sloes and hazel nuts at every autumn gathering, so it earns its keep", 'magic': 'sell the sloes, the nuts and the poles at the autumn fair, so the hedge pays its way'}, 'chance': 0.65}),
 ]},
{'name': 'the stream runs brown after the storm',
 'stages': 'young_adult adult mature elder',
 'age': (18, 85),
 'alpha': 'W.4 U.4 B.15 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, nature',
 'horizon': 'week',
 'roles': 'colleague, boss',
 'requires': 'farmer | forester | park ranger | professional beekeeper | gardener or groundskeeper | farm hand',
 'worlds': {'earth': 'after a night of storm the stream below the fields runs brown with soil, and the pool at the '
                     'bottom is filling with silt',
            'tribal': 'after the great storm the stream below the camp runs thick with earth, and the pool where the '
                      'fish spawn is filling with mud',
            'magic': 'after the storm the brook below the manor fields runs brown with soil, and the mill pond at '
                     'the bottom is silting up'},
 'timing': {'times': 'per farmer, forester, park ranger, beekeeper, groundskeeper or farm hand a year: about 1 in 10 '
                     'see soil wash off a field into a stream or a ditch after heavy rain (estimate); soil washed '
                     'off fields is one of the commonest troubles of small rivers on farmland (estimate); about 1.5 '
                     'lives in 100 are farmers, 3 in 100 gardeners or groundskeepers and 3 in 100 farm hands '
                     '(catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'After a night of rain like nobody remembers, the stream below the fields runs brown as tea, '
                       'and the pool at the bottom, where the trout lie in summer, has a bank of silt across it. Up '
                       'the slope, a field {colleague} ploughed straight down the hill last month has lost its top '
                       "inch of soil, and more is going every hour. The stream check for the farm's grant is due "
                       'this week, and {N} is the one who signs it.'),
                      ('W',
                       "The grant form asks whether the farm's ditches and streams run clean. {N} has always filled "
                       'it in honestly, and the answer has always been yes.'),
                      ('U',
                       'Soil goes where water takes it, and water takes the steepest way down. {N} can read on the '
                       'slope exactly which furrows sent it.'),
                      ('B',
                       'The washed field up the slope will be worth half what it was by the spring, and {colleague} '
                       'knows it. A buyer with ready money could do well this week.'),
                      ('R',
                       'The pool at the bottom was where {N} learned to swim, and now it is mud. {N} is halfway up '
                       "the hill to {colleague}'s gate before thinking about what to say."),
                      ('G',
                       'Grass holds soil, roots hold banks, and willow holds both. {N} looks at the bare bank and '
                       'thinks of what grew there when the stream ran clear.')],
            'tribal': [('',
                        'After the great storm the stream below the camp runs thick with earth, and the pool where '
                        "the fish spawn each spring is filling with mud. Up the slope, where {colleague}'s family "
                        'burned and dug the ground for a root patch this year, the earth is washing away with every '
                        'shower.')],
            'magic': [('',
                       'After a night of storm the brook below the manor fields runs brown with soil, and the '
                       "miller's pond at the bottom is silting up. Up the slope, a field {colleague} ploughed "
                       "straight down the hill has lost its top soil, and the lord's reeve comes this week to ask "
                       'whether the brook is kept.')]},
 'outcomes': (['The stream runs clear again by the summer, and the fish are back in the pool at the bottom.',
               'Whatever {N} chose, the next big storm sends less soil down the hill.'],
              ['The next storm sends the soil down again, and the pool at the bottom stays half mud for the year.',
               'It turns into a quarrel up and down the hill, and {colleague} stops waving across the fields.']),
 'options': [
    ('sign off the stream check as clean, since it ran clean all summer', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'hid a wrong', 'self_control': '-', 'closed': "approval: a stream check signed without looking; backfire: the inspector walks the stream the next month, the grant is held back, and the farm's name is noted", 'world': {'tribal': 'tell the elders the pool is as it always was, since it ran clear all summer', 'magic': 'tell the reeve the brook is kept, since it ran clear all summer'}, 'chance': 0.8}),
    ('take jars of water above and below the fields, and find where the soil comes from', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'mark': 'learned a skill', 'world': {'tribal': 'walk the stream above and below the camp, and find where the earth comes from'}, 'chance': 0.75}),
    ('offer {colleague} a low price for the washed field, while the mud is fresh', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': "offer {colleague}'s family a bargain for the washed slope, while the mud is fresh"}, 'chance': 0.7}),
    ('go straight up the hill and tell {colleague} what the ploughing has done', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'world': {'tribal': "go straight up the slope and tell {colleague}'s family what their digging has done"}, 'chance': 0.75}),
    ('drive willow stakes into the bare bank, so roots hold it by the summer', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'body': 'light', 'aims': 'steward of the land', 'chance': 0.75}),
    ('ring the river authority, and report the field that washed into the stream', 'W1', 'R.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'take it to the elders at the fire, and name the slope that washed into the stream', 'magic': 'report the washed field to the reeve, and name it before the manor court'}, 'chance': 0.6}),
    ('map where grass by the water would catch the soil, and plant those strips', 'U1', 'G.7', 0.5, '', {'v': 'achievement, tradition', 'aims': 'steward of the land', 'world': {'tribal': 'mark where grass by the water would catch the earth, and leave those strips unburned'}, 'chance': 0.65}),
    ('apply to the grant scheme for fencing and a grass strip, with every form in order', 'B1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': "ask the elders for the band's help to fence the stream bank, as the custom allows", 'magic': "petition the lord's steward for fencing and a meadow strip, with every form in order"}, 'chance': 0.7}),
    ('wade in with a rake, and clear the gravel to see how deep the silt lies', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'body': 'light', 'world': {'tribal': 'wade in and rake the mud off the spawning stones, to see how deep it lies', 'magic': 'wade in with a rake, and clear the millrace gravel to see how deep the silt lies'}, 'chance': 0.65}),
    ('let the wet bottom strip go to rough meadow, and sell the hay', 'G1', 'B.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'let the wet ground by the stream go to tall grass, and trade the cut grass at the gathering', 'magic': 'let the wet strip go to meadow, and sell the hay at the manor fair'}, 'chance': 0.65}),
 ]},
{'name': 'the year the lapwings did not nest',
 'stages': 'adult mature elder',
 'age': (28, 95),
 'alpha': 'W.15 U.4 B.15 R.15 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, nature',
 'horizon': 'months',
 'roles': 'colleague, mentor',
 'requires': 'steward of the land',
 'worlds': {'earth': "the trust's low meadow has had nesting lapwings every spring for as long as the counts go "
                     'back, and this spring there are none',
            'tribal': "the wet meadow below the grove has had the crested plovers' nests every spring the band "
                      'remembers, and this spring there are none',
            'magic': "the grove's wet meadow has had the crested plovers' nests every spring in the druids' book, "
                     'and this spring there are none'},
 'timing': {'times': "per steward of the land a year: about 1 in 8 see a bird or a flower the trust's land is known "
                     'for fail to come back (estimate); birds that nest on the ground in wet meadows have fallen '
                     'hard on farmland over the last generations (estimate); about 1 life in 1,000 is a steward of '
                     'the land (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "Every spring for twenty-two years the trust's count sheets have the same line: lapwings "
                       'nesting on the low meadow, eight pairs, eleven, six, nine. This spring {N} walks the meadow '
                       'three dawns running and finds none. The ground is drier than it was; dogs run loose from the '
                       'new path by the estate; the grazier stopped putting cattle on it two years ago. {colleague} '
                       'from the committee wants to know what the trust means to do.'),
                      ('W',
                       "The trust's plan for the meadow was written years ago and nobody has looked at it since. "
                       'There are rules the trust could make, and it has never made them.'),
                      ('U',
                       'Twenty-two years of count sheets sit in a box in {Ns} back room. Somewhere in them is the '
                       'year it started to go wrong.'),
                      ('B',
                       'Nothing happens on the meadow without money: the grazier wants paying, the drains want '
                       'blocking, the fence wants building. {N} knows who funds this kind of thing.'),
                      ('R',
                       '{N} lay out on that meadow at dawn as a child and watched the lapwings tumble over it. A '
                       'spring without that sound is a spring {N} will not accept.'),
                      ('G',
                       'Lapwings nest in short grass by wet hollows, and cattle make both. The meadow has grown rank '
                       'and dry since the cattle went, and the birds went with them.')],
            'tribal': [('',
                        'Every spring the band remembers, the crested plovers have tumbled over the wet meadow below '
                        "the grove and nested in its short grass. This spring {N}, the band's keeper of the grove, "
                        'walks it three dawns running and finds no nest. The herds have grazed elsewhere since the '
                        'river moved, and the meadow has gone tall and dry.')],
            'magic': [('',
                       "The druids' book of the grove has a line for every spring: the crested plovers nesting on "
                       'the wet meadow, eight pairs, eleven, six. This spring {N}, druid of the grove, finds none. A '
                       "new road runs along the meadow's edge, and the lord's hounds run loose on it.")]},
 'outcomes': (['The next spring three pairs are back on the low meadow, tumbling over it at dawn.',
               'Whatever {N} chose, the meadow is wetter and quieter by the next spring, and the worry eases.'],
              ['The next spring is as empty as this one, and {N} is the one who has to say so.',
               'The plan stalls in talk, the summer comes, and the meadow goes on as it was.']),
 'options': [
    ('close the meadow to dogs from spring to midsummer, with a sign on every gate', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'ask the elders to keep the dogs from the wet meadow until midsummer', 'magic': 'ask the lord to keep his hounds off the wet meadow until midsummer'}, 'chance': 0.75}),
    ('go through twenty years of count sheets, and find the year it began', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'grants': 'the one everyone asks', 'world': {'tribal': 'ask every old one of the band in turn which spring the plovers began to go', 'magic': "go through every spring in the druids' book, and find the year it began"}, 'chance': 0.8}),
    ('find the money to pay a grazier to bring cattle back and mow late', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'trade with the herding band to bring their herds through the wet meadow each spring', 'magic': "strike a bargain with a drover to graze the meadow, paid from the grove's tithes"}, 'chance': 0.7}),
    ("block the meadow's old drains one night, so the hollows hold water again", 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'mark': 'took a wild risk', 'closed': "approval: drains blocked that also drain the tenant's field; backfire: the tenant's next field floods, and the trust pays for the damage and the apology", 'world': {'tribal': "dam the meadow's ditch one night with stones and turf, without asking the elders", 'magic': "block the meadow's drains one night, without the lord's leave"}, 'chance': 0.8}),
    ('graze the meadow short again with a few old-breed cattle of your own', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'habit': True, 'aims': 'keeper of the land', 'world': {'tribal': "bring the band's own small herd to graze the wet meadow each spring", 'magic': "graze the meadow short with a few of the grove's own old-breed cattle"}, 'chance': 0.7}),
    ("put a nesting season into the trust's rules, voted on by the members", 'W1', 'G.7', 0.5, '', {'v': 'conformity, tradition', 'aims': 'keeper of the land', 'world': {'tribal': "ask the elders to make the plovers' season a custom of the band", 'magic': "ask the circle to write a nesting season into the grove's law"}, 'chance': 0.65}),
    ('draw up a meadow plan the grazier and the dog walkers can both keep', 'U1', 'W.7', 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': 'work out a way for the herds and the dogs that every hearth can keep', 'magic': "draw up a meadow plan the drovers and the lord's huntsmen can both keep"}, 'chance': 0.6}),
    ('interest the university in the meadow, and win a student to study it', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'interest the wise woman of the next band in the meadow, and have her watch it a season', 'magic': 'interest the scholars of the college in the meadow, and win a student to study it'}, 'chance': 0.7}),
    ('rally the volunteers and the local paper, and shame the estate over its dogs', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'world': {'tribal': 'rally the young hunters to tell every band how the dogs spoiled the meadow', 'magic': "rally the town's broadsheet against the lord's loose hounds"}, 'chance': 0.6}),
    ('lie out on the meadow at dawn each morning, and wait for the first bird back', 'G1', 'R.7', 0.5, '', {'v': 'tradition, stimulation', 'body': 'light', 'world': {'tribal': 'lie out on the wet meadow at dawn each morning, watching for the first plover'}, 'chance': 0.7}),
 ]},
{'name': 'a wood given with strings attached',
 'stages': 'adult mature elder',
 'age': (28, 95),
 'alpha': 'W.35 U.1 B.35 R.35 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community, money',
 'horizon': 'months',
 'roles': 'elder, colleague',
 'requires': 'steward of the land',
 'worlds': {'earth': 'an old landowner offers the trust his wood for nothing, on one condition: that his shooting '
                     'days go on in it for as long as he lives',
            'tribal': "an old hunter of the next band offers the grove's keeper his family's wood on the ridge, on "
                      'condition that his kin still hunt it each autumn',
            'magic': 'an old knight with no heir offers the grove his wood on the hill, on condition that his '
                     'hunting days go on in it as long as he lives'},
 'timing': {'times': 'per steward of the land a year: about 1 in 15 are offered land or a wood as a gift or a '
                     'bequest with conditions attached (estimate); many land trusts got their first land as a gift '
                     'or through a will (estimate); about 1 life in 1,000 is a steward of the land (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{elder}, who owns the wood above the town, asks {N} round for tea. He is eighty-six and has '
                       'no children who want the place. He will give the trust the wood, all forty acres of it, for '
                       'nothing. There is a letter from his lawyer, and one line in it says the shooting days go on, '
                       'with his friends and the pheasant pens, for as long as he lives. The committee meets on '
                       'Thursday.'),
                      ('W',
                       "A gift like this goes before the members, all of it, and the trust's rules say so. A line "
                       'kept back would be a lie told to the members.'),
                      ('U',
                       '{N} knows roughly what pheasant pens do to the floor of a wood, but not how much. It could '
                       'be measured.'),
                      ('B',
                       'Forty acres for nothing. The trust has never had a chance like it, and {N} knows the old '
                       "man's lawyer is a friend of a friend."),
                      ('R',
                       "Birds raised in pens and driven over guns in the trust's own wood. {N} can already hear what "
                       'the members will say, and part of {N} agrees with them.'),
                      ('G',
                       'The wood has stood two hundred years, shoot or no shoot. Old men do not live forever, and '
                       'woods outlast their owners.')],
            'tribal': [('',
                        "{elder}, an old hunter of the next band, comes to {N}, the band's keeper of the grove, with "
                        "a gift: his family's wood on the ridge, for the grove to keep. His kin must still hunt "
                        'there every autumn, as they always have, for as long as he lives.')],
            'magic': [('',
                       '{elder}, an old knight with no heir, sends for {N}, druid of the grove. He will give the '
                       'grove his wood on the hill, forty acres of old oak, if his hunting days go on in it with his '
                       'friends for as long as he lives. The circle meets at the new moon.')]},
 'outcomes': (['By the spring it is settled, and {N} can face the members at the meeting with a clear head.',
               "Whatever {N} chose, the wood above the town is still standing, and the trust's name is still good."],
              ['The wood splits everyone down the middle, and two old friends stop speaking.',
               'It drags on all winter, nobody is pleased with the end of it, and {N} is the one they blame.']),
 'options': [
    ('put the whole letter before the members, the shooting line included', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'tell the whole band at the fire what the gift asks, the hunting included', 'magic': "lay the knight's whole letter before the circle, the hunting clause included"}, 'chance': 0.8}),
    ('survey what the pheasant pens do to the wood floor, and put a number on it', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': 'count the deer and the young trees on the ridge, and see what the hunts leave', 'magic': "survey what the knight's hunts do to the floor of the wood, and set it down"}, 'chance': 0.75}),
    ('bargain with the old man for fewer shooting days and no new pens', 'B1', None, 0.45, '', {'v': 'power, achievement', 'grants': 'friend in power', 'world': {'tribal': 'bargain with the old hunter for fewer hunts and only his own kin', 'magic': 'bargain with the knight for fewer hunting days and no new kennels'}, 'chance': 0.7}),
    ('refuse the wood outright while the shooting goes on in it', 'R1', None, 0.45, '', {'v': 'self-direction, universalism', 'mark': 'made an enemy', 'world': {'tribal': 'refuse the ridge wood outright while another band hunts in it', 'magic': "refuse the knight's wood outright while his hunts go on in it"}, 'chance': 0.75}),
    ('take the wood, keep the shoot, and leave the shooting line out of the minutes', 'G1', None, 0.45, '', {'v': 'tradition, security', 'mark': 'hid a wrong', 'closed': "approval: a gift's condition kept from the members; backfire: the members find the shooting line in the deeds at the next meeting, and two of the committee resign", 'world': {'tribal': "take the wood, and say nothing at the fire of the old hunter's terms", 'magic': "take the wood, and leave the hunting clause out of the circle's record"}, 'chance': 0.85}),
    ('take the gift only if the deed keeps the wood standing for good', 'W1', 'G.7', 0.5, '', {'v': 'conformity, tradition', 'world': {'tribal': 'take the gift only if the old hunter swears at the fire that the wood will never be cut', 'magic': 'take the gift only if the deed binds every heir to keep the wood standing'}, 'chance': 0.6}),
    ('write rules for the shoot: no new pens, and no shooting in the nesting months', 'U1', 'W.7', 0.5, '', {'v': 'universalism, conformity', 'aims': 'keeper of the land', 'world': {'tribal': 'work out rules for the autumn hunts: no fires, and no hunting in the birthing season', 'magic': 'write rules for the hunts: no new kennels, and no hunting in the nesting months'}, 'chance': 0.65}),
    ('have a lawyer friend read the deed, and find what else it binds', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': "ask a trader who knows the ways of gifts what else the old hunter's terms bind", 'magic': 'have a clerk of the court read the deed, and find what else it binds'}, 'chance': 0.7}),
    ("take the whole thing to the town's paper, and let the town decide", 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'world': {'tribal': 'tell it at every fire in the valley, and let the bands decide', 'magic': "take it to the town's broadsheet, and let the town decide"}, 'chance': 0.65}),
    ('walk the wood with the old man, and hear why the shoot matters to him', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, tradition', 'mark': 'made a friend', 'world': {'tribal': 'walk the ridge wood with the old hunter, and hear why the hunts matter to him', 'magic': 'walk the wood with the old knight, and hear why the hunts matter to him'}, 'chance': 0.55}),
 ]},
{'name': 'the land trust needs a chair',
 'stages': 'adult mature elder',
 'age': (28, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.04, 0.03),
 'drivers': 'community+.3 prosper+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, nature',
 'horizon': 'months',
 'roles': 'mentor, colleague, rival, boss',
 'requires': 'farmer | forester | park ranger | professional beekeeper',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': "the old chair of the town's land trust steps down, and the members ask who will keep the "
                     'meadow, the wood and the river after her',
            'tribal': 'the old keeper of the grove can no longer walk the hunting grounds, and the bands ask who '
                      'will keep the grove and the grounds after her',
            'magic': 'the old druid of the grove goes to her rest, and the circle asks who will keep the grove after '
                     'her'},
 'timing': {'times': 'per farmer, forester, park ranger or beekeeper of three years or more a year: about 1 in 30 '
                     "are asked to stand for the chair of the town's land, wildlife or commons trust (estimate); "
                     'about one such trust a town of 10,000 to 20,000, its chair held about ten years (the land '
                     "trusts' census and the wildlife and commons groups; estimate); about 1 life in 1,000 is a "
                     'steward of the land (catalogue share)',
            'likelier': 'a chair stepping down, a fight over a field everyone knows, years of work parties, good '
                        'years with money for land',
            'rarer': 'a chair who stays twenty years, a trust that has folded, a town that has never had one',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       "{mentor} has chaired the town's land trust for nineteen years: the low meadow, the wood "
                       'above the town, two miles of river bank and a committee of nine who argue about all of them. '
                       'At the yearly meeting she stands up and says this is her last year. Afterwards three members '
                       "come and find {N} by the tea urn. {rival}, who sits on the council's planning committee, has "
                       'already said he would do it.'),
                      ('W',
                       'The trust has a constitution, and the chair is elected under it by the members, with a '
                       'seconder and a vote. {N} has read it twice.'),
                      ('U',
                       '{N} has opinions about the trust: the counts nobody looks at again, the plan nobody follows. '
                       'In the chair, they could be put right.'),
                      ('B',
                       'The chair is where the money, the council and the land deals meet. {N} would rather hold it '
                       'than watch {rival} hold it.'),
                      ('R',
                       "{N} has spent more Saturdays in the trust's mud than anyone. If anyone is going to fight for "
                       'that meadow, it should be {N}.'),
                      ('G',
                       "{N} has worked this valley's land for years, and knows which field floods first and where "
                       'the orchids come up. Nobody knows it better, in all its seasons.')],
            'tribal': [('',
                        'The old keeper of the grove, {mentor}, has grown too stiff to walk the hunting grounds and '
                        'says so at the fire. The bands look round for who will keep the grove, the burning and the '
                        'grounds after her, and {rival} of the other hearth has already said he will.')],
            'magic': [('',
                       'The old druid of the grove, {mentor}, has gone to her rest after forty years, and the circle '
                       'of the grove will name her successor at the next new moon. {rival}, who has the ear of the '
                       "lord's steward, has already put his name forward.")]},
 'outcomes': (['Within the season it is settled, and the valley turns to {N} first.',
               'Whatever {N} chose, the meadow, the wood and the river are in good hands, and {N} sleeps well that '
               'month.'],
              ['The choice falls on {rival}, and {N} has to smile through it with everyone else.',
               'It goes badly at the one meeting that mattered, and the choice falls on someone from outside the '
               'valley.']),
 'options': [
    ("stand for the chair by the trust's rules, with a seconder and a statement", 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'steward of the land', 'requires': 'good name in town', 'without': 'approval', 'lacking': 0.5, 'world': {'tribal': 'ask the elders and the old keeper by the custom, and keep every old rule of the grove', 'magic': 'put your name to the circle in the proper form, with a word on every law of the grove'}, 'chance': 0.3}),
    ('bring the members a written plan for the meadow, the wood and the river', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'steward of the land', 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'show the bands at the fire how you would keep the grove, the burning and the grounds, season by season', 'magic': 'bring the circle a written plan for the grove, the meadow and the stream'}, 'chance': 0.3}),
    ('go for the chair openly against {rival}, and win the committee over first', 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'steward of the land', 'mark': 'made an enemy', 'world': {'tribal': 'put yourself forward against {rival} of the other hearth, and win the elders over first', 'magic': "put your name forward against {rival}, and win the circle's elders over first"}, 'chance': 0.3}),
    ('tell the meeting plainly what the trust has let slip, and how to win it back', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'title': 'steward of the land', 'identity': True, 'world': {'tribal': 'tell the bands straight out at the fire what the grove has lost, and how to win it back', 'magic': 'tell the circle straight out what the grove has let slip, and how to fight for it'}, 'chance': 0.3}),
    ("stand as the one who knows the valley's land best, in all its seasons", 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'steward of the land', 'requires': 'good name in town', 'without': 'approval', 'lacking': 0.5, 'world': {'tribal': 'put yourself forward as the one who knows the grounds best, in every season', 'magic': 'put your name forward as the one who knows the grove best, in every season'}, 'chance': 0.3}),
    ('ask to work a year beside the old chair first, learning the books and the hedges', 'B.5 G.5', None, 0.5, '', {'v': 'achievement, security', 'self_control': '+', 'world': {'tribal': 'ask to walk the grounds a season beside the old keeper first', 'magic': "ask to serve a year at the old druid's side first"}, 'chance': 0.82}),
    ("take on the trust's yearly count instead, and leave the chair to others", 'U.5 G.5', None, 0.5, '', {'v': 'universalism, tradition', 'self_control': '-', 'world': {'tribal': 'take on the counting of the herds and the birds instead, and leave the grove to another', 'magic': "take on the grove's book of springs instead, and leave the chair to another"}, 'chance': 0.82}),
    ("refuse the chair in writing until the council hands over the low meadow's lease", 'U.5 R.5', None, 0.5, '', {'v': 'universalism, self-direction', 'mark': 'defied an authority', 'closed': 'approval: the chair refused on conditions; backfire: the members give the chair to someone else, and the council remembers the letter', 'world': {'tribal': 'refuse the grove until the elders give the wet meadow back to its keeping', 'magic': 'refuse the chair until the lord gives the low meadow back to the grove'}, 'chance': 0.82}),
    ("put the trust's deputy forward, and offer to stand at her side", 'W.5 B.5', None, 0.5, '', {'v': 'benevolence, security', 'binds': True, 'mark': 'made a friend', 'world': {'tribal': "speak at the fire for the old keeper's helper, and offer to stand beside her", 'magic': "speak to the circle for the old druid's helper, and offer to stand beside her"}, 'chance': 0.82}),
    ('ask the members at the yearly meeting who they want, and abide by it', 'W.5 R.5', None, 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'ask every hearth at the fire who they want to keep the grove', 'magic': 'ask every druid of the circle who they want, and abide by it'}, 'chance': 0.82}),
 ]},
{'name': 'the country comes to see the land',
 'stages': 'adult mature elder',
 'age': (35, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.02, 0.02),
 'drivers': 'era+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, nature, publiclife',
 'horizon': 'years',
 'roles': 'boss, colleague, mentor, friend',
 'requires': 'steward of the land',
 'tenure': (5.0, 100.0),
 'worlds': {'earth': 'the meadow, the wood and the river the trust has kept for years are suddenly famous, and '
                     'coaches of visitors come from across the country',
            'tribal': 'runners from bands far beyond the valley come to see the grove and the grounds the keeper has '
                      'kept, and to learn how',
            'magic': "druids and scholars from distant groves of the realm come to walk the grove's woods, and ask "
                     'its druid how it was done'},
 'timing': {'times': 'per steward of the land of five years or more a year: about 1 in 50 find people coming from '
                     'across the country to see the land the trust keeps, after a story, a programme or a rare bird '
                     '(estimate); a few hundred living people in a large country are known for a reserve, a wood or '
                     'a river they kept or brought back (estimate); about 3 lives in 100,000 become keepers of the '
                     'land (catalogue share; estimate)',
            'likelier': "years of the same valley's counts, a rare bird or flower back, a programme on the radio or "
                        'the television, a mentor who sends visitors on',
            'rarer': 'a trust with nothing to show yet, a fight with the council, a move away',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'It began with a paragraph in a big paper about the orchids on the low meadow, then a radio '
                       'piece, then a programme crew in waders in the river. Now coaches come on Sundays, the car '
                       "park is full by ten, schools write every week, and a minister's office has asked whether the "
                       "trust's way could be copied across the country. {boss}, the leader of the council, wants to "
                       'know what {N} means to do about it.'),
                      ('W',
                       'People come because the land is kept well, and it is kept well because the rules are kept. '
                       '{N} would like to keep it that way, however many come.'),
                      ('U',
                       'Twenty years of counts, and now there are enough eyes on the land to learn what really '
                       'worked. {N} has a question in mind that nobody has asked.'),
                      ('B',
                       "A name like this opens doors: the council's land committee, the national bodies, the money "
                       'that decides where land goes. {N} knows it will not last forever.'),
                      ('R',
                       'The coaches, the cameras, the children running down the boardwalk. {N} feels every bit of '
                       'it, and wants every one of them to love the place.'),
                      ('G',
                       '{N} never set out to be known. The meadow came back the way meadows do, one season on '
                       'another, and now people come from far away to stand in it.')],
            'tribal': [('',
                        'Runners have come from bands three valleys away to see the grove and the grounds {N} has '
                        'kept, and two elders have walked for days to sit at {Ns} fire and learn how the herds came '
                        'back. The traders carry the story from camp to camp, and {boss}, the eldest of the band, '
                        'asks what {N} means to do about it.')],
            'magic': [('',
                       "Druids and scholars from distant groves of the realm have come to walk the grove's woods, "
                       'and a royal clerk writes that the crown would have every grove kept the same way. {boss}, '
                       "the lord's steward, wants to know what {N}, druid of the grove, means to do.")]},
 'outcomes': (['By the end of the year {Ns} name is known far beyond the valley, and the visitors keep coming.',
               "Whatever {N} chose, the land is well kept and well loved, and the valley's own still come first."],
              ['The fuss dies down after a season, and the valley is quiet again.',
               'The talk moves on to another place, and {N} goes back to the ordinary work of the land, a little '
               'relieved.']),
 'options': [
    ('set fair rules for the visitors: paths, numbers and seasons, kept by all', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'title': 'keeper of the land', 'grants': 'known across the country', 'world': {'tribal': 'set the old rules for the visitors: where they may walk, how many, and in which moons', 'magic': 'set fair rules for the visitors: paths, numbers and seasons, kept by every grove'}, 'chance': 0.06}),
    ('publish the twenty years of counts, so any trust can do the same', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'keeper of the land', 'grants': 'known across the country', 'habit': True, 'world': {'tribal': "teach the twenty winters of counting to every band's keeper who comes", 'magic': "set down the grove's book of springs for every grove of the realm"}, 'chance': 0.06}),
    ('let the programme follow the trust for a year, with your name on the work', 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'keeper of the land', 'grants': 'known across the country', 'identity': True, 'world': {'tribal': "let the traders carry your name from camp to camp, with the grove's story", 'magic': "let the royal clerk set your name to the grove's way in the crown's book"}, 'chance': 0.06}),
    ('say yes to every school and every coach, and lead the walks yourself', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'title': 'keeper of the land', 'grants': 'known across the country', 'self_control': '-', 'world': {'tribal': 'say yes to every band that comes, and walk them round the grounds yourself', 'magic': 'say yes to every grove that sends, and walk them round the woods yourself'}, 'chance': 0.06}),
    ('keep the paths few and the visitors quiet, and the meadow first', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'title': 'keeper of the land', 'grants': 'known across the country', 'world': {'tribal': 'keep the paths few and the visitors quiet, and the grounds as they are', 'magic': 'keep the paths few and the visitors quiet, and the woods as they are'}, 'chance': 0.06}),
    ('open a café by the car park, and let its takings pay two wardens', 'B.5 R.5', None, 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'trade with the visiting bands for food and furs, to keep two young watchers at the grounds', 'magic': "let an innkeeper open by the grove's gate, and let the rent pay two wardens"}, 'chance': 0.8}),
    ('go out to the far groups yourself, and walk their own land with them', 'R.5 G.5', None, 0.5, '', {'v': 'benevolence, stimulation', 'body': 'light', 'world': {'tribal': 'walk out to the far bands yourself, and walk their own grounds with them', 'magic': 'ride out to the far groves yourself, and walk their own woods with them'}, 'chance': 0.8}),
    ('train two young wardens to take over one day, and teach them the whole work', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, benevolence', 'grants': "apprentice of one's own", 'binds': True, 'world': {'tribal': 'take two young ones of the band beside you, and teach them all you know of the grove', 'magic': 'take two young druids into the grove, and teach them all you know of its woods'}, 'chance': 0.8}),
    ('ask the council to make the meadow and the wood a reserve by law', 'W.5 G.5', None, 0.5, '', {'v': 'conformity, tradition', 'world': {'tribal': 'ask the gathering of the bands to swear the grove and the grounds be kept for good', 'magic': "ask the crown to make the grove's woods a reserve by royal charter"}, 'chance': 0.8}),
    ('write each town that asks a careful letter on keeping its own land', 'W.5 U.5', None, 0.5, '', {'v': 'universalism, benevolence', 'mark': 'helped someone in need', 'world': {'tribal': "send each far band's runner home with a careful word on keeping their own grounds", 'magic': 'write each grove that asks a careful letter on keeping its own woods'}, 'chance': 0.8}),
 ]},
{'name': 'what runs into the river at night',
 'stages': 'young_adult adult mature elder',
 'age': (20, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.015, 0.01),
 'drivers': 'trouble+.2 prosper+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, nature, friends',
 'horizon': 'week',
 'roles': 'friend, colleague, boss',
 'requires': 'steward of the land | keeper of the land | farmer | forester | park ranger | professional beekeeper',
 'worlds': {'earth': "walking the river at night, the steward finds a pipe from a friend's dairy running slurry into "
                     'the stream',
            'tribal': "walking the river at dusk, the keeper of the grove finds a friend's family soaking hides in "
                      "the pool above the band's drinking water",
            'magic': "walking the river at night, the druid finds a pipe from a friend's dye-works running into the "
                     'stream above the town'},
 'timing': {'times': 'per steward of the land, farmer, forester, ranger or beekeeper a year: about 1 in 70 find a '
                     "neighbour's farm or works letting something into a stream at night (estimate); slurry and "
                     'silage leaks are among the commonest causes of fish lost from small rivers on farmland (water '
                     "regulators' reports; estimate); about 1.5 lives in 100 are farmers (catalogue share)",
            'likelier': 'a wet winter and a full slurry store, an old pipe, a farm in debt, a dry summer with low '
                        'water',
            'rarer': 'a new store with a cover, a river warden who walks the bank, a farm with time to mend things',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'Walking the river bank at night after the first warm rain, {N} smells it before seeing it: a '
                       "pipe from the slurry store at {friend}'s dairy, half hidden in the nettles, running dark "
                       'into the stream. Below it the water is cloudy for a hundred yards, and the pool by the '
                       'bridge is empty of fish. {friend} has had a bad year with the milk price and has a letter '
                       'from the bank on the kitchen table. The river authority has a line that answers at any '
                       'hour.'),
                      ('W',
                       'The law on this is plain, and so is the duty of anyone who keeps land: report it, the same '
                       'night, whoever it is.'),
                      ('U',
                       'How much, for how long, and from where exactly? Without samples taken tonight, nobody will '
                       'ever know for sure.'),
                      ('B',
                       '{friend} owes the bank, and a fine would finish the farm. {N} could use that, or protect '
                       'it.'),
                      ('R',
                       'The pool by the bridge was full of trout last week. {N} wants to shout, and is frightened '
                       'for {friend} at the same time.'),
                      ('G',
                       'A stream mends once what fouls it stops: the water runs on, and the fish come back from '
                       'upstream within a few seasons. What matters is that the pipe stops tonight.')],
            'tribal': [('',
                        "Walking the river at dusk, {N}, the band's keeper of the grove, finds {friend}'s family "
                        "soaking a winter's hides in the still pool above the place where the band draws its water. "
                        'The water below runs cloudy and sour, and the little fish have gone from the shallows. '
                        "{friend}'s family had a hard winter, and the hides are their trade at the gathering.")],
            'magic': [('',
                       "Walking the river at night, {N}, druid of the grove, finds a pipe from {friend}'s dye-works "
                       'running into the stream above the town, the water below it stained and sour. {friend} owes '
                       "the moneylenders, and the lord's water bailiff would close the works for good.")]},
 'outcomes': (['The stream runs clear again within the month, and the matter is settled the way {N} chose.',
               'By the next spring the fish are back in the pool by the bridge, and {N} can look {friend} in the '
               'eye.'],
              ['The stream mends in its own time, but the matter goes badly: questions, a hearing and a cold silence '
               'along the valley.',
               'Word gets out the wrong way, and for a season {N} is the name the valley whispers about.']),
 'options': [
    ("ring the river authority's line that night, and report the pipe", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'world': {'tribal': 'tell the elders at the fire that night whose hides foul the pool', 'magic': "send word to the lord's water bailiff that night, and report the pipe"}, 'chance': 0.72}),
    ('take samples above and below the pipe, and write down every time', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'mark': 'learned a skill', 'world': {'tribal': 'look at and smell the water above and below the pool, and mark the places with stones', 'magic': 'draw water above and below the pipe in stoppered flasks, and note every hour'}, 'chance': 0.65}),
    ('tell {friend} there is one week to mend the pipe, or it gets reported', 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'made an enemy', 'world': {'tribal': "tell {friend}'s family they have till the new moon to move the hides, or the elders hear", 'magic': 'tell {friend} there is one week to mend the pipe, or the bailiff hears of it'}, 'chance': 0.73}),
    ('photograph the pipe by torchlight, and send the pictures to the paper', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'mark': 'took a wild risk', 'world': {'tribal': "run to the next band's fire that night, and tell everyone what fouls the river", 'magic': "take the tale to the town's broadsheet that night, before anyone can hide the pipe"}, 'chance': 0.66}),
    ('help {friend} block the pipe that night, and report it together in the morning', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'body': 'light', 'mark': 'helped someone in need', 'world': {'tribal': "help {friend}'s family carry the hides to a pit far from the river that night", 'magic': 'help {friend} block the pipe that night, and go to the bailiff together in the morning'}, 'chance': 0.7}),
    ('report it, and lay the samples before the town meeting', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': 'tell the elders, and lay the tale before the whole gathering of the bands', 'magic': "report it, and lay the flasks before the town's open meeting"}, 'chance': 0.75}),
    ('report it, and stand by {friend} through the inspection and the fine', 'W.34 B.33 R.33', None, 0.5, '', {'v': 'benevolence, security', 'binds': True, 'world': {'tribal': "tell the elders, and stand by {friend}'s family when they answer for it", 'magic': "report it, and stand by {friend} through the bailiff's hearing"}, 'chance': 0.69}),
    ("say nothing, for {friend}'s sake, and let the stream clear by itself", 'W.34 B.33 G.33', None, 0.5, '', {'v': 'security, benevolence', 'mark': 'hid a wrong', 'self_control': '-', 'takes_if_fails': 'good name in town', 'closed': "approval: a spill seen and kept quiet; backfire: the river authority traces the spill, learns the trust's chair walked that bank, and the town hears it", 'world': {'tribal': "say nothing at the fire, for {friend}'s sake, and let the pool clear by itself", 'magic': "say nothing, for {friend}'s sake, and let the brook clear by itself"}, 'chance': 0.6}),
    ('walk the river with {friend} every week until the fish come back to the pool', 'U.34 R.33 G.33', None, 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': "walk the river with {friend}'s family every moon until the little fish come back"}, 'chance': 0.78}),
    ('find a grant with {friend} for a covered store, and mend the farm for good', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "trade with the next band for a tanning place downriver, and help {friend}'s family dig the pit", 'magic': 'find a loan with {friend} for a covered vat, and mend the works for good'}, 'chance': 0.72}),
 ]},
{'name': 'the cranes nest on the old marsh',
 'stages': 'adult mature elder',
 'age': (35, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.01, 0.01),
 'drivers': 'era+.2 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, nature',
 'horizon': 'months',
 'roles': 'mentor, colleague, rival, boss',
 'requires': 'steward of the land | farmer | forester | park ranger | professional beekeeper',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': "a pair of cranes, gone from the country's marshes for generations, nests on the old marsh the "
                     "trust let flood, and the country's eyes turn to the valley",
            'tribal': 'a pair of great cranes, a bird the band knows only from the oldest songs, nests on the old '
                      'marsh below the grove, and the bands come to look',
            'magic': "a pair of great cranes, a bird the realm's old books call lost, nests on the grove's old "
                     "marsh, and the realm's eyes turn to the valley"},
 'timing': {'times': 'per steward of the land of two years or more, or farmer, forester, ranger or beekeeper of '
                     'eight, a year: about 1 in 100 see a rare bird or plant come back to land they keep (estimate); '
                     'cranes and other great marsh birds have come back to nest in a few places after centuries '
                     "away, and each return draws the country's eyes (estimate); about 3 lives in 100,000 become "
                     'keepers of the land (catalogue share)',
            'likelier': 'a marsh let flood years before, a dry spring elsewhere, a quiet valley, a year when the '
                        'papers want good news',
            'rarer': 'drained land, a busy path, a hard winter',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'Ten years ago {N} and a dozen volunteers blocked the ditches on the old marsh and let it '
                       'flood. This April, at dawn, {N} hears a sound like a trumpet from the reeds and, through the '
                       "glasses, sees two tall grey birds: a pair of cranes, gone from the country's marshes since "
                       "anyone's great-grandparents were young. By May there is a nest. Nobody else knows yet, and "
                       '{mentor} says that if word gets out, half the country will be in the lane by the weekend.'),
                      ('W',
                       "There are laws for a rare bird's nest, and a body that keeps the list. {N} has the form and "
                       'the number, and a careful habit of doing things properly.'),
                      ('U',
                       'Nobody in the country has watched cranes nest for generations. Every day of what happens on '
                       'that marsh is something no one alive has seen.'),
                      ('B',
                       "A bird like this could make the trust's name, and {Ns} with it: the money, the programme, "
                       'the minister on the boardwalk. {N} knows how quickly a chance like this goes.'),
                      ('R',
                       '{N} cannot stop grinning. Ten years of mud and arguments, and now this, at dawn, in the '
                       'reeds.'),
                      ('G',
                       'Water came back to the marsh, then the reeds, the frogs and the herons, and now the cranes. '
                       'It took ten years, the way such things take, and nothing could have hurried it.')],
            'tribal': [('',
                        "Ten winters ago {N}, the band's keeper of the grove, had the young ones dam the ditches on "
                        'the old marsh below the grove and let it flood. Now, at dawn, a call like a horn comes from '
                        'the reeds, and two tall grey birds stand in the water: great cranes, a bird the band knows '
                        'only from the oldest songs. Soon there is a nest, and nobody else has seen it yet.')],
            'magic': [('',
                       'Ten winters ago {N}, druid of the grove, let the old marsh flood again. Now, at dawn, a call '
                       "like a horn comes from the reeds: a pair of great cranes, a bird the realm's old books call "
                       'lost, and soon a nest. Nobody else knows, and {mentor} says that if word reaches the '
                       'capital, half the court will ride out to see.')]},
 'outcomes': (['By the autumn two young cranes fly over the marsh, and the valley is spoken of across the country.',
               'Whatever {N} chose, the chicks fly, and the marsh {N} let flood ten years ago is a place people '
               'speak of.'],
              ['The nest fails in a wet week early in the summer, as first nests often do, and the cranes leave.',
               'The fuss fades after a season, the cranes move on, and {N} goes back to the ordinary counts and the '
               'ordinary weeks.']),
 'options': [
    ("report the nest to the rare birds' body, and keep its rules to the letter", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'title': 'keeper of the land; steward of the land', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'world': {'tribal': 'tell the elders of every band at the gathering, and keep the old rules round the nest', 'magic': "report the nest to the realm's keepers of birds, and keep their rules to the letter"}, 'chance': 0.03}),
    ('watch the nest every day from a hide, and write all of it down', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'keeper of the land; steward of the land', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': 'watch the nest every dawn from the reeds, and remember every day of it', 'magic': "watch the nest every day from a hide, and set it all down in the grove's book"}, 'chance': 0.03}),
    ("tell the papers, and put the trust's name and your own on the cranes", 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'keeper of the land; steward of the land', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': 'tell the traders, and let your name travel with the cranes from camp to camp', 'magic': "tell the broadsheets, and put the grove's name and your own on the cranes"}, 'chance': 0.03}),
    ("camp at the marsh's edge until the chicks fly, and turn back anyone who comes", 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'door': True, 'title': 'keeper of the land; steward of the land', 'grants_if_fails': 'a long shot that missed', 'body': 'light', 'world': {'tribal': "sleep at the marsh's edge until the young fly, and turn back anyone who comes", 'magic': "camp at the marsh's edge until the young fly, and turn back any rider who comes"}, 'chance': 0.03}),
    ('keep the water high and the marsh quiet, and let the season run its course', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'title': 'keeper of the land; steward of the land', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'world': {'tribal': 'keep the dams high and the marsh quiet, and let the season run its course'}, 'chance': 0.03}),
    ('guard the nest with a rota of volunteers, day and night, by the rules', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': "guard the nest with a round of the band's young ones, day and night", 'magic': "guard the nest with a rota of the grove's novices, day and night"}, 'chance': 0.84}),
    ("write it up in the trust's newsletter, with the dates and the counts", 'W.34 U.33 B.33', None, 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': "tell it at the elders' fire, dawn by dawn, so it is remembered", 'magic': "write it up in the grove's book, with the dates and the counts"}, 'chance': 0.84}),
    ('build a hide at the far edge, and let the town see from a distance', 'W.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'build a screen of reeds at the far edge, and let the band look from a distance', 'magic': 'build a hide at the far edge, and let the townsfolk look from a distance'}, 'chance': 0.84}),
    ('shut the footpath past the marsh without waiting for the council', 'U.34 B.33 R.33', None, 0.5, '', {'v': 'self-direction, power', 'mark': 'defied an authority', 'closed': 'law: a public footpath shut without leave; backfire: the walkers report it, and the council makes the trust open the path and pay its costs', 'world': {'tribal': "block the hunters' trail past the marsh without waiting for the elders", 'magic': "chain the lord's path past the marsh without waiting for his leave"}, 'chance': 0.84}),
    ('keep the nest a secret, even from the committee, until the chicks fly', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'security, tradition', 'world': {'tribal': 'keep the nest a secret, even from the elders, until the young fly', 'magic': 'keep the nest a secret, even from the circle, until the young fly'}, 'chance': 0.84}),
 ]},
{'name': 'the circle meets at the old stones',
 'stages': 'adult mature elder',
 'age': (35, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'fortune+.2 community+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, nature',
 'horizon': 'months',
 'roles': 'elder, rival, mentor, colleague',
 'requires': 'steward of the land',
 'tenure': (3.0, 99.0),
 'worlds': {'magic': 'the druids of every grove gather at the old stones to name a new archdruid, and the spirits of '
                     'the deep grove offer an old pact'},
 'only': 'magic',
 'timing': {'times': 'per druid of the grove of three years or more in the magic world a year: about 1 in 60 is at '
                     'the old stones when the circle gathers to name a new archdruid (estimate); in many old tales '
                     'the keepers of the woods chose their chief at a gathering, and some said the spirits of the '
                     'deep woods had a voice in it (estimate); about 1 life in 1,000 is a druid of the grove '
                     '(catalogue share)',
            'likelier': 'an old archdruid failing, a druid known for the grove kept, a midsummer feast, a circle '
                        'already divided',
            'rarer': 'a young archdruid in good health, a grove far from the stones, a druid the circle mistrusts',
            'gap_years': (8.0, 20.0)},
 'scenes': {'magic': [('',
                       'At midsummer the druids of every grove in the realm walk to the old stones on the high moor, '
                       'where the archdruids have been named for longer than the books remember. {elder}, the old '
                       'archdruid, is too frail to keep the circle, and will step down at the next full moon. On the '
                       'first night a voice comes to {N} out of the deep grove beyond the stones: the old spirits of '
                       'the woods will win the circle for {N}, if {N} takes up the old pact and pays the price they '
                       'will name. {rival}, it is whispered, has heard the same voice.'),
                      ('W',
                       "The circle names its archdruid by its own law: a voice from every grove, and the eldest's "
                       'word last. {N} is uneasy at anything that comes round the side of it.'),
                      ('U',
                       "The old pact is written in the circle's oldest book, in a hand nobody has read for a hundred "
                       'years. {N} knows where the book is kept, and how to read the hand.'),
                      ('B',
                       'The druid of the high moors has more groves behind him than anyone, and no wish to be '
                       'archdruid himself. {N} knows what his word would be worth.'),
                      ('R',
                       'The stones hum at night, and the deep grove beyond them is dark and full of sound. {N} wants '
                       'to walk into it alone and see what is there.'),
                      ('G',
                       'Every grove of the realm has its own woods, its own springs and its own seasons. {N} would '
                       'like to have walked them all before asking any of them for a voice.')]},
 'outcomes': (['At the full moon the circle names its archdruid, the horns sound across the moor, and the groves '
               'settle into the new years.',
               'Whatever {N} chose, the midsummer gathering ends in peace, and the druids go home to their woods.'],
              ['The circle names {rival}, and nobody speaks of the voice in the deep grove again.',
               'The gathering splits over the naming, it drags on for a year, and {N} is left out of the end of '
               'it.']),
 'options': [
    ("wait for the circle's naming, and stand by its law of choosing", 'W1', None, 0.45, '', {'v': 'conformity, tradition', 'identity': True, 'title': 'keeper of the land', 'chance': 0.06}),
    ("take up the old pact from the circle's oldest book, at the price the spirits name", 'U1', None, 0.45, '', {'v': 'achievement, power', 'title': 'keeper of the land', 'mark': 'hid a wrong', 'closed': "approval: the spirits' pact, kept from the circle; backfire: the price comes due: seven winters keeping the deep grove's bounds by night, and the circle learns of the pact", 'self_control': '-', 'chance': 0.15}),
    ('count the groves one by one, and win the waverers before the naming', 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'keeper of the land', 'chance': 0.06}),
    ('walk alone into the deep grove at night, and ask the voice its name', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'title': 'keeper of the land', 'mark': 'took a wild risk', 'chance': 0.06}),
    ('go on keeping your own grove, and leave the naming to its season', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'keeper of the land', 'chance': 0.06}),
    ('tend the springs of the high moor with the young druids every night until the naming', 'R.5 G.5', None, 0.5, '', {'v': 'stimulation, tradition', 'habit': True, 'chance': 0.84}),
    ('find out who took up the old pact before, and name them before the circle', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, security', 'mark': 'made an enemy', 'chance': 0.66}),
    ("read the circle's oldest book through the night, and learn what the pact truly asks", 'U.5 R.5', None, 0.5, '', {'v': 'achievement, stimulation', 'mark': 'learned a skill', 'chance': 0.66}),
    ('speak for the druid of the high moors, and stand at his right hand', 'W.5 B.5', None, 0.5, '', {'v': 'security, benevolence', 'door': True, 'grants': 'friend in power', 'chance': 0.84}),
    ('walk to every grove of the realm first, and ask each for its voice', 'W.5 G.5', None, 0.5, '', {'v': 'tradition, conformity', 'chance': 0.66}),
 ]},
]

ECHOES = [
]

EVENTS_READ = []

MARKS = {}
