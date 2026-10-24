"""The land (v25 lane D, the engine's switch wa_land with world_answers and the world on; chroma-world/spheres/land-v1.md,
the values in sphere_data.LAND and what LAND leaves to the engine in the realm's LAND_ENGINE and LAND_DECIDE).

Earth's land is physical (decision #2): its health, wildness and hazards follow uses, weather and recovery rates, and it
reaches people through hazards, harvests, time outdoors and loss. Nothing here reads anyone's colour, and the land
wants, approves of or punishes nothing; colour enters only through what a person chooses to do (an option's face).
Three units, each whole behind its switch (decision #7's cut order):

  protected (wa_land itself): each town's three stretches (field, wood, water; health and wildness) with their recovery,
      the hazards' hits on them and their feedback on the hazard odds (World.land_hx: a drained marsh floods the town
      more, a wild untended wood burns hotter), the households a strike hits and the shape of their years after
      (after_disaster), the rest of the town's lesser blow, heat on the old and frail and its quarrels (x 1.1 for a
      spell: People's ties tick reads quarrel_x), the town's trust after a hit,
      "a loved stretch lost" for N3 (imp_world's land fact), and the scenario hook (scn: a hazard or a harvest the
      caller brings to a life's town)
  wa_land_dev (2nd in the cut order): what reaches lives left alone - the home health's drift with the town's uses and
      the times, time in nature (the dose), the harvests, sick land (solastalgia) and climate worry
  wa_land_play (6th): the nature moments (the batch's, load_batch(land=True)) at about one a year, who is there with
      the character (S["company"]), the options' faces, the ways they open (three held at most, each a ladder of three
      steps on its own clock), the bridges two ways open together, a Known life's land decisions (world answers'
      phase 2) on a stretch; the company's lasting parts (kin: a shared memory, recalled when they die; a group: its norm
      a little toward the chosen face), and notice (people 2.0: the tenders, or the builders and farmers, ask a life
      that leans their way in to one of their ways; those a choice costs push back through their rival moment)

Its own dice streams (the world seed's for the start, so a world keeps its land; _rng for the lives), so it moves no
other stream; the moments it brings and the ties it changes do change the lives, as they should, with the switch on."""
import re

import numpy as np

from world_base import HAZARDS, LOC_KINDS
from world_keys import HAUNT_KINDS, SECTORS
from world_people_base import BIT, G, NEVER, R

STRETCHES = ("field", "wood", "water")
F_, WO_, WA_ = 0, 1, 2
HARVESTS = ("good", "normal", "poor")
SHAPES = ("resilient", "recovery", "chronic", "delayed")
SIZES = {"a little": 0.02, "small": 0.1, "clear": 0.25, "strong": 0.5, "very strong": 1.0}
# the engine's needs and resources (library.NEEDS, RESOURCES), by index
N_SAF, N_BEL, N_MEA = 0, 1, 4
R_MON, R_TIM, R_HEA = 0, 1, 2
_HAPPENS = re.compile(r"(wellbeing|stress|health|vitality|meaning|belonging|safety|money|yield|town trust|land health|"
                      r"land wildness)\s*([+-])\s*(very strong|strong|clear|small|a little)")
KIN_BITS = BIT["parent"] | BIT["grandparent"] | BIT["sibling"] | BIT["child"] | BIT["kin"] | BIT["grandchild"] | BIT["inlaw"]
COMPANY_BITS = dict(friend=BIT["friend"], partner=BIT["partner"], kin=KIN_BITS, rival=BIT["rival"],
                    group=BIT["member"] | BIT["colleague"] | BIT["neighbour"])
LADDER_YEARS_DEFAULT = (2.0, 0.0, 5.0)


def _clip(x, lo=0.0, hi=1.0):
    return np.minimum(np.maximum(x, lo), hi)


def health_word(h):
    return "thriving" if h >= 0.75 else "fair" if h >= 0.5 else "worn" if h >= 0.3 else "sick"


def wild_word(w):
    return "wild" if w >= 0.6 else "half-wild" if w >= 0.3 else "tamed"


class Land:
    """The land of one world and its lives (WorldLink.land, People.land). Made by WorldLink.land_setup()."""

    def __init__(self, W, PP, P, L, R_, par_i=1):
        import sphere_data as SD
        self.T = SD.LAND; E = self.E = dict(R_.LAND_ENGINE, **(P.get("wa_land_par") or {})); self.R = R_
        self.W, self.PP = W, PP; N = self.N = int(PP.N)
        self.dev = bool(P.get("wa_land_dev", True)); self.play = bool(P.get("wa_land_play", True))
        self.par_i = int(par_i)
        ST = self.T["stretches"]; assert tuple(ST["order"]) == STRETCHES
        nl = self.nl = int(W.n_loc)
        cls = np.array([["city", "town", "rural"][int(c_)] for c_ in np.asarray(W.loc_place)])
        base = np.array([ST["start"][c_] for c_ in cls], float)                       # nl x (health, wildness)
        r0 = np.random.default_rng([int(PP.seed), 7731])                             # the world's own: its land
        nz = r0.uniform(-1.0, 1.0, (nl, 3, 2)) * float(ST["start_noise"])
        self.h = _clip(base[:, None, 0] + nz[..., 0], 0.02, 1.0)
        self.wd = _clip(base[:, None, 1] + nz[..., 1], 0.0, 1.0)
        self.h0, self.wd0 = self.h.copy(), self.wd.copy()
        self.home, self.whome = self.h.copy(), self.wd.copy()                       # what each stretch recovers to
        self.rec = np.array([float(ST["recover"][s_]) for s_ in STRETCHES])
        hits = ST["hazards"]["hits"]
        self.hits = np.array([[float(hits.get(hz_, {}).get(s_, 0.0)) for s_ in STRETCHES] for hz_ in HAZARDS])
        kinds = ST["kinds"]
        self.names = [list(kinds.get(LOC_KINDS[int(k_)], STRETCHES)) for k_ in np.asarray(W.loc_kind)]
        self._rng = np.random.default_rng([int(PP.seed), 7733, int(PP.run_seed)])
        # the towns
        self.hz_kind = np.full(nl, -1, np.int64); self.hz_t = np.full(nl, NEVER, np.int64)
        self.harvest = np.ones(nl, np.int64); self.harvest_t = np.full(nl, NEVER, np.int64)
        self.trust_t = np.full(nl, NEVER, np.int64)
        self.tend = np.zeros((nl, 3))
        self.ext0 = float(np.mean(np.asarray(W.extremes, float)))
        self.load0 = self._load()
        self.wcut = np.zeros(nl)                    # the wood's wildness lost to decisions this year (wood_cleared)
        self.wplan = np.full(nl, NEVER, np.int64)   # a decision to clear or take the wood (protest_at_the_wood)
        self.hx = np.ones((nl, len(HAZARDS)))
        W.land_hx = self.hx                         # read by World._nature_q and rate_mult("disaster")
        # the lives
        self.hit_t = np.full(N, NEVER, np.int64); self.shape = np.full(N, -1, np.int64); self.chron_end = np.zeros(N, bool)
        self.displaced = np.zeros(N, bool)
        self.att = np.full(N, -1, np.int64); self.att_h = np.full((N, 3), np.nan); self.att_w = np.full((N, 3), np.nan)
        self.lost = np.zeros(N, bool); self.lost_j = np.full(N, -1, np.int64); self.hy = np.zeros((N, 3))
        self.worry = np.full(N, -1, np.int64)
        self.walk = self._rng.lognormal(0.0, float(E["walk_sd"]), N)
        self.mins = np.zeros(N); self.dose = np.zeros(N)
        self.ways = [[] for _ in range(N)]; self.bopen = [[] for _ in range(N)]; self.bheld = [[] for _ in range(N)]
        self.hours = np.zeros(N)
        self.last = np.full(N, NEVER, np.int64)     # the week of the life's last land moment (the budget)
        self.fspent = np.zeros(N)                   # the moments the land brought, fading by the year (inside the budget)
        self.fq = {}                                # this week's: life -> the moment the land brings
        self.tot_m = np.zeros(N); self.tot_t = np.full(N, NEVER, np.int64)   # the drawn odds' mean over the year (seasons)
        self.kin_due = np.zeros(N, bool)            # a remembrance to come in the year after a kin's death
        self.once = [set() for _ in range(N)]       # moments the land brings once a life
        self.every = np.zeros((N, 3)); self._yr = -1   # everyday reach used this year, per stretch
        self.book = [dict() for _ in range(N)]; self.lt = np.full(N, NEVER, np.int64)
        self.kept = [[] for _ in range(N)]          # KEPT's land ring: what the life planted, saved or cleared
        self.dec = []                               # every Known land decision
        self.company = [None] * N; self.comp_s = np.full(N, -1, np.int64)
        self.news = []                              # (life, dict) for the story, drained by the engine
        self.mlog = []                              # (life, week, moment) of every land moment that came
        self.kin_t = np.full(N, NEVER, np.int64)
        self.par0 = np.zeros(N, bool); self.par_t = np.full(N, NEVER, np.int64)
        self.heat_t = np.full(nl, NEVER, np.int64)   # the town's last heat strike (heat_quarrel)
        self.qx = np.ones(N, np.float32); PP.quarrel_x = self.qx   # read by People's ties tick (a close tie's fight)
        self.dt0 = np.asarray(PP.died_t).copy()     # the cast's deaths as _watch last saw them
        self.mem = [[] for _ in range(N)]           # company kin: the shared memories (KEPT's people ring), recalled later
        self.lean = np.zeros((N, 2)); self.lean_j = np.full(N, -1, np.int64)   # notice: the land lean (tend, work)
        self.push = {}                              # notice: life -> [moment key, week due] (the pushback to come)
        self.fx_need = np.zeros((N, 5)); self.fx_mood = np.zeros(N); self.fx_stress = np.zeros(N); self.fx_res = np.zeros((N, 5))
        self.tg_money = np.zeros(N); self.tg_health = np.zeros(N)
        self.st = dict(hits=0, hit_shapes=[0] * 4, strikes=0, harvests=[0] * 3, moments=0, tone=dict(good=0, bad=0, mixed=0),
                       faces=[0] * 5, company={}, opened=0, bridges=0, decisions=0, lost=0, asks=0, ask_opened=0,
                       pushes=0, memories=0, recalls=0, norm_moves=0, heat_weeks=0)
        self.flood_back = []                        # LN6: (shape, low at one year, low at two years) of flood-hit lives
        self.FS = self.T["uses"]["faces"]
        self.WAYS = list(self.T["uses"]["ways"]["list"]); self.WK = {w_["key"]: i_ for i_, w_ in enumerate(self.WAYS)}
        self.BR = list(self.T["uses"]["ways"]["bridges"])
        # notice's asks: the tenders' ways (first led by W or G) and the builders' and farmers' (B or U), by stretch
        self.ask_ways = {(k_, j_): [i_ for i_, w_ in enumerate(self.WAYS) if w_["stretch"] == s_ and w_["lead"][0] in cs_]
                         for k_, cs_ in ((0, "WG"), (1, "BU")) for j_, s_ in enumerate(STRETCHES)}
        self._moments(L)
        self.WL = None

    # ------------------------------------------------------------------ the batch's moments
    def _moments(self, L):
        """Each moment of the batch with a land: key (the Library's earth_nature.py): its LAND row, its size, what it does
        itself (happens), its stretch (the ways its options open; a decision's from LAND_DECIDE), its company kinds."""
        S = int(L["S"]); src = L["src"]; self.notes = L["notes"]
        rows = {m_["key"]: m_ for m_ in self.T["moments"]["list"]}
        self.S = S; self.mrow = [None] * S
        self.ls = np.zeros(S, bool); self.ld = np.zeros(S, bool); self.lj = np.full(S, -1, np.int64)
        self.msize = np.zeros(S); self.mhap = [[] for _ in range(S)]; self.mwith = [[] for _ in range(S)]
        self.mtone = [""] * S; self.key_s = {}
        for si in range(S):
            k_ = str(src[si].get("land") or "").strip()
            if not k_ or k_ not in rows:
                continue
            row = rows[k_]; self.mrow[si] = k_
            dec = str(src[si].get("cast_want") or "").strip() == "decide"
            self.ld[si] = dec; self.ls[si] = not dec
            self.msize[si] = SIZES.get(str(row.get("size")), 0.1); self.mtone[si] = str(row.get("tone"))
            self.mhap[si] = [(d_, (1.0 if sg_ == "+" else -1.0) * SIZES[sz_]) for d_, sg_, sz_ in _HAPPENS.findall(str(row.get("happens", "")))]
            wv_ = src[si].get("with") or row.get("with") or []
            self.mwith[si] = [x_.strip() for x_ in (wv_.split(",") if isinstance(wv_, str) else wv_) if x_.strip()]
            js_ = [STRETCHES.index(self.WAYS[self.WK[nt["opens"]]]["stretch"]) for nt in (self.notes[si] or [])
                   if nt and nt.get("opens") in self.WK]
            if dec:
                self.lj[si] = STRETCHES.index(getattr(self.R, "LAND_DECIDE", {}).get(k_, "field"))
            elif js_:
                self.lj[si] = int(np.bincount(js_, minlength=3).argmax())
            self.key_s.setdefault(k_, []).append(si)
        self.ls_i = np.nonzero(self.ls)[0]
        gh_ = self.key_s.get("good_harvest", []); hf_ = self.key_s.get("harvest_fails", [])
        self.gate_good = np.isin(self.ls_i, gh_); self.gate_poor = np.isin(self.ls_i, hf_)
        self.bad = np.array([tn_ == "bad" for tn_ in self.mtone], bool); self.bad_ls = self.bad[self.ls_i]   # LN9

    # ------------------------------------------------------------------ the towns
    def _load(self):
        """Each town's uses pressing on each stretch (uses.load), nl x 3, a year: field from the farm share and
        density, wood from density's growth over the start, water from industry and size."""
        W = self.W
        sec = np.asarray(W.loc_sectors, float); den = np.asarray(W.loc_density, float); size = np.asarray(W.loc_size, float)
        grow = den * (np.asarray(W.loc_pop_share, float) / np.maximum(np.asarray(W.loc_pop0, float), 1e-9) - 1.0)
        return np.stack([(0.5 * sec[:, SECTORS.index("farm")] + 0.3 * den) * 0.02, 0.01 * grow / 0.1,
                         (0.4 * sec[:, SECTORS.index("industry")] + 0.2 * size / 3.0) * 0.02], 1)

    def _hx_set(self):
        """The hazards' feedback (stretches.hazards.feedback), physical state only: flood x (1 + the water's wildness lost
        since the start), fire x (1 + .5 x the wood's wildness over .6) unless a group tends the wood."""
        fl = HAZARDS.index("flood"); fi = HAZARDS.index("fire")
        self.hx[:, fl] = 1.0 + np.maximum(0.0, self.wd0[:, WA_] - self.wd[:, WA_])
        self.hx[:, fi] = np.where(self.tend[:, WO_] > 0, 1.0, 1.0 + 0.5 * np.maximum(0.0, self.wd[:, WO_] - 0.6))

    # ------------------------------------------------------------------ every week (from WorldLink.week)
    def week(self, S_):
        PP, W, E = self.PP, self.W, self.E
        t = int(PP.t); a = float(PP._age(t))
        if int(t // 52) != self._yr:
            self._yr = int(t // 52); self.every[:] = 0; self.wcut[:] = 0
        self.fspent *= np.exp(-1.0 / 52.0); self.fq = {}
        dn = np.asarray(W.disaster_now, float)
        for l in np.nonzero(dn > 0)[0]:
            self._strike(int(l), int(np.asarray(W.disaster_kind)[l]), float(dn[l]), t, a, S_)
        self._watch(t, S_)
        if self.push:
            self._pushback(t)
        if t % 4 == 0:
            self._month(t, a)
        if int(W.week_of_year) == 38 and self.dev:
            self._harvest(t, a)
        if t % 52 == 0:
            self._year(t, a)
        self._course(t, a)
        self._hx_set()

    def _here(self, l):
        return ~np.asarray(self.PP.dead, bool) & (np.asarray(self.PP.loc) == l)

    def _strike(self, l, h, sv, t, a, S_=None):
        """A hazard strikes town l (HAZARDS index h, severity sv): its stretches (hazards.hits), the households hit
        (disaster_hit: safety down very strongly, money clearly, the shape of their years after; leaving home one size
        more), the rest of the town (disaster_near: 1 in 5 cut off or out of work), heat on the old, the frail and
        those who work outdoors, the town's trust after a hit, and the moments a hit brings."""
        E = self.E; PP = self.PP; sd = E["sd"]; r = self._rng
        self.h[l] = _clip(self.h[l] - self.hits[h] * sv, 0.02, 1.0)
        self.hz_kind[l] = h; self.hz_t[l] = t; self.st["strikes"] += 1
        here = self._here(l); nm = HAZARDS[h]
        if nm in E["hit_kinds"]:
            self.trust_t[l] = t
            u = r.random(self.N); u2 = r.random(self.N); us = r.random(self.N)
            share = E["hit_share"][0] + E["hit_share"][1] * sv
            hit = here & (u < share) & (a >= 1.0)
            dis = hit & (sv > E["displaced_sev"])
            self.fx_need[hit, N_SAF] -= np.where(dis[hit], 1.5, 1.0) * sd["need"]
            self.fx_res[hit, R_MON] -= np.where(dis[hit], 0.5, 0.25) * sd["money"]
            ties = np.asarray(PP.ties, float)
            for n in np.nonzero(hit)[0]:
                lg = np.log([0.66, 0.2, 0.1, 0.04])
                lg[0] += E["shape_bonds"] * (ties[n] - 0.5)
                lg[2] += E["shape_bonds"] * (0.5 - ties[n]) + E["shape_money"] * float(dis[n])
                p_ = np.exp(lg - lg.max()); p_ /= p_.sum()
                s_ = int((p_.cumsum() <= us[n]).sum())
                s_ = min(s_, 3)
                self.hit_t[n] = t; self.shape[n] = s_; self.chron_end[n] = False; self.displaced[n] = bool(dis[n])
                self.st["hits"] += 1; self.st["hit_shapes"][s_] += 1
                if nm == "flood":
                    self.flood_back.append([int(n), s_, t])
                self.news.append((int(n), dict(kind="disaster_hit", hazard=nm, displaced=bool(dis[n]), course=SHAPES[s_])))
                self._fire(n, "flood_home" if nm == "flood" else "storm_damage" if nm == "storm" else None, t)
            near = here & ~hit & (u2 < E["disrupted"])
            self.fx_need[near, N_SAF] -= 0.25 * sd["need"]
            for n in np.nonzero(here & ~hit)[0]:
                self._fire(n, "neighbours_dig_out", t, p=E["force"].get("neighbours_dig_out", 0.0))
                if nm == "fire":
                    self._fire(n, "smoke_days", t, p=E["force"].get("smoke_days", 0.0))
        if nm == "heat":   # heat_summer: many lose a little vitality; the old, the frail and outdoor work lose health
            self.heat_t[l] = t   # and quarrels a little more likely for a spell (heat_quarrel, in _course)
            hea = np.asarray(PP.res, float)[:, R_HEA] if np.ndim(PP.res) == 2 else np.full(self.N, 0.6)
            weak = here & ((a >= E["heat_old"]) | (hea < E["heat_frail"]) | (np.asarray(PP.psector) == SECTORS.index("farm")))
            self.fx_mood[here] -= 0.5 * 0.1 * sd["mood"]; self.fx_res[here, R_HEA] -= 0.5 * 0.1 * sd["health"]
            self.fx_res[weak, R_HEA] -= 0.25 * sd["health"]
            for n in np.nonzero(here)[0]:
                self._fire(n, "heatwave", t, p=E["force"].get("heatwave", 0.0))
                if self.h[l, F_] < 0.5 or self.h[l, WA_] < 0.5:
                    self._fire(n, "drought", t, p=E["force"].get("drought", 0.0))
                    self._fire(n, "dry_well", t, p=E["force"].get("dry_well", 0.0))

    def _course(self, t, a):
        """Weekly: the hit lives' years after (after_disaster's four shapes), the town's trust after a hit, and the
        lasting reads (the dose, sick land, worry), as the safety need's supply and stress."""
        E = self.E; sd = E["sd"]; dead = np.asarray(self.PP.dead, bool)
        on = (self.hit_t > NEVER // 2) & ~dead
        lev = np.zeros(self.N)
        if on.any():
            dt = (t - self.hit_t).astype(float)
            for s_, nm in enumerate(SHAPES):
                m = on & (self.shape == s_)
                if not m.any():
                    continue
                full, fade = E["course"][nm]
                if nm == "chronic":
                    ok = m & (dt >= full) & ~self.chron_end
                    if ok.any():
                        x_ = self._rng.random(int(ok.sum()))
                        end_p = E["chronic_end"] * np.where(np.asarray(self.PP.ties, float)[ok] >= 0.5, 3.0, 1.0)
                        ix_ = np.nonzero(ok)[0][x_ < end_p]
                        self.chron_end[ix_] = True
                    lev[m] = np.where(self.chron_end[m], 0.0, 1.0)
                elif nm == "delayed":
                    dw, dl = E["delayed_dip"]
                    d_ = dt[m]
                    lev[m] = np.where(d_ < dw, dl, np.where(d_ < full, 0.0, np.where(d_ < 2 * full,
                                      1.0, _clip(1 - (d_ - 2 * full) / max(fade, 1), 0, 1))))
                else:
                    d_ = dt[m]
                    lev[m] = np.where(d_ < full, 1.0, _clip(1 - (d_ - full) / max(fade, 1), 0, 1))
            self.fx_need[:, N_SAF] -= 0.006 * E["course_safety"] * lev
            self.fx_stress += E["course_stress"] * lev
        self.low = lev
        hq_, hw_ = E["heat_quarrel"]   # heat_summer: quarrels x 1.1 while the heat's spell lasts in the town
        hot = (t - self.heat_t[np.asarray(self.PP.loc)]) < hw_
        self.qx[:] = np.where(hot & ~dead, np.float32(hq_), np.float32(1.0)); self.st["heat_weeks"] += int(hot.sum())
        for x_ in self.flood_back:   # LN6: still low at one year, at two years
            if len(x_) == 3 and t - x_[2] >= 52:
                x_.append(bool(lev[x_[0]] > 0.1))
            elif len(x_) == 4 and t - x_[2] >= 104:
                x_.append(bool(lev[x_[0]] > 0.1))
        dtr = t - self.trust_t
        tl = np.where(dtr < E["trust_weeks"], 1.0, 0.5 ** ((dtr - E["trust_weeks"]) / 13.0)) * (self.trust_t > NEVER // 2)
        self.trust_lv = tl
        self.fx_need[:, N_BEL] += 0.006 * E["trust_belong"] * tl[np.asarray(self.PP.loc)] * ~dead
        if self.dev:
            self.fx_mood += 0.1 * 0.057 * sd["mood"] * self.dose * ~dead
            self.tg_health = 0.128 * sd["health"] * self.dose * ~dead
            sick = self.lost & ~dead
            if sick.any():
                k_ = np.where(self.hy[np.arange(self.N), np.maximum(self.lost_j, 0)] >= E["haunt_years"], 2.5, 1.0)
                self.fx_need[sick, N_MEA] -= 0.006 * 0.1 * k_[sick]
            wy = (self.worry == 1) & ~dead & (E["worry_ages"][0] <= a <= E["worry_ages"][1])
            self.fx_need[wy, N_MEA] -= 0.006 * 0.1

    def _month(self, t, a):
        """Monthly: the minutes a week each life spends on the land (dose: walks by the town's nature access, the
        nature haunts' hours, the land ways' hours), and the dose it gives (by the stretch's health)."""
        if not self.dev:
            return
        PP, W, E = self.PP, self.W, self.E
        loc = np.asarray(PP.loc)
        hstr = self.h[loc]                                                   # N x 3
        walk = E["walk_min"] * np.asarray(W.loc_nature, float)[loc] * self.walk * (a >= 4)
        hh = np.zeros(self.N); nat = np.zeros(self.N); nh_ = np.ones(self.N)
        hp = getattr(W, "hp_s", None); hnt = getattr(PP, "hnt", None)
        if hp is not None and hnt is not None:
            try:
                hh, _ = PP._haunt_hours(a)
            except Exception:   # a People without the hours table: no haunt hours
                hh = np.zeros(self.N)
            P_ = hp.shape[2]; kd = (np.maximum(hnt, 0) // P_) % len(HAUNT_KINDS)
            ok = hnt >= 0; nh_ = np.maximum(ok.sum(1), 1)
            isn = np.isin(kd, [HAUNT_KINDS.index(k_) for k_ in E["nature_haunts"]]) & ok
            nat = isn.sum(1)
            self._hk = np.where(isn, np.where(kd == HAUNT_KINDS.index("prod.land"), F_, WO_), -1)
        hours = np.asarray(hh, float) * nat / nh_ + (self.hours if self.play else 0.0)
        self.mins = walk + 60.0 * hours
        sh = (walk * hstr.mean(1) + 60.0 * hours * np.where(nat > 0, hstr[:, WO_], hstr.mean(1))) / np.maximum(self.mins, 1e-9)
        self.dose = np.interp(sh, [0.15, 0.3, 0.6], [0.0, 0.5, 1.0]) * (self.mins >= self.T["dose"]["threshold_min_week"])

    def _harvest(self, t, a):
        """The year's harvest in each town (for_all_lives harvest: good .2, normal .6, poor .2; a field under .4 health
        moves .1 from good to poor): farm households gain a little or lose clearly, and a poor year raises the town's
        food prices a little for everyone there."""
        PP, E = self.PP, self.E; sd = E["sd"]; od = self.T["for_all_lives"][0]["odds"]
        u = self._rng.random(self.nl)
        sick = self.h[:, F_] < 0.4
        pg = od["good"] - 0.1 * sick   # (and poor, the rest, + .1)
        self.harvest = np.where(u < pg, 0, np.where(u < pg + od["normal"], 1, 2)); self.harvest_t[:] = t
        for k_ in range(3):
            self.st["harvests"][k_] += int((self.harvest == k_).sum())
        self._harvest_fx(np.arange(self.nl), np.ones(self.nl, np.int64))

    def _harvest_fx(self, ls, old):
        sd = self.E["sd"]; PP = self.PP
        loc = np.asarray(PP.loc); dead = np.asarray(PP.dead, bool)
        farm = (np.asarray(PP.psector) == SECTORS.index("farm")) & ~dead
        val = np.array([0.1, 0.0, -0.25]); food = np.array([0.0, 0.0, -0.05])
        for l in ls:
            here = (loc == l) & ~dead; d_ = self.harvest[l]; o_ = old[l] if np.ndim(old) else old
            self.fx_res[here & farm, R_MON] += (val[d_] - val[o_]) * sd["money"]
            self.fx_res[here, R_MON] += (food[d_] - food[o_]) * sd["money"]

    def _year(self, t, a):
        """Yearly: the home health's drift (dev: the uses' load against the start's, the times' warming on field and
        water), each stretch's recovery toward its home at its own rate, a group's tending, the attachment at 12 and
        the haunts' years, a loved stretch lost (N3), worry, the ways' clocks and the bridges, the moments the year's
        state brings."""
        PP, W, E = self.PP, self.W, self.E
        if self.dev:
            ld = self._load() - self.load0
            self.home = _clip(self.home - ld, 0.05, 1.0)
            dx = max(0.0, float(np.mean(np.asarray(W.extremes, float))) - self.ext0)
            self.home[:, [F_, WA_]] = _clip(self.home[:, [F_, WA_]] - 0.002 * dx, 0.05, 1.0)
        h_old = self.h.copy()
        self.h = _clip(self.h + self.tend + self.rec[None] * (self.home - self.h), 0.02, 1.0)
        self.wd = _clip(self.wd + self.rec[None] * (self.whome - self.wd), 0.0, 1.0)
        loc = np.asarray(PP.loc); dead = np.asarray(PP.dead, bool)
        if E["attach_age"] <= a < E["attach_age"] + 1:
            nn = (self.att < 0) & ~dead
            self.att[nn] = loc[nn]; self.att_h[nn] = self.h[loc[nn]]; self.att_w[nn] = self.wd[loc[nn]]
        hk = getattr(self, "_hk", None)
        if hk is not None:
            for j in (F_, WO_):
                self.hy[:, j] += (hk == j).any(1)
        for n in range(self.N):
            for w_ in self.ways[n]:
                self.hy[n, STRETCHES.index(self.WAYS[w_["i"]]["stretch"])] += 1.0 / max(len(self.ways[n]), 1)
        # N3's "a loved stretch lost": the stretches of the town they grew up in (at 12) lost .2 of health or
        # wildness since, or a stretch they hold a way on lost .2 since they took it up
        ok = self.att >= 0
        lost = np.zeros(self.N, bool); lj = np.full(self.N, -1, np.int64)
        if ok.any():
            dh = self.att_h[ok] - self.h[self.att[ok]]; dw = self.att_w[ok] - self.wd[self.att[ok]]
            dd = np.maximum(dh, dw); m_ = dd.max(1) >= E["lost"]
            lost[ok] = m_; lj[ok] = np.where(m_, dd.argmax(1), -1)
        for n in range(self.N):
            for w_ in self.ways[n]:
                j = STRETCHES.index(self.WAYS[w_["i"]]["stretch"]); l = int(w_["l"])
                if max(w_["h0"] - self.h[l, j], w_["w0"] - self.wd[l, j]) >= E["lost"]:
                    lost[n] = True; lj[n] = j
        new_ = lost & ~self.lost & ~dead
        self.st["lost"] += int(new_.sum())
        for n in np.nonzero(new_)[0]:
            self.news.append((int(n), dict(kind="stretch_lost", stretch=STRETCHES[int(lj[n])])))
        self.lost = lost & ~dead; self.lost_j = lj
        if self.dev:
            lo_, hi_ = E["worry_ages"]
            rising = float(np.mean(np.asarray(W.extremes, float))) - self.ext0 >= E["worry_rise"]
            if lo_ <= a <= hi_ and rising:
                nd = (self.worry < 0) & ~dead
                self.worry[nd] = (self._rng.random(int(nd.sum())) < E["worry_share"]).astype(np.int64)
                for n in np.nonzero((self.worry == 1) & ~dead)[0]:
                    self._fire(n, "climate_worry", t, p=E["force"].get("climate_worry", 0.0))
        if self.play:
            self._ways_year(t, a)
            self._asks(t, a)
        # the moments the year's state brings: the river back, the tree grown, the river sick, the wood cleared
        for n in np.nonzero(~dead)[0]:
            l = int(loc[n])
            if self.att[n] >= 0 and l == self.att[n] and (self.h[l] - self.att_h[n]).max() >= 0.15:
                self._fire(n, "river_clean_again", t, once=True)
            if any(k_["kind"] in ("planted", "saved") and t - k_["t"] >= 15 * 52 and self._stands(k_) for k_ in self.kept[n]):
                self._fire(n, "planted_tree_grown", t, once=True)
            if health_word(h_old[l, WA_]) != health_word(self.h[l, WA_]) and self.h[l, WA_] < h_old[l, WA_]:
                self._fire(n, "sick_river", t, p=E["force"].get("sick_river", 0.0))
            if self.wcut[l] >= 0.15:
                self._fire(n, "wood_cleared", t, p=E["force"].get("wood_cleared", 0.0))
            if t - self.wplan[l] < 52:
                self._fire(n, "protest_at_the_wood", t, p=E["force"].get("protest_at_the_wood", 0.0))
            if self.ways[n]:
                self._fire(n, "outdoor_injury", t, p=E["force"].get("outdoor_injury", 0.0))
        # a group's tending (uses.tend): each life holding a tending way (led by W or G) stands for its group of ten
        self.tend[:] = 0
        for n in np.nonzero(~dead)[0]:
            for w_ in self.ways[n]:
                wy_ = self.WAYS[w_["i"]]
                if "W" in wy_["lead"] or "G" in wy_["lead"]:
                    self.tend[int(loc[n]), STRETCHES.index(wy_["stretch"])] += E["tend_per10"]
        self.tend = np.minimum(self.tend, E["tend_cap"])

    def _stands(self, k_):
        """Whether what a life planted, saved or cleared still stands: the stretch still holds half its change."""
        cur = self.wd[k_["l"], k_["j"]] if k_["what"] == "wild" else self.h[k_["l"], k_["j"]]
        return (cur - k_["base"]) * np.sign(k_["d"]) >= 0.5 * abs(k_["d"])

    def _watch(self, t, S_):
        """The cast's turns the land's together moments wait for: a new partner (a first date outdoors), a kin who
        died (a remembrance tree; a kin the life shares a memory of on the land is recalled: company.kinds kin)."""
        if not self.play:
            return
        PP = self.PP; E = self.E
        dt = np.asarray(PP.died_t)   # kin who died since the last look (at any point of the week)
        dk = (dt != self.dt0) & (dt > NEVER // 2) & ((PP.rmask & KIN_BITS) != 0)
        self.dt0 = dt.copy()
        for n in np.nonzero(dk.any(1) & ~np.asarray(PP.dead, bool))[0]:
            self.kin_t[n] = t   # whether the remembrance comes in the year after: decided once, at the death
            self.kin_due[n] = self._rng.random() < float(E["force"].get("remembrance_tree", 0.0))
            gone = set(PP.uid[n, dk[n]].tolist())
            mm = [m_ for m_ in self.mem[n] if m_["cid"] in gone and not m_.get("recalled")]
            if mm:
                for m_ in mm:
                    m_["recalled"] = t
                self.st["recalls"] += 1; self._dim(n, "meaning", 0.1)
                self.news.append((int(n), dict(kind="memory_recalled", cid=int(mm[0]["cid"]), moment=mm[0]["moment"],
                                               age=mm[0]["age"])))
                if self._fire(n, "remembrance_tree", t, p=E["memory_recall"]):
                    self.kin_due[n] = False
        held = S_.get("held") if isinstance(S_, dict) else None
        if held is not None:
            par = np.asarray(held, bool)[:, self.par_i]
            self.par_t[par & ~self.par0] = t; self.par0 = par.copy()
        if t % 13 == 0:
            for n in np.nonzero(~np.asarray(PP.dead, bool))[0]:
                if self.kin_due[n] and t - self.kin_t[n] < 52 and self._fire(n, "remembrance_tree", t):
                    self.kin_due[n] = False
                if t - self.par_t[n] < 26:
                    self._fire(n, "first_date_outdoors", t, p=self.E["force"].get("first_date_outdoors", 0.0))

    # ------------------------------------------------------------------ the moments (wa_land_play)
    def _fire(self, n, key, t, p=1.0, once=False):
        """Bring the land's moment key to life n this week (WorldLink.fire_now), at chance p, inside the budget (never
        two land moments in a quarter) and not over another moment the world brings; once: once a life."""
        if key is None or not self.play or self.WL is None:
            return False
        ss = self.key_s.get(key)
        if not ss or n in self.WL.pending or t - self.last[n] < self.E["gap_weeks"]:
            return False
        if once and key in self.once[n]:
            return False
        if p < 1.0 and self._rng.random() >= p:
            return False
        si = ss[0] if len(ss) == 1 else ss[int(self._rng.integers(len(ss)))]
        if self.bad[si] and float(self.PP._age(t)) < self.E["bad_age"]:   # LN9: not told to the young (drawn as before)
            return False
        if once:
            self.once[n].add(key)
        self.WL.fire_now[n, si] = True; self.fq[int(n)] = int(si)
        return True

    def ev_scale(self, ev):
        """The drawn land moments' weekly odds (ev: N x the land moments), held to the budget: about per_year a year in
        all with the moments the land brings itself (fspent: those of about the last year), none inside gap_weeks of the
        last nor in a week the land brings one; a good harvest's moment only in a good year, a failed one's in a poor,
        each there at 1 / its year's odds (harvest odds), so it keeps its written share over the years.
        The budget reads the odds' mean over the year (tot_m), not the week's, so a season's moments get their whole
        share in their season (a week's at most season_x x the mean)."""
        loc = np.asarray(self.PP.loc); t = int(self.PP.t); E = self.E
        hv = self.harvest[loc]; fresh = (t - self.harvest_t[loc]) < 52
        od = self.T["for_all_lives"][0]["odds"]   # in its year at 1 / the year's odds: over the years, its written rate
        ev = ev * np.where(self.gate_good[None], ((hv == 0) & fresh)[:, None] / od["good"], 1.0)
        ev = ev * np.where(self.gate_poor[None], ((hv == 2) & fresh)[:, None] / od["poor"], 1.0)
        tot = ev.sum(1)
        new_ = self.tot_t < NEVER // 2
        a_ = np.where(new_, 1.0, 1.0 - np.exp(-np.maximum(t - self.tot_t, 0) / 52.0))
        self.tot_m += a_ * (tot - self.tot_m); self.tot_t[:] = t
        tm_ = np.maximum(self.tot_m, tot / float(E["season_x"]))
        b_ = np.maximum(float(E["per_year"]) - self.fspent, 0.0) / 52.0
        k = np.minimum(1.0, b_ / np.maximum(tm_, 1e-12)) * ((t - self.last) >= E["gap_weeks"])
        if self.fq:
            k[list(self.fq)] = 0.0
        ev = ev * k[:, None]
        if float(self.PP._age(t)) < E["bad_age"]:   # LN9: no bad land moment drawn for the young (the others' odds as before)
            ev[:, self.bad_ls] = 0.0
        return ev

    def seen(self, ns, ss):
        """The land moments that came this week (the budget's clock)."""
        t = int(self.PP.t)
        for n, si in zip(np.asarray(ns).tolist(), np.asarray(ss).tolist()):
            if 0 <= si < self.S and (self.ls[si] or self.ld[si]):
                self.last[n] = t; self.st["moments"] += 1; self.mlog.append((int(n), t, int(si)))
                if self.fq.get(int(n)) == int(si):   # the land brought it: inside the budget
                    self.fspent[n] += 1.0
                tn_ = self.mtone[si]
                if tn_ in self.st["tone"]:
                    self.st["tone"][tn_] += 1

    def company_draw(self, n, si, a):
        """Who is there in a together moment (company.kinds), drawn from the real cast by closeness, or alone (about .3
        for adults): None when the moment names no company. Colour never picks the company."""
        ks = self.mwith[si] if 0 <= si < self.S else []
        if not ks:
            self.company[n] = None; self.comp_s[n] = si; return None
        PP = self.PP; r = self._rng; E = self.E
        live = PP.used[n] & PP.lv[n]; c = np.asarray(PP.c[n], float); rm = np.asarray(PP.rmask[n])
        w = {}; who = {}
        for k_ in ks:
            if k_ == "alone":
                continue
            if k_ in COMPANY_BITS:
                m_ = live & ((rm & COMPANY_BITS[k_]) != 0) & (c > 0)
                if m_.any():
                    w[k_] = float(c[m_].sum()); who[k_] = np.nonzero(m_)[0]
            elif k_ in ("stranger", "witness"):
                w[k_] = 0.3
        al_ = E["alone"][0] if a >= 18 else E["alone"][1]
        tot = sum(w.values())
        if "alone" in ks and (tot <= 0 or r.random() < al_):
            pick = "alone"
        elif tot > 0:
            kk = list(w); p_ = np.array([w[k_] for k_ in kk]) / tot
            pick = kk[min(int((p_.cumsum() <= r.random()).sum()), len(kk) - 1)]
        else:
            pick = ks[0] if ks[0] in ("alone", "stranger", "witness") else None
        if pick is None:
            self.company[n] = None; self.comp_s[n] = si; return None
        cid = -1
        if pick in who:
            ix = who[pick]; p_ = c[ix] / c[ix].sum()
            k_ = int(ix[min(int((p_.cumsum() <= r.random()).sum()), len(ix) - 1)])
            cid = int(PP.uid[n, k_])
        self.company[n] = dict(kind=pick, cid=cid); self.comp_s[n] = si
        self.st["company"][pick] = self.st["company"].get(pick, 0) + 1
        return self.company[n]

    def _dim(self, n, dim, x, j=-1, l=-1):
        """One of the land's dimensions moved by x standard deviations of its felt state (land: x as a stretch's)."""
        sd = self.E["sd"]
        if dim in ("safety", "belonging", "meaning"):
            self.fx_need[n, {"safety": N_SAF, "belonging": N_BEL, "meaning": N_MEA}[dim]] += x * sd["need"]
        elif dim == "wellbeing":
            self.fx_mood[n] += x * sd["mood"]
        elif dim == "stress":
            self.fx_stress[n] += x * sd["stress"]
        elif dim == "health":
            self.fx_res[n, R_HEA] += x * sd["health"]
        elif dim == "vitality":
            self.fx_res[n, R_HEA] += 0.5 * x * sd["health"]; self.fx_mood[n] += 0.5 * x * sd["mood"]
        elif dim == "money":
            self.fx_res[n, R_MON] += x * sd["money"]
        elif dim == "yield":
            self.fx_res[n, R_MON] += 0.5 * x * sd["money"]
        elif dim == "town trust":
            self.fx_need[n, N_BEL] += 0.5 * x * sd["need"]
        elif dim in ("land health", "land_health", "land wildness", "land_wild") and l >= 0 and j >= 0:
            self._everyday(n, l, j, "wild" if "wild" in dim else "health", np.sign(x))

    def _everyday(self, n, l, j, what, sg):
        """reach.everyday: a life's own use moves a stretch by at most .002 a year (everyday_step a use)."""
        E = self.E
        room = E["everyday"] - self.every[n, j]
        d = min(E["everyday_step"], max(room, 0.0)) * float(sg)
        if d == 0:
            return
        self.every[n, j] += abs(d)
        if what == "wild":
            self.wd[l, j] = float(_clip(self.wd[l, j] + d)); self.whome[l, j] = float(_clip(self.whome[l, j] + 0.5 * d))
        else:
            self.h[l, j] = float(_clip(self.h[l, j] + d, 0.02, 1.0))
        self._unit(n, "land_wild" if what == "wild" else "land_health", l, j, abs(d))

    def on_act(self, ns, s, a, succ, idle, age, t):
        """The land moments answered this week: what the moment did (happens), the chosen option's face x the moment's
        size, the company's part, and the way the option opens."""
        PP = self.PP; E = self.E
        for n in np.asarray(ns).tolist():
            si = int(s[n])
            if not (0 <= si < self.S and self.ls[si]):
                continue
            l = int(PP.loc[n]); j = int(self.lj[si]) if self.lj[si] >= 0 else WO_
            for d_, x_ in self.mhap[si]:
                self._dim(n, d_, x_, j, l)
            if bool(idle[n]):
                continue
            nts = self.notes[si] or []
            nt = (nts[int(a[n])] if 0 <= int(a[n]) < len(nts) else None) or {}
            fc = str(nt.get("land") or "")
            if fc in self.FS:
                self.st["faces"]["WUBRG".index(fc)] += 1
                f_ = self.FS[fc]; sz = self.msize[si] * (1.0 if succ[n] else 0.5)
                for d_, v_ in f_["gains"].items():
                    self._dim(n, d_, v_ * sz, j, l)
                for d_, v_ in f_["costs"].items():
                    self._dim(n, d_, -v_ * sz, j, l)
                self._notice(n, fc, j, t)
            cm = self.company[n] if self.comp_s[n] == si else self.company_draw(n, si, age)
            if cm is not None:
                self._company_fx(n, cm, fc, t, si, age)
            op = nt.get("opens")
            if op in self.WK:
                self.open_way(n, op, age, t)
        self.company[:] = [None] * self.N; self.comp_s[:] = -1

    def pick(self, s, age):
        """The company of each life whose moment this week is a together moment (S["company"] at the situation
        pause); a life whose moment changes after the pause is drawn again when it is answered."""
        s = np.asarray(s)
        m = np.isin(s, self.ls_i)
        for n in range(self.N):
            if m[n]:
                if self.comp_s[n] != s[n]:
                    self.company_draw(n, int(s[n]), age)
            elif self.company[n] is not None:
                self.company[n] = None; self.comp_s[n] = -1
        return self.company

    def _company_fx(self, n, cm, face, t, si=-1, age=0.0):
        """company.kinds: alone restores (wellbeing, meaning); a friend a little closer and belonging; a partner clearly
        closer; kin belonging clearly, and the shared memory kept (KEPT's people ring, recalled when they die); a group
        belonging and town trust, its norm a little toward the chosen face; a stranger 1 in 4 a new acquaintance; a
        witness meaning; a rival's tie moves by the chosen face (a truce draws closer, a stand pushes further)."""
        PP = self.PP; E = self.E; k_ = cm["kind"]
        slot = PP._slot(n, cm["cid"]) if cm["cid"] >= 0 else -1
        def closer(x):
            if slot >= 0:
                PP.c[n, slot] = float(_clip(PP.c[n, slot] + x))
        if k_ == "alone":
            self._dim(n, "wellbeing", 0.1); self._dim(n, "meaning", 0.1)
        elif k_ == "friend":
            self._dim(n, "belonging", 0.1); closer(E["tie_small"])
        elif k_ == "partner":
            closer(E["tie_clear"])
        elif k_ == "kin":
            self._dim(n, "belonging", 0.25); closer(E["tie_small"])
            if cm["cid"] >= 0:
                self.mem[n].append(dict(cid=int(cm["cid"]), moment=self.mrow[si] if 0 <= si < self.S else None,
                                        age=round(float(age), 2), t=int(t)))
                self.st["memories"] += 1
        elif k_ == "group":
            self._dim(n, "belonging", 0.1); self._dim(n, "town trust", 0.1); closer(E["tie_small"])
            if face in self.FS:
                self._group_norm(n, face, t)
        elif k_ == "witness":
            self._dim(n, "meaning", 0.1)
        elif k_ == "stranger" and self._rng.random() < E["stranger_tie"]:
            F = PP._gen(np.array([n]), np.array([int(PP.t) - int(52 * max(5.0, PP._age(PP.t)))]), int(PP.t))
            PP._add(F, int(PP.t), R["acquaintance"], c0=0.06, trust0=0.45, quiet=True)
        elif k_ == "rival":
            closer(E["tie_small"] if face in ("W", "G") else -E["tie_small"] if face in ("B", "R") else 0.0)

    def _group_norm(self, n, face, t):
        """company group: the group's norm (People.snorm, the life's setting) a little toward the chosen face's colour,
        as an act's voice moves it (x (1 - cohesion / 2)), in the ledger's group_norm with world answers' ledger on. The
        setting: a club, the neighbours, a congregation or a movement the life is in, else its first other setting."""
        PP = self.PP; sk = np.asarray(PP.skind[n])
        js = [j_ for g_ in ("club", "neighbours", "congregation", "movement") for j_ in np.nonzero(sk == G[g_])[0]]
        if not js:
            js = list(np.nonzero((sk >= 0) & (sk != G["household"]) & (sk != G["work"]))[0])
        if not js:
            return
        j = int(js[0]); C_ = PP.snorm.shape[-1]
        tg = np.zeros(C_, np.float32); tg["WUBRG".index(face)] = 1.0
        s0 = PP.snorm[n, j].astype(float)
        k = np.float32(self.E["group_norm"] * (1.0 - float(PP.scoh[n, j]) / 2.0))
        nw = PP.snorm[n, j] + k * (tg - PP.snorm[n, j]); PP.snorm[n, j] = nw / nw.sum()
        self.st["norm_moves"] += 1
        if getattr(PP, "wa_l", False):
            PP._wa_gmove(n, j, t, dnorm=PP.snorm[n, j] - s0, what="the land")

    # ------------------------------------------------------------------ notice (people 2.0, as world_answers)
    def _notice(self, n, face, j, t):
        """A land choice noticed: the life's lean (tend: W, G; work: B, U) grows, and those it costs push back at
        push_p (the tenders when the face costs the land's health or wildness, the farmers and builders when it costs
        yield or money): their moment comes push_weeks later, its options the lean in or the backlash."""
        NT = self.E["notice"]; r = self._rng
        if face in "WG":
            self.lean[n, 0] += 1.0
        elif face in "BU":
            self.lean[n, 1] += 1.0
        self.lean_j[n] = j
        cs = self.FS[face]["costs"]
        who = [x_ for x_, ks_ in (("tend", ("land_health", "land_wild")), ("work", ("yield", "money")))
               if any(k_ in cs for k_ in ks_)]
        if not who or n in self.push or r.random() >= NT["push_p"]:
            return
        w_ = who[int(r.integers(len(who)))]
        key = NT["push_tend"][STRETCHES[j]] if w_ == "tend" else NT["push_work"]
        self.push[n] = [key, int(t) + int(r.integers(NT["push_weeks"][0], NT["push_weeks"][1] + 1)), w_]

    def _pushback(self, t):
        for n in list(self.push):
            key, due, w_ = self.push[n]
            if t < due:
                continue
            if bool(self.PP.dead[n]) or t - due > 26 or self._fire(n, key, t):
                if t - due <= 26 and not bool(self.PP.dead[n]):
                    self.st["pushes"] += 1
                    self.news.append((int(n), dict(kind="land_pushback", by="tenders" if w_ == "tend" else "farmers and builders",
                                                   moment=key)))
                del self.push[n]

    def _asks(self, t, a):
        """Yearly: the stretch's tenders (a tend lean) or its builders and farmers (a work lean) ask the life in, at ask_y x
        (1 + people x the lean's strength): one of their ways on the stretch the life last chose on, taken up when it
        holds room. The lean then fades by lean_decay."""
        NT = self.E["notice"]; r = self._rng; pe = float(self.T["notice"]["people"]); dead = np.asarray(self.PP.dead, bool)
        if a >= NT["ask_age"]:
            for n in np.nonzero(~dead & (self.lean.max(1) >= 1.0))[0]:
                s_ = min(1.0, float(self.lean[n].max()) / NT["lean_full"])
                if r.random() >= NT["ask_y"] * (1.0 + pe * s_):
                    continue
                k_ = int(self.lean[n].argmax()) if self.lean[n, 0] != self.lean[n, 1] else int(r.integers(2))
                j = int(self.lean_j[n]) if self.lean_j[n] >= 0 else int(r.integers(3))
                held = {w_["i"] for w_ in self.ways[n]}
                cand = [i_ for i_ in self.ask_ways[(k_, j)] if i_ not in held]
                if not cand:
                    continue
                i_ = cand[int(r.integers(len(cand)))]
                ok = self.open_way(n, self.WAYS[i_]["key"], a, t)
                self.st["asks"] += 1; self.st["ask_opened"] += int(ok)
                self.news.append((int(n), dict(kind="land_ask", by="tenders" if k_ == 0 else "farmers and builders",
                                               way=self.WAYS[i_]["key"], taken=bool(ok))))
        self.lean *= NT["lean_decay"]

    # ------------------------------------------------------------------ the ways and the bridges
    def open_way(self, n, key, age, t):
        """A way opened (an option's opens:): taken up from way_age[0] (a helper beside an adult), when the life holds
        fewer than three and not this one."""
        i = self.WK[key]
        if age < self.E["way_age"][0] or len(self.ways[n]) >= self.E["max_ways"] or any(w_["i"] == i for w_ in self.ways[n]):
            return False
        l = int(self.PP.loc[n]); j = STRETCHES.index(self.WAYS[i]["stretch"])
        self.ways[n].append(dict(i=i, key=key, step=0, since=float(age), worked=0.0, need=self._step_years(i, 1),
                                 l=l, h0=float(self.h[l, j]), w0=float(self.wd[l, j])))
        self.st["opened"] += 1
        self.news.append((int(n), dict(kind="way_opened", way=key)))
        self._bridges(n, t)
        self._hours(n)
        return True

    def _step_years(self, i, k):
        """The years from step k - 1 to step k of way i's ladder (ladder_years' [median, low, high], a triangular draw;
        step 0, its first rung, comes with taking the way up)."""
        ly = self.WAYS[i].get("ladder_years") or [LADDER_YEARS_DEFAULT] * 3
        md, lo, hi = (float(x_) for x_ in ly[min(k, len(ly) - 1)])
        lo = min(lo, md); hi = max(hi, md)
        return float(self._rng.triangular(lo, md, hi)) if hi > lo else md

    def _hours(self, n):
        self.hours[n] = float(sum(float(self.WAYS[w_["i"]]["hours"]) for w_ in self.ways[n]))

    def _ways_year(self, t, a):
        """Yearly: each held way's year worked (a step when its clock is done), its effect (.6 of its first colour's
        face and .4 of its second's, from LAND's effect, x way_k), its stretch at everyday reach, and the bridges."""
        PP = self.PP; E = self.E; dead = np.asarray(PP.dead, bool)
        for n in range(self.N):
            if dead[n] or not self.ways[n]:
                continue
            l = int(PP.loc[n])
            for w_ in self.ways[n]:
                wy = self.WAYS[w_["i"]]; j = STRETCHES.index(wy["stretch"])
                w_["worked"] += 1.0; w_["in_step"] = w_.get("in_step", 0.0) + 1.0
                if w_["step"] < 2 and w_["in_step"] >= w_["need"] and a >= E["way_age"][1]:   # steps 1, 2: an adult's
                    w_["step"] += 1; w_["since"] = float(a); w_["in_step"] = 0.0
                    w_["need"] = self._step_years(w_["i"], w_["step"] + 1) if w_["step"] < 2 else 0.0
                    self.news.append((int(n), dict(kind="way_step", way=wy["key"], step=int(w_["step"]),
                                                   title=(wy.get("ladder_titles") or [None] * 3)[w_["step"]])))
                for d_, v_ in wy.get("effect", {}).items():
                    self._dim(n, d_, E["way_k"] * float(v_), j, l if l == w_["l"] else -1)
            self._bridges(n, t)

    def _bridges(self, n, t):
        held = {w_["key"] for w_ in self.ways[n]}
        now = [b_ for b_ in range(len(self.BR)) if self.BR[b_]["a"] in held and self.BR[b_]["b"] in held]
        for b_ in now:
            if b_ not in self.bopen[n]:
                self.bopen[n].append(b_); self.st["bridges"] += 1
                self.news.append((int(n), dict(kind="bridge_open", opens=self.BR[b_]["opens"])))
        self.bheld[n] = now

    # ------------------------------------------------------------------ a Known life's land decision (phase 2)
    def decide(self, n, si, ai, succ, idle, reach, op, tm, t):
        """A world answers decision whose moment is the land's (save the wood, drain the marsh, ...): the chosen face
        moves the moment's stretch by reach.known's size x k_land per unit of standing (x the decision's quality, the
        crisis' opening and the team, as phase 2's town effect); wildness so moved is the stretch's new home (a
        drained marsh stays drained until someone re-floods it), health recovers at the stretch's own rate."""
        if not (0 <= si < self.S and self.ld[si]) or idle:
            return None
        nt = (self.notes[si] or [])
        nt = (nt[ai] if 0 <= ai < len(nt) else None) or {}
        fc = str(nt.get("land") or "")
        if fc not in self.FS:
            return None
        K = self.T["reach"]; kn = K["known"]
        sz = kn["strong"] if self.msize[si] >= 0.5 else kn["clear"] if self.msize[si] >= 0.25 else kn["small"]
        d = sz * float(K["k_land"]) * float(reach) * (0.8 if succ else 0.4) * float(op) * float(tm)
        l = int(self.PP.loc[n]); j = int(self.lj[si]); f_ = self.FS[fc]
        dh = d * (f_["gains"].get("land_health", 0.0) - f_["costs"].get("land_health", 0.0)) / 0.2
        dw = d * (f_["gains"].get("land_wild", 0.0) - f_["costs"].get("land_wild", 0.0)) / 0.2
        hb, wb = float(self.h[l, j]), float(self.wd[l, j])
        self.h[l, j] = float(_clip(hb + dh, 0.02, 1.0))
        self.wd[l, j] = float(_clip(wb + dw)); self.whome[l, j] = float(_clip(self.whome[l, j] + dw))
        if j == WO_ and dw < 0:
            self.wcut[l] += -dw; self.wplan[l] = t
        for what, dv, base in (("health", self.h[l, j] - hb, hb), ("wild", self.wd[l, j] - wb, wb)):
            if abs(dv) > 1e-9:
                self._unit(n, "land_saved" if dv > 0 else "land_lost", l, j, abs(dv))
                self.kept[n].append(dict(kind="planted" if dv > 0 and self.mrow[si] == "plant_trees" else
                                         "saved" if dv > 0 else "cleared", what=what, l=l, j=j, d=float(dv), base=base, t=int(t),
                                         moment=self.mrow[si]))
        ev = dict(land=self.mrow[si], stretch=STRETCHES[j], face=fc, health=round(float(self.h[l, j] - hb), 4),
                  wild=round(float(self.wd[l, j] - wb), 4))
        self.dec.append(dict(ev, n=int(n), t=int(t))); self.st["decisions"] += 1
        self._hx_set()
        return ev

    # ------------------------------------------------------------------ the ledger's land units
    def _unit(self, n, unit, l, j, amt):
        """The ledger's land units (land_health, land_wild, land_saved, land_lost): told when a stretch's total from the
        life passes .02, .05, .15 (a little, clearly, a lot), at most one land line a year (with the ledger on)."""
        PP = self.PP; key = (unit, int(l), int(j))
        rec = self.book[n].setdefault(key, dict(tot=0.0, lev=0))
        rec["tot"] += float(amt)
        st = (0.02, 0.05, 0.15)
        if rec["lev"] < 3 and rec["tot"] >= st[rec["lev"]] - 1e-12 and PP.t - self.lt[n] >= 52:
            rec["lev"] += 1; self.lt[n] = int(PP.t)
            if getattr(PP, "wa_l", False):
                PP._wa_tell(int(n), unit, ("a little", "clearly", "a lot")[rec["lev"] - 1],
                            dict(town=int(l), stretch=STRETCHES[j], name=self.names[l][j]), PP._wa_cause({}, None, PP.t), PP.t)

    # ------------------------------------------------------------------ what the engine applies, what the game reads
    def take(self):
        """The week's one-off moves the engine applies (and clears): needs (N x 5), mood, stress, resources (N x 5)."""
        out = (self.fx_need.copy(), self.fx_mood.copy(), self.fx_stress.copy(), self.fx_res.copy())
        self.fx_need[:] = 0; self.fx_mood[:] = 0; self.fx_stress[:] = 0; self.fx_res[:] = 0
        return out

    def targets(self):
        """What the land adds to the targets the resources drift to this week: money, health (the dose)."""
        return dict(money=self.tg_money, health=self.tg_health)

    def drain(self):
        out = self.news; self.news = []
        return out

    def scn(self, items, ns):
        """The scenario hook (scn): each item dict(kind, harvest, severity) is applied now to the towns of lives ns: a
        hazard strikes (as the world's own strike: World._strike), a harvest is set for the year."""
        PP, W = self.PP, self.W; t = int(PP.t); a = float(PP._age(t))
        ls = sorted({int(PP.loc[n]) for n in ns})
        for it in items or []:
            it = dict(it or {})
            k_ = it.get("kind")
            if k_ in HAZARDS:
                sv = float(it.get("severity", 0.6))
                for l in ls:
                    W.dis_pending.append([int(W.t), l, HAZARDS.index(k_), sv]); W._strike()
                    self._strike(l, HAZARDS.index(k_), max(sv, 0.01), t, a)
            hv = it.get("harvest")
            if hv in HARVESTS:
                old = self.harvest.copy()
                for l in ls:
                    self.harvest[l] = HARVESTS.index(hv); self.harvest_t[l] = t
                self._harvest_fx(ls, old)
        self._hx_set()

    def place(self, n):
        """The portrait's land row (public facts only): each stretch's name, health and wildness (and their words), the
        last hazard and how long ago, the last harvest."""
        l = int(self.PP.loc[n]); t = int(self.PP.t)
        land = [dict(stretch=STRETCHES[j], name=self.names[l][j], health=round(float(self.h[l, j]), 3),
                     wild=round(float(self.wd[l, j]), 3), health_word=health_word(self.h[l, j]),
                     wild_word=wild_word(self.wd[l, j])) for j in range(3)]
        hz = None if self.hz_kind[l] < 0 else dict(kind=HAZARDS[int(self.hz_kind[l])], age=round((t - int(self.hz_t[l])) / 52.0, 2))
        hv = HARVESTS[int(self.harvest[l])] if self.harvest_t[l] > NEVER // 2 else None
        return dict(land=land, land_hazard=hz, harvest=hv, land_tracked=bool(self.dev))

    def person(self, n):
        """Per person: the ways held (key, step 0-2, the age the step began, years worked), the bridges ever opened and
        held now (each dict(a, b, opens))."""
        return dict(ways=[dict(key=w_["key"], step=int(w_["step"]), step_since_age=round(float(w_["since"]), 2),
                               worked=round(float(w_["worked"]), 2)) for w_ in self.ways[n]],
                    bridges_open=[dict(self.BR[b_]) for b_ in self.bopen[n]],
                    bridges_held=[dict(self.BR[b_]) for b_ in self.bheld[n]])

    def output(self):
        """The run's land: each life's ways, bridges, the land ring (what it planted, saved or cleared and whether it
        still stands), its hit and course; the towns' stretches; the counts the checks read."""
        lives = []
        for n in range(self.N):
            ring = [dict(k_, stands=bool(self._stands(k_)), stretch=STRETCHES[k_["j"]]) for k_ in self.kept[n]]
            lives.append(dict(self.person(n), ring=ring, hit=bool(self.hit_t[n] > NEVER // 2),
                              course=SHAPES[int(self.shape[n])] if self.shape[n] >= 0 else None,
                              lost=bool(self.lost[n]), mins=round(float(self.mins[n]), 1),
                              told=[[u_, l_, STRETCHES[j_], round(r_["tot"], 5)] for (u_, l_, j_), r_ in self.book[n].items()]))
        return dict(stretches=list(STRETCHES), health=self.h.round(4).tolist(), wild=self.wd.round(4).tolist(),
                    start_health=self.h0.round(4).tolist(), start_wild=self.wd0.round(4).tolist(),
                    lives=lives, decisions=list(self.dec), counts=dict(self.st, flood_back=[list(x_) for x_ in self.flood_back]))
