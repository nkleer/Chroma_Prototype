# S5 "Sacred lines" (chroma-ideas/social-mechanics.md S5; Emren's card 10-10 09:15 UTC "v22.3"; its own switch, off).
# A line forms in a way that has led for years and twice cost them something real; offers that touch it become pivotal.
# LINE  by line kind (the Outer world's keys in dynamics.json "offers"; promise W, truth U, own_say B, loved R, home G):
#   name      the player-facing name of the line (character sheet heading, hover)
#   will_not  three sheet lines, each after the game's lead-in "Will not: ", so a clause: lower case, no end stop
#   peace     a clause for the peace reading ("She died true to ..."), lower case, no end stop
#   formed    the story line the year the line forms
#   held      the closing paragraph's line when the line was never crossed and was tested at least once
#   crossed   the closing paragraph's line when it was crossed and never healed
#   healed    the closing paragraph's line when it was crossed and later healed (amends or reflection)
LINE = {
    'promise': dict(name='A promise kept',
                    will_not=['break a promise once it is given', 'take a price to look the other way',
                              'jump the queue that everyone else waits in'],
                    peace='true to every promise they gave',
                    formed='{N} has kept their word twice when it cost them dearly, and it is part of them now.',
                    held='{N} was offered a price to break their word, and never took it.',
                    crossed='{N} once broke their word for a price, and it stayed with them to the end.',
                    healed='{N} once broke their word for a price, and later did all they could to make it right.'),
    'truth': dict(name='The truth of what they know',
                  will_not=['swear to something they did not see', 'sign a report they know is false',
                            'keep quiet about what they know for money'],
                  peace='true to what they knew',
                  formed='{N} has told the truth twice when a lie would have paid, and it is part of them now.',
                  held='{N} was offered a price to say what was not so, and never took it.',
                  crossed='{N} once said what was not so for a price, and it stayed with them to the end.',
                  healed='{N} once said what was not so for a price, and later told the truth, whatever it cost.'),
    'own_say': dict(name='Their own say',
                    will_not=['sell their vote or their voice', 'sign away what is theirs to decide',
                              'owe their place to anyone who bought it'],
                    peace='their own person to the last',
                    formed='{N} has twice refused to let anyone else decide for them, and paid for it.',
                    held='{N} was offered a price for their say over their own life, and never sold it.',
                    crossed='{N} once sold their say over their own life, and it stayed with them to the end.',
                    healed='{N} once sold their say over their own life, and later took it back.'),
    'loved': dict(name='The people they love',
                  will_not=['give up a friend for their own good', 'sell out the people who stood by them',
                            'trade away the thing that makes them feel alive'],
                  peace='true to the people they loved',
                  formed='{N} has twice stood by the people they love when it cost them, and it is part of them now.',
                  held='{N} was offered a price to give up the people they loved, and never took it.',
                  crossed='{N} once gave up someone they loved for a price, and it stayed with them to the end.',
                  healed='{N} once gave up someone they loved for a price, and later stood by them again.'),
    'home': dict(name='Home and kin',
                 will_not=['sell what was the family\'s', 'leave home and kin for a better wage',
                           'let the old place go for money'],
                 peace='true to home and kin',
                 formed='{N} has twice put home and kin before gain, and it is part of them now.',
                 held='{N} was offered a price for home and kin, and never let them go.',
                 crossed='{N} once let home go for a price, and it stayed with them to the end.',
                 healed='{N} once let home go for a price, and later went back to give what they could.'),
}

