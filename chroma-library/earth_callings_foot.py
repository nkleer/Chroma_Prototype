# Footprints (plan.md workstream 3; Engine 10-19): what each option visibly leaves, compiled by build.py from the
# foot: fields of the .lib parts. FOOT[(moment, option label)] = [(kind, value), ...]; kinds person, place, means,
# mark, door, lesson. Read only with the engine's foot_on switch; earth.py carries none of it.
FOOT = {('the board needs a chief executive', 'say no, and pour the year into your own place and its regulars'): [('place',
                                                                                                            'comm.shop')],
 ('the board needs a chief executive', 'tell the board honestly that a colleague would do it better, and back them'): [('person',
                                                                                                                        'colleague')],
 ('a rival firm is for sale', 'let it go, and build from nothing the one thing they did better'): [('mark',
                                                                                                    'learned a '
                                                                                                    'skill')],
 ('a rival firm is for sale', "hire the rival's best managers when the sale falls through"): [('person',
                                                                                               'colleague')],
 ('a rival firm is for sale', 'pass, and keep the firm the size it is, with no new debt'): [('door',
                                                                                             'turned down a chance')],
 ('the numbers that would look better moved', 'find the real cause of the gap, and show the backers a plan to close it'): [('lesson',
                                                                                                                            'every '
                                                                                                                            'gap '
                                                                                                                            'has '
                                                                                                                            'a '
                                                                                                                            'cause')],
 ('the numbers that would look better moved', 'ring every backer tonight, tell them straight, and ask them to hold their nerve'): [('person',
                                                                                                                                    'patron')],
 ('the numbers that would look better moved', 'ask the old suppliers to wait a season for their money, as in the bad years'): [('door',
                                                                                                                                'kept '
                                                                                                                                'your '
                                                                                                                                'word')],
 ('the numbers that would look better moved', 'show the staff the true figures, and cut the costs together, openly'): [('means',
                                                                                                                        'ties+.05')],
 ('the numbers that would look better moved', 'ask the old accountant who taught you the trade to audit every line early'): [('person',
                                                                                                                              'mentor')],
 ('the numbers that would look better moved', 'ask the biggest customer for an early payment, and a longer contract'): [('person',
                                                                                                                         'regular')],
 ('the market stall that became a chain', 'open one more stall, and run both well for a year before deciding'): [('place',
                                                                                                                  'comm.market')],
 ('the market stall that became a chain', 'keep it one stall, and keep the Saturdays for the joy of it'): [('means',
                                                                                                            'freedom+.05')],
 ('the market stall that became a chain', 'take an evening course in running a business while the stall keeps going'): [('place',
                                                                                                                         'learn.higher')],
 ('a seat among the merchant princes', 'speak at the guildhall against seats bought and sold, whoever wins'): [('place',
                                                                                                                'rule.voice')],
 ('officer selection', 'turn it down for now, and stay close to the friends you have'): [('means', 'ties+.04')],
 ('officer selection', 'go on the mountain leader course first, and apply again next year'): [('mark',
                                                                                               'learned a skill')],
 ('officer selection', 'ask an old officer of the town to put a name to the application'): [('person', 'patron')],
 ('officer selection', 'sit the practice papers until every score is safe, and go next year'): [('means',
                                                                                                 'time-.05')],
 ('the army needs a new general', "take command of the officers' academy instead, and remake it your own way"): [('place',
                                                                                                                  'learn.higher')],
 ('the army needs a new general', "back a rival's bid, in return for the command you really want"): [('person',
                                                                                                      'patron')],
 ('the army needs a new general', 'step aside for a better officer, and serve them as well as the last'): [('person',
                                                                                                            'boss')],
 ('the army needs a new general', 'take the far posting nobody wants, and serve where the army needs it most'): [('mark',
                                                                                                                  'moved '
                                                                                                                  'away')],
 ('the report on the night that went wrong', 'write the report true, every fact as it happened, and sign it'): [('person',
                                                                                                                 'friend '
                                                                                                                 'lost')],
 ('the report on the night that went wrong', 'visit the hurt soldier every week until they are back on their feet'): [('person',
                                                                                                                       'friend')],
 ('the report on the night that went wrong', 'rewrite the drill so no driver that tired ever takes the wheel again'): [('lesson',
                                                                                                                        'good '
                                                                                                                        'drills '
                                                                                                                        'keep '
                                                                                                                        'people '
                                                                                                                        'whole')],
 ('the report on the night that went wrong', 'write it true, and argue in it for the friend to be retrained, not punished'): [('door',
                                                                                                                               'helped '
                                                                                                                               'someone '
                                                                                                                               'in '
                                                                                                                               'need')],
 ('the report on the night that went wrong', 'go with the friend to the doctor about the sleepless nights first'): [('place',
                                                                                                                     'care.houses')],
 ('the report on the night that went wrong', 'ask the hurt soldier quietly what they want said, before writing a word'): [('person',
                                                                                                                           'colleague')],
 ('the field commission', "go before the selection board next spring, the usual way, with the general's letter"): [('person',
                                                                                                                    'patron')],
 ('the field commission', "join the army's flood rescue team, and write the drill it still uses"): [('place',
                                                                                                     'prot.rescue')],
 ('the war leader is chosen at the gathering', 'name the best leader among the other bands, and stand behind them'): [('person',
                                                                                                                       'boss')],
 ('the war leader is chosen at the gathering', "ask for a seat at the clans' council fire instead, to speak for your band"): [('place',
                                                                                                                               'rule.counsel')],
 ('the war leader is chosen at the gathering', 'give the shaman furs to ask the spirits who should lead, and abide by it'): [('means',
                                                                                                                              'money-.06')],
 ('the war leader is chosen at the gathering', 'say the clans need no war leader while no raiders come, and go home to hunt'): [('mark',
                                                                                                                                 'came '
                                                                                                                                 'home')],
 ('the war leader is chosen at the gathering', 'ask instead to keep the stores and the signal fires for all the clans'): [('place',
                                                                                                                           'prot.watch')],
 ('the congregation needs a senior minister', 'take the smaller post in the next town, and keep the family where it is rooted'): [('place',
                                                                                                                                   'faith.congregation')],
 ('the congregation needs a senior minister', 'stay with the flock you have, and study for the degree in the evenings'): [('place',
                                                                                                                           'learn.higher')],
 ('the congregation needs a senior minister', 'ask the congregation you serve first, and stand only with their blessing'): [('means',
                                                                                                                             'ties+.04')],
 ('the congregation needs a senior minister', 'offer to stand in for one set year while the panel keeps searching'): [('means',
                                                                                                                       'time-.06')],
 ('the order chooses its head', "spend the season of the election working at the order's poorest house"): [('place',
                                                                                                            'faith.orders')],
 ('the order chooses its head', 'ask the council to bind whoever is chosen to a term of ten years'): [('lesson',
                                                                                                       'power should '
                                                                                                       'have an '
                                                                                                       'end')],
 ('the order chooses its head', 'step aside for an older colleague whose turn it is, and serve under them'): [('person',
                                                                                                               'boss')],
 ("a colleague's theft the faith would rather bury", "send every slip and figure to the faith's council, and ask for an outside audit"): [('person',
                                                                                                                                           'colleague '
                                                                                                                                           'lost')],
 ("a colleague's theft the faith would rather bury", "go round to the colleague's house that evening, and have it out face to face"): [('person',
                                                                                                                                        'friend '
                                                                                                                                        'lost')],
 ("a colleague's theft the faith would rather bury", 'set up a finance committee: two signatures and an open ledger for every gift'): [('place',
                                                                                                                                        'rule.counsel')],
 ("a colleague's theft the faith would rather bury", "stand up at the faith's council and ask, on the record, where the money went"): [('person',
                                                                                                                                        'rival')],
 ("a colleague's theft the faith would rather bury", 'make the fund good from your own savings, so the poor go short of nothing'): [('means',
                                                                                                                                     'money-.06')],
 ("a colleague's theft the faith would rather bury", 'sit with the colleague, hear why, and help them own up to the congregation'): [('lesson',
                                                                                                                                      'a '
                                                                                                                                      'wrong '
                                                                                                                                      'owned '
                                                                                                                                      'can '
                                                                                                                                      'be '
                                                                                                                                      'mended')],
 ('a sermon that goes round the country', "give the talks it brings, but only in towns within a day's journey"): [('means',
                                                                                                                   'time-.05')],
 ('a sermon that goes round the country', 'answer the messages for one week, then switch the phone off and go back to work'): [('lesson',
                                                                                                                                'attention '
                                                                                                                                'passes, '
                                                                                                                                'the '
                                                                                                                                'work '
                                                                                                                                'stays')],
 ('the god speaks in the temple', 'spend the month before the council praying and listening in the temple garden'): [('place',
                                                                                                                      'faith.seeking')],
 ('the god speaks in the temple', "ask the council to rule that no oracle's word may decide the choosing"): [('lesson',
                                                                                                              'the '
                                                                                                              'law '
                                                                                                              'outlasts '
                                                                                                              'any '
                                                                                                              'oracle')],
 ('the ward needs someone in charge', 'ask to act up in the post for six months, and prove it first'): [('means',
                                                                                                         'time-.05')],
 ('the ward needs someone in charge', "go for a specialist's post instead, with better hours and better pay"): [('means',
                                                                                                                 'money+.05')],
 ('the ward needs someone in charge', 'ask the whole team at handover who they would want in charge'): [('means',
                                                                                                         'ties+.04')],
 ('patients come from far away', 'go part-time on the ward, and see the far families in a rented room'): [('means',
                                                                                                           'money+.05')],
 ('patients come from far away', 'go out to the far families yourself, one weekend a month'): [('means', 'time-.06')],
 ('patients come from far away', 'ask the managers for a clinic day of your own for the far patients'): [('place',
                                                                                                          'care.houses')],
 ('the wrong dose on the night shift', 'ring the union rep before saying a word to anyone'): [('person',
                                                                                               'go-between')],
 ('the wrong dose on the night shift', 'sit by the patient until morning, watching every breath until it passes'): [('lesson',
                                                                                                                     'stay '
                                                                                                                     'close '
                                                                                                                     'when '
                                                                                                                     'it '
                                                                                                                     'matters')],
 ('the wrong dose on the night shift', 'report it to the safety team with a plan for a second check on strong doses'): [('lesson',
                                                                                                                         'tired '
                                                                                                                         'hands '
                                                                                                                         'need '
                                                                                                                         'a '
                                                                                                                         'second '
                                                                                                                         'check')],
 ('the wrong dose on the night shift', 'put your name alone on the report, to shield the worn-out colleague'): [('door',
                                                                                                                 'kept '
                                                                                                                 'it '
                                                                                                                 'hidden')],
 ('the wrong dose on the night shift', 'ask the manager for fewer night shifts, before tiredness does it again'): [('means',
                                                                                                                    'health+.04')],
 ('the remedy that worked', 'grow the marigolds in your own garden, and teach the families to make it'): [('place',
                                                                                                           'prod.land')],
 ('the remedy that worked', "write it up for the hospital's own bulletin, with the dates and the weeks"): [('lesson',
                                                                                                            'write '
                                                                                                            'down '
                                                                                                            'what '
                                                                                                            'works')],
 ('the remedy that worked', 'ask the managers for one day a week for the wounds that will not heal'): [('means',
                                                                                                        'time-.05')],
 ('the remedy that worked', "keep it for the district's families, and turn the reporter from the paper away"): [('door',
                                                                                                                 'turned '
                                                                                                                 'down '
                                                                                                                 'a '
                                                                                                                 'chance')],
 ('the sickness in the winter camp', 'ask the elders to move the camp upriver to clean water, and plan the move'): [('lesson',
                                                                                                                     'clean '
                                                                                                                     'water '
                                                                                                                     'keeps '
                                                                                                                     'sickness '
                                                                                                                     'away')],
 ('the sickness in the winter camp', "trade the band's best furs to the next band for their healer's help"): [('means',
                                                                                                               'money-.06')],
 ('the sickness in the winter camp', 'stay in the sick shelter with the worst of them, and keep the others away'): [('means',
                                                                                                                     'health-.05')],
 ('the prototype works', 'make the first ones by hand for the street, and grow it from there'): [('person',
                                                                                                  'neighbour')],
 ('the prototype works', 'put the plans online for free, and see what other tinkerers make of it'): [('person',
                                                                                                      'colleague')],
 ('the prototype works', 'keep the job and the family evenings, and let it be a fine thing made'): [('means',
                                                                                                     'ties+.05')],
 ('the safety test you could skip', 'delay the launch a month, and run the full test as the plan says'): [('means',
                                                                                                           'money-.06')],
 ('the safety test you could skip', 'pay a test house to run it round the clock, whatever it costs'): [('means',
                                                                                                        'money-.10')],
 ('the safety test you could skip', 'launch with ten trial buyers who sign for it, and finish the test alongside'): [('lesson',
                                                                                                                      'a '
                                                                                                                      'careful '
                                                                                                                      'start '
                                                                                                                      'still '
                                                                                                                      'counts')],
 ('the safety test you could skip', 'call the team in, and run the test in shifts with them, day and night'): [('person',
                                                                                                                'colleague')],
 ('the safety test you could skip', 'ask the standards office for a staged launch: half now, the rest after the test'): [('means',
                                                                                                                          'money-.04')],
 ('the safety test you could skip', 'run the test cheaply in the yard, with what is to hand, and launch late'): [('means',
                                                                                                                  'time-.06')],
 ('the garage invention', 'make one for every neighbour who asks, and let word travel'): [('person', 'neighbour')],
 ('the garage invention', "join the inventors' club at the library, and learn how patents work first"): [('place',
                                                                                                          'learn.keeping')],
 ('the garage invention', 'let it go, and give the evenings back to the family and the job'): [('means', 'ties+.05')],
 ('the garage invention', 'build a second, better one just for the joy of it, and keep it at home'): [('place',
                                                                                                       'prod.craft')],
 ('the garage invention', 'sell the first few at the weekend market, and see who comes back for more'): [('place',
                                                                                                          'comm.market')],
 ('the guild commissions a flying ship', 'build a kite-ship for the midsummer fair, and charge for the first rides'): [('means',
                                                                                                                        'money+.05')],
 ('the guild commissions a flying ship', 'ask the guild for a year to build and test a small model first'): [('place',
                                                                                                              'prod.craft')]}
