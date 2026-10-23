"""Chroma library earth_clash: compiled by build.py from earth_clash.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'the new rule at home',
 'stages': 'juvenile young_adult',
 'age': (10, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'family, home',
 'horizon': 'months',
 'roles': 'parent, sibling, grandparent, friend',
 'clash': 'household',
 'band': 'teen',
 'worlds': {'earth': 'a new rule at home, back by nine on school nights, and it falls on the one evening that '
                     'matters',
            'tribal': 'a new rule of the hearth, back inside the camp by dark, on the very nights that matter most '
                      'to {N}',
            'magic': 'a new rule of the house, doors barred at the ninth bell, on the one evening {N} lives for'},
 'timing': {},
 'scenes': {'earth': [('',
                       'A new rule has come down from {clash.holder} for everyone in {clash.setting}: back by nine '
                       'on school nights, and no arguing about it. The one evening of the week that matters most to '
                       '{N} runs until ten. The whole house is waiting to see what {N} does.')],
            'tribal': [('',
                        'The word from {clash.holder} has been said at the fire: back inside the camp by dark, every '
                        'night, no exceptions. The gatherings {N} cares about begin after dark. The whole hearth is '
                        'waiting to see what {N} does.')],
            'magic': [('',
                       'The wards of {clash.setting} now close at the ninth bell, on the word of {clash.holder}. The '
                       'one evening {N} lives for runs past the tenth. The household is waiting to see what {N} '
                       'does.')]},
 'outcomes': (['The rule stays, but the one evening is allowed once a fortnight. Nobody quite won, and the house is '
               'calmer for it.',
               'It takes a month of trying, and by the end of term the evening is {Ns} again, on conditions {N} did '
               'not choose.'],
              ['Nothing moves. The rule stands as it was, {N} misses the evening, and the house goes quiet in a cold '
               'way.',
               'It half works: the rule bends for two weeks, then snaps back the first time {N} is late.']),
 'options': [
    ('write down why the rule is unfair, and ask for a proper family vote', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'clash': 'confront', 'chance': 0.5}),
    ('keep to the rule until the end of term, noting how it goes', 'U1', None, 0.45, '', {'v': 'self-direction, security', 'clash': 'give_in', 'chance': 0.85}),
    ("make a deal to sleep at {grandparent}'s on the nights that matter", 'B1', None, 0.45, '', {'v': 'power, self-direction', 'clash': 'leave', 'chance': 0.55}),
    ('spend every free hour you do have with the crowd at {clash.scene}', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'clash': 'own_scene', 'chance': 0.75}),
    ('ask {clash.ally} to sit down one evening with them and {clash.holder}', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'clash': 'bridge', 'chance': 0.6}),
    ('apply for the summer course that boards away from home, every form done right', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'clash': 'leave', 'chance': 0.6}),
    ('find a club that meets before nine, and soon help run it', 'U1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'clash': 'own_scene', 'chance': 0.7}),
    ('offer a trade: home early all week, for one late evening a week', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'bridge', 'chance': 0.55}),
    ('argue it out loud at dinner, with {sibling} on your side', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'clash': 'confront', 'chance': 0.45}),
    ('agree to the rule and mean it: the house runs better with it', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'clash': 'give_in', 'chance': 0.9}),
 ]},
{'name': 'the list on the kitchen wall',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'family, home, money',
 'horizon': 'months',
 'roles': 'parent, partner, sibling, friend',
 'clash': 'household',
 'band': 'adult',
 'worlds': {'earth': 'a list on the kitchen wall says how the house is run now, and one line of it cuts across {Ns} '
                     'plans',
            'tribal': "the elders of the hearth have shared out the winter's work and stores, and one share costs "
                      '{N} dearly',
            'magic': 'a sealed scroll of household rules hangs by the hearth, and one rule takes the very hours {N} '
                     'planned for'},
 'timing': {},
 'scenes': {'earth': [('',
                       'A list is pinned to the kitchen wall, in the hand of {clash.holder}: how {clash.setting} '
                       'will be run from now on, who pays for what and who decides. Most of it is fair. One line, '
                       'about {Ns} evenings and {Ns} share of the money, cuts straight across the life {N} has been '
                       'building.')],
            'tribal': [('',
                        "The elders of the hearth have shared out the winter's work and stores. Most of it is fair. "
                        'The part that falls on {N} takes the days {N} had set aside for something of {Ns} own, and '
                        '{clash.holder} will not hear a word against it.')],
            'magic': [('',
                       'A new scroll of household rules hangs by the hearth, sealed by {clash.holder}. Most of it is '
                       "fair. One rule, about who may use the house's study and when, takes the very hours {N} had "
                       'planned for.')]},
 'outcomes': (['The line is rewritten, not the way {N} wanted it, but in a way {N} can live with. The list stays on '
               'the wall.',
               '{N} gets the evenings back, and pays for them with a bigger share of the chores.'],
              ['Nothing changes. The list stays as it is, and the kitchen is a tense place for a while.',
               'It half works: the money part is settled, and the evenings are argued over every week.']),
 'options': [
    ('agree to the list as written, and keep your part of it', 'W1', None, 0.45, '', {'v': 'conformity, security', 'clash': 'give_in', 'chance': 0.9}),
    ('move out to a place of your own, with the sums done first', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'leave', 'chance': 0.65}),
    ('spend your evenings with the people at {clash.scene}, who take your plans seriously', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'own_scene', 'chance': 0.75}),
    ('cook a meal for the whole house, and say warmly what you need', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'clash': 'bridge', 'chance': 0.6}),
    ('remind {clash.holder} how this family always did it, and that it worked', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'clash': 'confront', 'chance': 0.5}),
    ("join the residents' committee, where your way of running things is welcome", 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'clash': 'own_scene', 'chance': 0.7}),
    ('write a new list with {clash.ally}, and bring it to the house together', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'bridge', 'chance': 0.55}),
    ('say plainly that their own money stays their own unless that line changes', 'B1', 'G.7', 0.5, '', {'v': 'power, security', 'clash': 'confront', 'chance': 0.45}),
    ('bite your tongue and keep to it, since the rent depends on it', 'R1', 'W.7', 0.5, '', {'v': 'security, conformity', 'clash': 'give_in', 'chance': 0.9}),
    ('move back to the town you grew up in, and think it through there', 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'clash': 'leave', 'chance': 0.6}),
 ]},
{'name': 'the subject that was taken off the timetable',
 'stages': 'juvenile young_adult',
 'age': (11, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'school, family',
 'horizon': 'months',
 'roles': 'parent, sibling, friend, a teacher',
 'clash': 'school',
 'band': 'teen',
 'worlds': {'earth': 'the new timetable puts {N} on the set course, and the subject {N} wanted most is gone from it',
            'tribal': 'the elders have given out the crafts for the year, and {N} is set to learn the wrong one',
            'magic': "the masters have set the year's course of study, and the art {N} hoped to learn is not on it"},
 'timing': {},
 'scenes': {'earth': [('',
                       'The new timetable is up at {clash.setting}, and {N} has been put on the set course. The '
                       'subject {N} wanted most is gone from it, and {clash.holder} says there will be no changes '
                       'this year. A whole year of {Ns} life has just been decided.')],
            'tribal': [('',
                        'The elders have given out the crafts for the year, and {N} has been set to learn the one '
                        'the family always learns. The craft {N} wanted goes to someone else, and {clash.holder} '
                        'says it is settled.')],
            'magic': [('',
                       "The masters of {clash.setting} have set the year's course of study. The art {N} hoped to "
                       'learn is not on it, and {clash.holder} says the course is the same for every student.')]},
 'outcomes': (['The subject comes back, as one lesson a week after school. It is not what {N} wanted, and it is '
               'something.',
               '{N} gets the change, a term late and with a pile of catching up to do.'],
              ['The timetable stays as it is, and {N} spends the year on a course {N} did not choose.',
               'It half works: {clash.holder} agrees to look again next year, and this year is gone.']),
 'options': [
    ('ask through the proper channels to move to the school that teaches it', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'clash': 'leave', 'chance': 0.55}),
    ('teach yourself the subject at the library, with others who want it too', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'own_scene', 'chance': 0.75}),
    ('offer a deal: top marks on the set course, for one class of your choosing', 'B1', None, 0.45, '', {'v': 'achievement, power', 'clash': 'bridge', 'chance': 0.5}),
    ('stand up in assembly and say the timetable is wrong', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'clash': 'confront', 'chance': 0.4}),
    ('take the set course as {sibling} did, and give it a fair chance', 'G1', None, 0.45, '', {'v': 'tradition, security', 'clash': 'give_in', 'chance': 0.9}),
    ('ask {clash.ally} to put your case to {clash.holder}, with your marks to back it', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'clash': 'bridge', 'chance': 0.55}),
    ('bring the numbers: how many asked for the subject, and why it matters', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'confront', 'chance': 0.5}),
    ('take the set course for now, and plan the switch for next year', 'B1', 'G.7', 0.5, '', {'v': 'achievement, security', 'clash': 'give_in', 'chance': 0.85}),
    ('ask {parent} for a year out at sixteen, to work out what you want', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, conformity', 'clash': 'leave', 'chance': 0.5}),
    ('join the after-school nature group, where your questions are welcome', 'G1', 'U.7', 0.5, '', {'v': 'benevolence, self-direction', 'clash': 'own_scene', 'chance': 0.75}),
 ]},
{'name': 'the course that wants it done one way',
 'stages': 'young_adult adult mature elder',
 'age': (18, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'learning, work, money',
 'horizon': 'months',
 'roles': 'a teacher, friend, colleague, partner',
 'clash': 'school',
 'band': 'adult',
 'worlds': {'earth': 'the college course marks every piece of work by the one approved method, and {Ns} own way '
                     'fails',
            'tribal': 'the old teacher of the craft will pass it on only if every step is done exactly the old way',
            'magic': 'the college of mages grades every working by the approved method, and {Ns} own method fails'},
 'timing': {},
 'scenes': {'earth': [('',
                       'At {clash.setting}, {clash.holder} has made it plain: every piece of work is done the one '
                       'approved way and handed in on the set night, or it fails. {N} has another way that works, '
                       'and a job and a life around the classes. The fees are already paid.')],
            'tribal': [('',
                        'The old teacher of the craft has said it twice now: every step the old way, in the old '
                        'order, or not at all. {N} has found a way that works better, and the teaching is the only '
                        'way into the craft.')],
            'magic': [('',
                       'At {clash.setting}, {clash.holder} grades every working by the approved method and no other. '
                       "{Ns} own method works, and fails the mark every time. The year's fees are paid.")]},
 'outcomes': (['One piece of work done {Ns} way is allowed, as a trial. It passes, narrowly, and the rule bends a '
               'little.',
               '{N} gets through the course, with a certificate and a few scars from the argument.'],
              ['The rule holds, and {Ns} best piece of work comes back marked as a fail.',
               'It half works: one mark is changed on appeal, and the rest of the year is done the approved way.']),
 'options': [
    ("join the students' society, and help set its rules", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'clash': 'own_scene', 'chance': 0.75}),
    ('show {clash.holder} your method beside theirs, and ask for a fair trial', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'bridge', 'chance': 0.5}),
    ('tell {clash.holder} straight: mark the work on results, or lose a paying student', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'confront', 'chance': 0.45}),
    ('grit your teeth and do it their way, because the fees are spent', 'R1', None, 0.45, '', {'v': 'self-direction, security', 'clash': 'give_in', 'chance': 0.85}),
    ('drop the course, and give the evenings back to the people at home', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'clash': 'leave', 'chance': 0.75}),
    ('read the course rules closely, and appeal the marks by the book', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'clash': 'confront', 'chance': 0.55}),
    ('do it their way to the letter, and keep your own method for later', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'clash': 'give_in', 'chance': 0.85}),
    ('walk out mid-term and put the time into a project of your own', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'leave', 'chance': 0.65}),
    ('find the crowd at {clash.scene} who learn by doing and argue till late', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'clash': 'own_scene', 'chance': 0.7}),
    ('ask {clash.ally}, who knows both sides, to find a way through for everyone', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'clash': 'bridge', 'chance': 0.6}),
 ]},
{'name': 'the rota at the Saturday job',
 'stages': 'juvenile young_adult',
 'age': (14, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money, friends',
 'horizon': 'months',
 'roles': 'boss, colleague, parent, friend',
 'clash': 'work',
 'band': 'teen',
 'worlds': {'earth': 'the new rota at the Saturday job takes every weekend, and an unpaid half hour to close up',
            'tribal': 'the herder wants {N} with the flock every rest day now, as well as the working days',
            'magic': "the workshop's master wants {N} at the bench every free day, and sweeping up after closing "
                     'too'},
 'timing': {},
 'scenes': {'earth': [('',
                       'The new rota is up at {clash.setting}: {N} now works every Saturday and most Sundays, and '
                       'stays on unpaid to close up. That is how it works now, says {clash.holder}: take it or leave '
                       'it. The money matters, and so does everything else {N} used to do with the weekend.')],
            'tribal': [('',
                        'The herder has told {N} to come with the flock every rest day as well as the working days. '
                        'The share of the herd is good. The rest days were the only days {N} had for anything '
                        'else.')],
            'magic': [('',
                       'The master of {clash.setting} wants {N} at the bench every free day now, and sweeping the '
                       'floor after closing for nothing. The coin is welcome, and the free days were everything '
                       'else.')]},
 'outcomes': (['The Sundays go back to how they were, and the closing half hour is paid. The Saturdays stay.',
               '{N} keeps one free weekend a month, and the pay goes down a little to match.'],
              ['The rota stays as it is, take it or leave it, and {N} is a little less welcome at work.',
               'It half works: the unpaid half hour stops, and every weekend is still taken.']),
 'options': [
    ('ask {clash.ally} to help draw up a fair rota that everyone signs', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'clash': 'bridge', 'chance': 0.6}),
    ('bring {clash.holder} the hours, written down, and the rules on young workers', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'confront', 'chance': 0.55}),
    ('take the extra hours for now, and save the money for something better', 'B1', None, 0.45, '', {'v': 'achievement, security', 'clash': 'give_in', 'chance': 0.85}),
    ('quit on the spot, and take your weekends back', 'R1', None, 0.45, '', {'v': 'stimulation, hedonism', 'clash': 'leave', 'chance': 0.7}),
    ('find weekend work at the farm shop, where the regulars know your name', 'G1', None, 0.45, '', {'v': 'benevolence, security', 'clash': 'own_scene', 'chance': 0.65}),
    ('agree to the rota and learn the work properly, start to finish', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'clash': 'give_in', 'chance': 0.85}),
    ('line up a better job first, then hand in your notice', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'clash': 'leave', 'chance': 0.55}),
    ('start selling what you make at the weekend market, on your own terms', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'own_scene', 'chance': 0.6}),
    ('get the whole crew together and ask {clash.holder}, cheerfully, for a fairer rota', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'clash': 'bridge', 'chance': 0.55}),
    ('speak up for all the young ones on the rota, not just yourself', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, universalism', 'clash': 'confront', 'chance': 0.45}),
 ]},
{'name': 'the new way of working',
 'stages': 'young_adult adult mature',
 'age': (18, 70),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, colleague, partner, friend',
 'clash': 'work',
 'band': 'adult',
 'worlds': {'earth': 'new hours, a new way of doing the job and a target by every name, and {Ns} way of working fits '
                     'none of it',
            'tribal': 'the hunt leader has changed how the hunts are run, and {Ns} way of tracking has no place in '
                      'it',
            'magic': 'the guild master has decreed a new method for every journeyman, and {Ns} own craft does not '
                     'fit it'},
 'timing': {},
 'scenes': {'earth': [('',
                       'From Monday, says {clash.holder}, things at {clash.setting} are done differently: new hours, '
                       'a new way of doing the job, and a target on the board by every name. {Ns} way of doing the '
                       'work, the one {N} is good at, fits none of it. There is rent to pay, and people counting on '
                       'the wage.')],
            'tribal': [('',
                        'The hunt leader has changed how the hunts are run: everyone in one line, at one pace, by '
                        'one plan. {Ns} way of tracking, the one that has fed families for years, has no place in '
                        'it, and the winter is coming.')],
            'magic': [('',
                       'The guild master of {clash.setting} has decreed a new method for every journeyman, from the '
                       "first cut to the last polish. {Ns} own craft does not fit it, and the guild's seal is what "
                       'brings the work in.')]},
 'outcomes': (['The new way stays, with one exception carved out for the part {N} does best. {N} still hates the '
               'board.',
               '{N} lands on their feet, a few months poorer in patience, and the work is good again.'],
              ['Nothing bends. The targets go up on the board, and {Ns} name is near the bottom of it.',
               'It half works: {clash.holder} listens, nods, and changes the hours but not the rest.']),
 'options': [
    ('point out in the staff meeting that the change breaks the agreed terms', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'clash': 'confront', 'chance': 0.5}),
    ('learn the new system inside out, and wait for its flaws to show', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'give_in', 'chance': 0.85}),
    ('take the better offer from across town, and say why on the way out', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'leave', 'chance': 0.6}),
    ('go out after work with the people who do the job the way you do', 'R1', None, 0.45, '', {'v': 'hedonism, stimulation', 'clash': 'own_scene', 'chance': 0.8}),
    ('ask {clash.ally}, who has been here longest, to help find a middle way', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'clash': 'bridge', 'chance': 0.55}),
    ('hand in proper notice, work it out in full, and leave on good terms', 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'clash': 'leave', 'chance': 0.7}),
    ("join the trade's evening meetups, where people swap better ways of doing it", 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'own_scene', 'chance': 0.75}),
    ('propose a trial: your team works your way for a month, results on the table', 'B1', 'G.7', 0.5, '', {'v': 'achievement, security', 'clash': 'bridge', 'chance': 0.5}),
    ('tell {clash.holder}, in front of everyone, that this will wreck the work', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'clash': 'confront', 'chance': 0.4}),
    ('keep your head down and do it their way: people at home rely on the wage', 'G1', 'U.7', 0.5, '', {'v': 'benevolence, security', 'clash': 'give_in', 'chance': 0.9}),
 ]},
{'name': 'the promises at the coming of age',
 'stages': 'juvenile young_adult',
 'age': (11, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'faith, family',
 'horizon': 'months',
 'roles': 'parent, grandparent, friend, elder',
 'clash': 'congregation',
 'band': 'teen',
 'worlds': {'earth': '{N} is to stand up at the coming-of-age gathering and say the promises, and is not sure they '
                     'are true for {N}',
            'tribal': 'the elders expect {N} at the coming-of-age rite, to speak the old vows in front of the whole '
                      'clan',
            'magic': "the temple expects {N} to take the novice's vows at the turning of the year, before the whole "
                     'house'},
 'timing': {},
 'scenes': {'earth': [('',
                       'Next month {N} is to stand up at {clash.setting} and say the promises of the coming of age, '
                       'in front of everyone. The family expects it, and so does {clash.holder}. {N} is not sure the '
                       'words are true for {N}, and saying them would mean something.')],
            'tribal': [('',
                        'At the next full moon {N} is to stand before the whole clan and speak the old vows. The '
                        "family's place in the clan rests on it, and {clash.holder} expects it. {N} is not sure the "
                        'vows are {Ns} own.')],
            'magic': [('',
                       "At the turning of the year {N} is to take the novice's vows before the whole house. {Ns} "
                       'name is already written in the book, in the hand of {clash.holder}. {N} is not sure the vows '
                       'are {Ns} to make.')]},
 'outcomes': (["The day is put off a year, with the family's grudging blessing, and {N} has time to find out what "
               '{N} thinks.',
               '{N} stands up and says the promises in words that are partly {Ns} own, and nobody objects.'],
              ['The day comes as planned. {N} goes through with it, and the doubt is still there afterwards.',
               'It half works: {clash.holder} agrees to wait, and the family talks of little else all summer.']),
 'options': [
    ('stand up and say the promises: the family has done it for generations', 'W1', None, 0.45, '', {'v': 'tradition, conformity', 'clash': 'give_in', 'chance': 0.9}),
    ("ask {parent} for a year's wait, to decide when older", 'U1', None, 0.45, '', {'v': 'self-direction, security', 'clash': 'leave', 'chance': 0.55}),
    ("find the young people's group that debates the big questions, and soon lead it", 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'own_scene', 'chance': 0.7}),
    ('tell {clash.ally} how you feel, all of it, and ask for help', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'clash': 'bridge', 'chance': 0.65}),
    ('tell {clash.holder} the old words deserve someone who means them', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'clash': 'confront', 'chance': 0.5}),
    ('join the volunteers who visit the care home, and serve without the vows', 'W1', 'B.7', 0.5, '', {'v': 'conformity, achievement', 'clash': 'own_scene', 'chance': 0.75}),
    ('ask {clash.holder} the questions you really have, and see if there is room', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'bridge', 'chance': 0.5}),
    ('say you will stand up only if you may say the words your own way', 'B1', 'G.7', 0.5, '', {'v': 'power, tradition', 'clash': 'confront', 'chance': 0.4}),
    ("say the words for the family's sake, though your heart is not in it", 'R1', 'W.7', 0.5, '', {'v': 'security, conformity', 'clash': 'give_in', 'chance': 0.9}),
    ("spend the summer at {grandparent}'s, away from it all, to think it through", 'G1', 'U.7', 0.5, '', {'v': 'tradition, self-direction', 'clash': 'leave', 'chance': 0.6}),
 ]},
{'name': 'what the congregation now expects',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'faith, community, friends',
 'horizon': 'months',
 'roles': 'friend, partner, elder, neighbour',
 'clash': 'congregation',
 'band': 'adult',
 'worlds': {'earth': "two evenings a week for the congregation's work, every gathering, and no open disagreement "
                     'with its decisions',
            'tribal': 'the keeper of the sacred fire asks more of everyone now, and wants no voice raised against '
                      'the old ruling',
            'magic': "the temple's high keeper demands more service of every member, and silence about its rulings"},
 'timing': {},
 'scenes': {'earth': [('',
                       'The word from {clash.holder} to {clash.setting} is plain: from now on, every member at every '
                       "gathering, two evenings a week for the congregation's work, and no open disagreement with "
                       'its decisions. {N} has a family, a job and opinions, and {Ns} friends of twenty years are '
                       'all here.')],
            'tribal': [('',
                        'The keeper of the sacred fire has asked more of everyone: a night a week at the fire, a '
                        'share of every hunt, and no voice raised against the old ruling. {N} has a family to feed '
                        'and a view of the ruling, and every friend {N} has sits at that fire.')],
            'magic': [('',
                       'The high keeper of {clash.setting} has demanded more service of every member, and silence '
                       "about the temple's rulings. {N} has work, a family and doubts about one ruling in "
                       'particular, and the temple is where {Ns} oldest friends are.')]},
 'outcomes': (['The evenings drop to one a week, and the rule on disagreement is quietly forgotten. It cost {N} a '
               'friend or two to get there.',
               '{N} finds a place to stand, inside or outside, and the old friends mostly stay friends.'],
              ['Nothing changes. The new expectations stand, and {N} is watched a little more closely at every '
               'gathering.',
               'It half works: the evenings are eased, and the silence about the decisions is not.']),
 'options': [
    ('write to the members, and resign your place properly', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'clash': 'leave', 'chance': 0.75}),
    ('look for a reading group that asks the old questions freely', 'U1', None, 0.45, '', {'v': 'self-direction, universalism', 'clash': 'own_scene', 'chance': 0.7}),
    ('broker a deal with {clash.holder}: fewer evenings, and a seat on the working group', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'bridge', 'chance': 0.5}),
    ('stand up at the next gathering and say what many are thinking', 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'clash': 'confront', 'chance': 0.45}),
    ('give the evenings gladly: these are your people, and the work matters', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'clash': 'give_in', 'chance': 0.9}),
    ('ask {clash.ally} to bring both sides to one meeting, with an agreed agenda', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'clash': 'bridge', 'chance': 0.55}),
    ('put the figures before the members: what is asked, what it costs, who decided', 'U1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'clash': 'confront', 'chance': 0.45}),
    ('go along with it for now, and win a seat where decisions get made', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'give_in', 'chance': 0.75}),
    ('stop going, and give those mornings to the hills and the people you love', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, benevolence', 'clash': 'leave', 'chance': 0.8}),
    ('join the smaller congregation across town, where things are done the gentler way', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'clash': 'own_scene', 'chance': 0.7}),
 ]},
{'name': 'the hall the town is closing',
 'stages': 'juvenile young_adult',
 'age': (12, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, friends',
 'horizon': 'months',
 'roles': 'friend, parent, neighbour, grandparent',
 'clash': 'town',
 'band': 'teen',
 'worlds': {'earth': 'the town is selling the old youth hall, and groups of young people in the square are to be '
                     'moved on',
            'tribal': "the elders have given the young people's clearing to the herds, and the young are to keep to "
                      'the camp',
            'magic': 'the council has sealed the old meeting hall, and the young are not to gather in the square '
                     'after dusk'},
 'timing': {},
 'scenes': {'earth': [('',
                       'The old youth hall is to be sold, by a vote of {clash.holder}, and from next month there is '
                       'nowhere in {clash.setting} for {Ns} age to go in the evenings. A new rule says groups of '
                       'young people in the square will be moved on. Everyone {N} knows is talking about it.')],
            'tribal': [('',
                        "The elders have given the young people's clearing to the herds, and the young are to keep "
                        "to the camp. There is nowhere left for {Ns} age to be together, away from the grown ones' "
                        'eyes.')],
            'magic': [('',
                       'The council of {clash.setting} has sealed the old meeting hall with a ward, and the young '
                       'are not to gather in the square after dusk. Everyone {N} knows is talking about it.')]},
 'outcomes': (['The hall is sold, and one room of it stays for the young on two evenings a week. It is smaller, and '
               'it is theirs.',
               'The council puts off the sale a year, and {N} finds that grown-ups can be moved, slowly.'],
              ['The hall is sold as planned, and the square is emptied every evening.',
               'It half works: the moving-on rule is dropped, and there is still nowhere to go.']),
 'options': [
    ('help start a youth club that meets in the school hall each week', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'clash': 'own_scene', 'chance': 0.65}),
    ('draw up a plan that keeps part of the hall, and take it to {clash.ally}', 'U1', None, 0.45, '', {'v': 'self-direction, universalism', 'clash': 'bridge', 'chance': 0.5}),
    ('go to the council meeting and demand somewhere better in return', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'confront', 'chance': 0.4}),
    ('keep within the new rules, grumbling, because there is no other choice yet', 'R1', None, 0.45, '', {'v': 'hedonism, security', 'clash': 'give_in', 'chance': 0.9}),
    ("spend the summer at {grandparent}'s, out where there is room to be young", 'G1', None, 0.45, '', {'v': 'tradition, security', 'clash': 'leave', 'chance': 0.6}),
    ('collect signatures, read up on the rules, and petition the council properly', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'clash': 'confront', 'chance': 0.5}),
    ('keep to the rules, and quietly learn how the council makes its decisions', 'U1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'clash': 'give_in', 'chance': 0.85}),
    ("make the next town's hall your own, by bus each weekend", 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'leave', 'chance': 0.65}),
    ('take your friends to the open fields at the edge of town on summer days', 'R1', 'G.7', 0.5, '', {'v': 'stimulation, benevolence', 'clash': 'own_scene', 'chance': 0.75}),
    ('get the old neighbours and the young ones round one table, with {clash.ally} chairing', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, conformity', 'clash': 'bridge', 'chance': 0.55}),
 ]},
{'name': 'the plan for the town',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'community, home, neighbours',
 'horizon': 'years',
 'roles': 'neighbour, friend, partner, rival',
 'clash': 'town',
 'band': 'adult',
 'worlds': {'earth': "the town's new plan builds over the common, moves the street market, and sets new rules on "
                     'what may be done at home',
            'tribal': "the clan's council has chosen to move camp across the river, away from the place {N} has made "
                      'home',
            'magic': 'the council has granted the old common to a builder-mage, and new rules come with the towers'},
 'timing': {},
 'scenes': {'earth': [('',
                       'A plan for {clash.setting} has been passed by {clash.holder}: the common by {Ns} street will '
                       "be built over, the street market moved, and new rules set on what may be done in one's own "
                       'front yard. {N} has lived here for years, and the plan runs straight through the part of '
                       'town {N} cares about.')],
            'tribal': [('',
                        "The clan's council has chosen to move camp across the river when the snows end. The new "
                        'ground is better for the herds and worse for everything {N} has built here, and the choice '
                        'has been made.')],
            'magic': [('',
                       'The council of {clash.setting} has granted the old common to a builder-mage. Towers will '
                       "rise where the market stood, and new rules come with them on what may be done on one's own "
                       'doorstep.')]},
 'outcomes': (['The plan goes ahead with half the common kept, after a year of meetings. {N} knows every name on the '
               'council now.',
               '{N} finds a way to live with the new town, and some of it turns out better than feared.'],
              ['The plan goes ahead as passed, and the common is fenced off by the spring.',
               'It half works: the market stays where it was, and the common is built over anyway.']),
 'options': [
    ('propose, through the proper channels, a smaller plan both sides could accept', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'clash': 'bridge', 'chance': 0.5}),
    ('read every page of the plan, and show the council where its numbers fail', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'confront', 'chance': 0.55}),
    ('accept the plan, and get in early on whatever it brings', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'give_in', 'chance': 0.75}),
    ('pack up and move somewhere with more life and fewer rules', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'clash': 'leave', 'chance': 0.7}),
    ('join the neighbours keeping the allotments the plan left alone', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'clash': 'own_scene', 'chance': 0.75}),
    ('follow the new rules to the letter, since the fines would ruin you', 'W1', 'B.7', 0.5, '', {'v': 'conformity, security', 'clash': 'give_in', 'chance': 0.9}),
    ('find the town that suits you best, visit it twice, then move', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'leave', 'chance': 0.65}),
    ("make your street's residents' group the one the council listens to", 'B1', 'G.7', 0.5, '', {'v': 'power, benevolence', 'clash': 'own_scene', 'chance': 0.6}),
    ('throw a street party, and invite the whole council to it', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, conformity', 'clash': 'bridge', 'chance': 0.55}),
    ('speak at the hearing for the families and the wildlife that use the common', 'G1', 'U.7', 0.5, '', {'v': 'universalism, self-direction', 'clash': 'confront', 'chance': 0.45}),
 ]},
{'name': "the club's new terms",
 'stages': 'juvenile young_adult',
 'age': (10, 19),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'friends, play',
 'horizon': 'months',
 'roles': 'friend, parent, rival, mentor',
 'clash': 'group',
 'band': 'teen',
 'worlds': {'earth': 'the club wants three practices a week, everything done the one way, and anyone who misses two '
                     'is out',
            'tribal': 'the leader of the young hunters wants every youth at every practice, done the one way, or out',
            'magic': "the apprentice circle's leader wants every evening and every working done the one way, or out"},
 'timing': {},
 'scenes': {'earth': [('',
                       'New terms have come from {clash.holder} for everyone in {clash.setting}: three practices a '
                       'week, everything done the one way, and anyone who misses two is out. {N} has been part of it '
                       'for years and {Ns} friends are all there, but the new terms leave no room for anything '
                       'else.')],
            'tribal': [('',
                        'The leader of the young hunters wants every youth at every practice, at dawn, every move '
                        'made the one way, or out. {Ns} friends are all among the young hunters, and the practices '
                        'take every free day.')],
            'magic': [('',
                       'The leader of the apprentice circle wants every evening, every working done the one way, and '
                       'any who miss two are out. {Ns} friends are all in the circle, and the evenings were all {N} '
                       'had.')]},
 'outcomes': (['The terms soften to two practices and one warning. Nobody says who won, and {N} is still in.',
               '{N} finds a place that fits, and keeps most of the old friends on the way.'],
              ['The terms stand, and {N} misses two practices before the month is out.',
               'It half works: the club agrees to a vote next season, and this season runs by the new terms.']),
 'options': [
    ("point out that the club's own rules say changes need a members' vote", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'clash': 'confront', 'chance': 0.5}),
    ('keep to the new terms for a season, and see what you learn', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'give_in', 'chance': 0.85}),
    ('quit, and take what you are good at to the other club that wants you', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'leave', 'chance': 0.65}),
    ('start something of your own with the others who feel the same', 'R1', None, 0.45, '', {'v': 'stimulation, self-direction', 'clash': 'own_scene', 'chance': 0.7}),
    ('ask {clash.ally} to speak for the old members and the new ones together', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'clash': 'bridge', 'chance': 0.55}),
    ('leave at the end of the season, properly, with your place handed on', 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'clash': 'leave', 'chance': 0.75}),
    ('find the open sessions at {clash.scene}, where you can try things your way', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'clash': 'own_scene', 'chance': 0.75}),
    ('offer {clash.holder} a deal: two practices, and you bring in two new members', 'B1', 'G.7', 0.5, '', {'v': 'power, security', 'clash': 'bridge', 'chance': 0.55}),
    ('tell {clash.holder}, in front of the whole club, that the new terms are unfair', 'R1', 'W.7', 0.5, '', {'v': 'stimulation, universalism', 'clash': 'confront', 'chance': 0.4}),
    ("go along with it for your friends' sake: the club is them", 'G1', 'U.7', 0.5, '', {'v': 'benevolence, self-direction', 'clash': 'give_in', 'chance': 0.9}),
 ]},
{'name': "the club's new direction",
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
 'drivers': '',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'friends, leisure, community',
 'horizon': 'months',
 'roles': 'friend, rival, regular, colleague',
 'clash': 'group',
 'band': 'adult',
 'worlds': {'earth': 'the club has taken money from a big backer, and with it a new name, new rules and the old '
                     'members asked to make way',
            'tribal': "the band's leader has made a pact with a stronger band, and the band's old ways must give way "
                      'to theirs',
            'magic': "the circle's chair has taken a patron's gold, and the patron's rules come with it"},
 'timing': {},
 'scenes': {'earth': [('',
                       'The news from {clash.holder} is that {clash.setting} will take money from a big backer, and '
                       'with it come a new name, new rules on how things are run, and the old members asked to make '
                       'way. {N} has given years to it, and the vote is next week.')],
            'tribal': [('',
                        "The band's leader has made a pact with a stronger band across the hills. Their ways come "
                        'with the pact: who leads, who hunts, who sits where. {N} has given years to this band.')],
            'magic': [('',
                       "The chair of {clash.setting} has taken a patron's gold, and the patron's rules come with it: "
                       'a new name, new workings, and the old members asked to make way. {N} has given years to the '
                       'circle.')]},
 'outcomes': (["The backer's money comes in with the old name kept, after a long night of arguing. Some members "
               'leave anyway.',
               '{N} ends up somewhere that feels like the club used to, and misses the old one less than expected.'],
              ['The vote goes through as announced, and the old members are thanked and shown the door.',
               'It half works: the old name stays, and nearly everything else changes.']),
 'options': [
    ('accept the vote: it was done by the rules, and the group decided', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'clash': 'give_in', 'chance': 0.9}),
    ('resign, and put the time into studying what you used to do there', 'U1', None, 0.45, '', {'v': 'self-direction, achievement', 'clash': 'leave', 'chance': 0.75}),
    ('set up a new group of your own, run your way, and invite the best', 'B1', None, 0.45, '', {'v': 'power, achievement', 'clash': 'own_scene', 'chance': 0.6}),
    ('throw an evening for old and new members alike, and get them talking', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'clash': 'bridge', 'chance': 0.6}),
    ('speak for the founding members at the meeting: this was theirs first', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'clash': 'confront', 'chance': 0.5}),
    ('join the older society in the next town, which keeps the old standards', 'W1', 'U.7', 0.5, '', {'v': 'conformity, self-direction', 'clash': 'own_scene', 'chance': 0.7}),
    ('work out with {clash.ally} a split both sides can sign: old name, new money', 'U1', 'B.7', 0.5, '', {'v': 'self-direction, power', 'clash': 'bridge', 'chance': 0.5}),
    ('tell {clash.holder} the members will leave too unless the terms change', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'clash': 'confront', 'chance': 0.45}),
    ('stay for the friends there, since leaving would cost you all of them', 'R1', 'G.7', 0.5, '', {'v': 'hedonism, benevolence', 'clash': 'give_in', 'chance': 0.85}),
    ('step away quietly, and give your evenings back to your family', 'G1', 'W.7', 0.5, '', {'v': 'benevolence, security', 'clash': 'leave', 'chance': 0.75}),
 ]},
]

ECHOES = [
]

EVENTS_READ = []

MARKS = {}
