"""Chroma library politics: compiled by build.py from politics.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'leaflets to deliver before Saturday',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 90),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.006,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'community, public life',
 'horizon': 'week',
 'roles': "friend, elder, neighbour, the candidate's volunteer",
 'worlds': {'earth': "a candidate's team leaves a box of leaflets and a map of streets at the door",
            'tribal': "a speaker's kin ask for someone to walk to the far hearths and speak for him before the "
                      'gathering',
            'magic': "a faction's herald needs broadsheets carried through the lower wards before the lots are cast"},
 'timing': {'times': 'open to anyone: in a year with an election about 8 in 100 teenagers and adults are asked to '
                     'help a local campaign, fewer in other years; about 3 to 4 US adults in 100 do campaign work in '
                     'an election year (ANES), and about 8 lives in 100 volunteer at some point (catalogue share; '
                     "estimate) (packs, 2026-10-07, Emren's ask for parliament in every game: no birth draw, so the "
                     "door can come to every life that wants it, at a rate that keeps about today's numbers)",
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       "A volunteer from a local candidate's team is at the door with a box of four hundred leaflets "
                       'and a photocopied map, three streets marked in yellow. They are short of hands, and every '
                       'leaflet has to be through a letterbox before Saturday.'),
                      ('W',
                       'Every household ought to hear from every candidate before it votes; that is how an election '
                       'is meant to work. The three streets in yellow are the ones nobody has covered.'),
                      ('U',
                       '{N} reads the leaflet on the doorstep: three promises, a bar chart with no scale, and a '
                       'photograph of the candidate outside the library that is about to close.'),
                      ('B',
                       "The candidate's face is on half the lampposts this month. Whoever wins will remember who "
                       'walked the streets for them, and who did not.'),
                      ('R',
                       'Last week the candidate stopped at the bus stop and talked to {N} like a person rather than '
                       'a vote. An evening out on the streets, with a reason to be there, sounds good.'),
                      ('G',
                       'The streets in yellow are the ones {N} has walked since childhood, and half the names on the '
                       'doorbells are names {N} knows.')],
            'tribal': [('',
                        "The speaker's sister comes to {Ns} hearth at dusk. The gathering is a moon away, the far "
                        "hearths have not heard her brother's case, and someone with good legs and a straight tongue "
                        'must walk there and speak for him.')],
            'magic': [('',
                       'A herald in faction colours sets a bundle of broadsheets on {Ns} step, the ink still wet. '
                       'The lots are cast in five days, and nobody has carried them through the lower wards.')]},
 'outcomes': (['By Friday night every door on the map has had its leaflet, and the team thanks {N} by name.',
               'Two neighbours stop {N} in the street to ask about the candidate, and {N} finds there is plenty to '
               'say.'],
              ['Rain soaks half the box on the first evening, and the rest goes round late and creased.',
               'A dog, a broken gate and a man who shouts about all politicians: by the second street {N} has had '
               'enough.']),
 'options': [
    ('take the map, and get a leaflet through every door on it by Friday night', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'title': 'campaign volunteer', 'self_control': '+', 'world': {'tribal': 'walk to every far hearth before the gathering, and speak for him at each one', 'magic': 'carry a broadsheet to every door in the lower wards before the lots'}, 'chance': 0.75}),
    ("read every candidate's leaflet first, then join the party whose sums add up", 'U1', None, 0.45, '', {'identity': True, 'v': 'self-direction, universalism', 'title': 'party member', 'world': {'tribal': "hear every speaker's kin out, then bind yourself to the faction that makes most sense", 'magic': "read every faction's broadsheet, then swear to the one whose sums add up"}, 'chance': 0.75}),
    ('deliver your share, and ask the candidate for ten minutes over coffee afterwards', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'speak at the far hearths, then ask the speaker for a place by his fire', 'magic': 'carry your share, then ask the candidate for a word at the tavern after'}, 'chance': 0.55}),
    ('grab the box and do the whole estate tonight, with music in your ears', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'title': 'campaign volunteer', 'body': 'light', 'world': {'tribal': "set off for the far hearths tonight, singing the speaker's name along the path", 'magic': 'run the broadsheets round the lower wards tonight, whistling as you go'}, 'chance': 0.7}),
    ('deliver your own street only, where people know your face and will stop to ask', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'title': 'campaign volunteer', 'world': {'tribal': 'speak for him only at the hearths of your own kin', 'magic': 'carry the broadsheets down your own lane only, where every door knows your face'}, 'chance': 0.8}),
    ('say you will help once you have heard every candidate at the public meeting', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'say you will speak for nobody until every speaker has been heard at the fire', 'magic': 'say you will carry nothing until every faction has spoken in the square'}, 'chance': 0.7}),
    ('skip the streets that never vote, and bin their leaflets behind the shops', 'U1', 'B.7', 0.5, '', {'v': 'achievement', 'mark': 'hid a wrong', 'closed': 'approval: binning leaflets the team asked to be delivered; backfire: a neighbour finds them in the bin and tells the candidate', 'self_control': '-', 'world': {'tribal': 'skip the hearths that never stand behind anyone, and say you went', 'magic': 'skip the lanes that never cast a lot, and drop their broadsheets in the canal'}, 'chance': 0.75}),
    ('say no: Saturday is for your own plans, and nobody is paying for this', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'world': {'tribal': 'say no: you have your own hunting to do before the gathering', 'magic': 'say no: the herald can pay a runner'}, 'chance': 0.95}),
    ('talk a friend into coming, and make an evening of it with chips after', 'R1', 'G.7', 0.5, '', {'door': True, 'v': 'benevolence, hedonism', 'aims': 'campaign volunteer', 'world': {'tribal': 'talk a friend into walking along, and make a night of it at the far fire', 'magic': 'talk a friend into coming, and finish the round at the tavern'}, 'chance': 0.75}),
    ('deliver them with the old neighbour who has walked every election for forty years', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'mark': 'learned a skill', 'world': {'tribal': 'walk the hearths with the old woman who has carried words for every speaker since her youth', 'magic': "walk the lanes with the old herald who has carried every faction's broadsheets for forty years"}, 'chance': 0.75}),
 ]},
{'name': 'poll workers wanted for election day',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (14, 90),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.006,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community, work',
 'horizon': 'week',
 'roles': "neighbour, friend, the station's supervisor",
 'worlds': {'earth': 'the council needs clerks for the polling stations, a fee and a fifteen-hour day',
            'tribal': 'the elders need someone with a clear head to keep the counting stones at the gathering',
            'magic': "the Order asks for witnesses at the warded urns, under its seal, for a day's silver"},
 'timing': {'times': 'open to anyone: about 3 adults in 100 a year see a call for polling-station staff they could '
                     'answer; the US staffed about 774,000 poll workers in 2020 (Pew Research Center 2024), and '
                     'about 3 lives in 100 work a polling station at some point (catalogue share; estimate) (packs, '
                     "2026-10-07, Emren's ask for parliament in every game: no birth draw, so the door can come to "
                     "every life that wants it, at a rate that keeps about today's numbers)",
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A notice from the town hall goes up at the library and online: poll clerks wanted for '
                       'election day. Training on Tuesday evening, a fee for the day, and the doors open at seven in '
                       'the morning and close at ten at night.'),
                      ('W',
                       'Someone has to hand out the ballot papers, check the names and seal the boxes, or none of it '
                       'counts. The notice says the stations are short of staff again this year.'),
                      ('U',
                       'The training covers the register, spoilt papers, and what to do when a name is missing. {N} '
                       'would like to see how the whole machine fits together.'),
                      ('B',
                       'The fee is decent for one day of sitting at a table, and it is paid whoever wins. A day '
                       'inside the station also shows exactly how power gets counted.'),
                      ('R',
                       'Fifteen hours in a school hall, then the count: boxes tipped onto tables, candidates pacing, '
                       'the result read out after midnight. {N} wants to be in the room for that.'),
                      ('G',
                       'The polling station is the old village hall, where {Ns} grandparents voted and where the '
                       'same faces have sat behind the trestle table for as long as anyone remembers.')],
            'tribal': [('',
                        'The elders want a steady hand to keep the counting stones when the band casts its pebbles '
                        'at the gathering: one bowl for each speaker, and no stone dropped or added.')],
            'magic': [('',
                       'A clerk of the Order nails a notice to the guild hall door: witnesses wanted at the warded '
                       "urns from dawn to the evening bell, under the Order's seal, for a day's silver.")]},
 'outcomes': (['The day runs long but smoothly, and the boxes leave under seal on time.',
               "The station's supervisor thanks {N} at the end of the night, and asks {N} back for the next "
               'election.'],
              ['A queue out of the door at seven, a register with a page missing, and {N} goes home wrung out.',
               "The council's list is already full, and {N} is not called this time."]),
 'options': [
    ("sign up, go to Tuesday's training, and sign the declaration of secrecy", 'W1', None, 0.45, '', {'binds': True, 'v': 'conformity, universalism', 'title': 'polling-station volunteer', 'world': {'tribal': "take the elders' charge, and swear by the fire to keep the stones true", 'magic': "swear the Order's oath of the urns, and take its seal for the day"}, 'chance': 0.75}),
    ("ask for the clerks' handbook, and learn the rule for every odd case", 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'mark': 'learned a skill', 'title': 'polling-station volunteer', 'self_control': '+', 'world': {'tribal': 'ask the elders how every hard case at the last gathering was settled', 'magic': "borrow the Order's book of the urns, and learn every rule in it"}, 'chance': 0.6}),
    ('take it for the fee and the day off, and say so plainly', 'B1', None, 0.45, '', {'v': 'security, achievement', 'title': 'polling-station volunteer', 'world': {'tribal': 'keep the stones for the share of meat the elders promise', 'magic': "take the seal for the day's silver, and say so plainly"}, 'chance': 0.75}),
    ('put your name down for the count, the loud late part after the doors close', 'R1', None, 0.45, '', {'v': 'stimulation', 'title': 'polling-station volunteer', 'world': {'tribal': 'ask to count the pebbles at the end, when every eye is on the bowls', 'magic': 'ask to stand by the urns when they are broken open at night'}, 'chance': 0.65}),
    ('pass this year, and leave it to the people who have done it for years', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'pass, and leave the stones to the old hands who always keep them', 'magic': 'pass, and leave the urns to the witnesses who stand there every time'}, 'chance': 0.92}),
    ('ask the council how the count is checked, and only then put your name down', 'W1', 'U.7', 0.5, '', {'v': 'security, self-direction', 'aims': 'polling-station volunteer', 'world': {'tribal': 'ask the elders how the stones are checked before you agree', 'magic': "ask the Order's clerk how the urns are warded before you agree"}, 'chance': 0.8}),
    ('work out the fee by the hour, and decide your day is worth more than that', 'U1', 'B.7', 0.5, '', {'v': 'achievement, security', 'world': {'tribal': "weigh the meat against a day's hunting, and decide to hunt", 'magic': 'reckon the silver against a day at your craft, and keep to your craft'}, 'chance': 0.9}),
    ('sign up for the fee, then cry off on the morning for a better offer', 'B1', 'R.7', 0.5, '', {'v': 'hedonism', 'mark': 'broke your word', 'closed': "approval: dropping out on the day; backfire: the station opens short-handed, and the name comes off the council's list", 'self_control': '-', 'world': {'tribal': 'agree to keep the stones, then slip off to a feast at the next camp', 'magic': 'take the seal, then send word of a fever and go to the fair'}, 'chance': 0.75}),
    ('offer to drive the old neighbours to the polls instead', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'helped someone in need', 'world': {'tribal': 'offer to walk the old ones to the gathering, carrying what they cannot', 'magic': 'offer your cart to take the old folk of the lane to the urns'}, 'chance': 0.85}),
    ('work the station in the village hall where your family has always voted', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'title': 'polling-station volunteer', 'world': {'tribal': 'keep the stones at the fire where your mother kept them in her day', 'magic': "stand witness at the urns in your own ward's hall, as your family always has"}, 'chance': 0.55}),
 ]},
{'name': 'the ward needs a candidate',
 'stages': 'young_adult adult mature elder',
 'age': (18, 85),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.15,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community, public life',
 'horizon': 'months',
 'roles': 'colleague, friend, boss, an old councillor',
 'requires': 'party member | local party officer | campaign organiser | union rep',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'the council elections are in May and the ward has no candidate',
            'tribal': 'the band will choose who speaks at the council fire this winter, and no one from your hearths '
                      'has asked',
            'magic': 'a seat on the town council falls open, and the faction has no one to put up for it'},
 'timing': {'times': 'per party member, local party officer, campaign organiser or union rep a year, about 5 in 100 '
                     'young adults, 8 in 100 adults and 10 in 100 in midlife and old age are asked, or see the '
                     'chance, to stand; England has about 17,000 principal and 100,000 parish councillors (LGIU, '
                     'NALC), many parish seats go uncontested, and about 3 lives in 100 stand for a local seat at '
                     'some point, about half of those asked (catalogue share; estimate); activists, campaign '
                     "volunteers and residents' committee members come to the ballot through 'the fight that made "
                     "you want to stand' or by joining a party (packs, 2026-10-07, Emren's ask for parliament in "
                     'every game: no birth draw, so the door can come to every life that wants it, at a rate that '
                     "keeps about today's numbers)",
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The council elections are in May, nominations close in five weeks, and {Ns} ward has no '
                       'candidate. At the end of a meeting about something else, {colleague} says what the room has '
                       'been thinking: why not {N}?'),
                      ('W',
                       'If nobody stands, the seat goes to the other side unopposed, and the ward gets no choice at '
                       'all. To {N} that feels like a duty left lying on the table.'),
                      ('U',
                       '{N} looks up the last three results. The seat was lost by two hundred votes last time, on a '
                       'turnout of under a third.'),
                      ('B',
                       'A councillor sits on the planning committee, the licensing panel and the budget. {N} has '
                       'spent years asking such people for things.'),
                      ('R',
                       '{N} is sick of complaining about the potholes, the shut youth club and the bus that never '
                       'comes. Standing would mean saying it out loud, on every doorstep.'),
                      ('G',
                       '{N} knows the shopkeepers by name, the parents at the school gate, and the old men on the '
                       'bench outside the post office. Few people know the ward better.')],
            'tribal': [('',
                        'As the winter camp is set, the elders ask which voices will be heard at the council fire '
                        'this season. No one from {Ns} cluster of hearths has stepped forward, and the others are '
                        'looking at {N}.')],
            'magic': [('',
                       "A seat on the town council has fallen open with the old member's death, and the faction's "
                       'back room goes quiet when the warden asks who will stand. Several heads turn toward {N}.')]},
 'outcomes': (['The papers go in before the deadline, and by the first weekend there is a name on the ballot and '
               'people ready to work for it.',
               "The ward's question gets a proper answer, and {N} knows exactly where {N} stands in it."],
              ['The meeting drags on, nobody agrees, and the deadline passes with the ward still empty.',
               '{N} says something at the meeting that is repeated all over the ward by Friday, and not kindly.']),
 'options': [
    ("put your name forward, and go through the branch's selection by the rules", 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'council candidate', 'grants': 'party nomination', 'requires': 'party member', 'without': 'approval', 'lacking': 0.5, 'world': {'tribal': "ask the faction's elders for their blessing, by the old forms, to be heard at the fire", 'magic': "seek the faction's seal at a proper selection in the back room"}, 'chance': 0.75}),
    ("read the council's budget papers, and stand on a costed plan for the ward", 'U1', None, 0.45, '', {'binds': True, 'v': 'achievement, universalism', 'mark': 'learned a skill', 'title': 'council candidate', 'world': {'tribal': 'learn what every family needs this winter, and ask to be heard on that', 'magic': "study the town's ledgers, and stand on a reckoned plan for the ward"}, 'chance': 0.75}),
    ("stand, in return for the branch's promise of a winnable seat next time round", 'B1', None, 0.45, '', {'binds': True, 'v': 'power, achievement', 'title': 'council candidate', 'grants': 'party nomination', 'requires': 'party member', 'without': 'approval', 'lacking': 0.5, 'world': {'tribal': "agree to speak, in return for the elders' promise of the speaker's place next summer", 'magic': "stand, in return for the warden's promise of a safer seat next time"}, 'chance': 0.55}),
    ('stand as an independent, on the one thing in the ward you are angriest about', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation, universalism', 'title': 'council candidate', 'world': {'tribal': 'ask to be heard at the fire on your own, for the one wrong you cannot let rest', 'magic': "stand without any faction's seal, on the one wrong you cannot let rest"}, 'chance': 0.8}),
    ('stay off the ballot, and keep the branch going: the minutes, the lists, the tea', 'G1', None, 0.45, '', {'habit': True, 'v': 'tradition, benevolence', 'title': 'local party officer', 'requires': 'party member', 'without': 'impossible', 'self_control': '+', 'world': {'tribal': "keep the faction's fire and its memory of who owes whom, and let another speak", 'magic': "keep the faction's ward rolls and its back room, and let another stand"}, 'chance': 0.75}),
    ("agree to be a paper candidate, so the party's name is on every ballot", 'W1', 'B.7', 0.5, '', {'v': 'conformity', 'title': 'council candidate', 'grants': 'party nomination', 'requires': 'party member', 'without': 'approval', 'lacking': 0.5, 'world': {'tribal': 'agree to stand at the fire for the faction, knowing the band will choose another', 'magic': "lend your name to the faction's lot, so its colours are in every urn"}, 'chance': 0.85}),
    ('draft a one-page manifesto for the ward, and post it to see who bites', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'aims': 'council candidate', 'world': {'tribal': 'try your words out at a few hearths first, and see who nods', 'magic': 'pin a page of what the ward needs to the guild hall door, and see who reads it'}, 'chance': 0.7}),
    ('say no: the hours would come out of the family business', 'B1', 'G.7', 0.5, '', {'v': 'security', 'mark': 'turned down a chance', 'world': {'tribal': 'say no: the family needs your hands for the winter stores', 'magic': 'say no: the hours would come out of the family workshop'}, 'chance': 0.9}),
    ('nominate the friend who did most in the last fight, and promise to knock every door', 'R1', 'W.7', 0.5, '', {'binds': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'name your friend at the fire, and promise to walk every hearth for them', 'magic': "put your friend's name to the warden, and swear to carry their banner through every lane"}, 'chance': 0.7}),
    ('ask the old councillor who held the seat for twenty years what it really takes', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'tradition, self-direction', 'aims': 'local councillor', 'world': {'tribal': 'sit with the old voice of the fire, and ask what it really takes', 'magic': 'call on the old councillor, and ask what the seat really costs'}, 'chance': 0.75}),
 ]},
{'name': 'a paid job on the campaign',
 'stages': 'young_adult adult mature elder',
 'age': (18, 85),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.03,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, public life',
 'horizon': 'months',
 'roles': 'friend, boss, colleague, partner',
 'requires': 'campaign volunteer | local party officer | party member',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'a campaign needs paid staff for six weeks, and someone has passed your name on',
            'tribal': 'a speaker who wants to be chief needs someone to walk the valley for him all summer, fed at '
                      'his fire',
            'magic': "a faction's house hires clerks and runners for the season of the lots, with board and a wage"},
 'timing': {'times': 'per campaign volunteer, local party officer or party member of a year or more, a year, about 3 '
                     'in 100 young adults, 2 in 100 adults and 1 in 100 in midlife hear of paid campaign or office '
                     'work they could take, most of it in big election years; about 1 life in 500 works a paid '
                     'campaign and 1 in 330 as an adviser (catalogue shares; estimate) (packs, 2026-10-07: no birth '
                     'draw; party members too, so each color has a way into party work)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       '{friend} has passed {Ns} name to a campaign that is hiring: six weeks of paid work before '
                       'polling day, perhaps more after if the candidate wins. It wants an organiser, a caseworker '
                       'for the office, a researcher who can write, and someone for the data desk.'),
                      ('W',
                       'The campaign has a code of conduct, a spending limit and an agent who signs off every '
                       'leaflet. {N} likes that the job comes with rules.'),
                      ('U',
                       'The job list reads like a map of how campaigns really work: target lists, canvass returns, '
                       'polling, casework. {N} wants to see the inside of the machine.'),
                      ('B',
                       'The pay is modest, but the people who work a winning campaign tend to get the jobs that '
                       'follow it.'),
                      ('R',
                       'Six weeks of doorsteps, late nights and a result at the end of it. {N} can already feel the '
                       'noise of the count.'),
                      ('G',
                       'The campaign office is above the old bakery on the high street, and the work would be on '
                       'streets {N} has known for years, for people {N} has known as long.')],
            'tribal': [('',
                        'A speaker who means to be chief of the clans needs someone to walk the valley for him all '
                        'summer, from band to band, carrying his words and bringing back what is said. Whoever goes '
                        'will eat at his fire.')],
            'magic': [('',
                       "A faction's house posts a notice in its window: clerks, runners and a reckoner wanted for "
                       'the season of the lots, with board, a wage, and a letter of character at the end.')]},
 'outcomes': (['{N} starts on Monday, and by the second week the work has a rhythm and a purpose.',
               'The campaign asks {N} to stay on after polling day, whatever the result.'],
              ['The post goes to someone with more experience, and {N} hears nothing more.',
               'Two weeks in, the money dries up, and the campaign lets half its staff go.']),
 'options': [
    ("apply for the agent's post at the party's area office, with references from the branch", 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'party official', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': "offer to keep the speaker's count of gifts and debts between the bands, with a word from the faction's elders", 'magic': "apply for the clerk's post at the faction's house, with a letter from your ward's warden"}, 'chance': 0.04}),
    ('send the data desk the model you built of the last election', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'title': 'pollster', 'requires': 'data analyst', 'without': 'impossible', 'world': {'tribal': 'tell the speaker which bands leaned his way last summer, hearth by hearth, and offer to keep that count', 'magic': 'send the house your tally of the last lots, guild by guild'}, 'chance': 0.12}),
    ("take the adviser's job, and set your price before the first day", 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'political adviser', 'requires': 'graduate', 'without': 'impossible', 'world': {'tribal': 'offer to sit behind the speaker at the fire, for a share of every gift he gets', 'magic': "offer to serve as the candidate's secretary, and name your wage first"}, 'chance': 0.12}),
    ('say yes to whatever they have, and be on the doorsteps by Monday', 'R1', None, 0.45, '', {'v': 'stimulation', 'title': 'campaign organiser', 'world': {'tribal': 'say yes, and be on the valley path by first light', 'magic': 'say yes, and be running the wards by Monday'}, 'chance': 0.07}),
    ("take the caseworker's job on your own high street, and carry your neighbours' troubles", 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'title': 'constituency caseworker', 'world': {'tribal': 'offer to carry the troubles of your own hearths to the speaker, and see them settled', 'magic': "take the petitions post in your own ward, and carry your neighbours' petitions to the Crown"}, 'chance': 0.12}),
    ('ask for the contract, the hours and the pay in writing, then answer', 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'aims': 'campaign organiser', 'world': {'tribal': 'ask the speaker, before witnesses, what you will be fed and for how long', 'magic': "ask for the terms under the house's seal before you answer"}, 'chance': 0.75}),
    ('turn it down, but ask to sit in on the data desk on polling night', 'U1', 'R.7', 0.5, '', {'door': True, 'v': 'self-direction, stimulation', 'aims': 'pollster', 'world': {'tribal': "turn it down, but ask to sit with the band's ear when the pebbles are counted", 'magic': "turn it down, but ask to watch the house's reckoner on the night the urns open"}, 'chance': 0.85}),
    ('turn it down, and put your cousin forward, who needs the work more', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': "send your sister's son in your place, since he needs a big man's favour more", 'magic': "put your cousin forward for the runners' post instead"}, 'chance': 0.65}),
    ("take the caseworker's job, because the people who ring that office have nobody else", 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'title': 'constituency caseworker', 'world': {'tribal': "offer to carry the families' troubles to the speaker, because nobody else will", 'magic': "take the clerk of petitions' post, because the petitioners have nobody else"}, 'chance': 0.12}),
    ('keep the day job: the family needs your wage and your evenings more than this', 'G1', 'U.7', 0.5, '', {'v': 'tradition, benevolence', 'mark': 'turned down a chance', 'world': {'tribal': 'stay with the band: the hunt needs your spear more than the speaker needs your legs', 'magic': 'stay at your craft: the household needs the steady wage and you at the table'}, 'chance': 0.9}),
 ]},
{'name': 'polling day in the ward',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 2.0, 2.0, 2.0, 2.0),
 'drivers': 'unrest+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'week',
 'roles': 'friend, rival, colleague, partner',
 'requires': 'council candidate',
 'worlds': {'earth': 'polling day, from the first voter at seven to the count after ten',
            'tribal': 'the night the band speaks at the council fire and says who will be heard',
            'magic': "the day the town council's lots are cast in the warded urns"},
 'timing': {'times': 'per council candidate: once a candidacy, on the day itself; about 3 lives in 100 stand for a '
                     'local seat at some point (catalogue share), and about 1 candidate in 3 wins (estimate from '
                     'about three candidates for each principal seat in England)',
            'likelier': 'a contested ward, a candidacy that runs all the way to the vote',
            'rarer': 'a seat filled unopposed, a candidate who withdraws before the day',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       'The polls open at seven and close at ten. {N} has a clipboard of names, a flask of coffee '
                       'and {friend} waiting in the car, and by midnight the ward will have decided.'),
                      ('W',
                       'The rules say how close a candidate may stand to the polling station door. {N} has read them '
                       'twice, and stands exactly that far away, smiling at everyone who passes.'),
                      ('U',
                       'On one sheet {N} has the turnout from the last three elections: which streets decide it, and '
                       'at what hour they come out to vote.'),
                      ('B',
                       '{rival} has more leaflets and a bigger team. {N} knows which streets still have votes in '
                       'them, and means to collect every one.'),
                      ('R',
                       '{N} has barely slept and does not care. Every door today is another chance, and the whole '
                       'day feels like the night before a match.'),
                      ('G',
                       '{N} grew up three streets from the polling station. Today the neighbours decide whether to '
                       'send one of their own to the town hall.')],
            'tribal': [('',
                        'The fire is built high and the families gather in a ring. When the elders call, each will '
                        'stand behind the one they want heard, and {N} waits to see who stands.')],
            'magic': [('',
                       "The warded urns stand in the guild hall under the Order's seal, and the townsfolk queue to "
                       'drop their lots. {N} watches the line from across the square.')]},
 'outcomes': (['When the result is given, {N} has won, and the volunteers cheer until they are hoarse.',
               'The day goes {Ns} way, and by the next evening a queue of neighbours is waiting with problems to '
               'solve.'],
              ['The result goes to {rival}, by fewer votes than anyone expected.',
               '{N} comes second, close enough to hurt and far enough to be sure.']),
 'options': [
    ('stand at the polling station door all day, greeting voters as far as the rules allow', 'W1', None, 0.45, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'v': 'conformity, achievement', 'world': {'tribal': 'sit at the fire from first light, greeting each family as it comes', 'magic': 'stand by the warded urns all day, at the distance the seals allow'}, 'chance': 0.36}),
    ('watch the turnout hour by hour, and send the volunteers where the vote is soft', 'U1', None, 0.45, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'grants': 'a list of supporters', 'v': 'achievement', 'world': {'tribal': 'listen at the hearths all day, and send friends to the families still undecided', 'magic': 'tally the lots cast by noon, and send runners to the lanes still to vote'}, 'chance': 0.38}),
    ('fight every doubtful ballot at the count, and demand a recount if it is close', 'B1', None, 0.45, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'v': 'power, self-direction', 'world': {'tribal': 'challenge every family that stands, and demand they stand again if it is close', 'magic': 'challenge every doubtful lot, and demand a second count if it is close'}, 'chance': 0.37}),
    ('knock on doors in the rain until the very minute the polls close', 'R1', None, 0.45, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'aims': 'local councillor', 'body': 'light', 'habit': True, 'v': 'achievement, stimulation', 'self_control': '+', 'world': {'tribal': 'walk from hearth to hearth until the last family has stood', 'magic': 'knock through the wards until the urns are sealed at the curfew bell'}, 'chance': 0.38}),
    ('stay home with the family, and trust the years spent on these streets', 'G1', None, 0.45, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'aims': 'local councillor', 'v': 'tradition', 'world': {'tribal': 'stay at your own hearth, and trust the years spent among these families'}, 'chance': 0.35}),
    ('drive the housebound to vote, starting with the families who owe a favour', 'B.5 G.5', None, 0.5, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'v': 'power, benevolence', 'world': {'tribal': 'carry the old ones to the fire, starting with the families in your debt', 'magic': 'send carts for the old and the lame, starting with the families in your debt'}, 'chance': 0.4}),
    ('put out a last leaflet with a story about the rival that is not quite true', 'B.5 R.5', None, 0.5, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'mark': 'hid a wrong', 'closed': 'law: a false statement about a candidate; backfire: the rival goes to the police, and the result is challenged in court', 'v': 'power, stimulation', 'world': {'tribal': 'send a tale round the hearths about the rival that is not quite true', 'magic': 'pay a herald to cry a tale about the rival that is not quite true'}, 'chance': 0.39}),
    ('fill in the postal vote forms for the old neighbours who find them hard', 'U.5 G.5', None, 0.5, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'mark': 'hid a wrong', 'closed': "law: handling other people's ballots; backfire: an election petition, and the police at the door", 'v': 'benevolence, universalism', 'world': {'tribal': 'say for the old ones at the fire where they stand, without asking them', 'magic': 'cast the lots of the old and the lame for them, as they would surely wish'}, 'chance': 0.38}),
    ('thank every volunteer by name at the count, win or lose', 'W.5 R.5', None, 0.5, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'grants': 'a loyal campaign team', 'grants_if_fails': 'a loyal campaign team', 'mark': 'made a friend', 'v': 'benevolence', 'world': {'tribal': 'thank every friend who walked the hearths, whatever the fire decides', 'magic': 'thank every runner by name at the urns, whatever the lots say'}, 'chance': 0.35}),
    ('be your own counting agent, and check every bundle of ballots against the rules', 'W.5 U.5', None, 0.5, '', {'title': 'local councillor', 'requires': 'party nomination', 'without': 'approval', 'lacking': 0.35, 'habit': True, 'v': 'conformity, security', 'world': {'tribal': 'sit with the counting stones, and see every pebble fairly placed', 'magic': 'sit as witness at the urns, and check every lot against the roll'}, 'chance': 0.36}),
 ]},
{'name': 'a seat falls vacant',
 'stages': 'young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.045, 0.09, 0.075, 0.02),
 'drivers': 'era+.3 unrest+.2 fortune+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, rival, partner',
 'requires': 'local councillor | mayor | political adviser | party official | campaign organiser | union rep',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'the member for the seat stands down, and the selection is in six weeks',
            'tribal': "the band's speaker to the gathering has died, and the families must send another",
            'magic': 'a seat in the Assembly falls open, and the faction will choose its candidate at the new moon'},
 'timing': {'times': 'per local councillor, mayor, political adviser, party official, campaign organiser or union '
                     'rep of two years or more a year: about 4 or 5 in 100 young adults, 9 in 100 adults, 7 or 8 in '
                     '100 in midlife and 2 in 100 elders see a parliamentary selection they could enter (a seat '
                     'whose member stands down, or a place on a party list, in a small parliament where every party '
                     'selects); about 70 UK seats a year get a new member (House of Commons), and a selection for a '
                     'winnable seat is won about 1 time in 5 (estimate) (packs, 2026-10-07: half as often again, so '
                     'a councillor who keeps trying meets a selection two or three times in a council career; a '
                     "party member's own habits and earlier tries lift the odds)",
            'likelier': 'a member retiring or stepping down, new boundaries, a change of government on the way, '
                        'years of work for the party in the area',
            'rarer': 'a member who holds the seat for decades, a long queue of hopefuls, a life far from the party',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The member for the seat announces at the weekend that this term will be the last. By Monday '
                       '{Ns} phone will not stop: the selection is in six weeks, and everyone wants to know whether '
                       '{N} will go for it.'),
                      ('W',
                       'There is a process: the forms, the hustings for members, the panel. {N} prints the timetable '
                       'and reads the rules before saying a word to anyone.'),
                      ('U',
                       '{N} pulls up the last three results in the seat, the boundary map and the membership '
                       'numbers, and begins to see how it could be won.'),
                      ('B',
                       'A seat like this comes up once in a decade. {N} is already counting who on the panel owes a '
                       'favour, and whom {rival} has in pocket.'),
                      ('R',
                       '{Ns} heart is racing. This is the chance {N} has wanted for years, and it feels like now or '
                       'never.'),
                      ('G',
                       '{N} knows these towns and villages, every school and every closed factory. If anyone should '
                       'speak for them, it should be someone who never left.')],
            'tribal': [('',
                        "The band's speaker died in the spring, and the gathering is two moons away. At the fire the "
                        'families begin to say names, and one of them is {Ns}.')],
            'magic': [('',
                       "A herald brings word that the city's seat in the Assembly stands empty. The faction will "
                       'choose at the new moon, and the guild halls are already full of whispers.')]},
 'outcomes': (['The choice is made, and by the end of six weeks {Ns} next years have a clear shape.',
               'The members hear {N} out, and the room is warmer than {N} dared to hope.'],
              ['The panel picks someone else, and {N} hears the result in a corridor.',
               'The six weeks slip away in meetings, and the chance is gone before {N} is ready.']),
 'options': [
    ('apply to the selection panel, and keep to every rule of the contest', 'W1', None, 0.45, '', {'grants': 'parliamentary nomination', 'title': 'parliamentary candidate', 'requires': 'party member', 'without': 'approval', 'lacking': 0.1, 'grants_if_fails': 'a long shot that missed', 'aims': 'member of parliament', 'v': 'conformity, achievement', 'world': {'tribal': "ask the faction's elders for their blessing, in the proper order", 'magic': 'petition the faction for its seal, by every form of the contest'}, 'chance': 0.12}),
    ('win the selection with a written plan for the seat that no rival can match', 'U1', None, 0.45, '', {'grants': 'parliamentary nomination', 'title': 'parliamentary candidate', 'requires': 'party member', 'without': 'approval', 'lacking': 0.1, 'grants_if_fails': 'a long shot that missed', 'v': 'achievement', 'world': {'tribal': "win the elders over with a plan for the band's summer at the gathering", 'magic': "win the faction over with a written plan for the city's seat"}, 'chance': 0.12}),
    ('sign up a hundred new members before the cut-off, each of them your vote', 'B1', None, 0.45, '', {'grants': 'parliamentary nomination', 'title': 'parliamentary candidate', 'requires': 'party member', 'without': 'approval', 'lacking': 0.1, 'grants_if_fails': 'a long shot that missed', 'v': 'power', 'world': {'tribal': 'bring a dozen families into the faction before the choosing, each bound by a gift', 'magic': 'swear a dozen new members into the faction before the new moon, each in your debt'}, 'chance': 0.12}),
    ('ring every member in the seat, and tell each one why it has to be you', 'R1', None, 0.45, '', {'grants': 'parliamentary nomination', 'title': 'parliamentary candidate', 'requires': 'party member', 'without': 'approval', 'lacking': 0.1, 'grants_if_fails': 'a long shot that missed', 'act': 'ring every member in the seat, and tell each one why it has to be them', 'v': 'achievement, self-direction', 'world': {'tribal': 'go to every hearth of the faction, and say why it must be you', 'magic': "knock on every member's door, and say why it must be you"}, 'chance': 0.12}),
    ('stand as the local candidate, with the old families of the seat at your back', 'G1', None, 0.45, '', {'grants': 'parliamentary nomination', 'title': 'parliamentary candidate', 'requires': 'party member', 'without': 'approval', 'lacking': 0.1, 'grants_if_fails': 'a long shot that missed', 'v': 'tradition', 'world': {'tribal': "ask to be sent as one of the valley's own, with the old families at your back", 'magic': "stand as the city's own, with the old houses of the ward at your back"}, 'chance': 0.12}),
    ('back a friend from the branch for the seat, and run their campaign instead', 'R.5 G.5', None, 0.5, '', {'grants': 'allies in the party', 'mark': 'made a friend', 'v': 'benevolence', 'world': {'tribal': 'stand behind a friend from your hearths, and walk the camps for them', 'magic': 'back a friend from the faction, and run their campaign through the wards'}, 'chance': 0.7}),
    ('stand as an independent, on your own money and your own plan', 'U.5 B.5', None, 0.5, '', {'title': 'parliamentary candidate', 'door': True, 'binds': True, 'mark': 'took a wild risk', 'identity': True, 'v': 'self-direction, power', 'world': {'tribal': "ask to be sent without any faction's blessing, on your own name", 'magic': "stand for the seat with no faction's seal, on your own purse"}, 'requires': 'local councillor', 'without': 'impossible', 'chance': 0.12}),
    ('call a public meeting in the seat first, and let the turnout decide', 'U.5 R.5', None, 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'call the young hunters to a fire of your own, and see who comes', 'magic': 'hire a hall in the city, and see who comes to hear you'}, 'chance': 0.78}),
    ('help the panel fix the shortlist for the favourite, for a promise of the next seat', 'W.5 B.5', None, 0.5, '', {'grants': 'allies in the party', 'binds': True, 'mark': 'hid a wrong', 'closed': "approval: a fixed selection; backfire: a rejected hopeful complains to the party's ruling body, and the selection is run again", 'v': 'power', 'world': {'tribal': 'help the elders settle on the favourite before the families choose, for a promise of the next turn', 'magic': "help the faction's stewards fix the list for the favourite, for a promise of the next seat"}, 'chance': 0.64}),
    ('stay in the work you have, close to the streets and people you know', 'W.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, tradition', 'world': {'tribal': 'stay at the council fire, close to the hearths you know', 'magic': 'stay in the town council, close to the lanes and people you know'}, 'chance': 0.88}),
 ]},
{'name': 'a seat the party cannot win',
 'stages': 'young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.003, 0.0045, 0.0045, 0.0015),
 'drivers': 'era+.2 unrest+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'friend, colleague, rival, partner',
 'requires': 'party member | local party officer',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'an election is called, and the party needs a name on the ballot in a seat it has never won',
            'tribal': 'the gathering comes, and the faction must send a speaker for a valley whose bands have never '
                      'stood behind it',
            'magic': 'the Assembly is summoned, and the faction needs a name on the lots of a ward it has never won'},
 'timing': {'times': 'per party member or local party officer of two years or more a year: about 1 in 700 is asked '
                     'to stand for parliament in a seat the party cannot win (estimate: about 3,200 such candidacies '
                     'at each UK general election, every four to five years, against about a million party members, '
                     'and about half of those asked say yes); 4,515 candidates stood for 650 seats in 2024 (House of '
                     'Commons), about 7 a seat with 1 in 7 winning, so about 4 paper candidacies come for every '
                     'candidacy in a seat the party can win (estimate); about 8 lives in 10,000 ever stand as a '
                     'paper candidate (estimate)',
            'likelier': 'an election called early, a party that stands in every seat, years of loyal work in the '
                        'branch',
            'rarer': 'a branch with plenty of willing names, a party that stands only where it can win, a life far '
                     'from the branch',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       "The election is called on a Tuesday. By Thursday the party's agent is on the phone: the seat "
                       'has never been won and never will be, but the party wants its name on every ballot paper, '
                       'and would {N} stand?'),
                      ('W',
                       'The party has a rule that every seat should be fought. {N} believes in rules like that, even '
                       'when the result is known before the first leaflet goes out.'),
                      ('U',
                       '{N} looks up the last result: fourth place, a lost deposit and a majority of twenty '
                       'thousand. Four weeks of hustings would still teach a great deal.'),
                      ('B',
                       'Nobody wins a seat like this. But the people who choose the winnable seats remember who said '
                       'yes when the party needed a name.'),
                      ('R',
                       '{N} has never stood for anything bigger than the branch committee. A real campaign, even a '
                       'hopeless one, sets the pulse racing.'),
                      ('G',
                       'The few hundred people who vote for the party here every time deserve a name on the ballot '
                       'paper, and {N} is one of them.')],
            'tribal': [('',
                        'The gathering is a moon away, and the faction has no speaker for the far valley, where the '
                        'bands have never stood behind it. The elders look round the fire and find {N}.')],
            'magic': [('',
                       "A herald proclaims the Assembly, and the faction's steward needs a name for the lots of a "
                       "ward it has never won. A letter under the faction's seal comes to {Ns} door.")]},
 'outcomes': (['The weeks go the way {N} meant them to, and the branch remembers who helped.',
               'By polling day {N} has done what was promised, and the agent sends a note of thanks.'],
              ['The nomination papers come back with a signature missing, and the weeks go to waste.',
               'Nothing goes to plan, and the branch is a little colder toward {N} for months.']),
 'options': [
    ('put your name on the ballot so the party fights every seat, as its rules ask', 'W1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'conformity, tradition', 'world': {'tribal': 'let the elders send you for the far valley, so no band goes unspoken for', 'magic': "put your name on the faction's lots, so every ward of the realm is fought"}, 'chance': 0.12}),
    ('stand, and use the four weeks to learn how a real campaign is run', 'U1', None, 0.45, '', {'title': 'parliamentary candidate', 'mark': 'learned a skill', 'v': 'achievement', 'world': {'tribal': "go as the faction's speaker, and learn how the gathering is won", 'magic': 'stand, and learn in four weeks how a campaign for the Assembly is run'}, 'chance': 0.12}),
    ('stand where nobody can win, so the party owes you a winnable seat later', 'B1', None, 0.45, '', {'title': 'parliamentary candidate', 'binds': True, 'act': 'stand where nobody can win, so the party owes them a winnable seat later', 'v': 'power, achievement', 'world': {'tribal': 'speak for the far valley, so the elders owe you a better band next summer', 'magic': 'stand in the lost ward, so the faction owes you a winnable seat later'}, 'chance': 0.12}),
    ('fight the seat as if it could be won, at every hustings and every door', 'R1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'stimulation', 'world': {'tribal': 'speak as if the far valley could be won, at every hearth', 'magic': 'fight the ward as if it could be won, in every hall and at every door'}, 'chance': 0.12}),
    ('stand for the few hundred neighbours who vote for the party here every time', 'G1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'tradition, universalism', 'world': {'tribal': 'speak for the few families of the far valley who have always stood with the faction', 'magic': 'stand for the few houses of the ward that have always kept faith with the faction'}, 'chance': 0.12}),
    ('knock on doors in the marginal seat next door, for a friend who can win it', 'R.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence, stimulation', 'world': {'tribal': 'walk the hearths of the next valley for a friend the bands might stand behind', 'magic': 'knock on doors in the next ward, for a friend who can win it'}, 'chance': 0.9}),
    ('ask for a winnable seat next time in writing, and say no when none comes', 'U.5 B.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'power, achievement', 'world': {'tribal': 'ask the elders to promise a better band next summer, and say no when they will not', 'magic': 'ask the steward for a winnable seat under seal first, and say no when none is sealed'}, 'chance': 0.9}),
    ('go to the hustings anyway, and ask the hardest questions from the floor', 'U.5 R.5', None, 0.5, '', {'v': 'stimulation', 'world': {'tribal': 'go to the gathering anyway, and ask the hardest questions from among the bands'}, 'chance': 0.9}),
    ('find the agent another name, and ask for a post at the area office in return', 'W.5 B.5', None, 0.5, '', {'binds': True, 'v': 'power', 'title': 'party official', 'requires': 'local party officer', 'without': 'impossible', 'world': {'tribal': "find the elders another speaker for the far valley, and ask to keep the faction's count of gifts in return", 'magic': "find the steward another name for the lots, and ask for a clerk's desk at the faction's house in return"}, 'chance': 0.25}),
    ("say no to the ballot, and take on the branch's minutes and lists instead", 'W.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, tradition', 'title': 'local party officer', 'requires': 'party member', 'without': 'impossible', 'world': {'tribal': "say no to the far valley, and keep the faction's fire and its memory of who owes whom instead", 'magic': "say no to the lots, and keep the faction's ward rolls instead"}, 'chance': 0.85}),
 ]},
{'name': 'election night',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'adult mature',
 'per_year': (0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
 'drivers': 'unrest+.2 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'partner, friend, rival, colleague, boss',
 'requires': 'parliamentary candidate | parliamentary nomination',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'the count in a sports hall, and the returning officer at the microphone',
            'tribal': 'the great gathering, where the bands stand behind the speakers they choose',
            'magic': "the night the Assembly's urns are opened in the city square"},
 'timing': {'times': 'per parliamentary candidate of a year or more (most are chosen a year or two ahead): once a '
                     'candidacy; 4,515 candidates stood for 650 seats in 2024 (House of Commons), so about 1 in 7 '
                     'wins, and about 1 in 2 of those picked for a winnable seat; an independent wins far less '
                     'often; about 1 life in 1,000 stands for parliament (catalogue share; estimate)',
            'likelier': 'a candidacy that runs to polling day',
            'rarer': 'a candidate who withdraws, an election called off',
            'gap_years': (1.5, 3.0)},
 'scenes': {'earth': [('',
                       'The count is in a sports hall under strip lights. Ballot boxes come in from the villages one '
                       'by one, the volunteers watch the tables, and {partner} keeps checking the clock.'),
                      ('W',
                       '{N} knows the order of the night by heart: the verification, the count, the candidates '
                       "called to the stage, the returning officer's declaration. There is comfort in the ritual."),
                      ('U',
                       '{N} has the result from every box at the last election in a notebook, and is watching the '
                       'early bundles to see which way the town is leaning.'),
                      ('B',
                       "Win or lose, the cameras are here, and tomorrow's story starts tonight. {N} has a line ready "
                       'for each outcome.'),
                      ('R',
                       '{N} cannot sit still. Every bundle that lands on the table is a jolt, and the volunteers are '
                       'as wound up as {N} is.'),
                      ('G',
                       'Two years of village halls and market days come down to one long night. {N} thinks of the '
                       'places that are being counted, and the people in them.')],
            'tribal': [('',
                        'The bands of the valley stand in a wide ring on the summer meadow. When the elders call '
                        'each name, the people walk to stand behind the speaker they choose, and {N} watches the '
                        'lines grow.')],
            'magic': [('',
                       "In the city square the Order's mages break the seals on the Assembly's urns one by one. The "
                       'crowd hushes at every tally, and {N} stands with {Ns} runners by the steps.')]},
 'outcomes': (['The returning officer reads out the numbers, and {Ns} is the highest; the hall erupts.',
               '{N} wins by a margin nobody predicted, and the next morning begins a different life.'],
              ['The numbers go the other way, and {N} stands on the stage while someone else gives the speech.',
               '{N} loses by a few hundred votes, and drives home through the empty dawn.']),
 'options': [
    ("wait for the declaration with the other candidates, and shake the winner's hand", 'W1', None, 0.45, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'conformity', 'world': {'tribal': "wait in the ring for the elders to name the speaker, and clasp the winner's arm", 'magic': 'wait on the steps for the herald to read the lots, and bow to the winner'}, 'chance': 0.5}),
    ('read the early boxes, and write both speeches before the result is known', 'U1', None, 0.45, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'aims': 'member of parliament', 'v': 'achievement', 'world': {'tribal': 'watch which bands move first, and ready words for either end', 'magic': "read the first urns' tallies, and write both orations before the herald speaks"}, 'chance': 0.5}),
    ("work the room of reporters, so tomorrow's story is told your way either way", 'B1', None, 0.45, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'power', 'world': {'tribal': "sit with the singers, so tomorrow's songs are sung your way either way", 'magic': "work the broadsheet writers, so tomorrow's sheets tell it your way either way"}, 'chance': 0.5}),
    ('cheer every ballot box as it comes in, out on the floor with the volunteers', 'R1', None, 0.45, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, benevolence', 'world': {'tribal': 'shout for every band that comes to stand, among your young followers', 'magic': 'cheer every urn as it is opened, among the runners in the square'}, 'chance': 0.5}),
    ('spend the evening at home with the family, and go to the count at the end', 'G1', None, 0.45, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'tradition', 'world': {'tribal': 'sit at your own hearth with the family until the elders send word', 'magic': "stay home with the family until the herald's boy knocks"}, 'chance': 0.48}),
    ('have a quiet concession ready, and keep your strength for the next election', 'B.5 G.5', None, 0.5, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'power', 'world': {'tribal': 'have a quiet word ready for a loss, and keep strength for the next summer', 'magic': 'have a quiet concession ready, and keep strength for the next lots'}, 'chance': 0.5}),
    ('demand a recount on the spot if the margin is a handful of votes', 'B.5 R.5', None, 0.5, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'power, self-direction', 'world': {'tribal': 'demand the bands stand again if only a handful divide the lines', 'magic': 'demand a second count under a fresh seal if a handful of lots divide it'}, 'chance': 0.48}),
    ('track every bundle on the tables, and call the result before anyone else', 'U.5 R.5', None, 0.5, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, achievement', 'world': {'tribal': 'count every face in the lines, and call the end before the elders do', 'magic': 'track every tally as it is read, and call the result before the herald'}, 'chance': 0.5}),
    ('thank the volunteers one by one before the result is read', 'W.5 G.5', None, 0.5, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants': 'a loyal campaign team', 'grants_if_fails': 'a loyal campaign team; a long shot that missed', 'mark': 'made a friend', 'v': 'benevolence', 'world': {'tribal': 'thank each young follower by name before the elders speak', 'magic': 'thank each runner by name before the herald reads the lots'}, 'chance': 0.5}),
    ('check every rule of the count with the agents, so no result can be challenged', 'W.5 U.5', None, 0.5, '', {'title': 'member of parliament', 'requires': 'parliamentary nomination', 'without': 'approval', 'lacking': 0.04, 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'conformity, security', 'world': {'tribal': 'watch that every family stands where it chose, so no one can dispute the lines', 'magic': "check every seal on the urns with the Order's witnesses, so no result can be challenged"}, 'chance': 0.52}),
 ]},
{'name': 'the town needs a mayor',
 'stages': 'young_adult adult mature elder',
 'age': (21, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'rite': 'mature',
 'per_year': (0.0, 0.0, 0.01, 0.02, 0.02, 0.01),
 'drivers': 'era+.2 community+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'colleague, rival, friend, partner, elder',
 'requires': 'local councillor',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the mayor stands down and the council, or the town, must choose',
            'tribal': 'the head of the camp is too old to lead the moves, and the band looks for another',
            'magic': 'the burgomaster dies in office, and the town council must choose before the fair'},
 'timing': {'times': 'per local councillor of three years or more a year: about 1 in 100 young adults, 2 in 100 '
                     'adults and in midlife and 1 in 100 elders are put forward when the post falls vacant; about 1 '
                     'councillor in 10 becomes mayor or council leader this way and about 1 in 5 by every route (the '
                     "run from outside, the council's own choice in time), about 1 life in 500 (catalogue share; "
                     'estimate)',
            'likelier': 'a mayor retiring or resigning, years on the council, a small town where everyone knows the '
                        'councillors',
            'rarer': 'a mayor in the first year of a term, a big city with professional politicians, a newcomer to '
                     'the council',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       'The mayor announces at the end of a council meeting that the next one will be the last. '
                       'Before the room has emptied, two councillors have asked {N} whether {N} will stand.'),
                      ('W',
                       'The town has rules for this, and {N} knows them: nominations, a vote of the council, an '
                       'oath. Whoever is chosen must serve the whole town, not one side of it.'),
                      ('U',
                       "{N} has read the town's budget for six years running and knows where it leaks. A mayor could "
                       'fix it, if the mayor knew how.'),
                      ('B',
                       "The mayor's office has the chain, the budget and the say over every big contract. {N} has "
                       'watched it held badly for years.'),
                      ('R',
                       '{N} feels the old itch: to stand in the square and tell the town what it could be, and see '
                       'if it believes.'),
                      ('G',
                       "{N} thinks of the old mayors' photographs in the corridor, some of them people {N} knew as a "
                       'child. The town has always looked after its own.')],
            'tribal': [('',
                        'The old head of the camp can no longer walk the long moves. At the fire the families look '
                        'round at one another, and more than one look stops at {N}.')],
            'magic': [('',
                       "The burgomaster's chain lies on a cushion in the guild hall, and the fair is three weeks "
                       'away. The councillors meet in twos and threes in the tavern corners.')]},
 'outcomes': (['The council chooses, and the town has a mayor it can work with by the time the summer comes.',
               'The choice is made in the open, and {Ns} part in it earns respect on every side of the chamber.'],
              ['The vote goes the other way, and the new mayor remembers who stood against them.',
               'The contest turns sour, and {N} spends the autumn mending friendships on the council.']),
 'options': [
    ("stand in the council's vote on a record of fair dealing with every side", 'W1', None, 0.45, '', {'title': 'mayor', 'aims': 'mayor', 'v': 'conformity, achievement', 'world': {'tribal': 'offer to lead the camp, on a name for fair dealing with every family', 'magic': 'stand before the town council on a record of fair dealing with every guild'}, 'chance': 0.3}),
    ("write a costed plan for the town's first hundred days, and run on it", 'U1', None, 0.45, '', {'title': 'mayor', 'v': 'achievement', 'world': {'tribal': 'lay out where the band should winter and hunt for three years, and ask to lead it there', 'magic': "write out the town's accounts and a plan for the first year, and stand on it"}, 'chance': 0.3}),
    ("count the council's votes, and promise each waverer what they need", 'B1', None, 0.45, '', {'title': 'mayor', 'v': 'power', 'world': {'tribal': 'count which families are on your side, and promise each waverer a share', 'magic': "count the councillors' lots, and promise each waverer a guild contract"}, 'chance': 0.31}),
    ('make the case in the market square, loud and plain, and let the town decide', 'R1', None, 0.45, '', {'title': 'mayor', 'v': 'stimulation, self-direction', 'world': {'tribal': 'speak to the whole band at the fire, loud and plain, and let it decide'}, 'chance': 0.3}),
    ("stand as one of the town's own, from a family here for generations", 'G1', None, 0.45, '', {'title': 'mayor', 'aims': 'mayor', 'v': 'tradition', 'world': {'tribal': 'stand as one whose grandmothers camped in this valley', 'magic': "stand as one of the city's own, from a house that has lived inside its walls for generations"}, 'chance': 0.3}),
    ('back an old friend who wants it more, and help run the campaign', 'R.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence', 'world': {'tribal': 'stand behind an old friend who wants it more, and talk the families round'}, 'chance': 0.72}),
    ("trade your support for the deputy post, with the town's budget in its brief", 'U.5 B.5', None, 0.5, '', {'grants': 'allies in the party', 'v': 'power, achievement', 'world': {'tribal': 'give your support for the place beside the new head that keeps the stores', 'magic': "trade your support for the deputy's chair and the keeping of the town's purse"}, 'chance': 0.7}),
    ('stay a councillor, and keep the planning work you know best', 'U.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, self-direction', 'world': {'tribal': 'stay a voice at the fire, and keep the work of choosing the camps', 'magic': "stay on the council, and keep the work of the town's walls and lanes"}, 'chance': 0.8}),
    ('make your vote depend on an open contest, with rules agreed in advance', 'W.5 B.5', None, 0.5, '', {'v': 'conformity', 'world': {'tribal': 'ask that the families choose in the open, by the old custom', 'magic': 'make your lot depend on an open contest, with rules sealed in advance'}, 'chance': 0.74}),
    ('speak up for a younger councillor who would make a better mayor', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'universalism, benevolence', 'world': {'tribal': 'speak up for a younger one who would lead the moves better', 'magic': 'speak up for a younger councillor who would wear the chain better'}, 'chance': 0.7}),
 ]},
{'name': 'the phone call from the leader',
 'stages': 'adult mature elder',
 'age': (24, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'mature',
 'per_year': (0.0, 0.0, 0.0, 0.06, 0.06, 0.04),
 'drivers': 'era+.4 ties+.1 fortune+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, family',
 'horizon': 'years',
 'roles': 'boss, partner, colleague, rival',
 'requires': 'member of parliament',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "the leader's office calls on reshuffle day",
            'tribal': "the chief calls you to the chief's fire and asks you to keep the peace with the river clans",
            'magic': 'a sealed letter: the throne would have you as a councillor of the Crown'},
 'timing': {'times': 'per member of parliament of two years or more a year: about 6 in 100 adults and in midlife and '
                     '4 in 100 elders, many more in the year a new government forms; about 1 member in 3 ever holds '
                     'office (Institute for Government: 120 paid ministers at a time; estimate)',
            'likelier': 'a new government, a reshuffle, years in the seat, allies in the party, a name for knowing a '
                        'subject',
            'rarer': 'the party in opposition, a record of rebellion, a member new to the house',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The phone rings on reshuffle morning, and a calm voice asks {N} to hold for the leader. A '
                       'post in the government is on offer, and {boss} would like an answer before lunch.'),
                      ('W',
                       'Government is a duty before it is an honour. {N} thinks of the oath, the boxes of papers, '
                       'the lost weekends, and of what {boss} needs from the party.'),
                      ('U',
                       '{N} already knows which department {N} could run well, and which would mean a year of '
                       'learning on the job in public.'),
                      ('B',
                       'This is the call {N} has waited years for. The question now is not whether to take it, but '
                       'what to ask for.'),
                      ('R',
                       '{Ns} heart is hammering. A minister. {N} wants to shout it down the corridor, and makes an '
                       'effort to sound calm.'),
                      ('G',
                       '{N} looks out at the familiar street and thinks about what a ministry would take from the '
                       'family and from the constituency.')],
            'tribal': [('',
                        "A runner comes from the chief's fire: the chief would have {N} as one of the chief's "
                        'speakers, keeper of the peace with the river clans. The families watch {N} walk to the '
                        'fire.')],
            'magic': [('',
                       "A letter arrives under the Crown's seal: the throne would have {N} as one of its "
                       'councillors. The messenger waits at the door for an answer.')]},
 'outcomes': (['The answer is given, and by the evening {N} knows what the next years will hold.',
               '{boss} takes the answer well, and a year later {N} is sure it was the right one.'],
              ['The call ends coolly, and the post goes to someone else by the afternoon.',
               'The new life turns out harder than it looked, and the weekends at home disappear first.']),
 'options': [
    ('accept the post offered, whatever it is, because the government needs it filled', 'W1', None, 0.45, '', {'title': 'minister', 'v': 'conformity, benevolence', 'world': {'tribal': 'take the duty offered, whatever it is, because the clans need it kept', 'magic': 'accept the office offered, whatever it is, because the realm needs it kept'}, 'chance': 0.88}),
    ('ask for the department whose brief you already know inside out', 'U1', None, 0.45, '', {'title': 'minister', 'v': 'achievement, self-direction', 'world': {'tribal': "ask for the duty you already know best, the hunt's share or the trade", 'magic': 'ask for the office whose work you already know inside out'}, 'chance': 0.7}),
    ('accept, and start building a base in the cabinet from the first day', 'B1', None, 0.45, '', {'title': 'minister', 'aims': 'minister', 'v': 'power, achievement', 'world': {'tribal': "accept, and start gathering friends around the chief's fire from the first day", 'magic': "accept, and start building a following among the Crown's councillors at once"}, 'chance': 0.88}),
    ('say yes before the leader has finished the sentence', 'R1', None, 0.45, '', {'title': 'minister', 'binds': True, 'v': 'stimulation', 'world': {'tribal': 'say yes before the chief has finished speaking', 'magic': 'write yes on the back of the letter before the messenger has turned away'}, 'chance': 0.82}),
    ('accept, and promise the constituency it will still come first', 'G1', None, 0.45, '', {'title': 'minister', 'binds': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'accept, and promise your own hearths they will still come first', 'magic': 'accept, and promise your home city it will still come first'}, 'chance': 0.85}),
    ('hold out for a bigger department, and wait for the leader to blink', 'B.5 G.5', None, 0.5, '', {'title': 'minister', 'self_control': '+', 'v': 'power', 'world': {'tribal': 'hold out for a weightier duty, and wait for the chief to give way', 'magic': 'hold out for a greater office, and wait for the throne to give way'}, 'chance': 0.4}),
    ('turn it down, and stay on the back benches free to speak for the place', 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'identity': True, 'v': 'self-direction, tradition', 'world': {'tribal': 'turn it down, and stay free to speak for your own band at the gathering', 'magic': 'turn it down, and stay free to speak for your own city in the Assembly'}, 'chance': 0.95}),
    ('accept only if the leader keeps the promise the seat was won on', 'W.5 R.5', None, 0.5, '', {'title': 'minister', 'v': 'universalism, conformity', 'world': {'tribal': 'accept only if the chief keeps the promise the band was given', 'magic': 'accept only if the throne keeps the promise the seat was won on'}, 'chance': 0.55}),
    ('ask for a junior post first, to learn the work of government properly', 'W.5 U.5', None, 0.5, '', {'title': 'minister', 'self_control': '+', 'door': True, 'v': 'conformity, achievement', 'world': {'tribal': "ask for a small duty first, to learn the chief's ways properly", 'magic': 'ask for a lesser office first, to learn the work of the Crown properly'}, 'chance': 0.8}),
    ('accept, and spend the first week finding out where the power really lies', 'U.5 B.5', None, 0.5, '', {'title': 'minister', 'v': 'power, achievement', 'world': {'tribal': 'accept, and spend the first days finding out who the chief truly listens to', 'magic': 'accept, and spend the first week finding out who the throne truly listens to'}, 'chance': 0.88}),
 ]},
{'name': 'the leadership falls vacant',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.04, 0.02),
 'drivers': 'unrest+.3 prosper-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, rival, colleague, friend, partner',
 'requires': 'member of parliament | minister',
 'tenure': (4.0, 100.0),
 'worlds': {'earth': 'the leader resigns after a defeat, and nominations close on Friday',
            'tribal': 'the faction head has fallen in a hunt, and the families will choose who leads them to the '
                      'gathering',
            'magic': 'the head of the faction steps down, and the houses will choose a new one at midsummer'},
 'timing': {'times': 'per member of parliament or minister of four years or more a year: about 3 in 100 adults, 4 in '
                     '100 in midlife and 2 in 100 elders see the leadership of their party open; most parties change '
                     'leader every four to six years, and only those known across the country have a real chance '
                     '(estimate)',
            'likelier': 'a lost election, a leader worn out by years in office, a party in turmoil, hard times for '
                        'the country',
            'rarer': 'a leader newly elected, a party winning comfortably, a member new to the house',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The leader resigns at dawn after the defeat, and the party has until Friday to gather '
                       'nominations. {Ns} phone fills with messages: some urging {N} to run, some asking for '
                       'support.'),
                      ('W',
                       'A party without a leader is a ship without a captain. {N} reads the rules of the contest and '
                       'thinks hard about who could actually hold it together.'),
                      ('U',
                       '{N} has a clear account of why the party lost and what it would take to win again. The '
                       'question is whether anyone else can see it.'),
                      ('B',
                       'A vacancy at the top comes once in a long while. {N} starts counting nominations in the '
                       'head, and finds the sum closer than expected.'),
                      ('R',
                       '{N} is angry at the defeat and at the people who caused it. Part of {N} wants to stand up '
                       'and say so, whatever it costs.'),
                      ('G',
                       '{N} remembers the old leaders, the founding meetings, the members who kept faith through the '
                       'lean years. The party needs its roots more than a new face.')],
            'tribal': [('',
                        "The faction's head fell in the autumn hunt, and the families will choose who leads them to "
                        'the gathering. At the fire the young look at the old, and the old look at {N}.')],
            'magic': [('',
                       'The head of the faction steps down after a bitter season in the Assembly. The houses will '
                       'choose at midsummer, and messengers already ride between them.')]},
 'outcomes': (['The contest is settled, and {N} comes out of it with more standing than before.',
               'The party comes together behind its new leader faster than anyone feared, and {Ns} part in it is '
               'remembered.'],
              ['The contest turns bitter, and {N} ends it with fewer friends in the party.',
               "The numbers never come, and {N} watches the new leader's first speech from the back of the hall."]),
 'options': [
    ('stand on a promise to hold every wing of the party together, by its rules', 'W1', None, 0.45, '', {'title': 'party leader', 'requires': 'known across the country', 'without': 'approval', 'lacking': 0.2, 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, benevolence', 'world': {'tribal': 'offer to lead on a promise to keep every family of the faction together', 'magic': 'stand on a promise to hold every house of the faction together, by its charter'}, 'chance': 0.15}),
    ('stand on a long, detailed plan to win back the country', 'U1', None, 0.45, '', {'title': 'party leader', 'requires': 'known across the country', 'without': 'approval', 'lacking': 0.2, 'grants_if_fails': 'a long shot that missed', 'v': 'achievement', 'world': {'tribal': 'offer to lead on a plan to win back the clans at the next gathering', 'magic': 'stand on a long, detailed plan to win back the Assembly'}, 'chance': 0.15}),
    ('gather the nominations quietly, and declare only when the numbers are certain', 'B1', None, 0.45, '', {'title': 'party leader', 'requires': 'known across the country', 'without': 'approval', 'lacking': 0.2, 'grants_if_fails': 'a long shot that missed', 'aims': 'party leader', 'self_control': '+', 'v': 'power', 'world': {'tribal': "gather the families' promises quietly, and speak only when they are certain", 'magic': "gather the houses' seals quietly, and declare only when the count is certain"}, 'chance': 0.17}),
    ('declare on the steps of party headquarters the morning after the defeat', 'R1', None, 0.45, '', {'title': 'party leader', 'requires': 'known across the country', 'without': 'approval', 'lacking': 0.2, 'grants_if_fails': 'a long shot that missed', 'aims': 'party leader', 'v': 'stimulation, self-direction', 'world': {'tribal': 'stand up at the fire the morning after the fall, and say you will lead', 'magic': "declare yourself on the steps of the faction's house the day after the fall"}, 'chance': 0.15}),
    ('stand as the one who remembers what the party was founded for', 'G1', None, 0.45, '', {'title': 'party leader', 'requires': 'known across the country', 'without': 'approval', 'lacking': 0.2, 'grants_if_fails': 'a long shot that missed', 'identity': True, 'v': 'tradition', 'world': {'tribal': 'offer to lead as the one who remembers why the faction was first bound', 'magic': 'stand as the one who remembers what the faction was founded for'}, 'chance': 0.15}),
    ('back the front-runner early, for a big post in the new team', 'B.5 R.5', None, 0.5, '', {'title': 'minister', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "stand behind the likeliest early, for a duty at the new head's side", 'magic': "back the favourite early, for an office in the new head's gift"}, 'chance': 0.62}),
    ('stay out, and write the account of why the party lost that everyone reads', 'U.5 G.5', None, 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': 'stay out, and tell the old story of why the faction fell, so all can learn it', 'magic': "stay out, and write the treatise on the faction's fall that every house reads"}, 'chance': 0.7}),
    ('run anyway to make a point, and drag the contest toward what matters', 'U.5 R.5', None, 0.5, '', {'identity': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'stand anyway to make a point, and turn the talk at the fire to what matters', 'magic': 'stand anyway to make a point, and drag the houses toward what matters'}, 'chance': 0.72}),
    ("back the candidate the party's elders prefer, and collect on it later", 'W.5 B.5', None, 0.5, '', {'grants': 'allies in the party', 'v': 'power', 'world': {'tribal': "stand behind the one the faction's elders prefer, and remember the debt", 'magic': 'back the one the old houses prefer, and collect on it later'}, 'chance': 0.75}),
    ("stay out, and keep the party's warring wings talking to each other", 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': "stay out, and keep the faction's quarrelling families at one fire", 'magic': "stay out, and keep the faction's quarrelling houses at one table"}, 'chance': 0.65}),
 ]},
{'name': 'the country goes to the polls',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'mature elder',
 'per_year': (0.0, 0.0, 0.0, 0.25, 0.25, 0.25),
 'drivers': 'unrest+.3 prosper-.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'partner, colleague, rival, boss, friend',
 'requires': 'party leader',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': "a general election campaign, with the leader's face on every screen",
            'tribal': 'the great gathering will choose a chief of the clans for the hard years ahead',
            'magic': 'the throne will name its Chancellor from the faction that wins the Assembly'},
 'timing': {'times': 'per party leader of a year or more: about once in four years; the leader of one of the two '
                     "largest parties wins about 1 time in 2, a smaller party's almost never; about 1 life in two to "
                     'three million heads a government (catalogue share; estimate)',
            'likelier': "the end of a parliament's term, a government that has lost its majority, a crisis that "
                        'forces an early vote',
            'rarer': 'a parliament in its first years, a leader newly chosen between elections',
            'gap_years': (2.0, 4.0)},
 'scenes': {'earth': [('',
                       'The election is called for the first week of June. For six weeks {Ns} face will be on every '
                       'screen, every poster and every front page, and at the end of it the country will decide.'),
                      ('W',
                       '{N} thinks of the country as a whole, the people who will vote against as much as the ones '
                       'who will vote for. Whoever wins must govern for all of them.'),
                      ('U',
                       'The polls, the marginal seats, the turnout models: {N} has them all on the wall of the '
                       'campaign room, and knows the race is tighter than it looks on television.'),
                      ('B',
                       'Everything {N} has built comes down to this. {N} wants it, and has stopped pretending '
                       'otherwise.'),
                      ('R',
                       'The crowds are bigger than {N} expected, and louder. {N} feeds on them, and wants more.'),
                      ('G',
                       '{N} thinks of the places that never see a leader except at election time, and of an old '
                       'promise to remember them.')],
            'tribal': [('',
                        'The clans will choose a chief for the hard years ahead at the great gathering. {N} walks '
                        'from camp to camp all summer, and at every fire the families ask the same questions.')],
            'magic': [('',
                       'The throne will name its Chancellor from the faction that wins the Assembly. Heralds cry '
                       '{Ns} name in every square, and the guild halls hang out their banners.')]},
 'outcomes': (['The country votes, and by the next morning {N} is asked to form a government.',
               'The result goes {Ns} way, and five years begin with a car at the door and a crowd in the street.'],
              ['The country chooses the other side, and {N} concedes before dawn.',
               'The result is close and bitter, and it goes against {N} by a handful of seats.']),
 'options': [
    ('campaign on steady government, with promises small enough to keep', 'W1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'v': 'security, conformity', 'world': {'tribal': 'ask for the chiefship on steady leadership, with promises small enough to keep', 'magic': 'campaign on steady counsel to the throne, with promises small enough to keep'}, 'chance': 0.38}),
    ('target each voter with messages built from data bought without consent', 'U1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'aims': 'head of government', 'mark': 'hid a wrong', 'closed': 'law: misuse of personal data; backfire: the regulator fines the party, and the story runs all week', 'v': 'achievement, power', 'world': {'tribal': "learn each family's private fears from a paid gossip, and play on them", 'magic': "buy the guilds' private rolls, and send each voter a letter to suit"}, 'chance': 0.38}),
    ('spend the money only on the seats that decide it, and nowhere else', 'B1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'v': 'power', 'world': {'tribal': 'give the feasts only to the clans that will decide it, and to no others', 'magic': 'spend the coffer only on the seats that decide it, and nowhere else'}, 'chance': 0.38}),
    ('tour the whole country in six weeks, three rallies a day', 'R1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name; rousing a crowd', 'body': 'heavy', 'v': 'stimulation, achievement', 'world': {'tribal': 'walk to every camp in the valley in one summer, speaking at each fire', 'magic': 'ride to every city of the realm in six weeks, three orations a day'}, 'chance': 0.38}),
    ('campaign in the towns and villages the other side has forgotten', 'G1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'v': 'tradition, universalism', 'world': {'tribal': 'go to the small far camps the other speakers never visit', 'magic': 'go to the hamlets and the forest towns the other factions forget'}, 'chance': 0.38}),
    ('if the result is hung, offer the smaller parties what they need to govern', 'B.5 G.5', None, 0.5, '', {'title': 'head of government', 'grants': 'coalition building', 'v': 'power', 'world': {'tribal': 'if the clans are split, offer the small bands what they need to stand together', 'magic': 'if the Assembly is split, offer the small factions what they need to join the government'}, 'chance': 0.4}),
    ('refuse to concede a close result until the last seat is settled', 'R.5 G.5', None, 0.5, '', {'title': 'head of government', 'v': 'self-direction, tradition', 'world': {'tribal': 'refuse to give way while the last clans are still choosing', 'magic': "refuse to give way until the last city's urns are opened"}, 'chance': 0.38}),
    ('challenge the other leader to a live debate in every corner of the country', 'U.5 R.5', None, 0.5, '', {'title': 'head of government', 'grants': 'debating', 'v': 'stimulation, achievement', 'world': {'tribal': 'challenge the rival speaker to dispute at every fire of the valley', 'magic': "challenge the rival faction's head to dispute in every city square"}, 'chance': 0.38}),
    ('concede at once if the night is lost, and offer the winner a working truce', 'W.5 B.5', None, 0.5, '', {'title': 'head of government', 'v': 'conformity', 'world': {'tribal': 'give way at once if the clans choose another, and offer peace to the new chief', 'magic': 'give way at once if the lots fall the other way, and offer the new Chancellor a truce'}, 'chance': 0.36}),
    ('publish the full cost of every promise, and dare the others to match it', 'W.5 U.5', None, 0.5, '', {'title': 'head of government', 'grants': 'a name for straight talk', 'identity': True, 'v': 'universalism, achievement', 'world': {'tribal': 'tell the gathering exactly what every promise will cost the clans, and dare the rivals to do the same', 'magic': 'publish the cost of every promise in the broadsheets, and dare the others to match it'}, 'chance': 0.38}),
 ]},
{'name': 'leaving politics for another life',
 'stages': 'adult mature elder',
 'age': (24, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.05, 0.07, 0.1),
 'drivers': 'stress+.3 family+.2 trouble+.1 money-.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, family',
 'horizon': 'years',
 'roles': 'partner, child, colleague, friend, boss',
 'requires': 'member of parliament | political adviser | mayor | campaign organiser',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'an offer from a firm, a partner who wants their life back, a seat that feels like a cage',
            'tribal': 'the hunt, the family and the quiet of one camp call louder than the gathering',
            'magic': 'a merchant house offers you a fortune to plead its case instead'},
 'timing': {'times': 'per member of parliament, political adviser, mayor or campaign organiser of a year or more, a '
                     'year: about 5 in 100 adults, 7 in 100 in midlife and 10 in 100 elders weigh leaving for '
                     'another life; more UK members leave by standing down than by defeat in most elections '
                     '(estimate)',
            'likelier': 'long hours away from the family, a partner who wants their life back, a good offer from '
                        'outside, a bruising year, age',
            'rarer': 'a safe seat and a happy home, a post at the start of its term, a cause not yet won',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'A firm rings with an offer at three times the pay. {partner} says, gently, that the house '
                       'has got used to {N} not being in it. The next election is eighteen months away.'),
                      ('W',
                       '{N} made promises to the voters, the party and the team. Leaving early would break some of '
                       'them, and staying would break others.'),
                      ('U',
                       '{N} lists what the years in politics have taught, and where else that knowledge would be '
                       'worth more, or do more good.'),
                      ('B',
                       '{N} knows exactly what the contacts and the know-how are worth on the open market, and that '
                       'the price falls every year out of office.'),
                      ('R',
                       'Some mornings {N} still loves the fight. Other mornings {N} wants to walk out of the '
                       'building and never come back.'),
                      ('G',
                       '{N} thinks of the house, the garden, the friends not seen in years. The work has started to '
                       'feel like a cage with a good view.')],
            'tribal': [('',
                        "The summer gatherings take {N} far from the band's hearths for moons at a time. The hunt, "
                        'the family and the quiet of one camp call louder every year.')],
            'magic': [('',
                       'A merchant house offers {N} a fortune to plead its case at court instead. At home the '
                       'letters from the family grow shorter.')]},
 'outcomes': (['{N} makes the choice, and within a year the new life has its own rhythm and its own satisfactions.',
               'The people {N} worked with take the news well, and some of them become friends for life.'],
              ['The new start goes badly, and {N} misses the old work more than expected.',
               'Nothing comes of the plan, and {N} carries on in the old job, a little more tired.']),
 'options': [
    ('stay to the end of the term, because the voters were promised it', 'W1', None, 0.45, '', {'mark': 'kept your word', 'self_control': '+', 'v': 'conformity, benevolence', 'world': {'tribal': 'stay until the next gathering, because the band was promised it', 'magic': 'stay to the end of the term, because the city was promised it'}, 'chance': 0.8}),
    ('take a post at a research institute, writing the policy instead of voting on it', 'U1', None, 0.45, '', {'title': 'policy analyst', 'requires': 'drafting policy', 'without': 'impossible', 'v': 'achievement, self-direction', 'world': {'tribal': 'become the elder who remembers what was tried before, and teach it at the fire', 'magic': 'take a chair at the academy, writing on statecraft instead of practising it'}, 'chance': 0.78}),
    ("take the firm's offer to lobby the people you used to work beside", 'B1', None, 0.45, '', {'title': 'lobbyist', 'requires': 'a parliamentary pass', 'without': 'approval', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'become a go-between for the flint-traders, pleading at the fires you once sat at', 'magic': "take the merchant house's gold to plead its case to your old colleagues"}, 'chance': 0.8}),
    ('walk away at the next election, and do the wild thing always put off', 'R1', None, 0.45, '', {'drops': 'member of parliament; political adviser; mayor; campaign organiser', 'mark': 'took a wild risk', 'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'walk away before the next gathering, and go on the long journey always put off', 'magic': 'walk away at the end of the term, and take ship for the far lands'}, 'chance': 0.82}),
    ('step down to be at home with the family, for as long as they need', 'G1', None, 0.45, '', {'drops': 'member of parliament; political adviser; mayor; campaign organiser', 'mark': 'came home', 'identity': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'give up the gathering to stay at your own hearth, for as long as the family needs'}, 'chance': 0.85}),
    ('start a consultancy of your own, selling what you know of how power works', 'B.5 R.5', None, 0.5, '', {'title': 'founder of a firm', 'binds': True, 'mark': 'took a wild risk', 'door': True, 'v': 'power, self-direction', 'world': {'tribal': 'set up as a go-between of your own, trading what you know of the chiefs', 'magic': 'open a house of your own, selling counsel on how the court works'}, 'chance': 0.62}),
    ('write speeches for a leader with a better chance of the top job', 'U.5 B.5', None, 0.5, '', {'title': 'speechwriter', 'requires': 'writing speeches', 'without': 'impossible', 'v': 'achievement, power', 'world': {'tribal': 'shape the words of a speaker with a better chance of becoming chief', 'magic': "write orations for a lord with a better chance of the Chancellor's chain"}, 'chance': 0.78}),
    ("go back to teaching, and run the school's debating club on the side", 'U.5 G.5', None, 0.5, '', {'title': 'teacher', 'requires': 'professional registration', 'without': 'law', 'habit': True, 'v': 'benevolence, universalism', 'world': {'tribal': "go back to teaching the young, and let them argue at the children's fire", 'magic': 'go back to tutoring at the academy, and keep its disputation club'}, 'chance': 0.7}),
    ('stay on, and hand the hardest duties to a younger colleague you trained', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'self_control': '-', 'world': {'tribal': 'stay, and hand the long journeys to a younger one you have taught'}, 'chance': 0.68}),
    ('resign over a point of principle, and say so plainly in public', 'W.5 R.5', None, 0.5, '', {'drops': 'member of parliament; political adviser; mayor; campaign organiser', 'identity': True, 'mark': 'defied an authority', 'v': 'universalism, self-direction', 'world': {'tribal': 'give up your place over a point of principle, and say so at the fire', 'magic': 'resign over a point of principle, and say so plainly in the Assembly'}, 'chance': 0.8}),
 ]},
{'name': 'the hustings in the church hall',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.3 career.3',
 'per_year': (0.0, 0.0, 0.7, 0.7, 0.7, 0.7),
 'drivers': 'community+.2 unrest+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, work',
 'horizon': 'moment',
 'roles': 'rival, friend, colleague, partner',
 'requires': 'council candidate | parliamentary candidate',
 'worlds': {'earth': 'a church hall, a moderator and a hundred folding chairs',
            'tribal': 'the candidates speak in turn at the fire, and the elders ask the hard questions',
            'magic': 'the candidates dispute on the steps of the guild hall'},
 'timing': {'times': 'per candidate: once or twice a campaign for a parliamentary candidate, for about 1 council '
                     'candidate in 3 (estimate)',
            'likelier': "a parliamentary race, a close contest, a town with churches, schools and residents' groups "
                        'that organise debates',
            'rarer': 'a council seat nobody contests, a candidate who refuses every debate',
            'gap_years': (0.5, 2.0)},
 'scenes': {'earth': [('',
                       'A hundred folding chairs in the church hall, a moderator from the local paper, and every '
                       'candidate in a row behind a trestle table. The questions come from the floor, and some of '
                       'them are angry.'),
                      ('W',
                       '{N} has promised to answer every question honestly, and the first one from the floor is the '
                       'hardest of the campaign.'),
                      ('U',
                       "{N} knows the figures: the waiting lists, the bus routes, the council's budget. The question "
                       'is whether the room wants figures.'),
                      ('B',
                       '{rival} is ahead. A good evening here could change that, and {N} has come ready to make it '
                       'one.'),
                      ('R',
                       '{N} feels the room before a word is said: tired, cross, hungry for someone to mean '
                       'something. {N} wants to be that someone.'),
                      ('G',
                       '{N} knows half the faces by name: the woman from the bakery, the old man who ran the youth '
                       'club. They will judge {N} on whether {N} sounds like one of them.')],
            'tribal': [('',
                        'The candidates sit in turn by the fire, and the elders ask the hard questions: the hunt, '
                        'the feud with the hill people, the winter stores. The whole band listens.')],
            'magic': [('',
                       'The candidates dispute on the steps of the guild hall, and a crowd of journeymen and '
                       'merchants shouts questions from the square.')]},
 'outcomes': (['The hall warms to {N}, and people come up afterwards to shake hands and ask for a poster.',
               'The account of the evening that goes round the town gives {N} the best line of the night.'],
              ['A question {N} cannot answer goes round the town by morning.',
               'The evening slips away from {N}, and {rival} gets the applause.']),
 'options': [
    ('answer every question straight, even the ones that will cost votes', 'W1', None, 0.45, '', {'grants': 'a name for straight talk', 'identity': True, 'v': 'universalism, conformity', 'world': {'tribal': 'answer every elder straight, even when the answer will cost support', 'magic': 'answer every question from the square straight, even the costly ones'}, 'chance': 0.7}),
    ('prepare for a week, and know the figures better than anyone on the panel', 'U1', None, 0.45, '', {'grants': 'debating', 'self_control': '+', 'v': 'achievement', 'world': {'tribal': "spend days asking the old ones, and know the band's stores better than any rival", 'magic': "prepare for a week, and know the city's accounts better than anyone on the steps"}, 'chance': 0.78}),
    ("take apart the rival's strongest argument, and win the room with it", 'B1', None, 0.45, '', {'grants': 'debating', 'v': 'power, achievement', 'world': {'tribal': "take apart the rival's best argument at the fire, and win the band with it", 'magic': "take apart the rival's best argument on the steps, and win the square with it"}, 'chance': 0.64}),
    ('tear up the notes, and speak from the heart about why you are standing', 'R1', None, 0.45, '', {'grants': 'rousing a crowd', 'v': 'stimulation, self-direction', 'chance': 0.7}),
    ('talk only about the street, the school and the bus that stopped running', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': "talk only of the band's own hearths, the hunt and the river", 'magic': 'talk only of the ward, its well, its school and its broken bridge'}, 'chance': 0.7}),
    ('fill the front rows with your own supporters before the doors open', 'B.5 G.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'seat your own families nearest the fire before the elders arrive', 'magic': 'fill the front of the square with your own people before the dispute begins'}, 'chance': 0.82}),
    ('learn every vote the rival ever cast, and quote them back one by one', 'U.5 B.5', None, 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'learn every promise the rival ever broke, and name them one by one', 'magic': 'learn every lot the rival ever cast in council, and quote them back one by one'}, 'chance': 0.72}),
    ("land a clever cheap shot about the rival's private life that gets a laugh", 'U.5 R.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: a personal attack in a public debate; backfire: the hall turns cold, and the local paper leads with it', 'self_control': '-', 'v': 'stimulation, power', 'world': {'tribal': "mock the rival's family at the fire, cleverly, for a laugh", 'magic': "mock the rival's private affairs on the steps, cleverly, for a laugh"}, 'chance': 0.68}),
    ('invite the rival for tea afterwards, and agree to keep the campaign clean', 'W.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'binds': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'share food with the rival after the fire, and agree to keep the contest clean', 'magic': 'invite the rival to supper after the dispute, and agree to keep the contest clean'}, 'chance': 0.7}),
    ("defend a heckled rival's right to finish speaking, whatever the hall thinks", 'W.5 R.5', None, 0.5, '', {'v': 'universalism', 'chance': 0.82}),
 ]},
{'name': 'the money runs short three weeks out',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.6, 0.6, 0.6, 0.6),
 'drivers': 'money-.3 prosper-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'friend, colleague, partner, rival',
 'requires': 'council candidate | parliamentary candidate',
 'worlds': {'earth': 'the campaign account is nearly empty three weeks before polling day',
            'tribal': "the stores for the speaker's feast are nearly gone, and the gathering is a moon away",
            'magic': 'the coffer is empty, and the heralds want paying before the lots'},
 'timing': {'times': 'per candidate: about 1 campaign in 2 runs short in the last weeks (estimate)',
            'likelier': 'a small party or an independent run, a hard year for donors, a long campaign, a rival with '
                        'deep pockets',
            'rarer': 'a well-funded party seat, a candidate with savings, a short campaign',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       'Three weeks before polling day the treasurer rings: the account is nearly empty, the '
                       'printers want paying, and the last leaflet run has not been ordered. {rival} has posters on '
                       'every lamp post on the ring road.'),
                      ('W',
                       'There are rules on what a campaign may spend and take, and {N} knows them. Whatever happens '
                       'next will happen inside them.'),
                      ('U',
                       '{N} opens the spreadsheet and asks which money did the most good so far, and which did '
                       'nothing at all.'),
                      ('B',
                       'Money is a tool like any other, and {N} knows who has it. The only question is what they '
                       'will want in return.'),
                      ('R',
                       '{N} is not going to lose for the price of a leaflet run. If it comes to it, {N} will pay for '
                       'it personally.'),
                      ('G',
                       'The ward has always looked after its own. {N} thinks of the summer fair, the bake sale, the '
                       'neighbours who have offered to help.')],
            'tribal': [('',
                        "The stores for the speaker's feast are nearly gone, and the gathering is a moon away. {N} "
                        'looks at the empty drying racks and the few furs left to give.')],
            'magic': [('',
                       "The faction's coffer is empty, and the heralds want paying before the lots. {N} counts the "
                       'last coins on the table twice.')]},
 'outcomes': (['The money is found, the leaflets go out, and the campaign finishes strong.',
               'The last weeks run on what there is, and nobody on the doorstep can tell the difference.'],
              ['The money does not come, and the last leaflet run is cancelled.',
               'The gap is closed, but at a price that weighs on {N} long after polling day.']),
 'options': [
    ('cut the spending to what is left, and run the last weeks on volunteers', 'W1', None, 0.45, '', {'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'give only what is left, and ask friends to walk the camps for nothing', 'magic': 'spend only what is left, and run the last weeks on unpaid runners'}, 'chance': 0.8}),
    ('rebuild the budget line by line, and spend only where it counts most', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'count every fur and every basket, and give only where it counts most', 'magic': 'rebuild the accounts line by line, and spend only where it counts most'}, 'chance': 0.78}),
    ('ring every business owner who ever asked a favour, and ask for one back', 'B1', None, 0.45, '', {'grants': 'donors; fundraising', 'habit': True, 'v': 'power', 'world': {'tribal': 'go to every family who ever asked a favour, and ask for one back', 'magic': 'call on every merchant who ever asked a favour, and ask for one back'}, 'chance': 0.7}),
    ('put every penny of your own savings in, and borrow the rest from family', 'R1', None, 0.45, '', {'takes': 'savings', 'grants': 'a campaign war chest', 'mark': 'took a wild risk', 'binds': True, 'v': 'self-direction', 'world': {'tribal': 'give away everything your own hearth has stored, and borrow the rest from kin', 'magic': 'empty your own purse into the coffer, and borrow the rest from kin'}, 'chance': 0.72}),
    ('ask the neighbours for small sums, door by door and at the summer fair', 'G1', None, 0.45, '', {'grants': 'fundraising', 'habit': True, 'v': 'tradition, benevolence', 'self_control': '+', 'world': {'tribal': 'ask every hearth for a little, a basket here and a fur there', 'magic': 'ask the neighbours for coppers, door by door and at the fair'}, 'chance': 0.72}),
    ('take a large cash gift that breaks the spending rules, and keep it off the books', 'B.5 R.5', None, 0.5, '', {'grants': 'a campaign war chest', 'mark': 'hid a wrong', 'closed': 'law: undeclared money over the spending limit; backfire: the campaign is fined, and the result is overturned in court', 'self_control': '-', 'v': 'power', 'world': {'tribal': 'take a great gift from a clan that wants something back, and tell no one', 'magic': "take a purse of gold beyond what the Order's rules allow, and keep it off the rolls"}, 'chance': 0.74}),
    ('throw a fundraising party in the back garden, and invite the whole street', 'R.5 G.5', None, 0.5, '', {'grants': 'fundraising', 'v': 'hedonism, benevolence', 'world': {'tribal': 'throw a feast with what is left, and ask every guest to bring something', 'magic': 'throw a supper in the yard, and invite the whole lane to give what they can'}, 'chance': 0.62}),
    ('set up a small monthly giving scheme for the supporters on the list', 'U.5 G.5', None, 0.5, '', {'grants': 'a campaign war chest', 'binds': True, 'v': 'security, achievement', 'world': {'tribal': 'ask each family on your side to set aside a share of every hunt', 'magic': 'ask every name on the roll for a small sum each month'}, 'chance': 0.62}),
    ('apply to the party for an emergency grant, with every figure in order', 'W.5 B.5', None, 0.5, '', {'grants': 'a campaign war chest', 'v': 'security, conformity', 'world': {'tribal': "ask the faction's elders for a share of their stores, in the proper way", 'magic': "petition the faction's steward for its reserve, with every figure in order"}, 'chance': 0.56}),
    ('publish the accounts openly, and ask supporters to match every gift', 'W.5 U.5', None, 0.5, '', {'grants': 'donors', 'v': 'universalism, achievement', 'world': {'tribal': 'show the band exactly what is left, and ask each family to match what others give', 'magic': 'post the accounts on the hall door, and ask supporters to match every gift'}, 'chance': 0.56}),
 ]},
{'name': 'a file on your opponent',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.12, 0.12, 0.12, 0.12),
 'drivers': 'unrest+.2 stress+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'rival, friend, colleague, boss',
 'requires': 'council candidate | parliamentary candidate',
 'worlds': {'earth': 'an envelope of documents about the other candidate',
            'tribal': "a woman tells you the rival's speaker once broke a hunting oath",
            'magic': 'a sealed packet of letters that would ruin your rival, if they are real'},
 'timing': {'times': 'per candidate: about 1 campaign in 10 is offered damaging material on a rival, more in close '
                     'races (estimate)',
            'likelier': 'a close race, a bitter local feud, a rival with a business or a long public past, a hostile '
                        'press',
            'rarer': 'a safe seat, a small village contest, a rival with a short, quiet life',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'A brown envelope arrives at the campaign office with no name on it. Inside are copies of '
                       "letters about {rival}'s business: a debt, a court date, a name {N} does not recognise."),
                      ('W',
                       'There are proper ways to raise a concern about a candidate, and an anonymous envelope is not '
                       "one of them. {N} holds it at arm's length."),
                      ('U',
                       '{N} reads every page twice. Some of it might be true; some of it looks too neat. Who gains '
                       'from {N} having this?'),
                      ('B',
                       "{N} weighs the envelope in one hand. Used well, it could end {rival}'s campaign in a week."),
                      ('R', '{N} feels sick, then angry. This is not the fight {N} signed up for.'),
                      ('G',
                       "{N} has known {rival}'s family for years, on the same streets and at the same school gates. "
                       'Whatever is in here, they still live here.')],
            'tribal': [('',
                        'A woman comes to {Ns} hearth after dark and says that {rival} once broke a hunting oath, '
                        'and she can name who saw it.')],
            'magic': [('',
                       'A sealed packet of letters is left at {Ns} door. If they are real they would ruin {rival}; '
                       'if they are forged they would ruin whoever uses them.')]},
 'outcomes': (['The file is dealt with the way {N} chose, and the campaign goes on.',
               'Weeks later {N} is glad of the choice, whatever the result on polling day.'],
              ['The story gets out anyway, and everyone assumes it came from {N}.',
               'The documents turn out to be forged, and {N} is caught in the mess.']),
 'options': [
    ('hand the envelope unopened to the officer who runs the election', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'take the woman to the elders, and let them hear it', 'magic': "hand the packet unopened to the Order's warden of the lots"}, 'chance': 0.88}),
    ('check every document before deciding anything, and take nothing at face value', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'ask quietly who else saw the oath broken, before deciding anything', 'magic': 'have the seals and the hands checked before deciding anything'}, 'chance': 0.9}),
    ('keep the file in the safe, in case it is ever needed', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'remember the tale, and keep it for a day it might be needed', 'magic': 'lock the packet away, in case it is ever needed'}, 'chance': 0.86}),
    ('throw the envelope in the bin, and win clean or not at all', 'R1', None, 0.45, '', {'self_control': '+', 'v': 'stimulation, universalism', 'world': {'tribal': 'send the woman away, and win clean or not at all', 'magic': 'throw the packet in the fire, and win clean or not at all'}, 'chance': 0.93}),
    ("leave it in the drawer, since the town knows the rival's family well enough", 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': "leave it be, since the band knows the rival's family well enough", 'magic': "leave it in the drawer, since the ward knows the rival's house well enough"}, 'chance': 0.8}),
    ('leak it through an old friend on the local paper, with nothing to link it back', 'B.5 G.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: an anonymous smear; backfire: the leak is traced back, and the story becomes one about the leaker', 'self_control': '-', 'v': 'power, tradition', 'world': {'tribal': 'let the tale slip to an old friend among the singers, with nothing to link it back', 'magic': 'pass the letters to an old friend at a broadsheet, with nothing to link them back'}, 'chance': 0.76}),
    ('find out who sent it, and why, before doing anything else', 'U.5 G.5', None, 0.5, '', {'v': 'security, self-direction', 'world': {'tribal': 'find out who sent the woman, and why, before doing anything else'}, 'chance': 0.66}),
    ("raise it in the next debate, on the record and to the rival's face", 'U.5 R.5', None, 0.5, '', {'mark': 'made an enemy', 'closed': 'approval: using unchecked papers against a rival; backfire: the rival sues for defamation', 'v': 'stimulation, power', 'world': {'tribal': 'say it at the next fire, in front of the rival and the whole band', 'magic': "raise it at the next dispute on the steps, to the rival's face"}, 'chance': 0.6}),
    ("pass it to the party's lawyers, and let them decide whether it can be used", 'W.5 B.5', None, 0.5, '', {'v': 'conformity, security', 'world': {'tribal': "pass it to the faction's elders, and let them decide what to do with it", 'magic': "pass it to the faction's advocates, and let them decide whether it can be used"}, 'chance': 0.72}),
    ('warn the rival that someone is passing a file around', 'W.5 R.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'universalism, benevolence', 'world': {'tribal': 'warn the rival that a tale is going round the hearths', 'magic': 'warn the rival that someone is hawking letters about them'}, 'chance': 0.62}),
 ]},
{'name': 'a vote against your conscience',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.25, 0.25, 0.25, 0.25),
 'drivers': 'stress+.2 unrest+.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'boss, colleague, friend',
 'requires': 'member of parliament | local councillor',
 'worlds': {'earth': 'a division bell, and a bill you think is wrong',
            'tribal': 'the faction will stand behind a raid you think will bring a blood feud',
            'magic': 'the faction will vote to hand the old forest to the Order, and you know what lives there'},
 'timing': {'times': 'per member of parliament or local councillor a year: about 1 in 4; party discipline makes most '
                     'members vote against their own view now and then (estimate)',
            'likelier': "a large majority whose leaders push hard, a bill that touches the member's town, a member "
                        'with strong views of their own',
            'rarer': 'a free vote, an independent member, a quiet year in the chamber',
            'gap_years': (0.5, 2.0)},
 'scenes': {'earth': [('',
                       'The division bell rings at seven. The bill in front of the chamber is one {N} thinks is '
                       'wrong, and {boss} has been clear: the party votes for it, and the party remembers who does '
                       'not.'),
                      ('W',
                       "{N} stood on the party's platform and owes it loyalty. {N} also owes the people who voted, "
                       'and tonight the two pull apart.'),
                      ('U',
                       '{N} has read every clause. Two of them will not do what the minister says they will, and {N} '
                       'can show why.'),
                      ('B',
                       'A vote is worth something to the whips tonight, and {N} knows it. The only question is what '
                       'to ask for.'),
                      ('R',
                       '{N} feels it in the stomach: this is wrong. Voting for it would mean looking away from '
                       'something {N} believes.'),
                      ('G',
                       '{N} thinks of the town back home, the people the bill will touch, the faces at the Friday '
                       'surgery.')],
            'tribal': [('',
                        'The faction will stand behind a raid on the hill people at the gathering. {N} thinks it '
                        'will start a blood feud that lasts for generations.')],
            'magic': [('',
                       'The faction will vote to hand the old forest to the Order, and {N} knows what lives there, '
                       'and what the forest keeps out.')]},
 'outcomes': (['The vote is cast, and {N} can live with it, whatever the whips think.',
               'The whips grumble, but the bill changes, and {N} keeps a place in the party.'],
              ['The party takes the whip away, and {N} sits alone for a season.',
               'The vote is cast, and {N} lies awake that night knowing it was the wrong one.']),
 'options': [
    ('vote with the party, and tell the whips which colleagues plan to rebel', 'W1', None, 0.45, '', {'closed': 'approval: informing on colleagues; backfire: the rebels find out who told', 'v': 'conformity', 'world': {'tribal': 'stand with the faction, and tell its head which speakers mean to break away', 'magic': 'vote with the faction, and tell its warden which members mean to break away'}, 'chance': 0.8}),
    ('write out the case against the clause, and vote by the evidence', 'U1', None, 0.45, '', {'takes_if_fails': 'the party whip', 'identity': True, 'v': 'self-direction, universalism', 'world': {'tribal': 'set out at the fire why the raid will fail, and stand by what the old feuds teach', 'magic': 'write out the case against the decree, and cast your lot by the evidence'}, 'chance': 0.76}),
    ('vote with the party, and make sure the whips know a favour is owed', 'B1', None, 0.45, '', {'mark': 'gave in to pressure', 'v': 'power', 'world': {'tribal': 'stand with the faction, and make sure its head knows a favour is owed', 'magic': 'vote with the faction, and make sure its warden knows a favour is owed'}, 'chance': 0.84}),
    ('vote against it, and say plainly why on the floor of the chamber', 'R1', None, 0.45, '', {'takes_if_fails': 'the party whip', 'mark': 'defied an authority', 'identity': True, 'v': 'stimulation, universalism', 'world': {'tribal': 'stand apart from the faction, and say plainly at the gathering why', 'magic': 'cast your lot against it, and say plainly why in the Assembly'}, 'chance': 0.74}),
    ('stay away from the vote, and spend the evening back home', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': "stay away from the gathering's choosing, and sit at your own hearth", 'magic': 'stay away from the Assembly that day, and spend it at home'}, 'chance': 0.72}),
    ('rally a dozen rebels, and threaten to sink the bill unless it changes', 'B.5 R.5', None, 0.5, '', {'grants': 'counting the votes', 'takes_if_fails': 'the party whip', 'mark': 'defied an authority', 'v': 'power, self-direction', 'world': {'tribal': 'rally a dozen speakers, and threaten to break the faction unless the raid is dropped', 'magic': 'rally a dozen members, and threaten to sink the decree unless it changes'}, 'chance': 0.5}),
    ('hold a public meeting back home, and vote the way the meeting decides', 'R.5 G.5', None, 0.5, '', {'takes_if_fails': 'the party whip', 'v': 'universalism, tradition', 'world': {'tribal': 'ask your own band at the fire, and stand the way it decides', 'magic': 'call a meeting in the ward, and cast your lot the way it decides'}, 'chance': 0.72}),
    ('table an amendment, and trade your vote for support for it', 'U.5 B.5', None, 0.5, '', {'grants': 'counting the votes', 'binds': True, 'v': 'achievement, power', 'world': {'tribal': 'offer a change to the plan, and trade your support for it', 'magic': 'table an amendment to the decree, and trade your lot for support'}, 'chance': 0.56}),
    ('vote with the party this once, and tell the whip it is the last time', 'W.5 G.5', None, 0.5, '', {'mark': 'gave in to pressure', 'v': 'conformity, tradition', 'self_control': '-', 'world': {'tribal': 'stand with the faction this once, and tell its head it is the last time', 'magic': 'vote with the faction this once, and tell its warden it is the last time'}, 'chance': 0.68}),
    ('ask the minister for a written promise on the clause, and vote on that', 'W.5 U.5', None, 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': "ask the faction's head for a sworn word on the raid, and stand by it", 'magic': 'ask the councillor of the Crown for a sealed promise on the decree, and vote on that'}, 'chance': 0.66}),
 ]},
{'name': 'a deal to get it through',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.1, 0.1, 0.1, 0.1),
 'drivers': 'unrest+.2 era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, rival, boss, friend',
 'requires': 'member of parliament | local councillor | mayor | minister',
 'worlds': {'earth': 'a hung chamber and a bill with your name on it',
            'tribal': 'the river clans will stand with the band at the gathering if it shares the salmon pools',
            'magic': 'the Order of the Tower will lend its votes if the decree exempts its lands'},
 'timing': {'times': 'per member of parliament, local councillor, mayor or minister a year: about 1 in 4 where no '
                     'party holds a majority, about 1 in 20 where one does, about 1 in 10 taken together (estimate)',
            'likelier': 'a hung chamber, a coalition government, a council with no overall control, a bill the '
                        'member has carried for years',
            'rarer': 'a large majority, a member with no bill of their own, a quiet session',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{Ns} bill is three votes short. The small group in the corner of the chamber has the votes, '
                       'and its leader has named a price: an exemption that would gut a quarter of the bill.'),
                      ('W',
                       'A deal is a promise, and a promise has to be kept by both sides. {N} wants to know exactly '
                       'what is being agreed before agreeing to anything.'),
                      ('U',
                       '{N} has drafted this bill for two years. Somewhere in the text there must be a version both '
                       'sides can live with.'),
                      ('B',
                       'Three votes. {N} counts who in that group wants what, and what each of them could be given '
                       'without giving away the bill.'),
                      ('R', '{N} is furious at the price, and half wants to march across the chamber and say so.'),
                      ('G',
                       'Good laws take root slowly. {N} wonders whether forcing this one now would do more harm than '
                       'letting it wait for a better season.')],
            'tribal': [('',
                        'The river clans will stand with the band at the gathering if the band shares the salmon '
                        "pools. Without them the band's choice will fail.")],
            'magic': [('',
                       'The Order of the Tower will lend its votes if the decree exempts its lands. Without the '
                       'Tower, the decree dies in the Assembly.')]},
 'outcomes': (['The bill passes, changed but alive, and {N} has a deal both sides can stand behind.',
               "The vote is won, and the partner group's leader shakes {Ns} hand in the corridor afterwards."],
              ['The deal falls apart on the morning of the vote, and the bill fails by three.',
               'The price turns out higher than anyone said, and {N} spends a year paying it.']),
 'options': [
    ("pay the partner's price in full, and keep every word of the deal", 'W1', None, 0.45, '', {'grants': 'coalition building', 'mark': 'kept your word', 'binds': True, 'v': 'conformity, security', 'world': {'tribal': 'give the river clans their share of the pools, and keep every word of it', 'magic': 'grant the Tower its exemption, and keep every word of the bargain'}, 'chance': 0.78}),
    ('split the bill, and pass now the half that everyone can agree on', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'split the plan, and agree now only the part every clan accepts', 'magic': 'split the decree, and pass now the half every faction accepts'}, 'chance': 0.72}),
    ('win one member of the partner group over with a committee chair', 'B1', None, 0.45, '', {'grants': 'counting the votes', 'v': 'power', 'world': {'tribal': "win over one speaker of the river clans with a place at the chief's fire", 'magic': "win one of the Tower's members over with a seat on a council of the Crown"}, 'chance': 0.6}),
    ("take the partner group's leader out for a long dinner, and settle it as friends", 'R1', None, 0.45, '', {'mark': 'made a friend', 'v': 'benevolence, hedonism', 'world': {'tribal': "share a long meal with the river clans' speaker, and settle it as friends", 'magic': "take the Tower's spokesman to a long supper, and settle it as friends"}, 'chance': 0.72}),
    ('let the bill wait a year, until the chamber is ready for it', 'G1', None, 0.45, '', {'mark': 'turned down a chance', 'self_control': '+', 'v': 'tradition', 'world': {'tribal': 'let the plan wait a year, until the clans are ready for it', 'magic': 'let the decree wait a year, until the Assembly is ready for it'}, 'chance': 0.56}),
    ("rewrite the bill overnight so the partner's worry is answered in the text", 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'a reform with your name on it', 'v': 'achievement, universalism', 'world': {'tribal': "reshape the plan overnight so the river clans' fear is answered in it", 'magic': "redraft the decree overnight so the Tower's worry is answered in its text"}, 'chance': 0.14}),
    ('build a group across the parties around the bill, member by member', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'friends across the aisle; coalition building', 'door': True, 'v': 'universalism, benevolence', 'world': {'tribal': 'build a circle of speakers from every clan around the plan, one by one', 'magic': 'build a circle of members from every faction around the decree, one by one'}, 'chance': 0.66}),
    ('go to the other side of the chamber, and do the deal with them instead', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'friends across the aisle', 'v': 'power, achievement', 'world': {'tribal': 'go to the rival faction, and strike the bargain with them instead', 'magic': 'go to the rival faction, and strike the bargain with them instead of the Tower'}, 'chance': 0.62}),
    ('trade the partner a local project it wants, in return for its votes', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'coalition building', 'v': 'power, security', 'world': {'tribal': 'give the river clans a hunting ground they want, in return for their support', 'magic': 'give the Tower a new road it wants, in return for its votes'}, 'chance': 0.7}),
    ('give up the bill, and keep the partner sweet for a bigger fight later', 'B.34 R.33 G.33', None, 0.5, '', {'self_control': '-', 'v': 'power', 'world': {'tribal': 'let the plan go, and keep the river clans close for a bigger quarrel later', 'magic': 'let the decree go, and keep the Tower close for a bigger fight later'}, 'chance': 0.7}),
 ]},
{'name': 'the constituency wants one thing, the party another',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.2, 0.2, 0.2, 0.2),
 'drivers': 'unrest+.2 prosper-.2 community+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, colleague, friend, elder',
 'requires': 'member of parliament | local councillor',
 'worlds': {'earth': 'a closure the party backs and the town hates',
            'tribal': 'the faction wants the band to move north; your own hearths want to stay by the lake',
            'magic': 'the faction backs the new road through the ward you speak for'},
 'timing': {'times': 'per member of parliament or local councillor a year: about 1 in 5 (estimate)',
            'likelier': "a closure, a road, a building plan or a cut that falls on the member's own town, hard times",
            'rarer': 'a member whose party and town agree on most things, prosperous years with little to close',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The party has backed the closure of the town's last big factory, and the town is furious. "
                       'Four hundred jobs, a petition with nine thousand names, and {boss} on the phone saying the '
                       'line is the line.'),
                      ('W',
                       '{N} owes the party loyalty and the town service, and today the two point opposite ways. One '
                       'of them has to give.'),
                      ('U',
                       '{N} asks for the figures: what the closure saves, what it costs the town, what else could be '
                       'done. The answer is not as simple as either side says.'),
                      ('B',
                       'The party needs {Ns} vote, and the town needs {Ns} voice. {N} wonders what each would give '
                       'to have it.'),
                      ('R',
                       '{N} has stood at those factory gates on a cold morning with the shift coming out. {N} is not '
                       'going to pretend not to care.'),
                      ('G',
                       '{N} grew up in the shadow of that factory. Half the families on {Ns} street have someone who '
                       'worked there.')],
            'tribal': [('',
                        'The faction wants the band to move north for the winter. {Ns} own hearths want to stay by '
                        'the lake where their dead are buried.')],
            'magic': [('',
                       'The faction backs the new road from the capital, and it runs straight through the ward {N} '
                       'speaks for: the old market, the chapel, three hundred homes.')]},
 'outcomes': (['The town and the party both come out of it with something, and {N} keeps the trust of both.',
               'The decision changes, and the town knows whose work changed it.'],
              ['The party wins, the town loses, and both blame {N}.',
               'The fight drags on for months, and {N} ends it trusted by neither side.']),
 'options': [
    ('keep to the party line, and explain it honestly at a public meeting', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': "keep to the faction's word, and explain it honestly at the band's fire", 'magic': "keep to the faction's line, and explain it honestly in the ward hall"}, 'chance': 0.64}),
    ('commission the full figures on the closure, and let them settle it', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': 'ask the old ones what every past move cost, and let that settle it', 'magic': 'have the costs of the road set out in full, and let them settle it'}, 'chance': 0.66}),
    ('back the party in public, and win the town a sweetener in private', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'stand with the faction, and win your hearths the best winter ground in return', 'magic': 'back the faction, and win the ward a new market hall in return'}, 'chance': 0.62}),
    ('stand with the town at the factory gates, in front of the cameras', 'R1', None, 0.45, '', {'takes_if_fails': 'the party whip', 'mark': 'defied an authority', 'v': 'stimulation, benevolence', 'world': {'tribal': 'stand with your own hearths by the lake, in front of all the families', 'magic': 'stand with the ward at the gates of the old market, in front of the heralds'}, 'chance': 0.62}),
    ('side with the town and its people, whatever it costs in the party', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'side with your own hearths, whatever it costs in the faction', 'magic': 'side with the ward and its people, whatever it costs in the faction'}, 'chance': 0.68}),
    ('work inside the party to change the decision through its committees', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'work inside the faction, elder by elder, to change the decision', 'magic': "work inside the faction's councils to change the decision"}, 'chance': 0.42}),
    ("lead a march from the town to the party's headquarters", 'W.34 R.33 G.33', None, 0.5, '', {'identity': True, 'body': 'light', 'v': 'universalism, benevolence', 'world': {'tribal': "lead your hearths to the faction's fire, all of them together", 'magic': "lead a march from the ward to the faction's house in the capital"}, 'chance': 0.72}),
    ('broker a deal: the closure goes ahead, with work found for every worker', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'coalition building', 'v': 'power', 'world': {'tribal': 'broker a deal: the move goes ahead, with the best ground for your hearths', 'magic': 'broker a deal: the road goes ahead, with new homes for every family'}, 'chance': 0.48}),
    ('help the town draw up its own plan to keep the factory running', 'U.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'universalism', 'world': {'tribal': 'help your hearths find a way to winter by the lake without the faction', 'magic': 'help the ward draw up its own route for the road around the old market'}, 'chance': 0.42}),
    ("leak the party's own figures that show the closure is a mistake", 'U.34 B.33 R.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'approval: leaking party papers; backfire: the leak is traced, and the whip is withdrawn', 'self_control': '-', 'v': 'power, self-direction', 'world': {'tribal': "let slip what the faction's elders said in private about the move", 'magic': "leak the faction's own surveys that show the road is a mistake"}, 'chance': 0.72}),
 ]},
{'name': 'a donor wants a favour',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.1, 0.1, 0.1, 0.1),
 'drivers': 'money+.2 prosper+.1 stress+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'friend, colleague, boss',
 'requires': 'donors | a campaign war chest',
 'worlds': {'earth': 'a dinner, and a question about a planning permit',
            'tribal': 'the family that gave most to your feast wants the best hunting ground',
            'magic': 'a merchant prince who filled your coffer wants the harbour licence'},
 'timing': {'times': 'per person with donors or a campaign war chest a year: about 1 in 10 are asked for something '
                     'in return; most ask for access, a few for something unlawful (estimate)',
            'likelier': "large gifts from few donors, a planning or contract decision near the donor's business, a "
                        'member with a vote that matters',
            'rarer': 'many small gifts, strict rules on donations, a member with no say over contracts or permits',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Over dinner the donor who paid for half of {Ns} last campaign mentions, between courses, a '
                       'planning application for a warehouse on the edge of town. The committee meets on Thursday, '
                       "and wouldn't it be good if someone had a word."),
                      ('W',
                       'There is a register of interests and a code of conduct, and {N} knows both by heart. A gift '
                       'was a gift; it bought nothing.'),
                      ('U',
                       '{N} thinks it through: what the donor asked, what was not said, and what would be on the '
                       'record if any of it came out.'),
                      ('B',
                       'Money given is rarely given for nothing, and {N} knew that when the cheque came. The '
                       'question is what this favour is worth, and what refusing it would cost.'),
                      ('R', '{N} feels the wine turn sour. Is that what the friendship was about all along?'),
                      ('G',
                       "The donor's family has been part of the town for three generations, and so has {Ns}. "
                       'Whatever happens tonight, they will still pass in the street.')],
            'tribal': [('',
                        'The family that gave most to {Ns} feast comes to the hearth with a gift of meat and asks, '
                        'smiling, for the best hunting ground on the river.')],
            'magic': [('',
                       'A merchant prince who filled {Ns} coffer sends a note with a jewelled seal: the harbour '
                       'licence comes up for renewal, and the prince would like it.')]},
 'outcomes': (['The evening ends with the line drawn where {N} chose to draw it, and nobody can say otherwise.',
               'Months later the matter is closed, and {Ns} name is nowhere near it.'],
              ['The donor takes offence, and the next campaign has a hole in its budget.',
               'A reporter starts asking questions about the donations, and the questions do not stop.']),
 'options': [
    ('report the request in writing to the standards commissioner', 'W1', None, 0.45, '', {'takes': 'donors', 'v': 'conformity, universalism', 'world': {'tribal': 'tell the elders openly what the family asked', 'magic': "report the request in writing to the Crown's warden of conduct"}, 'chance': 0.85}),
    ('find out exactly what the permit needs, and tell the donor the proper route', 'U1', None, 0.45, '', {'v': 'achievement, conformity', 'world': {'tribal': 'find out what the custom of the hunting grounds says, and tell the family the proper way', 'magic': 'find out what the licence requires, and tell the prince the proper route'}, 'chance': 0.82}),
    ('keep taking the money, and promise nothing out loud', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'keep taking the gifts, and promise nothing aloud', 'magic': 'keep taking the gold, and promise nothing aloud'}, 'chance': 0.8}),
    ('tell the donor to their face that the money buys nothing', 'R1', None, 0.45, '', {'takes': 'donors', 'mark': 'made an enemy', 'v': 'stimulation, universalism', 'world': {'tribal': 'tell the family to their faces that their gifts buy nothing', 'magic': "tell the prince to the prince's face that the gold buys nothing"}, 'chance': 0.84}),
    ('give the money back, and keep the friendship if it can be kept', 'G1', None, 0.45, '', {'takes': 'donors', 'v': 'tradition, benevolence', 'world': {'tribal': 'give back the meat and the furs, and keep the old bond if it can be kept', 'magic': 'return the gold, and keep the old friendship if it can be kept'}, 'chance': 0.8}),
    ('refuse, and publish every donation ever received, with the names', 'W.34 U.33 R.33', None, 0.5, '', {'takes': 'donors', 'identity': True, 'v': 'universalism', 'world': {'tribal': 'refuse, and name at the fire every gift ever given', 'magic': 'refuse, and post every gift ever received on the guild hall door'}, 'chance': 0.78}),
    ('explain to the donor over a long lunch what a member can and cannot do', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': "sit with the family's elder and explain what a voice at the fire can and cannot do", 'magic': 'explain to the prince over supper what a member can and cannot do'}, 'chance': 0.7}),
    ('offer a lawful meeting with the planning officers, and nothing more', 'W.34 B.33 G.33', None, 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'offer to bring the family before the elders, and nothing more', 'magic': 'offer a lawful hearing with the harbour office, and nothing more'}, 'chance': 0.72}),
    ('do the favour, but leave no trace of it on paper', 'U.34 B.33 R.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "law: using office for a donor's private gain; backfire: the donor kept the emails, and uses them later", 'self_control': '-', 'v': 'power, achievement', 'world': {'tribal': 'do the favour, but let no one see it done', 'magic': 'do the favour, but leave no trace of it in the rolls'}, 'chance': 0.7}),
    ('have a quiet word with the planning committee, as asked', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "law: using office for a donor's private gain; backfire: the police open a file, and the papers find the donations", 'self_control': '-', 'v': 'power', 'world': {'tribal': 'have a quiet word with the elders who share the grounds, as asked', 'magic': 'have a quiet word with the harbour masters, as asked'}, 'chance': 0.75}),
 ]},
{'name': 'a scandal breaks',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.02, 0.02, 0.02),
 'drivers': 'stress+.2 era+.1 trouble+.15',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, family',
 'horizon': 'months',
 'roles': 'partner, boss, colleague, friend, parent',
 'requires': 'member of parliament | minister | mayor | local councillor | political adviser',
 'worlds': {'earth': 'the story is on the front page in the morning',
            'tribal': 'the singers make a mocking song about you, and every band hears it',
            'magic': 'the heralds cry it in every square by noon'},
 'timing': {'times': 'per member of parliament, minister, mayor, local councillor or political adviser a year: about '
                     '2 in 100; about 1 member in 5 meets a public scandal over a career, from expenses to conduct '
                     '(estimate)',
            'likelier': "years in office, a hostile press, a past with loose ends, a friend's business near the "
                        "office, a recent wrong of one's own",
            'rarer': 'a short time in office, a quiet local post, a clean record and careful habits',
            'gap_years': (3.0, 10.0)},
 'scenes': {'earth': [('',
                       'The story is on the front page in the morning: the expenses, the dates, a photograph. By '
                       "eight o'clock there are reporters at the gate and forty missed calls on {Ns} phone."),
                      ('W',
                       '{N} knows which rules were broken, or seem to have been, and what the rules say should '
                       'happen next.'),
                      ('U',
                       '{N} reads the article three times, separating what is true, what is half true and what is '
                       'simply wrong.'),
                      ('B',
                       'Every scandal has a life cycle. {N} starts thinking about how to shorten this one, and who '
                       'would gain if it ran long.'),
                      ('R',
                       '{Ns} face burns. {N} wants to go out to the gate and have it out with the reporters, right '
                       'now.'),
                      ('G',
                       '{N} thinks of {partner}, of {parent} reading the paper over breakfast, of the neighbours. '
                       'The shame of it lands on the whole family.')],
            'tribal': [('',
                        'The singers have made a mocking song about {N}, and by the second night every band in the '
                        'valley is singing it.')],
            'magic': [('',
                       'By noon the heralds are crying it in every square, and a broadsheet with {Ns} name across '
                       'the top is nailed to the guild hall door.')]},
 'outcomes': (['The storm passes within a fortnight, and {N} comes out of it still standing.',
               'The way {N} handles it earns grudging respect, even from opponents.'],
              ['The story runs for weeks, and every new day brings a new detail.',
               'The party cuts {N} loose, and old friends stop calling.']),
 'options': [
    ('refer yourself to the standards inquiry, and step back until it reports', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'put yourself before the elders, and keep from the fire until they judge', 'magic': "put yourself before the Crown's inquiry, and step back until it reports"}, 'chance': 0.64}),
    ('publish every document yourself, the good with the bad, before the papers can', 'U1', None, 0.45, '', {'mark': 'owned up', 'grants_if_fails': 'known across the country', 'self_control': '+', 'v': 'universalism, achievement', 'world': {'tribal': 'tell the whole story at the fire yourself, the good with the bad, before the singers can', 'magic': 'publish every letter yourself, the good with the bad, before the broadsheets can'}, 'chance': 0.62}),
    ('say nothing at all, and wait for the next story to bury this one', 'B1', None, 0.45, '', {'self_control': '+', 'grants_if_fails': 'known across the country', 'v': 'power', 'world': {'tribal': 'say nothing, and wait for the next song to bury this one', 'magic': 'say nothing, and wait for the next scandal to bury this one'}, 'chance': 0.55}),
    ('go on air the same morning, own it, and apologise in plain words', 'R1', None, 0.45, '', {'mark': 'owned up', 'grants_if_fails': 'known across the country', 'v': 'stimulation, benevolence', 'self_control': '+', 'world': {'tribal': 'stand up at the fire that night, own it, and say sorry in plain words', 'magic': 'stand in the square that morning, own it, and apologise in plain words'}, 'chance': 0.68}),
    ('ask old friends on the local paper to leave the story alone', 'G1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: leaning on the local press; backfire: the editor prints the request on the front page', 'v': 'tradition', 'world': {'tribal': 'ask the old singers who owe your family to stop the song', 'magic': 'ask old friends among the heralds to let the story drop'}, 'chance': 0.58}),
    ('resign at once, so that a way back stays open in a few years', 'W.34 U.33 B.33', None, 0.5, '', {'drops': 'member of parliament; minister; mayor; local councillor; political adviser', 'mark': 'owned up', 'self_control': '+', 'v': 'security, conformity', 'world': {'tribal': 'give up your place at once, so a way back stays open in a few summers', 'magic': 'resign the seat at once, so a way back stays open in a few years'}, 'chance': 0.9}),
    ('own it and stay: tell the town what happened, and ask it to judge', 'W.34 R.33 G.33', None, 0.5, '', {'identity': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'own it and stay: tell the band what happened, and let it judge', 'magic': 'own it and stay: tell the city what happened, and let it judge'}, 'chance': 0.64}),
    ('blame a junior member of staff, and let them go', 'W.34 B.33 R.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: blaming staff for one's own wrong; backfire: the staff member goes to the papers", 'self_control': '-', 'v': 'power', 'world': {'tribal': 'blame a young follower, and send them away', 'magic': 'blame a junior clerk, and dismiss them'}, 'chance': 0.62}),
    ('deny everything, loudly, and call it a smear', 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'hid a wrong', 'grants_if_fails': 'known across the country', 'self_control': '-', 'v': 'self-direction, power', 'world': {'tribal': 'deny it all, loudly, and call the song a lie', 'magic': 'deny it all, loudly, and call the broadsheet a forgery'}, 'chance': 0.45}),
    ('hire a good lawyer, and answer only what the law requires', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'security, power', 'world': {'tribal': 'ask an old, wise elder to speak on your behalf, and answer only what custom requires', 'magic': 'hire a sharp advocate, and answer only what the law requires'}, 'chance': 0.72}),
 ]},
{'name': 'the reshuffle',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.3, 0.3, 0.3),
 'drivers': 'unrest+.2 era+.2 trouble+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, rival, partner',
 'requires': 'minister',
 'worlds': {'earth': 'the call on reshuffle day that does not go the way you hoped',
            'tribal': 'the chief gives your duty to another speaker',
            'magic': 'the throne recalls your seal of office'},
 'timing': {'times': 'per minister a year: about 1 in 3 are moved, sacked or kept at a reshuffle; UK ministers stay '
                     'in one post for about two years on average (Institute for Government; estimate)',
            'likelier': 'a government in trouble in the polls, a new leader, a scandal elsewhere in the cabinet, a '
                        'long time in one post',
            'rarer': 'a government newly formed, a minister in the middle of a big reform, a leader who dislikes '
                     'reshuffles',
            'gap_years': (1.0, 2.0)},
 'scenes': {'earth': [('',
                       'The call comes at eleven on reshuffle day, and {boss} is brief: the department is going to '
                       'someone else. There is a smaller post if {N} wants it, or there is the back benches.'),
                      ('W',
                       "Ministers serve at the leader's pleasure; {N} knew that on the first day. The question is "
                       'how to leave the post in good order.'),
                      ('U',
                       '{N} is half way through a reform that took two years to design. Whoever comes next will not '
                       'understand it.'),
                      ('B',
                       '{N} counts who in cabinet gains from this, and who in the press will be told what. A '
                       'demotion can be survived, if it is handled right.'),
                      ('R', '{N} feels it like a slap. After everything, a phone call and five minutes.'),
                      ('G',
                       '{N} thinks of the officials who became friends, the corridor that had begun to feel like '
                       'home. Seasons turn, in government as anywhere.')],
            'tribal': [('',
                        'The chief gives {Ns} duty to another speaker in front of the whole fire. The families watch '
                        'to see what {N} will do.')],
            'magic': [('',
                       "A messenger brings the throne's letter: the seal of {Ns} office is recalled, to be given to "
                       'another councillor by the next moon.')]},
 'outcomes': (['By the end of the day {N} is somewhere {N} can live with, and the party knows how {N} took it.',
               'The move turns out well, and a year later {N} is glad of the new post or of the freedom.'],
              ['The day goes badly, and the story in the papers the next morning is not kind.',
               '{N} leaves the department with nothing settled, and the reform stalls without its author.']),
 'options': [
    ('accept the lesser post offered, and do it properly', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'take the lesser duty offered, and keep it well', 'magic': 'accept the lesser office offered, and keep it well'}, 'chance': 0.84}),
    ('accept the new post, and read its whole brief before the first meeting', 'U1', None, 0.45, '', {'self_control': '+', 'v': 'achievement', 'world': {'tribal': 'take the new duty, and learn everything about it before the next fire', 'magic': 'accept the new office, and read its whole archive before the first sitting'}, 'chance': 0.9}),
    ('turn the lesser post down, and take a well-paid outside job alongside the seat', 'B1', None, 0.45, '', {'drops': 'minister', 'v': 'power, achievement', 'world': {'tribal': "turn the lesser duty down, and set up as a flint trader alongside the band's work", 'magic': "turn the lesser office down, and take a merchant house's retainer alongside the seat"}, 'chance': 0.8}),
    ('resign in protest, and say why from the back benches that afternoon', 'R1', None, 0.45, '', {'drops': 'minister', 'mark': 'defied an authority', 'v': 'self-direction', 'world': {'tribal': 'give back the duty in protest, and say why at the fire that night', 'magic': 'hand back the seal in protest, and say why in the Assembly that afternoon'}, 'chance': 0.76}),
    ('go back to the back benches with grace, and to long weekends at home', 'G1', None, 0.45, '', {'drops': 'minister', 'mark': 'came home', 'v': 'tradition', 'world': {'tribal': "step back from the chief's side with grace, and go home to your own hearth", 'magic': 'hand back the seal with grace, and go home to the city for a season'}, 'chance': 0.74}),
    ('accept the move, but tell the leader plainly what the old department still needs', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': 'take the new duty, but tell the chief plainly what the old one still needs', 'magic': 'accept the move, but tell the throne plainly what the old office still needs'}, 'chance': 0.62}),
    ('plead to stay, with a written case for everything achieved so far', 'W.34 U.33 B.33', None, 0.5, '', {'drops_if_fails': 'minister', 'v': 'achievement, power', 'world': {'tribal': 'ask to keep the duty, setting out everything done with it', 'magic': 'plead to keep the seal, with a written account of everything achieved'}, 'chance': 0.3}),
    ('leave office warmly, thanking the officials one by one', 'W.34 R.33 G.33', None, 0.5, '', {'drops': 'minister', 'mark': 'made a friend', 'v': 'benevolence', 'world': {'tribal': 'leave the duty warmly, thanking the old hands one by one', 'magic': 'leave office warmly, thanking the clerks one by one'}, 'chance': 0.85}),
    ('take the lesser post, and quietly build a base for the next leadership contest', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'allies in the party', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'take the lesser duty, and quietly gather families for the day the faction chooses again', 'magic': 'take the lesser office, and quietly build a following for the next contest'}, 'chance': 0.7}),
    ('brief the papers against the leader before the day is out', 'B.34 R.33 G.33', None, 0.5, '', {'mark': 'made an enemy', 'closed': "approval: briefing against one's own leader; backfire: the whip is withdrawn", 'takes': 'allies in the party', 'v': 'power, self-direction', 'world': {'tribal': 'set the singers against the chief before nightfall', 'magic': "brief the broadsheets against the throne's favourites before nightfall"}, 'chance': 0.72}),
 ]},
{'name': 'the night you lose the seat',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'mature elder',
 'per_year': (0.0, 0.0, 0.0, 0.04, 0.04, 0.03),
 'drivers': 'unrest+.3 prosper-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, family',
 'horizon': 'years',
 'roles': 'partner, rival, colleague, friend, boss',
 'requires': 'member of parliament',
 'title': 'former member of parliament',
 'drops': 'member of parliament',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': "the count, the cameras, and the other candidate's speech",
            'tribal': 'the bands stand behind another speaker, and your place at the gathering is gone',
            'magic': 'the urns turn against you, and your seat in the Assembly passes to another'},
 'timing': {'times': 'per member of parliament of a year or more a year: about 4 in 100 adults and in midlife and 3 '
                     'in 100 elders lose the seat; in a landslide a party can lose a third or more of its members in '
                     'one night (estimate)',
            'likelier': 'a landslide against the party, a marginal seat, new boundaries, a scandal, hard times',
            'rarer': 'a safe seat, a popular member, a good year for the party',
            'gap_years': (1.0, 4.0)},
 'scenes': {'earth': [('',
                       'The count is over by three in the morning. {rival} is at the microphone thanking the voters, '
                       'and the cameras have turned, very slowly, toward {N}.'),
                      ('W',
                       'The voters have decided, and {N} believes in that more than in any one result. It still '
                       'hurts.'),
                      ('U',
                       '{N} saw this coming in the numbers weeks ago, and hoped to be wrong. Now the question is '
                       'what went wrong, and where.'),
                      ('B',
                       'Years of work, gone in one night. {N} is already thinking about what is left: the name, the '
                       'contacts, the offers that will come.'),
                      ('R',
                       '{N} wants to shout at someone: the leader, the party, the voters, {rival}. Instead {N} '
                       'stands on the stage and grips the rail.'),
                      ('G',
                       '{N} thinks of the office in the high street, the staff who will lose their jobs, the case '
                       'files of people still waiting for help.')],
            'tribal': [('',
                        'The bands walk to stand behind another speaker, and {Ns} place at the gathering is gone. '
                        'The young followers look at the ground.')],
            'magic': [('',
                       'The last urn is opened and the herald cries another name. {Ns} seat in the Assembly passes '
                       'to a rival before the candles burn down.')]},
 'outcomes': (['{N} gets through the night with dignity, and the next chapter starts sooner than expected.',
               'A month later {N} has a plan, and the people who matter are still there.'],
              ['The night goes badly on camera, and the clip follows {N} for years.',
               'Months pass, and {N} still wakes at six with nowhere to be.']),
 'options': [
    ('concede with grace, and congratulate the winner by name from the stage', 'W1', None, 0.45, '', {'identity': True, 'v': 'conformity, benevolence', 'world': {'tribal': "give way with grace, and clasp the winner's arm before all the bands", 'magic': 'concede with grace, and bow to the winner before the whole square'}, 'chance': 0.92}),
    ('ask for the figures box by box, and work out where the votes went', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'ask the elders which bands moved, and work out why', 'magic': "ask for every urn's tally, and work out where the lots went"}, 'chance': 0.92}),
    ("take the lobbying firm's offer that arrives before the week is out", 'B1', None, 0.45, '', {'title': 'lobbyist', 'identity': True, 'v': 'power', 'world': {'tribal': "take the flint-traders' offer to plead their case at the fires", 'magic': "take the merchant house's offer to plead its case at court"}, 'chance': 0.8}),
    ('blame the leader on live television before leaving the count', 'R1', None, 0.45, '', {'mark': 'made an enemy', 'v': 'self-direction', 'world': {'tribal': "blame the faction's head before all the bands before leaving the meadow", 'magic': "blame the faction's head before the heralds before leaving the square"}, 'chance': 0.82}),
    ('go home, sleep for a week, and spend the summer with the family', 'G1', None, 0.45, '', {'mark': 'came home', 'v': 'tradition, hedonism', 'world': {'tribal': 'go back to your own hearth, sleep, and spend the summer with the family'}, 'chance': 0.88}),
    ('go back to the doorsteps of the seat the next morning, to win it back', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'parliamentary nomination', 'self_control': '+', 'binds': True, 'v': 'achievement, tradition', 'world': {'tribal': 'go back to the hearths the next morning, to win the band back', 'magic': "go back to the city's doors the next morning, to win the seat back"}, 'chance': 0.15}),
    ('take a post at party headquarters, and stay close to power', 'W.34 B.33 R.33', None, 0.5, '', {'title': 'party official', 'door': True, 'v': 'power', 'world': {'tribal': "become keeper of the faction's bonds, and stay close to its head", 'magic': "become steward of the faction's house, and stay close to its head"}, 'chance': 0.7}),
    ('go back to the old career, and keep a hand in the local party', 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'came home', 'v': 'security, tradition', 'world': {'tribal': "go back to the hunt, and keep a place at the faction's fire", 'magic': "go back to the old craft, and keep a hand in the faction's ward"}, 'chance': 0.8}),
    ('travel for a year, as far from politics as the money allows', 'U.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'walk to the far valleys for a year, as far from the gathering as legs allow', 'magic': 'take ship for a year, as far from the Assembly as the purse allows'}, 'chance': 0.88}),
    ('write the book about what really went on in government', 'U.34 B.33 R.33', None, 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'become a teller of what really went on at the gatherings', 'magic': 'write the memoir of what really went on in the Assembly'}, 'chance': 0.45}),
 ]},
{'name': 'the party turns on its leader',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.15, 0.15, 0.15),
 'drivers': 'unrest+.3 trouble+.2 prosper-.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'rival, colleague, boss, partner, friend',
 'requires': 'party leader',
 'worlds': {'earth': 'letters of no confidence and a vote on Tuesday',
            'tribal': "the families meet without you, and the faction's elders come to your fire",
            'magic': 'the houses of the faction meet in secret to unseat you'},
 'timing': {'times': 'per party leader a year: about 15 in 100; most leaders leave after a defeat or a revolt '
                     '(estimate)',
            'likelier': 'bad polls, a lost election, a scandal, rivals with a following of their own, years in the '
                        'job',
            'rarer': 'a leader newly chosen, a leader who has just won, a united party',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'On Friday the letters start to arrive at the party office, and by Sunday there are enough of '
                       'them. The vote of confidence is on Tuesday, and {rival} has stopped answering {Ns} calls.'),
                      ('W',
                       "The party's rules allow this, and a leader who believes in rules has to accept them now. The "
                       'vote must be held properly, whatever it brings.'),
                      ('U',
                       '{N} wants the numbers: how many letters, from whom, and how many more would follow if the '
                       'vote went badly.'),
                      ('B',
                       "{N} built this party's machine and knows every lever in it. The plotters have numbers; {N} "
                       'has favours.'),
                      ('R',
                       '{N} is furious, and hurt, and wants to stand up in front of the whole party and dare them.'),
                      ('G',
                       '{N} has seen leaders come and go, and remembers how the last ones fell. The members in the '
                       'towns did not choose this; a few people in the capital did.')],
            'tribal': [('',
                        "The families met without {N} under the new moon. Now the faction's elders come to {Ns} "
                        'fire, and they do not sit down.')],
            'magic': [('',
                       "The houses of the faction have met in secret in the Tower's shadow to unseat {N}. A friend "
                       'brings the news before dawn.')]},
 'outcomes': (['By Tuesday night the matter is settled the way {N} chose, and the party knows where it stands.',
               'The plotters back down, or {N} steps away on {Ns} own terms, and the dignity of it is remembered.'],
              ['The vote goes against {N}, and the new leader is chosen within the month.',
               '{N} survives the vote by a handful, and everyone knows it cannot last.']),
 'options': [
    ('use the rulebook to put off the vote until the autumn conference', 'W1', None, 0.45, '', {'drops_if_fails': 'party leader', 'closed': "approval: twisting the party's rules to save oneself; backfire: the party's committee overrules it, and the vote comes sooner", 'v': 'conformity', 'world': {'tribal': "invoke an old custom to put off the families' choosing until the next gathering", 'magic': "invoke the faction's charter to put off the vote until midsummer"}, 'chance': 0.42}),
    ('win the vote with a detailed plan for the next election, put to every member', 'U1', None, 0.45, '', {'drops_if_fails': 'party leader', 'identity': True, 'v': 'achievement', 'world': {'tribal': 'win the families back with a plan for the next gathering, told at every hearth', 'magic': 'win the houses back with a written plan for the next season'}, 'chance': 0.4}),
    ('fight the vote, ringing every member who owes a favour', 'B1', None, 0.45, '', {'drops_if_fails': 'party leader', 'identity': True, 'v': 'power', 'world': {'tribal': 'fight it, going to every family that owes a gift', 'magic': 'fight it, calling in every debt the houses owe'}, 'chance': 0.46}),
    ('make a speech to the whole party that dares the plotters to act', 'R1', None, 0.45, '', {'drops_if_fails': 'party leader', 'v': 'stimulation, self-direction', 'world': {'tribal': 'stand up at the great fire, and dare the plotters to act', 'magic': "stand up in the faction's hall, and dare the plotters to act"}, 'chance': 0.4}),
    ("go over the plotters' heads, to the members in the towns", 'G1', None, 0.45, '', {'drops_if_fails': 'party leader', 'v': 'tradition, universalism', 'world': {'tribal': "go over the elders' heads, to the families in the far camps", 'magic': "go over the houses' heads, to the faction's members in the towns"}, 'chance': 0.46}),
    ('resign with dignity that afternoon, before the vote is held', 'W.34 U.33 R.33', None, 0.5, '', {'drops': 'party leader', 'identity': True, 'v': 'conformity', 'world': {'tribal': 'give up the headship with dignity that day, before the families choose', 'magic': 'step down with dignity that day, before the houses vote'}, 'chance': 0.85}),
    ('strike a deal: a date for leaving, in return for peace until then', 'W.34 U.33 B.33', None, 0.5, '', {'binds': True, 'v': 'security, power', 'world': {'tribal': 'agree a summer for stepping down, in return for peace until then', 'magic': 'agree a date for stepping down, in return for peace until then'}, 'chance': 0.7}),
    ("bring in the party's elders to settle it behind closed doors", 'W.34 B.33 G.33', None, 0.5, '', {'v': 'tradition, security', 'world': {'tribal': 'call in the oldest of the faction to settle it at a quiet fire', 'magic': "call in the faction's old lords to settle it behind closed doors"}, 'chance': 0.65}),
    ('step aside, and back a successor who will keep the cause alive', 'U.34 R.33 G.33', None, 0.5, '', {'drops': 'party leader', 'v': 'universalism, benevolence', 'world': {'tribal': "step aside, and stand behind a younger one who will keep the faction's cause", 'magic': "step aside, and back a successor who will keep the faction's cause alive"}, 'chance': 0.72}),
    ('sack the ringleaders from the front bench, and dare the rest to try', 'B.34 R.33 G.33', None, 0.5, '', {'drops_if_fails': 'party leader', 'mark': 'made an enemy', 'v': 'power', 'world': {'tribal': "drive the ringleaders from the faction's fire, and dare the rest to follow", 'magic': 'strip the ringleaders of their offices, and dare the rest to try'}, 'chance': 0.55}),
 ]},
{'name': 'a speech that goes everywhere',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'era+.3 unrest+.2 fortune+.15',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'friend, colleague, partner, boss, rival',
 'requires': 'member of parliament | mayor | local councillor | party leader | council candidate | parliamentary '
             'candidate',
 'worlds': {'earth': 'a speech filmed on a phone that the whole country shares by morning',
            'tribal': 'words spoken at the fire that every band in the valley repeats by the next moon',
            'magic': 'an oration the heralds carry to every city of the realm'},
 'timing': {'times': 'per member of parliament, mayor, councillor, party leader or candidate a year: about 2 in 100 '
                     'adults and in midlife and 1 in 100 elders give a speech the whole country shares; only a few '
                     'in a hundred of those become known across the country by it (estimate)',
            'likelier': 'a speech on a subject the country is arguing about, a slow news week, a phone in the right '
                        'hand, strong feeling in the room',
            'rarer': 'a quiet year, a speech read from notes, a busy news week',
            'gap_years': (3.0, 10.0)},
 'scenes': {'earth': [('',
                       'Someone at the back of the hall filmed the speech on a phone. By breakfast it has been '
                       'watched four million times, and {Ns} phone has not stopped ringing since six.'),
                      ('W',
                       '{N} said what {N} believed, plainly, in front of the people it concerned. Now the whole '
                       'country has heard it, and every word has to stand.'),
                      ('U',
                       '{N} reads the comments for an hour and starts to see what people heard in it, and what they '
                       'missed.'),
                      ('B',
                       'Attention like this comes once in a career, if at all. {N} can feel how much it could open, '
                       'and how fast it will fade.'),
                      ('R',
                       '{N} watches the clip and hardly recognises the person in it, alight and furious and true. '
                       'Strangers are quoting it back.'),
                      ('G',
                       'The speech was about one street, one closed library, one family. {N} wants it to stay about '
                       'them.')],
            'tribal': [('',
                        'Words {N} spoke at the fire are carried from camp to camp, and by the next moon every band '
                        'in the valley is repeating them.')],
            'magic': [('',
                       'The heralds carry {Ns} oration from the Assembly to every city of the realm, and in the '
                       'taverns strangers argue over it.')]},
 'outcomes': (['The moment turns into something that lasts, and {N} is glad of the way it was used.',
               'Weeks later strangers still stop {N} in the street to talk about the speech.'],
              ['The attention fades within a week, and nothing much is left of it.',
               'The clip is cut and twisted by the other side, and {N} spends a month explaining what was really '
               'meant.']),
 'options': [
    ('keep to every word of it, and answer every reporter who rings', 'W1', None, 0.45, '', {'grants': 'handling the press', 'v': 'conformity, universalism', 'world': {'tribal': 'stand by every word of it, and answer every singer who asks', 'magic': 'stand by every word of it, and answer every herald who calls'}, 'chance': 0.78}),
    ('write the longer argument behind the speech, and publish it while people listen', 'U1', None, 0.45, '', {'grants': 'drafting policy', 'v': 'achievement', 'world': {'tribal': 'tell the longer story behind the words at every fire that will listen', 'magic': 'write the treatise behind the oration, and publish it while the realm listens'}, 'chance': 0.78}),
    ("make sure the party's leaders hear the name before the week is out", 'B1', None, 0.45, '', {'grants': 'a following in the party', 'v': 'power, achievement', 'world': {'tribal': "make sure the faction's elders hear the name before the moon turns", 'magic': "make sure the faction's lords hear the name before the week is out"}, 'chance': 0.78}),
    ('give the same speech again at a rally the next night, louder', 'R1', None, 0.45, '', {'grants': 'rousing a crowd', 'v': 'stimulation', 'world': {'tribal': 'speak the same words again at the next fire, louder', 'magic': 'give the same oration again in the square the next night, louder'}, 'chance': 0.78}),
    ('take the speech back to the people it was about, and let them speak next', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'take the words back to the families they were about, and let them speak next', 'magic': 'take the oration back to the ward it was about, and let its people speak next'}, 'chance': 0.62}),
    ('turn it into a national campaign for the cause, with the local people at its heart', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'known across the country', 'v': 'universalism, benevolence', 'world': {'tribal': 'carry the cause to every clan of the valley, with your own families at its heart', 'magic': "carry the cause to every city of the realm, with the ward's people at its heart"}, 'chance': 0.12}),
    ('travel to speak in every town that sends an invitation', 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'a following in the party', 'door': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'walk to speak at every fire that sends word', 'magic': 'ride to speak in every city that sends an invitation'}, 'chance': 0.7}),
    ("take every national programme's invitation, and become the face of the cause", 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'known across the country', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'become the face of the cause in the songs of every camp', 'magic': "take every herald's call, and become the face of the cause across the realm"}, 'chance': 0.14}),
    ('write a book on the back of it, while the publishers are calling', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'known across the country', 'v': 'achievement, power', 'world': {'tribal': 'become a teller of the cause, and let the tale travel', 'magic': 'write a pamphlet on the back of it, while the printers are calling'}, 'chance': 0.1}),
    ('turn down the cameras, and use the moment to win a better committee post', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'allies in the party', 'v': 'power, security', 'world': {'tribal': "turn the singers away, and use the moment to win a better place at the faction's fire", 'magic': 'turn the heralds away, and use the moment to win a better seat on a council of the Assembly'}, 'chance': 0.65}),
 ]},
{'name': 'standing with no party behind you',
 'stages': 'young_adult adult mature elder',
 'age': (22, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.002, 0.01, 0.01, 0.005),
 'drivers': 'unrest+.3 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'friend, partner, rival, colleague',
 'requires': 'local councillor | mayor | former member of parliament | voice at the town hall',
 'worlds': {'earth': 'an election is called, every party has its candidate, and none of them is from the town you '
                     'have served for years',
            'tribal': "the band will choose its speaker for the great gathering, and the faction's elders have named "
                      'theirs, a stranger to your hearths',
            'magic': "the lots for the city's seat in the Assembly are called, and every name on the roll carries a "
                     "faction's seal"},
 'timing': {'times': 'per councillor of four years, mayor of two, former member or long-standing civic voice a year: '
                     'about 1 in 100 weighs standing for parliament with no party (estimate, about ten times the '
                     'real rate on purpose); getting on the ballot takes ten signatures and a deposit (500 pounds in '
                     'the UK, Electoral Commission), and most who file are nominated; a few hundred independents '
                     'stand at each UK general election (4,515 candidates in all in 2024, House of Commons), and '
                     'between none and six have won at each of the last four (House of Commons results), about 1 in '
                     "100; here 'election night' decides at about 2 in 100 for a candidate with no party nomination",
            'likelier': 'a local fight the parties ignored, a member who has held the seat for decades, an angry '
                        'year with every party in disgrace, many years on the council, a name the town already knows',
            'rarer': 'a contented town, a close race between two parties where every vote is spoken for, a party '
                     'card in the pocket, no money to spare, heavy care duties',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       'The election is called on a Tuesday, and every party already has its candidate, none of them '
                       "from the town. {N} has spent years in its public life: the council chamber, the residents' "
                       'meetings, the fight to keep the library open. The nomination papers want ten signatures and '
                       'a deposit, and they are due on Thursday week.'),
                      ('W',
                       'Anyone of age may stand: the law says so, and {N} has read it twice. Ten signatures, a '
                       "deposit, a form filed by noon on the right day. After years of the council's standing "
                       'orders, these rules hold no fears.'),
                      ('U',
                       '{N} has the results from every ward {N} ever fought, and the last three for the seat beside '
                       "them. On paper there is a way through, if the town's own votes and the stay-at-homes could "
                       'be joined up.'),
                      ('B',
                       'Years of council work leave a ledger of favours: the traders helped with a licence, the '
                       'clubs with a grant, the families with a housing case. {N} has never called them in. This '
                       'would be the time.'),
                      ('R',
                       'The parties have had their turn. For years {N} has watched them send candidates who leave '
                       'the day after the count, and is tired of saying so only in the council chamber.'),
                      ('G',
                       'The town has sent the same kind of member to parliament for forty years, and not one of them '
                       'ever lived on its streets. {N} has, and half the doors in the ward have opened to {N} at '
                       'some time in the last ten years.')],
            'tribal': [('',
                        'The band will choose its speaker for the great gathering at the next full moon, and the '
                        "faction's elders have named a man from another valley. {N} has spoken at the council fire "
                        "for many summers with no faction's blessing, and the far hearths listen. A hawk circled "
                        '{Ns} hearth that morning, and some say it was a sign.')],
            'magic': [('',
                       "The lots for the city's seat in the Assembly will be cast at midsummer, and so far every "
                       "name on the roll carries a faction's seal. {N} has sat on the ward council for years under "
                       'none. A hedge-witch in the lower town sells luck charms to candidates; she says she has '
                       'never sold one to someone standing alone.')]},
 'outcomes': (['When it is over {N} has done what {N} set out to do, and people who never noticed {N} before stop in '
               'the street to say so.',
               'Something comes of the weeks that nobody predicted, and {N} wakes the next morning to a slightly '
               'different life.'],
              ['The papers come back from the returning officer with two signatures struck out, and the deadline '
               'passed at noon. {N} folds the form into a pocket and walks back past the council offices.',
               'It does not come off: the helpers and the money are not there in time. On the drive home {N} is '
               'already counting what the weeks cost, and what they taught.']),
 'options': [
    ('file the nomination papers by the book, and stand as an independent', 'W1', None, 0.45, '', {'title': 'parliamentary candidate', 'aims': 'member of parliament', 'v': 'conformity, universalism', 'world': {'tribal': "ask the elders by the old custom to hear you as the band's speaker, with no faction", 'magic': "enter your name on the Assembly roll by every form, with no faction's seal"}, 'chance': 0.7}),
    ('stand on a plan for the seat, costed line by line, that no party offered', 'U1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'achievement, self-direction', 'world': {'tribal': "ask to be sent on a plan for the band's summer that no faction offered", 'magic': 'stand on a written plan for the city, costed coin by coin, that no faction offered'}, 'chance': 0.7}),
    ('call in the favours of years, and raise the deposit and the leaflets from them', 'B1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'power, achievement', 'world': {'tribal': 'call in the gifts of many summers, and ask to be sent with them behind you', 'magic': 'call in the favours of years, and raise the roll fee and the heralds from them'}, 'chance': 0.7}),
    ('stand, and say out loud at every hustings what the parties will not', 'R1', None, 0.45, '', {'title': 'parliamentary candidate', 'aims': 'member of parliament', 'v': 'stimulation, self-direction', 'world': {'tribal': "stand up at every fire and say what the faction's elders will not", 'magic': "stand with the hedge-witch's charm at your throat, and cry in every square what the factions will not"}, 'chance': 0.7}),
    ("stand as the town's own candidate, carried by the neighbours of many years", 'G1', None, 0.45, '', {'title': 'parliamentary candidate', 'v': 'tradition, universalism', 'world': {'tribal': "ask to be sent as the band's own, carried by the hearths of many summers", 'magic': "stand as the ward's own, carried by the neighbours and the old houses of the lane"}, 'chance': 0.7}),
    ("call a public meeting, and make every party candidate sign the town's pledge", 'B.5 R.5', None, 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': "call the bands to a fire of your own, and make every speaker swear to the far hearths' needs", 'magic': "call a meeting in the guild hall, and make every candidate sign the ward's pledge"}, 'chance': 0.85}),
    ('knock on doors for the independent the town already knows and trusts', 'R.5 G.5', None, 0.5, '', {'title': 'campaign volunteer', 'v': 'benevolence, stimulation', 'world': {'tribal': 'walk the hearths for the one the band already trusts', 'magic': "carry the banner of the ward's own candidate through the lanes"}, 'chance': 0.85}),
    ('join the party that comes closest, and go for its nomination from inside', 'U.5 B.5', None, 0.5, '', {'title': 'party member', 'v': 'achievement, power', 'world': {'tribal': 'bind yourself to the faction nearest your mind, and seek its blessing from within', 'magic': 'swear to the faction nearest your mind, and seek its seal from within'}, 'chance': 0.85}),
    ('stay out of it, and keep the time for the council work and the family', 'W.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, tradition', 'world': {'tribal': 'stay at your own hearth, and keep the summer for the council fire and the family', 'magic': 'stay out of it, and keep the season for the ward council and the family'}, 'chance': 0.85}),
    ("send every candidate the town's questions, and publish all their answers", 'W.5 U.5', None, 0.5, '', {'v': 'universalism, conformity', 'world': {'tribal': "put the band's questions to every speaker at the fire, and remember the answers", 'magic': "send every candidate the ward's questions, and nail their answers to the hall door"}, 'chance': 0.85}),
 ]},
{'name': 'a run for mayor from outside the council',
 'stages': 'young_adult adult mature elder',
 'age': (25, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 0.001, 0.002, 0.002, 0.001),
 'drivers': 'unrest+.2 era+.1 community+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'months',
 'roles': 'friend, rival, partner, colleague',
 'requires': "local party officer | voice at the town hall | residents' committee member | school-governance board "
             'member | union rep | local hero | good name in town | founder of a firm | family business | party '
             'member | activist in a cause',
 'worlds': {'earth': 'the mayor stands again with the council behind them, and nobody expects a contest',
            'tribal': 'the old head of the camp will lead again unless someone asks the band to choose',
            'magic': "the burgomaster's chain has passed between three guild houses for a hundred years, and the "
                     'lots are due at the autumn fair'},
 'timing': {'times': 'per person with years of standing in a town outside its council (a branch officer of four '
                     'years, a committee member, union rep, activist or local hero of five, a party member of six, a '
                     'school governor of four, a good name of ten, a firm of eight, a family business of ten) a '
                     'year: about 1 in 500 is urged to run for mayor (estimate, about ten times the real rate on '
                     'purpose); getting on the ballot takes signatures, and a deposit in some places, and most who '
                     'file with a campaign behind them are nominated (estimate); France has a mayor for each of its '
                     '34,875 communes (DGCL 2025) and the US about 19,500 municipalities (Census of Governments); '
                     "here 'polling day for mayor' then decides at about 1 in 10 (estimate)",
            'likelier': 'a mayor in office for many terms, a scandal at the town hall, a town that elects its mayor '
                        'directly, a name everyone in the market knows',
            'rarer': 'a mayor chosen by the council alone, a contented town, a newcomer to the place, a life far '
                     'from its streets',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       'The mayor is standing again, with the council and the old names behind them, and nobody '
                       "expects a contest. {N} has never sat on the council, but has spent years in the town's life "
                       'outside it, and at the bakery and the school gate people keep saying that someone should '
                       'stand, and that {N} would be the one to do it.'),
                      ('W',
                       '{N} has served the town for years by its rules in other chairs, and the charter is plain: '
                       'any resident may stand for mayor. A fair contest is good for the town even when the result '
                       'looks settled.'),
                      ('U',
                       "{N} has read the town's accounts in the library and found what the council never explains: "
                       'where the money for the roads went. Someone from outside the chamber, with the numbers, '
                       'could ask the questions nobody on the council will.'),
                      ('B',
                       "The mayor's people have run the town hall for twelve years. In {Ns} own years in the town's "
                       'business {N} has met a few of the firms they have crossed, and knows what those firms might '
                       'give to see them gone.'),
                      ('R',
                       "{N} has shouted from the public gallery for years and never once sat on the council's "
                       'benches, and does not mean to start by asking permission. The town needs shaking, and {N} '
                       'wants to do the shaking.'),
                      ('G',
                       '{Ns} family has lived in the town for four generations, and {N} knows half its streets by '
                       'the names of who lives on them. The town hall stopped listening to those streets years '
                       'ago.')],
            'tribal': [('',
                        'The old head of the camp will lead the moves again unless someone stands at the fire and '
                        'asks the band to choose. {N} has never spoken at the council fire, but for many summers the '
                        'families on the far side of the camp have come to {Ns} hearth with their troubles.')],
            'magic': [('',
                       "The burgomaster's chain has passed between three old guild houses for a hundred years. {N} "
                       'belongs to none of them, though {Ns} name has hung over a shop in the square for twenty '
                       'years, and the lots for the chain will be cast at the autumn fair. A fortune-teller at the '
                       'last fair told {N}, laughing, that chains can be broken.')]},
 'outcomes': (['{N} sees it through, and by the end of it the town hall knows {Ns} name and has stopped pretending '
               'not to.',
               'When the autumn comes, what {N} set out to do is done, and people in the market stop {N} to talk '
               'about it.'],
              ['The campaign never quite gets off the ground: the hall stays half empty, the helpers drift back to '
               'their own lives, and {N} lets the deadline pass with the papers still on the kitchen table.',
               'It does not come off, and for a few weeks the town has a joke about it; by spring {N} is the one '
               'telling it.']),
 'options': [
    ('stand for mayor on a promise to run the town hall by its own rules', 'W1', None, 0.45, '', {'title': 'mayoral candidate', 'v': 'conformity, universalism', 'world': {'tribal': 'ask the band to choose you as head of the camp, by the old custom of asking', 'magic': "stand for the chain on a promise to keep the town's charter to the letter"}, 'chance': 0.7}),
    ("stand on what the town's own accounts show, and ask where the money went", 'U1', None, 0.45, '', {'title': 'mayoral candidate', 'v': 'achievement, self-direction', 'world': {'tribal': 'ask to lead the camp, and show the band where the winter stores went', 'magic': "stand on the town's own ledgers, and ask aloud where the coin went"}, 'chance': 0.7}),
    ('stand with the backing of the businesses the town hall has crossed', 'B1', None, 0.45, '', {'title': 'mayoral candidate', 'aims': 'mayor', 'v': 'power, achievement', 'world': {'tribal': 'ask to lead the camp with the families the old head has slighted at your back', 'magic': 'stand for the chain with the guilds the old houses have crossed at your back'}, 'chance': 0.7}),
    ('stand, and hold a meeting in the square every Saturday until polling day', 'R1', None, 0.45, '', {'title': 'mayoral candidate', 'v': 'stimulation, self-direction', 'world': {'tribal': 'stand up at the fire every night until the band chooses', 'magic': 'stand, and speak from the fountain steps every market day until the lots'}, 'chance': 0.7}),
    ('stand as the candidate of the old streets the town hall forgot', 'G1', None, 0.45, '', {'title': 'mayoral candidate', 'aims': 'mayor', 'v': 'tradition, universalism', 'world': {'tribal': 'ask to lead as the one the far hearths trust', 'magic': 'stand for the chain as the voice of the old lanes the guild houses forgot'}, 'chance': 0.7}),
    ('stand for the council first, in the ward where the family is known', 'B.5 G.5', None, 0.5, '', {'title': 'council candidate', 'v': 'achievement, tradition', 'world': {'tribal': 'ask to be heard at the council fire first, where your family is known', 'magic': 'stand for the town council first, in the ward where your house is known'}, 'chance': 0.8}),
    ('write a plan for the old streets, and take it to every candidate', 'U.5 G.5', None, 0.5, '', {'v': 'universalism', 'world': {'tribal': 'work out where the far hearths should camp next winter, and take it to every elder', 'magic': 'draw up a plan for the old lanes, and take it to every candidate for the chain'}, 'chance': 0.8}),
    ('start a newsletter that asks the town hall the questions nobody asks', 'U.5 R.5', None, 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': "bring the band's questions to the fire every night, and ask the old head to answer them", 'magic': 'print a broadsheet that asks the town hall the questions nobody asks'}, 'chance': 0.8}),
    ('back the councillor who would make a better mayor, for a say in the plan', 'W.5 B.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'stand behind a voice at the fire who would lead better, for a say in the moves', 'magic': "back a councillor who would wear the chain better, for a say in the town's plan"}, 'chance': 0.8}),
    ('ask the mayor the question everyone wants answered, at the public meeting', 'W.5 R.5', None, 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': 'ask the old head at the fire the question every family wants answered', 'magic': 'ask the burgomaster, before the whole guild hall, the question every house wants answered'}, 'chance': 0.8}),
 ]},
{'name': 'polling day for mayor',
 'stages': 'young_adult adult mature elder',
 'age': (25, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'community.5',
 'per_year': (0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
 'drivers': 'unrest+.2 era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'week',
 'roles': 'partner, friend, rival, colleague',
 'requires': 'mayoral candidate',
 'drops': 'mayoral candidate',
 'worlds': {'earth': 'polling day for mayor, and the count in the town hall by nine',
            'tribal': 'the band stands in a ring at the full moon, and each family walks to stand behind the one it '
                      'wants as head of the camp',
            'magic': "the urns for the burgomaster's chain are opened in the guild hall at dusk, under the Order's "
                     'seal'},
 'timing': {'times': 'per mayoral candidate: once a candidacy; where the mayor is elected directly, the sitting '
                     "mayor or the council's own candidate wins most races (estimate), and someone who never sat on "
                     'the council, with years of standing in the town behind them, wins perhaps 1 race in 10 '
                     '(estimate), more often in an angry year or against a mayor in office for many terms; France '
                     'has a mayor for each of its 34,875 communes (DGCL 2025) and the US about 19,500 municipalities '
                     '(Census of Governments); about 1 life in 500 ever stands for mayor (catalogue share; estimate)',
            'likelier': 'a candidacy that runs to polling day',
            'rarer': 'a candidate who withdraws, an election called off',
            'gap_years': (1.5, 3.0)},
 'scenes': {'earth': [('',
                       "Polling day. The posters are up on every lamp post, the mayor's face on most of them and "
                       '{Ns} on the rest. The polls close at ten, and the count is in the town hall, under the '
                       'portraits of mayors who all sat on the council first.'),
                      ('W',
                       '{N} voted at seven, has kept to every rule of the day, and has checked twice that the agents '
                       'know where to stand at the count.'),
                      ('U',
                       "{N} has the morning's turnout street by street. The old streets are voting; the new estates "
                       'are not, yet.'),
                      ('B',
                       "The mayor's people have run the town hall for years and know how to get their voters out. "
                       '{N} has put the last of the money into cars for the old and the housebound.'),
                      ('R',
                       '{N} has not sat down since six in the morning: a loudspeaker in the square, a handshake at '
                       'every school gate, a joke for every queue.'),
                      ('G',
                       '{Ns} family is out on the old streets, knocking on doors that have opened to them for '
                       'generations, and the neighbours who promised are coming out in their coats.')],
            'tribal': [('',
                        'At the full moon the band stands in a wide ring, and the elders call the old head of the '
                        'camp and then {N}. Each family walks to stand behind the one it wants, and {N} watches the '
                        'lines grow, slowly, on both sides.')],
            'magic': [('',
                       "At dusk in the guild hall the Order's witnesses break the seals on the urns for the "
                       "burgomaster's chain. The old guild houses stand together by the hearth, {Ns} people stand by "
                       'the door, and the fortune-teller in the crowd has stopped laughing.')]},
 'outcomes': (['By nine the count is done, and the town wakes the next morning to something {N} made happen.',
               '{N} sees the day through, and by the end of it the town hall has to reckon with {Ns} name.'],
              ['The count is done by nine in the town hall. {N} comes second of three, closer than anyone predicted '
               "and not close enough, shakes the mayor's hand on the steps and walks home past the bakery.",
               'It does not come off. The next morning {N} takes the posters down one lamp post at a time, and '
               'people stop in the street to say they voted for {N}.']),
 'options': [
    ('keep to every rule of the day, and be at the count when the boxes open', 'W1', None, 0.45, '', {'title': 'mayor', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': 'keep every custom of the choosing, and stand in the ring when the elders call', 'magic': 'keep every form of the day, and stand by the urns when the seals break'}, 'chance': 0.1}),
    ('send every helper to the streets where the turnout is still low', 'U1', None, 0.45, '', {'title': 'mayor', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'send every friend to the hearths that have not yet walked to the ring', 'magic': 'send every runner to the lanes where the urns are still light'}, 'chance': 0.1}),
    ('spend the last of the money on lifts to the polls for the housebound', 'B1', None, 0.45, '', {'title': 'mayor', 'grants_if_fails': 'a long shot that missed', 'aims': 'mayor', 'v': 'power, achievement', 'world': {'tribal': 'give the last of your stores so the old and the lame can be carried to the ring', 'magic': 'spend the last of your purse on carts to the urns for the old and the lame'}, 'chance': 0.1}),
    ('spend the whole day in the square with a loudspeaker until the polls close', 'R1', None, 0.45, '', {'title': 'mayor', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, hedonism', 'world': {'tribal': 'drum and sing at the edge of the ring until the last family has walked', 'magic': 'cry your name from the fountain steps until the urns are sealed'}, 'chance': 0.1}),
    ('walk the old streets with the family, knocking on every door that ever opened', 'G1', None, 0.45, '', {'title': 'mayor', 'grants_if_fails': 'a long shot that missed', 'aims': 'mayor', 'v': 'tradition, benevolence', 'world': {'tribal': 'walk the far hearths with your family, and bring every household to the ring', 'magic': 'walk the old lanes with your house, knocking on every door that ever opened'}, 'chance': 0.1}),
    ('trade your helpers to the challenger in the last days, for your plan in their programme', 'U.25 B.25 R.25 G.25', None, 0.5, '', {'v': 'power, benevolence', 'world': {'tribal': 'send your friends to stand behind the strongest challenger, for your plan in the next moves', 'magic': 'lend your runners to the strongest challenger, for your plan in their charter'}, 'chance': 0.8}),
    ('stop campaigning, and send every helper to the challenger likeliest to beat the mayor', 'W.25 B.25 R.25 G.25', None, 0.5, '', {'v': 'power, universalism', 'world': {'tribal': 'step out of the ring, and send your families behind the one likeliest to beat the old head', 'magic': 'stand down from the lots, and send your runners to the one likeliest to win the chain'}, 'chance': 0.8}),
    ('step aside for the younger candidate the old streets trust more, and run their day', 'W.25 U.25 R.25 G.25', None, 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'step aside for the younger one the far hearths trust more, and walk the hearths for them', 'magic': 'stand down for the younger candidate the old lanes trust more, and run their day at the urns'}, 'chance': 0.8}),
    ("agree a joint ticket with the strongest rival, and take the deputy's post if it wins", 'W.25 U.25 B.25 G.25', None, 0.5, '', {'v': 'power, security', 'world': {'tribal': 'join with the strongest rival, and take the place at their side if the band chooses them', 'magic': "join lists with the strongest rival, and take the deputy's seal if the chain is theirs"}, 'chance': 0.8}),
    ("concede before the count, and take the campaign's plan to whoever wins, in writing", 'W.25 U.25 B.25 R.25', None, 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'step out of the ring before the families walk, and bring your plan to whoever is chosen', 'magic': 'concede before the seals break, and take your plan to whoever wins the chain, in writing'}, 'chance': 0.8}),
 ]},
{'name': 'a challenge from the back benches',
 'stages': 'adult mature elder',
 'age': (25, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.004, 0.005, 0.003),
 'drivers': 'unrest+.3 prosper-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, rival, friend, partner',
 'requires': 'member of parliament',
 'worlds': {'earth': 'the leader is in trouble, the senior names wait for each other, and someone from the back '
                     'benches could move first',
            'tribal': "the faction's head has led the families badly for two summers, and the elders mutter but do "
                      'nothing',
            'magic': 'the head of the faction has lost three votes in the Assembly this season, and the great houses '
                     'wait for each other'},
 'timing': {'times': 'per member of parliament with four years or more in the seat and no post a year: about 1 in '
                     '200 thinks seriously about challenging the leader from the back benches (estimate); most '
                     'parties change leader every four to six years, nearly always for a name from the front bench, '
                     'and a back-bencher with no following and no name across the country wins perhaps 1 contest in '
                     '50 (estimate)',
            'likelier': 'a leader behind in the polls, a party that lets its members choose, many years on the back '
                        'benches, a cause the leadership has dropped',
            'rarer': 'a leader just elected, a party winning comfortably, a member with a post to lose',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       'The leader is in trouble: the polls are bad, the party is restless, and every senior name is '
                       'waiting for someone else to move first. Late one night in the tea room {colleague} says it '
                       'plainly: the front bench will never do it, so it will have to be someone from the back.'),
                      ('W',
                       "The party's rules allow any member with enough nominations to challenge. {N} has sat in the "
                       'house for years and never thought of it as a rule meant for someone like {N}, until now.'),
                      ('U',
                       "{N} has the numbers on the party's slide in a notebook, seat by seat, kept up for years. "
                       'Nobody at the top seems to have read them.'),
                      ('B',
                       'Nobody at the top will risk a career on a challenge. That leaves the field to whoever has '
                       'least to lose, and {N} has spent years on the back benches with very little to lose.'),
                      ('R',
                       '{N} is sick of the waiting, the briefings, the unnamed quotes in the papers. If somebody is '
                       'going to say it, it might as well be said out loud, by name.'),
                      ('G',
                       '{N} thinks of the members back home who knock on doors every winter for a party that no '
                       'longer listens to them. Someone should speak for them, even from the last row.')],
            'tribal': [('',
                        "The faction's head has led the families badly for two summers, and the elders mutter but do "
                        'nothing. {N}, a speaker of many gatherings whom nobody heeds, could step into the ring and '
                        'ask the families to choose again.')],
            'magic': [('',
                       'The head of the faction has lost three votes in the Assembly this season, and the great '
                       'houses wait for each other to move. {N} has sat on the back bench of the hall for years, '
                       "where nobody looks, beside an old mage who mutters that the faction's lots have not favoured "
                       'its head since the comet.')]},
 'outcomes': (['{N} does what {N} set out to do, and by the end of the week the whole party knows {Ns} name.',
               'The party settles its quarrel, and {Ns} part in it is remembered on both sides of the room.'],
              ['Nominations close at noon on Friday and {Ns} count is eleven short. {N} reads the statement out on '
               'the steps anyway, then takes the late train home with the papers folded on one knee.',
               "It does not come off. For a season the leader's people are cool in the corridors, and {N} eats alone "
               'in the tea room more often than before.']),
 'options': [
    ('gather the nominations the rules require, and challenge the leader in the open', 'W1', None, 0.45, '', {'title': 'party leader', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'allies in the party', 'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders, by the custom of the ring, for the families to choose again', 'magic': "gather the seals the faction's charter asks, and challenge its head openly"}, 'chance': 0.02}),
    ('publish a plan to turn the party round, and challenge on it', 'U1', None, 0.45, '', {'title': 'party leader', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'allies in the party', 'aims': 'party leader', 'v': 'achievement, self-direction', 'world': {'tribal': 'lay out at the fire how the faction could win back the bands, and ask to lead it', 'magic': 'publish a treatise on how the faction could win back the Assembly, and challenge on it'}, 'chance': 0.02}),
    ('count the nominations in secret, and strike the morning the leader stumbles', 'B1', None, 0.45, '', {'title': 'party leader', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'allies in the party', 'v': 'power, achievement', 'world': {'tribal': "count the families' promises quietly, and step into the ring the day the head stumbles", 'magic': "count the houses' seals in secret, and strike the morning the head stumbles"}, 'chance': 0.02}),
    ("stand up at the members' meeting and call for the leader to go", 'R1', None, 0.45, '', {'title': 'party leader', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'allies in the party', 'aims': 'party leader', 'v': 'stimulation, self-direction', 'world': {'tribal': "stand up at the gathering and call for the faction's head to step aside", 'magic': "stand up in the faction's hall and call for its head to go"}, 'chance': 0.02}),
    ('challenge as the voice of the members in the towns the party forgot', 'G1', None, 0.45, '', {'title': 'party leader', 'grants_if_fails': 'a long shot that missed', 'takes_if_fails': 'allies in the party', 'v': 'tradition, universalism', 'world': {'tribal': 'ask to lead as the voice of the far bands the faction forgot', 'magic': 'challenge as the voice of the small towns and old wards the faction forgot'}, 'chance': 0.02}),
    ('back the strongest challenger quietly, for a post in the new team', 'B.5 G.5', None, 0.5, '', {'grants': 'allies in the party', 'v': 'power', 'world': {'tribal': "stand quietly behind the strongest challenger, for a duty at the new head's side", 'magic': "back the strongest challenger quietly, for an office in the new head's gift"}, 'chance': 0.75}),
    ('let it be known you might run, and see what the leader offers', 'B.5 R.5', None, 0.5, '', {'act': 'let it be known they might run, and see what the leader offers', 'v': 'power, stimulation', 'world': {'tribal': 'let the families hear you might step into the ring, and see what the head offers', 'magic': 'let the houses hear you might challenge, and see what the head offers'}, 'chance': 0.75}),
    ('write the article that says what everyone in the party thinks, and sign it', 'U.5 R.5', None, 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'tell the singers what everyone at the fire thinks, and let them sing it with your name', 'magic': 'write the broadsheet that says what every member thinks, and sign it'}, 'chance': 0.75}),
    ('stay loyal in public, and tell the leader the hard truth in private', 'W.5 G.5', None, 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': "stand by the faction's head at the fire, and tell the head the hard truth alone", 'magic': 'stand by the head in the Assembly, and tell the hard truth behind closed doors'}, 'chance': 0.75}),
    ("ask the party's ruling body for an open contest under fair rules", 'W.5 U.5', None, 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders for an open choosing in the ring, by the old custom', 'magic': "petition the faction's council for an open contest under a sealed charter"}, 'chance': 0.75}),
 ]},
{'name': 'the campaign nobody gave a chance',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.03, 0.02),
 'drivers': 'unrest+.3 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'partner, colleague, rival, boss, friend',
 'requires': 'party leader',
 'worlds': {'earth': 'the election is called with the party third in every poll, a long way behind the two big ones',
            'tribal': 'the gathering will choose a chief of the clans, and the faction is the smallest at the meadow',
            'magic': 'the throne will name its Chancellor from the faction that wins the Assembly, and the faction '
                     'holds a handful of seats'},
 'timing': {'times': 'per party leader of two years or more a year: about 3 in 100 lead a party far behind in the '
                     'polls into a general election (estimate); the leader of one of the two largest parties wins '
                     'about 1 time in 2, while a party that starts the campaign third or lower forms the government '
                     'only a few times in a generation across the democracies (estimate); about 1 life in two to '
                     'three million heads a government (catalogue share; estimate)',
            'likelier': 'an angry year, both big parties in disgrace, a leader known across the country, a voting '
                        'system that rewards a surge',
            'rarer': 'a contented country, a two-party system with high walls, a party with no money and no seats',
            'gap_years': (4.0, 6.0)},
 'scenes': {'earth': [('',
                       'The election is called with the party third in every poll, a long way behind the two big '
                       'ones. {N} has led it for years through bad polls and good ones, the commentators have '
                       'already written it off, and the only question on the morning shows is how badly {N} will '
                       'lose.'),
                      ('W',
                       '{N} believes the country deserves a real choice, and a party that stands everywhere and '
                       'campaigns properly to the last day, whatever the polls say.'),
                      ('U',
                       '{N} has the seat-by-seat numbers. A swing nobody expects, in forty seats nobody is watching, '
                       'would change everything, and the numbers say it is possible, just.'),
                      ('B',
                       'Third place means the big parties ignore {N}, and that leaves room to move. {N} has a plan '
                       'for the last week that nobody will see coming.'),
                      ('R',
                       '{N} loves being the underdog. The crowds are small but loud, and every one of them is a '
                       'reason to keep going.'),
                      ('G',
                       '{N} thinks of the places where the party was born, the halls and the market towns, and means '
                       'to win them back one at a time.')],
            'tribal': [('',
                        'The gathering will choose a chief of the clans, and {Ns} faction is the smallest at the '
                        'meadow, a few bands from the far valleys. The great factions have already counted the '
                        'summer as theirs.')],
            'magic': [('',
                       'The throne will name its Chancellor from the faction that wins the Assembly, and {Ns} '
                       'faction holds a handful of seats among hundreds. In the taverns they say the chain will go '
                       'to one of the two great houses, as it always has, and an augur in the market will not take '
                       'bets on it either way.')]},
 'outcomes': (['The campaign goes the way {N} meant it to, and on the last night the halls are fuller than anyone '
               'predicted.',
               'By the end the party is talked about in places that had forgotten it, and {N} is the reason.'],
              ['At four in the morning the seats are counted, and the party has its few, as the polls said. {N} '
               'concedes in a half-empty hall and thanks the volunteers by name before the cameras leave.',
               'It does not come off. {N} sleeps for a day, then gets up and rings every candidate who lost, one by '
               'one.']),
 'options': [
    ('stand in every seat, and campaign to the last day as if it could be won', 'W1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'grants_if_fails': 'a long shot that missed', 'aims': 'head of government', 'v': 'conformity, security', 'world': {'tribal': 'send a speaker to every fire of the valley, and campaign to the last night as if it could be won', 'magic': 'put a name on the lots of every ward, and campaign to the last day as if it could be won'}, 'chance': 0.02}),
    ('pour everything into the forty seats the polls are not watching', 'U1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'give every feast and every visit to the bands nobody else is counting', 'magic': 'pour the coffer into the forty wards the great houses are not watching'}, 'chance': 0.02}),
    ("hold back the party's one big promise for the last week, then spring it", 'B1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'grants_if_fails': 'a long shot that missed', 'aims': 'head of government', 'v': 'power, achievement', 'world': {'tribal': "keep the faction's great gift secret until the last night, then give it before all the clans", 'magic': "keep the faction's one great promise sealed until the last week, then break the seal"}, 'chance': 0.02}),
    ('turn every small rally into a carnival, and dare the cameras to ignore it', 'R1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, hedonism', 'world': {'tribal': 'turn every small fire into a feast with drums, and dare the singers to ignore it', 'magic': 'turn every small meeting into a fair with music, and dare the heralds to ignore it'}, 'chance': 0.02}),
    ('campaign in the market towns where the party was born, one by one', 'G1', None, 0.45, '', {'title': 'head of government', 'grants': 'a household name', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, universalism', 'world': {'tribal': 'go back to the far valleys where the faction was first bound, one camp at a time', 'magic': 'campaign in the old market towns where the faction was founded, one by one'}, 'chance': 0.02}),
    ('fight to hold every seat the party already has, street by street', 'R.5 G.5', None, 0.5, '', {'v': 'tradition, stimulation', 'world': {'tribal': 'fight to keep every band that already stands with the faction, hearth by hearth', 'magic': 'fight to hold every seat the faction already has, ward by ward'}, 'chance': 0.75}),
    ('agree a deal in advance with the likely winner, for a say in government', 'U.5 B.5', None, 0.5, '', {'grants': 'coalition building', 'v': 'power, achievement', 'world': {'tribal': "agree with the likeliest chief before the choosing, for a duty at the chief's side", 'magic': "seal a bargain in advance with the likeliest house, for a place on the Crown's council"}, 'chance': 0.75}),
    ('write a manifesto for the long road: ten years, not six weeks', 'U.5 G.5', None, 0.5, '', {'v': 'universalism', 'world': {'tribal': "tell the faction's long plan at the fire: ten summers, not one", 'magic': "write the faction's charter for the long road: ten years, not one season"}, 'chance': 0.75}),
    ('agree with the nearest party not to stand against each other in close seats', 'W.5 B.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'agree with the nearest faction not to stand against each other at the close fires', 'magic': "agree with the nearest faction not to contest each other's close wards"}, 'chance': 0.75}),
    ('debate anyone, anywhere, on live television, and be honest about the odds', 'W.5 R.5', None, 0.5, '', {'grants': 'debating', 'v': 'universalism, stimulation', 'world': {'tribal': 'dispute with any speaker at any fire, and say plainly how the summer stands', 'magic': 'dispute with any rival in any square, and say plainly how the lots stand'}, 'chance': 0.75}),
 ]},
{'name': 'writing in cold for a job in politics',
 'stages': 'young_adult adult mature elder',
 'age': (20, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.004, 0.003, 0.002, 0.001),
 'drivers': 'era+.2 fortune+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'friend, mentor, boss, partner',
 'requires': 'local party officer | data analyst | salesperson | journalist | constituency caseworker',
 'tenure': (1.0, 60.0),
 'worlds': {'earth': 'a job advert, or a name in an article: the people who run the country need writers, '
                     'researchers, organisers and fixers',
            'tribal': "the band's speaker has no one to remember the old sayings, keep the faction's bonds or shape "
                      'his words',
            'magic': 'the faction houses post their wants on the guild hall door: a steward, a rhetor, a scholar of '
                     'statecraft, an advocate'},
 'timing': {'times': "per person a rung below a post in politics (a branch officer or a member's caseworker of a "
                     'year, a data analyst of two with a degree, a salesperson or a journalist of three) a year: '
                     'about 1 in 300 writes in for the post above (estimate, about ten times the real rate on '
                     'purpose); there are about 2,200 think tanks in the US and 500 in the UK (Penn TTCSP 2020) and '
                     'about 12,000 to 13,000 registered US federal lobbyists a year (OpenSecrets), with a few '
                     'hundred speechwriting posts and a few thousand staff to members in a large country (catalogue '
                     'estimates); most posts go to people someone inside vouches for, and a letter from the rung '
                     'below with no one to vouch lands about 1 time in 20 (estimate)',
            'likelier': "a new government hiring, a member newly elected for the person's own town, a skill the "
                        'trade is short of, a friend near power',
            'rarer': 'a government at the end of its term, a hiring freeze after a defeat, no time to write the '
                     'letter',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A job advert in the back of the paper, or a name in an article: the people who run the '
                       'country need writers, researchers, organisers and fixers. {N} has spent years one rung below '
                       "that work: running a branch, taking a member's cases, reporting, selling to the people who "
                       'decide, or building the numbers others quote. The letter would take one evening to write.'),
                      ('W',
                       "There is a proper way to apply for anything, and the party's head office advertises its "
                       'posts like any employer. {N} reads the job description three times, and ticks off every line '
                       'from years of running the branch.'),
                      ('U',
                       '{N} has spent years building the numbers others quote, and has an idea the think tanks have '
                       'missed, with the evidence to back it. A paper sent cold to the right desk might be read, if '
                       'it is good enough.'),
                      ('B',
                       '{N} has spent years selling to the people who decide, and knows that jobs like these are '
                       'rarely advertised. They go to people someone vouches for, and {N} knows someone who knows '
                       'someone.'),
                      ('R',
                       "{N} heard the leader's last big speech and thought, honestly, that it could have been "
                       'better. After years of writing for a living, {N} could write a better one tonight.'),
                      ('G',
                       'The new member for {Ns} town has never lived there. Somebody in that office should know its '
                       "streets, and {N} has learned every one of them through years of other people's cases.")],
            'tribal': [('',
                        'The speaker the band sends to the gathering has no one to remember the old sayings, no one '
                        "to keep the faction's bonds, no singer to shape his words. {N} has carried messages between "
                        'the hearths for many summers, and knows how to do each of those things.')],
            'magic': [('',
                       'The faction houses of the city post their wants on the guild hall door: a steward, a rhetor, '
                       'a scholar of statecraft, an advocate. {N} has no patron in any house, only years of good '
                       'work and a better head. A scryer in the lower town offers to read whether the letter will be '
                       'answered, for a silver piece.')]},
 'outcomes': (['{N} sees it through, and by the end of the season knows more about how the work is really done than '
               'any book could teach.',
               'Something comes of it: a name to call, a door half open, and a reason to keep going.'],
              ['The reply comes in a thin envelope: no, with one sentence of real praise for the work, signed by '
               'someone {N} has seen on television. {N} keeps it in a drawer.',
               'Nothing comes back at all. {N} waits a month, then two, then starts on the next thing, a little '
               'wiser about how such doors open.']),
 'options': [
    ("apply for the post the party's head office advertises, by every form", 'W1', None, 0.45, '', {'title': 'party official', 'requires': 'local party officer', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'conformity, security', 'world': {'tribal': "offer the elders to keep the faction's bonds, and recite every marriage and gift to prove it", 'magic': "apply to a faction's house for its steward's post, by every form"}, 'chance': 0.05}),
    ('send a think tank a paper nobody asked for, and ask for a desk', 'U1', None, 0.45, '', {'title': 'policy analyst', 'requires': 'data analyst', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'aims': 'policy analyst', 'v': 'achievement, self-direction', 'world': {'tribal': 'go to the old speakers and offer to remember what was tried before, and what came of it', 'magic': 'send the academy a treatise on statecraft unasked, and ask for a chair'}, 'chance': 0.05}),
    ('turn years of selling to the right people into a desk at a public affairs firm', 'B1', None, 0.45, '', {'title': 'lobbyist', 'requires': 'salesperson', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'power, achievement', 'world': {'tribal': "turn years of trading with the flint-traders into a go-between's place at the chief's side", 'magic': "turn years of trade with the great houses into an advocate's seat at court"}, 'chance': 0.05}),
    ('write the leader a better speech than the last one, and post it to the office', 'R1', None, 0.45, '', {'title': 'speechwriter', 'requires': 'journalist', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'make the speaker better words than his last, and sing them at his fire unasked', 'magic': "write the faction's head a better oration than the last, and send it unasked"}, 'chance': 0.05}),
    ("offer the town's new member the streets you learned through years of casework", 'G1', None, 0.45, '', {'act': "offer the town's new member the streets they learned through years of casework", 'title': 'political adviser', 'requires': 'constituency caseworker', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'door': True, 'aims': 'political adviser', 'v': 'benevolence, tradition', 'world': {'tribal': "offer to sit behind the band's new speaker as the one who knows every hearth", 'magic': "write to the ward's new member of the Assembly, offering to be the one who knows its lanes"}, 'chance': 0.05}),
    ("work an unpaid month in the local member's office, and learn who decides what", 'B.5 G.5', None, 0.5, '', {'v': 'power, security', 'world': {'tribal': "sit a moon behind the band's speaker unasked for anything, and learn who decides what", 'magic': 'clerk a month unpaid for a member of the Assembly, and learn who decides what'}, 'chance': 0.8}),
    ('knock on doors for a campaign first, where such jobs are really handed out', 'B.5 R.5', None, 0.5, '', {'title': 'campaign volunteer', 'v': 'achievement, stimulation', 'world': {'tribal': 'walk the hearths for a speaker first, where such places are really given', 'magic': "carry a faction's banner through the wards first, where such posts are really handed out"}, 'chance': 0.8}),
    ("write for the local paper on the town's politics, under your own name", 'U.5 G.5', None, 0.5, '', {'v': 'universalism', 'world': {'tribal': 'keep the tales of the council fire, and tell them fairly to anyone who asks', 'magic': "write on the town's quarrels for the broadsheet, under your own name"}, 'chance': 0.8}),
    ('work the polling station on election day, and see how it really runs', 'W.5 R.5', None, 0.5, '', {'title': 'polling-station volunteer', 'v': 'conformity, stimulation', 'world': {'tribal': 'keep the counting stones at the choosing, and see how it really runs', 'magic': 'stand witness at the warded urns, and see how the lots really run'}, 'chance': 0.8}),
    ('take an evening course in public policy, and apply properly next year', 'W.5 U.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'sit with the elders through a winter of council fires, and ask properly next summer', 'magic': "take the academy's evening lectures on statecraft, and apply properly next year"}, 'chance': 0.8}),
 ]},
{'name': 'the campaign loses its organiser',
 'stages': 'young_adult adult mature elder',
 'age': (18, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.008, 0.005),
 'drivers': 'era+.2 unrest+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'boss, colleague, friend, rival',
 'requires': 'campaign volunteer | local party officer',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': "two weeks before polling day the campaign's paid organiser walks out, and the office is in "
                     'chaos',
            'tribal': 'half a moon before the gathering, the young man who walked the valley for the speaker goes '
                      'off to another band',
            'magic': "a fortnight before the lots, the faction house's chief runner takes another house's silver and "
                     'is gone'},
 'timing': {'times': 'per campaign volunteer or local party officer of a year or more, a year: about 1 in 100 is on '
                     'a campaign that loses its organiser, agent or data lead in the last weeks before a vote '
                     '(estimate: staff turn over fast on short campaigns, and most campaigns fall in election '
                     'years); the post nearly always goes to someone the party sends in, and a volunteer who steps '
                     'up keeps it about 1 time in 20 (estimate)',
            'likelier': 'an election called early, a small campaign with one paid organiser, years of loyal work on '
                        'the doorsteps, a candidate who knows the volunteer',
            'rarer': 'a well-funded campaign with staff to spare, a party office close by, no time to spare from '
                     'work or family',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       "Two weeks before polling day the campaign's paid organiser walks out after a row with the "
                       'candidate. The rota is half empty, the leaflets are still in their boxes, and nobody knows '
                       'the password to the canvass data. {N} has knocked on doors for this party for years, and '
                       'everyone in the office is looking at everyone else.'),
                      ('W',
                       'Somebody has to keep the spending log, the imprints on the leaflets and the rota inside the '
                       'rules, or the whole campaign could be challenged. {N} knows those rules better than anyone '
                       'left in the room.'),
                      ('U',
                       'The canvass returns are a mess: three spreadsheets that disagree about the same streets. {N} '
                       'could sort them out in a night, if anyone handed over the password.'),
                      ('B',
                       "The candidate needs someone to run this now, and the party's regional office will take a "
                       'week to send anyone. {N} sees exactly what this moment is worth.'),
                      ('R',
                       'Two weeks, a half-empty rota and a race still there to be won. {N} can feel the pull of it '
                       'already.'),
                      ('G',
                       'The organiser kept a list of residents who rang with problems, and nobody has called them '
                       'back. {N} knows half of those names from the street.')],
            'tribal': [('',
                        'Half a moon before the gathering, the young man who walked the valley for the speaker has '
                        "gone to another band's fire. The hearths have not been visited, the gifts are not counted, "
                        "and the speaker's own kin look at {N}, who has carried his words for many summers.")],
            'magic': [('',
                       "A fortnight before the lots, the faction house's chief runner has taken another house's "
                       'silver and gone. The ward rolls are in disorder, the broadsheets are unprinted, and the '
                       "steward's eyes fall on {N}, who has carried the faction's banner for years.")]},
 'outcomes': (['{N} runs the last two weeks, and whatever the count says, the party asks {N} to stay on.',
               'The office settles around {N} within a day, and the rota fills faster than anyone expected.'],
              ['On Monday the regional office sends in its own organiser, who thanks {N} for holding the fort and '
               'takes back the clipboard. {N} goes out canvassing that evening anyway.',
               'The candidate says no, kindly, in the car park: they need someone the party knows. {N} drives home '
               'past the posters {N} put up, and is back on the doorsteps by the weekend.']),
 'options': [
    ('offer to run the last two weeks strictly by the book: rota, spending log, leaflets', 'W1', None, 0.45, '', {'title': 'campaign organiser', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': "offer the speaker's kin to keep the gifts and the round of hearths in order, by the old custom", 'magic': 'offer the steward to keep the rolls, the silver and every seal in order until the lots'}, 'chance': 0.05}),
    ('rebuild the canvass data overnight, and ask the candidate for the data desk', 'U1', None, 0.45, '', {'title': 'pollster', 'requires': 'data analyst', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, conformity', 'world': {'tribal': 'count overnight which hearths lean which way, and ask to keep the count for the speaker', 'magic': "set the ward tallies straight overnight, and ask the steward for the reckoner's stool"}, 'chance': 0.05}),
    ("ring the candidate before the regional office does, and ask for the organiser's post", 'B1', None, 0.45, '', {'title': 'campaign organiser', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': "go to the speaker before his kin do, and ask to walk the valley in the young man's place", 'magic': "reach the candidate before the faction house does, and ask for the chief runner's place"}, 'chance': 0.05}),
    ('pick up the clipboard, fill the rota by midnight, and simply start running it', 'R1', None, 0.45, '', {'title': 'campaign organiser', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation', 'world': {'tribal': "take up the young man's staff, gather the young hunters by nightfall, and set off down the valley", 'magic': "take up the runner's satchel, rouse the wards by midnight, and simply start"}, 'chance': 0.05}),
    ("call back every resident on the organiser's list, and ask to keep the casework", 'G1', None, 0.45, '', {'title': 'constituency caseworker', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'visit every hearth that sent a trouble to the speaker, and ask to keep carrying them', 'magic': 'call on every petitioner the runner left waiting, and ask to keep the petitions'}, 'chance': 0.05}),
    ("help whoever the party sends in, and keep your own ward's lists in order for them", 'W.25 U.25 B.25 G.25', None, 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': "help whoever the elders send, and keep your own hearths' count ready for them", 'magic': "serve whoever the faction house sends, and keep your own ward's rolls in order for them"}, 'chance': 0.8}),
    ("put forward the organiser from the next seat's campaign, and hold the phones till they come", 'W.25 U.25 B.25 R.25', None, 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'send for the one who walked the next valley for his speaker, and keep the word moving till he comes', 'magic': "send for the runner of the next ward's campaign, and keep the messages moving till they come"}, 'chance': 0.8}),
    ('keep knocking on doors, and leave the running of it to the candidate', 'W.25 U.25 R.25 G.25', None, 0.5, '', {'habit': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'keep walking the hearths, and leave the leading of it to the speaker', 'magic': 'keep carrying the banner door to door, and leave the running of it to the candidate'}, 'chance': 0.8}),
    ('ring round the branch for someone who has run a campaign before', 'W.25 B.25 R.25 G.25', None, 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'ask among the old ones for someone who has walked the valley for a speaker before', 'magic': 'ask round the faction for someone who has run a season of lots before'}, 'chance': 0.8}),
    ('step back: two weeks of this would cost the day job and the family too much', 'U.25 B.25 R.25 G.25', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, self-direction', 'world': {'tribal': 'step back: half a moon of this would cost the hunt and the family too much', 'magic': 'step back: a fortnight of this would cost the workshop and the household too much'}, 'chance': 0.8}),
 ]},
{'name': 'a family about to lose their home',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (18, 75),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'constituency caseworker',
 'worlds': {'earth': 'an eviction notice for Monday lands on your desk, and the family it names is waiting in the '
                     'corridor',
            'tribal': 'the band means to drive a family out over a feud before the next move of camp, and they come '
                      'to you to carry their case to the speaker',
            'magic': "the guild that owns their tenement will throw a family out at the week's end, and they bring "
                     'their petition to your desk'},
 'timing': {'times': 'per constituency caseworker a year: a housing case most weeks, an eviction at short notice '
                     'every month or two; about 1 life in 1,000 works as a caseworker (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       "A family of four waits in the corridor of the member's office with a bailiff's letter: out "
                       'on Monday, three days from now. {N} has the file open and the phone already in hand.'),
                      ('W',
                       'The council has a legal duty to a family made homeless, and {N} knows the paragraph by '
                       'heart. Someone only has to be made to follow it.'),
                      ('U',
                       "The notice is dated oddly, and the landlord's paperwork looks thin. {N} reads it twice, "
                       'looking for the flaw that buys time.'),
                      ('B',
                       "The landlord owns half the street and has never once returned the office's calls. A win here "
                       'would be noticed, and {N} knows how to make it loud.'),
                      ('R',
                       'The father keeps apologising for taking up time. {N} feels the anger rise: three days is '
                       'nothing, and nobody else in the building is going to fight for them.'),
                      ('G',
                       'The family have lived on that street for twenty years, and {N} grew up three streets away. '
                       'Everyone there knows them by name.')]},
 'outcomes': (['The family has a roof before the deadline, close to the street they know.',
               "The people driving the family out give them a month's grace, and by the end of it a new place is "
               'found.'],
              ["The deadline comes, and the family's things are carried out to a friend's shed.",
               'Nobody with the power to stop it will listen, and {N} spends the days knocking on doors that stay '
               'shut.']),
 'options': [
    ('open a homelessness case with the council, and hold it to its legal duty', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'grants': 'constituency casework', 'world': {'tribal': 'ask the elders to hold the band to its custom of sheltering a family in trouble', 'magic': "open a case with the Crown's almoner, and hold the city to its charter"}, 'chance': 0.75}),
    ('comb the notice for the legal flaw that buys the family time', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'ask the old ones whether the feud was ever settled by custom, and hold the band to that', 'magic': "comb the guild's writ for a flaw in its seals that buys the family time"}, 'chance': 0.55}),
    ('ring the landlord and hint that the member can slow his next planning application', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'made an enemy', 'closed': "approval: an office's power used as a threat; backfire: the landlord records the call and sends it to the local paper", 'world': {'tribal': "warn the feuding family's head that the speaker will remember who drove them out", 'magic': "let the guild's steward know that the member sits on the licensing board"}, 'chance': 0.65}),
    ("go round to the landlord's office and argue it out face to face", 'R1', None, 0.45, '', {'v': 'benevolence', 'identity': True, 'world': {'tribal': "walk to the feuding family's hearth and argue it out face to face", 'magic': 'march to the guild hall and argue it out with the steward face to face'}, 'chance': 0.4}),
    ('find the family a room with relatives or neighbours until something better comes', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': "find the family a place at a kinsman's hearth until the quarrel cools"}, 'chance': 0.8}),
    ("use the council's own rules to get them rehoused in the same neighbourhood", 'W1', 'G.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'invoke the custom that a family keeps its place in the camp it was born to', 'magic': "invoke the ward's old charter, so the family is housed in its own parish"}, 'chance': 0.6}),
    ("draft the member's letter so precisely that the council cannot wriggle out of its duty", 'U1', 'W.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': "frame the family's case so exactly that the speaker cannot let it drop", 'magic': "draft the member's sealed letter so precisely that the city cannot evade its duty"}, 'chance': 0.7}),
    ("trade a favour with a friendly housing officer for the landlord's file", 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'trade a gift with the elder who knows the whole story of the feud', 'magic': "trade a favour with a guild clerk for the tenement's ledger"}, 'chance': 0.75}),
    ('tip off the local paper, and make the landlord the story by Sunday', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'mark': 'defied an authority', 'closed': "approval: going to the press without the member's leave; backfire: the member is furious, and the next big case goes to a colleague", 'world': {'tribal': "ask the singers to make a song of the family's wrong before the gathering", 'magic': 'carry the story to the broadsheet printers in the market square'}, 'chance': 0.65}),
    ("gather the neighbours on the family's doorstep for Monday morning", 'G1', 'R.7', 0.5, '', {'v': 'benevolence, universalism', 'binds': True, 'identity': True, 'world': {'tribal': "gather the neighbouring hearths to stand around the family's shelter", 'magic': "gather the lane's neighbours on the tenement steps at dawn"}, 'chance': 0.35}),
 ]},
{'name': 'the same case for the third time',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (18, 75),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'constituency caseworker',
 'worlds': {'earth': 'the same name is back in your inbox, with the same complaint, for the third time this year',
            'tribal': 'the same widow sits at your fire with the same grievance about her share of the hunt, for the '
                      'third time this season',
            'magic': 'the same petition is back on your desk, under a new seal, with the same complaint inside'},
 'timing': {'times': 'per constituency caseworker: most months (estimate)'},
 'scenes': {'earth': [('',
                       'The widow from the estate is back: her payment has been stopped again by the same error, the '
                       'third time this year. She brings a tin of biscuits, and she knows {Ns} name.'),
                      ('W',
                       'Each time, {N} fixes it by the book, and each time the book sends it back. A rule that fails '
                       'the same woman three times is a broken rule.'),
                      ('U',
                       'The same code on the same letter, three times over. {N} begins to suspect the fault is not '
                       'in her file at all, but in the system that reads it.'),
                      ('B',
                       'The office is judged on cases closed, and this one keeps coming back open. {colleague} has '
                       'started passing her to {N} on purpose.'),
                      ('R',
                       '{N} feels a flash of impatience at the sight of her name, and then a flush of shame at the '
                       'flash.'),
                      ('G',
                       'She has had nobody much to talk to since her husband died, and these visits are part of her '
                       'month. {N} has started keeping the good chair free for her.')]},
 'outcomes': (['The fault is found at last, and the money arrives on time three months running.',
               'She comes by to say it is sorted and stays to talk a while, and {N} does not mind at all.'],
              ['The same error comes back in the spring, word for word.',
               "{boss} asks why one person takes up so much of the office's week, and {N} has no good answer."]),
 'options': [
    ('fix it by the book again, and log every step in her file', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'habit': True, 'self_control': '+', 'world': {'tribal': 'put her share right by custom again, and tell the elders each step', 'magic': 'put it right by the rules again, and enter every step in her file'}, 'chance': 0.92}),
    ('trace the error to its source in the benefits system, and report the fault', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'mark': 'learned a skill', 'world': {'tribal': 'trace the quarrel back to the first share that was cut wrong', 'magic': "trace the error back to the clerk's ledger where it began"}, 'chance': 0.45}),
    ('pass her to the newest colleague, and close the file on your own list', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'refused someone in need', 'self_control': '-', 'world': {'tribal': "send her to the youngest of the speaker's helpers, and be free of it", 'magic': 'pass her to the newest clerk, and strike her from your own roll'}, 'chance': 0.95}),
    ('tell her straight that this is the last time the office can do it for her', 'R1', None, 0.45, '', {'v': 'self-direction', 'world': {'tribal': 'tell her straight that this is the last time you will carry it for her', 'magic': 'tell her straight that this is the last petition the office will carry for her'}, 'chance': 0.65}),
    ('put the kettle on and fix it again, as part of the month', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'habit': True, 'self_control': '+', 'grants': 'constituency casework', 'world': {'tribal': 'sit with her by the fire and put it right again, as part of the season', 'magic': 'pour her a cup and put it right again, as part of the month'}, 'chance': 0.92}),
    ('set up a standing arrangement with the benefits office for her and others like her', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'binds': True, 'grants': 'handling red tape', 'world': {'tribal': 'get the hunt leader to set her share aside each time, without her having to ask', 'magic': "get the almoner's office to set her dole aside each quarter, without a fresh petition"}, 'chance': 0.55}),
    ('gather every case with the same error into one complaint to the ombudsman', 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'identity': True, 'world': {'tribal': 'gather every family wronged the same way, and bring them before the elders together', 'magic': 'gather every petition with the same flaw into one plea to the master of rolls'}, 'chance': 0.3}),
    ('get the member to put a written question to the minister and demand the figures', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'have the speaker ask at the gathering, before every band, how the shares are counted', 'magic': 'have the member lay a sealed question before the Assembly and demand the ledgers'}, 'chance': 0.7}),
    ('lose your temper with the benefits office until a manager takes the case', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'self_control': '-', 'world': {'tribal': "storm over to the hunt leader's fire and shout until he puts it right", 'magic': "storm into the almoner's office and shout until the master comes out"}, 'chance': 0.65}),
    ('take her along to the lunch club at the community centre, so the month holds more', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, hedonism', 'binds': True, 'mark': 'helped someone in need', 'world': {'tribal': 'bring her to sit with the old women at the evening fire', 'magic': "bring her to the widows' table at the tavern by the gate"}, 'chance': 0.75}),
 ]},
{'name': 'the leadership wants its favourite selected',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (20, 75),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'boss, colleague, elder',
 'requires': 'party official',
 'worlds': {'earth': "an email from headquarters asks for the leadership's favourite to be chosen for the seat, and "
                     'the rules say the local members choose',
            'tribal': "the faction's head wants his nephew sent to the gathering, and custom says the families "
                      'choose their own speaker',
            'magic': "the faction's lord wants his favourite on the lot for the seat, and the faction's charter says "
                     'the sworn members choose'},
 'timing': {'times': 'per party official a year: about 1 in 5 meet a selection the centre wants to steer; about 1 '
                     'life in 2,000 works for a party (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'The email from headquarters is three lines long: the leadership would be grateful if the '
                       'selection for the seat went to its favourite. The rules {N} keeps say the local members '
                       'choose, by open ballot.'),
                      ('W',
                       '{N} has run forty selections by the rulebook, and the rulebook is the one thing every member '
                       'trusts. Bend it once, and every loser after this will say it was bent again.'),
                      ('U',
                       '{N} reads the rules again, slowly. Three clauses would let the centre shape the shortlist '
                       'without breaking a single one.'),
                      ('B',
                       '{boss} sent the email, and {boss} decides who runs the region next year. The favourite will '
                       'probably win anyway; the only question is what helping is worth.'),
                      ('R',
                       'The members have a candidate of their own, a nurse from the ward who has knocked on doors '
                       'for ten years. {N} feels sick at the thought of telling her the race was over before it '
                       'began.'),
                      ('G',
                       'The branch has picked its own candidates for as long as anyone remembers, and {elder} still '
                       'talks about the one time the centre sent someone in.')]},
 'outcomes': (['The selection goes ahead, and the members accept the result, even those who lost.',
               'Those at the top let the matter drop, and nobody mentions the request again.'],
              ['The losing side cries foul, and the choice has to be made all over again.',
               '{boss} stops asking {N} into the rooms where things are decided, and the reason is plain enough.']),
 'options': [
    ('run the selection by the book, open ballot and all, and tell headquarters so', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'mark': 'defied an authority', 'world': {'tribal': 'hold the choosing by custom, every family heard, and tell the faction head so', 'magic': 'hold the choosing by the charter, every sworn lot counted, and tell the lord so'}, 'chance': 0.75}),
    ('find the clause that lets the centre shape the shortlist without breaking a rule', 'U1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'find the old custom that lets a faction head name who may be chosen', 'magic': 'find the clause in the charter that lets the lord shape the lot'}, 'chance': 0.7}),
    ('ask headquarters, plainly, what delivering the favourite would be worth', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'ask the faction head, plainly, what helping his nephew would be worth', 'magic': "ask the lord's steward, plainly, what the favour would be worth"}, 'chance': 0.7}),
    ("ring the members' own candidate tonight and tell her about the email", 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'mark': 'defied an authority', 'world': {'tribal': "go to the families' own choice tonight and tell her what the faction head wants", 'magic': "send word tonight to the members' own choice about the lord's letter"}, 'chance': 0.95}),
    ('let the branch elders know quietly, and leave them to settle it among themselves', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': "tell the faction's old women quietly, and leave them to settle it", 'magic': "let the ward's oldest members know quietly, and leave them to settle it"}, 'chance': 0.6}),
    ("ask the party's rules committee for a written ruling before doing anything", 'W1', 'U.7', 0.5, '', {'v': 'conformity', 'world': {'tribal': 'ask the oldest keeper of custom how such a choosing was made before', 'magic': "ask the faction's keeper of the charter for a ruling in writing"}, 'chance': 0.65}),
    ('brief headquarters on which branch votes the favourite needs, and how to win them', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'grants': 'a name as a fixer', 'world': {'tribal': 'tell the faction head which families his nephew must win, and how', 'magic': "tell the lord's steward which members the favourite must win, and how"}, 'chance': 0.6}),
    ("strike a deal: the favourite takes this seat, the members' candidate the next", 'B1', 'R.7', 0.5, '', {'v': 'power, benevolence', 'binds': True, 'world': {'tribal': "strike a bargain: the nephew goes this summer, the families' choice the next", 'magic': "strike a bargain: the favourite takes this lot, the members' choice the next"}, 'chance': 0.35}),
    ('read the email aloud at the branch meeting, and let the members decide whether to fight', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'tell the whole camp at the fire what the faction head wants, and let the families decide', 'magic': "read the lord's letter aloud at the ward meeting, and let the members decide"}, 'chance': 0.7}),
    ('shortlist the favourite alone, as the branch always did when the centre asked', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'mark': 'gave in to pressure', 'closed': "approval: a selection fixed against the party's own rules; backfire: a member leaks the emails, and the result is overturned on appeal", 'world': {'tribal': 'put only the nephew forward, as the families always did when a faction head asked', 'magic': 'put only the favourite on the lot, as the ward always did when the lord asked'}, 'chance': 0.8}),
 ]},
{'name': 'the party is broke after the election',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (20, 75),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, colleague, elder',
 'requires': 'party official',
 'worlds': {'earth': 'after the lost election comes the meeting about the overdraft: three months of money left and '
                     'twelve staff on the payroll',
            'tribal': "the faction's stores are gone after the feasting, the cold moons are coming, and the families "
                      'who gave are tired of giving',
            'magic': "the faction's coffer is empty after the lots, and the clerks and heralds still want paying"},
 'timing': {'times': 'per party official: after most lost elections, about one year in four, money and staff are cut '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'The election is lost, and so is the money. The meeting about the overdraft ends with one '
                       'line on the whiteboard: three months left, twelve people on the payroll, and {N} has to say '
                       'who goes.'),
                      ('W',
                       'Every person on that payroll was promised a job through the next campaign, and {N} signed '
                       'half of those letters.'),
                      ('U',
                       '{N} has the figures open: membership fees, small donors, the big ones who went quiet. There '
                       'is a pattern in who stopped giving, and when.'),
                      ('B',
                       'Two big donors have said they will come back if the party changes course. One of them has '
                       '{Ns} private number.'),
                      ('R',
                       '{colleague} has a baby due in March and is on the list. {N} wants to tear the list up and '
                       'find the money anywhere at all.'),
                      ('G',
                       'The party has been broke before, after the last landslide and the one before it. {elder}, '
                       'the old treasurer, says it always comes back, slowly, from the bottom up.')]},
 'outcomes': (['By spring the books balance, and nobody leaves who did not choose to.',
               'The members come through with small sums, and the doors stay open.'],
              ['The money runs out first, and four people are let go in a single afternoon.',
               'The money comes in, and with it a donor who expects a say in everything.']),
 'options': [
    ('cut every post by the same share, so nobody carries more than anyone else', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': "cut every family's share of what is left by the same handful", 'magic': "cut every clerk's wage by the same share, so nobody carries more"}, 'chance': 0.75}),
    ('work out who stopped giving and why, and write to each of them', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'fundraising', 'world': {'tribal': 'work out which families stopped giving, and why, and go to each'}, 'chance': 0.55}),
    ("take the big donor's money, and the strings that come with it", 'B1', None, 0.45, '', {'v': 'power', 'mark': 'gave in to pressure', 'world': {'tribal': "accept the rich family's gifts, and the say over the faction that comes with them", 'magic': "take the merchant prince's gold, and the strings that come with it"}, 'chance': 0.9}),
    ('give up your own salary for a quarter to keep the youngest staff on', 'R1', None, 0.45, '', {'v': 'benevolence', 'identity': True, 'binds': True, 'self_control': '+', 'world': {'tribal': 'give your own share of the stores to keep the youngest helpers fed', 'magic': 'give up your own wage for a season to keep the youngest clerks on'}, 'chance': 0.92}),
    ("close the regional offices, and run the party from members' front rooms", 'G1', None, 0.45, '', {'v': 'tradition', 'identity': True, 'world': {'tribal': "break the faction's big camp into family hearths until the herds come back", 'magic': "give up the faction's town house, and meet in members' kitchens"}, 'chance': 0.75}),
    ('bring in the auditors, and publish every account to the members', 'W1', 'U.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': "lay out every store and every gift before the faction's elders", 'magic': "open the coffer's ledgers to every sworn member"}, 'chance': 0.75}),
    ("sell the party's membership lists to a marketing firm", 'U1', 'B.7', 0.5, '', {'v': 'power, security', 'mark': 'hid a wrong', 'closed': "law: selling members' personal data without their consent; backfire: a regulator's fine, and the story in every paper", 'self_control': '-', 'world': {'tribal': "trade the faction's secrets about who owes whom to a rival clan's go-between", 'magic': "sell the faction's roll of members to a merchant house"}, 'chance': 0.8}),
    ('stage a gala dinner with a famous speaker, and charge what the room can bear', 'B1', 'R.7', 0.5, '', {'v': 'achievement, hedonism', 'grants': 'fundraising', 'world': {'tribal': 'hold a great feast with the best singer in the valley, and ask every guest for a gift', 'magic': 'stage a masked ball at the guild hall with a famous bard, and sell the seats dear'}, 'chance': 0.65}),
    ('ask every member yourself, one by one, for a small gift each month', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'habit': True, 'self_control': '+', 'world': {'tribal': 'walk to every hearth yourself and ask each for a little', 'magic': "knock on every member's door yourself and ask for a few coins each month"}, 'chance': 0.6}),
    ('ask the old treasurer how the party came back last time, and follow the plan', 'G1', 'W.7', 0.5, '', {'v': 'tradition, security', 'world': {'tribal': 'ask the oldest keeper of the stores how the faction came through the last lean winter, and do the same'}, 'chance': 0.7}),
 ]},
{'name': 'a client wants the minister by Friday',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (22, 80),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'friend, boss, colleague',
 'requires': 'lobbyist',
 'worlds': {'earth': 'a client on the phone wants a meeting with the minister by Friday, before the decision on its '
                     'routes',
            'tribal': "the flint-traders want the chief's ear before the gathering ends, and they have brought gifts "
                      'for whoever can get it',
            'magic': "a merchant house wants an audience with the Keeper of the Treasury by the week's end, and it "
                     'pays in gold'},
 'timing': {'times': 'per lobbyist a year: several times; about 1 life in 500 lobbies for a living (catalogue share; '
                     'OpenSecrets: about 12,000 to 13,000 registered US federal lobbyists a year; estimate)'},
 'scenes': {'earth': [('',
                       "The client runs the region's buses, and a new rule on country routes will be decided next "
                       'week. It wants twenty minutes with the minister by Friday, and it is paying {N} for exactly '
                       'that.'),
                      ('W',
                       "There is a proper way to do this: a registered meeting, an agenda, a line in the minister's "
                       'diary for anyone to read. {N} has always done it that way.'),
                      ('U',
                       '{N} knows which official actually drafts the rule, and that official reads evidence, not '
                       'phone calls. One good paper may matter more than twenty minutes of a minister.'),
                      ('B',
                       "{friend}, an old colleague, now works in the minister's private office. One call would do "
                       'it, and everyone in the trade knows it.'),
                      ('R',
                       'Four days and one shot at it: this is the part of the job that still makes {Ns} pulse race.'),
                      ('G',
                       'The buses run through villages {N} grew up near. The client is not wrong that the new rule '
                       'would cut the last route out to them.')]},
 'outcomes': (['The case is heard where it counts before the rule is decided, and the client signs on for another '
               'year.',
               'The client grumbles at first, then agrees that {N} called it right.'],
              ['The week ends with nothing to show, and the client takes its business to a rival.',
               'Word of how {N} went about it goes round the corridors, and two doors close.']),
 'options': [
    ('request the meeting through the official channel, entered in the register', 'W1', None, 0.45, '', {'v': 'conformity', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': "ask leave to speak at the chief's fire, holding up the go-between's token", 'magic': "petition for an audience through the Keeper's own clerks, entered in the court's book"}, 'chance': 0.2}),
    ('send the official who drafts the rule a short paper with the route figures', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': "tell the old hand who carries out the chief's word how the trade paths would be cut", 'magic': "send the Keeper's clerk a short treatise with the road figures"}, 'chance': 0.65}),
    ('ring your old colleague in the private office, and ask for twenty minutes as a favour', 'B1', None, 0.45, '', {'v': 'power', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': "ask your friend at the chief's side for a word in his ear before the fire", 'magic': "send a note to your old fellow clerk at the Keeper's side, and ask for the audience as a favour"}, 'chance': 0.75}),
    ("wait at the minister's Friday surgery, and make the case in person", 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': 'wait by the path the chief walks at dawn, and make the case to his face', 'magic': "wait on the Keeper's stair at the morning bell, and make the case in person"}, 'chance': 0.6}),
    ('bring the village riders to speak, and say nothing of who paid their fares', 'G1', None, 0.45, '', {'v': 'power, universalism', 'mark': 'hid a wrong', 'closed': "approval: a client's campaign passed off as a local one; backfire: a reporter finds out who paid the fares", 'world': {'tribal': 'bring the families of the trade path to speak, and never say the traders sent them', 'magic': 'bring the villagers to speak for the road, and never say the merchant house paid their way'}, 'chance': 0.6}),
    ('tell the client plainly what the rules allow by Friday, and bill for the advice', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'tell the traders plainly what custom allows before the gathering ends, and take a fair gift for it', 'magic': "tell the merchant house plainly what the court's rules allow, and send the bill"}, 'chance': 0.75}),
    ('write a sharp piece for the morning papers that puts the village route on every table', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'give the singers a sharp verse about the cut path, to sing at every fire', 'magic': 'write a sharp broadsheet that puts the village road in every tavern'}, 'chance': 0.4}),
    ('make the client promise to keep the village routes, as the price of your help', 'B1', 'G.7', 0.5, '', {'v': 'power, benevolence', 'binds': True, 'world': {'tribal': 'make the traders promise to keep the old path open, as the price of your help', 'magic': 'make the merchant house promise to keep the village road, as the price of your help'}, 'chance': 0.6}),
    ("argue with the client's board until it agrees to make its case in public", 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'argue with the traders until they agree to plead openly at the fire', 'magic': "argue with the merchant house's elders until they agree to plead openly in the Assembly"}, 'chance': 0.55}),
    ('ask the parish councils and the drivers who rides the route, and when', 'G1', 'U.7', 0.5, '', {'v': 'universalism, tradition', 'world': {'tribal': 'ask the families along the trade path how often they walk it, and for what', 'magic': "ask the carters' guild and the village elders who rides the road, and how often"}, 'chance': 0.9}),
 ]},
{'name': 'an old colleague now decides',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (22, 80),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'friend, colleague, boss',
 'requires': 'lobbyist',
 'worlds': {'earth': "a former colleague's name is in the new appointments, and the friend you shared an office with "
                     "now decides your client's case",
            'tribal': "the hunter you grew up with is now the chief's speaker, and the flint-traders you plead for "
                      'want you at his fire tomorrow',
            'magic': 'your old fellow clerk is now a councillor of the Crown, and the merchant house you serve wants '
                     'you at his door by morning'},
 'timing': {'times': "per lobbyist a year: about 1 in 5 find a former colleague in a post that decides a client's "
                     'case, most often after a change of government (estimate)'},
 'scenes': {'earth': [('',
                       'The new appointments are out, and {friend}, who shared {Ns} old office for six years, now '
                       'signs off the very decision {Ns} biggest client is waiting on. A message arrives within the '
                       'hour: drinks soon, like old times?'),
                      ('W',
                       'There are rules for exactly this: declare the friendship, keep every contact on the record, '
                       'let someone else handle the client if need be.'),
                      ('U',
                       '{N} knows how {friend} thinks, which papers {friend} reads first, which arguments land. That '
                       'knowledge is worth more than any favour, and it is perfectly legal.'),
                      ('B',
                       'In this trade a friend in the right chair is the whole game. The client knows it too; it '
                       'hired {N} partly for the address book.'),
                      ('R',
                       '{N} likes {friend}, truly likes them, and the thought of turning the friendship into a sales '
                       'call sits badly.'),
                      ('G',
                       'Six years of shared lunches and leaving cards. {N} would rather keep the friend than win the '
                       'case.')]},
 'outcomes': (['The case is decided on its merits, and the friendship comes through intact.',
               'The client stays, and {friend} says later that {N} handled it exactly right.'],
              ['The client moves its business to a firm with fewer scruples, or better friends.',
               '{friend} hears what was said behind closed doors, and the old warmth cools.']),
 'options': [
    ('declare the friendship to your firm, and hand the client to a colleague', 'W1', None, 0.45, '', {'v': 'conformity', 'identity': True, 'self_control': '+', 'world': {'tribal': 'tell the traders of the old bond, and send another go-between to the fire', 'magic': 'declare the old friendship to the house, and send another advocate to the councillor'}, 'chance': 0.92}),
    ('write a case that would win on any desk, and file it the usual way', 'U1', None, 0.45, '', {'v': 'achievement', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': "set the traders' case out so plainly that any speaker would take it, and bring it the usual way", 'magic': 'write a petition so sound it would win at any desk, and file it through the usual door'}, 'chance': 0.55}),
    ('go for the drinks, and make the case over the second glass', 'B1', None, 0.45, '', {'v': 'power, hedonism', 'habit': True, 'mark': 'hid a wrong', 'closed': 'approval: lobbying an official off the record; backfire: a photograph of the two of them turns up in a gossip column', 'self_control': '-', 'requires': 'registered lobbyist', 'without': 'law', 'world': {'tribal': 'share a meal at his fire, and make the case over the meat', 'magic': "share a bottle at the tavern by the councillor's gate, and make the case over the second cup"}, 'chance': 0.7}),
    ('go for the drinks, enjoy the evening, and never once mention work', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'sit at his fire for the night, laugh about the old hunts, and never mention the traders', 'magic': 'drink with him at the old tavern, and never once mention the house'}, 'chance': 0.95}),
    ('stay away until the case is decided, and pick the friendship up after', 'G1', None, 0.45, '', {'v': 'tradition', 'self_control': '+', 'world': {'tribal': 'keep away from his fire until the gathering decides, and sit with him after'}, 'chance': 0.9}),
    ('ask the ethics office for a ruling, then work the case inside it', 'W1', 'B.7', 0.5, '', {'v': 'conformity', 'world': {'tribal': 'ask the elders what custom allows between old friends, then plead inside it', 'magic': "ask the court's warden of conduct for a ruling, then work the case inside it"}, 'chance': 0.7}),
    ('build a clean wall between yourself and the case, and see your friend freely', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, benevolence', 'binds': True, 'world': {'tribal': "let another go-between carry the traders' gifts, so you can sit at his fire freely", 'magic': "wall yourself off from the house's petition, so you can see your friend freely"}, 'chance': 0.75}),
    ('trade stepping back from the case for a long, steady contract with your firm', 'B1', 'G.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'trade stepping back for a steady share of flint from the traders each season', 'magic': 'trade stepping back for a long, steady retainer from the house'}, 'chance': 0.55}),
    ('tell the client to its face that the friendship is not for sale', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'mark': 'made an enemy', 'world': {'tribal': 'tell the traders to their faces that the old bond is not for trade', 'magic': 'tell the merchant house to its face that the friendship is not for sale'}, 'chance': 0.65}),
    ('wait a season, watch how your friend runs the new post, and learn its ways', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'world': {'tribal': 'wait a moon, watch how he keeps the new duty, and learn his ways'}, 'chance': 0.7}),
 ]},
{'name': 'the report the funders will not like',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 85),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor',
 'requires': 'policy analyst',
 'worlds': {'earth': "your draft report says the scheme your institute's biggest funder loves does not work, and the "
                     "funder's email asks when it will be ready",
            'tribal': 'the elders ask what happened the last time the band split, and the true answer will anger the '
                      'families who asked',
            'magic': "the academy's patron paid for a treatise on his favourite scheme, and your findings say it "
                     'fails'},
 'timing': {'times': 'per policy analyst a year: about 1 in 5; about 1 life in 500 works as a policy analyst '
                     '(catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       "Eight months of work, and the numbers are clear: the job scheme the institute's biggest "
                       "funder champions has made no difference at all. The funder's email asks, warmly, when the "
                       'report will be out.'),
                      ('W',
                       "The institute's charter says findings are published whatever they show. {N} helped write "
                       'that line.'),
                      ('U',
                       '{N} checks the method one more time, half hoping for an error, and finds none. A null '
                       'result, done properly, is still a result.'),
                      ('B',
                       'The funder pays a third of the salaries, {Ns} own among them. {boss} has started dropping by '
                       'to ask how the draft reads.'),
                      ('R',
                       '{N} feels the old stubbornness rise: eight months of honest work, and someone wants it '
                       'softened before anyone has read it.'),
                      ('G',
                       'The scheme runs in towns {N} knows, and the people in it believe in it. Bad news lands on '
                       'real streets.')]},
 'outcomes': (['The report comes out, the method holds, and the funder asks what would work instead.',
               'The findings stand up to every challenge, and {Ns} name is now the one people quote.'],
              ['The funder pulls a third of the budget at the next review, and two posts go with it.',
               'The draft leaks early, and the story is the quarrel, not the findings.']),
 'options': [
    ("publish the findings in full, as the institute's charter requires", 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'identity': True, 'world': {'tribal': 'tell the whole story at the fire, as the elders asked, every part of it', 'magic': "publish the whole treatise, as the academy's charter requires"}, 'chance': 0.7}),
    ('run the analysis every other way you can, to be sure before anyone sees it', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'ask every old one who remembers the split, to be sure before speaking', 'magic': 'test the findings against every ledger in the archive, to be sure before anyone sees them'}, 'chance': 0.85}),
    ('warn the funder privately first, and offer a follow-up study on what would work', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'warn the families who asked before the fire, and offer to find out what would have held the band together', 'magic': 'warn the patron privately first, and offer him a second treatise on what would work'}, 'chance': 0.75}),
    ('send the draft to the funder with a blunt note: these are the numbers', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'world': {'tribal': 'tell the families straight out what happened, before the elders can soften it', 'magic': 'send the patron the draft with a blunt note: these are the findings'}, 'chance': 0.6}),
    ('let the report wait until the funding round is safely over', 'G1', None, 0.45, '', {'v': 'security, tradition', 'mark': 'hid a wrong', 'closed': "approval: holding back findings to keep a funder; backfire: a study elsewhere finds the same and asks in public why the institute's report never came out", 'self_control': '-', 'world': {'tribal': 'let the story wait until the families have settled for the winter', 'magic': "let the treatise wait until the patron's grant is renewed"}, 'chance': 0.92}),
    ('brief the funder in person before publication, and take the anger in the room', 'W1', 'R.7', 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'go to the families who asked before the fire, and take their anger at your own hearth', 'magic': 'brief the patron in person before the treatise goes out, and take his anger'}, 'chance': 0.65}),
    ('add what the people in the scheme said, so the report shows what did help them', 'U1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'add what the families who left said, so the story shows what held them', 'magic': 'add what the people in the scheme said, so the treatise shows what did help them'}, 'chance': 0.7}),
    ('line up a second funder first, so the institute can publish without fear', 'B1', 'W.7', 0.5, '', {'v': 'security, achievement', 'self_control': '+', 'world': {'tribal': 'win over a second family first, so the story can be told without fear', 'magic': 'find a second patron first, so the academy can publish without fear'}, 'chance': 0.2}),
    ('post the method openly, and challenge anyone to find the flaw', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'tell how you know it at the fire, and dare anyone to prove it wrong', 'magic': 'nail the method to the academy door, and dare any scholar to break it'}, 'chance': 0.65}),
    ('quietly warn the towns running the scheme, so they can plan before the news', 'G1', 'B.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'quietly warn the families who would be hurt, so they can make ready', 'magic': 'quietly warn the towns running the scheme, so they can plan before the treatise lands'}, 'chance': 0.75}),
 ]},
{'name': 'a party takes your idea and twists it',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 85),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, rival',
 'requires': 'policy analyst',
 'worlds': {'earth': "your idea is in a party leader's speech on the news, turned inside out",
            'tribal': 'a speaker at the fire uses your old story of the great drought to argue the very opposite of '
                      'its lesson',
            'magic': 'a faction quotes your treatise in the Assembly to justify the decree it was written to warn '
                     'against'},
 'timing': {'times': 'per policy analyst a year: about 1 in 10 see an idea of theirs taken up and changed by a party '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'A party leader stands at a podium and announces a plan built on {Ns} paper, word for word in '
                       'places, aimed at the opposite of what the paper found.'),
                      ('W',
                       'The paper was written for anyone to use; that is the point of public research. Using it to '
                       'say the opposite of what it found is not using it.'),
                      ('U',
                       '{N} rereads the paper. One table, taken alone, can be read their way. That is partly {Ns} '
                       'own fault.'),
                      ('B',
                       "{Ns} phone has not stopped: two papers want a comment, and a minister's office wants a "
                       'meeting. Being twisted is also being noticed.'),
                      ('R',
                       '{N} watches the clip twice with clenched fists. That is not what the work said, and now '
                       'everyone will think it did.'),
                      ('G',
                       'Ideas leave home like grown children and go where they will. {N} wrote it for the towns that '
                       'needed it, not for a podium.')]},
 'outcomes': (['The record is set straight, and the next time the idea is quoted, it is quoted right.',
               'The fuss passes, and {N} comes out of it with a fuller diary and a clearer paper.'],
              ['The twisted version sticks, and {Ns} name is now tied to a plan {N} believes will do harm.',
               '{boss} asks {N} to stop talking in public, and the institute stays silent.']),
 'options': [
    ("write to the party asking for a correction, quoting the paper's actual findings", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders to make the speaker take back what he said of the story', 'magic': 'petition the faction in writing for a correction, quoting the treatise'}, 'chance': 0.15}),
    ('publish a short note setting out what the paper does and does not show', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'identity': True, 'world': {'tribal': 'tell the drought story again at the next fire, all of it this time', 'magic': 'post a short gloss on the academy door: what the treatise does and does not say'}, 'chance': 0.92}),
    ('ask the party for a post advising it, and steer the idea back from inside', 'B1', None, 0.45, '', {'v': 'power, achievement', 'door': True, 'aims': 'political adviser', 'world': {'tribal': 'ask the speaker for a place behind him at the fire, and steer him from there', 'magic': "ask the faction for a secretary's post, and steer the decree from inside"}, 'chance': 0.2}),
    ('go on the evening news and say plainly that they have it backwards', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'stand up at the fire and say in front of everyone that he has it backwards', 'magic': 'climb the steps of the Assembly square and tell the crowd they have it backwards'}, 'chance': 0.6}),
    ('let it pass; the work will outlast the speech', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.7}),
    ("ask the institute's board for a formal statement, then speak freely yourself", 'W1', 'R.7', 0.5, '', {'v': 'conformity, self-direction', 'world': {'tribal': 'ask the elders to speak first, then say your piece freely at the fire', 'magic': "ask the academy's masters for a formal statement, then speak freely yourself"}, 'chance': 0.6}),
    ('rewrite the idea as a plain guide for the towns it was meant for', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'grants': 'drafting policy', 'world': {'tribal': 'turn the story into a plain rule of thumb the bands can use in a dry year', 'magic': 'rewrite the treatise as a plain primer for the towns it was meant for'}, 'chance': 0.7}),
    ('offer every other party the same briefing, so no one owns the idea', 'B1', 'W.7', 0.5, '', {'v': 'power, universalism', 'world': {'tribal': "tell the story to every faction's elders, so no one family owns it", 'magic': 'brief every faction in the Assembly alike, so no one owns the idea'}, 'chance': 0.65}),
    ("challenge the party's spokesman to a public debate on what the data say", 'R1', 'U.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'challenge the speaker to tell both versions of the story side by side at the fire', 'magic': "challenge the faction's rhetor to a disputation in the academy hall"}, 'chance': 0.3}),
    ("work quietly with the party's local people, who know the towns, to steer the plan", 'G1', 'B.7', 0.5, '', {'v': 'power, benevolence', 'world': {'tribal': "work quietly with the speaker's own kin, who know the land, to turn him", 'magic': "work quietly with the faction's ward wardens, who know the streets, to steer the decree"}, 'chance': 0.5}),
 ]},
{'name': 'the line the leader will not say',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, friend',
 'requires': 'speechwriter',
 'worlds': {'earth': 'the draft comes back with one line struck through twice: the honest one, and the best you have '
                     'written',
            'tribal': 'the speaker refuses the words you gave him for the gathering, the ones about the hunt that '
                      'failed',
            'magic': "the lord strikes your best line from the oration, the one that admits the city's debt"},
 'timing': {'times': 'per speechwriter a year: several times; about 1 life in 5,000 writes speeches for a living '
                     '(catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'The draft comes back at six with one line struck through twice: the sentence that admits the '
                       'plan has failed and says what comes next. In the margin {boss} has written two words: not '
                       'this.'),
                      ('W',
                       'The line is true, and the people listening deserve to hear it from the one who made the '
                       'promise. {N} wrote it as a duty, not a flourish.'),
                      ('U',
                       'Without that line, the next three paragraphs answer a question nobody asked. {N} sees '
                       'exactly where the speech now breaks.'),
                      ('B',
                       'The reasons are not hard to guess: the line is a gift to every opponent with a camera. {N} '
                       'has a career to think about as well.'),
                      ('R',
                       'It is the best line {N} has ever written, and it was struck out with two angry strokes of a '
                       'pen. {N} reads it aloud anyway, alone, and it still rings.'),
                      ('G',
                       'Plain words, the kind people back home say over the garden fence. {N} put them in because '
                       'the speech needed one moment like that.')]},
 'outcomes': (['The speech lands, and the hall listens all the way to the end.',
               'A truer version of the line survives, and it is the one people repeat afterwards.'],
              ['The speech goes out flat, and the commentators call it evasive.',
               '{boss} is cool with {N} for a week, and the next draft goes to someone else.']),
 'options': [
    ('accept the cut; the words belong to the one who says them', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'let the words go; the speaker carries his own words to the gathering', 'magic': 'accept the cut; the oration belongs to the lord'}, 'chance': 0.65}),
    ('rebuild the next three paragraphs so the speech holds together without it', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'reshape the rest of the words so they hold together without it'}, 'chance': 0.8}),
    ('keep the struck line in a drawer for the day it is worth something', 'B1', None, 0.45, '', {'v': 'power', 'self_control': '+', 'world': {'tribal': 'keep the refused words in your memory for a day they will be worth something'}, 'chance': 0.95}),
    ('leak the struck line to a journalist friend, because it deserves to be heard', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'mark': 'broke your word', 'closed': "approval: a leader's private draft handed to the press; backfire: the leak is traced to the only copy, and the job goes with it", 'self_control': '-', 'world': {'tribal': 'teach the refused words to a singer, so they reach the fires anyway', 'magic': 'slip the struck line to a broadsheet writer, so it reaches the taverns anyway'}, 'chance': 0.85}),
    ('find a gentler, plainer way to say the same truth, and send it back', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'chance': 0.6}),
    ('keep the line in the printed text, and let the leader skip it aloud', 'W1', 'G.7', 0.5, '', {'v': 'conformity, tradition', 'world': {'tribal': 'ask the elders to remember the words, even if the speaker will not say them', 'magic': 'keep the line in the written copy for the archive, and let the lord skip it aloud'}, 'chance': 0.55}),
    ('show the leader the evidence that voters reward a plain admission', 'U1', 'W.7', 0.5, '', {'v': 'achievement, universalism', 'world': {'tribal': 'remind the speaker what the old ones say of a speaker who hides a failed hunt', 'magic': 'show the lord what the tallies say of rulers who own their mistakes'}, 'chance': 0.35}),
    ('trade the line for a promise that the leader will say it next month', 'B1', 'U.7', 0.5, '', {'v': 'power', 'binds': True, 'world': {'tribal': "trade the words for the speaker's promise to say them at the next fire"}, 'chance': 0.45}),
    ('fight for the line in the meeting until the leader gives way', 'R1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'identity': True, 'grants': 'a name for straight talk', 'world': {'tribal': "go to the speaker's fire and argue for the words until he gives way", 'magic': "climb to the lord's study and argue for the line until he gives way"}, 'chance': 0.2}),
    ('ask the people the plan failed, and give the leader one sentence in their own words', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'ask the families of the failed hunt, and give the speaker one saying of their own', 'magic': 'ask the people of the lower wards, and give the lord one sentence of theirs'}, 'chance': 0.55}),
 ]},
{'name': 'the speech is due at midnight',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, colleague, friend',
 'requires': 'speechwriter',
 'worlds': {'earth': 'at eight in the evening the document is still empty, and the speech is due at midnight',
            'tribal': 'the gathering is at dawn, and the words the speaker will carry there are not ready',
            'magic': 'the oration is at the morning bell, and the page on your desk is still blank'},
 'timing': {'times': 'per speechwriter: most months (estimate)'},
 'scenes': {'earth': [('',
                       'At eight in the evening the document is empty except for a title. The speech is due at '
                       'midnight, the leader speaks at nine tomorrow, and {friend} has sent two messages about '
                       'dinner.'),
                      ('W',
                       'The leader promised the hall something specific, and the speech must keep that promise and '
                       'no more. {N} starts with the promise.'),
                      ('U',
                       '{N} lays out the bones first: three points, one story, one ask. The words come easier once '
                       'the skeleton is right.'),
                      ('B',
                       'Two other writers pitched for this speech, and {N} won it. A good one tonight means the big '
                       'autumn speech too.'),
                      ('R',
                       'Panic first, then the rush: {N} turns the music up and types the opening in one breath.'),
                      ('G',
                       "{N} goes back to the notes from last month's visit to the market town, and the stallholders' "
                       'own words.')]},
 'outcomes': (['The draft lands at five to midnight, and the leader changes only three words.',
               'The speech brings the hall to its feet, and one line is everywhere the next day.'],
              ['The draft is late, and the leader reads a version {colleague} finished in the small hours.',
               'The speech goes out on time and falls flat; nobody quotes a word of it.']),
 'options': [
    ('start from the promise the leader made, and build every paragraph to keep it', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'start from the promise the speaker made, and shape every saying to keep it'}, 'chance': 0.75}),
    ('outline the argument first, then write to the outline until it is done', 'U1', None, 0.45, '', {'v': 'achievement', 'habit': True, 'self_control': '+', 'world': {'tribal': 'lay out the bones of the words first, then fill them in until dawn'}, 'chance': 0.85}),
    ("pull the best paragraphs from the leader's old speeches, and stitch them into a new one", 'B1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': "gather the best of the speaker's old sayings, and weave them into new words", 'magic': "pull the best passages from the lord's old orations, and stitch them into a new one"}, 'chance': 0.9}),
    ('write the whole thing in one wild burst, and fix it after eleven', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'grants': 'writing speeches', 'world': {'tribal': 'say the whole thing out loud in one wild burst, and mend it after moonrise'}, 'chance': 0.8}),
    ('walk round the block in the dark, and let the first line come on its own', 'G1', None, 0.45, '', {'v': 'tradition, hedonism', 'world': {'tribal': 'walk down to the river in the dark, and let the first words come on their own', 'magic': 'walk the city walls in the dark, and let the first line come on its own'}, 'chance': 0.6}),
    ("ring the leader's office to ask what the people in the hall most need to hear", 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': "go to the speaker's kin, and ask what the families most need to hear", 'magic': "send a runner to the lord's steward, and ask what the hall most needs to hear"}, 'chance': 0.75}),
    ('check every figure in the draft twice before sending it', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'go over every claim in the words twice with the old ones before dawn', 'magic': 'check every figure in the oration twice before the copy goes'}, 'chance': 0.95}),
    ('lift a paragraph from a little-known old speech, and hope nobody checks', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'mark': 'hid a wrong', 'closed': 'approval: lines lifted from another speaker; backfire: a reporter spots the borrowed paragraph the next morning', 'self_control': '-', 'world': {'tribal': 'borrow the words of a dead speaker from a far band, and hope nobody knows them', 'magic': 'lift a passage from an old oration in the archive, and hope nobody has read it'}, 'chance': 0.8}),
    ('stay up until three to make it the best speech of the year', 'R1', 'B.7', 0.5, '', {'v': 'achievement, power', 'self_control': '+', 'world': {'tribal': 'stay up through the night to make it the best speech the gathering has heard'}, 'chance': 0.65}),
    ('read the draft aloud to a friend, and keep what makes them feel something', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'say the words aloud to a friend by the fire, and keep what stirs them', 'magic': 'read the draft aloud to a friend by candlelight, and keep what stirs them'}, 'chance': 0.7}),
 ]},
{'name': 'the poll that says your client is losing',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'pollster',
 'worlds': {'earth': "the new poll on your screen says the client's candidate is eight points behind, and the client "
                     'sees the slides at nine',
            'tribal': 'you have listened at every hearth, and the band will not send your speaker again; he expects '
                      'to hear it from you at the fire tonight',
            'magic': "the guild tallies show your patron's faction falling, and he wants the numbers on his desk by "
                     'the morning bell'},
 'timing': {'times': 'per pollster a year: about 1 in 2 deliver numbers a client does not want, in any year with an '
                     'election; about 1 life in 2,000 works as a pollster (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       "The numbers came in at midnight: the client's candidate is eight points behind with three "
                       'weeks to go. The client wants the slides by nine, and has said twice already that the last '
                       'poll was a fluke.'),
                      ('W',
                       'The client pays for the truth, whether it knows it or not. {N} has never changed a number to '
                       'please anyone.'),
                      ('U',
                       '{N} checks the sample, the weights and the wording of every question. The method is sound: '
                       'eight points, give or take three.'),
                      ('B',
                       "This client is a third of the firm's income, and a client who hears bad news often goes "
                       'looking for a new pollster.'),
                      ('R',
                       'A jolt goes through {N}: this is the poll people will remember, one way or the other, after '
                       'election night.'),
                      ('G',
                       '{N} has run focus groups in these towns for years. The numbers say what the people in those '
                       'rooms have been saying since spring, in plainer words.')]},
 'outcomes': (['The client hears it out, changes course, and the gap starts to close.',
               'The numbers stand, and the client trusts {Ns} word more than before.'],
              ['The client calls the poll wrong and stops answering.',
               'The gap stays where it was, and the client blames the messenger.']),
 'options': [
    ('present the numbers exactly as they are, margin of error and all', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'tell the speaker exactly what the hearths said, word for word', 'magic': 'lay the tallies before the patron exactly as they are'}, 'chance': 0.7}),
    ('quietly adjust the weights until the gap looks like four points', 'U1', None, 0.45, '', {'v': 'power, security', 'mark': 'hid a wrong', 'closed': "approval: numbers bent to please a client; backfire: the result lands eight points out, and the firm's name goes with it", 'self_control': '-', 'world': {'tribal': 'tell the speaker the hearths are wavering, when they have already turned', 'magic': 'trim the tallies until the fall looks gentle'}, 'chance': 0.92}),
    ('tell the client the gap can be closed, and sell it the study that shows how', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'tell the speaker the families can still be won, and offer to find out how, for a gift', 'magic': 'tell the patron the fall can be stopped, and sell him the deeper tally that shows how'}, 'chance': 0.7}),
    ('ring the client tonight and say it plainly before the meeting', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'world': {'tribal': "go to the speaker's fire now, before the evening gathering, and say it plainly", 'magic': "go to the patron's house tonight and say it plainly"}, 'chance': 0.9}),
    ('trust the long trend over one poll, and tell the client to hold its nerve', 'G1', None, 0.45, '', {'v': 'tradition, security', 'self_control': '+', 'world': {'tribal': "trust what the hearths have said all season over one evening's talk, and tell the speaker to hold firm"}, 'chance': 0.45}),
    ("publish the full tables, as the pollsters' code asks, whatever the client prefers", 'W1', 'U.7', 0.5, '', {'v': 'universalism, conformity', 'identity': True, 'mark': 'broke your word', 'closed': "approval: a client's private poll made public; backfire: the client sues for breach of contract", 'world': {'tribal': 'tell the elders openly what you heard at the hearths, as custom asks', 'magic': "post the full tallies at the guild hall, as the guild's code asks"}, 'chance': 0.7}),
    ('show the client which voters moved and why, so the poll becomes a plan', 'U1', 'B.7', 0.5, '', {'v': 'achievement', 'grants': 'reading the polls', 'world': {'tribal': 'show the speaker which hearths turned and why, so he knows where to go', 'magic': 'show the patron which wards turned and why, so the tallies become a plan'}, 'chance': 0.7}),
    ('push the client to spend everything on a last fortnight of rallies', 'B1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'push the speaker to feast every band in the valley before the gathering', 'magic': 'push the patron to spend his whole coffer on a fortnight of processions'}, 'chance': 0.45}),
    ('drive out to the swing town, and knock on doors to hear it firsthand', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'door': True, 'body': 'light', 'world': {'tribal': 'walk out to the far hearths yourself, and sit with the families', 'magic': 'ride out to the river ward, and listen in its taverns yourself'}, 'chance': 0.75}),
    ('tell the client what the people in the focus groups said, in their own words', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'tell the speaker what the families said, in their own words', 'magic': 'tell the patron what the people in the taverns said, in their own words'}, 'chance': 0.65}),
 ]},
{'name': 'the night the exit poll lands',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (21, 80),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'colleague, rival, boss',
 'requires': 'pollster',
 'worlds': {'earth': 'election night in the studio: the exit poll goes out at ten, with your name on it',
            'tribal': 'the night the gathering casts its pebbles, and the whole valley will learn whether your ear '
                      'was true',
            'magic': 'the night the urns are opened in the square, and your tallies are cried before the count'},
 'timing': {'times': 'per pollster: once a national election, about every four years (estimate)'},
 'scenes': {'earth': [('',
                       "Ten o'clock, election night. The exit poll {N} built goes out live to the whole country, and "
                       'for the next six hours every real result will be held up against it.'),
                      ('W',
                       'The exit poll belongs to the public, not to any party: one number, honestly made, read out '
                       'at ten. {N} has signed off every step.'),
                      ('U',
                       'Eleven thousand interviews at a hundred and forty polling stations, and a model built over '
                       'four years. {N} has rehearsed every way it could go wrong.'),
                      ('B',
                       'If the poll is right, {N} will be the name every editor rings for years. If it is wrong, '
                       '{rival} at the other firm will be on air by midnight saying so.'),
                      ('R',
                       "The studio lights, the countdown, the presenter's hand raised: {Ns} heart pounds like a "
                       'drum.'),
                      ('G',
                       'Somewhere out there, people who never think about polls are walking home from the polling '
                       'stations in the dark. The number is theirs.')]},
 'outcomes': (['By three in the morning the results match the exit poll within a seat or two.',
               "The presenter thanks {N} on air, and the firm's phones ring all the next week."],
              ['The first big result lands far from the poll, and the whole studio turns to look at {N}.',
               '{rival} is on another channel by midnight, explaining what went wrong with {Ns} numbers.']),
 'options': [
    ('stand by the published figure all night, whatever the first results do', 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '+', 'world': {'tribal': 'stand by your word all night, whatever the first pebbles show', 'magic': 'stand by the cried tallies all night, whatever the first urns show'}, 'chance': 0.75}),
    ('watch the first real results against the model, and say early which way it leans', 'U1', None, 0.45, '', {'v': 'achievement', 'identity': True, 'world': {'tribal': 'watch the first pebbles fall against what you heard, and say early which way it leans', 'magic': 'watch the first urns against your tallies, and say early which way it leans'}, 'chance': 0.7}),
    ('make sure every editor in the building has your card before midnight', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': "make sure every band's elders know your name before the pebbles are counted", 'magic': 'make sure every broadsheet writer in the square knows your name before midnight'}, 'chance': 0.92}),
    ('tell a friend the number before the polls close; it is too good to keep', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'mark': 'broke your word', 'closed': 'law: an exit poll told before the polls close; backfire: the friend posts it, and the regulator opens a case', 'self_control': '-', 'world': {'tribal': 'whisper what you heard to a friend before the pebbles are cast', 'magic': 'whisper the tallies to a friend before the urns are sealed'}, 'chance': 0.95}),
    ('sit back, and let the night come in result by result', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'sit back, and let the night come in heap by heap', 'magic': 'sit back, and let the night come in urn by urn'}, 'chance': 0.8}),
    ('explain the margin of error on air in words anyone can follow', 'W1', 'U.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'tell the gathered bands plainly how far your ear can be trusted', 'magic': 'tell the crowd in the square plainly how far the tallies can be trusted'}, 'chance': 0.75}),
    ('spot the first sign of a miss, and quietly adjust the projection before anyone else', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'spot the first sign that your ear was wrong, and change your word before anyone notices', 'magic': 'spot the first sign of a miss, and quietly mend the tallies before anyone else'}, 'chance': 0.45}),
    ('challenge the rival firm on air to a bet on whose numbers end closer', 'B1', 'R.7', 0.5, '', {'v': 'stimulation, power', 'identity': True, 'world': {'tribal': "wager a fine blade with the rival band's ear on whose word proves truer", 'magic': "wager a purse with the rival house's tallier on whose numbers prove closer"}, 'chance': 0.4}),
    ('slip out of the studio to the count, and watch it with the volunteers', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'slip away from the elders, and sit with the pebble-keepers by the fire', 'magic': 'slip out to the square, and watch the urns opened with the witnesses'}, 'chance': 0.9}),
    ('thank the interviewers on air, the ones who stood at the stations all day', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'identity': True, 'world': {'tribal': 'thank the listeners who walked to every hearth, in front of the whole gathering', 'magic': 'thank the runners who stood at the urns all day, in front of the crowd'}, 'chance': 0.65}),
 ]},
{'name': 'a door slammed in your face',
 'stages': 'child juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'moment',
 'roles': 'friend, colleague, elder',
 'requires': 'campaign volunteer',
 'worlds': {'earth': 'on a wet evening of canvassing, a door slams in your face halfway through your first sentence',
            'tribal': 'a hearth turns its back on you as you begin to speak for your speaker, and the next hearth is '
                      'watching',
            'magic': "a door in the lower wards is shut in your face before you can finish the faction's greeting"},
 'timing': {'times': 'per campaign volunteer: several times on any evening of canvassing; about 8 lives in 100 '
                     'volunteer (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       "A wet evening, the fourteenth door of the street. {N} gets as far as the candidate's name, "
                       'and the door slams so hard the letterbox rattles.'),
                      ('W',
                       'The clipboard has forty doors on it, and the campaign is counting on every one being '
                       'knocked. One slammed door does not change the job.'),
                      ('U',
                       '{N} marks the door on the sheet and wonders what went wrong: the opening line, the rosette, '
                       'the hour, or only the rain.'),
                      ('B',
                       'The candidate is two streets away, and {colleague} is keeping a tally of who knocks the most '
                       'doors tonight.'),
                      ('R', '{Ns} face burns. A slammed door feels personal, even when it is not.'),
                      ('G',
                       'It is {Ns} own street, three doors down from where {N} grew up. The man behind that door '
                       'once mended {Ns} bike.')]},
 'outcomes': (['The next door opens, and the woman behind it talks for twenty minutes and promises her vote.',
               'By the end of the evening the sheet is full, and the slammed door is a story to laugh about.'],
              ['Three more doors stay shut, and {N} walks home soaked and wondering what the point is.',
               "The man behind the slammed door complains to the candidate's people about the knocking."]),
 'options': [
    ('note the door politely on the sheet, and knock on the next one', 'W1', None, 0.45, '', {'v': 'conformity', 'habit': True, 'self_control': '+', 'grants': 'canvassing', 'world': {'tribal': 'remember the hearth, and walk on to the next', 'magic': "mark the door on the faction's roll, and knock on the next"}, 'chance': 0.88}),
    ('change your opening line for the rest of the street, and see what works', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'world': {'tribal': 'change how you begin at the rest of the hearths, and see what works'}, 'chance': 0.75}),
    ('leave the quiet streets, and work the ones near the candidate, where it will be noticed', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'leave the far hearths, and walk the ones near the speaker, where it will be noticed', 'magic': 'leave the quiet lanes, and work the ones near the candidate, where it will be noticed'}, 'chance': 0.88}),
    ('knock again, and ask politely for just ten seconds', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'call out to the hearth again, and ask for just one breath of its time'}, 'chance': 0.2}),
    ('go home; this street has voted one way for fifty years, so tick it all off', 'G1', None, 0.45, '', {'v': 'tradition, hedonism', 'mark': 'hid a wrong', 'closed': 'approval: doors logged that were never knocked; backfire: the organiser checks the sheets against the replies, and the names do not match', 'self_control': '-', 'world': {'tribal': 'go back to your own fire; these hearths have always gone one way, and say you spoke at each', 'magic': 'go home; this lane has always voted one way, so mark it all as knocked'}, 'chance': 0.95}),
    ('report the hostile door to the organiser, so nobody wastes another evening there', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': "tell the speaker's kin which hearth is closed, so nobody wastes another walk"}, 'chance': 0.65}),
    ('team up with a friend to find a quicker, livelier way through the street', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'mark': 'made a friend', 'world': {'tribal': 'pair up with a friend to find a quicker, merrier way round the hearths'}, 'chance': 0.65}),
    ('bring along an old neighbour, since every door on the street opens to her', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'bring along an old woman of these hearths, since every hearth welcomes her'}, 'chance': 0.75}),
    ('laugh it off with the others over chips afterwards, and come back next week', 'R1', 'W.7', 0.5, '', {'v': 'hedonism, conformity', 'habit': True, 'self_control': '+', 'grants': 'canvassing', 'world': {'tribal': 'laugh it off with the others at the fire, and walk out again next moon', 'magic': 'laugh it off with the others at the tavern, and come back next week'}, 'chance': 0.92}),
    ('ask the old hands which streets slam doors, and why, before the next round', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'door': True, 'grants': 'knowing every street', 'world': {'tribal': 'ask the old walkers which hearths turn their backs, and why', 'magic': "ask the faction's old hands which lanes shut their doors, and why"}, 'chance': 0.8}),
 ]},
{'name': 'the candidate remembers your name',
 'stages': 'child juvenile young_adult adult mature elder',
 'age': (14, 100),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.2,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'community',
 'horizon': 'moment',
 'roles': 'friend, colleague, mentor',
 'requires': 'campaign volunteer',
 'worlds': {'earth': 'at the count, the candidate crosses the hall, shakes your hand and calls you by your name',
            'tribal': 'at the fire, the speaker greets you by name in front of every hearth you walked to',
            'magic': 'in the square, the candidate calls you by name in front of the crowd'},
 'timing': {'times': 'per campaign volunteer: once or twice a campaign (estimate)'},
 'scenes': {'earth': [('',
                       'At the count, the candidate crosses the whole hall, shakes {Ns} hand and says {Ns} name '
                       "without a moment's pause. Six weeks of evenings, and somebody noticed."),
                      ('W',
                       '{N} only did what was asked, every evening, and that is exactly what the candidate gives '
                       'thanks for.'),
                      ('U',
                       '{N} wonders how the candidate does it: a card index, a trick of memory, or simply paying '
                       'attention.'),
                      ('B',
                       "People at the count saw the handshake. {N} notices one of the party's organisers writing "
                       'something down.'),
                      ('R', 'A rush of pure delight: {N} is grinning far too widely and does not care who sees.'),
                      ('G',
                       'The candidate grew up in the same town and knows {Ns} family. The handshake feels like the '
                       'town itself saying thanks.')]},
 'outcomes': (["The candidate's thanks are real, and {N} walks home through the dark streets light as air.",
               'The next week a message comes asking {N} to help again, this time with a bigger part.'],
              ['By morning the candidate has shaken a hundred hands, and the moment is gone.',
               'The handshake makes one of the old volunteers jealous, and the team goes a little cold.']),
 'options': [
    ('thank the candidate, and offer to help again at the next election', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'binds': True, 'chance': 0.75}),
    ('write down what worked this campaign, door by door, for next time', 'U1', None, 0.45, '', {'v': 'achievement', 'habit': True, 'mark': 'learned a skill', 'world': {'tribal': 'go over in your head what worked at each hearth, for next time', 'magic': 'write down what worked this campaign, lane by lane, for next time'}, 'chance': 0.95}),
    ('ask the candidate for a paid job on the next campaign', 'B1', None, 0.45, '', {'v': 'achievement, power', 'door': True, 'aims': 'campaign organiser', 'world': {'tribal': 'ask the speaker to keep you at his fire through the next gathering, fed for your walking', 'magic': "ask the candidate for a paid place among the faction's runners next season"}, 'chance': 0.4}),
    ('celebrate with the team until the hall closes', 'R1', None, 0.45, '', {'v': 'hedonism', 'world': {'tribal': 'dance with the other walkers until the fire burns down', 'magic': 'celebrate with the team until the tavern closes'}, 'chance': 0.95}),
    ('ask the candidate to come and meet the neighbours on your street', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': "ask the speaker to come and sit at your family's hearth", 'magic': 'ask the candidate to come and meet the neighbours in your lane'}, 'chance': 0.45}),
    ('ask the candidate for a written reference for your applications', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'ask the speaker to give his word for your walking before the elders', 'magic': 'ask the candidate for a letter under seal, to show the guilds'}, 'chance': 0.7}),
    ('ask to join the inner team next time, to see the real work up close', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, self-direction', 'door': True, 'world': {'tribal': "ask to walk with the speaker's own circle next season, to see how it is done", 'magic': "ask to join the faction's inner circle next season, to see the real work up close"}, 'chance': 0.6}),
    ('ask the candidate to sponsor your party membership, and say you mean to stand', 'B1', 'G.7', 0.5, '', {'v': 'achievement, security', 'identity': True, 'aims': 'party member', 'world': {'tribal': 'ask the speaker to bind you to the faction, and say you mean to speak at the fire one day', 'magic': 'ask the candidate to sponsor your oath to the faction, and say you mean to stand one day'}, 'chance': 0.9}),
    ('promise there and then to run the street team next time', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'binds': True, 'world': {'tribal': 'promise there and then to lead the hearth-walkers next time', 'magic': 'promise there and then to lead the lane runners next time'}, 'chance': 0.85}),
    ('ask the old agent who has run every campaign here to pass on the trade', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'mark': 'learned a skill', 'grants': 'campaigning', 'world': {'tribal': 'ask the old hearth-walker who has served every speaker here to pass on the craft', 'magic': 'ask the old faction hand who has run every campaign here to pass on the trade'}, 'chance': 0.75}),
 ]},
{'name': 'a voter not on the list',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'moment',
 'roles': 'elder, colleague, friend',
 'requires': 'polling-station volunteer',
 'worlds': {'earth': 'a voter at the desk in the school hall is not on the register, and the queue behind her is '
                     'growing',
            'tribal': 'a stranger from another band wants to cast a pebble at the gathering, and no one at the '
                      'stones can vouch for her',
            'magic': 'a voter with no seal on her papers wants a lot from the warded urn, and the queue behind her '
                     'is growing'},
 'timing': {'times': 'per polling-station volunteer: on most election days at a busy station; about 3 lives in 100 '
                     'work a polling station (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'An old woman at the desk in the school hall has voted at this station for forty years, she '
                       'says, and today she is not on the register. The queue behind her reaches the door.'),
                      ('W',
                       'The rules are clear: no name, no ordinary ballot. The rules are also what keep every other '
                       'vote in the box honest.'),
                      ('U',
                       '{N} runs a finger down the register twice. Her name is missing between two neighbours who '
                       'are there: a clerical slip, or a move nobody recorded.'),
                      ('B',
                       'The presiding officer is on a break, and for the next ten minutes the decision is {Ns} own. '
                       '{N} rather likes that.'),
                      ('R',
                       'The woman is near tears, and the man behind her is muttering. {N} feels the heat of the '
                       'whole queue.'),
                      ('G',
                       '{N} knows her: she lives on the corner by the bakery and has done for decades. Everyone in '
                       'this hall knows her.')]},
 'outcomes': (['The mix-up is sorted, and she leaves with her vote cast and her dignity whole.',
               'The queue moves again, and at the end of the day the presiding officer backs {Ns} call.'],
              ['She leaves without voting, telling everyone in the queue what she thinks of the station.',
               'The decision is questioned at the count, and {Ns} name goes into the incident book.']),
 'options': [
    ('explain the rules gently, and offer her the sealed ballot kept for disputed votes', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'explain the custom gently, and set her pebble aside until the elders have heard her', 'magic': 'explain the rules gently, and give her the sealed lot kept for disputed votes'}, 'chance': 0.7}),
    ('find the slip in the register, and ring the election office to check it', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'ask around the stones until someone remembers which band she came with', 'magic': "find the slip in the roll, and send a runner to the Order's registry to check it"}, 'chance': 0.7}),
    ('make the call yourself while the officer is out, and stand by it', 'B1', None, 0.45, '', {'v': 'power, self-direction', 'identity': True, 'world': {'tribal': 'make the call yourself while the elders are away, and stand by it', 'magic': 'make the call yourself while the warden is out, and stand by it'}, 'chance': 0.7}),
    ('stand up for her to the grumbling queue, and give her all the time she needs', 'R1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.9}),
    ('ask the old hands at the next table whether this has happened to her before', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'ask the old keepers of the stones whether this has happened to her before'}, 'chance': 0.7}),
    ('open a second desk to keep the queue moving while she is helped', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'set out a second heap of stones, so the others can cast while she is heard', 'magic': 'open a second urn table, so the queue keeps moving while she is helped'}, 'chance': 0.75}),
    ('read the rules loosely enough to give her an ordinary ballot', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'mark': 'broke the law', 'closed': "law: an ordinary ballot given to a voter not on the register; backfire: the result is challenged, and the station's papers are pulled", 'world': {'tribal': 'read the custom loosely enough to let her cast a pebble with the band', 'magic': 'read the rules loosely enough to let her cast an ordinary lot'}, 'chance': 0.85}),
    ('wait for the presiding officer, so the decision goes on record as theirs', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'self_control': '+', 'world': {'tribal': 'wait for the elders, so the choice is on record as theirs', 'magic': "wait for the warden, so the decision is entered under the Order's seal"}, 'chance': 0.92}),
    ('ring her daughter to bring the card that proves where she is registered', 'R1', 'U.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': "run to her kin's hearth to fetch someone who can vouch for her", 'magic': 'run to her lodging for the papers that prove her seal'}, 'chance': 0.55}),
    ('ask the neighbours in the queue to vouch for her, as people here always have', 'G1', 'B.7', 0.5, '', {'v': 'tradition, benevolence', 'identity': True, 'world': {'tribal': 'ask the families at the stones to vouch for her, as the bands always have'}, 'chance': 0.2}),
 ]},
{'name': 'the count runs past midnight',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'moment',
 'roles': 'colleague, elder, friend',
 'requires': 'polling-station volunteer',
 'worlds': {'earth': 'the count in the sports centre runs past midnight, and one bundle of ballots will not tally',
            'tribal': 'the counting goes on by firelight, and one heap of pebbles keeps coming out different',
            'magic': "the urns are counted under the Order's lamps until dawn, and one tray of lots will not tally"},
 'timing': {'times': 'per polling-station volunteer who stays for the count: at most national counts (estimate)'},
 'scenes': {'earth': [('',
                       'Past midnight in the sports centre: cold coffee and sore backs. One bundle of ballots has '
                       'been counted three times and comes out three different ways.'),
                      ('W',
                       "Every ballot in that bundle is somebody's voice, and the count is the moment it is heard. "
                       '{N} wants it right, not quick.'),
                      ('U',
                       'Three counts, three totals. {N} suspects two ballots stuck together, or one counted into the '
                       'wrong pile.'),
                      ('B',
                       "The candidates' agents are watching every hand, and one of them is very keen for the count "
                       'to end soon.'),
                      ('R',
                       '{N} is giddy with tiredness, laughing at nothing with {colleague}, and wide awake at the '
                       'same time.'),
                      ('G',
                       'The same faces as every election: {elder} with the flask, the retired teacher who checks '
                       "everyone's sums. {N} feels part of something old.")]},
 'outcomes': (['The bundle finally tallies at a quarter to two, and the declaration goes ahead to applause.',
               'The table walks out into the dawn together, tired and oddly proud.'],
              ["The recount drags on to four, and the agents' complaints go into the record.",
               'The bundle never tallies, and the whole count has to be checked again in the morning.']),
 'options': [
    ('sign the count sheet anyway, so the declaration is not held up', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'hid a wrong', 'closed': "law: a count signed off when it does not tally; backfire: a recount finds the gap, and the station's work is questioned", 'self_control': '-', 'world': {'tribal': 'tell the elders the heap is right, so the choosing is not held up', 'magic': "seal the tray's tally anyway, so the declaration is not held up"}, 'chance': 0.95}),
    ('spread the bundle out, and count it in tens, one ballot at a time', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'lay the pebbles out in rows of ten, one by one', 'magic': 'lay the lots out in rows of ten, one by one'}, 'chance': 0.9}),
    ('volunteer to lead the recount of the bundle, in front of the agents', 'B1', None, 0.45, '', {'v': 'achievement, power', 'self_control': '+', 'world': {'tribal': "offer to count the heap again yourself, in front of the speakers' kin", 'magic': "offer to lead the recount of the tray, in front of the factions' agents"}, 'chance': 0.65}),
    ('crack a joke to wake the table up, and start the bundle again', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'chance': 0.8}),
    ('pour out the tea from the flask, and let the old hands set the pace', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'pass round the warm broth, and let the old ones set the pace', 'magic': 'pour out the mulled wine, and let the old hands set the pace'}, 'chance': 0.8}),
    ('ask for a proper break for the whole table before the recount', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'ask the elders for a rest by the fire before the heap is counted again'}, 'chance': 0.92}),
    ('show the youngest counters the old checking trick, the way the old hands taught it', 'U1', 'G.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'show the youngest pebble-keepers the old way of checking a heap', 'magic': "show the youngest counters the old checking trick of the Order's clerks"}, 'chance': 0.8}),
    ('insist the agents watch every recount closely, so nobody can cry foul later', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': "make the speakers' kin watch every count closely, so nobody can cry foul later", 'magic': "make the factions' agents watch every recount closely, so nobody can cry foul later"}, 'chance': 0.8}),
    ('stay on after the others go, until the last ballot makes sense', 'R1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'self_control': '+', 'world': {'tribal': 'stay by the fire after the others sleep, until the last pebble makes sense', 'magic': 'stay under the lamps after the others go, until the last lot makes sense'}, 'chance': 0.7}),
    ('let the oldest counter, thirty elections on, settle it for the table', 'G1', 'B.7', 0.5, '', {'v': 'tradition, power', 'world': {'tribal': 'let the oldest keeper of the stones settle it for everyone'}, 'chance': 0.65}),
 ]},
{'name': 'the annual meeting nobody comes to',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.015,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'week',
 'roles': 'friend, elder, colleague',
 'requires': 'local party officer',
 'worlds': {'earth': "six people in a cold church hall for the branch's annual meeting, and the rules need ten to "
                     'make a quorum',
            'tribal': "few families come to the faction's fire for the yearly choosing of its elders, and custom "
                      'wants every hearth heard',
            'magic': "the faction's yearly meeting in an empty back room of the guild hall, and the charter wants "
                     'ten sworn members'},
 'timing': {'times': 'per local party officer: once a year; many branches struggle to reach a quorum outside '
                     'election years; about 1 life in 100 holds a local party office (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'Six people in a cold church hall, counting {N}, {elder} and the man who comes for the '
                       'biscuits. The rules need ten to make a quorum, and the posts of chair and treasurer are both '
                       'empty.'),
                      ('W',
                       'Without a quorum nothing the meeting decides is valid, and {N} knows the rulebook too well '
                       'to pretend otherwise.'),
                      ('U',
                       '{N} has the membership list: a hundred and twelve names. Most joined in one rush three years '
                       'ago and have not been seen since.'),
                      ('B',
                       'An empty branch is an opening: whoever fills the posts tonight runs the selection next '
                       'year.'),
                      ('R',
                       '{N} looks at the rows of empty chairs and feels a stubborn spark: this branch is not dying '
                       'on {Ns} watch.'),
                      ('G',
                       '{elder} has come to every annual meeting for forty years and remembers when this hall was '
                       'full. The urn is on, as always.')]},
 'outcomes': (['The next meeting has fourteen people in it, and two of them are under thirty.',
               'The posts are filled, and the branch has a proper chair for the first time in two years.'],
              ['The branch limps on for another year with six members and no treasurer.',
               'Word of the empty hall reaches the region, and the branch is merged with the next ward without being '
               'asked.']),
 'options': [
    ('write down a quorum that was not there, so the branch can elect its officers', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'hid a wrong', 'closed': 'approval: minutes that record members who were not there; backfire: an absent member reads the minutes and complains to the region', 'self_control': '-', 'world': {'tribal': 'say every hearth was heard when few were, so the faction can choose its elders', 'magic': "record ten sworn members in the faction's book when six were there"}, 'chance': 0.95}),
    ("propose merging with the next ward's branch, and hand over the books", 'U1', None, 0.45, '', {'v': 'achievement, security', 'drops': 'local party officer', 'world': {'tribal': "propose joining the faction's fire to the next camp's, and hand over the tallies of gifts", 'magic': "propose merging with the next ward's chapter, and hand over the books"}, 'chance': 0.7}),
    ('stand for chair and treasurer both, while nobody else wants them', 'B1', None, 0.45, '', {'v': 'power, achievement', 'identity': True, 'self_control': '+', 'world': {'tribal': "take both the faction's duties while no one else will", 'magic': "take both the warden's chain and the coffer key while no one else will"}, 'chance': 0.9}),
    ('stand up and tell the six why the branch matters, and mean every word', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'stand up and tell the few at the fire why the faction matters, and mean every word'}, 'chance': 0.7}),
    ('keep the minutes faithfully, adjourn, and try again next month', 'G1', None, 0.45, '', {'v': 'tradition, conformity', 'habit': True, 'self_control': '+', 'world': {'tribal': 'remember what was said faithfully, bank the fire, and try again next moon'}, 'chance': 0.95}),
    ('adjourn by the rules, and invite the whole ward to a summer fete instead', 'W1', 'G.7', 0.5, '', {'v': 'conformity, benevolence', 'door': True, 'world': {'tribal': 'put off the choosing by custom, and invite every hearth to a midsummer feast instead', 'magic': 'adjourn by the charter, and invite the whole ward to a street feast instead'}, 'chance': 0.6}),
    ('write to every lapsed member to ask what the branch should do for them', 'U1', 'W.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': 'visit every hearth that stayed away, and ask what the faction should do for them', 'magic': 'write to every lapsed member to ask what the faction should do for them'}, 'chance': 0.35}),
    ('pay for an online meeting service yourself, so members can vote from home', 'B1', 'U.7', 0.5, '', {'v': 'self-direction, achievement', 'world': {'tribal': "pay a runner from your own stores to carry each hearth's word to the fire", 'magic': "pay a scribe from your own purse to carry sealed votes from members' homes"}, 'chance': 0.7}),
    ('ring your old school friends, and talk them into joining before the next meeting', 'R1', 'B.7', 0.5, '', {'v': 'benevolence, power', 'mark': 'made a friend', 'world': {'tribal': 'go to the friends you grew up with, and talk them into the faction before the next fire'}, 'chance': 0.5}),
    ('take the six across to the cafe, and make it a night worth coming back for', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'turn the gathering into a night of songs, so people want to come back', 'magic': 'move the six to the tavern next door, and make it a night people want back'}, 'chance': 0.65}),
 ]},
{'name': 'two members want the same nomination',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (16, 100),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.015,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, friends',
 'horizon': 'months',
 'roles': 'friend, colleague, elder',
 'requires': 'local party officer',
 'worlds': {'earth': 'two members of the branch both want the nomination for the same council seat, and both ask for '
                     'your backing',
            'tribal': "two of the faction's young want to be its voice at the fire, and both come to your hearth for "
                      'your word',
            'magic': "two sworn members want the faction's seal for the same seat on the town council, and both ask "
                     'for yours'},
 'timing': {'times': 'per local party officer a year: about 1 in 5, most of all in the year before local elections '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       "Two members, {friend} and {colleague}, both want the branch's nomination for the one "
                       'winnable council seat. Both have rung {N} this week, and both have said, in nearly the same '
                       'words, that they are counting on {N}.'),
                      ('W',
                       '{N} runs the selection, and whoever runs it must be seen to have no favourite. That is the '
                       'whole of the job.'),
                      ('U',
                       '{N} has walked the ward with both. One is better on the doorstep, the other in the council '
                       'chamber, and the seat needs both.'),
                      ('B',
                       "Whoever wins will owe {N} for the result. The branch's next ten years may turn on who that "
                       'is.'),
                      ('R', '{friend} has been {Ns} friend since school, and {N} badly wants to say so out loud.'),
                      ('G',
                       '{colleague} comes from a family that has run this branch for three generations, and {elder} '
                       'expects it to go on that way.')]},
 'outcomes': (['The branch chooses, and the loser shakes hands and offers to run the campaign.',
               'Both stay in the branch, and the seat is fought with the whole team behind it.'],
              ['The loser walks out of the meeting and out of the party, and takes friends along.',
               'The quarrel spills into the local paper, and the seat is lost before the campaign begins.']),
 'options': [
    ('run a fair hustings and a secret ballot, and back neither in public', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'self_control': '+', 'world': {'tribal': 'let both speak at the fire, let the families choose, and say nothing for either', 'magic': 'hold a fair disputation and a sealed ballot, and back neither openly'}, 'chance': 0.75}),
    ('score both against what the seat needs, and share the scores with the branch', 'U1', None, 0.45, '', {'v': 'achievement', 'identity': True, 'world': {'tribal': 'weigh both against what the band needs, and tell the faction plainly'}, 'chance': 0.6}),
    ('sign up a dozen new members who will vote for your choice', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: a meeting packed with members signed up for one vote; backfire: the region freezes the selection and audits the new members', 'world': {'tribal': 'bring a dozen kin into the faction just in time to stand behind your choice', 'magic': 'enrol a dozen new sworn members just in time to cast for your choice'}, 'chance': 0.8}),
    ('tell your old friend, straight out, that you are backing them', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'tell your old friend, straight out, that your word is theirs'}, 'chance': 0.95}),
    ('ask the oldest members which of the two the ward would trust', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'ask the oldest of the faction which of the two the hearths would trust'}, 'chance': 0.65}),
    ('broker an agreement that the loser gets the next seat that comes up', 'W1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'binds': True, 'grants': 'settling disputes', 'world': {'tribal': 'broker an agreement that the other speaks at the next fire', 'magic': 'broker an agreement that the other gets the next seat that falls open'}, 'chance': 0.4}),
    ('write the selection rules down in full before anyone votes, and send them to both', 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'binds': True, 'world': {'tribal': 'set out the custom for the choosing before anyone stands, and tell it to both', 'magic': 'write the rules of the choosing in full before any lot is cast, and send them to both'}, 'chance': 0.95}),
    ('count the likely votes for each, and show both where they really stand', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'habit': True, 'grants': 'counting the votes', 'world': {'tribal': 'work out which families stand behind each, and show both where they stand', 'magic': 'count the likely lots for each, and show both where they stand'}, 'chance': 0.8}),
    ('talk one of them into standing for the county seat instead, where they could win big', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'talk one of them into asking to speak at the great gathering instead', 'magic': 'talk one of them into standing for the Assembly instead, where they could win big'}, 'chance': 0.35}),
    ('take both to the cafe, and let them have it out as friends', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'sit both at your hearth through the night, and let them have it out', 'magic': 'take both to the tavern, and let them have it out over a cup'}, 'chance': 0.55}),
 ]},
{'name': 'the branch meeting runs late',
 'stages': 'young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.001,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'moment',
 'roles': 'boss, colleague',
 'requires': 'party member',
 'worlds': {'earth': 'a branch meeting above a pub runs late: a motion on the local hospital, and two hours of '
                     'procedure before anyone reaches it',
            'tribal': "the faction's elders talk late at the fire, and the matter of the healer's lodge waits behind "
                      'every old quarrel',
            'magic': "the faction's ward meeting in a back room of the guild hall runs late, and the motion on the "
                     'infirmary is still not reached'},
 'timing': {'times': 'per party member a year: an active member sits through a long branch meeting several times a '
                     'year, though fewer than half of members ever attend one; about 6 lives in 100 belong to a '
                     'party at some point (catalogue share; estimate)',
            'gap_years': (5.0, 10.0)},
 'scenes': {'earth': [('',
                       'Nineteen members sit in the room above the pub, and the motion on the local hospital is item '
                       'eleven. At half past nine {boss}, who chairs the branch, is still going through the minutes '
                       'of the last meeting line by line.'),
                      ('W',
                       'Every amendment has to be moved, seconded and put to the vote, and {N} knows the standing '
                       'orders say so for good reasons. It is still only item four.'),
                      ('U',
                       "{N} has read the hospital trust's own figures twice and has a page of notes on the motion. "
                       'Nobody else in the room seems to have read them at all.'),
                      ('B',
                       'Half the room has drifted home. Whoever is still here at ten will decide what the branch '
                       'says about the hospital, and {N} means to be here.'),
                      ('R',
                       'The maternity ward is closing, and the room is arguing about whether the agenda went out on '
                       'time. {N} can feel the words building up like steam.'),
                      ('G',
                       'The same faces sit in the same chairs as every month: {colleague} by the radiator, the old '
                       'couple by the door. The branch has met above this pub for forty years.')],
            'tribal': [('',
                        "The fire has burned down twice, and the faction's elders are still on the old quarrel about "
                        "the eastern hearths. The matter of the healer's lodge, the one {N} came to hear, has not "
                        'been raised.')],
            'magic': [('',
                       "The candles in the back room of the guild hall are half gone, and the faction's warden is "
                       "still reading last month's petitions aloud. The motion on the infirmary waits at the bottom "
                       'of the roll.')]},
 'outcomes': (['The motion is reached at last, and the branch says what it came to say.',
               '{N} walks home late and tired, sure that the evening counted for something.'],
              ['Time runs out, and the motion is put off until next month, again.',
               'The vote goes the other way, and {boss} thanks {N} a little too politely at the door.']),
 'options': [
    ('learn the standing orders, and use them to move the hospital motion up', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'grants': 'knowing the rules of the house', 'world': {'tribal': "learn the customs of the fire, and use them to bring the healer's matter forward"}, 'chance': 0.7}),
    ("read the trust's own figures to the room before anyone votes", 'U1', None, 0.45, '', {'identity': True, 'v': 'universalism, achievement', 'world': {'tribal': 'tell the fire what the healer has seen this winter, before anyone decides', 'magic': "read the infirmary's own ledgers to the room before anyone votes"}, 'chance': 0.7}),
    ('stay until the room empties, and carry the motion with whoever is left', 'B1', None, 0.45, '', {'v': 'power, achievement', 'self_control': '+', 'chance': 0.9}),
    ('stand up out of turn and say what the closure means to the street', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'mark': 'defied an authority', 'world': {'tribal': 'speak out of turn and say what losing the healer means to every hearth'}, 'chance': 0.35}),
    ('stay quiet, as the old members do, and vote with the room when it comes', 'G1', None, 0.45, '', {'v': 'tradition, conformity', 'chance': 0.95}),
    ('propose a five-minute limit on every speech, so the branch gets to act', 'W1', 'R.7', 0.5, '', {'v': 'self-direction', 'world': {'tribal': 'ask the elders to let each voice speak once, so the fire gets to decide'}, 'chance': 0.65}),
    ("write the hospital's story for the branch newsletter, so members know what is at stake", 'U1', 'G.7', 0.5, '', {'v': 'tradition, universalism', 'world': {'tribal': "gather what the old ones remember of the healer's lodge, and tell it at the next fire", 'magic': "write the infirmary's story for the faction's broadsheet, so members know what is at stake"}, 'chance': 0.9}),
    ('plan to stand for branch chair next year, and run every meeting to time', 'B1', 'W.7', 0.5, '', {'v': 'power', 'aims': 'local party officer', 'world': {'tribal': 'plan to ask the families to make you an elder of the faction, and keep its fires short', 'magic': "plan to stand for the faction's ward office next year, and run its meetings to time"}, 'chance': 0.75}),
    ('walk out, and go and ask the night-shift nurses what is really happening', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'walk away from the fire, and go and ask the healer herself', 'magic': "walk out, and go and ask the infirmary's night nurses yourself"}, 'chance': 0.65}),
    ('have a quiet word with the old members by the door, and collect their proxy votes', 'G1', 'B.7', 0.5, '', {'v': 'power, tradition', 'closed': 'approval: proxy votes the branch rules do not allow; backfire: the votes are struck out, and the chair notes it in the minutes', 'world': {'tribal': 'have a quiet word with the old families, and speak in their name once they have gone to sleep', 'magic': 'have a quiet word with the old members, and cast their lots for them'}, 'chance': 0.65}),
 ]},
{'name': 'the party changes its line',
 'stages': 'young_adult adult mature elder',
 'age': (16, 95),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.001,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'months',
 'roles': 'boss, colleague, friend',
 'requires': 'party member',
 'worlds': {'earth': 'a policy shift announced on the news: the leadership drops the promise you joined the party '
                     'for',
            'tribal': 'the faction makes peace with the family it swore against, and the oath you took against them '
                      'is set aside',
            'magic': "the faction takes the Order's side in the Assembly, against the cause you swore to it for"},
 'timing': {'times': 'per party member a year: about 1 in 10 see the leadership drop or reverse a promise they '
                     'joined for; it comes with most new leaders and most manifestos (estimate)',
            'gap_years': (5.0, 10.0)},
 'scenes': {'earth': [('',
                       "The six o'clock news carries it in one line: the party is dropping the promise {N} joined "
                       'for. By seven {Ns} phone is full of messages from the branch, most of them in capital '
                       'letters.'),
                      ('W',
                       '{N} signed the membership form because of that promise, and still believes a promise made to '
                       "voters should be kept. The party's own rules say policy is made by conference, not by a "
                       'press release.'),
                      ('U',
                       '{N} reads the new policy paper in full, twice, looking for what changed and why. Some of the '
                       'reasoning holds up, and that is almost worse.'),
                      ('B',
                       'The leadership has chosen, and from now on the members who matter will be the ones who back '
                       'it. {N} can already see which way the next selection will go.'),
                      ('R',
                       '{N} remembers the night of joining: the hall, the cheering, the promise said out loud. Now '
                       'it is gone in a line on the news, and {N} is shaking with it.'),
                      ('G',
                       '{Ns} family has voted for this party for three generations. One bad policy does not undo a '
                       'family, {N} tells {friend}, not quite believing it.')],
            'tribal': [('',
                        "The faction's elders have shared a fire with the family the band swore against, and the old "
                        'oath is set aside. {N} swore that oath too, at the same fire, three winters ago.')],
            'magic': [('',
                       'The heralds cry it in the square at noon: the faction will stand with the Order in the '
                       "Assembly. {N} swore the faction's oath for the opposite cause.")]},
 'outcomes': (['The storm passes, and {N} knows where {N} stands with the party.',
               '{N} finds others who feel the same, and the anger turns into a plan.'],
              ['Nothing {N} does moves the leadership an inch, and the branch splits over it anyway.',
               '{friend} hears what {N} said, and keeps away for a month.']),
 'options': [
    ('put a motion to the next conference to restore the promise, by the rules', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'ask the elders to hear the oath again at the next great fire', 'magic': "put a motion to the faction's next assembly to restore the cause"}, 'chance': 0.55}),
    ('write a paper on what dropping the promise will cost, and send it up the line', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': 'work out what the peace will cost the band, and take it to the elders'}, 'chance': 0.55}),
    ('back the new line in public, and ask for a policy seat in return', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'world': {'tribal': "speak for the peace at the fire, and ask for a place among the faction's elders in return", 'magic': "back the faction's new line in the square, and ask for a seat in its inner council"}, 'chance': 0.7}),
    ('tear up your membership card, and say why in public', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'drops': 'party member', 'world': {'tribal': "walk away from the faction's fire, and say why before them all", 'magic': 'break your faction seal in the square, and say why'}, 'chance': 0.95}),
    ('stay in and stay quiet; parties change, and the old members outlast them', 'G1', None, 0.45, '', {'v': 'tradition', 'self_control': '+', 'world': {'tribal': 'stay with the faction and say nothing; factions change, and the old families outlast them', 'magic': 'stay in the faction and say nothing; factions change, and the old houses outlast them'}, 'chance': 0.8}),
    ("sign the rebels' open letter, with your name and your branch on it", 'W1', 'R.7', 0.5, '', {'v': 'stimulation, universalism', 'identity': True, 'mark': 'defied an authority', 'world': {'tribal': 'stand with the young ones who refuse the peace, and say your name aloud', 'magic': "put your seal to the rebels' open letter, with your ward beside it"}, 'chance': 0.95}),
    ("dig out the party's founding statement, and show the branch the promise was always there", 'U1', 'G.7', 0.5, '', {'door': True, 'v': 'tradition', 'world': {'tribal': 'remind the families of the words said when the faction first swore the oath', 'magic': "find the faction's founding charter, and show the ward the cause was always there"}, 'chance': 0.7}),
    ('trade your support for a written pledge on the one local promise that matters', 'B1', 'W.7', 0.5, '', {'v': 'power', 'binds': True, 'world': {'tribal': "trade your silence for the elders' word on the one thing your hearths need", 'magic': 'trade your support for a sealed pledge on the one local promise that matters'}, 'chance': 0.5}),
    ("go to the rebels' weekend meeting on a whim, to see who they really are", 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'door': True, 'world': {'tribal': "go to the young ones' fire on a whim, to see who they really are"}, 'chance': 0.9}),
    ('ride it out, and keep the branch ready for the day the leadership falls', 'G1', 'B.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'wait it out, and keep your hearths ready for the day the faction head falls', 'magic': "ride it out, and keep the ward ready for the day the faction's head falls"}, 'chance': 0.45}),
 ]},
{'name': 'the planning committee and the field',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.015,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'months',
 'roles': 'boss, colleague, rival',
 'requires': 'local councillor',
 'worlds': {'earth': 'the planning application for the last green field in the ward comes to committee: two hundred '
                     'houses, the officers for it, and a hall full of residents against it',
            'tribal': 'the band wants to move camp onto the old burial ground by the river, and every voice at the '
                      'fire must say where it stands',
            'magic': 'a guild wants the common meadow outside the walls for its new hall, and the town council must '
                     'vote on the grant'},
 'timing': {'times': 'per local councillor a year: a contested planning vote comes several times a year, a big one '
                     'on a green field every few years; about 1 life in 100 sits on a council (catalogue share; '
                     'about 117,000 councillors in England, LGIU and NALC)',
            'gap_years': (5.0, 10.0)},
 'scenes': {'earth': [('',
                       'The application is for two hundred houses on the last open field in the ward. The officers '
                       'recommend approval, the party group wants it through, and the public seats are full of '
                       'residents with home-made placards.'),
                      ('W',
                       'The rules are clear: a councillor decides a planning case on planning grounds, not on who '
                       'shouts loudest. {N} also promised the ward a fair hearing, and meant it.'),
                      ('U',
                       '{N} has read all four hundred pages, the flood-risk appendix included. Page three hundred '
                       'and twelve does not say what the summary says it says.'),
                      ('B',
                       '{boss}, who leads the group, has made it plain that the council needs the houses and the '
                       'money that comes with them. A vote against would be remembered at the next reshuffle of '
                       'committee seats.'),
                      ('R',
                       '{N} grew up kicking a ball on that field. Looking at the placards, {N} feels the whole room '
                       'tilt toward one answer.'),
                      ('G',
                       'The field has been grazed, played on and walked across for as long as anyone can remember. '
                       'Two hundred families also need somewhere to live.')],
            'tribal': [('',
                        'The elders point at the riverbank where the old ones lie: the driest ground for the winter '
                        'camp, and the most sacred. Every voice at the fire is asked where it stands, and {N} is '
                        'next.')],
            'magic': [('',
                       "The guild's masters have laid the drawings for their new hall on the council table. Outside "
                       "the window, the common meadow where the town's goats graze is gold in the evening light.")]},
 'outcomes': (['The committee reaches a decision {N} can stand behind, and the ward hears why.',
               "The vote is closer than anyone expected, and the field's future is settled for a few years at "
               'least.'],
              ['The vote goes the other way, and the people in the public seats leave without looking at {N}.',
               '{boss} hears how {N} handled it, and {N} is off the committee by the spring.']),
 'options': [
    ("vote with the officers' advice, on planning grounds alone", 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'follow the custom the eldest set out, and nothing more'}, 'chance': 0.9}),
    ('find the flaw in the flood report, and ask for the decision to be put off', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': 'show the fire where the river rose in the old floods, and ask the band to wait', 'magic': "find the flaw in the guild's survey of the meadow, and ask for the vote to be put off"}, 'chance': 0.45}),
    ('vote it through, and get the developer to pay for a sports hall for the ward', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'agree to the move, if your own hearths get the driest ground', 'magic': 'vote it through, and make the guild pay for a new well in the ward'}, 'chance': 0.55}),
    ('stand with the residents and vote against, whatever the group says', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'mark': 'defied an authority', 'world': {'tribal': 'stand with the families against the move, whatever the elders say', 'magic': 'stand with the townsfolk and vote against, whatever the faction says'}, 'chance': 0.3}),
    ('speak for the field as common ground the ward has always shared', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, universalism', 'world': {'tribal': 'speak for the dead who lie there, and the ground the band has always kept', 'magic': 'speak for the meadow as common ground the town has always shared'}, 'chance': 0.35}),
    ("propose a rule that protects the ward's last open spaces, and take it to full council", 'W1', 'G.7', 0.5, '', {'v': 'universalism, security', 'identity': True, 'grants': 'a reform with your name on it', 'world': {'tribal': 'propose a custom that no camp is ever made on the resting places of the dead', 'magic': "propose a bylaw that keeps the town's commons common, and take it to the full council"}, 'chance': 0.15}),
    ('broker a compromise the residents, the officers and the group can all sign', 'U1', 'W.7', 0.5, '', {'binds': True, 'v': 'universalism, conformity', 'grants': 'coalition building', 'world': {'tribal': 'work out a camp the families, the elders and the young can all accept', 'magic': 'broker a compromise the townsfolk, the guild and the council can all seal'}, 'chance': 0.55}),
    ("ask a friend in the trade what the developer's figures really show", 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'ask a friend what the elders really said in private', 'magic': 'ask a friend in the guild what its ledgers really show'}, 'chance': 0.65}),
    ("make a fiery speech against it, with the local paper's photographer in the room", 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': 'make a fiery speech against it, with the singers listening', 'magic': 'make a fiery speech against it, with the broadsheet writers in the room'}, 'chance': 0.75}),
    ('walk the field with the residents on Sunday, and let the anger become a campaign', 'G1', 'R.7', 0.5, '', {'binds': True, 'v': 'benevolence, stimulation', 'body': 'light', 'world': {'tribal': 'walk the burial ground with the families at dawn, and let the anger rise', 'magic': 'walk the meadow with the townsfolk on the feast day, and let the anger become a campaign'}, 'chance': 0.7}),
 ]},
{'name': 'a knock at the door at ten at night',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.015,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, home',
 'horizon': 'moment',
 'roles': 'partner, a resident',
 'requires': 'local councillor',
 'worlds': {'earth': 'at ten at night a resident you have never met is on your doorstep: her flat is flooding from '
                     'upstairs, and the landlord will not answer',
            'tribal': 'a family comes to your hearth at night with a feud that will not wait for the council fire',
            'magic': 'a petitioner knocks at your door after the curfew bell, with a grievance against the guild '
                     'that cannot wait until morning'},
 'timing': {'times': 'per local councillor a year: most councillors are approached at home by a resident in trouble '
                     'a few times a year (estimate)',
            'gap_years': (5.0, 10.0)},
 'scenes': {'earth': [('',
                       'At ten at night the doorbell goes. A woman {N} has never met stands on the step in a wet '
                       "coat: water is pouring through her ceiling, and the landlord's emergency line has rung out "
                       'for an hour.'),
                      ('W',
                       '{N} stood for the council to serve the ward, and the ward does not keep office hours. There '
                       'is also a proper way to log a case, and a reason for it.'),
                      ('B',
                       '{partner} is calling from the kitchen that dinner is going cold. The woman on the step lives '
                       'in a street that never votes for {N}, and the thought arrives before {N} can stop it.'),
                      ('G',
                       '{N} knows her block: built two generations ago, with pipes older than most of its tenants. '
                       '{N} knows the caretaker by name too.'),
                      ('U',
                       "{N} has seen this landlord's name on a dozen cases before. Somewhere in its tenancy "
                       'agreement is a clause it would rather nobody read.'),
                      ('R',
                       'She is shaking, from the cold or from the evening she has had. {N} wants to grab a coat and '
                       'go, and also wants, badly, one evening off.')],
            'tribal': [('',
                        'Long after dark a family stands at the edge of {Ns} firelight. A quarrel over a stolen net '
                        'has come to blows, and they will not wait for the council fire to hear it.')],
            'magic': [('',
                       'After the curfew bell there is a lamp at the door and a frightened face behind it: a tanner '
                       'whose workshop the guild has sealed, with a petition and nowhere else to take it.')]},
 'outcomes': (['The worst is over before midnight, and the case is in hand by morning.',
               'A week later the resident tells the neighbours who came to the door, and what happened next.'],
              ['Nothing anyone does tonight helps, and by morning the damage is done.',
               '{partner} goes to bed without a word, and the evening is gone for nothing.']),
 'options': [
    ("take her details, and log the case with the council's emergency line", 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'hear them out, and promise the matter to the elders at first light', 'magic': "take the petition, and enter it in the council's night book"}, 'chance': 0.9}),
    ('find the clause in her tenancy that binds the landlord, and coach her through the call', 'U1', None, 0.45, '', {'v': 'self-direction, benevolence', 'world': {'tribal': 'work out which old custom settles a stolen net, and tell them what to say', 'magic': "find the clause in the guild's charter that covers her, and coach her through it"}, 'chance': 0.85}),
    ("ring the housing director's private number, the one only councillors have", 'B1', None, 0.45, '', {'v': 'power, benevolence', 'world': {'tribal': 'wake the head of the other family yourself, and press them to settle', 'magic': 'send for the guild master by name, a summons only councillors may send'}, 'chance': 0.9}),
    ('tell her this is not the time, and to come to the surgery on Saturday', 'R1', None, 0.45, '', {'v': 'hedonism, security', 'mark': 'refused someone in need', 'self_control': '-', 'world': {'tribal': 'send them away from your fire until the council meets', 'magic': 'tell the petitioner to come back at the proper hour'}, 'chance': 0.95}),
    ("go round with her, and knock on the upstairs neighbour's door yourself", 'G1', None, 0.45, '', {'v': 'benevolence', 'body': 'light', 'mark': 'helped someone in need', 'world': {'tribal': "walk with them to the other family's hearth, and sit down between them", 'magic': "go with the petitioner to the guild hall's door yourself"}, 'chance': 0.75}),
    ('set up an evening surgery on her estate, so people need not come to your door', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'binds': True, 'world': {'tribal': 'set a night each moon when families may bring their quarrels to your hearth', 'magic': "set a weekly evening for petitions in the ward's own hall"}, 'chance': 0.8}),
    ('work the case through properly, and write it up for the housing committee', 'U1', 'W.7', 0.5, '', {'v': 'universalism, conformity', 'grants': 'constituency casework', 'world': {'tribal': 'work the quarrel through, and bring it to the council fire plainly set out', 'magic': 'take the case through the proper offices, and write it up for the council'}, 'chance': 0.9}),
    ('use the case to make the landlord hand over its repair records', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'use the quarrel to make both families say what really happened', 'magic': 'use the case to make the guild open its books on the sealed workshops'}, 'chance': 0.65}),
    ('post her story online tonight, with your name at the front of the fight', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'closed': "approval: a resident's trouble made public without her leave; backfire: she complains to the council's standards officer", 'world': {'tribal': 'tell the quarrel loudly at the next fire, with your name at the front of it', 'magic': 'cry her grievance in the square, with your name at the front of the fight'}, 'chance': 0.75}),
    ('take her in for the night, and let the case wait until morning', 'G1', 'R.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'take the family in at your own fire for the night', 'magic': 'take the petitioner in for the night, and let the guild wait until morning'}, 'chance': 0.95}),
 ]},
{'name': 'forty volunteers and one weekend left',
 'stages': 'young_adult adult mature',
 'age': (18, 70),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'campaign organiser',
 'worlds': {'earth': 'a campaign office with a whiteboard of streets: forty volunteers, one weekend left, and the '
                     'target lists say the ward is lost',
            'tribal': 'a dozen young hunters to send to the far bands before the gathering, and the word from the '
                      'hearths is that the speaker will lose',
            'magic': "forty runners and a single day before the lots are cast, and the tallies say the faction's "
                     'candidate is beaten'},
 'timing': {'times': 'per campaign organiser: once or twice a campaign the volunteers and the days run short of the '
                     'target; about 1 life in 500 works as a paid organiser (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'Forty volunteers, one weekend and a whiteboard of streets. The target lists say the ward is '
                       'lost by about two hundred votes, and {boss}, the candidate, has not been told yet.'),
                      ('W',
                       'The volunteers gave up their weekend on {Ns} word that it would count. {N} owes them a plan '
                       'that does.'),
                      ('U',
                       '{N} pulls up the turnout from the last three elections and starts looking for the streets '
                       'where the model might be wrong.'),
                      ('B',
                       'The regional office wants the forty sent to the next ward, where the race is close. A win '
                       'there would look very good on {Ns} record.'),
                      ('R',
                       '{boss} has knocked on doors every night for six weeks. {N} cannot bring the news, not yet '
                       'and not like this.'),
                      ('G',
                       '{N} knows these streets: which families talk to which, which estate turns out late, which '
                       "pensioners still remember the candidate's mother.")],
            'tribal': [('',
                        'A dozen young hunters wait at the edge of the camp with packs on their backs. The word from '
                        "the hearths is plain: the band's speaker will lose at the gathering, unless something "
                        'changes before the moon is full.')],
            'magic': [('',
                       "Forty runners crowd the faction's hall at dawn, waiting for orders. The tallies say the lots "
                       "will go against the faction's candidate tomorrow.")]},
 'outcomes': (["The weekend's work shows in the count, closer than the lists ever said.",
               'The helpers go home at the end tired, proud and asking about the next campaign.'],
              ['The lists were right, and the count is as bad as they said.',
               'Half the helpers drift off by the second afternoon, and the plan falls apart.']),
 'options': [
    ('tell the volunteers the truth about the numbers, and let them choose where to go', 'W1', None, 0.45, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'tell the young hunters what the hearths are saying, and let them choose where to go', 'magic': 'tell the runners what the tallies say, and let them choose where to go'}, 'chance': 0.65}),
    ('find the streets the model got wrong, and send everyone there', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'world': {'tribal': 'find the hearths the elders have misjudged, and send everyone there', 'magic': 'find the lanes the tallies got wrong, and send everyone there'}, 'chance': 0.45}),
    ('send the forty to the close ward next door, where a win is still possible', 'B1', None, 0.45, '', {'v': 'achievement, power', 'world': {'tribal': 'send the hunters to the bands still undecided, where it can still be won', 'magic': 'send the runners to the next ward, where the lots are still close'}, 'chance': 0.7}),
    ('throw everyone at the ward anyway, in one last loud weekend', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'mark': 'took a wild risk', 'world': {'tribal': 'send everyone to the far bands anyway, singing, in one last loud push', 'magic': 'throw every runner at the ward anyway, in one last loud day'}, 'chance': 0.3}),
    ('send them to the streets you know will turn out if someone knocks twice', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'send them to the hearths you know will stand up if asked twice', 'magic': 'send them to the lanes you know will turn out if someone knocks twice'}, 'chance': 0.7}),
    ('log every door this weekend, so the next campaign knows the ward', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'mark every hearth visited, so the next speaker knows the band', 'magic': 'keep a roll of every door this day, so the next campaign knows the ward'}, 'chance': 0.7}),
    ('send the region inflated canvass returns, so it backs the ward next time', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'mark': 'hid a wrong', 'closed': 'approval: false canvass figures sent to the party; backfire: the count shows the gap, and the region stops trusting the figures', 'world': {'tribal': 'tell the faction head more hearths stand with the speaker than really do', 'magic': "send the faction's house inflated tallies, so it backs the ward next time"}, 'chance': 0.85}),
    ('promise the volunteers a party at your own expense if they double the doors', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, achievement', 'world': {'tribal': 'promise the hunters a feast from your own stores if they reach every band', 'magic': 'promise the runners a night at the tavern on your purse if they double the doors'}, 'chance': 0.9}),
    ("knock doors all weekend yourself, beside the candidate's oldest friends", 'R1', 'G.7', 0.5, '', {'v': 'benevolence, tradition', 'body': 'light', 'world': {'tribal': "walk to the far hearths yourself, beside the speaker's oldest kin"}, 'self_control': '+', 'chance': 0.9}),
    ('keep the volunteers on the home ward, as you promised the branch', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'mark': 'kept your word', 'world': {'tribal': "keep the hunters among the band's own hearths, as you promised the elders", 'magic': 'keep the runners in the home ward, as you promised the faction'}, 'chance': 0.85}),
 ]},
{'name': 'the candidate goes off script',
 'stages': 'young_adult adult mature',
 'age': (18, 70),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, rival',
 'requires': 'campaign organiser',
 'worlds': {'earth': 'at noon the candidate said something careless on camera, and by two the clip is on every phone '
                     'in the ward',
            'tribal': "the speaker insulted a rival clan's elder in front of the gathering's runners, and the "
                      'singers have the line already',
            'magic': 'the candidate mocked the Order in the market square, and the broadsheet writers took it down '
                     'word for word'},
 'timing': {'times': "per campaign organiser: about one campaign in three has a candidate's slip that spreads "
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'At a market stall at noon {boss}, the candidate, made a careless joke about the people of '
                       'the next town. By two the clip is on every phone in the ward, and {rival} has shared it '
                       'twice.'),
                      ('W',
                       'There are nine days left and a code of conduct the campaign signed in public. {N} reads it '
                       'again with the clip playing on mute.'),
                      ('U',
                       '{N} watches the clip frame by frame. Cut ten seconds earlier it means something else, and '
                       'the other side has cut it ten seconds earlier.'),
                      ('B',
                       "A good organiser can turn a bad day into a story about the other side's dirty tricks. {N} "
                       'has done it before.'),
                      ('R',
                       '{N} wants to throw the phone across the office, then drive to wherever {boss} is and have it '
                       'out face to face.'),
                      ('G',
                       "The town the joke was about is where half the volunteers' families come from. {N} can "
                       'already hear what will be said at the school gates.')],
            'tribal': [('',
                        "At the trading place {boss}, the band's speaker, mocked an elder of the river clan in front "
                        'of runners from three bands. By dusk the singers are already making it a song.')],
            'magic': [('',
                       "In the market square {boss} made a jest at the Order's expense, before a crowd and two "
                       'broadsheet writers. By the evening bell the words are pasted on the tavern doors.')]},
 'outcomes': (['By the end of the week the story has moved on, and the campaign is still standing.',
               'The helpers turn out at the end of the week in bigger numbers than before.'],
              ['The slip is all anyone talks about for days, and support slips away street by street.',
               '{boss} blames {N} for the way it was handled, in front of the whole team.']),
 'options': [
    ('get the candidate to apologise in plain words before the evening news', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'mark': 'owned up', 'world': {'tribal': "bring the speaker to the elder's hearth to say sorry before dusk", 'magic': 'have the candidate apologise in plain words before the evening bell'}, 'chance': 0.5}),
    ('put out the full, uncut clip, so people can judge the words in context', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'grants': 'handling the press', 'world': {'tribal': 'get the runners who were there to tell the whole of what was said', 'magic': 'send the heralds the whole of what was said, word for word'}, 'chance': 0.7}),
    ('say the clip was doctored by the other side', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: a false claim that the clip was faked; backfire: the full recording surfaces, and the story doubles', 'world': {'tribal': "say the rival clan's runners twisted the speaker's words", 'magic': "say the broadsheet writers twisted the candidate's words"}, 'chance': 0.4}),
    ('quit on the spot, rather than defend that', 'R1', None, 0.45, '', {'v': 'self-direction', 'drops': 'campaign organiser', 'chance': 0.95}),
    ('let it blow over; the ward has heard worse, and knows the candidate', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'let it pass; the bands have heard worse, and know the speaker', 'magic': 'let it blow over; the ward has heard worse, and knows the candidate'}, 'chance': 0.45}),
    ('write down exactly what was said and when, for the record and the lawyers', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'fix the exact words in memory, for when the elders ask', 'magic': "write down exactly what was said and when, for the faction's clerk and the record"}, 'chance': 0.9}),
    ('dig up something worse the other candidate said last year, and push it out', 'U1', 'B.7', 0.5, '', {'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': "remind the bands of something worse the rival's speaker said last winter", 'magic': 'find something worse the rival candidate said last year, and give it to the heralds'}, 'chance': 0.75}),
    ('hide the candidate for two days, and send the loudest volunteers out instead', 'B1', 'R.7', 0.5, '', {'v': 'security, stimulation', 'world': {'tribal': 'keep the speaker at the camp, and send the boldest young hunters out instead', 'magic': 'keep the candidate indoors, and send the loudest runners out instead'}, 'chance': 0.75}),
    ('take the candidate to that town tonight, to face its people in person', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'body': 'light', 'world': {'tribal': "take the speaker to the river clan's fire tonight, to face its people", 'magic': "take the candidate to the Order's hall tonight, to face its wardens"}, 'chance': 0.6}),
    ('ask the elders of that town how amends are properly made there', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': "ask the river clan's elders how amends are properly made", 'magic': "ask the Order's old wardens how amends are properly made"}, 'chance': 0.75}),
 ]},
{'name': 'news the boss does not want to hear',
 'stages': 'young_adult adult mature',
 'age': (20, 75),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, colleague',
 'requires': 'political adviser',
 'worlds': {'earth': 'an evening in the office before the big announcement, and you know something about it the boss '
                     'does not want to hear',
            'tribal': "the speaker means to promise the hunt's share away at the fire tomorrow, and you know the "
                      'herds have not come',
            'magic': 'the councillor will read a decree at dawn that you know is flawed, and the seal is already on '
                     'it'},
 'timing': {'times': 'per political adviser a year: several times a year an adviser holds news the boss will not '
                     'like; about 1 life in 330 works as an adviser or staffer (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'It is eight in the evening, and the announcement is at ten tomorrow. {N} has just found that '
                       'the costings count the same money twice, and {boss} is in a good mood for the first time in '
                       'a month.'),
                      ('W',
                       'An adviser serves the office, not the mood in it. {N} also knows that {boss} will stand up '
                       'tomorrow and say these numbers in public, in good faith.'),
                      ('U',
                       '{N} checks the sums a third time, then a fourth. The error is real, and {N} can see exactly '
                       'where it came from.'),
                      ('B',
                       '{colleague} wrote the costings and is up for the same promotion as {N}. Whoever brings the '
                       'problem in will be remembered, one way or the other.'),
                      ('R',
                       '{N} can feel the words already in {Ns} mouth, too hot to hold. Saying them will spoil the '
                       'evening; not saying them will spoil something worse.'),
                      ('G',
                       '{N} has seen this before, in another office under another boss: a mistake let slide at night '
                       'becomes a scandal by spring. Some things do not change.')],
            'tribal': [('',
                        "{boss}, the band's speaker, means to tell the gathering tomorrow that the band will give "
                        'half its hunt to the river clans. {N} has walked the valley all week and knows the herds '
                        'have not come.')],
            'magic': [('',
                       "The decree lies on the councillor's desk with the seal already on it, to be read at dawn. "
                       "{N} has found the clause that would hand the town's grain store to the wrong guild.")]},
 'outcomes': (['The announcement goes out with true numbers, and nobody outside the office ever knows how close it '
               'came.',
               '{boss} listens, swears once, and thanks {N} the next morning.'],
              ['The announcement goes out as it was, and the error is found within a week.',
               '{boss} takes the news badly, and {N} is left out of the next meeting that matters.']),
 'options': [
    ('write a formal note of the error tonight, so it is on record before morning', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'tell the eldest of the band tonight, so it is known before morning', 'magic': 'write a sealed note of the error tonight, so it is on record before dawn'}, 'chance': 0.7}),
    ('fix the costings overnight, so the boss has true numbers to announce', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'walk the valley through the night, so the speaker has a true count of the herds', 'magic': 'redraft the decree overnight, so the councillor has a sound text to read'}, 'chance': 0.5}),
    ('make sure the colleague who wrote the costings is the one who tells the boss', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'make sure the hunter who counted the herds is the one who tells the speaker', 'magic': 'make sure the clerk who drafted it is the one who tells the councillor'}, 'chance': 0.9}),
    ('tell the boss straight, now, even if it ruins the evening', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'grants': 'a name for straight talk', 'chance': 0.65}),
    ('break it gently, starting with all that still holds up in the plan', 'G1', None, 0.45, '', {'v': 'benevolence, security', 'chance': 0.7}),
    ('report it through the proper channel, with your name on the find', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'bring it to the elders as custom asks, so they know who found it'}, 'chance': 0.55}),
    ('work out a bolder announcement the true numbers can carry, and pitch it tonight', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'work out a bolder promise the true herds can bear, and put it to the speaker tonight', 'magic': 'draft a bolder decree the coffers can truly bear, and pitch it tonight'}, 'chance': 0.7}),
    ('let the announcement go ahead, and fix the sums quietly later', 'B1', 'G.7', 0.5, '', {'v': 'security, conformity', 'mark': 'hid a wrong', 'closed': "approval: a known error left in a public announcement; backfire: a journalist finds the double count, and the adviser's own notes with it", 'self_control': '-', 'world': {'tribal': 'let the speaker make the promise, and hope the herds come late', 'magic': 'let the decree be read, and amend it quietly later'}, 'chance': 0.65}),
    ('leak it to a friendly journalist tonight, so the error cannot go out', 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'closed': "approval: briefing the press behind the boss's back; backfire: the leak is traced to the adviser", 'world': {'tribal': 'tell the singers tonight, so the promise cannot be made', 'magic': 'slip it to a broadsheet writer tonight, so the decree cannot be read'}, 'chance': 0.55}),
    ('sleep on it, and read it again at six with fresh eyes before saying anything', 'G1', 'U.7', 0.5, '', {'v': 'security, self-direction', 'chance': 0.5}),
 ]},
{'name': 'a briefing off the record',
 'stages': 'young_adult adult mature',
 'age': (20, 75),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, rival, friend',
 'requires': 'political adviser',
 'worlds': {'earth': 'a journalist rings late on a Thursday and wants the line, off the record, on the row everyone '
                     'is talking about',
            'tribal': 'a singer sits down beside you at the fire and asks what the speaker really thinks',
            'magic': 'a broadsheet writer stands you a drink and asks for the inside story of the quarrel at court'},
 'timing': {'times': 'per political adviser a year: advisers who deal with the press are asked for an off-the-record '
                     'line most weeks, a hard one against a colleague a few times a year (estimate)'},
 'scenes': {'earth': [('',
                       'At ten on a Thursday {Ns} phone lights up with the name of a political journalist. The row '
                       'in the party is everywhere, and the journalist wants the line, off the record, for '
                       "tomorrow's front page."),
                      ('W',
                       'The code for advisers is plain about what may be said and by whom. {N} knows it by heart, '
                       'and knows how often it is ignored.'),
                      ('U',
                       '{N} knows what the journalist already has, and can guess what is missing. Information is a '
                       'currency, and this is a market.'),
                      ('B',
                       '{rival}, another adviser, has been briefing against {boss} for weeks. One sentence tonight '
                       'could finish {rival} and make {N} the one adviser left standing.'),
                      ('R',
                       '{N} is still angry about the meeting this afternoon, and the journalist sounds like the only '
                       'person in the city who would listen.'),
                      ('G',
                       '{N} has known this journalist for ten years, since they both started out. There are rules '
                       'between them that nobody ever wrote down.')],
            'tribal': [('',
                        'Late at the fire, a singer from another band sits down beside {N} with a skin of berry '
                        'wine. The singer wants to know what {boss}, the speaker, really thinks of the river '
                        'clans.')],
            'magic': [('',
                       'In the corner of a tavern by the Assembly, a broadsheet writer stands {N} a drink and asks, '
                       "softly, what really happened in the councillor's chamber.")]},
 'outcomes': (['The story that goes round the next morning is one {N} can live with.',
               'The confidence is kept, and the next time {N} needs a fair hearing, there is one.'],
              ["The next morning's story has {Ns} words in it, and enough detail to guess who said them.",
               'The story goes round anyway, from someone else, and it is worse.']),
 'options': [
    ('send the journalist to the press office, as the rules say', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'tell the singer to ask the speaker, as custom says', 'magic': "send the writer to the councillor's herald, as the rules say"}, 'chance': 0.9}),
    ('give the agreed line, and steer the journalist toward a better story', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'handling the press', 'world': {'tribal': 'give the singer the agreed words, and a better tale to carry instead', 'magic': 'give the agreed line, and steer the writer toward a better story'}, 'chance': 0.9}),
    ('brief against the rival adviser, off the record and untraceable', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': 'approval: briefing against a colleague; backfire: the quote is traced to the adviser', 'world': {'tribal': "whisper to the singer against the speaker's other counsellor", 'magic': 'brief the writer against the rival counsellor, unnamed'}, 'chance': 0.6}),
    ('say exactly what you think of the row, and let them print it', 'R1', None, 0.45, '', {'habit': True, 'v': 'self-direction', 'closed': 'approval: speaking to the press without leave; backfire: the boss reads it over breakfast', 'world': {'tribal': 'say exactly what you think of the quarrel, and let the singer sing it', 'magic': 'say exactly what you think of the quarrel, and let them print it'}, 'chance': 0.9}),
    ('turn it down kindly; old friends do not trade on each other', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, benevolence', 'chance': 0.95}),
    ('give the official line, and bank a favour with the journalist', 'W1', 'B.7', 0.5, '', {'v': 'power', 'world': {'tribal': "give the speaker's own words, and bank a favour with the singer", 'magic': 'give the official line, and bank a favour with the writer'}, 'chance': 0.65}),
    ('tell the true story behind the row, sourced so carefully nobody can be blamed', 'U1', 'R.7', 0.5, '', {'identity': True, 'v': 'self-direction, universalism', 'world': {'tribal': 'tell the singer the true tale, so carefully that nobody can be blamed'}, 'closed': 'approval: briefing the press without leave; backfire: the details point straight back to the adviser', 'chance': 0.7}),
    ("trade a small story about the budget to keep the journalist off the boss's family", 'B1', 'G.7', 0.5, '', {'v': 'power', 'world': {'tribal': "trade the singer a small tale to keep the speaker's family out of the songs", 'magic': "trade the writer a small story to keep the councillor's family out of print"}, 'chance': 0.65}),
    ('tell the journalist the briefing war poisons the party, and you will not join', 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'world': {'tribal': 'tell the singer the whispering poisons the faction, and you will not join'}, 'chance': 0.7}),
    ('say little, listen long, and learn what the other side is saying', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'self-direction', 'chance': 0.65}),
 ]},
{'name': 'a developer offers the town a stadium',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community',
 'horizon': 'months',
 'roles': 'colleague, rival',
 'requires': 'mayor',
 'worlds': {'earth': 'the stadium deal on the council table: a developer offers the town a new stadium, paid for, '
                     'and the price is the old park',
            'tribal': 'a neighbouring clan offers to build a great fish weir if the band gives up its spring hunting '
                      'ground',
            'magic': 'a merchant house offers a new market hall if the town gives up the old grove'},
 'timing': {'times': 'per mayor a year: about 1 in 10 face a big development offer that splits the town; about 1 '
                     'life in 500 is a mayor (catalogue share; a mayor for each of 34,875 French communes, DGCL '
                     '2025, and about 19,500 US municipalities; estimate)'},
 'scenes': {'earth': [('',
                       "The developer's model sits on the council table under a glass lid: a stadium for twelve "
                       "thousand, a proper home for the town's club, paid for in full. The price is the old park, "
                       'its lime trees and its bandstand.'),
                      ('W',
                       'A mayor answers to the whole town: the fans who have waited thirty years for a proper '
                       'ground, and the families who use the park every day.'),
                      ('U',
                       'Stadiums seldom pay back what towns are promised, and the traffic study runs to two pages. '
                       '{N} reads the offer three times and wants the real numbers.'),
                      ('B',
                       'Over dinner the developer hinted that friends of the project are well looked after. {N} '
                       'heard the hint, and has not forgotten it.'),
                      ('R',
                       'The club is in {Ns} blood. The thought of a full stadium on a cup night, the noise of it, '
                       'makes {Ns} heart race.'),
                      ('G',
                       '{N} learned to ride a bike under those lime trees. The park is older than the town hall, and '
                       'people still meet at the bandstand on summer evenings.')],
            'tribal': [('',
                        "The river clan's headman has come with gifts: his people will build a great fish weir for "
                        'the band, enough to feed it through any winter, if the band gives up its spring hunting '
                        'ground on the ridge.')],
            'magic': [('',
                       "The merchant house's envoy unrolls plans for a market hall of pale stone. The price is the "
                       'old grove beyond the east gate, where the town has gathered at midsummer for longer than '
                       'anyone can remember.')]},
 'outcomes': (["The town's decision is made in the open, and {N} can face both sides of the quarrel.",
               'The deal that comes out of it is better for the town than the first offer.'],
              ['The council splits down the middle, and the quarrel runs for a year.',
               'The offer goes to a neighbouring town instead, and half of {Ns} own town blames {N} for it.']),
 'options': [
    ('propose a bylaw that no park is ever sold without a vote of the town', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'identity': True, 'grants': 'a reform with your name on it', 'world': {'tribal': "propose a custom that no hunting ground is ever traded without the whole band's word", 'magic': 'propose a bylaw that no common land is ever sold without a vote of the town'}, 'chance': 0.2}),
    ('commission an independent study of the real costs before anything is decided', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': "send the band's best trackers to see whether a weir there would really hold fish", 'magic': 'have the guild of surveyors cost the hall honestly before anything is decided'}, 'chance': 0.95}),
    ('take a quiet share of the deal from the developer, and see it through', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': "law: a kickback on a council deal; backfire: arrested when the developer's accounts are seized", 'world': {'tribal': "take the river clan's private gifts, and see the trade through", 'magic': "take the merchant house's quiet gold, and see the deal through"}, 'chance': 0.9}),
    ('back the stadium with everything you have, and sell it to the town yourself', 'R1', None, 0.45, '', {'v': 'stimulation, achievement', 'world': {'tribal': 'back the weir with all your heart, and win the band over yourself', 'magic': 'back the market hall with all your heart, and win the town over yourself'}, 'chance': 0.45}),
    ('refuse the offer: the park stays a park', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, universalism', 'world': {'tribal': "refuse the weir: the spring hunting ground stays the band's", 'magic': 'refuse the hall: the grove stays a grove'}, 'chance': 0.85}),
    ('put the offer to a vote of the whole town, and abide by the result', 'W1', 'R.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'put the offer to the whole band at the fire, and abide by what it says'}, 'chance': 0.8}),
    ('plan the stadium on the old rail yards instead, and save the park', 'U1', 'G.7', 0.5, '', {'v': 'universalism, security', 'world': {'tribal': 'find another place for the weir, and keep the spring ground', 'magic': 'find another site for the hall, and save the grove'}, 'chance': 0.35}),
    ('squeeze the developer for a community fund and free seats for every school', 'B1', 'W.7', 0.5, '', {'v': 'universalism, power', 'world': {'tribal': 'squeeze the river clan for a share of every catch for the old and the widowed', 'magic': 'squeeze the merchant house for an almshouse and free stalls for the poor'}, 'chance': 0.55}),
    ('walk the park and the rail yards with the fans and the dog walkers, and listen', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'world': {'tribal': 'walk the ridge and the river with the hunters and the fishers, and listen', 'magic': 'walk the grove and the market with the townsfolk, and listen'}, 'chance': 0.7}),
    ('stall the developer for a year, and let the offer grow', 'G1', 'B.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'keep the river clan waiting a year, and let the gifts grow', 'magic': 'keep the merchant house waiting a year, and let the offer grow'}, 'chance': 0.6}),
 ]},
{'name': 'the bins have not been collected',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.05,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community',
 'horizon': 'week',
 'roles': 'colleague, rival',
 'requires': 'mayor',
 'worlds': {'earth': 'rubbish piling up in the high street: the bin crews are on strike in a heatwave, and the town '
                     'blames the mayor',
            'tribal': "the camp's middens overflow in the heat, and the families quarrel over whose turn it is to "
                      'carry them away',
            'magic': "the city's refuse-golems have stopped working, the carters strike rather than do their work, "
                     'and the lanes stink in the heat'},
 'timing': {'times': 'per mayor a year: a failure of a basic service that the town blames on the mayor comes most '
                     'years (estimate)'},
 'scenes': {'earth': [('',
                       'Day nine of the bin strike, and the hottest week of the year. Rubbish bags are stacked '
                       'against the war memorial, the gulls have found them, and the local paper has {Ns} photograph '
                       'on the front page next to a rat.'),
                      ('W',
                       'The crews have a fair grievance about pay, and the town has a fair grievance about the '
                       'smell. {N} is mayor of both.'),
                      ('U',
                       'The contract, the budget and the strike ballot are spread across {Ns} desk. Somewhere in '
                       'them is the clause or the figure that unlocks this.'),
                      ('B',
                       '{rival}, who leads the opposition on the council, has called for {N} to resign by Friday. A '
                       'quick win this week would quiet {rival} for a year.'),
                      ('R',
                       'The smell hits {N} on the steps of the town hall, and so does the shouting of a man with a '
                       'bag of rubbish in each hand. {N} wants to shout back.'),
                      ('G',
                       'The crews are the sons and daughters of people {N} went to school with. The heat will break, '
                       'and the town will still be one town after.')],
            'tribal': [('',
                        'The middens at the edge of the camp have overflowed in the heat, and the flies are '
                        'everywhere. Two families are shouting over whose turn it was to carry the waste to the '
                        'gully, and both are looking at {N}.')],
            'magic': [('',
                       'The refuse-golems stand still in the lanes where their binding failed, and the carters have '
                       "struck rather than do the golems' work. The lanes stink, and the guild masters are at {Ns} "
                       'door.')]},
 'outcomes': (["The streets are clear by the weekend, and the town's temper cools with the weather.",
               'The settlement holds, and the town remembers who stayed in the room until it was done.'],
              ["The trouble drags into a third week, and the town's patience with {N} runs out.",
               'A settlement is struck, and falls apart two days later.']),
 'options': [
    ('sit down with the union and the contractor, and stay until there is a deal', 'W1', None, 0.45, '', {'v': 'universalism, security', 'self_control': '+', 'world': {'tribal': 'sit the two families down at your fire, and stay until it is settled', 'magic': 'sit the carters and the golem-wrights down, and stay until there is a deal'}, 'chance': 0.75}),
    ('find the money in the budget to settle the pay claim, line by line', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'work out a fair rota of turns, hearth by hearth', 'magic': "find the coin in the town's ledgers to settle the claim, line by line"}, 'chance': 0.6}),
    ('bring in private crews to clear the streets, strike or no strike', 'B1', None, 0.45, '', {'identity': True, 'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'send the young men of your own hearths to clear the middens, and settle the quarrel later', 'magic': 'hire carters from the next town to clear the lanes, strike or no strike'}, 'chance': 0.8}),
    ('put on gloves and clear the high street yourself, with whoever will help', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'body': 'heavy', 'world': {'tribal': 'carry the waste to the gully yourself, with whoever will help', 'magic': 'haul the refuse yourself, with whoever will help'}, 'self_control': '+', 'chance': 0.9}),
    ('wait for the heat to break and tempers to cool, and keep the town calm', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'wait for the heat to break and tempers to cool, and keep the camp calm'}, 'chance': 0.55}),
    ("hold an open meeting in the square, and take the town's anger in person", 'W1', 'R.7', 0.5, '', {'v': 'universalism', 'world': {'tribal': 'call the whole band to the fire, and take its anger in person'}, 'chance': 0.95}),
    ('set up street collection points, so neighbours can carry for each other', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'dig new midden pits downwind of every hearth, for families to share', 'magic': 'set up collection yards in each ward, so neighbours can carry for each other'}, 'chance': 0.8}),
    ('blame the contractor in public, and use the row to win a better contract', 'B1', 'W.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'blame the family that skipped its turn, and use it to set a firmer rota', 'magic': 'blame the golem-wrights in public, and use it to win a better charter'}, 'chance': 0.45}),
    ('go to the picket line at six and ask the crews what they really want', 'R1', 'U.7', 0.5, '', {'v': 'universalism', 'world': {'tribal': 'go to both families at dawn and ask what each of them really wants', 'magic': "go to the carters' yard at dawn and ask what they really want"}, 'chance': 0.65}),
    ("promise the foreman's nephew a council job if he talks the crews round", 'G1', 'B.7', 0.5, '', {'v': 'power, tradition', 'mark': 'hid a wrong', 'closed': 'law: a council job given as a favour; backfire: the appointment comes out, and the standards board investigates', 'world': {'tribal': "promise the old woman's grandson the best hunting place if she talks them round", 'magic': "promise the guild-father's nephew a town post if he talks the carters round"}, 'chance': 0.7}),
 ]},
{'name': 'the queue at the Friday surgery',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'partner, a constituent',
 'requires': 'member of parliament',
 'worlds': {'earth': "a library meeting room on a Friday: the member's advice surgery, and a queue out of the door "
                     'with the cases nobody else will take',
            'tribal': 'the families line up at your hearth when you come back from the gathering, each with a '
                      'grievance for the speaker',
            'magic': 'petitioners fill the hall of your town house on the weekly day, each with a seal and a '
                     'grievance'},
 'timing': {'times': 'per member of parliament: most weeks; members hold advice surgeries in the constituency most '
                     'Fridays; about 1 life in 10,000 sits in parliament (House of Commons, ONS: about 70 new '
                     'members a year against about 650,000 UK births)'},
 'scenes': {'earth': [('',
                       'The surgery starts at ten in a library meeting room. By half past, the queue is out of the '
                       "door: a visa refused, a man's benefits stopped, a pothole, a neighbour's hedge, and someone "
                       'who just wants to shout at a person with a title.'),
                      ('W',
                       'Every one of these people has a right to be heard by the member they elected, the man with '
                       'the hedge included. {N} takes each case in turn.'),
                      ('U',
                       'Most of the cases come from the same three offices, with the same three errors. {N} starts a '
                       'tally on the back of an envelope.'),
                      ('B',
                       "Two of today's cases would make good stories for the local paper. {N} notices, and is not "
                       'proud of noticing.'),
                      ('R',
                       'The woman in the third chair is in tears before she has finished sitting down, and something '
                       'in {N} goes tight and fierce.'),
                      ('G',
                       '{N} grew up four streets from this library. Some of the faces in the queue taught {N} at '
                       'school, or served {N} in the shop.')],
            'tribal': [('',
                        'Back from the gathering, {N} finds the families waiting at {Ns} hearth: a widow whose share '
                        'of the hunt was cut, two brothers quarrelling over a boundary stone, an old man who wants '
                        'the gathering to hear about the wolves.')],
            'magic': [('',
                       'On the weekly day the hall of {Ns} town house fills with petitioners: a widow with a sealed '
                       'claim, a tanner shut out of his guild, a farmer whose road the Order has closed.')]},
 'outcomes': (['Most of those waiting leave with a promise and a date, and a few with the thing they came for.',
               'One case that has been stuck for two years moves at last, and the family tells the whole street.'],
              ['The cases pile up faster than they can be chased, and three people come back next week, angrier.',
               'The day runs three hours over, and {partner} eats alone again.']),
 'options': [
    ('see every person in the queue, in order, however long it takes', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'habit': True, 'self_control': '+', 'world': {'tribal': 'hear every family that waits, in turn, however long it takes', 'magic': 'hear every petitioner, in order, however long it takes'}, 'chance': 0.7}),
    ('spot the pattern in the cases, and write to the office that causes them', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': "see what the grievances have in common, and take it to the chief's speakers", 'magic': 'spot the pattern in the petitions, and write to the office of the Crown behind them'}, 'chance': 0.85}),
    ('pick the two cases that will make the local paper, and make sure they do', 'B1', None, 0.45, '', {'habit': True, 'v': 'power, achievement', 'world': {'tribal': 'pick the two grievances the singers will love, and make sure they hear them', 'magic': 'pick the two petitions the broadsheets will love, and make sure they print them'}, 'chance': 0.9}),
    ('take up the case of the woman in tears on the spot, while she waits', 'R1', None, 0.45, '', {'v': 'benevolence', 'mark': 'helped someone in need', 'chance': 0.95}),
    ('listen to the man who only wants to shout, until he runs out of shouting', 'G1', None, 0.45, '', {'v': 'benevolence', 'world': {'tribal': 'let the old man talk about the wolves until he has said it all', 'magic': 'hear the angriest petitioner out, until he has said it all'}, 'chance': 0.5}),
    ('start a monthly surgery on the far estate, where nobody comes to the library', 'W1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'walk to the far hearths each moon, so they need not come to yours', 'magic': 'hold a monthly hearing in the poorest ward, where nobody comes to the town house'}, 'chance': 0.7}),
    ('keep a file on every case, so each one is chased to the end', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'habit': True, 'grants': 'constituency casework', 'world': {'tribal': 'keep every grievance in memory, and ask after each one at the next gathering', 'magic': 'keep a ledger of every petition, so each one is chased to the end'}, 'self_control': '+', 'chance': 0.95}),
    ("use your title to make the ministry's officials explain the visa rule in full", 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'power, achievement', 'world': {'tribal': "use your place at the gathering to make the chief's speakers explain the cut shares", 'magic': "use your seat to make the Crown's clerks explain the closed road in full"}, 'chance': 0.65}),
    ('raise the case of the woman in tears in the chamber, loudly, with cameras on', 'R1', 'B.7', 0.5, '', {'v': 'power, benevolence', 'world': {'tribal': "raise the widow's grievance at the gathering, loudly, with the singers listening", 'magic': "raise the widow's claim in the Assembly, loudly, with the heralds listening"}, 'chance': 0.65}),
    ('after the last case, join the street party next door and stay till dark', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'after the last grievance, join the dancing at the next hearth until the fire dies', 'magic': 'after the last petition, join the fair in the square until dark'}, 'chance': 0.95}),
 ]},
{'name': 'the whip on the phone',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, friend',
 'requires': 'member of parliament',
 'worlds': {'earth': "the whip's call on the train home: the party needs your vote on Tuesday for a bill the "
                     'constituency hates',
            'tribal': 'the faction head tells you how to speak at the gathering tomorrow, and it goes against what '
                      'your own hearths want',
            'magic': "the faction's warden comes with the line for tomorrow's vote in the Assembly, and it goes "
                     'against the town that sent you'},
 'timing': {'times': 'per member of parliament a year: a whipped vote the member dislikes comes several times a '
                     'year, a hard one against the constituency about once a year (estimate)'},
 'scenes': {'earth': [('',
                       "The whip, {boss}, rings as the train pulls out. Tuesday's bill moves the regional depot, and "
                       'its six hundred jobs, out of {Ns} constituency, and the party needs every vote.'),
                      ('W',
                       'The party stood on a manifesto, and the bill is in it. {N} was elected on that manifesto '
                       'too, and also on a hundred doorstep promises about the depot.'),
                      ('U',
                       'The bill has a clause, deep in its fourth schedule, that could be amended to keep the depot '
                       'open. {N} has read it twice.'),
                      ('B',
                       '{boss} does not threaten, and does not need to. The reshuffle is in the spring, and everyone '
                       'knows who draws up the list.'),
                      ('R',
                       '{N} promised on a hundred doorsteps to fight for that depot. The promise is still warm, and '
                       'so is {Ns} temper.'),
                      ('G',
                       'Half the families on {Ns} own street have someone at the depot. {N} will see them in the '
                       'shop on Saturday.')],
            'tribal': [('',
                        '{boss}, the faction head, sits by {N} at the edge of the gathering: tomorrow the faction '
                        'will speak for giving the upper valley to the river clans, and {N} will speak for it too. '
                        '{Ns} own hearths hunt in the upper valley.')],
            'magic': [('',
                       "{boss}, the faction's warden, arrives at {Ns} rooms with the line for tomorrow's vote in the "
                       'Assembly: a new tax on river tolls that will ruin the town that sent {N}.')]},
 'outcomes': (['The vote is cast, and {N} can explain it to anyone in the place that sent {N}.',
               'The measure is changed at the last minute, and the town keeps half of what it stood to lose.'],
              ['{boss} remembers, and {Ns} name drops off the list of those who will rise.',
               'The people back home hear of the vote before {N} can explain it, and the welcome there turns cold.']),
 'options': [
    ('vote with the party, though you promised the town otherwise', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'broke your word', 'self_control': '-', 'world': {'tribal': 'speak as the faction says, though you promised your hearths otherwise', 'magic': 'vote with the faction, though you promised the town otherwise'}, 'chance': 0.85}),
    ('table an amendment to save the depot, worded so the whips can accept it', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'knowing the rules of the house', 'world': {'tribal': 'find words for the gathering that give the river clans the valley and your hearths their hunting', 'magic': 'draft an amendment to spare the town, worded so the faction can accept it'}, 'chance': 0.3}),
    ('trade your vote for new jobs in the constituency, promised in writing', 'B1', None, 0.45, '', {'v': 'power, achievement', 'binds': True, 'world': {'tribal': "trade your voice for the faction's promise of a share in the river clans' catch", 'magic': "trade your vote for the faction's sealed promise of trade for the town"}, 'chance': 0.4}),
    ('rebel and vote against, and tell the whip why to their face', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'identity': True, 'mark': 'defied an authority', 'takes_if_fails': 'the party whip', 'world': {'tribal': 'speak against the faction at the gathering, and tell its head why to their face', 'magic': 'vote against the faction, and tell the warden why to their face'}, 'chance': 0.75}),
    ('go home for the weekend, and ask the depot workers what they want', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'go back to your own hearths, and ask the hunters what they want', 'magic': 'go home to the town, and ask the toll-keepers what they want'}, 'chance': 0.55}),
    ("abstain, as the rules allow, and put the constituency's case on the record", 'W1', 'G.7', 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'keep silent at the gathering, as custom allows, and speak for your hearths at your own fire', 'magic': "abstain, as the Assembly's rules allow, and put the town's case on the record"}, 'chance': 0.5}),
    ("send the minister's officials the depot figures, so the bill is fairer", 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'world': {'tribal': "tell the chief's speakers what the upper valley feeds, so the choice is fairer", 'magic': "send the Crown's clerks the town's ledgers, so the measure is fairer"}, 'chance': 0.65}),
    ("find out from friends in the whips' office how many rebels there really are", 'B1', 'U.7', 0.5, '', {'v': 'power, security', 'world': {'tribal': 'find out from friends in the faction how many will really speak against it', 'magic': "find out from friends in the faction's house how many will really vote against it"}, 'chance': 0.8}),
    ('tell the whip loudly that you will rebel unless the depot is saved', 'R1', 'B.7', 0.5, '', {'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'tell the faction head loudly that you will speak against it unless your hearths are spared', 'magic': 'tell the warden loudly that you will vote against it unless the town is spared'}, 'chance': 0.4}),
    ('ring the old friends at the depot, and promise them a vote against', 'G1', 'R.7', 0.5, '', {'v': 'tradition, benevolence', 'binds': True, 'world': {'tribal': 'go to the old hunters, and promise them you will speak against it', 'magic': 'write to old friends at the toll-gates, and promise them a vote against'}, 'chance': 0.75}),
 ]},
{'name': 'the officials say it cannot be done',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, colleague',
 'requires': 'minister',
 'worlds': {'earth': 'a meeting room in the department, where the officials explain, politely, why the policy you '
                     'promised cannot be done',
            'tribal': 'the old hands say the hunt cannot be moved before the herds pass, whatever you promised the '
                      'families',
            'magic': 'the clerks of the Treasury say the coffers cannot bear the measure you promised the Assembly'},
 'timing': {'times': 'per minister a year: several times a year; about 1 life in 30,000 becomes a minister '
                     '(catalogue share; Institute for Government: 120 paid ministers at a time; estimate)'},
 'scenes': {'earth': [('',
                       'The permanent secretary has brought eleven officials and a forty-page paper to the meeting. '
                       'Its message, politely put, is that the policy {N} promised at the election cannot be done in '
                       'this parliament, and perhaps not at all.'),
                      ('W',
                       'The department exists to serve the government of the day, and the government promised this '
                       'in public. {N} means to keep the promise, and to keep it properly.'),
                      ('U',
                       'The paper is good. {N} reads it twice that night and finds two assumptions that might not '
                       'hold, and one that certainly does.'),
                      ('B',
                       'Officials outlast ministers; they know it, and {N} knows it. The question is who blinks '
                       'first, and {N} has eighteen months at most.'),
                      ('R',
                       '{N} feels the heat rise while the reasons why not are read out. People voted for this, and '
                       'they are tired of being told why not.'),
                      ('G',
                       '{mentor}, who held the post twenty years ago, once said that a department is like a river: '
                       'it can be steered a little, but never made to run uphill.')],
            'tribal': [('',
                        "The old hands sit at the chief's fire and shake their heads: the camp cannot move to the "
                        'coast before the herds pass, whatever {N} promised the families. They have seen it tried.')],
            'magic': [('',
                       "The clerks of the Treasury lay their ledgers on the table of the Crown's council chamber. "
                       'The coffers, they say, cannot bear the measure {N} promised the Assembly.')]},
 'outcomes': (['The promise comes back in a shape that can be done, and the work begins.',
               'The people who must carry it out leave the room surprised, and from then on bring {N} their real '
               'worries early.'],
              ['The meeting ends in polite deadlock, and the promise slips another year.',
               'Word of the quarrel gets out, and {N} and the people who must carry it out spend a month blaming '
               'each other.']),
 'options': [
    ('hold to the promise, and ask for a plan to deliver it properly, however long', 'W1', None, 0.45, '', {'v': 'conformity, security', 'binds': True, 'world': {'tribal': 'hold to the promise, and ask the old hands how it can be done properly, however long'}, 'chance': 0.65}),
    ('find the weak assumption in their paper, and ask them to cost a smaller version', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': "find the weak point in the old hands' reasons, and ask what a smaller move would take", 'magic': "find the weak figure in the clerks' ledgers, and ask them to cost a smaller measure"}, 'chance': 0.7}),
    ('overrule them in writing, and make it clear whose careers depend on it', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'overrule the old hands before the chief, and make it clear whose standing depends on it', 'magic': 'overrule the clerks under your seal, and make it clear whose posts depend on it'}, 'chance': 0.55}),
    ('announce the start date in the chamber tomorrow, and let them catch up', 'R1', None, 0.45, '', {'binds': True, 'v': 'self-direction, stimulation', 'mark': 'took a wild risk', 'world': {'tribal': 'tell the families at the next fire the day the move begins, and let the old hands catch up', 'magic': 'announce the day it begins in the Assembly tomorrow, and let the clerks catch up'}, 'chance': 0.35}),
    ('hear them out to the end, and ask what the department has tried before', 'G1', None, 0.45, '', {'v': 'tradition', 'grants': 'officials who trust you', 'world': {'tribal': "hear the old hands out to the end, and ask what was tried in their fathers' time", 'magic': 'hear the clerks out to the end, and ask what the office has tried before'}, 'chance': 0.6}),
    ('set up a proper review with outside experts, and abide by what it finds', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'universalism, achievement', 'world': {'tribal': 'ask the wisest of the other bands to judge it, and abide by what they say', 'magic': "ask the academy's scholars to review it, and abide by what they find"}, 'chance': 0.8}),
    ('run a pilot first, in towns picked to make it look good', 'U1', 'B.7', 0.5, '', {'binds': True, 'v': 'power, achievement', 'mark': 'hid a wrong', 'closed': 'approval: a pilot rigged to succeed; backfire: the evaluation finds the towns were hand-picked', 'world': {'tribal': 'try it first with the hearths most likely to make it look good', 'magic': 'try it first in the towns most likely to make it look good'}, 'chance': 0.6}),
    ('go over their heads to the leader, and have it ordered from the top', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': "go over the old hands' heads to the chief, and have it ordered from the fire", 'magic': "go over the clerks' heads to the throne, and have it ordered under seal"}, 'chance': 0.65}),
    ('go to the towns that were promised it, and tell them honestly where it stands', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'owned up', 'world': {'tribal': 'go to the families who were promised it, and tell them honestly where it stands'}, 'chance': 0.95}),
    ('build it slowly, office by office, with the people who must run it', 'G1', 'W.7', 0.5, '', {'v': 'security, conformity', 'habit': True, 'self_control': '+', 'world': {'tribal': 'build it slowly, season by season, with the hunters who must do it', 'magic': 'build it slowly, office by office, with the clerks who must run it'}, 'chance': 0.65}),
 ]},
{'name': 'defending a policy you argued against',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, rival',
 'requires': 'minister',
 'worlds': {'earth': 'the despatch box, where you must defend in the chamber a policy you argued against in cabinet',
            'tribal': 'the chief chose the war you argued against, and you must speak for it at the gathering',
            'magic': "the throne's decree goes against your counsel, and you must read it in the Assembly"},
 'timing': {'times': 'per minister a year: about 1 in 3 must defend in public a policy they argued against in '
                     'private; collective responsibility binds every minister (estimate)'},
 'scenes': {'earth': [('',
                       'Cabinet decided on Tuesday, after {N} argued against the policy for an hour. On Thursday {N} '
                       'must stand at the despatch box and defend it, with {rival} across the chamber holding a copy '
                       'of {Ns} own old speech.'),
                      ('W',
                       'Collective responsibility is the rule: argue in private, stand together in public, or leave. '
                       '{N} has always believed in that rule.'),
                      ('U',
                       '{N} can see exactly which questions {rival} will ask, and the honest answer to each one.'),
                      ('B',
                       '{boss}, the leader, is watching how {N} handles this. Defend it well and {N} rises; defend '
                       'it badly and {N} becomes the minister who could not.'),
                      ('R',
                       '{N} still thinks the policy is wrong, and every word of the prepared answer sticks a little '
                       'on the way out.'),
                      ('G',
                       '{N} has sat in this government with these people for four years. Loyalty is not only to a '
                       'policy; it is also to the people around the table.')],
            'tribal': [('',
                        '{boss}, the chief, has chosen to lead the young hunters against the river clans, though {N} '
                        'spoke against it at the fire for half a night. Tomorrow at the gathering {N} must stand and '
                        'speak for it.')],
            'magic': [('',
                       "The throne's decree goes against everything {N} counselled, and the seal is already on it. "
                       'Tomorrow {N} must read it aloud in the Assembly, before the members who heard {N} argue the '
                       'other way.')]},
 'outcomes': (['The day passes, and {N} says nothing in public that {N} cannot live with later.',
               '{boss} notes how {N} handled it, and says so afterwards, in front of the others.'],
              ['{rival} reads {Ns} old words back to the house, and the jeers follow {N} for a week.',
               'The government carries the day, and {N} goes home feeling smaller for it.']),
 'options': [
    ('resign, as the rule asks of a minister who cannot defend the policy', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'drops': 'minister', 'world': {'tribal': 'give the chief back your duty, as custom asks of a speaker who cannot speak for it', 'magic': 'return your seal of office, as the rule asks of a councillor who cannot read the decree'}, 'chance': 0.95}),
    ('defend the parts that hold up, and say as little as possible on the rest', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'speak for the parts of it that hold, and say little of the rest'}, 'chance': 0.55}),
    ('defend it in full and well, and make sure the leader knows the price', 'B1', None, 0.45, '', {'v': 'power, achievement', 'self_control': '+', 'world': {'tribal': 'speak for it in full and well, and make sure the chief knows the price', 'magic': 'read it in full and well, and make sure the throne knows the price'}, 'chance': 0.7}),
    ('tell the leader to their face that you will defend it this once, and never again', 'R1', None, 0.45, '', {'binds': True, 'v': 'self-direction', 'world': {'tribal': 'tell the chief to their face that you will speak for it this once, and never again', 'magic': "tell the throne's envoy to their face that you will read it this once, and never again"}, 'chance': 0.75}),
    ('defend it for the sake of the colleagues around the table, if not the policy', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': "speak for it for the sake of those around the chief's fire, if not the war", 'magic': 'read it for the sake of the council around the table, if not the decree'}, 'chance': 0.55}),
    ('defend it, and win a promise in cabinet to review it in a year', 'W1', 'U.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': "speak for it, and win the chief's word to weigh it again after the winter", 'magic': "read it, and win the council's promise to review it in a year"}, 'chance': 0.35}),
    ('defend it badly on purpose, so everyone sees where you really stand', 'U1', 'B.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'speak for it so flatly that everyone sees where you really stand', 'magic': 'read it so flatly that everyone sees where you really stand'}, 'chance': 0.9}),
    ('leak your doubts to a friendly journalist, and keep your post', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, power', 'mark': 'broke your word', 'closed': 'approval: breaking cabinet confidence; backfire: the leak is traced, and the leader asks for the resignation', 'world': {'tribal': 'whisper your doubts to the singers, and keep your place by the chief', 'magic': 'let your doubts slip to a broadsheet writer, and keep your seal'}, 'chance': 0.85}),
    ('defend it, and tell the chamber honestly that you lost the argument inside', 'R1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': "speak for it, and tell the gathering honestly that you lost the argument at the chief's fire", 'magic': 'read it, and tell the Assembly honestly that you lost the argument at court'}, 'chance': 0.7}),
    ('go home for the weekend first, then come back and do your duty', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'go back to your own hearth for a night first, then come back and do your duty'}, 'chance': 0.95}),
 ]},
{'name': 'the party at war with itself',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'rival, colleague',
 'requires': 'party leader',
 'worlds': {'earth': 'two wings of the party briefing against each other every morning, and both want the leader to '
                     'choose',
            'tribal': 'two family lines in the faction will not sit at the same fire, and both want the faction head '
                      'to choose',
            'magic': "two houses of the faction drew blades in the Assembly's yard, and both want the head of the "
                     'faction to choose'},
 'timing': {'times': 'per party leader a year: about 1 in 3 face open war between the wings of the party; about 1 '
                     'life in 200,000 leads a national party (catalogue share; estimate)'},
 'scenes': {'earth': [('',
                       'Every morning brings another anonymous quote in the papers, one wing of the party calling '
                       'the other traitors and the other answering in kind. {rival} leads one wing and {colleague}, '
                       'an old ally, leads the other, and both want {N} to choose before conference.'),
                      ('W',
                       'A leader is meant to lead the whole party, not one half of it. {N} believes there is a fair '
                       'way through, if both sides can be brought to the same table.'),
                      ('U',
                       '{N} has the membership surveys, the polling by wing and a list of who briefs whom. The war '
                       'is less even than the papers think.'),
                      ('B',
                       'One wing is bigger, richer and more useful. Backing it would end the war in a month, and '
                       'leave {N} with a smaller party that is entirely {Ns} own.'),
                      ('R',
                       '{N} came into politics to fight the other side, not {Ns} own. {N} is sick of the briefing, '
                       'and close to saying so in public in words that cannot be taken back.'),
                      ('G',
                       'The party is older than any of them, and older than the quarrel. {N} has seen it split '
                       'before, and seen what it took to grow back.')],
            'tribal': [('',
                        'Since the quarrel over the salmon pools, two family lines in the faction will not sit at '
                        'the same fire. Both have come to {N}: the faction head must choose, before the gathering.')],
            'magic': [('',
                       "Two houses of the faction drew blades in the Assembly's yard last night; nobody died, but "
                       'the heralds have told the whole city. Both houses want {N} to choose.')]},
 'outcomes': (['By the next great meeting the sniping has stopped, and the party looks like one party again.',
               'The quarrel is not settled, but it moves back behind closed doors.'],
              ['One wing walks out, and takes a good share of the party with it.',
               'The war goes on, and the whole party pays for it when the people next choose.']),
 'options': [
    ('call both wings to one table, and stay there until there is a deal', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': 'call both lines to one fire, and stay there until there is peace', 'magic': 'call both houses to one table, and stay there until there is a pact'}, 'chance': 0.45}),
    ('find out who briefs whom, and deal with the source of the leaks first', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'find out who carries tales to whom, and deal with the source first', 'magic': 'find out who whispers to the heralds, and deal with the source first'}, 'chance': 0.75}),
    ('back the bigger wing, and purge the plotters of the other', 'B1', None, 0.45, '', {'identity': True, 'v': 'power', 'mark': 'made an enemy', 'world': {'tribal': 'back the stronger line, and drive the plotters of the other from the faction', 'magic': 'back the stronger house, and cast the plotters of the other out of the faction'}, 'chance': 0.45}),
    ('go on air and tell both wings to stop it, in words nobody can mistake', 'R1', None, 0.45, '', {'v': 'self-direction', 'world': {'tribal': 'stand up at the fire and tell both lines to stop it, in words nobody can mistake', 'magic': 'stand on the Assembly steps and tell both houses to stop it, in words nobody can mistake'}, 'chance': 0.75}),
    ('wait, and let the quarrel burn itself out, as the old ones always have', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.4}),
    ("use the party's rules to suspend the other wing's loudest voices, and only theirs", 'W1', 'B.7', 0.5, '', {'v': 'power', 'closed': 'approval: party rules turned against one wing only; backfire: an appeal panel overturns the suspensions, and the story runs for a week', 'world': {'tribal': "use the faction's customs to bar the other line's loudest voices from the fire, and only theirs", 'magic': "use the faction's charter to suspend the other house's loudest voices, and only theirs"}, 'chance': 0.75}),
    ('write a new programme that gives both wings something to fight for', 'U1', 'R.7', 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'find a new hunt that gives both lines something to strive for together', 'magic': 'draft a new cause that gives both houses something to fight for'}, 'chance': 0.45}),
    ("give each wing's chief a post, and keep the family together", 'B1', 'G.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'give the eldest of each line a duty, and keep the family together', 'magic': 'give the head of each house an office, and keep the family together'}, 'chance': 0.75}),
    ("call a snap vote of all the members, and let them choose the party's way", 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'mark': 'took a wild risk', 'world': {'tribal': 'call the whole faction to stand behind one way or the other, tonight', 'magic': 'call a snap vote of the whole faction, and let it choose its way'}, 'chance': 0.4}),
    ("go back to the founders' words, and ask both wings to read them again", 'G1', 'U.7', 0.5, '', {'v': 'tradition, universalism', 'world': {'tribal': 'tell both lines again the story of how the faction was founded', 'magic': "read both houses the faction's founding charter, and ask them to hear it again"}, 'chance': 0.55}),
 ]},
{'name': 'the speech at the party conference',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'partner, rival',
 'requires': 'party leader',
 'worlds': {'earth': "the conference hall, and the year's speech to the party: an hour long, with the country "
                     'watching',
            'tribal': 'the great feast where the faction head speaks, and every family listens for what the year '
                      'will bring',
            'magic': "the faction's midwinter oration in the great hall, with the heralds waiting at the doors"},
 'timing': {'times': 'per party leader: once a year, at the party conference (estimate)'},
 'scenes': {'earth': [('',
                       'Five thousand members in the hall, the cameras at the back, an hour on the clock. {N} stands '
                       "in the wings with the speech in a folder and {partner}'s hand on {Ns} arm."),
                      ('W',
                       'This is the one hour of the year when the leader speaks to the whole party at once, and '
                       'through it to the country. {N} has written the duty of it into every page.'),
                      ('U',
                       'The speech has been through eleven drafts. {N} knows where every pause falls, which line the '
                       'press will quote, and which line {N} actually cares about.'),
                      ('B',
                       'Three of the people in the front row would like {Ns} job, {rival} among them. A great speech '
                       'settles that for a year.'),
                      ('R',
                       'The music starts, the hall rises, and {N} feels the old thrill run up the spine, the one '
                       'that made {N} want all this in the first place.'),
                      ('G',
                       'Somewhere in the hall are the branch members from home who knocked on doors for {N} thirty '
                       'years ago. {N} looks for their faces before the lights go up.')],
            'tribal': [('',
                        'The great feast is laid, the families sit around the long fire, and every eye turns to {N}. '
                        'What the faction head says tonight, the band will talk of until spring.')],
            'magic': [('',
                       "The great hall is lit with a thousand candles for the faction's midwinter oration. Heralds "
                       'wait at the doors to carry {Ns} words to every square in the city by morning.')]},
 'outcomes': (['The hall is on its feet at the end, and for once friend and foe agree on what {N} said.',
               'The speech gives the party something to talk about besides itself, at least until spring.'],
              ['{N} loses the thread in the twelfth minute, and the stumble is all anyone remembers.',
               'The speech is fine and forgotten within days, and the rivals in the front row look pleased.']),
 'options': [
    ('give the speech as written, a promise kept to every wing of the party', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'mark': 'kept your word', 'world': {'tribal': 'say the words as agreed with the elders, a promise kept to every family', 'magic': 'give the oration as written, a promise kept to every house of the faction'}, 'chance': 0.9}),
    ('cut the applause lines, and set out the plan in full', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement', 'world': {'tribal': 'leave out the boasting, and set out the plan for the year in full', 'magic': 'cut the flourishes, and set out the plan in full'}, 'chance': 0.75}),
    ('use the speech to send a message to the rivals in the front row', 'B1', None, 0.45, '', {'v': 'power', 'chance': 0.85}),
    ('put the text aside, and speak from the heart for the last ten minutes', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'identity': True, 'grants': 'rousing a crowd', 'world': {'tribal': 'let the agreed words go, and speak from the heart at the end', 'magic': 'put the scroll aside, and speak from the heart at the end'}, 'chance': 0.7}),
    ('tell the story of the branch where you started, and the people still there', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, benevolence', 'grants': 'a following in the party', 'world': {'tribal': 'tell the story of the hearth where you started, and the people still there', 'magic': 'tell the story of the ward where you started, and the people still there'}, 'chance': 0.8}),
    ('call the vote on your plan that afternoon, while your own delegates fill the hall', 'W1', 'B.7', 0.5, '', {'v': 'power', 'closed': 'approval: a vote timed for a hall packed with loyal delegates; backfire: the other wing cries foul, and the vote is rerun', 'world': {'tribal': 'ask the families to stand behind your plan that night, while your own kin crowd the fire', 'magic': "call the faction's vote that evening, while your own sworn men fill the hall"}, 'chance': 0.6}),
    ('slip in one bold surprise you have kept from everyone, even the speechwriters', 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'world': {'tribal': 'save one bold surprise you have told no one, not even the singer who shaped the words', 'magic': 'slip in one bold surprise you have kept from everyone, even your rhetor'}, 'mark': 'took a wild risk', 'chance': 0.75}),
    ('promise the region that always backs the party a new hospital', 'B1', 'G.7', 0.5, '', {'v': 'power', 'binds': True, 'world': {'tribal': 'promise the bands that always stand with the faction a share of the best hunting', 'magic': 'promise the city that always backs the faction a new infirmary'}, 'chance': 0.65}),
    ("admit the party's mistakes of the last year, out loud, in front of everyone", 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'mark': 'owned up', 'world': {'tribal': "admit the faction's mistakes of the last year, aloud, before every family"}, 'chance': 0.85}),
    ('practise it one last time in the hotel room, with only your partner listening', 'G1', 'U.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': 'say it through one last time by your own fire, with only your partner listening', 'magic': 'practise it one last time in your rooms, with only your partner listening'}, 'chance': 0.95}),
 ]},
{'name': 'the call at three in the morning',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'partner, colleague',
 'requires': 'head of government',
 'worlds': {'earth': 'a phone by the bed at three in the morning, and a decision that cannot wait for cabinet',
            'tribal': 'a runner at dawn with news of raiders on the eastern ridge, and the chief must decide before '
                      'the sun is up',
            'magic': "a warden at the Chancellor's door before dawn, with news that cannot wait for the council"},
 'timing': {'times': 'per head of government a year: several times a year a crisis needs a decision at night; about '
                     '1 life in two to three million heads a government (catalogue share; the UK has had 17 prime '
                     'ministers since 1945)'},
 'scenes': {'earth': [('',
                       'The phone by the bed rings at five past three, and {partner} turns over without waking. The '
                       'river above the city is rising faster than any model said, the barrier may not hold until '
                       'morning, and the question is whether to wake sixty thousand people and move them now, in the '
                       'dark.'),
                      ('W',
                       'There is a procedure for this, written by people who thought hard about it in calmer times. '
                       'There is also no time for most of it.'),
                      ('U',
                       'The engineers give one chance in four that the barrier fails tonight. {N} asks them, twice, '
                       'what that number is made of.'),
                      ('B',
                       'Whatever happens, the decision will carry {Ns} name. Move them for nothing and be mocked; '
                       'leave them and be blamed for ever.'),
                      ('R',
                       '{N} is out of bed and half dressed before the official has finished the first sentence, '
                       'heart going hard.'),
                      ('G',
                       '{N} knows the city on the river: the old quarter, the care homes by the water, the families '
                       'who have lived through floods before and will not want to leave.')],
            'tribal': [('',
                        'A runner stumbles into the camp before dawn: raiders have been seen on the eastern ridge, a '
                        "day's walk from the river camps. The chief must choose before sunrise whether to move the "
                        'families or stand.')],
            'magic': [('',
                       "A warden stands at the Chancellor's door before the first bell: the old wards on the "
                       'northern dam are failing, and the river city below it sleeps. The council cannot be gathered '
                       'before dawn.')]},
 'outcomes': (['By morning the danger has passed, and the choice made in the night looks like the right one.',
               'The people are safe, whatever the night cost, and {N} can stand by every word of it.'],
              ['The decision comes late, the night does real damage, and there will be questions for a year.',
               'The danger never comes, and {N} spends a week answering for the panic.']),
 'options': [
    ('follow the emergency plan to the letter, and order the move', 'W1', None, 0.45, '', {'v': 'security, conformity', 'world': {'tribal': 'do as the old custom for raids says, and move the families to the high camp', 'magic': "follow the Order's old protocol for the dam to the letter, and order the city emptied"}, 'chance': 0.8}),
    ('ask the engineers for one more reading in an hour, then decide', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'send scouts to count the raiders, and decide when they return', 'magic': 'ask the wardens for one more reading of the wards in an hour, then decide'}, 'chance': 0.75}),
    ('wake the two ministers you trust most, decide with them, and own it', 'B1', None, 0.45, '', {'identity': True, 'v': 'power', 'world': {'tribal': 'wake the two speakers you trust most, decide with them, and own it', 'magic': 'wake the two councillors you trust most, decide with them, and own it'}, 'chance': 0.7}),
    ('order the move now, and go to the river yourself before dawn', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'body': 'light', 'world': {'tribal': 'order the families moved now, and go to the eastern camps yourself before dawn', 'magic': 'order the city emptied now, and ride to the dam yourself before dawn'}, 'chance': 0.75}),
    ('do what the old flood wardens of that river advise', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'do what the oldest hunters of the eastern camps advise', 'magic': 'do what the old dam-keepers of that river advise'}, 'chance': 0.85}),
    ("use the law's emergency powers, and act at once without waiting for anyone", 'W1', 'R.7', 0.5, '', {'v': 'security, self-direction', 'world': {'tribal': "act at once on the chief's own word, without waiting for the council", 'magic': "use the Chancellor's emergency seal, and act at once without waiting for anyone"}, 'chance': 0.85}),
    ('move the old quarter and the care homes first, where the water comes first', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'move the old and the mothers with babies first, from the camps nearest the ridge', 'magic': 'empty the low quarter and the almshouses first, where the water comes first'}, 'chance': 0.8}),
    ('decide with the ministers, and make sure the record shows who advised what', 'B1', 'W.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'decide with the speakers, and make sure the band remembers who advised what', 'magic': 'decide with the councillors, and have the clerks record who advised what'}, 'chance': 0.75}),
    ('go to the barrier yourself, and look at it with the engineers', 'R1', 'U.7', 0.5, '', {'v': 'self-direction, achievement', 'body': 'light', 'world': {'tribal': "climb the ridge yourself with the scouts, and see the raiders' fires", 'magic': 'go to the dam yourself, and look at the failing wards with the wardens'}, 'chance': 0.6}),
    ("ring the city's own mayor, and let the call be theirs, with your backing", 'G1', 'B.7', 0.5, '', {'v': 'tradition', 'world': {'tribal': 'send word to the head of the eastern camp, and let the call be theirs, with your backing', 'magic': "send to the city's burgomaster, and let the call be theirs, with your backing"}, 'chance': 0.7}),
 ]},
{'name': 'a decision nobody else can take',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'years',
 'roles': 'colleague, rival',
 'requires': 'head of government',
 'worlds': {'earth': 'a long table with the cabinet, and a slow, divisive choice that has waited ten years for '
                     'someone to make it',
            'tribal': 'whether the clans move to the coast before winter, a choice every chief before you has put '
                      'off',
            'magic': 'whether to open the old gate the Orders have kept shut for three hundred years'},
 'timing': {'times': 'per head of government a year: about once or twice (estimate)'},
 'scenes': {'earth': [('',
                       'The report on the new airport is the fourth in ten years. There are three sites, each '
                       "someone's home and someone's living, and four governments have put the choice off. The "
                       'cabinet sits round the long table, and everyone is looking at {N}.'),
                      ('W',
                       'The decision must be fair to every region and stand up in any court. {N} wants it made '
                       'properly, and made once.'),
                      ('U',
                       '{N} has read all four reports, and the numbers have barely moved since the first. What has '
                       'changed is how long the country has waited.'),
                      ('B',
                       'Whichever site is chosen, three seats will be lost and a generation of jobs won. {N} can '
                       'count both, and so, across the table, can {rival}.'),
                      ('R',
                       '{N} is tired of reports. Someone has to say a place out loud and take the blow, and {N} '
                       'would rather it was today.'),
                      ('G',
                       'Each site is a village with a church, a pub and families who have farmed there for '
                       'centuries. {N} has walked all three.')],
            'tribal': [('',
                        'For four winters every chief has put it off: whether the clans leave the valley for the '
                        'coast, where the fish are, or stay where their grandparents lie. The speakers sit around '
                        'the fire and wait for {N} to say it.')],
            'magic': [('',
                       'For three hundred years the Orders have kept the old gate under the mountain shut. Now the '
                       "realm's trade is failing, the merchants beg for it to be opened, and the council waits for "
                       'the Chancellor to decide.')]},
 'outcomes': (['The decision is taken at last, and the country, grumbling, gets on with it.',
               'Years later the choice made at that table looks wiser than anyone said at the time.'],
              ['The decision is taken, then unpicked piece by piece over the next two years.',
               'The table splits, the quarrel leaks, and the thing is put off for whoever comes next.']),
 'options': [
    ('put it to the people in a vote, and abide by the result', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'binds': True, 'world': {'tribal': 'put it to every clan at the gathering, and abide by what they choose', 'magic': 'put it to the Assembly in a vote, and abide by the result'}, 'chance': 0.4}),
    ('take the best of the four reports, and decide by the evidence', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, universalism', 'world': {'tribal': 'hear every scout and elder who has seen the coast, and decide by what they know', 'magic': "take the best of the scholars' reports, and decide by the evidence"}, 'chance': 0.75}),
    ('choose the site that costs your own side least, and say so plainly', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'choose the way that keeps your own faction strongest, and say so plainly', 'magic': 'choose the way that serves your own faction best, and say so plainly'}, 'chance': 0.75}),
    ('name the site at the table today, and take the storm that follows', 'R1', None, 0.45, '', {'v': 'self-direction, achievement', 'identity': True, 'world': {'tribal': 'say at the fire tonight which way the clans go, and take the storm that follows', 'magic': 'say at the council table today whether the gate opens, and take the storm that follows'}, 'chance': 0.45}),
    ('put it off another year, and let the country come to it in its own time', 'G1', None, 0.45, '', {'v': 'tradition', 'self_control': '-', 'world': {'tribal': 'put it off another winter, and let the clans come to it in their own time', 'magic': 'put it off another year, and let the realm come to it in its own time'}, 'chance': 0.3}),
    ('give parliament a free vote, and let members follow their hearts', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'world': {'tribal': 'let every speaker at the gathering stand where the heart says, free of the factions', 'magic': 'give the Assembly a free vote, and let members follow their hearts'}, 'chance': 0.65}),
    ('commission a fifth report, and leave the choice for later', 'U1', 'G.7', 0.5, '', {'v': 'security, tradition', 'self_control': '-', 'world': {'tribal': 'send scouts to the coast once more, and leave the choice for another winter', 'magic': 'ask the scholars for one more report, and leave the gate for later'}, 'chance': 0.4}),
    ('buy off the losing region with a package so big nobody can call it unfair', 'B1', 'W.7', 0.5, '', {'v': 'power, universalism', 'world': {'tribal': 'give the clans who lose so many gifts that nobody can call it unfair', 'magic': 'grant the losing guilds so much that nobody can call it unfair'}, 'chance': 0.5}),
    ('visit all three places in one week, and decide on what you see', 'R1', 'U.7', 0.5, '', {'v': 'self-direction', 'body': 'light', 'world': {'tribal': 'walk to the coast and back yourself, and decide on what you see', 'magic': "go down to the gate yourself with the Orders' wardens, and decide on what you see"}, 'chance': 0.9}),
    ('let the cabinet argue it out until the strongest view wins, and back it', 'G1', 'B.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'let the speakers argue it out until the strongest voice wins, and back it', 'magic': 'let the council argue it out until the strongest voice wins, and back it'}, 'chance': 0.85}),
 ]},
{'name': 'the first full council meeting',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, community',
 'horizon': 'week',
 'roles': 'boss, colleague, elder',
 'requires': 'local councillor',
 'threshold': 'title:local councillor',
 'step': 1,
 'worlds': {'earth': 'the first full meeting of the council: an agenda of two hundred pages, a seat on the back '
                     'benches and a vote on the first night',
            'tribal': 'the first council fire at which you sit among the voices, and the elders watch to see whom '
                      'you look to before you speak',
            'magic': 'the first sitting of the town council in the guild hall: a carved bench, a sealed roll of '
                     'business and a vote before the evening bell'},
 'timing': {'times': 'per new local councillor: once, in the first weeks after taking the title; about 1 life in 100 '
                     '(catalogue share)'},
 'trigger': {'requires': 'in the threshold season of local councillor, within the first six months after taking the '
                         "title (opened by 'polling day in the ward' or any other way in): step 1, the first weeks "
                         'in the seat',
             'likelier': "a first seat, won at the last election; a council where the person's side has just come to "
                         'power; a full agenda in the first month',
             'rarer': 'a seat taken by someone who served the council for years as an officer or a clerk; a small '
                      'parish council that meets a few times a year'},
 'scenes': {'earth': [('',
                       'The agenda for {Ns} first full council meeting runs to two hundred pages, and the vote on '
                       'the bins is the first item. {N} sits in the back row of the chamber behind a name card, and '
                       '{boss} leans over to say which way the group is voting.'),
                      ('W',
                       '{N} has read the standing orders twice and knows when a member may speak, how to second a '
                       'motion and what a point of order is. It feels like learning the rules of a new house.'),
                      ('U',
                       '{N} has tabbed every report and found two figures in the budget papers that do not add up.'),
                      ('B',
                       '{N} watches whom the officers defer to, who sits beside the leader, and which committee '
                       'chairs are still unfilled.'),
                      ('R',
                       '{N} wants to stand up on the first night and say what the ward sent {N} here to say, '
                       'procedure or not.'),
                      ('G',
                       '{N} sits in the seat that a councillor from the same streets held for twenty years, and '
                       'feels the weight of everyone who sat there before.')],
            'tribal': [('',
                        '{N} sits for the first time among the voices at the council fire, close enough to feel its '
                        'heat. The elders watch to see whom {N} looks to before speaking.')],
            'magic': [('',
                       'In the guild hall {N} takes a carved bench for the first time, and the clerk unrolls the '
                       "evening's business under the warded lamps.")]},
 'outcomes': (['By the end of the night {N} knows where to sit, when to speak and whom to ask.',
               '{boss} catches {N} on the way out and says it was a good first meeting.'],
              ['The meeting runs late into the night, and {N} goes home having understood half of it.',
               'Something {N} said or did on the first night is all anyone talks about the next morning, and not '
               'kindly.']),
 'options': [
    ('learn the standing orders by heart before speaking once in the chamber', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'learned a skill', 'world': {'tribal': 'learn the customs of the council fire by heart before speaking once', 'magic': "learn the council's rules and rites by heart before speaking once"}, 'chance': 0.9}),
    ('read every report, and ask the officers about the two figures that do not add up', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'world': {'tribal': "hear every family's account, and ask the elders about the two that do not agree", 'magic': 'read every roll, and ask the clerks about the two sums that do not add up'}, 'chance': 0.84}),
    ('ask the leader for a seat on the planning committee in the first week', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'ask the head of the faction for a place among those who choose the next camp', 'magic': "ask the faction's lord for a seat on the council's building committee"}, 'chance': 0.4}),
    ("stand up on the first night and speak about the ward's worst street, unscripted", 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'speak at the first fire about the hearths that flood every spring, as the words come', 'magic': "rise at the first sitting and speak about the ward's worst lane, unscripted"}, 'chance': 0.75}),
    ('ask the longest-serving councillor how things are really done here', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'made a friend', 'world': {'tribal': 'ask the oldest voice at the fire how things are really decided'}, 'chance': 0.84}),
    ('sign up for every training session the council runs for new members', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'sit with the elders each evening to learn the old judgments', 'magic': "attend every lesson the council's clerks give new members"}, 'chance': 0.95}),
    ('map who chairs what, who votes with whom and where the deals are made', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'work out who speaks for whom, which families stand together and where bargains are struck'}, 'chance': 0.75}),
    ('vote against your own group on the first night, to show your vote is your own', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, power', 'mark': 'defied an authority', 'world': {'tribal': 'stand against your own faction at the first fire, to show your voice is your own', 'magic': 'cast against your own faction at the first sitting, to show your vote is your own'}, 'chance': 0.75}),
    ('bring a few neighbours from the ward to sit in the public gallery', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'bring families from your own hearths to sit at the edge of the firelight', 'magic': "bring neighbours from the ward to the hall's public benches"}, 'chance': 0.94}),
    ('report back after every meeting in the community hall, as your predecessor always did', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'go back to your own hearths after every fire and tell them what was said', 'magic': "report back after every sitting in the ward's tavern, as the old member always did"}, 'chance': 0.86}),
 ]},
{'name': 'the casework that never stops',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'public life, family',
 'horizon': 'months',
 'roles': 'partner, colleague, boss',
 'requires': 'local councillor',
 'threshold': 'title:local councillor',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the emails, the calls and the knocks at the door have not stopped, and the day '
                     'job and the family are paying for it',
            'tribal': 'two moons in, the families bring their quarrels to your hearth morning and night, and your '
                      'own kin eat alone',
            'magic': 'ten weeks in, petitions come under the door every day, sealed and unsealed, and your own trade '
                     'waits'},
 'timing': {'times': 'per new local councillor: once, about ten weeks into the threshold season, for about half of '
                     "new councillors (the season's middle step brings this moment or 'whose councillor you are'); "
                     'about 1 life in 100 sits on a council (catalogue share), so about 1 in 200 meet it'},
 'trigger': {'requires': 'in the threshold season of local councillor, within the first six months after taking the '
                         'title: step 2, some weeks into the seat, once residents have learned where the councillor '
                         'lives',
             'likelier': 'a ward with poor housing or a failing service; a councillor who is known in the streets; a '
                         'council office that answers slowly',
             'rarer': 'a quiet ward; a councillor with a paid assistant or a seat on a council that handles casework '
                      'centrally'},
 'scenes': {'earth': [('',
                       'Ten weeks in, {N} has two hundred unanswered messages, a phone that rings at dinner and a '
                       'neighbour who stops {N} in the shop about a blocked drain. {partner} has started to say "the '
                       'council" the way people say the name of a rival.'),
                      ('W',
                       'Every case deserves an answer, in order, within a week. {N} keeps a list, and it is getting '
                       'longer, not shorter.'),
                      ('U',
                       '{N} notices that half the cases are the same few problems: the same landlord, the same bus '
                       'stop, the same broken system at the housing office.'),
                      ('B',
                       'Some residents vote and some do not; some cases make a name and some vanish. {N} is ashamed '
                       'to have noticed, and has noticed anyway.'),
                      ('R',
                       'A mother in tears on the doorstep about her damp flat makes {N} so angry that the rest of '
                       'the list can wait.'),
                      ('G', 'These are {Ns} own streets. The woman with the drain taught {N} to swim as a child.')],
            'tribal': [('',
                        'Every morning another family waits at {Ns} hearth with a quarrel about a share of meat or a '
                        'broken promise, and every evening {partner} eats alone.')],
            'magic': [('',
                       "Petitions come under {Ns} door every morning, some sealed with a guild's wax, some scrawled "
                       'on scraps, and {Ns} own workbench gathers dust.')]},
 'outcomes': (['By the end of the month the cases have a shape, and {N} still has evenings at home.',
               'A case that has dragged on for a year is settled, and the family stops {N} in the street to say '
               'thanks.'],
              ['The cases keep coming faster than {N} can answer, and the ward starts to say {N} never replies.',
               '{partner} says one quiet evening that it feels as if {N} married the ward.']),
 'options': [
    ('answer every case in turn, oldest first, however late the nights run', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, benevolence', 'self_control': '+', 'world': {'tribal': 'hear every quarrel in turn, oldest first, however late the fire burns', 'magic': 'answer every petition in turn, oldest first, however late the candles burn'}, 'chance': 0.65}),
    ('sort the cases into the few problems behind them, and take each problem to the council', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': 'find the few grievances behind all the quarrels, and bring each one to the fire', 'magic': 'sort the petitions into the few wrongs behind them, and take each one to the council'}, 'chance': 0.45}),
    ('take on the cases that will be noticed, and pass the rest to the officers', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'take up the quarrels the whole band will hear of, and send the rest to the elders', 'magic': 'take up the petitions the town will hear of, and pass the rest to the clerks'}, 'chance': 0.92}),
    ('drop everything for the family in the damp flat, and go round tonight', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'mark': 'helped someone in need', 'world': {'tribal': 'drop everything for the family whose shelter leaks, and go to them tonight', 'magic': 'drop everything for the family in the damp garret, and go round tonight'}, 'chance': 0.92}),
    ('keep one evening a week for your own family, and let the ward wait', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'world': {'tribal': 'keep one evening in every few for your own kin, and let the band wait'}, 'chance': 0.72}),
    ('set up a fixed surgery every Saturday, and tell residents to bring their cases there', 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'name one day each moon when families may bring their quarrels to your hearth', 'magic': 'set one fixed day a week for petitions, and turn the rest away'}, 'chance': 0.9}),
    ('set up a simple online form so cases arrive with the facts, and free your evenings', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, hedonism', 'world': {'tribal': 'teach the families to bring their witnesses with them, and free your evenings', 'magic': 'have a clerk take every petition down in a set form, and free your evenings'}, 'chance': 0.72}),
    ("get a friend in the housing office to move your ward's cases up the list", 'B1', 'G.7', 0.5, '', {'v': 'power', 'mark': 'hid a wrong', 'closed': "approval: jumping one ward's residents up a shared waiting list; backfire: another councillor finds out, and the standards committee asks questions", 'self_control': '-', 'world': {'tribal': "get a friend among the elders to settle your own hearths' quarrels first", 'magic': "get a friend among the clerks to move your ward's petitions to the top"}, 'chance': 0.85}),
    ("read out the month's worst case in the chamber, again and again, until the council acts", 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': 'speak of the worst wrong at every fire until the elders act', 'magic': 'read the worst petition aloud at every sitting until the council acts'}, 'chance': 0.6}),
    ('ask the old caseworker at the community centre how she handled these streets for years', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'grants': 'constituency casework', 'world': {'tribal': "ask the old woman who settled the band's quarrels for years how she did it", 'magic': 'ask the old petition-writer of the ward how she handled these lanes for years'}, 'chance': 0.72}),
 ]},
{'name': 'whose councillor you are',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, meaning',
 'horizon': 'years',
 'roles': 'boss, colleague, friend',
 'requires': 'local councillor',
 'threshold': 'title:local councillor',
 'step': 2,
 'transform': True,
 'worlds': {'earth': "ten weeks in, a vote on closing the ward's library, and the party, the cause, the ward and "
                     'your own ambition each want something different',
            'tribal': 'two moons in, a choice at the fire about moving camp, and the faction, your own hearths, the '
                      'young hunters who backed you and your own hopes each pull another way',
            'magic': "ten weeks in, a vote on selling the ward's old reading room, and the faction, the guild that "
                     'paid for your banners, the lane and your own hopes each want something different'},
 'timing': {'times': 'per new local councillor: once in the threshold season, for about half of new councillors (the '
                     "season's middle step brings this moment or 'the casework that never stops'); about 1 life in "
                     '100 sits on a council (catalogue share), so about 1 in 200 meet it'},
 'trigger': {'requires': 'in the threshold season of local councillor, within the first six months after taking the '
                         "title: step 2, the season's transforming chance, when the first vote comes on which the "
                         'party, the cause and the ward disagree',
             'likelier': 'a councillor who stood for a cause as well as a party; a ward that votes differently from '
                         'the town; a leader who keeps a tight whip',
             'rarer': 'an independent with no group to answer to; a council with no contested votes that season'},
 'scenes': {'earth': [('',
                       'A vote is coming on closing the library in {Ns} ward to save money for the whole town. The '
                       'group has a line, the people who campaigned for {N} have another, the ward has a third, and '
                       '{boss} says ambitious councillors do not make trouble in their first year.'),
                      ('W',
                       '{N} thinks of the declaration {N} signed: to serve the whole town, fairly and by the rules, '
                       'not just the streets that voted.'),
                      ('U',
                       "{N} has read the library's figures, the visitor counts and the cost of every alternative, "
                       'and thinks the answer is in the numbers, if anyone will look.'),
                      ('B',
                       'A seat on the council is a first rung. {N} can see the ladder from here: a committee chair, '
                       'the cabinet, a parliamentary selection.'),
                      ('R',
                       'The people who knocked on doors in the rain for {N} did it for the cause. {N} cannot look '
                       'them in the eye and vote the way the group wants.'),
                      ('G', 'The library is where {N} learned to read. Whatever the town needs, the ward is home.')],
            'tribal': [('',
                        "The band must choose whether to move camp to the far shore. The faction's heads want one "
                        'thing, {Ns} own hearths another, and the young hunters who backed {N} a third.')],
            'magic': [('',
                       "The council will vote on selling the ward's old reading room. The faction wants it sold, the "
                       'guild that paid for {Ns} banners wants it kept, and the lane is waiting to see.')]},
 'outcomes': (['The vote comes, {N} votes as {N} decided to, and for once the seat feels like {Ns} own.',
               'Within weeks people in the ward can say what kind of councillor {N} is, and most of them say it with '
               'respect.'],
              ['Whichever way {N} turns, someone who trusted {N} feels betrayed, and says so.',
               "{N} tries to be everyone's councillor and ends the month as nobody's."]),
 'options': [
    ('serve the whole town by the rules, even when your own ward loses', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, conformity', 'world': {'tribal': 'speak for the whole band by its customs, even when your own hearths lose'}, 'chance': 0.72}),
    ('decide every vote on the evidence, and publish your reasons each time', 'U1', None, 0.45, '', {'identity': True, 'habit': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'weigh every choice on what is known, and give your reasons at the fire each time'}, 'chance': 0.75}),
    ("treat the seat as the first rung, and vote with the group's leaders", 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'world': {'tribal': "treat your voice as the first step, and stand with the faction's heads", 'magic': "treat the seat as the first rung, and cast with the faction's lords"}, 'chance': 0.9}),
    ('vote with the cause you stood for, whatever the group decides', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation, universalism', 'mark': 'defied an authority', 'world': {'tribal': 'stand with the young hunters who backed you, whatever the faction decides', 'magic': 'cast with the cause you stood for, whatever the faction decides'}, 'chance': 0.7}),
    ('put the ward first in every vote, as one of its own', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'put your own hearths first in every choice, as one of them', 'magic': 'put the lane first in every vote, as one of its own'}, 'chance': 0.76}),
    ("take the town's hardest unsolved case as your cause, and see it through by the book", 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism, stimulation', 'world': {'tribal': "take up the band's oldest unsettled wrong, and see it through by custom"}, 'chance': 0.4}),
    ('spend your term on one long plan for the ward, worked out with its residents', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'world': {'tribal': "work out one long plan for your hearths' future with the families themselves"}, 'chance': 0.62}),
    ('build a bloc of councillors from both sides to run the committees properly', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power', 'grants': 'coalition building', 'world': {'tribal': "bind voices from both factions together to keep the fire's business in order", 'magic': 'bind councillors from both factions together to run the committees properly'}, 'chance': 0.45}),
    ('push the council to try what no council has tried, and learn as you go', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'push the band to try a way nobody has tried, and learn as it goes'}, 'chance': 0.35}),
    ("become the ward's fixer, the one who knows whom to call to get things done", 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'power', 'world': {'tribal': 'become the one who settles things quietly between the families of your hearths', 'magic': "become the lane's fixer, the one who knows whom to ask at the guild hall"}, 'chance': 0.48}),
 ]},
{'name': 'the ward knows your name now',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, friends',
 'horizon': 'months',
 'roles': 'friend, colleague, partner',
 'requires': 'local councillor',
 'threshold': 'title:local councillor',
 'step': 3,
 'worlds': {'earth': 'five months in, people stop you in the shop, ask after the drain and the bus stop, and old '
                     'friends ring for favours',
            'tribal': 'five moons in, the families greet you by name at the water, ask after their quarrels, and old '
                      'friends want your voice',
            'magic': "five months in, the lane's children call you by your title, the baker will not take your coin, "
                     'and old friends want a quiet word'},
 'timing': {'times': 'per new local councillor: once, about five months after taking the title, near the end of the '
                     'threshold season; about 1 life in 100 (catalogue share)'},
 'trigger': {'requires': 'in the threshold season of local councillor, within the first six months after taking the '
                         'title: step 3, near the end of the six months, as the new life settles',
             'likelier': 'a councillor who lives in the ward; a few cases settled; a local paper or a ward '
                         'newsletter that carries the name',
             'rarer': 'a councillor who lives outside the ward; a council in open crisis'},
 'scenes': {'earth': [('',
                       'Five months in, {N} cannot buy milk without being stopped twice: once about a pothole, once '
                       'to be thanked for a bus stop. {friend} jokes that {N} has become a landmark, and an old '
                       'school friend has rung twice about "a quiet word" on a licence.'),
                      ('W',
                       'The surgery runs every second Saturday, the minutes go out on time, and residents have '
                       'started to say the ward is properly looked after.'),
                      ('U',
                       '{N} can now read a planning report in twenty minutes and find the paragraph the officers '
                       'hoped nobody would notice.'),
                      ('B',
                       "The old school friend's quiet word is the third such request this month. {N} is starting to "
                       "see what a councillor's name is worth."),
                      ('R',
                       'The fizz of the first night has gone. Some evenings {N} misses being an ordinary person in '
                       'the pub.'),
                      ('G',
                       '{N} knows the streets in a new way now: who is ill, who has moved, which corner floods. The '
                       'ward feels like a wide family, with all that brings.')],
            'tribal': [('',
                        'Five moons in, the families greet {N} by name at the water, and an old friend sits down at '
                        '{Ns} fire wanting {Ns} voice in a quarrel of their own.')],
            'magic': [('',
                       "Five months in, the lane's children call {N} by title, the baker will not take {Ns} coin, "
                       'and an old friend wants a quiet word about a guild licence.')]},
 'outcomes': (["The ward has got used to {N}, and {N} has got used to being the ward's.",
               '{friend} says {N} is still the same person, just busier, and means it kindly.'],
              ['The favours, the calls and the stops in the street wear {N} thin by the end of the month.',
               'One unanswered request turns into a story about {N} that goes round every street.']),
 'options': [
    ('keep the fortnightly surgery going, rain or shine, even when nobody comes', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, benevolence', 'world': {'tribal': 'keep your hearth open on the set day each moon, even when nobody comes', 'magic': 'keep the petition day going every fortnight, even when nobody comes'}, 'chance': 0.85}),
    ('send the ward a short monthly report on what you did and did not manage', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': 'tell the families at each new moon what you managed at the fire, and what you did not', 'magic': "post a short monthly account on the ward's notice board of what you did and did not manage"}, 'chance': 0.92}),
    ('keep a quiet list of every favour you do, and of who owes you', 'B1', None, 0.45, '', {'habit': True, 'v': 'power', 'self_control': '+', 'world': {'tribal': 'keep count in your head of every favour you do, and of who owes you'}, 'chance': 0.95}),
    ('spend a Saturday night in the pub as yourself, councillor or not', 'R1', None, 0.45, '', {'habit': True, 'v': 'hedonism, self-direction', 'world': {'tribal': 'spend a night at the dancing as yourself, a voice at the fire or not', 'magic': 'spend a night at the tavern as yourself, councillor or not'}, 'chance': 0.88}),
    ('walk the whole ward on Sundays, stopping for anyone who wants to talk', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'walk round every hearth of the camp, stopping for anyone who wants to talk', 'magic': 'walk the whole ward on market days, stopping for anyone who wants to talk'}, 'chance': 0.75}),
    ("start a residents' forum that meets in the library every month", 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'call the families of your hearths together at every new moon to talk things through', 'magic': "start a monthly meeting of the lane's households in the old reading room"}, 'chance': 0.65}),
    ('read the code of conduct again, and declare every interest, even the small ones', 'U1', 'W.7', 0.5, '', {'v': 'conformity, security', 'world': {'tribal': 'ask the elders which gifts a voice at the fire may take, and refuse the rest', 'magic': "read the council's oath again, and declare every interest, even the small ones"}, 'chance': 0.96}),
    ('trade your vote on a small item for a place on the scrutiny committee', 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, power', 'world': {'tribal': 'trade your voice on a small matter for a place among the elders who weigh the stores', 'magic': "trade your vote on a small item for a seat on the council's audit bench"}, 'chance': 0.78}),
    ('tell the old friend no to their face, loudly enough for the whole pub to hear', 'R1', 'B.7', 0.5, '', {'v': 'power, self-direction', 'grants': 'a name for straight talk', 'world': {'tribal': "refuse the old friend's favour at the fire, loudly enough for the whole band to hear", 'magic': "refuse the old friend's favour in the tavern, loudly enough for the whole room to hear"}, 'chance': 0.84}),
    ('plant up the ugly corner by the bus stop with the neighbours, for fun', 'G1', 'R.7', 0.5, '', {'body': 'light', 'v': 'hedonism, benevolence', 'mark': 'made a friend', 'world': {'tribal': 'clear and plant the trampled ground by the water with the families, for the joy of it', 'magic': 'plant up the bare corner by the well with the neighbours, for the fun of it'}, 'chance': 0.9}),
 ]},
{'name': 'the chain of office',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, work',
 'horizon': 'week',
 'roles': 'colleague, elder, boss',
 'requires': 'mayor',
 'threshold': 'title:mayor',
 'step': 1,
 'worlds': {'earth': 'the chain goes round your neck in the council chamber, and on Monday the office, the staff and '
                     'the diary are yours',
            'tribal': 'the band gathers at dawn to see the head of the camp take up the old staff, and the first '
                      'question is where to camp next',
            'magic': "the burgomaster's chain, seal and keys are handed over in the town hall, and the clerks wait "
                     'for your first order'},
 'timing': {'times': 'per new mayor: once, in the first weeks after taking the title; about 1 life in 500 (catalogue '
                     'share; estimate)'},
 'trigger': {'requires': 'in the threshold season of mayor, within the first six months after taking the title '
                         "(opened by 'the town needs a mayor', a direct election or any other way in): step 1, the "
                         'first weeks in office',
             'likelier': 'a contested choice won; a town with an old mayoral office and its ceremonies; a mayor new '
                         "to the town hall's staff",
             'rarer': "a deputy who steps up after years in the office; a small place where the mayor's post is one "
                      'evening a week'},
 'scenes': {'earth': [('',
                       "The chain is heavier than it looks. After the ceremony {N} is shown the mayor's office: a "
                       'desk, a window over the square, a diary already full for six weeks and a secretary who has '
                       'served four mayors.'),
                      ('W',
                       '{N} reads the declaration of office aloud in the chamber without a slip, and means every '
                       'word of it.'),
                      ('U',
                       "{N} asks for the town's accounts, the list of contracts and the staff chart before the first "
                       'meeting, and reads them all weekend.'),
                      ('B',
                       "The diary is full of other people's priorities. {N} looks at it and starts deciding which of "
                       'them to cancel.'),
                      ('R',
                       '{N} wants to walk straight out of the chamber, still in the chain, into the market, and '
                       'shake every hand there.'),
                      ('G',
                       'In the corridor hang portraits of every mayor for a hundred and fifty years. {N} stops at '
                       'each one on the way to the office.')],
            'tribal': [('',
                        'At dawn the band gathers as the old staff of the camp passes into {Ns} hands, and the first '
                        'question is already waiting: where to camp when the river rises.')],
            'magic': [('',
                       'In the town hall the old burgomaster lifts the chain over {Ns} head and hands over the seal '
                       'and the keys, and the clerks wait, quills ready, for the first order.')]},
 'outcomes': (['By the end of the first week the post feels less like a ceremony and more like work.',
               'The town takes to {N} in the chain, and the first days go better than anyone feared.'],
              ['The first week goes on ceremonies and handshakes, and nothing {N} came to do has started.',
               'An early decision upsets the old guard, and the corridors are cool toward {N} for weeks.']),
 'options': [
    ('keep the diary as the office set it for the first month, and learn from it', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': "keep to the old order of the head's days for the first moon, and learn from it", 'magic': "keep the burgomaster's book of days as the clerks set it for the first month"}, 'chance': 0.94}),
    ("spend the first weekend reading the town's accounts and every big contract", 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'world': {'tribal': 'walk the whole camp counting the stores, the hides and the tools', 'magic': "spend the first days reading the town's ledgers and every guild charter"}, 'chance': 0.95}),
    ('cancel half the diary, and fill it with meetings that serve your own plan', 'B1', None, 0.45, '', {'v': 'power, self-direction', 'world': {'tribal': "set aside the elders' plans for the season, and put your own in their place", 'magic': 'strike half the appointments from the book, and fill it with your own'}, 'chance': 0.89}),
    ('walk out into the market in the chain, and shake every hand you can', 'R1', None, 0.45, '', {'body': 'light', 'v': 'stimulation, hedonism', 'world': {'tribal': 'go round every hearth at once with the staff in your hand'}, 'chance': 0.96}),
    ('ask the secretary who served four mayors what each of them got wrong', 'G1', None, 0.45, '', {'v': 'tradition, achievement', 'mark': 'made a friend', 'world': {'tribal': 'ask the oldest woman of the camp what each head before you got wrong', 'magic': 'ask the old clerk who served four burgomasters what each of them got wrong'}, 'chance': 0.8}),
    ("get the town clerk's briefing on the law of the office before signing anything", 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'ask the elders for the old rules of the head of the camp before deciding anything', 'magic': "get the town clerk's briefing on the law of the office before setting your seal to anything"}, 'chance': 0.96}),
    ('find out which officers really run the town hall, and win them over first', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'find out which families really decide things in the camp, and win them first', 'magic': 'find out which clerks really run the town hall, and win them over first'}, 'chance': 0.79}),
    ('get a local firm to pay for a party in the square on the first Saturday', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': 'get the richest family to give a feast for the whole camp', 'magic': 'get a merchant house to pay for a feast in the square on the first market day'}, 'chance': 0.86}),
    ("open the mayor's parlour to anyone who wants to see it, every Friday", 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': "let anyone who wants to sit at the head's fire, every evening", 'magic': "open the burgomaster's hall to anyone who wants to see it, every market day"}, 'chance': 0.92}),
    ('visit every care home and school in town in the first month, as old mayors did', 'G1', 'W.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'visit every old one and every mother of small children in the camp, as the old heads did', 'magic': 'visit every almshouse and school in town in the first month, as the old burgomasters did'}, 'chance': 0.78}),
 ]},
{'name': 'the day job or the town',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'public life, work, family',
 'horizon': 'months',
 'roles': 'boss, partner, colleague',
 'requires': 'mayor',
 'threshold': 'title:mayor',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the town needs a mayor every day of the week, and your employer needs you back '
                     'on Monday',
            'tribal': 'two moons in, the hunt leaves at the new moon, and the camp cannot be left without its head; '
                      'you cannot do both',
            'magic': "ten weeks in, your workshop and your guild's work wait, while the town needs its burgomaster "
                     'every hour the bells ring'},
 'timing': {'times': 'per new mayor: once, about ten weeks into the threshold season, for about half of new mayors '
                     "(the season's middle step brings this moment or 'the kind of mayor you will be'); about 1 life "
                     'in 500 is a mayor (catalogue share; estimate), so about 1 in 1,000 meet it'},
 'trigger': {'requires': 'in the threshold season of mayor, within the first six months after taking the title: step '
                         '2, some weeks into office, while the mayor still holds a day job',
             'likelier': 'a big town that needs a full-time mayor; a mayor with a career of their own; an allowance '
                         'too small to live on',
             'rarer': 'a retired mayor; a village where the post takes one evening a week; a post already paid as a '
                      'full-time office'},
 'scenes': {'earth': [('',
                       'Ten weeks in, {N} has used every day of holiday on the town. {boss} at {Ns} day job has '
                       "started to ask, politely, how long this can go on, and the mayor's allowance would not pay "
                       'the rent on its own. {partner} wants to know which of the two {N} is married to.'),
                      ('W',
                       '{N} promised the town a mayor who would be there, and promised {boss} at work a full week. '
                       'Both cannot be true.'),
                      ('U',
                       '{N} works it out on paper: hours, pay, pension, the allowance, and what a part-time mayor of '
                       'a town this size can and cannot do.'),
                      ('B',
                       "The town's business brings more contacts in a week than the day job did in ten years. {N} "
                       'wonders which of the two is really the career now.'),
                      ('R',
                       '{N} loves the work at the town hall and dreads Mondays at the old job. It has never been so '
                       'plain.'),
                      ('G',
                       "The day job pays for the house and the family's peace of mind, and {partner} is afraid of "
                       'what happens if the town throws {N} out at the next election.')],
            'tribal': [('',
                        'The hunt leaves at the new moon, and {Ns} spear has always gone with it. But a camp left '
                        'without its head while the river rises is a camp in danger.')],
            'magic': [('',
                       '{Ns} workbench at the guild has been cold for weeks, the masters are asking questions, and '
                       'the town needs its burgomaster every hour the bells ring.')]},
 'outcomes': (['{N} settles how the weeks will go, and the town and the household both seem able to live with it.',
               'The decision, once made, feels lighter than all the weeks of putting it off.'],
              ['{N} tries to keep both going and is too tired by the end of the month to do either well.',
               'The choice is made, and within weeks money at home is tighter than anyone planned for.']),
 'options': [
    ("keep both promises: work the full week, and do the town's business every evening", 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'self_control': '+', 'world': {'tribal': 'go with the hunt by day and lead the camp at night, as best you can', 'magic': "keep your place at the guild bench by day, and the town's business every evening"}, 'chance': 0.62}),
    ('decide what a part-time mayor can do, and hand the rest to the deputy', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': "share out the camp's work among the elders, so you can still go with the hunt", 'magic': 'decide what a part-time burgomaster can do, and hand the rest to the deputy'}, 'chance': 0.75}),
    ('resign from the day job, and take every paid seat that comes with the office', 'B1', None, 0.45, '', {'v': 'power, achievement', 'drops': 'kind:career', 'world': {'tribal': "give up your place in the hunt, and take the head's share of every kill", 'magic': 'give up your guild bench, and take every paid seat that comes with the office'}, 'chance': 0.92}),
    ('quit the day job tomorrow, because the town is where your heart is', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'mark': 'took a wild risk', 'drops': 'kind:career', 'world': {'tribal': 'lay down your spear tomorrow and stay with the camp, because your heart is here', 'magic': 'leave the guild bench tomorrow, because the town is where your heart is'}, 'chance': 0.95}),
    ("keep the day job and the family's security, and be a mayor in the evenings", 'G1', None, 0.45, '', {'v': 'security, tradition', 'world': {'tribal': 'go with the hunt as your family always has, and lead the camp when you return', 'magic': 'keep the craft your family has always followed, and be burgomaster by night'}, 'chance': 0.7}),
    ('ask the council to make the post full-time and properly paid, by an open vote', 'W1', 'B.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'ask the elders to free the head of the camp from the hunt, by custom', 'magic': "ask the council to make the burgomaster's post a paid office, by an open vote"}, 'chance': 0.3}),
    ('ask your employer for a four-day week, with a written plan for both jobs', 'U1', 'R.7', 0.5, '', {'v': 'self-direction', 'world': {'tribal': 'go with the hunt every other moon, by a plan the elders agree', 'magic': 'ask your guild master for a shorter week, with a written plan for both'}, 'chance': 0.7}),
    ("take a year's unpaid leave, and keep the old job warm in case the town turns", 'B1', 'G.7', 0.5, '', {'v': 'security', 'self_control': '+', 'world': {'tribal': 'send a younger kinsman on the hunt in your place, and keep your share', 'magic': "take a year's leave from the guild, and keep your bench in case the town turns"}, 'chance': 0.65}),
    ('tell the town it needs a full-time mayor, and that you will be one', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'kept your word', 'self_control': '+', 'drops': 'kind:career', 'world': {'tribal': 'tell the whole band at the fire that the camp needs its head here, and stay', 'magic': 'tell the town in the square that it needs a full-time burgomaster, and that you will be one'}, 'chance': 0.8}),
    ('ask the old mayors of the nearby villages how they managed both', 'G1', 'U.7', 0.5, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the heads of the nearby camps how they kept both', 'magic': 'ask the burgomasters of the nearby towns how they managed both'}, 'chance': 0.88}),
 ]},
{'name': 'the kind of mayor you will be',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, meaning',
 'horizon': 'years',
 'roles': 'colleague, rival, elder',
 'requires': 'mayor',
 'threshold': 'title:mayor',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'ten weeks in, the town is waiting to see what kind of mayor you are, and whatever you fight '
                     'for first will be the answer',
            'tribal': 'two moons in, the camp waits to see what kind of head you will be: keeper of the old ways, '
                      'hard bargainer or the one who leads the dancing',
            'magic': 'ten weeks in, the town waits to see what kind of burgomaster you will be, and the guilds have '
                     'started to place their bets'},
 'timing': {'times': "per new mayor: once in the threshold season, for about half of new mayors (the season's middle "
                     "step brings this moment or 'the day job or the town'); about 1 life in 500 is a mayor "
                     '(catalogue share; estimate), so about 1 in 1,000 meet it'},
 'trigger': {'requires': 'in the threshold season of mayor, within the first six months after taking the title: step '
                         "2, the season's transforming chance, once the first big choice of the term must be made",
             'likelier': 'a town with a long list of things it has always meant to do; a mayor elected on a promise; '
                         'a council that can be won over',
             'rarer': 'a caretaker mayor for a short term; a council so split that nothing can move'},
 'scenes': {'earth': [('',
                       'The town hall has a long list of things it has always meant to do: a new bus station, the '
                       'old swimming baths, the market hall that leaks. {N} cannot do them all, and whatever {N} '
                       'fights for first will become what people mean when they say "the mayor".'),
                      ('W',
                       '{N} thinks of the whole town: the estates and the old centre, the young families and the old '
                       'people in the care homes. A mayor for all of them, fairly.'),
                      ('U',
                       '{N} sees a plan of ten years in which every small decision leads to the next, and the town '
                       'is a different place at the end of it.'),
                      ('B',
                       'The town hall controls land, contracts and jobs. Used with a long plan, that is more power '
                       'than most people in town know.'),
                      ('R',
                       '{N} imagines the square full on a summer night, music playing, cranes on the skyline, and '
                       'everyone talking about what the mayor did next.'),
                      ('G',
                       'The town is old. The trees in the square were planted by people long dead, and {N} wants to '
                       'be the mayor who kept what matters.')],
            'tribal': [('',
                        'The camp waits to see what kind of head {N} will be: keeper of the old ways, hard bargainer '
                        'with the other clans, or the one who leads the dancing.')],
            'magic': [('',
                       'The guilds have started to place bets on what kind of burgomaster {N} will be, and the first '
                       'thing {N} fights for will settle them.')]},
 'outcomes': (['Within weeks the town has a sense of what {N} is for, and the first step is taken.',
               'The plan, or the promise, holds its first test, and the doubters go quiet.'],
              ["The first big push meets the council's wall, and {N} is the mayor of one stalled idea.",
               "What {N} meant and what the town hears drift apart, and the town's talk fills the gap."]),
 'options': [
    ('govern for every part of the town alike, and publish every decision with its reasons', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, conformity', 'world': {'tribal': 'lead for every hearth of the camp alike, and give your reasons at the fire for every choice'}, 'chance': 0.86}),
    ('draw up a ten-year plan for the town, and judge every decision against it', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, self-direction', 'grants': 'drafting policy', 'world': {'tribal': "work out a plan for the camp's next ten winters, and weigh every choice against it"}, 'chance': 0.72}),
    ("take control of the town's land and contracts, and use them to get things built", 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'world': {'tribal': "take charge of the camp's best ground and its trade, and use them to get things done", 'magic': "take control of the town's land and guild contracts, and use them to get things built"}, 'chance': 0.5}),
    ('promise the town the cranes up and the square rebuilt by next summer, on your name', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation, achievement', 'world': {'tribal': 'promise the band a great new shelter by next summer, on your name', 'magic': 'promise the town a new market hall raised by next summer, on your name'}, 'chance': 0.22}),
    ('protect the old town, its trees, its market and its ways, against every fashion', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition', 'world': {'tribal': "keep the camp's old ways, its sacred places and its seasons, against every new idea"}, 'chance': 0.8}),
    ("take on the town's slum landlords, by the letter of the law", 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism', 'mark': 'made an enemy', 'world': {'tribal': "take on the family that hoards the camp's best shelters, by the band's own customs", 'magic': "take on the town's slumlords and rack-renting guilds, by the letter of the law"}, 'chance': 0.62}),
    ('rebuild the town around its river and its parks, by careful design', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'world': {'tribal': 'move the camp, by careful plan, to where the river and the woods will feed it longest'}, 'chance': 0.38}),
    ('strike a deal with every faction on the council, so the town is governed steadily', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power', 'grants': 'coalition building', 'chance': 0.65}),
    ('try a bold new idea every season, and drop whatever fails', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, self-direction', 'chance': 0.8}),
    ("back the town's own firms and families first, and keep big outside money at the door", 'G1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'tradition', 'world': {'tribal': "favour the camp's own families in every trade, and keep the outside clans' gifts at a distance", 'magic': "back the town's own guilds and families first, and keep the great merchant houses at the gate"}, 'chance': 0.45}),
 ]},
{'name': 'the first budget passes',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'public life, money',
 'horizon': 'months',
 'roles': 'colleague, rival, boss',
 'requires': 'mayor',
 'threshold': 'title:mayor',
 'step': 3,
 'worlds': {'earth': 'five months in, the first budget comes to the vote: too little money, too many promises, and a '
                     'council that must pass it',
            'tribal': 'five moons in, before the winter camp, the head must share out the stores: too little dried '
                      'meat, too many families, and every share a judgment',
            'magic': "five months in, the town's first budget under your seal goes before the council: the coffer is "
                     'short and every guild wants more'},
 'timing': {'times': 'per new mayor: once, about five months after taking the title, near the end of the threshold '
                     'season, as the first budget comes to the vote; about 1 life in 500 (catalogue share; '
                     'estimate)'},
 'trigger': {'requires': 'in the threshold season of mayor, within the first six months after taking the title: step '
                         '3, near the end of the six months, when the first budget of the term is due',
             'likelier': 'a town with a gap between its money and its promises; a council where the mayor has no '
                         'sure majority; a hard year',
             'rarer': 'a rich town with money to spare; a budget set by the council leader rather than the mayor'},
 'scenes': {'earth': [('',
                       'Five months in, the budget goes to the vote. There is a gap of a few percent between what '
                       "the town has and what it has been promised, and every line {N} cuts is someone's job, "
                       "someone's bus route or someone's library."),
                      ('W',
                       "The law says the budget must balance. {N} has the clerk's note on that pinned to the wall."),
                      ('U',
                       '{N} knows every line now. The gap could be closed four ways, and {N} has costed all four.'),
                      ('B',
                       'Every councillor who wants something in the budget owes {N} a vote for it. {N} is counting.'),
                      ('R',
                       '{N} hates this part: choosing who loses. Some nights {N} wants to throw the whole '
                       'spreadsheet out of the window.'),
                      ('G',
                       '{N} thinks of the old swimming baths, the allotments, the band in the park: the things that '
                       'make the town itself, which a spreadsheet does not count.')],
            'tribal': [('',
                        'Winter is coming, and {N} must share out the stores. There is not enough for every family '
                        'to have what it had last year, and each share {N} names will be remembered.')],
            'magic': [('',
                       'The coffer is short, every guild sends a petition for more, and the council will vote on '
                       '{Ns} first budget at the next sitting.')]},
 'outcomes': (['The budget passes, not by much, and the town keeps most of what it loves.',
               'The town hall staff, who have seen many first budgets, say quietly that this one was well done.'],
              ['The budget fails at the first vote, and {N} must come back with a worse one.',
               'It passes, but the cut nobody noticed at the vote is the one the whole town notices by spring.']),
 'options': [
    ('cut every department by the same share, so nobody can say it was unfair', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': "cut every family's share of the stores by the same measure, so nobody can call it unfair", 'magic': 'cut every office and guild grant by the same share, so nobody can call it unfair'}, 'chance': 0.88}),
    ("move the shortfall into next year's figures, so the budget balances on paper", 'U1', None, 0.45, '', {'v': 'security, achievement', 'mark': 'hid a wrong', 'closed': "law: misstating the town's accounts; backfire: the auditor's report in the spring, and a vote of censure", 'self_control': '-', 'world': {'tribal': 'count the stores as fuller than they are, so the shares look enough', 'magic': "move the shortfall into next year's ledger, so the budget balances on parchment"}, 'chance': 0.9}),
    ("trade a pet project for each wavering councillor's vote until you have a majority", 'B1', None, 0.45, '', {'v': 'power', 'grants': 'counting the votes', 'world': {'tribal': 'promise each wavering family something of its own until enough of them stand with you'}, 'chance': 0.75}),
    ('spare the buses and the youth club, and dare the council to vote it down', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'self_control': '+', 'world': {'tribal': "spare the old ones' and the mothers' shares, and dare the elders to overrule you", 'magic': "spare the poor relief and the apprentices' school, and dare the council to vote it down"}, 'chance': 0.6}),
    ('protect the old baths, the allotments and the park, and cut the new projects instead', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'protect the shares for the old rites and the feasts, and cut the new ventures instead', 'magic': 'protect the old baths, the common gardens and the park, and cut the new projects instead'}, 'chance': 0.72}),
    ('hold a meeting in every ward first, and let the town choose its own cuts', 'W1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'let every hearth speak at the fire before the sharing, and let the band choose'}, 'chance': 0.72}),
    ('rebuild the budget line by line until it balances honestly, and show your working', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'self_control': '+', 'world': {'tribal': 'count the stores again, skin by skin, until the shares add up honestly, and show everyone', 'magic': 'rebuild the budget line by line until it balances honestly, and show the clerks your working'}, 'chance': 0.75}),
    ("sell the empty council offices, and put the money into fixing the town's broken systems", 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': "trade the camp's spare hides to the river clans for better tools and stone", 'magic': "sell the empty guild hall, and put the money into mending the town's broken wards"}, 'chance': 0.72}),
    ('stand up in the chamber and shame the councillors who want cuts only in other wards', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'mark': 'made an enemy', 'world': {'tribal': 'shame the families at the fire who want cuts only at other hearths', 'magic': 'rise in the council and shame those who want cuts only in other wards'}, 'chance': 0.69}),
    ("let the town's festival and the band in the park keep their money, whatever else goes", 'G1', 'R.7', 0.5, '', {'v': 'hedonism, tradition', 'world': {'tribal': 'keep the stores for the midwinter feast and the dancing, whatever else goes', 'magic': "let the town's fair and the musicians in the park keep their money, whatever else goes"}, 'chance': 0.82}),
 ]},
{'name': 'the first day in the chamber',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, work',
 'horizon': 'week',
 'roles': 'colleague, boss, elder',
 'requires': 'member of parliament',
 'threshold': 'title:member of parliament',
 'step': 1,
 'worlds': {'earth': 'the first days in parliament: the oath, a pass, a locker, a desk shared with three others and '
                     'nowhere to sit in the chamber',
            'tribal': "the first days at the great gathering of the clans as your band's speaker, among hundreds of "
                      'strangers and their fires',
            'magic': "the first sitting of the Assembly of the realm: the oath under the Order's seal, a pass warded "
                     'to your hand and a bench at the back'},
 'timing': {'times': 'per new member of parliament: once, in the first weeks after taking the title; about 1 life in '
                     '10,000 (House of Commons, ONS)'},
 'trigger': {'requires': 'in the threshold season of member of parliament, within the first six months after taking '
                         "the title (opened by 'election night', a by-election or any other way in): step 1, the "
                         'first weeks in the house',
             'likelier': 'a first election won; a large new intake after a change of government; a member from far '
                         'outside the capital',
             'rarer': 'a former member returning to the house; a member who worked in parliament for years as staff'},
 'scenes': {'earth': [('',
                       'On {Ns} first day in parliament {N} swears the oath, is given a pass, a locker and a desk in '
                       'an office shared with three other new members, and finds the chamber so full there is '
                       'nowhere to sit. Somebody shows {N} the way to the tea room twice.'),
                      ('W',
                       '{N} reads the oath slowly and feels it settle: the law, the house, the people of the '
                       'constituency. It is not nothing.'),
                      ('U',
                       "The building is a maze of corridors, rules and customs older than the country's roads. {N} "
                       'has a map, a rule book and a notebook, and is filling the notebook fast.'),
                      ('B', 'Old hands know within a week which new members to watch. {N} means to be on that list.'),
                      ('R',
                       "Under the painted ceiling {N} feels like a child let into the grown-ups' party, and wants to "
                       'stand up and cheer.'),
                      ('G',
                       '{N} thinks of the town back home: the bus stop where the campaign started, and the people '
                       'who will be watching the news tonight to catch a glimpse.')],
            'tribal': [('',
                        'At the great gathering {N} walks among hundreds of strangers and their fires as the speaker '
                        'for {Ns} band, and does not yet know where to sit.')],
            'magic': [('',
                       "Under the Order's seal {N} swears the oath of the Assembly, is given a pass warded to {Ns} "
                       'own hand, and finds no room on the crowded benches.')]},
 'outcomes': (['By the end of the first week {N} can find the chamber, the library and the way home without asking.',
               'An old member stops {N} in a corridor, says {N} will do well here, and seems to mean it.'],
              ['The first week passes in a blur of corridors, forms and waiting, and {N} is not sure what {N} did.',
               'A small first-week slip goes the rounds of the whole place, and {N} learns how fast it talks.']),
 'options': [
    ('take the oath, sign every register, and sit through every induction before speaking', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'swear the old words of the gathering, and keep silent until you know its customs', 'magic': "swear the oath under the Order's seal, sign every roll, and sit through every induction"}, 'chance': 0.95}),
    ('spend the first week learning the building, the rules and how a bill becomes law', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'world': {'tribal': 'spend the first days learning the gathering: its fires, its customs and how a choice is made', 'magic': "spend the first week learning the Assembly's halls, its rules and how a decree is made"}, 'chance': 0.92}),
    ('get noticed by the whips in the first week, and ask them for a committee', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': "make sure the faction's heads notice you in the first days, and ask them for a duty", 'magic': "make sure the faction's wardens notice you in the first week, and ask for a committee"}, 'chance': 0.59}),
    ("ask the constituency's burning question at the very first question time", 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': "rise at the first fire of the gathering and put your band's grievance, out of turn", 'magic': "rise at the first sitting and put your city's grievance to the Chancellor's bench"}, 'chance': 0.22}),
    ('hire your cousin to run the constituency office, without advertising the post', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'mark': 'hid a wrong', 'closed': 'approval: a family hire around the open process; backfire: a story in the papers and an inquiry by the expenses watchdog', 'self_control': '-', 'world': {'tribal': "make your cousin the one who carries the families' troubles to you, passing over abler hands", 'magic': 'make your cousin your clerk of petitions, without posting the place'}, 'chance': 0.92}),
    ('volunteer for the accounts committee nobody wants, to learn how the money really works', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'conformity, achievement', 'world': {'tribal': "offer to keep the gathering's tally of gifts, which nobody wants, to learn how things really work", 'magic': "volunteer for the Assembly's audit bench nobody wants, to learn how the coffers really work"}, 'chance': 0.75}),
    ('study which committees lead to office, and set out to sit on them', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'watch which speakers the chief listens to, and set out to sit near them', 'magic': 'study which committees lead to the offices of the Crown, and set out to sit on them'}, 'chance': 0.7}),
    ('spend the evenings in the bars where the members talk, and enjoy every one', 'B1', 'R.7', 0.5, '', {'habit': True, 'v': 'hedonism, power', 'world': {'tribal': 'spend the nights at the fires where the speakers talk, and enjoy every one', 'magic': 'spend the evenings in the taverns where the members talk, and enjoy every one'}, 'chance': 0.94}),
    ('bring your campaign volunteers on a tour of the building', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'kept your word', 'world': {'tribal': 'bring the young ones who walked the hearths in your name to see the gathering', 'magic': "bring your banner-bearers on a tour of the Assembly's halls"}, 'chance': 0.96}),
    ('open an office in the old place on the high street, open every Friday', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'keep a fire burning at home for the families each time you return from the gathering', 'magic': 'open your petition room in the old place on the high street, every market day'}, 'chance': 0.72}),
 ]},
{'name': 'the maiden speech',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, work',
 'horizon': 'months',
 'roles': 'mentor, colleague, boss',
 'requires': 'member of parliament',
 'threshold': 'title:member of parliament',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the first speech in the chamber: by custom about the constituency, without a '
                     'fight, and heard by the whole house',
            'tribal': 'two moons in, your first time to speak before all the clans, by custom about the band that '
                      'sent you, and every speaker listening',
            'magic': 'ten weeks in, your first oration in the Assembly, by custom in praise of the city that sent '
                     'you, with the whole Assembly listening'},
 'timing': {'times': 'per new member of parliament: once, about ten weeks into the threshold season, for about half '
                     "of new members (the season's middle step brings this moment or 'who you answer to'); nearly "
                     'every new member makes a maiden speech in the first months; about 1 life in 10,000 sits in '
                     'parliament (House of Commons, ONS), so about 1 in 20,000 meet it here'},
 'trigger': {'requires': 'in the threshold season of member of parliament, within the first six months after taking '
                         "the title: step 2, some weeks into the house, when the member's name comes up for the "
                         'first speech',
             'likelier': 'a new member in a parliament with the custom of a maiden speech; a busy debate on '
                         'something the constituency cares about',
             'rarer': 'a member returning to the house, who has spoken before; a member who becomes a minister at '
                      'once and speaks first from the front bench'},
 'scenes': {'earth': [('',
                       'Ten weeks in, {Ns} name is down for the maiden speech. By custom it praises the '
                       'constituency, avoids a fight and is heard in silence. {N} has eight drafts, and {mentor} has '
                       'read three of them.'),
                      ('W',
                       'The custom is clear: praise the member who came before, describe the constituency, avoid '
                       'controversy. {N} finds a dignity in it.'),
                      ('U',
                       '{N} wants a speech that is accurate in every figure and says one thing nobody in the house '
                       'has quite said before.'),
                      ('B',
                       'Speeches like this are clipped, quoted and remembered when the whips draw up their lists. '
                       '{N} writes with that in mind.'),
                      ('R',
                       '{N} wants to tear up the custom and say what the people back home are really angry about, in '
                       'their own words.'),
                      ('G',
                       '{N} wants the house to hear the place: the river, the closed pit, the old market, the '
                       'accent.')],
            'tribal': [('',
                        'For the first time {N} will speak before all the clans. By custom a first speaker tells of '
                        'the band that sent them and starts no quarrel, and every speaker listens.')],
            'magic': [('',
                       '{Ns} first oration in the Assembly is set for the morning bell. By custom it praises the '
                       'city that sent its member, and the whole Assembly will be listening.')]},
 'outcomes': (['The house listens, a few members nod, and back home people repeat what was said of their place.',
               '{mentor} catches {N} afterwards and says it was a proper speech.'],
              ['The benches are half empty and nobody listens, and {N} sits down feeling small.',
               'One line comes out wrong, and it is all anyone remembers of the speech.']),
 'options': [
    ('keep the custom: praise your predecessor, describe the place, avoid any fight', 'W1', None, 0.45, '', {'v': 'tradition, conformity', 'world': {'tribal': 'keep the custom: honour the last speaker, tell of your band, start no quarrel', 'magic': 'keep the custom: praise the member before you, describe your city, start no quarrel'}, 'chance': 0.94}),
    ('check every figure twice, and make one careful point nobody has made before', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'grants': 'debating', 'world': {'tribal': 'make one careful point nobody at the gathering has made before, true in every part'}, 'chance': 0.75}),
    ('write it to be quoted, with one line built for the evening news', 'B1', None, 0.45, '', {'v': 'achievement, power', 'grants': 'handling the press', 'world': {'tribal': 'build it around one saying the singers will carry to every band', 'magic': 'build it around one line the heralds will cry in every square'}, 'chance': 0.58}),
    ('throw away the notes halfway through, and speak as you would on a doorstep', 'R1', None, 0.45, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'forget the words you prepared, and speak as you would at your own fire', 'magic': 'put down your notes halfway through, and speak as you would in the tavern'}, 'chance': 0.85}),
    ('tell the house the story of the town, in its own words and its own accent', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'tell the gathering the story of your band, in its own words and its own songs', 'magic': 'tell the Assembly the story of your city, in its own words and its own accent'}, 'chance': 0.72}),
    ("back the government's line in the speech, word for word, where the whips can hear", 'W1', 'B.7', 0.5, '', {'v': 'conformity', 'world': {'tribal': "speak the faction's words, word for word, where its heads can hear", 'magic': "speak the faction's line, word for word, where its wardens can hear"}, 'chance': 0.8}),
    ('find the one fact that will shock the house, and build the speech around it', 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'world': {'tribal': 'find the one thing the clans do not know that will shake them, and build your words around it'}, 'chance': 0.4}),
    ('name the local firms and families who backed you, so they hear it said in parliament', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'name the families who fed your feast, so they hear it said at the gathering', 'magic': 'name the guilds and families who backed you, so they hear it said in the Assembly'}, 'chance': 0.93}),
    ('break the custom of no controversy, and name an injustice back home', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'mark': 'defied an authority', 'world': {'tribal': 'break the custom of the first speech, and name a wrong done to your band', 'magic': 'break the custom of the first oration, and name a wrong done to your city'}, 'chance': 0.65}),
    ('ask the oldest people in the constituency what the house should hear, and listen', 'G1', 'U.7', 0.5, '', {'v': 'tradition, universalism', 'world': {'tribal': 'ask the oldest of your band what the gathering should hear, and listen', 'magic': 'ask the oldest people of your city what the Assembly should hear, and listen'}, 'chance': 0.82}),
 ]},
{'name': 'who you answer to',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, meaning',
 'horizon': 'years',
 'roles': 'boss, partner, colleague',
 'requires': 'member of parliament',
 'threshold': 'title:member of parliament',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'ten weeks in, the whips, the constituency, your conscience and your ambition all want your '
                     'vote on the same bill, and you must decide whom you answer to',
            'tribal': "two moons in, at the gathering, the faction's head, the families back home, your own judgment "
                      'and your hunger to rise all pull at your voice',
            'magic': "ten weeks in, the faction's warden, the city that sent you, your conscience and your hopes at "
                     'court all want your lot cast their way'},
 'timing': {'times': 'per new member of parliament: once in the threshold season, for about half of new members (the '
                     "season's middle step brings this moment or 'the maiden speech'); about 1 life in 10,000 sits "
                     'in parliament (House of Commons, ONS), so about 1 in 20,000 meet it'},
 'trigger': {'requires': 'in the threshold season of member of parliament, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, when the first whipped vote comes on "
                         "which the party, the constituency and the member's own view disagree",
             'likelier': 'a party in government with a big programme; a constituency with its own interest in the '
                         'bill; a member elected on a local cause',
             'rarer': 'an independent with no whip; a parliament in recess for most of the season'},
 'scenes': {'earth': [('',
                       'Ten weeks in, a bill comes to its second reading. The whips want {Ns} vote, the constituency '
                       'is against it, {Ns} own reading of it is mixed, and a career in the house may turn on the '
                       'answer. On the phone that night {partner} asks whom {N} works for now.'),
                      ('W',
                       "{N} was elected on the party's promises and swore an oath to the house. Both say the same "
                       'thing: keep faith with the institution that sent {N}.'),
                      ('U',
                       '{N} has read the bill, the briefings from both sides and the research behind them. The '
                       'evidence points one way, and nobody else seems to have read it.'),
                      ('B',
                       'The whips keep lists. A loyal vote now is a post in two years; a rebel is a backbencher for '
                       'a decade.'),
                      ('R', '{N} can feel in the gut what is right, and it is not what the whips want.'),
                      ('G',
                       '{N} thinks of the town: the factory gate, the chapel, the families who have sent someone '
                       'like {N} to this place for three generations.')],
            'tribal': [('',
                        "At the gathering the faction's head wants {Ns} voice for a raid, {Ns} own band wants peace, "
                        "and {N} can feel which way the chief's favour lies.")],
            'magic': [('',
                       "The faction's warden brings the line for tomorrow's vote in the Assembly. {Ns} city has sent "
                       'a letter against it, and {Ns} hopes at court lie with the faction.')]},
 'outcomes': (['The vote is cast, and {N} can explain it to anyone, at home or in the house, without looking away.',
               'Over the following weeks the people who matter to {N} come to see what kind of member {N} is, and '
               'most of them respect it.'],
              ['Whichever way {N} goes, someone feels betrayed: the whips, the people back home, or {Ns} own '
               'conscience.',
               '{N} tries to please every side and ends up trusted by none of them.']),
 'options': [
    ('vote with the party you were elected for, and keep faith with its promises', 'W1', None, 0.45, '', {'identity': True, 'v': 'conformity, security', 'world': {'tribal': 'stand with the faction that sent you, and keep faith with its word', 'magic': 'cast with the faction whose seal you carry, and keep faith with its promises'}, 'chance': 0.82}),
    ('read every bill yourself, and vote on the evidence whatever the whips say', 'U1', None, 0.45, '', {'identity': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'weigh every choice yourself, and speak on what you know, whatever the faction says', 'magic': 'read every decree yourself, and cast on the evidence, whatever the wardens say'}, 'chance': 0.74}),
    ('vote with the whips, and make sure they know it, for a post later', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'world': {'tribal': "stand with the faction's heads, and make sure they remember it when duties are given", 'magic': 'cast with the faction, and make sure its wardens remember it when offices are given'}, 'chance': 0.91}),
    ('vote with your conscience against the whip, and say why in the chamber', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation, universalism', 'mark': 'defied an authority', 'self_control': '+', 'takes_if_fails': 'the party whip', 'world': {'tribal': 'stand against the faction when your heart says so, and say why at the fire', 'magic': "cast against the faction's line when your conscience says so, and say why in the Assembly"}, 'chance': 0.68}),
    ('vote as the constituency wants, every time, as one of its own', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'speak as your band wants, every time, as one of its own', 'magic': 'cast as your city wants, every time, as one of its own'}, 'chance': 0.72}),
    ('promise the constituency in public to vote against any bill that hurts it', 'W1', 'R.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'benevolence, universalism', 'mark': 'kept your word', 'world': {'tribal': 'swear to your band at the fire to oppose anything that hurts it', 'magic': 'swear to your city in its square to oppose any decree that hurts it'}, 'chance': 0.45}),
    ("become the house's expert on the one thing the constituency lives by", 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'achievement, tradition', 'world': {'tribal': "become the gathering's best knower of the one thing your band lives by", 'magic': "become the Assembly's master of the one trade your city lives by"}, 'chance': 0.72}),
    ('trade your vote for money for the constituency, promised in writing', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, benevolence', 'grants': 'counting the votes', 'world': {'tribal': 'trade your voice for a share of the hunting grounds for your band, sworn before the elders', 'magic': 'trade your lot for coin for your city, promised under seal'}, 'chance': 0.35}),
    ('join the rebels who want the bill rewritten, and help draft the amendment', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, universalism', 'grants': 'drafting policy', 'world': {'tribal': 'join the speakers who want the choice remade, and help shape the new words', 'magic': 'join the rebels who want the decree rewritten, and help draft the new clauses'}, 'chance': 0.71}),
    ('build your own power base in the region, so no whip can ever touch you', 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'power', 'world': {'tribal': 'gather the bands of your own valley behind you, so no faction head can touch you', 'magic': 'gather the towns of your own province behind you, so no warden can touch you'}, 'chance': 0.3}),
 ]},
{'name': 'the Thursday train home',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, family, friends',
 'horizon': 'months',
 'roles': 'partner, friend, colleague',
 'requires': 'member of parliament',
 'threshold': 'title:member of parliament',
 'step': 3,
 'worlds': {'earth': 'five months in, the Thursday train home: the weekend surgery, a partner who has run the house '
                     'alone all week, and old friends who now want favours',
            'tribal': 'five moons in, the gathering rests and you walk home to your own hearth, where your family '
                      'has managed without you and old friends want your voice',
            'magic': 'five months in, the Assembly rises for the week and the coach takes you home to a household '
                     'run without you, and to old friends with petitions'},
 'timing': {'times': 'per new member of parliament: once, about five months after taking the title, near the end of '
                     'the threshold season; about 1 life in 10,000 (House of Commons, ONS)'},
 'trigger': {'requires': 'in the threshold season of member of parliament, within the first six months after taking '
                         'the title: step 3, near the end of the six months, as the weeks in the capital and the '
                         'weekends at home settle into a pattern',
             'likelier': 'a constituency far from the capital; a partner and family who stayed at home; a member who '
                         'kept old friends in the town',
             'rarer': 'a seat in the capital itself; a member who lives alone or moved the family to the capital'},
 'scenes': {'earth': [('',
                       'Five months in, {N} knows the Thursday train by heart: the same seat, the case of '
                       'constituency letters, the window going dark. At home {partner} has run the house alone since '
                       'Monday, and the weekend is already full: a surgery on Friday, a fete on Saturday, and an old '
                       'friend who wants a quick word about a planning application.'),
                      ('W',
                       '{N} has kept every promise to the constituency and very few to the family. On the train {N} '
                       'writes a list of both.'),
                      ('U',
                       "{N} uses the three hours on the train to work through the week's casework, and has not "
                       'looked out of the window in months.'),
                      ('B',
                       "The old friend's quick word is about a planning application. {N} knows exactly what is being "
                       'asked, and what it might be worth.'),
                      ('R',
                       '{N} misses the old life: Friday nights out, saying whatever came to mind, and nobody '
                       'watching.'),
                      ('G',
                       'The town comes into view: the church tower, the river, the lights of the estate. Home, and '
                       'it feels further away each week.')],
            'tribal': [('',
                        'The gathering rests for a moon, and {N} walks home to {Ns} own hearth, where {partner} has '
                        'kept everything going alone and old friends are already waiting with favours to ask.')],
            'magic': [('',
                       'The Assembly rises for the week, and the coach takes {N} home to a household run without '
                       '{N}, and to old friends with petitions in hand.')]},
 'outcomes': (['The weekend holds, and on the last evening {N} leaves feeling like a person, not only a member.',
               '{partner} says that, for the first time in months, it felt as if {N} had come home.'],
              ['The calls and the callers keep coming all weekend, and Sunday is gone before it starts.',
               '{N} leaves again with the feeling that home has learned to run without {N}.']),
 'options': [
    ('keep Sunday for the family, whoever calls, and tell the constituency so', 'W1', None, 0.45, '', {'v': 'benevolence, security', 'world': {'tribal': 'keep one day at home for your kin, whoever comes to your hearth', 'magic': 'keep the rest-day for your household, whoever knocks, and tell the city so'}, 'chance': 0.74}),
    ('plan the weeks to the hour so the family gets fixed time, written in the diary', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'plan the moons ahead so your kin know when you will be home', 'magic': 'plan the weeks to the hour so your household gets fixed time, written in the book'}, 'chance': 0.88}),
    ('promise the old friend a look at the application, and make sure they owe you', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'promise the old friend your voice, and make sure they owe you', 'magic': 'promise the old friend a look at the petition, and make sure they owe you'}, 'chance': 0.94}),
    ('skip the Saturday fete and take your partner away for the weekend', 'R1', None, 0.45, '', {'door': True, 'v': 'hedonism, benevolence', 'world': {'tribal': 'leave the feast early and take your partner up into the hills for a few days', 'magic': 'skip the Saturday fair and take your partner away to the coast'}, 'chance': 0.95}),
    ('spend Saturday morning at the allotment on your own street, as you always did', 'G1', None, 0.45, '', {'v': 'tradition, hedonism', 'world': {'tribal': 'spend a morning gathering at the old places, as you always did'}, 'chance': 0.85}),
    ('bring the family along to the Friday surgery, so the work becomes a family thing', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'bring your kin to sit with you when the families come with their troubles', 'magic': 'bring your household to the petition day, so the work becomes a family thing'}, 'chance': 0.52}),
    ('write down what you can and cannot do for friends who ask, and share it', 'U1', 'W.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'tell your friends plainly at the fire what you can and cannot do for them', 'magic': 'write out what you can and cannot do for friends who ask, and send it round'}, 'chance': 0.85}),
    ('hire a sharp office manager to run the weekends, and buy back your Saturdays', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'world': {'tribal': "give a sharp young kinsman the families' troubles to sort, and win back your days", 'magic': 'hire a sharp steward to run the petition days, and buy back your rest-day'}, 'chance': 0.72}),
    ('turn the fete into a rally: speak from a lorry and work the crowd', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'grants': 'rousing a crowd', 'world': {'tribal': 'turn the feast into a rally: climb the rock and stir the crowd', 'magic': 'turn the fair into a rally: speak from a cart and work the crowd'}, 'chance': 0.89}),
    ('walk the dog by the river on Sunday morning, phone switched off', 'G1', 'R.7', 0.5, '', {'habit': True, 'v': 'hedonism, self-direction', 'world': {'tribal': 'walk alone by the river at dawn, with no one to answer', 'magic': 'walk by the river on the rest-day morning, with no one to answer'}, 'chance': 0.95}),
 ]},
{'name': 'the first morning at the department',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, work',
 'horizon': 'week',
 'roles': 'boss, colleague, friend',
 'requires': 'minister',
 'threshold': 'title:minister',
 'step': 1,
 'worlds': {'earth': 'the first morning as a minister: a car at the door, a private office of strangers, a box of '
                     'papers and a department of thousands',
            'tribal': "the first morning as keeper of one of the chief's duties, the hunt's share, the peace or the "
                      'trade, with the old hands who carried it for the last keeper',
            'magic': 'the first morning in an office of the Crown: the seal on the desk, ledgers to the ceiling, and '
                     'clerks who served ten councillors before you'},
 'timing': {'times': 'per new minister: once, in the first weeks after taking the title; about 1 life in 30,000 '
                     '(catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of minister, within the first six months after taking the title '
                         "(opened by 'the phone call from the leader' or any other way in): step 1, the first weeks "
                         'in the department',
             'likelier': 'a first ministerial post; a new government filling every post at once; a department the '
                         'person has never worked in',
             'rarer': 'a minister moved sideways from another department; a post without a department of its own'},
 'scenes': {'earth': [('',
                       'On the first morning a car comes for {N}. At the department a private office of six '
                       'strangers stands up when {N} walks in, the permanent secretary shakes hands, and there is a '
                       'box of papers on the desk with a note: "Decisions needed by Friday."'),
                      ('W',
                       '{N} reads the code for ministers and the rules on gifts and interests before opening the '
                       'box. It seems the right order.'),
                      ('U',
                       'There are two thousand pages of briefing. {N} reads the summaries first, then the annexes, '
                       'and starts a list of questions.'),
                      ('B',
                       'The department has a budget larger than some countries. {N} looks at the organisation chart '
                       'and sees where the power sits.'),
                      ('R',
                       '{N} grins at the car, the office and the people standing up, and wants to do something on '
                       'day one that the country will notice.'),
                      ('G',
                       'On the wall is a list of every minister since the department began. Some of the names {N} '
                       'learned at school.')],
            'tribal': [('',
                        "The chief has given {N} the keeping of one duty: the hunt's share, the peace, or the trade "
                        'with other clans. The old hands who kept it for the last keeper wait to see what {N} is.')],
            'magic': [('',
                       'On the desk in the office of the Crown lies a seal, and beside it ledgers to the ceiling. '
                       'The clerks, who served ten councillors before {N}, bow and wait.')]},
 'outcomes': (['By the end of the first day {N} has a desk, a team and the first decisions made.',
               'The people around {N} go home that evening saying the new minister will be all right.'],
              ['The first days are swallowed by introductions and rules, and the pile of decisions is still waiting '
               'at the end of the week.',
               'Something said on the first morning travels round the whole place by noon, and not in {Ns} favour.']),
 'options': [
    ('read the code for ministers, and declare every interest before opening the box', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': "ask the elders which gifts a keeper of the chief's duty may take, before taking any", 'magic': "read the code of the Crown's councillors, and declare every interest before breaking a seal"}, 'chance': 0.96}),
    ('read the whole briefing, and send back a list of hard questions by evening', 'U1', None, 0.45, '', {'v': 'achievement', 'world': {'tribal': 'hear out every old hand who kept the duty before you, and come back with hard questions', 'magic': "read the clerks' briefing rolls end to end, and send back hard questions by evening"}, 'chance': 0.88}),
    ('name your own adviser on the first day, before the department offers one', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'choose your own right hand on the first day, before the old hands offer one', 'magic': 'name your own secretary on the first day, before the clerks offer one'}, 'chance': 0.85}),
    ('announce one change on the first day, on the steps, before anyone can stop you', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'change one thing about the duty on the first day, before anyone can stop you', 'magic': 'proclaim one change on the first day, from the steps, before anyone can stop you'}, 'chance': 0.35}),
    ('walk the whole building on the first morning, floor by floor, and meet the staff', 'G1', None, 0.45, '', {'body': 'light', 'v': 'benevolence, tradition', 'mark': 'made a friend', 'world': {'tribal': 'walk out to every camp the duty touches, and meet the people who carry it', 'magic': 'climb the whole tower of offices on the first morning, and meet every clerk'}, 'chance': 0.85}),
    ('ask the permanent secretary for a frank account of what went wrong last time', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'conformity, achievement', 'world': {'tribal': 'ask the old hands for a plain account of where the last keeper went wrong', 'magic': 'ask the chief clerk for a frank account of where your predecessor went wrong'}, 'chance': 0.83}),
    ('work out which three decisions in the box will shape the year, and take them yourself', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'work out which three choices will shape the year, and keep them for yourself', 'magic': 'work out which three seals will shape the year, and set them yourself'}, 'chance': 0.68}),
    ('send the car away and take the bus, and make sure the cameras see it', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': "refuse the escort of young hunters and walk to the chief's fire alone, and let everyone see", 'magic': 'send the carriage away and walk through the market, and make sure the heralds see it'}, 'chance': 0.94}),
    ('ring the friends from home who were there at the start, and tell them first', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'send word first to the friends at your own hearth who were there at the start', 'magic': 'write first to the friends at home who were there at the start'}, 'chance': 0.97}),
    ('keep the private office your predecessor left, and trust the staff who know the work', 'G1', 'W.7', 0.5, '', {'v': 'tradition, security', 'world': {'tribal': 'keep the old hands the last keeper left, and trust them to know the work', 'magic': 'keep the clerks your predecessor left, and trust them to know the work'}, 'chance': 0.68}),
 ]},
{'name': 'the brief you did not ask for',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'public life, work',
 'horizon': 'months',
 'roles': 'boss, colleague, partner',
 'requires': 'minister',
 'threshold': 'title:minister',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the brief you were given is not the one you wanted, the subject is one you knew '
                     'nothing about, and the leader expects results',
            'tribal': 'two moons in, the chief gave you the peace with the river clans when you know only the hunt, '
                      'and the chief wants the peace kept',
            'magic': 'ten weeks in, the throne gave you the Wardenship of the Roads when your heart was in the '
                     'Treasury, and the throne expects the roads mended'},
 'timing': {'times': 'per new minister: once, about ten weeks into the threshold season, for about half of new '
                     "ministers (the season's middle step brings this moment or 'the decision that will carry your "
                     "name'); about 1 life in 30,000 is a minister (catalogue share; estimate), so about 1 in 60,000 "
                     'meet it'},
 'trigger': {'requires': 'in the threshold season of minister, within the first six months after taking the title: '
                         'step 2, some weeks into the post, when it is clear the post is not the one the person '
                         'hoped for',
             'likelier': 'a minister given a post outside their own field; a leader who uses posts to reward and to '
                         'punish; a junior post',
             'rarer': 'a minister given the post they asked for; a specialist appointed for their expertise'},
 'scenes': {'earth': [('',
                       'Ten weeks in, {N} is still the minister for a subject {N} knew nothing about on the day of '
                       'the phone call. {N} wanted another post; {boss} gave this one and wants results by the '
                       "summer. In the safe is a report on the department's failures that the last minister kept "
                       'from the house.'),
                      ('W',
                       'Ministers serve where they are sent. {N} has said it to {partner} several times this month, '
                       'as if to be convinced.'),
                      ('U',
                       'A whole new field to master: its law, its history, its numbers, its experts. Part of {N} is '
                       'delighted.'),
                      ('B', 'A post nobody wanted is a post nobody watches. {N} sees room in that.'),
                      ('R',
                       '{N} feels sidelined and a little humiliated, and the buried report makes {N} angrier every '
                       'time {N} reads it.'),
                      ('G',
                       'The officials have worked in this field for thirty years. {N} is the eleventh minister they '
                       'have had in that time.')],
            'tribal': [('',
                        'The chief gave {N} the peace with the river clans, when {N} knows only the hunt. The old '
                        'hands whisper about a promise the last keeper made to the river clans and never kept.')],
            'magic': [('',
                       'The throne gave {N} the Wardenship of the Roads, when {Ns} heart was in the Treasury. In a '
                       'locked chest lies the report on the roads that the last Warden kept from the Assembly.')]},
 'outcomes': (['By the end of the month {N} knows the subject well enough to hold a room on it.',
               '{boss} says in front of the others that {N} has taken a hard post and made something of it.'],
              ['Every week shows how little {N} knows, and the officials have started to manage {N} rather than '
               'serve.',
               '{Ns} frustration shows, and word reaches the leader that {N} is sulking.']),
 'options': [
    ('serve where the leader put you, and do the post properly, without complaint', 'W1', None, 0.45, '', {'v': 'conformity', 'world': {'tribal': 'keep the duty the chief gave you, and keep it well, without complaint', 'magic': 'serve where the throne put you, and do the office properly, without complaint'}, 'chance': 0.95}),
    ('read yourself into the subject: its law, its history and its experts, every evening', 'U1', None, 0.45, '', {'habit': True, 'v': 'achievement, self-direction', 'grants': 'drafting policy', 'world': {'tribal': 'learn everything about the duty from those who know it, every evening', 'magic': 'read yourself into the office: its law, its history and its scholars, every evening'}, 'chance': 0.72}),
    ('use the quiet post to build allies in cabinet for the post you really want', 'B1', None, 0.45, '', {'v': 'power, achievement', 'grants': 'allies in the party', 'world': {'tribal': "use the quiet duty to win friends among the chief's speakers for the duty you want", 'magic': 'use the quiet office to win friends among the councillors for the seat you want'}, 'chance': 0.78}),
    ('leak the buried report to a journalist friend, so the public knows', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'mark': 'hid a wrong', 'closed': "approval: leaking a confidential report; backfire: a leak inquiry traces it, and the leader asks for the minister's resignation", 'self_control': '-', 'world': {'tribal': 'tell a singer what the last keeper hid, so every fire hears of it', 'magic': 'slip the buried report to a broadsheet writer, so the whole city knows'}, 'chance': 0.92}),
    ('ask the oldest officials what was tried in this field before, and what came of it', 'G1', None, 0.45, '', {'v': 'tradition, achievement', 'world': {'tribal': 'ask the oldest hands what was tried before, and what came of it', 'magic': 'ask the oldest clerks what was tried before, and what came of it'}, 'chance': 0.75}),
    ('ask formally for a move at the next reshuffle, and do this post well meanwhile', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': 'ask the chief, by custom, for another duty at the next gathering, and keep this one well', 'magic': 'petition the throne for another office, and do this one well meanwhile'}, 'chance': 0.35}),
    ('find the bold reform this field has needed for years, and argue it on the evidence', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'world': {'tribal': 'find the bold change the duty has needed for years, and argue it from what is known'}, 'chance': 0.4}),
    ('keep the post safe: avoid every risk, guard the budget, and wait', 'B1', 'G.7', 0.5, '', {'v': 'security', 'self_control': '+', 'world': {'tribal': 'keep the duty safe: risk nothing, guard its share, and wait', 'magic': 'keep the office safe: risk nothing, guard its coffer, and wait'}, 'chance': 0.92}),
    ('publish the buried report yourself, openly, and take the blame for what it shows', 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'mark': 'owned up', 'world': {'tribal': 'tell the whole gathering what the last keeper hid, openly, and carry the blame', 'magic': 'publish the buried report yourself, under your own seal, and take the blame'}, 'chance': 0.65}),
    ('spend a week out in the field with the people the department serves, and listen', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'benevolence, universalism', 'world': {'tribal': 'spend a moon among the people the duty touches, and listen', 'magic': 'spend a week among the people the office serves, and listen'}, 'chance': 0.78}),
 ]},
{'name': 'the decision that will carry your name',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, meaning',
 'horizon': 'years',
 'roles': 'boss, colleague, rival',
 'requires': 'minister',
 'threshold': 'title:minister',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'ten weeks in, one decision in the department will outlast you, and how you make it will decide '
                     'what kind of minister you are',
            'tribal': 'two moons in, the duty the chief gave you holds one choice the clans will remember for a '
                      'generation, and it is yours to make',
            'magic': 'ten weeks in, one decree under your seal will outlast your office, and the court is waiting to '
                     'see what kind of councillor you are'},
 'timing': {'times': "per new minister: once in the threshold season, for about half of new ministers (the season's "
                     "middle step brings this moment or 'the brief you did not ask for'); about 1 life in 30,000 is "
                     'a minister (catalogue share; estimate), so about 1 in 60,000 meet it'},
 'trigger': {'requires': 'in the threshold season of minister, within the first six months after taking the title: '
                         "step 2, the season's transforming chance, when the department's big decision of the term "
                         "reaches the minister's desk",
             'likelier': 'a department with a reform long waited for; a leader who leaves the minister room to '
                         'choose; a full parliament still ahead',
             'rarer': 'a caretaker government near its end; a junior post with no decisions of its own'},
 'scenes': {'earth': [('',
                       'Ten weeks in, one decision in the department will outlast {N}: a reform the field has waited '
                       "years for, a rule that will bear the minister's name. {N} can make it in many ways, and each "
                       'would make a different kind of minister.'),
                      ('W',
                       '{N} wants a reform built to last: consulted on, written into law, defended in the house and '
                       'fair to everyone it touches.'),
                      ('U',
                       '{N} has the evidence, the pilots and the models. It could be the best-designed reform in a '
                       'generation, if {N} has the patience.'),
                      ('B',
                       'A reform that bears {Ns} name is power: in cabinet, in the party, in the next leadership '
                       'race. {N} means to make it count.'),
                      ('R',
                       'The people this field has failed are angry, and {N} is angry with them. This is the chance '
                       'to do something big, now.'),
                      ('G',
                       'Some things in this field have worked for a hundred years. {N} is wary of breaking what '
                       'holds, even while mending what does not.')],
            'tribal': [('',
                        'One choice in the duty the chief gave {N} will be remembered for a generation: how the '
                        'hunting grounds are shared, or which clans the band trades with. It is {Ns} to make.')],
            'magic': [('',
                       'One decree under {Ns} seal will outlast the office, and the whole court is waiting to see '
                       'what kind of councillor of the Crown {N} means to be.')]},
 'outcomes': (['The decision is made, and the department, grumbling or not, starts to carry it out.',
               'Over the following weeks the people who follow the field start to say what {N} stands for, and they '
               'say it right.'],
              ["The decision stalls between the officials and the leader's table, and the weeks run out.",
               'It goes through, but not as {N} meant it, and {Ns} name sits on something {N} barely recognises.']),
 'options': [
    ('consult everyone it touches, and write the reform into law, slowly and properly', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, conformity', 'grants': 'a reform with your name on it', 'world': {'tribal': 'hear every family it touches, and make the change a custom of the clans, slowly and properly', 'magic': 'hear everyone it touches, and write the reform into a decree, slowly and properly'}, 'chance': 0.2}),
    ('design it on the evidence, pilot it, and let the results decide', 'U1', None, 0.45, '', {'identity': True, 'v': 'universalism, achievement', 'grants': 'drafting policy', 'world': {'tribal': 'try it first in one camp, watch what happens, and let that decide'}, 'chance': 0.7}),
    ('make it your own, cut the deals in cabinet, and put your name on it', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'grants': 'a reform with your name on it', 'world': {'tribal': 'make it your own, strike the bargains among the speakers, and put your name to it', 'magic': 'make it your own, strike the bargains at court, and set your seal on it'}, 'chance': 0.2}),
    ('announce the reform in a fiery speech, before the department is ready', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation, self-direction', 'mark': 'took a wild risk', 'world': {'tribal': 'announce the change at the great fire, before the old hands are ready', 'magic': 'proclaim the reform in the Assembly, before the clerks are ready'}, 'chance': 0.52}),
    ('protect what works in the field, and change only what has clearly failed', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition', 'self_control': '+', 'chance': 0.65}),
    ('take up the cause of the people the field has failed, through a public inquiry', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism', 'world': {'tribal': 'take up the cause of the families the duty has failed, before the elders at the fire', 'magic': 'take up the cause of those the office has failed, through an open hearing at court'}, 'chance': 0.7}),
    ('build the reform from the ground up, region by region, with the people who live it', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'world': {'tribal': 'build the change from the ground up, camp by camp, with the people who live it', 'magic': 'build the reform from the ground up, town by town, with the people who live it'}, 'chance': 0.65}),
    ('trade support with two other ministers so the reform passes cabinet intact', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power', 'grants': 'allies in the party', 'world': {'tribal': "trade support with two other speakers so the change passes the chief's fire intact", 'magic': "trade support with two other councillors so the decree passes the Crown's council intact"}, 'chance': 0.62}),
    ('throw out the old approach entirely, and try something the field has never seen', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, self-direction', 'chance': 0.5}),
    ('hand the reform to the local bodies that know it best, and keep the centre out', 'G1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'self-direction, tradition', 'world': {'tribal': "leave the change in the hands of each camp, and keep the chief's fire out of it", 'magic': 'hand the reform to the towns and guilds that know it best, and keep the court out'}, 'chance': 0.3}),
 ]},
{'name': 'the department starts to trust you',
 'stages': 'adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, work',
 'horizon': 'months',
 'roles': 'colleague, boss, partner',
 'requires': 'minister',
 'threshold': 'title:minister',
 'step': 3,
 'worlds': {'earth': 'five months in, the officials have stopped handling you and started telling you things, and '
                     "the department's ways have become yours",
            'tribal': 'five moons in, the old hands bring you the truth before you ask, and the duty feels like your '
                      'own',
            'magic': 'five months in, the clerks bring you the real ledgers, not the fair copies, and the office '
                     'begins to feel like yours'},
 'timing': {'times': 'per new minister: once, about five months after taking the title, near the end of the '
                     'threshold season; about 1 life in 30,000 (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of minister, within the first six months after taking the title: '
                         'step 3, near the end of the six months, as minister and department settle together',
             'likelier': 'a minister who has listened to the officials; a quiet few months; a department with a '
                         'long-serving permanent secretary',
             'rarer': 'a minister at war with the department; a reshuffle rumour that makes everyone wait'},
 'scenes': {'earth': [('',
                       'Five months in, {N} notices a change. The permanent secretary has started to warn {N} before '
                       'trouble rather than after, and a junior official says in a meeting, "Minister, I think we '
                       'have this wrong," and nobody flinches.'),
                      ('W', 'The department has its rules and so does {N}, and they have found that the two fit.'),
                      ('U',
                       '{N} can now read a submission and find the weak paragraph in a minute. The officials have '
                       'noticed.'),
                      ('B',
                       'Trust is leverage. {N} knows which officials will go the extra mile, and which favours '
                       'bought it.'),
                      ('R',
                       '{N} still loses {Ns} temper sometimes, but the staff have learned it passes, and that {N} '
                       'always says sorry.'),
                      ('G',
                       'The rhythm of the department has become {Ns} rhythm: Monday papers, Wednesday questions, the '
                       'long table on Thursday.')],
            'tribal': [('',
                        'By the turn of the season the old hands bring {N} the truth before {N} asks, and the duty '
                        'feels like {Ns} own.')],
            'magic': [('',
                       'Five months in, the clerks bring {N} the real ledgers, not the fair copies, and the office '
                       'of the Crown begins to feel like {Ns} own.')]},
 'outcomes': (['By the end of the month the department brings {N} problems early, while they can still be fixed.',
               'A senior official says, privately, that {N} is the best minister they have served in years.'],
              ['One bad week and one sharp word in public, and the trust built over months is gone.',
               "The officials trust {N}, but the leader's office does not, and decisions are taken over {Ns} head."]),
 'options': [
    ('thank officials in writing, by name, for each piece of good work', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'grants': 'officials who trust you', 'world': {'tribal': 'thank each old hand at the fire, by name, for each piece of good work', 'magic': 'thank the clerks under your seal, by name, for each piece of good work'}, 'chance': 0.92}),
    ('ask the officials where your own judgments have gone wrong so far', 'U1', None, 0.45, '', {'door': True, 'v': 'achievement, universalism', 'grants': 'officials who trust you', 'world': {'tribal': 'ask the old hands where your own judgments have gone wrong so far', 'magic': 'ask the clerks where your own judgments have gone wrong so far'}, 'chance': 0.81}),
    ('use the new trust to move your own people into the key posts', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'use the new trust to put your own people where the duty is decided'}, 'chance': 0.89}),
    ('take the private office out for a long night to celebrate the half-year', 'R1', None, 0.45, '', {'v': 'hedonism', 'mark': 'made a friend', 'world': {'tribal': 'hold a feast for the old hands to mark the turn of the season', 'magic': 'take your clerks to the best tavern in the city for a long night'}, 'chance': 0.95}),
    ("keep the department's old Friday tea, and go to it every week", 'G1', None, 0.45, '', {'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'sit with the old hands at their evening fire, every night you can', 'magic': "keep the office's old custom of a Friday cup, and go to it every week"}, 'chance': 0.94}),
    ('back an official in public when the mistake was your own', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'owned up', 'grants': 'officials who trust you', 'world': {'tribal': 'stand up for an old hand at the fire when the mistake was your own', 'magic': 'defend a clerk at court when the mistake was your own'}, 'chance': 0.8}),
    ("write down how the department's decisions should be made, and follow it yourself", 'U1', 'W.7', 0.5, '', {'v': 'conformity, achievement', 'self_control': '+', 'world': {'tribal': "set out plainly how the duty's choices should be made, and keep to it yourself", 'magic': "write down how the office's decisions should be sealed, and keep to it yourself"}, 'chance': 0.88}),
    ('trade a favour with the treasury for the data system the officials have begged for', 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, power', 'world': {'tribal': 'trade a favour with the keeper of the stores for the tally-sticks the old hands have begged for', 'magic': 'trade a favour with the Treasury for the warded archive the clerks have begged for'}, 'chance': 0.45}),
    ('tell the officials bluntly that those who deliver will be the ones who rise', 'R1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': 'tell the old hands plainly that those who deliver will be the ones who rise'}, 'chance': 0.83}),
    ('take a day off with your family, and let the department run itself', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'world': {'tribal': 'spend a day with your kin by the water, and let the duty run itself', 'magic': 'take a day with your household in the country, and let the office run itself'}, 'chance': 0.79}),
 ]},
{'name': 'the door closes behind you',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'public life, home',
 'horizon': 'week',
 'roles': 'colleague, friend, partner',
 'requires': 'head of government',
 'threshold': 'title:head of government',
 'step': 1,
 'worlds': {'earth': 'the first night in office: the famous door, the cameras, a few words on the step, and inside a '
                     'building of strangers and a pile of sealed letters',
            'tribal': 'the first night as chief of the gathered clans: the great fire, the clan heads around it, and '
                      'every face turned to you',
            'magic': 'the first night as Chancellor: the chain, a first audience at the foot of the throne, and a '
                     'tower of rooms full of strangers'},
 'timing': {'times': 'per new head of government: once, in the first weeks after taking the title; about 1 life in '
                     'two to three million (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of head of government, within the first six months after taking '
                         "the title (opened by 'the country goes to the polls', a coalition deal, a leader who falls "
                         'in office or any other way in): step 1, the first days in office',
             'likelier': 'a general election won; a change of government after years in opposition; a leader new to '
                         'high office',
             'rarer': 'a leader who takes over in mid-term and keeps the same cabinet; a caretaker head of '
                      'government'},
 'scenes': {'earth': [('',
                       'The cameras flash, {N} says a few words on the step, and the door closes behind {N}. Inside, '
                       'the staff line the corridor and clap. Then the cabinet secretary takes {N} to a small room '
                       'with a pile of sealed letters, briefings only the head of government is told, and a file the '
                       'last government hoped would never come out.'),
                      ('W',
                       '{N} reads the guidance on the constitution and the office on the first night, slowly, the '
                       'way some people read scripture.'),
                      ('U',
                       'The secret briefings are worse and stranger than {N} imagined. {N} has questions, and the '
                       'first night is not long enough for them.'),
                      ('B',
                       'The whole machinery of the state now answers to {N}. {N} can feel it hum, and sets out to '
                       'learn which levers move what.'),
                      ('R',
                       '{N} can hardly believe it, and wants to ring {friend}, laugh out loud and open a window to '
                       'the noise outside.'),
                      ('G',
                       'In the corridor hang the portraits of everyone who held the office before. {N} looks at the '
                       'oldest one for a long time.')],
            'tribal': [('',
                        'As the great fire is lit, the heads of the clans sit down around it and turn to {N}. {N} '
                        'has seen chiefs sit in that place since childhood, and now it is {Ns}.')],
            'magic': [('',
                       "At the foot of the throne {N} kneels and receives the Chancellor's chain. Then the doors "
                       'close, and the clerks lead {N} up a tower of rooms full of strangers and sealed letters.')]},
 'outcomes': (['By morning {N} has read what must be read, and the first day starts with a plan.',
               'The staff, who have seen many first nights, tell each other that this one will be all right.'],
              ['The first night runs out before the briefings do, and {N} starts the first day already behind.',
               'A first-night choice is all anyone talks about by morning, and not as {N} would have wished.']),
 'options': [
    ("keep the last government's embarrassing file sealed, to protect the office", 'W1', None, 0.45, '', {'v': 'security, conformity', 'mark': 'hid a wrong', 'closed': 'approval: keeping a file from a public inquiry; backfire: a leak, and an inquiry into the cover-up', 'self_control': '-', 'world': {'tribal': "keep silent about what the last chief did wrong, to protect the chief's place", 'magic': "keep the last Chancellor's shameful file under seal, to protect the office"}, 'chance': 0.9}),
    ('read every secret briefing through the night, and send back questions by dawn', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'world': {'tribal': 'listen through the night to everything the old hands say a chief must know', 'magic': 'read every sealed briefing through the night, and send back questions by dawn'}, 'chance': 0.92}),
    ('appoint your chief of staff and your inner circle before the first morning', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': 'choose your right hand and your closest circle before the first dawn', 'magic': 'name your first secretary and your inner circle before the morning bell'}, 'chance': 0.95}),
    ('go back out to the cameras and say what you really feel, unscripted', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'go back out to the fire and say what you really feel, as it comes', 'magic': 'step back out before the crowd and say what you really feel, unscripted'}, 'chance': 0.78}),
    ('spend the first night with your family in the official flat, and make it home', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': "spend the first night with your kin at the chief's fire, and make it home", 'magic': "spend the first night with your household in the Chancellor's tower, and make it home"}, 'chance': 0.88}),
    ('go through the rules of the office with the cabinet secretary, line by line', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': "sit with the eldest of the clans through the night and learn the chief's customs", 'magic': 'go through the law of the office with the chief clerk of the Chancellery, line by line'}, 'chance': 0.95}),
    ('spend the first night working out who in your own cabinet could unseat you', 'U1', 'B.7', 0.5, '', {'v': 'power, security', 'world': {'tribal': 'spend the first night working out which clan head could bring you down', 'magic': 'spend the first night working out who at court could unseat you'}, 'chance': 0.8}),
    ('throw a party for the campaign team in the official rooms on the first night', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, power', 'world': {'tribal': 'throw a feast for the young ones who carried your name, on the first night', 'magic': "throw a feast for your retinue in the Chancellor's hall on the first night"}, 'chance': 0.94}),
    ('walk back out on the first night, through the crowd that waited outside', 'R1', 'G.7', 0.5, '', {'body': 'light', 'v': 'benevolence, stimulation', 'world': {'tribal': 'walk out from the fire on the first night among all the clans who waited', 'magic': 'walk out of the tower on the first night, through the crowd that waited at the gate'}, 'chance': 0.88}),
    ('write by hand to every living former head of government, and ask for their counsel', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'send word to every living chief before you, and ask for their counsel', 'magic': 'write by hand to every living Chancellor before you, and ask for their counsel'}, 'chance': 0.84}),
 ]},
{'name': "the government's first crisis",
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'public life, work',
 'horizon': 'months',
 'roles': 'colleague, rival, elder',
 'requires': 'head of government',
 'threshold': 'title:head of government',
 'step': 2,
 'worlds': {'earth': 'ten weeks in, the first crisis: a flood, a failing bank, a strike or trouble at the border, '
                     'and every eye on the new head of government',
            'tribal': 'two moons in, the first hard moon as chief: raiders on the far bank or a flood that drowns a '
                      'camp, and every clan watching what the new chief does',
            'magic': 'ten weeks in, the first storm of the new Chancellery: a surge of wild magic in a northern '
                     'city, a guild revolt or a blight, and the court watching'},
 'timing': {'times': 'per new head of government: once, about ten weeks into the threshold season, for about half of '
                     "new heads of government (the season's middle step brings this moment or 'what this government "
                     "is for'); most new governments meet a crisis in their first months (estimate); about 1 life in "
                     'two to three million heads a government (catalogue share; estimate), so about 1 in four to six '
                     'million meet it'},
 'trigger': {'requires': 'in the threshold season of head of government, within the first six months after taking '
                         'the title: step 2, some weeks into office, when the first crisis of the term breaks',
             'likelier': 'hard years (unrest, a harsh season); a government elected in a crisis; a thin majority',
             'rarer': 'calm and prosperous years; a head of government who takes over a crisis already under '
                      'control'},
 'scenes': {'earth': [('',
                       'Ten weeks in, the first real crisis lands: {disaster} in the north, or a bank in trouble, '
                       'and the news has nothing else. The cabinet room fills. Every option has a cost, and the new '
                       'government will be judged by the next three days.'),
                      ('W',
                       'There is a plan for this, written years ago and kept in a binder. {N} asks for it first.'),
                      ('U',
                       '{N} wants the facts before the decisions: the numbers, the models and the experts, all in '
                       'one room, now.'),
                      ('B',
                       'A crisis is also a chance: to act fast, to look strong, to get through measures that would '
                       'never pass in a calm week.'),
                      ('R',
                       '{N} wants to be there, on the ground, with the people it is happening to, not in a meeting '
                       'room.'),
                      ('G',
                       '{N} remembers how the old leaders handled the last crisis like this, and what the country '
                       'needed then: calm, and time.')],
            'tribal': [('',
                        'Two moons in, raiders cross the far river, or a flood drowns a camp, and every clan watches '
                        'what the new chief does.')],
            'magic': [('',
                       'Ten weeks into the new Chancellery a surge of wild magic tears through a northern city, and '
                       'the court and the Orders watch what the Chancellor does.')]},
 'outcomes': (['The crisis passes, the response holds, and the country decides the new head of government can be '
               'trusted with a hard week.',
               'Even the other side admits, grudgingly, that it was handled well.'],
              ['The response stumbles in the first days, and the stumble becomes the story of the government.',
               'The crisis passes, but one decision taken in the heat of it will cost {N} for years.']),
 'options': [
    ('follow the emergency plan the state already has, step by step, and chair every meeting', 'W1', None, 0.45, '', {'v': 'security, conformity', 'world': {'tribal': 'follow the old ways the clans keep for such times, step by step, and lead every council', 'magic': "follow the realm's old plan for such times, step by step, and chair every council"}, 'chance': 0.75}),
    ('bring the best experts into one room, and decide nothing until you have the facts', 'U1', None, 0.45, '', {'door': True, 'v': 'universalism, achievement', 'world': {'tribal': 'call those who know the land and the weather best, and decide nothing until you know', 'magic': 'summon the best scholars and mages into one room, and decide nothing until you have the facts'}, 'chance': 0.7}),
    ('use the crisis to push through powers the government has wanted for years', 'B1', None, 0.45, '', {'v': 'power', 'world': {'tribal': "use the danger to take powers the chief's fire has long wanted", 'magic': 'use the crisis to take powers the Chancellery has wanted for years'}, 'chance': 0.58}),
    ('go to where it is happening the same day, and stand with the people there', 'R1', None, 0.45, '', {'door': True, 'body': 'light', 'v': 'benevolence, stimulation', 'world': {'tribal': 'go to the stricken camp the same day, and stand with its people', 'magic': 'ride to the stricken city the same day, and stand with its people'}, 'chance': 0.92}),
    ("stay calm, do less, and let the country's old institutions do what they know", 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'keep calm, do little, and let each clan do what it has always done in hard times', 'magic': 'keep calm, do less, and let the old Orders and guilds do what they know'}, 'chance': 0.4}),
    ('take personal charge of the response, with a daily briefing you give yourself', 'W1', 'B.7', 0.5, '', {'v': 'power', 'grants': 'handling the press', 'world': {'tribal': 'take the whole response into your own hands, and speak to the clans every evening', 'magic': "take the response into your own hands, and send out a herald's bulletin every day"}, 'chance': 0.75}),
    ('throw out the old plan, and improvise a new one from the facts, fast', 'U1', 'R.7', 0.5, '', {'v': 'self-direction', 'chance': 0.4}),
    ('strike a quick deal with the big firms to keep the jobs in the stricken region', 'B1', 'G.7', 0.5, '', {'v': 'power', 'world': {'tribal': 'strike a quick bargain with the strongest clan to feed the stricken camps', 'magic': 'strike a quick bargain with the merchant houses to keep the stricken city fed'}, 'chance': 0.62}),
    ('tell the country the plain truth tonight, the bad parts included', 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'grants': 'a name for straight talk', 'world': {'tribal': 'tell all the clans the plain truth at the fire tonight, the worst of it too', 'magic': 'tell the realm the plain truth by the heralds tonight, the worst of it too'}, 'chance': 0.75}),
    ('call the leader who handled the last crisis like this, and ask what they learned', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'tradition, achievement', 'world': {'tribal': 'go to the old chief who led the clans through the last such time, and ask what was learned', 'magic': 'seek out the old Chancellor who weathered the last such storm, and ask what was learned'}, 'chance': 0.8}),
 ]},
{'name': 'what this government is for',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, meaning',
 'horizon': 'years',
 'roles': 'colleague, rival, partner',
 'requires': 'head of government',
 'threshold': 'title:head of government',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'ten weeks in, the work of government has filled every hour, and you must decide what this '
                     'government is for before the days decide it for you',
            'tribal': 'two moons in, the clans followed you for a reason, and before the summer ends you must say '
                      'what your time as chief is for',
            'magic': 'ten weeks in, the throne asks its new Chancellor, before the whole court, what this '
                     'Chancellery will be remembered for'},
 'timing': {'times': 'per new head of government: once in the threshold season, for about half of new heads of '
                     "government (the season's middle step brings this moment or 'the government's first crisis'); "
                     'about 1 life in two to three million heads a government (catalogue share; estimate), so about '
                     '1 in four to six million meet it'},
 'trigger': {'requires': 'in the threshold season of head of government, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, once the first weeks of governing "
                         'have shown how little time there is',
             'likelier': 'a government with a majority and a full term ahead; a leader who won on a mood rather than '
                         'a programme',
             'rarer': 'a caretaker or a minority government living week to week'},
 'scenes': {'earth': [('',
                       'Ten weeks in, the diary is full and the crises keep coming. One evening {N} sits with a '
                       "blank sheet of paper and the cabinet's long list, and asks the question the campaign never "
                       'had time for: what is this government for?'),
                      ('W',
                       '{N} thinks of the constitution, the courts, the civil service: the institutions that must '
                       'still stand when {N} is gone.'),
                      ('U',
                       '{N} sees the long game: the plans that will take ten years, and the strategy that keeps a '
                       'government alive long enough to finish them.'),
                      ('B',
                       'Power is a window that closes. {N} knows how many months of real authority a new government '
                       'has, and means to use every one.'),
                      ('R',
                       '{N} remembers the faces in the crowds during the campaign, the angry and the hopeful. This '
                       'government is for them, or it is for nothing.'),
                      ('G',
                       '{N} thinks of the country as something old and living: its land, its towns, its ways. A '
                       'government should guard it, not remake it.')],
            'tribal': [('',
                        'The clans followed {N} for a reason. Before the summer ends {N} must say at the great fire '
                        'what this time as chief is for.')],
            'magic': [('',
                       'Before the whole court the throne asks its new Chancellor what this Chancellery will be '
                       'remembered for, and the Orders lean in to hear the answer.')]},
 'outcomes': (['The answer, once given, holds: ministers, officials and the country start to know what the '
               'government is for.',
               'Months later people who never backed {N} can still say what {N} stands for, and say it fairly.'],
              ["The answer is lost in the next week's crises, and the government drifts from day to day.",
               'What {N} says the government is for and what it does start to drift apart, and the other side '
               'notices first.']),
 'options': [
    ('govern through the institutions, and leave them stronger than before', 'W1', None, 0.45, '', {'identity': True, 'v': 'universalism, security', 'world': {'tribal': "lead through the clans' councils and customs, and leave them stronger than before", 'magic': 'govern through the Assembly, the courts and the Orders, and leave them stronger than before'}, 'chance': 0.72}),
    ('set three long goals, plan every year toward them, and promise nothing you cannot measure', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'set three long aims for the clans, plan every season toward them, and promise nothing you cannot show'}, 'chance': 0.72}),
    ('gather every lever of the state into your own office, and use them while they last', 'B1', None, 0.45, '', {'identity': True, 'v': 'power', 'world': {'tribal': 'gather every power of the gathering into your own hands, and use them while they last', 'magic': 'gather every lever of the realm into the Chancellery, and use them while they last'}, 'chance': 0.75}),
    ('govern as the voice of the people who sent you, and say so every day', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, stimulation', 'grants': 'rousing a crowd', 'world': {'tribal': 'lead as the voice of the bands who raised you, and say so at every fire', 'magic': 'govern as the voice of the common folk who raised you, and say so in every square'}, 'chance': 0.75}),
    ("guard the country's land, towns and ways, and change only what must change", 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition', 'world': {'tribal': "guard the clans' lands, hunts and ways, and change only what must change", 'magic': 'ask the oldest oracle of the realm what the land needs, and guard that above all'}, 'chance': 0.72}),
    ("write a charter of the people's rights, and bind the government to it", 'W1', 'R.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'set down before all the clans what no chief may take from a family, and bind yourself to it', 'magic': "draft a charter of the people's rights, and bind the Chancellery to it by oath"}, 'chance': 0.3}),
    ("plan a generation's renewal of the land, the rivers and the forgotten towns", 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'world': {'tribal': "plan, for a generation, how the clans can share the valley's land and rivers", 'magic': "plan a generation's renewal of the land, the rivers and the forgotten towns of the realm"}, 'chance': 0.58}),
    ('build a coalition so broad that nobody can bring the government down', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power', 'grants': 'coalition building', 'world': {'tribal': 'bind so many clans to your fire that nobody can bring you down', 'magic': 'bind so many factions and Orders to you that nobody can bring the Chancellery down'}, 'chance': 0.35}),
    ('try bold reforms quickly, and keep only what works', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation, achievement', 'world': {'tribal': 'try new ways quickly, and keep only what works'}, 'chance': 0.4}),
    ('make the country strong on its own: its food, its energy and its towns', 'G1', 'B.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, tradition', 'world': {'tribal': 'make the clans strong on their own: their food, their stores and their camps', 'magic': 'make the realm strong on its own: its grain, its mines and its towns'}, 'chance': 0.65}),
 ]},
{'name': 'the country gets used to your face',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'public life, family, friends',
 'horizon': 'months',
 'roles': 'partner, friend, colleague',
 'requires': 'head of government',
 'threshold': 'title:head of government',
 'step': 3,
 'worlds': {'earth': 'five months in, the country has got used to your face: comedians do your voice, strangers know '
                     'your walk, and your family lives behind a police cordon',
            'tribal': 'five moons in, every clan knows your face, the singers make songs of you, and your kin cannot '
                      'go to the river without being stared at',
            'magic': 'five months in, your likeness is on the broadsheets in every city, the minstrels mock your '
                     'walk, and your household lives behind warded doors'},
 'timing': {'times': 'per new head of government: once, about five months after taking the title, near the end of '
                     'the threshold season; about 1 life in two to three million (catalogue share; estimate)'},
 'trigger': {'requires': 'in the threshold season of head of government, within the first six months after taking '
                         "the title: step 3, near the end of the six months, as the office becomes the person's "
                         'daily life',
             'likelier': 'a leader new to fame; a family that had a private life before; old friends who stayed in '
                         'the home town',
             'rarer': 'a leader who was already a household name; a leader with no family at home'},
 'scenes': {'earth': [('',
                       'Five months in, the country has got used to {N}. A comedian on television does {Ns} voice '
                       'better than {N} does, {partner} has given up going to the supermarket, and every old friend '
                       'either has a favour to ask or has stopped calling.'),
                      ('W',
                       '{N} has learned the weight of the office: every word is weighed and every gesture read. {N} '
                       'carries it carefully, and it is heavy.'),
                      ('U',
                       '{N} studies the polls and the clips, and finds it strange to read about a person who both is '
                       'and is not {N}.'),
                      ('B',
                       'Recognition is power. A face the whole country knows opens any door, and {N} has stopped '
                       'pretending not to enjoy it.'),
                      ('R',
                       '{N} misses walking down a street unseen, sitting in a pub, saying something foolish without '
                       'it being news.'),
                      ('G',
                       'The house in the home town stands empty most weeks. The neighbours keep an eye on it, and '
                       'send word that the garden is overgrown.')],
            'tribal': [('',
                        'Five moons in, every clan knows {Ns} face, the singers make mocking songs of {Ns} walk, and '
                        '{partner} cannot go to the river without being stared at.')],
            'magic': [('',
                       'Five months in, {Ns} likeness is on broadsheets in every city, the minstrels mock {Ns} walk, '
                       'and the household lives behind warded doors.')]},
 'outcomes': (["The country's gaze becomes something {N} can carry, and the family finds a way to live inside it.",
               '{partner} says one evening, laughing, that they have got used to the face too.'],
              ['The attention never lets up, and {N} snaps in public at the end of a long week.',
               'An old friend sells a story about {N}, and the family closes ranks a little tighter.']),
 'options': [
    ('keep to the duties of the office in public, and never let the mask slip', 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '+', 'world': {'tribal': "keep to the chief's duties before the clans, and never let the mask slip"}, 'chance': 0.84}),
    ('study how the country sees you, and change one thing a month on purpose', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'listen to how the clans speak of you, and change one thing each moon on purpose', 'magic': 'study how the realm sees you, and change one thing each month on purpose'}, 'chance': 0.85}),
    ('use the famous face: every visit, every handshake, every photograph, for the next election', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'use the face every clan knows: every visit, every gift, every feast, for the next gathering', 'magic': 'use the face the realm knows: every visit, every handshake, every portrait, for the next lots'}, 'chance': 0.8}),
    ('slip out one evening without the cameras, and have a drink with old friends', 'R1', None, 0.45, '', {'habit': True, 'v': 'hedonism, self-direction', 'world': {'tribal': "slip away one night without your guards, and sit at an old friend's fire", 'magic': 'slip out one evening without the guards, and drink with old friends in a tavern'}, 'chance': 0.65}),
    ('go home to your own town one weekend a month, and walk its streets as before', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'world': {'tribal': "go back to your own band's camp each moon, and walk among its hearths as before", 'magic': 'go home to your own town each month, and walk its lanes as before'}, 'chance': 0.65}),
    ('hold an open door every week for people from every part of the country', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'keep your fire open each moon to anyone from any clan', 'magic': 'hold an open audience every week for anyone from any part of the realm'}, 'chance': 0.7}),
    ('set clear rules on what friends and family may ask of the office', 'U1', 'W.7', 0.5, '', {'v': 'conformity, security', 'world': {'tribal': 'tell your kin and friends plainly what they may and may not ask of the chief'}, 'chance': 0.92}),
    ('hire the best people money can buy to manage your image and your diary', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'gather the cleverest young ones to shape how the clans see you', 'magic': 'hire the best heralds and secretaries gold can buy to manage your name and your days'}, 'chance': 0.92}),
    ('laugh at the comedians in public, and do the voice better than they do', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, power', 'world': {'tribal': "laugh at the singers' mocking songs, and sing them back better at the fire", 'magic': "laugh at the minstrels' mockery in public, and do the voice better than they do"}, 'chance': 0.75}),
    ('plant a tree in the official garden with your family, and keep one corner wild', 'G1', 'R.7', 0.5, '', {'body': 'light', 'v': 'hedonism, benevolence', 'world': {'tribal': "plant a sapling by the chief's fire with your kin, and leave one patch wild", 'magic': 'plant a tree in the Chancellery garden with your household, and keep one corner wild'}, 'chance': 0.96}),
 ]},
{'name': 'an omen at the council fire',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.1, 0.1, 0.1, 0.1),
 'drivers': 'harsh+.2 unrest+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, meaning',
 'horizon': 'moment',
 'roles': 'elder, rival, friend, partner',
 'requires': 'council candidate',
 'worlds': {'tribal': 'as the band weighs who will be heard at the fire, a sign comes, and every face turns to you'},
 'only': 'tribal',
 'timing': {'times': 'per council candidate in the tribal world: about 1 candidacy in 10 meets a sign the band reads '
                     'for or against the person (estimate)',
            'likelier': 'a hard season, a band that keeps close to its shaman, a close choice between two who ask to '
                        'be heard',
            'rarer': 'easy years, elders who put little weight on signs, a choice already settled'},
 'scenes': {'tribal': [('',
                        'The band sits close around the council fire to weigh who will be heard this winter. Out of '
                        'the dusk a hawk stoops low and leaves a feather turning at {Ns} feet, and every voice '
                        'stops.'),
                       ('W',
                        'There is a custom for this, as for everything: a sign belongs to the elders to read, not to '
                        'the one it falls beside. {N} keeps still and waits for {elder} to speak.'),
                       ('U',
                        '{N} watches the faces around the fire more closely than the feather. A hawk hunting at dusk '
                        'is nothing strange; what the band makes of it is another matter.'),
                       ('B',
                        'Every eye in the band is on {N}, and {rival} has gone quiet across the fire. A moment like '
                        'this does not come twice.'),
                       ('R',
                        '{Ns} heart is pounding. The feather is still rocking in the dust, and {N} wants to snatch '
                        'it up and speak before the moment cools.'),
                       ('G',
                        'The hawk has hunted over this valley for as long as {N} can remember. If the spirits are '
                        'speaking through it, {N} wants to hear what they truly mean.')]},
 'outcomes': (['By the time the fire burns low, the band has settled things the way {N} hoped.',
               'The elders nod to {N} across the fire, and the talk of the sign goes on for days.'],
              ["The elders read the sign another way, and the band's eyes move on to {rival}.",
               'Someone laughs at the wrong moment, and whatever the sign meant is lost in the noise.']),
 'options': [
    ('ask the elders to read the sign by the old custom, and abide by their word', 'W1', None, 0.45, '', {'title': 'local councillor', 'v': 'tradition, conformity', 'self_control': '+', 'chance': 0.5}),
    ("slip a second feather into the elders' bundle, so the reading comes out your way", 'U1', None, 0.45, '', {'title': 'local councillor', 'mark': 'hid a wrong', 'closed': 'approval: faking a sign before the band; backfire: someone saw the feather planted, and the whole band turns away', 'v': 'power, achievement', 'self_control': '-', 'chance': 0.5}),
    ('pick up the feather and tell the band the hawk came for you', 'B1', None, 0.45, '', {'act': 'pick up the feather and tell the band the hawk came for them', 'title': 'local councillor', 'aims': 'local councillor', 'identity': True, 'v': 'power, achievement', 'chance': 0.5}),
    ('jump up while every face is turned, and speak from the heart about the winter', 'R1', None, 0.45, '', {'title': 'local councillor', 'aims': 'local councillor', 'v': 'stimulation, self-direction', 'chance': 0.5}),
    ('carry the feather to the shaman, and let its meaning come in its own time', 'G1', None, 0.45, '', {'title': 'local councillor', 'v': 'tradition', 'self_control': '+', 'chance': 0.5}),
    ('say a hunting hawk is no sign, and ask to be judged on your work', 'W.34 U.33 R.33', None, 0.5, '', {'identity': True, 'grants': 'a name for straight talk', 'v': 'universalism, self-direction', 'chance': 0.75}),
    ('say the sign fell for your friend, and stand behind your friend instead', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence', 'chance': 0.8}),
    ('remind the band that your family has spoken at this fire for three generations', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'a following in the party', 'v': 'tradition, power', 'chance': 0.6}),
    ('promise the young hunters first share of the next kill for their voices', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'a loyal campaign team', 'v': 'power, achievement', 'chance': 0.8}),
    ('say nothing, and watch who looks at the feather and who looks away', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'counting the votes', 'v': 'security, power', 'chance': 0.85}),
 ]},
{'name': 'the spirits turn from the leader',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.05, 0.05, 0.05, 0.05),
 'drivers': 'harsh+.4 unrest+.2 prosper-.3 trouble+.15',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, meaning',
 'horizon': 'months',
 'roles': 'elder, rival, partner, friend',
 'requires': 'mayor | member of parliament | party leader | head of government',
 'worlds': {'tribal': 'the herds have not come, the children are sick, and the band whispers that the spirits have '
                      'turned from you'},
 'only': 'tribal',
 'timing': {'times': 'per head of the camp, speaker, faction head or chief in the tribal world a year: about 5 in '
                     '100, after a failed hunt or a sickness (estimate)',
            'likelier': 'a hard winter, a hunt that fails twice running, a sickness in the camp, a rival who keeps '
                        'the whispering going',
            'rarer': 'good seasons, a shaman who stands by the leader, a leader who shares the hard choices with the '
                     'elders'},
 'scenes': {'tribal': [('',
                        'For the second moon the herds have not come down the valley, and a cough has gone round the '
                        'hearths. Wherever {N} walks the talk stops, and {rival} is heard saying the spirits no '
                        'longer walk with the one who leads.'),
                       ('W',
                        '{N} has led by the customs the band has always kept. If a rite was missed or a taboo '
                        'broken, it must be put right in front of everyone.'),
                       ('U',
                        '{N} goes over every step of the last hunts, the winds and the trails. Herds do not vanish '
                        'for no reason, and neither do coughs.'),
                       ('B',
                        '{N} hears the whispers for what they are: {rival} reaching for the place at the head of the '
                        'fire. The surest answer to hunger is meat, brought home by the one who leads.'),
                       ('R',
                        '{N} is sick of the whispering and the long faces, and of {rival} smiling through all of it. '
                        'Sitting by the fire and waiting is the worst of it.'),
                       ('G',
                        'The seasons turn as they will, lean years after fat ones. {N} wonders whether this is a '
                        'sign to lead differently, or to let another lead.')]},
 'outcomes': (['Before the next moon the mood of the band turns, and the whispering dies away.',
               'The herds come back down the valley, and the families speak of {N} with respect again.'],
              ['The whispering grows louder, and the families start to gather at the fire of {rival}.',
               'The sickness lingers through the winter, and the band remembers who was leading when it came.']),
 'options': [
    ('perform the rite of asking pardon before the whole band, as custom demands', 'W1', None, 0.45, '', {'identity': True, 'habit': True, 'v': 'tradition, conformity', 'chance': 0.6}),
    ("follow the herds' old trails for days, and show the band where they went", 'U1', None, 0.45, '', {'body': 'heavy', 'v': 'universalism, achievement', 'self_control': '+', 'chance': 0.7}),
    ('swear to bring meat home, and drive the best hunters out over the far ridge', 'B1', None, 0.45, '', {'binds': True, 'body': 'heavy', 'v': 'achievement, power', 'chance': 0.55}),
    ('accuse a rival at the fire of breaking a hunting taboo before the hunt', 'R1', None, 0.45, '', {'mark': 'made an enemy', 'closed': "approval: a charge made without proof; backfire: the rival's kin prove it false, and the band turns on the accuser", 'v': 'power, security', 'chance': 0.65}),
    ('step down, and let the band choose another to lead through the lean time', 'G1', None, 0.45, '', {'drops': 'mayor; member of parliament', 'identity': True, 'v': 'tradition', 'mark': 'gave in to pressure', 'chance': 0.9}),
    ('sit with the shaman and the old hunters until they agree where the herds went', 'W.34 U.33 G.33', None, 0.5, '', {'door': True, 'v': 'tradition, universalism', 'chance': 0.65}),
    ('share out the stored meat by strict rule, with a tally the whole band can see', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, conformity', 'self_control': '+', 'chance': 0.75}),
    ('call the band to the fire, and dare any doubter to say it to your face', 'W.34 B.33 R.33', None, 0.5, '', {'identity': True, 'v': 'power', 'chance': 0.65}),
    ('move camp to cleaner ground by the river, and take the sick to the healer there', 'U.34 R.33 G.33', None, 0.5, '', {'body': 'heavy', 'v': 'tradition, benevolence', 'chance': 0.65}),
    ('go alone to the high rocks for three days, and come back with a vision', 'B.34 R.33 G.33', None, 0.5, '', {'body': 'heavy', 'mark': 'took a wild risk', 'v': 'power, tradition', 'chance': 0.6}),
 ]},
{'name': 'the shaman reads your dream',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.01),
 'drivers': 'community+.2 unrest+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'community, meaning',
 'horizon': 'months',
 'roles': 'elder, partner, friend, rival, parent',
 'requires': 'party member | campaign volunteer | local councillor',
 'tenure': (2.0, 100.0),
 'worlds': {'tribal': 'you tell the shaman a dream of a great fire, and the shaman says it means the band will send '
                      'you to the gathering'},
 'only': 'tribal',
 'timing': {'times': 'per faction member, hearth-walker or voice at the fire in the tribal world, of two years or '
                     'more, a year: about 1 in 100 (estimate)',
            'likelier': 'a band whose speaker has grown old, a shaman close to the family, a dream told at a feast',
            'rarer': 'a band with a strong speaker, a shaman of a rival family, someone who keeps their dreams to '
                     'themselves'},
 'scenes': {'tribal': [('',
                        '{N} tells the shaman a dream of a great fire on the plain, with every clan of the valley '
                        'around it. The shaman listens with closed eyes, then says it plainly: the band will send '
                        '{N} to speak at the gathering.'),
                       ('W',
                        '{N} feels the weight of it at once. To speak for the band at the gathering is a duty to '
                        'every hearth, not an honour to wear.'),
                       ('U',
                        '{N} turns the dream over in the dark. Was the shaman reading the spirits, or the mood of '
                        'the band, or both?'),
                       ('B',
                        'A speaker at the gathering sits with the heads of every clan. {N} begins to count which '
                        "families would stand behind the shaman's words."),
                       ('R',
                        '{N} cannot sleep for the joy of it. The great fire, the plain, the clans: {N} can already '
                        'feel the heat of it.'),
                       ('G',
                        'Dreams come when they come, like rain. {N} thinks of {parent}, who was never sent, and of '
                        'the old way of thanking a shaman with the best of the hunt.')]},
 'outcomes': (['The band takes the dream to heart, and things move the way {N} hoped.',
               'By the new moon the families are talking about {N}, and most of the talk is kind.'],
              ['The elders say a dream is only a dream, and the talk moves on to other hearths.',
               '{rival} hears of the reading and laughs at it by every fire, and the band laughs along.']),
 'options': [
    ("take the shaman's reading to the elders, and ask them to put your name forward", 'W1', None, 0.45, '', {'title': 'parliamentary candidate', 'aims': 'member of parliament', 'v': 'conformity, tradition', 'chance': 0.55}),
    ('ask the shaman for a second sign before believing the first', 'U1', None, 0.45, '', {'v': 'self-direction', 'chance': 0.85}),
    ('go to each family head alone, and say what a speaker could do for them', 'B1', None, 0.45, '', {'title': 'parliamentary candidate', 'aims': 'member of parliament', 'v': 'power, achievement', 'chance': 0.6}),
    ('stand up at the fire that night and tell the band the dream yourself', 'R1', None, 0.45, '', {'title': 'parliamentary candidate', 'aims': 'member of parliament', 'v': 'stimulation, self-direction', 'chance': 0.6}),
    ('bring the shaman the best of your kill, so the reading is told at every hearth', 'G1', None, 0.45, '', {'title': 'parliamentary candidate', 'mark': 'hid a wrong', 'closed': 'approval: a gift for a louder reading; backfire: the elders learn of the gift, and the dream counts for nothing', 'v': 'tradition, power', 'chance': 0.5}),
    ('remind the families that your line has spoken for the band before', 'B.5 G.5', None, 0.5, '', {'grants': 'a following in the party', 'v': 'tradition, power', 'chance': 0.65}),
    ('call in every gift the families owe you, and ask for their voices', 'B.5 R.5', None, 0.5, '', {'grants': 'allies in the party', 'v': 'power', 'chance': 0.65}),
    ('tell the dream as a story at every hearth, and watch who leans in', 'U.5 R.5', None, 0.5, '', {'door': True, 'grants': 'canvassing', 'v': 'stimulation, achievement', 'chance': 0.85}),
    ('ask your partner and kin whether the hearth can spare you for a summer', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'chance': 0.85}),
    ('thank the shaman, and say the band must choose its speaker in the open', 'W.5 U.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'universalism, conformity', 'chance': 0.85}),
 ]},
{'name': 'a feast to win the families',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
 'drivers': 'prosper+.2 harsh-.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'community, money',
 'horizon': 'months',
 'roles': 'rival, partner, elder, friend',
 'once': True,
 'requires': 'council candidate | parliamentary candidate | party leader',
 'worlds': {'tribal': 'the gathering is a moon away, and the families will follow whoever feasts them best'},
 'only': 'tribal',
 'timing': {'times': 'per candidate or faction head in the tribal world: once a candidacy, before the gathering '
                     '(estimate)',
            'likelier': 'a contested choice, a good season with stores to spare, a rival who has already feasted the '
                        'band',
            'rarer': 'a lean year, a choice nobody contests'},
 'scenes': {'tribal': [('',
                        'The gathering is a moon away, and {rival} has already feasted half the band on smoked fish '
                        'and honey. The families are waiting to see what {N} will put by the fire.'),
                       ('W',
                        'Custom is clear: one who asks to speak for the band feeds the band. {N} reckons what is '
                        'fair to every hearth, no more and no less.'),
                       ('U',
                        '{N} counts the stores twice: the dried meat, the furs, the shells. Every basket given now '
                        'is a basket the winter will not have.'),
                       ('B',
                        "A feast is a bargain made in public. {N} wants to know which families' voices count, and "
                        'what each one will cost.'),
                       ('R',
                        '{N} can already hear the drums and smell the meat over the fire. If there is to be a feast, '
                        'it should be one the valley talks about for years.'),
                       ('G',
                        'The feasts of {Ns} grandmother are still remembered: the first meat of the season, the '
                        'elders served first. Some ways are old because they work.')]},
 'outcomes': (['The feast is talked about at every hearth, and the families lean toward {N}.',
               'When the gathering comes, the families remember who fed them, and how.'],
              ['The feast runs thin before the night is half over, and the families drift back to the fire of '
               '{rival}.',
               'The band eats well and says kind things, and then follows whoever it was going to follow anyway.']),
 'options': [
    ('give a fair feast by custom, an equal share for every hearth', 'W1', None, 0.45, '', {'grants': 'good name in town', 'v': 'conformity, tradition', 'chance': 0.75}),
    ('count the stores, keep enough for winter, and feast the band on the rest', 'U1', None, 0.45, '', {'v': 'security, achievement', 'chance': 0.85}),
    ('feast only the families whose voices will count at the fire', 'B1', None, 0.45, '', {'grants': 'allies in the party', 'v': 'power', 'mark': 'made an enemy', 'chance': 0.75}),
    ('give it all: every skin and basket, one great night by the fire', 'R1', None, 0.45, '', {'takes': 'a campaign war chest', 'grants': 'a following in the party', 'v': 'achievement, stimulation', 'self_control': '-', 'chance': 0.7}),
    ('feast the families the old way, with the first meat and the elders served first', 'G1', None, 0.45, '', {'habit': True, 'v': 'tradition', 'chance': 0.7}),
    ('take the young hunters out, and feast the band on what you bring home', 'R.5 G.5', None, 0.5, '', {'body': 'heavy', 'grants': 'a loyal campaign team', 'v': 'stimulation, benevolence', 'chance': 0.7}),
    ('borrow stores from kin, and keep a careful tally of what is owed', 'U.5 B.5', None, 0.5, '', {'binds': True, 'grants': 'a campaign war chest', 'v': 'power, security', 'chance': 0.8}),
    ('refuse the custom: the stores belong to the winter, and the band knows it', 'U.5 G.5', None, 0.5, '', {'identity': True, 'mark': 'turned down a chance', 'v': 'security, universalism', 'chance': 0.55}),
    ('let the families who bring the most stand nearest the fire', 'W.5 B.5', None, 0.5, '', {'grants': 'donors', 'v': 'power', 'chance': 0.75}),
    ('invite the families of your rival as well, and serve them first', 'W.5 R.5', None, 0.5, '', {'grants': 'friends across the aisle', 'door': True, 'v': 'benevolence, universalism', 'chance': 0.55}),
 ]},
{'name': 'the oracle names you',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.01),
 'drivers': 'era+.3 fortune+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'boss, rival, mentor, partner, colleague',
 'requires': 'member of parliament | local councillor | mayor',
 'tenure': (2.0, 100.0),
 'worlds': {'magic': 'the oracle of the high tower speaks your name in front of the whole court'},
 'only': 'magic',
 'timing': {'times': 'per member of the Assembly, town councillor or burgomaster in the magic world, of two years or '
                     'more, a year: about 1 in 100 (estimate)',
            'likelier': 'a court that keeps an oracle, a time of change at the top, a name already spoken in the '
                        'Assembly',
            'rarer': 'a quiet reign, an Order that distrusts prophecy, a name nobody at court knows'},
 'scenes': {'magic': [('',
                       'At the midsummer audience the oracle of the high tower lifts its veiled head and, in a voice '
                       'like wind through a bell, speaks {Ns} name. It says {N} will rise. The whole court turns to '
                       'look.'),
                      ('W',
                       '{N} wants nothing done in a hurry. A prophecy spoken at court belongs to the court and the '
                       'faction to weigh, not to one member with hopes.'),
                      ('U',
                       "{N} knows the oracle's old sayings by heart, and how many came true only in a sideways "
                       'sense. The exact words matter.'),
                      ('B',
                       'By evening three lords who never knew {Ns} name have sent invitations to dine. {N} notes '
                       'every one of them.'),
                      ('R',
                       'The blood rushes to {Ns} face, and {N} has to stop from laughing aloud. Rise to what, and '
                       'when?'),
                      ('G',
                       'Some things are woven before anyone is born. {N} wonders whether this is one of them, or '
                       'only an old voice in a tower.')]},
 'outcomes': (["The court's attention settles where {N} wants it, and the prophecy works in {Ns} favour.",
               'A year on, people still speak of the day the oracle named {N}, and doors open that were shut '
               'before.'],
              ['The prophecy turns sour at court, and the lords who dined with {N} stop sending invitations.',
               "Months pass and nothing rises, and {rival} starts calling {N} the oracle's fool."]),
 'options': [
    ('tell the faction at once, and let its lord decide what to make of it', 'W1', None, 0.45, '', {'v': 'conformity', 'chance': 0.85}),
    ('find out what the oracle asks of those it names, before doing anything else', 'U1', None, 0.45, '', {'v': 'self-direction, security', 'chance': 0.8}),
    ('let the court believe it, and gather the favours that come with it', 'B1', None, 0.45, '', {'grants': 'friend in power', 'door': True, 'habit': True, 'v': 'power', 'mark': 'made a friend', 'chance': 0.75}),
    ('laugh it off before the whole court, and say your fate is your own', 'R1', None, 0.45, '', {'v': 'self-direction', 'chance': 0.9}),
    ('go home to the ward, and let what is meant to come find its way', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.85}),
    ('speak out against any office given by prophecy, your own included', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'turned down a chance', 'grants': 'a name for straight talk', 'v': 'universalism', 'chance': 0.65}),
    ('make the most of the stir, and speak in every hall while the realm listens', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'known across the country', 'v': 'power, achievement', 'chance': 0.12}),
    ('pledge the faction your loyalty, so that the prophecy rises with it', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'allies in the party', 'v': 'security, conformity', 'chance': 0.7}),
    ('take the prophecy to heart, and ask the throne for a seat on its council', 'U.34 R.33 G.33', None, 0.5, '', {'title': 'minister', 'requires': 'member of parliament', 'without': 'impossible', 'aims': 'minister', 'mark': 'took a wild risk', 'takes_if_fails': 'allies in the party', 'v': 'achievement, stimulation', 'chance': 0.25}),
    ('say nothing, and quietly learn who at court now fears you', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'counting the votes', 'v': 'power, security', 'chance': 0.8}),
 ]},
{'name': 'a bargain with something old',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.005, 0.005, 0.005, 0.005),
 'drivers': 'unrest+.2 stress+.2 trouble+.15',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'partner, rival, grandparent, friend',
 'requires': 'parliamentary candidate | member of parliament | party leader',
 'tenure': (1.0, 100.0),
 'worlds': {'magic': 'in the barrow on the night before the lots, a voice offers you the Assembly, and asks for '
                     'something later'},
 'only': 'magic',
 'timing': {'times': 'per candidate, member of the Assembly or faction head in the magic world, of a year or more, a '
                     'year: about 1 in 200; most refuse, and few who accept are found out (estimate)',
            'likelier': 'a close race, a desperate year, old barrows near the city, a house that has bargained '
                        'before',
            'rarer': "a safe seat, the Order's wards near the house, a calm year"},
 'scenes': {'magic': [('',
                       'On the night before the lots {N} walks out past the city wall to think, and from under the '
                       'old barrow a voice says {Ns} name. It offers the seat in the Assembly, sure as sunrise, and '
                       'asks only for something later.'),
                      ('W',
                       'There are laws about such voices, older than the Assembly itself. {N} knows exactly what the '
                       'Order says about bargains under the hill.'),
                      ('U',
                       '{N} listens to every word with great care. Things under hills are bound by what they say, '
                       'and so is anyone who answers.'),
                      ('B',
                       'Tomorrow the lots may go either way. Here is a certainty, and {N} has never turned down a '
                       'certainty without hearing the price.'),
                      ('R',
                       'The hair stands up on {Ns} arms. Part of {N} wants to run, and part wants to shout yes into '
                       'the dark just to see what happens.'),
                      ('G',
                       'The barrow was old when the city was a ring of huts. {N} remembers the stories {grandparent} '
                       'told about people who made deals with what sleeps there.')]},
 'outcomes': (['By the time the urns are opened, {N} is sure the choice was right, whatever comes later.',
               'The lots fall the way {N} hoped, and the city wakes as if nothing happened in the night.'],
              ['The lots go against {N}, and the barrow is silent when {N} goes back.',
               'Word of the night under the hill reaches the Order, and {N} is called to explain.']),
 'options': [
    ('tell the Order what lies under the hill, and let its wardens deal with it', 'W1', None, 0.45, '', {'mark': 'turned down a chance', 'v': 'conformity, security', 'chance': 0.85}),
    ('answer with a promise worded so cleverly that it can never come due', 'U1', None, 0.45, '', {'title': 'member of parliament', 'mark': 'took a wild risk', 'v': 'self-direction, achievement', 'chance': 0.35}),
    ('make it name the full price first, and promise nothing yet', 'B1', None, 0.45, '', {'v': 'power', 'chance': 0.75}),
    ('accept: the seat tomorrow, and whatever it asks later', 'R1', None, 0.45, '', {'title': 'member of parliament', 'aims': 'member of parliament', 'binds': True, 'mark': 'took a wild risk', 'closed': 'law: a pact with an old power, forbidden by the Order; backfire: the Order finds the mark of it, and the seat is stripped', 'v': 'stimulation, achievement', 'chance': 0.7}),
    ("leave bread and salt at the barrow's door, and go home without an answer", 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.8}),
    ('bind it by oath on its old name: the seat, at a price you set', 'W.34 U.33 G.33', None, 0.5, '', {'title': 'member of parliament', 'binds': True, 'mark': 'took a wild risk', 'closed': "law: a pact with an old power, forbidden by the Order; backfire: the Order's court, and the seat lost", 'v': 'security, tradition', 'chance': 0.45}),
    ('refuse, and win the lots the long way, with every pledge counted twice', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'counting the votes', 'v': 'achievement, conformity', 'self_control': '+', 'chance': 0.7}),
    ('go home, tell your partner everything, and decide together by morning', 'W.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence', 'chance': 0.85}),
    ('ask for the seat and a following in the faction, and haggle hard over the price', 'U.34 B.33 R.33', None, 0.5, '', {'title': 'member of parliament', 'grants': 'a following in the party', 'binds': True, 'mark': 'took a wild risk', 'closed': 'law: a pact with an old power, forbidden by the Order; backfire: the Order finds the mark of it, and the seat and the following are lost', 'v': 'power', 'chance': 0.7}),
    ('refuse, and fight for every lot with your own people and your own strength', 'B.34 R.33 G.33', None, 0.5, '', {'grants': 'a loyal campaign team', 'identity': True, 'v': 'achievement, self-direction', 'self_control': '+', 'chance': 0.7}),
 ]},
{'name': 'a binding oath of office',
 'stages': 'young_adult adult mature elder',
 'age': (21, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
 'drivers': 'era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'mentor, boss, partner, rival, colleague',
 'once': True,
 'requires': 'minister | mayor | head of government',
 'tenure': (0.0, 1.0),
 'worlds': {'magic': "the Order's mages bring the old oath of office, and the words burn as you read them"},
 'only': 'magic',
 'timing': {'times': 'per councillor of the Crown, burgomaster or Chancellor in the magic world: once, on taking the '
                     'office, where an Order keeps the old oath (estimate)',
            'likelier': 'an old city, an office the Orders founded, a realm that remembers an oath-breaker',
            'rarer': 'a new town without an Order, a lesser office the Crown fills by letter'},
 'scenes': {'magic': [('',
                       'Three mages of the Order carry in the old oath of office, cut in a slab of dark stone. As '
                       '{N} reads it aloud the words glow, and {N} feels each one settle on {Ns} shoulders like a '
                       'hand.'),
                      ('W',
                       'An oath is what makes an office more than a chair. {N} has waited years to say these words '
                       'and means every one of them.'),
                      ('U',
                       '{N} reads ahead while speaking. The fourth clause is broader than anyone said, and nobody '
                       'seems to have read the sixth in a hundred years.'),
                      ('B',
                       'The oath binds whoever swears it. {N} wonders who else in the hall has sworn it, and how '
                       'carefully.'),
                      ('R',
                       'The words burn on the tongue. {N} has never liked promises that cannot be taken back, and '
                       'these cannot.'),
                      ('G',
                       'The first holders of the office swore these same words by the old well, before the city had '
                       'walls. {N} feels the weight of all of them.')]},
 'outcomes': (['The oath settles, and {N} takes up the office with a clear sense of what it holds.',
               'Months later {N} feels the oath only as a quiet weight, the way an old ring feels on a finger.'],
              ["The hall murmurs, and the Order's mages exchange a long look that {N} does not like.",
               'The words sit badly from the first day, and {N} wakes more than once with them burning in {Ns} '
               'mouth.']),
 'options': [
    ('swear the oath plainly, every word, before the whole hall', 'W1', None, 0.45, '', {'binds': True, 'v': 'conformity, tradition', 'chance': 0.95}),
    ('read every clause three times, and ask the mages what each one binds', 'U1', None, 0.45, '', {'grants': 'knowing the rules of the house', 'identity': True, 'habit': True, 'v': 'self-direction, security', 'chance': 0.9}),
    ('swear it with a reservation held silent in your mind', 'B1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "approval: an oath of office sworn in bad faith; backfire: the oath bites, and its mark shows on the oath-taker's hands for all to see", 'v': 'power, self-direction', 'self_control': '-', 'chance': 0.85}),
    ('refuse to swear, and give up the offices that need the oath', 'R1', None, 0.45, '', {'drops': 'minister; mayor; head of government', 'identity': True, 'mark': 'turned down a chance', 'v': 'self-direction', 'chance': 0.9}),
    ('ask to swear it by the old well, as the first holders did', 'G1', None, 0.45, '', {'binds': True, 'v': 'tradition', 'chance': 0.7}),
    ('swear, and use the oath as a shield against every favour asked of you', 'B.5 G.5', None, 0.5, '', {'v': 'tradition', 'self_control': '+', 'chance': 0.85}),
    ('demand the old words be changed first, or swear no oath at all', 'B.5 R.5', None, 0.5, '', {'v': 'power, self-direction', 'chance': 0.5}),
    ("ask the eldest mage for the oath's oldest wording, and swear that instead", 'U.5 G.5', None, 0.5, '', {'door': True, 'binds': True, 'v': 'tradition, universalism', 'chance': 0.55}),
    ('swear, and tell the hall plainly which clause you will never turn on the people', 'W.5 R.5', None, 0.5, '', {'grants': 'a name for straight talk', 'binds': True, 'v': 'benevolence, universalism', 'chance': 0.85}),
    ('petition the Order through the proper channel for a gentler wording', 'W.5 U.5', None, 0.5, '', {'grants': 'drafting policy', 'v': 'conformity, universalism', 'chance': 0.35}),
 ]},
{'name': "a rival's curse",
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.01),
 'drivers': 'unrest+.3 trouble+.15',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, health',
 'horizon': 'months',
 'roles': 'rival, partner, colleague, friend',
 'requires': 'member of parliament | minister | mayor | party leader',
 'worlds': {'magic': 'your voice fails in the chamber three days running, and a hex-mark is found under your door'},
 'only': 'magic',
 'timing': {'times': 'per office-holder in the magic world a year: about 1 in 100 (estimate)',
            'likelier': 'a bitter rivalry, a close vote coming, hedge-witches for hire in the city, wards on the '
                        'house that have lapsed',
            'rarer': "the Order's wards on the house, an office-holder with few enemies"},
 'scenes': {'magic': [('',
                       'For three days running {Ns} voice dies the moment {N} rises to speak in the chamber. On the '
                       'fourth morning a servant finds a hex-mark scratched under the door of the house, and '
                       'everyone knows who has wanted {Ns} seat.'),
                      ('W',
                       'There is a court for exactly this. Laying a curse on an office-holder of the realm is a '
                       'crime, and crimes have names and punishments.'),
                      ('U',
                       '{N} copies the hex-mark carefully onto paper. Every hand that draws such marks has its '
                       'habits, and habits can be traced.'),
                      ('B',
                       '{N} knows what the curse is for: to make {N} look weak before the vote. The question is how '
                       'to make it cost {rival} more than it costs {N}.'),
                      ('R',
                       '{N} is furious, and hoarse, and more determined than ever to stand up in that chamber every '
                       'single day.'),
                      ('G',
                       '{N} thinks of the old healer beyond the walls, who knows the herbs for fevers and the salts '
                       'for hexes, and of home, where nobody has to speak at all.')]},
 'outcomes': (['Within a month {Ns} voice is back, and the matter is settled the way {N} chose.',
               'The story of the hex goes round the city, and most of the sympathy goes to {N}.'],
              ['The hex holds through the vote, and {N} sits silent while the bill passes.',
               'The matter drags on for months, and {rival} smiles every time {N} rises to speak.']),
 'options': [
    ("take the hex-mark to the Order's court, and name the rival though you lack proof", 'W1', None, 0.45, '', {'mark': 'made an enemy', 'closed': 'approval: an accusation without proof; backfire: the court clears the rival, and the accuser pays the costs', 'v': 'conformity, security', 'chance': 0.5}),
    ('trace the hex-mark to whoever drew it, and take the proof to the Order', 'U1', None, 0.45, '', {'v': 'self-direction, security', 'chance': 0.65}),
    ('pay a hedge-witch to turn the curse back on the rival', 'B1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "law: buying a curse against an office-holder; backfire: the Order's court, and the office in danger", 'v': 'power', 'chance': 0.65}),
    ('rise in the chamber every day anyway, cracked voice and all', 'R1', None, 0.45, '', {'habit': True, 'v': 'self-direction, stimulation', 'self_control': '+', 'chance': 0.7}),
    ('go to the old healer beyond the walls for a counter-charm of herbs and salt', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.65}),
    ('go home to your district, and tell your own people the story yourself', 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'benevolence, tradition', 'chance': 0.7}),
    ('let it be known the hex has failed, and watch who in the faction flinches', 'U.5 B.5', None, 0.5, '', {'v': 'power, security', 'chance': 0.7}),
    ('have a friend read out your speech mocking the hex, and dare the rival again', 'U.5 R.5', None, 0.5, '', {'grants': 'rousing a crowd', 'v': 'stimulation, self-direction', 'chance': 0.65}),
    ('ask the faction to ward your house and lend you a stand-in for the votes', 'W.5 B.5', None, 0.5, '', {'v': 'power', 'chance': 0.8}),
    ('give up your offices with dignity, and wait out the hex at home', 'W.5 G.5', None, 0.5, '', {'drops': 'member of parliament; mayor', 'mark': 'gave in to pressure', 'v': 'security, tradition', 'self_control': '-', 'chance': 0.9}),
 ]},
]

ECHOES = [
{'name': 'the fight that made you want to stand',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.005,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'community, public life',
 'horizon': 'months',
 'roles': 'friend, neighbour, rival, colleague',
 'once': True,
 'worlds': {'earth': 'the fight you lost or won still makes you angry, and the next election is close',
            'tribal': 'the quarrel at the fire is over, but you keep thinking you could have spoken for the band '
                      'yourself',
            'magic': "the guild's ruling still stings, and the town council will sit again in spring"},
 'timing': {'times': 'per person who met a local fight, a protest, an injustice or a bitter election in the last '
                     'three years: about 1 in 10 feel the pull to stand in the years after; many councillors say a '
                     'local fight first brought them in (estimate)'},
 'after': "moment 'your town faces a change you could fight', 'a protest to save the local hospital', 'a sense of "
          "injustice', 'a bitter election' or 'they ask you to lead because you stood up once' within the last three "
          'years, and no elected office held (no [local councillor], [mayor] or [member of parliament])',
 'delay_years': (0, 3),
 'likelier': 'an election within the year; the fight was settled by a council vote; friends or family in a party, a '
             'union or a cause; time to spare',
 'rarer': 'stress above 1.5; heavy care duties; a move away from the place of the fight; a settlement everyone could '
          'live with',
 'scenes': {'earth': [('',
                       'Months after the fight, {N} still finds the arguments running on the way to work. Now the '
                       'posters are going up for the next council election, and the same names are on them.'),
                      ('W',
                       'The decision was made by people who never read the objections, under rules nobody local had '
                       'a say in. {N} keeps thinking that rules are only as good as the people at the table.'),
                      ('U',
                       '{N} has worked out exactly where the fight was decided: one committee, three votes, a report '
                       'nobody challenged. Next time, someone who has read the papers should be in that room.'),
                      ('B',
                       'The people who decided were not cleverer or better; they simply had the seats. {N} has '
                       'started to wonder why {N} has never had one.'),
                      ('R',
                       'It still makes {Ns} blood boil. Every time {N} passes the place, the old anger comes back, '
                       'and with it a voice that says: then do something.'),
                      ('G',
                       'The fight was about a place {N} loves and the people who live there. Whether caring for it '
                       'needs a seat on the council is the question {N} keeps turning over.')],
            'tribal': [('',
                        'The quarrel at the council fire ended a moon ago, and the band went the way the loudest '
                        'voices wanted. {N} keeps thinking of the words that could have been said, and of who should '
                        'have said them.')],
            'magic': [('',
                       "The guild's ruling went against the ward, sealed and nailed to the hall door. The town "
                       "council sits again in spring, and its seats are open to anyone with a faction's seal or "
                       'enough names.')]},
 'outcomes': (['{N} steps forward, and people from the fight turn up to help without being asked.',
               'Whatever comes of it, {N} feels the old anger turn into something with a shape.'],
              ['The election comes and goes, and {N} does nothing but complain about the result.',
               'The old allies have scattered, and nobody wants to go through it all again.']),
 'options': [
    ('stand for the council in May, to change the rules from the inside', 'W1', None, 0.45, '', {'identity': True, 'v': 'universalism, conformity', 'title': 'council candidate', 'world': {'tribal': "ask to be heard at the council fire this winter, to change the band's custom from within", 'magic': 'stand for the town council in spring, to change the rules from inside the hall'}, 'chance': 0.7}),
    ('read how the decision was made, and join the party whose plans would have stopped it', 'U1', None, 0.45, '', {'v': 'self-direction, universalism', 'title': 'party member', 'world': {'tribal': 'hear how the elders decided, and bind yourself to the faction that argued your side', 'magic': "study the guild's ruling, and swear to the faction that argued against it"}, 'chance': 0.92}),
    ('join the party that runs the council, and get to know who decides', 'B1', None, 0.45, '', {'habit': True, 'v': 'power', 'title': 'party member', 'world': {'tribal': 'bind yourself to the strongest faction at the fire, and sit near its elders', 'magic': 'swear to the faction that holds the council, and learn whose word counts'}, 'chance': 0.8}),
    ('stand, and turn the people from the fight into a campaign team', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'title': 'council candidate', 'grants': 'a movement behind you', 'world': {'tribal': 'ask to be heard at the fire, with the young hunters from the quarrel walking the hearths at your side', 'magic': 'stand for the council, with the brotherhood from the fight carrying your banner'}, 'chance': 0.65}),
    ('let it rest: the fight was for the place, never for a seat', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition', 'mark': 'turned down a chance', 'world': {'tribal': 'let it rest: you spoke for your hearth, not to be heard at the fire', 'magic': 'let it rest: the fight was for the lane, never for a seat'}, 'chance': 0.75}),
    ('join the party of the neighbour who led the fight, and give it your evenings', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, conformity', 'title': 'party member', 'world': {'tribal': 'bind yourself to the faction of the one who led the quarrel at the fire, and walk the hearths for it', 'magic': 'swear to the faction of the neighbour who led the fight against the guild, and carry its banner'}, 'chance': 0.75}),
    ('write down what the fight taught, for the next street that has to face it', 'U1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'teach the young ones what the quarrel taught, so the next one goes better', 'magic': 'write a plain account of the fight for the next ward that faces the guild'}, 'chance': 0.85}),
    ('find out who picks the candidates, and make a point of being useful to them', 'B1', 'W.7', 0.5, '', {'door': True, 'v': 'power', 'aims': 'council candidate', 'world': {'tribal': 'find out which elders bless a voice at the fire, and make a point of being useful to them', 'magic': "learn who hands out the faction's seals, and make a point of being useful to them"}, 'chance': 0.65}),
    ('join the party that fought hardest, and argue its case online every night', 'R1', 'U.7', 0.5, '', {'v': 'stimulation', 'title': 'party member', 'self_control': '-', 'world': {'tribal': 'bind yourself to the faction that fought hardest, and argue its case with anyone at the fire every night', 'magic': 'swear to the faction that fought the guild hardest, and argue its case in the taverns every night'}, 'chance': 0.75}),
    ("take a seat on the residents' committee first, where the street already knows your name", 'G1', 'B.7', 0.5, '', {'binds': True, 'v': 'power, tradition', 'title': "residents' committee member", 'world': {'tribal': 'become an elder of your own hearths first, where every family knows your name', 'magic': 'become warden of your own street first, where every door knows your face'}, 'chance': 0.6}),
 ]},
{'name': 'the debate you never forgot',
 'stages': 'young_adult adult mature elder',
 'age': (19, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.04,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'public life, meaning',
 'horizon': 'months',
 'roles': 'rival, mentor, friend, partner',
 'once': True,
 'worlds': {'earth': 'a television debate reminds you of the school debate you won, or lost, years ago',
            'tribal': 'an argument at the fire stirs the memory of the first time you stood up to speak as a child',
            'magic': "a disputation in the market square takes you back to the academy's debating hall"},
 'timing': {'times': 'per person who debated at school as a teenager, or defended a speaker they could not stand as '
                     'a young campaigner: about 1 in 20 come back to it as adults, eight to thirty years later '
                     '(estimate)'},
 'after': "moment 'a debate or contest at school' as a teenager, or 'defending a speaker you cannot stand' as a "
          'young campaigner, and now an adult with time to spare (time above 0.4: fewer hours at work, children '
          'grown, retired)',
 'delay_years': (8, 30),
 'likelier': 'the old debate was won, or lost narrowly; an election on the way; children grown or fewer working '
             'hours; a friend or partner in politics',
 'rarer': 'stress above 1.5; long working hours; heavy care duties; a long distaste for politics',
 'scenes': {'earth': [('',
                       'On a weeknight {N} half-watches a televised debate, and one candidate fumbles a question {N} '
                       'would have answered without notes years ago. Suddenly it all comes back: the hall, the '
                       'lectern, the timer, {rival} on the other side.'),
                      ('W',
                       'The debate on the screen has no rules worth the name: interruptions, dodged questions, a '
                       'moderator who gives up. {N} remembers a contest where the time limits were kept to the '
                       'second, and misses it.'),
                      ('U',
                       '{N} spots the hole in the first answer before the opponent does, and is surprised how much '
                       'of the old pleasure is still there.'),
                      ('B',
                       'The people on the screen are paid, quoted and listened to for doing what {N} once did for a '
                       'cup. The thought does not go away.'),
                      ('R',
                       '{N} is talking back to the television by the second question, and on {Ns} feet by the fifth. '
                       'The old thrill of standing up to argue is right there.'),
                      ('G',
                       '{mentor}, who coached the team all those years ago, always said {N} spoke best about home. '
                       '{N} wonders whether that is still true.')],
            'tribal': [('',
                        'Two hunters argue at the fire about where to winter, and neither says it well. {N} '
                        'remembers standing up at this same fire as a child, for the first time, with every face '
                        'turned and both knees shaking.')],
            'magic': [('',
                       'A disputation in the market square draws a crowd, two scholars trading points over a new '
                       "decree. {N} is taken straight back to the academy's debating hall, and the night {N} won, or "
                       'lost, before the masters.')]},
 'outcomes': (['{N} finds the old voice is still there, and someone in the room notices.',
               'Within a few months {N} is arguing about something that matters, with people who listen.'],
              ['The first evening out goes badly, and {N} decides the past is better left where it was.',
               'Work and home fill the evenings again, and the old debate goes back to being a story.']),
 'options': [
    ('stand for the council, where the arguing ends in a vote that counts', 'W1', None, 0.45, '', {'v': 'universalism, achievement', 'title': 'council candidate', 'world': {'tribal': 'ask to be heard at the council fire, where the arguing ends in a choice', 'magic': 'stand for the town council, where disputation ends in a vote'}, 'chance': 0.7}),
    ("volunteer in a member's office, research and drafting a few evenings a week", 'U1', None, 0.45, '', {'habit': True, 'v': 'achievement, self-direction', 'title': 'campaign volunteer', 'aims': 'political adviser', 'world': {'tribal': "offer to sit behind the band's speaker, and help shape what he says", 'magic': "offer your pen to a councillor's secretary, a few evenings a week"}, 'chance': 0.35}),
    ('look up your old school rival, now a councillor, and ask what it takes', 'B1', None, 0.45, '', {'v': 'power, achievement', 'aims': 'council candidate', 'world': {'tribal': 'seek out your rival from childhood, now a voice at the fire, and ask how it is done', 'magic': 'call on your old academy rival, now on the council, and ask what it takes'}, 'chance': 0.8}),
    ('join an evening debating club, and argue every week for the joy of it', 'R1', None, 0.45, '', {'habit': True, 'v': 'stimulation, hedonism', 'grants': 'debating', 'self_control': '+', 'world': {'tribal': 'join the old talkers who argue at the fire every night, for the joy of it', 'magic': 'join a disputation society in the lower town, and argue every week'}, 'chance': 0.8}),
    ('let it rest: that debate belongs to the person you were back then', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': "let it rest: that was a child's moment at the fire", 'magic': "let it rest: the academy's hall belongs to the student you were"}, 'chance': 0.8}),
    ("coach the local school's debating team one evening a week", 'W1', 'G.7', 0.5, '', {'habit': True, 'v': 'benevolence, tradition', 'world': {'tribal': "teach the band's children to stand up and speak at the fire", 'magic': "tutor the academy's young disputants one evening a week"}, 'chance': 0.7}),
    ('read both sides of the debate, and write a fair letter to the local paper', 'U1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'world': {'tribal': 'speak at the fire for both sides fairly, and let the band weigh them', 'magic': 'write a fair letter to the broadsheet on both sides of the decree'}, 'chance': 0.7}),
    ('join a party, and learn its policy papers until you are its speaker at meetings', 'B1', 'U.7', 0.5, '', {'identity': True, 'v': 'achievement, power', 'mark': 'learned a skill', 'title': 'party member', 'self_control': '+', 'world': {'tribal': 'bind yourself to a faction, and learn its quarrels until you are its voice at the fire', 'magic': 'swear to a faction, and learn its positions until you are the one it puts up to speak'}, 'chance': 0.75}),
    ('knock on doors for the candidate who argues the way you used to', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, achievement', 'title': 'campaign volunteer', 'world': {'tribal': 'walk the hearths for the speaker who argues the way you once did', 'magic': 'carry the banner of the candidate who argues the way you once did'}, 'chance': 0.85}),
    ('join the party your family has always voted for, and argue its case over Sunday dinner', 'G1', 'R.7', 0.5, '', {'v': 'tradition, hedonism', 'title': 'party member', 'world': {'tribal': 'bind yourself to the faction your family has stood with for generations, and argue its case at the family hearth', 'magic': 'swear to the faction your family has always backed, and argue its case over the feast-day table'}, 'chance': 0.7}),
 ]},
{'name': 'the race comes round again',
 'stages': 'young_adult adult mature elder',
 'age': (24, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.15,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'friend, partner, rival, colleague',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, the same race comes round again, and people still '
                     'remember your name',
            'tribal': 'summers after the band chose another, the same choosing comes round again, and some hearths '
                      'still say your name',
            'magic': 'years after the lots went against you, the same seat, chain or seal is up for the casting '
                     'again'},
 'timing': {'times': "per person who went for a seat, a mayoralty, a party's lead or the government on long odds and "
                     'lost: about 1 in 5 tries again at a later contest (estimate); the second run starts with a '
                     'name people remember and a team that knows how, and a candidate who stands again usually does '
                     'better than the first time (estimate); here the second try is written at 12 in 100, above '
                     'every first try (2 to 10) and below the fair races (30 to 50)'},
 'after': "moment 'election night', 'polling day for mayor', 'a challenge from the back benches', 'the campaign "
          "nobody gave a chance' or 'the leadership falls vacant' within the last month, a long shot taken there and "
          'missed ([a long shot that missed] held, and a failed long shot that month); when it comes, no other long '
          'shot missed since, and a leadership or the government only while the person still holds the rung below it',
 'delay_years': (3, 12),
 'likelier': 'the holder of the post standing down, every party in disgrace, the old campaign team still in touch, a '
             'name still known, time and a little money to spare',
 'rarer': 'stress above 1.5; little money; a move away since the first race',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, the same race comes round again: the seat falls '
                       'vacant, the mayor stands down, the leader stumbles, or the country goes back to the polls. '
                       'On the first evening three people ring, one of them {friend}, who still has the old list of '
                       'supporters in a drawer.'),
                      ('W',
                       '{N} reads the rules again. Nothing has changed: the same forms, the same deadlines, the same '
                       'right as anyone. What has changed is that {N} knows how it is done.'),
                      ('U',
                       '{N} still has the old results, and the new ones beside them. The gap is smaller than it was, '
                       'and {N} can see exactly where the votes would come from.'),
                      ('B',
                       'Last time {N} went in with too little. This time there are people who owe {N} favours, and a '
                       'name the papers already know.'),
                      ('R',
                       'The old fire is still there. {N} told {partner} it was a one-off, and both of them knew it '
                       'was not.'),
                      ('G',
                       'The people who backed {N} last time never forgot. At the shop and at the school gate they '
                       'keep asking when {N} will try again.')],
            'tribal': [('',
                        'Summers after the band chose another, the same choosing comes round again, and the one '
                        'chosen then is too stiff to make the walk. At some hearths they still say {Ns} name.')],
            'magic': [('',
                       'Years after the lots went against {N}, the same seat, chain or seal is up for the casting '
                       'again. The hedge-witch in the lower town says she remembers {N}, and that charms are cheaper '
                       'the second time.')]},
 'outcomes': (['{N} sees it through this time with open eyes, and whatever the count says, everyone knows exactly '
               'who {N} is.',
               'The second time feels different: steadier, and stranger, and in the end worth it.'],
              ['One place higher this time, and a good deal closer. {N} laughs on the stage at the count, and is not '
               'sure why.',
               'It does not come off again. {N} walks home the long way, past the hall where the count was, and '
               'finds it does not hurt the way it did.']),
 'options': [
    ('try again, by the same rules, with everything learned the first time', 'W1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': 'ask again by the old custom, knowing now how it is done', 'magic': 'enter your name for the casting again, by every form, knowing now how it is done'}, 'chance': 0.12}),
    ('try again on the numbers, only where the gap can close', 'U1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'ask again, and spend every day at the hearths that came closest last time', 'magic': 'try again, and spend every coin where the gap can close'}, 'chance': 0.12}),
    ('try again, and call in every favour gathered since the first time', 'B1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'ask again, and call in every gift given since the first summer', 'magic': 'try again, and call in every favour owed since the first lots'}, 'chance': 0.12}),
    ('try again, louder, and enjoy every minute of it this time', 'R1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, hedonism', 'world': {'tribal': 'ask again, louder at every fire, and enjoy every night of it', 'magic': 'try again, louder in every square, with the cheaper charm this time'}, 'chance': 0.12}),
    ('try again for the people who asked, with the old team at the door', 'G1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, benevolence', 'world': {'tribal': 'ask again for the hearths that asked, with the old friends walking beside you', 'magic': 'try again for the lanes that asked, with the old team at every door'}, 'chance': 0.12}),
    ('write a plain account of the first try, for whoever comes next', 'W1', 'U.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': 'teach the young at the fire how the first asking went, for whoever asks next', 'magic': 'write a plain account of the first casting, for whoever tries next'}, 'chance': 0.8}),
    ("be a younger candidate's agent, and run their numbers like a machine", 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'stand behind a younger one who asks the band, and count every family for them', 'magic': "be a younger candidate's agent, and tally their lanes like a guild clerk"}, 'chance': 0.8}),
    ('back a younger rival this time, for a place in their team', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': 'stand behind a younger rival this time, for a place at their side', 'magic': 'back a younger rival this time, for a seat at their table'}, 'chance': 0.8}),
    ('throw a party for the old campaign team, and let the race go', 'R1', 'G.7', 0.5, '', {'grants': 'a loyal campaign team', 'v': 'hedonism, benevolence', 'world': {'tribal': 'hold a feast for the friends who walked the hearths, and let the choosing go', 'magic': 'throw a feast for the old team at the tavern, and let the casting go'}, 'chance': 0.8}),
    ("let it go, and give what it would cost to the town's food bank", 'G1', 'W.7', 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'let it go, and give the stores you would have spent to the hungriest hearths', 'magic': 'let it go, and give the fee to the almshouse of the lower town'}, 'chance': 0.8}),
 ]},
{'name': 'making peace with the long shot',
 'stages': 'young_adult adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.3,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'meaning, community',
 'horizon': 'months',
 'roles': 'friend, partner, child, colleague, mentor',
 'once': True,
 'worlds': {'earth': 'years later the old leaflet, or the letter, turns up in a drawer, and a young neighbour is '
                     'thinking of standing',
            'tribal': 'a child at the fire asks about the summer you asked the band for more than it would give',
            'magic': 'an apprentice at the guild hall finds your old broadsheet in a drawer and asks what happened'},
 'timing': {'times': 'per person who went for a long shot in politics and missed: about 2 in 5 come back to it years '
                     'later in a settled way, telling it, teaching it, cheering someone younger on or letting it '
                     'rest (estimate)'},
 'after': "moment 'election night', 'a seat falls vacant', 'the leadership falls vacant', 'polling day for mayor', "
          "'a challenge from the back benches', 'the campaign nobody gave a chance' or 'writing in cold for a job in "
          "politics' within the last month, a long shot taken there and missed ([a long shot that missed] held, and "
          'a failed long shot that month)',
 'delay_years': (2, 15),
 'likelier': 'age; a quiet year; children grown or retired; a young person nearby with the same itch; friends from '
             'the attempt still around',
 'rarer': 'stress above 1.5; poor health; a fresh grievance about the old race',
 'scenes': {'earth': [('',
                       'Years later, sorting a drawer, {N} finds the papers from the attempt: a leaflet with a '
                       'younger face on it, a letter, a speech nobody heard. That evening a young neighbour mentions '
                       'over the fence that they are thinking of standing for something.'),
                      ('W',
                       '{N} did it properly, by the rules, and lost by them. There is a quiet pride in that, which '
                       'took years to notice.'),
                      ('U',
                       '{N} can say now exactly why it failed, and what it would have taken. The account is cooler '
                       'than it was, and more useful.'),
                      ('B',
                       'It cost money, time and a few friends. {N} has done the sum many times, and lately it comes '
                       'out closer to even.'),
                      ('R',
                       '{N} would do it again. That is the surprising part: not the losing, but how much {N} still '
                       'loved the trying.'),
                      ('G',
                       'The neighbours who walked the streets with {N} still say hello in a particular way. Whatever '
                       'was lost, that was kept.')],
            'tribal': [('',
                        'At the fire a child asks about the summer {N} asked the band for more than it would give. '
                        'The old ones smile; they remember it better than {N} thought.')],
            'magic': [('',
                       'An apprentice at the guild hall finds {Ns} old broadsheet in a drawer, the ink faded and the '
                       'promises still there, and brings it over to ask what happened.')]},
 'outcomes': (['{N} finds the old attempt has become a story worth telling, and the telling does someone else some '
               'good.',
               'Something settles. The long shot is part of {Ns} life now, neither a wound nor a boast.'],
              ['The old disappointment comes back sharper than expected, and {N} puts the papers away again for '
               'another year.',
               'Nobody seems to want the story just now, and {N} keeps it for later.']),
 'options': [
    ("write it down plainly, as it happened, for the town's archive", 'W1', None, 0.45, '', {'v': 'tradition, conformity', 'world': {'tribal': 'tell it plainly at the fire, as it happened, so the band keeps it', 'magic': "write it down plainly for the guild hall's chronicle"}, 'chance': 0.85}),
    ('teach an evening course on how politics really works, the losses included', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'teach the young at the fire how the band really chooses, the losses included', 'magic': 'give the academy a winter of lectures on how the Assembly really works, the losses included'}, 'chance': 0.85}),
    ('tell the story at dinners, and let it open the doors it can', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'tell the story at every feast, and let it win the friends it can', 'magic': 'tell the story at every guild dinner, and let it open the doors it can'}, 'chance': 0.85}),
    ('help a young neighbour stand, and cheer loudest at their count', 'R1', None, 0.45, '', {'mark': 'helped someone in need', 'v': 'stimulation, benevolence', 'world': {'tribal': 'stand behind a young one who asks to be heard, and shout loudest when the families choose', 'magic': 'help a young neighbour stand for the lots, and cheer loudest at the urns'}, 'chance': 0.85}),
    ('let it rest, and keep the old papers in a drawer where they belong', 'G1', None, 0.45, '', {'v': 'tradition', 'world': {'tribal': 'let it rest, and keep the memory where it belongs', 'magic': 'let it rest, and keep the old broadsheet in the chest where it belongs'}, 'chance': 0.85}),
    ('join the board that oversees local elections, so newcomers get a fair start', 'W1', 'B.7', 0.5, '', {'v': 'conformity, universalism', 'world': {'tribal': 'sit with the keepers of the counting stones, so newcomers get a fair hearing', 'magic': "sit with the Order's witnesses at the urns, so newcomers get a fair start"}, 'chance': 0.8}),
    ('write the whole story as a book, and let it sting where it should', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'make the whole story into a long tale for the singers, stings and all', 'magic': 'write the whole story as a chapbook, and let it sting where it should'}, 'chance': 0.8}),
    ('set up a small fund for first-time candidates from the old streets', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'lay by stores each autumn for the young ones from the far hearths who ask to be heard', 'magic': 'endow a small purse for first-time candidates from the old lanes'}, 'chance': 0.8}),
    ('coach the school debating team, and teach them how to lose well', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': "teach the band's children to speak at the fire, and how to lose well", 'magic': "coach the academy's young disputants, and teach them how to lose well"}, 'chance': 0.8}),
    ('meet the old team each year on the anniversary, and work out what it taught', 'G1', 'U.7', 0.5, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'sit with the old friends each year at the same moon, and work out what it taught', 'magic': 'meet the old team each year at the same tavern, and work out what it taught'}, 'chance': 0.8}),
 ]},
]

EVENTS_READ = [{'name': 'the count goes against you',
  'source': 'community',
  'tone': 'mixed',
  'base': 'need:belonging-.04',
  'worlds': {'earth': 'the returning officer reads out the numbers, and your name is not at the top',
             'tribal': 'the band stands behind another, and you are left by the fire',
             'magic': 'the urns are opened, and the lots favour your rival'},
  'timing': {'times': 'per candidate who loses: once a defeat; most candidates lose (4,515 candidates for 650 seats '
                      'in 2024, House of Commons), about 2 council candidates in 3 and 6 parliamentary candidates in '
                      '7 (estimate)',
             'likelier': 'a crowded field, a seat the other side has held for decades, a bad year for the party',
             'rarer': "a safe seat for the candidate's own side, an uncontested ward",
             'window': (18, 95),
             'gap_years': (1.0, 4.0)},
  'readings': [('a duty done: the voters decided, and that is the whole point',
                'W1',
                1.0,
                'meaning+.05',
                'W',
                "{N} shakes the winner's hand, thanks the counting staff, and goes home at peace."),
               ('a lesson: the numbers show where it went wrong, street by street',
                'U1',
                0.9,
                'competence+.05',
                'U',
                '{N} asks for the box-by-box figures and spends the weekend marking them on a map.'),
               ('a waste: years and money thrown at people who did not want it',
                'B1',
                0.6,
                'autonomy+.05',
                'B',
                '{N} adds up what the campaign cost, and decides the next fight will be chosen with more care.'),
               ('a heartbreak: it mattered so much, and the place said no',
                'R1',
                0.6,
                'belonging+.05',
                'R',
                '{N} cries in the car park, then goes out with the volunteers and stays until they close the doors.'),
               ('the way things are: this place has always voted that way',
                'G1',
                0.9,
                'safety+.05',
                'G',
                '{N} goes home, makes tea, and is back in the garden by the morning.')],
  'scenes': {'earth': [('',
                        'The returning officer reads out the numbers in alphabetical order, and when {Ns} name comes '
                        "it is not followed by the highest figure. Across the hall, {rival}'s supporters are already "
                        'cheering.')],
             'tribal': [('',
                         'The families walk to stand behind the speakers they choose, and the line behind {rival} '
                         'grows longer and longer. When the elders call an end, {N} is left by the fire with a '
                         'handful of friends.')],
             'magic': [('',
                        "The Order's mage reads the lots from the last urn, and the herald cries {rival}'s name "
                        'across the square. {Ns} runners stand very still on the steps.')]}}]

MARKS = {}
