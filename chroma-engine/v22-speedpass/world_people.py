"""world_people.py: the per-character side of the outer world (chroma-world specs 2, 3 and 7; the interface is
chroma-engine/world-build.md, "world_people.py: what it exposes").

Vectorised over the run's N lives, all born in one shared World W at the same world week t0. Per life:
- drawn birth: locality, neighbourhood, family class, parents, siblings, grandparents, aunts, uncles and cousins
  (spec 3 §2.5b), from the society's population shares;
- the named cast (spec 2): up to K people with their own pies, the character's reading of them, closeness (which sets
  the layer), trust, contact, marks and debts, a light life of their own (age, health, money, partner, job, mood:
  ruling R8, no reduced engine per person) and at most one want toward the character;
- settings (spec 3 §1): household, class, work, congregation, club, scene, online, neighbours, gang, unit, ward and
  movement, with norms, cohesion, the character's rank and time share, members, leader, gate and exit cost;
- what the engine reads each week: niche, msg_w, support, belong, alive, community, ties, approval, standing and
  felt reach (spec 7 §2, §6);
- levers and pushes (spec 7 §3; reach per domain), `who` slots, wants due, place and moving (with candidate
  localities), emigration to a neighbour society and return (spec 5 §5: society id, status, language, harder gates at
  first), views for the game (cast, place, settings, reach, public figures through the character's reading), save and
  load.

Rules kept (world-build.md): fit between two pies is overlap or distance only, the same for every pair of colors;
one random stream per (world seed, run seed); the world's history is only touched through W.push; no years, names or
brands (names are integer indices the game maps); numpy and stdlib only.

Cadence (t: the world week): week (cast layers 1-2: contact, closeness, deaths; partner and children follow the
engine; wants ripen; niche, msg_w, support, help, belong, felt reach, contagion, events), month when t % 4 == 0 (the
life course of settings, contact in settings, the close index, standing and reach, community, ties, the alive friend
column; the settings' slow drift of norms, cohesion and strictness every second month), quarter when t % 13 == 0
(cast layers 3-4, the reading, trust and breaks, members' turnover, new people, roles, wants arising, the full alive
counts, local norm and approval; the cast's own light lives every half year). `tick(t, S)` runs all three on their
weeks; each is safe to call twice in a week.
"""
# Since the split (chroma-engine/CLAUDE.md): the module code outside class People is in world_people_base.py and
# People's methods are in the nine mixin modules below; this file keeps the class and its __init__. Every name
# world_people.py had is still importable from world_people.
from world_people_base import *  # noqa: F401,F403
from world_people_base import (_EPS, _EPS6, _LOWBIT, _LUT, _NKI, _NW, _csum, _isin_small, _ix, _logit, _norm, _nz2,
    _sig, _uclip)  # noqa: F401
from world_people_roster import RosterMixin
from world_people_settings import SettingsMixin
from world_people_ticks import TicksMixin
from world_people_lives import LivesMixin
from world_people_sacred import SacredMixin
from world_people_eyes import EyesMixin
from world_people_acts import ActsMixin
from world_people_lead import LeadMixin
from world_people_views import ViewsMixin
from world_people_answers import AnswersMixin, WA_KEPT, WA_NATION, WA_RINGS, WA_SCOPES, WA_SIZES, WA_UNITS  # noqa: F401

# the modules that make up world_people (the Engine's checks read their sources, and the world cache hashes them)
_PARTS = ('world_people_base', 'world_people_roster', 'world_people_settings', 'world_people_ticks',
          'world_people_lives', 'world_people_sacred', 'world_people_eyes', 'world_people_acts', 'world_people_lead',
          'world_people_views', 'world_people_answers')


class People(RosterMixin, SettingsMixin, TicksMixin, LivesMixin, SacredMixin, EyesMixin, ActsMixin, LeadMixin,
             ViewsMixin, AnswersMixin):
    """The cast, settings, place and reach of N characters in one World (see the module docstring)."""

    def __init__(self, W, N, run_seed=0, female=None, cfg=None):
        P = dict(PP_DEFAULT); P.update(cfg or {}); self.P = P
        self.W = W; self.N = N = int(N); self.K = K = int(P["K"]); self.M = M = int(P["M"])
        self.KC = min(int(P["KC"]), K)
        self.seed = int(getattr(W, "seed", getattr(W, "_seed", 0))); self.run_seed = int(run_seed)
        self.rng = np.random.default_rng([self.seed, 31, self.run_seed])
        # color-indexed draws are made in the world's canonical frame and relabelled like every color table, so a
        # World(color_perm=p) gives the same lives with their colors relabelled (the equivariance test)
        cp = P.get("color_perm")
        self.perm = np.asarray(getattr(W, "perm", np.arange(C)) if cp is None else cp, np.int64)
        self.iperm = np.argsort(self.perm)
        self.female = (np.zeros(N, bool) if female is None else
                       np.broadcast_to(np.asarray(female, bool), (N,)).copy())
        z = lambda dt, v: np.full((N, K), v, dt)
        # the cast: one row per life, one column per slot
        i32 = np.int32   # ids, name indices and weeks fit in 32 bits (half the memory traffic of int64)
        self.used = z(bool, False); self.lv = z(bool, False); self.uid = z(i32, -1)
        self.nm = z(i32, 0); self.line = z(i32, 0); self.kof = z(i32, -1)
        self.role = z(np.int8, -1); self.rmask = z(np.int32, 0); self.face = z(bool, False)
        self.born = z(i32, 0); self.fem = z(bool, False); self.since = z(i32, 0); self.died_t = z(i32, NEVER)
        self.pie = np.full((N, K, C), 1.0 / C, np.float32); self.read = np.full((N, K, C), 1.0 / C, np.float32)
        self.c = z(np.float32, 0.0); self.cmax = z(np.float32, 0.0); self.trust = z(np.float32, 0.5)
        self.last = z(i32, NEVER); self.fsh = z(np.float32, 0.0); self.fkin = z(np.float32, 0.0)
        self.fkin_far = z(np.float32, 0.0); self.mset = z(np.uint8 if M <= 8 else np.uint16, 0)
        self.debt = z(np.int8, 0); self.mgood = z(np.uint8, 0); self.mbad = z(np.uint8, 0)
        self.secret = z(bool, False); self.brk = z(i32, NEVER)
        self.health = z(np.float32, 1.0); self.money = z(np.float32, 0.5); self.mcls = z(np.int8, 1)
        self.emp = z(bool, False); self.sector = z(np.int8, -1); self.inst = z(i32, -1)
        self.mpart = z(bool, False); self.nkids = z(np.int8, 0); self.mood = z(np.float32, 0.6)
        self.want = z(np.int8, -1); self.wripe = z(np.float32, 0.0); self.wstate = z(np.int8, 0)
        self.wknown = z(bool, False); self.wdue = z(i32, NEVER); self.stand = z(np.int8, 0)
        self.mloc = z(i32, 0); self.faith = z(np.int16, -1); self.party = z(i32, -1)
        self.strict = z(np.float32, 0.0); self.fbiz = z(bool, False); self.inci = z(bool, False)
        self.unext = np.zeros(N, np.int64)
        # settings
        assert M <= 8, "settings are a byte of bits per cast member"
        self.skind = np.full((N, M), -1, np.int8); self.snorm = np.full((N, M, C), 1.0 / C, np.float32)
        self.sanch = np.full((N, M, C), 1.0 / C, np.float32)
        self.scoh = np.zeros((N, M), np.float32); self.srank = np.zeros((N, M), np.float32)
        self.sts = np.zeros((N, M), np.float32); self.ssize = np.zeros((N, M), np.int64)
        self.sncast = np.zeros((N, M), np.int64); self.sgate = np.zeros((N, M), np.int8)
        self.sxcost = np.zeros((N, M), np.float32); self.sform = np.zeros((N, M), np.int64)
        self.sjoin = np.zeros((N, M), np.int64); self.sref = np.full((N, M), -1, np.int64)
        self.slead = np.full((N, M), -1, np.int64)   # leader's slot, -1 none, -2 the character
        self.sstrict = np.zeros((N, M), np.float32); self._fitm = np.zeros((N, M), np.float32)
        self._sh = np.arange(M, dtype=self.mset.dtype)[None, :, None]
        # the person
        self.loc = np.zeros(N, np.int64); self.nb = np.zeros(N, np.int64); self.cls = np.ones(N, np.int64)
        self.pfaith = np.full(N, -1, np.int64); self.pparty = np.full(N, -1, np.int64); self.pline = np.zeros(N, np.int64)
        self.hhj = np.full(N, -1, np.int64); self.own_home = np.zeros(N, bool); self.pslot = np.full(N, -1, np.int64)
        self.psector = np.full(N, -1, np.int64); self.n_moves = np.zeros(N, np.int64); self.last_move = np.full(N, NEVER)
        self.par_change = np.full(N, NEVER); self.older_sib = np.zeros(N, np.int64); self.younger_sib = np.zeros(N, np.int64)
        self.family_mix = np.full((N, C), 1.0 / C); self.vol_tgt = np.zeros(N, np.int64); self.sociab = np.ones(N)
        self.fr_bias = np.zeros(N); self.objk = np.zeros((N, NNORM)); self.cont_t = np.full((N, 2), NEVER)
        self.lens = np.full((N, C), 1.0 / C); self.w = np.full((N, C), 1.0 / C); self.w32 = self.w.astype(np.float32)
        self._lkm = np.zeros((N, K), np.float32); self._Dn = np.zeros(N, np.float32)
        self._psq = np.full((N, K), 1.0 / C, np.float32)   # each cast member's sum of squared shares (their spread)
        self.held = np.zeros((N, len(KN)), bool); self.dead = np.zeros(N, bool); self._nch = np.zeros(N, np.int64)
        self._nchl = np.zeros(N, np.int64)   # the character's living children in the cast
        self.kids_eng = None                 # the engine's living children (S["children"]), when it sends them
        # what the engine reads
        self.niche = np.full((N, C), 1.0 / C); self.msg_w = np.ones(N); self.support = np.zeros(N); self.help = np.zeros(N)
        self.belong = np.zeros(N); self.alive = np.zeros((N, len(ENGINE_ROLES))); self.community = np.zeros(N)
        self.ties = np.zeros(N); self.approval = np.zeros((N, NNORM)); self.local_norm = np.full((N, NNORM), 0.5)
        self.standing = np.zeros((N, 4)); self.reach = np.tile(REACH[0], (N, 1)); self.felt_reach = self.reach.copy()
        self.dstanding = np.zeros((N, len(DOMAINS))); self.dreach = np.tile(REACH[0][RING_OF], (N, 1))
        self.died = np.zeros((N, len(ENGINE_ROLES)), np.int64)
        self.contagion = dict(divorce=np.ones(N), quit=np.ones(N))
        self.events = []; self._carry = []; self._due = []; self.pend = {}
        self._setmix = np.zeros((N, C)); self._setw = np.zeros(N); self._belong_set = np.zeros(N); self._comm = np.zeros(N)
        self._den = np.ones(N); self.ci = np.zeros((N, self.KC), np.int64)
        self._r_w = [np.float32(1 - np.exp(-1 / 52.0 / P[k_])) for k_ in ("tau_up", "tau_dn_kin", "tau_dn")]
        ma_ = P["move_age"]   # yearly moving rate by whole year of age (the table's line at mid-year)
        self._mr_tab = np.interp(np.arange(121) + 0.5, [a_ for a_, _ in ma_], [r_ for _, r_ in ma_]).astype(np.float32)
        self._last_m = self._last_q = self._last_w = self._last_appr = self._last_set = None; self._defer = None
        self._last_lives = 0
        self.t0 = 0; self.t = 0
        self.watch = np.ones(N, bool) if P["watch"] is None else np.isin(np.arange(N), np.asarray(P["watch"]))
        self.nh = []; self._coh_tab = None; self._coh_y0 = 0
        self._kf_near = np.array([P["kin_f"].get(r_, (0, 0))[0] for r_ in ROLE], np.float32)
        self._kf_far = np.array([P["kin_f"].get(r_, (0, 0))[1] for r_ in ROLE], np.float32)
        self.res = np.full((N, len(RESOURCES)), 0.5); self.stress = np.zeros(N); self.outlook = np.full(N, 0.45)
        self.attr = np.zeros(N, np.int64); self.risky = np.zeros(N); self.title_st = None; self.partner_same = None
        self.dom_st = None
        # the society each life lives in (spec 5 §5): its id (0 home; a neighbour its index + 1), the life's status
        # there, its language skill; per cast member, the society they live in (msoc)
        hs = self._wf("society_id", 0); hs = int(hs) if np.ndim(hs) == 0 else 0
        self.soc = np.full(N, hs, np.int64); self.soc_home = self.soc.copy()
        self.stat = np.zeros(N, np.int8); self.lang = np.ones(N); self.arr_t = np.full(N, NEVER)
        self.cls_home = np.ones(N, np.int64); self.loc_home = np.zeros(N, np.int64); self.par_apart = np.zeros(N, bool)
        self.msoc = z(np.int16, hs)
        self._xsoc = False   # True once a life has lived abroad: only then are societies compared (home lives unchanged)
        self._smem = {}      # (life, society id): (language, status) kept for a return
        self._Ws = {}        # N == 1: the Worlds left behind, by society id
        self._world_static()
        # the spheres of society, phase 2 (item 15): the world's switches decide; off, none of this exists
        wp_ = getattr(W, "p", None) or {}
        self.sph_h = bool(wp_.get("sph_haunts", False)); self.sph_hr = bool(wp_.get("sph_hours", False))
        self.sph_mk = bool(wp_.get("sph_marks", False))
        if self.sph_h or self.sph_hr or self.sph_mk:
            self._sph_init()
        # phase 4: the levers on places and town spheres, and felt fairness per sphere (each off: nothing of it exists)
        self.sph_lv = bool(wp_.get("sph_levers", False)); self.sph_fr = bool(wp_.get("sph_fair", False))
        if wp_.get("sph_deep", False):   # phase 5, service as a chapter: comrades met in a unit fade at half speed
            self.comrade = np.zeros((N, K), bool)
            self.roots = np.zeros(N, bool)       # debts and holdings: a life holding something moves half as readily
            self.care_buy = np.zeros(N, bool)    # a carer with money buys help (the engine sets it each month)
        if wp_.get("prison_ties", False):   # spheres finishing pack, part 4: fellow inmates (the engine makes them at a
            self.inmate = np.zeros((N, K), bool)       # release) fade at half speed for 10 years from when they were made
            self.inmate_t = np.full((N, K), NEVER, np.int64)
        self.far_on = bool(wp_.get("far_ties", False))
        if self.far_on:   # far_ties (item 18): the towns' events touch the people living there; a far tie calls
            self._far_init(run_seed)
        # S3 and S4 (chroma-ideas/social-mechanics.md): off, nothing of them exists (S5 asks getattr(PP, "eyes_on", False))
        self.eyes_on = bool(wp_.get("sph_eyes", False)) and self.sph_h   # with the haunts (their places and life stages)
        self.odd_on = self.eyes_on and bool(wp_.get("sph_odd", False))
        if self.eyes_on:
            self._eyes_init(wp_)
        self.lw = bool(wp_.get("lead_ways", False)) and self.sph_lv   # S7: ways to lead, with phase 4's levers
        if self.lw:
            self._lead_init()
        self.sac_on = bool(wp_.get("sacred", False))
        if self.sac_on:   # S5, sacred lines: what a life will not sell, and the offers made for it (off: nothing of it exists)
            self._sac_init(run_seed)
        self.seen_on = bool(wp_.get("seen_done", False))
        if self.seen_on:   # seen_done (S6): the paths and colour ways each life has seen walked; felt odds and dreams read it
            self._seen_init()
        self.pt_on = bool(wp_.get("place_turnover", False)) and self.sph_h
        if self.pt_on:     # finishing pack, part 2: their places close and new ones open (off: nothing of it exists)
            self._pt_init(run_seed)
        if self.sph_lv or self.sph_fr:
            self.fair = np.full((N, 9), 0.5)    # felt fairness in each sphere, 0..1 (sph_fair)
            self.fair_log = []                  # [week, life, sphere, +1 went well / -1 badly]: voice and loyalty acts
            self._p4_yr = -1
        self.fr_read = bool(wp_.get("fair_read", False)) and self.sph_fr
        self.bt_on = bool(wp_.get("body_trust", False)) and self.sph_fr
        if self.bt_on:   # body_trust (finishing pack part 3): trust in each sphere's bodies (off: nothing of it exists)
            self._bt_init()
        if self.fr_read:   # S1: fairness read five ways (the town events already fired are not read)
            self._fr_i = len(getattr(W, "sph_ev_log", ()))
            self._fr_n = np.zeros(5)    # how often each part of fairness was heard of lately (habituation; FR_HABIT)
            self.fr_cnt = np.zeros(5)   # every move applied, by part (read only: tools/fair_check.py s1_counts)
