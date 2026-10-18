# PLACE_NAME  the word for their name at a place, shown in "your places": (rep_min, word) pairs, best first; the game
#             takes the first pair whose rep_min the life's rep there (-1 to 1) reaches. A new face (rep 0) is known.
PLACE_NAME = [(.6, 'well thought of'), (.3, 'liked'), (-.1, 'known'), (-.3, 'talked about'), (-.6, 'frowned on'),
              (-1, 'a bad name')]

TALK = {
    'good': ['{go} says {place} thinks you {read}.', 'Word from {place}, through {go}: they think you {read}.',
             '{go} heard it at {place}: people there think you {read}.'],
    'bent': ['{go} says {place} has it that you {read}, though that is not quite how it went.',
             'By the time it reaches you through {go}, {place} thinks you {read}.'],
    'warn': ['{go} warns you that {place} thinks you {read}.',
             '{go} lowers their voice: at {place} they say you {read}.'],
}

