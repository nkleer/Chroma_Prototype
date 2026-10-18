# SHADOW        each face's shadow side (phase 5, N5): what the face turns into when events push it there
SHADOW = {
    'rule.W': "Rule for rule's sake: the form before the person, harsh with small wrongs, outsiders judged by rules made without them.",
    'rule.U': 'The cold file: the plan that fits the record, not the people; the reform studied until its moment passes; the expert no one may question.',
    'rule.B': "Over-reach: office used to reward one's own, every ally a debt to call in, and a faction head who stands alone when the tide turns.",
    'rule.R': 'The mob and the burnt bridge: anger that skips the hearing, punishes the wrong person, and tears down what it cannot replace.',
    'rule.G': "Rule of the past: 'it has always been so', while the newcomer and the young never get a say.",
    'gather.W': 'Belonging as policing: gossip keeps people in line, a seat depends on behaving, newcomers wait years on probation.',
    'gather.U': 'Talk instead of action: a closed circle of the clever, newcomers mocked for the wrong word, every evening a contest to win.',
    'gather.B': "The clique and the fixer: doors shut to keep value in, friends kept for use, the town's business done in a back room.",
    'gather.R': 'Brawls, drink that becomes the habit, nights that cost the morning, bridges burned in one loud hour.',
    'gather.G': 'Closed to outsiders: feasts that keep the old feud, newcomers strangers after twenty years, the young drifting off unheard.',
    'arts.W': "Art made to order: the anthem one must stand for, the censor's pen, the classic no one may question or change.",
    'arts.U': 'Art for the few: the closed school and its jargon, the critic who sneers at what people love, the cold master who breaks a pupil.',
    'arts.B': "Fame at any price: the work bent to whatever sells, the patron's pet, the star who uses everyone and is alone when the applause stops.",
    'arts.R': 'Excess and burnout: nights that wreck the body, cruelty passed off as honesty, the troupe that splits in a rage, a gift spent before it grows.',
    'arts.G': "Closed to the new and the stranger: the tune that must never change, the newcomer's song mocked, tradition used to keep people in their place.",
    'faith.W': 'The fold that polices its own: piety watched, the one who strays shamed or shut out, helpers who give until empty.',
    'faith.U': 'Faith argued into a cold system: hair-splitting that divides congregations, pride over the simple faithful, doubt that never lands.',
    'faith.B': 'Faith as a lever over others: blessings sold, fear of the dead turned into fees, the founder who owns the followers.',
    'faith.R': 'Fervour that burns out: zeal that turns on the doubter, the newly devout who cut every old tie, a crowd that hunts sinners.',
    'faith.G': 'The rite kept after its reason is lost: fatalism in a plague, a circle closed to strangers, change refused while the roof falls in.',
    'care.W': "Rigid care: the form before the patient, visiting hours that shut out kin, the 'deserving' poor judged at the door, a carer who gives until empty.",
    'care.U': 'Stuck in the case: the patient as a file, slow while the illness moves, cold with the frightened, or keen on a remedy before it is safe.',
    'care.B': 'Over-reach: care only for those who pay, the name before the patient, mistakes hidden to guard it, and a healer no colleague will stand beside.',
    'care.R': "Burnout: risks taken with other people's bodies, heroics before the facts, the rescuer worn out, the long dull care left to others.",
    'care.G': 'Stuck in its ways: harmful old remedies, the healer called too late, and the daughter who carries it all because she always has.',
    'learn.W': 'Rote and obedience: sitting still graded above thinking, the odd child shamed, and the rule kept long after its reason.',
    'learn.U': 'The ivory tower: knowledge kept in its own language, cold to those it should serve, blind to what it cannot measure.',
    'learn.B': 'Credentials as a gate: knowledge hoarded, every classmate a rival, the shut-out told they lacked merit, and at the top, no peers left.',
    'learn.R': 'Half-finished and reckless: the basics skipped, the careful mocked, and the mishap that hurts others because no one checked.',
    'learn.G': "We always did it so: the stranger's knowledge refused, the child who asks why silenced, and a harmful old remedy kept because it is old.",
    'prod.W': 'Closed rolls and rigid rules: the newcomer kept out, the better method refused because it breaks the code, the slow hand shamed.',
    'prod.U': 'People as parts: a clock over every task, the plan that ignores the field and the crew, trials weighed while the season passes.',
    'prod.B': 'Over-reach and use: wages squeezed, safety cut, partners dropped when they stop paying, and the owner alone atop a failing firm.',
    'prod.R': 'Burnout and short sight: the half-finished, the rush that strips a field or a sea, one risk too many, the crew left behind.',
    'prod.G': 'Stuck in its ways: the old method kept while the yield fails, outsiders never taken on, children bound to a trade they never chose.',
    'comm.W': 'Rules as a wall: closed rolls, licences only insiders get, prices fixed so low the grower starves, and the newcomer fined for selling.',
    'comm.U': 'The model above the people: speculation on paper, a clerk who forecloses by the numbers, risk spread so cleverly no one sees the crash.',
    'comm.B': 'Over-reach: every bargain pressed to the last coin, rivals bought out, the debtor squeezed dry, and a fortune that leaves its maker rich and alone.',
    'comm.R': "Ruin by risk: the hunch that takes the family's savings, every supplier's bridge burned, the stall abandoned when the thrill is gone.",
    'comm.G': 'Kin first: the stranger pays double, a gift that cannot be refused becomes a chain, and the old way is kept while the trade dies.',
    'prot.W': "The heavy hand: order put above people, the poor quarter's small wrongs punished hard, orders obeyed without asking whom they hurt.",
    'prot.U': 'Watching everyone just in case: files on neighbours, people as pins on a map, a warning weighed so long the danger arrives first.',
    'prot.B': 'Loyal only to the fee: the company that changes sides for better pay, the guard who lets the street burn, and no one left who trusts them.',
    'prot.R': 'The fight for its own sake: the brawl sought out, revenge without end, comrades led into a fight they did not need, a body worn out young.',
    'prot.G': 'Fear of the stranger: the newcomer blamed for every theft, the posse that takes justice into its own hands, the old feud kept alive.',
}

# GREY          the shadow side of each sphere as the town sees it (phase 5, N5's grey share): name, line, and the
#               lines when it grows and when it shrinks. N5's moments wait for the Crime pack.
GREY = {
    'rule': dict(name='the quiet word', line='Where the open court fails people, cases are settled by a quiet word, a cousin in the office, or a favour owed.', grows='More people settle things off the record this year.', shrinks='The quiet word counts for less; people take their cases to the open court.'),
    'gather': dict(name='the after-hours door', line='When the open rooms close or turn people away, the evening moves behind the after-hours door.', grows='The after-hours door is busier than it was.', shrinks='Fewer evenings end behind the after-hours door.'),
    'arts': dict(name='the copy under the counter', line='Where the open stage is closed or costly, songs, films and books pass hand to hand, copied and unpaid.', grows='More copies change hands under the counter.', shrinks='People pay for the songs and shows they love again.'),
    'faith': dict(name='the private healer of souls', line='When the open house of worship fails people, some turn to the charm seller, the paid prophet and the closed circle.', grows='The charm sellers and closed circles gain a following.', shrinks='Fewer people go to the charm sellers this year.'),
    'care': dict(name='the quack and the cash clinic', line='Where open care is slow or dear, people buy from the quack, the cash clinic and the pills sold online.', grows='More people buy their care off the books.', shrinks='People trust the open clinics again.'),
    'learn': dict(name='the bought certificate', line='When open schooling fails people, diplomas are bought, exams are sold and the right school is a matter of money.', grows='Bought certificates are easier to find than they were.', shrinks='A certificate means what it says again.'),
    'prod': dict(name='the cash job', line='Where open work is scarce or unfair, work goes off the books: cash in hand, no contract, no cover.', grows='More work is cash in hand this year.', shrinks='More of the work in town is on the books again.'),
    'comm': dict(name='goods under the counter', line='When the open market fails people, trade moves under the counter: the man with the van, the loan shark, the unpaid tax.', grows='More trade goes under the counter.', shrinks='Fewer people need the man with the van.'),
    'prot': dict(name='the protection that is paid for', line='Where the watch fails people, safety is bought from a crew, a racket or a private guard who answers to no one.', grows='More shops pay someone for protection.', shrinks='Fewer people pay a crew to keep them safe.'),
}

# DEEP          the deep state's panel words (phase 5): label, hover line, and the lines when it begins and ends.
#               Fills: {N} and the engine's own ({hours}, {who}, {years}, {owed}, {creditors}, {holdings}, {credentials}).
DEEP = {
    'care_load': dict(name='Care given', hover='The hours given each week to someone who cannot manage alone.', begins="{N} gives {hours} hours a week to {who}'s care.", ends='The care {N} gave is over, and the hours are their own again.'),
    'service': dict(name='Years of service', hover='Time in the forces or the watch, as a chapter of a life with its start, its cost and its return.', begins='{N} has served {years} years.', ends="{N}'s years of service are behind them."),
    'debts': dict(name='Debts and dues', hover='What is owed and to whom: the bank, a lender, family, friends, or a debt of honour.', begins='{N} owes {owed} in all, to {creditors}.', ends="{N}'s last debt is paid."),
    'holdings': dict(name='Holdings', hover='What is owned and kept: a home, land, a stall, savings, a share in a firm.', begins='{N} holds {holdings}.', ends='{N} has nothing left in their own name.'),
    'credentials': dict(name='Papers and qualifications', hover='The certificates, licences and degrees that open doors, and the ones still missing.', begins='{N} holds {credentials}.', ends='{N} holds no papers that count here.'),
}

