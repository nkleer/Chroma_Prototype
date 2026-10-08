# Chroma Library, modern Earth: the character's inner voice and the world's lessons (engine v7, explain.py).
# Draft, Library thread, 2026-10-05. Review copy: earth_voice.md. Checks: check_voice.py, output in checks_voice.md.
#
# FORMAT. Four dicts with the engine's shape (chroma-engine/v7-handoff.md, "For the Library"):
#   VOICE[key]   = [(color, line), ...]   before a choice: 12 voice keys (one per moment) and 10 asides
#   LESSONS[key] = [(color, line), ...]   after a choice: 33 lesson keys, how the world works (27, and 6 for titles and perks)
#   HEART_WHY[driver], HEAD_WHY[driver] = phrase   why the heart and the head want their option, in the first person
#                                                  (at the end of the file; explain.before merges them over its own)
# color is "" (any color) or one of W U B R G. explain._pick pools the variants whose color string holds the
# character's strongest color with the "" ones, and draws one of them at random when the game passes an rng.
# Every key has two "" variants and the same number for each color: four a color for the 13 keys that come up most
# (agree, torn, dream_calls, becoming, time_short; short_horizon, out_of_reach, undisciplined; the lessons practice,
# surprise_teaches, habit, closer_to, perk_helped), so repeats show less, and two a color for the rest. 55 keys, 790 lines.
#
# FILLS. The engine replaces these; a line uses only the fills its key receives (check_voice.py checks this).
#   Voice keys: the character's own thoughts. First person, no {N}, at most 25 words. Options are quoted in curly
#     quotes, as in the defaults:
#       heart_over_head, head_over_heart, torn   “{heart}” (what the heart wants) and “{head}” (what the head picks);
#                                                one "" line each also gives the reason: {heart_why}, {head_why}
#       agree                                    “{heart}” (heart and head want the same option)
#       want_but_doubt, duty, habit, becoming,
#       time_short                               “{x}” (the option they agree on)
#       dream_calls                              “{x}” and {goal} ("the dream of a working life", "the passion for
#                                                freedom", "the plan for doing right and freedom": the name of the goal,
#                                                so it is served, fed, honoured or stepped toward, never wanted or had)
#       need_first                               “{x}” and {need} (safety, belonging, autonomy, competence, meaning)
#       stuck                                    none (the character sees no option at all)
#     {heart_why} and {head_why} are this file's HEART_WHY and HEAD_WHY phrases (the engine's own are in the third
#     person, "it is what {N} believes in"). They follow "because", and are used only in torn, heart_over_head and
#     head_over_heart. They hold no fills: {goal} and {need} can be empty when the reason is drawn.
#   Asides: a quiet observation by the narrator. Third person, at most 14 words, {N} only, except lacks: {N} and {what}
#     (the say of the title or perk the best way needs, from earth_perks_titles.py), always after a colon at the end.
#   Lessons: third person, present tense, at most 18 words; never a number, never a verdict. {N} in all, plus:
#     practice {c}; surprise_teaches {c} {dir}; door {c}; commit_start {kind} {kind_ref} {c}; turning_point {c};
#     backfire {kind} (law, approval of others, means: written "without the {kind}" or "with no {kind} behind");
#     duty_kept, commit_end {kind} {kind_ref}. {kind} is a noun, always "the {kind}": the job, the relationship, the
#     family, the community, the faith. {kind_ref} carries its own article: their work, their relationship, family
#     life, the community, their faith (never after "the", never at a sentence start);
#     need_met {need}; goal_step, goal_setback {goal} (plain, lower case, never at a sentence start);
#     sealed {goal} ("the dream of freedom": the dream that has just become a passion);
#     goal_end {goal} {what} ({goal} is capitalised, "The dream of a working life", so the line starts "{goal}: {what}.");
#     rite, rite_quiet {stage} (juvenile, young adult, adult, mature, elder: "the {stage} years"; rite_quiet is a passage
#     no event marked); closer_to {guild} (plain words, "principled and thoughtful": always "becoming {guild}");
#     title_gain, title_loss, status_gain {what} (a title's say, "a nurse", "married", "out of work": after "is", "being"
#     or "no longer"); perk_gain, perk_loss, perk_helped {what} (a perk's say as a predicate, explain.predicate: "can
#     drive", "has a car", "is a landlord": right after "{N} " or "someone who ").
#     {c} is a color name. It is used once, in a "" variant, in each of the five keys whose default uses it.
#     Not used: {perk} (the perk's catalogue name) and {guild_name} (the guild's game name).
#
# No line names a color: a person in the world does not know about colors.

VOICE = {
    # ================================================================ voice keys: the moment, in the character's own words

    # agree: heart and head want the same thing.
    "agree": [
        ("", "No argument inside me this time: “{heart}”."),
        ("", "My head and my heart point the same way: “{heart}”."),
        ("W", "It's fair, it's right, and I want it too: “{heart}”."),
        ("W", "What I want and what I ought to do line up for once: “{heart}”."),
        ("W", "My conscience and my wishes shake hands on this one: “{heart}”."),
        ("W", "I could look anyone in the eye after “{heart}”, and I want it besides."),
        ("U", "I've thought it through, and my gut agrees: “{heart}”."),
        ("U", "Every way I turn it, the answer comes out the same: “{heart}”."),
        ("U", "The facts point to “{heart}”, and so does my gut. Rare, and welcome."),
        ("U", "I don't need to deliberate this time. “{heart}” is plainly my answer."),
        ("B", "“{heart}”. It's what I want, and it pays. Easy."),
        ("B", "No need to haggle with myself: “{heart}” gets me what I'm after."),
        ("B", "What I want and what works for me are the same thing here: “{heart}”."),
        ("B", "“{heart}”. No trade-offs, no catch I can see. I'll take it."),
        ("R", "“{heart}”! I don't even have to think about it."),
        ("R", "Yes. “{heart}”. All of me is already moving."),
        ("R", "My whole body says “{heart}”, and for once my head says go too."),
        ("R", "“{heart}”, obviously. I don't know why I'm even asking."),
        ("G", "To me it's as natural as water running downhill: “{heart}”."),
        ("G", "“{heart}” sits right with me, all the way down to my roots."),
        ("G", "Some choices simply belong to me, and “{heart}” is one of them."),
        ("G", "“{heart}” feels like coming home. I don't have to think twice."),
    ],

    # heart_over_head: they disagree and the heart is winning (Emren's Red example is the first R line). The second ""
    # line gives the heart's reason ({heart_why}, from HEART_WHY below).
    "heart_over_head": [
        ("", "I know “{head}” makes more sense. I'm going with “{heart}” anyway."),
        ("", "“{heart}” wins, because {heart_why}. I can still hear “{head}”, but only faintly."),
        ("W", "“{head}” is the proper way, I know. But my heart says “{heart}”, and I mean to answer it."),
        ("W", "Anyone sensible would tell me “{head}”. But “{heart}” feels fair to me, and I'll stand by it."),
        ("U", "I can see that “{head}” is the smarter move. I can also see myself choosing “{heart}”."),
        ("U", "My reasoning says “{head}”. Something louder than reasoning says “{heart}”."),
        ("B", "“{head}” is the safe bet. But I want “{heart}”, and I'm not sorry for wanting it."),
        ("B", "Fine, “{head}” is smarter. I'd still rather have what I want: “{heart}”."),
        ("R", "I feel “{heart}” most. “{head}” looks more logical, but I don't care."),
        ("R", "“{heart}”, now. “{head}” can wait for someone with less fire in them than me."),
        ("G", "“{head}” is what my head would pick. Something older and deeper says “{heart}”, and I trust it."),
        ("G", "I'll go where the current takes me: “{heart}”. “{head}” is a path I'd have to force."),
    ],

    # head_over_heart: they disagree and the head is winning. The second "" line gives the head's reason ({head_why}).
    "head_over_heart": [
        ("", "Part of me aches for “{heart}”. The rest of me has already chosen “{head}”."),
        ("", "“{heart}” is tempting, but I'm choosing “{head}”, because {head_why}."),
        ("W", "“{heart}” is what I'd like. “{head}” is what I think is proper, so that's what I'll do."),
        ("W", "My feelings say “{heart}”. But people are counting on me, so: “{head}”."),
        ("U", "I can already see where “{heart}” leads. “{head}” is the better plan."),
        ("U", "“{heart}” is my first instinct. “{head}” is my considered answer, and I'll go with that."),
        ("B", "“{heart}” is what I want right now. “{head}” is what I want more, later."),
        ("B", "I'm not throwing away my advantage on a mood. “{head}”, not “{heart}”."),
        ("R", "Everything in me is shouting “{heart}”. Fine. Just this once, “{head}”."),
        ("R", "I hate it, but “{head}”. “{heart}” will have to burn quietly in me for now."),
        ("G", "“{heart}” calls to me, but this isn't its season. “{head}”."),
        ("G", "Let “{heart}” rest for now. I can feel that “{head}” is the way this needs to go."),
    ],

    # torn: they disagree and it is close. The second "" line gives both reasons, as the engine's default does.
    "torn": [
        ("", "“{heart}” or “{head}”? I keep going back and forth."),
        ("", "Part of me wants “{heart}”, because {heart_why}. Part of me wants “{head}”, because {head_why}."),
        ("W", "Is “{heart}” fair? Is “{head}”? I wish someone would just tell me the rule."),
        ("W", "“{heart}” feels right to me. “{head}” feels proper. Why aren't they the same?"),
        ("W", "If I choose “{heart}”, who gets let down? If I choose “{head}”, who does?"),
        ("W", "Both “{heart}” and “{head}” could be called right. I need a rule to break the tie."),
        ("U", "My case for “{heart}”, my case for “{head}”: they come out almost even, and that bothers me."),
        ("U", "I need one more piece of the puzzle before I can choose between “{heart}” and “{head}”."),
        ("U", "There's a good argument for “{heart}” and a good one for “{head}”. Annoyingly even, to me."),
        ("U", "Let me lay it out again: “{heart}” on one side, “{head}” on the other. Still level."),
        ("B", "“{heart}” pays now, “{head}” pays later. Which is worth more to me?"),
        ("B", "I keep weighing “{heart}” against “{head}”, and the scales won't settle."),
        ("B", "“{heart}” or “{head}”: which one leaves me better off? I honestly can't tell yet."),
        ("B", "I hate a choice where I can't see the winner. “{heart}”? “{head}”?"),
        ("R", "“{heart}”! Or “{head}”? I can't stand not knowing what I want."),
        ("R", "My gut says “{heart}”, then out of nowhere “{head}”. Make up your mind, gut."),
        ("R", "I want “{heart}”, I want “{head}”, and I want this to stop being hard."),
        ("R", "Ugh. “{heart}” tugs one way, “{head}” the other, and I'm the rope."),
        ("G", "Two paths: “{heart}” and “{head}”. Maybe I should wait and see which one feels like home."),
        ("G", "“{heart}” and “{head}” both have roots in me. Pulling up either one will hurt."),
        ("G", "“{heart}” and “{head}” are like two streams. I'll wait to see which one runs deeper."),
        ("G", "My people would understand “{heart}”, and they'd understand “{head}”. That doesn't help me choose."),
    ],

    # want_but_doubt: they agree, but the character doubts it can be done.
    "want_but_doubt": [
        ("", "I want “{x}”. I just don't think I can pull it off."),
        ("", "“{x}” is the one for me. If only I believed it would work."),
        ("W", "I'd like to do “{x}” properly. Whether I can manage it is another question."),
        ("W", "Somebody has to try “{x}”, so I will, even if it probably won't come off."),
        ("U", "“{x}” is the best option I have, and I can see the odds are poor."),
        ("U", "I've checked and checked: “{x}” is the right call, and a long shot."),
        ("B", "“{x}” would get me what I want, if I can get it at all."),
        ("B", "“{x}” is worth having. I just doubt I'm strong enough to take it."),
        ("R", "I want “{x}” so much it hurts. I just don't see it happening."),
        ("R", "“{x}”. Probably hopeless. I want it anyway."),
        ("G", "“{x}” feels like my path, but the ground looks hard and stony."),
        ("G", "Maybe “{x}” isn't meant to happen for me. I'd still like to try."),
    ],

    # dream_calls: they agree because it serves a dream, passion or plan ({goal}: "the dream of a working life",
    # "the passion for freedom", "the plan for doing right and freedom").
    "dream_calls": [
        ("", "“{x}” would bring me a step closer to {goal}."),
        ("", "Whenever I think about {goal}, “{x}” is part of it."),
        ("W", "I promised myself I'd honour {goal}, and “{x}” is how I keep that promise."),
        ("W", "“{x}” is a step toward {goal}, and I mean to see it through properly."),
        ("W", "If I mean to see {goal} through, I have to do my part, and “{x}” is my part."),
        ("W", "“{x}” keeps faith with {goal}. I said I'd work for it, and I will."),
        ("U", "If I'm serious about {goal}, then “{x}” is the logical next step."),
        ("U", "I've mapped the road to {goal}, and “{x}” is on it."),
        ("U", "“{x}” moves me forward on {goal}, exactly as I planned."),
        ("U", "If I do “{x}” now, I make progress on {goal} that I can measure. The logic is simple."),
        ("B", "“{x}” gets me closer to {goal}. That's all I need to know."),
        ("B", "I'll take every step that serves {goal}, starting with “{x}”."),
        ("B", "I mean to make {goal} pay off, and “{x}” is where I start."),
        ("B", "Every step toward {goal} is a step toward what I want. “{x}”, then."),
        ("R", "I can feel {goal} pulling at me, and “{x}” answers it!"),
        ("R", "“{x}”! Anything that feeds {goal} is worth it to me."),
        ("R", "“{x}”! Yes! That's how {goal} starts being real for me."),
        ("R", "My heart's been set on {goal} for ages. “{x}” keeps it racing."),
        ("G", "Something in me has been growing toward {goal} for a long time. “{x}” feeds it."),
        ("G", "“{x}” is a small step on the long road to {goal}, and I'm patient."),
        ("G", "“{x}” is part of the slow growing of {goal}. I won't rush it, and I won't stop."),
        ("G", "Some paths choose you, and the path to {goal} chose me. “{x}” is where it leads now."),
    ],

    # duty: they agree because a role expects it.
    "duty": [
        ("", "“{x}” is what's expected of me, so that's that."),
        ("", "People are counting on me, and what they're counting on is “{x}”."),
        ("W", "“{x}” is my part to play. I won't let the others down."),
        ("W", "If everyone does their share, things work. “{x}” is my share."),
        ("U", "Everyone expects “{x}” from me, and I can see why: it keeps things running."),
        ("U", "I know what my place here asks of me: “{x}”. Simple enough."),
        ("B", "“{x}” is what's expected. Doing it keeps my place, and my place is worth keeping."),
        ("B", "They expect “{x}” of me. Fine. People who deliver get trusted, and trust is useful."),
        ("R", "Everyone's waiting for “{x}”, so all right. But nobody gets to tell me how to feel about it."),
        ("R", "“{x}”. Not because I'm told to, but because they're my people."),
        ("G", "“{x}” is what someone in my place does. It has always been that way."),
        ("G", "My people have always done “{x}”, and now it's my turn."),
    ],

    # need_first: they agree because a need is badly unmet ({need}).
    "need_first": [
        ("", "I'm so short of {need}. “{x}” would help."),
        ("", "Right now I'd take anything that brings me some {need}, and “{x}” does."),
        ("W", "I've put everyone else first for long enough. I need {need} too, and “{x}” helps."),
        ("W", "Everybody deserves some {need}, and I've had too little. “{x}” would give me some."),
        ("U", "The problem is plain: I'm missing {need}. “{x}” is the fix."),
        ("U", "I can't think straight without {need}. “{x}” comes first."),
        ("B", "I'm running low on {need}, and that makes me weak. “{x}” covers it."),
        ("B", "First things first. I need {need}, and “{x}” gets it for me."),
        ("R", "I'm starving for {need}. “{x}”, right now."),
        ("R", "I can't stand going without {need} any longer. “{x}”!"),
        ("G", "A plant can't grow without water, and I can't grow without {need}. “{x}” is rain."),
        ("G", "Something in me is wilting for want of {need}. “{x}” would tend it."),
    ],

    # habit: they agree because it is the usual way.
    "habit": [
        ("", "“{x}”, the way I always do."),
        ("", "I don't even have to decide. “{x}”, same as ever."),
        ("W", "There's a proper way of doing this, and mine is “{x}”."),
        ("W", "“{x}” is how I always handle this. Being steady is a kind of promise I keep."),
        ("U", "“{x}” has worked for me before. No reason to reinvent it."),
        ("U", "I've tried other ways. “{x}” is the one that works for me."),
        ("B", "“{x}”. Why change what keeps working for me?"),
        ("B", "I know “{x}” inside out. That's an edge, and I'm keeping it."),
        ("R", "“{x}”, like always. I'm halfway into it before I've even thought."),
        ("R", "I don't stop to think. “{x}”, the way my body already knows."),
        ("G", "“{x}”, like a path worn through the grass. My feet just follow it."),
        ("G", "It's always been “{x}” for me. Old ways are old for a reason."),
    ],

    # becoming: they agree because it is who the character wants to become.
    "becoming": [
        ("", "“{x}” is who I want to be."),
        ("", "The person I'm trying to become would choose “{x}”."),
        ("W", "I want to be someone people can rely on. Someone like that chooses “{x}”."),
        ("W", "“{x}”. That's the kind of person I mean to be: fair, steady, there."),
        ("W", "I want to be someone who does the decent thing without being asked. “{x}”."),
        ("W", "When I look back on my life, I want to see “{x}” in it."),
        ("U", "I'm becoming someone who thinks before acting. That person picks “{x}”."),
        ("U", "“{x}” is practice for the person I'm working on being."),
        ("U", "Every time I choose like this, I get closer to the mind I want: “{x}”."),
        ("U", "“{x}” is the sort of choice the person I'm studying to be would make."),
        ("B", "“{x}” is what the stronger version of me does. I'm getting there."),
        ("B", "I'm building myself into someone who wins. “{x}” is part of the build."),
        ("B", "The me I'm building doesn't hesitate. “{x}”."),
        ("B", "“{x}” is one more brick in the person I'm making of myself."),
        ("R", "“{x}”! That's me, the real me, the one I want everyone to see."),
        ("R", "I want to be someone who lives out loud. Someone like that says yes to “{x}”."),
        ("R", "“{x}”: that's who I am when I'm most myself."),
        ("R", "I'm done being who other people want. “{x}” is me."),
        ("G", "“{x}” is who I'm growing into, slowly, the way a tree grows into its shape."),
        ("G", "I'm growing toward the person I'm meant to be, and “{x}” is part of that."),
        ("G", "“{x}” is the kind of thing the people I come from would be proud to see in me."),
        ("G", "A tree becomes what it is by growing, a little each year. “{x}” is my growing."),
    ],

    # time_short: they agree because time feels short.
    "time_short": [
        ("", "Time is running out on me. “{x}”, now."),
        ("", "If not now, maybe never. I choose “{x}”."),
        ("W", "Time is short, and I want to leave things in order. “{x}”."),
        ("W", "I may not get another chance to do this properly. “{x}”."),
        ("W", "There are things I owe people before time runs out. “{x}” is one of them."),
        ("W", "I'd rather do this properly now than leave it undone. “{x}”."),
        ("U", "If I wait, the chance closes. The timing tells me “{x}”."),
        ("U", "I've looked at the time I have left for this, and it's not much. “{x}” first."),
        ("U", "The window for this is closing; I can see it. “{x}”, while it's open."),
        ("U", "Waiting has a cost, and the cost is rising for me. “{x}”."),
        ("B", "The clock is running, and I'm not losing this chance. “{x}”."),
        ("B", "No time for me to be polite about it. “{x}”, before the door shuts."),
        ("B", "Opportunities don't wait for me, so I won't wait for them. “{x}”."),
        ("B", "I've no time to lose, and nothing to gain by waiting. “{x}”."),
        ("R", "Time's running out, and I'm not wasting what's left. “{x}”!"),
        ("R", "Life's too short for me to wait. “{x}”, while I still can."),
        ("R", "Now, now, now. “{x}”, before I miss it."),
        ("R", "I'm not spending what time I have on maybe. “{x}”!"),
        ("G", "Every season ends. Before this one does, I choose “{x}”."),
        ("G", "Days like this don't come around for me forever. “{x}”, while they're here."),
        ("G", "Everything has its season, and mine is passing. “{x}”, while it's still mine."),
        ("G", "The days are getting shorter for me. “{x}”, while the light lasts."),
    ],

    # stuck: the character sees no way at all (no option fills).
    "stuck": [
        ("", "I can't see any way through this."),
        ("", "Every door I look at is shut."),
        ("W", "There's no right way out of this one, and no rule that helps me."),
        ("W", "I'd do the proper thing if I could find it. I can't."),
        ("U", "I've looked at this from every side, and I can't find a single move."),
        ("U", "No plan fits this. I don't have enough to work with."),
        ("B", "Nothing to trade, nothing to use, no way to win. I hate this."),
        ("B", "For once I have nothing to bargain with."),
        ("R", "I want to scream, and there's still no way out."),
        ("R", "Trapped. I can feel it in my chest, and I can't do a thing."),
        ("G", "Sometimes all I can do is wait for the weather to change."),
        ("G", "No path here. Maybe I'm meant to stand still for a while."),
    ],

    # ================================================================ asides: what in the character bent this moment
    # Third person, {N} only (an aside can come with "stuck", when the option fills are empty).

    # stressed: under strain the heart speaks louder.
    "stressed": [
        ("", "{N} is under so much strain that every feeling comes out louder."),
        ("", "Worn thin, {N} hears the heart far more than the head."),
        ("W", "{N} is carrying too many duties at once, and it is starting to show."),
        ("W", "With so much owed to so many, {N} has little calm left."),
        ("U", "Stress is fogging {N}'s thinking, and {N} can tell."),
        ("U", "Too much is pressing in; {N} cannot think as clearly as usual."),
        ("B", "Under this much pressure, {N} reaches for whatever feels good first."),
        ("B", "{N} is stretched tight, and pressure makes anyone grab what is nearest."),
        ("R", "{N} is wound up tight, ready to snap at anything."),
        ("R", "{N}'s nerves are raw, and every spark catches."),
        ("G", "{N} is like a tree in a storm: bending, not thinking."),
        ("G", "{N} is shaken, and the oldest instincts are taking over."),
    ],

    # little_control: they disagree, and the character rarely overrules a feeling.
    "little_control": [
        ("", "{N} rarely talks a feeling down once it gets going."),
        ("", "When a feeling takes hold, {N} usually lets it steer."),
        ("W", "{N} means to keep to the rules, but feelings often win the argument."),
        ("W", "{N} believes in self-restraint more easily than {N} practises it."),
        ("U", "{N} can see the sensible move; acting on it is the hard part."),
        ("U", "{N}'s thinking is quick, but it seldom holds the reins."),
        ("B", "{N} wants what {N} wants, right away, and rarely argues with that."),
        ("B", "{N} seldom tells a craving no."),
        ("R", "{N} lives by feel, and seldom stops to argue with it."),
        ("R", "Once {N} is fired up, nobody talks them down, least of all {N}."),
        ("G", "{N} follows instinct the way a river follows the land."),
        ("G", "{N} trusts the pull of the moment, and rarely resists it."),
    ],

    # disciplined: learned self-control is high.
    "disciplined": [
        ("", "{N} has learned to hold to a decision, even when it stings."),
        ("", "Practice has given {N} a firm grip on impulses."),
        ("W", "{N} has made a habit of keeping promises, including those made to themselves."),
        ("W", "Keeping faith with what is right has made {N} steady."),
        ("U", "{N} has trained the mind to wait before it acts."),
        ("U", "{N} has learned to let a feeling pass, then decide."),
        ("B", "{N} has learned that self-control is a kind of power."),
        ("B", "{N} can say no to now for the sake of later."),
        ("R", "{N} has learned to aim the fire instead of just letting it burn."),
        ("R", "{N} still feels everything, but has learned to choose the moment."),
        ("G", "Like a tree that bends but holds, {N} has learned to stand firm."),
        ("G", "{N} has learned patience the slow way, and it holds."),
    ],

    # undisciplined: learned self-control is low.
    "undisciplined": [
        ("", "{N} has grown used to giving in, and it shows."),
        ("", "Giving in has become easy for {N}, and easy is hard to unlearn."),
        ("W", "{N} has let a few promises slide, and each slide comes easier."),
        ("W", "{N} knows the rules but has stopped holding to them."),
        ("W", "{N} keeps meaning to hold the line, and keeps not holding it."),
        ("W", "{N}'s good intentions have been giving way more often lately."),
        ("U", "{N} knows the pattern by now: give in, regret it, repeat."),
        ("U", "{N} keeps making plans and then dropping them."),
        ("U", "{N} can predict the giving in, and still gives in."),
        ("U", "{N}'s plans have stopped surviving the moment of temptation."),
        ("B", "{N} has stopped saying no to what feels good."),
        ("B", "Lately {N} grabs what is closest and leaves tomorrow to tomorrow."),
        ("B", "{N} has been taking the quick reward over the bigger one."),
        ("B", "{N} keeps cashing in early on what could have grown."),
        ("R", "{N} has stopped fighting the urges and just rides them."),
        ("R", "These days {N} follows every spark wherever it leads."),
        ("R", "{N} has been saying yes to every impulse lately."),
        ("R", "Lately {N} cannot sit with a want for long."),
        ("G", "{N} has been drifting, letting the current choose."),
        ("G", "{N} has stopped tending the habit of holding firm, and it is wilting."),
        ("G", "{N} has been bending with every breeze."),
        ("G", "{N}'s patience is wearing away, like a riverbank in flood."),
    ],

    # blind_spot: the best way is open, but the character does not think of it.
    "blind_spot": [
        ("", "{N} hasn't noticed every way through this."),
        ("", "A better way is open here, but {N} cannot see it."),
        ("W", "{N} looks only at the proper options, and misses one that would work."),
        ("W", "Following the usual rules, {N} walks right past a better way."),
        ("U", "Even {N}, who notices so much, has missed an option here."),
        ("U", "{N} has not spotted the best move yet."),
        ("B", "An easy advantage sits right in front of {N}, unseen."),
        ("B", "{N} is missing an angle that would pay off."),
        ("R", "{N} is so caught up in the moment that a better way slips by."),
        ("R", "In the heat of it, {N} misses a door standing wide open."),
        ("G", "{N} keeps to the familiar path and misses a gentler one."),
        ("G", "A way through grows right beside {N}, unnoticed."),
    ],

    # out_of_reach: the best way is closed (by the world or by means).
    "out_of_reach": [
        ("", "The choice {N} would really make is out of reach."),
        ("", "The way {N} would most like to go is closed."),
        ("W", "The fairest way out is closed to {N}, and that feels wrong."),
        ("W", "What {N} thinks ought to happen is simply not possible here."),
        ("W", "The proper way through is barred to {N} here."),
        ("W", "{N} can see what would be fair, and cannot reach it."),
        ("U", "{N} can see the best solution clearly. It just isn't available."),
        ("U", "The option {N} would pick, all things weighed, is closed."),
        ("U", "The best option exists, but {N} cannot get to it."),
        ("U", "{N}'s first choice is ruled out before it starts."),
        ("B", "What {N} really wants is beyond reach, for now."),
        ("B", "{N} can see the prize, and the door to it is locked."),
        ("B", "The thing {N} would take, given the chance, is not within reach."),
        ("B", "{N} has neither the means nor the opening for what they really want."),
        ("R", "What {N}'s heart wants most is not on the table."),
        ("R", "The thing {N} is burning for is just out of reach."),
        ("R", "{N} would go straight for it, if it were there to go for."),
        ("R", "The door {N}'s heart wants is shut tight."),
        ("G", "What {N} longs for isn't growing here, not this season."),
        ("G", "The way {N} would choose is closed, like a path under snow."),
        ("G", "What {N} would choose belongs to another place or time."),
        ("G", "The path {N} longs for is overgrown and closed for now."),
    ],

    # hopeful: a high outlook makes the character think the likely pick better than it is.
    "hopeful": [
        ("", "{N} expects this to go well, maybe better than it will."),
        ("", "{N} is sure it will all work out."),
        ("W", "{N} trusts that doing things properly will be rewarded."),
        ("W", "{N} believes fairness will win out here."),
        ("U", "{N}'s reckoning comes out rosy, perhaps too rosy."),
        ("U", "{N} is confident the plan will hold."),
        ("B", "{N} is sure of winning this one."),
        ("B", "{N} rates their own chances very highly."),
        ("R", "{N} feels lucky today, all the way down."),
        ("R", "{N} is riding high, and nothing looks hard from up here."),
        ("G", "{N} trusts things will turn out the way they are meant to."),
        ("G", "{N} feels the wind at their back."),
    ],

    # gloomy: a low outlook makes the character think the likely pick worse than it is.
    "gloomy": [
        ("", "{N} is braced for it to go wrong."),
        ("", "{N} doubts anything good can come of this."),
        ("W", "{N} expects to be let down, as usual."),
        ("W", "{N} doubts the world will play fair this time."),
        ("U", "{N} has worked out every way this could fail."),
        ("U", "Every outcome {N} imagines ends badly."),
        ("B", "{N} assumes the odds are stacked against them."),
        ("B", "{N} expects to lose, and is already counting the cost."),
        ("R", "{N} feels beaten before anything has even started."),
        ("R", "A heavy mood has {N} sure this will go wrong."),
        ("G", "{N} feels a long winter coming."),
        ("G", "{N} expects a poor harvest from this."),
    ],

    # short_horizon: time felt short is part of what drives the likely pick.
    "short_horizon": [
        ("", "{N} feels the time slipping away."),
        ("", "{N} is more aware than usual that time is limited."),
        ("W", "{N} wants to set things right while there is still time."),
        ("W", "{N} feels how little time is left to do what is owed."),
        ("W", "{N} feels the duties piling up against the time left to meet them."),
        ("W", "With time feeling short, {N} wants every promise kept."),
        ("U", "{N} has noticed how fast time is passing."),
        ("U", "{N} is measuring the time left, and it is not much."),
        ("U", "{N} keeps noticing how much has passed, and how little may be left."),
        ("U", "Time pressure is shaping {N}'s choices, and {N} knows it."),
        ("B", "{N} feels the window for getting what they want closing."),
        ("B", "{N} knows chances do not wait, and time is running down."),
        ("B", "{N} senses chances slipping away, and wants to grab them first."),
        ("B", "{N} wants results soon; later may not come."),
        ("R", "{N} wants to live it all now, before it is gone."),
        ("R", "{N} can hear the clock ticking, loudly."),
        ("R", "{N} feels the hurry of a life that won't wait."),
        ("R", "Every moment feels precious to {N} now, and short."),
        ("G", "{N} feels the season turning, and the days growing shorter."),
        ("G", "{N} senses a season of life drawing to its close."),
        ("G", "{N} senses the year turning, and their own years with it."),
        ("G", "Like autumn leaves, {N}'s days feel fewer."),
    ],

    # lacks: the best way needs a title or perk the character does not hold. Fills: {N}, {what} (that title's or
    # perk's say: "a nurse", "married", "can drive", "a local hero"). Title says follow "is", perk says follow the
    # name, and some perk says are nouns, so {what} always comes after a colon at the end of the line.
    "lacks": [
        ("", "The way {N} would choose is open only to those who fit this: {what}."),
        ("", "To go the way {N} wants, {N} would have to fit this: {what}."),
        ("W", "The right way here asks for something {N} does not have yet: {what}."),
        ("W", "For {N}, the rules keep the best way for those who qualify: {what}."),
        ("U", "{N} sees the best option, and the missing piece: {what}."),
        ("U", "The best move has a requirement {N} cannot meet yet: {what}."),
        ("B", "{N} could take the best way, if only {N} had what it takes: {what}."),
        ("B", "The prize is there for {N}, but the ticket in is missing: {what}."),
        ("R", "{N} would leap at it, but it takes what {N} lacks: {what}."),
        ("R", "The door {N} wants opens only for this: {what}."),
        ("G", "The way {N} longs for is for those who have grown into it: {what}."),
        ("G", "That path belongs to someone further along than {N}: {what}."),
    ],
}

LESSONS = {
    # ================================================================ lessons: how the world works, as this week showed it
    # Third person, present tense. The variant follows the character's strongest color, not the act's: each color
    # tells the same mechanism through its own eyes, whatever the act was.

    # practice: the act worked; acting in its ways makes the person better at them. Fills: {c} (the act's color).
    "practice": [
        ("", "Each time {c} ways work for {N}, they come a little easier."),
        ("", "What works once comes easier the next time."),
        ("W", "Doing a thing properly, again and again, makes it part of who a person is."),
        ("W", "When a way of acting holds up, others trust it more, and so does {N}."),
        ("W", "A way of acting that keeps working becomes a way {N} can be counted on."),
        ("W", "Doing well what one set out to do builds a quiet confidence."),
        ("U", "Each success adds to what {N} knows how to do."),
        ("U", "Skill grows from what works: the mind keeps whatever proved useful."),
        ("U", "The mind learns from results: what worked is remembered and refined."),
        ("U", "Each success sharpens a method, and sharper methods succeed more often."),
        ("B", "What gets results gets used again. That is how strengths are built."),
        ("B", "Every win is a tool {N} gets to keep."),
        ("B", "Success breeds success: each win makes the next one easier to take."),
        ("B", "Strength grows where it is used and rewarded."),
        ("R", "Doing what works makes the next try faster and bolder."),
        ("R", "Success feeds the nerve: {N} reaches for that move more readily now."),
        ("R", "Getting it right once gives the heart the nerve to go again."),
        ("R", "What works feels good, and what feels good gets done again."),
        ("G", "A path walked often becomes easy underfoot."),
        ("G", "Skills grow like roots: quietly, a little more each time they are used."),
        ("G", "What is tended and bears fruit is tended again."),
        ("G", "A skill that works settles in, the way a seed settles into soil."),
    ],

    # hard_win: the head chose a hard thing, against poor odds, and it worked.
    "hard_win": [
        ("", "Pulling off a hard thing on purpose makes the next hard thing feel possible."),
        ("", "Choosing the difficult road, and making it, strengthens the will."),
        ("W", "Holding to the harder course teaches a person to trust their own resolve."),
        ("W", "Hard things done on purpose make a person steadier."),
        ("U", "Beating the odds by choice teaches the mind that it can steer."),
        ("U", "A long shot taken with care, and won, makes patience feel worth it."),
        ("B", "Winning the hard way builds a will that can be relied on."),
        ("B", "Each hard-won victory makes the next sacrifice easier to make."),
        ("R", "Pushing through when quitting would be easier makes the fire steadier."),
        ("R", "Grit grows by being used, and today it gets used."),
        ("G", "Like wood that grows dense in hard winters, will grows in hard choices."),
        ("G", "What is earned slowly against the odds roots deep."),
    ],

    # self_control_up: an act of discipline; it builds self-control whether or not it works out.
    "self_control_up": [
        ("", "Holding firm builds self-control, whether or not it pays off this time."),
        ("", "Every promise kept to oneself makes the next one easier to keep."),
        ("W", "Self-control is built like trust: by keeping one's word, especially when it costs."),
        ("W", "Each time {N} holds to a rule of their own, the rule gets easier to hold."),
        ("U", "Self-control works like a muscle: using it is what strengthens it."),
        ("U", "Sticking to the plan, even unrewarded, trains the mind to stick next time."),
        ("B", "Saying no to now, for something later, builds a power that lasts."),
        ("B", "Each time {N} holds back, {N} gets better at holding back."),
        ("R", "Sticking with something when the fire dims teaches the heart to stay."),
        ("R", "Holding on through the dull part makes holding on easier."),
        ("G", "Patience grows with tending, like anything that lives."),
        ("G", "Each time {N} holds steady, the roots of patience go a little deeper."),
    ],

    # self_control_down: giving in or giving up; it wears self-control down either way.
    "self_control_down": [
        ("", "Giving in once makes giving in a little easier next time."),
        ("", "Every time a resolve is dropped, the next one sits looser."),
        ("W", "Each promise to oneself that breaks makes the next one easier to break."),
        ("W", "When a rule {N} set for themselves slides, it slides more easily next time."),
        ("U", "Each time a person gives in, the mind learns that giving in is an option."),
        ("U", "Each dropped plan makes dropping plans a little more normal."),
        ("B", "Taking the easy option costs a little of the grip {N} has on things."),
        ("B", "Every small surrender spends a little of {N}'s will."),
        ("R", "Giving in feels good now, and it loosens the reins a little more."),
        ("R", "The more the heart gets its way, the harder it is to tell it no."),
        ("G", "Like a path through grass, giving in wears itself deeper each time."),
        ("G", "Each time {N} lets go, the letting go puts down another root."),
    ],

    # surprise_teaches: a big surprise teaches the most. Fills: {dir} {c} ("more Red", "less Blue").
    "surprise_teaches": [
        ("", "An outcome nobody expected teaches the most: {N} leans {dir} {c} for it."),
        ("", "What turns out differently than expected leaves the deepest mark."),
        ("W", "When things defy expectations, a person rethinks what they held to be sure."),
        ("W", "A surprise like this makes {N} question the rules they counted on."),
        ("W", "An outcome no one predicted makes a person re-examine what they took for granted."),
        ("W", "When the expected does not happen, the rules a person lives by shift a little."),
        ("U", "Being wrong about an outcome teaches more than being right."),
        ("U", "The bigger the surprise, the more {N} redraws their picture of the world."),
        ("U", "The gap between what was expected and what happened is where learning lives."),
        ("U", "A broken prediction teaches more than many that came true."),
        ("B", "An unexpected result shows what actually pays, and {N} takes note."),
        ("B", "Surprises show where the real advantage lies."),
        ("B", "When the unexpected pays off, or costs dearly, {N} remembers exactly why."),
        ("B", "Surprises reveal who really holds the cards, and {N} adjusts."),
        ("R", "Being knocked sideways by an outcome stays with a person far longer."),
        ("R", "A shock, good or bad, rewires the gut a little."),
        ("R", "Shocks stick: a jolt like this changes what the gut reaches for next."),
        ("R", "The unexpected hits harder, and the heart does not forget the blow or the thrill."),
        ("G", "The unexpected turns a person, the way a flood moves a river."),
        ("G", "What comes out of nowhere reshapes the ground under {N}."),
        ("G", "Like a storm that changes a coastline, a surprise reshapes a person."),
        ("G", "Sudden turns of fortune leave their mark the way a frost marks the leaves."),
    ],

    # fail_own_ways: a big failure in the person's own ways turns them toward what the moment called for.
    "fail_own_ways": [
        ("", "When {N}'s usual way fails badly, {N} starts looking for other ways."),
        ("", "A big failure in familiar ways opens the mind to unfamiliar ones."),
        ("W", "When the proper way fails badly, even firm rules start to bend."),
        ("W", "A hard fall in one's own ways shows what the moment really needed."),
        ("U", "When a trusted method fails badly, the mind starts testing other methods."),
        ("U", "A big miss is a clue: it points toward what would have worked."),
        ("B", "When the old tools stop working, {N} picks up new ones."),
        ("B", "A costly failure sends a person shopping for a better strategy."),
        ("R", "Crashing hard the usual way makes even a stubborn heart try something new."),
        ("R", "When the gut leads straight into a wall, {N} starts listening to other voices."),
        ("G", "A tree battered from one side grows toward the other."),
        ("G", "When the familiar path washes out, a person learns another way across."),
    ],

    # defended: a failure in long-held ways does not shake the belief.
    "defended": [
        ("", "{N} has lived this way long enough that a stumble does not shake it."),
        ("", "A long-held belief can take a failure without breaking."),
        ("W", "A way of life practised for long is sturdy against bad days."),
        ("W", "When a way has held for years, a single failure reads as bad luck."),
        ("U", "A long record of success outweighs a fresh failure in the mind."),
        ("U", "With enough experience behind a belief, a bad result gets explained away."),
        ("B", "A setback does not undo a strategy that has paid for so long."),
        ("B", "Seasoned confidence shrugs off a loss."),
        ("R", "When something runs this deep in a person, a bad day makes them hold on tighter."),
        ("R", "A heart that has been true to itself this long does not flinch at a blow."),
        ("G", "Old roots hold through a bad storm."),
        ("G", "A way of life grown over many seasons is not uprooted by a bad season."),
    ],

    # habit: the act builds habit; repeating it makes it pull harder.
    "habit": [
        ("", "Each time it is done, it becomes a little more automatic."),
        ("", "Things done often start to do themselves."),
        ("W", "Routines that are kept end up keeping the person in return."),
        ("W", "What is done regularly becomes part of how a person runs their days."),
        ("W", "What is done faithfully each day becomes hard to leave undone."),
        ("W", "Repeating a thing turns it from a choice into a custom."),
        ("U", "Repetition carves a groove, and the mind slides into it."),
        ("U", "The mind loves a shortcut: what is repeated gets chosen faster."),
        ("U", "Each repeat makes the choice cheaper to make and harder to notice."),
        ("U", "Habits save effort, and that is exactly why they grip so tightly."),
        ("B", "Every repeat makes it more {N}'s own, and harder to give up."),
        ("B", "A habit pays in comfort and charges in freedom, a little more each time."),
        ("B", "A habit is a small bargain: easier now, a little less free later."),
        ("B", "The more it is done, the more it owns a little of {N}."),
        ("R", "The more it is done, the louder it calls."),
        ("R", "Doing it again lights the same spark, and the spark wants more."),
        ("R", "What starts as a spark, repeated, becomes a pull that is hard to resist."),
        ("R", "Doing it again and again carves it into the body."),
        ("G", "The more a path is walked, the harder it is to step off it."),
        ("G", "Habits grow like ivy: slowly, then everywhere."),
        ("G", "Each repetition is a root going down, and roots hold."),
        ("G", "Like water shaping stone, repetition shapes a person slowly and surely."),
    ],

    # door: the act worked and opened a door to new ways. Fills: {c} (the act's color).
    "door": [
        ("", "A new door has opened, and what lies behind it leans {c}."),
        ("", "A new experience shows a person ways they had never considered."),
        ("W", "New company brings new expectations, and {N} begins to feel them."),
        ("W", "Meeting new people widens a person's sense of what is fair and possible."),
        ("U", "Seeing something new raises questions, and questions pull a person forward."),
        ("U", "Every new place or person adds to the map {N} carries."),
        ("B", "New doors mean new chances, and {N} starts wanting what is behind them."),
        ("B", "A new connection is something new to work with, and it changes what {N} goes after."),
        ("R", "A taste of something new wakes a hunger for more of it."),
        ("R", "New places, new people: suddenly {N} wants things {N} never wanted before."),
        ("G", "New ground brings new seeds, and some of them take root."),
        ("G", "Time among new people slowly changes what feels like home."),
    ],

    # binding: the act worked and started an obligation that is hard to undo.
    "binding": [
        ("", "A bond like this holds firm, and takes some freedom with it."),
        ("", "Some commitments are easy to make and hard to undo."),
        ("W", "A vow kept is a weight carried, and also a place to stand."),
        ("W", "Binding oneself gives others something to count on, and asks for freedom in return."),
        ("U", "A commitment narrows the future: fewer options, more certainty."),
        ("U", "Tying oneself down trades some choices for a clearer road."),
        ("B", "Every bond has a price, paid in freedom."),
        ("B", "A tie like this holds {N} as surely as it helps."),
        ("R", "Being tied down chafes, even when the tie was chosen freely."),
        ("R", "A bond made from the heart is hard to slip out of later."),
        ("G", "Once something takes root, it is not easily pulled up."),
        ("G", "Ties grow like vines: they hold a person up and hold them in place."),
    ],

    # backfire: an option closed by law, approval or means was taken, and it failed. Fills: {kind} = law,
    # approval of others, means (so: "without the {kind}", "with no {kind} behind").
    "backfire": [
        ("", "Acting with no {kind} behind it costs extra when it fails."),
        ("", "Going ahead without the {kind} has a price when it does not work."),
        ("W", "Acting without the {kind} on one's side makes a fall land harder."),
        ("W", "When something done without the {kind} fails, the cost comes due."),
        ("U", "Without the {kind}, a failure has fewer safety nets."),
        ("U", "The risk of acting without the {kind} is real, and failure collects it."),
        ("B", "Acting without the {kind} is a gamble, and a lost gamble is paid in full."),
        ("B", "Going it alone, with no {kind} behind {N}, makes a failure cost more."),
        ("R", "Charging ahead without the {kind} feels free, until it fails and the bill arrives."),
        ("R", "Leaping without the {kind} behind them, a person lands hard when it fails."),
        ("G", "Pushing against the grain, with no {kind} behind it, brings a hard fall."),
        ("G", "What grows without the {kind} to shelter it is easily broken."),
    ],

    # need_met: the act met a need that was lacking. Fills: {need}.
    "need_met": [
        ("", "Getting what was most missing, {need}, lifts a person more than anything else."),
        ("", "The hungrier a need, the more it means to have it met: {need}, at last."),
        ("W", "When someone finally gets the {need} they lacked, everything else steadies."),
        ("W", "A person with enough {need} has more to give to others."),
        ("U", "Satisfaction rises most where something was lacking, and {N} lacked {need}."),
        ("U", "Fixing the biggest gap, {need}, matters more than polishing what already works."),
        ("B", "What is scarce is worth the most, and {N} was short of {need}."),
        ("B", "Covering a shortfall in {need} pays back more than adding to plenty."),
        ("R", "Getting {need} after going without it feels better than almost anything."),
        ("R", "Water tastes best to the thirsty, and {N} was thirsty for {need}."),
        ("G", "A dry field drinks the rain fastest, and {N} had gone without {need}."),
        ("G", "Like sun after a long winter, {need} brings back what was wilting."),
    ],

    # duty_kept: a held commitment's own moment went well, and living up to it deepens it. Fills: {kind} (job,
    # relationship, family, community, faith: always "the {kind}", never the subject of a verb) and {kind_ref} (their
    # work, their relationship, family life, the community, their faith: it brings its own article).
    "duty_kept": [
        ("", "Living up to the {kind} deepens the bond."),
        ("", "Every hour {N} gives to {kind_ref} makes the tie a little stronger."),
        ("W", "Doing what is owed to the {kind} binds {N} a little closer."),
        ("W", "Keeping a commitment strengthens it: {N} is bound more firmly to the {kind}."),
        ("U", "Each effort {N} spends on {kind_ref} makes the next one feel more natural."),
        ("U", "The more {N} puts into the {kind}, the more reason there is to keep putting in."),
        ("B", "When {N} comes through in {kind_ref}, the stake grows, and stakes are hard to walk away from."),
        ("B", "Each success {N} has in {kind_ref} is an investment that makes leaving costlier."),
        ("R", "Giving the heart fully to the {kind} makes the bond burn brighter."),
        ("R", "When {N} pours real feeling into {kind_ref}, duty turns into devotion."),
        ("G", "{N} tends {kind_ref} season after season, and the roots go deeper."),
        ("G", "What is cared for grows, and {N}'s care for the {kind} grows with it."),
    ],

    # ---------------------------------------------------------------- commitments, goals and life events

    # commit_start: a commitment started (or was inherited). Fills: {kind} and {kind_ref} (as in duty_kept), {c}
    # ("Red and Green").
    "commit_start": [
        ("", "With the {kind} comes a new way of living, and it pulls {N} toward {c}."),
        ("", "Along with the {kind} come new habits, new people and new expectations."),
        ("W", "Duties arrive with the {kind}, and duties shape a person over time."),
        ("W", "With the {kind} come new rules to live by, and they slowly become {N}'s own."),
        ("U", "Every commitment has its own logic, and with the {kind}, {N} begins to learn it."),
        ("U", "Starting out with the {kind} changes the questions {N} asks every day."),
        ("B", "New chances and new costs arrive with the {kind}, and both change a person."),
        ("B", "Being bound to the {kind} changes what {N} wants, not just what {N} does."),
        ("R", "With the {kind} in {N}'s life, what {N} longs for starts to change."),
        ("R", "New feelings come with the {kind}, and new feelings change a person."),
        ("G", "With the {kind}, {N} is planted in new soil, and the soil shapes what grows."),
        ("G", "New roots go down with the {kind}, and roots change the tree."),
    ],

    # commit_end: a commitment ended (left, lost job, broke up, widowed, retired: every line fits all of them, a
    # bereavement included). Fills: {kind} and {kind_ref} (as in duty_kept).
    "commit_end": [
        ("", "An ending costs what was put into the {kind}, and frees the time and care it took."),
        ("", "Life without the {kind} leaves gaps, and room."),
        ("W", "Without the {kind}, a whole set of duties falls away, and some shelter with it."),
        ("W", "Losing the {kind} leaves promises with nowhere to go, until new ones take their place."),
        ("U", "What was built around the {kind} has to be rebuilt around something else."),
        ("U", "Without the {kind}, the days lose a shape they had, and the mind looks for a new one."),
        ("B", "Without the {kind}, what was invested is gone, and so is what it paid back."),
        ("B", "Losing the {kind} costs a stake, and leaves {N} to decide what to build next."),
        ("R", "Losing the {kind} hurts, and the hurt changes what the heart reaches for."),
        ("R", "Life without the {kind} feels emptier, and the heart goes looking for what can fill it."),
        ("G", "When a season ends, what it grew returns to the soil. So it goes with {kind_ref}."),
        ("G", "After an ending like this, life is a field left fallow: bare, and resting."),
    ],

    # goal_step: a step toward a dream, passion or plan worked. Fills: {goal} ("the dream of a working life", "the
    # passion for freedom", "the plan for doing right and freedom": the goal's name, so it grows, is fed or tested).
    "goal_step": [
        ("", "Every step that works makes {goal} feel more real."),
        ("", "Progress feeds a goal, and {goal} grows stronger for it."),
        ("W", "Keeping at {goal}, step by careful step, makes it sturdier."),
        ("W", "Each step done properly builds {N}'s faith in {goal}."),
        ("U", "Each step that works is evidence for {goal}: it can be done."),
        ("U", "Progress confirms the reasoning: {goal} looks more possible now."),
        ("B", "Every gain toward {goal} makes {N} want it more."),
        ("B", "Each success is a payment toward {goal}."),
        ("R", "Each win toward {goal} makes the wanting burn hotter."),
        ("R", "Progress is fuel, and {goal} feels closer and brighter for it."),
        ("G", "Like a seedling in sun, {goal} grows with each good step."),
        ("G", "Small steps that work are how {goal} takes root."),
    ],

    # goal_setback: a step toward a dream, passion or plan failed. Fills: {goal}.
    "goal_setback": [
        ("", "A setback shakes {goal}, and doubt makes the shaking worse."),
        ("", "Failing a step toward {goal} makes it feel further away."),
        ("W", "When effort toward {goal} fails, the commitment to it is tested."),
        ("W", "A setback puts {goal} on trial in {N}'s mind."),
        ("U", "A failed step is evidence too, and {N} trusts {goal} a little less for it."),
        ("U", "Setbacks make {goal} look less likely, and doubt makes it look worse still."),
        ("B", "A loss on the way to {goal} raises the price of keeping at it."),
        ("B", "Every setback makes {N} weigh whether {goal} is still worth the cost."),
        ("R", "A blow like this cools {goal}, especially when the heart starts to doubt."),
        ("R", "Setbacks sting, and the sting makes {goal} feel smaller."),
        ("G", "A late frost sets {goal} back, though roots can survive a frost."),
        ("G", "Not every season is kind to {goal}; some set it back."),
    ],

    # sealed: a dream that kept working, and felt like the person's own, became a passion. Fills: {goal}
    # (the dream's name, "the dream of freedom").
    "sealed": [
        ("", "Tries that worked and felt true have turned {goal} into a passion."),
        ("", "Fed by success that felt like {N}'s own, {goal} is now a passion."),
        ("W", "Kept faithfully and rewarded, {goal} has become something {N} lives by."),
        ("W", "A dream honoured long enough becomes a calling: {goal} is a passion now."),
        ("U", "Enough tries that worked, each freely chosen, turn {goal} into a passion."),
        ("U", "Proof that it works, and that it is truly {N}'s, makes {goal} a passion."),
        ("B", "Wins that felt like {N}'s own have made {goal} something {N} will not give up."),
        ("B", "Success that is truly {N}'s own turns a want into a passion: {goal}."),
        ("R", "Every try that worked and felt alive has set {goal} alight: a passion now."),
        ("R", "When it works and feels like {N}, {goal} turns into a passion."),
        ("G", "Watered by success and freely loved, {goal} has rooted into a passion."),
        ("G", "Grown in good soil, {goal} has become part of {N}: a passion."),
    ],

    # goal_end: a dream, passion or plan ended. Fills: {goal} (capitalised: "The dream of a working life") and {what}
    # (achieved, let go, faded, drifted away, pushed aside, not reached in time). The second sentence fits every end.
    "goal_end": [
        ("", "{goal}: {what}. Every goal ends somehow, and the ending shapes what comes next."),
        ("", "{goal}: {what}. What it asked of {N} leaves its mark either way."),
        ("W", "{goal}: {what}. Whatever the ending, what was given to it was real."),
        ("W", "{goal}: {what}. An ending settles accounts and leaves room for new promises."),
        ("U", "{goal}: {what}. How a goal ends teaches what to aim for next."),
        ("U", "{goal}: {what}. Each ending sharpens the picture of what is worth pursuing."),
        ("B", "{goal}: {what}. What it cost, and what it paid, can be counted now."),
        ("B", "{goal}: {what}. An ended goal frees effort for the next."),
        ("R", "{goal}: {what}. Endings hit the heart first, and the heart remembers."),
        ("R", "{goal}: {what}. When something {N} burned for ends, the fire looks for somewhere new."),
        ("G", "{goal}: {what}. Everything has its season, and this one has turned."),
        ("G", "{goal}: {what}. What ends feeds what grows next."),
    ],

    # loss: someone close died; time feels shorter.
    "loss": [
        ("", "Losing someone close makes a person feel how short time is."),
        ("", "After a loss, the years ahead seem fewer and more precious."),
        ("W", "Losing someone shows how little time there is to be there for the living."),
        ("W", "After a death, promises still unkept start to feel urgent."),
        ("U", "A loss reminds the mind of something it knew and avoided: time runs out."),
        ("U", "After a loss, a person starts measuring time more carefully."),
        ("B", "A loss makes plain that there is no time to waste on what does not matter."),
        ("B", "After losing someone, a person reaches harder for what they want, while they can."),
        ("R", "Loss makes the heart want to live everything now."),
        ("R", "After someone is gone, every day feels louder and shorter."),
        ("G", "A loss reminds a person that every life has its season."),
        ("G", "When someone close returns to the earth, the living feel the season turning."),
    ],

    # stress_up: stress rose a lot this week; the heart will be louder next time.
    "stress_up": [
        ("", "As stress rises, the heart grows louder and the head harder to hear."),
        ("", "Strain piles up, and a strained person acts more on impulse."),
        ("W", "Too much pressure makes even careful people break their own rules."),
        ("W", "When the load grows heavy, staying calm and fair gets harder."),
        ("U", "Stress narrows the mind: the next choice is more likely to come from the gut."),
        ("U", "A strained mind thinks less and reacts more."),
        ("B", "Pressure makes people grab what is closest, not what serves them best."),
        ("B", "Stress spends self-control that could have been saved for later."),
        ("R", "When the pressure builds, feelings take the wheel."),
        ("R", "Strain is fuel on the fire: the next spark catches faster."),
        ("G", "A storm bends every tree, and stress bends judgement the same way."),
        ("G", "Strain wears a person down, like wind wearing at a hillside."),
    ],

    # regret: the heart chose against the head, and it went wrong.
    "regret": [
        ("", "Choosing with the heart against the head, and losing, stays with a person."),
        ("", "When the heart wins the argument and then loses the gamble, the memory lingers."),
        ("W", "Going against one's better judgement, and paying for it, weighs on a person."),
        ("W", "A choice made against what {N} knew was wise leaves a lasting ache."),
        ("U", "A mistake the mind warned against is the one it keeps replaying."),
        ("U", "Overruling the head and failing leaves a lesson the head will not let go of."),
        ("B", "A loss {N} walked into with open eyes stings longest."),
        ("B", "Paying for a choice the head advised against is a cost that lingers."),
        ("R", "When the heart leads and it goes wrong, the ache outlasts the moment."),
        ("R", "Feelings that led {N} into trouble leave a bruise that takes time to fade."),
        ("G", "Some missteps stay with a person, like a stone in the shoe."),
        ("G", "Going against an inner warning leaves a mark that heals slowly."),
    ],

    # rite: a rite of passage into the next stage. Fills: {stage} (juvenile, young adult, adult, mature, elder).
    "rite": [
        ("", "A moment like this marks a passage: {N} has entered the {stage} years."),
        ("", "Some moments draw a line across a life, and {N} crosses into the {stage} years."),
        ("W", "A moment like this marks a new place in life: the {stage} years, with new duties."),
        ("W", "In the {stage} years, others hold {N} to a new standard."),
        ("U", "Life comes in stages, and this moment moves {N} into the {stage} years."),
        ("U", "A turning moment like this one sets {N} in the {stage} years, and changes what is expected."),
        ("B", "A moment like this resets the game: {N} enters the {stage} years, with new stakes."),
        ("B", "Stepping into the {stage} years brings new chances and new rivals."),
        ("R", "Something big happens, and suddenly {N} is in the {stage} years, like it or not."),
        ("R", "Big moments push a person across a line, and this one opens the {stage} years."),
        ("G", "As seasons turn, so do lives: {N} is in the {stage} years now."),
        ("G", "A moment like this turns a life's season: the {stage} years begin."),
    ],

    # rite_quiet: a passage into the next stage that no event marked (the window closed quietly). Fills: {stage}.
    "rite_quiet": [
        ("", "No one marked the day, but {N} has slipped quietly into the {stage} years."),
        ("", "Nothing announced it, yet {N} is in the {stage} years now."),
        ("W", "No ceremony marked it, but the {stage} years have begun for {N}, with all they ask."),
        ("W", "Without any rite to mark it, {N} has entered the {stage} years all the same."),
        ("U", "There is no moment to point to, but {N} is in the {stage} years now."),
        ("U", "Lives change by degrees as well as by events: {N} has reached the {stage} years."),
        ("B", "No one handed {N} the {stage} years; they have arrived anyway, with their own stakes."),
        ("B", "The {stage} years arrive for {N} with no fanfare, and the stakes change all the same."),
        ("R", "No big moment, no fuss: {N} simply wakes up in the {stage} years."),
        ("R", "It happens without anyone noticing, even {N}: the {stage} years are here."),
        ("G", "Like a season turning in the night, {N} has passed into the {stage} years."),
        ("G", "As a tree adds a ring unseen, {N} has grown into the {stage} years."),
    ],

    # turning_point: doubts piled up and the person is turning away from a color. Fills: {c}.
    "turning_point": [
        ("", "Doubts pile up until a person turns, and {N} is turning away from {c}."),
        ("", "Enough doubt, piled high enough, turns a person around."),
        ("W", "When a belief keeps failing a person, even a sworn commitment can give way."),
        ("W", "Doubts that gather long enough can turn even the most faithful."),
        ("U", "Enough evidence against a belief eventually changes the mind that held it."),
        ("U", "A mind can only explain away so much before it changes course."),
        ("B", "When a way of life stops paying, a person eventually cuts their losses."),
        ("B", "Doubt adds up like debt, and one day it is called in."),
        ("R", "When the heart stops believing in something, it lets go all at once."),
        ("R", "Feelings that sour for long enough flip, sudden and complete."),
        ("G", "Even a river changes course when enough stones pile up."),
        ("G", "Doubts gather like silt until the current finds a new channel."),
    ],

    # breakthrough: a want held back for long enough broke through.
    "breakthrough": [
        ("", "A want held down long enough breaks through in the end."),
        ("", "What a person keeps denying themselves does not go away; it waits."),
        ("W", "Denying a want for duty's sake works for a while, then it breaks loose."),
        ("W", "A need kept silent long enough finds its own voice."),
        ("U", "Pushing a desire down does not solve it; the pressure builds until it bursts."),
        ("U", "Pressure kept hidden still grows, and sooner or later it shows."),
        ("B", "Wanting something and never taking it builds a hunger that wins in the end."),
        ("B", "What a person truly wants, they reach for eventually, one way or another."),
        ("R", "Feelings shoved down too long come roaring back up."),
        ("R", "A fire banked too long flares up all at once."),
        ("G", "A seed under a stone still grows, and given time it splits the stone."),
        ("G", "Like water behind a dam, a held-back want finds its way through."),
    ],

    # closer_to: a rising or falling color is moving the person toward another identity. Fills: {guild}
    # (plain words, "principled and thoughtful", "passionate": always "becoming {guild}").
    "closer_to": [
        ("", "Step by step, {N} is closer to becoming {guild}."),
        ("", "These changes add up, and they carry {N} toward becoming {guild}."),
        ("W", "Each choice like this sets {N} further along the road to becoming {guild}."),
        ("W", "People notice how {N} acts, and see someone on the way to becoming {guild}."),
        ("W", "Bit by bit, {N}'s choices are adding up to becoming {guild}."),
        ("W", "The way {N} keeps choosing is leading toward becoming {guild}."),
        ("U", "The pattern is clear now: {N} is moving toward becoming {guild}."),
        ("U", "Add up the changes and the direction shows: toward becoming {guild}."),
        ("U", "If the trend holds, {N} is on course for becoming {guild}."),
        ("U", "The evidence of the past weeks points one way: toward becoming {guild}."),
        ("B", "Each move like this brings {N} closer to becoming {guild}."),
        ("B", "{N} is building toward becoming {guild}, whether or not anyone sees it yet."),
        ("B", "{N} is gaining ground toward becoming {guild}."),
        ("B", "Every gain like this puts {N} within closer reach of becoming {guild}."),
        ("R", "Without quite meaning to, {N} is heading toward becoming {guild}."),
        ("R", "{N} is changing fast, and the change points toward becoming {guild}."),
        ("R", "Something in {N} is shifting, and it is shifting toward becoming {guild}."),
        ("R", "{N} is turning into someone new: closer to becoming {guild}."),
        ("G", "Like a sapling finding its shape, {N} is growing toward becoming {guild}."),
        ("G", "Little by little, the way things are going, {N} is nearer to becoming {guild}."),
        ("G", "As a river finds its course, {N} is finding the way toward becoming {guild}."),
        ("G", "Season by season, {N} is ripening toward becoming {guild}."),
    ],

    # drifting_from (engine 15:00): a color falling away moves the person out of an identity. Fills: {lost} (the color's
    # adjective: principled, thoughtful, driven, passionate, grounded) and {guild} (what stays, plain words, or "no one
    # in particular"; always "being {guild}").
    "drifting_from": [
        ("", "{N} is letting go of being {lost}, and settling into being {guild}."),
        ("", "Bit by bit, {N} is less {lost} than before, and what stays is being {guild}."),
        ("W", "What once made {N} {lost} is fading, and the habits left are those of being {guild}."),
        ("W", "{N} has quietly stopped keeping faith with being {lost}; being {guild} is what remains."),
        ("W", "Others may see it before {N} does: less {lost} now, and settling into being {guild}."),
        ("W", "The old duty of being {lost} weighs less on {N} now, and being {guild} is what holds."),
        ("U", "The record shows it: {N} is less {lost} than a while ago, and settling into being {guild}."),
        ("U", "The trend runs the other way now: away from being {lost}, toward being {guild}."),
        ("U", "Add up the weeks and being {lost} falls away; what remains is being {guild}."),
        ("U", "Looked at closely, being {lost} explains less of {N} now than being {guild} does."),
        ("B", "{N} is spending less on being {lost} now, and keeping what pays: being {guild}."),
        ("B", "Being {lost} no longer earns {N} much, so {N} is letting it go and settling into being {guild}."),
        ("B", "{N} has stopped investing in being {lost}; being {guild} is what is left to build on."),
        ("B", "Less {lost} than before, {N} holds on to what still serves: being {guild}."),
        ("R", "The fire of being {lost} is cooling in {N}, and what is left is being {guild}."),
        ("R", "{N} can feel it slipping away: being {lost}. What remains is being {guild}."),
        ("R", "Something that made {N} {lost} has gone quiet, and {N} is settling into being {guild}."),
        ("R", "{N} is less {lost} these days, and not yet sure how being {guild} will feel."),
        ("G", "Like a season turning, being {lost} is passing out of {N}, and being {guild} is what stays."),
        ("G", "{N} is shedding being {lost} the way a tree sheds leaves, and settling into being {guild}."),
        ("G", "Year by year, being {lost} wears away in {N}, and what is left is being {guild}."),
        ("G", "The old root of being {lost} is loosening in {N}; being {guild} is what holds."),
    ],

    # ---------------------------------------------------------------- titles and perks (catalogue: earth_perks_titles.py)
    # {what} is the title's or perk's say. A title's say follows "is", "being" or "no longer" ("a nurse", "married",
    # "on the team", "out of work"). A perk's say reaches these lessons through explain.predicate, which puts "is" before
    # the noun says ("a landlord" becomes "is a landlord"), so a perk line puts {what} right after "{N} " or after
    # "someone who " ("It helped that {N} {what}.", "{N} is no longer someone who {what}.").

    # title_gain: a title of a commitment kind was gained (a job, a partner stage, a parent, a team, a faith role).
    "title_gain": [
        ("", "{N} is {what} now, and the role comes with its own ways and expectations."),
        ("", "Being {what} gives {N} a place, and the place asks things back."),
        ("W", "Being {what} comes with duties, and others will hold {N} to them."),
        ("W", "{N} is {what} now: people expect certain things, and {N} expects them too."),
        ("U", "Being {what} is a new role to learn, with its own rules and rewards."),
        ("U", "{N} is {what} now, and that changes what {N} needs to know."),
        ("B", "Being {what} brings standing, and a cost in time and freedom."),
        ("B", "{N} is {what} now: a new position, with new power and new demands."),
        ("R", "{N} is {what} now, and it already feels like part of who {N} is."),
        ("R", "Being {what} changes how {N} spends the days, and how those days feel."),
        ("G", "{N} is {what} now, and finds a place among others who are the same."),
        ("G", "Being {what} plants {N} in a new part of life, and it will shape what grows."),
    ],

    # title_loss: a title or status ended (a job, a partner stage, new in town, out of work). Fits losing a valued
    # role and leaving a hard status behind alike.
    "title_loss": [
        ("", "{N} is no longer {what}, and a part of how others saw {N} goes with it."),
        ("", "Being {what} is over for {N}, and the days take a new shape."),
        ("W", "{N} is no longer {what}, and the duties that came with it fall away."),
        ("W", "No longer {what}, {N} has to find a new place among others."),
        ("U", "{N} is no longer {what}; what that role taught stays, while the role does not."),
        ("U", "Now that {N} is no longer {what}, the days run on different rules."),
        ("B", "{N} is no longer {what}: what it gave and what it cost both end."),
        ("B", "Being {what} is behind {N} now, along with whatever it was worth."),
        ("R", "{N} is no longer {what}, and it takes a while to feel what that means."),
        ("R", "No longer {what}: something that filled {N}'s days has changed."),
        ("G", "{N} is no longer {what}; like a season, it has passed."),
        ("G", "A part of life closes: {N} is no longer {what}."),
    ],

    # status_gain: a status was gained (a graduate, retired, a homeowner, divorced, out of work, someone with a
    # record, a widow or widower). Neutral: it fits a hard status and a welcome one alike.
    "status_gain": [
        ("", "{N} is {what} now, and others see {N} a little differently."),
        ("", "Some facts about a life change how the world treats a person: {N} is {what}."),
        ("W", "Being {what} changes where {N} stands with others, and what they expect."),
        ("W", "Others take note: {N} is {what} now, and the rules around {N} shift."),
        ("U", "Being {what} changes the odds {N} meets, in ways that are not always obvious."),
        ("U", "{N} is {what} now, a fact that will quietly shape what comes next."),
        ("B", "Being {what} opens some doors and closes others, and {N} counts both."),
        ("B", "{N} is {what} now, and that changes what others will offer."),
        ("R", "{N} is {what} now, and it changes how a whole day feels."),
        ("R", "Being {what} is part of {N}'s story now, whatever anyone thinks of it."),
        ("G", "{N} is {what} now: a new season of life, with its own weather."),
        ("G", "Being {what} becomes part of the ground {N} stands on."),
    ],

    # perk_gain: a perk was gained or regained (a skill, a credential, standing, a bond, an asset). {what}: "can drive",
    # "has a car", "is a landlord", "has come into an inheritance".
    "perk_gain": [
        ("", "Now {N} {what}, and a few doors that were shut begin to open."),
        ("", "Something has changed: {N} {what}, and more is within reach."),
        ("W", "Now that {N} {what}, there is more {N} can offer others."),
        ("W", "{N} {what}, and that brings new things to answer for."),
        ("U", "Now {N} {what}, and every plan has one more thing to draw on."),
        ("U", "{N} {what}, which widens the range of things {N} can try."),
        ("B", "{N} {what}, and that is an advantage {N} did not have before."),
        ("B", "What a person holds decides what they can reach, and now {N} {what}."),
        ("R", "Now {N} {what}, and more of the world opens up."),
        ("R", "{N} {what}, and suddenly there are new doors to run through."),
        ("G", "{N} {what}, and something new has taken root in {N}'s life."),
        ("G", "A life grows by what it gathers, and now {N} {what}."),
    ],

    # perk_loss: a perk was lost or suspended. What it taught fades slowly; access goes at once. {what} as in perk_gain,
    # after "someone who " or in "it is no longer true that {N} {what}".
    "perk_loss": [
        ("", "It is no longer true that {N} {what}, and some doors close with that."),
        ("", "{N} has stopped being someone who {what}, for now or for good."),
        ("W", "{N} is no longer someone who {what}, and what others expect of {N} shifts too."),
        ("W", "No longer is {N} someone who {what}, and others will have to adjust."),
        ("U", "It is no longer true that {N} {what}; plans that leaned on it need rethinking."),
        ("U", "{N} is no longer someone who {what}, so there are fewer options to work with."),
        ("B", "{N} is no longer someone who {what}: an advantage gone, and a gap others can use."),
        ("B", "{N} can no longer count on being someone who {what}, and that costs."),
        ("R", "It stings: {N} is no longer someone who {what}."),
        ("R", "A door slams shut, for now at least: it is no longer true that {N} {what}."),
        ("G", "Things come and go like seasons: {N} is no longer someone who {what}."),
        ("G", "A root is cut: {N} has stopped being someone who {what}, though what it fed may hold."),
    ],

    # perk_helped: a perk gained this past year (a skill, standing or a bond) made an uncertain act work. Among the most
    # frequent lessons once titles and perks are on, so it has four lines a color.
    "perk_helped": [
        ("", "It helped that {N} {what}."),
        ("", "This went more easily because {N} {what}."),
        ("W", "Being ready is most of doing a thing well, and {N} {what}."),
        ("W", "Preparation done properly pays off: it counted that {N} {what}."),
        ("W", "Others trusted it would go well, since {N} {what}."),
        ("W", "A duty is easier to meet when {N} {what}."),
        ("U", "The odds shift for someone well equipped, and {N} {what}."),
        ("U", "Luck favours the prepared: it made a difference that {N} {what}."),
        ("U", "This turned from hard to manageable because {N} {what}."),
        ("U", "What a person brings to a moment shapes how it goes, and {N} {what}."),
        ("B", "Advantages add up, and this one paid off: {N} {what}."),
        ("B", "It pays to have what others lack, and {N} {what}."),
        ("B", "The edge that counted this time: {N} {what}."),
        ("B", "Because {N} {what}, {N} had the upper hand."),
        ("R", "It flowed, because {N} {what}."),
        ("R", "Doing it came easier, since {N} {what}."),
        ("R", "Nerve got {N} started, and the rest came because {N} {what}."),
        ("R", "Some battles are won before they start, and {N} {what}."),
        ("G", "What has grown in {N}'s life bears fruit now: {N} {what}."),
        ("G", "Something newly rooted held firm in the moment: {N} {what}."),
        ("G", "The people and skills around a person carry them further, and {N} {what}."),
        ("G", "What a person tends, tends them back: {N} {what}."),
    ],
}

# ================================================================ why the heart and the head want their option
# explain.before fills {heart_why} and {head_why} from the strongest driver behind each option, merging these over
# its own third-person phrases ({**HEART_WHY, **L["HEART_WHY"]}), so every key is given and none of the engine's
# leaks. First person, written to follow "because", under 9 words, and the same for every color. No fills: {goal}
# and {need} can be empty when these are drawn. Where the heart and the head share a driver, the phrases differ, so a
# torn line never gives the same reason twice.
#   motives, values: what the heart likes, what the head holds right; habit: the usual way; becoming: who the person
#   wants to be; odds: the better chance; needs: a need the option would meet; role: what a held commitment expects;
#   goals: a dream, passion or plan it serves; horizon: time felt short; exit: walking away from a commitment, against
#   what was put into it (for the head also wanting out: "because of all I have already put into this" fits both).
HEART_WHY = {
    "motives": "it feels right to me",
    "habit": "it is what I always do",
    "needs": "it gives me something I lack",
    "role": "people expect it of me",
    "goals": "it feeds what I have been reaching for",
    "horizon": "I can feel time running out",
    "exit": "walking away would cost me too much",
}
HEAD_WHY = {
    "values": "it is what I believe in",
    "becoming": "it is who I want to be",
    "odds": "I think it is the better bet",
    "needs": "it would fill what I am missing",
    "role": "it is what I am supposed to do",
    "goals": "it is a step toward what I want",
    "horizon": "I may not have much time left",
    "exit": "of all I have already put into this",
    "exit_out": "staying no longer fits who I am",   # engine 15:00: the head's reason for leaving
}
