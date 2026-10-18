"""Chroma's shared outer world: one society per world seed, shared by every life in a run (chroma-world package, agreed
by Emren 2026-10-06 10:51; build plan chroma-engine/world-build.md; keys chroma-engine/world-fields.md and world_keys.py).

    W = World(seed, cfg=None)       cfg: pace, tech_level, climate, setting, preset, legacy (see CFG_DEFAULT)
    W.burn_in(80)                   the world alone before the birth (spec 5 §4); the log keeps it
    W.tick(week)                    every week with the world clock (W.t0 + the life's week), or W.tick() for one week
    W.spawn_neighbour(k)            a full World for neighbour k, its clock equal to this one's (emigration, spec 5 §5);
                                    W.society_id is 0 at home, k + 1 in a spawned neighbour
    W.disaster_now, W.disaster_kind per locality: severity (0..1) and HAZARDS index of a disaster striking this week,
                                    else 0 and -1 (cleared the next week)

Ticks follow package.md §4: the season every week; every 13 weeks the quarter in order nature, other societies,
economy, state, institutions, places, culture, society and eras, public figures, history log; every 52 weeks the year
(technology, belief, the generations turning 15 to 25, the population). Pushes queued by the lives land at the next
quarter tick.

Rules kept (world-build.md "Rules every part keeps"):
- No color rule. Nothing here reads or defines a relation between colors on the wheel. Fit between two pies is overlap
  or distance, the same for every pair. Every color-indexed table is a module-level array below; World(color_perm=p)
  permutes all of them (and every color-indexed random draw) at construction, so a permuted world is the same world
  with its colors relabelled (the equivariance test in calib_v10/world_check.py).
- One world per seed: own streams np.random.default_rng([seed + 104729, k]), one k per domain (a spawned neighbour
  adds its society id: [seed + 104729, k, society]). The world never sees N.
- Timeless: keys and ids only, never a year, a brand, a real place, person or event.
- pace (0.5 to 2) multiplies only the world's hazards (recession start, crises, war, pandemic, disasters) and how fast
  society's pressure builds.
- numpy and the standard library only; no file input or output; safe in Pyodide.
"""
# Since the split (chroma-engine/CLAUDE.md): the module code outside class World is in world_base.py and World's
# methods are in the five mixin modules below; this file keeps the class and its core (construction, the clock and
# emigration, whose spawn_neighbour builds a World). Every name world.py had is still importable from world, except
# _FAIR_TAGS (fair_tags()'s cache, which lives in world_base).
from world_base import *  # noqa: F401,F403
from world_base import (_cd, _cl, _jsafe, _logit, _mix, _norm, _sig, _tv, _uclip)  # noqa: F401
from world_hooks import HooksMixin
from world_society import SocietyMixin
from world_years import YearsMixin
from world_spheres import SpheresMixin
from world_events import EventsMixin

# the modules that make up world (the Engine's checks read their sources, and the world cache hashes them)
_PARTS = ('world_base', 'world_hooks', 'world_society', 'world_years', 'world_spheres', 'world_events')


class World(HooksMixin, SocietyMixin, YearsMixin, SpheresMixin, EventsMixin):
    """The shared outer world. See the module docstring and world-build.md for what it exposes."""

    _STREAMS = dict(setup=0, nature=1, abroad=2, economy=3, state=4, institution=5, place=6, culture=7, society=8,
                    figure=9, tech=10, belief=11, group=12)
    _CONST = ("p", "cfg", "perm", "NEEDM", "LOADP", "NPROF", "WPROF", "GMIX", "FPROF", "ROUT", "OLIG", "VPRE",
              "DSEC", "DOPEN", "DENT", "R", "pace", "gidx", "gadult", "_seed", "trace")

    # ------------------------------------------------------------------------------------------------ construction
    def __init__(self, seed, cfg=None, color_perm=None, params=None, society=0, start_t=0):
        """society > 0 and start_t are for spawn_neighbour: the neighbour's own streams, and its clock at setup."""
        cfg = dict(CFG_DEFAULT, **(cfg or {}))
        self.cfg = cfg
        self.p = dict(W_DEFAULT, **(params or cfg.get("params") or {}))
        self._seed = int(seed)
        self.perm = np.arange(C) if color_perm is None else np.asarray(color_perm, int)
        self.pace = float(cfg["pace"])
        self._tables()
        self.society_id = int(society)                     # 0 = home; a spawned neighbour is its index + 1 (spec 5 §5)
        self.R = [np.random.default_rng([self._seed + 104729, k] + ([self.society_id] if self.society_id else []))
                  for k in range(len(self._STREAMS))]
        self.log, self.record, self.push_log = [], [], []
        self._queue = []
        self._setup(int(start_t))

    def _s3(self, k):
        """Whether a stage 3 rule of the v22 update is on (stage3-rules.md §8)."""
        return bool(self.p.get(k, False))

    def _tables(self):
        """Every color-indexed table, permuted once (color_perm)."""
        P = self.perm
        self.NEEDM = NEED_MAP[:, P]
        self.LOADP = LOAD[:, P]
        self.NPROF = NORM_PROF[:, P]
        self.WPROF = WELFARE_PROF[P]
        self.GMIX = {g: m[P] for g, m in GUILD_MIX.items()}
        self.FPROF = FAITH_PROF[:, P]
        if self.p.get("c5_faith"):                         # C5: the slots' colours (even until a movement is founded)
            self.FPROF = np.vstack([self.FPROF, getattr(self, "c5_prof", np.full((NM, C), 0.2))])
        self.ROUT, self.OLIG = ROUTINE[P], OLIGARCHY[P]
        pre = self.cfg["preset"]
        if isinstance(pre, (list, tuple, np.ndarray)):       # a value climate in the canonical frame (spawn_neighbour)
            self.VPRE = _norm(np.asarray(pre, float))[P]
        else:
            self.VPRE = (V_RICH if pre == "typical rich" else np.full(C, 0.2))[P]
        L = self.LOADP
        V_ = {v: i for i, v in enumerate(VALUES)}
        def d(plus, minus):
            x = L[[V_[v] for v in plus]].sum(0) - L[[V_[v] for v in minus]].sum(0)
            return x / np.abs(x).max()                       # zero-sum (LOAD rows sum to 0), largest share 1
        self.DSEC = d(["self-direction", "universalism"], ["security", "tradition"])      # secure vs insecure youth
        self.DOPEN = d(["self-direction", "stimulation", "universalism"], ["tradition", "conformity", "security"])
        self.DENT = d(["achievement", "stimulation"], ["security", "conformity"])          # enterprise vs caution

    def _profile_src(self, src):
        if src in self.GMIX or " " in src and all(t in self.GMIX for t in src.split()):
            return 0.6 * np.mean([self.GMIX[t] for t in src.split()], 0) + 0.08
        return 0.6 * _mix(src)[self.perm] + 0.08

    def _cn(self, r, *shape):
        """Color-indexed normal noise, drawn in the canonical frame and permuted like every color table."""
        return r.normal(size=shape + (C,))[..., self.perm]

    def _setup(self, start_t=0):
        p, r = self.p, self.R[0]
        cfg = self.cfg
        # clock
        self.t = self.t0 = int(start_t)
        self.week_of_year = self.t % 52
        self.season = int(WEEK_SEASON[self.week_of_year])
        self.clim_t0 = None                                # the climate scenario's anchor (the first birth), set once
        self.rich = 1.0                                    # how rich against home (a spawned neighbour: its ext_rich)
        # ---- economy
        self.phase, self.severity, self.exp_q, self.rec_q, self.rec_len, self.last_sev = 0, 0, int(r.integers(0, 16)), 0, 0, 0
        self.gap, self.gap_prev, self.gap_ema, self.housing, self.house_m = 0.05, 0.05, 0.0, 0.0, 0.0
        self.house_hist = np.zeros(12)
        self.natural = float(p["u_nat"])
        self.u_rise, self.u_rise_tgt, self.u_noise = 0.0, 0.0, 0.0
        self.unemp, self.unemp_prev = self.natural, self.natural
        self.infl, self.infl_e = p["infl0"], 0.0
        self.energy, self.food = 0.0, 0.0
        self.ineq = p["ineq0"]
        self.sector_tilt = np.zeros(5)
        self.payoff = np.full(C, 0.2)
        self.rec_declared, self.rec_start_t, self.rec_end_t = False, -1, -1
        self.n_rec = 0
        # ---- technology (setup level)
        lvl = cfg["tech_level"]
        self.tech_ceil = np.array(TECH_CEIL[lvl], float)
        self.tech_keys = list(TECH_KEYS)
        self.tech_adopt_v = self.tech_ceil.copy()
        self.tech_exists = self.tech_ceil > 0
        self.tech_kind = [-1] * NT                         # NEW_TECH index for kinds that arrived later
        self.tech_born = [0] * NT
        self.automation = np.array([.10, .25, .15, .10, .03]) * (0.7 if lvl == "behind" else 1.3 if lvl == "ahead" else 1.0)
        self.medical0 = {"behind": .55, "modern": .70, "ahead": .80}[lvl]
        self.medical = self.medical0
        self.comm = float(0.5 * self.tech_ceil[0] + 0.5 * self.tech_ceil[2])
        self.watch = {"behind": .25, "modern": .40, "ahead": .55}[lvl]
        # ---- nature
        self.climate = cfg["climate"]
        self.warming = self._warming(0)
        self.extremes = self._extremes(self.warming)
        self.pandemic, self.pand_q = 0, 0
        self.pand_n = 0
        # ---- localities (spec 3 §2)
        boom_energy = r.random() < 0.5
        rows = [list(x) for x in LOC_TABLE]
        if boom_energy:
            rows[-1][0], rows[-1][1], rows[-1][6] = BOOM_ENERGY
        nl = len(rows)
        self.n_loc = nl
        self.loc_kind = np.array([LOC_KINDS.index(x[0]) for x in rows])
        self.loc_kind_key = [x[0] if cfg["setting"] == "earth" else LOC_KIND_ALIASES[cfg["setting"]][x[0]] for x in rows]
        self.loc_feat = np.array([[f in x[1].split() for f in FEATURES] for x in rows])
        self.loc_size = np.array([x[2] for x in rows])
        self.loc_density = np.array([x[3] for x in rows], float)
        self.loc_pop0 = np.array([x[4] for x in rows], float); self.loc_pop0 /= self.loc_pop0.sum()
        self.loc_pop_share = self.loc_pop0.copy()
        self.loc_class_mix = np.array([x[5] for x in rows], float)
        self.loc_sector_base = np.array([x[6] for x in rows], float)
        self.loc_sectors = self.loc_sector_base.copy()
        self.loc_ufac = np.array([x[7] for x in rows], float)
        self.loc_rent0 = np.array([x[8] for x in rows], float)
        self.loc_rent = self.loc_rent0.copy()
        self.loc_crime0 = np.array([x[9] for x in rows], float)
        self.loc_crime = self.loc_crime0.copy()
        hz = np.array([x[10] for x in rows], float)
        hz[:, 2] *= r.uniform(0.0, 2.0)                    # how seismic this world's land is
        self.loc_hazards = _uclip(hz * np.exp(0.2 * r.normal(size=hz.shape)), 0, 1)
        self.loc_nature = np.array([x[11] for x in rows], float)
        self.loc_place = np.array([x[12] for x in rows])
        self.loc_services = _uclip(np.array([[.6, .55, .4], [.7, .65, .55], [.8, .75, .7], [.85, .85, .85]])[self.loc_size]
                                    + 0.05 * r.normal(size=(nl, 3)), 0.1, 1)
        self.loc_unemp = np.full(nl, self.natural)
        self.loc_trend = np.ones(nl, int)
        self.loc_growth = np.zeros(nl)
        self.loc_disaster = np.zeros(nl)                   # years of recovery left after a disaster
        self.disaster_now = np.zeros(nl)                   # severity of a disaster striking this week (0 none)
        self.disaster_kind = np.full(nl, -1)               # its HAZARDS index (-1 none)
        self.dis_pending, self.dis_on = [], False          # [week, loc, hazard, severity] drawn for the coming quarter
        self.loc_next_vote = r.integers(1, 20, nl)
        self.loc_crime_ma = self.loc_crime.copy()
        ref_mult = self._extremes(self._warming_now())
        self.haz_ref = float((self.loc_pop0 * (self.loc_hazards * np.array(p["dis_base"]) * ref_mult).sum(1)).sum())
        self.crime_ref = float((self.loc_pop0 * self.loc_crime0).sum())
        # neighbourhoods
        nbn = np.array([1, 3, 4, 5])[self.loc_size]
        self.nb_loc = np.repeat(np.arange(nl), np.asarray(nbn).astype(np.intp))   # intp: the browser's numpy is 32-bit
        q = np.concatenate([(np.arange(k) + 0.5) / k for k in nbn])
        cum = np.cumsum(self.loc_class_mix, 1)[self.nb_loc]
        self.nb_class = (q[:, None] > cum[:, :2]).sum(1)
        self.n_nb = len(self.nb_loc)
        self.nb_efficacy = _uclip(np.array([.45, .58, .70])[self.nb_class] + 0.06 * r.normal(size=self.n_nb), .1, .95)
        self.nb_crime = self.loc_crime[self.nb_loc].copy()
        # ---- population groups (spec 2 §6): age band x class x place x faith (0 secular, 1.. faiths) x migrant
        self.pop = self._init_pop(r)
        g = np.indices(self.pop.shape).reshape(5, -1)
        self.gidx = g
        self.gadult = g[0] >= 1
        # ---- culture, generations
        self.Y0 = 110                                      # cohort array row of birth year 0 (oldest born -110 y)
        y0 = self.t // 52                                  # 0 at home; a spawned neighbour starts later
        ncoh = self.Y0 + max(400, y0 + 130)
        nz_ = self._cn(r, ncoh)
        if self._s3("cult_no_dice"):                       # LW1 1h: no dice in the culture
            nz_ = 0.0 * nz_
        self.coh = np.tile(self.VPRE, (ncoh, 1)) * np.exp(p["coh_noise"] * nz_)
        self.coh /= self.coh.sum(1, keepdims=True)
        self.coh_fixed = np.zeros(len(self.coh), bool); self.coh_fixed[:self.Y0 + y0 - 14] = True
        self.coh_n = np.zeros(len(self.coh)); self.coh_n[:self.Y0 + y0 - 14] = 11
        self.V_anchor = self.VPRE.copy()
        self.mig_tilt = np.zeros(C)
        self.norm_x = _logit(np.array([NORM_START[k] for k in NORM_KEYS]))
        self.norm_x += 0.25 * r.normal(size=NN)
        self.norm_x0 = _logit(np.array([NORM_MOD[k] for k in NORM_KEYS]))      # modern acceptance under the modern law
        self.lawsign0 = np.zeros(NN)
        self.lawsign0[:NL] = 1.0 - np.array([LAW_MOD[k] for k in LAW_KEYS])
        for kk, v in RIGHT_MOD.items():
            self.lawsign0[NI[kk]] = 2 * v - 1
        self.norm_hist = np.tile(self.norm_x, (21, 1))      # last 5 years, quarterly
        self.norm_push = np.zeros(NN)
        self.norm_pub = _sig(self.norm_x).round(2)
        self.trust, self.fear, self.polar = p["trust0"], p["fear0"], 0.1
        self.spiritual, self.conspiracy = 0.15, 0.10
        # ---- belief
        self.cosmology = COSMOLOGY.get(cfg["setting"], "believed")
        self.holy_shift = np.zeros(self._nf())
        # ---- state
        self.regime = p["regime0"] if cfg["preset"] in ("typical rich", "even") else float(cfg.get("regime", p["regime0"]))
        self._regime_derived()
        self.laws = np.array([LAW_START[k] for k in LAW_KEYS], int)
        self.law_push = np.zeros(NL)
        self.law_since = np.zeros(NL)
        self.welfare, self.welfare_pub = 0.45, 0.45
        self.rights = np.array([.85, .85, .9, .2, .45])
        self.unrest, self.war, self.war_with, self.war_q, self.lost_war_q = 0.05, 0, -1, 0, 0
        self.lockdown = 0.0
        # ---- belief shares, value climate and demand need the population
        self._group_mix()
        self.V = self._V()
        self.Vc_hist = [self.V.tolist()]
        Dem0 = self.V.copy()
        self.Dem, self.Dem_q = Dem0.copy(), Dem0.copy()
        self.G = _norm(Dem0 * np.exp(p["g_noise"] * self._cn(r)))
        self.support, self.gov_q, self.next_vote = p["s_win"], 0, int(r.integers(4, 20))
        self.gov_party, self.opp_party = 0, 1
        self.u_at_office = self.natural
        # ---- other societies (spec 5 §5)
        self._init_ext(r)
        # ---- institutions (spec 4) and public figures (spec 5 §6)
        self._init_inst(r)
        self._init_figs(r)
        if self._s3("hist_chance_only"):                   # LW2 2e: the first government is its party's (drawn as before)
            self.G = self.inst_profile[self.party_ids[self.gov_party]].copy()
        # ---- society (spec 6)
        self.Q, self.open_q, self.since_break, self.gap_now = 0.0, 0, 40, 0.0
        self.Pos = self._pos()
        self.Pos_slow = self.Pos.copy() if p["era_ref"] > 0 else np.full(C, 0.2)
        self.Pos_era = self.Pos.copy()
        self.pos_hist = np.tile(self.Pos, (41, 1))         # last 10 years, quarterly
        self.gap_slow = _tv(self.Pos, self.Dem_q)
        self.need_base = np.zeros(5)
        self.unmet_mean = np.zeros(5)
        self.era_i, self.era_k, self.era_key, self.era_p = 0.0, 0, None, np.zeros(C)
        self.era_since, self.era_lead, self.era_lead_q, self.n_era = -1, -1, 0, 0
        self.era_at = []                                   # [t, key, intensity, kind] at each era start
        self.harsh_loc = np.zeros(nl)
        self.loc_mix = np.tile(self.V, (nl, 1))
        self.loc_gov = _norm(self.loc_mix * np.exp(0.25 * self._cn(r, nl)))
        self.prosper = self.gap
        self.unemp_sector = np.full(5, self.natural)
        self.unemp_loc = self.loc_unemp
        self._derive_econ()
        self.revival = (0, 0)
        self.norm_speed = 0.0
        self.cycles = []          # hidden: [start t, end t, severity] of each recession (tests; never published)
        self.trace = [] if cfg.get("trace") else None

    def _init_pop(self, r):
        """Age x class x place x faith x migrant shares of a typical rich democracy (estimates: OECD age structure,
        about 4 in 5 urban, migrant stock rising toward 1 in 7, faith of the older society at the burn-in's start)."""
        age = np.array([.16, .12, .13, .13, .13, .13, .11, .09])
        place = np.array([(self.loc_pop0 * (self.loc_place == k)).sum() for k in range(3)])
        cls = np.array([[.28, .48, .24], [.33, .52, .15], [.35, .53, .12]])           # by place
        sec = np.array([.16, .16, .14, .12, .10, .08, .07, .06])                        # secular share by age
        fsh = np.array([.86, .08, .06])                                                  # among the faithful, natives
        mig_f = np.array([.25, .30, .15, .30])                                           # migrants: secular, faiths
        mig_age = np.array([.05, .18, .25, .20, .14, .09, .06, .03])
        mig = 0.08
        pop = np.zeros((8, 3, 3, NF + 1, 2))
        for a in range(8):
            fn = np.concatenate([[sec[a]], (1 - sec[a]) * fsh])
            for pl in range(3):
                pop[a, :, pl, :, 0] = (1 - mig) * age[a] * place[pl] * cls[pl][:, None] * fn[None, :]
                pop[a, :, pl, :, 1] = mig * mig_age[a] * place[pl] * np.array([.45, .45, .10])[:, None] * mig_f[None, :]
        if self.p.get("c5_faith"):                         # C5: the movement slots, empty at the start
            pop = np.concatenate([pop, np.zeros((8, 3, 3, NM, 2))], axis=3)
        return pop / pop.sum()

    def _nf(self):
        """The faiths on the faith axis: NF, and C5's NM movement slots when it is on."""
        return NF + (NM if self.p.get("c5_faith") else 0)

    def _regime_derived(self):
        demo = _cl((self.regime + 10) / 20, 0, 1)
        self.demo = demo
        self.law_rule = 0.3 + 0.6 * demo ** 1.5
        self.capacity = 0.45 + 0.4 * demo
        self.rights_base = demo ** 1.5

    def _init_ext(self, r):
        n = int(r.integers(3, 6))
        self.n_ext = n
        reg = np.where(np.arange(n) < 2, r.uniform(7, 10, n), 0.0)
        for j in range(2, n):
            u_ = r.random()
            reg[j] = r.uniform(7, 10) if u_ < 0.45 else r.uniform(-5, 5) if u_ < 0.8 else r.uniform(-10, -6)
        self.ext_regime = reg
        self.ext_V = _norm(np.tile(self.VPRE, (n, 1)) * np.exp(0.15 * self._cn(r, n)))
        self.ext_anchor = np.tile(self.VPRE, (n, 1))       # where each neighbour's value climate drifts back to
        self.ext_society = np.arange(n) + 1                # each neighbour's society id (spawn_neighbour)
        self.ext_G = _norm(self.ext_V * np.exp(0.3 * self._cn(r, n)))
        self.ext_rich = np.where(reg >= 6, r.uniform(0.7, 1.1, n), r.uniform(0.2, 0.6, n))
        rel = np.where(reg >= 6, np.where(r.random(n) < 0.6, 0, 1), np.where(r.random(n) < 0.5, 1, 2))
        self.ext_relation = rel.astype(int)
        self.ext_trade = r.uniform(0.05, 0.3, n) * np.where(reg >= 6, 1.0, 0.5)
        self.ext_phase = np.zeros(n, int)
        self.ext_rec_q = np.full(n, 99)                     # quarters since a recession started
        self.ext_exp_q = r.integers(0, 16, n)
        self.ext_war = np.zeros(n, int)                     # at war (with anyone) 0/1
        self.ext_migration = np.zeros(n)
        self.ext_next_gov = r.integers(8, 40, n)
        self.world_rec, self.world_q = 0, 0
        self.trade_hit = 0.0
        self.mig_in = self.p["mig0"]

    def _init_inst(self, r):
        rows = []                                           # kind, level, loc, native, sector, public
        def add(kind, level, loc, native, sector=-1, public=True):
            rows.append((INST_KINDS.index(kind), level, loc, native, sector, public))
        for l in range(self.n_loc):
            s = self.loc_size[l]
            for _ in range([1, 2, 3, 4][s]): add("school", 0, l, self._profile_src(NATIVE_SRC["school"][0]))
            if s >= 1:
                for _ in range(2 if s == 3 else 1): add("hospital", 0, l, self._profile_src("simic"))
            add("police", 0, l, self._profile_src("boros"))
            add("council", 0, l, self._profile_src("azorius"))
            for _ in range([1, 2, 3, 4][s]):
                sec = int(r.choice(5, p=self.loc_sector_base[l]))
                add("employer", 0, l, self._profile_src(SECTOR_GUILDS[sec][int(r.integers(len(SECTOR_GUILDS[sec])))]), sec, sec == 4)
        for l in UNIVERSITY_LOCS: add("university", 1, l, self._profile_src("simic izzet"))
        for l in COURT_LOCS: add("court", 1, l, self._profile_src("azorius"))
        for l in PRISON_LOCS: add("prison", 1, l, self._profile_src("boros"))
        for l in RMEDIA_LOCS: add("media", 1, l, self._profile_src(NATIVE_SRC["media"][int(r.integers(2))]), -1, False)
        add("court", 2, 0, self._profile_src("azorius"))
        for _ in range(3): add("ministry", 2, 0, self._profile_src("azorius"))
        add("army", 2, 0, self._profile_src("boros"))
        add("media", 2, 0, self._profile_src("rakdos"), -1, False); add("media", 2, 0, self._profile_src("dimir"), -1, False)
        for _ in range(3): add("bank", 2, 0, self._profile_src("orzhov"), 3, False)
        for sec in (1, 2, 3, 3):
            add("employer", 2, 0, self._profile_src(SECTOR_GUILDS[sec][int(r.integers(len(SECTOR_GUILDS[sec])))]), sec, False)
        for _ in range(2): add("union", 2, 0, self._profile_src("gruul selesnya"), -1, False)
        for _ in range(2): add("charity", 2, 0, self._profile_src("selesnya"), -1, False)
        for f in range(NF): add("faith body", 2, 0, self.FPROF[f].copy(), -1, False)
        self.party_ids = []
        for j in range(4):
            prof = _norm(self.V * np.exp(0.35 * self._cn(r)))
            self.party_ids.append(len(rows)); add("party", 2, 0, prof, -1, False)
        n = len(rows)
        self.n_inst = n
        self.inst_kind = np.array([x[0] for x in rows]); self.inst_level = np.array([x[1] for x in rows])
        self.inst_loc = np.array([x[2] for x in rows]); self.inst_native = np.array([x[3] for x in rows])
        self.inst_sector = np.array([x[4] for x in rows]); self.inst_public = np.array([x[5] for x in rows])
        self.inst_profile = self.inst_native.copy()
        self.inst_faith = np.full(n, -1); fb = np.nonzero(self.inst_kind == INST_KINDS.index("faith body"))[0]
        self.inst_faith[fb] = np.arange(NF)
        self.party_ids = np.array(self.party_ids)
        k = self.inst_kind
        K = {x: INST_KINDS.index(x) for x in INST_KINDS}
        self.inst_firm = ((k == K["employer"]) & ~self.inst_public) | (k == K["bank"])     # market firms
        self.inst_pubemp = (k == K["employer"]) & self.inst_public                         # public employers
        reach = np.array([{"school": .4, "university": 1.5, "employer": 1.0, "bank": 2.0, "hospital": .8, "police": .6,
                           "court": .8, "prison": .3, "army": 1.5, "faith body": 0.0, "media": 1.0, "party": 0.0,
                           "union": 1.5, "charity": .8, "council": .4, "ministry": 2.0}[INST_KINDS[x]] for x in k])
        reach *= np.where(self.inst_level == 2, 2.5, 1.0)
        self.inst_reach = reach                            # faith bodies get their faith's share, yearly
        base = {"school": .65, "university": .65, "employer": .50, "bank": .45, "hospital": .70, "police": .60,
                "court": .52, "prison": .40, "army": .65, "faith body": .48, "media": .46, "party": .25, "union": .45,
                "charity": .60, "council": .45, "ministry": .40}   # OECD Trust Survey 2023 where measured (media set
                                                                         # higher so its lower capacity lands it near 0.4); others estimates
        self.inst_legit0 = np.array([base[INST_KINDS[x]] for x in k])
        self.inst_legitimacy = _uclip(self.inst_legit0 + 0.05 * r.normal(size=n), .05, .95)
        self.inst_capacity = _uclip(0.7 + 0.08 * r.normal(size=n), .2, 1)
        self.inst_corruption = _uclip(0.12 + 0.05 * r.normal(size=n), .01, .6)
        self.inst_age = r.uniform(5, 80, n)
        self.inst_age[self.inst_firm & (self.inst_level == 0)] = r.uniform(0, 30, (self.inst_firm & (self.inst_level == 0)).sum())
        self.inst_finances = _uclip(0.5 + 0.15 * r.normal(size=n), 0, 1)
        self.inst_leader_fig = np.full(n, -1)
        self.inst_leader_pie = _norm(np.where(self.inst_public[:, None], self.G, self.V) * np.exp(0.3 * self._cn(r, n)))
        self.inst_leader_q = r.integers(0, 24, n).astype(float)
        self.inst_gen = np.zeros(n, int)                    # bumps when a firm closes and a new one takes its place
        oc = np.array([.78, .92, 1.0])
        self.inst_open_cls = _uclip(oc + 0.04 * r.normal(size=(n, 3)), .3, 1)
        self.inst_open_mig = _uclip(0.70 + 0.05 * r.normal(size=n), .3, 1)    # Bertrand and Mullainathan 2004: ~2/3
        self._openness()
        self._state_corruption()

    def _state_corruption(self):
        """state.corruption (package registry): the public bodies' corruption weighted by their reach."""
        w = self.inst_public * self.inst_reach
        self.corruption = float(w @ self.inst_corruption / max(float(w.sum()), 1e-9))

    def _openness(self):
        self.inst_openness = (self.inst_open_cls[:, :, None] * np.stack([np.ones(self.n_inst), self.inst_open_mig], 1)[:, None, :]).reshape(self.n_inst, 6)

    def _init_figs(self, r):
        self.F_role, self.F_pie, self.F_standing, self.F_alive, self.F_party = [], [], [], [], []
        self.F_born, self.F_female, self.F_mom, self.F_active, self.F_inst = [], [], [], [], []
        self.fig_role_now = {}
        self.fig = -1
        for role in range(len(FIG_ROLES)):
            self._new_fig(r, role, quiet=True)

    # public figures as arrays (world-build.md: W.fig_* role, pie, standing, alive, party)
    fig_role = property(lambda self: np.array(self.F_role, int))
    fig_pie = property(lambda self: np.array(self.F_pie, float).reshape(-1, C))
    fig_standing = property(lambda self: np.array(self.F_standing, float))
    fig_alive = property(lambda self: np.array(self.F_alive, bool))
    fig_party = property(lambda self: np.array(self.F_party, int))
    fig_born = property(lambda self: np.array(self.F_born, int))
    fig_female = property(lambda self: np.array(self.F_female, bool))
    fig_active = property(lambda self: np.array(self.F_active, bool))
    fig_inst = property(lambda self: np.array(self.F_inst, int))

    def _set_role(self, role, fid):
        old = self.fig_role_now.get(role)
        if old is not None and old != fid:
            self.F_active[old] = False
        self.fig_role_now[role] = fid
        self.F_role[fid] = role; self.F_active[fid] = True
        inst = self.F_inst[fid]
        if role in (0, 1):
            inst = int(self.party_ids[self.F_party[fid]]); self.F_inst[fid] = inst
        if inst >= 0:
            self.inst_leader_fig[inst] = fid; self.inst_leader_pie[inst] = np.asarray(self.F_pie[fid]); self.inst_leader_q[inst] = 0
        self.fig = self.fig_role_now.get(0, -1)

    def _new_fig(self, r, role, quiet=False, party=None):
        """A new public figure rises into a role (spec 5 §6). Pies come from what the role stands in (party, faith,
        firm, the society), never from a rule about the role's colors."""
        x = r.random(4); nz = self._cn(r)
        rn = FIG_ROLES[role]
        inst = -1
        if role in (0, 1):
            party = (self.gov_party if role == 0 else self.opp_party) if party is None else party
            inst = int(self.party_ids[party]); base = self.inst_profile[inst]
        elif rn == "preacher":
            inst = int(np.nonzero(self.inst_faith == int(np.argmax(self.faith_share[:NF])))[0][0]); base = self.FPROF[self.inst_faith[inst]]
        elif rn == "scientist":
            inst = int(np.nonzero(self.inst_kind == INST_KINDS.index("university"))[0][0]); base = self.inst_profile[inst]
        elif rn == "magnate":
            cand = np.nonzero(self.inst_firm & (self.inst_level == 2))[0]; inst = int(cand[int(x[3] * len(cand))]); base = self.inst_profile[inst]
        elif rn == "activist":
            base = self.Dem_q
        else:
            base = self.V
        pie = _norm(base * np.exp((0.35 if rn in ("star", "athlete") else 0.25) * nz))
        fid = len(self.F_role)
        age = {"athlete": 22, "star": 26}.get(rn, 40) + 12 * x[0]
        self.F_role.append(role); self.F_pie.append(pie.tolist()); self.F_standing.append(float(0.35 + 0.3 * x[1]))
        self.F_alive.append(True); self.F_party.append(-1 if party is None else int(party))
        self.F_born.append(int(self.t - age * 52)); self.F_female.append(bool(x[2] < 0.5)); self.F_mom.append(0.05)
        self.F_active.append(True); self.F_inst.append(inst)
        self._set_role(role, fid)
        if not quiet:
            self._event("figure", "rises", rn, dict(fig=fid, party=self.F_party[fid]), big=role == 0)
        return fid

    # ------------------------------------------------------------------------------------------------ clock
    def burn_in(self, years=80):
        """The world alone before the birth (spec 5 §4). Ends with t0 = the birth's world week. The climate scenario is
        anchored at the first birth only: a saved world run on before a later birth keeps its warming."""
        self.t0 = self.t + int(round(years * 52))
        if self.clim_t0 is None:
            self.clim_t0 = self.t0
        while self.t < self.t0:
            self._week()
        return self

    def tick(self, week=None):
        """Run the world up to the given world week (every week in between), or one week when week is None."""
        target = self.t + 1 if week is None else int(week)
        while self.t < target:
            self._week()

    # ------------------------------------------------------------------------------------------------ emigration (spec 5 §5)
    def spawn_neighbour(self, k, years=60):
        """A full World for neighbour k, for a character who emigrates there (spec 5 §5).

        Built from the neighbour's light state here: its value climate (the preset), regime, richness (tech level),
        government colors, economy phase and relation, with its own streams from (seed, society id = k + 1). It runs
        alone for `years` before this world's clock (from 0 when this world is younger), so its t equals this world's
        t, and shares t0 and the climate anchor. In it this world is neighbour 0, its relation mirrored, and this
        world's other neighbours follow; ext_society gives each neighbour's society id. Nothing here touches this
        world's state or streams, so the home world ticks on exactly as before. Entry k of a spawned world whose
        ext_society is 0 is the home world itself: keep using that World (ValueError here)."""
        k = int(k)
        soc = np.asarray(getattr(self, "ext_society", np.arange(self.n_ext) + 1))
        sid = int(soc[k])
        if sid == 0:
            raise ValueError("neighbour %d is the home world; go back to that World" % k)
        rich = float(self.ext_rich[k])
        cfg = {a: b for a, b in self.cfg.items() if a != "legacy"}
        cfg.update(preset=[float(v) for v in self.ext_V[k][np.argsort(self.perm)]], regime=float(self.ext_regime[k]),
                   tech_level=self.cfg["tech_level"] if rich >= 0.65 else "behind", trace=False)
        start = max(self.t - int(round(years * 52)), 0)
        N = World(self._seed, cfg=cfg, color_perm=self.perm.tolist(), params=dict(self.p), society=sid, start_t=start)
        N.rich = rich
        N.t0 = int(self.t0)
        N.clim_t0 = int(self.clim_t0 if self.clim_t0 is not None else self.t0)
        N._ext_from(self, k)
        N.tick(self.t)
        N.regime = float(self.ext_regime[k]); N._regime_derived()      # the light state at arrival
        N.G = self.ext_G[k].copy()
        N._force_phase(int(self.ext_phase[k]), int(self.ext_rec_q[k]))
        N._ext_from(self, k)
        if self.war and self.war_with == k:              # at war with each other: the front is mirrored
            N.war, N.war_with, N.war_q = 3 - int(self.war), 0, int(self.war_q)
        elif self.ext_war[k]:                            # at war elsewhere (the war that sends refugees)
            if not N.war:
                N.war, N.war_with, N.war_q = 2, -1, 0
        else:
            N.war, N.war_with = 0, -1
        N._derive_econ()
        return N

    def _ext_from(self, home, k):
        """Neighbours seen from a spawned neighbour: home (entry 0, the relation mirrored), then home's others."""
        others = [j for j in range(home.n_ext) if j != k]
        n = 1 + len(others)
        hsoc = np.asarray(getattr(home, "ext_society", np.arange(home.n_ext) + 1))
        self.n_ext = n
        self.ext_society = np.array([home.society_id] + [int(hsoc[j]) for j in others])
        self.ext_regime = np.array([float(home.regime)] + [float(home.ext_regime[j]) for j in others])
        self.ext_V = np.vstack([home.V] + [home.ext_V[j] for j in others])
        self.ext_anchor = np.vstack([home.VPRE] + [home.ext_anchor[j] for j in others])
        self.ext_G = np.vstack([home.G] + [home.ext_G[j] for j in others])
        self.ext_rich = np.array([float(getattr(home, "rich", 1.0))] + [float(home.ext_rich[j]) for j in others])
        reg = self.ext_regime
        rel = np.where((reg >= 6) & (self.regime >= 6), 0, np.where((reg < 0) | (self.regime < 0), 2, 1))
        rel[0] = home.ext_relation[k]
        self.ext_relation = rel.astype(int)
        self.ext_trade = np.array([float(home.ext_trade[k])] + [float(home.ext_trade[j]) for j in others])
        self.ext_phase = np.array([int(home.phase)] + [int(home.ext_phase[j]) for j in others])
        self.ext_rec_q = np.array([int(home.rec_q) if home.phase == 1 else 99] + [int(home.ext_rec_q[j]) for j in others])
        self.ext_exp_q = np.array([int(home.exp_q)] + [int(home.ext_exp_q[j]) for j in others])
        self.ext_war = np.array([int(home.war > 0)] + [int(home.ext_war[j]) for j in others])
        self.ext_next_gov = np.array([max(int(home.next_vote), 1) if home.regime >= 0 else 28]
                                     + [int(home.ext_next_gov[j]) for j in others])
        self.ext_migration = _uclip(0.2 * (1 - self.ext_rich) + 0.6 * self.ext_war + 0.2 * (self.ext_phase == 1), 0, 1)
        self.world_rec, self.world_q = int(home.world_rec), int(home.world_q)
        if self.war_with >= n:
            self.war_with = -1

    def _force_phase(self, ph, rec_q=0):
        """Set the economy's phase to a spawned neighbour's light state (a mild recession starts or the one running ends)."""
        if ph == 1 and self.phase == 0:
            self.phase, self.severity, self.rec_q = 1, 0, int(min(max(rec_q, 0), 3))
            self.rec_len = max(self.rec_q + 2, 3)
            self.u_rise_tgt = self.u_rise + self.p["u_rise"][0]
            self.rec_start_t = int(self.t - 13 * self.rec_q); self.n_rec += 1
            self.cycles.append([self.rec_start_t, -1, 0])
        elif ph == 0 and self.phase == 1:
            self.phase, self.exp_q, self.last_sev = 0, 0, self.severity
            self.rec_end_t = self.t
            self.cycles[-1][1] = int(self.t)
        self._derive_econ()

    def _week(self):
        self.t += 1
        self.week_of_year = self.t % 52
        self.season = int(WEEK_SEASON[self.week_of_year])
        if self.dis_on:                                    # last week's strikes are over
            self.disaster_now[:] = 0; self.disaster_kind[:] = -1; self.dis_on = False
        if self.dis_pending:
            self._strike()
        if self.t % 13 == 0:
            self._quarter()
        if self.t % 52 == 0:
            self._year()

    def _quarter(self):
        self._apply_pushes()
        self._nature_q()
        self._ext_q()
        self._econ_q()
        self._state_q()
        self._inst_q()
        self._place_q()
        self._culture_q()
        self._society_q()
        if (self.p.get("sph_town", False) or self.p.get("sph_haunts", False) or self.p.get("sph_hours", False)
                or self.p.get("sph_events", False) or self.p.get("sph_pairs", False)):
            self._sphere_q()   # (phase 2's haunts and hours read the town spheres, so either switch computes them)
            if self.p.get("sph_haunts", False):
                self._sph_places_q()
                if self.p.get("place_turnover", False):   # finishing pack, part 2: places close and open
                    self._pt_q()
        self._figures_q()
        self._history_q()
        if self.trace is not None:
            self._trace()

    def _year(self):
        self._tech_y()
        self._belief_y()
        if self.p.get("c5_faith"):
            self._c5_y()
        self._generations_y()
        self._pop_y()
