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
# Since the split (the CLAUDE.md files): the module code before class Game is in game_base.py, the code after it in
# game_words.py, and Game's methods in the five mixin modules below; this file keeps PRESETS, the class and its
# core (__init__, _intervene, age, advance, decide). Every name game.py had is still importable from game.
from game_base import *  # noqa: F401,F403
from game_base import (_LIBS)  # noqa: F401
from game_words import *  # noqa: F401,F403
from game_words import (_CAT, _adjs, _again, _becoming, _c, _cap, _closing, _decade, _deeds, _drift, _epic_cause,
    _epic_thing, _episodes, _ident_a, _merged, _move, _nouns, _nth, _num, _quoted, _shape, _song_colors, _thing,
    _ways, _when, _why)  # noqa: F401
from game_checkpoints import CheckpointsMixin
from game_world import WorldMixin
from game_voice import VoiceMixin
from game_life import LifeMixin
from game_views import ViewsMixin
from game_causes import CausesMixin
from game_bold import BoldMixin
from game_because import BecauseMixin
from game_foot import FootMixin
from game_aims import AimsMixin
from game_asks import AsksMixin

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


class Game(CheckpointsMixin, WorldMixin, VoiceMixin, LifeMixin, ViewsMixin, CausesMixin, BoldMixin, BecauseMixin, FootMixin, AimsMixin, AsksMixin):
    """One life. Drive it with advance() and decide(); read it with status() and the log."""
    _recall_t = -10 ** 6    # week a memory coming back was last told
    # how much each part of temperament must move before the log says so, and the words for up and down
    TEMPER = (("react", 0.25, "more easily shaken", "harder to shake"),
              ("steady", 0.35, "steadier in who they are", "less sure of who they are"),
              ("base_mood", 0.1, "more content by nature", "less content by nature"),
              ("outlook", 0.12, "more sure that effort pays off", "less sure that effort pays off"))
    # ------------------------------------------------------------------ v7: dreams, passions and plans
    # ------------------------------------------------------------------ point 1: the everyday life between moments
    CIRCLE = ((r"choir|singer|music", "the choir"), (r"club|organiser", "the club"), (r"team|league|rescue", "the team"),
              (r"church|congregation|worship|deacon|elder|faith", "the congregation"), (r"garden", "the community garden"),
              (r"union", "the union"), (r"party|campaign|activist|advocate|rights|cause", "the campaign"),
              (r"volunteer|kitchen|shelter", "the volunteers"), (r"radio", "the radio station"), (r"co-?op|committee|resident", "the residents' committee"))
    _kin_t = None           # week the story's family was last matched to the world's
    KIN_WAIT = 12           # weeks a death in the world waits for the engine's own record before the story says it
    DUE_WAIT = 8            # F7: weeks a world death of kin waits in story.due for an engine death to claim it (F7.2 allows 13)
    NEWS_GAP = 8 * 52       # one public figure's scandals, rises and falls: the story tells one in this many weeks
    world_source = None     # the engine's outer world: a callable, hidden week -> (snapshot, record, cast, standing); None until it lands
    _wloc = None            # the locality they live in, as last told
    ROLL_ROLES = dict(parent=("mother", "father"), sibling=("sibling",), grandparent=("grandparent",), partner=("partner",),
                      child=("child",))   # F7: the world's kin roles the story's deaths are matched by

    def __init__(self, name="Ari", seed=1, world="neutral", society="", wealth=0.3, faith=None,
                 upbringing="", start_age=0.0, freq="normal", detail=1, years=80, place="town", setting="earth", sex=None,
                 pace=1.0, tech="modern", climate="middle", earlier=None, earlier_data=None, **_):
        self.name = name
        self.setting = setting if setting in SETTINGS else "earth"
        # v22.5, F12 (world_hold): each start draws its own world and story names (the same seed, another start: another life)
        self._start_off = start_offset(self.setting, place, society, wealth, faith, upbringing) if GAME["world_hold"] else 0
        self.story = Story(name, int(seed) + self._start_off, place, self.setting)   # the built-in narration (story.py)
        self.story.hold = GAME["world_hold"]
        import story as ST_                             # F12: every told act of the clan or the towers in its own words
        ST_.ACT_WORLD.clear(); ST_.ACT_WORLD.update(world_table(self.setting, "LABELS"))
        self.wv = WorldView(int(seed) + self._start_off, self.setting, name, fig_own=GAME["fig_own"])     # the outer world's panel, circle, reach and story lines
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
        if self.up_mix is not None:
            P["up_mix"] = self.up_mix                   # v22.5 F15: the engine's start lean reads it (up_lean, off until the refit)
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
        if GAME["returns"]:
            P["echo_play"] = True       # Picks come back: the Engine's hook, read once as the life starts, set only by the game
        if GAME["causes"] and "role_why" in E.DEFAULT:
            P["role_why"] = True        # Every change has a cause: the Engine records why each title or perk came or went
        if GAME["because"] and "need_why" in E.DEFAULT:
            P["need_why"] = True        # Because of you, and meanwhile: the Engine records why each need moved this week
        if GAME["foot"] and "foot_on" in E.DEFAULT:
            P["foot_on"] = True         # v24 footprints: the Engine gives what a pick leaves real state, and hands it over
        if GAME["aims"] and "aims" in E.DEFAULT:
            P["aims"] = True            # v24 aims: ladders toward what they want to become, and the heights reached
            P["heights"] = True
        if GAME["bold"] and "bold_play" in E.DEFAULT:
            P["bold_play"] = True       # Bold ways: the Engine offers a card's bold ways when the game asks (bold_ask)
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
            if self._start_off:
                P["world_seed"] = int(seed) + self._start_off
            import world_link as WLM_
            if hasattr(WLM_, "start_fits"):             # v22.5, F12: what the start promises, read by the engine's start_hold
                P["world_cfg"]["start"] = dict(place=place, wealth=float(wealth), hard=place == "neighbourhood",
                                               faith="none" if faith == "none" else ("held" if faith else None),
                                               society=mix(society).tolist() if society else None)
            if earlier and earlier_data and earlier_data.get("key") == earlier.get("key"):
                import world as WM
                P["world_obj"] = WM.World.load(earlier_data["world"])
                self.wv.seed = int(earlier_data["world"]["seed"])          # the same world names the same people and places
                if earlier.get("grandchild") and earlier_data.get("people"):
                    P["world_cfg"]["legacy"] = earlier_data["people"]
            elif earlier:
                raise ValueError("the earlier world this life begins in is not in this browser")
        P.update({k_: v_ for k_, v_ in ENGINE_SET.items() if not k_.isupper()})   # checks only (CHROMA_ENGINE); empty in played lives
        if P.get("death_life", E.DEFAULT.get("death_life")):   # v22.5 F2: death comes from the life, past 80 to about 100
            years = max(years, DEATH_LIFE_YEARS)
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
        self._steer = None              # v24: the player's lean between asks, dict(color, until, n, moved) (game_asks.py)
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
        self._seasons = []                  # v22.5 proposal: owned picks' seasons (ends, strength, week)
        self._pick_mix = np.zeros(C); self._pick_wt = 0.0; self._pick_t = 0
        self._prng = np.random.default_rng(int(seed) + 5151)
        self.history["pivots"] = []     # (age, kind, colors before, target, size): kind own, toward, half or backfire
        # S2 (GAME own_...): how far each way the voice pushes toward has become theirs, the acts of this year by the color
        # leading their ways and the acts each color was expected to lead (for the fade), the season leans that no longer
        # end (color -> (target, strength)), a random stream of its own (reactance), and each step crossed (age, color,
        # step) and bounce back (age, color, "back")
        self.ix = np.zeros(C); self._ix_use = np.zeros(C); self._ix_exp = np.zeros(C); self._own_leans = {}
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
        # item 6 (GAME lines_tied): the memory this week's moment brought back, waiting for that moment's line; the new name
        # and its phrase for the next year header; this week's told event, temperament at the end of last week, and the
        # told events since temperament was last told (its move that week, the event's name)
        self._recall_now = None; self._became_head = None
        self._week_ev = None; self._temper_prev = None; self._temper_evs = []
        self.history["times"] = []      # WL5 (item 11): what the times did to them, by age (the World panel)
        self.history["steers"] = []     # P3: each push or lean, with the era's fit, for the World panel's timeline
        self._wyear = {}                # WL4: this year's world effects told, (kind, channel, dir) -> size in "big" units
        self._wfx_t = {}                # WL1: (kind, channel, dir) -> week last told
        self._price, self._price_t = 0.0, 0   # 5.6: the price of pushes against them, and when it was last added to
        self._turn_pick = None          # the turning point's answer, applied at the end of its week
        self.history["turns"] = []      # (age, color, kind, held)
        self._threads = {}              # F5: what a pick started (("r", title), ("c", commitment), ("g", goal id)) -> its cause
        self._last_pick = None
        self._picks, self._seeds, self._ret_owed = {}, [], 0   # Picks come back: each asked pick by its week; the seeds the
        # marked ones planted; returns asked that have not yet taken a repeat's place
        self._bold_t, self._bold_now, self._bold_pick, self._link_owed, self._bold_watch = None, [], -1, 0, None   # Bold ways: the week and moment
        # promised to the player at the situation pause, the bold ways offered and the character's own slot at choose, and
        # links asked that have not yet taken an everyday ask's place
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
        if self.up_mix is not None and age < 15 and not P.get("up_lean"):   # (F15 on: the engine's start lean does it)
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
                if "P" in loc:
                    self.story.one_roll = bool(loc["P"].get("one_roll"))   # F7: the story reads the engine's one roll
                    if self.story.one_roll and "alive" in loc and loc["alive"].shape[1] > 5:
                        self.story.kids_n = int(loc["alive"][0, 5])
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
                if GAME["bold"]:
                    self._bold_situation(t, loc, int(np.asarray(val).ravel()[0]), until_checkpoint)
                reply = val                             # the engine times life events itself since v6
            elif kind == "choose":
                self._title_now(loc)
                if t == 6 * 52:
                    self._family_faith(loc)
                if GAME["bold"]:
                    self._bold_choose(loc)
                cp = self._checkpoint(t, loc, val) if until_checkpoint and t / 52 >= self.start_age else None
                if cp is not None:
                    self._steer = None                  # v24: a lean held between asks ends at the next ask
                    self.pending = cp
                    return "checkpoint"
                reply = val
                if self._steer is not None and t / 52 >= self.start_age:
                    reply = self._steer_between(t, loc, val)   # v24: the player's lean between asks
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
        own = int(cp["own"]) if cp.get("bold") else int(a[0])   # Bold ways: their own pick may be a bold way
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
            a = a.copy(); a[0] = bix(pick)             # a bold way plays as its base way
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
        if cp.get("bold"):
            self._bold_take(cp, choice)                 # Bold ways: the slot taken, or -1, always told to the Engine
        if GAME["returns"] and self.loc is not None and "P" in self.loc:
            self.loc["P"]["echo_asked"] = True          # Picks come back: the engine plants this asked pick's seeds
        if GAME["own_ix"] and lt and choice == own:     # S2: the light steer kept their own pick
            self._cp_week["lean"] = lt["color"]
        if self.loc is not None and "P" in self.loc:   # item 4: the week of a pick counts whole (own lesson, drift, outside)
            self.loc["P"]["own_k"] = self.loc["P"]["drift_k"] = self.loc["P"]["ev_push_k"] = 1.0
        self.pending = None
        self._last_cp = self.t
        try:
            self._msg = self._gen.send(a)
        except StopIteration as e:                      # the life ends in the very week of the choice
            self.over = True; self.result = e.value
            self._life_review()
