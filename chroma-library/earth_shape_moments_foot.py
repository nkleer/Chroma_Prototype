# Footprints (plan.md workstream 3; Engine 10-19): what each option visibly leaves, compiled by build.py from the
# foot: fields of the .lib parts. FOOT[(moment, option label)] = [(kind, value), ...]; kinds person, place, means,
# mark, door, lesson. Read only with the engine's foot_on switch; earth.py carries none of it.
FOOT = {('the ordinary weeknight at {aim.place}', 'take the dullest job on the list and have it done by the next meeting'): [('mark',
                                                                                                                       'kept '
                                                                                                                       'your '
                                                                                                                       'word')],
 ('the ordinary weeknight at {aim.place}', 'read up on how others have gone about {aim.thing} before saying a word'): [('lesson',
                                                                                                                        'others '
                                                                                                                        'have '
                                                                                                                        'tried '
                                                                                                                        'this '
                                                                                                                        'before')],
 ('the ordinary weeknight at {aim.place}', 'offer to speak for the group next time, so people learn your name'): [('means',
                                                                                                                   'ties+.03')],
 ('the ordinary weeknight at {aim.place}', 'stay on after the meeting arguing about what the group should really do'): [('person',
                                                                                                                         'friend')],
 ('the ordinary weeknight at {aim.place}', 'come when the week allows, and keep the other evenings for home'): [('means',
                                                                                                                 'time+.03')],
 ('the ordinary weeknight at {aim.place}', 'write down who does what, so nothing falls through the cracks'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the ordinary weeknight at {aim.place}', 'work out which job would actually change something, and take that one'): [('lesson',
                                                                                                                       'the '
                                                                                                                       'right '
                                                                                                                       'job '
                                                                                                                       'beats '
                                                                                                                       'more '
                                                                                                                       'jobs')],
 ('the ordinary weeknight at {aim.place}', 'skip the list and start something of your own that the group can join'): [('mark',
                                                                                                                       'took '
                                                                                                                       'a '
                                                                                                                       'wild '
                                                                                                                       'risk')],
 ('the ordinary weeknight at {aim.place}', 'leave the jobs for tonight and just get to know the people in the room'): [('means',
                                                                                                                        'ties+.04')],
 ('the ordinary weeknight at {aim.place}', 'do the jobs nobody sees, and turn up again next week the same'): [('person',
                                                                                                               'regular')],
 ('the week that {aim.doing} takes every evening', 'keep to the plan the group agreed, one task at a time, however long it takes'): [('mark',
                                                                                                                                      'kept '
                                                                                                                                      'your '
                                                                                                                                      'word')],
 ('the week that {aim.doing} takes every evening', 'rework the plan so it needs fewer evenings from fewer people'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the week that {aim.doing} takes every evening', 'hand the small jobs to others and keep only the calls that matter'): [('person',
                                                                                                                           'patron')],
 ('the week that {aim.doing} takes every evening', 'throw every evening at it this week and sleep when it is done'): [('means',
                                                                                                                       'health-.04')],
 ('the week that {aim.doing} takes every evening', 'keep two evenings free for home, whatever the week brings'): [('means',
                                                                                                                   'ties+.04')],
 ('the week that {aim.doing} takes every evening', 'ask the group to name a deputy, and train them properly'): [('person',
                                                                                                                 'colleague')],
 ('the week that {aim.doing} takes every evening', 'try a new way of reaching people that nobody here has tried'): [('mark',
                                                                                                                     'took '
                                                                                                                     'a '
                                                                                                                     'wild '
                                                                                                                     'risk')],
 ('the week that {aim.doing} takes every evening', 'take the lead in public, and let the old hands run things quietly'): [('person',
                                                                                                                           'elder')],
 ('the week that {aim.doing} takes every evening', 'promise the group the hardest part of the plan, and do it in the open'): [('door',
                                                                                                                               'kept '
                                                                                                                               'your '
                                                                                                                               'word')],
 ('the week that {aim.doing} takes every evening', 'step back for a month and watch how the group manages alone'): [('lesson',
                                                                                                                     'the '
                                                                                                                     'work '
                                                                                                                     'goes '
                                                                                                                     'on '
                                                                                                                     'without '
                                                                                                                     'you')],
 ('three minutes to speak at {aim.contest}', 'put your name on the list and speak to the facts the group agreed'): [('place',
                                                                                                                     'rule.voice')],
 ('three minutes to speak at {aim.contest}', 'prepare one clear point and the figures behind it, and time it to the second'): [('mark',
                                                                                                                                'learned '
                                                                                                                                'a '
                                                                                                                                'skill')],
 ('three minutes to speak at {aim.contest}', 'ask to speak last, so this is the point the room remembers'): [('person',
                                                                                                              'rival')],
 ('three minutes to speak at {aim.contest}', 'speak from the heart about why it matters, notes or no notes'): [('mark',
                                                                                                                'took '
                                                                                                                'a '
                                                                                                                'wild '
                                                                                                                'risk')],
 ('three minutes to speak at {aim.contest}', 'let an older member speak this time, and stand beside them while they do'): [('person',
                                                                                                                            'elder')],
 ('three minutes to speak at {aim.contest}', 'sit in the front row and take careful notes for the group'): [('lesson',
                                                                                                             'see '
                                                                                                             'how it '
                                                                                                             'is '
                                                                                                             'done '
                                                                                                             'first')],
 ('three minutes to speak at {aim.contest}', 'help the main speaker sharpen their words, and let them take the floor'): [('person',
                                                                                                                          'colleague')],
 ('three minutes to speak at {aim.contest}', 'ask the hardest question of the evening from the back of the room'): [('mark',
                                                                                                                     'defied '
                                                                                                                     'an '
                                                                                                                     'authority')],
 ('three minutes to speak at {aim.contest}', 'bring the whole street along so the room is full of faces'): [('means',
                                                                                                             'ties+.05')],
 ('three minutes to speak at {aim.contest}', 'stay home this time and help the group write its next letter'): [('lesson',
                                                                                                                'the '
                                                                                                                'speaking '
                                                                                                                'rests '
                                                                                                                'on '
                                                                                                                'quiet '
                                                                                                                'work')],
 ('the day {aim.contest} settles it', 'go through the proper channels to the last form, and let the case speak'): [('mark',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ('the day {aim.contest} settles it', 'spend the week answering every point the other side could raise'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ('the day {aim.contest} settles it', 'meet the undecided ones one by one before the day'): [('person',
                                                                                              'go-between')],
 ('the day {aim.contest} settles it', 'gather everyone who cares outside on the day, peacefully, to be seen and heard'): [('place',
                                                                                                                           'gather.great')],
 ('the day {aim.contest} settles it', 'ask the people the decision touches to tell it in their own words'): [('person',
                                                                                                              'neighbour')],
 ('the day {aim.contest} settles it', "agree a fair compromise in advance with the other side's leaders"): [('door',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the day {aim.contest} settles it', 'say out loud the one thing everyone has been too careful to say'): [('mark',
                                                                                                            'defied '
                                                                                                            'an '
                                                                                                            'authority')],
 ('the day {aim.contest} settles it', 'let the oldest names in town carry it, and stand where they can see you'): [('person',
                                                                                                                    'elder')],
 ('the day {aim.contest} settles it', 'step aside so a newer voice can take this one, and back them all the way'): [('person',
                                                                                                                     'friend')],
 ('the day {aim.contest} settles it', 'hold back this round, and gather what you learn for the next one'): [('lesson',
                                                                                                             'the '
                                                                                                             'right '
                                                                                                             'time '
                                                                                                             'matters')],
 ('the one who has done this for thirty years', 'do exactly what they say for a full year before questioning any of it'): [('person',
                                                                                                                            'mentor')],
 ('the one who has done this for thirty years', 'ask about every case they lost, and what they would do differently'): [('lesson',
                                                                                                                         'the '
                                                                                                                         'losses '
                                                                                                                         'teach '
                                                                                                                         'the '
                                                                                                                         'most')],
 ('the one who has done this for thirty years', 'let them open the doors they know, and remember who stands behind each'): [('person',
                                                                                                                             'patron')],
 ('the one who has done this for thirty years', 'take what fits and argue with the rest, out loud'): [('mark',
                                                                                                       'defied an '
                                                                                                       'authority')],
 ('the one who has done this for thirty years', 'spend time with them away from the work, and let the teaching come slowly'): [('person',
                                                                                                                                'elder')],
 ('the one who has done this for thirty years', 'write down what they teach, so it can be passed on'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the one who has done this for thirty years', 'learn how they read a room, and use it at the next meeting'): [('means',
                                                                                                                 'ties+.04')],
 ('the one who has done this for thirty years', 'ask them to put you in front of the people who decide, now'): [('mark',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ('the one who has done this for thirty years', 'follow them on their rounds and simply listen to the people they meet'): [('person',
                                                                                                                            'neighbour')],
 ('the one who has done this for thirty years', 'thank them, and keep to the slower pace your own life allows'): [('lesson',
                                                                                                                   'a '
                                                                                                                   'good '
                                                                                                                   'teacher '
                                                                                                                   'can '
                                                                                                                   'wait')],
 ('the other group knocking on the same doors', 'propose one shared plan, with clear rules on who does what'): [('door',
                                                                                                                 'kept '
                                                                                                                 'your '
                                                                                                                 'word')],
 ('the other group knocking on the same doors', 'study what they do better, and borrow it openly'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the other group knocking on the same doors', 'outwork them until people come to your door first'): [('person',
                                                                                                        'rival')],
 ('the other group knocking on the same doors', 'challenge them to a public debate about whose way works'): [('place',
                                                                                                              'gather.talk')],
 ('the other group knocking on the same doors', 'leave them the streets they already know, and keep to the old patch'): [('lesson',
                                                                                                                          'there '
                                                                                                                          'is '
                                                                                                                          'room '
                                                                                                                          'for '
                                                                                                                          'both')],
 ('the other group knocking on the same doors', 'meet them in private and agree to split the work fairly'): [('person',
                                                                                                              'go-between')],
 ('the other group knocking on the same doors', 'try the bold thing they keep talking about, before they do'): [('mark',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ('the other group knocking on the same doors', 'win over their oldest supporters, one by one'): [('person',
                                                                                                   'regular')],
 ('the other group knocking on the same doors', 'say publicly what they get right, and mean it'): [('means',
                                                                                                    'ties+.04')],
 ('the other group knocking on the same doors', 'invite them round, and find the one thing you both want most'): [('person',
                                                                                                                   'friend')],
 ('the year it all went the other way', 'go back to the next meeting as if nothing has changed'): [('mark',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('the year it all went the other way', 'sit down and work out, honestly, why it went the way it did'): [('lesson',
                                                                                                          'a loss '
                                                                                                          'shows '
                                                                                                          'where to '
                                                                                                          'look')],
 ('the year it all went the other way', 'find out who blocked it, and plan how to get past them next time'): [('person',
                                                                                                               'rival')],
 ('the year it all went the other way', 'be angry for a week, then start again louder'): [('means', 'health-.03')],
 ('the year it all went the other way', 'let it go, and keep the friends you made along the way'): [('person',
                                                                                                     'friend')],
 ('the year it all went the other way', 'keep the records safe, so whoever comes next can pick it up'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the year it all went the other way', 'turn what you learned into advice that others will pay to hear'): [('means',
                                                                                                             'money+.04')],
 ('the year it all went the other way', 'put on something nobody can ignore, peacefully, within the week'): [('mark',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ('the year it all went the other way', 'turn to other things for a month, then come back to it'): [('lesson',
                                                                                                     'rest is part '
                                                                                                     'of the work')],
 ('the year it all went the other way', 'thank the neighbours who stayed, and close this chapter for good'): [('person',
                                                                                                               'neighbour')],
 ('the same faces, the same answer', 'sign up for another year and keep every promise you made'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('the same faces, the same answer', 'change how you do it: new people, new ways in, one fresh plan'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the same faces, the same answer', 'stay on only if you lead the next stage, and say so plainly'): [('person',
                                                                                                       'rival')],
 ('the same faces, the same answer', 'give it one more burst, everything at once, and see what breaks loose'): [('mark',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ('the same faces, the same answer', 'step back to the edge for a year, and help when asked'): [('means',
                                                                                                 'time+.05')],
 ('the same faces, the same answer', 'hand over the running of it, and keep one seat at the table'): [('person',
                                                                                                       'colleague')],
 ('the same faces, the same answer', 'put on something public and joyful for it, where the dull meetings were'): [('place',
                                                                                                                   'gather.great')],
 ('the same faces, the same answer', 'let it go, and keep the people who will still answer your calls'): [('person',
                                                                                                           'friend')],
 ('the same faces, the same answer', 'say it plainly at the meeting: you are done, and here is what you learned'): [('lesson',
                                                                                                                     'knowing '
                                                                                                                     'when '
                                                                                                                     'to '
                                                                                                                     'stop')],
 ('the same faces, the same answer', 'slow down, and spend the year learning how others broke through'): [('lesson',
                                                                                                           'slow '
                                                                                                           'years '
                                                                                                           'can '
                                                                                                           'still '
                                                                                                           'teach')],
 ('what {aim.doing} is costing at home', 'pay your fair share from the budget agreed at home, and no more'): [('means',
                                                                                                               'money-.04')],
 ('what {aim.doing} is costing at home', 'find a cheaper way to the same step, and go on without the big spend'): [('mark',
                                                                                                                    'learned '
                                                                                                                    'a '
                                                                                                                    'skill')],
 ('what {aim.doing} is costing at home', 'ask the people who gain most to pay, and make it worth their while'): [('person',
                                                                                                                  'patron')],
 ('what {aim.doing} is costing at home', 'put everything into it now: savings, evenings, the lot'): [('means',
                                                                                                      'money-.10')],
 ('what {aim.doing} is costing at home', 'put home first, and hand {aim.thing} to someone with more to spare'): [('lesson',
                                                                                                                  'home '
                                                                                                                  'was '
                                                                                                                  'paying '
                                                                                                                  'all '
                                                                                                                  'along')],
 ('what {aim.doing} is costing at home', 'wait a year, save for it properly, then go on'): [('door',
                                                                                             'kept your word')],
 ('what {aim.doing} is costing at home', 'trade your know-how for the hall and the printing instead of money'): [('person',
                                                                                                                  'go-between')],
 ('what {aim.doing} is costing at home', 'borrow to cover it, and trust the step to pay it back'): [('door',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('what {aim.doing} is costing at home', 'sit down with the family, say what it means, and ask for their help'): [('means',
                                                                                                                   'ties+.03')],
 ('what {aim.doing} is costing at home', 'step away for good, and teach the next one all you know'): [('lesson',
                                                                                                       'passing it '
                                                                                                       'on keeps it '
                                                                                                       'going')],
 ('the seat that has just come free', 'accept, and keep the rules of the seat to the letter'): [('place',
                                                                                                 'rule.counsel')],
 ('the seat that has just come free', 'ask for the terms in writing, weigh them, then accept'): [('person',
                                                                                                  'colleague')],
 ('the seat that has just come free', 'take it, and use it to push {aim.thing} further than anyone expects'): [('person',
                                                                                                                'patron')],
 ('the seat that has just come free', 'turn it down, so you can keep saying what you really think'): [('mark',
                                                                                                       'turned down '
                                                                                                       'a chance')],
 ('the seat that has just come free', 'say not yet: the household needs the time more this year'): [('door',
                                                                                                     'turned down a '
                                                                                                     'chance')],
 ('the seat that has just come free', 'take it on condition the group gets a say in what you do there'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the seat that has just come free', 'take it, and change how the seat itself works'): [('mark',
                                                                                          'defied an authority')],
 ('the seat that has just come free', 'take it, and bring the old hands in as advisers'): [('person', 'elder')],
 ('the seat that has just come free', 'step back from {aim.thing} altogether, and keep the friends you made in it'): [('person',
                                                                                                                       'friend')],
 ('the seat that has just come free', 'let this road go, and give your time to learning something new'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the door that will not open here', 'go through {aim.round} properly, with a letter of introduction'): [('person',
                                                                                                           'patron')],
 ('the door that will not open here', 'look into {aim.round} carefully first, and go in knowing how it works'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('the door that will not open here', 'go round, and make sure the ones who blocked the way hear how it went'): [('person',
                                                                                                                  'rival')],
 ('the door that will not open here', 'stop waiting and start through {aim.round} this week'): [('mark',
                                                                                                 'took a wild risk')],
 ('the door that will not open here', 'let it rest, and keep the people you met on the way'): [('person', 'friend')],
 ('the door that will not open here', 'ask the ones in the way what would change their mind, then go round'): [('person',
                                                                                                                'go-between')],
 ('the door that will not open here', 'find someone inside {aim.round} who owes a favour'): [('person', 'colleague')],
 ('the door that will not open here', 'go round loudly, and dare the old way to keep up'): [('mark',
                                                                                             'defied an authority')],
 ('the door that will not open here', 'take a season off, then try {aim.round} when the family has room for it'): [('means',
                                                                                                                    'time+.04')],
 ('the door that will not open here', 'give it up here, and pass what you know to whoever comes next'): [('lesson',
                                                                                                          'a shut '
                                                                                                          'door ends '
                                                                                                          'nothing')],
 ('what the family makes of {aim.doing}', 'keep going, and keep every promise you make at home as well'): [('mark',
                                                                                                            'kept '
                                                                                                            'your '
                                                                                                            'word')],
 ('what the family makes of {aim.doing}', 'explain what {aim.thing} is really about, with facts, and keep going'): [('lesson',
                                                                                                                     'saying '
                                                                                                                     'it '
                                                                                                                     'plainly '
                                                                                                                     'helps')],
 ('what the family makes of {aim.doing}', "keep at it, and stop asking for anyone's blessing"): [('mark',
                                                                                                  'defied an '
                                                                                                  'authority')],
 ('what the family makes of {aim.doing}', 'bring the family to see it for themselves, once'): [('means', 'ties+.04')],
 ('what the family makes of {aim.doing}', 'cut back to what the family can live with'): [('means', 'ties+.05')],
 ('what the family makes of {aim.doing}', 'agree a set number of evenings with them, and hold to it'): [('door',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('what the family makes of {aim.doing}', "let the family's worry change how you do it, not whether"): [('lesson',
                                                                                                         'worry can '
                                                                                                         'carry good '
                                                                                                         'sense')],
 ('what the family makes of {aim.doing}', 'keep going, and ask an older relative to put in a word at home'): [('person',
                                                                                                               'go-between')],
 ('what the family makes of {aim.doing}', 'give way for now, because the rows at home have become too much'): [('mark',
                                                                                                                'gave '
                                                                                                                'in '
                                                                                                                'to '
                                                                                                                'pressure')],
 ('what the family makes of {aim.doing}', 'take a quieter part for now, and learn what you can from the edge'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('{aim.rung}, and the proof is plain', 'thank everyone who helped, by name, at the next meeting'): [('means',
                                                                                                      'ties+.04')],
 ('{aim.rung}, and the proof is plain', 'write down what worked, so the next step starts from it'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('{aim.rung}, and the proof is plain', 'let it be known around town, and use it to open the next door'): [('person',
                                                                                                            'patron')],
 ('{aim.rung}, and the proof is plain', 'celebrate loudly with everyone who stood alongside'): [('person', 'friend')],
 ('{aim.rung}, and the proof is plain', 'tell the family first, quietly, at home'): [('lesson',
                                                                                      'home is where it lands')],
 ('{aim.rung}, and the proof is plain', 'go straight back to work on {aim.next} the next morning'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('{aim.rung}, and the proof is plain', 'quietly ask what this new standing makes it possible to change'): [('lesson',
                                                                                                             'standing '
                                                                                                             'is a '
                                                                                                             'tool')],
 ('{aim.rung}, and the proof is plain', 'take the floor at the celebration and speak about what comes next'): [('place',
                                                                                                                'gather.great')],
 ('{aim.rung}, and the proof is plain', 'take the whole group out of town for a day off'): [('means', 'health+.03')],
 ('{aim.rung}, and the proof is plain', 'mark it with the old customs your family keeps for such days'): [('person',
                                                                                                           'elder')],
 ('the quiet hour of {aim.doing}', 'keep the hour exactly as it is meant to be kept, sign or no sign'): [('mark',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('the quiet hour of {aim.doing}', 'write down each week what the hour brings, even when it is nothing'): [('lesson',
                                                                                                            'nothing '
                                                                                                            'is also '
                                                                                                            'an '
                                                                                                            'answer')],
 ('the quiet hour of {aim.doing}', 'set a harder discipline, and hold to it'): [('mark', 'learned a skill')],
 ('the quiet hour of {aim.doing}', 'let the hour go where it wants: music, walking, a sudden question'): [('means',
                                                                                                           'freedom+.03')],
 ('the quiet hour of {aim.doing}', 'keep it shorter, and keep it with {friend}'): [('person', 'friend')],
 ('the quiet hour of {aim.doing}', 'take a small duty for the hour, so it has a purpose beyond you'): [('door',
                                                                                                        'kept your '
                                                                                                        'word')],
 ('the quiet hour of {aim.doing}', 'spend the hour with writing from far outside what you know'): [('place',
                                                                                                    'learn.keeping')],
 ('the quiet hour of {aim.doing}', 'go early, before the others, and have the place alone'): [('means', 'time-.03')],
 ('the quiet hour of {aim.doing}', 'sing during the hour, even if only under the breath'): [('lesson',
                                                                                             'a voice fills an empty '
                                                                                             'hour')],
 ('the quiet hour of {aim.doing}', 'take the hour outdoors, and see whether it means more there'): [('place',
                                                                                                     'prod.wild')],
 ('the people who come to {N} now', 'keep to the set teaching, and see each person in turn'): [('means', 'time-.04')],
 ('the people who come to {N} now', 'answer the hardest question properly, even if the others must wait'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('the people who come to {N} now', 'start a proper class at set times, with your name on it'): [('place',
                                                                                                  'gather.talk')],
 ('the people who come to {N} now', 'drop the plan and talk with whoever needs it most today'): [('mark',
                                                                                                  'helped someone in '
                                                                                                  'need')],
 ('the people who come to {N} now', 'send them home kindly, and keep this evening for your own quiet'): [('lesson',
                                                                                                          'the '
                                                                                                          'teacher '
                                                                                                          'needs '
                                                                                                          'keeping '
                                                                                                          'too')],
 ('the people who come to {N} now', 'write down the answers you keep giving, for others to use'): [('person',
                                                                                                    'regular')],
 ('the people who come to {N} now', 'train one of them to take the beginners, and keep the hard cases'): [('person',
                                                                                                           'colleague')],
 ('the people who come to {N} now', 'fill the hall for one open evening instead of three small ones'): [('place',
                                                                                                         'gather.hall')],
 ('the people who come to {N} now', 'take them walking, and talk where the light is good'): [('place', 'prod.wild')],
 ('the people who come to {N} now', 'ask {aim.person} to share the load, as the old ones did'): [('person', 'elder')],
 ('the first rite of {aim.contest}', 'prepare the way the rite asks, and take part in full'): [('mark',
                                                                                                'kept your word')],
 ('the first rite of {aim.contest}', 'find out what the rite is for, then take part knowing why'): [('lesson',
                                                                                                     'knowing why '
                                                                                                     'changes it')],
 ('the first rite of {aim.contest}', 'take part, and keep it more strictly than anyone else there'): [('person',
                                                                                                       'rival')],
 ('the first rite of {aim.contest}', 'go in with no plan, and let it be what it is'): [('mark', 'took a wild risk')],
 ('the first rite of {aim.contest}', "wait a year, until it feels like your own and not the family's"): [('lesson',
                                                                                                          'there is '
                                                                                                          'no rush')],
 ('the first rite of {aim.contest}', 'take part, and ask to be the one who helps the newcomers next time'): [('door',
                                                                                                              'kept '
                                                                                                              'your '
                                                                                                              'word')],
 ('the first rite of {aim.contest}', 'take part, and keep a private record of everything you feel'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('the first rite of {aim.contest}', 'make a point of taking part beside the oldest member, who did it at your age'): [('person',
                                                                                                                        'elder')],
 ('the first rite of {aim.contest}', 'say plainly you are not ready, and help with the preparations instead'): [('person',
                                                                                                                 'friend')],
 ('the first rite of {aim.contest}', 'watch it from the side this time, and ask your questions after'): [('person',
                                                                                                          'mentor')],
 ('the year {N} is asked to lead {aim.contest}', 'lead it exactly as it has always been led'): [('door',
                                                                                                 'kept your word')],
 ('the year {N} is asked to lead {aim.contest}', 'lead it, and tell the room honestly about the question you cannot answer'): [('mark',
                                                                                                                                'owned '
                                                                                                                                'up')],
 ('the year {N} is asked to lead {aim.contest}', 'lead it so well that nobody sees the doubt behind it'): [('door',
                                                                                                            'kept it '
                                                                                                            'hidden')],
 ('the year {N} is asked to lead {aim.contest}', 'lead it in your own way, with music and silences nobody expected'): [('mark',
                                                                                                                        'defied '
                                                                                                                        'an '
                                                                                                                        'authority')],
 ('the year {N} is asked to lead {aim.contest}', 'ask an older one to lead this year, and stand beside them'): [('person',
                                                                                                                 'elder')],
 ('the year {N} is asked to lead {aim.contest}', 'lead it, and spend the month before in study with {aim.person}'): [('person',
                                                                                                                      'mentor')],
 ('the year {N} is asked to lead {aim.contest}', 'write a new reading for it that people will argue over for years'): [('person',
                                                                                                                        'rival')],
 ('the year {N} is asked to lead {aim.contest}', 'make it the largest gathering the place has ever seen'): [('place',
                                                                                                             'gather.great')],
 ('the year {N} is asked to lead {aim.contest}', 'take the rite outdoors, to where it was first kept'): [('place',
                                                                                                          'faith.shrines')],
 ('the year {N} is asked to lead {aim.contest}', 'step back this year, and keep the question company in private'): [('lesson',
                                                                                                                     'a '
                                                                                                                     'question '
                                                                                                                     'can '
                                                                                                                     'be '
                                                                                                                     'lived '
                                                                                                                     'with')],
 ('the teacher who answers with a question', 'meet every month without fail, and do the reading set'): [('person',
                                                                                                         'mentor')],
 ('the teacher who answers with a question', 'bring your hardest doubt to the very first meeting'): [('mark',
                                                                                                      'owned up')],
 ('the teacher who answers with a question', 'learn all they know, and ask who else is worth meeting'): [('person',
                                                                                                          'patron')],
 ('the teacher who answers with a question', 'argue back every time, and see whether they enjoy it too'): [('lesson',
                                                                                                            'arguing '
                                                                                                            'can be '
                                                                                                            'listening')],
 ('the teacher who answers with a question', 'meet when you can, and let it grow at its own pace'): [('person',
                                                                                                      'elder')],
 ('the teacher who answers with a question', 'take them as your teacher formally, in front of the others'): [('place',
                                                                                                              'faith.orders')],
 ('the teacher who answers with a question', 'ask them what they got wrong when they were young'): [('person',
                                                                                                     'friend')],
 ('the teacher who answers with a question', 'ask them for the old ways nobody else bothers to teach'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the teacher who answers with a question', 'thank them warmly, and keep to your own way for now'): [('door',
                                                                                                       'turned down '
                                                                                                       'a chance')],
 ('the teacher who answers with a question', 'walk with them in silence for the first few meetings'): [('lesson',
                                                                                                        'silence can '
                                                                                                        'teach too')],
 ('the one who seems to have it all worked out', 'answer them calmly from what the teaching says, and leave it there'): [('means',
                                                                                                                          'ties+.03')],
 ('the one who seems to have it all worked out', 'study what they say until you can answer it fairly'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the one who seems to have it all worked out', 'show them up in the next discussion, in front of everyone'): [('person',
                                                                                                                 'rival')],
 ('the one who seems to have it all worked out', 'tell them exactly how it felt to hear that'): [('door',
                                                                                                  'made an enemy')],
 ('the one who seems to have it all worked out', 'let them be, and keep to your own quiet path'): [('lesson',
                                                                                                    'their sureness '
                                                                                                    'is theirs')],
 ('the one who seems to have it all worked out', 'ask {aim.person} to hear you both and settle the point'): [('person',
                                                                                                              'go-between')],
 ('the one who seems to have it all worked out', 'learn from where they are strong, and say nothing until you are stronger'): [('lesson',
                                                                                                                                'rivals '
                                                                                                                                'can '
                                                                                                                                'be '
                                                                                                                                'teachers')],
 ('the one who seems to have it all worked out', 'challenge them to an open debate, and enjoy every minute'): [('place',
                                                                                                                'gather.talk')],
 ('the one who seems to have it all worked out', 'invite them on a walk and talk about something else entirely'): [('person',
                                                                                                                    'friend')],
 ('the one who seems to have it all worked out', 'step back from the group they lead, and find another to sit with'): [('place',
                                                                                                                        'faith.seeking')],
 ('the season when it all goes quiet', 'keep going every week, even while it means nothing'): [('mark',
                                                                                                'kept your word')],
 ('the season when it all goes quiet', 'take the doubt seriously, and read everything you can on it'): [('place',
                                                                                                         'learn.keeping')],
 ('the season when it all goes quiet', 'have it out, face to face, with the one who broke the promise'): [('mark',
                                                                                                           'defied '
                                                                                                           'an '
                                                                                                           'authority')],
 ('the season when it all goes quiet', 'walk away from it openly, and see what is left when the noise stops'): [('lesson',
                                                                                                                 'some '
                                                                                                                 'answers '
                                                                                                                 'come '
                                                                                                                 'after '
                                                                                                                 'leaving')],
 ('the season when it all goes quiet', 'step back gently, and keep the friends you made there'): [('person',
                                                                                                   'friend')],
 ('the season when it all goes quiet', 'ask for a different part in it, away from the hurt'): [('person',
                                                                                                'go-between')],
 ('the season when it all goes quiet', 'look for others who have doubted, and talk it through with them'): [('place',
                                                                                                             'faith.seeking')],
 ('the season when it all goes quiet', 'go back to the oldest, simplest form of the practice'): [('mark',
                                                                                                  'learned a skill')],
 ('the season when it all goes quiet', 'tell {aim.person} honestly how it is, and let them help'): [('person',
                                                                                                     'mentor')],
 ('the season when it all goes quiet', 'take time out of doors, and let the questions settle'): [('place',
                                                                                                  'prod.wild')],
 ('the years when nothing deepens', 'keep to it faithfully, as you promised, and trust the years'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the years when nothing deepens', 'change how you practise: new texts, new teachers, new questions'): [('person',
                                                                                                          'mentor')],
 ('the years when nothing deepens', 'ask for more responsibility, and grow through the work'): [('place',
                                                                                                 'faith.orders')],
 ('the years when nothing deepens', 'try something long thought to be out of reach'): [('mark', 'took a wild risk')],
 ('the years when nothing deepens', 'keep a smaller part for a while, and give the time to home'): [('means',
                                                                                                     'ties+.05')],
 ('the years when nothing deepens', 'slow down to one study night a week, and keep it'): [('mark',
                                                                                           'learned a skill')],
 ('the years when nothing deepens', 'let it go, and carry what it taught into the rest of life'): [('lesson',
                                                                                                    'what was kept '
                                                                                                    'stays with '
                                                                                                    'you')],
 ('the years when nothing deepens', 'step out for a season, and come back only if you miss it'): [('means',
                                                                                                   'freedom+.04')],
 ('the years when nothing deepens', 'go on retreat for a month, somewhere you have never been'): [('place',
                                                                                                   'faith.shrines')],
 ('the years when nothing deepens', 'let it rest, and stay close to the ones who kept the practice too'): [('person',
                                                                                                            'friend')],
 ('what going deeper asks of the household', 'give what the custom asks, and no more than the budget allows'): [('means',
                                                                                                                 'money-.04')],
 ('what going deeper asks of the household', 'find a shorter course that teaches the same, and pay for that'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('what going deeper asks of the household', 'ask {aim.person} to sponsor the place, and owe them for it'): [('person',
                                                                                                              'patron')],
 ('what going deeper asks of the household', 'give it everything: the savings, the season, all of it'): [('means',
                                                                                                          'money-.09')],
 ('what going deeper asks of the household', 'put the family first, and keep the practice at home for now'): [('means',
                                                                                                               'ties+.05')],
 ('what going deeper asks of the household', 'wait a year and save for it properly'): [('door', 'kept your word')],
 ('what going deeper asks of the household', 'go, and bring the family to share the closing days'): [('means',
                                                                                                      'ties+.03')],
 ('what going deeper asks of the household', 'go, and send money home every week you are away'): [('means',
                                                                                                   'money-.06')],
 ('what going deeper asks of the household', 'let this path go, and keep the friends met along it'): [('person',
                                                                                                       'friend')],
 ('what going deeper asks of the household', 'let it go, and keep reading on your own'): [('lesson',
                                                                                           'what you read stays '
                                                                                           'yours')],
 ('the invitation to serve', 'accept, and take on every duty that comes with it'): [('place', 'faith.orders')],
 ('the invitation to serve', "ask for a year's trial first, and decide then with open eyes"): [('door',
                                                                                                'turned down a '
                                                                                                'chance')],
 ('the invitation to serve', 'take it, and aim to lead the whole community within a few years'): [('person',
                                                                                                   'patron')],
 ('the invitation to serve', 'turn it down: it would tie you to one place and one way'): [('mark',
                                                                                           'turned down a chance')],
 ('the invitation to serve', 'take it, if it means staying near the people already known'): [('means', 'ties+.04')],
 ('the invitation to serve', 'accept, and ask for time to study as part of the role'): [('place', 'learn.higher')],
 ('the invitation to serve', 'take it, and set out clear terms before starting'): [('door', 'kept your word')],
 ('the invitation to serve', 'take it, and go wherever they send'): [('mark', 'moved away')],
 ('the invitation to serve', 'let the role go, and keep the practice in your own life, unofficially'): [('lesson',
                                                                                                         'a calling '
                                                                                                         'can live '
                                                                                                         'at home')],
 ('the invitation to serve', 'step away from it for good, and stay with the people who rely on them here'): [('person',
                                                                                                              'neighbour')],
 ('the community that will not take {N} as {N} is', 'go through {aim.round}, with a good word from an old friend'): [('person',
                                                                                                                      'go-between')],
 ('the community that will not take {N} as {N} is', 'try several ways round before settling on one'): [('place',
                                                                                                        'faith.seeking')],
 ('the community that will not take {N} as {N} is', 'go round, and build something of your own there that others will join'): [('person',
                                                                                                                                'regular')],
 ('the community that will not take {N} as {N} is', 'leave the old door behind and throw everything into {aim.round}'): [('mark',
                                                                                                                          'defied '
                                                                                                                          'an '
                                                                                                                          'authority')],
 ('the community that will not take {N} as {N} is', 'let it rest, and keep it as a private thing at home'): [('lesson',
                                                                                                              'it '
                                                                                                              'can '
                                                                                                              'live '
                                                                                                              'in '
                                                                                                              'small '
                                                                                                              'things')],
 ('the community that will not take {N} as {N} is', 'ask the ones in charge, formally, to think again, and go round meanwhile'): [('person',
                                                                                                                                   'elder')],
 ('the community that will not take {N} as {N} is', 'go through {aim.round}, and keep the questions that got you shut out'): [('mark',
                                                                                                                               'learned '
                                                                                                                               'a '
                                                                                                                               'skill')],
 ('the community that will not take {N} as {N} is', 'find the relatives who would quietly back you, and go round together'): [('means',
                                                                                                                               'ties+.04')],
 ('the community that will not take {N} as {N} is', 'let this one go, and keep the one friend who stood by through it all'): [('person',
                                                                                                                               'friend')],
 ('the community that will not take {N} as {N} is', 'wait a season, then try {aim.round} when things at home are calmer'): [('means',
                                                                                                                             'time+.03')],
 ('the talk at home about {aim.thing}', 'keep to it quietly, and keep every family duty too'): [('door',
                                                                                                 'kept your word')],
 ('the talk at home about {aim.thing}', 'explain calmly what it means, and hear what it means to them'): [('lesson',
                                                                                                           'both '
                                                                                                           'sides '
                                                                                                           'can be '
                                                                                                           'heard')],
 ('the talk at home about {aim.thing}', 'make clear it is your life and your choice'): [('mark',
                                                                                         'defied an authority')],
 ('the talk at home about {aim.thing}', 'say how it hurts when they make light of it, and leave if you must'): [('means',
                                                                                                                 'ties-.03')],
 ('the talk at home about {aim.thing}', 'take it more lightly at home, for the sake of peace'): [('means',
                                                                                                  'ties+.04')],
 ('the talk at home about {aim.thing}', 'agree to keep it to set times, and study the rest on your own'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ('the talk at home about {aim.thing}', 'find the relative who understands, and let them speak up at home'): [('person',
                                                                                                               'go-between')],
 ('the talk at home about {aim.thing}', 'bring them along once, so they see what you see'): [('lesson',
                                                                                              'seeing is better than '
                                                                                              'telling')],
 ('the talk at home about {aim.thing}', 'let their worry slow you down, because you love them'): [('means',
                                                                                                   'time+.03')],
 ('the talk at home about {aim.thing}', 'step back from it, because the arguments at home have worn you down'): [('mark',
                                                                                                                  'gave '
                                                                                                                  'in '
                                                                                                                  'to '
                                                                                                                  'pressure')],
 ('{aim.rung}, where others can see it', 'give thanks the way the custom asks, with everyone present'): [('means',
                                                                                                          'ties+.04')],
 ('{aim.rung}, where others can see it', 'sit with it alone for a day, and think about what it means'): [('lesson',
                                                                                                          'arriving '
                                                                                                          'is '
                                                                                                          'another '
                                                                                                          'beginning')],
 ('{aim.rung}, where others can see it', 'let it be known, and take on what the new place allows'): [('person',
                                                                                                      'patron')],
 ('{aim.rung}, where others can see it', 'sing, dance and share the day with anyone who comes'): [('place',
                                                                                                   'arts.song')],
 ('{aim.rung}, where others can see it', 'go home and share it quietly with the oldest in the family'): [('person',
                                                                                                          'elder')],
 ('{aim.rung}, where others can see it', 'take up the new duties at once, and do them well from the first day'): [('door',
                                                                                                                   'kept '
                                                                                                                   'your '
                                                                                                                   'word')],
 ('{aim.rung}, where others can see it', 'write about the road here, honestly, for others still on it'): [('lesson',
                                                                                                           'the road '
                                                                                                           'is worth '
                                                                                                           'telling')],
 ('{aim.rung}, where others can see it', 'use the new standing to help the ones who did the teaching'): [('mark',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('{aim.rung}, where others can see it', 'open the doors to everyone for a day of welcome'): [('place',
                                                                                               'gather.great')],
 ('{aim.rung}, where others can see it', 'go back to the start, and read the first words again with new eyes'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('an ordinary night of {aim.doing}', 'finish the drill exactly as it was set, every last repeat'): [('mark',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('an ordinary night of {aim.doing}', 'go over the one thing slowly until you see why it goes wrong'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('an ordinary night of {aim.doing}', 'ask the best one there for a lesson, and stay until it comes right'): [('person',
                                                                                                               'mentor')],
 ('an ordinary night of {aim.doing}', 'drop the drill and just mess about for the rest of the night'): [('lesson',
                                                                                                         'play keeps '
                                                                                                         'it alive')],
 ('an ordinary night of {aim.doing}', 'stop when the body says stop, and come back fresh next week'): [('means',
                                                                                                        'health+.03')],
 ('an ordinary night of {aim.doing}', 'note down what went wrong, and set the same drill for next week'): [('lesson',
                                                                                                            'small '
                                                                                                            'notes '
                                                                                                            'add '
                                                                                                            'up')],
 ('an ordinary night of {aim.doing}', 'work out which weakness the others will spot first, and fix that'): [('door',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('an ordinary night of {aim.doing}', 'turn the last half hour into a contest with whoever is left'): [('person',
                                                                                                        'rival')],
 ('an ordinary night of {aim.doing}', 'keep going with a friend long after it stops being practice'): [('person',
                                                                                                        'friend')],
 ('an ordinary night of {aim.doing}', 'help the newer ones set up, and walk home the long way'): [('means',
                                                                                                   'ties+.03')],
 ('the hours nobody sees', 'keep to the plan to the letter, rest days included'): [('mark', 'kept your word')],
 ('the hours nobody sees', 'take apart the last three defeats and find the pattern in them'): [('mark',
                                                                                                'learned a skill')],
 ('the hours nobody sees', 'add a second session every day, whatever it costs'): [('means', 'time-.08')],
 ('the hours nobody sees', 'throw out the plan for a week and do it for joy alone'): [('lesson',
                                                                                       'joy is part of the work')],
 ('the hours nobody sees', 'ease off for a week and let the body catch up'): [('means', 'health+.04')],
 ('the hours nobody sees', "train to the group's schedule, and quietly outwork everyone in it"): [('person',
                                                                                                   'rival')],
 ('the hours nobody sees', 'cut everything that does not help, but keep one family day a week'): [('means',
                                                                                                   'ties+.03')],
 ('the hours nobody sees', 'go back to the first teacher and relearn the basics properly'): [('person', 'mentor')],
 ('the hours nobody sees', 'try a strange new approach for a month, just to see what breaks'): [('mark',
                                                                                                 'took a wild risk')],
 ('the hours nobody sees', 'turn the hardest session into a game the whole group plays'): [('person', 'friend')],
 ('a name on the entry list', 'enter, and have everything ready the night before'): [('mark', 'kept your word')],
 ('a name on the entry list', 'enter, and study how the others went about it last time'): [('mark',
                                                                                            'learned a skill')],
 ('a name on the entry list', 'enter, and say out loud that you mean to win'): [('person', 'rival')],
 ('a name on the entry list', "put your name beside {friend}'s on the spot, before nerves can argue"): [('person',
                                                                                                         'friend')],
 ('a name on the entry list', 'wait for next time, and go along this time just to watch'): [('lesson',
                                                                                             'a year of watching '
                                                                                             'helps')],
 ('a name on the entry list', "enter the beginners' section, as the organisers advise"): [('lesson',
                                                                                           'start where the ground '
                                                                                           'is firm')],
 ('a name on the entry list', 'pick the section where you have a real chance of placing'): [('door',
                                                                                             'learned a skill')],
 ('a name on the entry list', 'enter the hardest section, because that is where it counts'): [('mark',
                                                                                               'took a wild risk')],
 ('a name on the entry list', 'skip the big one, and spend the weekend doing it for fun with friends'): [('means',
                                                                                                          'ties+.03')],
 ('a name on the entry list', "enter as one of the team, for the team's sake more than your own"): [('means',
                                                                                                     'ties+.04')],
 ('the one that counts', 'enter, and prepare exactly as planned, nothing new at the last minute'): [('mark',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('the one that counts', 'enter, and study every likely opponent in detail'): [('mark', 'learned a skill')],
 ('the one that counts', 'enter, and let everyone know who has come to win'): [('person', 'rival')],
 ('the one that counts', 'enter, and go all out from the very first minute'): [('mark', 'took a wild risk')],
 ('the one that counts', "let this one go by, and keep the year's rhythm steady"): [('lesson',
                                                                                     'not every year is the year')],
 ('the one that counts', "enter under the club's name, and carry its hopes with your own"): [('person', 'friend')],
 ('the one that counts', 'enter, and bring the family to watch so it is theirs too'): [('means', 'ties+.04')],
 ('the one that counts', 'skip it, and use the weeks to rebuild the basics properly'): [('door', 'learned a skill')],
 ('the one that counts', 'enter, with one bold new idea kept back for the day'): [('lesson', 'surprise works once')],
 ('the one that counts', 'go because the others are going and need a full side'): [('means', 'time-.04')],
 ('someone who has been there', 'ask properly, and agree the hours and the ground rules at the start'): [('person',
                                                                                                          'mentor')],
 ('someone who has been there', 'ask a hundred questions, and test every answer in practice'): [('mark',
                                                                                                 'learned a skill')],
 ('someone who has been there', 'make sure you are picked over the other one who asked'): [('person', 'rival')],
 ('someone who has been there', 'say yes on the spot, before the offer cools'): [('person', 'mentor')],
 ('someone who has been there', 'thank {mentor}, and keep learning the way the family taught'): [('lesson',
                                                                                                  'the old way still '
                                                                                                  'teaches')],
 ('someone who has been there', 'take the advice, and keep a notebook of every correction'): [('door',
                                                                                               'learned a skill')],
 ('someone who has been there', 'learn everything {mentor} knows, and then where {mentor} is wrong'): [('lesson',
                                                                                                        'even '
                                                                                                        'teachers '
                                                                                                        'miss '
                                                                                                        'things')],
 ('someone who has been there', 'ask for the hardest sessions going, and none of the easy ones'): [('means',
                                                                                                    'time-.06')],
 ('someone who has been there', 'go for the company as much as the teaching, and enjoy it'): [('person', 'friend')],
 ('someone who has been there', 'bring {parent} along, so the whole family agrees to it'): [('means', 'ties+.03')],
 ('the one who keeps winning', 'shake hands, play fair, and train to your own plan'): [('person', 'rival')],
 ('the one who keeps winning', 'study how {rival} wins, down to the smallest habit'): [('mark', 'learned a skill')],
 ('the one who keeps winning', 'make beating {rival} the only thing that matters this month'): [('means',
                                                                                                 'time-.06')],
 ('the one who keeps winning', 'challenge {rival} to a rematch right now, there and then'): [('mark',
                                                                                              'took a wild risk')],
 ('the one who keeps winning', 'let it be: {rival} is on one road and {N} on another'): [('lesson',
                                                                                          'someone will always be '
                                                                                          'ahead')],
 ('the one who keeps winning', 'ask to be drawn against {rival}, fair and square, and win it'): [('door',
                                                                                                  'made an enemy')],
 ('the one who keeps winning', 'train alongside {rival}, and use every session to close the gap'): [('person',
                                                                                                     'friend')],
 ('the one who keeps winning', 'ask {rival} how they learned, and really listen'): [('person', 'mentor')],
 ('the one who keeps winning', 'try something {rival} has never seen, just to see the look on their face'): [('door',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ('the one who keeps winning', 'laugh it off, and keep it a rivalry the whole place can enjoy'): [('means',
                                                                                                   'ties+.04')],
 ('the year nothing moved', 'finish the year as promised, then stop, and stay friends with the group'): [('mark',
                                                                                                          'kept your '
                                                                                                          'word'),
                                                                                                         ('person',
                                                                                                          'friend')],
 ('the year nothing moved', 'change the method completely: new drills, new routine, new eyes'): [('mark',
                                                                                                  'learned a skill')],
 ('the year nothing moved', 'find out what the people ahead do differently, and copy it'): [('person', 'rival')],
 ('the year nothing moved', 'let it go with no plan to come back, and see what fills the evenings'): [('lesson',
                                                                                                       'free '
                                                                                                       'evenings '
                                                                                                       'have their '
                                                                                                       'uses')],
 ('the year nothing moved', "keep going at the body's own pace, and stop counting results"): [('means',
                                                                                               'health+.03')],
 ('the year nothing moved', 'ask for an honest review of the year, and plan from what it says'): [('person',
                                                                                                   'mentor')],
 ('the year nothing moved', 'stop for good, and take the discipline it taught somewhere it counts more'): [('lesson',
                                                                                                            'discipline '
                                                                                                            'travels '
                                                                                                            'well')],
 ('the year nothing moved', 'keep it on your own terms: once a week, no plan, no pressure'): [('means', 'time+.05')],
 ('the year nothing moved', 'move to a looser group where it is just for the love of it'): [('place',
                                                                                             'gather.circle')],
 ('the year nothing moved', "sign up again, and help run the newcomers' sessions as well"): [('mark',
                                                                                              'helped someone in '
                                                                                              'need')],
 ('what {aim.doing} costs now', 'pay, but only within the budget the household agrees on'): [('mark',
                                                                                              'kept your word')],
 ('what {aim.doing} costs now', 'pay for the one thing that makes the most difference, and nothing else'): [('means',
                                                                                                             'money-.04')],
 ('what {aim.doing} costs now', 'pay whatever it takes, and find the money somehow'): [('means', 'money-.10')],
 ('what {aim.doing} costs now', 'turn down the extras, and train harder with what there is'): [('lesson',
                                                                                                'less gear, more '
                                                                                                'nerve')],
 ('what {aim.doing} costs now', 'let it go as a serious thing, and keep it for weekends with the family'): [('lesson',
                                                                                                             'the '
                                                                                                             'family '
                                                                                                             'comes '
                                                                                                             'before '
                                                                                                             'the '
                                                                                                             'fee')],
 ('what {aim.doing} costs now', 'pay, and put in the hours to earn the place it buys'): [('means', 'time-.06')],
 ('what {aim.doing} costs now', 'ask the wider family to chip in, and promise them a result'): [('door',
                                                                                                 'kept your word')],
 ('what {aim.doing} costs now', 'wait a season, and learn what can be learned for free meanwhile'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('what {aim.doing} costs now', 'find a cheaper way: borrowed equipment, shared lifts, free sessions'): [('person',
                                                                                                          'friend')],
 ('what {aim.doing} costs now', 'stop at this level, and coach the beginners for nothing on the side'): [('person',
                                                                                                          'friend')],
 ('the offer from further up', 'accept, once the terms and the hours are written down and agreed'): [('mark',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the offer from further up', 'ask for a trial week first, and decide on what it shows'): [('lesson',
                                                                                             'a trial before a '
                                                                                             'promise')],
 ('the offer from further up', 'take it, and make sure everyone back home hears about it'): [('person', 'patron')],
 ('the offer from further up', 'say yes tonight, and work out the rest later'): [('mark', 'took a wild risk')],
 ('the offer from further up', 'take it, if the whole household can make the change together'): [('mark',
                                                                                                  'moved away')],
 ('the offer from further up', 'take it, on the condition that school or work still comes first'): [('door',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('the offer from further up', 'ask to start next year instead, and spend the year getting stronger'): [('door',
                                                                                                         'turned '
                                                                                                         'down a '
                                                                                                         'chance')],
 ('the offer from further up', 'try out against the others it was offered to, and win the place outright'): [('person',
                                                                                                              'rival')],
 ('the offer from further up', 'turn it down, and keep {aim.doing} where the joy of it is'): [('person', 'friend')],
 ('the offer from further up', 'let it go here, with thanks, and give the time to home and town'): [('lesson',
                                                                                                     'knowing when '
                                                                                                     'is a skill')],
 ('a bad run', 'keep to the plan the coach sets for coming back, step by step'): [('person', 'mentor')],
 ('a bad run', 'go back over every loss, and find what actually changed'): [('mark', 'learned a skill')],
 ('a bad run', 'come back early and prove everyone wrong'): [('means', 'health-.04')],
 ('a bad run', 'let it all out to {friend}, then go straight back in'): [('person', 'friend')],
 ('a bad run', 'let it go, and keep what it gave: the strength, the friends, the habit'): [('lesson',
                                                                                            'it gave more than it '
                                                                                            'took')],
 ('a bad run', 'set a firm date for the comeback, and train to hit it'): [('means', 'time-.05')],
 ('a bad run', 'rest properly for once, sleep and eat well, because the best ones do'): [('means', 'health+.04')],
 ('a bad run', 'go back to the very first things learned, slowly'): [('door', 'learned a skill')],
 ('a bad run', 'stop for good, and put what it taught into something new'): [('mark', 'learned a skill')],
 ('a bad run', 'keep turning up for the group, even if only to help out'): [('means', 'ties+.04')],
 ('the door that will not open', 'apply for {aim.round} properly, with everything they ask for'): [('means',
                                                                                                    'time-.03')],
 ('the door that will not open', 'look into {aim.round} carefully: who runs it, how good it is, what it asks'): [('lesson',
                                                                                                                  'ask '
                                                                                                                  'before '
                                                                                                                  'you '
                                                                                                                  'join')],
 ('the door that will not open', 'go round the people in charge, straight to {aim.round}'): [('mark',
                                                                                              'defied an authority')],
 ('the door that will not open', 'turn up at {aim.round} tomorrow and talk your way in'): [('mark',
                                                                                            'took a wild risk')],
 ('the door that will not open', 'wait a year for a place where the family already belongs'): [('mark',
                                                                                                'stayed home')],
 ('the door that will not open', 'ask for the reasons in writing, and fix each one before next year'): [('door',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the door that will not open', 'try {aim.round}, and use what it teaches to come back stronger'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the door that will not open', 'try {aim.round}, and enjoy beating the people who said no'): [('person', 'rival')],
 ('the door that will not open', 'let it go, and find something new that is open right now'): [('lesson',
                                                                                                'a shut door frees '
                                                                                                'the evening')],
 ('the door that will not open', 'let it go, and keep the people it brought into your life'): [('person', 'friend')],
 ("the family's view of {aim.doing}", 'agree fixed hours for {aim.doing}, and keep to them'): [('mark',
                                                                                                'kept your word')],
 ("the family's view of {aim.doing}", 'lay out the plan and the numbers, and let them see the sense'): [('lesson',
                                                                                                         'a plan '
                                                                                                         'answers '
                                                                                                         'worry '
                                                                                                         'best')],
 ("the family's view of {aim.doing}", 'say it plainly: this matters more than anything else'): [('means',
                                                                                                 'ties-.04')],
 ("the family's view of {aim.doing}", 'storm off, then turn up at {aim.place} anyway'): [('mark',
                                                                                          'defied an authority')],
 ("the family's view of {aim.doing}", "give way, and ease off {aim.doing} for the family's sake"): [('mark',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ("the family's view of {aim.doing}", 'promise a result by the end of the year in return for their backing'): [('door',
                                                                                                                'kept '
                                                                                                                'your '
                                                                                                                'word')],
 ("the family's view of {aim.doing}", 'bring them to watch once, and let what they see change their minds'): [('means',
                                                                                                               'ties+.04')],
 ("the family's view of {aim.doing}", 'listen properly, and take on what is fair in what they say'): [('lesson',
                                                                                                       'they were '
                                                                                                       'partly '
                                                                                                       'right')],
 ("the family's view of {aim.doing}", 'hear them out, then carry on your own way, quietly'): [('door',
                                                                                               'kept it hidden')],
 ("the family's view of {aim.doing}", 'agree to cut back, unhappy about it, for peace at the table'): [('means',
                                                                                                        'ties+.03')],
 ('the result that settles it', 'thank everyone who helped, one at a time, before anything else'): [('means',
                                                                                                     'ties+.03')],
 ('the result that settles it', 'write down what worked, before the feeling fades'): [('mark', 'learned a skill')],
 ('the result that settles it', 'let everyone know, and set the next target that same night'): [('lesson',
                                                                                                 'one result is a '
                                                                                                 'start')],
 ('the result that settles it', 'celebrate loudly with everyone who was there'): [('person', 'friend')],
 ('the result that settles it', 'go home quietly, and tell the family first'): [('lesson',
                                                                                 'the family was the ground')],
 ('the result that settles it', 'sit down with the coach and plan the next stage properly'): [('person', 'mentor')],
 ('the result that settles it', 'work out quietly what this opens, and who to talk to next'): [('person', 'patron')],
 ('the result that settles it', 'throw a party, and make sure the doubters are invited'): [('person', 'rival')],
 ('the result that settles it', 'take the whole family out to eat, the loudest table in the place'): [('means',
                                                                                                       'ties+.04')],
 ('the result that settles it', 'go back to practice the next morning as usual, and help the beginners'): [('mark',
                                                                                                            'helped '
                                                                                                            'someone '
                                                                                                            'in '
                                                                                                            'need')],
 ('a small step further out', 'keep to a set routine: a little every day, written in the diary'): [('mark',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('a small step further out', 'read up first, and go knowing what to expect'): [('place', 'learn.keeping')],
 ('a small step further out', 'go one step further than anyone in the group dares'): [('person', 'rival')],
 ('a small step further out', 'throw out the plan and follow whatever turns up'): [('mark', 'took a wild risk')],
 ('a small step further out', 'take it slowly this week, and enjoy the ground already covered'): [('means',
                                                                                                   'health+.03')],
 ('a small step further out', "join an organised group, and aim to be leading it by the year's end"): [('place',
                                                                                                        'gather.hall')],
 ('a small step further out', 'take {friend} along, and make it something the two of you share'): [('person',
                                                                                                    'friend')],
 ('a small step further out', 'go with someone who has done it for years, and watch how they move'): [('person',
                                                                                                       'mentor')],
 ('a small step further out', 'try the odd option nobody recommends, just to find out'): [('lesson',
                                                                                           'the odd road teaches '
                                                                                           'most')],
 ('a small step further out', 'do less this week, and spend the time helping a newcomer start'): [('mark',
                                                                                                   'helped someone '
                                                                                                   'in need')],
 ('the seasoned way of doing it', 'keep up the dull upkeep: the checks, the practice, the planning'): [('means',
                                                                                                        'time-.04')],
 ('the seasoned way of doing it', 'learn the one hard thing that is still missing'): [('mark', 'learned a skill')],
 ('the seasoned way of doing it', 'take on a harder test than anyone expects of {N}'): [('mark', 'took a wild risk')],
 ('the seasoned way of doing it', 'go somewhere new on impulse, just to feel the first time again'): [('person',
                                                                                                       'friend')],
 ('the seasoned way of doing it', 'slow down, and go back to the places and people already loved'): [('means',
                                                                                                      'ties+.04')],
 ('the seasoned way of doing it', 'write up what the years have taught, for those starting out'): [('lesson',
                                                                                                    'writing it down '
                                                                                                    'makes it '
                                                                                                    'clear')],
 ('the seasoned way of doing it', 'specialise in the one thing few others can do'): [('door', 'learned a skill')],
 ('the seasoned way of doing it', 'go bigger: longer, further, harder, and see what holds'): [('means',
                                                                                               'health-.03')],
 ('the seasoned way of doing it', 'take a season just for pleasure, with no goals and no records'): [('means',
                                                                                                      'freedom+.05')],
 ('the seasoned way of doing it', 'take a younger one along, and show them how it is done'): [('mark',
                                                                                               'helped someone in '
                                                                                               'need')],
 ('the first real test', 'sign up, and prepare by the book, step by step'): [('means', 'time-.04')],
 ('the first real test', 'sign up, and learn everything about it beforehand'): [('mark', 'learned a skill')],
 ('the first real test', 'sign up for the harder version, the one people talk about'): [('mark', 'took a wild risk')],
 ('the first real test', 'sign up on the spot with {friend}, and go in fresh'): [('person', 'friend')],
 ('the first real test', 'wait until next year, when it feels right'): [('lesson', 'there is always next year')],
 ('the first real test', 'sign up with the group, and aim to come out at the top of it'): [('person', 'rival')],
 ('the first real test', 'sign up with someone close, and see it through together'): [('means', 'ties+.04')],
 ('the first real test', 'skip it, and spend the time on the basics instead'): [('door', 'learned a skill')],
 ('the first real test', 'sign up for the odd version that nobody else picks'): [('means', 'time-.03')],
 ('the first real test', 'skip it this time, and go along to cheer the others through'): [('means', 'ties+.03')],
 ('the undertaking people talk about', 'say yes, and prepare to the exact standard asked'): [('means', 'time-.06')],
 ('the undertaking people talk about', 'say yes, and study every account of those who tried before'): [('place',
                                                                                                        'learn.keeping')],
 ('the undertaking people talk about', 'say yes, and make sure everyone knows {N} means to finish first'): [('person',
                                                                                                             'rival')],
 ('the undertaking people talk about', 'say yes before the doubts can arrive'): [('mark', 'took a wild risk')],
 ('the undertaking people talk about', 'say no this time: the people at home need {N} more this year'): [('mark',
                                                                                                          'stayed '
                                                                                                          'home')],
 ('the undertaking people talk about', 'say yes, with a proper plan and someone at home who knows it'): [('door',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('the undertaking people talk about', 'say yes, and find a backer to pay for it in return for the story'): [('person',
                                                                                                              'patron')],
 ('the undertaking people talk about', 'say yes to the hardest version, the one that makes a name'): [('means',
                                                                                                       'health-.03')],
 ('the undertaking people talk about', 'say no, and keep the year for smaller trips with friends'): [('person',
                                                                                                      'friend')],
 ('the undertaking people talk about', 'say yes, as one of a team that looks after its own'): [('person',
                                                                                                'colleague')],
 ('the old hand who offers to show', 'accept, and agree when and how often to meet'): [('person', 'mentor')],
 ('the old hand who offers to show', 'accept, and ask about everything that ever went wrong for them'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the old hand who offers to show', 'accept, and ask for the introductions only {mentor} can make'): [('person',
                                                                                                        'patron')],
 ('the old hand who offers to show', 'ask to go along next time, wherever it is'): [('mark', 'took a wild risk')],
 ('the old hand who offers to show', 'listen to the stories, and keep learning at your own pace'): [('lesson',
                                                                                                     'stories carry '
                                                                                                     'the know-how')],
 ('the old hand who offers to show', 'accept, and work to be the best pupil {mentor} has had'): [('means',
                                                                                                  'time-.05')],
 ('the old hand who offers to show', 'accept, and bring {friend} along so both of you learn'): [('person', 'friend')],
 ('the old hand who offers to show', 'ask {mentor} to teach the old ways first, before the new'): [('person',
                                                                                                    'mentor')],
 ('the old hand who offers to show', 'take one tip, and go and try it straight away on your own'): [('door',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('the old hand who offers to show', 'thank {mentor}, and keep it loose: no lessons, just company when it suits'): [('means',
                                                                                                                     'freedom+.03')],
 ('the one who has been further', 'wish {rival} well, and keep to your own plan'): [('means', 'time-.03')],
 ('the one who has been further', "listen to {rival}'s stories for the useful parts"): [('mark', 'learned a skill')],
 ('the one who has been further', 'get to the next step before {rival}, whatever it takes'): [('means', 'time-.06')],
 ('the one who has been further', 'dare {rival} to do the next one together'): [('person', 'friend')],
 ('the one who has been further', 'let {rival} talk, and go back to your own pace'): [('lesson',
                                                                                       'comparing spoils the trip')],
 ('the one who has been further', 'suggest swapping notes, fairly, both ways'): [('person', 'colleague')],
 ('the one who has been further', 'find the gap {rival} has missed, and take it'): [('mark', 'took a wild risk')],
 ('the one who has been further', 'turn it into an open race, and enjoy every minute of it'): [('person', 'rival')],
 ('the one who has been further', 'laugh about it with {rival}, and invite them home for a meal'): [('means',
                                                                                                     'ties+.04')],
 ('the one who has been further', 'ask {rival} to share the costs and the planning on the next one'): [('means',
                                                                                                        'money+.03')],
 ('the thrill that went flat', 'book it anyway, as promised, and let the work bring the feeling back'): [('door',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('the thrill that went flat', 'change it completely: a new kind of challenge, a new skill to learn'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the thrill that went flat', 'raise the stakes until it means something again'): [('mark', 'took a wild risk')],
 ('the thrill that went flat', 'take a long break, and come back only if the itch returns'): [('means',
                                                                                               'freedom+.04')],
 ('the thrill that went flat', 'let it go, and keep the people met along the way'): [('person', 'friend')],
 ('the thrill that went flat', 'stop, and turn the experience into work: guiding, teaching, translating'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('the thrill that went flat', 'slow down to one trip a year, and make that one count'): [('means', 'time+.05')],
 ('the thrill that went flat', 'go back to the very first place, and see it with older eyes'): [('lesson',
                                                                                                 'old places look '
                                                                                                 'new later')],
 ('the thrill that went flat', 'let it go, and take its curiosity into something entirely new'): [('lesson',
                                                                                                   'curiosity '
                                                                                                   'outlasts the '
                                                                                                   'hobby')],
 ('the thrill that went flat', 'go on, but with a group, for the company more than the rush'): [('place',
                                                                                                 'gather.circle')],
 ('the price of going further', 'pay from what was set aside for it, and stop at the agreed limit'): [('means',
                                                                                                       'money-.06')],
 ('the price of going further', 'work out the cheapest way to do it properly, then pay for that'): [('means',
                                                                                                     'money-.03')],
 ('the price of going further', 'borrow, sell something, do whatever it takes to go'): [('means', 'money-.10')],
 ('the price of going further', 'go now, pay later, and see what happens'): [('door', 'took a wild risk')],
 ('the price of going further', 'let this one go: home needs the money, and {N}, more'): [('lesson',
                                                                                           'some years are for '
                                                                                           'staying')],
 ('the price of going further', 'wait a year, save properly, and plan it right'): [('means', 'money+.05')],
 ('the price of going further', 'find a way to be paid to go: a job, a grant, a backer'): [('person', 'patron')],
 ('the price of going further', 'turn down the costly version, and do it rough and cheap'): [('means', 'health-.03')],
 ('the price of going further', 'stop here, and keep the skills for trips close to home'): [('mark',
                                                                                             'learned a skill')],
 ('the price of going further', "pay, with the family's blessing and their help with the cost"): [('means',
                                                                                                   'ties+.03')],
 ('the offer to go far', 'accept, once the plans, the money and the return date are clear'): [('mark', 'moved away')],
 ('the offer to go far', 'ask to see the whole plan, test it, then decide'): [('lesson', 'a good plan shows itself')],
 ('the offer to go far', 'take it, and make the most of every contact it brings'): [('person', 'patron')],
 ('the offer to go far', 'say yes before the call has even ended'): [('mark', 'took a wild risk')],
 ('the offer to go far', 'decline it: the people at home need {N} here this year'): [('mark',
                                                                                      'turned down a chance')],
 ('the offer to go far', 'accept, but only on terms that bring {N} back with something to show'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('the offer to go far', 'say yes if {friend} can come too, and push hard for it'): [('person', 'friend')],
 ('the offer to go far', 'ask to go for a shorter spell next year instead'): [('door', 'turned down a chance')],
 ('the offer to go far', 'turn it down, and plan a stranger journey of your own'): [('means', 'freedom+.04')],
 ('the offer to go far', 'let it go for good, and put the restlessness into something at home'): [('lesson',
                                                                                                   'the itch can '
                                                                                                   'point anywhere')],
 ('the trip that went wrong', 'go over what went wrong with someone experienced, and fix the plan'): [('person',
                                                                                                       'mentor')],
 ('the trip that went wrong', 'work out exactly where it turned, and learn the skill that was missing'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the trip that went wrong', 'go straight back, harder, before the fear can set in'): [('mark', 'took a wild risk')],
 ('the trip that went wrong', 'tell the story to everyone until it becomes a good one'): [('means', 'ties+.04')],
 ('the trip that went wrong', 'stay home for a season and let body and nerve recover'): [('means', 'health+.04')],
 ('the trip that went wrong', 'take a proper course in first aid and planning'): [('place', 'prot.rescue')],
 ('the trip that went wrong', 'let it go, and use what it taught somewhere else'): [('lesson',
                                                                                     'a hard trip still teaches')],
 ('the trip that went wrong', 'go back to the same place, and finish what was started'): [('door',
                                                                                           'took a wild risk')],
 ('the trip that went wrong', 'let it go, and keep the friends who helped bring {N} home'): [('person', 'friend')],
 ('the trip that went wrong', 'keep going, but only with a group that looks after its own'): [('place',
                                                                                               'gather.circle')],
 ('the road that is closed', 'apply for {aim.round} through the proper channels'): [('means', 'time-.03')],
 ('the road that is closed', 'look into {aim.round}, and find the version that teaches most'): [('mark',
                                                                                                 'learned a skill')],
 ('the road that is closed', 'use {aim.round} as a stepping stone, and say so openly'): [('person', 'colleague')],
 ('the road that is closed', "start on {aim.round} today, without waiting for anyone's leave"): [('mark',
                                                                                                  'defied an '
                                                                                                  'authority')],
 ('the road that is closed', 'wait for the road to open again, and tend what is close'): [('mark', 'stayed home')],
 ('the road that is closed', 'ask the people who said no what would change their minds, and do it'): [('door',
                                                                                                       'kept your '
                                                                                                       'word')],
 ('the road that is closed', "take {aim.round} with the family's help and blessing"): [('means', 'ties+.03')],
 ('the road that is closed', 'let it go, and learn the ground right here instead'): [('mark', 'learned a skill')],
 ('the road that is closed', 'try {aim.round}, and see where the odd road leads'): [('person', 'friend')],
 ('the road that is closed', 'let it go, and give the time to the people who need {N} here'): [('person',
                                                                                                'neighbour')],
 ('the worry at home', 'promise to send word at set times, and keep every promise'): [('door', 'kept your word')],
 ('the worry at home', 'show them the plan, the precautions and the numbers'): [('lesson',
                                                                                 'facts make fear smaller')],
 ('the worry at home', 'say it is {Ns} own life, and go anyway'): [('means', 'ties-.04')],
 ('the worry at home', 'laugh, hug them, and go'): [('means', 'freedom+.03')],
 ('the worry at home', 'stay closer to home for a while, for their sake'): [('mark', 'stayed home')],
 ('the worry at home', 'agree fair rules together: where, how long, how often'): [('means', 'ties+.03')],
 ('the worry at home', 'find the trip that satisfies both sides, and argue for that one'): [('lesson',
                                                                                             'half a yes still '
                                                                                             'moves')],
 ('the worry at home', 'promise them anything, then do as you please'): [('door', 'broke your word')],
 ('the worry at home', 'take them along on one trip, so they see it for themselves'): [('means', 'ties+.04')],
 ('the worry at home', 'give way, and keep {aim.doing} to what the family is easy with'): [('mark',
                                                                                            'gave in to pressure')],
 ('the day it shows', 'write to every person who helped along the way'): [('person', 'mentor')],
 ('the day it shows', 'go over the whole road again in a notebook, page by page'): [('mark', 'learned a skill')],
 ('the day it shows', 'let the people who matter in the field hear of it'): [('person', 'patron')],
 ('the day it shows', 'throw open the doors at home for a long, loud celebration'): [('person', 'friend')],
 ('the day it shows', 'go home quietly, and sleep in your own bed'): [('lesson', 'home feels different after')],
 ('the day it shows', 'accept the role it brings: leading others out'): [('person', 'colleague')],
 ('the day it shows', 'bring the family the stories and the gifts'): [('means', 'ties+.04')],
 ('the day it shows', 'go back to where it started, and see how far it has come'): [('lesson',
                                                                                     'the start looks small from '
                                                                                     'here')],
 ('the day it shows', 'plan the next strange thing before the week is out'): [('door', 'took a wild risk')],
 ('the day it shows', 'give a talk at the hall for anyone thinking of going'): [('place', 'gather.hall')],
 ('the long evening at {aim.place}', 'do the part again, exactly as you were shown, until it is right'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the long evening at {aim.place}', 'take the part apart to see why it keeps going wrong'): [('lesson',
                                                                                               'the mistake shows '
                                                                                               'the way')],
 ('the long evening at {aim.place}', 'stay later than everyone else, so the people who matter notice'): [('means',
                                                                                                          'time-.04')],
 ('the long evening at {aim.place}', 'leave it, and make something quick and wild just for fun'): [('means',
                                                                                                    'freedom+.03')],
 ('the long evening at {aim.place}', 'put the tools down and go home in time for supper'): [('means', 'ties+.03')],
 ('the long evening at {aim.place}', 'write down every step in a notebook kept for the purpose'): [('means',
                                                                                                    'time-.03')],
 ('the long evening at {aim.place}', "ask {aim.person} for the trick behind it, and offer an hour's help in return"): [('person',
                                                                                                                        'mentor')],
 ('the long evening at {aim.place}', 'race {friend} to finish first, and the slower one tidies up'): [('means',
                                                                                                       'ties+.02')],
 ('the long evening at {aim.place}', 'open the door, put music on and work at whatever pace comes'): [('lesson',
                                                                                                       'a light hand '
                                                                                                       'works '
                                                                                                       'better')],
 ('the long evening at {aim.place}', 'help the youngest one at the next bench with theirs first'): [('mark',
                                                                                                     'helped someone '
                                                                                                     'in need')],
 ('the season the hard jobs come to {N}', 'keep to the standard you are known for on every single job'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the season the hard jobs come to {N}', 'set aside one morning a week to try a new method'): [('mark',
                                                                                                 'learned a skill')],
 ('the season the hard jobs come to {N}', 'take only the jobs that carry your name further'): [('means',
                                                                                                'money+.05')],
 ('the season the hard jobs come to {N}', 'drop the queue for a week and make the piece dreamed of for years'): [('mark',
                                                                                                                  'took '
                                                                                                                  'a '
                                                                                                                  'wild '
                                                                                                                  'risk')],
 ('the season the hard jobs come to {N}', 'take the season more slowly and keep evenings for the people at home'): [('means',
                                                                                                                     'ties+.04')],
 ('the season the hard jobs come to {N}', 'set fair prices and a waiting list, and keep to both'): [('means',
                                                                                                     'money+.04')],
 ('the season the hard jobs come to {N}', 'take on an apprentice and let them carry the plain jobs'): [('person',
                                                                                                        'colleague')],
 ('the season the hard jobs come to {N}', 'teach the new one by working beside them, slowly, the old way'): [('lesson',
                                                                                                              'teaching '
                                                                                                              'shows '
                                                                                                              'the '
                                                                                                              'gaps')],
 ('the season the hard jobs come to {N}', 'turn down two safe jobs to make room for one strange one'): [('mark',
                                                                                                         'turned '
                                                                                                         'down a '
                                                                                                         'chance')],
 ('the season the hard jobs come to {N}', 'take a month off, then come back to the queue with fresh eyes'): [('means',
                                                                                                              'time+.05')],
 ('a first go at {aim.contest}', 'enter, read the rules twice, and hand the work in on time'): [('means',
                                                                                                 'time-.03')],
 ('a first go at {aim.contest}', 'enter to find out what the judges actually look for'): [('lesson',
                                                                                           'judges see different '
                                                                                           'things')],
 ('a first go at {aim.contest}', "enter to win, and study last year's winners first"): [('person', 'rival')],
 ('a first go at {aim.contest}', 'enter with something nobody would expect from a beginner'): [('mark',
                                                                                                'took a wild risk')],
 ('a first go at {aim.contest}', 'sit this one out and keep working quietly at home'): [('means', 'ties+.03')],
 ('a first go at {aim.contest}', 'sit it out this year, and go along to watch how it is run'): [('lesson',
                                                                                                 'watching first '
                                                                                                 'pays off')],
 ('a first go at {aim.contest}', 'enter, and ask the judges afterwards how to score higher'): [('person', 'mentor')],
 ('a first go at {aim.contest}', "skip the beginners' one and wait for a contest worth winning"): [('mark',
                                                                                                    'turned down a '
                                                                                                    'chance')],
 ('a first go at {aim.contest}', 'enter alongside {friend}, for the fun of the day'): [('means', 'ties+.02')],
 ('a first go at {aim.contest}', 'help the organisers set up instead of entering'): [('place', 'gather.hall')],
 ('{aim.contest} with the best of them', 'enter, and prepare to the same careful plan as always'): [('means',
                                                                                                     'time-.05')],
 ('{aim.contest} with the best of them', 'enter with the new method nobody has shown in public yet'): [('mark',
                                                                                                        'learned a '
                                                                                                        'skill')],
 ('{aim.contest} with the best of them', 'enter, and see that word of the entry reaches the right ears'): [('person',
                                                                                                            'patron')],
 ('{aim.contest} with the best of them', 'enter on the last day with the boldest piece you have'): [('mark',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('{aim.contest} with the best of them', 'let this one pass; the season at home matters more'): [('means',
                                                                                                  'ties+.04')],
 ('{aim.contest} with the best of them', 'enter as the one to beat, and keep your nerve in public'): [('person',
                                                                                                       'rival')],
 ('{aim.contest} with the best of them', 'skip it, and put the work into the regulars who already come'): [('person',
                                                                                                            'regular')],
 ('{aim.contest} with the best of them', 'skip it this year and spend the weeks learning from an older hand'): [('person',
                                                                                                                 'mentor')],
 ('{aim.contest} with the best of them', 'enter something half-finished, to see what the judges make of it'): [('lesson',
                                                                                                                'a '
                                                                                                                'rough '
                                                                                                                'draft '
                                                                                                                'teaches '
                                                                                                                'fast')],
 ('{aim.contest} with the best of them', 'enter with {friend} as a pair, and share whatever comes'): [('means',
                                                                                                       'ties+.03')],
 ('the one who could teach {N} properly', 'come every Saturday, on time, and do what you are told'): [('door',
                                                                                                       'kept your '
                                                                                                       'word')],
 ('the one who could teach {N} properly', 'come with a list of questions, and write down every answer'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the one who could teach {N} properly', 'come, and make sure you are the best pupil they have ever had'): [('person',
                                                                                                              'rival')],
 ('the one who could teach {N} properly', 'say yes, then argue with every method they show'): [('lesson',
                                                                                                'arguing is a way of '
                                                                                                'learning')],
 ('the one who could teach {N} properly', 'thank them, and say Saturdays belong to the family for now'): [('mark',
                                                                                                           'turned '
                                                                                                           'down a '
                                                                                                           'chance')],
 ('the one who could teach {N} properly', 'ask to come once a month and work on what they set in between'): [('means',
                                                                                                              'time-.03')],
 ('the one who could teach {N} properly', 'swap what you know of the newer tools for their old tricks'): [('person',
                                                                                                           'mentor')],
 ('the one who could teach {N} properly', 'turn up with your best piece and ask what is wrong with it'): [('lesson',
                                                                                                           'hard '
                                                                                                           'words '
                                                                                                           'help '
                                                                                                           'most')],
 ('the one who could teach {N} properly', 'bring {friend} along, so the Saturdays feel like your own'): [('means',
                                                                                                          'ties+.03')],
 ('the one who could teach {N} properly', 'offer to sweep up and fetch things, and learn by being near'): [('person',
                                                                                                            'mentor')],
 ('the one at the next bench', 'work harder by the rules and let the results speak'): [('means', 'time-.04')],
 ('the one at the next bench', 'study what {rival} does well and take the best of it'): [('mark', 'learned a skill')],
 ('the one at the next bench', 'challenge {rival} openly, in front of everyone'): [('person', 'rival')],
 ('the one at the next bench', 'make something so different that nobody can compare the two'): [('mark',
                                                                                                 'took a wild risk')],
 ('the one at the next bench', 'stop counting, and make the work for the people it is for'): [('lesson',
                                                                                               'the work is not a '
                                                                                               'race')],
 ('the one at the next bench', 'ask for a fair chance at the next big job, and say so plainly'): [('lesson',
                                                                                                   'asking plainly '
                                                                                                   'can work')],
 ('the one at the next bench', 'win {rival} over, and work side by side instead'): [('person', 'friend')],
 ('the one at the next bench', 'keep your head down and learn from an older hand for a while'): [('person',
                                                                                                  'mentor')],
 ('the one at the next bench', 'propose a friendly match: the same job, two ways, and others judge'): [('means',
                                                                                                        'time-.03')],
 ('the one at the next bench', 'tell {rival} to their face what you think, then shake hands'): [('door',
                                                                                                 'made a friend')],
 ('the work that failed in front of everyone', 'own the fault, put it right for nothing, and start again'): [('mark',
                                                                                                              'owned '
                                                                                                              'up')],
 ('the work that failed in front of everyone', 'find out exactly why it failed before touching anything else'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('the work that failed in front of everyone', 'make the next piece so good that nobody remembers this one'): [('means',
                                                                                                                'time-.05')],
 ('the work that failed in front of everyone', 'walk away from {aim.doing} for good, and mean it'): [('lesson',
                                                                                                      'knowing when '
                                                                                                      'it is done')],
 ('the work that failed in front of everyone', 'set {aim.doing} aside and turn back to the people at home'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the work that failed in front of everyone', 'go back to the first steps and rebuild the method, piece by piece'): [('lesson',
                                                                                                                       'the '
                                                                                                                       'basics '
                                                                                                                       'hold '
                                                                                                                       'everything '
                                                                                                                       'up')],
 ('the work that failed in front of everyone', 'quietly ask the people it was for what went wrong, and win them back'): [('person',
                                                                                                                          'regular')],
 ('the work that failed in front of everyone', 'put it down to bad luck and take on a harder job at once'): [('mark',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ('the work that failed in front of everyone', 'let it go for now, and keep close to the friend who stood by through it'): [('person',
                                                                                                                             'friend')],
 ('the work that failed in front of everyone', 'stay on and finish the season you promised, then decide'): [('door',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the year nothing gets better', 'keep to the routine, every week, and trust it to turn'): [('door',
                                                                                              'kept your word')],
 ('the year nothing gets better', 'change the method completely and start the year as a beginner'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the year nothing gets better', 'find a harder teacher who allows no coasting'): [('person', 'mentor')],
 ('the year nothing gets better', 'stop for good, and go looking for whatever feels alive now'): [('lesson',
                                                                                                   'moving on frees '
                                                                                                   'the hands')],
 ('the year nothing gets better', 'step back to one evening a week, and keep it for the joy'): [('means',
                                                                                                 'time+.04')],
 ('the year nothing gets better', 'set a clear test for the spring, and decide then'): [('lesson',
                                                                                         'a deadline clears the '
                                                                                         'head')],
 ('the year nothing gets better', 'let it go, and give your tools to someone just starting'): [('mark',
                                                                                                'learned a skill')],
 ('the year nothing gets better', 'slow right down, and teach a beginner what you already know'): [('person',
                                                                                                    'colleague')],
 ('the year nothing gets better', 'take a month off, then come back with a completely new idea'): [('means',
                                                                                                    'freedom+.03')],
 ('the year nothing gets better', 'go back, but join a different group at {aim.place} with new faces'): [('person',
                                                                                                          'friend')],
 ('the price of the next step', 'pay, but only what the household agreed, to the last coin'): [('door',
                                                                                                'kept your word')],
 ('the price of the next step', 'buy the tools second-hand, mend them, and pay for the course alone'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the price of the next step', 'take on extra work to pay for all of it alone'): [('means', 'time-.06')],
 ('the price of the next step', 'throw your savings at the best of everything'): [('means', 'money-.08')],
 ('the price of the next step', 'let {aim.doing} go, and put the money where the family needs it'): [('lesson',
                                                                                                      'what was '
                                                                                                      'learned '
                                                                                                      'stays')],
 ('the price of the next step', 'skip the course this year, and learn from library books meanwhile'): [('place',
                                                                                                        'learn.keeping')],
 ('the price of the next step', 'ask {aim.person} if you can work for them in place of a fee'): [('person',
                                                                                                  'mentor')],
 ('the price of the next step', 'borrow the money and bet on it paying back'): [('door', 'took a wild risk')],
 ('the price of the next step', 'keep going with what you have, and ask {friend} to share tools'): [('means',
                                                                                                     'ties+.03')],
 ('the price of the next step', 'wait a year, put a little by each week, and decide then'): [('means', 'money+.03')],
 ('the offer that would change everything', 'take it, on proper terms written down and signed'): [('mark',
                                                                                                   'moved away')],
 ('the offer that would change everything', 'take it for what you will learn there, whatever the pay'): [('person',
                                                                                                          'mentor')],
 ('the offer that would change everything', 'take it, and bargain hard for more than they offered'): [('means',
                                                                                                       'money+.06')],
 ('the offer that would change everything', 'say yes on the spot and pack the same night'): [('mark',
                                                                                              'took a wild risk')],
 ('the offer that would change everything', 'turn it down, and stay where the family needs an extra pair of hands'): [('mark',
                                                                                                                       'stayed '
                                                                                                                       'home')],
 ('the offer that would change everything', 'ask to start in a year, once your promises here are kept'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the offer that would change everything', 'turn it down, and build the same thing here, on your own ground'): [('door',
                                                                                                                  'turned '
                                                                                                                  'down '
                                                                                                                  'a '
                                                                                                                  'chance')],
 ('the offer that would change everything', 'keep {aim.doing} as a love rather than a living, and say no with thanks'): [('lesson',
                                                                                                                          'some '
                                                                                                                          'loves '
                                                                                                                          'stay '
                                                                                                                          'small')],
 ('the offer that would change everything', 'take it for a trial season only, with the way home left open'): [('mark',
                                                                                                               'left '
                                                                                                               'home')],
 ('the offer that would change everything', 'let the whole road go, and keep the friends the offer brought'): [('person',
                                                                                                                'friend')],
 ('the waiting list that runs past spring', 'accept the answer for now and set {aim.doing} aside with good grace'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the waiting list that runs past spring', 'look into every way in, {aim.round} too, and pick the best'): [('lesson',
                                                                                                             'there '
                                                                                                             'is '
                                                                                                             'more '
                                                                                                             'than '
                                                                                                             'one '
                                                                                                             'door')],
 ('the waiting list that runs past spring', 'go round to {aim.round} and be useful there at once'): [('person',
                                                                                                      'colleague')],
 ('the waiting list that runs past spring', 'try {aim.round} tomorrow, without asking anyone first'): [('means',
                                                                                                        'freedom+.03')],
 ('the waiting list that runs past spring', 'ask around the neighbours until someone knows another way in'): [('person',
                                                                                                               'neighbour')],
 ('the waiting list that runs past spring', 'work from books at home this year, then try {aim.round}'): [('place',
                                                                                                          'learn.keeping')],
 ('the waiting list that runs past spring', 'trade a skill you already have for a spot at {aim.round}'): [('means',
                                                                                                           'time-.03')],
 ('the waiting list that runs past spring', 'wait for the spring, then turn up at {aim.round} with the work to show'): [('person',
                                                                                                                         'rival')],
 ('the waiting list that runs past spring', 'let {aim.doing} go for now, and keep the friend you made while waiting'): [('person',
                                                                                                                         'friend')],
 ('the waiting list that runs past spring', 'ask {mentor} for lessons at home until a place opens'): [('person',
                                                                                                       'mentor')],
 ('what the family says about {aim.doing}', 'keep at it, but meet the family halfway on the hours'): [('door',
                                                                                                       'kept your '
                                                                                                       'word')],
 ('what the family says about {aim.doing}', 'show them, calmly, what the work has already led to'): [('lesson',
                                                                                                      'proof beats '
                                                                                                      'argument')],
 ('what the family says about {aim.doing}', 'tell them you will prove them wrong, and mean it'): [('mark',
                                                                                                   'defied an '
                                                                                                   'authority')],
 ('what the family says about {aim.doing}', 'storm off to {aim.place} and work until they come round'): [('means',
                                                                                                          'ties-.04')],
 ('what the family says about {aim.doing}', "take their worry to heart, and cut back for the family's sake"): [('means',
                                                                                                                'ties+.05')],
 ('what the family says about {aim.doing}', 'agree to their terms for a year, then hold them to their side'): [('mark',
                                                                                                                'kept '
                                                                                                                'your '
                                                                                                                'word')],
 ('what the family says about {aim.doing}', 'bring the work home and let it win them over at the table'): [('lesson',
                                                                                                            'the '
                                                                                                            'work '
                                                                                                            'can '
                                                                                                            'speak '
                                                                                                            'for '
                                                                                                            'itself')],
 ('what the family says about {aim.doing}', 'listen to what worries them most, and change only that part'): [('means',
                                                                                                              'time+.03')],
 ('what the family says about {aim.doing}', 'keep going quietly and let them find out at the first showing'): [('door',
                                                                                                                'kept '
                                                                                                                'it '
                                                                                                                'hidden')],
 ('what the family says about {aim.doing}', 'have the row, then do the dishes together'): [('means', 'ties+.02')],
 ('the day the work is proven', 'thank every teacher along the way, one by one, properly'): [('person', 'mentor')],
 ('the day the work is proven', 'note what worked, and begin at once on what comes next'): [('mark',
                                                                                             'learned a skill')],
 ('the day the work is proven', 'spread the news this week wherever it can open a door'): [('person', 'patron')],
 ('the day the work is proven', 'throw a party at {aim.place} and invite everyone'): [('means', 'ties+.05')],
 ('the day the work is proven', 'tell only the family, quietly, over supper'): [('lesson', 'quiet joy lasts longer')],
 ('the day the work is proven', 'write the standard down, as a promise to keep it'): [('door', 'kept your word')],
 ('the day the work is proven', 'ask what the next step needs, and plan for it tonight'): [('lesson',
                                                                                            'the next step is a '
                                                                                            'plan')],
 ('the day the work is proven', 'go straight back to work the next morning, harder than before'): [('means',
                                                                                                    'time-.03')],
 ('the day the work is proven', 'take {friend} out for the day and celebrate in the open air'): [('means',
                                                                                                  'freedom+.03')],
 ('the day the work is proven', 'give your first tools to the next beginner at {aim.place}'): [('mark',
                                                                                                'helped someone in '
                                                                                                'need')],
 ('the hour that nobody hears', 'do the set exercises in order, the full hour, every day'): [('door',
                                                                                              'kept your word')],
 ('the hour that nobody hears', 'slow the hard stretch right down and take it apart'): [('mark', 'learned a skill')],
 ('the hour that nobody hears', 'put your work beside the best you know, and look hard at the gap'): [('lesson',
                                                                                                       'the gap '
                                                                                                       'shows what '
                                                                                                       'to fix')],
 ('the hour that nobody hears', 'throw the exercises aside and improvise until it feels alive'): [('means',
                                                                                                   'freedom+.03')],
 ('the hour that nobody hears', 'stop early and spend the rest of the evening with the family'): [('means',
                                                                                                   'ties+.03')],
 ('the hour that nobody hears', 'set a target for the week and keep a tally of it'): [('means', 'time-.03')],
 ('the hour that nobody hears', 'practise where the family can watch, and let them cheer'): [('means', 'ties+.04')],
 ('the hour that nobody hears', 'go back to the first simple piece you loved and find it again'): [('lesson',
                                                                                                    'the old piece '
                                                                                                    'still teaches')],
 ('the hour that nobody hears', 'try the hard stretch ten new ways and keep the strangest'): [('mark',
                                                                                               'learned a skill')],
 ('the hour that nobody hears', 'ask {friend} to join in, and practise together as a pair'): [('means', 'ties+.02')],
 ('the season people start to expect things', 'keep the same strict daily hours, whatever the season brings'): [('door',
                                                                                                                 'kept '
                                                                                                                 'your '
                                                                                                                 'word')],
 ('the season people start to expect things', 'spend the season on one hard new piece nobody has asked for'): [('mark',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ('the season people start to expect things', 'say yes to every showing that will grow the following'): [('person',
                                                                                                          'patron')],
 ('the season people start to expect things', 'change everything about how you work this season, on a hunch'): [('mark',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ('the season people start to expect things', 'slow the season down and keep the weekends for home'): [('means',
                                                                                                        'ties+.04')],
 ('the season people start to expect things', 'keep a written plan for each week and go over it on Sundays'): [('lesson',
                                                                                                                'a '
                                                                                                                'plan '
                                                                                                                'carries '
                                                                                                                'the '
                                                                                                                'weeks')],
 ('the season people start to expect things', 'study what the following comes back for, and give them more of it'): [('means',
                                                                                                                      'money+.04')],
 ('the season people start to expect things', 'book a run of showings in new places, one after another'): [('means',
                                                                                                            'health-.03')],
 ('the season people start to expect things', 'take a month away from it all and come back hungry'): [('means',
                                                                                                       'freedom+.04')],
 ('the season people start to expect things', 'spend Saturday mornings teaching the young ones for nothing'): [('mark',
                                                                                                                'helped '
                                                                                                                'someone '
                                                                                                                'in '
                                                                                                                'need')],
 ('the sign-up sheet for {aim.contest}', 'enter, rehearse every day, and arrive early on the night'): [('means',
                                                                                                        'time-.03')],
 ('the sign-up sheet for {aim.contest}', 'enter with a simple piece you know inside out'): [('mark',
                                                                                             'learned a skill')],
 ('the sign-up sheet for {aim.contest}', 'enter with the hardest piece you can manage, to stand out'): [('person',
                                                                                                         'rival')],
 ('the sign-up sheet for {aim.contest}', 'enter and make it up on the night, trusting the moment'): [('mark',
                                                                                                      'took a wild '
                                                                                                      'risk')],
 ('the sign-up sheet for {aim.contest}', 'rub the name out; this one can wait until you are ready'): [('means',
                                                                                                       'time+.03')],
 ('the sign-up sheet for {aim.contest}', 'enter, but first ask {aim.person} what the judges want'): [('person',
                                                                                                      'mentor')],
 ('the sign-up sheet for {aim.contest}', 'skip it, and put on a show at home for the family instead'): [('means',
                                                                                                         'ties+.04')],
 ('the sign-up sheet for {aim.contest}', 'go and watch this time, and take notes for next time'): [('lesson',
                                                                                                    'watching others '
                                                                                                    'shows how')],
 ('the sign-up sheet for {aim.contest}', 'enter with something of your own instead of the set piece'): [('lesson',
                                                                                                         'a piece of '
                                                                                                         "one's own "
                                                                                                         'carries')],
 ('the sign-up sheet for {aim.contest}', 'enter alongside {friend}, so neither stands up there alone'): [('means',
                                                                                                          'ties+.03')],
 ('{aim.contest} where names are made', 'accept, and prepare with the same discipline as always'): [('means',
                                                                                                     'time-.05')],
 ('{aim.contest} where names are made', 'accept, and bring a new piece made for that room alone'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('{aim.contest} where names are made', 'accept, and bring the piece most likely to win the room'): [('person',
                                                                                                      'patron')],
 ('{aim.contest} where names are made', 'accept, and bring something that will split the room in two'): [('mark',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('{aim.contest} where names are made', 'let the place go to someone who needs it more this year'): [('mark',
                                                                                                      'helped '
                                                                                                      'someone in '
                                                                                                      'need')],
 ('{aim.contest} where names are made', 'turn it down this year, and spend the month on the work itself'): [('lesson',
                                                                                                             'the '
                                                                                                             'work '
                                                                                                             'comes '
                                                                                                             'before '
                                                                                                             'the '
                                                                                                             'room')],
 ('{aim.contest} where names are made', 'accept, and use the night to meet the people who book the next ones'): [('person',
                                                                                                                  'go-between')],
 ('{aim.contest} where names are made', 'skip it and hold out for an even bigger night'): [('mark',
                                                                                            'turned down a chance')],
 ('{aim.contest} where names are made', 'accept, and bring the people you started with along to share it'): [('means',
                                                                                                              'ties+.04')],
 ('{aim.contest} where names are made', 'accept, and do it the way the first teacher showed it'): [('lesson',
                                                                                                    'the first way '
                                                                                                    'still holds')],
 ('the teacher who saw something in {N}', 'accept, turn up every Tuesday, and do the work set'): [('person',
                                                                                                   'mentor')],
 ('the teacher who saw something in {N}', 'accept, and ask why behind every correction'): [('mark',
                                                                                            'learned a skill')],
 ('the teacher who saw something in {N}', 'accept, and ask what it takes to be their best pupil ever'): [('means',
                                                                                                          'time-.05')],
 ('the teacher who saw something in {N}', 'say yes, but only if you can keep your own wild way of doing it'): [('mark',
                                                                                                                'defied '
                                                                                                                'an '
                                                                                                                'authority')],
 ('the teacher who saw something in {N}', 'say no kindly, and keep Tuesdays for {friend}'): [('means', 'ties+.04')],
 ('the teacher who saw something in {N}', 'accept, and agree a clear goal for the year with them'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the teacher who saw something in {N}', 'ask to share the Tuesday lessons with another pupil'): [('person',
                                                                                                    'friend')],
 ('the teacher who saw something in {N}', 'take lessons every other week, and practise alone in between'): [('means',
                                                                                                             'time+.03')],
 ('the teacher who saw something in {N}', 'accept, and bring them something new of your own every week'): [('lesson',
                                                                                                            'showing '
                                                                                                            'the '
                                                                                                            'work '
                                                                                                            'helps '
                                                                                                            'it '
                                                                                                            'grow')],
 ('the teacher who saw something in {N}', "accept on a whim, and then, to everyone's surprise, stay"): [('mark',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('the other one they compare {N} with', 'ask plainly why the spot went elsewhere, and what would earn the next'): [('lesson',
                                                                                                                     'asking '
                                                                                                                     'straight '
                                                                                                                     'gets '
                                                                                                                     'answers')],
 ('the other one they compare {N} with', 'go and watch {rival} closely, and learn what they know'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the other one they compare {N} with', 'make sure the next showing is so good the spot comes back'): [('means',
                                                                                                         'time-.05')],
 ('the other one they compare {N} with', 'answer with something loud and new, straight away'): [('mark',
                                                                                                 'took a wild risk')],
 ('the other one they compare {N} with', 'wish {rival} well, and stop keeping score against them'): [('means',
                                                                                                      'freedom+.03')],
 ('the other one they compare {N} with', 'put the rivalry into a strict new practice plan'): [('means', 'time-.03')],
 ('the other one they compare {N} with', 'propose showing together, and share the following between the two'): [('person',
                                                                                                                 'colleague')],
 ('the other one they compare {N} with', 'call {rival} out in public, and let the people decide'): [('person',
                                                                                                     'rival')],
 ('the other one they compare {N} with', 'share the long walk home with {rival}, and find out who they are'): [('person',
                                                                                                                'friend')],
 ('the other one they compare {N} with', 'keep your head down, and keep the promises you already made'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the answer that came back no', 'take the answer as final, and set {aim.doing} down tidily'): [('mark',
                                                                                                  'learned a skill')],
 ('the answer that came back no', 'go back over the work alone, and find its weak places unaided'): [('lesson',
                                                                                                      'the weak '
                                                                                                      'places show '
                                                                                                      'the way')],
 ('the answer that came back no', 'try again at once, somewhere that will say yes'): [('means', 'time-.04')],
 ('the answer that came back no', 'stop for good, and put the energy into something new'): [('lesson',
                                                                                             'an ending can be '
                                                                                             'clean')],
 ('the answer that came back no', 'go home, rest, and let the family talk over why it all began'): [('means',
                                                                                                     'ties+.03')],
 ('the answer that came back no', 'apply again next year, with a stronger piece and a clear plan'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the answer that came back no', 'let the big plans go, and keep the friends the work brought along'): [('person',
                                                                                                          'friend')],
 ('the answer that came back no', 'take a quiet season off, then begin again more slowly'): [('means', 'time+.04')],
 ('the answer that came back no', 'turn the rejection into the subject of the next piece'): [('mark',
                                                                                              'took a wild risk')],
 ('the answer that came back no', 'rage about it for one day, then book the next try'): [('means', 'time-.03')],
 ('the year the work stood still', 'book the dates and keep the routine, trusting it to turn'): [('door',
                                                                                                  'kept your word')],
 ('the year the work stood still', 'book half the dates, and spend the rest learning something new'): [('mark',
                                                                                                        'learned a '
                                                                                                        'skill')],
 ('the year the work stood still', 'find someone who can bring the work to a bigger crowd'): [('person',
                                                                                               'go-between')],
 ('the year the work stood still', 'let the dates go and walk away from {aim.doing} for good'): [('lesson',
                                                                                                  'leaving is '
                                                                                                  'allowed too')],
 ('the year the work stood still', 'book only a few dates, and keep the rest of the year gentle'): [('means',
                                                                                                     'time+.04')],
 ('the year the work stood still', 'ask {mentor} to look at the work and give an honest verdict'): [('lesson',
                                                                                                     'an outside eye '
                                                                                                     'helps')],
 ('the year the work stood still', 'change the whole style, and aim it at a new crowd'): [('mark',
                                                                                           'took a wild risk')],
 ('the year the work stood still', 'skip a season and travel to see what others are making'): [('means',
                                                                                                'freedom+.04')],
 ('the year the work stood still', 'let {aim.doing} go, and keep the people you made it with'): [('person',
                                                                                                  'friend')],
 ('the year the work stood still', 'keep going for the few who still come, and thank them by name'): [('person',
                                                                                                       'regular')],
 ('what the next step asks of the household', 'pay what the family agreed, and not a coin more'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('what the next step asks of the household', 'find good second-hand kit, and pay only for the lessons'): [('lesson',
                                                                                                            'cheaper '
                                                                                                            'can be '
                                                                                                            'smarter')],
 ('what the next step asks of the household', 'ask the family for the very best, and promise it will pay back'): [('means',
                                                                                                                   'ties-.03')],
 ('what the next step asks of the household', 'spend everything saved on it, today'): [('means', 'money-.08')],
 ('what the next step asks of the household', 'let {aim.doing} go as a goal, and keep it at home for joy'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('what the next step asks of the household', 'wait a term, put by what you can, and start properly then'): [('means',
                                                                                                              'time+.03')],
 ('what the next step asks of the household', 'keep going without lessons, learning beside others at the free group'): [('place',
                                                                                                                         'gather.circle')],
 ('what the next step asks of the household', "borrow old kit from the family's cupboard and learn alone a while"): [('means',
                                                                                                                      'ties+.03')],
 ('what the next step asks of the household', 'pay for the lessons in hours, by helping out at {aim.place}'): [('person',
                                                                                                                'mentor')],
 ('what the next step asks of the household', 'let it go for now, and keep the friends you made in the lessons'): [('person',
                                                                                                                    'friend')],
 ('the offer to go further', 'take it, once the terms are clear and fair on paper'): [('means', 'money+.05')],
 ('the offer to go further', 'take it for the teachers and the time to work'): [('person', 'mentor')],
 ('the offer to go further', 'take it, and push for a bigger part than offered'): [('person', 'patron')],
 ('the offer to go further', 'take it at once, and sort out the rest on the way'): [('mark', 'took a wild risk')],
 ('the offer to go further', 'say no, and stay home where the family needs the help'): [('mark', 'stayed home')],
 ('the offer to go further', 'ask for it to wait a year, until you are properly ready'): [('door',
                                                                                           'turned down a chance')],
 ('the offer to go further', 'turn it down, and let the big road go with no regrets'): [('lesson',
                                                                                         'not every road needs '
                                                                                         'taking')],
 ('the offer to go further', 'turn it down, and make the same chance some other way'): [('mark',
                                                                                         'turned down a chance')],
 ('the offer to go further', 'take it, and bring {friend} along for the road'): [('mark', 'left home')],
 ('the offer to go further', 'let it go with thanks, and keep the teacher who made it possible'): [('person',
                                                                                                    'mentor')],
 ('no way in at {aim.place}', "wait for next year's try, working steadily at {aim.round} meanwhile"): [('person',
                                                                                                        'teacher')],
 ('no way in at {aim.place}', 'try three ways in at once, {aim.round} among them, and keep the best'): [('lesson',
                                                                                                         'there are '
                                                                                                         'many ways '
                                                                                                         'in')],
 ('no way in at {aim.place}', 'go to {aim.round} and get noticed by whoever runs it'): [('person', 'patron')],
 ('no way in at {aim.place}', 'make your own way in: start something with whoever will join'): [('mark',
                                                                                                 'took a wild risk')],
 ('no way in at {aim.place}', 'let it go, and keep {aim.doing} as something for home'): [('mark', 'learned a skill')],
 ('no way in at {aim.place}', 'apply properly to {aim.round}, with every form filled in'): [('means', 'time-.03')],
 ('no way in at {aim.place}', 'let the old door go, and help {friend} start a small group at home'): [('place',
                                                                                                       'gather.circle')],
 ('no way in at {aim.place}', 'ask a teacher outside the family for quiet lessons'): [('person', 'mentor')],
 ('no way in at {aim.place}', 'put the work out where anyone at all can find it, and see who answers'): [('means',
                                                                                                          'freedom+.03')],
 ('no way in at {aim.place}', 'let {aim.doing} go for now, and keep the friends who were turned away too'): [('person',
                                                                                                              'friend')],
 ('what home makes of {aim.doing}', 'agree fair rules for the hours, and keep to them'): [('mark', 'kept your word')],
 ('what home makes of {aim.doing}', 'lay out a plan: hours, costs, and what happens if it does not work'): [('lesson',
                                                                                                             'a plan '
                                                                                                             'calms '
                                                                                                             'people')],
 ('what home makes of {aim.doing}', 'insist it is your life and your choice, and hold firm'): [('mark',
                                                                                                'defied an '
                                                                                                'authority')],
 ('what home makes of {aim.doing}', 'ask them to come and see the next showing before they decide'): [('lesson',
                                                                                                       'seeing it '
                                                                                                       'changes '
                                                                                                       'minds')],
 ('what home makes of {aim.doing}', "ease off for the family's sake, and keep it as a pastime"): [('means',
                                                                                                   'ties+.05')],
 ('what home makes of {aim.doing}', 'take the steady path they want, and keep {aim.doing} on the side'): [('mark',
                                                                                                           'gave in '
                                                                                                           'to '
                                                                                                           'pressure')],
 ('what home makes of {aim.doing}', 'promise one more year, and show results they can see'): [('door',
                                                                                               'kept your word')],
 ('what home makes of {aim.doing}', 'do it anyway, and let them find out at the next showing'): [('door',
                                                                                                  'kept it hidden')],
 ('what home makes of {aim.doing}', 'bring them into it: a whole day of {aim.doing} together'): [('means',
                                                                                                  'ties+.03')],
 ('what home makes of {aim.doing}', 'listen to the worry, and cut the hours they cannot bear'): [('means',
                                                                                                  'time+.03')],
 ('the night the people came', 'write a proper thank-you to everyone who helped along the way'): [('means',
                                                                                                   'ties+.04')],
 ('the night the people came', 'go home and begin the next piece that same night'): [('mark', 'learned a skill')],
 ('the night the people came', 'make sure the news reaches everyone who matters, today'): [('person', 'patron')],
 ('the night the people came', 'dance round the kitchen and tell everyone you meet'): [('means', 'freedom+.03')],
 ('the night the people came', 'keep it quiet, and share it with the family at home'): [('lesson',
                                                                                         'the family saw it all')],
 ('the night the people came', 'raise the standard again the very next morning'): [('means', 'time-.03')],
 ('the night the people came', 'treat the people from the very start to a meal'): [('means', 'money-.03')],
 ('the night the people came', 'go back to your first teacher and show them what came of it'): [('person', 'mentor')],
 ('the night the people came', 'ask the people who came what moved them, and write it down'): [('lesson',
                                                                                                'each one heard '
                                                                                                'something else')],
 ('the night the people came', "give the night's flowers to the youngest in the room"): [('mark',
                                                                                          'helped someone in need')],
 ("the first term's fee falls due", 'sign on for the full term, and turn up to every session it covers'): [('mark',
                                                                                                            'kept '
                                                                                                            'your '
                                                                                                            'word')],
 ("the first term's fee falls due", 'ask what the term actually teaches, and sign on only for the part that helps'): [('lesson',
                                                                                                                       'ask '
                                                                                                                       'what '
                                                                                                                       'it '
                                                                                                                       'covers')],
 ("the first term's fee falls due", 'sign on, and ask to be moved up to the stronger group straight away'): [('person',
                                                                                                              'rival')],
 ("the first term's fee falls due", 'skip the fee, and play for fun wherever a game turns up'): [('means',
                                                                                                  'freedom+.03')],
 ("the first term's fee falls due", "stop here, glad of the start, and keep the friends from the beginners' weeks"): [('person',
                                                                                                                       'friend')],
 ("the first term's fee falls due", 'sign on, and keep a notebook of every session to see what changes'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ("the first term's fee falls due", 'wait a term, and watch how the regulars do it before paying to join'): [('lesson',
                                                                                                              'watching '
                                                                                                              'teaches '
                                                                                                              'too')],
 ("the first term's fee falls due", 'sign on, and ask to be entered in {aim.contest} before the term is out'): [('mark',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ("the first term's fee falls due", 'sign on together with a friend, so neither of them drops out alone'): [('person',
                                                                                                             'friend')],
 ("the first term's fee falls due", 'let it go for now, and help out at {aim.place} on the open days instead'): [('mark',
                                                                                                                  'helped '
                                                                                                                  'someone '
                                                                                                                  'in '
                                                                                                                  'need')],
 ("the beginners' group moves up", 'move up with the group as planned, and keep to every session'): [('mark',
                                                                                                      'kept your '
                                                                                                      'word')],
 ("the beginners' group moves up", 'ask to stay with the newcomers a few more weeks, and move up when ready'): [('lesson',
                                                                                                                 'ready '
                                                                                                                 'beats '
                                                                                                                 'early')],
 ("the beginners' group moves up", 'move up, and pick out the best one there to measure against'): [('person',
                                                                                                     'rival')],
 ("the beginners' group moves up", 'try one session at the harder level, and decide on the spot'): [('lesson',
                                                                                                     'try it before '
                                                                                                     'deciding')],
 ("the beginners' group moves up", 'let it go before it stops being fun, and keep in touch with the group'): [('person',
                                                                                                               'friend')],
 ("the beginners' group moves up", 'move up, and do the extra drills the main group expects of newcomers'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ("the beginners' group moves up", 'find another place where beginners keep a session of their own'): [('place',
                                                                                                        'gather.games')],
 ("the beginners' group moves up", 'move up, but only every other week, and practise at home in between'): [('means',
                                                                                                             'time+.04')],
 ("the beginners' group moves up", 'move up, and make a point of welcoming the next beginner through the door'): [('mark',
                                                                                                                   'helped '
                                                                                                                   'someone '
                                                                                                                   'in '
                                                                                                                   'need')],
 ("the beginners' group moves up", 'stop, and take what the first weeks taught into something calmer'): [('lesson',
                                                                                                          'a start '
                                                                                                          'is never '
                                                                                                          'wasted')],
 ('the first real piece comes out wrong', 'order the materials, and make the same piece again, step by step as taught'): [('mark',
                                                                                                                           'learned '
                                                                                                                           'a '
                                                                                                                           'skill')],
 ('the first real piece comes out wrong', 'take the spoiled piece apart, and find exactly where it went wrong'): [('lesson',
                                                                                                                   'the '
                                                                                                                   'mistake '
                                                                                                                   'shows '
                                                                                                                   'the '
                                                                                                                   'way')],
 ('the first real piece comes out wrong', 'ask the best hand at {aim.place} to look at it and say what is wrong'): [('person',
                                                                                                                     'mentor')],
 ('the first real piece comes out wrong', 'start something completely different, just to get the fun of it back'): [('means',
                                                                                                                     'freedom+.03')],
 ('the first real piece comes out wrong', 'leave the order for a month, and let the disappointment settle first'): [('lesson',
                                                                                                                     'disappointment '
                                                                                                                     'settles '
                                                                                                                     'with '
                                                                                                                     'time')],
 ('the first real piece comes out wrong', 'make the next piece smaller and simpler, and get one thing right'): [('lesson',
                                                                                                                 'small '
                                                                                                                 'and '
                                                                                                                 'right '
                                                                                                                 'first')],
 ('the first real piece comes out wrong', 'let it go, and keep the eye for good work that it trained'): [('lesson',
                                                                                                          'a trained '
                                                                                                          'eye '
                                                                                                          'stays')],
 ('the first real piece comes out wrong', 'keep the crooked piece in plain sight, and beat it on the next try'): [('lesson',
                                                                                                                   'pride '
                                                                                                                   'can '
                                                                                                                   'be '
                                                                                                                   'a '
                                                                                                                   'spur')],
 ('the first real piece comes out wrong', 'stop for good, and give the crooked piece to someone who will like it anyway'): [('person',
                                                                                                                             'friend')],
 ('the first real piece comes out wrong', 'go on, but only in the class sessions, with no extra hours at home'): [('means',
                                                                                                                   'time+.03')],
 ('the weeks of nothing but the basics', 'sign up again, and do the plain work as carefully as the rest'): [('mark',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the weeks of nothing but the basics', 'ask what each plain exercise is for, and practise with that in mind'): [('lesson',
                                                                                                                   'every '
                                                                                                                   'drill '
                                                                                                                   'has '
                                                                                                                   'a '
                                                                                                                   'reason')],
 ('the weeks of nothing but the basics', 'turn the basics into a race, and be the quickest clean hand in the group'): [('person',
                                                                                                                        'rival')],
 ('the weeks of nothing but the basics', 'make something small and real at home on the side, to keep the spark'): [('mark',
                                                                                                                    'learned '
                                                                                                                    'a '
                                                                                                                    'skill')],
 ('the weeks of nothing but the basics', 'let it go, and keep the few plain skills for mending things at home'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('the weeks of nothing but the basics', 'sign up, and ask the teacher for a harder version of each exercise'): [('person',
                                                                                                                  'mentor')],
 ('the weeks of nothing but the basics', 'find a teacher who teaches the basics through real pieces'): [('person',
                                                                                                         'teacher')],
 ('the weeks of nothing but the basics', "skip a term, and come back when the household's weeks are less full"): [('means',
                                                                                                                   'time+.04')],
 ('the weeks of nothing but the basics', 'stop for good, and teach a younger one the bits already learned'): [('mark',
                                                                                                               'helped '
                                                                                                               'someone '
                                                                                                               'in '
                                                                                                               'need')],
 ('the weeks of nothing but the basics', 'keep at it slowly, one session a week, and stop worrying about the pace'): [('lesson',
                                                                                                                       'slow '
                                                                                                                       'still '
                                                                                                                       'gets '
                                                                                                                       'there')],
 ('the first piece turned away', "read the call's rules again, and send the next piece exactly as asked"): [('lesson',
                                                                                                             'read '
                                                                                                             'the '
                                                                                                             'rules '
                                                                                                             'first')],
 ('the first piece turned away', 'ask the ones who said no what would have made it a yes'): [('person', 'mentor')],
 ('the first piece turned away', 'send it somewhere bigger, to prove the first lot wrong'): [('mark',
                                                                                              'took a wild risk')],
 ('the first piece turned away', 'make something new and bolder for the next call, straight away'): [('lesson',
                                                                                                      'new work '
                                                                                                      'answers '
                                                                                                      'best')],
 ('the first piece turned away', 'keep making things for friends and family, and skip the calls for a while'): [('means',
                                                                                                                 'ties+.03')],
 ('the first piece turned away', 'keep a file of every piece sent and every answer, and learn from the pattern'): [('mark',
                                                                                                                    'learned '
                                                                                                                    'a '
                                                                                                                    'skill')],
 ('the first piece turned away', 'study the pieces that were taken, and work out what they had'): [('lesson',
                                                                                                    'see what gets '
                                                                                                    'chosen')],
 ('the first piece turned away', 'stop sending work out, and make things only for the fun of it'): [('means',
                                                                                                     'freedom+.03')],
 ('the first piece turned away', 'let it go for good, and keep the friends made at the first show'): [('person',
                                                                                                       'friend')],
 ('the first piece turned away', 'stop for now, and keep the habit of looking closely that it gave'): [('lesson',
                                                                                                        'looking '
                                                                                                        'closely is '
                                                                                                        'kept')],
 ('when practice stops being new', 'book the next block, and keep a set time each day for practice'): [('mark',
                                                                                                        'kept your '
                                                                                                        'word')],
 ('when practice stops being new', 'ask the teacher for pieces that are hard in a new way'): [('person', 'teacher')],
 ('when practice stops being new', 'set a goal: one piece played or shown in public before the year is out'): [('lesson',
                                                                                                                'a '
                                                                                                                'goal '
                                                                                                                'pulls '
                                                                                                                'hard')],
 ('when practice stops being new', 'drop the set pieces, and play or make whatever comes, for a month'): [('means',
                                                                                                           'freedom+.03')],
 ('when practice stops being new', 'stop the lessons, and keep {aim.doing} as a small thing at home'): [('means',
                                                                                                         'ties+.03')],
 ('when practice stops being new', 'book the lessons, and practise with a chart until it is habit again'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('when practice stops being new', 'find a group to do it with, so it stops being a lonely hour'): [('place',
                                                                                                     'gather.circle')],
 ('when practice stops being new', 'stop for good, and keep the ear and the hands it trained'): [('mark',
                                                                                                  'learned a skill')],
 ('when practice stops being new', "stop, and spend the hours helping at the school's or the street's shows"): [('mark',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('when practice stops being new', 'take a term off, and come back to it if it is missed'): [('lesson',
                                                                                              'missing it tells the '
                                                                                              'truth')],
 ('the chapter that will not go in', 'go back to the start of the hard part, and work through it in order'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the chapter that will not go in', 'find a different explanation of the same thing, from another book or teacher'): [('lesson',
                                                                                                                        'another '
                                                                                                                        'way '
                                                                                                                        'in '
                                                                                                                        'exists')],
 ('the chapter that will not go in', 'ask the cleverest one in the group to explain it, and trade help for help'): [('lesson',
                                                                                                                     'help '
                                                                                                                     'is '
                                                                                                                     'worth '
                                                                                                                     'trading')],
 ('the chapter that will not go in', 'skip ahead to the parts that are fun, and come back to it later'): [('means',
                                                                                                           'freedom+.03')],
 ('the chapter that will not go in', 'stop here, and keep the curiosity for reading in a gentler way'): [('lesson',
                                                                                                          'curiosity '
                                                                                                          'does not '
                                                                                                          'need '
                                                                                                          'tests')],
 ('the chapter that will not go in', 'ask the teacher for extra time after the lesson, and bring every question'): [('person',
                                                                                                                     'teacher')],
 ('the chapter that will not go in', 'let it go, and keep the habit of hard thinking for something else'): [('lesson',
                                                                                                             'hard '
                                                                                                             'thinking '
                                                                                                             'travels '
                                                                                                             'well')],
 ('the chapter that will not go in', 'sit the test anyway, and use whatever comes back as a map'): [('mark',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('the chapter that will not go in', 'study it with a friend, out loud, until it makes sense to both'): [('person',
                                                                                                          'friend')],
 ('the chapter that will not go in', 'slow down, take the test next time round, and learn it properly'): [('means',
                                                                                                           'health+.02')],
 ('the first marked work comes back', 'read every comment, put each one right, and hand the work in again anyway'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the first marked work comes back', 'work out which mistakes were understanding and which were carelessness'): [('lesson',
                                                                                                                   'know '
                                                                                                                   'which '
                                                                                                                   'mistake '
                                                                                                                   'it '
                                                                                                                   'was')],
 ('the first marked work comes back', 'go on to the next part, and set out to beat the top mark'): [('person',
                                                                                                     'rival')],
 ('the first marked work comes back', 'change the way of studying completely: new hours, new place, new method'): [('place',
                                                                                                                    'learn.keeping')],
 ('the first marked work comes back', 'stop the course, and keep the subject as something to read about at leisure'): [('lesson',
                                                                                                                        'interest '
                                                                                                                        'outlives '
                                                                                                                        'the '
                                                                                                                        'marks')],
 ('the first marked work comes back', 'ask the teacher what a good mark looks like, then work to that'): [('person',
                                                                                                           'teacher')],
 ('the first marked work comes back', 'let it go, and take the method it taught to a subject that fits better'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('the first marked work comes back', 'go on, but take the next part more slowly, over two terms instead of one'): [('means',
                                                                                                                     'time+.04')],
 ('the first marked work comes back', 'go on, and start a study group for the others who did badly too'): [('mark',
                                                                                                            'helped '
                                                                                                            'someone '
                                                                                                            'in '
                                                                                                            'need')],
 ('the first marked work comes back', 'put the next part off a term, and read around the subject meanwhile'): [('means',
                                                                                                                'health+.02')],
 ('the end of the trial months', 'accept the offer, and learn the rules of the place properly'): [('mark',
                                                                                                   'kept your word')],
 ('the end of the trial months', 'ask what the next year would actually teach, and decide on the answer'): [('lesson',
                                                                                                             'ask '
                                                                                                             'what '
                                                                                                             'it '
                                                                                                             'teaches')],
 ('the end of the trial months', 'accept, but ask for one real task to carry alone'): [('person', 'boss')],
 ('the end of the trial months', 'turn it down, and try another kind of work before settling on one'): [('lesson',
                                                                                                         'a first '
                                                                                                         'job '
                                                                                                         'teaches '
                                                                                                         'anyway')],
 ('the end of the trial months', 'stay on, but ask for hours that leave room for home'): [('means', 'time+.04')],
 ('the end of the trial months', 'accept, and keep a notebook of how the senior people do things'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the end of the trial months', 'stay, and quietly learn which jobs lead somewhere and which do not'): [('person',
                                                                                                          'colleague')],
 ('the end of the trial months', 'stay only if the dull jobs come with something new each month'): [('lesson',
                                                                                                     'ask and it may '
                                                                                                     'come')],
 ('the end of the trial months', 'leave on good terms, and keep the friend made on the first day'): [('person',
                                                                                                      'friend')],
 ('the end of the trial months', "ask to start the full post after the season's family duties are done"): [('means',
                                                                                                            'ties+.03')],
 ('the week of the first review', 'go in prepared, with a list of what was done and what comes next'): [('lesson',
                                                                                                         'a list '
                                                                                                         'speaks '
                                                                                                         'well')],
 ('the week of the first review', 'ask in the review for a new task, one that would teach something'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the week of the first review', 'ask in the review for more pay or a better title, and say why'): [('means',
                                                                                                      'money+.04')],
 ('the week of the first review', 'say plainly in the review that the work has gone dull, and see what is offered'): [('lesson',
                                                                                                                       'plain '
                                                                                                                       'words '
                                                                                                                       'open '
                                                                                                                       'doors')],
 ('the week of the first review', 'ask to drop to fewer days, and keep the job without the push'): [('means',
                                                                                                     'time+.05')],
 ('the week of the first review', 'take on the extra work everyone avoids, and say so at the review'): [('person',
                                                                                                         'boss')],
 ('the week of the first review', 'quietly look for another post in the same line of work'): [('lesson',
                                                                                               'the line matters, '
                                                                                               'not the place')],
 ('the week of the first review', 'ask for the review to be put back a season, and settle in first'): [('means',
                                                                                                        'health+.03')],
 ('the week of the first review', 'hand in notice after the review, and try something that feels more useful'): [('lesson',
                                                                                                                  'knowing '
                                                                                                                  'what '
                                                                                                                  'bores '
                                                                                                                  'is '
                                                                                                                  'useful')],
 ('the week of the first review', 'stop after the review, and use the spare hours to work out what fits'): [('person',
                                                                                                             'colleague')],
 ('the group asks for a regular hand', 'take the regular job, and keep to it every week as promised'): [('mark',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('the group asks for a regular hand', 'ask what the job really involves before saying yes or no'): [('lesson',
                                                                                                      'ask before '
                                                                                                      'saying yes')],
 ('the group asks for a regular hand', 'take it, and push to have a say in what the group does next'): [('person',
                                                                                                         'rival')],
 ('the group asks for a regular hand', 'stay a helper for the big days only, and skip the weekly grind'): [('means',
                                                                                                            'freedom+.03')],
 ('the group asks for a regular hand', 'step back, glad to have helped once, and keep the people met'): [('person',
                                                                                                          'friend')],
 ('the group asks for a regular hand', 'take the job, and write down how it is done so others can follow'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('the group asks for a regular hand', 'offer a smaller job that fits the week, and do it well'): [('means',
                                                                                                    'time+.03')],
 ('the group asks for a regular hand', 'take it on, and start something bolder than the group has tried'): [('mark',
                                                                                                             'took a '
                                                                                                             'wild '
                                                                                                             'risk')],
 ('the group asks for a regular hand', 'share the job with a friend, so it stays fun for both'): [('person',
                                                                                                   'friend')],
 ('the group asks for a regular hand', 'stop, and give the hours to a neighbour who needs them more'): [('mark',
                                                                                                         'helped '
                                                                                                         'someone in '
                                                                                                         'need')],
 ('the first petition sent back', 'go to the next meeting, and help redraft the request by the proper rules'): [('person',
                                                                                                                 'colleague')],
 ('the first petition sent back', 'find out exactly why it was refused, and who decided'): [('lesson',
                                                                                             'find who decides')],
 ('the first petition sent back', 'go back with more names behind it, so it cannot be ignored'): [('means',
                                                                                                   'ties+.04')],
 ('the first petition sent back', 'make the refusal public, loudly, and see who joins'): [('mark',
                                                                                           'defied an authority')],
 ('the first petition sent back', 'stop chasing the big ask, and help one person nearby instead'): [('mark',
                                                                                                     'helped someone '
                                                                                                     'in need')],
 ('the first petition sent back', 'go on, and take the slow official route all the way up'): [('lesson',
                                                                                               'the slow route still '
                                                                                               'arrives')],
 ('the first petition sent back', 'try a different way in altogether: a new group, a new door'): [('place',
                                                                                                   'rule.voice')],
 ('the first petition sent back', 'take a season off from it, and come back with fresh strength'): [('means',
                                                                                                     'health+.03')],
 ('the first petition sent back', 'stop for now, and keep in touch with the ones who stood up alongside'): [('person',
                                                                                                             'friend')],
 ('the first petition sent back', 'stay in the group, but only to listen and learn for now'): [('mark',
                                                                                                'learned a skill')],
 ('the lease with more than one name on it', 'sign, and set out together in writing who pays for what'): [('mark',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the lease with more than one name on it', 'talk it through properly first: money, chores, what each expects'): [('lesson',
                                                                                                                    'say '
                                                                                                                    'it '
                                                                                                                    'before '
                                                                                                                    'signing')],
 ('the lease with more than one name on it', "sign, but keep an account and a room that are only one's own"): [('means',
                                                                                                                'freedom+.03')],
 ('the lease with more than one name on it', 'skip the lease for now, and share the place a few months to see'): [('lesson',
                                                                                                                   'trying '
                                                                                                                   'first '
                                                                                                                   'is '
                                                                                                                   'fair')],
 ('the lease with more than one name on it', 'sign, and ask family and friends round to the new place the first weekend'): [('means',
                                                                                                                             'ties+.04')],
 ('the lease with more than one name on it', 'sign for six months instead of a year, and review it honestly then'): [('lesson',
                                                                                                                      'a '
                                                                                                                      'short '
                                                                                                                      'promise '
                                                                                                                      'first')],
 ('the lease with more than one name on it', 'let it go gently, and say clearly why, so everyone can move on'): [('lesson',
                                                                                                                  'knowing '
                                                                                                                  'what '
                                                                                                                  'is '
                                                                                                                  'wanted')],
 ('the lease with more than one name on it', 'sign straight away, and pick the bolder place across town'): [('mark',
                                                                                                             'took a '
                                                                                                             'wild '
                                                                                                             'risk')],
 ('the lease with more than one name on it', 'wait until the end of the summer, and keep the easy months a little longer'): [('means',
                                                                                                                              'ties+.03')],
 ('the lease with more than one name on it', 'step back from the lease, and stay on good terms with the others'): [('person',
                                                                                                                    'friend')],
 ('the rota nobody keeps', 'bring a fair rota to the talk, and be the first to keep it'): [('mark',
                                                                                            'kept your word')],
 ('the rota nobody keeps', 'work out where the money and hours actually go, and bring the figures'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('the rota nobody keeps', "take charge of the household's money, and run it tightly"): [('means', 'money+.04')],
 ('the rota nobody keeps', 'skip the rota, and turn the chores into one loud evening a week'): [('means',
                                                                                                 'ties+.03')],
 ('the rota nobody keeps', 'ease off the plans for now, and just look after each other through the winter'): [('means',
                                                                                                               'health+.03')],
 ('the rota nobody keeps', 'agree house rules at the talk, and see that everyone keeps them'): [('lesson',
                                                                                                 'rules need someone '
                                                                                                 'keeping them')],
 ('the rota nobody keeps', 'try a different setup: separate shelves, separate bills, shared meals'): [('lesson',
                                                                                                       'shared does '
                                                                                                       'not mean '
                                                                                                       'everything')],
 ('the rota nobody keeps', 'slow the big plans by a year, and get the everyday running first'): [('means',
                                                                                                  'time+.04')],
 ('the rota nobody keeps', 'admit it is not working, and part on fair terms before it sours'): [('lesson',
                                                                                                 'living together '
                                                                                                 'shows people')],
 ('the rota nobody keeps', 'let this household go, and keep the friendship it started with'): [('person', 'friend')],
 ('the first winter on the plot', 'pay the rent, and keep the winter jobs on the list, week by week'): [('mark',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('the first winter on the plot', "use the bare months to read up, and plan next year's ground properly"): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('the first winter on the plot', 'take on the empty plot next door too, while it is going cheap'): [('means',
                                                                                                      'money-.04')],
 ('the first winter on the plot', 'try something new for winter: a cold frame, a hardy crop, an odd idea'): [('lesson',
                                                                                                              'winter '
                                                                                                              'still '
                                                                                                              'grows '
                                                                                                              'things')],
 ('the first winter on the plot', 'come only on mild days, and let the ground rest as it does in winter'): [('means',
                                                                                                             'health+.03')],
 ('the first winter on the plot', 'ask the old hands which winter jobs matter, and do those first'): [('person',
                                                                                                       'mentor')],
 ('the first winter on the plot', 'give up the plot, and grow a little at home with what was learned'): [('lesson',
                                                                                                          'small '
                                                                                                          'ground '
                                                                                                          'still '
                                                                                                          'teaches')],
 ('the first winter on the plot', 'keep it, and set out to have the best plot on the row by summer'): [('person',
                                                                                                        'rival')],
 ('the first winter on the plot', 'share the plot with a friend, half the work and twice the company'): [('person',
                                                                                                          'friend')],
 ('the first winter on the plot', 'hand the plot on to someone on the waiting list, and help them start'): [('mark',
                                                                                                             'helped '
                                                                                                             'someone '
                                                                                                             'in '
                                                                                                             'need')],
 ("the first season's losses", 'start again on the same plan, and do each step more carefully'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ("the first season's losses", 'find out exactly what went wrong, and change only that'): [('lesson',
                                                                                            'find the one cause')],
 ("the first season's losses", 'double the effort this season, and leave nothing to chance'): [('means',
                                                                                                'health-.03')],
 ("the first season's losses", 'try something different altogether next season, and see what takes'): [('lesson',
                                                                                                        'trying '
                                                                                                        'things '
                                                                                                        'shows what '
                                                                                                        'works')],
 ("the first season's losses", 'start smaller, with only what did well, and go gently'): [('means', 'time+.03')],
 ("the first season's losses", 'join the local society, and follow the methods of its best old hands'): [('place',
                                                                                                          'prod.land')],
 ("the first season's losses", 'let it go, and take what was learned into some other outdoor work'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ("the first season's losses", 'skip a season, and come back when there is time to do it well'): [('means',
                                                                                                   'time+.04')],
 ("the first season's losses", 'go on, and share the failures openly with the other beginners'): [('person',
                                                                                                   'friend')],
 ("the first season's losses", 'stop, and keep the eye for weather and seasons that the year gave'): [('lesson',
                                                                                                       'weather is '
                                                                                                       'read '
                                                                                                       'slowly')],
 ("the newcomers' welcome comes to an end", 'join the course, and keep the early mornings as asked'): [('mark',
                                                                                                        'kept your '
                                                                                                        'word')],
 ("the newcomers' welcome comes to an end", 'ask to sit in on a session first, and decide after'): [('lesson',
                                                                                                     'see it before '
                                                                                                     'joining')],
 ("the newcomers' welcome comes to an end", 'join, and ask for a teacher who will push hard'): [('person', 'mentor')],
 ("the newcomers' welcome comes to an end", 'keep coming to the gatherings, but skip the course and the set hours'): [('means',
                                                                                                                       'freedom+.03')],
 ("the newcomers' welcome comes to an end", 'join, and bring along someone who has been lonely lately'): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ("the newcomers' welcome comes to an end", 'join, and keep a quiet notebook of the questions it raises'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ("the newcomers' welcome comes to an end", 'step away, and keep the habit of stillness it taught'): [('lesson',
                                                                                                       'stillness '
                                                                                                       'can be '
                                                                                                       'kept')],
 ("the newcomers' welcome comes to an end", 'join, and go at it with everything for the first season'): [('means',
                                                                                                          'time-.04')],
 ("the newcomers' welcome comes to an end", 'let it go, but keep up with the friend who first brought the invitation'): [('person',
                                                                                                                          'friend')],
 ("the newcomers' welcome comes to an end", 'look for a quieter group nearby whose ways suit the week better'): [('place',
                                                                                                                  'faith.congregation')],
 ('the mornings that feel empty', 'keep the practice exactly, and go on the retreat as promised'): [('mark',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('the mornings that feel empty', 'talk the emptiness through with an older one who has felt it too'): [('person',
                                                                                                         'mentor')],
 ('the mornings that feel empty', 'go on the retreat, and set out to come back changed'): [('lesson',
                                                                                            'some things come '
                                                                                            'unforced')],
 ('the mornings that feel empty', 'try a different practice for a while: walking, music, silence outdoors'): [('means',
                                                                                                               'health+.03')],
 ('the mornings that feel empty', 'give up the retreat place, and keep a small practice at home for now'): [('means',
                                                                                                             'time+.03')],
 ('the mornings that feel empty', 'go on the retreat, and take on the hardest of its disciplines'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('the mornings that feel empty', 'let it go, and keep looking for meaning in other places'): [('lesson',
                                                                                                'the search goes '
                                                                                                'on')],
 ('the mornings that feel empty', 'put the retreat off a year, and give the practice time to come back'): [('lesson',
                                                                                                            'flat '
                                                                                                            'weeks '
                                                                                                            'do '
                                                                                                            'pass')],
 ('the mornings that feel empty', 'stop for now, and give the morning hour to helping at the shelter'): [('mark',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('the mornings that feel empty', 'go on the retreat with a friend, and talk it all over after'): [('person',
                                                                                                    'friend')],
 ('home from the first hard outing', 'go again, after a proper course on safety and finding the way'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('home from the first hard outing', 'go over what went wrong with the group, and change the plan'): [('lesson',
                                                                                                       'the weak '
                                                                                                       'point '
                                                                                                       'shows')],
 ('home from the first hard outing', 'go again, and lead this time, to be sure it is done right'): [('lesson',
                                                                                                     'leading weighs '
                                                                                                     'more')],
 ('home from the first hard outing', 'go again straight away, before the fear has time to set'): [('mark',
                                                                                                   'took a wild '
                                                                                                   'risk')],
 ('home from the first hard outing', 'stay home this time, and go next season when it feels right'): [('means',
                                                                                                       'health+.03')],
 ('home from the first hard outing', 'go again on an easier route, and build up from there step by step'): [('lesson',
                                                                                                             'easier '
                                                                                                             'first, '
                                                                                                             'then '
                                                                                                             'harder')],
 ('home from the first hard outing', 'stop, and keep the hard-won knack for reading weather and maps'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('home from the first hard outing', 'go again, with better gear and a harder route to prove the point'): [('means',
                                                                                                            'money-.04')],
 ('home from the first hard outing', 'let it go, and keep the friends made on that hard first trip'): [('person',
                                                                                                        'friend')],
 ('home from the first hard outing', 'go again, but only with the seasoned group that looks after newcomers'): [('place',
                                                                                                                 'gather.circle')],
 ('the deposit on the first big trip', 'pay the deposit from savings set aside for it, and plan every day'): [('means',
                                                                                                               'money-.06')],
 ('the deposit on the first big trip', 'find a cheaper way to do the same trip, and pay for that'): [('lesson',
                                                                                                      'cheaper is '
                                                                                                      'not worse')],
 ('the deposit on the first big trip', 'pay, and stretch it into a longer, bigger trip than planned'): [('means',
                                                                                                         'money-.10')],
 ('the deposit on the first big trip', 'pay tonight, before there is time to think better of it'): [('mark',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('the deposit on the first big trip', 'put the big trip off a year, and keep the small outings close to home'): [('means',
                                                                                                                   'ties+.03')],
 ('the deposit on the first big trip', 'pay, and take extra work to cover it before leaving'): [('means',
                                                                                                 'time-.05')],
 ('the deposit on the first big trip', 'let the deposit go, and spend the money learning a new skill instead'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('the deposit on the first big trip', 'ask the family to help with the deposit, and promise to bring them along next time'): [('person',
                                                                                                                                'parent')],
 ('the deposit on the first big trip', 'stop the plans, and put the saved money toward what the household needs'): [('lesson',
                                                                                                                     'the '
                                                                                                                     'road '
                                                                                                                     'will '
                                                                                                                     'wait')],
 ('the deposit on the first big trip', 'take a shorter trip this year instead, and learn from that first'): [('lesson',
                                                                                                              'short '
                                                                                                              'trips '
                                                                                                              'teach '
                                                                                                              'first')],
 ('an ordinary week in the household', 'keep the shared meal to its day and its hour, however tired everyone is'): [('door',
                                                                                                                     'kept '
                                                                                                                     'your '
                                                                                                                     'word')],
 ('an ordinary week in the household', 'ask everyone what the week needs, and fix the part that keeps going wrong'): [('lesson',
                                                                                                                       'asking '
                                                                                                                       'first '
                                                                                                                       'saves '
                                                                                                                       'arguments')],
 ('an ordinary week in the household', 'take one job at home and make it plainly their own'): [('means', 'time-.03')],
 ('an ordinary week in the household', 'turn a dull evening into a game night, and ask {friend} round'): [('means',
                                                                                                           'ties+.04')],
 ('an ordinary week in the household', 'help {grandparent} do things the way they always did'): [('lesson',
                                                                                                  'the old way has '
                                                                                                  'its reasons')],
 ('an ordinary week in the household', "write the household's jobs on a list by the door, and keep to it"): [('means',
                                                                                                              'time+.03')],
 ('an ordinary week in the household', 'learn the one repair that everyone else at home avoids'): [('mark',
                                                                                                    'learned a '
                                                                                                    'skill')],
 ('an ordinary week in the household', 'strike a deal to swap the dull job for the fun one, this week only'): [('means',
                                                                                                                'freedom+.03')],
 ('an ordinary week in the household', 'bring everyone outside for the evening, whatever the weather'): [('means',
                                                                                                          'ties+.03')],
 ('an ordinary week in the household', 'let the week run itself for once, and just be part of it'): [('means',
                                                                                                      'health+.03')],
 ('the long table, years on', 'keep every birthday, call and gathering on its date, as always'): [('door',
                                                                                                   'kept your word')],
 ('the long table, years on', 'write down how the household runs, so it does not live only in one head'): [('lesson',
                                                                                                            'written '
                                                                                                            'ways '
                                                                                                            'outlast '
                                                                                                            'memory')],
 ('the long table, years on', 'ask the grown ones to take a fixed share, and hold them to it'): [('means',
                                                                                                  'ties-.03')],
 ('the long table, years on', 'throw a gathering for no reason at all, and fill the house'): [('means', 'money-.04'),
                                                                                              ('person', 'friend')],
 ('the long table, years on', "hand one of the family's ways to {child}, slowly, by doing it together"): [('means',
                                                                                                           'ties+.04')],
 ('the long table, years on', "set the family's calendar for the year and give everyone their part"): [('means',
                                                                                                        'freedom-.03')],
 ('the long table, years on', 'try a new way of meeting, a trip together instead of the same table'): [('means',
                                                                                                        'money-.05')],
 ('the long table, years on', 'let the grown children host this year, and keep your hands off'): [('means',
                                                                                                   'time+.05')],
 ('the long table, years on', 'step back for a season and let the house be quieter'): [('means', 'health+.04')],
 ('the long table, years on', 'sit with the oldest ones and learn what they still remember'): [('person', 'elder')],
 ('when {aim.contest} comes to the household', 'draw up a strict budget together, and everyone keeps to it'): [('means',
                                                                                                                'money+.04')],
 ('when {aim.contest} comes to the household', 'look into every grant, swap and saving there is, and use them'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('when {aim.contest} comes to the household', 'take on extra work and carry the household through yourself'): [('means',
                                                                                                                 'money+.05'),
                                                                                                                ('means',
                                                                                                                 'health-.04')],
 ('when {aim.contest} comes to the household', 'keep spirits up with music, games and a feast made of almost nothing'): [('means',
                                                                                                                          'ties+.05')],
 ('when {aim.contest} comes to the household', 'ask the neighbours and the wider family to pool what they have'): [('person',
                                                                                                                    'neighbour')],
 ('when {aim.contest} comes to the household', 'sit everyone down and plan the months ahead, week by week'): [('lesson',
                                                                                                               'a '
                                                                                                               'plan '
                                                                                                               'calms '
                                                                                                               'a '
                                                                                                               'house')],
 ('when {aim.contest} comes to the household', 'sell what the household can spare, and drive a hard bargain'): [('means',
                                                                                                                 'money+.05')],
 ('when {aim.contest} comes to the household', 'keep the trouble to yourself and act as if all is well'): [('door',
                                                                                                            'kept it '
                                                                                                            'hidden')],
 ('when {aim.contest} comes to the household', 'take everyone to stay with the wider family for the worst weeks'): [('means',
                                                                                                                     'money+.03')],
 ('when {aim.contest} comes to the household', 'keep your head down, keep things as they are, and let it pass'): [('lesson',
                                                                                                                   'hard '
                                                                                                                   'seasons '
                                                                                                                   'do '
                                                                                                                   'pass')],
 ('the season the whole family is tested', 'call the family together and share out the care fairly, on a rota'): [('door',
                                                                                                                   'kept '
                                                                                                                   'your '
                                                                                                                   'word')],
 ('the season the whole family is tested', 'find out every kind of help there is, and get the right one in'): [('place',
                                                                                                                'care.houses')],
 ('the season the whole family is tested', 'take the decisions yourself, quickly, and answer for them'): [('means',
                                                                                                           'time-.05')],
 ('the season the whole family is tested', 'move everyone in together for the season and make it loud and warm'): [('means',
                                                                                                                    'ties+.06'),
                                                                                                                   ('means',
                                                                                                                    'freedom-.04')],
 ('the season the whole family is tested', 'take the oldest one in, and do the caring as it was once done for them'): [('mark',
                                                                                                                        'helped '
                                                                                                                        'someone '
                                                                                                                        'in '
                                                                                                                        'need')],
 ('the season the whole family is tested', 'set the rules for the shared house, and see that they are kept'): [('means',
                                                                                                                'ties-.03')],
 ('the season the whole family is tested', 'let the crisis run its course, and step in only where you are needed'): [('means',
                                                                                                                      'health+.03')],
 ('the season the whole family is tested', 'pay for help from outside so the family can stay a family'): [('means',
                                                                                                           'money-.08')],
 ('the season the whole family is tested', 'say plainly you cannot carry it this time, and ask someone else to lead'): [('means',
                                                                                                                         'time+.04')],
 ('the season the whole family is tested', 'let each branch of the family handle its own part, and trust them'): [('lesson',
                                                                                                                   'trust '
                                                                                                                   'lets '
                                                                                                                   'others '
                                                                                                                   'step '
                                                                                                                   'up')],
 ('the one who has kept a household before', 'ask how they did it, and follow the advice to the letter for a year'): [('person',
                                                                                                                       'mentor')],
 ('the one who has kept a household before', 'listen to everything, then keep only what fits your own house'): [('lesson',
                                                                                                                 'take '
                                                                                                                 'advice, '
                                                                                                                 'keep '
                                                                                                                 'judgement')],
 ('the one who has kept a household before', 'ask them to put in a word where it will open doors for the family'): [('person',
                                                                                                                     'patron')],
 ('the one who has kept a household before', 'invite them round and let the house speak for itself'): [('person',
                                                                                                        'friend')],
 ('the one who has kept a household before', 'visit them every week, and help with whatever they are doing'): [('mark',
                                                                                                                'helped '
                                                                                                                'someone '
                                                                                                                'in '
                                                                                                                'need')],
 ('the one who has kept a household before', "ask them to sit down over the family's plans and accounts together"): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the one who has kept a household before', 'trade what you are good at for what they know'): [('person', 'mentor')],
 ('the one who has kept a household before', 'thank them, and keep their number for a harder day'): [('door',
                                                                                                      'turned down a '
                                                                                                      'chance')],
 ('the one who has kept a household before', 'bring the whole house along, and make an afternoon of it'): [('means',
                                                                                                            'ties+.04')],
 ('the one who has kept a household before', 'take things slower, the way they wish they had at your age'): [('means',
                                                                                                              'health+.03')],
 ('the other branch of the family', 'propose taking turns, year by year, and write it down'): [('door',
                                                                                                'kept your word')],
 ('the other branch of the family', 'find out through someone they trust what {rival} really wants from it'): [('person',
                                                                                                                'go-between')],
 ('the other branch of the family', 'make your gathering the one nobody will want to miss'): [('means', 'money-.05')],
 ('the other branch of the family', 'have it out with {rival} face to face, and clear the air'): [('lesson',
                                                                                                   'saying it aloud '
                                                                                                   'clears the air')],
 ('the other branch of the family', 'let them have it this year, and keep the peace'): [('mark',
                                                                                         'gave in to pressure')],
 ('the other branch of the family', 'invite {rival} to run it together, and share the credit'): [('means',
                                                                                                  'ties+.04')],
 ('the other branch of the family', 'start a new day of your own that does not compete with theirs'): [('means',
                                                                                                        'freedom+.03')],
 ('the other branch of the family', 'win over the oldest of the family first, and the rest will follow'): [('person',
                                                                                                            'elder')],
 ('the other branch of the family', 'go to theirs with good grace, and bring the best dish'): [('means', 'ties+.05')],
 ('the other branch of the family', 'hold a smaller gathering of your own, the way you like it'): [('place',
                                                                                                    'gather.house')],
 ('the hope that does not come this year', 'pick the plan up where it broke, and start again on the same lines'): [('door',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ('the hope that does not come this year', 'work out what went wrong, and what can be different next time'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the hope that does not come this year', 'push harder, find another way in, and do not wait'): [('means',
                                                                                                   'time-.05')],
 ('the hope that does not come this year', 'get away for a few days, then come back to it with fresh eyes'): [('means',
                                                                                                               'freedom+.03')],
 ('the hope that does not come this year', 'lean on the people closest, and let them carry some of it'): [('means',
                                                                                                           'ties+.05')],
 ('the hope that does not come this year', 'ask someone who has been through the same how they went on'): [('place',
                                                                                                            'gather.talk')],
 ('the hope that does not come this year', 'set a new, smaller goal for this year that can really be reached'): [('lesson',
                                                                                                                  'a '
                                                                                                                  'smaller '
                                                                                                                  'step '
                                                                                                                  'still '
                                                                                                                  'counts')],
 ('the hope that does not come this year', 'let this one go, and put the energy into your work for a while'): [('person',
                                                                                                                'colleague')],
 ('the hope that does not come this year', 'stop chasing it, and give the time to the people already at home'): [('lesson',
                                                                                                                  'the '
                                                                                                                  'people '
                                                                                                                  'here '
                                                                                                                  'still '
                                                                                                                  'count')],
 ('the hope that does not come this year', 'let the hope rest, and stay close to the friend who stood by you'): [('person',
                                                                                                                  'friend')],
 ('the household that runs on habit', 'keep every habit exactly as it is, since steadiness is the point'): [('door',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the household that runs on habit', 'change one thing that has gone stale, and see what follows'): [('lesson',
                                                                                                       'one change '
                                                                                                       'can wake a '
                                                                                                       'house')],
 ('the household that runs on habit', 'set the household a goal for the year, and see that it is met'): [('means',
                                                                                                          'money+.04')],
 ('the household that runs on habit', 'shake it up with a move, a trip or a room made new'): [('mark',
                                                                                               'took a wild risk')],
 ('the household that runs on habit', 'stop measuring for a while, and be glad of what holds'): [('means',
                                                                                                  'health+.03')],
 ('the household that runs on habit', "take on a bigger family duty, such as an elder's care"): [('means',
                                                                                                  'time-.05')],
 ('the household that runs on habit', 'ask the others at home what they want next, and follow their lead'): [('means',
                                                                                                              'ties+.04')],
 ('the household that runs on habit', 'ease back for a year, and spend some of the time on yourself'): [('means',
                                                                                                         'freedom+.04')],
 ('the household that runs on habit', 'let it go, and put the hours into friends outside the house'): [('person',
                                                                                                        'friend')],
 ('the household that runs on habit', 'let it go as a goal, and simply live in the home it has become'): [('lesson',
                                                                                                           'it was '
                                                                                                           'already '
                                                                                                           'a home')],
 ('what the household can afford', 'pay only what the household agreed, and nothing over it'): [('means',
                                                                                                 'money-.05')],
 ('what the household can afford', 'find the cheaper way that gets most of it, and pay for that'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('what the household can afford', 'borrow what it takes, and back yourself to pay it back'): [('means',
                                                                                                'money-.08')],
 ('what the household can afford', 'throw everything at it now, savings and all'): [('mark', 'took a wild risk')],
 ('what the household can afford', "put the family's peace first, and let this one go"): [('lesson',
                                                                                           'a smaller place can hold '
                                                                                           'us')],
 ('what the household can afford', 'say not this year, set a date, and save toward it'): [('door', 'kept your word')],
 ('what the household can afford', 'let it go, and put what was saved into something that pays back'): [('lesson',
                                                                                                         'knowing '
                                                                                                         'the limit '
                                                                                                         'is a '
                                                                                                         'skill')],
 ('what the household can afford', 'refuse the price as it stands, and bargain hard for a better one'): [('means',
                                                                                                          'money+.03')],
 ('what the household can afford', 'ask the wider family to chip in, and promise them a room in return'): [('means',
                                                                                                            'ties+.04')],
 ('what the household can afford', 'make do where you are, and make it work better'): [('mark', 'stayed home')],
 ('the step that will not wait', 'take it, but only once everyone at home has said yes'): [('door',
                                                                                            'kept your word')],
 ('the step that will not wait', 'ask for every detail first, then take it with open eyes'): [('person',
                                                                                               'go-between')],
 ('the step that will not wait', 'take it at once, before anyone else can'): [('person', 'rival')],
 ('the step that will not wait', 'jump at it, and sort out the details afterwards'): [('mark', 'took a wild risk')],
 ('the step that will not wait', 'say no, because the timing would cost the family too much'): [('mark',
                                                                                                 'turned down a '
                                                                                                 'chance')],
 ('the step that will not wait', 'take it on firm terms, written down and agreed'): [('means', 'money-.04')],
 ('the step that will not wait', 'think it through, and find you no longer want this at all'): [('lesson',
                                                                                                 'wanting can '
                                                                                                 'change')],
 ('the step that will not wait', 'turn it down, and use the offer to win something smaller nearer home'): [('means',
                                                                                                            'money+.03')],
 ('the step that will not wait', 'let it go, and keep the friend who offered it'): [('person', 'friend')],
 ('the step that will not wait', 'let it pass this time, and wait for a moment that suits everyone'): [('door',
                                                                                                        'turned down '
                                                                                                        'a chance')],
 ('a way round at home', 'go the other way properly: ask, apply, and follow its rules'): [('door', 'kept your word')],
 ('a way round at home', 'look into {aim.round} carefully before committing to it'): [('mark', 'learned a skill')],
 ('a way round at home', 'take {aim.round}, and make it work better than the straight road would have'): [('means',
                                                                                                           'money-.04')],
 ('a way round at home', 'throw yourself into {aim.round} and see where it leads'): [('mark', 'took a wild risk')],
 ('a way round at home', 'wait at home a while longer, and go round only when the family can come too'): [('mark',
                                                                                                           'stayed '
                                                                                                           'home')],
 ('a way round at home', 'ask someone who went that way how it really is'): [('person', 'go-between')],
 ('a way round at home', 'let the old plan go, and take what you learned somewhere else'): [('lesson',
                                                                                             'the road taught plenty '
                                                                                             'anyway')],
 ('a way round at home', 'go round without telling the family, and tell them once it works'): [('door',
                                                                                                'kept it hidden')],
 ('a way round at home', 'take a smaller version of it now, rather than the whole thing later'): [('means',
                                                                                                   'freedom+.03')],
 ('a way round at home', 'let it go for now, and stay close to the people who said no'): [('lesson',
                                                                                           'some roads wait for '
                                                                                           'later')],
 ('what the family makes of it', 'hear them out, then lay out your plan step by step'): [('means', 'ties+.03')],
 ('what the family makes of it', 'answer every worry with a fact, one at a time'): [('lesson',
                                                                                     'calm answers carry further')],
 ('what the family makes of it', 'say plainly that it is your life and your call'): [('means', 'ties-.04')],
 ('what the family makes of it', 'dig in, and tell them they will come round once they see it'): [('mark',
                                                                                                   'defied an '
                                                                                                   'authority')],
 ('what the family makes of it', 'take their worry seriously, and slow your plans to their pace'): [('means',
                                                                                                     'ties+.05')],
 ('what the family makes of it', 'agree to wait a set time, if they back you after it'): [('door', 'kept your word')],
 ('what the family makes of it', 'go ahead quietly, and let them see by how it goes'): [('means', 'freedom+.04')],
 ('what the family makes of it', 'win over the oldest of the family, and let them bring the rest round'): [('person',
                                                                                                            'elder')],
 ('what the family makes of it', 'give in for now, for the sake of peace at home'): [('mark', 'gave in to pressure')],
 ('what the family makes of it', 'ask {parent} what they wish someone had told them at your age'): [('lesson',
                                                                                                     'they were '
                                                                                                     'young once '
                                                                                                     'too')],
 ('the household that has shown it holds', "mark the day properly, with the family's old words"): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('the household that has shown it holds', 'sit quietly afterwards and write down how it came about'): [('lesson',
                                                                                                         'it was '
                                                                                                         'built from '
                                                                                                         'small '
                                                                                                         'days')],
 ('the household that has shown it holds', 'let the wider family and the street know, and enjoy it'): [('person',
                                                                                                        'neighbour')],
 ('the household that has shown it holds', 'throw the party of the year, and dance until late'): [('means',
                                                                                                   'money-.04'),
                                                                                                  ('means',
                                                                                                   'ties+.04')],
 ('the household that has shown it holds', 'thank everyone who carried a part of it, the oldest first'): [('means',
                                                                                                           'ties+.05')],
 ('the household that has shown it holds', 'take stock with the others at home, and plan the next years together'): [('means',
                                                                                                                      'ties+.03')],
 ('the household that has shown it holds', 'put it on record, and leave a copy of the papers in the town archive'): [('place',
                                                                                                                      'learn.keeping')],
 ('the household that has shown it holds', 'enjoy it for one evening, then straight back to the next thing'): [('means',
                                                                                                                'time-.04')],
 ('the household that has shown it holds', 'take everyone out for a long day in the open, all of them'): [('means',
                                                                                                           'health+.03')],
 ('the household that has shown it holds', 'change nothing, and keep the door open as it always was'): [('mark',
                                                                                                         'stayed '
                                                                                                         'home')],
 ('an early hour at {aim.place}', 'do the jobs in the order the old hands taught, every one'): [('door',
                                                                                                 'kept your word')],
 ('an early hour at {aim.place}', 'try one small change, and note what difference it makes'): [('mark',
                                                                                                'learned a skill')],
 ('an early hour at {aim.place}', 'get ahead of everyone else on the season, whatever it takes'): [('means',
                                                                                                    'health-.03')],
 ('an early hour at {aim.place}', 'go out in the worst of the weather, just for the feel of it'): [('means',
                                                                                                    'health+.03')],
 ('an early hour at {aim.place}', 'slow down, and watch what the weather and the season are doing'): [('lesson',
                                                                                                       'the season '
                                                                                                       'sets the '
                                                                                                       'pace')],
 ('an early hour at {aim.place}', 'keep a record of every hour out there, and what came of it'): [('lesson',
                                                                                                   'records show '
                                                                                                   'what memory '
                                                                                                   'misses')],
 ('an early hour at {aim.place}', 'read up on it indoors, and go out once the weather lifts'): [('means',
                                                                                                 'freedom+.03')],
 ('an early hour at {aim.place}', 'leave the dull jobs, and spend the hour on what is doing best'): [('means',
                                                                                                      'time+.03')],
 ('an early hour at {aim.place}', "give the hour a miss for {friend}'s sake, and come back next week"): [('means',
                                                                                                          'ties+.03')],
 ('an early hour at {aim.place}', 'bring someone newer along, and show them what you know'): [('person', 'friend')],
 ("the year's round in {Ns} keeping", 'keep the rota and the rules exactly, so everyone knows where they stand'): [('door',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ("the year's round in {Ns} keeping", 'start a proper record, and teach others to keep it'): [('mark',
                                                                                               'learned a skill')],
 ("the year's round in {Ns} keeping", 'take the decisions yourself, and make {aim.place} the best around'): [('means',
                                                                                                              'time-.05')],
 ("the year's round in {Ns} keeping", 'try something bold this year that nobody has tried there'): [('mark',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ("the year's round in {Ns} keeping", 'plan for what the soil, the water and the creatures will need in twenty years'): [('lesson',
                                                                                                                          'the '
                                                                                                                          'long '
                                                                                                                          'view '
                                                                                                                          'pays '
                                                                                                                          'slowly')],
 ("the year's round in {Ns} keeping", 'write the way it is done into a guide for the newcomers'): [('person',
                                                                                                    'regular')],
 ("the year's round in {Ns} keeping", 'find the money and the help to do it properly, on a plan'): [('person',
                                                                                                     'patron')],
 ("the year's round in {Ns} keeping", 'hand the dull parts to others, and keep the best for yourself'): [('means',
                                                                                                          'freedom+.04')],
 ("the year's round in {Ns} keeping", 'take a season off the planning, and simply be out there'): [('means',
                                                                                                    'health+.04')],
 ("the year's round in {Ns} keeping", 'let the younger ones take a share of the running now'): [('means',
                                                                                                 'time+.05')],
 ('the day of {aim.contest}', 'enter by the rules, every form filled and every class read'): [('place',
                                                                                               'gather.great')],
 ('the day of {aim.contest}', 'study what the judges look for, and prepare for exactly that'): [('mark',
                                                                                                 'learned a skill')],
 ('the day of {aim.contest}', 'enter everything you can, and go for the top prize'): [('person', 'rival')],
 ('the day of {aim.contest}', 'enter on the morning, on a whim, with whatever looks best'): [('mark',
                                                                                              'took a wild risk')],
 ('the day of {aim.contest}', 'go along to help and watch, and show nothing this year'): [('person', 'regular')],
 ('the day of {aim.contest}', 'enter with the club, and help it take the shield'): [('place', 'gather.hall')],
 ('the day of {aim.contest}', 'enter something unusual, just to see what they make of it'): [('lesson',
                                                                                              'odd things get '
                                                                                              'noticed')],
 ('the day of {aim.contest}', 'enter only what you are sure of, and keep the rest back'): [('lesson',
                                                                                            'show what you are sure '
                                                                                            'of')],
 ('the day of {aim.contest}', 'skip the judging, and enjoy the day with {friend}'): [('means', 'ties+.04')],
 ('the day of {aim.contest}', 'spend the day swapping notes with the old hands instead'): [('person', 'mentor')],
 ('the judges from beyond the town', 'prepare by the book for months, and present it without a fault'): [('means',
                                                                                                          'time-.05')],
 ('the judges from beyond the town', 'bring something nobody else has, from years of your own trials'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the judges from beyond the town', 'go to win, and make sure the right people see you do it'): [('person',
                                                                                                   'patron')],
 ('the judges from beyond the town', 'go for the hardest class there is, the one you might well lose'): [('mark',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the judges from beyond the town', "let the year's work speak, and enter it just as it is"): [('lesson',
                                                                                                 'plain work stands '
                                                                                                 'up')],
 ('the judges from beyond the town', 'offer to help run it or judge a class instead of entering'): [('place',
                                                                                                     'gather.great')],
 ('the judges from beyond the town', 'enter, and use the day to meet every buyer and board worth knowing'): [('person',
                                                                                                              'colleague')],
 ('the judges from beyond the town', 'stay away this year, and come back next time with something unbeatable'): [('door',
                                                                                                                  'turned '
                                                                                                                  'down '
                                                                                                                  'a '
                                                                                                                  'chance')],
 ('the judges from beyond the town', 'go along for the spectacle, and come home full of ideas'): [('lesson',
                                                                                                   'the best learn '
                                                                                                   'by looking')],
 ('the judges from beyond the town', 'bring the whole group from {aim.place}, and enter as one'): [('means',
                                                                                                    'ties+.05')],
 ('the old hand at {aim.place}', 'turn up on time every week, and do exactly as you are told'): [('person',
                                                                                                  'mentor')],
 ('the old hand at {aim.place}', 'ask why about everything, and write the answers down'): [('mark',
                                                                                            'learned a skill')],
 ('the old hand at {aim.place}', 'learn everything they know, then set out to do it better'): [('person', 'mentor')],
 ('the old hand at {aim.place}', 'argue with half of it, and try the rest straight away'): [('lesson',
                                                                                             'arguing teaches too')],
 ('the old hand at {aim.place}', 'work alongside them in silence, and learn by watching'): [('person', 'elder')],
 ('the old hand at {aim.place}', 'ask them to put your name forward where it counts'): [('person', 'patron')],
 ('the old hand at {aim.place}', 'take the lessons when the season allows, not every week'): [('means',
                                                                                               'freedom+.03')],
 ('the old hand at {aim.place}', 'take only the tips that help, and keep to your own way'): [('means', 'time+.03')],
 ('the old hand at {aim.place}', 'bring a friend along, and make the mornings a habit for both'): [('person',
                                                                                                    'friend')],
 ('the old hand at {aim.place}', 'help them with their own work, and ask questions as you go'): [('mark',
                                                                                                  'helped someone in '
                                                                                                  'need')],
 ('the neighbour who does it the other way', 'keep to the proven way, and let the results speak over the years'): [('lesson',
                                                                                                                    'one '
                                                                                                                    'good '
                                                                                                                    'season '
                                                                                                                    'proves '
                                                                                                                    'little')],
 ('the neighbour who does it the other way', 'ask {rival} straight out how they do it'): [('person', 'friend')],
 ('the neighbour who does it the other way', 'set out to beat them at the next show, in front of everyone'): [('person',
                                                                                                               'rival')],
 ('the neighbour who does it the other way', 'try their way on one corner, just to see'): [('mark',
                                                                                            'learned a skill')],
 ('the neighbour who does it the other way', 'wish them well, and keep doing what suits your own stretch'): [('means',
                                                                                                              'ties+.03')],
 ('the neighbour who does it the other way', 'propose a fair trial side by side, with honest records'): [('door',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('the neighbour who does it the other way', 'quietly study their methods, and better them'): [('means', 'time-.04')],
 ('the neighbour who does it the other way', 'needle them at {aim.place} until it becomes a proper contest'): [('means',
                                                                                                                'ties-.03')],
 ('the neighbour who does it the other way', 'stop comparing for a season, and just enjoy being out there'): [('means',
                                                                                                               'health+.03')],
 ('the neighbour who does it the other way', 'suggest pooling what you each have, so both stretches do better'): [('person',
                                                                                                                   'neighbour')],
 ('the season the weather takes', 'start again at once, the way it has always been done'): [('means', 'time-.04')],
 ('the season the weather takes', 'work out what made it worse, and change what you can for next time'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the season the weather takes', 'buy in what was lost, and carry on as if nothing happened'): [('means',
                                                                                                  'money-.06')],
 ('the season the weather takes', 'go back out into the mess the next morning, and start clearing'): [('means',
                                                                                                       'health-.03')],
 ('the season the weather takes', 'take the season as it came, and plan round the weather from now on'): [('lesson',
                                                                                                           'the '
                                                                                                           'weather '
                                                                                                           'keeps no '
                                                                                                           'score')],
 ('the season the weather takes', 'rally the others at {aim.place} to rebuild together, on a plan'): [('means',
                                                                                                       'ties+.05')],
 ('the season the weather takes', 'let it go, and take what the loss taught into something new'): [('lesson',
                                                                                                    'a loss can '
                                                                                                    'point '
                                                                                                    'elsewhere')],
 ('the season the weather takes', 'cut your losses, and let this go for something steadier'): [('mark',
                                                                                                'learned a skill')],
 ('the season the weather takes', 'step back for good, and give your tools to someone starting out'): [('person',
                                                                                                        'friend')],
 ('the season the weather takes', 'listen to {elder}, and change what you grow or where you go'): [('person',
                                                                                                    'elder')],
 ('the season nothing improves', 'keep at it exactly as you are, and trust the years'): [('door', 'kept your word')],
 ('the season nothing improves', 'change your method from the ground up, and test it properly'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ('the season nothing improves', 'set yourself a hard target for this season, and hit it'): [('means', 'time-.05')],
 ('the season nothing improves', 'drop the routine, and go about it some completely new way'): [('mark',
                                                                                                 'took a wild risk')],
 ('the season nothing improves', 'cut back to a few hours, and keep it for the quiet it gives'): [('means',
                                                                                                   'time+.05')],
 ('the season nothing improves', 'join a course or a society, and learn the next part properly'): [('place',
                                                                                                    'gather.hall')],
 ('the season nothing improves', 'bring in a partner who knows the part you do not'): [('person', 'colleague')],
 ('the season nothing improves', 'take a year away from it, and come back hungry'): [('means', 'freedom+.05')],
 ('the season nothing improves', 'let it go, and spend the hours outdoors in other ways'): [('lesson',
                                                                                             'being out there was '
                                                                                             'the point')],
 ('the season nothing improves', 'hand your place to someone keener, and help them start'): [('person', 'friend')],
 ('the fees, the gear and the weekends', 'pay what the budget allows, and nothing beyond it'): [('means',
                                                                                                 'money-.04')],
 ('the fees, the gear and the weekends', 'mend the old gear, share the rest, and pay only the fees'): [('mark',
                                                                                                        'learned a '
                                                                                                        'skill')],
 ('the fees, the gear and the weekends', 'pay it all, and earn it back with work on the side'): [('means',
                                                                                                  'money-.06')],
 ('the fees, the gear and the weekends', 'pay whatever it takes, since it is the best part of the week'): [('means',
                                                                                                            'money-.08')],
 ('the fees, the gear and the weekends', 'let it go this year, and give the weekends back to the family'): [('lesson',
                                                                                                             'some '
                                                                                                             'seasons '
                                                                                                             'belong '
                                                                                                             'elsewhere')],
 ('the fees, the gear and the weekends', 'ask the club or society for a fair deal, and hold them to it'): [('means',
                                                                                                            'money+.03')],
 ('the fees, the gear and the weekends', 'work out that it is not worth it, and put the hours elsewhere'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('the fees, the gear and the weekends', 'refuse the rise, and find a cheaper patch through a neighbour'): [('person',
                                                                                                             'neighbour')],
 ('the fees, the gear and the weekends', 'say not this year, and come back when the money is there'): [('door',
                                                                                                        'turned down '
                                                                                                        'a chance')],
 ('the fees, the gear and the weekends', 'go fewer weekends, and agree the days with the family first'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ('the offer with a date on it', 'take it on the proper terms, and keep every one of them'): [('door',
                                                                                               'kept your word')],
 ('the offer with a date on it', 'take it after reading every term, and what it will ask'): [('lesson',
                                                                                              'read every term '
                                                                                              'first')],
 ('the offer with a date on it', 'take it, and ask for more while they are offering'): [('person', 'patron')],
 ('the offer with a date on it', 'take it on the spot, and work the rest out as it comes'): [('mark',
                                                                                              'took a wild risk')],
 ('the offer with a date on it', 'say no, since you already have what you can care for well'): [('mark',
                                                                                                 'turned down a '
                                                                                                 'chance')],
 ('the offer with a date on it', "ask for a season's trial before committing to it all"): [('means', 'time-.04')],
 ('the offer with a date on it', 'take it with a partner, and share the work and the gain'): [('person',
                                                                                               'colleague')],
 ('the offer with a date on it', 'turn it down, and use their interest to bargain for what you want more'): [('means',
                                                                                                              'money+.03')],
 ('the offer with a date on it', 'let it pass, and see that it goes to someone who needs it more'): [('mark',
                                                                                                      'helped '
                                                                                                      'someone in '
                                                                                                      'need')],
 ('the offer with a date on it', 'let the whole thing go, and keep only the part you love doing'): [('lesson',
                                                                                                     'enough to care '
                                                                                                     'for well')],
 ('the way in that is shut', 'apply the proper way to {aim.round}, and wait your turn there'): [('door',
                                                                                                 'kept your word')],
 ('the way in that is shut', 'try {aim.round} for one season, and see if it works'): [('mark', 'learned a skill')],
 ('the way in that is shut', 'go straight to {aim.round}, and make yourself useful there fast'): [('person',
                                                                                                   'regular')],
 ('the way in that is shut', 'turn up at {aim.round} tomorrow, and simply start'): [('mark', 'took a wild risk')],
 ('the way in that is shut', 'keep your name on the old list, and go round meanwhile with {friend}'): [('means',
                                                                                                        'ties+.03')],
 ('the way in that is shut', 'ask the people in charge to make room, and press the point'): [('person',
                                                                                              'go-between')],
 ('the way in that is shut', 'let it go, and take what you learned into something else outdoors'): [('lesson',
                                                                                                     'the waiting '
                                                                                                     'taught '
                                                                                                     'patience')],
 ('the way in that is shut', "share someone else's patch or stretch, and split the work"): [('person', 'neighbour')],
 ('the way in that is shut', 'give it up for now, and help the ones who did get in'): [('person', 'friend')],
 ('the way in that is shut', 'wait one more season, learning at {aim.round} meanwhile'): [('place', 'learn.keeping')],
 ('what the family makes of the hours outdoors', 'agree fair hours with them, and keep to them'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('what the family makes of the hours outdoors', 'show them what you have learned, and the results behind it'): [('lesson',
                                                                                                                  'showing '
                                                                                                                  'beats '
                                                                                                                  'telling')],
 ('what the family makes of the hours outdoors', 'say it is your time and your choice, and leave it there'): [('means',
                                                                                                               'ties-.03')],
 ('what the family makes of the hours outdoors', 'keep going exactly as before, and let them grumble'): [('means',
                                                                                                          'freedom+.04')],
 ('what the family makes of the hours outdoors', 'bring them out to {aim.place} for a day, so they can see it'): [('means',
                                                                                                                   'ties+.05')],
 ('what the family makes of the hours outdoors', 'cut back in the busy weeks, and keep the holidays for it'): [('means',
                                                                                                                'time+.04')],
 ('what the family makes of the hours outdoors', 'lay out where it could lead: a living, a seat, a name'): [('lesson',
                                                                                                             'a plan '
                                                                                                             'calms '
                                                                                                             'worried '
                                                                                                             'people')],
 ('what the family makes of the hours outdoors', 'agree at home, and go anyway when nobody is looking'): [('door',
                                                                                                           'kept it '
                                                                                                           'hidden')],
 ('what the family makes of the hours outdoors', 'give in for now, and go back to it once things are calmer'): [('mark',
                                                                                                                 'gave '
                                                                                                                 'in '
                                                                                                                 'to '
                                                                                                                 'pressure')],
 ('what the family makes of the hours outdoors', 'ask an older relative who understands to speak up for them'): [('person',
                                                                                                                  'elder')],
 ('the season it shows', 'thank the people who run {aim.place}, and take on what comes with it'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('the season it shows', 'write down what worked, so the next one starts further on'): [('lesson',
                                                                                         'slow years made the '
                                                                                         'difference')],
 ('the season it shows', 'let the town know, and make the most of the name'): [('person', 'patron')],
 ('the season it shows', 'celebrate out there with everyone who helped, until dark'): [('means', 'ties+.05')],
 ('the season it shows', 'go out alone the next morning, and carry on as before'): [('means', 'health+.03')],
 ('the season it shows', 'accept the role it brings, and run it well'): [('means', 'time-.05')],
 ('the season it shows', 'start planning the next thing at once, bigger and stranger'): [('means', 'time-.03')],
 ('the season it shows', 'treat yourself to the one tool you have always wanted for it'): [('means', 'money-.04')],
 ('the season it shows', 'throw a party for the whole of {aim.place}, and invite the town'): [('person',
                                                                                               'neighbour')],
 ('the season it shows', 'take a newcomer under their wing, the way someone once did for them'): [('person',
                                                                                                   'friend')],
 ('the evening where both are wanted', 'say yes, and plan the evening in proper order with {aim.person}'): [('person',
                                                                                                             'colleague')],
 ('the evening where both are wanted', 'say yes, and spend the week working out exactly where the two connect'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('the evening where both are wanted', 'say yes, and make sure the evening goes out under {Ns} own name'): [('person',
                                                                                                             'patron')],
 ('the evening where both are wanted', 'say yes, and walk in with no plan but a bag of things to show'): [('person',
                                                                                                           'friend')],
 ('the evening where both are wanted', 'thank {aim.person}, and wait until the two have settled side by side'): [('lesson',
                                                                                                                  'some '
                                                                                                                  'things '
                                                                                                                  'need '
                                                                                                                  'to '
                                                                                                                  'ripen')],
 ('the evening where both are wanted', 'ask for a later date, once the fit between them is worked out on paper'): [('lesson',
                                                                                                                    'a '
                                                                                                                    'plan '
                                                                                                                    'before '
                                                                                                                    'a '
                                                                                                                    'crowd')],
 ('the evening where both are wanted', 'prepare one sharp example that shows what neither does alone'): [('person',
                                                                                                          'regular')],
 ('the evening where both are wanted', 'pass on this one, and save the idea for a bigger room later'): [('door',
                                                                                                         'turned '
                                                                                                         'down a '
                                                                                                         'chance')],
 ('the evening where both are wanted', 'turn it into a hands-on night where everyone has a go at both'): [('place',
                                                                                                           'gather.hall')],
 ('the evening where both are wanted', 'bring two people who know {aim2.thing} to help the evening go well'): [('person',
                                                                                                                'friend')],
 ('a gap only {N} can see', 'keep quiet for now, since it is not {Ns} place to correct the old hands'): [('lesson',
                                                                                                          'rank '
                                                                                                          'keeps its '
                                                                                                          'own '
                                                                                                          'timing')],
 ('a gap only {N} can see', 'note how {aim2.doing} handles it, and test the fix on one small case'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('a gap only {N} can see', 'fix it quietly, and let the better results speak for {N}'): [('person', 'patron')],
 ('a gap only {N} can see', 'let it go, as the pleasure of each lies in keeping them separate'): [('lesson',
                                                                                                   'each has its own '
                                                                                                   'pleasure')],
 ('a gap only {N} can see', 'mention it gently to the one who has been there longest'): [('person', 'elder')],
 ('a gap only {N} can see', 'raise it at the next meeting, with a proposal ready and {Ns} name on it'): [('person',
                                                                                                          'colleague')],
 ('a gap only {N} can see', 'offer the fix to the whole group, if {N} may lead the change'): [('place',
                                                                                               'gather.hall')],
 ('a gap only {N} can see', 'leave it for now, and watch a full season first to be sure'): [('means', 'time+.03')],
 ('a gap only {N} can see', 'try the fix on the spot one evening, and see who notices'): [('person', 'rival')],
 ('a gap only {N} can see', 'bring it up laughing over tea, and let the group decide together'): [('person',
                                                                                                   'friend')],
 ('the project that needs both halves', 'accept, and agree a clear share of the work and the hours'): [('person',
                                                                                                        'colleague')],
 ('the project that needs both halves', 'ask to wait until the plans are clear enough to judge properly'): [('lesson',
                                                                                                             'see '
                                                                                                             'the '
                                                                                                             'plans '
                                                                                                             'first')],
 ('the project that needs both halves', 'accept, provided {N} leads the part where the two meet'): [('person',
                                                                                                     'patron')],
 ('the project that needs both halves', 'throw in at once, and sketch the first idea at the meeting itself'): [('mark',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ('the project that needs both halves', 'accept, and bring in people from both sides who have helped before'): [('person',
                                                                                                                 'friend')],
 ('the project that needs both halves', 'accept, and draw up a careful plan of where each half fits'): [('place',
                                                                                                         'rule.counsel')],
 ('the project that needs both halves', 'take the hardest part, the piece nobody else knows how to design'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the project that needs both halves', 'accept on the spot, and promise the planners more than they asked for'): [('person',
                                                                                                                    'go-between')],
 ('the project that needs both halves', 'say no for now, so the season keeps its free evenings'): [('means',
                                                                                                    'time+.04')],
 ('the project that needs both halves', 'decline, and point the planners to someone with more time'): [('lesson',
                                                                                                        'others can '
                                                                                                        'carry it')],
 ('the newcomer who wants both', 'agree, and set regular hours and a fair way to share them'): [('person',
                                                                                                 'regular')],
 ('the newcomer who wants both', 'agree, and work out a course that moves from one to the other'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('the newcomer who wants both', 'decline, since the way {N} does it is an edge worth keeping close'): [('lesson',
                                                                                                         'an edge '
                                                                                                         'kept '
                                                                                                         'close')],
 ('the newcomer who wants both', 'agree, and teach it the way it comes, all at once and by feel'): [('person',
                                                                                                     'friend')],
 ('the newcomer who wants both', 'say not yet, until {N} has lived longer with the two together'): [('lesson',
                                                                                                     'teach what has '
                                                                                                     'settled')],
 ('the newcomer who wants both', 'send the newcomer to the proper teachers of each, one at a time'): [('door',
                                                                                                       'turned down '
                                                                                                       'a chance')],
 ('the newcomer who wants both', 'agree, and build a small circle of learners around the pair'): [('place',
                                                                                                   'gather.circle')],
 ('the newcomer who wants both', 'agree, starting with the slow basics that both of them share'): [('mark',
                                                                                                    'learned a '
                                                                                                    'skill')],
 ('the newcomer who wants both', 'agree, and try odd exercises that jump between the two mid-session'): [('mark',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the newcomer who wants both', 'agree, and open the sessions to anyone else who wants to come'): [('place',
                                                                                                     'gather.hall')],
 ('one habit carried across', 'ask {aim.person} first whether the new habit is allowed'): [('person', 'mentor')],
 ('one habit carried across', 'test the habit for a fortnight, and keep careful notes on it'): [('mark',
                                                                                                 'learned a skill')],
 ('one habit carried across', 'adopt it outright, and let the others wonder what changed'): [('person', 'rival')],
 ('one habit carried across', 'leave it, because {aim2.doing} is the escape and not a tool'): [('lesson',
                                                                                                'keep one thing '
                                                                                                'free')],
 ('one habit carried across', 'work it in slowly, in the small daily part nobody watches'): [('mark',
                                                                                              'learned a skill')],
 ('one habit carried across', 'finish the season the usual way, and study the habit properly after'): [('means',
                                                                                                        'time+.03')],
 ('one habit carried across', 'hold it back until it is proven, so nobody sees an early stumble'): [('lesson',
                                                                                                     'proof before '
                                                                                                     'show')],
 ('one habit carried across', 'bring it out on the important day itself, all or nothing'): [('mark',
                                                                                             'took a wild risk')],
 ('one habit carried across', 'try it out with a friend from {aim2.thing}, for the fun of it'): [('person',
                                                                                                  'friend')],
 ('one habit carried across', 'show the habit to the group, so that all of them can share it'): [('person',
                                                                                                  'colleague')],
 ('two crowds that never meet', 'leave each group to its own customs for now'): [('lesson',
                                                                                  'each crowd has its ways')],
 ('two crowds that never meet', 'wait, and first find out what each side actually wants from the other'): [('lesson',
                                                                                                            'find '
                                                                                                            'the '
                                                                                                            'need '
                                                                                                            'first')],
 ('two crowds that never meet', 'host it, and make sure {N} is the one both sides thank'): [('person', 'patron')],
 ('two crowds that never meet', 'throw the evening together within a week, food, noise and all'): [('place',
                                                                                                    'gather.house')],
 ('two crowds that never meet', 'invite a few from each side round to {Ns} home first, quietly'): [('person',
                                                                                                    'friend')],
 ('two crowds that never meet', 'organise it properly, with {N} chairing and both leaders thanked'): [('person',
                                                                                                       'go-between')],
 ('two crowds that never meet', 'hold back, and keep both crowds as {Ns} own private worlds'): [('means',
                                                                                                 'time+.03')],
 ('two crowds that never meet', 'pair one person from each side who share the same small problem'): [('person',
                                                                                                      'colleague')],
 ('two crowds that never meet', 'run one mixed evening as an experiment, and see what sparks'): [('place',
                                                                                                  'gather.hall')],
 ('two crowds that never meet', 'ask both crowds along to the yearly fair as one big group'): [('place',
                                                                                                'gather.great')],
 ('a need the town has not named', "write to the town's committee with a plain offer to help"): [('place',
                                                                                                  'rule.counsel')],
 ('a need the town has not named', 'look into exactly who needs what, and then offer something that fits'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('a need the town has not named', 'leave it, since unpaid work for the town would cost {N} the season'): [('lesson',
                                                                                                            'time '
                                                                                                            'has a '
                                                                                                            'price '
                                                                                                            'too')],
 ('a need the town has not named', 'start helping straight away, and work out the rest along the way'): [('mark',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('a need the town has not named', 'start with the neighbours on {Ns} own street, nothing grand'): [('person',
                                                                                                     'neighbour')],
 ('a need the town has not named', 'draw up a careful offer, and take it to the people in charge'): [('person',
                                                                                                      'go-between')],
 ('a need the town has not named', 'design a fix that uses both, and keep the credit for it'): [('person', 'patron')],
 ('a need the town has not named', 'wait until someone asks, and pays properly, before stepping in'): [('door',
                                                                                                        'turned down '
                                                                                                        'a chance')],
 ('a need the town has not named', 'gather a few friends from both sides and simply get on with it'): [('person',
                                                                                                        'friend')],
 ('a need the town has not named', 'leave it to those whose job it is, and keep {Ns} own house steady'): [('lesson',
                                                                                                           'others '
                                                                                                           'hold '
                                                                                                           'that '
                                                                                                           'duty')],
 ('the work that shows both', 'agree, and keep strictly to what the day asks for'): [('person', 'colleague')],
 ('the work that shows both', 'agree, and make a careful account of how the two inform each other'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('the work that shows both', 'agree, and aim the piece at the most important people who will come'): [('person',
                                                                                                        'patron')],
 ('the work that shows both', 'agree, and make the boldest thing that comes to mind'): [('mark', 'took a wild risk')],
 ('the work that shows both', 'let it pass this year, and keep the season for the usual round'): [('lesson',
                                                                                                   'there is always '
                                                                                                   'next year')],
 ('the work that shows both', 'agree, and make it the piece people will remember {N} by'): [('place',
                                                                                             'gather.great')],
 ('the work that shows both', "agree, and make it with the household's help so it is partly theirs"): [('person',
                                                                                                        'friend')],
 ('the work that shows both', 'agree, and make something modest and useful rather than showy'): [('mark',
                                                                                                  'learned a skill')],
 ('the work that shows both', 'say no for now, as forcing an unready idea would spoil it'): [('lesson',
                                                                                              'ideas come when '
                                                                                              'ready')],
 ('the work that shows both', 'say no to the piece, and offer to help run the day instead'): [('person',
                                                                                               'colleague')],
 ('a trial run on a quiet day', 'decline politely, as the weekend is already promised to others'): [('mark',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('a trial run on a quiet day', 'accept, and run it as a small, careful test with notes'): [('mark',
                                                                                             'learned a skill')],
 ('a trial run on a quiet day', 'accept, and invite one person whose good opinion matters'): [('person', 'patron')],
 ('a trial run on a quiet day', 'let the day go, as the idea is more fun as a daydream for now'): [('lesson',
                                                                                                    'some ideas like '
                                                                                                    'waiting')],
 ('a trial run on a quiet day', 'accept, and keep it small and homely with familiar faces'): [('person', 'friend')],
 ('a trial run on a quiet day', 'accept, and set out the session step by step beforehand'): [('person', 'colleague')],
 ('a trial run on a quiet day', 'accept, and use the trial to find what could later be offered properly'): [('place',
                                                                                                             'gather.hall')],
 ('a trial run on a quiet day', 'accept, and make the trial lively enough that word gets round'): [('person',
                                                                                                    'regular')],
 ('a trial run on a quiet day', 'spend the free day outdoors with friends instead'): [('lesson',
                                                                                       'rest feeds the next idea')],
 ('a trial run on a quiet day', 'accept, and ask {aim.person} to stay and help keep it on track'): [('person',
                                                                                                     'mentor')],
 ('the opening that asks for both', 'apply by the book, with the worked example done exactly to the brief'): [('person',
                                                                                                               'boss')],
 ('the opening that asks for both', 'hold off, as one worked example is not yet enough to judge the fit'): [('lesson',
                                                                                                             'know '
                                                                                                             'the '
                                                                                                             'fit '
                                                                                                             'first')],
 ('the opening that asks for both', 'let this one pass, since a better-placed opening will come on {Ns} terms'): [('door',
                                                                                                                   'turned '
                                                                                                                   'down '
                                                                                                                   'a '
                                                                                                                   'chance')],
 ('the opening that asks for both', 'apply on impulse, with the wildest worked example {N} can imagine'): [('mark',
                                                                                                            'took a '
                                                                                                            'wild '
                                                                                                            'risk')],
 ('the opening that asks for both', 'apply, with an example drawn from {Ns} own everyday round'): [('mark',
                                                                                                    'learned a '
                                                                                                    'skill')],
 ('the opening that asks for both', 'apply, and ask {aim.person} for a letter to go with it'): [('person', 'patron')],
 ('the opening that asks for both', 'apply, and make the example about the town that raised {N}'): [('person',
                                                                                                     'elder')],
 ('the opening that asks for both', 'leave it, and spend the year learning how the two truly fit'): [('lesson',
                                                                                                      'the fit takes '
                                                                                                      'years')],
 ('the opening that asks for both', 'apply with an example built on an experiment nobody has tried'): [('place',
                                                                                                        'learn.keeping')],
 ('the opening that asks for both', 'apply as a pair, with a friend who knows {aim2.thing} well'): [('person',
                                                                                                     'friend')],
 ('the long evening with {aim.thing}', 'keep the same hour every evening, whatever else is on'): [('means',
                                                                                                   'time-.04')],
 ('the long evening with {aim.thing}', 'write down exactly what does not make sense, and start from there'): [('lesson',
                                                                                                               'naming '
                                                                                                               'the '
                                                                                                               'muddle '
                                                                                                               'helps')],
 ('the long evening with {aim.thing}', 'set out to know more of it than anyone around by spring'): [('person',
                                                                                                     'rival')],
 ('the long evening with {aim.thing}', 'chase the part that is most exciting tonight, and leave the rest'): [('means',
                                                                                                              'time-.03')],
 ('the long evening with {aim.thing}', 'put it down early and come back to it fresh tomorrow'): [('means',
                                                                                                  'health+.03')],
 ('the long evening with {aim.thing}', 'ask a teacher to set a little extra each week'): [('person', 'teacher')],
 ('the long evening with {aim.thing}', 'look up the hardest question on it, and try it alone'): [('mark',
                                                                                                  'learned a skill')],
 ('the long evening with {aim.thing}', 'make it a race with a friend: who gets further by the weekend'): [('person',
                                                                                                           'friend')],
 ('the long evening with {aim.thing}', 'go out and look for where it turns up in ordinary life'): [('lesson',
                                                                                                    'it turns up '
                                                                                                    'everywhere once '
                                                                                                    'seen')],
 ('the long evening with {aim.thing}', 'do it beside {parent} at the kitchen table, at an easy pace'): [('means',
                                                                                                         'ties+.03')],
 ('the slow hours behind every answer', 'set aside two fixed mornings a week and guard them from everyone'): [('means',
                                                                                                               'time-.05')],
 ('the slow hours behind every answer', 'go back and check what everyone in the field now takes for granted'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('the slow hours behind every answer', 'keep up only with the work that stays a step ahead of the others'): [('person',
                                                                                                               'rival')],
 ('the slow hours behind every answer', 'follow the strange new thread nobody else has noticed yet'): [('mark',
                                                                                                        'took a wild '
                                                                                                        'risk')],
 ('the slow hours behind every answer', 'cut the hours back to what still feels good, and let the rest wait'): [('means',
                                                                                                                 'health+.04')],
 ('the slow hours behind every answer', 'join the committee that sets the standard, so the hours count for more'): [('place',
                                                                                                                     'rule.counsel')],
 ('the slow hours behind every answer', 'take on a younger helper for the checking, and keep the hardest part'): [('person',
                                                                                                                   'colleague')],
 ('the slow hours behind every answer', 'sit with an older hand who has done this forty years, and compare notes'): [('person',
                                                                                                                      'elder')],
 ('the slow hours behind every answer', 'write up what is known so far, rough as it is, and show it'): [('lesson',
                                                                                                         'unfinished '
                                                                                                         'work still '
                                                                                                         'teaches')],
 ('the slow hours behind every answer', 'take a month away, and come back steady for those who rely on the work'): [('means',
                                                                                                                     'freedom+.04')],
 ('the first test of what {N} knows', 'revise what was set, in the order it was set'): [('means', 'time-.03')],
 ('the first test of what {N} knows', 'work out what they are likely to ask, and practise exactly that'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ('the first test of what {N} knows', 'go in to beat the best of the others, not just to pass'): [('person',
                                                                                                   'rival')],
 ('the first test of what {N} knows', 'go in cold and trust what is already there'): [('lesson',
                                                                                       'nerves fade once it starts')],
 ('the first test of what {N} knows', 'ask to sit it another time, when it feels less rushed'): [('means',
                                                                                                  'health+.03')],
 ('the first test of what {N} knows', 'ask a teacher what a good answer looks like, and practise one'): [('person',
                                                                                                          'teacher')],
 ('the first test of what {N} knows', 'quiz each other with someone from the group until one cracks'): [('person',
                                                                                                         'friend')],
 ('the first test of what {N} knows', 'leave it: a test this small is not worth the fuss'): [('lesson',
                                                                                              'not every test '
                                                                                              'counts')],
 ('the first test of what {N} knows', 'go along with {friend} for the company, and see what happens'): [('means',
                                                                                                         'ties+.03')],
 ('the first test of what {N} knows', 'stay home to help {parent}, and sit the next one instead'): [('mark',
                                                                                                     'helped someone '
                                                                                                     'in need')],
 ('standing up to be questioned', 'accept, and prepare by the standards the others will judge by'): [('means',
                                                                                                      'time-.06')],
 ('standing up to be questioned', 'accept, and prepare for the hardest question anyone in the room could ask'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('standing up to be questioned', "accept, and go in to change the room's mind"): [('person', 'rival')],
 ('standing up to be questioned', 'accept, and speak without notes, as it comes'): [('mark', 'took a wild risk')],
 ('standing up to be questioned', 'decline politely: this season belongs to other things'): [('mark',
                                                                                              'turned down a '
                                                                                              'chance')],
 ('standing up to be questioned', 'accept, and bring along the colleagues who stand behind the work'): [('person',
                                                                                                         'colleague')],
 ('standing up to be questioned', 'send a younger one in your place, and coach them for it'): [('mark',
                                                                                                'helped someone in '
                                                                                                'need')],
 ('standing up to be questioned', 'go, answer plainly, and listen more than talk'): [('person', 'mentor')],
 ('standing up to be questioned', 'turn it down, and spend the month on the question itself'): [('lesson',
                                                                                                 'the work outlasts '
                                                                                                 'the stage')],
 ('standing up to be questioned', 'say yes, and make it a day the young ones in the field remember'): [('place',
                                                                                                        'gather.great')],
 ('the one who has done it before', 'accept, and turn up at the agreed hour every week'): [('door',
                                                                                            'kept your word')],
 ('the one who has done it before', 'accept, and come with a list of questions each time'): [('person', 'mentor')],
 ('the one who has done it before', 'accept, and learn everything they know as fast as possible'): [('person',
                                                                                                     'mentor')],
 ('the one who has done it before', 'thank them, and keep doing it your own way'): [('mark', 'turned down a chance')],
 ('the one who has done it before', 'ask whether {friend} can come along too'): [('person', 'friend')],
 ('the one who has done it before', 'accept, on condition they mark everything strictly'): [('means', 'time-.04')],
 ('the one who has done it before', 'ask them for hard tests, aimed where the work is weakest'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ('the one who has done it before', 'take the one tip that matters most and run with it alone'): [('lesson',
                                                                                                   'one good tip '
                                                                                                   'goes far')],
 ('the one who has done it before', 'ask to watch them at their own work instead of being taught'): [('person',
                                                                                                      'mentor')],
 ('the one who has done it before', 'say not yet: there is enough on just now, perhaps after the summer'): [('means',
                                                                                                             'time+.03')],
 ('the other one who knows', 'agree on what would settle it, and abide by the result'): [('person', 'rival')],
 ('the other one who knows', 'go away and check, properly, which answer is right'): [('mark', 'learned a skill')],
 ('the other one who knows', 'make sure the people who matter hear your side first'): [('person', 'patron')],
 ('the other one who knows', 'argue it out there and then, as loudly as it takes'): [('person', 'rival')],
 ('the other one who knows', 'let it go: there is room for two who know it'): [('person', 'friend')],
 ('the other one who knows', 'ask a respected third person to judge between the two answers'): [('person', 'elder')],
 ('the other one who knows', 'quietly win over the people the rival depends on'): [('means', 'ties+.04')],
 ('the other one who knows', 'ask the rival over, and work through it together'): [('person', 'colleague')],
 ('the other one who knows', "take the rival's best point and build something new on it"): [('lesson',
                                                                                             'a rival sharpens the '
                                                                                             'work')],
 ('the other one who knows', 'stop arguing and challenge them to a fair test in public'): [('mark',
                                                                                            'took a wild risk')],
 ('the answer that was wrong', 'own the mistake openly, and put it right where it was made'): [('mark', 'owned up')],
 ('the answer that was wrong', 'find exactly where the thinking went wrong'): [('mark', 'learned a skill')],
 ('the answer that was wrong', 'come back next time so well prepared nobody remembers it'): [('means', 'time-.04')],
 ('the answer that was wrong', 'let {aim.thing} go: it has stopped being worth the sting'): [('lesson',
                                                                                              'pride heals slower '
                                                                                              'than skill')],
 ('the answer that was wrong', 'take a quiet week, then go back to it gently'): [('means', 'health+.03')],
 ('the answer that was wrong', 'ask {aim.person} to go through the mistake step by step'): [('person', 'mentor')],
 ('the answer that was wrong', 'write down what went wrong, so it never happens the same way twice'): [('lesson',
                                                                                                        'a mistake '
                                                                                                        'written '
                                                                                                        'down stays '
                                                                                                        'small')],
 ('the answer that was wrong', 'prove them wrong with something bolder'): [('mark', 'took a wild risk')],
 ('the answer that was wrong', 'walk it off outside, then talk it through with {friend}'): [('means', 'ties+.03')],
 ('the answer that was wrong', 'decide this is not the road, and keep the friends it brought'): [('person',
                                                                                                  'friend')],
 ('the long flat stretch', 'keep the same routine: the steady way has worked so far'): [('means', 'time-.04')],
 ('the long flat stretch', 'change the method entirely, and see what that shows'): [('mark', 'learned a skill')],
 ('the long flat stretch', 'find out what the ones further on did differently, and copy it'): [('person',
                                                                                                'colleague')],
 ('the long flat stretch', 'throw out the routine and follow whatever still stirs curiosity'): [('lesson',
                                                                                                 'boredom asks for '
                                                                                                 'something new')],
 ('the long flat stretch', 'slow to an easy pace for a while, and let it settle'): [('means', 'health+.04')],
 ('the long flat stretch', 'set a firm test six months from now, and train for that'): [('door', 'kept your word')],
 ('the long flat stretch', 'let it go, and put what it taught into something that pays'): [('mark',
                                                                                            'learned a skill')],
 ('the long flat stretch', 'come back to it only when a real question pulls hard enough'): [('lesson',
                                                                                             'questions return when '
                                                                                             'they are ready')],
 ('the long flat stretch', 'give it a season off, and try something next to it'): [('means', 'freedom+.04')],
 ('the long flat stretch', 'let it go gracefully, and pass the notes to someone just starting'): [('person',
                                                                                                   'friend')],
 ('what the next step costs', 'pay, but only from money set aside, and keep to the budget'): [('means', 'money-.05')],
 ('what the next step costs', 'find the cheapest way to the same knowledge, and use that'): [('mark',
                                                                                              'learned a skill')],
 ('what the next step costs', 'pay the full price and make sure it pays back'): [('means', 'money-.08')],
 ('what the next step costs', 'throw everything at it: the money, the evenings, the lot'): [('means', 'money-.10')],
 ('what the next step costs', 'not this year: the family needs the money more'): [('means', 'ties+.03')],
 ('what the next step costs', 'apply for a grant first, and wait for the answer before spending'): [('place',
                                                                                                     'learn.higher')],
 ('what the next step costs', 'pay half now, and earn the rest by teaching the basics to others'): [('means',
                                                                                                     'time-.06')],
 ('what the next step costs', 'borrow it, and trust in paying it off'): [('place', 'comm.credit')],
 ('what the next step costs', 'let it go: what has been learned stays, whatever happens next'): [('lesson',
                                                                                                  'learning stays '
                                                                                                  'after stopping')],
 ('what the next step costs', 'let it go, and pass on what is already known to someone at home'): [('lesson',
                                                                                                    'teaching fixes '
                                                                                                    'knowledge in '
                                                                                                    'place')],
 ('the place that will not wait', 'accept, and arrange everything properly before leaving'): [('mark', 'moved away')],
 ('the place that will not wait', 'accept, for the work and nothing else'): [('place', 'learn.higher')],
 ('the place that will not wait', 'accept, but ask for better terms first'): [('person', 'patron')],
 ('the place that will not wait', 'say yes on the spot and pack tonight'): [('mark', 'took a wild risk')],
 ('the place that will not wait', 'decline: home and the people here come first'): [('mark', 'stayed home')],
 ('the place that will not wait', "ask for a year's delay, to arrive properly prepared"): [('door',
                                                                                            'turned down a chance')],
 ('the place that will not wait', 'take it part time, and keep your roots here'): [('means', 'time-.06')],
 ('the place that will not wait', 'stay, and find a way to learn the same things from here'): [('person', 'teacher')],
 ('the place that will not wait', 'take it, and treat the move as half the adventure'): [('mark', 'left home')],
 ('the place that will not wait', 'let this road end here, and keep the people it brought along'): [('person',
                                                                                                     'friend')],
 ('no way in by the front door', 'let it go rather than get in by a door not worth respecting'): [('lesson',
                                                                                                   'the rule was not '
                                                                                                   'personal')],
 ('no way in by the front door', 'try {aim.round}, and work out how to make it serve'): [('mark', 'learned a skill')],
 ('no way in by the front door', 'take the other way, and use it to pass those who went the usual one'): [('person',
                                                                                                           'rival')],
 ('no way in by the front door', 'go the other way at once, before anyone can argue against it'): [('mark',
                                                                                                    'defied an '
                                                                                                    'authority')],
 ('no way in by the front door', 'go the other way slowly, a little each month, as life allows'): [('means',
                                                                                                    'time-.02')],
 ('no way in by the front door', 'ask the ones who closed the door what would open it, and do that'): [('person',
                                                                                                        'keeper')],
 ('no way in by the front door', 'find someone already on the other road who can open the way in'): [('person',
                                                                                                      'friend')],
 ('no way in by the front door', 'stop knocking on this door, and let {aim.thing} go for now'): [('mark',
                                                                                                  'learned a skill')],
 ('no way in by the front door', 'go the other way in with {friend}, so it is less lonely'): [('means', 'ties+.03')],
 ('no way in by the front door', 'go round through the older people at home who know the way'): [('person', 'elder')],
 ('the talk at supper about {aim.thing}', 'explain calmly what it is for, and how many hours it will take each week'): [('door',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('the talk at supper about {aim.thing}', 'show them what has been learned, and let it speak for itself'): [('means',
                                                                                                             'ties+.03')],
 ('the talk at supper about {aim.thing}', 'tell them it is going on, whatever anyone thinks'): [('mark',
                                                                                                 'defied an '
                                                                                                 'authority')],
 ('the talk at supper about {aim.thing}', 'argue it out, hotly, until somebody laughs'): [('lesson',
                                                                                           'arguments at home blow '
                                                                                           'over')],
 ('the talk at supper about {aim.thing}', 'agree gladly to give it fewer hours, and more to the family'): [('means',
                                                                                                            'ties+.04')],
 ('the talk at supper about {aim.thing}', 'strike a fair deal: so many hours, and the chores done first'): [('mark',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the talk at supper about {aim.thing}', 'do what they ask for now, and carry on quietly later'): [('mark',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ('the talk at supper about {aim.thing}', 'ask {parent} to come and see what it is really like'): [('lesson',
                                                                                                    'seeing it '
                                                                                                    'changes minds')],
 ('the talk at supper about {aim.thing}', 'take the worry seriously, and cut back where they are right'): [('means',
                                                                                                            'time+.03')],
 ('the talk at supper about {aim.thing}', 'give way because they insist, and keep the peace at home'): [('door',
                                                                                                         'gave in to '
                                                                                                         'pressure')],
 ('{aim.rung}, at last', 'thank the people who helped, one by one'): [('person', 'mentor')],
 ('{aim.rung}, at last', 'note it quietly and go straight back to the next question'): [('mark', 'learned a skill')],
 ('{aim.rung}, at last', 'make sure the right people hear about it'): [('person', 'patron')],
 ('{aim.rung}, at last', 'celebrate loudly, with everyone who will come'): [('person', 'friend')],
 ('{aim.rung}, at last', 'tell {parent} first, and keep the day simple'): [('means', 'ties+.03')],
 ('{aim.rung}, at last', 'write down the road here, for the next one who tries'): [('lesson',
                                                                                    'the road looks clearer behind')],
 ('{aim.rung}, at last', 'ask straight away what it takes to reach the next step'): [('means', 'time-.03')],
 ('{aim.rung}, at last', 'hold a small party and say a few proud words'): [('means', 'ties+.04')],
 ('{aim.rung}, at last', 'go somewhere wide and open, alone, and let it sink in'): [('means', 'health+.03')],
 ('{aim.rung}, at last', 'share the credit with everyone who helped along the way'): [('means', 'ties+.05')],
 ('the ordinary week at {aim.place}', 'do every task the way it is meant to be done, and on time'): [('mark',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the ordinary week at {aim.place}', 'watch how the best one there does it, and work out why'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ('the ordinary week at {aim.place}', 'volunteer for whatever the people in charge will notice'): [('person',
                                                                                                    'boss')],
 ('the ordinary week at {aim.place}', 'try a faster way of your own, and see if it holds'): [('mark',
                                                                                              'took a wild risk')],
 ('the ordinary week at {aim.place}', 'do your share, help the others with theirs, and go home on time'): [('person',
                                                                                                            'colleague')],
 ('the ordinary week at {aim.place}', 'ask for a clear list of what would earn more responsibility'): [('means',
                                                                                                        'time-.03')],
 ('the ordinary week at {aim.place}', 'learn who really keeps the place running, and stay on their side'): [('person',
                                                                                                             'go-between')],
 ('the ordinary week at {aim.place}', 'ask the old hand how it used to be done, and why it changed'): [('person',
                                                                                                        'elder')],
 ('the ordinary week at {aim.place}', 'keep a notebook of every mistake and every trick'): [('lesson',
                                                                                             'small tricks add up')],
 ('the ordinary week at {aim.place}', 'coast the slow days, and save strength for the busy ones when others need help'): [('means',
                                                                                                                           'health+.03')],
 ('the weight of being the one they answer to', 'keep regular hours, a clear plan, and the door open at set times'): [('means',
                                                                                                                       'time-.04')],
 ('the weight of being the one they answer to', 'stay sharp on the work itself, not only the managing of it'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('the weight of being the one they answer to', 'take on more, and make sure everyone knows who carries it'): [('means',
                                                                                                                'time-.06')],
 ('the weight of being the one they answer to', 'shake up how things are done, and see who keeps up'): [('person',
                                                                                                         'rival')],
 ('the weight of being the one they answer to', 'hand some of the load to others, and keep the evenings for home'): [('means',
                                                                                                                      'ties+.04')],
 ('the weight of being the one they answer to', 'set up a proper weekly meeting, so problems surface early'): [('person',
                                                                                                                'colleague')],
 ('the weight of being the one they answer to', 'read the numbers every week, and act on what they show'): [('means',
                                                                                                             'money+.04')],
 ('the weight of being the one they answer to', 'chase the one big piece of work that could make your name'): [('mark',
                                                                                                                'took '
                                                                                                                'a '
                                                                                                                'wild '
                                                                                                                'risk')],
 ('the weight of being the one they answer to', 'take a long walk at midday, and let the day sort itself out'): [('means',
                                                                                                                  'health+.04')],
 ('the weight of being the one they answer to', 'train up the one who will take over one day'): [('lesson',
                                                                                                  'teaching shows '
                                                                                                  'what is known')],
 ('the morning of {aim.contest}', 'prepare properly, dress properly, and arrive early'): [('means', 'time-.03')],
 ('the morning of {aim.contest}', 'find out what they really look for, and prepare exactly that'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('the morning of {aim.contest}', 'go in to be the one they cannot turn down'): [('person', 'boss')],
 ('the morning of {aim.contest}', 'go in unrehearsed and natural, and trust it'): [('lesson',
                                                                                    'nerves can pass for keenness')],
 ('the morning of {aim.contest}', 'let this one pass: the timing is wrong at home'): [('means', 'ties+.03')],
 ('the morning of {aim.contest}', 'ask a senior colleague to put in a good word before the day'): [('person',
                                                                                                    'patron')],
 ('the morning of {aim.contest}', 'skip it, and stay where the work is known and safe'): [('mark',
                                                                                           'turned down a chance')],
 ('the morning of {aim.contest}', 'ask the people already in the job what the day is really like'): [('person',
                                                                                                      'colleague')],
 ('the morning of {aim.contest}', 'rehearse the hardest questions with {friend} the night before'): [('person',
                                                                                                      'friend')],
 ('the morning of {aim.contest}', 'go in to show what the job could do for the people there'): [('means',
                                                                                                 'ties+.02')],
 ('the decision at the top table', 'stand, and make the case through the proper channels'): [('place',
                                                                                              'rule.counsel')],
 ('the decision at the top table', 'stand, with a plan nobody can fault'): [('mark', 'learned a skill')],
 ('the decision at the top table', 'stand, and line up support person by person before the day'): [('person',
                                                                                                    'patron')],
 ('the decision at the top table', 'stand, and say exactly what is true on the day, plainly'): [('mark',
                                                                                                 'took a wild risk')],
 ('the decision at the top table', 'stand aside for someone the others trust more'): [('person', 'colleague')],
 ('the decision at the top table', 'stand, and send everyone a written plan to read beforehand'): [('means',
                                                                                                    'time-.05')],
 ('the decision at the top table', 'count the support honestly, and stay out if it is not there'): [('lesson',
                                                                                                     'an honest '
                                                                                                     'count saves a '
                                                                                                     'fall')],
 ('the decision at the top table', 'stand, and make it a contest people talk about for years'): [('person', 'rival')],
 ('the decision at the top table', 'sit this one out, and give the season to the family'): [('means', 'ties+.05')],
 ('the decision at the top table', 'stand, with the backing of the people looked after over the years'): [('means',
                                                                                                           'ties+.03')],
 ('someone further up the road', 'accept gratefully, and keep every meeting'): [('person', 'mentor')],
 ('someone further up the road', 'accept, and bring one hard problem from the job each time'): [('mark',
                                                                                                 'learned a skill')],
 ('someone further up the road', 'accept, and ask for the introductions straight away'): [('person', 'patron')],
 ('someone further up the road', 'say thanks but no, and find a way alone'): [('mark', 'turned down a chance')],
 ('someone further up the road', 'accept, and bring the newer ones along to learn too'): [('person', 'colleague')],
 ('someone further up the road', 'accept, and agree plainly what each side gets from it'): [('door',
                                                                                             'kept your word')],
 ('someone further up the road', 'take the help, and keep the plans private'): [('person', 'mentor')],
 ('someone further up the road', 'ask them how they got there, and just listen'): [('lesson',
                                                                                    'their road was not straight '
                                                                                    'either')],
 ('someone further up the road', 'act at once on the one piece of advice that changes everything'): [('mark',
                                                                                                      'took a wild '
                                                                                                      'risk')],
 ('someone further up the road', 'accept, but only if they will help {friend} as well'): [('mark',
                                                                                           'helped someone in need')],
 ('the other name for the same step', 'set the record straight, calmly, with the facts'): [('person', 'rival')],
 ('the other name for the same step', 'let the work speak: make the next piece undeniable'): [('mark',
                                                                                               'learned a skill')],
 ('the other name for the same step', 'make sure the boss knows exactly who did what'): [('person', 'boss')],
 ('the other name for the same step', 'have it out with {rival} face to face, today'): [('person', 'rival')],
 ('the other name for the same step', 'let it go: there are better things to give the energy to'): [('means',
                                                                                                     'health+.03')],
 ('the other name for the same step', 'start keeping a clear record of who does what'): [('lesson',
                                                                                          'write it down at the '
                                                                                          'time')],
 ('the other name for the same step', 'study what {rival} does well, and do it better'): [('means', 'time-.04')],
 ('the other name for the same step', 'outshine them with a bold project nobody asked for'): [('mark',
                                                                                               'took a wild risk')],
 ('the other name for the same step', 'ask {rival} out to lunch, and see whether an alliance is possible'): [('person',
                                                                                                              'friend')],
 ('the other name for the same step', 'offer, openly, to share the next piece of work, and see what they do'): [('person',
                                                                                                                 'colleague')],
 ('the job that went wrong', 'own it plainly to the people who need to hear, and fix what can be fixed'): [('mark',
                                                                                                            'owned '
                                                                                                            'up')],
 ('the job that went wrong', 'go through exactly what happened, one step at a time'): [('mark', 'learned a skill')],
 ('the job that went wrong', 'find the next opening fast, before the story spreads'): [('person', 'boss')],
 ('the job that went wrong', 'walk out for a day, then come back harder'): [('lesson', 'anger fuels a day')],
 ('the job that went wrong', 'step back from {aim.thing}, and keep the people met through it'): [('person',
                                                                                                  'friend')],
 ('the job that went wrong', 'ask for a fair review, and a second chance on the record'): [('person', 'go-between')],
 ('the job that went wrong', 'leave quietly for steadier work, and keep what was learned'): [('mark',
                                                                                              'learned a skill')],
 ('the job that went wrong', 'talk it over with {friend} before deciding anything'): [('means', 'ties+.04')],
 ('the job that went wrong', 'start again from the bottom somewhere new, wiser for it'): [('mark', 'moved away')],
 ('the job that went wrong', 'take the blame for the team, and carry on'): [('mark', 'helped someone in need')],
 ('stuck at the same step, another year', 'keep doing it well, and trust that it will be seen'): [('means',
                                                                                                   'time-.03')],
 ('stuck at the same step, another year', 'learn the one skill the next step needs, and prove it'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('stuck at the same step, another year', 'ask straight out what it takes, and set a date'): [('person', 'boss')],
 ('stuck at the same step, another year', 'change the tasks inside the same job, just to feel it move'): [('lesson',
                                                                                                           'a new '
                                                                                                           'task '
                                                                                                           'wakes '
                                                                                                           'interest')],
 ('stuck at the same step, another year', 'settle into it: a steady place has its own worth'): [('means',
                                                                                                 'health+.04')],
 ('stuck at the same step, another year', 'take an evening course while keeping the job steady'): [('place',
                                                                                                    'learn.higher')],
 ('stuck at the same step, another year', 'quietly look elsewhere, and find out the going rate'): [('means',
                                                                                                    'money+.04')],
 ('stuck at the same step, another year', 'let {aim.thing} go, and put the energy into something of your own'): [('lesson',
                                                                                                                  'ambition '
                                                                                                                  'can '
                                                                                                                  'change '
                                                                                                                  'its '
                                                                                                                  'shape')],
 ('stuck at the same step, another year', 'cut back to fewer days, and live a little more'): [('means',
                                                                                               'freedom+.05')],
 ('stuck at the same step, another year', 'leave the climbing to others, and keep the people the years brought'): [('person',
                                                                                                                    'friend')],
 ('what moving up would cost', 'pay it by the book: a budget, a plan, and a date it ends'): [('means', 'money-.05')],
 ('what moving up would cost', 'find a cheaper way to the same qualification'): [('mark', 'learned a skill')],
 ('what moving up would cost', 'pay whatever it takes: this is the step that matters'): [('means', 'money-.10')],
 ('what moving up would cost', 'go all in now, and sort out the rest later'): [('means', 'health-.04')],
 ('what moving up would cost', 'wait a year, until the family can carry it'): [('means', 'ties+.03')],
 ('what moving up would cost', 'ask the employer to pay, in return for staying two years'): [('door',
                                                                                              'kept your word')],
 ('what moving up would cost', 'let the next step go, and keep the safety already built'): [('lesson',
                                                                                             'enough can be plenty')],
 ('what moving up would cost', 'lay it out plainly to the family, and decide together'): [('means', 'ties+.04')],
 ('what moving up would cost', "let it go, and spend the know-how on work of one's own choosing"): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('what moving up would cost', 'pay it, and promise the family every weekend back'): [('mark', 'kept your word')],
 ('the offer from elsewhere', 'accept, once the terms are written down and fair'): [('means', 'money+.05')],
 ('the offer from elsewhere', 'accept, for what it will teach'): [('mark', 'learned a skill')],
 ('the offer from elsewhere', 'accept, and get the best terms anyone there has ever had'): [('person', 'patron')],
 ('the offer from elsewhere', 'accept tonight, and tell everyone tomorrow'): [('mark', 'took a wild risk')],
 ('the offer from elsewhere', 'turn it down: the family is settled here'): [('mark', 'stayed home')],
 ('the offer from elsewhere', 'ask for six months to finish the work already started'): [('door', 'kept your word')],
 ('the offer from elsewhere', 'accept, but only on condition it can be done from here'): [('means', 'freedom+.03')],
 ('the offer from elsewhere', 'turn it down, and use what it showed to start something new'): [('lesson',
                                                                                                'worth more than '
                                                                                                'expected')],
 ('the offer from elsewhere', 'take it, and bring the family along for the adventure'): [('mark', 'moved away')],
 ('the offer from elsewhere', 'let the climb end here, among old friends and neighbours'): [('person', 'friend')],
 ('the way up that was closed', 'go round by the proper route, and keep every paper in order'): [('means',
                                                                                                  'time-.04')],
 ('the way up that was closed', 'study how others in the same place got round it, and do what worked'): [('lesson',
                                                                                                          'others '
                                                                                                          'found the '
                                                                                                          'gap '
                                                                                                          'first')],
 ('the way up that was closed', 'go round, and come back one day above the ones who shut the door'): [('person',
                                                                                                       'rival')],
 ('the way up that was closed', 'go round at once, and do not look back'): [('mark', 'defied an authority')],
 ('the way up that was closed', 'go round slowly, keeping the present work during the trial'): [('means',
                                                                                                 'time-.03')],
 ('the way up that was closed', 'challenge the rule openly, and go round in the meantime'): [('place', 'rule.voice')],
 ('the way up that was closed', "let this road go, and put your effort into the family's own work"): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('the way up that was closed', 'ask someone from home already on the other road how it is done'): [('person',
                                                                                                     'go-between')],
 ('the way up that was closed', 'go round by starting something small of your own on the side'): [('place',
                                                                                                   'comm.market')],
 ('the way up that was closed', 'stop pushing at it, and give the energy to the people close by'): [('person',
                                                                                                     'neighbour')],
 ('what they say at home about the work', 'explain the plan, the steps and the hours, calmly'): [('means',
                                                                                                  'ties+.03')],
 ('what they say at home about the work', 'show them the numbers and the prospects, plainly'): [('lesson',
                                                                                                 'plain facts calm a '
                                                                                                 'room')],
 ('what they say at home about the work', 'tell them this is your life, and your choice'): [('mark',
                                                                                             'defied an authority')],
 ('what they say at home about the work', 'get upset, say too much, and apologise later'): [('means', 'ties-.03')],
 ('what they say at home about the work', 'take their worry to heart, and choose steadier work for now'): [('mark',
                                                                                                            'stayed '
                                                                                                            'home')],
 ('what they say at home about the work', 'agree to a trial year, and to look at it again together'): [('door',
                                                                                                        'kept your '
                                                                                                        'word')],
 ('what they say at home about the work', 'listen properly, then do it your way anyway, more carefully'): [('lesson',
                                                                                                            'listening '
                                                                                                            'is not '
                                                                                                            'agreeing')],
 ('what they say at home about the work', 'agree for now, and plan your own move quietly'): [('door',
                                                                                              'gave in to pressure')],
 ('what they say at home about the work', 'bring {parent} to see the workplace, and meet the people'): [('means',
                                                                                                         'ties+.04')],
 ('what they say at home about the work', 'do what the family asks, because it is theirs to ask'): [('mark',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ('{aim.rung}, and everyone knows it', 'thank the people who made it possible, and get on with the job'): [('person',
                                                                                                            'colleague')],
 ('{aim.rung}, and everyone knows it', 'look at once at what the new step demands, and start learning it'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('{aim.rung}, and everyone knows it', 'make sure the news reaches everyone who had doubts'): [('person', 'rival')],
 ('{aim.rung}, and everyone knows it', 'throw a party for everyone, and stay up until dawn'): [('person', 'friend')],
 ('{aim.rung}, and everyone knows it', 'go home, tell the family, and have a quiet supper'): [('means', 'ties+.04')],
 ('{aim.rung}, and everyone knows it', 'dress your best, and hold your head up on the first day'): [('person',
                                                                                                     'boss')],
 ('{aim.rung}, and everyone knows it', 'buy something lasting for the house to mark it'): [('means', 'money-.04')],
 ('{aim.rung}, and everyone knows it', 'visit the old hand who taught the trade, and tell them first'): [('person',
                                                                                                          'mentor')],
 ('{aim.rung}, and everyone knows it', 'take a day off, alone, and think about what comes after'): [('means',
                                                                                                     'freedom+.03')],
 ('{aim.rung}, and everyone knows it', 'celebrate with the whole team, and make it their day too'): [('means',
                                                                                                      'ties+.05')]}
