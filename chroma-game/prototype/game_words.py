"""The game layer's words and the life's closing texts: everything game.py held after class Game, moved out verbatim.
game.py and the Game mixins import from here."""
import numpy as np
import re
from game_base import (ADJ, C, COLORS, E, ES, ESP, GAME, IDENT_NAME, NOUN, STATUS_WORD, an, ident_meaning, ident_name,
    library_for)

# the peace reading (Emren's first goal idea, 2026-10-04: satisfaction and peace while staying true to one's mindset and
# skillset; kept as a reading, never a score, Emren 21:44). Rows: how well they lived; columns: how much it was their own.
LONG_SHOT = float(getattr(E, "DEFAULT", {}).get("long_shot", 0.10))   # the engine's own line: a title reached for when it works for fewer than 1 in 10 people

# Sex at birth, own gender, and the role the world expects (chroma-identity/for-the-game.md, Emren 10-07 01:57, N1d).
# The engine's fields (for-the-engine.md §6) are read when the pin has them; until then each one is "not found yet".
ENGINE_INTERSEX = "intersex_p" in getattr(E, "DEFAULT", {})
ROLE_STRICT0 = {"earth": 0.3, "tribal": 0.7, "magic": 0.5}     # the engine's setting defaults (for-the-engine.md §3)
ACCEPT0 = {"earth": 0.5, "tribal": 0.3, "magic": 0.5}          # accept_trans defaults (§4)
# a memory coming back (engine v10's recall), in the story's words: {when} "at 14" or "as a child", {what} the old act
RECALL_LINES = dict(
    scar=["An old wound opens: {when}, {{N}} chose to {what}, and it went badly. Not that again.",
          "{{N}} has been here before: {when}, they chose to {what}, and it still stings.",
          "This comes too close to an old hurt: {when}, {{N}} chose to {what}, and it went wrong."],
    good=["A good memory comes back: {when}, {{N}} chose to {what}, and it worked.",
          "{{N}} has done this before: {when}, they chose to {what}, and it went well."],
    bad=["{{N}} remembers: {when}, they chose to {what}, and it did not work.",
         "{{N}} has been here before: {when}, they chose to {what}, and it went wrong."])
RECALL_GAP = 3           # years between two told memories (scars apart); the engine recalls about 2.7 a year
RECALL_MIN = 0.9         # how strong a memory must come back to be told (the engine's floor is epi_recall .7)
TEMPER_AGAIN = 5 * 52    # item 6: weeks before the temperament line names the same event again
# item 6: a commitment's change as the event the temperament line names (TEMPER_CAUSE {event}), by what and kind, else by
# what alone ({kind} filled); "inherited" names nothing
TIED_COMMIT = dict(start=dict(partner="settling down with someone", career="starting out in their work",
                              community="joining their community", faith="taking up their faith", children="becoming a parent"),
                   left=dict(partner="the breakup", career="walking away from their work",
                             community="leaving their community", faith="leaving their faith"))
TIED_COMMIT_ANY = {"left": "walking away from their {kind}", "lost job": "losing their job", "retired": "retiring",
                   "widowed": "losing their partner", "moved": "changing employer"}
WORLD_ON = True          # the engine's outer world in Earth lives, where the pin has it (False: the world of v21)
# the engine's own names for the identity values in the week's state, where they differ from for-the-engine.md §6:
# key -> (local name, column or None)
ID_LOCAL = {"found_gender": ("found_id", 0), "found_attr": ("found_id", 1), "found_ace": ("found_id", 2),
            "found_intersex": ("found_id", 3), "role_strict": ("RS0", None), "accept_trans": ("AT0", None),
            "role_fit": ("rfit_avg", None), "named": ("named_g", None), "came_out": ("came_o", None)}
TWO_WORD = {"wife or husband": ("wife", "husband", "spouse"), "girlfriend or boyfriend": ("girlfriend", "boyfriend", "partner"),
            "mother or father": ("mother", "father", "parent"), "lead actor or actress": ("lead actress", "lead actor", "lead actor")}
TWO_RE = re.compile(r"\b(" + "|".join(map(re.escape, TWO_WORD)) + r")\b")
PRESSURE = {"earth": ["People talk.", "The family goes quiet at dinner.", "A few looks follow {N} for a while."],
            "tribal": ["The elders say nothing, and it is loud.", "At the fire, the talk stops when {N} sits down.",
                       "The old women watch {N} longer than they need to."],
            "magic": ["The lane talks about it behind its hands.", "An aunt makes the sign against ill luck when {N} passes.",
                      "At the hall, the greetings come a little late."]}
DRAWN = {0: "{o}", 1: "mostly {o}", 2: "both men and women", 3: "mostly {s}", 4: "{s}"}


def strict_word(v):
    return "loose" if v < 0.4 else "firm" if v < 0.65 else "strict"


def fit_word(v):
    return "it fits them" if v >= 0.8 else "it chafes" if v >= 0.5 else "it weighs on them"


def age_word(g, age):
    """'a girl', 'a young man', 'a person'... for g in f, m, x (nonbinary: a child, a young person, a person)."""
    if age < 13:
        return {"f": "a girl", "m": "a boy"}.get(g, "a child")
    if age < 18:
        return {"f": "a young woman", "m": "a young man"}.get(g, "a young person")
    return {"f": "a woman", "m": "a man"}.get(g, "a person")
LONG_SHOT_KINDS = ("career", "community", "faith")   # by odds alone, only titles one strives for; a pack's marked long shot, any
DEATH_FROM = 16          # the character's own death is possible from this age (or the start age, if later); a game default
DEATH_LIFE_YEARS = 112   # v22.5 F2: with the engine's death_life on, death comes from the life, so a life may run on to about 100
# v22.5 F1 and F2: the body's and the mind's own turns and a last decline (engine body, mind and death_life switches; nothing
# shows with them off), the game's words until the Library has its own. Level 0 is always told, 1 at normal detail, 2 every week
BODY_SAY = {("condition", "begins"): (0, "{name} learns they will live with {what}."),
            ("condition", "begins young"): (0, "{name} is found to have {what}."),
            ("condition", "eases"): (1, "{name}'s {what} eases as they grow."),
            ("serious", "begins"): (0, "{name} is diagnosed with {what}."),
            ("serious", "begins stroke"): (0, "{name} has a stroke."),
            ("serious", "through it"): (0, "{name} comes through {the}, though it has taken something from them."),
            ("injury", "hurt"): (2, "{name} is hurt and takes weeks to mend."),
            ("low season", "begins"): (1, "A low season settles over {name}."),
            ("low season", "lifts"): (1, "The low season lifts from {name}."),
            ("anxiety", "begins"): (1, "Worry starts to follow {name} through the days."),
            ("anxiety", "lifts"): (1, "{name}'s worry eases."),
            ("numbing", "begins"): (1, "{name} starts numbing the evenings: a drink, a screen, anything not to feel it."),
            ("numbing", "lifts"): (1, "{name} stops reaching for the numbing.")}
BODY_WHAT = {"heart condition": "a heart condition", "heart disease": "heart disease"}
BODY_THE = {"cancer": "the cancer", "heart disease": "the heart trouble", "a stroke": "the stroke", "lung disease": "the lung disease"}
DECLINE_SAY = dict(old="{name} grows frail; the last season of their life has begun.",
                   serious="{name}'s illness turns; now it is months, not years.",
                   condition="{name}'s body begins to fail them, and this time it does not recover.")
STAGE_WORD = dict(child="childhood", juvenile="youth", young_adult="young adulthood", adult="adulthood", mature="maturity", elder="old age")
SEASON_STEP = {1: "the crossing", 2: "the in-between", 3: "settling in"}
# item 3, the voice in their head (chroma-ideas/voice-mechanics.md): its record per life (n moments decided, steer the
# pushes, d the summed colors pushed (picked minus their own), ax the same on the five questions, rel summed reluctance,
# dw what the pushes moved), and the ten sides of the five questions that name it (engine AXES: + side, - side)
VOICE_SIDES = [("group vs individual", "people", "themselves"), ("security vs freedom", "safety", "freedom"),
               ("head vs heart", "head", "heart"), ("destiny vs free will", "meant", "will"), ("nature vs nurture", "already", "make")]
VOICE_AX = np.array([E.AXES[a] for a, _, _ in VOICE_SIDES], float)
VOICE_MIN = 5            # pushes before the voice has a name of its own
VOICE_HALF = 156         # weeks for a push's move to count half in what the voice did (life pulls them back)
VOICE_FADE = 0.5 ** (1 / VOICE_HALF)
VOICE_RECALL = 104       # weeks: a push the same way within two years is remembered in the answer


def art(say):
    """A title or name with its article: 'a judge', 'the first in the family at university', 'an Explorer'."""
    if say.startswith(("The ", "A ", "An ")):        # mid-sentence: "became the Guardian"
        return say[0].lower() + say[1:]
    return say if not say or re.match(r"(a|an|the|one) ", say) else an(say)


def voice_empty():
    return dict(n=0, steer=0, d=[0.0] * C, ax=[0.0] * len(VOICE_SIDES), rel=0.0, dw=[0.0] * C)


def voice_share(vdw, total):
    """How much of a change of colors was the voice's doing: its pushes' part along the change, 0 to 1."""
    tt = float(np.dot(total, total))
    return float(np.clip(np.dot(vdw, total) / tt, 0.0, 1.0)) if tt > 1e-6 else 0.0


# 5.5 (item 4): names from color dynamics. The name is the identity of the last NAME_WEEKS of colors; "becoming" a rise
# (or, for a color of the name, a fall) of BECOMING over BECOMING_YEARS yearly readings, said after the name
NAME_WEEKS = 208
BECOMING, BECOMING_YEARS = 0.08, 3
GROW_WORDS = dict(W="taking duty to heart", U="growing curious", B="growing ambitious", R="growing passionate",
                  G="putting down roots")
FADE_WORDS = dict(W="loosening their hold on order", U="losing some of their curiosity", B="letting go of some ambition",
                  R="cooling", G="pulling up some roots")
# item 11 (world-in-life.md): WL1's bands, (told from, big from) by channel (the Library's proposal); the engine's kinds as
# the Library names them; a kind's own words for a cause with no name; weeks before the same kind of line again
# (measured in a Modern Earth life: housing moves money by about .011 most years, a crime wave safety by .012 to .015,
# so the everyday ripples stay quiet and a disaster or a real price shock is told)
WFX_BAND = dict(money=(0.015, 0.03), freedom=(0.015, 0.03), time=(0.015, 0.03), health=(0.015, 0.03), ties=(0.015, 0.03),
                safety=(0.02, 0.06), risk=(0.2, 0.5), home=(0.2, 0.5))
WFX_BAND["close person"] = (0.2, 0.5)
WFX_KIND_LIB = dict(crime="crime wave", prices_work="prices", rec_hours="recession", disaster_time="disaster")   # WL2 (PR #62): its kinds told as the Library's
# the world's record entries behind an effect (world_link CAUSE_REC: domain, kind), as the hover names them
WFX_CAUSE = {"recession declared": "the recession", "recession over": "the end of the recession",
             "world recession": "the world recession", "war comes home": "the war", "war begins": "the war",
             "war ends": "the end of the war", "welfare raised": "higher welfare", "budget cut": "the budget cuts",
             "government falls": "the fall of the government", "right gained": "a new right", "law changed": "a new law",
             "regime changes": "the change of regime", "crime wave": "the crime wave in their town", "disaster": "the disaster",
             "pandemic": "the pandemic", "price shock": "the price shock", "arrives": "new technology",
             "spreads": "technology spreading", "era begins": "the new era"}
WFX_KIND = dict(prices="rising prices", housing="the housing market", welfare="the welfare rules", rights="the law on rights",
                crime="the crime wave", war="the war", disaster="the disaster", unemployment="the jobs market",
                illness="the illness going round", pandemic="the pandemic", recession="the recession",
                prices_work="prices eating into wages", rec_hours="the recession's shorter hours",
                disaster_time="the disaster in their town")
WFX_AGAIN = 52

# spheres phase 4 (PR #84, sph_levers): a lever act on their town's sphere, told as theirs. The Library has no words for
# levers yet (earth_story.py, earth_spheres.py), so these are the game's: the act by lever, {where} it landed (their
# place in that sphere, by the Library's haunt names as "their places" shows them, else the town's sphere), and what came
# of it by the engine's word (moved, backfired, fired <event>, moved <state>, none); came: the panel's short words, with
# the Library's name for an event set off; their standing there is the Library's rung word (earth_spheres.RUNG)
SPH_LEVER = dict(
    act=dict(exit="{N} turns their back on {where}", voice="{N} speaks up for change in {where}", loyalty="{N} stands by {where}",
             neglect="{N} lets {where} go untended", subvert="{N} works the system in {where}",
             found="{N} sets up something new in {where}", fund="{N} puts money into {where}", lead="{N} takes the lead in {where}",
             office="{N} uses their office on {where}"),
    sphere=dict(rule="the town's rule and law", gather="the town's gatherings", arts="the town's arts", faith="the town's faith",
                care="the town's care for the sick", learn="the town's learning", prod="the town's work", comm="the town's trade",
                prot="the town's safety"),
    moved=dict(voice=", and it shifts a little their way.", subvert=", and it bends a little their way.",
               exit=", and it drifts further from their ways without them.", neglect=", and it drifts along with the rest of the town.",
               loyalty=", and it holds to its ways a while longer.", found=", and a place in town takes on their ways.",
               fund=", and their money pulls it their way for years.", lead=", and it shifts a little their way."),
    backfired=", but it backfires and turns against their ways.", none=", and nothing comes of it.",
    fired=", and it brings {what} to town.", state=", and it makes for {what}.",
    # the office's events and states (sphere_data.LEVER_OFFICE), as what the act brings
    what=dict(rights_narrowed="narrower rights", charter_won="a charter of its own", the_count="a count of people and land",
              curfew="a curfew", meeting_place_opens="a new meeting place", common_ground="a square open to everyone",
              work_banned="a ban on a work of art", school_of_arts="a school of the arts", faith_outlawed="a ban on a faith",
              tolerance="peace between the faiths", temple_raised="a new house of worship", house_of_care_opens="a new house of care",
              care_for_all="care for all", censors_close="the censors", first_school="a first school", schools_for_all="free schooling for all",
              venture_founded="a new venture", usury_banned="a ban on usury", market_granted="a market", bank_opens="a bank",
              crackdown="a crackdown", watch_founded="a new watch", **{"arts.licence": "licences for the arts", "care.reach": "less care within reach",
              "prod.room": "less room for new work", "prod.skill": "more skill in the trades", "prot.hired_share": "more guards for hire"}),
    came=dict(moved="it moved", backfired="it backfired", fired="it set something off", state="it changed the rules", none="nothing came of it"),
)
LEVER_AGAIN = 52         # weeks before the same lever on the same sphere is told again at the normal level

# far-off events through ties (PR #95, far_ties): a close tie's news from the town they live in (the engine's far_event
# and line are Outer world's words, sphere_data.FAR), a tie taken into the household and their leaving, and the words for
# a far want on the circle. The far moments themselves are the Library's (earth-far-ties.lib, PR #90), with their slots
# {their_town} and {far_event} filled from the engine's word on the call
FAR_SAY = dict(
    away=dict(good="Good news from {town}, where {who} lives: {event}.", hard="Hard news from {town}, where {who} lives: {event}.",
              mixed="Mixed news from {town}, where {who} lives: {event}."),
    here=dict(good="In town, {event}, and it goes well for {who}.", hard="In town, {event}, and it hits {who} hard.",
              mixed="In town, {event}, and for {who} it cuts both ways."),
    took="{who} comes to live with {N} for a while.", back="{who} goes back home{town} after their time in {Ns} home.",
    stayed="After their time in {Ns} home, {who} finds a place of their own in town.",
    want=dict(far_hard="help after hard news in their town", far_good="to share good news from their town",
              far_mixed="to talk over news from their town, good and hard"),
)
FAR_AGAIN = 26           # weeks before the same tie's far news is told again at the normal level

# v22.4's social mechanics on the page (chroma-ideas/social-mechanics.md S1, S3 to S7; the Engine's fields in
# chroma-engine/notes/v22.4-fields/, the Library's words in earth_spheres.py). FAIR_SIDE: a sphere's felt fairness under the
# first reads unfair on its hover (.5 is even), over the second fair (the engine's own line for loyalty and voice); between,
# no line. TALK_AGAIN: weeks between two go-betweens' words at the normal level (a life hears one for most acts, about ten
# a year; the same good word from the same place waits three times as long); TALK_QUIET: the same for the detailed story.
# LEAD_COLOUR: the colour of each way to lead, W U B R G (the ways' words, legitimacy words and the places a post leads
# are the Library's: earth_spheres LEAD_WAY, LEAD_LEGIT, LEAD_PLACE, SETTING_PLACE, SPHERE_PLACE). SEEN_ROW: S6's row
# shows on an option on a path (a title it gives or aims at) for every word, on one in a colour way only when they saw
# that way go wrong (nearly every life has seen each way done, the Engine's own finding); SEEN_MARK: the row's short word
# (the page marks none only on the hover)
FAIR_SIDE = (0.5, 0.65)
TALK_AGAIN, TALK_QUIET = 52, 8
LEAD_COLOUR = dict(rules="W", knowing="U", favours="B", inspiring="R", custom="G")
SEEN_ROW = dict(path=("seen", "none", "wrong", "far"), way=("wrong",))
SEEN_MARK = dict(seen="seen it done", wrong="saw it go wrong", far="seen it, far off", none="never seen it done")


def lead_words(name):
    """S7: one of the Library's tables for ways to lead (earth_spheres), empty in a pin from before it had them."""
    return getattr(ESP, name, None) or {}


def cap_first(s):
    return s[:1].upper() + s[1:] if s else s


# F5 (item 4): a pick's thread is told on a later moment that follows from it, within THREAD_YEARS, once per THREAD_AGAIN weeks
THREAD_YEARS, THREAD_AGAIN = 12, 156
THREAD_COMMIT = dict(career="their working life took a new road", partner="a life together began",
                     children="a family began", community="they joined a community", faith="a faith became theirs")
THREAD_GOAL = dict(plan="they set out on a plan", dream="a dream took hold", passion="a passion took hold")
WORLD_AGAIN = 104        # G2 (B package): weeks before the same world line (kind and words) is told again

NEED_HINT = ("{N}'s sense of {need} is running thin. Needs fade a little every week unless something feeds them: acts that "
             "work, the people and roles in their life, money, health and free time. A need that is lacking pulls satisfaction "
             "down, and meeting it lifts satisfaction most. Options show which needs they would meet.")

PEACE_WORDS = {
    ("high", "high"): "At peace: a good life, and their own.",
    ("high", "mid"): "Content, and mostly themselves.",
    ("high", "low"): "Content, though much of it was not of their choosing.",
    ("mid", "high"): "True to themselves, with an ordinary share of peace.",
    ("mid", "mid"): "An ordinary peace: some of it earned, some of it given.",
    ("mid", "low"): "Getting by, in a life often steered from outside.",
    ("low", "high"): "True to themselves, at a cost.",
    ("low", "mid"): "A hard road, only partly their own.",
    ("low", "low"): "Restless to the end, and seldom their own.",
}
HOME_UNTIL = 18           # F5: the times are told through the home while young and under this age
INTEG_PUSHES = 10        # F13: integrity is read over the pushes, with at least this many in the divisor
PEACE_BANDS = dict(well=(0.65, 0.55), own=(0.9, 0.8))       # high from, mid from; test/peace_bands.py on the final pin
# (2026-10-06, 36 lives: well .49-.77, a third high and a sixth low; own .94-.99 when the player never pushes, .88-.94 at
# 30% pushed, .76-.88 at 70%)


def odds_words(p):
    """Long odds in words: '3 in 100', 'fewer than 1 in 100'."""
    if p is None:
        return "long odds"
    n = int(round(p * 100))
    return f"{n} in 100" if n >= 1 else "fewer than 1 in 100"


TRY_WORDS = {2: "a second time", 3: "a third time", 4: "a fourth time", 5: "a fifth time"}


def long_shot_words(x):
    """One long shot, for the review and the resolution: the climb (the rung they stood on, which try this was), the
    reach, the odds, and what came of it (Emren 09:18: commitment and repeated tries, never one jump from nothing)."""
    at = f"At {int(x['age'])}, " if x.get("age") is not None else ""
    rung = x.get("rung")
    if rung:
        yrs = rung.get("years") or 0
        noun = re.match(r"(a|an|the|one) ", rung["say"])       # "as an amateur actor", but "standing for the council"
        at += f"after {'a year' if yrs <= 1 else f'{yrs} years'} {'as ' if noun else ''}{rung['say']}, "
    tries = x.get("tries", 1)
    again = f" {TRY_WORDS.get(tries, 'once more')}" if tries > 1 else ""
    odds = "long odds" if x["odds"] is None else "odds of " + odds_words(x["odds"])
    aim = x["say"] if re.match(r"(a|an|the|one) ", x["say"]) else an(x["name"])
    line = f"{at}they tried{again} to become {aim} against {odds}"
    if x["made"]:
        return cap1(line + ", and made it.")
    return cap1(line + (", and missed again. The trying was theirs." if tries > 1 else ", and missed. The trying was theirs."))


def cap1(s):
    return s[:1].upper() + s[1:]


# The end of a life told as one paragraph (implementation list item 1, Emren 10-08 21:44: "with color history throughout
# life and the biggest, rare events-content history. like a paragraph"). The story of the colors through the years (the
# identities held, when and why they turned), then the biggest and rarest things the life met, ending with the question
# of the colors it lived longest. Built-in words for now; the wording is the Library's to replace.
HELD_MIN = 3             # years an identity must hold to count as a stage of the life (shorter spells are passing moods)
TURNS_TOLD = 3           # at most this many turns are told: the first identity, the longest-held ones, and the last
WHY_YEARS = 2            # a turn's cause is looked for in this many years before it
RARE_TOLD = 2            # how many of the biggest and rarest things are named
RARE_SHARE = 0.10        # rare, as the Book says it: under 1 life in 10 meets it
# Stakes on the card: what a way's mark does to the people side, said about now (named when the moment has the person;
# the second form when it does not). A mark is left whether the way works or not, so it is for good either way
STAKE_MARK = {"made a friend": ("makes a friend of {p}", "makes a new friend"),
              "made an enemy": ("makes an enemy of {p}", "makes an enemy"),
              "helped someone in need": ("helps {p} when it counts", "helps someone in need"),
              "refused someone in need": ("turns {p} away", "turns away someone in need"),
              "kept your word": ("keeps their word to {p}", "keeps their word"),
              "broke your word": ("breaks their word to {p}", "breaks their word"),
              "took them in": ("takes {p} in", "takes someone in")}
STAKE_NEAR = ("friend", "friend2", "partner", "sibling", "parent", "child", "grandparent", "elder")   # already close: a
# friend made is someone new, so these are never named for it
STAKE_KIND = ("made an enemy", "refused someone in need", "broke your word")   # never said of a child in the scene
STAKE_SOON = re.compile(r"\b(later|come back|comes back|came back|return|returns)\b")   # a backfire told this way could read
# as a pick coming back, so the card leaves it out


def stake_risk(p):
    """The Library's death_if_fails (the share of an act's failures that end the life) in plain words."""
    return ("a slim risk to their life" if p <= 0.002 else "a small risk to their life" if p <= 0.005
            else "a real risk to their life" if p < 0.02 else "a grave risk to their life")
TITLE_KINDS = ("career", "community", "faith", "status")   # the titles that can turn a life or count among its rarest things
DEATH_WORD = dict(parent="a parent", sibling="a sibling", friend="a friend", grandparent="a grandparent",
                  partner="their partner", child="a child")
DEATH_WEIGHT = dict(child=0, partner=1, parent=2, sibling=3, friend=4, grandparent=5)   # the nearer, the likelier the cause


def _why(met, at, share, say_of):
    """What most likely turned them at age at: a death close by, a title taken up, or the rarest of the world's readings,
    in the WHY_YEARS before it. None when nothing stands out."""
    near = [m for m in met if at - WHY_YEARS <= m[0] <= at]
    deaths = sorted((m for m in near if m[1] == "death"), key=lambda m: DEATH_WEIGHT.get(m[2], 9))
    if deaths and deaths[0][2] != "grandparent":
        return f"the death of {DEATH_WORD.get(deaths[0][2], 'someone close')}"
    roles = [m for m in near if m[1] == "role" and (share("role", m[2]) or 1) < 0.5]
    if roles:
        return _becoming(say_of(roles[-1][2]))
    reads = sorted((m for m in near if m[1] == "read" and share("read", m[2]) is not None and share("read", m[2]) < 0.5),
                   key=lambda m: share("read", m[2]))
    if reads:
        return _quoted(reads[0][2])
    if deaths:                                       # a grandparent's death is common: it counts when nothing else does
        return f"the death of {DEATH_WORD['grandparent']}"
    return None


def _becoming(say):
    """'becoming a baker', 'becoming the first in the family at university', 'being out of work', 'keeping a record'."""
    if re.match(r"\w+ing\b", say):
        return say
    v = re.match(r"(works|directs|runs|leads|keeps|teaches|sits|holds) ", say)    # 'works the polling station'
    if v:
        w = v.group(1)[:-1]
        w = {"teache": "teach", "run": "runn", "sit": "sitt"}.get(w, w)
        return w + "ing" + say[len(v.group(1)):]
    return ("becoming " if re.match(r"(a|an|the|one) ", say) else "being ") + say


def _quoted(name):
    return f"\u201c{name}\u201d"


def _ident_a(lbl):
    """'a Striver', but 'one of the Rooted' for the names that are not nouns."""
    nm = ident_name(lbl)
    nm = nm[4:] if nm.startswith("The ") else nm
    return f"one of the {nm}" if nm.endswith("ed") or nm in ("Enduring", "Whole") else an(nm)


def life_names(h):
    """F13: who they were, year by year, as the chapter headings named them (the settled identity, _yearly's history
    "name"); a life from before it was kept reads the yearly identity instead."""
    if h.get("name"):
        return [l for _, l, *_ in h["name"] if l]
    return [l for _, l in h.get("label", []) if l]


def _episodes(label):
    """The life's identities as episodes (Emren 10-09: flow, zigzags, identities held side by side): each is
    [kind, labels, from age, to age], kind "steady" (one identity held HELD_MIN years or more) or "swing" (two identities
    taking turns, three changes or more within one stretch). Shorter spells between are passing moods, left out."""
    runs = []
    for i, (a, l) in enumerate(label):
        if not l:
            continue
        end = label[i + 1][0] if i + 1 < len(label) else a + 1
        if runs and runs[-1][0] == l:
            runs[-1][2] = end
        else:
            runs.append([l, a, end])
    eps, i = [], 0
    while i < len(runs):
        pair, j = {runs[i][0]}, i
        while j + 1 < len(runs) and len(pair | {runs[j + 1][0]}) <= 2:
            j += 1; pair.add(runs[j][0])
        if j - i >= 3 and len(pair) == 2 and runs[j][2] - runs[i][1] >= 2 * HELD_MIN:
            order = list(dict.fromkeys(r[0] for r in runs[i:j + 1]))
            eps.append(["swing", order, runs[i][1], runs[j][2]]); i = j + 1
        elif runs[i][2] - runs[i][1] >= HELD_MIN:
            eps.append(["steady", [runs[i][0]], runs[i][1], runs[i][2]]); i += 1
        else:
            i += 1
    out = []
    for e in eps:                                    # the same identity again after a passing mood: one episode
        if out and out[-1][0] == e[0] == "steady" and out[-1][1] == e[1]:
            out[-1][3] = e[3]
        else:
            out.append(e)
    return out or ([["steady", [runs[-1][0]], runs[-1][1], runs[-1][2]]] if runs else [])


def _adjs(cols):
    """'curious and ambitious' for UB; colors as the story's adjectives."""
    a_ = [ADJ[c] for c in COLORS if c in cols]
    return a_[0] if len(a_) == 1 else ", ".join(a_[:-1]) + " and " + a_[-1] if a_ else "unsettled"


def _nouns(cols):
    n_ = [NOUN[c] for c in COLORS if c in cols]
    return n_[0] if len(n_) == 1 else ", ".join(n_[:-1]) + " and " + n_[-1]


def _when(a):
    a = int(a)
    return ("in childhood" if a < 10 else "in their teens" if a < 20 else f"in their {a // 10 * 10}s" if a < 90
            else "at the very end")


def _drift(ws, a0, a1, b0, b1):
    """What moved between two stretches of the life: the color that rose most and the one that fell most."""
    pick = lambda x, y: [w for a, w in ws if x <= a < y]
    p, q = pick(a0, a1), pick(b0, b1)
    if not p or not q:
        return None, None
    d = np.mean(np.asarray(q, float), axis=0) - np.mean(np.asarray(p, float), axis=0)
    up, dn = int(np.argmax(d)), int(np.argmin(d))
    return (COLORS[up] if d[up] > 0.02 else None), (COLORS[dn] if d[dn] < -0.02 else None)


def _move(up, dn, k):
    """A drift in words, in one of a few shapes."""
    if up and dn:
        return [f"their {NOUN[up]} grew as their {NOUN[dn]} faded", f"{NOUN[up]} crowded out {NOUN[dn]}",
                f"they grew more {ADJ[up]} and less {ADJ[dn]}"][k % 3]
    if up:
        return [f"their {NOUN[up]} grew", f"they grew more {ADJ[up]}"][k % 2]
    if dn:
        return [f"their {NOUN[dn]} faded", f"they grew less {ADJ[dn]}"][k % 2]
    return ""


def _thing(k, n_, say_of, i):
    """A rare thing the life met, told in passing: 'against the odds they became an actor', or a moment few lives hold."""
    if k == "long":
        return f"against the odds they became {n_}"
    if k == "role":
        say = say_of(n_)
        return (f"they became {say}" if re.match(r"(a|an|the|one) ", say) else
                f"they took to {say}" if re.match(r"\w+ing\b", say) else f"they found themselves {say}")
    if k == "mark":
        return f"they {n_}"
    return [f"came a moment few people live: {_quoted(n_)}", f"something few lives hold: {_quoted(n_)}",
            f"a moment that stayed with them, {_quoted(n_)}"][i % 3]


def _closing(h, review):
    """The life's satisfaction and peace over the years, said once at the end (Emren 10-09: close on the character's
    history overall)."""
    c = dict(h.get("content", [])); p = dict(h.get("peace", []))
    if len(c) < 4:
        return ""
    def by_decade(d_):
        dec = {}
        for a, v in d_.items():
            if a >= 20:                              # adult decades: the teens are hard in almost every life
                dec.setdefault(int(a) // 10 * 10, []).append(v)
        return {k: float(np.mean(v)) for k, v in dec.items() if len(v) >= 3}
    S = []
    dc, dp = by_decade(c), by_decade(p)
    if len(dc) >= 2:
        best, worst = max(dc, key=dc.get), min(dc, key=dc.get)
        if dc[best] - dc[worst] >= 0.08:
            S.append(f"They were most content {_when(best)} and least {_when(worst)}")
        else:
            S.append("Their contentment ran level through the decades, never far from where it began")
    if len(dp) >= 2:
        calm, storm = max(dp, key=dp.get), min(dp, key=dp.get)
        if dp[calm] - dp[storm] < 0.08:
            S[-1] += "; their peace held steady."
        elif S and calm == max(dc, key=dc.get):
            S[-1] += f"; {_when(calm)[3:] if _when(calm).startswith('in ') else _when(calm)} were also their most peaceful years."
        else:
            S[-1] += f"; peace was deepest {_when(calm)}, thinnest {_when(storm)}."
    f = review.get("forced", 0); integ = review.get("integrity", 1.0)
    S.append("Every choice in it was their own." if not f else "Most of it was of their own choosing." if integ >= 0.9
             else "Much of it was steered from outside, and they felt it.")
    return " ".join(S)


# The life as a bard's song (Emren 10-09: "more poetic and epic, like Homer or Ovid's Metamorphoses ... a song now in
# an ancient Greek tavern, sung by bards"; and: "more variety, life to life ... not random, related to outcomes,
# preferences, moments and choices of the player, connected to the five color stat map"). Every choice of words below is
# read from the life: the colors it led with, the colors that rose, fell or flickered, the shape of its contentment, the
# ways it acted at the player's moments and how they turned out, the player's pushes, its losses and long shots.
# The words are the Library's (earth_story.py SONG, SONG_WORLD and MARK_SAY, pinned in engine_pin/), key for key with
# the game's own below, which stay for a pin without them. Keys, fills and selectors: chroma-library/INTERFACE.md.
SONG_OWN = {
    "epithet": dict(W="steadfast", U="many-minded", B="far-reaching", R="fire-hearted", G="deep-rooted"),
    "open": dict(        # the lead color's opening, after the old songs; a life of many changes takes Ovid's
        W=dict(full="Sing, Muse, of {N}, {ep}, who kept faith with others for {age} years"),
        U=dict(full="Tell me, Muse, of {N}, {ep}, the one of many turns, who wandered {age} years and wondered at all of it"),
        B=dict(full="Of ambition and its price I sing, and of {N}, {ep}, who made their own way for {age} years"),
        R=dict(full="Sing, goddess, of the fire of {N}, {ep}, who burned bright for {age} years"),
        G=dict(full="Of roots and of returning I sing, and of {N}, {ep}, who belonged to their place for {age} years")),
    "open_many": "My mind is bent to tell of bodies changed into new forms: of {N}, {ep}, who in {age} years was {n} people, and all of them themselves",
    "numbers": ["no one", "one", "two", "three", "four", "five", "six"],
    "first_child": "As a child they were {adjs}, and the seed of who they would be was already in them.",
    "first_later": "By their {nth} year they were {adjs}.",
    "unsettled": "unsettled",
    "swing": "they turned {img}, {span}: {winds}.",
    "span_all": "all their days",
    "span_years": "for {n} years",
    "winds_both": "{adjs} always, while their {nouns} came and went",
    "winds_apart": "now {a}, now {b}",
    "flicker": dict(     # a swing, by the color that came and went
        W=dict(first="like a lamp lit and put out and lit again"), U=dict(first="like a question asked, set aside and asked again"),
        B=dict(first="like a coin turned over and over in the hand"), R=dict(first="like a flame in a gusting wind"),
        G=dict(first="like the tide that leaves the shore and always comes back")),
    "harbour": "At {age} the winds fell still, and they came to harbour, {adjs} at last.",
    "turn": dict(death=dict(big="And {cause}, and {gods} remade them.", small="And {cause}, and they were not the same after."),
                 title=dict(big="Then, {cause}, a great change came over them.", small="Then, {cause}, they were changed a little."),
                 event=dict(big="Then, {cause}, the world shook them into a new shape.", small="Then, {cause}, something shifted in them.")),
    "cause_death": dict(parent="when a parent went down to the house of the dead", sibling="when a sibling went down into the dark",
                        friend="when a friend was taken from them", grandparent="when the old ones of the house were laid in the earth",
                        partner="when the one they loved went down into the dark before them", child="when a child of theirs was taken",
                        other="when someone dear went down into the dark"),
    "cause_moment": "in the year of {moment}",
    "cause_title": "upon {becoming}",
    "drift": dict(big="And with the years a great change came over them, as changes come in the old tales.",
                  mid="{Decade} the old shape loosened, and a new one grew.",
                  small="Slowly, as stone is worn by water, they were changed."),
    "rise": dict(W=dict(first="a sense of duty rose in them as a lamp is lit in a window at dusk", again="a sense of duty rose in them again"),
                 U=dict(first="curiosity rose in them as a river cuts its way down to the sea", again="curiosity rose in them again"),
                 B=dict(first="ambition rose in them as a hawk climbs on the warm wind", again="ambition rose in them again"),
                 R=dict(first="passion rose in them as fire runs through summer grass", again="passion rose in them again"),
                 G=dict(first="rootedness rose in them as an oak sends its roots down into the dark earth", again="rootedness rose in them again")),
    "fall": dict(W=dict(first="the old duties slipped from their shoulders like a cloak", again="their sense of duty faded once more"),
                 U=dict(first="their questions fell quiet, like birds at evening", again="their curiosity faded once more"),
                 B=dict(first="their hunger for more was laid down like a sword", again="their ambition faded once more"),
                 R=dict(first="the fire in them sank to embers", again="their passion faded once more"),
                 G=dict(first="their roots let go of the old ground", again="their rootedness faded once more")),
    "home": "So they came home to an old self, as the wanderer comes home.",
    "longest": "For {n} years they were {ident}, and that was the longest of their shapes.",
    "rare_long": "Against the odds, as the bards love best, at {age} they became {title}.",
    "rare_became": "This too the song keeps, for few are given it: at {age} they became {title}.",
    "rare_took": "This too the song keeps, for few are given it: at {age} they took to {doing}.",
    "rare_mark": "And the song does not hide it: at {age} they {deed}.",
    "rare_moment": dict(W="And this the song keeps for the ones who come after: {moment}, in their {nth} year.",
                        U="And a thing few ever see, they saw, at {age}: {moment}.",
                        B="And at {age} came a day that few are dealt, and they played it: {moment}.",
                        R="And at {age} came a day few ever live, and they lived it whole: {moment}.",
                        G="And at {age}, a day the whole place remembered: {moment}."),
    "deeds_reach": dict(own="When the moment came, they reached most often for their {noun}.",
                        other="When the moment came, they reached most often for their {noun}, though it was not the color they wore longest."),
    "deeds_won": dict(often="And {gods} favoured them more often than not.", half="Half the time they won, and half the time they rose again.",
                      seldom="Often they failed, and every time they got up and went on."),
    "deeds_pushed": "And {n} times {hand} was on them, and it pushed them toward their {noun}",
    "deeds_pushed_end": dict(willing=", and they went willingly.", bore=", and they bore it.", against=", against their own heart."),
    "deeds_once": "Once {hand} was on them, and it pushed them toward their {noun}",
    "deeds_free": "No god bent their will: every road they walked, they chose.",
    "shape": dict(       # the shape of their contentment over the adult years
        rise="Their life climbed like a road into the hills: the hardest years were the first, the best came late.",
        fall="Their life was a river that widened and slowed: the bright years came early, and later the waters ran quieter.",
        valley="They went down into the valley {lo} and climbed out of it again, into the high ground {hi}.",
        fallen="They stood on the heights {hi}, went down into the valley {lo}, and climbed out of it again.",
        summit="Their life rose to a summit {hi} and came gently down from it.",
        level="Their years ran even, like a long plain under a steady sky."),
    "decade_youth": "in their youth",
    "decade": "in their {d}s",
    "peace": "Their deepest peace was {decade}, still as water at evening.",
    "buried": "They buried {n} of their own, and carried each of them.",
    "reached": dict(never="And {n} times they reached for what lay beyond them, and never once took hold of it, and reached anyway.",
                    once="And {n} times they reached for what lay beyond them, and once took hold of it.",
                    more="And {n} times they reached for what lay beyond them, and {made} times took hold of it."),
    "death_early": "At {age} they went down into the dark, {how}, and the song does not grieve it less.",
    "death_old": "Full of years at {age}, they went down into the dark, and the dark was kind.",
    "close": "So it is sung now, {hall}: the song of {N}, {glad}. {cheer} {toast}",
    "cheer": "Raise the cup.",
    "hall": "where the cups are filled and the night is long",
    "gods": "the gods",
    "hand": "the gods' hand",
    "glad": {("high", "high"): "who lived, and lost, and was glad", ("high", "mid"): "who lived well, and mostly as themselves",
             ("high", "low"): "who was glad, though the gods chose much of it", ("mid", "high"): "who went their own way at an ordinary price",
             ("mid", "mid"): "who took the good with the bad, as mortals must", ("mid", "low"): "who bore what was laid on them, and went on",
             ("low", "high"): "who paid dearly to stay themselves, and paid it", ("low", "mid"): "who walked a hard road, and did not stop",
             ("low", "low"): "who suffered much, and still was there to tell of it"},
    "toast": dict(W=dict(glad="To a life that kept faith with others."), U=dict(glad="To a mind that never stopped asking."),
                  B=dict(glad="To one who made their own way."), R=dict(glad="To a heart that burned."), G=dict(glad="To one who belonged.")),
}
for _c in COLORS:        # the game's own words have one opening, image and toast per color: the variants share them
    SONG_OWN["open"][_c]["short"] = SONG_OWN["open"][_c]["full"]
    SONG_OWN["flicker"][_c]["again"] = SONG_OWN["flicker"][_c]["first"] + ", once more"
    SONG_OWN["toast"][_c]["hard"] = SONG_OWN["toast"][_c]["glad"]
SONG_OWN_WORLD = dict(tribal=dict(hall="around the fire, when the elders sing"),
                      magic=dict(hall="in the halls, when the bards take up the lyre"))
EPIC_TOLD = 6            # stanzas of change at most, after the invocation
OPEN_FULL = 60           # the opening for a full life from this age, the short one before it
TALK_PUSHES = 5          # pushes before the last conversation is told in full ("few" below it, "none" with none)
TALK_TRUST = 0.2         # trust in a color that counts in the last conversation, either way
TALK_SHARE = 1 / 3       # the voice's share of their color change from which "glad" takes its second line


def _merged(a, b):
    """a with b's keys over it, one key, color or band at a time (SONG_WORLD changes single words, not whole tables)."""
    out = dict(a)
    for k, v in b.items():
        out[k] = _merged(a[k], v) if isinstance(v, dict) and isinstance(a.get(k), dict) else v
    return out


def song_words(setting):
    """The song's words for a world: the Library's, with that world's own over them, or the game's own without the pin."""
    if getattr(ES, "SONG", None):
        return _merged(ES.SONG, getattr(ES, "SONG_WORLD", {}).get(setting, {}))
    return _merged(SONG_OWN, SONG_OWN_WORLD.get(setting, {}))


def _cap(s):
    return s[:1].upper() + s[1:]


def _num(n, W):
    """'three'; past the song's last number word, the Library's "many" when it gives one (else digits)."""
    if 0 <= n < len(W["numbers"]):
        return W["numbers"][n]
    return W.get("many") or ("many" if len(W["numbers"]) > 7 else str(n))


def _again(entry, seen, key):
    """A color's first or repeat line (flicker, rise, fall); the k-th repeat takes again[(k-1) % len] when the Library
    gives a list (Library PR #29), the one line when it gives a string."""
    k = seen.get(key, 0); seen[key] = k + 1
    if not k:
        return entry["first"]
    a = entry["again"]
    return a[(k - 1) % len(a)] if isinstance(a, (list, tuple)) else a


def _song_colors(h):
    """The life's colors, most held over the years first (the mean of its weekly colors), and those means."""
    ws = h.get("w", [])
    allw = np.mean(np.asarray([w for _, w in ws], float), axis=0) if ws else np.full(5, 0.2)
    return [COLORS[i] for i in np.argsort(-allw)], allw


def _epic_cause(met, at, share, say_of, W):
    """What turned them, in the song's words, and what kind of cause it was."""
    near = [m for m in met if at - WHY_YEARS <= m[0] <= at]
    deaths = sorted((m for m in near if m[1] == "death"), key=lambda m: DEATH_WEIGHT.get(m[2], 9))
    if deaths and deaths[0][2] != "grandparent":
        return W["cause_death"].get(deaths[0][2], W["cause_death"]["other"]), "death"
    why = _why(met, at, share, say_of)
    if why is None:
        return None, None
    if why.startswith("the death of"):
        return W["cause_death"]["grandparent"], "death"
    return ((W["cause_moment"].format(moment=why), "event") if why.startswith("“") else
            (W["cause_title"].format(becoming=why), "title"))


def _nth(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _decade(a, W):
    return W["decade_youth"] if a < 20 else W["decade"].format(d=a // 10 * 10)


def _epic_thing(k, n_, say_of, at, lead, W):
    """A rare thing the life met, as the song keeps it; the framing follows the life's lead color."""
    if k == "long":
        return W["rare_long"].format(age=at, title=n_)
    if k == "role":
        say = say_of(n_)
        return (W["rare_became"].format(age=at, title=say) if re.match(r"(a|an|the|one) ", say) else
                W["rare_took"].format(age=at, doing=_becoming(say)))
    if k == "mark":
        return W["rare_mark"].format(age=at, deed=getattr(ES, "MARK_SAY", {}).get(n_, n_))
    return W["rare_moment"][lead].format(moment=_quoted(n_), age=at, nth=_nth(at))


def _ways(acts):
    """The colors of the ways they acted at the player's moments: their share, from 'W+U>R' strings."""
    v = np.zeros(5)
    for _, cols, _, _ in acts:
        ways = [c for c in str(cols).partition(">")[0].split("+") if c in COLORS]
        for c in ways:
            v[COLORS.index(c)] += 1 / len(ways)
    return v


def _deeds(acts, lead_w, review, W):
    """The stanza of deeds: how they acted when it mattered, how it went, and where the gods' hand (the player) pushed."""
    if len(acts) < 3:
        return ""
    own = [a for a in acts if not a[3]]; pushed = [a for a in acts if a[3]]
    v = _ways(own or acts)
    if v.sum() == 0:
        return ""
    top = COLORS[int(np.argmax(v))]
    S = [W["deeds_reach"]["own" if top == lead_w else "other"].format(noun=NOUN[top])]
    won = sum(a[2] for a in acts) / len(acts)
    S.append(W["deeds_won"]["often" if won >= 0.65 else "half" if won >= 0.4 else "seldom"].format(gods=W["gods"]))
    if pushed:
        pv = _ways(pushed)
        pt = COLORS[int(np.argmax(pv))] if pv.sum() else None
        integ = review.get("integrity", 1.0)
        if pt:
            n_ = max(int(review.get("forced") or 0), 1)     # F13: the review's count of pushes, not only those that came to an act
            S.append((W["deeds_once"] if n_ == 1 else W["deeds_pushed"]).format(n=_num(n_, W), hand=W["hand"], noun=NOUN[pt])
                     + W["deeds_pushed_end"]["willing" if integ >= 0.9 else "bore" if integ >= 0.75 else "against"])
    else:
        S.append(W["deeds_free"])
    return " ".join(S)


def _shape(c, W):
    """The shape of contentment over the adult decades: rise, fall, valley, summit or level, with where."""
    dec = {}
    for a, v in c:
        if a >= 20:
            dec.setdefault(int(a) // 10 * 10, []).append(v)
    dec = {d: float(np.mean(v)) for d, v in dec.items() if len(v) >= 3}
    if len(dec) < 3:
        return ""
    ds = sorted(dec); vals = [dec[d] for d in ds]
    hi, lo = ds[int(np.argmax(vals))], ds[int(np.argmin(vals))]
    if max(vals) - min(vals) < 0.08:
        kind = "level"
    elif lo not in (ds[0], ds[-1]):
        kind = "valley" if hi > lo else "fallen"
    elif hi not in (ds[0], ds[-1]):
        kind = "summit"
    else:
        kind = "rise" if hi > lo else "fall"
    return W["shape"][kind].format(hi=_decade(hi, W), lo=_decade(lo, W))


def life_paragraph(name, h, review, setting):
    """The life as a bard's song, for the end of a life (review["story"]): stanzas parted by blank lines."""
    try:
        from rarity import RARITY
    except Exception:
        RARITY = {}
    W = song_words(setting)
    adjs = lambda cols: _adjs(cols) if cols else W["unsettled"]
    rs = RARITY if setting == "earth" else {}
    share = lambda kind, n_: rs.get(kind, {}).get(n_)
    met = h.get("met", [])
    say_of = lambda n_: h.get("title_say", {}).get(n_) or an(n_)
    ws = h.get("w", [])
    died = review.get("died")
    age = int((died or {}).get("age") or review.get("age") or 0)
    eps = _episodes([(a, l) for a, l, *_ in h["name"]] if h.get("name") else h["label"])   # F13: the headings' names
    n_shapes = len({l for e in eps for l in e[1]})
    if len(eps) > EPIC_TOLD:                          # a long song tires: the first, the last, and the longest between
        keep = sorted(range(1, len(eps) - 1), key=lambda i: eps[i][2] - eps[i][3])[:EPIC_TOLD - 2]
        eps = [eps[i] for i in sorted({0, len(eps) - 1, *keep})]
    rare = [(0.0, x["age"], "long", x["say"] if re.match(r"(a|an|the|one) ", x["say"]) else an(x["name"]))
            for x in h.get("long", []) if x.get("made") and x.get("age") is not None]
    rare += sorted(((share(kk, n_), a, kk, n_) for a, kk, n_ in met if kk != "death" and share(kk, n_)
                    and share(kk, n_) < RARE_SHARE), key=lambda r: (r[0], r[1]))
    rare = sorted(rare[:RARE_TOLD], key=lambda r: r[1])
    home = lambda r: max([j for j, e in enumerate(eps) if e[2] <= r[1]] or [0])
    order, allw = _song_colors(h)
    lead = order[0]
    ep = f"{W['epithet'][order[0]]} and {W['epithet'][order[1]]}"
    # the invocation: a life of many shapes takes Ovid's opening, a steadier one its lead color's, full or cut short
    V = [(W["open_many"].format(N=name, ep=ep, age=age, n=_num(n_shapes, W)) if n_shapes >= 4 else
          W["open"][lead]["full" if age >= OPEN_FULL else "short"].format(N=name, ep=ep, age=age)) + "."]
    used = {}
    for i, (kind, ls, a0, a1) in enumerate(eps):
        a0i, dur = int(a0), int(round(a1 - a0))
        if kind == "swing":
            both, flick = set(ls[0]) & set(ls[1]), set(ls[0]) ^ set(ls[1])
            fc = max(flick, key=lambda c: allw[COLORS.index(c)]) if flick else lead
            img = _again(W["flicker"][fc], used, "k" + fc)              # the same color flickering again
            winds = (W["winds_both"].format(adjs=adjs(both), nouns=_nouns(flick)) if both else
                     W["winds_apart"].format(a=adjs(ls[0]), b=adjs(ls[1])))
            cause, ck = _epic_cause(met, a0, share, say_of, W) if i else (None, None)
            span = W["span_all"] if i == 0 and a1 - a0 >= 0.6 * max(age, 1) else W["span_years"].format(n=_num(dur, W))
            s_ = W["swing"].format(img=img, span=span, winds=winds)
            s_ = _cap(cause) + ", " + s_ if cause else _cap(s_)
        elif i == 0:
            s_ = (W["first_child"] if a0 < 18 else W["first_later"]).format(adjs=adjs(ls[0]), nth=_nth(a0i))
        else:
            pk, pls, pa0, pa1 = eps[i - 1]
            up, dn = _drift(ws, pa0, pa1, a0, a1)
            pick_ = lambda x, y: [w for a, w in ws if x <= a < y]
            p_, q_ = pick_(pa0, pa1), pick_(a0, a1)
            size = float(np.abs(np.mean(q_, axis=0) - np.mean(p_, axis=0)).sum()) if p_ and q_ else 0.0
            cause, ck = _epic_cause(met, a0, share, say_of, W)
            harbour = pk == "swing" and ls[0] in pls
            if harbour:                                  # the swing's end: the harbour says it, no drift after it
                head = W["harbour"].format(age=a0i, adjs=adjs(ls[0]))
                up = dn = None
            elif cause:                                  # the cause's kind and the change's size choose the words
                head = W["turn"][ck]["big" if size >= 0.25 else "small"].format(cause=cause, gods=W["gods"])
            else:
                head = W["drift"]["big" if size >= 0.25 else "mid" if size >= 0.12 else "small"].format(Decade=_cap(_decade(a0i, W)))
            parts = ([_again(W["rise"][up], used, up)] if up else []) + ([_again(W["fall"][dn], used, "f" + dn)] if dn else [])
            s_ = head + (" " + _cap("; ".join(parts)) + "." if parts else "")
            if any(ls[0] in e[1] for e in eps[:i - 1]) and not harbour:
                s_ += " " + W["home"]
        if kind == "steady" and dur >= 10 and i == max(range(len(eps)), key=lambda j: eps[j][3] - eps[j][2]):
            s_ += " " + W["longest"].format(n=_num(dur, W), ident=_ident_a(ls[0]))
        for r in (r_ for r_ in rare if home(r_) == i):
            s_ += " " + _epic_thing(r[2], r[3], say_of, int(r[1]), lead, W)
        V.append(s_)
    # their deeds at the player's moments, and the gods' hand
    d_ = _deeds(h.get("acts", []), lead, review, W)
    if d_:
        V.append(d_)
    if h.get("returns"):                              # Picks come back: the pick that came back after the longest years
        x = max(h["returns"], key=lambda r_: r_["age"] - r_["seed"]["age"])
        V.append(W.get("came_back", "And what they did at {a}, at “{m}”, came back to them at {b}, at “{n}”.").format(
            a=int(x["seed"]["age"]), m=x["seed"]["moment"], b=int(x["age"]), n=x["moment"], N=name))
    # the ups and downs, losses and long shots, and the end
    T = []
    sh = _shape(h.get("content", []), W)
    if sh:
        T.append(sh)
    dp = {}
    for a, v in h.get("peace", []):
        if a >= 20:
            dp.setdefault(int(a) // 10 * 10, []).append(v)
    dp = {d: float(np.mean(v)) for d, v in dp.items() if len(v) >= 3}
    if dp:
        T.append(W["peace"].format(decade=_decade(max(dp, key=dp.get), W)))
    lost = sum(1 for m in met if m[1] == "death" and m[2] != "grandparent")
    if lost >= 3:
        T.append(W["buried"].format(n=_num(lost, W)))
    tried = [x for x in h.get("long", [])]
    if len(tried) >= 2:
        made = sum(1 for x in tried if x["made"])
        T.append(W["reached"]["never" if made == 0 else "once" if made == 1 else "more"].format(n=_num(len(tried), W), made=_num(made, W)))
    if died and died.get("cause") not in (None, "old age"):
        T.append(W["death_early"].format(age=int(died["age"]), how=died["how"]))
    else:
        T.append(W["death_old"].format(age=age))
    V.append(" ".join(T))
    # the close: gladness by the peace reading's bands, the toast by the lead color and how well they lived
    bands = tuple((review.get("reading") or {}).get("bands") or ("mid", "mid"))
    V.append(W["close"].format(hall=W["hall"], N=name, glad=W["glad"].get(bands, W["glad"][("mid", "mid")]), cheer=W["cheer"],
                               toast=W["toast"][lead]["hard" if bands[0] == "low" else "glad"]))
    return "\n\n".join(V)


def last_talk(name, name_s, h, review, setting):
    """The last conversation with the voice, told after the song (earth_story.py LAST_TALK): what it gave and what it cost,
    by the character's trust in the player per color, and whether they were glad of it, by their trust along the colors
    the player pushed and the voice's share of their color change. Empty without the Library's words."""
    LT = getattr(ES, "LAST_TALK", None)
    if not LT:
        return ""
    noun = (getattr(ES, "VOICE", {}).get("noun") or {})
    fill = dict(N=name, Ns=name_s, voice=noun.get(setting) or noun.get("earth") or "voice")
    n = h.get("forced", 0)
    if n < TALK_PUSHES:
        return LT["none" if not n else "few"].format(**fill)
    tr = np.asarray([(review.get("trust") or {}).get(c, 0.0) for c in COLORS], float)
    lead = _song_colors(h)[0][0]
    S = [LT["intro"]]
    hi, lo = COLORS[int(np.argmax(tr))], COLORS[int(np.argmin(tr))]
    if tr.max() > TALK_TRUST:                          # what it gave: the color they came to trust most
        S.append(LT["gave"][hi]["own" if hi == lead else "other"])
    if tr.min() < -TALK_TRUST:                         # what it cost: the one they resented most, opposed to the lead or not
        S.append(LT["cost"][lo]["enemy" if (COLORS.index(lo) - COLORS.index(lead)) % 5 in (2, 3) else "other"])
    pv = _ways([a for a in h.get("acts", []) if a[3]])   # trust over all pushes: along the colors the player pushed
    over = float(pv @ tr / pv.sum()) if pv.sum() else float(tr.mean())
    glad = "glad" if over > TALK_TRUST else "sorry" if over < -TALK_TRUST else "torn"
    S.append(LT["glad"][glad][int(h.get("voice", {}).get("share", 0.0) >= TALK_SHARE)])
    return " ".join(S).format(**fill)


def peace_reading(ful, ser, integ, gifts):
    """The end-of-life reading: how well they lived (satisfaction and peace through adulthood) and how much the life was
    their own (true to their wants, and acts that used their gifts)."""
    well = (ful + ser) / 2
    own = integ if gifts is None else (integ + gifts) / 2
    band = lambda v, k: "high" if v >= PEACE_BANDS[k][0] else "mid" if v >= PEACE_BANDS[k][1] else "low"
    bw, bo = band(well, "well"), band(own, "own")
    return dict(words=PEACE_WORDS[(bw, bo)], well=round(well, 3), own=round(own, 3), bands=[bw, bo])


_CAT = {}


def book_catalog(setting):
    """Everything the Book of Moments can hold in a world, with how rare it is (rarity.py, modern Earth only for now)."""
    key = "earth" if setting == "earth" else "base"
    if key in _CAT:
        return _CAT[key]
    try:
        from rarity import RARITY
    except Exception:
        RARITY = {}
    rs = RARITY if key == "earth" else {}
    sh = lambda kind, n_: rs.get(kind, {}).get(n_)
    L, wm = library_for(setting)
    src = {x["name"]: x for x in (L["src"] if L.get("src") and "COND" in L else [])}
    mom = []
    for n_ in L["names"]:
        if n_ == "an ordinary week":
            continue
        x = src.get(n_, {})
        mom.append(["s|" + n_, (x.get("life") or "life").split(",")[0].strip(), x.get("tier", ""), sh("sit", n_)])
    for e_ in L.get("EVR", []):
        mom.append(["e|" + e_["name"], e_.get("source", "life event"), "event", sh("read", e_["name"])])
    GR = L.get("ROLES")
    titles = [[GR["names"][i], STATUS_WORD.get(GR["names"][i], GR["say"][i]), GR["kindname"][i], sh("role", GR["names"][i])]
              for i in range(GR["NT"])] if GR is not None else []
    _CAT[key] = dict(world=key, lives=rs.get("lives", 0), moments=mom, deeds=[[m_, sh("mark", m_)] for m_ in L.get("MARKS", [])],
                     titles=titles, idents={l_: [n_, ident_meaning(l_)] for l_, n_ in IDENT_NAME.items() if l_})
    return _CAT[key]


def clean(x):
    """Plain Python values (for the browser's JSON): numpy numbers, booleans and arrays become their Python kind."""
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return clean(x.tolist())
    if isinstance(x, np.generic):
        return x.item()
    return x


def hint(d):
    if d < -0.25:
        return "much worse"
    if d < -0.08:
        return "worse"
    if d <= 0.08:
        return "about right"
    if d <= 0.25:
        return "better"
    return "much better"


def reluctance(gap, ref=1.0, below_by=0.0, clash=False):
    """0 (glad to) .. 1 (dead against): how much a push to this option goes against the character (see GAME).
    gap: how far it falls below the best option they see; ref: this moment's typical gap; below_by: how far it falls
    below doing nothing (negative when above); clash: its colors are enemies of who they are."""
    G = GAME
    r = min(1.0, (max(0.0, gap / max(ref, G["rel_ref"]) - G["rel_z0"]) / G["rel_zs"]) ** G["rel_zp"])
    if clash and gap >= G["rel_clash"]:
        r = max(r, min(1.0, 0.6 + 0.4 * (gap - G["rel_clash"]) / G["rel_clash_s"]))
    if below_by > 0:
        r = max(r, min(0.6, G["rel_dn"] + 0.3 * below_by / G["rel_dn_s"]))
    return r


def clash_with(colors, ident):
    """The colors of an option's ends that are enemies of the character's identity colors, when its ends share none of
    them and are more enemy than ally to them (Magic's pie: W-B, W-R, U-R, U-G, B-G)."""
    ends = [c for c in (colors.split(">")[-1] if colors else "").split("+") if c in E.IDX]
    idc = [c for c in (ident or "") if c in E.IDX]
    if not ends or not idc or set(ends) & set(idc):
        return []
    score = sum(E.ENEMY[E.IDX[e], E.IDX[c]] - E.ALLY[E.IDX[e], E.IDX[c]] for e in ends for c in idc)
    return [e for e in ends if any(E.ENEMY[E.IDX[e], E.IDX[c]] for c in idc)] if score > 0 else []


def rel_word(r):
    return "no" if r < 0.05 else "low" if r < 0.3 else "medium" if r < 0.6 else "high"


ACCEPT = ["would go with it", "okay with it", "reluctant", "against it"]
ACC_FROM_ENGINE = {"would go with it": "would go with it", "okay with it": "okay with it", "reluctant": "reluctant", "against": "against it"}


def accept_word(r, own=False):
    """How the character feels about being pushed to an option, in their own words."""
    return "their own pick" if own else ACCEPT[0 if r < 0.02 else 1 if r < 0.3 else 2 if r < 0.6 else 3]
