"""world_link.py: how the engine reads the outer world (chroma-engine/world-build.md, "How the engine reads the world").

engine.run builds one WorldLink when P["world"] is True and calls it at fixed points; with the world off nothing here
runs and the engine is unchanged. The link owns the World (world.py, one per world seed) and the People (world_people.py,
one row per life of the run) and turns their state into what the engine already reads: era, drivers, niche, support,
rate multipliers per moment, gates on moments, closures on options, wants that bring a moment, and pushes after acts.

Rules kept: no color pair is special here (only the modules' overlap and distance); the world's history never depends
on the lives except through pushes; keys only, the game writes the words."""
import re
import numpy as np
try:   # speed pass: np.clip's own ufunc, called without its Python wrapper (the same numbers)
    from numpy._core.umath import clip as _uclip
except ImportError:
    from numpy.core.umath import clip as _uclip
import world as WM
import world_people as PM
import world_keys as WK

TOY_SEASON = {k_: i_ for i_, k_ in enumerate(WK.TIME_OF_YEAR)}   # winter, spring, summer, autumn = the world's season
# moments the world brings on its own events (Library W39 and the specs): (domain, kind, key or None, moment, share of
# those the moment's gates admit who meet it that week). With the world on, these moments have no background rate.
WORLD_MOMENTS = [
    ("state", "election", None, "election day", 0.6),
    ("state", "election", "change", "a landslide on election night", 0.35),
    ("era", "breakthrough", "revolution", "the old order falls", 0.8),
    ("state", "regime changes", None, "the old order falls", 0.8),
    ("belief", "revival", None, "a revival fills the square", 0.25),
    ("tech", "arrives", "new treatment", "a cure is found at last", 0.3),
    ("tech", "arrives", "new medium", "everyone is suddenly on the new medium", 0.5),
    ("tech", "arrives", "new machine", "the machines come for the work", 0.3),
    ("tech", "arrives", "new kind of job", "the machines come for the work", 0.3),
    ("nature", "price shock", "energy", "the power and the networks go down", 0.4),
    ("economy", "recession declared", "crisis", "a crash takes the savings", 0.5),
    ("economy", "recession declared", "severe", "a crash takes the savings", 0.3),
    ("abroad", "war comes home", None, "war comes", 0.7),
    ("abroad", "war begins", None, "the call to serve", 0.15),
    # the C hooks (stage3-rules.md section 5; Library earth-world-seasons.lib and earth-world-institutions.lib): a sixth
    # field names who can meet it, "place" for the people living in the event's place (value["loc"]), "staff" for those
    # who work at its institution (value["inst"]); without one, everyone the gates admit
    ("institution", "sold", None, "new owners take over the firm", 0.6, "staff"),
    ("institution", "merged", None, "folded into a bigger firm", 0.7, "staff"),
    ("institution", "nationalised", None, "the state takes over the failing firm", 0.7, "staff"),
    ("institution", "leak", None, "the private files get out", 0.5, "staff"),
    ("institution", "cover-up", None, "the thing the bosses are hiding", 0.3, "staff"),
    ("nature", "bad air", None, "a season of bad air", 0.3, "place"),
    ("nature", "bad water", None, "the river runs foul", 0.4, "place"),
    ("nature", "poisoned river", None, "the river runs foul", 0.4, "place"),
    ("nature", "drought", None, "a dry year on the land", 0.5, "place"),
    ("nature", "glorious spring", None, "a glorious spring", 0.15, "place"),
    ("nature", "recovery", None, "the town builds itself back", 0.4, "place"),
    ("belief", "new movement", None, "a new faith comes to town", 0.3, "place"),
    ("belief", "faith tension", None, "the hall on the corner is shut", 0.4, "place"),
]
CRIME_W = re.compile(r"\b(robbed|burgl|mugg|attacked|break-in|broken into|stolen|pickpocket)", re.I)
DISASTER_W = re.compile(r"\b(flood|fire|storm|earthquake|quake|drought|heatwave|hurricane|landslide)\b", re.I)
PANDEMIC_W = re.compile(r"\b(pandemic|epidemic|outbreak|lockdown)\b", re.I)
RK = ["illness", "old_death", "disaster", "crime", "war", "pandemic", "jobloss", "birth"]
# outside events (read events) the world's own disasters bring: with the world on they come when a disaster strikes the
# person's town or a close person's (spec 5 §2), not on their own clock
DIS_EVR = re.compile(r"\b(disaster|flood|wildfire|earthquake|hurricane)\b", re.I)
# the lever an option pulls when the Library writes none (world-fields.md, "lever:"): by its mark; drops: or moves: is
# an exit, and an act closed by law at an institution is subvert
LEVER_MARK = {"left home": "exit", "moved away": "exit",
              "defied an authority": "subvert", "broke the law": "subvert", "hid a wrong": "subvert",
              "came out": "voice", "named their gender": "voice", "owned up": "voice", "made an enemy": "voice",
              "kept your word": "loyalty", "helped someone in need": "loyalty", "stayed home": "loyalty",
              "made a friend": "loyalty", "came home": "loyalty",
              "refused someone in need": "neglect", "broke your word": "neglect"}
NORM_MARK = {"came out": "coming out", "named their gender": "transition"}   # the norm such an act is judged by
# where an option's push lands when the Library writes no pushes: (world-fields.md): the moment's at:, group: or who:,
# else the commitment the option or moment is about
PUSH_COMMIT = {"career": ("institution", "employer"), "community": ("group", None), "faith": ("belief", None),
               "partner": ("close", "partner"), "children": ("close", "child")}
LOCAL_SEEN = ("disaster", "crime wave", "local election",   # local public events a person living there lives through
              "bad air", "bad water", "poisoned river", "drought", "glorious spring", "recovery",   # (C4's with its hook on)
              "new movement", "faith tension")                                                       # (C5's)
# the typical world after the 80-year burn-in (seeds 1-6 or 1-8, modern Earth): every channel below is neutral there
CLIM_REF = 0.51     # acceptance of coming out (.70) x the sexuality right (.73)
U_REF = 6.5         # local unemployment, percent
CAP_REF, OPEN_REF = 0.83, 0.91   # hospitals' and universities' capacity; universities' openness, mean over the classes
INFL_REF, WELF_REF, RIGHTS_REF = 3.0, 0.63, 0.82
REACH_K = 0.5       # utility of voice and subvert at the outer rings per unit of felt reach (0 to 1)
CRIME_REF = 0.17    # local crime
BELONG_REF = 0.85   # belonging met by settings and close people (People.belong): the mean week from age 20 (seed 3, 40 lives)
# WL2's sizes (values for the v22.3 refit): workers feel this share of the price squeeze the jobless feel (real wages
# lag prices); a recession takes about 3% of a wage's money (hours and raises; Great Recession hours -3%, BLS) and gives
# a little time back; a disaster in town costs money and time while its damage lasts; a lockdown at its peak (.35)
# takes about .1 off the ties a life drifts to
WL2_PAR = dict(price_work=0.5, rec_money=0.02, rec_free=0.01, dis_money=0.05, dis_free=0.03, pand_tie=0.3)
DIS_NEAR = 0.35     # share of disasters in a close person's town that become the life's own outside event
# the world's own record entries behind each kind of effect on a life (domain, kind), for its cause on hover (stage 1, WL1)
CAUSE_REC = {"housing": (("economy", "recession declared"), ("economy", "recession over")),
             "prices": (("nature", "price shock"), ("economy", "recession declared"), ("abroad", "world recession"),
                        ("abroad", "war comes home")),
             "welfare": (("state", "welfare raised"), ("institution", "budget cut"), ("state", "government falls")),
             "rights": (("state", "right gained"), ("state", "law changed"), ("state", "regime changes")),
             "law": (("state", "law changed"), ("state", "right gained"), ("state", "regime changes")),
             "crime": (("place", "crime wave"),), "war": (("abroad", "war comes home"), ("abroad", "war begins"), ("abroad", "war ends")),
             "disaster": (("nature", "disaster"),), "illness": (("nature", "pandemic"),), "pandemic": (("nature", "pandemic"),),
             "unemployment": (("economy", "recession declared"), ("abroad", "world recession"), ("tech", "arrives", "new machine"),
                              ("tech", "arrives", "new kind of job")),
             "university places": (("institution", "budget cut"),), "hospital places": (("institution", "budget cut"),),
             "technology": (("tech", "arrives"), ("tech", "spreads")), "norm": (("era", "era begins"),)}   # (domain, kind[, key's start])
CAUSE_REC.update(prices_work=CAUSE_REC["prices"], disaster_time=CAUSE_REC["disaster"],   # WL2's effects
                 recession=(("economy", "recession declared"), ("abroad", "world recession")))
CAUSE_REC["rec_hours"] = CAUSE_REC["recession"]
# a disaster's outside events by the world's hazard (world.HAZARDS), for P["dis_match"] (WL6): words in the event's name
HAZ_EVR = {"flood": r"\bflood", "fire": r"\b(wild)?fire", "quake": r"\b(earth)?quake", "storm": r"\b(storm|hurricane)",
           "heat": r"\b(heat|drought)"}
TIME_REF = 0.015   # time the groups no commitment counts take in the typical life (group_time): mean life-week from age 3 (seeds 3, 4, 40 lives x 80 years: .017, .013)
# the domain a title's standing counts in (spec 7 §2: a famous actor stands high in culture, not in the economy): by its
# institution (W40 institution=), else its sector; the packs' stage and screen titles sit at an employer in services
TITLE_DOM = {"party": "state", "ministry": "state", "council": "place", "university": "tech", "media": "culture",
             "faith body": "belief", "charity": "group", "union": "group"}
TITLE_DOM_NAME = {"lobbyist": "state", "pollster": "state"}


def title_domain(name, inst, sector):
    if name in TITLE_DOM_NAME:
        return TITLE_DOM_NAME[name]
    if inst == "charity" and sector == "knowledge":
        return "tech"
    if inst in TITLE_DOM:
        return TITLE_DOM[inst]
    if inst == "employer":
        return "culture" if sector == "services" else "tech" if sector == "knowledge" else "economy"
    if inst is not None:
        return "institution"
    return {"public": "institution", "knowledge": "tech"}.get(sector, "economy")


MIGRATE_T = {"immigrant", "refugee", "asylum applicant"}   # the catalogue's titles that take a life to another society
CITIZEN_T = {"naturalised citizen", "citizenship"}


def _isin_small(a, vals):
    """Speed pass: np.isin against a few whole numbers, as equalities (the same answer, without isin's sorting)."""
    a = np.asarray(a); r = np.zeros(a.shape, bool)
    for v_ in vals:
        r |= a == v_
    return r


class WorldLink:
    def __init__(self, E, P, L, N, seed, female, attr, KILLS, ENDS, CAR):
        cfg = dict(P.get("world_cfg") or {})
        burn = cfg.pop("burn_years", 80)
        legacy = cfg.pop("legacy", None)   # People.save() of an earlier life: this one is born into that family line
        W = P.get("world_obj")
        if W is None:
            ws = P.get("world_seed")
            s3_ = {k: bool(P[k]) for k in getattr(WM, "S3_RULES", ()) if k in P}   # stage 3 switches (stage3-rules.md §8)
            s3_.update({k: P[k] for k in getattr(WM, "SPH_RULES", ()) if P.get(k)})   # the spheres' (item 15), when on
            s3_.update({k: P[k] for k in getattr(WM, "C_RULES", ()) if P.get(k)})     # the C hooks' (item 10), when on
            if s3_:
                cfg["params"] = dict(cfg.get("params") or {}, **s3_)
            W = WM.World(int(seed if ws is None else ws), cfg=cfg)
            W.burn_in(burn)
        self.W = W; self.t0 = int(W.t); self.N = N; self.E = E; self.L = L
        PP = P.get("people_obj")
        if PP is None:
            PP = PM.People(W, N, run_seed=int(seed), female=np.asarray(female, bool))
            PP.birth(self.t0, legacy=legacy)
        self.PP = PP
        S, K = L["S"], L["K"]; self.S = S
        names = L["names"]; src = L["src"]
        # each moment's rate kind (world-build.md: illness and old-age deaths by season and medicine, disasters by place,
        # crime by place, war, pandemic, job loss by sector, births)
        rk = np.full(S, -1)
        for si in range(S):
            nm = names[si]; life = str(src[si].get("life", "")); tier = str(src[si].get("tier", ""))
            if KILLS[si] >= 0:
                rk[si] = RK.index("old_death")
            elif ENDS[si] == CAR:
                rk[si] = RK.index("jobloss")
            elif nm in ("war comes", "the call to serve"):
                rk[si] = RK.index("war")
            elif "a baby on the way" in nm:
                rk[si] = RK.index("birth")
            elif PANDEMIC_W.search(nm):
                rk[si] = RK.index("pandemic")
            elif DISASTER_W.search(nm):
                rk[si] = RK.index("disaster")
            elif CRIME_W.search(nm):
                rk[si] = RK.index("crime")
            elif "health" in life and tier == "life event":
                rk[si] = RK.index("illness")
        self.rk = rk
        # the channels the engine reads (package §5): which moments a close person's divorce or quitting makes likelier,
        # which the wish to move scales, which options find a job, gain a place in education, or are an illness's
        PAR_ = [c_[0] for c_ in E.COMMITMENTS].index("partner")
        GR_ = L.get("ROLES") or {}; AT_ = np.asarray(GR_.get("A_TITLE", np.full((S, K), -1)))
        tn_ = list(GR_.get("names", [])); kn_ = list(GR_.get("kindname", []))
        car_t = [i_ for i_ in range(len(kn_)) if kn_[i_] == "career"]
        edu_t = [i_ for i_, nm_ in enumerate(tn_) if re.search(r"\b(student|pupil|apprentice|trainee|graduate)\b", str(nm_))]
        drops_ = [[str((nt or {}).get("drops") or "") for nt in (L["notes"][si] if si < len(L["notes"]) else [])] for si in range(S)]
        self.div_s = np.array([ENDS[si] == PAR_ or bool(re.search(r"\b(divorce|separat|marriage ends|break up|breaking up)", names[si]))
                               for si in range(S)], bool)
        self.quit_s = np.array([any(d_ and ("career" in d_ or "{title}" in d_) for d_ in drops_[si]) or
                                bool(re.search(r"\b(quit|resign|walk out|hand in your notice)", names[si])) for si in range(S)], bool)
        self.move_s = np.asarray(L["MOVES"][:S], bool) | np.array([bool(re.search(r"\bmov(e|es|ing)\b|somewhere else", names[si]))
                                                                  for si in range(S)], bool)
        self.job_o = np.isin(AT_, car_t) if AT_.shape == (S, K) else np.zeros((S, K), bool)
        self.adm_o = np.isin(AT_, edu_t) if AT_.shape == (S, K) and edu_t else np.zeros((S, K), bool)
        self.ill_s = rk == RK.index("illness")
        idx = {nm: i for i, nm in enumerate(names)}
        self.wm = [(x_[0], x_[1], x_[2], idx[x_[3]], x_[4], x_[5] if len(x_) > 5 else "all") for x_ in WORLD_MOMENTS
                   if x_[3] in idx]
        self.wm_s = np.array(sorted({x[3] for x in self.wm}), int)
        self.toy = np.asarray(L.get("W_TOY", np.zeros((S, 4)))); self.toy_set = np.asarray(L.get("W_TOY_SET", np.zeros(S, bool)))
        self.toy_on = self.toy.sum(1) > 0
        self.holy = np.asarray(L.get("W_HOLY", np.full(S, -1))); self.where = np.asarray(L.get("W_WHERE", np.zeros((S, 1), bool)))
        self.group = np.asarray(L.get("W_GROUP", np.full(S, -1))); self.prem = np.asarray(L.get("W_PREMISE", np.full(S, -1)))
        self.want = np.asarray(L.get("W_WANT", np.full(S, -1)))
        # the spheres (item 15, phase 2): a moment among a haunt's regulars, one opened by a rung in its sphere, and the
        # haunt choices (an option's face picks the place)
        self.haunt = np.asarray(L.get("W_HAUNT", np.full(S, -1))); self.ladder = np.asarray(L.get("W_LADDER", np.full(S, -1)))
        self.msph = np.asarray(L.get("W_SPHERE", np.full(S, -1))); self.hpick = np.asarray(L.get("W_HPICK", np.zeros(S, bool)))
        self.osph = np.asarray(L.get("W_OSPH", np.full((S, K), -1))); self.ocol = np.asarray(L.get("W_OCOL", np.full((S, K), -1)))
        self.H_GREAT = WK.HAUNT_KINDS.index("gather.great")
        self.sphev = np.asarray(L.get("W_SPHEV", np.full(S, -1)))   # sphere events' moments (phase 3): the event's index
        if self.sphev.dtype == bool:                                  # (a batch read before phase 3: held back)
            self.sphev = np.where(self.sphev, 0, -1)
        self.law = np.asarray(L.get("W_LAW", np.full((S, K), -1))); self.norm = np.asarray(L.get("W_NORM", np.full((S, K), -1)))
        self.tech = np.asarray(L.get("W_TECH", np.full((S, K), -1))); self.lever = np.asarray(L.get("W_LEVER", np.full((S, K), -1)))
        self.law_neg = np.asarray(L.get("W_LAW_NEG", np.zeros((S, K), bool)))     # a leading minus (v23 W38): the option
        self.norm_neg = np.asarray(L.get("W_NORM_NEG", np.zeros((S, K), bool)))   # goes against the law or norm in force
        self.push = np.asarray(L.get("W_PUSH", np.full((S, K), -1)))
        self._infer_pushes(E, L, S, K)
        self.ssm = WK.LAW_KEYS.index("same-sex marriage")
        self.NI = {k_: i_ for i_, k_ in enumerate(WK.NORM_KEYS_ALL)}
        # a want moment's options that meet the want (the cast member's wish): a mark of helping or coming home, a title
        # or a skill it gives, a bond it makes, or kindness among its values; one marked as a refusal never does
        REFUSE = {"refused someone in need", "turned down a chance", "made an enemy", "broke your word"}
        MEET = {"helped someone in need", "came home"}
        self.meets = np.zeros((S, K), bool)
        for si in np.nonzero(self.want >= 0)[0]:
            for ki, nt in enumerate(L["notes"][si]):
                mk_ = str(nt.get("mark") or "").strip()
                if mk_ in REFUSE:
                    continue
                self.meets[si, ki] = bool(mk_ in MEET or nt.get("title") or nt.get("grants") or nt.get("binds")
                                          or "benevolence" in str(nt.get("v") or ""))
        self.want_s = {}                  # want key -> moments that answer it
        for si in np.nonzero(self.want >= 0)[0]:
            self.want_s.setdefault(WK.CAST_WANTS[int(self.want[si])], []).append(int(si))
        self.pending = {}                 # n -> (cast id, want key, moment) offered this week
        # W40: a pack-made head of government leads the state (the first life to hold it, one state); a minister or head
        # of government can pass a law the norms already point to; a government that falls takes their office with it
        self.self_head = None; self.gov_office = np.zeros(N, bool); self.office_lost = np.zeros(N, bool)
        self.self_lead = float(P.get("world_self_lead", 0.05))   # quarterly pull of the government's colors to the leader's
        self.self_law = {}                # law key -> (life, week) a minister among the lives pushed it (W40)
        self.hist = []                    # monthly, published figures only (Emren 10:09): dict(t, recession, unemp, infl, war, era)
        self._pub = {}                    # the latest published figure per key
        self._rec_i = len(W.record)       # the public record before the birth stays in W.record (the panel's history)
        self._carry = []; self._pp_i = 0  # cast events not yet handed to the engine (the birth's come before the first week)
        self.dis_own = np.zeros(N); self.dis_near = np.zeros(N, bool)   # a disaster in one's town (severity) or a close one's
        self.dis_haz = [None] * N; self.dis_rec = [None] * N   # its hazard (world.HAZARDS) and record entry, where it struck
        self.dis_nhaz = [None] * N                             # the hazard of one in a close person's town
        self._nbw = {}                    # society id -> the neighbour's full World, once a life has gone there (N == 1)
        self.layer2 = float(PP.P["layer_c"][1])   # closeness of the close circle's second layer: "their people"
        self.acc_ = self.accept()
        self.fac = np.ones((N, S)); self.last_ev = self.t0
        self.fire_now = np.zeros((N, S), bool)
        self.fire_why = {}                # moment -> the world's record entry that brought it this week (the reports)
        self.log = []                     # world events while the run lived (JSON-safe, with the character's age)
        self.week_events = []

    def _infer_pushes(self, E, L, S, K):
        """Each option's lever, push domain, target and norm (S, K): as written, else inferred (world-fields.md)."""
        notes = L["notes"]; MARKS = list(L.get("MARKS", [])); MK = np.asarray(L["MARK"])
        at = np.asarray(L.get("W_AT", np.full(S, -1))); who = L.get("W_WHO", [[]] * S)
        sub = L.get("W_PUSH_SUB", {}); COMMIT = np.asarray(L["COMMIT"]); DOM = np.asarray(L["DOM"])
        CL = np.asarray(L.get("CLOSED", np.full((S, K), -1)))
        KN_ = [c_[0] for c_ in E.COMMITMENTS]
        # W40: a moment of national office (its requires: names a minister, the head of government or a member of
        # parliament) acts on the state; a minister's success there passes the law the norms already point to
        self.office_s = np.array([bool(re.search(r"\b(minister|head of government|member of parliament)\b",
                                                 str(L["src"][si].get("requires", "")))) for si in range(S)], bool)
        self.lev_i = np.full((S, K), -1, np.int64); self.dom_i = np.full((S, K), -1, np.int64)
        self.tgt_i = np.full((S, K), None, dtype=object); self.var_i = np.full((S, K), None, dtype=object)
        for si in range(S):
            row = notes[si] if si < len(notes) else []
            for ki in range(min(K, len(row))):
                nt = row[ki] if isinstance(row[ki], dict) else {}
                mk_ = MARKS[MK[si, ki]] if MK[si, ki] >= 0 else ""
                lv = int(self.lever[si, ki])
                if lv < 0:
                    if mk_ in LEVER_MARK:
                        lv = WK.LEVERS.index(LEVER_MARK[mk_])
                    elif nt.get("drops") or str(nt.get("moves", "")).strip().lower() in ("yes", "true", "1"):
                        lv = WK.LEVERS.index("exit")
                    elif CL[si, ki] == 0 and at[si] >= 0:
                        lv = WK.LEVERS.index("subvert")
                if lv < 0:
                    continue
                self.lev_i[si, ki] = lv
                d = int(self.push[si, ki]); tg = sub.get((si, ki))
                if d < 0:
                    if mk_ in NORM_MARK:   # coming out or naming one's gender moves the culture's acceptance of it
                        d = WK.DOMAINS.index("culture"); self.var_i[si, ki] = NORM_MARK[mk_]
                    elif self.office_s[si]:
                        d = WK.DOMAINS.index("state")
                    elif at[si] >= 0:
                        d = WK.DOMAINS.index("institution"); tg = WK.INST_KINDS[int(at[si])]
                    elif self.group[si] >= 0:
                        d = WK.DOMAINS.index("group"); tg = WK.GROUP_KINDS[int(self.group[si])]
                    elif who[si]:
                        d = WK.DOMAINS.index("close"); tg = who[si][0]
                    else:
                        ck = int(COMMIT[si, ki]) if COMMIT[si, ki] >= 0 else (int(np.argmax(DOM[si])) if DOM[si].max() > 0 else -1)
                        dn_, tg = PUSH_COMMIT.get(KN_[ck], ("close", None)) if ck >= 0 else ("close", None)
                        d = WK.DOMAINS.index(dn_)
                self.dom_i[si, ki] = d; self.tgt_i[si, ki] = tg
        # the norm each option is judged by (its norm:, else its law:, else coming out or naming one's gender): a close
        # person's strong objection to it grows into an approval closure (spec 2 §3)
        L2N = np.array([WK.NORM_KEYS_ALL.index(k_) for k_ in WK.LAW_KEYS_ALL] + [-1])   # a law key's norm (W38b keys sit after)
        nk_ = np.where(self.norm >= 0, self.norm, L2N[self.law]).astype(np.int64)
        for si, ki in zip(*np.nonzero((MK >= 0) & (nk_ < 0))):
            m_ = MARKS[MK[si, ki]]
            if m_ in NORM_MARK:
                nk_[si, ki] = WK.NORM_KEYS_ALL.index(NORM_MARK[m_])
        self.nrm_i = np.where(nk_ < len(WK.NORM_KEYS), nk_, -1)   # the W38b keys: close people's objections not kept

    def accept(self):
        """Acceptance per norm key where each person lives and among their own people (N, n_norm), 0 to 1."""
        nv = np.array([float(self.W.norm(k_)) for k_ in WK.NORM_KEYS_ALL])
        ap = np.asarray(self.PP.approval, float)
        ap = np.pad(ap, ((0, 0), (0, len(nv) - ap.shape[1])))   # the W38b keys: no view of their own among one's people
        return _uclip(nv[None, :] + ap, 0, 1)

    # ---- every week, before the engine's week
    def week(self, t, S_):
        W, PP = self.W, self.PP
        self._carry.extend(PP.events[self._pp_i:])   # cast events the engine has not had yet (the birth's, the act's)
        W.tick(self.t0 + t)
        PP.tick(self.t0 + t, S_)
        self._pp_i = 0
        self.harsh_n = np.asarray(W.harsh_loc, float)[PP.loc] if np.ndim(W.harsh_loc) else np.full(self.N, float(W.harsh_loc))
        self._office(t, S_)
        new = [e for e in W.events_since(self.last_ev)] if t > 0 else []
        self.last_ev = int(W.t)
        rec_ = W.record[self._rec_i:]; self._rec_i = len(W.record)   # public only (Emren 10:09): the story and the panel
        self.week_events = [dict(e, age=round(t / 52, 2)) for e in rec_]
        for e in self.week_events:
            if e.get("kind") == "published":
                self._pub[e.get("key")] = e.get("value")
            elif e.get("kind") == "law changed" and e.get("key") in self.self_law:   # W40: the minister's own law
                n_, t_ = self.self_law.pop(e["key"])
                if W.t - t_ <= 26:
                    e["self"] = True; e["by_life"] = n_
            elif e.get("domain") == "nature" and e.get("kind") == "disaster" and isinstance(e.get("value"), dict):
                l_ = int(e["value"].get("loc", -1)); sv_ = float(e["value"].get("severity", 0.5))
                own_ = PP.loc == l_
                for n_ in np.nonzero(own_ & (sv_ >= self.dis_own))[0]:   # the worst strike of the week, as dis_own keeps
                    self.dis_haz[n_] = e.get("key"); self.dis_rec[n_] = e
                self.dis_own = np.where(own_, np.maximum(self.dis_own, sv_), self.dis_own)
                nr_ = ~own_ & (PP.used & PP.lv & (PP.c >= self.layer2) & (PP.mloc == l_)).any(1)
                for n_ in np.nonzero(nr_)[0]:
                    self.dis_nhaz[n_] = e.get("key")
                self.dis_near |= nr_
        if self.gov_office.any() and any(e.get("kind") == "government falls" for e in rec_):
            self.office_lost = self.gov_office.copy()    # the engine ends their minister's or head of government's title
        self.log.extend(e for e in self.week_events if e.get("big") or e.get("domain") in ("era", "state", "abroad", "economy"))
        self.acc_ = self.accept()
        if t % 4 == 0:   # the world's course month by month, as published (for checks and the game's charts)
            self.hist.append(dict(t=int(t), recession=bool(getattr(W, "rec_declared", False)),
                                  unemp=self._pub.get("unemployment"), infl=self._pub.get("inflation"),
                                  war=int(getattr(W, "war", 0)), era=W.era_key))
        # moments the world's events bring this week
        self.fire_now[:] = False; self.fire_why = {}
        for e in new:
            for d, k, key, si, sh, sel in self.wm:
                if e.get("domain") == d and e.get("kind") == k and (key is None or e.get("value") == key or e.get("key") == key):
                    hit_ = PP.rng.random(self.N) < sh
                    if sel == "place":                     # only the people living in the event's place
                        hit_ &= PP.loc == int((e.get("value") or {}).get("loc", -1))
                    elif sel == "staff":                   # only the people who work there
                        hit_ &= self._staff(int((e.get("value") or {}).get("inst", -1)))
                    self.fire_now[:, si] |= hit_
                    self.fire_why[si] = e
        if W.p.get("c3_inst"):
            self._c3_merged(new)
        # wants ripe this week: the moment that answers it, with the cast member in its first who: slot
        self.pending = {}
        for n_, cid_, key_ in PP.want_due(PP.t):
            ss_ = self.want_s.get(key_)
            if ss_ and n_ not in self.pending:
                si_ = ss_[int(PP.rng.integers(len(ss_)))]
                self.pending[n_] = (cid_, key_, si_); self.fire_now[n_, si_] = True
        return self.week_events

    def _staff(self, i):
        """The lives whose own work setting is institution i (N,)."""
        PP = self.PP
        return ((PP.skind == PM.G["work"]) & (PP.sref == i)).any(1)

    def _c3_merged(self, new):
        """C3 merged: the folded firm's staff, lives and cast alike, now work at the bigger one (its slot became a new
        firm), and a quarter of the lives among them face the job-loss rate x3 for a quarter."""
        PP, W = self.PP, self.W
        for e in new:
            if e.get("domain") != "institution" or e.get("kind") != "merged":
                continue
            v = e.get("value") or {}; a, b = int(v.get("inst", -1)), int(v.get("into", -1))
            if a < 0 or b < 0:
                continue
            moved = self._staff(a)
            wk = (PP.skind == PM.G["work"]) & (PP.sref == a)
            PP.sref[wk] = b
            PP.inst[PP.inst == a] = b
            if moved.any():
                if getattr(PP, "c3_jl", None) is None:     # made on the first merger (a world with C3 off saves none)
                    PP.c3_jl = np.zeros(self.N, np.int64)
                hit = moved & (PP.rng.random(self.N) < W._c_par("merge_share"))
                PP.c3_jl = np.where(hit, int(W.t) + 13, PP.c3_jl)

    def drain(self):
        """The cast events since the last call (n, kind, ...), each handed over once: the birth's before the first week,
        the week's own, and those of the act (pushes, wants met or refused)."""
        out = self._carry + list(self.PP.events[self._pp_i:])
        self._carry = []; self._pp_i = len(self.PP.events)
        return out

    def disasters(self):
        """Since the last call: the severity of a disaster in each person's own town (0 none), and whether one struck a
        close person's town (layers 1 and 2). The engine brings the disaster's outside event on these (spec 5 §2)."""
        own, near = self.dis_own.copy(), self.dis_near.copy()
        self.dis_own[:] = 0; self.dis_near[:] = False
        self.dis_haz_now, self.dis_rec_now, self.dis_nhaz_now = self.dis_haz, self.dis_rec, self.dis_nhaz   # this call's,
        self.dis_haz = [None] * self.N; self.dis_rec = [None] * self.N; self.dis_nhaz = [None] * self.N   # for the story
        return own, near

    def story(self, ns, dead):
        """This week's public events for each logged life {n: [entries]}: big ones always, the rest only when they touch
        the character (self=True: their town's disaster, crime wave or election, their own workplace, school or unit)
        or their people (touches=[cast ids] in layers 1 and 2: where they live or work) (Emren 10:42; hooks §2.3)."""
        PP = self.PP; out = {}
        if not self.week_events:
            return out
        INSTK = [WK.GROUP_KINDS.index(g_) for g_ in ("work", "class", "unit", "ward")]
        for n in ns:
            if dead[n]:
                continue
            ks = np.nonzero(PP.used[n] & PP.lv[n] & (PP.c[n] >= self.layer2))[0]
            mine = set(int(x_) for x_ in PP.sref[n][np.isin(PP.skind[n], INSTK) & (PP.sref[n] >= 0)])
            lst = []
            for e in self.week_events:
                v = e.get("value") if isinstance(e.get("value"), dict) else {}
                me, tch = (bool(e.get("self")) and e.get("by_life") == n) or v.get("life") == n, []
                if "inst" in v and e.get("domain") == "institution" and e.get("kind") != "new firm":   # (a new firm
                    i_ = int(v["inst"]); me = me or i_ in mine                     # can reuse a closed one's id)
                    tch = [int(PP.uid[n, k]) for k in ks if int(PP.inst[n, k]) == i_]
                elif "loc" in v and e.get("kind") in LOCAL_SEEN:
                    l_ = int(v["loc"]); me = me or int(PP.loc[n]) == l_
                    if e.get("kind") != "local election":
                        tch = [int(PP.uid[n, k]) for k in ks if int(PP.mloc[n, k]) == l_]
                if e.get("big") or me or tch:
                    lst.append(dict(e, self=me, touches=tch))
            if lst:
                out[n] = lst
        return out

    def _office(self, t, S_):
        W = self.W; self.office_lost = np.zeros(self.N, bool)
        go_ = S_.get("gov_office"); hg_ = S_.get("head_gov")
        self.gov_office = np.zeros(self.N, bool) if go_ is None else np.asarray(go_, bool).copy()
        if hg_ is None:
            return
        hg_ = np.asarray(hg_, bool)
        if self.self_head is not None and not hg_[self.self_head]:
            W._event("state", "head of government", "left office", dict(life=int(self.self_head)), big=True)
            self.self_head = None
        if self.self_head is None and hg_.any():
            self.self_head = int(np.argmax(hg_))
            W._event("state", "head of government", "self", dict(life=self.self_head, party=int(W.gov_party)), big=True)
        if self.self_head is not None and t % 13 == 0:   # the leader's own colors pull the government's
            g_ = np.asarray(W.G, float) + self.self_lead * (np.asarray(S_["w"], float)[self.self_head] - W.G)
            W.G = g_ / g_.sum()

    def law_due(self):
        """The law the norms (and the government's fit) already point away from its state: (key, sign) or None; sign +1
        moves it toward legal, -1 toward banned. A minister passes what the norms support (spec 4, world.push)."""
        W = self.W; p = W.p; NL = len(WK.LAW_KEYS)
        n_ = WM._sig(np.asarray(W.norm_x[:NL], float))
        neff = n_ + p["law_fit"] * ((np.asarray(W.G) - 0.2) @ np.asarray(W.NPROF)[:NL].T)
        tgt = np.where(neff > p["law_cut"][1], 0, np.where(neff > p["law_cut"][0], 1, 2))
        laws = np.asarray(W.laws)
        gap = np.where(tgt != laws, np.minimum(np.abs(neff - p["law_cut"][0]), np.abs(neff - p["law_cut"][1])), -1.0)
        if gap.max() < 0:
            return None
        k = int(np.argmax(gap))
        return WK.LAW_KEYS[k], (1 if tgt[k] < laws[k] else -1)

    def deaths(self):
        """This week's deaths in each person's cast by the engine's roles (N, 5): the engine lives the moment."""
        return np.asarray(self.PP.died)

    def resolve(self, n, s_n, a_n, succ_n, idle_n):
        """After the act: a want the moment answered (met or refused) moves trust and closeness."""
        pv_ = self.pending.get(int(n))
        if pv_ is None or pv_[2] != int(s_n):
            return None
        return self.PP.resolve_want(int(n), pv_[0], pv_[1], bool(self.meets[s_n, a_n]) and not idle_n, succ=bool(succ_n))

    def era(self):
        W = self.W
        return float(W.era_i), np.asarray(W.era_p, float), int(W.era_k)

    # ---- monthly: per person and moment, how the world tilts or gates the moment
    def moment_factor(self, age):
        W, PP, N, S = self.W, self.PP, self.N, self.S
        f = np.ones((N, S))
        if self.toy_on.any():   # time of year: a set season holds the moment to it (x4 there, 0 elsewhere); an inferred
            a_ = np.where(self.toy_set, 1.0, 0.25)                    # tilt keeps a quarter of that (the year's mean stays 1)
            ins_ = self.toy[:, int(W.season)] > 0
            f *= np.where(self.toy_on, (1 - a_) + a_ * 4 * ins_, 1.0)[None]
        if (self.holy >= 0).any():   # a holy day moment comes in the weeks of that day (of the culture's main faith)
            hw_ = W.holy_weeks(); wk_ = int(W.week_of_year)
            for si in np.nonzero(self.holy >= 0)[0]:
                ws_ = hw_.get(WK.HOLY_KEYS[self.holy[si]], set())
                f[:, si] *= (52.0 / max(len(ws_), 1)) if wk_ in ws_ else 0.0
        if self.where.any():   # a place feature the moment needs
            feat = np.asarray(getattr(W, "loc_feat", np.zeros((1, self.where.shape[1]), bool)), bool)[PP.loc]   # N, F
            need = self.where.any(1)
            ok = (feat.astype(np.float32) @ self.where.T.astype(np.float32)) > 0                             # N, S
            f *= np.where(need[None], ok, 1.0)
        if (self.group >= 0).any():   # a setting of that kind the person is in
            ing = (np.asarray(PP.skind)[:, :, None] == np.arange(len(WK.GROUP_KINDS))[None, None, :]).any(1)   # speed pass: one comparison
            gs_ = self.group >= 0
            f[:, gs_] *= ing[:, self.group[gs_]]
        if (self.haunt >= 0).any():   # spheres phase 2: among the regulars of a haunt of that kind (the great gathering:
            hn_ = getattr(PP, "hnt", None)                       # the whole town's); no haunts built, never
            hs_ = np.nonzero(self.haunt >= 0)[0]
            if hn_ is None or getattr(W, "hp_s", None) is None:
                f[:, hs_] = 0.0
            else:
                P_ = W.hp_s.shape[2]; hk_ = np.where(hn_ >= 0, (hn_ // P_) % len(WK.HAUNT_KINDS), -1)   # N x 3
                ok_ = (hk_[:, :, None] == self.haunt[hs_][None, None, :]).any(1) | (self.haunt[hs_] == self.H_GREAT)[None, :]
                f[:, hs_] *= ok_
        if (self.sphev >= 0).any():   # a sphere event's moment: only in a town that had that event in the last year
            se_ = np.nonzero(self.sphev >= 0)[0]
            last_ = getattr(W, "sph_ev_last", None)
            if not W.p.get("sph_events") or last_ is None:
                f[:, se_] = 0.0
            else:
                f[:, se_] *= (int(W.t) - last_[np.asarray(PP.loc)][:, self.sphev[se_]]) <= 52
        if (self.ladder >= 0).any():   # a rung in the moment's sphere (no sphere: any) at least the one it names
            rg_ = getattr(PP, "rung", None)
            ls_ = np.nonzero(self.ladder >= 0)[0]
            if rg_ is None or not getattr(PP, "sph_hr", False):
                f[:, ls_] = 0.0
            else:
                rgm_ = np.where((self.msph[ls_] >= 0)[None, :], rg_[:, np.maximum(self.msph[ls_], 0)], rg_.max(1)[:, None])
                f[:, ls_] *= np.floor(rgm_) >= self.ladder[ls_][None, :]
        if (self.prem >= 0).any():   # a moment that needs a technology the world has not got
            th_ = {}   # speed pass: each technology asked once a week
            for si in np.nonzero(self.prem >= 0)[0]:
                k_ = int(self.prem[si])
                if k_ not in th_:
                    th_[k_] = W.tech_has(WK.TECH_KEYS[k_])
                if not th_[k_]:
                    f[:, si] = 0.0
        self.fac = f
        return f

    def rate_factor(self, held_title_sector):
        """Per person and moment, the world's multiplier on a life event's yearly rate (N, S)."""
        W, PP, N, S = self.W, self.PP, self.N, self.S
        r = np.ones((N, S))
        if getattr(self, "_rk_m", None) is None:   # speed pass: each kind's moments found once (rk never changes)
            self._rk_m = [(k_, nm_, self.rk == k_) for k_, nm_ in enumerate(RK) if (self.rk == k_).any()]
        for k_, nm_, m_ in self._rk_m:
            v_ = W.rate_mult(nm_)
            if nm_ in ("disaster", "crime"):
                v_ = np.asarray(v_, float)[PP.loc][:, None]
            elif nm_ == "jobloss":
                v_ = np.asarray(v_, float)[_uclip(held_title_sector, 0, len(v_) - 1)][:, None]
                v_ = np.where((held_title_sector >= 0)[:, None], v_, float(np.mean(W.rate_mult("jobloss"))))
                if getattr(PP, "c3_jl", None) is not None:   # C3: a merger's quarter of risk
                    v_ = v_ * np.where(PP.c3_jl > W.t, W._c_par("merge_jl"), 1.0)[:, None]
            r[:, m_] *= v_
        ci_ = W.c4_illness() if W.p.get("c4_nature") else None   # C4: bad air or water in the person's place
        if ci_ is not None and self.ill_s.any():
            r[:, self.ill_s] *= ci_[PP.loc][:, None]
        r[:, self.wm_s] = 0.0          # these come on the world's events instead
        return r

    # ---- options: law, norm and technology (world-fields.md)
    def closures(self, s, partner_same, age):
        """Units of closure per option (N, K) by kind: law, approval (norm) and means (technology), and the options
        the world has not got (not offered). A legal option written closed by law is opened (law_open)."""
        W, PP, N = self.W, self.PP, self.N
        K = self.law.shape[1]
        lw = self.law[s]; nm = self.norm[s]; te = self.tech[s]
        u_law = np.zeros((N, K)); law_open = np.zeros((N, K), bool); u_app = np.zeros((N, K)); u_mea = np.zeros((N, K))
        gone = np.zeros((N, K), bool)
        if (lw >= 0).any():
            st_ = np.array([W.law_state(k_) for k_ in WK.LAW_KEYS_ALL])[np.maximum(lw, 0)]   # 0 legal, 1 restricted, 2 banned
            if self.law_neg.any():   # -key: against the law where the act is in force or allowed (evading a call-up)
                st_ = np.where(self.law_neg[s], 2 - st_, st_)
            app_ = lw >= 0
            app_ &= (lw != self.ssm) | partner_same[:, None]      # same-sex marriage's law binds a same-sex couple only
            u_law = np.where(app_, np.where(st_ == 2, 1.0, np.where(st_ == 1, 0.5, 0.0)), 0.0)
            law_open = app_ & (st_ == 0)
        if (nm >= 0).any():
            acc_ = self.acc_                                        # N, n_norm: society's norm with the close circle's view
            a_ = np.take_along_axis(acc_, np.maximum(nm, 0), 1)
            if self.norm_neg.any():   # -key: frowned on where the norm is accepted (snubbing a same-sex partner)
                a_ = np.where(self.norm_neg[s], 1 - a_, a_)
            u_app = np.where(nm >= 0, 2.0 * (1 - a_), 0.0)
        if (te >= 0).any():
            for k_ in np.unique(te[te >= 0]):
                key = WK.TECH_KEYS[k_]
                if not W.tech_has(key):
                    gone |= te == k_
                else:
                    ad_ = np.array([W.tech_adopt(key, cls=int(c_)) for c_ in range(3)])[_uclip(PP.cls, 0, 2)]
                    u_mea = np.maximum(u_mea, np.where(te == k_, 1 - ad_[:, None], 0.0))
        return u_law, law_open, u_app, u_mea, gone

    # ---- the person's role and acceptance with the world on (N1b, outer world round 3)
    def role_norms(self):
        PP, W = self.PP, self.W
        ap_ = self.acc_
        rs_ = 1 - ap_[:, self.NI["role crossing"]]
        at_ = ap_[:, self.NI["transition"]] * float(np.asarray(W.rights)[WM.RIGHTS.index("sexuality")])
        return rs_, at_

    # ---- the channels the engine reads (package §5), each 1 or 0 at an ordinary person in an ordinary modern world
    def climate(self):
        """How hostile the place and one's people are to being out (N,): 0 at or above modern Earth's start (acceptance
        of coming out .70 x the sexuality right .73 after the 80-year burn-in, seeds 1-8), up to 1 where neither holds.
        A faith's community is in the local norms already, so the engine adds no faith term with the world on."""
        a_ = self.acc_[:, self.NI["coming out"]] * float(np.asarray(self.W.rights)[WM.RIGHTS.index("sexuality")])
        return _uclip((CLIM_REF - a_) / CLIM_REF, 0, 1)

    def channel_rates(self):
        """Per person and moment (N, S): a close person's divorce or quitting makes one's own likelier for a while
        (contagion, spec 2 §3), and the wish to move (move_wish, spec 3 §2.6: after a partnership starts or ends, where
        work is scarce) scales the moving moments against an ordinary person of that age."""
        PP = self.PP; r = np.ones((self.N, self.S))
        ct = getattr(PP, "contagion", None) or {}
        if self.div_s.any() and "divorce" in ct:
            r[:, self.div_s] *= np.asarray(ct["divorce"], float)[:, None]
        if self.quit_s.any() and "quit" in ct:
            r[:, self.quit_s] *= np.asarray(ct["quit"], float)[:, None]
        if self.move_s.any():
            ma_ = PP.P["move_age"]
            base = np.interp(PP._age(PP.t), [a_ for a_, _ in ma_], [r_ for _, r_ in ma_]) / 52.0
            mw_ = np.broadcast_to(np.asarray(PP.move_wish(), float), (self.N,))
            r[:, self.move_s] *= _uclip(mw_ / max(float(base), 1e-9), 0.5, 3.0)[:, None]
        return r

    def reach_pull(self, s):
        """(N, K) pull toward voice and subvert at institutions and the outer rings by felt reach (spec 7 §6): what makes
        a character vote, petition or organise. Zero at a felt reach of 0.75 (one of many who still count)."""
        lv = self.lev_i[s]; dm = self.dom_i[s]
        on = _isin_small(lv, [WK.LEVERS.index("voice"), WK.LEVERS.index("subvert")]) & (dm >= 0)
        if not on.any():
            return 0.0
        ring = np.where(dm >= 0, PM.RING_OF[np.maximum(dm, 0)], 0)
        on &= ring >= 2
        fr = np.take_along_axis(np.asarray(self.PP.felt_reach, float), ring.astype(np.intp), 1)
        return np.where(on, REACH_K * (fr / 3.0 - 0.25), 0.0)

    def odds(self, s):
        """(N, K) added to the options' difficulty (DIFF units; the engine's gain 3 turns .1 into about a third of an
        odds ratio): finding a job by the local unemployment (matching elasticity .5), a place in education by the
        local university's capacity and its openness to the person's class, an illness's acts by the hospitals'
        capacity there. 0 at the burn-in's typical world."""
        d = np.zeros((self.N, self.job_o.shape[1]))
        for v_ in self.odds_parts(s).values():
            d += v_
        return d

    def odds_parts(self, s):
        """odds() by cause, {"unemployment", "university places", "hospital places": (N, K)}, only those that apply."""
        W, PP = self.W, self.PP; N = self.N
        out = {}
        jo, ao = self.job_o[s], self.adm_o[s]
        if jo.any():
            ul = np.asarray(getattr(W, "loc_unemp", np.full(PP.n_loc, U_REF)), float)[PP.loc]
            out["unemployment"] = jo * _uclip(0.5 * np.log(np.maximum(ul, 0.5) / U_REF) / 3.0, -0.15, 0.25)[:, None]
        if ao.any() or self.ill_s[s].any():
            cap = np.asarray(W.inst_capacity, float); kd = np.asarray(W.inst_kind); il = np.asarray(W.inst_loc)
            def local(kind, v):   # the mean over that kind's institutions in each person's town, else the country's
                m_ = kd == WK.INST_KINDS.index(kind)
                if not m_.any():
                    return np.ones(N)
                tot = np.bincount(il[m_].astype(np.intp), weights=v[m_], minlength=PP.n_loc)
                cnt = np.bincount(il[m_].astype(np.intp), minlength=PP.n_loc)
                return np.where(cnt[PP.loc] > 0, tot[PP.loc] / np.maximum(cnt[PP.loc], 1), v[m_].mean())
            if ao.any():
                oc = np.asarray(W.inst_open_cls, float)[:, _uclip(PP.cls, 0, 2)]   # n_inst, N: openness to each one's class
                uni = kd == WK.INST_KINDS.index("university")
                op_ = oc[uni].mean(0) if uni.any() else np.full(N, OPEN_REF)
                f_ = local("university", cap) / CAP_REF * op_ / OPEN_REF
                out["university places"] = ao * _uclip(-np.log(np.maximum(f_, 0.1)) / 3.0, -0.15, 0.2)[:, None]
            if self.ill_s[s].any():
                f_ = local("hospital", cap) / CAP_REF
                out["hospital places"] = self.ill_s[s][:, None] * _uclip(-0.5 * np.log(np.maximum(f_, 0.1)) / 3.0, -0.1, 0.2)[:, None]
        return out

    # ---- other societies (spec 5 §5; Emren 10:30 "Yes, fully")
    def on_title(self, n, name):
        """A title the engine just gave life n that moves it between societies or changes its standing there."""
        PP = self.PP
        if not hasattr(PP, "soc"):
            return
        abroad = int(PP.soc[n]) != int(PP.soc_home[n])
        if name in MIGRATE_T and not abroad:
            self.emigrate(n)
        elif name == "returned migrant" and abroad:
            self.return_home(n)
        elif name in CITIZEN_T and abroad:
            PP.set_status(n, "citizen")
        elif name == "second language":
            PP.lang_boost(n, 0.5)

    def emigrate(self, n):
        """Life n leaves for a neighbour, drawn toward the richer ones at peace (spec 5 §5). With one life the neighbour
        becomes a full World (spawned once, kept for a return) and the link reads it from then on."""
        W, PP = self.W, self.PP
        nx = int(getattr(W, "n_ext", 0))
        if nx <= 0:
            return None
        soc = np.asarray(getattr(W, "ext_society", np.arange(nx) + 1), int)
        rich = np.asarray(getattr(W, "ext_rich", np.ones(nx)), float)
        rel = np.asarray(getattr(W, "ext_relation", np.full(nx, 2)), float)
        wt = np.maximum(rich, 0.05) * np.where(rel > 0, 1.0, 0.1) * (soc != int(PP.soc[n]))
        if wt.sum() <= 0:
            return None
        k = int(PP.rng.choice(nx, p=wt / wt.sum())); sid = int(soc[k])
        if self.N == 1:
            W_new = self._nbw.get(sid)
            if W_new is None:
                W_new = W.spawn_neighbour(k); self._nbw[sid] = W_new
            loc = PP.emigrate(n, W_new=W_new)
        else:
            loc = PP.emigrate(n, society_id=sid)
        self._rebind()
        return loc

    def return_home(self, n):
        loc = self.PP.return_home(n)
        self._rebind()
        return loc

    def move(self, n, local, why=None):
        """A move the engine made: coming home from abroad goes back to the home society; any other is a move here."""
        PP = self.PP
        if why == "came home" and hasattr(PP, "soc") and int(PP.soc[n]) != int(PP.soc_home[n]):
            return self.return_home(n)
        return PP.move(int(n), local=local, why=why, t=PP.t)

    def _rebind(self):
        """After a switch of World (one life abroad or back): read the new one from its present on."""
        if getattr(self.PP, "W", self.W) is not self.W:
            self.W = self.PP.W
            if int(self.W.t) < int(self.PP.t):   # the World left behind ran on without the life: catch it up quietly
                self.W.tick(int(self.PP.t))
            self._rec_i = len(self.W.record); self.last_ev = int(self.W.t)
        self.acc_ = self.accept()

    def group_time(self, held, com, fai):
        """(N,) added to free time (package §5, time from the settings' time shares): the shares of one's clubs, scenes,
        online communities, gangs and movements, and a congregation one goes to without the faith commitment, less what
        the commitments already count (community: its largest group; faith: the congregation; career: work), against
        the typical life's (TIME_REF), so 0 at the typical world."""
        PP = self.PP; sk = np.asarray(PP.skind); ts = np.where(sk >= 0, np.asarray(PP.sts, float), 0.0)
        vk = _isin_small(sk, [PM.G[g_] for g_ in ("club", "scene", "online", "gang", "movement")])
        vs = np.where(vk, ts, 0.0)
        cg = np.where(sk == PM.G["congregation"], ts, 0.0).sum(1)
        extra = vs.sum(1) - np.where(held[:, com], vs.max(1), 0.0) + np.where(held[:, fai], 0.0, cg)
        return -(extra - TIME_REF)

    def safety(self):
        """What the place adds to the safety need's supply (N,): crime there, a war, a disaster's aftermath."""
        p = self.safety_parts()
        return p["crime"] + p["war"] + p["disaster"]

    def safety_parts(self):
        """safety() by cause, {"crime", "war", "disaster": (N,)}."""
        W, PP = self.W, self.PP
        cr = np.asarray(W.loc_crime, float)[PP.loc]; ds = np.minimum(np.asarray(W.loc_disaster, float)[PP.loc], 1)
        return {"crime": -0.5 * (cr - CRIME_REF), "war": -(0.15 * float(getattr(W, "war", 0) > 0)) + np.zeros(self.N),
                "disaster": -(0.15 * ds)}

    def resources(self, employed):
        """What the world adds to the targets the engine's resources drift to (money, freedom), (N,) each: rent where
        housing is dear for those without a home of their own, prices eating a fixed income, the welfare floor for those
        out of work, the rights there are. 0 at the burn-in's typical world."""
        p = self.resources_parts(employed)
        return p["housing"] + p["prices"] + p["welfare"], p["rights"]

    def resources_parts(self, employed):
        """resources() by cause: money from "housing" (rent), "prices" and "welfare" (the floor), freedom from
        "rights", each (N,)."""
        W, PP = self.W, self.PP
        rent = -0.05 * float(_uclip(W.housing, -1, 1)) * ~np.asarray(PP.own_home, bool)
        inf_ = self._pub.get("inflation"); inf_ = INFL_REF if inf_ is None else float(inf_)
        price = -0.004 * _uclip(inf_ - INFL_REF, -5, 15) * ~np.asarray(employed, bool)
        floor = 0.15 * (float(W.welfare) - WELF_REF) * ~np.asarray(employed, bool)
        free = np.full(self.N, 0.2 * (float(np.mean(W.rights)) - RIGHTS_REF))
        return {"housing": rent, "prices": price, "welfare": floor, "rights": free}

    def wl2_parts(self, employed):
        """WL2 (world-in-life.md), the small effects the world was missing, added to the targets the resources drift to,
        each (N,) and 0 in a calm world: money from "prices_work" (prices eat a wage too, as wages lag), "recession"
        (fewer hours and no raise for those who keep their job, twice in a severe one) and "disaster" (a disaster in
        their own town costs money); freedom from "rec_hours" (the hours cut give a little time back) and
        "disaster_time" (time spent clearing up); ties from "pandemic" (a lockdown cuts time with people)."""
        W, PP, k = self.W, self.PP, WL2_PAR
        emp = np.asarray(employed, bool)
        inf_ = self._pub.get("inflation"); inf_ = INFL_REF if inf_ is None else float(inf_)
        rec = float(getattr(W, "phase", 0) == 1) * (2.0 if getattr(W, "severity", 0) == 2 else 1.0)
        ds = np.minimum(np.asarray(W.loc_disaster, float)[PP.loc], 1)
        lock = float(getattr(W, "lockdown", 0.0))
        return {"prices_work": -k["price_work"] * 0.004 * _uclip(inf_ - INFL_REF, -5, 15) * emp,
                "recession": -k["rec_money"] * rec * emp, "rec_hours": k["rec_free"] * rec * emp,
                "disaster": -k["dis_money"] * ds, "disaster_time": -k["dis_free"] * ds,
                "pandemic": -k["pand_tie"] * lock + np.zeros(self.N)}

    def cause(self, kind, years=5, key=None):
        """The world behind an effect of `kind` (CAUSE_REC), for the game's hover: the latest public record entry of
        that kind in the last `years` years (domain, kind, key, the character's age then), else None; with key, only
        an entry about that key (a law's own change)."""
        want = CAUSE_REC.get(kind, ())
        if not want:
            return None
        lim = int(self.W.t) - 52 * years
        for e in reversed(self.W.record):
            if int(e.get("t", 0)) < lim:
                break
            if any(e.get("domain") == w_[0] and e.get("kind") == w_[1] and (len(w_) < 3 or str(e.get("key") or "").startswith(w_[2]))
                   for w_ in want) and (key is None or e.get("key") == key):
                return dict(domain=e.get("domain"), kind=e.get("kind"), key=e.get("key"),
                            age=round((int(e["t"]) - self.t0) / 52, 2))
        return None

    # ---- after the act
    def on_act(self, live, s, a, ma, succ, L, marks_defied=None):
        """The acts of this week: the close circle judges each (and objects by the act's norm), and an act with a lever
        pushes where it lands (written or inferred in _infer_pushes). Returns the push results, one per push."""
        idx = np.nonzero(live)[0]
        if not len(idx):
            return []
        si_, ai_ = s[idx], a[idx]
        out = self.PP.on_act(idx, ma[idx], succ[idx].astype(float), lever=self.lev_i[si_, ai_], pushes=self.dom_i[si_, ai_],
                             target=self.tgt_i[si_, ai_], norm=self.nrm_i[si_, ai_], var=self.var_i[si_, ai_], t=self.PP.t)
        res = out.get("results", []) if isinstance(out, dict) else []
        hp_ = self.hpick[si_] & (succ[idx] > 0) & (self.osph[si_, ai_] >= 0) & (self.ocol[si_, ai_] >= 0)
        if hp_.any() and getattr(self.PP, "sph_h", False):   # the haunt choice (N1): the option's face picks the place
            for n_, s2_, a2_ in zip(idx[hp_], si_[hp_], ai_[hp_]):
                self.PP.pick_haunt(int(n_), int(self.osph[s2_, a2_]), int(self.ocol[s2_, a2_]))
        mn_ = self.gov_office[idx] & self.office_s[si_] & (succ[idx] > 0)
        if mn_.any():   # W40: a minister's success in office passes the law the norms already point to (it lands, or
            ld_ = self.law_due()   # not, at the world's next quarter; the record shows it as the character's if it does)
            if ld_ is not None:
                for n_ in idx[mn_]:
                    self.W.push("state", ld_[0], 2.0, ld_[1])
                    self.self_law[ld_[0]] = (int(n_), int(self.W.t))
        return res

    def option_levers(self, si):
        """Each option of moment si: None, or dict(lever, target) (target: the domain, or 'domain sub-kind'), for the
        game's icons (hooks §2.6). An empty list when no option pushes."""
        K_ = min(len(self.L["labels"][si]), self.lev_i.shape[1])
        out = []
        for ki in range(K_):
            lv = int(self.lev_i[si, ki])
            if lv < 0 or self.dom_i[si, ki] < 0:
                out.append(None); continue
            d = WK.DOMAINS[int(self.dom_i[si, ki])]; tg = self.tgt_i[si, ki]
            out.append(dict(lever=WK.LEVERS[lv], target=d if tg is None else f"{d} {tg}"))
        return out if any(x_ is not None for x_ in out) else []

    def who(self, n, si):
        """{slot: cast id} for the moment's who: slots (the game names them); a want's holder takes the first slot."""
        sl_ = list(self.L.get("W_WHO", [[]] * self.S)[si])
        if not sl_:
            return None
        pv_ = self.pending.get(int(n))
        first_ = pv_[0] if pv_ is not None and pv_[2] == si else None
        out = self.PP.fill(int(n), sl_[1:] if first_ is not None else sl_)
        if first_ is not None:
            out = {sl_[0]: int(first_), **out}
        return {k_: int(v_) for k_, v_ in out.items()}

    def output(self, log_lives, w=None):
        """What the run hands the game: the world's log and public state, its save, and each logged life's people."""
        PP = self.PP
        snap = self.W.snapshot()
        snap["gov"]["leader_self"] = self.self_head is not None and int(self.self_head) in [int(i) for i in log_lives]
        others = {int(k_): W_.save() for k_, W_ in (getattr(PP, "_Ws", None) or {}).items() if W_ is not self.W}
        return dict(t0=self.t0, record=list(self.W.record), log=self.log, hist=self.hist, snapshot=snap,
                    save=self.W.save(), saves_other=others, people={int(i): PP.save(int(i)) for i in log_lives},
                    cast={int(i): PP.cast_view(int(i)) for i in log_lives},
                    place={int(i): PP.place_view(int(i)) for i in log_lives},
                    settings={int(i): PP.settings_view(int(i)) for i in log_lives},
                    reach={int(i): PP.reach_view(int(i)) for i in log_lives},
                    figures={int(i): PP.figure_view(int(i)) for i in log_lives})   # public figures as the life reads them

    def save(self, n):
        return dict(world=self.W.save(), people=self.PP.save(n))
