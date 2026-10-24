"""Release's reader for v24's "world answers" bar rows (records/v24/scope.md WA1 to WA9; the spec is
chroma-world/spheres/world-answers-v1.md, sections 2, 4 D, 5 and 6 F7). The Engine tunes its refit against this reading.

    python3 -B wa_check.py run <tree> <seed> <N> <years> <out.json> [--px '<json>'] [--notice-off]
    python3 -B wa_check.py judge <dir of run JSONs> [--off <dir of --notice-off runs>] [--out report.txt]
                                 [--min-known 10] [--min-group 5]
    python3 -B wa_check.py same <tree> <seed> <N> <years> [--px '<json>']     (the reader is read-only: same lives)

RUN. One world as answers/measure.py makes it (world_seed = seed, preset (seed - 41) % 4 + 1 as check_pack, Earth with
its packs, world on), from <tree> (a whole repository: its chroma-engine/v22-speedpass first on sys.path, batch.LIB_DIR
and batch.PACK_DIR pointed at its chroma-library and chroma-packs, as out/heights/heights_engine.py does). P = the
engine's DEFAULT, world_answers True with its sub-switches at their defaults, then --px, then --notice-off (wa_notice
False). The batch loads the Library's world answers moments (load_batch wa=, as tools/t_steps.py does), and aims= and
foot= when P turns those on. The run is driven by run_steps with every value sent back unchanged (run()'s lives;
`same` checks that the wrappers below change no life). OMP_NUM_THREADS defaults to 1.

DEFINITIONS (one life; every number below is in the per-life JSON, rounded to 5 places):
  rings     close (the cast's colours, weighted by closeness), groups (its settings' norms), places (its haunts' mixes),
            town (its town's nine sphere mixes). Change is total variation (TV), sum |d| / 2 of a colour mix.
  direct    measure.py's "caused", its own wrappers copied: the TV the life's own pushes made at the moment they landed
            (People._push, People._sph_lever). As in measure.py it counts every place and every town the push moved,
            while total counts only the life's own haunts and town, so a lever that founds or moves a place in town
            that is not their haunt can lift the places share past 1. Kept for comparability with the spec's "today";
            the own-haunts and own-town part is kept beside it (direct_own, ledger_x places_own) and shown, not judged.
  ledger    the TV the Engine's wa_ledger counts for the life OUTSIDE those pushes, read at the ledger's entry points
            (_wa_pmove's colours, _wa_gmove's norm, _wa_gvec, _wa_unit's place_mix, place_founded and town_sphere) under
            the ledger's own gates (wa_ledger on, from ledger.from_age, 12), by source: "being there" (presence, A and B),
            "leading it" (the leaders' mix), "holding out" (the odd one out), "the years together" (a partner's or
            child's drift), "decision" (F2), "other". The close ring's is weighted by closeness, as measure.py weighs
            that ring. What the ledger counts inside the pushes is kept apart as ledger.direct (a cross-check of
            direct, from 12) and never added. TV units only: closeness and trust moved (sum |d|), group members gained
            (share of the size at joining), places kept open (a count) and national pushes (push size in reach units,
            by domain) are separate fields (ledger_x).
  caused    direct + ledger (every source but ledger.direct).       total: measure.py's quarter-by-quarter TV of the
            ring while the life lives (People.quarter).               share = caused / total (0 when both are 0; when
            only total is 0 the share is left out and counted).
  world share   (chan "outside world" + chan "social") / the sum of the 9 channels, each summed |.| over colours
            (measure.py, an.py): the world's share of the character's own colour change. All 9 shares are kept.
  Known     Release's reading: heights_judge.parts(...)["ge_known_strict"] (imported from out/heights/heights_judge.py:
            leading a sphere (rung 4), "good name in town" or a master's stand-in, or Notable or Historic), its inputs
            read as heights_engine.py reads them (roles ever held, TIER 2 summits, floor(PP.rung) per sphere and the
            settings led at each year's first week). Beside it the Engine's own: phase 2's Known weeks
            (wa_ledger known_weeks, only with wa_phase2) and the heights' Known week (with heights on).
  highest rung    Release's rung peak, max over spheres (0 newcomer .. 4 leader); standing peak, max of People.standing
            (0 .. 3) at the same reads; maxrung_q, measure.py's unfloored quarterly peak.
  told      the ledger's told lines (wa_told): count, ages, by ring.
  decisions the decision moments answered (wa_dec, "left it" included; decided counted apart), national when made at
            national standing; Known years = known_weeks / 52, national years from wa_nat each week (a wrapper on
            wa_set_known); the lead colour while Known = argmax of the character's colours summed over the Known weeks.
  kept      at the end of the run, per ring, sum kept_u x TV_u / sum TV_u over the footprints whose state can still be
            read, kept_u the Engine's own F5 projection clip((now - base) . dir / dir . dir, 0, 1) as wa_output reads it;
            with the share of the ring's TV that was readable (per ring: kept, sum kept x TV, TV read, TV in all).
            Beside it the Engine's own (kept_engine: its largest footprint only).
  national  Release's own reading (the engine has no counter of national change): by family (state: support, welfare,
            Q, laws, law_push; colour: Dem_q, dem_push; culture: norm_x, norm_push, trust; economy: ineq, housing; institution: inst_legitimacy,
            inst_corruption, inst_capacity; tech: tech_adopt_v, medical0; belief: the faith shares of pop), caused =
            sum |d| the life's own pushes made when they landed (World._apply_pushes applies the queue one push at a
            time, same order, same result; a push is the life's when it comes from its People._push, its decision or
            its minister's law), total = sum |d| quarter by quarter while the life lives. The national share is the
            largest family share. law_push, dem_push and norm_push are the queues the pushes land in (the world adds
            them into laws, Dem_q and norm_x and decays them each quarter; nothing else moves them), so each family
            counts the state with its queue inside: read on the queue alone, a life that pushes it at all owns all of
            its change (10-20, with the Engine: dem_push alone gave one life .65 of the national colour's change, .006
            of Dem_q's with the queue inside).
  met (WA4) new people entering the cast in People._new_people (by chance and through friends, where E2's alike draws
            act) while the life's strongest goal has gs >= .5 (wa_gstr: the engine sets it each week, wa_notice on or off);
            fitting when E2's fit >= .5 (clip(5 x pie . goal mix - 1, 0, 1), 1 for a cast member in the goal's sphere who
            stands, as _wa_fill_bonus). Rate = fitting met / strong-goal years (quarters / 4). The engine's own wa_met
            counts only E2's alike draws, which do not exist with wa_notice off, so it cannot make the ratio (met.engine).

JUDGE (pools the seeds; bands from sphere_data.WORLD_ANSWERS["checks"] and ["phase2"], stored by each run):
  WA1 world   median world share, all lives                          >= checks.WA1_world_share_min
  WA1 rings   lives not Known (Release): median share, groups/places/town <= checks.WA1_ring_share_max
  WA2 alone   share of lives whose caused groups + places is under 1e-6   <= checks.WA2_none_left_alone_max
  WA2 lines   lives reaching 80: median told lines >= WA2_lines_median_min, and the least >= WA2_lines_min (the bar says
              played lives; lives left alone are read here, which is stricter)
  WA3         median share by highest rung (2 or less, 3, 4), groups, places and town: strictly rising (each level read
              from --min-group lives); by standing peak shown beside it. The close ring is shown, not judged: its share
              passes 1 because the ledger's weekly drifts ("the years together") are summed while total is quarterly net
  WA4         fitting met a strong-goal year, wa_notice on / off, the seeds in both   within checks.WA4_notice_x
  WA7 town    Known (Release) lives: median town share                within phase2.checks.WA7_town_share
  WA7 nation  lives that never held "head of government" (Release's head of state): the largest national share
              <= phase2.checks.WA7_national_share_max (every life; median and 90th percentile shown)
  WA7 world   Known (Release) lives: median world share                >= phase2.checks.WA7_world_share_min
  WA8         the Engine's Known lives: decisions a Known year pooled (sum decisions / sum years), below national within
              phase2.decisions_y.known; at national standing read only (Emren's card 10-20: not reached in v24, the
              band .national in v25); colour-even: the pooled rate by lead colour while
              Known (colours with --min-group lives), max / min <= phase2.checks.WA8_colour_even_x
  WA9         Known (Release) lives: median kept, groups, places and town together   within phase2.checks.WA9_kept
A row with fewer than --min-known Known lives says so and is not judged. The Engine's Known reading is shown beside."""
import argparse, glob, importlib.util, json, math, os, subprocess, sys, time

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HEIGHTS_JUDGE = "/mnt/project-files/chroma-release/out/heights/heights_judge.py"
PRESETS = {1: "", 2: "W.6 G.4", 3: "U.7 R.3", 4: "B.6 R.4"}          # measure.py's
RINGS = ("close", "groups", "places", "town")
LED_RING = dict(place_mix="places", place_founded="places", town_sphere="town")
FAM = dict(state=("support", "welfare", "Q", "laws", "law_push"), colour=("Dem_q", "dem_push"), culture=("norm_x", "norm_push", "trust"),
           economy=("ineq", "housing"), institution=("inst_legitimacy", "inst_corruption", "inst_capacity"),
           tech=("tech_adopt_v", "medical0"), belief=("@faith",))
DOM_FAM = dict(state=("state", "colour"), culture=("culture", "colour"), economy=("economy",),
               institution=("institution",), tech=("tech",), belief=("belief",))
COL = "WUBRG"
TOOL = "wa_check v1"


def r5(x):
    if x is None:
        return None
    x = float(x)
    return None if math.isnan(x) else round(x, 5)


def heights_judge():
    """Release's Known reading, imported from heights_judge.py (one definition)."""
    sp = importlib.util.spec_from_file_location("release_heights_judge", HEIGHTS_JUDGE)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


def tv(a, b):
    return 0.5 * float(np.abs(np.asarray(a, float) - np.asarray(b, float)).sum())


# ===================================================================================================== run: the wrappers
class Rec:
    """Everything the wrappers record, one world."""

    def __init__(self, N):
        self.N = N; z = lambda: np.zeros(N)
        self.direct = {r: z() for r in RINGS}; self.total = {r: z() for r in RINGS}
        self.own = {r: z() for r in ("places", "town")}             # direct, on the life's own haunts and town only
        self.led = {r: {} for r in RINGS}; self.ledx = {}          # ring -> source -> N; field -> source -> N
        self.nat_led = [dict() for _ in range(N)]                   # the ledger's national pushes by domain
        self.maxrung = z(); self.maxstand = z()
        self.nat_c = {f: z() for f in FAM}; self.nat_t = {f: z() for f in FAM}
        self.nat_prev = None; self.nat_lost = 0; self.nat_items = 0
        self.met_fit = z(); self.met_all = z(); self.met_fsum = z(); self.strong_q = z()
        self.natw = z(); self.kw = np.zeros((N, 5)); self.PP = None; self.extra = None
        self.prev = {}

    def add(self, d, key, lab, n, v):
        a = d.setdefault(key, {}).setdefault(lab, np.zeros(self.N))
        if np.ndim(n) == 0:
            a[int(n)] += float(v)
        else:
            np.add.at(a, np.asarray(n, np.int64), np.asarray(v, float))


REC = None
CTX = []   # (source, life) while a push or a decision runs


def _label(what):
    if CTX:
        return CTX[-1][0]
    return what if isinstance(what, str) else "other"


def fam_snap(W, fams):
    out = {}
    for f in fams:
        for a in FAM[f]:
            if a == "@faith":
                p = getattr(W, "pop", None)
                if p is not None and np.ndim(p) >= 4:
                    s = np.moveaxis(np.asarray(p, float), 3, 0).reshape(np.shape(p)[3], -1).sum(1)
                    out[(f, a)] = s / max(float(s.sum()), 1e-300)
                else:
                    out[(f, a)] = None
            else:
                v = getattr(W, a, None)
                out[(f, a)] = None if v is None else np.array(v, float).reshape(-1)
    return out


def fam_diff(s0, s1):
    """Sum |d| per family between two snapshots (a variable missing before counts from 0; a grown one, its new part)."""
    d = {}
    for (f, a), v1 in s1.items():
        v0 = s0.get((f, a))
        if v1 is None:
            continue
        v0 = np.zeros_like(v1) if v0 is None else v0
        if v0.shape != v1.shape:
            m = max(len(v0), len(v1)); v0 = np.pad(v0, (0, m - len(v0))); v1 = np.pad(v1, (0, m - len(v1)))
        d[f] = d.get(f, 0.0) + float(np.abs(v1 - v0).sum())
    return d


def install(N):
    """The read-only wrappers. measure.py's (People._push, People._sph_lever, People.quarter: direct and total) are
    copied from answers/measure.py; the others read the ledger, the national pushes, the people met and Known."""
    global REC
    import world_people as WP
    import world as WM
    REC = R = Rec(N)
    P_ = WP.People

    def snap(self, n):   # measure.py
        W = self.W
        s = dict(pie=self.pie[n].copy(), c=self.c[n].copy(), snorm=self.snorm[n].copy())
        if getattr(W, "hp_s", None) is not None:
            s["hp"] = W.hp_s.copy(); s["sph"] = W.sph_s.copy()
        return s

    def credit(self, n, s0):   # measure.py
        R.direct["close"][n] += float((np.maximum(self.c[n], s0["c"]) * 0.5 * np.abs(self.pie[n] - s0["pie"]).sum(1)).sum())
        R.direct["groups"][n] += tv(self.snorm[n], s0["snorm"])
        if "hp" in s0:
            R.direct["places"][n] += tv(self.W.hp_s, s0["hp"])
            R.direct["town"][n] += tv(self.W.sph_s, s0["sph"])
            hp = self.W.hp_s.reshape(-1, self.W.hp_s.shape[-1]); hp0 = s0["hp"].reshape(hp.shape)   # (not measure.py's)
            h = self.hnt[n]; h = h[h >= 0]; l = int(self.loc[n])
            R.own["places"][n] += 0.5 * float(np.abs(hp[h] - hp0[h]).sum())
            R.own["town"][n] += tv(self.W.sph_s[l], s0["sph"][l])

    _push0 = P_._push
    def _push(self, n, ma, q, lev, dom, base, target, var, t):
        s0 = snap(self, n); CTX.append(("direct", int(n)))
        try:
            r = _push0(self, n, ma, q, lev, dom, base, target, var, t)
        finally:
            CTX.pop()
        credit(self, n, s0)
        return r
    P_._push = _push

    _sl0 = P_._sph_lever
    def _sph_lever(self, n, j, lev, ma, q, office, dom, t):
        s0 = snap(self, n); CTX.append(("direct", int(n)))
        try:
            r = _sl0(self, n, j, lev, ma, q, office, dom, t)
        finally:
            CTX.pop()
        credit(self, n, s0)
        return r
    P_._sph_lever = _sph_lever

    _q0 = P_.quarter
    def quarter(self, t, S):   # measure.py's, as it is
        W = self.W; prev = R.prev
        if R.PP is None:
            R.PP = self
        if prev:
            alive = ~self.dead
            same = (self.uid == prev["uid"]) & self.used & prev["used"]
            w = np.maximum(self.c, prev["c"]) * same
            R.total["close"] += alive * (w * 0.5 * np.abs(self.pie - prev["pie"]).sum(2)).sum(1)
            sk = (self.skind == prev["skind"]) & (self.skind >= 0)
            R.total["groups"] += alive * (sk * 0.5 * np.abs(self.snorm - prev["snorm"]).sum(2)).sum(1)
            if "hp" in prev and getattr(self, "hnt", None) is not None:
                hp = W.hp_s.reshape(-1, W.hp_s.shape[-1]); hp0 = prev["hp"].reshape(hp.shape)
                dp = 0.5 * np.abs(hp - hp0).sum(1)
                h = self.hnt
                R.total["places"] += alive * np.where(h >= 0, dp[np.maximum(h, 0)], 0).sum(1)
                ds = 0.5 * np.abs(W.sph_s - prev["sph"]).sum((1, 2))
                R.total["town"] += alive * ds[self.loc]
        r = _q0(self, t, S)
        if getattr(self, "rung", None) is not None:
            np.maximum(R.maxrung, np.where(self.dead, 0, self.rung.max(1)), out=R.maxrung)
        np.maximum(R.maxstand, np.where(self.dead, 0, np.asarray(self.standing).max(1)), out=R.maxstand)
        prev.update(uid=self.uid.copy(), used=self.used.copy(), c=self.c.copy(), pie=self.pie.copy(),
                    skind=self.skind.copy(), snorm=self.snorm.copy())
        if getattr(W, "hp_s", None) is not None:
            prev.update(hp=W.hp_s.copy(), sph=W.sph_s.copy())
        return r
    P_.quarter = quarter

    # ---- the ledger's entry points (each calls the engine's own unchanged)
    _gm0 = P_._wa_gmove
    def _wa_gmove(self, n, j, t, dnorm=None, members=None, what=None):
        if self.wa_l and self._age(t) >= self.wa_age0:
            lab = _label(what)
            if dnorm is not None:
                R.add(R.led, "groups", lab, n, 0.5 * float(np.abs(np.asarray(dnorm, float)).sum()))
            if members is not None:
                R.add(R.ledx, "group_members", lab, n, float(members))
        return _gm0(self, n, j, t, dnorm=dnorm, members=members, what=what)
    P_._wa_gmove = _wa_gmove

    _gv0 = P_._wa_gvec
    def _wa_gvec(self, m, d, t, what):
        if self._age(t) >= self.wa_age0:
            R.add(R.led, "groups", _label(what), np.arange(self.N), (m * 0.5 * np.abs(np.asarray(d, float)).sum(-1)).sum(1))
        return _gv0(self, m, d, t, what)
    P_._wa_gvec = _wa_gvec

    _un0 = P_._wa_unit
    def _wa_unit(self, n, unit, key, amt, who, t, base=None, d=None, size=None, what=None):
        if self.wa_l and self._age(t) >= self.wa_age0:
            lab = _label(what)
            if unit in LED_RING:
                R.add(R.led, LED_RING[unit], lab, n, float(amt))
                if unit != "town_sphere" and int(key) in self.hnt[int(n)]:
                    R.add(R.ledx, "places_own", lab, n, float(amt))
            elif unit == "place_kept_open":
                R.add(R.ledx, "kept_open", lab, n, 1.0)
            elif unit == "nation":
                R.add(R.ledx, "nation", lab, n, float(amt))
                R.nat_led[int(n)][str(key)] = R.nat_led[int(n)].get(str(key), 0.0) + float(amt)
        return _un0(self, n, unit, key, amt, who, t, base=base, d=d, size=size, what=what)
    P_._wa_unit = _wa_unit

    _pm0 = P_._wa_pmove
    def _wa_pmove(self, nn, kk, t, col=None, dc=None, dtr=None, what=None):
        if self.wa_l and len(nn) and self._age(t) >= self.wa_age0:
            lab = _label(what); nn_ = np.asarray(nn, np.int64); kk_ = np.asarray(kk, np.int64)
            if col is not None:
                tv_ = 0.5 * np.abs(np.asarray(col, float)).sum(-1)
                R.add(R.led, "close", lab, nn_, tv_ * np.asarray(self.c[nn_, kk_], float))
                R.add(R.ledx, "person_colours_raw", lab, nn_, tv_)
            if dc is not None:
                R.add(R.ledx, "closeness", lab, nn_, np.abs(np.asarray(dc, float)))
            if dtr is not None:
                R.add(R.ledx, "trust", lab, nn_, np.abs(np.asarray(dtr, float)))
        return _pm0(self, nn, kk, t, col=col, dc=dc, dtr=dtr, what=what)
    P_._wa_pmove = _wa_pmove

    _rs0 = P_.wa_resolve
    def wa_resolve(self, n, key, j, scope, ma, succ, idle, t=None):
        CTX.append(("decision", int(n)))
        try:
            return _rs0(self, n, key, j, scope, ma, succ, idle, t)
        finally:
            CTX.pop()
    P_.wa_resolve = wa_resolve

    _ws0 = P_.wa_setup
    def wa_setup(self, P):
        R.PP = self
        return _ws0(self, P)
    P_.wa_setup = wa_setup

    _sk0 = P_.wa_set_known
    def wa_set_known(self, known, national, t):
        r = _sk0(self, known, national, t)
        R.natw += self.wa_nat
        R.kw += np.asarray(self.w, float) * self.wa_known[:, None]
        return r
    P_.wa_set_known = wa_set_known

    _np0 = P_._new_people
    def _new_people(self, t):
        if not hasattr(self, "wa_gstr"):
            return _np0(self, t)
        uid0 = self.uid.copy(); used0 = self.used.copy()
        strong = ~self.dead & (self.wa_gstr >= 0.5) & (self.wa_gsph >= 0)
        r = _np0(self, t)
        R.strong_q += strong
        new = self.used & ((self.uid != uid0) | ~used0) & strong[:, None]
        for n_ in np.nonzero(new.any(1))[0]:
            ks = np.nonzero(new[n_])[0]
            fit = np.clip(self.pie.shape[-1] * (np.asarray(self.pie[n_, ks], float) @ self.wa_gmix[n_]) - 1, 0, 1)
            inn = self._wa_cast_in(int(n_), int(self.wa_gsph[n_]))[ks] & (np.asarray(self.stand[n_, ks]) >= 1)
            fit = np.where(inn, 1.0, fit)
            R.met_all[n_] += len(ks); R.met_fit[n_] += int((fit >= 0.5).sum()); R.met_fsum[n_] += float(fit.sum())
        return r
    P_._new_people = _new_people

    _wo0 = P_.wa_output
    def wa_output(self):
        out = _wo0(self)
        R.extra = read_end(self)
        return out
    P_.wa_output = wa_output

    # ---- the national pushes: whose each is, and what it moved when it landed
    W_ = WM.World
    _wp0 = W_.push
    def push(self, domain, var, amount, sign):
        n = CTX[-1][1] if CTX else None
        if n is None:   # W40's minister: WorldLink.on_act pushes the law inside its loop over the lives (n_)
            f = sys._getframe(1)
            if f.f_code.co_name == "on_act" and "mn_" in f.f_locals and "n_" in f.f_locals:
                n = int(f.f_locals["n_"])
        self.__dict__.setdefault("_wa_tags", []).append(n)
        return _wp0(self, domain, var, amount, sign)
    W_.push = push

    _ap0 = W_._apply_pushes
    def _apply_pushes(self):
        allf = tuple(FAM)
        s = fam_snap(self, allf)
        PP = R.PP
        alive = (~np.asarray(PP.dead)) if PP is not None else np.ones(R.N, bool)
        if R.nat_prev is not None:
            for f, v in fam_diff(R.nat_prev, s).items():
                R.nat_t[f] += alive * v
        R.nat_prev = s
        q = list(self._queue); tags = list(self.__dict__.get("_wa_tags", []))
        self._wa_tags = []
        if len(tags) != len(q):
            R.nat_lost += abs(len(q) - len(tags)); tags = (tags + [None] * len(q))[:len(q)]
        if not q:
            return _ap0(self)
        for it, n in zip(q, tags):   # one at a time: the same pushes in the same order, the same state after
            fams = DOM_FAM.get(str(it[0]), ()) if n is not None else ()
            s0 = fam_snap(self, fams) if fams else None
            self._queue = [it]
            _ap0(self)
            if s0 is not None:
                R.nat_items += 1
                for f, v in fam_diff(s0, fam_snap(self, fams)).items():
                    R.nat_c[f][n] += v
        self._queue = []   # (the totals are read quarter to quarter, at the start of each quarter's pushes)
    W_._apply_pushes = _apply_pushes


def read_end(PP):
    """At the end of the run (inside wa_output): told lines, decisions and what the world kept, per life."""
    W = PP.W; N = PP.N; C = PP.pie.shape[-1]
    told = []
    for n in range(N):
        ls = PP.wa_told[n]; br = {}
        for ln in ls:
            u = ln.get("unit"); rg = "nation" if u == "nation" else ("person" if str(u).startswith("person") else
                                                                  "group" if str(u).startswith("group") else
                                                                  "place" if str(u).startswith("place") else "town_sphere")
            br[rg] = br.get(rg, 0) + 1
        told.append(dict(n=len(ls), ages=[round(float(x.get("age", 0)), 2) for x in ls], by_ring=br))
    dec = [dict(n=0, national=0, decided=0) for _ in range(N)]
    for d in PP.wa_dec:
        x = dec[int(d["n"])]; x["n"] += 1; x["national"] += bool(d.get("national")); x["decided"] += d.get("answer") == "decided"
    kept = []
    for n in range(N):
        acc = {r: [0.0, 0.0, 0.0] for r in ("person", "group", "place", "town_sphere")}   # sum kept x tv, sum tv read, sum tv
        for k in np.nonzero(PP.wa_puid[n] >= 0)[0]:
            w = float(PP.wa_ptot[n, k, 0])
            if w <= 0:
                continue
            acc["person"][2] += w
            if PP.uid[n, k] == PP.wa_puid[n, k]:
                dv = PP.wa_pdir[n, k].astype(float); dd = float(dv @ dv)
                if dd > 1e-12:
                    kp = float(np.clip((PP.pie[n, k] - PP.wa_pbase[n, k]) @ dv / dd, 0, 1))
                    acc["person"][0] += kp * w; acc["person"][1] += w
        for j in range(PP.M):
            w = float(PP.wa_gtot[n, j, 0])
            if w <= 0:
                continue
            acc["group"][2] += w
            dv = PP.wa_gdir[n, j]; dd = float(dv @ dv)
            if PP.skind[n, j] >= 0 and PP.sjoin[n, j] == PP.wa_gjoin[n, j] and dd > 1e-12:
                kp = float(np.clip((PP.snorm[n, j] - PP.wa_gbase[n, j]) @ dv / dd, 0, 1))
                acc["group"][0] += kp * w; acc["group"][1] += w
        for (unit, key), rec in PP.wa_u[n].items():
            if unit not in LED_RING:
                continue
            r_ = "place" if LED_RING[unit] == "places" else "town_sphere"; w = float(rec["tot"])
            if w <= 0:
                continue
            acc[r_][2] += w
            if rec["dir"] is None or rec["base"] is None:
                continue
            dv = rec["dir"]; dd = float(dv @ dv); cur = None
            if r_ == "place" and getattr(W, "hp_s", None) is not None:
                cur = W.hp_s.reshape(-1, C)[int(key)]
            elif r_ == "town_sphere" and getattr(W, "sph_s", None) is not None:
                cur = W.sph_s[key[0], key[1]]
            if cur is not None and dd > 1e-12:
                kp = float(np.clip((cur - rec["base"]) @ dv / dd, 0, 1))
                acc[r_][0] += kp * w; acc[r_][1] += w
        kept.append({r: [r5(a[0] / a[1]) if a[1] > 0 else None, r5(a[0]), r5(a[1]), r5(a[2])] for r, a in acc.items()})
    return dict(told=told, dec=dec, kept=kept, met_engine=np.asarray(PP.wa_met, float).tolist())


def setup(tree, px, notice_off):
    eng = os.path.join(tree, "chroma-engine", "v22-speedpass")
    for k in list(os.environ):
        if k.startswith("CHROMA_") or k == "PACK_DIR":
            os.environ.pop(k)
    sys.path.insert(0, eng)
    import engine as E, batch
    if not os.path.abspath(E.__file__).startswith(os.path.abspath(eng)):
        raise SystemExit(f"engine imported from {E.__file__}, not {eng}")
    batch.LIB_DIR = os.path.join(tree, "chroma-library"); batch.PACK_DIR = os.path.join(tree, "chroma-packs")
    P = dict(E.DEFAULT)
    if "world_answers" not in P:
        raise SystemExit("this engine has no world_answers switch")
    P["world_answers"] = True
    P.update(px)
    if notice_off:
        P["wa_notice"] = False
    kw = {}
    va = batch.load_batch.__code__.co_varnames
    for k, sw in (("wa", "world_answers"), ("aims", "aims"), ("foot", "foot_on")):
        if k in va:
            kw[k] = bool(P.get(sw))
    L = batch.load_batch("earth", packs=list(batch.PACKS), **kw)
    return E, batch, L, P, kw


def world_P(E, P, seed):
    """measure.py's world: world_seed = seed, preset (seed - 41) % 4 + 1, Earth."""
    pr = (seed - 41) % 4 + 1
    P = dict(P); P.update(world=True, world_seed=seed, world_cfg=dict(setting="earth"))
    if PRESETS[pr]:
        m = E.parse(PRESETS[pr]); m = m / m.sum()
        P["f_world"] = 0.25 * (m - 0.2) * 5 / 4; P["world_profile"] = 0.6 * np.full(E.C, 0.2) + 0.4 * m
    return P, pr


def drive(E, N, Y, seed, P, L):
    """run_steps with every value sent back unchanged; Release's peaks read at each year's first week (heights_engine.py)."""
    from world_people_base import G, LEAD_KINDS
    g = E.run_steps(N=N, years=Y, seed=seed, P=P, lib=L)
    pk = dict(rung=None, stand=None, lead={k: np.zeros(N, bool) for k in LEAD_KINDS})
    p = next(g)
    try:
        while True:
            if p.kind == "week" and p.t % 52 == 0:
                PP = getattr(p.state.get("WL"), "PP", None)
                if PP is not None:
                    r = np.floor(PP.rung)
                    pk["rung"] = r if pk["rung"] is None else np.maximum(pk["rung"], r)
                    s = np.asarray(PP.standing) if hasattr(PP, "standing") else None
                    if s is not None:
                        pk["stand"] = s if pk["stand"] is None else np.maximum(pk["stand"], s)
                    me = PP.slead == -2
                    for k in LEAD_KINDS:
                        pk["lead"][k] |= (me & (PP.skind == G[k])).any(1)
            p = g.send(p.value)
    except StopIteration as done:
        return done.value, pk


def cmd_run(a):
    t0 = time.time()
    px = json.loads(a.px) if a.px else {}
    E, batch, L, P, kw = setup(a.tree, px, a.notice_off)
    import sphere_data as SD
    T = SD.WORLD_ANSWERS
    bands = dict(checks=T.get("checks"), phase2_checks=T.get("phase2", {}).get("checks"),
                 decisions_y=T.get("phase2", {}).get("decisions_y"), from_age=T.get("ledger", {}).get("from_age"))
    HJ = heights_judge()
    N, Y, seed = a.N, a.years, a.seed
    install(N)
    P, pr = world_P(E, P, seed)
    o, pk = drive(E, N, Y, seed, P, L)
    R = REC; X = R.extra
    secs = round(time.time() - t0, 1)
    # Release's Known (heights_judge.parts), inputs as heights_engine.py reads them
    RO = o["roles"]; names = list(RO["names"]); ever = np.asarray(RO["ever"]).astype(bool)
    tier = np.asarray(L["ROLES"]["TIER"]) if "TIER" in L["ROLES"] else np.zeros(len(names), int)
    summits = [names[i] for i in range(len(names)) if i < len(tier) and tier[i] == 2]
    missing = sorted(x for x in HJ.ALL_NAMED if x not in names)
    ch = np.abs(np.asarray(o["chan"], float)).sum(2); chn = list(E.CHANNELS)
    cs = ch / np.maximum(ch.sum(1, keepdims=True), 1e-300)
    io, isoc = chn.index("outside world"), chn.index("social")
    dage = np.full(N, float(Y))
    for n_, t_, _ in o["died"]:
        dage[n_] = min(dage[n_], t_ / 52)
    WH = o["W_hist"]
    lead40 = [int(np.argmax(np.asarray(WH[40])[n])) for n in range(N)] if len(WH) > 40 else [None] * N
    wend = np.asarray(o["w"]) if np.ndim(o.get("w")) == 2 else np.asarray(WH[-1])
    WAL = o.get("wa_ledger") or {}; lv = WAL.get("lives") or [dict() for _ in range(N)]
    ht = np.asarray(o["heights"]["week"]) if o.get("heights") else None
    lives = []
    for n in range(N):
        rung = pk["rung"][n].tolist() if pk["rung"] is not None else None
        lead = {k: bool(v[n]) for k, v in pk["lead"].items()}
        hp = HJ.parts({names[i] for i in np.nonzero(ever[n])[0]}, summits, rung, lead)
        led = {r: {k: r5(v[n]) for k, v in R.led[r].items() if v[n] > 0} for r in RINGS}
        ledx = {f: {k: r5(v[n]) for k, v in d.items() if v[n] > 0} for f, d in R.ledx.items()}
        x = lv[n] if n < len(lv) else {}
        rings_e = x.get("rings") or {}
        kn_w = int(x.get("known_weeks", 0) or 0)
        lives.append(dict(
            n=n, dage=r5(dage[n]),
            rung_peak=None if rung is None else int(max(rung)), standing_peak=None if pk["stand"] is None else int(np.max(pk["stand"][n])),
            maxrung_q=r5(R.maxrung[n]), maxstand_q=r5(R.maxstand[n]),
            known=bool(hp["ge_known_strict"]), kparts={k: bool(hp[k]) for k in ("rung4", "good_name", "master", "notable", "historic", "state")},
            eng_known_weeks=kn_w, eng_nat_weeks=int(R.natw[n]),
            eng_known_age=None if ht is None or ht[n, 0] < 0 else r5(ht[n, 0] / 52),
            lead_end=int(np.argmax(wend[n])), lead40=lead40[n], lead_known=int(np.argmax(R.kw[n])) if R.kw[n].sum() > 0 else None,
            chan=[r5(v) for v in cs[n]], world_share=r5(cs[n, io] + cs[n, isoc]), outside_share=r5(cs[n, io]), chan_total=r5(ch[n].sum()),
            direct={r: r5(R.direct[r][n]) for r in RINGS}, total={r: r5(R.total[r][n]) for r in RINGS},
            direct_own={r: r5(v[n]) for r, v in R.own.items()},
            ledger=led, ledger_x=ledx, nation_led={k: r5(v) for k, v in R.nat_led[n].items()},
            nat={f: [r5(R.nat_c[f][n]), r5(R.nat_t[f][n])] for f in FAM},
            told=X["told"][n] if X else dict(n=0, ages=[], by_ring={}),
            dec=X["dec"][n] if X else dict(n=0, national=0, decided=0),
            met=dict(fit=r5(R.met_fit[n]), all=r5(R.met_all[n]), fitsum=r5(R.met_fsum[n]), strong_q=r5(R.strong_q[n]),
                     engine=r5(X["met_engine"][n]) if X else None),
            kept=X["kept"][n] if X else None,
            kept_engine={r: (v or {}).get("kept") for r, v in rings_e.items()},
            eng_rings_total={r: (v or {}).get("total") for r, v in rings_e.items()},
            by_rung=x.get("by_rung")))
    try:
        sha = subprocess.run(["git", "-C", a.tree, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        sha = None
    sw = {k: P.get(k) for k in ("world_answers", "wa_groups", "wa_places", "wa_ledger", "wa_notice", "wa_phase2", "heights", "aims")}
    res = dict(tool=TOOL, tree=a.tree, sha=sha, seed=seed, preset=pr, N=N, Y=Y, px=px, notice_off=bool(a.notice_off),
               switches=sw, batch_kw=kw, secs=secs, bands=bands, channels=chn, colours=COL, families={f: list(v) for f, v in FAM.items()},
               names_missing=missing, nat_untagged=R.nat_lost, nat_items=R.nat_items, ledger_on=bool(WAL), lives=lives)
    tmp = a.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(res, f, separators=(",", ":"))
    os.replace(tmp, a.out)
    print(f"wa_check run: seed {seed} preset {pr}, {N} lives x {Y} years in {secs} s; switches {sw}; "
          f"Known (Release) {sum(l['known'] for l in lives)}, Engine Known {sum(l['eng_known_weeks'] > 0 for l in lives)}; "
          f"told lines median {np.median([l['told']['n'] for l in lives]):.0f}; -> {a.out}", flush=True)


def cmd_same(a):
    """The wrappers are read-only: the same world run plainly (run()) and through this reader gives the same lives."""
    import hashlib
    px = json.loads(a.px) if a.px else {}
    E, batch, L, P, kw = setup(a.tree, px, False)
    P, pr = world_P(E, P, a.seed)
    dig = lambda o: hashlib.md5(json.dumps(dict(W=np.asarray(o["W_hist"]).round(12).tolist(), chan=np.asarray(o["chan"]).round(12).tolist(),
                                                died=np.asarray(o["died"]).tolist(), told=[x["told"] for x in o.get("wa_ledger", {}).get("lives", [])],
                                                dec=len(o.get("wa_ledger", {}).get("decisions", []))), default=str).encode()).hexdigest()
    t0 = time.time(); d0 = dig(E.run(N=a.N, years=a.years, seed=a.seed, P=P, lib=L)); t1 = time.time()
    install(a.N)
    o, _ = drive(E, a.N, a.years, a.seed, P, L); d1 = dig(o); t2 = time.time()
    print(f"wa_check same: plain {d0[:12]} ({t1 - t0:.0f} s), through the reader {d1[:12]} ({t2 - t1:.0f} s), "
          f"{a.N} lives x {a.years} years, seed {a.seed}, px {px}: {'SAME' if d0 == d1 else 'DIFFERENT'}")
    sys.exit(0 if d0 == d1 else 1)


# ===================================================================================================== judge
def load_dir(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            r = json.load(open(f))
        except (OSError, ValueError):
            continue
        if str(r.get("tool", "")).startswith("wa_check"):
            r["_file"] = os.path.basename(f); out.append(r)
    return out


def share(l, ring):
    c = (l["direct"][ring] or 0.0) + sum(v or 0.0 for k, v in l["ledger"][ring].items() if k != "direct")
    t = l["total"][ring] or 0.0
    if t > 1e-12:
        return c / t
    return 0.0 if c <= 1e-12 else None


def caused(l, ring):
    return (l["direct"][ring] or 0.0) + sum(v or 0.0 for k, v in l["ledger"][ring].items() if k != "direct")


def share_own(l, ring):
    """The cross-check (shown, not judged): caused on the life's own haunts or town only, over the same total."""
    lx = l["ledger_x"].get("places_own", {}) if ring == "places" else l["ledger"]["town"]
    c = ((l.get("direct_own") or {}).get(ring) or 0.0) + sum(v or 0.0 for k, v in lx.items() if k != "direct")
    t = l["total"][ring] or 0.0
    return c / t if t > 1e-12 else (0.0 if c <= 1e-12 else None)


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def pct(xs, q):
    xs = [x for x in xs if x is not None]
    return float(np.percentile(xs, q)) if xs else None


def f4(x):
    return "n/a" if x is None else f"{x:.4f}"


def nat_share(l):
    s = [c / t for c, t in (v for v in l["nat"].values()) if t and t > 0 and c is not None]
    return max(s) if s else 0.0


def kept_all(l):
    k = l.get("kept") or {}
    num = sum((k[r][1] or 0.0) for r in ("group", "place", "town_sphere") if k.get(r))
    den = sum((k[r][2] or 0.0) for r in ("group", "place", "town_sphere") if k.get(r))
    return num / den if den > 0 else None


def verdict(ok):
    return "PASS" if ok else "MISS"


def cmd_judge(a):
    runs = [r for r in load_dir(a.dir) if not r.get("notice_off")]
    skipped = [r["_file"] for r in load_dir(a.dir) if r.get("notice_off")]
    if not runs:
        raise SystemExit(f"no wa_check run JSONs in {a.dir}")
    B = runs[0]["bands"]; CK = B["checks"]; C2 = B["phase2_checks"]; DY = B["decisions_y"]
    rep = [f"v24 world answers (records/v24/scope.md WA1-WA9), wa_check judge {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
           f"runs: {len(runs)} ({', '.join(r['_file'] for r in runs)}); seeds {sorted({r['seed'] for r in runs})}; "
           f"tree {runs[0]['tree']} sha {str(runs[0].get('sha'))[:12]}; {runs[0]['N']} lives x {runs[0]['Y']} years a seed"]
    for k in ("bands", "switches", "px", "sha", "Y"):
        if len({json.dumps(r.get(k), sort_keys=True) for r in runs}) > 1:
            rep.append(f"WARNING: the runs differ in {k}: {sorted({json.dumps(r.get(k), sort_keys=True) for r in runs})}")
    rep.append(f"switches: {runs[0]['switches']}; px {runs[0]['px']}; wall time a run: "
               f"{', '.join(str(r['secs']) + ' s' for r in runs)}")
    if skipped:
        rep.append(f"left out (wa_notice off; give them with --off): {skipped}")
    if any(r.get("names_missing") for r in runs):
        rep.append(f"Known reading: names the run does not know: {sorted({x for r in runs for x in r['names_missing']})}")
    L = [l for r in runs for l in r["lives"]]
    K = [l for l in L if l["known"]]; NK = [l for l in L if not l["known"]]
    KE = [l for l in L if l["eng_known_weeks"] > 0]
    rep += [f"lives {len(L)}; Known (Release, ge_known_strict) {len(K)}; the Engine's phase-2 Known {len(KE)} "
            f"(both {sum(l['known'] and l['eng_known_weeks'] > 0 for l in L)}); reaching 80: {sum((l['dage'] or 0) >= 80 for l in L)}", ""]
    mk = a.min_known

    # WA1
    ws = [l["world_share"] for l in L]
    m = med(ws)
    rep.append(f"WA1 world share      median {f4(m)} (p10 {f4(pct(ws, 10))}, p90 {f4(pct(ws, 90))}; outside world alone "
               f"{f4(med([l['outside_share'] for l in L]))})   band >= {CK['WA1_world_share_min']}   "
               f"{verdict(m is not None and m >= CK['WA1_world_share_min'])}   [lives {len(L)}]")
    caps = CK["WA1_ring_share_max"]; parts = []; ok = True; und = 0
    for rg in ("groups", "places", "town"):
        sh = [share(l, rg) for l in NK]; und += sum(x is None for x in sh); mm = med(sh)
        ok &= mm is not None and mm <= caps[rg]
        dm = med([(l["direct"][rg] or 0) / l["total"][rg] if (l["total"][rg] or 0) > 1e-12 else None for l in NK])
        ow = f"; own {'haunts' if rg == 'places' else 'town'} only {f4(med([share_own(l, rg) for l in NK]))}" if rg != "groups" else ""
        parts.append(f"{rg} {f4(mm)} (direct alone {f4(dm)}{ow}) <= {caps[rg]}")
    rep.append(f"WA1 rings below Known  {'; '.join(parts)}   {verdict(ok and len(NK) > 0)}   [lives below Known {len(NK)} of {len(L)}"
               f"{f'; {und} shares undefined (total 0)' if und else ''}]")

    # WA2
    z = [caused(l, "groups") + caused(l, "places") < 1e-6 for l in L]; zg = [caused(l, "groups") < 1e-6 for l in L]
    v = sum(z) / len(L)
    rep.append(f"WA2 left alone, nothing moved in groups and places   {v:.3f} ({sum(z)} of {len(L)}; groups alone {sum(zg) / len(L):.3f})"
               f"   band <= {CK['WA2_none_left_alone_max']}   {verdict(v <= CK['WA2_none_left_alone_max'])}   [lives {len(L)}]")
    L80 = [l for l in L if (l["dage"] or 0) >= 80]
    if L80:
        tn = [l["told"]["n"] for l in L80]; mm = med(tn)
        rep.append(f"WA2 told lines, lives reaching 80   median {mm:.1f}, least {min(tn)} ({sum(x >= CK['WA2_lines_min'] for x in tn)} of "
                   f"{len(tn)} with {CK['WA2_lines_min']} or more; the least judged here on lives left alone, stricter than the bar's "
                   f"played lives)   band median >= {CK['WA2_lines_median_min']}, least >= {CK['WA2_lines_min']}   "
                   f"{verdict(mm >= CK['WA2_lines_median_min'] and min(tn) >= CK['WA2_lines_min'])}   [lives {len(L80)}]")
    else:
        tn = [l["told"]["n"] for l in L]; yr = [l["dage"] for l in L]
        rep.append(f"WA2 told lines   NOT READ: no life reached 80 (all lives: median {med(tn):.1f} lines, least {min(tn)}, "
                   f"over a median {med(yr):.1f} years; {sum(x >= CK['WA2_lines_min'] for x in tn)} of {len(tn)} with "
                   f"{CK['WA2_lines_min']} or more)   band median >= {CK['WA2_lines_median_min']} in 80 years   [lives {len(L)}]")

    # WA3
    lev = lambda l: None if l["rung_peak"] is None else min(max(l["rung_peak"], 2), 4)
    parts = []; ok = True; read = True
    for rg in ("groups", "places", "town", "close"):
        ms = []
        for k in (2, 3, 4):
            g = [share(l, rg) for l in L if lev(l) == k]
            ms.append((k, len(g), med(g) if len(g) >= a.min_group else None))
        got = [x[2] for x in ms if x[2] is not None]
        rise = len(got) >= 2 and all(b > a_ for a_, b in zip(got, got[1:]))
        if rg != "close":
            ok &= rise; read &= len(got) >= 2
        parts.append(f"{rg} " + ", ".join(f"{'<=2' if k == 2 else k}: {f4(mv)} ({n})" for k, n, mv in ms) + ("" if rg != "close" else " (shown)"))
    nlev = {k: sum(lev(l) == k for l in L) for k in (2, 3, 4)}
    rep.append(f"WA3 share by highest rung (lives)   {'; '.join(parts)}   band: rises at each level (groups, places, town)   "
               f"{verdict(ok) if read else 'NOT READ: fewer than 2 rung levels with ' + str(a.min_group) + ' lives'}   [lives {len(L)}: {nlev}]")
    parts = []
    for rg in ("groups", "places", "town"):
        parts.append(f"{rg} " + ", ".join(f"{s}: {f4(med([share(l, rg) for l in L if l['standing_peak'] == s]))} "
                                           f"({sum(l['standing_peak'] == s for l in L)})" for s in (0, 1, 2, 3)))
    rep.append(f"    by standing peak (shown): {'; '.join(parts)}")

    # WA4
    if a.off:
        offs = [r for r in load_dir(a.off) if r.get("notice_off")]
        so = {r["seed"] for r in offs} & {r["seed"] for r in runs}
        if not so:
            rep.append("WA4 noticed   NOT READ: no seed has both a run and a --notice-off run")
        else:
            def rate(rs):
                ls = [l for r in rs if r["seed"] in so for l in r["lives"]]
                fit = sum(l["met"]["fit"] or 0 for l in ls); yrs = sum(l["met"]["strong_q"] or 0 for l in ls) / 4
                fs = sum(l["met"]["fitsum"] or 0 for l in ls); al = sum(l["met"]["all"] or 0 for l in ls)
                return fit, yrs, fs, al, len(ls)
            f1, y1, s1, a1, n1 = rate(runs); f0, y0, s0, a0, n0 = rate(offs)
            r1 = f1 / y1 if y1 else None; r0 = f0 / y0 if y0 else None
            x = r1 / r0 if r1 is not None and r0 else None
            lo, hi = CK["WA4_notice_x"]
            rep.append(f"WA4 fitting people met a strong-goal year, on / off   {f4(x)} (on {f4(r1)} = {f1:.0f} in {y1:.1f} years; off "
                       f"{f4(r0)} = {f0:.0f} in {y0:.1f} years; fit-weighted {f4((s1 / y1) / (s0 / y0) if y1 and y0 and s0 else None)}; "
                       f"all met {f4((a1 / y1) / (a0 / y0) if y1 and y0 and a0 else None)})   band {lo} to {hi}   "
                       f"{verdict(x is not None and lo <= x <= hi) if x is not None else 'NOT READ: no strong-goal meeting off'}"
                       f"   [seeds {sorted(so)}; lives on {n1}, off {n0}]")
    else:
        rep.append("WA4 noticed   NOT READ: no --off runs given")

    # WA7
    lo, hi = C2["WA7_town_share"]
    if len(K) >= mk:
        m = med([share(l, "town") for l in K])
        rep.append(f"WA7 Known lives' share of their town's change   median {f4(m)} (direct alone "
                   f"{f4(med([(l['direct']['town'] or 0) / l['total']['town'] if (l['total']['town'] or 0) > 1e-12 else None for l in K]))}"
                   f"; own town only {f4(med([share_own(l, 'town') for l in K]))})"
                   f"   band {lo} to {hi}   {verdict(m is not None and lo <= m <= hi)}   [Known lives {len(K)}]")
    else:
        rep.append(f"WA7 Known town share   NOT READ: {len(K)} Known lives, fewer than {mk} (median {f4(med([share(l, 'town') for l in K]))})")
    if KE:
        rep.append(f"    the Engine's Known ({len(KE)}): town share median {f4(med([share(l, 'town') for l in KE]))}")
    BH = [l for l in L if not l["kparts"]["state"]]
    ns = [nat_share(l) for l in BH]
    mx = max(ns) if ns else None
    rep.append(f"WA7 share of national change, below head of state   largest {f4(mx)} (median {f4(med(ns))}, p90 {f4(pct(ns, 90))}; "
               f"Known {f4(max([nat_share(l) for l in BH if l['known']], default=None))})   band <= {C2['WA7_national_share_max']} "
               f"every life   {verdict(mx is not None and mx <= C2['WA7_national_share_max'])}   [lives {len(BH)}; "
               f"{sum(r.get('nat_untagged', 0) for r in runs)} pushes untagged]")
    if len(K) >= mk:
        m = med([l["world_share"] for l in K])
        rep.append(f"WA7 the world's share of a Known character's change   median {f4(m)}   band >= {C2['WA7_world_share_min']}   "
                   f"{verdict(m is not None and m >= C2['WA7_world_share_min'])}   [Known lives {len(K)}]")
    else:
        rep.append(f"WA7 Known world share   NOT READ: {len(K)} Known lives, fewer than {mk} (median {f4(med([l['world_share'] for l in K]))})")
    if KE:
        rep.append(f"    the Engine's Known ({len(KE)}): world share median {f4(med([l['world_share'] for l in KE]))}")

    # WA8
    if len(KE) < mk:
        why = "wa_phase2 is off in these runs" if not any(r["switches"].get("wa_phase2") for r in runs) else f"fewer than {mk}"
        rep.append(f"WA8 decisions a Known year   NOT READ: the Engine's Known lives {len(KE)} ({why}); decisions in all lives "
                   f"{sum(l['dec']['n'] for l in L)}")
    else:
        dk = sum(l["dec"]["n"] - l["dec"]["national"] for l in KE); yk = sum(l["eng_known_weeks"] - l["eng_nat_weeks"] for l in KE) / 52
        dn = sum(l["dec"]["national"] for l in KE); yn = sum(l["eng_nat_weeks"] for l in KE) / 52
        rk = dk / yk if yk else None; rn = dn / yn if yn else None
        (k0, k1), (n0, n1) = DY["known"], DY["national"]
        dd = sum(l["dec"]["decided"] for l in KE) / max(sum(l["dec"]["n"] for l in KE), 1)
        rep.append(f"WA8 decisions for others a Known year   {f4(rk)} ({dk} in {yk:.1f} years; {dd:.2f} decided, the rest left)   band {k0} to {k1}"
                   f"   {verdict(rk is not None and k0 <= rk <= k1)}   [the Engine's Known lives {len(KE)}]")
        rep.append(f"    WA8 at national standing (read only: Emren's card 10-20, not reached in v24, the band in v25)   {f4(rn)} ({dn} in {yn:.1f} years)   band {n0} to {n1}   "
                   f"{verdict(n0 <= rn <= n1) if rn is not None else 'NOT READ: no national years'}   "
                   f"[lives at national standing {sum(l['eng_nat_weeks'] > 0 for l in KE)}]")
        by = {}
        for l in KE:
            c = l["lead_known"] if l["lead_known"] is not None else l["lead_end"]
            x = by.setdefault(c, [0, 0.0, 0]); x[0] += l["dec"]["n"]; x[1] += l["eng_known_weeks"] / 52; x[2] += 1
        rr = {COL[c]: (x[0] / x[1] if x[1] else None, x[2]) for c, x in sorted(by.items())}
        got = [v[0] for v in rr.values() if v[0] is not None and v[1] >= a.min_group]
        ratio = max(got) / min(got) if len(got) >= 2 and min(got) > 0 else None
        rep.append(f"WA8 colour-even across lead colours   max/min {f4(ratio)} ("
                   + ", ".join(f"{c} {f4(v[0])} ({v[1]})" for c, v in rr.items()) + f")   band <= {C2['WA8_colour_even_x']}   "
                   + (verdict(ratio <= C2["WA8_colour_even_x"]) if ratio is not None else f"NOT READ: fewer than 2 colours with {a.min_group} lives")
                   + f"   [the Engine's Known lives {len(KE)}]")

    # WA9
    lo, hi = C2["WA9_kept"]
    kv = [kept_all(l) for l in K]
    if len([x for x in kv if x is not None]) >= mk:
        m = med(kv)
        byr = ", ".join(f"{r} {f4(med([(l['kept'] or {}).get(r, [None])[0] for l in K]))}" for r in ("group", "place", "town_sphere", "person"))
        eng = ", ".join(f"{r} {f4(med([(l['kept_engine'] or {}).get(r) for l in K]))}" for r in ("group", "place", "town_sphere", "person"))
        rep.append(f"WA9 what the world kept, Known lives   median {f4(m)} (by ring {byr}; the Engine's largest footprint {eng})   "
                   f"band {lo} to {hi}   {verdict(m is not None and lo <= m <= hi)}   [Known lives {len(K)}, {sum(x is not None for x in kv)} with a readable footprint]")
    else:
        rep.append(f"WA9 kept   NOT READ: {sum(x is not None for x in kv)} Known lives with a readable footprint, fewer than {mk} "
                   f"(median {f4(med(kv))}; all lives {f4(med([kept_all(l) for l in L]))})")
    if KE:
        rep.append(f"    the Engine's Known ({len(KE)}): kept median {f4(med([kept_all(l) for l in KE]))}")
    rep += ["", "Definitions: wa_check.py's docstring (" + os.path.abspath(__file__) + ")."]
    txt = "\n".join(rep) + "\n"
    if a.out:
        with open(a.out, "w") as f:
            f.write(txt)
    print(txt)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nm in ("run", "same"):
        s = sub.add_parser(nm)
        s.add_argument("tree"); s.add_argument("seed", type=int); s.add_argument("N", type=int); s.add_argument("years", type=int)
        if nm == "run":
            s.add_argument("out"); s.add_argument("--notice-off", action="store_true")
        s.add_argument("--px", default="{}")
    s = sub.add_parser("judge")
    s.add_argument("dir"); s.add_argument("--off"); s.add_argument("--out")
    s.add_argument("--min-known", type=int, default=10); s.add_argument("--min-group", type=int, default=5)
    a = ap.parse_args()
    {"run": cmd_run, "same": cmd_same, "judge": cmd_judge}[a.cmd](a)


if __name__ == "__main__":
    main()
