"""Chroma library science: compiled by build.py from science.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'volunteers wanted to count what lives here',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (12, 90),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.04,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'community, nature',
 'horizon': 'months',
 'roles': "elder, friend, parent, the count's organiser",
 'share': 0.27,
 'share_group': 'citizen_science',
 'worlds': {'earth': 'a notice at the library asks for volunteers to count the birds, butterflies or river life of '
                     'the area this season'},
 'timing': {'times': 'per person from age 12: a call to count the birds, butterflies or river life of the area comes '
                     'many times over a life, through a school, a library or the local news; about 1 US adult in 10 '
                     'takes part in some citizen science in a year (Pew Research Center 2020)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A notice on the library board asks for volunteers for the spring count: one morning a week, '
                       'a clipboard, and a stretch of the river path. Training is on Saturday, with tea.'),
                      ('W',
                       'The county has counted its birds the same way every spring for forty years, the notice says, '
                       'and one stretch still has nobody to walk it. It is the path behind {Ns} street.'),
                      ('U',
                       'The small print explains the method: fixed routes, fixed times, ten minutes at each point, '
                       'and a photograph for any doubtful sighting. {N} likes that someone has worked out how to '
                       'turn a walk into evidence.'),
                      ('B',
                       "Almost in passing, the notice says last year's figures went into the council's report on the "
                       'houses planned for the meadow. Whoever does the counting, {N} realises, has a hand in that '
                       'report.'),
                      ('R',
                       'Last week {N} saw a kingfisher at the bridge, a streak of colour and then nothing. {N} has '
                       'wanted to see it again ever since.'),
                      ('G',
                       '{elder} has walked the river path every morning for thirty years and knows where the otters '
                       'come up. The count would be a reason to walk it alongside {elder}, and listen.')]},
 'outcomes': (["By midsummer {N} knows every bird on the stretch by its call, and the season's sheets are in on "
               'time.',
               'The count goes ahead with one more pair of eyes, and {Ns} name is in the list of thanks at the back '
               'of the county report.'],
              ['Two wet Saturdays in a row, and {N} never quite gets back into it.',
               '{N} goes to the wrong meeting point, misses the training, and the season starts without {N}.']),
 'options': [
    ('go to the Saturday training, and take a stretch of the route for the whole season', 'W1', None, 0.45, '', {'habit': True, 'v': 'universalism, conformity', 'title': 'citizen scientist', 'chance': 0.8}),
    ('read up on how the count works, then practise in the park for a month first', 'U1', None, 0.45, '', {'habit': True, 'v': 'self-direction, achievement', 'mark': 'learned a skill', 'self_control': '+', 'chance': 0.85}),
    ('count the meadow every week, so the neighbours have figures to put to the council', 'B1', None, 0.45, '', {'habit': True, 'identity': True, 'v': 'power, security', 'title': 'community observer', 'chance': 0.55}),
    ('turn up at dawn with binoculars and a flask, and count for the joy of it', 'R1', None, 0.45, '', {'habit': True, 'v': 'stimulation, hedonism', 'title': 'citizen scientist', 'self_control': '+', 'chance': 0.85}),
    ("count the river, but leave the otters' holt off the sheet, so nobody comes looking", 'G1', None, 0.45, '', {'v': 'universalism, security', 'mark': 'hid a wrong', 'closed': 'approval: leaving a sighting off a shared record; backfire: the holt is missing from the survey, and the bank is cleared for the new path', 'chance': 0.75}),
    ('bring a younger one from the family along, and teach them to tell the birds apart', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'benevolence, self-direction', 'chance': 0.65}),
    ("learn the calls well enough to be asked to lead next year's beginners' walk", 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.6}),
    ('keep Saturday mornings for yourself; nobody is paid to do this', 'B1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'chance': 0.95}),
    ('talk the whole family into a muddy Sunday morning on the count, with a picnic after', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, hedonism', 'chance': 0.65}),
    ('walk it with the old neighbour who knows the path, and keep the record their way', 'G1', 'W.7', 0.5, '', {'door': True, 'v': 'tradition, universalism', 'mark': 'learned a skill', 'title': 'citizen scientist', 'chance': 0.7}),
 ]},
{'name': 'a project online asks for a thousand pairs of eyes',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (12, 90),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.04,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'leisure, learning',
 'horizon': 'months',
 'roles': "parent, grandparent, friend, the project's scientists",
 'share': 0.25,
 'share_group': 'citizen_science',
 'worlds': {'earth': "an online project asks the public to help sort its images: galaxies, old ships' weather logs, "
                     'animals on camera-trap photos'},
 'timing': {'times': 'per person from age 12 who is online: an appeal to help sort galaxies, old logbooks or '
                     'camera-trap photos turns up every few years in the news or a feed; few join, and about 6 lives '
                     'in 100 ever take up citizen science for a season or more (estimate)',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       "A news item links to a science project that needs the public's eyes: half a million "
                       'photographs from camera traps in a far-off forest, each to be checked for animals. {N} '
                       'clicks through, and the first picture loads: dark leaves, and two eyes.'),
                      ('W',
                       'Every photograph is shown to fifteen volunteers and the answers are pooled, so no one '
                       "person's mistake counts for much. {N} likes the fairness of it, one careful pair of eyes "
                       'among many.'),
                      ('U',
                       'The tutorial takes six minutes, and the forum below it runs to thousands of posts on how the '
                       "crowd's answers are checked against the experts'. {N} wants to know how good the crowd "
                       'really is.'),
                      ('B',
                       "There is a leaderboard, and the project's papers thank the top volunteers by name. One of "
                       'them, a retired postman, is now listed as a co-author.'),
                      ('R',
                       'Empty forest, empty forest, empty forest, then a leopard yawning straight into the lens. {N} '
                       'laughs out loud, alone at the kitchen table.'),
                      ('G',
                       'The cameras have watched the same valley for six years, and day after day the same animals '
                       'pass the same tree. There is something steadying in watching a place go on living with '
                       'nobody there.')]},
 'outcomes': (["A month in, {N} can tell a civet from a mongoose at a glance, and the project's counter holds "
               'thousands of {Ns} answers.',
               'A scientist on the forum thanks {N} by name, and says the volunteers have saved the team a year.'],
              ['After a week the photographs blur into one another, and {N} stops logging in.',
               "{Ns} answers turn out to disagree with the experts' more often than not, and the project quietly "
               'gives them less weight.']),
 'options': [
    ('do the tutorial properly, then classify fifty photographs every evening before bed', 'W1', None, 0.45, '', {'habit': True, 'v': 'universalism, conformity', 'title': 'citizen scientist', 'self_control': '+', 'chance': 0.75}),
    ("study the forum's guide to the hard cases until your answers match the experts'", 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'title': 'citizen scientist', 'chance': 0.7}),
    ('log every hour you put in, and list it on your CV as volunteer research', 'B1', None, 0.45, '', {'habit': True, 'v': 'achievement', 'self_control': '+', 'chance': 0.9}),
    ('flag the odd shape in one photograph, and argue on the forum until a scientist looks', 'R1', None, 0.45, '', {'door': True, 'v': 'stimulation, self-direction', 'chance': 0.6}),
    ("spend a quiet hour every Sunday with the same valley's cameras, season after season", 'G1', None, 0.45, '', {'habit': True, 'v': 'universalism, tradition', 'title': 'citizen scientist', 'self_control': '+', 'chance': 0.75}),
    ('volunteer for the dull work of re-checking the photographs the crowd disagreed on', 'W1', 'U.7', 0.5, '', {'v': 'universalism, conformity', 'mark': 'learned a skill', 'self_control': '+', 'chance': 0.75}),
    ('quietly run a small script that clicks through the easy photographs for points', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': "approval: automated answers break the project's rules; backfire: the account is banned and every answer wiped", 'chance': 0.7}),
    ("ask for the big cats' raw footage, and cut a video of it to post online", 'B1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'chance': 0.5}),
    ('show the leopard to the family at dinner, and get everyone clicking together', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, hedonism', 'chance': 0.75}),
    ('do a page each evening with someone in the family who cannot get out much', 'G1', 'W.7', 0.5, '', {'v': 'benevolence', 'chance': 0.7}),
 ]},
{'name': 'a lab needs hands for the summer',
 'stages': 'young_adult adult',
 'age': (21, 45),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.08,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, learning',
 'horizon': 'months',
 'roles': 'mentor, boss, friend, colleague',
 'requires': 'graduate',
 'share': 0.35,
 'share_group': 'research_entry',
 'worlds': {'earth': 'a professor or a company lab needs a temporary assistant for the summer, and someone has '
                     'passed your name on'},
 'timing': {'times': 'per graduate aged 21 to 45: perhaps 1 in 10 are offered temporary research work through a '
                     'professor or a company lab, most of them science graduates soon after the degree; about 4 '
                     'adults in 10 hold a degree (OECD), so perhaps 1 life in 25 meets it (estimate)',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       '{mentor} forwards a message: a lab needs a pair of hands for twelve weeks this summer, paid, '
                       'starting on Monday week. The work is samples, spreadsheets and whatever breaks.'),
                      ('W',
                       'The offer comes with a contract, a safety induction and a folder of procedures to sign. {N} '
                       'reads every page, and finds the care in it reassuring.'),
                      ('U',
                       'The lab works on the very question {N} wrote a final-year essay about. Twelve weeks inside '
                       'the real thing, not the textbook version of it.'),
                      ('B',
                       'The pay is poor, but a summer in this lab means a reference from a professor people have '
                       'heard of. {N} starts counting the doors it could open.'),
                      ('R',
                       '{N} reads the message twice and is already picturing Monday week: new people, new machines, '
                       'something different every day.'),
                      ('G',
                       'The lab is in the old building by the river, where {N} studied. It would mean another summer '
                       'in the same town, near {friend} and the streets {N} knows by heart.')]},
 'outcomes': (['By the end of August {N} knows the lab inside out, and the professor offers to write a reference.',
               'The summer settles the question {N} came in with, one way or the other, and {N} leaves sure of the '
               'next step.'],
              ["The lab's money comes through late, the post shrinks to four weeks, and most of them are spent "
               'washing glassware.',
               '{N} and the professor get off on the wrong foot in the first week, and it never quite recovers.']),
 'options': [
    ('accept, and ask for the procedures to read before the first day', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'research assistant', 'chance': 0.12}),
    ("ask for the project's last report, and say yes only if the question holds up", 'U1', None, 0.45, '', {'v': 'self-direction', 'title': 'research assistant', 'chance': 0.12}),
    ('say you have run their sequencer before, and learn it over the weekend', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'research assistant', 'mark': 'hid a wrong', 'closed': 'approval: claiming experience that is not there; backfire: the first run fails and the professor asks who trained them', 'chance': 0.12}),
    ('say yes on the spot, and turn up on Monday week ready for anything', 'R1', None, 0.45, '', {'door': True, 'v': 'stimulation', 'title': 'research assistant', 'chance': 0.12}),
    ('say no, and spend the summer at home with the family as planned', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, benevolence', 'mark': 'stayed home', 'chance': 0.92}),
    ('agree once it is a proper contract, with the hours and the pay in writing', 'W1', 'B.7', 0.5, '', {'v': 'security, conformity', 'title': 'research assistant', 'chance': 0.12}),
    ("say yes, and ask for a small experiment of your own alongside the lab's work", 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'title': 'research assistant', 'chance': 0.12}),
    ("turn it down for better-paid work, and put the summer's wages toward a deposit", 'B1', 'G.7', 0.5, '', {'v': 'security, achievement', 'mark': 'turned down a chance', 'chance': 0.8}),
    ('pass the post to a friend who needs the work more, and help them settle in', 'R1', 'W.7', 0.5, '', {'binds': True, 'v': 'benevolence', 'mark': 'helped someone in need', 'chance': 0.85}),
    ("ask to work on the lab's field trips, where the samples are gathered", 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'self-direction, universalism', 'aims': 'research assistant', 'chance': 0.5}),
 ]},
{'name': 'a research post you are half qualified for',
 'stages': 'young_adult adult',
 'age': (21, 45),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.02,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, friend, partner, rival',
 'requires': 'graduate',
 'share': 0.3,
 'share_group': 'research_entry',
 'worlds': {'earth': 'a two-year research post asks for more than you have, and applications close on Friday'},
 'timing': {'times': 'per graduate aged 21 to 45: perhaps 1 in 5 who look for work meet a fixed-term research post '
                     'that asks for more than they have, most often science graduates; about 1 life in 50 ever holds '
                     'a research assistant post (estimate)',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       'The advert is for a two-year research post, and {N} meets about half of what it asks: the '
                       "degree yes, the three years' experience no, the software skills only in part. Applications "
                       'close on Friday.'),
                      ('W',
                       'The advert lists eleven essential criteria. {N} goes down them with a pen, ticking only the '
                       'honest ones, and stops at six.'),
                      ('U',
                       "{N} reads the group's last three papers and starts to see where {Ns} odd mix of skills might "
                       'fit. Their data handling has a gap that anyone could see.'),
                      ('B',
                       '{N} has heard that adverts like this are wish lists, and that the people who get such posts '
                       'are often simply the ones who apply anyway.'),
                      ('R',
                       'It is exactly the work {N} has wanted for years. Just reading it makes {Ns} heart race, and '
                       'the missing half of the criteria feels like a detail.'),
                      ('G',
                       '{mentor} used to say that the right post comes in its own season. {N} wonders whether this '
                       'is that season, or only a tempting one.')]},
 'outcomes': (['The letter lands well, and {N} is asked to an interview the following week.',
               'Whatever the outcome, {N} comes away knowing exactly what is missing, and how to get it.'],
              ['An automatic email arrives a month later: the post has gone to someone with the full three years.',
               '{N} misses the Friday deadline by an hour, and the portal will not reopen.']),
 'options': [
    ('apply honestly, and say plainly in the letter which criteria you do not meet yet', 'W1', None, 0.45, '', {'identity': True, 'v': 'conformity, achievement', 'title': 'research assistant', 'chance': 0.12}),
    ('take the evening course that covers the missing half, and apply next round', 'U1', None, 0.45, '', {'door': True, 'v': 'achievement, self-direction', 'mark': 'learned a skill', 'self_control': '+', 'aims': 'research assistant', 'chance': 0.85}),
    ('ring the group leader before applying, and talk your way onto the shortlist', 'B1', None, 0.45, '', {'v': 'achievement, power', 'title': 'research assistant', 'chance': 0.12}),
    ('apply tonight, and let the letter say how much you want this work', 'R1', None, 0.45, '', {'v': 'stimulation', 'title': 'research assistant', 'chance': 0.12}),
    ("offer to take over the group's neglected data archive, and learn it field by field", 'G1', None, 0.45, '', {'binds': True, 'v': 'universalism, security', 'title': 'research data steward', 'requires': 'research assistant', 'without': 'impossible', 'chance': 0.12}),
    ('ring the contact named in the advert, and ask what would make a strong candidate', 'W1', 'B.7', 0.5, '', {'v': 'achievement, security', 'chance': 0.85}),
    ('build a small tool for their public data, and send it with the application', 'U1', 'R.7', 0.5, '', {'identity': True, 'v': 'self-direction, stimulation', 'title': 'research software engineer', 'requires': 'research assistant', 'without': 'impossible', 'chance': 0.12}),
    ('weigh the pay cut against the rent, and stay in the job you have', 'B1', 'G.7', 0.5, '', {'v': 'security', 'mark': 'turned down a chance', 'chance': 0.85}),
    ('tell a friend who fits the post better, and help with their application', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'mark': 'helped someone in need', 'chance': 0.85}),
    ('ask your old supervisor honestly whether you are ready, and take the answer', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'chance': 0.8}),
 ]},
{'name': 'the contract runs out',
 'stages': 'young_adult adult mature',
 'age': (20, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'adult',
 'per_year': (0.0, 0.0, 0.35, 0.3, 0.2, 0.0),
 'drivers': 'prosper-.3 unrest+.2 money-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, mentor, colleague, partner',
 'requires': 'research assistant',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'your fixed-term research contract ends in three months, and nobody has said whether there is '
                     'another'},
 'timing': {'times': 'per research assistant of a year or more a year: about 35 in 100 young adults, 30 in 100 '
                     'adults and 20 in 100 in midlife come to the end of a fixed-term contract with no renewal '
                     "promised; most research assistant posts run one to three years on one grant's money, and older "
                     'assistants more often hold rolling posts (estimate)',
            'likelier': 'a post paid from a single grant, tight research budgets, a supervisor who is retiring or '
                        'moving away',
            'rarer': 'an open-ended post, a group with steady money, a boom in research spending'},
 'scenes': {'earth': [('',
                       'The email from human resources is two lines long: the contract ends on the last day of June. '
                       '{boss} says there might be money in the autumn, and might not.'),
                      ('W',
                       '{N} has done every task the post asked, on time and to the standard. The rules still say the '
                       'post ends in June, and rules are rules.'),
                      ('U',
                       'On the back of a protocol {N} makes two lists: what two years at this bench have taught, and '
                       'what every advertised post asks for. The second list is longer.'),
                      ('B',
                       'Two years of evenings at the bench, and {boss} talks about the autumn as if it were the '
                       'weather. {N} starts counting who owes a favour.'),
                      ('R',
                       '{N} reads the email standing up, then goes out to the car park and walks round it twice. '
                       'Whatever comes next, {N} wants to be the one who picks it.'),
                      ('G',
                       'The lab has come to feel like a second home: the hum of the freezers, the same faces at '
                       'morning coffee. {N} can feel the season turning.')]},
 'outcomes': (['By the end of June the next step is settled, and {N} knows where the autumn will be spent.',
               '{boss} writes a warm reference, and the first door {N} knocks on opens.'],
              ['June ends with nothing signed, and {N} clears the desk into a cardboard box.',
               'The post goes to someone with more papers, and {N} hears about it in the corridor.']),
 'options': [
    ('apply for a funded doctoral place, and do it the proper way first', 'W1', None, 0.45, '', {'door': True, 'binds': True, 'drops': 'research assistant', 'v': 'conformity, achievement', 'self_control': '+', 'aims': 'research scientist', 'chance': 0.55}),
    ('apply for the scientist post on the strength of the work, papers attached', 'U1', None, 0.45, '', {'title': 'research scientist', 'requires': 'doctoral graduate', 'without': 'approval', 'v': 'achievement', 'chance': 0.45}),
    ('ring everyone who owes a favour until someone finds money for a new contract', 'B1', None, 0.45, '', {'v': 'power, security', 'self_control': '+', 'chance': 0.65}),
    ('let it end, and spend the summer travelling before deciding anything', 'R1', None, 0.45, '', {'drops': 'research assistant', 'v': 'hedonism, stimulation', 'chance': 0.92}),
    ("ask to stay on as the keeper of the group's data and records", 'G1', None, 0.45, '', {'title': 'research data steward', 'requires': 'working with data', 'without': 'approval', 'v': 'security, tradition', 'chance': 0.12}),
    ('become the one person who knows where every sample is kept, and make it known', 'B.5 G.5', None, 0.5, '', {'habit': True, 'v': 'power', 'chance': 0.65}),
    ('take a better-paid post at a company lab abroad, and leave within the month', 'B.5 R.5', None, 0.5, '', {'door': True, 'mark': 'moved away', 'v': 'achievement, stimulation', 'chance': 0.6}),
    ('write up two years of notes as a clean dataset while looking for the next post', 'U.5 G.5', None, 0.5, '', {'v': 'achievement, universalism', 'self_control': '+', 'chance': 0.85}),
    ('argue at the group meeting that the project cannot finish without the post', 'W.5 R.5', None, 0.5, '', {'v': 'achievement, self-direction', 'chance': 0.55}),
    ('take the technician post the group can offer, and keep its methods in good order', 'W.5 U.5', None, 0.5, '', {'title': 'laboratory technician', 'v': 'security, conformity', 'chance': 0.9}),
 ]},
{'name': 'a fellowship of your own',
 'stages': 'young_adult adult mature',
 'age': (24, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'adult',
 'per_year': (0.0, 0.0, 0.03, 0.04, 0.015, 0.0),
 'drivers': 'prosper+.3 ties+.2 fortune+.15 money+.1',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'years',
 'roles': 'mentor, boss, colleague, partner, rival',
 'requires': 'research scientist',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': 'a funder offers you a fellowship of your own: five years of money for your own question'},
 'timing': {'times': 'per research scientist of two years or more a year: about 3 in 100 young adults, 4 in 100 '
                     'adults and 1.5 in 100 in midlife are offered a fellowship or a starting grant in their own '
                     'name, money for their own question for three to five years; personal fellowships fund roughly '
                     'one application in six to ten, and most go to scientists in the first ten years after a '
                     'doctorate (estimate)',
            'likelier': 'published work others cite, a mentor who backs the application, a prosperous time for '
                        'research, a recent success',
            'rarer': "years spent on other people's projects, a career break that is still showing on the record, "
                     'hard times for research money'},
 'scenes': {'earth': [('',
                       'The letter from the funder opens with congratulations. Five years of money, in {Ns} own '
                       'name, for {Ns} own question. {N} reads it three times before believing it.'),
                      ('W',
                       'The fellowship comes with conditions: annual reports, an ethics review, a host institution '
                       'that must sign. {N} reads every clause, because a promise made on paper is a promise.'),
                      ('U',
                       'Five years. {N} begins at once to sketch what the first year should settle, and what the '
                       'fifth could answer if the first goes well.'),
                      ('B',
                       "For the first time nobody else's name sits above {Ns} on the money. {N} knows exactly what "
                       'that is worth in the next conversation with {boss}.'),
                      ('R',
                       '{N} rings {partner}, then {mentor}, then anyone who picks up, and is laughing too hard to '
                       'finish a sentence.'),
                      ('G',
                       '{N} thinks of the old field notebooks on the shelf at home, where the question first '
                       'appeared. It has taken this long to grow, and it is finally ready.')]},
 'outcomes': (['The decision holds, and the next five years take a shape {N} chose.',
               '{mentor} hears the news and says it was only a matter of time, and {N} almost believes it.'],
              ['The host institution will not agree the terms, and the offer lapses in the autumn.',
               'The paperwork drags on for months, and by the time it clears, half the plan no longer makes sense.']),
 'options': [
    ('accept, and keep every reporting promise to the funder to the letter', 'W1', None, 0.45, '', {'grants': 'research grant; a research project under way', 'v': 'conformity, achievement', 'chance': 0.9}),
    ('take a month to test whether the question deserves five years before saying yes', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'chance': 0.9}),
    ('use the offer to bargain the institute into a permanent post', 'B1', None, 0.45, '', {'v': 'power, security', 'chance': 0.6}),
    ('say yes on the spot, and set up on your own terms', 'R1', None, 0.45, '', {'title': 'independent investigator', 'grants': 'research grant; a research project under way', 'v': 'self-direction, stimulation', 'chance': 0.15}),
    ('turn it down, and stay with the group and the place the work belongs to', 'G1', None, 0.45, '', {'identity': True, 'mark': 'turned down a chance', 'v': 'tradition', 'chance': 0.95}),
    ('take it abroad, to the field station by the reef you always wanted to study', 'R.5 G.5', None, 0.5, '', {'door': True, 'binds': True, 'mark': 'moved away', 'grants': 'research grant; a research project under way', 'v': 'stimulation, self-direction', 'chance': 0.65}),
    ('build a speciality nobody else has, and answer to no one for five years', 'U.5 B.5', None, 0.5, '', {'identity': True, 'binds': True, 'title': 'independent investigator', 'grants': 'research grant; a research project under way', 'v': 'self-direction, power', 'chance': 0.15}),
    ('go it alone on the risky question no grant panel would ever touch', 'U.5 R.5', None, 0.5, '', {'title': 'independent investigator', 'grants': 'research grant; a research project under way', 'v': 'stimulation', 'chance': 0.15}),
    ('accept, but negotiate staff, space and a budget line before signing', 'W.5 B.5', None, 0.5, '', {'binds': True, 'title': 'research project lead', 'grants': 'research grant; a research project under way', 'v': 'power, achievement', 'chance': 0.65}),
    ('ask the funder whether it can be shared with a colleague whose contract is ending', 'W.5 G.5', None, 0.5, '', {'grants': 'research grant; research collaborators', 'mark': 'helped someone in need', 'v': 'benevolence', 'chance': 0.4}),
 ]},
{'name': 'they want you to lead a group',
 'stages': 'young_adult adult mature',
 'age': (27, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'mature',
 'per_year': (0.0, 0.0, 0.02, 0.05, 0.04, 0.0),
 'drivers': 'prosper+.3 ties+.2 fortune+.1 money+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'years',
 'roles': 'boss, mentor, colleague, rival',
 'requires': 'research project lead',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the institute asks you to lead a research group of your own: eight people, a budget and the '
                     'direction of the work'},
 'timing': {'times': 'per research project lead of three years or more a year: about 2 in 100 young adults, 5 in 100 '
                     'adults and 4 in 100 in midlife are asked to take on a research group of their own, with its '
                     'people, its money and its direction; roughly one project lead in three leads a group at some '
                     'point, and many are asked more than once before they say yes (estimate)',
            'likelier': 'a project that delivered, published work and a grant in hand, a group whose leader is '
                        'retiring or leaving, good years for the institution',
            'rarer': 'a shrinking department, a short record, a reputation for wanting to stay at the bench'},
 'scenes': {'earth': [('',
                       "{boss} closes the office door and gets to the point: the group's leader is leaving in the "
                       'spring, and the institute wants {N} to take it on. Eight people, a budget, and every '
                       'decision that comes with them.'),
                      ('W',
                       "A group is a responsibility before it is an honour: eight people's contracts, their "
                       'training, their safety. {N} pictures signing every one of those forms.'),
                      ('U',
                       '{N} wonders how much science is left in a job made of budgets and meetings, and starts to '
                       'work it out in hours per week.'),
                      ('B',
                       "Eight people, a budget and a say in the department's plans. {N} has wanted this kind of room "
                       'for years, and {rival} wanted it too.'),
                      ('R',
                       '{Ns} first thought is of the bench, and the experiment still running there. Then a jolt of '
                       'excitement: everything could be done differently.'),
                      ('G',
                       '{N} thinks of the old head of the group, who kept everyone together through two lean '
                       'decades. Those are big shoes, and the people in the group are like family.')]},
 'outcomes': (['{boss} takes the answer well, and by the spring the next years have the shape {N} wanted.',
               'A year on, {N} is sure the choice was right, whatever the hard weeks cost.'],
              ['The institute takes the answer badly, and {N} feels it in every meeting for a year.',
               'The new role swallows every week, and {N} cannot remember the last day at the bench.']),
 'options': [
    ('ask for the post to be advertised, and go through the open competition like anyone else', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.75}),
    ('talk to three group leaders about their real weeks before answering', 'U1', None, 0.45, '', {'v': 'self-direction', 'chance': 0.85}),
    ('say yes only with more starting money, and hold out until they agree', 'B1', None, 0.45, '', {'title': 'research group leader', 'v': 'power', 'self_control': '+', 'chance': 0.6}),
    ('say yes before the meeting is over, and work out the rest as you go', 'R1', None, 0.45, '', {'binds': True, 'title': 'research group leader', 'v': 'stimulation, achievement', 'chance': 0.8}),
    ('ask the retiring head to stay on one more year, and decide beside them', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.75}),
    ('take the group, and keep the best of the old team and the equipment close', 'B.5 G.5', None, 0.5, '', {'title': 'research group leader', 'v': 'power', 'chance': 0.6}),
    ('take the group and run it your own way from the first week', 'B.5 R.5', None, 0.5, '', {'identity': True, 'title': 'research group leader', 'v': 'power, self-direction', 'chance': 0.75}),
    ('decline, and ask instead for a year to try the odd idea you keep putting off', 'U.5 R.5', None, 0.5, '', {'door': True, 'mark': 'turned down a chance', 'v': 'stimulation', 'chance': 0.45}),
    ('accept, and bring on the juniors the way your own mentor once did', 'W.5 G.5', None, 0.5, '', {'title': 'research group leader', 'v': 'benevolence, tradition', 'chance': 0.8}),
    ("accept the chair that comes with the group, and set down five years' goals", 'W.5 U.5', None, 0.5, '', {'title': 'research group leader; professor', 'v': 'achievement, conformity', 'chance': 0.7}),
 ]},
{'name': 'the facility needs a head',
 'stages': 'young_adult adult mature',
 'age': (24, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'mature',
 'per_year': (0.0, 0.0, 0.002, 0.006, 0.008, 0.0),
 'drivers': 'prosper+.2 ties+.2 fortune+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'years',
 'roles': 'boss, colleague, mentor, elder',
 'requires': 'laboratory technician | research scientist',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the shared facility where you work needs a new head, and the institute asks you'},
 'timing': {'times': 'per laboratory technician or research scientist of three years or more a year: about 2 in '
                     '1,000 young adults, 6 in 1,000 adults and 8 in 1,000 in midlife are asked to head a shared '
                     'facility (a microscopy suite, a sequencing service, a set of instruments many groups use); '
                     'such posts are few, roughly one for every twenty of the technicians and staff scientists who '
                     'keep the machines running, and open when the old head retires or moves on (estimate)',
            'likelier': 'years on the same machines, being the one who fixes them, a head of facility near '
                        'retirement, an institution that is growing',
            'rarer': 'a short time in post, a facility being closed or merged, an institution that hires its heads '
                     'from outside'},
 'scenes': {'earth': [('',
                       "The facility manager retires at the year's end, and the institute has found nobody. {boss} "
                       'asks {N}, who has kept the old microscope running for years, whether {N} would take the '
                       'whole place on.'),
                      ('W',
                       '{N} thinks of the logbook, the safety sheets and the queue of students who need training. '
                       'Someone has to keep all of it in order, and {N} already does half of it.'),
                      ('U',
                       '{N} knows every quirk of the old microscope and most of the new one. Running the place would '
                       'mean learning the other machines just as well, and the thought is not unwelcome.'),
                      ('B',
                       'Head of facility comes with a salary grade, a budget and a say in what the institute buys. '
                       "Years of fixing other people's machines may finally pay."),
                      ('R',
                       '{N} loves the moment the image comes up sharp on the screen. Running the facility means '
                       'spreadsheets and meetings, and the thought sits badly.'),
                      ('G',
                       '{elder} trained {N} on these machines, and someone trained {elder} before that. The '
                       'instruments and the know-how have always been handed on this way.')]},
 'outcomes': (["The facility has a head by the year's end, and the booking calendar fills up again.",
               "The first users' meeting goes well, and even the busiest group leaders nod along."],
              ['The institute drags its feet, and the facility runs without a head through the winter.',
               'Two groups quarrel over the first decision, and {N} is caught in the middle.']),
 'options': [
    ('accept, and write the booking rules and safety training before anything else', 'W1', None, 0.45, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'v': 'security, conformity', 'chance': 0.75}),
    ('ask for a month to learn every instrument down to the last setting first', 'U1', None, 0.45, '', {'v': 'achievement, conformity', 'self_control': '+', 'chance': 0.85}),
    ('accept, and make the facility pay its way by selling machine time to companies', 'B1', None, 0.45, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'v': 'power, achievement', 'chance': 0.75}),
    ('tell the institute bluntly what the facility needs, whoever ends up leading it', 'R1', None, 0.45, '', {'v': 'universalism, self-direction', 'chance': 0.65}),
    ('accept, and run it as the old head did, every user known by name', 'G1', None, 0.45, '', {'binds': True, 'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'v': 'tradition, benevolence', 'chance': 0.7}),
    ('turn the post down, but offer to run the training days on the machines you love', 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence, self-direction', 'chance': 0.75}),
    ('negotiate a specialist post instead, as the one person who can run the new machine', 'U.5 B.5', None, 0.5, '', {'v': 'achievement, power', 'chance': 0.65}),
    ('take it on jointly with a colleague, as some other facilities do', 'U.5 G.5', None, 0.5, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'v': 'universalism, benevolence', 'chance': 0.55}),
    ('write the dean a costed case for proper funding before anyone takes the job', 'W.5 B.5', None, 0.5, '', {'v': 'security', 'chance': 0.45}),
    ('speak up at the meeting for a junior technician who has earned the chance', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'universalism', 'chance': 0.55}),
 ]},
{'name': 'leaving research for another life',
 'stages': 'young_adult adult mature',
 'age': (24, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'adult mature',
 'per_year': (0.0, 0.0, 0.07, 0.05, 0.03, 0.0),
 'drivers': 'money-.3 stress+.3 family+.2 prosper-.2 trouble+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'partner, mentor, friend, boss',
 'requires': 'research scientist',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'after years of short contracts, you wonder whether to leave research for another kind of life'},
 'timing': {'times': 'per research scientist of a year or more a year: about 7 in 100 young adults, 5 in 100 adults '
                     'and 3 in 100 in midlife come to a point where leaving research for another field is a real '
                     'choice; in rich countries about half of science doctorates work outside research ten years on, '
                     'and most who leave do so in the first years of fixed-term posts (estimate)',
            'likelier': 'one fixed-term contract after another, a move to a new city for each post, a partner or '
                        'children who need a settled place, low pay next to friends outside research',
            'rarer': 'a permanent post, a growing field, a funded group, research that pays well'},
 'scenes': {'earth': [('',
                       'Another contract ends in March, and the only post on offer is in another country again. '
                       '{partner} asks, gently, what the plan is.'),
                      ('W',
                       '{N} owes something to the people who trained {N} and the funders who paid. {N} also owes '
                       'something to {partner}, and to a life that keeps being put off.'),
                      ('U',
                       '{N} lays it out like a problem: what the skills are worth outside, what would be lost, the '
                       'odds of a permanent post inside. The numbers are not kind.'),
                      ('B',
                       'Friends from the same degree own houses. {N} has a dozen papers and a bicycle. It is time '
                       'the skills started to pay.'),
                      ('R',
                       'Some mornings {N} still feels the old thrill at the bench. Other mornings {N} wants to throw '
                       'the whole thing in and start something new.'),
                      ('G',
                       'Research has been {Ns} whole working life. Leaving would feel like leaving home, but staying '
                       'no longer feels like staying anywhere.')]},
 'outcomes': (['{N} makes the move, and within a year the new life has its own rhythm and its own satisfactions.',
               'The skills turn out to be worth more than {N} thought, and the old papers are still {Ns}.'],
              ['The new start goes badly, and {N} misses the bench more than expected.',
               'Nothing comes of it by March, and {N} signs another short contract, a little more tired.']),
 'options': [
    ("move into school teaching, and bring the lab's questions to a classroom", 'W1', None, 0.45, '', {'door': True, 'title': 'teacher', 'requires': 'professional registration', 'without': 'law', 'v': 'benevolence, conformity', 'chance': 0.6}),
    ("take a data analyst's job, where the same methods are worth more", 'U1', None, 0.45, '', {'title': 'data analyst', 'v': 'achievement, security', 'chance': 0.7}),
    ('leave to start a small company on what you know best', 'B1', None, 0.45, '', {'door': True, 'binds': True, 'title': 'founder of a firm', 'v': 'power, self-direction', 'mark': 'took a wild risk', 'chance': 0.45}),
    ('become a science communicator, at a museum or on the radio', 'R1', None, 0.45, '', {'identity': True, 'title': 'science communication specialist', 'requires': 'explaining science', 'without': 'means', 'v': 'stimulation, benevolence', 'chance': 0.4}),
    ('leave research to be at home for the family, for as long as they need', 'G1', None, 0.45, '', {'identity': True, 'drops': 'research scientist', 'v': 'benevolence, tradition', 'chance': 0.75}),
    ('stay, and campaign for fair contracts for everyone on short posts', 'W.34 U.33 R.33', None, 0.5, '', {'identity': True, 'v': 'universalism', 'chance': 0.4}),
    ('stay one more year, and build a case with figures for a permanent post', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, achievement', 'self_control': '+', 'chance': 0.45}),
    ('move back home and start a science club in the town where you grew up', 'W.34 R.33 G.33', None, 0.5, '', {'drops': 'research scientist', 'mark': 'came home', 'v': 'benevolence, tradition', 'chance': 0.7}),
    ('move into evidence synthesis, weighing whole fields for the people who decide', 'U.34 B.33 G.33', None, 0.5, '', {'title': 'evidence synthesis specialist', 'v': 'universalism, achievement', 'chance': 0.3}),
    ('take a paid job outside, and keep the question you love going at weekends', 'B.34 R.33 G.33', None, 0.5, '', {'drops': 'research scientist', 'grants': 'a research project under way', 'v': 'self-direction', 'chance': 0.75}),
 ]},
{'name': 'the funding call closes on Friday',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.3, 0.35, 0.3, 0.0),
 'drivers': 'prosper+.2 era+.2 stress+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, mentor, boss, partner',
 'requires': 'a research project under way',
 'worlds': {'earth': 'a funding call that fits your project closes on Friday, and the proposal is not written'},
 'timing': {'times': 'per person with a research project under way a year: about 30 in 100 young adults, 35 in 100 '
                     'adults and 30 in 100 in midlife meet a funding call that fits the work, with a deadline that '
                     "will not move; researchers who live on grants apply once or twice a year, volunteers' projects "
                     'far less often, and a credible proposal is funded about one time in five to one in four '
                     '(estimate from the success rates public funders report)',
            'likelier': 'a project whose money runs out next year, a funder with a new programme, prosperous years '
                        'for research',
            'rarer': 'a project with long-term money, a volunteer project with no institution to apply through, cuts '
                     'to research budgets'},
 'scenes': {'earth': [('',
                       "The call was announced three weeks ago and closes at five on Friday. The project's money "
                       'runs out next year, and {N} has a blank document, a budget template and four days.'),
                      ('W',
                       'The guidance notes run to forty pages. {N} prints them, reads every page with a pen in hand, '
                       'and starts a checklist.'),
                      ('U',
                       '{N} knows the question is good. The hard part is saying in two pages why it matters and how '
                       'it will be answered, without a wasted word.'),
                      ('B',
                       "Last year's winners all used the same three phrases. {N} notices, and wonders how far the "
                       'project could lean toward them.'),
                      ('R',
                       'Four days is mad. {N} feels the deadline like a starting gun and wants to write the whole '
                       'thing in one long burst.'),
                      ('G',
                       'Funding calls come and go like weather. {N} looks at the work on the bench, which needs '
                       'tending this week whatever the funder decides.')]},
 'outcomes': (['By Friday evening the decision is behind {N}, and it was the right one for the work.',
               'Months later the project has money for another year, from this call or the next one.'],
              ['At ten to five the upload portal freezes, and nothing goes in.',
               'The rejection comes in the spring, with three reviews, two of them kind.']),
 'options': [
    ('write it by the book, every form, budget line and support letter in order', 'W1', None, 0.45, '', {'grants': 'research grant; grant writing', 'grants_if_fails': 'grant writing', 'v': 'conformity, achievement', 'chance': 0.22}),
    ('spend the week sharpening one question until the proposal is airtight', 'U1', None, 0.45, '', {'grants': 'research grant; grant writing', 'grants_if_fails': 'grant writing', 'v': 'achievement', 'chance': 0.25}),
    ('bend the project to fit what the call wants to fund this year', 'B1', None, 0.45, '', {'grants': 'research grant; grant writing', 'grants_if_fails': 'grant writing', 'v': 'power, achievement', 'chance': 0.3}),
    ('write it in three nights on pure conviction, and send it at midnight', 'R1', None, 0.45, '', {'habit': True, 'grants': 'research grant; grant writing', 'grants_if_fails': 'grant writing', 'v': 'stimulation', 'self_control': '+', 'chance': 0.22}),
    ('build the case on the long record of the place, and send it plainly', 'G1', None, 0.45, '', {'grants': 'research grant; grant writing', 'grants_if_fails': 'grant writing', 'v': 'tradition', 'chance': 0.24}),
    ('write it with the whole team, each part by whoever knows it best', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'grant writing', 'v': 'benevolence, achievement', 'chance': 0.8}),
    ("skip this call, and press the funder's officer for one that fits next year", 'W.34 B.33 R.33', None, 0.5, '', {'v': 'power, achievement', 'chance': 0.55}),
    ('ask the old hand who sits on funding panels to read it and mark it up', 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'grant writing', 'v': 'tradition, achievement', 'chance': 0.75}),
    ('let it pass: the deadline is mad, and the work itself matters more', 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'self-direction', 'chance': 0.92}),
    ("read last year's winning proposals first, and learn how they are built", 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'grant writing', 'v': 'achievement', 'chance': 0.85}),
 ]},
{'name': 'pressure to say more than the data show',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.1, 0.12, 0.1, 0.0),
 'drivers': 'stress+.3 money-.2 era+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'boss, colleague, mentor',
 'requires': 'a research project under way',
 'worlds': {'earth': 'a partner wants the results described as a success, and the data show something much smaller'},
 'timing': {'times': 'per person with a research project under way a year: about 10 in 100 young adults, 12 in 100 '
                     'adults and 10 in 100 in midlife are pressed by a funder, a partner company, a boss or a press '
                     'office to claim more than the results show; surveys of researchers find such pressure common, '
                     'most of all where money or publicity is at stake (estimate)',
            'likelier': 'a company paying for the work, a press office, a result that matters for money or policy, a '
                        'boss under pressure of their own',
            'rarer': 'a project with no sponsor, a field with strict reporting rules, a team that has been burned '
                     'before'},
 'scenes': {'earth': [('',
                       'The draft press release comes from the partner company with a headline that says the method '
                       'works. {Ns} data show a small effect in one group out of four, and {boss} has already said '
                       'it looks fine.'),
                      ('W',
                       'There are guidelines for exactly this, and {N} knows where they are kept. A claim that goes '
                       "out under the institute's name is bound by the institute's rules."),
                      ('U',
                       '{N} reads the headline against the figure: one subgroup, wide error bars, a result that only '
                       'just crossed the line. The headline describes a different study.'),
                      ('B',
                       'The partner company pays for half the project and has hinted at a second phase. A strong '
                       'headline helps everyone, and {N} could ask for something in return.'),
                      ('R',
                       '{N} reads the headline and feels heat rise up the neck. It is not true, and everyone in the '
                       'room knows it.'),
                      ('G',
                       '{N} has seen this before: a big claim, a season of fuss, then the quiet years when the real '
                       'result settles in. The work will outlast the headline either way.')]},
 'outcomes': (["The wording is settled, the partner is satisfied, and the project's next phase looks safe.",
               'The press interest passes without harm, and {N} comes out of it with standing intact.'],
              ['The strong headline runs anyway, with {Ns} name under it.',
               'The partner takes offence, and the second phase of the project quietly disappears.']),
 'options': [
    ('report the pressure through the proper channel, the research integrity office', 'W1', None, 0.45, '', {'identity': True, 'grants': 'research integrity', 'v': 'conformity, universalism', 'chance': 0.55}),
    ('rewrite the summary yourself, every claim matched to the figure behind it', 'U1', None, 0.45, '', {'identity': True, 'grants': 'research integrity', 'v': 'universalism, achievement', 'self_control': '+', 'chance': 0.75}),
    ('agree to the stronger wording in return for your name on the follow-up grant', 'B1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a claim the data do not support; backfire: a larger study finds the effect is small, and the strong claim carries this name', 'v': 'power, achievement', 'self_control': '-', 'chance': 0.8}),
    ('refuse flatly in the meeting, and say out loud that the claim is not true', 'R1', None, 0.45, '', {'identity': True, 'mark': 'defied an authority', 'v': 'self-direction, universalism', 'chance': 0.65}),
    ('say nothing to the press, and let the paper speak for itself in time', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.65}),
    ('stall politely until the press interest moves on to something else', 'B.5 G.5', None, 0.5, '', {'v': 'security, power', 'chance': 0.8}),
    ('take the press officer to see the actual samples, so the numbers feel real', 'R.5 G.5', None, 0.5, '', {'v': 'benevolence, universalism', 'chance': 0.45}),
    ('write the press release yourself, exciting and exact at once', 'U.5 R.5', None, 0.5, '', {'v': 'achievement, stimulation', 'chance': 0.7}),
    ('negotiate wording everyone can live with: strong verbs, honest numbers', 'W.5 B.5', None, 0.5, '', {'v': 'conformity, power', 'chance': 0.7}),
    ('add a plain paragraph on what the data cannot show, and insist it stays in', 'W.5 U.5', None, 0.5, '', {'grants': 'research integrity', 'v': 'universalism, conformity', 'chance': 0.65}),
 ]},
{'name': 'an error in your published work',
 'stages': 'young_adult adult mature',
 'age': (22, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.025, 0.02, 0.0),
 'drivers': 'stress+.2 era+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'colleague, mentor, boss',
 'requires': 'published research',
 'worlds': {'earth': 'someone finds an error in a paper you published, and the main result shrinks'},
 'timing': {'times': 'per person with published research a year: about 2 in 100 young adults and people in midlife '
                     'and 2.5 in 100 adults find a real error in their own published work (a coding slip, a '
                     'mislabelled sample, a wrong unit); journals correct only a small share of papers, but someone '
                     'who publishes for decades meets at least one such error more often than not (estimate)',
            'likelier': 'many papers, long analysis code, data handled by many hands, a field where others re-run '
                        'published work',
            'rarer': 'few papers, simple methods, work nobody looks at again'},
 'scenes': {'earth': [('',
                       'A student re-running the analysis for a new project comes to {Ns} door with a printout. A '
                       'line of code in the published paper counted some samples twice. Fixed, the main effect '
                       'shrinks by a third.'),
                      ('W',
                       'The paper is part of the record now, cited forty times. A record that is wrong has to be put '
                       'right, and the journal has a form for exactly that.'),
                      ('U',
                       '{N} sits down with the code straight away. Before anything else, {N} needs to know exactly '
                       'what the error changes, and what it does not.'),
                      ('B',
                       'Forty citations, and a grant renewal that leans on them. {N} feels the ground shift, and '
                       'starts to think about who else knows.'),
                      ('R',
                       '{Ns} face burns. {N} wants to tell everyone at once, or to tear up the printout, and cannot '
                       'tell which.'),
                      ('G',
                       'Mistakes find their way into every harvest. What matters now is what to do with this one, '
                       'since it has come to light.')]},
 'outcomes': (['The matter is settled the way {N} chose, and the work goes on without a scandal.',
               'The main finding survives, smaller but solid, and the grant renewal goes through.'],
              ['The story gets out before {N} is ready, and the corridor goes quiet when {N} walks by.',
               'The grant panel hears about the error and asks hard questions at the renewal.']),
 'options': [
    ('write to the journal at once and ask for a formal correction', 'W1', None, 0.45, '', {'identity': True, 'grants': 'research integrity', 'mark': 'owned up', 'v': 'conformity, universalism', 'chance': 0.9}),
    ('fix the numbers in the next paper, and say nothing about the old one', 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a known error left in the record; backfire: someone else finds it and asks in public why it was never corrected', 'v': 'achievement', 'self_control': '-', 'chance': 0.75}),
    ('tell the co-authors the slip was made by the junior who ran the analysis', 'B1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "approval: blaming a junior for one's own error; backfire: the junior kept the emails that show who wrote the code", 'v': 'power, security', 'chance': 0.65}),
    ('tell the whole lab that afternoon, embarrassed and honest, and fix it together', 'R1', None, 0.45, '', {'mark': 'owned up', 'v': 'benevolence, self-direction', 'self_control': '+', 'chance': 0.92}),
    ('let it lie: the paper is old, and the field has moved on', 'G1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a known error left in the record; backfire: a review repeats the old number, and the error spreads', 'v': 'security, tradition', 'self_control': '-', 'chance': 0.75}),
    ('publish the correction yourself before anyone else can, on your own terms', 'B.5 R.5', None, 0.5, '', {'mark': 'owned up', 'v': 'power, self-direction', 'self_control': '+', 'chance': 0.8}),
    ('rerun everything first, to know exactly how bad it is before telling anyone', 'U.5 B.5', None, 0.5, '', {'habit': True, 'v': 'achievement, security', 'chance': 0.9}),
    ('thank the student, and redo the whole analysis together, line by line', 'U.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'v': 'benevolence, achievement', 'chance': 0.8}),
    ('tell the co-authors first, and decide together how to set it right', 'W.5 G.5', None, 0.5, '', {'v': 'conformity, benevolence', 'chance': 0.8}),
    ('retract the whole paper, though the main finding mostly survives', 'W.5 R.5', None, 0.5, '', {'grants': 'research integrity', 'mark': 'owned up', 'v': 'universalism', 'chance': 0.9}),
 ]},
{'name': 'the field season is lost',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.06, 0.06, 0.05, 0.0),
 'drivers': 'harsh+.4 unrest+.4 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss, friend',
 'requires': 'a research project under way',
 'worlds': {'earth': 'the season for your fieldwork is lost to a storm, a permit, a war or a broken boat, and it '
                     'comes once a year'},
 'timing': {'times': 'per person with a research project under way a year: about 6 in 100 young adults and adults '
                     'and 5 in 100 in midlife lose a season or an observation window that cannot be had back: a '
                     'storm, a permit refused or late, a war or an epidemic that shuts a border, a broken boat, '
                     'cloud over the telescope for the whole run; field projects lose a season in perhaps one year '
                     'in six (estimate)',
            'likelier': 'fieldwork far from home, a harsh climate, unrest in the region, a short window each year (a '
                        'nesting season, a polar summer)',
            'rarer': 'work in a lab or at a desk, a long project with years to spare, settled and peaceful places'},
 'scenes': {'earth': [('',
                       "The email from the harbour master is short: the research boat's engine has failed, and the "
                       'parts will not come before October. The sampling window closes in September, and it opens '
                       'once a year.'),
                      ('W',
                       "The funder's rules allow an extension in exceptional circumstances. {N} reads the clause "
                       'twice and starts gathering the papers that prove this is one.'),
                      ('U',
                       '{N} spreads out the charts and the old data. If the boat cannot go, there must be some other '
                       'way of seeing the same water.'),
                      ('B',
                       "A whole year's budget is committed to a season that will not happen. {N} starts working out "
                       'what can be saved, sold or traded.'),
                      ('R',
                       '{N} paces the quay, looking at the water out past the harbour wall, so close it hurts. There '
                       'has to be a way out there.'),
                      ('G',
                       'The sea keeps its own calendar, and this year it has said no. {N} always knew the season was '
                       'a gift, not a promise.')]},
 'outcomes': (["The project bends but does not break, and next year's work stands on what was saved.",
               'The new plan turns out better than the old one, and {N} wonders why it was not tried first.'],
              ['The season is lost for good, and a gap opens in the record that will never be filled.',
               'The money runs out before the next window, and the project ends with half its question answered.']),
 'options': [
    ("ask the funder formally for a year's extension, with every reason documented", 'W1', None, 0.45, '', {'v': 'security, conformity', 'chance': 0.7}),
    ('rebuild the study around satellite images and old records instead', 'U1', None, 0.45, '', {'door': True, 'v': 'achievement, self-direction', 'chance': 0.6}),
    ("trade your place in the field for a share of a partner team's samples", 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.7}),
    ('go out anyway on a hired fishing boat, permit or no permit', 'R1', None, 0.45, '', {'body': 'heavy', 'mark': 'took a wild risk', 'closed': "law: sampling a protected site without the permit; backfire: the samples are seized and the fine comes in the project's name", 'v': 'stimulation', 'self_control': '-', 'chance': 0.6}),
    ('close the project well: archive what there is and hand the site on', 'G1', None, 0.45, '', {'takes': 'a research project under way', 'grants': 'project triage', 'v': 'tradition', 'chance': 0.75}),
    ('narrow the project to the one site still in reach, and guard its data', 'B.5 G.5', None, 0.5, '', {'v': 'security, achievement', 'chance': 0.85}),
    ("rewrite the question so that last year's samples can answer it", 'U.5 B.5', None, 0.5, '', {'v': 'achievement', 'chance': 0.6}),
    ('build a cheap floating sensor and send it out with a local boat', 'U.5 R.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'stimulation', 'chance': 0.45}),
    ('wait for next season, and keep the local helpers paid in the meantime', 'W.5 G.5', None, 0.5, '', {'binds': True, 'mark': 'kept your word', 'v': 'benevolence, tradition', 'self_control': '+', 'chance': 0.75}),
    ('write to every partner and fight for a berth on another ship', 'W.5 R.5', None, 0.5, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.5}),
 ]},
{'name': 'an old dataset suddenly matters',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.03, 0.04, 0.0),
 'drivers': 'era+.3 unrest+.2 community+.1 fortune+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'colleague, boss, friend, elder',
 'requires': 'a research project under way',
 'worlds': {'earth': 'data you gathered years ago suddenly matter, and everyone wants them at once'},
 'timing': {'times': 'per person with a research project under way a year: about 1 in 100 young adults, 3 in 100 '
                     'adults and 4 in 100 in midlife see data they gathered years ago suddenly matter, when a new '
                     'disease, a court case, a pollution scare or a changing climate makes the old measurements the '
                     'only baseline there is; the longer someone has kept records, the likelier it gets (estimate)',
            'likelier': 'records kept for years and documented well, a crisis or a court case nearby, a changing '
                        'climate',
            'rarer': 'a short career, data lost or never written up, a field that moves on fast'},
 'scenes': {'earth': [('',
                       'A lawyer, a reporter and a health official all ring in the same week. A factory upstream is '
                       'in court, and {Ns} ten-year-old water samples and the questionnaires from the fishing town '
                       'are the only record of what the river was like before.'),
                      ('W',
                       'The families signed consent forms ten years ago for one study, on one set of terms. {N} digs '
                       'out the box of forms before answering anyone.'),
                      ('U',
                       '{N} opens the old files and sees at once what they could show now, with methods that did not '
                       'exist back then.'),
                      ('B',
                       'Three parties want the same data, and only {N} has them. That is a position worth thinking '
                       'about carefully.'),
                      ('R',
                       '{N} remembers the fishermen who rowed out with the sample bottles every month. Their work '
                       'matters now, and {N} wants everyone to know it.'),
                      ('G',
                       'The samples sat in the freezer for ten years, like seed in a dry season. Now the rain has '
                       'come.')]},
 'outcomes': (['The old data are handled the way {N} chose, and nobody can say they were misused.',
               'Requests keep coming for years, and the dataset becomes the one everyone cites.'],
              ['The data turn out patchier than {N} remembered, and a key year is missing.',
               'The lawyers on both sides fight over the data, and {N} spends a year answering their letters.']),
 'options': [
    ('check every consent form, then reuse the data only within those terms', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, universalism', 'self_control': '+', 'chance': 0.75}),
    ('run the new analysis at once, without rereading the old consent forms', 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "approval: using people's data beyond what they agreed to; backfire: the ethics board halts the paper, and the families read about it in the newspaper", 'v': 'achievement', 'self_control': '-', 'chance': 0.85}),
    ('sell access to the cleaned, nameless data to a consultancy, at a good price', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.8}),
    ('put the water data online tonight, names stripped, for anyone to use', 'R1', None, 0.45, '', {'v': 'universalism, stimulation', 'chance': 0.85}),
    ('guard it: the data belong to the town and the river they came from', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition', 'chance': 0.7}),
    ('ring the reporters yourself, and make sure the story says whose data these are', 'B.5 R.5', None, 0.5, '', {'v': 'power, stimulation', 'chance': 0.7}),
    ('drive back to the town to tell the families their samples matter now', 'R.5 G.5', None, 0.5, '', {'v': 'benevolence', 'chance': 0.8}),
    ('clean and document it properly, so others can use it for decades', 'U.5 G.5', None, 0.5, '', {'habit': True, 'grants': 'a dataset others use', 'v': 'universalism', 'self_control': '+', 'chance': 0.7}),
    ('license it through the institute, on terms that protect the families', 'W.5 B.5', None, 0.5, '', {'v': 'security', 'chance': 0.7}),
    ('publish a proper data paper describing it, then open it to all', 'W.5 U.5', None, 0.5, '', {'grants': 'a dataset others use', 'v': 'universalism, achievement', 'chance': 0.65}),
 ]},
{'name': 'a community proposes a better question',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.3 community.3',
 'per_year': (0.0, 0.0, 0.02, 0.03, 0.03, 0.0),
 'drivers': 'community+.4 ties+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'elder, colleague, friend, boss',
 'requires': 'a research project under way | volunteer research organiser',
 'tenure': (1.0, 100.0),
 'worlds': {'earth': 'at a public meeting about your project, local people propose a better question than the one '
                     'you are asking'},
 'timing': {'times': 'per person with a research project under way, or a volunteer research organiser, of a year or '
                     'more, a year: about 2 in 100 young adults and 3 in 100 adults and people in midlife hear the '
                     'people the work is about propose a better question than the one being asked, at a public '
                     "meeting, in a letter or from the project's own volunteers; it comes far more often to projects "
                     'that work in one place with its people (estimate)',
            'likelier': 'research in a town, a farm, a school or a clinic, public meetings, volunteers in the '
                        'project, years in one place',
            'rarer': 'lab or desk work far from the people it concerns, a project that never reports back'},
 'scenes': {'earth': [('',
                       "At the village hall, after {N} presents the first results on the river's fish, {elder} "
                       'stands up at the back. The real question, {elder} says, is not how many fish there are, but '
                       'why the eels stopped coming after the weir was built.'),
                      ('W',
                       'The project has a protocol, approved and funded, with a plan for every month. But these are '
                       'the people the work is meant to serve, and {elder} has a point.'),
                      ('U',
                       '{N} feels the click of a better question landing. The weir, the eels, forty years of local '
                       'memory: it could be tested, with the right design.'),
                      ('B',
                       'The funder pays for the question in the proposal, not this one. Then again, a question the '
                       'whole valley cares about is worth something too.'),
                      ('R', '{N} wants to leap up and say yes, of course, that is the question, start tomorrow.'),
                      ('G',
                       'The old fishers have watched this river longer than any instrument. {N} feels a little '
                       'ashamed not to have asked them first.')]},
 'outcomes': (["The meeting ends with a plan everyone can live with, and the valley stays on the project's side.",
               'The meeting ends with handshakes, and a list of names who want to help.'],
              ['The funder refuses the change, and the valley feels it was not heard.',
               'The meeting turns sour, and {elder} walks out before the end.']),
 'options': [
    ('invite them onto a proper steering group, with minutes and a vote', 'W1', None, 0.45, '', {'grants': 'community listening', 'v': 'universalism, conformity', 'chance': 0.7}),
    ('explain clearly what this study can and cannot answer, and why', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'chance': 0.85}),
    ('thank them, and keep the project on the question the funder pays for', 'B1', None, 0.45, '', {'v': 'security, power', 'chance': 0.92}),
    ('throw out the old plan and start again with their question', 'R1', None, 0.45, '', {'door': True, 'v': 'stimulation', 'aims': 'participatory research coordinator', 'chance': 0.45}),
    ('share the work with the valley, and take on coordinating it with them', 'G1', None, 0.45, '', {'door': True, 'binds': True, 'title': 'participatory research coordinator', 'requires': 'research scientist', 'without': 'impossible', 'v': 'benevolence, universalism', 'chance': 0.3}),
    ('take their question, and run it as your own study without them', 'B.5 G.5', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: using a community's question without credit or consent; backfire: the valley stops letting the team onto the river", 'v': 'power, achievement', 'chance': 0.75}),
    ('spend a season listening in the valley before changing anything', 'U.5 G.5', None, 0.5, '', {'door': True, 'grants': 'community listening', 'v': 'universalism, tradition', 'self_control': '+', 'chance': 0.8}),
    ('redesign the study on the spot with them, sketching on the whiteboard together', 'U.5 R.5', None, 0.5, '', {'v': 'stimulation, universalism', 'chance': 0.7}),
    ('strike a deal: their question gets a work package if they help with sampling', 'W.5 B.5', None, 0.5, '', {'v': 'power, conformity', 'chance': 0.7}),
    ('stand up and say in front of everyone that they are right', 'W.5 R.5', None, 0.5, '', {'identity': True, 'mark': 'owned up', 'v': 'universalism', 'chance': 0.92}),
 ]},
{'name': 'whose name goes first',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.1, 0.08, 0.06, 0.0),
 'drivers': 'stress+.2 ties+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss, mentor',
 'requires': 'a research project under way',
 'worlds': {'earth': 'the paper is finished, and the team must decide whose name goes first'},
 'timing': {'times': 'per person with a research project under way a year: about 10 in 100 young adults, 8 in 100 '
                     'adults and 6 in 100 in midlife meet a real dispute over who is named first, or named at all, '
                     'on shared work; surveys find about one researcher in three has been through an authorship '
                     'dispute, most often early in a career, when names count most (estimate)',
            'likelier': 'large teams, a junior who did most of the work, a senior who expects a place, fields where '
                        'the first name decides jobs',
            'rarer': 'working alone, fields that list names alphabetically, groups with written contribution rules'},
 'scenes': {'earth': [('',
                       'The paper is finished, and only the author list is left. {colleague} did most of the '
                       'analysis, a technician kept the machine alive through the winter, {N} had the idea and found '
                       'the money, and {boss} expects a place as head of the lab.'),
                      ('W',
                       'Journals have written rules for this: who designed, who did, who wrote. {N} pulls them up '
                       'and starts filling in the boxes honestly.'),
                      ('U',
                       '{N} tries to measure it: hours, ideas, figures, pages written. However it is counted, it '
                       'does not come out as one clean order.'),
                      ('B',
                       'The first name on this paper will matter for the next grant and the next job. {N} knows it, '
                       'and so does everyone else on the list.'),
                      ('R',
                       '{N} cannot bear a fight over names after a year of good work together. It should simply be '
                       'fair, and someone should say so out loud.'),
                      ('G',
                       'In this lab the order has always gone a certain way. {N} remembers being the junior once, '
                       'and how that felt.')]},
 'outcomes': (['The list is settled, everyone signs off, and the paper goes out with no hard feelings.',
               '{colleague} reads the final order and smiles, and the next project starts on trust.'],
              ['The argument drags on for weeks, and the paper sits unsent.',
               'Someone feels cheated, and a good working friendship cools for years.']),
 'options': [
    ("follow the lab's custom and give the head of the lab the place the junior earned", 'W1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: an author order that does not match the work; backfire: the junior complains to the journal, and the list is corrected in public', 'v': 'conformity, power', 'self_control': '-', 'chance': 0.9}),
    ('write down who did what, task by task, and let the list decide', 'U1', None, 0.45, '', {'identity': True, 'grants': 'credit negotiation', 'v': 'universalism, achievement', 'chance': 0.75}),
    ('claim first place outright, on the strength of the idea and the money', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'mark': 'made an enemy', 'chance': 0.65}),
    ('fight openly for the junior who did the analysis to be named first', 'R1', None, 0.45, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'chance': 0.7}),
    ('talk it over with everyone at the lab dinner until it feels fair to all', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'chance': 0.6}),
    ('trade first place for the lead on the next paper, and shake on it', 'B.5 R.5', None, 0.5, '', {'binds': True, 'grants': 'credit negotiation', 'v': 'power, achievement', 'chance': 0.85}),
    ('take your own name off it, if that keeps the team together', 'R.5 G.5', None, 0.5, '', {'v': 'benevolence', 'chance': 0.92}),
    ("propose shared first place, with each person's part spelled out", 'U.5 B.5', None, 0.5, '', {'grants': 'credit negotiation', 'v': 'achievement', 'chance': 0.7}),
    ('add the technician as an author, since the work could not exist without them', 'W.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'universalism, benevolence', 'chance': 0.7}),
    ('bring in a written contribution policy for the whole group, from now on', 'W.5 U.5', None, 0.5, '', {'habit': True, 'binds': True, 'grants': 'credit negotiation', 'v': 'universalism, conformity', 'chance': 0.75}),
 ]},
{'name': 'a collaboration that goes unusually well',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.05, 0.06, 0.05, 0.0),
 'drivers': 'ties+.3 prosper+.2 fortune+.15',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'colleague, friend, boss',
 'requires': 'a research project under way',
 'worlds': {'earth': 'a collaboration with another team goes better than anyone expected'},
 'timing': {'times': 'per person with a research project under way a year: about 5 in 100 young adults and people in '
                     'midlife and 6 in 100 adults find a collaboration that goes unusually well, two teams whose '
                     'skills fit so the work runs faster and better than either could manage alone; most researchers '
                     'can name one or two in a working life (estimate)',
            'likelier': 'skills that complement each other, a good first meeting, money for travel, people who like '
                        'each other',
            'rarer': 'working alone, rivalry between groups, distance and no money to meet'},
 'scenes': {'earth': [('',
                       "Six months into working with {colleague}'s group in another city, the work runs faster than "
                       'either team ever managed alone. Their models and {Ns} measurements fit together like two '
                       'halves of a broken plate.'),
                      ('W',
                       '{N} is careful by nature, and this is going almost too well. Good partnerships need clear '
                       'agreements before anything goes wrong.'),
                      ('U',
                       'Every call with {colleague} ends with an idea {N} would never have had alone. {N} keeps a '
                       'notebook just for them.'),
                      ('B',
                       'Two groups together are stronger than either one. {N} can see how this could become '
                       'something funders notice, and wonders who would lead it.'),
                      ('R',
                       'The calls run late with laughter, and {N} looks forward to them all week. Work has not felt '
                       'like this for years.'),
                      ('G',
                       'It grew on its own, from one shared dataset and a chat at a conference. {N} would rather not '
                       'dig it up to see how the roots are doing.')]},
 'outcomes': (['The work doubles, the papers come, and the friendship holds.',
               'Years later, both groups still date their best work from this year.'],
              ['The partnership grows faster than anyone can manage, and small frictions start to show.',
               '{colleague} moves to a new post, and the spark goes too.']),
 'options': [
    ('put it on a sound footing: a written agreement on data, credit and duties', 'W1', None, 0.45, '', {'binds': True, 'grants': 'research collaborators', 'v': 'security, conformity', 'chance': 0.8}),
    ('spend a week in their lab to learn how they think', 'U1', None, 0.45, '', {'door': True, 'mark': 'learned a skill', 'v': 'self-direction, achievement', 'chance': 0.9}),
    ('make sure your group is the one the funders see at the centre of it', 'B1', None, 0.45, '', {'v': 'power', 'chance': 0.7}),
    ('fly the whole team over for a week of work and long dinners', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'chance': 0.85}),
    ('keep it small and easy, the way it grew, and do not force it', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.7}),
    ('turn it into a joint project on an urgent public question', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, achievement', 'chance': 0.5}),
    ('write a shared methods handbook, so the partnership outlives any one person', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'research collaborators', 'v': 'tradition, universalism', 'chance': 0.7}),
    ('invite three more labs in, and start a proper network', 'W.34 B.33 R.33', None, 0.5, '', {'door': True, 'v': 'achievement, power', 'chance': 0.65}),
    ('build a long-term partnership around the one dataset both teams depend on', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'research collaborators', 'v': 'security, achievement', 'chance': 0.75}),
    ('go and work alongside them for a season, on their ground', 'B.34 R.33 G.33', None, 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'chance': 0.8}),
 ]},
{'name': 'the instrument time you were promised',
 'stages': 'young_adult adult mature',
 'age': (20, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.12, 0.12, 0.1, 0.0),
 'drivers': 'prosper-.2 stress+.2 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss, friend, rival',
 'requires': 'instrument time',
 'worlds': {'earth': 'the time you were promised on a shared instrument goes to a bigger group'},
 'timing': {'times': 'per person with time booked on a shared instrument a year: about 12 in 100 young adults and '
                     'adults and 10 in 100 in midlife lose a promised slot (a big microscope, a sequencer, a '
                     'telescope, a research ship) to a larger group, a breakdown or a change of priorities; shared '
                     'facilities are booked well beyond what they can run, and small users are bumped first '
                     '(estimate)',
            'likelier': 'a small group, a busy facility, a large consortium in the same queue, an instrument near '
                        'the end of its life',
            'rarer': "an instrument in one's own institution, a booking paid in full, a quiet year"},
 'scenes': {'earth': [('',
                       'Two weeks before {Ns} booked week on the big microscope, an email from the facility says the '
                       'slot has gone to a large consortium with a deadline. {Ns} samples are prepared, labelled and '
                       'waiting in the freezer.'),
                      ('W',
                       'The booking was confirmed in writing, months ago, through the proper process. {N} rereads '
                       "the confirmation, then the facility's rules on cancellations."),
                      ('U',
                       '{N} starts listing other ways to get the same measurement: a smaller machine, a different '
                       'method, a longer run somewhere else.'),
                      ('B',
                       'The consortium has forty names and a great deal of money. {N} has samples they might want, '
                       'and that is something to bargain with.'),
                      ('R',
                       '{N} is out of the chair before reaching the end of the email, already halfway to the '
                       'facility office.'),
                      ('G',
                       'Big groups have always gone first in this building. {N} looks at the samples in the freezer, '
                       'which will keep, and at the calendar, which will turn.')]},
 'outcomes': (['The samples get measured, one way or another, and the project keeps to its timetable.',
               'The facility apologises, and the next booking comes with a guarantee in writing.'],
              ['The slot is gone, the next free week is in the spring, and the project slips half a year.',
               'Tempers fray in the facility office, and {N} is quietly moved down the list.']),
 'options': [
    ('appeal to the booking committee, with the written confirmation attached', 'W1', None, 0.45, '', {'takes_if_fails': 'instrument time', 'v': 'conformity, security', 'chance': 0.55}),
    ('redesign the experiment to run on the older machine down the corridor', 'U1', None, 0.45, '', {'takes': 'instrument time', 'mark': 'learned a skill', 'v': 'achievement', 'chance': 0.7}),
    ('offer the big group a share of the data in exchange for half the slot', 'B1', None, 0.45, '', {'door': True, 'takes_if_fails': 'instrument time', 'v': 'power', 'chance': 0.65}),
    ('come in at night and run the samples on the machine anyway', 'R1', None, 0.45, '', {'takes': 'instrument time', 'mark': 'hid a wrong', 'closed': 'approval: using the instrument without a booking; backfire: the facility bans the whole group for a month', 'v': 'self-direction, stimulation', 'self_control': '-', 'chance': 0.65}),
    ('wait for the next round, and use the months to prepare better samples', 'G1', None, 0.45, '', {'takes': 'instrument time', 'v': 'security, tradition', 'self_control': '+', 'chance': 0.75}),
    ('take it to the facility board as a question of fair rules for small groups', 'W.34 U.33 B.33', None, 0.5, '', {'identity': True, 'takes_if_fails': 'instrument time', 'v': 'universalism, power', 'chance': 0.45}),
    ('ring a friend who runs the same machine in another city and ask a favour', 'W.34 R.33 G.33', None, 0.5, '', {'door': True, 'takes': 'instrument time', 'v': 'benevolence', 'chance': 0.7}),
    ('accept the change gracefully, and get a written promise of priority next time', 'W.34 B.33 G.33', None, 0.5, '', {'takes': 'instrument time', 'v': 'security', 'chance': 0.8}),
    ('build a makeshift rig from parts in the workshop and get rough data', 'U.34 R.33 G.33', None, 0.5, '', {'door': True, 'takes': 'instrument time', 'mark': 'learned a skill', 'v': 'self-direction, stimulation', 'chance': 0.5}),
    ("march into the facility manager's office and argue the slot back", 'U.34 B.33 R.33', None, 0.5, '', {'takes_if_fails': 'instrument time', 'v': 'power, achievement', 'chance': 0.45}),
 ]},
{'name': 'a finding that makes the news',
 'stages': 'adult mature elder',
 'age': (28, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.03, 0.015),
 'drivers': 'era+.3 fortune+.15',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'colleague, boss, partner, friend',
 'requires': 'published research',
 'worlds': {'earth': 'a finding of yours makes the national news, and the press calls'},
 'timing': {'times': 'per person with published research a year: about 3 in 100 adults and people in midlife and 1.5 '
                     'in 100 elders see a finding of theirs taken up by the national news, reporters ringing and '
                     'producers asking for interviews; most such stories last a week, and only a few in a hundred '
                     "make the researcher's own name known across the country (estimate)",
            'likelier': 'a finding about health, food, animals, space or the climate, a press office that pushes it, '
                        'a slow news week, a public argument the finding touches',
            'rarer': 'technical work far from daily life, a field the press rarely covers, a busy news week'},
 'scenes': {'earth': [('',
                       'A national paper runs {Ns} finding on page three, and by ten in the morning the phone has '
                       'not stopped. A radio producer, two reporters and a breakfast television show all want {N}, '
                       'today.'),
                      ('W',
                       '{N} thinks of the people who will hear this over breakfast, and of the duty to tell them '
                       "only what is true. The institute's media guidelines are in the drawer."),
                      ('U',
                       '{N} winces at the headline, which says more than the study did. The interesting part, the '
                       'part the reporter missed, is far more subtle.'),
                      ('B',
                       'Attention like this comes once in a career, if at all. {N} can feel how much it could open, '
                       'and how fast it will fade.'),
                      ('R',
                       '{N} is lit up: people care about this, ordinary people at their kitchen tables. {N} wants to '
                       'tell them everything.'),
                      ('G',
                       '{N} watches the fuss from a little distance. News blows through like wind; the work took '
                       'years to make and will take years to settle.')]},
 'outcomes': (['The finding reaches the public the way it deserves, and the right people get in touch.',
               'Weeks later strangers mention the interview, and the field takes notice of {N}.'],
              ['The story is garbled in the edit, and {N} winces at every clip.',
               'The attention dies within a week, and the one interview that mattered never happens.']),
 'options': [
    ('give one careful interview, and insist on checking every quote before it runs', 'W1', None, 0.45, '', {'grants': 'explaining science', 'v': 'universalism, conformity', 'chance': 0.55}),
    ('send the reporter a one-page note on what the finding does and does not mean', 'U1', None, 0.45, '', {'v': 'universalism', 'chance': 0.75}),
    ('say yes to every programme that calls, while the interest lasts', 'B1', None, 0.45, '', {'habit': True, 'v': 'power, achievement', 'chance': 0.9}),
    ('go on the breakfast show and let the excitement show', 'R1', None, 0.45, '', {'grants': 'explaining science', 'v': 'stimulation', 'chance': 0.9}),
    ('take the reporter out to the field site, and let the place tell the story', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'chance': 0.6}),
    ('write a piece for a national paper that explains the uncertainty honestly', 'W.34 U.33 R.33', None, 0.5, '', {'grants': 'explaining science', 'v': 'universalism, stimulation', 'chance': 0.6}),
    ('turn the reporters away politely, and send them to a colleague who knows more', 'W.34 U.33 G.33', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence, universalism', 'chance': 0.92}),
    ("let the press office's bolder headline stand, because the institute wants it", 'W.34 B.33 G.33', None, 0.5, '', {'mark': 'gave in to pressure', 'closed': 'approval: a headline that claims more than the paper; backfire: colleagues write a public letter correcting it', 'v': 'security, conformity', 'self_control': '-', 'chance': 0.8}),
    ('turn the attention into a book proposal and a lecture tour', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'known across the country', 'v': 'achievement, power', 'chance': 0.15}),
    ('lead a public campaign for the place the finding is about', 'B.34 R.33 G.33', None, 0.5, '', {'identity': True, 'grants': 'known across the country', 'v': 'power, universalism', 'chance': 0.15}),
 ]},
{'name': "a rival's result contradicts yours",
 'stages': 'adult mature elder',
 'age': (28, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.03, 0.01),
 'drivers': 'era+.2 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'rival, colleague, mentor',
 'requires': 'published research',
 'worlds': {'earth': 'a rival group publishes a result that says your best-known finding is wrong'},
 'timing': {'times': 'per person with published research a year: about 3 in 100 adults and people in midlife and 1 '
                     'in 100 elders see a rival group publish a result that contradicts one of theirs; large '
                     'replication projects in several fields have repeated only about half of the published findings '
                     'they tried, so most people who publish for many years meet such a challenge (estimate)',
            'likelier': 'a well-known finding, a crowded field, small samples in the original work, a rival group on '
                        'the same question',
            'rarer': 'a quiet corner of a field, findings already repeated many times, work nobody else can afford '
                     'to repeat'},
 'scenes': {'earth': [('',
                       "The new issue of the journal has a paper from {rival}'s group, and its title says, in "
                       'effect, that {Ns} best-known finding does not hold. Colleagues have already started '
                       'forwarding it, with question marks.'),
                      ('W',
                       'There is a proper way to settle this: the evidence laid out in the open and judged by people '
                       'with no stake in either side. {N} believes in that way, even now.'),
                      ('U',
                       '{N} reads the methods section twice, slowly. Somewhere in it is the difference between the '
                       'two studies, and finding it matters more than winning.'),
                      ('B',
                       '{rival} has wanted this for years. {N} feels the challenge like a shove in a crowd, and has '
                       'no intention of stepping aside.'),
                      ('R',
                       '{Ns} pulse is up before the abstract is finished. It feels personal, and part of {N} wants '
                       'to pick up the phone right now.'),
                      ('G',
                       'Findings are like trees: some stand for a century, some fall in the first storm. {N} has '
                       'seen both, and waits to see which this one is.')]},
 'outcomes': (['The question is settled in the open, and {Ns} standing in the field survives it, or grows.',
               'The two groups work out why their results differ, and the field moves forward.'],
              ['The dispute turns ugly in public, and neither side comes out of it well.',
               'The original finding does not hold, and {N} has to watch it fall in front of everyone.']),
 'options': [
    ('ask an independent lab to repeat both studies, and accept what it finds', 'W1', None, 0.45, '', {'grants': 'a finding that held up', 'v': 'universalism, conformity', 'chance': 0.5}),
    ('repeat your own experiment step by step, with their method alongside', 'U1', None, 0.45, '', {'grants': 'a finding that held up', 'v': 'achievement, universalism', 'chance': 0.6}),
    ('publish a sharp reply that takes their methods apart', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'mark': 'made an enemy', 'chance': 0.7}),
    ('ring the rival and suggest settling it together, at one bench', 'R1', None, 0.45, '', {'grants': 'research collaborators', 'v': 'stimulation, benevolence', 'chance': 0.55}),
    ('let time decide: good findings last, and weak ones fade', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.6}),
    ('propose a joint replication with the rival, its plan registered in advance', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'a finding that held up', 'v': 'universalism, achievement', 'chance': 0.45}),
    ('concede in public that their result is the stronger one, and thank them', 'W.34 R.33 G.33', None, 0.5, '', {'identity': True, 'mark': 'owned up', 'v': 'universalism, benevolence', 'chance': 0.92}),
    ('rally the co-authors and answer in one strong joint letter', 'W.34 B.33 R.33', None, 0.5, '', {'v': 'power, conformity', 'chance': 0.7}),
    ('go back to the original site and look again with fresh eyes', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'a nose for the odd result', 'v': 'self-direction, stimulation', 'chance': 0.65}),
    ("accept the journal's request to review their next paper, and pick it apart", 'U.34 B.33 G.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': "approval: reviewing a rival's work without declaring the conflict; backfire: the editor finds out, and both groups' papers are pulled for review", 'v': 'power', 'chance': 0.75}),
 ]},
{'name': 'a discovery nobody asked you for',
 'stages': 'young_adult adult mature elder',
 'age': (25, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.002, 0.003, 0.003, 0.002),
 'drivers': 'fortune+.2 era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning, nature',
 'horizon': 'years',
 'roles': 'mentor, friend, partner, rival, colleague',
 'requires': 'research scientist | research assistant | citizen scientist | community observer | volunteer research '
             'organiser',
 'tenure': (2.0, 70.0),
 'worlds': {'earth': 'after years of careful watching, something you found on your own looks new to science, and '
                     'nobody asked you for it',
            'tribal': "after many summers of watching, you find something the elders' lore has no name for, and "
                      'nobody asked you to look',
            'magic': "after years of keeping your notebooks, you find something the Academy's books do not hold, and "
                     'no master asked you to look'},
 'timing': {'times': 'per person with years of research practice a year (a research scientist or assistant, or a '
                     'volunteer observer of five years or more with a publication): perhaps 1 in 300 comes upon '
                     'something outside their own project that looks new to science (a comet or a variable star, a '
                     'species far outside its known range, a pattern in old parish or weather records) and thinks of '
                     'claiming it (estimate); amateurs still find some new comets and many bright novae each year, '
                     'and amateur co-authors appear on a few papers in 100 in astronomy and natural history '
                     "(estimate); turning such a find into research in one's own name, with money and a post, comes "
                     'to perhaps 1 claimant in 25 who already has a publication record (estimate); a first find more '
                     'often ends as a co-authored note',
            'likelier': 'years of patient records, a good instrument, a mentor in the field, savings or a patron, a '
                        'time when the field is hungry for data',
            'rarer': 'no time to spare, a find nobody can check, a field with no money for newcomers',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'It started as a note in the margin of a record {N} has kept for years: a light where none '
                       'should be, a beetle far from home, a column of old figures that will not add up. Three '
                       'checks later it is still there, and as far as {N} can find, nobody in the field has seen '
                       'it.'),
                      ('W',
                       "{N} has kept the records for years by the project's rules, every date and every reading in "
                       'its place. That is exactly why this one entry cannot be waved away.'),
                      ('U',
                       '{N} has read everything published on it twice. Either the find is new, or the whole field '
                       'has missed the same thing for years, and both possibilities are thrilling.'),
                      ('B',
                       "A find like this could be a name, a post, a life of one's own. {N} knows that whoever claims "
                       'it first, and claims it well, is the one who will be remembered.'),
                      ('R',
                       '{N} cannot sleep. The find sits there like a door left open, and every part of {N} wants to '
                       'run through it.'),
                      ('G',
                       'It turned up in the same field, the same river, the same patch of sky {N} has watched for '
                       'years. The place gave it up after long acquaintance, and it feels like a gift.')],
            'tribal': [('',
                        "The elders' lore has a name for every plant on the hill but this one, and {N} has walked "
                        'that hill for twenty summers. The old women say it eases a fever. At the fire people begin '
                        'to wonder whether {N} should go and learn its ways, and be fed by the band for the '
                        'learning.')],
            'magic': [('',
                       "The star {N} has charted for many winters moves where the Academy's tables say no star "
                       "should be. No master has asked a hedge-watcher's opinion, but {N} already has a note in the "
                       "Academy's proceedings, and the purse for free scholars closes at midsummer.")]},
 'outcomes': (['The answer, when it comes, is yes, and {N} reads it standing up in the kitchen, twice.',
               'People who know the field take the find seriously, and {Ns} name goes on it where {N} wanted it.'],
              ['The letter is kind and short: the find is real and carefully observed, but the money goes to a '
               'project already running. One sentence calls the case the best the panel read from outside a big lab, '
               'and {N} reads that sentence many times.',
               '{N} presents it anyway, to nine people and a tired chair at the end of a long day; one of them asks '
               'a very good question, and nobody writes back afterwards.']),
 'options': [
    ("write the find up to the field's standard, every check shown, and apply for a fellowship", 'W1', None, 0.45, '', {'title': 'independent investigator', 'grants': 'a research project under way', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, achievement', 'world': {'tribal': "bring the find to the elders' circle in the proper way, and ask to be fed while you learn it", 'magic': "present the find to the Academy by every form, and petition for a free scholar's purse"}, 'chance': 0.04}),
    ('build a case no panel can wave away, and ask for money in your own name', 'U1', None, 0.45, '', {'title': 'independent investigator', 'grants': 'a research project under way', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': "learn the plant's ways through a whole year of moons before asking the elders for anything", 'magic': 'chart the star through a whole winter, and petition with tables no master can fault'}, 'chance': 0.04}),
    ('put the find before the one professor whose word opens doors, and ask for backing', 'B1', None, 0.45, '', {'title': 'independent investigator', 'grants': 'a research project under way', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': 'take the find first to the eldest healer, whose word the whole band follows, and ask her backing', 'magic': 'show the find first to the one master whose seal opens every door, and ask for patronage'}, 'chance': 0.04}),
    ('go after it full time on your own savings, sure the results will carry you', 'R1', None, 0.45, '', {'act': 'go after it full time on their own savings, sure the results will carry them', 'title': 'independent investigator', 'grants': 'a research project under way', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'binds': True, 'v': 'stimulation', 'world': {'tribal': 'leave the hunt and go alone into the hills to learn it, trusting the band to feed you after', 'magic': 'give up your post, buy a better lens with your savings, and chase the star every night'}, 'chance': 0.04}),
    ('let the club, the village and the old volunteers back you as their own researcher', 'G1', None, 0.45, '', {'act': 'let the club, the village and the old volunteers back them as their own researcher', 'title': 'independent investigator', 'grants': 'a research project under way', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'let your own hearths speak for you at the fire, as the one of theirs who should learn it', 'magic': 'let your guild and your street put up a purse, so one of their own can study it'}, 'chance': 0.04}),
    ('make the find the heart of a new volunteer survey, and run it yourself', 'B.5 G.5', None, 0.5, '', {'title': 'volunteer research organiser', 'habit': True, 'door': True, 'v': 'power, tradition', 'world': {'tribal': 'gather the young watchers of the band to keep count of the new plant, and lead them', 'magic': 'found a circle of lay correspondents to watch the star, and keep its rolls yourself'}, 'chance': 0.8}),
    ('chase it as your own project, every evening and weekend, and see where it goes', 'B.5 R.5', None, 0.5, '', {'grants': 'a research project under way', 'v': 'self-direction, achievement', 'world': {'tribal': 'go up the hill every spare day to learn the plant, and see where it leads', 'magic': 'turn the attic into a study for the star, every spare night, and see where it leads'}, 'chance': 0.8}),
    ('add the find to the long record, and keep watching the same place', 'U.5 G.5', None, 0.5, '', {'title': 'community observer', 'v': 'universalism, tradition', 'world': {'tribal': "add the plant to the band's long memory of the hill, and keep walking the same path", 'magic': 'enter the star in your own long ledger of the sky, and keep the same watch each night'}, 'chance': 0.85}),
    ('hand every note to the specialists who study it, and cheer when they confirm it', 'W.5 R.5', None, 0.5, '', {'grants': 'research collaborators', 'mark': 'made a friend', 'v': 'universalism, benevolence', 'world': {'tribal': "give all you know of the plant to the band's healers, and cheer when it works", 'magic': "send every note to the Academy's masters, and cheer when they confirm it"}, 'chance': 0.85}),
    ('write it up as a short note with a professional, your name second', 'W.5 U.5', None, 0.5, '', {'grants': 'published research', 'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'teach it to the healers carefully, so your name is sung after theirs', 'magic': 'write it up with a master of the Academy, your name second in the proceedings'}, 'chance': 0.75}),
 ]},
{'name': 'a group of your own, open to all comers',
 'stages': 'young_adult adult mature',
 'age': (30, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.015, 0.02, 0.015, 0.0),
 'drivers': 'prosper+.3 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, rival, partner',
 'requires': 'research scientist | postdoctoral researcher',
 'tenure': (4.0, 45.0),
 'worlds': {'earth': 'a new institute hires group leaders from anywhere, and your grant and your years would let you '
                     'apply',
            'tribal': 'the keeper of the lore-circle steps down, and any watcher of long standing may ask for the '
                      'place',
            'magic': 'the Academy opens a new workshop, and any scholar of long standing with a purse may petition '
                     'to be its master'},
 'timing': {'times': 'per research scientist of four years or more with a grant in hand, a year: perhaps 1 in 30 '
                     'sees a group-leader post advertised at another institution and could apply (estimate); such a '
                     'post draws about 100 to 300 applications, 5 to 8 are interviewed and one is appointed '
                     '(estimate from advertising figures); most group leaders first lead a project or hold a '
                     'fellowship of their own, and a scientist who skips that step is appointed perhaps 1 time in 25 '
                     'even with a grant (estimate); in the life sciences about 1 doctorate in 6 to 10 leads a group '
                     'of their own ten years on (national surveys of doctorate holders, estimate)',
            'likelier': "papers others cite, a mentor's backing, a boom in research money, a new institute hiring, "
                        'years of supervising students',
            'rarer': "hard times for research money, years on other people's projects, a career break still showing "
                     'on the record',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The advertisement is one page long: a new institute, five posts for group leaders, open to '
                       "researchers from anywhere, with a research plan, a record and money of one's own. {N} has "
                       'the grant and the years, if not yet a project led, reads it on a Sunday and keeps coming '
                       'back to it all week.'),
                      ('W',
                       'The criteria are printed in a box at the bottom of the page. {N} goes through them one by '
                       'one, ticking what is there and circling what is not.'),
                      ('U',
                       '{N} has carried the plan around for years: the question, the first three experiments, the '
                       'one result that would change the field. Here, at last, is a page that asks for it.'),
                      ('B',
                       'Five posts and a few hundred applicants. {N} starts listing who sits on the panel, who '
                       'trained whom, and who owes {N} a favour.'),
                      ('R',
                       "{N} reads it and feels the old fire: a lab, a group, a question of one's own. The odds are "
                       "somebody else's problem."),
                      ('G',
                       '{N} thinks of the people already working side by side: the technician, the two students, the '
                       "friend from the next lab. A group of one's own would be them, together, and that is worth "
                       'asking for.')],
            'tribal': [('',
                        'The keeper of the lore-circle is too old now to climb the watching hill. The elders say any '
                        'watcher of long standing may ask for the place at the next full moon, and some of them look '
                        'at {N}, who has watched for many winters.')],
            'magic': [('',
                       "A notice on the Academy's gate: a new workshop, with rooms, a furnace and three apprentices, "
                       'for a scholar of long standing with the best plan and a purse to bring. {N} reads it twice '
                       'on the way past.')]},
 'outcomes': (['The phone call comes on a Thursday afternoon, and {N} has to sit down to hear the rest of it.',
               'The plan is read the way {N} hoped, and the next years take the shape {N} chose.'],
              ["{N} comes sixth of six at the interviews. The chair's letter says the plan was the most original the "
               'panel read, and that the post went to someone who had already led a project of their own.',
               'The answer arrives as a form email with a reference number, and {N} walks home the long way, past '
               "the institute's lit windows."]),
 'options': [
    ('apply by the book: every form, every reference, a five-year plan the panel can check', 'W1', None, 0.45, '', {'title': 'research group leader', 'requires': 'research grant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'conformity, achievement', 'world': {'tribal': 'ask for the place at the full moon in the proper way, with two elders to speak for you', 'magic': "petition by every form of the Academy, with two masters' seals and a five-year plan"}, 'chance': 0.04}),
    ('write the research plan of a lifetime, and let the science make the case', 'U1', None, 0.45, '', {'title': 'research group leader', 'requires': 'research grant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'show the elders the whole teaching you would give the young watchers, season by season', 'magic': 'make the treatise of your life your petition, and let the learning make the case'}, 'chance': 0.04}),
    ("get the institute's director to read your plan over dinner, before the panel meets", 'B1', None, 0.45, '', {'title': 'research group leader', 'requires': 'research grant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': "win the eldest's ear over a gift of meat before the circle meets", 'magic': "dine with the Academy's provost before the petitions are opened, and leave your plan on the table"}, 'chance': 0.04}),
    ('turn up at the institute unannounced with the plan, and ask to see the director', 'R1', None, 0.45, '', {'title': 'research group leader', 'requires': 'research grant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'climb the watching hill at dawn and start teaching the young ones before anyone has said yes', 'magic': "walk into the Academy's council hall with the plan under your arm, and ask to be heard"}, 'chance': 0.04}),
    ('apply with the whole team named in the plan, the people who would come with you', 'G1', None, 0.45, '', {'act': 'apply with the whole team named in the plan, the people who would come with them', 'title': 'research group leader', 'requires': 'research grant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'ask for the place with the young watchers you already teach standing beside you', 'magic': "petition with your journeymen's names written on the scroll beside yours"}, 'chance': 0.04}),
    ("back a friend's application instead, and offer to be the first to join their group", 'R.5 G.5', None, 0.5, '', {'mark': 'made a friend', 'door': True, 'v': 'benevolence, stimulation', 'world': {'tribal': 'stand behind a friend who asks for the place, and offer to be the first watcher in the circle', 'magic': "back a friend's petition, and offer to be the first journeyman in the workshop"}, 'chance': 0.8}),
    ('ask the panel what a winning application needs, and plan the next round around it', 'U.5 B.5', None, 0.5, '', {'aims': 'research group leader', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'ask the elders what the next keeper must bring, and spend the year getting it', 'magic': 'ask the provost what wins a workshop, and spend the year preparing for the next opening'}, 'chance': 0.8}),
    ('take the plan to a smaller institute that wants a project led, not a group', 'U.5 R.5', None, 0.5, '', {'title': 'research project lead', 'requires': 'research grant', 'without': 'impossible', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': "offer to lead one season's watching for a smaller band that asks", 'magic': 'take the plan to a lesser college that wants one project led, not a workshop'}, 'chance': 0.75}),
    ('use the application to win a permanent contract where you are', 'W.5 B.5', None, 0.5, '', {'v': 'security', 'world': {'tribal': 'let the band see you were asked about, and win a surer place at your own fire', 'magic': 'let your own master hear of the petition, and win a sealed contract where you are'}, 'chance': 0.75}),
    ('let this one pass: the work and the people already there are enough for now', 'W.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'v': 'security, tradition', 'world': {'tribal': 'let this one pass, and keep watching with the people you know', 'magic': 'leave the petition unwritten, and stay with your own bench and your own people'}, 'chance': 0.8}),
 ]},
{'name': 'a facility looks outside for its next head',
 'stages': 'young_adult adult mature',
 'age': (30, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.003, 0.005, 0.005, 0.0),
 'drivers': 'prosper+.2 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor, rival, friend',
 'requires': 'laboratory technician | research scientist',
 'tenure': (4.0, 45.0),
 'worlds': {'earth': 'a research facility elsewhere looks outside for its next head, and you have kept such machines '
                     'running for years',
            'tribal': "the keeper of a far band's sighting stones can no longer climb to them, and they ask who else "
                      "can read the sun's turnings",
            'magic': "another city's great orrery needs a new keeper, and for once the post is cried in the market "
                     'as well as the halls'},
 'timing': {'times': 'per laboratory technician or research scientist of four years or more at the bench, a year: '
                     'perhaps 1 in 200 sees a head-of-facility post advertised outside their own institution and '
                     'could apply (estimate); a shared facility changes its head about once in 10 to 20 years, and '
                     'most posts go to a deputy or a long-serving technician inside; an outside applicant with the '
                     'right record is appointed perhaps 1 time in 20 (estimate)',
            'likelier': 'years of keeping difficult machines running, a name among the people who use them, a '
                        'facility in trouble that wants fresh hands',
            'rarer': 'a deputy who has waited years for the post, an institution that never hires from outside',
            'gap_years': (5.0, 12.0)},
 'scenes': {'earth': [('',
                       "The post is advertised in the trade press and on another institute's pages: head of a shared "
                       'facility, its instruments booked by forty groups, its old head retiring. Applicants from '
                       'outside are welcome, it says, and {N}, who has kept machines like these running for years, '
                       'cannot stop reading the list.'),
                      ('W',
                       '{N} has kept every service log for years, signed and dated, and knows what it takes to keep '
                       'a machine honest for the people who rely on it. The advertisement asks for exactly that, in '
                       'other words.'),
                      ('U',
                       '{N} reads the instrument list and starts working out, almost without meaning to, what each '
                       'machine could measure that nobody has asked of it yet.'),
                      ('B',
                       'A facility is power of a quiet kind: every group in the building needs a slot, and the head '
                       'decides who gets one. {N} notices that, and notices that the post went out a week before '
                       'anyone expected.'),
                      ('R',
                       '{N} knows machines like these down to the last valve, but not these exact ones, and that is '
                       'the best part. The thought of learning them from the inside makes {Ns} hands itch.'),
                      ('G',
                       'The old head ran the place for twenty-six years and knew every user by name. {N} could see '
                       'keeping it that way, a workshop where everyone is welcome and nothing useful is thrown '
                       'away.')],
            'tribal': [('',
                        "The keeper of a neighbouring band's sighting stones can no longer climb to them, and that "
                        'band must know when the sun turns. Word comes asking who else has watched stones long '
                        'enough, and {N} has watched the home stones for many winters.')],
            'magic': [('',
                       'A crier reads the notice in the square: the great orrery of the river city needs a keeper, '
                       'and any who can tend its wheels and lenses may apply at the tower door. {N} has kept the '
                       "home Academy's lesser clocks true for years.")]},
 'outcomes': (["The board rings on a Friday: the keys are {Ns} from the first of the month, and so are forty groups' "
               'worth of problems.',
               'The choice turns out well, and within a year {N} knows every sound the machines make.'],
              ["The post goes to the deputy who has waited eleven years for it. The panel's letter says {Ns} plan "
               'for the instruments was the most interesting they heard, and that the deputy has been asked to read '
               'it.',
               '{N} is shown round the machine room, asks good questions, and hears nothing for six weeks; then a '
               'two-line email, and the long drive home is spent going over every answer.']),
 'options': [
    ('apply with a full record of every machine you have kept running, every log attached', 'W1', None, 0.45, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': 'go to the elders with every turning of the sun you have marked, and ask for the stones', 'magic': 'apply at the tower door with a ledger of every clock and lens you have kept true'}, 'chance': 0.05}),
    ('show the panel what the machines could measure that nobody has tried yet', 'U1', None, 0.45, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'show the elders a turning of the sky the stones could mark that nobody has marked yet', 'magic': 'show the masters a motion the orrery could reckon that nobody has set it to'}, 'chance': 0.05}),
    ('get the retiring head to name you as the one to follow, before the interviews', 'B1', None, 0.45, '', {'act': 'get the retiring head to name them as the one to follow, before the interviews', 'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': "win the old keeper's blessing before the elders meet, so the stones pass to you", 'magic': "win the old keeper's word to the provost, so the keys pass to you"}, 'chance': 0.05}),
    ('ask to run the main instrument for a day, and let the results speak', 'R1', None, 0.45, '', {'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, achievement', 'world': {'tribal': 'climb to the stones at the turning and mark it truly before anyone asks', 'magic': 'ask to run the orrery for one night, and let the masters find it true in the morning'}, 'chance': 0.05}),
    ('apply with the users behind you: the students and groups who come to you for help', 'G1', None, 0.45, '', {'act': 'apply with the users behind them: the students and groups who come to them for help', 'title': 'research facility lead', 'requires': 'lab work', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'ask for the stones with the families you mark the seasons for standing behind you', 'magic': 'apply with the scholars and apprentices you have helped standing behind you'}, 'chance': 0.05}),
    ('stay with the machines you know, and become the one the new head cannot manage without', 'B.5 G.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'keep your own watch, and become the one the new keeper must ask', 'magic': 'stay at your own bench, and become the one the new keeper must send for'}, 'chance': 0.8}),
    ('take the better-paid job at the firm that builds the machines instead', 'B.5 R.5', None, 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': 'go to the flint-traders who make the best tools, and learn their trade instead', 'magic': "take service with the instrument-makers' guild, for better pay"}, 'chance': 0.75}),
    ('spend a winter learning the instrument from the inside, ready for the next opening', 'U.5 R.5', None, 0.5, '', {'aims': 'research facility lead', 'mark': 'learned a skill', 'habit': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'spend the winter at the stones beside the old keeper, learning every mark', 'magic': 'spend the winter inside the orrery with its old keeper, learning every wheel'}, 'chance': 0.8}),
    ('recommend the long-serving technician who knows the place best, and say why', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': "speak at the fire for the old keeper's helper, who has climbed with him for years", 'magic': "speak to the provost for the orrery's old journeyman, who has tended it for years"}, 'chance': 0.8}),
    ("take the deputy head's post instead, and learn the job beside whoever is chosen", 'W.5 U.5', None, 0.5, '', {'grants': 'trusted with the keys', 'habit': True, 'v': 'security, achievement', 'world': {'tribal': "ask to carry the old keeper's marks and tend the stones, under whoever is chosen", 'magic': "ask to be the orrery's under-keeper, beside whoever is chosen"}, 'chance': 0.75}),
 ]},
{'name': 'a search for a new voice for science',
 'stages': 'young_adult adult mature elder',
 'age': (23, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.006, 0.006, 0.004, 0.002),
 'drivers': 'era+.2 fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'friend, partner, colleague, mentor, rival',
 'requires': 'explaining science',
 'tenure': (3.0, 70.0),
 'worlds': {'earth': 'a broadcaster and a science museum look for a new voice for science, and your years of talks '
                     'fit what they ask',
            'tribal': 'the great gathering will choose a new teller of what the watchers have learned, and your '
                      'tellings are known at many fires',
            'magic': 'the Academy seeks a new lecturer for the market square, and your back-room lectures have been '
                     'talked about for years'},
 'timing': {'times': 'per person who has explained science in public for three years or more, with research, science '
                     'reporting or teaching behind them, a year: perhaps 1 in 150 sees a search for a science '
                     "presenter, a museum's public voice or a broadcaster's science desk and answers it (estimate); "
                     'such searches draw from dozens to a few thousand entries, most from people with no record; '
                     'someone with years of talks and a research, reporting or teaching background is shortlisted '
                     'perhaps 1 time in 5 and chosen about 1 time in 20 (estimate)',
            'likelier': "a gift for explaining, a following of one's own, a film or a talk that did well, a time "
                        'when broadcasters want new faces',
            'rarer': 'shyness, no time, a field that rarely makes the news',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'The notice runs for a week: a broadcaster and a science museum want a new voice for science, '
                       'and ask for a two-minute film explaining one idea, from people who already explain science '
                       'to the public. {N} has given talks for years, watches the advertisement twice and starts, '
                       'without quite deciding to, to choose the idea.'),
                      ('W',
                       'The rules are precise: two minutes, one idea, no music, a signed form. {N} prints them, '
                       'because a fair contest is one where everyone sends the same thing.'),
                      ('U',
                       'The hard part is not the camera; it is choosing an idea that can be made clear in two '
                       'minutes without one false word. {N} has been working on that problem for years without '
                       'knowing it.'),
                      ('B',
                       'Many will apply, and the one chosen will be someone the producers have already heard of. {N} '
                       'starts thinking about who might mention {Ns} name to them.'),
                      ('R',
                       '{N} has explained this stuff at every party for years, waving a fork, and people stay to '
                       'listen. Why not on a real screen?'),
                      ('G',
                       '{Ns} students, neighbours and the regulars at the library talks already call {N} the one who '
                       'makes science make sense, and half of them have sent {N} the notice.')],
            'tribal': [('',
                        'At the gathering a new teller will be chosen, the one who carries what the watchers learned '
                        "from fire to fire. {N} has told the watchers' findings at many fires for years, and the "
                        'bands will cheer for the one they want.')],
            'magic': [('',
                       'A herald reads it in the square: the Academy wants a lecturer for market days, someone to '
                       'make the new wonders plain to porters and fishwives alike. {N} has lectured in tavern back '
                       'rooms for years; the trial is on the steps, on the first day of spring.')]},
 'outcomes': (['The phone rings on a wet Tuesday: the producers loved the film, and could {N} come in on Monday?',
               'The voice finds its room, and people who never cared for science stay to listen to {N}.'],
              ['The email thanks {N} for one of several hundred entries and says the standard was very high. A week '
               'later a producer writes, unasked, that {Ns} film made the whole office laugh and learn something, '
               'and that it nearly made the last three.',
               '{N} watches the first episode with someone else presenting it, says the new face is quite good, and '
               'goes to bed early.']),
 'options': [
    ('send in the film and the form exactly as the rules ask, on the first day', 'W1', None, 0.45, '', {'title': 'science communication specialist', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, achievement', 'world': {'tribal': 'stand up at the fire when the elders call, and tell one thing in the old order', 'magic': 'present yourself on the steps at the first bell, the lecture written out as the notice asked'}, 'chance': 0.05}),
    ('spend a month on the clearest two minutes anyone has made about one idea', 'U1', None, 0.45, '', {'title': 'science communication specialist', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'spend a moon shaping one teaching so clear a child could carry it home', 'magic': 'spend a month polishing one lecture until not a word in it is false'}, 'chance': 0.05}),
    ('ask a producer met once at a talk to move the film to the top', 'B1', None, 0.45, '', {'title': 'science communication specialist', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'ask the singer who owes you a favour to name you to the elders first', 'magic': 'ask a clerk of the Academy who owes you a favour to set your name first on the list'}, 'chance': 0.05}),
    ('turn up at the audition with a kitchen experiment that fizzes and foams', 'R1', None, 0.45, '', {'title': 'science communication specialist', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, hedonism', 'world': {'tribal': 'leap up at the fire unbidden and show the bands how the stones mark the sun', 'magic': 'push to the front of the steps with a flask that changes colour, and start talking'}, 'chance': 0.05}),
    ('send the film the people you teach made of you at work, in your own place', 'G1', None, 0.45, '', {'act': 'send the film the people they teach made of them at work, in their own place', 'title': 'science communication specialist', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'let the families of your own fire stand up and say why it should be you', 'magic': 'let your neighbours walk with you to the steps, and speak for you before you begin'}, 'chance': 0.05}),
    ('start a monthly science night at the local pub or library instead', 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'habit': True, 'v': 'stimulation, benevolence', 'world': {'tribal': 'light a small fire of your own once a moon, where anyone may ask what the watchers have seen', 'magic': 'start a monthly lecture in the back room of the tavern, for whoever comes'}, 'chance': 0.8}),
    ('start a channel of your own, and build an audience the slow way', 'U.5 B.5', None, 0.5, '', {'aims': 'science communication specialist', 'door': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'teach at every fire you pass, and let the bands come to know your name slowly', 'magic': 'print a broadsheet of wonders each month, and win its readers one by one'}, 'chance': 0.8}),
    ('give free talks at the museum on Saturdays, to learn the craft properly', 'U.5 G.5', None, 0.5, '', {'grants': 'public speaking', 'mark': 'learned a skill', 'v': 'universalism, benevolence', 'world': {'tribal': 'walk with the young watchers on the hill and teach them, to learn how teaching is done', 'magic': "guide visitors round the Academy's halls on feast days, to learn the craft of telling"}, 'chance': 0.8}),
    ('keep the job you have, and bring science into it more often', 'W.5 B.5', None, 0.5, '', {'habit': True, 'v': 'security, achievement', 'world': {'tribal': 'keep your place in the band, and bring what the watchers know to your own hearth', 'magic': 'keep your post, and bring the new wonders into your own work and your guild'}, 'chance': 0.8}),
    ('help a friend make a better film than yours, and cheer when it airs', 'W.5 R.5', None, 0.5, '', {'act': 'help a friend make a better film than their own, and cheer when it airs', 'mark': 'made a friend', 'v': 'benevolence, stimulation', 'world': {'tribal': 'help a friend shape a telling for the fire, and cheer loudest when they stand', 'magic': 'help a friend rehearse for the steps, and cheer loudest in the crowd'}, 'chance': 0.8}),
 ]},
{'name': 'a chair falls vacant at another university',
 'stages': 'adult mature',
 'age': (32, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.0),
 'drivers': 'prosper+.3 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, rival, partner',
 'requires': 'research group leader | research scientist',
 'tenure': (3.0, 50.0),
 'worlds': {'earth': 'a chair in your field falls vacant at another university, and your record would let you apply',
            'tribal': 'the teacher who held the teaching seat of a far band has gone to the ancestors, and they ask '
                      'whether a keeper of long standing would come',
            'magic': "a master's chair at another city's Academy stands empty, and petitions are welcome from "
                     'scholars of standing'},
 'timing': {'times': 'per research group leader of three years or more, or research scientist of eight years or '
                     'more, with published work, a year: perhaps 1 in 50 sees a chair in their field advertised at '
                     'another university and could apply (estimate); a chair draws dozens of applications from '
                     'senior people, a handful are interviewed, and most go to someone who already holds a chair or '
                     'a well-known name; an applicant who has never held one is appointed perhaps 1 time in 30 '
                     '(estimate)',
            'likelier': 'a long record of published work, a group that delivered, a field the university is '
                        'building, a mentor on the committee',
            'rarer': 'a thin record, a narrow field, a university that hires only sitting professors, hard times for '
                     'research money',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'The notice is short: a chair in {Ns} field at a university in another city, its holder '
                       'retiring, applications from senior researchers welcome. {N} reads the list of what the chair '
                       'asks for and finds in it, line by line, a description of the last ten years.'),
                      ('W',
                       'The criteria run to two pages: teaching, service, a record of funding, a plan for the '
                       'department. {N} checks each one against the file of evidence kept since the first post, and '
                       'starts a folder.'),
                      ('U',
                       '{N} pictures a chair that would let one question be followed for twenty years without asking '
                       "anyone's leave, and starts listing what the first five would settle."),
                      ('B',
                       'A chair is the strongest position the field has to offer: a say in hiring, in money, in what '
                       'gets studied. {N} knows two people on the committee, and one of them owes {N} a favour.'),
                      ('R',
                       'The notice has been open on {Ns} screen all afternoon. A new city, a new department, a '
                       'lecture hall full of strangers: the thought makes {N} restless in the best way.'),
                      ('G',
                       'The professor who is retiring there trained half the people {N} works with. Applying feels '
                       'less like a move than like being asked to keep something going.')],
            'tribal': [('',
                        "The keeper of a far band's teaching seat has gone to the ancestors, and word comes along "
                        'the river: a watcher of long standing who teaches well might come and take the seat. {N} '
                        'has taught the young watchers of the home band for many winters.')],
            'magic': [('',
                       "A notice is nailed to the Academy gate of the river city: a master's chair is empty, its old "
                       'holder gone to rest, and petitions are welcome from scholars of standing. {N} has led a '
                       'workshop at the home Academy for years.')]},
 'outcomes': (['The committee rings on a Tuesday: the chair is {Ns} from the autumn, and the first lecture is '
               'already on the timetable.',
               'The choice turns out well, and within a year the new department feels like a place {N} chose.'],
              ['{N} comes second. The chair of the committee writes, unasked, that the vote was close and the '
               'lecture the best they heard, and that the post went to someone who already held a chair elsewhere.',
               'The interview day is long and bright and goes well, {N} thinks; the letter in the spring is two '
               'lines long, and {N} reads it twice on the train home.']),
 'options': [
    ('apply with every requirement met and shown, the teaching and the service too', 'W1', None, 0.45, '', {'title': 'professor', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': 'ask for the seat in the proper way, every winter of teaching counted', 'magic': 'petition by every form, each lecture and each duty set down in order'}, 'chance': 0.03}),
    ('send a plan for twenty years of one question, and let the work make the case', 'U1', None, 0.45, '', {'title': 'professor', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'achievement, conformity', 'world': {'tribal': 'show the far band the whole teaching you would give, winter by winter', 'magic': "send the council the plan of a lifetime's study, and let it plead for you"}, 'chance': 0.03}),
    ('get the committee member who owes you a favour to put your name forward', 'B1', None, 0.45, '', {'act': 'get the committee member who owes them a favour to put their name forward', 'title': 'professor', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'have the elder who owes you a gift speak your name at the far fire first', 'magic': 'have the master who owes you a favour set your name before the council first'}, 'chance': 0.03}),
    ('ring the head of department, and ask to give a lecture there next week', 'R1', None, 0.45, '', {'title': 'professor', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'walk to the far band unasked, and teach at their fire before anyone has chosen', 'magic': 'ride to the river city, and lecture in its hall before the petitions are read'}, 'chance': 0.03}),
    ('apply with the backing of the students and colleagues who grew up in your group', 'G1', None, 0.45, '', {'act': 'apply with the backing of the students and colleagues who grew up in their group', 'title': 'professor', 'requires': 'published research', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'go with the young watchers you taught, who will speak for you at the far fire', 'magic': 'petition with the journeymen you trained, their names set beside yours'}, 'chance': 0.03}),
    ('stay, and use the call to win better terms where you are', 'B.5 G.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'let the home band hear you were sent for, and keep a stronger seat at your own fire', 'magic': 'let your own Academy hear of the call, and win a better seat where you are'}, 'chance': 0.8}),
    ("back a younger colleague's application, and write the warmest letter of your life", 'R.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, stimulation', 'world': {'tribal': 'speak at the far fire for a younger watcher who asks for the seat', 'magic': "write the warmest letter of your life for a younger scholar's petition"}, 'chance': 0.8}),
    ('ask what the committee wanted, and build the record for the next chair that opens', 'U.5 B.5', None, 0.5, '', {'aims': 'professor', 'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': 'ask the far band what their teacher must bring, and spend the winters getting it', 'magic': 'ask the council what wins a chair, and spend the years preparing for the next'}, 'chance': 0.8}),
    ('turn it down, and see the projects promised to your group through', 'W.5 R.5', None, 0.5, '', {'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'stay, and keep the teaching promised to the young watchers of your own band', 'magic': 'stay, and keep the promises made to your own journeymen'}, 'chance': 0.8}),
    ('take on more teaching and committee work, the duties a chair is chosen for', 'W.5 U.5', None, 0.5, '', {'grants': 'teaching', 'habit': True, 'v': 'conformity, achievement', 'world': {'tribal': "take on more of the band's teaching and its councils, the work the seat asks", 'magic': 'take on more lectures and council duties, the work a chair is chosen for'}, 'chance': 0.8}),
 ]},
{'name': "a scientist's post at a famous lab",
 'stages': 'young_adult adult mature',
 'age': (22, 60),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.015, 0.005, 0.0),
 'drivers': 'prosper+.3 era+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, rival, friend',
 'requires': 'research assistant | laboratory technician | research data steward | research software engineer',
 'tenure': (2.0, 40.0),
 'worlds': {'earth': "a scientist's post opens at one of the most famous laboratories in your field, and your years "
                     'at the bench would let you apply',
            'tribal': 'the most famous band of watchers, by the great river, wants one more watcher, and any helper '
                      'of long standing may ask',
            'magic': "the most famous workshop of the Academy's capital seeks a new scholar, and any journeyman of "
                     'standing may petition'},
 'timing': {'times': 'per research assistant, laboratory technician, research data steward or research software '
                     "engineer of two years or more, a year: perhaps 1 in 50 sees a scientist's post advertised at "
                     'one of the most famous laboratories in their field and applies (estimate); such posts draw '
                     'hundreds of applicants, most with a doctorate and papers of their own, and someone applying '
                     'from a support post is appointed perhaps 1 time in 25 (estimate)',
            'likelier': "a method of one's own that others use, a supervisor with a famous name, papers with one's "
                        'name on them, a lab expanding its staff',
            'rarer': 'no degree in the field, years spent only on routine work, a lab that hires its scientists from '
                     'its own students',
            'gap_years': (3.0, 10.0)},
 'scenes': {'earth': [('',
                       "The advertisement is in the field's main journal: a scientist's post in a laboratory whose "
                       'papers {N} has read for years, whose name everyone in the building knows. {N} has the '
                       "degree, the years at the bench and a method of one's own, if not the doctorate most "
                       'applicants will have, and reads it three times on the way home.'),
                      ('W',
                       'The post asks for eight things, listed in a box. {N} goes through them honestly with a pen '
                       'and finds five ticks, two half ticks and one blank.'),
                      ('U',
                       "{N} knows the lab's last three papers better than most of its own staff do, and knows "
                       'exactly where the method {N} built would fit into their next one.'),
                      ('B',
                       'Nobody gets a post like this from a cold application. {N} starts thinking about who has '
                       'worked there, and who still owes whom a favour.'),
                      ('R',
                       "The lab's famous instrument, the questions it chases, the people in the photographs on its "
                       'website: {N} wants to be there so much it is almost funny.'),
                      ('G',
                       'The group {N} works in now took {N} in as a beginner and taught everything {N} knows. '
                       'Leaving would be a loss, even for a famous name.')],
            'tribal': [('',
                        'Word comes down the great river: the band whose watchers are known at every fire wants one '
                        'more, and any helper who has counted beside the watchers for years may ask. {N} has counted '
                        "the herds beside the home band's watchers for many seasons.")],
            'magic': [('',
                       'A herald from the capital cries it in the square: the most famous workshop of the Academy '
                       "seeks a new scholar, and journeymen of standing may petition. {N} has kept a master's "
                       'instruments and tables for years.')]},
 'outcomes': (['The call comes on a Friday: the lab wants {N}, and the start date is the first of next month.',
               "The move goes the way {N} hoped, and within a year {Ns} name is on one of the lab's papers."],
              ['{N} is one of six asked to give a talk, and the questions afterwards are sharp and fair. The post '
               "goes to someone with two doctoral years at a rival lab; the director's email says {Ns} method was "
               'the best thing they saw all week.',
               'The rejection is a form letter, and {N} reads it at the bench between two runs, then finishes the '
               'second run.']),
 'options': [
    ('apply exactly to the advert, every criterion answered with evidence', 'W1', None, 0.45, '', {'title': 'research scientist', 'requires': 'graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity', 'world': {'tribal': 'ask the famous band in the proper way, every count you have made laid out', 'magic': 'petition by every form, each skill you have attested by a seal'}, 'chance': 0.04}),
    ('send the method you built, and show what it could do in their hands', 'U1', None, 0.45, '', {'title': 'research scientist', 'requires': 'graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, conformity', 'world': {'tribal': 'show them the way of counting you made, and what it could tell them', 'magic': 'send them the instrument you built, and the tables it has made'}, 'chance': 0.04}),
    ("ask the professor you assisted to ring the lab's director for you", 'B1', None, 0.45, '', {'act': "ask the professor they assisted to ring the lab's director for them", 'title': 'research scientist', 'requires': 'graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'ask the elder you served to send word to the famous band for you', 'magic': 'ask the master you served to write to the famous workshop for you'}, 'chance': 0.04}),
    ("turn up at the lab's open day, and talk your way to the bench", 'R1', None, 0.45, '', {'title': 'research scientist', 'requires': 'graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'walk to the great river band unasked, and start counting beside them', 'magic': 'walk into the famous workshop on its open day, and set to work at a bench'}, 'chance': 0.04}),
    ('apply with letters from the people whose project you kept running', 'G1', None, 0.45, '', {'act': 'apply with letters from the people whose project they kept running', 'title': 'research scientist', 'requires': 'graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'go with the word of the hearths whose counts you kept for years', 'magic': 'petition with letters from the masters whose work you kept for years'}, 'chance': 0.04}),
    ('take a better-paid post at a company lab instead', 'B.5 R.5', None, 0.5, '', {'v': 'achievement, stimulation', 'world': {'tribal': "go to the traders' camp, where a good counter is paid in salt", 'magic': 'take service with a merchant house that pays a scholar well'}, 'chance': 0.8}),
    ('ask to spend a summer in the famous lab, to learn how it works', 'U.5 G.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'universalism', 'world': {'tribal': 'ask to walk one season with the famous band, to learn their ways', 'magic': 'ask to spend a summer in the famous workshop, learning its ways'}, 'chance': 0.8}),
    ('start the doctorate the post asks for, on a question of your own', 'U.5 R.5', None, 0.5, '', {'aims': 'research scientist', 'door': True, 'v': 'self-direction, achievement', 'world': {'tribal': 'go to the lore-keepers for the long learning the band asks of its watchers', 'magic': "enter the Academy's long course for a doctor's ring, on a question of your own"}, 'chance': 0.8}),
    ('let your own lab see the application, and bargain for a longer contract', 'W.5 B.5', None, 0.5, '', {'v': 'security', 'world': {'tribal': 'let your own band see you were asked about, and win a surer place', 'magic': 'let your master see the petition, and win a sealed contract where you are'}, 'chance': 0.8}),
    ('stay with the group that trained you; its work is not finished', 'W.5 G.5', None, 0.5, '', {'act': 'stay with the group that trained them; its work is not finished', 'v': 'tradition, benevolence', 'world': {'tribal': 'stay with the band that taught you to count; its watching is not done', 'magic': 'stay with the workshop that trained you; its work is not finished'}, 'chance': 0.8}),
 ]},
{'name': 'a named fellowship, one a year',
 'stages': 'young_adult adult',
 'age': (25, 45),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.02, 0.0, 0.0),
 'drivers': 'prosper+.3 era+.2 fortune+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, rival, partner',
 'requires': 'research scientist',
 'tenure': (0.0, 5.0),
 'worlds': {'earth': "a famous funder's named fellowship pays one young scientist's question for three years, and "
                     'you have the doctorate to apply',
            'tribal': 'the elders give one young watcher each year three winters fed by the band, to learn one thing '
                      'of their own choosing',
            'magic': "a founder's purse at the Academy pays one young doctor a year for three years on a question of "
                     'their own'},
 'timing': {'times': 'per research scientist in the first years after a doctorate, a year: perhaps 1 in 30 applies '
                     "for one of the few named fellowships, a famous funder's or a learned society's, that pay a "
                     "young scientist's own question for three years (estimate); such fellowships fund perhaps 2 to "
                     '5 applications in 100 (estimate from the success rates such funders report), while most new '
                     'doctors who want a postdoc find an ordinary one in a funded group',
            'likelier': 'a doctorate that produced papers, a host lab with a famous name, a supervisor who backs the '
                        'application, a field the funder favours',
            'rarer': 'a doctorate that took long and produced little, no host lab willing to sign, hard times for '
                     'research money',
            'gap_years': (3.0, 6.0)},
 'scenes': {'earth': [('',
                       'The fellowship carries a famous name and comes once a year: three years of salary and money '
                       "for one young scientist's own question, at any lab that will host them. {Ns} doctorate is "
                       'fresh, the idea has been waiting since the second year of it, and the deadline is in five '
                       'weeks.'),
                      ('W',
                       "The guidance notes are precise: a host lab's signed letter, a three-year plan, two referees, "
                       "a budget in the funder's own format. {N} prints them and starts at the top."),
                      ('U',
                       '{N} has carried the question since the second year of the doctorate: what it is, why it '
                       'matters, and the three experiments that would answer it. Five weeks is enough to write it '
                       'down properly.'),
                      ('B',
                       'Past winners have gone on to lead groups of their own, almost all of them. {N} knows the '
                       'name on the fellowship opens doors for the rest of a career.'),
                      ('R',
                       'The idea is wild, and {N} loves it, and nobody else would ever fund it. That is exactly why '
                       'it belongs here.'),
                      ('G',
                       '{N} thinks of the lab and the town where the doctorate was done. The fellowship could take '
                       'the question back there, to the people who made it possible.')],
            'tribal': [('',
                        'At the gathering the elders name one young watcher a year to be fed by the band for three '
                        'winters while they learn one thing of their own choosing. {N} has only lately been named a '
                        'watcher, and already has a question nobody else is asking.')],
            'magic': [('',
                       "The founder's purse is cried at the Academy's gate each spring: three years of bread and "
                       "candles for one young doctor's own question. {Ns} doctor's ring is new, and the question has "
                       'kept {N} awake for a year.')]},
 'outcomes': (["The funder's email arrives on a Sunday night, and {N} reads it four times before waking anyone.",
               'The three years begin, and the question {N} carried since the doctorate finally has its own bench.'],
              ["{N} is one of eight called to interview, out of several hundred. The panel's letter calls the idea "
               'the most original of the year and says it was not yet ready; {N} pins the letter above the desk.',
               'The application goes in at four minutes to midnight, and the answer in March is no; {N} takes the '
               'funded post in a large group instead, and keeps the idea in a drawer.']),
 'options': [
    ("apply exactly as the guidance asks, with the host lab's letter signed", 'W1', None, 0.45, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity', 'world': {'tribal': 'ask the elders by the old form, with your teacher standing beside you', 'magic': "petition by every form of the founder's rules, your host master's seal attached"}, 'chance': 0.04}),
    ('write the proposal of a lifetime: one question, three years, every step costed', 'U1', None, 0.45, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': 'lay before the elders one question for three winters, every step planned', 'magic': 'write a petition of one question for three years, every step accounted'}, 'chance': 0.04}),
    ("get your doctoral supervisor to call the fellowship's chair", 'B1', None, 0.45, '', {'act': "get their doctoral supervisor to call the fellowship's chair", 'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'have your teacher speak your name to the eldest before the gathering', 'magic': "have your old master write to the founder's trustees on your behalf"}, 'chance': 0.04}),
    ('pitch the boldest idea you have in the interview, and ignore the safe plan', 'R1', None, 0.45, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'tell the elders the wildest thing you mean to learn, and leave the safe plan unsaid', 'magic': 'put the wildest idea before the trustees, and leave the safe plan in your satchel'}, 'chance': 0.04}),
    ('apply to take the fellowship back to the lab and the town you came from', 'G1', None, 0.45, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, benevolence', 'world': {'tribal': 'ask to take the learning back to the band you came from', 'magic': 'petition to take the purse home, to the workshop where you began'}, 'chance': 0.04}),
    ('stay in the home lab on a bridging contract, and guard your data', 'B.5 G.5', None, 0.5, '', {'v': 'power', 'world': {'tribal': 'stay at your own fire one more winter, and keep your counts close', 'magic': "stay in your master's workshop one more year, and keep your notes close"}, 'chance': 0.75}),
    ('spend a year at a field station instead, among people you like', 'R.5 G.5', None, 0.5, '', {'v': 'stimulation, benevolence', 'world': {'tribal': 'go out with the summer hunters for a year, among friends', 'magic': 'spend a year at a far observatory, among friends'}, 'chance': 0.75}),
    ('keep the bold idea, and work it up on evenings for the next round', 'U.5 R.5', None, 0.5, '', {'aims': 'postdoctoral researcher', 'habit': True, 'v': 'stimulation', 'world': {'tribal': 'keep the bold thought, and shape it by the evening fire for the next gathering', 'magic': 'keep the bold idea, and work it up by candlelight for the next round'}, 'chance': 0.75}),
    ('take a company post with a salary and a pension', 'W.5 B.5', None, 0.5, '', {'v': 'security', 'world': {'tribal': 'take a sure place with a rich band that trades in salt', 'magic': 'take service with a merchant house, its wages paid every quarter'}, 'chance': 0.75}),
    ('take the ordinary funded postdoc in a large group, with its plan', 'W.5 U.5', None, 0.5, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'v': 'achievement, conformity', 'world': {'tribal': "join a large band's watchers for three winters, under their keeper's plan", 'magic': "take a journeyman's place for three years in a great workshop, under its plan"}, 'chance': 0.75}),
 ]},
{'name': 'a national centre opens its posts',
 'stages': 'young_adult adult mature',
 'age': (26, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.01, 0.0),
 'drivers': 'prosper+.3 era+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, rival, friend',
 'requires': 'research scientist',
 'tenure': (2.0, 45.0),
 'worlds': {'earth': 'a national research centre opens a round of posts, and your years as a scientist would let you '
                     'apply for one',
            'tribal': 'the great gathering of the bands looks for keepers of its shared counts, stores and tellings, '
                      'and any watcher of long standing may ask',
            'magic': "the realm's new Academy opens posts for assessors, instrument-makers, record-keepers and "
                     'masters of works, and any scholar of standing may petition'},
 'timing': {'times': 'per research scientist of two years or more, a year: perhaps 1 in 80 sees a national research '
                     'centre open a round of posts that fit them (a data service, a software team, an evidence unit, '
                     'a programme with towns and farms, projects to lead) and applies (estimate); a national '
                     "centre's round draws hundreds of applicants for a few dozen posts, and someone moving across "
                     "from a scientist's post is appointed perhaps 1 time in 25 (estimate)",
            'likelier': 'a skill the centre names in its plan, years in a field it is building, a mentor already '
                        'there, a government that is spending on research',
            'rarer': 'a narrow speciality, hard times for public money, a centre that fills its posts from inside',
            'gap_years': (3.0, 10.0)},
 'scenes': {'earth': [('',
                       'The national centre has been in the news for a year, and now its first round of posts is '
                       'out: an evidence unit, a software team, a programme with towns and farms, a team for the '
                       'long records, and projects to lead. {N} reads the whole list twice and finds that one of '
                       'them reads like a description of who {N} might become.'),
                      ('W',
                       'Each post comes with a person specification and a scoring grid. {N} likes that: the centre '
                       'has said in advance exactly how it will choose.'),
                      ('U',
                       "{N} reads the centre's ten-year plan and sees the gap in it at once, the thing nobody has "
                       'been hired to do yet.'),
                      ('B',
                       "A national centre is where the money, the attention and the next decade's decisions will be. "
                       '{N} wants to be inside it early, in a post with some say.'),
                      ('R',
                       'A new place, built from nothing, where nothing is settled yet: {N} can feel the pull of it '
                       'like weather.'),
                      ('G',
                       'The posts that matter most to {N} are the quiet ones: the people who will keep the records, '
                       'and the ones who will work with the towns and farms the science is about.')],
            'tribal': [('',
                        'The great gathering will keep shared counts of the herds, shared stores and shared tellings '
                        'for every band, and it asks for keepers. Any watcher of long standing may ask, and {N} has '
                        'watched for many seasons.')],
            'magic': [('',
                       'A herald reads it in every market of the realm: the new Academy of the realm needs '
                       'assessors, instrument-makers, record-keepers and masters of works, and scholars of standing '
                       'may petition at the capital by midsummer.')]},
 'outcomes': (['The letter from the centre comes in a heavy envelope: a start date, a desk in the new building, and '
               'a welcome day in the autumn.',
               "The new post turns out to be what {N} hoped, and {N} is in the room when the centre's first big "
               'decisions are made.'],
              ['{N} reaches the last round of interviews in the new building, all glass and fresh paint. The post '
               "goes to someone already doing the job elsewhere; the panel's note says {Ns} answers were the "
               'clearest of the day.',
               "The centre's portal rejects the upload twice, the third attempt goes in at the last minute, and the "
               'answer is no; {N} keeps the person specification anyway, as a list of things to learn.']),
 'options': [
    ('apply for the evidence unit, with a review done to its own standard', 'W1', None, 0.45, '', {'title': 'evidence synthesis specialist', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, universalism', 'world': {'tribal': "ask to be one who weighs every band's counts for the gathering, in the proper way", 'magic': "petition for the assessors' bench, with a judgement written to its own rules"}, 'chance': 0.04}),
    ('apply to build its software, with a working tool attached', 'U1', None, 0.45, '', {'title': 'research software engineer', 'requires': 'writing code', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, conformity', 'world': {'tribal': "ask to make the gathering's tally-sticks and knots, with a set already made", 'magic': "petition for the instrument-makers' bench, a working engine in hand"}, 'chance': 0.04}),
    ('apply to lead one of its new projects, and get two directors to back you', 'B1', None, 0.45, '', {'act': 'apply to lead one of its new projects, and get two directors to back them', 'title': 'research project lead', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'power, achievement', 'world': {'tribal': "ask to lead one of the gathering's great counts, with two elders behind you", 'magic': "petition to lead one of the new works, with two masters' seals behind you"}, 'chance': 0.04}),
    ('apply for the post out with the towns and farms, and go to the interview muddy', 'R1', None, 0.45, '', {'title': 'participatory research coordinator', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, benevolence', 'world': {'tribal': 'ask to be the one who goes out among the far bands, and come to the fire straight from the trail', 'magic': 'petition for the post among the villages, and come before the council with the road still on your boots'}, 'chance': 0.04}),
    ('apply to keep its long records, the ones meant to outlast everyone', 'G1', None, 0.45, '', {'title': 'research data steward', 'requires': 'working with data', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, universalism', 'world': {'tribal': "ask to keep the gathering's long memory, the counts meant to outlast everyone", 'magic': "petition to keep the realm's long ledgers, the ones meant to outlast every scholar"}, 'chance': 0.04}),
    ("take a company's offer instead, at twice the salary", 'B.5 R.5', None, 0.5, '', {'v': 'achievement', 'world': {'tribal': 'go with the salt traders, who pay a counter twice what the band does', 'magic': "take a merchant house's offer, at twice a scholar's wage"}, 'chance': 0.8}),
    ('ask what the centre found missing, and build it for the next round', 'U.5 B.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': 'ask what the gathering found lacking, and learn it before the next', 'magic': 'ask what the council found lacking, and master it for the next opening'}, 'chance': 0.8}),
    ('send the centre your best dataset, and offer to help with theirs', 'U.5 G.5', None, 0.5, '', {'grants': 'research collaborators', 'v': 'universalism, benevolence', 'world': {'tribal': 'send the gathering your best counts as a gift, and offer help with theirs', 'magic': 'send the Academy of the realm your best tables, and offer help with theirs'}, 'chance': 0.8}),
    ('stay with the long study you have kept for years', 'W.5 G.5', None, 0.5, '', {'identity': True, 'v': 'tradition', 'world': {'tribal': 'stay with the long watch you have kept for many winters', 'magic': 'stay with the long ledger you have kept for years'}, 'chance': 0.8}),
    ('recommend the colleague who fits the post better, and say why', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence', 'world': {'tribal': 'name a friend at the fire who fits the place better, and say why', 'magic': 'commend a fellow scholar who fits the post better, and say why'}, 'chance': 0.8}),
 ]},
{'name': 'the survey wants a paid assistant',
 'stages': 'young_adult adult mature',
 'age': (18, 60),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.005, 0.0),
 'drivers': 'prosper+.2 era+.2 community+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'mentor, friend, colleague, partner, rival',
 'requires': 'citizen scientist | community observer',
 'tenure': (4.0, 80.0),
 'worlds': {'earth': "the survey you have volunteered for over years advertises a paid assistant's post, and your "
                     'records are known there',
            'tribal': "the watchers of the elders' circle want a helper fed by the band, and your counts are known "
                      'at the fire',
            'magic': "the Academy's survey of the realm takes on a paid assistant, and your years of sightings are "
                     'known to its masters'},
 'timing': {'times': 'per citizen scientist or community observer of four years or more, a year: perhaps 1 in 100 '
                     "sees the survey or project they volunteer for advertise a paid assistant's post and applies "
                     '(estimate); such posts usually go to science graduates, and a volunteer without the degree is '
                     'taken on perhaps 1 time in 25, more often where the project already knows their records '
                     '(estimate)',
            'likelier': "years of careful records, a project that knows the volunteer's name, a degree in any "
                        'subject, a project with new money',
            'rarer': 'no time to change jobs, a project that hires only graduates of its own university, records '
                     'nobody has checked',
            'gap_years': (4.0, 12.0)},
 'scenes': {'earth': [('',
                       "The newsletter that comes with every season's count has a box on the back page this time: "
                       'the survey has money for a paid assistant, two years, to help run the counts and check the '
                       'records. {N} has sent in counts for years, and reads the box twice over breakfast.'),
                      ('W',
                       'The post asks for a degree in a relevant subject "or equivalent experience". {N} has kept '
                       "the counts by the survey's rules for years, every sheet signed, and wonders whether that is "
                       'the equivalent.'),
                      ('U',
                       "{N} knows the survey's records from the inside: which counters are careful, which routes are "
                       'thin, where the trends are real. Nobody with a degree from outside could know that.'),
                      ('B',
                       'A paid post is a foot in the door of research itself. {N} knows the scientist who runs the '
                       'survey by sight, and wonders whether a word in the right ear would help.'),
                      ('R',
                       '{N} has done this for love, every season, in every weather. Being paid to do it would be '
                       'almost too good to bear.'),
                      ('G',
                       'The volunteers {N} counts beside have been a second family for years. The post would mean '
                       'doing the same work with them, only now as the one they ring.')],
            'tribal': [('',
                        'At the fire the elders say the circle of watchers wants a helper fed by the band, to keep '
                        'the counts and teach the young ones to count. {N} has counted the geese beside the watchers '
                        'for many springs, and they know {Ns} marks.')],
            'magic': [('',
                       "A notice comes with the season's letter from the Academy: its survey of the realm will pay "
                       "an assistant to keep its ledgers and check the correspondents' sightings. {N} has sent in "
                       'sightings for years, each one in a careful hand.')]},
 'outcomes': (['The scientist rings on a Thursday evening: the post is {Ns}, and could {N} start with the spring '
               'count?',
               "The first season as the survey's assistant goes well, and the old volunteers are proud to say they "
               'knew {N} when.'],
              ['{N} is asked to interview, the only one there with no degree, and answers every question about the '
               'routes better than the panel expected. The post goes to a graduate from the university; the '
               "scientist writes that {Ns} records are the survey's best, and asks {N} to keep sending them.",
               'The letter says the post has gone to someone with the right qualification, and {N} goes out on the '
               'next count anyway, in the rain, because the birds do not know.']),
 'options': [
    ('apply with every count you have made, checked and in order', 'W1', None, 0.45, '', {'title': 'research assistant', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': 'ask the elders for the place, every count you have made laid out in order', 'magic': 'petition with every sighting you have sent, checked and bound in order'}, 'chance': 0.04}),
    ('send the survey an analysis of your own records it never asked for', 'U1', None, 0.45, '', {'title': 'research assistant', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, conformity', 'world': {'tribal': 'show the elders what your counts say that nobody asked them to say', 'magic': 'send the masters a reckoning of your own sightings, unasked'}, 'chance': 0.04}),
    ('ask the scientist who leads the survey to make the post yours', 'B1', None, 0.45, '', {'act': 'ask the scientist who leads the survey to make the post theirs', 'title': 'research assistant', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'ask the keeper of the watch to give the place to you', 'magic': 'ask the master of the survey to set your name on the post'}, 'chance': 0.04}),
    ('ring the next morning, and offer to start that week', 'R1', None, 0.45, '', {'title': 'research assistant', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'go to the keeper at dawn, and offer to start counting that day', 'magic': "knock at the master's door at first light, and offer to start that week"}, 'chance': 0.04}),
    ('apply with the other volunteers behind you, who know your counts', 'G1', None, 0.45, '', {'act': 'apply with the other volunteers behind them, who know their counts', 'title': 'research assistant', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'ask with the watchers you count beside standing behind you', 'magic': "petition with your fellow correspondents' names beside yours"}, 'chance': 0.04}),
    ('keep volunteering, and take charge of the records for your own patch', 'B.5 G.5', None, 0.5, '', {'habit': True, 'v': 'power', 'world': {'tribal': 'keep watching, and take charge of the counts on your own hill', 'magic': 'keep sending sightings, and take charge of the ledger for your own district'}, 'chance': 0.8}),
    ('take the evening course the post asks for, and apply next time', 'U.5 B.5', None, 0.5, '', {'aims': 'research assistant', 'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': 'learn from the lore-keepers what the place asks, and ask again next year', 'magic': "take the Academy's evening lessons the post asks for, and petition next time"}, 'chance': 0.8}),
    ("build a small tool that checks the volunteers' records, and give it away", 'U.5 R.5', None, 0.5, '', {'grants': 'a nose for the odd result', 'v': 'stimulation, benevolence', 'world': {'tribal': 'make a counting-cord that catches mistakes, and give it to every watcher', 'magic': 'build a small engine that checks the sightings, and give it to the survey'}, 'chance': 0.8}),
    ('stay a volunteer, the way the old counters always were', 'W.5 G.5', None, 0.5, '', {'identity': True, 'v': 'tradition', 'world': {'tribal': 'keep watching for nothing, the way the old watchers always did', 'magic': 'stay an unpaid correspondent, the way the old ones always were'}, 'chance': 0.8}),
    ('urge a younger volunteer with the degree to apply, and help with the letter', 'W.5 R.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence', 'world': {'tribal': 'send a young watcher who has the learning to ask, and help with the asking', 'magic': "urge a young correspondent with the Academy's ring to petition, and help write it"}, 'chance': 0.8}),
 ]},
{'name': 'the code everyone uses has a bug',
 'stages': 'young_adult adult mature elder',
 'age': (20, 70),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss, mentor',
 'requires': 'research software engineer',
 'worlds': {'earth': 'you find a bug in the analysis package dozens of labs rely on, and some published numbers may '
                     'be off'},
 'timing': {'times': 'per research software engineer: a bug in a package many labs rely on turns up a few times a '
                     'year, and one that may have changed published numbers perhaps once every few years; about 1 '
                     'life in 500 ever works as a research software engineer (estimate)'},
 'scenes': {'earth': [('',
                       'Late on a Tuesday, {N} finds that the analysis package dozens of labs rely on has been '
                       'rounding one value wrongly for two years. Some published numbers may be off.'),
                      ('W',
                       'Every lab that cites the package trusted it to do what the manual says. The list of those '
                       'labs, in a file on {Ns} desktop, runs to four pages.'),
                      ('U',
                       'The bug only bites when two rare settings meet. {N} wants to know exactly which results it '
                       'touched before saying a word to anyone.'),
                      ('B',
                       'The bug came in with one of {Ns} own changes, two years ago, and the grant that pays for the '
                       'package is up for renewal this month.'),
                      ('R',
                       'First a sick lurch in the stomach, then an odd thrill: it is a beautiful bug, and nobody '
                       'else in the world has seen it yet.'),
                      ('G',
                       'The package has grown for ten years, patch on patch, like an old farmhouse. {N} has found a '
                       'crack in a wall nobody has touched since it was built.')]},
 'outcomes': (['The fix goes out, the labs rerun their numbers, and most of the published results barely move.',
               'Two labs write to thank {N}, and one asks for help checking an old paper.'],
              ["A reviewer spots the bug in someone else's paper first, and the questions arrive at {Ns} desk.",
               'The fix breaks something else, and the help forum fills up overnight.']),
 'options': [
    ('post a warning to every user today, naming the versions affected', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'mark': 'owned up', 'chance': 0.93}),
    ('trace every result the bug could have touched before telling anyone', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.65}),
    ('fix it quietly in the next release and say nothing about the old numbers', 'B1', None, 0.45, '', {'v': 'security, power', 'mark': 'hid a wrong', 'closed': 'approval: hiding a known error from the people who rely on the code; backfire: a user finds the bug in an old version and traces it to the silent fix', 'self_control': '-', 'chance': 0.9}),
    ('stay up through the night writing the fix, and ship it by breakfast', 'R1', None, 0.45, '', {'v': 'achievement, stimulation', 'chance': 0.75}),
    ("ring the package's retired founder and ask how that part was meant to work", 'G1', None, 0.45, '', {'v': 'tradition', 'door': True, 'chance': 0.6}),
    ('write the test that would have caught it, and make it a rule for every change', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'habit': True, 'mark': 'learned a skill', 'grants': 'reproducible workflow', 'chance': 0.88}),
    ('work out which big labs are hit and tell them first, privately', 'U1', 'B.7', 0.5, '', {'v': 'power', 'chance': 0.7}),
    ('use the bug to win a fortnight off support duty, to rebuild the module your way', 'B1', 'R.7', 0.5, '', {'v': 'self-direction', 'chance': 0.6}),
    ('pour a wild month into rewriting the crumbling module so it lasts another decade', 'R1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'self_control': '+', 'chance': 0.5}),
    ('ask the long-time users to recheck their own results together, as the project always has', 'G1', 'W.7', 0.5, '', {'v': 'universalism, tradition', 'chance': 0.55}),
 ]},
{'name': 'a paper that thanks everyone but your software',
 'stages': 'young_adult adult mature elder',
 'age': (20, 70),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss, friend',
 'requires': 'research software engineer',
 'worlds': {'earth': 'a much-praised paper ran every analysis on your software, and its thanks go to everyone but '
                     'the software'},
 'timing': {'times': 'per research software engineer: a paper that ran its analysis on their software and does not '
                     'credit it appears several times a year; much of the research software in daily use is never '
                     'cited by the papers that rely on it (estimate)'},
 'scenes': {'earth': [('',
                       'A paper from down the corridor makes the news, and every figure in it came out of {Ns} '
                       'software. The acknowledgements thank the funders, the reviewers and the coffee machine, but '
                       'not the code.'),
                      ('W',
                       'There is a proper way to credit software, a citation and a version number, and {N} wrote the '
                       'guidance page that explains it. The paper ignored every line.'),
                      ('U',
                       '{N} counts: eleven papers this year ran on the tool, and four cite it. Citations are what '
                       'the next review of the software will be judged on.'),
                      ('B',
                       'Software nobody cites looks unused, and unused software loses its funding. {colleague}, the '
                       "paper's first author, is up for promotion on the strength of it."),
                      ('R',
                       '{N} reads the acknowledgements twice and feels the heat climb up the neck. Months of '
                       'evenings went into that tool.'),
                      ('G',
                       'Software is like the pipes in a house: nobody thanks them until they burst. {N} has always '
                       'half known this, and it still stings.')]},
 'outcomes': (['The next paper from down the corridor cites the software, and its first author says thanks in the '
               'lift.',
               "The tool's use is counted properly at last, and its funding review goes smoothly."],
              ['Nothing changes, and the next paper thanks the coffee machine again.',
               'The first author takes it personally, and the corridor goes quiet whenever {N} walks down it.']),
 'options': [
    ('write to the journal and ask for a correction that adds the citation', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.45}),
    ('make the software print how to cite it at the end of every run', 'U1', None, 0.45, '', {'v': 'achievement', 'chance': 0.8}),
    ('list every paper that ran on your tool and ask for a regrade on them', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'chance': 0.45}),
    ('say it straight out at the lab meeting: the software made that paper', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'chance': 0.75}),
    ('let it go; the people who matter know who built the tool', 'G1', None, 0.45, '', {'v': 'tradition (humility)', 'chance': 0.9}),
    ("draft the institute's first rule on how research software is credited", 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'chance': 0.55}),
    ('publish a short paper on the software itself, so it has something citable', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'grants': 'published research', 'chance': 0.65}),
    ('grab a free demo slot at the big conference and show the tool off', 'B1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'door': True, 'chance': 0.85}),
    ('buy the first author a drink and tell them, friend to friend, how it felt', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'made a friend', 'chance': 0.8}),
    ('propose the tool as a shared service with its own budget, and offer to run it', 'G1', 'W.7', 0.5, '', {'title': 'research facility lead', 'requires': 'reproducible workflow', 'without': 'impossible', 'v': 'universalism, benevolence', 'chance': 0.1}),
 ]},
{'name': 'a request for data you promised to protect',
 'stages': 'young_adult adult mature elder',
 'age': (22, 70),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'colleague, boss, elder',
 'requires': 'research data steward',
 'worlds': {'earth': 'a respected researcher asks for the full survey file, addresses and all, that the town gave on '
                     'a promise of privacy'},
 'timing': {'times': 'per research data steward: a request for identifiable data held under a promise of privacy '
                     'comes perhaps once or twice a year, often from a respected researcher with a good reason; '
                     'about 1 life in 1,000 ever works as a research data steward (estimate)'},
 'scenes': {'earth': [('',
                       '{colleague} from a big university wants the full health survey file, addresses included, for '
                       "a study of the old factory's pollution. Three thousand people in {place} answered the survey "
                       'on a promise that no address would ever leave the archive.'),
                      ('W',
                       'The consent form is clear, and {N} has read it a hundred times: answers for research, '
                       'addresses never. Rules that bend for a good cause are not rules.'),
                      ('U',
                       'There may be a way to give the study what it needs without a single address: distances to '
                       'the factory, worked out inside the archive. {N} starts sketching it on the back of an '
                       'envelope.'),
                      ('B',
                       "{colleague} sits on the committee that decides the archive's funding next spring. A refusal "
                       'will be remembered.'),
                      ('R',
                       '{N} met some of these people when the survey was taken: a woman who brought biscuits, a man '
                       'who told his whole life story. The thought of their addresses in an email makes {N} angry.'),
                      ('G',
                       'The town trusted the archive the way people trust the old bank on the high street. Trust '
                       'like that took thirty years to grow and could go in a week.')]},
 'outcomes': (['The study gets what it needs, and not one address leaves the archive.',
               "{colleague} accepts the answer, and the town's trust in the archive holds."],
              ["{colleague} goes over {Ns} head, and the archive's director wants an explanation by Friday.",
               'Word reaches {place} that its survey was asked for, and people start asking questions at the shop.']),
 'options': [
    ("refuse, and quote the consent form's exact words", 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.92}),
    ('work out the distances inside the archive, so no address ever leaves it', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'mark': 'learned a skill', 'chance': 0.72}),
    ('send the full file, addresses and all, and keep the committee sweet', 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'broke your word', 'closed': "law: sharing personal data beyond what people agreed to; backfire: a breach report, and the archive's name in the local paper", 'self_control': '-', 'chance': 0.82}),
    ('tell the requester in plain, heated words what those people were promised', 'R1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.72}),
    ('ask the old survey team what people were told on their doorsteps', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.8}),
    ("refuse in writing, copy the archive's director, and keep a record of it all", 'W1', 'B.7', 0.5, '', {'v': 'security', 'chance': 0.9}),
    ('open a locked online room where the study can explore but never download', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'binds': True, 'chance': 0.7}),
    ("trade a safe extract for the university's help keeping the archive alive", 'B1', 'G.7', 0.5, '', {'v': 'security, power', 'chance': 0.38}),
    ('stand up at the ethics committee and argue that the town must be asked first', 'R1', 'W.7', 0.5, '', {'v': 'universalism', 'identity': True, 'chance': 0.72}),
    ('hold an evening at the community centre so people can decide whether to join the study', 'G1', 'U.7', 0.5, '', {'v': 'universalism, benevolence', 'binds': True, 'chance': 0.4}),
 ]},
{'name': 'the archive nobody funds',
 'stages': 'young_adult adult mature elder',
 'age': (22, 70),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, colleague, elder',
 'requires': 'research data steward',
 'worlds': {'earth': 'the archive you look after loses its funding at the end of the year, because every grant pays '
                     'for new data and none for the old'},
 'timing': {'times': 'per research data steward: a collection or archive losing its money comes perhaps once in five '
                     'to ten years of a working life, since most grants pay for new data and few for keeping old '
                     'data (estimate)'},
 'scenes': {'earth': [('',
                       'The letter says it kindly: the archive {N} looks after, thirty years of records, has no '
                       'funding after December. Every grant pays for new data, and none pays to keep the old.'),
                      ('W',
                       'Hundreds of studies cite the archive, and the people who made those records were told their '
                       'work would be kept. {N} feels that promise as {Ns} own.'),
                      ('U',
                       '{N} pulls the download logs: forty countries last year, and a spike every time a flood or a '
                       'drought makes the news. The numbers make the case, if anyone reads them.'),
                      ('B',
                       '{Ns} own salary sits on the same budget line as the servers. Whoever saves the archive will '
                       'also decide who runs it.'),
                      ('R',
                       "{N} wants to march into the dean's office with a hard drive in each hand and drop them on "
                       'the desk.'),
                      ('G',
                       'Some of these records were written by hand by people long dead, the seasons of a whole '
                       'region one line at a time. {N} cannot picture them simply gone.')]},
 'outcomes': (['A funder steps in for three more years, and the servers hum on.',
               'The archive survives on a smaller budget, and its users finally know what it costs to keep.'],
              ['December comes, the money ends, and the archive goes read-only while its future is argued over.',
               'The rescue falls through, and {boss} starts asking which parts of the archive could simply be '
               'switched off.']),
 'options': [
    ('write to every user and ask them to sign a letter to the funders', 'W1', None, 0.45, '', {'v': 'universalism', 'chance': 0.35}),
    ('build the case from the download logs and send it to three funders', 'U1', None, 0.45, '', {'v': 'achievement', 'chance': 0.35}),
    ('take the data job a bank keeps offering, before the axe falls', 'B1', None, 0.45, '', {'v': 'security, achievement', 'drops': 'research data steward', 'chance': 0.8}),
    ('post the letter online with a photo of the old drives, and ask for help', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'identity': True, 'chance': 0.35}),
    ('copy everything to a second home at another university, just in case', 'G1', None, 0.45, '', {'v': 'security, tradition', 'chance': 0.72}),
    ("put the archive's case to the director in the formal budget review", 'W1', 'B.7', 0.5, '', {'v': 'security', 'chance': 0.45}),
    ('turn the records into a live map anyone can play with, to show what they hold', 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'chance': 0.85}),
    ('trade your own hours down to three days a week, so the servers keep running', 'B1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'binds': True, 'self_control': '+', 'chance': 0.65}),
    ('give your evenings to keeping the archive running until money is found', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'habit': True, 'self_control': '+', 'binds': True, 'chance': 0.85}),
    ('gather the old data keepers for a day and write down what only they remember', 'G1', 'U.7', 0.5, '', {'v': 'tradition', 'door': True, 'mark': 'learned a skill', 'chance': 0.75}),
 ]},
{'name': 'the evidence points where nobody wants it to',
 'stages': 'young_adult adult mature elder',
 'age': (24, 75),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, elder',
 'requires': 'evidence synthesis specialist',
 'worlds': {'earth': 'your review finds that a much-loved programme, run by the charity paying for the review, makes '
                     'no measurable difference'},
 'timing': {'times': 'per evidence synthesis specialist: a review finding that a well-loved programme makes no '
                     'measurable difference, with its backers paying for the review, comes perhaps once every few '
                     'years; about 1 life in 2,000 ever works in evidence synthesis (estimate)'},
 'scenes': {'earth': [('',
                       'The review {N} has spent a year on is nearly done, and the pooled evidence says the '
                       'parenting course the charity has run for twenty years makes no measurable difference. The '
                       'charity paid for the review.'),
                      ('W',
                       'The protocol was registered before a single study was read, and it says the findings are '
                       'published whatever they show. {N} signed it.'),
                      ('U',
                       'Twelve trials, most of them small, two of them good. {N} reads the two good ones again, '
                       'looking for anything the pooled number hides.'),
                      ('B',
                       'The charity is {Ns} biggest client, and its director has already asked, very politely, '
                       'whether the summary could lead with the positives.'),
                      ('R',
                       '{N} has met the volunteers who run the course: warm, tireless people. Writing this feels '
                       'like kicking them.'),
                      ('G',
                       "The course has been part of the town's life for twenty years, like the Saturday market. Some "
                       'things matter in ways a trial cannot measure, and {N} knows that is not the question that '
                       'was asked.')]},
 'outcomes': (['The review comes out as written, and the charity starts redesigning the course around what the '
               'evidence shows.',
               'The director reads it twice, sighs, and thanks {N} for being straight with them.'],
              ['The charity sits on the review for a year, and the course carries on unchanged.',
               'A newspaper gets hold of it first, and the volunteers read about it in the worst possible way.']),
 'options': [
    ('publish the finding exactly as the protocol says, softening nothing', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'identity': True, 'chance': 0.7}),
    ('check whether the two good trials tell a different story, and report that too', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'chance': 0.8}),
    ('ask the charity for a second contract, to rebuild the course around the evidence', 'B1', None, 0.45, '', {'v': 'achievement, power', 'chance': 0.5}),
    ('go and tell the volunteers yourself, before they read it anywhere else', 'R1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.82}),
    ("soften the summary for the volunteers' sake, as an old friend of the course would", 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'mark': 'gave in to pressure', 'closed': "approval: slanting a review's summary; backfire: another team reanalyses the review and says so in print", 'self_control': '-', 'chance': 0.9}),
    ("invoke the contract's clause that guarantees your right to publish", 'W1', 'R.7', 0.5, '', {'v': 'self-direction', 'chance': 0.75}),
    ('visit the families the course did help, to learn what the charity should keep', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, universalism', 'door': True, 'chance': 0.6}),
    ('offer the director a neutral wording that keeps both the client and the record', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'chance': 0.75}),
    ('throw out the draft and rerun the whole analysis from scratch, just to be sure', 'R1', 'U.7', 0.5, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.88}),
    ('settle the wording over a long lunch with the director, and keep the work coming', 'G1', 'B.7', 0.5, '', {'v': 'power', 'chance': 0.7}),
 ]},
{'name': 'a hundred studies and no agreement',
 'stages': 'young_adult adult mature elder',
 'age': (24, 75),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor',
 'requires': 'evidence synthesis specialist',
 'worlds': {'earth': 'a hundred studies passed the screening, they measure the same thing in forty ways, and the '
                     'policy team wants one number'},
 'timing': {'times': 'per evidence synthesis specialist: nearly every review meets studies that measure the same '
                     'thing in many ways, and a policy team that wants one number anyway comes a few times a year; '
                     'about 1 life in 2,000 ever works in evidence synthesis (estimate)'},
 'scenes': {'earth': [('',
                       'One hundred and four studies passed the screening, and they measure the same outcome in '
                       'thirty-eight different ways. The policy team wants one number by the end of the month.'),
                      ('W',
                       "The method's rules say what can be pooled and what cannot, and most of this cannot. {N} also "
                       'knows the policy team will decide either way, with or without the review.'),
                      ('U',
                       '{N} spreads the studies over the floor in piles by method. A pattern almost shows, the way a '
                       'face almost shows in a cloud.'),
                      ('B',
                       'A clean single number would get the review quoted for years, and {Ns} name with it. A list '
                       'of caveats gets quoted by nobody.'),
                      ('R',
                       'Three months of reading, and the honest answer is "it depends". {N} wants to laugh and throw '
                       'the whole stack in the air.'),
                      ('G',
                       'Every field goes through a muddle like this before it settles, the way a river runs muddy '
                       'after the spring rains. {N} has seen it before.')]},
 'outcomes': (['The review goes out with a clear answer to a narrower question, and the policy team uses it.',
               'The policy team accepts the honest muddle, and the next round of trials is designed around it.'],
              ['The deadline passes, and the decision is made without the review.',
               "The policy team takes a number from somewhere else, and nobody reads the review's caveats."]),
 'options': [
    ('report that the evidence cannot be pooled, and say exactly why', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.72}),
    ('sort the studies by method, card by card, every evening until the pattern shows', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'learned a skill', 'habit': True, 'self_control': '+', 'chance': 0.65}),
    ('send the best single estimate you can defend, under your own name', 'B1', None, 0.45, '', {'v': 'achievement, power', 'identity': True, 'chance': 0.82}),
    ('quietly drop the studies that muddy the picture, and go with your gut', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'hid a wrong', 'closed': 'approval: dropping studies without saying so; backfire: a methods reviewer finds the missing studies and says so in public', 'chance': 0.68}),
    ('tell the policy team to wait two years for the trials now running', 'G1', None, 0.45, '', {'v': 'tradition (patience), security', 'chance': 0.3}),
    ('keep strictly to the method, and work the weekends so the answer comes before the vote', 'W1', 'R.7', 0.5, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.55}),
    ('map where the studies disagree and why, so the next trials can grow from it', 'U1', 'G.7', 0.5, '', {'v': 'universalism', 'chance': 0.67}),
    ('trade the policy team a smaller, solid answer for the extra month you need', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'chance': 0.65}),
    ('follow the one strange subgroup that keeps turning up, wherever it leads', 'R1', 'U.7', 0.5, '', {'v': 'stimulation', 'chance': 0.35}),
    ('call on the old circle of reviewers who untangled this field once before', 'G1', 'B.7', 0.5, '', {'v': 'security, power', 'chance': 0.82}),
 ]},
{'name': 'the headline gets it wrong',
 'stages': 'young_adult adult mature elder',
 'age': (22, 75),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, rival',
 'requires': 'science communication specialist',
 'worlds': {'earth': 'your careful press release about a small study comes back as a national headline that promises '
                     'far too much'},
 'timing': {'times': 'per science communication specialist: a careful release that comes back as a headline '
                     'promising far too much happens a few times a year; even when UK university health releases did '
                     'not exaggerate, about 1 news story in 10 to 1 in 6 still did (Sumner and colleagues, BMJ '
                     '2014)'},
 'scenes': {'earth': [('',
                       'The press release {N} wrote said a study in mice suggests a possible link. By breakfast a '
                       "national paper's headline says chocolate halves the risk of dementia, and it is everywhere."),
                      ('W',
                       'People will change what they eat on the strength of that headline. {N} feels responsible for '
                       'every one of them, because the release went out under {Ns} name.'),
                      ('U',
                       '{N} lays the release beside the article and marks where the meaning slipped: one word in the '
                       'second paragraph, "may", quietly dropped by the paper.'),
                      ('B',
                       'The story has been shared two hundred thousand times, and {boss} has already forwarded the '
                       'numbers with three exclamation marks. The lead scientist has sent one line: call me.'),
                      ('R',
                       '{N} reads the headline on the bus and nearly shouts out loud. Someone across the aisle is '
                       'reading it too, nodding.'),
                      ('G',
                       'A story like this runs its course like a fever, high for three days and then gone. What '
                       'matters is what is left standing when it passes.')]},
 'outcomes': (['The correction runs the next day, and the story settles into something nearer the truth.',
               'The lead scientist calls back calmer, and the next release is written together.'],
              ['The headline outlives every correction, and {N} hears it repeated at a family dinner months later.',
               "The lead scientist stops answering, and the next study's news goes to another office."]),
 'options': [
    ('ask the paper for a correction, and publish a clarification of your own today', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.4}),
    ('quietly add the missing caveat to the online release, with no note of the change', 'U1', None, 0.45, '', {'v': 'security', 'mark': 'hid a wrong', 'closed': 'approval: changing a published release without notice; backfire: an archived copy shows the change, and a reporter writes about it', 'self_control': '-', 'chance': 0.8}),
    ('ride the wave and line up radio interviews while the story is hot', 'B1', None, 0.45, '', {'v': 'achievement, power', 'door': True, 'chance': 0.85}),
    ('ring the reporter and tell them exactly what you think of that headline', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'made an enemy', 'chance': 0.7}),
    ('let it blow over, and make the next release harder to twist', 'G1', None, 0.45, '', {'v': 'tradition (patience), security', 'chance': 0.65}),
    ('call the lead scientist before anyone else, and sort it out together', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'chance': 0.85}),
    ('write a plain explainer of what the study did and did not show', 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'chance': 0.7}),
    ('trade the reporter an exclusive on the next study for a fair follow-up now', 'B1', 'U.7', 0.5, '', {'v': 'power, universalism', 'chance': 0.5}),
    ('go on the breakfast show yourself and own the story before anyone else does', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'chance': 0.55}),
    ('sit with the lead scientist over a long coffee and let them get it all out', 'G1', 'R.7', 0.5, '', {'v': 'benevolence', 'chance': 0.9}),
 ]},
{'name': 'a live interview on a hard question',
 'stages': 'young_adult adult mature elder',
 'age': (22, 75),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'parent, boss, rival',
 'requires': 'science communication specialist',
 'worlds': {'earth': "on live radio the presenter wants a yes or a no on whether the town's water is safe, and the "
                     'honest answer takes longer'},
 'timing': {'times': 'per science communication specialist: a live interview that presses for a yes or a no on an '
                     'unsettled question comes a few times a year, and weekly during a local scare; about 1 life in '
                     '1,000 ever works as a science communicator (estimate)'},
 'scenes': {'earth': [('',
                       'The on-air light comes on, and the presenter turns to {N}: "So, is the town\'s water safe or '
                       'not? Yes or no." The honest answer takes more than ten seconds.'),
                      ('W',
                       'Thousands of people are listening at their kitchen tables, and some will decide tonight what '
                       'to give their children to drink. {N} owes them the truth, with its doubts left in.'),
                      ('U',
                       '{N} has three numbers ready, ranked, and a sentence for each. The trick is choosing the one '
                       'that survives being cut off halfway.'),
                      ('B',
                       'The presenter likes a fight, and the other guest is a local politician who wants one too. '
                       'Whoever sounds surest will win the hour.'),
                      ('R',
                       '{Ns} heart is going like a drum, and somehow it feels wonderful. This is what {N} trained '
                       'for.'),
                      ('G',
                       '{N} thinks of {parent}, listening at home with the radio on the windowsill, and decides to '
                       'answer as if talking to no one else.')]},
 'outcomes': (['The interview lands, and the phone-in afterwards is full of people saying they finally understand.',
               'A clip of {Ns} answer goes round the town, and the water board asks {N} to help with its next '
               'notice.'],
              ['The answer comes out tangled, and the presenter moves on with a shrug.',
               'The clip that spreads is the worst five seconds, cut out of context.']),
 'options': [
    ('give the honest answer, doubts and all, even if it sounds weak', 'W1', None, 0.45, '', {'v': 'universalism', 'chance': 0.55}),
    ('quote only the reassuring figure, and leave the other two unsaid', 'U1', None, 0.45, '', {'v': 'security, achievement', 'mark': 'hid a wrong', 'closed': 'approval: leaving out the worrying figures; backfire: the full figures are published the next week', 'chance': 0.75}),
    ('make sure you get the last word, and spend it on the one number that matters', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.65}),
    ('let your excitement show and tell them why this question keeps you up at night', 'R1', None, 0.45, '', {'v': 'stimulation', 'act': 'let their excitement show and tell the listeners why this question keeps them up at night', 'chance': 0.88}),
    ('talk it through the way you would with a neighbour over the fence', 'G1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.75}),
    ("give the water board's helpline twice, so worried families know where to turn", 'W1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'chance': 0.95}),
    ("correct the politician's wrong figure on air, calmly, with the source", 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'identity': True, 'mark': 'made an enemy', 'chance': 0.5}),
    ('steer every question back to the three points you came to make', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.75}),
    ('take the politician on head-first and win the room', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'chance': 0.6}),
    ('let the silence sit after the question, until the answer comes from the gut', 'G1', 'R.7', 0.5, '', {'v': 'self-direction', 'chance': 0.45}),
 ]},
{'name': 'the meeting in the village hall',
 'stages': 'young_adult adult mature elder',
 'age': (22, 75),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'moment',
 'roles': 'elder, colleague, boss',
 'requires': 'participatory research coordinator',
 'worlds': {'earth': 'the village hall is full, and the residents want to know why the flooding study they joined '
                     'still has no answer'},
 'timing': {'times': 'per participatory research coordinator: a full public meeting where the people in the study '
                     'ask why there is still no answer comes about once or twice a year; about 1 life in 2,000 ever '
                     'coordinates a community research project (estimate)'},
 'scenes': {'earth': [('',
                       'The village hall smells of tea urns and wet coats, and every chair is taken. The residents '
                       'want to know why, eighteen months in, the flooding study still has no answer.'),
                      ('W',
                       '{N} promised the village a report every quarter, and the last one was late. The minutes of '
                       'that meeting are pinned to the noticeboard by the door.'),
                      ('U',
                       '{N} has the first results in a folder: suggestive, not solid. Showing them now would answer '
                       'the room, and might mislead it.'),
                      ('B',
                       "The council's flood money will be shared out in the spring, to whichever village makes the "
                       'strongest case. Everyone in the hall knows it.'),
                      ('R',
                       'A farmer at the back stands up, flushed, and says his family has read this river for three '
                       'generations and nobody has asked them a thing. Half the room claps.'),
                      ('G',
                       "The hall was built by the villagers' grandparents after the great flood seventy years ago, "
                       'and the high-water mark is still painted on the wall beside the stage.')]},
 'outcomes': (['The meeting ends late but warmer, and the villagers sign up to keep measuring through the winter.',
               "The farmer comes over afterwards, and his family's flood notes go into the study."],
              ['Half the room walks out before the end, and the study loses its rain-gauge volunteers.',
               'The local paper reports the meeting as a row, and the council takes note.']),
 'options': [
    ('apologise for the late report, and set a date you can keep', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'mark': 'owned up', 'self_control': '+', 'chance': 0.8}),
    ('show the early results, with every doubt spelled out on the slide', 'U1', None, 0.45, '', {'v': 'universalism', 'identity': True, 'chance': 0.65}),
    ('tell them plainly the results will strengthen their case for the flood money', 'B1', None, 0.45, '', {'v': 'power', 'chance': 0.75}),
    ('invite the farmer to the front and hand him the microphone', 'R1', None, 0.45, '', {'v': 'benevolence, self-direction', 'mark': 'made a friend', 'chance': 0.75}),
    ('ask the oldest residents to mark on the map where the water has always come', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.85}),
    ("write the villagers' questions into the study plan, one by one, on the spot", 'W1', 'U.7', 0.5, '', {'v': 'universalism, conformity', 'binds': True, 'chance': 0.75}),
    ('sketch how a village network of rain gauges would make their case harder to ignore', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.75}),
    ('offer the loudest critics seats on the steering group, and let them run with it', 'B1', 'R.7', 0.5, '', {'v': 'power, self-direction', 'binds': True, 'chance': 0.7}),
    ('stay until the last chair is stacked, talking with whoever lingers', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'chance': 0.92}),
    ('let the village elders chair the next meeting, as the village did things before the study', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'chance': 0.5}),
 ]},
{'name': 'whose data are these',
 'stages': 'young_adult adult mature elder',
 'age': (22, 75),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, elder, friend',
 'requires': 'participatory research coordinator',
 'worlds': {'earth': "the journal wants the study's data made open, and the fishing families who gathered it say the "
                     'map of the fish is theirs'},
 'timing': {'times': 'per participatory research coordinator: a clash between a journal or funder asking for open '
                     'data and a community that says the data are its own comes perhaps once in each project, more '
                     'often as open-data rules spread (estimate)'},
 'scenes': {'earth': [('',
                       "The journal will publish the study only if the full dataset is made open. The fishermen's "
                       'association, who logged every catch for four years, says the map of where the fish are is '
                       'theirs, and not for the trawlers.'),
                      ('W',
                       'There is a signed partnership agreement, and {N} wrote half of it. It says the data are '
                       'shared, and it never says what shared means.'),
                      ('U',
                       '{N} works out what could be released safely: blurred locations, monthly totals. Whether that '
                       "still meets the journal's rules is another question."),
                      ('B',
                       'Whoever holds the map holds the fishing grounds. A trawler company has already asked, '
                       'through a friend of {boss}, what the data would cost.'),
                      ('R',
                       '{N} has been out on the boats at four in the morning, hauling nets with these people. '
                       'Handing their grounds to strangers would feel like betrayal.'),
                      ('G',
                       'Fishing families here have kept their best grounds to themselves for generations, passed '
                       'from parent to child. The study asked them to write those grounds down.')]},
 'outcomes': (['The data find a home that both the journal and the association can live with, and the study goes to '
               'press.',
               'The association agrees, and the skippers ask for the next study to be theirs from the start.'],
              ['The association withdraws, and four years of logbooks go back into a drawer at the harbour.',
               'The paper is rejected, and {boss} asks why {N} let it come to this.']),
 'options': [
    ("release the full data as the university's rules say, whatever the association thinks", 'W1', None, 0.45, '', {'v': 'conformity', 'mark': 'broke your word', 'closed': 'approval: releasing data the partners refused; backfire: the association pulls out and warns every harbour on the coast', 'self_control': '-', 'chance': 0.75}),
    ('release only blurred locations and monthly totals, and explain the method', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'identity': True, 'chance': 0.75}),
    ('offer the association a place among the authors and a share of any data income', 'B1', None, 0.45, '', {'v': 'achievement, power', 'chance': 0.58}),
    ('side with the fishers out loud, and tell the journal to publish without the data', 'R1', None, 0.45, '', {'v': 'benevolence, self-direction', 'chance': 0.3}),
    ('hand the data back to the association, and let them keep it', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'identity': True, 'mark': 'kept your word', 'self_control': '+', 'chance': 0.9}),
    ('ask the journal for the exception its own rules allow for community data', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'chance': 0.5}),
    ('design a licence that lets the association decide who gets the data, and charge for it', 'U1', 'B.7', 0.5, '', {'v': 'power, self-direction', 'binds': True, 'chance': 0.6}),
    ('find a journal with looser rules and publish there, free of the fight', 'B1', 'R.7', 0.5, '', {'v': 'self-direction', 'chance': 0.75}),
    ('go down to the harbour at dawn and hear the families out on the boats', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'door': True, 'grants': 'community partners', 'chance': 0.8}),
    ("let the association's oldest skippers decide, the way the harbour settles things", 'G1', 'W.7', 0.5, '', {'v': 'tradition', 'chance': 0.55}),
 ]},
{'name': 'the same stretch of river, every Sunday',
 'stages': 'child juvenile young_adult adult mature elder',
 'age': (12, 95),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'leisure, nature',
 'horizon': 'months',
 'roles': 'friend, parent, elder',
 'requires': 'citizen scientist',
 'worlds': {'earth': 'thirty Sundays in a row you have counted the same mile of river, and this morning it is '
                     'raining sideways'},
 'timing': {'times': 'per citizen scientist with a regular count: a count day when rain or a hard week makes going a '
                     'chore comes several times a season; about 1 US adult in 10 takes part in citizen science in a '
                     'year (Pew Research Center 2020), and about 6 lives in 100 keep at it (estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Thirty Sundays in a row {N} has walked the same mile of river with a clipboard. This morning '
                       'it is raining sideways, and the warm kitchen is right there.'),
                      ('W',
                       'The survey needs the same mile counted every week, or the line on its graph breaks. {N} '
                       'signed up for the whole year.'),
                      ('U',
                       'The counts have been flat for weeks, and {N} has started to wonder whether the method can '
                       'see a real change, or only the weather.'),
                      ('B',
                       "The survey's app ranks its volunteers by records sent in, and {N} is fourth in the region. "
                       'One more good season and the top spot is in reach.'),
                      ('R',
                       '{N} loved the first Sundays: the kingfisher, the mist, the mud. Lately it feels like '
                       'homework.'),
                      ('G',
                       'The river is different every week and the same every year: the alders leaf, the water drops, '
                       'the herons come back. {N} has started to feel the year the way a farmer does.')]},
 'outcomes': (["The Sundays find their rhythm again, and by autumn {Ns} records fill a whole stretch of the survey's "
               'map.',
               'One wet morning a kingfisher lands a few feet away, and {N} remembers why this started.'],
              ["{N} misses three Sundays in a row, and the survey's line for this stretch of river goes blank.",
               'The counts stay flat and grey, and the clipboard ends up on a shelf by the door.']),
 'options': [
    ('go out in the rain anyway; a promise to the survey is a promise', 'W1', None, 0.45, '', {'v': 'conformity', 'habit': True, 'mark': 'kept your word', 'self_control': '+', 'chance': 0.88}),
    ('read up on the method, to see whether the flat counts mean anything', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'door': True, 'chance': 0.85}),
    ('aim for the top spot, and add a second stretch of river on Saturdays', 'B1', None, 0.45, '', {'v': 'achievement', 'habit': True, 'self_control': '+', 'chance': 0.82}),
    ('take the day off and do something completely different', 'R1', None, 0.45, '', {'v': 'hedonism', 'self_control': '-', 'chance': 0.95}),
    ('stay home and write in the usual numbers; the river never changes this time of year', 'G1', None, 0.45, '', {'v': 'tradition, hedonism', 'mark': 'hid a wrong', 'closed': 'approval: entering counts that were never made; backfire: a survey checker spots rows that never change', 'self_control': '-', 'chance': 0.88}),
    ('ask the survey for a proper training day, so your records count as expert ones', 'W1', 'B.7', 0.5, '', {'v': 'achievement, power', 'door': True, 'chance': 0.5}),
    ('set a cheap trail camera on the bank to catch what you miss', 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'mark': 'learned a skill', 'chance': 0.65}),
    ('talk the angling club into letting you walk their private bank as well', 'B1', 'G.7', 0.5, '', {'v': 'power, universalism', 'act': 'talk the angling club into letting them walk its private bank as well', 'chance': 0.55}),
    ('talk a friend into coming every week, so the count never misses a Sunday', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'mark': 'made a friend', 'binds': True, 'chance': 0.65}),
    ('keep a notebook of what the river does beyond the count: water, leaves, light', 'G1', 'U.7', 0.5, '', {'v': 'universalism', 'habit': True, 'aims': 'community observer', 'chance': 0.7}),
 ]},
{'name': 'your record does not match the official one',
 'stages': 'child juvenile young_adult adult mature elder',
 'age': (12, 95),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'leisure, nature, community',
 'horizon': 'months',
 'roles': 'friend, grandparent, elder',
 'requires': 'citizen scientist',
 'worlds': {'earth': 'your water tests from the brook show a sharp rise after every storm, and the official station '
                     'shows nothing at all'},
 'timing': {'times': 'per citizen scientist who measures what an official station also measures: a clear, lasting '
                     'mismatch with the official record turns up perhaps once in several years; many such gaps come '
                     'from method, and some point to something real (estimate)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{Ns} water tests from the brook behind {place} show a sharp rise every time it rains. The '
                       "agency's official station, two miles downstream, shows nothing at all."),
                      ('W',
                       "The agency's figures are the ones the law listens to, and {N} has always trusted them. Now "
                       'one of the two records must be wrong.'),
                      ('U',
                       '{N} lays the two records side by side. The station samples once a month, on a fixed day; '
                       '{Ns} tests catch the hours after a storm. Both could be right.'),
                      ('B',
                       "The agency's reply was polite and short: volunteer data cannot be used. {N} notices that a "
                       'reply like that is easiest to write when nobody else is asking.'),
                      ('R',
                       '{N} has watched the brook go cloudy and smell of the farm after every downpour. A '
                       'spreadsheet will not talk {N} out of what {Ns} own eyes saw.'),
                      ('G',
                       'The brook runs past the house where {grandparent} grew up. Something in it has changed, the '
                       "way an old friend's face changes when they are unwell.")]},
 'outcomes': (["The agency sends someone out after a storm, and the next month's official figures show the rise.",
               "The records are checked, and {Ns} name goes on the survey's list of volunteers whose data it "
               'trusts.'],
              ['The agency files the readings away unread, and the brook goes on clouding after every storm.',
               'The test kit turns out to have been faulty all along, and {N} has to start again from scratch.']),
 'options': [
    ('delete the odd readings from your log, since the official station must be right', 'W1', None, 0.45, '', {'v': 'conformity', 'mark': 'hid a wrong', 'closed': "approval: deleting one's own data to fit; backfire: the survey's checkers see the gaps and ask why", 'self_control': '-', 'chance': 0.9}),
    ('buy a better test kit and sample both spots at the same hour for a month', 'U1', None, 0.45, '', {'v': 'achievement', 'habit': True, 'self_control': '+', 'mark': 'learned a skill', 'chance': 0.75}),
    ('take your numbers to the local paper before the agency can shrug them off', 'B1', None, 0.45, '', {'v': 'power', 'identity': True, 'mark': 'made an enemy', 'chance': 0.7}),
    ('post the photos of the cloudy brook online and tag the agency', 'R1', None, 0.45, '', {'v': 'self-direction', 'chance': 0.55}),
    ('ask the farmers upstream, who know the brook, what has changed this year', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.65}),
    ('get the parish council to log the complaint officially, so the agency has to answer', 'W1', 'B.7', 0.5, '', {'v': 'power, conformity', 'chance': 0.45}),
    ('rig up a cheap sensor that tests the brook every hour, even at night', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, achievement', 'chance': 0.47}),
    ('offer the upstream farmer your records in return for a look at his drains', 'B1', 'G.7', 0.5, '', {'v': 'universalism, security', 'chance': 0.65}),
    ('go out in the storm at night to take the sample that settles it', 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'body': 'light', 'mark': 'took a wild risk', 'chance': 0.55}),
    ('keep testing quietly, season after season, until the pattern speaks for itself', 'G1', 'U.7', 0.5, '', {'v': 'universalism, tradition', 'self_control': '+', 'habit': True, 'chance': 0.5}),
 ]},
{'name': 'forty years of rain in one notebook',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (12, 100),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'leisure, nature, friends',
 'horizon': 'week',
 'roles': 'elder, friend',
 'requires': 'community observer',
 'worlds': {'earth': 'the rain record has no gap in forty years, and a three-week trip with a friend would make the '
                     'first one'},
 'timing': {'times': 'per community observer: a trip, an illness or a family need that would break the record comes '
                     'up every year or two; records with no gap for decades are rare, and about 1 life in 50 ever '
                     'keeps a long record of one place (estimate)'},
 'scenes': {'earth': [('',
                       'The rain notebook has no gap in forty years: {elder} read the gauge every morning at nine '
                       'for most of them, and {N} has done it since. Now {friend} has asked {N} along on a '
                       'three-week trip, and the record would break.'),
                      ('W',
                       'Forty years, no gaps: that is what makes the notebook worth anything to the weather service. '
                       '{N} feels the weight of every one of those mornings.'),
                      ('U',
                       '{N} wonders how much a three-week gap really costs the record, and whether the nearest '
                       "station's readings could fill it honestly."),
                      ('B',
                       'In the wet months a three-week hole would cost the record most; in the dry ones hardly '
                       'anything. {N} starts working out how to get {friend} to wait.'),
                      ('R',
                       'Three weeks somewhere new, with {friend}: {N} wants it so badly that the notebook on the '
                       'windowsill starts to look like a chain.'),
                      ('G',
                       'Rain falls whether anyone writes it down or not. Still, the morning walk to the gauge has '
                       'become as much a part of {N} as breakfast.')]},
 'outcomes': (['The record runs on without a break, and the old notebook stays in its place on the windowsill.',
               'The weather service writes to say the long record helped it check a new flood model.'],
              ['A storm comes the one week nobody was watching, and the notebook will always have a hole where it '
               'should be.',
               '{friend} goes without {N}, and things between them are cooler for a while.']),
 'options': [
    ('turn the trip down; the record comes first', 'W1', None, 0.45, '', {'v': 'conformity, tradition', 'mark': 'turned down a chance', 'chance': 0.9}),
    ('leave the gap, and fill it from the nearest station, clearly marked as such', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'chance': 0.88}),
    ('get your friend to move the trip to the dry season, when a gap costs least', 'B1', None, 0.45, '', {'v': 'self-direction, achievement', 'chance': 0.73}),
    ('go on the trip, and fill in the three weeks afterwards with a good guess', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'mark': 'hid a wrong', 'closed': 'approval: inventing readings for a public record; backfire: the weather service compares them with the nearest station and asks questions', 'self_control': '-', 'chance': 0.9}),
    ('go, and let the gap come; rain falls the same whether written down or not', 'G1', None, 0.45, '', {'v': 'tradition (acceptance), hedonism', 'chance': 0.92}),
    ("follow the weather service's rules for a stand-in observer, then go with a clear head", 'W1', 'R.7', 0.5, '', {'v': 'hedonism, conformity', 'chance': 0.58}),
    ('set up an automatic gauge beside the old one, so the record runs on', 'U1', 'G.7', 0.5, '', {'v': 'security', 'mark': 'learned a skill', 'chance': 0.72}),
    ('ask the weather service to pay for an automatic gauge, since it uses your figures', 'B1', 'W.7', 0.5, '', {'v': 'security, power', 'chance': 0.55}),
    ('take a rain gauge on the trip and keep a second notebook there', 'R1', 'U.7', 0.5, '', {'v': 'stimulation', 'door': True, 'chance': 0.85}),
    ("teach a younger relative the gauge, so the record stays in the family's hands", 'G1', 'B.7', 0.5, '', {'v': 'tradition, power', 'binds': True, 'chance': 0.7}),
 ]},
{'name': 'the developers want your survey',
 'stages': 'juvenile young_adult adult mature elder',
 'age': (12, 100),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.07,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'nature, community, money',
 'horizon': 'months',
 'roles': 'elder, friend, rival',
 'requires': 'community observer',
 'worlds': {'earth': 'a builder wants houses on the meadow you have surveyed for years, and its consultants ask for '
                     'your records, for a fee'},
 'timing': {'times': 'per community observer: a builder or its consultants asking for the records of a surveyed '
                     'place comes perhaps once in ten to twenty years of keeping them, more often near growing towns '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       'A builder plans eighty houses on the meadow behind {place}, and its consultants have written '
                       'asking for {Ns} survey records: years of birds, flowers and moths, field by field. They '
                       'offer a fee.'),
                      ('W',
                       'There is a public planning process, and evidence should go to it openly, whoever it helps. '
                       '{N} believes in that, and finds it harder to believe this week.'),
                      ('U',
                       '{N} knows what the records show: the meadow is richer than anything around it, except in the '
                       'two dry years. A careless reader could make the dry years the whole story.'),
                      ('B',
                       'The fee is more money than the records have ever earned. And whoever holds the only long '
                       'record of the meadow holds a card in this game.'),
                      ('R',
                       'The thought of diggers on the meadow makes {Ns} hands shake. {N} wants to tear the letter in '
                       'half.'),
                      ('G',
                       'Skylarks nest in the long grass every spring, and they were there before the town. {N} has '
                       'watched generation after generation of them rise.')]},
 'outcomes': (["The records reach the planning hearing, and the meadow's two best fields are left out of the plan.",
               "The consultants' report has to quote {Ns} figures in full, and the builder redraws the scheme."],
              ['The houses are approved anyway, and {Ns} records are quoted in the report as proof the meadow is '
               'ordinary.',
               'The neighbours argue about what {N} did, and the street splits over it.']),
 'options': [
    ('send the records to the planning office, where everyone can see them', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.6}),
    ('send the consultants the records with a careful note on what the dry years mean', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'chance': 0.55}),
    ('sell the builder the records, and take the fee', 'B1', None, 0.45, '', {'v': 'achievement, security', 'chance': 0.92}),
    ('refuse flat out, and tell the builder what you think of eighty houses on a meadow', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'made an enemy', 'chance': 0.45}),
    ('keep the records to yourself; the meadow is not theirs to measure', 'G1', None, 0.45, '', {'v': 'tradition', 'identity': True, 'chance': 0.9}),
    ('register as a formal objector, so you can speak at the hearing', 'W1', 'R.7', 0.5, '', {'v': 'universalism, self-direction', 'identity': True, 'door': True, 'chance': 0.67}),
    ('map where on the site the rare plants grow, so any plan has to spare them', 'U1', 'G.7', 0.5, '', {'v': 'universalism', 'grants': 'fieldwork', 'chance': 0.6}),
    ('demand that the builder pay for an independent survey before anything is decided', 'B1', 'W.7', 0.5, '', {'v': 'universalism, power', 'chance': 0.55}),
    ('throw yourself into a dawn-to-dusk survey this June, to catch everything that lives there', 'R1', 'U.7', 0.5, '', {'v': 'achievement, stimulation', 'body': 'light', 'chance': 0.55}),
    ("ask the landowner's family, who have known you for years, not to sell", 'G1', 'B.7', 0.5, '', {'v': 'power, tradition', 'act': "ask the landowner's family, who have known them for years, not to sell", 'chance': 0.23}),
 ]},
{'name': 'volunteers drifting away',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'community, leisure',
 'horizon': 'months',
 'roles': 'friend, elder, colleague',
 'requires': 'volunteer research organiser',
 'worlds': {'earth': 'the volunteer survey you organise had sixty people three years ago, and this spring twenty-two '
                     'turn up'},
 'timing': {'times': 'per volunteer research organiser: a clear fall in turnout over a few seasons comes every few '
                     'years in most volunteer projects, as founders age and newcomers move on; about 3 lives in '
                     '1,000 ever organise volunteer research (estimate)'},
 'scenes': {'earth': [('',
                       'Three years ago sixty volunteers came to the spring briefing. This year {N} counts '
                       'twenty-two chairs filled, and half the faces are grey.'),
                      ('W',
                       'Every volunteer signed up for a season, and a season is what the survey needs to mean '
                       'anything. {N} keeps the register, and its gaps hurt.'),
                      ('U',
                       '{N} goes through the old sign-up sheets: people drop away in the third month, almost always '
                       'after the long winter counts. There is a pattern there.'),
                      ('B',
                       "The grant that pays for the kits asks for volunteer numbers in its report, and this year's "
                       'numbers will not look good.'),
                      ('R',
                       'The first year was a joy: muddy boots, the pub after every count, people laughing in the '
                       'rain. Somewhere along the way it became a chore, and {N} misses the fun as much as the '
                       'people.'),
                      ('G',
                       "Groups like this rise and fall like a tide; {N} saw the old naturalists' society shrink and "
                       'come back. The ones who stay are like family now.')]},
 'outcomes': (['By autumn the chairs are fuller, and two of the new faces are leading counts of their own.',
               'The survey shrinks but steadies, and the people who stay say it is the best season yet.'],
              ['The spring count goes ahead with nine people, and two sites are left uncounted.',
               "The funder's report goes in late and thin, and the kit grant is cut for next year."]),
 'options': [
    ('ring every lapsed volunteer in turn, and ask kindly whether they will be back', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'chance': 0.6}),
    ("count every one-off visitor as a volunteer in the funder's report", 'U1', None, 0.45, '', {'v': 'security, achievement', 'mark': 'hid a wrong', 'closed': 'approval: inflating the numbers in a report to a funder; backfire: the funder asks to see the sign-in sheets', 'self_control': '-', 'chance': 0.75}),
    ('offer every regular a kit of their own to keep, if they stay the whole season', 'B1', None, 0.45, '', {'v': 'achievement', 'chance': 0.75}),
    ('bring back the pub after every count, and make it fun again', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'habit': True, 'chance': 0.9}),
    ('let the drifting ones go, and look after the twenty-two who stayed', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'chance': 0.85}),
    ('set up a buddy system, so no newcomer counts alone in their first season', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'grants': 'organising people', 'chance': 0.8}),
    ('cut the winter counts to the ones the analysis truly needs, and write down why', 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'chance': 0.65}),
    ('recruit at the university each term, where students need field hours for their degrees', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'habit': True, 'chance': 0.75}),
    ('throw a big launch with the local radio, and make the survey the thing to join', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'chance': 0.4}),
    ('hand the night walks to the youngest volunteers, and let them run them their way', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, benevolence', 'chance': 0.55}),
 ]},
{'name': "a scientist wants your volunteers' data",
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'community, work',
 'horizon': 'months',
 'roles': 'mentor, friend, elder',
 'requires': 'volunteer research organiser',
 'worlds': {'earth': "a professor wants the survey's ten years of volunteer records for a big paper, with your name "
                     'on it and a line of thanks for the rest'},
 'timing': {'times': "per volunteer research organiser: a professional scientist asking for the project's long "
                     'volunteer records for a paper comes perhaps once every few years, once the records run to a '
                     'decade or more (estimate)'},
 'scenes': {'earth': [('',
                       "A professor from the university has found the survey's ten years of records online and wants "
                       'them for a major paper. The offer: {Ns} name among the authors, and a line of thanks for '
                       '"the volunteers".'),
                      ('W',
                       'Two hundred people collected those records in all weathers. A line of thanks under a '
                       "professor's name does not seem a fair account of who did the work."),
                      ('U',
                       'A real analysis could answer the question the volunteers have wondered about for years, '
                       'which the group could never answer alone.'),
                      ('B',
                       'A name on a paper in a big journal would open doors for {N} that ten years of organising '
                       'never did. The professor knows that, and so does {N}.'),
                      ('R',
                       'The professor\'s email called the volunteers "a resource". {N} read the word aloud at the '
                       'kitchen table, then read it again, louder.'),
                      ('G',
                       'The data grew the way a hedge grows, a little each year, tended by many hands. {N} has never '
                       "thought of it as anyone's to give away.")]},
 'outcomes': (["The paper comes out with the volunteers' names in it, and the group reads it aloud at the next "
               'count.',
               "The professor agrees to the group's terms, and a second study is planned together."],
              ["The professor takes the data from the public pages anyway, and the group's work appears under other "
               'names.',
               'The volunteers split over the offer, and three of the longest-serving ones stop coming.']),
 'options': [
    ('agree only if every regular volunteer is named in the paper', 'W1', None, 0.45, '', {'v': 'universalism', 'identity': True, 'chance': 0.5}),
    ('ask the professor to share the analysis with the group before it is published', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'chance': 0.6}),
    ('take the authorship, and say nothing to the volunteers until the paper is out', 'B1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': "approval: giving away the group's data without asking it; backfire: a volunteer finds the paper and asks the group how it happened", 'grants': 'published research', 'chance': 0.85}),
    ('put the offer to the volunteers at the next count, and let them shout it out', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'chance': 0.9}),
    ('say no; the data stays with the people who gathered it', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'turned down a chance', 'identity': True, 'chance': 0.92}),
    ('write simple terms for any scientist who wants the data, and let the group vote', 'W1', 'G.7', 0.5, '', {'v': 'conformity, universalism', 'binds': True, 'chance': 0.85}),
    ('look up how the professor has treated volunteers in past papers', 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'chance': 0.75}),
    ("bargain for a second paper written by the volunteers themselves, with the professor's help", 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.4}),
    ('ring the professor and say the price is real credit, or no data', 'R1', 'B.7', 0.5, '', {'v': 'power, self-direction', 'chance': 0.55}),
    ('invite the professor out on a dawn count first, to meet the people and the place', 'G1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'chance': 0.45}),
 ]},
{'name': 'the protocol says one thing, the supervisor another',
 'stages': 'young_adult adult mature',
 'age': (20, 67),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, mentor',
 'requires': 'research assistant',
 'worlds': {'earth': 'the written protocol says one thing, your supervisor says to do it another way, and the '
                     'samples are due Friday'},
 'timing': {'times': 'per research assistant: a supervisor asks for a way of working the written protocol does not '
                     'allow, with a deadline close, perhaps once or twice a year; about 1 life in 50 ever holds a '
                     'research assistant post (estimate)'},
 'scenes': {'earth': [('',
                       'The written protocol on the bench says three washes. {boss} has just told {N} to skip the '
                       'third and run the samples tonight, because Friday is close.'),
                      ('W',
                       'Every step in a protocol is there because someone once got it wrong. If a step changes, the '
                       'lab book is supposed to say so, and say who decided.'),
                      ('U',
                       'The protocol was written for the old reagent. {N} suspects {boss} may be right about the '
                       'third wash, and wants to know for certain.'),
                      ('B',
                       '{boss} writes the reference letters, and {N} will need one by spring. A wash step is not the '
                       'hill to stand on. Or is it?'),
                      ('R',
                       'Being told one thing on paper and another out loud makes {N} want to say so, right now, in '
                       'front of everyone.'),
                      ('G',
                       '{colleague}, who has worked at this bench for twenty years, shrugs: the protocol and the '
                       'supervisors have always disagreed, and the lab goes on.')]},
 'outcomes': (['The samples go out on Friday, and the lab book says exactly what was done.',
               '{boss} looks into it, and the step is settled for everyone, in writing.'],
              ['The Friday run comes back noisy, and nobody can say for sure which step to blame.',
               '{boss} takes it badly, and for a week {N} gets only the dullest jobs on the rota.']),
 'options': [
    ('follow the written protocol, since it is the version everyone signed', 'W1', None, 0.45, '', {'v': 'conformity, security', 'self_control': '+', 'chance': 0.75}),
    ('look up the new reagent and work out which way gives cleaner data', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'mark': 'learned a skill', 'chance': 0.75}),
    ("do it the supervisor's way, and keep a private note in case it goes wrong", 'B1', None, 0.45, '', {'v': 'security, power', 'chance': 0.95}),
    ('tell the supervisor straight out that skipping the step feels wrong', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'defied an authority', 'chance': 0.75}),
    ('ask the oldest hand in the lab how this has been settled before', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.7}),
    ('put your objection in the lab book, on record and off your chest', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, conformity', 'chance': 0.92}),
    ('dig through the old lab books to learn why the third wash was ever added', 'U1', 'G.7', 0.5, '', {'v': 'tradition, self-direction', 'chance': 0.7}),
    ('agree to skip it only if the supervisor signs the change in the lab book', 'B1', 'W.7', 0.5, '', {'v': 'security, conformity', 'chance': 0.75}),
    ('stay late and run half the samples each way, to see who is right', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, achievement', 'self_control': '+', 'chance': 0.9}),
    ('skip the step as the lab always does, and log it as done', 'G1', 'B.7', 0.5, '', {'v': 'conformity, security', 'mark': 'hid a wrong', 'closed': 'approval: a lab record that does not match the work; backfire: a later audit finds the samples and the record disagree', 'self_control': '-', 'chance': 0.75}),
 ]},
{'name': 'your name is not on the paper',
 'stages': 'young_adult adult mature',
 'age': (20, 67),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor',
 'requires': 'research assistant',
 'worlds': {'earth': "the draft of the lab's paper goes round, and the method you built is in it, but your name is "
                     'not'},
 'timing': {'times': 'per research assistant: a paper built partly on their work goes round without their name '
                     'perhaps once in every two or three years in the post; technical and support staff are left off '
                     'author lists far more often than scientists (estimate)'},
 'scenes': {'earth': [('',
                       'The draft goes round the lab on Monday. The method {N} spent four months getting to work is '
                       'on page three; {Ns} name is not on page one, only "the technical staff" in the thanks.'),
                      ('W',
                       "The journal's authorship rules are pinned above the printer. {N} reads them again, line by "
                       'line, and tries to read them fairly.'),
                      ('U',
                       '{N} goes through the figures one by one: two, three and five could not exist without the '
                       'method. Whether that makes {N} an author is another question, and {N} wants it answered '
                       'properly.'),
                      ('B',
                       'A first paper is what the next application will ask for. Without a name on this one, {N} is '
                       'still a pair of hands for hire.'),
                      ('R',
                       '{N} reads the author list on the bus home, and the heat climbs from the collar to the ears.'),
                      ('G',
                       '{mentor} once said that in every lab the quiet work holds up the loud work, and the quiet '
                       'work is seldom named. {N} remembers it now, and is not sure it helps.')]},
 'outcomes': (['{boss} reads the case again, and the next version of the draft has {Ns} name on it.',
               'The matter is settled in a way {N} can live with, and the bench feels like {Ns} own again.'],
              ['The paper goes to the journal as it was, and the method appears under other names.',
               '{boss} hears about it second-hand, and the lab is cool towards {N} for weeks.']),
 'options': [
    ("ask the supervisor to check the list against the journal's authorship rules", 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'chance': 0.65}),
    ('list exactly what you did, figure by figure, and send it to the first author', 'U1', None, 0.45, '', {'v': 'achievement', 'identity': True, 'chance': 0.6}),
    ('refuse to hand over the code until your name goes on the paper', 'B1', None, 0.45, '', {'v': 'power', 'mark': 'made an enemy', 'closed': 'approval: holding back shared lab work; backfire: you are taken off the project and the code is rewritten without you', 'chance': 0.45}),
    ("type your own name into the draft's author list, in plain sight", 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'mark': 'defied an authority', 'closed': 'approval: changing the author list without asking; backfire: the first author deletes it and tells the supervisor', 'chance': 0.3}),
    ('take it in your stride: the method works, and that was the point', 'G1', None, 0.45, '', {'v': 'tradition (acceptance)', 'chance': 0.9}),
    ('ask for a written lab rule on credit, for the sake of every assistant here', 'W1', 'R.7', 0.5, '', {'v': 'universalism, benevolence', 'identity': True, 'chance': 0.45}),
    ('write the method up as a protocol, and apply to stay on as its scientist', 'U1', 'G.7', 0.5, '', {'title': 'research scientist', 'requires': 'doctoral graduate', 'without': 'approval', 'v': 'achievement, security', 'mark': 'learned a skill', 'chance': 0.12}),
    ('trade this paper for a written promise of first place on the next one', 'B1', 'W.7', 0.5, '', {'v': 'security, achievement', 'binds': True, 'grants': 'credit negotiation', 'self_control': '+', 'chance': 0.6}),
    ('throw yourself into improving the analysis until the paper cannot do without it', 'R1', 'U.7', 0.5, '', {'v': 'achievement, stimulation', 'self_control': '+', 'chance': 0.8}),
    ('let it pass and wait; when the method is needed again, they will come asking', 'G1', 'B.7', 0.5, '', {'v': 'power', 'chance': 0.5}),
 ]},
{'name': 'a careful result that says no',
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor',
 'requires': 'research scientist',
 'worlds': {'earth': 'three years of careful work say the opposite of what you hoped, and the report to the funder '
                     'is due next month'},
 'timing': {'times': 'per research scientist: a careful result against the hypothesis comes every year or two, and '
                     'one that lands with a report due perhaps once in three years; roughly half of honest studies '
                     'end null or inconclusive; about 1 life in 80 ever holds such a post (estimate)'},
 'scenes': {'earth': [('',
                       'The last batch of data is in, and it is clean. It says the effect {N} has chased for three '
                       'years is not there, and the report to the funder is due in four weeks.'),
                      ('W',
                       'The funder paid for an honest answer, not a happy one. {N} opens the report template at the '
                       'section headed "Findings" and sits with the cursor blinking.'),
                      ('U',
                       '{N} checks the controls, the sample size and the code. Everything holds. Now the interesting '
                       'question is why the idea was wrong.'),
                      ('B',
                       'The next grant depends on this report, and a "no" is a hard thing to sell. {N} starts '
                       'turning over what else is in the data.'),
                      ('R',
                       '{N} stares at the plot for a long minute, then shuts the laptop hard and walks out into the '
                       'cold without a coat.'),
                      ('G',
                       '{mentor} used to say that nature does not care what anyone hoped. The lake outside the '
                       'window looks exactly as it did three years ago.')]},
 'outcomes': (["The report goes in on time, and the funder's reply asks to see the next proposal.",
               '{colleague} reads the result and says it will save the whole field a few wasted years.'],
              ["The funder's letter is polite and short, and the next call does not mention the topic at all.",
               '{N} spends a month on it and still cannot make the result sit right.']),
 'options': [
    ('write the report as it stands: a clean null result, plainly stated', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'identity': True, 'chance': 0.85}),
    ('redo the whole analysis from scratch to be sure the null is real', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.85}),
    ('find an outcome in the data that did come out, and lead the report with it', 'B1', None, 0.45, '', {'v': 'achievement, power', 'mark': 'hid a wrong', 'closed': 'approval: reporting a side result as if it were the main question; backfire: a reviewer asks for the original plan and sees the switch', 'self_control': '-', 'chance': 0.75}),
    ('stand up at the group meeting and say it plainly: the idea was wrong', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'owned up', 'chance': 0.9}),
    ('let the hypothesis go, and ask what the system is really doing', 'G1', None, 0.45, '', {'v': 'universalism, self-direction', 'door': True, 'grants': 'a nose for the odd result', 'chance': 0.7}),
    ('deposit the full data in a public archive, so the record stays whole', 'W1', 'G.7', 0.5, '', {'v': 'universalism', 'chance': 0.6}),
    ('plan a bounded follow-up the funder can trust, and propose it in the report', 'U1', 'W.7', 0.5, '', {'v': 'security, achievement', 'binds': True, 'grants': 'experimental design', 'chance': 0.6}),
    ('talk the funder into a project of your own on the new explanation', 'B1', 'U.7', 0.5, '', {'title': 'research project lead', 'requires': 'research grant', 'without': 'impossible', 'v': 'achievement, power', 'door': True, 'chance': 0.1}),
    ('ring the funder today and sell the surprise as the bigger story', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'chance': 0.5}),
    ('go back to the field site and watch until the old excitement comes back', 'G1', 'R.7', 0.5, '', {'v': 'stimulation, hedonism', 'body': 'light', 'chance': 0.7}),
 ]},
{'name': 'the reviewers come back',
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, rival, mentor',
 'requires': 'research scientist',
 'worlds': {'earth': 'the reviews of your paper come back: one criticism is fair and hits hard, another is plainly '
                     'wrong'},
 'timing': {'times': 'per research scientist: reviews of a submitted paper come back a few times a year, nearly '
                     'always a mix of fair points and some that miss; most papers are revised at least once before '
                     'acceptance; about 1 life in 80 ever holds such a post (estimate)'},
 'scenes': {'earth': [('',
                       'The reviews arrive on a Sunday night. The second reviewer has found a real weakness in the '
                       'sampling, and on the same page has misread the main figure.'),
                      ('W',
                       'The journal allows sixty days and asks for a reply to every point, in order. {N} opens a '
                       'blank table with two columns: the comment, and the answer.'),
                      ('U',
                       'The weakness is real; {N} can see now that a wider sample would have closed it. The '
                       'misreading is just as plain, and {N} can already see the panel that would prevent it.'),
                      ('B',
                       '{N} is fairly sure the second reviewer is {rival}, who has a paper on the same question '
                       'coming out elsewhere.'),
                      ('R',
                       'The first reading leaves {N} pacing the kitchen at midnight, composing replies that could '
                       'never be sent.'),
                      ('G',
                       '{N} sleeps on it. By morning the reviews read differently: half of it is a gift, and half is '
                       'weather that will pass.')]},
 'outcomes': (['The revised paper goes back, and the editor accepts it with one small change.',
               'The fair point makes the paper better, and {N} says so in the reply without flinching.'],
              ['The second round of reviews is harsher than the first, and the paper is rejected.',
               "The reply takes four months instead of one, and {rival}'s paper comes out first."]),
 'options': [
    ('answer every point in order, politely, conceding what is fair', 'W1', None, 0.45, '', {'v': 'conformity', 'chance': 0.65}),
    ('try other tests on the data until the weakness goes away', 'U1', None, 0.45, '', {'v': 'achievement', 'mark': 'hid a wrong', 'closed': 'approval: choosing the test to fit the result; backfire: a reader re-runs the data and the effect is gone', 'self_control': '-', 'chance': 0.75}),
    ('do the extra sampling over your weekends, and answer the fair point in full', 'B1', None, 0.45, '', {'v': 'achievement, power', 'self_control': '+', 'chance': 0.85}),
    ('write the whole reply in one fierce weekend, while the fire lasts', 'R1', None, 0.45, '', {'v': 'stimulation, achievement', 'chance': 0.85}),
    ('ask your old supervisor how they would weigh these reviews', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.8}),
    ('narrow the claim to what the sample can bear, and let the rest go', 'W1', 'G.7', 0.5, '', {'v': 'universalism, conformity', 'chance': 0.75}),
    ('add a clear new panel that shows the misreading, so the editor can judge', 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'chance': 0.65}),
    ('hire a statistician with the leftover budget to answer the fair point properly', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'door': True, 'chance': 0.75}),
    ('fire back a sharp reply that wins the argument on the misread figure', 'R1', 'B.7', 0.5, '', {'v': 'power, achievement', 'mark': 'made an enemy', 'self_control': '-', 'chance': 0.4}),
    ('put the reviews away for a week and spend it in the field', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, self-direction', 'body': 'light', 'chance': 0.65}),
 ]},
{'name': 'the budget will not stretch to everything',
 'stages': 'young_adult adult mature',
 'age': (27, 75),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'research project lead',
 'worlds': {'earth': 'halfway through your project the money will not cover everything you promised: the people, the '
                     'samples and the field season'},
 'timing': {'times': 'per research project lead: money that will not cover everything promised comes about once in '
                     'each project, most often past the halfway point as costs rise; about 1 life in 200 ever leads '
                     'a research project (estimate)'},
 'scenes': {'earth': [('',
                       'Halfway through the project, the spreadsheet says it plainly: the money will not cover the '
                       'last field season, the second postdoc year and the sequencing all at once.'),
                      ('W',
                       '{N} rereads what the project promised the funder and the team. Every line was a promise, and '
                       'somebody, perhaps {colleague}, will have to be told which one breaks.'),
                      ('U',
                       '{N} builds three versions of the remaining year, line by line, and asks of each one what it '
                       'can still prove.'),
                      ('B',
                       'Somewhere in the department there is unspent money with a year-end deadline on it. {N} '
                       'starts working out who holds it.'),
                      ('R',
                       '{N} wants to tear up the spreadsheet, keep everything anyway, and find the money somehow, '
                       'later.'),
                      ('G',
                       'Projects have seasons, {N} thinks, and this one is past its spring. What matters now is what '
                       'can still ripen.')]},
 'outcomes': (['The plan is cut to fit, and what is left of the project is still worth doing.',
               'The money turns up from an unexpected line, and the field season goes ahead after all.'],
              ['The cuts fall in the wrong place, and the main question can no longer be answered with what remains.',
               'The funder takes two months to reply, and by then the field season has passed.']),
 'options': [
    ('keep every promise made to the team first, and cut the work instead', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'mark': 'kept your word', 'chance': 0.75}),
    ('weigh each remaining task by what it adds to the answer, and cut from the bottom', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'project triage', 'chance': 0.75}),
    ("find the department's unspent money before its year-end deadline, and claim it", 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.45}),
    ('keep the whole team and the field season, and trust the money to turn up', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'mark': 'took a wild risk', 'chance': 0.2}),
    ('let the last field season go, and spend what is left on the samples already frozen', 'G1', None, 0.45, '', {'v': 'security, tradition', 'chance': 0.9}),
    ('ask the funder, by the book, to move travel money into the analysis', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'chance': 0.75}),
    ('rewrite the plan so the most publishable part is finished first', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.75}),
    ('bargain the department into making the project a standing group, with your postdoc kept on', 'B1', 'R.7', 0.5, '', {'title': 'research group leader', 'requires': 'a loyal research team', 'without': 'impossible', 'v': 'power, achievement', 'chance': 0.06}),
    ('charge the field season to another grant, to keep the long record unbroken', 'R1', 'G.7', 0.5, '', {'v': 'universalism, security', 'mark': 'hid a wrong', 'closed': 'approval: costs charged to a grant they do not belong to; backfire: an audit finds them and the money is clawed back', 'chance': 0.8}),
    ('keep everyone on at reduced hours, the way a family shares a lean year', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'binds': True, 'chance': 0.6}),
 ]},
{'name': 'a team member knows more than you now',
 'stages': 'young_adult adult mature',
 'age': (27, 75),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss',
 'requires': 'research project lead',
 'worlds': {'earth': 'the postdoc you hired two years ago now knows the method better than you, and the whole team '
                     'has noticed'},
 'timing': {'times': 'per research project lead: a junior who comes to know the method better than the lead happens '
                     'perhaps once every few years, most often in the second or third year of a project with a '
                     'postdoc on it (estimate)'},
 'scenes': {'earth': [('',
                       'In the lab meeting, everyone turns to {colleague} with the hard question about the method, '
                       'not to {N}. {N} hired {colleague} two years ago.'),
                      ('W',
                       '{N} is still the one who signs for the project and the one the funder will call. The '
                       'responsibility has not moved, even if the knowledge has.'),
                      ('U',
                       "{N} reads {colleague}'s latest analysis twice and finds nothing to improve. It is a strange, "
                       'clean feeling.'),
                      ('B',
                       '{colleague} will be applying for posts soon, and every post {colleague} wins could carry a '
                       'line of the work away.'),
                      ('R', '{N} feels two things at once and cannot pull them apart: pride, and a small hot sting.'),
                      ('G',
                       'This is how it should go, {N} thinks: the young tree outgrows the stake that held it up.')]},
 'outcomes': (['The team finds its new shape, and the work moves faster than it has in a year.',
               '{colleague} stays on, and the next paper is better than anything {N} could have written alone.'],
              ['{colleague} accepts an offer elsewhere, and the method walks out of the door too.',
               'The meeting goes stiff and polite, and nobody says what everyone has noticed.']),
 'options': [
    ("ask the institute to make your colleague's new role official, with the pay", 'W1', None, 0.45, '', {'v': 'universalism, benevolence', 'chance': 0.35}),
    ('ask for lessons in the new method, and become the student again', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'door': True, 'mark': 'learned a skill', 'chance': 0.9}),
    ('make sure your name stays last on every paper the method produces', 'B1', None, 0.45, '', {'v': 'power, achievement', 'identity': True, 'chance': 0.9}),
    ('tell the team out loud that the student has become the teacher', 'R1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.9}),
    ('keep to your own bench and your own part, as always', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.75}),
    ("hand the method's decisions to your colleague, and keep a weekly check-in", 'W1', 'U.7', 0.5, '', {'v': 'achievement, benevolence', 'habit': True, 'grants': 'supervising researchers', 'chance': 0.85}),
    ('learn everything your colleague knows before they move on and take it with them', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.5}),
    ('win your colleague a raise so they stay, and get back to your own questions', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, benevolence', 'chance': 0.65}),
    ('go out to the field with your colleague and work side by side again', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'door': True, 'body': 'light', 'chance': 0.9}),
    ('make your colleague co-lead, and let the team settle who does what', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'binds': True, 'grants': 'research collaborators', 'chance': 0.6}),
 ]},
{'name': 'eight people and one grant',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague, boss',
 'requires': 'research group leader',
 'worlds': {'earth': 'the grant renewal comes through smaller than you asked: eight people in your group, and money '
                     'for five'},
 'timing': {'times': 'per research group leader: a grant or a renewal smaller than asked, with more people than '
                     'money, comes every few years, since funders often trim the budgets they approve; about 1 life '
                     'in 500 ever leads a research group (estimate)',
            'gap_years': (8.0, 15.0)},
 'scenes': {'earth': [('',
                       'The renewal letter is good news and bad news: the grant goes on, at two thirds of what {N} '
                       'asked for. There are eight people in the group.'),
                      ('W',
                       "{N} has a list of every contract's end date and every promise made at interview. Fairness "
                       'has to start from that list.'),
                      ('U',
                       '{N} maps who does what and which line of the work each person carries, looking for the '
                       'arrangement that keeps the science whole.'),
                      ('B',
                       '{N} knows which two people bring in their own money and which ones only cost it. That is not '
                       'the whole question, but it is part of it.'),
                      ('R', '{colleague} has a baby due in March. {N} cannot look at the list without seeing faces.'),
                      ('G',
                       'The group grew like a hedge, a little every year. Now it has to be cut back, and {N} wants '
                       'it to grow back thick.')]},
 'outcomes': (['The group comes through the lean year smaller but whole, and the work goes on.',
               'Two of the people who had to leave land good posts nearby, and still come to the Friday seminar.'],
              ['The decision leaks before {N} has told anyone, and the lab goes quiet for a month.',
               'The best postdoc takes an offer abroad rather than wait, and a line of the work ends with the '
               'move.']),
 'options': [
    ('honour every contract to its end date, and decide renewals by the written criteria', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'mark': 'kept your word', 'chance': 0.8}),
    ('redraw the work plan so five posts carry the science, and choose by that', 'U1', None, 0.45, '', {'v': 'achievement', 'chance': 0.75}),
    ('keep the two who bring in their own money, and let the others go', 'B1', None, 0.45, '', {'v': 'power, achievement', 'identity': True, 'chance': 0.85}),
    ('cut your own salary to keep everyone on for another six months', 'R1', None, 0.45, '', {'v': 'benevolence', 'binds': True, 'mark': 'helped someone in need', 'chance': 0.6}),
    ('give the one open post to your longest-serving student, without advertising it', 'G1', None, 0.45, '', {'v': 'benevolence, security', 'mark': 'hid a wrong', 'closed': 'approval: a post filled without the open call the rules require; backfire: a complaint, and the appointment is reversed', 'chance': 0.6}),
    ('put the dean on the next paper, as expected here, and ask for bridging money', 'W1', 'B.7', 0.5, '', {'v': 'power, conformity', 'mark': 'hid a wrong', 'closed': "approval: an author who did none of the work; backfire: the journal's contribution check flags the name", 'self_control': '-', 'chance': 0.6}),
    ('spend your nights on a small bridging proposal to keep one more person on', 'U1', 'R.7', 0.5, '', {'v': 'benevolence', 'self_control': '+', 'grants': 'grant writing', 'chance': 0.35}),
    ("call in favours to place each person who leaves in a friend's lab", 'B1', 'G.7', 0.5, '', {'v': 'benevolence', 'chance': 0.7}),
    ('tell the whole group the numbers at once, straight, before rumours start', 'R1', 'W.7', 0.5, '', {'v': 'universalism, benevolence', 'chance': 0.9}),
    ('slow the work down so the long study survives the lean years', 'G1', 'U.7', 0.5, '', {'v': 'security, universalism', 'self_control': '+', 'chance': 0.7}),
 ]},
{'name': 'the work you would rather be doing',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'years',
 'roles': 'colleague, boss',
 'requires': 'research group leader',
 'worlds': {'earth': 'your days are budgets, reviews and meetings, and you have not run an experiment of your own in '
                     'two years'},
 'timing': {'times': 'per research group leader: the pull back toward hands-on work is felt most years, and comes to '
                     'a real choice perhaps once in five years; most leaders run few experiments of their own once '
                     'the group grows (estimate)',
            'gap_years': (8.0, 15.0)},
 'scenes': {'earth': [('',
                       '{N} counts it up on a Sunday: two years as head of the group, and not one experiment of {Ns} '
                       "own. The weeks are meetings, budgets, reviews and other people's problems."),
                      ('W',
                       'Someone has to carry the group, sign the forms and sit on the committees. {N} took the job '
                       'knowing that, and it still feels like a duty worth doing.'),
                      ('U',
                       '{N} misses the moment when new data come in and nobody in the world knows the answer yet. '
                       'Managing is a craft too, but not that one.'),
                      ('B',
                       'The title brings money, a voice in the faculty and people who answer to {N}. Giving it up '
                       'would mean giving all of that up.'),
                      ('R',
                       'In a dull budget meeting {N} catches sight of the old bench through the glass door and '
                       'wants, badly, to be there.'),
                      ('G',
                       '{N} was happiest at the bench, with the slow work under {Ns} hands. That was who {N} was, '
                       'and maybe still is.')]},
 'outcomes': (['The weeks find a better balance, and some evenings {N} goes home smelling of the lab again.',
               'The group takes the change well, and {colleague} steps up in a way nobody expected.'],
              ['The plan lasts a month before the meetings swallow it again.',
               'The dean takes it badly, and the next budget round is harder for the whole group.']),
 'options': [
    ('keep the group and do the job well, because people depend on it', 'W1', None, 0.45, '', {'v': 'benevolence, conformity', 'self_control': '+', 'chance': 0.9}),
    ('take the chair the faculty offers, and guard one morning a week for your own experiment', 'U1', None, 0.45, '', {'title': 'professor', 'requires': 'published research', 'without': 'approval', 'v': 'achievement, security', 'identity': True, 'habit': True, 'self_control': '+', 'chance': 0.12}),
    ("steer the group's next grant toward the experiment you want to run yourself", 'B1', None, 0.45, '', {'v': 'self-direction, power', 'chance': 0.75}),
    ('hand back the group and walk back to the bench', 'R1', None, 0.45, '', {'v': 'self-direction, hedonism', 'identity': True, 'drops': 'research group leader', 'title': 'research scientist', 'chance': 0.6}),
    ('accept that this season of the work is about others, and let your own rest', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'chance': 0.75}),
    ('apply for a sabbatical year of research, and come back with results to show', 'W1', 'B.7', 0.5, '', {'v': 'achievement, self-direction', 'door': True, 'chance': 0.55}),
    ('learn the new technique your students use, just for the thrill of it', 'U1', 'R.7', 0.5, '', {'v': 'stimulation', 'door': True, 'mark': 'learned a skill', 'chance': 0.85}),
    ('bargain to step down slowly, keeping a small team at the bench', 'B1', 'G.7', 0.5, '', {'v': 'security, self-direction', 'drops': 'research group leader', 'title': 'research project lead', 'chance': 0.5}),
    ('tell the group honestly that you miss the bench, and ask who wants more say', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'chance': 0.7}),
    ('take up a slow side study by hand, the old way, in your own time', 'G1', 'U.7', 0.5, '', {'v': 'self-direction, tradition', 'habit': True, 'self_control': '+', 'chance': 0.85}),
 ]},
{'name': 'the old instrument fails before the big run',
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'colleague, boss',
 'requires': 'research facility lead',
 'worlds': {'earth': "the facility's twenty-year-old microscope breaks down three days before the busiest week of "
                     'the year'},
 'timing': {'times': 'per research facility lead: a key instrument breaking down just before a busy spell comes a '
                     'few times a year where the kit is old; about 1 life in 2,000 ever runs a research facility '
                     '(estimate)'},
 'scenes': {'earth': [('',
                       "Three days before the busiest week of the year, the facility's old electron microscope "
                       'throws an error {N} has never seen. Three groups have booked the week.'),
                      ('W',
                       'There is a service contract, a fault log and a list of booked users who must be told. {N} '
                       'starts with the list.'),
                      ('U',
                       "{N} reads the error code, the logs and last night's temperature record. Somewhere in there "
                       'is a pattern.'),
                      ('B',
                       'A new machine has been on {Ns} wish list for five years. A dead old one makes the case '
                       'better than any memo could.'),
                      ('R', '{N} has the side panel off before {colleague} has finished saying the word "error".'),
                      ('G',
                       '{N} has kept this machine running for twelve years and knows its sounds the way a sailor '
                       'knows a hull. It sounds tired.')]},
 'outcomes': (['The machine hums back to life before the weekend, and the booked groups get their week.',
               "The fix holds, and the fault becomes a page in the facility's handbook that will save the next "
               'breakdown.'],
              ['The part is out of production, and the machine stays dark for six weeks.',
               "The fix seems to work, then fails again halfway through the first group's run."]),
 'options': [
    ('log the fault, warn every booked group, and call the service engineer', 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.6}),
    ('trace the fault through the logs until you know which part failed', 'U1', None, 0.45, '', {'v': 'achievement', 'grants': 'instrument troubleshooting', 'chance': 0.65}),
    ('promise the maker a look at a new machine if their engineer comes tomorrow', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.6}),
    ('open it up tonight and try the fix you suspect', 'R1', None, 0.45, '', {'v': 'stimulation', 'body': 'light', 'chance': 0.7}),
    ('ring the retired engineer who kept this model going for decades', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.8}),
    ('draw up a fair new schedule, and let the groups swap slots as they like', 'W1', 'R.7', 0.5, '', {'v': 'universalism, self-direction', 'chance': 0.75}),
    ('write down every fix you find, so the next keeper can keep it alive', 'U1', 'G.7', 0.5, '', {'v': 'tradition, universalism', 'chance': 0.9}),
    ("borrow time on a rival institute's machine, for a favour you will owe", 'B1', 'W.7', 0.5, '', {'v': 'security, benevolence', 'binds': True, 'chance': 0.7}),
    ('turn the breakdown into a hands-on class, and fix it with the students', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, universalism', 'door': True, 'chance': 0.65}),
    ('salvage the part from the scrapped machine in the basement, and skip the contract', 'G1', 'B.7', 0.5, '', {'v': 'security, self-direction', 'chance': 0.65}),
 ]},
{'name': 'every group wants the machine first',
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, rival, boss',
 'requires': 'research facility lead',
 'worlds': {'earth': "the new booking season opens, and every group wants the same few weeks on the facility's best "
                     'machine'},
 'timing': {'times': 'per research facility lead: a contest over the best weeks on the main machine comes with every '
                     'booking round, two to four times a year, since big shared instruments are often asked for '
                     'several times over (estimate)'},
 'scenes': {'earth': [('',
                       'The booking calendar for the next six months opens on Monday. By Tuesday, eleven groups have '
                       'asked for the same four weeks.'),
                      ('W',
                       'The facility has a booking policy, written by {N} five years ago, and on paper it is fair. '
                       'It was never tested by eleven requests for four weeks.'),
                      ('U',
                       '{N} pulls the use records: who booked time and never came, whose runs actually produced '
                       'data, whose samples were never ready.'),
                      ('B',
                       '{rival} sits on the committee that funds the facility and wants two of the four weeks. {N} '
                       'knows exactly what saying no would cost.'),
                      ('R',
                       '{N} has always had a soft spot for the student who turns up at seven with samples on ice and '
                       'a hopeful face.'),
                      ('G',
                       'Every year the same rush, {N} thinks, like birds to a feeder at the first frost. It passes, '
                       'and the machine hums through it.')]},
 'outcomes': (['The calendar fills, and for once nobody comes to {Ns} door to complain.',
               'The runs go well, and three groups thank the facility by name in their papers.'],
              ['Two groups go over {Ns} head to the director, and the calendar is redone by someone else.',
               'The weeks go out, and the group that missed out stops using the facility altogether.']),
 'options': [
    ('apply the booking policy exactly as written, whoever is asking', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'identity': True, 'chance': 0.75}),
    ('rank the requests by what each run can show, and publish the scores', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'identity': True, 'chance': 0.6}),
    ('give the committee member one week, and make sure they know what it cost', 'B1', None, 0.45, '', {'v': 'power, security', 'chance': 0.9}),
    ('give the student with samples on ice the first slot, and defend it', 'R1', None, 0.45, '', {'v': 'benevolence', 'chance': 0.75}),
    ('keep the weeks for the groups who have always used them, in the old order', 'G1', None, 0.45, '', {'v': 'tradition', 'identity': True, 'chance': 0.8}),
    ('set aside one open week a month for anyone with a wild idea', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'chance': 0.7}),
    ('keep a share of time for long studies that need the same week each year', 'U1', 'G.7', 0.5, '', {'v': 'tradition, universalism', 'chance': 0.65}),
    ('trade the committee member a week for funding a fairer booking system', 'B1', 'W.7', 0.5, '', {'v': 'security, universalism', 'chance': 0.55}),
    ('run the machine through the nights yourself, so every group gets data', 'R1', 'U.7', 0.5, '', {'v': 'benevolence, achievement', 'habit': True, 'body': 'heavy', 'self_control': '+', 'chance': 0.75}),
    ('let the groups fight it out among themselves, and stay out of it', 'G1', 'B.7', 0.5, '', {'v': 'security', 'chance': 0.45}),
 ]},
{'name': 'nobody pays for this question',
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'years',
 'roles': 'friend',
 'requires': 'independent investigator',
 'worlds': {'earth': "the question you care about most fits no funder's call, and your savings will last about a "
                     'year'},
 'timing': {'times': "per independent investigator: a question that fits no funder's call is felt most years, and "
                     'comes to a hard choice with savings running short perhaps once every few years; about 1 life '
                     'in 2,000 ever works as an independent investigator (estimate)',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       '{N} has read every funding call for a year. None of them asks the question {N} cares about, '
                       'the savings will last until next autumn, and {friend} has started sending job adverts, half '
                       'as a joke.'),
                      ('W',
                       '{N} believes the question matters to more people than {N}: to the river, and to the town '
                       'that drinks from it. Someone ought to fund it, and the right way is to show them why.'),
                      ('U',
                       '{N} keeps a notebook with the whole question broken into pieces. Some of the pieces could be '
                       'answered with open data and a laptop.'),
                      ('B',
                       'Nobody funds what nobody has heard of. {N} has been thinking about who could be made to '
                       'care, and what they would want in return.'),
                      ('R',
                       '{N} wakes at five most mornings already thinking about it. That has to count for something.'),
                      ('G',
                       '{N} has walked the same stretch of river for nine years. The question grew out of it like a '
                       'root, and it is not going anywhere.')]},
 'outcomes': (['The work finds a way to go on, and the first real answer is in the notebook by spring.',
               'Someone unexpected reads the early results and asks how to help.'],
              ['The money runs out in the summer, and the question goes back in the drawer.',
               'The year goes on chores and paperwork, and the question barely moves.']),
 'options': [
    ('set a strict budget and a stop date, and keep to both', 'W1', None, 0.45, '', {'v': 'security, conformity', 'self_control': '+', 'chance': 0.9}),
    ('teach yourself the statistics to answer part of it from open data', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'mark': 'learned a skill', 'chance': 0.75}),
    ('take paid consulting two days a week to fund the other three', 'B1', None, 0.45, '', {'v': 'achievement, security', 'habit': True, 'self_control': '+', 'chance': 0.85}),
    ('spend the savings on it anyway, and trust the next step to show itself', 'R1', None, 0.45, '', {'v': 'stimulation', 'mark': 'took a wild risk', 'self_control': '-', 'chance': 0.8}),
    ('ask the people who have fished the river for generations what they have seen', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.65}),
    ("start a residents' group to fund the river survey together", 'W1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'binds': True, 'chance': 0.4}),
    ("use the water board's records, shared in confidence, for the town's sake", 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'mark': 'broke your word', 'closed': 'approval: records shared in confidence, used without leave; backfire: the board cuts off all access and writes to the journal', 'chance': 0.7}),
    ("sell your survey data to a developer's consultants, and fund the real work with it", 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.75}),
    ('pitch it with all your fire to a wealthy local who loves the river', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'grants': 'patron', 'chance': 0.25}),
    ('do it the way the old naturalists did: slowly, by hand, for love', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, hedonism', 'identity': True, 'self_control': '+', 'chance': 0.85}),
 ]},
{'name': 'a lab offers you a desk, with conditions',
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'independent investigator',
 'worlds': {'earth': 'a university lab offers you a desk, its equipment and its name, if your work joins their '
                     'programme'},
 'timing': {'times': "per independent investigator: an offer of a desk, equipment and an institution's name in "
                     'return for joining its programme comes perhaps once every three to five years, more often to '
                     'those with published work (estimate)',
            'gap_years': (4.0, 8.0)},
 'scenes': {'earth': [('',
                       '{boss}, who runs a large university lab, offers {N} a desk, the equipment and the '
                       "university's name on the papers. In return the work joins the lab's programme, and {boss} "
                       'gets a say in it.'),
                      ('W',
                       'An institution would mean ethics review, a library, a pension and colleagues to check the '
                       'work. {N} has missed all of that more than {N} admits.'),
                      ('U',
                       "{N} draws up two lists: what the lab's machines would make possible, and what joining the "
                       'programme would rule out.'),
                      ('B',
                       "{N} has spent years being nobody's employee. The question is what that freedom is worth in "
                       'equipment, and whether the price can be bargained down.'),
                      ('R',
                       '{N} pictures asking permission to change the question, and something in {Ns} chest goes '
                       'tight.'),
                      ('G',
                       'The lab is in the city, two hours from the river. The work grew where it is, and {N} is not '
                       'sure it would survive being moved.')]},
 'outcomes': (['The choice is made, and {N} sleeps well the first night after it.',
               '{boss} takes the answer well, and the door between them stays open.'],
              ['The terms harden in the contract, and {N} ends up with less say than was promised.',
               '{boss} withdraws the offer, and the desk goes to someone with a bigger name.']),
 'options': [
    ("take the post and bring the work under the lab's rules and review", 'W1', None, 0.45, '', {'v': 'security, conformity', 'door': True, 'binds': True, 'drops': 'independent investigator', 'title': 'research scientist', 'chance': 0.85}),
    ('ask for a visiting post instead: the library and the machines, but your own questions', 'U1', None, 0.45, '', {'v': 'self-direction', 'grants': 'institutional affiliation', 'chance': 0.6}),
    ('bargain it down: the desk and the machines, credit for the lab, but no say', 'B1', None, 0.45, '', {'v': 'power, self-direction', 'identity': True, 'grants': 'institutional affiliation', 'chance': 0.4}),
    ('turn it down on the spot: nobody else chooses your questions', 'R1', None, 0.45, '', {'v': 'self-direction', 'identity': True, 'mark': 'turned down a chance', 'chance': 0.95}),
    ('stay where the work grew, and keep the lab as a friend instead', 'G1', None, 0.45, '', {'v': 'tradition', 'identity': True, 'grants': 'research collaborators', 'chance': 0.6}),
    ('sign only if the data stay with the community where they were collected', 'W1', 'G.7', 0.5, '', {'v': 'universalism, tradition', 'chance': 0.6}),
    ("take the post on a joint plan where the lab's programme and your question truly overlap", 'U1', 'W.7', 0.5, '', {'v': 'achievement, conformity', 'binds': True, 'drops': 'independent investigator', 'title': 'research scientist', 'chance': 0.7}),
    ('take the desk, but get it in writing that you keep your own data', 'B1', 'U.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.75}),
    ('say yes for one year only, keeping the right to walk out with the work', 'R1', 'B.7', 0.5, '', {'v': 'power, stimulation', 'grants': 'institutional affiliation', 'chance': 0.6}),
    ("ask for a season's trial, and see whether the work still feels alive there", 'G1', 'R.7', 0.5, '', {'v': 'self-direction, hedonism', 'door': True, 'chance': 0.65}),
 ]},
{'name': 'the first week with your own bench',
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, mentor',
 'requires': 'research scientist',
 'threshold': 'title:research scientist',
 'step': 1,
 'worlds': {'earth': 'the first week in the new post: a bench, a desk and a login of your own, and nobody yet saying '
                     'what to do first'},
 'timing': {'times': 'once, in the first weeks after becoming a research scientist: nearly everyone who takes such a '
                     'post meets it; about 1 life in 80 ever holds a research scientist post (estimate)'},
 'trigger': {'requires': 'in the threshold season of research scientist, within the first six months after taking '
                         "the title (opened by 'the contract runs out', a finished doctorate or any other way in): "
                         'step 1, the first weeks in the post',
             'likelier': 'a new institute or a new city; a post won after a long search; the first post after a '
                         'doctorate',
             'rarer': 'a step up inside the same lab, at the same bench; a crisis at home that crowds out the new '
                      'start'},
 'scenes': {'earth': [('',
                       'On Monday {N} is shown a bench, half a shelf in the cold room and a desk by the window. By '
                       'Wednesday nobody has said what to do first.'),
                      ('W',
                       '{N} reads the safety induction, the lab rules and the booking system from end to end, and '
                       'signs every form before touching anything.'),
                      ('U',
                       'The empty bench is a blank page. {N} lists every question worth asking here and sorts them '
                       'by how long each would take to answer.'),
                      ('B',
                       'Whoever claims the good shelf, the freezer drawer and a slot on the shared machine in the '
                       'first week keeps them for years. {N} has noticed.'),
                      ('R',
                       '{N} unpacks a box of old notebooks onto the bench and wants to start something, anything, '
                       'this afternoon.'),
                      ('G',
                       "The bench still carries the last owner's labels, and the plant on the windowsill has not "
                       'been watered in weeks. {N} waters it, and feels for the rhythm of the place before changing '
                       'anything.')]},
 'outcomes': (['By Friday the bench has a plan on it, and {N} knows whom to ask for what.',
               '{boss} stops by at the end of the week, looks around and says it is a good start.'],
              ['The week goes on forms, broken logins and waiting, and nothing gets started.',
               'Something done in a hurry rubs someone the wrong way, and the corridor remembers.']),
 'options': [
    ('do every induction, rule and booking form before starting any work', 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.92}),
    ("spend the week reading the lab's old notebooks and the papers behind them", 'U1', None, 0.45, '', {'door': True, 'v': 'self-direction, achievement', 'mark': 'learned a skill', 'chance': 0.85}),
    ('claim the freezer drawer, the good shelf and a weekly slot on the shared machine', 'B1', None, 0.45, '', {'v': 'power, security', 'chance': 0.85}),
    ('start a quick pilot experiment on Wednesday, before anyone sets a plan', 'R1', None, 0.45, '', {'v': 'stimulation', 'chance': 0.79}),
    ('ask the oldest technician, over tea, how the lab really runs', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'made a friend', 'chance': 0.8}),
    ('sign the fixed-term postdoc contract, and agree a three-year plan with the boss', 'W1', 'U.7', 0.5, '', {'title': 'postdoctoral researcher', 'requires': 'doctoral graduate', 'without': 'impossible', 'v': 'achievement, conformity', 'chance': 0.84}),
    ('map who controls the money, the machines and the hiring before choosing a project', 'U1', 'B.7', 0.5, '', {'v': 'power, security', 'chance': 0.82}),
    ('book the big machine for the quiet Friday nights nobody else wants', 'B1', 'R.7', 0.5, '', {'habit': True, 'v': 'stimulation, self-direction', 'chance': 0.85}),
    ('put up photographs, bring in a kettle and make the bench feel like home', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, security', 'chance': 0.88}),
    ("keep the last owner's labels and routines until you understand why they are there", 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'chance': 0.9}),
 ]},
{'name': "a question of your own, or the boss's",
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'boss, mentor, colleague',
 'requires': 'research scientist',
 'threshold': 'title:research scientist',
 'step': 2,
 'worlds': {'earth': "your post is paid from the boss's grant, which asks one question, and you have started to care "
                     'about another'},
 'timing': {'times': 'once, in the first months after becoming a research scientist: most first posts are paid from '
                     "a supervisor's grant, and perhaps half of new scientists come to care about another question "
                     'that soon; across all lives about 1 in 160 (estimate)'},
 'trigger': {'requires': 'in the threshold season of research scientist, within the first six months after taking '
                         "the title: step 2, some weeks into the post, while the salary comes from someone else's "
                         'grant',
             'likelier': "a post on a supervisor's grant, as most first posts are; an idea carried over from the "
                         'doctorate; a supervisor who leaves little room',
             'rarer': "a fellowship or a permanent post of one's own; a supervisor who already shares the person's "
                      'question'},
 'scenes': {'earth': [('',
                       'The grant that pays {Ns} salary asks one question. Over the past weeks {N} has fallen for a '
                       'different one, and {boss} wants a work plan by the end of the month.'),
                      ('W',
                       'The money was given for a stated piece of work, and the funders were promised it. {N} feels '
                       'the weight of that promise, even with another idea burning.'),
                      ('U',
                       '{Ns} own question is cleaner and might explain more, but it would take a year to know. {N} '
                       'sketches both designs side by side on one page.'),
                      ('B',
                       "Papers on the boss's question will carry the boss's name. A question of {Ns} own is what a "
                       'career is built on.'),
                      ('R',
                       'The new idea keeps {N} awake at night. The funded question has started to feel like '
                       'homework.'),
                      ('G',
                       "The lab has worked on the boss's question for twelve years, with samples and records going "
                       'back to the start. {Ns} idea would grow better from those roots than from nothing.')]},
 'outcomes': (['{N} and {boss} agree on a split that keeps the funded work going and lets the new question start.',
               'By the end of the month {N} has a plan that feels like {Ns} own.'],
              ['{boss} says no, and the new idea goes back in a drawer.',
               'The month goes on arguing and second-guessing, and neither question moves.']),
 'options': [
    ('do the funded work as promised, and keep your idea for the next grant round', 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'kept your word', 'self_control': '+', 'chance': 0.88}),
    ('design one experiment that could answer both questions at once', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.45}),
    ('tell the boss you will stay only if one day a week is your own', 'B1', None, 0.45, '', {'v': 'power, self-direction', 'chance': 0.48}),
    ('work on your own idea every evening and weekend, for the love of it', 'R1', None, 0.45, '', {'habit': True, 'v': 'stimulation, self-direction', 'self_control': '+', 'chance': 0.82}),
    ("look back through the lab's twelve years of records for where your question already shows", 'G1', None, 0.45, '', {'v': 'tradition, achievement', 'chance': 0.48}),
    ("put your idea into the grant's next report, with your name on it", 'W1', 'B.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.6}),
    ('trim the outliers from your evening pilot until your idea looks too good to drop', 'U1', 'R.7', 0.5, '', {'v': 'self-direction', 'mark': 'hid a wrong', 'closed': 'approval: selective analysis of research data; backfire: the boss asks for a clean rerun and the effect is gone', 'self_control': '-', 'chance': 0.9}),
    ("do the boss's work, and save every leftover sample toward your own question later", 'B1', 'G.7', 0.5, '', {'v': 'security, achievement', 'self_control': '+', 'chance': 0.9}),
    ('say plainly at the lab meeting that the funded question is the wrong one', 'R1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'mark': 'defied an authority', 'chance': 0.45}),
    ('ask your old mentor which of the two questions will still matter in twenty years', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'chance': 0.84}),
 ]},
{'name': 'the experiment that will define you',
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'boss, mentor, rival, colleague',
 'requires': 'research scientist',
 'threshold': 'title:research scientist',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'there is money and time for one big experiment this year, and how you choose it will set what '
                     'kind of scientist you become'},
 'timing': {'times': 'once, in the first months after becoming a research scientist, for the perhaps 1 in 3 given '
                     'money and time to choose one big piece of work; across all lives about 1 in 250 (estimate)'},
 'trigger': {'requires': 'in the threshold season of research scientist, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, once there is some money and time to "
                         'choose the big piece of work',
             'likelier': 'a fellowship, a start-up fund or a boss who gives real freedom; two good ideas competing; '
                         'a rival on the same problem',
             'rarer': 'a post with no say over the work; money too tight for anything but the funded plan'},
 'scenes': {'earth': [('',
                       'There is money and time for one big piece of work this year. Whatever {N} chooses will fill '
                       'the next three years and become what people mean when they say {Ns} name.'),
                      ('W',
                       '{N} thinks of the doctors, farmers and planners who may one day rely on this result. It has '
                       'to be something they can trust.'),
                      ('U',
                       'Two explanations fit everything known so far. {N} has spent a week designing the one '
                       'experiment that could tell them apart.'),
                      ('B',
                       '{rival} is working on the same problem two floors up. Whoever owns the method first will own '
                       'the field for a decade.'),
                      ('R',
                       'There is a wild idea {N} cannot shake, the kind supervisors talk students out of. Now there '
                       'is no supervisor to do the talking.'),
                      ('G',
                       '{N} keeps coming back to one {place}, one population, one slow process. The experiment that '
                       'matters there would take years of patience.')]},
 'outcomes': (['The first results come in on schedule, and they are solid enough to build three years on.',
               'Within the year people in the field start to say what {N} stands for, and they say it right.'],
              ['The experiment eats the year and gives back nothing that can be used.',
               'Halfway through, {N} sees the plan was wrong for the question, and has to start again.']),
 'options': [
    ('design a large preregistered study that others can repeat and rely on', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, conformity', 'grants': 'research integrity', 'chance': 0.65}),
    ('build the cleanest test between the two explanations, whatever it shows', 'U1', None, 0.45, '', {'identity': True, 'v': 'self-direction, universalism', 'grants': 'experimental design', 'chance': 0.68}),
    ('develop a method nobody else has, and keep the details close until it is out', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'self_control': '+', 'chance': 0.62}),
    ('bet the year on the odd idea that excites you, against all advice', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation', 'mark': 'took a wild risk', 'chance': 0.5}),
    ('commit to ten years of watching one place through every season', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'tradition, universalism', 'grants': 'fieldwork', 'chance': 0.7}),
    ('take on the urgent problem that moves you most, and do it strictly by the book', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism, stimulation', 'chance': 0.48}),
    ('pair models with years of close watching of one living system', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, self-direction', 'chance': 0.68}),
    ('sign on as the junior partner in a big consortium, and make yourself its indispensable expert', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, achievement', 'chance': 0.7}),
    ('teach yourself a whole new method in a month, because the question demands it', 'R1', 'U.7', 0.5, '', {'identity': True, 'door': True, 'v': 'stimulation, achievement', 'mark': 'learned a skill', 'self_control': '+', 'chance': 0.72}),
    ("build your speciality around the lab's irreplaceable old collection, and guard it", 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'power', 'chance': 0.65}),
 ]},
{'name': 'half a year in, the work has a shape',
 'stages': 'young_adult adult mature',
 'age': (24, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss, friend',
 'requires': 'research scientist',
 'threshold': 'title:research scientist',
 'step': 3,
 'worlds': {'earth': 'half a year into the post, the weeks have found a pattern: what you do, when, and with whom'},
 'timing': {'times': 'once, about six months after becoming a research scientist, for most who are still in the '
                     'post; about 1 life in 80 ever holds a research scientist post (estimate)'},
 'trigger': {'requires': 'in the threshold season of research scientist, within the first six months after taking '
                         'the title: step 3, near the end of the six months, as the new life settles',
             'likelier': 'a steady post and a first small result; colleagues the person gets on with',
             'rarer': 'a crisis in the lab or at home; a post already ending'},
 'scenes': {'earth': [('',
                       'Six months in, {N} notices that the weeks have a shape: Mondays at the bench, Thursdays on '
                       'the analysis, a lab meeting that no longer sets {Ns} heart racing.'),
                      ('W',
                       '{Ns} lab notebook is up to date to the day, and {colleague} has started borrowing it as a '
                       'model.'),
                      ('U',
                       'A first small result is in. It is not exciting, but {N} understands exactly why it came out '
                       'the way it did.'),
                      ('B',
                       '{N} has worked out who in the building gets things done and who only talks. The list is '
                       'short and useful.'),
                      ('R',
                       'Some days the work still feels like play. Other days {N} misses the fizz of the first week.'),
                      ('G',
                       'The plant on the windowsill has made it through the summer. {N} has stopped feeling like the '
                       'new one.')]},
 'outcomes': (['The weeks keep their shape, and the work starts to move without being pushed.',
               'At the lab meeting {boss} mentions how far {N} has come since the first week.'],
              ['A deadline from nowhere knocks the new routine flat within a fortnight.',
               'The pattern turns out to be a rut, and {N} is restless by the end of the month.']),
 'options': [
    ('set a fixed weekly routine and keep to it, even in the busy weeks', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, security', 'self_control': '+', 'chance': 0.82}),
    ('write up the small result properly, though nobody has asked for it yet', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.92}),
    ('drop the duties that do nothing for your work, politely and for good', 'B1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.8}),
    ('take the long weekend you promised yourself, and go somewhere wild', 'R1', None, 0.45, '', {'door': True, 'v': 'hedonism, stimulation', 'chance': 0.92}),
    ('let the work settle into its own pace instead of pushing it', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.75}),
    ('start a monthly lunch for the corridor, so new people are not left alone', 'W1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'made a friend', 'chance': 0.8}),
    ('turn your notes into a protocol the whole lab can follow', 'U1', 'W.7', 0.5, '', {'v': 'universalism, achievement', 'grants': 'reproducible workflow', 'chance': 0.66}),
    ('trade your spare machine hours for lessons from the statistics expert', 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, self-direction', 'grants': 'statistical judgment', 'chance': 0.75}),
    ('volunteer for the conference talk nobody else wants to give', 'R1', 'B.7', 0.5, '', {'v': 'achievement, stimulation', 'chance': 0.85}),
    ('spend Friday afternoons in the greenhouse or the field, just watching, for joy', 'G1', 'R.7', 0.5, '', {'habit': True, 'v': 'hedonism, self-direction', 'chance': 0.88}),
 ]},
{'name': 'keys to an empty lab',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, elder',
 'requires': 'research group leader',
 'threshold': 'title:research group leader',
 'step': 1,
 'worlds': {'earth': 'you are handed the keys to an empty lab, a start-up budget and a catalogue of equipment to '
                     'order'},
 'timing': {'times': 'once, in the first weeks after becoming a research group leader, for the perhaps 1 in 2 who '
                     'fit out new rooms; about 1 life in 500 ever leads a research group, so about 1 in 1,000 meet '
                     'it (estimate)'},
 'trigger': {'requires': 'in the threshold season of research group leader, within the first six months after taking '
                         "the title (opened by 'they want you to lead a group' or any other appointment): step 1, "
                         'the first weeks, with new rooms to fit out',
             'likelier': 'a new building or a move to a new institute; a start-up budget that comes with the post',
             'rarer': 'a group that keeps its old rooms and kit; a post with no money of its own'},
 'scenes': {'earth': [('',
                       'The lab is bare: benches, sockets, a sink and an echo. {N} holds the keys, a start-up budget '
                       'and a catalogue of equipment, and nobody else is here yet.'),
                      ('W',
                       "Before the first order goes in, {N} reads the institute's rules on purchasing, safety and "
                       'hiring, and opens a file for each.'),
                      ('U',
                       '{N} paces the room with a tape measure, working out where every instrument should stand so '
                       'the work flows from door to window.'),
                      ('B',
                       'The start-up money is the most {N} will ever spend without asking anyone. Every choice now '
                       'is leverage later.'),
                      ('R',
                       '{N} stands in the middle of the empty room and laughs out loud. It is all {Ns} to fill.'),
                      ('G',
                       'The room still smells faintly of the group that worked here for thirty years. A faded '
                       'photograph of them is pinned inside a cupboard door.')]},
 'outcomes': (['By the end of the week the orders are in and the room has a plan pinned to the wall.',
               'The first boxes arrive, and the empty lab starts to look like a place where work will happen.'],
              ['An order goes wrong, and half the budget is tied up in a machine that will not fit through the door.',
               'The department freezes purchases for the quarter, and the room stays empty.']),
 'options': [
    ('open a safety file and a purchase log before buying a single pipette', 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.92}),
    ('plan the layout around how the work will flow, then order to the plan', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.92}),
    ('spend most of the start-up money early, before the department can claw it back', 'B1', None, 0.45, '', {'v': 'power, security', 'chance': 0.9}),
    ('order the one big instrument you have dreamed of, and worry about the rest later', 'R1', None, 0.45, '', {'v': 'stimulation', 'chance': 0.8}),
    ('ask a retired member of the old group what the room was good for', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'made a friend', 'chance': 0.75}),
    ('ask three established group leaders what they wish they had bought first', 'W1', 'U.7', 0.5, '', {'door': True, 'v': 'conformity, achievement', 'chance': 0.82}),
    ('compare every quote and play the suppliers off against each other for discounts', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.82}),
    ("borrow a colleague's spare kit for a year, and spend the savings on something bold", 'B1', 'R.7', 0.5, '', {'v': 'stimulation, power', 'chance': 0.72}),
    ('paint the walls and bring in plants, so the people who come will want to stay', 'R1', 'G.7', 0.5, '', {'body': 'light', 'v': 'benevolence, hedonism', 'chance': 0.85}),
    ('buy only what the first year needs, and keep the rest for the group to come', 'G1', 'W.7', 0.5, '', {'v': 'security, benevolence', 'self_control': '+', 'chance': 0.8}),
 ]},
{'name': 'hiring the first two people',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, rival, mentor, friend',
 'requires': 'research group leader',
 'threshold': 'title:research group leader',
 'step': 2,
 'worlds': {'earth': 'two posts are open, the first you have ever filled, and the people you pick will shape the '
                     'group for years'},
 'timing': {'times': 'once, in the first months after becoming a research group leader; most new leaders fill their '
                     'first posts within the first year; about 1 life in 500 ever leads a research group (estimate)'},
 'trigger': {'requires': 'in the threshold season of research group leader, within the first six months after taking '
                         'the title: step 2, some weeks in, with posts to fill',
             'likelier': 'a start-up budget with posts in it; people who left with the old leader; a field with many '
                         'applicants',
             'rarer': 'a group already full; a hiring freeze at the institute'},
 'scenes': {'earth': [('',
                       'Two posts, forty applications. The first people {N} chooses will set the tone of the group '
                       'for years, and {N} has never hired anyone.'),
                      ('W',
                       '{N} writes the criteria before reading a single application, so every candidate is judged '
                       'the same way.'),
                      ('U',
                       'One candidate has a flawless record. Another has a strange, brilliant thesis and a two-year '
                       'gap. {N} reads both twice.'),
                      ('B',
                       "A former student of {rival} has applied. Hiring them would bring {rival}'s methods and "
                       'contacts along.'),
                      ('R',
                       'In the interview one candidate lights up talking about a failed experiment, and {N} feels '
                       'the room change.'),
                      ('G',
                       '{N} thinks less about the best candidate on paper than about who will still be here, and '
                       'still be kind, in five years.')]},
 'outcomes': (['The two people who start in the new year turn out to be the ones the group needed.',
               'Word gets round that {N} hires fairly, and the next round of applicants is stronger.'],
              ['One of the new hires leaves within three months, and the post has to be filled again.',
               'The choice causes a quarrel in the department, and {N} starts the group under a cloud.']),
 'options': [
    ('score every candidate against the written criteria, and hire the top two', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'chance': 0.72}),
    ('set every finalist a real problem from the lab, and judge how they think', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.75}),
    ("hire the rival's former student, with the methods and contacts they bring", 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.68}),
    ('hire the one who lit up in the interview, on instinct', 'R1', None, 0.45, '', {'v': 'stimulation', 'chance': 0.58}),
    ('hire someone from the lab you trained in, whose people you know', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.75}),
    ("use the institute's fast-track rules to sign the best candidate before other labs bid", 'W1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.65}),
    ('take a chance on the odd thesis with the gap, after checking it properly', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, universalism', 'chance': 0.48}),
    ("quietly give one post to a friend's partner who needs work in town", 'B1', 'G.7', 0.5, '', {'v': 'security, benevolence', 'mark': 'hid a wrong', 'closed': 'approval: a post filled around the fair process; backfire: a passed-over candidate complains and the hire is reviewed', 'self_control': '-', 'chance': 0.88}),
    ('ring every candidate you turn down, and tell each one honestly why', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'self_control': '+', 'chance': 0.8}),
    ("ask the finalists' old supervisors, quietly, how each one copes in a bad month", 'G1', 'U.7', 0.5, '', {'v': 'tradition, security', 'chance': 0.72}),
 ]},
{'name': 'the culture you set now',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'colleague, mentor, boss',
 'requires': 'research group leader',
 'threshold': 'title:research group leader',
 'step': 2,
 'transform': True,
 'worlds': {'earth': 'the group is new under you, and the habits you set in these months will last as long as the '
                     'group does'},
 'timing': {'times': 'once, in the first months after becoming a research group leader; nearly every new leader sets '
                     "the group's habits then, knowingly or not; about 1 life in 500 ever leads a research group "
                     '(estimate)'},
 'trigger': {'requires': 'in the threshold season of research group leader, within the first six months after taking '
                         "the title: step 2, the season's transforming chance, once the first people are in place",
             'likelier': "a new group or a group that lost its old leader; the person's memory of labs that worked "
                         'and labs that did not',
             'rarer': 'a group so large that its ways were set long ago; a leader who is rarely there'},
 'scenes': {'earth': [('',
                       'The group is new to {N}, and {N} is new to it. How meetings run, who gets the credit, what '
                       "happens after a mistake: whatever {N} does in these months will still be the group's way in "
                       'ten years.'),
                      ('W',
                       '{N} drafts a page of group rules: authorship, data, hours, how disagreements are settled. It '
                       'feels stiff, and necessary.'),
                      ('U',
                       '{N} wants a group where every claim is challenged, every method explained and every result '
                       'checked twice, and wonders how to build that without fear.'),
                      ('B',
                       'Funders back groups that deliver. {N} thinks about targets, deadlines and whose name goes '
                       'where.'),
                      ('R',
                       '{N} remembers the labs that crushed people, and the one lab that felt like a band on tour. '
                       'Only one kind is worth building.'),
                      ('G',
                       '{N} thinks of the group as something to grow, like a family or an orchard: slow, rooted, '
                       'looked after.')]},
 'outcomes': (['The habits take, and new people pick them up without being told.',
               'A year on, people outside the group can say what it stands for, and they are right.'],
              ['The rules feel like a cage, or the freedom like chaos, and the first member starts looking '
               'elsewhere.',
               'What {N} meant to build and what the group became drift apart, and nobody says so.']),
 'options': [
    ('write clear rules on credit, data and hours, and apply them to yourself first', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'conformity, universalism', 'grants': 'credit negotiation', 'chance': 0.85}),
    ('make every result face a hard internal review before it leaves the room', 'U1', None, 0.45, '', {'identity': True, 'v': 'achievement, universalism', 'grants': 'research integrity', 'chance': 0.72}),
    ('set high targets, reward whoever delivers, and let the rest find other labs', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, achievement', 'chance': 0.8}),
    ('run the group loose and fiery: open doors, wild ideas, arguments over a beer', 'R1', None, 0.45, '', {'identity': True, 'habit': True, 'v': 'stimulation, hedonism', 'grants': 'a loyal research team', 'chance': 0.69}),
    ('treat the group like a family: birthdays, slow growth, nobody left behind', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'benevolence, tradition', 'grants': 'supervising researchers', 'chance': 0.7}),
    ('commit the group to a hard public problem, and let that duty fire everyone up', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism, stimulation', 'chance': 0.48}),
    ('build slow, careful studies the group can grow with for decades', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'chance': 0.66}),
    ('trade favours with the department heads until the group has a protected place', 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'power, security', 'chance': 0.72}),
    ('promise every member a year of freedom on a question of their own', 'R1', 'U.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'self-direction, stimulation', 'chance': 0.72}),
    ('keep the group small and self-reliant, beholden to no big consortium', 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'self-direction, security', 'chance': 0.7}),
 ]},
{'name': 'the group meeting runs itself',
 'stages': 'young_adult adult mature',
 'age': (30, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague',
 'requires': 'research group leader',
 'threshold': 'title:research group leader',
 'step': 3,
 'worlds': {'earth': 'one Tuesday the group meeting starts, runs and ends well without you steering it'},
 'timing': {'times': 'once, near six months after becoming a research group leader, for the perhaps 1 in 2 whose '
                     'group settles that soon; across all lives about 1 in 1,000 (estimate)'},
 'trigger': {'requires': 'in the threshold season of research group leader, within the first six months after taking '
                         'the title: step 3, near the end of the six months, as the group settles',
             'likelier': 'a group with a few months of shared work behind it; people who get on',
             'rarer': 'a quarrel in the group; a member leaving; a leader away most weeks'},
 'scenes': {'earth': [('',
                       'One Tuesday {N} arrives late to the group meeting and finds it already under way: '
                       '{colleague} in the chair, the agenda followed, a disagreement settled. Nobody needed {N} to '
                       'steer.'),
                      ('W',
                       'The rota, the minutes, the order of speakers: everything {N} set up in the first weeks is '
                       'simply how things are done now.'),
                      ('U',
                       '{N} listens from the back as two juniors argue a point of method better than {N} could have '
                       'a year ago.'),
                      ('B',
                       'A group that runs without its leader is either a triumph or a sign that the leader is no '
                       'longer needed. {N} weighs which.'),
                      ('R', '{N} feels a sudden pang: the group is growing up, and the wild first months are over.'),
                      ('G',
                       'Like a hedge that has finally taken, the group holds its own shape now, and {N} only needs '
                       'to tend it.')]},
 'outcomes': (['The meetings keep running well, and {N} gets a morning a week back for the work.',
               '{colleague} says, half joking, that this is the best-run group in the building.'],
              ['The calm lasts a fortnight, then an old quarrel flares and everyone looks to {N} again.',
               '{N} steps back a little too far, and a decision gets made that {N} would never have made.']),
 'options': [
    ('hand the chair to a different member each month, by rota', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'chance': 0.82}),
    ('use the freed hours to get back to your own analysis', 'U1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.92}),
    ('step in and take the chair back, so nobody forgets who leads', 'B1', None, 0.45, '', {'v': 'power', 'chance': 0.92}),
    ("skip next week's meeting and spend the morning at the bench", 'R1', None, 0.45, '', {'v': 'hedonism, self-direction', 'chance': 0.86}),
    ('sit back and let the group find its own way, saying little', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'chance': 0.72}),
    ('set up a welcome pack and a buddy for every new member', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, security', 'chance': 0.8}),
    ("ask the group to review your own work as hard as each other's", 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'chance': 0.78}),
    ('court a big collaborator for data the group could never get alone', 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, power', 'chance': 0.45}),
    ('throw the group a party for its first result, and invite the dean', 'R1', 'B.7', 0.5, '', {'v': 'hedonism, power', 'chance': 0.75}),
    ('walk the long way home and let yourself be glad, for once', 'G1', 'R.7', 0.5, '', {'v': 'hedonism', 'chance': 0.9}),
 ]},
{'name': 'nobody to report to on Monday',
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'week',
 'roles': 'friend, partner, mentor',
 'requires': 'independent investigator',
 'threshold': 'title:independent investigator',
 'step': 1,
 'worlds': {'earth': 'the fellowship has started, and on Monday morning there is nobody to report to and nobody to '
                     'say what to do'},
 'timing': {'times': 'once, in the first weeks after becoming an independent investigator: nearly everyone who goes '
                     'it alone meets it; about 1 life in 2,000 ever works as an independent investigator (estimate)'},
 'trigger': {'requires': 'in the threshold season of independent investigator, within the first six months after '
                         "taking the title (opened by 'a fellowship of your own', savings, a patron or any other way "
                         'in): step 1, the first weeks working alone',
             'likelier': "years spent on other people's projects before this; money in the account for several years",
             'rarer': 'an investigator who has worked alone before; money that covers only months'},
 'scenes': {'earth': [('',
                       'Monday morning. The fellowship has started, the money is in the account, and for the first '
                       'time in {Ns} working life nobody expects {N} anywhere at nine.'),
                      ('W',
                       "{N} writes out the fellowship's terms on one page and pins it above the desk: what was "
                       'promised, by when, and to whom.'),
                      ('U',
                       'Five years, one question and nobody to interrupt. {N} opens a fresh notebook and writes the '
                       'question at the top of the first page.'),
                      ('B',
                       'The fellowship is money, time and a name. {N} thinks about how to turn five years of freedom '
                       'into a position nobody can take away.'),
                      ('R',
                       '{N} sleeps until ten, makes a huge breakfast, and then works until two in the morning '
                       'because the idea will not wait.'),
                      ('G',
                       '{N} sets the desk by a window that looks out toward the {place} the work is about, and '
                       'watches the light change before starting.')]},
 'outcomes': (['By Friday the week has a shape, and {N} has done more real work than in any month of the old job.',
               '{mentor} rings to ask how it is going, and {N} finds there is a lot to say.'],
              ['The week slips away in errands and email, and the notebook is still blank by Friday.',
               'The freedom feels like falling, and {N} spends Thursday wondering whether this was a mistake.']),
 'options': [
    ('set office hours for yourself and keep them as if a boss were watching', 'W1', None, 0.45, '', {'habit': True, 'v': 'conformity, achievement', 'self_control': '+', 'chance': 0.75}),
    ('spend the first week reading everything published on the question since you last looked', 'U1', None, 0.45, '', {'door': True, 'v': 'self-direction, achievement', 'mark': 'learned a skill', 'chance': 0.92}),
    ('announce the fellowship widely, and line up collaborators who want your time', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.75}),
    ('set aside the plan you wrote for the funders, and start on what excites you most', 'R1', None, 0.45, '', {'v': 'stimulation', 'closed': 'approval: departing from the funded plan; backfire: the first progress report shows it', 'chance': 0.88}),
    ('spend the first days out at the site, looking, before writing a word', 'G1', None, 0.45, '', {'v': 'tradition, self-direction', 'chance': 0.85}),
    ('write a plan with yearly milestones, and send it to your old mentor to check', 'W1', 'U.7', 0.5, '', {'v': 'achievement, conformity', 'chance': 0.82}),
    ('work out which part of the question only you can answer, and stake it first', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'chance': 0.68}),
    ('rent a cheap room away from the institute, so nobody can drop by', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, hedonism', 'chance': 0.88}),
    ('have your partner and friends round to celebrate, and talk about the work all night', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, benevolence', 'chance': 0.92}),
    ('offer to help the local society that has logged the question for decades', 'G1', 'W.7', 0.5, '', {'door': True, 'v': 'tradition, benevolence', 'mark': 'made a friend', 'chance': 0.68}),
 ]},
{'name': 'the silence after the first rejection',
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'months',
 'roles': 'friend, mentor, partner, rival',
 'requires': 'independent investigator',
 'threshold': 'title:independent investigator',
 'step': 2,
 'worlds': {'earth': 'the first paper you sent out alone has been rejected, and with no group around you, nobody '
                     'else says a word'},
 'timing': {'times': 'once, in the first months after becoming an independent investigator, for the many whose first '
                     'paper or proposal sent alone is turned down; funders refuse most proposals; about 1 life in '
                     '2,000 ever works this way (estimate)'},
 'trigger': {'requires': 'in the threshold season of independent investigator, within the first six months after '
                         'taking the title: step 2, some weeks in, after the first paper or proposal sent out alone '
                         'comes back rejected',
             'likelier': 'working from home or a rented room; no colleagues nearby; a first submission to a '
                         'demanding journal or funder',
             'rarer': 'a shared workspace or a host lab; a submission that was accepted'},
 'scenes': {'earth': [('',
                       'The rejection comes on a Thursday: three short reviews, one of them unkind. With no group '
                       'around, there is nobody in the corridor to say it happens to everyone. The room is very '
                       'quiet.'),
                      ('W',
                       '{N} reads the reviews the way a judge reads a case: which points are fair, which are not, '
                       'and what the rules allow in reply.'),
                      ('U',
                       'Under the unkind tone, one reviewer has found a real gap in the analysis. {N} hates to admit '
                       'it, and cannot stop thinking about it.'),
                      ('B', 'The unkind reviewer writes a lot like {rival}. {N} files that away for later.'),
                      ('R', '{N} wants to fire off a reply tonight, every word of it true and burning.'),
                      ('G',
                       'In the old days {mentor} would have been down the hall. {N} looks at the phone for a long '
                       'time.')]},
 'outcomes': (['Within the week {N} is back at the work, and the next version is stronger for the beating.',
               'The silence breaks: someone {N} trusts reads the paper and says plainly what it needs.'],
              ['The paper sits in a folder for a month while {N} avoids it.',
               'The second journal says no as well, and {N} starts to wonder who the work is for.']),
 'options': [
    ('answer every point in order, concede the fair ones, and send it out again', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'chance': 0.85}),
    ('rerun the analysis to close the gap the harsh reviewer found', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'self_control': '+', 'grants': 'statistical judgment', 'chance': 0.72}),
    ('send it unchanged to the next journal on the list the same afternoon', 'B1', None, 0.45, '', {'v': 'achievement, self-direction', 'chance': 0.6}),
    ('write the reviewers a furious reply tonight, and send it', 'R1', None, 0.45, '', {'v': 'self-direction', 'mark': 'made an enemy', 'closed': 'approval: an angry letter to anonymous reviewers; backfire: the editor remembers the name', 'self_control': '-', 'chance': 0.35}),
    ('let it sit for a week, and walk every day before reading it again', 'G1', None, 0.45, '', {'v': 'tradition, security', 'self_control': '+', 'chance': 0.75}),
    ('ask the editor, through the proper channel, whether a revised version would be considered', 'W1', 'B.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.4}),
    ('turn the harsh review into a sharper, bolder second version', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'chance': 0.7}),
    ('take the steady post you were offered, and let the fellowship go', 'B1', 'G.7', 0.5, '', {'v': 'security', 'drops': 'independent investigator', 'self_control': '-', 'chance': 0.92}),
    ('ring a friend who was rejected too, and agree to swap drafts every month', 'R1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'chance': 0.88}),
    ('ring your old supervisor and ask which criticisms are worth answering', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'tradition, achievement', 'chance': 0.8}),
 ]},
{'name': 'whose question is this, really',
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'friend, mentor, partner, elder',
 'requires': 'independent investigator',
 'threshold': 'title:independent investigator',
 'step': 2,
 'transform': True,
 'worlds': {'earth': "months into working alone, you wonder whose question you are really answering: the funder's, "
                     "the field's, a place's, or your own"},
 'timing': {'times': 'once, in the first months after becoming an independent investigator, for the perhaps 1 in 2 '
                     'whose question has already drifted from the proposal; across all lives about 1 in 4,000 '
                     '(estimate)'},
 'trigger': {'requires': 'in the threshold season of independent investigator, within the first six months after '
                         "taking the title: step 2, the season's transforming chance, once the question has drifted "
                         'from the proposal',
             'likelier': 'a question that has sharpened since the proposal; an offer of money with strings; people '
                         'at the site who ask their own questions',
             'rarer': 'a fellowship with no room to change course; a question already settled'},
 'scenes': {'earth': [('',
                       'Months into the fellowship, {N} reads the original proposal again and barely recognises it. '
                       'The question has drifted, and {N} has to decide whose question this work is answering.'),
                      ('W',
                       'The fellowship was given for a stated purpose by people who trusted {N}. {N} feels bound to '
                       'them, and to the public whose money it is.'),
                      ('U',
                       'The question has sharpened into something stranger and more precise than the proposal. {N} '
                       'suspects the new one is the true one.'),
                      ('B',
                       'A company has offered money to point the work at their problem. With it, {N} would never '
                       'need a fellowship again.'),
                      ('R',
                       '{N} wakes up knowing exactly what the work is about, and it is nothing a committee would '
                       'fund.'),
                      ('G',
                       'The people who live by the {place} have their own question about it, older than any '
                       'proposal. {N} has been listening.')]},
 'outcomes': (['{N} knows whose question it is now, and the work runs faster for knowing.',
               'The people the work is for, whoever they turn out to be, start to rely on it.'],
              ['{N} swings between questions for months and finishes none of them.',
               'The choice costs {N} the people who backed the first question, and the money goes with them.']),
 'options': [
    ('return to the question you were funded for, and finish what was promised', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'conformity, benevolence', 'mark': 'kept your word', 'self_control': '+', 'chance': 0.72}),
    ('follow the sharper question, and write to the funders to explain the change', 'U1', None, 0.45, '', {'identity': True, 'v': 'self-direction, universalism', 'chance': 0.66}),
    ("take the company's money and build a practice that answers to no fellowship", 'B1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'power, self-direction', 'grants': 'patron', 'chance': 0.48}),
    ('chase the question nobody would fund, and stake your own savings on it', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'self-direction, stimulation', 'mark': 'took a wild risk', 'chance': 0.48}),
    ('take up the question the people of the place have always asked', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'benevolence, tradition', 'grants': 'community listening', 'chance': 0.62}),
    ('open the work to the public: a notebook online that anyone can follow and join', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism, stimulation', 'chance': 0.78}),
    ('let the work become a patient study of one living system, however long it takes', 'U1', 'G.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'universalism, tradition', 'chance': 0.72}),
    ('sell your speciality to public agencies as a service they can rely on', 'B1', 'W.7', 0.5, '', {'identity': True, 'v': 'power, security', 'chance': 0.75}),
    ('throw yourself into the strangest result in the data until it makes sense', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'stimulation', 'grants': 'a nose for the odd result', 'chance': 0.72}),
    ('tie the question to one place, and become the one who knows it best', 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'power, tradition', 'grants': 'fieldwork', 'chance': 0.72}),
 ]},
{'name': "a rhythm of one's own",
 'stages': 'young_adult adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'friend, partner, colleague',
 'requires': 'independent investigator',
 'threshold': 'title:independent investigator',
 'step': 3,
 'worlds': {'earth': 'months into working alone, your days have found a rhythm nobody set for you'},
 'timing': {'times': 'once, about six months after becoming an independent investigator, for those whose money still '
                     'holds; about 1 life in 2,000 ever works as an independent investigator (estimate)'},
 'trigger': {'requires': 'in the threshold season of independent investigator, within the first six months after '
                         'taking the title: step 3, near the end of the six months, as the new life settles',
             'likelier': 'money that still holds; a few people to talk the work over with',
             'rarer': 'money running short already; a rejection that still stings'},
 'scenes': {'earth': [('',
                       'Months in, {N} has stopped noticing that nobody sets the hours. Mornings for thinking, '
                       'afternoons for the dull work, a long walk at four. The work moves.'),
                      ('W',
                       '{N} keeps a ledger of hours and money, and the first report to the funders goes in a week '
                       'early.'),
                      ('U', '{N} has found the hours of the day when the hard thinking comes, and guards them.'),
                      ('B',
                       'Working alone means every hour is {Ns} own, and every hour is unpaid unless it pays. {N} has '
                       'learned to count them.'),
                      ('R', 'Some weeks {N} works ninety hours and some weeks barely ten. It feels like breathing.'),
                      ('G',
                       'The work follows the seasons at the {place}: busy when the water is high, quiet in the dead '
                       'of winter.')]},
 'outcomes': (['The rhythm holds through a bad week, and {N} trusts it now.',
               '{friend} says {N} looks better than in years, and means it.'],
              ['One late payment and one lost month, and the rhythm turns into worry.',
               'The days blur into each other, and {N} realises it has been a week since speaking to anyone.']),
 'options': [
    ('send the first progress report in early, with the accounts in order', 'W1', None, 0.45, '', {'v': 'conformity, security', 'chance': 0.9}),
    ('guard the best two hours of every morning for the hardest thinking', 'U1', None, 0.45, '', {'habit': True, 'v': 'achievement, self-direction', 'self_control': '+', 'chance': 0.8}),
    ("write the next grant application now, while the fellowship's name is fresh", 'B1', None, 0.45, '', {'v': 'achievement, security', 'self_control': '+', 'chance': 0.87}),
    ('spend the travel money on a trip that is mostly a holiday', 'R1', None, 0.45, '', {'v': 'hedonism', 'mark': 'hid a wrong', 'closed': "approval: fellowship money spent on a holiday; backfire: the funder's audit asks for the receipts", 'self_control': '-', 'chance': 0.88}),
    ('let the work follow the seasons at the site, busy and quiet in turn', 'G1', None, 0.45, '', {'v': 'tradition', 'chance': 0.78}),
    ('join a shared workspace where other lone researchers keep the same hours', 'W1', 'G.7', 0.5, '', {'door': True, 'v': 'security, benevolence', 'mark': 'made a friend', 'chance': 0.8}),
    ('write a short public note each month on what you found and what failed', 'U1', 'W.7', 0.5, '', {'habit': True, 'v': 'universalism', 'chance': 0.8}),
    ('trade analysis work with another independent researcher, skill for skill', 'B1', 'U.7', 0.5, '', {'v': 'achievement', 'grants': 'research collaborators', 'chance': 0.75}),
    ('say yes on the spot when a journalist rings about the work', 'R1', 'B.7', 0.5, '', {'v': 'stimulation, achievement', 'chance': 0.92}),
    ('bring your partner or a friend along on the field days, for the company', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'chance': 0.82}),
 ]},
{'name': 'your name on the door of the machine room',
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague',
 'requires': 'research facility lead',
 'threshold': 'title:research facility lead',
 'step': 1,
 'worlds': {'earth': 'the sign on the machine room door now carries your name, and with it the keys, the service '
                     'contracts and the queue'},
 'timing': {'times': 'once, in the first weeks after taking charge of a research facility: every new head meets it; '
                     'about 1 life in 2,000 ever runs a research facility (estimate)'},
 'trigger': {'requires': 'in the threshold season of research facility lead, within the first six months after '
                         "taking the title (opened by 'the facility needs a head' or any other appointment): step 1, "
                         'the first weeks in charge',
             'likelier': "a head who came up through the facility's own staff; a facility left with overdue "
                         'paperwork',
             'rarer': 'a facility handed over in perfect order; a head brought in from outside with a team of their '
                      'own'},
 'scenes': {'earth': [('',
                       'A new sign on the door of the machine room carries {Ns} name. With it come the master keys, '
                       'eleven service contracts, a queue of forty users and a budget spreadsheet nobody has opened '
                       'in a year.'),
                      ('W',
                       '{N} reads every service contract, safety certificate and user agreement, and finds three '
                       'certificates overdue.'),
                      ('U',
                       '{N} pulls the error logs for every machine and starts a list of which ones are drifting and '
                       'why.'),
                      ('B',
                       'The facility charges every group for its time. {N} realises the price list is power, and '
                       'nobody has changed it in six years.'),
                      ('R',
                       '{N} wants to fling the doors open and fill the place with people, now that nobody can say '
                       'no.'),
                      ('G',
                       '{N} has worked in this room for eight years. The machines feel less like equipment than like '
                       'old horses in a stable.')]},
 'outcomes': (['By the end of the week {N} knows where every problem is, and the users know who to come to.',
               '{boss} drops in, sees the logbook open and the queue moving, and leaves {N} to it.'],
              ['A machine goes down on the third day, and the first week is spent apologising.',
               'Something from the old ways gets changed too fast, and the technicians close ranks.']),
 'options': [
    ('sign the overdue safety certificates today, checked or not, as the rules require', 'W1', None, 0.45, '', {'v': 'conformity', 'mark': 'hid a wrong', 'closed': 'law: signing off safety checks that were never done; backfire: an inspector finds a machine that was never checked', 'self_control': '-', 'chance': 0.92}),
    ('spend the first nights running test samples on each machine to see where it stands', 'U1', None, 0.45, '', {'v': 'achievement', 'self_control': '+', 'chance': 0.8}),
    ('rewrite the price list so the facility finally pays its way', 'B1', None, 0.45, '', {'v': 'power, security', 'chance': 0.7}),
    ('throw the doors open on Friday for anyone who wants a tour, with music', 'R1', None, 0.45, '', {'v': 'hedonism, benevolence', 'chance': 0.92}),
    ('walk the room each morning before the users come, and listen to the machines', 'G1', None, 0.45, '', {'habit': True, 'v': 'tradition', 'chance': 0.92}),
    ('send every user a note asking what the facility does badly', 'W1', 'U.7', 0.5, '', {'v': 'universalism, achievement', 'chance': 0.75}),
    ('read the usage logs to find which groups book time and never use it', 'U1', 'B.7', 0.5, '', {'v': 'power', 'chance': 0.88}),
    ('keep the free nights on the big machine for a project of your own', 'B1', 'R.7', 0.5, '', {'habit': True, 'v': 'self-direction, achievement', 'self_control': '+', 'chance': 0.85}),
    ('take the technicians out for a drink and tell them the room is theirs too', 'R1', 'G.7', 0.5, '', {'v': 'benevolence', 'mark': 'made a friend', 'chance': 0.9}),
    ('keep the old logbooks on the shelf, and write in them as the old team did', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'chance': 0.9}),
 ]},
{'name': 'the old head still drops by',
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'elder, colleague, boss',
 'requires': 'research facility lead',
 'threshold': 'title:research facility lead',
 'step': 2,
 'worlds': {'earth': "the facility's old head has retired but still drops by most weeks, and the staff still go to "
                     'them first'},
 'timing': {'times': 'once, in the first months after taking charge of a research facility, for the perhaps 1 in 3 '
                     'whose predecessor retired nearby; across all lives about 1 in 6,000 (estimate)'},
 'trigger': {'requires': 'in the threshold season of research facility lead, within the first six months after '
                         'taking the title: step 2, some weeks in, while the former head still lives nearby',
             'likelier': 'a former head who ran the place for decades and retired locally; a new head who came up '
                         'from the staff',
             'rarer': 'a former head who moved away or fell out with the institute'},
 'scenes': {'earth': [('',
                       "{elder}, who ran the facility for twenty years, retired at the year's end but still drops by "
                       'most weeks with biscuits, and the technicians still take their questions to {elder} first.'),
                      ('W',
                       'There can only be one person in charge of a shared service, or nobody knows whose word '
                       'counts. {N} knows it, and dreads saying so.'),
                      ('U',
                       '{elder} knows things about the old instruments that are written down nowhere. Every visit is '
                       'a lesson {N} would be a fool to miss.'),
                      ('B',
                       'Every time a technician walks past {N} to ask {elder}, the staff learn who really runs the '
                       'place.'),
                      ('R', '{N} is fond of the old devil and also wants to shout. Both feelings arrive at once.'),
                      ('G',
                       'The old head is part of the place, like the worn step at the door. {N} wonders whether a '
                       'place ever really changes hands.')]},
 'outcomes': (["The old head's visits find their place, and the staff start bringing their questions to {N}.",
               '{elder} says, on the way out one afternoon, that the place is in good hands.'],
              ['{elder} takes offence and stops coming, and half the staff blame {N}.',
               'Nothing changes, and {N} is still the second person anyone asks.']),
 'options': [
    ('tell the old head kindly, in private, that questions now come to you', 'W1', None, 0.45, '', {'v': 'conformity, security', 'act': 'tell the old head kindly, in private, that questions now come to them', 'chance': 0.62}),
    ("record the old head's knowledge in long interviews before it is lost", 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'mark': 'learned a skill', 'chance': 0.85}),
    ("change the access cards, so visits go through the front desk like anyone's", 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'made an enemy', 'chance': 0.9}),
    ('have it out with the old head over a pint: all of it, loudly', 'R1', None, 0.45, '', {'v': 'self-direction', 'chance': 0.64}),
    ('let the visits go on, and trust the staff to come round in their own time', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'self_control': '+', 'chance': 0.45}),
    ('ask the director to give the old head an emeritus title with clear limits', 'W1', 'B.7', 0.5, '', {'v': 'power, conformity', 'chance': 0.68}),
    ('work out what the old head did best, and drop what was holding the place back', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, achievement', 'chance': 0.65}),
    ('hire the old head as a paid adviser, and keep the knowledge and the loyalty close', 'B1', 'G.7', 0.5, '', {'v': 'power', 'chance': 0.72}),
    ('tell the whole team, warmly and plainly, how things will run from now on', 'R1', 'W.7', 0.5, '', {'v': 'conformity, self-direction', 'chance': 0.75}),
    ('ask the oldest technician how the place has changed hands before', 'G1', 'U.7', 0.5, '', {'v': 'tradition', 'chance': 0.86}),
 ]},
{'name': 'what the facility is for',
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'boss, colleague, rival',
 'requires': 'research facility lead',
 'threshold': 'title:research facility lead',
 'step': 2,
 'transform': True,
 'worlds': {'earth': "the institute's review asks you to say in writing what the facility is for, and the answer "
                     'will set the next ten years'},
 'timing': {'times': 'once, in the first months after taking charge of a research facility, for the perhaps 1 in 2 '
                     'whose institute reviews it or sets its budget that year; across all lives about 1 in 4,000 '
                     '(estimate)'},
 'trigger': {'requires': 'in the threshold season of research facility lead, within the first six months after '
                         "taking the title: step 2, the season's transforming chance, when the institute's review "
                         "asks for the facility's purpose",
             'likelier': 'a review or a budget round in the first year; a new instrument on offer; groups competing '
                         'for time',
             'rarer': "a facility whose purpose is fixed by a funder's contract; a head with no say over the budget"},
 'scenes': {'earth': [('',
                       "The institute's review asks {N} one question, in writing: what is this facility for? The "
                       'answer will decide the budget, the hiring and the machines for the next ten years.'),
                      ('W',
                       'Forty groups depend on the facility, many of them small and poor. {N} thinks a shared '
                       'service exists so that everyone gets a fair turn.'),
                      ('U',
                       'The newest detector could measure what nobody in the country can measure yet, if the '
                       'facility spent five years learning it.'),
                      ('B',
                       'The facility holds the only machine of its kind for three hundred miles. Whoever runs it '
                       'holds something everyone needs.'),
                      ('R',
                       '{N} remembers the night when a facility head let a student try a mad idea on the big machine '
                       'at two in the morning. It changed everything for that student.'),
                      ('G',
                       'Some of these instruments have run for thirty years, and the records they made go back '
                       'further. {N} thinks the first duty is to keep them going.')]},
 'outcomes': (['The review accepts {Ns} answer, and the budget follows it.',
               'Within a year the users can say what the facility stands for, and they come for exactly that.'],
              ['The review picks another answer, and {N} has to run the facility for a purpose {N} argued against.',
               'The answer pleases nobody, and the budget is cut while the arguing goes on.']),
 'options': [
    ('write it as a fair service: open booking, fair prices, a turn for every group', 'W1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'universalism, conformity', 'chance': 0.65}),
    ('stake the facility on the new detector and the five years it takes to master', 'U1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'achievement, self-direction', 'chance': 0.45}),
    ('make the facility indispensable: exclusive methods, a waiting list, prices to match', 'B1', None, 0.45, '', {'identity': True, 'v': 'power', 'chance': 0.65}),
    ('keep a share of machine time for wild ideas from anyone, students included', 'R1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'stimulation, universalism', 'chance': 0.75}),
    ('put the long records first: keep the old instruments running and the archive whole', 'G1', None, 0.45, '', {'identity': True, 'binds': True, 'v': 'tradition', 'chance': 0.68}),
    ('open the doors to schools and the public one weekend a month', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'benevolence, universalism', 'chance': 0.75}),
    ('train every user properly, so the know-how lives in many hands', 'U1', 'G.7', 0.5, '', {'identity': True, 'v': 'universalism, benevolence', 'grants': 'supervising researchers', 'chance': 0.7}),
    ("sign long contracts with the big groups that guarantee the facility's money", 'B1', 'W.7', 0.5, '', {'identity': True, 'binds': True, 'v': 'security, power', 'chance': 0.68}),
    ('rebuild the old machine with your own hands, so it measures better than new', 'R1', 'U.7', 0.5, '', {'identity': True, 'v': 'achievement, stimulation', 'grants': 'instrument troubleshooting', 'self_control': '+', 'chance': 0.45}),
    ('close the facility to outside users, and keep it for the home institute', 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'security, tradition', 'mark': 'refused someone in need', 'closed': "approval: breaking the open-access terms the facility was funded on; backfire: the funder's review finds the outside groups turned away", 'chance': 0.45}),
 ]},
{'name': "the users' meeting goes quietly",
 'stages': 'young_adult adult mature',
 'age': (28, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.3,
 'tier': 'inner',
 'tone': 'joy',
 'life': 'work',
 'horizon': 'months',
 'roles': 'colleague, boss, rival',
 'requires': 'research facility lead',
 'threshold': 'title:research facility lead',
 'step': 3,
 'worlds': {'earth': "at the users' meeting nobody shouts, nobody threatens to leave, and the last question is about "
                     'science instead of booking'},
 'timing': {'times': 'once, near six months after taking charge of a research facility, for the perhaps 1 in 2 whose '
                     'booking rules and machines have held; across all lives about 1 in 4,000 (estimate)'},
 'trigger': {'requires': 'in the threshold season of research facility lead, within the first six months after '
                         'taking the title: step 3, near the end of the six months, as the facility settles',
             'likelier': 'booking rules that have held for a term; machines that have stayed up',
             'rarer': 'a breakdown in the last weeks; a quarrel over time still open'},
 'scenes': {'earth': [('',
                       "The users' meeting is over in fifty minutes. Nobody shouts about the booking system, nobody "
                       'threatens to take their samples elsewhere, and the last question is about science.'),
                      ('W',
                       'The booking rules have held all term without a single complaint to the director. {N} reads '
                       'the minutes twice to be sure.'),
                      ('U',
                       'One of the last questions is about a measurement nobody could make here a year ago. {N} '
                       'answers it in detail.'),
                      ('B',
                       '{rival}, who complained loudest last time, said nothing at all. {N} wonders what that '
                       'silence is worth.'),
                      ('R',
                       '{N} had a speech ready for a fight, and there was no fight. The relief feels almost like '
                       'disappointment.'),
                      ('G',
                       'The technicians stay after the meeting to finish the coffee and talk. The room feels like '
                       'theirs again.')]},
 'outcomes': (['The quiet holds into the next term, and the users start asking what else the facility could do.',
               '{boss} forwards the minutes to the director with one line: this is how it should look.'],
              ['The calm was only tiredness, and the old quarrels are back by the next booking round.',
               'A machine fails the week after, and the good meeting is forgotten.']),
 'options': [
    ("send everyone the minutes and the year's figures, as you promised", 'W1', None, 0.45, '', {'v': 'conformity', 'mark': 'kept your word', 'chance': 0.92}),
    ("use the quiet to plan next year's upgrade in detail", 'U1', None, 0.45, '', {'v': 'achievement', 'chance': 0.82}),
    ('make sure the director hears the meeting went quietly, and who made it so', 'B1', None, 0.45, '', {'v': 'power, achievement', 'chance': 0.85}),
    ('take the team out to celebrate, and leave the paperwork until Monday', 'R1', None, 0.45, '', {'v': 'hedonism', 'chance': 0.88}),
    ('let the planned upgrade slide a year, since nothing is going wrong', 'G1', None, 0.45, '', {'v': 'tradition, security', 'self_control': '-', 'chance': 0.86}),
    ('write a handbook so the facility keeps its ways when the next head comes', 'W1', 'G.7', 0.5, '', {'v': 'security, tradition', 'chance': 0.72}),
    ("publish the facility's uptime and error figures for every user to see", 'U1', 'W.7', 0.5, '', {'v': 'universalism', 'chance': 0.88}),
    ('get the maker to lend a new detector, for your name in their brochure', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'chance': 0.7}),
    ("buy last time's loudest complainer a drink, and win them over for good", 'R1', 'B.7', 0.5, '', {'v': 'power, benevolence', 'mark': 'made a friend', 'chance': 0.76}),
    ('enjoy a quiet week at the machines, doing the hands-on work you love', 'G1', 'R.7', 0.5, '', {'v': 'hedonism', 'chance': 0.92}),
 ]},
]

ECHOES = [
{'name': 'the finding will not leave you alone',
 'stages': 'young_adult adult mature elder',
 'age': (18, 92),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.03,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'mentor, boss, colleague, friend, partner',
 'once': True,
 'worlds': {'earth': 'months after the breakthrough in your work, the question behind it keeps you awake at night'},
 'timing': {'times': 'per person outside research in the two years after a breakthrough in their own work: perhaps 1 '
                     'in 10 find its question keeps pulling at them, and few of those turn to research; across all '
                     'lives perhaps 1 in 15 meet it (estimate)'},
 'after': "event lived through: 'a breakthrough in your work' within the last two years, and no research career "
          'title held (the person works at something else: a ward, a workshop, a farm, a school, an office)',
 'delay_years': (0, 2),
 'likelier': 'a degree; a friend, partner or mentor in research; time and money to spare; a curious bent (much Blue '
             'or Red in the color history)',
 'rarer': 'a research title already held; stress above 1.5; heavy care duties; money below 0.2',
 'scenes': {'earth': [('',
                       'Months after it first worked, {N} still turns it over on the way home: not the result '
                       'itself, but the question behind it. Why did it work, and would it work anywhere else?'),
                      ('W',
                       'Something that works ought to be checked properly, by people whose job it is, so that others '
                       'can rely on it. Leaving it in a drawer feels to {N} like a duty left undone.'),
                      ('U',
                       'Every answer has opened two new questions, and {N} has filled half a notebook with them. '
                       'Read back, the notebook looks a lot like a research plan.'),
                      ('B',
                       'A university two towns away works on exactly this, and has no idea that {N} exists. {N} sees '
                       'no reason why that should stay so.'),
                      ('R',
                       'The finding has the grip of a first love. {N} lies awake planning experiments that would '
                       'need a lab {N} does not have.'),
                      ('G',
                       'It grew out of years of ordinary work, the way a path forms where people keep walking. {N} '
                       'wonders whether to follow the path further, or let it be what it was.')]},
 'outcomes': (['The question gets a proper home at last, and {N} sleeps through the night again.',
               'Someone who knows the field takes {N} seriously, and the work begins to go somewhere.'],
              ['Nobody answers, the notes go into a box, and the question goes on nagging.',
               'The second try does not work, and {N} begins to wonder whether the first one really did.']),
 'options': [
    ('write it up carefully, and send it to the department that studies such things', 'W1', None, 0.45, '', {'door': True, 'v': 'universalism, conformity', 'chance': 0.6}),
    ('apply for a research assistant post, to learn to study it properly', 'U1', None, 0.45, '', {'binds': True, 'v': 'self-direction, achievement', 'title': 'research assistant', 'requires': 'graduate', 'without': 'impossible', 'chance': 0.55}),
    ('offer the professor your notes in return for a place on the team', 'B1', None, 0.45, '', {'door': True, 'binds': True, 'v': 'achievement, power', 'title': 'research assistant', 'requires': 'graduate', 'without': 'impossible', 'chance': 0.5}),
    ('turn the spare room into a workbench, and chase it every evening and weekend', 'R1', None, 0.45, '', {'habit': True, 'v': 'stimulation, self-direction', 'grants': 'a research project under way', 'self_control': '+', 'chance': 0.8}),
    ('let it be what it was: a good piece of work, and enough', 'G1', None, 0.45, '', {'v': 'tradition', 'mark': 'turned down a chance', 'chance': 0.85}),
    ('join the citizen science project closest to the question, and do it by the book', 'W1', 'R.7', 0.5, '', {'v': 'universalism, stimulation', 'title': 'citizen scientist', 'chance': 0.85}),
    ('read everything published on it, slowly, over the winter evenings', 'U1', 'G.7', 0.5, '', {'habit': True, 'v': 'self-direction, universalism', 'chance': 0.92}),
    ('pay for proper tests out of your own savings, and keep a full record', 'B1', 'W.7', 0.5, '', {'v': 'achievement, security', 'grants': 'a research project under way', 'self_control': '+', 'chance': 0.85}),
    ('borrow the equipment at work after hours to test it, without asking anyone', 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'mark': 'hid a wrong', 'closed': "approval: using the employer's equipment without leave; backfire: the night log shows the hours, and the manager wants to know why", 'chance': 0.65}),
    ('keep it inside the team, as the quiet edge your workplace has over the rest', 'G1', 'B.7', 0.5, '', {'v': 'power', 'chance': 0.6}),
 ]},
{'name': 'a question from childhood comes back',
 'stages': 'young_adult adult mature elder',
 'age': (27, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'leisure, meaning, nature',
 'horizon': 'months',
 'roles': 'grandparent, child, friend, partner',
 'once': True,
 'worlds': {'earth': 'something small brings back a question you chased as a child, and for once there is time to '
                     'follow it'},
 'timing': {'times': 'per adult who chased a question or felt awe as a child: perhaps 1 in 10 come back to it once '
                     'there is time, most often after the children leave home or at retirement; across all lives '
                     'perhaps 1 in 12 (estimate)'},
 'after': "moment 'a curiosity that will not let go' or 'awe' lived through as a child or teenager, and now an adult "
          'with time to spare (time above 0.4: fewer hours at work, children grown, retired)',
 'delay_years': (15, 50),
 'likelier': 'retirement or fewer working hours; children grown; a child or grandchild asking the same question; a '
             'move back to the place where it began',
 'rarer': 'stress above 1.5; money below 0.2; long working hours; poor health',
 'scenes': {'earth': [('',
                       "Something small brings it back: a child's question at bedtime, a programme on the radio, the "
                       'smell of wet earth after rain. The thing {N} wondered about at fourteen, and dropped when '
                       'life got busy, is still there.'),
                      ('W',
                       '{N} was always told there would be time for such things later. Now the hours are finally '
                       '{Ns} own, and the old question feels like a promise still to keep.'),
                      ('U',
                       '{N} remembers exactly what was left unanswered back then. The answer might be sitting in a '
                       'library by now, or the question might still be open.'),
                      ('B',
                       'What once seemed a childish question now looks like a corner of knowledge {N} could make '
                       '{Ns} own. Nobody else in town has bothered with it.'),
                      ('R',
                       'The old wonder comes back whole, like a song from the summer {N} was fourteen, and {N} wants '
                       'to drop everything and go after it.'),
                      ('G',
                       '{N} remembers {grandparent} naming the stars from the back step, one by one. The question '
                       'has waited all these years, like seeds kept in a drawer.')]},
 'outcomes': (['Within a season the old question has a shape again, and {Ns} weekends hold something entirely {Ns} '
               'own.',
               'Someone who knows the subject answers {Ns} letter, and {N} finds there is still useful work for a '
               'beginner.'],
              ['The first weeks are a tangle of jargon and wrong turns, and the old wonder goes flat.',
               'Life fills the free hours up again, and the question goes back into its drawer.']),
 'options': [
    ('sign up for the long-running survey nearest the old question, and keep its schedule', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'title': 'citizen scientist', 'chance': 0.8}),
    ('enrol in an evening course on the subject, and do every piece of the coursework', 'U1', None, 0.45, '', {'door': True, 'v': 'self-direction, achievement', 'mark': 'learned a skill', 'chance': 0.85}),
    ("make the question your own project, and become the town's expert on it", 'B1', None, 0.45, '', {'v': 'achievement, power', 'grants': 'a research project under way', 'chance': 0.7}),
    ('buy the kit it needs tomorrow, and go out with it that same evening', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'chance': 0.95}),
    ('let it rest: some questions are better kept as wonder than answered', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'chance': 0.85}),
    ("offer to keep the village's weather or bird record, as someone always has", 'W1', 'G.7', 0.5, '', {'binds': True, 'v': 'tradition, benevolence', 'title': 'community observer', 'chance': 0.7}),
    ('write to a scientist who studies it, and offer careful hours to the work', 'U1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'chance': 0.65}),
    ('pay for good equipment and a few lessons with an expert, and catch up fast', 'B1', 'U.7', 0.5, '', {'door': True, 'v': 'achievement, self-direction', 'mark': 'learned a skill', 'aims': 'independent investigator', 'chance': 0.8}),
    ('start a blog or a channel about the question, and see who comes to follow', 'R1', 'B.7', 0.5, '', {'identity': True, 'v': 'stimulation, achievement', 'chance': 0.55}),
    ('return every month to the place where it began, and watch it as before', 'G1', 'R.7', 0.5, '', {'habit': True, 'v': 'tradition, hedonism', 'title': 'community observer', 'self_control': '+', 'chance': 0.65}),
 ]},
{'name': 'the old door opens a crack',
 'stages': 'young_adult adult mature elder',
 'age': (28, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.2,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'mentor, friend, partner, colleague, rival',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, the same kind of door opens again, and someone '
                     'remembers your first try',
            'tribal': 'many winters after the elders said not yet, the same place is open again, and someone '
                      'remembers your first asking',
            'magic': 'years after the Academy refused your petition, the same kind of post is offered again, and a '
                     'master remembers your name'},
 'timing': {'times': 'per person whose science long shot missed and who is still on the rung below it: perhaps 1 in '
                     '4 go for the same kind of post or money again within about ten years (estimate); in several '
                     "large funders' published figures a resubmitted proposal is funded about one and a half to two "
                     'times as often as a first submission, so a second try runs a little better than the first '
                     '(approximate)'},
 'after': "perk [a long shot that missed] gained at 'a discovery nobody asked you for', 'a group of your own, open "
          "to all comers', 'a facility looks outside for its next head', 'a search for a new voice for science', 'a "
          "chair falls vacant at another university', 'a scientist's post at a famous lab', 'a named fellowship, one "
          "a year', 'a national centre opens its posts' or 'the survey wants a paid assistant' (the try for the "
          'title missed), the title still not held, and the person still on the rung below it',
 'delay_years': (3, 12),
 'likelier': 'a publication, a grant, savings or a patron since the first try; a mentor or collaborator who '
             'remembers the first application; years of supervising others; the old find confirmed by someone else',
 'rarer': 'stress above 1.5; poor health; heavy care duties; money below 0.15',
 'scenes': {'earth': [('',
                       'The call comes years later, from an unexpected side: the same kind of post, or the same kind '
                       'of money, open again, and a note from someone who sat on the old panel. We remember the '
                       'first application, it says. Do try again.'),
                      ('W',
                       'This time {N} knows exactly what the forms want, and where the first application fell short. '
                       'The gaps have been filled one by one over the years, like a ledger brought up to date.'),
                      ('U',
                       'Since the first no, {N} has kept working on the question in odd hours, and the evidence has '
                       'grown. Read side by side, the old case looks like a draft of the new one.'),
                      ('B',
                       'The first try was not wasted: {N} learned who decides, and who listens to whom. Some of '
                       'those people now return {Ns} calls.'),
                      ('R',
                       'The old hunger comes back all at once, as if no years had passed, and {Ns} heart is going '
                       'faster than it has in a long time.'),
                      ('G',
                       '{N} thinks of the people who backed the first try and never said a word of reproach when it '
                       'failed. Going again would be for them as much as for {N}.')],
            'tribal': [('',
                        'Many winters after the elders said not yet, the eldest healer sends word to {Ns} hearth: '
                        'the band would hear again what {N} once asked for.')],
            'magic': [('',
                       "Years after the petition was refused, a letter comes under the Academy's seal: the same kind "
                       "of post is open again, and a line in a master's hand recalls the old petition with "
                       'respect.')]},
 'outcomes': (['This time the answer is yes, and {N} keeps the old letter of refusal in the same drawer as the new '
               'one, for the symmetry.',
               'The second try lands where the first could not, and {N} starts the work as if the years between had '
               'been preparation.'],
              ['The second no is kinder than the first, and more specific: two of the three on the panel said yes. '
               '{N} reads the third opinion once, and does not read it again.',
               'The application goes in on the last night, and the answer is the same as before; this time {N} finds '
               'it easier to laugh.']),
 'options': [
    ('apply again, every gap in the first application closed one by one', 'W1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, achievement', 'world': {'tribal': "ask the elders again in the proper way, with every winter's learning since", 'magic': 'petition again by every form, each lack of the first petition made good'}, 'chance': 0.07}),
    ('send the new case: the years of work gathered since the first no', 'U1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'bring the elders everything you have watched and tried in the winters since', 'magic': 'send the Academy the new tables, years of work gathered since the refusal'}, 'chance': 0.07}),
    ('write to the panel member who praised the first try, and ask for a word', 'B1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'go first to the elder who spoke kindly of you last time, and ask for her voice', 'magic': 'write to the master who praised the first petition, and ask for his word at the council'}, 'chance': 0.07}),
    ('say yes before the doubts can start, and go for it again with everything', 'R1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation', 'world': {'tribal': 'stand up at the fire and ask again before anyone can say it is too late', 'magic': 'send the petition the same night, before the doubts can wake'}, 'chance': 0.07}),
    ('go again with the people who stood by the first try, their names beside yours', 'G1', None, 0.45, '', {'act': 'go again with the people who stood by the first try, their names beside theirs', 'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'ask again with the families who stood by you the first time beside you at the fire', 'magic': "petition again with your guild's names beside yours on the scroll"}, 'chance': 0.07}),
    ('ask what the first try lacked, and mend it piece by piece for next time', 'W1', 'B.7', 0.5, '', {'mark': 'learned a skill', 'door': True, 'v': 'conformity, achievement', 'world': {'tribal': 'ask the elders what the first asking lacked, and mend it season by season', 'magic': 'ask the council what the first petition lacked, and mend it piece by piece'}, 'chance': 0.85}),
    ('test the old plan again on your own time before deciding anything', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'go back to the hill alone for a moon and test the old plan before deciding', 'magic': 'test the old plan again in the attic before deciding anything'}, 'chance': 0.85}),
    ('keep the day job, and build the case slowly on the side for the next round', 'B1', 'G.7', 0.5, '', {'self_control': '+', 'v': 'security, achievement', 'world': {'tribal': 'keep hunting with the band, and gather the proof slowly for the next gathering', 'magic': 'keep your post, and build the case by candlelight for the next opening'}, 'chance': 0.85}),
    ('turn it down cheerfully, and keep the promises already made to others', 'R1', 'W.7', 0.5, '', {'mark': 'turned down a chance', 'v': 'benevolence, conformity', 'world': {'tribal': 'say no gladly, and keep the promises already made at your own hearth', 'magic': 'decline with a light heart, and keep the promises already made to your household'}, 'chance': 0.85}),
    ('ask the people who know the work best whether it is ready, and listen', 'G1', 'U.7', 0.5, '', {'v': 'tradition, universalism', 'world': {'tribal': 'ask the oldest watchers whether the time is right, and wait for their answer', 'magic': 'ask the scholars who know the work best whether it is ready, and listen'}, 'chance': 0.85}),
 ]},
{'name': 'the story of the long shot',
 'stages': 'adult mature elder',
 'age': (32, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.1,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'meaning, community',
 'horizon': 'years',
 'roles': 'friend, partner, colleague, mentor, grandparent',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, someone asks about it, and you find out how you tell it '
                     'now',
            'tribal': 'at a winter fire, years after the long try, a young one asks about it, and you hear how you '
                      'tell it now',
            'magic': 'years after the refused petition, a young scholar asks about it, and you hear how you tell it '
                     'now'},
 'timing': {'times': 'per person whose science long shot missed: perhaps 1 in 3 come, years later, to tell it as '
                     'part of who they are rather than as a wound (estimate); studies of regret find that over the '
                     'long run people regret the chances they did not take more than the attempts that failed'},
 'after': "perk [a long shot that missed] gained at one of the pack's long-shot moments ('a discovery nobody asked "
          "you for', 'a group of your own, open to all comers', 'a facility looks outside for its next head', 'a "
          "search for a new voice for science', 'a chair falls vacant at another university', 'a scientist's post at "
          "a famous lab', 'a named fellowship, one a year', 'a national centre opens its posts', 'the survey wants a "
          "paid assistant', or the second try 'the old door opens a crack'), at least five years ago",
 'delay_years': (5, 25),
 'likelier': 'retirement or fewer working hours; someone younger trying something similar; a reunion, a talk or a '
             "grandchild's question; a second try that landed, or one let go",
 'rarer': 'stress above 1.5; a fresh loss; the long shot still raw',
 'scenes': {'earth': [('',
                       'Somebody asks about it at last: a younger colleague, a student, a neighbour at a party. Did '
                       '{N} not once go for that? And from the way the answer comes out, {N} finds out how the story '
                       'is told these days.'),
                      ('W',
                       '{N} sees now what the attempt was: a promise to the work, made in the open and by the rules. '
                       'That it failed does not undo the keeping of it.'),
                      ('U',
                       'Over the years {N} has worked out exactly why it missed: two things that could have been '
                       'done better, and three that were luck. The account is clear, and clarity is a kind of '
                       'peace.'),
                      ('B',
                       'The attempt opened doors nobody saw at the time: names, a reputation for nerve, people who '
                       'remembered. {N} can count what it paid, and the sum is not small.'),
                      ('R',
                       '{N} laughs before getting to the end of the story. What a thing it was, to go for it like '
                       'that, and how alive it felt at the time.'),
                      ('G',
                       'The notebook from that year is still on the shelf, between the seed catalogues and the '
                       'photographs. {N} does not need to open it to know what is inside.')],
            'tribal': [('',
                        'At the winter fire a young hunter asks {N} about the year of asking the elders, and the '
                        'whole hearth goes quiet to listen.')],
            'magic': [('',
                       "A young scholar at the Academy's gate recognises {Ns} name from an old petition, and asks, "
                       'shyly, how it felt to be refused.')]},
 'outcomes': (['The story comes out lighter than {N} expected, and someone at the table says it is the best thing '
               'they have heard all year.',
               'Telling it, {N} finds that the attempt has become a good part of the life, and not a wound in it.'],
              ['The old sting is still there after all, and {N} changes the subject before the end.',
               'Halfway through the telling {N} hears the old excuses creeping back, and stops; it is not quite told '
               'yet.']),
 'options': [
    ('teach the method the attempt taught you, properly, to a class that wants it', 'W1', None, 0.45, '', {'act': 'teach the method the attempt taught them, properly, to a class that wants it', 'grants': 'teaching', 'identity': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'teach the young watchers the patient ways the long try taught you', 'magic': "take a class at the Academy's lesser school, and teach the method properly"}, 'chance': 0.88}),
    ('write the honest account: what was tried, what was learned, and why it missed', 'U1', None, 0.45, '', {'identity': True, 'v': 'universalism, self-direction', 'world': {'tribal': 'shape the whole tale truly for the singers, the missing as well as the trying', 'magic': 'write the honest memoir of the petition, the errors as well as the hopes'}, 'chance': 0.88}),
    ('turn the story into a talk that gets you asked back again and again', 'B1', None, 0.45, '', {'act': 'turn the story into a talk that gets them asked back again and again', 'grants': 'public speaking', 'identity': True, 'v': 'achievement, power', 'world': {'tribal': 'make the tale one the bands ask you to tell at every gathering', 'magic': 'make the tale a lecture the guild halls pay to hear'}, 'chance': 0.88}),
    ('tell it at the table as the best story you own, laughing at the ending', 'R1', None, 0.45, '', {'act': 'tell it at the table as the best story they own, laughing at the ending', 'mark': 'made a friend', 'identity': True, 'v': 'hedonism, stimulation', 'world': {'tribal': 'tell it at the fire as the best tale you have, laughing loudest at the end', 'magic': 'tell it in the tavern as the best tale you own, laughing at the ending'}, 'chance': 0.88}),
    ('put the old notebook back on the shelf, and let it rest there for good', 'G1', None, 0.45, '', {'identity': True, 'self_control': '+', 'v': 'tradition', 'world': {'tribal': 'lay the old marking-stick back in the roof thatch, and let it rest there', 'magic': 'shelve the old petition with your other papers, and let it rest there'}, 'chance': 0.88}),
    ('cheer at the front when a young person from the club tries the same thing', 'W1', 'R.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'shout loudest at the fire when a young watcher asks the elders the same thing', 'magic': 'cheer from the front row when a young scholar petitions the Academy'}, 'chance': 0.85}),
    ('give the old kit and notes to the club, for the next one who wonders', 'U1', 'G.7', 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': "give your marking-sticks and your lore to the band's young, for the next one who wonders", 'magic': 'give your lens and your ledgers to the guild school, for the next one who wonders'}, 'chance': 0.85}),
    ('put your name and some money behind a small fund for first attempts', 'B1', 'W.7', 0.5, '', {'v': 'power, benevolence', 'world': {'tribal': 'give a share of each hunt to feed the next young one who goes to learn', 'magic': 'found a small purse in your name for first petitions to the Academy'}, 'chance': 0.85}),
    ('take up something new and hard, just to feel the old nerve again', 'R1', 'U.7', 0.5, '', {'mark': 'learned a skill', 'self_control': '+', 'v': 'stimulation', 'world': {'tribal': 'learn a hard new craft from another band, just to feel the old nerve', 'magic': 'take up a hard new study, just to feel the old nerve again'}, 'chance': 0.85}),
    ('frame the letter that said no, with its one kind sentence underlined', 'G1', 'B.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "keep the elders' answer in a knotted cord at the hearth, the kind word knotted twice", 'magic': "frame the Academy's letter of refusal, its one kind sentence underlined"}, 'chance': 0.85}),
 ]},
]

EVENTS_READ = [{'name': 'the results are in',
  'source': 'work',
  'tone': 'mixed',
  'base': 'need:competence+.05',
  'worlds': {'earth': "a year's results come back, and they show nothing: no effect, or nothing anyone can be sure "
                      'of'},
  'timing': {'times': 'per person with a research project under way: about once a year a planned analysis or a '
                      "season's data comes back; roughly half of honest studies end null or inconclusive (estimate)",
             'likelier': 'careful designs that give the idea a real chance to be wrong, small samples, hard '
                         'questions',
             'rarer': 'projects that only describe or count, very large studies',
             'window': (18, 80),
             'gap_years': (0.5, 2.0)},
  'readings': [('a duty done: an honest answer is still an answer, and it belongs on the record',
                'W1',
                1.0,
                'meaning+.05',
                'W',
                '{N} writes the null result up properly and sends it where others will find it.'),
               ('a puzzle: if the effect is not there, something else explains what was seen',
                'U1',
                1.0,
                'competence+.05',
                'U',
                '{N} pins the flat graph above the desk and starts listing what else could explain it.'),
               ('a waste: a year that bought nothing, so the next question must pay its way',
                'B1',
                0.6,
                'autonomy+.05',
                'B',
                '{N} totals what the year cost and starts choosing a question that will pay for itself.'),
               ('a heartbreak: the idea that mattered most is simply not true',
                'R1',
                0.6,
                'belonging+.05',
                'R',
                '{N} stares at the screen for a long time, then rings {friend} and talks it through over a drink.'),
               ('the way things are: the world owes nobody a result',
                'G1',
                0.9,
                'safety+.05',
                'G',
                "{N} shrugs, waters the plants on the windowsill, and plans next season's sampling.")],
  'scenes': {'earth': [('',
                        'The last batch comes back on a Tuesday. {N} runs the analysis twice, and the two lines on '
                        'the graph lie on top of each other: whatever {N} expected to see is not there.')]}}]

MARKS = {}
