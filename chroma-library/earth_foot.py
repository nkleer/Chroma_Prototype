# Footprints (plan.md workstream 3; Engine 10-19): what each option visibly leaves, compiled by build.py from the
# foot: fields of earth-*.lib. FOOT[(moment, option label)] = [(kind, value), ...]; kinds person, place, means,
# mark, door, lesson. Read only with the engine's foot_on switch; earth.py carries none of it.
FOOT = {('burnout', 'see the doctor, take the sick leave, and follow the plan to the letter'): [('place', 'care.houses')],
 ('burnout', 'work out what is draining your strength, and redesign your days around it'): [('lesson',
                                                                                             'know what drains you')],
 ('burnout', 'push through on coffee and willpower; you cannot afford to fall behind'): [('means', 'health-.08')],
 ('burnout', 'quit on the spot and walk out into the sunshine'): [('means', 'freedom+.08'), ('means', 'money-.08')],
 ('burnout', 'take time off, walk in the woods each day, and let your body heal slowly'): [('means', 'health+.05')],
 ('burnout', 'set hard limits on your hours, and fill the evenings with something you love'): [('means', 'time+.06')],
 ('burnout', 'stop hiding it, tell your family and friends, and lean on them'): [('means', 'ties+.06')],
 ('burnout', 'hand off what you can, keep only what matters, and outlast the bad stretch'): [('means', 'time+.04')],
 ('burnout', 'quietly pass your workload to others, and rest while they carry it'): [('door', 'kept it hidden')],
 ('a serious accident or illness', 'follow every instruction from the doctors and the physiotherapist'): [('place',
                                                                                                           'care.houses')],
 ('a serious accident or illness', 'laugh it off, and turn the ward into a party for every visitor'): [('means',
                                                                                                        'ties+.04')],
 ('a serious accident or illness', 'rest, and trust your body to heal in its own time'): [('lesson',
                                                                                           'healing will not be '
                                                                                           'hurried')],
 ('a serious accident or illness', 'plan your recovery like a project, with targets, aids and deadlines'): [('means',
                                                                                                             'health+.06')],
 ('a serious accident or illness', 'work from the hospital bed and refuse to lose your place'): [('means',
                                                                                                  'health-.05')],
 ('a serious accident or illness', 'set one fierce goal, a hill to climb by next year, and train for it'): [('means',
                                                                                                             'health+.08')],
 ('buying a home', 'take a safe fixed-rate mortgage, and never miss a payment'): [('door', 'kept your word')],
 ('buying a home', 'study the market for a year and buy only when the numbers are right'): [('means', 'money+.04')],
 ('buying a home', 'buy from a desperate seller, well below the asking price'): [('means', 'money+.08')],
 ('buying a home', 'buy the house you fell for, even if it stretches you thin'): [('means', 'money-.10')],
 ('buying a home', 'buy in the town where your family has always lived'): [('door', 'stayed home')],
 ('buying a home', 'buy close to your family, so you can all look after one another'): [('means', 'ties+.06')],
 ('buying a home', 'choose the safest, best-run street in town, after months of research'): [('person', 'neighbour')],
 ('your child falls seriously ill', "keep every appointment and every dose, and run the family's week around them"): [('place',
                                                                                                                       'care.houses')],
 ('your child falls seriously ill', 'pull every string you have until the best specialist takes them on'): [('means',
                                                                                                             'ties-.04')],
 ('your child falls seriously ill', 'move into the chair beside their bed, and refuse to leave'): [('means',
                                                                                                    'health-.06')],
 ('your child falls seriously ill', 'lean on your faith, or long walks outdoors, and take each day as it comes'): [('means',
                                                                                                                    'health+.03')],
 ('your child falls seriously ill', 'take the whole family to the sea between treatments, and live each good day'): [('means',
                                                                                                                      'money-.05')],
 ('your child falls seriously ill', 'find a trial of a new treatment, and raise the money for their place'): [('door',
                                                                                                               'took '
                                                                                                               'a '
                                                                                                               'wild '
                                                                                                               'risk')],
 ('your child falls seriously ill', 'read through the night, then take your questions straight to the ward round'): [('lesson',
                                                                                                                      'doctors '
                                                                                                                      'answer '
                                                                                                                      'when '
                                                                                                                      'asked')],
 ('your child falls seriously ill', 'keep your job and the money steady, so the care never has to stop'): [('means',
                                                                                                            'time-.06')],
 ('your child falls seriously ill', 'gather the family, and keep watch at the bedside in turns'): [('means',
                                                                                                    'ties+.05')],
 ('your child dies', 'give them the funeral the family has always held, and keep every anniversary'): [('door',
                                                                                                        'kept your '
                                                                                                        'word')],
 ('your child dies', 'read every report, and learn exactly what happened and why'): [('lesson',
                                                                                      'knowing does not undo it')],
 ('your child dies', 'go back to work within the week, and let nobody see how deep it goes'): [('door',
                                                                                                'kept it hidden')],
 ('your child dies', 'let the grief out, loud and raw, wherever and whenever it comes'): [('lesson',
                                                                                           'grief comes out its own '
                                                                                           'way')],
 ('your child dies', 'plant a tree where they loved to be, and sit by it through the seasons'): [('means',
                                                                                                  'health+.03')],
 ('your child dies', 'close the door on the world for a while, and keep the family near'): [('means', 'ties-.05')],
 ('your child dies', 'pour the anger into something hard, a marathon or a house to rebuild'): [('means', 'time-.06')],
 ('your child dies', 'ask everyone who knew them for a story, and write each one down'): [('means', 'ties+.05')],
 ('your child dies', 'stand up at the funeral and tell everyone, laughing and crying, who they were'): [('means',
                                                                                                         'ties+.04')],
 ('starting school', 'line up, listen, and learn the rules quickly'): [('lesson', 'rules make a big place smaller')],
 ('starting school', 'ask the teacher a hundred questions on the first day'): [('person', 'teacher')],
 ('starting school', 'stay close to your sibling and the kids from your street'): [('place', 'gather.circle')],
 ('starting school', 'sit at the front and do exactly what is asked, and do it well'): [('lesson',
                                                                                         'doing it well gets '
                                                                                         'noticed')],
 ('starting school', 'spend every break watching the ants by the fence'): [('place', 'prod.wild')],
 ('starting school', 'volunteer for every job, brave and eager to help'): [('means', 'ties+.03')],
 ('starting school', 'keep to your own little gang and guard your corner of the yard'): [('person', 'rival')],
 ('your parents split up', 'keep to the agreed week between the two homes, and keep up at school'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('your parents split up', 'ask each parent, on their own, for the real reasons, and compare the answers'): [('lesson',
                                                                                                              'every '
                                                                                                              'story '
                                                                                                              'has '
                                                                                                              'two '
                                                                                                              'sides')],
 ('your parents split up', 'play your parents off against each other for money, freedom and a later curfew'): [('means',
                                                                                                                'freedom+.06')],
 ('your parents split up', 'tell them both, tears and all, how much this hurts and that you love them'): [('means',
                                                                                                           'ties+.03')],
 ('your parents split up', 'move in with your grandparents for a while, away from both houses'): [('door',
                                                                                                   'left home')],
 ('your parents split up', 'refuse to change schools or leave your friends, whatever the grown-ups decide'): [('door',
                                                                                                               'stayed '
                                                                                                               'home')],
 ('your parents split up', 'listen in on their phone calls, to know what is coming before anyone says'): [('door',
                                                                                                           'hid a '
                                                                                                           'wrong')],
 ('your parents split up', 'choose which parent to live with, and argue your case to both'): [('means',
                                                                                               'freedom+.03')],
 ('your parents split up', 'get both parents to agree one set of rules, and hold them to it'): [('lesson',
                                                                                                 'fair rules can be '
                                                                                                 'asked for')],
 ('your parents split up', 'keep the peace at both houses, and keep how you feel to yourself'): [('door',
                                                                                                  'kept it hidden')],
 ('two houses from now on', 'learn the new week by heart, which nights where, and keep to it'): [('lesson',
                                                                                                  'a routine makes '
                                                                                                  'change bearable')],
 ('two houses from now on', 'ask both parents, one at a time, to explain exactly why'): [('lesson',
                                                                                          'grown-ups do not always '
                                                                                          'know why')],
 ('two houses from now on', 'pack your own bag for each house, so nothing you need is ever left behind'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ('two houses from now on', 'shout that you hate them both, and slam your door'): [('means', 'ties-.03')],
 ('two houses from now on', 'dig in your heels: you will not leave your school or your friends'): [('door',
                                                                                                    'stayed home')],
 ('two houses from now on', 'listen at doors, to know what is coming before anyone tells you'): [('door',
                                                                                                  'hid a wrong')],
 ('two houses from now on', 'hatch a plan to get your parents back together, and put it into action'): [('door',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('two houses from now on', 'make both parents agree the same rules for you, and hold them to it'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('two houses from now on', 'try to be extra good at both houses, so nobody else gets upset'): [('door',
                                                                                                 'kept it hidden')],
 ('the family moves to a new town', 'look up everything about the new town: the schools, the clubs, the buses'): [('means',
                                                                                                                   'freedom+.03')],
 ('the family moves to a new town', 'decide to reinvent yourself at the new school, as someone people look up to'): [('lesson',
                                                                                                                      'a '
                                                                                                                      'new '
                                                                                                                      'start '
                                                                                                                      'lets '
                                                                                                                      'you '
                                                                                                                      'choose')],
 ('the family moves to a new town', 'throw a loud goodbye party for your friends on the last night'): [('means',
                                                                                                        'ties+.03')],
 ('the family moves to a new town', 'walk your old streets one last time, and promise yourself you will come back'): [('door',
                                                                                                                       'came '
                                                                                                                       'home')],
 ('the family moves to a new town', 'join a team or a club in the first week, to find your feet fast'): [('place',
                                                                                                          'gather.games')],
 ('the family moves to a new town', 'set up your new room with all your old things, just as it was'): [('lesson',
                                                                                                        'old things '
                                                                                                        'make '
                                                                                                        'anywhere '
                                                                                                        'home')],
 ('the family moves to a new town', 'stay close to your family and keep a low profile until you know who to trust'): [('means',
                                                                                                                       'ties-.03')],
 ('the family moves to a new town', 'work out who runs things at the new school, and get on their side fast'): [('person',
                                                                                                                 'friend')],
 ('the family moves to a new town', 'square up to the first kid at the new school who tries to push you around'): [('person',
                                                                                                                    'rival')],
 ('moving to a new town', 'find out everything about the new town before you get there'): [('place',
                                                                                            'learn.keeping')],
 ('moving to a new town', 'decide to be someone new at the new school, someone the others look up to'): [('lesson',
                                                                                                          'you can '
                                                                                                          'start '
                                                                                                          'over '
                                                                                                          'fresh')],
 ('moving to a new town', 'refuse to pack, and lock yourself in the bathroom'): [('door', 'defied an authority')],
 ('moving to a new town', 'bury a tin of treasures in the old garden, and promise to come back for it'): [('door',
                                                                                                           'came '
                                                                                                           'home')],
 ('moving to a new town', 'join every club at the new school in the first week, to learn the place fast'): [('place',
                                                                                                             'gather.hall')],
 ('moving to a new town', 'plan the new bedroom carefully, with all your old things around you'): [('lesson',
                                                                                                    'old things make '
                                                                                                    'a new home')],
 ('moving to a new town', 'stick close to your family and keep your head down until you know who to trust'): [('means',
                                                                                                               'ties-.03')],
 ('moving to a new town', 'work out who runs the new playground, and get on their side fast'): [('person', 'friend')],
 ('moving to a new town', 'square up to the biggest kid on the first day, so nobody pushes you around'): [('person',
                                                                                                           'rival')],
 ('a grandparent dies', 'read a poem at the funeral, standing up straight in front of everyone'): [('lesson',
                                                                                                    'grief can be '
                                                                                                    'spoken aloud')],
 ('a grandparent dies', 'ask every question you have about dying, until someone gives a real answer'): [('person',
                                                                                                         'elder')],
 ('a grandparent dies', "ask for your grandparent's watch, before anyone else thinks to"): [('means', 'ties-.03')],
 ('a grandparent dies', 'cry out loud at the funeral, and not care who hears'): [('means', 'ties+.03')],
 ('a grandparent dies', 'make a careful album of the old photos and letters, and keep it as your own'): [('door',
                                                                                                          'came '
                                                                                                          'home')],
 ('a grandparent dies', "keep your grandparent's photo by your bed, and say goodnight to it every night"): [('lesson',
                                                                                                             'love '
                                                                                                             'goes '
                                                                                                             'on '
                                                                                                             'after '
                                                                                                             'goodbye')],
 ('a grandparent dies', "take over your grandparent's daily jobs, like walking the dog, and be proud of it"): [('means',
                                                                                                                'time-.03')],
 ('a grandparent dies', 'go alone to the pond where you used to fish together, and sit with it'): [('place',
                                                                                                    'prod.wild')],
 ('a grandparent dies', 'decide that crying does not help, and keep your feelings to yourself'): [('door',
                                                                                                   'kept it hidden')],
 ('a pet of your own', 'keep it in your room, and let your sibling hold it only when you say'): [('means',
                                                                                                  'ties-.03')],
 ('a pet of your own', 'play with it for hours, chasing string all over the house'): [('lesson',
                                                                                       'play is its own reward')],
 ('a pet of your own', 'let it sleep on your bed every night, curled against your feet'): [('lesson',
                                                                                            'comfort can come on '
                                                                                            'four paws')],
 ('a pet of your own', 'ask the vet how to look after it properly, and write it all down'): [('mark',
                                                                                              'learned a skill')],
 ('a pet of your own', 'teach it tricks so it wins the pet show at the school fair'): [('means', 'time-.03')],
 ('a pet of your own', 'carry it out into the garden to show it the grass and the birds'): [('place', 'prod.wild')],
 ('you are picked for something special', 'turn up early to every practice, in a clean uniform'): [('place',
                                                                                                    'arts.song')],
 ('you are picked for something special', 'say yes on the spot to every concert, before anyone can talk you out of it'): [('place',
                                                                                                                           'arts.stage')],
 ('you are picked for something special', 'ask for the solo, promising to work twice as hard for it'): [('door',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('you are picked for something special', 'find out who sang in it long ago, and learn the old songs they loved'): [('person',
                                                                                                                     'elder')],
 ('you are picked for something special', 'trust your natural gift, skip practice, and still expect the best part'): [('door',
                                                                                                                       'defied '
                                                                                                                       'an '
                                                                                                                       'authority')],
 ('the night it goes too far', 'call the police from the bathroom, and press charges this time'): [('person',
                                                                                                    'partner lost')],
 ('the night it goes too far', 'keep calm, talk them down, and plan the way out for the morning'): [('door',
                                                                                                     'left home')],
 ('the night it goes too far', 'agree to everything tonight, and empty the joint account at nine tomorrow'): [('means',
                                                                                                               'money+.06')],
 ('the night it goes too far', 'kill them, here, tonight, before they can hurt you again'): [('door',
                                                                                              'broke the law')],
 ('the night it goes too far', "stay, for the family's name and the years together, and hide the bruises again"): [('door',
                                                                                                                    'kept '
                                                                                                                    'it '
                                                                                                                    'hidden')],
 ('the night it goes too far', 'get your family round tonight, and take everything that is yours'): [('person',
                                                                                                      'partner '
                                                                                                      'lost')],
 ('the night it goes too far', 'fight your way out of the door and run to the neighbours'): [('person', 'neighbour')],
 ('the night it goes too far', 'slip out to the refuge whose number you saved months ago'): [('place',
                                                                                              'care.houses')],
 ('the night it goes too far', 'stand in front of them and say, out loud, that it ends tonight'): [('mark',
                                                                                                    'took a wild '
                                                                                                    'risk')],
 ('the night it goes too far', 'photograph everything tonight, and take it all to a lawyer in the morning'): [('means',
                                                                                                               'money-.06')],
 ('an offer from people who do not ask twice', 'ask for a day to think, and find out exactly who these people are'): [('lesson',
                                                                                                                       'a '
                                                                                                                       'day '
                                                                                                                       'can '
                                                                                                                       'buy '
                                                                                                                       'clarity')],
 ('an offer from people who do not ask twice', 'take the job, and kill the man they name, for the money'): [('door',
                                                                                                             'broke '
                                                                                                             'the '
                                                                                                             'law')],
 ('an offer from people who do not ask twice', 'ask the cousin who works for them what the job really costs'): [('person',
                                                                                                                 'go-between')],
 ('an offer from people who do not ask twice', 'turn him down politely, and remember every detail for the police'): [('door',
                                                                                                                      'turned '
                                                                                                                      'down '
                                                                                                                      'a '
                                                                                                                      'chance')],
 ('an offer from people who do not ask twice', 'agree to drive for them, and never to touch anything else'): [('door',
                                                                                                               'broke '
                                                                                                               'the '
                                                                                                               'law')],
 ('an offer from people who do not ask twice', 'ask for a job that pays twice as much and carries half the risk'): [('door',
                                                                                                                     'took '
                                                                                                                     'a '
                                                                                                                     'wild '
                                                                                                                     'risk')],
 ('an offer from people who do not ask twice', 'take it to the elders of your street, and let them deal with these people'): [('person',
                                                                                                                               'elder')],
 ('the man who hurt your family walks free', 'see that he pays with his life, since the court would not'): [('door',
                                                                                                             'broke '
                                                                                                             'the '
                                                                                                             'law')],
 ('the man who hurt your family walks free', 'find the flaw in the case, and push for an appeal until it is heard'): [('means',
                                                                                                                       'time-.06')],
 ('the man who hurt your family walks free', 'turn to your brother or sister, and spend your evenings helping them live again'): [('mark',
                                                                                                                                   'helped '
                                                                                                                                   'someone '
                                                                                                                                   'in '
                                                                                                                                   'need')],
 ('the man who hurt your family walks free', 'wait for him in the car park, and give him the beating he got away with'): [('door',
                                                                                                                           'broke '
                                                                                                                           'the '
                                                                                                                           'law')],
 ('the man who hurt your family walks free', 'dig into his past until you find something the police will want'): [('person',
                                                                                                                   'go-between')],
 ('the man who hurt your family walks free', 'set up a fund for your brother or sister, and tell the story to the papers'): [('means',
                                                                                                                              'ties+.03')],
 ('the man who hurt your family walks free', 'forgive him, slowly, so that the hate does not eat the family too'): [('lesson',
                                                                                                                     'letting '
                                                                                                                     'go '
                                                                                                                     'takes '
                                                                                                                     'years')],
 ('the man who hurt your family walks free', "campaign to change the law, with the family's photograph on every poster"): [('place',
                                                                                                                            'rule.voice')],
 ('the neighbour who wants your land', 'take the deeds to court, and let the law settle the line'): [('means',
                                                                                                      'money-.06')],
 ('the neighbour who wants your land', 'hire a surveyor, and put a camera on the boundary'): [('means', 'money-.03')],
 ('the neighbour who wants your land', 'buy up the debt on their farm, quietly, and wait'): [('means', 'money-.10')],
 ('the neighbour who wants your land', 'take the old shotgun, and shoot them when they next step onto your land'): [('door',
                                                                                                                     'broke '
                                                                                                                     'the '
                                                                                                                     'law')],
 ('the neighbour who wants your land', 'rig a floodlight and a siren on the boundary, and enjoy their fright'): [('door',
                                                                                                                  'made '
                                                                                                                  'an '
                                                                                                                  'enemy')],
 ('the neighbour who wants your land', 'offer to buy the strip, and keep the peace on your own terms'): [('means',
                                                                                                          'money-.06')],
 ('the neighbour who wants your land', 'stand at the fence every morning, and dare them to cross it'): [('means',
                                                                                                         'time-.03')],
 ('the neighbour who wants your land', 'ask the oldest neighbours where the line really ran, and listen'): [('person',
                                                                                                             'elder')],
 ('a business partner about to ruin you', 'plan their death so carefully that no one ever suspects you'): [('door',
                                                                                                            'kept it '
                                                                                                            'hidden')],
 ('a business partner about to ruin you', 'move what is left into your own name tonight, before they can'): [('door',
                                                                                                              'broke '
                                                                                                              'the '
                                                                                                              'law')],
 ('a business partner about to ruin you', 'drive to their house and have it out, right now'): [('person', 'rival')],
 ('a business partner about to ruin you', 'call the staff together, tell them the truth, and face it together'): [('door',
                                                                                                                   'owned '
                                                                                                                   'up')],
 ('a business partner about to ruin you', 'buy them out with everything you can raise, and keep the jobs alive'): [('means',
                                                                                                                    'money-.10')],
 ('a business partner about to ruin you', 'start a rival firm the next morning, and take your loyal clients with you'): [('person',
                                                                                                                          'colleague '
                                                                                                                          'lost')],
 ('a business partner about to ruin you', 'confront them with the proof in front of the board, without warning'): [('door',
                                                                                                                    'made '
                                                                                                                    'an '
                                                                                                                    'enemy')],
 ('a business partner about to ruin you', 'ask an old friend of you both to broker a settlement'): [('person',
                                                                                                     'go-between')],
 ('a business partner about to ruin you', 'have an outside accountant trace every payment, and take the case to court'): [('means',
                                                                                                                           'money-.06')],
 ('a stranger on the pavement who does not get up', 'wait by him for the police, and tell them the push was yours'): [('means',
                                                                                                                       'freedom-.05')],
 ('a stranger on the pavement who does not get up', 'walk away fast, before the camera over the door gets a good look'): [('door',
                                                                                                                           'kept '
                                                                                                                           'it '
                                                                                                                           'hidden')],
 ('a stranger on the pavement who does not get up', 'send your friend home, so they are not caught up in it'): [('lesson',
                                                                                                                 'get '
                                                                                                                 'your '
                                                                                                                 'friends '
                                                                                                                 'clear '
                                                                                                                 'first')],
 ('a stranger on the pavement who does not get up', 'give a full statement that makes clear he shoved first'): [('person',
                                                                                                                 'rival')],
 ('a stranger on the pavement who does not get up', 'ring for an ambulance and do exactly what the call handler says'): [('mark',
                                                                                                                          'helped '
                                                                                                                          'someone '
                                                                                                                          'in '
                                                                                                                          'need')],
 ('a stranger on the pavement who does not get up', 'film the whole scene on your phone, loudly, so nobody can twist it later'): [('lesson',
                                                                                                                                   'the '
                                                                                                                                   'footage '
                                                                                                                                   'tells '
                                                                                                                                   'the '
                                                                                                                                   'truth')],
 ('a stranger on the pavement who does not get up', 'stand between him and his furious friend until the paramedics come'): [('mark',
                                                                                                                             'took '
                                                                                                                             'a '
                                                                                                                             'wild '
                                                                                                                             'risk')],
 ('the first months of retirement', 'draw up a weekly timetable: volunteering Mondays, the pool Wednesdays, family Sundays'): [('place',
                                                                                                                                'gather.games')],
 ('the first months of retirement', 'enrol at the university for the degree you never had time to finish'): [('place',
                                                                                                              'learn.higher')],
 ('the first months of retirement', 'buy an old camper van and just go'): [('means', 'freedom+.06')],
 ('the first months of retirement', 'spend the mornings in the garden and the afternoons with family and friends'): [('means',
                                                                                                                      'ties+.06')],
 ('the first months of retirement', 'turn the garage into a workshop and invent things all day long'): [('place',
                                                                                                         'prod.craft')],
 ('the first months of retirement', 'take the chair of a charity board and run it like your old department'): [('place',
                                                                                                                'rule.counsel')],
 ('your partner dies', 'read everything about grief and keep a journal of each day'): [('lesson',
                                                                                        'writing it down helps')],
 ('your partner dies', 'take charge of the money and the house at once, and decide everything alone'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('your partner dies', 'let yourself fall apart, and cry wherever and whenever it comes'): [('lesson',
                                                                                             'grief comes in its own '
                                                                                             'way')],
 ('your partner dies', 'keep their chair, their garden and their routines, as if they were still here'): [('means',
                                                                                                           'ties-.03')],
 ('your partner dies', 'walk out to the hills you both loved and scatter the ashes yourself'): [('place',
                                                                                                 'prod.wild')],
 ('your partner dies', 'go through every one of their papers, looking for what they kept hidden'): [('door',
                                                                                                     'kept it '
                                                                                                     'hidden')],
 ('your partner dies', 'let the family and old friends carry you through the first year'): [('means', 'ties+.06')],
 ('your partner dies', 'join a bereavement group and follow its course week by week'): [('place', 'gather.talk')],
 ('moving to a smaller home or into care', 'move on the date the family agreed, with every box labelled'): [('mark',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('moving to a smaller home or into care', 'visit every place on the list and choose by the inspection reports'): [('place',
                                                                                                                    'care.houses')],
 ('moving to a smaller home or into care', 'sell to the highest bidder and buy the best flat money can buy'): [('means',
                                                                                                                'money+.06')],
 ('moving to a smaller home or into care', 'give the furniture to whoever will love it, and keep only the photographs'): [('lesson',
                                                                                                                           'memories '
                                                                                                                           'matter '
                                                                                                                           'more '
                                                                                                                           'than '
                                                                                                                           'things')],
 ('moving to a smaller home or into care', 'hold a farewell evening: a story for each room, then a dance in the empty one'): [('means',
                                                                                                                               'ties+.06')],
 ('moving to a smaller home or into care', 'choose a place in your own neighbourhood, with a garden, and move in slowly'): [('person',
                                                                                                                             'neighbour')],
 ('moving to a smaller home or into care', 'march into the care home office and get the best room in writing'): [('place',
                                                                                                                  'care.houses')],
 ('moving to a smaller home or into care', 'rent the house out, live on the income, and keep it in the family'): [('means',
                                                                                                                   'money+.06')],
 ('a late love', 'invite them to Sunday lunch with the family, and court them properly'): [('person', 'prospect')],
 ('a late love', 'take it slowly, and get to know them over many long conversations'): [('person', 'prospect')],
 ('a late love', 'keep your money separate and your will unchanged before it gets serious'): [('lesson',
                                                                                               'protect what you '
                                                                                               'have built')],
 ('a late love', 'kiss them at the end of the evening and see what happens'): [('person', 'prospect')],
 ('a late love', 'trust your instinct about them, and let it unfold without plans'): [('person', 'prospect')],
 ("honoured for your life's work", 'accept graciously, wear your best, and thank the committee in a proper speech'): [('means',
                                                                                                                       'ties+.03')],
 ("honoured for your life's work", 'rewrite the speech for weeks, until every word is exact'): [('lesson',
                                                                                                 'the right words '
                                                                                                 'take time')],
 ("honoured for your life's work", 'invite everyone who ever doubted you, and make sure they see it'): [('person',
                                                                                                         'rival')],
 ("honoured for your life's work", 'turn the dinner into a party, and dance with the mayor'): [('person', 'friend')],
 ("honoured for your life's work", 'say it belongs to everyone you worked beside, and share the stage with them'): [('means',
                                                                                                                     'ties+.06')],
 ("honoured for your life's work", "use your new standing on the town's committees to steer money to your own causes"): [('place',
                                                                                                                          'rule.counsel')],
 ("honoured for your life's work", 'write a frank, funny memoir of the work, mistakes and all'): [('place',
                                                                                                   'arts.page')],
 ("honoured for your life's work", 'use your new fame to raise the money to save the old woodland'): [('place',
                                                                                                       'rule.voice')],
 ("honoured for your life's work", 'spend the next year teaching an apprentice everything your hands know'): [('person',
                                                                                                               'colleague')],
 ('facing the end', 'call the family in one by one, and say what must be said'): [('means', 'ties+.06')],
 ('facing the end', 'ask for every result, and read until you understand your illness'): [('lesson',
                                                                                           'knowing is easier than '
                                                                                           'fearing')],
 ('facing the end', 'demand the best specialists, and pay for every scan and trial there is'): [('means',
                                                                                                 'money-.10')],
 ('facing the end', 'leave the hospital, cash in the savings and do everything on the list'): [('means',
                                                                                                'money-.10')],
 ('facing the end', 'go home to die among your own things, with the window open'): [('mark', 'came home')],
 ('facing the end', 'talk with the chaplain or a counsellor, and make your peace with what comes'): [('place',
                                                                                                      'faith.seeking')],
 ('facing the end', 'write a clear plan for your care and your funeral, so nobody has to guess'): [('lesson',
                                                                                                    'nobody should '
                                                                                                    'have to guess')],
 ('facing the end', 'leave your body to the medical school, so even your death teaches something'): [('mark',
                                                                                                      'helped '
                                                                                                      'someone in '
                                                                                                      'need')],
 ('who stays home with the baby', "keep your job, and plan the baby's care down to the hour"): [('lesson',
                                                                                                 'a plan makes room '
                                                                                                 'for all')],
 ('who stays home with the baby', 'take every paid week of leave yourself, and claim every benefit going'): [('means',
                                                                                                              'money+.03')],
 ('who stays home with the baby', 'go back to the work you love, and race home every night for bath time'): [('means',
                                                                                                              'time-.06')],
 ('who stays home with the baby', 'let the grandparents take the baby on weekdays, the way families always have'): [('means',
                                                                                                                     'ties+.06')],
 ('who stays home with the baby', 'pay a neighbour who raised a family to mind the baby, and both keep working'): [('person',
                                                                                                                    'neighbour')],
 ('who stays home with the baby', "ask for flexible hours, and work from home around the baby's sleeps"): [('means',
                                                                                                            'time+.06')],
 ('who stays home with the baby', 'take on extra shifts to bring in what the family now needs'): [('means',
                                                                                                   'money+.06')],
 ('who stays home with the baby', 'stay home yourself, and give the baby every hour of the first year'): [('door',
                                                                                                           'stayed '
                                                                                                           'home')],
 ('a child of your own, another way', 'put it off: travel and live well while you are young, and decide later'): [('means',
                                                                                                                   'freedom+.06')],
 ('a child of your own, another way', 'decide the two of you are family enough, and let that be your life'): [('lesson',
                                                                                                               'two '
                                                                                                               'can '
                                                                                                               'be a '
                                                                                                               'family')],
 ('a child of your own, another way', 'save hard for two years first, so whichever route you choose is paid for'): [('means',
                                                                                                                     'money+.06')],
 ('a child of your own, another way', "give your time to the family's children instead, and be the one they run to"): [('means',
                                                                                                                        'ties+.06')],
 ('a child of your own, another way', 'join a group of couples who have done it, and learn each route from them'): [('place',
                                                                                                                     'gather.talk')],
 ('telling the family who you are', 'tell them all together at the family table, calmly and with respect'): [('means',
                                                                                                              'ties+.04')],
 ('telling the family who you are', 'tell them with answers ready, and meet every question with patience'): [('lesson',
                                                                                                              'patience '
                                                                                                              'lets '
                                                                                                              'them '
                                                                                                              'catch '
                                                                                                              'up')],
 ('telling the family who you are', 'wait until you no longer depend on them, then tell them on your own terms'): [('means',
                                                                                                                    'freedom+.06')],
 ('telling the family who you are', 'say it at the big family party, out loud, and let the chips fall'): [('mark',
                                                                                                           'took a '
                                                                                                           'wild '
                                                                                                           'risk')],
 ('telling the family who you are', 'tell your grandparent first, and let the news travel through the family gently'): [('lesson',
                                                                                                                         'a '
                                                                                                                         'quiet '
                                                                                                                         'word '
                                                                                                                         'goes '
                                                                                                                         'further')],
 ('telling the family who you are', 'tell them, and walk out for good if they will not accept it'): [('door',
                                                                                                      'left home')],
 ('telling the family who you are', 'cry it out at the kitchen table, and ask for a hug'): [('means', 'health+.03')],
 ('telling the family who you are', 'ask a cousin who already knows to sit in when you tell them'): [('person',
                                                                                                      'go-between')],
 ('telling the family who you are', 'keep it from them for good, and keep the family as it is'): [('door',
                                                                                                   'kept it hidden')],
 ('telling the family who you are', 'write them a long, careful letter, and give them a week to take it in'): [('means',
                                                                                                                'freedom+.04')],
 ('an invitation for three', 'ask for a week to think, and talk it over with them both first'): [('lesson',
                                                                                                  'time to think '
                                                                                                  'helps')],
 ('an invitation for three', 'say yes, on the condition that you can leave whenever you like'): [('mark',
                                                                                                  'took a wild '
                                                                                                  'risk')],
 ('an invitation for three', 'stay, and keep the night a secret from every friend you share'): [('door',
                                                                                                 'kept it hidden')],
 ('an invitation for three', 'say not tonight, and let it grow slowly, if it is going to'): [('lesson',
                                                                                              'some things grow '
                                                                                              'slowly')],
 ('an invitation for three', 'say yes, with one rule agreed at the table: anyone can stop at any time'): [('mark',
                                                                                                           'took a '
                                                                                                           'wild '
                                                                                                           'risk')],
 ('an invitation for three', 'thank them warmly, say no, and talk it through so the friendship holds'): [('means',
                                                                                                          'ties+.03')],
 ('a holiday romance', 'enjoy every day of it, and say a proper goodbye at the bus on Saturday'): [('lesson',
                                                                                                    'a good goodbye '
                                                                                                    'matters')],
 ('a holiday romance', 'find out what their life at home is really like before going any deeper'): [('lesson',
                                                                                                     'find out '
                                                                                                     'before '
                                                                                                     'falling')],
 ('a holiday romance', 'write them a long letter on the last night, saying everything'): [('person', 'prospect')],
 ('a holiday romance', 'invite them to visit your home town, and pay for the ticket and the visa'): [('person',
                                                                                                      'prospect'),
                                                                                                     ('means',
                                                                                                      'money-.06')],
 ('a holiday romance', 'introduce them to your family on a video call on the last night'): [('person', 'prospect')],
 ('your first real job', 'work every hour you can get and save every penny, like a squirrel before winter'): [('means',
                                                                                                               'money+.06')],
 ('your first real job', 'quit the moment it gets boring, and blow the pay on a good time'): [('means',
                                                                                               'freedom+.03')],
 ('your first real job', 'come up with a better way to run your section, and pitch it to the boss'): [('person',
                                                                                                       'boss')],
 ('your first real job', 'hand most of your first pay to your family, as is expected'): [('means', 'money-.03')],
 ('your first real job', 'learn your rights at work and make sure every payslip is right'): [('mark',
                                                                                              'learned a skill')],
 ('a close friend moves away', 'plan the visits: train times, savings, the summer holidays'): [('means',
                                                                                                'money-.03')],
 ('a close friend moves away', 'help them sell what they cannot take, for a fair cut'): [('lesson',
                                                                                          'a fair deal eases a '
                                                                                          'goodbye')],
 ('a close friend moves away', 'skip school to spend their whole last day together'): [('door',
                                                                                        'defied an authority')],
 ('a close friend moves away', 'help them pack, say a proper goodbye, and let them go'): [('person', 'friend lost')],
 ('a close friend moves away', 'keep tabs on their new life online, and on whoever replaces you'): [('lesson',
                                                                                                     'watching from '
                                                                                                     'afar is '
                                                                                                     'lonely')],
 ('a close friend moves away', 'bury a time capsule together, to dig up in ten years'): [('door', 'kept your word')],
 ('a close friend moves away', 'throw the farewell party yourself, and step into their place in the group'): [('place',
                                                                                                               'gather.circle')],
 ('a close friend moves away', 'get the whole group out to wave them off on moving day, with a huge banner'): [('means',
                                                                                                                'ties+.03')],
 ('money runs out at home', 'cut back on everything without complaint, and help keep the house running'): [('mark',
                                                                                                            'helped '
                                                                                                            'someone '
                                                                                                            'in '
                                                                                                            'need')],
 ('money runs out at home', 'do cash jobs for the neighbours, and keep a cut for yourself'): [('person',
                                                                                               'neighbour')],
 ('money runs out at home', 'keep the house laughing: games, music and silly nights in for everyone'): [('lesson',
                                                                                                         'laughter '
                                                                                                         'makes hard '
                                                                                                         'times '
                                                                                                         'lighter')],
 ('money runs out at home', 'start a Saturday car wash with friends, with a rota, prices and a sign'): [('place',
                                                                                                         'gather.circle')],
 ('money runs out at home', 'lend your parent your savings, and write down exactly what they owe you'): [('means',
                                                                                                          'money-.06')],
 ('money runs out at home', 'find things in the house worth selling, and haggle hard for the best price'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('you win a scholarship or a place', 'accept, and write proper thank-you letters to everyone who helped'): [('person',
                                                                                                              'mentor')],
 ('you win a scholarship or a place', 'read everything about the new school and arrive already ahead'): [('place',
                                                                                                          'learn.keeping')],
 ('you win a scholarship or a place', 'ring everyone you know, and celebrate as loudly as you can'): [('means',
                                                                                                       'ties+.03')],
 ('you win a scholarship or a place', 'turn it down, and stay with your friends and family where you belong'): [('door',
                                                                                                                 'stayed '
                                                                                                                 'home')],
 ('you win a scholarship or a place', 'accept, and keep helping your old friends with their homework after school'): [('means',
                                                                                                                       'time-.03')],
 ('you win a scholarship or a place', 'take the place, and race to the top of the new class in the first term'): [('person',
                                                                                                                   'rival')],
 ('you win a scholarship or a place', "accept for the family's sake, and carry their hopes like a debt to repay"): [('door',
                                                                                                                     'gave '
                                                                                                                     'in '
                                                                                                                     'to '
                                                                                                                     'pressure')],
 ('you win a scholarship or a place', 'take it, and learn to fend for yourself on the long journey each day'): [('means',
                                                                                                                 'freedom+.03')],
 ('a trip far from home', "follow the group's rules and be a model guest in your host family's home"): [('lesson',
                                                                                                         'good '
                                                                                                         'guests are '
                                                                                                         'asked '
                                                                                                         'back')],
 ('a trip far from home', 'bring sweets from home and sell them at three times the price'): [('means', 'money+.03')],
 ('a trip far from home', 'report the friends who broke curfew, so the teachers pick you to lead next time'): [('person',
                                                                                                                'rival')],
 ('a trip far from home', "throw yourself into the host family's festival as if you were one of them"): [('person',
                                                                                                          'friend')],
 ('a teacher or coach who believes in you', 'do every piece of extra work they set, on time, and thank them properly'): [('person',
                                                                                                                          'mentor')],
 ('a teacher or coach who believes in you', 'ask for a reading list and work through every book on it'): [('place',
                                                                                                           'learn.keeping')],
 ('a teacher or coach who believes in you', 'ask them to put in a word for you with people who can open doors'): [('person',
                                                                                                                   'patron')],
 ('a teacher or coach who believes in you', 'throw yourself into it overnight, with everything you have got'): [('means',
                                                                                                                 'time-.06')],
 ('a teacher or coach who believes in you', 'thank them, and keep growing at your own pace'): [('lesson',
                                                                                                'your own pace is '
                                                                                                'enough')],
 ('a teacher or coach who believes in you', 'help them coach the younger kids on Saturday mornings'): [('place',
                                                                                                        'gather.games')],
 ('a teacher or coach who believes in you', 'lean on their kindness for free extra lessons'): [('mark',
                                                                                                'learned a skill')],
 ('a teacher or coach who believes in you', 'go after the top prize in your year, fired up by what they said'): [('person',
                                                                                                                  'rival')],
 ('a teacher or coach who believes in you', 'stop holding back the gift you were born with, and let it run'): [('lesson',
                                                                                                                'the '
                                                                                                                'gift '
                                                                                                                'grows '
                                                                                                                'when '
                                                                                                                'used')],
 ('a teacher who sees something in you', 'do every bit of extra work they set, neatly and on time'): [('mark',
                                                                                                       'learned a '
                                                                                                       'skill')],
 ('a teacher who sees something in you', 'ask them for harder books and puzzles, and work through every one'): [('place',
                                                                                                                 'learn.keeping')],
 ('a teacher who sees something in you', 'ask them to put you in the special group, ahead of the others'): [('means',
                                                                                                             'ties-.03')],
 ('a teacher who sees something in you', 'throw yourself into it, and talk about nothing else at home'): [('lesson',
                                                                                                           'being '
                                                                                                           'seen '
                                                                                                           'lights '
                                                                                                           'you up')],
 ('a teacher who sees something in you', 'say thank you, and keep going at your own pace'): [('lesson',
                                                                                              'your own pace is '
                                                                                              'enough')],
 ('a teacher who sees something in you', 'help them look after the little ones at the club or in the playground'): [('place',
                                                                                                                     'gather.hall')],
 ('a teacher who sees something in you', 'ask to be their helper every week, and learn how they do things'): [('person',
                                                                                                               'mentor')],
 ('a teacher who sees something in you', 'make yourself their favourite, and get all the extra help going'): [('person',
                                                                                                               'mentor')],
 ('a teacher who sees something in you', 'tell the whole class the teacher says you are the best'): [('person',
                                                                                                      'rival')],
 ('a teacher who sees something in you', 'stop hiding what you are good at, and show it off for the joy of it'): [('means',
                                                                                                                   'ties+.03')],
 ('making peace with family you had cut off', 'answer politely, and suggest one meeting on neutral ground'): [('means',
                                                                                                               'ties+.03')],
 ('making peace with family you had cut off', 'ask them in writing what has changed, before agreeing to anything'): [('lesson',
                                                                                                                      'the '
                                                                                                                      'story '
                                                                                                                      'has '
                                                                                                                      'two '
                                                                                                                      'sides')],
 ('making peace with family you had cut off', 'make peace now, with one eye on the family money'): [('door',
                                                                                                     'kept it '
                                                                                                     'hidden')],
 ('making peace with family you had cut off', 'ring them that night and pour out everything held in for years'): [('mark',
                                                                                                                   'took '
                                                                                                                   'a '
                                                                                                                   'wild '
                                                                                                                   'risk')],
 ('making peace with family you had cut off', 'write a letter owning your part, and post it the same night'): [('door',
                                                                                                                'owned '
                                                                                                                'up')],
 ('making peace with family you had cut off', 'ask an old aunt or a family friend to bring you together, and keep the peace'): [('person',
                                                                                                                                 'go-between')],
 ('making peace with family you had cut off', 'agree to family occasions only, with clear limits, and nothing more'): [('place',
                                                                                                                        'gather.house')],
 ('making peace with family you had cut off', 'test them first with a small secret, and see whether it travels'): [('lesson',
                                                                                                                    'trust '
                                                                                                                    'is '
                                                                                                                    'tested '
                                                                                                                    'in '
                                                                                                                    'small '
                                                                                                                    'things')],
 ('making peace with family you had cut off', 'turn up on their doorstep unannounced, and settle it face to face'): [('mark',
                                                                                                                      'came '
                                                                                                                      'home')],
 ('a parent dies', 'keep every funeral custom, and stand beside the family the whole day'): [('means', 'ties+.03')],
 ('a parent dies', 'ask every question about how and why they died, until it makes sense'): [('means', 'health+.03')],
 ('a parent dies', 'decide nobody will ever see you cry, and look after yourself from now on'): [('door',
                                                                                                  'kept it hidden')],
 ('a parent dies', 'cry and rage at everyone, and slam every door in the house'): [('means', 'ties-.03')],
 ('a parent dies', 'plant something where they lie, and tend it every season'): [('means', 'time-.03')],
 ('a parent dies', 'go alone to their favourite place, and let the grief out where nobody can see'): [('lesson',
                                                                                                       'grief needs '
                                                                                                       'somewhere to '
                                                                                                       'go')],
 ('a parent dies', 'go through their things alone, looking for what they never told anyone'): [('door',
                                                                                                'hid a wrong')],
 ('a parent dies', 'make a book of everything you remember about them, before it fades'): [('lesson',
                                                                                            'memories fade unless '
                                                                                            'kept')],
 ('a parent dies', 'stand up at the funeral, voice shaking, and read out what you wrote for them'): [('means',
                                                                                                      'ties+.03')],
 ('losing a parent too soon', 'put on your good clothes, and sit still and straight through the funeral'): [('means',
                                                                                                             'ties+.02')],
 ('losing a parent too soon', 'ask the grown-ups where they have gone, again and again, until an answer fits'): [('lesson',
                                                                                                                  'some '
                                                                                                                  'answers '
                                                                                                                  'never '
                                                                                                                  'quite '
                                                                                                                  'fit')],
 ('losing a parent too soon', 'decide not to need anybody, and look after yourself from now on'): [('means',
                                                                                                    'ties-.03')],
 ('losing a parent too soon', 'scream into the pillow, and slam the door on anyone who tries to help'): [('means',
                                                                                                          'ties-.02')],
 ('losing a parent too soon', 'help plant flowers by their grave, and water them on every visit'): [('means',
                                                                                                     'time-.02')],
 ('losing a parent too soon', 'run to the spot outdoors they loved best, and cry there as long as you need'): [('lesson',
                                                                                                                'crying '
                                                                                                                'out '
                                                                                                                'loud '
                                                                                                                'helps')],
 ('losing a parent too soon', 'creep into their room when nobody is looking, and go through their things'): [('door',
                                                                                                              'kept '
                                                                                                              'it '
                                                                                                              'hidden')],
 ('losing a parent too soon', "make a memory box of their photos and treasures, with the family's help"): [('means',
                                                                                                            'ties+.03')],
 ('losing a parent too soon', 'do little jobs around the house, so the family can manage without them'): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('losing a parent too soon', 'say goodbye to them out loud at the funeral, in front of everyone'): [('means',
                                                                                                      'ties+.02')],
 ('a brother or sister dies', "trace the family's health history, to learn what took them"): [('means',
                                                                                               'health+.03')],
 ('a brother or sister dies', 'get straight back to work or school, and let nobody see how hard it hit'): [('means',
                                                                                                            'health-.03')],
 ('a brother or sister dies', 'take up the plans they never got to, and live them out'): [('mark',
                                                                                           'took a wild risk')],
 ('a brother or sister dies', 'go back alone to where you grew up together, and walk the old paths'): [('mark',
                                                                                                        'came home')],
 ('a brother or sister dies', 'settle their affairs line by line, so nobody can cheat their family'): [('means',
                                                                                                        'time-.06')],
 ('a brother or sister dies', 'ask that the next baby born in the family carry their name'): [('lesson',
                                                                                               'a name keeps them '
                                                                                               'near')],
 ('a brother or sister dies', 'hold the wake your own way, in the woods they loved, with their music'): [('lesson',
                                                                                                          'grief can '
                                                                                                          'be done '
                                                                                                          'your '
                                                                                                          'way')],
 ('a brother or sister dies', 'keep their secrets, and burn the letters nobody else should read'): [('door',
                                                                                                     'kept it '
                                                                                                     'hidden')],
 ("a partner's affair comes to light", 'sort out your own money, home and work first, then decide about them'): [('means',
                                                                                                                  'money+.03')],
 ("a partner's affair comes to light", 'throw their things out of the window into the street'): [('door',
                                                                                                  'made an enemy')],
 ("a partner's affair comes to light", 'pack a bag that night, walk out, and let them do the chasing'): [('person',
                                                                                                          'partner '
                                                                                                          'lost')],
 ("a partner's affair comes to light", 'ask what was missing between you, and try counselling together'): [('place',
                                                                                                            'gather.talk')],
 ("a partner's affair comes to light", 'ask every question, there and then, until you understand what happened'): [('lesson',
                                                                                                                    'the '
                                                                                                                    'truth '
                                                                                                                    'hurts '
                                                                                                                    'less '
                                                                                                                    'than '
                                                                                                                    'guessing')],
 ("a partner's affair comes to light", 'see a lawyer before saying a word, and get everything in writing'): [('means',
                                                                                                              'money-.03')],
 ('betrayed by a friend or a business partner', 'take it to the police and the courts, and see it through to the end'): [('means',
                                                                                                                          'money-.06')],
 ('betrayed by a friend or a business partner', 'take what is left, the tools, the van, the last clients, before they do'): [('means',
                                                                                                                              'money+.06')],
 ('betrayed by a friend or a business partner', 'cut them off without a word, and never speak their name again'): [('person',
                                                                                                                    'friend '
                                                                                                                    'lost')],
 ('betrayed by a friend or a business partner', 'forgive them once, and agree in writing how they will pay it back'): [('door',
                                                                                                                        'kept '
                                                                                                                        'your '
                                                                                                                        'word')],
 ('betrayed by a friend or a business partner', 'trust nobody with money again, and rebuild alone from nothing'): [('means',
                                                                                                                    'ties-.06')],
 ('a friend for life', 'spend every free hour together, and let everything else wait'): [('means', 'time-.06')],
 ('a friend for life', 'set a regular day each week to learn something new together'): [('mark', 'learned a skill')],
 ('a friend for life', 'make use of everything they have, for adventures you could never afford alone'): [('mark',
                                                                                                           'took a '
                                                                                                           'wild '
                                                                                                           'risk')],
 ('a friend for life', 'bring them home and make them part of the family: meals, holidays, everything'): [('place',
                                                                                                           'gather.house')],
 ('a best friend of your own', 'ask them a hundred questions, and remember every answer'): [('person', 'friend')],
 ('a best friend of your own', 'play together every single day, and forget about everything else'): [('person',
                                                                                                      'friend')],
 ('a best friend of your own', 'be happy just being together, even doing nothing much at all'): [('person',
                                                                                                  'friend')],
 ('a best friend of your own', 'set a day each week to do homework together and test each other'): [('lesson',
                                                                                                     'two heads '
                                                                                                     'learn faster')],
 ('a best friend of your own', 'make the most of everything they have: the trampoline, the games, the dog'): [('place',
                                                                                                               'gather.house')],
 ('a long-lost relative finds you', 'write back warmly, and arrange to meet properly, with the family there'): [('person',
                                                                                                                 'friend')],
 ('a long-lost relative finds you', 'find out what they want before you let them near the family'): [('lesson',
                                                                                                      'caution keeps '
                                                                                                      'the family '
                                                                                                      'safe')],
 ('a long-lost relative finds you', 'go and meet them that very week, wherever they live'): [('person', 'friend')],
 ('a long-lost relative finds you', 'tell them the old family stories, so they know where they belong'): [('door',
                                                                                                           'took '
                                                                                                           'them '
                                                                                                           'in')],
 ('a long-lost relative finds you', 'welcome them properly, but only once a test has proved the claim'): [('person',
                                                                                                           'friend')],
 ('a long-lost relative finds you', 'visit the old village the family came from together, and learn its story'): [('mark',
                                                                                                                   'came '
                                                                                                                   'home')],
 ('a narrow escape', 'wait for the signal every time from now on, and look both ways even then'): [('means',
                                                                                                    'health+.03')],
 ('a narrow escape', 'work out exactly how it happened, so it never happens again'): [('lesson',
                                                                                       'half a second makes the '
                                                                                       'difference')],
 ('a narrow escape', 'milk the fright for all the sympathy and favours it brings'): [('means', 'ties+.02')],
 ('a narrow escape', 'live boldly from now on, since you were spared'): [('mark', 'took a wild risk')],
 ('a narrow escape', 'spend the day outdoors, glad of the sun on your face and the ground underfoot'): [('lesson',
                                                                                                         'glad just '
                                                                                                         'to be '
                                                                                                         'alive')],
 ('a narrow escape', 'drop whatever wastes your time, and spend it on the people you love'): [('means', 'ties+.06')],
 ('a narrow escape', 'start a loud campaign for a traffic camera at that corner'): [('place', 'rule.voice')],
 ('a narrow escape', 'go somewhere quiet, and think long about what really matters now'): [('place',
                                                                                            'faith.seeking')],
 ('a close call on the road', 'say sorry for running out, and promise to stop, look and listen every time'): [('door',
                                                                                                               'kept '
                                                                                                               'your '
                                                                                                               'word')],
 ('a close call on the road', 'ask question after question about it, until you know exactly what happened'): [('lesson',
                                                                                                               'how '
                                                                                                               'close '
                                                                                                               'close '
                                                                                                               'really '
                                                                                                               'is')],
 ('a close call on the road', 'make the most of the fuss: the cuddles, the treats, the ice cream'): [('lesson',
                                                                                                      'a fright '
                                                                                                      'brings '
                                                                                                      'treats')],
 ('a close call on the road', 'laugh it off, and run straight back out to play'): [('mark', 'took a wild risk')],
 ('a close call on the road', 'lie in bed listening to the house, glad of every ordinary sound'): [('means',
                                                                                                    'ties+.02')],
 ('a close call on the road', "insist it was the driver's fault, because cars are meant to stop for children"): [('door',
                                                                                                                  'hid '
                                                                                                                  'a '
                                                                                                                  'wrong')],
 ('a close call on the road', 'use the fright to keep the family close around you all evening'): [('means',
                                                                                                   'ties+.03')],
 ('a close call on the road', 'tell the whole class, loudly and at length, always to stop and look'): [('mark',
                                                                                                        'helped '
                                                                                                        'someone in '
                                                                                                        'need')],
 ('a close call on the road', 'sit at the window a long while, watching the cars, until you understand them'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('robbed or attacked in the street', 'report it at once, give a full statement, and see it through to court'): [('means',
                                                                                                                  'time-.03')],
 ('robbed or attacked in the street', 'study the streets and change your routes, so it cannot happen again'): [('lesson',
                                                                                                                'know '
                                                                                                                'the '
                                                                                                                'streets '
                                                                                                                'you '
                                                                                                                'walk')],
 ('robbed or attacked in the street', 'make yourself a hard target: never alone, never lost, never soft'): [('means',
                                                                                                             'freedom-.03')],
 ('robbed or attacked in the street', 'stop going out after dark, and keep close to home and your own'): [('means',
                                                                                                           'freedom-.06')],
 ('robbed or attacked in the street', 'take up boxing, and get strong enough that nobody tries it again'): [('place',
                                                                                                             'gather.games')],
 ("your child's big success", 'make a proper speech at the family dinner, and give them a gift to keep'): [('means',
                                                                                                            'money-.03')],
 ("your child's big success", 'ask what they want to do with it, and help them plan the next step'): [('means',
                                                                                                       'time-.03')],
 ("your child's big success", 'boast about it everywhere, as if it were your own success'): [('person', 'rival')],
 ("your child's big success", 'throw a huge party and tell everyone you have ever met'): [('means', 'money-.06')],
 ("your child's big success", 'step back, and let them make their own way from here'): [('lesson',
                                                                                         'letting go is part of '
                                                                                         'loving')],
 ("your child's big success", "hang the photograph on the family wall, beside the grandparents'"): [('lesson',
                                                                                                     'each '
                                                                                                     'generation '
                                                                                                     'adds a face')],
 ("your child's big success", 'go through the contract and the small print with them, line by line'): [('means',
                                                                                                        'time-.02')],
 ("your child's big success", 'ring your contacts to open the next door for them'): [('means', 'ties-.03')],
 ("your child's big success", 'push them, while the fire is lit, to aim even higher'): [('means', 'ties-.02')],
 ("your child's big success", 'take them off somewhere wild for a weekend, just the two of you'): [('means',
                                                                                                    'ties+.03')],
 ('your closest friend dies', 'go to every memorial and anniversary for them, and never miss one'): [('means',
                                                                                                      'time-.03')],
 ('your closest friend dies', 'decide life is too short, and start taking what you want from it'): [('means',
                                                                                                     'freedom+.06')],
 ('your closest friend dies', 'speak at the funeral, and promise out loud to live the way they did'): [('door',
                                                                                                        'kept your '
                                                                                                        'word')],
 ('your closest friend dies', 'keep to the few friends you have left, and let nobody new in'): [('means',
                                                                                                 'ties-.06')],
 ('your closest friend dies', 'plan the memorial yourself, every reading and song exactly as they would want'): [('lesson',
                                                                                                                  'a '
                                                                                                                  'goodbye '
                                                                                                                  'can '
                                                                                                                  'be '
                                                                                                                  'well '
                                                                                                                  'made')],
 ('your closest friend dies', 'step into their place on the project, and finish it as well as they would have'): [('person',
                                                                                                                   'colleague')],
 ('your closest friend dies', 'hand in your notice that week, and chase the life they always told you to'): [('mark',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk'),
                                                                                                             ('means',
                                                                                                              'money-.06')],
 ('losing a grandparent', "sit with the old letters and photographs, and write down the family's story"): [('lesson',
                                                                                                            'every '
                                                                                                            'family '
                                                                                                            'has a '
                                                                                                            'story')],
 ('losing a grandparent', 'help clear the house, and ask for the keepsake in return'): [('means', 'money+.02')],
 ('losing a grandparent', 'drop everything and go at once, to see them before the coffin is closed'): [('mark',
                                                                                                        'came home')],
 ('losing a grandparent', 'take on the old recipes and the garden, and keep them going as they did'): [('mark',
                                                                                                        'learned a '
                                                                                                        'skill')],
 ('losing a grandparent', 'argue hard against selling the old house, so it stays in the family'): [('door',
                                                                                                    'made an enemy')],
 ('losing a grandparent', 'walk their old walk alone, all day, until the grief settles'): [('lesson',
                                                                                            'grief eases on the '
                                                                                            'move')],
 ('losing a grandparent', 'step up and organise what needs doing, since nobody else will'): [('means', 'time-.03')],
 ('losing a grandparent', 'prepare a few careful words for the funeral, telling their life in order'): [('means',
                                                                                                         'ties+.03')],
 ('a breakthrough in your work', 'take it to your mentor first, and let them judge it before anyone else hears'): [('person',
                                                                                                                    'mentor')],
 ('a breakthrough in your work', 'keep it secret until you have worked out how to profit from it'): [('means',
                                                                                                      'money+.06')],
 ('a breakthrough in your work', 'tell everyone you know tonight, without checking a thing'): [('mark',
                                                                                                'took a wild risk')],
 ('a breakthrough in your work', 'take it as a gift, and fold it quietly into the everyday work'): [('lesson',
                                                                                                     'the work '
                                                                                                     'itself is '
                                                                                                     'enough')],
 ('a breakthrough in your work', 'check it three times, write it up, and send it to the judges of such work'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('a breakthrough in your work', 'make sure it is on record under your own name before anyone can copy it'): [('means',
                                                                                                               'money+.05')],
 ('a breakthrough in your work', 'say nothing, and let it grow quietly until you are far ahead of the rest'): [('door',
                                                                                                                'kept '
                                                                                                                'it '
                                                                                                                'hidden')],
 ('an operation gives something back', 'follow the recovery plan to the letter, every exercise, every day'): [('means',
                                                                                                               'health+.06')],
 ('an operation gives something back', 'read up on how the operation works, and ask the surgeon every question you have'): [('lesson',
                                                                                                                             'knowing '
                                                                                                                             'how '
                                                                                                                             'it '
                                                                                                                             'works '
                                                                                                                             'helps')],
 ('an operation gives something back', 'take charge of your own recovery, and be back on your feet before anyone expects'): [('means',
                                                                                                                              'freedom+.06')],
 ('an operation gives something back', 'take it slowly, and let the body heal at its own pace'): [('lesson',
                                                                                                   'healing cannot '
                                                                                                   'be hurried')],
 ('an operation gives something back', 'keep every rule of recovery, so you can run, dance or play again by summer'): [('place',
                                                                                                                        'gather.games')],
 ('an operation gives something back', 'learn how the body heals, and work with it rather than against it'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('an operation gives something back', 'promise yourself a reward for every week the exercises get done'): [('mark',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('an operation gives something back', 'test what the new body can do, a little further each day, to find its limits'): [('means',
                                                                                                                          'health+.05')],
 ('an operation gives something back', 'let the family carry everything for months, long after you need them to'): [('means',
                                                                                                                     'ties-.05')],
 ('an operation that makes things better', 'keep every rule the nurse gave you, even the boring ones'): [('means',
                                                                                                          'health+.06')],
 ('an operation that makes things better', 'ask the doctor to show you the pictures, and explain what they did'): [('lesson',
                                                                                                                    'asking '
                                                                                                                    'makes '
                                                                                                                    'it '
                                                                                                                    'less '
                                                                                                                    'scary')],
 ('an operation that makes things better', 'enjoy being fussed over, and ask for ice cream and the remote'): [('means',
                                                                                                               'ties+.03')],
 ('an operation that makes things better', 'race back out to play long before you are allowed'): [('mark',
                                                                                                   'defied an '
                                                                                                   'authority')],
 ('an operation that makes things better', 'rest, and let it mend in its own good time'): [('lesson',
                                                                                            'rest does its own '
                                                                                            'work')],
 ('an operation that makes things better', "keep to the doctor's rules, so you can be out playing again by summer"): [('place',
                                                                                                                       'gather.games')],
 ('an operation that makes things better', 'ask how the body heals itself, and watch it get better day by day'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('an operation that makes things better', 'bargain for a treat for every day you stick to the rules without a fuss'): [('mark',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('an operation that makes things better', 'try out what you can do now, a little more each day, just to see'): [('means',
                                                                                                                  'health+.05')],
 ('an operation that makes things better', 'let the family wait on you for weeks, long after you need it'): [('means',
                                                                                                              'ties-.04')],
 ('earning a qualification', 'go straight on to the next level of study, years more of it'): [('place',
                                                                                               'learn.higher')],
 ('earning a qualification', 'use it at once to bargain for more: more money, more say, a better place'): [('means',
                                                                                                            'money+.06')],
 ('earning a qualification', 'throw the biggest party anyone can remember'): [('person', 'friend')],
 ('earning a qualification', 'put the paper away in a drawer; the work matters, not the certificate'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('earning a qualification', 'hold a proper family celebration, with the grandparents in the place of honour'): [('means',
                                                                                                                  'ties+.05')],
 ('earning a qualification', 'pull every string you can to get into the best course there is'): [('person',
                                                                                                  'patron')],
 ('earning a qualification', 'ride the high, and apply that same week for the next rung up'): [('mark',
                                                                                                'took a wild risk')],
 ('earning a qualification', 'spend the whole summer outdoors before deciding anything at all'): [('means',
                                                                                                   'freedom+.05')],
 ('the badge you worked for', 'start on the next grade straight away, and the one after that'): [('mark',
                                                                                                  'learned a skill')],
 ('the badge you worked for', 'ask for a reward for it: a later bedtime, more pocket money'): [('means',
                                                                                                'freedom+.03')],
 ('the badge you worked for', 'beg for a party, and invite the whole class'): [('person', 'friend')],
 ('the badge you worked for', 'put it away in a drawer, and just go on enjoying the thing itself'): [('lesson',
                                                                                                      'the fun is in '
                                                                                                      'doing it')],
 ('the badge you worked for', 'show it to the grandparents first, and let them make a fuss'): [('means', 'ties+.04')],
 ('the badge you worked for', 'talk the grown-ups into lessons with the best teacher around'): [('person',
                                                                                                 'teacher')],
 ('the badge you worked for', 'spend the rest of the summer outdoors, with no lessons at all'): [('means',
                                                                                                  'freedom+.05')],
 ('money worries end', 'buy yourself the expensive thing you were refused all those years'): [('means', 'money-.06')],
 ('money worries end', 'keep every spare penny inside the family, and turn away the friend who asks'): [('person',
                                                                                                         'friend '
                                                                                                         'lost')],
 ('a stranger saves you, or you save one', 'go back to the spot and work out exactly what went wrong'): [('lesson',
                                                                                                          'know the '
                                                                                                          'water '
                                                                                                          'before '
                                                                                                          'trusting '
                                                                                                          'it')],
 ('a stranger saves you, or you save one', 'sell the story and the video to whoever pays most'): [('means',
                                                                                                   'money+.05')],
 ('a stranger saves you, or you save one', 'hug the stranger and cry, right there on the shore'): [('person',
                                                                                                    'friend')],
 ('a stranger saves you, or you save one', 'take it as a sign that you were meant to be there, that day'): [('lesson',
                                                                                                             'some '
                                                                                                             'days '
                                                                                                             'you '
                                                                                                             'are '
                                                                                                             'needed')],
 ('a stranger saves you, or you save one', 'use all the attention to push the council for a rail and a lifebuoy'): [('place',
                                                                                                                     'rule.voice')],
 ('a stranger to the rescue', 'ask exactly what went wrong, and how the stranger knew what to do'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('a stranger to the rescue', 'tell the story at school until everyone wants to hear it'): [('means', 'ties+.04')],
 ('a stranger to the rescue', 'cling to the stranger and cry, and refuse to let go'): [('person', 'friend')],
 ('a stranger to the rescue', 'decide that someone was looking out for you that day'): [('lesson',
                                                                                         'help can come from '
                                                                                         'nowhere')],
 ('a stranger to the rescue', 'start swimming lessons, and keep at them until you can swim a length'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('a stranger to the rescue', 'use your picture in the paper to warn other children about the lake'): [('mark',
                                                                                                        'helped '
                                                                                                        'someone in '
                                                                                                        'need')],
 ('a stranger to the rescue', 'go back into the water next week, with a grown-up close by, to beat the fear'): [('lesson',
                                                                                                                 'the '
                                                                                                                 'water '
                                                                                                                 'can '
                                                                                                                 'be '
                                                                                                                 'trusted '
                                                                                                                 'again')],
 ('a cause you fought for wins', 'go home, tend your own garden, and let others carry the movement on'): [('means',
                                                                                                           'time+.06')],
 ('financial ruin', 'file for bankruptcy properly, declare everything, and start again from nothing'): [('means',
                                                                                                         'money-.10')],
 ('financial ruin', 'retrain in a new trade, and build a new business from the wreck of the old'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('financial ruin', 'pay the friends and small traders you owe first, and keep nothing back'): [('mark',
                                                                                                 'kept your word')],
 ('financial ruin', 'walk away from the wreck, leave town, and start over where nobody knows you'): [('mark',
                                                                                                      'moved away')],
 ('losing the home', 'go to legal aid, pay what you can, and keep every letter in order'): [('means', 'money-.05')],
 ('losing the home', 'take any room at all in the same neighbourhood, to stay near your roots'): [('person',
                                                                                                   'neighbour')],
 ('losing the home', 'move somewhere cheaper, save for years, and buy a small place nobody can take'): [('mark',
                                                                                                         'moved '
                                                                                                         'away'),
                                                                                                        ('means',
                                                                                                         'money+.06')],
 ('losing the home', 'sell almost everything, live out of a van, and see where the road goes'): [('means',
                                                                                                  'freedom+.10')],
 ('war comes', 'keep your head down, hide the food, and plan every road out'): [('door', 'kept it hidden')],
 ('war comes', 'bar the door, keep every scrap of food for your own, and turn strangers away'): [('means',
                                                                                                  'ties-.06')],
 ('war comes', 'dig in for a long war: ration, store, and keep the household going for years'): [('means',
                                                                                                  'money-.06')],
 ('war comes', 'put your trade to work for the war: the factory, the radio room, the field hospital'): [('place',
                                                                                                         'prot.host')],
 ('war comes', 'take up arms with the neighbours, and hold the street yourselves'): [('place', 'prot.watch'),
                                                                                     ('mark', 'took a wild risk')],
 ('war comes', 'slip across the border before the call-up, and start over wherever you land'): [('mark',
                                                                                                 'moved away'),
                                                                                                ('door',
                                                                                                 'broke the law')],
 ('a public scandal', 'own up in public, and name everyone else who was in on it too'): [('person', 'rival')],
 ('a public scandal', 'face them all down, head up, and refuse to hide'): [('lesson', 'head up, the talk fades')],
 ('a public scandal', 'stay out of sight for a while, and let it blow over'): [('means', 'ties-.05')],
 ('a public scandal', 'get someone everyone respects to vouch for you in public'): [('person', 'patron')],
 ('a public scandal', 'write your whole side of it, honestly and at length, where everyone can read it'): [('door',
                                                                                                            'owned '
                                                                                                            'up')],
 ('a public scandal', 'quietly call in favours until the group takes you back'): [('person', 'go-between')],
 ('a public scandal', 'go to each person you hurt, face to face, and say sorry'): [('means', 'ties+.05')],
 ('a public scandal', 'talk it through with the oldest, wisest person you know, until you understand it'): [('person',
                                                                                                             'elder')],
 ('a heart attack or stroke', 'take every pill, keep every appointment, and keep to the diet to the letter'): [('means',
                                                                                                                'health+.06')],
 ('a heart attack or stroke', 'track every number, and test what brings each one down'): [('mark',
                                                                                           'learned a skill')],
 ('a heart attack or stroke', 'hide how bad it was, and go back early, so nobody thinks you are slipping'): [('door',
                                                                                                              'kept '
                                                                                                              'it '
                                                                                                              'hidden')],
 ('a heart attack or stroke', 'go back to the old habits within the month; life is for living'): [('means',
                                                                                                   'health-.06')],
 ('a heart attack or stroke', 'slow your whole life down: fewer hours, more walks, early nights'): [('means',
                                                                                                     'time+.06')],
 ('a heart attack or stroke', 'join the rehabilitation class, do every drill, and enter a charity walk'): [('place',
                                                                                                            'care.houses')],
 ('a heart attack or stroke', 'pay for the best private specialist, and get the whole family checked too'): [('means',
                                                                                                              'money-.08')],
 ('a heart attack or stroke', 'climb the steepest hill around, to find out what the heart can take now'): [('mark',
                                                                                                            'took a '
                                                                                                            'wild '
                                                                                                            'risk')],
 ('living with a chronic illness', 'learn the routine, and keep it every single day without fail'): [('means',
                                                                                                      'health+.06')],
 ('living with a chronic illness', 'read every study, and test on yourself what helps and what does not'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('living with a chronic illness', 'fit it into your days on your own terms, and ask nobody for favours'): [('means',
                                                                                                             'freedom+.05')],
 ('living with a chronic illness', 'accept it as your lot, and make room for it without a fuss'): [('lesson',
                                                                                                    'make room and '
                                                                                                    'carry on')],
 ('living with a chronic illness', 'refuse to be slowed down, and train harder than anyone around you'): [('place',
                                                                                                           'gather.games')],
 ('living with a chronic illness', 'go back to the outdoors, walk every day, and let the body find its own strength'): [('means',
                                                                                                                         'health+.05')],
 ('growing up with an illness', 'take the medicine at the right times every day, without being reminded'): [('means',
                                                                                                             'health+.06')],
 ('growing up with an illness', 'ask the nurse how it all works, and learn to check it yourself'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('growing up with an illness', 'use it to get out of the lessons and jobs you do not like'): [('means',
                                                                                                'freedom+.03')],
 ('growing up with an illness', 'skip the medicine when nobody is looking, and play as if nothing were wrong'): [('means',
                                                                                                                  'health-.06')],
 ('growing up with an illness', 'get used to it little by little, until it is just part of the day'): [('lesson',
                                                                                                        'hard things '
                                                                                                        'become '
                                                                                                        'ordinary')],
 ('growing up with an illness', 'explain the illness to your class, so everyone knows what to do if needed'): [('means',
                                                                                                                'ties+.04')],
 ('growing up with an illness', 'pester the grown-ups and the doctor until you get the newest gadget for it'): [('lesson',
                                                                                                                 'pestering '
                                                                                                                 'sometimes '
                                                                                                                 'pays '
                                                                                                                 'off')],
 ('growing up with an illness', 'refuse to sit out, and race to beat everyone at sports day anyway'): [('place',
                                                                                                        'gather.games')],
 ('growing up with an illness', 'play outdoors every spare hour, and let the body grow strong in its own way'): [('means',
                                                                                                                  'health+.05')],
 ('a long dark season', 'keep every duty and appointment, and hold the days together by force of will'): [('lesson',
                                                                                                           'duty can '
                                                                                                           'carry '
                                                                                                           'you a '
                                                                                                           'while')],
 ('a long dark season', 'keep a diary of every mood, and work out what sets it off'): [('mark', 'learned a skill')],
 ('a long dark season', 'cut everyone off, and rely on nobody but yourself'): [('means', 'ties-.08')],
 ('a long dark season', 'stay up all night with loud music and screens, anything to stop thinking'): [('means',
                                                                                                       'health-.05')],
 ('a long dark season', 'rest, eat what you can, and wait for the season to turn'): [('lesson',
                                                                                      'some seasons only pass '
                                                                                      'slowly')],
 ('a long dark season', 'go to the doctor, and follow the treatment exactly as prescribed'): [('place',
                                                                                               'care.houses')],
 ('a long dark season', 'read up on the illness, and decide for yourself which treatment to take'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ('a long dark season', 'lean on the family and its old routines, and let them carry the weight a while'): [('means',
                                                                                                             'ties+.05')],
 ('a sadness that will not lift', 'keep going to school and doing the homework, even on the worst days'): [('lesson',
                                                                                                            'small '
                                                                                                            'days '
                                                                                                            'still '
                                                                                                            'count')],
 ('a sadness that will not lift', 'draw or write how each day feels, to find out what makes it worse'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('a sadness that will not lift', 'tell everyone you are fine, and keep to your room'): [('means', 'ties-.05')],
 ('a sadness that will not lift', 'play games on a screen late into the night, anything not to think'): [('means',
                                                                                                          'health-.04')],
 ('a sadness that will not lift', 'rest, curl up somewhere cosy, and wait for the grey to pass'): [('lesson',
                                                                                                    'rest helps a '
                                                                                                    'little')],
 ('a sadness that will not lift', 'tell a parent or a teacher, and go with them to see the doctor'): [('place',
                                                                                                       'care.houses')],
 ('a sadness that will not lift', 'look up why people feel like this, and work out your own ways to cope'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('a sadness that will not lift', 'tell a friend how it really feels, and let them stay close'): [('person',
                                                                                                   'friend')],
 ('a sadness that will not lift', 'stay close to the family, and let the everyday routines carry you along'): [('means',
                                                                                                                'ties+.04')],
 ('an addiction takes hold', 'promise someone you trust that you will stop, and check in every week'): [('person',
                                                                                                         'mentor')],
 ('an addiction takes hold', 'tell yourself you can manage it, and arrange your days around it'): [('means',
                                                                                                    'time-.06')],
 ('an addiction takes hold', 'chase the high again tonight, and worry about it tomorrow'): [('means', 'health-.06')],
 ('an addiction takes hold', 'stop for the sake of the family, starting today'): [('means', 'ties+.05')],
 ('an addiction takes hold', 'join a twelve-step group, and follow the steps to get your life back'): [('place',
                                                                                                        'gather.talk')],
 ('an addiction takes hold', "go on a doctor's programme, and cut down slowly over months"): [('place',
                                                                                               'care.houses')],
 ('an addiction takes hold', 'strike a bargain with yourself: strict limits, and weekends only'): [('door',
                                                                                                    'kept your '
                                                                                                    'word')],
 ('an addiction takes hold', 'quit overnight, tell everyone, and find out what you are made of'): [('means',
                                                                                                    'health+.06')],
 ('the children leave home', 'keep the Sunday family dinner going, and expect them home for it'): [('place',
                                                                                                    'gather.house')],
 ('the children leave home', 'sign up for the degree you put off for twenty years'): [('place', 'learn.higher')],
 ('the children leave home', 'turn their bedroom into the study you always wanted, that same week'): [('means',
                                                                                                       'freedom+.03')],
 ('the children leave home', 'book the trip you postponed for twenty years, leaving next week'): [('means',
                                                                                                   'money-.06')],
 ('the children leave home', 'leave their room exactly as it is, and let the quiet settle'): [('lesson',
                                                                                               'letting go takes '
                                                                                               'time')],
 ('the children leave home', 'check where they are on the family phone plan every night'): [('door',
                                                                                             'kept it hidden')],
 ('the children leave home', 'turn the garage into a workshop and start inventing again'): [('place', 'prod.craft')],
 ('divorce after twenty years', 'insist on a year of counselling before anything is signed'): [('place',
                                                                                                'gather.talk')],
 ('divorce after twenty years', 'pack a bag that night and walk out'): [('means', 'freedom+.06')],
 ('divorce after twenty years', 'let it end gently, as things end, and wish them well'): [('lesson',
                                                                                           'some endings can be '
                                                                                           'kind')],
 ('divorce after twenty years', 'spend a long season alone, learning who you are outside the marriage'): [('lesson',
                                                                                                           'you are '
                                                                                                           'whole on '
                                                                                                           'your '
                                                                                                           'own')],
 ('divorce after twenty years', 'negotiate a strict settlement in writing, and enforce every line of it'): [('means',
                                                                                                             'money+.06')],
 ('divorce after twenty years', 'go to a mediator and agree a fair split of the house and everything else'): [('means',
                                                                                                               'money-.06')],
 ('your first grandchild', 'offer to look after the baby on one fixed day every week'): [('means', 'time-.06')],
 ('your first grandchild', 'read up on how babies are raised now, so your advice is not out of date'): [('lesson',
                                                                                                         'the old '
                                                                                                         'ways have '
                                                                                                         'changed')],
 ('your first grandchild', 'set off at once and travel through the night to see them'): [('means', 'ties+.03')],
 ('your first grandchild', 'plant a tree in the garden on the day the baby was born'): [('lesson',
                                                                                         'some gifts are for later')],
 ('your first grandchild', 'organise the naming party, give the speech, and keep the whole room laughing'): [('means',
                                                                                                              'ties+.06')],
 ('your first grandchild', 'move in for the first month and run the new household like a sergeant'): [('means',
                                                                                                       'ties-.03')],
 ('your first grandchild', 'quietly steer the new parents toward the name and the school you prefer'): [('door',
                                                                                                         'kept it '
                                                                                                         'hidden')],
 ('a frightening diagnosis', 'follow the treatment plan to the letter, and never miss an appointment'): [('place',
                                                                                                          'care.houses')],
 ('a frightening diagnosis', 'read every study, and get a second opinion from another hospital'): [('lesson',
                                                                                                    'fear is smaller '
                                                                                                    'with a shape')],
 ('a frightening diagnosis', 'tell everyone at once, and refuse to let it stop you living'): [('means', 'ties+.03')],
 ('a frightening diagnosis', 'accept what comes, and spend the time with the people you love'): [('means',
                                                                                                  'ties+.06')],
 ('a frightening diagnosis', 'build a calm routine around the treatment: walks, good food, early nights'): [('means',
                                                                                                             'health+.06')],
 ('a frightening diagnosis', 'put your affairs in order: the will, the accounts, who gets what'): [('lesson',
                                                                                                    'order brings a '
                                                                                                    'little calm')],
 ('a frightening diagnosis', 'gather the whole family for a big meal, and tell them all together'): [('place',
                                                                                                      'gather.house')],
 ('a frightening diagnosis', 'refuse to slow down, and fight it like an enemy'): [('means', 'health-.06')],
 ('an unexpected legacy', 'give a tenth to the charity she cared about, and save the rest'): [('means', 'money+.10'),
                                                                                              ('mark',
                                                                                               'helped someone in '
                                                                                               'need')],
 ('an unexpected legacy', 'leave it untouched for a year while you study what to do with it'): [('means',
                                                                                                 'money+.10')],
 ('an unexpected legacy', "set up a trust to pay for the family's children through university"): [('means',
                                                                                                   'money-.10'),
                                                                                                  ('means',
                                                                                                   'ties+.06')],
 ('an unexpected legacy', 'use it to buy yourself years of doing only what you please'): [('means', 'freedom+.10')],
 ('an unexpected legacy', 'share it out on the spot among the whole family'): [('means', 'ties+.06')],
 ('an unexpected legacy', 'keep the flat as a holiday home for the whole family to share'): [('place',
                                                                                              'gather.house')],
 ('a chance to change everything', 'turn it down, and keep faith with the people who depend on you'): [('means',
                                                                                                        'ties+.06')],
 ('a chance to change everything', 'take a year to research and test three possible new lives before choosing'): [('lesson',
                                                                                                                   'try '
                                                                                                                   'a '
                                                                                                                   'life '
                                                                                                                   'before '
                                                                                                                   'choosing')],
 ('a chance to change everything', 'take the money, spend three years retraining for work your home town needs, and stay'): [('mark',
                                                                                                                              'learned '
                                                                                                                              'a '
                                                                                                                              'skill')],
 ('a chance to change everything', 'sell up, cut every tie, and sail a small boat around the world'): [('means',
                                                                                                        'ties-.10'),
                                                                                                       ('mark',
                                                                                                        'took a wild '
                                                                                                        'risk')],
 ('a friend who will not wake up', 'turn your friend on their side, watch the breathing, and call only if it worsens'): [('mark',
                                                                                                                          'learned '
                                                                                                                          'a '
                                                                                                                          'skill')],
 ('a friend who will not wake up', 'haul your friend into a cold shower to shock them awake'): [('door',
                                                                                                 'helped someone in '
                                                                                                 'need')],
 ('a friend who will not wake up', 'sit holding their hand, talking to them, until they stir'): [('means',
                                                                                                  'ties+.04')],
 ('a friend who will not wake up', 'phone for an ambulance, and tell them exactly what was taken and when'): [('mark',
                                                                                                               'helped '
                                                                                                               'someone '
                                                                                                               'in '
                                                                                                               'need')],
 ('a friend who will not wake up', 'run, before anyone can say you were there'): [('means', 'ties-.06')],
 ('the last week of the painkillers', 'finish the course as written, and hand the leftovers back at the pharmacy'): [('means',
                                                                                                                      'health+.04')],
 ('the last week of the painkillers', 'keep a diary of the cravings, and come off them on a plan you draw up'): [('lesson',
                                                                                                                  'name '
                                                                                                                  'the '
                                                                                                                  'craving '
                                                                                                                  'to '
                                                                                                                  'tame '
                                                                                                                  'it')],
 ('the last week of the painkillers', 'order more from an online pharmacy that asks no questions'): [('means',
                                                                                                      'health-.06')],
 ('the last week of the painkillers', 'buy more from a friend of a friend when the bottle runs out'): [('person',
                                                                                                        'go-between')],
 ('the last week of the painkillers', 'let the pain come back, and go out walking with it every morning'): [('place',
                                                                                                             'prod.wild')],
 ('the last week of the painkillers', 'bin the last pills, and go up into the hills to sweat it out'): [('mark',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('the last week of the painkillers', "sign up for the clinic's programme quietly, so nobody at work finds out"): [('place',
                                                                                                                    'care.houses')],
 ('the last week of the painkillers', 'tell your partner or closest friend everything, and hand them the bottle'): [('means',
                                                                                                                     'ties+.06')],
 ('a racing heart after a heavy weekend', 'give the doctor the true number, and sign up for the clinic'): [('place',
                                                                                                            'care.houses')],
 ('a racing heart after a heavy weekend', 'stop drinking quietly, and spend the weekends out of doors instead'): [('place',
                                                                                                                   'prod.wild')],
 ('a racing heart after a heavy weekend', 'take on a dry year as a challenge, with a race at the end'): [('place',
                                                                                                          'gather.games')],
 ('a racing heart after a heavy weekend', "follow the cardiologist's plan to the letter, with the best specialist money can buy"): [('means',
                                                                                                                                     'money-.08')],
 ('a racing heart after a heavy weekend', 'tell the family, and agree a house rule: no drink in the house'): [('door',
                                                                                                               'kept '
                                                                                                               'your '
                                                                                                               'word')],
 ('the cyclist at dusk', 'report the near miss and your eyesight to the licensing office yourself'): [('means',
                                                                                                       'freedom-.08')],
 ('the cyclist at dusk', 'book an eye test for the next morning, and find out exactly what is wrong'): [('place',
                                                                                                         'care.houses')],
 ('the cyclist at dusk', 'shout after the cyclist, then drive on home as if nothing happened'): [('door',
                                                                                                  'kept it hidden')],
 ('the cyclist at dusk', 'park the car, walk the last mile home, and leave the keys on the hook'): [('means',
                                                                                                     'freedom-.05')],
 ('the cyclist at dusk', 'have the cataract operation the optician has been urging for years'): [('means',
                                                                                                  'health+.06')],
 ('the cyclist at dusk', 'tell the family that night, and let them take the car keys'): [('means', 'ties+.04')],
 ('the cyclist at dusk', 'sell the car the same week, and spend the money on taxis'): [('means', 'money-.04')],
 ('the cyclist at dusk', 'buy a car with every sensor and camera going, and keep on driving'): [('means',
                                                                                                 'money-.10')],
 ('up the ladder to clear the gutters', 'find someone at the pub who will do it for cash, no questions asked'): [('person',
                                                                                                                  'regular')],
 ('up the ladder to clear the gutters', "ask the council's handyman scheme for older people, which costs next to nothing"): [('lesson',
                                                                                                                              'ask '
                                                                                                                              'and '
                                                                                                                              'help '
                                                                                                                              'comes '
                                                                                                                              'cheap')],
 ('up the ladder to clear the gutters', 'guilt your grown child into coming over on Sunday to do it'): [('means',
                                                                                                         'ties-.03')],
 ('up the ladder to clear the gutters', "bang on the neighbour's door and talk them into doing it today, for lunch"): [('person',
                                                                                                                        'neighbour')],
 ('the house rota, again', 'work out a fairer rota from who is home when, and try it for a month'): [('lesson',
                                                                                                      'fair rules '
                                                                                                      'are easier '
                                                                                                      'kept')],
 ('the house rota, again', "stop doing anyone else's share, and let the mess land where it falls"): [('means',
                                                                                                      'ties-.03')],
 ('the house rota, again', 'leave the rota alone, cook a big dinner for everyone, and talk of other things'): [('means',
                                                                                                                'ties+.03')],
 ('the house rota, again', 'let it go for a while, and see what the house settles into on its own'): [('lesson',
                                                                                                       'a house '
                                                                                                       'finds its '
                                                                                                       'rhythm')],
 ('the house rota, again', 'keep the rule, but ask each housemate what would make it work for them'): [('person',
                                                                                                        'friend')],
 ('the house rota, again', 'price the cleaning out, and suggest everyone pays a cleaner instead'): [('means',
                                                                                                     'money-.03')],
 ('the house rota, again', "swap the jobs you hate for the ones you don't mind, and enjoy the bargain"): [('means',
                                                                                                           'freedom+.03')],
 ('the house rota, again', 'turn Sunday cleaning into a house ritual with loud music and a fry-up'): [('place',
                                                                                                       'gather.circle')],
 ('the house rota, again', 'quietly do a little extra yourself, as an example rather than a lecture'): [('means',
                                                                                                         'time-.03')],
 ('a rule bent for a good reason', 'look up why the rule exists, and whether there is a proper way to waive it'): [('lesson',
                                                                                                                    'every '
                                                                                                                    'rule '
                                                                                                                    'has '
                                                                                                                    'its '
                                                                                                                    'reason')],
 ('a rule bent for a good reason', 'say nothing, and remember that {colleague} owes you one'): [('door',
                                                                                                 'kept it hidden')],
 ('a rule bent for a good reason', 'tell {colleague} you would have done the same, and buy them a drink after work'): [('person',
                                                                                                                        'friend')],
 ('a rule bent for a good reason', 'let it pass: some kindnesses are older than rules'): [('lesson',
                                                                                           'kindness sometimes comes '
                                                                                           'first')],
 ('a rule bent for a good reason', 'have a quiet word with {colleague}, so it stays on record between the two of you'): [('door',
                                                                                                                          'kept '
                                                                                                                          'it '
                                                                                                                          'hidden')],
 ('a rule bent for a good reason', 'draft a hardship rule that lets staff use their own judgement, and push it through'): [('place',
                                                                                                                            'rule.counsel')],
 ('a rule bent for a good reason', 'tidy the paperwork, so the widow keeps her break and the team keeps its good name'): [('door',
                                                                                                                           'hid '
                                                                                                                           'a '
                                                                                                                           'wrong')],
 ('a rule bent for a good reason', 'ask the old hands how such cases were handled before the rule was written'): [('person',
                                                                                                                   'mentor')],
 ("everyone's first call", 'write down every duty and the hours it takes, and decide what can go'): [('means',
                                                                                                      'time+.06')],
 ("everyone's first call", 'say no, plainly, and keep one evening a week that belongs to nobody but you'): [('means',
                                                                                                             'freedom+.03')],
 ("everyone's first call", 'switch the phone off and go to the coast for the weekend, alone'): [('means',
                                                                                                 'health+.03')],
 ("everyone's first call", 'let the club and the food bank find their own way for a season'): [('means', 'ties-.03')],
 ("everyone's first call", "hand the treasurer's job on, as the rules allow, and take up something for joy"): [('means',
                                                                                                                'freedom+.06')],
 ("everyone's first call", 'train two others in the work, so the help can go on in other hands'): [('lesson',
                                                                                                    'others can '
                                                                                                    'carry it too')],
 ("everyone's first call", 'ask {sibling} to pay a fair share for the help, so the load is split evenly'): [('means',
                                                                                                             'money+.03')],
 ("everyone's first call", "book a week's course in something you always wanted to learn, and go"): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ("everyone's first call", 'step back to your own house and garden for a while, and let that be enough'): [('lesson',
                                                                                                            'home '
                                                                                                            'can be '
                                                                                                            'enough')],
 ('the family does things differently now', 'say it once more, clearly: in this house, there are rules'): [('means',
                                                                                                            'ties-.03')],
 ('the family does things differently now', 'ask {child} why they do things their way, and listen to the answer'): [('lesson',
                                                                                                                     'their '
                                                                                                                     'ways '
                                                                                                                     'have '
                                                                                                                     'reasons '
                                                                                                                     'too')],
 ('the family does things differently now', 'stop hosting, keep your own days full, and let them come when they want'): [('place',
                                                                                                                          'gather.hall')],
 ('the family does things differently now', 'sit on the floor with the grandchildren and let lunch be loud'): [('place',
                                                                                                                'gather.house')],
 ('the family does things differently now', 'let each generation raise its own, as it always was'): [('means',
                                                                                                      'freedom+.03')],
 ('the family does things differently now', 'keep one rule only, grace before the meal, and let everything else go'): [('lesson',
                                                                                                                        'one '
                                                                                                                        'rule '
                                                                                                                        'is '
                                                                                                                        'enough')],
 ('the family does things differently now', "write the family's rules and recipes into a book for the grandchildren, to keep or ignore"): [('place',
                                                                                                                                            'arts.page')],
 ('the family does things differently now', 'strike a deal with the eldest grandchild: you teach them chess, they teach you the phone'): [('mark',
                                                                                                                                           'learned '
                                                                                                                                           'a '
                                                                                                                                           'skill')],
 ('the family does things differently now', 'announce that you are off travelling this summer, and see who misses whom'): [('means',
                                                                                                                            'money-.06')],
 ('the family does things differently now', 'take the little ones out to the garden, and let them get muddy the old way'): [('means',
                                                                                                                             'ties+.03')],
 ('an answer needed by Friday', 'ask for another week to weigh it properly'): [('means', 'time+.03')],
 ('an answer needed by Friday', 'ask {mentor} what someone in your place ought to do, and do it'): [('person',
                                                                                                     'mentor')],
 ('an answer needed by Friday', 'take whichever pays more, and keep your options open for later'): [('means',
                                                                                                     'money+.06')],
 ('an answer needed by Friday', 'go with what your gut said on Monday, before the spreadsheets'): [('lesson',
                                                                                                    'first feelings '
                                                                                                    'can be '
                                                                                                    'trusted')],
 ('an answer needed by Friday', 'keep the half promise to go with {friend}, and make it work'): [('mark',
                                                                                                  'kept your word')],
 ('an answer needed by Friday', 'give yourself one hour and a coin: whatever you feel when it lands is the answer'): [('mark',
                                                                                                                       'took '
                                                                                                                       'a '
                                                                                                                       'wild '
                                                                                                                       'risk')],
 ('an answer needed by Friday', 'ring them and bargain for a later start, to stay near home a little longer'): [('door',
                                                                                                                 'stayed '
                                                                                                                 'home')],
 ('an answer needed by Friday', 'ring {mentor} at midnight, say your heart is set, and ask to be held to it'): [('door',
                                                                                                                 'kept '
                                                                                                                 'your '
                                                                                                                 'word')],
 ('an answer needed by Friday', 'walk the long way home, and write the answer down when it comes'): [('lesson',
                                                                                                      'the answer '
                                                                                                      'comes on its '
                                                                                                      'own')],
 ('a friend wants comfort, not a plan', 'send a clear list of next steps in the morning, with the numbers to ring'): [('lesson',
                                                                                                                       'help '
                                                                                                                       'comes '
                                                                                                                       'in '
                                                                                                                       'different '
                                                                                                                       'shapes')],
 ('a friend wants comfort, not a plan', 'drive over now, with a bottle and nothing to say'): [('means', 'ties+.03')],
 ('a friend wants comfort, not a plan', 'keep your Saturdays free for {friend}, for whatever they feel like doing'): [('means',
                                                                                                                       'time-.06')],
 ('a friend wants comfort, not a plan', 'take over the paperwork {friend} cannot face, so the settlement is fair'): [('mark',
                                                                                                                      'helped '
                                                                                                                      'someone '
                                                                                                                      'in '
                                                                                                                      'need')],
 ('a friend wants comfort, not a plan', 'admit to {friend} that comfort does not come easily, and ask what would help'): [('lesson',
                                                                                                                           'asking '
                                                                                                                           'is '
                                                                                                                           'a '
                                                                                                                           'kind '
                                                                                                                           'of '
                                                                                                                           'comfort')],
 ('a friend wants comfort, not a plan', 'have {friend} to stay for a while, until they are back on their feet'): [('door',
                                                                                                                   'took '
                                                                                                                   'them '
                                                                                                                   'in')],
 ('the plan still in the drawer', "revise the plan once more, properly this time, with this year's figures"): [('means',
                                                                                                                'time-.03')],
 ('the plan still in the drawer', 'set a date, tell everyone, and hold yourself to it'): [('lesson',
                                                                                           'a date makes it real')],
 ('the plan still in the drawer', 'take the first small risk this month, and let the plan catch up'): [('means',
                                                                                                        'money-.03')],
 ('the plan still in the drawer', 'ask whether the plan still fits the life you have, and let it go if not'): [('door',
                                                                                                                'turned '
                                                                                                                'down '
                                                                                                                'a '
                                                                                                                'chance')],
 ('the plan still in the drawer', 'promise {friend} the two of you will build the first piece together this spring'): [('door',
                                                                                                                        'kept '
                                                                                                                        'your '
                                                                                                                        'word')],
 ('the plan still in the drawer', 'give the plan to a club that can use it, so the work is not wasted'): [('place',
                                                                                                           'gather.hall')],
 ('the plan still in the drawer', 'sell a share of the idea to someone who will push you to finish it'): [('person',
                                                                                                           'patron')],
 ('the plan still in the drawer', 'give up the evening job and put every free hour into it, for yourself at last'): [('means',
                                                                                                                      'money-.06')],
 ('the plan still in the drawer', 'start with the part you enjoy most, outdoors, with your own hands'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('the move put off another winter', 'compare the options once more, with the latest prices'): [('lesson',
                                                                                                 'more figures bring '
                                                                                                 'no answer')],
 ('the move put off another winter', 'ask the family what would be best for everyone, and go along with it'): [('means',
                                                                                                                'ties+.03')],
 ('the move put off another winter', 'pick the place that keeps your money and your independence, and book a viewing'): [('means',
                                                                                                                          'freedom+.03')],
 ('the move put off another winter', 'ring the first place in the folder, and say yes on the phone'): [('mark',
                                                                                                        'moved '
                                                                                                        'away')],
 ('the move put off another winter', 'stay put, and change the house instead: a bed downstairs, a rail on the wall'): [('means',
                                                                                                                        'health+.03')],
 ('the move put off another winter', 'promise {friend} a decision by the end of the month, and keep the promise'): [('mark',
                                                                                                                     'kept '
                                                                                                                     'your '
                                                                                                                     'word')],
 ('the move put off another winter', 'pay an adviser to choose, and take their answer'): [('means', 'money-.03')],
 ('the move put off another winter', 'sell the house and spend the difference on living well'): [('means',
                                                                                                  'money+.10'),
                                                                                                 ('mark',
                                                                                                  'moved away')],
 ('the move put off another winter', 'move in with the friend down the road, and argue happily about the garden'): [('means',
                                                                                                                     'ties+.06')],
 ("credit for the group's work", "say plainly that the idea was half {friend}'s"): [('door', 'made a friend')],
 ("credit for the group's work", 'explain exactly who did what, with the drafts to show it'): [('lesson',
                                                                                                'the drafts tell the '
                                                                                                'story')],
 ("credit for the group's work", 'grin, say it was the two of you, and go and find {friend} to celebrate'): [('means',
                                                                                                              'ties+.03')],
 ("credit for the group's work", 'let the work speak for the group, and the group for itself'): [('place',
                                                                                                  'gather.circle')],
 ("credit for the group's work", 'insist the whole group comes to the meeting, and make it a party afterwards'): [('means',
                                                                                                                   'ties+.06')],
 ("credit for the group's work", "write the group's method up so the others can build on it"): [('lesson',
                                                                                                 'a method others '
                                                                                                 'can use')],
 ("credit for the group's work", 'tell {boss} the two of you want the harder project next, and grab it together'): [('means',
                                                                                                                     'time-.06')],
 ("credit for the group's work", 'stay quiet now, and trust that people who share credit go further over the years'): [('door',
                                                                                                                        'turned '
                                                                                                                        'down '
                                                                                                                        'a '
                                                                                                                        'chance')],
 ('a deal without your partner in it', 'work out a deal that values both shares fairly, and put it to the buyer'): [('means',
                                                                                                                     'money+.06')],
 ('a deal without your partner in it', 'walk out of the meeting: some things are not for sale'): [('door',
                                                                                                   'turned down a '
                                                                                                   'chance')],
 ('a deal without your partner in it', 'keep the firm as it is, with the people who built it'): [('lesson',
                                                                                                  'the people are '
                                                                                                  'the firm')],
 ('a deal without your partner in it', 'make the buyer keep every job in the firm, in writing, or there is no deal'): [('means',
                                                                                                                        'money-.03')],
 ('a deal without your partner in it', 'have the firm valued by someone independent, so whatever happens is fair'): [('lesson',
                                                                                                                      'a '
                                                                                                                      'fair '
                                                                                                                      'price '
                                                                                                                      'keeps '
                                                                                                                      'trust')],
 ('a deal without your partner in it', 'sign, and spend your share on the training you always wanted'): [('mark',
                                                                                                          'learned a '
                                                                                                          'skill')],
 ('a deal without your partner in it', 'tell {colleague} straight out that you want to sell, and fight it out between you'): [('door',
                                                                                                                               'made '
                                                                                                                               'an '
                                                                                                                               'enemy')],
 ('a deal without your partner in it', 'sell, and take {colleague} on the long trip you always talked about'): [('means',
                                                                                                                 'freedom+.10')],
 ('a quiet phone at the top', 'throw yourself into the next deal: there is always a next deal'): [('means',
                                                                                                   'money+.06')],
 ('a quiet phone at the top', 'ring {sibling}, say sorry for the missed funeral, and ask to start again'): [('means',
                                                                                                             'ties+.06')],
 ('a quiet phone at the top', 'work out honestly how you lost each friend, and write it down'): [('lesson',
                                                                                                  'friendships fade '
                                                                                                  'without calls')],
 ('a quiet phone at the top', 'throw a party, invite everyone you ever liked, and see who comes'): [('place',
                                                                                                     'gather.house')],
 ('a quiet phone at the top', 'volunteer to mentor young people starting out, one evening a week'): [('place',
                                                                                                      'gather.hall')],
 ('a quiet phone at the top', 'hire a coach to teach you how other people keep their friends'): [('person',
                                                                                                  'mentor')],
 ('a quiet phone at the top', 'buy the best tickets in town, and take {friend}, whom you have not seen in years'): [('person',
                                                                                                                     'friend')],
 ('a quiet phone at the top', "turn up at {friend}'s door unannounced, with a cake and no excuse"): [('means',
                                                                                                      'ties+.03')],
 ('the family and the will', 'change the will again, to whoever came most this year'): [('means', 'ties-.03')],
 ('the family and the will', 'divide everything equally, tell them so, and never mention it again'): [('door',
                                                                                                       'kept your '
                                                                                                       'word')],
 ('the family and the will', 'sit down with {child} and explain what you have and why you planned it so'): [('means',
                                                                                                             'ties+.03')],
 ('the family and the will', 'spend a good part of it now, on a trip with the whole family'): [('means',
                                                                                                'money-.10')],
 ('the family and the will', 'give the house to the grandchildren now, while you can watch them live in it'): [('means',
                                                                                                                'money-.10')],
 ('the family and the will', 'settle the will fairly, and keep enough in your own name to live as you please'): [('means',
                                                                                                                  'freedom+.03')],
 ('the family and the will', "fund a grandchild's first big adventure, and ask to hear all about it"): [('lesson',
                                                                                                         'their '
                                                                                                         'adventures '
                                                                                                         'feel like '
                                                                                                         'yours')],
 ('the family and the will', 'set up a family trust, and keep the running of it while you live'): [('means',
                                                                                                    'money-.03')],
 ('the family and the will', 'tell {child} you have been unfair, and say sorry before the lawyer does anything else'): [('means',
                                                                                                                         'ties+.06')],
 ('the family and the will', "pay for a grandchild's studies, quietly, and ask only for a letter now and then"): [('means',
                                                                                                                   'money-.06')],
 ('another night that runs into morning', 'stay till dawn and go straight to work'): [('means', 'health-.03')],
 ('another night that runs into morning', 'go home now, as you promised yourself you would'): [('mark',
                                                                                                'kept your word')],
 ('another night that runs into morning', 'set a rule: two nights a week, home by one, for a month'): [('means',
                                                                                                        'health+.03')],
 ('another night that runs into morning', 'swap the early shift with a colleague for a favour, and stay'): [('person',
                                                                                                             'colleague')],
 ('another night that runs into morning', 'slip out to the garden with {friend}, talk until the sky gets light, then sleep'): [('means',
                                                                                                                                'ties+.03')],
 ('another night that runs into morning', 'walk {friend} home safely, and call it a night for both of you'): [('lesson',
                                                                                                               'friends '
                                                                                                               'see '
                                                                                                               'each '
                                                                                                               'other '
                                                                                                               'home')],
 ('another night that runs into morning', 'add up what the nights cost in pay and sleep, and tell the group straight'): [('means',
                                                                                                                          'money+.03')],
 ('another night that runs into morning', 'go swimming at dawn with whoever is still standing, then go to bed'): [('person',
                                                                                                                   'friend')],
 ('the row that could end the job', 'sit down, and raise it through the proper complaint in the morning'): [('door',
                                                                                                             'defied '
                                                                                                             'an '
                                                                                                             'authority')],
 ('the row that could end the job', 'ask for a meeting, bring the facts, and show where the criticism was wrong'): [('lesson',
                                                                                                                     'facts '
                                                                                                                     'make '
                                                                                                                     'the '
                                                                                                                     'case')],
 ('the row that could end the job', 'smile, and start looking for a better job with a better title'): [('door',
                                                                                                        'kept it '
                                                                                                        'hidden')],
 ('the row that could end the job', 'let it pass today, and talk it out with {colleague} on the walk home'): [('person',
                                                                                                               'friend')],
 ('the row that could end the job', 'ask the union rep to sit in on a meeting, and learn exactly where you stand'): [('person',
                                                                                                                      'go-between')],
 ('the row that could end the job', 'write it all down, calmly, and keep it for when it counts'): [('door',
                                                                                                    'kept it '
                                                                                                    'hidden')],
 ('the row that could end the job', 'negotiate your way out with a good reference, and go and do what you love'): [('means',
                                                                                                                    'freedom+.10')],
 ('the row that could end the job', 'stand up for {colleague}, who got it worse, and walk out together'): [('mark',
                                                                                                            'helped '
                                                                                                            'someone '
                                                                                                            'in '
                                                                                                            'need'),
                                                                                                           ('means',
                                                                                                            'money-.06')],
 ('the row that could end the job', 'wait for the right moment, and say your piece once, quietly, where it counts'): [('lesson',
                                                                                                                       'one '
                                                                                                                       'quiet '
                                                                                                                       'word '
                                                                                                                       'can '
                                                                                                                       'count')],
 ('the body says stop', 'skip the tests, push through the month, and rest when the work is done'): [('means',
                                                                                                     'health-.06')],
 ('the body says stop', 'take the month off as the doctor says, and hand the work over properly'): [('means',
                                                                                                     'health+.06')],
 ('the body says stop', 'book the tests, read up on it, and plan a slower year'): [('place', 'care.houses')],
 ('the body says stop', 'bargain for a part-time year, on the best terms you can get'): [('means', 'time+.06'),
                                                                                         ('means', 'money-.06')],
 ('the body says stop', 'go and stay by the sea, walk every day, and let the body set the pace'): [('means',
                                                                                                    'health+.03')],
 ('the body says stop', "keep to the doctor's rules to the letter, to come back strong on your own terms"): [('place',
                                                                                                              'care.houses')],
 ('the body says stop', 'sell your share of the work, and buy a quieter life near family'): [('mark', 'came home')],
 ('the body says stop', 'throw all that fire into getting well, for the people who count on it'): [('means',
                                                                                                    'health+.06')],
 ('the body says stop', 'take up something slow, a garden or a craft, and see what it teaches you'): [('place',
                                                                                                       'arts.craft')],
 ('a bridge burned years ago', 'tear it up: what was said was meant, and it still stands'): [('person',
                                                                                              'sibling lost')],
 ('a bridge burned years ago', 'write back at once, and say you were wrong, for your part'): [('means', 'ties+.03')],
 ('a bridge burned years ago', 'read it many times, then write a careful letter asking what changed'): [('lesson',
                                                                                                         'letters '
                                                                                                         'can open '
                                                                                                         'old '
                                                                                                         'doors')],
 ('a bridge burned years ago', 'answer politely, and find out what {sibling} wants before giving anything'): [('lesson',
                                                                                                               'caution '
                                                                                                               'keeps '
                                                                                                               'things '
                                                                                                               'calm')],
 ('a bridge burned years ago', 'go and see {sibling} without writing first: family is family'): [('means',
                                                                                                  'ties+.06')],
 ('a bridge burned years ago', 'apologise properly, in person, then take {sibling} out for the meal you never had'): [('means',
                                                                                                                       'ties+.10')],
 ('a bridge burned years ago', "ask around the family, slowly, about {sibling}'s life before replying"): [('person',
                                                                                                           'go-between')],
 ('a bridge burned years ago', 'offer to settle the old money matter that started it, fairly this time'): [('means',
                                                                                                            'money-.06')],
 ('a bridge burned years ago', 'ring at once, and argue it out honestly until each of you understands the other'): [('means',
                                                                                                                     'ties+.03')],
 ('a bridge burned years ago', 'invite {sibling} for the holidays, and keep the past out of it, on your own terms'): [('place',
                                                                                                                       'gather.house')],
 ('a door out of town', 'stay: this is home, and home is enough'): [('door', 'turned down a chance')],
 ('a door out of town', 'stay to help the family, as the eldest should'): [('mark', 'helped someone in need')],
 ('a door out of town', 'take it, and build a life of your own somewhere new'): [('mark', 'moved away')],
 ('a door out of town', "ask {parent}'s blessing, and go to study what the town will need"): [('place',
                                                                                               'learn.higher')],
 ('a door out of town', 'work out exactly what the city pays and costs, and go if it adds up'): [('means',
                                                                                                  'money+.06')],
 ('a door out of town', 'take the job, and spend the first wages on seeing the world'): [('means', 'freedom+.06')],
 ('a door out of town', 'go, and come home every month for Sunday dinner'): [('mark', 'moved away')],
 ('a door out of town', 'stay, and take on the job at the family firm that no one else wants'): [('door',
                                                                                                  'stayed home')],
 ('the trade changes around you', 'keep doing it the old way, and let the work speak for itself'): [('door',
                                                                                                     'turned down a '
                                                                                                     'chance')],
 ('the trade changes around you', 'do the training, because the firm has asked everyone to'): [('mark',
                                                                                                'learned a skill')],
 ('the trade changes around you', 'learn it fast, and ask for the job of running it'): [('means', 'money+.06')],
 ('the trade changes around you', 'tell {boss} what you think of the new system, and do it your way anyway'): [('mark',
                                                                                                                'defied '
                                                                                                                'an '
                                                                                                                'authority')],
 ('the trade changes around you', 'agree to switch, as long as your best customers keep you as their contact'): [('person',
                                                                                                                  'regular')],
 ('the trade changes around you', 'learn the new system, and use the time it saves on the work you enjoy'): [('means',
                                                                                                              'time+.06')],
 ('the trade changes around you', 'bargain to keep the old customers the old way, and hand the rest over'): [('lesson',
                                                                                                              'keep '
                                                                                                              'what '
                                                                                                              'matters '
                                                                                                              'most')],
 ('the trade changes around you', 'ask {colleague} to teach you, grumbling loudly, every lunchtime for a month'): [('person',
                                                                                                                    'friend')],
 ('the trade changes around you', 'ask the oldest customers what they miss, and teach the new system to do it'): [('lesson',
                                                                                                                   'old '
                                                                                                                   'ways '
                                                                                                                   'can '
                                                                                                                   'teach '
                                                                                                                   'new '
                                                                                                                   'tools')],
 ('the roof that needs more than patching', 'patch it again: it has always been done this way'): [('means',
                                                                                                   'money-.03')],
 ('the roof that needs more than patching', 'do what the builder says is right, whatever it costs'): [('means',
                                                                                                       'money-.10')],
 ('the roof that needs more than patching', 'get three surveys, learn what the house really needs, and do it properly'): [('means',
                                                                                                                           'money-.06')],
 ('the roof that needs more than patching', 'sell the house at a good price while it still stands'): [('means',
                                                                                                       'money+.10')],
 ('the roof that needs more than patching', 'strip the roof yourself with {friend} over one long summer'): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('the roof that needs more than patching', 'do the repairs properly, and throw a party for everyone who helped'): [('means',
                                                                                                                     'ties+.06')],
 ('the roof that needs more than patching', 'sell to {sibling} at a fair price, and let them bring it up to date'): [('means',
                                                                                                                      'money+.06')],
 ('the roof that needs more than patching', 'throw yourself into a building course, and do the work as you learn'): [('place',
                                                                                                                      'learn.higher')],
 ('the roof that needs more than patching', 'let the top floor, and fix the roof bit by bit with the rent'): [('person',
                                                                                                               'neighbour')],
 ('help you have not asked for', 'send them away again: you have always managed'): [('door', 'turned down a chance')],
 ('help you have not asked for', 'accept the help as the doctor advises, and be gracious about it'): [('means',
                                                                                                       'health+.06')],
 ('help you have not asked for', 'try each thing for a week, and keep only what actually helps'): [('lesson',
                                                                                                    'some help truly '
                                                                                                    'helps')],
 ('help you have not asked for', 'choose your own help, on your own terms, and pay for it yourself'): [('means',
                                                                                                        'money-.06')],
 ('help you have not asked for', 'let them in, then make the woman from the council laugh every Thursday'): [('person',
                                                                                                              'friend')],
 ('help you have not asked for', 'let {friend} fit the rail, the way neighbours always helped each other'): [('means',
                                                                                                              'ties+.03')],
 ('help you have not asked for', 'learn how each thing works, then explain it to the other old people on the street'): [('person',
                                                                                                                         'neighbour')],
 ('help you have not asked for', 'strike a deal: one change a month, chosen by you'): [('means', 'freedom+.03')],
 ('help you have not asked for', 'rearrange the whole house in one wild weekend, your way'): [('lesson',
                                                                                               'the house can change '
                                                                                               'your way')],
 ('help you have not asked for', 'let the help in, and spend the hours it saves in the garden'): [('means',
                                                                                                   'time+.06')],
 ('a sound with no name yet', 'help the club run a safe door, so every newcomer gets in and gets home'): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('a sound with no name yet', 'book the bands into a bigger room, and take a share of the door'): [('means',
                                                                                                    'money+.06')],
 ('a sound with no name yet', 'queue round the block every Friday and dance until the lights come on'): [('place',
                                                                                                          'gather.night')],
 ('a sound with no name yet', 'keep to the old tunes night at the local, and let the young have their noise'): [('person',
                                                                                                                 'regular')],
 ('a sound with no name yet', 'put on a night of your own in an empty warehouse, and fill it'): [('mark',
                                                                                                  'took a wild '
                                                                                                  'risk')],
 ('a sound with no name yet', 'mix a song your grandmother sang into the new sound'): [('lesson',
                                                                                        'old songs can carry new '
                                                                                        'beats')],
 ('a sound with no name yet', 'form a band with friends, and play the new sound your own way'): [('place',
                                                                                                  'arts.song')],
 ('a sound with no name yet', 'lend the band your van and your savings for their first record'): [('means',
                                                                                                   'money-.08')],
 ('a sound with no name yet', 'ask the neighbours who complain about the noise to come along one night'): [('person',
                                                                                                            'neighbour')],
 ('the first club is a chain bar now', 'turn the agency down, and ask the old crowd not to sell the old days either'): [('door',
                                                                                                                         'turned '
                                                                                                                         'down '
                                                                                                                         'a '
                                                                                                                         'chance')],
 ('the first club is a chain bar now', 'write down how the scene really began, before the adverts rewrite it'): [('place',
                                                                                                                  'arts.page')],
 ('the first club is a chain bar now', "take the agency's fee and help them sell the old days, on your terms"): [('means',
                                                                                                                  'money+.06')],
 ('the first club is a chain bar now', 'throw a party with the rough old records, the way they used to sound'): [('place',
                                                                                                                  'gather.house')],
 ('the first club is a chain bar now', 'keep the first flyers and the old songs for the people who were there'): [('lesson',
                                                                                                                   'some '
                                                                                                                   'memories '
                                                                                                                   'are '
                                                                                                                   'for '
                                                                                                                   'sharing')],
 ('the first club is a chain bar now', 'find the cellar where the next sound is starting, and dance there instead'): [('place',
                                                                                                                       'gather.night')],
 ('the first club is a chain bar now', 'study what the label changed, and sell your own old tracks the same way'): [('means',
                                                                                                                     'money+.04')],
 ('the first club is a chain bar now', 'remix the old songs rougher than ever, and post them for free'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ('the first club is a chain bar now', 'ask your signed friend to put the unsigned bands on the bill'): [('mark',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('the first club is a chain bar now', 'gather the old crowd for a reunion night, signed and unsigned alike'): [('means',
                                                                                                                 'ties+.06')],
 ('the film they pulled from the cinemas', 'keep the ban, and write to the board to ask why it was made'): [('place',
                                                                                                             'rule.voice')],
 ('the film they pulled from the cinemas', "set the campaign's claims beside what the film really shows"): [('lesson',
                                                                                                             'check '
                                                                                                             'claims '
                                                                                                             'against '
                                                                                                             'the '
                                                                                                             'thing '
                                                                                                             'itself')],
 ('the film they pulled from the cinemas', 'sell copies of the film from your phone, at a price'): [('means',
                                                                                                     'money+.04')],
 ('the film they pulled from the cinemas', 'let the film go, and keep the peace with your family'): [('door',
                                                                                                      'gave in to '
                                                                                                      'pressure')],
 ('the film they pulled from the cinemas', 'find out who paid for the campaign, and what they wanted from it'): [('lesson',
                                                                                                                  'ask '
                                                                                                                  'who '
                                                                                                                  'gains '
                                                                                                                  'from '
                                                                                                                  'it')],
 ('the film they pulled from the cinemas', 'keep a copy hidden safely, for the day the ban is lifted'): [('door',
                                                                                                          'kept it '
                                                                                                          'hidden')],
 ('the film they pulled from the cinemas', 'talk the film through with your family at the kitchen table, in your own words'): [('means',
                                                                                                                                'ties+.04')],
 ('the film they pulled from the cinemas', 'sign the open letter against the ban, with your name in full'): [('door',
                                                                                                              'defied '
                                                                                                              'an '
                                                                                                              'authority')],
 ('the last voice that knew the old songs', 'gather the family to sing together at the funeral, whatever anyone remembers'): [('means',
                                                                                                                               'ties+.05')],
 ('the last voice that knew the old songs', 'piece the songs together from fragments, old letters and notebooks'): [('mark',
                                                                                                                     'learned '
                                                                                                                     'a '
                                                                                                                     'skill')],
 ('the last voice that knew the old songs', 'ask the university for any recording they made, and offer to pay for a copy'): [('person',
                                                                                                                              'keeper')],
 ('the last voice that knew the old songs', 'sing the one verse you know at the wake, loud and off-key, the way she did'): [('lesson',
                                                                                                                             'sing '
                                                                                                                             'it '
                                                                                                                             'badly '
                                                                                                                             'but '
                                                                                                                             'sing '
                                                                                                                             'it')],
 ('the last voice that knew the old songs', 'let the songs go, and keep her in the stories the family still tells'): [('lesson',
                                                                                                                       'stories '
                                                                                                                       'outlast '
                                                                                                                       'the '
                                                                                                                       'songs')],
 ('the last voice that knew the old songs', 'make a song of your own about her, and play it wherever they will have you'): [('place',
                                                                                                                             'arts.song')],
 ('the last voice that knew the old songs', 'write down every line anyone remembers, with the tunes, for the children'): [('place',
                                                                                                                           'arts.page')],
 ('the last voice that knew the old songs', 'start a yearly night in her name where anyone may sing what they remember'): [('place',
                                                                                                                            'gather.hall')],
 ('the folk festival in the field', "learn the closing song's words, and sing it with the whole field on the last night"): [('lesson',
                                                                                                                             'one '
                                                                                                                             'song '
                                                                                                                             'can '
                                                                                                                             'hold '
                                                                                                                             'a '
                                                                                                                             'field')],
 ('the folk festival in the field', "sell the family's old craft at a stall, and come home with an order book"): [('means',
                                                                                                                   'money+.06')],
 ('the folk festival in the field', 'dance every set until the band packs up'): [('place', 'gather.great')],
 ('the folk festival in the field', 'go up on the small stage and sing the song you learned at home'): [('place',
                                                                                                         'arts.song')],
 ('the folk festival in the field', 'ask the organisers how the festival pays, and what it would take to run one'): [('person',
                                                                                                                      'mentor')],
 ('the folk festival in the field', 'record the oldest singers on your phone, with their names and their stories'): [('person',
                                                                                                                      'elder')],
 ('the folk festival in the field', "pay for a coach so the care home's old folk can come for a day"): [('mark',
                                                                                                         'helped '
                                                                                                         'someone in '
                                                                                                         'need')],
 ('the folk festival in the field', "join the procession with the town's banner and the drums"): [('means',
                                                                                                   'ties+.04')],
 ('the series with the ending nobody agrees on', 'say what you think at dinner, and listen to every side of the table'): [('means',
                                                                                                                           'ties+.03')],
 ('the series with the ending nobody agrees on', 'write a long post showing how the clues pointed to the ending all along'): [('lesson',
                                                                                                                               'the '
                                                                                                                               'clues '
                                                                                                                               'were '
                                                                                                                               'there '
                                                                                                                               'all '
                                                                                                                               'along')],
 ('the series with the ending nobody agrees on', 'keep your view to yourself, and agree with whoever matters in the room'): [('door',
                                                                                                                              'gave '
                                                                                                                              'in '
                                                                                                                              'to '
                                                                                                                              'pressure')],
 ('the series with the ending nobody agrees on', 'argue it out with your friend until one of you storms off'): [('means',
                                                                                                                 'ties-.03')],
 ('the series with the ending nobody agrees on', 'turn it off and watch the old shows with your family instead'): [('means',
                                                                                                                    'ties+.04')],
 ('the series with the ending nobody agrees on', 'say plainly it was only a story, and change the subject to the weekend'): [('lesson',
                                                                                                                              'some '
                                                                                                                              'stories '
                                                                                                                              'are '
                                                                                                                              'only '
                                                                                                                              'stories')],
 ('the series with the ending nobody agrees on', 'hold a watch party for the last episode, with food and the whole street'): [('person',
                                                                                                                               'neighbour')],
 ('the series with the ending nobody agrees on', 'make a short video of your own ending, and see who shares it'): [('place',
                                                                                                                    'arts.screen')],
 ('the series with the ending nobody agrees on', 'get a speaker to the community centre to talk about the question it asks'): [('place',
                                                                                                                                'gather.hall')],
 ('the series with the ending nobody agrees on', 'start a reading group on the book the series came from'): [('place',
                                                                                                              'arts.page')],
 ('the arts centre in the old station', 'join the town choir for the opening night, and learn your part by heart'): [('place',
                                                                                                                      'arts.song')],
 ('the arts centre in the old station', "apply for the job running the founder's programme"): [('person', 'patron')],
 ('the arts centre in the old station', 'go to the open auditions on Saturday and give it everything'): [('place',
                                                                                                          'arts.stage')],
 ('the arts centre in the old station', 'ask the centre to hang the old station photos in the foyer'): [('lesson',
                                                                                                         'a building '
                                                                                                         'can '
                                                                                                         'remember')],
 ('the arts centre in the old station', 'take a job backstage shifting sets, and keep your eyes open'): [('means',
                                                                                                          'money+.04')],
 ('the arts centre in the old station', "offer to make a show of the old station's history from the families' stories"): [('place',
                                                                                                                           'arts.tale')],
 ('the arts centre in the old station', 'pitch the centre a strange new show nobody has seen before'): [('mark',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('the arts centre in the old station', "sit on the centre's board, and see that the cheap seats stay cheap"): [('place',
                                                                                                                 'rule.counsel')],
 ('the arts centre in the old station', 'start a youth theatre in the centre that anyone can join for free'): [('place',
                                                                                                                'arts.stage'),
                                                                                                               ('means',
                                                                                                                'time-.06')],
 ('the venues close and the band plays kitchens', "put in for the council's free concerts in the square"): [('means',
                                                                                                             'money+.03')],
 ('the venues close and the band plays kitchens', 'take a day job, and play only when the pay is decent'): [('means',
                                                                                                             'money+.06')],
 ('the venues close and the band plays kitchens', 'play every kitchen party going, for food and the hat'): [('place',
                                                                                                             'gather.house')],
 ('the venues close and the band plays kitchens', 'sell the spare gear to get through the winter, and keep the one guitar'): [('means',
                                                                                                                               'money+.04')],
 ('the venues close and the band plays kitchens', 'teach lessons by video to pupils far away who can still pay'): [('means',
                                                                                                                    'money+.05')],
 ('the venues close and the band plays kitchens', 'record an album in the kitchen on a laptop, rough and live'): [('lesson',
                                                                                                                   'rough '
                                                                                                                   'can '
                                                                                                                   'still '
                                                                                                                   'be '
                                                                                                                   'true')],
 ('the venues close and the band plays kitchens', 'gather the out-of-work players into one big band for a free night in the square'): [('means',
                                                                                                                                        'ties+.06')],
 ('every song in your pocket', 'start a singing night at the hall, where the whole room sings the same songs'): [('place',
                                                                                                                  'gather.hall')],
 ('every song in your pocket', 'build a following online, one song a week, and charge for the live shows'): [('means',
                                                                                                              'money+.05')],
 ('every song in your pocket', 'make a song tonight and put it out by morning'): [('lesson',
                                                                                   'nobody needs to give '
                                                                                   'permission')],
 ('every song in your pocket', 'take the playing to weddings and parties, where people still pay for a band'): [('means',
                                                                                                                 'money+.04')],
 ('every song in your pocket', 'team up with your friend and push the song until it goes everywhere'): [('mark',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('every song in your pocket', 'build a new sound from samples of a hundred old records'): [('lesson',
                                                                                             'old records hold new '
                                                                                             'songs')],
 ('every song in your pocket', 'keep the cover band going once a month, for those who still come'): [('place',
                                                                                                      'arts.song')],
 ('every song in your pocket', "teach the neighbours' children to play, so they make music as well as hear it"): [('person',
                                                                                                                   'neighbour')],
 ('the song about the empty chair', 'stand for the anthem at the match, and sing every word'): [('place',
                                                                                                 'gather.games')],
 ('the song about the empty chair', 'ask why the songs changed, and write about what each one left out'): [('place',
                                                                                                            'arts.page')],
 ('the song about the empty chair', 'sing the war songs at the camps and the town halls, and make your name'): [('means',
                                                                                                                 'money+.05')],
 ('the song about the empty chair', 'teach the children the old tune with the old words, as your grandmother did'): [('means',
                                                                                                                      'ties+.04')],
 ('the song about the empty chair', "sing the empty-chair song at a neighbour's wake, plainly, as it is"): [('person',
                                                                                                             'neighbour')],
 ('the song about the empty chair', 'play the old dance tunes at the homecoming, so people can dance again'): [('place',
                                                                                                                'gather.great')],
 ('the song about the empty chair', 'notice which songs the news plays and which it never does'): [('lesson',
                                                                                                    'what is left '
                                                                                                    'out matters')],
 ('the song about the empty chair', 'lead the choir in the empty-chair song at the memorial in the square'): [('place',
                                                                                                               'arts.song')],
 ('the song about the empty chair', "collect the soldiers' own songs and letters for the town's memorial book"): [('place',
                                                                                                                   'learn.keeping')],
 ('the sketch about the minister', 'say at the table that the sketch should mock what he did, not how he talks'): [('lesson',
                                                                                                                    'mock '
                                                                                                                    'the '
                                                                                                                    'deed '
                                                                                                                    'not '
                                                                                                                    'the '
                                                                                                                    'voice')],
 ('the sketch about the minister', "look up the minister's real words, and share them beside the sketch"): [('lesson',
                                                                                                             'the '
                                                                                                             'record '
                                                                                                             'speaks '
                                                                                                             'for '
                                                                                                             'itself')],
 ('the sketch about the minister', 'keep quiet about it, since you cannot know who is listening'): [('door',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ('the sketch about the minister', 'sing the best line out loud in the canteen, and get the room going'): [('person',
                                                                                                            'colleague')],
 ('the sketch about the minister', "stand up for the home town's way of talking, and leave the minister to his own"): [('means',
                                                                                                                        'ties+.03')],
 ('the sketch about the minister', 'write your own sketch about the local council, and do it at the open mic'): [('place',
                                                                                                                  'arts.stage')],
 ('the sketch about the minister', 'sing it with the crowd at the match, a whole stand at once'): [('place',
                                                                                                    'gather.games')],
 ('the sketch about the minister', 'watch who laughs and who does not, and remember it'): [('door', 'made an enemy')],
 ('the sketch about the minister', 'keep the sketch away from the family dinner, where half the table voted for him'): [('means',
                                                                                                                         'ties+.04')],
 ('the sketch about the minister', 'write to the paper asking for an inquiry into what the minister did'): [('place',
                                                                                                             'rule.voice')],
 ("a classmate's song is everywhere", 'send a warm message saying the whole town is proud, and mean it'): [('person',
                                                                                                            'friend')],
 ("a classmate's song is everywhere", 'answer the message, and offer to help run the tour'): [('person',
                                                                                               'colleague')],
 ("a classmate's song is everywhere", 'pick up the old guitar again, and play your own songs at the open mic'): [('place',
                                                                                                                  'arts.song')],
 ("a classmate's song is everywhere", "play the song at the family's Sunday dinner, and tell everyone where it comes from"): [('means',
                                                                                                                               'ties+.03')],
 ("a classmate's song is everywhere", 'ask the classmate how they got the song heard, and do the same'): [('person',
                                                                                                           'mentor')],
 ("a classmate's song is everywhere", 'write a song of your own about the town, and post it the same night'): [('lesson',
                                                                                                                'your '
                                                                                                                'own '
                                                                                                                'town '
                                                                                                                'is '
                                                                                                                'a '
                                                                                                                'song')],
 ("a classmate's song is everywhere", 'put up the money for a homecoming gig, and give the takings to the school'): [('means',
                                                                                                                      'money-.06')],
 ("a classmate's song is everywhere", 'ask the classmate to come back and sing at the summer fair'): [('place',
                                                                                                       'gather.great')],
 ('the director everyone admired', 'stand with the actors who spoke, and say so where people can hear'): [('mark',
                                                                                                           'defied '
                                                                                                           'an '
                                                                                                           'authority')],
 ('the director everyone admired', 'read every account in full before judging'): [('lesson',
                                                                                   'hear every side first')],
 ('the director everyone admired', 'sell your signed posters while they still fetch a price'): [('means',
                                                                                                 'money+.03')],
 ('the director everyone admired', 'throw out the box set in a rage, and tell everyone why'): [('means', 'ties-.03')],
 ('the director everyone admired', 'keep watching the films quietly with the family, as you always have'): [('means',
                                                                                                             'ties+.03')],
 ('the director everyone admired', 'keep the films, and learn what the actors themselves put into them'): [('lesson',
                                                                                                            'the '
                                                                                                            'actors '
                                                                                                            'made it '
                                                                                                            'too')],
 ('the director everyone admired', 'make a short film of your own about a set where nobody shouts'): [('place',
                                                                                                       'arts.screen')],
 ('the director everyone admired', 'give to the fund the actors have set up for others in the same trade'): [('mark',
                                                                                                              'helped '
                                                                                                              'someone '
                                                                                                              'in '
                                                                                                              'need')],
 ('the director everyone admired', 'talk it through with your friend, and agree to differ without falling out'): [('means',
                                                                                                                   'ties+.04')],
 ('the last night at the little theatre', 'sell programmes at the final show, so the last night runs as it should'): [('person',
                                                                                                                       'regular')],
 ('the last night at the little theatre', 'find out what saving the building would truly cost, and show the town'): [('lesson',
                                                                                                                      'know '
                                                                                                                      'the '
                                                                                                                      'cost '
                                                                                                                      'before '
                                                                                                                      'the '
                                                                                                                      'fight')],
 ('the last night at the little theatre', 'ask the developer to keep a small stage on the ground floor of the flats'): [('person',
                                                                                                                         'patron')],
 ('the last night at the little theatre', 'stage one last wild show of your own on the night after the final one'): [('mark',
                                                                                                                      'took '
                                                                                                                      'a '
                                                                                                                      'wild '
                                                                                                                      'risk')],
 ('the last night at the little theatre', "sit in the family's row at the final show, and take home the seat plate"): [('means',
                                                                                                                        'ties+.03')],
 ('the last night at the little theatre', 'say goodbye on the last night, and take the family to the new place in town'): [('place',
                                                                                                                            'arts.stage')],
 ('the last night at the little theatre', 'start a company of your own in a room above a shop with the old cast'): [('place',
                                                                                                                     'arts.stage')],
 ('the last night at the little theatre', "gather the theatre's programmes and photos for the town archive"): [('place',
                                                                                                                'learn.keeping')],
 ('the last night at the little theatre', 'lead a march down the main street to save the theatre'): [('place',
                                                                                                      'rule.voice')],
 ('the last night at the little theatre', 'raise a petition, and put a costed plan for a trust to the council'): [('place',
                                                                                                                   'rule.counsel')],
 ('the village pottery sells far away', 'ask the village to register the old patterns, so no factory can copy them'): [('place',
                                                                                                                        'rule.counsel')],
 ('the village pottery sells far away', 'let no piece leave the kiln until it is right, orders or not'): [('lesson',
                                                                                                           'right is '
                                                                                                           'worth '
                                                                                                           'the '
                                                                                                           'wait')],
 ('the village pottery sells far away', "take the dealer's order for a thousand, and hire help to fill it"): [('means',
                                                                                                               'money+.10')],
 ('the village pottery sells far away', 'throw the workshop open to the visitors, with music and the wheel going'): [('means',
                                                                                                                      'ties+.05')],
 ('the village pottery sells far away', 'keep making the old patterns only, whatever the dealer offers'): [('means',
                                                                                                            'money-.04')],
 ('the village pottery sells far away', "make the dealer's design on weekdays and the old patterns at the weekend"): [('means',
                                                                                                                       'time-.05')],
 ('the village pottery sells far away', 'open your own shop online, with your own name and your own designs'): [('place',
                                                                                                                 'comm.shop')],
 ('the village pottery sells far away', "invent a new glaze that keeps the old lines and catches a visitor's eye"): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the village pottery sells far away', "help the co-op set fair prices, so every family's kiln gets orders"): [('place',
                                                                                                                 'comm.market')],
 ('the village pottery sells far away', 'start classes in the old craft for the young who have come home'): [('place',
                                                                                                              'arts.craft')],
 ('a free music school with instruments to borrow', 'join the open choir, and sing in the spring concert'): [('place',
                                                                                                              'arts.song')],
 ('a free music school with instruments to borrow', 'apply for the paid post running the school'): [('means',
                                                                                                     'money+.05')],
 ('a free music school with instruments to borrow', 'play the drum kit in the back room every night it is open'): [('place',
                                                                                                                    'gather.hall')],
 ('a free music school with instruments to borrow', 'start a band with the other beginners in your class'): [('person',
                                                                                                              'friend')],
 ('a free music school with instruments to borrow', "audition for the school's top group, and the scholarship that comes with it"): [('person',
                                                                                                                                      'teacher')],
 ('a free music school with instruments to borrow', "play with the school's band at the street party in summer"): [('person',
                                                                                                                    'neighbour')],
 ('a free music school with instruments to borrow', "help teach the beginners' class one evening a week"): [('person',
                                                                                                             'colleague')],
 ('the archive wiped clean', 'hand the phone in, as the new rules say, and keep the peace'): [('lesson',
                                                                                               'some losses are '
                                                                                               'chosen')],
 ('the archive wiped clean', 'make a quiet list of every song and dance the archive held'): [('place',
                                                                                              'learn.keeping')],
 ('the archive wiped clean', 'copy the recording, and pass it only to people who can repay the favour'): [('person',
                                                                                                           'patron')],
 ('the archive wiped clean', 'sing the old songs to the children at home, behind closed curtains'): [('means',
                                                                                                      'ties+.04')],
 ('the archive wiped clean', 'play the banned songs at an underground night, for a paying crowd'): [('means',
                                                                                                     'money+.04')],
 ('the archive wiped clean', 'hide copies in a dozen places nobody would think to look'): [('door',
                                                                                            'kept it hidden')],
 ('the archive wiped clean', "teach the old songs to the neighbours' children along with your own"): [('person',
                                                                                                       'neighbour')],
 ('the archive wiped clean', 'send a copy to a library abroad that keeps what others destroy'): [('door',
                                                                                                  'defied an '
                                                                                                  'authority')],
 ('a novel in the home tongue', 'ask the school to teach the home tongue to every child who wants it'): [('place',
                                                                                                          'rule.voice')],
 ('a novel in the home tongue', 'keep to the ruling tongue at work and in letters, where it still counts for more'): [('door',
                                                                                                                       'gave '
                                                                                                                       'in '
                                                                                                                       'to '
                                                                                                                       'pressure')],
 ('a novel in the home tongue', 'quote the best lines loudly, online and in the street'): [('lesson',
                                                                                            'the old words still '
                                                                                            'bite')],
 ('a novel in the home tongue', 'read the novel aloud at the family table, a chapter every evening'): [('means',
                                                                                                        'ties+.05')],
 ('a novel in the home tongue', 'write a story of your own in the home tongue, and send it to a publisher'): [('place',
                                                                                                               'arts.page')],
 ('a novel in the home tongue', 'turn a chapter into a play for the street party, in the home tongue'): [('person',
                                                                                                          'neighbour')],
 ('a novel in the home tongue', 'write down the old sayings your grandparents use, before they are lost'): [('place',
                                                                                                             'arts.tale')],
 ('a novel in the home tongue', 'pay for copies of the novel for the town library and the care home'): [('means',
                                                                                                         'money-.04')],
 ('a novel in the home tongue', 'start a reading group in the home tongue at the library'): [('place',
                                                                                              'learn.keeping')],
 ('the band comes home after the flood', 'lead the closing song for the families who lost their homes'): [('means',
                                                                                                           'ties+.04')],
 ('the band comes home after the flood', 'keep the books for the night, so every gift is counted and seen'): [('lesson',
                                                                                                               'counted '
                                                                                                               'gifts '
                                                                                                               'are '
                                                                                                               'trusted '
                                                                                                               'gifts')],
 ('the band comes home after the flood', 'have your business named on the poster, in return for a big gift'): [('means',
                                                                                                                'money-.08')],
 ('the band comes home after the flood', 'warm up the crowd before the band, and get the buckets filled'): [('place',
                                                                                                             'arts.stage')],
 ('the band comes home after the flood', 'sell tea and cakes at the gate, and hand over all the takings'): [('mark',
                                                                                                             'helped '
                                                                                                             'someone '
                                                                                                             'in '
                                                                                                             'need')],
 ('the band comes home after the flood', 'record the night, and the stories of the flooded families, for the town'): [('place',
                                                                                                                       'learn.keeping')],
 ('the band comes home after the flood', "match every bucket's takings from your own savings, and say so on the night"): [('means',
                                                                                                                           'money-.10')],
 ('the band comes home after the flood', 'rally the crowd to sign up for the rebuilding, then and there'): [('place',
                                                                                                             'prot.rescue')],
 ('the street pulls together after the storm', 'find out who needs power for a machine, and plan whose turn the generator is'): [('lesson',
                                                                                                                                  'a '
                                                                                                                                  'plan '
                                                                                                                                  'beats '
                                                                                                                                  'a '
                                                                                                                                  'scramble')],
 ('the street pulls together after the storm', 'run your generator for the old neighbour, and ask the street to chip in for fuel'): [('means',
                                                                                                                                      'money-.03')],
 ('the street pulls together after the storm', 'drive the old neighbour to the clinic before the low road floods'): [('person',
                                                                                                                      'elder')],
 ('the street pulls together after the storm', 'open your house as the warm room for anyone without heat tonight'): [('place',
                                                                                                                      'gather.house')],
 ('the street pulls together after the storm', 'run a cable from your generator to three houses, though it is not allowed'): [('door',
                                                                                                                               'broke '
                                                                                                                               'the '
                                                                                                                               'law')],
 ('the street pulls together after the storm', "check each old neighbour's pills, and make sure nobody runs out before the roads open"): [('mark',
                                                                                                                                           'helped '
                                                                                                                                           'someone '
                                                                                                                                           'in '
                                                                                                                                           'need')],
 ('the street pulls together after the storm', 'join the crew clearing the fallen tree from the road to the clinic'): [('person',
                                                                                                                        'neighbour')],
 ('the street pulls together after the storm', 'pin a list on the noticeboard of who needs what and who can give it'): [('means',
                                                                                                                         'ties+.03')],
 ('a medicine in the cupboard is withdrawn', 'write a formal complaint to the health board, with the dates and the prescription'): [('lesson',
                                                                                                                                     'put '
                                                                                                                                     'it '
                                                                                                                                     'in '
                                                                                                                                     'writing')],
 ('a medicine in the cupboard is withdrawn', 'book your parent a heart check, and go through the study with the doctor'): [('means',
                                                                                                                            'time-.03')],
 ('a medicine in the cupboard is withdrawn', "sign your parent up to the group claim against the pill's maker"): [('means',
                                                                                                                   'money+.03')],
 ('a medicine in the cupboard is withdrawn', "spend the next weeks at your parent's side, and keep the house calm"): [('means',
                                                                                                                       'time-.06')],
 ('a medicine in the cupboard is withdrawn', 'take your parent off the new pills and onto walks, rest and good food'): [('means',
                                                                                                                         'health+.03')],
 ('a medicine in the cupboard is withdrawn', 'find a specialist of your own choosing for a second opinion'): [('place',
                                                                                                               'care.houses')],
 ('a medicine in the cupboard is withdrawn', 'get the other patients talking online, and push the maker for the full data'): [('means',
                                                                                                                               'ties+.03')],
 ('a medicine in the cupboard is withdrawn', 'press the health board to pay for heart checks for everyone who took it'): [('place',
                                                                                                                           'rule.voice')],
 ('a medicine in the cupboard is withdrawn', 'start a support group for the families of people who took the pill'): [('place',
                                                                                                                      'gather.talk')],
 ('the new vaccine splits the dinner table', 'book the vaccine for yourself, and help the old neighbours book theirs'): [('person',
                                                                                                                          'neighbour')],
 ('the new vaccine splits the dinner table', 'send your sibling the study, with the numbers marked, and ask them to read it'): [('lesson',
                                                                                                                                 'show '
                                                                                                                                 'your '
                                                                                                                                 'working')],
 ('the new vaccine splits the dinner table', 'ask your own doctor about your own case, and decide in your own time'): [('means',
                                                                                                                        'freedom+.03')],
 ('the new vaccine splits the dinner table', 'change the subject, pass the potatoes, and keep the family at one table'): [('lesson',
                                                                                                                           'peace '
                                                                                                                           'at '
                                                                                                                           'the '
                                                                                                                           'table '
                                                                                                                           'first')],
 ('the new vaccine splits the dinner table', 'wait and see how it goes for others before deciding anything'): [('door',
                                                                                                                'turned '
                                                                                                                'down '
                                                                                                                'a '
                                                                                                                'chance')],
 ('the new vaccine splits the dinner table', 'take it on the first day, and tell everyone honestly how it went'): [('means',
                                                                                                                    'health+.03')],
 ('the new vaccine splits the dinner table', "ask the family doctor round to answer everyone's questions over tea"): [('means',
                                                                                                                       'ties+.03')],
 ('the new vaccine splits the dinner table', 'volunteer at the vaccine clinic, checking names and answering questions'): [('place',
                                                                                                                           'care.houses')],
 ('a new birth centre in town', 'go with your sibling to the open evening, and ask about every safety check'): [('means',
                                                                                                                 'ties+.03')],
 ('a new birth centre in town', 'read the figures for both places, and lay them out plainly for the family'): [('lesson',
                                                                                                                'lay '
                                                                                                                'the '
                                                                                                                'numbers '
                                                                                                                'out '
                                                                                                                'plainly')],
 ('a new birth centre in town', 'tell the family the choice belongs to the parents, and make them stop arguing'): [('lesson',
                                                                                                                    'their '
                                                                                                                    'baby, '
                                                                                                                    'their '
                                                                                                                    'choice')],
 ('a new birth centre in town', 'cook and freeze meals for the weeks after the birth'): [('means', 'time-.03')],
 ('a new birth centre in town', 'help them write a birth plan of their own, with every choice spelled out'): [('means',
                                                                                                               'time-.02')],
 ('a new birth centre in town', "sit in on a midwives' class and learn what the first weeks really need"): [('mark',
                                                                                                             'learned '
                                                                                                             'a '
                                                                                                             'skill')],
 ('a new birth centre in town', "give to the new unit's appeal, and see the family's name on the donors' board"): [('means',
                                                                                                                    'money-.06')],
 ('a new birth centre in town', 'sign up as a volunteer driver, taking families to the birth centre at night'): [('place',
                                                                                                                  'care.houses')],
 ('the labour that stalls in the night', 'do exactly as the staff ask, and keep out of their way'): [('lesson',
                                                                                                      'trust the '
                                                                                                      'people who '
                                                                                                      'know')],
 ('the labour that stalls in the night', 'ask the midwife to explain each step, and pass it on plainly to the family'): [('means',
                                                                                                                          'ties+.03')],
 ('the labour that stalls in the night', 'ask for the senior surgeon by name, and ask to be beside your partner in theatre'): [('person',
                                                                                                                                'keeper')],
 ('the labour that stalls in the night', 'talk and joke with your partner all the way to theatre, to keep the fear away'): [('means',
                                                                                                                             'ties+.03')],
 ('the labour that stalls in the night', "hold your partner's hand and breathe with them, slow and steady"): [('means',
                                                                                                               'ties+.04')],
 ('the labour that stalls in the night', 'tell both families plainly what is happening, and ask them to wait at home'): [('means',
                                                                                                                          'ties-.02')],
 ('the labour that stalls in the night', "rub your partner's back through each wave of pain until the team arrives"): [('mark',
                                                                                                                        'helped '
                                                                                                                        'someone '
                                                                                                                        'in '
                                                                                                                        'need')],
 ('the labour that stalls in the night', 'read the consent form line by line, and ask what each risk really means'): [('lesson',
                                                                                                                       'ask '
                                                                                                                       'what '
                                                                                                                       'each '
                                                                                                                       'risk '
                                                                                                                       'means')],
 ('the labour that stalls in the night', 'run for the midwife the moment the monitor changes'): [('door',
                                                                                                  'helped someone in '
                                                                                                  'need')],
 ('the labour that stalls in the night', 'write down every time and every word the doctors say, for later'): [('means',
                                                                                                               'ties+.02')],
 ('the hospice nurse comes every morning', 'keep the family rota, so someone is with your parent day and night'): [('means',
                                                                                                                    'time-.06')],
 ('the hospice nurse comes every morning', 'ask the nurse plainly what the last days will bring, and tell the family'): [('person',
                                                                                                                          'keeper')],
 ('the hospice nurse comes every morning', 'help your parent write down their own wishes for the end, and see them kept'): [('door',
                                                                                                                             'kept '
                                                                                                                             'your '
                                                                                                                             'word')],
 ('the hospice nurse comes every morning', 'bring in the old friends, the music and the stories for one last good evening'): [('means',
                                                                                                                               'ties+.04')],
 ('the hospice nurse comes every morning', 'sit by the bed in the evenings and simply hold their hand'): [('lesson',
                                                                                                           'being '
                                                                                                           'there is '
                                                                                                           'enough')],
 ('the hospice nurse comes every morning', 'pour your parent the glass of whisky they ask for, whatever the leaflet says'): [('lesson',
                                                                                                                              'small '
                                                                                                                              'joys '
                                                                                                                              'to '
                                                                                                                              'the '
                                                                                                                              'very '
                                                                                                                              'end')],
 ('the hospice nurse comes every morning', 'set up a video call, so the cousins far away can say goodbye'): [('means',
                                                                                                              'ties+.03')],
 ('the hospice nurse comes every morning', 'give to the hospice that cares for your parent, and join its circle of friends'): [('place',
                                                                                                                                'care.houses')],
 ('the hospice nurse comes every morning', 'share the nights with your siblings, so that no one wears out'): [('means',
                                                                                                               'health+.03')],
 ('a clinic opens on the corner', "register the whole family at the clinic, and book everyone's check-ups"): [('place',
                                                                                                               'care.houses')],
 ('a clinic opens on the corner', 'book the blood tests you have put off for two years'): [('means', 'health+.03')],
 ('a clinic opens on the corner', 'apply for the part-time post on the desk, on hours that suit you'): [('means',
                                                                                                         'money+.06')],
 ('a clinic opens on the corner', 'take your parent along, and introduce them to the nurse yourself'): [('means',
                                                                                                         'ties+.03')],
 ('a clinic opens on the corner', 'tell your parent plainly that the cough needs looking at, and walk them in'): [('mark',
                                                                                                                   'helped '
                                                                                                                   'someone '
                                                                                                                   'in '
                                                                                                                   'need')],
 ('a clinic opens on the corner', "join the clinic's walking group on Saturday mornings"): [('place',
                                                                                             'gather.circle')],
 ('a clinic opens on the corner', "offer to set up the clinic's online booking yourself, over a weekend"): [('person',
                                                                                                             'keeper')],
 ('a clinic opens on the corner', "give to the appeal for the clinic's new wing, and see your name on the board"): [('means',
                                                                                                                     'money-.06')],
 ('a clinic opens on the corner', "join the patients' group that checks the clinic keeps its promises"): [('place',
                                                                                                           'rule.counsel')],
 ('the tap water is safe again', "follow the council's notice to the letter: flush the pipes and change the filters"): [('means',
                                                                                                                         'health+.03')],
 ('the tap water is safe again', 'send a sample from your own tap away for testing before trusting it'): [('means',
                                                                                                           'money-.03')],
 ('the tap water is safe again', 'cancel the bottled water, and put what you save toward something of your own'): [('means',
                                                                                                                    'money+.03')],
 ('the tap water is safe again', 'fill a glass from the tap the first morning and drink it down'): [('lesson',
                                                                                                     'taste it and '
                                                                                                     'see')],
 ('the tap water is safe again', 'take a jug of the new water to the old neighbour who still distrusts it'): [('person',
                                                                                                               'neighbour')],
 ('the tap water is safe again', "read the council's report, and find out who will be paying for the works"): [('lesson',
                                                                                                                'follow '
                                                                                                                'the '
                                                                                                                'money')],
 ('the tap water is safe again', 'start a vegetable plot again, now the water is safe to use on it'): [('place',
                                                                                                        'prod.land')],
 ('the tap water is safe again', 'help the council tell the housebound, door by door, that the water is safe'): [('mark',
                                                                                                                  'helped '
                                                                                                                  'someone '
                                                                                                                  'in '
                                                                                                                  'need')],
 ('the tap water is safe again', 'volunteer to hand out safe water in the last week of the works'): [('means',
                                                                                                      'ties+.03')],
 ("a grandparent's remedy no one else knows", 'write the recipe down exactly, with every amount, and share it with the family'): [('means',
                                                                                                                                   'ties+.03')],
 ("a grandparent's remedy no one else knows", 'ask the pharmacist what in the tea might really work, and why'): [('lesson',
                                                                                                                  'old '
                                                                                                                  'remedies '
                                                                                                                  'can '
                                                                                                                  'have '
                                                                                                                  'reasons')],
 ("a grandparent's remedy no one else knows", 'ask your grandparent to teach you alone, and keep the recipe as your own'): [('door',
                                                                                                                             'kept '
                                                                                                                             'it '
                                                                                                                             'hidden')],
 ("a grandparent's remedy no one else knows", 'brew it with your grandparent tonight, guessing the amounts and laughing at the mistakes'): [('lesson',
                                                                                                                                             'laugh '
                                                                                                                                             'at '
                                                                                                                                             'your '
                                                                                                                                             'mistakes')],
 ("a grandparent's remedy no one else knows", 'find out which of the herbs are safe and which are not, before anyone drinks it'): [('place',
                                                                                                                                    'learn.keeping')],
 ("a grandparent's remedy no one else knows", 'film your grandparent making it, and post it online for anyone to try'): [('place',
                                                                                                                          'arts.screen')],
 ("a grandparent's remedy no one else knows", 'gather the cousins for a Sunday when your grandparent teaches all of you'): [('place',
                                                                                                                             'gather.house')],
 ("a grandparent's remedy no one else knows", 'make a big pot when colds go round, and carry cups door to door'): [('person',
                                                                                                                    'neighbour')],
 ('a mutual aid fund on the street', 'sign up, pay your share every month, and never miss a payment'): [('place',
                                                                                                         'gather.hall')],
 ('a mutual aid fund on the street', "offer to keep the fund's books, and post them every month for all to see"): [('means',
                                                                                                                    'time-.03')],
 ('a mutual aid fund on the street', 'stand for treasurer, and run the fund the way you think best'): [('place',
                                                                                                        'rule.counsel')],
 ('a mutual aid fund on the street', "put your name first on the drivers' list, for any hour of the night"): [('person',
                                                                                                               'neighbour')],
 ('a mutual aid fund on the street', "cook the first week's meals for whoever on the street is ill"): [('mark',
                                                                                                        'helped '
                                                                                                        'someone in '
                                                                                                        'need')],
 ('a mutual aid fund on the street', 'pay in when it suits, and help out your own way when the mood takes'): [('means',
                                                                                                               'freedom+.03')],
 ('a mutual aid fund on the street', "list everyone's needs and skills, and match the one to the other"): [('means',
                                                                                                            'ties+.04')],
 ('a mutual aid fund on the street', 'put in a larger sum to start the fund, and take a seat on its committee'): [('means',
                                                                                                                   'money-.06')],
 ('a mutual aid fund on the street', "write the group's rules, so everyone knows who pays and who gets help"): [('lesson',
                                                                                                                 'clear '
                                                                                                                 'rules '
                                                                                                                 'keep '
                                                                                                                 'the '
                                                                                                                 'peace')],
 ('a carer lets a parent stay at home', 'go through the care plan with the carer, and keep the rota on the fridge'): [('means',
                                                                                                                       'time+.03')],
 ('a carer lets a parent stay at home', "keep a notebook of your parent's good days and bad days, and spot what changes"): [('lesson',
                                                                                                                             'small '
                                                                                                                             'changes '
                                                                                                                             'tell '
                                                                                                                             'you '
                                                                                                                             'most')],
 ('a carer lets a parent stay at home', 'take your evenings back, and put them into your own work at last'): [('means',
                                                                                                               'time+.06')],
 ('a carer lets a parent stay at home', 'drop in unannounced now and then, with cake, to see how things really are'): [('means',
                                                                                                                        'ties+.03')],
 ('a carer lets a parent stay at home', 'bring the grandchildren round every Sunday, the way it has always been'): [('place',
                                                                                                                     'gather.house')],
 ('a carer lets a parent stay at home', 'tell your parent plainly that this help is how they keep their own front door'): [('lesson',
                                                                                                                            'plain '
                                                                                                                            'words '
                                                                                                                            'can '
                                                                                                                            'be '
                                                                                                                            'kind')],
 ('a carer lets a parent stay at home', 'rearrange the flat with your parent, so everything they need is within reach'): [('mark',
                                                                                                                           'helped '
                                                                                                                           'someone '
                                                                                                                           'in '
                                                                                                                           'need')],
 ('a carer lets a parent stay at home', 'fit a call button and a door camera, and teach your parent to use them'): [('means',
                                                                                                                     'money-.03')],
 ('a carer lets a parent stay at home', 'pay more into a pension of your own, now you see what one buys'): [('means',
                                                                                                             'money-.04')],
 ('a carer lets a parent stay at home', 'sign up as a volunteer driver for the old people on your street'): [('place',
                                                                                                              'care.houses')],
 ('care becomes free at the point of need', 'take your place in the queue for the knee, as everyone must'): [('lesson',
                                                                                                              'the '
                                                                                                              'same '
                                                                                                              'queue '
                                                                                                              'for '
                                                                                                              'all')],
 ('care becomes free at the point of need', 'ask the doctor how your case is scored, and what would move it up the list'): [('lesson',
                                                                                                                             'ask '
                                                                                                                             'how '
                                                                                                                             'the '
                                                                                                                             'list '
                                                                                                                             'works')],
 ('care becomes free at the point of need', 'pay a private clinic to fix the knee next month'): [('means',
                                                                                                  'money-.06')],
 ('care becomes free at the point of need', 'drive your parent to every appointment, and make the recovery a party'): [('means',
                                                                                                                        'ties+.04')],
 ('care becomes free at the point of need', 'nurse your parent at home through the weeks after the operation'): [('means',
                                                                                                                  'time-.06')],
 ('care becomes free at the point of need', 'ignore the knee, and keep playing on it, waiting list or not'): [('means',
                                                                                                               'health-.06')],
 ('care becomes free at the point of need', 'strengthen the knee yourself with swimming and long walks while you wait'): [('means',
                                                                                                                           'health+.05')],
 ('care becomes free at the point of need', 'find out which hospital in the region has the shortest list, and go there'): [('means',
                                                                                                                            'time-.03')],
 ('care becomes free at the point of need', "help at the hospital's friends' group, so the queue moves for others"): [('place',
                                                                                                                       'care.houses')],
 ('care becomes free at the point of need', 'write to the health board with the figures on the waits, and ask for more staff'): [('place',
                                                                                                                                  'rule.voice')],
 ('the treatment the insurance will not cover', "apply to the hospital's hardship fund, with every form filled in properly"): [('means',
                                                                                                                                'money+.03')],
 ('the treatment the insurance will not cover', 'read the policy clause by clause, and appeal on the line they missed'): [('lesson',
                                                                                                                           'read '
                                                                                                                           'the '
                                                                                                                           'small '
                                                                                                                           'print')],
 ('the treatment the insurance will not cover', 'ring the billing office and bargain the price down, line by line'): [('means',
                                                                                                                       'money-.06')],
 ('the treatment the insurance will not cover', 'call the insurer every day until a manager agrees to look again'): [('means',
                                                                                                                      'time-.03')],
 ('the treatment the insurance will not cover', 'ask the family to share the cost, and sell the car if you must'): [('means',
                                                                                                                     'freedom-.04')],
 ('the treatment the insurance will not cover', 'tell your partner plainly what you can and cannot afford, and choose together'): [('lesson',
                                                                                                                                    'decide '
                                                                                                                                    'it '
                                                                                                                                    'together')],
 ('the treatment the insurance will not cover', 'find the doctor in town who treats people for nothing on Thursdays'): [('place',
                                                                                                                         'care.houses')],
 ('the treatment the insurance will not cover', "start a fundraiser and tell your partner's story to everyone you know"): [('means',
                                                                                                                            'money+.06')],
 ('the treatment the insurance will not cover', "join the patients' campaign pressing for the treatment to be covered"): [('place',
                                                                                                                           'rule.voice')],
 ('the care home where nobody knows the names', 'put it in writing to the manager and the inspectors that the standards are not met'): [('door',
                                                                                                                                         'defied '
                                                                                                                                         'an '
                                                                                                                                         'authority')],
 ('the care home where nobody knows the names', "pin a page on your parent's needs by the bed, for every new face"): [('lesson',
                                                                                                                       'write '
                                                                                                                       'down '
                                                                                                                       'what '
                                                                                                                       'matters')],
 ('the care home where nobody knows the names', 'hire a carer of your own choosing to sit with your parent three afternoons a week'): [('means',
                                                                                                                                        'money-.10')],
 ('the care home where nobody knows the names', "come in every evening after work, and do your parent's bedtime round yourself"): [('means',
                                                                                                                                    'time-.06')],
 ('the care home where nobody knows the names', "cut your hours at work, and take on your parent's care at home"): [('means',
                                                                                                                     'money-.06'),
                                                                                                                    ('means',
                                                                                                                     'time-.08')],
 ('the care home where nobody knows the names', 'take your parent out into the garden on every visit, whatever the rota says'): [('lesson',
                                                                                                                                  'a '
                                                                                                                                  'little '
                                                                                                                                  'sun '
                                                                                                                                  'goes '
                                                                                                                                  'far')],
 ('the care home where nobody knows the names', 'compare the staffing at every care home nearby, and move your parent to the best'): [('person',
                                                                                                                                       'keeper')],
 ('the care home where nobody knows the names', "join the home's board of friends, and raise money to pay the carers better"): [('place',
                                                                                                                                 'care.houses')],
 ('the care home where nobody knows the names', 'set up a rota with your siblings, so that one of you visits every day'): [('means',
                                                                                                                            'ties+.04')],
 ('a brother or sister home from the war, changed', "book your sibling into the veterans' team, and go with them to the first session"): [('place',
                                                                                                                                           'care.houses')],
 ('a brother or sister home from the war, changed', "tell your sibling the choice is theirs, and leave the clinic's letter on the table"): [('lesson',
                                                                                                                                             'some '
                                                                                                                                             'choices '
                                                                                                                                             'are '
                                                                                                                                             'not '
                                                                                                                                             'yours')],
 ('a brother or sister home from the war, changed', 'turn up every Saturday and get your sibling out of the house, whatever it takes'): [('means',
                                                                                                                                          'time-.04')],
 ('a brother or sister home from the war, changed', 'let your sibling move back in with the family for a quiet season'): [('door',
                                                                                                                           'took '
                                                                                                                           'them '
                                                                                                                           'in')],
 ('a brother or sister home from the war, changed', 'tell your sibling plainly that they are not well, and that it is no shame'): [('lesson',
                                                                                                                                    'say '
                                                                                                                                    'the '
                                                                                                                                    'hard '
                                                                                                                                    'thing '
                                                                                                                                    'kindly')],
 ('a brother or sister home from the war, changed', 'take your sibling on long rides and loud nights out, the way you used to'): [('means',
                                                                                                                                   'health-.03')],
 ('a brother or sister home from the war, changed', 'go along with your sibling to the new therapy the clinic is trying out'): [('place',
                                                                                                                                 'gather.talk')],
 ('a brother or sister home from the war, changed', 'ask the old friends to visit in turn, so your sibling is never alone long'): [('means',
                                                                                                                                    'ties+.04')],
 ('a brother or sister home from the war, changed', 'press the clinic for a proper plan in writing, with dates'): [('person',
                                                                                                                    'keeper')],
 ("the famous surgeon's two-year list", "ask your parent's doctor for a referral, and get them on the list properly"): [('lesson',
                                                                                                                         'do '
                                                                                                                         'it '
                                                                                                                         'properly '
                                                                                                                         'from '
                                                                                                                         'the '
                                                                                                                         'start')],
 ("the famous surgeon's two-year list", "read the surgeon's results with your parent, and weigh the odds together"): [('lesson',
                                                                                                                       'weigh '
                                                                                                                       'the '
                                                                                                                       'odds '
                                                                                                                       'together')],
 ("the famous surgeon's two-year list", 'write to the surgeon yourself, and offer to pay privately to come sooner'): [('means',
                                                                                                                       'money-.10')],
 ("the famous surgeon's two-year list", "drive your parent to the surgeon's open day, and make sure you are both heard"): [('person',
                                                                                                                            'keeper')],
 ("the famous surgeon's two-year list", 'ask your parent what they want, and respect it if the answer is to stay home'): [('means',
                                                                                                                           'ties+.04')],
 ("the famous surgeon's two-year list", 'help your parent get as fit as they can for the operation while you wait'): [('means',
                                                                                                                       'health+.03')],
 ("the famous surgeon's two-year list", 'find a surgeon the famous one trained, nearer home and with a shorter list'): [('place',
                                                                                                                         'care.houses')],
 ("the famous surgeon's two-year list", 'ask the doctors what helps in the meantime, and try it patiently at home'): [('means',
                                                                                                                       'time-.03')],
 ("the famous surgeon's two-year list", "start a fund in your parent's name to bring the operation to the local hospital"): [('place',
                                                                                                                              'rule.voice')],
 ("the famous surgeon's two-year list", 'volunteer as a driver for patients making the long trip to that hospital'): [('means',
                                                                                                                       'time-.06')],
 ('the care home on the evening news', 'make a formal complaint to the inspectors, and give your evidence to the inquiry'): [('door',
                                                                                                                              'defied '
                                                                                                                              'an '
                                                                                                                              'authority')],
 ('the care home on the evening news', "check your parent's care records line by line, and report every false entry"): [('lesson',
                                                                                                                         'check '
                                                                                                                         'every '
                                                                                                                         'line '
                                                                                                                         'yourself')],
 ('the care home on the evening news', "join the families' claim against the owners, and hold out for a proper settlement"): [('means',
                                                                                                                               'money+.06')],
 ('the care home on the evening news', "drive there tonight, and demand to see your parent's room with your own eyes"): [('mark',
                                                                                                                          'defied '
                                                                                                                          'an '
                                                                                                                          'authority')],
 ('the care home on the evening news', 'take your parent home to live with the family, and care for them yourselves'): [('door',
                                                                                                                         'took '
                                                                                                                         'them '
                                                                                                                         'in')],
 ('the care home on the evening news', 'turn up at a different hour every day, unannounced, and see for yourself'): [('means',
                                                                                                                      'time-.06')],
 ('the care home on the evening news', 'ask your parent gently what their days there were really like, and write it down'): [('means',
                                                                                                                              'ties+.03')],
 ('the care home on the evening news', 'find the best-run home in the region, and pay the fee to move your parent there'): [('means',
                                                                                                                             'money-.10')],
 ('the care home on the evening news', "join the families' group that sits in on the new inspections"): [('place',
                                                                                                          'care.houses')],
 ('the loan the new owners call in', 'write to everyone you owe and set out an honest plan to pay each in turn'): [('door',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ('the loan the new owners call in', 'read the loan papers clause by clause, and find what the new owners can really demand'): [('lesson',
                                                                                                                                 'small '
                                                                                                                                 'print '
                                                                                                                                 'can '
                                                                                                                                 'buy '
                                                                                                                                 'time')],
 ('the loan the new owners call in', 'move the loan to a rival lender before the deadline, at a higher rate'): [('means',
                                                                                                                 'money-.06')],
 ('the loan the new owners call in', 'ask your parents for a loan, as they once asked theirs'): [('means',
                                                                                                  'money+.06')],
 ('the loan the new owners call in', 'take the good watch to the pawn shop to see the month through'): [('means',
                                                                                                         'money+.03')],
 ('the loan the new owners call in', 'sit the family down and draw up a household budget everyone keeps to'): [('means',
                                                                                                                'money+.04')],
 ('the loan the new owners call in', 'start a small trade from the spare room, planned to cover the payments'): [('place',
                                                                                                                  'comm.shop')],
 ('the loan the new owners call in', 'lend a neighbour the money to keep their shop open, on written terms'): [('door',
                                                                                                                'helped '
                                                                                                                'someone '
                                                                                                                'in '
                                                                                                                'need')],
 ('the loan the new owners call in', 'march with the other borrowers to the council to demand time to pay'): [('place',
                                                                                                               'rule.voice')],
 ('the depot at the edge of town', 'apply for a depot job through the job centre, like everyone else'): [('means',
                                                                                                          'money+.06')],
 ('the depot at the edge of town', 'work out what the town makes that could now sell far away, and tell the council'): [('lesson',
                                                                                                                         'the '
                                                                                                                         'road '
                                                                                                                         'runs '
                                                                                                                         'both '
                                                                                                                         'ways')],
 ('the depot at the edge of town', 'rent the empty plot by the slip road and open a food van for drivers'): [('place',
                                                                                                              'comm.shop')],
 ('the depot at the edge of town', 'keep the family shop on the old road open for the neighbours who still come'): [('door',
                                                                                                                     'stayed '
                                                                                                                     'home')],
 ('the depot at the edge of town', 'open the family shop late for the night shift at the depot'): [('person',
                                                                                                    'regular')],
 ('the depot at the edge of town', 'buy goods off the trucks in bulk and sell them at the weekend market'): [('place',
                                                                                                              'comm.market')],
 ('the depot at the edge of town', 'start a small delivery round linking the depot to the villages'): [('means',
                                                                                                        'money+.04')],
 ('the depot at the edge of town', 'ask the council for safe crossings on the depot road before someone is hurt'): [('place',
                                                                                                                     'rule.voice')],
 ('the market in the empty car park', 'help the market warden check the scales and give the pitches out by turn'): [('person',
                                                                                                                     'keeper')],
 ('the market in the empty car park', 'walk every row before buying, and keep a list of the best prices'): [('means',
                                                                                                             'money+.03')],
 ('the market in the empty car park', 'take a pitch of your own and sell what you make'): [('place', 'comm.market')],
 ('the market in the empty car park', 'haggle for the oldest lamp on the second-hand stall, just for the fun of it'): [('lesson',
                                                                                                                        'haggling '
                                                                                                                        'is '
                                                                                                                        'half '
                                                                                                                        'the '
                                                                                                                        'fun')],
 ('the market in the empty car park', "buy from the same growers every week and learn their children's names"): [('person',
                                                                                                                  'regular')],
 ('the market in the empty car park', 'buy at house clearances and sell at the market with a patter of your own'): [('means',
                                                                                                                     'money+.05')],
 ('the market in the empty car park', 'bring the whole family to spend Saturday morning at the market'): [('means',
                                                                                                           'ties+.03')],
 ('the market in the empty car park', "start a stall swapping seeds and cuttings from neighbours' gardens"): [('person',
                                                                                                               'neighbour')],
 ('the market in the empty car park', "help write the market's rules so that every pitch is given by turn"): [('place',
                                                                                                               'rule.counsel')],
 ('the weekly shop buys less each month', 'share out what there is fairly, and cut your own plate first'): [('means',
                                                                                                             'health-.04')],
 ('the weekly shop buys less each month', 'plan a month of meals by price, and keep to the list'): [('lesson',
                                                                                                     'a plan '
                                                                                                     'stretches '
                                                                                                     'every meal')],
 ('the weekly shop buys less each month', 'buy dried goods in bulk now, before the next rise'): [('means',
                                                                                                  'money+.04')],
 ('the weekly shop buys less each month', 'haggle at the market at closing time for whatever the stalls have left'): [('place',
                                                                                                                       'comm.market')],
 ('the weekly shop buys less each month', 'run a tab at the corner shop whose owner has known your family for years'): [('person',
                                                                                                                         'keeper')],
 ('the weekly shop buys less each month', 'sell the good bicycle to keep the cupboards full until spring'): [('means',
                                                                                                              'money+.03')],
 ('the weekly shop buys less each month', 'cook one big pot each Sunday with the neighbours, everyone bringing what they can'): [('place',
                                                                                                                                  'gather.house')],
 ('the weekly shop buys less each month', "compare every shop's prices and buy each thing where it is cheapest"): [('means',
                                                                                                                    'money+.03')],
 ('the weekly shop buys less each month', 'join the neighbours demanding that the council cap the price of bread'): [('place',
                                                                                                                      'rule.voice')],
 ('the shop that tripled the price of water', 'report the price to the council and ask for a cap on water'): [('lesson',
                                                                                                               'a '
                                                                                                               'fair '
                                                                                                               'complaint '
                                                                                                               'gets '
                                                                                                               'heard')],
 ('the shop that tripled the price of water', 'find out what the shop paid for the water, and post the figures for the street'): [('lesson',
                                                                                                                                   'the '
                                                                                                                                   'figures '
                                                                                                                                   'speak '
                                                                                                                                   'for '
                                                                                                                                   'themselves')],
 ('the shop that tripled the price of water', 'fetch water by the pallet from the next town, and sell it at a fair margin'): [('means',
                                                                                                                               'money+.06')],
 ('the shop that tripled the price of water', 'join the picket at the door and lead the chanting'): [('person',
                                                                                                      'rival')],
 ('the shop that tripled the price of water', 'sell cheap water by the picket from the boot of your car'): [('means',
                                                                                                             'money+.03')],
 ('the shop that tripled the price of water', 'quietly ask the owner to drop the price before the council does it for him'): [('person',
                                                                                                                               'friend')],
 ('the shop that tripled the price of water', 'get the street collecting rainwater and sharing it house by house'): [('person',
                                                                                                                      'neighbour')],
 ('the shop that tripled the price of water', 'stand between the owner and the crowd and ask both sides to calm down'): [('mark',
                                                                                                                          'took '
                                                                                                                          'a '
                                                                                                                          'wild '
                                                                                                                          'risk')],
 ('the shop that tripled the price of water', 'lead a boycott of the shop until the price comes down'): [('place',
                                                                                                          'rule.voice')],
 ('the letter that writes off the debt', "put the freed money aside each month until there is a year's cushion"): [('means',
                                                                                                                    'money+.08')],
 ('the letter that writes off the debt', 'borrow on the clean record to buy the van the business needs'): [('means',
                                                                                                            'money-.05')],
 ('the letter that writes off the debt', 'throw a party for everyone who helped you through the debt years'): [('means',
                                                                                                                'ties+.05')],
 ('the letter that writes off the debt', 'take the family away on the first holiday in six years'): [('means',
                                                                                                      'money-.04')],
 ('the letter that writes off the debt', 'read the new law closely and find which of your other debts it caps'): [('means',
                                                                                                                   'money+.04')],
 ('the letter that writes off the debt', 'set up a small fund at work that lends colleagues money without interest'): [('place',
                                                                                                                        'comm.credit')],
 ('the letter that writes off the debt', 'volunteer at the advice centre, helping neighbours read their own letters'): [('mark',
                                                                                                                         'helped '
                                                                                                                         'someone '
                                                                                                                         'in '
                                                                                                                         'need')],
 ('a ten-year wait for a permit', 'put your name on the waiting list and sell only where no permit is needed'): [('means',
                                                                                                                  'money-.05')],
 ('a ten-year wait for a permit', 'read the new rule closely and find the pitches it does not cover'): [('lesson',
                                                                                                         'every rule '
                                                                                                         'has its '
                                                                                                         'edges')],
 ('a ten-year wait for a permit', 'rent a spare permit from an old holder, at whatever price they ask'): [('means',
                                                                                                           'money-.08')],
 ('a ten-year wait for a permit', 'keep selling on the corner, and pack up fast when the inspectors come'): [('mark',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ('a ten-year wait for a permit', "move the stall to the family's front yard, where the neighbours can find it"): [('person',
                                                                                                                    'neighbour')],
 ('a ten-year wait for a permit', 'go into partnership with a cousin who holds a permit, and share the takings'): [('person',
                                                                                                                    'colleague')],
 ('a ten-year wait for a permit', 'pay a shopkeeper for the use of their doorway, which the rule allows'): [('person',
                                                                                                             'keeper')],
 ('a ten-year wait for a permit', "gather the old vendors' records to prove the stalls were here long before the rule"): [('place',
                                                                                                                           'learn.keeping')],
 ('a ten-year wait for a permit', 'march with the vendors on the city hall to open the permit rolls'): [('place',
                                                                                                         'rule.voice')],
 ('a ten-year wait for a permit', 'draft a scheme that gives permits out by turn, and take it to the council'): [('place',
                                                                                                                  'rule.counsel')],
 ('the man with the van at the market', 'report the van to the inspectors, with the days and times it parks'): [('person',
                                                                                                                 'rival')],
 ('the man with the van at the market', 'turn the driving down, since the sums show far more risk than pay'): [('lesson',
                                                                                                                'some '
                                                                                                                'pay '
                                                                                                                'costs '
                                                                                                                'too '
                                                                                                                'much')],
 ('the man with the van at the market', 'buy a few cartons and sell them on to colleagues at a margin'): [('means',
                                                                                                           'money+.03')],
 ('the man with the van at the market', "buy your parent's usual cartons from the van, as the whole street does"): [('means',
                                                                                                                     'money+.03')],
 ('the man with the van at the market', "strike a deal to sell the man's cartons from your own stall, for a share"): [('means',
                                                                                                                       'money+.06')],
 ('the man with the van at the market', 'help your parent cut down slowly, now that the habit costs so much'): [('mark',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('the man with the van at the market', 'write a sharp piece for the local news on why the van does such good trade'): [('lesson',
                                                                                                                         'the '
                                                                                                                         'trade '
                                                                                                                         'follows '
                                                                                                                         'the '
                                                                                                                         'price')],
 ('the man with the van at the market', 'lend the corner shopkeeper the money to ride out the trade the van has taken'): [('person',
                                                                                                                           'keeper')],
 ('the man with the van at the market', 'ask the street to buy from the corner shop, whose owner pays the tax'): [('place',
                                                                                                                   'comm.shop')],
 ("the investment club's phone goes dead", 'take your papers to the police and give a full statement'): [('lesson',
                                                                                                          'the '
                                                                                                          'papers '
                                                                                                          'are your '
                                                                                                          'proof')],
 ("the investment club's phone goes dead", "gather every member's statements and work out where the money went"): [('means',
                                                                                                                    'time-.05')],
 ("the investment club's phone goes dead", "hire a lawyer to claim the founder's house before the others do"): [('means',
                                                                                                                 'money-.06')],
 ("the investment club's phone goes dead", 'tell your parent they were right all along, and ask for their help'): [('lesson',
                                                                                                                    'pride '
                                                                                                                    'is '
                                                                                                                    'worth '
                                                                                                                    'less '
                                                                                                                    'than '
                                                                                                                    'help')],
 ("the investment club's phone goes dead", 'bring the members together for a meal, so nobody faces it alone'): [('place',
                                                                                                                 'gather.talk')],
 ("the investment club's phone goes dead", "start a page that warns others about schemes that pay from newcomers' money"): [('place',
                                                                                                                             'arts.page')],
 ("the investment club's phone goes dead", "lead the members' group that pursues the founder through the courts"): [('person',
                                                                                                                     'rival')],
 ("the investment club's phone goes dead", "write to the regulator asking for rules on clubs that take people's savings"): [('place',
                                                                                                                             'rule.voice')],
 ('a second flat with almost nothing down', 'borrow only what one wage can repay, whatever the lender offers'): [('lesson',
                                                                                                                  'borrow '
                                                                                                                  'what '
                                                                                                                  'you '
                                                                                                                  'can '
                                                                                                                  'repay')],
 ('a second flat with almost nothing down', 'stay out, since the rents no longer cover the prices, and say so'): [('means',
                                                                                                                   'money+.04')],
 ('a second flat with almost nothing down', 'buy a second flat with almost nothing down, and let it out'): [('means',
                                                                                                             'money+.08')],
 ('a second flat with almost nothing down', 'stay in the rented flat near the family, and call it home'): [('door',
                                                                                                            'stayed '
                                                                                                            'home')],
 ('a second flat with almost nothing down', 'go in with your friends on a flat by the sea for all to share'): [('place',
                                                                                                                'gather.house')],
 ('a second flat with almost nothing down', 'sell your flat while the market is at its top, and rent for a while'): [('means',
                                                                                                                      'money+.06')],
 ('a second flat with almost nothing down', 'help your parents work out whether to sell the family house or keep it'): [('lesson',
                                                                                                                         'a '
                                                                                                                         'home '
                                                                                                                         'is '
                                                                                                                         'more '
                                                                                                                         'than '
                                                                                                                         'money')],
 ('a second flat with almost nothing down', 'lend your younger brother or sister the deposit, on written terms'): [('means',
                                                                                                                    'money-.06')],
 ('a second flat with almost nothing down', 'join the campaign for homes a person on one wage can afford'): [('place',
                                                                                                              'rule.voice')],
 ('money that buys less every month', 'press your boss, with the others at work, for wages that keep up with prices'): [('person',
                                                                                                                         'colleague')],
 ('money that buys less every month', 'move the savings, carefully, into goods that keep their worth'): [('means',
                                                                                                          'money+.05')],
 ('money that buys less every month', 'buy the car now on a fixed loan, and let the rising prices shrink the debt'): [('means',
                                                                                                                       'freedom+.05')],
 ('money that buys less every month', 'spend each wage the day it comes, on what the month needs'): [('lesson',
                                                                                                      'spend it '
                                                                                                      'before it '
                                                                                                      'shrinks')],
 ('money that buys less every month', 'swap work and goods with the neighbours instead of using money'): [('person',
                                                                                                           'neighbour')],
 ('money that buys less every month', "keep the family's savings in rings and tools rather than in money"): [('means',
                                                                                                              'money+.03')],
 ('money that buys less every month', 'trade goods between shops that price them differently from week to week'): [('place',
                                                                                                                    'comm.market')],
 ('money that buys less every month', 'march with the pensioners demanding that their payments rise with prices'): [('place',
                                                                                                                     'rule.voice')],
 ("your turn at the savings circle's pot", 'ask the circle to agree one rule for late payers, and keep it for everyone'): [('lesson',
                                                                                                                            'the '
                                                                                                                            'same '
                                                                                                                            'rule '
                                                                                                                            'for '
                                                                                                                            'everyone')],
 ("your turn at the savings circle's pot", "spend the pot on a freezer sized to last season's sales"): [('means',
                                                                                                         'money+.03')],
 ("your turn at the savings circle's pot", 'use the pot as the deposit on a second stall'): [('means', 'money+.06')],
 ("your turn at the savings circle's pot", 'buy the awning you have wanted for years, and the string of lights too'): [('means',
                                                                                                                        'money-.03')],
 ("your turn at the savings circle's pot", 'take the pot early in return for paying in a little more each month'): [('means',
                                                                                                                     'money-.04')],
 ("your turn at the savings circle's pot", 'throw a supper for the whole circle when the pot is paid out'): [('means',
                                                                                                              'ties+.04')],
 ("your turn at the savings circle's pot", "offer to keep the circle's book, and know who owes what"): [('place',
                                                                                                         'comm.credit')],
 ("your turn at the savings circle's pot", 'ask the circle to give your friend time, and share the gap in turns'): [('mark',
                                                                                                                     'helped '
                                                                                                                     'someone '
                                                                                                                     'in '
                                                                                                                     'need')],
 ("your turn at the savings circle's pot", "write the circle's rules down, so a new member knows them from the first day"): [('lesson',
                                                                                                                              'a '
                                                                                                                              'rule '
                                                                                                                              'on '
                                                                                                                              'paper '
                                                                                                                              'outlasts '
                                                                                                                              'memory')],
 ('the first bank branch in the village', 'open a savings account and pay in the same sum every week'): [('means',
                                                                                                          'money+.04')],
 ('the first bank branch in the village', "compare the three lenders' terms line by line before signing anything"): [('lesson',
                                                                                                                      'read '
                                                                                                                      'the '
                                                                                                                      'terms '
                                                                                                                      'before '
                                                                                                                      'signing')],
 ('the first bank branch in the village', 'borrow for the machine that does the work of three hands'): [('means',
                                                                                                         'time+.06')],
 ('the first bank branch in the village', 'take the loan while it is offered, and start the business you always talked about'): [('mark',
                                                                                                                                  'took '
                                                                                                                                  'a '
                                                                                                                                  'wild '
                                                                                                                                  'risk')],
 ('the first bank branch in the village', "keep saving with the neighbours' circle, as the family always has"): [('means',
                                                                                                                  'ties+.03')],
 ('the first bank branch in the village', 'borrow for a stall at the summer fairs, and take the family along'): [('place',
                                                                                                                  'comm.market')],
 ('the first bank branch in the village', "apply for the clerk's post at the new branch"): [('place', 'comm.credit')],
 ('the first bank branch in the village', 'borrow a little to try a new crop, planned to be paid off in two seasons'): [('means',
                                                                                                                         'money-.03')],
 ('the first bank branch in the village', 'stand guarantor for a neighbour the bank would not lend to alone'): [('door',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('the first bank branch in the village', 'help your grandparent open a first account, and show them how it works'): [('mark',
                                                                                                                       'helped '
                                                                                                                       'someone '
                                                                                                                       'in '
                                                                                                                       'need')],
 ('the superstore on the ring road', 'take a job on the tills, with its written wage and fixed hours'): [('means',
                                                                                                          'money+.05')],
 ('the superstore on the ring road', 'shop at both, buying each thing where it is cheaper'): [('means', 'money+.03')],
 ('the superstore on the ring road', "apply for the supervisor's post and aim for the manager's office"): [('person',
                                                                                                            'rival')],
 ('the superstore on the ring road', 'do the big weekly shop at the superstore and enjoy every aisle'): [('lesson',
                                                                                                          'plenty '
                                                                                                          'has its '
                                                                                                          'own '
                                                                                                          'pleasure')],
 ('the superstore on the ring road', 'keep buying from the grocer, even when it costs more'): [('person', 'keeper')],
 ('the superstore on the ring road', 'take the superstore job, and still buy the Sunday meat from the butcher'): [('person',
                                                                                                                   'colleague')],
 ('the superstore on the ring road', 'open a stall outside the superstore selling what it does not stock'): [('means',
                                                                                                              'money+.04')],
 ('the superstore on the ring road', "help the town's small shops set up one shared delivery round"): [('place',
                                                                                                        'comm.shop')],
 ('the superstore on the ring road', "organise a market day for the town's small shops on the old square"): [('place',
                                                                                                              'comm.market')],
 ('the superstore on the ring road', 'ask the council to hold the superstore to its promise of local jobs'): [('place',
                                                                                                               'rule.voice')],
 ('the part that will not come', "wait your turn on the garage's list, and take the bus meanwhile"): [('means',
                                                                                                       'time-.06')],
 ('the part that will not come', 'search the scrapyards for the same model with the part still in it'): [('lesson',
                                                                                                          'every '
                                                                                                          'scrapyard '
                                                                                                          'hides a '
                                                                                                          'spare')],
 ('the part that will not come', 'pay the dealer three times the price and be driving by Friday'): [('means',
                                                                                                     'money-.06')],
 ('the part that will not come', 'ask your friend for a lift each morning, and fill their tank on Fridays'): [('means',
                                                                                                               'money-.03')],
 ('the part that will not come', "borrow your parent's old car, and keep it running for them in return"): [('door',
                                                                                                            'kept '
                                                                                                            'your '
                                                                                                            'word')],
 ('the part that will not come', 'cycle to work with a group from the street'): [('place', 'gather.circle')],
 ('the part that will not come', 'find out who is hoarding parts, and buy a share of their stock'): [('means',
                                                                                                      'money+.05')],
 ('the part that will not come', "join the drivers who want the garage's list made public, so nobody jumps it"): [('place',
                                                                                                                   'rule.voice')],
 ('the part that will not come', 'ask your boss in writing for hours that fit the bus timetable'): [('means',
                                                                                                     'time+.03')],
 ("the gift book at a cousin's wedding", 'give the sum the family agreed every guest would give'): [('means',
                                                                                                     'money-.03')],
 ("the gift book at a cousin's wedding", "look up what the cousin's family gave last time, and match it exactly"): [('lesson',
                                                                                                                     'every '
                                                                                                                     'gift '
                                                                                                                     'is '
                                                                                                                     'remembered')],
 ("the gift book at a cousin's wedding", 'give the largest envelope of the evening, and let it be noticed'): [('means',
                                                                                                               'money-.08')],
 ("the gift book at a cousin's wedding", "give a month's wages, because the day deserves it"): [('means',
                                                                                                 'money-.10')],
 ("the gift book at a cousin's wedding", "give what your parents' families gave each other forty years ago, and a little more"): [('means',
                                                                                                                                   'ties+.03')],
 ("the gift book at a cousin's wedding", 'hire the band as your gift, and make the dancing the talk of the night'): [('means',
                                                                                                                      'money-.05')],
 ("the gift book at a cousin's wedding", 'give the couple a share in a savings fund instead of cash, a gift that grows'): [('means',
                                                                                                                            'money-.04')],
 ("the gift book at a cousin's wedding", 'help the aunt keep the gift book, and learn who owes whom'): [('person',
                                                                                                         'mentor')],
 ("the gift book at a cousin's wedding", 'suggest the family stop counting envelopes, and let each guest give what they can'): [('mark',
                                                                                                                                 'defied '
                                                                                                                                 'an '
                                                                                                                                 'authority')],
 ('new shops on the empty high street', "speak up for the new shops at the residents' meeting when others complain"): [('place',
                                                                                                                        'rule.voice')],
 ('new shops on the empty high street', 'rent your empty unit to one of the new families, on a fair lease'): [('means',
                                                                                                               'money+.06')],
 ('new shops on the empty high street', "try one of everything on the new bakery's counter"): [('place',
                                                                                                'comm.shop')],
 ('new shops on the empty high street', 'keep buying from the old shops that are left, while they last'): [('person',
                                                                                                            'keeper')],
 ('new shops on the empty high street', "answer the card in the window and work behind the new grocer's counter"): [('person',
                                                                                                                     'boss')],
 ('new shops on the empty high street', 'lend a new family the money for their shop fittings, on written terms'): [('door',
                                                                                                                    'helped '
                                                                                                                    'someone '
                                                                                                                    'in '
                                                                                                                    'need')],
 ('the stall that takes payment by phone', "insist that the bakery serve your grandparent for cash, as the market's rules say"): [('lesson',
                                                                                                                                   'the '
                                                                                                                                   'rules '
                                                                                                                                   'are '
                                                                                                                                   'on '
                                                                                                                                   'your '
                                                                                                                                   'side')],
 ('the stall that takes payment by phone', 'learn the new way to pay properly, and teach it to your grandparent'): [('mark',
                                                                                                                     'learned '
                                                                                                                     'a '
                                                                                                                     'skill')],
 ('the stall that takes payment by phone', 'set your own stall up to take phone payments before the others do'): [('means',
                                                                                                                   'money+.04')],
 ('the stall that takes payment by phone', 'pay for everything by phone, and leave the purse at home'): [('lesson',
                                                                                                          'new ways '
                                                                                                          'can be '
                                                                                                          'easy')],
 ('the stall that takes payment by phone', 'go to the market with your grandparent, and pay for them in cash'): [('means',
                                                                                                                  'time-.04')],
 ('the stall that takes payment by phone', 'keep a jar of change for the old regulars, and take phones from everyone else'): [('person',
                                                                                                                               'regular')],
 ('the stall that takes payment by phone', 'set up a phone account for your grandparent, and check it with them each week'): [('mark',
                                                                                                                               'helped '
                                                                                                                               'someone '
                                                                                                                               'in '
                                                                                                                               'need')],
 ('the stall that takes payment by phone', 'make a simple card that lets the old regulars pay without a phone'): [('place',
                                                                                                                   'comm.credit')],
 ('the stall that takes payment by phone', 'lend the old stallholder next door the money for a payment reader'): [('door',
                                                                                                                   'helped '
                                                                                                                   'someone '
                                                                                                                   'in '
                                                                                                                   'need')],
 ('the stall that takes payment by phone', 'start a petition to keep cash at the market, and gather names among the old regulars'): [('place',
                                                                                                                                      'rule.voice')],
 ('the rent goes up by a fifth', 'pay the new rent, and cut the household budget to match it'): [('means',
                                                                                                  'money-.06')],
 ('the rent goes up by a fifth', 'show the landlord what similar flats rent for, and offer a smaller rise'): [('lesson',
                                                                                                               'a '
                                                                                                               'fair '
                                                                                                               'figure '
                                                                                                               'opens '
                                                                                                               'talks')],
 ('the rent goes up by a fifth', 'find a flat in a cheaper street with a longer lease, before the rise begins'): [('means',
                                                                                                                   'money+.04')],
 ('the rent goes up by a fifth', 'move in with your parents for a year to save'): [('mark', 'came home')],
 ('the rent goes up by a fifth', 'take a lodger in the spare room to cover the rise'): [('means', 'money+.05')],
 ('the rent goes up by a fifth', "share a bigger house with your brother or sister's family, and split the rent"): [('means',
                                                                                                                     'ties+.05')],
 ('the rent goes up by a fifth', 'rent a cheaper flat far out and work from home three days a week'): [('means',
                                                                                                        'freedom+.04')],
 ('the rent goes up by a fifth', "lead the street's tenants in bargaining with the landlord together"): [('place',
                                                                                                          'rule.voice')],
 ('the rent goes up by a fifth', 'join the tenants who refuse the rise, and stand with the neighbours'): [('person',
                                                                                                           'neighbour')],
 ('the job centre in the old bank', 'take a numbered place in the queue and apply for the posts in order'): [('lesson',
                                                                                                              'your '
                                                                                                              'turn '
                                                                                                              'does '
                                                                                                              'come')],
 ('the job centre in the old bank', 'hold out for the post that pays what you are worth'): [('means', 'money-.04')],
 ('the job centre in the old bank', "take the first day's shift going, and see where it leads"): [('means',
                                                                                                   'money+.03')],
 ('the job centre in the old bank', 'let your cousin vouch for you at his firm'): [('person', 'boss')],
 ('the job centre in the old bank', 'sign with the agency that places whole crews, at a rate you name'): [('means',
                                                                                                           'money+.05')],
 ('the job centre in the old bank', 'take a job on the same crew as your friends, wherever it is'): [('means',
                                                                                                      'ties+.04')],
 ('the job centre in the old bank', 'ask the adviser which firms are short of hands, and apply there first'): [('person',
                                                                                                                'go-between')],
 ('the job centre in the old bank', 'volunteer on Saturdays to help the adviser match people to posts'): [('means',
                                                                                                           'time-.04')],
 ("the young one's rite of passage", "go over the rite's words with the young one each evening until they are sure"): [('means',
                                                                                                                        'time-.04')],
 ("the young one's rite of passage", 'explain to the young one what each part of the rite means, and why'): [('lesson',
                                                                                                              'children '
                                                                                                              'ask '
                                                                                                              'the '
                                                                                                              'real '
                                                                                                              'questions')],
 ("the young one's rite of passage", 'throw the biggest party the street has seen, and invite the people who matter'): [('person',
                                                                                                                         'patron')],
 ("the young one's rite of passage", 'stand up at the party and give a speech that has the whole room in tears'): [('means',
                                                                                                                    'ties+.03')],
 ("the young one's rite of passage", 'bring out the old family keepsake, and pass it on at the end of the rite'): [('lesson',
                                                                                                                    'keepsakes '
                                                                                                                    'are '
                                                                                                                    'meant '
                                                                                                                    'to '
                                                                                                                    'travel')],
 ("the young one's rite of passage", "spend beyond the family's means, so the family is not outdone"): [('means',
                                                                                                         'money-.10')],
 ("the young one's rite of passage", 'take the young one and friends out for a night under the sky, as of old'): [('means',
                                                                                                                   'ties+.03')],
 ("the young one's rite of passage", 'ask a respected elder to take the young one under their wing from now on'): [('person',
                                                                                                                    'elder')],
 ("the young one's rite of passage", 'gather every relative under one roof for the day, even the ones who stopped speaking'): [('means',
                                                                                                                                'ties+.06')],
 ("the young one's rite of passage", 'sit in on the class before the rite, and help the teacher with the nervous ones'): [('place',
                                                                                                                           'faith.congregation')],
 ('the old walking road is full again', 'walk with a notebook, and ask each pilgrim why they came'): [('lesson',
                                                                                                       'everyone '
                                                                                                       'walks for a '
                                                                                                       'reason')],
 ('the old walking road is full again', 'go as a paid guide for a group of first-timers'): [('means', 'money+.04')],
 ('the old walking road is full again', 'carry a stone from the family graves and leave it at the shrine'): [('lesson',
                                                                                                              'the '
                                                                                                              'dead '
                                                                                                              'travel '
                                                                                                              'with '
                                                                                                              'us')],
 ('the old walking road is full again', 'sell cold drinks and blister plasters at the steepest bend of the road'): [('means',
                                                                                                                     'money+.05')],
 ('the old walking road is full again', 'walk the last stretch barefoot, the way the old pilgrims did'): [('means',
                                                                                                           'health-.03')],
 ('the old walking road is full again', "fall in beside an old pilgrim and learn the road's stories as you walk"): [('person',
                                                                                                                     'mentor')],
 ('the old walking road is full again', "help run the pilgrims' hostel for the season, and keep its books straight"): [('place',
                                                                                                                        'faith.shrines')],
 ('the building fund is gone', "stand up at the members' meeting and ask the leader to step down"): [('mark',
                                                                                                      'defied an '
                                                                                                      'authority')],
 ('the building fund is gone', 'ask to see the accounts, and go through them line by line'): [('lesson',
                                                                                               'read the books '
                                                                                               'yourself')],
 ('the building fund is gone', 'put your name forward for the board while the old one falls'): [('place',
                                                                                                 'rule.counsel')],
 ('the building fund is gone', 'keep coming on the holy days, for the sake of the old hall'): [('lesson',
                                                                                                'the hall outlasts '
                                                                                                'its leaders')],
 ('the building fund is gone', 'quietly move the family to another house of worship across town'): [('place',
                                                                                                     'faith.congregation')],
 ('the building fund is gone', 'stop going, and spend the rest day with the family instead'): [('means', 'time+.04')],
 ('the building fund is gone', 'push for an outside auditor and new rules on every fund'): [('door',
                                                                                             'made an enemy')],
 ('the building fund is gone', 'help draw up a fair plan to pay the givers back'): [('mark',
                                                                                     'helped someone in need')],
 ('a box of books from next door', 'hand the box to the authorities, and keep your own record clean'): [('person',
                                                                                                         'neighbour '
                                                                                                         'lost')],
 ('a box of books from next door', "write up the family's story without names, and send it to the papers"): [('door',
                                                                                                              'defied '
                                                                                                              'an '
                                                                                                              'authority')],
 ('a box of books from next door', 'ask a friend in the council office how the family can appeal'): [('person',
                                                                                                      'go-between')],
 ('the leaders of every faith share a meal', 'invite a family of another faith to share your holy day meal'): [('person',
                                                                                                                'friend')],
 ('the leaders of every faith share a meal', "join a circle that reads each faith's teachings together, one evening a month"): [('place',
                                                                                                                                 'faith.seeking')],
 ('the leaders of every faith share a meal', "open your shop on every faith's feast days, with something for each"): [('means',
                                                                                                                       'money+.04')],
 ('the leaders of every faith share a meal', 'go to every feast in town this year, whoever is hosting'): [('means',
                                                                                                           'ties+.05')],
 ('the leaders of every faith share a meal', 'keep your own feasts as always, and greet the others warmly in the street'): [('person',
                                                                                                                             'neighbour')],
 ('the leaders of every faith share a meal', 'broker a deal for the faiths to share the empty hall on different days'): [('lesson',
                                                                                                                          'empty '
                                                                                                                          'rooms '
                                                                                                                          'can '
                                                                                                                          'be '
                                                                                                                          'shared')],
 ('the leaders of every faith share a meal', 'write to the paper about the shared meal, and ask for another next year'): [('lesson',
                                                                                                                           'one '
                                                                                                                           'letter '
                                                                                                                           'can '
                                                                                                                           'start '
                                                                                                                           'something')],
 ('the leaders of every faith share a meal', "ask the council to put every faith's holy days in the town calendar"): [('place',
                                                                                                                       'rule.voice')],
 ('the leaders of every faith share a meal', 'help cook for a feast that the two faiths of the street share'): [('means',
                                                                                                                 'ties+.04')],
 ('a face in the window', 'ask the elders to keep the crowds orderly and the claims modest'): [('person', 'elder')],
 ('a face in the window', 'look into what the window really shows before believing or scoffing'): [('lesson',
                                                                                                    'some things '
                                                                                                    'stay '
                                                                                                    'unexplained')],
 ('a face in the window', 'rent out your driveway to the visitors by the hour'): [('means', 'money+.04')],
 ('a face in the window', 'join the crowd at the window and sing with them until late'): [('place', 'gather.great')],
 ('a face in the window', 'go with your grandparent each evening, and light a candle beside them'): [('place',
                                                                                                      'faith.shrines')],
 ('a face in the window', 'trust what your heart says about it, and say so to anyone who asks'): [('lesson',
                                                                                                   'say what you '
                                                                                                   'truly think')],
 ('a face in the window', 'sell your sharpest photographs of the window to the papers'): [('means', 'money+.05')],
 ('a face in the window', 'say nothing against the healing, and simply keep your grandparent company'): [('means',
                                                                                                          'time-.03')],
 ('a face in the window', 'help the council set up parking and first aid for the crowds'): [('place', 'prot.rescue')],
 ('a face in the window', 'warn the crowd not to give up their medicine on the strength of a story'): [('mark',
                                                                                                        'helped '
                                                                                                        'someone in '
                                                                                                        'need')],
 ('ten people at the graveside', 'give up your own place so an older relative can be there'): [('mark',
                                                                                                'helped someone in '
                                                                                                'need')],
 ('ten people at the graveside', 'write a eulogy, and send it to every relative who cannot come'): [('means',
                                                                                                     'ties+.04')],
 ('ten people at the graveside', 'stand outside the gate in the rain, as close as the rules allow'): [('means',
                                                                                                       'health-.03')],
 ('ten people at the graveside', 'promise the family a proper second rite when the rules lift'): [('door',
                                                                                                   'kept your word')],
 ('ten people at the graveside', 'pay for a stone and a gathering later that no one will forget'): [('means',
                                                                                                     'money-.08')],
 ('ten people at the graveside', 'slip into the back of the hall, and break the rule to be there'): [('mark',
                                                                                                      'defied an '
                                                                                                      'authority')],
 ('ten people at the graveside', 'gather the cousins online that night to tell stories of the dead until late'): [('means',
                                                                                                                   'ties+.05')],
 ('ten people at the graveside', 'keep the old mourning days at home, with a candle and an empty chair'): [('lesson',
                                                                                                            'grief '
                                                                                                            'needs '
                                                                                                            'somewhere '
                                                                                                            'to go')],
 ('ten people at the graveside', "ask the faith's leaders for a short rite that families can hold at home"): [('place',
                                                                                                               'faith.congregation')],
 ('the new house of worship opens', "take charge of the new building's cleaning and repairs rota"): [('means',
                                                                                                      'time-.05')],
 ('the new house of worship opens', 'start a weekday class in one of the new rooms'): [('place',
                                                                                        'faith.congregation')],
 ('the new house of worship opens', 'pay for a room and have it named for your family'): [('means', 'money-.10')],
 ('the new house of worship opens', 'help put on a first-night concert for the whole town'): [('place', 'arts.song')],
 ('the new house of worship opens', "carry the family's old bench in from the old building"): [('lesson',
                                                                                                'old things belong '
                                                                                                'in new rooms')],
 ('the new house of worship opens', "buy a carved stone with your parents' names for the front wall"): [('means',
                                                                                                         'money-.06')],
 ('the new house of worship opens', 'sit on the committee that decides who may use the rooms'): [('place',
                                                                                                  'rule.counsel')],
 ('the new house of worship opens', 'paint a mural in the hallway with the children of the congregation'): [('place',
                                                                                                             'arts.craft')],
 ('the new house of worship opens', 'cook for everyone on the opening day, the way it was done at the old hall'): [('means',
                                                                                                                    'ties+.04')],
 ('the new house of worship opens', 'lead the procession from the old building to the new one'): [('place',
                                                                                                   'gather.great')],
 ('none of your friends go any more', "go back once a month, for your parent's sake"): [('place',
                                                                                         'faith.congregation')],
 ('none of your friends go any more', 'read the teachings again as a grown-up, and see what still stands'): [('lesson',
                                                                                                              'some '
                                                                                                              'of it '
                                                                                                              'still '
                                                                                                              'holds')],
 ('none of your friends go any more', 'tell your parent, kindly, that you have stopped believing'): [('means',
                                                                                                      'freedom+.04')],
 ('none of your friends go any more', 'keep the home rites, and let the house of worship go'): [('lesson',
                                                                                                 'the rites can live '
                                                                                                 'at home')],
 ('none of your friends go any more', 'come only at the holidays, and keep the peace at home'): [('door',
                                                                                                  'gave in to '
                                                                                                  'pressure')],
 ('none of your friends go any more', 'spend the rest days as you please, and stop explaining yourself'): [('means',
                                                                                                            'time+.05')],
 ('none of your friends go any more', 'ask your parent what the faith gave them, and really listen'): [('means',
                                                                                                        'ties+.04')],
 ('none of your friends go any more', 'bring your friends along to a holiday service, for the music and the food'): [('means',
                                                                                                                      'ties+.03')],
 ('none of your friends go any more', 'look for a quieter house of worship where questions are welcome'): [('place',
                                                                                                            'faith.seeking')],
 ('the fast ends and the table fills', 'say the blessing for the meal, and name the dead in it'): [('lesson',
                                                                                                    'naming the dead '
                                                                                                    'keeps them '
                                                                                                    'near')],
 ('the fast ends and the table fills', 'ask the oldest at the table what the fast was first for'): [('person',
                                                                                                     'elder')],
 ('the fast ends and the table fills', 'use the meal to patch up a quarrel that has been costing you'): [('means',
                                                                                                          'ties+.05')],
 ('the fast ends and the table fills', 'get everyone singing the old songs before the dishes are cleared'): [('means',
                                                                                                              'ties+.03')],
 ('the fast ends and the table fills', 'set a plate at the empty chair, the way the old families did'): [('lesson',
                                                                                                          'an empty '
                                                                                                          'chair '
                                                                                                          'still '
                                                                                                          'counts')],
 ('the fast ends and the table fills', 'stay out late with old friends from town, and skip the second day'): [('means',
                                                                                                               'freedom+.03')],
 ('the fast ends and the table fills', 'tell the funniest stories of the dead until the whole table laughs'): [('means',
                                                                                                                'ties+.04')],
 ('the fast ends and the table fills', 'sit beside the newcomer and find out who they really are'): [('person',
                                                                                                      'friend')],
 ('the fast ends and the table fills', 'draw up who cooks what next year, so no one carries the feast alone'): [('means',
                                                                                                                 'time+.03')],
 ('a call to serve after a loss', 'start the training, and give the next years to those who grieve'): [('place',
                                                                                                        'faith.orders')],
 ('a call to serve after a loss', "train, and aim to lead the faith's counselling work in the district one day"): [('place',
                                                                                                                    'faith.orders')],
 ('a call to serve after a loss', "ask your family's blessing before taking a single step"): [('means', 'ties+.03')],
 ('a call to serve after a loss', 'train, but keep the rest of your life exactly your own'): [('means', 'time-.04')],
 ('a call to serve after a loss', 'sit with the dying on the ward as a volunteer for a year, then decide'): [('place',
                                                                                                              'care.houses')],
 ('a call to serve after a loss', 'keep a journal of the call, and talk it through with a teacher you trust'): [('person',
                                                                                                                 'teacher')],
 ('a call to serve after a loss', 'set out a plan with your partner: savings, hours and a date to look again'): [('lesson',
                                                                                                                  'a '
                                                                                                                  'plan '
                                                                                                                  'makes '
                                                                                                                  'room '
                                                                                                                  'for '
                                                                                                                  'callings')],
 ('a call to serve after a loss', 'turn the training down for now, and serve the grieving in your own street'): [('mark',
                                                                                                                  'helped '
                                                                                                                  'someone '
                                                                                                                  'in '
                                                                                                                  'need')],
 ('the hill of offerings is cleared', 'ask the council to check whether the permits were granted properly'): [('place',
                                                                                                               'rule.counsel')],
 ('the hill of offerings is cleared', 'dig through the records to find out who sold the hill, and how'): [('place',
                                                                                                           'learn.keeping')],
 ('the hill of offerings is cleared', "take the builders' day wages while the work lasts"): [('means', 'money+.05')],
 ('the hill of offerings is cleared', 'join the camp at the gate, and stay as long as it holds'): [('place',
                                                                                                    'rule.voice')],
 ('the hill of offerings is cleared', 'go up the hill one last time with your grandparent before it is gone'): [('lesson',
                                                                                                                 'say '
                                                                                                                 'goodbye '
                                                                                                                 'while '
                                                                                                                 'you '
                                                                                                                 'can')],
 ('the hill of offerings is cleared', 'sell hot food to the camp and the builders alike'): [('means', 'money+.04')],
 ('the hill of offerings is cleared', 'press the developer to spare the oldest trees in return for a quiet site'): [('door',
                                                                                                                     'kept '
                                                                                                                     'your '
                                                                                                                     'word')],
 ('the hill of offerings is cleared', 'take cuttings from the old trees to plant on another hill'): [('place',
                                                                                                      'faith.shrines')],
 ('the hill of offerings is cleared', 'help the old families gather the offerings before the machines reach them'): [('means',
                                                                                                                      'ties+.04')],
 ('the food bank opens five days a week', 'sign up for two shifts a week on the food bank rota'): [('place',
                                                                                                    'faith.congregation')],
 ('the food bank opens five days a week', 'find out who in town is going hungry and why, and tell the council'): [('place',
                                                                                                                   'rule.voice')],
 ('the food bank opens five days a week', 'take a parcel home for your own family, and let pride wait'): [('means',
                                                                                                           'money+.04')],
 ('the food bank opens five days a week', 'cook a hot meal for the queue on the coldest night'): [('mark',
                                                                                                   'helped someone '
                                                                                                   'in need')],
 ('the food bank opens five days a week', 'ask the shops you know to give their unsold food each night'): [('person',
                                                                                                            'keeper')],
 ('the food bank opens five days a week', "run a lively raffle night to fill the hall's shelves"): [('means',
                                                                                                     'ties+.04')],
 ('the food bank opens five days a week', "eat at the hall's table with your family, and help clear up after"): [('means',
                                                                                                                  'ties+.03')],
 ('the food bank opens five days a week', 'stand at the door and greet everyone who comes by name'): [('person',
                                                                                                       'regular')],
 ('the food bank opens five days a week', 'set up a fair system so the food goes to those who need it most'): [('lesson',
                                                                                                                'fair '
                                                                                                                'rules '
                                                                                                                'reach '
                                                                                                                'more '
                                                                                                                'people')],
 ('a broken shop window on the high street', 'go to the police with the owner, and give your account of the night'): [('person',
                                                                                                                       'neighbour')],
 ('a broken shop window on the high street', 'keep out of it, and keep your own door shut for a few days'): [('person',
                                                                                                              'neighbour '
                                                                                                              'lost')],
 ('a broken shop window on the high street', 'keep watch at the shop door for the next few nights'): [('place',
                                                                                                       'prot.watch')],
 ('a broken shop window on the high street', 'keep buying your bread there every morning, as always'): [('person',
                                                                                                         'keeper')],
 ('a broken shop window on the high street', 'raise a quiet collection on the street to pay for new glass'): [('mark',
                                                                                                               'helped '
                                                                                                               'someone '
                                                                                                               'in '
                                                                                                               'need')],
 ('a broken shop window on the high street', 'get the whole street out for a supper on the pavement, every family together'): [('means',
                                                                                                                                'ties+.05')],
 ('a broken shop window on the high street', 'take a quiet word to the people stirring things up in the pub'): [('door',
                                                                                                                 'made '
                                                                                                                 'an '
                                                                                                                 'enemy')],
 ('a broken shop window on the high street', 'speak at the council meeting against the hatred on the street'): [('place',
                                                                                                                 'rule.voice')],
 ('a broken shop window on the high street', 'help the owner fit shutters and a camera before the next night'): [('means',
                                                                                                                  'time-.03')],
 ('the leader of thirty years steps down', 'serve on the search committee, and keep it fair and by the book'): [('place',
                                                                                                                 'rule.counsel')],
 ('the leader of thirty years steps down', 'write down what the congregation needs, and send it to the committee'): [('lesson',
                                                                                                                      'say '
                                                                                                                      'plainly '
                                                                                                                      'what '
                                                                                                                      'is '
                                                                                                                      'needed')],
 ('the leader of thirty years steps down', 'put your own name forward for the post'): [('person', 'rival')],
 ('the leader of thirty years steps down', 'campaign loudly for the young preacher who fills the hall'): [('place',
                                                                                                           'rule.voice')],
 ('the leader of thirty years steps down', 'throw the old leader a farewell the whole town will remember'): [('means',
                                                                                                              'money-.04')],
 ('the leader of thirty years steps down', 'back the candidate the old families want, and keep the peace'): [('door',
                                                                                                              'gave '
                                                                                                              'in to '
                                                                                                              'pressure')],
 ('the leader of thirty years steps down', 'ask the old leader, privately, whom they would choose and why'): [('lesson',
                                                                                                               'ask '
                                                                                                               'the '
                                                                                                               'one '
                                                                                                               'who '
                                                                                                               'knows')],
 ('the leader of thirty years steps down', 'invite every candidate to speak openly to the whole congregation'): [('means',
                                                                                                                  'ties+.04')],
 ('the leader of thirty years steps down', 'steer the choosing over quiet coffees in the back room'): [('door',
                                                                                                        'kept it '
                                                                                                        'hidden')],
 ('the leader of thirty years steps down', 'hold a night of song in thanks for the old leader before the vote'): [('place',
                                                                                                                   'arts.song')],
 ('the retreat house is sold', "save the house's books and records for the town library"): [('place',
                                                                                             'learn.keeping')],
 ('the retreat house is sold', 'buy a field of the land yourself while the price is low'): [('means', 'money-.10')],
 ('the retreat house is sold', 'join the petition to stop the sale, and speak at the hearing'): [('place',
                                                                                                  'rule.voice')],
 ('the retreat house is sold', 'help the old residents keep their graveyard out of the sale'): [('mark',
                                                                                                 'helped someone in '
                                                                                                 'need')],
 ('the retreat house is sold', 'camp in the old orchard on the last night with your aunt and her friends'): [('means',
                                                                                                              'ties+.04')],
 ('the retreat house is sold', "read the sale's small print, and find the clause that saves the prayer room"): [('lesson',
                                                                                                                 'the '
                                                                                                                 'small '
                                                                                                                 'print '
                                                                                                                 'matters')],
 ('the retreat house is sold', "record your aunt's memories of the house before they are forgotten"): [('lesson',
                                                                                                        'every house '
                                                                                                        'keeps its '
                                                                                                        'stories')],
 ('the retreat house is sold', 'press the council to keep part of the house as a care home'): [('place',
                                                                                                'rule.counsel')],
 ('a wedding with two rites', "ask the couple, gently, whether one of them will take up the other's faith"): [('means',
                                                                                                               'ties-.03')],
 ('a wedding with two rites', 'stand up at the wedding and toast the couple, loud and proud'): [('person', 'friend')],
 ('a wedding with two rites', "stay away from the wedding, and keep to the family's old ways"): [('means',
                                                                                                  'ties-.06')],
 ('a wedding with two rites', 'pay for the feast, so both families eat as well as each other'): [('means',
                                                                                                  'money-.08')],
 ('a wedding with two rites', 'dance with both grandmothers, whatever the band is playing'): [('lesson',
                                                                                               'a dance can mend a '
                                                                                               'lot')],
 ('a wedding with two rites', 'help the couple write a rite of their own that honours both sides'): [('lesson',
                                                                                                      'two families '
                                                                                                      'can share one '
                                                                                                      'day')],
 ('a wedding with two rites', 'broker a seating plan that keeps the quarrelsome uncles apart'): [('means',
                                                                                                  'time-.03')],
 ('a wedding with two rites', 'sit both sets of parents down before the day and agree the order of things'): [('means',
                                                                                                               'ties+.04')],
 ('a fortune left to the food bank', "keep the gift's conditions to the letter, year after year"): [('place',
                                                                                                     'rule.counsel')],
 ('a fortune left to the food bank', 'ask the town what it needs most before anything is spent'): [('lesson',
                                                                                                    'ask before you '
                                                                                                    'spend')],
 ('a fortune left to the food bank', 'give a gift of your own beside hers, with your name on a second plaque'): [('means',
                                                                                                                  'money-.08')],
 ('a fortune left to the food bank', 'throw open the new kitchen with a feast for the whole street'): [('means',
                                                                                                        'ties+.05')],
 ('a fortune left to the food bank', 'write a gift to the kitchen into your own will'): [('door', 'kept your word')],
 ('a fortune left to the food bank', 'push to spend the money fast and boldly on something new'): [('door',
                                                                                                    'took a wild '
                                                                                                    'risk')],
 ('a fortune left to the food bank', 'cook in the new kitchen at weekends, and teach the young to cook'): [('place',
                                                                                                            'faith.congregation')],
 ('a fortune left to the food bank', "set up a fund for poor children's schooling, as the old gifts did"): [('mark',
                                                                                                             'helped '
                                                                                                             'someone '
                                                                                                             'in '
                                                                                                             'need')],
 ('a fortune left to the food bank', 'invest the fortune carefully so it lasts a hundred years'): [('lesson',
                                                                                                    'slow money '
                                                                                                    'lasts longest')],
 ('a fortune left to the food bank', 'draw up clear rules for who may ask for help, and how'): [('means',
                                                                                                 'time-.04')],
 ('the funeral bill', 'split the bill fairly between the cousins, by what each can pay'): [('means', 'money-.04')],
 ('the funeral bill', 'find what the dead one wrote down about their wishes, and follow it'): [('door',
                                                                                                'kept your word')],
 ('the funeral bill', 'borrow what it takes so the funeral is the finest the street has seen'): [('means',
                                                                                                  'money-.10')],
 ('the funeral bill', 'sing the old song at the grave, and let the tears come'): [('lesson',
                                                                                   'tears are allowed here')],
 ('the funeral bill', 'keep every mourning custom the family has, down to the last'): [('means', 'time-.04')],
 ('the funeral bill', 'speak at the service yourself, and make the farewell your own'): [('means', 'ties+.03')],
 ('the funeral bill', "choose a simple rite, and give what is saved to the dead one's favourite cause"): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('the funeral bill', 'write the eulogy from the stories every cousin sends you'): [('means', 'ties+.05')],
 ('the funeral bill', "ask the faith's funeral fund for help, and fill in every form"): [('means', 'money+.04')],
 ('the funeral bill', 'cook the funeral meal with the aunts, the way it has always been done'): [('means',
                                                                                                  'ties+.04')],
 ('a new café on the corner', "offer to set out the long tables on the new place's open community night"): [('place',
                                                                                                             'gather.house')],
 ('a new café on the corner', 'get to know the owner in the first week, before anyone else does'): [('person',
                                                                                                     'keeper')],
 ('a new café on the corner', 'be there on the opening night and stay until they stack the chairs'): [('person',
                                                                                                       'friend')],
 ('a new café on the corner', 'keep to the old bar, where your name is on a mug behind the counter'): [('lesson',
                                                                                                        'the '
                                                                                                        'regulars '
                                                                                                        'notice who '
                                                                                                        'stays')],
 ('a new café on the corner', 'split the week between both places, and stay on good terms with both keepers'): [('means',
                                                                                                                 'ties+.03')],
 ('a new café on the corner', 'ask the owner for the back room on Fridays, and fill it with your own crowd'): [('place',
                                                                                                                'gather.circle')],
 ('a new café on the corner', 'take the old quiz team to the new place, and win on the first night'): [('place',
                                                                                                        'gather.house')],
 ('a new café on the corner', 'ask the new owner to welcome the old regulars with a shared supper'): [('person',
                                                                                                       'regular')],
 ('a new café on the corner', 'help run the Tuesday talks, so that anyone who comes may speak'): [('place',
                                                                                                   'gather.talk')],
 ('the wake in the old bar', 'draw up a plan to keep the bar open, and take it to the family'): [('means',
                                                                                                  'time-.06')],
 ('the wake in the old bar', 'ask the family for first refusal on the lease, before anyone else asks'): [('door',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the wake in the old bar', 'lead the wake the way the owner would have wanted, loud and long'): [('means',
                                                                                                    'ties+.03')],
 ('the wake in the old bar', 'speak at the funeral about the owner and the old days at the bar'): [('lesson',
                                                                                                    'saying it aloud '
                                                                                                    'helps')],
 ('the wake in the old bar', 'keep coming whoever buys it, and tell the new owner who the old regulars are'): [('person',
                                                                                                                'keeper')],
 ('the wake in the old bar', "gather the regulars' stories and photos of the bar before they are lost"): [('person',
                                                                                                           'elder')],
 ('the wake in the old bar', "hold a night of stories about the owner, with the owner's favourite band after"): [('place',
                                                                                                                  'arts.tale')],
 ('the wake in the old bar', 'pay for the wake, and ask the regulars to join a fund to buy the bar'): [('means',
                                                                                                        'money-.06')],
 ('the wake in the old bar', 'rally the regulars to object together when a developer bids for the building'): [('place',
                                                                                                                'rule.voice')],
 ('the morning after the fight outside the club', 'give the police a statement of exactly what you saw'): [('door',
                                                                                                            'made an '
                                                                                                            'enemy')],
 ('the morning after the fight outside the club', 'ask the club for the camera footage before anyone tells their story'): [('lesson',
                                                                                                                            'the '
                                                                                                                            'cameras '
                                                                                                                            'take '
                                                                                                                            'no '
                                                                                                                            'sides')],
 ('the morning after the fight outside the club', 'keep your name out of it, and stay friendly with the doormen'): [('door',
                                                                                                                     'refused '
                                                                                                                     'someone '
                                                                                                                     'in '
                                                                                                                     'need')],
 ('the morning after the fight outside the club', 'bring the old crowd to the bedside with food and music, so your friend laughs again'): [('means',
                                                                                                                                            'ties+.03')],
 ('the morning after the fight outside the club', 'find out quietly who saw what, and whom the police will believe'): [('person',
                                                                                                                        'go-between')],
 ('the morning after the fight outside the club', 'write the whole night down while you are still angry, then decide what to do'): [('lesson',
                                                                                                                                     'anger '
                                                                                                                                     'reads '
                                                                                                                                     'differently '
                                                                                                                                     'next '
                                                                                                                                     'day')],
 ('the morning after the fight outside the club', 'pay for a lawyer for your friend, and ask the regulars to chip in'): [('means',
                                                                                                                          'money-.06')],
 ('the morning after the fight outside the club', 'ask the elders of both families to sit down before it turns into a feud'): [('person',
                                                                                                                                'elder')],
 ('the bars must close at ten', 'keep the closing hour, and see the older regulars safely home by ten'): [('person',
                                                                                                           'regular')],
 ('the bars must close at ten', 'ask the council in writing what the closing hour is for, and share the answer'): [('lesson',
                                                                                                                    'asking '
                                                                                                                    'in '
                                                                                                                    'writing '
                                                                                                                    'gets '
                                                                                                                    'answers')],
 ('the bars must close at ten', 'rent a basement and run the after-hours door yourself'): [('means', 'money+.06'),
                                                                                           ('door', 'broke the law')],
 ('the bars must close at ten', 'move the Saturday gathering to your kitchen, and invite the whole street'): [('place',
                                                                                                               'gather.house')],
 ('the bars must close at ten', 'throw your own party in a flat, music loud, door open to friends of friends'): [('person',
                                                                                                                  'friend')],
 ('the bars must close at ten', 'find out which bars the patrols leave alone, and why'): [('person', 'go-between')],
 ('the bars must close at ten', 'start a reading evening at home on the nights the bars are shut'): [('place',
                                                                                                      'gather.circle')],
 ('the bars must close at ten', 'set up a rota so nobody on the street walks home alone at night'): [('place',
                                                                                                      'prot.watch')],
 ('the bars must close at ten', 'march against the closing hour, singing with the bar crowd'): [('place',
                                                                                                 'rule.voice')],
 ('the dry years', "keep the law, and help out at the sober reading room's evenings"): [('place', 'learn.keeping')],
 ('the dry years', 'weigh what each side claims, and argue it out at the debating club'): [('place', 'gather.talk')],
 ('the dry years', 'sell the bottles in your cellar to the back-room clubs, at a good price'): [('means',
                                                                                                 'money+.06')],
 ('the dry years', 'learn the knock, and keep your Friday nights at the teacup club'): [('place', 'gather.night')],
 ('the dry years', 'brew a little at home for the family feasts, as the old ones did'): [('door', 'kept it hidden')],
 ('the dry years', 'open a teacup club of your own at the back of a café'): [('place', 'gather.night'),
                                                                             ('door', 'broke the law')],
 ('the dry years', 'keep the dances going in the hall, with fruit punch and the same band'): [('place',
                                                                                               'gather.hall')],
 ('the dry years', "pay the old bar's rent through the ban, so it can open again one day"): [('means', 'money-.10')],
 ('the dry years', 'put the case for repeal to the town meeting, with the facts and a vote'): [('place',
                                                                                                'rule.voice')],
 ('the flood in the community centre', 'turn up with gloves every Saturday until the hall is cleared'): [('means',
                                                                                                          'time-.06')],
 ('the flood in the community centre', 'get the building surveyed, and work out what saving it truly costs'): [('lesson',
                                                                                                                'saving '
                                                                                                                'costs '
                                                                                                                'more '
                                                                                                                'than '
                                                                                                                'it '
                                                                                                                'seems')],
 ('the flood in the community centre', "take the rich family's money, and get your group the best room in the new hall"): [('person',
                                                                                                                            'patron')],
 ('the flood in the community centre', 'throw a fundraising party in the car park, mud and all'): [('means',
                                                                                                    'ties+.03')],
 ('the flood in the community centre', 'host your group in your own kitchen every week until the hall is back'): [('place',
                                                                                                                   'gather.house')],
 ('the flood in the community centre', 'start a new night of your own in a rented room while the hall is shut'): [('place',
                                                                                                                   'gather.circle')],
 ('the flood in the community centre', 'save the old photos and records from the mud, and dry them page by page'): [('place',
                                                                                                                     'learn.keeping')],
 ('the flood in the community centre', 'draw up a better hall with the young members, and show it at the meeting'): [('person',
                                                                                                                      'friend')],
 ('the flood in the community centre', 'join the committee that spends the rebuilding money, and share it among every group'): [('place',
                                                                                                                                 'rule.counsel')],
 ('the flood in the community centre', 'hold a shared supper each month so the scattered groups still meet'): [('person',
                                                                                                                'neighbour')],
 ('long tables in the street when the war ends', 'sit with the soldiers and listen to what the war was really like'): [('lesson',
                                                                                                                        'the '
                                                                                                                        'news '
                                                                                                                        'told '
                                                                                                                        'it '
                                                                                                                        'wrong')],
 ('long tables in the street when the war ends', 'dance in the street with strangers until dawn'): [('means',
                                                                                                     'ties+.03')],
 ('long tables in the street when the war ends', 'carry the family table out into the street and cook the dish everyone missed'): [('place',
                                                                                                                                    'gather.great')],
 ('long tables in the street when the war ends', 'sit with the soldier nobody wants to talk to, and keep the drinks coming'): [('person',
                                                                                                                                'friend')],
 ('long tables in the street when the war ends', 'introduce the soldiers home without work to the people who are hiring'): [('mark',
                                                                                                                             'helped '
                                                                                                                             'someone '
                                                                                                                             'in '
                                                                                                                             'need')],
 ('long tables in the street when the war ends', 'lead the whole street in the old songs from before the war'): [('place',
                                                                                                                  'arts.song')],
 ('long tables in the street when the war ends', 'set up a table where people can ask after the missing and the found'): [('person',
                                                                                                                           'neighbour')],
 ('hard times fill the soup night', 'sit at the bar where the bosses drink, and ask who needs a hand this week'): [('person',
                                                                                                                    'boss')],
 ('hard times fill the soup night', 'throw a party where everyone brings what they can'): [('place', 'gather.house')],
 ('hard times fill the soup night', 'keep the Sunday dinner going, however small, with a place kept for your friend'): [('lesson',
                                                                                                                         'a '
                                                                                                                         'small '
                                                                                                                         'table '
                                                                                                                         'still '
                                                                                                                         'holds')],
 ('hard times fill the soup night', 'keep going to the corner bar, and buy a drink for whoever is out of work'): [('means',
                                                                                                                   'money-.03')],
 ('hard times fill the soup night', 'start a swap night for tools, clothes and seeds at the community centre'): [('place',
                                                                                                                  'gather.hall')],
 ('hard times fill the soup night', 'get the old team back together for free matches in the park'): [('place',
                                                                                                      'gather.games')],
 ('hard times fill the soup night', 'help keep the job board, so every new post is seen by everyone'): [('means',
                                                                                                         'ties+.03')],
 ('three days at the convention', 'volunteer at the door and help the newcomers find their way'): [('place',
                                                                                                    'gather.great')],
 ('three days at the convention', 'work the stalls with your cards, and come home with three new contacts'): [('person',
                                                                                                               'colleague')],
 ('three days at the convention', 'enter the contest on the last afternoon, in front of everyone'): [('person',
                                                                                                      'rival')],
 ('three days at the convention', 'meet the old friends at the same café table, as every year'): [('place',
                                                                                                   'gather.circle')],
 ('three days at the convention', 'trade news with the stallholders each morning before the doors open'): [('place',
                                                                                                            'comm.market')],
 ('three days at the convention', 'show what you have made or grown at a stall of your own'): [('means',
                                                                                                'money+.03')],
 ('three days at the convention', "pay for the club's table, and host the members who cannot afford to come"): [('means',
                                                                                                                 'money-.06')],
 ('three days at the convention', 'turn up in the club shirt with the whole group, and cheer your side on'): [('means',
                                                                                                               'ties+.03')],
 ('the club adds a waiting list', 'vote to let in everyone on the list, in the order they applied'): [('means',
                                                                                                       'ties+.03')],
 ('the club adds a waiting list', 'show the meeting what the minutes say about who waits and who does not'): [('person',
                                                                                                               'rival')],
 ('the club adds a waiting list', 'vote with the old members, and keep the fee where it is'): [('person', 'elder')],
 ('the club adds a waiting list', 'resign from the club and say why, loudly'): [('means', 'ties-.06')],
 ('the club adds a waiting list', "keep the old families' club as it is, and invite your friend home instead"): [('place',
                                                                                                                  'gather.house')],
 ('the club adds a waiting list', 'sponsor your friend yourself, and vouch for them in front of the members'): [('door',
                                                                                                                 'kept '
                                                                                                                 'your '
                                                                                                                 'word')],
 ('the club adds a waiting list', 'find out quietly who on the committee could move your friend up the list'): [('person',
                                                                                                                 'go-between')],
 ('the club adds a waiting list', 'help the new families start their own club, with talks and a band'): [('place',
                                                                                                          'gather.hall')],
 ('the club adds a waiting list', 'offer to run a free open night each month for anyone in town'): [('means',
                                                                                                     'time-.03')],
 ('the club adds a waiting list', 'rally the younger members to vote the waiting list down'): [('door',
                                                                                                'defied an '
                                                                                                'authority')],
 ('someone at the table passes it on', 'stand up at the table and remind everyone what the rule has always been'): [('lesson',
                                                                                                                     'some '
                                                                                                                     'rules '
                                                                                                                     'need '
                                                                                                                     'saying '
                                                                                                                     'aloud')],
 ('someone at the table passes it on', 'work out quietly who could have known, and keep it to yourself'): [('door',
                                                                                                            'kept it '
                                                                                                            'hidden')],
 ('someone at the table passes it on', 'find out what the informer is being paid, and by whom'): [('person',
                                                                                                   'rival')],
 ('someone at the table passes it on', 'stop talking at the bar, and keep the real talk for your own kitchen table'): [('means',
                                                                                                                        'ties-.03')],
 ('someone at the table passes it on', 'find a new bar with your own crowd, where you choose who sits down'): [('place',
                                                                                                                'gather.circle')],
 ('someone at the table passes it on', 'take the old crowd to the hills for a weekend, where nobody is listening'): [('means',
                                                                                                                      'ties+.03')],
 ('someone at the table passes it on', 'feed the table a false story, and see where it turns up'): [('lesson',
                                                                                                     'a false trail '
                                                                                                     'finds the '
                                                                                                     'leak')],
 ('someone at the table passes it on', "write to the employer with the regulars' names, saying the joke was only a joke"): [('door',
                                                                                                                             'defied '
                                                                                                                             'an '
                                                                                                                             'authority')],
 ('the team is down to nine players', "take on the secretary's job, so someone holds the team together"): [('means',
                                                                                                            'time-.06')],
 ('the team is down to nine players', 'work out a plan to merge with the club in the next town'): [('person',
                                                                                                    'colleague')],
 ('the team is down to nine players', "use the team's trouble to win yourself a seat on the league committee"): [('place',
                                                                                                                  'rule.counsel')],
 ('the team is down to nine players', 'ring every old player and talk them into one more season'): [('person',
                                                                                                     'friend')],
 ('the team is down to nine players', 'let the team go, and keep Sunday evenings for home'): [('means', 'time+.06')],
 ('the team is down to nine players', 'say plainly that the team has run its course, and buy the last round'): [('means',
                                                                                                                 'money-.03')],
 ('the team is down to nine players', 'start a kickabout in the park instead, with no league and no list'): [('place',
                                                                                                              'gather.games')],
 ('the team is down to nine players', 'set up a group chat and a shorter match that fits a working week'): [('means',
                                                                                                             'ties+.03')],
 ('the team is down to nine players', 'pay the league fees yourself this season, to keep the team alive'): [('means',
                                                                                                             'money-.06')],
 ('the team is down to nine players', 'call a meeting where every player gets a say on what happens next'): [('lesson',
                                                                                                              'everyone '
                                                                                                              'heard '
                                                                                                              'stays '
                                                                                                              'longer')],
 ('a dozen new groups in a year', "take on the group's list, its keys and its tea rota"): [('means', 'time-.06')],
 ('a dozen new groups in a year', 'put yourself up for treasurer while the group is new'): [('place', 'gather.hall')],
 ('a dozen new groups in a year', "join the parents' circle, and bring the grandparents along too"): [('place',
                                                                                                       'gather.circle')],
 ('a dozen new groups in a year', 'say yes to whichever group asks first, and take it as it comes'): [('person',
                                                                                                       'neighbour')],
 ('a dozen new groups in a year', 'start a walking group that goes wherever its members feel like going'): [('person',
                                                                                                             'friend')],
 ('a dozen new groups in a year', 'find out which groups the council will fund, and steer the group that way'): [('place',
                                                                                                                  'rule.counsel')],
 ('a dozen new groups in a year', 'turn up for every match of the new team in its shirt, with a drum'): [('place',
                                                                                                          'gather.games')],
 ('a dozen new groups in a year', 'draw up a fair set of rules for the group, and put them to a vote'): [('lesson',
                                                                                                          'rules '
                                                                                                          'agreed '
                                                                                                          'are rules '
                                                                                                          'kept')],
 ('the whole street watches the final', "watch with the old supporters' club, as you have for years"): [('place',
                                                                                                         'gather.games')],
 ('the whole street watches the final', 'talk the old hands at the bar through every move of the game'): [('person',
                                                                                                           'regular')],
 ('the whole street watches the final', 'paint your face, lose your voice, and dance on a table when the goal goes in'): [('means',
                                                                                                                           'ties+.03')],
 ('the whole street watches the final', 'watch it at home with the family, in the same chairs as always'): [('lesson',
                                                                                                             'some '
                                                                                                             'evenings '
                                                                                                             'belong '
                                                                                                             'to '
                                                                                                             'family')],
 ('the whole street watches the final', 'go to the big screen in the park, and hug whichever stranger is nearest'): [('person',
                                                                                                                      'friend')],
 ('the whole street watches the final', "compare notes with the club's old scout, and learn whom to watch next season"): [('person',
                                                                                                                           'mentor')],
 ('the whole street watches the final', 'teach the youngest in the family the rules as the game goes'): [('lesson',
                                                                                                          'teaching '
                                                                                                          'it makes '
                                                                                                          'it '
                                                                                                          'yours')],
 ('the whole street watches the final', 'pay for a screen and food at the community centre for anyone who comes'): [('means',
                                                                                                                     'money-.06')],
 ('the whole street watches the final', "lead the street in the club's songs until the final whistle"): [('person',
                                                                                                          'neighbour')],
 ('a post says the water is poisoned', 'tell the family to boil the water, and not share the post until it is checked'): [('lesson',
                                                                                                                           'fear '
                                                                                                                           'spreads '
                                                                                                                           'faster '
                                                                                                                           'than '
                                                                                                                           'facts')],
 ('a post says the water is poisoned', "ask who has seen a real test, and wait for the council's results"): [('lesson',
                                                                                                              'wait '
                                                                                                              'for '
                                                                                                              'the '
                                                                                                              'real '
                                                                                                              'result')],
 ('a post says the water is poisoned', 'buy a stock of bottled water early, before the price climbs again'): [('means',
                                                                                                               'money-.03')],
 ('a post says the water is poisoned', 'share the post with everyone you know, just in case'): [('door',
                                                                                                 'gave in to '
                                                                                                 'pressure')],
 ('a post says the water is poisoned', 'drink a glass from the tap in front of the neighbours, and carry on as before'): [('mark',
                                                                                                                           'took '
                                                                                                                           'a '
                                                                                                                           'wild '
                                                                                                                           'risk')],
 ('a post says the water is poisoned', 'take a sample of the water to be tested, and share the result'): [('person',
                                                                                                           'neighbour')],
 ('a post says the water is poisoned', 'post a sharp reply with the facts, and keep at it all night'): [('person',
                                                                                                         'rival')],
 ('a post says the water is poisoned', 'ask the council for a statement tonight, and offer to hand it round'): [('place',
                                                                                                                 'rule.counsel')],
 ('a post says the water is poisoned', 'rally the neighbours to the waterworks gates to demand answers'): [('place',
                                                                                                            'rule.voice')],
 ("the town's new news feed", 'write in politely to ask that the item be put right'): [('lesson',
                                                                                        'asking politely sometimes '
                                                                                        'works')],
 ("the town's new news feed", 'check every claim in the item, and post the true story under it'): [('person',
                                                                                                    'rival')],
 ("the town's new news feed", 'get to know the person who runs the feed, and bring them better stories'): [('person',
                                                                                                            'go-between')],
 ("the town's new news feed", 'answer the item with a joke so good the whole town laughs along'): [('means',
                                                                                                    'ties+.03')],
 ("the town's new news feed", 'turn off the phone and go to the market as usual, head up'): [('place',
                                                                                              'comm.market')],
 ("the town's new news feed", 'find out who sent the item in, and what they hoped to gain'): [('lesson',
                                                                                               'every story has a '
                                                                                               'sender')],
 ("the town's new news feed", 'start your own page about the town, with the arguments and the jokes'): [('place',
                                                                                                         'arts.page')],
 ("the town's new news feed", "offer the feed a weekly piece on the town's clubs, each one in its turn"): [('place',
                                                                                                            'gather.hall')],
 ("the town's new news feed", 'ask the feed to carry the births and the weddings, not the quarrels'): [('person',
                                                                                                        'neighbour')],
 ('the old rail yard becomes a park', 'sign up to the rota that keeps the park clean and safe'): [('place',
                                                                                                   'prot.watch')],
 ('the old rail yard becomes a park', 'rent a stall on the market square on Saturdays'): [('place', 'comm.market')],
 ('the old rail yard becomes a park', 'bring the whole family for a picnic every Sunday, and ask the neighbours along'): [('person',
                                                                                                                           'neighbour')],
 ('the old rail yard becomes a park', 'put on a music night on the benches, and fill the square with your crowd'): [('place',
                                                                                                                     'arts.song')],
 ('the old rail yard becomes a park', 'pay for a bench with a plaque, and see that it is kept'): [('means',
                                                                                                   'money-.06')],
 ('the old rail yard becomes a park', 'go to the park meeting and speak up for keeping it open to all'): [('place',
                                                                                                           'rule.counsel')],
 ('nobody can find the drawings for the pumps', 'press the council to have the whole system written down, with copies kept for all'): [('place',
                                                                                                                                        'rule.voice')],
 ('nobody can find the drawings for the pumps', 'ring the retired engineer and ask him to talk you through the system'): [('person',
                                                                                                                           'mentor')],
 ('nobody can find the drawings for the pumps', 'learn the old system first, and offer the council your help at a price'): [('means',
                                                                                                                             'money+.06')],
 ('nobody can find the drawings for the pumps', 'walk the route of the pipes with the old men who laid them'): [('person',
                                                                                                                 'elder')],
 ('nobody can find the drawings for the pumps', 'study each burst pipe as it is dug up, and write down what it teaches'): [('lesson',
                                                                                                                            'every '
                                                                                                                            'break '
                                                                                                                            'teaches '
                                                                                                                            'something')],
 ('nobody can find the drawings for the pumps', 'teach yourself the pumps from manuals at night, and mend one on your own'): [('mark',
                                                                                                                               'learned '
                                                                                                                               'a '
                                                                                                                               'skill')],
 ('nobody can find the drawings for the pumps', 'record what the old pipe-layers remember before it is lost as well'): [('place',
                                                                                                                         'learn.keeping')],
 ('nobody can find the drawings for the pumps', 'start a class for the young plumbers, so no skill rests with one person again'): [('place',
                                                                                                                                    'prod.craft')],
 ('nobody can find the drawings for the pumps', 'draw up a plain manual of the whole system for whoever comes next'): [('lesson',
                                                                                                                        'write '
                                                                                                                        'it '
                                                                                                                        'down '
                                                                                                                        'for '
                                                                                                                        'others')],
 ('a new school across the river', 'go door to door on the far bank, so every family knows a place is theirs'): [('means',
                                                                                                                  'ties+.06')],
 ('a new school across the river', 'sit in on a lesson, and ask the new teacher how they teach reading'): [('person',
                                                                                                            'teacher')],
 ('a new school across the river', "stand for the new school's board in its first year"): [('place', 'rule.counsel')],
 ('a new school across the river', 'move your child to the new school in the first week, and see how it goes'): [('means',
                                                                                                                  'time+.06')],
 ('a new school across the river', 'keep your child at the old school in town, with the cousins'): [('door',
                                                                                                     'stayed home')],
 ('a new school across the river', 'spend the free morning hour reading together, whatever book the child picks'): [('lesson',
                                                                                                                     'the '
                                                                                                                     'quiet '
                                                                                                                     'hour '
                                                                                                                     'matters')],
 ('a new school across the river', "read the new school's reports and the teachers' records before you choose"): [('lesson',
                                                                                                                   'look '
                                                                                                                   'closely '
                                                                                                                   'before '
                                                                                                                   'choosing')],
 ('a new school across the river', 'help the class start a garden by the river and record what grows'): [('place',
                                                                                                          'prod.land')],
 ('a new school across the river', "join the parents' committee that helps build and keep the new school"): [('place',
                                                                                                              'rule.counsel')],
 ('a new school across the river', "speak up at the meeting for the far bank's children to get the first places"): [('place',
                                                                                                                     'rule.voice')],
 ('a university on the old army base', "help the town school's leavers fill in their university applications"): [('mark',
                                                                                                                  'helped '
                                                                                                                  'someone '
                                                                                                                  'in '
                                                                                                                  'need')],
 ('a university on the old army base', 'take a job in the university office, for the free course that comes with it'): [('place',
                                                                                                                         'learn.higher')],
 ('a university on the old army base', "talk your way into the labs' open day and try every machine they let you touch"): [('lesson',
                                                                                                                            'asking '
                                                                                                                            'gets '
                                                                                                                            'you '
                                                                                                                            'inside')],
 ('a university on the old army base', "lead the new students on a walk of the town's old streets and stories"): [('person',
                                                                                                                   'friend')],
 ('a university on the old army base', "coach the students' new walking club in the hills you know by heart"): [('place',
                                                                                                                 'gather.games')],
 ('a university on the old army base', 'find out which departments will hire locals, before the posts are advertised'): [('lesson',
                                                                                                                          'early '
                                                                                                                          'knowledge '
                                                                                                                          'is '
                                                                                                                          'worth '
                                                                                                                          'having')],
 ('a university on the old army base', 'help the university count and map the wildlife living on the old base'): [('place',
                                                                                                                   'prod.wild')],
 ('a university on the old army base', "start a small scholarship for one local child each year, in the family's name"): [('means',
                                                                                                                           'money-.06')],
 ('a university on the old army base', "campaign for free places for the town's poorer children, and fill the hall to do it"): [('place',
                                                                                                                                 'rule.voice')],
 ('two more years at school', 'stay on and keep up every subject, the way the new rule intends'): [('lesson',
                                                                                                    'steady work '
                                                                                                    'pays off '
                                                                                                    'later')],
 ('two more years at school', 'pick the hardest subject on offer, just to see what it is like'): [('person',
                                                                                                   'teacher')],
 ('two more years at school', 'choose the subjects that lead to the best-paid courses, and work for top marks'): [('place',
                                                                                                                   'learn.higher')],
 ('two more years at school', 'help in the family shop after school and on Saturdays'): [('place', 'comm.shop')],
 ('two more years at school', "ask last year's leavers what they wish they had done, and do that"): [('person',
                                                                                                      'mentor')],
 ('two more years at school', "join the school's outdoor club, and learn the hills and the river by feel"): [('place',
                                                                                                              'gather.games')],
 ('two more years at school', 'read the new rules closely, and find the course that counts toward a trade licence'): [('place',
                                                                                                                       'prod.craft')],
 ('two more years at school', 'speak up at the school council for trade classes for everyone who wants them'): [('place',
                                                                                                                 'rule.counsel')],
 ('two more years at school', 'ask the teachers to set out what the two years must cover, and keep to it'): [('lesson',
                                                                                                              'ask '
                                                                                                              'what '
                                                                                                              'is '
                                                                                                              'expected')],
 ('four points short on the results letter', 'accept the second choice, and give it your best from the first day'): [('place',
                                                                                                                      'learn.higher')],
 ('four points short on the results letter', 'ask to see the marked paper, and learn exactly where the four points went'): [('lesson',
                                                                                                                             'mistakes '
                                                                                                                             'are '
                                                                                                                             'worth '
                                                                                                                             'seeing')],
 ('four points short on the results letter', 'take the second choice, and start planning a transfer in the first week'): [('place',
                                                                                                                           'learn.higher')],
 ('four points short on the results letter', 'turn the place down, and work with your hands for a year before deciding'): [('mark',
                                                                                                                            'learned '
                                                                                                                            'a '
                                                                                                                            'skill')],
 ('four points short on the results letter', 'take the place at the college near home, close to the family'): [('place',
                                                                                                                'learn.higher')],
 ('four points short on the results letter', 'spend the summer working at the outdoor centre, and decide in the autumn'): [('means',
                                                                                                                            'money+.03')],
 ('four points short on the results letter', 'ask the old teacher who knows you best which road truly suits you'): [('person',
                                                                                                                     'mentor')],
 ('four points short on the results letter', 'apply for the scholarship place that asks two years of service in return'): [('door',
                                                                                                                            'kept '
                                                                                                                            'your '
                                                                                                                            'word')],
 ('four points short on the results letter', 'sit the exam again next year, with a plan for every paper'): [('means',
                                                                                                             'time-.06')],
 ('the works is hiring two hundred', 'help run the free training evenings, so anyone in town can apply'): [('mark',
                                                                                                            'helped '
                                                                                                            'someone '
                                                                                                            'in '
                                                                                                            'need')],
 ('the works is hiring two hundred', "go to the lab's public talk and ask how the finding really works"): [('place',
                                                                                                            'learn.higher')],
 ('the works is hiring two hundred', 'apply on the first morning, and ask what it takes to run a line'): [('place',
                                                                                                           'prod.craft')],
 ('the works is hiring two hundred', 'take the job the family would have taken, and bring a cousin along'): [('means',
                                                                                                              'money+.06')],
 ('the works is hiring two hundred', 'join the team that studies every early fault on the new line'): [('person',
                                                                                                        'colleague')],
 ('the works is hiring two hundred', 'teach the new hands on the floor the way you learned, beside them'): [('person',
                                                                                                             'friend')],
 ('the works is hiring two hundred', 'build a small test model at home from the published plans, and show it off'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the works is hiring two hundred', "give to the works' training fund, so the town's young get places first"): [('means',
                                                                                                                  'money-.06')],
 ('the works is hiring two hundred', 'help the college write a fair entry test for the training places'): [('lesson',
                                                                                                            'fairness '
                                                                                                            'takes '
                                                                                                            'careful '
                                                                                                            'work')],
 ('books pulled from the school library', 'hand in the copy as the notice asks, and write to the council asking why'): [('door',
                                                                                                                         'gave '
                                                                                                                         'in '
                                                                                                                         'to '
                                                                                                                         'pressure')],
 ('books pulled from the school library', 'read the complaints and every pulled book, and judge them for yourself'): [('lesson',
                                                                                                                       'read '
                                                                                                                       'before '
                                                                                                                       'you '
                                                                                                                       'judge')],
 ('books pulled from the school library', 'keep your head down this year, and keep your marks up'): [('means',
                                                                                                      'freedom-.03')],
 ('books pulled from the school library', "keep the family's copies at home, and read them together as before"): [('means',
                                                                                                                   'ties+.03')],
 ('books pulled from the school library', 'start a reading circle in a café for the books nobody may read at school'): [('place',
                                                                                                                         'gather.circle')],
 ('books pulled from the school library', 'learn the old songs the list leaves out from the people who still sing them'): [('place',
                                                                                                                            'arts.song')],
 ('books pulled from the school library', 'borrow the pulled books from the archivist, and lend them only to those you trust'): [('door',
                                                                                                                                  'kept '
                                                                                                                                  'it '
                                                                                                                                  'hidden')],
 ('books pulled from the school library', "ask the parents' committee to meet the council about the list, all together"): [('place',
                                                                                                                            'rule.counsel')],
 ('books pulled from the school library', 'ask the school board to set out a fair, open rule for how books are judged'): [('place',
                                                                                                                           'rule.voice')],
 ('half the class takes jobs abroad', 'stay, and take the teaching post at the old school'): [('person',
                                                                                               'colleague')],
 ('half the class takes jobs abroad', 'stay near the family, and use what you learned in the family firm'): [('means',
                                                                                                              'ties+.06')],
 ('half the class takes jobs abroad', "go for one summer's work abroad, and come back with what your hands learned"): [('mark',
                                                                                                                        'learned '
                                                                                                                        'a '
                                                                                                                        'skill')],
 ('half the class takes jobs abroad', 'set up a small lab at home with the friends who stay, and show its work'): [('means',
                                                                                                                    'money-.06')],
 ('half the class takes jobs abroad', 'stay and help run the night school, so others learn what you learned'): [('place',
                                                                                                                 'learn.higher')],
 ('new teachers at the college from far away', 'ask the newcomer surgeon which of her mistakes taught her the most'): [('person',
                                                                                                                        'mentor')],
 ('new teachers at the college from far away', "pick up the newcomers' language in the café, your own way, word by word"): [('mark',
                                                                                                                             'learned '
                                                                                                                             'a '
                                                                                                                             'skill')],
 ('new teachers at the college from far away', "join the newcomers' lab project, and help build the first test model"): [('person',
                                                                                                                          'colleague')],
 ('new teachers at the college from far away', "help the newcomers' children settle in at the local school"): [('mark',
                                                                                                                'helped '
                                                                                                                'someone '
                                                                                                                'in '
                                                                                                                'need')],
 ('new teachers at the college from far away', "help the college set a fair test so the newcomers' old training counts"): [('place',
                                                                                                                            'learn.higher')],
 ('the library reopens after the refit', 'help run the free reading class for grown-ups on Thursday evenings'): [('place',
                                                                                                                  'learn.keeping')],
 ('the library reopens after the refit', 'read your way along one shelf, a book a week, all winter'): [('lesson',
                                                                                                        'a book a '
                                                                                                        'week adds '
                                                                                                        'up')],
 ('the library reopens after the refit', 'book the best study room for every evening of the exam season'): [('place',
                                                                                                             'learn.keeping')],
 ('the library reopens after the refit', "take the family's youngest to the children's corner every Saturday"): [('place',
                                                                                                                  'learn.keeping')],
 ('the library reopens after the refit', 'teach yourself a whole new subject from the shelves, with no course and no exam'): [('mark',
                                                                                                                               'learned '
                                                                                                                               'a '
                                                                                                                               'skill')],
 ('the library reopens after the refit', "join the history group that records the old people's memories of the town"): [('place',
                                                                                                                         'gather.circle')],
 ('the library reopens after the refit', "build something in the workshop, and show it at the library's open evening"): [('place',
                                                                                                                          'arts.craft')],
 ('the library reopens after the refit', "pay for a shelf of new books, with the family's name on a small plate"): [('means',
                                                                                                                     'money-.06')],
 ('the library reopens after the refit', "take a turn on the volunteers' rota that keeps the reading room open late"): [('place',
                                                                                                                         'learn.keeping')],
 ('six weeks with the schools on strike', 'set a daily timetable of reading and sums at the kitchen table'): [('lesson',
                                                                                                               'routine '
                                                                                                               'holds '
                                                                                                               'a '
                                                                                                               'house '
                                                                                                               'together')],
 ('six weeks with the schools on strike', "read both sides' figures, and explain the strike honestly to the children"): [('lesson',
                                                                                                                          'children '
                                                                                                                          'follow '
                                                                                                                          'honest '
                                                                                                                          'reasons')],
 ('six weeks with the schools on strike', 'pay a tutor for the weeks of the strike, and keep your child ahead'): [('means',
                                                                                                                   'money-.06')],
 ('six weeks with the schools on strike', 'take the children to the museum and the woods, and call it school'): [('means',
                                                                                                                  'time-.06')],
 ('six weeks with the schools on strike', "take your turn minding the street's children, and teach them what you know"): [('person',
                                                                                                                           'neighbour')],
 ('six weeks with the schools on strike', 'keep a note of what the children forget, and plan to catch it up later'): [('means',
                                                                                                                       'time-.03')],
 ('six weeks with the schools on strike', 'find out what deal is on the table before the council announces it'): [('person',
                                                                                                                   'go-between')],
 ('six weeks with the schools on strike', "set the street's children a building project in the garage, and test it together"): [('means',
                                                                                                                                 'ties+.03')],
 ('six weeks with the schools on strike', "organise the street's rota of parents, so every child is minded"): [('place',
                                                                                                                'gather.circle')],
 ('six weeks with the schools on strike', 'bring the parents to stand with the teachers at the school gate'): [('place',
                                                                                                                'rule.voice')],
 ('a year with the schools shut', 'do every lesson that comes through, at the hour it is set'): [('lesson',
                                                                                                  'keep the '
                                                                                                  'timetable '
                                                                                                  'anyway')],
 ('a year with the schools shut', 'work through the old textbooks at home, a chapter a day'): [('mark',
                                                                                                'learned a skill')],
 ('a year with the schools shut', 'find an older student online who will tutor you ahead of the class'): [('person',
                                                                                                           'mentor')],
 ('a year with the schools shut', 'keep a list of what the year has cost, and plan how to catch it up'): [('lesson',
                                                                                                           'count '
                                                                                                           'the cost '
                                                                                                           'then '
                                                                                                           'plan')],
 ('a year with the schools shut', 'keep a diary of the year in the town, for the archive to keep'): [('place',
                                                                                                      'learn.keeping')],
 ('a year with the schools shut', 'build a phone charger from old parts with the science teacher'): [('person',
                                                                                                      'teacher')],
 ('a year with the schools shut', 'ask the aid charity for a laptop and a place in its classes'): [('person',
                                                                                                    'patron')],
 ('a degree and a job at the till', 'keep applying for posts in the field, one careful letter at a time'): [('lesson',
                                                                                                             'keep '
                                                                                                             'going '
                                                                                                             'letter '
                                                                                                             'by '
                                                                                                             'letter')],
 ('a degree and a job at the till', 'keep reading in the field in the evenings, and write about it online'): [('place',
                                                                                                               'arts.page')],
 ('a degree and a job at the till', 'work every contact you have for a post, and call in favours'): [('means',
                                                                                                      'ties-.06')],
 ('a degree and a job at the till', 'go to the Thursday meetings of the young, and speak at one'): [('place',
                                                                                                     'rule.voice')],
 ('a degree and a job at the till', 'teach what you know online, your own way, to whoever will pay'): [('means',
                                                                                                        'money+.06')],
 ('a degree and a job at the till', 'study the hiring lists, and find the field with more posts than graduates'): [('lesson',
                                                                                                                    'follow '
                                                                                                                    'where '
                                                                                                                    'the '
                                                                                                                    'posts '
                                                                                                                    'are')],
 ('a degree and a job at the till', "tutor the street's children for free on Saturdays while you look"): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('a degree and a job at the till', 'press the university to publish how many of its graduates find work'): [('place',
                                                                                                              'rule.voice')],
 ('a weekend school for the old language', 'go every Saturday, and bring the whole family along'): [('place',
                                                                                                     'gather.hall')],
 ('a weekend school for the old language', "read up on the language's history, and ask the oldest speakers what the words mean"): [('person',
                                                                                                                                    'elder')],
 ('a weekend school for the old language', 'offer to teach a class at the weekend school, for the small wage'): [('means',
                                                                                                                  'money+.03')],
 ('a weekend school for the old language', 'laugh at your own mistakes in class, and learn from each one'): [('lesson',
                                                                                                              'mistakes '
                                                                                                              'are '
                                                                                                              'part '
                                                                                                              'of '
                                                                                                              'learning')],
 ('a weekend school for the old language', 'mix the old words into your own songs and posts, your own way'): [('place',
                                                                                                               'arts.song')],
 ('a weekend school for the old language', 'record the oldest speakers telling their stories, for the school to keep'): [('place',
                                                                                                                          'learn.keeping')],
 ('a weekend school for the old language', 'speak up for the old language at the town school, so every child can take it'): [('place',
                                                                                                                              'rule.voice')],
 ('a weekend school for the old language', 'help write a simple course book, so every class learns the same words'): [('place',
                                                                                                                       'arts.page')],
 ('the archive floods overnight', 'write to every archive and scholar who might hold copies of the old registers'): [('place',
                                                                                                                      'learn.keeping')],
 ('the archive floods overnight', "have the family's claim written down and witnessed before the arguments start"): [('lesson',
                                                                                                                      'get '
                                                                                                                      'it '
                                                                                                                      'in '
                                                                                                                      'writing')],
 ('the archive floods overnight', 'carry boxes out of the basement with the crew until the water is gone'): [('place',
                                                                                                              'prot.rescue')],
 ('the archive floods overnight', 'sit with the oldest in the family, and write down all they remember'): [('means',
                                                                                                            'ties+.03')],
 ('the archive floods overnight', 'study what went wrong in the basement, and show how to keep the next store safe'): [('lesson',
                                                                                                                        'a '
                                                                                                                        'store '
                                                                                                                        'needs '
                                                                                                                        'a '
                                                                                                                        'plan')],
 ('the archive floods overnight', 'dry the old photographs by hand, one by one, on the kitchen table'): [('means',
                                                                                                          'time-.06')],
 ('the archive floods overnight', 'help the archivist sort out which papers can still prove a claim'): [('person',
                                                                                                         'keeper')],
 ('the archive floods overnight', 'rally the neighbours with buckets and boxes before the water rises again'): [('means',
                                                                                                                 'ties+.06')],
 ('the archive floods overnight', 'press for a rule that every record is copied and kept in two places'): [('place',
                                                                                                            'rule.voice')],
 ('the family in the flat below', 'put the father in touch with the firm that needs an accountant'): [('door',
                                                                                                       'helped '
                                                                                                       'someone in '
                                                                                                       'need')],
 ('the family in the flat below', 'keep a polite distance, and greet them on the stairs'): [('lesson',
                                                                                             'a greeting is enough')],
 ('the family in the flat below', 'pick up a little of their language, word by word, just for the fun of it'): [('mark',
                                                                                                                 'learned '
                                                                                                                 'a '
                                                                                                                 'skill')],
 ('the family in the flat below', "teach the family's youngest to ride a bike in the yard"): [('person',
                                                                                               'neighbour')],
 ('the family in the flat below', 'swap recipes with the grandmother, and write them down for both families'): [('person',
                                                                                                                 'elder')],
 ('the family in the flat below', "pay for the children's school trip, so they are not left out"): [('means',
                                                                                                     'money-.03')],
 ('the family in the flat below', 'show the parents how the forms work, step by step, until they can do them alone'): [('mark',
                                                                                                                        'helped '
                                                                                                                        'someone '
                                                                                                                        'in '
                                                                                                                        'need')],
 ('the metal under the hills', 'ask the town meeting to set one fair rent for every new hand in the camp'): [('place',
                                                                                                              'rule.voice')],
 ('the metal under the hills', 'work out how long the seam will last, then decide what to stake on it'): [('lesson',
                                                                                                           'every '
                                                                                                           'boom has '
                                                                                                           'an end')],
 ('the metal under the hills', 'lease your field to the company at the new price, and bank every payment'): [('means',
                                                                                                              'money+.10')],
 ('the metal under the hills', 'dig in on the ranch, and let the company build round you'): [('door', 'stayed home')],
 ('the metal under the hills', 'work double shifts for a year, spend freely, and get out before the bust'): [('means',
                                                                                                              'health-.06')],
 ('the metal under the hills', 'guide the prospectors over the hills you know by heart, for a fee'): [('means',
                                                                                                       'money+.03')],
 ('the metal under the hills', 'count the springs on the old range, and show the council what the digging does'): [('place',
                                                                                                                    'rule.counsel')],
 ('the metal under the hills', 'open a boarding house for the new hands, with fair rent and clean beds'): [('place',
                                                                                                            'gather.house')],
 ('the metal under the hills', "get yourself trained as the mine's safety inspector"): [('mark', 'learned a skill')],
 ('the plant moves its line abroad', "buy two old machines at the auction, and take orders from the plant's customers"): [('place',
                                                                                                                           'prod.craft')],
 ('the plant moves its line abroad', 'stay and scrape by, so the family is still here when work comes back'): [('means',
                                                                                                                'money-.06')],
 ('the plant moves its line abroad', "fix the neighbours' cars and boilers by hand in your garage, a job at a time"): [('means',
                                                                                                                        'money+.03')],
 ('the plant moves its line abroad', 'find out who is buying the line, and sell them what only you know about it'): [('means',
                                                                                                                      'money+.06')],
 ('the plant moves its line abroad', 'write down how the old line ran, so the skill is not lost with the plant'): [('lesson',
                                                                                                                    'skill '
                                                                                                                    'lives '
                                                                                                                    'on '
                                                                                                                    'in '
                                                                                                                    'writing')],
 ('the plant moves its line abroad', 'put your payout into a small firm that hires the old crew'): [('means',
                                                                                                     'money-.10')],
 ('the third week on the picket line', 'show the crew what the offer is worth against prices, month by month'): [('lesson',
                                                                                                                  'the '
                                                                                                                  'figures '
                                                                                                                  'speak '
                                                                                                                  'plainly')],
 ('the third week on the picket line', 'keep the brazier going every night, and lead the songs at the gate'): [('person',
                                                                                                                'friend')],
 ('the third week on the picket line', 'bring the young hands to the gate, and tell them how the last strike was won'): [('means',
                                                                                                                          'ties+.03')],
 ('the third week on the picket line', 'take cleaning work across town to see the family through, and say so openly'): [('means',
                                                                                                                         'money+.03')],
 ('the third week on the picket line', "spend the strike weeks mending the neighbours' roofs and fences for food and favours"): [('person',
                                                                                                                                  'neighbour')],
 ('the third week on the picket line', 'find out quietly how long the firm can run on the skeleton shift'): [('lesson',
                                                                                                              'every '
                                                                                                              'side '
                                                                                                              'has '
                                                                                                              'its '
                                                                                                              'limit')],
 ('the third week on the picket line', "join the union team that checks the firm's books and drafts a fair counter-offer"): [('place',
                                                                                                                              'rule.counsel')],
 ('the scaffolding comes down', 'give the inspectors a full statement of everything you saw on the site'): [('door',
                                                                                                             'made '
                                                                                                             'an '
                                                                                                             'enemy')],
 ('the scaffolding comes down', 'photograph the clamps and the failed joints before the firm clears them away'): [('lesson',
                                                                                                                   'proof '
                                                                                                                   'outlasts '
                                                                                                                   'memory')],
 ('the scaffolding comes down', "finish the job on time, take the firm's bonus, and keep your head down"): [('means',
                                                                                                             'money+.06')],
 ('the scaffolding comes down', 'walk off the site for good, and find work in another trade'): [('person',
                                                                                                 'colleague lost')],
 ('the scaffolding comes down', 'go back on Monday, and check every clamp you climb on yourself'): [('lesson',
                                                                                                     'check it '
                                                                                                     'yourself every '
                                                                                                     'time')],
 ('the scaffolding comes down', 'sign on with a better-paid crew on a safer site across town'): [('means',
                                                                                                  'money+.06')],
 ('the scaffolding comes down', 'teach the young hands on the site how to check a scaffold before they climb'): [('person',
                                                                                                                  'colleague')],
 ('the scaffolding comes down', "stand as the site's safety rep, with the right to stop the job"): [('place',
                                                                                                     'rule.counsel')],
 ('the last family farm in the valley', 'take the offer only if the firm keeps on every hand who works the farm'): [('mark',
                                                                                                                     'helped '
                                                                                                                     'someone '
                                                                                                                     'in '
                                                                                                                     'need')],
 ('the last family farm in the valley', 'work out what the farm could earn with new crops, then answer'): [('lesson',
                                                                                                            'land '
                                                                                                            'has '
                                                                                                            'more '
                                                                                                            'than '
                                                                                                            'one '
                                                                                                            'use')],
 ('the last family farm in the valley', 'bargain the offer up, sell, and buy a smaller farm in another valley'): [('mark',
                                                                                                                   'moved '
                                                                                                                   'away')],
 ('the last family farm in the valley', 'turn the offer down, and keep the farm for the children'): [('door',
                                                                                                      'stayed home')],
 ('the last family farm in the valley', 'keep the orchard worked by hand, and sell the fruit at the farm gate'): [('means',
                                                                                                                   'money+.03')],
 ('the last family farm in the valley', 'find out what the firm truly needs your land for, and price it to match'): [('means',
                                                                                                                      'money+.10')],
 ('the last family farm in the valley', 'turn the farm into something the firm cannot copy, a cider press or a farm shop'): [('place',
                                                                                                                              'comm.shop')],
 ('the last family farm in the valley', "buy the neighbour's last field before the firm can, and hire their hands"): [('means',
                                                                                                                       'money-.10')],
 ('the last family farm in the valley', 'get the last farmers to pool their land and farm it together'): [('place',
                                                                                                           'prod.land')],
 ('a title to the fields your family worked', 'ask the land office to put the day labourers on the list too'): [('mark',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('a title to the fields your family worked', 'plant what you always wanted to grow, and work the hours you choose'): [('means',
                                                                                                                        'freedom+.06')],
 ('a title to the fields your family worked', 'hold a family supper in the barn, and give the old hands the first toast'): [('means',
                                                                                                                             'ties+.03')],
 ('a title to the fields your family worked', "sell the far field to clear the family's debts, and farm the rest well"): [('means',
                                                                                                                           'money+.06')],
 ('a title to the fields your family worked', 'learn which crop the town will pay most for, before the neighbours do'): [('place',
                                                                                                                          'comm.market')],
 ('a title to the fields your family worked', 'try a crop nobody in the valley has grown, on one field'): [('lesson',
                                                                                                            'try '
                                                                                                            'small '
                                                                                                            'before '
                                                                                                            'going '
                                                                                                            'big')],
 ('a title to the fields your family worked', 'share the plough and the harvest work with the families on either side'): [('person',
                                                                                                                           'neighbour')],
 ('a title to the fields your family worked', 'stand with the families whose titles the old estate is fighting in court'): [('place',
                                                                                                                             'rule.voice')],
 ('the boats tied up in the harbour', 'keep the closure, and report the boats that slip out at night'): [('person',
                                                                                                          'rival')],
 ('the boats tied up in the harbour', 'sign on with the scientists to count the fish through the closed years'): [('place',
                                                                                                                   'prod.wild')],
 ('the boats tied up in the harbour', 'sell the boat up the coast now, while it still fetches a price'): [('means',
                                                                                                           'money+.10')],
 ('the boats tied up in the harbour', 'keep the boat painted and ready for the day the fishery opens again'): [('door',
                                                                                                                'stayed '
                                                                                                                'home')],
 ('the boats tied up in the harbour', 'strip the old boats for engines and timber, and sell what can be sold'): [('means',
                                                                                                                  'money+.06')],
 ('the boats tied up in the harbour', 'refit your boat to take visitors out to see the seals'): [('means',
                                                                                                  'money-.06')],
 ('the boats tied up in the harbour', 'lend the crews out of work enough to see them through the first winter'): [('door',
                                                                                                                   'helped '
                                                                                                                   'someone '
                                                                                                                   'in '
                                                                                                                   'need')],
 ('the boats tied up in the harbour', 'lead the crews to the harbour office to demand help for the families'): [('place',
                                                                                                                 'rule.voice')],
 ('the count comes back rising', "ask the meeting to check every boat's landings the same way, your own first"): [('place',
                                                                                                                   'rule.counsel')],
 ('the count comes back rising', 'bring your four years of catch logs to the next count'): [('lesson',
                                                                                             'careful records earn '
                                                                                             'trust')],
 ('the count comes back rising', 'buy up the quota of a crew that is retiring, before the limits rise'): [('means',
                                                                                                           'money-.10')],
 ('the count comes back rising', 'take the boat out past the point for one long trip, within your share'): [('lesson',
                                                                                                             'the '
                                                                                                             'open '
                                                                                                             'water '
                                                                                                             'still '
                                                                                                             'calls')],
 ('the count comes back rising', 'take the youngest of the family out on the first good trip to the old grounds'): [('means',
                                                                                                                     'ties+.03')],
 ('the count comes back rising', 'fish every day the season allows, and spend the summer as you please'): [('means',
                                                                                                            'money+.06')],
 ('the count comes back rising', 'keep your best grounds to yourself until the new limits are set'): [('door',
                                                                                                       'kept it '
                                                                                                       'hidden')],
 ('the count comes back rising', "help the scientists tag the young fish, so next year's count is truer"): [('place',
                                                                                                             'prod.wild')],
 ('the count comes back rising', 'land your catch together with the small boats, so all get the same price'): [('place',
                                                                                                                'comm.market')],
 ('a sign in every window', 'ask for the same raise for every hand on the team, not only yourself'): [('means',
                                                                                                       'ties+.03')],
 ('a sign in every window', 'name a high figure and a say in the rota, and get it in writing'): [('means',
                                                                                                  'money+.06')],
 ('a sign in every window', 'walk out, and take the best-paid job going across town'): [('person', 'boss lost')],
 ('a sign in every window', 'stay on at the old rate, and help the farm bring in the harvest'): [('means',
                                                                                                  'money-.03')],
 ('a sign in every window', 'work two jobs at the new rates for a year, and spend it on living well'): [('means',
                                                                                                         'time-.06')],
 ('a sign in every window', 'cook by eye and by the day, for whichever kitchen pays most'): [('means',
                                                                                              'freedom+.06')],
 ('a sign in every window', 'find out what every kitchen in town is paying, then bargain'): [('means', 'money+.03')],
 ('a sign in every window', 'bring in friends and neighbours to share the harvest work for fair pay'): [('place',
                                                                                                         'prod.land')],
 ('a sign in every window', 'help draw up a fair pay scale for the trade in town, posted for all'): [('place',
                                                                                                      'rule.counsel')],
 ("the cooperative's own cheese plant", 'sell every load through the cooperative, even in a month the buyer pays more'): [('mark',
                                                                                                                           'kept '
                                                                                                                           'your '
                                                                                                                           'word')],
 ("the cooperative's own cheese plant", "keep the cooperative's books, and post the figures every month"): [('means',
                                                                                                             'time-.03')],
 ("the cooperative's own cheese plant", 'put your savings into extra shares while they are cheap'): [('means',
                                                                                                      'money-.06')],
 ("the cooperative's own cheese plant", 'help build the plant with your own hands, weekends and all'): [('person',
                                                                                                         'friend')],
 ("the cooperative's own cheese plant", 'bring your children to the meetings, so they learn how it is run'): [('lesson',
                                                                                                               'the '
                                                                                                               'young '
                                                                                                               'keep '
                                                                                                               'what '
                                                                                                               'they '
                                                                                                               'see')],
 ("the cooperative's own cheese plant", "drive the cooperative's cheese to the city markets yourself, and sell it hard"): [('place',
                                                                                                                            'comm.market')],
 ("the cooperative's own cheese plant", 'build a cheaper way to cool the milk on the farms, and show the members'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ("the cooperative's own cheese plant", 'stand for the board, and see that the small farms get the same as the large'): [('place',
                                                                                                                          'rule.counsel')],
 ("the cooperative's own cheese plant", "share the milk run with the neighbours, so no farm's load is left behind"): [('person',
                                                                                                                       'neighbour')],
 ('overtime for the war abroad', 'ask the union to set a limit on the weekend hours for everyone'): [('means',
                                                                                                      'time+.03')],
 ('overtime for the war abroad', 'ask the engineers exactly what the new parts are for'): [('lesson',
                                                                                            'know what your work '
                                                                                            'makes')],
 ('overtime for the war abroad', 'take every weekend of overtime, and clear the loan by spring'): [('means',
                                                                                                    'money+.10')],
 ('overtime for the war abroad', 'quit the plant, and join the protesters at the gate'): [('place', 'rule.voice')],
 ('overtime for the war abroad', "keep the plant's old customers supplied on the side, for when the war ends"): [('person',
                                                                                                                  'regular')],
 ('overtime for the war abroad', 'take the overtime as it comes, and save it all for when the orders stop'): [('means',
                                                                                                               'money+.06')],
 ('overtime for the war abroad', 'sign on for the double shifts, and spend the pay as fast as it comes'): [('means',
                                                                                                            'health-.06')],
 ('overtime for the war abroad', 'rig up a faster way to make the new part, just to see if it works'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('overtime for the war abroad', 'set up a rota so the weekend shifts are shared fairly across the floor'): [('person',
                                                                                                              'colleague')],
 ('overtime for the war abroad', 'check every new part against the standard, however fast the orders come'): [('lesson',
                                                                                                               'careful '
                                                                                                               'work '
                                                                                                               'outlasts '
                                                                                                               'the '
                                                                                                               'rush')],
 ("the valley's oil in the papers", 'press only what meets the old standard, however many orders come'): [('means',
                                                                                                           'money-.06')],
 ("the valley's oil in the papers", 'send the oil to be tested, and learn what makes it the best'): [('mark',
                                                                                                      'learned a '
                                                                                                      'skill')],
 ("the valley's oil in the papers", "raise your price, and sign the city shop's biggest order"): [('means',
                                                                                                   'money+.10')],
 ("the valley's oil in the papers", 'open a stall at the press for the visitors, with tastings and music'): [('place',
                                                                                                              'comm.market')],
 ("the valley's oil in the papers", 'teach the young of the family the old pressing, before the rush changes it'): [('lesson',
                                                                                                                     'skills '
                                                                                                                     'pass '
                                                                                                                     'on '
                                                                                                                     'by '
                                                                                                                     'hand')],
 ("the valley's oil in the papers", 'keep the grove as it is, and sell only the land you cannot work'): [('means',
                                                                                                          'money+.06')],
 ("the valley's oil in the papers", 'pick by hand on the morning the fruit feels right, as the old ones did'): [('place',
                                                                                                                 'prod.land')],
 ("the valley's oil in the papers", 'try a new pressing of your own, and enter it at the fair'): [('place',
                                                                                                   'gather.great')],
 ("the valley's oil in the papers", 'build a shared press the small growers can use at a fair rate'): [('person',
                                                                                                        'neighbour')],
 ("the valley's oil in the papers", "help write a mark that only the valley's true oil may carry"): [('place',
                                                                                                      'rule.counsel')],
 ('the school bus leaves half empty', 'stay, and take on the shared harvest work the young have left behind'): [('means',
                                                                                                                 'time-.06')],
 ('the school bus leaves half empty', 'weigh the city wages against the city rents, and only then decide'): [('lesson',
                                                                                                              'count '
                                                                                                              'the '
                                                                                                              'rent '
                                                                                                              'before '
                                                                                                              'the '
                                                                                                              'wage')],
 ('the school bus leaves half empty', 'go to the city with one bag and no plan, and see what happens'): [('mark',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the school bus leaves half empty', 'stay, and take on the farm from your parent'): [('place', 'prod.land')],
 ('the school bus leaves half empty', 'work the city season, and come home flush for the winter'): [('means',
                                                                                                     'money+.06')],
 ('the school bus leaves half empty', 'learn a skill the city pays for, and sell it from the valley online'): [('mark',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ('the school bus leaves half empty', 'help the families who stayed share the work of the farms that lost their young'): [('person',
                                                                                                                           'neighbour')],
 ('the school bus leaves half empty', 'campaign to keep the valley school open, though the bus is half empty'): [('place',
                                                                                                                  'rule.voice')],
 ('four of the old crew in a rented unit', 'join on a fair wage, and help your friend set the safety rules from day one'): [('place',
                                                                                                                             'prod.craft')],
 ('four of the old crew in a rented unit', 'join as the one who works out how to make the product better and cheaper'): [('place',
                                                                                                                          'prod.craft')],
 ('four of the old crew in a rented unit', 'quit the safe job on Friday, and start at the unit on Monday'): [('mark',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ('four of the old crew in a rented unit', "keep the safe job for the family's sake, and help at the unit on Saturdays"): [('means',
                                                                                                                            'time-.03')],
 ('four of the old crew in a rented unit', "join, but keep your savings out of it until the first year's books are in"): [('place',
                                                                                                                           'prod.craft')],
 ('four of the old crew in a rented unit', 'take piece work from the new firm, and keep your own hours'): [('means',
                                                                                                            'freedom+.06')],
 ('four of the old crew in a rented unit', "build the unit's first machine from parts out of the old plant"): [('mark',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ('four of the old crew in a rented unit', "set up the firm's quality checks, so its first orders go out right"): [('lesson',
                                                                                                                    'first '
                                                                                                                    'orders '
                                                                                                                    'make '
                                                                                                                    'the '
                                                                                                                    'name')],
 ('the van that keeps circling', 'ring the police and report the van, its plate and the times'): [('lesson',
                                                                                                   'the number is '
                                                                                                   'there to ring')],
 ('the van that keeps circling', "keep a log of the van's times for a week before saying anything"): [('lesson',
                                                                                                       'a week of '
                                                                                                       'notes tells '
                                                                                                       'all')],
 ('the van that keeps circling', "take what you saw to the depot's owner, and make sure they know who spotted it"): [('person',
                                                                                                                      'patron')],
 ('the van that keeps circling', 'tell the neighbours and the other shops on the street to keep an eye out'): [('person',
                                                                                                                'neighbour')],
 ('the van that keeps circling', 'stay late with two neighbours and stand by the gate when the bags go out'): [('person',
                                                                                                                'friend')],
 ('the van that keeps circling', 'have a quiet word with the guard firm that collects the takings'): [('person',
                                                                                                       'go-between')],
 ('the van that keeps circling', "photograph the van's plate as it passes, and send it in that night"): [('mark',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the van that keeps circling', 'ask the manager to change the collection time and the route, and log it'): [('person',
                                                                                                               'boss')],
 ('the van that keeps circling', 'ring the police, then knock on every door on the street that evening'): [('means',
                                                                                                            'ties+.06')],
 ('the city is surrounded', 'trade the spare batteries you put by for food and favours'): [('means', 'health+.03')],
 ('the city is surrounded', 'keep the family in the flat, and share only with the neighbours you know'): [('means',
                                                                                                           'ties-.03')],
 ('the city is surrounded', 'plant beans and herbs in every window box and in the courtyard'): [('lesson',
                                                                                                 'even a window box '
                                                                                                 'can feed')],
 ('the city is surrounded', 'patch up the old generator so the stairwell has light at night'): [('mark',
                                                                                                 'learned a skill')],
 ('the city is surrounded', "get the council to pay the building's volunteers in food, and keep the books"): [('place',
                                                                                                               'rule.counsel')],
 ('the ceasefire holds', 'go to the service for the ones who did not come back'): [('lesson',
                                                                                    'some grief is shared out loud')],
 ('the ceasefire holds', 'meet the evening train with a crowd of friends and a great deal of noise'): [('person',
                                                                                                        'friend')],
 ('the ceasefire holds', 'cook the homecoming meal and set every place at the table'): [('means', 'ties+.03')],
 ('the ceasefire holds', 'find the returning reservists work, for a fee from the firms that hire them'): [('means',
                                                                                                           'money+.06')],
 ('the ceasefire holds', 'give the one who came home time and quiet, and listen when they want to talk'): [('means',
                                                                                                            'time-.03')],
 ('the ceasefire holds', "help run the council's desk that finds each returning reservist a post"): [('place',
                                                                                                      'rule.counsel')],
 ('the ceasefire holds', 'speak at the town meeting for keeping the peace when the hard voices start'): [('place',
                                                                                                          'rule.voice')],
 ('home from service for good', "go with them to the veterans' office and sort out every form they are owed"): [('person',
                                                                                                                 'go-between')],
 ('home from service for good', 'find out which courses the study grant pays for, and help them choose'): [('lesson',
                                                                                                            'good '
                                                                                                            'help '
                                                                                                            'starts '
                                                                                                            'with '
                                                                                                            'the '
                                                                                                            'facts')],
 ('home from service for good', "get them taken on at a guard firm where a soldier's skills pay well"): [('door',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('home from service for good', 'take them out to the old places with the old crowd, just like before'): [('place',
                                                                                                           'gather.circle')],
 ('home from service for good', 'keep a place at the table for them every Sunday, and ask nothing'): [('place',
                                                                                                       'gather.house')],
 ('home from service for good', 'help them put the grant into a small trade of their own near home'): [('place',
                                                                                                        'comm.shop')],
 ('home from service for good', 'go into business with them: a removals van, two strong backs and no boss'): [('means',
                                                                                                               'money+.06')],
 ('home from service for good', 'walk the hills with them on Saturdays, and let them talk or not'): [('place',
                                                                                                      'prod.wild')],
 ('home from service for good', 'stand up for them at the clinic until they are seen sooner'): [('mark',
                                                                                                 'helped someone in '
                                                                                                 'need')],
 ('home from service for good', "join the veterans' group at the hall and help run its evenings"): [('place',
                                                                                                     'gather.hall')],
 ('a night guard for the main street', 'draw up one fair rule for what each shop pays and what the guard covers'): [('lesson',
                                                                                                                     'a '
                                                                                                                     'fair '
                                                                                                                     'rule '
                                                                                                                     'holds '
                                                                                                                     'a '
                                                                                                                     'street')],
 ('a night guard for the main street', 'bid for the job at a proper price, and run it as a business'): [('means',
                                                                                                         'money+.06')],
 ('a night guard for the main street', 'take the night shift yourself and walk the street until dawn'): [('place',
                                                                                                          'prot.watch')],
 ('a night guard for the main street', 'pay your share and keep a light on in your window at night'): [('means',
                                                                                                        'money-.03')],
 ('a night guard for the main street', 'start a small guard crew of your own with two friends and a van'): [('means',
                                                                                                             'freedom+.06')],
 ('a night guard for the main street', 'get a cheaper rate from the big guard firm by sharing it with the next street'): [('means',
                                                                                                                           'money+.03')],
 ('a night guard for the main street', 'set up a phone tree between the guard and the flats above the shops'): [('means',
                                                                                                                 'ties+.06')],
 ('a night guard for the main street', 'collect the money door to door and keep the book of who has paid'): [('person',
                                                                                                              'neighbour')],
 ('a night guard for the main street', 'speak up for the corner shop that cannot pay, and cover its share'): [('means',
                                                                                                               'money-.06')],
 ('the new radios and phone maps', 'test the maps on your own beat and write up where they go wrong'): [('mark',
                                                                                                         'learned a '
                                                                                                         'skill')],
 ('the new radios and phone maps', 'ask for the new specialist post, and the pay that comes with it'): [('means',
                                                                                                         'money+.06')],
 ('the new radios and phone maps', 'keep your own way of working, and trust your feet over the screen'): [('door',
                                                                                                           'turned '
                                                                                                           'down a '
                                                                                                           'chance')],
 ('the new radios and phone maps', 'teach the volunteer crews in your patch to use the new kit'): [('place',
                                                                                                    'prot.rescue')],
 ('the new radios and phone maps', "train the neighbours' watch on the radios, for a modest fee"): [('means',
                                                                                                     'money+.03')],
 ('the new radios and phone maps', 'sell the station a better way to use the maps, and take the credit'): [('person',
                                                                                                            'rival')],
 ('the new radios and phone maps', 'build a faster call-out plan with the new kit, and try it on the night shift'): [('mark',
                                                                                                                      'took '
                                                                                                                      'a '
                                                                                                                      'wild '
                                                                                                                      'risk')],
 ('the new radios and phone maps', 'pair each new recruit with an old hand who knows the streets'): [('means',
                                                                                                      'ties+.03')],
 ('the new radios and phone maps', 'take the first night out with the new kit, and show the doubters it works'): [('lesson',
                                                                                                                   'a '
                                                                                                                   'working '
                                                                                                                   'night '
                                                                                                                   'wins '
                                                                                                                   'doubters')],
 ('officers on foot on the estate', 'apply to join the new team, and take the oath'): [('place', 'prot.watch')],
 ('officers on foot on the estate', 'tell the officer which corners, which hours, and which doors to knock on'): [('lesson',
                                                                                                                   'the '
                                                                                                                   'estate '
                                                                                                                   'knows '
                                                                                                                   'its '
                                                                                                                   'own '
                                                                                                                   'corners')],
 ('officers on foot on the estate', 'ask the council what the posts pay, and apply for the best of them'): [('means',
                                                                                                             'money+.06')],
 ('officers on foot on the estate', 'keep your distance, and wait to see if they last the year'): [('means',
                                                                                                    'ties-.03')],
 ('officers on foot on the estate', 'ask the officer in for tea and introduce her to the neighbours'): [('person',
                                                                                                         'friend')],
 ('officers on foot on the estate', 'join the team as the one who goes in first, for the overtime'): [('place',
                                                                                                       'prot.watch'),
                                                                                                      ('mark',
                                                                                                       'took a wild '
                                                                                                       'risk')],
 ('officers on foot on the estate', 'offer to sit on the panel that checks how the team is doing'): [('place',
                                                                                                      'rule.counsel')],
 ('officers on foot on the estate', "sign up for the residents' group that meets the team every month"): [('place',
                                                                                                           'gather.hall')],
 ('officers on foot on the estate', "help the team write down the estate's worries, block by block"): [('means',
                                                                                                        'ties+.06')],
 ('break-ins on your side of town', 'report everything to the police, and press them to send a patrol'): [('lesson',
                                                                                                           'pressing '
                                                                                                           'keeps '
                                                                                                           'them '
                                                                                                           'coming')],
 ('break-ins on your side of town', 'work out the pattern in the break-ins and post it for the street'): [('means',
                                                                                                           'ties+.03')],
 ('break-ins on your side of town', 'pay for a proper alarm, and start looking at houses in a safer part of town'): [('means',
                                                                                                                      'money-.06')],
 ('break-ins on your side of town', 'stay up at the window at night, ready to shout the street awake'): [('means',
                                                                                                          'health-.03')],
 ('break-ins on your side of town', "knock on the older neighbours' doors each evening, and check they are locked up"): [('person',
                                                                                                                          'neighbour')],
 ('break-ins on your side of town', 'hire a guard firm together with three other houses, and share the cost'): [('means',
                                                                                                                 'money-.03')],
 ('break-ins on your side of town', 'put up a camera of your own, and send the clips straight to the police'): [('lesson',
                                                                                                                 'a '
                                                                                                                 'camera '
                                                                                                                 'sees '
                                                                                                                 'what '
                                                                                                                 'neighbours '
                                                                                                                 'miss')],
 ('break-ins on your side of town', 'press the council in writing for street lights and a patrol'): [('place',
                                                                                                      'rule.voice')],
 ('break-ins on your side of town', "speak up for the new family when the street's chat blames them"): [('person',
                                                                                                         'friend')],
 ('a crew collecting from the late shops', 'go to the police with what you saw, and give a statement'): [('door',
                                                                                                          'made an '
                                                                                                          'enemy')],
 ('a crew collecting from the late shops', 'write down their car, their times and their faces, and keep it somewhere safe'): [('door',
                                                                                                                               'kept '
                                                                                                                               'it '
                                                                                                                               'hidden')],
 ('a crew collecting from the late shops', 'tell your boss to pay for now, and keep your own head down'): [('door',
                                                                                                            'gave in '
                                                                                                            'to '
                                                                                                            'pressure')],
 ('a crew collecting from the late shops', 'ask the other shopkeepers round to a meeting in the back room'): [('place',
                                                                                                               'comm.shop')],
 ('a crew collecting from the late shops', 'move the takings out each evening, and close the shop an hour earlier'): [('means',
                                                                                                                       'money-.06')],
 ('a crew collecting from the late shops', 'get the neighbours to fit a camera that covers every door on the parade'): [('lesson',
                                                                                                                         'many '
                                                                                                                         'doors '
                                                                                                                         'watched '
                                                                                                                         'are '
                                                                                                                         'safer')],
 ('a crew collecting from the late shops', 'get the shops to hire one licensed guard together, on the books'): [('means',
                                                                                                                 'money-.03')],
 ('a crew collecting from the late shops', 'walk with all the shopkeepers to the station together, and report it as one'): [('means',
                                                                                                                             'ties+.06')],
 ('the camp in the square is cleared', 'go to the station and ask, properly, what your friend is charged with'): [('lesson',
                                                                                                                   'asking '
                                                                                                                   'properly '
                                                                                                                   'gets '
                                                                                                                   'answers')],
 ('the camp in the square is cleared', 'gather the videos and the witnesses, and set out what happened in order'): [('door',
                                                                                                                     'helped '
                                                                                                                     'someone '
                                                                                                                     'in '
                                                                                                                     'need')],
 ('the camp in the square is cleared', 'stay well out of it, since a name on a list does nobody any good'): [('door',
                                                                                                              'refused '
                                                                                                              'someone '
                                                                                                              'in '
                                                                                                              'need')],
 ('the camp in the square is cleared', 'find your friend a lawyer, and be waiting at the door when they come out'): [('mark',
                                                                                                                      'helped '
                                                                                                                      'someone '
                                                                                                                      'in '
                                                                                                                      'need')],
 ('the camp in the square is cleared', "keep your head down at work, and send your friend's family money for the fines"): [('means',
                                                                                                                            'money-.06')],
 ('the camp in the square is cleared', 'quietly pass the videos to a journalist who knows what to do with them'): [('person',
                                                                                                                    'go-between')],
 ('the camp in the square is cleared', 'stand at the front of the crowd outside the station and demand the arrests be explained'): [('mark',
                                                                                                                                     'defied '
                                                                                                                                     'an '
                                                                                                                                     'authority')],
 ('the camp in the square is cleared', 'lodge a formal complaint with the board that oversees the police'): [('place',
                                                                                                              'rule.voice')],
 ('more patrols and more stops', 'carry your papers, answer every stop politely, and keep a note of each one'): [('lesson',
                                                                                                                  'keep '
                                                                                                                  'calm '
                                                                                                                  'and '
                                                                                                                  'keep '
                                                                                                                  'records')],
 ('more patrols and more stops', "collect the street's stories of the stops and send them to the council"): [('place',
                                                                                                              'rule.voice')],
 ('more patrols and more stops', 'take the new job at the prison while it is hiring'): [('means', 'money+.06')],
 ('more patrols and more stops', 'keep the young ones in the family close, and off the corners after dark'): [('means',
                                                                                                               'ties+.03')],
 ('more patrols and more stops', "visit the cousin inside every month, and keep the family's place for them"): [('means',
                                                                                                                 'time-.06')],
 ('more patrols and more stops', 'find your cousin the best lawyer in town, and pay whatever it takes'): [('means',
                                                                                                           'money-.10')],
 ('more patrols and more stops', 'set up a map online of every stop on the street, and share it'): [('door',
                                                                                                     'defied an '
                                                                                                     'authority')],
 ('more patrols and more stops', "ask the beat officer to the residents' meeting, so both sides can talk"): [('person',
                                                                                                              'go-between')],
 ('more patrols and more stops', 'write to your representative with the numbers, asking for the rules to be reviewed'): [('lesson',
                                                                                                                          'numbers '
                                                                                                                          'make '
                                                                                                                          'a '
                                                                                                                          'letter '
                                                                                                                          'heard')],
 ('the street starts its own watch', 'draw up the map and the phone tree for the whole street'): [('means',
                                                                                                   'ties+.06')],
 ('the street starts its own watch', 'get the local businesses to pay for the signs and the radios'): [('person',
                                                                                                        'patron')],
 ('the street starts its own watch', 'walk the late round on the worst nights, torch in hand'): [('place',
                                                                                                  'prot.watch')],
 ('the street starts its own watch', 'become the one the rota calls when something needs doing fast'): [('mark',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('the street starts its own watch', 'lead the rota, and keep the list of who walks when'): [('place', 'prot.watch')],
 ('the street starts its own watch', 'keep a log of every call and pass it to the beat officer each month'): [('person',
                                                                                                               'go-between')],
 ('lights and cameras on the estate', "thank the council for the lights at the residents' meeting"): [('lesson',
                                                                                                       'thanks are '
                                                                                                       'remembered '
                                                                                                       'too')],
 ('lights and cameras on the estate', 'ask the council in writing who sees the footage, and for how long'): [('place',
                                                                                                              'rule.voice')],
 ('lights and cameras on the estate', 'fit a good lock and a light of your own, and leave the cameras to others'): [('means',
                                                                                                                     'money-.03')],
 ('lights and cameras on the estate', 'strike a deal with the council: lights on the lane, no cameras on the doors'): [('person',
                                                                                                                        'go-between')],
 ('lights and cameras on the estate', 'test whether the cameras really see the back lane, and post what you find'): [('lesson',
                                                                                                                      'see '
                                                                                                                      'for '
                                                                                                                      'yourself '
                                                                                                                      'before '
                                                                                                                      'trusting')],
 ('lights and cameras on the estate', 'get a seat on the panel the council sets up to oversee the cameras'): [('place',
                                                                                                               'rule.counsel')],
 ('lights and cameras on the estate', 'read the rules on the cameras and explain them to the neighbours'): [('means',
                                                                                                             'ties+.03')],
 ('a college inside the prison', "write to the governor in support of your sibling's place on the course"): [('door',
                                                                                                              'helped '
                                                                                                              'someone '
                                                                                                              'in '
                                                                                                              'need')],
 ('a college inside the prison', 'find out what the course leads to, and which trades take people with records'): [('lesson',
                                                                                                                    'a '
                                                                                                                    'way '
                                                                                                                    'back '
                                                                                                                    'can '
                                                                                                                    'be '
                                                                                                                    'found')],
 ('a college inside the prison', 'put money by each month, so your sibling has a start when they come out'): [('means',
                                                                                                               'money-.06')],
 ('a college inside the prison', 'get on the bus to the prison this weekend, the first time in a year'): [('means',
                                                                                                           'ties+.03')],
 ('a college inside the prison', 'clear the spare room for the day they come home'): [('door', 'took them in')],
 ('a college inside the prison', 'offer them a start in your own work when they are out, at a fair wage'): [('door',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('a college inside the prison', 'gather the whole family to visit together, the first time in years'): [('means',
                                                                                                          'ties+.06')],
 ('a college inside the prison', 'send them books and plans for the joinery course every month'): [('means',
                                                                                                    'money-.03')],
 ('a college inside the prison', 'talk to the probation officer about the terms of an early release'): [('person',
                                                                                                         'go-between')],
 ('the army splits', 'refuse to take a side, and say so to anyone who asks'): [('mark', 'defied an authority')],
 ('the army splits', 'keep the roads out mapped and the papers ready, in case you must go'): [('lesson',
                                                                                               'a packed bag brings '
                                                                                               'calm')],
 ('the army splits', 'deal with whichever side holds the street this week'): [('door', 'gave in to pressure')],
 ('the army splits', 'keep your head down, stock the cupboards, and bring your own through it'): [('means',
                                                                                                   'money-.06')],
 ('the army splits', "take the family to the grandparents' village in the hills, away from the lines"): [('mark',
                                                                                                          'moved '
                                                                                                          'away')],
 ('the army splits', 'stand up at the town meeting against neighbours turning on neighbours'): [('place',
                                                                                                 'rule.voice')],
 ('the army splits', 'volunteer with the relief agency that takes food across both lines'): [('place',
                                                                                              'prot.rescue')],
 ('your name in the leaked files', 'join the legal claim against the city for the tracking'): [('place',
                                                                                                'rule.voice')],
 ('your name in the leaked files', 'ask for your full file, and read every page of it'): [('lesson',
                                                                                           'the whole file tells '
                                                                                           'more')],
 ('your name in the leaked files', 'sell your story to the paper that is running the leak'): [('means', 'money+.06')],
 ('your name in the leaked files', "go round to your friend's house tonight and have it out"): [('person',
                                                                                                 'friend lost')],
 ('your name in the leaked files', 'ask your friend over, and hear them out before judging'): [('lesson',
                                                                                                'people have their '
                                                                                                'reasons')],
 ('your name in the leaked files', 'change phones, change habits, and say nothing to anyone'): [('means',
                                                                                                 'freedom-.03')],
 ('your name in the leaked files', 'laugh about the file over a long night with the friends from the march'): [('place',
                                                                                                                'gather.circle')],
 ('your name in the leaked files', 'find out who else your friend reported on, and keep it to yourself for now'): [('door',
                                                                                                                    'kept '
                                                                                                                    'it '
                                                                                                                    'hidden')],
 ('your name in the leaked files', 'stand up at the public hearing and read out what the file said'): [('mark',
                                                                                                        'defied an '
                                                                                                        'authority')],
 ('your name in the leaked files', 'help the group going through the files to warn everyone named in them'): [('mark',
                                                                                                               'helped '
                                                                                                               'someone '
                                                                                                               'in '
                                                                                                               'need')],
 ('a feud spills into the street', 'ask the beat officer to talk to both sides before something happens'): [('person',
                                                                                                             'go-between')],
 ('a feud spills into the street', 'find the post that started it, and show both sides what was really said'): [('lesson',
                                                                                                                 'most '
                                                                                                                 'rows '
                                                                                                                 'start '
                                                                                                                 'smaller '
                                                                                                                 'than '
                                                                                                                 'told')],
 ('a feud spills into the street', 'broker a quiet deal with the one you know on the other side'): [('door',
                                                                                                     'kept your '
                                                                                                     'word')],
 ('a feud spills into the street', 'keep your sibling home and away from the other estate until it cools'): [('means',
                                                                                                              'time-.03')],
 ('a feud spills into the street', 'get your sibling a job well away from the crew, and keep them close'): [('door',
                                                                                                             'helped '
                                                                                                             'someone '
                                                                                                             'in '
                                                                                                             'need')],
 ('a feud spills into the street', 'stand by your sibling every day, and refuse to join in anything'): [('lesson',
                                                                                                         'you can '
                                                                                                         'stand by '
                                                                                                         'without '
                                                                                                         'joining')],
 ('a feud spills into the street', 'post how it really started, and dare both sides to read it'): [('person',
                                                                                                    'rival')],
 ('a feud spills into the street', 'get the elders of both families round one table, with tea and a deal'): [('person',
                                                                                                              'elder')],
 ('a feud spills into the street', 'take it to the youth worker who knows both crews, and help them settle it'): [('person',
                                                                                                                   'mentor')],
 ('trouble on the late bus', 'press the alarm, ring the police, and tell the man they are on the way'): [('door',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('trouble on the late bus', 'ring the police quietly, and give them the stop and a description'): [('lesson',
                                                                                                     'a quiet call '
                                                                                                     'still counts')],
 ('trouble on the late bus', 'keep your seat by the door, and quietly shield the passengers behind it'): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('trouble on the late bus', 'ask the man what he wants, and get him off at the next stop'): [('mark',
                                                                                               'took a wild risk')],
 ('trouble on the late bus', 'film it on your phone and call out that the police can already see it'): [('lesson',
                                                                                                         'a raised '
                                                                                                         'phone '
                                                                                                         'calms '
                                                                                                         'people')],
 ('trouble on the late bus', 'get the passengers on their feet together behind the driver'): [('person', 'regular')],
 ('the quake on the old side of town', 'sign on at the shelter, and take a shift keeping the list of names'): [('place',
                                                                                                                'prot.rescue')],
 ('the quake on the old side of town', 'help the crews work out which blocks to search first'): [('mark',
                                                                                                  'helped someone in '
                                                                                                  'need')],
 ('the quake on the old side of town', 'let your spare room to a family who lost their home, at a fair rent'): [('means',
                                                                                                                 'money+.03')],
 ('the quake on the old side of town', 'drive your van between the shelter and the rubble, day and night'): [('means',
                                                                                                              'health-.03')],
 ('the quake on the old side of town', 'lead the neighbours to the park on the high, firm ground, and keep them there'): [('means',
                                                                                                                           'ties+.06')],
 ('the quake on the old side of town', 'run the donations desk at the gym, and keep a strict record of it'): [('lesson',
                                                                                                               'a '
                                                                                                               'strict '
                                                                                                               'list '
                                                                                                               'keeps '
                                                                                                               'trust')],
 ('the flood wall gives way', 'turn out with the dyke watch and fill sandbags at the breach'): [('place',
                                                                                                 'prot.rescue')],
 ('the flood wall gives way', 'take the old warnings to the council and ask why they were ignored'): [('place',
                                                                                                       'rule.voice')],
 ('the flood wall gives way', 'get the insurance claim in first, with photographs of every room'): [('means',
                                                                                                     'money+.06')],
 ('the flood wall gives way', 'carry everything you can up to the top floor, and stay with the house'): [('door',
                                                                                                          'stayed '
                                                                                                          'home')],
 ('the flood wall gives way', 'hire out your boat and your back to the shops that need clearing'): [('means',
                                                                                                     'money+.03')],
 ('the flood wall gives way', 'join the committee that decides who pays for the new wall'): [('place',
                                                                                              'rule.counsel')],
 ('the flood wall gives way', 'dig out the old drainage ditch again with the neighbours who remember it'): [('person',
                                                                                                             'elder')],
 ('the long quarrel next door ends', 'hear the other side through to the end, then give your own as plainly'): [('person',
                                                                                                                 'neighbour')],
 ('the long quarrel next door ends', 'bring the old map and the letters, and settle the facts before anyone apologises'): [('lesson',
                                                                                                                            'the '
                                                                                                                            'facts '
                                                                                                                            'cool '
                                                                                                                            'an '
                                                                                                                            'old '
                                                                                                                            'quarrel')],
 ('the long quarrel next door ends', 'agree to the peace, but only once they pay for the new fence'): [('means',
                                                                                                        'money+.03')],
 ('the long quarrel next door ends', 'bring both grandmothers to the table, and let the old ties do the mending'): [('means',
                                                                                                                     'ties+.06')],
 ('the long quarrel next door ends', 'settle it with a deal over the hedge, and keep good terms for favours ahead'): [('door',
                                                                                                                       'made '
                                                                                                                       'a '
                                                                                                                       'friend')],
 ('the long quarrel next door ends', 'write down what both sides agree, simply, so the children never start it again'): [('door',
                                                                                                                          'kept '
                                                                                                                          'your '
                                                                                                                          'word')],
 ('the long quarrel next door ends', 'speak up at the table for the neighbour your own family wronged first'): [('door',
                                                                                                                 'owned '
                                                                                                                 'up')],
 ('the permits followed the donations', "ask at the council's open meeting for a proper inquiry, with every name heard"): [('place',
                                                                                                                            'rule.voice')],
 ('the permits followed the donations', 'read every leaked file before believing a word anyone says about it'): [('lesson',
                                                                                                                  'read '
                                                                                                                  'it '
                                                                                                                  'all '
                                                                                                                  'before '
                                                                                                                  'judging')],
 ('the permits followed the donations', 'stand by the named friend in public, because friends owe each other that'): [('means',
                                                                                                                       'ties-.03')],
 ('the permits followed the donations', 'keep out of the quarrel, and keep a place at the table for the named family'): [('lesson',
                                                                                                                          'old '
                                                                                                                          'friends '
                                                                                                                          'outlast '
                                                                                                                          'a '
                                                                                                                          'scandal')],
 ('the permits followed the donations', 'get the neighbours to object to the next permit together, as one street'): [('person',
                                                                                                                      'neighbour')],
 ('the permits followed the donations', 'quietly pass the reporter the one paper the leak missed, for a favour later'): [('person',
                                                                                                                          'go-between')],
 ('the permits followed the donations', 'start a public list of every permit and donation, open for anyone to check'): [('means',
                                                                                                                         'time-.06')],
 ('the permits followed the donations', 'offer to help the council clean house, and take a seat on its new panel'): [('place',
                                                                                                                      'rule.counsel')],
 ('the permits followed the donations', 'visit the named family, and urge them gently to answer for it honestly'): [('mark',
                                                                                                                     'helped '
                                                                                                                     'someone '
                                                                                                                     'in '
                                                                                                                     'need')],
 ('the petition saves the bus route', 'write to thank the councillors who listened, and say you will see it kept'): [('door',
                                                                                                                      'kept '
                                                                                                                      'your '
                                                                                                                      'word')],
 ('the petition saves the bus route', 'offer to help the woman who started it, and get to know who she knows'): [('person',
                                                                                                                  'go-between')],
 ('the petition saves the bus route', 'start a second petition the same week, for the broken streetlights on the hill'): [('place',
                                                                                                                           'rule.voice')],
 ('the petition saves the bus route', "join the residents' committee, where the same few families pick the next fight"): [('place',
                                                                                                                           'rule.counsel')],
 ('the petition saves the bus route', 'put your name forward for the council seat that falls open next spring'): [('door',
                                                                                                                   'took '
                                                                                                                   'a '
                                                                                                                   'wild '
                                                                                                                   'risk')],
 ('the petition saves the bus route', 'design a simpler way for anyone to start a petition, and send it to the council'): [('lesson',
                                                                                                                            'the '
                                                                                                                            'council '
                                                                                                                            'can '
                                                                                                                            'be '
                                                                                                                            'moved')],
 ('the petition saves the bus route', 'help set up a group that keeps watch on the route and meets each month'): [('place',
                                                                                                                   'gather.hall')],
 ('the petition saves the bus route', "pin the council's full decision in the shelter, so nobody can deny the promise"): [('lesson',
                                                                                                                           'a '
                                                                                                                           'promise '
                                                                                                                           'in '
                                                                                                                           'writing '
                                                                                                                           'holds')],
 ('the old laws come back', 'keep the new rules to the letter, whichever way you voted'): [('means', 'freedom-.03')],
 ('the old laws come back', 'gather the figures on what the repeal changes, and share them plainly'): [('lesson',
                                                                                                        'numbers '
                                                                                                        'calm a '
                                                                                                        'heated '
                                                                                                        'street')],
 ('the old laws come back', 'get on good terms with the people newly in favour at the town hall'): [('person',
                                                                                                     'patron')],
 ('the old laws come back', 'join the crowd outside the town hall on the night the repeal passes'): [('place',
                                                                                                      'gather.great')],
 ('the old laws come back', 'sit with the old people of the street, and let them enjoy what came back'): [('person',
                                                                                                           'elder')],
 ('the old laws come back', 'find the gap the repeal left open, and quietly make use of it'): [('means',
                                                                                                'money+.03')],
 ('the old laws come back', 'ask the older neighbours what life under the old law was like, before deciding'): [('person',
                                                                                                                 'neighbour')],
 ('the old laws come back', "stand for the residents' board to argue for a softer version of the rules"): [('place',
                                                                                                            'rule.counsel')],
 ('the old laws come back', 'stand up at the open meeting for the people the repeal hits hardest'): [('place',
                                                                                                      'rule.voice')],
 ('the court clears the builder', 'help the families file the appeal, with every step done properly'): [('door',
                                                                                                         'helped '
                                                                                                         'someone in '
                                                                                                         'need')],
 ('the court clears the builder', "find someone with weight at the town hall to take the families' side"): [('person',
                                                                                                             'patron')],
 ('the court clears the builder', 'stand outside the court with a sign on the day the builder comes out'): [('place',
                                                                                                             'rule.voice')],
 ('the court clears the builder', 'turn every family you know away from hiring that builder again'): [('person',
                                                                                                       'rival')],
 ('the court clears the builder', 'gather the whole street on the council steps for the families'): [('place',
                                                                                                      'gather.great')],
 ('the court clears the builder', 'dig out the old ruling the defence hoped nobody would remember'): [('lesson',
                                                                                                       'old rulings '
                                                                                                       'still have '
                                                                                                       'teeth')],
 ('the court clears the builder', 'start a fund so the families can afford a proper lawyer'): [('means', 'time-.06')],
 ('the amnesty list', 'accept the amnesty as law, and greet the man civilly if you meet'): [('lesson',
                                                                                             'a nod can end things')],
 ('the amnesty list', 'call in every favour owed to find work for the one who came home'): [('means', 'ties-.06')],
 ('the amnesty list', 'throw a homecoming party the whole street will hear'): [('means', 'ties+.03')],
 ('the amnesty list', 'let the family gather slowly, and leave the old wrongs for another day'): [('lesson',
                                                                                                   'some wrongs can '
                                                                                                   'wait')],
 ('the amnesty list', 'ask a mediator what could be done between the two families'): [('person', 'go-between')],
 ('the amnesty list', 'speak at the hearing on the next round, for those still left out'): [('place', 'rule.voice')],
 ('the amnesty list', 'claim for the family the compensation the amnesty allows'): [('means', 'money+.06')],
 ('a new charge on the water bill', 'pay the charge on time, and ask the meeting that everyone pays alike'): [('means',
                                                                                                               'money-.03')],
 ('a new charge on the water bill', 'lay out what each street pays, and show the meeting where it falls hardest'): [('place',
                                                                                                                     'rule.voice')],
 ('a new charge on the water bill', 'find the exemption a neighbour got, and apply for it under the same rule'): [('means',
                                                                                                                   'money+.03')],
 ('a new charge on the water bill', 'cut back at home and pay it quietly, as the family always has'): [('means',
                                                                                                        'freedom-.03')],
 ('a new charge on the water bill', 'draft a fairer charge by size of house, and put it to the meeting'): [('lesson',
                                                                                                            'fairness '
                                                                                                            'can be '
                                                                                                            'measured')],
 ('a new charge on the water bill', 'volunteer for the council panel that decides who gets let off'): [('place',
                                                                                                        'rule.counsel')],
 ('new powers after the attack', 'keep the new rules, and write to your representative asking for a time limit'): [('place',
                                                                                                                    'rule.voice')],
 ('new powers after the attack', 'keep on good terms with the officers who now decide who gets questioned'): [('person',
                                                                                                               'patron')],
 ('new powers after the attack', 'move the evenings home, and keep the old friends close and quiet'): [('place',
                                                                                                        'gather.house')],
 ('new powers after the attack', 'start a private group online where the talk goes on, out of sight'): [('place',
                                                                                                         'gather.circle')],
 ('new powers after the attack', 'find a lawyer who knows the new law, and get the questioning of your friend stopped'): [('means',
                                                                                                                           'money-.06')],
 ('new powers after the attack', 'keep a record of everyone questioned on the street, to hand over when it is safe'): [('door',
                                                                                                                        'kept '
                                                                                                                        'it '
                                                                                                                        'hidden')],
 ('new powers after the attack', "ask the residents' meeting to stand together for anyone who is questioned"): [('person',
                                                                                                                 'neighbour')],
 ('the district gets its own council', 'volunteer to take the minutes at every meeting of the first year'): [('place',
                                                                                                              'rule.counsel')],
 ('the district gets its own council', "rewrite the new council's standing rules in plain words for everyone"): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('the district gets its own council', 'build a following among the shopkeepers, and stand for one of the seven seats'): [('means',
                                                                                                                           'ties+.06')],
 ('the district gets its own council', 'bring the complaint the old council never heard on the very first night'): [('lesson',
                                                                                                                     'a '
                                                                                                                     'new '
                                                                                                                     'room '
                                                                                                                     'hears '
                                                                                                                     'old '
                                                                                                                     'complaints')],
 ('the district gets its own council', 'ask the founders to choose the first candidates together, as the campaign always did'): [('person',
                                                                                                                                  'elder')],
 ('the district gets its own council', "back the old families' candidate, and keep a word in hand for later"): [('person',
                                                                                                                 'patron')],
 ('the district gets its own council', 'read the whole new budget first, and ask the one awkward question'): [('lesson',
                                                                                                               'one '
                                                                                                               'question '
                                                                                                               'can '
                                                                                                               'shift '
                                                                                                               'a '
                                                                                                               'room')],
 ('the district gets its own council', 'propose that any resident may put a question on the agenda'): [('place',
                                                                                                        'rule.voice')],
 ('the district gets its own council', "set up a circle to settle neighbours' quarrels before they reach the council"): [('place',
                                                                                                                          'gather.talk')],
 ('the district gets its own council', 'stand as an independent for the seat on your own street'): [('door',
                                                                                                     'took a wild '
                                                                                                     'risk')],
 ('the budget fails again', 'keep the paperwork in order and wait your turn, as the rules say'): [('means',
                                                                                                   'time-.03')],
 ('the budget fails again', 'send both leaders the cost of the deadlock, worked out street by street'): [('place',
                                                                                                          'rule.voice')],
 ('the budget fails again', 'find a friend in the planning office who can push one form through'): [('person',
                                                                                                     'go-between')],
 ('the budget fails again', 'stand at the next election against both sides, on a promise to end the deadlock'): [('door',
                                                                                                                  'took '
                                                                                                                  'a '
                                                                                                                  'wild '
                                                                                                                  'risk')],
 ('the budget fails again', 'ask the oldest councillors how the town got through the last deadlock'): [('person',
                                                                                                        'elder')],
 ('the budget fails again', 'throw in with the side most likely to win, and help it carry the vote'): [('person',
                                                                                                        'patron')],
 ('the budget fails again', 'draft a fair compromise both sides could sign, and send it to both'): [('lesson',
                                                                                                     'both sides '
                                                                                                     'want a way '
                                                                                                     'out')],
 ('the paramedic is named online', 'say publicly that she deserves a fair hearing before anyone is blamed'): [('lesson',
                                                                                                               'a '
                                                                                                               'name '
                                                                                                               'online '
                                                                                                               'proves '
                                                                                                               'nothing')],
 ('the paramedic is named online', 'gather the known facts in one place, and post them without comment'): [('lesson',
                                                                                                            'facts '
                                                                                                            'travel '
                                                                                                            'slower '
                                                                                                            'than '
                                                                                                            'names')],
 ('the paramedic is named online', 'keep quiet until the inquiry reports, and keep your own name out of it'): [('door',
                                                                                                                'refused '
                                                                                                                'someone '
                                                                                                                'in '
                                                                                                                'need')],
 ('the paramedic is named online', 'answer the angriest posts one by one, all through the night'): [('person',
                                                                                                     'rival')],
 ('the paramedic is named online', 'quietly let the people who matter on the estate know whose side you are on'): [('means',
                                                                                                                    'ties+.03')],
 ('the paramedic is named online', 'hear her side in her own kitchen, and write it down faithfully'): [('person',
                                                                                                        'friend')],
 ('the paramedic is named online', "start a campaign for the inquiry's findings to be published in full"): [('place',
                                                                                                             'rule.voice')],
 ('the counter at the door', 'answer every question truly, the lodger included'): [('door', 'owned up')],
 ('the counter at the door', 'find out what the answers are used for before filling in a single box'): [('lesson',
                                                                                                         'ask what '
                                                                                                         'the form '
                                                                                                         'is for')],
 ('the counter at the door', "tell the counter through the door that it is nobody's business"): [('mark',
                                                                                                  'defied an '
                                                                                                  'authority')],
 ('the counter at the door', 'walk the counter round to the neighbours who never open their doors'): [('person',
                                                                                                       'neighbour')],
 ('the counter at the door', 'sign up as a counter for the fee, and see who really lives where'): [('means',
                                                                                                    'money+.03')],
 ('the counter at the door', 'knock on every door on the street, so nobody on it is missed'): [('means', 'ties+.03')],
 ('the counter at the door', 'work out what the street gains from every extra name counted'): [('lesson',
                                                                                                'every name counted '
                                                                                                'carries weight')],
 ('the counter at the door', 'ask how the answers are kept, and write to the council if the reply is vague'): [('place',
                                                                                                                'rule.voice')],
 ('ruled from the other capital', 'keep working at the town hall under the new rule, honestly and by the book'): [('person',
                                                                                                                   'boss')],
 ('ruled from the other capital', 'take the post the new officials offer to locals who know the town'): [('means',
                                                                                                          'money+.06')],
 ('ruled from the other capital', 'teach the old language at home every evening to the youngest of the family'): [('means',
                                                                                                                   'time-.06')],
 ('ruled from the other capital', "keep your head down, trade with whoever rules, and hold on to the family's land"): [('door',
                                                                                                                        'gave '
                                                                                                                        'in '
                                                                                                                        'to '
                                                                                                                        'pressure')],
 ('ruled from the other capital', 'write down what happens to the town, and get it out to the wider world'): [('door',
                                                                                                               'defied '
                                                                                                               'an '
                                                                                                               'authority')],
 ('ruled from the other capital', 'stand for the council the new rulers allow, to keep some say local'): [('place',
                                                                                                           'rule.counsel')],
 ('ruled from the other capital', 'hide the old town records safely in the attic, for when this ends'): [('door',
                                                                                                          'kept it '
                                                                                                          'hidden')],
 ('a month to leave', 'speak at the hearing for the family, as a neighbour who knows them'): [('place',
                                                                                               'rule.voice')],
 ('a month to leave', 'find the exception in the law that fits their case, and file it in time'): [('mark',
                                                                                                    'helped someone '
                                                                                                    'in need')],
 ('a month to leave', 'buy the house next door cheaply, before someone else does'): [('means', 'money-.10')],
 ('a month to leave', "keep away from it all, and keep your own family's papers in order"): [('door',
                                                                                              'refused someone in '
                                                                                              'need')],
 ('a month to leave', 'get a lawyer who owes you a favour to take their appeal'): [('means', 'ties-.03')],
 ('a month to leave', 'gather the stories of every family on the list, and publish them'): [('door',
                                                                                             'defied an authority')],
 ('a month to leave', "get the whole street to sign for the family's right to stay"): [('person', 'neighbour')],
 ('the councillor wins the playground', 'thank her in writing, and ask that every estate get the same'): [('lesson',
                                                                                                           'councillors '
                                                                                                           'remember '
                                                                                                           'who said '
                                                                                                           'thanks')],
 ('the councillor wins the playground', 'ask at the council where the money came from, line by line'): [('lesson',
                                                                                                         'every gift '
                                                                                                         'costs '
                                                                                                         'someone '
                                                                                                         'something')],
 ('the councillor wins the playground', "promise her your vote and your family's, and ask what she needs"): [('person',
                                                                                                              'patron')],
 ('the councillor wins the playground', 'throw the opening party with every family on the estate'): [('means',
                                                                                                      'ties+.06')],
 ('the councillor wins the playground', "work out what the estate's next ask should be, and bring it to her quietly"): [('person',
                                                                                                                         'go-between')],
 ('the councillor wins the playground', 'propose that the estates set the playground budget themselves, in the open'): [('place',
                                                                                                                         'rule.counsel')],
 ('the councillor wins the playground', 'volunteer for her campaign at the next election'): [('place', 'rule.voice')],
 ('the councillor wins the playground', "start a residents' group to look after it and share it with the next estate"): [('place',
                                                                                                                          'gather.hall')],
 ('asked to stand for a child at the naming', 'say yes, and learn every word of the rite by heart for the day'): [('place',
                                                                                                                   'faith.congregation')],
 ('asked to stand for a child at the naming', 'ask whoever leads the rite to explain each part before you agree'): [('place',
                                                                                                                     'faith.seeking')],
 ('asked to stand for a child at the naming', "agree, on condition that you get a real say in the child's schooling"): [('lesson',
                                                                                                                         'a '
                                                                                                                         'say '
                                                                                                                         'comes '
                                                                                                                         'with '
                                                                                                                         'a '
                                                                                                                         'duty')],
 ('asked to stand for a child at the naming', 'say yes on the spot, and swear to be the most fun person in her life'): [('door',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('asked to stand for a child at the naming', 'ask for the old family shawl, and hold the baby in it at the rite'): [('lesson',
                                                                                                                      'old '
                                                                                                                      'things '
                                                                                                                      'carry '
                                                                                                                      'the '
                                                                                                                      'family')],
 ('asked to stand for a child at the naming', 'draw up a fair order for the rite, with a part for each side'): [('means',
                                                                                                                 'ties+.03')],
 ('asked to stand for a child at the naming', 'ring the parent who is staying away, and tell them plainly they are needed'): [('means',
                                                                                                                               'ties+.06')],
 ('asked to stand for a child at the naming', 'ask the oldest relatives how namings were done in their day, and keep some of it'): [('person',
                                                                                                                                     'elder')],
 ('asked to stand for a child at the naming', 'throw the naming party yourself, so big and loud that nobody wants to miss it'): [('means',
                                                                                                                                  'money-.06')],
 ('asked to stand for a child at the naming', 'let the grandparents lead the rite, and quietly win their help for the young parents'): [('mark',
                                                                                                                                         'helped '
                                                                                                                                         'someone '
                                                                                                                                         'in '
                                                                                                                                         'need')],
 ('who comes to the wedding', 'meet both families, and find what each rite truly cannot do without'): [('lesson',
                                                                                                        'every rite '
                                                                                                        'has a '
                                                                                                        'core')],
 ('who comes to the wedding', 'broker a deal: the old way at the rite, the new way at the party'): [('means',
                                                                                                     'ties+.03')],
 ('who comes to the wedding', 'tell your parent that if they stay away, they will regret it all their life'): [('means',
                                                                                                                'ties-.03')],
 ('who comes to the wedding', 'ask the eldest of both families to lead the rite together'): [('person', 'elder')],
 ('who comes to the wedding', 'host the wedding meal at your own home, so both families come to your table'): [('place',
                                                                                                                'gather.house')],
 ('who comes to the wedding', 'find a hall and a leader for the rite that neither family can object to'): [('place',
                                                                                                            'gather.hall')],
 ('who comes to the wedding', 'help the couple write a rite of their own, with something from each side'): [('place',
                                                                                                             'faith.seeking')],
 ('who comes to the wedding', 'sit with your parent every evening that week until they agree to come'): [('means',
                                                                                                          'ties+.06')],
 ('who comes to the wedding', 'stand up at the family meal, and say the wedding goes ahead with or without them'): [('lesson',
                                                                                                                     'say '
                                                                                                                     'it '
                                                                                                                     'once '
                                                                                                                     'out '
                                                                                                                     'loud')],
 ('a new teacher with a way of their own', 'keep every rule of the class, and help the slow ones keep up'): [('person',
                                                                                                              'friend')],
 ('a new teacher with a way of their own', 'aim for the top of the chart, and ask exactly how to get there'): [('means',
                                                                                                                'time-.06')],
 ('a new teacher with a way of their own', 'volunteer for every experiment and every outing, first in line'): [('lesson',
                                                                                                                'first '
                                                                                                                'in '
                                                                                                                'line '
                                                                                                                'sees '
                                                                                                                'most')],
 ('a new teacher with a way of their own', 'ask the teacher to teach you the old names of the places around you'): [('mark',
                                                                                                                     'learned '
                                                                                                                     'a '
                                                                                                                     'skill')],
 ('a new teacher with a way of their own', 'dig the class garden with the teacher, and keep it growing all summer'): [('person',
                                                                                                                       'mentor')],
 ('a new teacher with a way of their own', 'find out what the teacher thinks the best pupils do, and do just that'): [('lesson',
                                                                                                                       'watch '
                                                                                                                       'what '
                                                                                                                       'gets '
                                                                                                                       'praised')],
 ('a new teacher with a way of their own', 'write down the old stories the teacher tells, in a book of your own'): [('place',
                                                                                                                     'arts.page')],
 ('a new teacher with a way of their own', 'ask to be the class monitor, and keep the register yourself'): [('means',
                                                                                                             'time-.03')],
 ('picked at the gate at dawn', 'wait your turn in the line, and trust the foreman to pick fairly'): [('lesson',
                                                                                                       'fair lines '
                                                                                                       'move '
                                                                                                       'slowly')],
 ('picked at the gate at dawn', 'show the foreman the safety card you earned at the job centre last week'): [('person',
                                                                                                              'boss')],
 ('picked at the gate at dawn', "step forward and name a day rate lower than anyone else's"): [('person', 'rival')],
 ('picked at the gate at dawn', 'push to the front and say you will take any job going, starting now'): [('means',
                                                                                                          'money+.03')],
 ('picked at the gate at dawn', "tell the foreman which family you come from, and let your uncle's name speak"): [('lesson',
                                                                                                                   'a '
                                                                                                                   'name '
                                                                                                                   'opens '
                                                                                                                   'doors')],
 ('picked at the gate at dawn', 'sign on at the job centre, and apply by the book for every post listed'): [('means',
                                                                                                             'time-.03')],
 ('picked at the gate at dawn', 'ask the shopkeeper who has known your family for years to take you on'): [('place',
                                                                                                            'comm.shop')],
 ('back at the job centre after thirty years', 'sign on, keep every appointment, and apply for every post the adviser lists'): [('means',
                                                                                                                                 'time-.06')],
 ('back at the job centre after thirty years', 'set up on your own account with the payout and the old customers'): [('place',
                                                                                                                      'prod.craft')],
 ('back at the job centre after thirty years', 'take the first thing going, anything outdoors, and see where it leads'): [('lesson',
                                                                                                                           'new '
                                                                                                                           'ground '
                                                                                                                           'at '
                                                                                                                           'any '
                                                                                                                           'age')],
 ('back at the job centre after thirty years', 'ask the old hands from the works who is taking people on'): [('means',
                                                                                                              'ties+.03')],
 ('back at the job centre after thirty years', 'sell your skills by the day to whoever pays most, and keep your own hours'): [('means',
                                                                                                                               'freedom+.06')],
 ('back at the job centre after thirty years', "find the firm that took over the old works' orders, and show them what you know"): [('person',
                                                                                                                                     'boss')],
 ('back at the job centre after thirty years', "offer to train a new firm's young hands in the old trade"): [('person',
                                                                                                              'colleague')],
 ('back at the job centre after thirty years', 'join the other laid-off hands to start a small workshop as a co-op'): [('place',
                                                                                                                        'prod.craft')],
 ('back at the job centre after thirty years', 'stand up at the jobs fair, and say plainly that older hands are being passed over'): [('place',
                                                                                                                                       'rule.voice')],
 ('the branch splits over the candidate', 'insist the branch choose by its own rules, with a secret ballot'): [('lesson',
                                                                                                                'fair '
                                                                                                                'rules '
                                                                                                                'outlast '
                                                                                                                'a '
                                                                                                                'feud')],
 ('the branch splits over the candidate', 'ask both of them to set out their plans for the ward at one meeting'): [('means',
                                                                                                                    'ties+.03')],
 ('the branch splits over the candidate', 'count the votes each side has, and join the winner before the meeting'): [('door',
                                                                                                                      'gave '
                                                                                                                      'in '
                                                                                                                      'to '
                                                                                                                      'pressure')],
 ('the branch splits over the candidate', 'walk out of the branch, and put your effort into a street campaign instead'): [('means',
                                                                                                                           'freedom+.06')],
 ('the branch splits over the candidate', 'draw up a fair way to choose, and get both sides to sign it first'): [('door',
                                                                                                                  'kept '
                                                                                                                  'your '
                                                                                                                  'word')],
 ('the branch splits over the candidate', 'tell the whole meeting that the feud is losing them the ward'): [('person',
                                                                                                             'rival')],
 ('the branch splits over the candidate', 'keep going to every meeting, and hear the old members out before you vote'): [('person',
                                                                                                                          'elder')],
 ('the branch splits over the candidate', 'stop going to branch meetings until it is settled, and let others decide'): [('means',
                                                                                                                         'ties-.03')],
 ('the chair of the council steps down', 'take the chair, and run every meeting by the standing orders, your own side included'): [('person',
                                                                                                                                    'rival')],
 ('the chair of the council steps down', 'take the chair on one condition: every report and vote open for anyone to read'): [('means',
                                                                                                                              'time-.06')],
 ('the chair of the council steps down', 'let your name go forward only once you have the votes for your own budget'): [('person',
                                                                                                                         'colleague')],
 ('the chair of the council steps down', 'turn the chair down, and keep the seat where you can still speak out of turn'): [('door',
                                                                                                                            'turned '
                                                                                                                            'down '
                                                                                                                            'a '
                                                                                                                            'chance')],
 ('the chair of the council steps down', 'put forward the member for the old ward, and serve loyally under him'): [('person',
                                                                                                                    'boss')],
 ('the chair of the council steps down', 'give up the seat at the next election, and go back to your own street'): [('means',
                                                                                                                     'freedom+.10')],
 ('the chair of the council steps down', 'back a young member for the chair, and pay for her campaign at the next election'): [('means',
                                                                                                                                'money-.06')],
 ('the chair of the council steps down', 'open the meetings to the public on evenings, with three minutes for anyone who asks'): [('means',
                                                                                                                                   'ties+.06')],
 ('the chair of the council steps down', 'take the chair, and strike a budget deal with the other side in the first week'): [('person',
                                                                                                                              'friend')],
 ('the chair of the council steps down', "start a free legal advice fund at the town hall, in the old chair's name"): [('mark',
                                                                                                                        'helped '
                                                                                                                        'someone '
                                                                                                                        'in '
                                                                                                                        'need')],
 ('the society splits over the open nights', "put both plans to the annual meeting, and abide by the members' vote"): [('door',
                                                                                                                        'kept '
                                                                                                                        'your '
                                                                                                                        'word')],
 ('the society splits over the open nights', 'run the open nights for one season as a trial, and show the meeting the figures'): [('person',
                                                                                                                                   'regular')],
 ('the society splits over the open nights', 'pay for the roof yourself, on the understanding that the open nights go ahead'): [('means',
                                                                                                                                 'money-.10')],
 ('the society splits over the open nights', 'throw the next open night before the vote, and let the hall decide for itself'): [('person',
                                                                                                                                 'rival')],
 ('the society splits over the open nights', "write a new rule book with a members' night and an open night each week"): [('lesson',
                                                                                                                           'one '
                                                                                                                           'hall '
                                                                                                                           'can '
                                                                                                                           'hold '
                                                                                                                           'two '
                                                                                                                           'camps')],
 ('the society splits over the open nights', 'hold a supper for both sides at the hall, and ask them to stay one society'): [('means',
                                                                                                                              'ties+.06')],
 ('the society splits over the open nights', 'step down as chair, and help the young ones start a society of their own'): [('means',
                                                                                                                            'freedom+.06')],
 ('the society splits over the open nights', 'get the hall licensed for late open nights, through a friend on the licensing board'): [('person',
                                                                                                                                       'go-between')],
 ("the players' grant is cut", 'rebuild the season around the plays that sell, and show the council the takings'): [('means',
                                                                                                                     'money+.06')],
 ("the players' grant is cut", 'keep teaching the old plays to the young ones, whatever stage you end up on'): [('lesson',
                                                                                                                 'the '
                                                                                                                 'craft '
                                                                                                                 'travels '
                                                                                                                 'with '
                                                                                                                 'you')],
 ("the players' grant is cut", "take a seat on the town's arts board, and argue for the theatre's grant there"): [('place',
                                                                                                                   'rule.counsel')],
 ("the players' grant is cut", "lead the whole company, in costume, to the council's next meeting"): [('place',
                                                                                                       'rule.voice')],
 ("the players' grant is cut", 'start a theatre school in the old hall, and let its fees pay for the stage'): [('means',
                                                                                                                'time-.10')],
 ("the players' grant is cut", "pay for one young player's place each year, in the founders' name"): [('means',
                                                                                                       'money-.06')],
 ("the players' grant is cut", "make the young ones the company's board, and stage whatever they choose"): [('means',
                                                                                                             'ties+.06')],
 ('the kitchen in the back hall is running out', 'tell the congregation plainly what it costs, and ask every household for a share'): [('means',
                                                                                                                                        'ties+.03')],
 ('the kitchen in the back hall is running out', "join the kitchen to the town's food bank, so it runs on their stores"): [('person',
                                                                                                                            'colleague')],
 ('the kitchen in the back hall is running out', 'give a large gift of your own, and name the kitchen for your family'): [('means',
                                                                                                                           'money-.10')],
 ('the kitchen in the back hall is running out', 'preach on it at the gathering, so that nobody leaves without giving'): [('person',
                                                                                                                           'rival')],
 ('the kitchen in the back hall is running out', 'ask the old families who started it to come back and cook as their mothers did'): [('person',
                                                                                                                                      'elder')],
 ('the kitchen in the back hall is running out', "stand for the council in May, with the kitchen's grant as your one promise"): [('place',
                                                                                                                                  'rule.voice'),
                                                                                                                                 ('door',
                                                                                                                                  'kept '
                                                                                                                                  'your '
                                                                                                                                  'word')],
 ('the kitchen in the back hall is running out', 'set up a trust for the kitchen, with its own board and its own books'): [('place',
                                                                                                                            'rule.counsel')],
 ('the kitchen in the back hall is running out', 'hand the kitchen to the young ones, and let them run it their own way'): [('means',
                                                                                                                             'freedom+.06')],
 ('the kitchen in the back hall is running out', 'ask the councillor who worships with you for a ward grant, as a favour'): [('person',
                                                                                                                              'patron')],
 ("the small ward's last winter", "stand up at the board's hearing, and tell what the ward does for every patient"): [('lesson',
                                                                                                                       'the '
                                                                                                                       'work '
                                                                                                                       'can '
                                                                                                                       'speak '
                                                                                                                       'for '
                                                                                                                       'itself')],
 ("the small ward's last winter", "take the ward sister's post when she retires, and run the ward by the figures"): [('means',
                                                                                                                      'money+.06')],
 ("the small ward's last winter", "make a named gift to the families' fund, and sit on its committee"): [('means',
                                                                                                          'money-.06')],
 ("the small ward's last winter", 'work every extra hour the ward needs to get through its last winter'): [('means',
                                                                                                            'time-.10')],
 ("the small ward's last winter", 'stand for the staff seat on the hospital board, and argue for the ward there'): [('place',
                                                                                                                     'rule.counsel')],
 ("the small ward's last winter", "take on the families' fund, and run it as the ward's own league of friends"): [('means',
                                                                                                                   'ties+.06')],
 ("the small ward's last winter", 'take a post at the private clinic across town, where the old patients will go'): [('person',
                                                                                                                      'boss')],
 ("the small ward's last winter", "start a carers' circle where families learn the daily exercises from each other"): [('place',
                                                                                                                        'gather.talk')],
 ("the small ward's last winter", 'go on the evening news with what closing the ward will cost the town'): [('mark',
                                                                                                             'defied '
                                                                                                             'an '
                                                                                                             'authority')],
 ('the college ends its evening classes', 'speak for the evening classes at the college council, and ask for one more year'): [('door',
                                                                                                                                'kept '
                                                                                                                                'your '
                                                                                                                                'word')],
 ('the college ends its evening classes', 'offer to run the evening programme, and make it pay with a certificate employers want'): [('means',
                                                                                                                                      'money+.06')],
 ('the college ends its evening classes', 'teach the class anyway, in the back room of the pub, for nothing'): [('place',
                                                                                                                 'gather.night')],
 ('the college ends its evening classes', 'keep teaching the day classes, and let the evening ones end quietly'): [('means',
                                                                                                                    'ties-.03')],
 ('the college ends its evening classes', 'set up a bursary in your name so poor students can take the course elsewhere'): [('means',
                                                                                                                             'money-.06')],
 ('the college ends its evening classes', 'stand for the college council, and vote for the evening classes from inside'): [('place',
                                                                                                                            'rule.counsel')],
 ('the college ends its evening classes', 'get the old students to teach the new ones, one evening a week, unpaid'): [('person',
                                                                                                                       'friend')],
 ('the college ends its evening classes', "ask the college's richest old pupil to pay for the classes for three years"): [('person',
                                                                                                                           'patron')],
 ("the warden of the makers' association retires", 'take the post, and write the standard down so anyone can see what passes'): [('means',
                                                                                                                                  'time-.06')],
 ("the warden of the makers' association retires", "put your savings behind your best apprentice's workshop, and let others judge"): [('means',
                                                                                                                                       'money-.10')],
 ("the warden of the makers' association retires", 'turn the post down, and keep making what moves you at your own bench'): [('door',
                                                                                                                              'turned '
                                                                                                                              'down '
                                                                                                                              'a '
                                                                                                                              'chance')],
 ("the warden of the makers' association retires", 'take the post as the old warden held it, and keep the test he set'): [('person',
                                                                                                                           'mentor')],
 ("the warden of the makers' association retires", "tell the association's meeting plainly which nephews passed who should not have"): [('person',
                                                                                                                                         'rival')],
 ("the warden of the makers' association retires", 'set up a yearly prize for the best apprentice piece, judged without names'): [('means',
                                                                                                                                   'money-.03')],
 ("the warden of the makers' association retires", 'open a workshop of your own that trains apprentices outside the association'): [('mark',
                                                                                                                                     'took '
                                                                                                                                     'a '
                                                                                                                                     'wild '
                                                                                                                                     'risk')],
 ("the warden of the makers' association retires", "stand for the town's trade board, and win the association's test a place in its rules"): [('place',
                                                                                                                                               'rule.counsel')],
 ('the queue at the credit union', 'take the chair, and tell the queue the plain truth about the loss'): [('door',
                                                                                                           'owned '
                                                                                                           'up')],
 ('the queue at the credit union', 'open the books to every member, line by line, at a meeting tomorrow night'): [('means',
                                                                                                                   'ties+.03')],
 ('the queue at the credit union', 'keep your own savings in, and tell the queue so, loudly'): [('mark',
                                                                                                 'took a wild risk')],
 ('the queue at the credit union', "put your family's savings in to cover the loss, as your parents would have"): [('means',
                                                                                                                    'money-.10')],
 ('the queue at the credit union', 'ask the members to stay a year, and give them a vote on every large loan'): [('door',
                                                                                                                  'kept '
                                                                                                                  'your '
                                                                                                                  'word')],
 ('the queue at the credit union', 'tell the whole market on Saturday that you are staying in, and why'): [('place',
                                                                                                            'comm.market')],
 ('the queue at the credit union', 'get the council to stand behind the savings, through your seat on its finance committee'): [('person',
                                                                                                                                 'colleague')],
 ('the queue at the credit union', 'close the credit union in good order, and pay every member what is left'): [('lesson',
                                                                                                                 'ending '
                                                                                                                 'well '
                                                                                                                 'is '
                                                                                                                 'still '
                                                                                                                 'work')],
 ('the queue at the credit union', "ask the town's biggest trader to lend the credit union the money at a fair rate"): [('person',
                                                                                                                         'patron')],
 ('the night desk at the station closes', 'lead the watch rota on the dark nights yourself, the same streets for every house'): [('means',
                                                                                                                                  'time-.10')],
 ('the night desk at the station closes', "take last year's calls to the panel, and show where the nights are worst"): [('person',
                                                                                                                         'colleague')],
 ('the night desk at the station closes', 'pay for a night guard on the main street, and let the shops pay you back'): [('means',
                                                                                                                         'money-.06')],
 ('the night desk at the station closes', 'walk the high street yourself on the first dark night, phone in hand'): [('mark',
                                                                                                                     'took '
                                                                                                                     'a '
                                                                                                                     'wild '
                                                                                                                     'risk')],
 ('the night desk at the station closes', "stand for the council's seat on the police board, and fight the closing there"): [('place',
                                                                                                                              'rule.counsel')],
 ('the night desk at the station closes', 'get the shops to pay into a watch fund for lamps on the dark lanes'): [('person',
                                                                                                                   'patron')],
 ('the night desk at the station closes', 'train the watch to spot trouble early and report it clearly'): [('lesson',
                                                                                                            'early '
                                                                                                            'word '
                                                                                                            'beats '
                                                                                                            'late '
                                                                                                            'help')],
 ('the night desk at the station closes', 'step down, and let the young ones lead the watch their own way'): [('means',
                                                                                                               'freedom+.06')],
 ('nominations close on Friday', 'stand for the seat, and promise a weekly surgery in the ward for anyone'): [('door',
                                                                                                               'kept '
                                                                                                               'your '
                                                                                                               'word')],
 ('nominations close on Friday', 'ask both candidates to a meeting on the estate, and question them in public'): [('person',
                                                                                                                   'rival')],
 ('nominations close on Friday', 'stand, but only once a party has promised its backing and its money'): [('place',
                                                                                                           'rule.voice')],
 ('nominations close on Friday', 'say no, and leave the seat to whoever wants it'): [('door',
                                                                                      'turned down a chance')],
 ('nominations close on Friday', 'back the neighbour who would do it best, and raise the money for her leaflets'): [('person',
                                                                                                                     'friend')],
 ('nominations close on Friday', 'knock on every door on the estate, and get people out to vote, whoever stands'): [('means',
                                                                                                                     'ties+.06')],
 ('nominations close on Friday', 'stand as an independent, with no party, on one promise for the estate'): [('means',
                                                                                                             'money-.06')],
 ('nominations close on Friday', 'ask the old families on the estate who they would trust, and stand behind that person'): [('person',
                                                                                                                             'elder')],
 ('nominations close on Friday', "sign the stranger's form in return for his promise on the estate's repairs"): [('person',
                                                                                                                  'patron')],
 ('lost fairly at the small claims hearing', 'accept the ruling, pay the costs, and thank the clerk on the way out'): [('means',
                                                                                                                        'money-.06')],
 ('lost fairly at the small claims hearing', 'find a lawyer who can find an opening, and appeal on a point of law'): [('means',
                                                                                                                       'money-.10')],
 ('lost fairly at the small claims hearing', "settle it the old way, and ask the builder's family to make it right"): [('person',
                                                                                                                        'go-between')],
 ('lost fairly at the small claims hearing', 'write to the advice office, so other buyers know about that kind of contract'): [('mark',
                                                                                                                                'helped '
                                                                                                                                'someone '
                                                                                                                                'in '
                                                                                                                                'need')],
 ('lost fairly at the small claims hearing', 'pay up, and tell the street that the court was fair, whatever they say'): [('means',
                                                                                                                          'money-.06')],
 ('lost fairly at the small claims hearing', 'hold back the last payment you still owe the builder, ruling or no ruling'): [('person',
                                                                                                                             'rival')],
 ('lost fairly at the small claims hearing', 'leave the costs letter unopened on the side for a month, and hope it goes away'): [('door',
                                                                                                                                  'kept '
                                                                                                                                  'it '
                                                                                                                                  'hidden')],
 ("the foreman's inquiry into the jammed press", 'sign the warning, and do the guard check every morning from now on'): [('door',
                                                                                                                          'kept '
                                                                                                                          'your '
                                                                                                                          'word')],
 ("the foreman's inquiry into the jammed press", 'accept the finding, and ask that the loose guard go in the report as well'): [('door',
                                                                                                                                 'owned '
                                                                                                                                 'up')],
 ("the foreman's inquiry into the jammed press", 'walk off the floor that day, and look for work at the other plant'): [('means',
                                                                                                                         'money-.06')],
 ("the foreman's inquiry into the jammed press", 'go to see your workmate at home with your family, and say it was your fault'): [('person',
                                                                                                                                   'friend')],
 ("the foreman's inquiry into the jammed press", 'propose a signed check sheet for every press, every morning'): [('lesson',
                                                                                                                   'small '
                                                                                                                   'checks '
                                                                                                                   'stop '
                                                                                                                   'big '
                                                                                                                   'harm')],
 ("the foreman's inquiry into the jammed press", 'tell the whole shift at break that the foreman was fair, and the check matters'): [('person',
                                                                                                                                      'mentor')],
 ("the foreman's inquiry into the jammed press", 'ask the union rep to get the warning cut to a year, on your clean record'): [('person',
                                                                                                                                'go-between')],
 ("the foreman's inquiry into the jammed press", 'go through the motions from now on, and do only what the foreman sees'): [('door',
                                                                                                                             'hid '
                                                                                                                             'a '
                                                                                                                             'wrong')],
 ("the foreman's inquiry into the jammed press", 'offer to train the new starters in the checks, if the warning comes off sooner'): [('person',
                                                                                                                                      'colleague')],
 ("the song learned at a parent's knee", 'learn one verse every night until the whole song is yours by heart'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ("the song learned at a parent's knee", 'ask what every strange word means before singing it back'): [('lesson',
                                                                                                        'every old '
                                                                                                        'word has a '
                                                                                                        'story')],
 ("the song learned at a parent's knee", 'sing it at the family party, and take a bow when everyone claps'): [('means',
                                                                                                               'ties+.03')],
 ("the song learned at a parent's knee", 'sing the loud bit as loud as you can, and dance round the bed'): [('lesson',
                                                                                                             'a loud '
                                                                                                             'song '
                                                                                                             'chases '
                                                                                                             'fear')],
 ("the song learned at a parent's knee", 'ask the grandparent to sing it too, the way it was sung long ago'): [('means',
                                                                                                                'ties+.03')],
 ("the song learned at a parent's knee", 'sing it on the walk to school every morning, stamping on the beat'): [('person',
                                                                                                                 'friend')],
 ("the song learned at a parent's knee", 'pick out the tune on the toy piano, and play it for the visitors'): [('door',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ("the song learned at a parent's knee", 'make up a new verse about the dog, and sing it at tea'): [('place',
                                                                                                     'arts.song')],
 ("the song learned at a parent's knee", 'put a hand up at assembly when the teacher asks who knows a song'): [('person',
                                                                                                                'teacher')],
 ("the song learned at a parent's knee", 'sing it each night to the baby in the cot, word for word'): [('means',
                                                                                                        'ties+.06')],
 ('the hall committee turns down your play', 'write to the committee, ask for its reasons in writing, and appeal'): [('door',
                                                                                                                      'defied '
                                                                                                                      'an '
                                                                                                                      'authority')],
 ('the hall committee turns down your play', 'rewrite the scenes they hated until no fair reader could object'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ('the hall committee turns down your play', 'send it to the theatre in the city, and mention the refusal in the letter'): [('place',
                                                                                                                             'arts.stage')],
 ('the hall committee turns down your play', 'read the whole play aloud on the hall steps on its would-be opening night'): [('mark',
                                                                                                                             'defied '
                                                                                                                             'an '
                                                                                                                             'authority')],
 ('the hall committee turns down your play', 'read it to the families whose stories are in it, and ask what they think'): [('means',
                                                                                                                            'ties+.06')],
 ('the hall committee turns down your play', 'get a councillor to back it, and bring it to the committee again in spring'): [('person',
                                                                                                                              'patron')],
 ('the hall committee turns down your play', 'ask the oldest families to come to the next meeting and speak for it'): [('person',
                                                                                                                        'elder')],
 ('the hall committee turns down your play', 'cut it to one quiet hour, and stage it in a front room for the neighbours'): [('place',
                                                                                                                             'gather.house')],
 ('the hall committee turns down your play', 'turn the empty mill into a stage for one night, with a cast of friends'): [('place',
                                                                                                                          'arts.stage')],
 ('the hall committee turns down your play', 'post the line they laughed at online, and let the town decide who looks foolish'): [('door',
                                                                                                                                   'made '
                                                                                                                                   'an '
                                                                                                                                   'enemy')],
 ("asked to play at a friend's wedding", 'practise every evening for five weeks, until it cannot go wrong'): [('mark',
                                                                                                               'kept '
                                                                                                               'your '
                                                                                                               'word')],
 ("asked to play at a friend's wedding", 'work out a new arrangement for one instrument, note by note'): [('mark',
                                                                                                           'learned '
                                                                                                           'a '
                                                                                                           'skill')],
 ("asked to play at a friend's wedding", 'agree a fee, kindly but firmly, and bring cards for the guests'): [('means',
                                                                                                              'money+.03')],
 ("asked to play at a friend's wedding", 'play it your own way on the day, with all the feeling you have'): [('door',
                                                                                                              'took '
                                                                                                              'a '
                                                                                                              'wild '
                                                                                                              'risk')],
 ("asked to play at a friend's wedding", 'play the old wedding tune of the region first, then their song'): [('lesson',
                                                                                                              'old '
                                                                                                              'tunes '
                                                                                                              'carry '
                                                                                                              'a '
                                                                                                              'room')],
 ("asked to play at a friend's wedding", 'ask the couple exactly what they want, and rehearse it in the real room'): [('lesson',
                                                                                                                       'rehearse '
                                                                                                                       'where '
                                                                                                                       'you '
                                                                                                                       'will '
                                                                                                                       'play')],
 ("asked to play at a friend's wedding", 'bring in two friends from the old band, rehearsed and properly paid'): [('place',
                                                                                                                   'arts.song')],
 ("asked to play at a friend's wedding", 'write a verse of your own about the couple, and add it at the end'): [('means',
                                                                                                                 'ties+.06')],
 ("asked to play at a friend's wedding", 'get the whole hall dancing the old way straight after the first dance'): [('person',
                                                                                                                     'friend')],
 ("asked to play at a friend's wedding", 'play for nothing, as your gift, and let both families remember who gave it'): [('door',
                                                                                                                          'made '
                                                                                                                          'a '
                                                                                                                          'friend')],
 ('strangers singing your song', "join in quietly, and let it go on being everyone's song"): [('door',
                                                                                               'kept it hidden')],
 ('strangers singing your song', 'ask them where they learned it, and trace how it travelled'): [('lesson',
                                                                                                  'songs travel '
                                                                                                  'further than '
                                                                                                  'singers')],
 ('strangers singing your song', 'tell the table you wrote it, and register it in your name the next morning'): [('means',
                                                                                                                  'money+.03')],
 ('strangers singing your song', 'stand up and sing the verse they have forgotten, at the top of your voice'): [('person',
                                                                                                                 'friend')],
 ('strangers singing your song', 'say nothing and smile, since that is how the old songs were always made'): [('lesson',
                                                                                                               'old '
                                                                                                               'songs '
                                                                                                               'belong '
                                                                                                               'to '
                                                                                                               'everyone')],
 ('strangers singing your song', 'keep the better line, and write the song out properly for anyone to use'): [('place',
                                                                                                               'arts.page')],
 ('strangers singing your song', 'write to the folk society so the song is listed under your name'): [('place',
                                                                                                       'arts.song')],
 ('strangers singing your song', "learn the strangers' new lines, and sing their version at the local from now on"): [('place',
                                                                                                                       'gather.night')],
 ('strangers singing your song', 'buy the table a round, and sing every verse with them until closing'): [('means',
                                                                                                           'ties+.03')],
 ('strangers singing your song', 'film the strangers singing it, and post it with the true story'): [('door',
                                                                                                      'took a wild '
                                                                                                      'risk')],
 ('the funeral where everyone sings', 'stand, start the first line clearly, and keep the room together to the end'): [('door',
                                                                                                                       'helped '
                                                                                                                       'someone '
                                                                                                                       'in '
                                                                                                                       'need')],
 ('the funeral where everyone sings', 'hum the note quietly first, so the room starts in a key it can reach'): [('lesson',
                                                                                                                 'a '
                                                                                                                 'quiet '
                                                                                                                 'start '
                                                                                                                 'carries '
                                                                                                                 'further')],
 ('the funeral where everyone sings', 'step up to the front, start it alone, and carry the whole chapel'): [('place',
                                                                                                             'arts.song')],
 ('the funeral where everyone sings', 'sing it through the tears, as loudly as the dead would have wanted'): [('lesson',
                                                                                                               'tears '
                                                                                                               'and '
                                                                                                               'songs '
                                                                                                               'belong '
                                                                                                               'together')],
 ('the funeral where everyone sings', 'sing the old coast verse the family thought was lost'): [('means',
                                                                                                 'ties+.06')],
 ('the funeral where everyone sings', 'hand round the words, and agree with the family who leads which verse'): [('door',
                                                                                                                  'kept '
                                                                                                                  'your '
                                                                                                                  'word')],
 ('the funeral where everyone sings', 'ask the oldest mourners to sing the old verse first, then everyone joins'): [('person',
                                                                                                                     'elder')],
 ('the funeral where everyone sings', 'change one line to name what everyone loved in them, and sing it out'): [('door',
                                                                                                                 'made '
                                                                                                                 'a '
                                                                                                                 'friend')],
 ('the funeral where everyone sings', 'start a second song nobody planned, the rowdy one they loved best'): [('person',
                                                                                                              'friend')],
 ('the funeral where everyone sings', 'record the room singing, and give the family a copy to keep'): [('means',
                                                                                                        'ties+.03')],
 ('the last telling at the bedside', 'listen without a word, then promise to tell it to the next child in turn'): [('door',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ('the last telling at the bedside', 'ask about every gap and every strange name before the evening ends'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('the last telling at the bedside', 'record it on the phone, every word, and keep the copy safe'): [('lesson',
                                                                                                      'a copy keeps '
                                                                                                      'the voice')],
 ('the last telling at the bedside', 'laugh at the old jokes, cry at the end, and hold their hand all through'): [('lesson',
                                                                                                                   'laughter '
                                                                                                                   'belongs '
                                                                                                                   'at '
                                                                                                                   'the '
                                                                                                                   'end')],
 ('the last telling at the bedside', 'tell it back to them the next night, so they can hear it is kept'): [('place',
                                                                                                            'arts.tale')],
 ('the last telling at the bedside', 'gather the family round the bed the next night to hear it together'): [('means',
                                                                                                              'ties+.06')],
 ('the last telling at the bedside', 'ring the cousins far away, and hold up the phone so they hear it too'): [('means',
                                                                                                                'ties+.03')],
 ('the last telling at the bedside', 'write it out that night, word for word, with notes on every strange name'): [('place',
                                                                                                                    'arts.page')],
 ('the last telling at the bedside', 'ask them to tell the ending again, then the bits they always left out'): [('door',
                                                                                                                 'kept '
                                                                                                                 'it '
                                                                                                                 'hidden')],
 ('the last telling at the bedside', "take the tale to the folk society, and have it kept under the family's name"): [('place',
                                                                                                                       'learn.keeping')],
 ('a child picks up your old instrument', 'teach the scales first, every evening, the way you were taught'): [('means',
                                                                                                               'time-.03')],
 ('a child picks up your old instrument', 'show them the proper grip, and explain why each finger goes where it does'): [('lesson',
                                                                                                                          'knowing '
                                                                                                                          'why '
                                                                                                                          'makes '
                                                                                                                          'it '
                                                                                                                          'stick')],
 ('a child picks up your old instrument', 'find them the best teacher in town, and pay for the lessons'): [('means',
                                                                                                            'money-.06')],
 ('a child picks up your old instrument', 'take up your own playing again, and play together every evening'): [('means',
                                                                                                                'time-.06')],
 ('a child picks up your old instrument', 'teach them the old tunes by ear, the way your grandparent taught you'): [('lesson',
                                                                                                                     'tunes '
                                                                                                                     'live '
                                                                                                                     'in '
                                                                                                                     'the '
                                                                                                                     'ear')],
 ('a child picks up your old instrument', 'set a fair half hour of practice a day, and keep a chart on the fridge'): [('door',
                                                                                                                       'kept '
                                                                                                                       'your '
                                                                                                                       'word')],
 ('a child picks up your old instrument', 'give them the instrument for keeps, with the story of everyone who played it'): [('means',
                                                                                                                             'ties+.06')],
 ('a child picks up your old instrument', 'plan the exams a year ahead, and put them in for the first one'): [('door',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('a child picks up your old instrument', 'take them to the Sunday afternoon session, and let them sit in at the back'): [('place',
                                                                                                                           'arts.song')],
 ('a child picks up your old instrument', 'form a family band for the summer fair, and put them at the front'): [('place',
                                                                                                                  'gather.great')],
 ('the hours of waiting on the maternity ward', 'keep the waiting room in order: a rota for the chairs, the calls and the coffee'): [('lesson',
                                                                                                                                      'a '
                                                                                                                                      'rota '
                                                                                                                                      'calms '
                                                                                                                                      'a '
                                                                                                                                      'crowd')],
 ('the hours of waiting on the maternity ward', 'ask the midwife plainly what each stage means, and explain it to the others'): [('person',
                                                                                                                                  'keeper')],
 ('the hours of waiting on the maternity ward', 'arrange a private room for the new family, and pay for it yourself'): [('means',
                                                                                                                         'money-.06')],
 ('the hours of waiting on the maternity ward', 'get the whole corridor laughing until the door finally opens'): [('means',
                                                                                                                   'ties+.04')],
 ('the hours of waiting on the maternity ward', 'sit beside the anxious grandparent-to-be, and let the hours pass together'): [('lesson',
                                                                                                                                'waiting '
                                                                                                                                'is '
                                                                                                                                'easier '
                                                                                                                                'shared')],
 ('the hours of waiting on the maternity ward', "go home before dawn, and fill the new family's freezer for a month"): [('means',
                                                                                                                         'time-.03')],
 ('the hours of waiting on the maternity ward', 'ring the oldest aunt to hear how every baby in the family arrived'): [('person',
                                                                                                                        'elder')],
 ('the hours of waiting on the maternity ward', 'talk the night nurse into explaining every beep and number on the screens'): [('mark',
                                                                                                                                'learned '
                                                                                                                                'a '
                                                                                                                                'skill')],
 ('the hours of waiting on the maternity ward', "plan the family's visits for the first week, and put yourself first on the list"): [('means',
                                                                                                                                      'ties-.02')],
 ('fourteen months on the list for a new hip', 'wait your turn on the list like everyone else, and keep every appointment'): [('means',
                                                                                                                               'health-.04')],
 ('fourteen months on the list for a new hip', "compare every hospital's waiting figures, and move to the shortest list in reach"): [('place',
                                                                                                                                      'care.houses')],
 ('fourteen months on the list for a new hip', 'pay the private clinic, and have the operation next month'): [('means',
                                                                                                               'money-.10')],
 ('fourteen months on the list for a new hip', 'ring the hospital every week until they offer a cancelled slot'): [('lesson',
                                                                                                                    'ask '
                                                                                                                    'often, '
                                                                                                                    'and '
                                                                                                                    'ask '
                                                                                                                    'again')],
 ('fourteen months on the list for a new hip', "manage with a stick, warm baths and the neighbours' help until the day comes"): [('person',
                                                                                                                                  'neighbour')],
 ('fourteen months on the list for a new hip', 'keep walking every day through the stiffness, as far as the body allows'): [('means',
                                                                                                                             'health+.03')],
 ('fourteen months on the list for a new hip', "give to the hospital's friends' fund for the extra surgeon it is raising for"): [('means',
                                                                                                                                  'money-.03')],
 ('fourteen months on the list for a new hip', "join the patients' panel that checks how the list is run"): [('place',
                                                                                                              'rule.counsel')],
 ('deciding for a parent who cannot speak', 'ask for a family meeting with the doctors, and choose together what is fairest to them'): [('means',
                                                                                                                                         'ties+.03')],
 ('deciding for a parent who cannot speak', 'ask for the plain odds of each path, and take one night to weigh them'): [('lesson',
                                                                                                                        'weigh '
                                                                                                                        'it, '
                                                                                                                        'then '
                                                                                                                        'decide')],
 ('deciding for a parent who cannot speak', 'get a second opinion from the best specialist, and then decide alone'): [('means',
                                                                                                                       'ties-.03')],
 ('deciding for a parent who cannot speak', 'choose the operation now, while it can still make a difference'): [('door',
                                                                                                                 'took '
                                                                                                                 'a '
                                                                                                                 'wild '
                                                                                                                 'risk')],
 ('deciding for a parent who cannot speak', 'let the body set the pace: keep them comfortable, and wait beside them'): [('means',
                                                                                                                         'time-.04')],
 ('deciding for a parent who cannot speak', 'ask the palliative nurse for the plain truth, and choose comfort if that is it'): [('person',
                                                                                                                                 'keeper')],
 ('deciding for a parent who cannot speak', 'remind the doctors what the parent once said over dinner, and hold them to it'): [('door',
                                                                                                                                'kept '
                                                                                                                                'your '
                                                                                                                                'word')],
 ('deciding for a parent who cannot speak', 'ask whether a trial of some new treatment could take them, and push for it'): [('place',
                                                                                                                             'care.houses')],
 ('deciding for a parent who cannot speak', 'gather the whole family at the bedside, and decide in a circle'): [('means',
                                                                                                                 'ties+.05')],
 ('deciding for a parent who cannot speak', "ask the hospital's ethics panel to set out each path and the rules for it"): [('place',
                                                                                                                            'rule.counsel')],
 ("the carer's afternoon off", 'ask your brother or sister for a fair share of the weeks, written down and kept'): [('means',
                                                                                                                     'time+.04')],
 ("the carer's afternoon off", 'find out every kind of help the council and the clinic offer carers, and claim it'): [('means',
                                                                                                                       'money+.04')],
 ("the carer's afternoon off", 'take the respite week, and spend it somewhere just for yourself'): [('means',
                                                                                                     'health+.05')],
 ("the carer's afternoon off", 'turn the day centre down, and carry on with nerve and good humour'): [('means',
                                                                                                       'health-.05')],
 ("the carer's afternoon off", 'ask the neighbours to sit with them one afternoon a week, as streets once did'): [('person',
                                                                                                                   'neighbour')],
 ("the carer's afternoon off", 'tell the absent relatives plainly what the care costs, and what they owe'): [('means',
                                                                                                              'ties-.03')],
 ("the carer's afternoon off", 'take them out to the park and the café on every good day, whatever the effort'): [('lesson',
                                                                                                                   'good '
                                                                                                                   'days '
                                                                                                                   'are '
                                                                                                                   'worth '
                                                                                                                   'the '
                                                                                                                   'effort')],
 ("the carer's afternoon off", 'try every new aid, the hoist, the alarm, the bed sensor, to win back nights'): [('means',
                                                                                                                 'health+.03')],
 ("the carer's afternoon off", 'pay a care worker for two mornings a week, and keep your own job going'): [('means',
                                                                                                            'money-.06')],
 ("the carer's afternoon off", 'write up the whole care plan, so anyone could step in tomorrow'): [('means',
                                                                                                    'freedom+.03')],
 ('the first coins at the car-boot table', 'sell each toy at the price on its label, and count the change out loud'): [('lesson',
                                                                                                                        'honest '
                                                                                                                        'change '
                                                                                                                        'earns '
                                                                                                                        'trust')],
 ('the first coins at the car-boot table', 'move the toys that sell to the front, and mark down the rest'): [('mark',
                                                                                                              'learned '
                                                                                                              'a '
                                                                                                              'skill')],
 ('the first coins at the car-boot table', 'ask more from the buyers who look keen, and less from the ones who walk on'): [('lesson',
                                                                                                                            'keen '
                                                                                                                            'buyers '
                                                                                                                            'pay '
                                                                                                                            'more')],
 ('the first coins at the car-boot table', 'call out to every passer-by, and make them laugh until they stop'): [('person',
                                                                                                                  'regular')],
 ('the first coins at the car-boot table', 'give the best toy free to a small child whose parent cannot afford it'): [('mark',
                                                                                                                       'helped '
                                                                                                                       'someone '
                                                                                                                       'in '
                                                                                                                       'need')],
 ('the first coins at the car-boot table', 'keep a page of what sold and for how much, all morning'): [('door',
                                                                                                        'learned a '
                                                                                                        'skill')],
 ('the first coins at the car-boot table', 'stand up to the grown-up who tries to pay half the label price'): [('mark',
                                                                                                                'defied '
                                                                                                                'an '
                                                                                                                'authority')],
 ('the first coins at the car-boot table', 'swap a box of comics with the child at the next table instead of selling it'): [('person',
                                                                                                                             'friend')],
 ('the first coins at the car-boot table', 'auction the last three toys to the small crowd, and take the top bid'): [('place',
                                                                                                                      'comm.market')],
 ('the first coins at the car-boot table', 'put half the takings in the family tin, and keep the rest for yourself'): [('means',
                                                                                                                        'ties+.03')],
 ("the shop's opening day", 'open on the hour posted, and give the first customer honest weight and a receipt'): [('mark',
                                                                                                                   'kept '
                                                                                                                   'your '
                                                                                                                   'word')],
 ("the shop's opening day", 'log every customer who comes in, and what they ask for that you do not stock'): [('lesson',
                                                                                                               'the '
                                                                                                               'gaps '
                                                                                                               'show '
                                                                                                               'what '
                                                                                                               'sells')],
 ("the shop's opening day", 'stand at the door yourself, and talk every passer-by into one small purchase'): [('means',
                                                                                                               'money+.03')],
 ("the shop's opening day", 'hand out free samples on the step, with music playing, until a crowd comes'): [('means',
                                                                                                             'money-.03')],
 ("the shop's opening day", 'give the first sale to the old grocer across the road, and refuse his money'): [('person',
                                                                                                              'neighbour')],
 ("the shop's opening day", "frame the first note taken, and pin the shop's terms beside it"): [('door',
                                                                                                 'kept your word')],
 ("the shop's opening day", 'put a price board in the window, and dare the big shops to beat it'): [('person',
                                                                                                     'rival')],
 ("the shop's opening day", "note which neighbours buy most, and offer them a regulars' card by the afternoon"): [('person',
                                                                                                                   'regular')],
 ("the shop's opening day", 'ask each customer what the street is missing, and order it in for next week'): [('means',
                                                                                                              'ties+.03')],
 ("the shop's opening day", 'close at noon for a party on the pavement, with the whole street invited'): [('means',
                                                                                                           'ties+.06')],
 ('the regular who never pays', 'work out with him what he can pay each week, and write it down'): [('door',
                                                                                                     'helped someone '
                                                                                                     'in need')],
 ('the regular who never pays', 'keep his basket behind the till until he pays something today'): [('means',
                                                                                                    'money+.03')],
 ('the regular who never pays', 'tell him in front of the whole queue that he owes you the winter'): [('person',
                                                                                                       'rival')],
 ('the regular who never pays', 'serve him as always, and trust him to pay when he can'): [('means', 'money-.06')],
 ('the regular who never pays', 'send him a plain written account, with dates, and a fair day to settle'): [('lesson',
                                                                                                             'put '
                                                                                                             'the '
                                                                                                             'debt '
                                                                                                             'in '
                                                                                                             'writing')],
 ('the regular who never pays', 'take the debt to the small claims hearing at the town hall'): [('door',
                                                                                                 'made an enemy')],
 ('the regular who never pays', 'sell the debt to a collector for half, and be done with it'): [('means',
                                                                                                 'money+.06')],
 ('the regular who never pays', 'strike it from the book with a laugh, and ask him to bring his wife'): [('person',
                                                                                                          'friend')],
 ('the regular who never pays', 'take his old bicycle as surety until the page is paid'): [('lesson',
                                                                                            'a pledge makes promises '
                                                                                            'real')],
 ('the keys of the shop to a grown child', "write down the shop's terms and suppliers, and hand them over with the keys"): [('means',
                                                                                                                             'freedom+.06')],
 ('the keys of the shop to a grown child', 'go through thirty years of the books together, one season at a time'): [('lesson',
                                                                                                                     'the '
                                                                                                                     'books '
                                                                                                                     'tell '
                                                                                                                     'the '
                                                                                                                     'story')],
 ('the keys of the shop to a grown child', 'keep the lease in your own name for five more years, and see how it goes'): [('means',
                                                                                                                          'money+.03')],
 ('the keys of the shop to a grown child', 'hand over the keys, and leave on a long trip the next morning'): [('means',
                                                                                                               'freedom+.10')],
 ('the keys of the shop to a grown child', 'stand behind the counter one day a week, so the regulars see the hand-over'): [('place',
                                                                                                                            'comm.shop')],
 ('the keys of the shop to a grown child', 'tell each regular yourself, and ask them to give the new ways a fair try'): [('means',
                                                                                                                          'ties+.03')],
 ('the keys of the shop to a grown child', 'hold a farewell day at the old prices, and announce the hand-over from the step'): [('means',
                                                                                                                                 'money-.03')],
 ('the keys of the shop to a grown child', 'sell the shop to your child at a fair valuation, with the papers drawn up properly'): [('means',
                                                                                                                                    'money+.10')],
 ('the keys of the shop to a grown child', 'learn the phone orders alongside your child, and try the new way first'): [('mark',
                                                                                                                        'learned '
                                                                                                                        'a '
                                                                                                                        'skill')],
 ('the keys of the shop to a grown child', 'collect the old debts in the tab book yourself before handing over'): [('person',
                                                                                                                    'regular '
                                                                                                                    'lost')],
 ('the first signature on monthly payments', 'read the agreement through with the clerk, line by line, before you sign'): [('lesson',
                                                                                                                            'read '
                                                                                                                            'before '
                                                                                                                            'you '
                                                                                                                            'sign')],
 ('the first signature on monthly payments', 'take the papers home, compare the total with two other shops, and come back'): [('means',
                                                                                                                               'money+.06')],
 ('the first signature on monthly payments', 'tell the clerk you will sign today if the interest comes off'): [('means',
                                                                                                                'money+.03')],
 ('the first signature on monthly payments', 'sign with a flourish, and have the sofa on Friday'): [('means',
                                                                                                     'money-.06')],
 ('the first signature on monthly payments', "take the old sofa from the family's spare room, and sign only for the bed"): [('means',
                                                                                                                             'ties+.03')],
 ('the first signature on monthly payments', 'pay a large deposit now, so the payments end in a year'): [('means',
                                                                                                          'money-.10')],
 ('the first signature on monthly payments', 'set up a household fund with your partner, and pay each month from it together'): [('door',
                                                                                                                                  'kept '
                                                                                                                                  'your '
                                                                                                                                  'word')],
 ('the first signature on monthly payments', 'find the offer with no interest if paid inside a year, and plan to beat it'): [('door',
                                                                                                                              'took '
                                                                                                                              'a '
                                                                                                                              'wild '
                                                                                                                              'risk')],
 ('the first signature on monthly payments', 'walk out, buy it all second hand online that evening, and owe nothing'): [('means',
                                                                                                                         'freedom+.03')],
 ('the first signature on monthly payments', 'sign for the sofa, and throw a housewarming for everyone who helped with the move'): [('place',
                                                                                                                                     'gather.house')],
 ("the lender's yes or no", 'walk the lender through the honest figures, the bad months first'): [('door',
                                                                                                   'owned up')],
 ("the lender's yes or no", 'show how the risk is spread across three markets and two seasons'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ("the lender's yes or no", 'mention the other lender who is already interested, true or not'): [('door',
                                                                                                  'hid a wrong')],
 ("the lender's yes or no", 'tell the lender the story of the trial stall day that sold out by noon'): [('lesson',
                                                                                                         'a good '
                                                                                                         'story '
                                                                                                         'opens '
                                                                                                         'doors')],
 ("the lender's yes or no", 'bring letters from the regulars who have promised to buy from the van'): [('means',
                                                                                                        'ties+.03')],
 ("the lender's yes or no", 'ask what the bank needs for a yes, and come back in a month meeting it'): [('door',
                                                                                                         'kept your '
                                                                                                         'word')],
 ("the lender's yes or no", "ask the stallholders' savings circle to stand surety together"): [('place',
                                                                                                'comm.credit')],
 ("the lender's yes or no", 'walk out, and pay for the first van with orders taken in advance from the regulars'): [('means',
                                                                                                                     'freedom+.06')],
 ("the lender's yes or no", 'offer the lender a share of the takings instead of a fixed rate'): [('means',
                                                                                                  'money-.06')],
 ("the lender's yes or no", "put up the family's savings as surety, and borrow half as much"): [('door',
                                                                                                 'took a wild risk')],
 ('the pitch fee doubles', 'call a meeting of every stallholder, and ask the council to review the fee'): [('place',
                                                                                                            'rule.voice')],
 ('the pitch fee doubles', 'find out who bought the market, and what they mean to build on it'): [('lesson',
                                                                                                   'follow who owns '
                                                                                                   'the ground')],
 ('the pitch fee doubles', 'offer to take the empty pitches at the old rate, and wait the owners out'): [('door',
                                                                                                          'took a '
                                                                                                          'wild '
                                                                                                          'risk')],
 ('the pitch fee doubles', 'take the stall on the road to the fair towns, and leave the market behind'): [('means',
                                                                                                           'freedom+.06')],
 ('the pitch fee doubles', 'stay on at the new fee for the regulars who have bought from you for years'): [('means',
                                                                                                            'money-.06')],
 ('the pitch fee doubles', 'ask the lawyer two stalls down to read the old lease for a clause they broke'): [('door',
                                                                                                              'defied '
                                                                                                              'an '
                                                                                                              'authority')],
 ('the pitch fee doubles', "start a stallholders' co-op, and run your own market in the church car park"): [('place',
                                                                                                             'comm.market')],
 ('the pitch fee doubles', 'sell online through the week, and from the van at the market gate on Saturdays'): [('means',
                                                                                                                'time-.06')],
 ('the pitch fee doubles', 'sell off the stock at one great last market, and start again elsewhere'): [('means',
                                                                                                        'money+.06')],
 ('the order that makes the business', 'sign only for what you know you can deliver, and say so plainly'): [('mark',
                                                                                                             'kept '
                                                                                                             'your '
                                                                                                             'word')],
 ('the order that makes the business', 'ask for a week to cost the order, and come back with a plan'): [('lesson',
                                                                                                         'cost it '
                                                                                                         'before you '
                                                                                                         'promise')],
 ('the order that makes the business', 'say yes, and hold out for a better price per jar before signing'): [('means',
                                                                                                             'money+.06')],
 ('the order that makes the business', 'ask the neighbours who grow the tomatoes whether they can grow ten times as many'): [('person',
                                                                                                                              'neighbour')],
 ('the order that makes the business', 'have someone you trust read the contract, clause by clause, before signing'): [('lesson',
                                                                                                                        'read '
                                                                                                                        'every '
                                                                                                                        'clause '
                                                                                                                        'twice')],
 ('the order that makes the business', 'borrow from the family against the contract, and build a proper kitchen'): [('means',
                                                                                                                     'money-.10')],
 ('the order that makes the business', 'offer the buyer a new recipe that nobody else makes, at a higher price'): [('door',
                                                                                                                    'took '
                                                                                                                    'a '
                                                                                                                    'wild '
                                                                                                                    'risk')],
 ('the order that makes the business', 'keep the old customers first, and give the chain only what is left'): [('door',
                                                                                                                'turned '
                                                                                                                'down '
                                                                                                                'a '
                                                                                                                'chance')],
 ('the order that makes the business', 'throw a party for the growers and the kitchen, then hire them all'): [('person',
                                                                                                               'colleague')],
 ('the bargain that was a cheat', "report the sale to the consumer office, with the mechanic's written report"): [('lesson',
                                                                                                                   'complaints '
                                                                                                                   'count '
                                                                                                                   'in '
                                                                                                                   'writing')],
 ('the bargain that was a cheat', "find the car's old service records, and prove what the mileage really was"): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ('the bargain that was a cheat', 'go round with the report and offer him a quiet deal: half back, or court'): [('means',
                                                                                                                 'money+.06')],
 ('the bargain that was a cheat', 'warn everyone you know, and ask who else has bought from him'): [('means',
                                                                                                     'ties+.06')],
 ('the bargain that was a cheat', 'gather the others he cheated, and take him to the small claims court together'): [('person',
                                                                                                                      'friend')],
 ('the bargain that was a cheat', 'stand by his car lot on Saturday morning, and tell every buyer what he did'): [('person',
                                                                                                                   'rival')],
 ('the bargain that was a cheat', 'sell the car to a breaker for parts, and learn what to check next time'): [('means',
                                                                                                               'money-.06')],
 ('the bargain that was a cheat', 'have the mechanic teach you to check a car, and help friends buy theirs'): [('person',
                                                                                                                'mentor')],
 ('the bargain that was a cheat', 'answer his next advert, and confront him in front of the next buyer'): [('door',
                                                                                                            'made an '
                                                                                                            'enemy')],
 ('the last market day at the old pitch', 'sweep the pitch clean at closing, and hand the key back to the warden in person'): [('means',
                                                                                                                                'freedom+.06')],
 ('the last market day at the old pitch', "give the notebook of forty years' prices to the town library"): [('place',
                                                                                                             'learn.keeping')],
 ('the last market day at the old pitch', 'sell the pitch to the highest bidder among the waiting traders'): [('means',
                                                                                                               'money+.06')],
 ('the last market day at the old pitch', 'sell off the whole stock cheap by noon, and buy the round at the café'): [('lesson',
                                                                                                                      'end '
                                                                                                                      'the '
                                                                                                                      'day '
                                                                                                                      'laughing')],
 ('the last market day at the old pitch', 'give the last of the stock to the regulars as keepsakes'): [('means',
                                                                                                        'ties+.06')],
 ('the last market day at the old pitch', 'teach the youngest trader on the row to keep the books before you go'): [('person',
                                                                                                                     'friend')],
 ('the last market day at the old pitch', 'pass the pitch to the young trader at the top of the waiting list, for nothing'): [('mark',
                                                                                                                               'helped '
                                                                                                                               'someone '
                                                                                                                               'in '
                                                                                                                               'need')],
 ('the last market day at the old pitch', 'keep a share in the pitch, and let a younger trader run it for a cut'): [('means',
                                                                                                                     'money+.03')],
 ('the last market day at the old pitch', 'stay until the lamps go up, and dance with the stallholders round the brazier'): [('means',
                                                                                                                              'ties+.03')],
 ('the last market day at the old pitch', 'auction the old scales and the sign to the crowd, for the stories'): [('means',
                                                                                                                  'money+.03')],
 ('the first fast kept to the end', 'ask the teacher of the rite what the fast is really for, and write it down'): [('person',
                                                                                                                     'teacher')],
 ('the first fast kept to the end', 'keep it to the end, and make sure the whole family knows you did'): [('means',
                                                                                                           'ties+.03')],
 ('the first fast kept to the end', 'eat a secret biscuit behind the bike sheds, then carry on with the fast'): [('door',
                                                                                                                  'kept '
                                                                                                                  'it '
                                                                                                                  'hidden')],
 ('the first fast kept to the end', 'rise before dawn every day for the small meal with your grandparent'): [('lesson',
                                                                                                              'dawn '
                                                                                                              'is '
                                                                                                              'the '
                                                                                                              'quietest '
                                                                                                              'hour')],
 ('the first fast kept to the end', 'race your cousins to the evening table, and make every breaking of the fast a party'): [('means',
                                                                                                                              'ties+.03')],
 ('the first fast kept to the end', 'work out which hours are hardest, and plan each day around them'): [('lesson',
                                                                                                          'plan '
                                                                                                          'around '
                                                                                                          'the hard '
                                                                                                          'hours')],
 ('the first fast kept to the end', 'keep a diary of every hungry day, and what it makes you feel'): [('place',
                                                                                                       'arts.page')],
 ('the first fast kept to the end', 'help serve the evening meal for the poor, and eat only after they have'): [('mark',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('the first fast kept to the end', 'fast alongside your grandparent, and keep each other going to the last evening'): [('door',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('naming your own child', 'hold the full rite at the house of worship, and learn every line for the day'): [('place',
                                                                                                              'faith.congregation')],
 ('naming your own child', 'choose a name for what it means, and explain your reasons to both families'): [('lesson',
                                                                                                            'a name '
                                                                                                            'carries '
                                                                                                            'a '
                                                                                                            'story')],
 ('naming your own child', 'give the baby the family name first, and the name you wanted second'): [('door',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ('naming your own child', 'announce the name you love at the rite, before anyone can talk you out of it'): [('means',
                                                                                                              'ties-.03')],
 ('naming your own child', "give the baby a grandparent's name, as the first child always has"): [('lesson',
                                                                                                   'the old names '
                                                                                                   'come round '
                                                                                                   'again')],
 ('naming your own child', "hold the naming in the family's old house, and invite everyone who might help later"): [('means',
                                                                                                                     'ties+.06')],
 ('naming your own child', 'throw a naming party so big that the quarrel over the rite is forgotten'): [('means',
                                                                                                         'money-.06')],
 ('naming your own child', 'write a short rite of your own with your partner, and say it at home'): [('door',
                                                                                                      'defied an '
                                                                                                      'authority')],
 ('naming your own child', "keep the old rite, and add one new blessing in your partner's words"): [('means',
                                                                                                     'ties+.03')],
 ('naming your own child', 'sit both families down with the leader of the rite, and agree the order together'): [('person',
                                                                                                                  'elder')],
 ('a wedding without the old rite', 'marry at the town hall, then ask the elders for a blessing afterwards'): [('place',
                                                                                                                'faith.congregation')],
 ('a wedding without the old rite', 'write down why the rite would be a lie, and give it to your parents'): [('lesson',
                                                                                                              'saying '
                                                                                                              'it '
                                                                                                              'plainly '
                                                                                                              'on '
                                                                                                              'paper')],
 ('a wedding without the old rite', "agree to the rite in return for the family's help with the house"): [('means',
                                                                                                           'money+.06')],
 ('a wedding without the old rite', 'marry at the town hall next month, and send the family a photograph'): [('means',
                                                                                                              'ties-.06')],
 ('a wedding without the old rite', 'keep one old custom on the day, so the ancestors are not left out'): [('lesson',
                                                                                                            'old '
                                                                                                            'customs '
                                                                                                            'fit new '
                                                                                                            'days')],
 ('a wedding without the old rite', 'throw the best party the family has ever seen, rite or no rite'): [('means',
                                                                                                         'money-.06')],
 ('a wedding without the old rite', 'ask the oldest relative which customs are older than the faith, and keep those'): [('person',
                                                                                                                         'elder')],
 ('a wedding without the old rite', 'make up a ceremony of your own on a hilltop, in words you both wrote'): [('door',
                                                                                                               'defied '
                                                                                                               'an '
                                                                                                               'authority')],
 ('a wedding without the old rite', 'strike a deal with your parents: the town hall now, the rite at the first child'): [('door',
                                                                                                                          'kept '
                                                                                                                          'your '
                                                                                                                          'word')],
 ('a wedding without the old rite', 'visit your parents every week until the wedding, and listen more than you talk'): [('means',
                                                                                                                         'ties+.06')],
 ('telling the family you have left the faith', 'tell your parents together, gently and honestly, and answer every question'): [('door',
                                                                                                                                 'owned '
                                                                                                                                 'up')],
 ('telling the family you have left the faith', 'write it all in a letter, so they can read your reasons in their own time'): [('lesson',
                                                                                                                                'some '
                                                                                                                                'things '
                                                                                                                                'read '
                                                                                                                                'better '
                                                                                                                                'than '
                                                                                                                                'said')],
 ('telling the family you have left the faith', 'say nothing yet, and let them find out slowly, when you are ready'): [('door',
                                                                                                                        'kept '
                                                                                                                        'it '
                                                                                                                        'hidden')],
 ('telling the family you have left the faith', 'say it at the table before the meal is served, and let it land'): [('means',
                                                                                                                     'ties-.06')],
 ('telling the family you have left the faith', 'tell them you have left, and promise to come home for every feast'): [('door',
                                                                                                                        'came '
                                                                                                                        'home')],
 ('telling the family you have left the faith', 'tell your grandparent first, and let them soften the ground with your parents'): [('means',
                                                                                                                                    'ties+.03')],
 ('telling the family you have left the faith', 'tell them on a walk in the garden, and cry together if it comes to that'): [('lesson',
                                                                                                                              'tears '
                                                                                                                              'can '
                                                                                                                              'say '
                                                                                                                              'it '
                                                                                                                              'too')],
 ('telling the family you have left the faith', 'answer their hardest questions honestly, even the ones that hurt you both'): [('means',
                                                                                                                                'ties-.03')],
 ('telling the family you have left the faith', 'agree with your sibling exactly what each of you will say, and stick to it'): [('door',
                                                                                                                                 'kept '
                                                                                                                                 'your '
                                                                                                                                 'word')],
 ('telling the family you have left the faith', 'ask the elder your parents trust most to sit in when you tell them'): [('person',
                                                                                                                         'elder')],
 ('a vow made before the gathering', 'ask the elders whether a vow can be changed honestly, rather than broken'): [('person',
                                                                                                                    'elder')],
 ('a vow made before the gathering', 'spend Saturday with your grandparent instead, and hear how they kept theirs'): [('lesson',
                                                                                                                       'an '
                                                                                                                       'old '
                                                                                                                       'vow '
                                                                                                                       'kept '
                                                                                                                       'quietly')],
 ('a vow made before the gathering', 'throw the birthday party yourself, at your place, with no drink in the house'): [('place',
                                                                                                                        'gather.house')],
 ('a vow made before the gathering', 'take your friend up the hills for the birthday, with a fire and tea'): [('means',
                                                                                                               'ties+.03')],
 ('a vow made before the gathering', 'read what the old teachers wrote about vows, and keep yours in their spirit'): [('lesson',
                                                                                                                       'a '
                                                                                                                       'vow '
                                                                                                                       'lives '
                                                                                                                       'in '
                                                                                                                       'its '
                                                                                                                       'spirit')],
 ('a vow made before the gathering', 'ask an elder to stand by you, and ring them whenever it gets hard'): [('person',
                                                                                                             'mentor')],
 ('a vow made before the gathering', "keep a written count of every day kept, and read it out at the year's end"): [('door',
                                                                                                                     'kept '
                                                                                                                     'your '
                                                                                                                     'word')],
 ('the twelfth day on the pilgrim road', 'walk the next days in silence, and listen to what comes'): [('lesson',
                                                                                                       'quiet '
                                                                                                       'walking '
                                                                                                       'clears the '
                                                                                                       'head')],
 ('the twelfth day on the pilgrim road', 'bargain a bed at the full hostel, and get your friend one too'): [('means',
                                                                                                             'money-.03')],
 ('the twelfth day on the pilgrim road', 'stride off alone at first light, and meet the group at the shrine'): [('means',
                                                                                                                 'ties-.03')],
 ('the twelfth day on the pilgrim road', 'sleep under the stars by the old waymark, as the first pilgrims did'): [('place',
                                                                                                                   'faith.shrines')],
 ('the twelfth day on the pilgrim road', 'fall in with the old hands who know the road, and learn its short cuts'): [('person',
                                                                                                                      'mentor')],
 ('the twelfth day on the pilgrim road', "ask a farmer about the road's oldest stretch, and walk what the guidebooks skip"): [('lesson',
                                                                                                                               'the '
                                                                                                                               'oldest '
                                                                                                                               'road '
                                                                                                                               'goes '
                                                                                                                               'unmapped')],
 ('the twelfth day on the pilgrim road', "take charge of the group's pace and money, so nobody is left behind"): [('means',
                                                                                                                   'ties+.06')],
 ('the first night out at eighteen', 'keep the group together all night, and see everyone home safe'): [('mark',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('the first night out at eighteen', 'stay near the edge for the first hour, and watch how the place works'): [('lesson',
                                                                                                                'watch '
                                                                                                                'the '
                                                                                                                'room '
                                                                                                                'first')],
 ('the first night out at eighteen', 'make sure you are seen with the right crowd, and leave with their numbers'): [('means',
                                                                                                                     'ties+.06')],
 ('the first night out at eighteen', 'dance from the first song until the lights come on'): [('person', 'friend')],
 ('the first night out at eighteen', 'start at the corner bar where your cousins started, and toast them there'): [('place',
                                                                                                                    'gather.night')],
 ('the first night out at eighteen', 'agree the plan with everyone first: one meeting place, one taxi, one time home'): [('means',
                                                                                                                          'ties+.03')],
 ('the first night out at eighteen', 'talk the door staff round when they stop the youngest of your group'): [('mark',
                                                                                                               'helped '
                                                                                                               'someone '
                                                                                                               'in '
                                                                                                               'need')],
 ('the first night out at eighteen', 'find out where the good crowd goes on which night, and follow it there'): [('place',
                                                                                                                  'gather.night')],
 ('the first night out at eighteen', 'leave the club at three with everyone, and watch the sun come up from the hill'): [('lesson',
                                                                                                                          'the '
                                                                                                                          'best '
                                                                                                                          'part '
                                                                                                                          'comes '
                                                                                                                          'after')],
 ('the first night out at eighteen', 'make one drink last all night, and get to know the barman instead'): [('person',
                                                                                                             'keeper')],
 ('turned away at the door', 'ask the doorman calmly which rule you broke, and wait for an answer'): [('door',
                                                                                                       'defied an '
                                                                                                       'authority')],
 ('turned away at the door', 'watch the door for ten minutes, and work out whom it lets in and why'): [('lesson',
                                                                                                        'who gets in '
                                                                                                        'follows a '
                                                                                                        'pattern')],
 ('turned away at the door', 'ring the friend of a friend who knows the manager, and get put on the list'): [('person',
                                                                                                              'go-between')],
 ('turned away at the door', 'tell the doorman what you think of him, loudly, and walk off down the street'): [('person',
                                                                                                                'rival')],
 ('turned away at the door', 'text the others to meet at the old corner bar, where everyone gets in'): [('place',
                                                                                                         'gather.house')],
 ('turned away at the door', 'write a plain, fair account of the door, and ask who else it has happened to'): [('place',
                                                                                                                'rule.voice')],
 ('turned away at the door', "come back next week in the right clothes, learn the doorman's name, and be let in"): [('door',
                                                                                                                     'gave '
                                                                                                                     'in '
                                                                                                                     'to '
                                                                                                                     'pressure')],
 ('turned away at the door', 'start an open night of your own in a cellar, with no list and no door'): [('place',
                                                                                                         'gather.night')],
 ('turned away at the door', 'take the group to the park with music on a phone, and dance under the trees'): [('means',
                                                                                                               'ties+.03')],
 ('turned away at the door', 'shrug it off, and make a night of it at the late café by the market'): [('person',
                                                                                                       'regular')],
 ('the old bar is sold', 'make a list of every regular, and find each one a table somewhere new'): [('mark',
                                                                                                     'helped someone '
                                                                                                     'in need')],
 ('the old bar is sold', 'look up the sale at the council, and find out whether it can be stopped'): [('place',
                                                                                                       'rule.counsel')],
 ('the old bar is sold', 'ask the keeper about taking on the licence, and find two backers by Saturday'): [('person',
                                                                                                            'patron')],
 ('the old bar is sold', 'plan the loudest last night the street has heard, with a band and a midnight toast'): [('means',
                                                                                                                  'ties+.03')],
 ('the old bar is sold', 'ask the buyers for the long table, and carry it home with the regulars'): [('place',
                                                                                                      'gather.house')],
 ('the old bar is sold', 'call a meeting of the regulars, and put to a vote where the group goes next'): [('person',
                                                                                                           'regular')],
 ('the old bar is sold', 'move the Thursday table, rota and all, to the café across the road'): [('person',
                                                                                                  'keeper')],
 ('the old bar is sold', 'put on a night of stories about the old place, and record every one'): [('place',
                                                                                                   'arts.tale')],
 ('the old bar is sold', 'buy the old sign, and hang it over a back room you rent yourself'): [('means',
                                                                                                'money-.06')],
 ('the old bar is sold', 'let it go, and become a regular at the next nearest bar within the month'): [('place',
                                                                                                        'gather.night')],
 ('the toast at the wedding', 'name everyone who helped the couple, and leave nobody out'): [('mark',
                                                                                              'kept your word')],
 ('the toast at the wedding', 'write it out, try it on three friends, and cut every line that rings false'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the toast at the wedding', 'keep it short, polished and funny, and work the right tables afterwards'): [('person',
                                                                                                            'patron')],
 ('the toast at the wedding', 'throw away the notes, and say what you feel about your friend'): [('mark',
                                                                                                  'took a wild '
                                                                                                  'risk')],
 ('the toast at the wedding', 'tell the story of the two families, and raise a glass to the grandparents'): [('person',
                                                                                                              'elder')],
 ('the toast at the wedding', 'tell the one embarrassing story everyone knows anyway, and let the room laugh along'): [('lesson',
                                                                                                                        'a '
                                                                                                                        'shared '
                                                                                                                        'laugh '
                                                                                                                        'carries '
                                                                                                                        'a '
                                                                                                                        'room')],
 ('the toast at the wedding', "ask the couple's grandparents how they met, and build the toast round it"): [('lesson',
                                                                                                             'how '
                                                                                                             'they '
                                                                                                             'met '
                                                                                                             'says '
                                                                                                             'much')],
 ('the toast at the wedding', 'write a short funny poem about the couple, and lead the room in its last line'): [('means',
                                                                                                                  'ties+.03')],
 ('the toast at the wedding', 'toast the couple, thank the hosts and the cooks, and pass the hat for the honeymoon'): [('means',
                                                                                                                        'money-.03')],
 ('the toast at the wedding', "call the couple's oldest friends to their feet to raise their glasses together"): [('person',
                                                                                                                   'friend')],
 ('leaving school for a wage', 'take the job, and hand the wage to the family every Friday'): [('mark',
                                                                                                'helped someone in '
                                                                                                'need')],
 ('leaving school for a wage', 'ask the school about night classes, so you can sit the exams while working'): [('place',
                                                                                                                'learn.higher')],
 ('leaving school for a wage', 'take the job, and keep back enough of each wage to build something of your own'): [('means',
                                                                                                                    'money+.06')],
 ('leaving school for a wage', 'walk out of school on Friday, and turn up at the warehouse on Monday'): [('door',
                                                                                                          'turned '
                                                                                                          'down a '
                                                                                                          'chance')],
 ('leaving school for a wage', 'ask the grandparents what to do, and do whatever the family decides'): [('lesson',
                                                                                                         'the family '
                                                                                                         'decides '
                                                                                                         'together')],
 ('leaving school for a wage', "take the job an uncle's friend offers, where the family can keep an eye on you"): [('person',
                                                                                                                    'boss')],
 ('leaving school for a wage', 'stay at school, and learn the family trade from a grandparent at weekends'): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('leaving school for a wage', 'find a weekend job that pays nearly as much, and stay on at school'): [('means',
                                                                                                        'money+.03')],
 ('leaving school for a wage', 'ask the warehouse to hold the place a year, and work every Saturday until then'): [('door',
                                                                                                                    'kept '
                                                                                                                    'your '
                                                                                                                    'word')],
 ('leaving school for a wage', 'tell your parent straight out that you mean to finish school, and why'): [('lesson',
                                                                                                           'say it '
                                                                                                           'plainly '
                                                                                                           'with '
                                                                                                           'reasons')],
 ("the first year at the master's bench", 'do every task to the letter, and ask when the next stage of training begins'): [('lesson',
                                                                                                                            'doing '
                                                                                                                            'it '
                                                                                                                            'right '
                                                                                                                            'gets '
                                                                                                                            'noticed')],
 ("the first year at the master's bench", 'make yourself useful to the best customers, so they ask for you by name'): [('person',
                                                                                                                        'regular')],
 ("the first year at the master's bench", 'stay late and try the real work on the scrap pieces, without asking'): [('mark',
                                                                                                                    'learned '
                                                                                                                    'a '
                                                                                                                    'skill')],
 ("the first year at the master's bench", 'sweep and watch without complaint, the way the master was taught before you'): [('lesson',
                                                                                                                            'patience '
                                                                                                                            'comes '
                                                                                                                            'before '
                                                                                                                            'the '
                                                                                                                            'real '
                                                                                                                            'work')],
 ("the first year at the master's bench", 'make something small at home with the old family tools, and bring it in to show'): [('place',
                                                                                                                                'arts.craft')],
 ("the first year at the master's bench", 'learn the one skill nobody else in the shop has bothered to master'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ("the first year at the master's bench", 'go and watch how another workshop does the job, on your day off'): [('person',
                                                                                                                'colleague')],
 ("the first year at the master's bench", 'ask the master, politely, for a date to start on real work'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ("the first year at the master's bench", 'help the older apprentice with their jobs, and learn from them in turn'): [('person',
                                                                                                                       'friend')],
 ('the final piece before the judges', 'answer every question plainly, and show the judges each step of the work'): [('lesson',
                                                                                                                      'plain '
                                                                                                                      'answers '
                                                                                                                      'carry '
                                                                                                                      'weight')],
 ('the final piece before the judges', 'point out the flaw yourself, and explain how you would fix it'): [('lesson',
                                                                                                           'naming a '
                                                                                                           'flaw '
                                                                                                           'builds '
                                                                                                           'trust')],
 ('the final piece before the judges', "lead with the piece's strongest part, and steer the judges past its weak one"): [('door',
                                                                                                                          'kept '
                                                                                                                          'it '
                                                                                                                          'hidden')],
 ('the final piece before the judges', 'defend the risky change you made last week, with all the fire you have'): [('mark',
                                                                                                                    'took '
                                                                                                                    'a '
                                                                                                                    'wild '
                                                                                                                    'risk')],
 ('the final piece before the judges', 'tell the judges whose way of working you learned, and stand on it'): [('means',
                                                                                                               'ties+.03')],
 ('the final piece before the judges', 'turn the afternoon into a show the judges will talk about for years'): [('means',
                                                                                                                 'ties+.06')],
 ('the final piece before the judges', 'lay out the old pattern books the work was drawn from, page by page'): [('place',
                                                                                                                 'learn.keeping')],
 ('the final piece before the judges', 'ask the judges to try the piece for themselves, there and then'): [('mark',
                                                                                                            'took a '
                                                                                                            'wild '
                                                                                                            'risk')],
 ('the final piece before the judges', 'bring letters from the master and from clients, and set them on the table'): [('person',
                                                                                                                       'patron')],
 ('the final piece before the judges', 'thank your master before the judges, before a single word about the piece'): [('means',
                                                                                                                       'ties+.03')],
 ('the first in the family to graduate', 'thank your family by name when the graduates are asked to stand'): [('means',
                                                                                                               'ties+.06')],
 ('the first in the family to graduate', 'spend the evening explaining to the family what you studied, and why it matters'): [('lesson',
                                                                                                                               'share '
                                                                                                                               'what '
                                                                                                                               'you '
                                                                                                                               'learned')],
 ('the first in the family to graduate', 'leave the family lunch early to meet the people who can help your career'): [('person',
                                                                                                                        'patron')],
 ('the first in the family to graduate', 'skip the smart lunch, and take the whole family for a loud meal you cannot afford'): [('means',
                                                                                                                                 'money-.03')],
 ('the first in the family to graduate', "hang the certificate in your parents' front room, where the whole street will see it"): [('lesson',
                                                                                                                                    'the '
                                                                                                                                    'whole '
                                                                                                                                    'family '
                                                                                                                                    'earned '
                                                                                                                                    'it')],
 ('the first in the family to graduate', 'throw a party on the home street, and invite every neighbour who ever helped'): [('person',
                                                                                                                            'neighbour')],
 ('the first in the family to graduate', 'ask the grandparents for the story of why none of them could study'): [('means',
                                                                                                                  'ties+.03')],
 ('the first in the family to graduate', 'set up a small fund so the next cousin can study without your debts'): [('means',
                                                                                                                   'money-.06')],
 ('the first in the family to graduate', 'go back to your old school, and tell the pupils there that it can be done'): [('person',
                                                                                                                         'teacher')],
 ('the old well that never ran dry', 'tell the council at once, and ask for a fair rota at the well'): [('place',
                                                                                                         'rule.counsel')],
 ('the old well that never ran dry', 'bring the engineers to see it, and find out why their maps missed it'): [('lesson',
                                                                                                                'maps '
                                                                                                                'can '
                                                                                                                'miss '
                                                                                                                'things')],
 ('the old well that never ran dry', 'keep the key yourself, and decide who draws water from the well'): [('person',
                                                                                                           'rival')],
 ('the old well that never ran dry', 'clear the well out yourself this weekend, with whoever turns up to help'): [('person',
                                                                                                                   'neighbour')],
 ('the old well that never ran dry', "clean the spring the old way, and say your grandfather's words over it"): [('lesson',
                                                                                                                  'a '
                                                                                                                  'kept '
                                                                                                                  'spring '
                                                                                                                  'keeps '
                                                                                                                  'giving')],
 ('the old well that never ran dry', 'have the council name the well after your family before you hand it over'): [('means',
                                                                                                                    'ties+.03')],
 ('the old well that never ran dry', 'stand up at the town meeting, and tell the engineers to their faces they were wrong'): [('mark',
                                                                                                                               'defied '
                                                                                                                               'an '
                                                                                                                               'authority')],
 ('the old well that never ran dry', 'test the water with a kit from the shop, and post the results for the town'): [('mark',
                                                                                                                      'learned '
                                                                                                                      'a '
                                                                                                                      'skill')],
 ('the old well that never ran dry', 'teach the children at the school how to find and keep a spring'): [('means',
                                                                                                          'ties+.06')],
 ('the old well that never ran dry', 'write down all the old ones said about water, and give it to the library'): [('place',
                                                                                                                    'learn.keeping')],
 ('a row of your own on the family plot', 'pick it all and share it out at supper, a fair helping for everyone'): [('means',
                                                                                                                    'ties+.03')],
 ('a row of your own on the family plot', 'set out a box of beans at the farm gate with a price you chose'): [('lesson',
                                                                                                               'a '
                                                                                                               'fair '
                                                                                                               'price '
                                                                                                               'sells')],
 ('a row of your own on the family plot', 'leave the marrow on the vine to see how huge it can get'): [('lesson',
                                                                                                        'waiting can '
                                                                                                        'be '
                                                                                                        'exciting')],
 ('a row of your own on the family plot', 'save seeds from the best plants for next spring, the way your grandparent does'): [('mark',
                                                                                                                               'learned '
                                                                                                                               'a '
                                                                                                                               'skill')],
 ('a row of your own on the family plot', 'turn the bruised ones into jam and give the tops to the hens'): [('place',
                                                                                                             'prod.land')],
 ('a row of your own on the family plot', 'swap the strawberries at school for whatever you want most that week'): [('person',
                                                                                                                     'friend')],
 ('a row of your own on the family plot', "weigh every picking on the kitchen scales and keep the family's harvest list"): [('means',
                                                                                                                             'time-.03')],
 ("the test piece on the judges' bench", 'tell the judges about the gap before they find it'): [('lesson',
                                                                                                 'say it before they '
                                                                                                 'see it')],
 ("the test piece on the judges' bench", 'set the piece in the light so the eye goes to its best side'): [('door',
                                                                                                           'kept it '
                                                                                                           'hidden')],
 ("the test piece on the judges' bench", 'finish it exactly the way your mentor taught, step by careful step'): [('mark',
                                                                                                                  'learned '
                                                                                                                  'a '
                                                                                                                  'skill')],
 ("the test piece on the judges' bench", 'put the rule away and finish the joint by feel, as your hands tell you'): [('lesson',
                                                                                                                      'hands '
                                                                                                                      'know '
                                                                                                                      'more '
                                                                                                                      'than '
                                                                                                                      'rules')],
 ("the test piece on the judges' bench", 'find out from past apprentices what these judges always mark down'): [('person',
                                                                                                                 'colleague')],
 ("the test piece on the judges' bench", 'pick a seasoned board from the old stock and read its grain before you cut'): [('mark',
                                                                                                                          'learned '
                                                                                                                          'a '
                                                                                                                          'skill')],
 ("the test piece on the judges' bench", 'ask the workshop to stand behind a second attempt if this one fails'): [('place',
                                                                                                                   'prod.craft')],
 ('hurt on the job', 'work out why the guard failed, and write down how to stop it next time'): [('lesson',
                                                                                                  'find the cause '
                                                                                                  'not the blame')],
 ('hurt on the job', 'let the family carry you through the weeks off, and heal properly'): [('means', 'health+.06')],
 ('hurt on the job', 'take the payout, and look for work your hand can still do'): [('means', 'money+.06')],
 ('hurt on the job', 'spend the weeks off working your hand back into shape at the old bench at home'): [('place',
                                                                                                          'prod.craft')],
 ('hurt on the job', 'read the rules on claims, and claim every week of pay you are owed'): [('means', 'money+.03')],
 ('hurt on the job', 'ask for the inspector, and have every machine on the floor checked'): [('mark',
                                                                                              'defied an authority')],
 ('taking on your first hand', 'write a fair contract, the wage and the hours, before anyone starts'): [('door',
                                                                                                         'kept your '
                                                                                                         'word')],
 ('taking on your first hand', 'give each of them a trial day and keep the one who works best'): [('lesson',
                                                                                                   'the work shows '
                                                                                                   'who fits')],
 ('taking on your first hand', 'hire the one who will take the lowest wage, and keep the margin'): [('means',
                                                                                                     'money+.03')],
 ('taking on your first hand', 'hire the one you would most like to spend long days beside'): [('person', 'friend')],
 ('taking on your first hand', "take on the friend's daughter, and teach her the trade from the start"): [('person',
                                                                                                           'colleague')],
 ('taking on your first hand', 'pay someone by the job instead, and keep the workshop your own'): [('means',
                                                                                                    'freedom+.03')],
 ('taking on your first hand', "hire the one who worked at your rival's shop, and learn how they do it"): [('person',
                                                                                                            'colleague')],
 ('taking on your first hand', 'look for the one who learns fastest, and train them in your methods'): [('person',
                                                                                                         'colleague')],
 ('taking on your first hand', 'offer the new hand a share of the profits as well as the wage'): [('means',
                                                                                                   'money-.06')],
 ('no one to take the trade on', 'draw up a fair sale, and see that the hands keep their jobs'): [('mark',
                                                                                                   'helped someone '
                                                                                                   'in need')],
 ('no one to take the trade on', 'write down everything you know about the work, for whoever comes next'): [('lesson',
                                                                                                             'what '
                                                                                                             'you '
                                                                                                             'know '
                                                                                                             'outlives '
                                                                                                             'the '
                                                                                                             'work')],
 ('no one to take the trade on', 'sell to the highest bidder, and enjoy what you earned'): [('means', 'money+.10')],
 ('no one to take the trade on', 'lock the gate for a year, and take the long trip you always put off'): [('means',
                                                                                                           'freedom+.10')],
 ('no one to take the trade on', 'offer the place to the hired hand who loves it, though they are not kin'): [('means',
                                                                                                               'ties+.06')],
 ('no one to take the trade on', 'sell the land and the tools piece by piece, and let nothing go to waste'): [('means',
                                                                                                               'money+.03')],
 ('no one to take the trade on', 'keep the name and the recipes, and license them to a bigger firm'): [('means',
                                                                                                        'money+.06')],
 ('no one to take the trade on', 'turn the old barn into something new, a school for the trade or a maker space'): [('place',
                                                                                                                     'prod.craft')],
 ('no one to take the trade on', 'offer the whole place to the hands and the neighbours as a cooperative'): [('means',
                                                                                                              'money-.06')],
 ('no one to take the trade on', 'turn down the buyer who would close it, though they offer most, and say why'): [('lesson',
                                                                                                                   'some '
                                                                                                                   'offers '
                                                                                                                   'cost '
                                                                                                                   'too '
                                                                                                                   'much')],
 ('the first thing you made that sold', 'price the rest by the hours and the materials, no more and no less'): [('lesson',
                                                                                                                 'a '
                                                                                                                 'fair '
                                                                                                                 'price '
                                                                                                                 'is '
                                                                                                                 'simple '
                                                                                                                 'sums')],
 ('the first thing you made that sold', 'ask the buyer what made them choose it, and remember every word'): [('person',
                                                                                                              'regular')],
 ('the first thing you made that sold', 'raise the price on the rest of the row straight away'): [('means',
                                                                                                   'money+.03')],
 ('the first thing you made that sold', 'spend it that afternoon on something you have wanted for ages'): [('means',
                                                                                                            'money-.03')],
 ('the first thing you made that sold', 'go straight round to show your mentor the first sale'): [('means',
                                                                                                   'ties+.03')],
 ('the first thing you made that sold', 'make ten more before next weekend and take a stall of your own'): [('place',
                                                                                                             'comm.market')],
 ('the first thing you made that sold', 'make the next one by feel alone, with no pattern at all'): [('lesson',
                                                                                                      'the hands can '
                                                                                                      'lead')],
 ('the first thing you made that sold', 'work out which pieces sell best, and make only those'): [('means',
                                                                                                   'money+.06')],
 ('the first thing you made that sold', 'put your own mark on the base of every piece, and stand behind each one'): [('door',
                                                                                                                      'kept '
                                                                                                                      'your '
                                                                                                                      'word')],
 ('a backer for the workshop', 'have a lawyer write down every share and every duty before you sign'): [('person',
                                                                                                         'patron')],
 ('a backer for the workshop', 'look into every venture she has backed before you answer'): [('lesson',
                                                                                              'know who you deal '
                                                                                              'with')],
 ('a backer for the workshop', 'bargain until you keep the larger share and the last word'): [('means', 'money+.10')],
 ('a backer for the workshop', 'turn it down, and keep the freedom to make whatever you like'): [('means',
                                                                                                  'freedom+.06')],
 ('a backer for the workshop', 'ask the family to put in their savings instead, so it stays in the family'): [('means',
                                                                                                               'money+.06')],
 ('a backer for the workshop', 'stay small and keep making things the slow way, by hand'): [('lesson',
                                                                                             'small can be enough')],
 ('a backer for the workshop', 'take the money, but keep your methods out of the contract'): [('person', 'patron')],
 ('a backer for the workshop', 'take the money, build the bigger workshop, and hire from the town'): [('person',
                                                                                                       'patron'),
                                                                                                      ('person',
                                                                                                       'colleague')],
 ('a backer for the workshop', 'ask the hands and the regulars to buy in instead, a small share each'): [('means',
                                                                                                          'ties+.06')],
 ('the first arrest you make', 'caution him, arrest him by the book, and treat him with courtesy'): [('lesson',
                                                                                                      'courtesy '
                                                                                                      'holds even in '
                                                                                                      'an arrest')],
 ('the first arrest you make', 'ask him where the rest of the pipe has gone, and who buys it'): [('door',
                                                                                                  'made an enemy')],
 ('the first arrest you make', 'arrest him, and make sure the station knows it was your catch'): [('person',
                                                                                                   'rival')],
 ('the first arrest you make', 'stand between him and the gate, and talk him down until help comes'): [('mark',
                                                                                                        'took a wild '
                                                                                                        'risk')],
 ('the first arrest you make', 'ask his name and his street, and work out whose family he is'): [('person',
                                                                                                  'neighbour')],
 ('the first arrest you make', 'take him in, and tell the custody desk about the children'): [('mark',
                                                                                               'helped someone in '
                                                                                               'need')],
 ('the first arrest you make', 'walk him to the van yourself, talking all the way, so he stays calm'): [('lesson',
                                                                                                         'calm words '
                                                                                                         'keep '
                                                                                                         'people '
                                                                                                         'calm')],
 ('the first arrest you make', 'offer to put in a good word if he names the buyer'): [('door', 'kept your word')],
 ('the first arrest you make', 'radio it in at once, and keep him safe and still until the van comes'): [('person',
                                                                                                          'colleague')],
 ('the first arrest you make', 'write every word he says in the notebook before anything else'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ('the first day in uniform', 'say every word of the oath as if it binds you for life'): [('door', 'kept your word')],
 ('the first day in uniform', 'ask the instructors which postings teach most, and put in for one'): [('person',
                                                                                                      'teacher')],
 ('the first day in uniform', 'ask for the posting with the most overtime and the quickest promotion'): [('means',
                                                                                                          'money+.06')],
 ('the first day in uniform', 'ask for the busiest station in the city, starting tomorrow'): [('place',
                                                                                               'prot.watch')],
 ('the first day in uniform', 'keep your training notes, and go over the rules again each night'): [('mark',
                                                                                                     'learned a '
                                                                                                     'skill')],
 ('the first day in uniform', 'volunteer for the night response team from the first week'): [('person', 'colleague')],
 ('the first day in uniform', 'ask an old officer from home what the job was like in their day'): [('person',
                                                                                                    'elder')],
 ('the first day in uniform', 'ask the veteran instructor for the plain truth about the work'): [('person',
                                                                                                  'mentor')],
 ('the farewell at the barracks fence', 'stand straight and wave until the bus is gone, as the families do'): [('means',
                                                                                                                'ties+.03')],
 ('the farewell at the barracks fence', 'ask how and when you can reach them out there, and write it all down'): [('person',
                                                                                                                   'go-between')],
 ('the farewell at the barracks fence', 'slip them some money for the posting, and say only what helps'): [('means',
                                                                                                            'money-.03')],
 ('the farewell at the barracks fence', 'push through to the front, and hug them one last time'): [('lesson',
                                                                                                    'say it while '
                                                                                                    'you can')],
 ('the farewell at the barracks fence', "give them the family's old keepsake to carry, and ask for it back"): [('door',
                                                                                                                'came '
                                                                                                                'home')],
 ('the farewell at the barracks fence', 'tell them plainly to keep their head down and just come home'): [('lesson',
                                                                                                           'plain '
                                                                                                           'words '
                                                                                                           'carry '
                                                                                                           'far')],
 ('the farewell at the barracks fence', 'set up one family chat, so news from the posting reaches everyone at once'): [('means',
                                                                                                                        'ties+.06')],
 ('the farewell at the barracks fence', 'record a message from everyone at home, for them to play on the first bad night'): [('door',
                                                                                                                              'helped '
                                                                                                                              'someone '
                                                                                                                              'in '
                                                                                                                              'need')],
 ('the farewell at the barracks fence', 'promise to look after the family at home until they are back'): [('door',
                                                                                                           'stayed '
                                                                                                           'home')],
 ('the farewell at the barracks fence', 'make them promise to write every week, and promise the same'): [('door',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('a comrade lost on the mountain road', 'carry the coffin with the section at the funeral, in full dress'): [('means',
                                                                                                               'ties+.06')],
 ('a comrade lost on the mountain road', 'read the report on the crash, and ask what would have stopped it'): [('mark',
                                                                                                                'learned '
                                                                                                                'a '
                                                                                                                'skill')],
 ('a comrade lost on the mountain road', 'keep your head down, and get through the posting in one piece'): [('means',
                                                                                                             'ties-.06')],
 ('a comrade lost on the mountain road', 'gather the section that night, and tell the stories out loud'): [('person',
                                                                                                            'friend')],
 ('a comrade lost on the mountain road', 'write to the family, and visit them on your next leave'): [('door',
                                                                                                      'kept your '
                                                                                                      'word')],
 ('a comrade lost on the mountain road', 'take the grief quietly, and keep the youngest in the section steady'): [('mark',
                                                                                                                   'helped '
                                                                                                                   'someone '
                                                                                                                   'in '
                                                                                                                   'need')],
 ('a comrade lost on the mountain road', 'drive with the whole section to the funeral in the home village'): [('lesson',
                                                                                                               'grief '
                                                                                                               'is '
                                                                                                               'lighter '
                                                                                                               'shared')],
 ('a comrade lost on the mountain road', 'push for a new rule on night driving, and test it on the next move'): [('mark',
                                                                                                                  'defied '
                                                                                                                  'an '
                                                                                                                  'authority')],
 ('a comrade lost on the mountain road', 'collect from the unit for the family, and see the pension comes through'): [('door',
                                                                                                                       'helped '
                                                                                                                       'someone '
                                                                                                                       'in '
                                                                                                                       'need')],
 ('a comrade lost on the mountain road', 'ask for a full inquiry, and give your evidence plainly'): [('door',
                                                                                                      'defied an '
                                                                                                      'authority')],
 ('home from the posting, and not the same', 'keep a strict routine at home, the way the posting ran'): [('means',
                                                                                                          'ties-.03')],
 ('home from the posting, and not the same', 'read up on what coming back does to people, and name what is happening'): [('lesson',
                                                                                                                          'naming '
                                                                                                                          'it '
                                                                                                                          'makes '
                                                                                                                          'it '
                                                                                                                          'smaller')],
 ('home from the posting, and not the same', 'say you are fine, and keep it to yourself'): [('door',
                                                                                             'kept it hidden')],
 ('home from the posting, and not the same', 'take the family to the coast for a week, and try to feel it all again'): [('means',
                                                                                                                         'money-.03')],
 ('home from the posting, and not the same', 'go back to the old haunts and the old faces, slowly, one by one'): [('person',
                                                                                                                   'friend')],
 ('home from the posting, and not the same', 'meet up with the old hands from the unit, who need nothing explained'): [('place',
                                                                                                                        'gather.circle')],
 ('home from the posting, and not the same', 'walk the hills every morning, alone, until the noise inside goes quiet'): [('means',
                                                                                                                          'health+.06')],
 ('home from the posting, and not the same', 'book yourself in at the clinic for returning soldiers, and go'): [('place',
                                                                                                                 'care.houses')],
 ('home from the posting, and not the same', 'put in for a home posting, and plan the next five years'): [('door',
                                                                                                           'stayed '
                                                                                                           'home')],
 ('home from the posting, and not the same', 'tell your partner the whole truth one night, however hard it is to say'): [('door',
                                                                                                                          'owned '
                                                                                                                          'up')],
 ('the names read at the stone', 'read every name slowly and clearly, exactly as it is cut in the stone'): [('lesson',
                                                                                                             'every '
                                                                                                             'name '
                                                                                                             'deserves '
                                                                                                             'its '
                                                                                                             'time')],
 ('the names read at the stone', 'find out something true about each name, and say a line for each'): [('place',
                                                                                                        'learn.keeping')],
 ('the names read at the stone', "read them, then press the councillors on the veterans' home before the cameras"): [('place',
                                                                                                                      'rule.voice')],
 ('the names read at the stone', 'say what nobody says out loud: what it cost, and who sent them'): [('mark',
                                                                                                      'defied an '
                                                                                                      'authority')],
 ('the names read at the stone', 'bring the families of the names to stand at the front'): [('means', 'ties+.06')],
 ('the names read at the stone', 'read the names, then take the youngest soldiers for a quiet drink after'): [('person',
                                                                                                               'friend')],
 ('the names read at the stone', 'turn the evening after into a loud night for the old unit, on you'): [('means',
                                                                                                         'money-.03')],
 ('the names read at the stone', "record the old hands' stories after the service, before they are lost"): [('person',
                                                                                                             'elder')],
 ('the names read at the stone', 'ask one relative from each family to lay a flower beside you'): [('means',
                                                                                                    'ties+.03')],
 ('the names read at the stone', 'get the stone corrected where one name has been spelled wrong for years'): [('place',
                                                                                                               'rule.counsel')],
 ('the first visit to a brother or sister inside', 'keep to every rule of the visit, so nothing stops the next one'): [('lesson',
                                                                                                                        'small '
                                                                                                                        'rules '
                                                                                                                        'keep '
                                                                                                                        'the '
                                                                                                                        'door '
                                                                                                                        'open')],
 ('the first visit to a brother or sister inside', 'ask what the days are like inside, and what would help them most'): [('door',
                                                                                                                          'helped '
                                                                                                                          'someone '
                                                                                                                          'in '
                                                                                                                          'need')],
 ('the first visit to a brother or sister inside', 'talk through the appeal and the lawyer, and what it will cost'): [('means',
                                                                                                                       'money-.10')],
 ('the first visit to a brother or sister inside', 'make them laugh about the old days for the whole hour'): [('lesson',
                                                                                                               'laughter '
                                                                                                               'fits '
                                                                                                               'in '
                                                                                                               'any '
                                                                                                               'room')],
 ('the first visit to a brother or sister inside', 'bring news of every cousin and aunt, so they know home is waiting'): [('means',
                                                                                                                           'ties+.06')],
 ('the first visit to a brother or sister inside', 'promise to come every week, whatever the bus fare and the queue'): [('door',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('the first visit to a brother or sister inside', 'find out about the college course inside, and how to get them a place'): [('person',
                                                                                                                               'go-between')],
 ('the first visit to a brother or sister inside', 'write them a long letter that night, saying all the room would not let you'): [('means',
                                                                                                                                    'ties+.03')],
 ('the first visit to a brother or sister inside', 'put money on their account each month, and keep a careful record'): [('means',
                                                                                                                          'money-.06')],
 ('the first visit to a brother or sister inside', 'make their room ready at home, for whenever they come out'): [('door',
                                                                                                                   'took '
                                                                                                                   'them '
                                                                                                                   'in')],
 ('the back door forced', 'report it at once, and give the police a full and honest list'): [('means', 'time-.03')],
 ('the back door forced', 'walk the house slowly, and work out how they got in and when'): [('lesson',
                                                                                             'a house shows its weak '
                                                                                             'spots')],
 ('the back door forced', 'fit the best locks and an alarm that week, whatever it costs'): [('means', 'money-.06')],
 ('the back door forced', 'knock on every door in the street tonight, asking who saw what'): [('person',
                                                                                               'neighbour')],
 ('the back door forced', 'go next door, and stay with the neighbours until the house feels safe'): [('person',
                                                                                                      'friend')],
 ('the back door forced', 'post the doorbell camera clips online, and offer a reward for the rings'): [('means',
                                                                                                        'money-.03')],
 ('the back door forced', 'ask the old neighbours what has changed on the street lately'): [('person', 'elder')],
 ('the back door forced', 'rig up lights and a homemade alarm that very night, and test them'): [('mark',
                                                                                                  'learned a skill')],
 ('the back door forced', 'chase the insurer and the police every week until the claim is settled'): [('means',
                                                                                                       'money+.03')],
 ('the back door forced', "start a phone tree with the neighbours, so the street watches each other's doors"): [('place',
                                                                                                                 'prot.watch')],
 ('the car in the ditch ahead', 'ring the emergency line, and set warning lights behind the crash'): [('door',
                                                                                                       'helped '
                                                                                                       'someone in '
                                                                                                       'need')],
 ('the car in the ditch ahead', 'check for fuel and smoke before you go near, and send others back'): [('lesson',
                                                                                                        'danger '
                                                                                                        'first, then '
                                                                                                        'help')],
 ('the car in the ditch ahead', 'take charge of the scene, and tell the next drivers where to stand'): [('lesson',
                                                                                                         'people '
                                                                                                         'follow a '
                                                                                                         'clear '
                                                                                                         'voice')],
 ('the car in the ditch ahead', 'film the scene from a safe distance, for the police and the insurers'): [('means',
                                                                                                           'ties-.03')],
 ('the car in the ditch ahead', 'flag down the farmer from the next field, who knows how this ditch floods'): [('person',
                                                                                                                'neighbour')],
 ('the car in the ditch ahead', 'get the stopped drivers working together: blankets, torches, the traffic'): [('person',
                                                                                                               'friend')],
 ('the car in the ditch ahead', 'go down with the first-aid kit, doing what the course taught you'): [('mark',
                                                                                                       'helped '
                                                                                                       'someone in '
                                                                                                       'need')],
 ('the old woman across the landing', 'follow the drill: close the door, take the stairs, report who is missing'): [('lesson',
                                                                                                                     'the '
                                                                                                                     'drill '
                                                                                                                     'is '
                                                                                                                     'for '
                                                                                                                     'tonight')],
 ('the old woman across the landing', 'check which floor the smoke is coming from before you choose a stair'): [('lesson',
                                                                                                                 'a '
                                                                                                                 'calm '
                                                                                                                 'look '
                                                                                                                 'picks '
                                                                                                                 'the '
                                                                                                                 'stair')],
 ('the old woman across the landing', 'ring her phone from the stairs while getting yourself clear'): [('person',
                                                                                                        'neighbour')],
 ('the old woman across the landing', 'take charge at the meeting point, and count the residents off the list'): [('means',
                                                                                                                   'ties+.03')],
 ('the pager goes at two in the morning', 'do exactly what the crew leader tells you, and nothing more'): [('person',
                                                                                                            'boss')],
 ('the pager goes at two in the morning', 'read the house as you pull up: the doors, the windows, where people sleep'): [('mark',
                                                                                                                          'learned '
                                                                                                                          'a '
                                                                                                                          'skill')],
 ('the pager goes at two in the morning', 'stay with the pump and the hoses, the job you know best'): [('lesson',
                                                                                                        'the known '
                                                                                                        'job still '
                                                                                                        'matters')],
 ('the pager goes at two in the morning', 'look after the family on the pavement, with blankets and names, while the crew works'): [('mark',
                                                                                                                                     'helped '
                                                                                                                                     'someone '
                                                                                                                                     'in '
                                                                                                                                     'need')],
 ('the pager goes at two in the morning', 'take the hose at the front, and show the old hands what you can do'): [('mark',
                                                                                                                   'took '
                                                                                                                   'a '
                                                                                                                   'wild '
                                                                                                                   'risk')],
 ('the pager goes at two in the morning', 'run to wake the houses either side before the smoke reaches them'): [('door',
                                                                                                                 'helped '
                                                                                                                 'someone '
                                                                                                                 'in '
                                                                                                                 'need')],
 ('the pager goes at two in the morning', 'keep the radio log and the timings, and learn from every minute'): [('lesson',
                                                                                                                'every '
                                                                                                                'minute '
                                                                                                                'can '
                                                                                                                'teach '
                                                                                                                'something')],
 ('the pager goes at two in the morning', "knock on the neighbours' doors in turn, and count everyone out"): [('person',
                                                                                                               'neighbour')],
 ('the pager goes at two in the morning', 'check the gear and the air twice, as the drill says, before moving'): [('person',
                                                                                                                   'colleague')],
 ('called as a witness against someone you know', 'write down tonight what you saw, before anyone else can tell you'): [('lesson',
                                                                                                                         'write '
                                                                                                                         'it '
                                                                                                                         'while '
                                                                                                                         'it '
                                                                                                                         'is '
                                                                                                                         'fresh')],
 ('called as a witness against someone you know', 'ask the lawyer whether you can be let off, and keep your head down'): [('door',
                                                                                                                           'kept '
                                                                                                                           'it '
                                                                                                                           'hidden')],
 ('called as a witness against someone you know', "go to your colleague's family first, so they hear it from you"): [('lesson',
                                                                                                                      'hard '
                                                                                                                      'news '
                                                                                                                      'is '
                                                                                                                      'kinder '
                                                                                                                      'in '
                                                                                                                      'person')],
 ('called as a witness against someone you know', 'go with the family to urge your colleague to own up before the trial'): [('door',
                                                                                                                             'helped '
                                                                                                                             'someone '
                                                                                                                             'in '
                                                                                                                             'need')],
 ('called as a witness against someone you know', 'tell the defence lawyer, too, which parts you are sure of and which not'): [('mark',
                                                                                                                                'kept '
                                                                                                                                'your '
                                                                                                                                'word')],
 ('called as a witness against someone you know', "say in court what you saw, and that the yard's careless rules made it easy"): [('mark',
                                                                                                                                   'defied '
                                                                                                                                   'an '
                                                                                                                                   'authority')],
 ('called as a witness against someone you know', "ask the yard's manager to stand by you, so your job is safe after the trial"): [('person',
                                                                                                                                    'patron')],
 ('called as a witness against someone you know', 'give your evidence plainly, then call on the family the next day as before'): [('means',
                                                                                                                                   'ties+.03')],
 ('the clerk who wants something for the licence', 'tell the clerk you will wait your turn, and ask for a written date'): [('means',
                                                                                                                            'time-.06')],
 ('the clerk who wants something for the licence', "note the clerk's words and the time, and ask round who else was asked"): [('means',
                                                                                                                               'ties+.03')],
 ('the clerk who wants something for the licence', 'slip an envelope into the file, and ask when the licence will be ready'): [('door',
                                                                                                                                'hid '
                                                                                                                                'a '
                                                                                                                                'wrong')],
 ('the clerk who wants something for the licence', 'ask the clerk to say that again, loudly, so the whole queue can hear'): [('mark',
                                                                                                                              'defied '
                                                                                                                              'an '
                                                                                                                              'authority')],
 ('the clerk who wants something for the licence', 'ask the oldest shopkeeper on the street how it is done here'): [('person',
                                                                                                                     'elder')],
 ('the clerk who wants something for the licence', 'ask an old family friend on the council to have a quiet word with the clerk'): [('person',
                                                                                                                                     'go-between')],
 ('the clerk who wants something for the licence', 'record the clerk on the phone the next time, and let the clerk know it'): [('person',
                                                                                                                                'rival')],
 ('the clerk who wants something for the licence', "gather the other shopkeepers' stories, and take them to the local paper"): [('place',
                                                                                                                                 'rule.voice')],
 ('the clerk who wants something for the licence', "get the traders' association to complain together, so nobody stands alone"): [('place',
                                                                                                                                   'comm.shop')],
 ('the clerk who wants something for the licence', "write to the council's auditor with the dates, the words and the file number"): [('lesson',
                                                                                                                                      'dates '
                                                                                                                                      'and '
                                                                                                                                      'file '
                                                                                                                                      'numbers '
                                                                                                                                      'carry '
                                                                                                                                      'weight')],
 ('the trial of a friend', 'keep your seat in the gallery every day until the verdict, whatever it is'): [('means',
                                                                                                           'time-.06')],
 ('the trial of a friend', 'ask your friend for the whole truth, and decide after hearing it'): [('lesson',
                                                                                                  'hear the whole '
                                                                                                  'truth first')],
 ('the trial of a friend', 'tell your friend straight that you are angry, and that you are staying anyway'): [('mark',
                                                                                                               'kept '
                                                                                                               'your '
                                                                                                               'word')],
 ('the trial of a friend', 'visit your friend in the cells at lunch, and urge them to take the plea'): [('lesson',
                                                                                                         'hard '
                                                                                                         'advice is '
                                                                                                         'still '
                                                                                                         'advice')],
 ('the trial of a friend', 'find out who lost money, and what the family could pay back'): [('person', 'go-between')],
 ('the trial of a friend', 'write to the judge about who your friend was before, and what went wrong'): [('door',
                                                                                                          'helped '
                                                                                                          'someone '
                                                                                                          'in need')],
 ('the trial of a friend', 'find your friend a sharper lawyer through someone you know, and pay the first fee'): [('means',
                                                                                                                   'money-.06')],
 ('the trial of a friend', 'promise the mother you will visit, whatever the sentence'): [('door', 'kept your word')],
 ('the crowd at the town hall steps', 'link arms with the stewards, and hold the front still and quiet'): [('place',
                                                                                                            'rule.voice')],
 ('the crowd at the town hall steps', 'lead your friend down the side street before the square closes'): [('mark',
                                                                                                           'helped '
                                                                                                           'someone '
                                                                                                           'in '
                                                                                                           'need')],
 ('the crowd at the town hall steps', 'climb onto the fountain, and tell the crowd where to go next'): [('mark',
                                                                                                         'took a '
                                                                                                         'wild '
                                                                                                         'risk')],
 ('the crowd at the town hall steps', 'stay at the front, and chant until the doors open'): [('mark',
                                                                                              'defied an authority')],
 ('the crowd at the town hall steps', 'gather the families from your street, and see every one of them home'): [('means',
                                                                                                                 'ties+.06')],
 ('the crowd at the town hall steps', "find the councillor you know, and get the street's elders in by the side door"): [('person',
                                                                                                                          'elder')],
 ('the crowd at the town hall steps', "start the town's old song, loud, until the whole square is singing instead"): [('lesson',
                                                                                                                       'a '
                                                                                                                       'song '
                                                                                                                       'can '
                                                                                                                       'turn '
                                                                                                                       'a '
                                                                                                                       'crowd')],
 ('the crowd at the town hall steps', 'film the police line and the front calmly, so the truth of the night is kept'): [('lesson',
                                                                                                                         'a '
                                                                                                                         'calm '
                                                                                                                         'record '
                                                                                                                         'outlasts '
                                                                                                                         'the '
                                                                                                                         'night')],
 ('the crowd at the town hall steps', 'offer the officer in charge three speakers to go in and see the council tonight'): [('person',
                                                                                                                            'go-between')],
 ('the crowd at the town hall steps', 'tell the stewards who threw the bottle, and which way they went'): [('door',
                                                                                                            'made an '
                                                                                                            'enemy')],
 ('your partner falls seriously ill', 'accept the long road, and quietly set money aside for the hard years'): [('means',
                                                                                                                 'money+.06')],
 ('your partner falls seriously ill', 'find the best specialist in the country, and pull every string to get them seen'): [('means',
                                                                                                                            'ties-.05')],
 ('going into foster care', 'learn the house rules on the first night, and keep every one'): [('lesson',
                                                                                               'rules can keep you '
                                                                                               'safe')],
 ('going into foster care', 'ask the social worker exactly what happens next, and when you can go home'): [('person',
                                                                                                            'go-between')],
 ('going into foster care', 'keep a secret store of snacks under the bed, just in case'): [('door',
                                                                                            'kept it hidden')],
 ('going into foster care', 'explore the whole new house and garden, and make friends with the dog by teatime'): [('means',
                                                                                                                   'freedom+.03')],
 ('going into foster care', 'keep the thing from home with you every night, under the pillow'): [('means',
                                                                                                  'ties+.03')],
 ('going into foster care', 'make a card for your mum or dad every week, ready for the next visit'): [('door',
                                                                                                       'came home')],
 ('going into foster care', 'work out which grown-up really decides things, and ask them, not the others'): [('lesson',
                                                                                                              'ask '
                                                                                                              'the '
                                                                                                              'one '
                                                                                                              'who '
                                                                                                              'decides')],
 ('going into foster care', 'be so helpful around the house that the family will want to keep you'): [('door',
                                                                                                       'took them '
                                                                                                       'in')],
 ('going into foster care', 'keep a diary of everything that happens, to tell it right one day'): [('mark',
                                                                                                    'learned a '
                                                                                                    'skill')],
 ('the call to serve', 'apply for a deferment to finish your studies, with every paper in order'): [('place',
                                                                                                     'learn.higher')],
 ('the call to serve', 'claim the hardship exemption as the one who keeps the family going'): [('means', 'ties+.04')],
 ('the call to serve', 'object on conscience before the board, and serve in a care home instead'): [('place',
                                                                                                     'care.houses')],
 ('a landslide on election night', 'accept the result, whichever way you voted, and say so in public'): [('lesson',
                                                                                                          'a fair '
                                                                                                          'count '
                                                                                                          'deserves '
                                                                                                          'respect')],
 ('a landslide on election night', "go to the winning party's open meeting the next morning, for the doors it will open"): [('place',
                                                                                                                             'rule.voice')],
 ('a landslide on election night', 'skip the results, go out dancing, and hear who won in the morning'): [('lesson',
                                                                                                           'life '
                                                                                                           'goes on '
                                                                                                           'either '
                                                                                                           'way')],
 ('a landslide on election night', 'sit up with the family elders, who have seen governments come and go'): [('means',
                                                                                                              'ties+.03')],
 ('a landslide on election night', 'write to your new representative that night, setting out what the town needs'): [('place',
                                                                                                                      'rule.voice')],
 ('a landslide on election night', 'move your savings out of reach of the new taxes everyone expects'): [('means',
                                                                                                          'money+.03')],
 ('the old order falls', 'find out who will hold power by noon, and offer them your services'): [('person',
                                                                                                  'patron')],
 ('the old order falls', 'shutter the house, keep everyone in, and open the door to nobody'): [('means', 'ties-.06')],
 ('the old order falls', 'join the neighbours guarding the street, hunting guns and all, until order returns'): [('place',
                                                                                                                  'prot.watch')],
 ('the old order falls', 'slip across the border with one bag before the roads close'): [('mark', 'moved away')],
 ('the old order falls', 'take the family out to the relatives in the countryside until the city settles'): [('door',
                                                                                                              'left '
                                                                                                              'home')],
 ('the old order falls', 'buy the houses the fleeing officials sell off, for almost nothing'): [('means',
                                                                                                 'money+.06')],
 ('a revival fills the square', 'go to three meetings with a notebook, to understand what draws people in'): [('place',
                                                                                                               'faith.seeking')],
 ('a revival fills the square', 'get close to the preacher, and make yourself useful to the leaders'): [('person',
                                                                                                         'patron')],
 ('a revival fills the square', 'keep to the faith of your family, and let the wave roll past'): [('place',
                                                                                                   'faith.congregation')],
 ('a revival fills the square', 'buy the empty shops around the square while the crowds keep coming'): [('place',
                                                                                                         'comm.shop')],
 ('a cure is found at last', 'help the one who is ill through every form, and wait their turn'): [('mark',
                                                                                                   'helped someone '
                                                                                                   'in need')],
 ('a cure is found at last', 'pay a private clinic to get it to them first, whatever it costs'): [('means',
                                                                                                   'money-.10')],
 ('a cure is found at last', 'drop everything and drive through the night to be there for the first dose'): [('lesson',
                                                                                                              'be '
                                                                                                              'there '
                                                                                                              'when '
                                                                                                              'it '
                                                                                                              'counts')],
 ('a cure is found at last', 'trust the old care that has kept them going, until the new one proves itself'): [('door',
                                                                                                                'turned '
                                                                                                                'down '
                                                                                                                'a '
                                                                                                                'chance')],
 ('a cure is found at last', 'order it from abroad online, without a prescription, and get it to them now'): [('door',
                                                                                                               'broke '
                                                                                                               'the '
                                                                                                               'law')],
 ('a cure is found at last', 'take flowers to the grave of the one it came too late for'): [('lesson',
                                                                                             'some cures come too '
                                                                                             'late')],
 ('a cure is found at last', 'start a campaign to get the cure paid for, for everyone who needs it'): [('place',
                                                                                                        'rule.voice')],
 ('everyone is suddenly on the new medium', 'wait until there are proper rules for it, then join and use it with care'): [('lesson',
                                                                                                                           'be '
                                                                                                                           'careful '
                                                                                                                           'first '
                                                                                                                           'then '
                                                                                                                           'join')],
 ('everyone is suddenly on the new medium', 'post everything, day and night, for the thrill of being seen'): [('means',
                                                                                                               'time-.06')],
 ('everyone is suddenly on the new medium', 'stay off it, and keep talking to people face to face'): [('means',
                                                                                                       'time+.06')],
 ('everyone is suddenly on the new medium', 'help the oldest in the family onto it, so everyone can see each other'): [('means',
                                                                                                                        'ties+.06')],
 ('everyone is suddenly on the new medium', 'speak up at the school meeting for sensible rules on it for children'): [('place',
                                                                                                                       'rule.voice')],
 ('the machines come for the work', 'work out which parts of the job no machine can do, and claim them'): [('lesson',
                                                                                                            'find '
                                                                                                            'what '
                                                                                                            'only '
                                                                                                            'hands '
                                                                                                            'can '
                                                                                                            'do')],
 ('the machines come for the work', 'build a cheaper machine of your own, and sell it to the small firms'): [('place',
                                                                                                              'comm.market')],
 ('the machines come for the work', 'share your shifts with the older hands, so nobody has to go'): [('means',
                                                                                                      'money-.06')],
 ('the power and the networks go down', 'dig out the battery radio and piece together what is really going on'): [('lesson',
                                                                                                                   'facts '
                                                                                                                   'are '
                                                                                                                   'worth '
                                                                                                                   'digging '
                                                                                                                   'for')],
 ('the power and the networks go down', 'buy up fuel, water and batteries in the first hour, and sell the spare'): [('means',
                                                                                                                     'money+.06')],
 ('the power and the networks go down', 'make the larder last, a little each day, and wait calmly for the lights'): [('lesson',
                                                                                                                      'a '
                                                                                                                      'little '
                                                                                                                      'each '
                                                                                                                      'day '
                                                                                                                      'lasts')],
 ('the power and the networks go down', 'slip into the shut shop and take what the household needs'): [('door',
                                                                                                        'hid a '
                                                                                                        'wrong')],
 ('the power and the networks go down', 'pack the car and drive everyone out to family where the lights are on'): [('means',
                                                                                                                    'ties+.03')],
 ('a crash takes the savings', 'keep paying in every month as planned, and trust the long run'): [('means',
                                                                                                   'money-.03')],
 ('a crash takes the savings', 'stop opening the statements, and live on less until it passes'): [('means',
                                                                                                   'freedom-.06')],
 ('a crash takes the savings', 'buy cheap while everyone else is selling, and wait as long as it takes'): [('means',
                                                                                                            'money-.06')],
 ('a crash takes the savings', 'take what is left out of the bank in cash, and keep it at home'): [('lesson',
                                                                                                    'cash at hand '
                                                                                                    'feels safer')],
 ('a crash takes the savings', 'join the savers suing the bank for every last thing it owes'): [('place',
                                                                                                 'rule.voice')],
 ('a crash takes the savings', 'sit down with a free adviser and draw up a slow plan to rebuild'): [('person',
                                                                                                     'mentor')],
 ('new owners take over the firm', "stay on, learn the new owners' rules, and do the job as well as ever"): [('person',
                                                                                                              'boss')],
 ('new owners take over the firm', "read up on the new owners' past deals before deciding anything"): [('lesson',
                                                                                                        'know who '
                                                                                                        'you work '
                                                                                                        'for')],
 ('new owners take over the firm', 'get to the new managers first, and make yourself the one they rely on'): [('person',
                                                                                                               'patron')],
 ('new owners take over the firm', 'hand in your notice the week the new name goes up over the door'): [('means',
                                                                                                         'freedom+.06')],
 ('new owners take over the firm', 'keep doing your hours, and wait to see what the year brings'): [('lesson',
                                                                                                     'most storms '
                                                                                                     'blow over')],
 ('new owners take over the firm', 'ask the new owners in writing what happens to pay, pensions and jobs'): [('door',
                                                                                                              'defied '
                                                                                                              'an '
                                                                                                              'authority')],
 ('new owners take over the firm', "speak for the whole team at the new owners' first staff meeting"): [('person',
                                                                                                         'colleague')],
 ('new owners take over the firm', 'line up another post quietly, and stay until the new plan is clear'): [('door',
                                                                                                            'kept it '
                                                                                                            'hidden')],
 ('new owners take over the firm', 'ask for a rise as the price of staying, and mean it'): [('means', 'money+.06')],
 ('new owners take over the firm', 'take the payout offered to anyone who leaves, and put it by'): [('means',
                                                                                                     'money+.10')],
 ('folded into a bigger firm', 'apply for your post in the new structure, properly and on time'): [('person',
                                                                                                    'boss')],
 ('folded into a bigger firm', 'work out where your role stands on the new chart before anyone says'): [('lesson',
                                                                                                         'the chart '
                                                                                                         'tells its '
                                                                                                         'own '
                                                                                                         'story')],
 ('folded into a bigger firm', 'make sure whoever draws up the cuts knows your name and your numbers'): [('person',
                                                                                                          'patron')],
 ('folded into a bigger firm', 'leave before the choice is made over your head, and say why on the way out'): [('means',
                                                                                                                'money-.06')],
 ('folded into a bigger firm', 'stick with the old team, whatever the new chart says'): [('person', 'colleague')],
 ('folded into a bigger firm', 'throw a send-off for everyone from the old firm, the leavers first'): [('means',
                                                                                                        'ties+.06')],
 ('folded into a bigger firm', 'volunteer for the team that maps the old jobs onto the new ones'): [('means',
                                                                                                     'time-.06')],
 ('folded into a bigger firm', 'ask the union what the law owes the staff, and hold the firm to it'): [('door',
                                                                                                        'defied an '
                                                                                                        'authority')],
 ('the state takes over the failing firm', 'sign the new public contract and keep to its rules from the first day'): [('person',
                                                                                                                       'boss')],
 ('the state takes over the failing firm', 'put yourself forward for one of the posts the old managers left'): [('means',
                                                                                                                 'money+.06')],
 ('the state takes over the failing firm', 'leave for a private firm rather than work for the government'): [('person',
                                                                                                              'colleague '
                                                                                                              'lost')],
 ('the state takes over the failing firm', 'stay for the steady job and the pension, and be glad of them'): [('means',
                                                                                                              'money+.03')],
 ('the state takes over the failing firm', 'get the redundancy terms the old firm promised in writing, just in case'): [('lesson',
                                                                                                                         'get '
                                                                                                                         'promises '
                                                                                                                         'on '
                                                                                                                         'paper')],
 ('the state takes over the failing firm', 'find out which old contracts the new body will honour, and be the one who knows'): [('means',
                                                                                                                                 'ties+.03')],
 ('the state takes over the failing firm', 'speak up at the handover meeting for the service the town depends on'): [('place',
                                                                                                                      'rule.voice')],
 ('the state takes over the failing firm', "help write the new body's working rules so they are clear and fair"): [('place',
                                                                                                                    'rule.counsel')],
 ('the private files get out', "follow the bosses' script to the letter, and pass every complaint up the line"): [('door',
                                                                                                                   'gave '
                                                                                                                   'in '
                                                                                                                   'to '
                                                                                                                   'pressure')],
 ('the private files get out', 'trace how the records got out, and write it up for the bosses'): [('mark',
                                                                                                   'learned a '
                                                                                                   'skill')],
 ('the private files get out', 'keep your own part clean, and let the blame land where it falls'): [('lesson',
                                                                                                     'keep your own '
                                                                                                     'record clean')],
 ('the private files get out', 'change your own passwords and bank details tonight, before anything else'): [('means',
                                                                                                              'time-.03')],
 ('the private files get out', 'stay on the line with the frightened callers as long as they need'): [('mark',
                                                                                                       'helped '
                                                                                                       'someone in '
                                                                                                       'need')],
 ('the private files get out', 'press the bosses to tell every customer plainly what was lost'): [('door',
                                                                                                   'made an enemy')],
 ('the private files get out', 'draw up a plain guide for callers on what to do now, and share it round'): [('lesson',
                                                                                                             'plain '
                                                                                                             'words '
                                                                                                             'calm '
                                                                                                             'frightened '
                                                                                                             'people')],
 ('the thing the bosses are hiding', 'copy every document quietly and keep it safe before deciding anything'): [('door',
                                                                                                                 'kept '
                                                                                                                 'it '
                                                                                                                 'hidden')],
 ('the thing the bosses are hiding', 'hand in your notice, and find work you can do with a clear conscience'): [('means',
                                                                                                                 'money-.06')],
 ('the thing the bosses are hiding', 'send the papers to the inspectors without your name on them'): [('door',
                                                                                                       'defied an '
                                                                                                       'authority')],
 ('the thing the bosses are hiding', 'put things right in your own corner, quietly, and keep a note of everything'): [('lesson',
                                                                                                                       'small '
                                                                                                                       'quiet '
                                                                                                                       'fixes '
                                                                                                                       'still '
                                                                                                                       'count')],
 ('the thing the bosses are hiding', 'talk to the others who know, and go to the bosses together'): [('person',
                                                                                                      'colleague')],
 ('a new faith comes to town', "stand with your own faith's elders, and warn the neighbours off the new movement"): [('person',
                                                                                                                      'elder')],
 ('a new faith comes to town', 'rent the new movement a hall at a good price, and sell them the chairs'): [('means',
                                                                                                            'money+.06')],
 ('a new faith comes to town', 'go to one of their open nights, for the singing and the stir of it'): [('place',
                                                                                                        'faith.seeking')],
 ('a new faith comes to town', 'hold to the faith you were raised in, and say so when they come knocking'): [('lesson',
                                                                                                              'knowing '
                                                                                                              'where '
                                                                                                              'you '
                                                                                                              'stand')],
 ('a new faith comes to town', 'join the new movement for the friends and the standing, and rise fast in it'): [('place',
                                                                                                                 'faith.congregation'),
                                                                                                                ('person',
                                                                                                                 'friend')],
 ('a new faith comes to town', 'let the fuss pass, and spend your weekends as you always have'): [('door',
                                                                                                   'stayed home')],
 ('a new faith comes to town', 'ask the friend who joined how it has changed their life, and really listen'): [('means',
                                                                                                                'ties+.03')],
 ('a new faith comes to town', "ask the council to check the new movement's permits and its money"): [('person',
                                                                                                       'rival')],
 ('a new faith comes to town', "read the new movement's teachings side by side with those of your own faith"): [('lesson',
                                                                                                                 'both '
                                                                                                                 'teachings '
                                                                                                                 'share '
                                                                                                                 'old '
                                                                                                                 'roots')],
 ('the hall on the corner is shut', 'keep the family table open to all, with one rule: no arguing at meals'): [('means',
                                                                                                                'ties+.06')],
 ('the hall on the corner is shut', 'keep out of it, and wait for the town to calm down'): [('lesson',
                                                                                             'trouble passes if left '
                                                                                             'alone')],
 ('the hall on the corner is shut', 'move the family across town, away from the trouble'): [('mark', 'moved away')],
 ('the hall on the corner is shut', 'help the elders of both halls find a quiet room to talk in'): [('person',
                                                                                                     'elder')],
 ('the hall on the corner is shut', 'write an open letter to the town, asking both sides to stop'): [('place',
                                                                                                      'rule.voice')],
 ('the hall on the corner is shut', 'ask the council for firm rules on protests near any hall'): [('place',
                                                                                                   'rule.counsel')],
 ('a season of bad air', "keep the household to the council's advice, windows shut and outings short"): [('means',
                                                                                                          'freedom-.03')],
 ('a season of bad air', 'check the readings each morning and plan every outing around the cleanest hours'): [('lesson',
                                                                                                               'plan '
                                                                                                               'around '
                                                                                                               'the '
                                                                                                               'clean '
                                                                                                               'hours')],
 ('a season of bad air', 'buy a good air filter early, before the price climbs, and sell on the spare'): [('means',
                                                                                                           'money+.03')],
 ('a season of bad air', 'go out anyway and run your usual route, haze or no haze'): [('means', 'health-.06')],
 ('a season of bad air', "gather the street's readings and take them to the council meeting"): [('place',
                                                                                                 'rule.voice')],
 ('a season of bad air', 'plant a thick hedge by the road and fill the house with air-cleaning plants'): [('means',
                                                                                                           'health+.03')],
 ('a season of bad air', 'take the cleaning-crew work nobody else wants this summer, at triple pay'): [('means',
                                                                                                        'money+.06')],
 ('a season of bad air', 'wait it out indoors and use the weeks to put your own affairs in order'): [('lesson',
                                                                                                      'quiet weeks '
                                                                                                      'set things '
                                                                                                      'straight')],
 ('the river runs foul', "file a formal complaint and ask the council to enforce the works' permit"): [('place',
                                                                                                        'rule.voice')],
 ('the river runs foul', 'buy water in bottles, keep everyone away from the river, and wait for it to clear'): [('means',
                                                                                                                 'money-.03')],
 ('the river runs foul', "help draft the council's report on what went wrong and who must pay"): [('place',
                                                                                                   'rule.counsel')],
 ('the river runs foul', "post the test results online, with the firm's name, before anyone can bury them"): [('door',
                                                                                                               'made '
                                                                                                               'an '
                                                                                                               'enemy')],
 ('the river runs foul', 'sign up to the group claim against the firm and push hard for a payout'): [('means',
                                                                                                      'money+.06')],
 ('the river runs foul', 'sell your plot by the river quietly, before the prices fall'): [('door', 'kept it hidden')],
 ('a dry year on the land', 'pack a bag and go to the city for work until the rain comes back'): [('means',
                                                                                                   'money+.06')],
 ('a dry year on the land', 'help the council share out the reservoir fairly between farms and homes'): [('place',
                                                                                                          'rule.counsel')],
 ('a dry year on the land', 'take a night shift on the fire watch in the dry hills'): [('place', 'prot.rescue')],
 ('a dry year on the land', 'work out which crops will still pay, and plant them before anyone else does'): [('means',
                                                                                                              'money+.06')],
 ('a dry year on the land', 'haul water up to the farm by hand every morning to keep the animals alive'): [('means',
                                                                                                            'time-.06')],
 ('a dry year on the land', 'tighten the household belt, spend nothing, and sit the year out'): [('means',
                                                                                                  'money+.03')],
 ('a glorious spring', 'start a notebook of what flowers when, on long walks before work'): [('place', 'prod.wild')],
 ('a glorious spring', 'set up a stall at the weekend market while people are in the mood to spend'): [('place',
                                                                                                        'comm.market')],
 ('a glorious spring', 'skip work on the first warm day and take everyone to the lake'): [('lesson',
                                                                                           'a day off pays back')],
 ('a glorious spring', 'dig and plant the garden, and spend the long evenings sitting in it'): [('means',
                                                                                                 'health+.03')],
 ('a glorious spring', 'use the light evenings to finish the course you put off all winter'): [('place',
                                                                                                'learn.higher')],
 ('a glorious spring', 'take the bike out alone and ride somewhere you have never been'): [('means', 'freedom+.03')],
 ('a glorious spring', 'get the street to back a community garden, and offer to run it'): [('place', 'prod.land')],
 ('a glorious spring', 'plant trees along the school road with the children and the old folk of the street'): [('means',
                                                                                                                'ties+.06')],
 ('the town builds itself back', "sit on the residents' committee that checks the rebuilding against the plan"): [('place',
                                                                                                                   'rule.counsel')],
 ('the town builds itself back', 'bid for a small rebuilding contract while the money is flowing'): [('means',
                                                                                                      'money+.06')],
 ('the town builds itself back', 'keep to your old shops and your old bench, so the town has its life back'): [('means',
                                                                                                                'ties+.03')],
 ('the town builds itself back', 'find the gaps in the rebuilding grants and get your own repairs paid first'): [('means',
                                                                                                                  'money+.03')],
 ('the town builds itself back', 'help plant the banks and hillsides so the land holds better next time'): [('place',
                                                                                                             'prod.wild')],
 ('the town builds itself back', 'press the council at every meeting until the clinic has its own building again'): [('place',
                                                                                                                      'rule.voice')],
 ('a boom year', 'stay with your employer and take the raise offered for staying'): [('means', 'money+.03')],
 ('a boom year', 'play two offers against each other until one pays far more'): [('means', 'money+.06')],
 ('a boom year', 'put the extra pay aside for the lean years that always follow'): [('means', 'money+.06')],
 ('a boom year', 'spend the extra on the long trip you always put off'): [('means', 'money-.10')],
 ('a boom year', 'push for promotion now, while the firm needs every good person'): [('lesson',
                                                                                      'ask while they need you')],
 ('the jobs come back to town', 'sign on at the reopened works and be there on time every shift'): [('place',
                                                                                                     'prod.craft')],
 ('the jobs come back to town', 'open a pop-up bar in the old station and see if it takes off'): [('door',
                                                                                                   'took a wild '
                                                                                                   'risk')],
 ('the jobs come back to town', 'put in a word for your cousins, so the family gets the good shifts'): [('person',
                                                                                                         'colleague')],
 ('the jobs come back to town', 'call the ones who left and tell them to come home, there is work again'): [('means',
                                                                                                             'ties+.06')],
 ('the jobs come back to town', 'pitch a new idea to the owners at their open day'): [('person', 'patron')],
 ('the jobs come back to town', "get a seat on the works' liaison board as the town's voice"): [('place',
                                                                                                 'rule.counsel')],
 ('the jobs come back to town', 'help the council set up a jobs board so everyone hears of the openings'): [('door',
                                                                                                             'helped '
                                                                                                             'someone '
                                                                                                             'in '
                                                                                                             'need')],
 ('a bumper harvest', 'help run the harvest supper and see that every household gets a share'): [('place',
                                                                                                  'gather.hall')],
 ('a bumper harvest', "work out what a glut does to prices and plan next year's planting around it"): [('lesson',
                                                                                                        'a glut '
                                                                                                        'lowers '
                                                                                                        'every '
                                                                                                        'price')],
 ('a bumper harvest', 'buy grain cheap now and store it to sell in the spring'): [('door', 'took a wild risk')],
 ('a bumper harvest', 'dance at the harvest fair until the band packs up'): [('person', 'friend')],
 ('a bumper harvest', 'spend the week bottling, drying and putting by for the winter'): [('means', 'money+.03')],
 ('a bumper harvest', 'drive a van of cheap produce to the city market and sell it fast'): [('means', 'money+.06')],
 ('a bumper harvest', "sign a contract now that fixes next year's price in your favour"): [('door',
                                                                                            'kept your word')],
 ('a bumper harvest', 'save seed from the best plants, with notes on which did well'): [('mark', 'learned a skill')],
 ('a bumper harvest', 'lead the harvest parade through the town, banners and all'): [('place', 'gather.great')],
 ('a new law opens a door', 'accept the new law, though you argued against it, and say so plainly'): [('lesson',
                                                                                                       'a fair loss '
                                                                                                       'still '
                                                                                                       'counts')],
 ('a new law opens a door', 'read the new law in full and explain it to friends who are confused'): [('means',
                                                                                                      'ties+.03')],
 ('a new law opens a door', 'take the new freedom in the very first week, whatever anyone says'): [('means',
                                                                                                    'freedom+.06')],
 ('a new law opens a door', 'keep to the old ways in your own house, and leave others to theirs'): [('door',
                                                                                                     'stayed home')],
 ('a new law opens a door', 'wait to see who gains from it before taking any side'): [('door',
                                                                                       'turned down a chance')],
 ('a new law opens a door', 'hear out the elders and the young on it before making up your mind'): [('person',
                                                                                                     'elder')],
 ('a new law opens a door', 'write openly online about what the change means for people like yourself'): [('place',
                                                                                                           'arts.page')],
 ('a new law opens a door', 'join the campaign to hedge the new law about with rules and licences'): [('place',
                                                                                                       'rule.voice')],
 ('a new law opens a door', 'march in the celebration that weekend with everyone it frees'): [('place',
                                                                                               'gather.great')],
 ('a feast in a year of trust', 'keep the whole fast and every rite before the feast, as the faith teaches'): [('place',
                                                                                                                'faith.congregation')],
 ('a feast in a year of trust', 'find out what each custom of the feast means, and tell the young ones'): [('means',
                                                                                                            'ties+.03')],
 ('a feast in a year of trust', 'dance in the street until dawn with everyone else'): [('person', 'friend')],
 ('a feast in a year of trust', 'play host to the biggest table in the street, and enjoy every bit of the attention'): [('means',
                                                                                                                         'money-.06')],
 ('a feast in a year of trust', "help keep the feast's accounts, and earn a say in how the money is spent"): [('place',
                                                                                                               'rule.counsel')],
 ('a feast in a year of trust', "help the elders write down the feast's old customs before they are forgotten"): [('place',
                                                                                                                   'learn.keeping')],
 ('the congregation splits in two', 'stay in the old building with the elders, and keep the old order'): [('place',
                                                                                                           'faith.congregation')],
 ('the congregation splits in two', 'go to both for a month, and see which keeps faith with its own teaching'): [('lesson',
                                                                                                                  'watch '
                                                                                                                  'what '
                                                                                                                  'each '
                                                                                                                  'side '
                                                                                                                  'does')],
 ('the congregation splits in two', 'side with whichever half keeps the building, the funds and the board'): [('place',
                                                                                                               'faith.congregation')],
 ('the congregation splits in two', 'stay with the families you grew up beside, wherever they go'): [('means',
                                                                                                      'ties+.04')],
 ('the congregation splits in two', 'call a meeting of both halves, and ask for a fair vote on the building'): [('place',
                                                                                                                 'rule.counsel')],
 ('the congregation splits in two', 'stop going to either, and keep your faith at home for now'): [('means',
                                                                                                    'ties-.04')],
 ('the congregation splits in two', "take charge of the new hall's money and rota before anyone else does"): [('person',
                                                                                                               'rival')],
 ('the congregation splits in two', 'broker a quiet deal to share the old building on alternate weeks'): [('door',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ("the gang's test of loyalty", 'keep the bag and your silence for the week, exactly as told'): [('door',
                                                                                                  'kept it hidden')],
 ("the gang's test of loyalty", 'open the bag in secret first, to know exactly what you are risking'): [('lesson',
                                                                                                         'know what '
                                                                                                         'you '
                                                                                                         'carry')],
 ("the gang's test of loyalty", 'keep the bag, and ask for a cut of whatever it is worth'): [('means', 'money+.06')],
 ("the gang's test of loyalty", 'tell your family everything, and let them help you get out'): [('door', 'owned up')],
 ("the gang's test of loyalty", 'hand the bag back with a joke, and keep the friends but not the gang'): [('means',
                                                                                                           'freedom+.04')],
 ("the gang's test of loyalty", 'keep the bag, and ask in return for a real place in the gang'): [('person',
                                                                                                   'mentor')],
 ("the gang's test of loyalty", "keep the bag this once for your friend's sake, and never again"): [('door',
                                                                                                     'gave in to '
                                                                                                     'pressure')],
 ('the club reaches the final', 'turn up early, kit ready, and do exactly the job you are given'): [('lesson',
                                                                                                     'small jobs win '
                                                                                                     'big days')],
 ('the club reaches the final', "study the other side's last five games, and share what you find with the coach"): [('person',
                                                                                                                     'mentor')],
 ('the club reaches the final', 'make sure you are next to the chairman in the photograph with the cup'): [('person',
                                                                                                            'patron')],
 ('the club reaches the final', 'lead the singing from the first whistle to the last, louder than anyone'): [('place',
                                                                                                              'gather.great')],
 ('the club reaches the final', 'help run the day: tickets, the minibus, the kit and the list of who is where'): [('means',
                                                                                                                   'time-.04')],
 ('the club reaches the final', 'bake for the clubhouse tea after the match, win or lose'): [('means', 'ties+.03')],
 ('the club reaches the final', 'find a sponsor for the new kit while the crowd is in a good mood'): [('person',
                                                                                                       'patron')],
 ('moving in with a partner', 'sit down together and agree house rules, chores and money, in writing'): [('door',
                                                                                                          'kept your '
                                                                                                          'word')],
 ('moving in with a partner', 'plan the move like a project: lists, budgets and a timetable'): [('means',
                                                                                                 'money+.03')],
 ('moving in with a partner', 'keep a separate bank account of your own, just in case'): [('means', 'freedom+.04')],
 ('moving in with a partner', 'throw a housewarming party on the first night, among the boxes'): [('person',
                                                                                                   'neighbour')],
 ('moving in with a partner', 'fill the place with plants and family things until it feels like home'): [('lesson',
                                                                                                          'a home is '
                                                                                                          'made '
                                                                                                          'slowly')],
 ('moving in with a partner', 'take a cheap place round the corner from your family, with them on hand'): [('door',
                                                                                                            'stayed '
                                                                                                            'home')],
 ('moving in with a partner', 'split the rent by income and keep a fair shared ledger'): [('lesson',
                                                                                           'fair shares keep the '
                                                                                           'peace')],
 ('a breakup', 'write it all out until you understand what went wrong'): [('lesson', 'knowing why helps it heal')],
 ('a breakup', 'make sure you keep the friends and everything worth having, and let them start again'): [('means',
                                                                                                          'ties+.05')],
 ('a breakup', 'go dancing with your friends that night, and cry on their shoulders after'): [('person', 'friend')],
 ('a breakup', 'stay close to your family for a while, and let it heal'): [('means', 'health+.03')],
 ('a breakup', 'take long walks and slowly work out what you need next time'): [('lesson',
                                                                                 'know what you need next')],
 ('a breakup', 'pour it all into a song or a story that is brutally honest'): [('place', 'arts.song')],
 ('a breakup', 'insist on getting back everything you lent and every penny you are owed'): [('means', 'money+.04')],
 ('losing your job', 'sign on for benefits straight away and apply for jobs every single day'): [('means',
                                                                                                  'money+.03')],
 ('losing your job', 'move in with family, and work cash in hand for people you know'): [('mark', 'came home')],
 ('losing your job', 'take the time to work out, calmly, what work you were really meant for'): [('means',
                                                                                                  'money-.05')],
 ('losing your job', 'take the first decent offer within a week and get moving'): [('person', 'boss')],
 ('losing your job', 'live on next to nothing, sell what you can, and wait for the right opening'): [('means',
                                                                                                      'money-.08')],
 ('a baby on the way, planned or not', 'tell only your closest family, and end the pregnancy quietly'): [('door',
                                                                                                          'kept it '
                                                                                                          'hidden')],
 ('a baby on the way, planned or not', 'count what a child would cost right now, and end the pregnancy early'): [('means',
                                                                                                                  'freedom+.05')],
 ('a baby on the way, planned or not', 'get the facts from a doctor, then follow your heart and end the pregnancy'): [('lesson',
                                                                                                                       'trust '
                                                                                                                       'your '
                                                                                                                       'own '
                                                                                                                       'judgement')],
 ('a baby on the way, planned or not', 'see the pregnancy through, and choose a loving family to adopt the baby'): [('door',
                                                                                                                     'took '
                                                                                                                     'them '
                                                                                                                     'in')],
 ('a baby on the way, planned or not', 'end the pregnancy, and say so openly to anyone who asks'): [('lesson',
                                                                                                     'no need to '
                                                                                                     'hide it')],
 ('an unexpected chance: a grant, a role, a stage', 'accept, and work every day to deserve the honour'): [('person',
                                                                                                           'mentor')],
 ('an unexpected chance: a grant, a role, a stage', 'accept, and spend the first month studying everything the role demands'): [('mark',
                                                                                                                                 'learned '
                                                                                                                                 'a '
                                                                                                                                 'skill')],
 ('an unexpected chance: a grant, a role, a stage', 'use the offer to bargain for something better elsewhere'): [('means',
                                                                                                                  'money+.06')],
 ('an unexpected chance: a grant, a role, a stage', 'turn it down; the timing is wrong, and the family needs a hand at home'): [('door',
                                                                                                                                 'stayed '
                                                                                                                                 'home')]}
