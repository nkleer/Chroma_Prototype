# Chroma Library: words for the played game (implementation list "v22", stage 1). Library thread, 2026-10-09.
# Plain data: nothing is imported. The game reads it; the engine does not, so lives with no player are unchanged.
# Keys, fills and what chooses each variant: chroma-library/INTERFACE.md, "earth_story.py". Checks:
# chroma-library/tests/check_story.py (fills, length, no color named, timeless setting, safety words).
#
# SONG          the end of a life as a bard's song (item 1), replacing the placeholder words of game.py life_paragraph()
#               key for key; SONG_WORLD holds the words that differ in the tribal and magic worlds.
# MARK_SAY      each history mark as the song says it, in the third person ("kept their word").
# LAST_TALK     the last conversation with the voice (P5's, joined to item 1): what it gave, what it cost, whether
#               they were glad; read from trust per color and the pushes they accepted or resented.
# VOICE         the voice in the story (item 3): its name, the character's answers by color distance and trust, the
#               outcome, trust turning, identity change, chapter, end and Book lines.
#
# Every choice of words is read from the life (Emren 10-09: "not random, related to outcomes, preferences, moments and
# choices of the player"); none is drawn by chance or taken in turn. INTERFACE.md names each selector.
# The song speaks of the character as "they" (as the game's song does). The other lines name them once with {N} (or
# {Ns}, the possessive) and say "they" after, as the game does; the character's own words are in the first person.
# No line names a color.

# ======================================================================================================== the song
SONG = {
    # the life's two longest-held colors, as "{ep0} and {ep1}" (lead first)
    "epithet": dict(W="steadfast", U="many-minded", B="far-reaching", R="fire-hearted", G="deep-rooted"),

    # the opening, by the lead color: "full" when the life reached 60, "short" when it ended sooner. Fills {N} {ep} {age}
    "open": dict(
        W=dict(full="Sing, Muse, of {N}, {ep}, who kept faith with others for {age} years",
               short="Sing, Muse, of {N}, {ep}, who kept faith with others through {age} short years"),
        U=dict(full="Tell me, Muse, of {N}, {ep}, the one of many turns, who wondered at the world for {age} years",
               short="Tell me, Muse, of {N}, {ep}, the one of many turns, who had only {age} years to wonder in"),
        B=dict(full="Of ambition and its price I sing, and of {N}, {ep}, who made their own way for {age} years",
               short="Of ambition and its price I sing, and of {N}, {ep}, who made their own way and had only {age} years to make it"),
        R=dict(full="Sing, goddess, of the fire of {N}, {ep}, who burned bright for {age} years",
               short="Sing, goddess, of the fire of {N}, {ep}, who burned bright and fast, {age} years and gone"),
        G=dict(full="Of roots and of returning I sing, and of {N}, {ep}, who belonged to their place for {age} years",
               short="Of roots and of returning I sing, and of {N}, {ep}, whose place held them only {age} years")),
    # a life of four identities or more takes the opening of the old book of changes. Fills {N} {ep} {age} {n}
    "open_many": "My mind is bent to tell of bodies changed into new forms: of {N}, {ep}, who in {age} years was {n} people, and every one of them themselves",
    "numbers": ["no one", "one", "two", "three", "four", "five", "six"],

    # the first stanza: an identity that began in childhood (before 18), or later. Fills {adjs}; {nth}
    "first_child": "As a child they were {adjs}, and the seed of who they would be was already in them.",
    "first_later": "By their {nth} year they were {adjs}.",
    "unsettled": "unsettled",            # {adjs} when no color stands out

    # a swing: two identities taking turns. "they turned {img}, {span}: {winds}." The cause, when there is one, comes
    # first as in game.py ("When ..., they turned ..."). {img} is FLICKER[color]["first"], or ["again"] when that color
    # has flickered before in the song.
    "swing": "they turned {img}, {span}: {winds}.",
    "span_all": "all their days",        # the swing is the first stanza and fills 60% of the life or more
    "span_years": "for {n} years",
    "winds_both": "{adjs} always, while their {nouns} came and went",   # the two identities share colors
    "winds_apart": "now {a}, now {b}",                                    # they share none
    "flicker": dict(
        W=dict(first="like a lamp lit, put out and lit again", again="like the lamp once more, lit and put out and lit"),
        U=dict(first="like a question asked, set aside and asked again", again="like the old question, asked once more"),
        B=dict(first="like a coin turned over and over in the hand", again="like the coin again, turned and turned in the hand"),
        R=dict(first="like a flame in a gusting wind", again="like the flame again, bent low and rising"),
        G=dict(first="like the tide that leaves the shore and always comes back", again="like the tide once more, out and home")),

    # the end of a swing, when the identity that won had been one of its two. Fills {age} {adjs}
    "harbour": "At {age} the winds fell still, and they came to harbour, {adjs} at last.",

    # a turn with a cause. {cause} is one of the cause phrases below; "big" when the colors moved .25 or more.
    "turn": dict(
        death=dict(big="And {cause}, and {gods} remade them.", small="And {cause}, and they were not the same after."),
        title=dict(big="Then, {cause}, a great change came over them.", small="Then, {cause}, they were changed a little."),
        event=dict(big="Then, {cause}, the world shook them into a new shape.", small="Then, {cause}, something shifted in them.")),
    "cause_death": dict(
        parent="when a parent went down to the house of the dead",
        sibling="when one who had shared their childhood went down into the dark",
        friend="when a friend was taken from them",
        grandparent="when the old ones of the house were laid in the earth",
        partner="when the one they loved went down into the dark before them",
        child="when a child of theirs was taken from them",
        other="when someone dear went down into the dark"),
    "cause_moment": "in the year of {moment}",      # {moment} is the moment's name in curly quotes
    "cause_title": "upon {becoming}",               # "upon becoming a baker", "upon being out of work"

    # a turn with no cause: "big" .25 or more, "mid" .12 or more, else "small". Fills {Decade} ("In their 40s")
    "drift": dict(
        big="And with the years a great change came over them, as changes come in the old tales.",
        mid="{Decade} the old shape loosened, and a new one grew.",
        small="Slowly, as stone is worn by water, they were changed."),

    # the color that rose most and the one that fell most between two stanzas, as whole clauses joined by "; ".
    # "first" the first time the song says it of that color, "again" after.
    "rise": dict(
        W=dict(first="a sense of duty rose in them as a lamp is lit in a window at dusk",
               again="duty rose in them again, as the lamp is lit once more"),
        U=dict(first="curiosity rose in them as a river cuts its way down to the sea",
               again="curiosity woke again, as a river finds its old bed"),
        B=dict(first="ambition rose in them as a hawk climbs on the warm wind",
               again="ambition climbed again, as the hawk returns to the wind"),
        R=dict(first="passion rose in them as fire runs through summer grass",
               again="the fire in them caught again, as it always would"),
        G=dict(first="they put down roots as an oak sends its roots into the dark earth",
               again="they put down roots again, deeper than before")),
    "fall": dict(
        W=dict(first="the old duties slipped from their shoulders like a cloak", again="duty slipped from them once more"),
        U=dict(first="their questions fell quiet, like birds at evening", again="their questions fell quiet again"),
        B=dict(first="their hunger for more was laid down like a sword", again="they set their hunger down once more"),
        R=dict(first="the fire in them sank to embers", again="the fire sank low again"),
        G=dict(first="their roots let go of the old ground", again="their roots let go once more")),

    # after a stanza whose identity they had held before (not after a harbour)
    "home": "So they came home to an old self, as the wanderer comes home.",
    # the longest-held identity, held 10 years or more. Fills {n} {ident} ("a Striver", "one of the Rooted")
    "longest": "For {n} years they were {ident}, and that was the longest of their shapes.",

    # the rarest things the life met, where they fell. Fills {age} and the thing's own fill
    "rare_long": "Against the odds, as the bards love best, at {age} they became {title}.",
    "rare_became": "This too the song keeps, for few are given it: at {age} they became {title}.",
    "rare_took": "This too the song keeps, for few are given it: at {age} they took to {doing}.",
    "rare_mark": "And the song does not hide it: at {age} they {deed}.",          # {deed} is MARK_SAY[mark]
    "rare_moment": dict(                              # by the life's lead color. Fills {moment} {age} {nth}
        W="And this the song keeps for the ones who come after: {moment}, in their {nth} year.",
        U="And a thing few ever see, they saw, at {age}: {moment}.",
        B="And at {age} came a day that few are dealt, and they played it: {moment}.",
        R="And at {age} came a day few ever live, and they lived it whole: {moment}.",
        G="And at {age}, a day the whole place remembered: {moment}."),

    # the stanza of deeds: how they acted at the player's moments. "own" when the ways they reached for most were
    # their lead color, "other" when not. Fills {noun} (the game's NOUN of that color)
    "deeds_reach": dict(own="When the moment came, they reached most often for their {noun}.",
                        other="When the moment came, they reached most often for their {noun}, though it was not the self they wore longest."),
    "deeds_won": dict(often="And {gods} favoured them more often than not.",            # 65% of those acts or more worked
                      half="Half the time they won, and half the time they rose again.",   # 40% or more
                      seldom="Often they failed, and every time they got up and went on."),
    # the player's pushes: "And {n} times {hand} was on them, and it pushed them toward {noun}" and one ending, by the
    # share of the life that stayed their own (integrity): willing .9 or more, bore .75 or more, else against
    "deeds_pushed": "And {n} times {hand} was on them, and it pushed them toward {noun}",
    "deeds_pushed_end": dict(willing=", and they went willingly.", bore=", and they bore it.",
                             against=", against their own heart."),
    "deeds_once": "Once {hand} was on them, and it pushed them toward {noun}",         # when {n} is 1
    "deeds_free": "No god bent their will: every road they walked, they chose.",

    # the shape of their contentment over the adult decades. Fills {hi} {lo} ("in their 30s", "in their youth")
    "shape": dict(
        rise="Their life climbed like a road into the hills: the hardest years were the first, and the best came late.",
        fall="Their life was a river that widened and slowed: the bright years came early, and later the waters ran quieter.",
        valley="They went down into the valley {lo} and climbed out of it again, into the high ground {hi}.",
        fallen="They stood on the heights {hi}, went down into the valley {lo}, and climbed out of it again.",
        summit="Their life rose to a summit {hi} and came gently down from it.",
        level="Their years ran even, like a long plain under a steady sky."),
    "decade_youth": "in their youth",                 # under 20
    "decade": "in their {d}s",                       # {d} 20, 30 ...
    "peace": "Their deepest peace was {decade}, still as water at evening.",
    "buried": "They buried {n} of their own, and carried each of them.",      # three or more close deaths
    "reached": dict(                                  # two long shots or more. Fills {n} {made}
        never="And {n} times they reached for what lay beyond them, and never once took hold of it, and reached anyway.",
        once="And {n} times they reached for what lay beyond them, and once took hold of it.",
        more="And {n} times they reached for what lay beyond them, and {made} times took hold of it."),
    # the end: "early" for any cause but old age (fills {age} {how}), "old" for old age
    "death_early": "At {age} they went down into the dark, {how}, and the song does not grieve it less.",
    "death_old": "Full of years at {age}, they went down into the dark, and the dark was kind.",

    # the last stanza. Fills {hall} {N} {glad} {cheer} {toast}
    "close": "So it is sung now, {hall}: the song of {N}, {glad}. {cheer} {toast}",
    "cheer": "Raise the cup.",
    "hall": "where the cups are filled and the night is long",
    "gods": "the gods",
    "hand": "the gods' hand",
    # by the peace reading's bands (how well they lived, how much it was their own)
    "glad": {("high", "high"): "who lived, and lost, and was glad",
             ("high", "mid"): "who lived well, and mostly as themselves",
             ("high", "low"): "who was glad, though the gods chose much of it",
             ("mid", "high"): "who went their own way at an ordinary price",
             ("mid", "mid"): "who took the good with the bad, as mortals must",
             ("mid", "low"): "who bore what was laid on them, and went on",
             ("low", "high"): "who paid dearly to stay themselves, and paid it",
             ("low", "mid"): "who walked a hard road, and did not stop",
             ("low", "low"): "who suffered much, and still was there to tell of it"},
    # the toast, by the lead color: "glad" when how well they lived is high or mid, "hard" when it is low
    "toast": dict(
        W=dict(glad="To a life that kept faith with others.", hard="To one who kept faith, even when it cost them."),
        U=dict(glad="To a mind that never stopped asking.", hard="To a mind that kept asking, even in the dark."),
        B=dict(glad="To one who made their own way.", hard="To one who made their own way, whatever it cost."),
        R=dict(glad="To a heart that burned.", hard="To a heart that burned, and burned anyway."),
        G=dict(glad="To one who belonged.", hard="To one who held on to their place through everything.")),
}

# the words that differ by world; every other key is the same in all three
SONG_WORLD = {
    "tribal": {
        "hall": "around the fire, when the elders sing",
        "cheer": "Feed the fire.",
        "gods": "the spirits",
        "hand": "the spirits' hand",
        "deeds_free": "No spirit bent their will: every trail they walked, they chose.",
        "glad": {("high", "low"): "who was glad, though the spirits chose much of it",
                 ("mid", "mid"): "who took the good with the bad, as the people must"},
        "flicker": dict(
            W=dict(first="like a fire banked at night and woken at dawn", again="like the fire again, banked and woken"),
            B=dict(first="like a stone turned over and over in the hand", again="like the stone again, turned and turned in the hand")),
        "rise": dict(W=dict(first="a sense of duty rose in them as the fire is fed when the night comes down",
                            again="duty rose in them again, as the fire is fed once more")),
        "fall": dict(B=dict(first="their hunger for more was laid down like a spear", again="they set their hunger down once more")),
        "cause_death": dict(parent="when a parent walked out to the place of the dead",
                            grandparent="when the old ones of the band were given back to the earth"),
    },
    "magic": {
        "hall": "in the high halls, when the bards take up the lyre",
        "cheer": "Raise the cup.",
    },
}

# each history mark as the song says it: "at 30 they kept their word"
MARK_SAY = {
    "hid a wrong": "hid a wrong they had done",
    "owned up": "owned up to a wrong",
    "kept your word": "kept their word when it cost them",
    "broke your word": "broke their word",
    "learned a skill": "learned a craft",
    "took a wild risk": "took a wild risk",
    "left home": "left home",
    "stayed home": "stayed home when they might have gone",
    "moved away": "moved far away",
    "turned down a chance": "turned down a great chance",
    "helped someone in need": "helped someone in need",
    "refused someone in need": "turned away someone in need",
    "made an enemy": "made an enemy",
    "made a friend": "made a friend for life",
    "defied an authority": "defied the powers over them",
    "gave in to pressure": "gave in to those who pressed them",
    "came home": "came home",
    "came out": "told the world who they loved",
    "kept it hidden": "kept who they were hidden",
    "used drugs": "turned to drugs",
    "broke the law": "broke the law",
    "hurt someone badly": "hurt someone badly",
    "took a life": "took a life",
    "named their gender": "named who they were",
}

# ============================================================================================= the last conversation
# Told after the song. The game picks: "intro"; "gave" from the color with the highest trust (above .2), "cost" from
# the one with the lowest (below -.2), either left out when no color passes; "glad" from the trust over all the pushes
# (glad above .2, sorry below -.2, else torn). Variants: gave "own" when that color is the character's lead, else
# "other"; cost "enemy" when it is opposed to the lead (two steps round the wheel), else "other"; glad [0] when the
# voice did less than a third of their color change, [1] when a third or more. A life with no push hears "none"; one
# with fewer than five pushes hears "few". {voice} is VOICE["noun"] for the world.
LAST_TALK = {
    "intro": "At the very end, {N} spoke to the {voice} that had been with them all those years.",
    "gave": dict(
        W=dict(own="“You held me to my word when I was tired of keeping it.”",
               other="“You taught me to keep faith with people. I didn't know I could.”"),
        U=dict(own="“You made me stop and think, and the thinking saved me more than once.”",
               other="“You taught me to look before I leapt. I'd never have learned it alone.”"),
        B=dict(own="“You showed me where the chances were, and I took them.”",
               other="“You taught me to stand up for myself. Nobody else ever did.”"),
        R=dict(own="“You let me feel things all the way through.”",
               other="“You taught me to say what I felt. It frightened me, and it set me free.”"),
        G=dict(own="“You kept me close to home when I might have wandered off.”",
               other="“You taught me to let things be. I found a kind of peace there.”")),
    "cost": dict(
        W=dict(enemy="“But you bound me to rules that were never mine.”",
               other="“But you kept me dutiful when I needed to be free.”"),
        U=dict(enemy="“But you made me weigh everything, and some things should never be weighed.”",
               other="“But you made me doubt when I should have leapt.”"),
        B=dict(enemy="“But you made me put myself first, and I lost people for it.”",
               other="“But you made me grasp, and grasping never filled me.”"),
        R=dict(enemy="“But you threw me into fights that were never mine.”",
               other="“But you rushed me, and some of it I can't undo.”"),
        G=dict(enemy="“But you held me still when I wanted to change things.”",
               other="“But you told me to wait, and some things never came.”")),
    "glad": dict(
        glad=["“I'm glad you were there.”", "“I wouldn't have been me without you.”"],
        torn=["“I don't know if I'm grateful or angry. Both, I think.”", "“So much of me was you. I'll never untangle it.”"],
        sorry=["“I wish I had lived it alone.”", "“So much of who I became was you. I wish it had been me.”"]),
    "none": "{N} never knew there was a voice inside; every choice felt like their own.",
    "few": "{N} heard the voice only once or twice, and never learned what it was.",
}

# ======================================================================================================== the voice
VOICE = {
    # what the character takes the voice for, by world (P5 may widen this)
    "noun": dict(earth="voice", tribal="spirit", magic="voice"),

    # its name in this life, by its strongest side on the five questions (voice-mechanics.md section 5): "trusted"
    # while the character's trust in that side's colors is 0 or more, "doubted" below 0. "none" until about five
    # steered picks; "quiet" when the player lets them be.
    "name": dict(
        people=dict(trusted="the kind {voice}", doubted="the {voice} that always puts others first"),
        themselves=dict(trusted="the shrewd {voice}", doubted="the {voice} that says “you first”"),
        safety=dict(trusted="the careful {voice}", doubted="the timid {voice}"),
        freedom=dict(trusted="the free {voice}", doubted="the restless {voice}"),
        head=dict(trusted="the clear {voice}", doubted="the cold {voice}"),
        heart=dict(trusted="the warm {voice}", doubted="the hot-headed {voice}"),
        make=dict(trusted="the striving {voice}", doubted="the {voice} that is never satisfied"),
        already=dict(trusted="the {voice} that says “be yourself”", doubted="the {voice} that will not let them grow"),
        will=dict(trusted="the bold {voice}", doubted="the defiant {voice}"),
        meant=dict(trusted="the patient {voice}", doubted="the resigned {voice}")),
    "none": "a {voice}",
    "quiet": "a quiet {voice}",

    # the character's answer to a pick against them: by the pick's main color (its ways), its distance from the
    # character's lead color ("same": one of their identity colors; "ally": next to the lead on the wheel; "enemy":
    # two steps away), and their trust in the act's colors ("trust" .25 or more, "doubt" -.25 or less, else "unsure").
    # Two lines each: [0] when the pick is light (reluctance under .5), [1] when heavy. First person, at most 25 words.
    "answer": dict(
        W=dict(
            same=dict(trust=["Yes. You're right, I owe them that.", "I'd have got there myself. Thank you for getting me there sooner."],
                      unsure=["Fine. It's the right thing, even if it's not what I wanted today.", "I know what's expected. I just wanted one day off from it."],
                      doubt=["I know my duty. I don't need you reciting it.", "The last time you made me do the decent thing, it cost me."]),
            ally=dict(trust=["Not quite my way, but I can see the sense in keeping faith.", "Alright. Done properly. You've not steered me wrong yet."],
                      unsure=["By the book, then. I'll try.", "Rules again. I can live with it, I suppose."],
                      doubt=["Since when do I care what's proper? Fine. Once.", "You and your rules. Last time they tied my hands."]),
            enemy=dict(trust=["This isn't me. But you've been right before, so I'll do the decent thing.", "Everything in me says no. I'll trust you anyway."],
                       unsure=["This goes against who I am. Still, I'll play by their rules.", "Keep my word to people I barely know? If you say so."],
                       doubt=["This goes against everything I am, and you know it.", "Them before me, again. Last time you made me do that, I paid."])),
        U=dict(
            same=dict(trust=["Good. Think it through first.", "Yes. Better to know before I leap."],
                      unsure=["More thinking. Alright, but not forever.", "I'll look into it. You're probably right."],
                      doubt=["I've thought about it enough already.", "Last time you made me think it over, the chance was gone."]),
            ally=dict(trust=["Not how I'd do it, but a plan won't hurt.", "Alright, learn first. You've earned that much."],
                      unsure=["A plan, then. I'd rather just get on with it.", "Study first. Fine. I'll give it a go."],
                      doubt=["More questions. Last time all that thinking left me standing still.", "I don't need to understand it. I need to do it."]),
            enemy=dict(trust=["This isn't how I live, all this weighing. But you've been right before.", "Everything in me wants to leave it be. I'll trust you and look closer."],
                       unsure=["This goes against who I am. Some things are better left unexamined.", "Pick it all apart, when I'd rather let it be. Alright."],
                       doubt=["Picking everything apart again. This goes against everything I am.", "Last time I let you make me weigh it all, I lost what mattered."])),
        B=dict(
            same=dict(trust=["Yes. Take it while it's there.", "You're right. Nobody else will look after me."],
                      unsure=["Alright, I'll take what's mine.", "Fine, me first. It's how things work."],
                      doubt=["I know how to look after myself.", "Last time you had me grab for more, it slipped away."]),
            ally=dict(trust=["Not my usual way, but you've a good eye for a chance.", "Alright, I'll play it to my advantage. You've earned that."],
                      unsure=["Looking out for myself, then. It feels a bit cold.", "If I don't take it, someone else will. I suppose."],
                      doubt=["Grabbing again. Last time it made me look small.", "Since when do I think only of myself? Once, then."]),
            enemy=dict(trust=["This isn't me, putting myself first. But you've been right, so I'll take it.", "Everything in me says share it. I'll trust you and keep it."],
                       unsure=["This goes against who I am. Me, at their cost?", "Me before them. Alright, but I won't feel good about it."],
                       doubt=["Me first, at their cost? This goes against everything I am.", "Last time you made me put myself first, I lost people for it."])),
        R=dict(
            same=dict(trust=["Yes! Now, while it's burning.", "You're right. I'd regret not doing it."],
                      unsure=["Alright, I'll go with my gut.", "Fine. I'll say it the way I feel it."],
                      doubt=["I don't need you to stoke me. I burn well enough.", "Last time you let me loose, I wrecked something."]),
            ally=dict(trust=["Not how I'd usually go, but you've been right about my heart.", "Alright, I'll follow the feeling. You know me."],
                      unsure=["Act now and think later. I'll try it.", "On impulse, then. It's not really me."],
                      doubt=["Rushing in again. Last time it ended badly.", "I'm not that wild. Fine. Once."]),
            enemy=dict(trust=["This isn't me, leaping without looking. But you've been right before.", "Everything in me says be careful. I'll trust you and jump."],
                       unsure=["This goes against who I am. Feeling first, and reasons after?", "Throw caution away. Alright, if you say so."],
                       doubt=["This goes against everything I am. I don't act on a whim.", "Last time you made me rush, I paid for it for years."])),
        G=dict(
            same=dict(trust=["Yes. Let it come in its own time.", "You're right. Stay close to what I know."],
                      unsure=["Alright, I'll let it be.", "Fine. The old way, then."],
                      doubt=["I don't need to be told to be patient.", "Last time you told me to wait, it passed me by."]),
            ally=dict(trust=["Not quite my way, but you've been right about letting things grow.", "Alright, I'll stay with what I have. You know best."],
                      unsure=["Wait it out, then. I'll try.", "Let it take its course. I suppose."],
                      doubt=["Sitting still again. Last time it cost me.", "Since when do I just accept things? Fine. Once."]),
            enemy=dict(trust=["This isn't me, letting it be. But you've been right before.", "Everything in me wants to change it. I'll trust you and leave it."],
                       unsure=["This goes against who I am. Accept it as it is?", "Back to the old ways. Alright, if I must."],
                       doubt=["This goes against everything I am. I won't just sit and accept it.", "Last time you made me leave things be, I lost my chance."]))),

    # in place of the answer, when the voice last pushed the same way (its main color): how that turned out. {lost} is
    # that moment's name in curly quotes; "failed_plain" when the game has no name for it
    "memory": dict(worked=["Last time I listened, it worked.", "You were right last time. Alright."],
                   failed=["You again. Last time you cost me {lost}.", "Last time I listened to you, I lost {lost}."],
                   failed_plain=["You again. Last time it went badly.", "I listened last time, and look how that went."]),

    # after a pick they resisted: was the voice right? [0] light reluctance (under .5), [1] heavy. Third person
    "outcome": dict(right=["So the voice knew something after all.", "The voice was right, and {N} knows it."],
                    wrong=["Not the voice's best idea.", "{N} went against their own grain for this, and it failed."]),

    # trust in a color crossing .5 ("up") or -.5 ("down"); [0] the first time in this life, [1] after
    "trust_turn": dict(
        W=dict(up=["{N} has come to trust the voice when it speaks of duty.", "When the voice says do right by others, {N} listens now."],
               down=["{N} has stopped listening when the voice speaks of duty, though they still go along.", "Duty, says the voice. {N} has heard that one too often."]),
        U=dict(up=["{N} has come to trust the voice that says think first.", "When the voice asks {N} to look closer, they give it the time now."],
               down=["{N} no longer believes the voice that says think it through.", "Another plan, says the voice. {N} has stopped believing in its plans."]),
        B=dict(up=["{N} has come to trust the voice that says take the chance.", "When the voice points at an opening, {N} goes for it now."],
               down=["{N} no longer trusts the voice that says look after yourself.", "Grab it, says the voice. {N} has learned what that costs."]),
        R=dict(up=["{N} has come to trust the voice that says follow your heart.", "When the voice says now, {N} goes without a second thought."],
               down=["{N} no longer trusts the voice that says act on it.", "Go on, says the voice. {N} has been burned too often to listen."]),
        G=dict(up=["{N} has come to trust the voice that says let it be.", "When the voice says wait, {N} waits, and is glad of it."],
               down=["{N} no longer trusts the voice that says wait.", "Leave it, says the voice. {N} has waited too long before."])),

    # an identity change the voice's pushes did most of; by the trust in the colors it pushed. Fills {ident}
    "became": dict(trusted="{N} became {ident}, and knows it was not all their own doing.",
                   unsure="{N} became {ident}, half by choice and half at the voice's insistence.",
                   doubted="{N} became {ident}, pushed there more than walked."),

    # the yearly chapter, at most one voice line a year. Fills {name} (the voice's name in this life)
    "chapter": dict(
        first=["Somewhere this year a voice spoke up in {N}, and {N} listened.", "This year {N} began to hear a voice that was not quite their own."],
        won=["This year {name} won most of the arguments.", "More often than not this year, {name} had its way."],
        trust_up=["This was the year {N} began to trust {name}.", "{N} leaned on {name} more this year, and it held."],
        trust_down=["This was the year {N} stopped believing {name}.", "{N} went along with {name} this year, and resented every step."],
        quiet=["For years the voice was quiet, and {N} was simply {N}.", "A year without the voice. {N} chose everything alone."]),
    # [0] the first time the chapter has that kind of line in this life, [1] after; "first" is said once

    # the end of a life, one sentence before the last conversation. Fills {name} {adj} (the game's ADJ of the lead
    # color) and {share}; "trusted" when trust over all pushes is above .2, "doubted" below -.2, else "mixed"
    "end": dict(trusted="All {Ns} life {name} argued with their {adj} heart. They came to trust it, and {share} of who they became was its doing.",
                mixed="All {Ns} life {name} argued with their {adj} heart. Some of it they took as their own, and some they never forgave.",
                doubted="All {Ns} life {name} argued with their {adj} heart. They never trusted it, yet {share} of who they became was its doing.",
                quiet="The voice in {N} was a quiet one, and they lived their own life."),
    # {share}: the voice's part of their color change
    "share": [(0.15, "a little"), (0.30, "a quarter"), (0.40, "a third"), (0.60, "half"), (1.01, "most")],   # (below, words)

    # the Book's one line per life. Fills {start} {end} (identity names) and {lean} below, by the color pushed most
    "book": dict(steered="{N}: {start}, steered toward {lean}; became {end}.",
                 free="{N}: {start}, left to choose; became {end}."),
    "lean": dict(W="duty", U="thought", B="ambition", R="feeling", G="patience"),
}
