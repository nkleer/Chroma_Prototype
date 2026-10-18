# S6 "Seen it done" (chroma-ideas/social-mechanics.md S6; Emren's card 10-10 09:21 UTC "v22.3"; its own switch, off).
# Kept with the other social words. The option row says whether they have seen anyone take this path or this way.
# SEEN  seen (a model they know succeeded), none (no one they know has), wrong (they saw it fail for someone), far (a
#       model far above them, three rungs or more, or 25 years older), and dream (a dream between 8 and 20 seeded from
#       a model). Slots {N}, {Ns} and {who} (the model, as the game names them: her aunt Mira); none has no {who}.
#       Full sentences; {who} never opens one, since it starts lower case.
SEEN = {
    'seen': ['{N} has seen it done: {who}.', '{N} watched {who} do it, and it worked.',
             '{N} knows it can be done: {who} did it.'],
    'none': ['No one {N} knows has done this.', '{N} has never seen anyone do this.',
             'Nobody in {Ns} world has tried this.'],
    'wrong': ['{N} saw it go wrong for {who}.', '{N} remembers how it went for {who}, and it went badly.',
              'It ended badly for {who}, and {N} was there to see it.'],
    'far': ['{N} has seen it done, but only by {who}, far out of reach.',
            '{N} looks up to {who}, but that life feels a world away.'],
    'dream': ['{N} dreams of doing what {who} does, one day.', 'Since knowing {who}, {N} has wanted the same.',
              '{N} plays at being {who}, over and over.'],
}
