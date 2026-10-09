"""Chroma library earth_play: compiled by build.py from earth_play.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'the day it all comes to a head',
 'stages': 'child juvenile young_adult adult mature elder',
 'age': (14, 110),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.8,
 'rate': 0.0,
 'tier': 'inner',
 'tone': 'mixed',
 'life': 'home, work, friends',
 'horizon': 'years',
 'roles': 'friend, partner, parent',
 'worlds': {'earth': 'for a long time you have lived one way while something in you pulls another, and now it cannot '
                     'go on'},
 'timing': {'times': 'In played lives only, at most once or twice a life, when the steering has run against them for '
                     "a long time (the game's hook)",
            'gap_years': (5.0, 30.0)},
 'trigger': {'requires': "a played life only (the game's hook, never the engine's rates): the price of the player's "
                         "pushes against the character's own pull (strain, pent-up wanting and stress from steered "
                         "picks) has built past the game's line over a season or more",
             'likelier': 'many heavy pushes against them; pushes resented in hindsight; low trust in the voice; a '
                         'shadow growing in the color pushed against',
             'rarer': 'pushes they came to own (accepted in hindsight); high trust in the voice; a life the player '
                      'mostly leaves to them'},
 'scenes': {'earth': [('',
                       'For a long time now {N} has been living one way while something deeper pulls another. '
                       'Tonight, alone, {N} knows it cannot go on like this. One of them has to win.'),
                      ('W',
                       '{N} has done what was asked for so long that {N} no longer knows which duties are their own. '
                       'Something has to give, and it has to be decided now.'),
                      ('U',
                       '{N} lies awake turning it over: which of these two lives is the real one? There is no more '
                       'time to study it. {N} has to choose.'),
                      ('B',
                       '{N} counts what this double life has cost, and the sum is too high. Tonight {N} decides '
                       'which self gets the rest of it.'),
                      ('R',
                       'It boils over. {N} is shaking with it, done with half measures and done with pretending.'),
                      ('G',
                       'Like a tree grown crooked against a wall, {N} has bent as far as a person can bend. Now it '
                       'either breaks, or it settles.')]},
 'outcomes': (['{N} wakes the next morning as someone who has decided, and the decision holds.',
               'It is not easy, but the two halves of {N} stop fighting. One of them has won.'],
              ['{N} decides, and within weeks the old pull is back as strong as ever.',
               'The resolve breaks on the first hard day, and {N} is pulled two ways again.']),
 'options': [
    ('from now on, live by your duties and keep faith with those who count on you', 'W1', None, 0.45, '', {'identity': True, 'v': 'conformity, benevolence', 'act': 'settle for good on a life of duty and keeping faith', 'chance': 0.55}),
    ('from now on, think things through and follow what you find to be true', 'U1', None, 0.45, '', {'identity': True, 'v': 'self-direction', 'act': 'settle for good on a life of thinking things through', 'chance': 0.55}),
    ('from now on, put your own way first and make of your life what you choose', 'B1', None, 0.45, '', {'identity': True, 'v': 'achievement, power', 'act': 'settle for good on putting their own way first', 'chance': 0.55}),
    ('from now on, follow your heart wherever it goes, whatever it costs', 'R1', None, 0.45, '', {'identity': True, 'v': 'stimulation, hedonism', 'act': 'settle for good on following their heart', 'chance': 0.55}),
    ('from now on, accept who you are and stay rooted where you belong', 'G1', None, 0.45, '', {'identity': True, 'v': 'tradition, security', 'act': 'settle for good on staying rooted in who they are', 'chance': 0.55}),
 ]},
]

ECHOES = [
]

EVENTS_READ = []

MARKS = {}
