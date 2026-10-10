"""Chroma: the game layer (text prototype).

The engine decides the character's life week by week. The player sets the scene, watches, and at
checkpoints may pick an option for the character. A pick always happens (Emren, 2026-10-04): it skips
the character's own noticing, wanting and self-control, but the further it is from what they wanted
(reluctance), the more it costs them. Only what is impossible stays closed; options the character
lacks the means for, or that their surroundings do not offer, can be forced at extra cost and risk.

Nothing here writes colors or meta variables directly. The game acts only through what the engine
already has: the aspiration (upbringing), surroundings, resources, the chosen option, the true
chance of success, the surprise of the outcome, stress and pent-up pressure.
"""
import re
import numpy as np
from collections import deque
import os
import sys
from link import E, PIN
import explain as X             # engine v7: the character's view before a choice, what came of it after
import foresee as F             # engine v7: the foreseen outcome of a plan
from story import Story, LIB_READ, act, chooses, plain, ADJ, NOUN, EPITHETS, SETTINGS, load_library_story, DRIVER_WORD, neg_of, STATUS_WORD, mk, NAME_POOL, an
from worldview import WorldView, EngineWorld, from_engine, who_word, lever_info, push_words   # the outer world as the player sees it (chroma-world/)
try:
    import earth_play as EP     # 5.6: the turning point, put to the player by the game alone (never loaded into a life)
except ImportError:
    EP = None
try:
    import earth_story as ES    # the Library's words for the played game: the song, the voice, threads (chroma-library)
except ImportError:
    ES = None
try:
    import earth_spheres as ESP # item 15: the Library's sphere words for "your places" (haunt names, rungs, faces)
except ImportError:
    ESP = None
try:
    import routine as RT        # point 1 (Emren 20:39): everyday routine lines for the interlude between moments
except ImportError:
    RT = None
try:
    import earth_story as ES    # the Library's words for the end of a life: the song, the marks, the last conversation
except Exception:
    ES = None

C = E.C
COLORS = E.COLORS
CNAME = dict(W="White", U="Blue", B="Black", R="Red", G="Green")
STAGES = E.STAGE_NAMES
KNAMES = E.KNAMES
RNAMES = ["money", "time", "health", "ties", "freedom"]

# ---- the costs of a forced pick (game parameters, tuned by eye; candidates to move into the engine)
GAME = dict(
    # reluctance. Since the engine's points hand-off (12:30) explain.before gives each option its own level and reluctance
    # (accept), and the game uses those; the rule below is the game's stopgap, kept for options before() leaves out.
    # (Emren 2026-10-05 09:25: "I would go with it" and "I am okay with it" are different feelings; a character
    # should be at least okay with options it is not against). The gap is how far an option's appeal falls below the best
    # option the character sees. It is read against this moment's typical gap (the median over the other options they
    # see, at least rel_ref): z = gap / ref, reluctance ((z - rel_z0) / rel_zs) ** rel_zp. Against it means against who
    # they are: an option whose ends are enemies of their identity colors (and share none of them) and whose gap is past
    # rel_clash is at least .6; an option liked less than doing nothing is at least rel_dn, rising to .6 at rel_dn_s below
    # it. Words: under .02 "would go with it", .3 "okay with it", .6 "reluctant", else "against it". Measured in
    # test/acceptance.py (README, version 14). A first try read only the gap from the best option: in later life the
    # utility gaps grow to 4 to 8 for everything outside the character's colors, and 36% of moments read reluctant or
    # against for 70% or more of the options.
    rel_ref=1.0, rel_z0=0.2, rel_zs=2.91, rel_zp=1.357, rel_clash=3.5, rel_clash_s=4.0, rel_dn=0.3, rel_dn_s=1.5,
    effort=1.5,          # half-hearted effort: true odds drop by this many logit units at full reluctance
    out_of_reach=1.2,    # extra logit penalty for forcing an option the character lacks the means or the opening for
    learn_keep=0.4,      # a fully reluctant act still teaches this share of its surprise (Emren: "Scaled")
    stress=0.4,          # stress added at full reluctance (stress lowers peace and strengthens habit)
    backlash=1.2,        # pent-up pressure toward what they wanted, at full reluctance (it can break through)
    backfire_stress=0.3, # forcing an out-of-reach option and failing: extra stress
    backfire_money=0.05, # ... and a loss of money
    upbringing=0.006,    # weekly pull of the family's values on a child's want, until 15
    # hindsight and trust (IDEAS.md, "Player intervention that helps", Emren 2026-10-09): after a push, the character
    # judges it. A push that worked and fed a need they lacked is partly accepted: some of its stress, pent-up wanting,
    # lost autonomy and its count against "their own" are undone (never all of it, or pushing would be free). A push
    # that failed, or worked but fed nothing they lacked while they were reluctant, is resented. Either way the
    # character's trust in the player moves, per color, along the colors of the act.
    need_thin=0.5,       # a need below this is lacking (the sheet's "thin"); a first one brings a one-time hint
    hind_max=0.6,        # the most of a push's costs hindsight can undo
    hind_full=0.012,     # an act's lift to needs they lacked (shares of one) for the full hind_max: about a point
    hind_min=0.004,      # less lift than this to needs they lacked is nothing
    hind_rel=0.1,        # a push they were this reluctant about or more is judged afterwards; below it, they didn't mind
    resent_more=0.3,     # a resented push that failed: this much more pent-up wanting, x its resentment
    trust_gain=0.25,     # trust gained by a fully accepted push, along the act's colors (toward 1)
    trust_loss=0.2,      # trust lost by a resented push at full reluctance (toward -1)
    trust_cut=0.5,       # at full trust in the act's colors, this share of a push's resentment (stress, wanting) is spared
    distrust_add=0.5,    # at full distrust, this much more resentment
    # clarity item 7, "trust that moves" (chroma-hud/gameplay-check/findings.md §1; chroma-ideas/voice-mechanics.md §2;
    # Emren 10-10 10:25 UTC "apply all of them"; v22.4, off until its refit): every push is judged by its outcome, not only
    # the reluctant ones. A push that hindsight leaves unjudged still moves trust along the act's colors: + (judge_a +
    # judge_b x reluctance) x (1 - trust) when it worked, - the same x (1 + trust) when it failed (voice-mechanics.md's
    # .02 + .08 x reluctance, doubled for trust's -1 to 1 scale). Accepted and resented pushes keep their own steps.
    trust_judge=False, judge_a=0.04, judge_b=0.16,
    # item 4, pivotal picks (implementation list; chroma-ideas/gameplay-feel.md §5; Emren 2026-10-08 22:58, 23:18): every
    # moment put to the player is a turning point. Its pick teaches more the further it is from who they are; a success
    # teaches toward the picked ways and they lead the character's own acts for a season (F2); a failure can backfire
    # toward what they wanted. Letting them choose confirms who they are and steadies them. The weeks without the player
    # weigh about half. All of it acts in played lives only: lives with no player never run the game.
    # calibrated 2026-10-09 on steered lives (preset 1, seeds 1-6; let, most:U, most:W): piv .25 put a steered color at
    # .60 at 40; .15 with piv_own .3 holds it in the name at 40 in 6 of 6 but lets left-alone lives settle into one color,
    # piv_own .1 keeps them varied but their name changes 4.5 times after 18: piv_own .2 between
    piv=0.15,            # a pivotal pick's lesson: this x plasticity x the move toward the picked ways (as the engine's ev_z)
    piv_far=1.0,         # ... x (1 + piv_far x how far the pick is from their colors now, 0 to 1): up to twice
    piv_core=0.3,        # this share of the lesson reaches the deep core at once, so a turning point lasts
    piv_own=0.2,         # letting them choose teaches at this share (and leans at this share): it confirms who they are
    piv_fail=0.5,        # a failure that does not backfire (and a push they resented although it worked) teaches at this share
    learn_full=True,     # a pushed act teaches in full (v22.1 cut a reluctant act's lesson to learn_keep; off restores it)
    piv_steady=0.02,     # letting them choose: the deep core follows who they are now by this share (steadies, less drift)
    backfire=0.6,        # a pushed pick that failed backfires with chance backfire x distance x stakes (at most .8), always
                         # when they resented it (hindsight); a backfire teaches toward what they wanted, with no season lean
    lean=0.012,          # F2: weekly pull of the picked ways on their wants, fading to nothing over lean_weeks
    lean_weeks=26,       # six months (Lally et al. 2010: 18 to 254 days for a new habit)
    quiet_k=0.5,         # the weeks without the player: their own lesson, random drift and outside pushes at this share
                         # (engine P own_k, drift_k, ev_push_k, read live; the era's current stays whole, item 12)
    plan_lean=0.5,       # 5.4: a plan they take up leans toward the picks of the last seasons by up to this share
    pick_half=26,        # weeks for the picks' weight in that lean to halve
    # 5.6, this life's threads first: a moment that follows from the life's own titles, commitments, plans and dreams
    # weighs more when the game picks the moments to put to the player, more again when a pick of theirs started it (F5
    # tells that); an everyday moment most lives meet (told_share or more of lives) with no tie to the life is told, not
    # asked. Only this life's history counts (F1 is out)
    tie_imp=0.3, tie_pick=0.3, told_share=0.85,
    # P3, three forces (IDEAS.md; engine-needs-and-steering.md section 5): besides letting them choose and pushing an
    # option (the strong steer), a light steer tilts their own pick toward a color (the engine's steer: + light_k x
    # (5 x the option's ways in that color - 1) to each option's pull, 1 = a third of the values' pull). It costs only
    # what it changed: the act's reluctance x the share of its odds the steer gave it. Steering with the era's pull costs
    # less, against it more: costs x (1 - era_cost x fit), fit -1 to 1 from the era's colors and strength (era_full)
    light_k=1.0, era_cost=0.4, era_full=0.5,
    # 5.6, the price builds to a turning point (earth_play.py, "the day it all comes to a head"): each push adds its
    # resentment and half its reluctance to a price that halves every turn_half weeks; past turn_line, at most turn_max
    # times a life and turn_gap weeks apart, the next moment is the turning point. The pick is a turning point turn_piv
    # times a pick's: picking the color pushed most is the reinvention, their own lead the snap back. It holds with the
    # option's chance (a little more for their own lead); held, the strain and pent-up wanting are let go
    turn_line=2.0, turn_half=52, turn_gap=260, turn_max=0, turn_piv=3.0,   # turn_max 0: off in v22.2 (moves to v22.3, 10-09); 2 when on
    world_steers=False,  # the World panel's marks for each push or lean against the era: off in v22.2 (v22.3)
    fig_own=True,        # K12 (v22.3): no public figure shares the character's first name
    # S2 "Making it their own" (chroma-ideas/social-mechanics.md S2; Emren 10-10 09:04 UTC; v22.4 by the "Split" card 09:55, off until its refit): per color, how far a way
    # the voice pushes toward has become theirs (ix, 0 to 1; steps at .25 "ought to", .5 sees the point, .8 theirs). Each
    # push toward a color adds own_k x push x A x T x S x H: A the steer (light own_light, strong own_strong), T .5 + their
    # trust in that color, S .5 + own_sup x that color's share around them (their haunts' faces and close people, the
    # engine's "around"; an even surround without it), H own_acc when they accepted it, own_res (a step back at half size)
    # when they resented it. A way led by fewer than own_use acts in a year fades by up to own_fade; reluctance in a way is
    # x (1 - own_rel x ix); the peace reading counts a push as their own by its way's ix; at own_theirs the season lean
    # toward it no longer ends. A strong push at reluctance over own_react_rel while ix is under .25 bounces back with
    # chance own_react: ix falls own_react_back and the pent-up wanting grows as a push's does
    own_ix=False, own_k=0.15, own_light=1.5, own_strong=0.6, own_sup=2.5, own_acc=1.5, own_res=-0.5, own_fade=0.02,
    own_use=4, own_rel=0.8, own_theirs=0.8, own_react=0.15, own_react_rel=0.7, own_react_back=0.1,
)
OWN_STEPS = ((0.8, "theirs"), (0.5, "sees"), (0.25, "ought"), (0.0, "asked"))   # S2: ix -> the Library's step key

# stage 1's played-life rules at their off values (the update's UPD_OFF rule: every new mechanic can be switched off):
# with these a played life is the one v22.1 plays, step for step (test/same_engine.py with CHROMA_GAME=off)
GAME_OFF = dict(piv=0.0, piv_own=0.0, piv_steady=0.0, learn_full=False, lean=0.0, quiet_k=1.0, plan_lean=0.0, tie_imp=0.0, tie_pick=0.0, told_share=2.0,
                era_cost=0.0, backfire=0.0, turn_max=0, fig_own=False, own_ix=False, trust_judge=False)
if os.environ.get("CHROMA_GAME"):                   # checks and calibration only: "off", or settings as JSON
    import json as _json
    GAME.update(GAME_OFF if os.environ["CHROMA_GAME"] == "off" else _json.loads(os.environ["CHROMA_GAME"]))
# checks only: settings for the engine's own P as JSON (for example CHROMA_ENGINE='{"shadows": true}' to see light and
# shadow on screen), laid over the life's P when it is set up. Read only when set: without it every life is the page's own
# (upper-case keys set the pinned batch.py's flags instead, before the Earth library loads: {"FAR_MOMENTS": true})
ENGINE_SET = {}
if os.environ.get("CHROMA_ENGINE"):
    import json as _json
    ENGINE_SET = _json.loads(os.environ["CHROMA_ENGINE"])

# Life events (bereavement, disaster, meeting someone...) come at the engine's own yearly rates since v6: a personal
# rate between half and twice the typical one, moved week by week by the context around the person (family, ties,
# money, health, the era, the world, stress, and their own recent trouble and fortune). Every other week is ordinary
# life: one of the everyday situations, most often "an ordinary week". The game's own event clock (EVENT_YEARS,
# CONTEXT) was a stopgap for v5 and is gone.
#
# Modern Earth runs on the Library's Earth batch (the final release batch, next3, 2026-10-07: 527 situations and 5,615
# options in earth.py, with sex and gender and the outer world's moments) with the three approved content packs
# (science, politics, stage) and the Library's dreams (dreams.py), all read through the person's colors with the
# Library's own scenes. With the Engine's outer world on (P["world"]), the life runs inside a world of its own
# (worldview.EngineWorld reads it). Tribal and magic run on the engine's
# base library with the game's own lines and the same dreams until the Library writes those worlds.
_LIBS = {}


# content packs on top of the Earth batch (Emren's point 8): None loads the engine's approved list (batch.PACKS); a pack's
# moments are earth_<pack>.py next to earth.py, its catalogue, rules and helps in engine_pin/packs/<pack>/
PACKS = None


def batch_mod():
    """The pinned engine_pin/batch.py (its act-field codes: TITLE_HELD, MISSED_TITLE, KIND_ACT)."""
    import batch
    return batch


def library_for(setting):
    """The compiled library for a setting (cached), and the world module holding its story fields (or None)."""
    key = setting if setting in ("earth", "tribal", "magic") else "base"
    if key not in _LIBS:
        if key == "earth":
            import batch                            # pinned engine_pin/batch.py; earth.py is pinned next to it
            batch.LIB_DIR = PIN
            batch.PACK_DIR = os.path.join(PIN, "packs")   # pinned copies of chroma-packs/core and chroma-packs/<pack>
            for k_, v_ in ENGINE_SET.items():       # checks only (CHROMA_ENGINE): the batch's own flags
                if k_.isupper():
                    setattr(batch, k_, v_)
            _LIBS[key] = (batch.load_batch("earth", packs=PACKS, setting="earth"), sys.modules.get("earth"))
        else:
            _LIBS[key] = (with_dreams(E.compile_library(), key), None)
    return _LIBS[key]


def with_dreams(L, setting):
    """The Library's dreams for a world that plays on the seed library (tribal, magic): its sparks and the dreams a new
    one is named by, the way batch.load_batch attaches them for Earth (chroma-library/dreams.py, Emren 10-06 22:19)."""
    try:
        import dreams as D_
    except ImportError:
        return L
    if setting in D_.DREAM_TRIGGERS:
        L["DREAM_TRIGGERS"] = list(D_.DREAM_TRIGGERS[setting])
        L["DREAMS"] = [d_ for d_ in D_.DREAMS if setting in d_["worlds"].split()]
    return L
CTX_WORDS = dict(family="own household", ties="ties", money="money", health="health", era="era", harsh="harsh world",
                 unrest="unrest", prosper="prosperity", community="community", stress="stress",
                 trouble="recent trouble", fortune="recent fortune")

# How the world around them stands, in words (Emren 09:25: "+0.5, -0.3 in 'around them' is not representing any").
# The engine's context X runs about -1..1 (recent trouble and fortune 0..2); bands set from 2 Earth lives' spread.
AROUND_WORDS = {
    "own household": [(0.3, "settled"), (-0.3, "unsettled"), (-9, "none of their own")],
    "ties": [(0.2, "close"), (-0.1, "a few"), (-9, "thin")],
    "money": [(0.25, "comfortable"), (-0.15, "getting by"), (-0.42, "tight"), (-9, "poor")],
    "health": [(0.35, "good"), (0.0, "fair"), (-9, "poor")],
    "era": [(0.5, "turbulent times"), (0.15, "changing times"), (-9, "quiet times")],
    "community": [(0.6, "strong"), (0.2, "some"), (-9, "weak")],
    "stress": [(0.5, "high"), (0.15, "some"), (-9, "low")],
    "recent trouble": [(1.4, "a lot"), (0.6, "some"), (-9, "little")],
    "recent fortune": [(1.4, "a lot"), (0.6, "some"), (-9, "little")],
}
AROUND_DEFAULT = [(0.5, "high"), (0.15, "some"), (-9, "low")]


def invest_word(v):
    """What a commitment has taken out of them so far (the engine's investment I, 0 up to about 3)."""
    return "a great deal" if v >= 2 else "a lot" if v >= 1 else "some" if v >= 0.35 else "a little"


def around_word(key, v):
    return next(w for t, w in AROUND_WORDS.get(key, AROUND_DEFAULT) if v >= t)


# States: one-word moods and circumstances read off the character's numbers (Emren 09:25: adjectives like "happy",
# "excited", "wealthy"; later they can open or require events, like perks, once the engine takes them in).
# (word, icon, good, variable, test, threshold). Thresholds sit near the 10th or 90th percentile of adult years.
STATES = [
    ("happy", "ci-sun", 1, "content", ">=", 0.62), ("unhappy", "ci-raincloud", -1, "content", "<=", 0.3),
    ("at peace", "ci-meter-peace", 1, "peace", ">=", 0.56), ("restless", "ci-storm", -1, "peace", "<=", 0.24),
    ("overwhelmed", "ci-wave", -1, "stress", ">=", 1.1), ("stressed", "ci-meter-strain", -1, "stress", ">=", 0.8), ("relaxed", "ci-bird", 1, "stress", "<=", 0.35),
    ("excited", "ci-firework", 1, "mood", ">=", 0.15), ("downcast", "ci-raincloud", -1, "mood", "<=", -0.13),
    ("frustrated", "ci-fist", -1, "want", ">=", 0.7),
    ("wealthy", "ci-domain-money", 1, "money", ">=", 0.45), ("broke", "ci-wallet", -1, "money", "<=", 0.02),
    ("stretched thin", "ci-clock", -1, "time", "<=", 0.12),
    ("in poor health", "ci-domain-health", -1, "health", "<=", 0.55),
    ("well loved", "ci-hug", 1, "ties", ">=", 0.8), ("lonely", "ci-person", -1, "ties", "<=", 0.1),
    ("hemmed in", "ci-padlock", -1, "freedom", "<=", 0.18), ("free", "ci-bird", 1, "freedom", ">=", 0.82),
    ("on a lucky streak", "ci-horseshoe", 1, "fortune", ">=", 1.8), ("down on their luck", "ci-raincloud", -1, "trouble", ">=", 1.8),
]
# how the page shows the engine's adjectives: an icon (Chroma's own set, chroma-art/game/ink-icons.svg) and whether the
# state is good (1), hard (-1) or neither (0)
ADJ_LOOK = {"happy": ("ci-sun", 1), "unhappy": ("ci-raincloud", -1), "calm": ("ci-meter-peace", 1), "restless": ("ci-storm", -1),
            "stressed": ("ci-meter-strain", -1), "excited": ("ci-firework", 1), "low": ("ci-raincloud", -1), "hurting": ("ci-teardrop", -1),
            "unfulfilled": ("ci-moon", -1), "lonely": ("ci-person", -1), "adrift": ("ci-compass", -1), "insecure": ("ci-shield", -1),
            "wealthy": ("ci-domain-money", 1), "poor": ("ci-wallet", -1), "stretched": ("ci-clock", -1), "hemmed in": ("ci-padlock", -1),
            "well connected": ("ci-handshake", 1), "disciplined": ("ci-anchor", 1), "impulsive": ("ci-dice", -1),
            "searching": ("ci-signpost", 0), "settled": ("ci-roots", 1),
            # light and shadow (item 2): the five shadow states, with the visuals thread's glyphs (ink-icons.json "shadow")
            "rigid": ("ci-shadow-rigid", -1), "indecisive": ("ci-shadow-indecisive", -1), "ruthless": ("ci-shadow-ruthless", -1),
            "reckless": ("ci-shadow-reckless", -1), "stuck in their ways": ("ci-shadow-stuck", -1)}
# Light and shadow (stage 2, item 2; chroma-ideas/shadows-mechanics.md §6), the game's words for it. Only shown while the
# engine's shadows switch is on (loc["SHON"]); nothing here is read back by the engine. The engine's four sources, in its
# order (sh_src[..., 0..3]): holding on, ruling, no counterweight, strain. Holding on is told in the colour's own words
SH_HOLD = dict(W="holding on to the old rules", U="holding on to the old answers", B="holding on to the old ambitions",
               R="holding on to the old thrills", G="holding on to the old ways")
SH_FRAC = ((0.15, "a little"), (0.29, "a quarter"), (0.42, "a third"), (0.58, "half"), (0.71, "two thirds"),
           (0.87, "three quarters"), (9, "nearly all"))   # how much of a colour is in shadow, in words
SH_SHOW = 0.05                    # a shadow part under this is not drawn or told
SH_SRC_SHOW = 0.3                 # a source under this (0 to 1) is not named
ADJ_READS = dict(content="satisfaction", peace="peace", stress="strain", mood="recent ups and downs", wound="grief and harm",
                 unmet_hope="hopes not met", belonging="belonging", meaning="a sense of meaning", safety="feeling safe",
                 money="money", time="time to spare", freedom="freedom", ties="people to lean on", discipline="self-control",
                 gap="the gap between who they are and who they want to be")
# Point 4 (Emren 20:39): a state's hover gives its exact definition. Each engine adjective reads one variable over the last
# three months (adj_smooth); ADJ_SCALE says how the page shows that variable: "of100" a 0..1 quantity as out of 100, "pts"
# the engine's own scale times 100 (mood runs about -1..1; strain, grief, hope not met, self-control and the gap have no top)
ADJ_SCALE = dict(content="of100", peace="of100", belonging="of100", meaning="of100", safety="of100", money="of100", time="of100",
                 freedom="of100", ties="of100", stress="pts", mood="pts", wound="pts", unmet_hope="pts", discipline="pts", gap="pts")
STATE_NAME = dict(content="Satisfaction", peace="Peace", stress="Strain", mood="Mood this season", want="Pent-up wanting",
                  money="Money", time="Time", health="Health", ties="Ties", freedom="Freedom",
                  fortune="Recent fortune", trouble="Recent trouble")

# Titles and perks (Emren 12:05: "Use this title and perk ideas and implement it to the game"). The catalogue is the
# Library's (chroma-library/earth_perks_titles.py; the draft is copied into engine_pin/ until it leaves drafts); the engine
# gives and takes them (chroma-engine/roles-handoff.md). The game shows them: in the HUD, on the options (what an act
# needs, which perks help it, what it can give or take) and in the story when one is gained or lost.
def need_level_word(v):
    """A need's level in the character sheet's words."""
    return "well met" if v >= 0.75 else "met" if v >= 0.5 else "thin" if v >= 0.3 else "barely met"


NEED_WORD = dict(safety="safety", belonging="belonging", autonomy="room to choose", competence="a sense of skill", meaning="meaning")
SUS_T = -10 ** 7 // 2             # the engine's p_sus holds NEVER (-10**7) when a perk is not suspended
RUSTY = 0.3                       # a skill or credential no longer held still shows, faded, while its level is above this
COMMIT_KINDS = ("career", "partner", "children", "community", "faith")
PERK_ORDER = ("credential", "skill", "asset", "standing", "bond")
# how the engine says a title or perk was gained or lost, and the level it is told at (0 always, 1 normal, 2 every week);
# a loss the commitment's own line already tells (a job lost, a break-up) or a title that grew into another is not told
ROLE_QUIET = {"came": 2, "retired": 2, "replaced": 9, "became": 9, "left": 9, "lost job": 9, "broke up": 9, "widowed": 9,
              "it ended": 9, "found work": 1, "time passed": 1, "outgrew it": 1, "slipped away": 1, "moved": 1, "the partner died": 9,
              "the marriage ended": 1, "walked away": 2, "no work for a year": 0, "lost it": 1, "reshaped": 1,
              "financial ruin": 1, "missed payments": 1, "no money to keep it": 1, "spent while out of work": 1,
              "the doctor says to stop driving": 1, "a partner at home": 1, "the children grown": 1, "spent in hard times": 1,
              "drifted away": 2, "the engagement broken off": 9}
# a loss another line already tells: out of work at pension age (the retiree line), a soldier who served (the veteran line)
ROLE_QUIET_LOST = {"reached pension age": 9, "served": 9}
ROLE_AGAIN = 5 * 52               # a perk gained or lost again within this many weeks of the last time it was told: quieter


SEASONS = ["winter"] * 9 + ["spring"] * 13 + ["summer"] * 13 + ["autumn"] * 13 + ["winter"] * 4


def season_of(t):
    """The season of a week (the year runs from midwinter)."""
    return SEASONS[int(t) % 52]


def adj_defs():
    """Every state the engine knows, with its exact definition (point 4): the variable it reads, which side, where it begins
    and ends, from what age, and how many adults are in it at a time."""
    return {a[0]: dict(say=a[1], var=a[2], reads=ADJ_READS.get(a[2], a[2]), side=int(a[3]), on=float(a[4]), off=float(a[5]),
                       from_age=float(a[6]), share=float(a[8]), scale=ADJ_SCALE.get(a[2], "pts"),
                       icon=ADJ_LOOK.get(a[0], ("dot", 0))[0], good=ADJ_LOOK.get(a[0], ("dot", 0))[1]) for a in E.ADJECTIVES}


def base_word(b):
    """The Library's chance for an act, as most people manage it: 'about 8 times in 10' (the engine's suggestion)."""
    if b is None:
        return ""
    n = int(b * 10 + 0.5)
    return "almost always" if b >= 0.95 else "almost never" if b < 0.05 else f"about {max(1, min(9, n))} times in 10"


def role_info(GR, i):
    """A title or perk of the catalogue, in words: its name, how it is said, its kind, the ways it asks for (a title) or
    helps (a perk), and what it does: a title meets or costs needs and means; a perk helps acts in its ways by a few
    points, or only opens doors (an access perk: odds 0)."""
    NT = GR["NT"]; title = bool(i < NT)
    say = STATUS_WORD.get(GR["names"][i], GR["say"][i]) if title else GR["say"][i]
    d = dict(i=int(i), name=GR["names"][i], say=say, kind=GR["kindname"][i], title=title,
             ways="".join(c for c, v in zip(COLORS, GR["ways"][i]) if v > 0))
    if title:
        fx = [(NEED_WORD.get(n, n), float(v)) for n, v in zip(E.NEEDS, GR["meets_need"][i]) if abs(v) >= 0.02]
        fx += [(RNAMES[j], float(v)) for j, v in enumerate(GR["meets_res"][i]) if abs(v) >= 0.02]
        d["meets"] = [[w_, 1 if v > 0 else -1] for w_, v in sorted(fx, key=lambda x: -abs(x[1]))][:5]
        d["pred"] = "is " + d["say"]
    else:
        p = i - NT; odds = float(GR["odds"][p])
        d["pred"] = X.predicate(d["say"])
        d["plus"] = int(round(odds * 100))           # points added to acts in its ways, at even odds (engine: odds .05 = +5)
        half = float(GR["half"][p]); d["half"] = half if half > 0 else None
    return d


# v6 loops told in the story: an act joining opposed colors (tension span above this, typical .15-.22); a hard blow
# (the year's worst wound above this, about the top tenth of years; at most every 4 years); a streak of trouble or fortune (above this, about the top sixth; at most every 5 years)
SPAN_TOLD, WOUND_TOLD, STREAK_TOLD = 0.12, 1.6, 1.8
# outside events read through the person's colors (Earth batch, about 540 a life): told when they hit hard, at most every
# three quarters of a year; all of them at the most detailed level
READ_TOLD, READ_GAP = 1.15, 39

# a big moment the player did not decide is told at most this often (weeks), so frequent ones do not crowd the story
TOLD_GAP = {"relationship strain": 156, "reconsidering a commitment": 156}

FREQ = {  # checkpoint frequency: minimum weeks between checkpoints, how important a moment must be,
           # and how many weeks before the same kind of situation can be a checkpoint again
    "rare": (156, 1.6, 312),
    "normal": (72, 1.3, 156),
    "often": (26, 1.0, 52),
    "every": (0, 0.0, 0),
}

WORLDS = {
    "neutral": ("Neutral world: nobody frames any colors as opposed", "neutral"),
    "questions": ("Mild tension on Magic's five questions (group vs individual, security vs freedom, ...); joining opposed "
                  "ways can pay off or tear (the engine's default world)", "mild"),
    "pie": ("Magic's color pie taken literally: opposite colors clash, neighbouring colors bond", "pie"),
}


def mix(spec):
    """'W.6 G.4' -> five shares summing to 1."""
    v = E.parse(spec)
    return v / v.sum() if v.sum() > 0 else np.full(C, 0.2)


def letters(v, thr=0.24):
    """Colors standing out in a mix, e.g. 'W+G'."""
    v = np.asarray(v, float)
    if v.sum() <= 0:
        return "-"
    v = v / v.sum()
    out = [COLORS[i] for i in np.argsort(-v) if v[i] >= thr]
    return "+".join(out) if out else COLORS[int(np.argmax(v))]


# Chroma's own names for who a person is (Emren 2026-10-05 20:46, "Our own names"): plain words a player who never played
# Magic can read. The meaning comes from the engine's combos.IDEAS (Magic's own writing); the Magic name stays in small print.
IDENT_NAME = {
    "": "Still forming",
    "W": "The Guardian", "U": "The Seeker", "B": "The Striver", "R": "The Free Spirit", "G": "The Rooted",
    "WU": "The Lawkeeper", "UB": "The Strategist", "BR": "The Reveller", "RG": "The Wild Heart", "WG": "The Good Neighbour",
    "WB": "The Patron", "UR": "The Inventor", "BG": "The Realist", "WR": "The Champion", "UG": "The Explorer",
    "WUG": "The Noble", "WUB": "The Perfectionist", "UBR": "The Mastermind", "BRG": "The Survivor", "WRG": "The Big Heart",
    "WBG": "The Enduring", "WUR": "The Disciple", "UBG": "The Collector", "WBR": "The Fighter", "URG": "The Wanderer",
    "WUBR": "The Architect", "UBRG": "The Rebel", "WBRG": "The Firebrand", "WURG": "The Idealist", "WUBG": "The Planner",
    "WUBRG": "The Whole",
}
IDENT_MEANING_MORE = {          # the four- and five-color identities (combos.IDEAS covers one to three colors)
    "WUBR": "the made world: order, knowledge, ambition and drive, without Green's acceptance",
    "UBRG": "no rules but their own: everything except White's order",
    "WBRG": "act first: will and action, without Blue's second thoughts",
    "WURG": "the open hand: everyone's good, without Black's self-interest",
    "WUBG": "slow and sure: growth without Red's impulse",
    "WUBRG": "all five colors at once: no single way stands out",
    "": "too young for who they are to have formed",
}


def ident_name(lbl):
    """Chroma's own name for an identity label ('WBG' -> 'The Enduring')."""
    return IDENT_NAME.get(lbl or "", lbl or "Still forming")


def ident_meaning(lbl):
    idea = E.IDEAS.get(lbl, None) if hasattr(E, "IDEAS") else None
    return idea[1] if idea else IDENT_MEANING_MORE.get(lbl or "", "")


def magic_name(lbl):
    """The Magic: The Gathering name, for the small print ('Abzan')."""
    return E.GUILD.get(lbl, lbl) if lbl else ""


def label_name(lbl):
    if lbl == "":
        return "still forming"
    m = ident_meaning(lbl)
    return f"{ident_name(lbl)} ({m})" if m else ident_name(lbl)


PRESETS = {
    "1": dict(title="Newborn in an ordinary world",
              blurb="Born to a family of modest means. Every path is open and nothing is earned yet.",
              world="questions", society="", wealth=0.3, faith=None, upbringing="", start_age=0.0, place="town", setting="earth"),
    "2": dict(title="Raised devout in a traditional village",
              blurb="A close village that rewards order and tradition; the family faith expects duty and harmony.",
              world="questions", society="W.6 G.4", wealth=0.2, faith="W.6 G.4", upbringing="W.6 G.4", start_age=16.0, place="village", setting="earth"),
    "3": dict(title="A scholar's child in a city of learning",
              blurb="Books everywhere, a city that rewards study and invention. No family faith.",
              world="neutral", society="U.7 R.3", wealth=0.5, faith="none", upbringing="U.8 W.2", start_age=20.0, place="city", setting="earth"),
    "4": dict(title="Growing up on hard streets",
              blurb="Poor, a city where deals and nerve pay off. Family is loose; you learn to look after yourself.",
              world="questions", society="B.6 R.4", wealth=0.08, faith="none", upbringing="B.5 R.5", start_age=14.0, place="neighbourhood", setting="earth"),
    "5": dict(title="A child of the river clan (tribal)",
              blurb="A clan that lives by the river and the hunt. The elders keep the old ways, and everyone shares.",
              world="questions", society="G.5 W.3 R.2", wealth=0.2, faith="G.6 W.4", upbringing="G.6 W.4", start_age=0.0,
              place="river camp", setting="tribal"),
    "6": dict(title="Born under the spires (a world of magic)",
              blurb="A tower town of guilds, archives and old powers. Learning and cunning are prized; a gift may one day awaken.",
              world="pie", society="U.5 W.3 B.2", wealth=0.35, faith=None, upbringing="U.6 B.4", start_age=0.0,
              place="tower town", setting="magic"),
}


class Game:
    """One life. Drive it with advance() and decide(); read it with status() and the log."""

    def __init__(self, name="Ari", seed=1, world="neutral", society="", wealth=0.3, faith=None,
                 upbringing="", start_age=0.0, freq="normal", detail=1, years=80, place="town", setting="earth", sex=None,
                 pace=1.0, tech="modern", climate="middle", earlier=None, earlier_data=None, **_):
        self.name = name
        self.setting = setting if setting in SETTINGS else "earth"
        self.story = Story(name, seed, place, self.setting)   # the built-in narration (story.py)
        self.wv = WorldView(int(seed), self.setting, name, fig_own=GAME["fig_own"])     # the outer world's panel, circle, reach and story lines
        self.story.seen_as = lambda: self.gender_view()["seen_word"][2:] if self.loc is not None else "child"   # {seen_as} (N1d §3)
        self._epithet = ""
        self.ledger = False             # also show the numbers under the story (key l)
        self._voice_label = ""
        self.seed = int(seed)
        self.vrng = np.random.default_rng(self.seed + 7)   # picks among the Library's voice and lesson variants
        self.start_age = float(start_age)
        self.freq = freq
        self.detail = detail            # 0 quiet, 1 normal, 2 every week
        self.log = []                   # lines not yet shown
        self.feed = []                  # the same lines with a type and details, for the browser's HUD
        self.up_mix = mix(upbringing) if upbringing else None
        self.faith_mix = mix(faith) if faith not in (None, "none", "") else None
        P = dict(framing=WORLDS[world][1])
        if society:
            P["f_world"] = 0.25 * (mix(society) - 0.2) * 5 / 4      # the society rewards these ways of acting
            P["world_profile"] = 0.6 * np.full(C, 0.2) + 0.4 * mix(society)
        r0 = list(E.DEFAULT["res0"]); r0[0] = float(wealth); P["res0"] = tuple(r0)
        if faith == "none":
            P["faith_inherit"] = 0.0
        elif faith:
            P["faith_inherit"] = 1.0
        # the engine's next hand-off (point 11): sex from setup (None: the engine draws it); attraction and unease stay hidden
        # in the engine and come out only as the story finds them. The character's own death is off while the past is
        # simulated and in childhood, and on from the later of the start age and DEATH_FROM (see advance)
        # N1d: intersex reaches the engine once it knows it; until then the game draws the sex they are raised as (half
        # and half, from the seed) and keeps the birth itself on its side
        self.born_intersex = sex == "intersex"
        if self.born_intersex and not ENGINE_INTERSEX:
            sex = "female" if np.random.default_rng([int(seed), 91]).random() < 0.5 else "male"
        P["sex"] = sex if sex in ("female", "male", "intersex") else None
        P["self_death"] = False
        # the outer world (chroma-world/, approved 10-06 10:51; in the final version by Emren's 22:24 word): on wherever the
        # pinned engine has it, for Earth lives (presets 5 and 6 stay as they are, ruling R1); its seed is the life's
        # The setup's world inputs (release row W41; world-build.md): the history dial (pace 0.5 calm to 2 turbulent, only the
        # world's hazards), the technology level, the warming path; or an earlier world, the one a finished life left behind
        # (World.save() kept by the page), whose own settings and names go on. A grandchild's family line needs the
        # engine to read world_cfg["legacy"].
        if WORLD_ON and "world" in E.DEFAULT and setting == "earth":
            P["world"] = True
            P["world_cfg"] = dict(setting="earth", pace=float(min(2.0, max(0.5, float(pace or 1.0)))),
                                  tech_level=tech if tech in ("behind", "modern", "ahead") else "modern",
                                  climate=climate if climate in ("low", "middle", "high") else "middle")
            if earlier and earlier_data and earlier_data.get("key") == earlier.get("key"):
                import world as WM
                P["world_obj"] = WM.World.load(earlier_data["world"])
                self.wv.seed = int(earlier_data["world"]["seed"])          # the same world names the same people and places
                if earlier.get("grandchild") and earlier_data.get("people"):
                    P["world_cfg"]["legacy"] = earlier_data["people"]
            elif earlier:
                raise ValueError("the earlier world this life begins in is not in this browser")
        P.update({k_: v_ for k_, v_ in ENGINE_SET.items() if not k_.isupper()})   # checks only (CHROMA_ENGINE); empty in played lives
        self.sex = P["sex"] if P["sex"] != "intersex" else None
        self._named_seen = False                        # 'named their gender' already offered a new name
        self._death_on = False
        self.P = P
        self.setup = dict(setting=setting, world=world, society=society, wealth=wealth, faith=faith, upbringing=upbringing, start_age=start_age)
        self.L, world_mod = library_for(self.setting)
        self.batch = "COND" in self.L
        self.ORD = self.L["names"].index("an ordinary week") if "an ordinary week" in self.L["names"] else -1
        load_library_story(self.L["src"] if self.batch else [], getattr(world_mod, "EVENTS_READ", ()))
        # keys for the visuals thread's pictures and option icons (chroma-art/): the situation's name, life domain, tier and
        # tone, and each option's act tag
        self.sitmeta = {x["name"]: dict(life=x.get("life", ""), tier=x.get("tier", ""), tone=x.get("tone", ""), variant_of=x.get("variant_of", ""),
                                        tags=[str(o[4]) if len(o) > 4 and o[4] else "" for o in x.get("options", ())],
                                        marks=[str(o[5].get("mark", "")) if len(o) > 5 and isinstance(o[5], dict) else ""
                                               for o in x.get("options", ())])
                        for x in (self.L["src"] if self.batch else [])}
        self._gen = E.run_steps(N=1, years=years, seed=self.seed, P=P, intervention=self._intervene, lib=self.L,
                                log_lives=(0,))
        self._msg = next(self._gen)
        if self.batch and "alive" in self._msg[2]:     # the story's family matches the engine's
            al = self._msg[2]["alive"][0]
            self.story.set_family(int(al[1]), int(al[3]))
            WL0 = self._msg[2].get("WL")
            if WL0 is not None:                         # with the outer world on, the family and the birthplace are the world's
                try:
                    sib = [p_ for p_ in WL0.PP.cast_view(0) if "sibling" in p_.get("roles", [])]
                    self.story.world_siblings([("f" if p_.get("sex") == "female" else "m") for p_ in sib])
                    self._world_place(WL0, birth=True)
                except Exception:
                    pass
        self._last_read = -10 ** 6      # week an outside event read through their colors was last told
        self._read_told = {}            # outside event -> week it was last told
        self._role_told = {}            # title or perk -> week it was last told
        self._ev_i = 0
        self._last_cp = -10 ** 6
        self._last_seen = {}            # situation -> week it was last a checkpoint
        self._cp_n = {}                 # situation -> how many times it has been a checkpoint
        self._yr = dict(wound=0.0, support=0.0)   # v6: the year's hardest blow and the support then
        self._streak_t = -10 ** 6       # week a streak of trouble or fortune was last told
        self._after_t = -10 ** 6        # week the aftermath of a hard blow was last told
        self._last_line = {}            # situation -> week it was last told in the log
        self.burn_in = self.start_age > 0
        self._prev_label = ""
        self._wring = deque(maxlen=NAME_WEEKS)   # 5.5: the colors week by week over the last four years, their sum, and the
        self._wsum = np.zeros(C)                 # name they give (the settled core) and who they are becoming
        self._core_label = ""
        self._becoming_c = None; self._becoming = ""
        self._shown_label = None        # the identity last named in the yearly line
        self._named = set()             # identities whose meaning has been told once
        self._last_recon = {}           # commitment -> week it was last reconsidered at a checkpoint
        self._temper_told = None        # temperament when the log last mentioned it
        self._sh_told = {}              # item 2: each shadow state as the yearly chapter last told it (on or off)
        self.pending = None             # a checkpoint waiting for the player
        self._force = None              # this week's forced pick: dict(rel, closed, idx)
        self._cp_week = None            # the checkpoint being resolved this week, for its outcome line
        self.over = False
        self.result = None
        self.t = 0
        self.loc = None
        self.history = dict(content=[], peace=[], label=[], w=[], picks=0, own=0, forced=0, rel=[], gift=[], long=[],
                            accepted=0, resented=0, name=[],
                            met=[], title_say={}, acts=[])   # met: (age, kind, name) the first time, for the life told as one paragraph
        self.resolution = None          # v7: what came of the last choice, shown until the player goes on
        self._trace = []                # point 2 (Emren 20:39): the colors week by week, for the page's slow animation
        self._w_prev = None             # colors and means at the end of last week, for what a told act moved
        self._res_prev = None
        self.seen_labels = set()
        self.trust = np.zeros(C)        # the character's trust in the player, per color, -1 (resented) to 1 (trusted)
        # item 4: pivotal picks (GAME piv...): the season leans running (target shares, strength, start week), the picks'
        # recent ways for the plans they take up (5.4), and a random stream of the game's own (backfires)
        self._leans = []
        self._pick_mix = np.zeros(C); self._pick_wt = 0.0; self._pick_t = 0
        self._prng = np.random.default_rng(int(seed) + 5151)
        self.history["pivots"] = []     # (age, kind, colors before, target, size): kind own, toward, half or backfire
        # S2 (GAME own_...): how far each way the voice pushes toward has become theirs, the acts of this year by the color
        # leading their ways (for the fade), the season leans that no longer end (color -> (target, strength)), a random
        # stream of its own (reactance), and each step crossed (age, color, step) and bounce back (age, color, "back")
        self.ix = np.zeros(C); self._ix_use = np.zeros(C); self._own_leans = {}
        self._ixrng = np.random.default_rng(int(seed) + 6262)
        if GAME["own_ix"]:
            self.history["own_ix"] = []; self.history["rel_way"] = []
        self.history["voice"] = voice_empty()   # item 3: the voice in their head (chroma-ideas/voice-mechanics.md)
        self._voice_said = {}           # item 3: how often each kind of voice line was told (the second variant after the first)
        self._trust_side = np.zeros(C, int)     # trust per color past .5 (1) or -.5 (-1), for the turn lines
        self._vyear = dict(steer=0, won=0, turn=None)   # this year's pushes, the ones that worked, a trust turn
        self._vline_y = None            # the year of age of the last voice line in the story (one a year at most)
        self._vlast = {}                # color -> the last push mostly in that color (worked, the moment's name)
        self._w_start = None            # their colors when the player came in (what life and the voice moved since)
        self._name_mark = None          # colors and the voice's change when the name last changed (for "became")
        self.history["times"] = []      # WL5 (item 11): what the times did to them, by age (the World panel)
        self.history["steers"] = []     # P3: each push or lean, with the era's fit, for the World panel's timeline
        self._wyear = {}                # WL4: this year's world effects told, (kind, channel, dir) -> size in "big" units
        self._wfx_t = {}                # WL1: (kind, channel, dir) -> week last told
        self._price, self._price_t = 0.0, 0   # 5.6: the price of pushes against them, and when it was last added to
        self._turn_pick = None          # the turning point's answer, applied at the end of its week
        self.history["turns"] = []      # (age, color, kind, held)
        self._threads = {}              # F5: what a pick started (("r", title), ("c", commitment), ("g", goal id)) -> its cause
        self._last_pick = None
        try:                            # how many lives meet each moment (the Book's rarity), Modern Earth only
            from rarity import RARITY
            self._sit_share = (RARITY.get("sit") or {}) if self.setting == "earth" else {}
        except Exception:
            self._sit_share = {}
        self._need_hint = False         # the one-time hint about needs has been given

    # ------------------------------------------------------------------ engine callbacks
    def _intervene(self, t, P, nic, y):
        """Runs every week inside the engine: the family's values pull on a child's want until 15."""
        age = t / 52
        if t == 0 and self.up_mix is not None:
            nic[0] = 0.5 * nic[0] + 0.5 * self.up_mix                   # the family's surroundings
        if self.up_mix is not None and age < 15:
            y[0] += GAME["upbringing"] * E.centre(5 * (self.up_mix - E.softmax(y[0])))
        if age >= self.start_age:       # item 4: the player is here. The weeks without them weigh less; a pick week is whole
            P["own_k"] = P["drift_k"] = P["ev_push_k"] = GAME["quiet_k"]       # (decide sets them back to 1 for its week)
            if getattr(self, "_leans", None):   # F2: the picked ways lead their own acts for a season, fading
                yw = E.softmax(y[0])
                for T, st, t0 in self._leans:
                    f = 1 - (t - t0) / GAME["lean_weeks"]
                    if f > 0:
                        y[0] += GAME["lean"] * st * f * E.centre(5 * (T - yw))
                    elif GAME["own_ix"] and st > 0 and getattr(self, "ix", None) is not None and self.ix[int(np.argmax(T))] >= GAME["own_theirs"]:
                        self._own_leans[int(np.argmax(T))] = (T, st)       # S2: the way is theirs, so its lean stays
                self._leans = [x for x in self._leans if t - x[2] < GAME["lean_weeks"]]
            if getattr(self, "_own_leans", None):
                yw = E.softmax(y[0])
                for c in list(self._own_leans):
                    if self.ix[c] < GAME["own_theirs"]:
                        del self._own_leans[c]
                    else:
                        T, st = self._own_leans[c]
                        y[0] += GAME["lean"] * st * E.centre(5 * (T - yw))
        y[0] -= y[0].mean()

    # ------------------------------------------------------------------ main loop
    def age(self):
        return self.t / 52

    def advance(self, weeks=None, until_checkpoint=True, until_age=None):
        """Run the life forward. Stops at a checkpoint, after `weeks` weeks, at `until_age`, or at the end.
        Returns 'checkpoint', 'paused' or 'over'."""
        if self.pending is not None:
            return "checkpoint"
        if self.over:                                   # ended in the week of a choice (decide): nothing left to run
            return "over"
        stop_t = None if weeks is None else self.t + weeks
        while True:
            kind, t, loc, val = self._msg
            self.t = t; self.loc = loc; self.story.age = t / 52
            reply = None
            if kind == "week":
                if loc.get("WL") is not None:            # the engine's outer world (P["world"] on): the panel reads it, big news is told
                    if not isinstance(self.world_source, EngineWorld):
                        self.world_source = EngineWorld(self)
                    self._world_place(loc["WL"])
                    for r_ in self.world_source.news():
                        self._world_news(r_)
                if not self._death_on and t / 52 >= max(self.start_age, DEATH_FROM) and "P" in loc and "self_death" in loc["P"]:
                    loc["P"]["self_death"] = True; self._death_on = True      # the engine reads P live, week by week
                if self._death_on and "dead" in loc and bool(loc["dead"][0]):
                    return self._on_death(t, loc)
                if self.burn_in and t / 52 >= self.start_age:
                    self.burn_in = False
                    self._say(f"== {self.name} is {self.start_age:g} now. From here on, you are the voice in their head. ==", 0, "start")
                if stop_t is not None and t >= stop_t:
                    return "paused"
                if until_age is not None and t / 52 >= until_age:
                    return "paused"
                self._on_week(t, loc)
                w_ = E.softmax(loc["z"][0])
                self._name_week(w_, loc)
                if self._w_start is None and t / 52 >= self.start_age:
                    self._w_start = w_.copy()           # item 3: their colors when the player came in
                if len(self._trace) < 3000:              # E9: each week also its bands (in, fading, rising, out) and label
                    lb = self._core_label                # one rule everywhere: the label is the name (5.5), the identity of the
                    bd = "".join(b_[0] for b_ in X.bands(w_, lb)) if hasattr(X, "bands") else ""   # last four years' colors,
                    self._trace.append([int(t)] + [round(float(x), 4) for x in w_]                # as the HUD and the sheet
                                       + [round(float(x), 4) for x in E.softmax(loc["y"][0])] + [bd, lb])   # read it
            elif kind == "situation":
                self._title_now(loc)
                reply = val                             # the engine times life events itself since v6
            elif kind == "choose":
                self._title_now(loc)
                if t == 6 * 52:
                    self._family_faith(loc)
                cp = self._checkpoint(t, loc, val) if until_checkpoint and t / 52 >= self.start_age else None
                if cp is not None:
                    self.pending = cp
                    return "checkpoint"
                reply = val
            elif kind == "odds":
                reply = self._on_odds(loc, val)
            elif kind == "learn":
                reply = self._on_learn(loc, val)
            elif kind == "end":
                self._on_end(t, loc)
                if self.resolution is not None and self.resolution.get("new"):
                    self.resolution["new"] = False          # v7 (Emren 08:15): every choice gets its resolution
                    try:
                        self._msg = self._gen.send(None)
                    except StopIteration as e:
                        self.over = True; self.result = e.value
                        self._life_review()
                        return "over"
                    return "resolved"
            try:
                self._msg = self._gen.send(reply)
            except StopIteration as e:
                self.over = True; self.result = e.value
                self._life_review()
                return "over"

    def decide(self, pick=None, light=None):
        """Answer the pending checkpoint: an option index, or None to let the character choose; light, a color letter, tilts
        their own pick toward that color instead (P3)."""
        cp = self.pending
        assert cp is not None
        a = cp["a"]
        if cp.get("turning"):                           # 5.6: the engine's week goes on with their own pick; the answer is the game's
            if light:
                pick = next((o["idx"] for o in cp["options"] if o["colors"] == light), None)
            choice = cp["own"] if pick is None else int(pick)
            self._turn_pick = dict(cp=cp, choice=choice)
            self.history["picks"] += 1; self.history["own" if choice == cp["own"] else "forced"] += 1
            self.pending = None; self._last_cp = self.t
            try:
                self._msg = self._gen.send(a)
            except StopIteration as e:
                self.over = True; self.result = e.value
                self._life_review()
            return
        own = int(a[0])
        lt = None
        if light and pick is None and self.loc is not None:
            pick, lt = self._light_steer(self.loc, cp, light)
            self.history["light"] = self.history.get("light", 0) + 1
        if pick is None or pick == own:
            self._force = None
            choice = own
            self.history["own"] += 1
        else:
            o = cp["by_idx"][pick]             # by the engine's option number: options closed to this person leave gaps in the list
            rel = o["rel"] * (lt["share"] if lt else 1.0) * o.get("era_k", 1.0)   # P3: a light steer costs what it changed; the era
            self._force = dict(rel=rel, closed=o["status"] == "out of reach", idx=pick, acc=o.get("acc") or accept_word(o["rel"]),
                               trust=o.get("trust", 0.0), light=lt)
            a = a.copy(); a[0] = pick
            choice = pick
            self.history["forced"] += 1; self.history["rel"].append(rel)
            if GAME["own_ix"]:
                self.history["rel_way"].append([round(float(x), 3) for x in self._ways(self.loc, pick)] if self.loc is not None else None)
        self.history["picks"] += 1
        if choice != own or lt:                         # P3: the World panel's timeline shows each steer against the era
            o_ = cp["by_idx"].get(choice, {})
            self.history["steers"].append(dict(age=round(cp["age"], 2), kind="lean" if lt else "push", colors=o_.get("colors", ""),
                                               era=o_.get("era", 0.0), lean=(lt or {}).get("color", "")))
        g_ = self._gift_fit(cp["by_idx"].get(choice, {}))
        if g_ is not None:
            self.history["gift"].append(g_)
        self._cp_week = dict(cp=cp, choice=choice, own=own)
        if self.loc is not None and "P" in self.loc:   # item 4: the week of a pick counts whole (own lesson, drift, outside)
            self.loc["P"]["own_k"] = self.loc["P"]["drift_k"] = self.loc["P"]["ev_push_k"] = 1.0
        self.pending = None
        self._last_cp = self.t
        try:
            self._msg = self._gen.send(a)
        except StopIteration as e:                      # the life ends in the very week of the choice
            self.over = True; self.result = e.value
            self._life_review()

    def _light_steer(self, loc, cp, c):
        """P3: a light steer toward color c. Their own pick is drawn again with the steer added to each option's pull, as
        the engine's P["steer"] does before the draw (same formula; the moment is put to the player after the engine's
        draw, so the game draws it here). Returns the option and dict(color, share): the share of the drawn act's odds
        that the steer gave it, which is the share of a push's cost it carries."""
        P = loc["P"]; U = np.asarray(loc["U"][0], float); dn = np.asarray(loc["do_nothing"][0], bool)
        seen = np.asarray(loc["seen"][0], bool) & np.asarray(loc["mask"][0], bool)
        tau = float(P["tau0"] * (1 + 0.5 * float(loc["stress"][0])))
        m = np.asarray(loc["m"][0], float); mix = np.zeros(C); mix[COLORS.index(c)] = 1.0
        sU = np.where(dn, 0.0, GAME["light_k"] * (5 * (m @ mix) - 1))
        lg0 = np.where(seen, U / tau, -np.inf); lg1 = np.where(seen, (U + sU) / tau, -np.inf)
        p0 = np.exp(lg0 - lg0.max()); p0 /= p0.sum(); p1 = np.exp(lg1 - lg1.max()); p1 /= p1.sum()
        k = int((p1.cumsum() > self._prng.random()).argmax())
        if k not in cp["by_idx"]:
            return None, None
        share = float(np.clip(1 - p0[k] / max(p1[k], 1e-12), 0.0, 1.0))
        return k, dict(color=c, share=round(share, 3), moved=round(float(p1[k] - p0[k]), 3))

    def _era_fit(self, loc, T):
        """P3: how much an act's ways go with the era's pull (1) or against it (-1); 0 in quiet times. From the engine's
        STATE e_i (the era's strength) and e_p (its colors)."""
        if "e_p" not in loc or "e_i" not in loc:
            return 0.0
        ep = np.asarray(loc["e_p"], float).reshape(-1, C)[0] if np.size(loc["e_p"]) >= C else None
        ei = float(np.asarray(loc["e_i"], float).ravel()[0])
        if ep is None or ei <= 0:
            return 0.0
        a, b = np.asarray(T, float) - 0.2, ep - 0.2
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        return 0.0 if na < 1e-9 or nb < 1e-9 else float(np.dot(a, b) / (na * nb) * min(1.0, ei / GAME["era_full"]))

    def era_view(self, loc=None):
        """P3: the era's pull for the page: its colors as letters and shares, its strength 0 to 1."""
        loc = self.loc if loc is None else loc
        if loc is None or "e_p" not in loc or "e_i" not in loc or np.size(loc["e_p"]) < C:
            return None
        ep = np.asarray(loc["e_p"], float).reshape(-1, C)[0]; ei = float(np.asarray(loc["e_i"], float).ravel()[0])
        return dict(p=[round(float(x), 3) for x in ep], i=round(min(1.0, ei / GAME["era_full"]), 3), letters=letters(ep))

    # ------------------------------------------------------------------ checkpoints
    def _importance(self, loc, s, a):
        L = loc["L"]
        stakes = float(L["STAKES"][s])
        stage = int(loc["stage"][0])
        commit = bool((L["COMMIT"][s][loc["mask"][0]] >= 0).any())
        rite = stage < len(STAGES) - 1 and bool(L["RIT"][s, stage + 1])
        U_R, U_I = loc["U_R"][0], loc["U_I"][0]
        seen = loc["seen"][0] & ~loc["do_nothing"][0]
        conflict = seen.any() and int(np.argmax(np.where(seen, U_R, -np.inf))) != int(np.argmax(np.where(seen, U_I, -np.inf)))
        return stakes + 0.4 * commit + 0.3 * rite + 0.3 * conflict

    def _checkpoint(self, t, loc, a):
        recon = bool(loc["recon"][0])
        s = int(loc["s"][0])
        if s == self.ORD and not recon:
            return None
        gap_weeks, thr, again = FREQ[self.freq]
        if not recon and self._turn_due(t):
            return self._build_turning(t, loc, a)
        sea = None if recon else self.season(loc)
        if sea and sea["this_week"]:
            # Emren's point 6: a crossing is never a quiet level-up, so each of its season's moments (the crossing, the
            # in-between, settling in, and above all the transforming chance) is put to the player, whatever the pacing
            pass
        elif recon:
            # a commitment in a clash coming up for decision is always a moment for the player (Emren: clash endings
            # are checkpoints); a quieter reconsideration waits like any other moment. Neither repeats too soon.
            kk = int(loc["rk"][0])
            if t - self._last_recon.get(kk, -10 ** 6) < again // 2:
                return None
            if loc["clash0"][0, kk] < 0 and t - self._last_cp < gap_weeks:
                return None
            self._last_recon[kk] = t
        else:
            # v6: life events are rare and come at real rates, so they are the big moments to offer the player; everyday
            # situations fill most weeks, and each one waits longer every time it has been a checkpoint (variety)
            life = "had_ev" in loc and bool(loc["had_ev"][0]) and int(loc["s_ev"][0]) == s
            if t - self._last_cp < (gap_weeks // 2 if life else gap_weeks):
                return None
            wait = (again // 2) * self._cp_n.get(s, 0) if life else again * (1 + self._cp_n.get(s, 0))
            if t - self._last_seen.get(s, -10 ** 6) < wait:
                return None
            tied, cause = self._thread_of(loc, s) if t / 52 >= self.start_age else (True, None)
            if (not tied and not life and thr > 0
                    and (self._sit_share.get(self.L["names"][s]) or 0.0) >= GAME["told_share"]):
                return None                     # 5.6: an everyday moment with no tie to this life is told, not asked
            if (self._importance(loc, s, a) + (0.5 if life else 0.0) + GAME["tie_imp"] * tied
                    + GAME["tie_pick"] * (cause is not None) < thr):
                return None
        self._last_seen[s] = t
        self._cp_n[s] = self._cp_n.get(s, 0) + 1
        return self._build_checkpoint(t, loc, a)

    @staticmethod
    def _colors(loc, k):
        """An option's colors: its ways, and the end they serve when that differs ('W>U': White means for a Blue end)."""
        means = letters(loc["m"][0, k])
        e = np.maximum(loc["e0"][0, k], 0) if "e0" in loc else None
        ends = letters(e) if e is not None and e.sum() > 0 else means
        return means if ends == means else f"{means}>{ends}"

    @staticmethod
    def _kills(L, s):
        """The role who dies in this moment (the Library's kills: field), or None."""
        k = int(L["KILLS"][s]) if "KILLS" in L else -1
        return E.ROLES[k] if k >= 0 else None

    def _true_odds(self, loc, k):
        P, L = loc["P"], loc["L"]
        m = loc["m"][0, k]; alpha = loc["alpha"][0]
        fit = P["fit"] * (m * (alpha - alpha.mean())).sum()
        pb = loc.get("pbump")                       # perks that help acts in their ways (logit units, as the engine adds them)
        pb = float(pb[0, k]) if np.ndim(pb) == 2 else 0.0
        return float(1 / (1 + np.exp(-P["gain"] * ((m * (loc["sig"][0] + loc["f_tot"][0])).sum() + fit - loc["diff"][0, k]) - pb)))

    def _build_checkpoint(self, t, loc, a):
        L = loc["L"]; s = int(loc["s"][0])
        mask = loc["mask"][0]; seen = loc["seen"][0]; open_ = loc["open_"][0]
        open_r = loc["open_r"][0]; dn = loc["do_nothing"][0]
        U = loc["U"][0]; pr = loc["pr"][0]; p_hat = loc["p_hat"][0]
        own = int(a[0])
        recon = bool(loc["recon"][0])
        seen_k = [k for k in range(len(mask)) if mask[k] and seen[k] and not (recon and k > 3)]
        Ubest = max([float(U[own])] + [float(U[k]) for k in seen_k])         # the best they see, not the sampled pick
        u_dn = max([float(U[k]) for k in range(len(mask)) if mask[k] and dn[k]] or [-np.inf])
        gaps = [Ubest - float(U[k]) for k in seen_k if k != own and not dn[k]]
        ref = max(GAME["rel_ref"], float(np.median(gaps)) if gaps else 0.0)       # this moment's typical gap
        labels = L["labels"][s]
        opts = []
        for k in range(len(mask)):
            if not mask[k]:
                continue
            if recon and k > 3:
                continue
            if dn[k]:
                status = "considered"
            elif seen[k]:
                status = "considered"
            elif open_[k]:
                status = "didn't think of it"
            else:
                status = "out of reach"
            why = ""
            if status == "out of reach":
                req = L["REQ"][s, k]; res = loc["res"][0]
                lack = [RNAMES[j] for j in range(len(req)) if req[j] > 0 and res[j] < req[j]]
                why = "lacks " + ", ".join(lack) if (lack and not open_r[k]) else "not on offer around them"
            clash = [] if dn[k] else clash_with(self._colors(loc, k), self._prev_label)
            rel = 0.0 if k == own else reluctance(Ubest - float(U[k]), ref, u_dn - float(U[k]), bool(clash)) * self._own_k(loc, k)
            pt = self._true_odds(loc, k); pt0 = pt
            if k != own:
                lg = np.log(pt / (1 - pt)) - GAME["effort"] * rel - (GAME["out_of_reach"] if status == "out of reach" else 0)
                pt = float(1 / (1 + np.exp(-lg)))
            ph = float(p_hat[k])
            label = labels[k].replace("{title}", getattr(self.story, "title_now", None) or "their role")
            if recon:
                kk = int(loc["rk"][0]); label = re.sub(r"\bit\b", f"the {KNAMES[kk]}", label, count=1)
            commit = int(L["COMMIT"][s, k])
            opts.append(dict(idx=k, label=label, colors=self._colors(loc, k) if not dn[k] else "-",
                             felt=ph, true=pt, hint=hint(pt - ph) if not dn[k] else "",
                             lean=float(pr[k]) if np.isfinite(pr[k]) else 0.0,
                             rel=rel, status=status, why=why, gap=Ubest - float(U[k]), span=Ubest - u_dn, clash=clash, true0=pt0,
                             acc="their own pick" if k == own else accept_word(rel), trust=self._trust_on(loc, k),
                             commit=KNAMES[commit] if commit >= 0 and not loc["held"][0, commit] else None,
                             follows=self._follows(loc, s, k, ph, commit, recon)))
        title = L["names"][s]
        extra = ""
        kind = None
        if recon:
            kk = int(loc["rk"][0]); kind = KNAMES[kk]
            held_y = (t - loc["since"][0, kk]) / 52
            title = f"reconsidering their {kind}"
            asks = " and ".join(ADJ[c] for c in letters(loc["prof"][0, kk]).split("+"))
            wants = " and ".join(ADJ[c] for c in letters(E.softmax(loc["y"][0])).split("+"))
            extra = self.story.recon_note(kind, held_y, asks, wants)
            if self.ledger:
                extra += (f" [invested {loc['I'][0, kk]:.2f}; expects {letters(loc['prof'][0, kk])}, "
                          f"wants {letters(E.softmax(loc['y'][0]))}]")
        # the scene, and what the character thinks about the act they lean toward
        m = self.story.moment(t, L["names"][s], int(loc["stage"][0]), t / 52, kind, self._kills(L, s))
        self._far_moment(m, loc, s)                     # far_ties: the far moment's tie, town and event (Library slots)
        self._social_slots(m, loc, s)                   # v22.4: the places, post or price the moment is about
        if m["ctx"].get("_social"):                     # and its options' own slots, as its scene fills them
            for o in opts:
                o["label"] = self.story.slots_in(o["label"], m)
        try:
            sr = self._seen_rows(loc, s)                # S6: "seen it done" on the option row
        except Exception:
            sr = None
        for o in opts if sr else ():
            if o["idx"] in sr and o["colors"] != "-":   # never on doing nothing
                o["seen"] = sr[o["idx"]]
        lean = next((o for o in opts if o["idx"] == own), None)
        thought = ""
        if lean is not None and lean["colors"] != "-":
            thought = self.story.reason(lean["colors"].replace("+", "")) + " " + self.story.confidence(lean["felt"])
        elif lean is not None:
            thought = self.story.thought("Not now. Let it be.", "wait", "")
        mm = np.maximum(np.asarray(loc["m"][0], float), 0)
        oc = loc.get("option_causes"); causes = oc(0) if callable(oc) else None
        for o in opts:                                  # P3: steering with the era's pull costs less, against it more
            fit = self._era_fit(loc, mm[o["idx"]] / mm[o["idx"]].sum()) if mm[o["idx"]].sum() > 0 else 0.0
            o["era"] = round(fit, 2); o["era_k"] = float(np.clip(1 - GAME["era_cost"] * fit, 0.5, 1.5))
            if causes and o["idx"] < len(causes) and causes[o["idx"]]:
                o["wcause"] = self._option_cause(causes[o["idx"]])   # WL3: the world closes it, or makes it harder or easier
        cp = dict(t=t, age=t / 52, title=title, extra=extra, stakes=float(L["STAKES"][s]), recon=recon, s=s, sit=L["names"][s],
                  scene=self.story.scene(m), thought=thought, moment=m,
                  options=sorted(opts, key=lambda o: o["idx"]), own=own, a=a.copy(), by_idx={o["idx"]: o for o in opts})
        if not recon and t / 52 >= self.start_age:      # F5: a moment that follows from a pick of theirs says so
            _, cause = self._thread_of(loc, s)
            if cause is not None:
                cp["thread"] = self._thread_line(cause, t / 52); cause["told"] = int(t)   # each thread told once in a while
        b = X.say(X.before(loc, 0, rng=self.vrng), self.name)
        cp["snap"] = X.snapshot(loc, 0, b)
        cp["view"] = self._view(loc, b, cp)
        return cp

    # ------------------------------------------------------------------ v7: the character's view, and what came of it
    def _goal_words(self, loc, text):
        """The engine's default goal names ("the plan (B W)") in the story's words."""
        if not text or "gk" not in loc or "the " not in text:
            return text
        for j in np.nonzero(loc["gk"][0] >= 0)[0]:
            raw = X.goal_name(loc, 0, j)
            if raw in text:
                kind = E.G_KINDS[int(loc["gk"][0, j])]; d = int(loc["gd"][0, j])
                hz = E.HORIZONS[int(loc["ghz"][0, j])] if kind == "plan" and "ghz" in loc else ""
                text = text.replace(raw, self.story.name_goal(raw, kind, KNAMES[d] if d >= 0 else "", loc["gm"][0, j], int(loc["gid"][0, j]), hz))
        return text

    def _view(self, loc, b, cp):
        """explain.before(), joined to the checkpoint's options: the heart's and the head's share of each, the reality
        hint (a band of words; the game's own odds, which include the cost of a push), and the inner voice in story words."""
        raw = {o["k"]: o for o in b["options"]}
        L = loc["L"]; s = int(loc["s"][0])
        rename = []
        for o in cp["options"]:
            e = raw.get(o["idx"], {})
            o["kind"] = e.get("kind", "")
            acc = e.get("accept")
            if acc and o["idx"] != cp["own"]:          # the engine's word and the cost of forcing it
                o["acc"] = ACC_FROM_ENGINE.get(acc["level"], acc["level"]); o["rel"] = float(acc["reluctance"])
                kx = self._own_k(loc, o["idx"])
                if kx < 1.0:                            # S2: a way that has become theirs costs less to be pushed into
                    o["rel"] *= kx; o["acc"] = accept_word(o["rel"])
                o["acc_clash"] = float(acc["clash"])
                if o["acc"] not in ("reluctant", "against it"):
                    o["clash"] = []
                pt = o["true0"]
                lg = np.log(pt / (1 - pt)) - GAME["effort"] * o["rel"] - (GAME["out_of_reach"] if o["status"] == "out of reach" else 0)
                o["true"] = float(1 / (1 + np.exp(-lg)))
                if o["colors"] != "-":
                    o["hint"] = hint(o["true"] - o["felt"])
            if e.get("needs"):                          # titles and perks: what it needs, which perks help it, what it gives or takes
                o["needs"] = self._role_need(e["needs"]); o["closed"] = e.get("closed")
            GR = L.get("ROLES")
            if e.get("helped_by") and GR is not None:
                o["helped"] = [role_info(GR, GR["ID"][nm]) for nm in e["helped_by"] if nm in GR["ID"]]
            lv = lever_info(e.get("lever") or (L["LEVER"][s][o["idx"]] if "LEVER" in L else None),
                            e.get("target") or (L["TARGET"][s][o["idx"]] if "TARGET" in L else None))
            if lv:                                      # spec 7: the lever an act on the outer world uses, and its target
                o["lever"] = lv
            o["roles_fx"] = self._role_fx(loc, s, o["idx"])
            if any(d["when"] == "ok" and d["gain"] and d.get("title") for d in o["roles_fx"]):
                o["rung"] = self._rung_below(loc, s)    # the step they stand on, for a long shot's climb
            if e.get("base") is not None:               # the Library's chance: how often it works for most people at these ages
                o["base"] = float(e["base"])
            if o["label"] != L["labels"][s][o["idx"]]:
                rename.append((L["labels"][s][o["idx"]], o["label"]))
            if e.get("felt") is None:
                continue
            # the engine's reality hint is for the act as the character would do it; a push costs effort on top (rel)
            o["reality"] = dict(e["reality"], why=self._goal_words(loc, e["reality"]["why"]))
            o["heart"], o["head"] = e["heart"], e["head"]
            o["drivers"] = {k: [[DRIVER_WORD.get(nm, nm), round(v, 3)] for nm, v in e["drivers"][k]] for k in ("heart", "head")}
        ins = b["insight"]
        line = self._goal_words(loc, ins["line"])
        for a_, b_ in rename:
            line = line.replace(a_, b_)
        asides = [self.story.aside(x["key"], self._goal_words(loc, x["line"])) for x in b["asides"]]
        own, heart, head = cp["own"], b["heart"], b["head"]
        if heart >= 0 and own not in (heart, head) and own in cp["by_idx"]:
            asides.append(self.story.aside("lean_other", "Yet when it comes to it, {N} leans toward “" + cp["by_idx"][own]["label"] + "”."))
        return dict(key=ins["key"], line=self.story.insight(ins["key"], line, ins["heart_driver"], ins["head_driver"], b["self_control"]),
                    asides=asides, heart=heart, head=head, self_control=b["self_control"], voice_color=b["voice_color"],
                    heart_driver=DRIVER_WORD.get(ins["heart_driver"], ins["heart_driver"]),
                    head_driver=DRIVER_WORD.get(ins["head_driver"], ins["head_driver"]))

    def _resolution(self, loc, cpw, ev, text, o, pushed, rel, moved):
        """explain.after() for the choice just made: what happened, what changed in the person and around them, who it
        touched, what they are moving toward, and how the world works, as this week showed it."""
        r = X.say(X.after(cpw["cp"]["snap"], loc, 0, rng=self.vrng), self.name)
        def word(c):
            w = re.sub(r" in ([WUBRG]) ways", lambda m_: f" in {CNAME[m_.group(1)]} ways", c["word"])
            return dict(what=c["what"], word=w, delta=c["delta"], size=c["size"])
        changes = [word(c) for c in r["changes"] if c["size"] >= 0.5 and c["word"]][:9]
        became = [c for c in changes if c["size"] >= 1][:3]
        a = r["act"]
        res = dict(age=round(self.t / 52, 1), title=cpw["cp"]["title"], act=o["label"], colors=o["colors"], worked=bool(a["worked"]),
                   surprise=a["surprise"], felt=round(float(a["felt"]), 2), pushed=pushed, rel=round(rel, 2),
                   with_heart=bool(a.get("with_heart")), with_head=bool(a.get("with_head")), regret=bool(a.get("regret")),
                   text=text, changes=changes, became=became,
                   push=[dict(why=k, color=v["color"], dir=v["dir"]) for k, v in r["color_push"].items() if v["size"] >= 1][:3],
                   closer=dict(r["identity"]["closer_to"], guild=ident_name(r["identity"]["closer_to"]["identity"])) if r["identity"]["closer_to"] else None,
                   identity=dict(before=r["identity"]["before"], now=r["identity"]["now"], guild=ident_name(r["identity"]["now"])),
                   lessons=[dict(key=l_["key"], line=self._goal_words(loc, l_["line"])) for l_ in r["lessons"]],
                   events=r["events"], people=sorted({int(x) for x in re.findall(r"⟦p:(\d+)⟧", text)}),
                   states=[dict(word=e_["say"], what=e_["what"], good=ADJ_LOOK.get(e_["name"], ("", 0))[1],
                                icon=ADJ_LOOK.get(e_["name"], ("dot", 0))[0]) for e_ in r["events"] if e_.get("kind") == "state"],
                   roles=self._res_roles(loc, r["events"]),
                   dw=moved.get("dw"), dres=moved.get("dres"), new=True)
        wp = push_words(r.get("world_push") or a.get("world_push"))
        if wp:                                          # spec 7 §3: what a push on the outer world did
            res["world_push"] = wp
        ls = self._long_shot(o)
        if ls:                                          # a title reached for against long odds: kept, made or missed
            ls.update(made=bool(a["worked"]), age=res["age"], moment=res["title"],
                      tries=self._tries(ls["name"]))
            ls["words"] = long_shot_words(ls)
            self.history["long"].append(ls); res["long_shot"] = ls
        gv = self.gender_view(loc)
        cw = a.get("cross", o.get("cross"))            # the engine's crossing weight on the act (for-the-engine.md §6)
        if cw is None and loc is not None and "act_cw" in loc:
            cw = float(np.ravel(loc["act_cw"])[0])
        if cw and float(cw) > 0 and gv["strict"] >= 0.4:   # one short line of felt pressure; nothing where the world is loose
            res["pressure"] = self.story.rng.choice(PRESSURE.get(self.setting, PRESSURE["earth"])).replace("{N}", self.name)
        if gv["named"] and not self._named_seen:       # they named their gender: a new name, if they want one
            self._named_seen = True
            res["rename"] = dict(old=self.name, suggest=self.story._name(gv["own"] if gv["own"] in ("f", "m", "x") else "x"))
        res["say"] = self.story.resolution(res)
        return clean(res)

    def _needs_moved(self, loc, snap):
        """Every need that moved this week, from just before the choice to the end of the week (IDEAS.md, "Make needs
        visible", fix 2), with its level in the sheet's words."""
        if "need" not in loc or snap.get("need") is None:
            return []
        before = np.asarray(snap["need"], float); after = np.asarray(loc["need"][0], float)
        out = []
        for j, nm in enumerate(E.NEEDS):
            d = float(after[j] - before[j])
            if abs(d) < 0.01:                            # a point or more, so the shown percentages differ
                continue
            out.append(dict(need=nm, before=round(float(before[j]), 3), after=round(float(after[j]), 3), delta=round(d, 3),
                            lacking=bool(before[j] < GAME["need_thin"]), word=need_level_word(float(after[j]))))
        return sorted(out, key=lambda x: -abs(x["delta"]))

    def _hindsight(self, loc, cpw, worked, needs):
        """The character judges the push just made (IDEAS.md, "Player intervention that helps"), if they were at least
        reluctant about it ("okay with it" costs nothing, so there is nothing to look back on). Accepted: it worked and
        fed a need they lacked; part of its costs is undone and trust grows along the act's colors. Resented: it failed,
        or it worked but fed nothing they lacked while they were reluctant; trust falls, and a failure adds wanting.
        Otherwise it passes without a judgment. Changes the engine's state in place, as the forced-pick costs do."""
        f = self._force or {}
        rel = float(f.get("rel", 0.0)); rs = float(f.get("resent", rel))
        prof = self._profile(loc, cpw["choice"])
        # what the act gave to needs they lacked: its ends' share of the engine's refill, read at the moment (follows
        # "lift"); one act lifts a need by about a point, which the week's drain and other events can hide in the totals
        lift = (cpw["cp"]["by_idx"].get(cpw["choice"], {}).get("follows") or {}).get("lift") or []
        gain = sum(x["gain"] for x in lift)
        fed = lift[0] if lift else None
        out = dict(kind="none", share=0.0, need=fed["need"] if fed else None, trust_before=round(self._trust_on(loc, cpw["choice"]), 3))
        if rel < GAME["hind_rel"]:                          # they were fine with it: nothing to look back on
            pass
        elif worked and gain >= GAME["hind_min"]:
            share = GAME["hind_max"] * min(1.0, gain / GAME["hind_full"])
            loc["stress"][0] = max(0.0, float(loc["stress"][0]) - share * GAME["stress"] * rs)
            loc["Q"][0] = max(0.0, float(loc["Q"][0]) - share * GAME["backlash"] * rs)
            aut = E.NEEDS.index("autonomy")
            lost = next((-x["delta"] for x in needs if x["need"] == "autonomy" and x["delta"] < 0), 0.0)
            if lost > 0:
                loc["need"][0, aut] += share * lost
            if self.history["rel"]:
                self.history["rel"][-1] *= 1 - share           # a push they came to own counts less against "their own"
            self.trust += GAME["trust_gain"] * share / GAME["hind_max"] * prof * (1 - self.trust)
            self.history["accepted"] += 1
            out.update(kind="accepted", share=round(share, 3))
        elif rel >= 0.3 and (not worked or gain < GAME["hind_min"]):
            if not worked:
                loc["Q"][0] += GAME["resent_more"] * GAME["backlash"] * rs
            self.trust -= GAME["trust_loss"] * rel * prof * (1 + self.trust)
            self.history["resented"] += 1
            out.update(kind="resented", share=round(rel, 3))
        if out["kind"] == "none" and GAME["trust_judge"]:   # item 7: an unjudged push still moves trust by how it went
            st = (GAME["judge_a"] + GAME["judge_b"] * rel) * prof
            self.trust += st * (1 - self.trust) if worked else -st * (1 + self.trust)
            out["judged"] = "worked" if worked else "failed"
        self.trust = np.clip(self.trust, -1.0, 1.0)
        out["trust_after"] = round(self._trust_on(loc, cpw["choice"]), 3)
        out["line"] = self.story.hindsight(out["kind"], NEED_WORD.get(out["need"], out["need"] or ""), worked)
        return out

    def _pivot(self, loc, cpw, worked, hind):
        """Item 4: the pick at a moment put to the player is a turning point (GAME piv...). It moves the colors, and part of
        the deep core, toward the picked ways (or toward what they wanted, on a backfire) and starts the season lean (F2).
        Changes the engine's state in place at the week's end, as the forced-pick costs do."""
        k, own = int(cpw["choice"]), int(cpw["own"])
        m = np.maximum(np.asarray(loc["m"][0], float), 0)
        if m[k].sum() <= 0:                                  # doing nothing teaches nothing about their ways
            return None
        T = m[k] / m[k].sum()
        w = E.softmax(loc["z"][0]); dist = float(0.5 * np.abs(T - w).sum())
        stakes = float(loc["L"]["STAKES"][int(loc["s"][0])])
        judged = (hind or {}).get("kind")
        kind, share, lean = ("own", GAME["piv_own"], GAME["piv_own"]) if k == own else ("toward", 1.0, 1.0)
        if k != own and (not worked or judged == "resented"):
            kind, share, lean = "half", GAME["piv_fail"], 0.5
            if not worked and (judged == "resented" or self._prng.random() < min(0.8, GAME["backfire"] * dist * stakes)):
                if m[own].sum() > 0:                         # it backfires: they learn toward what they wanted instead
                    kind, share, lean, T = "backfire", 1.0, 0.0, m[own] / m[own].sum()
        size = share * (1 + GAME["piv_far"] * dist)
        plast = float(loc["plast"][0]) if "plast" in loc else 0.2
        dz = GAME["piv"] * plast * size * E.centre(5 * (T - w))
        loc["z"][0] += dz
        if "k" in loc:
            loc["k"][0] += GAME["piv_core"] * dz
            if kind == "own":                                # letting them choose steadies them
                loc["k"][0] += GAME["piv_steady"] * (loc["z"][0] - loc["k"][0])
        if lean:
            self._leans.append((T, lean, int(self.t)))
            dec = 0.5 ** ((self.t - self._pick_t) / GAME["pick_half"])
            self._pick_mix = self._pick_mix * dec + lean * T; self._pick_wt = self._pick_wt * dec + lean; self._pick_t = int(self.t)
        self.history["pivots"].append((round(self.t / 52, 1), kind, [round(float(x), 3) for x in w],
                                       [round(float(x), 3) for x in T], round(size, 3)))
        return dict(kind=kind, size=round(size, 3), toward=letters(T), dist=round(dist, 3),
                    moved=[round(float(x) * 100, 2) for x in E.softmax(loc["z"][0]) - w])

    def _plan_lean(self, loc, g):
        """Item 4, 5.4: a plan they take up leans toward the ways of their recent picks (GAME plan_lean), so a few picks can
        shape a decade. Changes the new plan's colors in place (and the moments that offer it a step)."""
        if g.get("kind") != "plan" or g.get("what") != "begins" or g.get("by_player") or self._pick_wt <= 0 or "gid" not in loc:
            return
        js = np.nonzero(loc["gid"][0] == int(g.get("id", -1)))[0]
        if not len(js):
            return
        j = int(js[0])
        wt = self._pick_wt * 0.5 ** ((self.t - self._pick_t) / GAME["pick_half"])
        lam = GAME["plan_lean"] * min(1.0, wt)
        if lam < 0.02:
            return
        mix = (1 - lam) * np.asarray(loc["gm"][0, j], float) + lam * self._pick_mix / max(self._pick_wt, 1e-9)
        loc["gm"][0, j] = mix / mix.sum()
        if callable(loc.get("goal_rel_S")) and "gsr" in loc:
            loc["gsr"][0, j] = loc["goal_rel_S"](loc["gm"][0, j], int(loc["gd"][0, j]))
        g["mix"] = loc["gm"][0, j].round(2).tolist(); g["led"] = round(lam, 2)

    def _mark_threads(self, cpw, new, GR, age):
        """F5 (item 4, gameplay-feel.md 5.3): what this week's pick started (a title or perk, a commitment, a plan or
        dream of their own) becomes a thread; later moments that follow from it say so, the pick on hover."""
        o = cpw["cp"]["by_idx"][cpw["choice"]]
        if o["colors"] == "-":                           # waiting starts no thread
            return
        cause = dict(age=int(age), t=int(self.t), act=o["label"], moment=cpw["cp"]["title"], pushed=cpw["choice"] != cpw["own"])
        self._last_pick = cause
        for ev in new:
            r, c, g = ev.get("role"), ev.get("commitment"), ev.get("goal")
            if r and r["what"] == "gained" and GR is not None and r["name"] in GR["ID"] and GR["ID"][r["name"]] < GR["NT"]:
                d = role_info(GR, GR["ID"][r["name"]])
                self._threads[("r", d["i"])] = dict(cause, key="title", title=d["say"], what="they became " + d["say"])
            elif c and c["what"] == "start":
                self._threads[("c", c["kind"])] = dict(cause, key="commitment", kind=c["kind"],
                                                       what=THREAD_COMMIT.get(c["kind"], "a commitment began"))
            elif g and g.get("what") == "begins" and g.get("kind") in THREAD_GOAL:
                gid = int(g.get("id", -1))
                nm = (self.story.dreams.get(gid) or {}).get("name", "") if g["kind"] != "plan" else ""
                self._threads[("g", gid)] = dict(cause, key="plan" if g["kind"] == "plan" else "dream", goal=nm, what=THREAD_GOAL[g["kind"]])

    # ------------------------------------------------------------------ 5.6: the price builds to a turning point
    def _price_now(self):
        return self._price * 0.5 ** ((self.t - self._price_t) / GAME["turn_half"])

    def _turn_due(self, t):
        if EP is None or self.setting != "earth" or t / 52 < max(self.start_age, 14) or len(self.history["turns"]) >= GAME["turn_max"]:
            return False
        last = self.history["turns"][-1]["t"] if self.history["turns"] else -10 ** 6
        return t - last >= GAME["turn_gap"] and t - self._last_cp >= FREQ[self.freq][0] // 2 and self._price_now() >= GAME["turn_line"]

    def _build_turning(self, t, loc, a):
        """5.6: "the day it all comes to a head" (Library earth_play.py), built by the game: five one-color options, their
        own pick the option of their lead color. The engine's moment this week goes on as their own."""
        S = EP.SITUATIONS[0]
        w = E.softmax(loc["z"][0]); lead = COLORS[int(np.argmax(w))]
        opts = []
        for i, (label, means, _e, _d, _t, x) in enumerate(S["options"]):
            c = means[0]
            opts.append(dict(idx=i, label=label, colors=c, felt=float(x.get("chance", 0.55)), hint="", lean=0.0, status="open",
                             rel=0.0 if c == lead else 0.3, why="", commit=None, follows={}, kind="", act=x.get("act", label),
                             acc="their own pick" if c == lead else "okay with it", trust=float(self.trust[COLORS.index(c)]),
                             era=0.0))
        own = next(o["idx"] for o in opts if o["colors"] == lead)
        sc = dict((c_, x_) for c_, x_ in S["scenes"]["earth"])
        cp = dict(t=t, age=t / 52, title=S["name"], extra="", stakes=float(S["stakes"]), recon=False, s=int(loc["s"][0]), sit=S["name"],
                  scene=self.story.fill(sc.get(lead) or sc.get("", "")), thought="", moment=None, options=opts, own=own, a=a.copy(),
                  by_idx={o["idx"]: o for o in opts}, turning=True)
        return cp

    def _turning_end(self, t, loc, tp):
        """5.6: the turning point's pick, at the end of its week: a lesson turn_piv times a pick's toward the chosen color,
        half of it into the deep core; held (the option's chance, more for their own lead), the strain and the pent-up
        wanting are let go and the new way leads their acts for a year; broken, a little of it stays."""
        cp, k = tp["cp"], tp["choice"]
        o = cp["by_idx"][k]; c = o["colors"]; ci = COLORS.index(c)
        w = E.softmax(loc["z"][0]); lead = cp["by_idx"][cp["own"]]["colors"]
        d = np.asarray(self.history["voice"]["d"], float)
        pushed = COLORS[int(np.argmax(d))] if d.max() > 0 else None
        kind = "snap back" if c == lead else "reinvention" if c == pushed else "turn"
        held = bool(self._prng.random() < min(0.9, o["felt"] + (0.2 if c == lead else 0.0)))
        T = np.full(C, 0.1); T[ci] = 0.6
        plast = float(loc["plast"][0]) if "plast" in loc else 0.2
        dz = GAME["piv"] * GAME["turn_piv"] * plast * (1.0 if held else 0.4) * E.centre(5 * (T - w))
        loc["z"][0] += dz
        if "k" in loc:
            loc["k"][0] += (0.5 if held else 0.15) * dz
        if held:
            loc["stress"][0] *= 0.5; loc["Q"][0] *= 0.3
            self._leans.append((T, 1.0, int(t))); self._leans.append((T, 1.0, int(t) + GAME["lean_weeks"]))
        self._price, self._price_t = 0.0, int(t)
        self.history["turns"].append(dict(t=int(t), age=round(t / 52, 1), color=c, kind=kind, held=held))
        outs = EP.SITUATIONS[0]["outcomes"][0 if held else 1]
        line = self.story.fill("{N} decides " + chooses(act(o["act"])) + ". " + outs[len(self.history["turns"]) % len(outs)])
        self._say(mk("T", f"{c}|{kind}|{int(held)}", line), 0, "turning", color=c, kind=kind, held=held)

    # ------------------------------------------------------------------ item 11: the world in their life (WL1, WL3 to WL6)
    @staticmethod
    def _wband(ch, size):
        """WL1's bands (the Library's proposal, set here): None (not told), "small" or "big"."""
        size = abs(float(size))
        if ch == "option":
            return "big"
        lo, hi = WFX_BAND.get(ch, WFX_BAND["risk"] if ch.endswith("risk") else (None, None))
        if lo is None or size < lo:
            return None
        return "big" if size >= hi else "small"

    @staticmethod
    def _wcause_text(c, kind):
        """A world effect's cause in plain words, for the hover: "the recession, since 34"."""
        if not c:
            return WFX_KIND.get(kind, kind)
        ck = c.get("kind")
        key = c.get("key")
        nm = (f"the {key}" if key and ck == "arrives" else key) or WFX_CAUSE.get(ck) or WFX_KIND.get(ck) or WFX_KIND.get(kind, kind)
        return str(nm) + (f", since {int(c['age'])}" if c.get("age") is not None else "")

    def _world_effects(self, t, loc):
        """WL1 and WL5 (item 11, world-in-life.md): when the engine reports that a world event changed something of theirs
        (STATE wfx: money, freedom, safety, a risk, a close person, their town), one small line sized to the change, the
        cause on hover; the same kind of line not again within a year. Each told effect goes into the life's record of what
        the times did (the World panel) and the year's line (WL4)."""
        if ES is None or "wfx" not in loc:
            return
        W = loc["wfx"]
        xs = W[0] if len(W) and isinstance(W[0], (list, tuple)) else W
        for e in xs or []:
            ch, kind, d = e.get("channel", ""), e.get("kind", ""), e.get("dir", "up")
            band = self._wband(ch, e.get("size", 0))
            if band is None or ch == "moment":
                continue
            k = WFX_KIND_LIB.get(kind, kind)
            line = ((ES.WORLD.get(k) or {}).get(ch) or {}).get(d, {}).get(band) or (ES.WORLD_CHANNEL.get(ch) or {}).get(d, {}).get(band)
            if not line:
                continue
            key = (kind, ch, d)
            yk = abs(float(e.get("size", 0))) / (WFX_BAND.get(ch, WFX_BAND["risk"])[1] if ch != "option" else 1.0)
            self._wyear[key] = self._wyear.get(key, 0.0) + min(yk, 2.0)
            if t - self._wfx_t.get(key, -10 ** 6) < WFX_AGAIN:     # counted for the year's line, not told again
                self.history["times"].append(dict(age=round(t / 52, 1), kind=k, channel=ch, dir=d, told=False))
                continue
            self._wfx_t[key] = t
            cause = self._wcause_text(e.get("cause"), kind)
            text = self.story.fill(line.replace("{who}", "someone close to them"))
            self._say(mk("X", f"{k}|{ch}|{d}|{band}|{cause.replace('|', '/')}", text), 0 if band == "big" else 1, "world_fx",
                      kind=k, channel=ch, dir=d, band=band, cause=cause)
            self.history["times"].append(dict(age=round(t / 52, 1), text=plain(text), kind=k, channel=ch, dir=d, cause=cause, big=band == "big"))

    def _times_year(self):
        """WL4: the year's one line on how the times touched them: close (a disaster, war, their town or a close person),
        else mixed (the two largest point opposite ways), else by the largest; what, from the two largest."""
        y, self._wyear = self._wyear, {}
        if ES is None or not y or self.burn_in or sum(y.values()) < 1.0:
            return                                       # a year the times really touched them: one big change or a few small
        items = sorted(y.items(), key=lambda kv: -kv[1])[:2]
        good = lambda ch, d: (d == "up") == (not ch.endswith("risk"))
        if any(ch in ("home", "close person") or WFX_KIND_LIB.get(k, k) in ("disaster", "war") for (k, ch, d) in y):
            tone = "close"
        elif len(items) == 2 and good(*items[0][0][1:]) != good(*items[1][0][1:]):
            tone = "mixed"
        else:
            (k, ch, d), _ = items[0]
            tone = (("easier" if d == "up" else "lean") if ch in ("money", "time", "health", "ties") else
                    ("freer" if d == "up" else "narrower") if ch in ("freedom", "option") else
                    ("calmer" if d == "up" else "uneasy") if ch == "safety" else ("uneasy" if d == "up" else "calmer"))
        whats = []
        for (k, ch, d), _ in items:
            w_ = ((ES.YEAR_WHAT.get(WFX_KIND_LIB.get(k, k)) or {}).get(ch) or {}).get(d) or (ES.YEAR_WHAT_CHANNEL.get(ch) or {}).get(d)
            if w_ and w_ not in whats:
                whats.append(w_.replace("{who}", "someone close to them"))
        last = getattr(self, "_wyear_said", (None, -99))
        if whats and tone in ES.YEAR and not (last[0] == (tone, tuple(whats)) and self.t - last[1] < 3 * 52):
            self._wyear_said = ((tone, tuple(whats)), int(self.t))
            self._say(self.story.fill(ES.YEAR[tone].replace("{what}", " and ".join(whats))), 0, "world_year", tone=tone)

    def _disaster_read(self, r):
        """WL6 (item 11): "a disaster in the next town" told as the disaster that happened, by the engine's hazard and
        where tags (Library DISASTER_READ): its scene, and the same color's reading in that disaster's words."""
        D = getattr(ES, "DISASTER_READ", None) if ES else None
        if not D or not r.get("hazard") or r["hazard"] not in D:
            return r
        d = D[r["hazard"]].get(r.get("where") or "near") or D[r["hazard"]].get("near")
        ev = LIB_READ.get(r["name"]) or {}
        c = next((x[4] for x in ev.get("readings", ()) if x[0] == r.get("reading")), None)
        if not d or c not in d:
            return r
        return dict(r, _scene=d.get("scene", ""), reading=d[c][0], say=d[c][1])

    def _option_cause(self, cs):
        """WL3: the world's biggest reason an option is closed, harder or easier (engine option_causes), as the Library's
        note, and the cause's own name for the hover."""
        c = max(cs, key=lambda c_: abs(float(c_.get("size", 0) or 0)))
        how = c.get("how", "harder")
        h = "closed" if how in ("banned", "not there", "out of reach") else "easier" if how in ("allowed", "easier") else "harder"
        k = c.get("kind") if c.get("kind") in ("law", "norm", "technology") else "norm" if how == "frowned on" else "odds"
        note = (getattr(ES, "OPTION_CAUSE", {}).get(k) or {}).get(h) if ES else None
        if not note:
            return None
        return dict(note=note, how=h, hover=cap_first(self._wcause_text(c.get("cause"), c.get("key") or c.get("kind", ""))
                                                       if c.get("cause") else str(c.get("key") or c.get("kind", ""))) + f" ({how})")

    def world_panel(self):
        """The player's world panel: public facts now and the history so far, by age and era (spec 1 §8); with WL5's record
        of what the times did to them, and P3's steers against the era, for the timeline."""
        wd = self.world_data()
        if not wd:
            return None
        p = self.wv.panel(wd[0], wd[1], self.age())
        if isinstance(p, dict):
            p["times"] = [x for x in self.history.get("times", []) if x.get("told", True)][-60:]
            p["steers"] = self.history.get("steers", [])[-200:] if GAME["world_steers"] else []
            if self.history.get("levers"):              # spheres phase 4: their lever acts on the town's spheres
                p["levers"] = self.history["levers"][-200:]
        return p

    # ------------------------------------------------------------------ spheres phase 4 and far ties: told, display only
    # (PRs #84 and #95, world-fields.md). They read the engine's events and the world as it stands; they draw no dice and
    # write nothing the engine reads. With sph_levers and far_ties off the engine logs none of these events.
    def _lever_where(self, loc, r):
        """Where a lever landed: their place in that sphere, by the Library's name for it as "their places" shows it (else
        the engine's place name in the world's epoch), or else the town's sphere."""
        WL = loc.get("WL")
        if int(r.get("place", -1)) >= 0 and WL is not None:
            try:
                h = WL.W.place_info(int(r["place"]))
                ns = ((ESP.HAUNT.get(h["kind"]) or {}).get("names") or []) if ESP is not None else []
                if ns:
                    return ns[h["name"] % len(ns)]
                import sphere_data as SD
                nm = (SD.PLACE_BY_EPOCH.get(h["kind"]) or {}).get(WL.W.sph_epoch)
                if nm:
                    return nm
            except Exception:
                pass
        return SPH_LEVER["sphere"].get(r.get("sphere"), "the town")

    def _lever_told(self, t, loc, r):
        """Spheres phase 4 (sph_levers): their lever act on their town's sphere (the engine's sphere_lever record) told as
        theirs: what they pushed, where it landed and whether it moved, backfired or set off an event. Nothing at all is
        quiet (the detailed story); the same lever on the same sphere within LEVER_AGAIN too. Kept for the World panel."""
        lv, sp, moved = r.get("lever", ""), r.get("sphere", ""), str(r.get("moved") or "none")
        act = SPH_LEVER["act"].get(lv)
        if not act:
            return
        head, _, rest = moved.partition(" ")
        went = ("fired" if head == "fired" else "state") if rest else moved if moved in ("moved", "backfired") else "none"
        what = SPH_LEVER["what"].get(rest, rest.replace("_", " ").replace(".", " "))
        where = self._lever_where(loc, r)
        tail = SPH_LEVER["moved"].get(lv, SPH_LEVER["moved"]["voice"]) if went == "moved" else SPH_LEVER[went].replace("{what}", what)
        text = self.story.fill(act.replace("{where}", where) + tail)
        came, rung = SPH_LEVER["came"][went], str(r.get("rung") or "")
        if ESP is not None:                             # the Library's words: the event set off, their rung in that sphere
            ev_ = (ESP.EVENT.get(f"{sp}.{rest}") or {}).get("name") if went == "fired" else None
            came = f"{came}: {ev_.lower()}" if ev_ else came
            LADDER = ["newcomer", "regular", "known", "pillar", "leader"]       # world_keys.LADDER, the engine's order
            rung = ESP.RUNG[sp][LADDER.index(rung)] if sp in ESP.RUNG and rung in LADDER else rung
        told = self.__dict__.setdefault("_lever_t", {})
        lvl = 0 if went in ("fired", "state") else 2 if went == "none" else 1
        if lvl == 1 and t - told.get((lv, sp), -10 ** 6) < LEVER_AGAIN:
            lvl = 2
        if lvl <= 1:
            told[(lv, sp)] = t
        self._say(mk("L", f"{lv}|{where}|{came}|{rung}", text), lvl + int(self.burn_in), "lever", lever=lv, sphere=sp, went=went)
        if went != "none" or float(r.get("size") or 0) > 0:     # an act with no reach at all (a child's) stays off the panel
            self.history.setdefault("levers", []).append(dict(age=round(t / 52, 1), lever=lv, sphere=sp, where=where, went=went,
                                                              came=came, rung=rung, text=plain(text)))

    def _far_town(self, loc, l_):
        """A town of their society by its name (as the World panel and the story name places)."""
        from worldview import place_name, loc_key
        WL = loc.get("WL")
        return place_name(self.wv.seed, loc_key(EngineWorld.soc(WL) if WL is not None else 0, int(l_)), self.setting)

    def _cast_who(self, cid):
        """A cast member as a world line names them ("their sister Mira"), and their name alone; None without a world."""
        wd = self.world_data()
        if not wd:
            return None
        from worldview import person_name
        p = next((c_ for c_ in wd[2] if c_.get("id") == cid), {})
        nm = self.cast_names(wd[2]).get(cid) or person_name(self.wv.seed, cid, False, self.setting)
        return who_word(p, nm), nm

    def _far_told(self, t, loc, c):
        """far_ties (PR #95): a close tie's news from the town they live in (cast event "far"), a tie taken into the
        household and how their stay ends ("taken in"); a want's cause (F5) is kept for the circle's hover."""
        kind, cid = c.get("kind"), int(c.get("cid", -1))
        if kind == "want":                                   # every want event passes here; only one with a cause is kept
            if c.get("cause"):
                self.__dict__.setdefault("_want_why", {})[cid] = (c.get("key"), c["cause"])
                self.__dict__.setdefault("_far_seen", {})[cid] = c["cause"]
            elif c.get("state") == "begins" and self.__dict__.get("_want_why"):
                self._want_why.pop(cid, None)
            return
        seen = self.__dict__.setdefault("_far_seen", {})     # cid -> the last far cause told or wanted (where they came from)
        who = self._cast_who(cid)
        if who is None:
            return
        w_, nm = who
        if kind == "far":
            cs = c.get("cause") or {}
            seen[cid] = cs
            sign = cs.get("sign") if cs.get("sign") in ("good", "hard", "mixed") else "mixed"
            text = (FAR_SAY["here" if c.get("here") else "away"][sign].replace("{town}", self._far_town(loc, cs.get("town", 0)))
                    .replace("{event}", cs.get("far_event") or "something happened"))
            lines = "; ".join(str(x_) for x_ in cs.get("line") or ())
            told = self.__dict__.setdefault("_far_t", {})
            lvl = 2 if c.get("here") or t - told.get(cid, -10 ** 6) < FAR_AGAIN else 1
            if lvl <= 1:
                told[cid] = t
            self._say(mk("F", f"{sign}|{nm}|{lines}", self._far_fill(text, w_)), lvl + int(self.burn_in), "far", kind="far",
                      sign=sign, here=bool(c.get("here")))
        elif kind == "taken in":
            st = c.get("state")
            if st is None:
                text = FAR_SAY["took"]
            elif st == "went back":
                l_ = (seen.get(cid) or {}).get("town")
                text = FAR_SAY["back"].replace("{town}", f" to {self._far_town(loc, l_)}" if l_ is not None else "")
            else:
                text = FAR_SAY["stayed"]
            self._say(self._far_fill(text, w_), (0 if st is None else 1) + int(self.burn_in), "far", kind="taken in", state=st or "")

    def _far_fill(self, text, who):
        """A far line with the tie named: their name at the start of a sentence capitalised, no comma before a stop."""
        return re.sub(r",([.:])", r"\1", cap_first(self.story.fill(text.replace("{who}", who))))

    def _far_moment(self, m, loc, s, ev=None):
        """A far moment (the Library's earth-far-ties.lib: cast_want far_hard, far_good or far_mixed) names the tie who
        calls in its first who: slot, {their_town} and {far_event}, from the engine's word on the call: the logged event's
        who and far, or, at a checkpoint, the call waiting on this moment (world_link pending, far_info; read only)."""
        if m is None or not self.batch or "far_event" in m["ctx"]:
            return
        if not str(self.L["src"][s].get("cast_want") or "").startswith("far_"):
            return
        WL = loc.get("WL")
        fi, slot, cid = None, None, None
        if ev is not None:
            fi = ev.get("far")
            slot, cid = next(iter((ev.get("who") or {}).items()), (None, None))
        elif WL is not None:
            fi = WL.far_info(0, s)
            pv = WL.pending.get(0)
            cid = int(pv[0]) if pv is not None and pv[2] == s else None
            slot = next(iter((self.L.get("W_WHO") or {s: ()})[s] or ()), None)
        if not fi:
            return
        m["ctx"]["their_town"] = self._far_town(loc, (fi.get("their_town") or {}).get("loc", fi.get("town", 0)))
        m["ctx"]["far_event"] = fi.get("far_event") or "something happened there"
        who = self._cast_who(int(cid)) if slot and cid is not None else None
        if who is not None and "_p_" + slot not in m["ctx"]:
            m["ctx"][slot] = who[1]

    # ------------------------------------------------------------------ v22.4's social mechanics (S1, S3 to S7): display only
    def _pron(self):
        """The character's object and possessive pronoun, by the gender they live as (N1d): her, him or them."""
        try:
            g = self.gender_view()["self"] if self.loc is not None else None
        except Exception:
            g = None
        return {"f": ("her", "her"), "m": ("him", "his")}.get(g, ("them", "their"))

    def _place_word(self, p):
        """A place of theirs by its plain name: a haunt by the Library's name for it ("the Curtain Call"), a setting's
        place by its own ("the house of worship"); "" for none."""
        if not isinstance(p, dict) or ESP is None:
            return ""
        if isinstance(p.get("place"), str):
            return p["place"]
        k = p.get("kind")
        if k is None:
            return ""
        ns = (ESP.HAUNT.get(k) or {}).get("names") or [(ESP.PLACE.get(k) or {}).get("name", "")]
        return str(ns[int(p.get("name", 0)) % len(ns)]) if ns and ns[0] else ""

    def _name_word(self, rep):
        """S3: their name at a place in the Library's words (earth_spheres.PLACE_NAME), from the engine's rep (-1 to 1)."""
        pn = getattr(ESP, "PLACE_NAME", None) or [(-1, "known")]
        return next((w for r, w in pn if float(rep) >= r), pn[-1][1])

    def _read_clause(self, face, act, side):
        """S3: how a place read an act (earth_spheres.READ "face.act", gift or danger): a clause after "thinks you"."""
        if not face or not act or side not in ("gift", "danger"):
            return ""
        return (getattr(ESP, "READ", {}).get(f"{face}.{act}") or {}).get(side, "")

    def _fair_lines(self, PP):
        """S1 (fair_read): per sphere that reads fair or unfair to them, the line for its hover in "their places": "Feels
        unfair to her: the council decided behind closed doors and gave no reason." Unfair names the part that pulls it
        down most, fair the part that holds it up most. None while the switch is off."""
        fi = PP.fair_info(0) if hasattr(PP, "fair_info") and ESP is not None else None
        if not fi:
            return None
        obj = self._pron()[0]; out = {}
        FP, FS = getattr(ESP, "FAIR_PART", {}), getattr(ESP, "FAIR", {})
        for sp, d in fi.items():
            f_, parts = float(d.get("fair", 0.5)), d.get("parts") or {}
            if f_ < FAIR_SIDE[0]:
                side, part = "unfair", d.get("weakest") or (min(parts, key=parts.get) if parts else None)
            elif f_ > FAIR_SIDE[1]:
                side, part = "fair", max(parts, key=parts.get) if parts else None
            else:
                continue
            w = (FS.get(f"{sp}.{part}") or FP.get(part) or {}).get(side)
            if w:
                out[sp] = dict(side=side, part=(FP.get(part) or {}).get("name", part), line=f"Feels {side} to {obj}: {w}.")
        return out or None

    def _eyes_word(self, e):
        """S3, S4: one place's eyes on them, for its hover: their name there, its last word on what they did (the
        reading as a clause), a go-between there, and with sph_odd whether they are the odd one out, blended in or held on."""
        d = dict(rep=round(float(e.get("rep", 0.0)), 2), name_word=self._name_word(e.get("rep", 0.0)),
                 read=self._read_clause(e.get("face"), e.get("act"), e.get("side")), go=bool(e.get("go_between")))
        if "odd" in e:
            d.update(odd=bool(e["odd"]), blended=bool(e.get("blended")), held=bool(e.get("held")))
        return d

    def _social_places(self, WL, hi, P):
        """v22.4 on "their places", each part only while its engine switch is on (nothing is added while off): S1's
        fairness line per sphere, S3's name and last word at each haunt and the places their settings meet (with S4's odd
        one out), and S7's posts they lead now."""
        PP = WL.PP
        try:
            fl = self._fair_lines(PP)
            if fl:
                P["fair"] = fl
        except Exception:
            pass
        if getattr(PP, "eyes_on", False):
            try:
                ei = PP.eyes_info(0) or []
            except Exception:
                ei = []
            byid, sets = {}, []
            for e_ in ei:
                pl = e_.get("place") or {}
                if int(pl.get("slot", 0)) >= 3:
                    sp = pl.get("sphere")
                    sets.append(dict(self._eyes_word(e_), name=self._place_word(pl), sphere=sp,
                                     sphere_name=(ESP.SPHERE.get(sp) or {}).get("name", sp), setting=pl.get("kind", ""),
                                     lead=str(pl.get("face") or e_.get("face") or "")[-1:], lead_name=pl.get("face_name", "")))
                else:
                    byid[int(pl.get("place", -1))] = self._eyes_word(e_)
            for h, h0 in zip(P["haunts"], hi["haunts"]):
                d_ = byid.get(int(h0.get("place", -2)))
                if d_:
                    h.update(d_)
            if sets:
                P["settings"] = [x for x in sets if x["name"]]
        try:
            posts = self._posts_view(WL)
        except Exception:
            posts = None
        if posts:
            P["posts"] = posts

    def _post_place(self, p):
        """S7: the plain name of what a post leads, the lead moments' {place}: a title's place (LEAD_PLACE), the setting
        led, a named place by its name, else the sphere's."""
        pl = p.get("place") or {}
        if pl.get("title"):
            return LEAD_PLACE.get(pl["title"], "the " + str(pl["title"]).split(" ")[0])
        pk = str(p.get("post_kind") or "")
        st = pl.get("setting") or (pk[len("setting_"):] if pk.startswith("setting_") else None)
        if st:
            return SETTING_PLACE.get(st, "the " + str(st).replace("_", " "))
        nm = self._place_word(pl) if pl.get("kind") else ""
        return nm or SPHERE_PLACE.get(p.get("sphere") or pl.get("sphere"), "the place")

    def _posts_view(self, WL):
        """S7 (lead_ways): the posts they lead now, for "their places": what they lead, their way (the game's words and its
        colour), how accepted they are, since when, terms and falls. None while the switch is off or nothing is led."""
        if not getattr(WL, "lw", False):
            return None
        out = []
        for p_ in WL.lead_info(0) or []:
            if p_.get("end") is not None:
                continue
            way = LEAD_WAY.get(p_.get("way"), (str(p_.get("way") or ""), p_.get("colour") or ""))
            lg = float(p_.get("legit", 0.5)); title = (p_.get("place") or {}).get("title")
            sp = p_.get("sphere")
            out.append(dict(name=self._post_place(p_), title=self.gword(title) if title else "", kind=p_.get("kind"),
                            sphere=sp, sphere_name=(ESP.SPHERE.get(sp) or {}).get("name", sp) if ESP is not None else sp,
                            way=way[0], colour=way[1], legit=round(lg, 2),
                            legit_word=next((w for v, w in LEAD_LEGIT if lg >= v), LEAD_LEGIT[-1][1]),
                            since=round(float(p_.get("start") or 0.0), 1), terms=int(p_.get("terms") or 0),
                            falls=len(p_.get("falls") or ())))
        return out or None

    def _lines_view(self):
        """S5 (sacred): the lines they will not cross, for the sheet: its kind, the Library's name for it, one "will not"
        clause, its colour, the age it formed and how it stands (whole, held, crossed or healed). None while off."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        PP = getattr(WL, "PP", None)
        if PP is None or not getattr(PP, "sac_on", False) or ESP is None or not hasattr(ESP, "LINE"):
            return None
        import world_keys as WK_
        out = []
        for j in range(PP.sac_line.shape[1]):
            k = int(PP.sac_line[0, j])
            if k < 0:
                continue
            kind = WK_.SACRED_KINDS[k]; LN = ESP.LINE.get(kind) or {}
            wn = LN.get("will_not") or [""]
            held, crossed = int(PP.sac_held[0, j]), int(PP.sac_crossed[0, j])
            state = ("healed" if int(PP.sac_wound[0, j]) < -10 ** 6 else "crossed") if crossed else "held" if held else "whole"
            out.append(dict(kind=kind, name=LN.get("name", kind), will_not=wn[(self.seed + k) % len(wn)], colour=COLORS[k],
                            formed=round((int(PP.sac_t[0, j]) - WL.t0) / 52, 1), state=state, held=held, crossed=crossed))
        return out or None

    def _lines_closing(self):
        """S5: the closing paragraph's line per sacred line tested in the life (LINE held, crossed or healed)."""
        try:
            lines = self._lines_view() or []
        except Exception:
            return ""
        out = [self.story.fill((ESP.LINE.get(x["kind"]) or {}).get(x["state"], "")) for x in lines if x["state"] != "whole"]
        return " ".join(x_ for x_ in out if x_)

    def _talk_told(self, t, loc, c):
        """S3: a go-between brings a place's reading back ("Cato says the Curtain Call thinks you kept to the rules"), at
        most once in TALK_AGAIN weeks at the normal level and once in TALK_QUIET in the detailed story."""
        if self.burn_in or ESP is None or not hasattr(ESP, "TALK"):
            return
        told = self.__dict__.setdefault("_talk_t", [-10 ** 6, None])
        kind = c.get("talk") if c.get("talk") in ESP.TALK else "good"
        pl = self._place_word(c.get("place"))
        gap = t - told[0]
        if (pl, kind) == told[1] and kind == "good":
            gap /= 3                                    # the same good word from the same place: once in three times as long
        lvl = 1 if gap >= TALK_AGAIN else 2 if gap >= TALK_QUIET else 9
        if lvl > self.detail:
            return
        read = self._read_clause(c.get("face"), c.get("act"), c.get("told") or c.get("side"))
        who = self._cast_who(int(c.get("go", -1))) if read and pl else None
        if who is None:
            return
        tpl = ESP.TALK[kind]
        text = tpl[int(t) % len(tpl)].replace("{go}", who[1]).replace("{place}", pl).replace("{read}", read)
        told[0], told[1] = t, (pl, kind)
        self._say(mk("N", f"{kind}|{pl}", cap_first(text)), lvl, "talk", kind=kind, place=pl)

    def _line_told(self, t, c):
        """S5: the year a sacred line forms, the Library's line for it (LINE formed)."""
        if c.get("what") != "line" or ESP is None or not hasattr(ESP, "LINE"):
            return
        LN = ESP.LINE.get(c.get("line")) or {}
        if LN.get("formed"):
            self._say(mk("S", f"{c.get('line')}|{c.get('colour', '')}", self.story.fill(LN["formed"])), int(self.burn_in),
                      "line", kind=c.get("line"))

    def _seen_who(self, d, WL):
        """S6: the model as the option row names them ("her aunt Mira"), a public figure by name; None if unknown."""
        if d.get("figure") is not None and WL is not None:
            from worldview import FIG_SOC
            return self.wv.fig(int(d["figure"]) + FIG_SOC * EngineWorld.soc(WL))
        if d.get("who") is None:
            return None
        who = self._cast_who(int(d["who"]))
        if who is None:
            return None
        w_, nm = who
        if w_.startswith("their "):
            return self._pron()[1] + w_[len("their"):]
        return nm

    def _seen_rows(self, loc, s):
        """S6 (seen_done): per option of moment s, the row "Mira has seen it done: her aunt Ines" (SEEN_ROW says which
        options carry one): kind, the short word and the Library's sentence (earth_spheres.SEEN). None while off."""
        WL = loc.get("WL")
        if not getattr(WL, "seen_on", False) or ESP is None or not hasattr(ESP, "SEEN"):
            return None
        info = WL.seen_info(0, s) or []
        out = {}
        for k, d in enumerate(info):
            if not d or d.get("kind") not in SEEN_ROW["path" if d.get("path") is not None else "way"]:
                continue
            kind = d["kind"]
            who = self._seen_who(d, WL) if kind != "none" else ""
            if who is None:
                continue
            tpl = ESP.SEEN.get(kind) or []
            if not tpl:
                continue
            text = self.story.fill(tpl[(self.seed + s + k) % len(tpl)].replace("{who}", who))
            out[k] = dict(kind=kind, word=SEEN_MARK.get(kind, kind), text=text)
        return out or None

    def _seen_dream_told(self, t, d):
        """S6: a dream seeded from someone they watched (8 to 20): the Library's SEEN dream line."""
        if ESP is None or not hasattr(ESP, "SEEN") or not ESP.SEEN.get("dream"):
            return
        who = self._seen_who(d, self.loc.get("WL") if isinstance(self.loc, dict) else None)
        if who is None:
            return
        tpl = ESP.SEEN["dream"]
        self._say(self.story.fill(tpl[int(t) % len(tpl)].replace("{who}", who)), 1 + int(self.burn_in), "seen", kind="dream",
                  path=d.get("path", ""))

    def _social_slots(self, m, loc, s, ev=None):
        """v22.4's moments name what they are about (the Library's #103, #106, #107): a caught-between moment its two
        places ({place_a}, {place_b}), an odd-one-out its place and a lead moment the post's ({place}), a sacred offer its
        price ({offer}; there {place} stays the town). From the logged moment's own word, or at a checkpoint from the
        engine's on the moment waiting (eyes_info, lead_info, sacred_info; read only)."""
        if m is None:
            return
        cw = str(self.L["src"][s].get("cast_want") or "")
        if cw not in ("caught", "odd", "sacred", "tragic", "amends") and not cw.startswith("lead_"):
            return
        WL = loc.get("WL"); ctx = m["ctx"]; ctx["_social"] = True
        try:
            if cw in ("caught", "odd"):
                ei = ev.get("eyes") if ev is not None else WL.eyes_info(0, s) if hasattr(WL, "eyes_info") else None
                for k_ in ("place_a", "place_b", "place"):
                    if ei and ei.get(k_) and k_ not in ctx:
                        ctx[k_] = self._place_word(ei[k_])
            elif cw.startswith("lead_"):
                li = ev.get("lead") if ev is not None else WL.lead_info(0, s) if getattr(WL, "lw", False) else None
                if li and "place" not in ctx:
                    ctx["place"] = self._post_place(li)
            else:
                si = ev.get("sacred") if ev is not None else WL.sacred_info(0, s) if hasattr(WL, "sacred_info") else None
                if si and si.get("offer") and "offer" not in ctx:
                    ctx["offer"] = si["offer"]
        except Exception:
            pass

    def _want_why_rows(self, circle):
        """F5 on the circle's hover: a want that came of a far event carries its cause; a far want gets its own words."""
        why = self.__dict__.get("_want_why")
        if not why:
            return
        for p_ in circle:
            k_, cs = why.get(p_["id"], (None, None))
            if not cs or not p_.get("want") or p_["want"] != str(k_).replace("_", " "):
                continue
            p_["want"] = FAR_SAY["want"].get(k_, p_["want"])
            town = self._far_town(self.loc, cs.get("town", 0)) if isinstance(self.loc, dict) else "their town"
            p_["want_why"] = cap_first(f"{cs.get('far_event', 'something happened')} in {town}"
                                       + (": " + "; ".join(cs["line"]) if cs.get("line") else ""))

    # ------------------------------------------------------------------ item 3: the voice in their head
    def _vsay(self, kind, xs):
        """A Library voice line pair: the first variant the first time this kind is told, the second after."""
        n = self._voice_said.get(kind, 0); self._voice_said[kind] = n + 1
        return xs[min(n, len(xs) - 1)] if isinstance(xs, list) else xs

    def _vfill(self, text, **kw):
        noun = ES.VOICE["noun"].get(self.setting, "voice") if ES else "voice"
        text = text.replace("{voice}", noun).replace("{name}", kw.pop("name", "") or self.voice_name())
        for k, v in kw.items():
            text = text.replace("{" + k + "}", str(v))
        return self.story.fill(text)

    def voice_name(self):
        """The voice's name in this life (voice-mechanics.md section 5): the strongest of the ten sides it pushed toward,
        trusted or doubted by the character's trust in that side's colors; "a voice" before VOICE_MIN pushes, "a quiet
        voice" when the player mostly lets them be."""
        if ES is None:
            return "the voice"
        v = self.history["voice"]; V = ES.VOICE
        noun = V["noun"].get(self.setting, "voice")
        if v["steer"] < VOICE_MIN:
            quiet = v["n"] >= 10 and v["steer"] / v["n"] < 0.2
            return (V["quiet"] if quiet else V["none"]).replace("{voice}", noun)
        ax = np.asarray(v.get("rk") or v["ax"], float)   # the side its pushes stood for most steadily among the open ways
        i = int(np.argmax(np.abs(ax))); sg = 1 if ax[i] > 0 else -1
        side = VOICE_SIDES[i][1 if sg > 0 else 2]
        cols = [c for c in range(C) if VOICE_AX[i, c] * sg > 0]
        tr = float(np.mean(self.trust[cols])) if cols else 0.0
        return V["name"][side]["doubted" if tr < 0 else "trusted"].replace("{voice}", noun)

    def _voice_trust(self, d):
        """The character's trust in the voice as one number: over the colors it pushed toward, an even mean; with item 7 on
        (GAME trust_judge), weighted by how much it pushed toward each, so the colors it pushed most decide the word."""
        pushed = d > 0
        if GAME["trust_judge"]:
            return float(d[pushed] @ self.trust[pushed] / d[pushed].sum())
        return float(np.mean(self.trust[pushed]))

    def voice_view(self, loc=None):
        """The panel row "The voice in their head": its name, the character's trust in words, and on hover what the voice
        moved in this life against what life itself moved, per color, in points."""
        v = self.history["voice"]; loc = self.loc if loc is None else loc
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed and v["steer"] else 0.0
        word = "" if not v["steer"] else "they trust it" if tr >= 0.25 else "they doubt it" if tr <= -0.25 else "they are unsure of it"
        total = (E.softmax(loc["z"][0]) - np.asarray(self._w_start, float)) if loc is not None and self._w_start is not None else np.zeros(C)
        vdw = self._vdw()
        return dict(name=self.voice_name(), trust=word, steer=v["steer"], n=v["n"], share=round(voice_share(vdw, total), 3),
                    voice=[round(float(x) * 100, 1) for x in vdw], life=[round(float(x) * 100, 1) for x in total - vdw],
                    toward=[round(float(x), 3) for x in d / max(v["steer"], 1)], **({"own": self.own_view()} if GAME["own_ix"] else {}))

    def _voice_pick(self, loc, cpw, worked, pushed, rel, moved, rs):
        """Item 3 at each decided moment: the record (the steer: the picked act's colors minus what they would have done),
        what the push moved, and the character's answer to the voice and its outcome (Library VOICE lines). Returns
        (answer, outcome) for a push, else None."""
        v = self.history["voice"]; v["n"] += 1
        if not pushed or ES is None:
            return None
        m = np.maximum(np.asarray(loc["m"][0], float), 0)
        cv = lambda k: m[k] / m[k].sum() if m[k].sum() > 0 else np.full(C, 0.2)
        k, own = int(cpw["choice"]), int(cpw["own"])
        diff = cv(k) - cv(own)
        v["steer"] += 1; v["rel"] = round(v["rel"] + rel, 3)
        v["d"] = [round(x + float(y), 4) for x, y in zip(v["d"], diff)]
        v["ax"] = [round(x + float(y), 4) for x, y in zip(v["ax"], VOICE_AX @ diff)]
        ks = [o for o in range(m.shape[0]) if m[o].sum() > 0]
        if len(ks) > 1:                                  # where the pick stood among the open ways, per side (-1 to 1)
            vals = np.array([VOICE_AX @ cv(o) for o in ks]); pv = VOICE_AX @ cv(k)
            rk = ((vals < pv - 1e-9).sum(0) - (vals > pv + 1e-9).sum(0)) / (len(ks) - 1)
            v["rk"] = [round(x + float(y), 4) for x, y in zip(v.get("rk") or [0.0] * len(VOICE_SIDES), rk)]
        dw = np.asarray(moved.get("dw") or np.zeros(C), float) / 100 + np.asarray((rs.get("pivot") or {}).get("moved") or np.zeros(C), float) / 100
        v["dw"] = [round(float(x) + float(y), 4) for x, y in zip(self._vdw(), dw)]; v["dw_t"] = int(self.t)
        self._vyear["steer"] += 1; self._vyear["won"] += int(worked)
        V = ES.VOICE; c = COLORS[int(np.argmax(cv(k)))]
        lead = int(np.argmax(E.softmax(loc["z"][0]))); ci = COLORS.index(c)
        rel_ = "same" if c in (self._core_label or COLORS[lead]) else "ally" if (ci - lead) % C in (1, C - 1) else "enemy"
        tr = float(self.trust[ci]); tw = "trust" if tr >= 0.25 else "doubt" if tr <= -0.25 else "unsure"
        last = self._vlast.get(c)
        if (last is not None and self.t - last["t"] <= VOICE_RECALL and not self._vlast.get("_mem")):
            # the voice pushed this way not long ago: they remember how it went (not twice running)
            key = "worked" if last["worked"] else "failed" if last.get("moment") else "failed_plain"
            ans = self._vfill(self._vsay("memory_" + key, V["memory"][key]), lost="“" + str(last.get("moment", "")) + "”")
        else:
            ans = self._vfill(V["answer"][c][rel_][tw][1 if rel >= 0.5 else 0])
        self._vlast["_mem"] = last is not None and self.t - last["t"] <= VOICE_RECALL and not self._vlast.get("_mem")
        self._vlast[c] = dict(worked=worked, moment=cpw["cp"]["title"], t=int(self.t))
        out = ""
        if rel >= GAME["hind_rel"]:                      # they resisted: was the voice right?
            out = self._vfill(V["outcome"]["right" if worked else "wrong"][1 if rel >= 0.5 else 0])
        rs["voice"] = dict(answer=ans, outcome=out, name=self.voice_name())
        return "“" + ans + "”", out

    def _voice_trust_turn(self):
        """Item 3: trust in a color crossing .5 or -.5 is told once, as the relationship turns."""
        if ES is None or self.burn_in:
            return
        for i, c in enumerate(COLORS):
            st = 1 if self.trust[i] >= 0.5 else -1 if self.trust[i] <= -0.5 else 0
            if st and st != self._trust_side[i]:
                d = "up" if st > 0 else "down"
                self._vline(self._vfill(self._vsay("turn", ES.VOICE["trust_turn"][c][d])), turn=d, color=c)
                self._vyear["turn"] = d
            self._trust_side[i] = st

    def _vline(self, text, **meta):
        """A voice line in the story: one a year at most (voice-mechanics.md section 9), the first that comes."""
        y = int(round(self.t / 52, 1))
        if y == self._vline_y:
            return False
        self._vline_y = y
        self._say(text, 0, "voice", **meta)
        return True

    def _vdw(self):
        """What the voice's pushes still hold of their colors now, per color: each push's move, fading as life pulls
        them back (VOICE_HALF)."""
        v = self.history["voice"]
        return np.asarray(v["dw"], float) * VOICE_FADE ** (self.t - v.get("dw_t", self.t))

    def _voice_became(self, lbl):
        """Item 3: a new name that the voice's pushes did most of is told as partly not their own doing."""
        v = self.history["voice"]; w = np.asarray(self._wring[-1], float)
        mark, self._name_mark = self._name_mark, (w.copy(), self._vdw().copy(), int(self.t))
        if ES is None or mark is None or self.burn_in or v["steer"] < VOICE_MIN or not lbl:
            return
        share = voice_share(self._vdw() - mark[1] * VOICE_FADE ** (self.t - mark[2]), w - mark[0])
        if share < 0.5 or self.t - v.get("became_t", -10 ** 6) < 5 * 52:
            return                                       # told when the voice did most of it, once in five years at most
        v["became_t"] = int(self.t)
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed else 0.0
        key = "trusted" if tr >= 0.25 else "doubted" if tr <= -0.25 else "unsure"
        self._vline(self._vfill(ES.VOICE["became"][key], ident=art(ident_name(lbl))), became=lbl, share=round(share, 2))

    def _voice_chapter(self, age):
        """Item 3: at most one voice line in a year's chapter, and only in years with something to say: the first year of
        the voice, trust turning, the voice winning most arguments, or a long quiet."""
        y, self._vyear = self._vyear, dict(steer=0, won=0, turn=None)
        v = self.history["voice"]
        if ES is None or self.burn_in or not v["n"]:
            return
        V = ES.VOICE["chapter"]; kind = None
        if y["turn"]:
            kind = "trust_up" if y["turn"] == "up" else "trust_down"
        elif y["steer"] and v["steer"] == y["steer"]:
            kind = "first"
        elif y["steer"] >= 3 and y["won"] * 2 > y["steer"]:
            kind = "won"
        elif not y["steer"] and v["steer"] and age - v.get("last_age", age) >= 3 and age - v.get("quiet_age", -99) >= 10:
            kind = "quiet"; v["quiet_age"] = age
        if y["steer"]:
            v["last_age"] = age
        if kind:
            self._vline(self._vfill(self._vsay("ch_" + kind, V[kind])), chapter=kind)

    def voice_review(self, h):
        """Item 3 at the end of a life: the voice's last sentence for the song (VOICE end) and the Book's line for this
        life (VOICE book)."""
        v = h["voice"]
        if ES is None:
            return {}
        V = ES.VOICE; vw = self.voice_view()
        share = vw["share"]; sw = next((w_ for b_, w_ in V["share"] if share < b_), V["share"][-1][1])
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed and v["steer"] else 0.0
        key = "quiet" if v["steer"] < VOICE_MIN else "trusted" if tr > 0.2 else "doubted" if tr < -0.2 else "mixed"
        lead = COLORS[int(np.argmax(np.asarray(h["w"][-1][1], float)))] if h["w"] else "W"
        end = self._vfill(V["end"][key], adj=ADJ[lead], share=sw)
        names = [l_ for a_, l_, *_ in h.get("name", []) if l_]
        start = next((l_ for a_, l_, *_ in h.get("name", []) if a_ >= self.start_age and l_), names[0] if names else "")
        book = self._vfill(V["book"]["steered" if v["steer"] else "free"], start=art(ident_name(start)) if start else "still forming",
                           end=art(ident_name(names[-1])) if names else "still forming",
                           lean=V["lean"][COLORS[int(np.argmax(d))]] if v["steer"] else "")
        return dict(name=vw["name"], trust=vw["trust"], share=share, end=end, book=book, steer=v["steer"], n=v["n"],
                    voice=vw["voice"], life=vw["life"])

    def _thread_line(self, cause, age):
        """F5: the story sentence that ties a moment back to the pick that started its thread, and the cause in plain words
        for the hover. Built-in words until the Library's drop B (chroma-library/earth_play.py) brings its own."""
        when = "this year" if age - cause["age"] < 1 else "a year ago" if age - cause["age"] < 2 else f"at {cause['age']}"
        did = chooses(act(plain(cause["act"]))).rstrip(".")
        how = "you pushed it" if cause.get("pushed") else "they chose it themselves"
        why = f"It goes back to {when}, at “{cause['moment']}”, when they chose {did} ({how}), and {cause['what']}."
        T = getattr(ES, "THREAD", None); H = getattr(ES, "THREAD_HOVER", None)
        line = hover = ""
        if T and H:                                      # the Library's sentence by what the thread is, its hover first
            k = cause.get("key")
            who = next((self.story.say(p) for p in self.story.alive("partner")), "their partner") if cause.get("kind") == "partner" else ""
            fills = dict(title=art(cause.get("title", "")), who=who, plan=cause.get("goal") or "their plan",
                         dream=cause.get("goal") or "their dream", age=cause["age"])
            if k == "title":
                line, hover = T["title"]["held"], H["title"]["held"]
            elif k == "commitment" and cause.get("kind") in T["commitment"]:
                line, hover = T["commitment"][cause["kind"]], H["commitment"][cause["kind"]]
            elif k in ("plan", "dream"):
                line, hover = T[k], H[k]
            for f_, v_ in fills.items():
                line, hover = line.replace("{" + f_ + "}", str(v_)), hover.replace("{" + f_ + "}", str(v_))
        if not line:
            line = "This goes back to the day {N} chose " + did + "."
        return dict(line=self.story.fill(line), cause=(self.story.fill(hover) + " " if hover else "") + why, age=cause["age"])

    def _thread_of(self, loc, s):
        """5.6 and F5: whether moment s follows from this life's own threads (it needs a title or perk they hold, an
        option steps a commitment they hold, or it offers a step toward a plan or dream they hold), and the pick that
        started that thread, when one did (the latest)."""
        L = loc["L"]; GR = L.get("ROLES") if loc.get("RON") else None
        found = []
        if GR is not None and "S_HOLDM" in GR and "r_has" in loc:
            hm = np.asarray(GR["S_HOLDM"][s], bool); has = np.asarray(loc["r_has"][0], bool); n = min(len(hm), len(has))
            found += [("r", int(i)) for i in np.nonzero(hm[:n] & has[:n])[0]]
        com = np.asarray(L["COMMIT"][s])[np.asarray(loc["mask"][0], bool)]
        found += [("c", KNAMES[d]) for d in sorted({int(x) for x in com if x >= 0}) if loc["held"][0, d]]
        if "gsr" in loc and "gk" in loc and "gid" in loc:
            found += [("g", int(loc["gid"][0, j])) for j in np.nonzero(loc["gk"][0] >= 0)[0] if loc["gsr"][0, j, s] >= 0.5]
        causes = [self._threads[f] for f in found if f in self._threads
                  and self.t - self._threads[f]["t"] <= THREAD_YEARS * 52 and self.t - self._threads[f].get("told", -10 ** 6) >= THREAD_AGAIN]
        return bool(found), (max(causes, key=lambda c_: c_["t"]) if causes else None)

    def trust_view(self):
        """Trust per color, for the page and the status screen."""
        return {c: round(float(v), 3) for c, v in zip(COLORS, self.trust)}

    def _tries(self, name):
        """Which try at this title this is: 1 + the misses at it since they last made it."""
        n = 1
        for x in reversed(self.history["long"]):
            if x["name"] == name:
                if x["made"]:
                    break
                n += 1
        return n

    @staticmethod
    def _long_shot(o):
        """Emren 2026-10-06 (packs thread): any title can be pushed for at long odds, and a missed one is a story of its own.
        The title an option reaches for if it works, when it works for fewer than LONG_SHOT of people (the Library's chance,
        else the true odds) or when failing grants the packs' long-shot perk; else None."""
        fx = o.get("roles_fx") or ()
        aim = next((d for d in fx if d["when"] == "ok" and d["gain"] and d.get("title")), None)
        if aim is None:
            return None
        odds = o.get("base", o.get("true"))
        marked = any(d["when"] == "fail" and d["gain"] and "long shot" in str(d.get("name", "")) for d in fx)
        if not marked and (odds is None or odds >= LONG_SHOT or aim.get("kind") not in LONG_SHOT_KINDS):
            return None
        return dict(name=aim["name"], say=aim["say"], odds=None if odds is None else round(float(odds), 3), rung=o.get("rung"))

    def _res_roles(self, loc, events):
        """Titles and perks this choice's week gained or lost (explain.after's title and perk events), as chips."""
        GR = self.L.get("ROLES") if loc.get("RON") else None
        out = []
        for e_ in events:
            if e_.get("kind") not in ("title", "perk") or GR is None or e_["name"] not in GR["ID"]:
                continue
            d = role_info(GR, GR["ID"][e_["name"]]); up = e_["what"] in ("gained", "regained", "restored", "reshaped")
            how = e_.get("how") or ""
            if not up and (how in ("replaced",) or how.startswith("became") or (how.startswith("the ") and how.endswith(" ended"))):
                continue                                # told by the title that replaced or ended it
            d.update(what=e_["what"], how=how, up=up, word=(d["say"] if d["title"] else d["pred"]) if up else
                     ("no longer " + d["say"]) if d["title"] else neg_of(d["pred"]))
            if e_["what"] == "reshaped":
                d["word"] = d["say"] + ", another way"
            if e_.get("profile"):
                d["profile"] = e_["profile"]
            if e_.get("refines"):
                d["on"] = e_["refines"]
            out.append(d)
        return out[:6]

    # ------------------------------------------------------------------ forced picks: costs
    def _follows(self, loc, s, k, felt, commit, recon):
        """What may follow an option, as the character can foresee it from the library's own tags: what it costs,
        what success and failure bring, which needs success meets, and the chance it starts a commitment.
        A placeholder until the engine gives foreseen outcomes for plans."""
        L = loc["L"]
        if loc["do_nothing"][0, k]:
            return dict(cost=[], win=[], lose=[], needs=[], commit_p=0.0)
        def moves(v):
            return [f"{'+' if x > 0 else '-'}{RNAMES[j]}" for j, x in enumerate(v) if abs(x) >= 0.02]
        e = np.maximum(loc["e"][0, k], 0)
        nv = E.NMAP @ e
        needs = [E.NEEDS[j] for j in np.argsort(-nv)[:2] if nv[j] > 0.05] if not recon else []
        cp = 0.0
        if commit >= 0 and not loc["held"][0, commit] and not recon:
            cp = felt * float(loc["P"]["commit_p"][commit])
        return dict(cost=moves(L["PAY"][s, k]), win=moves(L["WIN"][s, k]), lose=moves(L["LOSE"][s, k]),
                    needs=needs, commit_p=cp, lift=[] if recon else self._lift(loc, s, nv))

    def _lift(self, loc, s, nv):
        """Which lacking needs an option's ends would feed if it works, and how much that matters (IDEAS.md, "Make needs
        visible"): the engine's own refill rule (0.12 x stakes x ends' share x room left), read against how low the need
        is now. Needs met is the biggest driver of satisfaction, most of all a need that was lacking."""
        if "need" not in loc:
            return []
        need = loc["need"][0]; st = max(float(loc["L"]["STAKES"][s]), 0.9)
        out = []
        for j in np.argsort(-nv):
            lv = float(need[j])
            if nv[j] <= 0.05 or lv >= GAME["need_thin"]:
                continue
            gain = 0.12 * st * float(nv[j]) * (1 - lv)
            out.append(dict(need=E.NEEDS[j], level=round(lv, 3), gain=round(gain, 3), word=need_level_word(lv),
                            lift="a big lift" if lv < 0.3 else "a lift"))
        return out[:2]

    @staticmethod
    def _ways(loc, k):
        """An act's ways as shares of one (even when it has none)."""
        m = np.maximum(np.asarray(loc["m"][0, k], float), 0)
        return m / m.sum() if m.sum() > 0 else np.full(C, 1 / C)

    # ------------------------------------------------------------------ S2: making it their own (GAME own_...)
    def _own_k(self, loc, k):
        """S2: what is left of a push's reluctance in act k's ways, 1 - own_rel x how far they have become theirs."""
        if not GAME["own_ix"] or not self.ix.any() or np.maximum(np.asarray(loc["m"][0, k], float), 0).sum() <= 0:
            return 1.0
        return 1.0 - GAME["own_rel"] * float(self._ways(loc, k) @ self.ix)

    @staticmethod
    def _around(loc):
        """S2: the colors around them as shares of one (the engine's "around": their haunts' faces and close people);
        even without it."""
        a = loc.get("around") if loc is not None else None
        a = np.maximum(np.asarray(a, float).reshape(-1)[:C], 0) if a is not None else np.zeros(C)
        return a / a.sum() if a.sum() > 0 else np.full(C, 1 / C)

    def _own_step(self, x):
        return next(k for lo, k in OWN_STEPS if x >= lo)

    def _own_push(self, loc, cpw, hind):
        """S2: a push toward ways the character would not have taken moves how far each has become theirs:
        own_k x push x A x T x S x H per color (GAME own_...). A hard push at high reluctance into a way not yet
        "ought to" can bounce back instead. Returns what moved, for the resolution, or None."""
        k, own = int(cpw["choice"]), int(cpw["own"])
        push = np.maximum(self._ways(loc, k) - self._ways(loc, own), 0)
        if push.sum() <= 0:
            return None
        f = self._force or {}
        before = self.ix.copy(); age = round(self.t / 52, 1)
        way = float(push @ before) / float(push.sum())
        if not f.get("light") and f.get("rel", 0.0) > GAME["own_react_rel"] and way < 0.25 and self._ixrng.random() < GAME["own_react"]:
            self.ix = np.clip(self.ix - GAME["own_react_back"] * push / push.max(), 0.0, 1.0)     # reactance: it bounces back
            loc["Q"][0] += GAME["backlash"] * float(f.get("resent", f.get("rel", 0.0)))
            for c in np.nonzero(self.ix < before)[0]:
                self.history["own_ix"].append((age, COLORS[c], "back"))
            return dict(kind="back", ix=[round(float(x), 3) for x in self.ix])
        A = GAME["own_light"] if f.get("light") else GAME["own_strong"]
        T = np.maximum(0.0, 0.5 + self.trust)
        S = 0.5 + GAME["own_sup"] * self._around(loc)
        judged = (hind or {}).get("kind")
        H = GAME["own_acc"] if judged == "accepted" else GAME["own_res"] if judged == "resented" else 1.0
        self.ix = np.clip(self.ix + GAME["own_k"] * push * A * T * S * H, 0.0, 1.0)
        for c in range(C):
            s0, s1 = self._own_step(before[c]), self._own_step(self.ix[c])
            if s0 != s1:
                self.history["own_ix"].append((age, COLORS[c], s1))
        return dict(kind="step", ix=[round(float(x), 3) for x in self.ix])

    def _own_year(self):
        """S2, once a year: a way led by fewer than own_use of the year's acts fades by up to own_fade."""
        self.ix = np.maximum(0.0, self.ix - GAME["own_fade"] * np.clip(1 - self._ix_use / GAME["own_use"], 0.0, 1.0))
        self._ix_use[:] = 0

    def own_view(self):
        """S2, the Voice row's hover: each way the voice pushed toward (or that has a step), how far it has become theirs,
        in the Library's words for that way (VOICE["own"]: trusted or doubted by their trust in that color)."""
        if not GAME["own_ix"]:
            return []
        d = np.asarray(self.history["voice"]["d"], float)
        V = (ES.VOICE.get("own") if ES is not None else None) or {}
        out = []
        for i, c in enumerate(COLORS):
            if d[i] <= 0 and self.ix[i] <= 0.005:
                continue
            step = self._own_step(float(self.ix[i]))
            lines = (V.get(c) or {}).get(step) or []
            line = self._vfill(lines[0 if self.trust[i] >= 0 else 1]) if lines else ""
            out.append(dict(color=c, ix=round(float(self.ix[i]), 3), step=step, line=line))
        return out

    def _profile(self, loc, k):
        """An act's colors for trust: its ways and its ends, half and half, as shares of one."""
        p = 0.5 * np.maximum(loc["m"][0, k], 0) + 0.5 * np.maximum(loc["e0"][0, k] if "e0" in loc else loc["e"][0, k], 0)
        return p / p.sum() if p.sum() > 0 else np.full(C, 1 / C)

    def _trust_on(self, loc, k):
        """The character's trust in the player along an act's colors, -1 to 1."""
        return float(self._profile(loc, k) @ self.trust)

    @staticmethod
    def _resent(rel, trust):
        """How much of a push's reluctance becomes resentment (stress and pent-up wanting): trust in the act's colors spares
        some of it, distrust adds to it. The effort (lower odds) is the character's own inertia and stays as it is."""
        return rel * (1 - GAME["trust_cut"] * max(trust, 0.0) + GAME["distrust_add"] * max(-trust, 0.0))

    def _on_odds(self, loc, p_true):
        f = self._force
        if f is None:
            return p_true
        pt = float(np.clip(p_true[0], 1e-6, 1 - 1e-6))
        lg = np.log(pt / (1 - pt)) - GAME["effort"] * f["rel"] - (GAME["out_of_reach"] if f["closed"] else 0.0)
        p = p_true.copy(); p[0] = 1 / (1 + np.exp(-lg))
        return p

    def _on_learn(self, loc, delta):
        f = self._force
        if f is None:
            return delta
        rel = f["rel"]; tr = f.get("trust", 0.0)
        f["resent"] = rs = self._resent(rel, tr)
        self._price = self._price_now() + rs + 0.5 * rel; self._price_t = int(self.t)   # 5.6: the price builds
        # item 4 (Emren 10-08 23:18): the price of a push moves from learning to cost. The act teaches in full (v22.1 cut a
        # reluctant act's lesson to learn_keep); what it teaches about who they are is the pivotal lesson (_pivot)
        d = delta
        if not GAME["learn_full"]:                       # off (GAME_OFF): v22.1's cut, trust letting more of it in
            d = delta.copy(); d[0] *= 1 - (1 - GAME["learn_keep"]) * rel * (1 - max(tr, 0.0))
        loc["stress"][0] += GAME["stress"] * rs
        loc["Q"][0] += GAME["backlash"] * rs                              # wanting what they were denied builds up
        if f["closed"] and not loc["succ"][0]:
            loc["stress"][0] += GAME["backfire_stress"]
            loc["res"][0, 0] = max(0.0, loc["res"][0, 0] - GAME["backfire_money"])
        f["succ"] = bool(loc["succ"][0])
        return d

    # ------------------------------------------------------------------ narration
    def _met(self, age, ev, sit):
        """What this life met, once each, with the age: moments, the world's readings, titles gained, deeds, deaths close by
        (implementation list item 1: the end of a life told as one paragraph)."""
        h = self.history
        if "situation" in ev:
            kind, name = "sit", sit
        elif "outside" in ev:
            kind, name = "read", ev["outside"]["name"]
        elif "role" in ev and ev["role"]["what"] == "gained":
            if ev["role"].get("kind") not in TITLE_KINDS:
                return                          # skills, bonds, children and partners are not a stage of the life
            kind, name = "role", ev["role"]["name"]
            GR = self.L.get("ROLES")
            if GR is not None and name in GR["ID"]:
                h["title_say"][name] = GR["say"][GR["ID"][name]]      # 'a baker', 'out of work'
        elif "mark" in ev:
            kind, name = "mark", ev["mark"]["mark"]
        elif "death" in ev:
            h["met"].append((round(age, 1), "death", ev["death"]["role"]))    # each death counts
            return
        else:
            return
        if name != "an ordinary week" and not any(m[1] == kind and m[2] == name for m in h["met"]):
            h["met"].append((round(age, 1), kind, name))

    def _say(self, line, level=0, tag="note", **meta):
        if " or " in line and self.loc is not None:     # two-word titles in their own words (N1d §3)
            line = self.gword(line)
        if level <= self.detail:
            self.log.append(plain(line))
            if line:
                self.feed.append(dict(tag=tag, text=line, age=round(self.t / 52, 1), **meta))

    def _on_week(self, t, loc):
        if t % 52 == 0 and t >= 3 * 52:
            self._yearly(t, loc)
        if not self._need_hint and not self.burn_in and "need" in loc and t / 52 >= max(self.start_age, 6):
            j = int(np.argmin(loc["need"][0]))
            if float(loc["need"][0, j]) < GAME["need_thin"]:   # IDEAS.md, "Make needs visible", fix 5: the rule, once
                self._need_hint = True
                self._say(NEED_HINT.format(need=NEED_WORD[E.NEEDS[j]], N=self.name), 0, "hint", need=E.NEEDS[j],
                          need_level=round(float(loc["need"][0, j]), 3))

    def conditions(self, loc):
        """The context the engine times life events by (v6 drivers, about -1..1; trouble and fortune 0..2)."""
        X = loc.get("X")
        if X is None:
            return {}
        return {c: float(X[0, i]) for i, c in enumerate(E.CTX)}

    def shadow_view(self, loc=None):
        """Light and shadow (stage 2, item 2) as the page shows it: per colour its shadow part (the share of the colour in
        shadow, 0 to 1), its force, whether the state shows (the engine's adjective, on above .5 and off below .35), whether
        the person has seen it, the line ("Red 40%, a quarter of it in shadow: reckless at times") and the sources in
        words. None while the engine's shadows switch is off. Reads only; nothing is drawn at random or written back."""
        loc = self.loc if loc is None else loc
        if loc is None or not loc.get("SHON") or "shS" not in loc:
            return None
        w = E.softmax(loc["z"][0]); s = np.asarray(loc["shS"][0]); e = np.asarray(loc["shA"][0])
        src = np.asarray(loc["sh_src"][0]); seen = np.asarray(loc["sh_seen"][0]); sk = np.asarray(loc["P"]["sh_src"], float)
        adj = np.asarray(loc["adj"][0]) if "adj" in loc else None
        cols = []
        for i, c in enumerate(COLORS):
            st = E.SH_STATES[i]; ai = E.ADJ_ID.get(st, -1)
            on = bool(adj is not None and 0 <= ai < len(adj) and adj[ai])
            frac = next(wd for top, wd in SH_FRAC if s[i] < top)
            how = st if on else f"{st} at times" if e[i] >= 0.2 else "hardly felt"
            en = [COLORS[j] for j in np.nonzero(E.ENEMY[i])[0]]
            words = (SH_HOLD[c], f"their {NOUN[c]} rules the rest", f"no {' or '.join(CNAME[x] for x in en)} to argue with",
                     "strain pressing on it")
            order = sorted((j for j in range(4) if src[i, j] >= SH_SRC_SHOW), key=lambda j: -sk[j] * src[i, j])
            cols.append(dict(c=c, state=st, part=round(float(s[i]), 3), force=round(float(e[i]), 3), on=on, seen=bool(seen[i]),
                             show=bool(s[i] >= SH_SHOW),
                             line=f"{CNAME[c]} {round(float(w[i]) * 100)}%, {frac} of it in shadow: {how}" if s[i] >= SH_SHOW else "",
                             src=[words[j] for j in order], src_v=[round(float(x), 3) for x in src[i]]))
        return dict(cols=cols, on=float(E.ADJ_ALL[E.ADJ_ID[E.SH_STATES[0]]][4]), off=float(E.ADJ_ALL[E.ADJ_ID[E.SH_STATES[0]]][5]))

    def shadow_pull(self, loc, k):
        """Item 2, the option card's mark: the colour whose shadow drives the heart's pick k, once the person has seen that
        shadow (seen[c]), else None. The shadow drives it when, without the shadow's overuse bonus (P sh_over x the option's
        colours x the force, the engine's own term on U_I), the heart would pick another option."""
        if k is None or k < 0 or not loc.get("SHON") or "shA" not in loc or "U_I" not in loc:
            return None
        e = np.asarray(loc["shA"][0]); m = np.asarray(loc["m"][0])
        ok = np.asarray(loc["seen"][0]) & ~np.asarray(loc["do_nothing"][0])
        if not ok[k]:
            return None
        shU = float(loc["P"]["sh_over"]) * (m @ e)
        alt = int(np.argmax(np.where(ok, np.asarray(loc["U_I"][0]) - shU, -np.inf)))
        if alt == k or shU[k] <= shU[alt]:
            return None
        c = int(np.argmax(m[k] * e))
        if m[k, c] * e[c] <= 0 or not bool(loc["sh_seen"][0][c]):
            return None
        return dict(c=COLORS[c], state=E.SH_STATES[c], icon=ADJ_LOOK.get(E.SH_STATES[c], ("dot", 0))[0])

    def states(self, loc=None):
        """The character's states now: the engine's adjectives (engine.ADJECTIVES, point 3), else the game's own reading."""
        loc = self.loc if loc is None else loc
        if loc is None:
            return []
        if "adj" in loc:
            t = float(loc.get("t", self.t))
            out, sh = [], []
            av = loc.get("adj_v")
            ADJ_T = getattr(E, "ADJ_ALL", E.ADJECTIVES)     # the 21 states, then the shadow states (held only with shadows on)
            SV = self.shadow_view(loc) or {}
            for i in np.nonzero(np.asarray(loc["adj"][0]))[0]:
                nm = E.ADJ_NAMES[i]; icon, good = ADJ_LOOK.get(nm, ("dot", 0))
                _, _, var, side, on, off, from_age, _, share = ADJ_T[i]
                d = dict(word=E.ADJ_SAY[i], name=nm, icon=icon, good=good, var=var, reads=ADJ_READS.get(var, var),
                         years=round(max(0.0, t - float(loc["adj_since"][0, i])) / 52, 1),
                         side=int(side), on=float(on), off=float(off), from_age=float(from_age), share=float(share),
                         scale=ADJ_SCALE.get(var, "pts"),
                         value=round(float(av[0, i]) * side, 4) if av is not None else None)
                if i >= len(E.ADJECTIVES):                  # a shadow state: its colour's line and sources for the hover
                    c_ = var[-1]; d.update(reads=f"the pull of the shadow on {CNAME.get(c_, c_)}", scale="of100",
                                           shadow=next((x for x in SV.get("cols", ()) if x["c"] == c_), None))
                    sh.append(d)
                else:
                    out.append(d)
            return sorted(out, key=lambda d: -d["good"])[:6] + sh    # a shadow state always shows, beside the others
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        X = self.conditions(loc)
        v = dict(content=float(loc["content"][0]), peace=float(loc["peace"][0]), stress=float(loc["stress"][0]),
                 mood=float(np.ravel(loc["mood"])[0]) if "mood" in loc else 0.0, want=float(loc["Q"][0]) / max(thr, 1e-9),
                 fortune=X.get("fortune", 0.0), trouble=X.get("trouble", 0.0),
                 **{RNAMES[i]: float(loc["res"][0, i]) for i in range(5)})
        young = int(loc["stage"][0]) < 2
        out, used = [], set()
        if min(v["fortune"], v["trouble"]) >= 1.8:      # both at once: a life of ups and downs, told by whichever is larger
            used.add("trouble" if v["fortune"] >= v["trouble"] else "fortune")
        for word, icon, good, var, op, t in STATES:
            if var in used or (young and var in ("money", "want")):
                continue
            x = v[var]
            hit = x >= t if op == ">=" else x <= t
            if hit:
                used.add(var)
                out.append(dict(word=word, icon=icon, good=good, var=var, name=STATE_NAME[var],
                                value=round(x, 3), level=round(abs(x - t) / max(abs(t), 0.1), 3)))
        return sorted(out, key=lambda d: -d["level"])[:5]

    def roles(self, loc=None):
        """The titles, statuses and perks the character holds now (None without the catalogue): titles by life domain
        (a community holds up to three), statuses, and perks held, suspended for a while, or rusty (a skill or credential
        no longer held that still helps a little while it fades)."""
        loc = self.loc if loc is None else loc
        GR = self.L.get("ROLES")
        if loc is None or GR is None or not loc.get("RON") or "r_has" not in loc:
            return None
        t = float(self.t); NT = GR["NT"]
        has = np.asarray(loc["r_has"][0]); since = np.asarray(loc["r_since"][0])
        yrs = lambda i: round(max(0.0, t - float(since[i])) / 52, 1)
        out = dict(titles={}, statuses=[], perks=[])
        prof = np.asarray(loc["r_prof"][0]) if "r_prof" in loc and "pwords" in GR else None
        refm = GR.get("REFM"); facets = []
        for i in np.nonzero(has[:NT])[0]:
            d = role_info(GR, i); d["years"] = yrs(i)
            if prof is not None and len(GR["pwords"][i]) > 1:      # a title held in one of its ways (its profile's words)
                d["profile"] = GR["pwords"][i][int(prof[i])] or None
            if refm is not None and GR["refines"][i] >= 0:         # a facet: held on top of a title, never in its socket
                facets.append(d)
            elif d["kind"] == "status":
                out["statuses"].append(d)
            else:
                out["titles"].setdefault(d["kind"], []).append(d)
        for d in facets:                                           # on the held title it sits on (the engine keeps one)
            on = next((x for xs in out["titles"].values() for x in xs if refm[d["i"], x["i"]]), None)
            if on is None:
                on = next((x for x in facets if x is not d and refm[d["i"], x["i"]]), None)   # a facet on a facet
            if on is not None:
                d["on"] = on["name"]; on.setdefault("facets", []).append(d)
            else:
                out["titles"].setdefault(d["kind"], []).append(d)
        flat = lambda x: [y for f in x.get("facets", []) for y in [f] + flat(f)]
        for xs in out["titles"].values():                          # a facet on a facet (raising a grandchild) joins the title
            for x in xs:
                if x.get("facets"):
                    x["facets"] = flat(x)
                    for f in x["facets"]:
                        f.pop("facets", None)
        acc = np.asarray(loc["p_acc"][0]); sus = np.asarray(loc["p_sus"][0]); lev = np.asarray(loc["p_lev"][0])
        rusty = []
        for p in range(GR["NP"]):
            i = NT + p
            if has[i]:
                d = role_info(GR, i); d.update(state="held", years=yrs(i))
            elif acc[p] and sus[p] > SUS_T:
                d = role_info(GR, i); d.update(state="suspended", back_in=round(max(0.0, float(sus[p]) - t) / 52, 1))
            elif lev[p] >= RUSTY and GR["half"][p] > 0:
                d = role_info(GR, i); d.update(state="rusty", level=round(float(lev[p]), 2)); rusty.append(d)
                continue
            else:
                continue
            out["perks"].append(d)
        kinds = list(PERK_ORDER)
        out["perks"].sort(key=lambda d: (d["state"] != "held", kinds.index(d["kind"]) if d["kind"] in kinds else 9, -d.get("years", 0)))
        out["perks"] += sorted(rusty, key=lambda d: -d["level"])[:4]
        out["statuses"].sort(key=lambda d: d["years"])
        return out

    def _role_need(self, nm):
        """What an option needs that the character lacks (explain.before's needs: a title, a perk or a state), in words."""
        GR = self.L.get("ROLES") or {}
        if nm in GR.get("ID", {}):
            d = role_info(GR, GR["ID"][nm])
        else:
            d = dict(name=nm, say=nm, kind="state", title=False, ways="", pred="is " + nm)
        d["line"] = f"only if {self.name} {d['pred']}"
        return d

    def _rung_below(self, loc, s):
        """The title that brings them to this moment (holds:, the rung below a bold try) and how long they have held it,
        or None (Emren 09:18: big titles come through consecutive steps)."""
        GR = self.L.get("ROLES")
        if GR is None or not hasattr(X, "title_held_index") or "r_since" not in loc:
            return None
        i = X.title_held_index(loc, 0, s)
        if i < 0:
            return None
        yrs = (float(loc["t"]) - float(np.asarray(loc["r_since"][0])[i])) / 52
        return dict(say=role_info(GR, i)["say"], years=int(max(yrs, 0)))

    def _role_fx(self, loc, s, k):
        """What an option can give or take (the Library's act fields: title, grants, drops, takes, suspends; each also
        _if_fails), in words: [dict(op, when, name, say, title, kind, gain, line)]."""
        GR = self.L.get("ROLES")
        fx = GR["A_FX"].get((int(s), int(k))) if GR is not None and loc.get("RON") else None
        out = []
        for when in ("ok", "fail"):
            for op, j, yrs in (fx or {}).get(when, ()):
                if j == getattr(batch_mod(), "MISSED_TITLE", -3):   # {missed}: the title their last long shot missed
                    mt = loc.get("missed_t")
                    j = int(mt[0]) if mt is not None else -1
                elif j < 0:                                     # {title}: the title held that brought them here
                    if j <= getattr(batch_mod(), "KIND_ACT", -10):   # kind:<kind> drops every title of a kind: not shown
                        continue
                    j = X.title_held_index(loc, 0, s) if hasattr(X, "title_held_index") else -1
                if j < 0:
                    continue
                d = role_info(GR, j); gain = op in ("title", "grants")
                tail = d["pred"] if gain else neg_of(d["pred"])
                if op == "suspends":
                    tail += f", for {'a year' if yrs <= 1 else f'{yrs:g} years'}"
                d.update(op=op, when=when, gain=gain,
                         line=("If it works: " if when == "ok" else "If it fails: ") + f"{self.name} {tail}" + (" from then on." if gain else "."))
                out.append(d)
        return out

    _recall_t = -10 ** 6    # week a memory coming back was last told

    @property
    def _recalled(self):
        """The old moments already told as memories (each comes back in the story once)."""
        if "_recalled_" not in self.__dict__:
            self._recalled_ = set()
        return self._recalled_

    def _recall(self, t, sev):
        """Engine v10's memory (E1, interpretation-memory.md): an act that hit hard can come back when the same moment
        returns or an act leans the same way, about 2.7 times a year. The story tells one now and then: no two within
        RECALL_GAP years, each old moment once, a scar whatever its strength, any other only when it comes back strong."""
        if t - self._recall_t < 52 * RECALL_GAP:
            return
        for ev in sev:
            rc = ev.get("recall")
            if not rc:
                continue
            key = (rc.get("age"), rc.get("choice"))
            if key in self._recalled or (not rc.get("scar") and float(rc.get("strength", 0)) < RECALL_MIN):
                continue
            self._recall_t = t; self._recalled.add(key)
            a = int(rc.get("age", 0)); what = act(str(rc.get("choice", "")))
            when = "as a child" if a < 12 else f"at {a}"
            kind = "scar" if rc.get("scar") else "good" if rc.get("success") else "bad"
            pool = RECALL_LINES[kind]
            line = pool[(int(t) * 7 + a) % len(pool)].format(when=when, When=when[:1].upper() + when[1:], what=what)
            icon = "ci-heartbreak" if kind == "scar" else "ci-diary"
            self._say(mk("O", f"memory|{icon}|1", self.story.fill(line)), 0 if not self.burn_in else 1, "memory", icon=icon)
            return

    def _family_faith(self, loc):
        """The engine gives an inherited faith a random profile; a chosen family faith replaces it."""
        F = E.KIDX["faith"]
        if self.faith_mix is None or not loc["held"][0, F]:
            return
        loc["prof"][0, F] = self.faith_mix
        for ev in loc["events"][0][::-1]:
            if "commitment" in ev and ev["commitment"].get("what") == "inherited":
                ev["commitment"]["profile"] = self.faith_mix.round(2).tolist()
                break

    def _on_end(self, t, loc):
        """Tell what happened this week. The story (story.py) tells it; with the ledger on (key l), the numbers follow."""
        if "wound" in loc:                          # v6: the year's hardest blow, and how supported they were then
            wd = float(loc["wound"][0])
            if wd > self._yr["wound"]:
                self._yr.update(wound=wd, support=float(loc["support"][0]))
        if GAME["own_ix"] and not self.burn_in and "a" in loc:   # S2: the color leading this week's act, for the yearly fade
            m_ = np.maximum(np.asarray(loc["m"][0, int(loc["a"][0])], float), 0)
            if m_.sum() > 0:
                self._ix_use[int(np.argmax(m_))] += 1
        evs = loc["events"][0]
        new = evs[self._ev_i:]; self._ev_i = len(evs)
        w_now = E.softmax(loc["z"][0]); res_now = loc["res"][0].copy()
        moved = {}
        if self._w_prev is not None:     # what this week moved: colors in points, means, as the browser's hover shows them
            moved = dict(dw=[round(float(x) * 100, 2) for x in w_now - self._w_prev],
                         dres={RNAMES[i]: round(float(res_now[i] - self._res_prev[i]), 3) for i in range(5)
                               if abs(res_now[i] - self._res_prev[i]) >= 0.005})
        self._w_prev = w_now; self._res_prev = res_now
        cpw = self._cp_week; self._cp_week = None
        tp, self._turn_pick = self._turn_pick, None
        if tp is not None:
            self._turning_end(t, loc, tp)
        L = self.L
        s = int(loc["s"][0]); sit = L["names"][s]
        stage = int(loc["stage"][0]); age = t / 52
        sev = [ev for ev in new if "situation" in ev]
        self._recall(t, sev)
        kills = self._kills(L, s)
        m = None
        if sev or cpw is not None:
            kind = KNAMES[int(loc["rk"][0])] if bool(loc["recon"][0]) else None
            m = cpw["cp"]["moment"] if cpw is not None else self.story.moment(t, sit, stage, age, kind, kills)
            if cpw is None and sev:
                self._far_moment(m, loc, s, sev[0])     # far_ties: the far moment's tie, town and event (Library slots)
                self._social_slots(m, loc, s, sev[0])   # v22.4: the places, post or price the moment is about
        GR = L.get("ROLES") if loc.get("RON") else None
        fold, folded = {}, set()      # a title that came with a commitment started this week is told in the commitment's line
        gained_now = set()            # titles gained this week: a facet that came with one (newlywed) shows on the HUD only
        if GR is not None:
            starts = {ev["commitment"]["kind"] for ev in new if "commitment" in ev and ev["commitment"]["what"] == "start"}
            for ev in new:
                r = ev.get("role")
                if r and r["what"] == "gained" and r["name"] in GR["ID"]:
                    gained_now.add(GR["ID"][r["name"]])
                if (r and r["what"] == "gained" and r["kind"] in starts and r["kind"] not in fold and r["name"] in GR["ID"]
                        and not ("refines" in GR and GR["refines"][GR["ID"][r["name"]]] >= 0)):
                    fold[r["kind"]] = role_info(GR, GR["ID"][r["name"]]); folded.add(id(r))
        if cpw is not None and age >= self.start_age:
            self._mark_threads(cpw, new, GR, age)
        if age >= self.start_age:
            self._world_effects(t, loc)               # WL1, WL5: what the world changed of theirs this week     # F5: what the pick started, for the moments that follow from it
        for ev in sev + [ev for ev in new if "situation" not in ev]:     # the moment first, then what followed from it
            self._met(age, ev, sit)
            if "situation" in ev:
                if m["ctx"].get("_dying") and not self.batch:   # the person in the scene is gone (the batch logs deaths itself)
                    self.story.scene(m)
                    self.story.dies(m["ctx"].get("_p_dead"))
                if cpw is not None:
                    o = cpw["cp"]["by_idx"][cpw["choice"]]
                    pushed = cpw["choice"] != cpw["own"]
                    f = self._force or {}
                    line = self.story.outcome(m, ev, L["labels"][s][cpw["choice"]], pushed, f.get("rel", 0.0) if pushed else 0.0,
                                              bool(f.get("closed")) if pushed else False, o["colors"])
                    rb = None
                    if "span" in loc and float(loc["span"][0]) > SPAN_TOLD:     # v6: joining opposed ways fits or tears
                        line += "\n" + self.story.rebound(bool(ev["success"]), float(loc["span"][0])); rb = bool(ev["success"])
                    if not ev["success"] and loc.get("SHON"):      # item 2: an act their shadow made fail is named
                        sl = self._shadow_fail(new, t)
                        if sl:
                            line += "\n" + sl
                    self.resolution = self._resolution(loc, cpw, ev, line, o, pushed, f.get("rel", 0.0) if pushed else 0.0, moved)
                    self.history["acts"].append((round(age, 1), o["colors"], bool(ev["success"]), bool(pushed)))   # the song's deeds
                    rs = self.resolution
                    rs["needs"] = self._needs_moved(loc, cpw["cp"]["snap"])
                    if pushed:
                        rs["hindsight"] = self._hindsight(loc, cpw, bool(ev["success"]), rs["needs"])
                        self._voice_trust_turn()
                    rs["pivot"] = self._pivot(loc, cpw, bool(ev["success"]), rs.get("hindsight"))
                    vo = self._voice_pick(loc, cpw, bool(ev["success"]), pushed, f.get("rel", 0.0) if pushed else 0.0, moved, rs)
                    if pushed and GAME["own_ix"]:       # S2: how far the pushed ways have become theirs
                        rs["own"] = self._own_push(loc, cpw, rs.get("hindsight"))
                    if vo:                              # item 3: their answer to the voice, and whether it was right
                        line = "\n".join(x for x in (vo[0], line, vo[1]) if x); rs["text"] = line
                    rs["say"] = "\n".join(x for x in (rs["say"], self.story.needs_line(rs["needs"]),
                                                        (rs.get("hindsight") or {}).get("line", "")) if x)
                    self._say(line, 0, "choice", sit=sit, ok=bool(ev["success"]), pushed=cpw["choice"] != cpw["own"],
                              colors=o["colors"], act=o["label"], rebound=rb, felt=round(o["felt"], 2), real=round(o["true"], 2),
                              rel=round(o["rel"], 2) if pushed else 0.0, delta=round(float(ev.get("delta", 0.0)), 2),
                              title=cpw["cp"]["title"], res=dict(became=rs["became"], closer=rs["closer"], surprise=rs["surprise"],
                                                                 heart=rs["with_heart"], head=rs["with_head"], regret=rs["regret"],
                                                                 lesson=rs["lessons"][0] if rs["lessons"] else None), **moved)
                    if self.ledger:
                        self._say(self._outcome_line(ev, cpw, loc), 0, "ledger")
                elif s == self.ORD:
                    line = self.story.ordinary(ev, L["labels"][s].index(ev["choice"]))
                    self._say(line, 2, "ordinary", colors=self._colors(loc, int(loc["a"][0])))
                elif sit in ("bereavement", "crisis or disaster") or kills:
                    col = self._colors(loc, int(loc["a"][0]))
                    self._say(self.story.told_moment(m, ev, col), 0, "loss" if (kills or sit == "bereavement") else "crisis",
                              sit=sit, ok=bool(ev["success"]), colors=col, delta=round(float(ev.get("delta", 0.0)), 2),
                              gate=ev.get("gate", ""), **moved)
                    if self.ledger:
                        self._say(self._choice_line(ev), 0, "ledger")
                elif self.detail >= 2:
                    col = self._colors(loc, int(loc["a"][0]))
                    self._say(self.story.told_moment(m, ev, col), 2, "moment", sit=sit, ok=bool(ev["success"]),
                              colors=col, delta=round(float(ev.get("delta", 0.0)), 2), gate=ev.get("gate", ""), **moved)
                elif (float(loc["L"]["STAKES"][s]) >= 1.0 and t - self._last_line.get(s, -10 ** 6) >= TOLD_GAP.get(sit, 104)
                      and not self.burn_in):
                    self._last_line[s] = t
                    col = self._colors(loc, int(loc["a"][0]))
                    self._say(self.story.told_moment(m, ev, col), 1, "moment", sit=sit, ok=bool(ev["success"]),
                              colors=col, delta=round(float(ev.get("delta", 0.0)), 2), gate=ev.get("gate", ""), **moved)
                    if self.ledger:
                        self._say(self._choice_line(ev), 1, "ledger")
                elif self.batch and L["src"][s].get("tier") == "everyday":   # untold everyday weeks still shape the year
                    self.story.tally(loc["m"][0, int(loc["a"][0])])
            else:
                line = None; tag = "note"; meta = {}
                if "outside" in ev:
                    o = ev["outside"]
                    line = self.story.outside(o, stage, 0 if self.burn_in else self.detail)   # the past is told briefly
                    tag = "move" if o["name"] == "moving somewhere new" else "outside"
                    meta = dict(source=o.get("source", ""), sit=o["name"],
                                took=round(float(o["took"]), 2) if o.get("took") is not None else None,
                                message=letters(np.asarray(o["message"], float)) if o.get("message") is not None else "")
                elif "era" in ev:
                    line = self.story.era(ev["era"]); tag = "era"
                    meta = dict(kind=ev["era"]["kind"], idea=ev["era"]["idea"], took=round(float(ev["era"]["took"]), 2))
                elif "commitment" in ev:
                    c = ev["commitment"]
                    ends = int(L["ENDS"][s]) if "ENDS" in L else -1
                    shown = m is not None and m["text"] is not None
                    if not (shown and c["what"] != "start" and ends >= 0 and KNAMES[ends] == c["kind"]):
                        line = self.story.commitment(c, m, fold.get(c["kind"]) if c["what"] == "start" else None)
                    else:
                        self.story.settle(c)            # the moment told it; the people still change
                    tag = "commitment"; meta = dict(kind=c["kind"], what=c["what"],
                                                    expects=letters(np.asarray(c["profile"], float)) if c.get("profile") else "")
                elif "clash" in ev:
                    line = self.story.clash(ev["clash"]); tag = "clash"; meta = dict(kind=ev["clash"]["kind"])
                elif "rite" in ev:
                    line = self.story.rite(ev["rite"], sit if sev or cpw is not None else None)
                    tag = "rite"; meta = dict(to=ev["rite"]["to"].replace("_", " "))
                elif "conversion" in ev:
                    line = self.story.conversion(ev["conversion"]); tag = "turn"
                elif "breakthrough" in ev:
                    line = self.story.breakthrough(ev["breakthrough"]); tag = "breakthrough"
                elif "death" in ev:
                    alone = ev["death"]["role"] == "partner" and not any(
                        "commitment" in e_ and e_["commitment"]["what"] == "widowed" for e_ in new)
                    line = self.story.death(ev["death"], m, age, alone); tag = "death"
                elif "mark" in ev:
                    self.story.mark(ev["mark"]["mark"], m)
                elif "goal" in ev:                      # v7: dreams, passions and plans
                    g = ev["goal"]
                    if age >= self.start_age:
                        self._plan_lean(loc, g)         # item 4, 5.4: picks lead to plans
                    gl = self.story.goal(g)
                    if gl:
                        quiet = g["what"] in ("pushed aside", "extended") or (g["kind"] == "plan" and g.get("horizon") == "week")
                        lvl = 2 if quiet else 1 if self.burn_in and g["kind"] == "plan" else 0
                        self._say(gl, lvl, "goal", kind=g["kind"], what=g["what"], domain=g.get("domain", ""),
                                  source=g.get("source", ""), horizon=g.get("horizon", ""), trigger=g.get("trigger", ""),
                                  colors=letters(np.asarray(g.get("mix", (0.2,) * 5), float)),
                                  dream=(self.story.dreams.get(int(g.get("id", 0))) or {}).get("name", ""))
                elif "world" in ev:                     # the outer world (spec 1 §8): big public events always; the rest when it
                    w0 = ev["world"]                    # touches them or their people
                    if "domain" not in w0:
                        recs = [w0]
                    elif w0.get("big") or loc.get("WL") is None:
                        recs = []                       # the engine's big ones are told once, by news()
                    else:                               # the engine's own record (WL.story): their town, their workplace, their people
                        recs = [dict(r_, self=bool(w0.get("self")), touches=[int(x_) for x_ in w0.get("touches") or []])
                                for r_ in from_engine(w0, loc["WL"].t0, EngineWorld.soc(loc["WL"]))]
                    for w_ in recs:
                        wd = self.world_data()
                        byid = {c_["id"]: c_ for c_ in wd[2]} if wd else {}
                        names = {p_["id"]: who_word(byid.get(p_["id"], p_), p_["name"])
                                 for p_ in self.wv.circle(wd[2], names=self.cast_names(wd[2])) if p_["layer"] <= 3} if wd else {}
                        wl = self.wv.line(w_, names)
                        if wl:                          # G2 (B package): the same world line is not told again within WORLD_AGAIN weeks
                            told = self.__dict__.setdefault("_wline_t", {})
                            if t - told.get((w_["kind"], wl[1]), -10 ** 6) < WORLD_AGAIN:
                                continue
                            told[(w_["kind"], wl[1])] = t
                            lvl = 0 if w_.get("big") or (w_.get("self") and w_["kind"] not in ("local_election", "crime_wave")) else \
                                2 if w_["kind"] == "local_election" else 1     # a council vote is for the detailed story only
                            self._say(mk("O", f"{w_['kind']}|{wl[0]}|{int(bool(w_.get('big')))}", self.story.fill(wl[1])),
                                      lvl, "world", kind=w_["kind"], icon=wl[0])
                elif "role" in ev and GR is not None and id(ev["role"]) not in folded and ev["role"]["name"] in GR["ID"]:
                    r = ev["role"]                      # a title or perk gained, lost, suspended or restored
                    d = role_info(GR, GR["ID"][r["name"]])
                    how = r["how"]
                    if how == "a partner at home, or the children grown":    # the rule's two reasons: say the one that holds
                        how = "a partner at home" if loc["held"][0, KNAMES.index("partner")] else "the children grown"
                    key = how.split(" ")[0] if how.startswith(("came ", "became ", "grew ", "through ")) else how
                    lvl = ROLE_QUIET.get(key, 0)
                    if r["what"] == "lost":
                        lvl = ROLE_QUIET_LOST.get(how, lvl)
                        if how.startswith("the ") and how.endswith(" ended"):
                            lvl = 9                     # a facet that ends with its title: the title's own line tells it
                    if (r["what"] == "gained" and "refines" in GR and GR["refines"][d["i"]] >= 0
                            and any(GR["REFM"][d["i"], j] for j in gained_now if j != d["i"] and j < GR["NT"])):
                        lvl = max(lvl, 2)               # newly married, the week of the wedding: the HUD shows it on the title
                    if not d["title"] and r["what"] != "suspended":
                        lvl = max(lvl, 1)               # perks: told at the normal level, titles always
                    if not d["title"] and t - self._role_told.get(r["name"], -10 ** 6) < ROLE_AGAIN:
                        lvl = max(lvl, 2)               # a perk that comes and goes (good for a loan) is told once in a while
                    if self.burn_in:
                        lvl += 1                        # the past before the chosen start age is told briefly
                    if lvl <= 2:
                        frm = how[len("grew from "):] if how.startswith("grew from ") else None
                        frm = GR["say"][GR["ID"][frm]] if frm in GR["ID"] else None
                        rl = self.story.title_line(r, d, frm)
                        if rl and lvl <= self.detail:
                            self._role_told[r["name"]] = t
                        if rl:
                            self._say(rl, lvl, "role", name=r["name"], kind=r["kind"], what=r["what"], how=how, title=d["title"],
                                      ways=d["ways"])
                elif "read" in ev:
                    r = ev["read"]
                    lvl = 2 if self.burn_in else 1 if (r["impact"] >= READ_TOLD and t - self._last_read >= READ_GAP
                                                       and t - self._read_told.get(r["name"], -10 ** 6) >= 5 * 52) else 2
                    if lvl <= self.detail:
                        self._last_read = t; self._read_told[r["name"]] = t
                        r = self._disaster_read(r)      # WL6: the disaster that happened, not always a flood
                        self._say(self.story.read(r, stage), lvl, "read", sit=r["name"], reading=r.get("reading", ""),
                                  impact=round(float(r.get("impact", 0.0)), 2))
                elif "sphere_lever" in ev:              # spheres phase 4 (sph_levers): their act on the town's sphere
                    self._lever_told(t, loc, ev["sphere_lever"])
                elif "cast" in ev and ev["cast"].get("kind") in ("far", "taken in", "want"):
                    self._far_told(t, loc, ev["cast"])  # far_ties: a close tie's news, a tie taken in, a want's cause
                elif "cast" in ev and ev["cast"].get("kind") == "talk":
                    self._talk_told(t, loc, ev["cast"])  # S3: a go-between brings a place's word on them
                elif "cast" in ev and ev["cast"].get("kind") == "sacred":
                    self._line_told(t, ev["cast"])      # S5: a sacred line forms
                elif isinstance(ev.get("seen"), dict) and ev["seen"].get("kind") == "dream":
                    self._seen_dream_told(t, ev["seen"])   # S6: a dream seeded from someone they watched
                if line:
                    self._say(line, 0, tag, **meta)
                    if self.ledger:
                        old = self._event_line(ev)
                        if old:
                            self._say(old, 0, "ledger")
        if self.batch and "alive" in loc and loc.get("WL") is not None and (self._kin_t is None or t - self._kin_t >= 4
                                                                     or int(loc["alive"][0, 1]) > len(self.story.alive("sibling"))):
            self._kin_sync(t, loc)          # the family the world was born into, a new sibling the week it comes, else monthly
        if self.batch and "alive" in loc and loc["alive"].shape[1] > 5 and self.story.alive("child"):   # R15: a later child is one more in the family
            for _ in range(int(loc["alive"][0, 5]) - len(self.story.alive("child"))):
                self._say(self.story.later_child(), 0 if not self.burn_in else 1, "kin")
        self._force = None

    def _choice_line(self, ev):
        ok = "it worked" if ev["success"] else "it went badly"
        line = f"  {ev['age']:5.1f}  {ev['situation']}: {self.name} chose to {ev['choice']} ({ok})."
        if ev.get("gate") and ev["gate"] != "chosen" and ev.get("wanted") and ev["wanted"] != ev["choice"]:
            why = {"pulled away": "habit pulled them away", "unnoticed": "it never crossed their mind",
                   "lacked the means": "they lacked the means", "not offered": "it wasn't on offer"}.get(ev["gate"], ev["gate"])
            line += f" They wanted to {ev['wanted']}, but {why}."
        return line

    def _outcome_line(self, ev, cpw, loc):
        cp = cpw["cp"]; o = cp["by_idx"][cpw["choice"]]
        ok = "It worked." if ev["success"] else "It went badly."
        if cpw["choice"] == cpw["own"]:
            who = f"{self.name} did what they leaned toward: {o['label']}."
        else:
            who = f"You pushed {self.name} to {o['label']}."
        line = f"  {ev['age']:5.1f}  >> {who} {ok}"
        if self._force is not None and cpw["choice"] != cpw["own"]:
            acc = self._force.get("acc") or accept_word(self._force["rel"])
            if acc in ("reluctant", "against it"):
                line += f" It wasn't their choice ({acc}): stress and pent-up wanting rise."
            elif acc == "okay with it":
                line += " It wasn't their choice, but they were okay with it."
            if self._force["closed"] and not ev["success"]:
                line += " Forcing what was out of reach backfired: more stress, some money lost."
        return line

    def _event_line(self, ev):
        n = self.name
        if "outside" in ev:
            o = ev["outside"]; took = o.get("took")
            tail = ""
            if took is not None and o.get("message"):
                msg = letters(o["message"])
                tail = (f" It pulled their wanting toward {msg}." if took > 0.3 else
                        f" They pushed back against its {msg} message." if took < -0.3 else f" It left them unmoved.")
            return f"  {o['age']:5.1f}  [{o['source']}] {o['name'][0].upper() + o['name'][1:]}.{tail}"
        if "era" in ev:
            e = ev["era"]; took = e["took"]
            react = "embrace it" if took > 0.3 else "resist it" if took < -0.3 else "shrug it off"
            return f"  {e['age']:5.1f}  [the times] A {e['kind']} era of {e['name']} ({e['idea']}) begins. {n} tends to {react}."
        if "commitment" in ev:
            c = ev["commitment"]; kind = c["kind"]; what = c["what"]
            prof = letters(c["profile"]) if c.get("profile") else ""
            if what == "start":
                return f"  {c['age']:5.1f}  [title] {n} takes on a {kind}, through \"{c.get('through', '')}\". It expects {prof}."
            if what == "inherited":
                return f"  {c['age']:5.1f}  [title] {n} is raised inside the family faith, which expects {prof}."
            words = {"left": f"{n} walks away from their {kind}.", "lost job": f"{n} loses their job.",
                     "retired": f"{n} retires.", "widowed": f"{n}'s partner dies."}
            return f"  {c['age']:5.1f}  [title] " + words.get(what, f"{kind}: {what}.")
        if "clash" in ev:
            c = ev["clash"]
            return f"  {c['end']:5.1f}  [clash] The clash with their {c['kind']} (since {c['start']:.1f}) ends: {c['how']}."
        if "rite" in ev:
            r = ev["rite"]
            if r.get("quiet"):
                return f"  {r['age']:5.1f}  [stage] {n} grows quietly into a {r['to'].replace('_', ' ')}."
            return f"  {r['age']:5.1f}  [stage] A rite of passage: {n} becomes a {r['to'].replace('_', ' ')} ({r['event']})."
        if "conversion" in ev:
            c = ev["conversion"]
            return (f"  {c['age']:5.1f}  [turning point] {n} loses faith in {CNAME[c['disowned']]} ways "
                    f"and turns toward {letters(c['toward'])}.")
        if "breakthrough" in ev:
            b = ev["breakthrough"]
            return (f"  {b['age']:5.1f}  [breakthrough] Pent-up wanting breaks through: {n} moves toward "
                    f"{letters(b['want'])}.")
        return None

    def _shadow_fail(self, new, t):
        """Item 2: "<State>: <clause>." for an act that failed because of the shadow (the engine's "shadow" event this week),
        in the Library's words (earth_story.SHADOW_FAIL); "" without them."""
        sh = next((e["shadow"] for e in new if "shadow" in e), None)
        W = getattr(ES, "SHADOW_FAIL", None) if ES is not None else None
        if sh is None or not W or not W.get(sh["state"]):
            return ""
        pool = W[sh["state"]]
        return self.story.fill(f"{sh['state'][:1].upper()}{sh['state'][1:]}: {pool[int(t) % len(pool)]}.")

    def _shadow_year(self, t, loc):
        """Item 2: the yearly chapter's line when a shadow state comes on (grow) or goes off (fade), in the Library's words
        (earth_story.SHADOW_YEAR). Only with the engine's shadows switch on; the first year sets what is known."""
        W = getattr(ES, "SHADOW_YEAR", None) if ES is not None else None
        if not loc.get("SHON") or "adj" not in loc or not W:
            return
        adj = np.asarray(loc["adj"][0])
        for st in E.SH_STATES:
            i = E.ADJ_ID.get(st, -1)
            on = bool(0 <= i < len(adj) and adj[i])
            was = self._sh_told.get(st)
            self._sh_told[st] = on
            if was is None or was == on or self.burn_in or not W.get(st):
                continue
            pool = W[st]["grow" if on else "fade"]
            self._say(self.story.fill(pool[(int(t) // 52) % len(pool)]), 1, "shadow", state=st, on=on)

    def _yearly(self, t, loc):
        if GAME["own_ix"] and not self.burn_in:
            self._own_year()
        w = E.softmax(loc["z"][0]); M = float(loc["M"][0])
        lbl = E.identity(w, M, self._prev_label); self._prev_label = lbl
        self.seen_labels.add(lbl)
        c, p = float(loc["content"][0]), float(loc["peace"][0])
        self.history["content"].append((t / 52, c)); self.history["peace"].append((t / 52, p)); self.history["label"].append((t / 52, lbl))
        self.history["w"].append((t / 52, [round(float(x), 3) for x in w]))
        # the story's voice: present identity blended with a fading memory of past ones (story.py)
        self.story.update_voice(w)
        self._shadow_year(t, loc)
        vl = self._core_label                       # 5.5: the chapter names who they have settled into, and who they are becoming
        self._becoming_year()
        if vl != self._voice_label:                 # a new identity in the telling: a short phrase for it
            eps = EPITHETS.get(vl, [])
            self._epithet = eps[len(self._named) % len(eps)] if eps else ""
            self._named.add(vl)
        ident = (ident_name(vl) + (f", {self._becoming or self._epithet}" if self._becoming or self._epithet else "")) if vl else ""
        self._voice_label = vl
        self.history["name"].append((t / 52, vl, self._becoming))
        self._say("", 0)
        head, _, body = self.story.chapter(t / 52, int(loc["stage"][0]), w, c, p, ident).partition("\n")
        self.log.append(head)
        self.feed.append(dict(tag="chapter", text="", age=int(round(t / 52)), stage=STAGES[int(loc["stage"][0])].replace("_", " "),
                              label=vl, guild=ident_name(vl) if vl else "", epithet=self._epithet if vl else "",
                              becoming=self._becoming if vl else "",
                              w=[round(float(x), 3) for x in w], content=round(c, 2), peace=round(p, 2),
                              voice=[round(float(x), 3) for x in self.story.voice], weeks=self.story.last_weeks))
        if body:
            self._say(body, 0, "year")
        self._voice_chapter(t / 52)
        self._times_year()                          # WL4: one line on how the times touched them this year
        self._year_notes(t, loc)
        if self.batch and "alive" in loc and loc.get("WL") is None:   # grandparents of grown-up grandchildren die outside
            # the Library's moments (with the outer world on, _kin_sync says it once the engine's record is overdue)
            line = self.story.quiet_deaths("grandparent", int(loc["alive"][0, 3]), t / 52)
            if line:
                self._say(line, 0 if not self.burn_in else 1, "death")
        if self.ledger:
            held = [KNAMES[k] for k in range(len(KNAMES)) if loc["held"][0, k]]
            cols = " ".join(f"{COLORS[i]}{w[i] * 100:3.0f}" for i in range(C))
            voice = " ".join(f"{COLORS[i]}{self.story.voice[i] * 100:3.0f}" for i in range(C))
            self._say(f"   [now {label_name(lbl) if lbl else 'unformed'} | {cols} | voice {voice} | content {c:.2f} peace {p:.2f}"
                      + (f" | {', '.join(held)}" if held else "") + "]", 0, "ledger")
        self._temperament_news(t, loc)

    def _name_week(self, w, loc):
        """5.5 (implementation list item 4; chroma-ideas/gameplay-feel.md): the name says who they have settled into, the
        identity of the colors held over the last four years, read week by week with the usual hold (a color joins above
        .22 and leaves below .18). Measured on lives left alone: 3.6 name changes after 18, against 13.9 for the
        yearly reading."""
        if len(self._wring) == NAME_WEEKS:
            self._wsum -= self._wring[0]
        self._wring.append(np.asarray(w, float)); self._wsum += self._wring[-1]
        if "M" in loc:
            was = self._core_label
            self._core_label = E.identity(self._wsum / len(self._wring), float(loc["M"][0]), self._core_label)
            if self._core_label != was:
                self._voice_became(self._core_label)

    def _becoming_year(self):
        """5.5: who they are becoming, once a year: the color that rose most over the last three years when it rose by
        BECOMING or more ("growing curious"), else a color of the name that fell as much ("loosening their hold on
        order"). Said once it has held two readings (F4), so it reads as news: about a third of adult years or less."""
        W = self.history["w"]
        cand = None
        if self._core_label and len(W) > BECOMING_YEARS:
            d = np.asarray(W[-1][1]) - np.asarray(W[-1 - BECOMING_YEARS][1])
            up, dn = int(np.argmax(d)), int(np.argmin(d))
            if d[up] >= BECOMING:
                cand = ("grow", COLORS[up])
            elif d[dn] <= -BECOMING and COLORS[dn] in self._core_label:
                cand = ("fade", COLORS[dn])
        shown = cand if cand is not None and cand == self._becoming_c else None
        self._becoming_c = cand
        self._becoming = "" if shown is None else (GROW_WORDS if shown[0] == "grow" else FADE_WORDS)[shown[1]]

    def _year_notes(self, t, loc):
        """Engine v6 loops, told once a year when they clearly happened: after a hard blow, support heals or its lack
        hardens; trouble and fortune come in streaks."""
        yr, age = self._yr, t / 52
        self._yr = dict(wound=0.0, support=0.0)
        if yr["wound"] >= WOUND_TOLD and not self.burn_in and t - self._after_t >= 4 * 52:
            if yr["support"] >= 0.75:
                self._say(self.story.aftermath(True, age, yr["wound"], yr["support"]), 0, "healed", wound=round(yr["wound"], 2),
                          support=round(yr["support"], 2)); self._after_t = t
            elif yr["support"] <= 0.4:
                self._say(self.story.aftermath(False, age, yr["wound"], yr["support"]), 0, "hardened", wound=round(yr["wound"], 2),
                          support=round(yr["support"], 2)); self._after_t = t
        if "trouble" in loc and t - self._streak_t >= 5 * 52 and not self.burn_in:
            tr, fo = float(loc["trouble"][0]), float(loc["fortune"][0])
            if tr >= STREAK_TOLD and tr > fo:
                self._say(self.story.streak(True, tr), 0, "trouble", streak=round(tr, 2)); self._streak_t = t
            elif fo >= STREAK_TOLD:
                self._say(self.story.streak(False, fo), 0, "fortune", streak=round(fo, 2)); self._streak_t = t

    # how much each part of temperament must move before the log says so, and the words for up and down
    TEMPER = (("react", 0.25, "more easily shaken", "harder to shake"),
              ("steady", 0.35, "steadier in who they are", "less sure of who they are"),
              ("base_mood", 0.1, "more content by nature", "less content by nature"),
              ("outlook", 0.12, "more sure that effort pays off", "less sure that effort pays off"))

    def _temperament_news(self, t, loc):
        """Temperament is never set by the player; it forms from the life lived. Say when it has clearly moved."""
        if "react" not in loc or t < 6 * 52:
            return
        now = {k: float(loc[k][0]) for k, *_ in self.TEMPER}
        if self._temper_told is None:
            self._temper_told = now
            return
        moved = []; keys = []
        for k, step, up, down in self.TEMPER:
            d = now[k] - self._temper_told[k]
            if abs(d) >= step:
                moved.append(up if d > 0 else down); keys.append(f"{k}{d:+.2f}"); self._temper_told[k] = now[k]
        if moved:
            self._say(self.story.temperament(moved, keys), 0, "temper", temper={k: round(v, 2) for k, v in now.items()})

    # ------------------------------------------------------------------ status
    def status(self):
        loc = self.loc
        if loc is None:
            return "Not started."
        w = E.softmax(loc["z"][0]); a = E.softmax(loc["y"][0])
        kw = E.softmax(loc["k"][0]); habit = loc["habit"][0]
        hs = habit / max(habit.sum(), 1e-9) if habit.sum() > 0 else np.full(C, 0.2)
        rsh = (loc["held"][0] * loc["I"][0]) @ loc["prof"][0]
        role = rsh / rsh.sum() if rsh.sum() > 0 else np.full(C, 0.2)
        inertia = 0.4 * kw + 0.3 * hs + 0.3 * role - 0.2
        doors = loc["doors"](loc["nic"], loc["res"])[0]
        ready = float(loc["plast"][0] * loc["ctrl"][0])
        acc = ready * (loc["SE"][0] / 0.5) * doors
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        Q = float(loc["Q"][0])
        young = int(loc["stage"][0]) < 2
        lbl = self._core_label                   # 5.5: the name, from the last four years' colors
        now = E.identity(w, float(loc["M"][0]), self._prev_label)
        L = []
        L.append(f"{self.name}, age {self.age():.1f}, {STAGES[int(loc['stage'][0])].replace('_', ' ')}. Identity: {label_name(lbl)}"
                 + (f", {self._becoming}" if self._becoming else "") + "."
                 + (f" This year alone: {label_name(now)}." if now and now != lbl else ""))
        L.append("")
        L.append("           " + "  ".join(f"{CNAME[c]:>6}" for c in COLORS))
        L.append("position   " + "  ".join(f"{v * 100:5.0f}%" for v in w) + "   where they are")
        L.append("demand     " + "  ".join(f"{d * 100:+5.0f} " for d in a - w) + "   where they want to move")
        L.append("inertia    " + "  ".join(f"{d * 100:+5.0f} " for d in inertia) + "   how hard they hold on")
        L.append("accelerat. " + "  ".join(f"{v * 100:5.0f}%" for v in acc) + "   how fast they could move now")
        L.append("skill      " + "  ".join(f"{v * 100:5.0f}%" for v in loc["sig"][0]) + "   skillset")
        L.append("belief     " + "  ".join(f"{v * 100:5.0f}%" for v in loc["SE"][0]) + "   mindset: belief they can act that way")
        L.append("lens       " + "  ".join(f"{v * 100:5.0f}%" for v in kw) + "   mindset: what they notice first")
        L.append("voice      " + "  ".join(f"{v * 100:5.0f}%" for v in self.story.voice) + "   how the story is told (past and present identity)")
        L.append("")
        st = self.states(loc)
        if st:
            L.append("state        " + ", ".join(x["word"] for x in st))
        L.append(f"satisfaction {float(loc['content'][0]) * 100:.0f}%   peace {float(loc['peace'][0]) * 100:.0f}%   "
                 f"strain {float(loc['stress'][0]) * 100:.0f}%   pent-up wanting {Q / max(thr, 1e-9) * 100:.0f}% of breaking through"
                 + (" (once a young adult)" if young else ""))
        cond = self.conditions(loc)
        if cond:
            L.append("around them  " + ", ".join(f"{CTX_WORDS[k]}: {around_word(CTX_WORDS[k], v)}" for k, v in cond.items() if abs(v) >= 0.05))
        if "react" in loc:
            L.append(f"temperament  reactivity {float(loc['react'][0]) * 50:.0f}%   steadiness {float(loc['steady'][0]) * 100:.0f}%   "
                     f"baseline mood {float(loc['base_mood'][0]) * 100:.0f}%   outlook {float(loc['outlook'][0]) * 100:.0f}%")
        L.append("resources    " + "  ".join(f"{RNAMES[i]} {loc['res'][0, i] * 100:.0f}%" for i in range(5)))
        if "need" in loc:
            L.append("needs        " + "  ".join(f"{NEED_WORD[n]} {float(v) * 100:.0f}% ({need_level_word(float(v))})"
                                                for n, v in zip(E.NEEDS, loc["need"][0])))
        if self.history["forced"]:
            L.append("trust in you " + "  ".join(f"{CNAME[c]} {v * 100:+.0f}" for c, v in zip(COLORS, self.trust))
                     + f"   (pushes accepted {self.history['accepted']}, resented {self.history['resented']})")
        held = [k for k in range(len(KNAMES)) if loc["held"][0, k]]
        R = self.roles(loc)
        if held:
            for k in held:
                yrs = (self.t - loc["since"][0, k]) / 52
                cl = " - in a clash" if loc["clash0"][0, k] >= 0 else ""
                nm = ", ".join(x["say"] + "".join(f" ({f['say']})" for f in x.get("facets", []))
                               for x in (R["titles"].get(KNAMES[k], []) if R else []))
                L.append(f"title        {KNAMES[k]}{': ' + nm if nm else ''}: {yrs:.0f} years, invested {invest_word(float(loc['I'][0, k]))}, "
                         f"expects {letters(loc['prof'][0, k])}{cl}")
        else:
            L.append("titles       none yet")
        if R and R["statuses"]:
            L.append("status       " + ", ".join(x["say"] for x in R["statuses"]))
        if R and R["perks"]:
            L.append("perks        " + "; ".join(x["pred"] + {"held": "", "suspended": " (on hold for now)", "rusty": " (rusty)"}[x["state"]]
                                                for x in R["perks"]))
        for x in self.goals(loc):
            tail = (f" ({x['horizon']}, due at {x['due']:.0f}; feels {x['felt'] * 100:.0f}%, plans like it come true {x['hint']}; "
                    f"{x['progress'] * 100:.0f}% of the way)" if x["kind"] == "plan" else f" [{x['colors']}]")
            L.append(f"{x['kind']:<12} {x['name']}{tail}, strength {x['strength'] * 100:.0f}%" + (" [your plan]" if x["by_player"] else ""))
        return "\n".join(L)

    def hud(self):
        """Everything the browser's HUD shows, as plain numbers and words (status() is the same for the terminal)."""
        loc = self.loc
        d = dict(name=self.name, age=round(self.age(), 1), setting=self.setting, place=self.story.place,
                 freq=self.freq, detail=self.detail, ledger=self.ledger, over=self.over)
        if loc is None:
            return d
        w = E.softmax(loc["z"][0]); a = E.softmax(loc["y"][0])
        kw = E.softmax(loc["k"][0]); habit = loc["habit"][0]
        hs = habit / max(habit.sum(), 1e-9) if habit.sum() > 0 else np.full(C, 0.2)
        rsh = (loc["held"][0] * loc["I"][0]) @ loc["prof"][0]
        role = rsh / rsh.sum() if rsh.sum() > 0 else np.full(C, 0.2)
        inertia = 0.4 * kw + 0.3 * hs + 0.3 * role - 0.2
        doors = loc["doors"](loc["nic"], loc["res"])[0]
        acc = float(loc["plast"][0] * loc["ctrl"][0]) * (loc["SE"][0] / 0.5) * doors
        dyn = X.dynamics(loc, 0, self._prev_label) if hasattr(X, "dynamics") else None
        if dyn is not None:                          # the engine's own weekly feed (next hand-off), when the pin has it
            inertia = np.asarray(dyn["inertia"]); acc = np.asarray(dyn["accelerator"])
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        lbl = self._core_label                   # 5.5: the name, from the last four years' colors
        r = lambda v: [round(float(x), 3) for x in v]
        vl = self._voice_label
        d.update(stage=STAGES[int(loc["stage"][0])].replace("_", " "),
                 label=lbl, guild=ident_name(lbl), magic=magic_name(lbl), meaning=ident_meaning(lbl),
                 voice_label=vl, voice_guild=ident_name(vl) if vl else "", epithet=self._epithet if vl else "",
                 becoming=self._becoming if lbl else "", voice_row=self.voice_view(loc),
                 w=r(w), demand=r(a - w), inertia=r(inertia), acc=r(acc), skill=r(loc["sig"][0]), belief=r(loc["SE"][0]),
                 lens=r(kw), voice=r(self.story.voice),
                 content=round(float(loc["content"][0]), 3), peace=round(float(loc["peace"][0]), 3),
                 stress=round(float(loc["stress"][0]), 3), want=round(float(loc["Q"][0]), 2), want_thr=round(thr, 2),
                 young=int(loc["stage"][0]) < 2,
                 res={RNAMES[i]: round(float(loc["res"][0, i]), 3) for i in range(5)},
                 around={CTX_WORDS[k]: round(float(v), 2) for k, v in self.conditions(loc).items() if abs(v) >= 0.05},
                 around_words={CTX_WORDS[k]: around_word(CTX_WORDS[k], float(v)) for k, v in self.conditions(loc).items() if abs(v) >= 0.05},
                 states=self.states(loc))
        shv = self.shadow_view(loc)
        if shv is not None:                          # item 2: light and shadow, only with the engine's shadows switch on
            d["shadow"] = shv
        if dyn is not None:
            d["dyn"] = dict(openness=dyn["openness"], window=bool(dyn["window"]), near=dyn["near"], bands=dyn["bands"],
                            parts={k: r(v) for k, v in dyn["inertia_parts"].items()}, readiness=dyn["readiness"])
        d["season_x"] = self.season(loc)
        d["sex"] = self.sex_now(loc)
        gv = self.gender_view(loc)
        d["sexword"] = gv["word"]; d["who"] = gv["rows"]
        if "react" in loc:
            d["temper"] = {k: round(float(loc[k][0]), 2) for k in ("react", "steady", "base_mood", "outlook")}
        d["needs"] = {n: round(float(v), 3) for n, v in zip(E.NEEDS, loc["need"][0])} if "need" in loc else {}
        d["need_thin"] = GAME["need_thin"]
        d["trust"] = self.trust_view(); d["pushes"] = dict(forced=self.history["forced"], accepted=self.history["accepted"],
                                                           resented=self.history["resented"])
        d["inner"] = {k: round(float(np.ravel(loc[v])[0]), 3) for k, v in (("self_control", "dsc"), ("mood", "mood"), ("wound", "wound"),
                                                                          ("gap", "gap_r"), ("horizon", "hzf"), ("formed", "M"))
                      if v in loc}
        d["week"] = int(self.t % 52)
        d["season"] = season_of(self.t)
        d["ident_rule"] = [0.22, 0.18]              # a color joins who they are above .22 and leaves below .18 (engine.identity)
        d["titles"] = [dict(kind=KNAMES[k], years=round((self.t - loc["since"][0, k]) / 52, 1), invested=round(float(loc["I"][0, k]), 2),
                            expects=letters(loc["prof"][0, k]), clash=bool(loc["clash0"][0, k] >= 0))
                       for k in range(len(KNAMES)) if loc["held"][0, k]]
        R = self.roles(loc)
        if R is not None:                           # the titles inside each life domain, statuses, and perks
            g_ = gv["self"]
            gw = lambda x: ({k: gw(v) for k, v in x.items()} if isinstance(x, dict) else [gw(v) for v in x] if isinstance(x, list)
                            else self.gword(x, g_))
            for t_ in d["titles"]:
                t_["named"] = gw(R["titles"].get(t_["kind"], []))
            d["statuses"] = gw(R["statuses"]); d["perks"] = R["perks"]
        d["cast"] = [dict(id=p["id"], name=p["name"], role=p["role"], alive=p["alive"], met=p.get("met"), seen=p.get("seen", 0))
                     for p in self.story.people if p["introduced"]]
        d["spark"] = [[round(a_, 1), round(c_, 2), round(p_, 2)] for (a_, c_), (_, p_) in
                      zip(self.history["content"][-90:], self.history["peace"][-90:])]
        # the life so far, year by year, for the timeline: age, the five colors, satisfaction, peace, identity
        d["river"] = [[round(a_, 1)] + w_ + [round(c_, 2), round(p_, 2), l_] for (a_, w_), (_, c_), (_, p_), (_, l_) in
                      zip(self.history["w"], self.history["content"], self.history["peace"], self.history["label"])]
        d["guilds"] = dict({k: v for k, v in IDENT_NAME.items() if k}, **{l_: ident_name(l_) for _, l_ in self.history["label"] if l_})
        d["goals"] = self.goals()
        pv = self.places_view()
        if pv:
            d["places"] = pv
        try:
            ln = self._lines_view()                     # S5: the lines they will not cross, while sacred is on
        except Exception:
            ln = None
        if ln:
            d["lines"] = ln
        wd = self.world_data()
        if wd:                                          # the outer world: the named cast by layer, and reach by standing
            d["circle"] = self.wv.circle(wd[2], self.t, self.cast_names(wd[2])); d["reach"] = self.wv.reach(wd[3])
            self._want_why_rows(d["circle"])
            era = (wd[0] or {}).get("era")
            if era:
                from worldview import letters_of, era_name
                ls = letters_of(era.get("colors", era.get("letters", "W")))
                d["world_era"] = dict(letters=ls, name=era_name(ls))
        return d

    # ------------------------------------------------------------------ v7: dreams, passions and plans
    # ------------------------------------------------------------------ point 1: the everyday life between moments
    CIRCLE = ((r"choir|singer|music", "the choir"), (r"club|organiser", "the club"), (r"team|league|rescue", "the team"),
              (r"church|congregation|worship|deacon|elder|faith", "the congregation"), (r"garden", "the community garden"),
              (r"union", "the union"), (r"party|campaign|activist|advocate|rights|cause", "the campaign"),
              (r"volunteer|kitchen|shelter", "the volunteers"), (r"radio", "the radio station"), (r"co-?op|committee|resident", "the residents' committee"))

    def _routine_ctx(self):
        loc = self.loc; held = loc["held"][0]; age = self.age(); K = {k: held[i] for i, k in enumerate(KNAMES)}
        R = self.roles(loc) or dict(titles={}, statuses=[], perks=[])
        adj = {E.ADJ_NAMES[i] for i in np.nonzero(np.asarray(loc["adj"][0]))[0]} if "adj" in loc else set()
        who = lambda *roles: next((p for r in roles for p in self.story.alive(r) if p["introduced"]), None)
        slot = {}
        partner, child, friend, parent = who("partner"), who("child"), who("friend"), who("mother", "father")
        for k, p in (("partner", partner), ("child", child), ("friend", friend), ("parent", parent)):
            if p is not None:
                slot[k] = mk("p", p["id"], p["name"])
        job = (R["titles"].get("career") or [None])[0]
        if job is not None:
            j_ = STATUS_WORD.get(job["name"], job["say"])          # with its article: "life as an office worker"
            slot["job"] = j_ if re.match(r"(a|an|the) ", j_) else an(j_)
        com = (R["titles"].get("community") or [None])[0]
        if com is not None or K.get("community"):
            nm = com["name"] if com else ""
            slot["circle"] = next((w for pat, w in self.CIRCLE if re.search(pat, nm)), "the circle" if self.setting == "tribal"
                                  else "the guild" if self.setting == "magic" else "the group")
        stats = {d["name"] for d in R["statuses"]}
        need = set()
        if K.get("career") and "job" in slot:
            need.add("career")
        if 5 <= age < 18 or (age < 26 and any("student" in d["name"] for xs in R["titles"].values() for d in xs)):
            need.add("student")
        if "retiree" in stats or (age >= 66 and not K.get("career")):
            need.add("retired")
        need |= {k for k in ("partner", "children", "faith", "community") if K.get(k) and (k not in ("partner", "children")
                                                                                         or (k == "partner" and partner) or (k == "children" and child))}
        if not K.get("partner") and age >= 18:
            need.add("no_partner")
        if friend:
            need.add("friend")
        if parent:
            need.add("parent_alive")
        need |= {a for a in ("poor", "wealthy", "stressed", "happy", "unhappy", "lonely", "calm", "restless") if a in adj}
        if float(loc["res"][0, 2]) < 0.45:
            need.add("in_poor_health")
        w = E.softmax(loc["z"][0])
        return dict(age=age, world=self.story.wcode, need=need, color=COLORS[int(np.argmax(w))], season=season_of(self.t), slot=slot)

    def routine(self, n=8):
        """Everyday lines for the interlude: what keeps happening in their life at this age (drawn once a year from routine.py,
        with its own seeded stream, so the telling never changes the life or the rest of the story)."""
        if RT is None or self.loc is None or self.over:
            return dict(age=int(self.age()), lines=[])
        a = int(self.age())
        if getattr(self, "_rout", None) is not None and self._rout["age"] == a:
            return self._rout
        ctx = self._routine_ctx()
        cands, wts = [], []
        for text, when in RT.ROUTINE:
            lo, hi = when.get("age", (0, 200))
            if not (lo <= ctx["age"] < hi) or ctx["world"] not in when.get("world", "ETM"):
                continue
            nd = when.get("need", ())
            if any(x not in ctx["need"] for x in nd) or (when.get("season") and when["season"] != ctx["season"]):
                continue
            if when.get("color") and when["color"] != ctx["color"]:
                continue
            cands.append(text); wts.append(1.0 + len(nd) + (1.0 if when.get("color") else 0) + (0.5 if when.get("season") else 0))
        rng = np.random.default_rng(self.seed * 1009 + a)
        k = min(n, len(cands))
        pick = rng.choice(len(cands), size=k, replace=False, p=np.array(wts) / sum(wts)) if k else []
        lines = []
        for i in pick:                      # only {N} and {place} are left for fill(), which never touches the cast for them
            x = re.sub(r"\{(partner|child|friend|parent|job|circle)\}", lambda m: ctx["slot"].get(m.group(1), "\x00"), cands[i])
            if "\x00" not in x and not re.search(r"\{(?!N\}|Ns\}|place\})\w+\}", x):
                lines.append(self.story.fill(x))
        self._rout = dict(age=a, lines=lines, season=ctx["season"], color=ctx["color"])
        return self._rout

    def take_trace(self):
        """The colors (and where they want to be) week by week since the page last asked: [[t, W..G, want W..G], ...]."""
        out, self._trace = self._trace, []
        return out

    _kin_t = None           # week the story's family was last matched to the world's
    KIN_WAIT = 12           # weeks a death in the world waits for the engine's own record before the story says it

    def _kin_sync(self, t, loc):
        """With the outer world on, the family is the world's: siblings there at the birth are met quietly as older
        ones, a younger one born later is told; a sibling the world lost without a moment is said goodbye to."""
        first = self._kin_t is None
        self._kin_t = t
        n_e = int(loc["alive"][0, 1]); have = len(self.story.alive("sibling"))
        if n_e > have:
            wd = self.world_data()
            sib = sorted((p_ for p_ in (wd[2] if wd else []) if "sibling" in p_.get("roles", []) and p_.get("alive")),
                         key=lambda p_: -int(p_.get("born_t", 0)))
            sexes = [("f" if p_.get("sex") == "female" else "m") for p_ in sib[:n_e - have]]
            line = self.story.new_kin("sibling", n_e - have, sexes, told=not first and t / 52 >= 1)
            if line:
                self._say(line, 0 if not self.burn_in else 1, "kin")
        if first:
            return
        gap = self.__dict__.setdefault("_kin_gap", {})
        for role, n_w in (("sibling", n_e), ("grandparent", int(loc["alive"][0, 3]))):
            if n_w >= len(self.story.alive(role)):
                gap.pop(role, None)
            elif t - gap.setdefault(role, t) >= self.KIN_WAIT:   # the engine's own record of the death (told with its moment)
                gap.pop(role, None)                         # follows the world's within weeks; after KIN_WAIT, say it
                line = self.story.quiet_deaths(role, n_w, t / 52)
                if line:
                    self._say(line, 0 if not self.burn_in else 1, "death")

    NEWS_GAP = 8 * 52       # one public figure's scandals, rises and falls: the story tells one in this many weeks

    def _world_news(self, r):
        """A big public event of the engine's world, told in the story (spec 1 §8: big public events always). The timeline
        keeps every one; the story does not repeat the same figure's news within NEWS_GAP weeks, nor the same line within two years."""
        wl = self.wv.line(r, {})
        told = self.__dict__.setdefault("_news_t", {})
        key = (r["kind"], r["figure"]) if r.get("figure") is not None else wl[1] if wl else None
        if key is not None and self.t - told.get(key, -10 ** 6) < (self.NEWS_GAP if r.get("figure") is not None else 104):
            return
        if key is not None:
            told[key] = self.t
        if wl:
            self._say(mk("O", f"{r['kind']}|{wl[0]}|1", self.story.fill(wl[1])), 0 if not self.burn_in else 1, "world", kind=r["kind"], icon=wl[0])

    world_source = None     # the engine's outer world: a callable, hidden week -> (snapshot, record, cast, standing); None until it lands
    _wloc = None            # the locality they live in, as last told

    def _world_place(self, WL, birth=False):
        """Where a life begins and where it moves to (spec 3 §2.5b, §2.6: drawn, discovered as the story opens). birth:
        at the start, the story's birth line names the place (no line of its own)."""
        try:
            pv = WL.PP.place_view(0)
        except Exception:
            return
        from worldview import place_name, loc_key
        l = loc_key(pv.get("society", 0), pv.get("loc", 0))
        if l == self._wloc:
            return
        name = place_name(self.wv.seed, l, self.setting)
        kind = str(pv.get("kind", "")).replace("_", " ")
        a_kind = an(kind) if kind else ""
        if birth:
            self._wloc = l
            self.story.birth_place = mk("O", "place|ci-cottage|1", name + (f", {a_kind}" if a_kind else ""))
            return
        soc, home = pv.get("society", 0), pv.get("home_society", 0)
        was = self.__dict__.get("_wsoc", home); self._wsoc = soc
        abroad = soc is not None and soc != home        # emigration (W35-3): the society they move to, and coming home
        where = (f", {a_kind}" if a_kind else "") + (f" in {self.wv.society_name(soc)}" if abroad else "")
        if self._wloc is None:
            line = f"{{N}} is born in {name}" + (f", {a_kind}" if a_kind else "") + "."
        elif abroad and soc != was:
            line = f"{{N}} moves abroad, to {name}{where}."
        elif not abroad and was not in (None, home):
            line = f"{{N}} comes home, to {name}" + (f", {a_kind}" if a_kind else "") + "."
        else:
            line = f"{{N}} moves to {name}{where}."
        first = self._wloc is None
        self._wloc = l
        tag, icon = ("world", "ci-cottage") if first else ("move", "ci-box")
        self._say(mk("O", f"place|{icon}|1", self.story.fill(line)), 0 if not self.burn_in else 1, tag, kind="place", icon=icon)

    def cast_names(self, cast):
        """One family, one set of names: the world's kin (parents, siblings, partner, children, grandparents) take the names
        the story already gave them, matched by role and sex; once matched, a person keeps the name for the life."""
        m = self.__dict__.setdefault("_castname", {})
        used = set(m.values())
        ROLE = dict(parent=("mother", "father"), sibling=("sibling",), partner=("partner",), child=("child",), grandparent=("grandparent",))
        from story import FEM_REF, MAS_REF
        for p in cast:
            if p.get("id") in m:
                continue
            r = next((x for x in ("partner", "parent", "child", "sibling", "grandparent") if x in p.get("roles", [])), None)
            if r is None:
                continue
            sx = "f" if p.get("sex") == "female" else "m"
            roles = ROLE[r] if r != "parent" else (("mother",) if sx == "f" else ("father",))
            def q_sex(q):
                return "f" if FEM_REF.search(q["ref"]) else "m" if MAS_REF.search(q["ref"]) else None
            cs = [q for q in self.story.people if q["role"] in roles and q["name"] not in used]
            cs = [q for q in cs if q_sex(q) in (sx, None)] or cs
            cs.sort(key=lambda q: q["alive"] != bool(p.get("alive", True)))
            if cs:
                m[p["id"]] = cs[0]["name"]; used.add(cs[0]["name"])
        return m

    def world_save(self):
        """The world this life leaves behind, for a later life to begin in (spec 1: legacy worlds): the world's whole
        state, and the character's cast for a grandchild's line. None without a world."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        if WL is None:
            return None
        d = dict(key=f"{int(WL.W._seed)}-{int(WL.t0)}-{int(WL.W.t)}", seed=int(WL.W._seed), name=self.name,
                 age=round(self.age(), 1), alive=getattr(self, "died", None) is None, world=WL.W.save())
        try:
            w = np.asarray(self.loc["w"][0], float) if "w" in self.loc else None
            d["people"] = WL.PP.save(0, w=w, alive=False)
        except Exception:
            pass
        return d

    def places_view(self):
        """Item 15's player view, "your places": the haunts they go to (the Library's name for the place, its kind, the face
        that leads it, whether a setting of theirs meets there), their standing in each sphere they have climbed in, and the
        town's spheres by their share of the hours. Display only; empty while the engine's sphere switches are off."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        if WL is None or ESP is None:
            return None
        try:
            hi = WL.PP.haunts_info(0)
        except Exception:
            return None
        if not hi["haunts"] and not hi["rungs"]:
            return None
        nm = lambda d, k: (d.get(k) or {}).get("name", k)
        haunts = []
        for h in hi["haunts"]:
            H = ESP.HAUNT.get(h["kind"], {}); ns = H.get("names") or [nm(ESP.PLACE, h["kind"])]
            haunts.append(dict(name=ns[h["name"] % len(ns)], kind=nm(ESP.PLACE, h["kind"]), sphere=h["sphere"],
                               sphere_name=nm(ESP.SPHERE, h["sphere"]), lead=h["leads"][-1], lead_name=nm(ESP.FACE, h["leads"]),
                               lead_line=(ESP.FACE.get(h["leads"]) or {}).get("line", ""), faces=h["faces"],
                               keeper=H.get("keeper", ""), setting=h["setting"]))
        LADDER = ["newcomer", "regular", "known", "pillar", "leader"]       # world_keys.LADDER, the engine's order
        rungs = [dict(sphere=s_, sphere_name=nm(ESP.SPHERE, s_), rung=LADDER.index(r_), word=ESP.RUNG[s_][LADDER.index(r_)],
                      question=(ESP.SPHERE.get(s_) or {}).get("question", ""))
                 for s_, r_ in hi["rungs"].items() if r_ in LADDER and s_ in ESP.RUNG]
        rungs.sort(key=lambda r: -r["rung"])
        town = []
        try:
            l = int(WL.PP.loc[0]); sp = WL.W._sph_portrait() if getattr(WL.W, "sph_s", None) is not None else []
            sp = next((x["spheres"] for x in sp if x["town"] == l), {})
            town = sorted((dict(sphere=s_, sphere_name=nm(ESP.SPHERE, s_), hours=v["hours"], lead=v["leads"][-1],
                                lead_name=nm(ESP.FACE, v["leads"])) for s_, v in sp.items()), key=lambda x: -x["hours"])
        except Exception:
            town = []
        P = dict(haunts=haunts, rungs=rungs, town=town)
        try:
            self._social_places(WL, hi, P)              # v22.4 (S1, S3, S4, S7): only while their switches are on
        except Exception:
            pass
        return P

    def world_data(self):
        """What the outer world shows now (world-hooks-for-engine.md), or None while the engine has no world."""
        if self.world_source is None:
            return None
        try:
            return self.world_source(self.t)
        except Exception:
            return None


    def goals(self, loc=None):
        """The dreams, passions and plans the character holds now; a plan comes with its foreseen outcome (foresee.py):
        the felt odds, and reality only as a rough hint, as Emren asked."""
        loc = self.loc if loc is None else loc
        if loc is None or "gk" not in loc:
            return []
        out = []
        for j in np.nonzero(loc["gk"][0] >= 0)[0]:
            kind = E.G_KINDS[int(loc["gk"][0, j])]; d = int(loc["gd"][0, j]); mix_ = loc["gm"][0, j]
            g_d, g_p, verb = self.story.goal_words(kind, KNAMES[d] if d >= 0 else "", mix_, int(loc["gid"][0, j]))
            item = dict(j=int(j), id=int(loc["gid"][0, j]), kind=kind, name={"dream": g_d, "passion": g_p}.get(kind, verb),
                        domain=KNAMES[d] if d >= 0 else "", colors=letters(np.asarray(mix_, float)),
                        strength=round(float(loc["gs"][0, j]), 2), source=E.G_SOURCES[int(loc["gsrc"][0, j])],
                        by_player=bool(loc["gby"][0, j]))
            info = self.story.dreams.get(item["id"])
            if info:                                # a dream the engine named from the Library's catalogue
                item["dream"] = info["name"]
            if kind == "plan":
                f = F.foresee(loc, 0, j)
                item.update(felt=f["felt"], hint=f["hint"], horizon=f["horizon"], due=f["due_age"], progress=f["progress"],
                            left_out=f["left_out"], felt0=f["felt_at_start"])
                life = self.story.life_words(item["id"]) if f["horizon"] == "life" else None
                if life:
                    item["name"] = life
            out.append(item)
        order = dict(passion=0, plan=1, dream=2)
        return clean(sorted(out, key=lambda x: (order[x["kind"]], -x["strength"])))

    def _paused_locals(self):
        """The engine's locals where the run waits now (a plan made here takes effect from this week)."""
        return self._msg[2] if self._msg is not None and not self.over else None

    def plan_preview(self, horizon="year", domain=None, mix=None):
        S = self._paused_locals()
        if S is None or "gk" not in S:
            return None
        if domain and S["held"][0, KNAMES.index(domain)]:
            return dict(blocked=f"{self.name} already has {'a ' + domain if domain != 'children' else 'children'}")
        f = F.preview(S, 0, horizon, domain, mix)
        f["name"] = self.story.goal_words("plan", domain or "", np.asarray(F._mix(S, 0, None if mix is None else np.asarray(mix, float))), 0)[2]
        return clean(f)

    def plan_add(self, horizon="year", domain=None, mix=None):
        S = self._paused_locals()
        if S is None or "gk" not in S:
            return -1, "plans need engine v7"
        j, f = F.add_plan(S, 0, horizon, domain, None if mix is None else np.asarray(mix, float))
        return j, clean(f)

    def plan_drop(self, j):
        S = self._paused_locals()
        return S is not None and F.drop_plan(S, 0, int(j))

    def cp_hud(self, numbering):
        """The pending checkpoint for the browser: the scene, and each option with its odds and what may follow."""
        cp = self.pending
        if cp is None:
            return None
        rev = {v: k for k, v in numbering.items()}
        meta = self.sitmeta.get(cp["sit"], {}); tags = meta.get("tags", []); marks = meta.get("marks", [])
        opts = []
        for o in cp["options"]:
            col = o["colors"]
            means, _, ends = col.partition(">")
            v = cp.get("view") or {}
            opts.append(dict(n=rev.get(o["idx"]), label=o["label"], colors=col,
                             means=[] if col == "-" else means.split("+"), ends=[] if col == "-" else (ends or means).split("+"),
                             felt=round(o["felt"], 3), hint=o["hint"], lean=round(o["lean"], 3), status=o["status"],
                             rel=round(o["rel"], 3), rel_word=rel_word(o["rel"]), why=o["why"], commit=o["commit"],
                             clash=o.get("clash", []),
                             own=o["idx"] == cp["own"], follows=o["follows"],
                             reality=o.get("reality"), heart=o.get("heart"), head=o.get("head"), drivers=o.get("drivers"),
                             heart_pick=o["idx"] == v.get("heart"), head_pick=o["idx"] == v.get("head"),
                             accept="their own pick" if o["idx"] == cp["own"] else o.get("acc") or accept_word(o["rel"]), k=int(o["idx"]),
                             trust=round(o.get("trust", 0.0), 3), resent=round(self._resent(o["rel"] * o.get("era_k", 1.0), o.get("trust", 0.0)), 3),
                             era=o.get("era", 0.0), wcause=o.get("wcause"),
                             needs=o.get("needs"), closed=o.get("closed"), helped=o.get("helped", []), roles_fx=o.get("roles_fx", []),
                             base=round(o["base"], 2) if o.get("base") is not None else None,
                             tag=tags[o["idx"]] if o["idx"] < len(tags) else "",
                             mark=marks[o["idx"]] if o["idx"] < len(marks) else ""))
            if o.get("seen"):                           # S6, only while seen_done is on
                opts[-1]["seen"] = o["seen"]
        sp = self.shadow_pull(self.loc, (cp.get("view") or {}).get("heart")) if self.loc is not None else None
        if sp is not None:                           # item 2: once seen, the heart's pick their shadow drives carries a mark
            for o in opts:
                if o["heart_pick"]:
                    o["shadow"] = sp
        # a perk that helps most of this moment's options says little on each row: the row names one that helps only a few
        cnt = {}
        for o in opts:
            for h in o["helped"]:
                if h.get("plus", 0) >= 3:
                    cnt[h["name"]] = cnt.get(h["name"], 0) + 1
        for o in opts:
            o["helped_row"] = next((h["name"] for h in o["helped"] if h.get("plus", 0) >= 3 and cnt[h["name"]] <= 2), None)
        st = cp["stakes"]
        v = cp.get("view")
        voice = None if v is None else dict(key=v["key"], line=v["line"], asides=v["asides"], self_control=v["self_control"],
                                            heart_driver=v["heart_driver"], head_driver=v["head_driver"], color=v["voice_color"])
        return dict(age=round(cp["age"], 1), title=cp["title"], stakes=round(st, 2), season=self.season(),
                    stake_word="very high" if st >= 1.2 else "high" if st >= 0.95 else "moderate",
                    scene=cp.get("scene", ""), extra=cp.get("extra", ""), thought=cp.get("thought", ""), recon=cp["recon"],
                    thread=cp.get("thread"), era=self.era_view(), options=opts, voice=voice, art=dict(sit=cp["sit"], life=meta.get("life", ""), tier=meta.get("tier", ""),
                                                         tone=meta.get("tone", ""), variant_of=meta.get("variant_of", ""), recon=cp["recon"]))

    def season(self, loc=None):
        """Emren's point 6: the crossing they are in (a stage or a new title), in words, or None (engine explain.season)."""
        loc = self.loc if loc is None else loc
        need = ("s", "sea_k", "sea_t0", "sea_done", "t", "P", "L")
        x = X.season(loc, 0) if loc is not None and hasattr(X, "season") and all(k in loc for k in need) else None
        if not x:
            return None
        into = STAGE_WORD.get(x["name"], x["name"].replace("_", " ")) if x["kind"] == "stage" else x["name"]
        return dict(kind=x["kind"], into=into, step=int(x["step"]), step_word=SEASON_STEP.get(int(x["step"]), ""),
                    this_week=x["this_week"], transform=x["transform"], weeks_in=x["weeks_in"], weeks_left=x["weeks_left"])

    def _idv(self, loc, k):
        """One of the engine's per-person identity values (for-the-engine.md §6), or None while the pin has none. The
        engine keeps some under its own names in the week's state (chroma-engine/sex-gender.md): ID_LOCAL maps them."""
        if loc is None:
            return None
        if k not in loc and k in ID_LOCAL:
            name, col = ID_LOCAL[k]
            if name not in loc:
                return None
            v = np.asarray(loc[name]); v = np.ravel(v[0] if v.ndim >= 2 else v)     # (1, k) per person, (1,) or a scalar
            x = v[col] if col is not None and v.size > col else v[0] if v.size else None
            if x is None:
                return None
            x = x.item() if hasattr(x, "item") else x
            if k == "role_fit":
                return 1 - float(x)
            if k == "role_strict" and "faith_given" in loc and "I" in loc:    # plus half a strongly held family faith
                try:
                    x = min(1.0, float(x) + 0.5 * float(np.ravel(loc["faith_given"])[0]) * float(np.asarray(loc["I"])[0, E.KIDX["faith"]]))
                except Exception:
                    pass
            return x
        if k not in loc:
            return None
        v = np.ravel(np.asarray(loc[k]))
        return v[0].item() if v.size else None

    def _found(self, loc, k):
        """Whether the character has found this about themselves by now (the engine's found_* week, never before)."""
        w = self._idv(loc, "found_" + k)
        return w is not None and 0 <= w <= self.t

    def _mark(self, loc, name):
        L = self.L
        if loc is None or name not in L.get("MARKS", []) or "mark_n" not in loc:
            return False
        return bool(np.asarray(loc["mark_n"])[0][L["MARKS"].index(name)] > 0)

    def gender_view(self, loc=None):
        """Who they are, as far as the story has found it (N1d): the role their world expects (f, m or x for the words),
        how they name themselves, and the sheet's lines. Nothing hidden shows before the week it is found."""
        loc = self.loc if loc is None else loc
        raised = self.sex_now(loc)
        rs = {"female": "f", "male": "m"}.get(raised)
        inter = bool(self._idv(loc, "intersex")) if self._idv(loc, "intersex") is not None else self.born_intersex
        gs = self._idv(loc, "gender_self") if self._found(loc, "gender") else None
        named = self._mark(loc, "named their gender")
        own = None
        if gs is not None and gs > 0:
            own = "x" if gs == 2 else {"f": "m", "m": "f"}.get(rs)
        selfg = own if (own and named) else rs
        acc = self._idv(loc, "accept_trans"); acc = ACCEPT0.get(self.setting, 0.5) if acc is None else acc
        seen = own if (own and named and acc >= 0.5) else rs
        age = self.age()
        rows = []
        if rs:
            rows.append(["Born", ("intersex, raised as " + {"f": "a girl", "m": "a boy"}[rs]) if inter else {"f": "a girl", "m": "a boy"}[rs],
                         "The body they were born with, chosen at setup or drawn at real rates."])
        elif inter:                         # before the first week: the engine has not yet drawn how they are raised
            rows.append(["Born", "intersex", "The body they were born with, chosen at setup or drawn at real rates."])
        if gs is not None:
            g_ = own or rs
            word = {"f": "a woman", "m": "a man", "x": "neither, or both"}.get(g_, "")
            how = "" if gs == 0 else (", and lives as themselves" if named else ", told a few" if self._mark(loc, "came out") else ", known only to them")
            rows.append(["Knows themselves as", word + how, "Who they know themselves to be. Found in play at real rates, never chosen and never changed by what they do."])
        at = self._idv(loc, "attr") if self._found(loc, "attr") else None
        if self._found(loc, "ace") and self._idv(loc, "ace"):
            rows.append(["Drawn to", "no one in that way", "Who they are drawn to, as the story found it."])
        elif at is not None and rs:
            o, s_ = ("men", "women") if rs == "f" else ("women", "men")
            out = "" if at < 2 else (", and out" if self._mark(loc, "came out") else ", not out")
            rows.append(["Drawn to", DRAWN[int(at)].format(o=o, s=s_) + out, "Who they are drawn to, as the story found it."])
        st = self._idv(loc, "role_strict"); st = ROLE_STRICT0.get(self.setting, 0.3) if st is None else st
        fit = self._idv(loc, "role_fit")
        rows.append(["What their world expects", strict_word(st) + ("" if fit is None or not rs else ", and " + fit_word(fit)),
                     "How firmly their world, their family's faith and the people around them expect them to live as a "
                     + ("girl or woman" if seen == "f" else "boy or man" if seen == "m" else "girl or a boy") + " should here, and how that sits with them. "
                     "Living outside it costs more where the world is strict."])
        return dict(raised=rs, self=selfg, seen=seen, word=age_word(selfg, age), seen_word=age_word(seen, age), rows=rows,
                    strict=st, named=named, own=own)

    def gword(self, text, g=None):
        """Two-word titles in the character's own words: wife or husband, mother or father... (N1d §3)."""
        if not isinstance(text, str) or " or " not in text:
            return text
        g = g or (self.gender_view()["self"] if self.loc is not None else None)
        k = {"f": 0, "m": 1, "x": 2}.get(g)
        return text if k is None else TWO_RE.sub(lambda m_: TWO_WORD[m_.group(1)][k], text)

    def rename(self, new):
        """A new name the character takes when they name their gender (N1d §4); the story uses it from now on."""
        new = (new or "").strip()[:24]
        if not new or new == self.name:
            return False
        old = self.name
        self.name = new; self.story.name = new
        self.history.setdefault("names", []).append((round(self.age(), 1), old, new))
        self._say(f"From now on, {new}.", 0, "moment")
        if isinstance(self.resolution, dict):
            self.resolution.pop("rename", None)
        return True

    def sex_now(self, loc=None):
        """'female' or 'male' as set up or drawn by the engine (None before the run has it)."""
        loc = self.loc if loc is None else loc
        if loc is None or "female" not in loc:
            return self.sex
        return "female" if bool(np.asarray(loc["female"])[0]) else "male"

    def _title_now(self, loc):
        """The title that brings them to this moment, for the Library's {title} slot (engine next hand-off)."""
        self.story.title_now = X.title_held(loc, 0) if hasattr(X, "title_held") and "s" in loc else None

    def _on_death(self, t, loc):
        """The character's own death (engine P["self_death"]): the story tells it and the life ends here."""
        died = loc.get("died") or []
        cause = died[-1][2] if died else "illness"
        age = int(t / 52)
        if cause.startswith("through "):
            how = f"after choosing to {cause[len('through '):]}"
        else:
            how = {"illness": "of an illness", "old age": "of old age"}.get(cause, cause)
        self._say(f"{self.name} dies at {age}, {how}.", 0, "death")
        self.died = dict(age=round(t / 52, 1), cause=cause, how=how)
        self.over = True; self.result = None
        self._life_review()
        return "over"

    def _gift_fit(self, o):
        """How well a chosen act fits what they are good at: their mean skill in the ways it uses, against their best
        skill (1 = their strongest way). None for doing nothing."""
        if self.loc is None or "sig" not in self.loc or not o.get("colors") or o["colors"] == "-":
            return None
        ways = [c for c in o["colors"].partition(">")[0].split("+") if c in COLORS]
        sig = np.asarray(self.loc["sig"][0], float)
        if not ways or sig.max() <= 0:
            return None
        return float(np.clip(np.mean([sig[COLORS.index(c)] for c in ways]) / sig.max(), 0, 1))

    # ------------------------------------------------------------------ the Book of Moments (Emren chose "Book and peace", 21:44)
    def life_id(self):
        first = self.history["names"][0][1] if self.history.get("names") else self.name   # a new name keeps the life's id
        return f"{self.seed}-{first}-{self.setting}-{int(self.start_age)}"

    def book(self):
        """What this life has met so far, for the Book of Moments the page keeps across lives: moments (situations and
        life events), deeds (the engine's marks), titles ever held, identities lived. Keys match book_catalog()."""
        o = self.result if self.over and self.result is not None and "sit_n" in self.result else None
        loc = self.loc
        if o is None and loc is None:
            return None
        L = self.L
        sit_n = np.asarray((o or loc)["sit_n"][0])
        mom = ["s|" + L["names"][i] for i in np.nonzero(sit_n > 0)[0] if L["names"][i] != "an ordinary week"]
        evr = [e_["name"] for e_ in L.get("EVR", [])]
        mom += ["e|" + n_ for n_ in dict.fromkeys(evr[int(j)] for _, _, j, _ in (o or loc)["read_log"] if int(j) < len(evr))]
        mk_n = np.asarray(o["marks"]["n"][0] if o is not None else loc.get("mark_n", np.zeros((1, 0)))[0])
        deeds = [L["MARKS"][i] for i in np.nonzero(mk_n > 0)[0]] if len(mk_n) else []
        titles = []
        GR = L.get("ROLES")
        if GR is not None:
            ever = o["roles"]["ever"][0] if o is not None and o.get("roles") else loc.get("r_ever", [None])[0]
            if ever is not None:
                titles = [GR["names"][i] for i in np.nonzero(np.asarray(ever)[:GR["NT"]])[0]]
        idents = list(dict.fromkeys(l_ for _, l_ in self.history["label"] if l_))
        d = dict(id=self.life_id(), name=self.name, setting=self.setting, start=round(self.start_age, 1), age=round(self.age(), 1),
                 over=bool(self.over), moments=mom, deeds=deeds, titles=titles, idents=idents,
                 long=list(dict.fromkeys(("made|" if x["made"] else "missed|") + x["name"] for x in self.history["long"])))
        if self.over and getattr(self, "review", None):
            r = self.review
            d.update(final=r["final_label"], reading=r["reading"])
        v = self.history["voice"]                    # item 3: the Book's Your Voice page adds the lives up
        d["voice"] = dict(n=v["n"], steer=v["steer"], ax=v["ax"], line=(getattr(self, "review", None) or {}).get("voice", {}).get("book", "")
                          if self.over else "")
        return d

    def _life_review(self):
        h = self.history
        adult = [c for a, c in h["content"] if a >= 18]; adultp = [p for a, p in h["peace"] if a >= 18]
        ful = float(np.mean(adult)) if adult else 0.0
        ser = float(np.mean(adultp)) if adultp else 0.0
        integ = 1 - float(np.sum(h["rel"])) / max(h["picks"], 1) if h["picks"] else 1.0
        if GAME["own_ix"] and h["picks"] and len(h["rel_way"]) == len(h["rel"]):   # S2: a push in a way that became theirs
            integ = 1 - sum(r * (1 - (float(np.asarray(wy) @ self.ix) if wy is not None else 0.0))   # counts as their own by it
                            for r, wy in zip(h["rel"], h["rel_way"])) / h["picks"]
        o = self.result
        w = o["w"][0] if o is not None else E.softmax(self.loc["z"][0])
        labels = [l for _, l in h["label"]]
        path = []
        for l in labels:
            if not path or path[-1] != l:
                path.append(l)
        gifts = float(np.mean(h["gift"])) if h["gift"] else None
        self.review = dict(epitaph=self.story.epitaph(w), fulfilment=ful, serenity=ser, integrity=integ, gifts=gifts,
                           final=label_name(labels[-1] if labels else ""), final_label=labels[-1] if labels else "",
                           path=[ident_name(l) for l in path if l], path_labels=[l for l in path if l], paths=len({l for l in labels if l}),
                           forced=h["forced"], own=h["own"], accepted=h["accepted"], resented=h["resented"], trust=self.trust_view(),
                           age=round(self.age(), 1), died=getattr(self, "died", None),
                           long_shots=[dict(say=x["say"], made=x["made"], age=x["age"], odds=x["odds"], words=x["words"]) for x in h["long"]])
        self.review["reading"] = peace_reading(ful, ser, integ, gifts)
        self.review["story"] = life_paragraph(self.story.fill("{N}"), h, self.review, self.setting)
        cl = self._lines_closing()                           # S5: how their sacred lines stood at the end
        if cl:
            self.review["story"] += "\n\n" + cl
        self.review["voice"] = self.voice_review(h)          # item 3: the voice's last sentence and the Book's line
        vr = self.review["voice"] or {}
        if vr.get("end"):                                    # the voice's last sentence closes the song, before the last talk
            self.review["story"] += "\n\n" + vr["end"]
        # the last conversation with the voice (earth_story.py LAST_TALK) has no place of its own on the page yet: its own
        # field, and the song's last stanza after a blank line
        h.setdefault("voice", voice_empty())["share"] = vr.get("share", 0.0)
        self.review["last_talk"] = last_talk(self.story.fill("{N}"), self.story.fill("{Ns}"), h, self.review, self.setting)
        if self.review["last_talk"]:
            self.review["story"] += "\n\n" + self.review["last_talk"]


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
# LEAD_WAY: the five ways to lead in the game's words (the Library has moments for them, no table of names yet), W U B R
# G; LEAD_LEGIT: legitimacy in words, best first (under .2 a post falls). LEAD_PLACE: the plain name of what a leading
# title leads (world_people.LEAD_TITLES), the moments' {place}; SETTING_PLACE the same for a setting they lead;
# SPHERE_PLACE the last resort, by sphere. SEEN_ROW: S6's row shows on an option on a path (a title it gives or aims at)
# for every word, on one in a colour way only when they saw that way go wrong (nearly every life has seen each way done,
# the Engine's own finding); SEEN_MARK: the row's short word (the page marks none only on the hover)
FAIR_SIDE = (0.5, 0.65)
TALK_AGAIN, TALK_QUIET = 52, 8
LEAD_WAY = dict(rules=("by fair rules", "W"), knowing=("by knowing best", "U"), favours=("by favours owed", "B"),
                inspiring=("by inspiring them", "R"), custom=("as one of them, keeping to custom", "G"))
LEAD_LEGIT = [(0.7, "firmly accepted"), (0.45, "accepted"), (0.2, "doubted"), (0.0, "losing their hold")]
LEAD_PLACE = {"head of government": "the government", "minister": "the ministry", "party leader": "the party",
              "member of parliament": "the seat in parliament", "mayor": "the town hall", "local councillor": "the council",
              "lay judge": "the bench", "research group leader": "the research group",
              "community centre manager": "the community centre", "artistic director": "the company",
              "shift manager": "the shift", "head chef": "the kitchen", "founder of a firm": "the firm",
              "union rep": "the union branch", "shop owner": "the shop", "café or bar owner": "the café",
              "community theatre director": "the community theatre", "deacon or elder": "the congregation",
              "team captain": "the team", "community-garden coordinator": "the community garden",
              "parent-association organiser": "the parents' association", "book-club organiser": "the book club",
              "board-game club organiser": "the games club", "neighbourhood-watch coordinator": "the neighbourhood watch",
              "festival organiser": "the festival", "volunteer research organiser": "the volunteer research group",
              "disability-rights organiser": "the rights group", "campaign organiser": "the campaign",
              "founder of a movement": "the movement"}
SETTING_PLACE = dict(work="the workplace", congregation="the congregation", club="the club", gang="the crew",
                     unit="the unit", movement="the movement", **{"class": "the class", "member_led": "the group"})
SPHERE_PLACE = dict(rule="the council", gather="the hall", arts="the company", faith="the congregation", care="the clinic",
                    learn="the school", prod="the works", comm="the business", prot="the station")
SEEN_ROW = dict(path=("seen", "none", "wrong", "far"), way=("wrong",))
SEEN_MARK = dict(seen="seen it done", wrong="saw it go wrong", far="seen it, far off", none="never seen it done")


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
            S.append((W["deeds_once"] if len(pushed) == 1 else W["deeds_pushed"]).format(n=_num(len(pushed), W), hand=W["hand"], noun=NOUN[pt])
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
    eps = _episodes(h["label"])
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
