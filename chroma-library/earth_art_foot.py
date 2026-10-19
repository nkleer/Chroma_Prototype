# Footprints (plan.md workstream 3; Engine 10-19): what each option visibly leaves, compiled by build.py from the
# foot: fields of the .lib parts. FOOT[(moment, option label)] = [(kind, value), ...]; kinds person, place, means,
# mark, door, lesson. Read only with the engine's foot_on switch; earth.py carries none of it.
FOOT = {("a dealer asks for a painting in a dead master's hand", 'paint it as an honest copy, marked as one on the back and the bill'): [('means',
                                                                                                                                   'money+.03')],
 ("a dealer asks for a painting in a dead master's hand", 'say no, but keep a written note of the offer to hold over the dealer'): [('door',
                                                                                                                                     'kept '
                                                                                                                                     'it '
                                                                                                                                     'hidden')],
 ("a dealer asks for a painting in a dead master's hand", 'tell the dealer what the offer is worth, loudly, in front of the customers'): [('person',
                                                                                                                                           'rival')],
 ("a dealer asks for a painting in a dead master's hand", "tell the dead painter's family what the dealer is planning"): [('person',
                                                                                                                           'friend')],
 ("a dealer asks for a painting in a dead master's hand", 'laugh it off, and paint the dead master a tribute under your own name'): [('lesson',
                                                                                                                                      'the '
                                                                                                                                      'old '
                                                                                                                                      'master '
                                                                                                                                      'still '
                                                                                                                                      'teaches')],
 ("a friend's secret would make the book", 'change it beyond knowing: another town, another age, another life'): [('mark',
                                                                                                                   'learned '
                                                                                                                   'a '
                                                                                                                   'skill')],
 ("a friend's secret would make the book", "offer the friend a share of the book's money for the right to use it"): [('means',
                                                                                                                      'money-.03')],
 ("a friend's secret would make the book", 'write it as one poem for the friend alone, and keep it out of the book'): [('lesson',
                                                                                                                        'some '
                                                                                                                        'things '
                                                                                                                        'are '
                                                                                                                        'written '
                                                                                                                        'for '
                                                                                                                        'one')],
 ("a friend's secret would make the book", 'ask the friend first, and cut whatever they ask to be cut'): [('mark',
                                                                                                           'kept '
                                                                                                           'your '
                                                                                                           'word')],
 ("a friend's secret would make the book", 'agree in writing with the friend what may go in, and keep to it'): [('door',
                                                                                                                 'kept '
                                                                                                                 'your '
                                                                                                                 'word')],
 ("a friend's secret would make the book", 'keep the pages in a drawer, for a book written years from now'): [('door',
                                                                                                               'kept '
                                                                                                               'it '
                                                                                                               'hidden')],
 ("a friend's secret would make the book", 'ask the friend to write that chapter in their own words, under their own name'): [('lesson',
                                                                                                                               'the '
                                                                                                                               'story '
                                                                                                                               'is '
                                                                                                                               'theirs '
                                                                                                                               'to '
                                                                                                                               'tell')],
 ("the idea in someone else's sketchbook", 'tell the friend the idea could sell, and offer to find the buyer'): [('person',
                                                                                                                  'patron')],
 ("the idea in someone else's sketchbook", 'close the sketchbook, and make something wholly your own that night'): [('door',
                                                                                                                     'kept '
                                                                                                                     'it '
                                                                                                                     'hidden')],
 ("the idea in someone else's sketchbook", "make the piece, with the friend's name beside your own on the label"): [('door',
                                                                                                                     'owned '
                                                                                                                     'up')],
 ("the idea in someone else's sketchbook", 'leave a note in the sketchbook: this one is good, make it'): [('lesson',
                                                                                                           'a little '
                                                                                                           'praise '
                                                                                                           'goes '
                                                                                                           'far')],
 ("the idea in someone else's sketchbook", 'make an answer to it, and hang both side by side at the show'): [('person',
                                                                                                              'rival')],
 ('an advert wants your style', 'turn it down, and paint the offer letter into the next wall as a joke'): [('lesson',
                                                                                                            'laughing '
                                                                                                            'back is '
                                                                                                            'an '
                                                                                                            'answer')],
 ('an advert wants your style', 'say no, and write an open letter about who owns a style'): [('place',
                                                                                              'gather.talk')],
 ('an advert wants your style', 'ask the neighbours who helped paint the walls, and do what they decide'): [('person',
                                                                                                             'neighbour')],
 ('an advert wants your style', 'take the money, and buy a year to paint nothing but your own work'): [('means',
                                                                                                        'time+.10')],
 ('hands that will not hold the brush', 'see the specialist, and follow the treatment to the letter'): [('place',
                                                                                                         'care.houses')],
 ('hands that will not hold the brush', 'learn to draw with the other hand, slowly, like a child again'): [('mark',
                                                                                                            'learned '
                                                                                                            'a '
                                                                                                            'skill')],
 ('the sketch that went round the world', "ask the class's old tutor to go through everything, and study for a year first"): [('person',
                                                                                                                               'mentor')],
 ('the sketch that went round the world', 'turn the offers down, and give the original to the woman with the umbrella'): [('person',
                                                                                                                           'friend')],
 ('the open submission to the great summer show', 'take a stall at the summer art fair in the park instead, and sell what sells'): [('place',
                                                                                                                                     'comm.market')],
 ('the open submission to the great summer show', 'enter every smaller open show in the region this year, and note what each one hangs'): [('place',
                                                                                                                                            'arts.craft')],
 ('the manuscript in the pile on the floor', "join a writers' group at the library, and swap chapters every fortnight for a year"): [('place',
                                                                                                                                      'gather.circle')],
 ('the manuscript in the pile on the floor', 'read the best chapter aloud at the poetry night, and see if the room goes quiet'): [('place',
                                                                                                                                   'arts.tale')],
 ('the late starter at the easel', "join the college's sculpture course, the oldest in the room by forty years"): [('place',
                                                                                                                    'learn.higher')],
 ('the late starter at the easel', 'enter the open show for over-sixties, and go to the opening in a good coat'): [('place',
                                                                                                                    'arts.craft')],
 ('the late starter at the easel', 'sell a few small pictures at the winter fair, and watch what people pick up'): [('place',
                                                                                                                     'comm.market')],
 ('the late starter at the easel', 'keep the best twenty canvases, give the rest to the family, and paint on'): [('means',
                                                                                                                  'ties+.03')],
 ('the other side of the easel', 'write the school a fairer way to judge a folder, and offer it for next year'): [('place',
                                                                                                                   'learn.higher')],
 ('the other side of the easel', 'take the boldest hopeful on as a summer assistant, before the dealer does'): [('person',
                                                                                                                 'colleague')],
 ('the judge stops at your table at the craft fair', 'take a young maker from the town as an apprentice for a year'): [('person',
                                                                                                                        'colleague')],
 ('the judge stops at your table at the craft fair', 'book a bigger stall for next year, in the front row by the gate'): [('place',
                                                                                                                           'comm.market')],
 ('the judge stops at your table at the craft fair', "chalk the judge's words on the stall's board, and raise the prices by Sunday"): [('means',
                                                                                                                                        'money+.03')],
 ('art school applications', 'send the portfolio exactly as the guidance asks, every piece mounted and labelled'): [('place',
                                                                                                                     'learn.higher')],
 ('art school applications', 'take a paid portfolio course on Saturdays, and apply with what it teaches'): [('person',
                                                                                                             'teacher')],
 ('art school applications', 'apply only to the school whose graduates end up in the big galleries'): [('place',
                                                                                                        'learn.higher')],
 ('art school applications', 'apply to the art school in your own town, with home in every drawing'): [('place',
                                                                                                        'learn.higher')],
 ('art school applications', 'skip art school, and sell prints at the weekend market instead'): [('place',
                                                                                                  'comm.market')],
 ('art school applications', 'take the free foundation year at the local college before choosing'): [('place',
                                                                                                      'learn.higher')],
 ('art school applications', 'tell your parents straight that this is the life you want, and ask their blessing'): [('means',
                                                                                                                     'freedom+.03')],
 ('the degree show', "price every piece sensibly, and sell what sells to the show's visitors"): [('means',
                                                                                                  'money+.06')],
 ('the degree show', 'go and assist a working sculptor in the next city, mixing plaster and learning'): [('person',
                                                                                                          'mentor')],
 ('a wall that needs a mural', 'offer to restore the faded old mural on the library wall instead'): [('place',
                                                                                                      'learn.keeping')],
 ('the first commission', 'ask for a single drawing first, to learn how a brief is done'): [('person', 'boss')],
 ('the first commission', 'have the contract read line by line before signing anything'): [('lesson',
                                                                                            'know the bargain before '
                                                                                            'agreeing')],
 ('the first show', 'ask the gallery for the sales of every first show it has hung, before signing'): [('place',
                                                                                                        'arts.craft')],
 ('the first show', 'turn the show down until the work is ready, and say so plainly'): [('lesson',
                                                                                         'the work sets its own '
                                                                                         'pace')],
 ('the first show', 'give a talk on the work in the gallery on the second Saturday'): [('means', 'ties+.03')],
 ('the school needs an art teacher', 'turn it down, and run paid weekend classes from the studio instead'): [('means',
                                                                                                              'money+.03')],
 ('the school needs an art teacher', 'help in the art room one morning a week for a term, the checks done first'): [('person',
                                                                                                                     'colleague')],
 ('the school needs an art teacher', 'start a lunchtime comic club at the school, with a teacher in the room'): [('place',
                                                                                                                  'arts.page')],
 ('the school needs an art teacher', 'ask the head for the pay, the hours and the budget in writing first'): [('lesson',
                                                                                                               'ask '
                                                                                                               'the '
                                                                                                               'terms '
                                                                                                               'before '
                                                                                                               'saying '
                                                                                                               'yes')],
 ('an empty shop on the corner', "rent only the window, and sell the town's painters on commission"): [('place',
                                                                                                        'arts.craft')],
 ('an empty shop on the corner', 'write a business plan, and take it to the bank before signing anything'): [('lesson',
                                                                                                              'the '
                                                                                                              'sums '
                                                                                                              'come '
                                                                                                              'first')],
 ('a publisher reads the manuscript', 'trade a read of the manuscript for editing work with a friend in publishing'): [('person',
                                                                                                                        'go-between')],
 ('a publisher reads the manuscript', 'send it out, and promise yourself to write every morning whatever comes back'): [('door',
                                                                                                                         'kept '
                                                                                                                         'your '
                                                                                                                         'word')],
 ('a work in the national collection', 'lend the piece for a year, so the curators can live with it before deciding'): [('person',
                                                                                                                         'keeper')],
 ('a national prize for writing', 'sign the next two books with the old publisher, at a better advance'): [('means',
                                                                                                            'money+.06')],
 ('a national prize for writing', 'turn the tour down, and go back to the desk for the next book'): [('means',
                                                                                                      'time+.06')],
 ('the painted cave at the winter camp', 'paint the chief at the head of the hunt, larger than life, as the chief wants'): [('person',
                                                                                                                             'patron')],
 ("the carver's mask for the dead", "carve a second mask for the band to keep, so the chief's face is not lost"): [('lesson',
                                                                                                                    'a '
                                                                                                                    'face '
                                                                                                                    'can '
                                                                                                                    'outlast '
                                                                                                                    'a '
                                                                                                                    'life')],
 ("the carver's mask for the dead", 'carve it fierce in a single night, from the skull of the bear the chief killed'): [('mark',
                                                                                                                         'took '
                                                                                                                         'a '
                                                                                                                         'wild '
                                                                                                                         'risk')],
 ("the queen's portrait sitting", 'ask to paint her at ease in her garden, over many quiet sittings'): [('person',
                                                                                                         'patron')],
 ("the queen's portrait sitting", "ask the last court painter's widow for his notes on painting the queen"): [('mark',
                                                                                                               'learned '
                                                                                                               'a '
                                                                                                               'skill')],
 ('the illuminated book for the cathedral', 'agree a fee for every page with the chapter, and hire two helpers'): [('person',
                                                                                                                    'colleague')]}
