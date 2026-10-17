"""The game layer's settings, names and helpers: everything game.py held before class Game (PRESETS aside, which
stays in game.py), moved out verbatim. game.py and the Game mixins import from here."""
import re
import numpy as np
from collections import deque
import os
import sys
from link import E, PIN
import explain as X             # engine v7: the character's view before a choice, what came of it after
import foresee as F             # engine v7: the foreseen outcome of a plan
from story import Story, TAKEN_IN, LIB_READ, act, chooses, plain, ADJ, NOUN, EPITHETS, SETTINGS, load_library_story, DRIVER_WORD, neg_of, STATUS_WORD, mk, NAME_POOL, an
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
    import worlds as WDS        # v22.5, F12: the Library's words and own ways of the tribal and magic worlds (chroma-library)
except ImportError:
    WDS = None
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
    # clarity item 6, "every line has a cause" (findings.md §1 and §3; Emren 10-10 10:25 UTC "apply all of them"; v22.4,
    # off until its refit): no story-only lines between moments. A memory is told inside the moment that brought it back
    # (Library RECALL_IN), or not at all; the times are one clause in the year's lead (YEAR_LEAD); a new name the voice did
    # most of is said on the year header (VOICE became_head); the temperament line names the told event whose week moved
    # it most (TEMPER_CAUSE); readings and outside events always show the color they pulled. Words only: the life is the
    # same either way. Each part keeps today's line while the pinned earth_story.py lacks its words
    lines_tied=False,
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
    # when they resented it. A way fades by up to own_fade a year when it led fewer of the year's acts than own_use times
    # its own expected share (the share of the year's open options that way leads: a way the moments rarely offer is
    # not asked to lead as many acts as a common one; acts with even ways, doing nothing, lead none); reluctance in a way is
    # x (1 - own_rel x ix); the peace reading counts a push as their own by its way's ix; at own_theirs the season lean
    # toward it no longer ends. A strong push at reluctance over own_react_rel while ix is under .25 bounces back with
    # chance own_react: ix falls own_react_back and the pent-up wanting grows as a push's does. A light steer that leaves
    # them on the pick they would have made, an act their steered way leads, is the voice and they agreeing: that way
    # moves own_lived x a light push of the act's share in it (without it a way they already live by stalls short of theirs)
    own_ix=False, own_k=0.15, own_light=1.5, own_strong=0.6, own_sup=2.5, own_acc=1.5, own_res=-0.5, own_fade=0.02,
    own_use=0.4, own_rel=0.8, own_theirs=0.8, own_react=0.15, own_react_rel=0.7, own_react_back=0.1, own_lived=0.5,
    # v22.5 proposal, "a voice that reads well" (chroma-ideas/player-impact/findings.md; Emren 10-11 11:45 UTC): a well-read
    # pick should leave the life better, not only cost less. Played lives only; every part off by default (lives as today).
    # Owned picks: a push toward the moment's head mark (what they judge best on reflection, explain.before), its heart
    # mark (what they wanted and did not dare) or either ("both") is theirs, not the voice's: it builds no pent-up wanting
    # and only own_stress of a push's strain, and when it works it lets go of own_free of the wanting already built
    # (self-determination: acting on one's own judgement is endorsement, whoever suggested it). "" is off
    own_mark="", own_stress=0.5, own_free=0.3,
    # A way lived becomes who they are: the season's lean (F2) moves who they are (z) by lean_self a week as it moves what
    # they want (lean), so a season of a new way does not leave them wanting to be someone they are not (self-perception;
    # today only the want moves, and the want-self gap it opens is what the engine's frustration and content read)
    lean_self=0.0,
    # A voice that teaches: an owned push toward the head's pick that works builds their discipline own_teach of the way to
    # its bound (the engine's disc_range), so in the weeks without the player they act on their own judgement more often
    # (self-control is learned; a hard thing done on purpose builds it, engine disc_win and disc_tag)
    own_teach=0.0,
    # A dream within reach: a push toward an option that serves a dream, passion or plan they hold (the engine's goal fit
    # rel of at least dream_fit) is theirs too (dream_own: it counts as owned, as own_mark's picks do), and when it works
    # the voice's backing firms the goal up dream_firm of the way to full strength, so they take more of its steps on their
    # own, and adds dream_help of the engine's own step to a plan's progress (support for goal pursuit)
    dream_own=False, dream_fit=0.5, dream_firm=0.0, dream_help=0.0,
    # Readable stakes: a need under hind_thin counts as one they lack, for the option row's "lift" and for hindsight (need_thin
    # .5 today: adult needs sit at .6 to .9, so the lift showed on few rows and hindsight seldom accepted a push)
    hind_thin=0.5,
    # A season that holds: an owned pick that worked (toward their heart, or accepted in hindsight) keeps its routine for
    # the season (lean_weeks, fading): its ends keep feeding the needs they meet at season_need of the engine's own weekly
    # refill, and strain eases by season_calm a week (a sense of control; the hook for v22.5 F1's Mind, "steadier picks")
    season_need=0.0, season_calm=0.0,
    # Forks, not weather: a moment whose options lead to different lasting places (a title or perk, a commitment, money or
    # time won or lost) weighs fork_k more for the player; with fork_told an everyday moment whose options all end alike is
    # told, not asked. rung_ask: a moment that offers a pack career's rung or a summit is always put to the player
    fork_k=0.0, fork_told=False, rung_ask=False,
    # v22.5, rare moments are asked (push_rare, 10-11: on the same 60 lives, pushed lives met 545 distinct rare moments
    # against 475 left alone, but the game put only 75 and 73 of them to the player): a moment under RARE_SHARE of lives
    # (the Book's rare), met for the first time, comes up at a life event's pace (half the gap) and weighs rare_imp more
    # when the game picks the moments to put to the player (a moment rung_ask already puts to them is not weighed again).
    # Off until its proof
    rare_ask=False, rare_imp=0.5,
    # Picks come back (chroma-ideas/gameplay-2026-10-17/picks-come-back.md, Emren 10-17): an asked pick that leaves a mark
    # plants a seed (the moment, the way, the person in the scene, how it went, the age). A later moment that answers it
    # (the Engine's echo_play hook; without it, an echo of the same mark ret_gap weeks or more after the pick) is always
    # put to the player, opens on the earlier pick, brings back its person, and leans ret_tilt (logit) toward working if
    # the first time went well, away if badly; a moment met before waits while a return is due. Off until the joint proof
    returns=False, ret_tilt=0.15, ret_gap=52,
    # v22.5, F12 "The world and the start hold" (chroma-ideas/realism/v22.5-realism-list.md; off until v22.5's refit, with
    # the engine's own_open and start_hold): the tribal and magic worlds speak their own words (the Library's worlds.py:
    # option labels, moment titles, the means, a lost place in the work, a backfire; no money, sirens, profits or votes
    # in the story's own lines there); an option closed by a means it is short of says so, never "not on offer"; the
    # story's place follows the world's (a village start in a village, a move to a city a city); each start draws its own
    # world and story names (with the same seed, the four modern starts are four lives, not one in four coats)
    world_hold=False,
    # v22.5 realism F15 (the clan and the towers settle as their own colours): tribal and magic lives play on the Library's
    # colour-even seed moments (worlds.py SEED, one option per colour) instead of the engine's own seed library, whose
    # options lean White (False: the engine's)
    world_seed=False,
    # v22.5 F15 (Engine, clan and towers): the faith a life inherits leans faith_home of the way from the world's faith mix
    # toward the family's own colours (engine fam) (0: the world's mix, as before)
    faith_home=0.0,
    # v22.5 realism F10, once means once, the story's side (no life changes): line_wait, the years before the same line of
    # an outside reading, the world, an ordinary week or a year's chapter is told again word for word (0: as before);
    # news_touch, national news only when it touches them: from news_age (their own place's, a war, a pandemic and a
    # recession at any age), a law told once for each state it reaches, the government's fall told once with its
    # election, and the same kind of national news at most once in news_gap years (False: as before)
    line_wait=0.0, news_touch=False, news_age=10.0, news_gap=4.0,
)
LINE_WAIT_TAGS = {"read", "world", "world_year", "world_fx", "ordinary", "year", "fortune", "trouble", "memory", "seen", "talk",
                  "temper", "healed", "hardened", "voice"}   # F10: the lines line_wait holds back (scenes, choices, deaths
# and commitments are told whenever they happen)
NEWS_ALL = {"war", "war_end", "pandemic", "recession", "world_recession", "revolution", "regime"}   # F10: news that touches
# everyone, at any age (the rest of the national news from news_age)
OWN_STEPS = ((0.8, "theirs"), (0.5, "sees"), (0.25, "ought"), (0.0, "asked"))   # S2: ix -> the Library's step key

# stage 1's played-life rules at their off values (the update's UPD_OFF rule: every new mechanic can be switched off):
# with these a played life is the one v22.1 plays, step for step (test/same_engine.py with CHROMA_GAME=off)
GAME_OFF = dict(piv=0.0, piv_own=0.0, piv_steady=0.0, learn_full=False, lean=0.0, quiet_k=1.0, plan_lean=0.0, tie_imp=0.0, tie_pick=0.0, told_share=2.0,
                era_cost=0.0, backfire=0.0, turn_max=0, fig_own=False, own_ix=False, trust_judge=False, lines_tied=False,
                own_mark="", lean_self=0.0, own_teach=0.0, dream_own=False, dream_firm=0.0, dream_help=0.0, hind_thin=0.5, season_need=0.0, season_calm=0.0, fork_k=0.0, fork_told=False, rung_ask=False,
                world_hold=False, world_seed=False, faith_home=0.0,
                line_wait=0.0, news_touch=False, rare_ask=False, returns=False,
                own_stress=0.5, own_free=0.3, dream_fit=0.5, rare_imp=0.5)
# v22.5's joint refit (chroma-engine/notes/v22.5-refit-plan.md §2, with the engine's V225): every v22.5 game switch on
# with its fitted value. F12 world_hold (with the engine's own_open and start_hold), F15 world_seed, F10 line_wait and news_touch (the
# values chroma-release/check_roll.py proves), the player-impact rules V1-V8 (chroma-ideas/player-impact/scripts/
# proto_v8.env), rare_ask, and clarity items 6 and 7, lines_tied and trust_judge (every line has a cause; every push judged
# by how it went: planned for v22.4's refit, needed now the v22.5 rules leave few pushes reluctant). V225_OFF keeps
# the values before (v22.4's played lives, with the engine's UPD_OFF)
V225 = dict(world_hold=True, world_seed=True, faith_home=1.0, line_wait=5.0, news_touch=True, trust_judge=True, lines_tied=True,
            own_mark="both", own_stress=0.3, own_free=0.5, lean_self=0.012, hind_thin=0.7, season_need=1.0, season_calm=0.012,
            fork_k=0.3, fork_told=True, rung_ask=True, own_teach=0.05, dream_own=True, dream_fit=0.5, dream_firm=0.15,
            dream_help=1.0, rare_ask=True, rare_imp=0.5)
V225_OFF = {k: GAME[k] for k in V225}
GAME.update(V225)
# The spheres finishing pack (chroma-world/spheres/finish-pack-draft.md; Emren chose "Parts 1 to 5" 10-17 02:03 UTC), the
# game's part 1: S2, making it their own (own_ix), with the values above. Off, like the Engine's parts 2 to 5, until the
# pack's joint refit tunes and switches them on together; CHROMA_GAME="pack" plays a life with it on (the steered row own_even)
PACK = dict(own_ix=True)
PACK_OFF = {k: GAME[k] for k in PACK}
if os.environ.get("CHROMA_GAME"):                   # checks and calibration only: "off", "v224", "pack" or settings as JSON
    import json as _json
    GAME.update({"off": GAME_OFF, "v224": {**V225_OFF, **PACK_OFF}, "pack": PACK}.get(os.environ["CHROMA_GAME"])
                or _json.loads(os.environ["CHROMA_GAME"]))
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


def start_offset(setting, place, society, wealth, faith, upbringing):
    """v22.5, F12 (world_hold): a start's own offset to the seed, the same for the same start (its settings, not its title)."""
    import zlib
    return 1 + zlib.crc32(f"{setting}|{place}|{society}|{float(wealth):.3f}|{faith}|{upbringing}".encode()) % 999983


def place_word(kind):
    """v22.5, F12 (world_hold): the story's word for a world locality's kind (its {place}: the village, the city, the
    town, the countryside)."""
    k = str(kind)
    for w_, keys in (("village", ("village", "hamlet")), ("city", ("city", "capital")), ("countryside", ("remote",))):
        if any(x in k for x in keys):
            return w_
    return "town"


def world_says(setting, part, key, default=None):
    """v22.5, F12 (GAME world_hold): the Library's word for key in a tribal or magic world (worlds.py WORDS, TITLES or
    LABELS: part), else default (Earth, an unlisted key, or the switch off)."""
    if not GAME["world_hold"] or WDS is None:
        return default
    return getattr(WDS, part, {}).get(setting, {}).get(key, default)


def world_table(setting, part):
    """v22.5, F12 (GAME world_hold): a whole table of the Library's worlds.py for this world ({} for Earth or off)."""
    return dict(getattr(WDS, part, {}).get(setting, {})) if GAME["world_hold"] and WDS is not None else {}


def res_names(setting):
    """The five means as this world names them (money: goods in the clan, coin in the towers, with world_hold)."""
    r = world_says(setting, "WORDS", "res")
    return [r.get(x, x) for x in RNAMES] if r else RNAMES


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
            if GAME["returns"] and hasattr(batch, "RETURN_MOMENTS"):
                batch.RETURN_MOMENTS = True             # Picks come back: the Library's return moments (earth.RETURNS)
            _LIBS[key] = (batch.load_batch("earth", packs=PACKS, setting="earth"), sys.modules.get("earth"))
        else:                                       # v22.5 F15 (world_seed): the clan and the towers on the Library's seed
            seed_ = getattr(WDS, "SEED", None) if GAME["world_seed"] and key in ("tribal", "magic") else None
            _LIBS[key] = (with_dreams(E.compile_library(situations=seed_), key), None)
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
    import batch                                    # v22.5 (F6, F12): what the engine's dream_grow and own_open read, attached
    if hasattr(batch, "dream_grow_data") and setting in D_.DREAM_TRIGGERS:   # as the Earth batch attaches it; read only
        batch.dream_grow_data(L, D_, setting)                               # with those switches on
    if hasattr(batch, "own_ways") and WDS is not None and setting in getattr(WDS, "OWN", {}):
        batch.own_ways(L, WDS.OWN[setting])
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
