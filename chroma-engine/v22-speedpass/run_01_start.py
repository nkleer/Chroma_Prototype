# run_01_start.py: part 1 of 18 of engine._run, the life loop.
# The signature, the settings, the random streams, the times (eras) and their messages.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
def _run(N=1000, years=80, seed=0, P=None, record_every=52, intervention=None, lib=None, log_lives=(), pausing=False):
    # the whole simulation; run() and run_steps() below call it. With pausing=True it pauses six times a week
    # (PAUSES); with pausing=False it never pauses and runs exactly as run() always did.
    P = {**DEFAULT, **(P or {})}
    NMAP = NMAP_V6 if P["aut_self"] else NMAP_V5
    SP_ = np.asarray(P["stage_p"], float) if P["stage_p"] is not None else STAGE_P    # plasticity by life stage
    rng = np.random.default_rng(seed)
    L = lib if lib is not None else LIB
    FR = FRAMINGS[P["framing"]] if isinstance(P["framing"], str) else np.asarray(P["framing"], float)
    FRpos = np.maximum(FR, 0)
    # default ends: serve your method colors, and (only if the culture frames them as
    # opposed) work against the opposed colors
    FRN_ = P["framing"] if isinstance(P["framing"], str) else None
    in_fr = lambda key: P[key] is None or FRN_ is None or FRN_ in P[key]   # a custom matrix keeps both
    Eeff = L["E"] if not in_fr("ends_frames") else \
        np.where(L["OVR"][..., None], L["E"], L["E"] - 0.25 * np.einsum("ij,skj->ski", FRpos, L["M"]))
    MU_ = P["mu"] if in_fr("drift_frames") else 0.0
    T = years * 52
    z = np.zeros((N, C)); k = np.zeros((N, C)); v = np.zeros((N, C))
    M = np.zeros(N); D = np.zeros((N, C)); J = np.zeros((N, C, C))
    sig = np.full((N, C), 0.3); SE = np.full((N, C), 0.5)
    need = np.full((N, NJ), 0.6); fb = np.zeros((N, C))
    nimp = np.ones((N, NJ))                                 # v6: how much each need matters to the person (accommodation)
    nic = np.tile(P["world_profile"], (N, 1)).astype(float)
    if P["family_conc"]:   # v6: each child is born into a family with its own ways (the person still starts at 0.2 each)
        wp_ = np.asarray(P["world_profile"], float); wp_ = wp_ / wp_.sum()
        nic = rng.dirichlet(P["family_conc"] * C * wp_, N)
    turn_pm = np.exp(rng.uniform(np.log(P["turn_spread"][0]), np.log(P["turn_spread"][1]), N))   # v6: rooted vs mobile lives
    circle = nic.copy()                                       # v6: the mix the people currently around you bring
    fam = nic.copy()                                          # v7: the family's own ways (whom a child first admires)
    stress = np.zeros(N); habit = np.zeros((N, C)); B = np.zeros(N)
    y = np.zeros((N, C))                     # aspiration log-ratios (who the person wants to be)
    res = np.tile(np.asarray(P["res0"], float), (N, 1))
    hh_res0 = res[:, RIDX["money"]].copy()                  # F3, world off: the start's means are the household's level
    held = np.zeros((N, NK), bool); I = np.zeros((N, NK)); prof = np.full((N, NK, C), 0.2)
    sat = np.full((N, NK), 0.6); since = np.zeros((N, NK)); pension = np.zeros(N)
    LOAD = np.array([c[1] for c in COMMITMENTS]); KPAY = np.array([parse(c[2], NIDX, NJ) for c in COMMITMENTS])
    FREE_STAGE = np.asarray(P["freedom_stage"], float)
    IMP_FREE = np.minimum(L["IMP"][:, NIDX["autonomy"]], 0)    # impositions on autonomy also take freedom
    BEREAVE = np.array([nm == "bereavement" for nm in L["names"]])
    EXIT = parse("R.5 U.3 B.2"); EXIT /= EXIT.sum()
    EXITW = np.asarray(P["exit_weight"], float)            # leaving children costs far more than leaving a club
    RATE = L["RATE"] * np.where(np.array(L["names"]) == "an ordinary week", P["ordinary_w"], 1.0)
    CP = np.asarray(P["commit_p"], float); retired = np.zeros(N, bool); faith_given = np.zeros(N, bool)   # raised in the faith they hold
    left_given = np.zeros(N, bool); faith_drifted = np.zeros(N, bool)   # left the faith they were raised in; drifted, not decided
    drift_now = np.zeros(N, bool)                         # this week's quiet endings of a faith (read by end)
    sit_n = np.zeros((N, L["S"]), np.int32); lev_log = []
    ev_pm = np.exp(rng.uniform(np.log(P["ev_spread"][0]), np.log(P["ev_spread"][1]), (N, L["S"])))   # personal event rates
    ev_last = np.full((N, L["S"]), -10 ** 6); DRV = L["DRV"]
    PERY = L["PERY"]; EVERYDAY = (PERY.sum(1) == 0) & L["STG"].any(1)     # v6: life events vs everyday situations
    if P["ev_fit"] or P["ill_real"]:   # F9: life events fitted to Release's rows; the body's and mind's at their real rates
        rn_ = np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]
        PERY = PERY.copy()
        for nm_, f_ in (P["ev_fit"] or {}).items():   # a factor, or one per stage
            PERY[rn_ == nm_] *= np.asarray(f_, float)
        if P["ill_real"]:   # Emren's event_scale makes big life events a little more often; illness keeps its real rate
            PERY[np.isin(rn_, list(BODY_MOMENTS) + list(MIND_MOMENTS))] /= P["event_scale"]
    REG_ = (EVERYDAY & (L["RATE"] >= 1) & ~np.asarray(L.get("INNER", np.zeros(L["S"], bool)), bool)
            & ~np.asarray(L.get("ECHO", np.zeros(L["S"], bool)), bool))       # ordinary everyday moments (not title or joining ones)
    CAR, PAR, KID, COM, FAI = KIDX["career"], KIDX["partner"], KIDX["children"], KIDX["community"], KIDX["faith"]
    clash0 = np.full((N, NK), -1); clashI = np.zeros((N, NK)); clash_by = np.full((N, NK), -1); clash_log = []
    MON, TIM, HEA, TIE, FRE = (RIDX[r] for r in ("money", "time", "health", "ties", "freedom"))
    commit_log = []; R_hist = []; K_hist = []
    birth_log = []   # each child a life gains (n, week, moment, option): the first, or one more while there are children
    plast = np.zeros(N); ctrl = np.zeros(N)
    fhz = np.zeros(N); hz_mem = np.zeros(N); hea_last = np.full(N, -1.0)   # v7 felt horizon: limited time felt, reminders
    dsc = np.ones(N)                                     # v7 discipline: self-control learned from plans kept and broken
    CUR_ON = bool(P["cur_on"]); cur_sum = np.zeros(N); cur_m = None   # item 12: the steady current, and how much it moved each life
    SHON = bool(P["shadows"]) and (bool(P["sh_world"]) or not bool(P["world"])); SHG_ = np.asarray(P["sh_gain"], float)
    NM_ON = bool(P["nm_on"])   # P4: each person's own colour-to-need table (needs x colours), from the shared one
    NMP = np.repeat(NMAP[None], N, 0); NM_TOT = NMAP.sum(0); NM_LO = P["nm_band"][0] * NMAP; NM_HI = P["nm_band"][1] * NMAP
    CU_ON = bool(P["curious"]); asked = np.zeros(N)   # item 7: how much others come to them for answers (C4)
    NA_OUT = len(ADJ_ALL) if SHON else ADJ_BASE   # the adjectives the outputs carry
    DOM_ON = bool(P["domains"]); NA_D = len(AREAS)
    Dz = np.zeros((N, NA_D, C)); D_hist = []   # v23 life domains: each area's offset on the colors (log-ratio units)
    # light and shadow: the shadow part s (shS), its force e (shA), the four sources (sh_src: holding on, ruling, no
    # counterweight, strain), whether the person has seen it (a reflection met), the last reflection and breakthrough
    shS = np.zeros((N, C)); shA = np.zeros((N, C)); sh_src = np.zeros((N, C, 4)); sh_seen = np.zeros((N, C), bool)
    sh_rt = np.full((N, C), -10 ** 7); sh_brk = np.full(N, -10 ** 7); sh_n = np.zeros((N, C), int); sh_log = []
    ENEMY_B = ENEMY > 0
    # the colours over the last ten years, each quarter (pair and insight moments: a colour's rise, how long it has held)
    w_q = np.full((40, N, C), 0.2); w_qi = 0
    HZT = HZ_TILT if P["hz_tilt"] is None else (parse(P["hz_tilt"]) if isinstance(P["hz_tilt"], str) else np.asarray(P["hz_tilt"], float))
    HZW = np.maximum(HZT, 0) / max(np.maximum(HZT, 0).sum(), 1e-9)   # where a short horizon pulls the want
    V_hist = {k_: [] for k_ in ("acc", "chan", "core", "wound", "support", "trouble", "fortune", "habit", "role", "SE", "ctrl", "plast", "Q", "doors", "content", "peace", "skill", "fneed", "mood", "stress", "cload", "tension",
                                       "react", "steady", "base_mood", "outlook", "gap",
                                       "n_dream", "n_passion", "n_plan", "harmonious", "regret", "horizon", "discipline", "n_titles", "n_perks", "lvl", "q_rel", "need", "unmet", "hope_w", "adj", "adj_v", "threat", "scar")}   # for the color vectors (Emren, 2026-10-04)
    CTRL = np.asarray(P["ctrl_stage"], float)
    gates = np.zeros((NS, 14))                # per stage: events, wanted-best unavailable, unnoticed, pulled away, tried, tried+succeeded,
                                             # want and pull disagree (both options seen), want won that conflict,
                                             # same two when the person wants to change (gap > 0.1), same two under high stress (> 1),
                                             # wanted-best closed by missing resources, closed by the niche
    stage = np.zeros(N, int); eps_k = np.full(N, P["eps_core"])
    tw_held = tw_has = None                   # what was held last week, for transition windows
    TWo = np.zeros(N)                         # an open window of its own (tw_sep), on the same half-life as openness
    chan = np.zeros((N, len(CHANNELS), C))
    conv_log = []; rite_log = []
    Q = np.zeros(N); brk_log = []; force_re = np.zeros(N, bool)   # pent-up demand and breakthroughs
    tries = np.zeros(N); wins = np.zeros(N); blocked = np.zeros(N)                 # wanted attempts, successes, wanted options closed
    lvl = np.full(N, 0.6); mood = np.zeros(N); content = np.full(N, 0.6); peace = np.full(N, 0.6)   # meta variables
    hold = np.full((N, C), 0.2)
    gap_r = np.zeros(N); q_rel = np.zeros(N); unmet = np.zeros(N); hzf = np.zeros(N)
    NA_ = len(ADJ_ALL); adj = np.zeros((N, NA_), bool); adj_since = np.zeros((N, NA_)); adj_log = []   # v7 adjectives
    adj_v = None
    ADJ_SIDE = np.array([a_[3] for a_ in ADJ_ALL], float); ADJ_ON = np.array([a_[4] for a_ in ADJ_ALL])
    ADJ_OFF = np.array([a_[5] for a_ in ADJ_ALL]); ADJ_AGE = np.array([a_[6] for a_ in ADJ_ALL], float)
    SMID = np.asarray(P["sat_mid_stage"], float) - 0.8 + P["sat_mid"]
    smid = np.full(N, SMID[0]); hope = lvl + P["hope_young"]   # v7: what counts as enough now; what life is hoped to give
    RST = None if P["r_stage"] is None else np.asarray(P["r_stage"], float)
    TST = np.asarray(P["T_stage"], float); RR = np.asarray(P["r_ref"], float); TON = 1.0 if P["temperament"] else 0.0
    react = np.ones(N); steady = np.zeros(N); base_mood = np.full(N, P["base_ref"]); outlook = np.full(N, P["o_ref"])   # temperament
    # the outside world: one shared history of eras, and personal events
    hist = make_history(P, years, seed)
    era_p = np.zeros((T + 1, C)); era_i = np.zeros(T + 1); era_k = np.zeros(T + 1, int); era_at = {}
    for a0, a1, key, inten, kind in hist:
        era_p[a0:a1] = COMBO_MIX[key]; era_i[a0:a1] = inten; era_k[a0:a1] = ERA_KINDS.index(kind); era_at[a0] = (key, inten, kind)
    ev_log = []
    def accept(idx, msg, social):
        """How person idx takes a message (+1 embraces it, -1 pushes back): fit with mindset, discontent,
        openness, group lean (for social sources), and how strongly they hold what it would take."""
        lens = softmax(k[idx]); wi = softmax(z[idx])
        fit = 5 * (lens * msg).sum(1) - 1
        give = np.maximum(0, wi - msg); give /= np.maximum(give.sum(1, keepdims=True), 1e-9)
        holdp = 5 * (give * hold[idx]).sum(1)
        return np.tanh(P["acc0"] + P["acc_fit"] * fit + P["acc_disc"] * (0.55 - content[idx]) + P["acc_open"] * np.minimum(B[idx], 2) / 2
                       + P["acc_conf"] * social * (wi @ GROUP) - P["acc_hold"] * (holdp - 1))
    def take_in(idx, msg, amt, src_i):
        """A taken message moves the want, and a little of the motives (felt experience)."""
        dy = P["ev_eta"] * amt[:, None] * centre(5 * (msg - softmax(y[idx])))
        y[idx] += dy; asrc[idx, src_i] += dy
        dz = P["ev_z"] * (plast[idx] * amt)[:, None] * centre(5 * (msg - softmax(z[idx])))
        pk_ = P["era_push_k"] if src_i == 8 else P["ev_push_k"]   # played lives: the game weighs outside pushes
        if pk_ != 1.0:
            dz = pk_ * dz
        z[idx] += dz; chan[idx, 8] += dz
    def sac_fx(n, ev_):
        """S5 (chroma-ideas/social-mechanics.md): what an offer, tragic trade-off or amends does in the engine. Held: the
        money and ties not had. Crossed: a moral injury (stress), a seed in the line colour's shadow part (with shadows)
        and a turning point's lesson toward the act's ways (the game's item 4 pick at its full "toward" kind: piv x
        plasticity x (1 + piv_far x distance), piv_core of it to the deep core). Healed: stress eased."""
        sp_ = WL.PP.sac_par
        res[n, MON] -= ev_.get("money", 0.0); res[n, TIE] -= ev_.get("ties", 0.0)
        if ev_.get("crossed"):
            stress[n] += ev_["wound"]
            if SHON:
                for c_ in ev_["colours"]:
                    shS[n, c_] = min(1.0, shS[n, c_] + ev_["seed"])
            T_ = np.maximum(ma[n], 0)
            if T_.sum() > 0 and sp_["piv"] and not ev_.get("quiet"):
                T_ = T_ / T_.sum(); w_ = softmax(z[n]); d_ = 0.5 * np.abs(T_ - w_).sum()
                dz_ = sp_["piv"] * plast[n] * (1 + sp_["piv_far"] * d_) * centre(5 * (T_ - w_))
                z[n] += dz_; k[n] += sp_["piv_core"] * dz_; chan[n, 7] += dz_
        if ev_.get("healed") or ev_.get("what") == "healed":
            stress[n] = max(0.0, stress[n] - ev_.get("heal", sp_["heal"]))
    def inst_expo():
        return 0.5 + 0.5 * held[:, CAR] + 0.3 * held[:, COM]
    def era_expo(kind):
        """Who an era reaches: a policy reaches everyone, institutions reach those inside them (work, community),
        a cosmology (a religious or ideological era) reaches the faithful most."""
        return [0.8 + 0.2 * held[:, CAR], inst_expo(), 0.4 + held[:, FAI] * (0.6 + I[:, FAI])][kind]
    f_need = np.full(N, 0.8); cload = np.zeros(N); tension = np.zeros(N)
    asrc = np.zeros((N, len(ASOURCES), C)); A_src = []          # what moved the want, by source (cumulative)
    asrc_c = asrc[log_lives[0]] if len(log_lives) else None   # the played life's (a view: it moves with asrc)
    NW_ON = bool(P["need_why"])   # need_why: why each need moved this week, by source (a record only, never a draw)
    (NW_ACT, NW_FADE, NW_SET, NW_OUT, NW_READ, NW_LOSS, NW_MEANS, NW_COMMIT, NW_TITLE, NW_CARE, NW_GOAL, NW_PEOPLE, NW_AGE,
     NW_PLAYER) = range(len(NSOURCES))
    nw = np.zeros((N, len(NSOURCES), NJ)) if NW_ON else None   # this week's need moves so far, by source
    nw_imp = np.full(N, -1) if NW_ON else None                 # this week's silent setback (IMPOSITIONS index), -1 none
    nw_prev = need.copy() if NW_ON else None                   # needs at the last mark
    def nw_mark(k_):
        """need_why: the needs' moves since the last mark are source k_'s (every write to need is followed by a mark)."""
        nw[:, k_] += need - nw_prev; nw_prev[:] = need
    def nw_clip():
        """need_why: what the clip to 0..1 took off (or added) goes back to the week's moves of that sign, pro rata (to
        the fade where there are none, as when the caller set a need past 1 at a pause)."""
        d_ = need - nw_prev
        up_ = np.maximum(nw, 0); dn_ = np.minimum(nw, 0); tu_ = up_.sum(1); td_ = dn_.sum(1)
        cut_ = np.minimum(d_, 0); lift_ = np.maximum(d_, 0)
        fu_ = np.divide(cut_, tu_, out=np.zeros_like(cut_), where=tu_ > 0)
        fd_ = np.divide(lift_, -td_, out=np.zeros_like(lift_), where=td_ < 0)
        nw[:] += up_ * fu_[:, None] - dn_ * fd_[:, None]
        nw[:, NW_FADE] += np.where(tu_ > 0, 0, cut_) + np.where(td_ < 0, 0, lift_)
        nw_prev[:] = need
    W_hist = []; M_hist = []; S_hist = []; A_hist = []
    reb = np.zeros((N, 2))                                       # v6: tension rebounds over the life (fit together, split)
    trouble = np.zeros(N); fortune = np.zeros(N)                 # v6: recent big events that went badly / well (decay over years)
    thr = np.full(N, 0.5); mem_s = np.zeros((N, C)); mem_f = np.zeros((N, C)); scar = np.zeros((N, C))   # v10 interpretation
    AXSEC = np.array(AXES["security vs freedom"], float) if P["thr_vec"] is None else \
        (AXSEC_SW if P["thr_vec"] == "schwartz" else np.asarray(P["thr_vec"], float))
    MIS_ON = any(P[k_] for k_ in ("mis_focus", "mis_mem", "mis_scar", "mis_mood", "mis_status"))
    DMS_ = 0.5 ** (1 / (52 * P["mem_pos"])); DMF_ = 0.5 ** (1 / (52 * P["mem_neg"]))
    hub_ = np.zeros(N); xp_ = np.zeros((N, C))                    # status held (hubris) and expertise by color, yearly
    def mem_rel():
        """What memory says of each color's ways, -1 (went badly) to 1 (went well), shrunk while there is little of it."""
        return (mem_s - mem_f) / (mem_s + mem_f + P["mem_eps"])
    wound = np.zeros(N)                                          # v6: a hard event leaves the person open for months
    moved = np.zeros(N)                                          # v6: this week brought new people around the person
    support = np.zeros(N)                                        # v6: being cared for (belonging and ties)
    had_ev = np.zeros(N, bool)
    events = {i: [] for i in log_lives}
    epi = {i: [] for i in log_lives}                             # v10: episodes a logged life may recall (for the game)
