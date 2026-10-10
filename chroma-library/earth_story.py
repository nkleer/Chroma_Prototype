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
# THREAD        the sentence that ties a moment to its cause in this life, and its hover (F5, item 4).
# WORLD         what a world event did to them (WL1), the year's line (YEAR, WL4), the option notes (OPTION_CAUSE, WL3)
#               and the disaster readings by hazard (DISASTER_READ, WL6), item 11.
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
    # the song says every count in words: numbers[n] for 0 to 20; above 20 the game says "many"
    "numbers": ["no one", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"],

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
    # "first" the first time the song says it of that color; "again" is a list, and the k-th time after the first
    # takes again[(k - 1) % len(again)], so no clause repeats word for word until all of them are used.
    "rise": dict(
        W=dict(first="a sense of duty rose in them as a lamp is lit in a window at dusk",
               again=["duty rose in them again, as the lamp is lit once more",
                      "once more the old sense of duty came back to them, steady as a hearth",
                      "duty returned to them, as the bell calls the town each morning"]),
        U=dict(first="curiosity rose in them as a river cuts its way down to the sea",
               again=["curiosity woke again, as a river finds its old bed",
                      "once more the questions came, as spring water finds its way",
                      "their curiosity returned, quick as a stream after rain"]),
        B=dict(first="ambition rose in them as a hawk climbs on the warm wind",
               again=["ambition climbed again, as the hawk returns to the wind",
                      "once more they wanted more, as the hawk wants the height",
                      "their ambition rose again, patient as a hunter at dawn"]),
        R=dict(first="passion rose in them as fire runs through summer grass",
               again=["the fire in them caught again, as it always would",
                      "once more passion blazed up in them, like dry wood in a sudden wind",
                      "their passion flared again, bright as sparks flying up"]),
        G=dict(first="they put down roots as an oak sends its roots into the dark earth",
               again=["they put down roots again, deeper than before",
                      "once more they sank roots, as ivy finds the old wall",
                      "their roots went down again, quiet and sure as winter grass"])),
    "fall": dict(
        W=dict(first="the old duties slipped from their shoulders like a cloak",
               again=["duty slipped from them once more", "again they shrugged off what was owed",
                      "the weight of duty eased from them again"]),
        U=dict(first="their questions fell quiet, like birds at evening",
               again=["their questions fell quiet again", "once more they stopped asking why",
                      "their curiosity slept again, like a field under snow"]),
        B=dict(first="their hunger for more was laid down like a sword",
               again=["they set their hunger down once more", "again they wanted less, and let it go",
                      "their ambition was put away again, like a blade in its sheath"]),
        R=dict(first="the fire in them sank to embers",
               again=["the fire sank low again", "once more their passion cooled to ash",
                      "the flame in them dimmed again, as a hearth at midnight"]),
        G=dict(first="their roots let go of the old ground",
               again=["their roots let go once more", "again they pulled up from the ground they knew",
                      "once more they loosened their hold on the place"])),

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
    # the player's pushes: "And {n} times {hand} was on them, and it pushed them toward their {noun}" and one ending, by the
    # share of the life that stayed their own (integrity): willing .9 or more, bore .75 or more, else against
    "deeds_pushed": "And {n} times {hand} was on them, and it pushed them toward their {noun}",
    "deeds_pushed_end": dict(willing=", and they went willingly.", bore=", and they bore it.",
                             against=", against their own heart."),
    "deeds_once": "Once {hand} was on them, and it pushed them toward their {noun}",         # when {n} is 1
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
                            again=["duty rose in them again, as the fire is fed once more",
                                   "once more the old sense of duty came back to them, steady as the band's fire",
                                   "duty returned to them, as the drum calls the band at dawn"])),
        "fall": dict(B=dict(first="their hunger for more was laid down like a spear",
                            again=["they set their hunger down once more", "again they wanted less, and let it go",
                                   "their ambition was put away again, like a spear laid by the fire"])),
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
# (glad above .2, sorry below -.2, else torn): the trust per color weighted by how many of the player's pushes went
# toward each color (a push counts for the colors of the act pushed), or the plain mean of the five when no push has a
# color. Variants: gave "own" when that color is the character's lead, else
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
    # item 6 "every line has a cause" (v22.4, the Game's switch lines_tied): the same, as a short phrase after the new
    # name on the year header. Lower case, no end stop
    "became_head": dict(trusted="not all their own doing", unsure="half by choice, half at the voice's insistence",
                        doubted="pushed there more than walked"),

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

    # S2 "Making it their own" (chroma-ideas/social-mechanics.md S2; Emren 10-10 09:04 UTC "v22.3"): the Voice row's
    # hover, for each way the voice pushes toward, by how far it has become theirs (ix): "asked" under .25 (only because
    # asked), "ought" from .25 (out of ought and guilt), "sees" from .5 (they see its value), "theirs" from .8 (part of
    # who they are). Said in the pushed way's own terms (right, sense, worth, feel, who we are). Two lines: the first
    # while their trust in the voice for that way is 0 or more, the second while it is below 0. Fills {N} {Ns} {voice}.
    "own": dict(
        W=dict(asked=["{N} keeps to it because the {voice} asks, trusting it is meant well.",
                      "{N} keeps to it only because the {voice} asks, and would drop it tomorrow."],
               ought=["{N} feels it is owed, and would feel bad letting it slip.",
                      "{N} keeps to it out of duty and a nagging guilt, not belief."],
               sees=["{N} has come to see that it is the right thing to do.",
                     "{N} sees now that it is right, whoever first asked."],
               theirs=["It is simply right to {N} now, and no one needs to ask.",
                       "It is right to {N} now, the {voice}'s asking long forgotten."]),
        U=dict(asked=["{N} goes along with it because the {voice} asks, waiting to see if it makes sense.",
                      "{N} does it only because the {voice} asks, and has not seen the sense of it."],
               ought=["{N} feels a sensible person should, and is a little ashamed not to.",
                      "{N} does it because it seems expected of a thinking person, not from understanding."],
               sees=["{N} has worked it through, and it makes sense now.",
                     "{N} has found the sense in it alone, whatever the {voice} said."],
               theirs=["It makes so much sense to {N} that it no longer needs thinking about.",
                       "{N} would argue for it now, as if the idea had been theirs all along."]),
        B=dict(asked=["{N} does it because the {voice} asks, hoping it pays off.",
                      "{N} does it only because the {voice} asks, and sees nothing in it for them."],
               ought=["{N} feels they ought to if they want to get on, and resents the push a little.",
                      "{N} does it because getting on seems to demand it, not because they want to."],
               sees=["{N} sees what it is worth to them now.",
                     "{N} has worked out what it is worth to them, never mind the {voice}."],
               theirs=["It is worth it to {N}, plain and simple, and part of how they get on.",
                       "{N} would not give it up now: it is theirs, and it pays."]),
        R=dict(asked=["{N} goes along with it because the {voice} asks, though it does not feel like them yet.",
                      "{N} does it only because the {voice} asks, and it feels like wearing someone else's coat."],
               ought=["{N} feels they should want it, and is cross with themselves when they do not.",
                      "{N} forces it out of a guilty sense that they ought to, and it chafes."],
               sees=["{N} has started to feel why it matters, in the moment.",
                     "{N} feels the point of it now, on their own terms."],
               theirs=["It feels like {N} now, as natural as breathing.",
                       "{N} would swear it was always them, whatever the {voice} once pushed."]),
        G=dict(asked=["{N} keeps to it because the {voice} asks, as one takes advice from an elder.",
                      "{N} keeps to it only because the {voice} asks, and it is not how their people do things."],
               ought=["{N} feels it is expected of them, and would be ashamed to let it go.",
                      "{N} keeps to it from a sense of what is expected, more habit than heart."],
               sees=["{N} sees how it fits the people and the place they come from.",
                     "{N} has found where it fits in their own roots, without the {voice}."],
               theirs=["It is part of who {N} and their people are now.",
                       "It is woven into {Ns} life now, like something handed down."])),
}

# ============================================================================================ the thread (F5, item 4)
# When a moment comes because of something earlier in this life, the moment's text carries one sentence tying back to
# it, and hovering it shows the cause. Only this life's own history is used. THREAD[cause] is the sentence, by the
# kind of cause; THREAD_HOVER[cause] is the hover. Fills {N} {Ns} {age} (the age it happened) and the cause's own:
# {did} (THREAD_DID[mark]), {title}, {plan}, {dream}, {road}, {who} (the person, as the game names them: "her sister").
THREAD = {
    "mark": {
        "hid a wrong": "Somewhere behind this is the wrong {N} once kept hidden.",
        "owned up": "This goes back to the day {N} owned up.",
        "kept your word": "This goes back to a promise {N} kept.",
        "broke your word": "This goes back to a promise {N} broke.",
        "learned a skill": "This comes from the skill {N} took the trouble to learn.",
        "took a wild risk": "This comes from a wild risk {N} once took.",
        "left home": "This goes back to the day {N} left home.",
        "stayed home": "This goes back to the time {N} chose to stay.",
        "moved away": "This comes from the move that took {N} far from where they started.",
        "turned down a chance": "This goes back to the chance {N} once turned down.",
        "helped someone in need": "This goes back to the time {N} helped someone who needed it.",
        "refused someone in need": "This goes back to the time {N} turned someone away.",
        "made an enemy": "This comes from an enemy {N} made along the way.",
        "made a friend": "This comes through a friend {N} made along the way.",
        "defied an authority": "This goes back to the day {N} stood up to the people in charge.",
        "gave in to pressure": "This goes back to the time {N} gave in.",
        "came home": "This goes back to the day {N} came home.",
        "came out": "This goes back to the day {N} told people who they love.",
        "kept it hidden": "This comes from what {N} has kept hidden.",
        "used drugs": "This goes back to the time {N} turned to drugs.",
        "broke the law": "This goes back to the time {N} broke the law.",
        "hurt someone badly": "This goes back to the person {N} hurt.",
        "took a life": "This goes back to the life {N} took.",
        "named their gender": "This goes back to the day {N} named who they are."},
    "title": dict(held="This comes with being {title}.",
                  lost="This goes back to the day {N} stopped being {title}."),
    "commitment": dict(career="This comes with the work {N} chose.",
                       community="This comes through the people {N} threw in their lot with.",
                       faith="This comes with the faith {N} keeps.",
                       partner="This comes with the life {N} shares with {who}.",
                       children="This comes with being a parent."),
    "plan": "This belongs to the plan {N} set out on.",
    "dream": "This touches the dream {N} has carried for years.",
    "road": "This is the next step on the road {N} took at {age}.",
    "person": "This comes through {who}.",
}
THREAD_HOVER = {
    "mark": "Because {N} {did} at {age}.",
    "title": dict(held="Because {N} is {title}.", lost="Because {N} stopped being {title} at {age}."),
    "commitment": dict(career="Because of {Ns} work.", community="Because of {Ns} community.",
                       faith="Because of {Ns} faith.", partner="Because of {Ns} life with {who}.",
                       children="Because of {Ns} children."),
    "plan": "Because of {Ns} plan: {plan}.",
    "dream": "Because of {Ns} dream: {dream}.",
    "road": "Because {N} took the road of {road} at {age}.",
    "person": "Because of {who}.",
}
# each mark as the hover says it, after "{N}" and before "at {age}"
THREAD_DID = {
    "hid a wrong": "hid a wrong", "owned up": "owned up to a wrong", "kept your word": "kept their word",
    "broke your word": "broke their word", "learned a skill": "learned a skill", "took a wild risk": "took a wild risk",
    "left home": "left home", "stayed home": "stayed home", "moved away": "moved away",
    "turned down a chance": "turned down a chance", "helped someone in need": "helped someone in need",
    "refused someone in need": "turned away someone in need", "made an enemy": "made an enemy",
    "made a friend": "made a friend", "defied an authority": "defied an authority",
    "gave in to pressure": "gave in to pressure", "came home": "came home", "came out": "came out",
    "kept it hidden": "kept who they are hidden", "used drugs": "used drugs", "broke the law": "broke the law",
    "hurt someone badly": "hurt someone badly", "took a life": "took a life", "named their gender": "named their gender",
}

# ================================================================================= the world in their life (item 11)
# WL1: one small line when a world event changed something of theirs, from the engine's report (STATE "wfx": kind,
# channel, size, dir, cause, age). WORLD[kind][channel][dir][band]; when a kind has no line for that channel, the game
# uses WORLD_CHANNEL[channel][dir][band]. The cause (the world record's own name) goes on the hover, not in the line.
# band "big" when |size| is .03 or more for money and freedom, .5 or more for a risk (its multiple minus 1) or a close
# person, and for an option closed or opened outright; else "small". Below .01 (money, freedom) or .2 (a risk) the
# game tells nothing (Library proposal; the Game sets the floor). Fills {N} {Ns}, and {who} for a close person.
WORLD = {
    "recession": {
        "job loss risk": dict(
            up=dict(small="Since the downturn, {N} hears more talk of cuts at work.",
                    big="With the crisis, jobs are going all around {N}, and their own no longer feels safe."),
            down=dict(small="The downturn is easing, and the talk of cuts at {Ns} work dies down.",
                      big="The crisis is over, and {N} stops waiting for bad news at work."))},
    "unemployment": {
        "job loss risk": dict(
            up=dict(small="Work is getting harder to find, and {N} holds on to the job they have.",
                    big="So many people {N} knows are out of work that {N} keeps their head down to keep their own job."),
            down=dict(small="There is more work about, and {N} worries less about losing theirs.",
                      big="Work is easy to find again, and the fear of losing it lifts from {N}."))},
    "prices": {
        "money": dict(
            down=dict(small="Prices keep creeping up, and with no wage to keep pace, {Ns} money buys a little less each month.",
                      big="Prices are climbing fast, and with no wage rising to meet them, {N} has to count every coin."),
            up=dict(small="Prices settle, and {Ns} money stretches a little further.",
                    big="Prices have steadied at last, and {N} can stop counting every coin."))},
    "housing": {
        "money": dict(
            down=dict(small="Rents creep up, and the rent takes a little more of what {N} has.",
                      big="Rents have shot up, and keeping a roof overhead now takes much of what {N} has."),
            up=dict(small="Rents ease a little, and {N} keeps a little more each month.",
                    big="Rents have come down, and {N} has room to breathe each month."))},
    "welfare": {
        "money": dict(
            up=dict(small="The support for people out of work goes up a little, and {N} has a little more to get by on.",
                    big="The support for people out of work is raised, and {N} can cover the basics again."),
            down=dict(small="The support for people out of work is trimmed, and {N} has a little less to get by on.",
                      big="The support for people out of work is cut hard, and {N} has to choose which bills to pay."))},
    "rights": {
        "freedom": dict(
            up=dict(small="The rules loosen a little, and {N} feels a little freer to live as they like.",
                    big="New rights come in, and {N} can live more openly than before."),
            down=dict(small="The rules tighten a little, and {N} feels watched.",
                      big="Rights are taken back, and {N} has to live more carefully now."))},
    "crime wave": {
        "crime risk": dict(
            up=dict(small="There has been a run of break-ins nearby, and {N} checks the locks twice.",
                    big="Crime is up all over town, and {N} no longer walks home alone after dark."),
            down=dict(small="Things are quieter on the streets, and {N} worries less on the way home.",
                      big="The streets are safe again, and {N} walks home at night without thinking about it.")),
        "safety": dict(
            down=dict(small="The crime nearby leaves {N} a little on edge.",
                      big="After the crimes nearby, {N} does not feel safe at home."),
            up=dict(small="With crime falling, {N} rests a little easier.",
                    big="With the streets safe again, {N} sleeps soundly."))},
    "disaster": {
        "disaster risk": dict(
            up=dict(small="After the last disaster, {N} keeps an eye on the weather.",
                    big="Disasters are coming more often now, and {N} keeps a bag packed by the door."),
            down=dict(small="The new defences are holding, and {N} worries a little less about the next disaster.",
                      big="Disasters have grown rare again, and {N} stops listening for the warnings.")),
        "safety": dict(
            down=dict(small="The disaster has left {N} jumpy.", big="The disaster has left {N} afraid in their own home."),
            up=dict(small="The town is mending, and {N} feels a little steadier.",
                    big="The town has come back from the disaster, and so has {N}.")),
        "close person": dict(
            down=dict(small="The disaster has hit {who}, and {N} does what they can.",
                      big="The disaster has hit {who} hard, and {N} can think of little else."))},
    "war": {
        "safety": dict(
            down=dict(small="The war abroad feels closer every week, and {N} follows the news anxiously.",
                      big="The war has come close to home, and {N} lives with the fear of it."),
            up=dict(small="The war is winding down, and {N} breathes out.",
                    big="Peace at last, and {N} lets themselves plan again.")),
        "close person": dict(
            down=dict(small="The war has taken {who} far away, and {N} waits for news.",
                      big="The war has reached {who}, and {N} can think of little else."))},
    "law": {
        "option": dict(
            down=dict(small="A new law makes a road {N} might have taken harder.",
                      big="A new law closes a door {N} had been counting on."),
            up=dict(small="A new law makes a road easier for {N}.",
                    big="A new law means {N} can do what was closed to them before.")),
        "freedom": dict(
            up=dict(small="A new law gives {N} a little more room.", big="A new law lets {N} live more freely than before."),
            down=dict(small="A new law hems {N} in a little.", big="A new law hems {N} in, and {N} feels it every day."))},
    "hospital places": {
        "option": dict(
            down=dict(small="The hospitals are stretched, and {N} would wait longer to be seen.",
                      big="There are too few hospital beds, and {N} cannot count on care if it is needed."),
            up=dict(small="A new ward opens, and getting care is a little easier for {N}.",
                    big="Care is easy to get again, and {N} can stop worrying about being seen."))},
    "university places": {
        "option": dict(
            down=dict(small="University places are scarce, and the way into study narrows for {N}.",
                      big="With so few university places, the door to study is all but closed to {N}."),
            up=dict(small="There are more university places now, and study is within {Ns} reach.",
                    big="The universities have opened their doors wide, and study is there for {N} if they want it."))},
    "pandemic": {   # WL2 (Engine #62): a sickness going round keeps people apart; told on the ties channel
        "ties": dict(
            down=dict(small="With the sickness going round, {N} sees friends less and keeps close to home.",
                      big="The sickness has shut everyone indoors, and {N} has not sat with a friend in months."),
            up=dict(small="The sickness is ebbing, and {N} starts seeing friends again.",
                    big="The sickness is over at last, and {N} is back among the people they missed."))},
}
WORLD_CHANNEL = {
    "money": dict(down=dict(small="The times take a little out of {Ns} pocket.", big="The times hit {Ns} pocket hard."),
                  up=dict(small="The times put a little more in {Ns} pocket.", big="The times are good to {Ns} pocket.")),
    "freedom": dict(down=dict(small="The times close in a little on how {N} can live.",
                              big="The times close in on how {N} can live."),
                    up=dict(small="The times give {N} a little more room to live as they like.",
                            big="The times open up, and {N} has room to live as they like.")),
    "safety": dict(down=dict(small="The times leave {N} a little uneasy.", big="The times leave {N} afraid."),
                   up=dict(small="The times feel a little safer to {N}.",
                           big="The times feel safe again, and {N} lets their guard down.")),
    "job loss risk": dict(up=dict(small="Work feels a little less certain for {N}.", big="{Ns} work no longer feels safe."),
                          down=dict(small="Work feels a little more certain for {N}.",
                                    big="{N} stops worrying about losing their work.")),
    "disaster risk": dict(up=dict(small="The next disaster feels a little closer to {N}.",
                                  big="{N} has stopped asking whether the next disaster will come, only when."),
                          down=dict(small="{N} worries a little less about the next disaster.",
                                    big="{N} stops worrying about the next disaster.")),
    "crime risk": dict(up=dict(small="{N} is a little more careful on the streets.",
                               big="{N} no longer feels safe on the streets."),
                       down=dict(small="{N} is a little less careful on the streets.",
                                 big="{N} walks the streets without a second thought.")),
    "option": dict(down=dict(small="A road {N} might have taken gets harder.", big="A door {N} was counting on closes."),
                   up=dict(small="A road gets easier for {N}.", big="A door {N} had given up on opens.")),
    "close person": dict(down=dict(small="The times are hard on {who}, and {N} feels it too.",
                                   big="The times hit {who} hard, and {N} carries it with them."),
                         up=dict(small="The times are kind to {who}, and {N} is glad.",
                                 big="The times are good to {who}, and some of it reaches {N}.")),
    "ties": dict(down=dict(small="The times keep {N} a little further from the people they know.",
                           big="The times cut {N} off from the people they know."),
                 up=dict(small="The times bring {N} a little closer to the people they know.",
                         big="The times bring {N} back among friends.")),
}

# WL4: the year's chapter, one line on how the times touched them that year (not the headlines), from that year's
# reports. The tone: "close" when a disaster, a war or a close person's report is among them; else "mixed" when the two
# largest point opposite ways; else by the largest: money (lean or easier), freedom or an option (narrower or freer),
# a risk (uneasy or calmer). {what} is one or two YEAR_WHAT clauses (the two largest), joined by " and ". Fills {N}.
YEAR = {
    "lean": "A lean year for {N}: {what}.",
    "easier": "An easier year for {N}: {what}.",
    "uneasy": "An uneasy year for {N}: {what}.",
    "calmer": "A calmer year for {N}: {what}.",
    "freer": "A freer year for {N}: {what}.",
    "narrower": "A narrower year for {N}: {what}.",
    "close": "The times came close to {N} this year: {what}.",
    "mixed": "The times gave and took from {N} this year: {what}.",
}
# item 6 "every line has a cause" (v22.4, the Game's switch lines_tied): the times as one clause in the year's lead, by
# the same tones as YEAR. The game adds the semicolon before and the full stop after. Fills {what} (as YEAR)
YEAR_LEAD = {
    "lean": "lean times: {what}",
    "easier": "easier times: {what}",
    "uneasy": "uneasy times: {what}",
    "calmer": "calmer times: {what}",
    "freer": "freer times: {what}",
    "narrower": "narrower times: {what}",
    "close": "the times came close: {what}",
    "mixed": "the times gave and took: {what}",
}
# item 6: a memory told inside the moment that brought it back (the game's RECALL_LINES stay as the fallback). scar: it
# went badly and left a wound; good: it worked; bad: it did not. Clauses, no end stop. Fills {when} ("as a child", "at
# 17"), {what} (a bare verb phrase after "chose to") and {N}
RECALL_IN = {
    "scar": ["it opens an old wound: {when}, {N} chose to {what}, and it went badly",
             "{N} has been here before: {when}, they chose to {what}, and it still stings",
             "it comes too close to an old hurt: {when}, {N} chose to {what}, and it went wrong"],
    "good": ["it brings back a good memory: {when}, {N} chose to {what}, and it worked",
             "{N} has done this before: {when}, they chose to {what}, and it went well",
             "it feels familiar: {when}, {N} chose to {what}, and it paid off"],
    "bad": ["{N} remembers: {when}, they chose to {what}, and it did not work",
            "it has been tried before: {when}, {N} chose to {what}, and it went wrong",
            "an old attempt comes to mind: {when}, {N} chose to {what}, and it came to nothing"],
}
# item 6: the temperament line names the event that moved it most. Fills {N}, {m} (what they have become, as today's
# line) and {event} (a lower-case noun phrase with its article: "the divorce", "losing their mother"). With no event the
# game keeps today's line
TEMPER_CAUSE = ["Since {event}, {N} has become {m}.", "People who know {N} say {event} made them {m}.",
                "After {event}, {N} slowly became {m}."]
# light and shadow (stage 2, item 2; chroma-ideas/shadows-mechanics.md section 6), the Game's outcome naming and chapter
# line. Keys are the engine's five shadow states. Shown only with the engine's shadows switch on.
# SHADOW_FAIL[state]: when an act fails because of the shadow, the game prints "<State word>: <clause>." on its own line
# under the outcome. Lower case, no end stop. Fills {N} only
SHADOW_FAIL = {
    "rigid": ["the rule held, and the person it was for did not",
              "{N} kept to the letter of it, and lost the point of it",
              "there was no give in it, and something gave way instead"],
    "indecisive": ["{N} weighed it one more time, and the chance went by",
                   "every side was seen, and none was chosen in time",
                   "the answer came, but the moment had already passed"],
    "ruthless": ["{N} took what was there, and the people went with it",
                 "the deal was won, and the trust behind it was lost",
                 "it worked on paper, and cost them someone who mattered"],
    "reckless": ["{N} went all in, and this time the bill came at once",
                 "the cost was plain to see, and {N} paid it in full",
                 "it went one step too far, and something broke that will not mend quickly"],
    "stuck in their ways": ["{N} did it the old way, and the old way no longer fit",
                            "what always worked did not work this time",
                            "the change came anyway, and {N} was not ready for it"],
}
# SHADOW_YEAR[state][grow|fade]: the yearly chapter's one line when the state comes on (grow) or goes off (fade). Whole
# sentences. Fills {N} only
SHADOW_YEAR = {
    "rigid": dict(grow=["This was the year the rules became a wall.",
                        "{N} held everything tighter this year, and the people near them felt it."],
                  fade=["This was the year {N} let a rule bend, and nothing fell.",
                        "Something loosened in {N} this year; a small mistake was allowed to stay small."]),
    "indecisive": dict(grow=["This was the year {N} kept waiting for one more answer.",
                             "Doubt took up more room this year, and choices waited until they made themselves."],
                       fade=["This was the year {N} chose before they were sure, and it was all right.",
                             "{N} stopped asking for one more night this year, and decided."]),
    "ruthless": dict(grow=["This was the year people became tools to {N}.",
                           "{N} won more this year, and kept fewer friends."],
                     fade=["This was the year {N} gave something back without asking what it bought.",
                           "{N} let someone else win this year, and found they could bear it."]),
    "reckless": dict(grow=["This was the year {N} stopped counting the cost.",
                           "Every risk looked like a door this year, and {N} went through most of them."],
                     fade=["This was the year {N} stopped to count the cost first.",
                           "{N} walked away from a risk this year, and did not feel smaller for it."]),
    "stuck in their ways": dict(grow=["This was the year {N} stopped letting anything change.",
                                      "The old ways closed around {N} this year like a coat buttoned to the neck."],
                                fade=["This was the year {N} tried something new, and kept it.",
                                      "{N} let one old habit go this year, and the house did not fall."]),
}
# YEAR_WHAT[kind][channel][dir], falling back to YEAR_WHAT_CHANNEL[channel][dir]. Clauses, past tense. Fills {who}
YEAR_WHAT = {
    "recession": {"job loss risk": dict(up="the downturn put jobs at risk", down="the downturn eased")},
    "unemployment": {"job loss risk": dict(up="work grew scarce", down="work was easier to find")},
    "prices": {"money": dict(down="prices outran their money", up="prices settled")},
    "housing": {"money": dict(down="rents went up", up="rents came down")},
    "welfare": {"money": dict(up="the support for those out of work went up",
                              down="the support for those out of work was cut")},
    "rights": {"freedom": dict(up="new rights came in", down="rights were taken back")},
    "crime wave": {"crime risk": dict(up="crime rose nearby", down="the streets grew quieter"),
                   "safety": dict(down="crime nearby left them on edge", up="the streets felt safe again")},
    "disaster": {"disaster risk": dict(up="disasters came more often", down="disasters grew rarer"),
                 "safety": dict(down="a disaster shook them", up="the town mended after the disaster"),
                 "close person": dict(down="a disaster hit {who}")},
    "war": {"safety": dict(down="the war came closer", up="the war wound down"),
            "close person": dict(down="the war reached {who}")},
    "law": {"option": dict(down="a new law closed a door", up="a new law opened a door"),
            "freedom": dict(up="a new law gave them more room", down="a new law hemmed them in")},
    "hospital places": {"option": dict(down="care was harder to get", up="care was easier to get")},
    "university places": {"option": dict(down="places to study grew scarce", up="places to study opened up")},
    "pandemic": {"ties": dict(down="the sickness kept them from their friends", up="friends met again after the sickness")},
}
YEAR_WHAT_CHANNEL = {
    "money": dict(down="money was tighter", up="money went further"),
    "freedom": dict(down="life narrowed", up="life opened up"),
    "safety": dict(down="the times felt dangerous", up="the times felt safer"),
    "job loss risk": dict(up="work felt less certain", down="work felt more certain"),
    "disaster risk": dict(up="the next disaster felt closer", down="the next disaster felt further off"),
    "crime risk": dict(up="the streets felt less safe", down="the streets felt safer"),
    "option": dict(down="a door closed", up="a door opened"),
    "close person": dict(down="the times were hard on {who}", up="the times were kind to {who}"),
    "ties": dict(down="they saw less of the people they know", up="they saw more of the people they know"),
}

# WL3: the note on an option the world makes closed, harder or easier, from option_causes(n) (kind: law, norm,
# technology, odds); the cause's own name goes on the hover. Short phrases, no fills.
OPTION_CAUSE = {
    "law": dict(closed="Not allowed by law here", harder="The law makes this harder", easier="The law allows this now"),
    "norm": dict(closed="Not done around here", harder="Frowned on these days", easier="More accepted these days"),
    "technology": dict(closed="Not possible yet", harder="Hard to manage with what there is",
                       easier="Easier with the new tools"),
    "odds": dict(closed="No way in right now", harder="Harder than usual right now", easier="Easier than usual right now"),
}

# WL6: the outside event "a disaster in the next town" told as the disaster that happened. The Engine tags the event's
# story entry with hazard (flood, fire, quake, storm, heat) and where ("home": their own town; "near": a close person's
# or the next town). DISASTER_READ[hazard][where] gives the scene and each color's reading as (label, say), in place of
# earth.py's (flood, near is earth.py's own text). The readings' impact and needs stay earth.py's, so lives are unchanged.
DISASTER_READ = {
    "flood": {
        "near": dict(
            scene="The river burst its banks in the night. Ten miles away a whole town is under muddy water, and {Ns} phone is full of messages from people who live there.",
            W=("organise: collect, sort, send, help", "{N} helps at the collection point in the school hall all week."),
            U=("why there, why now, and what would have stopped it?", "{N} studies the flood maps and writes to the council about the defences."),
            B=("it could have been here; make sure your own are protected first", "{N} packs an emergency bag that afternoon and checks the family is covered."),
            R=("get over there and start bailing", "{N} gets a lift over with a load of buckets and works until dark."),
            G=("the river takes back what was its own", "{N} stands on the bridge and watches the muddy water for a long time.")),
        "home": dict(
            scene="The river came up in the night. By morning {Ns} street is under water to the doorsteps, and the whole town is wading through the mud.",
            W=("organise: sandbags, rotas, and a list of who needs checking on", "{N} knocks on every door in the street to check on the old and the alone."),
            U=("why here, why now, and what would have held it back?", "{N} studies the flood maps and goes to the council meeting with questions about the defences."),
            B=("look after your own first: the house, the papers, the insurance", "{N} moves everything of value upstairs and is first in line with the insurance claim."),
            R=("wade in and start bailing", "{N} is out in the water with a bucket before anyone has said what to do."),
            G=("the water comes and the water goes", "{N} watches the water from the upstairs window, and starts again when it goes down."))},
    "fire": {
        "near": dict(
            scene="A wildfire swept through the hills behind the next town in the night. Whole streets there are ash, and {Ns} phone is full of messages from people who live there.",
            W=("organise: gather what they need and get it there", "{N} sorts clothes and food for the families who lost their homes, all week."),
            U=("why there, and what would have stopped it spreading?", "{N} reads everything about the fire's path and writes to the council about clearing the hills."),
            B=("it could have been here; make your own place safe first", "{N} clears the dry brush round the house that weekend and checks the family is covered."),
            R=("get over there and help, whatever it takes", "{N} drives over with water and blankets and works at the shelter until dark."),
            G=("fire has always been part of the land", "{N} stands at the edge of the burned hills and watches the smoke for a long time.")),
        "home": dict(
            scene="The fire came over the ridge in the night. {Ns} street was spared by a change of wind, but the edge of town is charred and the air still smells of smoke.",
            W=("organise: shelter, food, and a list of who has nowhere to go", "{N} opens the house to a family who lost theirs and helps run the shelter."),
            U=("why here, and what would have kept it out?", "{N} goes to the meeting about the fire breaks with a list of questions."),
            B=("secure your own first: the house, the papers, the claim", "{N} packs the papers in a fireproof box and is first in line with the insurance claim."),
            R=("go and help, now", "{N} is out on the ridge with a hose and a shovel before anyone asks."),
            G=("the land burns and the land comes back", "{N} walks the burned edge of town, and weeks later is the first to notice the new shoots."))},
    "quake": {
        "near": dict(
            scene="The ground shook in the night. In the next town buildings came down, and {Ns} phone is full of messages from people who live there.",
            W=("organise: blankets, food, and a place to sleep", "{N} sorts blankets and food at the collection point all week."),
            U=("why there, and how would better building have saved it?", "{N} reads up on how houses are built to stand a quake, and writes to the council."),
            B=("it could have been here; make your own house safe first", "{N} bolts the shelves to the walls that afternoon and checks the family is covered."),
            R=("get over there and dig", "{N} goes over with a shovel and helps clear the rubble until dark."),
            G=("the ground moves, as it always has", "{N} sits on the back step that evening and feels how still the ground is now.")),
        "home": dict(
            scene="The ground shook in the night. {Ns} house stood, with cracks up the walls, but down the street a building came down, and the whole town is out in the cold.",
            W=("organise: food, shelter, and checks on every neighbour", "{N} helps set up the shelter in the sports hall and keeps the list of who is safe."),
            U=("what held, what fell, and why?", "{N} goes from house to house noting which walls held, and takes the notes to the council."),
            B=("secure your own first: the walls, the cracks, the claim", "{N} has the walls checked before anyone else's and is first in line with the claim."),
            R=("dig, now, with your hands if you must", "{N} is out at the fallen building with the neighbours, clearing it until the rescuers arrive."),
            G=("the earth moves, and people go on", "{N} sleeps in the garden for a week, and then moves back in."))},
    "storm": {
        "near": dict(
            scene="A storm tore along the coast in the night. In the next town roofs are gone and trees lie across the roads, and {Ns} phone is full of messages from people who live there.",
            W=("organise: tarps, food, and hands to help", "{N} loads a van with tarps and food for the next town and drives it over."),
            U=("why there, and what would have stood up to it?", "{N} reads up on the storm and writes to the council about the sea wall."),
            B=("it could have been here; tie down your own place first", "{N} ties down everything loose at home that afternoon and checks the family is covered."),
            R=("get over there and clear the roads", "{N} goes over with a saw and helps clear the fallen trees until dark."),
            G=("the sea and the wind were here first", "{N} walks the shore the next morning and watches the grey water for a long time.")),
        "home": dict(
            scene="The storm hit in the night. By morning the roofs on {Ns} street are open to the sky, and trees lie across the roads.",
            W=("organise: tarps, ladders, and the worst roofs first", "{N} gets the neighbours together to cover the worst roofs first."),
            U=("what gave way, and why?", "{N} goes over every broken roof on the street and works out what failed."),
            B=("secure your own first: the roof, the papers, the claim", "{N} gets the roof fixed before the builders are booked out and files the claim that day."),
            R=("up the ladder, now", "{N} is on the neighbours' roofs with a hammer before the wind has dropped."),
            G=("the wind takes what it takes", "{N} sweeps up the leaves and the broken tiles, and lets the rest be."))},
    "heat": {
        "near": dict(
            scene="A heatwave has gripped the region for weeks. In the next town the water has run out and the old are being taken to hospital, and {Ns} phone is full of messages from people who live there.",
            W=("organise: water, fans, and visits to the old", "{N} drives water over to the next town and checks on the old people there."),
            U=("why so hot, and what would keep a town cool?", "{N} reads up on the heat and writes to the council about shade and water."),
            B=("it could be here next; make sure your own are cared for first", "{N} stocks up on water that afternoon and makes sure the family is managing."),
            R=("get over there and help", "{N} spends the weekend carrying water to people in the next town."),
            G=("the land has dry years, and wet ones", "{N} sits in the shade through the worst of the afternoons and waits for the weather to turn.")),
        "home": dict(
            scene="The heat has not broken for weeks. The town's water is rationed, the streets are empty by noon, and {N} lies awake every night in the stifling dark.",
            W=("organise: water rounds and checks on the old", "{N} takes water round to the old and the alone on the street every evening."),
            U=("what keeps a house cool, and why did no one plan for this?", "{N} works out how to keep the house cool and shares it with the neighbours."),
            B=("look after your own first: water, shade, a cool room", "{N} gets the family into the coolest room and keeps the water for them."),
            R=("out and help, heat or no heat", "{N} spends the hottest days carrying water to anyone who needs it."),
            G=("the heat will pass, as it always does", "{N} keeps still through the worst of the afternoons, and waits for the rain."))},
}

# ================================================================== the world's new events (stage 3, items C3 C4 C5 T4)
# The world panel and story words for the event kinds stage 3 adds (chroma-world/model/stage3-rules.md sections 4 and
# 5), keyed by the Engine's event kind. "panel" is the timeline entry (a phrase, as the game's worldview.EVENT); "story"
# is the line told when the news reaches the character (as worldview.STORY); "self" is added when the event is the
# character's own institution or place (as worldview.SELF_TAIL). Fills: {inst} (the institution as the game names it,
# "the factory in Redmouth"), {place}, {movement} (a name from MOVEMENT_NAMES), and {N} in "self". A reform that opens a
# door uses the game's own "law" entry.
WORLD_EVENT = {
    "sold": dict(panel="{inst} is sold",
                 story="New owners take over {inst}, and nobody yet knows what they want from it.",
                 self="{N} works there, and waits like everyone else to hear what changes."),
    "merged": dict(panel="{inst} is taken over by a bigger rival",
                   story="A bigger rival swallows {inst}, and the sign over the door changes within the month.",
                   self="{N} works there, and the talk at work is of who will be kept on."),
    "nationalised": dict(panel="{inst} is taken into public hands",
                         story="Rather than let {inst} close, the state takes it over.",
                         self="{N} works there, and the job is saved, for now."),
    "leak": dict(panel="private records leak from {inst}",
                 story="Private records from {inst} turn up online, and everyone who ever used it checks whether theirs are there.",
                 self="{N} works there, and the phones do not stop ringing."),
    "cover-up": dict(panel="a cover-up at {inst} comes to light",
                     story="It comes out that {inst} hid a wrong for years, and the question everyone asks is who knew.",
                     self="{N} works there, and people look at the staff differently now."),
    "bad air": dict(panel="a season of bad air in {place}",
                    story="A haze sits over {place} for weeks, and people with weak chests stay indoors.",
                    self="{N} lives there, and the air catches in the throat on the way to work."),
    "bad water": dict(panel="the water in {place} is unsafe",
                      story="Notices go up across {place}: boil the water before you drink it.",
                      self="{N} lives there, and every kettle in the street is on."),
    "poisoned river": dict(panel="the river at {place} is poisoned",
                           story="Dead fish line the banks below the works at {place}, and the argument over who is to blame begins.",
                           self="{N} lives there, and the river smells of it."),
    "drought": dict(panel="a drought around {place}",
                    story="No rain for months around {place}: the fields crack, and food costs more.",
                    self="{N} lives there, and watches the sky every morning."),
    "glorious spring": dict(panel="a glorious spring",
                            story="Spring comes early and stays kind, and the whole of {place} seems to be out of doors.",
                            self="{N} lives there, and the evenings are long and soft."),
    "recovery": dict(panel="{place} rebuilds",
                     story="There is scaffolding all over {place}: slowly, the town is putting itself back together.",
                     self="{N} lives there, and every week something else opens again."),
    "boom year": dict(panel="a boom year",
                      story="Work is easy to find this year, and the shops are busy even on a weekday.",
                      self="{N} feels it too: there is more to go round."),
    "good year in town": dict(panel="jobs come back to {place}",
                              story="New jobs come to {place}, and the empty shops on the high street are filling again.",
                              self="{N} lives there, and the town feels lighter."),
    "good harvest": dict(panel="a good harvest",
                         story="A good harvest: food is cheap and plentiful, and the market stalls are piled high.",
                         self="{N} notices it at the till, and at the table."),
    "festival year": dict(panel="a festival year",
                          story="This year's feast is the biggest anyone remembers: the streets are hung with lights, and everyone is invited.",
                          self="{N} is in the crowd, whatever {N} believes."),
    "movement founded": dict(panel="a new movement, {movement}, is founded",
                             story="A new movement calls itself {movement}, and its meetings fill faster than anyone expected.",
                             self="{N} knows people who have been."),
    "movement grows": dict(panel="{movement} grows",
                           story="Now {movement} has a hall in every town, and its people knock on doors on Saturdays.",
                           self="{N} has had someone from it at the door."),
    "claims spread": dict(panel="word of wonders at {movement}",
                          story="People say there were wonders at a meeting of {movement}: a healing, a voice. Others say a good deal less.",
                          self="{N} hears it from someone who swears they were there."),
    "faith tension": dict(panel="tension between faiths in {place}",
                          story="After a protest, a hall in {place} is closed, and families who used to eat together no longer do.",
                          self="{N} lives there, and feels the street divide."),
    "movement fades": dict(panel="{movement} fades",
                           story="The meetings of {movement} thin out, and its hall is let to a dance class.",
                           self="{N} still knows people who were in it."),
}

# Invented, timeless names for the three new faith movement slots (stage 3, C5). Each passes the setting check; none
# is the name of a real faith or group. The game takes one per movement, from the world seed, and never reuses one.
MOVEMENT_NAMES = [
    "the Lantern Way", "the Fellowship of the Quiet Hour", "the Hearth Circle", "the Ninth Hour",
    "the Long Road Fellowship", "the House of the Open Sky", "the Seekers of Still Water", "the Last Light",
    "the Way of Two Rivers", "the Tidewatch", "the Society of the Bell", "the First Light Fellowship",
    "the Covenant of the Ash Tree", "the Circle of the Returning Bird", "the Bright Field", "the Open Hand",
    "the Keepers of the Well", "the Stillwater Gathering", "the Company of the Morning Star", "the Little Flame",
    "the Turning Year", "the Kindred of the Stone", "the Harbour Light", "the Hill of Voices",
]
