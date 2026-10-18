# S3 "Their places' eyes" (chroma-ideas/social-mechanics.md S3; Emren's card 10-10 09:07 UTC "v22.3"; its own switch,
# off). How a place reads what the character did, by the place's face (the reader) and the act's colour.
# READ  "reader.act" (5 x 5): gift (the place thinks well of it) and danger (it thinks badly of it). Each is a clause
#       that follows "thinks you": past tense, second person, lower case, no end stop, naming no type of person.
# TALK  the line that brings a place's reading back through a go-between: slots {go} (their name), {place} (the
#       place's short name) and {read} (a READ clause); good, bent (the story has changed on the way) and warn.
READ = {
    'W.W': dict(gift='did the right thing by everyone, and kept to the rules',
                danger='stuck to the rules even when people were hurt by them'),
    'W.U': dict(gift='thought it through and did it properly',
                danger='put a clever plan ahead of the people it touched'),
    'W.B': dict(gift='looked after your own and paid your way',
                danger='put yourself first and let the rest of us down'),
    'W.R': dict(gift='stood up for someone when it mattered',
                danger='acted on a whim and left others to clear up after you'),
    'W.G': dict(gift='kept faith with your family and the old ways',
                danger='put your own people before what was fair'),
    'U.W': dict(gift='followed a fair process and stuck to it',
                danger='did what you were told without asking why'),
    'U.U': dict(gift='worked it out and got it right', danger='thought about it so long that you missed the moment'),
    'U.B': dict(gift='saw the opening and used it well', danger='were too clever for your own good'),
    'U.R': dict(gift='trusted your gut, and it paid off', danger='acted before you thought, and it showed'),
    'U.G': dict(gift='kept to what has always worked', danger='would not change even when the facts did'),
    'B.W': dict(gift='earned people\'s trust, and that is worth something', danger='let the rules tie your hands'),
    'B.U': dict(gift='played it smart and came out ahead', danger='knew better and still did not act on it'),
    'B.B': dict(gift='looked after yourself, and nobody can blame you', danger='got greedy and showed your hand'),
    'B.R': dict(gift='went after what you wanted and got it', danger='threw it all away on a passing feeling'),
    'B.G': dict(gift='kept hold of what is yours and your family\'s', danger='clung to the old ways and lost out'),
    'R.W': dict(gift='stood by your word when it was hard', danger='chose the rulebook over the people you love'),
    'R.U': dict(gift='knew what you were doing, and did it with nerve',
                danger='turned something warm into a cold sum'),
    'R.B': dict(gift='fought for what you wanted, and good for you', danger='sold out the people who stood by you'),
    'R.R': dict(gift='followed your heart, whatever anyone said', danger='burned too hot and hurt the people near you'),
    'R.G': dict(gift='stood by your own people all the way', danger='let old habits keep you from living'),
    'G.W': dict(gift='kept faith with what the place holds dear', danger='put outsiders\' rules above your own people'),
    'G.U': dict(gift='learned the old ways and understood them',
                danger='thought you knew better than those who came before'),
    'G.B': dict(gift='made sure the family will not go short', danger='put your own gain above your own people'),
    'G.R': dict(gift='showed real heart for the people here', danger='forgot where you came from in the rush'),
    'G.G': dict(gift='did what has always been done here, and did it well',
                danger='would not let anything change, even for the better'),
}

