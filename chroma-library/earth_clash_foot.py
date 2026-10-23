# Footprints (plan.md workstream 3; Engine 10-19): what each option visibly leaves, compiled by build.py from the
# foot: fields of the .lib parts. FOOT[(moment, option label)] = [(kind, value), ...]; kinds person, place, means,
# mark, door, lesson. Read only with the engine's foot_on switch; earth.py carries none of it.
FOOT = {('the new rule at home', 'write down why the rule is unfair, and ask for a proper family vote'): [('lesson',
                                                                                                    'rules can be '
                                                                                                    'argued fairly')],
 ('the new rule at home', 'keep to the rule until the end of term, noting how it goes'): [('means', 'freedom-.03')],
 ('the new rule at home', 'keep to your own room in the evenings, on your own projects'): [('means', 'ties-.03')],
 ('the new rule at home', 'spend every free hour you do have with the crowd at {clash.scene}'): [('place',
                                                                                                  'gather.circle'),
                                                                                                 ('person',
                                                                                                  'friend')],
 ('the new rule at home', 'ask {clash.ally} to sit down one evening with them and {clash.holder}'): [('means',
                                                                                                      'ties+.03')],
 ('the new rule at home', 'set a strict timetable of your own, and spend the evenings by it in your room'): [('means',
                                                                                                              'time+.03')],
 ('the new rule at home', 'find a club of your own at school, and soon help run it'): [('place', 'gather.hall')],
 ('the new rule at home', 'offer a trade: keep to it most of the week, with one evening free of it'): [('lesson',
                                                                                                        'a fair '
                                                                                                        'trade can '
                                                                                                        'settle '
                                                                                                        'things')],
 ('the new rule at home', 'argue it out loud at dinner, with {sibling} on your side'): [('mark',
                                                                                         'defied an authority')],
 ('the new rule at home', 'agree to the rule, and keep to it at home'): [('mark', 'kept your word')],
 ('the list on the kitchen wall', 'agree to the list as written, and keep your part of it'): [('mark',
                                                                                               'kept your word')],
 ('the list on the kitchen wall', 'move out to a place of your own, with the sums done first'): [('mark',
                                                                                                  'left home')],
 ('the list on the kitchen wall', 'spend your evenings with the people at {clash.scene}, who take your plans seriously'): [('place',
                                                                                                                            'gather.circle')],
 ('the list on the kitchen wall', 'cook a meal for the whole house, and say warmly what you need'): [('means',
                                                                                                      'ties+.03')],
 ('the list on the kitchen wall', 'remind {clash.holder} how this family always did it, and that it worked'): [('lesson',
                                                                                                                'old '
                                                                                                                'ways '
                                                                                                                'can '
                                                                                                                'argue '
                                                                                                                'too')],
 ('the list on the kitchen wall', "join the residents' committee, where your way of running things is welcome"): [('place',
                                                                                                                   'rule.counsel')],
 ('the list on the kitchen wall', 'write a new list with {clash.ally}, and bring it to the house together'): [('person',
                                                                                                               'go-between')],
 ('the list on the kitchen wall', 'say plainly where the line is, and that it holds unless something changes'): [('person',
                                                                                                                  'rival')],
 ('the list on the kitchen wall', 'keep to the new line as written, and let the rest of the list be'): [('means',
                                                                                                         'freedom-.03')],
 ('the list on the kitchen wall', 'move back to the town you grew up in, and think it through there'): [('mark',
                                                                                                         'moved '
                                                                                                         'away')],
 ('the notice at school', 'ask through the proper channels to move to another school'): [('means', 'ties-.03')],
 ('the notice at school', 'spend the free periods in the library, with others who feel the same'): [('place',
                                                                                                     'learn.keeping')],
 ('the notice at school', 'offer a deal: top marks all year, for one exception of your choosing'): [('door',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('the notice at school', 'stand up in assembly and say the new line is wrong'): [('mark', 'defied an authority')],
 ('the notice at school', 'go along with it this year, as {sibling} did before'): [('means', 'freedom-.03')],
 ('the notice at school', 'ask {clash.ally} to put your case to {clash.holder}, with your marks to back it'): [('person',
                                                                                                                'mentor')],
 ('the notice at school', 'bring the numbers: how many it affects, and what it costs them'): [('lesson',
                                                                                               'facts carry weight '
                                                                                               'sometimes')],
 ('the notice at school', 'do what the notice asks, every day of term'): [('mark', 'kept your word')],
 ('the notice at school', 'ask {parent} for a year out at sixteen, to work out what you want'): [('means',
                                                                                                  'freedom+.06')],
 ('the notice at school', 'join the after-school nature group, where your questions are welcome'): [('place',
                                                                                                     'gather.circle'),
                                                                                                    ('person',
                                                                                                     'friend')],
 ('what the course now asks', "join the students' society, and help set its rules"): [('place', 'gather.hall')],
 ('what the course now asks', 'show {clash.holder} what your way produces, and ask for a fair trial'): [('person',
                                                                                                         'teacher')],
 ('what the course now asks', 'tell {clash.holder} straight: judge the work on results, or lose a paying student'): [('person',
                                                                                                                      'rival')],
 ('what the course now asks', 'hand the work in as asked, on the set night'): [('means', 'time-.03')],
 ('what the course now asks', 'drop the course, and give the evenings back to the people at home'): [('means',
                                                                                                      'time+.06')],
 ('what the course now asks', 'read the course rules closely, and appeal by the book'): [('lesson',
                                                                                          'the small print cuts both '
                                                                                          'ways')],
 ('what the course now asks', 'learn the approved way to the letter, and use it'): [('mark', 'learned a skill')],
 ('what the course now asks', 'walk out mid-term and put the time into a project of your own'): [('door',
                                                                                                  'turned down a '
                                                                                                  'chance')],
 ('what the course now asks', 'find the crowd at {clash.scene} who learn by doing and argue till late'): [('place',
                                                                                                           'gather.circle'),
                                                                                                          ('person',
                                                                                                           'friend')],
 ('what the course now asks', 'ask {clash.ally}, who knows both sides, to find a way through for everyone'): [('person',
                                                                                                               'go-between')],
 ('the new terms at the Saturday job', 'ask {clash.ally} to help draw up fair terms that everyone signs'): [('means',
                                                                                                             'ties+.03')],
 ('the new terms at the Saturday job', 'bring {clash.holder} the hours, written down, and the rules on young workers'): [('lesson',
                                                                                                                          'knowing '
                                                                                                                          'the '
                                                                                                                          'rules '
                                                                                                                          'helps')],
 ('the new terms at the Saturday job', 'take the new terms as they stand, and the pay with them'): [('means',
                                                                                                     'money+.03')],
 ('the new terms at the Saturday job', 'quit on the spot, and take your weekends back'): [('means', 'freedom+.06')],
 ('the new terms at the Saturday job', 'find weekend work at the farm shop, where the regulars know your name'): [('place',
                                                                                                                   'prod.land')],
 ('the new terms at the Saturday job', 'agree to the terms, and learn the work properly, start to finish'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('the new terms at the Saturday job', 'line up a better job first, then hand in your notice'): [('person', 'boss')],
 ('the new terms at the Saturday job', 'start selling what you make at the weekend market, on your own terms'): [('place',
                                                                                                                  'comm.market')],
 ('the new terms at the Saturday job', 'get the whole crew together and ask {clash.holder}, cheerfully, for fairer terms'): [('person',
                                                                                                                              'colleague')],
 ('the new terms at the Saturday job', 'speak up for all the young workers there, side by side'): [('person',
                                                                                                    'rival')],
 ('the new way of working', 'point out in the staff meeting that the change breaks the agreed terms'): [('person',
                                                                                                         'rival')],
 ('the new way of working', 'learn the new system inside out, and work to it'): [('mark', 'learned a skill')],
 ('the new way of working', 'take the better offer from across town, and say why on the way out'): [('means',
                                                                                                     'money+.06')],
 ('the new way of working', 'go out after work with the people who do the job the way you do'): [('place',
                                                                                                  'gather.night')],
 ('the new way of working', 'ask {clash.ally}, who has been here longest, to help find a middle way'): [('person',
                                                                                                         'go-between')],
 ('the new way of working', 'hand in proper notice, work it out in full, and leave on good terms'): [('mark',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('the new way of working', "join the trade's evening meetups, where people swap better ways of doing it"): [('place',
                                                                                                              'gather.talk')],
 ('the new way of working', 'propose a trial: your team works your way for a month, results on the table'): [('lesson',
                                                                                                              'results '
                                                                                                              'speak '
                                                                                                              'for '
                                                                                                              'themselves')],
 ('the new way of working', 'tell {clash.holder}, in front of everyone, that this will wreck the work'): [('mark',
                                                                                                           'defied '
                                                                                                           'an '
                                                                                                           'authority')],
 ('the new way of working', 'work the new way, every hour it asks'): [('means', 'time-.06')],
 ('what the congregation expects of the young', 'do what is asked, at every gathering, as the family always has'): [('mark',
                                                                                                                     'kept '
                                                                                                                     'your '
                                                                                                                     'word')],
 ('what the congregation expects of the young', "ask {parent} for a year's wait, to decide when older"): [('door',
                                                                                                           'turned '
                                                                                                           'down a '
                                                                                                           'chance')],
 ('what the congregation expects of the young', "find the young people's group that debates the big questions, and soon lead it"): [('place',
                                                                                                                                     'faith.seeking')],
 ('what the congregation expects of the young', 'tell {clash.ally} how you feel, all of it, and ask for help'): [('means',
                                                                                                                  'ties+.03')],
 ('what the congregation expects of the young', 'tell {clash.holder} the old ways deserve someone who means them'): [('lesson',
                                                                                                                      'doubt '
                                                                                                                      'can '
                                                                                                                      'be '
                                                                                                                      'said '
                                                                                                                      'kindly')],
 ('what the congregation expects of the young', 'join the volunteers who visit the care home, and serve that way'): [('place',
                                                                                                                      'care.houses')],
 ('what the congregation expects of the young', 'ask {clash.holder} the questions you really have, and see if there is room'): [('person',
                                                                                                                                 'mentor')],
 ('what the congregation expects of the young', 'say you will do it only if you may do it your own way'): [('mark',
                                                                                                            'defied '
                                                                                                            'an '
                                                                                                            'authority')],
 ('what the congregation expects of the young', 'go to the classes the congregation runs, and learn what is asked'): [('place',
                                                                                                                       'faith.congregation')],
 ('what the congregation expects of the young', "spend the summer at {grandparent}'s, away from it all, to think it through"): [('means',
                                                                                                                                 'freedom+.03')],
 ('what the congregation now expects', 'write to the members, and resign your place properly'): [('means',
                                                                                                  'ties-.06')],
 ('what the congregation now expects', 'look for a reading group that asks the old questions freely'): [('place',
                                                                                                         'faith.seeking')],
 ('what the congregation now expects', 'broker a deal with {clash.holder}: less asked, and a seat on the working group'): [('means',
                                                                                                                            'ties+.03')],
 ('what the congregation now expects', 'stand up at the next gathering and say what many are thinking'): [('mark',
                                                                                                           'defied '
                                                                                                           'an '
                                                                                                           'authority')],
 ('what the congregation now expects', 'take on what is asked, alongside the people you have known for years'): [('mark',
                                                                                                                  'kept '
                                                                                                                  'your '
                                                                                                                  'word')],
 ('what the congregation now expects', 'ask {clash.ally} to bring both sides to one meeting, with an agreed agenda'): [('person',
                                                                                                                        'go-between')],
 ('what the congregation now expects', 'put the figures before the members: what is asked, what it costs, who decided'): [('person',
                                                                                                                           'rival')],
 ('what the congregation now expects', "do what is asked, and take on a role in the congregation's work"): [('means',
                                                                                                             'time-.06')],
 ('what the congregation now expects', 'stop going, and give those mornings to the hills and the people you love'): [('means',
                                                                                                                      'freedom+.06')],
 ('what the congregation now expects', 'join the smaller congregation across town, where things are done the gentler way'): [('place',
                                                                                                                              'faith.congregation')],
 ("the town's new rule for the young", 'help start a youth club that meets in the school hall each week'): [('place',
                                                                                                             'gather.hall')],
 ("the town's new rule for the young", 'draw up a fairer version of the rule, and take it to {clash.ally}'): [('person',
                                                                                                               'mentor')],
 ("the town's new rule for the young", 'go to the council meeting and demand something better in return'): [('person',
                                                                                                             'rival')],
 ("the town's new rule for the young", 'keep within the new rule, and find what there is to do'): [('means',
                                                                                                    'freedom-.03')],
 ("the town's new rule for the young", "spend the summer at {grandparent}'s, out where there is room to be young"): [('means',
                                                                                                                      'freedom+.03')],
 ("the town's new rule for the young", 'collect signatures, read up on the rules, and petition the council properly'): [('lesson',
                                                                                                                         'a '
                                                                                                                         'petition '
                                                                                                                         'gets '
                                                                                                                         'read')],
 ("the town's new rule for the young", 'keep to the rule, and learn how the council makes its decisions'): [('lesson',
                                                                                                             'how '
                                                                                                             'decisions '
                                                                                                             'get '
                                                                                                             'made')],
 ("the town's new rule for the young", "make the next town's hall your own, by bus each weekend"): [('means',
                                                                                                     'ties-.03')],
 ("the town's new rule for the young", 'take your friends to the open fields at the edge of town on summer days'): [('place',
                                                                                                                     'prod.wild')],
 ("the town's new rule for the young", 'get the old neighbours and the young ones round one table, with {clash.ally} chairing'): [('person',
                                                                                                                                   'neighbour')],
 ('the plan for the town', 'propose, through the proper channels, a smaller plan both sides could accept'): [('means',
                                                                                                              'ties+.03')],
 ('the plan for the town', 'read every page of the plan, and show the council where its numbers fail'): [('lesson',
                                                                                                          'public '
                                                                                                          'plans '
                                                                                                          'have weak '
                                                                                                          'points')],
 ('the plan for the town', 'accept the plan, and get in early on whatever it brings'): [('means', 'money+.06')],
 ('the plan for the town', 'pack up and move somewhere with more life and fewer rules'): [('mark', 'moved away')],
 ('the plan for the town', 'join the neighbours who keep the allotments going, whatever the plan'): [('place',
                                                                                                      'prod.land')],
 ('the plan for the town', "follow the plan's new rules to the letter"): [('mark', 'kept your word')],
 ('the plan for the town', 'find the town that suits you best, visit it twice, then move'): [('means', 'ties-.06')],
 ('the plan for the town', "make your street's residents' group the one the council listens to"): [('place',
                                                                                                    'rule.counsel')],
 ('the plan for the town', 'throw a street party, and invite the whole council to it'): [('person', 'neighbour')],
 ('the plan for the town', 'speak at the hearing for the families and the wildlife the plan would touch'): [('person',
                                                                                                             'rival')],
 ("the club's new terms", "point out that the club's own rules say changes need a members' vote"): [('lesson',
                                                                                                     'the rule book '
                                                                                                     'works both '
                                                                                                     'ways')],
 ("the club's new terms", 'keep to the new terms for a season, and see what you learn'): [('mark',
                                                                                           'learned a skill')],
 ("the club's new terms", 'quit, and take what you are good at to the other club'): [('means', 'ties-.03')],
 ("the club's new terms", 'start something of your own with the others who feel the same'): [('place',
                                                                                              'gather.circle'),
                                                                                             ('person', 'friend')],
 ("the club's new terms", 'ask {clash.ally} to speak for the old members and the new ones together'): [('person',
                                                                                                        'mentor')],
 ("the club's new terms", 'leave at the end of the season, properly, with your place handed on'): [('means',
                                                                                                    'freedom+.06')],
 ("the club's new terms", 'find the open sessions at {clash.scene}, where you can try things your way'): [('place',
                                                                                                           'gather.hall')],
 ("the club's new terms", 'offer {clash.holder} a deal: easier terms, and two new members brought in'): [('means',
                                                                                                          'ties+.03')],
 ("the club's new terms", 'tell {clash.holder}, in front of the whole club, that the new terms are unfair'): [('person',
                                                                                                               'rival')],
 ("the club's new terms", 'keep to the new terms, alongside the friends who stay'): [('means', 'time-.06')],
 ("the club's new direction", 'accept the vote, and stay on under the new terms'): [('mark', 'kept your word')],
 ("the club's new direction", 'resign, and put the time into studying what you used to do there'): [('means',
                                                                                                     'time+.06')],
 ("the club's new direction", 'set up a new group of your own, run your way, and invite the best'): [('place',
                                                                                                      'gather.circle')],
 ("the club's new direction", 'throw an evening for old and new members alike, and get them talking'): [('person',
                                                                                                         'friend')],
 ("the club's new direction", 'speak for the founding members at the meeting: this was theirs first'): [('lesson',
                                                                                                         'old '
                                                                                                         'members '
                                                                                                         'still '
                                                                                                         'carry '
                                                                                                         'weight')],
 ("the club's new direction", 'join the older society in the next town, which keeps the old standards'): [('place',
                                                                                                           'gather.hall')],
 ("the club's new direction", 'work out with {clash.ally} terms that both old and new members can sign'): [('person',
                                                                                                            'go-between')],
 ("the club's new direction", 'tell {clash.holder} the members will leave too unless the terms change'): [('person',
                                                                                                           'rival')],
 ("the club's new direction", 'stay on with the friends there, whatever the new terms'): [('means', 'freedom-.03')],
 ("the club's new direction", 'step away quietly, and give your evenings back to your family'): [('means',
                                                                                                  'freedom+.03')],
 ('the notice by the old stretch', 'step back from the whole quarrel, and put the evenings into schoolwork'): [('means',
                                                                                                                'time+.03')],
 ('the notice by the old stretch', "start a wildlife log with {friend}, and join the young recorders' group"): [('place',
                                                                                                                 'gather.circle')],
 ('the notice by the old stretch', 'offer {clash.holder} a deal: half the work goes ahead, and the young ones tend the rest'): [('door',
                                                                                                                                 'kept '
                                                                                                                                 'your '
                                                                                                                                 'word')],
 ('the notice by the old stretch', 'make a loud fuss about it at school and in the street, with a painted sign'): [('mark',
                                                                                                                    'defied '
                                                                                                                    'an '
                                                                                                                    'authority')],
 ('the notice by the old stretch', 'let the work go ahead, and help with the replanting that is promised'): [('place',
                                                                                                              'prod.wild')],
 ('the notice by the old stretch', "ask {clash.ally} to set out both sides' case at the open meeting"): [('person',
                                                                                                          'elder')],
 ('the notice by the old stretch', 'count the nests and the wildlife for a month, and send the numbers to the paper'): [('lesson',
                                                                                                                         'counted '
                                                                                                                         'things '
                                                                                                                         'get '
                                                                                                                         'noticed')],
 ('the notice by the old stretch', 'drop the objection, and take the summer work the plan brings'): [('means',
                                                                                                      'money+.03')],
 ('the notice by the old stretch', "spend the summer at {grandparent}'s, where the country is still open"): [('means',
                                                                                                              'freedom+.03')],
 ('the notice by the old stretch', 'join the volunteers who look after the reserve across the valley each weekend'): [('place',
                                                                                                                       'prod.land')],
 ('the decision on the land nearby', 'join the association that keeps watch over the land and water, by its rules'): [('place',
                                                                                                                       'rule.counsel')],
 ('the decision on the land nearby', 'work out with {clash.ally} a version of the plan both sides can live with'): [('person',
                                                                                                                     'mentor')],
 ('the decision on the land nearby', 'tell {clash.holder} there will be a legal challenge unless the neighbours get their share'): [('person',
                                                                                                                                     'rival')],
 ('the decision on the land nearby', 'take the offer made to the neighbours, sign, and let the matter rest'): [('mark',
                                                                                                                'kept '
                                                                                                                'your '
                                                                                                                'word')],
 ('the decision on the land nearby', 'pack up and move to where the land is still worked the old way'): [('mark',
                                                                                                          'moved '
                                                                                                          'away')],
 ('the decision on the land nearby', 'find the old rights to the land in the records, and hold them to it'): [('lesson',
                                                                                                               'old '
                                                                                                               'agreements '
                                                                                                               'still '
                                                                                                               'count')],
 ('the decision on the land nearby', 'keep to the new limits, and learn to make do with what is left'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the decision on the land nearby', 'hand your part in it to a neighbour on fair terms, and step away'): [('means',
                                                                                                            'money+.03')],
 ('the decision on the land nearby', 'throw in with the group that walks, fishes and clears litter there every month'): [('place',
                                                                                                                          'prod.wild')],
 ('the decision on the land nearby', 'bring the old farmers and the planners to walk the ground together'): [('means',
                                                                                                              'ties+.03')]}
