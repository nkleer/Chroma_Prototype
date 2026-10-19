"""Chroma library callings: compiled by build.py from callings.lib (edit the .lib, not this file).

Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is
(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine
ignores until it has fields for them. See library-spec.md.
"""

SITUATIONS = [
{'name': 'a rival opens across the street',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.1 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'rival, friend, colleague',
 'requires': 'shop owner | founder of a firm | café or bar owner | shift manager',
 'worlds': {'earth': 'a new place opens across the street, doing the same trade for a third less',
            'tribal': "a far band's trader lays out the same goods across the path at the gathering, for less",
            'magic': 'a new shop opens across the lane, with a painted sign and prices a third lower'},
 'timing': {'times': 'per shop owner, founder, café or bar owner or shift manager a year: about 1 in 6 see a rival '
                     'open close enough to take their custom (estimate); small shops, cafés and firms open and close '
                     'by the thousand every year, and about 2 lives in 10 own, found or manage a business at some '
                     'time (catalogue shares: shop owner .04, founder of a firm .03, café or bar owner .004, shift '
                     'manager .15)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'On Monday the paper comes off the windows across the street: a new place, bright and cheap, '
                       'doing what {Ns} place does at two-thirds of the price, with a queue round the corner on the '
                       'first morning. {rival}, who runs it, waves over the road.'),
                      ('W',
                       'Years on this street have taught {N} that customers remember who was fair to them. Prices '
                       "like the newcomer's cannot last, and {N} means to still be here when they stop."),
                      ('U',
                       '{N} counts the queue across the road from behind the counter: how many, how long they wait, '
                       'what they carry out. The prices do not add up, and {N} wants to know why.'),
                      ('B',
                       'Somebody is going to own this street. {N} would rather it was not the newcomer, and starts '
                       'working out who could be brought in to make sure of it.'),
                      ('R',
                       '{N} watches the queue over the road and feels the blood rise. If it is a fight the newcomer '
                       'wants, it is a fight the newcomer will get.'),
                      ('G',
                       'The regulars have come for years: the man with the old dog, the two nurses after the night '
                       'shift. {N} wonders whether the street has room for two, and what it would lose if it had '
                       'not.')],
            'tribal': [('',
                        'At the summer gathering a trader from a far band lays out goods across the path from {Ns} '
                        'place: the same flint, the same hides and dried fish, for less. The young ones are already '
                        'crowding round.')],
            'magic': [('',
                       'A new shop opens across the lane with a painted sign, a bell over the door and prices a '
                       'third below {Ns}. By noon there is a crowd at its counter, and {rival}, behind it, raises a '
                       'hand across the cobbles.')]},
 'outcomes': (['After a month the crowd across the way thins, and {Ns} trade picks up again.',
               'By the end of the season there is room for both, and the regulars still come.'],
              ["The newcomer's low prices run for months, and {Ns} trade falls by a third.",
               'Nothing {N} tries seems to work, and the winter goes by watching the queue across the way.']),
 'options': [
    ('keep the prices, the hours and the promises to the regulars exactly as they were', 'W1', None, 0.45, '', {'habit': True, 'v': 'tradition, conformity', 'world': {'tribal': 'keep the same fair trades and the same place at the gathering, as you always have'}, 'chance': 0.85}),
    ("go through the rival's prices line by line, and bargain again with every supplier", 'U1', None, 0.45, '', {'grants': 'striking a deal', 'v': 'achievement, security', 'world': {'tribal': 'weigh every trade the newcomer makes, and go back to the flint-knappers for better terms', 'magic': "go through the newcomer's prices line by line, and haggle anew with every supplier"}, 'chance': 0.75}),
    ('find a backer, and open a second place across town before the rival can', 'B1', None, 0.45, '', {'grants': 'investors who back you', 'aims': 'chief executive', 'v': 'power, achievement', 'world': {'tribal': 'find a trader with goods to share, and set out a second place at the next gathering first', 'magic': 'find a backer among the merchant houses, and open a second shop across the city first'}, 'chance': 0.55}),
    ('cut prices to the bone tomorrow, and fight them for every customer', 'R1', None, 0.45, '', {'self_control': '-', 'v': 'stimulation, power', 'world': {'tribal': 'give twice the goods for the same trade tomorrow, and fight for every trader who passes', 'magic': 'cut prices to the bone tomorrow, and fight the newcomer for every customer'}, 'chance': 0.6}),
    ('tell the old regulars the newcomer cuts corners, in the kitchen and in the books', 'G1', None, 0.45, '', {'mark': 'made an enemy', 'closed': "approval: a rumour spread about a rival's kitchen and books; backfire: the rumour is traced back, the rival's lawyer writes, and the old regulars feel used", 'self_control': '-', 'v': 'tradition, security', 'world': {'tribal': "tell the old trading friends the newcomer's dried meat is spoiled and the counts are crooked", 'magic': "tell the old customers the newcomer's kitchen breeds rats and the ledgers lie"}, 'chance': 0.55}),
    ("join the traders' association, and push for rules every newcomer must meet", 'W1', 'B.7', 0.5, '', {'door': True, 'v': 'power, conformity', 'world': {'tribal': 'ask the elders of the gathering for rules every newcomer must keep', 'magic': "join the street's merchants' guild, and press for rules every newcomer must meet"}, 'chance': 0.55}),
    ('rework the whole range in a weekend into something nobody else in town sells', 'U1', 'R.7', 0.5, '', {'door': True, 'identity': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'make a new kind of goods over a few nights, something no other band trades', 'magic': 'rework the whole range in a week into something no other shop in the city sells'}, 'chance': 0.65}),
    ("sponsor the street's summer fair, with the shop's name on every stall", 'B1', 'G.7', 0.5, '', {'habit': True, 'v': 'power, tradition', 'world': {'tribal': 'give a feast at the gathering, so every band remembers whose place it is', 'magic': "pay for the lane's midsummer fair, with the shop's name on every awning"}, 'chance': 0.85}),
    ('go over with two coffees, and tell the rival plainly where the line is', 'R1', 'W.7', 0.5, '', {'v': 'universalism, self-direction', 'world': {'tribal': 'cross the path with food to share, and tell the newcomer plainly what is fair', 'magic': 'cross the lane with two mugs of cider, and tell the newcomer plainly where the line is'}, 'chance': 0.8}),
    ('ask the oldest regulars what they would miss, and learn from every answer', 'G1', 'U.7', 0.5, '', {'door': True, 'v': 'benevolence, achievement', 'world': {'tribal': 'ask the oldest trading friends what they would miss, and learn from every answer'}, 'chance': 0.85}),
 ]},
{'name': 'the bank calls in the loan',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.4 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, mentor, partner, grandparent',
 'requires': 'shop owner | founder of a firm | café or bar owner | shift manager',
 'worlds': {'earth': 'the bank calls in the loan on the business, all of it, in thirty days',
            'tribal': "the trader who lent the winter's goods wants them all back before the next moon",
            'magic': "the moneylenders' house calls in the loan on the business, the whole sum, by the quarter day"},
 'timing': {'times': 'per shop owner, founder, café or bar owner or shift manager a year: about 1 in 15 see a lender '
                     "call in, cut or refuse to renew the loan the business runs on (estimate); small firms' loans "
                     'are called in by the thousand in a lean year, and about 2 lives in 10 own, found or manage a '
                     'business at some time (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The letter comes on a Tuesday: the bank is calling in the loan on the business, all of it, '
                       'in thirty days. There is a new manager at the branch and a new policy, and {N} has not '
                       'missed a payment in years.'),
                      ('W',
                       '{N} has kept every payment and every promise, and the bank has not kept its side. There must '
                       'be a proper way to put that right, and {N} means to find it.'),
                      ('U',
                       'Thirty days. {N} spreads the statements across the kitchen table and starts on the '
                       'arithmetic: what is owed, what could be sold, who else might lend.'),
                      ('B',
                       'The bank thinks it holds all the cards. {N} wonders what the business is worth to someone '
                       'else, and who would like to be asked.'),
                      ('R',
                       '{N} reads the letter twice, then throws it at the wall. Years of work, and a stranger at a '
                       'desk wants to end it in thirty days.'),
                      ('G',
                       "Everything in the place has a story: the old scales from {grandparent}'s time, the regulars' "
                       'names on the board by the door. {N} wonders whether it is time to let it all go, and start '
                       'again lighter.')],
            'tribal': [('',
                        "The trader from the river band who lent {N} the winter's goods, hides and flint and dried "
                        'meat to trade, has come back early. He wants all of it returned before the next moon, and '
                        'he will not say why.')],
            'magic': [('',
                       "A clerk from the moneylenders' house brings the letter under its seal: the loan on {Ns} "
                       'business is called in, the whole sum, by the quarter day. A new master sits in the '
                       'counting-room, and the old terms are gone.')]},
 'outcomes': (['The lender gives way, or the money is found, and the doors stay open at the turn of the month.',
               'A month later the debt is settled one way or another, and {N} sleeps through the night again.'],
              ["The time runs out, and the lender's people come for what is owed.",
               'Every door {N} knocks on stays shut, and the debt follows {N} into the new year.']),
 'options': [
    ('take every book and statement to the bank, and ask for the decision in writing', 'W1', None, 0.45, '', {'grants': 'good credit', 'v': 'security, conformity', 'world': {'tribal': 'lay every trade you have made before the lender, and ask for his reasons before the elders', 'magic': "take every ledger to the moneylenders' house, and ask for the decision under seal"}, 'chance': 0.6}),
    ('find another lender on better terms, and move the loan before the deadline', 'U1', None, 0.45, '', {'binds': True, 'v': 'achievement, security', 'world': {'tribal': 'find another trader with goods to lend, and settle the debt before the moon', 'magic': 'find another moneylender on better terms, and move the loan before the quarter day'}, 'chance': 0.6}),
    ('bring in a partner with money, for a share of the business', 'B1', None, 0.45, '', {'grants': 'investors who back you', 'aims': 'chief executive', 'binds': True, 'v': 'power, security', 'world': {'tribal': 'bring in a trader with goods to spare, for a share of every trade you make', 'magic': 'bring in a partner from a merchant house, for a share of the business'}, 'chance': 0.55}),
    ('go to the branch in person, and refuse to leave until a manager listens', 'R1', None, 0.45, '', {'self_control': '+', 'v': 'self-direction, stimulation', 'world': {'tribal': "go to the lender's fire, and refuse to leave until he hears you out", 'magic': 'go to the counting-room in person, and refuse to leave until the master listens'}, 'chance': 0.5}),
    ('sell up, clear the debt, and start again owing no one', 'G1', None, 0.45, '', {'drops': 'shop owner; café or bar owner', 'self_control': '+', 'v': 'security, tradition', 'world': {'tribal': 'trade away the place and its goods, clear the debt, and start again owing no one'}, 'chance': 0.85}),
    ('offer the bank the stock and the van as security, signed and witnessed', 'W1', 'B.7', 0.5, '', {'v': 'security, power', 'world': {'tribal': 'offer the lender your best hides and the canoe as a pledge, before the elders', 'magic': 'offer the moneylenders the stock and the cart as security, signed and sealed'}, 'chance': 0.7}),
    ('cut the business back to the one line that pays, and run it lean', 'U1', 'R.7', 0.5, '', {'self_control': '+', 'v': 'self-direction, achievement', 'world': {'tribal': 'trade only in the one thing that always sells, and travel light'}, 'chance': 0.7}),
    ("put the van and the stock in the family's name before the bank's men come", 'B1', 'G.7', 0.5, '', {'mark': 'hid a wrong', 'closed': "law: goods moved out of a creditor's reach; backfire: the court sets the transfer aside, and the family is dragged into the case", 'self_control': '-', 'v': 'security, benevolence', 'world': {'tribal': "hide the best hides and the canoe at a cousin's fire before the lender comes", 'magic': "put the cart and the stock in a cousin's name before the moneylenders' bailiffs come"}, 'chance': 0.75}),
    ("stand up at the traders' meeting, and tell everyone what the bank is doing", 'R1', 'W.7', 0.5, '', {'v': 'universalism, stimulation', 'world': {'tribal': "stand up at the gathering's fire, and tell every band what the lender is doing", 'magic': "stand up at the guild's meeting, and tell every merchant what the moneylenders are doing"}, 'chance': 0.8}),
    ('ask the old accountant who kept the books for years to find a way through', 'G1', 'U.7', 0.5, '', {'v': 'benevolence, security', 'world': {'tribal': 'ask the old trader who taught you to count to find a way through', 'magic': 'ask the old clerk who kept the ledgers for years to find a way through'}, 'chance': 0.45}),
 ]},
{'name': 'the board wants cuts by Friday',
 'stages': 'adult mature elder',
 'age': (28, 90),
 'alpha': 'W.1 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'boss, colleague, friend',
 'requires': 'chief executive',
 'worlds': {'earth': 'the board wants a plan on the table by Friday that cuts a tenth of the costs',
            'tribal': "the elders say the stores are short, and the band's trade must carry fewer hands before the "
                      'next gathering',
            'magic': "the guild council wants a tenth of the house's costs cut before its next sitting"},
 'timing': {'times': 'per chief executive a year: about 1 in 4 are told by a board or the backers to cut costs fast '
                     'after a short year (estimate); about 2 lives in 1,000 are ever a chief executive (catalogue '
                     'share; US Bureau of Labor Statistics)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The chair of the board rings on Monday night. The year's figures are short, the backers are "
                       'restless, and the board wants a plan on the table by Friday that cuts a tenth of the costs. '
                       'Everyone in the building knows that most of the costs are people.'),
                      ('W',
                       '{N} has always said the rules apply to everyone, from the loading bay to the top floor. This '
                       'week the firm finds out whether that was true.'),
                      ('U',
                       '{N} has the costs open on three screens: energy, rent, suppliers, wages. Somewhere in the '
                       'columns there is a tenth that need not be people.'),
                      ('B',
                       'The board is testing whether {N} can make the hard call. {N} means to pass the test, and to '
                       'come out of it stronger than before.'),
                      ('R',
                       '{N} thinks of the faces on the shop floor, the ones who stayed late through the bad winter. '
                       'Every line on the list has a name.'),
                      ('G',
                       'The firm grew slowly over thirty years, like a hedge, and {N} does not believe a hedge is '
                       'mended by cutting it to the root.')],
            'tribal': [('',
                        "The elders say the winter stores are short, and the band's trade must carry fewer hands "
                        'before the next gathering. {N}, who runs the trade, must say who goes back to the hunt and '
                        'who stays.')],
            'magic': [('',
                       "The guild council has sent word under its seal: the house's costs must fall by a tenth "
                       "before the next sitting, and the council will hear the guild master's plan on the first "
                       'day.')]},
 'outcomes': (['{Ns} plan is taken as it stands, and the business comes through the hard year with most of its '
               'people.',
               'By the spring the figures are back where the backers want them, and the talk among the staff has '
               'moved on.'],
              ['The plan is thrown out and another written over {Ns} head, and the cuts fall where {N} hoped they '
               'would not.',
               'The figures do not move, the backers grow louder, and the calls from the top stop being returned.']),
 'options': [
    ('cut evenly and by the rules: the same share from every department, the top included', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'world': {'tribal': "cut evenly by the old rule: the same share from every hearth, the trader's own included", 'magic': "cut evenly by the house's rules: the same share from every hall, the top table included"}, 'chance': 0.7}),
    ("change the pension scheme's small print, where only an expert would ever look", 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "law: the workers' pension promises cut without telling them; backfire: the regulator and the papers find out, and the board asks for a resignation", 'self_control': '-', 'v': 'achievement, power', 'world': {'tribal': 'quietly take back the shares of the stores promised to the old ones, where nobody counts', 'magic': "change the small print of the house's pension roll, where only a guild clerk would ever look"}, 'chance': 0.75}),
    ('sell the weakest division, and show the board a leaner, stronger firm', 'B1', None, 0.45, '', {'aims': 'magnate', 'v': 'power, achievement', 'world': {'tribal': 'give the weakest trade route to another band, and show the elders a stronger trade', 'magic': 'sell the weakest hall of the house, and show the council a leaner, stronger house'}, 'chance': 0.65}),
    ('refuse to cut a single job, and tell the board so to its face', 'R1', None, 0.45, '', {'identity': True, 'v': 'self-direction, benevolence', 'world': {'tribal': 'refuse to send a single hand back to the hunt, and tell the elders so at the fire', 'magic': 'refuse to dismiss a single hand, and tell the council so at the sitting'}, 'chance': 0.45}),
    ('ask the workers themselves where the waste is, and cut that first', 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'ask the ones who carry the trade where the waste is, and cut that first'}, 'chance': 0.65}),
    ('halve your own pay first, and ask every director to do the same', 'W1', 'R.7', 0.5, '', {'self_control': '+', 'v': 'benevolence, universalism', 'world': {'tribal': 'take half your own share of the stores first, and ask every elder to do the same', 'magic': 'halve your own wage first, and ask every master of the house to do the same'}, 'chance': 0.65}),
    ('find the tenth in rents, energy and suppliers, and keep every job', 'U1', 'G.7', 0.5, '', {'v': 'benevolence, achievement', 'world': {'tribal': 'find the tenth in wasted stores and long journeys, and keep every hand', 'magic': 'find the tenth in rents, lamp oil and suppliers, and keep every hand'}, 'chance': 0.6}),
    ("use the cuts to win the board's trust, and a seat on the backers' other boards", 'B1', 'W.7', 0.5, '', {'grants': 'a seat on boards', 'door': True, 'v': 'power, security', 'world': {'tribal': "use the hard season to win the elders' trust, and a voice at every trading circle", 'magic': "use the cuts to win the council's trust, and a seat on its other councils"}, 'chance': 0.7}),
    ('spend the week on the shop floor, and learn what the board has never seen', 'R1', 'U.7', 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'spend the days carrying loads with the others, and learn what the elders never see', 'magic': 'spend the week in the warehouses, and learn what the council has never seen'}, 'chance': 0.9}),
    ('offer the staff shorter hours now, and a share of the profits when the year turns', 'G1', 'B.7', 0.5, '', {'aims': 'magnate', 'binds': True, 'v': 'benevolence, security', 'world': {'tribal': 'offer the hands a lighter season now, and a share of the trade when the stores are full', 'magic': 'offer the hands shorter hours now, and a share of the profits when the year turns'}, 'chance': 0.7}),
 ]},
{'name': 'a takeover bid at dawn',
 'stages': 'adult mature elder',
 'age': (28, 90),
 'alpha': 'W.4 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'boss, colleague, friend, rival',
 'requires': 'chief executive',
 'worlds': {'earth': 'a bigger firm makes an offer for the whole company before the markets open',
            'tribal': "the trader of a great band offers to take the whole of the band's trade into his own",
            'magic': "a greater merchant house offers to buy the guild master's house outright, before the noon "
                     'bell'},
 'timing': {'times': 'per chief executive a year: about 1 in 20 see an offer made for the whole firm, friendly or '
                     'not (estimate); thousands of firms change hands each year, and about 2 lives in 1,000 are ever '
                     'a chief executive (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'At six in the morning the phone goes. A bigger firm has made an offer for the whole company, '
                       'a third above what it is worth on paper, and the news will be out when the markets open at '
                       'eight. The board wants {N} on a call in twenty minutes.'),
                      ('W',
                       'There are rules for a bid: the board, the owners, the regulator, the notice to the staff. '
                       '{N} gets out of bed and starts on them in order.'),
                      ('U',
                       'A third over the price is either generous or a sign the bidder knows something. {N} wants to '
                       'find out which before saying a word to anyone.'),
                      ('B',
                       'The firm is in play. Whoever moves first sets the price, and {N} intends to move first.'),
                      ('R',
                       '{N} built half of this firm, and somebody wants to buy it before breakfast. The answer '
                       'forming is not a polite one.'),
                      ('G',
                       'Thousands of people go to work for the firm, in four towns. {N} thinks of the old site by '
                       'the river, where it all began.')],
            'tribal': [('',
                        'At first light a runner comes from the great band downriver: their trader offers to take '
                        "the whole of {Ns} band's trade into his own, with goods for every hearth now and a share of "
                        'his trade forever after. The elders want an answer by the evening fire.')],
            'magic': [('',
                       "At dawn a clerk brings a letter under a great house's seal: it offers to buy {Ns} merchant "
                       "house outright, ships, halls and debts, at a third above what the guild's ledgers say it is "
                       'worth. The offer stands until the noon bell.')]},
 'outcomes': (['By nightfall the offer is settled the way {N} wanted, and the business wakes the next day still '
               'knowing itself.',
               'Weeks later the deal is done or dead, and {N} is still at the head of the table.'],
              ['The bidder goes round {N} to the owners, and by the end of the week the business has a new master.',
               'The day goes wrong from the first call, and the rest of the story is told without {N}.']),
 'options': [
    ('call the board together, and follow the rules for a bid to the letter', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'call the elders together, and follow the old way for such an offer, step by step', 'magic': "call the house's council together, and follow the guild's rules for an offer to the letter"}, 'chance': 0.6}),
    ('work through the night on what the firm is really worth, and show the board', 'U1', None, 0.45, '', {'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'count every hide, tool and trading friend the band has, and show the elders what it is worth', 'magic': 'work through the night on what the house is truly worth, and show its council'}, 'chance': 0.65}),
    ('find a friendly backer to buy a stake, and make the bid too dear', 'B1', None, 0.45, '', {'grants': 'investors who back you', 'aims': 'magnate', 'v': 'power', 'world': {'tribal': 'find a friendly band to take a share of the trade, so the great band cannot have it all', 'magic': 'find a friendly merchant house to buy a stake, and make the offer too dear'}, 'chance': 0.5}),
    ('tell a close friend to buy shares before the bid is made public', 'R1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'law: trading on what only the board knows; backfire: the regulator traces the trades to the friend, and both are charged', 'v': 'benevolence, hedonism', 'world': {'tribal': "tell your closest friend to trade for a share of the band's goods before the news is out", 'magic': 'tell a close friend to buy into the house before the offer is cried in the square'}, 'chance': 0.7}),
    ('ask the founders and the oldest staff what they want, and stand by it', 'G1', None, 0.45, '', {'mark': 'kept your word', 'v': 'tradition, benevolence', 'world': {'tribal': 'ask the oldest of the band what they want, and stand by it', 'magic': 'ask the founding family and the oldest hands what they want, and stand by it'}, 'chance': 0.75}),
    ('tell the staff the truth at the morning meeting, before the news does', 'W1', 'R.7', 0.5, '', {'identity': True, 'v': 'universalism, benevolence', 'world': {'tribal': "tell every hearth the truth before the runner's news goes round", 'magic': 'tell the hands the truth at the morning bell, before the criers do'}, 'chance': 0.7}),
    ('find out what the bidder did to the last firm it bought, town by town', 'U1', 'G.7', 0.5, '', {'v': 'universalism, security', 'world': {'tribal': 'find out what the great band did to the last band whose trade it took', 'magic': 'find out what the great house did to the last house it bought, hall by hall'}, 'chance': 0.65}),
    ("hold out for a better price, paid in the bigger firm's shares", 'B1', 'W.7', 0.5, '', {'grants': 'shares', 'self_control': '+', 'v': 'power, security', 'world': {'tribal': "hold out for more goods, and a share of the great band's trade forever after", 'magic': "hold out for a better price, paid in shares of the great house's ventures"}, 'chance': 0.8}),
    ("ring the bidder's chief executive at seven, and ask straight what they want", 'R1', 'U.7', 0.5, '', {'v': 'stimulation, self-direction', 'world': {'tribal': "walk to the great band's camp before the fire is lit, and ask their trader straight what he wants", 'magic': 'ride to the great house before the noon bell, and ask its master straight what it wants'}, 'chance': 0.6}),
    ('rally the staff and the town to buy shares together, and keep the firm local', 'G1', 'B.7', 0.5, '', {'identity': True, 'v': 'tradition, power', 'world': {'tribal': "ask every hearth to give something, so the band's trade stays the band's own", 'magic': "rally the hands and the quarter to buy shares together, and keep the house the city's own"}, 'chance': 0.55}),
 ]},
{'name': 'the board needs a chief executive',
 'stages': 'adult mature elder',
 'age': (28, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.03, 0.03, 0.01),
 'drivers': 'prosper+.3 money+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'mentor, rival, colleague, partner, boss',
 'requires': 'founder of a firm | shop owner | café or bar owner | shift manager',
 'tenure': (3.0, 100.0),
 'worlds': {'earth': 'the board of a larger firm needs a chief executive, and wants someone who knows the trade from '
                     'the till up',
            'tribal': "the band's trader at the gatherings has died, and the elders look for one who has traded well "
                      'alone',
            'magic': "the city's grocers' guild needs a new guild master, and the masters look among the shopkeepers "
                     'and merchants'},
 'timing': {'times': 'per founder, shop owner, café or bar owner or shift manager of three years or more a year: '
                     'about 1 in 30 are asked, or apply, to run a firm larger than their own (estimate); about 2 '
                     'lives in 1,000 are ever a chief executive, most after years of running a business or managing '
                     'one (catalogue share; US Bureau of Labor Statistics)',
            'likelier': "good years when firms grow and boards hire, a business of one's own that has done well, a "
                        'mentor who sits on a board, money or backers behind the name',
            'rarer': 'a lean year when boards cut rather than hire, a business far from any larger firm, a name '
                     'nobody on a board has heard',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'The chain that bought half the high street has lost its chief executive, and the board wants '
                       'someone who has run a business from the till up. {mentor} has put {Ns} name forward. There '
                       'is a plan to send in by Friday and an interview in a fortnight, and {rival}, who has run a '
                       'bigger place for longer, is on the list too.'),
                      ('W',
                       'The board will want a plan for the first year: the figures sourced, the risks named, the '
                       'promises costed. {N} starts writing it that evening, in order.'),
                      ('U',
                       "{N} reads the chain's last ten years of accounts on the train, and by the last stop has "
                       'found three things the board seems never to have noticed.'),
                      ('B',
                       'Running a chain is a different game from running a single place, and {N} has waited years to '
                       'play it. The vote is what counts, and {N} starts counting who holds one.'),
                      ('R',
                       '{N} could do this job, and could do it better than the last one. {N} is not going to pretend '
                       'otherwise in the interview.'),
                      ('G',
                       'The chain was a family firm once, before the backers came. {N} remembers when every branch '
                       'knew its customers by name, and wonders whether it could again.')],
            'tribal': [('',
                        "The band's trader at the gatherings, who carried its trade for many winters, has died, and "
                        'the elders look for someone who has traded well alone to carry it now. They have spoken '
                        '{Ns} name at the fire, and the name of {rival}.')],
            'magic': [('',
                       "The grocers' guild of the city has lost its guild master, and the masters look among the "
                       'shopkeepers and merchants for the next. {mentor} has spoken {Ns} name at the guildhall, and '
                       '{rival} is spoken of too.')]},
 'outcomes': (['The choice falls on {N}, and on the first morning a great many people are waiting to hear what {N} '
               'will say.',
               'Whatever {N} chose, the year that follows is a good one, and the name is known further than before.'],
              ['The board thanks {N} warmly, and chooses {rival}.',
               'The interview goes wrong in the first ten minutes, and the rest of the hour is very long.']),
 'options': [
    ('send the board a plan for the first year, every figure checked and sourced', 'W1', None, 0.45, '', {'title': 'chief executive', 'v': 'conformity, achievement', 'world': {'tribal': 'lay out before the elders how the trade will be carried, season by season', 'magic': 'send the guild a plan for the first year, every figure checked against the ledgers'}, 'chance': 0.25}),
    ('show the board what the accounts say that nobody has noticed', 'U1', None, 0.45, '', {'title': 'chief executive', 'requires': 'bookkeeping', 'without': 'approval', 'lacking': 0.5, 'v': 'achievement, self-direction', 'world': {'tribal': 'show the elders what the counted trades say that nobody has noticed', 'magic': 'show the guild what its own ledgers say that nobody has noticed'}, 'chance': 0.25}),
    ('ring every board member you know, and have the vote won before the interview', 'B1', None, 0.45, '', {'title': 'chief executive', 'aims': 'chief executive', 'v': 'power, achievement', 'world': {'tribal': "visit every elder's fire before the choosing, and have the choice made before it is spoken", 'magic': 'call on every guild master you know, and have the vote won before the sitting'}, 'chance': 0.25}),
    ('walk into the interview, and tell them straight what is wrong with the firm', 'R1', None, 0.45, '', {'title': 'chief executive', 'v': 'stimulation, self-direction', 'world': {'tribal': 'stand before the elders, and tell them straight what is wrong with the trade', 'magic': 'walk into the guildhall, and tell the masters straight what is wrong with the guild'}, 'chance': 0.25}),
    ('promise to run it like the family firm it once was, every branch known by name', 'G1', None, 0.45, '', {'title': 'chief executive', 'v': 'tradition, benevolence', 'world': {'tribal': "promise to carry the trade the old way, every band's trading friends known by name", 'magic': 'promise to run the guild as the old masters did, every shop known by name'}, 'chance': 0.25}),
    ('put money into the chain instead, and take a stake in the firm', 'B.5 G.5', None, 0.5, '', {'grants': 'stake in the firm', 'v': 'power, security', 'world': {'tribal': "give goods to the band's trade instead, for a share of what it brings back", 'magic': "put silver into the guild's venture instead, for a share of its trade"}, 'chance': 0.75}),
    ('say no, and pour the year into your own place and its regulars', 'R.5 G.5', None, 0.5, '', {'habit': True, 'self_control': '+', 'v': 'self-direction, tradition', 'world': {'tribal': 'say no, and give the season to your own trading place and its old friends', 'magic': 'say no, and give the year to your own shop and its regulars'}, 'chance': 0.75}),
    ('ask for a year as deputy first, to learn the firm from the inside', 'U.5 B.5', None, 0.5, '', {'grants': 'inner circle at work', 'v': 'achievement, power', 'world': {'tribal': 'ask to walk beside the new trader for a season, to learn the trade from the inside', 'magic': "ask to serve a year as the new master's deputy, to learn the guild from the inside"}, 'chance': 0.75}),
    ('tell the board honestly that a colleague would do it better, and back them', 'W.5 R.5', None, 0.5, '', {'v': 'benevolence, universalism', 'world': {'tribal': 'tell the elders honestly that another would carry it better, and stand behind them', 'magic': 'tell the guild honestly that another shopkeeper would do it better, and back them'}, 'chance': 0.75}),
    ("take a year's course in running a large firm before putting a name forward", 'W.5 U.5', None, 0.5, '', {'mark': 'learned a skill', 'v': 'achievement, conformity', 'world': {'tribal': 'sit a winter with the old trader of the next band, and learn how a great trade is carried', 'magic': "take a year's lessons from an old guild master before putting a name forward"}, 'chance': 0.75}),
 ]},
{'name': 'a rival firm is for sale',
 'stages': 'adult mature elder',
 'age': (30, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.03, 0.02),
 'drivers': 'prosper+.2 money+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'rival, partner, colleague, boss, friend',
 'requires': 'chief executive | founder of a firm',
 'tenure': (4.0, 100.0),
 'worlds': {'earth': 'the rival firm everyone in the trade knows is for sale, and the family wants it settled by the '
                     'summer',
            'tribal': 'the old trader of the far band can travel no more, and his trade along the rivers goes to '
                      'whoever can carry it',
            'magic': 'a rival merchant house is for sale, its ships, halls and trading rights, and the heirs want it '
                     'settled by midsummer'},
 'timing': {'times': 'per chief executive of four years or founder of eight a year: about 1 in 40 see a rival they '
                     'could buy come up for sale (estimate); thousands of firms are bought each year, but few buyers '
                     "become the owner of a country's great business group: about 5 lives in 100,000 are ever a "
                     'magnate (catalogue share; estimate)',
            'likelier': "good years and cheap loans, backers or shares to pay with, a rival's founder retiring with "
                        'no heir in the trade, a seat on boards that hears early',
            'rarer': 'a lean year, dear money, a regulator watching the trade, a firm already stretched',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'The rival firm {N} has fought for years, across every town and every contract, is for sale. '
                       'The founder is old, the children want out, and the papers say the family will settle by the '
                       'summer. With it would come the second name in the trade, and a business that would reach '
                       'across the land.'),
                      ('W',
                       "The rival's workers are good at what they do, and many have been there thirty years. If the "
                       'firm changes hands, {N} thinks, it should be into hands that keep faith with them.'),
                      ('U',
                       "Joined well, the two firms would be more than the sum of them: the rival's buyers and {Ns} "
                       'systems. Joined badly, they would be a mess for ten years. {N} wants to see the numbers.'),
                      ('B',
                       'This is the deal that turns a firm into an empire. {N} has wanted it for years, and so, {N} '
                       'knows, have three other buyers.'),
                      ('R',
                       'For years the rival was the enemy across the market. Now the old founder wants out, and {N} '
                       'wants to go and see the old fighter face to face.'),
                      ('G',
                       'The rival began as a family shop in a market town, as {Ns} own did. {N} wonders what the '
                       'town would become if a stranger bought it and moved it away.')],
            'tribal': [('',
                        'The old trader of the far band, whose trade has run along the rivers longer than anyone '
                        'remembers, can travel no more. His trading friends in every camp will need someone to trade '
                        'with, and the bands ask who will carry it.')],
            'magic': [('',
                       'The house of an old rival, ships, halls and trading rights along the coast, is for sale: the '
                       'old merchant is dying and the heirs want silver. Whoever buys it will be named among the '
                       'great houses of the realm.')]},
 'outcomes': (['The papers are signed at last, and overnight {N} answers for twice as many people as before.',
               'Whatever {N} chose, the business comes through the year stronger, and the trade talks about how it '
               'was done.'],
              ['Another buyer outbids everyone in the last week, and the rival goes to a stranger.',
               "The deal falls apart over the last details, and {N} is left with the lawyers' bills and a long "
               'summer.']),
 'options': [
    ('offer a fair price, and promise in writing to keep every site and pension', 'W1', None, 0.45, '', {'title': 'magnate', 'grants': 'a business empire', 'v': 'conformity, benevolence', 'world': {'tribal': 'offer the old trader a fair price, and promise before the elders to keep every trading friend', 'magic': 'offer a fair price, and promise under seal to keep every hall and hand'}, 'chance': 0.06}),
    ("pay in the firm's own shares, with a plan that joins the best of both", 'U1', None, 0.45, '', {'title': 'magnate', 'grants': 'a business empire', 'requires': 'shares', 'without': 'means', 'lacking': 0.5, 'v': 'achievement, power', 'world': {'tribal': "pay with a share of your own band's trade, and a plan that joins the best routes of both", 'magic': 'pay in shares of your own house, with a plan that joins the best of both'}, 'chance': 0.06}),
    ("put your savings and the firm's credit behind a bid nobody else can match", 'B1', None, 0.45, '', {'title': 'magnate', 'grants': 'a business empire', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'aims': 'magnate', 'identity': True, 'v': 'power', 'world': {'tribal': 'put every good you own behind an offer no other trader can match', 'magic': "put your savings and the house's credit behind a bid no other house can match"}, 'chance': 0.06}),
    ('go to see the old founder tonight, and shake on it over dinner', 'R1', None, 0.45, '', {'title': 'magnate', 'grants': 'a business empire', 'binds': True, 'v': 'stimulation, self-direction', 'world': {'tribal': "walk to the old trader's camp tonight, and settle it at his fire", 'magic': "ride to the old merchant's house tonight, and settle it over supper"}, 'chance': 0.06}),
    ('buy it to keep the old firm in its town, and its people in work', 'G1', None, 0.45, '', {'title': 'magnate', 'grants': 'a business empire', 'v': 'tradition, benevolence', 'world': {'tribal': "take it on to keep the old trader's friends in every camp, as they always were", 'magic': 'buy it to keep the old house in its port, and its hands in work'}, 'chance': 0.06}),
    ("buy only the rival's best site, fast, before the sale goes to auction", 'B.5 R.5', None, 0.5, '', {'grants': "premises of one's own", 'v': 'power, stimulation', 'world': {'tribal': "take only the old trader's best camp on the river, before anyone else can", 'magic': "buy only the old house's best wharf, fast, before the sale is cried"}, 'chance': 0.76}),
    ('merge as equals, with both names over the door side by side', 'U.5 G.5', None, 0.5, '', {'grants': 'business partner', 'v': 'universalism, achievement', 'world': {'tribal': 'join the two trades as equals, both names spoken at every fire', 'magic': 'join the two houses as equals, both names over the door'}, 'chance': 0.76}),
    ('let it go, and build from nothing the one thing they did better', 'U.5 R.5', None, 0.5, '', {'v': 'self-direction, achievement', 'world': {'tribal': 'let it go, and learn to make the one thing they traded better'}, 'chance': 0.76}),
    ("hire the rival's best managers when the sale falls through", 'W.5 B.5', None, 0.5, '', {'v': 'power, security', 'world': {'tribal': "take in the old trader's best carriers when nobody else takes the trade", 'magic': "hire the old house's best clerks and captains when the sale falls through"}, 'chance': 0.76}),
    ('pass, and keep the firm the size it is, with no new debt', 'W.5 G.5', None, 0.5, '', {'v': 'security, tradition', 'world': {'tribal': "let it pass, and keep the band's trade the size it is, owing no one", 'magic': 'pass, and keep the house the size it is, with no new debt'}, 'chance': 0.76}),
 ]},
{'name': 'the numbers that would look better moved',
 'stages': 'young_adult adult mature elder',
 'age': (22, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.015, 0.01),
 'drivers': 'prosper-.3 money-.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague, mentor, boss, friend',
 'requires': 'chief executive | magnate | founder of a firm | shop owner',
 'worlds': {'earth': "the year's figures are short, the backers are watching, and the accounts go to the auditors "
                     'next week',
            'tribal': "the band's count of goods is short before the gathering, and the traders who share their "
                      'goods will ask',
            'magic': "the house's ledgers are short before the guild's reckoning, and its backers among the merchant "
                     'houses are watching'},
 'timing': {'times': "per chief executive, magnate, founder or shop owner a year: about 1 in 80 face a year's "
                     'figures short enough that someone suggests moving them before the audit (estimate); the four '
                     'titles are about 7 lives in 100 (catalogue shares), so about 1 life in 200 meets it; fraud '
                     "surveys find that a real share of firms' false accounts begin as one short year covered over",
            'likelier': 'a lean year, backers who sell at the first bad figure, a loan whose terms turn on the '
                        "year's profit, a finance head who wants to help",
            'rarer': 'a firm with no outside backers, a good year, an auditor who knows the business well',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       "It is the last week before the year's accounts go to the auditors, and the figures are "
                       'short: a contract lost in the spring, a customer who went under owing money. The backers are '
                       'watching. {colleague}, who runs the finances, closes the door and says that a few costs '
                       'could sit in next year instead, and nobody would ever know.'),
                      ('W',
                       'The accounts are a promise to everyone who reads them: the backers, the bank, the staff, the '
                       "tax office. {N} has signed every year's set without a second thought, until now."),
                      ('U',
                       '{N} can see exactly how it would be done: which costs, which month, which line. It is '
                       'clever, and that is the trouble with it.'),
                      ('B',
                       'Backers do not forgive a bad year; they sell. One clean set of figures now, and next year '
                       'will put it right. {N} knows how that sentence usually ends.'),
                      ('R',
                       '{N} hates the feeling in the room: the closed door, the low voice. It would be simpler to '
                       'ring the backers and say the truth out loud.'),
                      ('G',
                       'The business has come through bad years before, the way a farm comes through a dry summer. '
                       '{N} thinks of the people on the payroll, and what a run on the backers would mean for '
                       'them.')],
            'tribal': [('',
                        'Before the gathering the band counts its goods, and the count is short: a canoe lost on the '
                        'river, a trade gone bad. The traders who share their goods with {N} will ask. {colleague}, '
                        'who keeps the count, says quietly that a few bundles could be counted twice.')],
            'magic': [('',
                       "The guild's reckoning is a week away and the house's ledgers are short: a ship lost in the "
                       "spring storms, a debtor fled. {colleague}, the house's clerk, closes the counting-room door "
                       "and says a few debts could be written into next year's book, and no auditor would ever "
                       'see.')]},
 'outcomes': (['The year closes the way {N} meant it to, and the backers are still there in the spring.',
               'A few months on, the gap is closed one way or another, and {N} can look the auditors in the eye.'],
              ['The backers hear the worst before {N} can tell it well, and two of them sell by the end of the '
               'month.',
               'It goes wrong from the first week, the gap grows, and the trade starts to talk about {Ns} business '
               'in a low voice.']),
 'options': [
    ('tell the backers the truth before the figures go out, as promised', 'W1', None, 0.45, '', {'mark': 'kept your word', 'self_control': '+', 'v': 'conformity, universalism', 'world': {'tribal': 'tell the traders who share their goods the true count before the gathering', 'magic': 'tell the backers the truth before the ledgers go to the guild, as promised'}, 'chance': 0.62}),
    ('find the real cause of the gap, and show the backers a plan to close it', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'find what went wrong with the count, and show the traders how it will be made good'}, 'chance': 0.67}),
    ('sell a part of the firm to a backer, and cover the gap with real money', 'B1', None, 0.45, '', {'grants': 'investors who back you', 'v': 'power, security', 'world': {'tribal': 'give a trader of another band a share of the trade, for goods to cover the gap', 'magic': 'sell a share of the house to a merchant house, and cover the gap with true silver'}, 'chance': 0.68}),
    ('ring every backer tonight, tell them straight, and ask them to hold their nerve', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'world': {'tribal': "go to every trader's fire tonight, tell them the count straight, and ask them to stay", 'magic': 'call on every backer tonight, tell them straight, and ask them to hold their nerve'}, 'chance': 0.72}),
    ('ask the old suppliers to wait a season for their money, as in the bad years', 'G1', None, 0.45, '', {'v': 'tradition, security', 'world': {'tribal': 'ask the old trading friends to wait a season for their goods, as in the hard winters', 'magic': 'ask the old suppliers to wait a season for their silver, as in the bad years'}, 'chance': 0.67}),
    ('show the staff the true figures, and cut the costs together, openly', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, benevolence', 'world': {'tribal': 'show every hearth the true count, and share the shortfall openly', 'magic': 'show the hands the true ledgers, and cut the costs together, openly'}, 'chance': 0.75}),
    ('ask the old accountant who taught you the trade to audit every line early', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'security, tradition', 'world': {'tribal': 'ask the old trader who taught you to count to go through every bundle', 'magic': 'ask the old clerk who taught you the trade to go through every line early'}, 'chance': 0.75}),
    ('take the loss on your own savings, quietly, so nobody is laid off', 'W.34 B.33 G.33', None, 0.5, '', {'takes': 'savings', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'benevolence, security', 'world': {'tribal': 'cover the gap from your own stores, quietly, so no hearth goes short', 'magic': 'cover the gap from your own purse, quietly, so no hand is let go'}, 'chance': 0.85}),
    ('move a few costs into next year, and sign off accounts that look healthy', 'U.34 B.33 R.33', None, 0.5, '', {'mark': 'hid a wrong', 'closed': 'law: the accounts falsified; backfire: the auditors find it, the backers pull out, and the boards want the name off their papers', 'takes_if_fails': 'a seat on boards', 'self_control': '-', 'v': 'power, security', 'world': {'tribal': 'count a few bundles twice, and give the traders a count that looks healthy', 'magic': "write a few debts into next year's book, and send the guild a ledger that looks healthy"}, 'chance': 0.7}),
    ('ask the biggest customer for an early payment, and a longer contract', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'security, power', 'world': {'tribal': 'ask the band that trades most with yours for goods now, and a longer friendship', 'magic': "ask the house's biggest customer for silver now, and a longer contract"}, 'chance': 0.6}),
 ]},
{'name': 'the market stall that became a chain',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.01, 0.005),
 'drivers': 'prosper+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'friend, mentor, partner, rival, grandparent',
 'requires': 'shop owner | café or bar owner | shop assistant',
 'tenure': (2.0, 99.0),
 'worlds': {'earth': 'the Saturday stall has a queue every week, and three shopping centres and an investor want '
                     'more of it',
            'tribal': 'the honey cakes from one fire are traded at every camp along the river, and far bands send '
                      'for more',
            'magic': 'the pie stall on the market square draws a crowd every market day, and merchants of three '
                     'cities write for more'},
 'timing': {'times': 'per shop owner or café or bar owner of two years, or shop assistant of four, a year: about 1 '
                     'in 100 find something they make or sell on the side drawing queues far beyond their own street '
                     '(estimate); most market stalls and small shops stay one place for life, and only a handful a '
                     'year grow into a chain; about 2 lives in 1,000 are ever a chief executive and about 3 in 100 '
                     'found a firm (catalogue shares)',
            'likelier': 'something people queue for, good years when shopping centres want new names, a backer who '
                        'notices, a friend who knows the trade',
            'rarer': 'a lean year, a town with little to spend, no time beside the day job, no savings at all',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'Two years ago {N} started a stall at the Saturday market with a recipe for spiced pies, to '
                       'make a little on the side. Now there is a queue round the square by nine, the pies are gone '
                       'by noon, three shopping centres have asked for a stall in their halls, and an investor in a '
                       'good coat has left a card.'),
                      ('W',
                       "{N} has kept the stall's accounts in an exercise book from the start, every pie and every "
                       'sale, and wants to know what doing this properly would look like before saying yes to '
                       'anyone.'),
                      ('U',
                       '{N} has been timing the queue: three minutes a customer at the start, forty seconds now. '
                       'Somewhere in that is a system, and a system can be copied.'),
                      ('B',
                       "A queue like that is money standing in line. {N} turns the investor's card over and over, "
                       'and starts counting shopping centres.'),
                      ('R',
                       '{N} wants to say yes to all of it at once: the halls, the investor, the second stall and the '
                       'third. Life is too short to bake for one square.'),
                      ('G',
                       "The recipe is {grandparent}'s, from a kitchen in a town with no shopping centres at all. {N} "
                       'wonders how big a thing can grow before it stops being itself.')],
            'tribal': [('',
                        "The honey cakes {N} bakes at the fire, a way of {grandparent}'s, are traded at every camp "
                        'along the river now. Runners come from far bands asking for more, and a trader from the '
                        'great band downriver offers goods for every cake {N} can make.')],
            'magic': [('',
                       '{Ns} pie stall on the market square draws a crowd every market day. Merchants of three '
                       'cities have written asking for stalls of their own, and a backer from a merchant house has '
                       'left a sealed card.')]},
 'outcomes': (['Within a year the thing {N} started is sold in three places at once, and the first stall still has '
               'its queue.',
               'Whatever {N} chose, the baking goes on, and {N} is glad of the road taken.'],
              ['The money comes with terms nobody could meet, and by the winter it is one stall again.',
               'The second place never takes, the crowds do not follow, and {N} goes back to the first stall with a '
               'little less pride and the same good recipe.']),
 'options': [
    ('register the business properly, and open the second stall by the book', 'W1', None, 0.45, '', {'title': 'founder of a firm', 'requires': 'shop assistant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, security', 'world': {'tribal': "ask the elders' leave, and set a second fire for the cakes at the next gathering, as is proper", 'magic': 'register the business with the guild, and open the second stall by its rules'}, 'chance': 0.03}),
    ('write down the recipe and the system, so any stall can run like the first', 'U1', None, 0.45, '', {'title': 'founder of a firm', 'requires': 'shop assistant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'teach the way of the cakes step by step, so any fire can bake them like the first', 'magic': 'write down the recipe and the system, so any stall in any city can run like the first'}, 'chance': 0.03}),
    ("take the investor's money, and open in every shopping centre that asked", 'B1', None, 0.45, '', {'title': 'chief executive', 'requires': 'shop owner', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'power, achievement', 'world': {'tribal': "take the great band's goods, and send cakes to every camp that asked", 'magic': "take the merchant house's silver, and open in every city that wrote"}, 'chance': 0.03}),
    ('quit the day job on Monday, and open three stalls at once', 'R1', None, 0.45, '', {'title': 'founder of a firm', 'requires': 'shop assistant', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'leave the hunt to the others, and set three fires baking at once', 'magic': 'leave the shop counter on Monday, and open three stalls at once'}, 'chance': 0.03}),
    ("grow it slowly with the café's own people, one new place a year", 'G1', None, 0.45, '', {'title': 'chief executive', 'requires': 'café or bar owner', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'tradition, benevolence', 'world': {'tribal': 'let it grow slowly with your own kin, one new fire each summer', 'magic': "grow it slowly with the tavern's own people, one new house a year"}, 'chance': 0.03}),
    ('open one more stall, and run both well for a year before deciding', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'set one more fire, and keep both well for a year before deciding'}, 'chance': 0.84}),
    ('keep it one stall, and keep the Saturdays for the joy of it', 'W.34 R.33 G.33', None, 0.5, '', {'habit': True, 'v': 'hedonism, tradition', 'world': {'tribal': 'keep it one fire, and bake for the joy of it', 'magic': 'keep it one stall, and keep the market days for the joy of it'}, 'chance': 0.84}),
    ('sell the recipe to a big chain for a fair price and a share', 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'savings', 'v': 'power, security', 'world': {'tribal': 'trade the way of the cakes to the great band, for goods now and a share later', 'magic': 'sell the recipe to a great house for a fair price and a share'}, 'chance': 0.84}),
    ('take an evening course in running a business while the stall keeps going', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'bookkeeping', 'self_control': '+', 'v': 'achievement, self-direction', 'world': {'tribal': 'sit with an old trader through the winter, and learn how a trade is carried', 'magic': 'take lessons from a guild clerk in the evenings while the stall keeps going'}, 'chance': 0.84}),
    ('ask the investor for a smaller sum, and a mentor from their firm', 'U.34 B.33 G.33', None, 0.5, '', {'grants': 'mentor', 'v': 'achievement, benevolence', 'world': {'tribal': "ask the great band's trader for a little, and to teach you the trade", 'magic': 'ask the backer for a smaller sum, and a mentor from the merchant house'}, 'chance': 0.84}),
 ]},
{'name': 'a seat among the merchant princes',
 'stages': 'adult mature elder',
 'age': (30, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'prosper+.2 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, money, publiclife',
 'horizon': 'months',
 'roles': 'rival, mentor, friend, boss',
 'requires': 'chief executive | founder of a firm',
 'tenure': (3.0, 99.0),
 'worlds': {'magic': 'a seat on the council of merchant princes falls free, and the princes vote at the new moon'},
 'only': 'magic',
 'timing': {'times': 'per guild master or merchant with a house of their own, of three years or more, in the magic '
                     'world a year: about 1 in 60 see a seat on the council of merchant princes fall free while they '
                     "could stand for it (estimate); the council's seats are few and held for life, and the merchant "
                     'princes are about 5 lives in 100,000 (catalogue share for the magnate; estimate)',
            'likelier': 'a house that has traded well for years, backers among the great houses, a prince who owes '
                        'the house a favour',
            'rarer': "a lean year at sea, a house far from the capital's port, an old feud with a prince's family",
            'gap_years': (8.0, 15.0)},
 'scenes': {'magic': [('',
                       'The oldest of the merchant princes, who held the spice wharves for fifty years, has died, '
                       'and his seat on the council falls free. The princes will vote at the new moon, and {rival} '
                       'is already sending gifts. In the cellars under the old counting-house, the merchants '
                       'whisper, something older than the city keeps a ledger of every debt, and will turn a vote '
                       'for a price it names later.'),
                      ('W',
                       "The council's charter is four hundred years old, and every word of it still binds. Its "
                       'oldest page, {N} knows, speaks of an oath the founders swore in the vault below.'),
                      ('U',
                       "The princes' votes each have a reason. {N} has started a chart of who owes whom, who fears "
                       'whom and who hates whom.'),
                      ('B',
                       "A seat among the princes is a share of the realm's trade for life, and a name the king's "
                       'treasurer knows. {N} has wanted it since the first ship came home.'),
                      ('R',
                       '{N} would rather win the seat at the council table, face to face, than by a hundred whispers '
                       'in a hundred corridors.'),
                      ('G',
                       '{Ns} house has traded on the old coast road for four generations. {N} thinks of the families '
                       'along it, and what a seat on the council would mean for them.')]},
 'outcomes': (['At the new moon the princes vote, and {N} takes the empty chair at the council table.',
               "Whatever {N} chose, the season of the vote is remembered well, and the house's name is spoken in the "
               'great halls.'],
              ["The princes choose another house, and {N} is thanked by the council's clerk and shown down the long "
               'stair.',
               "The vote is put off a year, the seat goes to a prince's nephew, and the house is no nearer the "
               'table.']),
 'options': [
    ("go down to the old vault, and swear the founder's oath to what keeps the ledgers", 'W1', None, 0.45, '', {'title': 'magnate', 'mark': 'hid a wrong', 'closed': "approval: a bargain sworn with the old thing under the counting-house, without the Order's leave; backfire: it comes to collect, and takes the house's luck and the seat with it", 'binds': True, 'self_control': '-', 'v': 'tradition, power', 'chance': 0.16}),
    ('chart who owes whom, and win each prince with what that prince wants', 'U1', None, 0.45, '', {'title': 'magnate', 'v': 'achievement, power', 'chance': 0.06}),
    ('call in every debt the princes owe the house, one by one, before the vote', 'B1', None, 0.45, '', {'title': 'magnate', 'aims': 'magnate', 'v': 'power', 'chance': 0.06}),
    ('stand up at the council table, and ask for the seat face to face', 'R1', None, 0.45, '', {'title': 'magnate', 'v': 'stimulation, self-direction', 'chance': 0.06}),
    ('bring the families of the coast road to the guildhall to speak for the house', 'G1', None, 0.45, '', {'title': 'magnate', 'v': 'tradition, benevolence', 'chance': 0.06}),
    ('back an old friend for the seat, and ask a share of the trade in return', 'B.5 G.5', None, 0.5, '', {'grants': 'friend in power', 'v': 'power, tradition', 'chance': 0.65}),
    ("buy the dead prince's ships at the auction, while the others argue", 'B.5 R.5', None, 0.5, '', {'grants': 'shares', 'v': 'power, stimulation', 'chance': 0.85}),
    ('wait a year, learn how the council votes, and stand next time', 'U.5 G.5', None, 0.5, '', {'mark': 'learned a skill', 'self_control': '+', 'v': 'achievement, security', 'chance': 0.85}),
    ('speak at the guildhall against seats bought and sold, whoever wins', 'W.5 R.5', None, 0.5, '', {'v': 'universalism, conformity', 'chance': 0.65}),
    ("ask for the council's clerkship instead, and learn its votes from the inside", 'W.5 U.5', None, 0.5, '', {'grants': 'inner circle at work', 'v': 'achievement, security', 'chance': 0.65}),
 ]},
{'name': 'the corporal is hurt on exercise',
 'stages': 'young_adult adult mature',
 'age': (17, 55),
 'alpha': 'W.4 U.1 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'moment',
 'roles': 'colleague, boss, friend',
 'requires': 'soldier',
 'worlds': {'earth': "a night exercise in the hills: the section's corporal falls on the scree and breaks a leg, and "
                     'someone has to take charge and get everyone down',
            'tribal': "a night watch in the hills: the leader of the hunters' party falls among the rocks and breaks "
                      'a leg, and someone has to bring everyone down to the camp',
            'magic': 'a night march over the fells: the corporal of the file falls on the scree and breaks a leg, '
                     'and someone has to bring everyone down to the fort'},
 'timing': {'times': 'per soldier a year: about 1 in 8 sees a comrade hurt badly enough on exercise or in training '
                     'to be carried off, with no officer near (estimate); training injuries are the commonest '
                     'injuries in peacetime armies, most of them to the legs and feet (armed forces injury surveys); '
                     'about 5 lives in 100 serve as soldiers (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Two in the morning on the exercise, high on the hill and in rain. The corporal, {colleague}, '
                       'slips on the scree, goes down hard and cannot stand: the leg is broken. Seven soldiers, one '
                       'radio, a map in a wet pocket and the meeting point far below, and everyone looks at everyone '
                       'else, and then at {N}.'),
                      ('W',
                       'There is a drill for this, and {N} learned it in the first week: the casualty first, then '
                       'the radio, then the count, then the route. Somebody has to say it out loud.'),
                      ('U',
                       '{N} pulls out the map under a torch, works out where they are to a hundred metres, and '
                       'starts thinking about the gentlest way off the hill rather than the shortest.'),
                      ('B',
                       'Someone will take charge in the next minute, and whoever does will be the one the officers '
                       'hear about tomorrow. {N} knows it, and so does everyone else in the section.'),
                      ('R',
                       '{N} is moving before anyone speaks: down beside the corporal, a hand on the shoulder, a joke '
                       'to stop the shaking. The rain is coming sideways, and there is no time to wait for orders.'),
                      ('G',
                       'The section has eaten, slept and marched together for a year. {N} looks round at the cold '
                       'faces and knows who is frightened, who is fine, and who will carry their end of a stretcher '
                       'all night without a word.')],
            'tribal': [('',
                        "High in the hills on the night watch, in rain, the leader of the hunters' party slips among "
                        'the rocks and cannot stand: the leg is broken. Six hunters of the guard, one torch and the '
                        'camp far below in the dark, and they all look at {N}.')],
            'magic': [('',
                       'On the night march over the fells the corporal of the file slips on the scree and cannot '
                       'stand: the leg is broken. Seven soldiers of the realm, one lantern and the fort far below, '
                       'and they all look at {N}.')]},
 'outcomes': (['By dawn everyone is off the hill, the broken leg is in good hands, and nobody else is hurt.',
               'The story of the night goes round the next day, and {Ns} name is in it.'],
              ['The way down takes the whole night, two more turn their ankles, and the questions start the next '
               'morning.',
               'Help comes late, and they arrive cold, shaken and arguing over who should have done what.']),
 'options': [
    ('take charge by the drill: the casualty, the radio, the count, then the route', 'W1', None, 0.45, '', {'grants': 'leading soldiers', 'aims': 'army officer', 'v': 'conformity, security', 'world': {'tribal': 'take charge as the old hunters taught: the hurt one, the signal fire, the count, the path', 'magic': 'take charge by the drill: the casualty, the signal horn, the count, the road'}, 'chance': 0.7}),
    ('find the gentlest way down on the map, and splint the leg before anyone moves', 'U1', None, 0.45, '', {'mark': 'learned a skill', 'v': 'achievement, security', 'world': {'tribal': 'find the gentlest path down by the stars, and bind the leg to a spear shaft before anyone moves'}, 'chance': 0.7}),
    ('get on the radio first, and make sure the officers know who took charge', 'B1', None, 0.45, '', {'aims': 'army officer', 'v': 'power, achievement', 'world': {'tribal': 'run to the ridge and light the signal fire, so the camp knows who took charge', 'magic': 'sound the horn for the fort, and make sure the captain knows who took charge'}, 'chance': 0.65}),
    ('carry the corporal down on your back, and let the others follow', 'R1', None, 0.45, '', {'grants': 'mentioned in dispatches', 'body': 'heavy', 'v': 'benevolence, stimulation', 'world': {'tribal': 'carry the hurt leader down the hill on your back, and let the others follow', 'magic': 'carry the corporal down on your back, and let the file follow'}, 'chance': 0.6}),
    ('keep everyone close and calm under the rocks, and wait warm for the rescue', 'G1', None, 0.45, '', {'self_control': '+', 'v': 'benevolence, security', 'world': {'tribal': 'keep everyone close and calm under the overhang, and wait warm for the camp to come', 'magic': "keep the file close and calm under the rocks, and wait warm for the fort's riders"}, 'chance': 0.75}),
    ('set a rota so everyone takes a turn keeping the corporal warm and talking', 'W1', 'G.7', 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'set a turn for each hunter to keep the hurt leader warm and talking', 'magic': 'set a rota so each soldier takes a turn keeping the corporal warm and talking'}, 'chance': 0.7}),
    ('log the time, the grid reference and every step taken, for the report', 'U1', 'W.7', 0.5, '', {'habit': True, 'v': 'conformity, security', 'world': {'tribal': 'mark the place with stones, and keep every step taken in mind for the elders', 'magic': "note the hour, the place and every step taken, for the captain's report"}, 'chance': 0.7}),
    ('listen to how the officers run the rescue, and learn it for your own turn', 'B1', 'U.7', 0.5, '', {'door': True, 'self_control': '+', 'v': 'achievement, power', 'world': {'tribal': 'watch how the old hunters bring the party in, and learn it for your own turn', 'magic': 'watch how the sergeants run the rescue, and learn it for your own turn'}, 'chance': 0.75}),
    ('run the whole way down alone for help, faster than anyone thinks possible', 'R1', 'B.7', 0.5, '', {'body': 'heavy', 'mark': 'took a wild risk', 'v': 'stimulation, achievement', 'world': {'tribal': 'run down alone through the dark to the camp, faster than anyone thinks possible', 'magic': 'run down alone through the dark to the fort, faster than anyone thinks possible'}, 'chance': 0.8}),
    ("sing the section's old songs all the way down, so nobody's spirit breaks", 'G1', 'R.7', 0.5, '', {'grants': 'old comrades', 'v': 'benevolence, tradition', 'world': {'tribal': "sing the band's old songs all the way down, so nobody's heart fails", 'magic': "sing the company's old marching songs all the way down, so nobody's heart fails"}, 'chance': 0.65}),
 ]},
{'name': 'the platoon gets a new sergeant',
 'stages': 'young_adult adult mature',
 'age': (17, 55),
 'alpha': 'W.1 U.4 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'colleague, boss, mentor',
 'requires': 'soldier',
 'worlds': {'earth': 'a new sergeant comes to the platoon and picks on its slowest recruit: extra drills at dawn, a '
                     "nickname, the whole platoon punished for one soldier's mistakes",
            'tribal': 'a new leader of the watch picks on the slowest hunter of the guard: the worst watches, the '
                      'heaviest loads, mockery at the fire',
            'magic': 'a new sergeant comes to the company and rides its slowest recruit: extra drill, the latrines, '
                     'names shouted across the parade ground'},
 'timing': {'times': 'per soldier a year: about 1 in 6 serves under a sergeant or a corporal who singles one soldier '
                     'out (estimate); service attitude surveys in several armies find about 1 serving soldier in 8 '
                     'to 10 reporting bullying, harassment or discrimination in a year; about 5 lives in 100 serve '
                     'as soldiers (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The new sergeant has been with the platoon a fortnight and has already found a target: '
                       '{colleague}, the slowest runner and the clumsiest on the range. Extra drills at dawn, a '
                       'nickname that has stuck, and the whole platoon doing press-ups in the mud for every mistake '
                       '{colleague} makes. Some of the others have started to join in.'),
                      ('W',
                       'The army has rules about how a sergeant may treat a soldier, and {N} has read them. Hard '
                       'training is one thing; this is something else, and the rules say so.'),
                      ('U',
                       '{N} watches the sergeant for a week and sees the pattern: always {colleague}, always in '
                       'front of everyone, never when an officer is near. A pattern can be written down.'),
                      ('B',
                       'The sergeant writes the reports that go up the chain, and nobody gets on by crossing them. '
                       '{N} wonders what it would cost to be on the wrong side, and what it might be worth to be on '
                       'the right one.'),
                      ('R',
                       'Every time the sergeant starts on {colleague}, {Ns} jaw tightens. It would feel very good to '
                       'say something, loudly, right there on the parade ground.'),
                      ('G',
                       'The platoon was a family before the sergeant came: rude, awkward and close. Now it is '
                       'splitting, and {colleague} eats alone. {N} feels it like weather turning.')],
            'tribal': [('',
                        'The new leader of the watch has been with the guard a moon and has found a target: '
                        '{colleague}, the slowest hunter, given the worst watches and the heaviest loads and mocked '
                        'at the fire every night. Some of the others have started to laugh along.')],
            'magic': [('',
                       'The new sergeant has been with the company a fortnight and has found a target: {colleague}, '
                       'the slowest recruit, given extra drill, the latrines and a nickname shouted across the '
                       'parade ground. Some of the others have started to join in.')]},
 'outcomes': (['Within a month things change the way {N} meant them to, and nobody eats alone any more.',
               'The pressure eases, and at the next test the slowest of them finishes with the others cheering.'],
              ['Nothing changes, and before long {colleague} asks to be sent somewhere else.',
               'Word of it gets back, and the next month is a long one for {N}.']),
 'options': [
    ('report the sergeant through the proper channel, in writing and signed', 'W1', None, 0.45, '', {'mark': 'helped someone in need', 'closed': 'approval: a complaint against a sergeant from the ranks; backfire: the platoon calls it informing, and the sergeant learns who wrote it', 'v': 'conformity, universalism', 'world': {'tribal': 'tell the elders at the fire, plainly, what the leader of the watch is doing', 'magic': 'report the sergeant to the captain through the proper channel, in writing and signed'}, 'chance': 0.6}),
    ('keep a dated note of every incident, until the pattern cannot be denied', 'U1', None, 0.45, '', {'self_control': '+', 'v': 'security, universalism', 'world': {'tribal': 'cut a notch in a stick for every time it happens, until the pattern cannot be denied'}, 'chance': 0.7}),
    ("make yourself the sergeant's right hand, and use it to steer them off the recruit", 'B1', None, 0.45, '', {'aims': 'army officer', 'v': 'power, security', 'world': {'tribal': "make yourself the watch leader's right hand, and use it to steer them off the slow hunter"}, 'chance': 0.65}),
    ('stand between the sergeant and the recruit next time, and say it out loud', 'R1', None, 0.45, '', {'mark': 'defied an authority', 'identity': True, 'v': 'universalism, stimulation', 'world': {'tribal': 'step between the watch leader and the slow hunter next time, and say it out loud', 'magic': 'step between the sergeant and the recruit on parade next time, and say it out loud'}, 'chance': 0.65}),
    ('sit with the recruit at meals, and bring the others back to the table', 'G1', None, 0.45, '', {'grants': 'old comrades', 'identity': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'sit with the slow hunter at the fire, and bring the others back to the circle', 'magic': 'sit with the recruit at mess, and bring the others back to the table'}, 'chance': 0.7}),
    ('set up evening runs for the whole section, so the recruit is never last alone', 'W1', 'G.7', 0.5, '', {'grants': 'leading soldiers', 'habit': True, 'v': 'benevolence, conformity', 'world': {'tribal': 'set up runs at dusk for the whole guard, so the slow hunter is never last alone', 'magic': 'set up evening runs for the whole file, so the recruit is never last alone'}, 'chance': 0.8}),
    ('look up the regulations, and show the platoon commander which ones are broken', 'U1', 'W.7', 0.5, '', {'identity': True, 'v': 'conformity, universalism', 'world': {'tribal': 'remind the elders of the old rule that the guard shames nobody at the fire', 'magic': "look up the articles of the realm's army, and show the captain which are broken"}, 'chance': 0.7}),
    ('buy the old quartermaster a drink, and learn what moves the new sergeant', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'bring the oldest hunter a share of meat, and learn what moves the new watch leader', 'magic': 'buy the old quartermaster a cup, and learn what moves the new sergeant'}, 'chance': 0.75}),
    ('get the platoon to stand together next time, so the sergeant faces all of them', 'R1', 'B.7', 0.5, '', {'binds': True, 'v': 'stimulation, power', 'world': {'tribal': 'get the whole guard to stand together next time, so the watch leader faces all of them', 'magic': 'get the company to stand together next time, so the sergeant faces all of them'}, 'chance': 0.75}),
    ('look away, and laugh along with the others, so you stay one of the platoon', 'G1', 'R.7', 0.5, '', {'mark': 'gave in to pressure', 'closed': 'approval: laughing along while a recruit is picked on; backfire: the recruit leaves the army, and the inquiry asks who saw it and said nothing', 'self_control': '-', 'v': 'hedonism, conformity', 'world': {'tribal': 'look away, and laugh along at the fire, so you stay one of the guard', 'magic': 'look away, and laugh along on parade, so you stay one of the company'}, 'chance': 0.7}),
 ]},
{'name': 'an order you think is wrong',
 'stages': 'young_adult adult mature',
 'age': (20, 62),
 'alpha': 'W.1 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'moment',
 'roles': 'boss, colleague, mentor',
 'requires': 'army officer',
 'worlds': {'earth': "an order from the commanding officer: drive the company's trucks over the mountain pass "
                     'tonight, in fog and ice, so the exercise can start on time at dawn',
            'tribal': 'the elder of the guard orders the hunters across the swollen river tonight, in the dark, so '
                      'they reach the far hills before the herd moves',
            'magic': "an order from the commander of the fort: take the company's wagons over the high pass tonight, "
                     'in fog and ice, so the review can begin at dawn'},
 'timing': {'times': 'per army officer a year: about 1 in 5 is given an order they believe puts their soldiers at '
                     'needless risk, most often to keep to a timetable (estimate); about 6 lives in 1,000 are army '
                     'officers (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The order comes down at six in the evening from {boss}, the commanding officer: the '
                       "company's trucks are to cross the pass tonight, so the exercise can start on time at dawn. "
                       'The forecast says fog and black ice, the drivers have been awake since five, and the old '
                       'road has no barrier on the drop side. {N} reads it twice.'),
                      ('W',
                       'An order is an order, and an army runs because people carry them out. But the rules also say '
                       "an officer answers for the soldiers' safety, and tonight the two pull different ways."),
                      ('U',
                       'There must be a better plan than this one: a later start, a lower road, a convoy at first '
                       'light with the gritter in front. {N} pulls out the map and the timetable.'),
                      ('B',
                       '{boss} writes {Ns} reports. Obeying costs nothing tonight, and refusing could cost a career; '
                       'but if a truck goes over the edge, the name on the movement order will be {Ns}.'),
                      ('R',
                       '{N} thinks of the drivers, red-eyed in the canteen, and feels the anger rise. Nobody who has '
                       'driven that road at night in ice would give this order.'),
                      ('G',
                       '{N} knows every driver by name, and the families of half of them. The exercise will happen '
                       'with or without tonight; each of the drivers has one life.')],
            'tribal': [('',
                        'At dusk the elder of the guard sends word: the hunters are to cross the swollen river '
                        'tonight, in the dark, to reach the far hills before the herd moves. The water is high and '
                        'brown, the hunters have walked since dawn, and {N} leads them.')],
            'magic': [('',
                       "At dusk a rider brings the order from {boss}, the commander of the fort: the company's "
                       'wagons are to cross the high pass tonight, in fog and ice, so the review can begin at dawn. '
                       'The drivers are spent, the road has no wall on the drop side, and {N} leads them.')]},
 'outcomes': (['The night passes without harm, and in the morning nobody has to explain anything they cannot.',
               'The commanders above hear how it was handled, and remember the name.'],
              ['It goes wrong from the first hour, and {N} spends the week answering for it.',
               'The order stands, the night is long and frightening, and {boss} is cool with {N} for months.']),
 'options': [
    ('carry out the order to the letter, with every safety check done twice', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'take the hunters over as the elder ordered, every rope and handhold checked twice', 'magic': 'carry out the order to the letter, every wagon and wheel checked twice'}, 'chance': 0.6}),
    ('work out a later, safer plan that still meets the start, and send it up', 'U1', None, 0.45, '', {'aims': 'general', 'v': 'achievement, security', 'world': {'tribal': 'find a safer crossing upstream that still reaches the far hills in time, and send word', 'magic': 'work out a later, safer road that still meets the dawn, and send it to the fort'}, 'chance': 0.7}),
    ('ask for the order in writing and signed, so the risk sits with whoever gave it', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': 'ask the elder to give the order again before all the hunters, so the risk sits with whoever gave it', 'magic': "ask for the order under the commander's seal, so the risk sits with whoever gave it"}, 'chance': 0.8}),
    ('refuse to send the drivers tonight, and tell the commander why, face to face', 'R1', None, 0.45, '', {'mark': 'defied an authority', 'closed': 'approval: an order refused; backfire: a formal warning on the record, and the commanding officer does not forget it', 'v': 'benevolence, self-direction', 'world': {'tribal': 'refuse to take the hunters into the river tonight, and tell the elder why, face to face', 'magic': 'refuse to send the wagons tonight, and tell the commander why, face to face'}, 'chance': 0.65}),
    ('let the drivers sleep six hours, cross at first light, and take what comes', 'G1', None, 0.45, '', {'identity': True, 'v': 'benevolence, security', 'world': {'tribal': 'let the hunters sleep, cross at first light when the water drops, and take what comes', 'magic': 'let the drivers sleep six hours, cross at first light, and take what comes'}, 'chance': 0.65}),
    ('ring the weather office and the road police, and get the facts on paper first', 'W1', 'U.7', 0.5, '', {'v': 'conformity, security', 'world': {'tribal': 'send the best tracker to read the river and the sky, and bring back the facts first', 'magic': 'send riders to the pass and the weather-wise, and get the facts set down first'}, 'chance': 0.8}),
    ('show the commander a plan that makes the delay look like their own idea', 'U1', 'B.7', 0.5, '', {'v': 'power, achievement', 'world': {'tribal': "show the elder a way that makes waiting look like the elder's own idea", 'magic': "show the commander a plan that makes the delay look like the commander's own idea"}, 'chance': 0.7}),
    ("go above the commander's head to the general staff, and get the order stopped", 'B1', 'R.7', 0.5, '', {'mark': 'made an enemy', 'v': 'power, benevolence', 'world': {'tribal': "go over the elder's head to the leader of all the guard, and get the order stopped", 'magic': "send a rider over the commander's head to the general's tent, and get the order stopped"}, 'chance': 0.6}),
    ('drive the pass alone first in the light truck, to see the road for the others', 'R1', 'G.7', 0.5, '', {'body': 'light', 'mark': 'took a wild risk', 'v': 'benevolence, stimulation', 'world': {'tribal': 'wade the river alone first on a rope, to find the footing for the others', 'magic': 'ride the pass alone first, to see the road for the others'}, 'chance': 0.75}),
    ('gather the drivers, and agree a rule together: nobody drives who has not slept', 'G1', 'W.7', 0.5, '', {'grants': 'leading soldiers', 'v': 'benevolence, conformity', 'world': {'tribal': 'gather the hunters, and agree together that nobody crosses who has not slept', 'magic': 'gather the drivers, and agree together that nobody drives who has not slept'}, 'chance': 0.75}),
 ]},
{'name': 'the unit comes home one short',
 'stages': 'young_adult adult mature',
 'age': (20, 62),
 'alpha': 'W.4 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, friends, meaning',
 'horizon': 'months',
 'roles': 'boss, colleague, mentor, friend',
 'requires': 'army officer',
 'worlds': {'earth': 'the unit is home from a deployment far away, one soldier short: a truck left a mountain road '
                     'in the last week, and a family is waiting for answers',
            'tribal': 'the guard is back from the long journey to the far hills, one hunter short: the river took '
                      'one of them at a crossing, and a hearth is waiting for someone to come and speak',
            'magic': 'the company is back from the long garrison in the north, one soldier short: a supply wagon '
                     'went off a mountain road, and a family in the town is waiting for word'},
 'timing': {'times': 'per army officer a year: about 1 in 25 loses a soldier of their own unit to an accident, an '
                     'illness or an operation abroad (estimate); in peacetime, road and training accidents are among '
                     'the commonest causes of death in armies (armed forces mortality reports); about 6 lives in '
                     '1,000 are army officers (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The unit came home on Tuesday to the families on the parade ground, one short. In the last '
                       'week of the deployment a truck left a mountain road at night, and one of the drivers did not '
                       'come home; the funeral was last week. Now the unit is on leave, the inquiry has begun, and '
                       "the driver's family has asked to see the officer who led them."),
                      ('W',
                       '{N} signed the movement orders for that convoy. There is a duty to the family, a duty to the '
                       'inquiry and a duty to the unit, and {N} means to keep all three.'),
                      ('U',
                       'The report says the truck left the road in darkness. {N} wants to know why: the road, the '
                       'truck, the hours the driver had worked, and the order that put them out there at night.'),
                      ('B',
                       'Inquiries look for someone to blame, and {N} knows how these things go: the name on the '
                       'order is usually the one that stays. {N} also knows who in the chain could make it go '
                       'another way.'),
                      ('R',
                       "{N} keeps seeing the driver's grin at the last roll call, and cannot sit still with it. The "
                       'grief comes out as anger: at the road, at the army, at {N}.'),
                      ('G',
                       'The unit is scattered on leave, each of them carrying it home alone. {N} thinks of the '
                       "driver's mother, of the soldiers who shared that truck, and of how a unit either holds "
                       'together after a loss or comes apart.')],
            'tribal': [('',
                        'The guard came back from the far hills one short: at a river crossing the water took one of '
                        "the hunters, and the others could not reach him. The band has mourned, and now the hunter's "
                        'mother has asked to see the one who led them.')],
            'magic': [('',
                       'The company came back from the long garrison in the north one short: a supply wagon went off '
                       'a mountain road at night, and its driver did not come home. The town has buried the driver, '
                       'and the family has asked to see the captain who led them.')]},
 'outcomes': (['They hold together, and the family knows the one they lost is not forgotten.',
               'A year on, the answers are clear, and the loss has changed something for the better.'],
              ['They scatter, and nobody quite talks about it again.',
               "The family's grief turns to anger, and much of it falls on {N}."]),
 'options': [
    ('visit the family, answer every question honestly, and keep in touch', 'W1', None, 0.45, '', {'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': "go to the hunter's hearth, answer every question honestly, and come back every moon", 'magic': "ride to the family's house, answer every question honestly, and keep writing"}, 'chance': 0.75}),
    ('push the inquiry for the true cause: the road, the truck, the hours worked', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'world': {'tribal': 'walk the crossing again, and find out truly why the water took the hunter', 'magic': 'press the inquiry for the true cause: the road, the wagon, the hours driven'}, 'chance': 0.6}),
    ('brief the general staff before the inquiry does, and shape what they hear first', 'B1', None, 0.45, '', {'aims': 'general', 'v': 'power, security', 'world': {'tribal': 'speak to the leader of all the guard before the elders meet, and shape what they hear first', 'magic': "ride to the general's staff before the inquiry sits, and shape what they hear first"}, 'chance': 0.7}),
    ('speak at the memorial from the heart, without notes', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'speak at the mourning fire from the heart', 'magic': 'speak at the burying from the heart, without notes'}, 'chance': 0.7}),
    ('ring every soldier on leave, and bring the unit back together at one table', 'G1', None, 0.45, '', {'grants': 'old comrades', 'v': 'benevolence, tradition', 'world': {'tribal': "go to every hunter's hearth, and bring the guard back together at one fire", 'magic': 'visit every soldier on leave, and bring the company back together at one table'}, 'chance': 0.65}),
    ('give the inquiry every order, log and timing, including your own mistakes', 'W1', 'U.7', 0.5, '', {'mark': 'owned up', 'identity': True, 'v': 'universalism, conformity', 'world': {'tribal': 'tell the elders every word and step of the crossing, your own mistakes too', 'magic': 'give the inquiry every order, log and hour, your own mistakes too'}, 'chance': 0.65}),
    ('work out what the inquiry will ask, and have every answer ready', 'U1', 'B.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'work out what the elders will ask, and have every answer ready'}, 'chance': 0.8}),
    ("call in favours to fund a race every year in the driver's name", 'B1', 'R.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': "call in what the bands owe, for a feast every year in the hunter's name", 'magic': "call in favours for a tournament every year in the driver's name"}, 'chance': 0.7}),
    ('take the soldiers who shared the truck away to the hills, and let them talk', 'R1', 'G.7', 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'take the hunters who were at the crossing up into the hills, and let them talk', 'magic': 'take the soldiers who rode with the wagon away to the hills, and let them talk'}, 'chance': 0.7}),
    ("keep the old custom: an empty place at the unit's table, every year", 'G1', 'W.7', 0.5, '', {'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': "keep the old custom: an empty place at the guard's fire, every year", 'magic': "keep the old custom: an empty place at the company's table, every year"}, 'chance': 0.75}),
 ]},
{'name': 'officer selection',
 'stages': 'young_adult adult',
 'age': (20, 40),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'rite': 'young_adult',
 'per_year': (0.0, 0.0, 0.08, 0.04, 0.0, 0.0),
 'drivers': 'era+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, school',
 'horizon': 'months',
 'roles': 'mentor, boss, parent, colleague, rival',
 'requires': 'soldier | graduate | national service done',
 'worlds': {'earth': 'the officer selection board: three days of tests, interviews and a muddy field, and a place at '
                     'the academy for about one candidate in three',
            'tribal': 'the elders of the guard test who may lead the hunters: three days of tracking, carrying, a '
                      'river crossing and speaking at the fire',
            'magic': "the realm's captains hold their selection at the old fort: three days of trials, questions and "
                     "a muddy field, for a place at the officers' school"},
 'timing': {'times': 'per soldier of two years, graduate or one who has done national service, aged 20 to 40, a '
                     'year: about 1 in 12 in the twenties and fewer later goes before an officer selection board '
                     '(estimate); about 1 member in 6 of an active army is an officer (US Department of Defense '
                     'figures in the catalogue), and selection boards pass about 1 candidate in 3 (estimate); about '
                     '6 lives in 1,000 become army officers (catalogue share)',
            'likelier': 'a sergeant who pushes, a degree and a fit body, years when the army is growing and short of '
                        'young officers',
            'rarer': 'a record with the police, poor health, a family that wants a safer life, a year of cuts to the '
                     'army',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The letter says three days at the selection board: written tests, an interview before a '
                       'panel of senior officers, a talk to give, and a field of mud with a plank, two oil drums and '
                       'a team of strangers who must all be got across. About one candidate in three is offered a '
                       'place at the academy. {mentor} has said for years that {N} should go.'),
                      ('W',
                       "{N} has read the board's handbook until the pages are soft: the qualities it looks for, the "
                       'dress for each day, the order of the tests. To lead soldiers is a duty before it is a rank.'),
                      ('U',
                       'The command tasks are puzzles with planks and drums and a clock running. {N} has been '
                       'practising them on the kitchen table with matchsticks and a ruler.'),
                      ('B',
                       'The board is the first gate on a long road, and {N} has looked up where the officers of '
                       'other years ended up: some of them sit on the general staff now.'),
                      ('R',
                       '{N} just wants to get into the mud and lead. The written tests feel like a fence to climb on '
                       'the way to the real thing.'),
                      ('G',
                       'Nobody in {Ns} family has been an officer. {parent} says the old soldiers of the town will '
                       'be proud, and {N} wonders what it means to rise above the people {N} came up with.')],
            'tribal': [('',
                        'The elders of the guard will choose new leaders of the hunters this season. For three days '
                        'the young hunters track, carry, take a party across the river and speak at the fire, and '
                        'the elders watch every one of them.')],
            'magic': [('',
                       "The realm's captains hold their selection at the old fort every spring: three days of "
                       'trials, questions before a panel of captains, and a field of mud where a team of strangers '
                       "must be got over a ditch with two barrels and a plank. A captain's commission waits for "
                       'perhaps one in three.')]},
 'outcomes': (['Word comes that {N} has been chosen, and a season later {N} stands in front of others as the one who '
               'leads them.',
               'Whatever {N} chose, the road ahead is clearer for it, and a year later {N} is glad of the choice.'],
              ['The answer is short and polite: not this time, perhaps in a year or two.',
               'The last day goes badly, a task falls apart in front of the panel, and the journey home is very '
               'long.']),
 'options': [
    ("prepare by the board's own handbook, and answer every question as an officer should", 'W1', None, 0.45, '', {'title': 'army officer', 'grants': "an officer's commission", 'v': 'conformity, achievement', 'world': {'tribal': 'learn the old rules of the guard by heart, and answer the elders as a leader should', 'magic': "learn the captains' articles by heart, and answer the panel as an officer should"}, 'chance': 0.35}),
    ('practise the command tasks for months, and solve the planks and drums cleanly', 'U1', None, 0.45, '', {'title': 'army officer', 'grants': "an officer's commission", 'mark': 'learned a skill', 'habit': True, 'v': 'achievement, self-direction', 'world': {'tribal': "practise the elders' trials for a season, and take the party over the river cleanly", 'magic': 'practise the trials for months, and solve the barrels and the plank cleanly'}, 'chance': 0.35}),
    ('tell the panel plainly that you mean to be a general one day', 'B1', None, 0.45, '', {'title': 'army officer', 'grants': "an officer's commission", 'aims': 'general', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'tell the elders plainly that you mean to be war leader of the clans one day', 'magic': 'tell the panel plainly that you mean to be a general of the realm one day'}, 'chance': 0.35}),
    ('throw yourself into the mud tasks, and lead from the front every time', 'R1', None, 0.45, '', {'title': 'army officer', 'grants': "an officer's commission", 'body': 'heavy', 'v': 'stimulation, achievement', 'world': {'tribal': 'throw yourself into every trial, and lead from the front every time'}, 'chance': 0.35}),
    ('speak at interview of the people you came up with, and what they taught', 'G1', None, 0.45, '', {'title': 'army officer', 'grants': "an officer's commission", 'v': 'benevolence, tradition', 'world': {'tribal': 'speak at the fire of the hunters you grew up beside, and what they taught', 'magic': 'speak before the panel of the people you came up with, and what they taught'}, 'chance': 0.35}),
    ('take the slower road through the ranks, and earn the stripes one by one', 'B.5 G.5', None, 0.5, '', {'grants': 'rank', 'self_control': '+', 'v': 'achievement, tradition', 'world': {'tribal': "stay a hunter of the guard, and earn the elders' trust one winter at a time", 'magic': 'take the slower road through the ranks, and earn the stripes one by one'}, 'chance': 0.75}),
    ('turn it down for now, and stay close to the friends you have', 'R.5 G.5', None, 0.5, '', {'mark': 'turned down a chance', 'self_control': '-', 'v': 'benevolence, hedonism', 'world': {'tribal': 'turn it down for now, and stay close to the hunters you run with'}, 'chance': 0.75}),
    ('go on the mountain leader course first, and apply again next year', 'U.5 R.5', None, 0.5, '', {'grants': 'navigation', 'door': True, 'v': 'achievement, stimulation', 'world': {'tribal': 'go into the high hills alone for a season first, and come back to the trials after', 'magic': 'walk the high passes with the mountain guides first, and come back to the trials next spring'}, 'chance': 0.75}),
    ('ask an old officer of the town to put a name to the application', 'W.5 B.5', None, 0.5, '', {'door': True, 'v': 'conformity, power', 'world': {'tribal': "ask the oldest leader of the guard to speak for the asking at the elders' fire", 'magic': 'ask an old captain of the town to set a seal on the application'}, 'chance': 0.75}),
    ('sit the practice papers until every score is safe, and go next year', 'W.5 U.5', None, 0.5, '', {'self_control': '+', 'v': 'achievement, conformity', 'world': {'tribal': "practise the elders' trials with the old hunters until they are sure, and go next season", 'magic': 'sit the practice papers until every score is safe, and go next spring'}, 'chance': 0.75}),
 ]},
{'name': 'the army needs a new general',
 'stages': 'adult mature',
 'age': (40, 62),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.04, 0.0),
 'drivers': 'era+.2 fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, publiclife',
 'horizon': 'months',
 'roles': 'boss, rival, mentor, colleague, partner',
 'requires': 'army officer',
 'tenure': (12.0, 100.0),
 'worlds': {'earth': 'a general retires, and the selection panel of the general staff will choose a successor from a '
                     'short list of senior officers',
            'tribal': 'the old war leader of the clans can no longer walk the hills, and asks the leaders of the '
                      'guard which of them will carry the spear after',
            'magic': 'a general of the realm has retired to the country, and the council of war will name a new one '
                     "from among the realm's captains"},
 'timing': {'times': 'per army officer of twelve years or more a year: about 1 in 30 is in the running when a '
                     "general's post falls free (estimate); armies have under 1 general for every 1,000 soldiers on "
                     'active duty (US Department of Defense figures in the catalogue), and most officers leave the '
                     'army long before; about 3 lives in 100,000 become generals (catalogue share)',
            'likelier': 'a command that went well, a mention in dispatches or an award, years when the army is '
                        'changing and needs new leaders, a patron on the general staff',
            'rarer': 'a quarrel with the government, an inquiry on the record, a shrinking army with fewer posts, a '
                     'career spent far from the capital',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'A general is retiring in the spring, and the selection panel of the general staff will '
                       'choose a successor from a short list. {Ns} name is on it after twenty years of postings, and '
                       "so is {rival}'s, an officer with a famous family and friends in the government. One post, "
                       'perhaps six names, and a panel that meets behind closed doors.'),
                      ('W',
                       '{N} has served twenty years by the rules: every report clean, every order carried out or '
                       'lawfully questioned. If that is not enough for the panel, then the rules mean less than {N} '
                       'thought.'),
                      ('U',
                       "For years {N} has been writing, privately, about what the army will need in twenty years' "
                       'time. The panel will ask, and for once the answer is ready.'),
                      ('B',
                       'Six names and one post. {N} knows which members of the panel owe {rival} favours, which ones '
                       'dine with ministers, and which ones have not yet made up their minds.'),
                      ('R',
                       '{N} has led from the front for twenty years, and the soldiers know it. The panel can read '
                       'the record; {N} would rather stand in front of them and say what the army needs.'),
                      ('G',
                       '{N} has watched two generations of soldiers come up through the ranks, and some of them lead '
                       'units of their own now. If the post comes, it comes; the army will need its old hands '
                       'whoever is chosen.')],
            'tribal': [('',
                        'The old war leader of the clans can no longer walk the hills, and at the autumn gathering '
                        'will hand the spear to one of the leaders of the guard. {N} has led the hunters for many '
                        'winters, and so has {rival}, whose father carried the spear before.')],
            'magic': [('',
                       'A general of the realm has retired to the country, and the council of war will name a new '
                       'one before the spring muster. {Ns} name is among the captains spoken of, and so is '
                       "{rival}'s, a captain of a great house with friends at court.")]},
 'outcomes': (['The choice falls on {N}, and by the next winter the whole army knows the name.',
               'Whatever {N} chose, the years ahead have a shape, and {N} is at peace with it.'],
              ['The post goes to {rival}, and {N} hears it the same day as everyone else.',
               'The panel takes a year to choose, and by then {Ns} name has quietly fallen off the list.']),
 'options': [
    ('put the name forward by the book, with twenty years of clean reports behind it', 'W1', None, 0.45, '', {'title': 'general', 'v': 'conformity, achievement', 'world': {'tribal': 'ask the old war leader for the spear by the old custom, with many winters of the guard behind the asking', 'magic': 'put the name before the council of war by the articles, with twenty years of clean reports'}, 'chance': 0.06}),
    ('send the panel a paper on what the army will need in twenty years', 'U1', None, 0.45, '', {'title': 'general', 'identity': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'tell the old war leader how the clans should keep the passes in the winters to come', 'magic': "send the council of war a treatise on what the realm's army will need"}, 'chance': 0.06}),
    ("lobby the minister's office and the old generals, one dinner at a time", 'B1', None, 0.45, '', {'title': 'general', 'aims': 'general', 'closed': "approval: lobbying the government over the army's head; backfire: the panel hears of it, and some of its members never forgive it", 'habit': True, 'v': 'power, achievement', 'world': {'tribal': 'win over the chiefs of the great clans, one feast at a time', 'magic': 'win over the lords of the council, one supper at a time'}, 'chance': 0.06}),
    ('tell the panel plainly what is wrong with the army, and how to fix it', 'R1', None, 0.45, '', {'title': 'general', 'identity': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'tell the old war leader plainly what is wrong with the guard, and how to fix it', 'magic': "tell the council of war plainly what is wrong with the realm's army, and how to fix it"}, 'chance': 0.06}),
    ('let the soldiers of twenty years speak up, and wait to be asked', 'G1', None, 0.45, '', {'title': 'general', 'v': 'tradition, benevolence', 'world': {'tribal': 'let the hunters of many winters speak up at the gathering, and wait to be asked'}, 'chance': 0.06}),
    ("take command of the officers' academy instead, and remake it your own way", 'B.5 R.5', None, 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': 'take the training of the young hunters instead, and make it your own', 'magic': "take the captaincy of the officers' school instead, and remake it your own way"}, 'chance': 0.74}),
    ("back a rival's bid, in return for the command you really want", 'U.5 B.5', None, 0.5, '', {'binds': True, 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'back another leader for the spear, in return for the guard of the far camps', 'magic': "back a rival captain's bid, in return for the command you really want"}, 'chance': 0.74}),
    ('take on a young officer to teach, and stay with the unit you know', 'U.5 G.5', None, 0.5, '', {'grants': "apprentice of one's own", 'v': 'benevolence, achievement', 'world': {'tribal': 'take a young hunter of the guard to teach, and stay with your own band', 'magic': 'take on a young captain to teach, and stay with the company you know'}, 'chance': 0.74}),
    ('step aside for a better officer, and serve them as well as the last', 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'step aside for a better leader, and serve the new war leader as well as the old'}, 'chance': 0.74}),
    ('take the far posting nobody wants, and serve where the army needs it most', 'W.5 R.5', None, 0.5, '', {'binds': True, 'self_control': '+', 'v': 'benevolence, conformity', 'world': {'tribal': 'take the guard of the far camps nobody wants, where the clans need it most', 'magic': 'take the frontier fort nobody wants, where the realm needs it most'}, 'chance': 0.74}),
 ]},
{'name': 'the report on the night that went wrong',
 'stages': 'young_adult adult mature',
 'age': (18, 65),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.01, 0.0),
 'drivers': 'harsh+.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, friends',
 'horizon': 'months',
 'roles': 'friend, colleague, boss, mentor',
 'requires': 'army officer | soldier | general',
 'worlds': {'earth': "on an exercise a friend's mistake turned a truck over, a soldier was hurt, and the report is "
                     'due on Friday with a signature on it',
            'tribal': "on the long hunt a friend's hurry overturned the raft at a crossing, a hunter of the guard "
                      'was hurt, and the elders want to hear how it happened',
            'magic': "on manoeuvres a friend's mistake turned a supply wagon over, a soldier was hurt, and the "
                     'captain wants the report by the end of the week'},
 'timing': {'times': 'per soldier, officer or general a year: about 1 in 80 has to write or sign a report on an '
                     "accident in which a friend's mistake hurt someone (estimate); armies look into thousands of "
                     'training and vehicle accidents a year, and incomplete or shaded accident reports are a common '
                     'finding of the inquiries that follow (estimate); about 5 lives in 100 serve as soldiers '
                     '(catalogue share)',
            'likelier': 'a tired unit at the end of a long exercise, old vehicles, a friend at the wheel, a unit '
                        'where mistakes are punished hard',
            'rarer': 'a unit with good drills and rested drivers, a name known for writing it straight',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'On the last night of the exercise {friend}, tired and driving too fast on a forest track, '
                       'turned a truck onto its side. A soldier in the back was hurt: a broken arm and a night in '
                       'hospital, mending now. Nobody else saw the speed but {N}, and the report is due on Friday '
                       'with {Ns} signature on it. {friend} has asked, quietly, for the road to be blamed.'),
                      ('W',
                       'A report is a promise that what it says is true. {N} has signed hundreds, and never one with '
                       'a word in it that was not so.'),
                      ('U',
                       '{N} has been over it a dozen times: the speed, the bend, the hours {friend} had been '
                       'driving, the drill that let a tired driver take the wheel. The truth is more interesting '
                       'than the blame.'),
                      ('B',
                       'An inquiry will read the report, and an inquiry wants a name. {N} weighs whose name it will '
                       'be, what each version costs, and who will owe what afterwards.'),
                      ('R',
                       '{friend} has been {Ns} friend since the first week of training. Putting that name in a '
                       'report feels like a betrayal, and so does lying for it.'),
                      ('G',
                       'The hurt soldier is mending, {friend} is sick with guilt, and the unit is holding its '
                       'breath. {N} thinks about what the unit needs to come through this whole.')],
            'tribal': [('',
                        'On the long hunt {friend}, tired and in a hurry, overturned the raft at the crossing, and a '
                        'hunter of the guard was hurt: a broken arm, mending now. Nobody else saw how it happened '
                        'but {N}, and the elders want to hear it at the fire. {friend} has asked, quietly, for the '
                        'river to be blamed.')],
            'magic': [('',
                       'On the last night of manoeuvres {friend}, tired and driving the team too hard on a forest '
                       'road, turned a supply wagon over. A soldier riding on it was hurt: a broken arm, mending '
                       'now. Nobody else saw but {N}, and the captain wants the report by the end of the week. '
                       '{friend} has asked, quietly, for the road to be blamed.')]},
 'outcomes': (['The matter is closed, the arm mends, and {N} can look everyone in the unit in the eye.',
               'A year on, the night is a story told to the newcomers, and things are done better because of it.'],
              ['The questions drag on for months, and the unit splits over who said what.',
               'It ends badly for {friend} anyway, and the friendship with it.']),
 'options': [
    ('write the report true, every fact as it happened, and sign it', 'W1', None, 0.45, '', {'self_control': '+', 'v': 'conformity, universalism', 'world': {'tribal': 'tell the elders the truth at the fire, every step as it happened', 'magic': 'write the report true, every fact as it happened, and set your seal on it'}, 'chance': 0.71}),
    ('write the cause as a fault in the old truck, and leave the speed out', 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'law: a report falsified; backfire: the inquiry tests the truck, finds nothing wrong with it, and takes the rank of whoever signed', 'takes_if_fails': 'rank', 'self_control': '-', 'v': 'benevolence, security', 'world': {'tribal': "tell the elders the raft's lashings failed, and leave the hurry out", 'magic': 'write the cause as a cracked axle, and leave the speed out'}, 'chance': 0.63}),
    ('write it straight, and make sure it shows who got the hurt soldier out', 'B1', None, 0.45, '', {'grants': 'mentioned in dispatches', 'v': 'achievement, power', 'world': {'tribal': 'tell it straight at the fire, and make sure the elders hear who carried the hurt hunter out', 'magic': 'write it straight, and make sure it shows who pulled the hurt soldier clear'}, 'chance': 0.67}),
    ('tell the friend to own up first, and stand beside them when they do', 'R1', None, 0.45, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'chance': 0.7}),
    ('visit the hurt soldier every week until they are back on their feet', 'G1', None, 0.45, '', {'v': 'benevolence', 'world': {'tribal': 'sit with the hurt hunter every day until the arm is mended', 'magic': "visit the hurt soldier at the healers' house every week until the arm mends"}, 'chance': 0.64}),
    ('rewrite the drill so no driver that tired ever takes the wheel again', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, conformity', 'world': {'tribal': 'set a new rule for the guard, so nobody that tired ever takes the raft across again', 'magic': 'rewrite the standing orders, so no driver that tired ever takes the reins again'}, 'chance': 0.75}),
    ('take a share of the blame, for not stopping a tired friend from driving', 'W.34 R.33 G.33', None, 0.5, '', {'mark': 'owned up', 'v': 'benevolence, conformity', 'world': {'tribal': 'take a share of the blame, for not stopping a tired friend at the crossing'}, 'chance': 0.72}),
    ('write it true, and argue in it for the friend to be retrained, not punished', 'W.34 B.33 R.33', None, 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'tell it true at the fire, and ask the elders to teach the friend again, not cast them out', 'magic': 'write it true, and argue for the friend to be retrained, not broken'}, 'chance': 0.66}),
    ('go with the friend to the doctor about the sleepless nights first', 'U.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, self-direction', 'world': {'tribal': 'take the friend to the healer about the sleepless nights first', 'magic': "go with the friend to the healers' house about the sleepless nights first"}, 'chance': 0.78}),
    ('ask the hurt soldier quietly what they want said, before writing a word', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'benevolence, security', 'world': {'tribal': 'ask the hurt hunter quietly what they want told, before the fire'}, 'chance': 0.84}),
 ]},
{'name': 'the field commission',
 'stages': 'young_adult adult mature',
 'age': (20, 45),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.005, 0.0),
 'drivers': 'fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, community',
 'horizon': 'week',
 'roles': 'boss, friend, colleague, mentor',
 'requires': 'soldier',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'the river floods a town, the army is sent in, and a general saw who held the footbridge all '
                     'night; now the general asks to meet that soldier',
            'tribal': 'the river floods the lower camp, the guard is sent down, and the war leader of the clans saw '
                      'who held the crossing all night',
            'magic': 'the river bursts its banks in a market town of the realm, the soldiers are sent in, and a '
                     'general riding through saw who held the bridge all night'},
 'timing': {'times': 'per soldier of three years or more a year: about 1 in 100 is sent with the army to a flood, a '
                     'fire or a storm and does something there that a general sees (estimate); armies are called out '
                     "to help after floods and fires in most years, and a commission from the ranks for one night's "
                     'work is rare, a handful in a generation (estimate); about 6 lives in 1,000 become army '
                     'officers (catalogue share)',
            'likelier': 'a wet winter or a dry summer, a unit sent to help, a general who visits the line, years of '
                        'good reports behind it',
            'rarer': 'a quiet year, a posting far from any town, a general who never leaves headquarters',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'The river came up through the lower town in the night, and the army was sent in. {N} spent '
                       'eleven hours at the old footbridge with a rope and a torch, bringing people over one at a '
                       "time: the old man from the chemist's, the woman with the dog, everyone from the terrace by "
                       'the mill. Nobody was lost. A general who had come to see the flood stopped and watched, and '
                       'now a staff car has come to the hall where the section is sleeping, asking for {N} by name.'),
                      ('W',
                       '{N} only did what the drill and the orders said: hold the crossing, count everyone over, '
                       "leave nobody behind. It is strange to be thanked for doing one's duty."),
                      ('U',
                       'All night {N} kept working out the river: where it was rising, where the rope would hold, '
                       'how long before the footbridge went. It held because the sums were right.'),
                      ('B',
                       'A general does not send a car for an ordinary soldier every day. {N} knows a door like this '
                       'opens once, and thinks fast about what to ask for.'),
                      ('R',
                       '{N} has not slept, is still wet to the waist, and has never felt so alive. The night was the '
                       'best and hardest thing {N} has ever done.'),
                      ('G',
                       'The people from the terrace keep coming to the hall with tea and dry socks. The town will '
                       'remember the night for fifty years, and {N} would rather stay and help it dry out than go '
                       'anywhere.')],
            'tribal': [('',
                        'The river rose into the lower camp in the night, and the guard was sent down. {N} held the '
                        'crossing all night with a rope and a torch, bringing the old people of the camp over one by '
                        'one, and nobody was lost. In the morning the war leader of the clans, who had come down to '
                        'see the flood, asked who held the crossing, and has sent for {N}.')],
            'magic': [('',
                       'The river burst its banks in the market town, and the soldiers were sent in. {N} held the '
                       'old bridge all night with a rope and a lantern, bringing the townsfolk over one by one, and '
                       'nobody was lost. A general of the realm riding through saw it, and in the morning a '
                       'messenger comes asking for {N} by name.')]},
 'outcomes': (['Within a season the answer comes, and from then on {N} leads where {N} once followed.',
               'Whatever {N} chose, the night by the river turns out to be the start of something, not the whole of '
               'it.'],
              ['The general goes home, and nothing more is heard.',
               'The thanks fade with the floodwater, and {N} is back on guard duty the next week with a story nobody '
               'quite believes.']),
 'options': [
    ('ask the general, through the proper channel, to be considered for a commission', 'W1', None, 0.45, '', {'title': 'army officer', 'grants_if_fails': 'a long shot that missed', 'v': 'conformity, achievement', 'world': {'tribal': 'ask the war leader, by the old custom, for leave to lead the guard', 'magic': "ask the general, through the proper channel, to be considered for a captain's commission"}, 'chance': 0.03}),
    ('give the general your plan for holding the crossing, and ask to train as an officer', 'U1', None, 0.45, '', {'title': 'army officer', 'grants_if_fails': 'a long shot that missed', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'show the war leader how the crossing was held, and ask to learn to lead', 'magic': 'set out for the general how the bridge was held, and ask to train as an officer'}, 'chance': 0.03}),
    ('ask the general straight out for a commission, while the papers are still running the story', 'B1', None, 0.45, '', {'title': 'army officer', 'grants_if_fails': 'a long shot that missed', 'aims': 'army officer', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'ask the war leader straight out for the leading of the guard, while the camps still talk of it', 'magic': 'ask the general straight out for a commission, while the town still sings of it'}, 'chance': 0.03}),
    ('volunteer for the next flood and the next, until the army cannot ignore it', 'R1', None, 0.45, '', {'title': 'army officer', 'grants_if_fails': 'a long shot that missed', 'mark': 'took a wild risk', 'body': 'heavy', 'self_control': '+', 'v': 'stimulation, benevolence', 'world': {'tribal': 'go down to every flood and fire after, until the clans cannot ignore it', 'magic': 'ride to every flood and fire after, until the realm cannot ignore it'}, 'chance': 0.03}),
    ('stay on to help the town dry out, and let the general hear of it', 'G1', None, 0.45, '', {'title': 'army officer', 'grants_if_fails': 'a long shot that missed', 'mark': 'helped someone in need', 'door': True, 'v': 'benevolence, tradition', 'world': {'tribal': 'stay on to help the lower camp rebuild, and let the war leader hear of it'}, 'chance': 0.03}),
    ("go before the selection board next spring, the usual way, with the general's letter", 'W.34 U.33 R.33', None, 0.5, '', {'aims': 'army officer', 'door': True, 'v': 'achievement, conformity', 'world': {'tribal': "go to the elders' trials next season, as the custom is, with the war leader's word", 'magic': "go before the captains' selection next spring, the usual way, with the general's letter"}, 'chance': 0.84}),
    ('give the credit to the whole section, and ask for nothing more', 'W.34 R.33 G.33', None, 0.5, '', {'grants': 'old comrades', 'mark': 'turned down a chance', 'v': 'benevolence, universalism', 'world': {'tribal': 'give the honour to all the hunters who held the rope, and ask for nothing more', 'magic': 'give the credit to the whole file, and ask for nothing more'}, 'chance': 0.84}),
    ("take the sergeant's stripes the general offers, and stay with the section", 'W.34 B.33 G.33', None, 0.5, '', {'grants': 'rank', 'binds': True, 'v': 'security, tradition', 'world': {'tribal': 'take the place of first hunter of the guard the war leader offers, and stay with the band', 'magic': "take the sergeant's stripes the general offers, and stay with the company"}, 'chance': 0.84}),
    ("make sure the general's report carries your name, and use it for the next step", 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'mentioned in dispatches', 'door': True, 'v': 'achievement, power', 'world': {'tribal': 'make sure the war leader speaks your name at the fire, and use it for the next step'}, 'chance': 0.84}),
    ("join the army's flood rescue team, and write the drill it still uses", 'U.34 B.33 G.33', None, 0.5, '', {'binds': True, 'v': 'achievement, security', 'world': {'tribal': 'become the one the camps send for at every flood, and teach the young hunters how', 'magic': 'join the river wardens, and write the drill they still use'}, 'chance': 0.84}),
 ]},
{'name': 'the war leader is chosen at the gathering',
 'stages': 'adult mature elder',
 'age': (25, 80),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': '',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'elder, rival, mentor, friend',
 'requires': 'army officer | soldier',
 'tenure': (3.0, 99.0),
 'worlds': {'tribal': 'the clans gather at the autumn camp to choose who will lead them if raiders come, and the '
                      'elders of every band will speak'},
 'only': 'tribal',
 'timing': {'times': 'per leader of the hunters and the guard of six winters, or hunter of the guard of twelve, in '
                     'the tribal world, a year: about 1 in 50 is at a gathering where the clans choose a war leader '
                     'against raiders (estimate); bands of hunters and gatherers chose a war leader only when a '
                     'threat was near, for a season, and most of the time had none (ethnographies of band societies; '
                     'estimate)',
            'likelier': 'word of raiders in the far valleys, a hard winter that brings strangers near, an old war '
                        'leader gone',
            'rarer': 'long years of peace between the clans, a gathering that breaks up in a quarrel',
            'gap_years': (5.0, 12.0)},
 'scenes': {'tribal': [('',
                        'The clans have gathered at the autumn camp by the great river, and word has come of '
                        'strangers raiding in the far valleys. Before the bands go to their winter places the elders '
                        'will choose who leads them all if the raiders come this way: a war leader for the winter, '
                        'and leaders for the guard of each band. {N} has walked with the guard for many winters, and '
                        "the elders' eyes keep coming back to {N}."),
                       ('W',
                        'There is an old law for the choosing: the elders speak in turn, the oath is sworn at the '
                        'fire, and the one chosen answers to all the clans. {N} means to keep it.'),
                       ('U',
                        '{N} has walked every pass into the valley and knows where the clans could watch for '
                        'strangers and where the signal fires would carry. A war leader should know such things '
                        'before anything else.'),
                       ('B',
                        'The biggest clans will decide it, whatever the elders say. {N} knows which chiefs listen to '
                        'whom, and what each of them wants from the winter.'),
                       ('R',
                        'The whole camp is restless with the news, and {N} feels it too: the wish to stand up and be '
                        'the one who leads, now, before the moment goes.'),
                       ('G',
                        "The clans have met at this bend of the river since before anyone's grandmother's "
                        'grandmother. Raiders have come and gone, and the river and the clans are still here. '
                        'Whoever leads, {N} thinks, should remember that.')]},
 'outcomes': (['The clans choose, the winter passes without raiders, and {N} walks the camp with a new place in it.',
               'Whatever {N} chose, the gathering ends at peace, and the bands go to their winter places trusting '
               'the choice.'],
              ["The elders choose {rival}, and {N} carries {rival}'s word to the far camps all winter.",
               'The gathering breaks up in a quarrel, and every band goes home with its own plan.']),
 'options': [
    ("stand before the clans by the old law, and swear the war leader's oath", 'W1', None, 0.45, '', {'title': 'general', 'requires': 'army officer', 'without': 'impossible', 'identity': True, 'v': 'conformity, tradition', 'chance': 0.06}),
    ('show the gathering how the clans would hold the passes if raiders came', 'U1', None, 0.45, '', {'title': 'general', 'requires': 'army officer', 'without': 'impossible', 'v': 'achievement, security', 'chance': 0.06}),
    ('win the chiefs of the biggest clans to your side before the gathering opens', 'B1', None, 0.45, '', {'title': 'general', 'requires': 'army officer', 'without': 'impossible', 'aims': 'general', 'v': 'power, achievement', 'chance': 0.06}),
    ('stand up at the fire, and say plainly that you will lead them, and why', 'R1', None, 0.45, '', {'title': 'general', 'requires': 'army officer', 'without': 'impossible', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'chance': 0.06}),
    ('let the hunters of your guard speak your name at the fire, and wait', 'G1', None, 0.45, '', {'title': 'general', 'requires': 'army officer', 'without': 'impossible', 'v': 'tradition, benevolence', 'chance': 0.06}),
    ('ask the elders by the old custom for a party of the guard to lead', 'W1', 'B.7', 0.5, '', {'title': 'army officer', 'requires': 'soldier', 'without': 'impossible', 'aims': 'army officer', 'v': 'conformity, power', 'chance': 0.35}),
    ('work out a scouting run over the far passes, and ask to lead it', 'U1', 'R.7', 0.5, '', {'title': 'army officer', 'requires': 'soldier', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'self-direction, stimulation', 'chance': 0.35}),
    ('win the young hunters of your band over, and ask to lead them as its guard', 'B1', 'G.7', 0.5, '', {'title': 'army officer', 'requires': 'soldier', 'without': 'impossible', 'v': 'power, benevolence', 'chance': 0.35}),
    ('offer to keep the hardest watch, at the edge of the camps, for the whole gathering', 'R1', 'W.7', 0.5, '', {'title': 'army officer', 'requires': 'soldier', 'without': 'impossible', 'body': 'heavy', 'habit': True, 'v': 'benevolence, stimulation', 'chance': 0.35}),
    ('sit with the oldest hunters to learn the hills, and offer to lead the young', 'G1', 'U.7', 0.5, '', {'title': 'army officer', 'requires': 'soldier', 'without': 'impossible', 'habit': True, 'v': 'tradition, achievement', 'chance': 0.35}),
    ('name the best leader among the other bands, and stand behind them', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'universalism, benevolence', 'chance': 0.7}),
    ("ask for a seat at the clans' council fire instead, to speak for your band", 'W.34 B.33 R.33', None, 0.5, '', {'v': 'power, conformity', 'chance': 0.7}),
    ('give the shaman furs to ask the spirits who should lead, and abide by it', 'W.34 B.33 G.33', None, 0.5, '', {'closed': "approval: the spirits' price, asked through the shaman; backfire: the shaman calls in the spirits' debt at every quarrel after, and the clans whisper that the choice was bought", 'binds': True, 'v': 'tradition, security', 'chance': 0.7}),
    ('say the clans need no war leader while no raiders come, and go home to hunt', 'U.34 R.33 G.33', None, 0.5, '', {'v': 'self-direction, universalism', 'chance': 0.7}),
    ('ask instead to keep the stores and the signal fires for all the clans', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'security, achievement', 'chance': 0.7}),
 ]},
{'name': 'the parish no one else will take',
 'stages': 'young_adult adult mature elder',
 'age': (23, 95),
 'alpha': 'W.4 U.1 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'faith, work, community',
 'horizon': 'years',
 'roles': 'boss, elder, colleague',
 'requires': 'ordained religious minister | member of a monastic community',
 'worlds': {'earth': "the faith's leaders need someone for a poor, far congregation in a town that has lost its "
                     "work, or for the order's last small house there",
            'tribal': 'the keepers of the rites need someone to go to a small, far band whose rite-keeper has died '
                      'and whose hunting has failed',
            'magic': 'the temple needs a priest, or a monk or nun of the order, for the cold shrine of a mining town '
                     'whose mine has closed'},
 'timing': {'times': 'per minister of religion or member of an order a year: about 1 in 6 are asked to take a hard '
                     'post, a poor, far or shrinking congregation or a small house of the order in a hard place '
                     '(estimate); about 4 lives in 1,000 are ministers of religion and 1 in 1,000 lives in a '
                     'religious community (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "{boss} rings from the faith's offices on a Monday. The congregation at the end of the valley "
                       'line has had nobody for two years: a cold stone building, a boiler that leaks, fourteen '
                       'faithful with an average age of seventy-eight, and a town whose factory closed ten years '
                       'ago. The order\'s little house there is down to two. "Nobody else will take it," {boss} '
                       'says, and waits.'),
                      ('W',
                       'Someone has to go, and the vows {N} took did not say only where it is warm. A post is a '
                       'duty, not a prize.'),
                      ('U',
                       '{N} wants the facts before an answer: how many come, what the building costs to heat, what '
                       'the town still has, and whether anything there can grow.'),
                      ('B',
                       'A hard post done well gets noticed. {N} also knows that two years in the valley could be two '
                       "years nobody in the faith's offices remembers."),
                      ('R',
                       'Fourteen people have kept a cold building going for two years with nobody to lead them. '
                       'Something tightens in {N} at the thought of them, and {N} wants to be on the train.'),
                      ('G',
                       '{N} has seen towns like that one: the boarded pub, the closed shops, the old women who still '
                       'polish the brass on a weekday. Places come back, slowly, if someone stays long enough.')],
            'tribal': [('',
                        'Word comes up the river from the keepers of the rites: the small band in the far hills has '
                        'lost its rite-keeper, the deer have gone from their valley, and nobody will go to them. The '
                        'old keeper who brings the word looks at {N} and says nothing more.')],
            'magic': [('',
                       "A letter comes under the temple's seal: the shrine in the mining town has stood cold since "
                       'the mine closed and its old priest died. The roof leaks, the bell is cracked, and a handful '
                       "of miners' widows still sweep the steps each morning. Nobody in the temple wants it.")]},
 'outcomes': (['A year on there are more faces at the rites than there were, and the place has begun to feel alive '
               'again.',
               "Whatever {N} chose, the faith's leaders find a way forward for the far congregation, and {N} sleeps "
               'well that night.'],
              ['The first winter is long and cold, and by spring there are fewer faces at the rites, not more.',
               "The faith's leaders are not pleased with how it went, and for a while {N} hears less from the "
               'offices.']),
 'options': [
    ("say yes, since the faith's leaders asked and someone has to go", 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'say yes, since the keepers of the rites asked and someone has to go', 'magic': 'say yes, since the temple asked and someone has to go'}, 'chance': 0.65}),
    ('spend a week in the town first, and go with a plan for the building', 'U1', None, 0.45, '', {'door': True, 'aims': 'senior cleric', 'v': 'achievement, security', 'world': {'tribal': 'spend a moon with the far band first, and go with a plan for the hard winters', 'magic': 'spend a week in the mining town first, and go with a plan for the shrine'}, 'chance': 0.75}),
    ("take it, on the leaders' word that it counts toward the next senior post", 'B1', None, 0.45, '', {'aims': 'senior cleric', 'v': 'power, achievement', 'world': {'tribal': "go, on the keepers' word that it will count when the many bands choose their next keeper", 'magic': "take it, on the temple's word that it counts toward a great temple later"}, 'chance': 0.55}),
    ('go at once, and keep the doors open every night of the first winter', 'R1', None, 0.45, '', {'habit': True, 'self_control': '+', 'body': 'light', 'v': 'stimulation, benevolence', 'world': {'tribal': "go at once, and keep the far band's fire lit for the rites every night of the first winter", 'magic': 'go at once, and keep the shrine open and lit every night of the first winter'}, 'chance': 0.75}),
    ('take it, and stay for good: learn every one of the fourteen by name', 'G1', None, 0.45, '', {'habit': True, 'grants': 'a flock that follows you', 'v': 'benevolence, tradition', 'world': {'tribal': 'go, and stay for good: learn every hearth of the far band by name', 'magic': 'take it, and stay for good: learn every widow on the steps by name'}, 'chance': 0.7}),
    ('take it for one year, as the rule allows, and report what the place truly needs', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'go for one winter, as the keepers allow, and bring back word of what the band truly needs', 'magic': "take it for one year, as the temple's rule allows, and report what the shrine truly needs"}, 'chance': 0.75}),
    ('ask for a second minister as well, with a costed case the leaders cannot refuse', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'ask for a second keeper to go too, with reasons the elders cannot turn down', 'magic': 'ask the temple for a second priest, with a reckoning it cannot refuse'}, 'chance': 0.65}),
    ('say no, and stay where the work is already growing', 'B1', 'R.7', 0.5, '', {'mark': 'turned down a chance', 'v': 'self-direction, security', 'world': {'tribal': 'say no, and stay with the band where the rites already draw every hearth', 'magic': 'say no, and stay at the shrine where the work is already growing'}, 'chance': 0.85}),
    ('preach in the market square on the first day, so the whole town knows', 'R1', 'G.7', 0.5, '', {'grants': 'preaching', 'v': 'stimulation, universalism', 'world': {'tribal': "speak for the spirits at the far band's fire on the first night, so every hearth hears", 'magic': 'preach on the market steps on the first day, so the whole town knows'}, 'chance': 0.65}),
    ('ask the old faithful what they need, and keep the services they have always had', 'G1', 'W.7', 0.5, '', {'self_control': '+', 'v': 'tradition, conformity', 'world': {'tribal': 'ask the old ones of the far band what they need, and keep the rites they have always kept', 'magic': 'ask the widows what they need, and keep the old offices they have always had'}, 'chance': 0.7}),
 ]},
{'name': 'a quarrel splits the congregation',
 'stages': 'young_adult adult mature elder',
 'age': (23, 95),
 'alpha': 'W.1 U.4 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'faith, community',
 'horizon': 'months',
 'roles': 'elder, colleague, boss',
 'requires': 'ordained religious minister | member of a monastic community',
 'worlds': {'earth': 'two sides of the congregation quarrel over a change: the new music, the old words of the '
                     'service, or selling the hall',
            'tribal': 'two sides of the band quarrel over the rites: the new songs the young bring, or moving the '
                      'sacred fire to the new camp',
            'magic': "two sides of the temple's faithful quarrel: the new hymns, the old tongue of the offices, or "
                     "selling the temple's old hall to a guild"},
 'timing': {'times': 'per minister of religion or member of an order a year: about 1 in 8 lead a congregation or a '
                     'house through a quarrel that splits it into sides, over the music, the words of the service or '
                     'the sale of a building (estimate); surveys of congregations find that most go through a '
                     'serious conflict every few years (estimate); about 4 lives in 1,000 are ministers of religion '
                     '(catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The members' meeting runs two hours over. One side wants the hall at the back sold, and the "
                       "money spent on a new roof and music the young will come for; the other side's grandparents "
                       'built that hall with their own hands. {elder} speaks for the old families and {colleague} '
                       'for the newcomers, and when they sit down both of them look at {N}.'),
                      ('W',
                       'There is a written constitution for exactly this: notice of a vote, a quorum, a fair count. '
                       '{N} is tired of people who want to win more than they want it done right.'),
                      ('U',
                       'Both sides are arguing about the hall, but {N} suspects the quarrel is about something else: '
                       'who belongs here now, and who decides.'),
                      ('B',
                       'Whichever side wins will run this congregation for twenty years. {N} can see who is going to '
                       "win, and so, perhaps, can the faith's leaders."),
                      ('R',
                       '{N} can feel the hurt in the room: the old man who laid the floor of that hall, the young '
                       "mother who only wants somewhere for the toddlers' group. {N} wants to tell all of them to "
                       'stop.'),
                      ('G',
                       'The hall has stood for sixty years, through quarrels like this one before. Halls are sold '
                       'and built again; families stay, if they are not torn apart first.')],
            'tribal': [('',
                        'At the fire the band splits. The young want to move the sacred fire to the new camp by the '
                        'river, where the fish are, and sing the new songs there; the old ones say the fire has '
                        "burned under the cliff since their grandmothers' grandmothers. {elder} speaks for the old "
                        'and {colleague} for the young, and both look at {N}.')],
            'magic': [('',
                       "The temple's chapter meeting runs late. A guild has offered good silver for the temple's old "
                       'hall, and the young faithful want new hymns in the common tongue; the old families still '
                       'sing the offices in the old tongue their forebears brought. {elder} and {colleague} both '
                       'turn to {N}.')]},
 'outcomes': (['By the next feast the two sides are sitting side by side again, and the question that split them is '
               'settled one way or the other.',
               'Whatever {N} chose, the quarrel cools, and a year later the newcomers and the old families are '
               'running the summer fair together.'],
              ['The vote goes through with a margin of three, and a dozen families stop coming.',
               'The quarrel drags on for a season, and {N} is blamed by both sides for not ending it sooner.']),
 'options': [
    ("call a members' meeting, and let the congregation vote by its own rules", 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'world': {'tribal': 'call the whole band to the fire, and let every hearth speak in the old order', 'magic': "call the chapter, and let the faithful vote by the temple's rule"}, 'chance': 0.65}),
    ('meet each side alone, and draft a middle way they can both live with', 'U1', None, 0.45, '', {'grants': 'settling disputes', 'v': 'universalism, achievement', 'world': {'tribal': 'sit with each side alone, and find a middle way both can live with', 'magic': 'hear each side alone, and draft a middle way both can live with'}, 'chance': 0.6}),
    ('back the side that will win, and make sure they remember who helped', 'B1', None, 0.45, '', {'aims': 'senior cleric', 'v': 'power', 'world': {'tribal': 'stand with the side that will win, and make sure they remember it', 'magic': 'back the side that will win, and make sure the chapter remembers it'}, 'chance': 0.7}),
    ('preach on it from the heart, and tell both sides they are wrong', 'R1', None, 0.45, '', {'self_control': '-', 'v': 'stimulation, universalism', 'world': {'tribal': 'speak for the spirits at the fire, and tell both sides they shame the dead'}, 'chance': 0.65}),
    ("take the old families' large gift for the roof, and speak for their side", 'G1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a gift for a vote; backfire: the other side finds out, and half the congregation leaves with them', 'self_control': '-', 'v': 'tradition, security', 'world': {'tribal': "take the old hearths' gift of furs, and speak for their side at the fire", 'magic': "take the old families' purse for the roof, and speak for them in chapter"}, 'chance': 0.75}),
    ('set up a working group from both sides, with a remit and a date to report', 'W1', 'U.7', 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'choose two from each side to sit apart and bring an answer before the moon is full', 'magic': 'name a committee from both sides, with a charge and a date to answer by'}, 'chance': 0.75}),
    ('find out what the hall is really worth, and who stands to gain from a sale', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'find out what the new camp would truly give, and who would gain most from the move', 'magic': 'find out what the hall is really worth, and who in the chapter gains by the sale'}, 'chance': 0.8}),
    ('give the newcomers the evening service to run however they like', 'B1', 'R.7', 0.5, '', {'v': 'self-direction, power', 'world': {'tribal': 'give the young the night songs to sing however they like', 'magic': 'give the young faithful the evening office to sing however they like'}, 'chance': 0.7}),
    ('bring both sides to one long shared meal, and let them talk till late', 'R1', 'G.7', 0.5, '', {'door': True, 'grants': 'a flock that follows you', 'v': 'benevolence, stimulation', 'world': {'tribal': 'bring both sides to one great shared meal at the fire, and let them talk till dawn', 'magic': 'bring both sides to one long table in the hall, and let them talk till late'}, 'chance': 0.75}),
    ('keep the old service and the new one side by side, a week each', 'G1', 'W.7', 0.5, '', {'v': 'tradition, conformity', 'world': {'tribal': 'keep the old songs and the new ones side by side, a night each', 'magic': 'keep the old office and the new hymns side by side, a week each'}, 'chance': 0.65}),
 ]},
{'name': 'the old house of worship needs a roof',
 'stages': 'adult mature elder',
 'age': (35, 95),
 'alpha': 'W.4 U.1 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'faith, money, community',
 'horizon': 'years',
 'roles': 'boss, elder, colleague',
 'requires': 'senior cleric',
 'worlds': {'earth': "the great old house of worship is falling in, and the money to save it would feed the town's "
                     'poor for years',
            'tribal': 'the great lodge of the gathering place is falling in, and the hides and meat to raise it '
                      'again would feed the hungry hearths all winter',
            'magic': "the roof of the great temple is failing, and the silver to mend it would feed the city's poor "
                     'for years'},
 'timing': {'times': 'per senior cleric a year: about 1 in 5 face a great repair on an old building the congregation '
                     'cannot afford (estimate); old houses of worship need a major repair every few decades, and '
                     'many close for want of the money (estimate); about 5 lives in 10,000 are senior clerics '
                     '(catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The surveyor's report runs to forty pages, and its last page is one long number: the roof of "
                       'the old house of worship, four hundred years old, is failing, and a beam came down in the '
                       'side aisle in the night. The same money would run the food bank in the basement for fifteen '
                       "years. {boss} at the faith's council has written to ask what {N} proposes."),
                      ('W',
                       "The building was given into the faith's keeping by people dead for centuries, and the poor "
                       "are the faith's charge too. {N} believes there is a right order to do these things in, if "
                       'only it can be found.'),
                      ('U',
                       '{N} reads the report twice and starts a spreadsheet: phases, grants, cheaper materials, what '
                       'can wait and what cannot.'),
                      ('B',
                       'A great building saved is the kind of work the faith remembers, and the council too, when '
                       'the order next chooses its head. {N} also knows which families in town have money and would '
                       'like their name on something.'),
                      ('R',
                       'People are sleeping in doorways two streets away, and the council wants a fund for slates. '
                       '{N} is angry before the meeting has even started.'),
                      ('G',
                       'The stones were cut from the hill above the town, and the yew in the yard is older than the '
                       "roof. Buildings, like people, have their time, and {N} wonders whether this one's has "
                       'come.')],
            'tribal': [('',
                        'The great lodge at the gathering place, where every band has met for the rites since the '
                        'oldest tellings, is sagging: its poles have rotted, and a beam fell at the last full moon. '
                        "To raise it again would take the hides and meat of a whole season's hunting, and three "
                        'hearths went hungry last winter.')],
            'magic': [('',
                       "The great temple's roof is failing: a beam fell in the side aisle at the last feast, and the "
                       "masons' guild names a sum in silver that would feed the city's poor for years. The temple's "
                       'council has written to ask what {N} proposes.')]},
 'outcomes': (['Two years on the roof is sound and the poor have not gone short, and nobody can quite say how both '
               'were managed.',
               'Whatever {N} chose, the house of worship finds a way through, and the town is glad of it.'],
              ["The money runs out halfway, the scaffolding stands all winter, and the council's next letter is "
               'shorter.',
               'The quarrel over roof or bread divides the congregation, and {N} is left holding both halves of '
               'it.']),
 'options': [
    ("apply to the faith's council for a grant by its rules, and wait the turn", 'W1', None, 0.45, '', {'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'ask the keepers of all the bands for their share by the old way, and wait', 'magic': "petition the temple's council for the repair by its rule, and wait the turn"}, 'chance': 0.7}),
    ('have the old silver valued, and sell it quietly to pay for the roof', 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "approval: the house's old silver sold without the council's leave; backfire: it is missed at the feast, and the faith's council asks where it went", 'self_control': '-', 'v': 'achievement, security', 'world': {'tribal': 'trade the old sacred shells away quietly, for the hides the lodge needs', 'magic': "have the temple's old silver weighed, and sell it quietly to pay the masons"}, 'chance': 0.75}),
    ('ask the richest family in town to pay, and carve their name over the door', 'B1', None, 0.45, '', {'aims': 'head of a faith order', 'v': 'power, achievement', 'world': {'tribal': 'ask the richest hearth for the hides, and cut their sign over the lodge door', 'magic': 'ask the richest merchant house to pay, and carve its arms over the door'}, 'chance': 0.65}),
    ('spend the money on the poor this winter, and let the roof wait', 'R1', None, 0.45, '', {'v': 'benevolence, self-direction', 'world': {'tribal': 'give the hides and meat to the hungry hearths this winter, and let the lodge wait', 'magic': 'spend the silver on the poor this winter, and let the roof wait'}, 'chance': 0.85}),
    ('close the great hall, and worship in the small side room that is still dry', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'world': {'tribal': 'let the great lodge fall, and hold the rites in the small lodge beside it', 'magic': 'close the great nave, and keep the offices in the side chapel that is still dry'}, 'chance': 0.7}),
    ('run a ten-year appeal with a committee, every gift accounted in public', 'W1', 'B.7', 0.5, '', {'grants': 'organising people', 'v': 'conformity, achievement', 'world': {'tribal': 'set every band a share to bring to each gathering for ten summers, and count it before all', 'magic': 'run a ten-year appeal with a council of givers, every coin accounted in public'}, 'chance': 0.7}),
    ('train a volunteer crew under one paid roofer, and let them do the rest', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, achievement', 'world': {'tribal': 'have one old lodge-builder teach the young hunters, and raise the poles together', 'magic': 'hire one master mason to train the faithful, and let them do the rest'}, 'chance': 0.65}),
    ('rent the hall to the town on weekdays, and put the rent into the roof', 'B1', 'G.7', 0.5, '', {'self_control': '+', 'v': 'achievement, security', 'world': {'tribal': 'lend the lodge to the traders between the rites, and take hides for the raising', 'magic': 'let the guilds hire the hall on weekdays, and put the rents into the roof'}, 'chance': 0.75}),
    ('climb up with the congregation every rest day, and mend what can be mended', 'R1', 'W.7', 0.5, '', {'self_control': '+', 'body': 'heavy', 'grants': 'a flock that follows you', 'v': 'stimulation, tradition', 'world': {'tribal': 'climb up with the band each rest day, and lash new poles where the old ones failed', 'magic': 'climb up with the faithful each rest day, and mend what the masons cannot reach'}, 'chance': 0.55}),
    ('ask the oldest members what the building means to them, and put it in the appeal', 'G1', 'U.7', 0.5, '', {'aims': 'head of a faith order', 'v': 'tradition, universalism', 'world': {'tribal': 'ask the oldest of every band what the lodge has meant to them, and tell it at the gathering', 'magic': "gather the oldest faithful's memories of the temple, and write them into the appeal"}, 'chance': 0.7}),
 ]},
{'name': 'the young want the old rite back',
 'stages': 'adult mature elder',
 'age': (35, 95),
 'alpha': 'W.1 U.4 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'faith, community',
 'horizon': 'months',
 'roles': 'elder, colleague, mentor',
 'requires': 'senior cleric',
 'worlds': {'earth': 'the young members want the ancient rite and its old words back, and the elders who fought for '
                     'the modern service are hurt',
            'tribal': 'the young of the bands want the oldest rite back, the long night of the masks, and the old '
                      'ones who set it aside are hurt',
            'magic': 'the young faithful want the old rite in the ancient tongue, and the elders who brought in the '
                     'common tongue are hurt'},
 'timing': {'times': 'per senior cleric a year: about 1 in 6 find the young asking for an older form of the rite '
                     'than the one their elders fought for (estimate); a turn back to old forms of worship among the '
                     'young is reported across many faiths (estimate); about 5 lives in 10,000 are senior clerics '
                     '(catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Eleven of the young members come to {Ns} study after the service with a printed booklet: the '
                       'old rite in its ancient words, as it was before the elders changed it forty years ago. They '
                       'want it once a month, at dawn, with the old chant. {elder}, who led the campaign for the '
                       'modern service when young, hears of it the same evening and does not come the next week.'),
                      ('W',
                       "The old rite is part of the faith's own law, never done away with, only set aside. {N} would "
                       "like the council's ruling before anything else."),
                      ('U',
                       '{N} read the old words at the seminary and has half forgotten them. There is a great deal in '
                       'them, and {N} wants to understand why the young have found them now.'),
                      ('B',
                       "Young members are rare, and these eleven are the congregation's future. Whoever gives them "
                       "what they want will be remembered for it, in the faith's offices too."),
                      ('R',
                       '{N} saw their faces when they chanted a line of it: lit up, the way faces look when they '
                       'find something true. It is hard not to want that for them.'),
                      ('G',
                       'Rites change and come back like seasons, and {N} has seen it before. What matters is that '
                       '{elder} and the young are still under the same roof in ten years.')],
            'tribal': [('',
                        'The young of the bands come to {N} at the gathering: they want the long night of the masks '
                        'back, the oldest rite, which the old ones set aside when they were young. {elder}, who '
                        'ended it, walks away from the fire without a word.')],
            'magic': [('',
                       'A dozen of the young faithful bring {N} a copy of the old rite in the ancient tongue, as it '
                       "was sung before the temple's elders changed it forty years ago. {elder}, who led that "
                       'change, stops coming to the evening office.')]},
 'outcomes': (['The old chant is heard again on the first morning of the month, and {elder} is there, at the back, '
               'by the second time.',
               'Whatever {N} chose, the young stay and the elders stay, and the congregation is fuller than it was.'],
              ['The young drift off to a congregation across the city that gives them the old rite every week.',
               "{elder} writes a hurt letter to the faith's council, and the quarrel outlives the season."]),
 'options': [
    ("ask the faith's council for a ruling, and keep to whatever it says", 'W1', None, 0.45, '', {'mark': 'kept your word', 'v': 'conformity, tradition', 'world': {'tribal': 'ask the keepers of all the bands to decide, and keep to it', 'magic': "ask the temple's council for a ruling, and keep to whatever it says"}, 'chance': 0.8}),
    ('study the old words with the young ones, line by line, before deciding', 'U1', None, 0.45, '', {'habit': True, 'grants': 'scripture', 'v': 'self-direction, tradition', 'world': {'tribal': 'learn what each old mask means with the young ones, one by one, before deciding', 'magic': 'read the ancient tongue with the young faithful, line by line, before deciding'}, 'chance': 0.75}),
    ('give the young ones the rite, and be known as the cleric who brought them back', 'B1', None, 0.45, '', {'identity': True, 'aims': 'head of a faith order', 'v': 'power, achievement', 'world': {'tribal': 'give the young the long night, and be known as the keeper who brought them back', 'magic': 'give the young the old rite, and be known as the priest who brought them back'}, 'chance': 0.65}),
    ("hold the old rite with them at dawn, without the elders' leave", 'R1', None, 0.45, '', {'mark': 'defied an authority', 'closed': "approval: the old rite held against the elders' wishes; backfire: the elders write to the faith's council, and the cleric is called in to explain", 'v': 'stimulation, tradition', 'world': {'tribal': "hold the long night of the masks with them, without the old ones' leave", 'magic': "sing the old rite with them at dawn, without the elders' leave"}, 'chance': 0.7}),
    ('visit the elders who fought for the modern service, one by one, and listen', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'world': {'tribal': 'sit with each of the old ones who ended the long night, and listen', 'magic': 'visit each elder who brought in the common tongue, and listen'}, 'chance': 0.7}),
    ("lead the old rite exactly by the book, and invite the faith's leaders to see it", 'W1', 'B.7', 0.5, '', {'aims': 'head of a faith order', 'v': 'conformity, power', 'world': {'tribal': 'lead the long night exactly as the oldest tellings say, and ask the keepers of all the bands to come', 'magic': "sing the old rite exactly by the rubric, and invite the temple's council to see it"}, 'chance': 0.6}),
    ('write a plain translation, so the young feel what the old words mean', 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': 'tell the young plainly what each old mask means, so they feel it', 'magic': 'write a plain translation beside the ancient tongue, so the young feel what it says'}, 'chance': 0.65}),
    ('offer the elders the places of honour at the old rite, so the families hold together', 'B1', 'G.7', 0.5, '', {'v': 'security, tradition', 'world': {'tribal': 'give the old ones the first places at the long night, so the hearths hold together', 'magic': 'give the elders the seats of honour at the old rite, so the families hold together'}, 'chance': 0.75}),
    ('preach that both rites belong to the faith, and both sides to each other', 'R1', 'W.7', 0.5, '', {'grants': 'a flock that follows you', 'v': 'universalism, stimulation', 'world': {'tribal': "speak for the spirits at the fire: both rites are the band's, and so are both sides", 'magic': 'preach that both rites belong to the faith, and both sides to the temple'}, 'chance': 0.7}),
    ('let the old rite come back slowly, at the great feasts, and see what it does', 'G1', 'U.7', 0.5, '', {'grants': 'leading a ceremony', 'v': 'tradition, self-direction', 'world': {'tribal': 'let the long night come back slowly, at the great gathering only, and see what it does', 'magic': 'let the old rite come back slowly, at the great feasts only, and see what it does'}, 'chance': 0.7}),
 ]},
{'name': 'the congregation needs a senior minister',
 'stages': 'adult mature elder',
 'age': (35, 85),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'faith.5',
 'per_year': (0.0, 0.0, 0.0, 0.04, 0.05, 0.02),
 'drivers': 'community+.3',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'faith, work',
 'horizon': 'months',
 'roles': 'boss, mentor, colleague, rival, partner',
 'requires': 'ordained religious minister | member of a monastic community',
 'tenure': (6.0, 100.0),
 'worlds': {'earth': "the great congregation in the town needs a senior minister, and the faith's panel will meet "
                     'the candidates in the spring',
            'tribal': 'the keepers of the rites for many bands need one among them to keep the rites at the great '
                      'gathering, and they will hear each one at the spring fire',
            'magic': "a great temple of the city needs a priest to lead it, and the temple's council will hear the "
                     'candidates at the spring feast'},
 'timing': {'times': 'per minister of religion or member of an order with six years or more behind them, a year: '
                     'about 1 in 25 sees a great congregation or a large house of the order look for a senior '
                     'minister and is asked to stand (estimate); about 1 minister in 8 comes to lead a great '
                     'congregation or to oversee others (catalogue note); about 5 lives in 10,000 are senior clerics '
                     '(catalogue share)',
            'likelier': "a congregation that has grown under them, a degree in theology, a mentor in the faith's "
                        'offices, a town that wants someone it knows',
            'rarer': "a minister new to the faith's ways, a far posting nobody sees, a faith with few great "
                     'congregations',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       "The letter is on the faith's headed paper: the great congregation in the town, eight hundred "
                       'members and a staff of six, needs a senior minister, and {Ns} name has been put forward. '
                       'There will be an application, references, a trial sermon and a panel in the spring. {mentor} '
                       'rings the same evening to say {N} should go for it; {rival}, it turns out, already has.'),
                      ('W',
                       "The faith's rules set the process down, and {N} means to keep every step of it: the degree, "
                       'the references, the sermon, the panel.'),
                      ('U',
                       'Eight hundred members, six staff, an old building and a roll that falls a little every year. '
                       '{N} starts thinking about what the place will need over ten years before thinking about the '
                       'panel at all.'),
                      ('B',
                       "It is the post that leads to the faith's council, sooner or later. {N} runs through the "
                       'names on the panel, and who knows whom.'),
                      ('R',
                       '{N} would rather preach than fill in forms. If the panel wants to know what kind of minister '
                       '{N} is, let them come and hear one.'),
                      ('G',
                       'The congregation {N} serves now has known the family for years: the weddings, the funerals, '
                       'the long winters. Leaving would be a loss on both sides, and the people there might want to '
                       'say so.')],
            'tribal': [('',
                        'At the spring fire the keepers of the rites for many bands will hear who should keep the '
                        'rites at the great gathering. {mentor}, the old keeper, says {N} should speak; {rival} from '
                        'the river band already means to.')],
            'magic': [('',
                       'A letter comes under the seal of a great temple of the city: it needs a priest to lead it, '
                       "and the temple's council will hear the candidates at the spring feast. {mentor} says {N} "
                       'must go; {rival} has already sent a name.')]},
 'outcomes': (['In the spring the letter comes, and by the autumn {N} has a new study, a great congregation and a '
               'diary with no empty evenings in it.',
               'Whatever {N} chose, the decision still feels right a year later, and the people {N} serves say so.'],
              ['The panel thanks {N} warmly and chooses {rival}, and {N} goes home the long way, rehearsing what '
               'might have been said.',
               'The year does not go as planned, and {N} is left with less time, less certainty and the same cold '
               'building.']),
 'options': [
    ('apply by the book: the degree, the references, the trial sermon, the panel', 'W1', None, 0.45, '', {'title': 'senior cleric', 'requires': 'a degree in theology', 'without': 'approval', 'lacking': 0.3, 'self_control': '+', 'v': 'conformity, tradition', 'world': {'tribal': "ask by the old way: the old shaman's years of teaching, the keepers' word, the telling at the fire", 'magic': "apply by the temple's rule: the temple school's seal, the letters, the sermon, the council"}, 'chance': 0.3}),
    ('send the panel a ten-year plan for the congregation, and the figures behind it', 'U1', None, 0.45, '', {'title': 'senior cleric', 'v': 'achievement, self-direction', 'world': {'tribal': "show the keepers how the great gathering's rites could be kept for ten summers to come", 'magic': "send the temple's council a plan for its next ten years, with the reckoning behind it"}, 'chance': 0.3}),
    ("ask the faith's leaders who know your work to put your name first", 'B1', None, 0.45, '', {'title': 'senior cleric', 'v': 'power, achievement', 'world': {'tribal': 'ask the keepers who owe your hearth a gift to speak your name first', 'magic': "ask the council's priests who owe a favour to put your name first"}, 'chance': 0.3}),
    ('preach the trial sermon without notes, as on any ordinary rest day', 'R1', None, 0.45, '', {'title': 'senior cleric', 'v': 'stimulation, self-direction', 'world': {'tribal': 'speak at the spring fire without the old words learned by heart, as the spirits move', 'magic': 'preach before the council without notes, as on any ordinary rest day'}, 'chance': 0.3}),
    ('let the families you have served write to the panel on your behalf', 'G1', None, 0.45, '', {'title': 'senior cleric', 'v': 'tradition, benevolence', 'world': {'tribal': 'let the hearths of your own band speak at the fire on your behalf', 'magic': 'let the families you have served write to the council on your behalf'}, 'chance': 0.3}),
    ('take the smaller post in the next town, and keep the family where it is rooted', 'B.5 G.5', None, 0.5, '', {'binds': True, 'v': 'security, tradition', 'world': {'tribal': 'take the rites of the band next to your own, and keep your hearth where it is', 'magic': 'take the smaller shrine in the next town, and keep the family where it is rooted'}, 'chance': 0.8}),
    ("put a fellow minister's name forward instead, and keep the favour owed", 'B.5 R.5', None, 0.5, '', {'grants': 'friend in power', 'v': 'benevolence, power', 'world': {'tribal': "speak a friend's name at the fire instead, and keep the gift owed", 'magic': "put a fellow priest's name forward instead, and keep the favour owed"}, 'chance': 0.8}),
    ('stay with the flock you have, and study for the degree in the evenings', 'U.5 G.5', None, 0.5, '', {'binds': True, 'grants': 'a degree in theology', 'self_control': '+', 'v': 'achievement, tradition', 'world': {'tribal': 'stay with your own band, and spend the winters learning from the old shaman', 'magic': "stay at your own shrine, and study for the temple school's seal by lamplight"}, 'chance': 0.8}),
    ('ask the congregation you serve first, and stand only with their blessing', 'W.5 R.5', None, 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': 'ask your own band at the fire first, and speak only with their blessing', 'magic': 'ask your own faithful first, and stand only with their blessing'}, 'chance': 0.8}),
    ('offer to stand in for one set year while the panel keeps searching', 'W.5 U.5', None, 0.5, '', {'v': 'conformity, achievement', 'world': {'tribal': 'offer to keep the great rites for one summer while the keepers go on choosing', 'magic': 'offer to lead the temple for one set year while the council keeps searching'}, 'chance': 0.8}),
 ]},
{'name': 'the order chooses its head',
 'stages': 'adult mature elder',
 'age': (45, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'faith.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.03, 0.03),
 'drivers': 'community+.2 fortune+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'faith, publiclife',
 'horizon': 'months',
 'roles': 'boss, rival, mentor, colleague',
 'requires': 'senior cleric | member of a monastic community',
 'tenure': (6.0, 100.0),
 'worlds': {'earth': 'the head of the faith order has died after thirty years, and the council meets to choose who '
                     'comes next',
            'tribal': 'the great shaman whom every band heeds has died, full of years, and the keepers of the rites '
                      'gather to choose who comes next',
            'magic': "the high priest of the god's order has died, and the order's council gathers in the great "
                     'temple to choose the next'},
 'timing': {'times': 'per senior cleric, or member of an order of six years or more, a year: about 1 in 40 is among '
                     'those the faith or the order weighs when it chooses a new head (estimate); heads of faith '
                     'bodies and of orders are few, most serve for life, and a council or a chapter chooses them '
                     '(estimate); about 2 lives in 100,000 lead a faith order (catalogue share)',
            'likelier': 'a flock that follows, a name known across the country, a degree in theology, long years in '
                        "the order, the old head's death or retirement",
            'rarer': 'a junior post, a faith that chooses its heads from elsewhere, a council already split',
            'gap_years': (8.0, 20.0)},
 'scenes': {'earth': [('',
                       'The old head of the order died in the spring, full of years, after thirty years in office, '
                       'and the council will meet at midsummer to choose who comes next. Three names are spoken of '
                       'in the corridors, and {Ns} is one of them. {rival} has been travelling to every house of the '
                       'order since the funeral; {mentor}, who has seen two of these elections, says the council '
                       'always surprises itself.'),
                      ('W',
                       'The order chooses its head by a rule nearly a thousand years old: a vigil, a vote, and a '
                       'second vote if the first is split. {N} has always kept the rule and will keep this one.'),
                      ('U',
                       '{N} has been thinking for years about where the order must go: the empty houses, the young '
                       'who come and do not stay, the money. Nobody else seems to have a plan at all.'),
                      ('B', 'Fourteen votes on the council, and eight make a head. {N} can count six already.'),
                      ('R',
                       '{N} is tired of the careful talk in the corridors. The order is shrinking, and somebody '
                       'should say so out loud.'),
                      ('G',
                       '{N} goes on with the day: prayer at dawn, the garden, the sick at the house in the town. If '
                       'the order wants {N}, it knows where to look.')],
            'tribal': [('',
                        'The great shaman whom every band heeded has died, full of years, and at midsummer the '
                        'keepers of the rites will gather at the sacred place to choose who comes next. {Ns} name is '
                        'spoken at the fires; {rival} has walked to every band since the burial.')],
            'magic': [('',
                       "The high priest of the god's order has died, and at midsummer the order's council will "
                       'gather in the great temple to choose the next. Three names are whispered in the cloisters, '
                       'and {Ns} is one; {rival} has visited every house of the order since the funeral rites.')]},
 'outcomes': (["At midsummer the bell rings for the council's choice, and by evening the whole order knows what kind "
               'of years are coming.',
               'Whatever {N} chose, the order comes through the choosing whole, and {N} is glad of the part played '
               'in it.'],
              ['The council chooses {rival} on the second vote, and {N} bows with the rest to the new head.',
               'The choosing drags on for a season, old friends take sides, and {N} comes out of it more tired than '
               'before.']),
 'options': [
    ('keep the vigil and the rule of election, and let the vote fall where it will', 'W1', None, 0.45, '', {'habit': True, 'title': 'head of a faith order', 'v': 'tradition, conformity', 'world': {'tribal': 'keep the vigil at the sacred place by the old way, and let the keepers choose', 'magic': "keep the vigil by the order's rule, and let the vote fall where it will"}, 'chance': 0.06}),
    ('set out for the council how the order must change over twenty years', 'U1', None, 0.45, '', {'title': 'head of a faith order', 'v': 'achievement, self-direction', 'world': {'tribal': "tell the keepers how the bands' rites must change in the winters to come", 'magic': 'set before the council how the order must change over twenty years'}, 'chance': 0.06}),
    ('win the votes over one supper at a time, until the count is sure', 'B1', None, 0.45, '', {'habit': True, 'self_control': '+', 'title': 'head of a faith order', 'v': 'power', 'world': {'tribal': 'win the keepers over one by one, with gifts and talk at every fire', 'magic': "win the council's votes one supper at a time, until the count is sure"}, 'chance': 0.06}),
    ('stand up in the council and say out loud that the order is dying', 'R1', None, 0.45, '', {'identity': True, 'title': 'head of a faith order', 'v': 'stimulation, universalism', 'world': {'tribal': 'stand at the fire and say aloud that the rites are dying in the bands', 'magic': 'stand up in the council and say aloud that the order is dying'}, 'chance': 0.06}),
    ('go on with the daily prayer and the sick, and let the order come or not', 'G1', None, 0.45, '', {'title': 'head of a faith order', 'mark': 'helped someone in need', 'v': 'tradition, benevolence', 'world': {'tribal': "go on with your own band's rites, and let the keepers come if they will", 'magic': 'go on with the daily offices and the sick, and let the order come if it will'}, 'chance': 0.06}),
    ("spend the season of the election working at the order's poorest house", 'R.5 G.5', None, 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'spend the season of the choosing with the poorest band, keeping their rites', 'magic': "spend the election season at the order's poorest house, among the sick"}, 'chance': 0.85}),
    ('back the strongest candidate early, and become their right hand', 'U.5 B.5', None, 0.5, '', {'binds': True, 'grants': 'friend in power', 'v': 'power, achievement', 'world': {'tribal': 'stand early with the strongest keeper, and be at their side at every fire', 'magic': 'back the strongest candidate early, and be their right hand in the council'}, 'chance': 0.85}),
    ('write an open letter to the whole order on what the next head must do', 'U.5 R.5', None, 0.5, '', {'mark': 'took a wild risk', 'v': 'self-direction, universalism', 'world': {'tribal': 'go from band to band, telling what the next great shaman must do', 'magic': 'write an open letter to every house of the order on what the next high priest must do'}, 'chance': 0.85}),
    ('ask the council to bind whoever is chosen to a term of ten years', 'W.5 B.5', None, 0.5, '', {'v': 'security, power', 'world': {'tribal': 'ask the keepers to choose the next great shaman for ten winters, not for life', 'magic': 'ask the council to bind whoever is chosen to a term of ten years'}, 'chance': 0.85}),
    ('step aside for an older colleague whose turn it is, and serve under them', 'W.5 G.5', None, 0.5, '', {'door': True, 'v': 'tradition, conformity', 'world': {'tribal': 'step aside for an older keeper whose time it is, and stand behind them', 'magic': 'step aside for an older priest whose turn it is, and serve under them'}, 'chance': 0.85}),
 ]},
{'name': "a colleague's theft the faith would rather bury",
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'faith.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.015, 0.01),
 'drivers': 'harsh+.2 prosper-.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'faith, work, money',
 'horizon': 'months',
 'roles': 'colleague, boss, friend',
 'requires': 'senior cleric | ordained religious minister | head of a faith order | deacon or elder',
 'worlds': {'earth': "a fellow cleric has been taking money given for the poor, and the faith's leaders want it "
                     'handled quietly',
            'tribal': 'a fellow keeper of the rites has been taking the furs and meat given at the rites for the '
                      'hungry hearths, and the old keepers want it kept within the fire',
            'magic': "a fellow priest has been taking the alms given at the temple for the poor, and the temple's "
                     'council wants it handled quietly'},
 'timing': {'times': 'per minister, senior cleric, head of an order or elder of a congregation a year: about 1 in 80 '
                     'learns that a fellow cleric has been taking money given for the poor (estimate); audits of '
                     'faith charities find money misused in a small share of them each year, and most cases come to '
                     'light through someone inside (estimate); about 3 lives in 100 are elders of a congregation and '
                     'about 4 in 1,000 ministers (catalogue shares)',
            'likelier': 'loose books, one person counting the collection alone, a colleague in debt, a faith that '
                        'prizes its good name above all',
            'rarer': 'two signatures on every gift, an outside auditor, a small congregation where everyone counts '
                     'the money together',
            'gap_years': (8.0, 20.0)},
 'scenes': {'earth': [('',
                       "The poor fund's book does not add up, and it has not added up for three years. {N} sits late "
                       'in the office with the bank statements and the collection slips, and the gap has one name on '
                       'it: {colleague}, who has counted the money alone every week since the old treasurer died. '
                       "When {N} rings {boss} at the faith's offices, the answer comes after a long pause: deal with "
                       "it quietly, for the sake of the faith's good name."),
                      ('W',
                       "The faith's leaders have asked, and {N} has always done what they ask. But the money was "
                       "given for the poor, and the faith's own law is plain about that."),
                      ('U',
                       '{N} goes through it twice: every slip, every withdrawal, the dates against {Ns} own diary. '
                       'The figures do not lie, and there is no innocent way to read them.'),
                      ('B',
                       '{colleague} has a great deal to lose, and {N} now knows exactly how much. That is a kind of '
                       'power, and {N} turns it over carefully.'),
                      ('R',
                       '{N} has known {colleague} for twenty years, and the anger and the hurt come up together. '
                       'There is no sleeping on this.'),
                      ('G',
                       'The money came from the old women in the front seats, a little every week for forty years. '
                       'They are the ones {N} keeps thinking of.')],
            'tribal': [('',
                        'The hungry hearths had less than was given for them all winter. {N} has watched where the '
                        'furs and meat went after the rites, and the trail leads to the shelter of {colleague}. The '
                        'old keepers, when {N} tells them, say it should be kept within the fire.')],
            'magic': [('',
                       "The temple's alms chest does not match the almoner's book, and has not for three years. {N} "
                       'follows the gap to {colleague}, who has counted the alms alone since the old almoner died, '
                       "and the temple's council answers {Ns} letter with one line: deal with it quietly.")]},
 'outcomes': (['By the summer the poor fund is whole again and the books are open, and the congregation knows as '
               'much as it needs to.',
               'Whatever {N} chose, the thing is settled, and {N} can face the old women in the front seats on the '
               'rest day.'],
              ["It comes out in the worst way, in the local paper, and for a season the faith's good name and {Ns} "
               'with it are in every mouth.',
               'The leaders close ranks, {colleague} is moved quietly to another post, and {N} is the one people '
               'stop speaking to.']),
 'options': [
    ("do as the faith's leaders ask, and let it be dealt with quietly", 'W1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a theft from the poor fund buried; backfire: the papers find it, and the trust is gone', 'takes_if_fails': 'a flock that follows you', 'self_control': '-', 'v': 'conformity, security', 'world': {'tribal': 'do as the old keepers ask, and keep it within the fire', 'magic': "do as the temple's council asks, and let it be dealt with quietly"}, 'chance': 0.71}),
    ("send every slip and figure to the faith's council, and ask for an outside audit", 'U1', None, 0.45, '', {'identity': True, 'v': 'universalism, conformity', 'world': {'tribal': 'lay every tally before the keepers of all the bands, and ask them to count it again', 'magic': "send every slip and figure to the order's council, and ask for an outside audit"}, 'chance': 0.59}),
    ('tell the colleague to repay every coin and resign, or the police hear of it', 'B1', None, 0.45, '', {'mark': 'made an enemy', 'v': 'power, universalism', 'world': {'tribal': 'tell the keeper to give back every fur and leave the rites, or the whole gathering hears of it', 'magic': 'tell the priest to repay every coin and resign, or the city watch hears of it'}, 'chance': 0.69}),
    ("go round to the colleague's house that evening, and have it out face to face", 'R1', None, 0.45, '', {'v': 'stimulation, universalism', 'world': {'tribal': "go to the keeper's shelter that night, and have it out face to face", 'magic': "go to the priest's lodging that evening, and have it out face to face"}, 'chance': 0.79}),
    ('stand up on the rest day, and tell the congregation the truth', 'G1', None, 0.45, '', {'identity': True, 'grants': 'a flock that follows you', 'v': 'benevolence, universalism', 'world': {'tribal': 'stand up at the rites, and tell the band the truth', 'magic': 'stand up at the rest-day office, and tell the faithful the truth'}, 'chance': 0.6}),
    ('take the accounts to the police yourself, whatever the leaders say', 'W.34 U.33 R.33', None, 0.5, '', {'mark': 'defied an authority', 'v': 'universalism, conformity', 'world': {'tribal': 'take the tallies to the elders of the gathering yourself, whatever the old keepers say', 'magic': 'take the accounts to the city watch yourself, whatever the council says'}, 'chance': 0.6}),
    ('set up a finance committee: two signatures and an open ledger for every gift', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'security, universalism', 'world': {'tribal': 'set two keepers to count every gift together, before the whole band', 'magic': 'set up a chapter of almoners: two seals and an open ledger for every gift'}, 'chance': 0.81}),
    ("stand up at the faith's council and ask, on the record, where the money went", 'W.34 B.33 R.33', None, 0.5, '', {'v': 'universalism, power', 'world': {'tribal': "stand at the keepers' fire and ask, before them all, where the gifts went", 'magic': "stand up in the order's council and ask, on the record, where the alms went"}, 'chance': 0.54}),
    ('make the fund good from your own savings, so the poor go short of nothing', 'U.34 B.33 G.33', None, 0.5, '', {'self_control': '+', 'v': 'benevolence, security', 'world': {'tribal': 'give furs and meat from your own hearth, so the hungry go short of nothing', 'magic': 'make the alms good from your own purse, so the poor go short of nothing'}, 'chance': 0.9}),
    ('sit with the colleague, hear why, and help them own up to the congregation', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, stimulation', 'world': {'tribal': 'sit with the keeper, hear why, and help them own it before the band', 'magic': 'sit with the priest, hear why, and help them own it before the faithful'}, 'chance': 0.57}),
 ]},
{'name': 'a sermon that goes round the country',
 'stages': 'adult mature elder',
 'age': (25, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'faith.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.01, 0.005),
 'drivers': 'era+.2 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'faith, publiclife',
 'horizon': 'week',
 'roles': 'friend, boss, mentor, colleague, rival',
 'requires': 'ordained religious minister | lay religious teacher | street preacher',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'someone films a sermon on a phone, by the end of the week it has gone round the whole country, '
                     "and the faith's leaders are writing",
            'tribal': 'a telling at the fire is carried by traders from band to band down the whole river, and the '
                      'keepers of far bands send for the one who spoke it',
            'magic': 'a sermon preached in a small chapel is copied by the printers and read aloud in every city of '
                     'the realm, and letters come from the great temples'},
 'timing': {'times': 'per minister, lay teacher or street preacher with three years or more behind them, a year: '
                     'about 1 in 100 has a sermon or a talk recorded and shared far beyond their own congregation '
                     '(estimate); sermons and talks are shared online by the thousand every week, and only a handful '
                     "a year lead to a great congregation's call or to ordination (estimate); about 4 lives in 1,000 "
                     'are ministers, 3 in 100 lay teachers of the faith and 5 in 1,000 street preachers (catalogue '
                     'shares)',
            'likelier': 'a sermon on something everyone is feeling that week, someone in the seats who films it '
                        'well, years of preaching behind it, a time when people are looking for words',
            'rarer': 'a quiet week, a sermon only the congregation would understand, a preacher nobody records',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       "On an ordinary rest day {N} spoke about the flood that had taken half the town's houses that "
                       'month: twelve minutes, no notes, on what people owe each other when the water comes. '
                       '{friend} filmed it on a phone and posted it that night. By Friday it has been watched two '
                       'million times, a newspaper has rung, and two letters lie on the table: one from a great '
                       "congregation in the city, one from the faith's leaders, who would like to talk about {Ns} "
                       'future.'),
                      ('W',
                       "{N} reads the faith's letter twice. It asks for a meeting, properly, and talks about "
                       'training and a future in the faith. {N} would like to answer it properly too.'),
                      ('U',
                       '{N} watches the sermon for the first time and tries to see what two million people heard in '
                       'it: the plainness, perhaps, or the timing. It is worth understanding before saying anything '
                       'else.'),
                      ('B',
                       'Attention like this lasts a fortnight, and letters like these do not come twice. {N} knows '
                       'which one leads further.'),
                      ('R',
                       '{N} still means every word of it, and the hundreds of messages from strangers make {N} want '
                       'to preach it again tomorrow, louder.'),
                      ('G',
                       "The people in the sermon are the town's own: the baker who opened her shop to the flooded, "
                       'the farmer with the tractor. {N} thinks the sermon belongs to them more than to anyone.')],
            'tribal': [('',
                        '{N} spoke at the fire of the flood that took the low camp, and of what each hearth owes the '
                        'others when the water comes. Traders carried the telling down the river, and now runners '
                        'come from far bands: their keepers of the rites want to hear the one who spoke it.')],
            'magic': [('',
                       '{N} preached in a small chapel on the flood that took the lower town, and a clerk copied it '
                       'down. The printers have sold it in every city of the realm, and two letters lie on the '
                       "table: one from a great temple of the capital, one from the order's council.")]},
 'outcomes': (['Within a month the letter that matters has a date in it, and {N} stands in a much larger room, with '
               'the same twelve minutes still going round.',
               'Whatever {N} chose, the sermon goes on doing good where it landed, and {N} is glad to have preached '
               'it.'],
              ["The talk dies down after ten days, something else takes everyone's attention, and the meeting with "
               "the faith's leaders is warm and comes to nothing.",
               'The panel listens politely and says {N} is a wonderful preacher, which is not the same as a yes.']),
 'options': [
    ("answer the faith's letter, and begin the full training for ordination", 'W1', None, 0.45, '', {'title': 'ordained religious minister', 'requires': 'lay religious teacher', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'v': 'conformity, tradition', 'world': {'tribal': "answer the keepers' runner, and begin the old shaman's long years of teaching", 'magic': "answer the order's letter, and enter the temple school for the full training"}, 'chance': 0.03}),
    ('turn the sermon into a careful series, and answer the city congregation with it', 'U1', None, 0.45, '', {'title': 'senior cleric', 'requires': 'ordained religious minister', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'achievement, self-direction', 'world': {'tribal': 'make the telling into a cycle for the long nights, and answer the far keepers with it', 'magic': 'turn the sermon into a careful cycle, and answer the great temple with it'}, 'chance': 0.03}),
    ("use the fortnight of fame to win the city congregation's senior post", 'B1', None, 0.45, '', {'title': 'senior cleric', 'requires': 'ordained religious minister', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': "use the moon when every fire knows the name to win the far keepers' great rites", 'magic': "use the season of fame to win the great temple's call"}, 'chance': 0.03}),
    ("say yes to the faith's call to train, and keep preaching in the street meanwhile", 'R1', None, 0.45, '', {'binds': True, 'title': 'ordained religious minister', 'requires': 'street preacher', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, self-direction', 'world': {'tribal': "say yes to the keepers' call, and go on speaking at every fire on the way", 'magic': "say yes to the order's call to train, and keep preaching in the market meanwhile"}, 'chance': 0.03}),
    ('ask the city congregation to come and worship with the flooded town first', 'G1', None, 0.45, '', {'title': 'senior cleric', 'requires': 'ordained religious minister', 'without': 'impossible', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': "ask the far keepers to come to the low camp's fire first, among the flooded hearths", 'magic': "ask the great temple's priests to come and pray with the flooded town first"}, 'chance': 0.03}),
    ('write the sermon out plainly as a booklet for the congregation, and leave it there', 'W.34 U.33 G.33', None, 0.5, '', {'grants': 'good name in town', 'v': 'tradition, universalism', 'world': {'tribal': "teach the telling to the band's own old ones, so it stays at the home fire", 'magic': "write the sermon out plainly for the chapel's faithful, and leave it there"}, 'chance': 0.84}),
    ("let the faith's own office put it out properly, with talks booked across the country", 'W.34 B.33 R.33', None, 0.5, '', {'grants': 'following online', 'v': 'achievement, conformity', 'world': {'tribal': 'let the keepers send the telling on properly, from fire to fire, with a night set for each band', 'magic': "let the order's printers put it out properly, with sermons booked in three cities"}, 'chance': 0.84}),
    ("give the talks it brings, but only in towns within a day's journey", 'W.34 B.33 G.33', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': "speak at the fires it brings, but only of the bands within a day's walk", 'magic': "preach where it brings the call, but only in towns within a day's ride"}, 'chance': 0.84}),
    ('give everything the sermon brings in to the flooded families, and say so', 'U.34 R.33 G.33', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': 'give every gift the telling brings to the flooded hearths, and say so at the fire', 'magic': 'give every coin the sermon brings to the flooded families, and say so from the pulpit'}, 'chance': 0.84}),
    ('answer the messages for one week, then switch the phone off and go back to work', 'U.34 B.33 R.33', None, 0.5, '', {'v': 'self-direction, security', 'world': {'tribal': "sit with the runners for one moon, then send them home and go back to the band's rites", 'magic': 'answer the letters for one week, then shut the door and go back to the chapel'}, 'chance': 0.84}),
 ]},
{'name': 'the god speaks in the temple',
 'stages': 'adult mature elder',
 'age': (45, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'faith.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': 'fortune+.2 community+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'faith, publiclife',
 'horizon': 'months',
 'roles': 'boss, rival, mentor, colleague',
 'requires': 'senior cleric | ordained religious minister',
 'tenure': (3.0, 99.0),
 'worlds': {'magic': "the temple's oracle says the god has chosen a new high priest, and will speak the chosen name "
                     'to the council for a price'},
 'only': 'magic',
 'timing': {'times': 'per priest of a great temple, or priest of ten years, in the magic world a year: about 1 in 60 '
                     'is at the temple when the oracle says the god has chosen a new high priest (estimate); in many '
                     'old faiths an oracle or a sign was asked before a high priest was chosen, and the council did '
                     'not always follow it (estimate); about 5 lives in 10,000 are priests of a great temple '
                     '(catalogue share)',
            'likelier': 'an old high priest failing, a priest known for devotion, a feast year, a council already '
                        'divided',
            'rarer': "a young high priest in good health, a temple far from the god's seat, a priest the oracle has "
                     'spoken against',
            'gap_years': (8.0, 20.0)},
 'scenes': {'magic': [('',
                       'On the feast of the god the oracle in the inner court goes into her trance before the whole '
                       'temple and speaks: the god has chosen a new high priest from among those present, and will '
                       'make the choice known. That night a temple servant brings {N} word that the oracle will '
                       'speak {Ns} name to the council, for a price she will name herself. {rival}, it is whispered, '
                       "has already been to her. The order's council meets at the new moon."),
                      ('W',
                       'The order chooses its high priest by its council and its law, and the god has always spoken '
                       'through that law. {N} is uneasy at any word that comes round the side of it.'),
                      ('U',
                       "Oracles have spoken before, and the council's archive records how often their words came "
                       'true. {N} goes down to the archive that night to read them.'),
                      ('B',
                       'The price will be high, and so is the seat. {N} weighs what the oracle could ask, and what a '
                       'high priest could pay back.'),
                      ('R',
                       '{N} felt something in the court when the oracle spoke, a stillness like the moment before a '
                       'storm. Whatever it was, {N} wants to meet it head on.'),
                      ('G',
                       'The god chose the grandmother of {Ns} grandmother to serve, the family says, and the god '
                       'chooses in its own seasons. {N} would rather wait for the god than buy its word.')]},
 'outcomes': (['At the new moon the council chooses, the bells ring across the city, and the temple settles into the '
               "new high priest's years.",
               "Whatever {N} chose, the season of the oracle passes, and the order's council does its work in "
               'peace.'],
              ["The council chooses {rival}, and nobody speaks of the oracle's word again.",
               "The oracle's season splits the council, the choosing drags on for a year, and {N} is left out of the "
               'end of it.']),
 'options': [
    ("wait for the council's vote, and stand by the order's law of choosing", 'W1', None, 0.45, '', {'identity': True, 'title': 'head of a faith order', 'requires': 'senior cleric', 'without': 'impossible', 'v': 'conformity, tradition', 'chance': 0.06}),
    ("read the archive's record of every oracle, and lay the truth of it before the council", 'U1', None, 0.45, '', {'self_control': '+', 'title': 'head of a faith order', 'requires': 'senior cleric', 'without': 'impossible', 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'chance': 0.06}),
    ("pay the oracle's price, and let her speak your name to the council", 'B1', None, 0.45, '', {'title': 'head of a faith order', 'requires': 'senior cleric', 'without': 'impossible', 'mark': 'hid a wrong', 'closed': "approval: the oracle's price, paid behind the council's back; backfire: the god's favour is a debt, and in the first year the oracle comes to collect it", 'self_control': '-', 'v': 'power, achievement', 'chance': 0.15}),
    ('stand before the oracle in the inner court, and ask the god to its face', 'R1', None, 0.45, '', {'title': 'head of a faith order', 'requires': 'senior cleric', 'without': 'impossible', 'v': 'stimulation, self-direction', 'chance': 0.06}),
    ("go on with the daily offices, and leave the choice to the god's own season", 'G1', None, 0.45, '', {'title': 'head of a faith order', 'requires': 'senior cleric', 'without': 'impossible', 'v': 'tradition, benevolence', 'chance': 0.06}),
    ('put forward an older and better priest, and stand at their right hand', 'B.5 G.5', None, 0.5, '', {'door': True, 'grants': 'friend in power', 'v': 'benevolence, security', 'chance': 0.66}),
    ('spend the month before the council praying and listening in the temple garden', 'U.5 G.5', None, 0.5, '', {'habit': True, 'v': 'tradition, self-direction', 'chance': 0.84}),
    ('find out who has paid the oracle before, and say so in open council', 'U.5 R.5', None, 0.5, '', {'mark': 'made an enemy', 'v': 'universalism, stimulation', 'chance': 0.66}),
    ("ask the council to rule that no oracle's word may decide the choosing", 'W.5 B.5', None, 0.5, '', {'v': 'conformity, power', 'chance': 0.66}),
    ('refuse openly to serve any high priest whose seat was bought from an oracle', 'W.5 R.5', None, 0.5, '', {'mark': 'defied an authority', 'v': 'universalism, conformity', 'chance': 0.84}),
 ]},
{'name': 'the birth that will not wait',
 'stages': 'young_adult adult mature elder',
 'age': (20, 75),
 'alpha': 'W.1 U.1 B.1 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, family',
 'horizon': 'moment',
 'roles': 'colleague, mentor',
 'requires': 'nurse | midwife | care worker | paramedic',
 'worlds': {'earth': 'a farmhouse at the top of a lane the snowplough has not reached, and a baby coming two weeks '
                     'early, an hour before any ambulance can',
            'tribal': "the band moving camp through the first snow, and a young mother's pains coming fast, a day's "
                      'walk from the birth shelter',
            'magic': "a coaching inn cut off by snow on the high road, and the innkeeper's daughter's baby coming "
                     "early, a day's ride from the temple house"},
 'timing': {'times': 'per nurse, midwife, care worker or paramedic a year: about 1 in 30 is there when a baby comes '
                     'too fast to reach the hospital or the midwife, paramedics and midwives most often (estimate); '
                     'about 1 birth in 200 comes before the mother reaches help (estimate); about 3 lives in 100 are '
                     'nurses, 8 in 100 care workers, 4 in 1,000 paramedics and 1 in 1,000 midwives (catalogue '
                     'shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       '{N} is on the last home visit of the day, at a farm at the top of a lane the snowplough has '
                       "not reached, when the old farmer's granddaughter, staying for the winter, goes into labour "
                       'two weeks early. The pains are already close together. The ambulance says an hour at best, '
                       'and the only thing in the kitchen that is ready is the kettle.'),
                      ('W',
                       'The emergency line has a script for this, and {N} has done the course. Clean towels, gloves, '
                       'the time written down: there is an order to things, even on a kitchen floor.'),
                      ('U',
                       "{N} counts the minutes between the pains and watches the young woman's face. The numbers say "
                       'this baby will not wait for any ambulance.'),
                      ('B',
                       "Somebody has to run this kitchen for the next hour. The farmer is shaking, the young woman's "
                       'partner is on the phone to his mother, and {N} is the only one in the room who has seen a '
                       'birth.'),
                      ('R',
                       '{Ns} heart is going like a drum, and that is fine. The baby is coming, {N} is here, and '
                       'nothing else matters now.'),
                      ('G',
                       'Babies have been born in farm kitchens for as long as there have been farms. The stove is '
                       'warm, the snow is quiet, and her body knows what it is doing.')],
            'tribal': [('',
                        'The band is moving camp along the river in the first snow when a young mother sits down '
                        "hard on the path, her pains coming fast. The birth shelter is a day's walk behind them, and "
                        '{N}, who has helped at many births, kneels beside her while the others pile up wood for a '
                        'fire.')],
            'magic': [('',
                       'Snow has closed the high road, and the coaching inn is full of stranded travellers when the '
                       "innkeeper's daughter's waters break, a fortnight early. The temple house is a day's ride "
                       'away, and {N}, a nurse of its wards on the way home, is the only healer under the roof.')]},
 'outcomes': (['The baby comes crying and strong, and mother and baby are warm and well long before help arrives.',
               'Within the week everyone around has heard the story, and the new mother asks for {N} by name.'],
              ['It is a frightening hour and a messy one, but mother and baby are both well when help comes.',
               'Others take over at the last minute and {Ns} part is lost in the rush, though mother and baby are '
               'both well.']),
 'options': [
    ('ring the emergency line, and do each thing the call handler says, in order', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'send a runner back for the old birth-keeper, and do each thing as she taught, in order', 'magic': 'send the stable boy riding for the temple house, and do each thing as the old midwives teach'}, 'chance': 0.8}),
    ('time the pains, and feel how the baby lies, before deciding anything', 'U1', None, 0.45, '', {'v': 'achievement, security', 'chance': 0.75}),
    ('take charge of the kitchen, and give everyone in the house a job', 'B1', None, 0.45, '', {'v': 'power, security', 'aims': 'senior nurse or midwife', 'world': {'tribal': 'take charge of the path, and give everyone in the band a job', 'magic': "take charge of the inn's kitchen, and give every stranded traveller a job"}, 'chance': 0.75}),
    ('kneel on the kitchen floor, and catch the baby there and then', 'R1', None, 0.45, '', {'v': 'stimulation, benevolence', 'body': 'light', 'grants': 'emergency care', 'world': {'tribal': 'kneel in the snow by the new fire, and catch the baby there and then', 'magic': "kneel on the inn's hearth, and catch the baby there and then"}, 'chance': 0.7}),
    ('keep her warm by the stove, and let the birth come at its own pace', 'G1', None, 0.45, '', {'v': 'benevolence, tradition', 'self_control': '+', 'grants': 'families who send for you', 'world': {'tribal': 'keep her warm by the fire under the furs, and let the birth come in its own time', 'magic': "keep her warm by the inn's hearth, and let the birth come at its own pace"}, 'chance': 0.75}),
    ('write the birth up for the hospital that night, with your name and every time', 'W1', 'B.7', 0.5, '', {'v': 'achievement, conformity', 'aims': 'senior nurse or midwife', 'world': {'tribal': 'tell the birth at the fire that night, step by step, so the elders know whose hands did it', 'magic': 'write the birth up for the temple house that night, with your name and every hour'}, 'chance': 0.6}),
    ('judge from the pains that there is still time, and drive her down the lane', 'U1', 'R.7', 0.5, '', {'v': 'stimulation, self-direction', 'world': {'tribal': 'judge from the pains that there is still time, and walk her on to the birth shelter', 'magic': 'judge from the pains that there is still time, and drive her down to the village in the sleigh'}, 'chance': 0.65}),
    ('phone the farmer down the valley, and talk him into clearing the lane with his tractor', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'mark': 'made a friend', 'world': {'tribal': "send word to the next band's hunters, and talk them into breaking a trail through the snow", 'magic': 'talk the stranded carters into digging the road out to the village'}, 'chance': 0.65}),
    ('send everyone out of the kitchen, loudly, and stand guard at the door', 'R1', 'W.7', 0.5, '', {'v': 'security, benevolence', 'world': {'tribal': 'send the band on ahead, loudly, and keep a quiet ring round the mother', 'magic': 'send the gawping travellers out of the kitchen, loudly, and stand guard at the door'}, 'chance': 0.7}),
    ('let her body lead, and note every sign for the midwives who come after', 'G1', 'U.7', 0.5, '', {'v': 'universalism, achievement', 'world': {'tribal': 'let her body lead, and remember every sign to tell the old birth-keeper', 'magic': "let her body lead, and note every sign for the temple's midwives"}, 'chance': 0.65}),
 ]},
{'name': 'the ward is two nurses short',
 'stages': 'young_adult adult mature elder',
 'age': (20, 75),
 'alpha': 'W.4 U.4 B.4 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, health',
 'horizon': 'week',
 'roles': 'colleague, boss',
 'requires': 'nurse | midwife | care worker | paramedic',
 'worlds': {'earth': 'the night shift on a ward of twenty-eight beds, two nurses short again, and the agency has '
                     'nobody to send',
            'tribal': 'the sickness shelter in the deep of winter, the sick laid close by the fire, and only two '
                      'pairs of hands to tend them through the night',
            'magic': 'the long ward of the temple house at night, two sisters down with the cough, and every bed '
                     'full'},
 'timing': {'times': 'per nurse, midwife, care worker or paramedic a year: about 1 in 2 work a night short of staff '
                     'at least once, and many work one every month (staff surveys; estimate); about 3 lives in 100 '
                     'are nurses and 8 in 100 care workers (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "Eight o'clock at night, and all twenty-eight beds on the ward are full. The rota says four "
                       'nurses; there are two, and {colleague} qualified a month ago. The agency has nobody to send, '
                       "the manager's phone goes to voicemail, and the drug round starts in half an hour."),
                      ('W',
                       'Every patient has checks due every four hours, and a box for each on the chart. Tonight '
                       'there are not enough hands to fill them all, and {N} knows what an empty box can mean.'),
                      ('U',
                       'Twenty-eight patients, two nurses, twelve hours. {N} is already working out which ones need '
                       'watching every hour and which can safely sleep.'),
                      ('B',
                       'This is the third short night this month, and every one of them was signed off upstairs as '
                       'fine. Someone up there is counting on nobody making a fuss.'),
                      ('R',
                       '{Ns} legs are tired already, and the night has not started. There is nothing for it but to '
                       'go, and keep going.'),
                      ('G',
                       'The old man in bed six cannot settle unless someone sits with him a while, and the woman in '
                       'bed nine is frightened of the dark. No chart on the ward says so.')],
            'tribal': [('',
                        'Deep in the winter the sick of the band lie close by the fire in the sickness shelter: an '
                        "old woman with a cough, a hunter with a hurt leg, a mother with a fever. Two of the band's "
                        'healers are down with it themselves, and {N} and {colleague} are the only hands left to '
                        'tend them through the long night.')],
            'magic': [('',
                       "Every bed in the temple house's long ward is full, and two of the sisters are down with the "
                       "cough. The night matron has gone to the city on the temple's business, and {N} and "
                       '{colleague} have the whole ward between them until dawn.')]},
 'outcomes': (["Dawn comes, every patient is safe, and the day staff find the night's work done.",
               'The night is hard but it holds, and the next week someone finally finds more hands for the nights.'],
              ['The night holds, just, and {N} goes home grey with tiredness, knowing it will happen again before '
               'the month is out.',
               'Something small is missed in the rush, nobody is harmed, and the morning brings a hard '
               'conversation.']),
 'options': [
    ("sign the night's checks as done, so every chart is complete by morning", 'W1', None, 0.45, '', {'v': 'conformity, security', 'mark': 'hid a wrong', 'self_control': '-', 'closed': 'approval: checks signed that were not done; backfire: the audit finds the gaps, and the ward manager asks who signed them', 'world': {'tribal': 'tell the elders at dawn that every one of the sick was tended through the night', 'magic': 'sign the night book as if every round was made'}, 'chance': 0.8}),
    ('rank the patients by need, and plan the whole night hour by hour', 'U1', None, 0.45, '', {'v': 'achievement, security', 'grants': 'organising people', 'world': {'tribal': 'rank the sick by need, and plan the whole night by the stars'}, 'chance': 0.75}),
    ('refuse to take more admissions until the ward has the staff it needs', 'B1', None, 0.45, '', {'v': 'power, security', 'mark': 'defied an authority', 'world': {'tribal': 'tell the elders no more of the sick may come to the shelter until there are more hands', 'magic': 'refuse the steward any more patients until the ward has the sisters it needs'}, 'chance': 0.7}),
    ('work straight through the night with no break, and cover both bays', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'body': 'light', 'self_control': '+', 'grants': 'used to night shifts', 'world': {'tribal': 'tend the sick straight through the night with no rest, both sides of the fire', 'magic': 'work straight through the night with no rest, and cover both ends of the ward'}, 'chance': 0.75}),
    ('sit with the frightened ones first, and let the paperwork wait', 'G1', None, 0.45, '', {'v': 'benevolence, universalism', 'self_control': '-', 'world': {'tribal': 'sit with the frightened ones first, and let the rest wait their turn', 'magic': 'sit with the frightened ones first, and let the ward book wait'}, 'chance': 0.7}),
    ('fill in the staffing report in full, and send it to the director', 'W1', 'B.7', 0.5, '', {'v': 'conformity, power', 'aims': 'senior nurse or midwife', 'world': {'tribal': 'tell the elders plainly at the fire how few hands there were, and ask for more', 'magic': "write the night's shortfall in the matron's book, and send it to the temple's steward"}, 'chance': 0.6}),
    ("agree a signal with the other nurse, so either can run to the other's bay", 'U1', 'R.7', 0.5, '', {'v': 'self-direction, stimulation', 'world': {'tribal': "agree a call with the other healer, so either can run to the other's side of the fire", 'magic': "agree a signal with the other sister, so either can run to the other's end of the ward"}, 'chance': 0.65}),
    ('call in a favour from the next ward, and borrow a nurse for the drug round', 'B1', 'G.7', 0.5, '', {'v': 'benevolence, power', 'world': {'tribal': 'call in a favour from the next hearth, and borrow a pair of hands for the night', 'magic': "call in a favour from the sisters' wing, and borrow a nurse for the medicine round"}, 'chance': 0.7}),
    ('tell the bed manager to their face that the ward is not safe tonight', 'R1', 'W.7', 0.5, '', {'v': 'security, universalism', 'mark': 'defied an authority', 'world': {'tribal': 'tell the eldest to their face that the sick are not safe with so few hands', 'magic': 'tell the steward to their face that the ward is not safe tonight'}, 'chance': 0.65}),
    ('show the families staying late how to help with drinks and meals', 'G1', 'U.7', 0.5, '', {'v': 'benevolence, universalism', 'door': True, 'world': {'tribal': 'show the kin sitting by the fire how to help with water and broth'}, 'chance': 0.7}),
 ]},
{'name': 'a family asks you to stay to the end',
 'stages': 'adult mature elder',
 'age': (26, 75),
 'alpha': 'W.4 U.4 B.1 R.1 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'week',
 'roles': 'colleague, mentor',
 'requires': 'senior nurse or midwife',
 'worlds': {'earth': 'an old patient near the end of a long illness, and a daughter who asks the senior nurse to be '
                     'there when it comes',
            'tribal': 'an old hunter of the band near the end of a long sickness, and his kin asking the '
                      'birth-keeper to sit with them through his last nights',
            'magic': 'an old woman in the quiet room of the temple house, near the end of a long illness, and her '
                     'son asking the healer to stay'},
 'timing': {'times': 'per senior nurse or midwife a year: about 1 in 4 are asked by a family to be with them at the '
                     'end (estimate); about half of all deaths in rich countries come after a long illness, in a '
                     'hospital, a hospice or a care home (estimate); about 4 lives in 1,000 are senior nurses or '
                     'midwives (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The old woman in the side room has been on the ward five weeks, and the end of her long '
                       'illness is close now: a day, perhaps two. She sleeps most of the time and is in no pain. Her '
                       "daughter finds {N} at the nurses' station, holding a cup of tea she has forgotten to drink, "
                       'and asks whether {N} will be there when it comes.'),
                      ('W',
                       'There is a plan for the last days, and {N} wrote most of it: comfort, mouth care, the '
                       "family's wishes, the words of their faith if they want them. A plan like that deserves to be "
                       'kept well.'),
                      ('U',
                       '{N} has seen many deaths and knows the signs: the breathing that changes, the hands that '
                       'cool. The family does not, and not knowing frightens them more than anything.'),
                      ('B',
                       'The bed managers want the side room for a new admission and have asked twice today. {N} has '
                       'the seniority to say no, and means to use it.'),
                      ('R',
                       '{N} liked her from the first day: the jokes about the food, the stories about dancing when '
                       'she was young. The ward will be quieter without her.'),
                      ('G',
                       'Eighty-nine years, and now her life is coming to its end the way lives do. {N} wants the end '
                       'to be quiet, and warm, and among her own.')],
            'tribal': [('',
                        'The old hunter has lain in his shelter since the first frosts, growing lighter every day, '
                        'and now he sleeps more than he wakes, without pain. His sons and daughters sit round the '
                        "fire outside, and the eldest daughter comes to {N}, the band's birth-keeper and first "
                        'healer, and asks {N} to sit with them through the last nights.')],
            'magic': [('',
                       "In the quiet room at the end of the temple house's long ward, an old woman of the town has "
                       'come to the last days of a long illness, peaceful and without pain. Her family keep watch by '
                       'the window, and her son asks {N}, a healer of the temple house, whether {N} will stay with '
                       'them when the time comes.')]},
 'outcomes': (['The end comes quietly in the early hours, with the family close, and nobody is alone.',
               'Some weeks later the family sends word of thanks, and it names {N}.'],
              ['The end comes peacefully on a night {N} is not there, and the family is sorry, and grateful all the '
               'same.',
               'The last days are calm, but the family quarrels in the corridor, and {N} cannot mend it.']),
 'options': [
    ('keep to her care plan hour by hour, and hold the night staff to it', 'W1', None, 0.45, '', {'v': 'conformity, benevolence', 'habit': True, 'world': {'tribal': 'tend him by the old ways hour by hour, and hold the other healers to them', 'magic': "keep to the temple's rule for the dying hour by hour, and hold the night sisters to it"}, 'chance': 0.75}),
    ('explain to the family plainly what each change means, and what comes next', 'U1', None, 0.45, '', {'v': 'benevolence, universalism', 'grants': 'calming people down', 'world': {'tribal': 'tell his kin plainly what each change means, and what comes next'}, 'chance': 0.75}),
    ('use your seniority to keep the side room, whatever the bed managers say', 'B1', None, 0.45, '', {'v': 'power, benevolence', 'world': {'tribal': 'use your standing to keep the shelter quiet and unmoved, whatever the hunters say about breaking camp', 'magic': 'use your standing to keep the quiet room, whatever the steward says about beds'}, 'chance': 0.8}),
    ('stay on through the night in your own time, holding her hand', 'R1', None, 0.45, '', {'v': 'benevolence', 'grants': 'families who send for you', 'aims': 'renowned healer', 'world': {'tribal': 'stay through the night at his side, holding his hand'}, 'chance': 0.9}),
    ('dim the lights, open the window, and let the family sit close in their own way', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'open the shelter to the night air, and let his kin sit close in their own way', 'magic': 'dim the lamps, open the window, and let the family sit close in their own way'}, 'chance': 0.75}),
    ("ask the family's own minister or elder in, as the family wishes", 'W1', 'G.7', 0.5, '', {'v': 'tradition, conformity', 'door': True, 'world': {'tribal': 'ask the keeper of the rites to come and sing the old songs over him, as his kin wish', 'magic': "send for the family's own priest, as they wish"}, 'chance': 0.65}),
    ('write a plan for her last nights that the night staff can follow exactly', 'U1', 'W.7', 0.5, '', {'v': 'security, conformity', 'aims': 'renowned healer', 'world': {'tribal': 'teach the other healers each thing to do in his last nights, so it is done right', 'magic': 'write a plan for her last nights that the night sisters can follow exactly'}, 'chance': 0.65}),
    ("call in a favour, and bring the hospice's specialist nurse to the bedside tonight", 'B1', 'U.7', 0.5, '', {'v': 'security, achievement', 'door': True, 'world': {'tribal': 'send for the old healer of the next band, who knows best how to ease the last nights', 'magic': "call in a favour, and bring the temple's most learned herb-healer to the bedside tonight"}, 'chance': 0.6}),
    ("tell her story at the managers' meeting, and win the ward a proper quiet room", 'R1', 'B.7', 0.5, '', {'v': 'achievement, benevolence', 'world': {'tribal': "tell his story at the elders' fire, and win the sick a shelter of their own, away from the noise", 'magic': 'tell her story to the temple council, and win the ward a quiet room of its own'}, 'chance': 0.5}),
    ('help the family bring in her old dog and the songs she loved', 'G1', 'R.7', 0.5, '', {'v': 'hedonism, benevolence', 'mark': 'helped someone in need', 'world': {'tribal': 'help his kin bring in his old hunting dog and sing the songs he loved', 'magic': 'help the family bring in her old cat and the songs she loved'}, 'chance': 0.65}),
 ]},
{'name': 'the managers want the birth centre closed',
 'stages': 'adult mature elder',
 'age': (26, 75),
 'alpha': 'W.1 U.1 B.4 R.4 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, community',
 'horizon': 'months',
 'roles': 'boss, colleague',
 'requires': 'senior nurse or midwife',
 'worlds': {'earth': "the hospital's managers plan to close the small birth centre in town and send every birth to "
                     'the big unit in the city, forty minutes away',
            'tribal': "the elders talk of giving up the birth shelter by the spring, and sending the band's mothers "
                      "to the big camp's healers downriver",
            'magic': 'the temple council means to shut the birthing house in the lower town, and send every mother '
                     'up the hill to the great temple'},
 'timing': {'times': 'per senior nurse or midwife a year: about 1 in 15 see their own unit, a small birth centre or '
                     'a ward, put up for closing or merging (estimate); small midwife-led birth centres open and '
                     'close with each round of budgets (estimate); about 4 lives in 1,000 are senior nurses or '
                     'midwives (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       "The letter comes on a Monday: after a review, the managers propose to close the town's small "
                       'birth centre and send every birth to the big unit in the city, forty minutes away by road. '
                       '{boss} calls it a consultation. Seven hundred babies were born in the centre last year, and '
                       "half the town's families know {N} by name."),
                      ('W',
                       'There is a proper process for this: a consultation, a safety review, a vote of the board. '
                       '{N} means to answer every page of it.'),
                      ('U',
                       "{N} has read the review's figures, and they leave things out: the forty-minute drive in "
                       'winter, the mothers whose babies come fast.'),
                      ('B',
                       'The managers want a saving they can show the board. {N} knows the councillors, the editor of '
                       'the local paper and two of the board by name.'),
                      ('R',
                       '{N} reads the letter twice, and then has to go and stand outside in the car park for a '
                       'while.'),
                      ('G',
                       'Three generations of the town were born in that building. Families who never set foot in the '
                       'city bring their babies back to show the midwives.')],
            'tribal': [('',
                        'The elders talk at the fire of giving up the birth shelter in the willows by the spring, '
                        "where the band's mothers have had their babies for longer than anyone remembers, and "
                        "sending the mothers to the big camp's healers downriver instead. {boss}, the eldest, says "
                        'it would be one shelter fewer to keep.')],
            'magic': [('',
                       'The temple council writes that the old birthing house in the lower town costs too much in '
                       'silver and lamp oil, and that from midsummer every mother of the town must climb the hill to '
                       "the great temple to give birth. {boss}, the council's steward, calls it a kindness.")]},
 'outcomes': (["The managers put the closing off for a year, and the centre's lights stay on.",
               'Whatever {N} chose, the mothers of the town still have somewhere near home to give birth.'],
              ['The centre closes by the summer, and the mothers of the town must go further to give birth.',
               'The fight drags on for months and wears everyone thin, and nothing is settled.']),
 'options': [
    ('answer the consultation point by point, through every proper channel', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': "speak at the elders' fire in your turn, as the custom is, for keeping the shelter", 'magic': "answer the council's letter point by point, through every proper channel"}, 'chance': 0.7}),
    ('work out what the long drive would mean in winter, and publish the figures', 'U1', None, 0.45, '', {'v': 'universalism, achievement', 'identity': True, 'world': {'tribal': "count the days' walk to the big camp in deep snow, and lay it out for the elders", 'magic': 'reckon the climb up the hill in winter for every mother, and set it before the council'}, 'chance': 0.75}),
    ("leak the managers' review to the local paper before the consultation opens", 'B1', None, 0.45, '', {'v': 'power', 'mark': 'defied an authority', 'closed': "approval: a confidential review leaked; backfire: the managers trace the leak, and a written warning goes on the senior nurse's record", 'world': {'tribal': "tell the other bands' elders what this band's elders plan, before they can decide it", 'magic': "pass the council's letter to the broadsheet printers before the council can meet"}, 'chance': 0.75}),
    ('stand up at the public meeting, and say unscripted what the centre means', 'R1', None, 0.45, '', {'v': 'self-direction, universalism', 'identity': True, 'world': {'tribal': "stand up at the band's fire, and say from the heart what the shelter means", 'magic': "stand up at the town's open meeting, and say from the heart what the birthing house means"}, 'chance': 0.8}),
    ('ask the families born there to come and tell the managers their own stories', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'grants': 'organising people', 'world': {'tribal': 'ask the families born in the shelter to come to the fire and tell their own stories', 'magic': 'ask the families born there to come before the council and tell their own stories'}, 'chance': 0.75}),
    ('draw up a plan for a smaller centre run by the midwives, within every rule', 'W1', 'G.7', 0.5, '', {'v': 'security, tradition', 'world': {'tribal': 'ask the elders for a smaller shelter by the spring, kept by the old women in the proper way', 'magic': "draw up a plan for a smaller birthing house run by the midwives, within the temple's rules"}, 'chance': 0.7}),
    ("redesign the centre's rota so it costs less and meets every standard", 'U1', 'W.7', 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'work out how the shelter can be kept with fewer hands and every custom still kept', 'magic': "redesign the birthing house's watches so they cost less and keep every rule"}, 'chance': 0.65}),
    ('strike a deal with the university to run the centre as a teaching unit', 'B1', 'U.7', 0.5, '', {'v': 'achievement, power', 'binds': True, 'world': {'tribal': "strike a bargain with the big camp's healers to send their young ones to learn at the shelter", 'magic': "strike a bargain with the apothecaries' college to train its students at the birthing house"}, 'chance': 0.65}),
    ('open a birth centre of your own, with the midwives who would lose theirs', 'R1', 'B.7', 0.5, '', {'v': 'self-direction, achievement', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'grants': 'a clinic of your own', 'binds': True, 'aims': 'renowned healer', 'world': {'tribal': "build a healer's lodge of your own by the spring, with the old women who would lose the shelter", 'magic': 'open a house of healing of your own in the lower town, with the midwives who would lose theirs'}, 'chance': 0.6}),
    ('start a home-birth service for the town, run from your own car', 'G1', 'R.7', 0.5, '', {'v': 'self-direction, tradition', 'world': {'tribal': 'go out to the mothers in their own shelters, wherever the band makes camp', 'magic': 'go out to the mothers in their own houses, with your bag and your lamp'}, 'chance': 0.65}),
 ]},
{'name': 'the ward needs someone in charge',
 'stages': 'adult mature',
 'age': (26, 67),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.06, 0.04, 0.0),
 'drivers': 'prosper+.1 community+.2',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work',
 'horizon': 'months',
 'roles': 'mentor, colleague, rival, boss',
 'requires': 'nurse | midwife',
 'tenure': (4.0, 100.0),
 'worlds': {'earth': 'the ward manager retires, and the post of the one in charge of the ward is advertised',
            'tribal': 'the old birth-keeper of the band can no longer walk to the births, and the women ask who will '
                      'keep the births and the sick after her',
            'magic': "the old matron of the temple house's long ward goes to her rest, and the council asks who will "
                     'keep the ward after her'},
 'timing': {'times': 'per nurse or midwife of four years or more a year: about 1 in 20 see the post of ward manager, '
                     'charge nurse or lead midwife open where they work, and weigh going for it (estimate); about 1 '
                     'registered nurse or midwife in 8 reaches that grade (workforce statistics), about 4 lives in '
                     '1,000 (catalogue share)',
            'likelier': 'a manager retiring, a new ward or birth centre opening, good years with money for posts, a '
                        'team that wants one of its own',
            'rarer': 'a freeze on posts, a manager who stays for twenty years, a hospital closing beds',
            'gap_years': (2.0, 5.0)},
 'scenes': {'earth': [('',
                       '{mentor}, who has run the ward for nineteen years, retires at the end of the year, and the '
                       'post is on the noticeboard: ward manager, interviews in a month. {rival} from the next ward '
                       'has already asked for the forms. Half the team have told {N} to go for it, and the other '
                       'half are waiting to see who does.'),
                      ('W',
                       'The post has a description, a list of standards and a panel. {N} reads every line, and knows '
                       'the standards by heart.'),
                      ('U',
                       '{N} has had ideas about the ward for years: the handover that takes too long, the drug round '
                       'that could be safer. In charge, they could be tried.'),
                      ('B',
                       'Ward manager is the first rung that counts. {N} wants it before {rival} gets it, and knows '
                       'exactly who sits on the panel.'),
                      ('R',
                       '{N} has never wanted a desk. But the ward needs someone who will fight for it, and {N} can '
                       'feel that it should be {N}.'),
                      ('G',
                       '{N} knows every family that comes back to the ward, and every creak of the old building. '
                       'Nobody else has been here so long, through so many winters of it.')],
            'tribal': [('',
                        'The old birth-keeper of the band has grown too stiff to walk to the births, and the women '
                        'have begun to ask who will keep the births and tend the sick after her. {mentor}, the old '
                        'birth-keeper herself, has looked at {N} more than once, and {rival} from the other hearth '
                        'has been gathering plants and saying so.')],
            'magic': [('',
                       "The old matron of the temple house's long ward has gone to her rest after thirty years, and "
                       'the temple council will name someone to keep the ward at the new moon. {rival}, from the '
                       "sisters' wing, has already been to see the steward.")]},
 'outcomes': (['Within the month it is settled, and the ward turns to {N} first.',
               'Whatever {N} chose, the ward is in good hands, and {N} sleeps well that month.'],
              ['The post goes to {rival}, and {N} has to smile all through the leaving party for {mentor}.',
               'It goes badly at the one moment that mattered, and the post goes to someone from outside.']),
 'options': [
    ('apply through the proper process, with a statement against every standard', 'W1', None, 0.45, '', {'v': 'conformity, achievement', 'title': 'senior nurse or midwife', 'requires': 'professional registration', 'without': 'approval', 'lacking': 0.3, 'world': {'tribal': 'ask the elders and the old birth-keeper by the custom, and keep every old rule of the births', 'magic': 'put your name to the council in the proper form, with a word on every rule of the ward'}, 'chance': 0.4}),
    ('take the leadership course, and bring a plan for a safer ward to the interview', 'U1', None, 0.45, '', {'v': 'achievement, conformity', 'door': True, 'title': 'senior nurse or midwife', 'requires': 'professional registration', 'without': 'approval', 'lacking': 0.3, 'mark': 'learned a skill', 'self_control': '+', 'world': {'tribal': 'learn every plant and every birth the old keeper knows, and show the women how you would keep them', 'magic': "study the temple's books of healing, and bring the council a plan for a safer ward"}, 'chance': 0.4}),
    ('go for it openly against the other candidate, and win the panel over first', 'B1', None, 0.45, '', {'v': 'power, achievement', 'mark': 'made an enemy', 'title': 'senior nurse or midwife', 'world': {'tribal': "put yourself forward openly against the other hearth's healer, and win the elders over first", 'magic': "put your name forward against the sisters' candidate, and win the steward over first"}, 'chance': 0.4}),
    ('tell the panel bluntly what the ward lacks, and how you would fight for it', 'R1', None, 0.45, '', {'v': 'self-direction, benevolence', 'title': 'senior nurse or midwife', 'world': {'tribal': "tell the women bluntly at the fire what the band's births lack, and how you would mend it", 'magic': 'tell the council bluntly what the ward lacks, and how you would fight for it'}, 'chance': 0.4}),
    ('go for it as the one who has known the ward and its families longest', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'mark': 'stayed home', 'identity': True, 'title': 'senior nurse or midwife', 'world': {'tribal': "put yourself forward as the one who has known every hearth's births longest", 'magic': 'put your name forward as the one who has known the ward and its families longest'}, 'chance': 0.4}),
    ('ask to act up in the post for six months, and prove it first', 'B.5 G.5', None, 0.5, '', {'v': 'achievement, security', 'self_control': '+', 'world': {'tribal': 'ask to keep the births beside the old birth-keeper for a season first, and prove it', 'magic': 'ask to keep the ward as acting matron for six months, and prove it first'}, 'chance': 0.82}),
    ("go for a specialist's post instead, with better hours and better pay", 'U.5 B.5', None, 0.5, '', {'v': 'achievement, self-direction', 'self_control': '-', 'world': {'tribal': "become the band's keeper of the strong plants instead, and leave the births to another", 'magic': "seek a place at the apothecaries' bench instead, with its better hours and better pay"}, 'chance': 0.82}),
    ('turn the post down in writing until the ward gets the two nurses it lacks', 'U.5 R.5', None, 0.5, '', {'v': 'universalism, self-direction', 'mark': 'defied an authority', 'closed': 'approval: a post refused on conditions; backfire: the managers give the post to someone else, and remember the letter', 'world': {'tribal': 'refuse to keep the births until the elders give the sick a second healer', 'magic': 'refuse the post in writing until the council gives the ward the two sisters it lacks'}, 'chance': 0.82}),
    ("put your colleague's name forward, and offer to stand beside them", 'W.5 G.5', None, 0.5, '', {'v': 'benevolence, tradition', 'binds': True, 'mark': 'made a friend', 'world': {'tribal': 'speak at the fire for the healer of your own hearth, and offer to stand beside them', 'magic': 'speak to the council for the sister at your side, and offer to stand beside her'}, 'chance': 0.82}),
    ('ask the whole team at handover who they would want in charge', 'W.5 R.5', None, 0.5, '', {'v': 'conformity, benevolence', 'world': {'tribal': 'ask the women of the band at the fire who they would want to keep the births', 'magic': 'ask the sisters of the ward at the change of watch who they would want as matron'}, 'chance': 0.82}),
 ]},
{'name': 'patients come from far away',
 'stages': 'adult mature elder',
 'age': (30, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.03, 0.02),
 'drivers': 'community+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning',
 'horizon': 'years',
 'roles': 'boss, colleague, mentor, friend',
 'requires': 'senior nurse or midwife | midwife | nurse | physician | complementary therapist',
 'tenure': (8.0, 100.0),
 'worlds': {'earth': 'families from other towns begin to ask for the healer by name, and the waiting list grows '
                     "longer than the district's own",
            'tribal': 'families from far bands send runners for the healer by name, and some walk for days to camp '
                      "beside the healer's fire",
            'magic': "families from distant towns of the realm write and travel to be in the healer's hands, and the "
                     "temple house's door is never quiet"},
 'timing': {'times': 'per senior nurse or midwife, nurse, midwife, physician or complementary therapist of eight '
                     'years or more a year: about 1 in 60 find patients travelling from other towns, by word of '
                     'mouth, to be in their care (estimate); about 5 lives in 100,000 become healers known across '
                     'the country (catalogue share; estimate)',
            'likelier': "years with the same district's families, a way of caring of one's own, a story in the "
                        'papers, a mentor who sends patients on',
            'rarer': "a busy city practice where nobody knows anyone's name, a move away, a hard year on the ward",
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'It began with one family, then another, then a woman who drove four hours with her father '
                       'because a neighbour had said {Ns} name. Now letters come every week, the waiting list runs '
                       'to the spring, and a reporter from a big paper has asked to spend a day on the rounds. '
                       '{boss} wants to know what {N} means to do about it.'),
                      ('W',
                       'People come because the care is good, and the care is good because it is done right, every '
                       'time. {N} would like to keep it that way, however many come.'),
                      ('U',
                       '{N} has wondered for years why some ways of caring work better than others. Now there are '
                       'enough patients to find out.'),
                      ('B',
                       "A name like this opens doors: a post of one's own making, a book, a seat at the tables where "
                       'the money is decided. {N} knows it will not last forever.'),
                      ('R',
                       'The families who come so far are frightened and hopeful at once. {N} feels every one of '
                       'them, and wants to say yes to them all.'),
                      ('G',
                       '{N} never set out to be known. The work grew the way a garden does, one season on another, '
                       'and now people come from far away to sit in it.')],
            'tribal': [('',
                        'Runners have come from bands three valleys away, asking for {N} by name, and two families '
                        "have walked for days to camp beside the healer's fire with their sick. The traders carry "
                        'the story from camp to camp, and {boss}, the eldest of the band, asks what {N} means to do '
                        'about it.')],
            'magic': [('',
                       'Letters come under the seals of distant towns, and families travel for days to sit in the '
                       "temple house's long hall and wait for {N}. A broadsheet writer from the capital has asked to "
                       "follow the rounds, and {boss}, the temple's steward, wants to know what {N} means to do.")]},
 'outcomes': (['By the end of the year {Ns} name is known far beyond the district, and the families keep coming.',
               "Whatever {N} chose, the far families are helped, and the district's own still come first."],
              ["The fuss dies down after a season, and the waiting list shrinks back to the district's own.",
               'The far families find another healer to talk about, and {N} goes back to the ordinary weeks, a '
               'little relieved.']),
 'options': [
    ('open a fair list for the far patients, first come first seen, and keep to it', 'W1', None, 0.45, '', {'v': 'universalism, conformity', 'title': 'renowned healer', 'grants': 'families who send for you', 'world': {'tribal': 'take the far sick in the order they came, by the old rule, and keep to it', 'magic': 'open a fair roll for the far patients, first come first seen, and keep to it'}, 'chance': 0.06}),
    ('study what works in your care, and publish it so others can do the same', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'renowned healer', 'grants': 'families who send for you', 'habit': True, 'world': {'tribal': "watch what works in your care season on season, and teach it to every band's healers", 'magic': 'study what works in your care, and set it down in a book for other healers'}, 'chance': 0.06}),
    ('let the reporter follow the rounds, and put your name to your way of caring', 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'renowned healer', 'grants': 'families who send for you', 'identity': True, 'world': {'tribal': 'let the traders carry your name from camp to camp, and name your way of healing for yourself', 'magic': 'let the broadsheet writer follow the rounds, and put your name to your way of caring'}, 'chance': 0.06}),
    ('say yes to every family that comes, and work the evenings to see them all', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'title': 'renowned healer', 'grants': 'families who send for you', 'self_control': '-', 'world': {'tribal': "say yes to every family that comes, and tend them by firelight after the day's work", 'magic': 'say yes to every family that comes, and work the evenings to see them all'}, 'chance': 0.06}),
    ("keep the district's own families first, and let the far ones wait their turn", 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'renowned healer', 'grants': 'families who send for you', 'world': {'tribal': "keep your own band's families first, and let the far ones wait their turn", 'magic': "keep the lower town's own families first, and let the far ones wait their turn"}, 'chance': 0.06}),
    ('go part-time on the ward, and see the far families in a rented room', 'B.5 R.5', None, 0.5, '', {'v': 'self-direction, achievement', 'habit': True, 'world': {'tribal': "leave the band's daily tending to others, and see the far families in a shelter of your own", 'magic': 'give up half your watches, and see the far families in a hired room in the town'}, 'chance': 0.8}),
    ('go out to the far families yourself, one weekend a month', 'R.5 G.5', None, 0.5, '', {'v': 'benevolence, stimulation', 'body': 'light', 'world': {'tribal': 'walk out to the far bands yourself, one moon in every three', 'magic': 'ride out to the far families yourself, one week in every month'}, 'chance': 0.8}),
    ('take two young nurses under your wing, and teach them all you know', 'U.5 G.5', None, 0.5, '', {'v': 'benevolence, achievement', 'grants': "apprentice of one's own", 'binds': True, 'world': {'tribal': 'take two young healers of the band beside you, and teach them all you know', 'magic': 'take two young sisters under your wing, and teach them all you know'}, 'chance': 0.8}),
    ('ask the managers for a clinic day of your own for the far patients', 'W.5 B.5', None, 0.5, '', {'v': 'achievement, security', 'world': {'tribal': 'ask the elders for a shelter by the camp where the far sick may wait', 'magic': 'ask the council for a day in the week of your own for the far patients'}, 'chance': 0.8}),
    ('write each far family a careful letter on what can be done near home', 'W.5 U.5', None, 0.5, '', {'v': 'universalism, benevolence', 'mark': 'helped someone in need', 'world': {'tribal': "send each far family's runner home with a careful word on what their own healers can do", 'magic': 'write each far family a careful letter on what their own healers can do'}, 'chance': 0.8}),
 ]},
{'name': 'the wrong dose on the night shift',
 'stages': 'young_adult adult mature elder',
 'age': (21, 75),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.02, 0.02, 0.015, 0.005),
 'drivers': 'stress+.2 trouble+.1',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, health',
 'horizon': 'week',
 'roles': 'colleague, boss, mentor',
 'requires': 'senior nurse or midwife | nurse | midwife | physician',
 'worlds': {'earth': 'at four in the morning a dose mistake comes to light: a patient given twice the dose, now '
                     'watched and safe, and fine by morning',
            'tribal': 'before dawn in the sickness shelter the healer finds that a sick man was given twice the '
                      'measure of the strong root, and that he will wake well',
            'magic': 'before dawn the healer finds in the ward book that an old carter was given a double draught of '
                     'the sleeping medicine, and that he will wake well'},
 'timing': {'times': 'per nurse, midwife, senior nurse or physician a year: about 1 in 50 make a dose mistake that '
                     'is caught before it does harm (estimate); mistakes with medicines are among the incidents '
                     'hospitals report most, and most of them harm nobody (patient-safety reporting; estimate); '
                     'about 3 lives in 100 are nurses (catalogue share)',
            'likelier': 'long shifts and short staff, two strengths of one medicine kept side by side, a new ward, '
                        'nights',
            'rarer': 'a second check on every strong dose, a rested team, a ward with time to stop and look',
            'gap_years': (5.0, 15.0)},
 'scenes': {'earth': [('',
                       'At four in the morning, checking the charts, {N} sees it: the old man in bed twelve was '
                       'given twice his dose of a strong painkiller at midnight. {colleague}, at the end of a '
                       'fourteen-hour day, drew it up, and {N} checked it and signed. He is breathing easily and his '
                       'colour is good; the doctor will say he needs watching and nothing more, and by morning he '
                       'will be fine. Nobody else has noticed yet.'),
                      ('W',
                       'There is a form for this, and a reason for the form. {N} knows the rule: report it at once, '
                       'whatever it costs.'),
                      ('U',
                       'Two strengths of the same medicine, kept side by side in boxes that look almost alike. {N} '
                       'can already see how it happened, and how it will happen again.'),
                      ('B',
                       'A mistake on the record stays on the record. {N} thinks of the promotion list, the '
                       'registration board, and the managers who will want a name to blame.'),
                      ('R',
                       '{Ns} stomach turns over. The man in bed twelve tells jokes about his grandchildren, and {N} '
                       'could have hurt him.'),
                      ('G',
                       'He is asleep, and his breathing is slow and even. The body has its own ways of mending, and '
                       '{N} can sit beside it and watch it mend.')],
            'tribal': [('',
                        "In the sickness shelter before dawn, {N} counts the roots left in the healer's bag and sees "
                        'it: the old hunter with the cough was given twice the measure of the strong root at '
                        "nightfall, from {colleague}'s mixing and {Ns} own hand. He sleeps deeply and breathes well, "
                        'and by morning he will wake, but nobody else knows yet.')],
            'magic': [('',
                       'Checking the ward book before dawn, {N} sees that the old carter in the end bed was given a '
                       'double draught of the sleeping medicine at midnight, mixed by {colleague} at the end of a '
                       'long watch and given by {N}. He breathes easily and will wake well, but nobody else has '
                       'noticed.')]},
 'outcomes': (['The patient wakes well and hungry, and the matter is settled the way {N} chose.',
               "A month later the ward does things a little differently, and {N} can look the patient's family in "
               'the eye.'],
              ['The patient is fine by morning, but the matter goes badly: questions, meetings and a cold silence '
               'among the others.',
               'Word gets out the wrong way, and for a season {N} is the name the others whisper about.']),
 'options': [
    ('tell the night doctor at once, and fill in the incident form before handover', 'W1', None, 0.45, '', {'v': 'conformity, security', 'identity': True, 'mark': 'owned up', 'world': {'tribal': 'wake the old healer at once, and tell the elders at first light, as the custom is', 'magic': 'wake the night physician at once, and write it in the ward book before the change of watch'}, 'chance': 0.69}),
    ('work out exactly how the two doses were mixed up, step by step', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'mark': 'learned a skill', 'world': {'tribal': 'work out exactly how the two measures of root were mixed up, step by step', 'magic': 'work out exactly how the two draughts were mixed up, step by step'}, 'chance': 0.71}),
    ('ring the union rep before saying a word to anyone', 'B1', None, 0.45, '', {'v': 'security, power', 'self_control': '+', 'world': {'tribal': "go first to the old healer who has the elders' ear, before saying a word to anyone", 'magic': "go first to the sisters' advocate in the temple, before saying a word to anyone"}, 'chance': 0.7}),
    ("tell the patient's daughter yourself, face to face, first thing in the morning", 'R1', None, 0.45, '', {'v': 'benevolence, self-direction', 'mark': 'owned up', 'world': {'tribal': "tell the old hunter's daughter yourself, face to face, at first light", 'magic': "tell the carter's daughter yourself, face to face, first thing in the morning"}, 'chance': 0.67}),
    ('sit by the patient until morning, watching every breath until it passes', 'G1', None, 0.45, '', {'v': 'benevolence', 'body': 'light', 'world': {'tribal': 'sit by the old hunter until morning, watching every breath until it passes', 'magic': 'sit by the old carter until morning, watching every breath until it passes'}, 'chance': 0.72}),
    ('tell the patient and the ward the whole of it, and write it all down', 'W.34 U.33 R.33', None, 0.5, '', {'v': 'conformity, benevolence', 'self_control': '+', 'mark': 'owned up', 'identity': True, 'world': {'tribal': 'tell the old hunter and the whole band the whole of it at the fire', 'magic': 'tell the carter and the whole ward the whole of it, and write it all in the book'}, 'chance': 0.75}),
    ('report it to the safety team with a plan for a second check on strong doses', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'universalism, security', 'world': {'tribal': 'ask the elders that every measure of the strong root be checked by a second healer', 'magic': 'ask the council that every strong draught be checked by a second sister'}, 'chance': 0.72}),
    ('put your name alone on the report, to shield the worn-out colleague', 'W.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence', 'world': {'tribal': 'tell the elders it was your hand alone, to shield the worn-out healer who mixed it', 'magic': 'write your name alone in the book, to shield the worn-out sister who mixed it'}, 'chance': 0.66}),
    ('correct the chart quietly, say nothing, and watch the patient yourself till morning', 'U.34 B.33 G.33', None, 0.5, '', {'v': 'security, power', 'mark': 'hid a wrong', 'self_control': '-', 'takes_if_fails': 'licence to prescribe', 'closed': 'approval: a mistake hidden; backfire: the pharmacy count and the record show it, and the leave to give strong medicines is taken away', 'world': {'tribal': 'say nothing, put back a root from your own store, and watch the old hunter yourself till morning', 'magic': 'mend the ward book quietly, say nothing, and watch the carter yourself till morning'}, 'chance': 0.6}),
    ('ask the manager for fewer night shifts, before tiredness does it again', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'security, self-direction', 'world': {'tribal': 'ask the elders to let you rest from the night tending, before tiredness does it again', 'magic': 'ask the steward for fewer night watches, before tiredness does it again'}, 'chance': 0.78}),
 ]},
{'name': 'the remedy that worked',
 'stages': 'adult mature elder',
 'age': (30, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.01, 0.01, 0.01),
 'drivers': 'community+.2 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, meaning, nature',
 'horizon': 'months',
 'roles': 'grandparent, colleague, mentor, boss',
 'requires': 'nurse | midwife | complementary therapist | senior nurse or midwife',
 'tenure': (3.0, 99.0),
 'worlds': {'earth': 'a dressing of honey and garden marigold heals the old wounds that would not close, and the '
                     'families start to talk about it',
            'tribal': 'a poultice of wild honey and the yellow meadow flower closes the old wounds that would not '
                      'heal, and the bands start to talk about it',
            'magic': "a salve of honey and marigold from the healer's own garden closes the wounds the temple's "
                     'physicians gave up on, and the town talks of nothing else'},
 'timing': {'times': 'per nurse, midwife, complementary therapist or senior nurse of three years or more a year: '
                     'about 1 in 100 find a way of caring of their own that the families start to talk about '
                     '(estimate); honey and plant dressings for slow wounds are old remedies that ward studies have '
                     'looked at again (estimate); about 5 lives in 100,000 become healers known across the country '
                     '(catalogue share)',
            'likelier': 'years with the same families, a garden or an old family way, a mentor who listens, a year '
                        'when the papers want a good story',
            'rarer': 'a ward that changes its dressings by the book alone, no time to watch a wound for weeks, a '
                     'move away',
            'gap_years': (6.0, 15.0)},
 'scenes': {'earth': [('',
                       'The old farmer from the next village had a wound on his leg that had not closed in a year. '
                       '{N} tried a dressing of honey and marigold from {Ns} own garden, the way {grandparent} used '
                       'to make it, and in six weeks it had healed. Then a second wound healed, and a third. Now the '
                       'families ask for {N} by name, the local paper has rung, and {mentor} says it ought to be '
                       'written up properly.'),
                      ('W',
                       'If it works, it should be done properly: measured, written down, checked, and taught the '
                       'same way every time. {N} has the notes of every dressing in a folder.'),
                      ('U',
                       'Why does it work? {N} has read everything there is on honey and wounds, and there is a '
                       'question in it nobody seems to have asked.'),
                      ('B',
                       'Something like this could make a name. {N} thinks of the conferences, the books, and the '
                       'people who would want to put their own name to it first.'),
                      ('R',
                       '{N} cannot stop thinking about all the people out there with wounds that will not close, '
                       'waiting and hoping. Every one of them should have this.'),
                      ('G',
                       "The marigolds came from {grandparent}'s seed, saved year after year. The garden gives, and "
                       'the body heals, if both are given time.')],
            'tribal': [('',
                        'The old hunter of the next band had a wound on his leg that had not closed since the '
                        'summer. {N} laid on a poultice of wild honey and the yellow meadow flower, the way '
                        '{grandparent} did it, and before the moon was out it had healed. Now runners come from far '
                        'camps asking for the healer who knows the yellow flower, and the traders carry the story '
                        'from fire to fire.')],
            'magic': [('',
                       "The temple's physicians had given up on the old carter's leg, and {N} dressed it with a "
                       'salve of honey and marigold from {Ns} own garden, the way {grandparent} made it. In six '
                       'weeks it had healed. Now families queue at the temple house door, a printer wants to sell '
                       "the recipe, and the masters of the apothecaries' college have written to ask what is in "
                       'it.')]},
 'outcomes': (['Within the year {Ns} dressing is talked about far beyond the district, and the wounds go on closing.',
               'Whatever {N} chose, the families keep coming, and the wounds that would not heal begin to close.'],
              ['The fuss fades after a season, the talk moves on, and {N} goes back to the ordinary dressings and '
               'the ordinary weeks.',
               'The next three wounds heal no faster than any others, and people stop asking, though {N} keeps '
               'making it.']),
 'options': [
    ('write it up as a careful protocol, and send it to the national nursing college', 'W1', None, 0.45, '', {'v': 'conformity, universalism', 'title': 'renowned healer', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'world': {'tribal': "set it down as the band's own way, step by step, and teach it at the great gathering", 'magic': "write it up as a careful rule of practice, and send it to the apothecaries' college"}, 'chance': 0.03}),
    ('run a proper trial with a doctor on twenty patients, and publish the results', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'renowned healer', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': 'try it on every slow wound in three bands, season by season, and mark which ones close', 'magic': 'try it with a temple physician on twenty patients, and set the results in a book'}, 'chance': 0.03}),
    ('give the dressing your own name, and take it to every conference that will listen', 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'renowned healer', 'grants_if_fails': 'a long shot that missed', 'world': {'tribal': "give the poultice your own name, and carry it to every band's gathering", 'magic': 'give the salve your own name, and show it before every guild that will listen'}, 'chance': 0.03}),
    ('say yes to every family who writes, and go to them, however far', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'door': True, 'title': 'renowned healer', 'grants_if_fails': 'a long shot that missed', 'body': 'light', 'world': {'tribal': 'say yes to every runner who comes, and walk to the far bands, however far', 'magic': 'say yes to every family who writes, and ride out to them, however far'}, 'chance': 0.03}),
    ('grow the marigolds in your own garden, and teach the families to make it', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'renowned healer', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'world': {'tribal': 'gather the yellow flower in the meadows each summer, and teach every hearth to make it', 'magic': "grow the marigolds in your own garden, and teach the town's families to make it"}, 'chance': 0.03}),
    ('teach it to the young nurses on the ward, one patient at a time', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'benevolence, tradition', 'grants': "apprentice of one's own", 'world': {'tribal': 'teach it to the young healers of the band, one wound at a time', 'magic': 'teach it to the young sisters of the ward, one patient at a time'}, 'chance': 0.84}),
    ("write it up for the hospital's own bulletin, with the dates and the weeks", 'W.34 U.33 B.33', None, 0.5, '', {'v': 'achievement, conformity', 'world': {'tribal': "tell it at the elders' fire, wound by wound and moon by moon, so it is remembered", 'magic': "write it up for the temple house's own book, with the dates and the weeks"}, 'chance': 0.84}),
    ('ask the managers for one day a week for the wounds that will not heal', 'W.34 B.33 R.33', None, 0.5, '', {'v': 'achievement, benevolence', 'habit': True, 'world': {'tribal': 'ask the elders to free you from the hunt one day in four, for the wounds that will not heal', 'magic': 'ask the council for one day a week for the wounds that will not heal'}, 'chance': 0.84}),
    ("keep using it on the ward's old wounds, without waiting for the managers' leave", 'U.34 R.33 G.33', None, 0.5, '', {'v': 'self-direction, benevolence', 'mark': 'defied an authority', 'closed': 'approval: a dressing used on the ward without leave; backfire: the medicines committee hears of it, and the senior nurse is told to stop and write it up', 'world': {'tribal': "keep laying it on every slow wound, without waiting for the elders' word", 'magic': "keep using it on the ward's old wounds, without waiting for the physicians' leave"}, 'chance': 0.84}),
    ("keep it for the district's families, and turn the reporter from the paper away", 'B.34 R.33 G.33', None, 0.5, '', {'v': 'security, tradition', 'world': {'tribal': "keep it for your own band's families, and send the far runners away", 'magic': "keep it for the lower town's families, and turn the printer away"}, 'chance': 0.84}),
 ]},
{'name': 'the sickness in the winter camp',
 'stages': 'adult mature elder',
 'age': (30, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.02),
 'drivers': 'harsh+.2 community+.1',
 'tier': 'life event',
 'tone': 'mixed',
 'life': 'work, community, health',
 'horizon': 'months',
 'roles': 'elder, colleague, rival',
 'requires': 'senior nurse or midwife | nurse | midwife',
 'tenure': (2.0, 99.0),
 'worlds': {'tribal': 'a fever runs through the winter camp by the frozen river, and the band looks to its healer'},
 'only': 'tribal',
 'timing': {'times': 'per healer of the band in the tribal world (the birth-keeper, or a nurse or midwife of two '
                     'winters) a year: about 1 in 50, in a winter when a fever runs through the camp (estimate); '
                     'small bands living close in winter shelters met fevers most winters, and most passed '
                     '(estimate)',
            'likelier': 'a hard winter in one camp, a slow pool for drinking water, a band crowded with visitors '
                        'from the gathering',
            'rarer': 'a mild winter on the move, clean running water, a band kept apart from the others',
            'gap_years': (5.0, 10.0)},
 'scenes': {'tribal': [('',
                        'In the deep of the winter a fever runs through the camp by the frozen river. A dozen of the '
                        'band lie hot and shivering in their shelters, old hunters and grown men and women alike, '
                        "and {colleague}, the band's other healer, is down with it too. The elders look to {N}, and "
                        'the runners from the next band say their healer cannot come before the moon turns.'),
                       ('W',
                        'The old rule is clear: the sick sleep apart from the well, and the healer goes to each in '
                        'turn. {N} has seen what happens when nobody keeps it.'),
                       ('U',
                        'The fever started in the shelters nearest the slow pool below the camp, and nowhere else. '
                        '{N} keeps thinking about the water.'),
                       ('B',
                        'Whoever brings the camp through this winter will be spoken of at every fire in the valley. '
                        '{N} knows it, and so does {rival}.'),
                       ('R',
                        '{N} has not slept for two nights and does not mean to. There is always another shelter, '
                        'another hot forehead, another cup of water to hold.'),
                       ('G',
                        'Fevers come with the deep cold, as they always have, and most of them pass. The willows by '
                        'the river still hold what the old ones used, under the snow.')]},
 'outcomes': (['The fever breaks in the shelters one by one, and by the thaw the whole camp is on its feet.',
               'Whatever {N} chose, the sickness passes, and the bands along the river hear whose hands tended it.'],
              ['The fever runs through the camp for a whole moon before it passes, and everyone is thin and tired by '
               'the thaw.',
               'The sickness passes in its own time and everyone recovers, but the band gives another healer the '
               'credit.']),
 'options': [
    ('keep the sick apart from the well by the old rule, and tend each in turn', 'W1', None, 0.45, '', {'v': 'conformity, security', 'title': 'renowned healer', 'grants': 'families who send for you', 'chance': 0.06}),
    ('find the water the fever came with, and move the drinking to the clean spring', 'U1', None, 0.45, '', {'v': 'achievement, universalism', 'title': 'renowned healer', 'grants': 'families who send for you', 'chance': 0.06}),
    ("send runners to every band for their healers' plants, and lead them all", 'B1', None, 0.45, '', {'v': 'power, achievement', 'title': 'renowned healer', 'grants': 'families who send for you', 'chance': 0.06}),
    ('go from shelter to shelter day and night, until the last fever breaks', 'R1', None, 0.45, '', {'v': 'benevolence, stimulation', 'title': 'renowned healer', 'grants': 'families who send for you', 'body': 'light', 'chance': 0.06}),
    ('brew the willow bark the old ones used for fevers, and carry it to every shelter', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'title': 'renowned healer', 'grants': 'families who send for you', 'chance': 0.06}),
    ('teach every hearth to boil its water and keep its sick warm', 'W.34 U.33 G.33', None, 0.5, '', {'v': 'universalism, benevolence', 'mark': 'helped someone in need', 'chance': 0.7}),
    ('ask the elders to move the camp upriver to clean water, and plan the move', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, achievement', 'binds': True, 'chance': 0.7}),
    ('ask the shaman to call on the river spirit for a cure, and promise its price', 'W.34 R.33 G.33', None, 0.5, '', {'v': 'tradition, benevolence', 'mark': 'took a wild risk', 'closed': "approval: the spirit's price; backfire: the fever passes, but the spirit's price comes due: the band must leave its best winter ground for three winters, and the elders blame the healer", 'chance': 0.7}),
    ("trade the band's best furs to the next band for their healer's help", 'U.34 B.33 R.33', None, 0.5, '', {'v': 'benevolence, power', 'chance': 0.7}),
    ('stay in the sick shelter with the worst of them, and keep the others away', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, security', 'body': 'light', 'chance': 0.7}),
 ]},
{'name': 'the idea in the shed at night',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.1 U.4 B.1 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'joy',
 'life': 'work, making',
 'horizon': 'months',
 'roles': 'partner, boss, mentor',
 'requires': 'software developer | civil engineer | machinist | electrician | founder of a firm | apprentice',
 'worlds': {'earth': 'an idea that will not let go, and the shed at the bottom of the garden: a bench, a lamp and a '
                     'box of old parts',
            'tribal': 'an idea for a new kind of tool that will not let go, worked at by the embers after the band '
                      'sleeps',
            'magic': "an idea for a new device that will not let go, built at night in the workshop's back room from "
                     'odds and ends'},
 'timing': {'times': 'per software developer, civil engineer, machinist, electrician, founder of a firm or '
                     'apprentice a year: about 1 in 6 works at an idea of their own in the evenings for a while '
                     '(estimate); about 1 life in 5 holds one of these trades at some time, and about 5 lives in '
                     '10,000 come to live from their own inventions (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'It started as a sketch on the back of a work rota, and now it will not leave {N} alone. Most '
                       'nights after supper {N} goes down to the shed at the bottom of the garden, switches on the '
                       'lamp over the bench and tips out the box of old parts: small motors, springs, the circuit '
                       'board from a broken washing machine. {partner} has stopped asking when {N} is coming to '
                       'bed.'),
                      ('W',
                       'Somewhere in {Ns} contract at work there is a clause about ideas. Before the next screw goes '
                       'in, {N} would like to know exactly whose idea this is, and to have it written down.'),
                      ('U',
                       'The thing almost works on paper. There is one joint that will not take the load, and {N} has '
                       'drawn it eleven ways in the notebook, each a little closer.'),
                      ('B',
                       '{N} keeps doing the sums in the dark: what it would cost to make, what a shop would charge, '
                       'who would buy the first thousand.'),
                      ('R',
                       '{N} cannot sleep for thinking about it. The urge is to build the whole thing tonight, all at '
                       'once, and watch it move.'),
                      ('G',
                       'The shed smells of oil and cut wood, and half the parts on the bench came from things {Ns} '
                       'grandfather mended and never threw away. Somewhere in that box is everything the idea '
                       'needs.')],
            'tribal': [('',
                        'When the band sleeps, {N} sits by the embers turning a new kind of tool over and over: a '
                        'scraper with a bone grip that will not slip, a hook that holds what the old ones lose. It '
                        'will not leave {N} alone, and the others laugh at the heap of broken tries by the '
                        'shelter.')],
            'magic': [('',
                       'Most nights, when the workshop has closed, {N} takes a lamp into the back room and works at '
                       "a device of {Ns} own: brass wheels, a spring from a broken clock, a lens from the glazier's "
                       'scraps. The master does not know, and {N} has not decided whether to say.')]},
 'outcomes': (['The idea takes shape, and one night it moves the way {N} saw it move in {Ns} head.',
               'Whatever {N} chose, the idea is further on by the spring, and the notebook is full of it.'],
              ['The part that would not take the load still will not, and the tries are put away for the winter.',
               'Work and sleep win, the evenings go to other things for weeks at a time, and the idea cools.']),
 'options': [
    ('read what your contract says about ideas, and keep a dated notebook of every step', 'W1', None, 0.45, '', {'v': 'conformity, security', 'world': {'tribal': 'ask the elders whether a new tool belongs to its maker or the band, and keep to it', 'magic': "read the guild's rules on new devices, and keep a dated book of every step"}, 'chance': 0.8}),
    ('draw it, model it, and build the first working part properly', 'U1', None, 0.45, '', {'grants': 'prototyping', 'aims': 'inventor', 'v': 'achievement, self-direction', 'world': {'tribal': 'shape it in soft wood first, then in bone, trying each part in turn', 'magic': 'draw it, build a small model, then make the first working part in brass'}, 'chance': 0.6}),
    ('take a rough one to the Saturday market every week, and see what people pay', 'B1', None, 0.45, '', {'habit': True, 'v': 'achievement, power', 'world': {'tribal': 'take a rough one to every trading meet, and see what people would give for it', 'magic': 'take a rough one to the market every week, and see what people pay'}, 'chance': 0.7}),
    ("build it on the firm's time, with the firm's parts, and say nothing", 'R1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': "law: an employer's design taken; backfire: the firm finds out, claims the idea as its own, and the patent with it", 'self_control': '-', 'v': 'stimulation, self-direction', 'world': {'tribal': "make it from the band's own store of good flint, and say nothing", 'magic': "build it on the master's time, with the master's brass, and say nothing"}, 'chance': 0.7}),
    ('build it from what is already in the shed: old motors, offcuts, a mended vice', 'G1', None, 0.45, '', {'v': 'tradition, universalism', 'world': {'tribal': 'make it from what is already by the shelter: old antler, offcuts of bone, worn stones', 'magic': 'build it from what is already in the back room: old wheels, offcuts, a mended vice'}, 'chance': 0.8}),
    ('keep two evenings a week for it, every week, and never more', 'W1', 'U.7', 0.5, '', {'self_control': '+', 'habit': True, 'v': 'achievement, conformity', 'world': {'tribal': 'keep two evenings of every moon for it, and never more'}, 'chance': 0.6}),
    ('look up every patent near the idea, and find the gap nobody owns yet', 'U1', 'B.7', 0.5, '', {'v': 'achievement, power', 'world': {'tribal': 'ask the traders which tools the far bands already make, and find the one nobody makes', 'magic': "search the guild's register of designs, and find the gap nobody holds yet"}, 'chance': 0.8}),
    ('save up for the parts first, then give yourself one summer to make it run', 'B1', 'R.7', 0.5, '', {'aims': 'inventor', 'self_control': '+', 'v': 'self-direction, achievement', 'world': {'tribal': 'put by furs for good stone first, then give yourself one summer to make it work'}, 'chance': 0.7}),
    ("build it at the kitchen table every weekend, with the whole family's hands in it", 'R1', 'G.7', 0.5, '', {'habit': True, 'v': 'benevolence, stimulation', 'world': {'tribal': "make it at the hearth every evening, with the whole family's hands in it", 'magic': "build it at the kitchen table every feast day, with the whole household's hands in it"}, 'chance': 0.7}),
    ("turn it to the allotments' broken water pump, built as the plot holders need it", 'G1', 'W.7', 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'world': {'tribal': "turn it to the band's leaking water skins, made as those who carry the water need it", 'magic': "turn it to the ward's broken well pump, built as the neighbours need it"}, 'chance': 0.6}),
 ]},
{'name': 'the machine nobody can fix',
 'stages': 'young_adult adult mature elder',
 'age': (18, 90),
 'alpha': 'W.4 U.1 B.4 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work',
 'horizon': 'week',
 'roles': 'boss, colleague, mentor',
 'requires': 'software developer | civil engineer | machinist | electrician | founder of a firm | apprentice',
 'worlds': {'earth': 'the old machine the whole works depends on has stopped, and the firm that made it closed '
                     'decades ago',
            'tribal': 'the great fish weir across the river has given way at the middle, days before the salmon run, '
                      'and nobody alive knows how it was first laid',
            'magic': "the great water-wheel that drives the guild's mill has seized, and the artificer who built its "
                     'governor is fifty years dead'},
 'timing': {'times': 'per software developer, civil engineer, machinist, electrician, founder of a firm or '
                     'apprentice a year: about 1 in 5 sees an old machine or system the work depends on fail with '
                     'nobody left who knows it well (estimate); about 1 life in 5 holds one of these trades at some '
                     'time (catalogue shares)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Monday morning, and the old machine at the heart of the works has stopped: a press the size '
                       'of a lorry, older than anyone on the floor, run by a grey control box nobody has opened in '
                       'years. The firm that made it closed decades ago, the manual is a few stained pages, and the '
                       'whole line stands still. {boss} looks round the room for someone who can fix it.'),
                      ('W',
                       'There is a right way to do this: lock it off, read what manual there is, test one thing at a '
                       'time and write each one down. {N} has seen what happens when people skip the steps.'),
                      ('U',
                       '{N} has wondered for years how the old thing actually works. Now it stands open on the '
                       'floor, and nobody will stop {N} finding out.'),
                      ('B',
                       'The works is losing money by the hour, and whoever gets it running will be remembered at '
                       'review time. {N} knows it, and so does {colleague}.'),
                      ('R',
                       'The line is silent, the floor is full of people standing about, and {N} wants to be inside '
                       'that machine with a torch and a spanner now.'),
                      ('G',
                       'The old machine has run through three generations of workers, and {mentor}, who kept it '
                       'going for thirty years, retired last spring. {N} thinks of the old tricks that went out of '
                       'the door with {mentor}.')],
            'tribal': [('',
                        'The great fish weir across the river, built by the grandparents of the oldest elder, has '
                        'given way at the middle, and the salmon run is days off. Nobody alive knows how it was '
                        'first laid, and the band looks to the ones who make things.')],
            'magic': [('',
                       "The great water-wheel that drives the guild's mill has seized, its clockwork governor jammed "
                       'solid, and the artificer who built it has been dead fifty years. The millers stand idle, the '
                       "city's flour runs low, and the guild master looks round for someone who can mend it.")]},
 'outcomes': (['By the end of the week the old machine is running again, and people stop by to look at it as if it '
               'were new.',
               'Whatever {N} chose, the work starts again, and {N} knows the old thing better than anyone now '
               'living.'],
              ['The fix holds for a day and then fails again, and the whole floor waits another week for help from '
               'outside.',
               'Nothing {N} tries brings it back, and {boss} sends far away for someone who costs a great deal.']),
 'options': [
    ('lock it off by the safety rules, though the manager wants it running today', 'W1', None, 0.45, '', {'mark': 'defied an authority', 'closed': "approval: the line stopped against the manager's word; backfire: a written warning, and the shift's pay docked for the lost day", 'identity': True, 'v': 'conformity, security', 'world': {'tribal': 'forbid anyone to wade out to the weir until it is made safe, whatever the elders say', 'magic': "chain the wheel still by the guild's rules, though the master wants it turning today"}, 'chance': 0.55}),
    ('take it apart, draw how it works, and make a new part that does the same', 'U1', None, 0.45, '', {'grants': 'prototyping', 'aims': 'inventor', 'v': 'achievement, self-direction', 'world': {'tribal': 'take the weir apart stake by stake, learn how it was laid, and cut a new middle', 'magic': 'take the governor apart, draw how it works, and make a new part that does the same'}, 'chance': 0.7}),
    ('tell the boss you can fix it, and name your price first', 'B1', None, 0.45, '', {'v': 'power, achievement', 'world': {'tribal': 'tell the elders you can mend the weir, and ask for the first fish of the run', 'magic': 'tell the guild master you can mend it, and name your fee first'}, 'chance': 0.65}),
    ('climb inside with a torch and a spanner, and get it running tonight', 'R1', None, 0.45, '', {'body': 'light', 'v': 'stimulation', 'world': {'tribal': 'wade out into the cold river, and lash the weir back together before dark', 'magic': 'climb into the wheel housing with a lamp and a spanner, and get it turning tonight'}, 'chance': 0.65}),
    ('visit the old fitter who kept it going, every evening, until you know it too', 'G1', None, 0.45, '', {'grants': 'fixing things', 'habit': True, 'v': 'tradition, benevolence', 'world': {'tribal': 'sit with the oldest weir-builder every evening, until you know how the grandparents laid it', 'magic': 'visit the old millwright who kept it turning, every evening, until you know it too'}, 'chance': 0.75}),
    ('write down every fault and every fix, so the next person has a manual', 'W1', 'U.7', 0.5, '', {'grants': 'fixing things', 'v': 'universalism, conformity', 'world': {'tribal': 'teach the young ones each stake and knot as it goes back, so the next mending is easier', 'magic': 'write down every fault and every fix, and leave the guild a proper manual'}, 'chance': 0.85}),
    ('design a modern replacement, and pitch it to the boss as your own project', 'U1', 'B.7', 0.5, '', {'aims': 'inventor', 'v': 'achievement, power', 'world': {'tribal': 'plan a better weir of your own making, and ask the elders for leave to build it', 'magic': 'design a new governor, and offer it to the guild master as your own work'}, 'chance': 0.7}),
    ('get the boss to pay double for a weekend crew, and lead the strip-down yourself', 'B1', 'R.7', 0.5, '', {'v': 'power, stimulation', 'world': {'tribal': 'promise the helpers a share of the first catch, and lead the rebuilding yourself', 'magic': 'get the guild to pay double for a feast-day crew, and lead the work yourself'}, 'chance': 0.75}),
    ('work through the weekend to save the old machine, and the jobs that hang on it', 'R1', 'G.7', 0.5, '', {'self_control': '+', 'v': 'benevolence, tradition', 'world': {'tribal': 'work day and night to save the old weir, and the winter food that hangs on it', 'magic': "work through the feast days to save the old wheel, and the millers' bread"}, 'chance': 0.75}),
    ('take the parts it needs from the old twin in the scrapyard, though it is sold', 'G1', 'W.7', 0.5, '', {'mark': 'hid a wrong', 'closed': 'law: parts taken from a machine already sold for scrap; backfire: the scrap dealer counts the gaps, sends the firm a bill, and the boss wants a name', 'v': 'security, tradition', 'world': {'tribal': 'take the stakes it needs from the old weir of the band upriver, though it is theirs', 'magic': "take the parts it needs from the old twin wheel in the breaker's yard, though it is sold"}, 'chance': 0.65}),
 ]},
{'name': 'a big firm wants to buy the patent',
 'stages': 'young_adult adult mature elder',
 'age': (20, 95),
 'alpha': 'W.1 U.4 B.1 R.1 G.4',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'mixed',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'colleague, partner, boss',
 'requires': 'inventor',
 'worlds': {'earth': 'a letter from a big firm: it wants to buy the patent outright, and it makes the very thing the '
                     'invention would replace',
            'tribal': 'a trader from the far bands comes with a canoe of goods for the sole right to make the new '
                      'tool',
            'magic': "a great merchant house offers a purse of gold for the guild's grant on the design, and it "
                     'sells the very device the design would replace'},
 'timing': {'times': 'per inventor a year: about 1 in 6 is offered money for a patent or a design, outright or as a '
                     'licence, and a few of those offers come from firms that would rather the idea never reached '
                     'the shops (estimate); about 5 lives in 10,000 come to live from their own inventions '
                     '(catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'The letter from the big firm is two pages long and very polite. They would like to buy {Ns} '
                       'patent outright, the one {N} and {colleague} spent three years of evenings on, for more '
                       'money than {N} has ever seen in one place. A smaller firm in town has rung as well. {N} '
                       'knows the big firm makes the very thing the invention would replace.'),
                      ('W',
                       'There was never a written agreement with {colleague}, only a handshake over the bench. {N} '
                       'thinks a handshake is still a promise.'),
                      ('U',
                       '{N} reads the offer three times, then the small print, then the patent itself. A patent runs '
                       'twenty years, and the right licence could be worth more than any sale.'),
                      ('B',
                       'The number in the letter is real money, and {N} knows the big firm would pay more if pushed. '
                       'Somebody is going to do well out of this, and it may as well be {N}.'),
                      ('R',
                       'Sell it, and someone in a meeting room decides what becomes of it. {N} built the thing, and '
                       'the thought of handing it over makes {Ns} jaw tighten.'),
                      ('G',
                       'The small firm in town employs forty people, half of them {Ns} neighbours. {N} pictures the '
                       'invention being made down the road, by hands {N} knows.')],
            'tribal': [('',
                        'A trader from the far bands has come with a canoe full of goods: flints, furs and shells. '
                        'The trader wants the sole right to make {Ns} new tool, for the far bands alone. {N} made it '
                        'with {colleague}, over three winters by the fire.')],
            'magic': [('',
                       'A great merchant house has sent its steward with a purse of gold and a contract on vellum: '
                       "it would buy the guild's grant on {Ns} design outright. {N} made it with {colleague} over "
                       'three years in the back room, and the merchant house sells the very device the design would '
                       'replace.')]},
 'outcomes': (['The matter is settled the way {N} wanted it, and the money, the rights and the friendship are where '
               '{N} meant them to be.',
               'Whatever {N} chose, a year later the invention is out in the world in some form, and {N} is working '
               'on the next one.'],
              ['The deal goes sour over the terms, and {N} spends the year arguing instead of making.',
               'The offer is withdrawn while {N} is still thinking, and the buyer brings out something very like it '
               'of their own.']),
 'options': [
    ("sell only on fair terms, read through by a lawyer, with the partner's share written in", 'W1', None, 0.45, '', {'grants': 'savings', 'mark': 'kept your word', 'v': 'security, conformity', 'world': {'tribal': "trade only before the elders, with the partner's share set out for all to hear", 'magic': "sell only on fair terms, witnessed at the guildhall, with the partner's share written in"}, 'chance': 0.7}),
    ('keep the patent, and license it to both firms for a fee on every one made', 'U1', None, 0.45, '', {'v': 'achievement, security', 'world': {'tribal': 'keep the making in your own hands, and let both bands make it for a gift on every one', 'magic': "keep the guild's grant, and let both houses make it for a fee on every one made"}, 'chance': 0.65}),
    ('sell to the firm that will shelve it, for top money, and keep the partner out', 'B1', None, 0.45, '', {'grants': 'savings', 'mark': 'broke your word', 'closed': "approval: a shared invention sold to be shelved, behind a partner's back; backfire: the partner finds the contract, and the whole trade hears who sold out", 'v': 'power', 'world': {'tribal': 'give the far trader the sole right to it, and tell the partner nothing until the canoe has gone', 'magic': 'sell to the house that will bury it, for the most gold, and keep the partner out'}, 'chance': 0.75}),
    ('turn them down flat, and find backers to make it yourself', 'R1', None, 0.45, '', {'grants': 'investors who back you', 'aims': 'celebrated inventor', 'binds': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'send the trader away, and find traders who will share their goods while you make it yourself', 'magic': 'turn the steward away, and find backers among the merchant houses to make it yourself'}, 'chance': 0.55}),
    ('sell it to the small firm in town, so it is made by people you know', 'G1', None, 0.45, '', {'grants': 'savings', 'identity': True, 'v': 'tradition, benevolence', 'world': {'tribal': "give the right to your own band's toolmakers, so it is made by hands you know", 'magic': 'sell it to the small workshop in the ward, so it is made by people you know'}, 'chance': 0.8}),
    ('license it for five years only, so the idea is free again after', 'W1', 'R.7', 0.5, '', {'v': 'self-direction, security', 'world': {'tribal': 'let the far trader make it for five summers only, and then it is free again', 'magic': 'grant the merchant house five years only, so the design is free again after'}, 'chance': 0.7}),
    ('license it cheaply to small makers everywhere, so it spreads on its own', 'U1', 'G.7', 0.5, '', {'aims': 'celebrated inventor', 'v': 'universalism, achievement', 'world': {'tribal': "show any band's toolmaker how to make it for a small gift, so it spreads on its own", 'magic': 'grant it cheaply to small workshops everywhere, so it spreads on its own'}, 'chance': 0.75}),
    ('play the two firms against each other, and put the winnings in trust for the team', 'B1', 'W.7', 0.5, '', {'grants': 'savings', 'self_control': '+', 'mark': 'made an enemy', 'v': 'power, benevolence', 'world': {'tribal': 'let the far trader and the near one bid against each other, and share the winnings with all who helped', 'magic': 'play the two houses against each other, and set the winnings in trust for the workshop'}, 'chance': 0.65}),
    ('tell them straight it is not finished, and walk away to make it better', 'R1', 'U.7', 0.5, '', {'v': 'achievement, self-direction', 'world': {'tribal': 'tell the trader plainly the tool is not finished, and go back to the fire to make it better', 'magic': 'tell the steward plainly it is not finished, and go back to the bench to make it better'}, 'chance': 0.85}),
    ('wait, let the big firm come back twice, and let the price grow', 'G1', 'B.7', 0.5, '', {'self_control': '+', 'v': 'power, security', 'world': {'tribal': 'wait, let the trader come back at the next two gatherings, and let the offer grow', 'magic': 'wait, let the steward call twice more, and let the price grow'}, 'chance': 0.6}),
 ]},
{'name': 'the prototype catches fire',
 'stages': 'young_adult adult mature elder',
 'age': (20, 95),
 'alpha': 'W.4 U.1 B.4 R.4 G.1',
 'stakes': 0.5,
 'rate': 0.5,
 'tier': 'everyday',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'week',
 'roles': 'partner, colleague, mentor',
 'requires': 'inventor',
 'worlds': {'earth': 'a test run in the workshop goes wrong: smoke, a small fire put out at once, and a burnt hand '
                     'under the cold tap',
            'tribal': 'a trial of the new tool goes wrong by the fire: the pitch flares, and a burnt hand goes into '
                      'the stream',
            'magic': 'a trial of the new device goes wrong in the workshop: a split boiler, a small blaze, and a '
                     'burnt hand in the water butt'},
 'timing': {'times': 'per inventor a year: about 1 in 4 has a test that goes wrong badly enough to stop the work for '
                     'a while, most with no harm beyond a scare and a small burn (estimate); about 5 lives in 10,000 '
                     'come to live from their own inventions (catalogue share)',
            'gap_years': (1.0, 3.0)},
 'scenes': {'earth': [('',
                       'Ten minutes into the test run the prototype starts to smell, then to smoke, then a small '
                       'flame runs along the casing. {N} has it out with the extinguisher in seconds, but the '
                       'workshop is full of smoke and the back of {Ns} hand is sore where it touched the casing. It '
                       "is nothing a cold tap and a dressing will not mend. The backers' showing is in three weeks."),
                      ('W',
                       'There is a book of rules for the workshop, and {N} wrote half of it. Every one of them says: '
                       'stop, write it down, tell people.'),
                      ('U',
                       '{N} stands in the smoke already thinking: the casing, the wiring, the heat at the joint. A '
                       'failure is the most a test can ever tell anyone.'),
                      ('B',
                       "Three weeks to the showing, and the backers' money runs out in four. {N} thinks about what "
                       'the backers need to hear, and what they do not.'),
                      ('R',
                       '{Ns} heart is still going hard and {N} is half laughing. It nearly worked; for nine minutes '
                       'it was the best thing {N} has ever made.'),
                      ('G',
                       'The workshop is quiet again, the smoke drifting out through the open door into the garden. '
                       '{N} sits on the step with a wet cloth round the hand and lets the shaking stop.')],
            'tribal': [('',
                        'The new tool was to set the fire-pitch on the arrows faster, and at the trial the pitch '
                        'flared up all at once along the shaft. {N} beat it out in the sand and plunged the burnt '
                        'hand into the stream. The traders who backed the making with good flint come at the next '
                        'moon.')],
            'magic': [('',
                       "The new device was to turn the mill's stones by steam, and at the trial its little boiler "
                       'hissed, split a seam and set the shavings on the floor alight. {N} smothered it with a wet '
                       'sack, and stands with a burnt hand in the water butt. The merchant house that backs the work '
                       'comes to see it in three weeks.')]},
 'outcomes': (['The fault is found, the next run goes the full hour, and the backers leave the showing talking among '
               'themselves.',
               'Whatever {N} chose, the burn heals in a fortnight, and the work goes on wiser for the scare.'],
              ['The fault stays hidden somewhere in the design, and the next two runs end in smoke as well.',
               'The backers hear about it from someone else first, and they go cold on the whole thing.']),
 'options': [
    ('stop every test, write up exactly what happened, and send it to the backers', 'W1', None, 0.45, '', {'mark': 'owned up', 'v': 'conformity, security', 'world': {'tribal': 'stop every trial, and tell the traders exactly what happened when they come', 'magic': 'stop every trial, write it up exactly, and send it to the merchant house'}, 'chance': 0.7}),
    ('find the fault quietly, and keep it from the backers until it is fixed', 'U1', None, 0.45, '', {'mark': 'hid a wrong', 'closed': 'approval: a fault kept from the backers; backfire: it fails again, in front of them, at the showing', 'v': 'achievement, security', 'world': {'tribal': 'find the fault alone, and say nothing to the traders until it is right', 'magic': 'find the fault quietly, and keep it from the merchant house until it is mended'}, 'chance': 0.65}),
    ('show the backers how close it came, and ask for the next round now', 'B1', None, 0.45, '', {'grants': 'investors who back you', 'mark': 'took a wild risk', 'v': 'power, achievement', 'world': {'tribal': 'show the traders how near the tool came, and ask for more flint now', 'magic': 'show the merchant house how near it came, and ask for the next purse now'}, 'chance': 0.55}),
    ('air the workshop, rebuild it overnight, and run it again at dawn', 'R1', None, 0.45, '', {'grants': 'prototyping', 'body': 'light', 'self_control': '+', 'v': 'stimulation', 'world': {'tribal': 'make the shaft again by the fire tonight, and try it again at first light', 'magic': 'air the workshop, rebuild it tonight, and fire it again at dawn'}, 'chance': 0.65}),
    ('let the workshop and the hand rest a week, and come back to it calm', 'G1', None, 0.45, '', {'self_control': '+', 'v': 'security, universalism', 'world': {'tribal': 'let the hand heal and the work rest a moon, and come back to it calm'}, 'chance': 0.8}),
    ('fit a proper fire screen and a test bench, so it can be pushed hard safely', 'W1', 'R.7', 0.5, '', {'v': 'security, stimulation', 'world': {'tribal': 'clear a ring of sand to test in, so the next trial can be pushed hard safely', 'magic': 'build a stone test bench with a water tank, so it can be pushed hard safely'}, 'chance': 0.7}),
    ('redesign it to run cooler and simpler, with fewer parts to fail', 'U1', 'G.7', 0.5, '', {'aims': 'celebrated inventor', 'v': 'universalism, achievement', 'world': {'tribal': 'make it plainer, with less pitch and fewer bindings to fail', 'magic': 'redesign it to run cooler and plainer, with fewer seams to split'}, 'chance': 0.75}),
    ('ring the insurer at once, and get every safety paper in order before the showing', 'B1', 'W.7', 0.5, '', {'v': 'security, power', 'world': {'tribal': 'go to the elders first, before the story spreads, and make it right with them', 'magic': "go to the guild's inspector first, and get every paper in order before the showing"}, 'chance': 0.85}),
    ('film the next run from three sides, and set it off again to see why', 'R1', 'U.7', 0.5, '', {'grants': 'prototyping', 'v': 'stimulation, achievement', 'world': {'tribal': 'have two friends watch from either side, and fire the next shaft to see why', 'magic': 'set three apprentices to watch from three sides, and fire it again to see why'}, 'chance': 0.75}),
    ('ask the retired engineer down the road, and get it right before the rivals do', 'G1', 'B.7', 0.5, '', {'grants': 'mentor', 'door': True, 'v': 'achievement, benevolence', 'world': {'tribal': 'ask the oldest toolmaker of the band, and get it right before the next band does', 'magic': 'ask the old artificer down the lane, and get it right before the rival houses do'}, 'chance': 0.6}),
 ]},
{'name': 'the prototype works',
 'stages': 'young_adult adult mature elder',
 'age': (20, 90),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.03, 0.04, 0.03, 0.01),
 'drivers': 'era+.3 fortune+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, making, money',
 'horizon': 'months',
 'roles': 'partner, boss, friend, colleague, mentor',
 'requires': 'software developer | civil engineer | machinist | electrician | founder of a firm | apprentice',
 'tenure': (2.0, 100.0),
 'worlds': {'earth': "a working model of an invention of one's own, on the bench at last, and the question of what "
                     'to do with it',
            'tribal': "a new tool of one's own that works at last, and the question of whether to make it the work "
                      'of a life',
            'magic': "a working model of a device of one's own on the bench at last, and the question of whether to "
                     'live as an artificer'},
 'timing': {'times': 'per software developer, civil engineer, machinist, electrician or apprentice of two years, or '
                     'founder of a firm of one, with the knack for making things, a year: about 1 in 30 has a '
                     'working model of an invention of their own; most never make a living from one: about 5 lives '
                     'in 10,000 come to live from their own inventions for years, and about 2 in 1,000 hold a patent '
                     '(catalogue shares; patent studies find about 1.6 in 1,000 people hold one by their thirties)',
            'likelier': "years in a trade, a workshop or a bench of one's own, good years for new machines and new "
                        'ways of working, a partner who backs it, a lucky first buyer',
            'rarer': 'no time or money for it, a firm that owns whatever its staff make, a lean year, a family that '
                     'needs every evening',
            'gap_years': (3.0, 8.0)},
 'scenes': {'earth': [('',
                       'At a quarter to midnight on a Tuesday the thing on the bench does what it was built to do, '
                       'and then does it again, a hundred times, without a fault. {N} rings {partner} from the shed, '
                       'unable to say anything sensible. It has taken three years of evenings. Now there is a '
                       'working model, a notebook of drawings, a job to go to in the morning, and a choice.'),
                      ('W',
                       '{N} knows how this should be done: a patent filed first, every test written up, the safety '
                       'marks earned before a single one is sold.'),
                      ('U',
                       'It works, and {N} can already see four ways it could work better. The model on the bench is '
                       'the ninth version; the twelfth would be something else again.'),
                      ('B',
                       'For a year {N} has kept a list of everyone who might buy it, back it or copy it. The order '
                       'in which they are rung matters a great deal.'),
                      ('R',
                       '{N} wants to hand in the notice tomorrow, rent a unit, and make a living from this or go '
                       'broke trying.'),
                      ('G',
                       '{Ns} neighbours have watched the light in the shed for three years. The first ones, {N} '
                       'thinks, should go to the people up and down the street who put up with the noise.')],
            'tribal': [('',
                        'By the stream the new tool does what {N} meant it to: the hook holds every fish it takes, '
                        'and the scraper bites without slipping. The others crowd round to try it. {N} could go back '
                        'to the hunt as before, or become the one the bands come to for tools.')],
            'magic': [('',
                       'On the bench in the back room the little device turns, and turns, and does not stop: the '
                       'model {N} has worked at for three years. The master has seen it now. {N} could go back to '
                       "the master's orders, or ask the guild for an artificer's mark.")]},
 'outcomes': (['Within the year the first ones have gone to people who paid for them, and {N} is an inventor, with a '
               'living to make from it.',
               'Whatever {N} chose, the thing on the bench goes out into the world in some form, and {N} is proud of '
               'the road taken.'],
              ['The first buyers are slow, the money runs out before the orders come, and {N} goes back to the trade '
               'with the model on a shelf.',
               'A rival with deeper pockets brings out something very like it, and {Ns} version is lost in the '
               'crowd.']),
 'options': [
    ('file the patent first, and show it to makers with every test written up', 'W1', None, 0.45, '', {'title': 'inventor', 'grants': 'a patent of your own', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'v': 'conformity, security', 'world': {'tribal': 'show the elders first, so all know whose tool it is, and let each band see it tried', 'magic': "file for the guild's grant first, and show it to the workshops with every trial written up"}, 'chance': 0.25}),
    ('build three more versions until it is truly ready, then take it to market', 'U1', None, 0.45, '', {'title': 'inventor', 'mark': 'learned a skill', 'self_control': '+', 'identity': True, 'v': 'achievement, self-direction', 'world': {'tribal': 'make three more until it is truly right, then take it to the gathering', 'magic': 'build three more models until it is truly ready, then take it to the market'}, 'chance': 0.25}),
    ('patent it in your own name, and sell it hard to every buyer on the list', 'B1', None, 0.45, '', {'title': 'inventor', 'grants': 'a patent of your own', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'aims': 'celebrated inventor', 'identity': True, 'v': 'power, achievement', 'world': {'tribal': 'make sure every band knows whose tool it is, and trade it hard at every camp', 'magic': "take the guild's grant in your own name, and sell it hard to every buyer on the list"}, 'chance': 0.25}),
    ('hand in your notice, rent a unit, and make your living from it', 'R1', None, 0.45, '', {'title': 'inventor', 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'world': {'tribal': 'leave the hunt to the others, and live by making the tool from now on', 'magic': "leave the master's workshop, take a room of your own, and live by it"}, 'chance': 0.25}),
    ('make the first ones by hand for the street, and grow it from there', 'G1', None, 0.45, '', {'title': 'inventor', 'v': 'tradition, benevolence', 'world': {'tribal': 'make the first ones for your own hearth and the next, and let it grow from there', 'magic': 'make the first ones by hand for the lane, and grow it from there'}, 'chance': 0.25}),
    ('offer it to your own firm, for a bonus and a share in every one sold', 'B.5 G.5', None, 0.5, '', {'grants': 'stake in the firm', 'v': 'security, power', 'world': {'tribal': "give it to your own band's toolmakers, for the best share of every trade", 'magic': 'offer it to your own master, for a purse and a share in every one made'}, 'chance': 0.75}),
    ('take it to the trade fair on your own money, and see who bites', 'B.5 R.5', None, 0.5, '', {'grants': 'contact in the trade', 'door': True, 'v': 'stimulation, achievement', 'world': {'tribal': 'carry it to the great gathering yourself, and see which trader wants it', 'magic': 'take it to the great fair at your own cost, and see which merchant bites'}, 'chance': 0.75}),
    ('put the plans online for free, and see what other tinkerers make of it', 'U.5 R.5', None, 0.5, '', {'aims': 'inventor', 'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'show any toolmaker who asks how it is made, and see what they make of it', 'magic': 'nail the plans to the guildhall door for any tinker, and see what they make of it'}, 'chance': 0.75}),
    ('keep the job and the family evenings, and let it be a fine thing made', 'W.5 G.5', None, 0.5, '', {'self_control': '-', 'v': 'security, benevolence', 'world': {'tribal': 'keep to the hunt and the hearth, and let it be a fine thing made', 'magic': "keep the master's work and the household's evenings, and let it be a fine thing made"}, 'chance': 0.75}),
    ("write it up for the engineers' journal, with every measurement checked twice", 'W.5 U.5', None, 0.5, '', {'grants': 'name in the field', 'v': 'achievement, conformity', 'world': {'tribal': "tell the making of it at the gathering's fire, every step in its right order", 'magic': "write it up for the artificers' guild book, with every measure checked twice"}, 'chance': 0.75}),
 ]},
{'name': 'an invention in every home',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.03, 0.02),
 'drivers': 'era+.3 prosper+.2',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, money, publiclife',
 'horizon': 'years',
 'roles': 'boss, rival, partner, colleague, friend',
 'requires': 'inventor',
 'tenure': (4.0, 100.0),
 'worlds': {'earth': 'the invention sells, the big makers ring, and it could be in every home in the land, or in '
                     'hardly any',
            'tribal': 'other bands want the new tool, and it could become a tool every band makes, or be forgotten '
                      'in a few winters',
            'magic': 'the device sells at the fairs, the great houses send their stewards, and it could stand in '
                     'every household of the realm'},
 'timing': {'times': 'per inventor of four years or more a year: about 1 in 40 has a real chance to get an invention '
                     'into ordinary homes everywhere; most never do, and about 5 lives in 100,000 become inventors '
                     'whose invention most households know (catalogue share; estimate)',
            'likelier': 'good years when people buy new things, a patent held, a big maker looking for something '
                        'new, a name in the field',
            'rarer': "hard years, a rival's copy already in the shops, no money for the tooling, an invention only "
                     'specialists need',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'Four years after the first one sold, {Ns} invention has a following: a few thousand in use, '
                       'letters from strangers, a shop in the city that sells out every month. Now a big maker wants '
                       "to talk, a morning show wants a demonstration, and {rival}'s cheaper copy has turned up on a "
                       'market stall. This is the year it goes into every home, or goes back to being a good idea a '
                       'few people liked.'),
                      ('W',
                       "Every home means every safety standard, every shop's buyer and every rule about what may go "
                       'on a shelf. {N} has the forms spread out on the kitchen table.'),
                      ('U',
                       'At the price it costs now, only the keen buy it. {N} keeps coming back to one question: how '
                       'to make it so simple and so cheap that anyone would.'),
                      ('B',
                       'The big maker has shops on every high street. One signature on the right terms, and {Ns} '
                       'name goes into all of them; on the wrong terms, the name goes nowhere.'),
                      ('R',
                       '{N} would rather show it to people than talk about it: in town squares, at fairs, on the '
                       'morning show, wherever there is a crowd.'),
                      ('G',
                       'The letters are the best part: a farmer, a nurse, an old man who can open his own jars '
                       'again. {N} wants it to reach people like them, and to go on reaching them.')],
            'tribal': [('',
                        'Traders from three bands have asked for {Ns} new tool this summer, and at the gathering a '
                        "far band's toolmaker was already making a poor copy. Made well and shown widely, it could "
                        'become a tool every band makes; if not, it will be forgotten in a few winters.')],
            'magic': [('',
                       'The device sells out at every fair, the great houses send their stewards with contracts, and '
                       "a rival workshop's cheap copy has appeared in the market. {N} can see it standing in every "
                       'household of the realm, or fading into a curiosity in a few cabinets.')]},
 'outcomes': (['Within two years it is everywhere: in kitchens and sheds and workplaces up and down the land, and '
               'people who have never heard {Ns} name use it every day.',
               'Whatever {N} chose, the invention keeps its following, and {N} is glad of the way it went out into '
               'the world.'],
              ['The big push comes to nothing: a cheaper copy takes the shelves, and {Ns} invention stays a thing a '
               'few thousand people love.',
               'The year goes on meetings, forms and arguments, and at the end of it the invention is where it '
               'was.']),
 'options': [
    ('get it through every safety standard, so every shop in the land can stock it', 'W1', None, 0.45, '', {'title': 'celebrated inventor', 'grants': 'an invention in everyday use', 'v': 'conformity, security', 'world': {'tribal': 'make each one to the same sure pattern, so every band can trust it', 'magic': "get it through every guild's standard, so every shop in the realm may stock it"}, 'chance': 0.06}),
    ('redesign it until it costs a tenth as much, and anyone can afford one', 'U1', None, 0.45, '', {'title': 'celebrated inventor', 'grants': 'an invention in everyday use', 'self_control': '+', 'v': 'achievement, universalism', 'world': {'tribal': "make it so plain that any band's toolmaker can make it in an afternoon", 'magic': 'redesign it until it costs a tenth as much, and any household can afford one'}, 'chance': 0.06}),
    ('sign with the biggest maker in the land, on your own terms', 'B1', None, 0.45, '', {'title': 'celebrated inventor', 'grants': 'an invention in everyday use', 'v': 'power, achievement', 'world': {'tribal': 'give the strongest trader of the rivers the making of it, on your own terms', 'magic': 'sign with the greatest merchant house of the realm, on your own terms'}, 'chance': 0.06}),
    ('take it on the road, and show it to the crowd in every town square', 'R1', None, 0.45, '', {'title': 'celebrated inventor', 'grants': 'an invention in everyday use', 'identity': True, 'v': 'stimulation', 'world': {'tribal': 'carry it to every camp along the rivers, and show it off at every fire', 'magic': 'take it on the road, and show it off in every market square of the realm'}, 'chance': 0.06}),
    ('let it spread by word of mouth, family to family, the way good things do', 'G1', None, 0.45, '', {'title': 'celebrated inventor', 'grants': 'an invention in everyday use', 'v': 'benevolence, tradition', 'world': {'tribal': 'let it pass from hearth to hearth and band to band, the way good things do', 'magic': 'let it spread by word of mouth, household to household, the way good things do'}, 'chance': 0.06}),
    ('give the design away free, so every family that wants one can make it', 'R.5 G.5', None, 0.5, '', {'grants': 'good name in town', 'v': 'universalism, benevolence', 'world': {'tribal': 'show every band how to make it, freely, as the old ones gave the bow', 'magic': 'give the design away freely, so every household that wants one can make it'}, 'chance': 0.75}),
    ('license it to the big maker for a share of every one sold', 'U.5 B.5', None, 0.5, '', {'grants': 'shares', 'v': 'power, achievement', 'world': {'tribal': 'let the strongest trader make it, for a share of every trade', 'magic': 'license it to a great house for a share of every one sold'}, 'chance': 0.75}),
    ('take on an apprentice, and teach them the whole design from the first drawing', 'U.5 G.5', None, 0.5, '', {'grants': "apprentice of one's own", 'binds': True, 'v': 'benevolence, achievement', 'world': {'tribal': 'take a young one of the band, and teach them the whole making from the first stone', 'magic': 'take an apprentice, and teach them the whole design from the first drawing'}, 'chance': 0.75}),
    ('bring in investors, with a board and honest books, and make it at scale', 'W.5 B.5', None, 0.5, '', {'grants': 'investors who back you', 'v': 'security, power', 'world': {'tribal': 'bring in traders who will share their goods, with every share agreed before the elders', 'magic': 'bring in backers from the merchant houses, with a council and honest books'}, 'chance': 0.75}),
    ('keep faith with the small makers who took it on first, and stay small', 'W.5 R.5', None, 0.5, '', {'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': 'keep faith with the toolmakers of your own band who made it first, and stay small', 'magic': 'keep faith with the small workshops that took it on first, and stay small'}, 'chance': 0.75}),
 ]},
{'name': 'the safety test you could skip',
 'stages': 'young_adult adult mature elder',
 'age': (22, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.015, 0.01, 0.005),
 'drivers': 'stress+.2 money-.2',
 'tier': 'life event',
 'tone': 'trouble',
 'life': 'work, money',
 'horizon': 'months',
 'roles': 'boss, colleague, partner, friend',
 'requires': 'inventor | civil engineer | celebrated inventor | founder of a firm',
 'worlds': {'earth': 'the launch is next week, and the last safety test takes a month',
            'tribal': 'the bands gather in seven days to take the new tool, and its last trial takes a moon',
            'magic': "the great fair opens in a week, and the guild's last trial of the device takes a month"},
 'timing': {'times': 'per inventor, civil engineer or founder of a firm a year: about 1 in 80 faces a launch or a '
                     'handover with the last safety test still to run and a reason to skip it (estimate); product '
                     'recalls are common enough that most makers can name one; the four titles are about 3 lives in '
                     '100 (catalogue shares)',
            'likelier': 'a date already sold to the buyers, money running short, a test that takes longer than the '
                        'launch can wait, a design that has never failed so far',
            'rarer': 'a firm with a safety officer who can say no, buyers who check, a maker who has lived through a '
                     'recall',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'The launch is booked for next Thursday: the first orders signed, the boxes printed, a room '
                       'hired for the trade press. Then {colleague} comes in with the test plan and points at the '
                       'last line. The long-run safety test, a month of use without a break, has not been done; '
                       'everything else has passed. The buyers, the bank and {boss} would all rather not hear about '
                       'it, and nobody would know.'),
                      ('W',
                       '{N} signed the test plan six months ago, and it says plainly what has to pass before '
                       'anything is sold. A signature is a promise.'),
                      ('U',
                       '{N} looks at the results so far and runs the numbers again. The design is sound, almost '
                       'certainly. Almost.'),
                      ('B',
                       "A month's delay costs the orders, the room, the bank's patience and maybe the firm. {N} "
                       'weighs what it would cost to wait against what it would cost to be wrong.'),
                      ('R',
                       '{N} is sick of waiting. Every part has passed every test, the thing works, and next Thursday '
                       'it is meant to go out into the world.'),
                      ('G',
                       "The first buyers are people {N} knows: a farm, a builder's yard, the hardware shop in town. "
                       '{N} pictures the thing in their hands a year from now, still working.')],
            'tribal': [('',
                        'In seven days the bands gather, and each has asked for the new tool. The last trial, a '
                        'whole moon of hard use on the hunt, is not done, though every other trial went well. The '
                        'elders want the gift ready, and nobody would know.')],
            'magic': [('',
                       "The great fair opens in a week, the merchant houses have ordered, and the guild's last "
                       'trial, a month of turning without a rest, has not been run. Every other trial has passed. '
                       "The guild's inspector is busy, and nobody would know.")]},
 'outcomes': (['The thing goes out into the world and keeps working, year after year, and the buyers come back for '
               'more.',
               'Whatever {N} chose, the launch is a good one in the end, and {N} sleeps well the night after.'],
              ["The delay costs the first orders and the bank's patience, and the year is a hard one.",
               'Something goes wrong between the bench and the buyers, and {N} spends the season putting it right, '
               'one buyer at a time.']),
 'options': [
    ('delay the launch a month, and run the full test as the plan says', 'W1', None, 0.45, '', {'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'tell the bands to wait a moon, and finish the trial as the old way asks', 'magic': "put off the fair a month, and run the guild's full trial as written"}, 'chance': 0.75}),
    ('design a faster test that finds the same faults in a week', 'U1', None, 0.45, '', {'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'find a harder trial that tests the tool as well in seven days', 'magic': 'devise a faster trial that finds the same faults in a week'}, 'chance': 0.7}),
    ('pay a test house to run it round the clock, whatever it costs', 'B1', None, 0.45, '', {'v': 'power, security', 'world': {'tribal': 'give good furs to every hunter who will use it day and night until the gathering', 'magic': "pay the guild's testers to run it day and night, whatever it costs"}, 'chance': 0.75}),
    ('use it hard yourself first, every day until the launch', 'R1', None, 0.45, '', {'body': 'light', 'mark': 'took a wild risk', 'v': 'stimulation, benevolence', 'world': {'tribal': 'use it yourself, hard, on every hunt until the gathering', 'magic': 'work it yourself, hard, every day until the fair'}, 'chance': 0.65}),
    ('ring the first buyers yourself, tell them why, and ask them to wait', 'G1', None, 0.45, '', {'mark': 'owned up', 'v': 'benevolence, tradition', 'world': {'tribal': "go to each band's elders yourself, tell them why, and ask them to wait", 'magic': 'visit the first buyers yourself, tell them why, and ask them to wait'}, 'chance': 0.7}),
    ('launch with ten trial buyers who sign for it, and finish the test alongside', 'W.34 U.33 B.33', None, 0.5, '', {'v': 'security, achievement', 'world': {'tribal': 'give the tool to ten hunters who agree to try it, and finish the trial with them', 'magic': 'sell to ten trial buyers who sign for it, and finish the trial alongside'}, 'chance': 0.6}),
    ('call the team in, and run the test in shifts with them, day and night', 'W.34 R.33 G.33', None, 0.5, '', {'v': 'benevolence, conformity', 'world': {'tribal': "gather the band's young hunters, and work the trial in turns, day and night", 'magic': 'call the whole workshop in, and run the trial in shifts, day and night'}, 'chance': 0.75}),
    ('ask the standards office for a staged launch: half now, the rest after the test', 'W.34 B.33 G.33', None, 0.5, '', {'v': 'security, power', 'world': {'tribal': 'ask the elders to let half the bands take it now, and the rest after the trial', 'magic': "ask the guild's inspector for half the fair now, and the rest after the trial"}, 'chance': 0.6}),
    ('run the test cheaply in the yard, with what is to hand, and launch late', 'U.34 R.33 G.33', None, 0.5, '', {'v': 'self-direction, universalism', 'world': {'tribal': 'run the trial roughly by the camp, with what is to hand, and come late to the gathering', 'magic': 'run the trial cheaply in the yard, with what is to hand, and come late to the fair'}, 'chance': 0.75}),
    ('skip the last test, and launch on the day you promised', 'U.34 B.33 R.33', None, 0.5, '', {'grants': 'savings', 'takes_if_fails': 'an invention in everyday use; name in the field', 'mark': 'hid a wrong', 'closed': "law: a safety test skipped; backfire: it fails in use, a customer is hurt, and the recall and the papers take the invention's good name with it", 'self_control': '-', 'v': 'achievement, power', 'world': {'tribal': 'skip the last trial, and give the tool at the gathering as promised', 'magic': "skip the guild's last trial, and open at the fair as promised"}, 'chance': 0.75}),
 ]},
{'name': 'the garage invention',
 'stages': 'young_adult adult mature elder',
 'age': (18, 95),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.01, 0.01, 0.005, 0.005),
 'drivers': 'era+.3 fortune+.3',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, making',
 'horizon': 'months',
 'roles': 'friend, parent, partner, mentor, boss',
 'requires': 'apprentice | machinist | electrician | software developer | repair-cafe volunteer',
 'tenure': (1.0, 99.0),
 'worlds': {'earth': 'something built in the garage for the fun of it, and strangers start to ask where to get one',
            'tribal': 'a new thing made by the fire for the fun of it, and people from other bands start to ask for '
                      'one',
            'magic': 'a small device built in a back room for the fun of it, and strangers at the market start to '
                     'ask for one'},
 'timing': {'times': 'per apprentice, machinist, electrician or software developer of a year, or repair-café '
                     'volunteer of two, with the knack for making things, a year: about 1 in 150 builds something in '
                     'a garage or a back room that strangers start to ask about (estimate); most such things stay a '
                     'hobby, and about 5 lives in 10,000 come to live from their own inventions (catalogue share; '
                     'estimate)',
            'likelier': 'a garage or a workshop, good years for new gadgets, a friend who films it, a lucky stranger '
                        'who asks',
            'rarer': 'no space and no free evenings, a lean year, a family that needs the money, nobody to show it '
                     'to',
            'gap_years': (4.0, 10.0)},
 'scenes': {'earth': [('',
                       'It began as a way to stop the garage door sticking, and now it opens jars, lifts bikes onto '
                       'the wall and waters the tomatoes on a timer. {friend} filmed it for a laugh, and strangers '
                       'have started asking where to buy one. {N} has a workbench, a soldering iron, a few evenings '
                       'a week, and a feeling that this could be something, or nothing at all.'),
                      ('W',
                       'Nobody becomes an inventor by accident, {N} thinks. There are competitions, forms, safety '
                       'marks and a proper way in, and {N} would rather take it.'),
                      ('U',
                       '{N} can see exactly what is wrong with it: the motor is too big and the timer drifts. A year '
                       'of evenings would make it something else.'),
                      ('B',
                       'Strangers asking where to buy one means a market. {N} wonders who will be at the trade show '
                       'this spring, and what a backer would want in return.'),
                      ('R',
                       '{N} built it laughing, and the best things are the ones built laughing. Why not just put it '
                       'out there and see what happens?'),
                      ('G',
                       'The first person who asked was the old neighbour two doors down, who cannot reach the high '
                       'shelves any more. {N} thinks about the street before the world.')],
            'tribal': [('',
                        'It began as a way to keep the fire-sticks dry, and now the little thing of bark and sinew '
                        "keeps an ember alive through a whole day's walk. The band's young ones carry it about at "
                        'the camp, and people from the next band asked for one at the last meeting. {N} wonders '
                        'whether it is a toy or the start of something.')],
            'magic': [('',
                       'It began as a toy to amuse the household: a little brass bird that sings at sunrise. Now it '
                       'opens the shutters, rings for the baker and wakes the whole lane. Strangers at the market '
                       "have asked where to buy one, and a merchant's clerk has left a card.")]},
 'outcomes': (['A year later strangers are paying for it, a maker has taken it on, and {N} gives up the old work to '
               'be an inventor, with a bench and a list of orders.',
               'Whatever {N} chose, the thing made for fun turns out to be a good beginning, and {N} is still making '
               'things a year on.'],
              ['The interest fades as fast as it came, and the thing goes back to being a toy for the household.',
               'The answers are polite and few, and {N} puts the drawings in a drawer, where they stay for years.']),
 'options': [
    ("enter it in the national inventors' competition, with every form filled in", 'W1', None, 0.45, '', {'title': 'inventor', 'grants_if_fails': 'a long shot that missed', 'door': True, 'v': 'conformity, achievement', 'world': {'tribal': "bring it to the elders' meeting of the bands, where new things are judged", 'magic': "enter it for the guild's prize for new devices, with every form filled in"}, 'chance': 0.03}),
    ('spend a year of evenings perfecting it, then take it to a maker', 'U1', None, 0.45, '', {'title': 'inventor', 'grants_if_fails': 'a long shot that missed', 'habit': True, 'v': 'achievement', 'world': {'tribal': 'spend a winter of evenings making it right, then take it to the best toolmaker of the rivers', 'magic': 'spend a year of evenings perfecting it, then take it to a great workshop'}, 'chance': 0.03}),
    ('find a backer at the spring trade show, and sign before they think twice', 'B1', None, 0.45, '', {'title': 'inventor', 'grants_if_fails': 'a long shot that missed', 'v': 'power, achievement', 'world': {'tribal': 'find a strong trader at the spring gathering, and strike the bargain at once', 'magic': 'find a backer at the spring fair, and set your seal before the merchant thinks twice'}, 'chance': 0.03}),
    ('put the film of it online tonight, and see what happens', 'R1', None, 0.45, '', {'title': 'inventor', 'grants_if_fails': 'a long shot that missed', 'v': 'stimulation, hedonism', 'world': {'tribal': 'show it off at every fire of the gathering, and see what happens', 'magic': 'show it off in the market square on the feast day, and see what happens'}, 'chance': 0.03}),
    ('make one for every neighbour who asks, and let word travel', 'G1', None, 0.45, '', {'title': 'inventor', 'grants_if_fails': 'a long shot that missed', 'v': 'benevolence, tradition', 'world': {'tribal': 'make one for every hearth that asks, and let word travel down the river', 'magic': 'make one for every household in the lane that asks, and let word travel'}, 'chance': 0.03}),
    ("join the inventors' club at the library, and learn how patents work first", 'W.34 U.33 R.33', None, 0.5, '', {'v': 'self-direction, conformity', 'world': {'tribal': "sit with the old toolmakers at the gathering, and learn first how a tool becomes one's own", 'magic': "join the artificers' reading room at the guildhall, and learn how a grant on a design works"}, 'chance': 0.83}),
    ('show it to the boss, and ask for a place on the team that develops it', 'W.34 U.33 B.33', None, 0.5, '', {'grants': 'inner circle at work', 'door': True, 'v': 'security, achievement', 'world': {'tribal': "show it to the band's best toolmaker, and ask to help with the making of it", 'magic': 'show it to your master, and ask for a place at the bench that develops it'}, 'chance': 0.83}),
    ('let it go, and give the evenings back to the family and the job', 'W.34 B.33 G.33', None, 0.5, '', {'self_control': '-', 'v': 'security, benevolence', 'world': {'tribal': 'let it go, and give the evenings back to the hearth and the hunt', 'magic': "let it go, and give the evenings back to the household and the master's work"}, 'chance': 0.83}),
    ('build a second, better one just for the joy of it, and keep it at home', 'U.34 R.33 G.33', None, 0.5, '', {'grants': 'prototyping', 'v': 'self-direction, hedonism', 'world': {'tribal': 'make a second, better one just for the joy of it, and keep it at your own hearth', 'magic': 'build a second, better one just for the joy of it, and keep it for the household'}, 'chance': 0.83}),
    ('sell the first few at the weekend market, and see who comes back for more', 'B.34 R.33 G.33', None, 0.5, '', {'v': 'stimulation, power', 'world': {'tribal': 'trade the first few at the gathering, and see who comes back for more', 'magic': 'sell the first few at the weekend market in the square, and see who comes back for more'}, 'chance': 0.83}),
 ]},
{'name': 'the guild commissions a flying ship',
 'stages': 'adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 1.0,
 'rate': 0.3,
 'domain': 'career.5',
 'per_year': (0.0, 0.0, 0.0, 0.02, 0.02, 0.01),
 'drivers': '',
 'tier': 'life event',
 'tone': 'joy',
 'life': 'work, publiclife',
 'horizon': 'years',
 'roles': 'boss, rival, mentor, colleague',
 'requires': 'inventor | civil engineer | machinist',
 'tenure': (3.0, 99.0),
 'worlds': {'magic': "the artificers' guild wants a ship that flies, and will choose who builds it"},
 'only': 'magic',
 'timing': {'times': 'per artificer of three years, or engineer or machinist of the guild of six, in the magic world '
                     "a year: about 1 in 50 hears that the artificers' guild wants a ship that flies and will choose "
                     "who builds it (estimate); a ship that keeps the air is the realm's newest wonder, and few "
                     'artificers in a generation build one',
            'likelier': "a guild flush with the court's silver, a name for clever work, a flood or a famine that "
                        'needs fast carrying, an old artificer retiring',
            'rarer': 'lean years, a guild master with a favourite, an Order that frowns on new wonders, a workshop '
                     'far from the capital',
            'gap_years': (5.0, 10.0)},
 'scenes': {'magic': [('',
                       'The guild master reads the commission aloud in the long hall: the court wants a ship that '
                       "flies, to carry the realm's letters over the mountains in a day, and the guild will choose "
                       'who builds it. A model of a hull hangs from the rafters, and nobody has yet made one keep '
                       'the air. In the lanes behind the guildhall an enchanter sells bindings that make a thing '
                       "rise, for a price, and without the Order's leave."),
                      ('W',
                       'The guild has a code for every beam and rivet, learned the hard way over two hundred years '
                       'of fallen bridges. {N} means to build a ship that keeps every line of it.'),
                      ('U',
                       'Nobody knows yet why a bird stays up. {N} has watched gulls over the harbour for a month '
                       'with a notebook, and suspects it is not the flapping at all.'),
                      ('B',
                       "Whoever builds this ship will be the realm's artificer, with a hall of their own and the "
                       "court's ear. {rival} has already been seen dining with the guild master, and {N} has heard "
                       "about the enchanter's bindings."),
                      ('R',
                       '{N} wants to be the first one up there: over the rooftops, over the river, with the wind in '
                       'the rigging and the whole city looking up.'),
                      ('G',
                       'The hill-folk have flown great kites over the high pastures for longer than the guild has '
                       'existed. {N} wonders whether anyone in the long hall has ever thought to ask them.')]},
 'outcomes': (["On a still morning in late summer the ship lifts off the guild's field, turns once over the river, "
               'and the whole city comes out onto the roofs to watch.',
               'Whatever {N} chose, the guild remembers the year of the flying ship, and {Ns} part in it.'],
              ['The ship rises a few feet, lurches, and settles back onto the field, and the guild gives the '
               'commission to {rival}.',
               "The court's silver runs out before the hull is finished, and the commission is put away for a better "
               'year.']),
 'options': [
    ("draw the ship to the guild's every rule, and prove each beam on paper first", 'W1', None, 0.45, '', {'title': 'inventor', 'requires': 'civil engineer', 'without': 'impossible', 'v': 'conformity, security', 'chance': 0.25}),
    ('work out from first principles how wings and wind could carry a hull', 'U1', None, 0.45, '', {'title': 'celebrated inventor', 'requires': 'inventor', 'without': 'impossible', 'v': 'achievement, self-direction', 'chance': 0.06}),
    ('promise the guild a ship by midsummer, and hire the best hands in the city', 'B1', None, 0.45, '', {'title': 'celebrated inventor', 'requires': 'inventor', 'without': 'impossible', 'binds': True, 'v': 'power, achievement', 'chance': 0.06}),
    ('build a small ship in the yard with your own hands, and fly it yourself', 'R1', None, 0.45, '', {'title': 'inventor', 'requires': 'machinist', 'without': 'impossible', 'body': 'light', 'v': 'stimulation', 'chance': 0.25}),
    ('build it light, the way the birds and the old kite-makers of the hills do', 'G1', None, 0.45, '', {'title': 'inventor', 'requires': 'machinist', 'without': 'impossible', 'v': 'tradition, universalism', 'chance': 0.25}),
    ('build a kite-ship for the midsummer fair, and charge for the first rides', 'B.5 R.5', None, 0.5, '', {'v': 'stimulation, power', 'chance': 0.55}),
    ("go up to the hill-folk's kite-makers, and learn how their great kites ride the wind", 'R.5 G.5', None, 0.5, '', {'grants': 'mentor', 'v': 'self-direction, universalism', 'chance': 0.55}),
    ("buy an enchanter's binding that makes the hull rise, without the Order's leave", 'U.5 B.5', None, 0.5, '', {'grants': 'name in the field', 'requires': 'savings', 'without': 'means', 'lacking': 0.5, 'mark': 'defied an authority', 'closed': "approval: an enchanter's binding bought without the Order's leave; backfire: the binding fades with the year, and the enchanter's price to renew it rises each time", 'self_control': '-', 'v': 'power, achievement', 'chance': 0.93}),
    ('put the old artificer forward, who has waited all their life for this', 'W.5 G.5', None, 0.5, '', {'mark': 'helped someone in need', 'v': 'benevolence, universalism', 'chance': 0.55}),
    ('ask the guild for a year to build and test a small model first', 'W.5 U.5', None, 0.5, '', {'grants': 'prototyping', 'binds': True, 'v': 'security, achievement', 'chance': 0.55}),
 ]},
]

ECHOES = [
{'name': 'the calling, years later',
 'stages': 'young_adult adult mature elder',
 'age': (20, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.1,
 'tier': 'echo',
 'tone': 'mixed',
 'life': 'work, meaning',
 'horizon': 'months',
 'roles': 'friend, partner, mentor, rival, boss',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, the same kind of door opens a crack: a great '
                     'congregation writes, a firm asks after the old design, backers come back, an officer remembers '
                     'the crossing, families send from far away',
            'tribal': 'winters after the attempt that failed, the same kind of call comes again from the far bands, '
                      'for the keeper, the toolmaker, the trader, the leader of the guard or the healer',
            'magic': 'years after the attempt that failed, the same kind of letter comes again, under the same kind '
                     'of seal'},
 'timing': {'times': "per person who missed a long shot on one of the five callings' roads: about 1 in 8 meet the "
                     'same kind of door again years later (estimate); many clerics, inventors, founders, officers '
                     'and healers say they were taken on a later try, and few long shots land on the first one '
                     '(estimate)'},
 'after': "a long shot missed in one of the five callings' long shots ('a sermon that goes round the country', 'the "
          "garage invention', 'the market stall that became a chain', 'the field commission', 'the remedy that "
          "worked'), holding [a long shot that missed], within the month of the miss; now 20 or more, not at a "
          "road's summit ([head of a faith order], [celebrated inventor], [magnate], [general], [renowned healer]); "
          'the try is for the same title again ({missed})',
 'delay_years': (3, 15),
 'likelier': 'the work kept up since; much Red and Black in the colour history; time to spare; a mentor, old '
             'comrades or backers who remember',
 'rarer': 'stress above 1.5; little money; poor health',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, the same kind of door opens a crack: a letter from a '
                       'great congregation, a firm asking after the old design, backers who still remember the shop, '
                       'an officer who remembers the crossing in the flood, a family travelling a long way to ask '
                       'for {N} by name. {N} reads it twice, standing very still, and then sits down.'),
                      ('W',
                       'The first time, {N} did what was asked and it was not enough. Since then {N} has learned how '
                       'such doors are opened, step by step, and has kept every step.'),
                      ('U',
                       '{N} has gone over the first attempt more often than anyone knows, and can say now exactly '
                       'what was missing, and why it showed.'),
                      ('B',
                       'The people who decide are older now, and some of them know {Ns} name. The odds are still '
                       'long, but they are not the same odds.'),
                      ('R',
                       'The old wanting comes back all at once, as sharp as the first time. {N} is older, and has '
                       'long since stopped caring who thinks it foolish.'),
                      ('G',
                       '{friend} has said for years that one try is not a life. The people who stood by {N} the '
                       'first time are still here, and would stand by {N} again.')],
            'tribal': [('',
                        'Winters after the attempt that failed, a runner comes from the far bands with the same kind '
                        'of call as before. {N} hears it at the edge of the firelight, and the old wanting stirs.')],
            'magic': [('',
                       'Years after the attempt that failed, a letter comes under the same kind of seal as the '
                       "first, in a different clerk's hand. {N} reads it twice at the window, and does not go out "
                       'that day.')]},
 'outcomes': (['This time the answer is yes; {N} reads it twice, sits very still, and then goes out to tell the one '
               'person who stood by the first try.',
               'Whatever {N} chose, the second time feels different: steadier, and entirely {Ns} own.'],
              ['It is the same kind of no as last time, nearly to the word, and {N} finds that it stings less, and '
               'is glad to have gone back at all.',
               'The try gets further than before, and one person who matters says one true thing about it; {N} walks '
               'home the long way, in no hurry at all.']),
 'options': [
    ('answer by the book this time, every form and step done before the date', 'W1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'conformity, security', 'world': {'tribal': 'answer the runner by the old way this time, every step kept before the moon turns', 'magic': 'answer under seal this time, every form and step done before the date'}, 'chance': 0.04}),
    ('spend a year getting ready, and go back with everything learned since', 'U1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'binds': True, 'mark': 'learned a skill', 'v': 'achievement, self-direction', 'world': {'tribal': 'spend a winter getting ready, and go back with everything learned since'}, 'chance': 0.04}),
    ('go back only when someone who matters will speak for the try', 'B1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'self_control': '+', 'v': 'power, achievement', 'world': {'tribal': 'go back only when an elder of standing will speak for the try', 'magic': 'go back only when a patron of standing will speak for the try'}, 'chance': 0.04}),
    ('go back at once, older and bolder, and stake everything on it', 'R1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'mark': 'took a wild risk', 'v': 'stimulation, self-direction', 'chance': 0.04}),
    ('go back with everyone who stood by the first try behind it this time', 'G1', None, 0.45, '', {'title': '{missed}', 'grants_if_fails': 'a long shot that missed', 'identity': True, 'mark': 'made a friend', 'v': 'tradition, benevolence', 'world': {'tribal': 'go back with your own band behind it this time, every hearth of it', 'magic': 'go back with your own ward behind it this time, every lane of it'}, 'chance': 0.04}),
    ('let it pass for now, and keep a careful note of when the next door opens', 'W1', 'B.7', 0.5, '', {'habit': True, 'v': 'security, achievement', 'world': {'tribal': 'let it pass for now, and keep count of the moons until the next call'}, 'chance': 0.78}),
    ('let it pass, and spend the year on something new that has caught the eye', 'U1', 'R.7', 0.5, '', {'door': True, 'v': 'self-direction, stimulation', 'world': {'tribal': 'let it pass, and spend the winter on something new that has caught the eye'}, 'chance': 0.78}),
    ('put a younger one forward instead, and use your name to open the door', 'B1', 'G.7', 0.5, '', {'door': True, 'v': 'benevolence, power', 'world': {'tribal': 'name a younger one at the fire instead, and use your name to open the way'}, 'chance': 0.78}),
    ('help a younger one try, and stand beside them through every step', 'R1', 'W.7', 0.5, '', {'self_control': '+', 'v': 'benevolence, stimulation', 'chance': 0.78}),
    ('let it pass, and go back to where the first try began, to learn it again', 'G1', 'U.7', 0.5, '', {'door': True, 'self_control': '+', 'v': 'tradition, self-direction', 'chance': 0.78}),
 ]},
{'name': 'the long shot becomes a life of service',
 'stages': 'young_adult adult mature elder',
 'age': (25, 100),
 'alpha': 'W.2 U.2 B.2 R.2 G.2',
 'stakes': 0.7,
 'rate': 0.05,
 'tier': 'echo',
 'tone': 'joy',
 'life': 'work, meaning, community',
 'horizon': 'years',
 'roles': 'friend, partner, colleague, mentor',
 'once': True,
 'worlds': {'earth': 'years after the long shot that missed, a young one in the same trade asks for help, and the '
                     'old attempt comes into the room with the one who made it',
            'tribal': 'winters after the attempt that failed, a young one of the band asks to learn, and the telling '
                      'of the attempt comes with the teaching',
            'magic': 'years after the attempt that failed, a young one of the guild asks to be taught, and the tale '
                     'of it comes with the teacher'},
 'timing': {'times': "per person who missed a long shot on one of the five callings' roads: about 1 in 10 come to "
                     'serve at the rung they hold, teach a young one or hold a door open for others, years later '
                     '(estimate); many who teach the young in faith, engineering, business, the forces and healing '
                     'once tried for something bigger themselves (estimate)'},
 'after': "a long shot missed in one of the five callings' long shots (as for 'the calling, years later'), holding "
          "[a long shot that missed]; now 25 or more, not at a road's summit",
 'delay_years': (5, 30),
 'likelier': "years gone by since the attempt; teaching, a mentor or an apprentice of one's own; much White and "
             'Green in the colour history',
 'rarer': 'stress above 1.5; poor health',
 'scenes': {'earth': [('',
                       'Years after the long shot that missed, a young one turns up at {Ns} door with the same look '
                       '{N} once had: a new minister with a sermon in a folder, an apprentice with a drawing of a '
                       'machine, a shop assistant with a plan, a soldier who wants to lead, a student nurse who '
                       'wants to know how it is done. Before anything else, the young one asks whether {N} ever '
                       'tried for something big.'),
                      ('W',
                       '{N} tells it straight: what was asked, what {N} gave, and the answer that came back. Then '
                       'the two of them start on the work, because that is how it should be done.'),
                      ('U',
                       'Over the years {N} has understood the attempt better than at the time: what the people who '
                       'chose were looking for, and what {N} had not yet learned. That is worth passing on.'),
                      ('B',
                       'It has become a good story, and {N} knows how to tell it: the long odds, the nerve, the near '
                       'thing at the end. A story like that opens doors for whoever hears it.'),
                      ('R',
                       'The ache has mostly gone, and what is left is the memory of the nerve it took. {N} would '
                       'like the young one to feel that once.'),
                      ('G',
                       'The attempt is part of {Ns} life now, like the old house and the long friendships. What '
                       'matters today is the young one at the door, who is nervous and trying not to show it.')],
            'tribal': [('',
                        'One winter a young one of the band asks {N} to teach them, and asks too whether it is true '
                        'that {N} once went to the far bands for something great and came back without it. The fire '
                        'goes quiet to hear the telling.')],
            'magic': [('',
                       'A young one of the guild asks {N} to teach them, and asks too whether {N} once tried for the '
                       'great hall and was turned away. The workshop goes quiet to hear the tale.')]},
 'outcomes': (['The young one comes back the next week, and the week after, and years later tells someone else that '
               'it all began at {Ns} door.',
               'Whatever {N} chose, the old attempt has found its place in the life, and {N} no longer flinches when '
               'it comes up.'],
              ['The young one drifts off after a month, and {N} goes back to the work with the old story still '
               'untold.',
               'Someone asks whether it was worth it, the answer comes out sharper than {N} meant, and {N} turns it '
               'over for a week.']),
 'options': [
    ('serve at the post already held, every week for years, and never miss a duty', 'W1', None, 0.45, '', {'grants': 'good name in town', 'identity': True, 'mark': 'kept your word', 'v': 'benevolence, conformity', 'world': {'tribal': "keep your place in the band's work, every day for years, and never miss a duty", 'magic': 'serve at the post already held, every rest day for years, and never miss a duty'}, 'chance': 0.78}),
    ('take the young one on, and teach them everything the long shot taught', 'U1', None, 0.45, '', {'grants': "apprentice of one's own", 'habit': True, 'v': 'achievement, benevolence', 'world': {'tribal': 'take the young one at your side, and teach them everything the long try taught'}, 'chance': 0.78}),
    ('use the name the attempt made to raise a fund for the young who try next', 'B1', None, 0.45, '', {'identity': True, 'v': 'power, benevolence', 'world': {'tribal': 'use the name the attempt made to gather gifts for the young ones who try next', 'magic': 'use the name the attempt made to raise a purse for the young who try next'}, 'chance': 0.78}),
    ('let the old attempt go for good, and throw everything into the work at hand', 'R1', None, 0.45, '', {'habit': True, 'v': 'hedonism, stimulation', 'chance': 0.78}),
    ('tell the whole story to the family one evening, and let them keep it', 'G1', None, 0.45, '', {'v': 'tradition, benevolence', 'world': {'tribal': 'tell the whole telling to your own hearth one night, and let them keep it'}, 'chance': 0.78}),
    ('hold the door open: speak up for every newcomer who tries what you tried', 'W1', 'R.7', 0.5, '', {'door': True, 'v': 'universalism, benevolence', 'world': {'tribal': 'hold the way open: speak at the fire for every young one who tries what you tried'}, 'chance': 0.78}),
    ('write down what the attempt taught, and leave it where the young will find it', 'U1', 'G.7', 0.5, '', {'self_control': '+', 'mark': 'learned a skill', 'v': 'universalism, tradition', 'world': {'tribal': "put what the attempt taught into a telling, and leave it with the band's young", 'magic': "write out what the attempt taught, and leave the pages in the guild's library"}, 'chance': 0.78}),
    ('set up a small yearly prize in the trade for the best first attempt', 'B1', 'W.7', 0.5, '', {'binds': True, 'grants': 'good name in town', 'v': 'power, universalism', 'world': {'tribal': 'give a fine gift each summer to the young one of the band whose first try was boldest', 'magic': 'found a small yearly purse in the guild for the best first attempt'}, 'chance': 0.78}),
    ('talk the whole attempt through, all night, with the friend who was there', 'R1', 'U.7', 0.5, '', {'door': True, 'v': 'stimulation, self-direction', 'world': {'tribal': 'talk the whole attempt through by the fire, all night, with the friend who was there'}, 'chance': 0.78}),
    ("help the town's young ones set up on their own, as the attempt once tried to", 'G1', 'B.7', 0.5, '', {'habit': True, 'v': 'benevolence, achievement', 'world': {'tribal': "help the band's young ones make their own way, as the attempt once tried to", 'magic': "help the ward's young ones set up on their own, as the attempt once tried to"}, 'chance': 0.78}),
 ]},
]

EVENTS_READ = []

MARKS = {}
