# Checks: the inner voice and the lessons (earth_voice.py)

File: `earth_voice.py` (run from `chroma-library/drafts/`: `python3 check_voice.py > checks_voice.md`).

812 lines in 56 keys: 12 voice keys, 10 asides, 34 lessons; 16 why phrases (HEART_WHY 7, HEAD_WHY 9).

## Results

| Check | Result |
| --- | --- |
| 1 coverage | pass |
| 2 fills | pass |
| 3 length | pass |
| 4 duplicates | pass |
| 5 color words | pass |
| 6 person | pass |
| 7 style | pass |
| 8 numbers and verdicts | pass |
| 9 safety | pass |
| 10 why phrases | pass |
| 11 engine values | pass |

## Per key

Counts per color tag, the longest line in words (a fill counts as one word; limit in brackets), the longest once filled (with the sample fills, every why pair and every engine value tried in check 11), and the fills used.

| Group | Key | any | W | U | B | R | G | Total | Longest | With fills | Fills used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| voice | agree | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 14 (25) | 15 | {heart} |
| voice | heart_over_head | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 18 (25) | 24 | {head} {heart} {heart_why} |
| voice | head_over_heart | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 17 (25) | 22 | {head} {head_why} {heart} |
| voice | torn | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 17 (25) | 33 | {head} {head_why} {heart} {heart_why} |
| voice | want_but_doubt | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (25) | 19 | {x} |
| voice | dream_calls | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 18 (25) | 29 | {goal} {x} |
| voice | duty | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 18 (25) | 22 | {x} |
| voice | need_first | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (25) | 19 | {need} {x} |
| voice | habit | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (25) | 20 | {x} |
| voice | becoming | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 18 (25) | 22 | {x} |
| voice | time_short | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 16 (25) | 20 | {x} |
| voice | stuck | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (25) | 14 | none |
| aside | stressed | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (14) | 14 | {N} |
| aside | little_control | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 13 (14) | 13 | {N} |
| aside | disciplined | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 13 (14) | 13 | {N} |
| aside | undisciplined | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 13 (14) | 13 | {N} |
| aside | blind_spot | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (14) | 14 | {N} |
| aside | out_of_reach | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 13 (14) | 13 | {N} |
| aside | hopeful | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 12 (14) | 12 | {N} |
| aside | gloomy | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 10 (14) | 10 | {N} |
| aside | short_horizon | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 13 (14) | 13 | {N} |
| aside | lacks | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (14) | 15 | {N} {what} |
| lesson | practice | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 15 (18) | 15 | {N} {c} |
| lesson | hard_win | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 14 | none |
| lesson | self_control_up | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 16 | {N} |
| lesson | self_control_down | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 15 | {N} |
| lesson | surprise_teaches | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 15 (18) | 15 | {N} {c} {dir} |
| lesson | fail_own_ways | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 14 | {N} |
| lesson | defended | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 16 | {N} |
| lesson | habit | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 14 (18) | 14 | {N} |
| lesson | door | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 16 | {N} {c} |
| lesson | binding | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 14 | {N} |
| lesson | backfire | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 17 | {N} {kind} |
| lesson | need_met | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 15 | {N} {need} |
| lesson | duty_kept | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 17 (18) | 18 | {N} {kind} {kind_ref} |
| lesson | commit_start | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 17 | {N} {c} {kind} |
| lesson | commit_end | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 18 (18) | 18 | {N} {kind} {kind_ref} |
| lesson | goal_step | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 12 (18) | 19 | {N} {goal} |
| lesson | goal_setback | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 22 | {N} {goal} |
| lesson | sealed | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 22 | {N} {goal} |
| lesson | goal_end | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 24 | {N} {goal} {what} |
| lesson | loss | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 16 | none |
| lesson | stress_up | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 15 | none |
| lesson | regret | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 15 | {N} |
| lesson | rite | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 17 (18) | 18 | {N} {stage} |
| lesson | rite_quiet | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 17 | {N} {stage} |
| lesson | turning_point | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 14 | {N} {c} |
| lesson | breakthrough | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 14 (18) | 14 | none |
| lesson | closer_to | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 14 (18) | 19 | {N} {guild} |
| lesson | drifting_from | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 18 (18) | 23 | {N} {guild} {lost} |
| lesson | title_gain | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 17 | {N} {what} |
| lesson | title_loss | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 16 (18) | 16 | {N} {what} |
| lesson | status_gain | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 15 (18) | 16 | {N} {what} |
| lesson | perk_gain | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 13 (18) | 21 | {N} {what} |
| lesson | perk_loss | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 17 (18) | 25 | {N} {what} |
| lesson | perk_helped | 2 | 4 | 4 | 4 | 4 | 4 | 22 | 14 (18) | 22 | {N} {what} |

Sample fills: {N} = Ada; {heart} = shout back; {head} = {x} = walk away and cool off; {goal} = the dream of a working life (goal_step: the passion for freedom; goal_setback: the plan for doing right and freedom; sealed: the dream of freedom; goal_end: The dream of a working life); {need} = belonging; {c} = Red (commit_start: Red and Green); {dir} = more; {kind} = family (backfire: approval of others); {kind_ref} = family life; {stage} = young adult; {guild} = principled and thoughtful; {what} = not reached in time (title_gain: a nurse; title_loss: married; status_gain: a graduate; perk_gain: can drive; perk_loss: is a landlord; perk_helped: knows first aid; lacks: can drive); {heart_why} and {head_why}: the file's motives and values phrases.

## Why phrases

HEART_WHY and HEAD_WHY, as the inner voice says them after "because", with their length in words (under 9).

| Side | Driver | Phrase | Words |
| --- | --- | --- | --- |
| HEART_WHY | motives | it feels right to me | 5 |
| HEART_WHY | habit | it is what I always do | 6 |
| HEART_WHY | needs | it gives me something I lack | 6 |
| HEART_WHY | role | people expect it of me | 5 |
| HEART_WHY | goals | it feeds what I have been reaching for | 8 |
| HEART_WHY | horizon | I can feel time running out | 6 |
| HEART_WHY | exit | walking away would cost me too much | 7 |
| HEAD_WHY | values | it is what I believe in | 6 |
| HEAD_WHY | becoming | it is who I want to be | 7 |
| HEAD_WHY | odds | I think it is the better bet | 7 |
| HEAD_WHY | needs | it would fill what I am missing | 7 |
| HEAD_WHY | role | it is what I am supposed to do | 8 |
| HEAD_WHY | goals | it is a step toward what I want | 8 |
| HEAD_WHY | horizon | I may not have much time left | 7 |
| HEAD_WHY | exit | of all I have already put into this | 8 |
| HEAD_WHY | exit_out | staying no longer fits who I am | 7 |

Lines that give the reasons, filled with every phrase they can draw (explain._fill, both passes) and the sample options: words with a fill counted as one, and the shortest and longest filled.

| Key | Color | Line | Words | Filled | Pairs tried |
| --- | --- | --- | --- | --- | --- |
| heart_over_head | any | “{heart}” wins, because {heart_why}. I can still hear “{head}”, but only faintly. | 12 | 21-24 | 7 |
| head_over_heart | any | “{heart}” is tempting, but I'm choosing “{head}”, because {head_why}. | 9 | 19-21 | 9 |
| torn | any | Part of me wants “{heart}”, because {heart_why}. Part of me wants “{head}”, because {head_why}. | 14 | 28-33 | 63 |

## Engine values tried

90 goal names (plain_goal: dream, passion, plan of every domain, color and pair; the lessons also get its 3 fallbacks), 30 sealed dream names, 540 goal endings, 5 kinds (noun and reference), 31 plain identities, 5 stages, 80 perk says through explain.predicate (earth_perks_titles.py).

| Key | Values | Longest filled |
| --- | --- | --- |
| dream_calls | 90 | 29 |
| need_first | 5 | 19 |
| need_met | 5 | 15 |
| duty_kept | 5 | 18 |
| commit_start | 5 | 17 |
| commit_end | 5 | 18 |
| goal_step | 93 | 19 |
| goal_setback | 93 | 22 |
| sealed | 30 | 22 |
| goal_end | 540 | 24 |
| rite | 5 | 18 |
| rite_quiet | 5 | 17 |
| closer_to | 31 | 19 |
| drifting_from | 160 | 23 |
| perk_gain | 80 | 21 |
| perk_loss | 80 | 25 |
| perk_helped | 80 | 22 |

## Notes for the engine

- explain._pick pools the strongest color's lines with the "" lines (all 56 keys have both), so the any-color lines are in play: with two of them beside n lines for the color, each turns up about once in 2 + n draws. That is also how often a {c} line or a line that gives the reasons ({heart_why} / {head_why}, all "" variants) is seen.
- Perfect-tense says read well after "{N} " and "It helped that", less well once lost (perk_loss): "{N} is no longer someone who has finished school" (lost: never); "{N} is no longer someone who has inherited money" (lost: spent, or lost to 'a dispute over an inheritance').
- plain_goal's fallback for a goal with no mix, "the dream of something of their own", is third person; in the inner voice (dream_calls) it would read "I ... the dream of something of their own". "something of my own" there, or "something of one's own" everywhere, would fit.

## For review (not failures)

Lesson lines with right, wrong, good, bad, better or worse, to confirm each reads as an outcome or a comparison and not as a moral verdict:

- lesson word "right" (read as outcome or comparison, not as a verdict?): practice [R]: Getting it right once gives the heart the nerve to go again.
- lesson word "good" (read as outcome or comparison, not as a verdict?): practice [R]: What works feels good, and what feels good gets done again.
- lesson word "good" (read as outcome or comparison, not as a verdict?): practice [R]: What works feels good, and what feels good gets done again.
- lesson word "better" (read as outcome or comparison, not as a verdict?): self_control_up [B]: Each time {N} holds back, {N} gets better at holding back.
- lesson word "good" (read as outcome or comparison, not as a verdict?): self_control_down [R]: Giving in feels good now, and it loosens the reins a little more.
- lesson word "wrong" (read as outcome or comparison, not as a verdict?): surprise_teaches [U]: Being wrong about an outcome teaches more than being right.
- lesson word "right" (read as outcome or comparison, not as a verdict?): surprise_teaches [U]: Being wrong about an outcome teaches more than being right.
- lesson word "good" (read as outcome or comparison, not as a verdict?): surprise_teaches [R]: A shock, good or bad, rewires the gut a little.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): surprise_teaches [R]: A shock, good or bad, rewires the gut a little.
- lesson word "better" (read as outcome or comparison, not as a verdict?): fail_own_ways [B]: A costly failure sends a person shopping for a better strategy.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [W]: A way of life practised for long is sturdy against bad days.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [W]: When a way has held for years, a single failure reads as bad luck.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [U]: With enough experience behind a belief, a bad result gets explained away.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [R]: When something runs this deep in a person, a bad day makes them hold on tighter.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [G]: Old roots hold through a bad storm.
- lesson word "bad" (read as outcome or comparison, not as a verdict?): defended [G]: A way of life grown over many seasons is not uprooted by a bad season.
- lesson word "better" (read as outcome or comparison, not as a verdict?): need_met [R]: Getting {need} after going without it feels better than almost anything.
- lesson word "good" (read as outcome or comparison, not as a verdict?): goal_step [G]: Like a seedling in sun, {goal} grows with each good step.
- lesson word "worse" (read as outcome or comparison, not as a verdict?): goal_setback [any]: A setback shakes {goal}, and doubt makes the shaking worse.
- lesson word "worse" (read as outcome or comparison, not as a verdict?): goal_setback [U]: Setbacks make {goal} look less likely, and doubt makes it look worse still.
- lesson word "good" (read as outcome or comparison, not as a verdict?): sealed [G]: Grown in good soil, {goal} has become part of {N}: a passion.
- lesson word "better" (read as outcome or comparison, not as a verdict?): regret [W]: Going against one's better judgement, and paying for it, weighs on a person.
- lesson word "wrong" (read as outcome or comparison, not as a verdict?): regret [R]: When the heart leads and it goes wrong, the ache outlasts the moment.
- lesson word "good" (read as outcome or comparison, not as a verdict?): perk_loss [any]: {N} has stopped being someone who {what}, for now or for good.
